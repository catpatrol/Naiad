#!/usr/bin/env python
"""TIER-C11 · STAGE W — EARLY WARNINGS FROM THE 1H CROSSES [LEANS L-W.0..L-W.6,
L-1.5; AMENDMENTS AM-3, AM-5, AM-6, AM-7].

Contract of record: exchange/queue/2026-09-24_TC11_APOLLO.md (sha256 bb38e016…,
STEP Q b9ed953), STAGE W.  Executor HEPHAESTUS; seed 20260924 (sensitivity
20260816), N_BOOT 4000.  Registration: P-WARN-1 (REGISTRATIONS.json seq 1,
payload sha c6121ba9…), CONDITIONAL, paired vs v6.

A RUNNER, RANGE-FREE: it imports tierc11_books (B) and tierc11_ride (RD), both
through tierc11_env (E, the range-free shim).  Stage W reads no range fact, so it
never imports tierc11_nest.  Parquet is read and written only through pandas on
path strings [AM-2]; no subprocess here (the F-DET harness lives in the fixtures).

WHAT IT BUILDS
  research_outputs/tierc11/stage_w/
    W1_EVENTS.parquet        every 1h engine-EMA-of-close cross 9/12, 12/26, 12/89
                             inside each v6 campaign's window (arm close, exit-bar
                             close], classified [L-W.2, L-W.3]; key (symbol,
                             entry_ms, pair, h1_open_ms); `recross_strict` (w10).
    W1_TIMELINE.parquet      each campaign's 4h timeline stamped with the 1h events
                             VISIBLE at each 4h close (close <= the 4h close) [L-W.1];
                             key (symbol, entry_ms, bar_close_ms).
    W1_CAMPAIGNS.parquet     one row per v6 campaign: the 1h-resolved exit, the two
                             +1R latch readings, cohort memberships, first events, the
                             forward-leg marks, the relay cross, the rule book's exit;
                             v6's and the rule book's net R each with its AM-7
                             haircut twin beside (haircut_net_r, rule_haircut_net_r).
    W2_COHORTS.parquet       the four post-entry cohorts (+ C3S, the strict re-cross
                             reading printed beside C3, w10) vs their AT-RISK sets, the
                             complement beside, per era [L-W.4].  Tier-E, whole.
    W2_FORWARD.parquet       each post-entry cohort's forward leg E[final net R − R
                             marked at the event's 1h close] [L-W.4].  Tier-E, whole.
    W2_PREENTRY.parquet      the four PRE-ENTRY event classes in (arm close, entry
                             close] vs the whole book, complement beside [L-W.4].
    W2_RELAY_WINDOWS.parquet the relay evidence per v6 window [L-W.6].
    W2_RELAY_WINDOWS_TWIN.parquet the rival population: every ARMED window of v6's
                             card (tide + displacement gates passed) holding no v6
                             campaign (no 4h trigger, or triggered and not entered) —
                             a Tier-E twin (sub-reading w7).
    W2_RELAY_SUMMARY.parquet share and lead distribution summaries, whole.
    W2_RELAY_HIST.parquet    the lead distributions binned, whole.
    P_WARN_1_COMPLEMENT.parquet  the complement comparison (Tier-E arm of P-WARN-1).
    MANIFEST_STAGE_W.json, STAGE_W.md
  research_outputs/tierc11/regbooks/P-WARN-1/
    <arm>.parquet + <arm>.json for: the rule book (scored iff the condition is MET,
    else tierE__rule_book_condition_not_met), base (v6, the paired key set),
    tierE__tuning, tierE__holdout; condition.json; STATUS.json.

THE READINGS BUILT (LEANS, quoted by id; the frozen text governs)
  L-W.0  the 1h walk law — RD.walk_of / RD.ride11(walk=) (foundation, untouched).
  L-W.1  a 1h bar is visible at a 4h decision instant iff its close <= that close
         (`visible`, `first_visible`).
  L-W.2  1h EMA-of-close crosses 9/12, 12/26, 12/89 by the ENGINE EMA
         (RD.cross_1h = engine.indicators.ema + crossover/crossunder), each known at
         the 1h close where the fast line changes side; with/against relative to
         the campaign direction.
  L-W.3  +1R latch = the first 1h child after the entry close whose high (low)
         reaches entry ± R (RD's `plus1r_1h_ms`; a mismatch bar: the parent decides);
         the 1h-RESOLVED exit (RD's `exit_close_ms`: the stop child's close; a
         bell / corridor_end at its 4h close; a mismatch-bar stop at the parent's
         close); IN-TRADE = close > entry close and strictly before that exit (the
         stop child excluded); PRE-ENTRY = arm close < close <= entry close; before
         +1R = index < the latch index (no latch: any in-trade cross); after +1R =
         index >= the latch index.
  L-W.4  cohorts vs AT-RISK sets, complement beside; the forward leg; the P-WARN-1
         condition by T5.cluster_boot_diff(cohort, whole book, seed 20260924,
         n_boot 4000) + T5._ci_from, MET iff the cluster-90% hi < 0 (the
         sensitivity seed 20260816 printed beside, deciding nothing).
  L-W.5  the rule book = RD.transform_book(v6, walk=True, warn_of=RD.warn_of) —
         per child STOP -> +1R latch -> at the close, pre-+1R counter 12/89 cross:
         exit at that 1h close; v6's BELL/HARVEST/TRAIL at 4h closes unchanged.
  L-W.6  per v6 window the first 1h with-trend 12/26 cross with arm close < close <
         the 4h trigger close; share and lead (1h bars, 4h bars), distribution whole.
  L-1.5  the paired book keeps v6's set; identity law asserted (RD.identity_findings)
         on every campaign the rule never acted on (0.000e+00 on net_r and exit_ms,
         exit_reason equal); a freed slot admits nothing (the re-ride rival is a
         disclosure count).
  AM-5   the mismatch-bar look-ahead disclosure; each book prints its mismatch count.
  AM-6   the two +1R latch readings are both output; they are compared here.
  AM-7   haircut_net_r = net_r − fee_r × slip_bps_side / taker_bps_side, with the
         stem's charter tier from E.fees().

EXECUTOR SUB-READINGS (Stage W; where the frozen text is silent — each disclosed,
never re-chosen after a number):
  (w1) AN EVENT ON A MISMATCH BAR IS TAKEN AT THE PARENT'S CLOSE for every
       comparison (L-W.0: "1h-only events on that bar (warn cross …) are taken at
       the parent's close"): `taken_ms` = the 1h close on a walkable bar, else the
       parent 4h close; the raw 1h close is kept beside (`close_ms`) and the count
       of classifications that the raw instant would change is printed.
  (w2) The W1 window of a campaign is (arm close, exit-bar close]: phases
       PRE-ENTRY, IN-TRADE, AT-EXIT (taken == the 1h-resolved exit: the stop
       child, or a cross closing at a bell / corridor_end close), POST-EXIT (after
       the exit, inside the exit bar) — every event classified, none dropped.
  (w3) The cohort latch is L-W.3's reading (`plus1r_1h_ms`); L-W.5's (`latch_1h_ms`,
       stop before latch on one child) is carried beside and their agreement
       printed [AM-6].
  (w4) A campaign is IN a cohort iff it holds >= 1 event of the class; the forward
       leg uses the FIRST such event (the one a rule would act on).
  (w5) THE MARK at an event = the campaign's net R had it exited at the event's
       taken instant at the tape's price there (the 1h close; the parent close on a
       mismatch bar), booked by tierc7._account_chain (RD.account11) with v6's band
       harvest only if the harvest bar precedes the event's 4h bar (a harvest at
       the same close is pre-empted, as the ride's intrabar-before-close order
       does), no adds; fees, funding and the D12 ceiling as the ride books them.
       For the P-WARN-1 cohort this IS the rule book's net R (asserted).
  (w6) AT-RISK sets (L-W.4): "before +1R" cohorts -> the whole v6 book; "after
       +1R" -> the campaigns that reached +1R (L-W.3 latch present); "9/12
       re-cross after entry" -> the campaigns still open 1h after entry: the
       1h-resolved exit strictly after entry close + 1h.
  (w7) "every v6 window" (L-W.6) = the v6 campaign set's windows (arm -> the 4h
       trigger that entered, the trigger close = the entry close).  A lag-0 window
       holds no 1h close strictly inside and counts as "no relay cross".  The rival
       population printed beside as a Tier-E twin = every ARMED window of v6's card
       (T9.card_candidates9 over replay9's bounds, tide and displacement gates
       passed) that holds NO v6 campaign: one that triggered and was not entered
       (end = its trigger close) or one that never triggered (end = its window
       close, the counter 12/89 4h cross, when that cross closed by the as-of —
       B.known_window_end — else the as-of close); the relay cross there is the
       first 1h with-trend 12/26 cross with arm close < taken < that end.  lead_1h =
       (window end − taken instant) / 1h; lead_4h = (window end − the first 4h close
       at which the cross is visible, L-W.1) / 4h (0 = visible only at the end's
       own close).  (The first build read the twin as "every triggered candidate
       window of v6's card, admission ignored"; see CHANGES AFTER FIRST OUTPUT, CH-1.)
  (w8) P(win) = share with net_r > 0; era = E.era_of(entry close) [L-1.3]; a bar
       straddling the era cut (open <= cut < close) is printed as a count (the
       regbook sidecars, STAGE_W.md).
  (w9) The condition block also prints the rival reading (cohort vs its
       COMPLEMENT, the TC7 lab `_stat` reading) with its interval — deciding nothing.
  (w10) C3 "1h 9/12 re-cross with trend after entry" (contract W2; L-W.4's "9/12
       re-cross after entry") is read as ANY in-trade with-trend 1h 9/12 cross: the
       fast line crossing back to the trade's side IS a re-cross of the 9/12.  This
       reading was built into the first output and is not changed; it was not
       disclosed there (verifier finding 5), so it is stated here.  The STRICT
       reading — a with-trend cross whose immediately preceding 9/12 cross on the
       asset's 1h tape (by 1h index, either direction) is a counter cross closing
       AFTER the entry close, i.e. the first with-trend cross is dropped when the
       9/12 was counter-side at the entry close — is printed BESIDE as cohort C3S
       (W1_EVENTS.recross_strict), Tier-E, deciding nothing.
  (w11) AM-7's haircut twin is printed beside every per-campaign net R of the
       stage's tables (W1_CAMPAIGNS: haircut_net_r / rule_haircut_net_r with fee_r
       / rule_fee_r; W2_RELAY_WINDOWS: haircut_net_r) and beside the complement
       table's sums (sum_v6_haircut_r / sum_rule_haircut_r).  The forward-leg marks
       stay net R (a mark is a hypothetical exit, not a trade row).

CHANGES AFTER FIRST OUTPUT (disclosed; no net_r, cohort, condition number or
registered figure moved by either; printed in STAGE_W.md and the manifest):
  CH-1 (w7) the twin population.  First built as "every triggered candidate window
       of v6's card, admission ignored".  On this corridor that population IS the
       v6 campaign set (the 200 triggered gate-passing windows == the 200 v6
       windows; no trigger was refused by an open position — relay_twin_check), so
       the twin duplicated the population it was meant to stand beside.  Rebuilt
       as the armed windows holding no v6 campaign.  Tier-E; gates nothing.
  CH-2 the regbook's exit_close_ms.  First built as the 1h-RESOLVED exit instant;
       changed to the CLOSE of the 4h exit bar — the estate's v6 schema
       (books/v6_campaigns.parquet), which the scorer's SC-7 F-BASE-IDENT compares
       on the base arm column by column — with the exact 1h instant kept as the
       extra column exit_instant_ms (EXIT_CLOSE_LAW).  Only that column (and so
       the book_sha256) moved; net_r / gross_r / fee_r / funding_r did not.
  (The builder's first-output files are not on disk; both changes are stated from
  the code's own law texts and the Stage W verifier's report, finding 2.)

WHAT WOULD MAKE THIS WRONG: classifying at the 4h exit-bar close (a cross after the
stop child would count in-trade — F-WARN-ASOF); reading a 1h bar that closes after
the 4h instant (F-WARN-ASOF); admitting pre-entry crosses into a post-entry cohort
(F-WARN-COHORT); a cohort latch that disagrees with the walk; a rule book that moves
an untouched campaign (F-IDENTITY); printing a verdict word on a Tier-E row.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_w.py              # canonical build
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_w.py --out-dir=DIR  # F-DET twin
      (DIR must be a direct child of research_outputs/tierc11/stage_w/_det_stage_w/,
       or of a `_det_stage_w/` directory OUTSIDE the repo tree)
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_books as B                   # noqa: E402  (imports tierc11_env: guards + shim + hook)
import tierc11_ride as RD                   # noqa: E402

import numpy as np                          # noqa: E402
import pandas as pd                         # noqa: E402

E = B.E
TP, T9, T7, T5, TB = E.TP, E.T9, E.T7, E.T5, E.TB
iso = TB.iso

# ══════════════════════════════════════════════════════════ CONSTANTS OF RECORD
PIN_MS = E.PIN_MS                           # 2026-09-25T00:00:00Z [L-0.1]
PIN_ISO = "2026-09-25T00:00:00Z"
SEED = 20260924                             # passed explicitly [L-0.3]
SEED_SENS = 20260816
N_BOOT = 4000
MS_1H = 3_600_000
MS_4H = 14_400_000
CARD, ROLES = TP.CONTROL_CARD, T9.V6_ROLES
REG = "P-WARN-1"
REG_PAYLOAD_SHA = "c6121ba9330a40bd31fd0dd1f78303b940417d3ac1f3a9eba8750979f84f0c99"
WARN_LABEL = RD.WARN_LABEL                  # 'warn_1h_12_89'
PAIRS = (("9/12", 9, 12), ("12/26", 12, 26), ("12/89", 12, 89))       # L-W.2
ERAS = ("ALL", "tuning", "holdout")
COLLAR = {"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
          "gates": "nothing"}               # L-1.4
COLLAR_COLS = tuple(COLLAR)
# the four post-entry cohorts [contract W2 / L-W.4]:
#   (id, label, pair, side, latch relation, at-risk set)
COHORTS = (
    ("C1", "counter_12_89_before_1r", "12/89", "counter", "before", "whole_book"),
    ("C2", "counter_12_26_before_1r", "12/26", "counter", "before", "whole_book"),
    ("C3", "with_9_12_recross_after_entry", "9/12", "with", "any", "open_1h_after_entry"),
    ("C4", "counter_12_89_after_1r", "12/89", "counter", "after", "reached_1r"),
    # (w10) the STRICT re-cross reading of C3, printed beside it — deciding nothing
    ("C3S", "with_9_12_recross_strict", "9/12", "with", "any", "open_1h_after_entry"),
)
STRICT_COHORTS = frozenset({"C3S"})         # an event must also be recross_strict (w10)
AT_RISK_TEXT = {
    "whole_book": "the whole v6 book (a 'before +1R' cohort) [L-W.4]",
    "open_1h_after_entry": "campaigns still open 1h after entry: 1h-resolved exit > entry "
                           "close + 1h [L-W.4; sub-reading w6]",
    "reached_1r": "campaigns that reached +1R (L-W.3 latch present) [L-W.4]",
}
# the four PRE-ENTRY classes in (arm close, entry close] [L-W.4]
PRE = (("P1", "counter_12_89", "12/89", "counter"),
       ("P2", "counter_12_26", "12/26", "counter"),
       ("P3", "with_9_12", "9/12", "with"),
       ("P4", "with_12_26", "12/26", "with"))
COHORT_GROUPS = ("cohort", "at_risk", "complement")
PRE_GROUPS = ("cohort", "whole_book", "complement")
LAG_BANDS = ("ALL", "0", "1-6", "7-15", ">=16")
RELAY_POPS = ("v6_campaigns", "armed_windows_not_entered")
RELAY_LAGS = {"v6_campaigns": LAG_BANDS, "armed_windows_not_entered": ("ALL",)}
RELAY_LEAD_REF = {"v6_campaigns": "the window's 4h trigger close (= the v6 entry close)",
                  "armed_windows_not_entered": "the window's end: its 4h trigger close "
                                               "if it triggered, else its window close "
                                               "(the counter 12/89 4h cross) or the as-of"}
LEAD_STATS = ("min", "q25", "median", "q75", "max", "mean")
LEAD1_BINS = (("1", 1, 1), ("2-3", 2, 3), ("4-7", 4, 7), ("8-15", 8, 15),
              ("16-31", 16, 31), ("32-63", 32, 63), ("64-127", 64, 127),
              ("128-255", 128, 255), (">=256", 256, None))
LEAD4_BINS = (("0", 0, 0), ("1", 1, 1), ("2-3", 2, 3), ("4-7", 4, 7), ("8-15", 8, 15),
              ("16-31", 16, 31), ("32-63", 32, 63), (">=64", 64, None))
COMP_GROUPS = ("cohort_C1", "complement_C1", "acted", "unacted", "ALL")
PHASES = ("PRE-ENTRY", "IN-TRADE", "AT-EXIT", "POST-EXIT")
SIDE_CLASSES = tuple(f"{p}_{s}" for p, _, _ in PAIRS for s in ("counter", "with"))

# the regbook interface (binding; the scorer reads ONLY these)
REQUIRED = ("symbol", "entry_ms", "entry_close_ms", "direction", "entry_px", "stop_px",
            "r_dist", "exit_close_ms", "exit_reason", "net_r", "gross_r", "fee_r",
            "funding_r", "haircut_net_r", "era", "lane")
REQ_INT = ("entry_ms", "entry_close_ms", "exit_close_ms")
REQ_FLOAT = ("entry_px", "stop_px", "r_dist", "net_r", "gross_r", "fee_r", "funding_r",
             "haircut_net_r")
REQ_STR = ("symbol", "exit_reason", "era", "lane")
BOOK_SHA_LAW = ("sha256 of the UTF-8 CSV written by Python's csv.writer (lineterminator "
                "'\\n', QUOTE_MINIMAL): header = the 16 required columns in interface "
                "order; rows sorted by (symbol, entry_close_ms) (stable); floats as "
                "repr(float(x)), ints as str(int(x)), strings as str(x)")
EXIT_CLOSE_LAW = ("exit_close_ms = the CLOSE of the 4h exit bar (exit bar open + 4h) — the "
                  "estate's v6 schema (books/v6_campaigns.parquet, the scorer's F-BASE-IDENT "
                  "referee); the exact 1h-resolved exit instant (L-W.3: the stop child's close, "
                  "the warn child's close, a bell / corridor_end at its 4h close) is the extra "
                  "column exit_instant_ms")
HAIRCUT_LAW = ("AM-7: haircut_net_r = net_r − fee_r × (slip_bps_side / taker_bps_side); "
               "fee_r = the ride's taker fee over every fill / r_dist; slip_bps_side = the "
               "stem's charter tier (A 2 · B 5 · C 10) from E.fees(); taker 5.0 bps/side")

OUT = E.OUT / "stage_w"
REG_DIR = E.OUT / "regbooks" / REG
DET_ROOT = OUT / "_det_stage_w"
MANIFEST = "MANIFEST_STAGE_W.json"
REPORT = "STAGE_W.md"
TABLES = {                                   # name -> (key, lens)
    "W1_EVENTS": (["symbol", "entry_ms", "pair", "h1_open_ms"], "1h"),
    "W1_TIMELINE": (["symbol", "entry_ms", "bar_close_ms"], "4h"),
    "W1_CAMPAIGNS": (["symbol", "entry_ms"], "4h"),
    "W2_COHORTS": (["cell"], "4h"),
    "W2_FORWARD": (["cell"], "4h"),
    "W2_PREENTRY": (["cell"], "4h"),
    "W2_RELAY_WINDOWS": (["symbol", "entry_ms"], "4h"),
    "W2_RELAY_WINDOWS_TWIN": (["symbol", "arm_ms", "direction"], "4h"),
    "W2_RELAY_SUMMARY": (["cell"], "4h"),
    "W2_RELAY_HIST": (["cell"], "4h"),
    "P_WARN_1_COMPLEMENT": (["cell"], "4h"),
}
ARMS_MET = ("scored", "base", "tierE__tuning", "tierE__holdout")
ARMS_NOT_MET = ("tierE__rule_book_condition_not_met", "base", "tierE__tuning",
                "tierE__holdout")

READINGS = (
    "[LEAN-HEPHAESTUS] L-W.2 events = 1h engine-EMA-of-close crosses 9/12, 12/26, 12/89 "
    "(RD.cross_1h), known at the 1h close where the fast line changes side; with = the "
    "trade's direction, counter = against.",
    "[LEAN-HEPHAESTUS] L-W.1 visible at a 4h instant T iff the 1h close <= T.",
    "[LEAN-HEPHAESTUS] L-W.3 IN-TRADE = entry close < taken < the 1h-resolved exit "
    "(RD exit_close_ms); PRE-ENTRY = arm close < taken <= entry close; before +1R = "
    "taken < the L-W.3 latch (RD plus1r_1h_ms; none = any in-trade); after = >=.",
    "[LEAN-HEPHAESTUS] L-W.4 at-risk sets: before-+1R and pre-entry -> whole book; "
    "after-+1R -> reached +1R; 9/12 re-cross -> open 1h after entry; condition = "
    "T5.cluster_boot_diff(cohort C1, whole book, seed 20260924, n_boot 4000), MET iff "
    "cluster-90% hi < 0.",
    "[LEAN-HEPHAESTUS] L-W.5 rule book = RD.transform_book(v6, walk=True, "
    "warn_of=RD.warn_of(12/89)); L-1.5 identity law on every campaign the rule never "
    "acted on.",
    "[LEAN-HEPHAESTUS] L-W.6 relay evidence = the first 1h with-trend 12/26 cross with "
    "arm close < taken < the 4h trigger close, per v6 window.",
    "[LEAN-HEPHAESTUS] (w1) an event on a mismatch bar is TAKEN at the parent's close "
    "[L-W.0]; (w5) the mark = the campaign exited at the event, booked by "
    "tierc7._account_chain; (w6) 9/12 at-risk = exit > entry close + 1h; (w7) every v6 "
    "window = the campaign windows; the armed windows holding no v6 campaign are a twin.",
    "[LEAN-HEPHAESTUS] AM-7 haircut_net_r = net_r − fee_r × slip/taker per stem "
    "(E.fees()).",
    "[LEAN-HEPHAESTUS] (w10) C3 '9/12 re-cross with trend after entry' = ANY in-trade "
    "with-trend 1h 9/12 cross (the reading of the first build, disclosed); C3S, printed "
    "beside and deciding nothing = the STRICT reading: a with-trend 9/12 cross whose "
    "preceding 9/12 cross on the 1h tape is a counter cross closing after the entry close.",
    "[LEAN-HEPHAESTUS] (w11) AM-7's haircut twin beside every per-campaign net R "
    "(W1_CAMPAIGNS, W2_RELAY_WINDOWS) and the complement table's sums; L-1.3 entry bars "
    "straddling the era cut printed as a count (sidecars, STAGE_W.md).",
)
CHANGES_AFTER_FIRST_OUTPUT = (
    {"id": "CH-1", "what": "the (w7) twin population",
     "first_output": "every triggered candidate window of v6's card, admission ignored",
     "now": "every ARMED window of v6's card (tide + displacement gates passed) holding no "
            "v6 campaign: triggered-not-entered (end = trigger close) or never triggered "
            "(end = the known window close, else the as-of)",
     "why": "on this corridor the first population IS the v6 campaign set (200 triggered "
            "gate-passing windows == the 200 v6 windows, none refused by an open position; "
            "relay_twin_check), so the twin duplicated the population it stands beside",
     "moved": "W2_RELAY_WINDOWS_TWIN and the armed_windows_not_entered rows of "
              "W2_RELAY_SUMMARY / W2_RELAY_HIST only (Tier-E, gates nothing); no net_r moved"},
    {"id": "CH-2", "what": "the regbook column exit_close_ms",
     "first_output": "the 1h-resolved exit instant (L-W.3)",
     "now": "the CLOSE of the 4h exit bar (the estate's v6 schema); the exact 1h instant "
            "is the extra column exit_instant_ms",
     "why": "books/v6_campaigns.parquet carries exit_close_ms as the 4h exit-bar close and "
            "the scorer's SC-7 F-BASE-IDENT compares the base arm to it column by column",
     "moved": "that column and so each arm's book_sha256; no net_r / gross_r / fee_r / "
              "funding_r moved"},
)
CHANGES_NOTE = ("the builder's first-output files are not on disk; both changes are stated "
                "from the code's own law texts and the Stage W verifier's report (finding 2)")


def _halt(msg: str) -> None:
    raise SystemExit(f"HALT: {msg}")


# ════════════════════════════════════════════════════════ THE BOOKS AND RIDES
_MEMO: dict = {}


def corridor() -> tuple[int, int, dict]:
    if "cor" not in _MEMO:
        _MEMO["cor"] = B.corridor()
    return _MEMO["cor"]


def rides() -> dict:
    """base = v6 (B.v6_book); walked = the v6 set on the 1h walk with no rule
    (the 1h-resolved exits and latches; identity asserted); rule = the warn book."""
    if "rides" not in _MEMO:
        lo, hi, _ = corridor()
        base = B.v6_book(lo, hi)
        walked = RD.transform_book(base, CARD, ROLES, lo, hi, walk=True)
        f_w, st_w = RD.identity_findings(base, walked)
        if f_w or st_w["acted"]:
            _halt(f"the walked identity ride is not v6 [L-W.0 / F-WALK-IDENT]: {f_w[:3]} "
                  f"{st_w}")
        ok, worst, why = TP.ctrl_diff(TP.journal_frame(walked), TP.journal_frame(base))
        if not ok or worst != 0.0:
            _halt(f"the walked identity ride differs from v6 on CTRL_COLS: {why}")
        rule = RD.transform_book(base, CARD, ROLES, lo, hi, walk=True,
                                 warn_of=lambda s: RD.warn_of(RD.walk_of(s)))
        keys = [(t.symbol, int(t.entry_ms)) for t in base]
        for bk, nm in ((walked, "walked"), (rule, "rule")):
            if [(t.symbol, int(t.entry_ms)) for t in bk] != keys:
                _halt(f"the {nm} book does not keep v6's keys in order [L-1.5]")
        _MEMO["rides"] = {"base": base, "walked": walked, "rule": rule,
                          "identity_walked": st_w, "ctrl_worst_walked": worst}
    return _MEMO["rides"]


def clear_memo(events: bool = True, rides_too: bool = False) -> None:
    """Fixture seam: drop the event memo (and optionally the rides)."""
    if events:
        _MEMO.pop("events", None)
    if rides_too:
        _MEMO.pop("rides", None)


# ══════════════════════════════════════════════════════════ THE 1h EVENT TAPE
def event_arrays(h1: RD.H1Tape) -> dict:
    """{pair: (up, dn)} over a 1h tape — the ENGINE EMA of the 1h close [L-W.2].
    Fixture seam: F-WARN-ASOF calls it on PREFIX tapes."""
    return {p: RD.cross_1h(h1, fa, sl) for p, fa, sl in PAIRS}


def asset_events(sym: str) -> pd.DataFrame:
    """Every 1h cross of the three pairs over the asset's whole 1h tape (closed at
    the pin), with its 4h parent, walkability and TAKEN instant (w1)."""
    memo = _MEMO.setdefault("events", {})
    if sym in memo:
        return memo[sym]
    W = RD.walk_of(sym)
    f = T9.frame(sym)["f"]
    h1 = W.h1
    o4 = np.asarray(f.open_ms, dtype=np.int64)
    arrs = event_arrays(h1)
    rows = []
    for p, _, _ in PAIRS:
        up, dn = arrs[p]
        # the pair's crosses in tape order, each with the PRECEDING cross of the same
        # pair (either direction) — the strict re-cross reading's input (w10)
        seq = sorted([(int(k), "up") for k in np.flatnonzero(up)]
                     + [(int(k), "dn") for k in np.flatnonzero(dn)])
        prev_x, prev_c = "", 0
        for k, cross in seq:
            op = int(h1.open_ms[k])
            J = int(np.searchsorted(o4, op, "right")) - 1
            if J < 0 or op >= int(o4[J]) + MS_4H:
                _halt(f"{sym} 1h bar {iso(op)} lies in no 4h frame bar")
            walkable = bool(W.ok[J])
            close = op + MS_1H
            pclose = int(o4[J]) + MS_4H
            rows.append({"pair": p, "cross": cross, "k": k, "h1_open_ms": op,
                         "close_ms": close, "J": J, "parent_open_ms": int(o4[J]),
                         "parent_close_ms": pclose, "walkable": walkable,
                         "taken_ms": close if walkable else pclose,
                         "px_taken": float(h1.c[k]) if walkable else float(f.c[J]),
                         "prev_cross": prev_x, "prev_close_ms": prev_c})
            prev_x, prev_c = cross, close
    d = pd.DataFrame(rows).sort_values(["taken_ms", "close_ms", "pair"],
                                       kind="mergesort").reset_index(drop=True)
    memo[sym] = d
    return d


# ══════════════════════════════════════ THE CLASSIFIERS (fixture seams: mutable)
def visible(close_ms: int, t4_close_ms: int) -> bool:
    """L-W.1: a 1h bar is visible at a 4h decision instant iff its close <= it."""
    return int(close_ms) <= int(t4_close_ms)


def first_visible(close_ms: int, closes4: np.ndarray) -> int:
    """The first 4h close (of the asset's frame) at which the 1h close is visible,
    judged through `visible` at the neighbouring 4h closes."""
    i = int(np.searchsorted(closes4, int(close_ms), "left"))
    i = min(i, len(closes4) - 1)
    while i > 0 and visible(close_ms, int(closes4[i - 1])):
        i -= 1
    while i < len(closes4) - 1 and not visible(close_ms, int(closes4[i])):
        i += 1
    if not visible(close_ms, int(closes4[i])):
        _halt(f"a 1h close {iso(int(close_ms))} is visible at no 4h close of the frame")
    return int(closes4[i])


def exit_instant(w) -> int:
    """L-W.3: the 1h-RESOLVED exit instant of the walked ride (the stop child's
    close; a bell / corridor_end at its 4h close; a mismatch-bar stop at the
    parent's close)."""
    x = getattr(w, "exit_close_ms", None)
    if x is None:
        _halt(f"{w.symbol} {iso(int(w.entry_ms))}: no 1h-resolved exit (ride without walk)")
    return int(x)


def latch_instant(w):
    """L-W.3's +1R latch: the first 1h child after the entry close whose high (low)
    reaches entry ± R (a mismatch bar: the parent decides) — RD's plus1r_1h_ms."""
    x = getattr(w, "plus1r_1h_ms", None)
    return None if x is None else int(x)


def latch_twin(w):
    """L-W.5's latch (stop before latch on one child) — RD's latch_1h_ms [AM-6]."""
    x = getattr(w, "latch_1h_ms", None)
    return None if x is None else int(x)


def phase_of(taken: int, arm_close: int, entry_close: int, exit_close: int) -> str | None:
    """L-W.3 windows (sub-reading w2)."""
    if taken <= arm_close:
        return None
    if taken <= entry_close:
        return "PRE-ENTRY"
    if taken < exit_close:
        return "IN-TRADE"
    if taken == exit_close:
        return "AT-EXIT"
    return "POST-EXIT"


def latch_rel(taken: int, latch) -> str:
    """L-W.3: before +1R = index < the latch index (no latch: before); after = >=."""
    if latch is None or taken < int(latch):
        return "before"
    return "after"


def side_of(cross: str, d: int) -> str:
    """L-W.2: with = the fast line crosses in the trade's direction."""
    return "with" if (cross == "up") == (int(d) == 1) else "counter"


def in_class(row: dict, pair: str, side: str, phase: str, rel: str) -> bool:
    return (row["pair"] == pair and row["side"] == side and row["phase"] == phase
            and (rel == "any" or row["latch_rel"] == rel))


def recross_strict(pair: str, side: str, prev_cross: str, prev_close_ms: int, d: int,
                   entry_close: int) -> bool:
    """(w10) the STRICT re-cross: a with-trend 9/12 cross whose preceding 9/12 cross
    on the 1h tape is a COUNTER cross closing after the entry close."""
    return bool(pair == "9/12" and side == "with" and prev_cross in ("up", "dn")
                and side_of(prev_cross, d) == "counter"
                and int(prev_close_ms) > int(entry_close))


def cohort_hits(er: list, cid: str, pair: str, side: str, rel: str) -> list:
    """The campaign's IN-TRADE events of cohort `cid` (w4); a STRICT cohort also needs
    the event to be a strict re-cross (w10)."""
    return [e for e in er if in_class(e, pair, side, "IN-TRADE", rel)
            and (cid not in STRICT_COHORTS or bool(e.get("recross_strict")))]


# ══════════════════════════════════════════════════════════ THE CAMPAIGNS
def campaign_info(t, w) -> dict:
    """The instants of one v6 campaign (t = the v6 Trade, w = its walked twin)."""
    if (t.symbol, int(t.entry_ms)) != (w.symbol, int(w.entry_ms)):
        _halt("campaign_info: base and walked trades are not the same campaign")
    return {"symbol": t.symbol, "entry_ms": int(t.entry_ms), "direction": int(t.direction),
            "arm_i": int(t.arm_i), "entry_i": int(t.entry_i), "exit_i": int(t.exit_i),
            "arm_close_ms": int(t.arm_ms) + MS_4H,
            "entry_close_ms": int(t.entry_ms) + MS_4H,
            "exit_close_ms": exit_instant(w),
            "exit_bar_close_ms": int(t.exit_ms) + MS_4H,
            "exit_resolved_by": str(w.exit_resolved_by),
            "exit_reason": str(t.exit_reason),
            "latch_ms": latch_instant(w), "latch_w5_ms": latch_twin(w),
            "latch_by": w.latch_1h_by,
            "n_walk_mismatch": int(w.n_walk_mismatch),
            "reached_1r_v6": bool(t.reached_1r),
            "net_r": float(t.net_r), "fee_r": float(t.fee_r),
            "haircut_net_r": haircut(t.symbol, t.net_r, t.fee_r),          # AM-7 (w11)
            "era": E.era_of(int(t.entry_ms) + MS_4H),
            "lag": int(t.entry_i) - int(t.arm_i)}


def classify_campaign(ci: dict, ev: pd.DataFrame, closes4: np.ndarray) -> list[dict]:
    """Every event of the asset's tape with arm close < taken <= the exit-bar close,
    classified [L-W.1..L-W.3; sub-readings w1, w2]."""
    lo, hi = ci["arm_close_ms"], max(ci["exit_bar_close_ms"], ci["exit_close_ms"])
    tk = ev["taken_ms"].to_numpy(np.int64)
    a = int(np.searchsorted(tk, lo, "right"))
    b = int(np.searchsorted(tk, hi, "right"))
    out = []
    for r in ev.iloc[a:b].itertuples(index=False):
        ph = phase_of(int(r.taken_ms), ci["arm_close_ms"], ci["entry_close_ms"],
                      ci["exit_close_ms"])
        if ph is None:
            continue
        ph_raw = phase_of(int(r.close_ms), ci["arm_close_ms"], ci["entry_close_ms"],
                          ci["exit_close_ms"])
        rel = latch_rel(int(r.taken_ms), ci["latch_ms"]) if ph == "IN-TRADE" else None
        rel_raw = (latch_rel(int(r.close_ms), ci["latch_ms"]) if ph_raw == "IN-TRADE"
                   else None)
        sd = side_of(r.cross, ci["direction"])
        strict = recross_strict(r.pair, sd, str(getattr(r, "prev_cross", "") or ""),
                                int(getattr(r, "prev_close_ms", 0) or 0), ci["direction"],
                                ci["entry_close_ms"])
        out.append({"symbol": ci["symbol"], "entry_ms": ci["entry_ms"],
                    "direction": ci["direction"], "pair": r.pair, "cross": r.cross,
                    "side": sd, "h1_index": int(r.k),
                    "h1_open_ms": int(r.h1_open_ms), "close_ms": int(r.close_ms),
                    "parent_open_ms": int(r.parent_open_ms), "on_mismatch_bar": not r.walkable,
                    "taken_ms": int(r.taken_ms),
                    "visible_4h_close_ms": first_visible(int(r.close_ms), closes4),
                    "px_taken": float(r.px_taken), "phase": ph,
                    "latch_rel": rel, "raw_instant_changes_class": bool(
                        ph_raw != ph or rel_raw != rel),
                    "recross_strict": strict,
                    "era": ci["era"]})
    return out


def timeline_rows(ci: dict, evrows: list[dict], closes4: np.ndarray) -> list[dict]:
    """The campaign's 4h timeline (closes in (arm close, exit-bar close]) stamped
    with the counts of its W1 events VISIBLE at each close, per class [L-W.1]."""
    out = []
    i0 = int(np.searchsorted(closes4, ci["arm_close_ms"], "right"))
    i1 = int(np.searchsorted(closes4, ci["exit_bar_close_ms"], "right"))
    for T in closes4[i0:i1]:
        T = int(T)
        row = {"symbol": ci["symbol"], "entry_ms": ci["entry_ms"], "bar_close_ms": T,
               "stage": ("armed" if T <= ci["entry_close_ms"]
                         else "in_trade" if T < ci["exit_bar_close_ms"] else "exit_bar")}
        for c in SIDE_CLASSES:
            row[f"n_vis_{c.replace('/', '_')}"] = 0
        row["n_vis_in_trade_pre1r_counter_12_89"] = 0
        for e in evrows:
            if visible(e["close_ms"], T):
                row[f"n_vis_{e['pair'].replace('/', '_')}_{e['side']}"] += 1
                if in_class(e, "12/89", "counter", "IN-TRADE", "before"):
                    row["n_vis_in_trade_pre1r_counter_12_89"] += 1
        out.append(row)
    return out


def mark_at(t, ev: dict) -> float:
    """(w5) the campaign's net R had it exited at the event's taken instant, at the
    tape's price there — booked by tierc7._account_chain (RD.account11)."""
    f = T9.frame(t.symbol)["f"]
    o4 = np.asarray(f.open_ms, dtype=np.int64)
    J = int(np.searchsorted(o4, int(ev["taken_ms"]) - 1, "right")) - 1
    if not (int(o4[J]) < int(ev["taken_ms"]) <= int(o4[J]) + MS_4H):
        _halt("mark_at: the event's taken instant is in no 4h bar")
    if J <= int(t.entry_i) or J > int(t.exit_i):
        _halt(f"mark_at: event bar {J} outside the campaign ({t.entry_i}, {t.exit_i}]")
    harv = None
    if t.harvested and int(t.harvest_i) < J:
        harv = (int(t.harvest_i), float(t.harvest_px), float(t.harvest_unit_move_r))
    leg = {"entry_i": int(t.entry_i), "exit_i": J, "exit_px": float(ev["px_taken"]),
           "entry_px": float(t.entry_px), "harvest": harv, "adds": [],
           "own_r": abs(float(t.entry_px) - float(t.stop_px))}
    return float(RD.account11(t.symbol, CARD, int(t.direction), float(t.r_dist),
                              leg)["net_r"])


# ═══════════════════════════════════════════════════════════════ W1
def w1(rd: dict) -> dict:
    """W1_EVENTS, W1_TIMELINE and the per-campaign facts."""
    base, walked, rule = rd["base"], rd["walked"], rd["rule"]
    ev_rows, tl_rows, camps = [], [], []
    closes = {}
    for s in E.CLASSIC5:
        f = T9.frame(s)["f"]
        closes[s] = np.asarray(f.open_ms, dtype=np.int64) + MS_4H
    for t, w, r in zip(base, walked, rule):
        ci = campaign_info(t, w)
        ev = asset_events(t.symbol)
        er = classify_campaign(ci, ev, closes[t.symbol])
        tl_rows += timeline_rows(ci, er, closes[t.symbol])
        ci["rule_exit_reason"] = str(r.exit_reason)
        ci["rule_net_r"] = float(r.net_r)
        ci["rule_fee_r"] = float(r.fee_r)
        ci["rule_haircut_net_r"] = haircut(r.symbol, r.net_r, r.fee_r)  # AM-7 (w11)
        ci["rule_exit_close_ms"] = int(r.exit_close_ms)
        ci["rule_acted"] = str(r.acted_by)
        ci["_t"], ci["_events"] = t, er
        camps.append(ci)
        ev_rows += er
    return {"camps": camps, "events": ev_rows, "timeline": tl_rows}


def campaign_table(camps: list[dict], marks: bool = True) -> pd.DataFrame:
    """W1_CAMPAIGNS: memberships, first events, marks and forward legs.  `marks`
    False skips the (w5) accounting (a classification-only recompute: the fixture
    seam for mutations of the classifiers, where mark_at's own guard would HALT
    first on an event it was never meant to price)."""
    rows = []
    for ci in camps:
        t, er = ci["_t"], ci["_events"]
        row = {k: v for k, v in ci.items() if not k.startswith("_")}
        row["win"] = bool(ci["net_r"] > 0)
        row["reached_1r"] = ci["latch_ms"] is not None
        row["latch_readings_agree"] = ci["latch_ms"] == ci["latch_w5_ms"]
        row["open_1h_after_entry"] = bool(ci["exit_close_ms"] > ci["entry_close_ms"] + MS_1H)
        row["n_events_w1"] = len(er)
        row["n_events_raw_instant_changes_class"] = sum(e["raw_instant_changes_class"]
                                                        for e in er)
        for cid, lab, pair, side, rel, _ in COHORTS:
            hits = cohort_hits(er, cid, pair, side, rel)
            row[f"{cid}_n_events"] = len(hits)
            row[f"{cid}_member"] = bool(hits)
            if hits:
                e0 = min(hits, key=lambda e: (e["taken_ms"], e["close_ms"]))
                mk = mark_at(t, e0) if marks else float("nan")
                row[f"{cid}_first_taken_ms"] = int(e0["taken_ms"])
                row[f"{cid}_first_on_mismatch_bar"] = bool(e0["on_mismatch_bar"])
                row[f"{cid}_mark_r"] = mk
                row[f"{cid}_fwd_r"] = float(ci["net_r"]) - mk
            else:
                row[f"{cid}_first_taken_ms"] = None
                row[f"{cid}_first_on_mismatch_bar"] = None
                row[f"{cid}_mark_r"] = None
                row[f"{cid}_fwd_r"] = None
        for pid, lab, pair, side in PRE:
            hits = [e for e in er if e["pair"] == pair and e["side"] == side
                    and e["phase"] == "PRE-ENTRY"]
            row[f"{pid}_n_events"] = len(hits)
            row[f"{pid}_member"] = bool(hits)
        rl = relay_cross(er, ci["arm_close_ms"], ci["entry_close_ms"], ci["direction"])
        row.update(rl)
        rows.append(row)
    d = pd.DataFrame(rows)
    for c in d.columns:
        if c.endswith(("_first_taken_ms", "latch_ms", "latch_w5_ms", "relay_close_ms",
                       "relay_taken_ms", "relay_visible_4h_close_ms", "relay_lead_1h",
                       "relay_lead_4h")):
            d[c] = d[c].astype("Int64")
        elif c.endswith(("_mark_r", "_fwd_r")):
            d[c] = d[c].astype("float64")
        elif c.endswith("_first_on_mismatch_bar") or c == "relay_on_mismatch_bar":
            d[c] = d[c].astype("boolean")
    return d


# ═══════════════════════════════════════════════════════════ L-W.6 THE RELAY
def relay_cross(er_or_ev, arm_close: int, trigger_close: int, d: int,
                closes4: np.ndarray | None = None) -> dict:
    """The first 1h with-trend 12/26 cross with arm close < taken < the 4h trigger
    close [L-W.6] — from a campaign's classified rows (or an asset's raw tape with
    `closes4`, the twin population)."""
    best = None
    for e in er_or_ev:
        if e["pair"] != "12/26":
            continue
        sd = e["side"] if "side" in e else side_of(e["cross"], d)
        if sd != "with":
            continue
        if arm_close < int(e["taken_ms"]) < trigger_close:
            if best is None or (int(e["taken_ms"]), int(e["close_ms"])) < (
                    int(best["taken_ms"]), int(best["close_ms"])):
                best = e
    if best is None:
        return {"relay_cross": False, "relay_close_ms": None, "relay_taken_ms": None,
                "relay_visible_4h_close_ms": None, "relay_on_mismatch_bar": None,
                "relay_lead_1h": None, "relay_lead_4h": None}
    vis = (int(best["visible_4h_close_ms"]) if "visible_4h_close_ms" in best
           else first_visible(int(best["close_ms"]), closes4))
    return {"relay_cross": True, "relay_close_ms": int(best["close_ms"]),
            "relay_taken_ms": int(best["taken_ms"]),
            "relay_visible_4h_close_ms": vis,
            "relay_on_mismatch_bar": bool(best.get("on_mismatch_bar",
                                                   not best.get("walkable", True))),
            "relay_lead_1h": (trigger_close - int(best["taken_ms"])) // MS_1H,
            "relay_lead_4h": (trigger_close - vis) // MS_4H}


def lag_band(lag: int) -> str:
    return B.lag_band(int(lag))


def relay_twin_windows(v6_keys: set) -> tuple[pd.DataFrame, dict]:
    """The TWIN population (w7): every ARMED window of v6's card (T9.card_candidates9
    over the ride bounds: tide and displacement gates passed) that holds NO v6
    campaign — a window that never triggered (end = its window close, the counter
    12/89 4h cross, as known at the as-of; an open window ends at the as-of) or one
    that triggered but was not entered (end = its trigger close).  The relay cross
    is the first 1h with-trend 12/26 cross with arm close < taken < that end.
    Also returns the check that the triggered gate-passing windows ARE v6's set."""
    lo, hi, _ = corridor()
    rows, trig_keys = [], set()
    for s in E.CLASSIC5:
        lo_i, hi_i, _n = B.ride_bounds(s, ROLES, lo, hi)
        f = T9.frame(s)["f"]
        o4 = np.asarray(f.open_ms, dtype=np.int64)
        closes4 = o4 + MS_4H
        arms_, cands = T9.card_candidates9(s, ROLES, lo_i, hi_i)
        trig = {(int(a.arm_i), int(a.direction)): int(ti) for ti, _d, a in cands}
        ev = asset_events(s)
        evl = ev.to_dict("records")
        tk = ev["taken_ms"].to_numpy(np.int64)
        for a in arms_:
            k = (int(a.arm_i), int(a.direction))
            if not (a.tide_ok and a.d_ok):
                continue
            if k in trig:
                key = (s, int(o4[trig[k]]))
                trig_keys.add(key)
                if key in v6_keys:
                    continue
                end_close, kind = int(o4[trig[k]]) + MS_4H, "trigger_not_entered"
            else:
                end_i = B.known_window_end(int(a.window_end_i), hi_i)
                if end_i <= hi_i:
                    end_close, kind = int(o4[end_i]) + MS_4H, "window_close"
                else:
                    end_close, kind = int(o4[hi_i]) + MS_4H, "as_of"
            arm_close = int(o4[int(a.arm_i)]) + MS_4H
            i0 = int(np.searchsorted(tk, arm_close, "right"))
            i1 = int(np.searchsorted(tk, end_close, "left"))
            rl = relay_cross(evl[i0:i1], arm_close, end_close, int(a.direction), closes4)
            rows.append({"symbol": s, "arm_ms": int(a.arm_ms), "direction": int(a.direction),
                         "arm_close_ms": arm_close, "end_close_ms": end_close,
                         "end_kind": kind, "window_bars": (end_close - arm_close) // MS_4H,
                         "era": E.era_of(end_close), **rl})
    d = pd.DataFrame(rows).sort_values(["symbol", "arm_ms", "direction"],
                                       kind="mergesort").reset_index(drop=True)
    for c in ("relay_close_ms", "relay_taken_ms", "relay_visible_4h_close_ms",
              "relay_lead_1h", "relay_lead_4h"):
        d[c] = d[c].astype("Int64")
    d["relay_on_mismatch_bar"] = d["relay_on_mismatch_bar"].astype("boolean")
    chk = {"triggered_gate_passing_windows": len(trig_keys),
           "v6_campaign_windows": len(v6_keys),
           "triggered_equals_v6_set": trig_keys == v6_keys,
           "triggered_not_entered": sorted(f"{a} {iso(b)}" for a, b in trig_keys - v6_keys),
           "v6_not_in_triggered": sorted(f"{a} {iso(b)}" for a, b in v6_keys - trig_keys),
           "twin_windows_by_end_kind": {k: int(v) for k, v in
                                        d["end_kind"].value_counts().sort_index().items()}}
    return d, chk


# ════════════════════════════════════════════════════════════ W2 TABLES
def _stats(net: np.ndarray) -> dict:
    n = int(len(net))
    if n == 0:
        return {"n": 0, "n_win": 0, "p_win": float("nan"), "mean_net_r": float("nan"),
                "sum_net_r": 0.0, "nan_reason": "n=0: no campaign in this cell"}
    return {"n": n, "n_win": int((net > 0).sum()), "p_win": float((net > 0).mean()),
            "mean_net_r": float(net.mean()), "sum_net_r": float(net.sum()), "nan_reason": ""}


def _era_mask(d: pd.DataFrame, era: str) -> np.ndarray:
    return np.ones(len(d), bool) if era == "ALL" else (d["era"] == era).to_numpy()


def at_risk_mask(c: pd.DataFrame, which: str) -> np.ndarray:
    if which == "whole_book":
        return np.ones(len(c), bool)
    if which == "open_1h_after_entry":
        return c["open_1h_after_entry"].to_numpy(bool)
    if which == "reached_1r":
        return c["reached_1r"].to_numpy(bool)
    _halt(f"unknown at-risk set {which}")
    return np.zeros(0, bool)


def w2_cohorts(c: pd.DataFrame) -> pd.DataFrame:
    rows = []
    net = c["net_r"].to_numpy(float)
    for cid, lab, pair, side, rel, ar in COHORTS:
        mem = c[f"{cid}_member"].to_numpy(bool)
        risk = at_risk_mask(c, ar)
        if bool((mem & ~risk).any()):
            _halt(f"{cid}: a cohort member outside its at-risk set [L-W.4]")
        for era in ERAS:
            em = _era_mask(c, era)
            sets = {"cohort": mem & em, "at_risk": risk & em,
                    "complement": risk & ~mem & em}
            m_risk = _stats(net[sets["at_risk"]])["mean_net_r"]
            for g in COHORT_GROUPS:
                st = _stats(net[sets[g]])
                rows.append({"cell": f"{cid}_{lab}|{g}|{era}", "cohort": f"{cid}_{lab}",
                             "group": g, "era": era, "pair": pair, "side": side,
                             "latch_relation": rel, "phase": "IN-TRADE",
                             "at_risk_set": AT_RISK_TEXT[ar], **st,
                             "mean_minus_at_risk_mean": (st["mean_net_r"] - m_risk
                                                         if st["n"] else float("nan")),
                             **COLLAR})
    return pd.DataFrame(rows)


def w2_forward(c: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for cid, lab, *_ in COHORTS:
        mem = c[f"{cid}_member"].to_numpy(bool)
        for era in ERAS:
            m = mem & _era_mask(c, era)
            fin = c.loc[m, "net_r"].to_numpy(float)
            mk = c.loc[m, f"{cid}_mark_r"].to_numpy(float)
            fw = c.loc[m, f"{cid}_fwd_r"].to_numpy(float)
            n = int(m.sum())
            rows.append({"cell": f"{cid}_{lab}|{era}", "cohort": f"{cid}_{lab}", "era": era,
                         "n": n,
                         "mean_final_net_r": float(fin.mean()) if n else float("nan"),
                         "mean_mark_r": float(mk.mean()) if n else float("nan"),
                         "mean_fwd_r": float(fw.mean()) if n else float("nan"),
                         "sum_fwd_r": float(fw.sum()) if n else 0.0,
                         "n_fwd_pos": int((fw > 0).sum()),
                         "p_fwd_pos": float((fw > 0).mean()) if n else float("nan"),
                         "event": "the FIRST event of the class per campaign (w4); mark = "
                                  "net R exited at its taken instant (w5)",
                         "nan_reason": "" if n else "n=0: no campaign in this cell",
                         **COLLAR})
    return pd.DataFrame(rows)


def w2_preentry(c: pd.DataFrame) -> pd.DataFrame:
    rows = []
    net = c["net_r"].to_numpy(float)
    for pid, lab, pair, side in PRE:
        mem = c[f"{pid}_member"].to_numpy(bool)
        nev = c[f"{pid}_n_events"].to_numpy(int)
        for era in ERAS:
            em = _era_mask(c, era)
            sets = {"cohort": mem & em, "whole_book": em, "complement": ~mem & em}
            m_all = _stats(net[em])["mean_net_r"]
            for g in PRE_GROUPS:
                st = _stats(net[sets[g]])
                rows.append({"cell": f"{pid}_{lab}|{g}|{era}", "event_class": f"{pid}_{lab}",
                             "group": g, "era": era, "pair": pair, "side": side,
                             "phase": "PRE-ENTRY (arm close, entry close]",
                             "n_events": int(nev[sets[g]].sum()), **st,
                             "mean_minus_whole_book_mean": (st["mean_net_r"] - m_all
                                                            if st["n"] else float("nan")),
                             **COLLAR})
    return pd.DataFrame(rows)


def _lead_stats(x: np.ndarray, pre: str) -> dict:
    if not len(x):
        return {f"{pre}_{s}": float("nan") for s in LEAD_STATS}
    return {f"{pre}_min": float(x.min()), f"{pre}_q25": float(np.percentile(x, 25)),
            f"{pre}_median": float(np.percentile(x, 50)),
            f"{pre}_q75": float(np.percentile(x, 75)), f"{pre}_max": float(x.max()),
            f"{pre}_mean": float(x.mean())}


def relay_summary(pops: dict) -> pd.DataFrame:
    rows = []
    for pop in RELAY_POPS:
        d = pops[pop]
        for era in ERAS:
            em = _era_mask(d, era)
            for lb in RELAY_LAGS[pop]:
                lm = (np.ones(len(d), bool) if lb == "ALL"
                      else d["lag"].map(lag_band).eq(lb).to_numpy())
                m = em & lm
                sub = d[m]
                has = sub["relay_cross"].to_numpy(bool)
                l1 = sub.loc[has, "relay_lead_1h"].to_numpy(float)
                l4 = sub.loc[has, "relay_lead_4h"].to_numpy(float)
                n = int(m.sum())
                rows.append({"cell": f"{pop}|{era}|{lb}", "population": pop, "era": era,
                             "lag_band": lb, "lead_reference": RELAY_LEAD_REF[pop],
                             "n_windows": n,
                             "n_lag0": (int((sub["lag"] == 0).sum()) if "lag" in sub.columns
                                        else 0),
                             "n_relay_cross": int(has.sum()),
                             "share_relay_cross": float(has.mean()) if n else float("nan"),
                             **_lead_stats(l1, "lead_1h"), **_lead_stats(l4, "lead_4h"),
                             "nan_reason": ("" if n and has.any() else
                                            "n=0: no window in this cell" if not n else
                                            "no relay cross in this cell: lead stats NaN"),
                             **COLLAR})
    return pd.DataFrame(rows)


def _bin(x: int, bins) -> str:
    for name, a, b in bins:
        if x >= a and (b is None or x <= b):
            return name
    _halt(f"a lead {x} falls in no bin")
    return ""


def relay_hist(pops: dict) -> pd.DataFrame:
    rows = []
    for pop in RELAY_POPS:
        d = pops[pop]
        has = d["relay_cross"].to_numpy(bool)
        for metric, bins in (("lead_1h", LEAD1_BINS), ("lead_4h", LEAD4_BINS)):
            vals = d.loc[has, f"relay_{metric}"].astype(int).tolist()
            cnt = {name: 0 for name, _, _ in bins}
            for v in vals:
                cnt[_bin(v, bins)] += 1
            for name, _, _ in bins:
                rows.append({"cell": f"{pop}|{metric}|{name}", "population": pop,
                             "metric": metric, "bin": name, "n": cnt[name], **COLLAR})
            rows.append({"cell": f"{pop}|{metric}|none", "population": pop,
                         "metric": metric, "bin": "none", "n": int((~has).sum()), **COLLAR})
    return pd.DataFrame(rows)


def relay_windows(c: pd.DataFrame) -> pd.DataFrame:
    cols = ["symbol", "entry_ms", "direction", "era", "lag", "arm_close_ms",
            "entry_close_ms", "relay_cross", "relay_close_ms", "relay_taken_ms",
            "relay_visible_4h_close_ms", "relay_on_mismatch_bar", "relay_lead_1h",
            "relay_lead_4h", "net_r", "haircut_net_r"]
    d = c[cols].rename(columns={"entry_close_ms": "trigger_close_ms"}).copy()
    for k, v in COLLAR.items():
        d[k] = v
    return d


# ═══════════════════════════════════════════════════ P-WARN-1: THE CONDITION
def condition(c: pd.DataFrame, rd: dict) -> dict:
    """L-W.4: delta = mean(C1 cohort) − mean(whole v6 book), asset-cluster
    bootstrap (T5.cluster_boot_diff, seed 20260924, n_boot 4000), T5._ci_from;
    MET iff the cluster-90% hi < 0.  The sensitivity seed and the rival
    (complement) reading are printed beside, deciding nothing."""
    base = rd["base"]
    net = np.array([float(t.net_r) for t in base])
    sym = np.array([t.symbol for t in base])
    mem = c["C1_member"].to_numpy(bool)
    if [(t.symbol, int(t.entry_ms)) for t in base] != list(zip(c["symbol"], c["entry_ms"])):
        _halt("condition: the campaign table is not in the book's order")
    va, ca = net[mem], sym[mem]
    point = float(va.mean() - net.mean())
    ci = T5._ci_from(T5.cluster_boot_diff(va, ca, net, sym, seed=SEED, n_boot=N_BOOT), point)
    cs = T5._ci_from(T5.cluster_boot_diff(va, ca, net, sym, seed=SEED_SENS, n_boot=N_BOOT),
                     point)
    vc, cc = net[~mem], sym[~mem]
    pr = float(va.mean() - vc.mean())
    rv = T5._ci_from(T5.cluster_boot_diff(va, ca, vc, cc, seed=SEED, n_boot=N_BOOT), pr)
    met = bool(ci["hi"] is not None and ci["hi"] < 0)
    keys = [f"{s}|{int(e)}" for s, e, m in zip(c["symbol"], c["entry_ms"], mem) if m]
    warn = [f"{s}|{int(e)}" for s, e, r in zip(c["symbol"], c["entry_ms"],
                                                c["rule_exit_reason"]) if r == WARN_LABEL]
    mism = [f"{s}|{int(e)}" for s, e, m, x in zip(c["symbol"], c["entry_ms"], mem,
                                                   c["C1_first_on_mismatch_bar"])
            if m and bool(x)]
    belltie = sorted(set(warn) - set(keys))
    per_asset = {s: {"cohort_n": int((ca == s).sum()),
                     "cohort_mean": float(va[ca == s].mean()) if (ca == s).any() else None,
                     "book_n": int((sym == s).sum()), "book_mean": float(net[sym == s].mean())}
                 for s in E.CLASSIC5}
    return {
        "registration": REG, "tier": "TIER-E",
        "selection_not_a_result": "a SELECTION, not a result",
        "gates": "nothing",                    # the L-1.4 collar, exact (L-W.4: Tier-E)
        "condition_role": ("the registered condition of P-WARN-1 (L-W.4): `met` decides only "
                           "whether P-WARN-1's rule book is the scored arm or a collared "
                           "Tier-E arm; it decides nothing else"),
        "condition_text": ("IF W2's \"1h counter-12/89 before +1R\" cohort's E[net] is below "
                           "the base by a cluster-90% interval excluding zero"),
        "reading": "L-W.4: cohort = v6 campaigns with an IN-TRADE counter 12/89 1h cross "
                   "before the +1R latch; delta = mean(cohort) − mean(whole v6 book) by "
                   "T5.cluster_boot_diff (asset clusters), T5._ci_from (5th–95th pct); "
                   "MET iff ci_hi < 0",
        "book": "v6, CLASSIC5, full corridor (the book the rule is scored on)",
        "cohort_n": int(mem.sum()), "cohort_mean": float(va.mean()),
        "book_n": int(len(net)), "book_mean": float(net.mean()), "delta": point,
        "ci_lo": ci["lo"], "ci_hi": ci["hi"], "met": met, "seed": SEED, "n_boot": N_BOOT,
        "sens_seed_ci": {"seed": SEED_SENS, "n_boot": N_BOOT, "lo": cs["lo"], "hi": cs["hi"],
                         "met_at_sens_seed": bool(cs["hi"] is not None and cs["hi"] < 0),
                         "note": "printed beside; decides nothing [L-1.4]"},
        "rival_complement": {"complement_n": int((~mem).sum()),
                             "complement_mean": float(vc.mean()), "delta": pr,
                             "ci_lo": rv["lo"], "ci_hi": rv["hi"], "seed": SEED,
                             "n_boot": N_BOOT,
                             "would_be_met": bool(rv["hi"] is not None and rv["hi"] < 0),
                             "note": "rival reading (cohort vs its complement, the TC7 lab "
                                     "_stat reading) (w9) — decides nothing"},
        "per_asset": per_asset,
        "cohort_keys": keys, "warn_exit_keys": sorted(warn),
        "listed_mismatch_keys": sorted(mism),
        "listed_belltie_keys": belltie, "belltie_n": len(belltie),
        "cohort_law": ("THE FROZEN LAW (L-W.4): condition-cohort keys == rule-book warn-exit "
                       "keys plus the keys whose first qualifying cross fell on a mismatch "
                       "bar (listed).  Belltie keys — a warn exit at the SAME instant as "
                       "v6's close exit (bell / corridor_end), which L-W.3's 'strictly "
                       "before the exit' keeps out of the cohort — are listed separately "
                       "and NOT absorbed: a non-empty belltie list breaks the law"),
        "cohort_law_holds": bool(set(keys) == set(warn) | set(mism)),
        "as_of": PIN_ISO,
    }


# ══════════════════════════════════════════════════════ THE REGBOOK ARMS
def _fees() -> dict:
    if "fees" not in _MEMO:
        fz = E.fees()
        for s in E.CLASSIC5:
            if fz[s]["taker_bps_side"] != float(T9.RC.FEE_BPS_SIDE):
                _halt(f"{s}: fee schedule taker {fz[s]['taker_bps_side']} != the ride's "
                      f"{T9.RC.FEE_BPS_SIDE} [L-1.1]")
        _MEMO["fees"] = fz
    return _MEMO["fees"]


def haircut(sym: str, net_r: float, fee_r: float) -> float:
    fz = _fees()[sym]
    return float(net_r) - float(fee_r) * (fz["slippage_bps_side"] / fz["taker_bps_side"])


def regbook_frame(book: list) -> pd.DataFrame:
    """The interface schema from Trade objects of a WALKED ride (1h-resolved exits),
    full precision, sorted by (symbol, entry_close_ms)."""
    rows = []
    for t in book:
        ec = int(t.entry_ms) + MS_4H
        if int(getattr(t, "entry_close_ms", ec)) != ec:
            _halt("regbook_frame: a v6-derived entry that is not its bar's close")
        x = getattr(t, "exit_close_ms", None)
        if x is None:
            _halt("regbook_frame: a trade without its 1h-resolved exit")
        fz = _fees()[t.symbol]
        rows.append({"symbol": str(t.symbol), "entry_ms": int(t.entry_ms),
                     "entry_close_ms": ec, "direction": int(t.direction),
                     "entry_px": float(t.entry_px), "stop_px": float(t.stop_px),
                     "r_dist": float(t.r_dist), "exit_close_ms": int(t.exit_ms) + MS_4H,
                     "exit_reason": str(t.exit_reason), "net_r": float(t.net_r),
                     "gross_r": float(t.gross_r), "fee_r": float(t.fee_r),
                     "funding_r": float(t.funding_r),
                     "haircut_net_r": haircut(t.symbol, t.net_r, t.fee_r),
                     "era": E.era_of(ec), "lane": str(t.lane),
                     # extras
                     "arm_ms": int(t.arm_ms), "exit_bar_open_ms": int(t.exit_ms),
                     "exit_instant_ms": int(x),
                     "exit_px": float(t.exit_px),
                     "exit_resolved_by": str(t.exit_resolved_by),
                     "acted_by": str(t.acted_by), "mfe_r": float(t.mfe_r),
                     "reached_1r": bool(t.reached_1r), "harvested": bool(t.harvested),
                     "n_walk_mismatch": int(t.n_walk_mismatch),
                     "slip_bps_side": float(fz["slippage_bps_side"]),
                     "slip_tier": str(fz["slippage_tier"]),
                     "as_of_last_closed_4h": PIN_ISO})
    d = pd.DataFrame(rows)
    d["direction"] = d["direction"].astype("int8")
    for c in REQ_INT + ("arm_ms", "exit_bar_open_ms", "exit_instant_ms", "n_walk_mismatch"):
        d[c] = d[c].astype("int64")
    d = d.sort_values(["symbol", "entry_close_ms"], kind="mergesort").reset_index(drop=True)
    return d


def _cell(v) -> str:
    if isinstance(v, (bool, np.bool_)):
        return str(bool(v))
    if isinstance(v, (int, np.integer)):
        return str(int(v))
    if isinstance(v, (float, np.floating)):
        return repr(float(v))
    return str(v)


def canonical_csv(d: pd.DataFrame) -> str:
    """BOOK_SHA_LAW's CSV (the required columns only)."""
    x = d[list(REQUIRED)].sort_values(["symbol", "entry_close_ms"], kind="mergesort")
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(REQUIRED)
    for row in x.itertuples(index=False, name=None):
        w.writerow([_cell(v) for v in row])
    return buf.getvalue()


def book_sha256(d: pd.DataFrame) -> str:
    return hashlib.sha256(canonical_csv(d).encode("utf-8")).hexdigest()


def n_straddle(entry_ms, entry_close_ms) -> int:
    """L-1.3: entry bars straddling the era cut (open <= cut < close), a count."""
    o = np.asarray(entry_ms, dtype=np.int64)
    c = np.asarray(entry_close_ms, dtype=np.int64)
    return int(((o <= int(E.ERA_CUT_MS)) & (c > int(E.ERA_CUT_MS))).sum())


def arm_sidecar(arm: str, kind: str, d: pd.DataFrame, era_scope: str, desc: str) -> dict:
    j = {"registration": REG, "arm": arm, "kind": kind, "ruler": "paired",
         "panel": list(E.CLASSIC5), "era_scope": era_scope, "n": int(len(d)),
         "sum_net_r": float(d["net_r"].sum()), "book_sha256": book_sha256(d),
         "n_entry_bar_straddles_era_cut": n_straddle(d["entry_ms"], d["entry_close_ms"]),
         "era_cut_ms": int(E.ERA_CUT_MS),
         "description": desc, "source_script": "scripts/tierc11_stage_w.py",
         "book_sha256_law": BOOK_SHA_LAW, "haircut_law": HAIRCUT_LAW,
         "exit_close_ms_law": EXIT_CLOSE_LAW,
         "required_columns": list(REQUIRED), "pairing_key": ["symbol", "entry_ms"],
         "registration_payload_sha256": REG_PAYLOAD_SHA,
         "honesty_labels": {"pre_seen": None, "selection_hazard": None,
                            "scale_in_sample": None,
                            "note": "REGISTRATIONS.json carries none for P-WARN-1"},
         "as_of": PIN_ISO, "seed": SEED}
    if kind == "tierE":
        j.update({"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
                  "gates": "nothing"})
    return j


def arms(rd: dict, cond: dict) -> dict:
    """{arm: (frame, sidecar)} [the REGBOOK INTERFACE]."""
    rule = regbook_frame(rd["rule"])
    base = regbook_frame(rd["walked"])
    met = bool(cond["met"])
    out = {}
    rule_desc = ("the WARN rule book [L-W.5]: every v6 campaign walked on its 1h children "
                 "(L-W.0); per child STOP -> +1R latch -> at the child's close, if pre-+1R "
                 "and a counter EMA12/EMA89 1h cross closed: exit at that 1h close; v6's "
                 "BELL / HARVEST / TRAIL at 4h closes unchanged; the set kept (paired); "
                 "identity law on untouched campaigns [L-1.5]")
    if met:
        out["scored"] = (rule, arm_sidecar("scored", "scored", rule, "full", rule_desc))
    else:
        nm = "tierE__rule_book_condition_not_met"
        out[nm] = (rule, arm_sidecar(nm, "tierE", rule, "full",
                                     rule_desc + " — CONDITION NOT MET: report-only, no slot "
                                     "spent [L-W.4, L-W.5]"))
    out["base"] = (base, arm_sidecar("base", "base", base, "full",
                                     "card v6 over the TC11 corridor (the paired base: the "
                                     "same campaigns, v6's exits; exit_close_ms the 4h "
                                     "exit-bar close as books/v6_campaigns.parquet, "
                                     "exit_instant_ms 1h-resolved by the walked identity "
                                     "ride; net_r identical at 0.000e+00) [L-1.6, L-1.5]"))
    for era in ("tuning", "holdout"):
        sl = rule[rule["era"] == era].reset_index(drop=True)
        nm = f"tierE__{era}"
        out[nm] = (sl, arm_sidecar(nm, "tierE", sl, era,
                                   f"the rule book, {era} slice (era by the entry close, "
                                   f"L-1.3) — paired against base on the same keys; a "
                                   f"SELECTION, not a result"))
    return out


def complement_table(c: pd.DataFrame) -> pd.DataFrame:
    """The complement comparison (a Tier-E arm of P-WARN-1): v6 vs the rule book on
    the C1 cohort, its complement, the acted / unacted campaigns and ALL."""
    rows = []
    v6 = c["net_r"].to_numpy(float)
    rl = c["rule_net_r"].to_numpy(float)
    v6h = c["haircut_net_r"].to_numpy(float)
    rlh = c["rule_haircut_net_r"].to_numpy(float)
    mem = c["C1_member"].to_numpy(bool)
    act = (c["rule_exit_reason"] == WARN_LABEL).to_numpy()
    groups = {"cohort_C1": mem, "complement_C1": ~mem, "acted": act, "unacted": ~act,
              "ALL": np.ones(len(c), bool)}
    for g in COMP_GROUPS:
        for era in ERAS:
            m = groups[g] & _era_mask(c, era)
            n = int(m.sum())
            dl = rl[m] - v6[m]
            rows.append({"cell": f"{g}|{era}", "group": g, "era": era, "n": n,
                         "sum_v6_r": float(v6[m].sum()), "sum_rule_r": float(rl[m].sum()),
                         "mean_v6_r": float(v6[m].mean()) if n else float("nan"),
                         "mean_rule_r": float(rl[m].mean()) if n else float("nan"),
                         "mean_delta_r": float(dl.mean()) if n else float("nan"),
                         "sum_delta_r": float(dl.sum()),
                         "sum_v6_haircut_r": float(v6h[m].sum()),       # AM-7 (w11)
                         "sum_rule_haircut_r": float(rlh[m].sum()),
                         "n_v6_win": int((v6[m] > 0).sum()),
                         "n_rule_win": int((rl[m] > 0).sum()),
                         "nan_reason": "" if n else "n=0: no campaign in this cell",
                         **COLLAR})
    return pd.DataFrame(rows)


def reride_disclosure(rd: dict) -> dict:
    """L-1.5: a freed slot admits nothing; the re-ride rival as a DISCLOSURE COUNT —
    per acted campaign, v6's triggered candidates on that asset with warn-exit bar <
    ti <= v6's exit bar (replay9's open_until law), with a valid stop."""
    lo, hi, _ = corridor()
    cands = {}
    for s in E.CLASSIC5:
        lo_i, hi_i, _n = B.ride_bounds(s, ROLES, lo, hi)
        cands[s] = [(int(ti), int(d)) for ti, d, _a in T9.card_candidates9(s, ROLES, lo_i,
                                                                             hi_i)[1]]
    n_camp = n_cand = n_valid = 0
    first = []
    for t, r in zip(rd["base"], rd["rule"]):
        if str(r.exit_reason) != WARN_LABEL:
            continue
        st = T9.frame(t.symbol)
        f = st["f"]
        hits = [(ti, d) for ti, d in cands[t.symbol] if int(r.exit_i) < ti <= int(t.exit_i)]
        valid = []
        for ti, d in hits:
            a = float(f.atr[ti])
            if not (np.isfinite(a) and a > 0):
                continue
            stp = T9.RC.struct_stop_4h(st["pv4"], ti, float(f.c[ti]), d, a,
                                       min_stop_atr=CARD.entry_rail_atr, forbidden=None)
            if stp is not None and np.isfinite(stp.r_dist) and stp.r_dist > 0:
                valid.append((ti, d))
        n_cand += len(hits)
        n_valid += len(valid)
        if valid:
            n_camp += 1
            first.append(f"{t.symbol} {iso(int(t.entry_ms))} -> would admit "
                         f"{iso(int(f.open_ms[valid[0][0]]))} d{valid[0][1]:+d}")
    return {"acted_campaigns_with_a_freed_slot_candidate": n_camp,
            "freed_slot_candidates": n_cand, "freed_slot_candidates_valid_stop": n_valid,
            "first_per_campaign": first,
            "law": "L-1.5: the freed slot admits NOTHING in the rule book; this count is "
                   "the re-ride rival's disclosure (chain effects of a re-ride not ridden)"}


def c3_strict_disclosure(c: pd.DataFrame) -> dict:
    """(w10) C3 (any with-trend 9/12 cross) vs C3S (strict re-cross): the members
    whose FIRST C3 event is not a strict re-cross (the 9/12 was counter-side at the
    entry close), and any membership difference."""
    m3 = c["C3_member"].to_numpy(bool)
    m3s = c["C3S_member"].to_numpy(bool)
    if bool((m3s & ~m3).any()):
        _halt("(w10) a strict re-cross member outside C3")
    f3 = c["C3_first_taken_ms"].astype("Int64")
    f3s = c["C3S_first_taken_ms"].astype("Int64")
    moved = [f"{s} {iso(int(e))}" for s, e, a, x, y in zip(c["symbol"], c["entry_ms"], m3, f3,
                                                              f3s)
             if a and (pd.isna(y) or int(x) != int(y))]
    only3 = [f"{s} {iso(int(e))}" for s, e, a, b in zip(c["symbol"], c["entry_ms"], m3, m3s)
             if a and not b]
    return {"c3_members": int(m3.sum()), "c3s_members": int(m3s.sum()),
            "members_first_event_not_strict": moved, "n_first_event_not_strict": len(moved),
            "c3_members_not_c3s": only3,
            "note": "C3 is the reading of record for the W2 tables (w10, the first build's "
                    "reading); C3S is printed beside it and decides nothing"}


def warn_on_harvest_close(rd: dict) -> list:
    """Acted campaigns whose warn exit falls ON the close of the 4h bar where v6
    harvested (the last child of v6's harvest bar): the ride books the child's warn
    exit before the 4h close's HARVEST slot, so the rule book books no harvest there
    (a verifier observation, printed)."""
    out = []
    for t, r in zip(rd["base"], rd["rule"]):
        if str(r.exit_reason) != WARN_LABEL or not bool(t.harvested):
            continue
        hclose = int(T9.frame(t.symbol)["f"].open_ms[int(t.harvest_i)]) + MS_4H
        if int(r.exit_close_ms) == hclose:
            out.append({"key": f"{t.symbol} {iso(int(t.entry_ms))}",
                        "warn_exit_instant": iso(int(r.exit_close_ms)),
                        "warn_exit_px": float(r.exit_px), "v6_harvest_px": float(t.harvest_px),
                        "abs_px_diff": abs(float(r.exit_px) - float(t.harvest_px)),
                        "rule_harvested": bool(r.harvested),
                        "rule_net_r": float(r.net_r), "v6_net_r": float(t.net_r)})
    return out


# ════════════════════════════════════════════════════════════════ COMPUTE
def compute() -> dict:
    lo, hi, meta = corridor()
    rd = rides()
    W = w1(rd)
    ctab = campaign_table(W["camps"])
    idf, ist = RD.identity_findings(rd["base"], rd["rule"])
    if idf:
        _halt(f"IDENTITY [L-1.5]: {idf[:3]}")
    acted = ctab["rule_exit_reason"] == WARN_LABEL
    if int(acted.sum()) != int(ist["acted"]):
        _halt("the acted count is not the warn-exit count")
    # (w5) for the P-WARN-1 cohort the mark IS the rule book's net R
    both = ctab["C1_member"].to_numpy(bool) & acted.to_numpy()
    dm = (ctab.loc[both, "C1_mark_r"].to_numpy(float)
          - ctab.loc[both, "rule_net_r"].to_numpy(float))
    if len(dm) and float(np.abs(dm).max()) != 0.0:
        _halt(f"the C1 mark is not the rule book's net R (worst {np.abs(dm).max():.3e})")
    ev = pd.DataFrame(W["events"])
    ev["on_mismatch_bar"] = ev["on_mismatch_bar"].astype(bool)
    for k, v in COLLAR.items():
        ev[k] = v
    tl = pd.DataFrame(W["timeline"])
    for k, v in COLLAR.items():
        tl[k] = v
    cw = ctab.copy()
    for k, v in COLLAR.items():
        cw[k] = v
    v6_keys = {(t.symbol, int(t.entry_ms)) for t in rd["base"]}
    twin, twin_chk = relay_twin_windows(v6_keys)
    for k, v in COLLAR.items():
        twin[k] = v
    pops = {"v6_campaigns": relay_windows(ctab), "armed_windows_not_entered": twin}
    cond = condition(ctab, rd)
    A = arms(rd, cond)
    tables = {
        "W1_EVENTS": ev, "W1_TIMELINE": tl, "W1_CAMPAIGNS": cw,
        "W2_COHORTS": w2_cohorts(ctab), "W2_FORWARD": w2_forward(ctab),
        "W2_PREENTRY": w2_preentry(ctab),
        "W2_RELAY_WINDOWS": pops["v6_campaigns"],
        "W2_RELAY_WINDOWS_TWIN": pops["armed_windows_not_entered"],
        "W2_RELAY_SUMMARY": relay_summary(pops), "W2_RELAY_HIST": relay_hist(pops),
        "P_WARN_1_COMPLEMENT": complement_table(ctab),
    }
    mism_rule = sorted({f"{t.symbol} {iso(int(ms))}" for t in rd["rule"]
                        for ms in t.walk_mismatch_ms})
    disclosures = {
        "identity_rule": ist, "identity_walked": rd["identity_walked"],
        "ctrl_worst_walked": rd["ctrl_worst_walked"],
        "n_walk_mismatch_rule_book": int(sum(int(t.n_walk_mismatch) for t in rd["rule"])),
        "n_walk_mismatch_base": int(sum(int(t.n_walk_mismatch) for t in rd["walked"])),
        "walk_mismatch_bars_ridden_rule_book": mism_rule,
        "latch_readings_agree": int(ctab["latch_readings_agree"].sum()),
        "latch_vs_v6_reached_1r_agree": int((ctab["reached_1r"]
                                             == ctab["reached_1r_v6"]).sum()),
        "events_raw_instant_changes_class": int(ev["raw_instant_changes_class"].sum()),
        "events_on_mismatch_bars": int(ev["on_mismatch_bar"].sum()),
        "reride": reride_disclosure(rd),
        "relay_twin_check": twin_chk,
        "exit_resolved_by_base": {k: int(v) for k, v in
                                  ctab["exit_resolved_by"].value_counts().sort_index().items()},
        "phase_counts": {k: int(v) for k, v in ev["phase"].value_counts().sort_index().items()},
        "c3_strict": c3_strict_disclosure(ctab),
        "warn_exit_on_v6_harvest_bar_close": warn_on_harvest_close(rd),
        "straddle_era_cut": {
            "law": "L-1.3: a bar straddling the era cut (open <= 2024-06-30T23:59:59Z < close) "
                   "is printed as a count",
            "v6_campaign_entry_bars": n_straddle(ctab["entry_ms"],
                                                 ctab["entry_close_ms"]),
            "twin_window_end_bars": n_straddle(twin["end_close_ms"] - MS_4H,
                                               twin["end_close_ms"])},
    }
    return {"lo": lo, "hi": hi, "meta": meta, "rides": rd, "campaigns": ctab,
            "tables": tables, "condition": cond, "arms": A, "disclosures": disclosures}


# ════════════════════════════════════════════════════════════════ WRITING
def _inside(p: Path, root: Path) -> bool:
    return p == root or root in p.parents


def _guard_out(out: Path) -> Path:
    o = Path(out).resolve()
    if o == OUT.resolve() or o.parent == DET_ROOT.resolve():
        return o
    trees = {ROOT.resolve(), Path(E.MAIN_TREE).resolve()}
    if o.parent.name == DET_ROOT.name and not any(_inside(o, t) for t in trees):
        return o
    _halt(f"output dir {o} is neither {OUT}, an F-DET run dir under {DET_ROOT}, nor one "
          f"under a {DET_ROOT.name}/ scratch outside the repo")
    return o


def reg_dir_for(out: Path) -> Path:
    o = Path(out).resolve()
    return REG_DIR if o == OUT.resolve() else o / "regbooks" / REG


def _write_parquet(d: pd.DataFrame, p: Path) -> None:
    tmp = p.with_suffix(".parquet.tmp")
    d.to_parquet(str(tmp), index=False)
    os.replace(tmp, p)


def _jdump(x) -> str:
    return json.dumps(x, indent=2, sort_keys=True, default=str, ensure_ascii=False) + "\n"


def registration_check() -> None:
    """The registration of record is the one this stage builds (payload sha pinned)."""
    regs = json.loads((E.OUT / "registrations" / "REGISTRATIONS.json").read_text(
        encoding="utf-8"))
    r = next((x for x in regs["registrations"] if x["registration"] == REG), None)
    if r is None or r["sha256"] != REG_PAYLOAD_SHA:
        _halt(f"{REG}'s payload sha is not {REG_PAYLOAD_SHA[:12]}… — not the registration "
              f"of record")
    for k in ("pre_seen", "selection_hazard", "scale_in_sample"):
        if r["operative_spec"].get(k) is not None:
            _halt(f"{REG} carries {k}; the sidecar's honesty labels would lie")


def build(out: Path = OUT) -> dict:
    out = _guard_out(out)
    registration_check()
    rdir = reg_dir_for(out)
    R = compute()
    out.mkdir(parents=True, exist_ok=True)
    rdir.mkdir(parents=True, exist_ok=True)
    put, Wsha, K, SK = TP.make_put(out, R["meta"], lens="4h")
    for name, (key, lens) in TABLES.items():
        put(R["tables"][name], name, key, lens_=lens)
    if SK:
        _halt(f"an empty table: {SK}")
    reg_files = {}
    for arm, (d, side) in R["arms"].items():
        _write_parquet(d, rdir / f"{arm}.parquet")
        (rdir / f"{arm}.json").write_text(_jdump(side), encoding="utf-8")
        reg_files[arm] = {"n": side["n"], "sum_net_r": side["sum_net_r"],
                          "book_sha256": side["book_sha256"], "kind": side["kind"]}
    cond = R["condition"]
    (rdir / "condition.json").write_text(_jdump(cond), encoding="utf-8")
    met = bool(cond["met"])
    status = {
        "registration": REG,
        "status": "BUILT" if met else "CONDITION_NOT_MET",
        "reason": (f"condition MET: delta {cond['delta']:+.6f}, cluster-90% "
                   f"[{cond['ci_lo']:+.6f}, {cond['ci_hi']:+.6f}] (hi < 0); the rule book "
                   f"is the scored arm, paired vs v6" if met else
                   f"condition NOT MET: delta {cond['delta']:+.6f}, cluster-90% "
                   f"[{cond['ci_lo']:+.6f}, {cond['ci_hi']:+.6f}] (hi >= 0) — "
                   f"report-only, no slot spent, stated [L-W.4]; the rule book is printed "
                   f"only as a collared Tier-E arm"),
        "arms": list(R["arms"]),
        "ruler": "paired",
        "condition_path": f"research_outputs/tierc11/regbooks/{REG}/condition.json",
        "tier_e_tables": {
            "complement_comparison": "research_outputs/tierc11/stage_w/"
                                     "P_WARN_1_COMPLEMENT.parquet",
            "forward_leg": "research_outputs/tierc11/stage_w/W2_FORWARD.parquet "
                           "(cells C1_counter_12_89_before_1r|*)",
            "cohorts": "research_outputs/tierc11/stage_w/W2_COHORTS.parquet"},
        "identity": R["disclosures"]["identity_rule"],
        "n_walk_mismatch_rule_book": R["disclosures"]["n_walk_mismatch_rule_book"],
        "reride_disclosure": R["disclosures"]["reride"],
        "as_of": PIN_ISO, "seed": SEED,
    }
    (rdir / "STATUS.json").write_text(_jdump(status), encoding="utf-8")
    man = {
        "tier": "TIER-C11", "stage": "TC11-W", "seed": SEED, "n_boot": N_BOOT,
        "as_of": PIN_ISO, "as_of_close_ms": PIN_MS,
        "corridor": {"lo": iso(R["lo"]), "hi_close": iso(R["hi"] + 1),
                     "panel": list(E.CLASSIC5)},
        "substrate": R["meta"]["substrate"], "input_sha": TP.input_sha(E.CLASSIC5),
        "sha": Wsha, "keys": K, "skipped_empty": SK,
        "float_precision": "stage_w tables: floats rounded to 6 dp at write "
                           "(tierc2_baseline.write_table via TP.make_put); regbooks: full "
                           "precision",
        "regbooks": {"dir": f"research_outputs/tierc11/regbooks/{REG}", "arms": reg_files,
                     "status": status["status"]},
        "condition": {k: cond[k] for k in ("cohort_n", "cohort_mean", "book_mean", "delta",
                                           "ci_lo", "ci_hi", "met", "seed", "n_boot")},
        "disclosures": R["disclosures"],
        "changes_after_first_output": list(CHANGES_AFTER_FIRST_OUTPUT),
        "changes_note": CHANGES_NOTE,
        "collar": COLLAR, "readings": list(READINGS),
        "books_manifest_book_sha_v6": json.loads(
            (B.OUT / B.MANIFEST).read_text(encoding="utf-8"))["book_sha"]["v6"],
        "book_sha_v6_live": B.book_sha(R["rides"]["base"]),
    }
    if man["books_manifest_book_sha_v6"] != man["book_sha_v6_live"]:
        _halt("the live v6 book is not the filed TC11-BOOKS v6 book")
    (out / MANIFEST).write_text(_jdump(man), encoding="utf-8")
    (out / REPORT).write_text(render_md(R, Wsha, reg_files, status), encoding="utf-8")
    R["manifest"], R["status"] = man, status
    return R


# ════════════════════════════════════════════════════════════════ THE REPORT
def _f(x, nd: int = 4) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    if isinstance(x, (int, np.integer)) and not isinstance(x, bool):
        return str(int(x))
    return f"{float(x):+.{nd}f}"


def _md_table(d: pd.DataFrame, cols: list, fmt: dict | None = None) -> list[str]:
    fmt = fmt or {}
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in d.itertuples(index=False):
        cells = []
        for c in cols:
            v = getattr(r, c)
            if c in fmt:
                cells.append(fmt[c](v))
            elif isinstance(v, (float, np.floating)):
                cells.append(_f(v))
            elif v is None or (v is pd.NA):
                cells.append("—")
            else:
                cells.append(str(v).replace("|", "\\|"))
        out.append("| " + " | ".join(cells) + " |")
    return out


def _pct(v) -> str:
    return "—" if v is None or not np.isfinite(float(v)) else f"{100 * float(v):.1f}%"


def render_md(R: dict, Wsha: dict, reg_files: dict, status: dict) -> str:
    T, cond, dis = R["tables"], R["condition"], R["disclosures"]
    L = [f"as_of_last_closed_4h: {PIN_ISO}", "",
         "# TIER-C11 · STAGE W — early warnings from the 1h crosses", "",
         "Contract: exchange/queue/2026-09-24_TC11_APOLLO.md (bb38e016…) STAGE W. Readings "
         "L-W.0..L-W.6, L-1.5, AM-3, AM-5, AM-6, AM-7. Seed 20260924 (sensitivity 20260816), "
         "N_BOOT 4000. Corridor " + f"{iso(R['lo'])} → {iso(R['hi'] + 1)}, CLASSIC5.", "",
         "Every table below except the P-WARN-1 condition block and the regbook arms is "
         "Tier-E — tier TIER-E · a SELECTION, not a result · gates nothing — and carries no "
         "verdict word. Every grid is printed whole.", "", "## Readings (executor)", ""]
    L += [f"- {x}" for x in READINGS]
    L += ["", "## Changes after first output (disclosed; no net_r moved)", "",
          f"({CHANGES_NOTE}.)", "",
          "| id | what | first output | now | why | what moved |", "|---|---|---|---|---|---|"]
    L += [f"| {c['id']} | {c['what']} | {c['first_output']} | {c['now']} | {c['why']} | "
          f"{c['moved']} |" for c in CHANGES_AFTER_FIRST_OUTPUT]
    L += ["", "Repair of 2026-09-25 (the Stage W verifier's MINOR findings; no rule, cohort, "
          "condition number or registered figure moved): the (w7) docstring rewritten to the "
          "twin as built; this block; AM-7 haircut columns beside every per-campaign net R "
          "(w11); condition.json's collar `gates` set to 'nothing' with the gating statement "
          "moved to `condition_role`; `cohort_law_holds` computed by the frozen law (belltie "
          "keys listed separately, never absorbed); the C3 reading disclosed as (w10) with the "
          "strict reading C3S printed beside; the L-1.3 straddle count printed; fixtures "
          "extended (independent marks, relay leads and twin windows hand-walked, mismatch "
          "plants on every C1 first event and on latch / stop-exit bars, timeline columns).",
          "", "## P-WARN-1 · the condition block (the only Tier-E place a CI is printed)", "",
          f"- cohort (v6 campaigns with an IN-TRADE counter 12/89 1h cross before the +1R "
          f"latch): n {cond['cohort_n']}, mean net R {_f(cond['cohort_mean'])}",
          f"- whole v6 book: n {cond['book_n']}, mean net R {_f(cond['book_mean'])}",
          f"- delta = mean(cohort) − mean(book) = {_f(cond['delta'], 6)}; cluster-90% "
          f"[{_f(cond['ci_lo'], 6)}, {_f(cond['ci_hi'], 6)}] (seed {SEED}, n_boot {N_BOOT})",
          f"- condition MET (ci_hi < 0): **{cond['met']}** → STATUS "
          f"**{status['status']}**",
          f"- sensitivity seed {SEED_SENS}: [{_f(cond['sens_seed_ci']['lo'], 6)}, "
          f"{_f(cond['sens_seed_ci']['hi'], 6)}] (hi < 0: "
          f"{cond['sens_seed_ci']['met_at_sens_seed']}) — decides nothing",
          f"- rival (cohort vs complement, w9): complement n "
          f"{cond['rival_complement']['complement_n']}, delta "
          f"{_f(cond['rival_complement']['delta'], 6)}, cluster-90% "
          f"[{_f(cond['rival_complement']['ci_lo'], 6)}, "
          f"{_f(cond['rival_complement']['ci_hi'], 6)}] — decides nothing",
          f"- cohort law (the frozen L-W.4 law; fixture F-WARN-COHORT): warn-exit keys "
          f"{len(cond['warn_exit_keys'])}, cohort keys {cond['cohort_n']}, listed mismatch-bar "
          f"keys {cond['listed_mismatch_keys'] or 'none'}; cohort == warn ∪ mismatch: "
          f"{cond['cohort_law_holds']}. Belltie keys (listed separately, never absorbed): "
          f"{cond['belltie_n']} {cond['listed_belltie_keys'] or ''}".rstrip(),
          f"- collar: tier {cond['tier']} · {cond['selection_not_a_result']} · gates "
          f"{cond['gates']}; role: {cond['condition_role']}",
          "", "Per asset (cohort vs book):", "",
          "| asset | cohort n | cohort mean | book n | book mean |", "|---|---|---|---|---|"]
    for s, v in cond["per_asset"].items():
        L.append(f"| {s} | {v['cohort_n']} | {_f(v['cohort_mean'])} | {v['book_n']} | "
                 f"{_f(v['book_mean'])} |")
    L += ["", "## P-WARN-1 · the regbook arms (book, not a verdict)", "",
          "| arm | kind | era_scope | n | sum net R | mean net R | sum haircut R | entry bars "
          "straddling the era cut | book_sha256 |",
          "|---|---|---|---|---|---|---|---|---|"]
    for arm, (d, side) in R["arms"].items():
        L.append(f"| {arm} | {side['kind']} | {side['era_scope']} | {side['n']} | "
                 f"{_f(side['sum_net_r'])} | "
                 f"{_f(side['sum_net_r'] / side['n']) if side['n'] else '—'} | "
                 f"{_f(float(d['haircut_net_r'].sum()))} | "
                 f"{side['n_entry_bar_straddles_era_cut']} | "
                 f"{side['book_sha256'][:16]}… |")
    L += ["", "All rows are books, not verdicts. The scorer (scripts/tierc11_score.py) reads "
          "the regbook dir.", "",
          f"- identity law (L-1.5) on the rule book: {dis['identity_rule']}; walked v6 "
          f"(no rule): {dis['identity_walked']}, CTRL_COLS worst "
          f"{dis['ctrl_worst_walked']:.3e}",
          f"- mismatch bars ridden (AM-5): rule book {dis['n_walk_mismatch_rule_book']}, base "
          f"{dis['n_walk_mismatch_base']}: {dis['walk_mismatch_bars_ridden_rule_book'] or 'none'}",
          f"- re-ride rival (L-1.5 disclosure): {dis['reride']['acted_campaigns_with_a_freed_slot_candidate']} "
          f"acted campaigns hold a freed-slot candidate "
          f"({dis['reride']['freed_slot_candidates']} candidates, "
          f"{dis['reride']['freed_slot_candidates_valid_stop']} with a valid stop); the rule "
          f"book admits none",
          f"- the two +1R latch readings (AM-6) agree on {dis['latch_readings_agree']}/"
          f"{len(R['campaigns'])}; latch present == v6 reached_1r on "
          f"{dis['latch_vs_v6_reached_1r_agree']}/{len(R['campaigns'])}",
          f"- events on mismatch bars (taken at the parent close, w1): "
          f"{dis['events_on_mismatch_bars']}; classifications the raw instant would change: "
          f"{dis['events_raw_instant_changes_class']}",
          f"- W1 phase counts: {dis['phase_counts']}; base exits resolved by "
          f"{dis['exit_resolved_by_base']}",
          f"- L-1.3 straddle counts (open <= the era cut < close): v6 campaign entry bars "
          f"{dis['straddle_era_cut']['v6_campaign_entry_bars']}; twin-window end bars "
          f"{dis['straddle_era_cut']['twin_window_end_bars']}; per arm in the table above",
          f"- (w10) C3 vs its strict reading C3S: C3 members "
          f"{dis['c3_strict']['c3_members']}, C3S members {dis['c3_strict']['c3s_members']}; "
          f"members whose FIRST C3 event is not a strict re-cross (the 9/12 counter-side at "
          f"the entry close): {dis['c3_strict']['n_first_event_not_strict']} "
          f"{dis['c3_strict']['members_first_event_not_strict'] or ''}; C3 members outside "
          f"C3S: {dis['c3_strict']['c3_members_not_c3s'] or 'none'} — C3S decides nothing",
          f"- warn exits ON the close of v6's harvest bar (the last child of that bar; the ride "
          f"books the child's warn exit before the 4h close's HARVEST slot, so the rule book "
          f"books no harvest there; the last child's close is the parent's close, the harvest "
          f"fill price): {len(dis['warn_exit_on_v6_harvest_bar_close'])}"]
    for x in dis["warn_exit_on_v6_harvest_bar_close"]:
        L.append(f"  - {x['key']}: warn exit {x['warn_exit_instant']} at {x['warn_exit_px']!r}; "
                 f"v6 harvest px {x['v6_harvest_px']!r} (|diff| {x['abs_px_diff']:.3e}); rule "
                 f"harvested {x['rule_harvested']}; rule net R {x['rule_net_r']:+.6f}, v6 net R "
                 f"{x['v6_net_r']:+.6f}")
    for x in dis["reride"]["first_per_campaign"]:
        L.append(f"  - re-ride candidate: {x}")
    ev = T["W1_EVENTS"]
    L += ["", "## W1 · the 1h event tape inside the v6 campaign windows (Tier-E, whole)", "",
          "Every 1h engine-EMA cross with arm close < taken <= the exit-bar close, by phase "
          "(L-W.3, w2) × pair × side (L-W.2); in-trade rows split by the +1R latch relation.",
          "", "| phase | pair | side | latch | n events | n campaigns |",
          "|---|---|---|---|---|---|"]
    for ph in PHASES:
        for p_, _, _ in PAIRS:
            for sd in ("counter", "with"):
                rels = ("before", "after") if ph == "IN-TRADE" else (None,)
                for rl in rels:
                    m = (ev["phase"] == ph) & (ev["pair"] == p_) & (ev["side"] == sd)
                    if rl is not None:
                        m &= ev["latch_rel"] == rl
                    sub = ev[m]
                    L.append(f"| {ph} | {p_} | {sd} | {rl or '—'} | {len(sub)} | "
                             f"{sub[['symbol', 'entry_ms']].drop_duplicates().shape[0]} |")
    L += ["", "## P_WARN_1_COMPLEMENT (Tier-E arm; v6 vs the rule book)", ""]
    L += _md_table(T["P_WARN_1_COMPLEMENT"],
                   ["cell", "n", "sum_v6_r", "sum_rule_r", "mean_v6_r", "mean_rule_r",
                    "mean_delta_r", "sum_delta_r", "sum_v6_haircut_r", "sum_rule_haircut_r",
                    "n_v6_win", "n_rule_win"])
    L += ["", "## W2 · post-entry cohorts vs their at-risk sets (Tier-E, whole)", ""]
    L += [f"- {k}: {v}" for k, v in AT_RISK_TEXT.items()]
    L += [""] + _md_table(T["W2_COHORTS"],
                          ["cell", "n", "n_win", "p_win", "mean_net_r", "sum_net_r",
                           "mean_minus_at_risk_mean"], {"p_win": _pct})
    L += ["", "## W2 · the forward leg E[final net R − R marked at the event] (Tier-E, whole)",
          ""]
    L += _md_table(T["W2_FORWARD"], ["cell", "n", "mean_final_net_r", "mean_mark_r",
                                     "mean_fwd_r", "sum_fwd_r", "n_fwd_pos", "p_fwd_pos"],
                   {"p_fwd_pos": _pct})
    L += ["", "## W2 · PRE-ENTRY classes in (arm close, entry close] vs the whole book "
          "(Tier-E, whole)", ""]
    L += _md_table(T["W2_PREENTRY"], ["cell", "n", "n_events", "n_win", "p_win", "mean_net_r",
                                      "sum_net_r", "mean_minus_whole_book_mean"],
                   {"p_win": _pct})
    L += ["", "## W2 · relay evidence [L-W.6] (Tier-E, whole)", ""]
    L += _md_table(T["W2_RELAY_SUMMARY"],
                   ["cell", "n_windows", "n_lag0", "n_relay_cross", "share_relay_cross"]
                   + [f"lead_1h_{s}" for s in LEAD_STATS] + [f"lead_4h_{s}" for s in LEAD_STATS],
                   {"share_relay_cross": _pct,
                    **{f"lead_{m}_{s}": (lambda v: "—" if not np.isfinite(float(v))
                                         else f"{float(v):.2f}")
                       for m in ("1h", "4h") for s in LEAD_STATS}})
    L += ["", "Lead distributions, binned (whole):", ""]
    L += _md_table(T["W2_RELAY_HIST"], ["cell", "n"])
    L += ["", "Per v6 window (the whole distribution):", ""]
    rw = T["W2_RELAY_WINDOWS"]
    L += _md_table(rw.assign(entry=rw["entry_ms"].map(lambda x: iso(int(x))),
                             relay=rw["relay_close_ms"].map(
                                 lambda x: "—" if pd.isna(x) else iso(int(x)))),
                   ["symbol", "entry", "direction", "era", "lag", "relay_cross", "relay",
                    "relay_on_mismatch_bar", "relay_lead_1h", "relay_lead_4h"])
    tc = dis["relay_twin_check"]
    L += ["", f"Twin population (w7) — armed windows of v6's card holding no v6 campaign: "
          f"triggered gate-passing windows {tc['triggered_gate_passing_windows']} vs v6 "
          f"campaign windows {tc['v6_campaign_windows']} (identical sets: "
          f"{tc['triggered_equals_v6_set']}; triggered, not entered: "
          f"{tc['triggered_not_entered'] or 'none'}); twin windows by end kind "
          f"{tc['twin_windows_by_end_kind']}. Per twin window (the whole distribution):", ""]
    tw = T["W2_RELAY_WINDOWS_TWIN"]
    L += _md_table(tw.assign(arm=tw["arm_ms"].map(lambda x: iso(int(x))),
                             end=tw["end_close_ms"].map(lambda x: iso(int(x))),
                             relay=tw["relay_close_ms"].map(
                                 lambda x: "—" if pd.isna(x) else iso(int(x)))),
                   ["symbol", "arm", "direction", "end", "end_kind", "window_bars", "era",
                    "relay_cross", "relay", "relay_lead_1h", "relay_lead_4h"])
    L += ["", "## Files", "", "| table | content sha256 |", "|---|---|"]
    L += [f"| {k} | {v} |" for k, v in sorted(Wsha.items())]
    L += ["", "| regbook arm | n | sum net R | book_sha256 |", "|---|---|---|---|"]
    L += [f"| {k} | {v['n']} | {_f(v['sum_net_r'], 6)} | {v['book_sha256']} |"
          for k, v in reg_files.items()]
    L += ["", "W1_EVENTS / W1_TIMELINE / W1_CAMPAIGNS / W2_RELAY_WINDOWS_TWIN are filed whole "
          "as parquet (row counts in the manifest keys); every row is collared.", ""]
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    od = next((a.split("=", 1)[1] for a in args if a.startswith("--out-dir=")), None)
    R = build(Path(od) if od else OUT)
    c = R["condition"]
    print(f"STAGE W · P-WARN-1 condition: cohort n {c['cohort_n']} · delta {c['delta']:+.6f} "
          f"· cluster-90% [{c['ci_lo']:+.6f}, {c['ci_hi']:+.6f}] · met {c['met']} · STATUS "
          f"{R['status']['status']}")
    for arm, (d, side) in R["arms"].items():
        print(f"  {arm}: n {side['n']} · ΣR {side['sum_net_r']:+.6f} · book, not a verdict")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
