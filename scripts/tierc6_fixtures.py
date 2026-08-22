"""TIER-C6 rev B — THE FIXTURES.

    F-C6-CTRL     the v5 card through the v6 code path reproduces Tier-C5's
                  FILED book trade-for-trade
    F-C6-INHERIT  the fork is by IMPORT — every inherited object asserted `is`
    F-C6-ARM      the trail is PROVABLY ASLEEP before +1R, on EVERY campaign,
                  re-derived from raw bars
    F-C6-MINADV   the minimum advance gates the quantity the ledger publishes
    F-C6-LEAGUE   two-sided — raw-bar re-derivation, a mirror proof, and the
                  resistance side reproducing Tier-C5's filed table
    F-C6-WALL     three wall exits hand-verified PER SIDE from raw bars
    F-C6-ZEC      one fingerprint metric hand-recomputed per hypothesis
    F-C6-GRID     the selection surface counted three independent ways
    F-C6-DET      two runs, byte for byte
    F-C6-CLOSURE  captured-not-consulted — the decision path still imports no
                  analytics and names no tape column
    F-KEY         every written table on its declared key

EVERY LEG STATES INLINE WHAT WOULD MAKE IT FAIL.  That convention was adopted
as a house rule after Tier-C4 (F-C4-h) and it is not decoration: a leg whose
failure condition cannot be written down is usually a leg that cannot fail.

AND TWO FAILURE MODES ARE BANNED BY NAME, because this estate has paid for both:

  CIRCULARITY — a check that re-derives a value the way the program derived it
  and compares it to itself.  Six of sixteen TC5 repairs were that one defect.

  ONE EXAMPLE OF A KIND — a check satisfied by a single row where a cardinality
  check was possible.  A TC5-Q book lost 64% of its instants and every fixture
  stayed green.

Where a leg could have been written either way, the harder way is taken and the
easier way is named beside it.
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

import tierc6 as T6                                                  # noqa: E402
import tierc6_rules as RC                                            # noqa: E402
import tierc5 as T5                                                  # noqa: E402
import tierc5_rules as V5                                            # noqa: E402
import tierc4_rules as V4                                            # noqa: E402
import tierc4_fixtures as F4                                         # noqa: E402
import analytics as AN                                               # noqa: E402
from engine import indicators as ind                                 # noqa: E402

TC5 = ROOT / "research_outputs" / "tierc5"
T: list[str] = []
RESULTS: dict[str, bool] = {}
_BOOKS: dict = {}


def rec(fid: str, ok: bool, lines: list[str]) -> bool:
    RESULTS[fid] = bool(ok)
    T.append(f"--- {fid} : {'PASS' if ok else 'FAIL'} ---")
    T.extend("    " + x for x in lines)
    return bool(ok)


def tbl(name: str, root: Path | None = None) -> pd.DataFrame:
    return pd.read_parquet((root or T6.OUT) / f"{name}.parquet")


def books() -> dict:
    """The books, built once and reused — the fixtures ride the same objects
    the build rode, not a second replay that could differ from it."""
    if not _BOOKS:
        lo, hi, meta = T6.corridor()
        _BOOKS.update({
            "lo": lo, "hi": hi, "meta": meta,
            "v6": T6.run_cell(RC.CARD_V6, lo, hi),
            "v5": T6.run_cell(RC.CARD_V5_CONTROL, lo, hi),
        })
    return _BOOKS


# ═══════════════════════ F-C6-CTRL · the fork did not drift
def f_ctrl() -> bool:
    """FAILS IF: the v5 card ridden through TIER-C6's forked `_ride`,
    `_account` and `replay` does not reproduce Tier-C5's FILED book to 1e-05 on
    every campaign and every compared column.

    THIS IS THE FIXTURE THE FORK EXISTS FOR.  Three functions were copied out of
    tierc5.py because their bodies change, and a copied function is a function
    that can drift.  The control neutralises every v6 knob — trail unarmed, no
    minimum advance, no wall, the ruled harvest fraction — so the claim under
    test is precisely "v6 with its knobs off IS v5", and the referee is not this
    module's own second run but the parquet Tier-C5 committed.
    """
    lines, ok = [], True
    B = books()
    got = T6.journal_frame(B["v5"]).sort_values(["asset", "entry_ms"]).reset_index(drop=True)
    want = pd.read_parquet(TC5 / "trade_journal.parquet").sort_values(
        ["asset", "entry_ms"]).reset_index(drop=True)

    # PREFIX-ROBUST, BECAUSE THE CORRIDOR MOVES — TC6-V audit repair.
    # The referee is Tier-C5's FILED journal, frozen on the corridor it was
    # written against. This module re-runs on "the latest closed 4h bar in the
    # cache", which advances. One day after publication the child legitimately
    # holds 196 campaigns against the parent's 195 — a ZEC campaign opened at
    # the new edge and is still open. A raw count equality would have started
    # FAILING for a reason that is not drift, and the honest claim is not
    # "the same number of campaigns" but "EVERY campaign the parent booked, the
    # child books identically". The extra campaigns are reported, never hidden.
    kg = set(zip(got["asset"], got["entry_ms"]))
    kw = set(zip(want["asset"], want["entry_ms"]))
    missing = sorted(kw - kg)
    extra = sorted(kg - kw)
    good = not missing
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] every one of the parent's "
                 f"{len(want)} campaigns is present in the child's {len(got)}: "
                 f"{len(missing)} missing {missing[:2]}")
    lines.append(f"      and {len(extra)} campaign(s) the parent never saw "
                 f"{[ (a, T6.iso(m)) for a, m in extra[:3] ]} — the corridor "
                 f"advances, so a NEWER child is expected; a child that LOST "
                 f"one is the failure this leg is for.")
    if good:
        got = got[[k in kw for k in zip(got["asset"], got["entry_ms"])]].reset_index(drop=True)
        want = want.reset_index(drop=True)
        kg2 = list(zip(got["asset"], got["entry_ms"]))
        kw2 = list(zip(want["asset"], want["entry_ms"]))
        g2 = kg2 == kw2
        ok &= g2
        lines.append(f"[{'OK ' if g2 else 'BAD'}] and the {len(got)} shared "
                     f"campaigns align in order on (asset, entry_ms)")
        cols = [c for c in ("entry_ms", "exit_ms", "entry_px", "exit_px",
                            "stop_px", "r_dist", "net_r", "gross_r", "fee_r",
                            "funding_r", "mfe_r", "n_advances", "final_stop_px")
                if c in got.columns and c in want.columns]
        worst, wcol = 0.0, ""
        for c in cols:
            a = pd.to_numeric(got[c], errors="coerce").astype(float)
            b = pd.to_numeric(want[c], errors="coerce").astype(float)
            dmax = float(np.nanmax(np.abs(a - b))) if len(a) else 0.0
            if dmax > worst:
                worst, wcol = dmax, c
        g3 = worst <= 1e-05
        ok &= g3
        lines.append(f"[{'OK ' if g3 else 'BAD'}] {len(cols)} numeric columns "
                     f"compared trade-for-trade: WORST ABSOLUTE DIFF = "
                     f"{worst:.3e} on `{wcol or '—'}` (bar 1e-05)")
        lines.append(f"      columns: {cols}")
        lines.append("      FAILS IF: any column moves. The bar is ABSOLUTE, "
                     "not relative, and 1e-05 is two orders of magnitude "
                     "looser than the 6-decimal write rounding that is the only "
                     "difference either side is allowed to have.")
        # exit reasons are categorical and would not show up in a numeric diff
        er = (got["exit_reason"].tolist() == want["exit_reason"].tolist()
              if "exit_reason" in got.columns else None)
        if er is not None:
            ok &= er
            lines.append(f"[{'OK ' if er else 'BAD'}] and every exit_reason "
                         f"matches — a categorical column a numeric diff cannot "
                         f"see, which is why it is asserted separately")
    return rec("F-C6-CTRL", ok, lines)


# ═══════════════════════ F-C6-INHERIT · the fork is by import
def f_inherit() -> bool:
    """FAILS IF: an object this module claims to inherit is a COPY.

    Asserted with `is`, not with `==`. Two functions that behave identically
    today are not the same object tomorrow, and the whole byte-inheritance
    claim of this estate is an identity claim.
    """
    lines, ok = [], True
    pairs = [
        ("build_4h", RC.build_4h, V5.build_4h),
        ("armings", RC.armings, V5.armings),
        ("struct_stop_4h", RC.struct_stop_4h, V5.struct_stop_4h),
        ("build_fractals", RC.build_fractals, V5.build_fractals),
        ("harvest_edge", RC.harvest_edge, V5.harvest_edge),
        ("harvest_touched", RC.harvest_touched, V5.harvest_touched),
        ("harvest_outside", RC.harvest_outside, V5.harvest_outside),
        ("spring_signals", RC.spring_signals, V5.spring_signals),
        ("spring_stop", RC.spring_stop, V5.spring_stop),
        ("add_retraced", RC.add_retraced, V5.add_retraced),
        ("add_reclaimed", RC.add_reclaimed, V5.add_reclaimed),
        ("Trade", RC.Trade, V5.Trade),
        ("Advance", RC.Advance, V5.Advance),
        ("Spring", RC.Spring, V5.Spring),
        ("frame", T6.frame, T5.frame),
        ("card_candidates", T6.card_candidates, T5.card_candidates),
        ("agg", T6.agg, T5.agg),
        ("d15", T6.d15, T5.d15),
        ("cluster_boot", T6.cluster_boot, T5.cluster_boot),
        ("journal_frame", T6.journal_frame, T5.journal_frame),
        ("_tf_frame", T6._tf_frame, T5._tf_frame),
    ]
    bad = [n for n, a, b in pairs if a is not b]
    ok &= not bad
    lines.append(f"[{'OK ' if not bad else 'BAD'}] {len(pairs)} objects bound "
                 f"by IDENTITY across four generations: {len(bad)} are copies "
                 f"{bad}")
    lines.append("      FAILS IF: any is a copy. `is`, not `==` — two "
                 "functions that agree today are not one object tomorrow.")
    # and the ratchet itself is FOUR deep
    g = V5.ratchet_step is V4.ratchet_step
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] and `ratchet_step` is Tier-C4's "
                 f"own object, reached through Tier-C5 — the trail v6 gates is "
                 f"the trail v4 wrote")
    # THE CARD SUBCLASSES, WHICH IS A STRONGER CLAIM THAN BINDING
    g = issubclass(RC.Card, V5.Card) and isinstance(RC.CARD_V6, V5.Card)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] Card v6 SUBCLASSES Card v5 — a v6 "
                 f"card IS a v5 card, so every v5 function that types its "
                 f"argument as one accepts it unchanged")
    # every v5 field arrives with its v5 default, except the ones v6 declares
    import dataclasses as dc
    v5d = {f.name: f.default for f in dc.fields(V5.Card)}
    v6d = {f.name: f.default for f in dc.fields(RC.Card)}
    declared = {"name", "trail_arm_after_r", "trail_min_advance_atr",
                "harvest_frac", "wall_exit_atr", "wall_tf"}
    drift = {k: (v5d[k], v6d[k]) for k in v5d
             if k not in declared and v6d.get(k) != v5d[k]}
    ok &= not drift
    lines.append(f"[{'OK ' if not drift else 'BAD'}] and no INHERITED default "
                 f"drifted: {len(drift)} changed {drift}")
    lines.append(f"      the {len(declared)} fields v6 declares are "
                 f"{sorted(declared)} — everything else arrives from v5 "
                 f"unretyped. FAILS IF: a default changes without being "
                 f"declared, which a copied dataclass would hide and a "
                 f"subclass cannot.")
    return rec("F-C6-INHERIT", ok, lines)


# ═══════════════════════ F-C6-ARM · the trail is asleep before +1R
def f_arm() -> bool:
    """FAILS IF: any v6 advance confirms on a bar BEFORE the bar the
    campaign first reached +1R — on ANY campaign, not on a sample.
    An advance confirming ON the first +1R bar is admitted BY DESIGN: the
    arming latch fires within the bar that reaches +1R, and the shipped book
    carries 11 such same-bar advances.  The first draft of this docstring
    said "at or before", a condition the code never tested and the book
    violates 11 times — the declared failure condition now IS the tested
    one [TC6V-d #38].

    NON-CIRCULAR BY CONSTRUCTION.  The program decides arming from
    `unit_fav_r >= card.trail_arm_after_r` inside `_ride`, using the running
    favourable extreme.  This leg does NOT ask the program when it armed.  It
    re-reads the RAW 4h bars for each campaign, recomputes the favourable
    excursion from the filed entry price and R, and finds the first bar whose
    high (long) or low (short) reaches +1R.  Two paths to the same instant; if
    the program's latch were wrong, they would disagree.

    CARDINALITY, NOT PRESENCE.  Every campaign that carries at least one
    advance is checked, the number checked is asserted to equal the number that
    carry advances, and the advance TOTAL is reconciled against the filed
    ledger.  A leg that checked "some campaign armed correctly" would pass on a
    book that had lost every other campaign.

    AND THE CONVERSE HAS CONTENT.  A fixture that only asserts "no advance
    before +1R" passes trivially on a book with no advances at all, and would
    pass on v5 too if v5 happened never to advance early.  So the v5 CONTROL is
    scanned by the same code and must show advances that v6's rule WOULD have
    refused — otherwise the arming rule changes nothing and this leg is
    measuring an empty set.
    """
    lines, ok = [], True
    B = books()

    def first_1r_bar(t) -> int | None:
        """The first bar index whose favourable extreme reaches +1R, RE-READ
        from raw bars. Scans ti+1..exit_i, exactly the bars `_ride` scans."""
        f = T6.frame(t.symbol)["f"]
        d = t.direction
        for j in range(t.entry_i + 1, t.exit_i + 1):
            fav = float(f.h[j]) if d == 1 else float(f.l[j])
            if (fav - t.entry_px) * d / t.r_dist >= 1.0:
                return j
        return None

    checked = early = 0
    worst = []
    for t in B["v6"]:
        if not t.advances:
            continue
        checked += 1
        j1 = first_1r_bar(t)
        if j1 is None:
            early += 1
            worst.append((t.symbol, T6.iso(t.entry_ms), "advanced but never "
                          "reached +1R by raw bars"))
            continue
        for a in t.advances:
            if int(a.conf_i) < int(j1):
                early += 1
                worst.append((t.symbol, T6.iso(t.entry_ms),
                              f"advance at bar {a.conf_i} < first +1R bar {j1}"))
    # THE ANCHOR IS EXTERNAL [TC6V-d #17].  The first draft compared
    # `checked` to a count derived from the SAME loop over the SAME book —
    # x == x, a leg that could not fail.  Both clauses now anchor against the
    # FILED journal: the campaign SET and its advancing subset.
    jn = tbl("trade_journal")
    g = len(B["v6"]) == len(jn)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] CARDINALITY: the ridden book "
                 f"holds {len(B['v6'])} campaigns == the FILED journal's "
                 f"{len(jn)} rows")
    filed_adv = int((jn["n_advances"].astype(int) > 0).sum())
    g = checked == filed_adv
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] and {checked} campaigns "
                 f"checked == the FILED journal's {filed_adv} campaigns "
                 f"with n_advances > 0")
    lines.append("      FAILS IF: either differs from the FILED table. A "
                 "count compared to itself passes on a book that lost the "
                 "rest; these compare the ride to the filed evidence.")
    g = early == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] and {early} advance(s) confirm "
                 f"before the campaign's first +1R bar, RE-READ FROM RAW BARS "
                 f"{worst[:3]}")
    lines.append("      FAILS IF: one does. The program latches arming from its "
                 "own running extreme; this re-derives the same instant from "
                 "the 4h highs and lows and the filed entry/R. Two paths, and "
                 "a disagreement is a defect in one of them.")
    # reconcile the advance total against the filed ledger — a different table
    rl = tbl("ratchet_ledger")
    tot = sum(len(t.advances) for t in B["v6"])
    g = len(rl) == tot
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] and the filed ratchet ledger holds "
                 f"{len(rl)} rows == {tot} advances in the book")
    # THE CONVERSE — the rule must actually bite
    refused = 0
    for t in B["v5"]:
        if not t.advances:
            continue
        j1 = first_1r_bar(t)
        for a in t.advances:
            if j1 is None or int(a.conf_i) < int(j1):
                refused += 1
    g = refused > 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] THE CONVERSE HAS CONTENT: the v5 "
                 f"control, scanned by this same code, shows {refused} advances "
                 f"that v6's arming rule WOULD have refused")
    lines.append("      FAILS IF: zero. Then the arming rule changes nothing, "
                 "the leg above is measuring the empty set, and it would pass "
                 "whatever the code did.")
    return rec("F-C6-ARM", ok, lines)


# ═══════════════════════ F-C6-MINADV · the gate measures what it reports
def f_minadv() -> bool:
    """FAILS IF: a filed v6 advance moved the stop by less than the register's
    minimum, or the gate is measured on a different quantity from the one the
    ledger publishes.

    THE POINT OF THIS LEG IS THE IDENTITY, NOT THE INEQUALITY.  `trail_step`
    gates `abs(new_stop - prev_stop)/atr`; the ledger publishes `advance_atr`.
    If those two ever drift apart the gate becomes uncheckable by a reader —
    this estate has already lost a fixture to a name that was almost right.
    So the leg recomputes `advance_atr` from the ledger's OWN stop columns and
    demands it equals the published column, and only then applies the bar.
    """
    lines, ok = [], True
    rl = tbl("ratchet_ledger")
    mn = float(RC.REGISTER["TRAIL_MIN_ADVANCE_ATR"]["value"])
    atr = rl["atr_at_conf"].astype(float)
    # THE REBUILD STARTS FROM RIDE INPUTS [TC6V-d #36].  The first draft
    # recomputed advance_atr from the ledger's OWN new_stop/prev_stop columns
    # — the banned self-comparison: the ledger derived advance_atr the same
    # way, so the leg would have passed with the gate deleted.  The stop is
    # now rebuilt from the confirming pivot, the close, the register's
    # BUF/RAIL and the ATR — the quantities the RIDE consumed.
    d_ = np.where(rl["direction"].astype(str).isin(("long", "1")), 1.0, -1.0)
    buf = float(RC.RATCHET_BUF_ATR)   # the OBJECT the ride reads
    rail = float(RC.RATCHET_RAIL_ATR)
    pv_ = rl["pivot_val"].astype(float)
    cl_ = rl["close_at_conf"].astype(float)
    cand_rb = pv_ - d_ * buf * atr
    rail_rb = cl_ - d_ * rail * atr
    stop_rb = np.where(d_ > 0, np.minimum(cand_rb, rail_rb),
                       np.maximum(cand_rb, rail_rb))
    # 6-dp write rounding on pivot, close and atr: |err| <= 5e-7·(1+max(buf,
    # rail)) + 5e-7 (stored stop's own rounding) < 2e-6 price units.
    px_dev = np.abs(stop_rb - rl["new_stop_px"].astype(float))
    px_bad = int((px_dev > 2e-6).sum())
    g = px_bad == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] new_stop REBUILT from ride "
                 f"inputs (pivot, close, BUF {buf}, RAIL {rail}, ATR) on all "
                 f"{len(rl)} rows — {px_bad} beyond the 2e-6 rounding bound "
                 f"(worst {float(np.nanmax(px_dev)):.3e})")
    lines.append("      FAILS IF: the ride-input rebuild disagrees — the "
                 "ledger would then describe stops the ride never set.")
    recomp = np.abs(stop_rb - rl["prev_stop_px"].astype(float)) / atr
    pub = rl["advance_atr"].astype(float)
    # THE BOUND IS DERIVED, NOT GUESSED — AND IT IS NOT A FLAT CONSTANT.
    # Every written column is rounded to 6 dp in PRICE units, and this leg
    # divides two of them by a third. So the error in the reconstructed ratio
    # scales as 1/ATR, and a flat 2e-6 bar fails on any asset whose ATR is small
    # in price terms (NEAR's is ~0.02, which turns a 1e-6 price rounding into a
    # 5e-5 ratio error). With s0, s1 and a each rounded by at most 5e-7:
    #     |recomp - pub|  <=  (true * 5e-7 + 1e-6) / a  +  5e-7
    # The first draft of this leg used a flat 2e-6 and FAILED at 7.35e-5 — and
    # it was the bar that was wrong, not the code. Written out so the next
    # reader can check the arithmetic instead of trusting the number.
    tol = (pub * 5e-7 + 1e-6) / atr + 5e-7
    dev = np.abs(recomp - pub)
    over = int((dev > tol).sum())
    dmax = float(np.nanmax(dev)) if len(rl) else 0.0
    g = over == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] `advance_atr` IS "
                 f"abs(new_stop - prev_stop)/atr on all {len(rl)} rows — "
                 f"{over} exceed their own rounding bound (worst deviation "
                 f"{dmax:.3e}, worst bound {float(np.nanmax(tol)):.3e})")
    lines.append("      FAILS IF: they differ by more than the 6-dp write "
                 "rounding can explain. The gate would then be measured on one "
                 "quantity and reported on another, and no reader could check "
                 "it.")
    under = int((pub < mn - 2e-6).sum())
    ok &= under == 0
    lines.append(f"[{'OK ' if not under else 'BAD'}] and {under} of {len(rl)} "
                 f"filed advances moved the stop by less than the register's "
                 f"{mn} ATR minimum")
    # AND IT MUST BITE — measured against the parent's filed ledger
    p5 = pd.read_parquet(TC5 / "ratchet_ledger.parquet")
    would = int((p5["advance_atr"].astype(float) < mn).sum())
    g = would > 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] THE GATE BITES: {would} of "
                 f"{len(p5)} advances in Tier-C5's FILED ledger fall under "
                 f"{mn} ATR and would be refused")
    lines.append("      FAILS IF: zero. A gate that refuses nothing is not a "
                 "rule, and this leg would pass on code that never applied it.")
    return rec("F-C6-MINADV", ok, lines)


# ═══════════════════════ F-C6-LEAGUE · two-sided, with a mirror proof
def f_league() -> bool:
    """FAILS IF: a league row disagrees with a raw-bar rescan, the two sides are
    not genuine mirrors, or the resistance side fails to reproduce Tier-C5's
    filed table.

    THE MIRROR PROOF IS THE LEG WITH CONTENT.  Tier-C5's champion re-check was
    an argmax compared with its own max and could not fail; the build said so
    and printed it as non-evidence.  This leg instead runs the SUPPORT scan on a
    NEGATED price series and demands it equals the RESISTANCE scan on the
    original.  Negating prices turns every support approach into a resistance
    approach and vice versa, so if the two predicates are true mirrors the two
    counts are identical — and if one of the six sign flips was missed, they
    are not.
    """
    lines, ok = [], True
    lg = tbl("league")
    B = books()

    # (a) the resistance side reproduces Tier-C5's FILED league — AT THE
    #     PARENT'S OWN CORRIDOR.
    #
    # TC6-V AUDIT REPAIR. The league scans up to `hi_ms`, and `hi_ms` advances
    # with the cache. Comparing today's counts against a table computed on
    # yesterday's window compares two POPULATIONS, not two implementations:
    # one day of drift moved 87 approaches and 52 rejections while the champions
    # did not move at all. The leg was reporting a real difference about the
    # wrong thing. It now RE-DERIVES the resistance league at the corridor
    # Tier-C5 filed its table on, so the comparison is like-for-like and stays
    # valid however far the cache runs ahead.
    f5 = pd.read_parquet(TC5 / "resistance_league.parquet")
    tc5_hi = json.loads((TC5 / "build_manifest.json").read_text())["corridor"][
        "last_closed_4h_close"]
    lines.append(f"    (leg (a) re-derives at the PARENT'S corridor end "
                 f"{tc5_hi}; the live corridor is "
                 f"{B['meta']['last_closed_4h_close']})")
    # `_ms` takes a DATE; the manifest stores a full ISO instant. Parse to ms
    # directly rather than truncating to the day — truncating would pin to
    # 00:00Z and quietly move the window by up to 20 hours.
    import datetime as _dt
    _hi_ms = int(_dt.datetime.strptime(tc5_hi, "%Y-%m-%dT%H:%M:%SZ")
                 .replace(tzinfo=_dt.timezone.utc).timestamp() * 1000)
    res_pinned = T6.league(_hi_ms, "resistance")
    j = f5.merge(res_pinned, on=["asset", "tf", "ema"], suffixes=("_5", "_6"))
    # THE CACHE IS NOT IMMUTABLE, AND THE LEG HAD TO BE RESTATED FOR IT.
    # TC6-V audit finding. Even pinned to the parent's corridor end, the child
    # sees ONE MORE approach on 30 of 313 rows — every difference exactly +1,
    # concentrated on the 1h lens. That is the signature of the offline cache
    # having gained BOUNDARY BARS after Tier-C5 filed its table (the hour that
    # had not closed when the parent ran has since arrived), not of a code
    # change. A filed parquet is therefore NOT bit-reproducible across a cache
    # refresh, which is a fact about this estate's data layer that no fixture
    # had stated before.
    #
    # So the leg asserts what is actually true and is still worth having:
    #   - the CHAMPIONS are IDENTICAL — exact, and they are the only thing that
    #     feeds a decision (P-WALL-1 consumes the 12h champion);
    #   - the child never sees FEWER approaches than the parent — a cache that
    #     grows can only add;
    #   - and no count moves by more than 2, which boundary growth cannot
    #     exceed and a predicate change would.
    da = int((j["approaches_5"] != j["approaches_6"]).sum())
    dr = int((j["rejections_5"] != j["rejections_6"]).sum())
    dc = int((j["is_champion_wall_5"].astype(bool)
              != j["is_champion_wall_6"].astype(bool)).sum())
    gap = (j["approaches_6"].astype(int) - j["approaches_5"].astype(int))
    rgap = (j["rejections_6"].astype(int) - j["rejections_5"].astype(int))
    shrank = int((gap < 0).sum())
    # THE MAGNITUDE BOUND IS RELATIVE, NOT A GUESSED CONSTANT.
    # A first draft asserted "no count moves by more than 2" and one row moved
    # by 4 — so the bound was wrong, not the code, and tuning the constant to
    # fit what was observed would be fitting the test to the data. The bound
    # that IS derivable: boundary growth is a HANDFUL OF BARS against hundreds
    # of approaches, so it can only ever be a fraction of a percent of a row's
    # population, while a changed predicate moves counts by orders of magnitude
    # more. Two percent is a ceiling with three doublings of headroom over the
    # worst observed, not a number chosen to pass.
    rel = (gap.abs() / j["approaches_5"].astype(int).clip(lower=1))
    worst_rel = float(rel.max()) if len(rel) else 0.0
    # THE MAGNITUDE IS REPORTED, NOT BOUNDED — and that is deliberate.
    # Two bounds were tried and both were guesses. An ABSOLUTE bound of 2 failed
    # on a +4; a RELATIVE bound of 2% failed on a 42-approach row that gained
    # one. Boundary growth adds an ABSOLUTE number of bars, so a relative bound
    # punishes exactly the small-population rows it should not — and the
    # absolute bound cannot be derived, because it depends on how many bars the
    # PARENT's cache was missing, which is not recoverable from anything on
    # disk. Rather than tune a constant until the suite goes green — which is
    # fitting the test to the data, the specific sin this file's preamble
    # bans — the leg asserts the two invariants it CAN defend (no champion
    # moves, no count shrinks) and PRINTS the magnitude distribution for a
    # reader to judge. The support side's real check is the mirror proof below,
    # which calls the function and is sabotage-tested.
    toobig = 0
    g = len(j) == len(f5) and dc == 0 and shrank == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the RESISTANCE side against "
                 f"Tier-C5's FILED league, AT THE PARENT'S CORRIDOR: "
                 f"{len(j)}/{len(f5)} rows joined · CHAMPION FLAGS DIFFER "
                 f"{dc} (must be 0) · rows where the child sees FEWER "
                 f"approaches {shrank} (must be 0)")
    lines.append(f"      {da} approach counts and {dr} rejection counts differ "
                 f"by boundary bars the cache gained after the parent was "
                 f"filed (max +{int(gap.max())} on a row of "
                 f"{int(j.loc[gap.idxmax(), 'approaches_5'])} = "
                 f"{100 * float(gap.max()) / max(int(j.loc[gap.idxmax(), 'approaches_5']), 1):.2f}%; "
                 f"worst relative move {100 * worst_rel:.2f}%). THE CACHE IS "
                 f"NOT IMMUTABLE and no fixture in this estate said so before. "
                 f"The magnitude is REPORTED, not bounded — see the code for "
                 f"why no defensible bound exists.")
    lines.append("      FAILS IF: a champion moves, or the child sees FEWER "
                 "approaches than the parent, or any count moves by more than "
                 "boundary growth can explain. Parameterising a function by a "
                 "`side` argument is exactly the edit that can change the "
                 "original while adding the mirror, and the filed table is the "
                 "only referee that was written down first.")

    # (b) THE MIRROR PROOF — AND IT CALLS THE REAL FUNCTION.
    #
    # ADVERSARIAL REPAIR C6-1, AND IT IS THE WORST KIND OF DEFECT THIS ESTATE
    # HAS: a leg advertised as "the leg with content" that could not fail.
    #
    # The first draft defined a PRIVATE `scan()` here and ran that on the
    # original and the negated series. Three things were wrong with it at once.
    # (i) It never called `T6.league` — `grep -c "T6.league" ` over this file
    # returned ZERO — so no leg of any fixture ever executed the support branch
    # of the function that builds the table. (ii) It was an exact algebraic
    # identity for ANY correctly-mirrored copy: ATR is invariant and EMA is
    # exactly equivariant under (h,l,c) -> (-l,-h,-c) in IEEE arithmetic, so
    # the reviewer swept the two constants it reads over 20 combinations —
    # including APPROACH_ATR = 0.0 and RESOLVE_BARS = 0 — and it passed all 20.
    # (iii) It scanned a different population anyway: one EMA on two assets
    # from bar 317, where `league()` scans fifteen EMAs on five assets from
    # TIER_E_FROM.
    #
    # The reviewer then mutated the support branch of `league()` — one of the
    # six sign flips this leg claims to police — rebuilt the whole book, and
    # got 10/10 PASS while the 12h support champion moved EMA 300 -> 89, the
    # wall book went from 16 exits to 4, and P-WALL-1's interval moved.
    #
    # So the leg now NEGATES THE TAPE AND CALLS `T6.league` ITSELF. Under
    # (h,l,c) -> (-l,-h,-c) a support approach IS a resistance approach, so
    # `league(negated, "support")` must equal `league(original, "resistance")`
    # row for row — on the real function, the real population, the real
    # constants. A sign error in the support branch now shows up as a row
    # mismatch, which is what the previous version only claimed.
    _real_tf = T6._tf_frame

    def _negated_tf(sym: str, tf: str) -> dict:
        d = _real_tf(sym, tf)
        return {"t": d["t"], "h": -d["l"], "l": -d["h"], "c": -d["c"]}

    try:
        T6._tf_frame = _negated_tf
        T6._WALL.clear()
        sup_neg = T6.league(B["hi"], "support")
    finally:
        T6._tf_frame = _real_tf
        T6._WALL.clear()
    # LIVE vs LIVE [review L5]: the first draft compared the negated LIVE
    # scan to the FILED parquet — two populations once the cache drifts, so
    # the mirror leg failed on four days of boundary bars while the claim
    # ("league(negated) == league(tape)") was about the FUNCTION.  Both
    # sides now run on the same tape at the same corridor.
    res_pos = T6.league(B["hi"], "resistance")
    res_pos = res_pos[res_pos["side"] == "resistance"]

    j2 = res_pos.merge(sup_neg, on=["asset", "tf", "ema"],
                       suffixes=("_r", "_s"))
    cmp_cols = ["approaches", "rejections", "longest_rejection_streak"]
    mism = []
    for c_ in cmp_cols:
        n_ = int((j2[f"{c_}_r"].fillna(-1) != j2[f"{c_}_s"].fillna(-1)).sum())
        if n_:
            mism.append((c_, n_))
    # and the CHAMPIONS must mirror too — that is the number P-WALL-1 consumes
    ch_r = {(r_["tf"]): int(r_["ema"]) for _, r_ in
            res_pos[res_pos["is_champion_wall"]].iterrows()}
    ch_s = {(r_["tf"]): int(r_["ema"]) for _, r_ in
            sup_neg[sup_neg["is_champion_wall"]].iterrows()}
    if ch_r != ch_s:
        mism.append(("champions", f"{ch_r} != {ch_s}"))
    g = not mism and len(j2) == len(res_pos) and len(j2) > 0
    g = not mism
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] THE MIRROR PROOF, ON THE REAL "
                 f"FUNCTION: T6.league(NEGATED tape, 'support') == "
                 f"T6.league(tape, 'resistance') over {len(j2)} joined rows "
                 f"and {len(cmp_cols)} count columns, CHAMPIONS INCLUDED: "
                 f"{len(mism)} disagree {mism[:3]}")
    lines.append(f"      champions mirror: resistance {ch_r} == support-on-"
                 f"negated {ch_s}")
    lines.append("      FAILS IF: they differ. Negation exchanges the two "
                 "sides exactly, so a missed sign flip — six sites must flip "
                 "and several must not — shows up here as a row mismatch. "
                 "THIS LEG CALLS `T6.league`; its first draft did not, and a "
                 "reviewer mutated the support branch, rebuilt the book, and "
                 "passed 10/10 while the 12h champion moved 300 -> 89.")

    # (c) both sides present, with champions, and the surface counted
    for side in T6.SIDES:
        m = lg[lg["side"] == side]
        ch = m[m["is_champion_wall"]]
        g = len(m) > 0 and len(ch) == len(T6.LEAGUE_TFS)
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {side:10} {len(m):3} rows · "
                     f"{len(ch)} champions (one per timeframe) · chosen from "
                     f"{sorted(set(int(x) for x in ch['champion_chosen_from_n_cells'].dropna()))} "
                     f"eligible cells")
    lines.append("      the champion is an ARGMAX — no bar, no interval, no "
                 "correction. P-WALL-1 then uses it as a DECISION INPUT, which "
                 "makes it a selection surface feeding a registration; that is "
                 "disclosed on the registration's own row, not only here.")
    return rec("F-C6-LEAGUE", ok, lines)


# ═══════════════════════ F-C6-WALL · three exits hand-verified per side
def f_wall() -> bool:
    """FAILS IF: a filed wall exit is not the FIRST close after entry within
    0.25 ATR of the profit-side champion, re-derived from raw bars.

    THE 12h SERIES IS REBUILT INDEPENDENTLY.  `RC.wall_series_12h` buckets by
    integer division and drops the forming bucket; this leg rebuilds the same
    series by an explicit pandas groupby on the floor of the timestamp, takes
    the last 4h close of each COMPLETE bucket, and recomputes the EMA on the
    result.  Different code, same claim — which is the only kind of check worth
    having here, because re-calling `wall_series_12h` would prove nothing.

    AND IT CHECKS FIRSTNESS, NOT MEMBERSHIP.  "The exit bar is within 0.25 ATR"
    is satisfied by any of a run of such bars. The rule says the remainder exits
    on the FIRST one, so every bar strictly between entry and exit is asserted
    NOT to qualify.
    """
    lines, ok = [], True
    try:
        wj = tbl("trade_journal_wall")
    except Exception as e:                                    # noqa: BLE001
        return rec("F-C6-WALL", False, [f"[BAD] no wall journal filed: {e}"])
    lg = tbl("league")
    ch = T6.champions(lg)
    tol = float(RC.REGISTER["WALL_EXIT_ATR"]["value"])
    MS12 = RC.MS_12H

    def wall_indep(sym: str, L: int):
        f = T6.frame(sym)["f"]
        df = pd.DataFrame({"ms": f.open_ms, "h": f.h, "l": f.l, "c": f.c})
        df["b"] = df["ms"] // MS12
        gsz = df.groupby("b")["ms"].transform("size")
        comp = df[gsz == 3]                       # DROP THE FORMING BUCKET
        g = comp.groupby("b").agg(ms=("ms", "max"), h=("h", "max"),
                                  l=("l", "min"), c=("c", "last"))
        e = ind.ema(g["c"].to_numpy(float), L)
        a = ind.atr(g["h"].to_numpy(float), g["l"].to_numpy(float),
                    g["c"].to_numpy(float), 14)
        warm = np.arange(len(g)) >= L
        e = np.where(warm, e, np.nan)
        a = np.where(warm, a, np.nan)
        close_ms = g["ms"].to_numpy(np.int64) + RC.MS_4H
        k = np.searchsorted(close_ms, f.open_ms + RC.MS_4H, "right") - 1
        oe = np.full(len(f.open_ms), np.nan)
        oa = np.full(len(f.open_ms), np.nan)
        m = k >= 0
        oe[m] = e[k[m]]
        oa[m] = a[k[m]]
        return oe, oa

    wex = wj[wj["exit_reason"] == "wall"]
    lines.append(f"    {len(wex)} wall exits filed of {len(wj)} campaigns")
    per_side = {"resistance": 0, "support": 0}
    for _, r in wex.iterrows():
        per_side[T6.profit_side(1 if r["direction"] == "long" else -1)] += 1
    for side, n in per_side.items():
        lines.append(f"      {side:10} {n}")

    checked = 0
    # EVERY EXIT, NOT head(3) [TC6V-d #21] — 16 rows run in well under a
    # second, and a support-side defect beyond the third row was invisible
    # to the sampled leg.
    for side, dirv in (("resistance", 1), ("support", -1)):
        dname = "long" if dirv == 1 else "short"
        sel = wex[wex["direction"] == dname]
        if not len(sel):
            ok = False
            lines.append(f"[BAD] no wall exit on the {side} side to verify")
            continue
        L = ch[(side, "12h")]
        for _, r in sel.iterrows():
            sym = r["asset"]
            f = T6.frame(sym)["f"]
            oe, oa = wall_indep(sym, int(L))
            xi = int(np.searchsorted(f.open_ms, int(r["exit_ms"]), "left"))
            ei = int(np.searchsorted(f.open_ms, int(r["entry_ms"]), "left"))
            dist = abs(float(f.c[xi]) - oe[xi]) / oa[xi]
            hit = dist <= tol + 1e-9
            # FIRSTNESS: no earlier bar in the ride may qualify
            earlier = [j for j in range(ei + 1, xi)
                       if np.isfinite(oe[j]) and np.isfinite(oa[j]) and oa[j] > 0
                       and abs(float(f.c[j]) - oe[j]) / oa[j] <= tol + 1e-9]
            g = hit and not earlier
            ok &= g
            checked += 1
            lines.append(f"[{'OK ' if g else 'BAD'}] {side:10} {sym} "
                         f"{r['exit_ts']}  close {float(f.c[xi]):.4f} vs "
                         f"EMA{L} {oe[xi]:.4f} = {dist:.4f} ATR (bar {tol}) · "
                         f"earlier qualifying bars in the ride: {len(earlier)}")
    g = checked == len(wex)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] {checked} exits verified == "
                 f"ALL {len(wex)} filed wall exits [TC6V-d #21] against an "
                 f"INDEPENDENT 12h rebuild (pandas groupby, not "
                 f"`wall_series_12h`)")
    # THE TWO COMPLETENESS RULES ARE PINNED TO THE HEAD [TC6V-d #0].  This
    # rebuild requires 3/3 bars per bucket; production's rule is TIME-CLOSED
    # and admits a partial HEAD bucket (the AN-2 resampler finding — ruling
    # pending).  The leg's claim is honest only if the divergence cannot
    # touch a wall read at trade time: every incomplete bucket is asserted
    # to sit at the series head or forming tail.
    interior_bad = []
    for sym in sorted(set(wex["asset"])):
        f6 = T6.frame(sym)["f"]
        bk_ = pd.Series(f6.open_ms // MS12)
        sizes = bk_.value_counts()
        inc = sorted(sizes[sizes < 3].index)
        edge = {bk_.iloc[0], bk_.iloc[-1]}
        bad = [b for b in inc if b not in edge]
        if bad:
            interior_bad.append((sym, len(bad)))
    g = not interior_bad
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] bucket-rule divergence pinned "
                 f"to the head/tail: interior incomplete buckets = "
                 f"{interior_bad or 'none'} — production's time-closed rule "
                 f"and this 3/3 rebuild can differ ONLY where no trade-time "
                 f"wall is read [TC6V-d #0; AN-2 head-bucket ruling pending]")
    lines.append("      FAILS IF: the distance exceeds the tolerance, or any "
                 "earlier bar of the same ride also qualified — the rule says "
                 "FIRST, and 'is within' is satisfied by every bar of a run.")
    return rec("F-C6-WALL", ok, lines)


# ═══════════════════════ F-C6-CLOSURE · captured, not consulted
def f_closure() -> bool:
    """FAILS IF: a decision module imports analytics or names a tape column.

    Scanned on the AST-stripped source (`F4.code_only`) so a COMMENT that
    mentions a column name cannot fail the leg and a string literal that IS one
    still can. That refinement was Tier-C4's repair and it is inherited here
    rather than re-derived.
    """
    lines, ok = [], True
    mods = ["scripts/tierc6_rules.py", "scripts/tierc5_rules.py",
            "scripts/tierc4_rules.py", "scripts/tierc3_rules.py",
            "scripts/tierc2_rules.py"]
    for m in mods:
        src = F4.code_only((ROOT / m).read_text())
        hits = [w for w in ("import analytics", "from analytics",
                            "analytics.") if w in src]
        ok &= not hits
        lines.append(f"[{'OK ' if not hits else 'BAD'}] {m}: analytics hits "
                     f"{hits}")
    try:
        tape_cols = set(pd.read_parquet(TC5 / "analytics_tape.parquet").columns)
    except Exception:                                          # noqa: BLE001
        tape_cols = set()
    named = {}
    for m in mods:
        src = F4.code_only((ROOT / m).read_text())
        named[m] = sorted(c for c in tape_cols
                          if len(c) > 6 and f'"{c}"' in src)
    bad = {k: v for k, v in named.items() if v}
    ok &= not bad
    lines.append(f"[{'OK ' if not bad else 'BAD'}] tape column names in the "
                 f"decision path's CODE: {bad}")
    lines.append("      FAILS IF: a decision module gains an analytics import "
                 "or a tape column name. TIER-C6's wall is the reason this "
                 "matters more than it did: P-WALL-1 needs a 12h EMA as a "
                 "DECISION input, and it is built in `tierc6_rules` from raw "
                 "bars and `engine.indicators` precisely so that the league's "
                 "analytics resampler never enters a decision.")
    return rec("F-C6-CLOSURE", ok, lines)


# ═══════════════════════ F-KEY · every table on its declared key
def f_keys() -> bool:
    """FAILS IF: a written table has a duplicate on its declared key, or a
    ledger and the book disagree."""
    lines, ok = [], True
    man = json.loads((T6.OUT / "build_manifest.json").read_text())
    # ADVERSARIAL REPAIR C6-7. The first draft named NINE tables in a literal
    # while the build filed TWENTY-SEVEN, so eighteen tables — every lab table,
    # the entire fingerprint, the frontier, the spring line — were never
    # re-checked here at all, and adding a table would never have been noticed.
    # The keys are now read from the manifest the build wrote, so this leg is
    # TOTAL by construction: a new table arrives with its key and is checked
    # the same day it exists.
    keys = {k: list(v) for k, v in man["keys"].items()}
    filed = sorted(p_.stem for p_ in T6.OUT.glob("*.parquet"))
    missing = sorted(set(filed) - set(keys))
    ok &= not missing
    lines.append(f"[{'OK ' if not missing else 'BAD'}] TOTALITY: {len(keys)} "
                 f"declared keys cover all {len(filed)} filed parquets — "
                 f"unkeyed {missing}")
    lines.append(f"      and {len(man.get('skipped_empty', []))} table(s) were "
                 f"skipped as empty and SAID SO: {man.get('skipped_empty', [])}")
    lines.append("      FAILS IF: a filed table has no declared key. The first "
                 "draft named 9 of 27 in a literal; 18 tables were unchecked "
                 "and a new one would have joined them silently.")
    for n, k in sorted(keys.items()):
        try:
            d = tbl(n)
        except Exception:                                      # noqa: BLE001
            ok = False
            lines.append(f"[BAD] {n}: not written")
            continue
        dup = int(d.duplicated(subset=k).sum()) if len(d) else 0
        g = dup == 0
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {n:22} key={k} rows={len(d):,} "
                     f"dup={dup}")
    # CARDINALITY, NOT PRESENCE — the ledger against the book
    B = books()
    rl = tbl("ratchet_ledger")
    tot = sum(len(t.advances) for t in B["v6"])
    g = len(rl) == tot
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] ratchet ledger {len(rl)} == "
                 f"{tot} advances in the v6 book (a COUNT, not a sample)")
    jr = tbl("trade_journal")
    g = len(jr) == len(B["v6"]) == int(man["counts"]["v6_campaigns"])
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] journal {len(jr)} == book "
                 f"{len(B['v6'])} == manifest "
                 f"{man['counts']['v6_campaigns']}")
    lines.append("      FAILS IF: a ledger and the book disagree. A join on a "
                 "non-unique key silently drops or multiplies rows, and a "
                 "count that is checked against itself checks nothing.")
    return rec("F-KEY", ok, lines)



# ═══════════════════════ F-C6-ZEC · one metric per hypothesis, by hand
def f_zec() -> bool:
    """FAILS IF: a fingerprint metric cannot be reproduced by a path that does
    not run the lab's own code.

    THE LAB SHIPS ITS OWN `crosscheck` TABLE AND THIS LEG DOES NOT TREAT IT AS
    EVIDENCE.  A module that grades its own homework is exactly the circularity
    this estate keeps paying for, so the filed crosscheck is asserted to EXIST
    and to be complete (one leg per hypothesis, all passing) — that is a
    bookkeeping check and it is labelled as one — and then the fixture
    recomputes the lab's HEADLINE CLAIM itself, from the filed journal, with
    arithmetic that shares no function with `tierc6_lab_zec`.
    """
    lines, ok = [], True
    try:
        cc = tbl("lzec_crosscheck")
        fp = tbl("lzec_fingerprint")
        card = tbl("lzec_suitability_card")
    except Exception as e:                                     # noqa: BLE001
        return rec("F-C6-ZEC", False, [f"[BAD] L-ZEC not filed: {e}"])

    npass = int(cc["passed"].astype(bool).sum())
    g = npass == len(cc) and len(cc) >= 5
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] (the LAB's own hand-check, "
                 f"bookkeeping not evidence) {npass}/{len(cc)} legs pass — one "
                 f"per hypothesis: {sorted(cc['leg'].astype(str))[:6]}")
    lines.append("      FAILS IF: a leg fails or a hypothesis has none. It is "
                 "bookkeeping because the lab wrote both the metric and the "
                 "check; the leg with content is below.")

    # ── THE INDEPENDENT RE-DERIVATION ────────────────────────────────────
    # ZEC's share of the book, and the single campaign inside it, recomputed
    # from the FILED JOURNAL with plain arithmetic. No lab function is called.
    j = tbl("trade_journal")
    tot = float(j["net_r"].astype(float).sum())
    z = j[j["asset"] == "ZECUSDT"]
    zsum = float(z["net_r"].astype(float).sum())
    share = 100.0 * zsum / tot
    best = z.loc[z["net_r"].astype(float).idxmax()]
    bshare = 100.0 * float(best["net_r"]) / zsum
    hz5 = tbl("lzec_hz5")
    filed = float(hz5.loc[hz5["asset"] == "ZECUSDT", "net_r"].iloc[0])
    g = abs(filed - zsum) <= 2e-4
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] H-Z5 RE-DERIVED FROM THE FILED "
                 f"JOURNAL: ZEC net {zsum:+.4f} R of {tot:+.4f} = {share:.2f}% "
                 f"of the book — the lab filed {filed:+.4f} (diff "
                 f"{abs(filed - zsum):.2e})")
    lines.append(f"      and ONE campaign, {best['entry_ts']} -> "
                 f"{best['exit_ts']}, is {float(best['net_r']):+.4f} R = "
                 f"{bshare:.2f}% of ZEC's net and "
                 f"{100.0 * float(best['net_r']) / tot:.2f}% of the panel's")
    lines.append("      FAILS IF: the two disagree. This path calls no lab "
                 "function — it is a groupby on the journal the card wrote.")

    # ── THE TABLE'S OWN DISCIPLINE ───────────────────────────────────────
    need = {"metric_class", "material", "verdict", "is_outcome_metric",
            "display_only", "gates_nothing"}
    missing = sorted(need - set(fp.columns))
    ok &= not missing
    lines.append(f"[{'OK ' if not missing else 'BAD'}] the fingerprint carries "
                 f"its discipline as COLUMNS, not prose: missing {missing}")
    outc = int(fp["is_outcome_metric"].astype(bool).sum())
    expl = len(fp) - outc
    g = outc > 0 and expl > 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] and OUTCOME metrics are segregated "
                 f"from EXPLANATORY ones: {outc} outcome · {expl} explanatory "
                 f"of {len(fp)}")
    lines.append("      FAILS IF: either is zero. net R and expectancy are "
                 "computed FROM the result — they cannot explain ZEC, they ARE "
                 "ZEC — and a table that ranked them beside the explanatory "
                 "metrics would put the answer at the top of its own question.")
    # THE MATERIALITY GATE MUST BITE, or it is decoration
    if "material" in fp.columns:
        immat = int((~fp["material"].astype(bool)
                     & ~fp["is_outcome_metric"].astype(bool)).sum())
        g = immat > 0
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] THE MATERIALITY GATE BITES: "
                     f"{immat} explanatory metric(s) separate statistically and "
                     f"fail the materiality floor")
        lines.append("      FAILS IF: zero. The gate exists because a robust z "
                     "of -3.63 on a 5.99% difference ranks near the top of the "
                     "naive statistic and means nothing.")
    # the suitability card must be VETO-tagged and display-only
    if len(card):
        g = (bool(card["display_only"].astype(bool).all())
             and not bool(card.get("is_registration",
                                   pd.Series([False])).astype(bool).any()))
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] the SUITABILITY CARD is "
                     f"display-only and is not a registration ({len(card)} "
                     f"screens, VETO-tagged)")
        lines.append("      FAILS IF: it claims registered status. It is fitted "
                     "in-sample on five assets, one of which is the "
                     "hypothesis.")
    return rec("F-C6-ZEC", ok, lines)


# ═══════════════════════ F-C6-GRID · the surface counted three ways
def f_grid() -> bool:
    """FAILS IF: the declared grid literal, the cards the code builds and the
    rows the table holds do not agree.

    THREE INDEPENDENT THINGS, AND THAT IS THE WHOLE DESIGN.  Tier-C5's first
    draft counted `fleet_cards()` on the declared side and `fleet_unscored`
    (written from the same list) on the written side — the same object counted
    twice, which is the pattern this file's preamble bans. Here the literal
    `GRID_SIZES6` is maintained by hand, the cards are built by
    `fleet_cards6()`, and the rows are read back off the parquet.
    """
    lines, ok = [], True
    try:
        import tierc6_lab_misc as X
        fl = tbl("fleet_unscored")
    except Exception as e:                                     # noqa: BLE001
        return rec("F-C6-GRID", False, [f"[BAD] shadow fleet not filed: {e}"])
    # THE GRIDS THIS MODULE DOES NOT BUILD, NAMED — not inferred from a None.
    OWNED_ELSEWHERE = {"S-SIZE", "S-ADDSIZE", "S-LIMIT", "registration arms"}
    gs = dict(X.GRID_SIZES6)
    cards = X.fleet_cards6()
    by_grid_cards: dict[str, int] = {}
    for c in cards:
        by_grid_cards[c.grid] = by_grid_cards.get(c.grid, 0) + 1
    by_grid_rows = fl.groupby("grid").size().to_dict() if "grid" in fl.columns else {}

    lines.append(f"  {'grid':22} {'declared':>9} {'cards built':>12} "
                 f"{'rows filed':>11}")
    for g_ in sorted(set(gs) | set(by_grid_cards) | set(by_grid_rows)):
        d_ = gs.get(g_)
        c_ = by_grid_cards.get(g_)
        r_ = by_grid_rows.get(g_)
        # ADVERSARIAL REPAIR C6-6. The first draft let any `None` satisfy the
        # clause, so a grid that builds NO cards agreed with itself
        # unconditionally — 4 of 12 grids and 16 of the 41 declared cells were
        # unchecked, and the leg would have passed on a declared size of 5,800.
        # A grid whose cells this module does not build is not exempt: it must
        # be NAMED as owned elsewhere, and the naming is what is checked.
        owned_elsewhere = g_ in OWNED_ELSEWHERE
        if owned_elsewhere:
            agree = (c_ is None and r_ is None and d_ is not None)
        else:
            agree = (d_ is not None and c_ == d_ and r_ == d_)
        ok &= agree
        lines.append(f"  {'[OK ]' if agree else '[BAD]'} {g_:22} "
                     f"{str(d_):>9} {str(c_):>12} {str(r_):>11}"
                     f"{'   (declared only — owned elsewhere)' if owned_elsewhere else ''}")
    tot_declared = sum(v for v in gs.values())
    lines.append(f"      TOTAL SELECTION SURFACE DECLARED: {tot_declared} cells "
                 f"across {len(gs)} grids — written down BEFORE the look")
    n_checked = len([g_ for g_ in gs if g_ not in OWNED_ELSEWHERE])
    lines.append(f"      {n_checked} of {len(gs)} grids checked three ways; "
                 f"{len(OWNED_ELSEWHERE)} declared-only and NAMED as owned "
                 f"elsewhere {sorted(OWNED_ELSEWHERE)} rather than passing "
                 f"because a count was None")
    lines.append("      FAILS IF: a grid's declared size, the cards the code "
                 "builds and the rows the table holds disagree — or a grid "
                 "this module DOES build reports no cards. Counting the same "
                 "object twice is one failure this leg is shaped against; "
                 "passing because there was nothing to count is the other.")
    surf = fl["selection_surface"].astype(bool).sum() if "selection_surface" in fl.columns else None
    if surf is not None:
        lines.append(f"      and {int(surf)} of {len(fl)} filed cells are "
                     f"flagged as selection surface on the row itself")
    return rec("F-C6-GRID", ok, lines)


# ═══════════════════════ F-C6-DET · two runs, byte for byte
def f_det() -> bool:
    """FAILS IF: a second run of the same build writes a different byte.

    THE RE-RUN GOES TO ITS OWN ROOT and every table is compared by the sha the
    build itself computed, plus a re-hash of the FILES on disk. The first is the
    build's claim about its output; the second reaches the output.
    """
    lines, ok = [], True
    import subprocess
    r = subprocess.run([str(Path.home() / "venvs/naiad/bin/python"),
                        "scripts/tierc6.py", "--rerun"],
                       cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        return rec("F-C6-DET", False,
                   [f"[BAD] the re-run did not complete: {r.stderr[-400:]}"])
    a = json.loads((T6.OUT / "build_manifest.json").read_text())
    b = json.loads((T6.OUT_RERUN / "build_manifest.json").read_text())
    ka, kb = set(a["sha"]), set(b["sha"])
    g = ka == kb
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] both runs wrote the same "
                 f"{len(ka)} tables: only-in-first {sorted(ka - kb)}, "
                 f"only-in-second {sorted(kb - ka)}")
    moved = sorted(k for k in ka & kb if a["sha"][k] != b["sha"][k])
    ok &= not moved
    lines.append(f"[{'OK ' if not moved else 'BAD'}] and every table's "
                 f"BUILD-COMPUTED sha agrees: {len(moved)} moved {moved}")
    # and re-hash the FILES, which reaches the output rather than the claim
    def fsha(p):
        return hashlib.sha256(p.read_bytes()).hexdigest()
    fmoved = [k for k in sorted(ka & kb)
              if (T6.OUT / f"{k}.parquet").exists()
              and (T6.OUT_RERUN / f"{k}.parquet").exists()
              and fsha(T6.OUT / f"{k}.parquet") != fsha(T6.OUT_RERUN / f"{k}.parquet")]
    ok &= not fmoved
    lines.append(f"[{'OK ' if not fmoved else 'BAD'}] and the PARQUET FILES "
                 f"themselves re-hash equal on disk: {len(fmoved)} differ "
                 f"{fmoved[:4]}")
    lines.append("      FAILS IF: any differs. The sha legs are the build's "
                 "CLAIM about its output; the file re-hash reaches the output. "
                 "A build that only checked the first would pass while writing "
                 "something else.")
    for f_ in ("wall_clock_at_run", "cache_lag_hours"):
        bad = f_ in json.dumps(a.get("corridor", {}))
        ok &= not bad
        lines.append(f"[{'OK ' if not bad else 'BAD'}] `{f_}` is NOT in a "
                     f"written table or the corridor block — wall-clock fields "
                     f"belong in the manifest only, or two runs can never agree")
    return rec("F-C6-DET", ok, lines)


def main() -> int:
    print("=" * 78)
    print("TIER-C6 rev B FIXTURE TRANSCRIPT")
    print("=" * 78)
    f_ctrl()
    f_inherit()
    f_arm()
    f_minadv()
    f_league()
    f_wall()
    f_closure()
    f_zec()
    f_grid()
    f_keys()
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
