"""Shadow lines (charter §3.5, build prompt §7) — computed every bar, never
traded. Outcomes are columns on journal rows, not separate books.

Conventions (documented for the autopsy):
- Shadow exit prices simulate on RAW prices (no slippage/fees) and report
  PER-UNIT R: (exit - fill)/(fill - stop_at_entry), sign-adjusted. Costs are
  near-identical across exit variants, so gross per-unit R is the comparable
  quantity; realized_r on the row stays net-of-costs.
- mfe_r / mae_r / give_back_r / postexit_cont are PER-UNIT R too (a full
  stop-out is -1R regardless of tranche size; multiply by size_r for
  campaign-R accounting).
- A tranche's shadow exits resolve no later than campaign death (X / opposite
  cross / V-reversal flatten). Tranches whose campaign is still open at data
  end stay unresolved and their EXIT rows are buffered (idempotent journal:
  a later run emits them).

Candidate exits raced in Phase 2 (X-A is the pre-registered starting
hypothesis; deterministic mechanizations below):
- X-A: survival ratchet untouched until a closed bar sits beyond the exec 200
  on the trade's side; from engagement, trail = e200 -/+ 0.5 x exec-ATR,
  one-way ratchet, closed bars only.
- X-B: X-A + bank 50% at the next open after the first TPW.
- X-C: X-A + bank 50% at the next open after the first extension close
  (close >= 2 x exec-ATR beyond the exec 9, trade side).
- X-D: mechanized Playbook stack — 25% at first TPW, 25% at first extension,
  remainder on the X-A trail / campaign death.
"""

from dataclasses import dataclass

import numpy as np

from engine import indicators as ind
from engine.journal import iso
from engine.signals import SignalResult
from engine.trading import Tranche, TradeResult


@dataclass
class TrancheEnrichment:
    resolved: bool
    mfe_r: float | None = None
    mae_r: float | None = None
    give_back_r: float | None = None
    cohort: str | None = None
    postexit_cont_1: float | None = None
    postexit_cont_5: float | None = None
    postexit_cont_20: float | None = None
    engagement_flags: dict | None = None
    shadow: dict | None = None


def _campaign_span(sig: SignalResult, d: int, fill_i: int) -> tuple[int, int | None]:
    """[fill_i, end] span of the position's direction run; end None if still
    running at data end. The run ends when dir flips or dies (X / opposite
    cross / V-reversal) — the real book flattens at the open of end+1. A
    same-direction re-arm increments the campaign id but does NOT flatten,
    so the span follows dir, not campaign_id."""
    dirs = sig.dir
    n = len(dirs)
    j = fill_i
    while j + 1 < n and dirs[j + 1] == d:
        j += 1
    return fill_i, (None if j == n - 1 and dirs[j] == d else j)


def _sim_stop_exit(sig: SignalResult, d: int, fill_i: int, camp_end: int | None,
                   stop_series: np.ndarray) -> tuple[float, int] | None:
    """First exit of a stop-order series from bar fill_i+1 on. Stop working
    during bar j = series value at j-1. Campaign death flattens at the open
    of camp_end+1. Returns (exit_px, exit_bar) or None if unresolved."""
    n = len(sig.c)
    last = camp_end if camp_end is not None else n - 1
    for j in range(fill_i + 1, last + 2):
        if j >= n:
            return None
        s = stop_series[j - 1]
        if not np.isnan(s):
            if (sig.o[j] - s) * d <= 0:
                return float(sig.o[j]), j
            hit = sig.l[j] <= s if d == 1 else sig.h[j] >= s
            if hit:
                return float(s), j
        if camp_end is not None and j == camp_end + 1:
            return float(sig.o[j]), j
    return None


def _unit_r(tr: Tranche, px: float) -> float:
    unit_risk = (tr.fill_px - tr.stop_at_entry) * tr.dir
    return (px - tr.fill_px) * tr.dir / unit_risk


def _xa_series(sig: SignalResult, tr: Tranche, buf: float,
               last: int) -> tuple[np.ndarray, int | None]:
    """X-A shadow stop series for one tranche + engagement bar (or None)."""
    n = len(sig.c)
    d = tr.dir
    real = sig.stop_long if d == 1 else sig.stop_short
    series = np.full(n, np.nan)
    engaged_at = None
    val = np.nan
    for j in range(tr.fill_i, min(last, n - 1) + 1):
        if engaged_at is None and (sig.c[j] - sig.e200x[j]) * d > 0:
            engaged_at = j
        if engaged_at is None:
            val = real[j]                       # survival phase: native ratchet
        else:
            trail = sig.e200x[j] - d * buf * sig.atr_x[j]
            if np.isnan(val):
                val = trail
            else:
                val = max(val, trail) if d == 1 else min(val, trail)
            if not np.isnan(real[j]):           # never looser than the ratchet
                val = max(val, real[j]) if d == 1 else min(val, real[j])
        series[j] = val
    return series, engaged_at


def _alt_anchor_series(sig: SignalResult, tr: Tranche, entry_bars: list[int],
                       stop_buf: float, atr_frozen: float | None,
                       trigger_offset: bool, last: int) -> np.ndarray:
    """Variant survival-ratchet series: same entry events, different anchor
    (trigger-bar extreme) or frozen buffer (ATR at campaign engagement)."""
    n = len(sig.c)
    d = tr.dir
    series = np.full(n, np.nan)
    val = np.nan
    ebars = sorted(b for b in entry_bars if tr.fill_i - 1 <= b <= last)
    k = 0
    for j in range(tr.fill_i - 1, min(last, n - 1) + 1):
        while k < len(ebars) and ebars[k] == j:
            e = ebars[k]
            anchor_bar = max(0, e - 1) if trigger_offset else e
            ext = sig.l[anchor_bar] if d == 1 else sig.h[anchor_bar]
            buf_atr = atr_frozen if atr_frozen is not None else sig.atr_x[e]
            cand = ext - d * stop_buf * buf_atr
            val = cand if np.isnan(val) else (max(val, cand) if d == 1 else min(val, cand))
            k += 1
        series[j] = val
    return series


def enrich_tranche(sig: SignalResult, tr: Tranche, sh_cfg: dict,
                   stop_buf: float, campaign_entry_bars: dict,
                   rib_cross: dict) -> TrancheEnrichment:
    n = len(sig.c)
    d = tr.dir
    if not tr.exited:
        return TrancheEnrichment(resolved=False)
    _, camp_end = _campaign_span(sig, d, tr.fill_i)
    if camp_end is None:
        return TrancheEnrichment(resolved=False)  # campaign still open
    if tr.exit_i + 20 >= n:
        return TrancheEnrichment(resolved=False)  # postexit window incomplete

    unit_risk = (tr.fill_px - tr.stop_at_entry) * d
    # Excursions: include the exit bar's extremes for intra-bar stop exits,
    # exclude them for open fills (flatten/gap — the exit preceded the bar).
    peak, trough = tr.peak, tr.trough
    if tr.exit_reason == "stop":
        j = tr.exit_i
        if d == 1:
            peak = max(peak, sig.h[j]); trough = min(trough, sig.l[j])
        else:
            peak = min(peak, sig.l[j]); trough = max(trough, sig.h[j])
    mfe = (peak - tr.fill_px) * d / unit_risk
    mae = (trough - tr.fill_px) * d / unit_risk
    realized_unit = _unit_r(tr, tr.exit_px)
    cohort = ("NEVER_GREEN" if mfe <= 0 else
              "STILLBORN" if mfe < 0.5 else
              "FADED" if mfe < 1.0 else "PROTECTED")

    def cont(k):
        j = tr.exit_i + k
        return round((sig.c[j] - tr.exit_px) * d / unit_risk, 6) + 0.0

    # --- candidate exits ---
    buf = sh_cfg["xa_trail_buf_atr"]
    last = camp_end
    xa_series, engaged_at = _xa_series(sig, tr, buf, last)
    xa = _sim_stop_exit(sig, d, tr.fill_i, camp_end, xa_series)
    if xa is None:
        return TrancheEnrichment(resolved=False)
    xa_r = _unit_r(tr, xa[0])

    # first TPW / extension after fill, within the campaign
    tpw_i = tr.first_tpw_i if tr.first_tpw_i is not None and tr.first_tpw_i <= last else None
    ext_i = None
    for j in range(tr.fill_i, last + 1):
        if not np.isnan(sig.atr_x[j]) and (sig.c[j] - sig.e9x[j]) * d >= sh_cfg["xc_ext_atr"] * sig.atr_x[j]:
            ext_i = j
            break

    # 1.0.8 (TC-4): ext_before_exit is windowed to THIS tranche's life
    # [fill_i, exit_i] — the 1.0.7 flag ran to campaign death and was
    # misnamed (R4 named gap). ext_i above (campaign window) still drives
    # the X-C/X-D shadow partials: shadow semantics are unchanged.
    ext_life_i = None
    for j in range(tr.fill_i, tr.exit_i + 1):
        if not np.isnan(sig.atr_x[j]) and (sig.c[j] - sig.e9x[j]) * d >= sh_cfg["xc_ext_atr"] * sig.atr_x[j]:
            ext_life_i = j
            break
    ext_i_offset = mfe_at_ext_r = None
    if ext_life_i is not None:
        ext_i_offset = ext_life_i - tr.fill_i
        fav = sig.h[tr.fill_i:ext_life_i + 1] if d == 1 else \
            sig.l[tr.fill_i:ext_life_i + 1]
        pk = float(fav.max()) if d == 1 else float(fav.min())
        pk = max(pk, tr.fill_px) if d == 1 else min(pk, tr.fill_px)
        mfe_at_ext_r = round((pk - tr.fill_px) * d / unit_risk, 6) + 0.0

    def blend(parts: list[tuple[float, float]]) -> float:
        return round(sum(f * r for f, r in parts), 6) + 0.0

    def partial_r(bar: int | None) -> float | None:
        if bar is None or bar + 1 >= n or (xa is not None and bar + 1 > xa[1]):
            return None
        return _unit_r(tr, float(sig.o[bar + 1]))

    tpw_r = partial_r(tpw_i)
    ext_r = partial_r(ext_i)
    xb_r = blend([(sh_cfg["xb_tpw_partial"], tpw_r),
                  (1 - sh_cfg["xb_tpw_partial"], xa_r)]) if tpw_r is not None else round(xa_r, 6)
    xc_r = blend([(sh_cfg["xc_partial"], ext_r),
                  (1 - sh_cfg["xc_partial"], xa_r)]) if ext_r is not None else round(xa_r, 6)
    parts, rem = [], 1.0
    if tpw_r is not None:
        parts.append((sh_cfg["xd_tpw_partial"], tpw_r)); rem -= sh_cfg["xd_tpw_partial"]
    if ext_r is not None:
        parts.append((sh_cfg["xd_ext_partial"], ext_r)); rem -= sh_cfg["xd_ext_partial"]
    parts.append((rem, xa_r))
    xd_r = blend(parts)

    # --- stop-anchor variants (same ratchet events, different anchor/buffer) ---
    entry_bars = campaign_entry_bars.get((tr.campaign, d), [])
    alt_anchor = _alt_anchor_series(sig, tr, entry_bars, stop_buf, None, True, last)
    alt_volbuf = _alt_anchor_series(sig, tr, entry_bars, stop_buf,
                                    float(sig.atr_x[entry_bars[0]]) if entry_bars else None,
                                    False, last)
    a_exit = _sim_stop_exit(sig, d, tr.fill_i, camp_end, alt_anchor)
    v_exit = _sim_stop_exit(sig, d, tr.fill_i, camp_end, alt_volbuf)

    # --- entry variant: first exec 9/89 cross in campaign direction ---
    alt = rib_cross.get((tr.campaign, d))
    entry_alt_px = entry_alt_t = entry_alt_stop = None
    if alt is not None:
        entry_alt_px = round(float(sig.c[alt]), 8)
        entry_alt_t = iso(int(sig.exec_open_ms[alt]))
        ext = sig.l[alt] if d == 1 else sig.h[alt]
        entry_alt_stop = round(float(ext - d * stop_buf * sig.atr_x[alt]), 8)

    shadow = {
        "entry_alt_px": entry_alt_px,
        "entry_alt_t": entry_alt_t,
        "entry_alt_stop": entry_alt_stop,
        "ladder_strict": bool(tr.born_aligned),
        "ladder_unthrottled_grade": tr.grade_uncapped if tr.kind != "V" else "V",
        "ladder_unthrottled_size_r": (0.5 if tr.grade_uncapped in ("A+", "A")
                                      else 0.25) if tr.kind == "R1" else
                                     (0.25 if tr.kind == "V" else 0.5),
        "stop_alt_anchor": round(float(alt_anchor[tr.fill_i]), 8) if not np.isnan(alt_anchor[tr.fill_i]) else None,
        "stop_alt_volbuf": round(float(alt_volbuf[tr.fill_i]), 8) if not np.isnan(alt_volbuf[tr.fill_i]) else None,
        "stop_alt_anchor_exit_r": round(_unit_r(tr, a_exit[0]), 6) if a_exit else None,
        "stop_alt_volbuf_exit_r": round(_unit_r(tr, v_exit[0]), 6) if v_exit else None,
        "size_full_r1": (round(tr.realized_r / tr.size_r, 6)
                         if tr.kind in ("R1", "V") else None),
        "size_big_adds": (round(tr.realized_r / tr.size_r, 6) if tr.kind == "ADD"
                          else round(tr.realized_r, 6)),
        "exit_XA": round(xa_r, 6),
        "exit_XB": xb_r,
        "exit_XC": xc_r,
        "exit_XD": xd_r,
    }
    flags = {
        "xa_engaged_before_exit": bool(engaged_at is not None and engaged_at < xa[1]),
        "tpw_before_exit": bool(tpw_i is not None),
        "ext_before_exit": bool(ext_life_i is not None),
        "ext_i_offset": ext_i_offset,
        "mfe_at_ext_r": mfe_at_ext_r,
    }
    return TrancheEnrichment(
        resolved=True,
        mfe_r=round(mfe, 6), mae_r=round(mae, 6),
        give_back_r=round(mfe - realized_unit, 6),
        cohort=cohort,
        postexit_cont_1=cont(1), postexit_cont_5=cont(5), postexit_cont_20=cont(20),
        engagement_flags=flags, shadow=shadow)


def build_shadow_context(sig: SignalResult, trades: TradeResult) -> tuple[dict, dict]:
    """Pre-compute per-campaign entry-event bars and first rib-cross bars."""
    campaign_entry_bars: dict[tuple[int, int], list[int]] = {}
    for ev in sig.events:
        if ev.evt in ("PRIME", "V") or (ev.evt == "CONFIRM"):
            camp = int(sig.campaign_id[ev.i])
            if camp:
                campaign_entry_bars.setdefault((camp, ev.dir), []).append(ev.i)

    rib_up = ind.crossover(sig.e9x, sig.e89x)
    rib_dn = ind.crossunder(sig.e9x, sig.e89x)
    rib_cross: dict[tuple[int, int], int] = {}
    for j in range(len(sig.c)):
        camp = int(sig.campaign_id[j])
        if not camp:
            continue
        d = int(sig.dir[j])
        if d == 1 and rib_up[j] and (camp, 1) not in rib_cross:
            rib_cross[(camp, 1)] = j
        elif d == -1 and rib_dn[j] and (camp, -1) not in rib_cross:
            rib_cross[(camp, -1)] = j
    return campaign_entry_bars, rib_cross
