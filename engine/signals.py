"""Signal layer — a literal port of SS_Cascade_v11_0_2.pine (build prompt §5).

The bar loop below mirrors the Pine script's global-scope execution order
statement for statement (section comments cite the Pine sections). All
governor/MTF inputs are pre-mapped onto exec bars by the confirmed-HTF rule
(engine/htf.py), which reproduces Pine's `expr[1] + lookahead_on` idiom —
including the property that a confirmed governor cross flag stays visible to
every exec bar of the following governor period (the Pine state machine
re-arms on each of those bars; so does this port).

Config divergence, flagged in the Phase 1 summary:
- v11_faithful: the Capitulation-V block clears campCounter (Pine literal).
- naiad_v0: charter §3.2 wins — V births a PROVISIONAL campaign
  (campCounter = not stage-aligned in the new direction; the standing
  upgrade check clears it when/once the stage confirms).

Decisions are computed on CLOSED exec bars only (invariant 1). The engine
emits events; fills belong to the trading layer.
"""

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from engine import indicators as ind
from engine.cells import INTERVAL_MS, MTF_SET, Cell
from engine.htf import map_htf_to_exec, take, take_bool

BIG = 100_000  # Pine's nz(..., 100000) sentinel for barssince


@dataclass
class SignalEvent:
    i: int                    # exec bar index into the loaded history
    evt: str                  # REGIME/STAGE/TAG/PRIME/CONFIRM/V/TPW/CLUSTER/X/REJECT
    dir: int                  # +1 long / -1 short / 0
    grade: str = "-"          # A+/A/B/C/V/-
    rc: int = 0
    zone: str = "-"           # Z1/Z2/Z3/-
    retr: float | None = None
    stop: float | None = None
    stage: int = 1
    tier: str = "-"           # full/provisional (REGIME + entry events)
    is_r1: bool = False
    is_add: bool = False      # R2+ PRIME or PRIME-backed CONFIRM
    arrow_visible: bool | None = None  # REGIME only (whipsaw filter, arrows only)
    reject_reason: str | None = None   # REJECT rows (funnel)
    subkey: str = "-"         # disambiguates same-bar same-type rows (TAG zone, reject kind)
    grade_uncapped: str = "-"  # PRIME only: grade ignoring the provisional B-cap
                               # (feeds the unthrottled structure-ladder shadow)


@dataclass
class SignalResult:
    """Everything downstream layers need, all confirmed-bar series."""
    exec_open_ms: np.ndarray
    o: np.ndarray
    h: np.ndarray
    l: np.ndarray
    c: np.ndarray
    v: np.ndarray
    e9x: np.ndarray
    e89x: np.ndarray
    e200x: np.ndarray
    atr_x: np.ndarray
    g_atr: np.ndarray         # mapped confirmed governor ATR
    g_e89: np.ndarray
    dir: np.ndarray           # campaign dir after each bar
    camp_counter: np.ndarray  # provisional flag after each bar
    stop_long: np.ndarray     # ratchet stop after each bar (nan = none)
    stop_short: np.ndarray
    active_zone: np.ndarray
    stage: np.ndarray         # 1/2 in campaign dir (2 = aligned)
    campaign_id: np.ndarray   # increments on every arming/V-birth; 0 = none
    events: list = field(default_factory=list)


def _prep_tf(df: pd.DataFrame, p: dict) -> dict:
    """Indicator pack for one timeframe's own kline series."""
    o = df["open"].to_numpy(float)
    h = df["high"].to_numpy(float)
    l = df["low"].to_numpy(float)
    c = df["close"].to_numpy(float)
    e9 = ind.ema(c, p["len_fast"])
    e89 = ind.ema(c, p["len_slow"])
    e200 = ind.ema(c, p["len_trend"])
    return {
        "open_ms": df["open_time"].to_numpy(np.int64),
        "o": o, "h": h, "l": l, "c": c,
        "e9": e9, "e89": e89, "e200": e200,
        "atr": ind.atr(h, l, c, p["atr_len"]),
        "bull": e9 > e89,
        "s2bu": e89 > e200,
        "s2be": e89 < e200,
        "bx": ind.crossover(e9, e89),
        "sx": ind.crossunder(e9, e89),
        "glo": ind.rolling_min(l, p["snipe_lookback"]),
        "ghi": ind.rolling_max(h, p["snipe_lookback"]),
    }


def compute_signals(cell: Cell, params: dict, exec_df: pd.DataFrame,
                    gov_df: pd.DataFrame, mtf_dfs: dict[str, pd.DataFrame],
                    v_births_provisional: bool) -> SignalResult:
    p = params
    n = len(exec_df)
    ex_open = exec_df["open_time"].to_numpy(np.int64)
    o = exec_df["open"].to_numpy(float)
    h = exec_df["high"].to_numpy(float)
    l = exec_df["low"].to_numpy(float)
    c = exec_df["close"].to_numpy(float)
    vol = exec_df["volume"].to_numpy(float)

    # ── EXECUTION-TF CALCULATIONS (Pine: exec layer) ──
    e9x = ind.ema(c, p["len_fast"])
    e89x = ind.ema(c, p["len_slow"])
    e200x = ind.ema(c, p["len_trend"])
    atr_x = ind.atr(h, l, c, p["atr_len"])
    vol_ma = ind.sma(vol, p["vol_len"])
    x9up = ind.crossover(c, e9x)
    x9dn = ind.crossunder(c, e9x)
    rib_up = ind.crossover(e9x, e89x)
    rib_dn = ind.crossunder(e9x, e89x)
    bar_range = h - l

    # ── Governor tuple, confirmed-visibility mapped (Pine: f_gov + security) ──
    gov = _prep_tf(gov_df, p)
    gidx = map_htf_to_exec(ex_open, gov["open_ms"], cell.tf_gov)
    gE9 = take(gov["e9"], gidx)
    gE89 = take(gov["e89"], gidx)
    gE200 = take(gov["e200"], gidx)
    gATR = take(gov["atr"], gidx)
    gIsBull = take_bool(gov["bull"], gidx)
    gS2B = take_bool(gov["s2bu"], gidx)
    gS2S = take_bool(gov["s2be"], gidx)
    gBullX = take_bool(gov["bx"], gidx)
    gBearX = take_bool(gov["sx"], gidx)
    gLo = take(gov["glo"], gidx)
    gHi = take(gov["ghi"], gidx)

    # ── MTF tuples (Pine: f_mtf x4), mapped the same way ──
    mtf = {}
    for tf in MTF_SET:
        t = _prep_tf(mtf_dfs[tf], p)
        midx = map_htf_to_exec(ex_open, t["open_ms"], tf)
        mtf[tf] = {
            "bx": take_bool(t["bx"], midx),
            "sx": take_bool(t["sx"], midx),
            "bull": take_bool(t["bull"], midx),
        }
    align_bull = mtf[cell.tf_align]["bull"]

    # ── Derived governor-layer series (Pine §4.1/§4.2) ──
    gBandTop = np.maximum(gE89, gE200)
    gBandBot = np.minimum(gE89, gE200)
    z1_prox, z2_prox, z3_prox = p["z1_prox"], p["z2_prox"], p["z3_prox"]
    z1Top, z1Bot = gE9 + z1_prox * gATR, gE9 - z1_prox * gATR
    z2Top, z2Bot = gE89 + z2_prox * gATR, gE89 - z2_prox * gATR
    z3Top, z3Bot = gBandTop + z3_prox * gATR, gBandBot - z3_prox * gATR

    prov_arm = p["provisional_arming"]
    prov_z12 = p["prov_zones"] == "Z1+Z2"
    zone_memory = cell.zone_memory
    cooldown = p["cooldown_bars"]
    max_rc = p["max_r_count"]
    snipe_on = p["snipe_on"]
    fib1, fib2 = p["fib1"], p["fib2"]
    cap_on, climax_mult = p["cap_on"], p["climax_mult"]
    cap_ext, cap_window, cap_vol_conf = p["cap_ext_atr"], p["cap_window"], p["cap_vol_conf"]
    tpw_on, cluster_n, cluster_win = p["tpw_on"], p["cluster_n"], p["cluster_win"]
    stop_buf = p["stop_buf_atr"]
    fail_win = p["fail_win"]
    structure_gate = p["structure_gate"]
    min_range, min_ribsep = p["min_bar_range_atr"], p["min_ribbon_sep_atr"]
    whipsaw = p["whipsaw_bars"]
    gov_ms = INTERVAL_MS[cell.tf_gov]

    # ── State (Pine `var` block) ──
    dir_ = 0
    r_count = 0
    last_sig_bar = -BIG
    stop_long = np.nan
    stop_short = np.nan
    camp_counter = False
    had_prime_ep = False
    tag_bar = [None, None, None]      # Z1/Z2/Z3 last tag bar
    tag_ext = [np.nan, np.nan, np.nan]
    snipe_origin = np.nan
    snipe_term = np.nan
    snipe_top = np.nan
    snipe_bot = np.nan
    snipe_frozen = False
    gov_seq = 0
    prev_gov_period = None
    last_bullx_seq = -BIG
    last_bearx_seq = -BIG
    beyond_bot_cnt = 0
    beyond_top_cnt = 0
    last_clx_dn = None
    last_clx_up = None
    last_mtf_bx = {tf: None for tf in MTF_SET}
    last_mtf_sx = {tf: None for tf in MTF_SET}
    prev_gS2B = False
    prev_gS2S = False
    prev_gBullX = False
    prev_gBearX = False
    campaign_seq = 0

    # Per-bar output arrays
    out_dir = np.zeros(n, dtype=np.int8)
    out_cc = np.zeros(n, dtype=bool)
    out_sl = np.full(n, np.nan)
    out_ss = np.full(n, np.nan)
    out_zone = np.zeros(n, dtype=np.int8)
    out_stage = np.ones(n, dtype=np.int8)
    out_camp = np.zeros(n, dtype=np.int64)
    events: list[SignalEvent] = []

    def isnan(x):
        return x != x

    for i in range(n):
        # Stage confirm events — edge on the mapped confirmed states (§4.1).
        stage_conf_bull = gS2B[i] and not prev_gS2B
        stage_conf_bear = gS2S[i] and not prev_gS2S

        # Aligned vs provisional classification of every cross (§4.1, ADD §1).
        aligned_bull_x = gBullX[i] and gS2B[i]
        aligned_bear_x = gBearX[i] and gS2S[i]
        counter_bull_x = gBullX[i] and not gS2B[i]
        counter_bear_x = gBearX[i] and not gS2S[i]
        arm_bull = gBullX[i] if prov_arm else aligned_bull_x
        arm_bear = gBearX[i] if prov_arm else aligned_bear_x

        # Whipsaw filter (arrows only, governor-bar counted). Pine order:
        # arrowOK computed from prior stamps, THEN this bar's cross stamps.
        gov_period = ex_open[i] // gov_ms
        if gov_period != prev_gov_period:
            gov_seq += 1
            prev_gov_period = gov_period
        bull_arrow_ok = gov_seq - last_bearx_seq >= whipsaw
        bear_arrow_ok = gov_seq - last_bullx_seq >= whipsaw
        if gBullX[i]:
            last_bullx_seq = gov_seq
        if gBearX[i]:
            last_bearx_seq = gov_seq

        stage_l = 2 if gS2B[i] else 1
        stage_s = 2 if gS2S[i] else 1

        # REGIME journal rows: edge-detected (first exec bar of visibility).
        # Pine's alert() re-fires on every exec bar of the governor period;
        # the journal wants the cross once, at the instant it became visible.
        if gBullX[i] and not prev_gBullX:
            events.append(SignalEvent(i, "REGIME", 1, stage=stage_l,
                                      tier="full" if aligned_bull_x else "provisional",
                                      arrow_visible=bool(bull_arrow_ok)))
        if gBearX[i] and not prev_gBearX:
            events.append(SignalEvent(i, "REGIME", -1, stage=stage_s,
                                      tier="full" if aligned_bear_x else "provisional",
                                      arrow_visible=bool(bear_arrow_ok)))
        if stage_conf_bull:
            events.append(SignalEvent(i, "STAGE", 1, stage=2))
        if stage_conf_bear:
            events.append(SignalEvent(i, "STAGE", -1, stage=2))

        # ── ARMING (§4.1, ADD §1) — literal, including re-arming on every
        # exec bar of the cross-visibility window. ──
        if arm_bull:
            if dir_ != 1 or not gBullX[i] or not prev_gBullX:
                campaign_seq += 1  # new campaign at first visibility bar
            dir_ = 1
            r_count = 0
            stop_short = np.nan
            camp_counter = counter_bull_x
            last_sig_bar = i
            had_prime_ep = False
            tag_bar = [None, None, None]
            tag_ext = [np.nan, np.nan, np.nan]
            snipe_origin = gLo[i]
            snipe_term = h[i]
            snipe_top = np.nan
            snipe_bot = np.nan
            snipe_frozen = False
        if arm_bear:
            if dir_ != -1 or not gBearX[i] or not prev_gBearX:
                campaign_seq += 1
            dir_ = -1
            r_count = 0
            stop_long = np.nan
            camp_counter = counter_bear_x
            last_sig_bar = i
            had_prime_ep = False
            tag_bar = [None, None, None]
            tag_ext = [np.nan, np.nan, np.nan]
            snipe_origin = gHi[i]
            snipe_term = l[i]
            snipe_top = np.nan
            snipe_bot = np.nan
            snipe_frozen = False

        # ADD §1: provisional upgrades to full on stage confirm in-direction.
        if camp_counter and ((dir_ == 1 and gS2B[i]) or (dir_ == -1 and gS2S[i])):
            camp_counter = False

        # ── ZONE ARMING & TAG TRACKING (§4.2) ──
        stage_aligned = gS2B[i] if dir_ == 1 else (gS2S[i] if dir_ == -1 else False)
        z1_armed = dir_ != 0
        z2_armed = dir_ != 0 and (not camp_counter or prov_z12)
        z3_armed = dir_ != 0 and stage_aligned

        def _tag_now(armed, top, bot):
            if not armed or isnan(top):
                return False
            return (l[i] <= top) if dir_ == 1 else (h[i] >= bot)

        tag_now = [_tag_now(z1_armed, z1Top[i], z1Bot[i]),
                   _tag_now(z2_armed, z2Top[i], z2Bot[i]),
                   _tag_now(z3_armed, z3Top[i], z3Bot[i])]
        fresh = [tag_now[k] and (tag_bar[k] is None or i - tag_bar[k] > zone_memory)
                 for k in range(3)]
        if any(fresh):
            had_prime_ep = False
        for k in range(3):
            if tag_now[k]:
                extk = l[i] if dir_ == 1 else h[i]
                if fresh[k] or isnan(tag_ext[k]):
                    tag_ext[k] = extk
                else:
                    tag_ext[k] = min(tag_ext[k], extk) if dir_ == 1 else max(tag_ext[k], extk)
                tag_bar[k] = i
            if fresh[k]:
                events.append(SignalEvent(i, "TAG", dir_, zone=f"Z{k+1}",
                                          stage=stage_l if dir_ == 1 else stage_s,
                                          tier="provisional" if camp_counter else "full",
                                          subkey=f"Z{k+1}"))

        # ADD §4: terminus freezes at the first Z2/Z3 tag of the campaign.
        if (tag_now[1] or tag_now[2]) and dir_ != 0 and not snipe_frozen:
            snipe_frozen = True

        # Sniper leg geometry (§4.5, ADD §4).
        if dir_ != 0 and not isnan(snipe_origin):
            if not snipe_frozen:
                if dir_ == 1:
                    snipe_term = h[i] if isnan(snipe_term) else max(snipe_term, h[i])
                else:
                    snipe_term = l[i] if isnan(snipe_term) else min(snipe_term, l[i])
            leg_hi = snipe_term if dir_ == 1 else snipe_origin
            leg_lo = snipe_origin if dir_ == 1 else snipe_term
            fib_a = leg_hi - fib1 * (leg_hi - leg_lo) if dir_ == 1 else leg_lo + fib1 * (leg_hi - leg_lo)
            fib_b = leg_hi - fib2 * (leg_hi - leg_lo) if dir_ == 1 else leg_lo + fib2 * (leg_hi - leg_lo)
            snipe_top = max(fib_a, fib_b)
            snipe_bot = min(fib_a, fib_b)

        # "Recently tagged" + innermost priority Z3 > Z2 > Z1 (§4.2).
        rec = [z1_armed and tag_bar[0] is not None and i - tag_bar[0] <= zone_memory,
               z2_armed and tag_bar[1] is not None and i - tag_bar[1] <= zone_memory,
               z3_armed and tag_bar[2] is not None and i - tag_bar[2] <= zone_memory]
        active_zone = 3 if rec[2] else 2 if rec[1] else 1 if rec[0] else 0
        z_top_a = (z3Top[i], z2Top[i], z1Top[i], np.nan)[3 - active_zone] if active_zone else np.nan
        z_bot_a = (z3Bot[i], z2Bot[i], z1Bot[i], np.nan)[3 - active_zone] if active_zone else np.nan
        tag_ext_a = (tag_ext[2], tag_ext[1], tag_ext[0], np.nan)[3 - active_zone] if active_zone else np.nan

        # ── TRIGGERS (§4.3) ──
        cool_ok = i - last_sig_bar >= cooldown
        rcap_ok = max_rc == 0 or r_count < max_rc
        rib_sep_ok = (not isnan(atr_x[i]) and abs(e9x[i] - e89x[i]) >= min_ribsep * atr_x[i]) or active_zone == 3
        range_ok = not isnan(atr_x[i]) and bar_range[i] >= min_range * atr_x[i]
        struct_ok_l = (not structure_gate) or gS2B[i] or camp_counter
        struct_ok_s = (not structure_gate) or gS2S[i] or camp_counter

        x9up_prev = x9up[i - 1] if i > 0 else False
        x9dn_prev = x9dn[i - 1] if i > 0 else False
        prime_l = (dir_ == 1 and struct_ok_l and active_zone > 0 and x9up_prev
                   and c[i] > e9x[i] and c[i] >= c[i - 1] and range_ok and rib_sep_ok
                   and cool_ok and rcap_ok)
        prime_s = (dir_ == -1 and struct_ok_s and active_zone > 0 and x9dn_prev
                   and c[i] < e9x[i] and c[i] <= c[i - 1] and range_ok and rib_sep_ok
                   and cool_ok and rcap_ok)

        confirm_x_l = dir_ == 1 and rib_up[i] and cool_ok
        confirm_x_s = dir_ == -1 and rib_dn[i] and cool_ok

        # ── Funnel: raw reclaim attempts that failed a gate (charter §3.5.6) ──
        raw_reclaim_l = dir_ == 1 and x9up_prev and c[i] > e9x[i] and c[i] >= c[i - 1]
        raw_reclaim_s = dir_ == -1 and x9dn_prev and c[i] < e9x[i] and c[i] <= c[i - 1]
        if (raw_reclaim_l or raw_reclaim_s) and not (prime_l or prime_s):
            d = 1 if raw_reclaim_l else -1
            reason = ("no_zone" if active_zone == 0 else
                      "structure" if not (struct_ok_l if d == 1 else struct_ok_s) else
                      "bar_range" if not range_ok else
                      "ribbon_sep" if not rib_sep_ok else
                      "cooldown" if not cool_ok else
                      "r_cap")
            events.append(SignalEvent(i, "REJECT", d, reject_reason=reason,
                                      zone=f"Z{active_zone}" if active_zone else "-",
                                      subkey="prime"))

        # ── CAPITULATION V (§4.6) ──
        climax_dn = (cap_on and not isnan(vol_ma[i]) and vol[i] >= climax_mult * vol_ma[i]
                     and c[i] < o[i] and not isnan(gE89[i]) and l[i] <= gE89[i] - cap_ext * gATR[i])
        climax_up = (cap_on and not isnan(vol_ma[i]) and vol[i] >= climax_mult * vol_ma[i]
                     and c[i] > o[i] and not isnan(gE89[i]) and h[i] >= gE89[i] + cap_ext * gATR[i])
        if climax_dn:
            last_clx_dn = i
        if climax_up:
            last_clx_up = i
        bs_clx_dn = i - last_clx_dn if last_clx_dn is not None else BIG
        bs_clx_up = i - last_clx_up if last_clx_up is not None else BIG
        prev_band_top = gBandTop[i - 1] if i > 0 else np.nan
        prev_band_bot = gBandBot[i - 1] if i > 0 else np.nan
        x_band_up = (not isnan(gBandTop[i]) and c[i] > gBandTop[i]
                     and i > 0 and not isnan(prev_band_top) and c[i - 1] <= prev_band_top)
        x_band_dn = (not isnan(gBandBot[i]) and c[i] < gBandBot[i]
                     and i > 0 and not isnan(prev_band_bot) and c[i - 1] >= prev_band_bot)
        cap_l = cap_on and x_band_up and bs_clx_dn <= cap_window and not isnan(vol_ma[i]) and vol[i] >= cap_vol_conf * vol_ma[i]
        cap_s = cap_on and x_band_dn and bs_clx_up <= cap_window and not isnan(vol_ma[i]) and vol[i] >= cap_vol_conf * vol_ma[i]

        # ── STATE UPDATES (§4.3/§4.6) — Pine order preserved. ──
        if prime_l or prime_s:
            r_count += 1
            had_prime_ep = True

        grade_c_l = confirm_x_l and not had_prime_ep and struct_ok_l and active_zone > 0
        grade_c_s = confirm_x_s and not had_prime_ep and struct_ok_s and active_zone > 0
        confirm_l = (confirm_x_l and had_prime_ep) or grade_c_l
        confirm_s = (confirm_x_s and had_prime_ep) or grade_c_s
        # ADD §2: a confirm-only re-cross failing the gate is dropped entirely
        # — journal it as a funnel reject (it produces no marker/stop/trade).
        if confirm_x_l and not had_prime_ep and not grade_c_l:
            events.append(SignalEvent(i, "REJECT", 1, reject_reason=(
                "c_gate_no_zone" if active_zone == 0 else "c_gate_structure"), subkey="confirm"))
        if confirm_x_s and not had_prime_ep and not grade_c_s:
            events.append(SignalEvent(i, "REJECT", -1, reject_reason=(
                "c_gate_no_zone" if active_zone == 0 else "c_gate_structure"), subkey="confirm"))

        # V arms/enters like a PRIME (campaign reversal); clears the leg.
        v_birth = False
        if cap_l and dir_ != 1:
            dir_ = 1
            r_count = 0
            campaign_seq += 1
            v_birth = True
            camp_counter = (not gS2B[i]) if v_births_provisional else False
            stop_short = np.nan
            had_prime_ep = False
            tag_bar = [None, None, None]
            tag_ext = [np.nan, np.nan, np.nan]
            snipe_origin = np.nan
            snipe_term = np.nan
            snipe_top = np.nan
            snipe_bot = np.nan
            snipe_frozen = False
        if cap_s and dir_ != -1:
            dir_ = -1
            r_count = 0
            campaign_seq += 1
            v_birth = True
            camp_counter = (not gS2S[i]) if v_births_provisional else False
            stop_long = np.nan
            had_prime_ep = False
            tag_bar = [None, None, None]
            tag_ext = [np.nan, np.nan, np.nan]
            snipe_origin = np.nan
            snipe_term = np.nan
            snipe_top = np.nan
            snipe_bot = np.nan
            snipe_frozen = False

        # Ratchet stop on PRIME / CONFIRM / V (na-safe, one-way — invariant 5).
        entry_l = ((prime_l or confirm_l) and dir_ == 1) or cap_l
        entry_s = ((prime_s or confirm_s) and dir_ == -1) or cap_s
        if entry_l:
            new_stop = l[i] - stop_buf * atr_x[i]
            stop_long = new_stop if isnan(stop_long) else max(stop_long, new_stop)
            last_sig_bar = i
        if entry_s:
            new_stop = h[i] + stop_buf * atr_x[i]
            stop_short = new_stop if isnan(stop_short) else min(stop_short, new_stop)
            last_sig_bar = i

        is_r1_l = prime_l and r_count == 1
        is_r2_l = prime_l and r_count >= 2
        is_r1_s = prime_s and r_count == 1
        is_r2_s = prime_s and r_count >= 2
        if (is_r1_l or is_r1_s) and not snipe_frozen:
            snipe_frozen = True

        # ── GRADES (§4.4, ADD §1/§3) ──
        ap_cont = (not isnan(snipe_top) and not isnan(tag_ext_a) and active_zone > 0
                   and tag_ext_a >= max(snipe_bot, z_bot_a) and tag_ext_a <= min(snipe_top, z_top_a))
        g_ap_l = prime_l and snipe_on and ap_cont and not camp_counter
        g_a_l = prime_l and not g_ap_l and align_bull[i] and not camp_counter
        g_ap_s = prime_s and snipe_on and ap_cont and not camp_counter
        g_a_s = prime_s and not g_ap_s and not align_bull[i] and not camp_counter

        # ── FAILURE X (§4.8) ──
        beyond_bot_cnt = beyond_bot_cnt + 1 if (not isnan(gBandBot[i]) and c[i] < gBandBot[i]) else 0
        beyond_top_cnt = beyond_top_cnt + 1 if (not isnan(gBandTop[i]) and c[i] > gBandTop[i]) else 0
        fail_l = dir_ == 1 and beyond_bot_cnt == fail_win
        fail_s = dir_ == -1 and beyond_top_cnt == fail_win
        if fail_l:
            dir_ = 0
            stop_long = np.nan
        if fail_s:
            dir_ = 0
            stop_short = np.nan

        # ── TPW & MTF CLUSTER (§4.7) — barssince includes the current bar. ──
        for tf in MTF_SET:
            if mtf[tf]["bx"][i]:
                last_mtf_bx[tf] = i
            if mtf[tf]["sx"][i]:
                last_mtf_sx[tf] = i
        cnt_bull_rec = sum(1 for tf in MTF_SET
                           if last_mtf_bx[tf] is not None and i - last_mtf_bx[tf] <= cluster_win)
        cnt_bear_rec = sum(1 for tf in MTF_SET
                           if last_mtf_sx[tf] is not None and i - last_mtf_sx[tf] <= cluster_win)
        any_bull_now = any(mtf[tf]["bx"][i] for tf in MTF_SET)
        any_bear_now = any(mtf[tf]["sx"][i] for tf in MTF_SET)
        tpw_l = tpw_on and dir_ == 1 and not isnan(stop_long) and cnt_bear_rec >= cluster_n and any_bear_now
        tpw_s = tpw_on and dir_ == -1 and not isnan(stop_short) and cnt_bull_rec >= cluster_n and any_bull_now
        cluster_bull = cnt_bull_rec >= cluster_n and any_bull_now
        cluster_bear = cnt_bear_rec >= cluster_n and any_bear_now

        # ── retr (ADD §5): tag-extreme retracement fraction of the leg. ──
        retr_ok = (not isnan(snipe_origin) and not isnan(snipe_term) and not isnan(tag_ext_a)
                   and ((snipe_term > snipe_origin) if dir_ == 1 else (snipe_origin > snipe_term)))
        if retr_ok:
            retr_val = ((snipe_term - tag_ext_a) / (snipe_term - snipe_origin) if dir_ == 1
                        else (tag_ext_a - snipe_term) / (snipe_origin - snipe_term))
        else:
            retr_val = None

        # ── Event emission (journal layer formats/timestamps them) ──
        zone_str = f"Z{active_zone}" if active_zone else "-"
        tier_str = "provisional" if camp_counter else "full"
        cur_stage = stage_l if dir_ == 1 else stage_s if dir_ == -1 else 1
        if prime_l or prime_s:
            d = 1 if prime_l else -1
            grade = ("A+" if (g_ap_l or g_ap_s) else
                     "A" if (g_a_l or g_a_s) else "B")
            # Uncapped grade (unthrottled-ladder shadow): same rules with the
            # provisional cap removed.
            if snipe_on and ap_cont:
                grade_un = "A+"
            elif (align_bull[i] if d == 1 else not align_bull[i]):
                grade_un = "A"
            else:
                grade_un = "B"
            events.append(SignalEvent(i, "PRIME", d, grade=grade, rc=r_count,
                                      zone=zone_str, retr=retr_val,
                                      stop=stop_long if d == 1 else stop_short,
                                      stage=cur_stage, tier=tier_str,
                                      is_r1=(is_r1_l or is_r1_s),
                                      is_add=(is_r2_l or is_r2_s),
                                      grade_uncapped=grade_un))
        if confirm_l or confirm_s:
            d = 1 if confirm_l else -1
            is_c = grade_c_l or grade_c_s
            events.append(SignalEvent(i, "CONFIRM", d, grade="C" if is_c else "-",
                                      rc=r_count, zone=zone_str,
                                      stop=stop_long if d == 1 else stop_short,
                                      stage=cur_stage, tier=tier_str,
                                      is_add=not is_c))
        if cap_l or cap_s:
            d = 1 if cap_l else -1
            events.append(SignalEvent(i, "V", d, grade="V", rc=r_count,
                                      stop=stop_long if d == 1 else stop_short,
                                      stage=cur_stage, tier=tier_str))
        if tpw_l or tpw_s:
            d = 1 if tpw_l else -1
            events.append(SignalEvent(i, "TPW", d, rc=r_count,
                                      stop=stop_long if d == 1 else stop_short,
                                      stage=cur_stage))
        if cluster_bull:
            events.append(SignalEvent(i, "CLUSTER", 1, stage=stage_l, subkey="bull"))
        if cluster_bear:
            events.append(SignalEvent(i, "CLUSTER", -1, stage=stage_s, subkey="bear"))
        if fail_l or fail_s:
            d = 1 if fail_l else -1
            events.append(SignalEvent(i, "X", d, rc=r_count,
                                      stage=stage_l if d == 1 else stage_s))

        # ── Per-bar state snapshot (post-update, i.e. as of this bar's close) ──
        out_dir[i] = dir_
        out_cc[i] = camp_counter
        out_sl[i] = stop_long
        out_ss[i] = stop_short
        out_zone[i] = active_zone
        out_stage[i] = 2 if (dir_ == 1 and gS2B[i]) or (dir_ == -1 and gS2S[i]) else 1
        out_camp[i] = campaign_seq if dir_ != 0 else 0

        prev_gS2B = gS2B[i]
        prev_gS2S = gS2S[i]
        prev_gBullX = gBullX[i]
        prev_gBearX = gBearX[i]

    return SignalResult(
        exec_open_ms=ex_open, o=o, h=h, l=l, c=c, v=vol,
        e9x=e9x, e89x=e89x, e200x=e200x, atr_x=atr_x,
        g_atr=gATR, g_e89=gE89,
        dir=out_dir, camp_counter=out_cc, stop_long=out_sl, stop_short=out_ss,
        active_zone=out_zone, stage=out_stage, campaign_id=out_camp,
        events=events,
    )
