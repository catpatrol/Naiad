#!/usr/bin/env python
"""TIER-C11 · STAGE R-a — R1 lenses · R2 feasibility per lens · R3 the nest on the
books (+ the reusable `nest-book` door) · R5 the chop table [LEANS L-R.1..L-R.5,
L-R.7; AM-1, AM-4, AM-6].

Contract of record: exchange/queue/2026-09-24_TC11_APOLLO.md (sha256 bb38e016…,
STEP Q b9ed953).  Executor HEPHAESTUS; seed 20260924.  Readings of record:
research_outputs/tierc11/LEANS.md (frozen) + LEANS_AMENDMENTS.md (AM-1..AM-7).
A RUNNER: it imports tierc11_nest (the only module that may reach the range
machine, L-0.3) and through it tierc11_env (E) and tierc10_census (C).  It is not
in the L-F.2 DECISION set; no decision module imports it.  It computes and scores
no registered book: every table it writes is TIER-E ("a SELECTION, not a
result", gates nothing) EXCEPT the seven R2 lens verdicts of record (L-R.4).

WHAT IT BUILDS (research_outputs/tierc11/stage_r/)
  R1_LENSES.parquet/.md     per asset x lens (CLASSIC5 x {5m,15m,1h,4h,12h,1d,1w};
                            UNSEEN12 x {1h,4h,1d}): the FILED pick of record
                            (SCALE_PICKS.json — a pin, never re-fitted) with its
                            window and labels, the tuning / whole-tape / first-half
                            picks and frozen 3.0, the confirmed-range count and
                            density per 100 bars at the pick of record and at 3.0
                            per era (ALL / tuning / holdout, era = the confirm
                            bar's CLOSE), the stability flag; the pins block and
                            the whole density grid in the .md [L-R.1..L-R.3].
  R2_FEASIBILITY.parquet/.md  TC10's [Q-R3] legs through the census's OWN
                            functions (C._r34_walk -> C.height_rows / height_grid ->
                            C.edge_arrays / edge_gate -> C.verdict_rows), per asset
                            AND pooled (POOLED:CLASSIC5 at every lens, POOLED:PANEL17
                            at 1h/4h/1d), x era {ALL, tuning, holdout} x scale
                            {calibrated, frozen3.0} x toll {taker (record, 10 bps rt),
                            charter twin (2 x (5 + slip tier) bps rt), maker twin
                            (4 bps rt)}.  The LENS VERDICT OF RECORD per lens =
                            POOLED:CLASSIC5 · holdout · calibrated · taker (`word` +
                            `verdict` on those 7 rows ONLY); every other row is Tier-E
                            with NO verdict word — its word in `would_read`, the census
                            booleans renamed *_would_pass (SR-13); the height ratio's
                            deciles d1..d9 carried and printed; the TC10 continuity
                            columns (AM-1, tc10_would_read / tc10_would_pass) beside
                            5m/4h/1d taker rows.
  R2_LENS_VERDICTS.json     {lens: {verdict, provisional, maker_twin, charter_twin,
                            n_ranges, ratio_median, share_ratio_lt_1, toll, edge_n,
                            edge_n_ranges, edge_median_term_h20, edge_toll_atr,
                            edge_net_h20, era, scale, pool, …}} for all 7 lenses —
                            Stage S reads the 1h entry (L-S.1).
  NEST_v6.parquet / NEST_trg912.parquet   the nest vector (N.nest_at) at every
                            instant of every campaign of both books, calibrated
                            (record) and frozen3.0 (twin) [L-R.5, AM-6].
  NEST_GRID_{FREQ,BY_STATE,BY_COIN}.parquet + NEST_GRID.md   the nesting grid at
                            ENTRY, whole; every row with its honesty labels and the
                            HOLDOUT slice beside (SR-12).
  R5_CHOP.parquet / R5_FIVE_ROW.parquet / R5_CHOP.md   v6 outcomes by 4h and 12h
                            state x %-of-range decile at entry, honesty labels and the
                            holdout slice beside (SR-12); TC10's five-row table (4h,
                            frozen 3.0) reproduced beside, all eleven columns [L-R.7].
  R5_CHOP_DIRECTION.parquet (+ its section in R5_CHOP.md / STAGE_R.md)   [SR-16; the
                            trading review D-2] BESIDE the unchanged R5 rows: the same v6
                            entries by 4h / 12h state split EXP_ALIGNED / EXP_COUNTER /
                            IN_RANGE / NONE (aligned = BULL_EXP for a long, BEAR_EXP for a
                            short) and the IN_RANGE entries by direction-adjusted pct
                            tercile (pct long, 100 - pct short; '<0', '>=100'), both
                            scales, n / n_long / n_short / E[net R] / P(win) / sum R with
                            SR-12's honesty labels and holdout slice — collared Tier-E,
                            decides nothing; partitioned against R5_CHOP (HALT otherwise).
  nestbook_probe/V6-PROBE/base.{parquet,json} + nest_books/V6-PROBE__base.{parquet,json}
                            the nest-book door tested on v6 (a probe in the REGBOOK
                            schema — NOT a registration).
  STAGE_R.md                the stage report, every table whole.
  build_manifest.json       content shas, keys, input shas, readings (no clock).
  lanes/ (the `lanes` subcommand, SR-15 — its own manifest; not part of `build`)
    NEST_<REG>.parquet/.json   the nest vector at every instant of every campaign of every
                            registered lane book (P-WARN-1, P-AGE-1, P-WIN-1, P-BRK-4H + its
                            tierE__panel17, P-RELAY-1, P-ADD-BRK, P-ADD-SFP, P-TP-RNG scored),
                            both scales, each row's named_event and exit_reason beside.
    NEST_GRID_LANES_{FREQ,BY_STATE,BY_COIN}.parquet + NEST_GRID_LANES.md   the nesting grid
                            at ENTRY per lane book, whole, collared, SR-12's honesty labels.
    LANES_MANIFEST.json     content shas, keys, per-book book_sha256 (== the scorer's input)
                            and the regbook bytes stamped (content + file sha), event
                            sources, input shas.

THE nest-book DOOR (for the later lanes pass):
  tierc11_stage_r.py nest-book --regbook <dir> --arm scored
                               --kind {v6transform,lane4h,relay,scalp5m} [--out DIR]
  reads <dir>/<arm>.parquet + <arm>.json (the REGBOOK INTERFACE), verifies n and
  book_sha256, stamps every campaign at its own lens bars (arm or entry -> exit)
  plus its named events, both scales, and writes
  stage_r/nest_books/<REG>__<arm>.{parquet,json} (or DIR).  Column conventions it
  reads are listed in NESTBOOK_COLUMNS (READINGS SR-9).  It REFUSES (HALT, naming
  the counts) a regbook whose own record (harvested / latched_1h / reached_1r /
  n_adds) says an event happened that no column stamps — it never files a nest that
  silently drops a named event [L-R.5; verifier MAJOR-4].

THE LANES PASS (SR-15): tierc11_stage_r.py lanes [--out-dir=DIR]  runs the door over
  every lane book (LANE_BOOKS) after verifying each is the book the scorer scored
  (scores/SCORE_MANIFEST.json), and writes stage_r/lanes/ (or DIR: a child of
  _det_stage_r/, or of a `_det_stage_r/` scratch outside the repo).

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_r.py build [--out-dir=DIR]
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_r.py lanes [--out-dir=DIR]
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_r.py nest-book --regbook DIR \\
            --arm scored --kind v6transform [--out DIR]
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_r.py lean      # the lean block
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tierc11_nest as N                                             # noqa: E402  (the range door)

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

E, C, RC = N.E, N.C, N.RC
TP = E.TP

# ══════════════════════════════════════════════════════════ 0 · CONSTANTS OF RECORD
ROOT = E.ROOT
OUT = E.OUT / "stage_r"
DET_ROOT = OUT / "_det_stage_r"
PIN_MS = E.PIN_MS
PIN_ISO = E.PIN_ISO
SEED = E.SEED
SUBSTRATE = E.SNAPSHOT.name
LEAN_TAG = E.LEAN_TAG
MS_4H = N.LENS_MS["4h"]
CLASSIC5 = tuple(E.CLASSIC5)
UNSEEN12 = tuple(E.UNSEEN12)
PANEL17 = tuple(E.PANEL17)
LENSES11 = tuple(N.LENSES11)                    # 5m 15m 1h 4h 12h 1d 1w
UNSEEN_LENSES = ("1h", "4h", "1d")              # [L-R.1] the twelve, Tier-E
NEST_LENSES = tuple(N.NEST_LENSES)              # 1h 4h 12h 1d 1w
ERAS = tuple(C.ERAS)                            # ALL tuning holdout
SCALE_KINDS = ("calibrated", "frozen3.0")       # record, twin
TOLLS = ("taker", "charter", "maker")           # record, twin, twin [L-R.4]
POOL_C5 = "POOLED:CLASSIC5"
POOL_P17 = "POOLED:PANEL17"
POOLS = {POOL_C5: (CLASSIC5, LENSES11), POOL_P17: (PANEL17, UNSEEN_LENSES)}
TC10_POOL_NAME = {POOL_C5: "POOLED:CLASSIC5", POOL_P17: "POOLED:ALL"}   # TC10's labels
TC10_LENSES = ("5m", "4h", "1d")                # the lenses TC10 measured [AM-1]
RECORD = {"panel": POOL_C5, "era": "holdout", "scale_kind": "calibrated", "toll": "taker"}
COLLAR = {"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
          "gates": "nothing"}
RECORD_COLLAR = {"tier": "R2 LENS VERDICT OF RECORD [L-R.4]",
                 "selection_not_a_result": "n/a — the lens verdict of record, not a selection",
                 "gates": ("range trading on this lens in this and every later tier unless the "
                           "toll model changes [contract R2]; at 1h also Stage S [L-S.1]")}
AS_OF = {"as_of_last_closed_4h": PIN_ISO, "as_of_substrate": SUBSTRATE}
WORD_PASS, WORD_FAIL, WORD_PROV = "PASS", "FAIL", "FAIL (provisional, n<30)"
REOPEN = ("FAIL — maker twin PASSES (the reopening path; needs a toll-model change the "
          "operator rules)")
DISCLOSURE = (
    "Disclosure [L-R.4]: TC10's per-era Q-R3 verdicts for 5m, 4h and 1d were seen before "
    "this era was chosen (4h CLASSIC5 pooled passes only on the holdout, +0.0062 ATR; 1d "
    "passes ALL and tuning and fails the holdout). 1h, 12h and 1w were never measured. The "
    "holdout is of record because the scale is tuning-calibrated.")
BOOKS = ("v6", "trg912")
BOOK_DIR = E.OUT / "books"
STATES4 = ("NONE", "IN_RANGE", "BULL_EXP", "BEAR_EXP")
COIN_CATS = ("both", "top", "bot", "none")
COIN_RULES = ("record", "mem_twin")
DECILES = tuple(f"[{10 * d},{10 * d + 10})" for d in range(10))
R5_LENSES = ("4h", "12h")
R5_BUCKETS = DECILES + ("<0", ">=100", "not-in-range:NONE", "not-in-range:BULL_EXP",
                        "not-in-range:BEAR_EXP", "__ALL__")
# R5 BY DIRECTION [SR-16; the trading review D-2, FINAL_REVIEW_2026-09-25] — beside the
# unchanged, direction-blind L-R.7 rows: collared Tier-E rows that decide nothing
R5_DIR_TABLE = "R5_CHOP_DIRECTION"
R5_ALIGN_BUCKETS = ("EXP_ALIGNED", "EXP_COUNTER", "IN_RANGE", "NONE", "__ALL__")
R5_ADJ_CUTS = (100.0 / 3.0, 200.0 / 3.0, 100.0)   # exact thirds; 100 opens '>=100' (SR-8's law)
R5_ADJ_BUCKETS = ("<0", "[0,33.33)", "[33.33,66.67)", "[66.67,100)", ">=100")
R5_DIR_BUCKETS = {"alignment": R5_ALIGN_BUCKETS, "pct_dir_adj": R5_ADJ_BUCKETS}
R5_DIR_SPLIT_LAW = {
    "alignment": ("the lens state at entry by the trade's direction: EXP_ALIGNED = BULL_EXP for "
                  "a long / BEAR_EXP for a short; EXP_COUNTER = the other expansion; IN_RANGE / "
                  "NONE as read [SR-16]"),
    "pct_dir_adj": ("IN_RANGE entries by direction-adjusted pct-of-range (pct for a long, "
                    "100 - pct for a short; 100 = the boundary the trade must break): "
                    "[0,100/3), [100/3,200/3), [200/3,100), '<0', '>=100' [SR-16]")}
TC10_STATES = ("BEAR_EXP", "BULL_EXP", "NEUTRAL", "NONE", "__ALL__")
FIVE_ROW_COLS = ("n", "n_assets", "net_r_sum", "expectancy_r", "median_net_r",
                 "win_rate_pct", "median_mfe_r", "median_pct_of_range",
                 "median_dist_boundary_atr", "n_in_range", "provisional")
TC10_JOURNAL_REL = "research_outputs/tierc10/panel/control_journal.parquet"
TC10_FIVE_ROW_REL = "research_outputs/tierc10/stamps/control_entry_by_state.parquet"
TC10_VERDICT_REL = "research_outputs/tierc10/census/height_toll_verdict.parquet"
TC10_WINDOW_CLOSE_MS = 1_790_006_400_000        # 2026-09-21T16:00:00Z (TC10's pin)
RATIO_DECILES = tuple(range(1, 10))              # the census's height ratio d1..d9 [contract R2]
TIER_E_WORD_COLS = ("would_read", "height_leg_would_pass", "edge_leg_would_pass",
                    "census_would_pass", "tc10_would_read", "tc10_would_pass")

# ── THE STAMP LAW [L-R.5, AM-6] — read at CALL time (F-NEST-BOOK plants it) ─────
INTRABAR_STAMP = "bar_open"                      # "bar_open" (record) | "bar_close" (sabotage)
INTRABAR_EXIT_REASONS = ("stop", "tp", "target")
CLOSE_EXIT_PREFIXES = ("bell", "corridor_end", "warn", "invalidation", "close")
EXIT_1H_COLS = ("exit_instant_ms", "exit_close_1h_ms")   # a 1h-walked ride's resolved exit
# the exit bar's lens CLOSE when exit_close_ms is not it (the relay files its 1h exit instant
# as exit_close_ms): the anchor of an intrabar exit's post-event twin [SR-15 THE TWIN LAW]
EXIT_BAR_CLOSE_COLS = ("exit_bar_close_ms",)

# ── THE REGBOOK INTERFACE (the orchestrator's binding schema) ────────────────
REGBOOK_REQUIRED = ("symbol", "entry_ms", "entry_close_ms", "direction", "entry_px",
                    "stop_px", "r_dist", "exit_close_ms", "exit_reason", "net_r", "gross_r",
                    "fee_r", "funding_r", "haircut_net_r", "era", "lane")
REGBOOK_FLOATS = ("entry_px", "stop_px", "r_dist", "net_r", "gross_r", "fee_r", "funding_r",
                  "haircut_net_r")
KINDS = {"v6transform": {"lens": "4h", "start": "arm"},
         "lane4h": {"lens": "4h", "start": "entry"},
         "relay": {"lens": "4h", "start": "arm"},
         "scalp5m": {"lens": "5m", "start": "entry"}}
NESTBOOK_COLUMNS = {
    "arm": "arm_close_ms | window_arm_close_ms | arm_ms + one lens bar (the arm bar's OPEN) | "
           "(v6transform) v6's own arm joined on the pairing key (symbol, entry_ms) [L-1.5]; "
           "kinds v6transform / relay start their bar closes there (a close event)",
    "exit": "exit_stamp_ms (ride11's stamp of record) | exit_event_ms (the books' L-R.5 stamp) "
            "| a 1h-walked ride's RESOLVED exit instant exit_instant_ms / exit_close_1h_ms, read "
            "by exit_resolved_by: '1h' -> the instant as filed (a stop at the close of the 1h "
            "child that resolves it, a warn exit at its 1h close), 'close' -> a CLOSE reason "
            "as filed at exit_close_ms (an intrabar reason resolved by 'close', or a 'close' "
            "exit off exit_close_ms, HALTs), 'parent' -> an intrabar reason at the parent "
            "bar's OPEN, a close reason at the parent's close (a missing exit_resolved_by "
            "HALTs) [the lanes pass: the warn exit and the add books' exits at their own "
            "instant, never the exit bar's 4h close] | derived: an intrabar reason (stop / tp "
            "/ target) -> the OPEN of the lens bar holding exit_close_ms, a close reason "
            "(bell* / corridor_end / warn* / invalidation* / close*) -> exit_close_ms; any "
            "other reason HALTs; THE TWIN LAW: an INTRABAR exit stamped before the close of "
            "the lens bar holding it (exit_bar_close_ms when filed — the relay, whose "
            "exit_close_ms is its 1h exit instant — else exit_close_ms; HALT unless it is "
            "that bar's close) carries the close-stamped twin 'exit_post_event' there; a "
            "stamp that IS that close (the resolving 1h child is the bar's last) has none, "
            "and a close event (a 1h warn exit) has none; a corridor_end campaign (OPEN at "
            "the pin) is stamped 'as_of_pin', never 'exit'",
    "+1R": "latch_stamp_ms (+ latch_post_event_ms) | latch_1h_ms gated by latched_1h: the "
           "resolving 1h child's close, a PARENT-decided latch (latch_1h_by 'parent' | its "
           "parent bar listed in walk_mismatch_ms) -> the parent's OPEN, an undecidable "
           "latch at a parent close HALTs; its twin by THE TWIN LAW: the close of the lens "
           "bar holding latch_1h_ms when after the stamp (the parent's close; the bar's close "
           "for a latch resolved before the bar's last 1h child; none when the resolving "
           "child is the bar's last) | derived on the lens tape by the bar-OPEN law when "
           "reached_1r is True (v6transform / lane4h), its twin at that bar's close | none",
    "harvest": "harvest_close_ms | harvest_ms + one lens bar | harvest_i on the lens tape "
               "(checked) | (v6transform) v6's own harvest close joined on the pairing key, "
               "checked per row against `harvested` and the exit stamp — gated by `harvested`; "
               "a close event inside (entry close, exit]",
    "adds / others": "add1_close_ms, add2_close_ms (close events; gated by n_adds); "
                     "ev_<name>_ms (kind <name>, as given)",
    "UNSTAMPED": "a campaign whose own record says an event happened (latched_1h / reached_1r "
                 "True, harvested True, n_adds > k) but no source above stamps it is counted, "
                 "and the door REFUSES to file (HALT naming the counts) [L-R.5 'plus the named "
                 "events']",
}
NEST_KEY = ["scale_kind", "symbol", "entry_ms", "instant_kind", "instant_ms"]

READINGS = (
    "SR-1 R1 COUNTS: a confirmed range's era is its CONFIRM bar's CLOSE [L-1.3] (the census's "
    "height_rows law); density per 100 bars = 100 x confirmed ranges in the era / bars of the "
    "lens in the era (tuning = bars with close <= 2024-06-30T23:59:59Z); ALL equals "
    "C.density_per_100 on the whole tape (asserted). The pick of record is READ from "
    "SCALE_PICKS.json (a pin) — never re-fitted; frozen 3.0 beside.",
    "SR-2 R2 TOLLS [L-R.4, L-1.1, L-1.2]: taker = fee_schedule round_trip_bps_used (10.0; "
    "== C.toll_bps_for, asserted); charter twin = 2 x (taker 5.0 + the stem's charter "
    "slippage tier A 2 / B 5 / C 10) bps round trip; maker twin = 2 x maker 2.0 = 4.0 bps round "
    "trip (maker legs carry zero slippage). A pooled height row pools per-range ratios, each "
    "struck on its own asset's toll; a pooled edge row's toll is the BINDING (max) per-asset "
    "median (census law C-f) — both the census's own functions, unchanged.",
    "SR-3 THE WORD [L-R.4]: PASS iff the height leg (n_ranges >= 30, median(ratio) >= 3.0, "
    "share(ratio < 1) <= 0.10) AND the edge leg (edge_n >= 30, edge_n_ranges >= 30, net = "
    "round(median term H20, 8) - round(toll, 8) > 0) both pass within the row's era; a FAIL "
    "with any leg under its floor (n_ranges, edge_n_ranges or edge_n < 30) reads "
    "'FAIL (provisional, n<30)'; else 'FAIL'. The census's own gate booleans are cross-checked "
    "(HALT on disagreement).",
    "SR-4 THE LENS VERDICT OF RECORD [L-R.4] = the POOLED:CLASSIC5 row, HOLDOUT era, "
    "calibrated scale (each member at its FILED pick), taker toll; 'FAIL — maker twin PASSES "
    "(…)' when taker FAILs and the maker twin of the same row PASSES. Every other row is "
    "Tier-E, its word in `would_read`, collared.",
    "SR-5 POOLED SCALE: a pooled calibrated row pools each member's run at ITS OWN filed pick "
    "(the census's pooling of per-asset runs); pick_window / scale_in_sample / "
    "stability_changed are carried per row, pooled rows name their fallback and "
    "stability-changed members [AM-4].",
    "SR-6 R3 INSTANTS [L-R.5, AM-6]: every CLOSE of the campaign's own lens from its arm "
    "close (entry close for a book without arming) through its exit stamp of record; plus the "
    "named events — arm, entry, harvest, bell, add, a close exit at their CLOSE; +1R and an "
    "intrabar exit (stop / tp) at the OPEN of their bar for the 4h books (latch bar = "
    "latch_1r_open_ms, exit = exit_event_ms: the books' UNWALKED 4h ride) — their "
    "close-stamped twins are labelled 'post-event' (instant kinds plus_1r_post_event / "
    "exit_post_event); a campaign OPEN at the pin (corridor_end) is stamped 'as_of_pin', never "
    "'exit'. Each row's stamp_law names its rule. The nest is N.nest_at(symbol, instants, "
    "scale) — per L read at the last CLOSED bar of L at or before the instant.",
    "SR-7 COINCIDENCE AT ENTRY (NEST_GRID): per lens L the category from L's two side flags — "
    "'both' (coin_top and coin_bot), 'top', 'bot', 'none'; 'NA' for 1w (no lens above). "
    "Record rule = the live L+1 boundaries (coin_*); twin = with L+1's live memory lines "
    "(coin_*_mem).",
    "SR-8 R5 BUCKETS [L-R.7]: IN_RANGE entries by pct-of-range (unclamped) decile [0,10) .. "
    "[90,100), '<0', '>=100'; not-in-range entries by state (NONE, BULL_EXP, BEAR_EXP); "
    "'__ALL__'. n, E[net R] (mean), P(win) (share net R > 0), sum R.",
    "SR-9 nest-book [L-R.5]: kinds v6transform (4h bars from the arm), lane4h (4h from the "
    "entry), relay (4h bars from the v6 arm — its stop, R, window and ride are 4h; its 1h entry "
    "instant is the named event 'entry'), scalp5m (5m bars from the entry). Columns read "
    "beyond the REGBOOK INTERFACE: " + "; ".join(f"{k} = {v}" for k, v in
                                                  NESTBOOK_COLUMNS.items()) + ".",
    "SR-10 TC10 CONTINUITY [AM-1]: TC10's census/height_toll_verdict.parquet rows (taker, "
    "10 bps) beside TC11's taker rows at 5m/4h/1d, keyed (lens, scale_kind, asset, era); "
    "POOLED:PANEL17 <-> TC10 'POOLED:ALL'. TC10's calibrated scale is ITS whole-tape pick "
    "(TC10 L2), not TC11's tuning pick; its frozen3.0 rows are the like-for-like ones.",
    "SR-11 R5 ANCHOR [L-R.7]: TC10's five-row table (control_entry_by_state.parquet, 4h, frozen "
    "3.0) is re-derived from the FILED TC10 control journal's 200 campaigns with the TC11 nest "
    "(4h state at the entry close; IN_RANGE printed as TC10's 'NEUTRAL'; |dist_signed_atr| = "
    "TC10's unsigned dist) and must equal it exactly (the build HALTs otherwise); the TC11 v6 "
    "book's own five rows ride beside (all eleven columns, both sides).",
    "SR-12 HONESTY OF THE AGGREGATED TABLES [L-R.2 SCALE-IN-SAMPLE, AM-4]: every R5_CHOP / "
    "NEST_GRID row carries lenses_read, pick_window, stability_changed_members, "
    "n_scale_in_sample, n_stability_changed and the HOLDOUT slice (n_holdout, "
    "mean_net_r_holdout, p_win_holdout, sum_net_r_holdout; era = the entry's CLOSE [L-1.3]) — "
    "the causal slice of a tuning-calibrated read, printed beside every cell.",
    "SR-13 NO VERDICT WORD OFF THE RECORD [L-1.4, L-R.4]: R2's `word` and `verdict` are "
    "printed on the seven lens-verdict-of-record rows only; every Tier-E row carries its word "
    "as `would_read`, and the census's booleans are renamed height_leg_would_pass / "
    "edge_leg_would_pass / census_would_pass (TC10's: tc10_would_read / tc10_would_pass).",
    "SR-14 THE PROBE [the nest-book self-test]: nestbook_probe/V6-PROBE is books/"
    "v6_campaigns.parquet (floats at the books table's 6 dp) in the REGBOOK schema — NOT the "
    "full-precision v6 base arm the stages file (its book_sha256 differs), never scored; the "
    "books' full-precision ΣR is read from books/build_manifest.json and printed beside.",
    "SR-15 THE LANES PASS [contract R3 'at every instant of every campaign of every card (base "
    "v6, 9/12, the lanes below)'; L-R.5, AM-6]: `lanes` runs the nest-book door (read_regbook "
    "-> instants_of -> nest_frame, both scales) over every REGISTERED scored arm that is a "
    "campaign book — P-WARN-1, P-AGE-1, P-WIN-1, P-BRK-4H, P-RELAY-1, P-ADD-BRK, P-ADD-SFP, "
    "P-TP-RNG (P-SCALP-2 is closed by R2 and files no book) — plus P-BRK-4H tierE__panel17 "
    "(the twelve: 12h / 1w NA, hence 4h / 12h / 1d coincidence NA). Each book must be the book "
    "the scorer scored (its sidecar book_sha256 == scores/SCORE_MANIFEST.json's input, HALT "
    "otherwise). Named events per L-R.5 / AM-6: arm, entry (the relay's 1h entry close: "
    "'relay_entry'), harvest, add (add1 / add2), bell, a warn exit at its 1h close, a close "
    "exit at its close — close events at their close; +1R, a stop and a TP fill are intrabar: "
    "at the OPEN of their bar or at the close of the 1h child that resolves them (the "
    "regbook's own stamp of record). THE TWIN LAW (one law for every intrabar event — +1R, "
    "a stop, a TP fill — every book, the relay included): an intrabar event whose stamp "
    "precedes the close of the 4h bar holding it carries exactly one close-stamped twin, "
    "labelled post-event, AT that close (a bar-OPEN stamp: the same bar's close; a 1h "
    "child's close: its parent 4h bar's close — exit_bar_close_ms for the relay, whose "
    "exit_close_ms is its 1h exit instant); a stamp that IS that close (the resolving 1h "
    "child is the bar's last) has none — its own instant is the close, a bar_close row "
    "through the exit stamp; close events (arm, entry, harvest, add, bell, a warn exit, a "
    "close exit) have none — a warn exit before its 4h bar's close ends the campaign there, "
    "so that close is not one of its instants. Each row's `stamp_law` names its rule from "
    "the event's own class (intrabar vs close), never from its position against "
    "exit_close_ms. An intrabar exit resolved by 'close' HALTs. A "
    "campaign OPEN at the pin -> 'as_of_pin'. Each row carries `named_event` (the event's "
    "name, 'bar_close' for a plain lens close) and the campaign's `exit_reason`. The nesting "
    "grid at ENTRY per book x scale x lens (state x coincidence frequency, outcomes by state, "
    "outcomes by coincidence: n, E[net R], P(win), sum R, the book's own net_r) is printed "
    "whole with SR-12's honesty labels, collared; declared cells: STATES4 (+ 'NA' where a "
    "member lacks the lens) x COIN_CATS (+ 'NA' where a member lacks L or L+1; 1w 'NA' only). "
    "LANES_MANIFEST.json pins, per book, the regbook bytes it stamped (the parquet's content "
    "sha — its csv — and its file sha) beside book_sha256, which covers the 16 required "
    "columns only, not the instant columns the nest reads.",
    "SR-16 R5 BY DIRECTION [the trading review D-2, research_outputs/tierc11/review/"
    "FINAL_REVIEW_2026-09-25.json: L-R.7's chop table is direction-blind as frozen, so a "
    "BULL_EXP / BEAR_EXP row mixes longs riding the expansion with shorts fading it — an "
    "alignment effect that reads as a market state]: BESIDE the R5 rows, which stay unchanged, "
    "R5_CHOP_DIRECTION prints collared Tier-E rows that DECIDE NOTHING, per scale "
    "(calibrated, frozen3.0) x lens {4h, 12h}, on the same v6 entries (direction = the book's "
    "own +1 long / -1 short). (i) 'alignment': the lens state at entry split EXP_ALIGNED "
    "(BULL_EXP for a long, BEAR_EXP for a short), EXP_COUNTER (the other expansion), "
    "IN_RANGE, NONE, and '__ALL__'. (ii) 'pct_dir_adj': the IN_RANGE entries by "
    "DIRECTION-ADJUSTED pct-of-range, unclamped (pct for a long, 100 - pct for a short, so "
    "100 is the boundary the trade must break and 0 the one behind it), in terciles "
    "[0,33.33), [33.33,66.67), [66.67,100) (exact cuts 100/3 and 200/3) plus '<0' and "
    "'>=100'. This is SR-8's half-open law, one law for both sides. The commission's "
    "text ('[66.67,100]' beside '>=100') overlaps only at exactly 100, which this law sends "
    "to '>=100' as SR-8 does; R5_CHOP.md prints how many entries sit on a cut. Columns: n "
    "(n_long / n_short beside), E[net R], P(win), sum R, and SR-12's honesty labels with "
    "the holdout slice. Partitions (the build HALTs otherwise): EXP_ALIGNED + EXP_COUNTER == "
    "R5's not-in-range BULL_EXP + BEAR_EXP; NONE == R5's not-in-range:NONE; IN_RANGE == R5's "
    "deciles + '<0' + '>=100' == the five pct_dir_adj buckets; '__ALL__' == R5's.",
)


def _halt(msg: str) -> None:
    raise SystemExit(f"HALT: {msg}")


def iso(ms) -> str:
    return C.iso(int(ms))


def clock(msg: str) -> None:                      # wall clock -> stdout only
    print(f"  [clock · stdout only] {msg}", flush=True)


# ══════════════════════════════════════════════════════════ 1 · WRITERS
def canon(df: pd.DataFrame, keys: list, round_floats: bool = True) -> pd.DataFrame:
    """C.canon (floats rounded to the census's 8 dp, total key order, HALT on a
    duplicate key) — or, for the nest tables (raw as-of reads at full precision),
    the same without the rounding."""
    if round_floats:
        return C.canon(df, keys)
    d = df.copy()
    d.attrs = {}
    d.columns = [str(c) for c in d.columns]
    dup = int(d.duplicated(subset=keys).sum())
    if dup:
        _halt(f"(F-KEY) key {keys} is NOT unique — {dup} duplicate row(s)")
    return d.sort_values(keys, kind="mergesort").reset_index(drop=True)


def put_table(df: pd.DataFrame, name: str, keys: list, out: Path, W: dict, K: dict,
              round_floats: bool = True, sub: str = "") -> pd.DataFrame:
    """canon -> an atomic parquet through pandas on a PATH STRING (AM-2) -> the
    content sha (C.content_sha, the csv) recorded in W, the key in K."""
    d = canon(df, keys, round_floats)
    root = out / sub if sub else out
    root.mkdir(parents=True, exist_ok=True)
    p = root / f"{name}.parquet"
    tmp = p.with_name(p.name + ".tmp")
    d.to_parquet(str(tmp), index=False)
    os.replace(tmp, p)
    rel = f"{sub}/{name}" if sub else name
    W[rel] = C.content_sha(d)
    K[rel] = list(keys)
    return d


def put_text(text: str, path: Path) -> bytes:
    b = text.encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(b)
    os.replace(tmp, path)
    return b


def put_json(obj, path: Path) -> bytes:
    return put_text(json.dumps(obj, indent=1, sort_keys=True, default=str) + "\n", path)


def read_parquet(p: Path) -> pd.DataFrame:
    return pd.read_parquet(str(p))


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ══════════════════════════════════════════════════════════ 2 · INPUTS, VERIFIED
def picks_record() -> dict:
    """SCALE_PICKS.json (the pins), verified against its provenance sidecar."""
    rec = N.picks()
    pb = N.PICKS_PATH.read_bytes()
    src = json.loads(N.SOURCES_PATH.read_text(encoding="utf-8"))
    if src.get("annotates_sha256") != sha_bytes(pb):
        _halt("SCALE_PICKS_SOURCES.json does not annotate the filed SCALE_PICKS.json bytes")
    return rec


def books_campaigns() -> dict:
    """The two campaign tables (+ v6's journal for mfe_r), each content sha verified
    against books/build_manifest.json before it is read further."""
    man = json.loads((BOOK_DIR / "build_manifest.json").read_text(encoding="utf-8"))
    out = {}
    for name in ("v6_campaigns", "trg912_campaigns", "v6_journal"):
        d = read_parquet(BOOK_DIR / f"{name}.parquet")
        got = E.TB._content_sha(d)
        if got != man["sha"][name]:
            _halt(f"books/{name}.parquet content sha {got[:12]}… != the books manifest's "
                  f"{man['sha'][name][:12]}… — the input moved")
        out[name] = d
    out["_manifest"] = man
    return out


def tc10_table(rel: str) -> pd.DataFrame:
    return read_parquet(E.tc10_record(rel))


# ══════════════════════════════════════════════════════════ 3 · TOLLS AND THE WORD
def toll_bps(stem: str, toll: str) -> float:
    f = E.fees()[stem]
    if toll == "taker":
        bps = float(f["taker_round_trip_bps"])
        if bps != float(C.toll_bps_for(stem)[0]):
            _halt(f"{stem}: fee_schedule taker {bps} != C.toll_bps_for")
        return bps
    if toll == "maker":
        return 2.0 * float(f["maker_bps_side"]) + 2.0 * float(f["maker_slippage_bps_side"])
    if toll == "charter":
        return 2.0 * (float(f["taker_bps_side"]) + float(f["slippage_bps_side"]))
    _halt(f"unknown toll {toll!r}")


def edge_net(median_term: float, toll_atr: float) -> float:
    """the census's NET: round(median, 8) - round(toll, 8) (C._edge_stats)."""
    if not (np.isfinite(median_term) and np.isfinite(toll_atr)):
        return float("nan")
    return float(np.round(float(median_term), C.ROUND_ND) - np.round(float(toll_atr), C.ROUND_ND))


def legs_of(n_ranges, ratio_median, share_lt1, edge_n, edge_n_ranges, net) -> tuple:
    """(height_pass, edge_pass, under_floor) by the census's pinned thresholds,
    read at CALL time."""
    n_ranges, edge_n, edge_n_ranges = int(n_ranges), int(edge_n), int(edge_n_ranges)
    h = bool(n_ranges >= C.HEIGHT_MIN_N_RANGES and np.isfinite(ratio_median)
             and ratio_median >= C.HEIGHT_RATIO_MIN and np.isfinite(share_lt1)
             and share_lt1 <= C.INFEASIBLE_MAX_SHARE)
    e = bool(edge_n >= C.EDGE_MIN_N_BARS and edge_n_ranges >= C.EDGE_MIN_N_RANGES
             and np.isfinite(net) and net > 0)
    under = bool(n_ranges < C.HEIGHT_MIN_N_RANGES or edge_n_ranges < C.EDGE_MIN_N_RANGES
                 or edge_n < C.EDGE_MIN_N_BARS)
    return h, e, under


def word_of(n_ranges, ratio_median, share_lt1, edge_n, edge_n_ranges, net) -> str:
    h, e, under = legs_of(n_ranges, ratio_median, share_lt1, edge_n, edge_n_ranges, net)
    if h and e:
        return WORD_PASS
    return WORD_PROV if under else WORD_FAIL


def record_verdict(word_taker: str, word_maker: str) -> str:
    if word_taker == WORD_PASS:
        return WORD_PASS
    if word_maker == WORD_PASS:
        return REOPEN
    return word_taker


# ══════════════════════════════════════════════════════════ 4 · R1 + R2 (one pass per lens)
def _members(lens: str) -> tuple:
    return CLASSIC5 + (UNSEEN12 if lens in UNSEEN_LENSES else ())


def _era_bars(tape) -> dict:
    t = N.era_cut11(tape)
    return {"ALL": int(tape.n), "tuning": int(t), "holdout": int(tape.n - t)}


def _confirmed_by_era(tape, macro) -> dict:
    ci = np.array([int(r.confirm_i) for r in macro["ranges"] if int(r.confirm_i) >= 0],
                  dtype=np.int64)
    era = E.era_of(tape.t0[ci] + tape.step) if len(ci) else np.array([], dtype=object)
    return {"ALL": int(len(ci)), "tuning": int((era == "tuning").sum()),
            "holdout": int((era == "holdout").sum())}


def _height_frame(parts: list, kind: str) -> pd.DataFrame:
    """Concatenate per-asset height rows; an empty panel becomes one all-NaN
    dummy row so C.height_grid files n_ranges 0 for every era (its isfinite
    filter drops the dummy) instead of filing nothing."""
    parts = [p for p in parts if len(p)]
    if parts:
        return pd.concat(parts, ignore_index=True)
    return pd.DataFrame({"ratio": [np.nan], "toll_atr": [np.nan], "height_atr": [np.nan],
                         "ratio_final": [np.nan], "scale_kind": [kind], "era": ["__none__"]})


def _scale_labels(stem: str, lens: str, kind: str) -> dict:
    lab = N.scale_label(stem, lens, kind)
    return {"pick_window": lab["pick_window"], "fallback": bool(lab["fallback"]),
            "stability_changed": lab["stability_changed"]}


def _in_sample_text(kind: str, fallback: bool, era: str) -> str:
    if kind == "frozen3.0":
        return "never (frozen 3.0 is fully causal)"
    if fallback:
        return "IN-SAMPLE at every instant (whole-tape fallback pick)"
    return {"tuning": "IN-SAMPLE (tuning-era bars; the tuning pick saw them)",
            "holdout": "OUT-OF-SAMPLE (holdout; the causal slice of a tuning pick)",
            "ALL": "MIXED (tuning bars in-sample, holdout bars out-of-sample)"}[era]


def lens_pass(lens: str) -> dict:
    """ONE LENS: every member asset x scale — the machine at the filed scale, the
    census walk (replay == the machine's breakout-die log, HALT otherwise), R1's
    counts, and per toll the census's height rows and edge arrays."""
    members = _members(lens)
    R1, H, A, LAB = {}, {}, {}, {}
    for s in members:
        tape = N.load11(s, lens)
        bars = _era_bars(tape)
        for kind in SCALE_KINDS:
            sc = N.scale_of(s, lens, kind)
            m = C.run_scale(tape, sc)["macro"]
            w = C._r34_walk(tape, m, RC.macro_pins(sc))
            truth = [(e["i"], e["rid"], e["side"], e["by"], e["closes"])
                     for e in m["events"] if e["event"] == "breakout-die"]
            mine = [(e["die_i"], e["rid"], e["side"], e["die_by"], e["max_closes"])
                    for e in w["episodes"] if e["end_kind"] == "die"]
            if truth != mine:
                _halt(f"{s} {lens} {kind}: the census walk is not the machine's breakout-die "
                      f"log ({len(mine)} vs {len(truth)}) [F-C10-ACC-REPLAY law]")
            cnt = _confirmed_by_era(tape, m)
            dens_all = 100.0 * cnt["ALL"] / bars["ALL"]
            if abs(dens_all - C.density_per_100(m)) > 0.0:
                _halt(f"{s} {lens} {kind}: ALL density {dens_all} != C.density_per_100")
            R1[(s, kind)] = {"counts": cnt, "bars": bars, "scale": float(sc)}
            LAB[(s, kind)] = _scale_labels(s, lens, kind)
            aid = PANEL17.index(s)
            base = None
            for toll in TOLLS:
                bps = toll_bps(s, toll)
                H[(s, kind, toll)] = C.height_rows(w, tape, s, lens, kind, bps)
                if base is None:
                    base = C.edge_arrays(tape, w, bps, aid=aid)
                    for k in ("term_H100", "live_H100"):     # the gate reads H20 only
                        base.pop(k, None)
                    A[(s, kind, toll)] = base
                else:
                    A[(s, kind, toll)] = _twin_edge(base, tape, w, bps)
    return {"R1": R1, "H": H, "A": A, "LAB": LAB, "members": members}


def _twin_edge(base: dict, tape, w: dict, bps: float) -> dict:
    """A TWIN toll's edge arrays: the record's per-bar ledger (the same bars, the
    same terms) with the toll re-struck at the twin's bps (C._toll_at, the census's
    own) — read at CALL time (F-FEAS plants it)."""
    return dict(base, toll=C._toll_at(tape, w["ir_t"], bps)) if base.get("n") else base


def r1_rows(lens: str, P: dict, rec: dict) -> list[dict]:
    by = rec["_by_cell"]
    rows = []
    for s in P["members"]:
        c = by[(s, lens)]
        cal, fz = P["R1"][(s, "calibrated")], P["R1"][(s, "frozen3.0")]
        if cal["scale"] != float(c["pick_of_record"]):
            _halt(f"{s} {lens}: the scale ridden {cal['scale']} is not the filed pick")
        st = c["stable_first_half_vs_tuning"]
        r = {"cell": f"{s}|{lens}", "asset": s, "lens": lens,
             "panel": "CLASSIC5" if s in CLASSIC5 else "UNSEEN12",
             "n_bars": cal["bars"]["ALL"], "n_bars_tuning": cal["bars"]["tuning"],
             "n_bars_holdout": cal["bars"]["holdout"],
             "first_bar_open": c["first_bar_open"], "last_bar_close": c["last_bar_close"],
             "pick_of_record": float(c["pick_of_record"]), "pick_window": c["pick_window"],
             "label": c["label"],
             "calibrated_in_sample": N.IN_SAMPLE_TEXT["tuning" if c["pick_window"] == "tuning"
                                                      else "whole"],
             "in_sample_tuning": bool(c["in_sample_tuning"]),
             "in_sample_holdout": bool(c["in_sample_holdout"]),
             "tuning_pick": (np.nan if c["tuning_pick"] is None else float(c["tuning_pick"])),
             "whole_tape_pick": float(c["whole_tape_pick"]),
             "first_half_pick": (np.nan if c["first_half_pick"] is None
                                 else float(c["first_half_pick"])),
             "frozen_scale": float(c["frozen_scale"]),
             "stability_changed": (None if st is None else (not bool(st))),
             "stability_printed_L_R_2": bool(s in CLASSIC5 and lens in N.STABILITY_LENSES),
             "pick_at_grid_edge": bool(c["pick_at_grid_edge"]),
             "target_bracketed": bool(c["target_bracketed"]),
             "density_at_pick_filed_per_100": float(c["density_at_pick_per_100"])}
        for era in ERAS:
            nb = cal["bars"][era]
            r[f"n_confirmed_{era}"] = cal["counts"][era]
            r[f"density_per_100_{era}"] = (100.0 * cal["counts"][era] / nb) if nb else np.nan
            r[f"n_confirmed_frozen_{era}"] = fz["counts"][era]
            r[f"density_frozen_per_100_{era}"] = (100.0 * fz["counts"][era] / nb) if nb else np.nan
        win = "tuning" if c["pick_window"] == "tuning" else "ALL"
        r["density_window_matches_filed"] = bool(
            round(r[f"density_per_100_{win}"], 8) == round(float(c["density_at_pick_per_100"]), 8))
        rows.append(r)
    return rows


def r2_rows(lens: str, P: dict, tc10: pd.DataFrame) -> list[dict]:
    fz = E.fees()
    panels = [(f"ASSET:{s}", (s,)) for s in P["members"]]
    for pname, (mem, lenses) in POOLS.items():
        if lens in lenses:
            panels.append((pname, tuple(mem)))
    rows = []
    for pname, mem in panels:
        pooled = len(mem) > 1
        for kind in SCALE_KINDS:
            labs = {s: P["LAB"][(s, kind)] for s in mem}
            fb = [s for s in mem if labs[s]["fallback"]]
            chg = [s for s in mem if labs[s]["stability_changed"] is True]
            if pooled:
                pw = sorted({labs[s]["pick_window"] for s in mem})
                pick_window = pw[0] if len(pw) == 1 else "MIXED: " + " / ".join(pw)
                stab = bool(chg) if any(labs[s]["stability_changed"] is not None
                                        for s in mem) else None
            else:
                pick_window = labs[mem[0]]["pick_window"]
                stab = labs[mem[0]]["stability_changed"]
            for toll in TOLLS:
                hl = _height_frame([P["H"][(s, kind, toll)] for s in mem], kind)
                name = pname if pooled else mem[0]
                hg = C.height_grid(hl, name, lens)
                hdec = {(h["scale_kind"], h["era"]): h for h in hg}
                Ai = (C._edge_cat([P["A"][(s, kind, toll)] for s in mem]) if pooled
                      else P["A"][(mem[0], kind, toll)])
                eg = {(name, kind, era): C.edge_gate(Ai, pooled, era) for era in ERAS}
                vr = C.verdict_rows(hg, eg, lens)
                if sorted(v["era"] for v in vr) != sorted(ERAS):
                    _halt(f"{pname} {lens} {kind} {toll}: verdict rows {[v['era'] for v in vr]}")
                bpsv = [toll_bps(s, toll) for s in mem]
                for v in vr:
                    era = v["era"]
                    net = edge_net(v["edge_median_term_h20"], v["edge_toll_atr"])
                    if not (np.isnan(net) and np.isnan(v["edge_net_h20"])) and \
                            net != v["edge_net_h20"]:
                        _halt(f"{pname} {lens} {era} {kind} {toll}: net {net} != census "
                              f"{v['edge_net_h20']}")
                    h_ok, e_ok, under = legs_of(v["n_ranges"], v["ratio_median"],
                                                v["share_ratio_lt_1"], v["edge_n"],
                                                v["edge_n_ranges"], net)
                    if h_ok != bool(v["gate_height_pass"]) or e_ok != bool(v["gate_edge_fade_pass"]) \
                            or bool(v["provisional"]) != under:
                        _halt(f"{pname} {lens} {era} {kind} {toll}: the word law disagrees with "
                              f"the census gates ({h_ok}/{v['gate_height_pass']}, {e_ok}/"
                              f"{v['gate_edge_fade_pass']}, {under}/{v['provisional']})")
                    w = word_of(v["n_ranges"], v["ratio_median"], v["share_ratio_lt_1"],
                                v["edge_n"], v["edge_n_ranges"], net)
                    if (w == WORD_PASS) != bool(v["verdict_pass"]):
                        _halt(f"{pname} {lens} {era}: word {w} vs census verdict_pass")
                    txt = sorted({_in_sample_text(kind, labs[s]["fallback"], era) for s in mem})
                    hrow = hdec[(kind, era)]
                    if any(float(hrow[f"ratio_d{q}"]) != float(v[f"ratio_d{q}"]) and not
                           (np.isnan(hrow[f"ratio_d{q}"]) and np.isnan(v[f"ratio_d{q}"]))
                           for q in (1, 5, 9)) or int(hrow["n_ranges"]) != int(v["n_ranges"]):
                        _halt(f"{pname} {lens} {era} {kind} {toll}: the height grid row is not "
                              f"the verdict row's")
                    r = {"cell": f"{pname}|{lens}|{era}|{kind}|{toll}",
                         "panel": pname, "lens": lens, "era": era, "scale_kind": kind,
                         "toll": toll, "pooled": pooled, "n_members": len(mem),
                         "members": ",".join(mem),
                         "scale_mult": (np.nan if pooled else P["R1"][(mem[0], kind)]["scale"]),
                         "toll_bps_rt_min": float(min(bpsv)), "toll_bps_rt_max": float(max(bpsv)),
                         "n_ranges": int(v["n_ranges"]), "ratio_median": v["ratio_median"],
                         **{f"ratio_d{q}": float(hrow[f"ratio_d{q}"]) for q in RATIO_DECILES},
                         "share_ratio_lt_1": v["share_ratio_lt_1"],
                         "height_atr_median": v["height_atr_median"],
                         "toll_atr_median": v["toll_atr_median"],
                         "height_leg_would_pass": bool(v["gate_height_pass"]),
                         "edge_n": int(v["edge_n"]), "edge_n_ranges": int(v["edge_n_ranges"]),
                         "edge_median_term_h20": v["edge_median_term_h20"],
                         "edge_toll_atr": v["edge_toll_atr"], "edge_net_h20": v["edge_net_h20"],
                         "edge_hit_rate_net": v["edge_hit_rate_net"],
                         "edge_leg_would_pass": bool(v["gate_edge_fade_pass"]),
                         "under_floor": bool(under),
                         "fail_reasons": "; ".join(x for x in (
                             v["gate_height_fail_reason"], v["gate_edge_fade_fail_reason"]) if x),
                         "census_would_pass": bool(v["verdict_pass"]),
                         "word": w, "is_lens_verdict_of_record": False,
                         "verdict": None, "would_read": None,
                         "pick_window": pick_window,
                         "scale_in_sample": (txt[0] if len(txt) == 1
                                             else "MIXED: " + " | ".join(txt)),
                         "fallback_members": ",".join(fb),
                         "stability_changed": stab,
                         "stability_changed_members": ",".join(chg)}
                    r.update(COLLAR)
                    rows.append(r)
    # TC10 continuity [AM-1]
    t10 = {}
    if lens in TC10_LENSES:
        z = tc10[tc10["lens"] == lens]
        t10 = {(str(a), str(k), str(e)): g for (a, k, e), g in
               z.groupby(["asset", "scale_kind", "era"], sort=True)}
    for r in rows:
        key = (TC10_POOL_NAME.get(r["panel"], r["panel"].replace("ASSET:", "")),
               r["scale_kind"], r["era"])
        g = t10.get(key) if r["toll"] == "taker" else None
        if g is not None and len(g) == 1:
            q = g.iloc[0]
            r["tc10_would_read"] = word_of(q["n_ranges"], q["ratio_median"],
                                           q["share_ratio_lt_1"], q["edge_n"], q["edge_n_ranges"],
                                           edge_net(q["edge_median_term_h20"],
                                                    q["edge_toll_atr"]))
            r["tc10_would_pass"] = bool(q["verdict_pass"])
            r["tc10_n_ranges"] = int(q["n_ranges"])
            r["tc10_ratio_median"] = float(q["ratio_median"])
            r["tc10_edge_n"] = int(q["edge_n"])
            r["tc10_edge_n_ranges"] = int(q["edge_n_ranges"])
            r["tc10_edge_net_h20"] = float(q["edge_net_h20"])
            r["tc10_note"] = ("TC10 as of 2026-09-21T16:00Z; TC10 calibrated = its whole-tape "
                              "pick (TC10 L2), not TC11's tuning pick" if r["scale_kind"] ==
                              "calibrated" else "TC10 as of 2026-09-21T16:00Z; frozen 3.0 "
                              "like-for-like")
        else:
            r["tc10_would_read"] = None
            r["tc10_would_pass"] = None
            r["tc10_n_ranges"] = None
            r["tc10_ratio_median"] = np.nan
            r["tc10_edge_n"] = None
            r["tc10_edge_n_ranges"] = None
            r["tc10_edge_net_h20"] = np.nan
            r["tc10_note"] = ("not measured by TC10 (lens / toll / panel)" if r["toll"] != "taker"
                              or lens not in TC10_LENSES else "no TC10 row for this key")
    return rows


R1_INT = ("n_bars", "n_bars_tuning", "n_bars_holdout") + tuple(
    f"n_confirmed_{e}" for e in ERAS) + tuple(f"n_confirmed_frozen_{e}" for e in ERAS)
R2_NULLABLE_INT = ("tc10_n_ranges", "tc10_edge_n", "tc10_edge_n_ranges")


def compute_r1_r2() -> tuple[pd.DataFrame, pd.DataFrame]:
    rec = picks_record()
    tc10 = tc10_table(TC10_VERDICT_REL)
    r1, r2 = [], []
    for lens in LENSES11:
        t0 = time.perf_counter()
        P = lens_pass(lens)
        r1 += r1_rows(lens, P, rec)
        r2 += r2_rows(lens, P, tc10)
        del P
        clock(f"R1/R2 lens {lens}: {time.perf_counter() - t0:.1f}s")
    R1 = pd.DataFrame(r1)
    for k, v in {**COLLAR, **AS_OF}.items():
        R1[k] = v
    R1["stability_changed"] = pd.array(R1["stability_changed"].tolist(), dtype="boolean")
    R2 = pd.DataFrame(r2)
    for k, v in AS_OF.items():
        R2[k] = v
    for c in ("tc10_would_pass", "stability_changed"):
        R2[c] = pd.array(R2[c].tolist(), dtype="boolean")
    for c in R2_NULLABLE_INT:
        R2[c] = pd.array(R2[c].tolist(), dtype="Int64")
    return R1, R2


def finalize_r2(R2: pd.DataFrame) -> pd.DataFrame:
    """THE WORDS, FROM THE PRINTED COLUMNS [L-R.4, SR-3, SR-4] — every row's word
    (and under_floor) re-struck by word_of on the row's own printed columns (the
    census thresholds read at CALL time); the lens verdict of record marked on
    exactly the RECORD cell per lens, its verdict = the taker word with the maker
    twin's word of the SAME (panel, lens, era, scale) beside; every other row
    Tier-E, collared, its word in `would_read`.  RECORD is read at call time."""
    d = R2.copy()
    nets = [edge_net(a, b) for a, b in zip(d["edge_median_term_h20"], d["edge_toll_atr"])]
    legs = [legs_of(a, b, c, e, f, g) for a, b, c, e, f, g in
            zip(d["n_ranges"], d["ratio_median"], d["share_ratio_lt_1"], d["edge_n"],
                d["edge_n_ranges"], nets)]
    d["under_floor"] = [x[2] for x in legs]
    words = [word_of(a, b, c, e, f, g) for a, b, c, e, f, g in
             zip(d["n_ranges"], d["ratio_median"], d["share_ratio_lt_1"], d["edge_n"],
                 d["edge_n_ranges"], nets)]
    rec = ((d["panel"] == RECORD["panel"]) & (d["era"] == RECORD["era"])
           & (d["scale_kind"] == RECORD["scale_kind"]) & (d["toll"] == RECORD["toll"]))
    d["is_lens_verdict_of_record"] = rec.to_numpy(bool)
    wk = {(p, l, e, k, t): w for p, l, e, k, t, w in
          zip(d["panel"], d["lens"], d["era"], d["scale_kind"], d["toll"], words)}
    d["verdict"] = [record_verdict(w, wk[(p, l, e, k, "maker")]) if r else None
                    for p, l, e, k, w, r in zip(d["panel"], d["lens"], d["era"],
                                                d["scale_kind"], words, rec)]
    # [L-1.4, L-R.4] the WORD sits only on the record rows; a Tier-E row carries its
    # word as `would_read` and no verdict word (verifier MINOR-1)
    d["word"] = [w if r else None for w, r in zip(words, rec)]
    d["would_read"] = [None if r else w for w, r in zip(words, rec)]
    for k, v in COLLAR.items():
        d[k] = [RECORD_COLLAR[k] if r else v for r in rec]
    return d


def word_any(R2: pd.DataFrame) -> pd.Series:
    """The row's own word wherever it is printed (record: `word`; Tier-E:
    `would_read`) — for the stage's internal lookups only."""
    return R2["word"].where(R2["word"].notna(), R2["would_read"])


def lens_verdicts(R2: pd.DataFrame) -> dict:
    out = {}
    for lens in LENSES11:
        z = R2[(R2["lens"] == lens) & (R2["panel"] == RECORD["panel"])
               & (R2["era"] == RECORD["era"]) & (R2["scale_kind"] == RECORD["scale_kind"])]
        rec = z[z["toll"] == "taker"]
        if len(rec) != 1 or not bool(rec["is_lens_verdict_of_record"].iloc[0]):
            _halt(f"R2: lens {lens} has {len(rec)} record rows")
        r = rec.iloc[0]
        wm = z[z["toll"] == "maker"]["would_read"].iloc[0]         # Tier-E twins' words
        wc = z[z["toll"] == "charter"]["would_read"].iloc[0]
        tw = R2[(R2["lens"] == lens) & (R2["panel"] == RECORD["panel"])
                & (R2["scale_kind"] == RECORD["scale_kind"]) & (R2["toll"] == "taker")]
        tw = tw.assign(word=word_any(tw))
        out[lens] = {
            "verdict": r["verdict"], "word": r["word"], "provisional": bool(r["under_floor"]),
            "maker_twin": wm, "charter_twin": wc,
            "n_ranges": int(r["n_ranges"]), "ratio_median": float(r["ratio_median"]),
            "share_ratio_lt_1": float(r["share_ratio_lt_1"]),
            "toll": "taker", "toll_bps_rt": float(r["toll_bps_rt_max"]),
            "edge_n": int(r["edge_n"]), "edge_n_ranges": int(r["edge_n_ranges"]),
            "edge_median_term_h20": float(r["edge_median_term_h20"]),
            "edge_toll_atr": float(r["edge_toll_atr"]),
            "edge_net_h20": float(r["edge_net_h20"]),
            "era": RECORD["era"], "scale": RECORD["scale_kind"], "pool": RECORD["panel"],
            "members": r["members"], "pick_window": r["pick_window"],
            "scale_in_sample": r["scale_in_sample"],
            "fallback_members": r["fallback_members"],
            "stability_changed_members": r["stability_changed_members"],
            "tier_e_tuning_word": tw[tw["era"] == "tuning"]["word"].iloc[0],
            "tier_e_all_word": tw[tw["era"] == "ALL"]["word"].iloc[0],
            "tier_e_note": "the tuning / ALL words are Tier-E twins: 'a SELECTION, not a result'",
        }
    return out


# ══════════════════════════════════════════════════════════ 5 · R3 THE NEST ON THE BOOKS
def regframe_from_campaigns(camp: pd.DataFrame) -> pd.DataFrame:
    """A 4h book's campaign table in the REGBOOK schema (+ the nest-book event
    columns): the stamps of record of an UNWALKED 4h ride — +1R at its latch
    bar's OPEN (latch_1r_open_ms), a stop exit at the exit bar's OPEN
    (exit_event_ms 'intrabar_open'), a bell / corridor_end exit at the close —
    their close-stamped twins as post-event.  INTRABAR_STAMP is read at call time."""
    fz = E.fees()
    d = pd.DataFrame({
        "symbol": camp["symbol"].astype(str), "entry_ms": camp["entry_ms"].astype(np.int64),
        "entry_close_ms": camp["entry_close_ms"].astype(np.int64),
        "direction": camp["direction"].astype(np.int8),
        "entry_px": camp["entry_px"].astype(float), "stop_px": camp["stop_px"].astype(float),
        "r_dist": camp["r_dist"].astype(float),
        "exit_close_ms": camp["exit_close_ms"].astype(np.int64),
        "exit_reason": camp["exit_reason"].astype(str),
        "net_r": camp["net_r"].astype(float), "gross_r": camp["gross_r"].astype(float),
        "fee_r": camp["fee_r"].astype(float), "funding_r": camp["funding_r"].astype(float)})
    slip = d["symbol"].map(lambda s: fz[s]["slippage_bps_side"]).astype(float)
    side = d["symbol"].map(lambda s: fz[s]["taker_bps_side"]).astype(float)
    d["haircut_net_r"] = d["net_r"] - d["fee_r"] * slip / side
    d["era"] = E.era_of(d["entry_close_ms"].to_numpy(np.int64)).astype(str)
    d["lane"] = camp["lane"].astype(str)
    d["arm_close_ms"] = camp["arm_close_ms"].astype(np.int64)
    lat = camp["latch_1r_open_ms"].astype("Int64")
    intr = camp["exit_event_stamp"].astype(str) == "intrabar_open"
    ev = camp["exit_event_ms"].astype(np.int64)
    if INTRABAR_STAMP == "bar_open":
        d["latch_stamp_ms"] = lat
        d["exit_stamp_ms"] = ev
    else:                                       # the close-stamping SABOTAGE
        d["latch_stamp_ms"] = lat + MS_4H
        d["exit_stamp_ms"] = np.where(intr, ev + MS_4H, ev).astype(np.int64)
    d["latch_post_event_ms"] = lat + MS_4H
    d["harvest_close_ms"] = camp["harvest_close_ms"].astype("Int64")
    return d


def regbook_sha(df: pd.DataFrame) -> str:
    """book_sha256 of the REGBOOK INTERFACE: sha256 of a canonical CSV of the
    required columns sorted by (symbol, entry_close_ms), floats at repr precision."""
    d = df[list(REGBOOK_REQUIRED)].sort_values(["symbol", "entry_close_ms"],
                                               kind="mergesort").reset_index(drop=True)
    for c in REGBOOK_FLOATS:                       # repr = the shortest round-trip form
        d[c] = [repr(float(x)) for x in d[c].to_numpy(float)]
    for c in ("entry_ms", "entry_close_ms", "exit_close_ms", "direction"):
        d[c] = d[c].astype(np.int64)
    return sha_bytes(d.to_csv(index=False, lineterminator="\n").encode("utf-8"))


def _v6_campaigns() -> pd.DataFrame:
    return read_parquet(BOOK_DIR / "v6_campaigns.parquet")


def _v6_arm_join(reg: pd.DataFrame) -> pd.Series:
    """kind v6transform without an arm column: the arm is v6's own (L-1.5: a paired
    transform keeps v6's arm, entry, stop and R), joined on the pairing key
    (symbol, entry_ms) from books/v6_campaigns.parquet; HALTS on any key v6 lacks."""
    v6 = _v6_campaigns()[["symbol", "entry_ms", "arm_close_ms"]]
    j = reg[["symbol", "entry_ms"]].merge(v6, on=["symbol", "entry_ms"], how="left",
                                          validate="m:1")
    if j["arm_close_ms"].isna().any():
        _halt(f"nest-book v6transform: {int(j['arm_close_ms'].isna().sum())} campaign(s) are "
              f"not v6 keys and carry no arm column")
    return pd.Series(j["arm_close_ms"].to_numpy(np.int64), index=reg.index)


def _v6_harvest_join(reg: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """kind v6transform without a harvest column: v6's own harvest close joined on the
    pairing key [L-1.5: a paired transform IS v6's campaign until its rule acts, so a
    harvest it records is v6's] -> (v6 harvest close ms or NA, the row is a v6 key).
    CHECKED per row in instants_of against the row's own `harvested` and exit stamp
    (HALT when the join does not hold)."""
    v6 = _v6_campaigns()[["symbol", "entry_ms", "harvested", "harvest_close_ms"]].rename(
        columns={"harvested": "_v6h", "harvest_close_ms": "_v6hc"})
    j = reg[["symbol", "entry_ms"]].merge(v6, on=["symbol", "entry_ms"], how="left",
                                          validate="m:1")
    keyed = j["_v6h"].notna().to_numpy(bool)
    v6h = j["_v6h"].astype("boolean").fillna(False).to_numpy(bool)
    hc = j["_v6hc"].astype("Int64").where(v6h)
    return (pd.Series(hc.to_numpy(), index=reg.index, dtype="Int64"),
            pd.Series(keyed, index=reg.index))


def _col(reg: pd.DataFrame, name: str) -> pd.Series:
    return reg[name].astype("Int64")


def _flag(reg: pd.DataFrame, name: str) -> np.ndarray:
    return reg[name].astype("boolean").fillna(False).to_numpy(bool)


def _true(x) -> bool:
    return (not pd.isna(x)) and bool(x)


def _int_set(x) -> set:
    """walk_mismatch_ms of one row (a list / array / text of ms / '' / NA) -> set."""
    if x is None:
        return set()
    if isinstance(x, (list, tuple, np.ndarray)):
        return {int(v) for v in x if not pd.isna(v)}
    if isinstance(x, str):
        return {int(t) for t in re.findall(r"-?\d+", x)}
    return set() if pd.isna(x) else {int(x)}


def _parent_latch(reg: pd.DataFrame, lat: pd.Series, step: int) -> np.ndarray:
    """[L-R.5, AM-6; verifier MINOR-8] which latch_1h_ms rows are PARENT-decided (a
    walk-mismatch bar: latch_1h_ms is then the parent's CLOSE, the post-event twin,
    and the stamp of record is the parent bar's OPEN).  Sources, first present wins:
    latch_1h_by ('parent'); walk_mismatch_ms (the latch's parent bar open listed);
    n_walk_mismatch (0 -> the child's close for sure).  A latch at a parent close
    that none of them can decide HALTS — never guessed."""
    cols = set(reg.columns)
    has = lat.notna().to_numpy(bool)
    lv = lat.fillna(0).astype(np.int64).to_numpy()
    at_close = has & (lv % step == 0)
    if "latch_1h_by" in cols:
        return has & (reg["latch_1h_by"].astype(str).to_numpy() == "parent")
    if "walk_mismatch_ms" in cols:
        return np.array([bool(a) and (int(v) - step) in _int_set(m)
                         for a, v, m in zip(at_close, lv, reg["walk_mismatch_ms"])], dtype=bool)
    if "n_walk_mismatch" in cols:
        amb = at_close & (reg["n_walk_mismatch"].fillna(0).astype(np.int64).to_numpy() > 0)
    else:
        amb = at_close
    if amb.any():
        _halt(f"nest-book: {int(amb.sum())} latch_1h_ms value(s) sit at a {step // 3_600_000}h "
              f"close on a campaign with walk-mismatch bars (or no mismatch record) and the "
              f"regbook carries no latch_stamp_ms / latch_1h_by / walk_mismatch_ms — a "
              f"parent-decided latch cannot be told from a 1h-resolved one [L-R.5, AM-6]")
    return np.zeros(len(reg), dtype=bool)


LAW_CLOSE = "close"
LAW_P1R_STAMP = "intrabar — the regbook's stamp of record as filed (latch_stamp_ms) [L-R.5, AM-6]"
LAW_P1R_CHILD = ("intrabar — the close of the resolving 1h child (latch_1h_ms; the 1h walk) "
                 "[L-R.5]")
LAW_P1R_PARENT = ("intrabar — the parent 4h bar's OPEN (latch_1h_ms − 4h: parent-decided on a "
                  "walk-mismatch bar) [L-R.5, AM-6]")
LAW_P1R_DERIVED = ("intrabar — the OPEN of the first {lens} bar after the entry reaching +1R "
                   "(derived on the lens tape: the unwalked bar-OPEN law) [L-R.5]")
LAW_P1R_BOOKS = ("intrabar — the OPEN of its 4h bar (the books' UNWALKED 4h ride: "
                 "latch_1r_open_ms) [L-R.5]")
LAW_EXIT_BOOKS = ("intrabar — the OPEN of its 4h bar (the books' UNWALKED 4h ride: "
                  "exit_event_ms) [L-R.5]")
LAW_EXIT_CHILD = ("intrabar — the close of the resolving 1h child ({col}; exit_resolved_by "
                  "'1h') [L-R.5]")
LAW_EXIT_PARENT = ("intrabar — the parent {lens} bar's OPEN ({col} − {lens}: exit_resolved_by "
                   "'parent') [L-R.5, AM-6]")
LAW_TWIN = "post-event twin (close)"
LAW_PIN = ("close — the campaign is OPEN at the pin (corridor_end): the as-of instant, NOT an "
           "exit [verifier MINOR-11]")


def resolve_events(reg: pd.DataFrame, kind: str) -> tuple[pd.DataFrame, dict]:
    """THE EVENT SOURCES of one regbook arm [SR-9], resolved ONCE per book (the
    first column present wins; each choice is named in the sidecar):
      arm      arm_close_ms | window_arm_close_ms | arm_ms + one lens bar (the arm
               bar's OPEN + step) | v6transform: v6's own arm by the pairing key
      exit     exit_stamp_ms | exit_event_ms (the books' L-R.5 stamp) | derived per
               row (_exit_stamp)
      +1R      latch_stamp_ms | latch_1h_ms (gated by latched_1h; a PARENT-decided
               latch -> the parent's OPEN, its close the twin: _parent_latch) |
               derived on the lens tape by the bar-OPEN law when reached_1r is True
               (kinds v6transform / lane4h, entry at a lens close) | none
      +1R twin latch_post_event_ms | the parent close (parent-decided) | the derived
               bar's CLOSE | none
      harvest  harvest_close_ms | harvest_ms + one lens bar | harvest_i on the lens
               tape (checked against entry_i) | v6transform: v6's own harvest by the
               pairing key (checked per row) — gated by `harvested`
      adds     add1_close_ms, add2_close_ms (close events), gated by n_adds
    A campaign whose `harvested` / reached_1r / n_adds records an event that no
    source stamps is counted UNSTAMPED and the door REFUSES to file (instants_of
    HALTs, naming the counts) [L-R.5 'plus the named events'; verifier MAJOR-4].
    Returns (frame of Int64 instants per row + private flags, {event: source})."""
    spec = KINDS[kind]
    lens = spec["lens"]
    step = N.LENS_MS[lens]
    cols = set(reg.columns)
    ev = pd.DataFrame(index=reg.index)
    src: dict = {}
    if spec["start"] == "arm":
        if "arm_close_ms" in cols:
            ev["arm"], src["arm"] = _col(reg, "arm_close_ms"), "arm_close_ms"
        elif "window_arm_close_ms" in cols:
            ev["arm"], src["arm"] = _col(reg, "window_arm_close_ms"), "window_arm_close_ms"
        elif "arm_ms" in cols:
            ev["arm"] = _col(reg, "arm_ms") + step
            src["arm"] = f"arm_ms + {lens} (the arm bar's OPEN + one bar)"
        elif kind == "v6transform":
            ev["arm"] = _v6_arm_join(reg).astype("Int64")
            src["arm"] = "v6's own arm, joined on (symbol, entry_ms) [L-1.5]"
        else:
            _halt(f"kind {kind} needs an arm column (arm_close_ms / window_arm_close_ms / "
                  f"arm_ms)")
    x1h = next((c for c in EXIT_1H_COLS if c in cols), None)
    if "exit_stamp_ms" in cols:
        src["exit"] = "exit_stamp_ms"
    elif "exit_event_ms" in cols:
        src["exit"] = "exit_event_ms"
    elif x1h is not None:
        if "exit_resolved_by" not in cols:
            _halt(f"nest-book: {x1h} without exit_resolved_by — a parent-decided stop cannot "
                  f"be told from a 1h-resolved one [L-R.5, AM-6]")
        src["exit"] = (f"{x1h} by exit_resolved_by ('1h' -> as filed; 'close' -> a close "
                       f"reason as filed at exit_close_ms; 'parent' -> an intrabar reason at "
                       f"the parent bar's OPEN, a close reason at the parent's close) "
                       f"[L-R.5, AM-6]")
    else:
        src["exit"] = ("derived per row (intrabar reason -> the OPEN of the lens bar holding "
                       "exit_close_ms; close reason -> exit_close_ms)")
    xbc = next((c for c in EXIT_BAR_CLOSE_COLS if c in cols), None)
    src["exit_post_event"] = (f"THE TWIN LAW: an intrabar exit stamped before the close of the "
                              f"{lens} bar holding it -> that close "
                              + (f"({xbc})" if xbc else "(exit_close_ms)"))
    ev["_p1r_parent"] = False
    if "latch_stamp_ms" in cols:
        ev["plus_1r"], src["plus_1r"] = _col(reg, "latch_stamp_ms"), "latch_stamp_ms"
        if "latch_post_event_ms" in cols:
            ev["plus_1r_post_event"] = _col(reg, "latch_post_event_ms")
            src["plus_1r_post_event"] = "latch_post_event_ms"
    elif "latch_1h_ms" in cols:
        lat = _col(reg, "latch_1h_ms")
        if "latched_1h" in cols:
            lat = lat.where(_flag(reg, "latched_1h"))
        par = _parent_latch(reg, lat, step)
        ev["_p1r_parent"] = par
        stamp = lat.where(~par, lat - step)
        ev["plus_1r"] = stamp
        hold = ((lat + (step - 1)) // step) * step       # the close of the lens bar holding it
        ev["plus_1r_post_event"] = hold.where((hold > stamp).fillna(False).astype(bool))
        src["plus_1r"] = ("latch_1h_ms (the resolving 1h child's close; a PARENT-decided latch "
                          "-> the parent's OPEN, source "
                          + next((c for c in ("latch_1h_by", "walk_mismatch_ms",
                                              "n_walk_mismatch") if c in cols),
                                 "none needed: no latch sits at a parent close") + ")")
        src["plus_1r_post_event"] = (f"THE TWIN LAW: the close of the {lens} bar holding "
                                     f"latch_1h_ms, when after the stamp (a parent-decided "
                                     f"latch: the parent's close; a latch resolved before the "
                                     f"bar's last 1h child: the bar's close; none when the "
                                     f"resolving child is the bar's last)")
    elif "reached_1r" in cols and kind in ("v6transform", "lane4h"):
        src["plus_1r"] = f"derived: the OPEN of the first {lens} bar after the entry whose " \
                         f"favourable extreme reaches entry +/- R (reached_1r rows only)"
        ev["plus_1r"] = pd.array([pd.NA] * len(reg), dtype="Int64")
        ev["plus_1r_post_event"] = pd.array([pd.NA] * len(reg), dtype="Int64")
        src["plus_1r_post_event"] = "derived: that bar's CLOSE"
    else:
        src["plus_1r"] = "none (no latch column; reached_1r rows, if any, are UNSTAMPED)"
    hv = None
    if "harvest_close_ms" in cols:
        hv, src["harvest"] = _col(reg, "harvest_close_ms"), "harvest_close_ms"
    elif "harvest_ms" in cols:
        hv, src["harvest"] = _col(reg, "harvest_ms") + step, f"harvest_ms + {lens}"
    elif "harvest_i" in cols:
        hv, src["harvest"] = None, f"harvest_i on the {lens} tape (checked against entry_i)"
    elif kind == "v6transform" and "harvested" in cols:
        hv6, keyed = _v6_harvest_join(reg)
        ev["_v6_harvest"], ev["_v6_keyed"] = hv6, keyed
        src["harvest"] = ("v6's own harvest close, joined on (symbol, entry_ms) [L-1.5] — "
                          "checked per row: harvested -> v6 harvested at or before the exit "
                          "stamp; not harvested -> v6 did not harvest before it")
    else:
        src["harvest"] = ("none (no harvest column; harvested rows, if any, are UNSTAMPED)")
    if hv is not None:
        if "harvested" in cols:
            hv = hv.where(_flag(reg, "harvested"))
        ev["harvest"] = hv
    for j in (1, 2):
        if f"add{j}_close_ms" in cols:
            ev[f"add{j}"], src[f"add{j}"] = _col(reg, f"add{j}_close_ms"), f"add{j}_close_ms"
    if "n_adds" in cols and not any(f"add{j}_close_ms" in cols for j in (1, 2)):
        src["adds"] = "none (no add{1,2}_close_ms; rows with n_adds > 0 are UNSTAMPED)"
    for c in sorted(c for c in cols if c.startswith("ev_") and c.endswith("_ms")):
        ev[c[3:-3]], src[c[3:-3]] = _col(reg, c), c
    return ev, src


def _exit_stamp(r, tape_closes: np.ndarray, step: int) -> tuple[int, str]:
    """(the exit stamp of record, how it was resolved): 'filed' (exit_stamp_ms /
    exit_event_ms as filed), '1h' (a 1h-walked ride's resolving child's close),
    'parent' (a parent-resolved exit: an intrabar reason at the parent's OPEN),
    'close' (a CLOSE reason resolved at exit_close_ms), 'derived' (from exit_reason on
    the lens tape).  HALTS on an intrabar reason resolved by 'close' — the ride
    resolves only bell / corridor_end exits at the close [tierc11_ride; verifier
    MINOR-3] — and on a 'close'-resolved exit off exit_close_ms."""
    for c in ("exit_stamp_ms", "exit_event_ms"):
        if c in r and not pd.isna(r[c]):
            return int(r[c]), "filed"
    reason = str(r["exit_reason"])
    ec = int(r["exit_close_ms"])
    for c in EXIT_1H_COLS:                     # a 1h-walked ride's resolved exit [SR-9]
        if c in r and not pd.isna(r[c]):
            x, by = int(r[c]), str(r["exit_resolved_by"])
            if not (int(r["entry_close_ms"]) < x <= ec):
                _halt(f"{r['symbol']} {iso(int(r['entry_close_ms']))}: {c} {iso(x)} is not "
                      f"inside (entry close, exit_close_ms {iso(ec)}]")
            intr = reason in INTRABAR_EXIT_REASONS
            if by == "parent":
                if x % step:
                    _halt(f"{r['symbol']} {iso(x)}: a parent-resolved exit not at a "
                          f"{step // 3_600_000}h close")
                return ((x - step if INTRABAR_STAMP == "bar_open" else x) if intr else x,
                        "parent")
            if by == "close":
                if intr:
                    _halt(f"{r['symbol']} {iso(int(r['entry_close_ms']))}: an intrabar exit "
                          f"({reason!r}) resolved by 'close' — a stop / TP fill is resolved "
                          f"by its 1h child or by the parent, never read at the close "
                          f"[L-R.5, AM-6]")
                if x != ec:
                    _halt(f"{r['symbol']} {iso(int(r['entry_close_ms']))}: a 'close'-resolved "
                          f"exit {c} {iso(x)} is not exit_close_ms {iso(ec)}")
                return x, "close"
            if by == "1h":
                if intr and INTRABAR_STAMP != "bar_open":   # the close-stamping SABOTAGE
                    k = int(np.searchsorted(tape_closes, x, side="left"))
                    return int(tape_closes[k]), "1h"
                return x, "1h"
            _halt(f"{r['symbol']} {iso(int(r['entry_close_ms']))}: exit_resolved_by {by!r} "
                  f"is none of '1h' / 'close' / 'parent'")
    if reason in INTRABAR_EXIT_REASONS:
        k = int(np.searchsorted(tape_closes, ec, side="left"))
        if k >= len(tape_closes):
            _halt(f"{r['symbol']}: exit_close_ms {iso(ec)} beyond the lens tape")
        op = int(tape_closes[k]) - step
        return (op if INTRABAR_STAMP == "bar_open" else int(tape_closes[k])), "derived"
    if reason.startswith(CLOSE_EXIT_PREFIXES):
        return ec, "derived"
    _halt(f"{r['symbol']} {iso(int(r['entry_close_ms']))}: exit_reason {reason!r} is neither a "
          f"known intrabar nor a known close reason and the regbook carries no exit stamp column")


def _exit_bar_close(r, ec: int) -> int:
    """[SR-15 THE TWIN LAW] the close of the lens bar holding the exit: exit_bar_close_ms
    when filed (the relay: its exit_close_ms is the 1h exit instant), else exit_close_ms."""
    for c in EXIT_BAR_CLOSE_COLS:
        if c in r and not pd.isna(r[c]):
            return int(r[c])
    return ec


def _derived_latch(r, tape, closes: np.ndarray) -> int | None:
    """[SR-9] the bar-OPEN law on the lens tape (the books' own, tierc10_stamps.
    _plus_1r_bar): the first bar in (entry bar, EXIT bar] whose favourable extreme
    reaches entry +/- R — the exit bar is the bar holding exit_close_ms, counted
    (the v6 ride latches at the TOP of a bar, before its stop / TP test).  None when
    the ride never latched (reached_1r False)."""
    if not bool(r["reached_1r"]):
        return None
    ec = int(r["entry_close_ms"])
    k0 = int(np.searchsorted(closes, ec, side="left"))
    if k0 >= len(closes) or int(closes[k0]) != ec:
        _halt(f"{r['symbol']} {iso(ec)}: a derived +1R needs an entry at a lens close")
    k1 = int(np.searchsorted(closes, int(r["exit_close_ms"]), side="left"))
    d, R, ep = int(r["direction"]), float(r["r_dist"]), float(r["entry_px"])
    ext = tape.h if d == 1 else tape.l
    for j in range(k0 + 1, min(k1, len(closes) - 1) + 1):
        if (float(ext[j]) - ep) * d / R >= 1.0:
            return j
    _halt(f"{r['symbol']} {iso(ec)}: reached_1r is True but no {tape.lens} bar through the exit "
          f"bar reaches +1R")


def instants_of(reg: pd.DataFrame, kind: str, laws: dict | None = None
                ) -> tuple[pd.DataFrame, dict]:
    """THE INSTANT LAW [L-R.5, SR-6, SR-9] for a regbook-schema frame: per campaign,
    every close of its own lens from its arm (or entry) through its exit stamp of
    record, plus its named events (sources resolved once, resolve_events).  One row
    per (campaign, instant_kind, instant); `stamp_law` names each row's rule (`laws`
    overrides it per event — the books path names its unwalked 4h law).  A campaign
    OPEN at the pin (corridor_end) gets 'as_of_pin', never 'exit'.  HALTS — the door
    refuses to file — when any recorded event is UNSTAMPED.  Returns (frame, sources)."""
    if kind not in KINDS:
        _halt(f"unknown nest-book kind {kind!r}; one of {list(KINDS)}")
    laws = laws or {}
    spec = KINDS[kind]
    lens = spec["lens"]
    step = N.LENS_MS[lens]
    evs, src = resolve_events(reg, kind)
    derive_latch = src.get("plus_1r", "").startswith("derived")
    v6_harvest = "_v6_harvest" in evs.columns
    cols = set(reg.columns)
    # the ride's own +1R record gates the UNSTAMPED count: latched_1h (a 1h-walked
    # ride's latch) when filed, else reached_1r
    p1r_gate = next((c for c in ("latched_1h", "reached_1r") if c in cols), None)
    unst = {"+1R": 0, "harvest": 0, "add": 0}
    rows = []
    for s in sorted(reg["symbol"].unique(), key=lambda x: (PANEL17.index(x) if x in PANEL17
                                                           else 99, x)):
        tape = N.load11(s, lens)
        closes = (tape.t0 + tape.step).astype(np.int64)
        g = reg[reg["symbol"] == s].sort_values("entry_close_ms", kind="mergesort")
        if src.get("harvest", "").startswith("harvest_i") and "entry_i" in g.columns:
            bad = [int(x) for x, e in zip(g["entry_i"], g["entry_ms"])
                   if int(tape.t0[int(x)]) != int(e)]
            if bad:
                _halt(f"{s}: the book's bar indices are not the {lens} tape's (entry_i {bad[:3]})")
        for idx, r in g.iterrows():
            base = (s, int(r["entry_ms"]), int(r["entry_close_ms"]), int(r["direction"]))
            ex, how = _exit_stamp(r, closes, step)
            ec = int(r["exit_close_ms"])
            e = evs.loc[idx]
            start = int(e["arm"]) if spec["start"] == "arm" else int(r["entry_close_ms"])
            if ex < int(r["entry_close_ms"]) or start > int(r["entry_close_ms"]):
                _halt(f"{s} {iso(int(r['entry_close_ms']))}: arm / exit stamp out of order")
            for c in closes[(closes >= start) & (closes <= ex)]:
                rows.append(base + ("bar_close", int(c), f"close ({lens} bar)"))

            def add(k: str, ms, law: str) -> bool:
                if ms is None or pd.isna(ms):
                    return False
                rows.append(base + (k, int(ms), laws.get(k, law)))
                return True
            if spec["start"] == "arm":
                add("arm", e["arm"], f"close ({src['arm']})")
            add("entry", r["entry_close_ms"], LAW_CLOSE)
            got_p1r = False
            if derive_latch:
                j = _derived_latch(r, tape, closes)
                if j is not None:
                    op, cl = int(closes[j]) - step, int(closes[j])
                    got_p1r = add("plus_1r", op if INTRABAR_STAMP == "bar_open" else cl,
                                  LAW_P1R_DERIVED.format(lens=lens))
                    add("plus_1r_post_event", cl, LAW_TWIN)
            else:
                if "plus_1r" in evs.columns:
                    law = (LAW_P1R_PARENT if bool(e["_p1r_parent"]) else LAW_P1R_CHILD) \
                        if src["plus_1r"].startswith("latch_1h_ms") else LAW_P1R_STAMP
                    got_p1r = add("plus_1r", e["plus_1r"], law)
                if "plus_1r_post_event" in evs.columns:
                    add("plus_1r_post_event", e["plus_1r_post_event"], LAW_TWIN)
            if p1r_gate is not None and _true(r[p1r_gate]) and not got_p1r:
                unst["+1R"] += 1
            harv = _true(r["harvested"]) if "harvested" in cols else None
            got_h = False
            if v6_harvest:
                hv6, keyed = e["_v6_harvest"], bool(e["_v6_keyed"])
                if harv and keyed:
                    if pd.isna(hv6) or int(hv6) > ex:
                        _halt(f"{s} {iso(int(r['entry_close_ms']))}: harvested, but v6's harvest "
                              f"({'none' if pd.isna(hv6) else iso(int(hv6))}) is not at or "
                              f"before the exit stamp {iso(ex)} — the pairing-key harvest join "
                              f"does not hold for this book [L-1.5]")
                    got_h = add("harvest", hv6, LAW_CLOSE + " (v6's harvest by the pairing key)")
                elif keyed and not harv and not pd.isna(hv6) and int(hv6) < ex:
                    _halt(f"{s} {iso(int(r['entry_close_ms']))}: NOT harvested, but v6 harvested "
                          f"at {iso(int(hv6))} before the exit stamp {iso(ex)} — the "
                          f"pairing-key harvest join does not hold for this book [L-1.5]")
            elif "harvest" in evs.columns:
                got_h = add("harvest", e["harvest"], LAW_CLOSE)
            elif src.get("harvest", "").startswith("harvest_i"):
                hi = r["harvest_i"]
                if not pd.isna(hi) and (harv is None or harv):
                    got_h = add("harvest", int(closes[int(hi)]), LAW_CLOSE)
            if got_h:
                h_ms = int(rows[-1][5])
                if not (int(r["entry_close_ms"]) < h_ms <= max(ex, ec)):
                    _halt(f"{s} {iso(int(r['entry_close_ms']))}: harvest {iso(h_ms)} is not "
                          f"inside (entry close, exit] — the harvest source is not this "
                          f"campaign's")
            if harv and not got_h:
                unst["harvest"] += 1
            n_add = 0
            for j2 in (1, 2):
                if f"add{j2}" in evs.columns:
                    n_add += int(add(f"add{j2}", e[f"add{j2}"], LAW_CLOSE))
            if "n_adds" in cols and not pd.isna(r["n_adds"]) and int(r["n_adds"]) > n_add:
                unst["add"] += int(r["n_adds"]) - n_add
            for c in [k for k in evs.columns if k not in ("arm", "plus_1r", "plus_1r_post_event",
                                                          "harvest", "add1", "add2")
                      and not k.startswith("_")]:
                add(c, e[c], "named event (as given)")
            reason = str(r["exit_reason"])
            if reason.startswith("bell"):
                add("bell", ec, LAW_CLOSE)
            if reason.startswith("corridor_end"):
                add("as_of_pin", ex, LAW_PIN)
            else:
                # the stamp law is the EVENT's class (intrabar vs close), never its
                # position against exit_close_ms [SR-15; verifier MINOR-1]
                intr = reason in INTRABAR_EXIT_REASONS
                if intr:
                    x1c = next((c for c in EXIT_1H_COLS if c in cols), "")
                    law = laws.get("exit_intrabar") or (
                        LAW_EXIT_CHILD.format(col=x1c) if how == "1h" else
                        LAW_EXIT_PARENT.format(col=x1c, lens=lens) if how == "parent" else
                        f"intrabar (stamp of record: {src['exit']})")
                else:
                    law = (f"close — a close event at its own instant (stamp of record: "
                           f"{src['exit']})" if ex < ec else LAW_CLOSE)
                add("exit", ex, law)
                xb = _exit_bar_close(r, ec)
                if intr and ex < xb:            # THE TWIN LAW [SR-15; verifier MINOR-2]
                    want = ex + step if ex % step == 0 else ((ex + step - 1) // step) * step
                    if xb != want:
                        _halt(f"{s} {iso(int(r['entry_close_ms']))}: the exit bar's close "
                              f"{iso(xb)} is not the close of the {lens} bar holding the "
                              f"intrabar exit stamp {iso(ex)} ({iso(want)}) — the twin "
                              f"anchor does not hold")
                    add("exit_post_event", xb, LAW_TWIN)
    if any(unst.values()):
        _halt("nest-book UNSTAMPED [L-R.5 'plus the named events'; verifier MAJOR-4]: "
              + " · ".join(f"{k} {v}" for k, v in unst.items() if v)
              + " recorded event(s) have no instant source (sources: "
              + "; ".join(f"{k} = {src.get(k, '—')}" for k in ("plus_1r", "harvest", "adds")
                          if k in src)
              + ") — the door refuses to file a nest that silently drops them")
    f = pd.DataFrame(rows, columns=["symbol", "entry_ms", "entry_close_ms", "direction",
                                    "instant_kind", "instant_ms", "stamp_law"])
    for c in ("entry_ms", "entry_close_ms", "instant_ms"):
        f[c] = f[c].astype(np.int64)
    f["direction"] = f["direction"].astype(np.int8)
    f["campaign_lens"] = lens
    f["nest_kind"] = kind
    return f, src


def nest_frame(inst: pd.DataFrame, scales=SCALE_KINDS) -> pd.DataFrame:
    """N.nest_at at the instants, per symbol and scale, joined back m:1."""
    parts = []
    for kind in scales:
        for s in sorted(inst["symbol"].unique(), key=lambda x: (PANEL17.index(x)
                                                                if x in PANEL17 else 99, x)):
            g = inst[inst["symbol"] == s]
            u = np.unique(g["instant_ms"].to_numpy(np.int64))
            nv = N.nest_at(s, u, kind)
            m = g.merge(nv, on="instant_ms", how="left", validate="m:1")
            if len(m) != len(g):
                _halt(f"nest join changed the row count for {s} {kind}")
            m.insert(0, "scale_kind", kind)
            parts.append(m)
    f = pd.concat(parts, ignore_index=True)
    f["instant_ts"] = [iso(x) for x in f["instant_ms"]]
    for k, v in {**COLLAR, **AS_OF}.items():
        f[k] = v
    return f


BOOK_LAWS = {"plus_1r": LAW_P1R_BOOKS, "exit_intrabar": LAW_EXIT_BOOKS}


def book_nest(camp: pd.DataFrame, book: str) -> pd.DataFrame:
    """The nest of one book of books/ — the books' UNWALKED 4h ride: +1R and a stop
    exit at the OPEN of their 4h bar, each row's stamp_law naming it [verifier
    MINOR-9: a 1h-walked regbook through the door stamps +1R at the resolving 1h
    child's close instead; both lawful under L-R.5, each table names its rule]."""
    reg = regframe_from_campaigns(camp)
    law = dict(BOOK_LAWS)
    f = nest_frame(instants_of(reg, "v6transform", laws=law)[0])
    f.insert(1, "book", book)
    return f


# ══════════════════════════════════════════════════════════ 6 · NEST GRID + R5
def coin_cat(top, bot, lens: str) -> np.ndarray:
    if lens == "1w":
        return np.array(["NA"] * len(top), dtype=object)
    t = pd.array(top, dtype="boolean")
    b = pd.array(bot, dtype="boolean")
    if bool(t.isna().any()) or bool(b.isna().any()):
        _halt(f"coincidence NA below 1w on lens {lens} (CLASSIC5 books)")
    t = np.asarray(t, dtype=bool)
    b = np.asarray(b, dtype=bool)
    return np.where(t & b, "both", np.where(t, "top", np.where(b, "bot", "none"))).astype(object)


def _stats(net: np.ndarray) -> dict:
    net = np.asarray(net, dtype=float)
    n = int(len(net))
    if not n:
        return {"n": 0, "mean_net_r": np.nan, "p_win": np.nan, "sum_net_r": np.nan,
                "nan_reason": "n = 0"}
    return {"n": n, "mean_net_r": float(net.mean()), "p_win": float((net > 0).mean()),
            "sum_net_r": float(net.sum()), "nan_reason": ""}


def entry_frame(nest: pd.DataFrame, camp: pd.DataFrame) -> pd.DataFrame:
    e = nest[nest["instant_kind"] == "entry"]
    j = e.merge(camp[["symbol", "entry_ms", "net_r"]], on=["symbol", "entry_ms"],
                how="left", validate="m:1")
    if j["net_r"].isna().any() or len(j) != 2 * len(camp):
        _halt("entry rows do not cover every campaign at both scales")
    j["era"] = E.era_of(j["entry_close_ms"].to_numpy(np.int64)).astype(str)
    return j


# ── THE HONESTY LABELS of the aggregated tables [L-R.2 SCALE-IN-SAMPLE, AM-4;
#    verifier MAJOR-3]: every R5 / NEST_GRID row names the lenses it consumes, their
#    pick windows and stability-changed members, counts its entries whose read is
#    in-sample / on a stability-changed pick, and prints the HOLDOUT slice (the only
#    causal slice of a tuning-calibrated read) beside the whole-book cell.
HONESTY_LAW = (
    "SCALE-IN-SAMPLE [L-R.2, AM-4]: a calibrated-scale range read at an instant <= the era cut "
    "(2024-06-30T23:59:59Z) is structurally IN-SAMPLE (the tuning pick saw those bars; a "
    "whole-tape fallback pick is in-sample at every instant; frozen 3.0 never is). Every row "
    "carries `lenses_read` (the lenses the cell consumes: L, and L+1 for a coincidence cell), "
    "their `pick_window` and `stability_changed_members` (first-half-of-tuning pick != "
    "tuning pick), `n_scale_in_sample` / `n_stability_changed` (the cell's entries whose read "
    "is in-sample / rides a stability-changed pick, on ANY consumed lens), and the HOLDOUT "
    "slice (entry close after the cut: n_holdout, mean_net_r_holdout, p_win_holdout, "
    "sum_net_r_holdout) — the causal slice of a tuning pick, printed beside every cell.")


def _lenses_read(L: str, coin: bool) -> tuple:
    U = N.LADDER[L]
    return (L, U) if (coin and U is not None) else (L,)


def _bool_col(z: pd.DataFrame, c: str) -> np.ndarray:
    return z[c].astype("boolean").fillna(False).to_numpy(bool)


def _lens_labels(z: pd.DataFrame, lenses: tuple) -> dict:
    """Lens-level labels over ALL the entries of one (book, scale): per consumed lens
    its pick window(s) and its stability-changed members; per entry the in-sample /
    stability-changed flags OR-ed over the consumed lenses."""
    isin = np.zeros(len(z), bool)
    stab = np.zeros(len(z), bool)
    pw, sm = [], []
    for c in lenses:
        isin |= _bool_col(z, f"{c}_scale_in_sample")
        sc = _bool_col(z, f"{c}_stability_changed")
        stab |= sc
        pw.append(f"{c}: " + " / ".join(sorted({str(x) for x in z[f"{c}_pick_window"]})))
        mem = sorted(set(z.loc[sc, "symbol"].astype(str)),
                     key=lambda x: (PANEL17.index(x) if x in PANEL17 else 99, x))
        sm.append(f"{c}: " + (",".join(mem) if mem else "none"))
    return {"lenses_read": "+".join(lenses), "pick_window": "; ".join(pw),
            "stability_changed_members": "; ".join(sm), "_isin": isin, "_stab": stab}


def _cell(net: np.ndarray, isin: np.ndarray, stab: np.ndarray, hold: np.ndarray) -> dict:
    """one cell: the whole-book statistics, the honesty counts and the holdout slice
    (the same _stats law on both)."""
    d = _stats(net)
    h = _stats(net[hold])
    d.update({"n_scale_in_sample": int(isin.sum()), "n_stability_changed": int(stab.sum()),
              "n_holdout": h["n"], "mean_net_r_holdout": h["mean_net_r"],
              "p_win_holdout": h["p_win"], "sum_net_r_holdout": h["sum_net_r"],
              "nan_reason_holdout": h["nan_reason"]})
    return d


def nest_grid(entries: dict) -> dict:
    freq, bys, byc = [], [], []
    for book in BOOKS:
        j = entries[book]
        for kind in SCALE_KINDS:
            z = j[j["scale_kind"] == kind].reset_index(drop=True)
            n_all = len(z)
            net = z["net_r"].to_numpy(float)
            hold = (z["era"] == "holdout").to_numpy(bool)
            for L in NEST_LENSES:
                st = z[f"{L}_state"].astype(str).to_numpy()
                cats = {"record": coin_cat(z[f"{L}_coin_top"], z[f"{L}_coin_bot"], L),
                        "mem_twin": coin_cat(z[f"{L}_coin_top_mem"], z[f"{L}_coin_bot_mem"], L)}
                ccs = ("NA",) if L == "1w" else COIN_CATS
                lc = _lens_labels(z, _lenses_read(L, coin=True))
                ls = _lens_labels(z, _lenses_read(L, coin=False))
                labc = {k: v for k, v in lc.items() if not k.startswith("_")}
                labs = {k: v for k, v in ls.items() if not k.startswith("_")}
                for rule in COIN_RULES:
                    cc = cats[rule]
                    for s4 in STATES4:
                        for c in ccs:
                            m = (st == s4) & (cc == c)
                            freq.append({"cell": f"{book}|{kind}|{L}|{rule}|{s4}|{c}",
                                         "book": book, "scale_kind": kind, "lens": L,
                                         "coin_rule": rule, "state": s4, "coin_cat": c,
                                         "n": int(m.sum()), "n_entries": n_all,
                                         "share": float(m.sum()) / n_all if n_all else np.nan,
                                         "n_scale_in_sample": int(lc["_isin"][m].sum()),
                                         "n_stability_changed": int(lc["_stab"][m].sum()),
                                         "n_holdout": int(hold[m].sum()), **labc})
                    for c in ccs:
                        m = cc == c
                        byc.append({"cell": f"{book}|{kind}|{L}|{rule}|{c}", "book": book,
                                    "scale_kind": kind, "lens": L, "coin_rule": rule,
                                    "coin_cat": c,
                                    **_cell(net[m], lc["_isin"][m], lc["_stab"][m], hold[m]),
                                    **labc})
                for s4 in STATES4 + ("__ALL__",):
                    m = np.ones(len(st), bool) if s4 == "__ALL__" else st == s4
                    bys.append({"cell": f"{book}|{kind}|{L}|{s4}", "book": book,
                                "scale_kind": kind, "lens": L, "state": s4,
                                **_cell(net[m], ls["_isin"][m], ls["_stab"][m], hold[m]),
                                **labs})
    out = {}
    for name, rows in (("NEST_GRID_FREQ", freq), ("NEST_GRID_BY_STATE", bys),
                       ("NEST_GRID_BY_COIN", byc)):
        d = pd.DataFrame(rows)
        for k, v in {**COLLAR, **AS_OF}.items():
            d[k] = v
        out[name] = d
    return out


def bucket_of(state: np.ndarray, pct: np.ndarray) -> np.ndarray:
    out = np.empty(len(state), dtype=object)
    for i, (s, p) in enumerate(zip(state, pct)):
        if s != "IN_RANGE":
            out[i] = f"not-in-range:{s}"
        elif not np.isfinite(p):
            _halt("an IN_RANGE entry carries no finite pct")
        elif p < 0:
            out[i] = "<0"
        elif p >= 100:
            out[i] = ">=100"
        else:
            out[i] = DECILES[int(p // 10)]
    return out


def r5_chop(entry_v6: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for kind in SCALE_KINDS:
        z = entry_v6[entry_v6["scale_kind"] == kind].reset_index(drop=True)
        net = z["net_r"].to_numpy(float)
        hold = (z["era"] == "holdout").to_numpy(bool)
        for L in R5_LENSES:
            b = bucket_of(z[f"{L}_state"].astype(str).to_numpy(), z[f"{L}_pct"].to_numpy(float))
            lab = _lens_labels(z, (L,))
            labs = {k: v for k, v in lab.items() if not k.startswith("_")}
            for bk in R5_BUCKETS:
                m = np.ones(len(b), bool) if bk == "__ALL__" else b == bk
                rows.append({"cell": f"{kind}|{L}|{bk}", "scale_kind": kind, "lens": L,
                             "bucket": bk,
                             **_cell(net[m], lab["_isin"][m], lab["_stab"][m], hold[m]),
                             **labs})
    d = pd.DataFrame(rows)
    for k, v in {**COLLAR, **AS_OF}.items():
        d[k] = v
    return d


# ── R5 BY DIRECTION [SR-16] — the seams align_of / dir_adj_pct are read at CALL time
#    (F-CHOP-VALUE plants them) ──────────────────────────────────────────────────
def _direction(z: pd.DataFrame) -> np.ndarray:
    d = z["direction"].to_numpy(np.int64)
    bad = ~np.isin(d, (1, -1))
    if bad.any():
        _halt(f"R5 BY DIRECTION: {int(bad.sum())} entry row(s) carry a direction outside "
              f"{{+1, -1}}")
    return d


def align_of(state: np.ndarray, direction: np.ndarray) -> np.ndarray:
    """EXP_ALIGNED = the lens expands the trade's way (BULL_EXP for a long, BEAR_EXP for
    a short); EXP_COUNTER = the other expansion; IN_RANGE / NONE as read."""
    out = np.empty(len(state), dtype=object)
    for i, (s, d) in enumerate(zip(state, direction)):
        if s in ("IN_RANGE", "NONE"):
            out[i] = s
        elif s in ("BULL_EXP", "BEAR_EXP"):
            out[i] = "EXP_ALIGNED" if (s == "BULL_EXP") == (int(d) > 0) else "EXP_COUNTER"
        else:
            _halt(f"R5 BY DIRECTION: undeclared lens state {s!r}")
    return out


def dir_adj_pct(pct: np.ndarray, direction: np.ndarray) -> np.ndarray:
    """pct for a long, 100 - pct for a short (unclamped): 100 = the boundary the trade
    must break, 0 = the one behind it."""
    pct = np.asarray(pct, dtype=float)
    return np.where(np.asarray(direction) > 0, pct, 100.0 - pct)


def adj_bucket_of(adj: np.ndarray) -> np.ndarray:
    """SR-8's half-open law on the adjusted pct: '<0'; [0, 100/3); [100/3, 200/3);
    [200/3, 100); '>=100'."""
    out = np.empty(len(adj), dtype=object)
    for i, a in enumerate(adj):
        if not np.isfinite(a):
            _halt("an IN_RANGE entry carries no finite pct")
        if a < 0:
            out[i] = "<0"
        elif a >= R5_ADJ_CUTS[2]:
            out[i] = ">=100"
        else:
            out[i] = R5_ADJ_BUCKETS[1 + int(a >= R5_ADJ_CUTS[0]) + int(a >= R5_ADJ_CUTS[1])]
    return out


def r5_direction(entry_v6: pd.DataFrame) -> pd.DataFrame:
    """R5_CHOP_DIRECTION [SR-16]: the v6 entries by alignment and by direction-adjusted
    pct tercile, per scale x {4h, 12h} — the same _cell / honesty law as R5_CHOP."""
    rows = []
    for kind in SCALE_KINDS:
        z = entry_v6[entry_v6["scale_kind"] == kind].reset_index(drop=True)
        net = z["net_r"].to_numpy(float)
        hold = (z["era"] == "holdout").to_numpy(bool)
        d = _direction(z)
        lng = d > 0
        for L in R5_LENSES:
            st = z[f"{L}_state"].astype(str).to_numpy()
            inr = st == "IN_RANGE"
            keys = {"alignment": align_of(st, d),
                    "pct_dir_adj": np.full(len(z), "", dtype=object)}
            keys["pct_dir_adj"][inr] = adj_bucket_of(
                dir_adj_pct(z[f"{L}_pct"].to_numpy(float), d)[inr])
            lab = _lens_labels(z, (L,))
            labs = {k: v for k, v in lab.items() if not k.startswith("_")}
            for split, arr in keys.items():
                for bk in R5_DIR_BUCKETS[split]:
                    m = np.ones(len(z), bool) if bk == "__ALL__" else arr == bk
                    rows.append({"cell": f"{kind}|{L}|{split}|{bk}", "scale_kind": kind,
                                 "lens": L, "split": split, "bucket": bk,
                                 "n_long": int((m & lng).sum()), "n_short": int((m & ~lng).sum()),
                                 **_cell(net[m], lab["_isin"][m], lab["_stab"][m], hold[m]),
                                 **labs, "split_law": R5_DIR_SPLIT_LAW[split]})
    out = pd.DataFrame(rows)
    for k, v in {**COLLAR, **AS_OF}.items():
        out[k] = v
    return out


def r5_direction_partition(R5: pd.DataFrame, R5D: pd.DataFrame) -> list[str]:
    """SR-16's partitions against the unchanged R5 rows (the build HALTs on any)."""
    out = []
    for kind in SCALE_KINDS:
        for L in R5_LENSES:
            a = R5[(R5["scale_kind"] == kind) & (R5["lens"] == L)].set_index("bucket")["n"]
            z = R5D[(R5D["scale_kind"] == kind) & (R5D["lens"] == L)]
            al = z[z["split"] == "alignment"].set_index("bucket")
            pc = z[z["split"] == "pct_dir_adj"].set_index("bucket")
            inr = int(sum(int(a[b]) for b in DECILES + ("<0", ">=100")))
            want = {"EXP_ALIGNED+EXP_COUNTER": (
                        int(al.loc["EXP_ALIGNED", "n"]) + int(al.loc["EXP_COUNTER", "n"]),
                        int(a["not-in-range:BULL_EXP"]) + int(a["not-in-range:BEAR_EXP"])),
                    "NONE": (int(al.loc["NONE", "n"]), int(a["not-in-range:NONE"])),
                    "IN_RANGE": (int(al.loc["IN_RANGE", "n"]), inr),
                    "pct_dir_adj": (int(pc["n"].sum()), inr),
                    "__ALL__": (int(al.loc["__ALL__", "n"]), int(a["__ALL__"])),
                    "n_long+n_short": (int((z["n_long"] + z["n_short"] != z["n"]).sum()), 0)}
            for k, (got, exp) in want.items():
                if got != exp:
                    out.append(f"{kind}|{L} {k}: {got} != {exp}")
    return out


def r5_direction_on_cut(entry_v6: pd.DataFrame) -> dict:
    """[SR-16 disclosure] per scale x lens: IN_RANGE entries whose adjusted pct sits
    exactly on a cut (0, 100/3, 200/3, 100) or between a printed label and its exact
    cut ([33.33, 100/3) or [200/3, 66.67)) — where another reading of the tercile text
    would move an entry."""
    out = {}
    for kind in SCALE_KINDS:
        z = entry_v6[entry_v6["scale_kind"] == kind].reset_index(drop=True)
        d = _direction(z)
        for L in R5_LENSES:
            inr = z[f"{L}_state"].astype(str).to_numpy() == "IN_RANGE"
            a = dir_adj_pct(z[f"{L}_pct"].to_numpy(float), d)[inr]
            on = np.isin(a, (0.0, 100.0) + R5_ADJ_CUTS[:2])
            sliver = ((a >= 33.33) & (a < R5_ADJ_CUTS[0])) | ((a >= R5_ADJ_CUTS[1]) & (a < 66.67))
            out[f"{kind}|{L}"] = {"n_in_range": int(inr.sum()), "n_on_a_cut": int(on.sum()),
                                  "n_between_label_and_cut": int(sliver.sum())}
    return out


def five_row(j: pd.DataFrame, shift_ms: int = 0, scale_kind: str = "frozen3.0") -> pd.DataFrame:
    """TC10's entry_state_crosstab (tierc10_stamps.py:1093), transcribed, on the TC11
    nest at FROZEN 3.0 (TC10 LEAN L2), 4h, read at the entry CLOSE (shift_ms /
    scale_kind are F-R5-ANCHOR's sabotage seams).  `j` needs asset, entry_ms, net_r,
    mfe_r."""
    parts = []
    for s in sorted(j["asset"].unique(), key=PANEL17.index):
        g = j[j["asset"] == s].copy()
        inst = g["entry_ms"].to_numpy(np.int64) + MS_4H + int(shift_ms)
        nv = N.nest_at(s, np.unique(inst), scale_kind)
        nv = nv.set_index("instant_ms")
        g["_st"] = nv.loc[inst, "4h_state"].astype(str).to_numpy()
        g["_pct"] = nv.loc[inst, "4h_pct"].to_numpy(float)
        g["_dist"] = np.abs(nv.loc[inst, "4h_dist_signed_atr"].to_numpy(float))
        g["_inr"] = nv.loc[inst, "4h_in_range"].astype("boolean").fillna(False).to_numpy(bool)
        parts.append(g)
    j = pd.concat(parts, ignore_index=True)
    j["_st"] = j["_st"].replace({"IN_RANGE": "NEUTRAL"})
    r6 = E.TB.r6
    rows = []
    for key in TC10_STATES:
        g = j if key == "__ALL__" else j[j["_st"] == key]
        net = g["net_r"].astype(float)
        n = int(len(g))
        rows.append({
            "macro_state_at_entry": key, "n": n, "n_assets": int(g["asset"].nunique()),
            "net_r_sum": r6(float(net.sum())) if n else None,
            "expectancy_r": r6(float(net.mean())) if n else None,
            "median_net_r": r6(float(net.median())) if n else None,
            "win_rate_pct": r6(100.0 * float((net > 0).mean())) if n else None,
            "median_mfe_r": r6(float(g["mfe_r"].astype(float).median())) if n else None,
            "median_pct_of_range": (r6(float(np.nanmedian(g["_pct"])))
                                    if n and np.isfinite(g["_pct"]).any() else None),
            "median_dist_boundary_atr": (r6(float(np.nanmedian(g["_dist"])))
                                         if n and np.isfinite(g["_dist"]).any() else None),
            "n_in_range": int(g["_inr"].sum()) if n else 0,
            "provisional": bool(n < 30)})
    return pd.DataFrame(rows)


FIVE_INT_COLS = ("n", "n_assets", "n_in_range")
FIVE_FLOAT_COLS = ("net_r_sum", "expectancy_r", "median_net_r", "win_rate_pct", "median_mfe_r",
                   "median_pct_of_range", "median_dist_boundary_atr")


def five_table(tc11_five: pd.DataFrame, filed_five: pd.DataFrame) -> pd.DataFrame:
    """R5_FIVE_ROW: ALL ELEVEN columns of the five-row table, the TC11 v6 book's
    (`tc11_*`) beside TC10's filed anchor (`tc10_*`) [L-R.7, SR-11; verifier MINOR-4].
    None (an empty row's statistic) -> NaN; provisional stays boolean."""
    fb = filed_five.set_index("macro_state_at_entry")
    tb = tc11_five.set_index("macro_state_at_entry")
    five = pd.DataFrame({"macro_state_at_entry": list(TC10_STATES)})
    for c in FIVE_ROW_COLS:
        for tag, src in (("tc11", tb), ("tc10", fb)):
            v = src.loc[list(TC10_STATES), c].tolist()
            if c in FIVE_INT_COLS:
                five[f"{tag}_{c}"] = np.array([int(x) for x in v], dtype=np.int64)
            elif c == "provisional":
                five[f"{tag}_{c}"] = np.array([bool(x) for x in v], dtype=bool)
            else:
                five[f"{tag}_{c}"] = np.array([np.nan if x is None or pd.isna(x) else float(x)
                                               for x in v], dtype=float)
    five["tc10_reproduced_on_filed_journal"] = True
    five["anchor_law"] = READINGS[10]
    return five


def five_row_findings(got: pd.DataFrame, filed: pd.DataFrame) -> list[str]:
    """R5 ANCHOR: every FIVE_ROW_COLS cell of the five rows equal (None == NaN)."""
    out = []
    fb = {str(r["macro_state_at_entry"]): r for _, r in filed.iterrows()}
    gb = {str(r["macro_state_at_entry"]): r for _, r in got.iterrows()}
    if sorted(fb) != sorted(TC10_STATES) or sorted(gb) != sorted(TC10_STATES):
        out.append(f"R5-ANCHOR-ROWS: filed {sorted(fb)} / got {sorted(gb)}")
        return out
    for st in TC10_STATES:
        for c in FIVE_ROW_COLS:
            a, b = gb[st][c], fb[st][c]
            na = a is None or (isinstance(a, float) and np.isnan(a))
            nb = b is None or (isinstance(b, float) and np.isnan(b))
            if na and nb:
                continue
            if na != nb or (c == "provisional" and bool(a) != bool(b)) or \
                    (c != "provisional" and float(a) != float(b)):
                out.append(f"R5-ANCHOR {st}.{c}: TC11 nest {a!r} != TC10 filed {b!r}")
    return out


# ══════════════════════════════════════════════════════════ 7 · THE nest-book DOOR
def read_regbook(regdir: Path, arm: str) -> tuple[pd.DataFrame, dict]:
    p, js = regdir / f"{arm}.parquet", regdir / f"{arm}.json"
    if not p.exists() or not js.exists():
        _halt(f"nest-book: {E.rel_of(E._real(p))} / .json absent")
    meta = json.loads(js.read_text(encoding="utf-8"))
    df = read_parquet(p)
    miss = [c for c in REGBOOK_REQUIRED if c not in df.columns]
    if miss:
        _halt(f"nest-book: {p.name} lacks the required columns {miss}")
    nul = [c for c in REGBOOK_REQUIRED if df[c].isna().any()]
    if nul:
        _halt(f"nest-book: {p.name} has nulls in required columns {nul}")
    if int(meta.get("n", -1)) != len(df):
        _halt(f"nest-book: sidecar n {meta.get('n')} != {len(df)} rows")
    sha = regbook_sha(df)
    if meta.get("book_sha256") != sha:
        _halt(f"nest-book: book_sha256 {str(meta.get('book_sha256'))[:12]}… != the rows' "
              f"{sha[:12]}…")
    return df, meta


def _src_rel(regdir: Path, out: Path) -> str:
    """The regbook's path as a DETERMINISTIC string: relative to the output root
    when it lies inside it (the probe, in every F-DET twin), else tree-relative."""
    r, o = Path(regdir).resolve(), Path(out).resolve()
    if _inside(r, o):
        return "<out>/" + str(r.relative_to(o))
    return E.rel_of(E._real(r))


def nest_book(regdir: Path, arm: str, kind: str, out: Path, W: dict | None = None,
              K: dict | None = None, sub: str = "") -> dict:
    """THE DOOR [L-R.5; SR-9]: stamp every campaign of a regbook arm; writes
    (out/sub)/<REG>__<arm>.parquet + .json."""
    df, meta = read_regbook(Path(regdir), arm)
    reg = str(meta.get("registration", Path(regdir).name)).split(" ")[0]
    inst, src = instants_of(df, kind)
    f = nest_frame(inst)
    f.insert(1, "registration", reg)
    f.insert(2, "arm", arm)
    W = {} if W is None else W
    K = {} if K is None else K
    name = f"{reg}__{arm}"
    d = put_table(f, name, NEST_KEY, Path(out), W, K, round_floats=False, sub=sub)
    side = {"registration": reg, "arm": arm, "kind": kind, "campaign_lens": KINDS[kind]["lens"],
            "source_regbook": _src_rel(Path(regdir), Path(out)),
            "book_sha256": meta["book_sha256"],
            "n_campaigns": int(len(df)), "n_rows": int(len(d)),
            "n_rows_by_kind": {k: int(v) for k, v in
                               d.groupby("instant_kind")["instant_ms"].size().items()},
            "event_sources": src,
            "scales": list(SCALE_KINDS), "content_sha256": C.content_sha(d), "key": NEST_KEY,
            "law": READINGS[5] + " " + READINGS[8], **COLLAR, **AS_OF,
            "source_script": "scripts/tierc11_stage_r.py nest-book"}
    put_json(side, (Path(out) / sub if sub else Path(out)) / f"{name}.json")
    return side


def write_probe(camp: pd.DataFrame, out: Path, W: dict, K: dict) -> Path:
    """The v6 book in the REGBOOK schema — the nest-book door's self-test."""
    reg = regframe_from_campaigns(camp)
    d = put_table(reg, "base", ["symbol", "entry_ms"], out, W, K, round_floats=False,
                  sub="nestbook_probe/V6-PROBE")
    meta = {"registration": "V6-PROBE", "arm": "base", "kind": "base", "ruler": "paired",
            "panel": list(CLASSIC5), "era_scope": "full", "n": int(len(d)),
            "sum_net_r": float(d["net_r"].sum()), "book_sha256": regbook_sha(d),
            "description": ("Stage R's nest-book self-test: books/v6_campaigns.parquet (the "
                            "v6 book with floats at the books table's 6 dp) in the REGBOOK "
                            "schema — NOT the full-precision v6 base arm the stages file (its "
                            "book_sha256 differs; net_r within 5e-7 per row), NOT a "
                            "registration, never scored [SR-14]"),
            "sum_net_r_law": "the sum of the books table's 6-dp rows (SR-14)",
            "source_script": "scripts/tierc11_stage_r.py", **COLLAR}
    put_json(meta, out / "nestbook_probe" / "V6-PROBE" / "base.json")
    return out / "nestbook_probe" / "V6-PROBE"


# ══════════════════════════════════════════════════════════ 8 · MARKDOWN
def _fmt(x, nd: int = 4) -> str:
    if x is None or (isinstance(x, float) and np.isnan(x)) or x is pd.NA:
        return "—"
    if isinstance(x, (bool, np.bool_)):
        return "True" if x else "False"
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    if isinstance(x, (float, np.floating)):
        return f"{float(x):.{nd}f}"
    return str(x)


def md_table(df: pd.DataFrame, cols: list, nd: dict | None = None) -> list[str]:
    nd = nd or {}
    L = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        L.append("| " + " | ".join(_fmt(r[c], nd.get(c, 4)) for c in cols) + " |")
    return L


def ordered(df: pd.DataFrame, spec: list) -> pd.DataFrame:
    """The md's natural order (the parquet keeps the canonical key order):
    spec = [(column, declared order tuple), ...]."""
    ranks = [df[c].map({v: i for i, v in enumerate(o)}) for c, o in spec]
    for c, r in zip([c for c, _ in spec], ranks):
        if r.isna().any():
            _halt(f"md order: {c} holds an undeclared value {sorted(set(df.loc[r.isna(), c]))}")
    key = pd.DataFrame({f"_r{i}": r.to_numpy() for i, r in enumerate(ranks)})
    idx = key.sort_values(list(key.columns), kind="mergesort").index
    return df.iloc[idx.to_numpy()].reset_index(drop=True)


R1_ORDER = [("asset", PANEL17), ("lens", LENSES11)]
GRID_ORDER = [("book", BOOKS), ("scale_kind", SCALE_KINDS), ("lens", NEST_LENSES)]


def collar_line() -> str:
    return (f"Collar on every table below unless marked RECORD: tier = '{COLLAR['tier']}' · "
            f"selection_not_a_result = '{COLLAR['selection_not_a_result']}' · gates = "
            f"'{COLLAR['gates']}'.")


def r1_md(R1: pd.DataFrame, grid: pd.DataFrame, rec: dict) -> list[str]:
    R1 = ordered(R1, R1_ORDER)
    L = ["## R1 · LENSES [L-R.1, L-R.2, L-R.3] — Tier-E", "", collar_line(), "",
         N.pins_block().rstrip("\n").replace(LEAN_TAG + " ", ""), "",
         "### Picks of record per asset x lens (SCALE_PICKS.json — the pins; never re-fitted)",
         ""]
    L += md_table(R1, ["asset", "lens", "n_bars", "n_bars_tuning", "pick_of_record",
                       "pick_window", "tuning_pick", "whole_tape_pick", "first_half_pick",
                       "frozen_scale", "stability_changed", "pick_at_grid_edge",
                       "in_sample_holdout"], {"pick_of_record": 2, "tuning_pick": 2,
                                              "whole_tape_pick": 2, "first_half_pick": 2,
                                              "frozen_scale": 1})
    L += ["", "### Confirmed ranges and density per 100 bars, by era (era = the confirm bar's "
          "CLOSE) — at the pick of record, and at frozen 3.0", ""]
    L += md_table(R1, ["asset", "lens", "n_confirmed_ALL", "n_confirmed_tuning",
                       "n_confirmed_holdout", "density_per_100_ALL", "density_per_100_tuning",
                       "density_per_100_holdout", "n_confirmed_frozen_ALL",
                       "n_confirmed_frozen_tuning", "n_confirmed_frozen_holdout",
                       "density_frozen_per_100_ALL", "density_frozen_per_100_holdout",
                       "density_window_matches_filed"])
    L += ["", "### Labels (pick window, in-sample text) per cell", ""]
    L += md_table(R1, ["asset", "lens", "pick_window", "label"])
    L += ["", "### Stability [L-R.2]: CLASSIC5 x {1h, 4h, 12h}, first half of tuning vs the "
          "whole tuning era", ""]
    st = R1[R1["stability_printed_L_R_2"]]
    L += md_table(st, ["asset", "lens", "first_half_pick", "tuning_pick", "stability_changed"],
                  {"first_half_pick": 2, "tuning_pick": 2})
    L += ["", f"### The whole density grid (SCALE_GRID.parquet, {len(grid)} rows, content sha "
          f"{rec['grid_content_sha256']}; * = the window's pick)", ""]
    sg = [float(s) for s in rec["scale_grid"]]
    L.append("| asset | lens | window | bars | " + " | ".join(f"{s:g}" for s in sg) + " |")
    L.append("|---|---|---|---|" + "---|" * len(sg))
    order = {s: i for i, s in enumerate(PANEL17)}
    lo = {l: i for i, l in enumerate(LENSES11)}
    wo = {w: i for i, w in enumerate(N.WINDOWS)}
    for (a, l, w), g in sorted(grid.groupby(["asset", "lens", "window"]),
                               key=lambda x: (order[x[0][0]], lo[x[0][1]], wo[x[0][2]])):
        g = g.sort_values("scale_mult")
        cells = [f"{d:.4f}{'*' if ch else ''}" for d, ch in zip(g["density_per_100"], g["chosen"])]
        L.append(f"| {a} | {l} | {w} | {int(g['window_bars'].iloc[0])} | " + " | ".join(cells)
                 + " |")
    return L


R2_MD_COLS = ["panel", "lens", "era", "scale_kind", "toll", "toll_bps_rt_min", "toll_bps_rt_max",
              "n_ranges", "ratio_median", "share_ratio_lt_1", "edge_n", "edge_n_ranges",
              "edge_median_term_h20", "edge_toll_atr", "edge_net_h20", "word", "verdict",
              "would_read", "pick_window", "tc10_would_read", "tc10_edge_net_h20"]
R2_DIST_COLS = (["panel", "lens", "era", "scale_kind", "toll", "n_ranges", "toll_atr_median",
                 "height_atr_median", "share_ratio_lt_1"]
                + [f"ratio_d{q}" for q in RATIO_DECILES])


def r2_md(R2: pd.DataFrame, V: dict) -> list[str]:
    L = ["## R2 · FEASIBILITY PER LENS [L-R.4; TC10's Q-R3 law, the census's own functions]",
         "", DISCLOSURE, "",
         "### THE LENS VERDICTS OF RECORD (POOLED:CLASSIC5 · holdout · calibrated · taker) — "
         "RECORD, not Tier-E", "",
         "| lens | VERDICT | maker twin | charter twin | n_ranges | ratio_median | share<1 | "
         "edge_n | edge_n_ranges | median term H20 | toll ATR | net H20 | pick window | scale "
         "in-sample | fallback members | stability-changed members | Tier-E tuning word | "
         "Tier-E ALL word |",
         "|" + "---|" * 18]
    for lens in LENSES11:
        v = V[lens]
        L.append(f"| {lens} | **{v['verdict']}** | {v['maker_twin']} | {v['charter_twin']} | "
                 f"{v['n_ranges']} | {v['ratio_median']:.4f} | {v['share_ratio_lt_1']:.4f} | "
                 f"{v['edge_n']} | {v['edge_n_ranges']} | {v['edge_median_term_h20']:+.6f} | "
                 f"{v['edge_toll_atr']:.6f} | {v['edge_net_h20']:+.6f} | {v['pick_window']} | "
                 f"{v['scale_in_sample']} | {v['fallback_members'] or '—'} | "
                 f"{v['stability_changed_members'] or '—'} | {v['tier_e_tuning_word']} | "
                 f"{v['tier_e_all_word']} |")
    L += ["", "Word law: " + READINGS[2], "", "Record law: " + READINGS[3], "",
          "### Every R2 row, WHOLE (" + str(len(R2)) + " rows). Record rows carry `word` and "
          "`verdict`; every other row is Tier-E (collared) with NO verdict word: its word is "
          "printed as `would_read` [L-1.4, L-R.4]. TC10 continuity (AM-1) on 5m / 4h / 1d "
          "taker rows (`tc10_would_read`).", "", collar_line(), ""]
    order = {p: i for i, p in enumerate([f"ASSET:{s}" for s in PANEL17] + [POOL_C5, POOL_P17])}
    lo = {l: i for i, l in enumerate(LENSES11)}
    eo = {e: i for i, e in enumerate(ERAS)}
    so = {s: i for i, s in enumerate(SCALE_KINDS)}
    to = {t: i for i, t in enumerate(TOLLS)}
    z = R2.assign(_o=[(lo[a], order[b], eo[c], so[d], to[e]) for a, b, c, d, e in
                      zip(R2["lens"], R2["panel"], R2["era"], R2["scale_kind"], R2["toll"])])
    z = z.sort_values("_o", kind="mergesort")
    L += md_table(z, R2_MD_COLS, {"toll_bps_rt_min": 1, "toll_bps_rt_max": 1,
                                  "edge_median_term_h20": 6, "edge_toll_atr": 6,
                                  "edge_net_h20": 6, "tc10_edge_net_h20": 6})
    L += ["", "### The height ÷ round-trip toll DISTRIBUTION per row, WHOLE (" + str(len(R2))
          + " rows): the census's deciles d1..d9 of the per-range ratio, the median height and "
          "toll in ATR [contract R2: 'height ÷ round-trip toll (distribution)']", "",
          collar_line(), ""]
    L += md_table(z, R2_DIST_COLS, {"toll_atr_median": 6, "height_atr_median": 4})
    return L


TWO_P1R_LAWS = (
    "Two lawful +1R stamps [L-R.5, AM-6; verifier MINOR-9] — each row's `stamp_law` names its "
    "rule: NEST_v6 / NEST_trg912 (the books' UNWALKED 4h ride) stamp +1R and a stop exit at "
    "the OPEN of their 4h bar; the nest-book door on a 1h-walked regbook (latch_1h_ms / "
    "exit_stamp_ms) stamps them at the close of the resolving 1h child (a parent-decided "
    "event on a walk-mismatch bar at the parent's OPEN). The same campaign can therefore carry "
    "a +1R instant 1–4 h apart in the two tables.")


def _honesty_lines(G: pd.DataFrame, book_col: bool) -> list[str]:
    """One line per (book, scale, lens): the in-sample share of the entries and the
    stability-changed members of the lens read (from the __ALL__-type row)."""
    L = []
    z = G[G["state"] == "__ALL__"] if "state" in G.columns else G[G["bucket"] == "__ALL__"]
    for _, r in z.iterrows():
        who = f"{r['book']} · " if book_col else "v6 · "
        L.append(f"- {who}{r['scale_kind']} · {r['lens']}: {int(r['n_scale_in_sample'])} of "
                 f"{int(r['n'])} entries read IN-SAMPLE; {int(r['n_stability_changed'])} on a "
                 f"stability-changed pick ({r['stability_changed_members']}); pick window "
                 f"{r['pick_window']}; holdout slice n {int(r['n_holdout'])}")
    return L


GRID_HONEST_COLS = ["n_scale_in_sample", "n_stability_changed", "n_holdout",
                    "mean_net_r_holdout", "p_win_holdout", "sum_net_r_holdout"]


def nest_md(G: dict, nests: dict) -> list[str]:
    L = ["## R3 · THE NEST ON THE BOOKS [L-R.5, AM-6] — Tier-E", "", collar_line(), "",
         READINGS[5], "", READINGS[6], "", TWO_P1R_LAWS, "", HONESTY_LAW, ""]
    for book, f in nests.items():
        c = f.groupby(["scale_kind", "instant_kind"]).size()
        L.append(f"- NEST_{book}.parquet: {len(f)} rows ({f['symbol'].nunique()} assets, "
                 f"{f.drop_duplicates(['symbol', 'entry_ms']).shape[0]} campaigns) — rows by "
                 f"(scale, kind): " + " · ".join(f"{a}/{b} {int(v)}" for (a, b), v in c.items()))
    bs = ordered(G["NEST_GRID_BY_STATE"], GRID_ORDER + [("state", STATES4 + ("__ALL__",))])
    L += ["", "### Honesty at ENTRY per (book, scale, lens) [L-R.2, AM-4] — the calibrated rows "
          "read a tuning-era pick: in-sample on every tuning-era entry", ""]
    L += _honesty_lines(bs, book_col=True)
    cc = COIN_CATS + ("NA",)
    L += ["", "### Frequency at ENTRY: state x coincidence, per lens (both books, both scales — "
          "calibrated = the scale of record, IN-SAMPLE on tuning-era entries; frozen3.0 = the "
          "causal twin — both coincidence rules)", ""]
    L += md_table(ordered(G["NEST_GRID_FREQ"], GRID_ORDER + [("coin_rule", COIN_RULES),
                                                             ("state", STATES4),
                                                             ("coin_cat", cc)]),
                  ["book", "scale_kind", "lens", "coin_rule", "state", "coin_cat", "n",
                   "n_entries", "share", "n_scale_in_sample", "n_stability_changed",
                   "n_holdout", "lenses_read", "pick_window"])
    L += ["", "### Outcomes by L state at ENTRY (n, E[net R], P(win), ΣR; the HOLDOUT slice "
          "beside — the causal slice of a calibrated read)", ""]
    L += md_table(bs, ["book", "scale_kind", "lens", "state", "n", "mean_net_r", "p_win",
                       "sum_net_r"] + GRID_HONEST_COLS + ["pick_window",
                                                          "stability_changed_members"])
    L += ["", "### Outcomes by coincidence at ENTRY (the HOLDOUT slice beside)", ""]
    L += md_table(ordered(G["NEST_GRID_BY_COIN"],
                          GRID_ORDER + [("coin_rule", COIN_RULES), ("coin_cat", cc)]),
                  ["book", "scale_kind", "lens", "coin_rule", "coin_cat", "n", "mean_net_r",
                   "p_win", "sum_net_r"] + GRID_HONEST_COLS + ["lenses_read", "pick_window",
                                                               "stability_changed_members"])
    return L


R5_DIR_MD_COLS = ["bucket", "n", "n_long", "n_short", "mean_net_r", "p_win", "sum_net_r"]


def r5_direction_md(R5D: pd.DataFrame, on_cut: dict) -> list[str]:
    """[SR-16] the R5 rows read by direction — beside L-R.7's rows, never in their place."""
    L = ["### R5 BY DIRECTION [SR-16; the trading review D-2] — collared Tier-E rows that "
         "DECIDE NOTHING", "",
         "L-R.7's chop table above is direction-blind as frozen and is printed unchanged. A "
         "BULL_EXP / BEAR_EXP row there mixes longs riding the expansion with shorts fading "
         "it, so it can read as a market state when the effect is alignment. The rows below "
         "read the SAME v6 entries (R5_CHOP_DIRECTION.parquet) by alignment and by "
         "direction-adjusted pct-of-range. They gate nothing and are not results.", "",
         collar_line(), "", READINGS[15], "",
         "Entries on a cut (the tercile text read another way would move them) — IN_RANGE "
         "entries whose adjusted pct is exactly 0, 100/3, 200/3 or 100, or lies between a "
         "printed label and its exact cut ([33.33, 100/3) or [200/3, 66.67)): "
         + " · ".join(f"{k} {v['n_on_a_cut']} on a cut, {v['n_between_label_and_cut']} "
                      f"between, of {v['n_in_range']} in range" for k, v in on_cut.items())
         + ".", "",
         "The honesty labels (lenses_read, pick_window, stability-changed members) are the R5 "
         "rows' own for the same lens; every row carries them and the HOLDOUT slice.", ""]
    for kind in SCALE_KINDS:
        for lens in R5_LENSES:
            z = R5D[(R5D["scale_kind"] == kind) & (R5D["lens"] == lens)]
            tag = (" (the scale of record; IN-SAMPLE on the tuning-era entries, the HOLDOUT "
                   "slice beside is the causal one)" if kind == "calibrated"
                   else " (the fully causal twin)")
            for split in R5_DIR_BUCKETS:
                zz = ordered(z[z["split"] == split], [("bucket", R5_DIR_BUCKETS[split])])
                L += [f"#### {lens} · {kind} · {split}{tag}", "",
                      "Law: " + R5_DIR_SPLIT_LAW[split], ""]
                L += md_table(zz, R5_DIR_MD_COLS + GRID_HONEST_COLS)
                L.append("")
    return L


def r5_md(R5: pd.DataFrame, five: pd.DataFrame, R5D: pd.DataFrame | None = None,
          on_cut: dict | None = None) -> list[str]:
    L = ["## R5 · THE CHOP TABLE [L-R.7] — v6 outcomes by 4h / 12h state x %-of-range decile at "
         "entry — Tier-E (printed first in §0)", "", collar_line(), "", READINGS[7], "",
         HONESTY_LAW, ""]
    L += _honesty_lines(ordered(R5, [("scale_kind", SCALE_KINDS), ("lens", R5_LENSES),
                                     ("bucket", R5_BUCKETS)]), book_col=False)
    L.append("")
    for kind in SCALE_KINDS:
        for lens in R5_LENSES:
            z = ordered(R5[(R5["scale_kind"] == kind) & (R5["lens"] == lens)],
                        [("bucket", R5_BUCKETS)])
            a = z[z["bucket"] == "__ALL__"].iloc[0]
            tag = (" (the scale of record — IN-SAMPLE on the tuning-era entries: "
                   f"{int(a['n_scale_in_sample'])} of {int(a['n'])}; stability-changed "
                   f"{a['stability_changed_members']} on {int(a['n_stability_changed'])} "
                   "entries; the HOLDOUT slice beside is the causal one)"
                   if kind == "calibrated" else " (the fully causal twin)")
            L += [f"### {lens} · {kind}{tag}", ""]
            L += md_table(z, ["bucket", "n", "mean_net_r", "p_win", "sum_net_r"]
                          + GRID_HONEST_COLS)
            L.append("")
    if R5D is not None:
        L += r5_direction_md(R5D, on_cut or {})
    L += ["### The anchor: TC10's five-row table (4h, frozen 3.0) beside the TC11 v6 book's own "
          "five rows — all eleven columns [L-R.7, SR-11]", ""]
    fo = ordered(five, [("macro_state_at_entry", TC10_STATES)])
    for tag, what in (("tc11", "the TC11 v6 book (books/v6_campaigns, the TC11 nest)"),
                      ("tc10", "TC10's filed stamps/control_entry_by_state.parquet "
                               "(reproduced exactly on the filed journal)")):
        L += [f"#### {tag}: {what}", ""]
        L += md_table(fo, ["macro_state_at_entry"] + [f"{tag}_{c}" for c in FIVE_ROW_COLS],
                      {f"{tag}_{c}": 6 for c in FIVE_FLOAT_COLS})
        L.append("")
    return L


def continuity_line(R2: pd.DataFrame) -> str:
    z = R2[(R2["toll"] == "taker") & (R2["lens"].isin(TC10_LENSES))
           & R2["tc10_would_read"].notna()]
    out = []
    for (k, e), g in z.groupby(["scale_kind", "era"], sort=True):
        same = ((g["n_ranges"].astype(int) == g["tc10_n_ranges"].astype(int))
                & (g["edge_n"].astype(int) == g["tc10_edge_n"].astype(int))
                & ((g["edge_net_h20"] == g["tc10_edge_net_h20"])
                   | (g["edge_net_h20"].isna() & g["tc10_edge_net_h20"].isna()))
                & (word_any(g) == g["tc10_would_read"]))
        out.append(f"{k}/{e} {int(same.sum())}/{len(g)} rows identical to TC10's")
    return ("taker rows at 5m/4h/1d vs TC10's filed height_toll_verdict (as of "
            "2026-09-21T16:00Z; n_ranges, edge_n, edge net H20, word): " + " · ".join(out)
            + ". The frozen-3.0 tuning era is the like-for-like slice (same bars, same scale); "
              "ALL / holdout add TC11's 3.3 days; TC10's calibrated scale was its whole-tape "
              "pick.")


def findings_not_fixed(V: dict, nests: dict) -> list[str]:
    """[L-R.4] every provisional FAIL among the lens verdicts of record, plus the
    stage's standing disclosures, for the operator."""
    L = []
    prov = [l for l in LENSES11 if V[l]["provisional"]]
    for l in prov:
        v = V[l]
        L.append(f"- R2 {l}: the lens verdict of record is **{v['verdict']}** — PROVISIONAL "
                 f"(a leg under its floor: n_ranges {v['n_ranges']}, edge_n {v['edge_n']}, "
                 f"edge_n_ranges {v['edge_n_ranges']}; floors 30 / 30 / 30). Per the contract a "
                 f"FAIL closes the lens for range trading; a provisional FAIL is listed here for "
                 f"the operator [L-R.4]. Pick window {v['pick_window']}; fallback members "
                 f"{v['fallback_members'] or 'none'}.")
    if not prov:
        L.append("- R2: no lens verdict of record is provisional.")
    L.append("- R3 lanes: the contract's R3 covers every card including the lanes; this build "
             "stamps base v6 and 9/12; the lanes are stamped by the `lanes` subcommand "
             "(stage_r/lanes/: NEST_<REG>.parquet, NEST_GRID_LANES.md, LANES_MANIFEST.json; "
             "SR-15) through the same nest-book door, after the owning stages filed the "
             "named-event instant columns (harvest_close_ms, add1_close_ms / add2_close_ms). The "
             "door still REFUSES (HALT, naming the counts) any regbook whose own record says a "
             "harvest / add / +1R happened with no instant to stamp it [L-R.5 'plus the named "
             "events'].")
    L.append("- R3 / R5 / NEST_GRID calibrated reads are IN-SAMPLE on every tuning-era entry "
             "(SCALE-IN-SAMPLE, L-R.2); each aggregated row prints its in-sample count and the "
             "holdout slice beside [SR-12].")
    L.append("- AM-5 (walk-mismatch bars) does not touch this stage's books: NEST_v6 / "
             "NEST_trg912 read the UNWALKED 4h ride.")
    return L


def lean_block() -> str:
    L = [f"{LEAN_TAG} STAGE R-a (tierc11_stage_r) · substrate {SUBSTRATE} · pin {PIN_ISO} "
         f"({PIN_MS}) · seed {SEED}"]
    L += [f"{LEAN_TAG} {x}" for x in READINGS]
    L.append(f"{LEAN_TAG} RECORD (L-R.4): panel {RECORD['panel']} · era {RECORD['era']} · scale "
             f"{RECORD['scale_kind']} · toll {RECORD['toll']}; tolls {list(TOLLS)}; eras "
             f"{list(ERAS)}; scales {list(SCALE_KINDS)}")
    L.append(f"{LEAN_TAG} INTRABAR_STAMP = {INTRABAR_STAMP!r}")
    return "\n".join(L) + "\n"


# ══════════════════════════════════════════════════════════ 9 · BUILD
OUTPUT_FILES = (
    "R1_LENSES.parquet", "R1_LENSES.md", "R2_FEASIBILITY.parquet", "R2_FEASIBILITY.md",
    "R2_LENS_VERDICTS.json", "NEST_v6.parquet", "NEST_trg912.parquet",
    "NEST_GRID_FREQ.parquet", "NEST_GRID_BY_STATE.parquet", "NEST_GRID_BY_COIN.parquet",
    "NEST_GRID.md", "R5_CHOP.parquet", "R5_CHOP_DIRECTION.parquet", "R5_FIVE_ROW.parquet",
    "R5_CHOP.md", "STAGE_R.md",
    "build_manifest.json", "nestbook_probe/V6-PROBE/base.parquet",
    "nestbook_probe/V6-PROBE/base.json", "nest_books/V6-PROBE__base.parquet",
    "nest_books/V6-PROBE__base.json")
KEYS = {"R1_LENSES": ["asset", "lens"],
        "R2_FEASIBILITY": ["panel", "lens", "era", "scale_kind", "toll"],
        "NEST_v6": ["book"] + NEST_KEY, "NEST_trg912": ["book"] + NEST_KEY,
        "NEST_GRID_FREQ": ["book", "scale_kind", "lens", "coin_rule", "state", "coin_cat"],
        "NEST_GRID_BY_STATE": ["book", "scale_kind", "lens", "state"],
        "NEST_GRID_BY_COIN": ["book", "scale_kind", "lens", "coin_rule", "coin_cat"],
        "R5_CHOP": ["scale_kind", "lens", "bucket"],
        R5_DIR_TABLE: ["scale_kind", "lens", "split", "bucket"],
        "R5_FIVE_ROW": ["macro_state_at_entry"]}


def _inside(p: Path, root: Path) -> bool:
    return p == root or root in p.parents


def _guard_out(out: Path) -> Path:
    """OUT; a direct child of DET_ROOT; or a direct child of a `_det_stage_r/`
    directory OUTSIDE the repo tree (a fixture --root scratch) [the books law]."""
    o = Path(out).resolve()
    if o == OUT.resolve() or o.parent == DET_ROOT.resolve():
        return o
    trees = {ROOT.resolve(), Path(E.MAIN_TREE).resolve()}
    if o.parent.name == DET_ROOT.name and not any(_inside(o, t) for t in trees):
        return o
    _halt(f"output dir {o} is neither {E.rel_of(E._real(OUT))}, an F-DET run dir under "
          f"{DET_ROOT.name}/, nor one under a {DET_ROOT.name}/ scratch outside the repo")
    return o


def build(out: Path = OUT) -> dict:
    out = _guard_out(out)
    W, K = {}, {}
    rec = picks_record()
    grid = read_parquet(N.GRID_PATH)
    if C.content_sha(C.canon(grid, N.GRID_KEY)) != rec["grid_content_sha256"]:
        _halt("SCALE_GRID.parquet content sha != SCALE_PICKS.json's grid_content_sha256")
    bk = books_campaigns()

    # R1 + R2
    t0 = time.perf_counter()
    R1, R2 = compute_r1_r2()
    R1 = put_table(R1, "R1_LENSES", KEYS["R1_LENSES"], out, W, K)
    R2 = put_table(finalize_r2(R2), "R2_FEASIBILITY", KEYS["R2_FEASIBILITY"], out, W, K)
    V = lens_verdicts(R2)
    clock(f"R1+R2 {time.perf_counter() - t0:.1f}s")

    # R3 the nest on the books
    t0 = time.perf_counter()
    nests, entries = {}, {}
    camps = {"v6": bk["v6_campaigns"], "trg912": bk["trg912_campaigns"]}
    for book in BOOKS:
        f = book_nest(camps[book], book)
        nests[book] = put_table(f, f"NEST_{book}", KEYS[f"NEST_{book}"], out, W, K,
                                round_floats=False)
        entries[book] = entry_frame(nests[book], camps[book])
    G = nest_grid(entries)
    for name, d in G.items():
        G[name] = put_table(d, name, KEYS[name], out, W, K)
    # the door, tested on v6
    probe = write_probe(camps["v6"], out, W, K)
    nb = nest_book(probe, "base", "v6transform", out, W, K, sub="nest_books")
    clock(f"R3 {time.perf_counter() - t0:.1f}s")

    # R5 + the anchor
    R5 = put_table(r5_chop(entries["v6"]), "R5_CHOP", KEYS["R5_CHOP"], out, W, K)
    # R5 by direction [SR-16] — beside the unchanged R5 rows, Tier-E, decides nothing
    R5D = put_table(r5_direction(entries["v6"]), R5_DIR_TABLE, KEYS[R5_DIR_TABLE], out, W, K)
    dir_bad = r5_direction_partition(R5, R5D)
    if dir_bad:
        _halt("R5 BY DIRECTION [SR-16] — the rows do not partition against R5_CHOP: "
              + " | ".join(dir_bad[:6]))
    on_cut = r5_direction_on_cut(entries["v6"])
    filed_j = tc10_table(TC10_JOURNAL_REL)
    filed_five = tc10_table(TC10_FIVE_ROW_REL)
    anchor_got = five_row(filed_j)
    anchor_bad = five_row_findings(anchor_got, filed_five)
    if anchor_bad:
        _halt("R5 ANCHOR [L-R.7] — the TC11 nest does not reproduce TC10's five-row table on "
              "the filed control journal: " + " | ".join(anchor_bad[:6]))
    jr = bk["v6_journal"][["asset", "entry_ms", "mfe_r"]]
    v6j = camps["v6"][["symbol", "entry_ms", "net_r"]].rename(columns={"symbol": "asset"}) \
        .merge(jr, on=["asset", "entry_ms"], how="left", validate="1:1")
    tc11_five = five_row(v6j)
    five = five_table(tc11_five, filed_five)
    for k, v in {**COLLAR, **AS_OF}.items():
        five[k] = v
    five = put_table(five, "R5_FIVE_ROW", KEYS["R5_FIVE_ROW"], out, W, K)

    # documents
    r1l = r1_md(R1, grid, rec)
    r2l = r2_md(R2, V)
    nml = nest_md(G, nests)
    r5l = r5_md(R5, five, R5D, on_cut)
    head = [f"as_of_last_closed_4h: {PIN_ISO}", ""]
    put_text("\n".join(head + ["# TIER-C11 · STAGE R · R1 LENSES", ""] + r1l) + "\n",
             out / "R1_LENSES.md")
    put_text("\n".join(head + ["# TIER-C11 · STAGE R · R2 FEASIBILITY", ""] + r2l) + "\n",
             out / "R2_FEASIBILITY.md")
    put_text("\n".join(head + ["# TIER-C11 · STAGE R · R3 NESTING GRID", ""] + nml) + "\n",
             out / "NEST_GRID.md")
    put_text("\n".join(head + ["# TIER-C11 · STAGE R · R5 CHOP", ""] + r5l) + "\n",
             out / "R5_CHOP.md")
    put_json({"law": READINGS[3], "record": RECORD, "disclosure": DISCLOSURE,
              "as_of_last_closed_4h": PIN_ISO, "lenses": V}, out / "R2_LENS_VERDICTS.json")
    books_line = []
    fp = bk["_manifest"]["net_r_sum"]
    for book in BOOKS:
        c = camps[book]
        books_line.append(f"- {book}: n {len(c)} · ΣR {float(c['net_r'].sum()):+.6f} (the sum "
                          f"of the books table's 6-dp rows; full precision {float(fp[book]):+.6f}"
                          f" per books/build_manifest.json) · mean R "
                          f"{float(c['net_r'].mean()):+.6f} (book, not a verdict; "
                          f"books/{book}_campaigns.parquet) [SR-14]")
    fnf = findings_not_fixed(V, nests)
    stage = (head + ["# TIER-C11 · STAGE R-a — ranges done once (R1 · R2 · R3 · R5)", "",
                     "Contract: exchange/queue/2026-09-24_TC11_APOLLO.md (bb38e016…) · readings "
                     "LEANS L-R.1..L-R.5, L-R.7 + AM-1, AM-4, AM-6 · executor HEPHAESTUS · seed "
                     f"{SEED} · substrate {SUBSTRATE}", "",
                     "No registered book is built in Stage R-a. The books read (both TIER-E "
                     "here):", ""] + books_line +
             ["", "## Executor readings of this stage", ""] + [f"- {x}" for x in READINGS] +
             ["", "## §0 lines this stage feeds", "",
              "- R5 chop table (printed first in §0): see R5 below.",
              "- R5 by direction [SR-16; the trading review D-2]: collared Tier-E rows beside "
              "the unchanged R5 rows (alignment; direction-adjusted pct terciles) — they decide "
              "nothing; see R5 below.",
              "- The lens verdicts of record per lens: " + " · ".join(
                  f"{l} **{V[l]['verdict']}**" for l in LENSES11),
              "- Stage S precondition [L-S.1]: the 1h lens verdict of record is "
              f"{V['1h']['verdict']} -> " + ("Stage S runs" if V["1h"]["verdict"] == WORD_PASS
                                             else f"CLOSED BY R2 (1h: {V['1h']['verdict']})")
              + f"; the tuning-era word beside it (Tier-E) is {V['1h']['tier_e_tuning_word']}.",
              "- TC10 continuity [AM-1]: " + continuity_line(R2), ""]
             + ["## Findings not fixed (for the operator) [L-R.4]", ""] + fnf + [""]
             + r5l + [""] + r2l + [""] + r1l + [""] + nml
             + ["", "## The nest-book door (tested on v6)", "",
                f"- probe regbook nestbook_probe/V6-PROBE/base.parquet (book_sha256 "
                f"{nb['book_sha256']}), nest_books/V6-PROBE__base.parquet: {nb['n_rows']} rows, "
                f"content sha {nb['content_sha256']}; rows by kind "
                + json.dumps(nb["n_rows_by_kind"], sort_keys=True), ""])
    put_text("\n".join(stage) + "\n", out / "STAGE_R.md")
    man = {"stage": "TC11-R (R-a: R1 R2 R3 R5)", "tier": "TIER-C11", "seed": SEED,
           "as_of": PIN_ISO, "as_of_close_ms": PIN_MS, "substrate": SUBSTRATE,
           "sha": W, "keys": K, "record": RECORD, "lens_verdicts": {l: V[l]["verdict"]
                                                                    for l in LENSES11},
           "inputs": {"SCALE_PICKS.json": sha_bytes(N.PICKS_PATH.read_bytes()),
                      "SCALE_GRID.content_sha256": rec["grid_content_sha256"],
                      "books_manifest_sha": bk["_manifest"]["sha"],
                      "tc10_records": [TC10_JOURNAL_REL, TC10_FIVE_ROW_REL, TC10_VERDICT_REL]},
           "r5_anchor": {"reproduced": True, "rows": list(TC10_STATES),
                         "columns": list(FIVE_ROW_COLS)},
           "r5_direction": {"reading": "SR-16", "table": R5_DIR_TABLE,
                            "review": "trading review D-2 (research_outputs/tierc11/review/"
                                      "FINAL_REVIEW_2026-09-25.json)",
                            "splits": {k: list(v) for k, v in R5_DIR_BUCKETS.items()},
                            "partition_vs_R5_CHOP": "checked (the build HALTs otherwise)",
                            "entries_on_a_cut": on_cut, **COLLAR},
           "nest_book_probe": {k: nb[k] for k in ("registration", "arm", "kind", "n_campaigns",
                                                  "n_rows", "content_sha256", "book_sha256")},
           "readings": list(READINGS), "collar": COLLAR, "record_collar": RECORD_COLLAR}
    put_json(man, out / "build_manifest.json")
    return {"R1": R1, "R2": R2, "V": V, "nests": nests, "G": G, "R5": R5, "R5D": R5D,
            "five": five, "manifest": man}


# ══════════════════════════════════════════════════════════ 10 · THE LANES PASS [SR-15]
LANES_DIR = "lanes"
LANES_OUT = OUT / LANES_DIR
REGBOOK_ROOT = E.OUT / "regbooks"
SCORE_MANIFEST_PATH = E.OUT / "scores" / "SCORE_MANIFEST.json"
LANE_BOOKS = (("P-WARN-1", "scored", "v6transform"), ("P-AGE-1", "scored", "v6transform"),
              ("P-WIN-1", "scored", "v6transform"), ("P-BRK-4H", "scored", "lane4h"),
              ("P-BRK-4H", "tierE__panel17", "lane4h"), ("P-RELAY-1", "scored", "relay"),
              ("P-ADD-BRK", "scored", "v6transform"), ("P-ADD-SFP", "scored", "v6transform"),
              ("P-TP-RNG", "scored", "v6transform"))              # REGISTRATIONS.json seq order
LANE_REGS = tuple(dict.fromkeys(r for r, _, _ in LANE_BOOKS))
LANE_LABELS = tuple(f"{r}/{a}" for r, a, _ in LANE_BOOKS)
LANES_KEYS = {**{f"NEST_{r}": ["arm"] + NEST_KEY for r in LANE_REGS},
              "NEST_GRID_LANES_FREQ": ["book", "scale_kind", "lens", "coin_rule", "state",
                                       "coin_cat"],
              "NEST_GRID_LANES_BY_STATE": ["book", "scale_kind", "lens", "state"],
              "NEST_GRID_LANES_BY_COIN": ["book", "scale_kind", "lens", "coin_rule", "coin_cat"]}
LANES_MANIFEST = "LANES_MANIFEST.json"
LANES_MD = "NEST_GRID_LANES.md"
STATES5 = STATES4 + ("NA",)
EXIT_NAMES = {"stop": "exit: stop", "tp": "TP fill", "target": "TP fill"}


def named_event(kind: str, reason: str, nest_kind: str) -> str:
    """SR-15: the L-R.5 name of an instant row (the door's instant_kind + the exit reason)."""
    if kind == "exit" or kind == "exit_post_event":
        base = (EXIT_NAMES.get(reason) or ("warn exit" if reason.startswith("warn") else
                                           f"exit: {reason}"))
        return base if kind == "exit" else f"{base} (post-event twin)"
    return {"bar_close": "bar_close", "arm": "arm",
            "entry": "relay_entry" if nest_kind == "relay" else "entry",
            "plus_1r": "+1R", "plus_1r_post_event": "+1R (post-event twin)",
            "harvest": "harvest", "add1": "add", "add2": "add", "bell": "bell",
            "as_of_pin": "open at the pin"}.get(kind, kind)


def _score_inputs() -> dict:
    man = json.loads(SCORE_MANIFEST_PATH.read_text(encoding="utf-8"))
    return {k: v.get("book_sha256") for k, v in man["inputs"].items()}


def lane_book(reg: str, arm: str, kind: str, scored: dict) -> tuple[pd.DataFrame, dict,
                                                                    pd.DataFrame]:
    """One lane book through the nest-book door [SR-9, SR-15]: (nest frame, sidecar
    entry, the regbook)."""
    regdir = REGBOOK_ROOT / reg
    raw = (regdir / f"{arm}.parquet").read_bytes()
    df, meta = read_regbook(regdir, arm)
    if sha_bytes((regdir / f"{arm}.parquet").read_bytes()) != sha_bytes(raw):
        _halt(f"lanes: {reg}/{arm}.parquet changed while it was read")
    content = C.content_sha(df)                 # before the door reads it
    want = scored.get(f"{reg}/{arm}")
    if want != meta["book_sha256"]:
        _halt(f"lanes: {reg}/{arm} book_sha256 {meta['book_sha256'][:12]}… is not the book the "
              f"scorer scored ({str(want)[:12]}… in scores/SCORE_MANIFEST.json)")
    if df.duplicated(subset=["symbol", "entry_ms"]).any():
        _halt(f"lanes: {reg}/{arm} (symbol, entry_ms) is not unique")
    inst, src = instants_of(df, kind)
    f = nest_frame(inst)
    x = f.merge(df[["symbol", "entry_ms", "exit_reason"]], on=["symbol", "entry_ms"],
                how="left", validate="m:1")
    if x["exit_reason"].isna().any() or len(x) != len(f):
        _halt(f"lanes: {reg}/{arm}: an instant row joins no campaign")
    f["exit_reason"] = x["exit_reason"].astype(str).to_numpy()
    f["named_event"] = [named_event(k, r, kind) for k, r in
                        zip(f["instant_kind"], f["exit_reason"])]
    f.insert(1, "registration", reg)
    f.insert(2, "arm", arm)
    cal = f[f["scale_kind"] == SCALE_KINDS[0]]
    side = {"registration": reg, "arm": arm, "kind": kind, "campaign_lens": KINDS[kind]["lens"],
            "source_regbook": E.rel_of(E._real(regdir)) + f"/{arm}.parquet",
            "book_sha256": meta["book_sha256"], "book_sha256_is_the_scored_input": True,
            "sidecar_file_sha256": sha_bytes((regdir / f"{arm}.json").read_bytes()),
            # the regbook bytes STAMPED (book_sha256 covers the 16 required columns only,
            # not the instant columns the nest reads) [SR-15; verifier MINOR-4]
            "regbook_content_sha256": content, "regbook_file_sha256": sha_bytes(raw),
            "panel": list(meta.get("panel", [])), "n_campaigns": int(len(df)),
            "n_rows": int(len(f)),
            "n_rows_by_kind_per_scale": {k: int(v) for k, v in
                                         cal.groupby("instant_kind").size().items()},
            "named_events_per_scale": {k: int(v) for k, v in
                                       cal.groupby("named_event").size().items()},
            "event_sources": src}
    return f, side, df


def _na_state(v) -> str:
    return "NA" if (v is None or (isinstance(v, float) and np.isnan(v)) or v is pd.NA) \
        else str(v)


def lane_coin_cat(top, bot, lens: str) -> np.ndarray:
    """SR-7 with the twelve's NA: a lens whose own or L+1 bundle is absent -> 'NA'."""
    if lens == "1w":
        return np.array(["NA"] * len(top), dtype=object)
    t = pd.array(top, dtype="boolean")
    b = pd.array(bot, dtype="boolean")
    na = np.asarray(t.isna() | b.isna(), dtype=bool)
    tv = np.asarray(t.fillna(False), dtype=bool)
    bv = np.asarray(b.fillna(False), dtype=bool)
    out = np.where(tv & bv, "both", np.where(tv, "top", np.where(bv, "bot", "none")))
    return np.where(na, "NA", out).astype(object)


def lane_decl(panel: list, lens: str) -> tuple[tuple, tuple]:
    """The declared (states, coincidence categories) of a book x lens [SR-15]."""
    lack = any(lens not in N.LENSES_OF[s] for s in panel)
    up = N.LADDER[lens]
    lack_up = up is not None and any(up not in N.LENSES_OF[s] for s in panel)
    states = STATES5 if lack else STATES4
    coins = ("NA",) if lens == "1w" else (COIN_CATS + ("NA",) if (lack or lack_up)
                                          else COIN_CATS)
    return states, coins


def lane_labels(z: pd.DataFrame, lenses: tuple) -> dict:
    """SR-12's labels over one (book, scale)'s entries, NA lenses skipped."""
    isin = np.zeros(len(z), bool)
    stab = np.zeros(len(z), bool)
    pw, sm = [], []
    for c in lenses:
        isin |= _bool_col(z, f"{c}_scale_in_sample")
        sc = _bool_col(z, f"{c}_stability_changed")
        stab |= sc
        w = sorted({str(x) for x in z[f"{c}_pick_window"] if x is not None and not pd.isna(x)})
        pw.append(f"{c}: " + (" / ".join(w) if w else "NA"))
        mem = sorted(set(z.loc[sc, "symbol"].astype(str)),
                     key=lambda x: (PANEL17.index(x) if x in PANEL17 else 99, x))
        sm.append(f"{c}: " + (",".join(mem) if mem else "none"))
    return {"lenses_read": "+".join(lenses), "pick_window": "; ".join(pw),
            "stability_changed_members": "; ".join(sm), "_isin": isin, "_stab": stab}


def lane_entries(f: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:
    e = f[f["instant_kind"] == "entry"]
    j = e.merge(df[["symbol", "entry_ms", "net_r"]], on=["symbol", "entry_ms"], how="left",
                validate="m:1")
    if j["net_r"].isna().any() or len(j) != len(SCALE_KINDS) * len(df):
        _halt("lanes: entry rows do not cover every campaign at both scales")
    j["era"] = E.era_of(j["entry_close_ms"].to_numpy(np.int64)).astype(str)
    return j


def lane_grid(entries: dict, panels: dict) -> dict:
    """The nesting grid at ENTRY per lane book, WHOLE [SR-7, SR-12, SR-15]."""
    freq, bys, byc = [], [], []
    for book in LANE_LABELS:
        j = entries[book]
        for kind in SCALE_KINDS:
            z = j[j["scale_kind"] == kind].reset_index(drop=True)
            n_all = len(z)
            net = z["net_r"].to_numpy(float)
            hold = (z["era"] == "holdout").to_numpy(bool)
            for L in NEST_LENSES:
                states, ccs = lane_decl(panels[book], L)
                st = np.array([_na_state(v) for v in z[f"{L}_state"]], dtype=object)
                bad = sorted(set(st) - set(states))
                if bad:
                    _halt(f"lanes: {book} {kind} {L}: undeclared state(s) {bad}")
                cats = {"record": lane_coin_cat(z[f"{L}_coin_top"], z[f"{L}_coin_bot"], L),
                        "mem_twin": lane_coin_cat(z[f"{L}_coin_top_mem"],
                                                  z[f"{L}_coin_bot_mem"], L)}
                for rule, cc in cats.items():
                    bad = sorted(set(cc) - set(ccs))
                    if bad:
                        _halt(f"lanes: {book} {kind} {L} {rule}: undeclared category {bad}")
                lc = lane_labels(z, _lenses_read(L, coin=True))
                ls = lane_labels(z, _lenses_read(L, coin=False))
                labc = {k: v for k, v in lc.items() if not k.startswith("_")}
                labs = {k: v for k, v in ls.items() if not k.startswith("_")}
                for rule in COIN_RULES:
                    cc = cats[rule]
                    for s4 in states:
                        for c in ccs:
                            m = (st == s4) & (cc == c)
                            freq.append({"cell": f"{book}|{kind}|{L}|{rule}|{s4}|{c}",
                                         "book": book, "scale_kind": kind, "lens": L,
                                         "coin_rule": rule, "state": s4, "coin_cat": c,
                                         "n": int(m.sum()), "n_entries": n_all,
                                         "share": float(m.sum()) / n_all if n_all else np.nan,
                                         "n_scale_in_sample": int(lc["_isin"][m].sum()),
                                         "n_stability_changed": int(lc["_stab"][m].sum()),
                                         "n_holdout": int(hold[m].sum()), **labc})
                    for c in ccs:
                        m = cc == c
                        byc.append({"cell": f"{book}|{kind}|{L}|{rule}|{c}", "book": book,
                                    "scale_kind": kind, "lens": L, "coin_rule": rule,
                                    "coin_cat": c,
                                    **_cell(net[m], lc["_isin"][m], lc["_stab"][m], hold[m]),
                                    **labc})
                for s4 in states + ("__ALL__",):
                    m = np.ones(len(st), bool) if s4 == "__ALL__" else st == s4
                    bys.append({"cell": f"{book}|{kind}|{L}|{s4}", "book": book,
                                "scale_kind": kind, "lens": L, "state": s4,
                                **_cell(net[m], ls["_isin"][m], ls["_stab"][m], hold[m]),
                                **labs})
    out = {}
    for name, rows in (("NEST_GRID_LANES_FREQ", freq), ("NEST_GRID_LANES_BY_STATE", bys),
                       ("NEST_GRID_LANES_BY_COIN", byc)):
        d = pd.DataFrame(rows)
        for k, v in {**COLLAR, **AS_OF}.items():
            d[k] = v
        out[name] = d
    return out


LANE_ORDER = [("book", LANE_LABELS), ("scale_kind", SCALE_KINDS), ("lens", NEST_LENSES)]


def lane_facts(G: dict) -> list[str]:
    """One line per book: the 4h and 12h state at entry (calibrated, the record; frozen
    beside) — the lane nest's headline distribution."""
    bs = G["NEST_GRID_LANES_BY_STATE"]
    L = []
    for book in LANE_LABELS:
        parts = []
        for kind in SCALE_KINDS:
            for lens in ("4h", "12h"):
                z = bs[(bs["book"] == book) & (bs["scale_kind"] == kind) & (bs["lens"] == lens)
                       & (bs["state"] != "__ALL__")]
                parts.append(f"{kind} {lens} " + " / ".join(
                    f"{r['state']} {int(r['n'])}" for _, r in ordered(
                        z, [("state", STATES5)]).iterrows() if int(r["n"]) or r["state"] != "NA"))
        L.append(f"- {book}: " + " · ".join(parts))
    return L


def lanes_md(G: dict, sides: dict) -> list[str]:
    head = [f"as_of_last_closed_4h: {PIN_ISO}", "",
            "# TIER-C11 · STAGE R · R3 THE NEST ON THE LANES — the nesting grid at entry per "
            "lane book [contract R3; L-R.5, AM-6, SR-15] — Tier-E", "", collar_line(), "",
            READINGS[14], "", READINGS[5], "", READINGS[6], "", READINGS[8], "", HONESTY_LAW, "",
            "Stamp laws differ by book and each row's `stamp_law` names its rule: the 4h rides "
            "without a 1h walk (P-AGE-1, P-WIN-1, P-BRK-4H, P-TP-RNG; P-WARN-1's +1R) stamp +1R "
            "/ a stop / a TP fill at the OPEN of their 4h bar; the 1h-walked books (P-RELAY-1, "
            "P-ADD-BRK, P-ADD-SFP; P-WARN-1's exits) at the close of the resolving 1h child "
            "(a parent-decided event on a walk-mismatch bar at the parent's OPEN) — both lawful "
            "under L-R.5. One twin law for all: an intrabar event (+1R, a stop, a TP fill) "
            "stamped before the close of its 4h bar carries one post-event twin at that close "
            "(the relay's exit bar close = exit_bar_close_ms); a stamp that is itself the 4h "
            "close (the bar's last 1h child) carries none; close events carry none.", "",
            "## The lane books", ""]
    L = list(head)
    for book in LANE_LABELS:
        sd = sides[book]
        L.append(f"- **{book}** ({sd['kind']}, lens {sd['campaign_lens']}; "
                 f"{len(sd['panel'])} assets): n {sd['n_campaigns']} campaigns · "
                 f"{sd['n_rows']} nest rows (both scales) · book_sha256 "
                 f"{sd['book_sha256'][:16]}… (== the scorer's input) · regbook stamped: "
                 f"content {sd['regbook_content_sha256'][:16]}… / file "
                 f"{sd['regbook_file_sha256'][:16]}… · instants per scale: "
                 + " · ".join(f"{k} {v}" for k, v in sd["n_rows_by_kind_per_scale"].items())
                 + " · named events per scale: "
                 + " · ".join(f"{k} {v}" for k, v in sd["named_events_per_scale"].items()
                              if k != "bar_close"))
        L.append("  - event sources: " + "; ".join(f"{k} = {v}" for k, v in
                                                   sd["event_sources"].items()))
    L += ["", "## The 4h / 12h state at ENTRY per lane (n; calibrated = the scale of record, "
          "IN-SAMPLE on tuning-era entries; frozen3.0 = the causal twin)", ""]
    L += lane_facts(G)
    bs = ordered(G["NEST_GRID_LANES_BY_STATE"], LANE_ORDER + [("state", STATES5 +
                                                              ("__ALL__",))])
    L += ["", "### Honesty at ENTRY per (book, scale, lens) [L-R.2, AM-4]", ""]
    L += _honesty_lines(bs, book_col=True)
    cc = COIN_CATS + ("NA",)
    L += ["", "### Frequency at ENTRY: state x coincidence, per lens (every lane book, both "
          "scales, both coincidence rules) — WHOLE", ""]
    L += md_table(ordered(G["NEST_GRID_LANES_FREQ"],
                          LANE_ORDER + [("coin_rule", COIN_RULES), ("state", STATES5),
                                        ("coin_cat", cc)]),
                  ["book", "scale_kind", "lens", "coin_rule", "state", "coin_cat", "n",
                   "n_entries", "share", "n_scale_in_sample", "n_stability_changed",
                   "n_holdout", "lenses_read", "pick_window"])
    L += ["", "### Outcomes by L state at ENTRY (n, E[net R], P(win), ΣR — the book's own "
          "net_r; the HOLDOUT slice beside) — WHOLE", ""]
    L += md_table(bs, ["book", "scale_kind", "lens", "state", "n", "mean_net_r", "p_win",
                       "sum_net_r"] + GRID_HONEST_COLS + ["pick_window",
                                                          "stability_changed_members"])
    L += ["", "### Outcomes by coincidence at ENTRY (the HOLDOUT slice beside) — WHOLE", ""]
    L += md_table(ordered(G["NEST_GRID_LANES_BY_COIN"],
                          LANE_ORDER + [("coin_rule", COIN_RULES), ("coin_cat", cc)]),
                  ["book", "scale_kind", "lens", "coin_rule", "coin_cat", "n", "mean_net_r",
                   "p_win", "sum_net_r"] + GRID_HONEST_COLS + ["lenses_read", "pick_window",
                                                               "stability_changed_members"])
    return L


def _guard_lanes(out: Path) -> Path:
    """stage_r/lanes (the record); a direct child of DET_ROOT; or a direct child of a
    `_det_stage_r/` directory OUTSIDE the repo tree (a fixture scratch)."""
    o = Path(out).resolve()
    if o == LANES_OUT.resolve() or o.parent == DET_ROOT.resolve():
        return o
    trees = {ROOT.resolve(), Path(E.MAIN_TREE).resolve()}
    if o.parent.name == DET_ROOT.name and not any(_inside(o, t) for t in trees):
        return o
    _halt(f"lanes --out-dir {o} is neither {E.rel_of(E._real(LANES_OUT))}, a run dir under "
          f"{DET_ROOT.name}/, nor one under a {DET_ROOT.name}/ scratch outside the repo")
    return o


def lanes(out: Path = LANES_OUT, books=LANE_BOOKS) -> dict:
    """THE LANES PASS [SR-15]: every lane book through the nest-book door, both scales;
    NEST_<REG>.parquet (+ .json), the lane nesting grid whole, NEST_GRID_LANES.md,
    LANES_MANIFEST.json."""
    out = _guard_lanes(out)
    W, K = {}, {}
    scored = _score_inputs()
    nests, sides, entries, panels, regs = {}, {}, {}, {}, {}
    for reg, arm, kind in books:
        f, side, df = lane_book(reg, arm, kind, scored)
        label = f"{reg}/{arm}"
        nests.setdefault(reg, []).append(f)
        sides[label] = side
        panels[label] = side["panel"] or sorted(set(df["symbol"]))
        entries[label] = lane_entries(f, df)
        regs[label] = df
    written = {}
    for reg in dict.fromkeys(r for r, _, _ in books):
        d = pd.concat(nests[reg], ignore_index=True)
        written[reg] = put_table(d, f"NEST_{reg}", LANES_KEYS[f"NEST_{reg}"], out, W, K,
                                 round_floats=False)
        arms = [a for r, a, _ in books if r == reg]
        put_json({"registration": reg, "arms": {a: sides[f"{reg}/{a}"] for a in arms},
                  "key": LANES_KEYS[f"NEST_{reg}"], "scales": list(SCALE_KINDS),
                  "content_sha256": W[f"NEST_{reg}"], "law": READINGS[14], **COLLAR, **AS_OF,
                  "source_script": "scripts/tierc11_stage_r.py lanes"},
                 out / f"NEST_{reg}.json")
    G = lane_grid(entries, panels)
    for name, d in G.items():
        G[name] = put_table(d, name, LANES_KEYS[name], out, W, K)
    md = put_text("\n".join(lanes_md(G, sides)) + "\n", out / LANES_MD)
    man = {"stage": "TC11-R (R3 lanes)", "tier": "TIER-C11", "seed": SEED, "as_of": PIN_ISO,
           "as_of_close_ms": PIN_MS, "substrate": SUBSTRATE, "sha": W, "keys": K,
           "books": {b: {k: v for k, v in sides[b].items() if k != "event_sources"}
                     for b in sides},
           "event_sources": {b: sides[b]["event_sources"] for b in sides},
           "inputs": {"SCALE_PICKS.json": sha_bytes(N.PICKS_PATH.read_bytes()),
                      "scores/SCORE_MANIFEST.json": sha_bytes(SCORE_MANIFEST_PATH.read_bytes())},
           "md_sha256": sha_bytes(md), "readings": [READINGS[14], READINGS[8], READINGS[5]],
           "collar": COLLAR}
    put_json(man, out / LANES_MANIFEST)
    return {"nests": written, "sides": sides, "G": G, "manifest": man, "entries": entries}


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    cmd = args[0] if args and not args[0].startswith("--") else "lean"
    if cmd == "build":
        out = next((a.split("=", 1)[1] for a in args if a.startswith("--out-dir=")), None)
        t0 = time.perf_counter()
        R = build(OUT if out is None else Path(out))
        clock(f"build wall {time.perf_counter() - t0:.1f}s")
        for l in LENSES11:
            sys.stdout.write(f"R2 {l}: {R['V'][l]['verdict']}\n")
        return 0
    if cmd == "lanes":
        out = next((a.split("=", 1)[1] for a in args if a.startswith("--out-dir=")), None)
        t0 = time.perf_counter()
        R = lanes(LANES_OUT if out is None else Path(out))
        clock(f"lanes wall {time.perf_counter() - t0:.1f}s")
        for b, sd in R["sides"].items():
            sys.stdout.write(f"{b}: n {sd['n_campaigns']} · rows {sd['n_rows']} · "
                             + json.dumps(sd["named_events_per_scale"], sort_keys=True) + "\n")
        return 0
    if cmd == "nest-book":
        def opt(name: str, default=None):
            for i, a in enumerate(args):
                if a == name and i + 1 < len(args):
                    return args[i + 1]
                if a.startswith(name + "="):
                    return a.split("=", 1)[1]
            return default
        regdir, arm, kind = opt("--regbook"), opt("--arm", "scored"), opt("--kind")
        if not regdir or not kind:
            _halt("nest-book needs --regbook DIR and --kind {"
                  + ",".join(KINDS) + "}")
        out = Path(opt("--out", str(OUT / "nest_books"))).resolve()
        trees = {ROOT.resolve(), Path(E.MAIN_TREE).resolve()}
        if not _inside(out, OUT.resolve()) and any(_inside(out, t) for t in trees):
            _halt(f"nest-book --out {out} must lie under {E.rel_of(E._real(OUT))} or outside "
                  f"the repo (a scratch) — Stage R writes no other stage's files")
        side = nest_book(Path(regdir), arm, kind, out)
        sys.stdout.write(json.dumps({k: side[k] for k in ("registration", "arm", "kind",
                                                          "n_campaigns", "n_rows",
                                                          "content_sha256")}) + "\n")
        return 0
    sys.stdout.write(lean_block())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
