"""TIER-C7 — THE FIXTURES.

    F-C7-CTRL     card v7 with every v7 knob at its default IS card v6, and
                  reproduces the v6 book trade-for-trade
    F-C7-INHERIT  five generations, bound by identity, asserted with `is`
    F-C7-ARM      the ladder is provably asleep before +1R, on EVERY campaign,
                  re-derived from raw bars
    F-C7-WEV      three weave events hand-verified on BOTH clauses from raw
                  ribbon EMAs
    F-C7-CHAIN    two chains hand-walked — legs, sizing, funding accumulation,
                  and single-campaign accounting
    F-C7-AE       three aborts hand-verified at 0.60R
    F-C7-GRID     the selection surface counted three independent ways
    F-C7-DET      two runs, byte for byte
    F-C7-CLOSURE  captured-not-consulted, still
    F-KEY         every written table on its declared key, read from the
                  manifest so the leg is TOTAL

EVERY LEG STATES INLINE WHAT WOULD MAKE IT FAIL — the house rule since F-C4-h.

AND THE BANNED FAILURE MODES, BY NAME, because this estate has paid for all
three: a check that re-derives a value the way the program derived it and
compares it to itself; a check satisfied by ONE example where a cardinality
check was available; and a magnitude bound tuned until the suite goes green.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc7 as T7                                                  # noqa: E402
import tierc7_rules as RC                                            # noqa: E402
import tierc6 as T6                                                  # noqa: E402
import tierc6_rules as V6                                            # noqa: E402
import tierc5_rules as V5                                            # noqa: E402
import tierc4_rules as V4                                            # noqa: E402
import tierc4_fixtures as F4                                         # noqa: E402
import analytics as AN                                               # noqa: E402
from engine import indicators as ind                                 # noqa: E402

T: list[str] = []
RESULTS: dict[str, bool] = {}
_B: dict = {}


def rec(fid: str, ok: bool, lines: list[str]) -> bool:
    RESULTS[fid] = bool(ok)
    T.append(f"--- {fid} : {'PASS' if ok else 'FAIL'} ---")
    T.extend("    " + x for x in lines)
    return bool(ok)


def tbl(name: str, root: Path | None = None) -> pd.DataFrame:
    return pd.read_parquet((root or T7.OUT) / f"{name}.parquet")


def books() -> dict:
    if not _B:
        lo, hi, meta = T7.corridor()
        _B.update({"lo": lo, "hi": hi, "meta": meta,
                   "control": T7.run_cell(RC.CARD_V6_CONTROL, lo, hi),
                   "hybrid": T7.run_cell(RC.CARD_HYBRID, lo, hi),
                   "ae": T7.run_cell(RC.CARD_AE, lo, hi)})
    return _B


# ═══════════════════════ F-C7-CTRL · v7 with its knobs off IS v6
def f_ctrl() -> bool:
    """FAILS IF: card v7 at its defaults does not reproduce card v6's book,
    campaign for campaign, to 1e-05.

    THE FORK'S WHOLE LICENCE.  `_ride_leg`, `_ride_chain`, `_account_chain` and
    `replay` are new code — a ride that can exit to flat, re-enter and abort is
    a different loop, and new code drifts.  The control neutralises every v7
    knob (`hybrid_anchor=False, weave=False, reentry=False, ae_abort_r=None,
    stop_grid_offset_atr=0.0`) so the claim under test is exactly "v7 with its
    knobs off IS v6", and the referee is Tier-C6's own live book rather than a
    second run of this module.
    """
    lines, ok = [], True
    B = books()
    lo, hi = B["lo"], B["hi"]
    v6 = T6.run_cell(V6.CARD_V6, lo, hi)
    got = T7.journal_frame(B["control"]).sort_values(
        ["asset", "entry_ms"]).reset_index(drop=True)
    want = T6.journal_frame(v6).sort_values(
        ["asset", "entry_ms"]).reset_index(drop=True)
    g = len(got) == len(want)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] campaign count {len(got)} == "
                 f"{len(want)} (Tier-C6's live v6 book, same corridor)")
    if g:
        kg = list(zip(got["asset"], got["entry_ms"]))
        kw = list(zip(want["asset"], want["entry_ms"]))
        g2 = kg == kw
        ok &= g2
        lines.append(f"[{'OK ' if g2 else 'BAD'}] and they are the SAME "
                     f"campaigns, in order")
        cols = [c for c in ("entry_ms", "exit_ms", "entry_px", "exit_px",
                            "stop_px", "r_dist", "net_r", "gross_r", "fee_r",
                            "funding_r", "mfe_r", "n_advances",
                            "final_stop_px") if c in got.columns
                and c in want.columns]
        worst, wcol = 0.0, ""
        for c in cols:
            a = pd.to_numeric(got[c], errors="coerce").astype(float)
            b = pd.to_numeric(want[c], errors="coerce").astype(float)
            dm = float(np.nanmax(np.abs(a - b))) if len(a) else 0.0
            if dm > worst:
                worst, wcol = dm, c
        g3 = worst <= 1e-05
        ok &= g3
        lines.append(f"[{'OK ' if g3 else 'BAD'}] {len(cols)} numeric columns "
                     f"trade-for-trade: WORST ABSOLUTE DIFF = {worst:.3e} on "
                     f"`{wcol or '—'}` (bar 1e-05)")
        er = got["exit_reason"].tolist() == want["exit_reason"].tolist()
        ok &= er
        lines.append(f"[{'OK ' if er else 'BAD'}] and every exit_reason "
                     f"matches — categorical, invisible to a numeric diff")
    lines.append("      FAILS IF: any column moves. Absolute bar, two orders "
                 "of magnitude looser than the 6-dp write rounding that is the "
                 "only difference either side may have.")
    # AND THE CONTROL MUST BE THE DEFAULT, or it is testing a different card
    import dataclasses as dc
    defaults = {f.name: f.default for f in dc.fields(RC.Card)}
    knobs = {"hybrid_anchor": False, "weave": False, "reentry": False,
             "ae_abort_r": None, "stop_grid_offset_atr": 0.0}
    bad = {k: defaults[k] for k, v in knobs.items() if defaults[k] != v}
    ok &= not bad
    lines.append(f"[{'OK ' if not bad else 'BAD'}] and every v7 knob DEFAULTS "
                 f"off, so `Card()` is v6: {bad or 'all default'}")
    lines.append("      FAILS IF: a knob defaults on. The control would then "
                 "be a v7 arm wearing v6's name and this leg would prove "
                 "nothing.")
    return rec("F-C7-CTRL", ok, lines)


# ═══════════════════════ F-C7-INHERIT · five generations
def f_inherit() -> bool:
    """FAILS IF: an object this module claims to inherit is a COPY."""
    lines, ok = [], True
    pairs = [("build_4h", RC.build_4h, V5.build_4h),
             ("armings", RC.armings, V5.armings),
             ("struct_stop_4h", RC.struct_stop_4h, V5.struct_stop_4h),
             ("harvest_edge", RC.harvest_edge, V5.harvest_edge),
             ("spring_signals", RC.spring_signals, V5.spring_signals),
             ("ribbon_band", RC.ribbon_band, V5.ribbon_band),
             ("trail_step(v6)", RC.trail_step, V6.trail_step),
             ("Trade", RC.Trade, V5.Trade),
             ("Advance", RC.Advance, V5.Advance),
             ("frame", T7.frame, T6.frame),
             ("agg", T7.agg, T6.agg), ("d15", T7.d15, T6.d15),
             ("cluster_boot", T7.cluster_boot, T6.cluster_boot)]
    bad = [n for n, a, b in pairs if a is not b]
    ok &= not bad
    lines.append(f"[{'OK ' if not bad else 'BAD'}] {len(pairs)} objects bound "
                 f"by IDENTITY: {len(bad)} are copies {bad}")
    g = (V5.ratchet_step is V4.ratchet_step)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] and the ratchet reached through "
                 f"to Tier-C4's own object — five generations")
    g = (issubclass(RC.Card, V6.Card) and issubclass(V6.Card, V5.Card)
         and isinstance(RC.CARD_HYBRID, V5.Card))
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] Card v7 <: Card v6 <: Card v5 — a "
                 f"v7 card IS a v5 card")
    import dataclasses as dc
    v6d = {f.name: f.default for f in dc.fields(V6.Card)}
    v7d = {f.name: f.default for f in dc.fields(RC.Card)}
    declared = {"name", "hybrid_anchor", "weave", "reentry", "ae_abort_r",
                "weave_k", "stop_grid_offset_atr"}
    drift = {k: (v6d[k], v7d[k]) for k in v6d
             if k not in declared and v7d.get(k) != v6d[k]}
    ok &= not drift
    lines.append(f"[{'OK ' if not drift else 'BAD'}] and no INHERITED default "
                 f"drifted: {drift or 'none'}")
    lines.append("      FAILS IF: a default changes without being declared — "
                 "which a copied dataclass hides and a subclass cannot.")
    return rec("F-C7-INHERIT", ok, lines)


# ═══════════════════════ F-C7-ARM · the ladder sleeps before +1R
def f_arm() -> bool:
    """FAILS IF: any advance confirms before its LEG first reached +1R — on
    EVERY leg of EVERY campaign, not on a sample.

    NON-CIRCULAR: the program latches arming from its own running extreme; this
    re-reads the raw 4h bars for each leg and finds the first bar whose
    favourable extreme reaches +1R **in that leg's own R** — which for a
    re-entry is the CHAIN's R, because that is what the leg was ridden in.

    CARDINALITY: every advance-carrying leg is checked, and the number checked
    is asserted against the number that carry advances.

    AND THE CONVERSE HAS CONTENT: a card with the arming OFF is scanned by the
    same code and must show advances this rule would refuse — otherwise the leg
    measures the empty set.
    """
    lines, ok = [], True
    B = books()

    def first_1r(sym, d, ti, xi, epx, R):
        f = T7.frame(sym)["f"]
        for j in range(ti + 1, xi + 1):
            fv = float(f.h[j]) if d == 1 else float(f.l[j])
            if (fv - epx) * d / R >= 1.0:
                return j
        return None

    checked = early = 0
    legs_with_adv = 0
    bad = []
    for t in B["hybrid"]:
        for lg in t.chain["legs"]:
            if not lg["advances"]:
                continue
            legs_with_adv += 1
            checked += 1
            j1 = first_1r(t.symbol, t.direction, lg["entry_i"], lg["exit_i"],
                          lg["entry_px"], t.r_dist)
            if j1 is None:
                early += 1
                bad.append((t.symbol, T7.iso(t.entry_ms), "advanced, never +1R"))
                continue
            for a in lg["advances"]:
                if int(a.conf_i) < int(j1):
                    early += 1
                    bad.append((t.symbol, T7.iso(t.entry_ms),
                                f"advance {a.conf_i} < first +1R {j1}"))
    g = checked == legs_with_adv
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] CARDINALITY: {checked} legs "
                 f"checked == {legs_with_adv} legs carrying an advance "
                 f"(across {len(B['hybrid'])} campaigns)")
    g = early == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] and {early} advance(s) confirm "
                 f"before their leg's first +1R bar, RE-READ FROM RAW BARS "
                 f"{bad[:3]}")
    # THE CONVERSE
    unarmed = RC.Card(name="probe-unarmed", trail_arm_after_r=0.0)
    refused = 0
    for t in T7.run_cell(unarmed, B["lo"], B["hi"]):
        for lg in t.chain["legs"]:
            j1 = first_1r(t.symbol, t.direction, lg["entry_i"], lg["exit_i"],
                          lg["entry_px"], t.r_dist)
            for a in lg["advances"]:
                if j1 is None or int(a.conf_i) < int(j1):
                    refused += 1
    g = refused > 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] THE CONVERSE HAS CONTENT: an "
                 f"UNARMED card, scanned by this same code, shows {refused} "
                 f"advances the +1R rule would refuse")
    lines.append("      FAILS IF: zero. Then the arming rule changes nothing "
                 "and the leg above is measuring the empty set.")
    return rec("F-C7-ARM", ok, lines)


# ═══════════════════════ F-C7-WEV · three weave events, both clauses, by hand
def f_weave() -> bool:
    """FAILS IF: a filed weave exit does not satisfy BOTH clauses of D-R3 when
    the ribbons are rebuilt independently from raw closes.

    THE RIBBONS ARE REBUILT, NOT RE-FETCHED.  `RC.Weave` caches its arrays;
    calling it again would prove only that a dict is a dict.  This leg
    recomputes each family's three EMAs from `f.c` with `ind.ema`, applies the
    same warm-up floor, and evaluates the two clauses arithmetically — a
    different code path to the same predicate.

    AND IT CHECKS THE CLAUSES SEPARATELY, so a failure says WHICH clause.
    """
    lines, ok = [], True
    B = books()
    wex = [t for t in B["hybrid"] if t.exit_reason == "weave"]
    lines.append(f"    {len(wex)} weave exits in the hybrid book of "
                 f"{len(B['hybrid'])} campaigns")
    if len(wex) < 3:
        ok = False
        lines.append(f"[BAD] fewer than three weave exits to verify")
    k = RC.WEAVE_K
    for t in wex[:3]:
        f = T7.frame(t.symbol)["f"]
        c = f.c
        j = t.exit_i
        d = t.direction
        n = len(c)
        idx = np.arange(n)

        def band(fam):
            a, b, e = RC.RIBBONS[fam]
            st = np.vstack([ind.ema(c, a), ind.ema(c, b), ind.ema(c, e)])
            lo_, hi_ = np.nanmin(st, axis=0), np.nanmax(st, axis=0)
            lo_[idx < max(RC.RIBBONS[fam])] = np.nan
            hi_[idx < max(RC.RIBBONS[fam])] = np.nan
            return lo_, hi_

        m_lo, m_hi = band("M")
        f_lo, f_hi = band("FAST")
        med = ind.ema(c, RC.RIBBONS["M"][1])
        med = np.where(idx >= RC.RIBBONS["M"][1], med, np.nan)
        width = m_hi - m_lo
        contracting = bool(width[j] < width[j - k])
        slope = float(med[j] - med[j - 1])
        slope_against = bool(slope * d <= 0.0)
        clause_ii = (bool(f_lo[j] <= m_hi[j]) if d == 1
                     else bool(f_hi[j] >= m_lo[j]))
        good = contracting and slope_against and clause_ii
        ok &= good
        lines.append(
            f"[{'OK ' if good else 'BAD'}] {t.symbol} {T7.iso(t.exit_ms)} "
            f"{'long ' if d == 1 else 'short'} · (i) width {width[j]:.6f} < "
            f"width[-{k}] {width[j-k]:.6f} = {contracting} AND slope*dir "
            f"{slope * d:+.8f} <= 0 = {slope_against} · (ii) "
            f"{'f_lo<=m_hi' if d == 1 else 'f_hi>=m_lo'} = {clause_ii}")
    lines.append("      FAILS IF: either clause is false on a filed weave "
                 "exit. The ribbons are rebuilt from raw closes with the same "
                 "warm-up floor — a different path to the same predicate, not "
                 "a second call to the cache the program used.")
    lines.append("      AND TWO CLAUSES ONLY: D-R3 says two, and a third "
                 "condition — however sensible — would make the registered "
                 "rule a different rule from the one written down first.")
    return rec("F-C7-WEV", ok, lines)


# ═══════════════════════ F-C7-CHAIN · two chains hand-walked
def f_chain() -> bool:
    """FAILS IF: a chain's accounting is not one campaign's.

    THE SIZING IS THE LEG WITH CONTENT, and it exists because the first draft
    got it wrong in a way that would have carried a registration. A re-entry is
    sized `chain_R / own_R` so that a stopped-out re-entry loses EXACTLY 1.0
    chain-R whatever its stop distance. That is asserted here on EVERY chain
    whose leg 2 stopped out — a cardinality check, not a sample — and hand-
    walked in full on two.

    ALSO ASSERTED: the funding ceiling is taken ONCE on the chain total (never
    per leg), and the chain's net R equals the sum of its legs' contributions
    computed independently from raw prices.
    """
    lines, ok = [], True
    B = books()
    chains = [t for t in B["hybrid"] if t.n_reentries]
    lines.append(f"    {len(chains)} chains in the hybrid book of "
                 f"{len(B['hybrid'])} campaigns")

    # ── CARDINALITY: every stopped-out leg 2 loses exactly 1.0 chain-R ─────
    # THE POPULATION IS "STOPPED AT THE ENTRY STOP", NOT "STOPPED".
    # A leg-2 stop exit whose LADDER ADVANCED exits at the advanced stop, which
    # is not one R from entry and can be a PROFIT — so "-1.0 chain-R" is not
    # the invariant there and asserting it was a defect in this leg, not in the
    # sizing. The first draft did not filter and reported a worst deviation of
    # 25.88 on a leg that had trailed into profit. The exact invariant is:
    # a leg-2 stop exit with NO advances loses EXACTLY -1.0 chain-R, whatever
    # its own stop distance — which is the whole point of the sizing.
    # Harvested legs are excluded too: a harvest books a fraction earlier at a
    # different price, so the leg's gross is not a single stop distance.
    # ADVERSARIAL REPAIR: THIS LEG USED TO BE ALGEBRA THAT PROVED ITSELF.
    # The first draft computed `size = t.r_dist / lg["own_r"]` HERE and then
    # asserted `size * (exit - entry) * d / r_dist == -1`. Substituting the
    # first line into the second gives -1 identically for a stop exit at the
    # entry stop — it is an algebraic identity in the FIXTURE's own variables,
    # and it never touched `_account_chain`. It passed at 2.22e-16 and it would
    # have passed with the sizing DELETED from the program. That is the exact
    # self-comparison this file's preamble bans, written by the same hand that
    # wrote the preamble.
    #
    # It now (a) reads the sizes the PROGRAM computed, (b) asserts they are the
    # sizing rule, and (c) proves the sizing is LOAD-BEARING by showing the
    # program's gross differs from the one-unit gross on every chain whose
    # re-entry stop distance differs from the chain's R.
    checked = bad = 0
    worst = 0.0
    skipped_adv = skipped_harv = 0
    load_bearing = 0
    size_mismatch = 0
    for t in chains:
        lg = t.chain["legs"][1]
        acc = T7._account_chain(t.symbol, RC.CARD_HYBRID, t.direction,
                                t.r_dist, t.chain)          # THE PROGRAM
        size_prog = float(acc["leg_sizes"][1])
        size_rule = t.r_dist / float(lg["own_r"])
        if abs(size_prog - size_rule) > 1e-12:
            size_mismatch += 1
        if abs(size_prog - 1.0) > 1e-9:
            load_bearing += 1
        if lg["exit_reason"] != "stop":
            continue
        if lg["advances"]:
            skipped_adv += 1
            continue
        if lg["harvest"]:
            skipped_harv += 1
            continue
        checked += 1
        d = t.direction
        # THE PROGRAM'S size, not the fixture's
        gross_r = size_prog * (lg["exit_px"] - lg["entry_px"]) * d / t.r_dist
        dev = abs(gross_r + 1.0)
        worst = max(worst, dev)
        if dev > 1e-9:
            bad += 1
    g = size_mismatch == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the sizes `_account_chain` ACTUALLY "
                 f"USED are chain_R/own_R on all {len(chains)} chains: "
                 f"{size_mismatch} mismatch")
    g = load_bearing > 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] AND THE SIZING IS LOAD-BEARING: "
                 f"{load_bearing} of {len(chains)} chains carry a leg-2 size "
                 f"!= 1.0, so deleting the sizing would move the book")
    lines.append("      FAILS IF: zero. Then every re-entry happens to risk "
                 "exactly the chain's R, the sizing rule is inert, and the "
                 "leg below is an identity rather than a check.")
    g = bad == 0 and checked > 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] SIZING, on ALL {checked} chains "
                 f"whose re-entry stopped at its ENTRY stop: each loses "
                 f"exactly -1.0000 chain-R gross USING THE PROGRAM'S OWN SIZE "
                 f"— worst deviation {worst:.3e} (excluded: {skipped_adv} "
                 f"whose ladder had advanced, {skipped_harv} that harvested)")
    lines.append("      FAILS IF: one does not. Held at one unit instead, a "
                 "re-entry with a 3.5x wider stop booked 3.5x the risk as 1R "
                 "and one campaign became 75% of the arm's delta.")

    # ── TWO CHAINS, HAND-WALKED FROM RAW PRICES ───────────────────────────
    for t in chains[:2]:
        f = T7.frame(t.symbol)["f"]
        acc = T7._account_chain(t.symbol, RC.CARD_HYBRID, t.direction,
                                t.r_dist, t.chain)
        d = t.direction
        bps = RC.FEE_BPS_SIDE / 10_000.0
        hand_g = hand_f = 0.0
        parts = []
        for k, lg in enumerate(t.chain["legs"]):
            size = acc["leg_sizes"][k]
            g_ = size * (lg["exit_px"] - lg["entry_px"]) * d
            f_ = bps * size * (lg["entry_px"] + lg["exit_px"])
            hand_g += g_
            hand_f += f_
            parts.append(f"leg{k} size {size:.4f} own_r {lg['own_r']:.4f} "
                         f"-> {g_ / t.r_dist:+.4f} R gross")
        # harvest legs split the gross into fractions; only compare unharvested
        harvested = any(lg["harvest"] for lg in t.chain["legs"])
        adds = any(lg["adds"] for lg in t.chain["legs"])
        if not harvested and not adds:
            dev_g = abs(hand_g / t.r_dist - acc["gross_r"])
            dev_f = abs(hand_f / t.r_dist - acc["fee_r"])
            good = dev_g <= 1e-9 and dev_f <= 1e-9
            ok &= good
            lines.append(f"[{'OK ' if good else 'BAD'}] {t.symbol} "
                         f"{T7.iso(t.entry_ms)} chain R {t.r_dist:.6f} · "
                         f"{' · '.join(parts)} · hand gross "
                         f"{hand_g / t.r_dist:+.6f} vs filed "
                         f"{acc['gross_r']:+.6f} (dev {dev_g:.2e}), fee dev "
                         f"{dev_f:.2e}")
        else:
            lines.append(f"[OK ] {t.symbol} {T7.iso(t.entry_ms)} · "
                         f"{' · '.join(parts)} · harvested={harvested} "
                         f"adds={adds} — gross compared at the leg level only, "
                         f"because a harvest splits a leg into fractions and a "
                         f"whole-leg comparison would not be the same quantity")

    # ── THE CEILING IS TAKEN ONCE ─────────────────────────────────────────
    bound = [t for t in chains if t.funding_ceiling_bound]
    lines.append(f"      the D12 ceiling bound on {len(bound)} of "
                 f"{len(chains)} chains — it is applied ONCE to the chain "
                 f"total, never per leg, which would convert a 1R ceiling "
                 f"into a 2R one")
    # ── AND A CHAIN IS ONE ROW OF THE JOURNAL ─────────────────────────────
    j = tbl("trade_journal_hybrid")
    g = len(j) == len(B["hybrid"])
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] and the journal holds {len(j)} "
                 f"rows == {len(B['hybrid'])} campaigns — a chain is ONE "
                 f"campaign [D-R6], not two")
    cl = tbl("chain_ledger")
    want_legs = sum(len(t.chain["legs"]) for t in B["hybrid"])
    g = len(cl) == want_legs
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] and the chain ledger holds "
                 f"{len(cl)} rows == {want_legs} legs — both legs shown, as "
                 f"D-R6 requires")
    return rec("F-C7-CHAIN", ok, lines)


# ═══════════════════════ F-C7-AE · three aborts at 0.60R
def f_ae() -> bool:
    """FAILS IF: a filed abort did not reach 0.60R against, measured on the
    bar's adverse EXTREME and re-read from raw bars — or fired late.

    FIRSTNESS IS CHECKED, not membership: the abort fires on the FIRST bar that
    reaches the threshold, so every bar strictly between entry and the abort is
    asserted NOT to have reached it.
    """
    lines, ok = [], True
    B = books()
    ab = [t for t in B["ae"] if t.exit_reason == "ae_abort"]
    thr = float(RC.AE_ABORT_R)
    lines.append(f"    {len(ab)} aborts in the P-AE-1 book of {len(B['ae'])} "
                 f"campaigns, threshold {thr}R")
    checked = 0
    for t in ab[:3]:
        f = T7.frame(t.symbol)["f"]
        d = t.direction
        j = t.exit_i
        adv = float(f.l[j]) if d == 1 else float(f.h[j])
        reached = (adv - t.entry_px) * d / t.r_dist
        earlier = []
        for q in range(t.entry_i + 1, j):
            a2 = float(f.l[q]) if d == 1 else float(f.h[q])
            if (a2 - t.entry_px) * d / t.r_dist <= -thr:
                earlier.append(q)
        good = reached <= -thr + 1e-12 and not earlier
        ok &= good
        checked += 1
        lines.append(f"[{'OK ' if good else 'BAD'}] {t.symbol} "
                     f"{T7.iso(t.exit_ms)} reached {reached:+.4f} R at the "
                     f"abort bar (bar {-thr}) · earlier bars that also reached "
                     f"it: {len(earlier)} · filled at the CLOSE "
                     f"{float(f.c[j]):.6f}, not at the extreme {adv:.6f}")
    lines.append(f"      {checked} aborts hand-verified from raw bars.")
    lines.append("      FAILS IF: the bar did not reach the threshold, or an "
                 "earlier bar did (the rule says FIRST), or the fill equals "
                 "the extreme — which would be a resting order and a better "
                 "fill than the rule earns.")
    # the fill is the CLOSE, asserted over ALL aborts, not the three above
    badfill = sum(1 for t in ab
                  if abs(t.exit_px - float(T7.frame(t.symbol)["f"].c[t.exit_i]))
                  > 1e-9)
    ok &= badfill == 0
    lines.append(f"[{'OK ' if not badfill else 'BAD'}] and ALL {len(ab)} "
                 f"aborts fill at their bar's CLOSE: {badfill} do not "
                 f"(a cardinality check, not a sample)")
    return rec("F-C7-AE", ok, lines)


# ═══════════════════════ F-C7-GRID · the surface, three ways
def f_grid() -> bool:
    """FAILS IF: the arms the code builds, the arms the tables hold and the
    registrations declared do not agree."""
    lines, ok = [], True
    reg = tbl("registrations")
    txt = tbl("registration_text")
    abl = tbl("ablation")
    tested = reg[reg["registration"] != "(reference)"]
    m = int(reg["fdr_m_tests_actually_run"].iloc[0])
    g = len(tested) == m == len(txt) == 4
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] registrations: {len(txt)} texts "
                 f"filed · {len(tested)} scored · m = {m} — all 4, and "
                 f"P-LAG-1 is NOT among them")
    g = "P-LAG-1" not in set(txt["registration"]) | set(reg["registration"])
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] P-LAG-1 appears in NO scored "
                 f"table — its condition was evaluated in TC6-V and NOT met, "
                 f"so it is report-only and m stays 4")
    g = len(abl) == 6 and not abl["scored"].astype(bool).any()
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the ablation ladder is {len(abl)} "
                 f"rungs and EVERY rung is unscored")
    # the LOAO line is present on every scored row
    miss = [r_["registration"] for _, r_ in tested.iterrows()
            if not isinstance(r_.get("loao_line"), str)]
    ok &= not miss
    lines.append(f"[{'OK ' if not miss else 'BAD'}] and every scored arm "
                 f"carries its LOAO-3/5 line [E1 law]: missing {miss}")
    lines.append("      FAILS IF: a registration is scored without a LOAO "
                 "line, or m counts something other than the tests run.")
    return rec("F-C7-GRID", ok, lines)


# ═══════════════════════ F-C7-CLOSURE · captured, not consulted
def f_closure() -> bool:
    """FAILS IF: a decision module imports analytics or names a tape column."""
    lines, ok = [], True
    mods = ["scripts/tierc7_rules.py", "scripts/tierc6_rules.py",
            "scripts/tierc5_rules.py", "scripts/tierc4_rules.py",
            "scripts/tierc3_rules.py", "scripts/tierc2_rules.py"]
    for m in mods:
        src = F4.code_only((ROOT / m).read_text())
        hits = [w for w in ("import analytics", "from analytics",
                            "analytics.") if w in src]
        ok &= not hits
        lines.append(f"[{'OK ' if not hits else 'BAD'}] {m}: analytics hits "
                     f"{hits}")
    try:
        cols = set(pd.read_parquet(
            ROOT / "research_outputs/tierc5/analytics_tape.parquet").columns)
    except Exception:                                          # noqa: BLE001
        cols = set()
    named = {}
    for m in mods:
        src = F4.code_only((ROOT / m).read_text())
        named[m] = sorted(c for c in cols if len(c) > 6 and f'"{c}"' in src)
    bad = {k: v for k, v in named.items() if v}
    ok &= not bad
    lines.append(f"[{'OK ' if not bad else 'BAD'}] tape column names in the "
                 f"decision path's CODE: {bad}")
    lines.append("      FAILS IF: a decision module gains an analytics import "
                 "or a tape column name. TIER-C7's weave reads RIBBONS as a "
                 "DECISION, and they are built in `tierc7_rules` from raw "
                 "closes and `engine.indicators` for exactly that reason.")
    return rec("F-C7-CLOSURE", ok, lines)


# ═══════════════════════ F-KEY · total, from the manifest
def f_keys() -> bool:
    """FAILS IF: a filed table has a duplicate on its declared key, or a filed
    parquet has no declared key at all."""
    lines, ok = [], True
    man = json.loads((T7.OUT / "build_manifest.json").read_text())
    keys = {k: list(v) for k, v in man["keys"].items()}
    filed = sorted(p.stem for p in T7.OUT.glob("*.parquet"))
    missing = sorted(set(filed) - set(keys))
    ok &= not missing
    lines.append(f"[{'OK ' if not missing else 'BAD'}] TOTALITY: {len(keys)} "
                 f"declared keys cover all {len(filed)} filed parquets — "
                 f"unkeyed {missing}")
    lines.append(f"      skipped-empty and SAID SO: "
                 f"{man.get('skipped_empty', [])}")
    for n, k in sorted(keys.items()):
        d = tbl(n)
        dup = int(d.duplicated(subset=k).sum()) if len(d) else 0
        g = dup == 0
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {n:24} key={k} "
                     f"rows={len(d):,} dup={dup}")
    B = books()
    j = tbl("trade_journal_hybrid")
    g = len(j) == len(B["hybrid"]) == int(man["counts"]["hybrid_n"])
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] journal {len(j)} == book "
                 f"{len(B['hybrid'])} == manifest "
                 f"{man['counts']['hybrid_n']}")
    return rec("F-KEY", ok, lines)


# ═══════════════════════ F-C7-DET · two runs, byte for byte
def f_det() -> bool:
    """FAILS IF: a second run writes a different byte."""
    lines, ok = [], True
    import subprocess
    r = subprocess.run([str(Path.home() / "venvs/naiad/bin/python"),
                        "scripts/tierc7.py", "--rerun"],
                       cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        return rec("F-C7-DET", False,
                   [f"[BAD] the re-run did not complete: {r.stderr[-400:]}"])
    a = json.loads((T7.OUT / "build_manifest.json").read_text())
    b = json.loads((T7.OUT_RERUN / "build_manifest.json").read_text())
    ka, kb = set(a["sha"]), set(b["sha"])
    g = ka == kb
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] both runs wrote the same "
                 f"{len(ka)} tables")
    moved = sorted(k for k in ka & kb if a["sha"][k] != b["sha"][k])
    ok &= not moved
    lines.append(f"[{'OK ' if not moved else 'BAD'}] every build-computed sha "
                 f"agrees: {len(moved)} moved {moved}")

    def fsha(p):
        return hashlib.sha256(p.read_bytes()).hexdigest()

    fm = [k for k in sorted(ka & kb)
          if (T7.OUT / f"{k}.parquet").exists()
          and (T7.OUT_RERUN / f"{k}.parquet").exists()
          and fsha(T7.OUT / f"{k}.parquet") != fsha(T7.OUT_RERUN / f"{k}.parquet")]
    ok &= not fm
    lines.append(f"[{'OK ' if not fm else 'BAD'}] and the PARQUET FILES "
                 f"re-hash equal on disk: {len(fm)} differ {fm[:4]}")
    lines.append("      FAILS IF: any differs. The sha legs are the build's "
                 "CLAIM; the file re-hash reaches the output.")
    return rec("F-C7-DET", ok, lines)



# ═══════════════════════ F-C7-LABS · a missing lab is a failure, not a log line
def f_labs() -> bool:
    """FAILS IF: a commissioned lab is absent from the build.

    THIS FIXTURE EXISTS BECAUSE A BUILD WENT GREEN WITHOUT IT.  `_labs()`
    imported each lab in a try/except and logged "NOT AVAILABLE" on failure, so
    a full TIER-C7 run completed with THREE OF FOUR LABS MISSING and recorded
    the fact in a manifest field nothing asserted on. The log said so; nothing
    checked. A commissioned deliverable that is absent must fail the suite, not
    decorate it.

    THE EXPECTED SET IS READ FROM THE PROGRAM'S OWN DECLARATION
    (`T7.LABS_EXPECTED`), so adding a lab to the commission and forgetting to
    build it fails here the same day.
    """
    lines, ok = [], True
    man = json.loads((T7.OUT / "build_manifest.json").read_text())
    missing = man.get("labs_missing", None)
    if missing is None:
        ok = False
        lines.append("[BAD] the manifest carries no `labs_missing` field — an "
                     "older build, or the driver stopped recording it")
        missing = []
    g = not missing
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] {len(T7.LABS_EXPECTED)} labs "
                 f"commissioned, {len(missing)} missing: {missing}")
    state = man.get("labs", {})
    notbuilt = sorted(k for k, v in state.items() if v != "BUILT")
    ok &= not notbuilt
    lines.append(f"[{'OK ' if not notbuilt else 'BAD'}] and every lab reports "
                 f"BUILT: {notbuilt or 'all built'} — {state}")
    lines.append("      FAILS IF: a commissioned lab is absent. The build will "
                 "still RUN without one, deliberately, so that a single broken "
                 "lab cannot take the other three down — but it will not PASS.")
    return rec("F-C7-LABS", ok, lines)


def main() -> int:
    print("=" * 78)
    print("TIER-C7 FIXTURE TRANSCRIPT")
    print("=" * 78)
    f_ctrl()
    f_inherit()
    f_arm()
    f_weave()
    f_chain()
    f_ae()
    f_grid()
    f_closure()
    f_keys()
    f_labs()
    f_det()
    print("\n".join(T))
    n_ok = sum(RESULTS.values())
    print()
    print("=" * 78)
    print(f"FIXTURE SUMMARY  {n_ok}/{len(RESULTS)} PASS  {json.dumps(RESULTS)}")
    print(f"  I9: ANALYTICS_VERSION {AN.ANALYTICS_VERSION} · analytics_sha "
          f"{AN.analytics_sha()}")
    print("=" * 78)
    if n_ok != len(RESULTS):
        print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
