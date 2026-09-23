"""THE ORACLE — the daily organ. D-2 of queue BR-1 (RATIFIED operator 2026-08-16).
Since OR-1 STEP F (2026-09-21) it goes to press as THE DAILY ORACLE: see "THE
TYPESETTING" below. The organs and every number they print are BR-1's and OR-1's.

Amendment A1-1 names the product: "Oracle" unqualified is THIS daily organ.
The census-2B artifact is always "ORACLE GRID", fully qualified. Every
deliverable of this build is `oracle_*`.

Emits briefs/oracle/oracle_<date>.html containing, per BR-1 §3 as amended:

    BOARD        C-5  one row per ROSTER symbol (REGISTER['ROSTER'], the Oracle's
                      own constant since OR-1 STEP C — never a typed count),
                      heat-sorted: regime chip · ATR-distance to the
                      nearest high-score cluster · two lines in the sand ·
                      posture word · since OR-2 R-1 the row's OWN as-of bar
                      and age, STALE past A2-7's limit (row_ages).
    TRAP CARDS   C-6  entry · structural invalidation (4h-lens anchor + the
                      min 1.0 ATR rail) · target · net R:R after toll · what
                      proves me wrong. Derivation in the appendix.
    WATCH        C-7  live 12/89 windows (age, displacement, trigger status)
                      + a static last-96-bars mantle thumbnail per asset,
                      rendered FROM the v4 payload pattern.
    SPAGHETTI    C-4  event-anchored at each asset's last 89/316 tide flip,
                      ATR-normalised, one panel.
    GRID FOOTER  C-8  yesterday's fired events classified against the ORACLE
                      GRID's NET table, per lens.
    R1 ALERTS    C-9  alert-price blocks, TradingView paste-ready, prices only.
    PROVENANCE   F-BR-8  DISPLAY-ONLY header, payload shas, date, both the
                      certified and the not-certified lists.

and, since OR-1 STEP D (2026-09-21), one section that is not BR-1's:

    TIDE TABLES  OR-1 D  the RangeFinder v2 MACRO range per ROSTER symbol on the 4h
                      lens: state · top/bottom · % position · ATR-distance to the
                      nearest boundary · PENDING breach · last event + age; the
                      EDGE WATCH sub-list; and a RANGE cell on every Board row.
                      DISPLAY AND SIBLING-TAPE ONLY: see "THE RANGE LAYER" below.
                      No gate, filter, heat, station, card or sizing reads a range
                      (F-BR-14). The machine is scripts/rangefinder_core.py
                      (A-OR1-1 iv), never engine/.

and, since OR-1 STEP E (2026-09-21), one more that is not BR-1's:

    MARKET PAGE  OR-1 E  operator ruling 7: the top movers of the Binance USDT-M
                      perpetual universe, OVERNIGHT and THE WEEK, printed from the
                      ONE json the fetch-only organ scripts/oracle_movers.py wrote
                      for THIS edition's date. This file never imports that organ
                      and never fetches; any other document, or none, prints WIRE
                      DOWN and no numbers. DISPLAY ONLY: see "THE MARKET PAGE"
                      below. Nothing of it reaches the view, the tape or the
                      calibration record, and no gate, filter, heat, station, card
                      or sizing reads a mover (F-MV-8, F-MV-9).

and, beside the render, per run: the D-4 tape parquet and the D-7 calibration
JSON (display-machinery distributions only, A1-4) — and, since AMENDMENT A-OR1-1
clause v (operator, 2026-09-22), the range layer's SIBLING tape, one row per roster
symbol under research_outputs/oracle/tape_ranges/. The D-4 tape is TC4's event
tape and its schema is untouched (A-BR2-1b doctrine): its 24 columns are the
pre-OR-1 24, and from A-OR1-1 on it carries no range column (the one D-4 tape
written with 32, 2026-09-21's, is disclosed under "D-4 THE TAPE" below).

THE TYPESETTING — OR-1 STEP F (2026-09-21), "semantics untouched, template only". The
page is set as a newspaper, light paper only [D-7a], in the operator's eight sections
(REGISTER['SECTIONS']), in his order:

    FRONT PAGE            the BOARD (C-5) under a headline and a lead that restate
                          its posture column and nothing else
    THE DOCKET            the TRAP CARDS (C-6)
    THE WATCH             the WATCH (C-7), a caption under every mantle strip, and
                          the SPAGHETTI (C-4) as a sub-block
    TIDE TABLES           OR-1 D, EDGE WATCH inside it
    TELEGRAMS             the R1 ALERTS (C-9)
    THE MARKET PAGE       OR-1 E
    YESTERDAY'S RETURNS   the GRID FOOTER (C-8) and its disclaimer
    COLOPHON              PROVENANCE (F-BR-8, the <footer>) and the [VETO] appendix
                          as a sub-block

No number, posture word, level, card field, R1 line, grid row, sha or note moved:
only markup, order, headings and ink. The build document carries the block-by-block
comparison of this template against the pre-STEP-F one over one view; F-BR-15 pins
the sections, the captions, the colophon, the inks and the LATE EDITION band.

THE EDITION'S WORD — AMENDMENT A-OR1-1 clause vii (operator, 2026-09-22), verbatim:
"Edition word follows verb and hour: full before 12:00 BA = Morning, after = Evening;
refresh = Refresh. A paper printed at night does not call itself the morning's."
run() takes the print time ONCE, from the same `now` its date comes from, and hands it
to render_html; edition_name() reads its hour on the Buenos Aires wall clock
(print_time_ba: ZoneInfo(ZONE), never the machine's zone), and the Colophon prints
that time and the word it gave (print_line), so the edition carries its own evidence.
Template only: the ear's format is STEP F's, only its word follows the law (F-BR-15).

C-0, CLOSED AT OR-1 STEP B (2026-09-21). From 2026-08-16 the D-7 logger wrote
the LITERAL `"maturity_withheld_fraction": 0.0` for every asset on every run,
and recorded neither family-cap binding nor target buckets, although BR-2
WORK(1) names all three as families to recalibrate. The three are now MEASURED
(see "D-7 THE CALIBRATION LOGGER" below; F-BR-13 pins it). Every calibration
JSON written before this change — 57 files on the day it landed, none carrying
`schema_version` — is HOLLOW for those three families and is excluded from any
recalibration. Measuring is display-only: no level, score, heat, station or
card moved (old-vs-new tape, payloads, Board and Cards compared byte-identical).

════════════════════════════════════════════════════════════════════════════
CLASS AND FIREWALL — BR-1 §2, binding, reprinted in the rendered footer.

Operations/display-only. (1) Live data is operations-only, forbidden as study
evidence. (2) No journal reads; no signal-outcome statistics on any window.
(3) Engine modules imported read-only, trading disabled, never modified.
(4) The archive may be mined for hypotheses, never scored. RECORDING an event
is operations; AGGREGATING outcomes is census work under G-7.

This module reads `analytics/` (the measurement side) for levels, VWAP and
ATR. It does NOT let analytics touch a station: every posture word comes from
`posture_engine`, whose own import closure is analytics-free so the decision
path stays captured-not-consulted (F-C2-6). F-BR-3 asserts both properties.

WHAT THIS MODULE NEVER DOES: it never reads journal/, never imports
engine.trading, never counts a win or a loss, never scores a window.
"""
from __future__ import annotations

import hashlib
import html
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from engine.data import cache_dir                     # noqa: E402
from analytics import levels as L                     # noqa: E402
from analytics import structure as ST                 # noqa: E402
from analytics import volatility as VOL               # noqa: E402
from analytics import vwap as VW                      # noqa: E402
from analytics import ANALYTICS_VERSION, analytics_sha  # noqa: E402

import posture_engine as PE                           # noqa: E402
import census2b_program as P                          # noqa: E402
import tierc3_rules as V3                             # noqa: E402
# THE RANGE MACHINE (OR-1 STEP D; its home since AMENDMENT A-OR1-1 clause iv, operator
# 2026-09-22: "The range module lives at scripts/rangefinder_core.py; engine/ is outside
# this lane's write authority (BR-1 §2 clause 3); promotion into engine/ is APOLLO's
# call"). A display organ, imported the way this file imports its other siblings in
# scripts/. rangefinder_core imports numpy, pandas, dataclasses and engine.indicators
# (read-only) and nothing else, so it brings no journal, no outcome package and no
# decision module into this file's closure (F-BR-14 measures that, it is not taken on
# trust). engine/rangefinder.py — the copy OR-1 STEP D1 created — is NOT imported here
# any more and F-BR-14 goes red if it comes back: it stays byte-frozen as TIER-C10's
# machine of record, and F-RF-1c/d/e (scripts/rangefinder_core_fixtures.py: the event
# logs, snapshot parity, source equivalence) hold the two copies to one machine. THE
# ALIAS IS FENCED: F-BR-14 reads this file's AST and goes red on any use of `RNG`, or
# of a name the machine defines, outside range_layer() and the one REGISTER row that
# imports the machine's window, and on any route to a module that no import statement
# names (importlib, __import__, globals(), sys.modules, frames, gc, ...).
import rangefinder_core as RNG                        # noqa: E402
# THE TARGET BUCKETS ARE IMPORTED, NEVER COPIED (CONVENTIONS §6.4: "live
# consumers IMPORT from the one definition"). brief_render.TARGET_BUCKETS is
# the only bucket definition in the estate (NEAR 0-2 · MID 2-6 · FAR 6+ ATR).
# The pin-vs-import decision was MEASURED at OR-1 STEP B, 2026-09-21, not
# assumed: brief_render's import closure in a clean subprocess is 14 modules,
# all stdlib (argparse, html, json, pathlib, ...) — no engine, no analytics,
# no forward_log, no positions — so F-BR-3's firewall stays green and the
# import costs ~3 ms (3.2-3.6 ms over four clean-subprocess runs).
# THE COUPLING THIS BUYS: the Oracle lane now imports a BRIEF-2 render module,
# so any import brief_render.py gains tomorrow lands in the Oracle's closure.
# F-BR-13 therefore re-measures that closure on every run and goes red on an
# estate component, and re-asserts that no local copy is ever assigned.
from brief_render import TARGET_BUCKETS, target_bucket  # noqa: E402

ZONE = "America/Argentina/Buenos_Aires"
OUT_DIR = ROOT / "briefs" / "oracle"
TAPE_DIR = ROOT / "research_outputs" / "oracle" / "tape"
# THE RANGE LAYER'S SIBLING TAPE (A-OR1-1 clause v, operator 2026-09-22, verbatim:
# "Range records go to a sibling tape, research_outputs/oracle/tape_ranges/; the TC4
# event tape's schema is untouched (A-BR2-1b doctrine)"). A module-level PATH like the
# others, so that any sandbox that calls run() can redirect it (oracle_topup --enumerate,
# the sandbox suite and F-BR-14's behaviour leg do). The name is FENCED: F-BR-14
# goes red on any use of it outside write_range_tape() — run() may only CALL that
# writer, once, and hand what it returns to log() and its return dict — and on any
# decision module that spells it or the directory's name. So are the lane's other paths
# (F-BR-14 leg (h)): each is named only by the functions that name it today.
TAPE_RANGES_DIR = ROOT / "research_outputs" / "oracle" / "tape_ranges"
CAL_DIR = ROOT / "research_outputs" / "oracle" / "calibration"
PAYLOAD_DIR = ROOT / "research_outputs" / "oracle" / "payloads"
GRID_PARQUET = ROOT / "research_outputs" / "census2b" / "oracle" / "oracle_grid.parquet"
# THE ONE THING THAT CROSSES THE MOVERS WALL (OR-1 STEP E): a directory this file
# READS one json from, by path. A module-level PATH like the four above so a fixture can
# point it into a TemporaryDirectory (F-MV-8); unlike the four above it is NEVER created
# and NEVER written from here: scripts/oracle_movers.py, a separate fetch-only process
# this file does not import, is the directory's only writer. The name is FENCED: F-MV-9
# reads this file's AST and goes red on any use of it outside load_movers().
MOVERS_DIR = ROOT / "research_outputs" / "oracle" / "movers"

# ═══════════════════════════════════════════════════════ THE CLOSED REGISTER
# Same law as tierc2/tierc3/posture_engine: nothing invented without saying so.
# 'ruled': False rows are [VETO] and are logged by D-7 every run.

REGISTER: dict[str, dict] = {
    # THE ROSTER IS THE ORACLE'S OWN CONSTANT: A LITERAL, IN THE OPERATOR'S ORDER
    # (OR-1 STEP C, 2026-09-21). Until that day this row read tuple(<the study
    # basket>), i.e. engine/cells.py's dict, "frozen at ratification (charter §4)".
    # Two different things were sharing one definition: the basket a study is
    # pre-registered on may never move, while the list the operator LOOKS at each
    # morning moves whenever he says so. He said so (ruling 1, verbatim in 'source'),
    # so the two are now separate definitions. engine/cells.py is untouched and this
    # file no longer imports the basket at all: F-BR-16 goes red if that binding, or
    # any second symbol list, comes back.
    #   NOTHING ON THIS PATH NEEDED THE BASKET. make_cell() raises KeyError for a
    # symbol outside the frozen ten — correct for the study, and never reached from
    # here: posture_engine, tierc2/tierc3_rules, analytics and load_lens take the
    # symbol as a plain string. MEASURED at STEP C, not assumed: build_view over this
    # roster with a recording spy on the basket and on make_cell logged zero touches.
    #   ONE DEFINITION (CONVENTIONS §6.4). Every live consumer IMPORTS this row:
    # build_view and fired_events below; F-BR-1, F-BR-5, F-BR-8 and F-BR-16 in
    # oracle_fixtures.py. The top-up's scope is never typed either: it is ENUMERATED
    # from a run over this row (oracle_topup.py --enumerate) and pinned to this
    # file's sha. So editing this tuple HALTs the top-up until the re-pin (F-TU-1),
    # and a symbol new to the cache must be BACKFILLED FIRST: load_lens HALTs on a
    # missing series and the top-up refuses to create one (status ABSENT).
    #   THE ORDER IS THE OPERATOR'S, not alphabetical: the order he typed his 22 in,
    # the dropped names removed. The Board re-sorts by heat, so the order shows only
    # in the run log, the enumeration, the fired-events walk and heat ties.
    "ROSTER": {
        "value": (
            "BTCUSDT", "ETHUSDT", "ENAUSDT", "SOLUSDT", "USELESSUSDT", "NEARUSDT",
            "1000PEPEUSDT", "LITUSDT", "FARTCOINUSDT", "HYPEUSDT", "XPLUSDT", "ZECUSDT",
            "UNIUSDT", "LTCUSDT", "BNBUSDT", "XMRUSDT", "DOGEUSDT", "1000BONKUSDT",
        ),
        "ruled": True,
        "source": "RATIFIED by operator ruling 1 of 2026-09-21, verbatim: '1-watchlist: drop "
                  "symbols without data from a binance contract' (queue OR-1 STEP C, "
                  "exchange/queue/2026-09-21_OR1_daily_oracle_ondemand_ARGUS.md). The "
                  "operator's 22 — BTC NPC ETH ENA SOL PUMPFUN USELESS NEAR 1000PEPE LIT "
                  "FARTCOIN HYPE XPL ZEC MNT UNI LTC ZCAT BNB XMR DOGE 1000BONK, as <X>USDT — "
                  "were probed ONCE against Binance USDT-M exchangeInfo (contractType "
                  "PERPETUAL, status TRADING) at 2026-09-21T15:45:56Z; the record is "
                  "research_outputs/oracle/roster_probe_2026-09-21.json. KEPT = this tuple, "
                  "in the operator's order. DROPPED BY RULING (absent from exchangeInfo: no "
                  "Binance USDT-M contract by that name): NPCUSDT, PUMPFUNUSDT, MNTUSDT, "
                  "ZCATUSDT. LEFT THE ROSTER (on it before OR-1, not among the operator's 22; "
                  "kline caches retained, never deleted): JTOUSDT, TAOUSDT. SUPERSEDES, as "
                  "history: BR-1 C-5 'Roster = current 10-asset capture set' and A1-2 'Roster "
                  "as-is', under which this row was the engine/cells.py study basket. That "
                  "basket stays frozen (charter §4) and is not this list.",
    },
    "LENS": {
        "value": PE.REGISTER["LENS"]["value"],
        "ruled": True,
        "source": "posture_engine.REGISTER['LENS'] — the rule card's 4h. The Board, the "
                  "Cards and the Watch all read ONE lens so a row means one thing.",
    },
    "MANTLE_BARS": {
        "value": 96,
        "ruled": True,
        "source": "BR-1 C-7 verbatim: 'static last-96-bars mantle thumbnail per asset'.",
    },
    "GRID_LENSES": {
        "value": ("5m", "15m", "30m", "1h", "4h"),
        "ruled": True,
        "source": "census2b_oracle.LENSES — the ORACLE GRID's own five lenses. C-8 "
                  "classifies fired events 'per lens', so the footer walks exactly these.",
    },
    "FIRED_WINDOW_HOURS": {
        "value": 24,
        "ruled": False,
        "deferred_to": "BR-2",
        "source": "DEFERRED-TO-BR2 by BR-1 Amendment A2-6 (operator, 2026-08-16): BR-2 proposes a measured value from a week of D-7 distributions; nothing self-adopts. ORIGINALLY: PROPOSED by the BR-1 build 2026-08-16 — UNRULED [VETO]. C-8 says "
                  "'yesterday's fired events' and does not define yesterday. 24h back "
                  "from the as-of bar. D-7 logs the resulting event count per run.",
    },
    "GRID_TOLL_KEY": {
        "value": ("4h", "12_26 IN-WINDOW"),
        "ruled": False,
        "deferred_to": "BR-2",
        "source": "DEFERRED-TO-BR2 by BR-1 Amendment A2-6 (operator, 2026-08-16): BR-2 proposes a measured value from a week of D-7 distributions; nothing self-adopts. ORIGINALLY: PROPOSED by the BR-1 build 2026-08-16 — UNRULED [VETO]. C-2 says the "
                  "toll comes from the ORACLE GRID 'by name and lens' but no mapping from "
                  "a Trap Card to a (lens, class) key is written anywhere. A card is a "
                  "12/26 in-window entry on the 4h lens, so this is that cell. "
                  "toll_atr = 0.035196 ATR at time of writing.",
    },
    "NET_RR_FORM": {
        "value": "(reward - toll_price) / (risk + toll_price)",
        "ruled": True,
        "source": "RATIFIED by BR-1 Amendment A2-4 (operator, 2026-08-16), closing "
                  "finding V-5: '(reward - toll) / (risk + toll), toll paid win or lose; "
                  "both inputs print beside every ratio.' Proposed by the BR-1 build "
                  "because no net-R:R formula existed anywhere in the estate while C-2 "
                  "required one and forbade a cost-free number. toll_price = toll_atr x "
                  "ATR(lens); both inputs print beside every ratio so the operator can "
                  "re-derive it by eye.",
    },
    "HEAT": {
        "value": "score / (1 + atr_distance)",
        "ruled": False,
        "deferred_to": "BR-2",
        "source": "DEFERRED-TO-BR2 by BR-1 Amendment A2-6 (operator, 2026-08-16): BR-2 proposes a measured value from a week of D-7 distributions; nothing self-adopts. ORIGINALLY: PROPOSED by the BR-1 build 2026-08-16 — UNRULED [VETO]. The only text "
                  "is 'sorted by heat (proximity x cluster score)'. Both inputs print in "
                  "the row so the sort is auditable. See posture_engine.REGISTER['HEAT_KEY'].",
    },
    "VWAP_WINDOWS_D": {
        "value": (7, 30),
        "ruled": True,
        "source": "analytics/INTERFACE — rolling VWAP windows; the 7d/30d pair is the "
                  "brief-2 short set. Rolling windows take NO maturity floor "
                  "(analytics.vwap docstring); the 90/365d windows are omitted here "
                  "because the Board reads today, not the year.",
    },
    "PIVOT_LOOKBACK_BARS": {
        "value": V3.REGISTER["PIVOT_LOOKBACK_4H"]["value"],
        "ruled": True,
        "source": "tierc3_rules.REGISTER['PIVOT_LOOKBACK_4H'] = 200 bars on the 4h lens.",
    },
    "TARGET_BUCKET_ATR": {
        "value": "lens",
        "ruled": False,
        "source": "PROPOSED by the OR-1 STEP B build 2026-09-21 — UNRULED [VETO]. The contract "
                  "says 'record target-bucket occupancy' and names no ATR. A Trap Card "
                  "prices its toll in the LENS ATR (trap_card: toll_price = toll_atr x "
                  "st.atr), so the D-7 logger buckets the card's target distance in that "
                  "same ATR. The bucket EDGES, though, are brief_render.TARGET_BUCKETS, and "
                  "the BRIEF-2 lane that wrote them measures target_distance_atr in the "
                  "DAILY ATR (brief2.py). Two honest bases, one ruling owed: so the logger "
                  "records the distance and the bucket on BOTH ('lens' and 'daily') every "
                  "run and only the headline `target_bucket` follows this row. Display-only: "
                  "nothing on the page, the tape or any card reads a bucket.",
    },
    # THE RANGE LAYER'S THREE CONSTANTS (OR-1 STEP D, 2026-09-21). All three are read
    # by range_layer() and the render functions and by NOTHING that gates: see "THE
    # RANGE LAYER" above build_view, and F-BR-14. Two are the contract's own [VETO]
    # defaults and print in the rendered [VETO] appendix until the operator rules.
    "RANGE_LENS": {
        "value": "4h",
        "ruled": False,
        "source": "PROPOSED by the OR-1 contract's own default — UNRULED [VETO]. STEP D, "
                  "verbatim: 'oracle_daily runs it per roster symbol on the 4h lens [VETO "
                  "default — the system's lens]'. 4h is the lens the v2 pins were calibrated "
                  "on (BTC 4h, KEY-C) and the lens build_view has ALREADY loaded, so the range "
                  "layer adds no cache read and the top-up scope gains no pair. THE BINDING IS "
                  "MEASURED, NOT NAMED: range_layer() checks the bar spacing of the frame it is "
                  "handed against this row and prints RANGE UNAVAILABLE rather than run a 4h "
                  "calibration over another lens's bars. A different range lens needs its own "
                  "cache read, a scope re-enumeration and a ruling. Display-only: no gate, "
                  "filter, heat, station, card or sizing reads a range (F-BR-14).",
    },
    "RANGE_WINDOW_BARS": {
        "value": RNG.V2_WINDOW_BARS,
        "ruled": True,
        "source": "rangefinder_core.V2_WINDOW_BARS = 1700 (scripts/rangefinder_core.py, the "
                  "Oracle's machine since A-OR1-1 iv), IMPORTED, never copied "
                  "(CONVENTIONS §6.4): the RangeFinder twin's V2 window, the last 1,700 4h "
                  "bars, which is the tape the v2 calibration of record (KEY-C) was measured "
                  "on. OR-1 STEP D fixes it with 'same v2 pins, same event log': the event log "
                  "is a function of the window (the machine's ATR seeds at the window's first "
                  "bar), so a different window is a different machine. A symbol whose cache is "
                  "shorter runs on what it has, and the Tide Tables print its true bar count.",
    },
    "RANGE_WATCH_ATR": {
        "value": 0.5,
        "ruled": False,
        "source": "PROPOSED by the OR-1 contract's own default — UNRULED [VETO]. STEP D, "
                  "verbatim: 'EDGE WATCH sub-list = distance ≤ 0.5 ATR [VETO] OR pending breach "
                  "open, sorted by distance'. The ATR is the range machine's own — "
                  "engine.indicators ATR(14) on the RANGE_LENS tape, the ATR its pins are "
                  "multiples of — NOT the daily ATR the Board's level distances use. '≤' is "
                  "inclusive, as written. The threshold picks rows for a display list and does "
                  "nothing else: no gate, filter, heat, station, card or sizing reads it, or "
                  "the list (F-BR-14).",
    },
    # THE MARKET PAGE'S ONE CONSTANT (OR-1 STEP E, 2026-09-21), AND WHY ITS VALUE IS A
    # POINTER. The fifty of ruling 7 is typed ONCE in the estate: oracle_movers.TOP_N, in
    # the organ that cuts the tables. CONVENTIONS §6.4 says a live consumer IMPORTS the
    # one definition, and this consumer may not: the Oracle is cache-only and the organ
    # fetches, so importing it would put the fetching organ inside a firewalled run (F-MV-9
    # goes red on exactly that). The number therefore crosses the wall the only way
    # anything does, inside the json, as `top_n`, and market_page() prints that many
    # rows. A second fifty typed here would be a second definition, free to drift from
    # the first; F-MV-3 holds the json's number to the ruling, F-MV-8 holds the page to
    # the json's number.
    "MARKET_PAGE_TOP_N": {
        "value": "read from the movers json (its own top_n field), never typed here",
        "ruled": True,
        "source": "RATIFIED by operator ruling 7 of 2026-09-21, verbatim: '7-add a list at the "
                  "end of the oracle with the top 50 coins by %change overnight and weekly' "
                  "(queue OR-1 STEP E: 'Render two tables, top 50 by signed % change each'). "
                  "SIGNED, largest first: the head of each table is the largest gain, not the "
                  "largest absolute move. The one definition of the number is "
                  "oracle_movers.REGISTER['TOP_N'], which the organ copies into every json it "
                  "writes; load_movers() refuses a document whose top_n is not a positive "
                  "integer, and market_page() cuts each table at it. Display-only: no gate, "
                  "filter, heat, station, card or sizing reads a mover (F-MV-9).",
    },
    # THE TYPESETTING'S CONSTANTS (OR-1 STEP F, 2026-09-21): THE DAILY ORACLE. STEP F is
    # "semantics untouched, template only", so every row below is read by render_html,
    # its typesetting helpers (page_css, mantle_caption, edition_verb, print_time_ba,
    # edition_name, print_line, edition_count, front_page, staleness_banner,
    # svg_spaghetti) and run()'s one masthead number and one print time, and
    # by NOTHING that computes a level, a word, a card or a row of the tape. Six rows
    # are the contract's own words and are 'ruled': True. Two are this build's reading
    # of words the contract leaves open: 'ruled': False, so they print in the rendered
    # [VETO] appendix and in D-7's veto_rows_awaiting_ruling until the operator rules.
    #   ONE PHRASE MAY NOT BE SPELT IN AN UNRULED ROW'S 'source': the band's two opening
    # words (REGISTER['LATE_EDITION']). An unruled source PRINTS in the appendix, and
    # the on-demand wrapper reads "banner UP" off that phrase anywhere in the page's
    # text. F-BR-15 holds the page to it: the phrase only inside the band.
    "TYPE_PALETTE": {
        "value": {"paper": "#F4ECD8", "ink": "#1A1A1A", "red": "#B3261E"},
        "ruled": True,
        "source": "OR-1 STEP F, verbatim: 'paper #F4ECD8, ink #1A1A1A, one red #B3261E for "
                  "alarms' and 'Light paper only [D-7a]'. ONE definition: page_css() "
                  "interpolates these three and derives the muted ink, the hairline and the "
                  "tint from the ink by alpha, so the style block types no fourth colour. "
                  "RED IS THE ALARM INK AND NOTHING ELSE: the late-edition band, WIRE DOWN, a "
                  "STALE TRIGGER chip and the range layer's PENDING / UNAVAILABLE marks — "
                  "exactly what the pre-STEP-F page set in its alarm treatment (terra AND "
                  "bold). Direction and posture, which that page told apart by hue alone, are "
                  "told apart in ink: long an open box, short a filled one; TRIGGERED a double "
                  "rule, ARMED a plain one, STALKING muted, DEAD dotted. F-BR-15 reads the "
                  "style block and goes red on the red under any other selector, on a "
                  "dark-theme remnant and on a theme switch. NOT PAGE INKS, by design: the "
                  "mantle strips' teal/terra displacement scale (MANTLE_JS, 'same law, same "
                  "colours' as VIZ-4, untouched) and the Spaghetti's per-symbol hues are DATA "
                  "encodings; the Spaghetti's hue wheel skips the red band so that an alarm "
                  "stays the only red on the paper.",
    },
    "TYPE_SERIF_STACK": {
        "value": '"Iowan Old Style", Palatino, Georgia, serif',
        "ruled": True,
        "source": "OR-1 STEP F, verbatim: 'serif stack \"Iowan Old Style\", Palatino, Georgia, "
                  "serif'. The page's face. ONE EXCEPTION, stated: the Telegrams block and "
                  "<code> are set in a typewriter face, because an R1 line is pasted into a "
                  "machine and has to read character for character.",
    },
    "MASTHEAD": {
        "value": {"title": "THE DAILY ORACLE", "volume": "Vol. I", "city": "Buenos Aires",
                  "price": "Price: one toll"},
        "ruled": True,
        "source": "OR-1 STEP F as amended by A-OR1-1 vii: 'MASTHEAD \"THE DAILY ORACLE\" · "
                  "ears: left \"Vol. I · No. <edition count>\", right \"Buenos Aires · <date> "
                  "· <Morning|Evening|Refresh> Edition · Price: one toll\"'. AMENDMENT "
                  "A-OR1-1 clause vii (operator, 2026-09-22), verbatim: \"Edition word "
                  "follows verb and hour: full before 12:00 BA = Morning, after = Evening; "
                  "refresh = Refresh. A paper printed at night does not call itself the "
                  "morning's.\" <date> is run()'s date_str; the edition's word is "
                  "edition_name(slot, printed_at): the refresh verb (a slot naming "
                  "'refresh') is Refresh at any hour; the full verb (every other slot) is "
                  "Morning while the print time's Buenos Aires wall-clock hour is before 12 "
                  "and Evening from 12:00:00 on. run() takes the print time ONCE and the "
                  "Colophon prints it: 'Printed <YYYY-MM-DD HH:MM> Buenos Aires (<word> "
                  "Edition: <verb>, slot <slot> · A-OR1-1 vii)'. The count is "
                  "REGISTER['EDITION_COUNT'].",
    },
    "SECTIONS": {
        "value": ("Front Page", "The Docket", "The Watch", "Tide Tables", "Telegrams",
                  "The Market Page", "Yesterday's Returns", "Colophon"),
        "ruled": True,
        "source": "OR-1 STEP F, the operator's eight, in his order: 'FRONT PAGE (the Board; "
                  "headline = the day's answer to \"where is business possible today\") · THE "
                  "DOCKET (Trap Cards) · THE WATCH (windows + mantle strips, EACH with a "
                  "caption) · TIDE TABLES (STEP D + Edge Watch) · TELEGRAMS (R1 blocks) · THE "
                  "MARKET PAGE (STEP E) · YESTERDAY'S RETURNS (ORACLE GRID footer) · COLOPHON "
                  "(DISPLAY-ONLY line, payload shas, certified/not-certified lists, as-of)'. "
                  "Every <h2> on the page is one of these and is BARE, styled through the "
                  "element: oracle_fixtures._sec, the movers fixtures and the wrapper's daily "
                  "self-check all split the page on the literal '<h2>' and find a section by "
                  "how its heading STARTS. TWO ORGANS HAVE NO SECTION OF THEIR OWN IN THE "
                  "EIGHT and are kept as <h3> sub-blocks, not lost: the Spaghetti (C-4) inside "
                  "The Watch, and the [VETO] appendix inside the Colophon.",
    },
    "MANTLE_CAPTION": {
        "value": "rows = threads, rod 5000 top → hem 9 bottom · columns = last {bars} bars · "
                 "hue = thread above/below price in ATR · dark pinch = knot · hole = unwoven",
        "ruled": True,
        "source": "OR-1 STEP F, verbatim, printed under EACH mantle strip (F-BR-15). The strip's "
                  "bar count is NOT typed a second time: mantle_caption() fills {bars} from "
                  "REGISTER['MANTLE_BARS'], the row mantle_payload() cuts the strip by, so a "
                  "caption cannot disagree with the strip it sits under. It replaces the "
                  "pre-STEP-F strip legend, which said three of the same five things; the "
                  "payload name and sha256 stay directly under the canvas (F-BR-4 reads the "
                  "sha within 900 characters of the tag), the caption after them.",
    },
    "LATE_EDITION": {
        "value": "LATE EDITION — {n} of {r} rows on a stale wire (oldest {as_of})",
        "ruled": True,
        "source": "OR-2 R-1 (operator 2026-09-22, ratified 'leans'), verbatim: 'The LATE "
                  "EDITION band fires when ANY row is stale and names the count: \"LATE "
                  "EDITION — N of R rows on a stale wire (oldest <as-of>)\"'. WHEN a row is "
                  "stale is still A2-7's arithmetic — its own as-of bar older than "
                  "STALE_LENS_PERIODS lens periods, measured from the bar's open — now judged "
                  "for EVERY row at the print time run() takes as it starts (A2-7 said 'at "
                  "render time'; the render follows within seconds), and A2-7's detail sentence still "
                  "follows the opening. <as-of> is the OLDEST row's bar, in the dateline's own "
                  "format. SUPERSEDES OR-1 STEP F's 'LATE EDITION — wire stale since <as-of>', "
                  "which judged the hottest asset's bar alone (finding OR1-a).",
    },
    "EDITION_COUNT": {
        "value": "distinct dates among tape/oracle_tape_<date>.parquet, this edition's date included",
        "ruled": False,
        "source": "PROPOSED by the OR-1 STEP F build 2026-09-21 — UNRULED [VETO]. The contract "
                  "prints 'Vol. I · No. <edition count>' and does not say what is counted. "
                  "Counted here: the DATES the Oracle has gone to press on, read off the D-4 "
                  "tape directory (one parquet per date), with this edition's own date added "
                  "because the page is rendered before the day's tape is written. NOT the "
                  "renders in briefs/oracle: on 2026-09-21 the operator moved that day's render "
                  "to his Desktop, and a count of renders would have gone backwards. A second "
                  "run on a date already printed — the refresh, an on-demand reprint — keeps "
                  "the day's number. Display-only: one number in the masthead.",
    },
    "FRONT_PAGE_HEADLINE": {
        "value": "'Business possible' needs a FRESH trigger; then TRIGGERED-but-stale, then "
                 "ARMED, in the Board's own order; neither word on the Board => 'No business "
                 "possible today'",
        "ruled": False,
        "source": "PROPOSED by the OR-1 STEP F build 2026-09-21 — UNRULED [VETO]. The contract: "
                  "'headline = the day's answer to \"where is business possible today\"', the "
                  "canon's one morning question (posture_engine.CANON_QUOTE_ENUMERATION), and "
                  "no rule for answering it. front_page() answers from the Board's POSTURE "
                  "COLUMN alone: the symbols whose word is the canon's station 3 (an open "
                  "window holds its entry alert), then station 2 (a window is open), in the "
                  "Board's own order; if neither word is on the Board the headline says so. A "
                  "STALE trigger is set apart, by the Board's own test (the row's freshest "
                  "in-window trigger is older than posture_engine's TRIGGER_FRESH_BARS, itself "
                  "[VETO]): that row of the register, verbatim, calls the ageless word "
                  "\"MISLEADING on a Board whose word the operator reads as 'the entry alert is "
                  "live now'\", and a headline is read before any row. So only a fresh trigger earns the "
                  "words 'Business possible' (F-BR-15). It restates words and marks already "
                  "printed in the rows beneath it: it reads no level, no ratio, no range and no "
                  "mover, adds no judgement, and is a pure function of the view (F-BR-6 renders "
                  "it twice and compares the bytes).",
    },
}

CERTIFIED = (
    "oscillators + ATR (72/72)", "resample_ohlcv (40/40)",
    "rolling VWAP both substrates (14/14, 28/28)",
    "anchored VWAP incl. sigma (42/42)", "band geometry (54 triples)",
)
NOT_CERTIFIED = (
    "volume_profile / LVN / va_nesting — FIXTURE-VERIFIED, never chart-certified BY DESIGN",
    "RVOL — uncertified",
    "posture canon v1 — the four-word MAP is PROPOSED, not ruled (see the [VETO] table)",
    "net R:R form — PROPOSED, no estate precedent exists",
)


# ═══════════════════════════════════════════════════════════════ LOADING

def load_lens(sym: str, tf: str, tail: int | None = None) -> pd.DataFrame:
    """Whole-file parquet read, the tierc2_baseline idiom. Cache only, no network."""
    p = cache_dir() / "klines" / f"{sym}_{tf}.parquet"
    if not p.exists():
        raise FileNotFoundError(f"HALT: no klines for {sym} {tf} at {p}")
    df = pd.read_parquet(p).sort_values("open_time").reset_index(drop=True)
    if tail is not None and len(df) > tail:
        df = df.iloc[-tail:].reset_index(drop=True)
    return df


def daily_atr(h1: pd.DataFrame) -> float:
    """The house daily-ATR convention: resample 1h -> 1d, then analytics ATR(14).

    Every ATR-normalised LEVEL distance in the brief uses this daily ATR, not
    the lens ATR (the two are different quantities and the estate keeps them
    apart deliberately).
    """
    r = ST.resample_ohlcv(h1["open_time"].to_numpy("int64"),
                          h1["open"].to_numpy("float64"), h1["high"].to_numpy("float64"),
                          h1["low"].to_numpy("float64"), h1["close"].to_numpy("float64"),
                          h1["volume"].to_numpy("float64"), 86_400_000)
    return float(VOL.atr(r["high"], r["low"], r["close"], 14)[-1])


# ═══════════════════════════════════════════════════════════════ LEVELS

def window_bars(open_time_ms, window_days) -> int:
    """How many bars sit inside a rolling VWAP window at the decision bar.

    analytics.vwap.rolling_vwap returns no sample depth, and analytics.vwap.
    maturity() needs one. The count uses the SAME membership rule rolling_vwap
    applies — "bar_open_time > current_bar_open_time - W, current included" —
    written the way brief2's rvwap block already writes it
    (`count_nonzero(t > t[-1] - need)`), so the number says how deep the sample
    behind the printed line really is. (rolling_vwap also floors its slice at
    the MIN_BARS = 10 most recent bars; 10 is below both maturity floors, so a
    window that thin classifies the same either way.)
    """
    t = np.asarray(open_time_ms, dtype="int64")
    if t.size == 0:
        return 0
    return int(np.count_nonzero(t > t[-1] - int(window_days) * VW.DAY_MS))


def level_registry(sym: str, h4: pd.DataFrame, h1: pd.DataFrame, atr_d: float,
                   maturity_out: list | None = None):
    """A level pool for the Board's clusters. analytics/ is the only arithmetic.

    Two families only, and both are causal at the decision bar:
      structure     — confirmed (5,5) 4h swing pivots, plus prior-day extremes
      vwap_rolling  — 7d / 30d rolling VWAP on the 1h substrate, hlc3 source

    analytics/levels has no time axis and cannot police causality, so the
    slicing is done HERE: confirmed_pivots carries CONFIRMATION_LAG = 5 and
    prior_period_extremes reads only completed days.

    `maturity_out` (C-0, OR-1 STEP B) is a MEASURING side-channel and nothing
    else. When a list is passed, one record per rolling window is appended:
    the bars inside the window, analytics.vwap.maturity()'s verdict on them,
    and how many line/band candidates this function offered to the registry.
    It WITHHOLDS NOTHING — every finite line and band is still added exactly
    as before (rolling windows take no floor by ruling, REGISTER
    ['VWAP_WINDOWS_D']). Withholding would be a semantic change to the Board;
    counting what the 16/60 floors WOULD withhold is display machinery, which
    is what A1-4 asked D-7 to log and what it never did until now.
    """
    reg = L.LevelRegistry()
    look = REGISTER["PIVOT_LOOKBACK_BARS"]["value"]
    hi = h4["high"].to_numpy("float64")
    lo = h4["low"].to_numpy("float64")
    n = len(hi)
    as_of = n - 1
    for kind, vals in (("high", hi), ("low", lo)):
        idx, lvl, _conf = ST.confirmed_pivots(vals, as_of, left=PE.REGISTER["PIVOT_L"]["value"],
                                              right=PE.REGISTER["PIVOT_R"]["value"], kind=kind)
        for i, v in zip(np.asarray(idx), np.asarray(lvl)):
            if int(i) >= n - look:
                reg.add("structure", f"4h pivot {kind} @{int(i)}", float(v),
                        "confirmed_pivots(4h)", timeframe="4h")

    ext = ST.prior_period_extremes(h1["open_time"].to_numpy("int64"),
                                   h1["high"].to_numpy("float64"),
                                   h1["low"].to_numpy("float64"), period="D")
    # Returns a (prior_high, prior_low) pair of as-of-each-bar arrays; the
    # decision bar is the last element of each. Causal by construction.
    pairs = ext.items() if isinstance(ext, dict) else zip(("high", "low"), ext)
    for label, arr in pairs:
        a = np.asarray(arr).ravel()
        if a.size == 0:
            continue
        v = float(a[-1])
        if np.isfinite(v):
            reg.add("structure", f"prior-day {str(label).replace('prior_', '')}", v,
                    "prior_period_extremes(1h->D)", timeframe="1d")

    src = VW.hlc3(h1["high"].to_numpy("float64"), h1["low"].to_numpy("float64"),
                  h1["close"].to_numpy("float64"))
    for wd in REGISTER["VWAP_WINDOWS_D"]["value"]:
        rv = VW.rolling_vwap(h1["open_time"].to_numpy("int64"), src,
                             h1["volume"].to_numpy("float64"), wd)
        n_line = n_band = 0                   # candidates OFFERED — counted, never gated
        v = float(np.asarray(rv["vwap"])[-1])
        if np.isfinite(v):
            reg.add("vwap_rolling", f"rVWAP {wd}d", v, "rolling_vwap(1h, hlc3)",
                    timeframe="1h")
            n_line += 1
        for k in (1, 2):
            for side in ("up", "dn"):
                band = rv.get(f"band_{side}_{k}")
                if band is None:
                    continue
                b = float(np.asarray(band)[-1])
                if np.isfinite(b):
                    reg.add("vwap_rolling", f"rVWAP {wd}d {side}{k}σ", b,
                            "vw_sigma_bands(1h)", timeframe="1h")
                    n_band += 1
        if maturity_out is not None:
            mat = VW.maturity(window_bars(h1["open_time"].to_numpy("int64"), wd))
            maturity_out.append({"window_d": int(wd), "bars": mat["bars"],
                                 "line_ok": bool(mat["line_ok"]),
                                 "band_ok": bool(mat["band_ok"]),
                                 "line_candidates": n_line,
                                 "band_candidates": n_band})

    members = L.collapse_same_family(reg.as_list(), atr_d)
    clusters = L.cluster(members, atr_d)
    return reg, members, clusters


# ═══════════════════════════════════════════════════════════════ THE TOLL

def grid_toll() -> pd.DataFrame:
    """The ORACLE GRID per-lens NET toll table, cut='ALL'. C-2's table."""
    if not GRID_PARQUET.exists():
        raise FileNotFoundError(f"HALT: ORACLE GRID absent at {GRID_PARQUET}; "
                                "C-2 forbids a cost-free number, so there is no "
                                "degraded mode. Rebuild with census2b_oracle.py.")
    g = pd.read_parquet(GRID_PARQUET)
    return g[g["cut"] == "ALL"].reset_index(drop=True)


def toll_for(g: pd.DataFrame, tf: str, cls: str) -> float | None:
    row = g[(g["tf"] == tf) & (g["cls"] == cls)]
    if row.empty:
        return None
    v = float(row["toll_atr"].iloc[0])
    return v if np.isfinite(v) else None


def net_rr(reward: float, risk: float, toll_price: float) -> float | None:
    """REGISTER['NET_RR_FORM'], [VETO]. No cost-free ratio is ever returned."""
    den = risk + toll_price
    if not np.isfinite(den) or den <= 0:
        return None
    v = (reward - toll_price) / den
    return float(v) if np.isfinite(v) else None


# ═══════════════════════════════════════════════════════ THE MANTLE PAYLOAD
# C-7: rendered FROM the v4 payload pattern, never recomputed ad hoc.
# The v4 shape is reproduced exactly: {'meta', 'data'}; meta.sha256 is the sha
# of the DATA BLOCK (json.dumps(data, sort_keys=True, separators=(',',':'))),
# which is the sha the shipped VIZ-4 footers stamp. Threads, thread_sr,
# thread_k, disp orientation (EMA - price)/ATR, and the null-means-absent rule
# are all the v4 contract's, not this build's.

THREADS = list(P.ALL_EMAS)                       # 18 lengths, 9 .. 5000
THREAD_SR = [fam for L_ in THREADS for fam, m in P.RIBBONS.items() if L_ in m]
STATE_K = {"FAST": 20, "M": 20, "MH": 40, "H": 111, "VH": 327, "UH": 577}
THREAD_K = [STATE_K[s] for s in THREAD_SR]


def _r3(x):
    return None if x is None or not np.isfinite(x) else round(float(x), 3)


def mantle_payload(sym: str, h4: pd.DataFrame, bars: int) -> dict:
    """A NARROW mantle payload: the last `bars` bars at stride 1.

    The shipped v4 payloads are decimated (stride 8 at 1h, 92 at 5m), so a
    'last-96-bars' strip is NOT a slice of them — 96 bars is 12 columns at 1h
    and about one column at 5m. Rather than silently reinterpret 'bars' as
    'steps', this emits a fresh payload whose source slice is short enough
    that decimate() would give stride 1 and every bar survives. The shape is
    identical; only the window is narrow.
    """
    close = h4["close"].to_numpy("float64")
    high = h4["high"].to_numpy("float64")
    low = h4["low"].to_numpy("float64")
    ot = h4["open_time"].to_numpy("int64")
    atr_v = P.atr(high, low, close, P.ATR_LEN)

    df = pd.DataFrame({"open_time": ot, "close": close, "high": high,
                       "low": low, "atr": atr_v})
    for L_ in THREADS:
        v = P.ema(close, L_)
        v[: min(P.warm_bars(L_), len(v))] = np.nan
        df[f"e{L_}"] = v

    sl = slice(max(0, len(df) - bars), len(df))
    ts = [int(t) for t in ot[sl]]

    disp = []
    for L_ in THREADS:
        e = df[f"e{L_}"].to_numpy("float64")[sl]
        a = atr_v[sl]
        c = close[sl]
        with np.errstate(invalid="ignore", divide="ignore"):
            d = np.where(np.isfinite(e) & np.isfinite(a) & (a > 0), (e - c) / a, np.nan)
        disp.append([_r3(x) for x in d])

    knot, orient = {}, {}
    for fam in P.FAMILIES:
        fs = P.family_state(fam, df)
        k = fs["knot"][sl]
        o = fs["orient"][sl]
        knot[fam] = [None if int(x) == P.KN_NA else int(x) for x in k]
        orient[fam] = [None if int(x) == P.OR_NA else int(x) for x in o]

    data = {
        "asset": sym, "lens": REGISTER["LENS"]["value"],
        "threads": THREADS, "thread_sr": THREAD_SR, "thread_k": THREAD_K,
        "hem_lens": [12, 26], "rod_lens": [2618, 3618, 4236, 4618, 5000],
        "ts": ts, "disp": disp,
        "knot": knot, "orient": orient,
        "knot_codes": {"no": 0, "knot": 1, "absent": None},
        "orient_codes": {"bear-fanned": -1, "mixed": 0, "bull-fanned": 1, "absent": None},
    }
    blob = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    meta = {
        "payload": f"oracle_mantle_{sym}_{REGISTER['LENS']['value']}.json",
        "sha256": hashlib.sha256(blob).hexdigest(),
        "rows": sum(len(v) for v in disp) + len(ts),
        "bars": len(ts),
        "class": "DISPLAY-ONLY / operations",
        "downsample_rule": f"stride 1, anchored at the LAST bar: the last {len(ts)} "
                           f"source bars of the {REGISTER['LENS']['value']} lens; every "
                           f"bar survives (no decimation)",
        "note": "displacements are (EMA-price)/ATR; null = not woven, render ABSENT "
                "never zero; knot/orient null = NOT COMPUTED, which is not 'no knot'",
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }
    return {"meta": meta, "data": data}


# ═════════════════════════════════════════════════════════ THE RANGE LAYER
# OR-1 STEP D (RATIFIED operator 2026-09-21). The contract: "oracle_daily runs it per
# roster symbol on the 4h lens [VETO default — the system's lens] and emits per
# symbol: macro state · macro top/bottom · %position · ATR-distance to nearest macro
# boundary · PENDING-breach flag · last event + age."
#
# THE WALL, which is the point of the step (OR-1 §2): "no gate, filter, or sizing
# reads a range or a mover." The range object is WRITTEN once, by build_view, into
# a["range"], AFTER that asset's levels, clusters, heat, station and card exist. It
# is READ by the render functions and by write_range_tape (the SIBLING tape, A-OR1-1
# v), and by nothing else: never level_registry, never trap_card, never net_rr, never
# fired_events, never r1_block, never write_calibration, never write_tape (the D-4
# tape carries no range column since A-OR1-1), never the Board's sort. F-BR-14 holds
# the wall four ways: posture_engine.py's sha256; the import closures of the decision
# modules; an AST scan of THIS file against an allow-list of reader functions; and a
# behavioural run in which the whole decision side of build_view must come out
# identical with the layer stubbed EMPTY, stubbed HOT (every symbol pinned on a
# boundary with a breach pending) and REAL. Since A-OR1-1 it also holds the machine
# (rangefinder_core, never engine.rangefinder, in this file's closure), both tapes'
# schemas, and a scan that no decision module names the sibling tape.
#
# NO NEW READ. The machine runs on the 4h frame build_view has ALREADY loaded, so the
# top-up scope gains no pair and no read. (The pin still moves, because this file's
# sha moved: oracle_topup.py --enumerate re-pins it and prints the same pairs.)
#
# A DISPLAY ORGAN MAY NOT TAKE THE PAGE DOWN EITHER. "Renders, never rules" cuts both
# ways: a fault inside the range machine on one symbol must not cost the operator
# his Board. range_layer() therefore CONTAINS its own failure and hands back
# range_empty(error=...): the Tide Tables print RANGE UNAVAILABLE with the reason in
# the alarm colour, the sibling tape records range_state = "UNAVAILABLE", and every other
# section renders as if the layer did not exist. Contained is not silent.
#
# UNCALIBRATED OFF BTC. The micro pins were calibrated on BTC 1D (KEY-A) and the v2
# pins on BTC 4h (KEY-C). On every other symbol they are borrowed numbers, and the
# page says so under the table on every edition.

RANGE_UNAVAILABLE = "UNAVAILABLE"
# What a reader prints for an asset whose view carries no range at all (a view built
# by older code, or by a fixture): an absence with a reason, never a blank.
RANGE_ABSENT = "this view carries no range for the asset"


def range_empty(state: str = RANGE_UNAVAILABLE, error: str | None = None) -> dict:
    """The range object of a symbol with NOTHING to show: rangefinder_core.snapshot's
    own key set (F-BR-14 pins the two equal) plus `error`. Used when the machine could
    not run (`error` says why), as the reader's default for a view that carries no
    range at all, and by F-BR-14 as the EMPTY stub."""
    return {"state": state, "has_range": False,
            "top": None, "bottom": None, "top0": None, "bottom0": None, "mid": None,
            "pos_pct": None, "atr": None, "dist_atr": None, "nearest_side": None,
            "pending": None, "n_pending_open": 0, "n_potential": 0,
            "last_event": None, "status_line": "",
            "as_of": None, "close": None, "n_bars": 0, "error": error}


def range_layer(h4: pd.DataFrame) -> dict:
    """One symbol's MACRO range as of the last bar of `h4`: the frame build_view has
    already loaded (and already cut to as_of_ms). No cache read, no network, no wall
    clock; `h4` is not mutated (tape_from_klines copies).

    The three calls are the RangeFinder twin's own, with its own v2 pins: the tape,
    the machine, the snapshot. Prices come from the full-precision Range fields,
    never from the 2-dp event log (see the hazard note in scripts/rangefinder_core.py).

    REGISTER['RANGE_LENS'] is enforced by MEASUREMENT: the median bar spacing of the
    tape must equal that lens's period, or the layer refuses. The pins are a 4h
    calibration; run over 1h bars they would draw confident boxes that mean nothing.

    NEVER RAISES. Any fault is returned as range_empty(error=...) and printed."""
    try:
        d = RNG.tape_from_klines(h4, n_bars=REGISTER["RANGE_WINDOW_BARS"]["value"])
        want = REGISTER["RANGE_LENS"]["value"]
        t0 = d["t0"].to_numpy("int64")
        if len(t0) >= 2:
            step = int(np.median(np.diff(t0)))
            if step != LENS_MS[want]:
                raise ValueError(
                    f"REGISTER['RANGE_LENS'] is {want} ({LENS_MS[want]} ms) but the frame "
                    f"build_view loaded steps {step} ms; the pins are a {want} calibration")
        v2 = RNG.run_v2(d, RNG.PINS_V2)
        return {**RNG.snapshot(d, v2), "error": None}
    except Exception as e:                     # contained, never silent: it prints
        return range_empty(error=f"{e.__class__.__name__}: {e}")


# ═══════════════════════════════════════════════════════════════ THE VIEW

def build_view(as_of_ms: int | None = None, log=print) -> dict:
    """Everything the render and the tape read. One pass, one substrate."""
    roster = list(REGISTER["ROSTER"]["value"])
    lens = REGISTER["LENS"]["value"]
    g = grid_toll()
    toll_tf, toll_cls = REGISTER["GRID_TOLL_KEY"]["value"]
    card_toll_atr = toll_for(g, toll_tf, toll_cls)
    if card_toll_atr is None:
        raise ValueError(f"HALT: no toll for {REGISTER['GRID_TOLL_KEY']['value']}")

    assets, payloads = [], {}
    for sym in roster:
        h4 = load_lens(sym, "4h")
        h1 = load_lens(sym, "1h", tail=24 * 400)
        if as_of_ms is not None:
            h4 = h4[h4["open_time"] <= as_of_ms].reset_index(drop=True)
            h1 = h1[h1["open_time"] <= as_of_ms].reset_index(drop=True)
        atr_d = daily_atr(h1)
        st = PE.stations_for(sym, h4)
        vwap_maturity: list[dict] = []        # C-0: measured here, logged by D-7
        reg, members, clusters = level_registry(sym, h4, h1, atr_d,
                                                maturity_out=vwap_maturity)
        price = st.close
        lis = L.lines_in_sand(clusters, price, atr_d)

        scored = [c for c in clusters if c["score"] > 0]
        nearest = min(scored, key=lambda c: abs(c["mean"] - price)) if scored else None
        nearest_d = abs(nearest["mean"] - price) / atr_d if nearest else float("nan")
        heat = (nearest["score"] / (1.0 + nearest_d)) if nearest else 0.0

        pay = mantle_payload(sym, h4, REGISTER["MANTLE_BARS"]["value"])
        payloads[pay["meta"]["payload"]] = pay

        assets.append({
            "symbol": sym, "station": st, "atr_d": atr_d, "price": price,
            "clusters": clusters, "n_levels": len(reg), "lis": lis,
            "vwap_maturity": vwap_maturity,
            "nearest": nearest, "nearest_d": nearest_d, "heat": heat,
            "payload_name": pay["meta"]["payload"], "payload_sha": pay["meta"]["sha256"],
            "card": trap_card(sym, h4, st, clusters, atr_d, card_toll_atr),
        })
        # OR-1 STEP D: THE ONE PLACE A RANGE IS WRITTEN. Deliberately the LAST thing
        # done for this asset, after its levels, heat, station and card exist, and
        # nothing below reads it back: the sort is on heat, fired_events takes the
        # roster. F-BR-14 goes red on any other mention of a range inside build_view.
        assets[-1]["range"] = range_layer(h4)
        log(f"  {sym:14} {st.board_word:10} heat={heat:6.3f} levels={len(reg):3d} "
            f"clusters={len(clusters):3d} atr_d={atr_d:.6g}")

    assets.sort(key=lambda a: -a["heat"])
    return {
        "as_of_ms": assets[0]["station"].as_of_ms if assets else 0,
        "lens": lens, "assets": assets, "payloads": payloads,
        "grid": g, "card_toll_atr": card_toll_atr,
        "fired": fired_events(roster, as_of_ms, g, log=log),
    }


def f_close_at(h4, i: int) -> float:
    """The close of bar i on the lens frame — the rule card's entry price."""
    return float(h4["close"].to_numpy("float64")[i])


def trap_card(sym, h4, st, clusters, atr_d, toll_atr) -> dict | None:
    """C-6. A pre-framed if-then, never a recommendation.

    entry        — the rule card enters at the in-window 12/26 bar close.
    invalidation — tierc3_rules.struct_stop_4h: the structural 4h anchor with
                   the 0.5 ATR buffer, RAILED to at least 1.0 ATR (the F-3
                   ruling). Not re-derived here; the module is called.
    target       — the nearest cluster beyond entry on the trade's side.
    net R:R      — REGISTER['NET_RR_FORM'], toll from the ORACLE GRID.
    """
    live = [w for w in st.open_windows if w.admitted]
    if not live:
        return None
    w = max(live, key=lambda w: w.arm_i)
    direction = w.direction
    atr_l = st.atr

    # THE ENTRY ANCHOR. The rule card is explicit — "TRIGGER: first in-window 4h
    # 12/26 cross -> enter at that bar close" — so a TRIGGERED window's entry is
    # the CLOSE OF THE TRIGGER BAR, not today's close. Anchoring it to today's
    # close silently re-prices a card that already fired: on NEARUSDT that was a
    # 10.1 ATR drift, and every derived field (risk, target, net R:R) inherited
    # it. An ARMED window has not fired yet, so its entry is genuinely unknown
    # and the card is PROVISIONAL: the last close stands in as the reference and
    # says so, rather than pretending to a price the market has not printed.
    if w.trigger_i is not None:
        entry = float(f_close_at(h4, w.trigger_i))
        entry_basis = (f"close of the 12/26 trigger bar, {w.trigger_age_bars} bar(s) ago"
                       + (" — STALE" if w.trigger_stale else ""))
        provisional = False
    else:
        entry = st.close
        entry_basis = "PROVISIONAL — the 12/26 has not fired; last close stands in"
        provisional = True

    # THE STOP IS NOT COMPUTED HERE. tierc3_rules.struct_stop_4h is the ratified
    # anchor: nearest confirmed 4h (5,5) pivot strictly beyond entry within the
    # lookback, offset 0.5 ATR, THEN railed to at least MIN_STOP_ATR. It returns
    # None for `no_struct_anchor`, and the rule card is explicit that the rail
    # does NOT invent a stop where structure names none — "A trade left with no
    # admissible anchor is NOT TAKEN. Printed both ways." So is this card.
    pv = V3.build_pivots_4h(h4["high"].to_numpy("float64"), h4["low"].to_numpy("float64"))
    stop = V3.struct_stop_4h(pv, st.as_of_i, entry, direction, atr_l,
                             lookback=REGISTER["PIVOT_LOOKBACK_BARS"]["value"],
                             min_stop_atr=PE.REGISTER["MIN_STOP_ATR"]["value"])
    if stop is None:
        return {
            "direction": "long" if direction == 1 else "short",
            "station": w.station, "arm_ms": w.arm_ms, "disp": w.disp,
            "not_taken": True, "provisional": provisional, "entry_basis": entry_basis,
            "trigger_age_bars": w.trigger_age_bars, "trigger_stale": w.trigger_stale,
            "entry": entry,
            "entry_rule": "at the close of the first in-window 4h 12/26 cross",
            "invalidation": None, "anchor": "NO ADMISSIBLE 4h PIVOT ANCHOR — NOT TAKEN",
            "risk": None, "target": None, "target_score": None, "reward": None,
            "toll_atr": toll_atr, "toll_price": toll_atr * atr_l, "net_rr": None,
            "wrong_if": ("no card exists: the rule card refuses a trade with no "
                         "admissible structural anchor, and the rail does not "
                         "invent one"),
        }
    stop_px = float(stop.stop_px)
    anchor = (f"4h swing pivot @bar {stop.anchor_bar} + "
              f"{PE.REGISTER['STOP_BUF_ATR']['value']} ATR buffer"
              + ("; RAIL BINDING at 1.0 ATR" if stop.rail_binding else "")
              + f"; {stop.n_eligible} eligible pivot(s)")
    risk = float(stop.r_dist)

    side = [c for c in clusters
            if (c["mean"] - entry) * direction > 0 and c["score"] > 0]
    tgt = min(side, key=lambda c: abs(c["mean"] - entry)) if side else None
    target_px = tgt["mean"] if tgt else None
    reward = abs(target_px - entry) if target_px is not None else None

    toll_price = toll_atr * atr_l
    rr = net_rr(reward, risk, toll_price) if reward is not None else None
    return {
        "direction": "long" if direction == 1 else "short",
        "station": w.station, "arm_ms": w.arm_ms, "disp": w.disp,
        "not_taken": False, "provisional": provisional, "entry_basis": entry_basis,
        "trigger_age_bars": w.trigger_age_bars, "trigger_stale": w.trigger_stale,
        "entry": entry, "entry_rule": "at the close of the first in-window 4h 12/26 cross",
        "invalidation": stop_px, "anchor": anchor, "risk": risk,
        "target": target_px, "target_score": (tgt["score"] if tgt else None),
        "reward": reward, "toll_atr": toll_atr, "toll_price": toll_price,
        "net_rr": rr,
        "wrong_if": ("a counter 4h 12/89 cross, or the 4h 89/316 turning against "
                     "the window — either closes it (rule card BELL)"),
    }


def fired_events(roster, as_of_ms, g, log=print) -> dict:
    """C-8. Yesterday's fired events, classified against the GRID's NET table.

    RECORDING, not aggregating: this counts events and prints the GRID's
    already-filed NET for that (lens, class). It computes no outcome of its
    own — that would be census work under G-7.
    """
    hours = REGISTER["FIRED_WINDOW_HOURS"]["value"]
    out, warm_note = [], {}
    tf_ms = {"5m": 300_000, "15m": 900_000, "30m": 1_800_000,
             "1h": 3_600_000, "4h": 14_400_000}
    warm = P.warm_bars(316)
    for tf in REGISTER["GRID_LENSES"]["value"]:
        src_tf, step = ("15m", 2) if tf == "30m" else (tf, 1)
        need = warm * 3 + int(hours * 3_600_000 / tf_ms[tf]) + 10
        for sym in roster:
            try:
                df = load_lens(sym, src_tf, tail=need * step + 50)
            except FileNotFoundError:
                continue
            if step > 1:
                r = ST.resample_ohlcv(df["open_time"].to_numpy("int64"),
                                      df["open"].to_numpy("float64"),
                                      df["high"].to_numpy("float64"),
                                      df["low"].to_numpy("float64"),
                                      df["close"].to_numpy("float64"),
                                      df["volume"].to_numpy("float64"), tf_ms[tf])
                df = pd.DataFrame({k: r[k] for k in
                                   ("open_time", "open", "high", "low", "close", "volume")})
            if as_of_ms is not None:
                df = df[df["open_time"] <= as_of_ms].reset_index(drop=True)
            if len(df) < warm + 5:
                continue
            f = PE.build_frame(df)
            x = PE.crosses(f)
            cut = int(f.open_ms[-1]) - hours * 3_600_000
            recent = f.open_ms >= cut
            for cls, series in (("12_89", x["w_up"] | x["w_dn"]),
                                ("12_26 IN-WINDOW", x["t_up"] | x["t_dn"]),
                                ("89_316", x["b_up"] | x["b_dn"])):
                n = int(np.count_nonzero(series & recent))
                if n:
                    out.append({"lens": tf, "asset": sym, "cls": cls, "n": n})
            warm_note[tf] = (f"EMA warm-up: {warm} bars needed for e316; "
                             f"{len(df)} loaded on {tf}"
                             + (" (derived from 15m by resample)" if step > 1 else ""))
    rows = {}
    for e in out:
        k = (e["lens"], e["cls"])
        rows.setdefault(k, {"lens": e["lens"], "cls": e["cls"], "n": 0, "assets": []})
        rows[k]["n"] += e["n"]
        rows[k]["assets"].append(f"{e['asset'].replace('USDT','')}x{e['n']}")
    for k, r in rows.items():
        row = g[(g["tf"] == r["lens"]) & (g["cls"] == r["cls"])]
        for h in ("H20", "H100"):
            v = float(row[f"{h}_net"].iloc[0]) if not row.empty else float("nan")
            r[f"{h}_net"] = None if not np.isfinite(v) else round(v, 6)
        t = float(row["toll_atr"].iloc[0]) if not row.empty else float("nan")
        r["toll_atr"] = None if not np.isfinite(t) else round(t, 6)
    log(f"  fired events in the last {hours}h: "
        f"{sum(r['n'] for r in rows.values())} across {len(rows)} (lens, class) cells")
    return {"rows": sorted(rows.values(), key=lambda r: (r["lens"], r["cls"])),
            "hours": hours, "warm_note": warm_note}


# ═══════════════════════════════════════════════════════════════ THE RENDER

def _f(x, nd=6):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    return f"{x:,.{nd}g}"


# The Spaghetti's inks (OR-1 STEP F). Hues 35..325 leave out the 35 degrees either side
# of red; 62% saturation at 34% lightness reads on REGISTER['TYPE_PALETTE']'s paper where
# the dark page's 55%/58% would wash out. Eighteen hues are not eighteen NAMES: the
# legend under the panel names every line, and the panel was never the place to read a
# single symbol off (that is the Board's job).
SPAG_HUE_LO, SPAG_HUE_HI = 35, 325
SPAG_SAT_LIGHT = "62%,34%"


def svg_spaghetti(view: dict) -> str:
    """C-4. One panel. Each asset's ATR-normalised path from its LAST 89/316
    tide flip. Event-anchored, exactly as the operator's two pins name it."""
    W, H, PAD = 920, 300, 34
    paths, legend = [], []
    series = []
    for a in view["assets"]:
        st = a["station"]
        if st.tide_flip_i is None:
            continue
        h4 = load_lens(a["symbol"], "4h")
        c = h4["close"].to_numpy("float64")
        i0 = st.tide_flip_i
        if i0 >= len(c) - 1:
            continue
        seg = (c[i0:] - c[i0]) / a["atr_d"]
        series.append((a["symbol"], seg, st.tide_flip_dir))
    if not series:
        return "<p class='muted'>no tide flip in loaded history</p>"
    n_max = max(len(s) for _, s, _ in series)
    v_max = max(float(np.nanmax(np.abs(s))) for _, s, _ in series) or 1.0
    for k, (sym, seg, dirn) in enumerate(series):
        # OR-1 STEP F, INK ONLY (the points are untouched): the hue wheel runs
        # SPAG_HUE_LO..SPAG_HUE_HI and so skips the red band — red is the page's alarm
        # ink (REGISTER['TYPE_PALETTE']) — and the lines are set dark enough for paper.
        hue = SPAG_HUE_LO + int((SPAG_HUE_HI - SPAG_HUE_LO) * k / max(1, len(series)))
        pts = []
        for i, v in enumerate(seg):
            x = PAD + (W - 2 * PAD) * (i / max(1, n_max - 1))
            y = H / 2 - (H / 2 - PAD) * (v / v_max)
            pts.append(f"{x:.1f},{y:.1f}")
        paths.append(f'<polyline points="{" ".join(pts)}" fill="none" '
                     f'stroke="hsl({hue},{SPAG_SAT_LIGHT})" stroke-width="1.6" opacity="0.85"/>')
        legend.append(f'<span style="color:hsl({hue},{SPAG_SAT_LIGHT})">■</span> '
                      f'{html.escape(sym.replace("USDT",""))} '
                      f'<span class="muted">({dirn}, {len(seg)}b)</span>')
    axis = (f'<line x1="{PAD}" y1="{H/2}" x2="{W-PAD}" y2="{H/2}" '
            f'stroke="currentColor" stroke-opacity="0.5" stroke-dasharray="3 3"/>')
    return (f'<svg class="spag" viewBox="0 0 {W} {H}" width="100%" role="img" '
            f'aria-label="ATR-normalised paths since each asset\'s last 89/316 tide flip">'
            f'{axis}{"".join(paths)}'
            f'<text x="{PAD}" y="16" fill="currentColor" fill-opacity="0.66" font-size="11">'
            f'+{v_max:.2f} ATR</text>'
            f'<text x="{PAD}" y="{H-6}" fill="currentColor" fill-opacity="0.66" font-size="11">'
            f'-{v_max:.2f} ATR</text></svg>'
            f'<div class="legend">{" · ".join(legend)}</div>')


MANTLE_JS = """
// heatCanvas — ported from the shipped VIZ-4 render, same law, same colours.
// disp is thread-major; null is ABSENT (alpha 0), never zero. Row order is
// flipped: rod on TOP, hem at the BOTTOM, exactly as the v4 strip draws it.
function divRGB(v){var t=Math.min(1,Math.log10(1+Math.abs(v)/0.5)/2.6);
  var a=[233,220,195],b=v>=0?[85,148,155]:[198,113,57],k=0.15+0.85*t;
  return [a[0]+(b[0]-a[0])*k,a[1]+(b[1]-a[1])*k,a[2]+(b[2]-a[2])*k];}
function heatCanvas(pl){var d=pl.data,nT=d.threads.length,nX=d.ts.length;
  var cv=document.createElement('canvas');cv.width=nX;cv.height=nT;
  var cx=cv.getContext('2d'),im=cx.createImageData(nX,nT);
  for(var i=0;i<nT;i++){var row=nT-1-i,sr=d.thread_sr[i];
    for(var j=0;j<nX;j++){var v=d.disp[i][j],o=4*(row*nX+j);
      if(v===null||v===undefined){im.data[o+3]=0;continue;}
      var c=divRGB(v),kn=d.knot[sr]&&d.knot[sr][j]===1?0.45:1;
      im.data[o]=c[0]*kn;im.data[o+1]=c[1]*kn;im.data[o+2]=c[2]*kn;im.data[o+3]=255;}}
  cx.putImageData(im,0,0);return cv;}
function paintStrips(){var P=window.__PAYLOADS||{};
  document.querySelectorAll('canvas[data-payload]').forEach(function(el){
    var pl=P[el.getAttribute('data-payload')];if(!pl)return;
    var src=heatCanvas(pl),cx=el.getContext('2d');
    cx.imageSmoothingEnabled=true;cx.drawImage(src,0,0,el.width,el.height);});}
document.addEventListener('DOMContentLoaded',paintStrips);
"""


# ─────────────────────────────── OR-1 STEP D · the range layer's three readers
# range_cell (the Board), range_watch + tide_tables (the Tide Tables section). With
# write_range_tape they are the ONLY functions that may read a["range"] (F-BR-14's
# allow-list). All three are pure functions of the view: no wall clock, no IO. The
# Board cell sits inside the section F-BR-6 renders twice and byte-compares.

def range_cell(a: dict) -> str:
    """The Board row's RANGE cell: the macro state; if a macro range is live, its
    bottom – top and the % position; a PENDING mark while a breach is open."""
    r = a.get("range") or range_empty(error=RANGE_ABSENT)
    if r.get("error"):
        return "<td class='rng'><span class='chip pend'>RANGE UNAVAILABLE</span></td>"
    bits = [f"<span class='chip'>{html.escape(str(r['state']))}</span>"]
    if r.get("has_range"):
        bits.append(f"<span class='muted'>{_f(r['bottom'])} – {_f(r['top'])}</span>")
        if r.get("pos_pct") is not None:
            bits.append(f"{r['pos_pct']:.0f}%")
    p = r.get("pending")
    if p:
        bits.append(f"<span class='chip pend'>PENDING {html.escape(str(p['side']))} "
                    f"· {p['bars_out']}b</span>")
    return f"<td class='rng'>{' '.join(bits)}</td>"


def range_watch(view: dict) -> list[dict]:
    """EDGE WATCH, as data. The contract: 'distance ≤ 0.5 ATR [VETO] OR pending breach
    open, sorted by distance'. The 0.5 is REGISTER['RANGE_WATCH_ATR']. A pending
    breach whose distance cannot be measured (no usable ATR) sorts LAST; ties break on
    the symbol so the list is deterministic. A DISPLAY LIST: nothing may act on it."""
    lim = REGISTER["RANGE_WATCH_ATR"]["value"]
    out = []
    for a in view["assets"]:
        r = a.get("range") or range_empty(error=RANGE_ABSENT)
        d, p = r.get("dist_atr"), r.get("pending")
        near = d is not None and d <= lim
        if near or p:
            out.append({"symbol": a["symbol"], "dist_atr": d, "near": near,
                        "nearest_side": r.get("nearest_side"),
                        "pos_pct": r.get("pos_pct"), "pending": p})
    out.sort(key=lambda w: (w["dist_atr"] is None,
                            w["dist_atr"] if w["dist_atr"] is not None else 0.0,
                            w["symbol"]))
    return out


def tide_tables(view: dict) -> str:
    """The TIDE TABLES section body: every roster symbol, then EDGE WATCH, then what
    this is not. Rows are in the OPERATOR'S roster order, not the Board's heat order:
    the table reads the same way every morning, and heat has no say in it."""
    lens = REGISTER["RANGE_LENS"]["value"]
    lim = REGISTER["RANGE_WATCH_ATR"]["value"]
    window = REGISTER["RANGE_WINDOW_BARS"]["value"]
    order = {s: i for i, s in enumerate(REGISTER["ROSTER"]["value"])}
    assets = sorted(view["assets"], key=lambda a: order.get(a["symbol"], len(order)))

    def _pos(r) -> str:
        v = r.get("pos_pct")
        if v is None:
            return "—"
        out = " <span class='pend'>outside, above the top</span>" if v > 100 else (
            " <span class='pend'>outside, below the bottom</span>" if v < 0 else "")
        return f"{v:.1f}%{out}"

    def _pending(p) -> str:
        if not p:
            return "—"
        return (f"<span class='chip pend'>PENDING</span> {html.escape(str(p['side']))} · "
                f"{p['bars_out']} bar(s) out · {p['closes']} close(s) beyond · opened "
                f"{html.escape(str(p['open_ts']))}Z")

    def _last(r) -> str:
        e = r.get("last_event")
        if not e:
            return "<span class='muted'>none yet</span>"
        return (f"{html.escape(str(e['event']))} <span class='muted'>· {e['age_bars']} "
                f"bar(s) ago · {html.escape(str(e['ts']))}Z</span>")

    def _bars(r) -> str:
        n = int(r.get("n_bars") or 0)
        return f"{n:,}" + (" <span class='muted'>(short)</span>" if n < window else "")

    rows, n_live, n_pend, n_fail = [], 0, 0, 0
    for a in assets:
        r = a.get("range") or range_empty(error=RANGE_ABSENT)
        sym = html.escape(a["symbol"].replace("USDT", ""))
        if r.get("error"):
            n_fail += 1
            rows.append(f"<tr><td class='sym'>{sym}</td><td><span class='chip pend'>"
                        f"{RANGE_UNAVAILABLE}</span></td><td colspan='6' class='pend'>RANGE "
                        f"LAYER FAILED on this symbol — {html.escape(str(r['error']))}. Every "
                        f"other section is unaffected.</td></tr>")
            continue
        state = f"<span class='chip'>{html.escape(str(r['state']))}</span>"
        if not r.get("has_range"):
            rows.append(f"<tr><td class='sym'>{sym}</td><td>{state}</td>"
                        f"<td colspan='4' class='muted'>no live macro range</td>"
                        f"<td>{_last(r)}</td><td class='num'>{_bars(r)}</td></tr>")
            continue
        n_live += 1
        n_pend += 1 if r.get("pending") else 0
        dist = ("—" if r.get("dist_atr") is None else
                f"{r['dist_atr']:.2f}<span class='muted'> ATR to the "
                f"{html.escape(str(r['nearest_side']))}</span>")
        rows.append(f"<tr><td class='sym'>{sym}</td><td>{state}</td>"
                    f"<td class='num'>{_f(r['bottom'])} – {_f(r['top'])}</td>"
                    f"<td class='num'>{_pos(r)}</td><td class='num'>{dist}</td>"
                    f"<td>{_pending(r.get('pending'))}</td>"
                    f"<td>{_last(r)}</td><td class='num'>{_bars(r)}</td></tr>")

    watch = range_watch(view)
    if watch:
        wrows = []
        for w in watch:
            why = " · ".join(x for x in (
                f"within {lim:g} ATR of the {w['nearest_side']}" if w["near"] else "",
                "breach PENDING" if w["pending"] else "") if x)
            dist = "—" if w["dist_atr"] is None else f"{w['dist_atr']:.2f}"
            pos = "—" if w["pos_pct"] is None else f"{w['pos_pct']:.1f}%"
            wrows.append(f"<tr><td class='sym'>{html.escape(w['symbol'].replace('USDT', ''))}"
                         f"</td><td class='num'>{dist}</td>"
                         f"<td>{html.escape(str(w['nearest_side'] or '—'))}</td>"
                         f"<td class='num'>{pos}</td><td>{html.escape(why)}</td>"
                         f"<td>{_pending(w['pending'])}</td></tr>")
        watch_html = ("<table><tr><th>asset</th><th>dist ATR</th><th>boundary</th>"
                      "<th>position</th><th>why it is here</th><th>pending breach</th></tr>"
                      + "".join(wrows) + "</table>")
    else:
        watch_html = (f"<p class='muted'>EDGE WATCH is empty: no roster symbol is within "
                      f"{lim:g} ATR of a live macro boundary, and no breach is pending.</p>")

    return f"""<p class="small muted">RangeFinder v2, MACRO scale, on the {lens} lens, over the
last {window:,} bars of the frame the Board already reads. {n_live} of {len(assets)} roster
symbol(s) hold a live macro range · {n_pend} breach(es) pending{f' · {n_fail} UNAVAILABLE' if n_fail else ''}.
Rows are in the operator's roster order. ("Tide Tables" is this section's name; it is not
the 89/316 tide of the Board's regime chip.)</p>
<table><tr><th>asset</th><th>macro state</th><th>macro bottom – top</th><th>position</th>
<th>nearest boundary</th><th>pending breach</th><th>last event</th><th>bars</th></tr>
{''.join(rows)}</table>
<h3>EDGE WATCH — {len(watch)} of {len(assets)} · within {lim:g} ATR of a macro boundary [VETO], or a breach pending · sorted by distance</h3>
{watch_html}
<p class="small muted">WHAT THIS IS NOT. The range pins were calibrated on BTC alone — the
micro pins on BTC 1D (KEY-A), the v2 macro pins on BTC 4h (KEY-C) — and are UNCALIBRATED on
every other symbol: off BTC these are borrowed numbers drawing boxes, not a measured
structure. DISPLAY-ONLY · renders, never rules: no gate, filter, heat, station, card or
sizing reads a range; the Board's sort and every posture word exist before the range does
(F-BR-14). KNOWN PRECISION HAZARD: the range twin's event log rounds prices to 2 dp, which
distorts MICRO containment on sub-dollar assets; this layer reads only the full-precision
MACRO Range fields and prints no micro range. ATR here is the range machine's own ATR(14) on
the {lens} tape, not the daily ATR behind the Board's dist column. A position above 100% or
below 0% is a close outside the box while a breach is pending. Each row is measured at that
symbol's own last cached {lens} bar; "(short)" marks a cache holding fewer than {window:,} bars.
RANGE_LENS and RANGE_WATCH_ATR are [VETO]: see the appendix.</p>"""


# ─────────────────────────────── OR-1 STEP E · THE MARKET PAGE (operator ruling 7)
# The contract: "oracle_daily reads the json only (cache-only stays true). Render two
# tables, top 50 by signed % change each: OVERNIGHT and THE WEEK; footnote universe size
# + fetch time; if the fetch failed, the page prints 'WIRE DOWN — no movers this
# edition', never stale numbers."
#
# THE WALL, both halves of it. (1) The Oracle is CACHE-ONLY (BR-1b: "it may never fetch
# inside a firewalled run") and a top-50 of ~530 contracts cannot be built from a cache
# that holds only the roster, so the fetching lives in scripts/oracle_movers.py, its
# own process, which this file NEVER imports. One json crosses, read by path. (2) OR-1
# §2: "no gate, filter, or sizing reads a range or a mover." The range layer needed an
# allow-list of seven readers because a range rides in the view. A mover does not ride
# anywhere: it is never put in the view, so build_view, the tape, the calibration
# record and every card CANNOT see one. load_movers() reads the file, movers_top()
# orders its rows, market_page() prints them, and render_html() calls
# market_page(date_str) ONCE; outside those, and the module constants just below, this
# file does not name a mover. F-MV-9 holds that by AST and by import closure; F-MV-8
# renders the page against every kind of bad document.
#
# NEVER A STALE NUMBER, which is the reader's half of the organ's contract ("a reader may
# print numbers ONLY from a document whose status is OK AND whose date is the edition's
# own date"). The loader opens EXACTLY ONE path, the one named for the edition's date.
# It never lists the directory, so there is no "newest file" for it to fall back to:
# yesterday's document, however healthy, is not reachable from here. Absent, unparseable,
# dated otherwise, status not OK, a fetch still in flight, or a table that is not what
# the organ promises: each is WIRE DOWN with its reason, and not one row.
#
# WHAT THE EDITION DATE IS: run()'s date_str, the machine-local date the edition is
# named by, which is the same clock the organ names its json by (oracle_movers.
# local_date). A json fetched at 09:00 is still "today's" at 16:00: the ruling asks for
# the day's list, not a live ticker, and the fetch time prints under the tables so the
# age is never hidden.
#
# A DISPLAY ORGAN MAY NOT TAKE THE PAGE DOWN (the range layer's rule, same reason):
# neither function raises. A fault is a WIRE DOWN line with the fault in it.

WIRE_DOWN = "WIRE DOWN — no movers this edition"
# (json table key, printed title): the contract's two tables, in the contract's order.
MOVERS_TABLES = (("overnight", "OVERNIGHT"), ("weekly", "THE WEEK"))
MOVERS_REASON_MAX = 600          # characters of a reason the page will print


def load_movers(date_str: str) -> tuple[dict | None, str]:
    """The movers document for the EDITION DATE, or None and the honest reason.

    PURE READ of one path: MOVERS_DIR / movers_<date_str>.json. No directory listing,
    no glob, no "latest", no network, no wall clock, no write; MOVERS_DIR is not created
    if it is missing. Returns (doc, "") only for a document that is parseable, dated
    `date_str`, status "OK", not in flight, and whose printable parts are what the
    organ's docstring promises: top_n a positive integer, fetched_utc an aware ISO
    stamp, the two method strings, and both tables lists of {symbol, pct, last_price}
    with finite numbers. Anything else is (None, reason). NEVER RAISES."""
    name = f"movers_{date_str}.json"
    try:
        p = MOVERS_DIR / name
        if not p.is_file():
            return None, (f"{name} is absent — the movers organ has written no document for "
                          f"this edition's date (it did not run, or it ran on another date)")
        try:
            doc = json.loads(p.read_bytes().decode("utf-8"))
        except ValueError as e:        # JSONDecodeError and UnicodeDecodeError both are
            return None, f"{name} is unparseable ({e.__class__.__name__})"
        if not isinstance(doc, dict):
            return None, f"{name} is unparseable (a json {type(doc).__name__}, not an object)"
        if doc.get("date") != date_str:
            return None, (f"{name} carries the date {doc.get('date')!r}, not this edition's "
                          f"{date_str}")
        if doc.get("status") != "OK":
            said = "; ".join(str(x) for x in (doc.get("fail_reasons") or [])) or "no reason recorded"
            return None, (f"{name} says status {doc.get('status')!r}"
                          + (", in flight or never finished" if doc.get("in_flight") else "")
                          + f" — {said}")
        if doc.get("in_flight") is not False:
            # the organ writes true only on its pre-fetch placeholder, which says FAIL; an
            # OK document that is not plainly finished contradicts itself and is not printed
            return None, (f"{name} says status 'OK' but in_flight is {doc.get('in_flight')!r} — "
                          f"only a run that says it finished is printed")

        def _num(x) -> bool:
            return isinstance(x, (int, float)) and not isinstance(x, bool) and bool(np.isfinite(x))

        bad = []
        if not (isinstance(doc.get("top_n"), int) and not isinstance(doc.get("top_n"), bool)
                and doc["top_n"] > 0):
            bad.append(f"top_n is {doc.get('top_n')!r}")
        if not (isinstance(doc.get("universe_count"), int)
                and not isinstance(doc.get("universe_count"), bool)):
            bad.append(f"universe_count is {doc.get('universe_count')!r}")
        try:
            if datetime.fromisoformat(doc["fetched_utc"]).tzinfo is None:
                bad.append("fetched_utc carries no UTC offset")
        except Exception:
            bad.append(f"fetched_utc is {doc.get('fetched_utc')!r}")
        method = doc.get("method")
        for key, _title in MOVERS_TABLES:
            if not (isinstance(method, dict) and isinstance(method.get(key), str) and method[key]):
                bad.append(f"no method string for {key}")
            rows = doc.get(key)
            if not isinstance(rows, list):
                bad.append(f"{key} is not a list")
            elif not all(isinstance(r, dict) and isinstance(r.get("symbol"), str) and r["symbol"]
                         and _num(r.get("pct")) and _num(r.get("last_price")) for r in rows):
                bad.append(f"{key} holds a row that is not {{symbol, pct, last_price}} with "
                           f"finite numbers")
        if bad:
            return None, f"{name} says OK but is malformed: " + "; ".join(bad)
        return doc, ""
    except Exception as e:                     # contained, never silent: it prints
        return None, f"{name} could not be read ({e.__class__.__name__}: {e})"


def movers_top(rows: list[dict], n: int) -> list[dict]:
    """The first n rows by SIGNED pct, largest first, ties on the symbol: the organ's
    own rule (oracle_movers.sort_rows), re-applied HERE so the order on the page is this
    file's guarantee and not an assumption about the file it was handed."""
    return sorted(rows, key=lambda r: (-r["pct"], r["symbol"]))[:n]


def market_page(date_str: str) -> str:
    """The Market Page section body. A pure function of (MOVERS_DIR, date_str): no wall
    clock, no network, no write, and NO VIEW: it takes no asset, no heat, no station, and
    hands nothing back to anything but the page. Prints the two tables for a document
    load_movers() accepts; otherwise exactly the WIRE DOWN line, the reason, and no row."""
    def _down(why: str) -> str:
        return (f"<p class='wire'>{html.escape(WIRE_DOWN)}</p>"
                f"<p class='small muted'>reason: {html.escape(why[:MOVERS_REASON_MAX])}</p>")

    doc, why = load_movers(date_str)
    if doc is None:
        return _down(why)
    try:
        n = doc["top_n"]
        fetched = datetime.fromisoformat(doc["fetched_utc"]).astimezone(timezone.utc)
        try:
            local = f"{fetched.astimezone(ZoneInfo(ZONE)).strftime('%Y-%m-%d %H:%M')} Buenos Aires"
        except Exception:                      # no tz database: the organ's own stamp
            local = f"{doc.get('fetched_local')} machine-local"
        tables, counts = [], []
        for key, title in MOVERS_TABLES:
            rows = movers_top(doc[key], n)
            body = "".join(
                f"<tr class='mv'><td class='num muted'>{i}</td>"
                f"<td class='sym'>{html.escape(r['symbol'].removesuffix('USDT'))}</td>"
                f"<td class='num'>{r['pct']:+,.3f}%</td>"
                f"<td class='num'>"
                f"{np.format_float_positional(r['last_price'], precision=10, unique=True, trim='-')}"
                f"</td></tr>" for i, r in enumerate(rows, 1))
            tables.append(
                f"<div><h3>{title} — top {len(rows)} of {len(doc[key]):,} by signed % change, "
                f"largest first</h3><table class='movers' data-table='{key}'><tr><th>#</th>"
                f"<th>symbol</th><th>% change</th><th>last price</th></tr>{body}</table></div>")
            nulls = doc.get(f"{key}_null")
            counts.append(f"{title}: {len(doc[key]):,} with a number, "
                          f"{len(nulls) if isinstance(nulls, list) else '—'} listed without one")
        reg = doc.get("register") if isinstance(doc.get("register"), dict) else {}
        # The organ's UNRULED rows surface HERE and not in the appendix table: the
        # appendix is built by render_html, which may not read a movers document.
        veto = [f"{k} = {v.get('value')}" for k, v in reg.items()
                if isinstance(v, dict) and not v.get("ruled", True)]
        veto_html = ("<p class='small muted'><span class='chip'>[VETO]</span> unruled in the "
                     "movers organ's own register, as this json carries it (operator defaults, "
                     "standing until vetoed): " + html.escape(" · ".join(veto)) + "</p>"
                     ) if veto else ""
        return f"""<p class="small muted">The day's list, not a live ticker: the {n} largest SIGNED
percent changes in each of two windows, largest gain first, over the whole Binance USDT-M
perpetual universe. Symbols print without their USDT quote.</p>
<div class="mkt">{''.join(tables)}</div>
<p class="small muted">UNIVERSE {doc['universe_count']:,} contract(s) — counted by the organ,
never asserted · {' · '.join(counts)}. FETCHED {fetched.strftime('%Y-%m-%dT%H:%M:%SZ')} UTC ·
{html.escape(local)}, by scripts/oracle_movers.py, a separate fetch-only organ: the Oracle read
movers_{html.escape(date_str)}.json and fetched nothing. OVERNIGHT, the method of record:
{html.escape(doc['method']['overnight'])}. THE WEEK, the method of record:
{html.escape(doc['method']['weekly'])}. The cut at {n} is the json's own top_n (operator ruling
7). DISPLAY-ONLY · renders, never rules: no gate, filter, heat, station, card or sizing reads a
mover, and nothing on this page reaches the tape or the calibration record (F-MV-9). A
document that is absent, unparseable, dated otherwise or not status OK prints no row at all,
only that the wire is down and why: an older day's numbers are never shown (F-MV-8).</p>
{veto_html}"""
    except Exception as e:                     # contained, never silent: it prints
        return _down(f"the Market Page could not be set from movers_{date_str}.json "
                     f"({e.__class__.__name__}: {e})")


# ═════════════════════════════ OR-1 STEP F · THE DAILY ORACLE, the typesetting
# The contract: "semantics untouched, template only". Everything from here to the end
# of render_html is INK AND ORDER. The rows, cards, windows, telegrams, grid rows and
# stamps are built exactly as they were before STEP F; what is new is a stylesheet, a
# masthead, eight headings, one caption, and a headline that restates the Board's own
# posture column. None of these helpers is handed, or may name, a range or a mover
# (F-BR-14 and F-MV-9 read this file's AST and would go red), and none reads a clock:
# the Front Page and The Watch are rendered twice and byte-compared on every edition
# (F-BR-6, and the wrapper's per-edition self-check — once per on-demand edition since
# the clock was suspended 2026-09-21, which may be no times on a day and five on another).

# The dateline's stamp format, shared by the band and the colophon so that "<as-of>"
# is the same string wherever the page prints it.
AS_OF_FMT = "%Y-%m-%dT%H:%MZ"

# THE STYLESHEET. Plain CSS with FIVE placeholders — __PAPER__, __INK__, __RED__,
# __INK_RGB__ and __SERIF__ — so it reads as CSS and not as an f-string of doubled
# braces; page_css() fills them from the REGISTER (three inks, the ink again as r,g,b
# for the alpha rules, and the serif stack). The comment read "four": page_css() does
# plain str.replace and raises nothing on a miss, so an editor who trusted a short
# inventory would ship a literal `__SERIF__` inside a `font:` shorthand and drop the
# whole declaration in silence. WHAT THE RULES ARE FOR, since a style block carries no
# why of its own:
#   · hairline column rules — `column-rule` on the lead, the Docket, the Watch, the
#     Telegrams, The Market Page and the colophon; `td+td` rules inside every table.
#   · small-caps section heads — on the h2 ELEMENT. An attribute on <h2> would break
#     every selector that splits the page on the literal '<h2>'.
#   · the drop cap — `.lead::first-letter`, a float, because `initial-letter` is not
#     in every browser the operator may open the page with.
#   · red — ONLY under the alarm classes: div.stale (the band), .chip.stale, .pend,
#     .wire. F-BR-15 parses this block and goes red on the red anywhere else.
#   · the strip's ground is a hairline hatch, not a dark plate: an unwoven hole shows
#     the hatch, a knot stays a dark pinch, and the two cannot be confused on paper.
#   · the one media query is a WIDTH query (the masthead stacks on a phone). There is
#     no colour-scheme query and no second palette: light paper only [D-7a].
PAGE_CSS = """
:root{--paper:__PAPER__;--ink:__INK__;--red:__RED__;
  --mut:rgba(__INK_RGB__,.66);--rule:rgba(__INK_RGB__,.32);--tint:rgba(__INK_RGB__,.06)}
*{box-sizing:border-box}
html,body{background:var(--paper)}
body{margin:0;color:var(--ink);font:15px/1.5 __SERIF__;font-variant-numeric:lining-nums;
  text-rendering:optimizeLegibility;-webkit-font-smoothing:antialiased}
.wrap{max-width:1180px;margin:0 auto;padding:20px 24px 72px}
main{overflow-x:auto}
.masthead{border-top:1px solid var(--ink);padding-top:12px}
.nameplate{display:grid;grid-template-columns:minmax(150px,1fr) auto minmax(150px,1fr);
  gap:10px 22px;align-items:center}
h1{margin:0;font-size:clamp(30px,5.2vw,62px);line-height:1;font-weight:700;
  letter-spacing:.045em;text-align:center;white-space:nowrap}
.ear{max-width:240px;border:1px solid var(--ink);padding:7px 10px;font-size:12px;
  line-height:1.4;font-variant:small-caps;letter-spacing:.07em;text-align:center;
  text-wrap:balance}
.ear span{white-space:nowrap}
.ear-l{justify-self:start} .ear-r{justify-self:end}
.folio{margin-top:12px;padding:5px 6px;border-top:3px double var(--ink);
  border-bottom:1px solid var(--ink);font-size:11.5px;letter-spacing:.09em;
  font-variant:small-caps;text-align:center}
div.stale{background:var(--red);color:var(--paper);padding:10px 16px;text-align:center;
  font-size:13.5px;line-height:1.45}
div.stale b{display:block;font-size:18px;letter-spacing:.14em;text-transform:uppercase}
.dateline{margin:8px 0 0;padding-bottom:8px;border-bottom:1px solid var(--rule);
  text-align:center;font-size:12px;color:var(--mut);word-break:break-word}
h2{margin:46px 0 14px;padding:7px 0 6px;border-top:3px double var(--ink);
  border-bottom:1px solid var(--ink);font-size:20px;font-weight:700;
  font-variant:small-caps;letter-spacing:.1em;text-align:center}
h3{margin:26px 0 8px;padding-bottom:4px;border-bottom:1px solid var(--rule);
  font-size:14.5px;font-weight:700;font-variant:small-caps;letter-spacing:.08em}
.headline{margin:20px auto 8px;max-width:1000px;font-size:clamp(26px,3.6vw,46px);
  line-height:1.08;font-weight:700;text-align:center;text-wrap:balance}
.deck{margin:0 auto 18px;max-width:900px;text-align:center;font-style:italic;
  font-size:16.5px;line-height:1.35}
.cols{columns:3 250px;column-gap:32px;column-rule:1px solid var(--rule);margin:0 0 20px;
  text-align:justify;hyphens:auto;-webkit-hyphens:auto}
.cols p{margin:0 0 .75em}
.lead::first-letter{float:left;font-size:4.1em;line-height:.78;font-weight:700;
  padding:.06em .1em 0 0}
table{width:100%;border-collapse:collapse;font-size:13px;
  font-variant-numeric:lining-nums tabular-nums;border-top:2px solid var(--ink);
  border-bottom:1px solid var(--ink)}
th{text-align:left;vertical-align:bottom;font-weight:700;font-size:11.5px;
  font-variant:small-caps;letter-spacing:.08em;border-bottom:1px solid var(--ink);
  padding:5px 8px}
td{padding:5px 8px;border-bottom:1px solid var(--rule);vertical-align:top}
th+th,td+td{border-left:1px solid var(--rule)}
tr:last-child td{border-bottom:0}
.num{text-align:right}
.board td.num{white-space:nowrap}
.muted{color:var(--mut)} .small{font-size:12px;color:var(--mut)}
.sym{font-weight:700;letter-spacing:.05em}
code{font-family:"Courier New",Courier,monospace;font-size:.92em}
.chip{display:inline-block;padding:0 6px;border:1px solid var(--ink);font-size:10.5px;
  line-height:1.6;letter-spacing:.08em;text-transform:uppercase;white-space:nowrap;
  vertical-align:1px}
.chip.defer{border-style:dashed}
.t-short,.d-short{background:var(--ink);color:var(--paper)}
.t-none,.prov{border-style:dotted;color:var(--mut)}
.chip.stale{color:var(--red);border-color:var(--red);font-weight:700}
.pend{color:var(--red);border-color:var(--red);font-weight:700}
.wire{border:2px solid var(--red);color:var(--red);font-weight:700;font-size:16px;
  letter-spacing:.12em;text-align:center;padding:10px 14px;margin:10px 0 6px}
.rng{font-size:12px}
.post{font-weight:700;letter-spacing:.1em;white-space:nowrap}
tr.w-triggered{background:var(--tint)}
td.post.w-triggered{text-decoration:underline;text-decoration-thickness:2px;
  text-underline-offset:3px}
td.post.w-stalking{font-weight:400;color:var(--mut)}
td.post.w-dead{font-weight:400;font-style:italic;color:var(--mut)}
.chip.w-triggered{border:3px double var(--ink);font-weight:700}
.chip.w-armed{font-weight:700}
.chip.w-stalking{color:var(--mut);border-color:var(--rule)}
.chip.w-dead{color:var(--mut);border-style:dotted}
.docket,.watchgrid{columns:2 440px;column-gap:34px;column-rule:1px solid var(--rule)}
.card,.wcell{break-inside:avoid;margin:0 0 16px;padding:0 0 14px;
  border-bottom:1px solid var(--rule)}
.card{margin-bottom:24px;padding-bottom:0;border-bottom:0}
.card-h,.wh{display:flex;flex-wrap:wrap;gap:8px;align-items:baseline;margin-bottom:6px}
.card-h b,.wh b{font-size:19px;letter-spacing:.04em}
.kv td:first-child{width:128px;font-size:10.5px;font-weight:700;letter-spacing:.08em}
.kv td.num{text-align:left}
.big{font-size:18px;font-weight:700;line-height:1.3}
.big .muted{font-size:12.5px;font-weight:400}
figure.mantle{margin:8px 0 0}
.strip{width:100%;height:auto;display:block;border:1px solid var(--ink);
  background:repeating-linear-gradient(45deg,var(--rule) 0 1px,transparent 1px 5px)}
.stripfoot{margin-top:4px;font-size:10.5px;color:var(--mut);word-break:break-all}
.stripcap{margin-top:2px;font-size:11.5px;font-style:italic;line-height:1.35}
svg.spag{display:block;color:var(--ink);border-top:1px solid var(--rule);
  border-bottom:1px solid var(--rule)}
.legend{margin-top:6px;font-size:12px;line-height:1.7;color:var(--ink)}
pre.r1{margin:0;padding:12px 14px;border:1px solid var(--ink);columns:300px;
  column-gap:28px;column-rule:1px solid var(--rule);white-space:pre;
  font:12.5px/1.55 "Courier New",Courier,monospace}
pre.held{margin:0;padding:10px 14px;border:1px dashed var(--rule);columns:300px;
  column-gap:28px;white-space:pre;color:var(--mut);
  font:12.5px/1.55 "Courier New",Courier,monospace}
td.asof{font-size:12px;line-height:1.3}
.mkt{columns:2 340px;column-gap:34px;column-rule:1px solid var(--rule)}
.mkt>div{break-inside:avoid}
.mkt h3{margin-top:0;font-size:12.5px;letter-spacing:.03em;min-height:2.9em}
.returns td:nth-child(2){white-space:nowrap}
.veto td.num{text-align:left}
footer{margin-top:22px;padding-top:12px;border-top:1px solid var(--ink);columns:2 420px;
  column-gap:34px;column-rule:1px solid var(--rule);font-size:11.5px;line-height:1.55;
  color:var(--mut);word-break:break-word}
@media (max-width:760px){.nameplate{grid-template-columns:1fr 1fr}
  h1{grid-column:1/-1;grid-row:1;white-space:normal}
  .ear{max-width:none;justify-self:stretch}}
"""


def page_css() -> str:
    """PAGE_CSS with the REGISTER's three inks and its serif stack filled in. The muted
    ink, the hairline and the tint are the INK at an alpha, so no fourth colour exists."""
    pal = REGISTER["TYPE_PALETTE"]["value"]
    ink = pal["ink"].lstrip("#")
    ink_rgb = ",".join(str(int(ink[i:i + 2], 16)) for i in (0, 2, 4))
    return (PAGE_CSS.replace("__PAPER__", pal["paper"]).replace("__INK__", pal["ink"])
            .replace("__RED__", pal["red"]).replace("__INK_RGB__", ink_rgb)
            .replace("__SERIF__", REGISTER["TYPE_SERIF_STACK"]["value"]))


def mantle_caption() -> str:
    """The contract's caption, the strip's bar count read from REGISTER['MANTLE_BARS']:
    the same row mantle_payload() is cut by, never a second literal."""
    return REGISTER["MANTLE_CAPTION"]["value"].format(bars=REGISTER["MANTLE_BARS"]["value"])


# AMENDMENT A-OR1-1 clause vii (operator, 2026-09-22), verbatim: "Edition word follows
# verb and hour: full before 12:00 BA = Morning, after = Evening; refresh = Refresh. A
# paper printed at night does not call itself the morning's." Until this clause the word
# followed the verb alone ('Morning Edition' for every slot that was not a refresh), and
# the one on-demand edition on disk, briefs/oracle/oracle_2026-09-21.html, printed at
# 22:26 Buenos Aires, calls itself the Morning Edition. It is REPORTED, never rewritten.
EDITION_NOON_BA = 12      # vii's "12:00 BA": the first hour of the Evening Edition


def edition_verb(slot: str) -> str:
    """vii's VERB, read off the slot: 'refresh' for any slot that names a refresh (the
    historical 16:00 'refresh', the skill's 'on-demand-refresh'); 'full' for every other
    slot ('full', 'on-demand-full', a catch-up, a --no-fetch full, a fixture's)."""
    return "refresh" if "refresh" in str(slot).lower() else "full"


def print_time_ba(printed_at: datetime) -> datetime:
    """The print time on the BUENOS AIRES wall clock: converted EXPLICITLY to
    ZoneInfo(ZONE), never read in the machine's local zone (vii's hour is BA's, whatever
    zone the laptop is set to). A NAIVE datetime is refused (ValueError): its zone would be
    whatever the machine says, which is exactly what vii's hour may not depend on."""
    if printed_at.tzinfo is None or printed_at.utcoffset() is None:
        raise ValueError(f"A-OR1-1 vii: the print time {printed_at!r} is naive — its hour "
                         f"would be the machine's zone's, not Buenos Aires'; hand an aware "
                         f"datetime")
    return printed_at.astimezone(ZoneInfo(ZONE))


def edition_name(slot: str, printed_at: datetime | None) -> str:
    """The edition's word under A-OR1-1 vii: VERB and HOUR.

    The refresh verb (edition_verb) -> 'Refresh Edition', at any hour; `printed_at` is
    not read. The full verb -> by the HOUR of `printed_at` on the Buenos Aires wall clock
    (print_time_ba): 'Morning Edition' while that hour is before EDITION_NOON_BA,
    'Evening Edition' from it on.
    THE BOUNDARY, stated: 12:00:00 Buenos Aires EXACTLY is EVENING (noon is not "before
    12:00"); 11:59:59.999999 is Morning; 00:00:00 is Morning again. A full verb with no
    print time has no hour for vii to read and is REFUSED (ValueError), never defaulted:
    run() hands every edition its print time, and render_html hands a proof its as-of."""
    if edition_verb(slot) == "refresh":
        return "Refresh Edition"
    if printed_at is None:
        raise ValueError(f"A-OR1-1 vii: slot {slot!r} is the full verb and no print time was "
                         f"handed — the edition word follows the hour, and there is none")
    return ("Morning Edition" if print_time_ba(printed_at).hour < EDITION_NOON_BA
            else "Evening Edition")


def print_line(slot: str, printed_at: datetime) -> str:
    """The edition's own evidence for its word, printed in the Colophon: the print time in
    Buenos Aires to the minute, the word vii gave, the verb and the slot. Plain text (the
    caller escapes it). F-BR-15 reads it back and holds the ear to it."""
    return (f"Printed {print_time_ba(printed_at).strftime('%Y-%m-%d %H:%M')} Buenos Aires "
            f"({edition_name(slot, printed_at)}: {edition_verb(slot)}, slot {slot} · "
            f"A-OR1-1 vii)")


def edition_count(date_str: str) -> int:
    """REGISTER['EDITION_COUNT'], [VETO]: the distinct DATES among TAPE_DIR's
    oracle_tape_<date>.parquet files, `date_str` included. A pure read of file NAMES
    (no parquet is opened, nothing is written); a name whose date does not parse is not
    an edition; a missing directory counts this edition alone. Called by run(), never
    by render_html."""
    dates = {date_str}
    for p in TAPE_DIR.glob("oracle_tape_*.parquet"):
        stamp = p.stem.removeprefix("oracle_tape_")
        try:
            datetime.strptime(stamp, "%Y-%m-%d")
        except ValueError:
            continue
        dates.add(stamp)
    return len(dates)


def _names(symbols) -> str:
    """'BTC' · 'BTC and ETH' · 'BTC, ETH and SOL': symbols print without their quote."""
    xs = [s.replace("USDT", "") for s in symbols]
    return xs[0] if len(xs) == 1 else f"{', '.join(xs[:-1])} and {xs[-1]}"


def front_page(view: dict, ages: dict | None = None) -> dict:
    """The Front Page's headline, deck and lead: REGISTER['FRONT_PAGE_HEADLINE'], [VETO].

    The day's answer to the canon's one morning question, "where is business possible
    today", READ OFF THE BOARD'S OWN POSTURE COLUMN and nothing else. The two words that
    answer it are taken from posture_engine.CANON by station number, never retyped:
    station 3 (an open window holds its entry alert) and station 2 (a window is open).
    A TRIGGERED row whose trigger the Board prints STALE is set apart, by the Board's
    own test (posture_engine.stations_for: the row's FRESHEST in-window trigger is
    stale), and only a FRESH trigger earns the words 'Business possible'.
    A pure function of the view: no clock, no IO. Returns HTML-escaped strings.
    `ages` (OR-2 R-1, row_ages) names the bars the lead says the roster was read at: one
    bar when every row shares it — the text is then what it always was — and the
    oldest-to-newest span when they differ, never the hottest row's bar alone (OR1-a)."""
    assets = view["assets"]
    word_of = {v["station"]: k for k, v in PE.CANON.items()}
    w_trig, w_armed = word_of[3], word_of[2]
    by: dict[str, list[str]] = {}
    for a in assets:                               # the Board's own order (heat)
        by.setdefault(a["station"].board_word, []).append(a["symbol"])
    trig, armed = by.get(w_trig, []), by.get(w_armed, [])

    def _stale(a) -> bool:                         # the Board's own test, not a second one
        trg = [w for w in a["station"].open_windows if w.trigger_i is not None]
        return bool(trg) and bool(min(trg, key=lambda w: w.trigger_age_bars).trigger_stale)

    stale = [a["symbol"] for a in assets
             if a["station"].board_word == w_trig and _stale(a)]
    fresh = [s for s in trig if s not in stale]
    said_h = ([f"{_names(fresh)} {w_trig.lower()}"] if fresh else []) \
        + ([f"{_names(stale)} {w_trig.lower()} but stale"] if stale else []) \
        + ([f"{_names(armed)} {w_armed.lower()} and waiting"] if armed else [])
    if fresh:
        headline = "Business possible: " + "; ".join(said_h)
    elif said_h:
        headline = "No fresh trigger on the roster: " + "; ".join(said_h)
    else:
        headline = (f"No business possible today: nothing on the roster is "
                    f"{w_trig.lower()} or {w_armed.lower()}")

    order = [w_trig, w_armed] + [w for w in PE.STATION_WORDS if w not in (w_trig, w_armed)]
    order += sorted(w for w in by if w not in order)
    n_cards = sum(1 for a in assets if a["card"])
    n_win = sum(len(a["station"].open_windows) for a in assets)
    n_win_sym = sum(1 for a in assets if a["station"].open_windows)
    deck = (f"{len(assets)} on the roster, {view['lens']} lens: "
            + " · ".join(f"{len(by.get(w, []))} {w}" for w in order)
            + f" — {n_cards} Trap Card{'' if n_cards == 1 else 's'} on The Docket")

    counts = [f"{len(by.get(w, []))} {w}" for w in order]
    first = len(by.get(order[0], []))
    counts[0] = f"{first} {'is' if first == 1 else 'are'} {order[0]}"
    if ages is None or ages["newest_ms"] == ages["oldest_ms"]:
        at_bar = "at the bar of " + as_of_stamp(view["as_of_ms"] if ages is None
                                                 else ages["newest_ms"])
    else:
        at_bar = (f"each at its own bar, from {as_of_stamp(ages['oldest_ms'])} to "
                  f"{as_of_stamp(ages['newest_ms'])}")
    said = []
    if trig:
        said.append(f"{w_trig}: {_names(trig)} — an open 12/89 window that holds its "
                    f"in-window 12/26 cross, the entry alert.")
    if stale:
        said.append(f"Printed STALE, the cross older than "
                    f"{PE.REGISTER['TRIGGER_FRESH_BARS']['value']} bars [VETO]: {_names(stale)}.")
    if armed:
        said.append(f"{w_armed}: {_names(armed)} — the window is open and the cross has "
                    f"not come.")
    if not said:
        said.append("No symbol holds an open window, with its trigger or without: by the "
                    "Board's own words there is no business possible today.")
    lead = (f"Of the {len(assets)} symbol{'' if len(assets) == 1 else 's'} on the roster, read "
            f"on the {view['lens']} lens {at_bar}, {', '.join(counts[:-1])} and "
            f"{counts[-1]}. " + " ".join(said))
    inside = (f"The Docket carries {n_cards} Trap Card{'' if n_cards == 1 else 's'}, one for "
              f"each symbol with an admitted open window: pre-framed if-thens, never "
              f"recommendations. The Watch follows {n_win} living 12/89 "
              f"window{'' if n_win == 1 else 's'} on {n_win_sym} "
              f"symbol{'' if n_win_sym == 1 else 's'}, with a mantle strip for every symbol "
              f"on the roster. Then the Tide Tables, the Telegrams, The Market Page and "
              f"Yesterday's Returns; the Colophon carries the provenance and the rows still "
              f"unruled.")
    creed = ("Every posture word on this page is the posture engine's, printed and never "
             "scored. The Board is sorted by heat, which is proposed and not ruled. This "
             "page renders; it does not rule, and nothing on it is advice.")
    esc = lambda s: html.escape(s, quote=False)    # noqa: E731
    return {"headline": esc(headline), "deck": esc(deck),
            "lead": (f'<p class="lead">{esc(lead)}</p><p>{esc(inside)}</p>'
                     f'<p>{esc(creed)}</p>')}


def render_html(view: dict, date_str: str, canon_sha: str, *,
                edition_no: int | None = None, slot: str = "full",
                printed_at: datetime | None = None) -> str:
    """The page. `edition_no`, `slot` and `printed_at` are the masthead's three variables
    and are KEYWORDS so that every older caller — the fixtures, the wrapper's per-edition
    self-check, the movers fixtures — still calls render_html(view, date_str, canon_sha)
    and still gets a page. A render nobody numbered is a PROOF, not an edition, and says
    so: 'No. —'. run() numbers the real ones (edition_count).

    `printed_at` is the print time (A-OR1-1 vii), an AWARE datetime taken ONCE by run():
    the ear's word follows its Buenos Aires hour and the Colophon prints it (print_line).
    render_html NEVER READS THE CLOCK FOR THE PRINT TIME, so the ear's word and the
    'Printed' line are functions of what it is handed. Since OR-2 R-1 the A2-7 staleness
    is too: every row's age (and so its STALE mark, its HELD R1 lines, the dateline's
    count and the LATE EDITION band) is measured to the print time it is handed
    (row_ages), where until then the band alone was judged against the wall clock at
    render time and could rise between two renders of the same inputs.
    A render handed no print time is UNTIMED (a second, separate property from the
    PROOF above, which is about the number): it prints no 'Printed' line, the Colophon
    says it is untimed, its ear reads vii at the view's as-of bar — a stamp it was
    handed, not the wall clock — and it ages every row against its OWN newest row."""
    lens = view["lens"]
    a0 = view["assets"]
    as_of = datetime.fromtimestamp(view["as_of_ms"] / 1000, timezone.utc)
    mast = REGISTER["MASTHEAD"]["value"]
    sec = [html.escape(s, quote=False) for s in REGISTER["SECTIONS"]["value"]]
    caption = html.escape(mantle_caption(), quote=False)
    # OR-2 R-1: every row aged ONCE, against the print time (positional on purpose)
    ages = row_ages(view, printed_at)
    fp = front_page(view, ages)
    ag_rows = ages["rows"]
    newest_s, oldest_s = as_of_stamp(ages["newest_ms"]), as_of_stamp(ages["oldest_ms"])

    # each ear item in its own no-wrap span, so a narrow ear breaks BETWEEN items and
    # never inside the date; the ear's text is still the contract's, " · "-joined
    def _ear(*items) -> str:
        return " · ".join(f"<span>{html.escape(str(x), quote=False)}</span>" for x in items)

    ear_left = _ear(mast["volume"], f"No. {'—' if edition_no is None else int(edition_no)}")
    # A-OR1-1 vii: the word follows the verb and the print time's Buenos Aires hour
    ear_right = _ear(mast["city"], date_str,
                     edition_name(slot, as_of if printed_at is None else printed_at),
                     mast["price"])
    if printed_at is None:
        printed = html.escape(
            f"UNTIMED: this render was handed no print time (run() hands every "
            f"edition its own), so it carries no print line; its ear reads A-OR1-1 vii at "
            f"the as-of bar, {print_time_ba(as_of).strftime('%Y-%m-%d %H:%M')} Buenos Aires.",
            quote=False)
    else:
        printed = html.escape(print_line(slot, printed_at), quote=False)

    board = []
    for a in a0:
        st = a["station"]
        w = st.board_word
        lis_txt = []
        for key in ("above", "below"):
            ln = a["lis"].get(key) if isinstance(a["lis"], dict) else None
            if ln and ln.get("mean") is not None:
                lis_txt.append(f"{key} {_f(ln['mean'])} "
                               f"<span class='muted'>(score {ln.get('score','—')})</span>")
        board.append(
            f"<tr class='w-{w.lower()}'><td class='sym'>{html.escape(a['symbol'].replace('USDT',''))}</td>"
            f"<td><span class='chip t-{st.tide}'>{st.tide}</span></td>"
            f"<td class='num'>{a['nearest_d']:.2f}<span class='muted'> ATR</span></td>"
            f"<td class='num muted'>{a['nearest']['score'] if a['nearest'] else '—'}</td>"
            f"<td class='lis'>{' · '.join(lis_txt) or '<span class=muted>—</span>'}</td>"
            f"<td class='post w-{w.lower()}'>{w}</td>"
            f"<td class='muted small'>{html.escape(st.board_reason)}</td>"
            f"{age_cell(ag_rows[a['symbol']])}"
            f"<td class='num muted'>{a['heat']:.3f}</td>"
            f"{range_cell(a)}</tr>")

    cards = []
    for a in a0:
        c = a["card"]
        if not c:
            continue
        cards.append(f"""
<div class="card">
  <div class="card-h"><b>{html.escape(a['symbol'].replace('USDT',''))}</b>
    <span class="chip d-{c['direction']}">{c['direction']}</span>
    <span class="chip w-{c['station'].lower()}">{c['station']}</span>
    {'<span class="chip stale">STALE TRIGGER</span>' if c.get('trigger_stale') else ''}
    {'<span class="chip prov">PROVISIONAL</span>' if c.get('provisional') else ''}
    {age_chip(ag_rows[a['symbol']])}
    <span class="muted small">displacement {c['disp']:.2f} ATR at the arming</span></div>
  <table class="kv">
    <tr><td>IF</td><td>{html.escape(c['entry_rule'])}</td></tr>
    <tr><td>ENTRY</td><td class="num">{_f(c['entry'])}
        <span class="muted">— {html.escape(c['entry_basis'])}</span></td></tr>
    <tr><td>INVALIDATION</td><td class="num">{_f(c['invalidation'])}
        <span class="muted">— {html.escape(c['anchor'])}; risk {_f(c['risk'])}</span></td></tr>
    <tr><td>TARGET</td><td class="num">{_f(c['target'])}
        <span class="muted">cluster score {c['target_score'] if c['target_score'] is not None else '—'}</span></td></tr>
    <tr><td>NET R:R</td><td class="num big">{'—' if c['net_rr'] is None else f"{c['net_rr']:.2f}"}
        <span class="muted">after toll {c['toll_atr']:.6f} ATR = {_f(c['toll_price'])}
        · {html.escape(REGISTER['NET_RR_FORM']['value'])} [VETO]</span></td></tr>
    <tr><td>WHAT PROVES ME WRONG</td><td>{html.escape(c['wrong_if'])}</td></tr>
  </table>
</div>""")

    watch = []
    for a in a0:
        st = a["station"]
        rows = []
        for w in st.open_windows:
            rows.append(f"<tr><td>{'long' if w.direction==1 else 'short'}</td>"
                        f"<td class='num'>{w.age_bars}</td>"
                        f"<td class='num'>{w.disp:.2f}</td>"
                        f"<td>{'TRIGGERED' if w.trigger_i is not None else 'waiting'}</td></tr>")
        tbl = ("<table class='watch'><tr><th>dir</th><th>age (4h bars)</th>"
               "<th>disp ATR</th><th>trigger</th></tr>" + "".join(rows) + "</table>"
               ) if rows else "<p class='muted small'>no open window</p>"
        watch.append(f"""
<div class="wcell">
  <div class="wh"><b>{html.escape(a['symbol'].replace('USDT',''))}</b>
      <span class="chip w-{st.board_word.lower()}">{st.board_word}</span></div>
  {tbl}
  <figure class="mantle"><canvas width="960" height="180" class="strip"
          data-payload="{html.escape(a['payload_name'])}"></canvas>
  <div class="stripfoot">payload {html.escape(a['payload_name'])} sha256
      {a['payload_sha']}</div>
  <figcaption class="stripcap">{caption}</figcaption></figure>
</div>""")

    fired = []
    for r in view["fired"]["rows"]:
        toll_s = "—" if r["toll_atr"] is None else format(r["toll_atr"], ".6f")
        h20_s = "—" if r["H20_net"] is None else format(r["H20_net"], "+.4f")
        h100_s = "—" if r["H100_net"] is None else format(r["H100_net"], "+.4f")
        fired.append(f"<tr><td>{r['lens']}</td><td>{html.escape(r['cls'])}</td>"
                     f"<td class='num'>{r['n']}</td>"
                     f"<td class='num'>{toll_s}</td>"
                     f"<td class='num'>{h20_s}</td>"
                     f"<td class='num'>{h100_s}</td>"
                     f"<td class='muted small'>{html.escape(', '.join(r['assets']))}</td></tr>")

    r1, r1_held = r1_split(view, ages["stale"])

    def _chip(src):
        return ('<span class="chip defer">DEFERRED-TO-BR2</span>'
                if src.get("deferred_to") == "BR-2"
                else '<span class="chip">[VETO]</span>')

    veto = []
    rows = ([(k, v) for k, v in PE.REGISTER.items() if not v["ruled"]]
            + [(k, v) for k, v in REGISTER.items() if not v["ruled"]]
            + [(f"CANON.{k}", v) for k, v in PE.CANON.items() if not v["ruled"]])
    try:
        import oracle_topup as _TU
        rows += [(k, v) for k, v in _TU.REGISTER.items() if not v.get("ruled", True)]
    except Exception:
        pass
    for name, src in rows:
        veto.append(f"<tr><td><code>{html.escape(name)}</code></td>"
                    f"<td>{_chip(src)}</td>"
                    f"<td class='num'>{html.escape(str(src.get('value', 'gate')))}</td>"
                    f"<td class='small'>{html.escape(src['source'])}</td></tr>")
    # THE FOOTNOTE COUNTS THE TABLE, it does not assert about it. It read "each is
    # DEFERRED-TO-BR2" — true of 9 rows and false of 5 (TARGET_BUCKET_ATR from STEP B,
    # RANGE_LENS and RANGE_WATCH_ATR from STEP D, EDITION_COUNT and FRONT_PAGE_HEADLINE
    # from STEP F), which carry no `deferred_to` key, print a bare [VETO] and are this
    # build's own defaults waiting on THIS operator, now. Sending him to BR-2 for them
    # sends him to a ruling that was never asked to cover them. Both integers come from
    # `rows`, the same list the table is built from, so the sentence cannot drift again.
    n_defer = sum(1 for _n, _s in rows if _s.get("deferred_to") == "BR-2")
    n_veto = len(rows) - n_defer
    veto_note = (
        f"{n_defer} of the {len(rows)} rows below are DEFERRED-TO-BR2, which proposes a "
        f"measured value from a week of D-7 distributions. {n_veto} carry a bare [VETO]: "
        f"builder defaults of this build, unruled, awaiting the operator's own ruling — "
        f"each row's last column names the step that proposed it. Nothing self-adopts.")

    pay_js = []
    for name, pl in view["payloads"].items():
        blob = json.dumps(pl, separators=(",", ":"), ensure_ascii=False)
        pay_js.append(f'window.__PAYLOADS=window.__PAYLOADS||{{}};'
                      f'window.__PAYLOADS[{json.dumps(name)}]={blob};')

    shas = " · ".join(f"payload {n} sha256 {p['meta']['sha256']}"
                      for n, p in view["payloads"].items())
    stale_banner = staleness_banner(view, ages)

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light only">
<title>{html.escape(mast['title'])} — {date_str}</title>
<style>{page_css()}</style></head><body><div class="wrap">
<header class="masthead">
<div class="nameplate">
<div class="ear ear-l">{ear_left}</div>
<h1>{html.escape(mast['title'])}</h1>
<div class="ear ear-r">{ear_right}</div>
</div>
<div class="folio">DISPLAY-ONLY · OPERATIONS · not study evidence · no journal is read ·
no outcome is scored · rules are born only under G-7 on exploration-classic</div>
</header>
{stale_banner}<p class="dateline">lens {lens} · as-of bar newest {newest_s} · oldest {oldest_s} ·
{len(ages['stale'])} of {ages['n']} rows stale · roster {len(a0)} · posture canon v1 sha256 {canon_sha}</p>
<main>

<h2>{sec[0]} — where is business possible today</h2>
<p class="headline">{fp['headline']}</p>
<p class="deck">{fp['deck']}</p>
<div class="cols">{fp['lead']}</div>
<table class="board"><tr><th>asset</th><th>regime</th><th>dist</th><th>score</th>
<th>two lines in the sand</th><th>posture</th><th>why</th><th>as-of · age</th><th>heat</th><th>range</th></tr>
{''.join(board)}</table>
<p class="small muted">AS-OF · AGE is each row's own last {lens} bar and its age, measured
from the bar's open to the print time (a proof handed no print time measures it to its
own newest row); past A2-7's limit of {STALE_LENS_PERIODS} lens periods
({ages['limit_ms'] / 3_600_000:g}h) the row reads STALE, its Trap Card says so and its
R1 prices are HELD out of the Telegrams' paste block (OR-2 R-1).
heat = {html.escape(REGISTER['HEAT']['value'])} [VETO — proposed,
not ruled]. Both inputs print in the row so the sort is auditable. RANGE is the 4h macro
range from the Tide Tables below, printed LAST because it is display-only: it enters no
heat, no sort, no posture word and no card.</p>

<h2>{sec[1]} — Trap Cards, pre-framed if-thens</h2>
<div class="docket">{''.join(cards) or '<p class="muted">no admitted open window on the roster.</p>'}</div>

<h2>{sec[2]} — living 12/89 windows</h2>
<div class="watchgrid">{''.join(watch)}</div>
<h3>Spaghetti — anchored at each asset's last 89/316 tide flip</h3>
{svg_spaghetti(view)}

<h2>{sec[3]} — macro ranges, display-only</h2>
{tide_tables(view)}

<h2>{sec[4]} — R1 alert prices, paste-ready</h2>
<pre class="r1">{html.escape(r1)}</pre>{held_block(r1_held, ages, lens)}

<h2>{sec[5]} — overnight and the week, display-only</h2>
{market_page(date_str)}

<h2>{sec[6]} — the ORACLE GRID footer, the last {view['fired']['hours']}h of fired events</h2>
<table class="returns"><tr><th>lens</th><th>class</th><th>fired</th><th>toll ATR</th>
<th>GRID NET H20</th><th>GRID NET H100</th><th>assets</th></tr>{''.join(fired)}</table>
<p class="small muted">NET is the ORACLE GRID's own filed median-minus-toll for that
(lens, class) cell — panel-pooled over 5 assets, m=0, unranked. It is NOT an outcome
computed from these events; this organ records events and reads the grid. Toll is not
comparable across assets. H20 at 4h is infeasible by construction (0 bars) and prints —.</p>

<h2>{sec[7]} — display-only: the provenance, and the rows still open</h2>
<h3>Appendix — posture canon v1 · the rows still open</h3>
<p class="small muted">BR-1 Amendment A2 (operator, 2026-08-16) ruled the naming, the
trigger pair, the net R:R form and the schedule; the schedule was SUSPENDED by operator
ruling 2026-09-21 and the Oracle now prints on demand. {veto_note}</p>
<table class="veto"><tr><th>constant</th><th>disposition</th><th>value</th><th>why it is not law</th></tr>
{''.join(veto)}</table>

<footer>
DISPLAY-ONLY · operations · {date_str} · lens {lens} · as-of bar newest {newest_s} · oldest {oldest_s} ·
posture canon v1 sha256 {canon_sha} · {shas} ·
displacements are (EMA−price)/ATR · analytics {ANALYTICS_VERSION} sha {analytics_sha()} ·
net R:R = {html.escape(REGISTER['NET_RR_FORM']['value'])}, toll from the ORACLE GRID
(census-2B, oracle_grid.parquet) — no cost-free number prints on this page.<br>
{printed}<br>
CERTIFIED: {html.escape(' · '.join(CERTIFIED))}.<br>
NOT CERTIFIED: {html.escape(' · '.join(NOT_CERTIFIED))}.<br>
No claim is made or implied. Nothing here is scored. Promotion requires registration
under G-7 on exploration-classic.
</footer>
</main></div>
<script>{''.join(pay_js)}</script>
<script>{MANTLE_JS}</script>
</body></html>"""


# ═══════════════════════════════════════════ A2-7 · THE STALENESS BANNER
# BR-1 Amendment A2-7 (operator, 2026-08-16), a PARTIAL remedy for finding T-3:
# launchd runs a missed calendar job on wake, so a laptop asleep at 06:45 can
# fetch AFTER the 07:00 Oracle has already rendered, and the brief would be a
# day stale with nothing to say so. This banner says so. It is display-only and
# [VETO-by-firing]: the threshold earns its keep the first time it fires.
#
# It does NOT close T-3. The wake-order race — should the Oracle refuse to
# render at all on a stale cache? — is still an open ruling.
STALE_LENS_PERIODS = 2

LENS_MS = {"5m": 300_000, "15m": 900_000, "30m": 1_800_000,
           "1h": 3_600_000, "4h": 14_400_000, "12h": 43_200_000}


# OR-2 R-1 · PER-ROW STALENESS (operator, 2026-09-22). A2-7's rule applied to EVERY row
# at its own as-of bar, where it was applied to the hottest asset's bar alone (OR-1
# finding OR1-a: with one symbol's tape cut back 3 days, the page printed that row's
# Trap Card and R1 alert prices from an 84-hour-old bar with no mark, and the band
# stayed silent). The limit is A2-7's own — STALE_LENS_PERIODS x LENS_MS[lens], read at
# call time, never retyped — and a row's age is measured from its bar's OPEN, as A2-7
# measures it. The instant rows are aged against is the PRINT TIME run() hands the
# render; a render handed none (a PROOF: the fixtures, the wrapper's self-check
# re-render) ages them against its own NEWEST row and reads no clock at all, so two
# renders of one view are byte-identical (F-BR-6, F-MV-8).

def row_as_of_ms(a: dict) -> int:
    """A row's as-of bar: the open time (ms UTC) of its last cached bar on the lens."""
    return int(a["station"].as_of_ms)


def row_ages(view: dict, printed_at: datetime | None = None) -> dict:
    """Every row's age and STALE verdict at one instant. Pure: never writes the view."""
    step = LENS_MS[view["lens"]]
    limit = STALE_LENS_PERIODS * step
    bars = {a["symbol"]: row_as_of_ms(a) for a in view["assets"]}
    newest = max(bars.values()) if bars else 0
    oldest = min(bars.values()) if bars else 0
    at = newest if printed_at is None else int(printed_at.timestamp() * 1000)
    rows = {}
    for sym, t in bars.items():
        age = at - t
        rows[sym] = {"as_of_ms": t, "age_ms": age, "age_bars": age // step,
                     "age_h": age / 3_600_000, "stale": age > limit}
    return {"at_ms": at, "timed": printed_at is not None, "limit_ms": limit,
            "rows": rows, "newest_ms": newest, "oldest_ms": oldest,
            "stale": [sym for sym, r in rows.items() if r["stale"]], "n": len(rows)}


def as_of_stamp(ms: int) -> str:
    """An as-of bar in the dateline's own format."""
    return datetime.fromtimestamp(int(ms) / 1000, timezone.utc).strftime(AS_OF_FMT)


def _age_words(r: dict) -> str:
    n = r["age_bars"]
    return f"{n} bar{'' if n == 1 else 's'} · {r['age_h']:.1f}h"


def age_cell(r: dict) -> str:
    """The Board's AS-OF · AGE cell: the row's own bar, its age, and STALE past A2-7."""
    chip = "<span class='chip stale'>STALE</span> " if r["stale"] else ""
    return (f"<td class='num asof'>{chip}{as_of_stamp(r['as_of_ms'])}<br>"
            f"<span class='muted small'>{_age_words(r)}</span></td>")


def age_chip(r: dict) -> str:
    """The Docket card header's mark: nothing on a fresh row."""
    if not r["stale"]:
        return ""
    return (f'<span class="chip stale">STALE</span> '
            f'<span class="muted small">bar {as_of_stamp(r["as_of_ms"])} · {_age_words(r)}</span>')


def r1_split(view: dict, stale) -> tuple[str, str]:
    """The Telegrams' two blocks, cut from ONE r1_block(view): the paste-ready lines of
    the fresh rows, and the HELD lines of the stale ones. A line is only ROUTED, never
    re-typed, so a fresh row's prices are byte-identical to r1_block's."""
    held_syms = set(stale)
    paste, held = [], []
    for ln in r1_block(view).split("\n"):
        if ln:
            (held if ln.split(" ", 1)[0] in held_syms else paste).append(ln)
    return "\n".join(paste), "\n".join(held)


def held_block(held: str, ages: dict, lens: str) -> str:
    """R-1 · a stale row's R1 lines LEAVE the paste-ready block and print beneath it,
    struck through, for reference only. The strike is for the eye; the exclusion is what
    protects the operator, because formatting dies on copy-paste and exclusion does not."""
    if not held:
        return ""
    lines = "\n".join(f"<s>{html.escape(ln)}</s>" for ln in held.split("\n"))
    names = _names([s for s in ages["stale"]])
    empty = ("The paste-ready block above is EMPTY: no row is on a fresh wire. "
             if len(ages["stale"]) == ages["n"] else "")
    return (f'\n<h3>HELD — stale wire</h3>\n<p class="small muted">{empty}Reference only, NOT '
            f'paste-ready: the last {lens} bar of {html.escape(names)} is older than A2-7\'s '
            f'{ages["limit_ms"] / 3_600_000:g}h limit, so these prices are left OUT of the block '
            f'above. Struck through here for the eye; copying would strip the strike, so they '
            f'are not in the block at all.</p>\n<pre class="held">{lines}</pre>')


def staleness_banner(view: dict, ages: dict | None = None) -> str:
    """A2-7, per row since OR-2 R-1. Fires when ANY row's as-of bar is older than
    STALE_LENS_PERIODS lens periods at the print time (row_ages) and names how many,
    and the oldest bar. The as-of stamps print regardless — the band adds an alarm, it
    never replaces the provenance."""
    ages = row_ages(view) if ages is None else ages
    if not ages["stale"]:
        return ""
    # OR-1 STEP F: the contract's opening words, then A2-7's own sentence, unchanged.
    # ONE <div class="stale"> WITH NO <div> INSIDE IT, on purpose: the movers fixture
    # cuts the band out of a page with a non-greedy `<div class="stale">.*?</div>`,
    # and a nested div would end that cut early.
    age_ms = ages["at_ms"] - ages["oldest_ms"]
    limit = ages["limit_ms"]
    head = REGISTER["LATE_EDITION"]["value"].format(
        n=len(ages["stale"]), r=ages["n"], as_of=as_of_stamp(ages["oldest_ms"]))
    return (f'<div class="stale"><b>{html.escape(head)}</b> The oldest {view["lens"]} bar is '
            f'{age_ms / 3_600_000:.1f}h old, over the {STALE_LENS_PERIODS}-lens-period '
            f'limit of {limit / 3_600_000:.1f}h. The top-up may not have run. Those rows read '
            f'STALE on the Board and The Docket and their R1 prices are HELD out of the '
            f'paste-ready block; every row is computed from its own bar and names it.</div>')


def r1_block(view: dict) -> str:
    """C-9 / F-BR-7. Prices only. Grammar: <SYMBOL> <TAG> <PRICE>, one per line.
    No prose, no advice, no ratio — a parser must be able to read every line."""
    out = []
    for a in view["assets"]:
        sym = a["symbol"]
        lis = a["lis"] if isinstance(a["lis"], dict) else {}
        for key, tag in (("above", "LIS_ABOVE"), ("below", "LIS_BELOW")):
            ln = lis.get(key)
            if ln and ln.get("mean") is not None:
                out.append(f"{sym} {tag} {float(ln['mean']):.10g}")
        c = a["card"]
        if c:
            if c["invalidation"] is not None:
                out.append(f"{sym} INVAL {float(c['invalidation']):.10g}")
            if c["target"] is not None:
                out.append(f"{sym} TARGET {float(c['target']):.10g}")
    return "\n".join(out)


# ═══════════════════════════════════════════════════════════ D-4 THE TAPE
# TC4'S EVENT TAPE, AND ITS SCHEMA IS UNTOUCHED. AMENDMENT A-OR1-1 clause v (operator,
# 2026-09-22), verbatim: "Range records go to a sibling tape,
# research_outputs/oracle/tape_ranges/; the TC4 event tape's schema is untouched
# (A-BR2-1b doctrine)." So TAPE_COLS is again EXACTLY the pre-OR-1 24 names in the
# pre-OR-1 order (`git show ee93644^:scripts/oracle_daily.py`), and write_tape is again
# exactly the pre-OR-1 function. From OR-1 STEP D2 (ee93644, 2026-09-21) until this
# amendment the list carried eight range_* columns APPENDED, and ONE tape was written
# that way: research_outputs/oracle/tape/oracle_tape_2026-09-21.parquet, 32 columns.
# It is REPORTED, never rewritten, never deleted: its first 24 columns are this schema,
# and a reader of the D-4 tape takes those. F-BR-14 goes red on a TAPE_COLS, or on a
# written D-4 tape, that is anything but these 24 names in this order.

TAPE_COLS = ["as_of_ms", "as_of_iso", "asset", "lens", "station", "tide",
             "tide_flip_ms", "direction", "arm_ms", "age_bars", "disp_atr",
             "d_ok", "trigger_ms", "trigger_on_arming_bar", "closed_by",
             "close_px", "atr_lens", "atr_daily", "n_levels", "n_clusters",
             "nearest_cluster_atr", "nearest_cluster_score", "heat",
             "payload_sha"]


def write_tape(view: dict, date_str: str) -> tuple[Path, str, int]:
    """C-10 / D-4. One event stream, two renders — HTML for the operator,
    parquet for TC4. RECORDING only: not one outcome column exists here.

    Since A-OR1-1 (2026-09-22) this is again, line for line, the pre-OR-1
    function: it reads no range. The range layer records to its own sibling
    tape, write_range_tape() below."""
    TAPE_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for a in view["assets"]:
        st = a["station"]
        base = {
            "as_of_ms": st.as_of_ms,
            "as_of_iso": datetime.fromtimestamp(st.as_of_ms / 1000, timezone.utc).isoformat(),
            "asset": a["symbol"], "lens": st.lens, "station": st.board_word,
            "tide": st.tide, "tide_flip_ms": st.tide_flip_ms,
            "close_px": st.close, "atr_lens": st.atr, "atr_daily": a["atr_d"],
            "n_levels": a["n_levels"], "n_clusters": len(a["clusters"]),
            "nearest_cluster_atr": a["nearest_d"],
            "nearest_cluster_score": (a["nearest"]["score"] if a["nearest"] else None),
            "heat": a["heat"], "payload_sha": a["payload_sha"],
        }
        wins = list(st.open_windows) + list(st.recent_dead)
        if not wins:
            rows.append({**base, "direction": None, "arm_ms": None, "age_bars": None,
                         "disp_atr": None, "d_ok": None, "trigger_ms": None,
                         "trigger_on_arming_bar": None, "closed_by": None})
        for w in wins:
            rows.append({**base, "station": w.station, "direction": w.direction,
                         "arm_ms": w.arm_ms, "age_bars": w.age_bars, "disp_atr": w.disp,
                         "d_ok": w.d_ok, "trigger_ms": w.trigger_ms,
                         "trigger_on_arming_bar": w.trigger_on_arming_bar,
                         "closed_by": w.closed_by or None})
    df = pd.DataFrame(rows, columns=TAPE_COLS)
    p = TAPE_DIR / f"oracle_tape_{date_str}.parquet"
    df.to_parquet(p, index=False)
    b = p.read_bytes()
    return p, hashlib.sha256(b).hexdigest(), len(b)


# ═══════════════════════════════════════ THE RANGE LAYER'S SIBLING TAPE (A-OR1-1 v)
# research_outputs/oracle/tape_ranges/oracle_tape_ranges_<date>.parquet (TAPE_RANGES_DIR):
# ONE ROW PER ROSTER SYMBOL per edition, in the D-4 tape's asset order. The D-4 tape's
# date, its overwrite-per-date semantics and its directory-creation behaviour, and run()
# writes it RIGHT AFTER the D-4 tape: after the render, in run()'s order, which F-BR-14
# leg (d) runs itself. A reader's in-place re-order would reach this record; F-BR-14's
# repr guard around the render is what catches it. RECORDING only: what the Tide Tables
# printed, per asset, at that asset's as-of bar. Nothing downstream may treat a column as
# a filter or a score without its own G-7 registration; no decision module may name it.
#
# THE ROW KEYS ARE THE D-4 TAPE'S OWN: as_of_ms, as_of_iso, asset, lens, built from the
# same station the D-4 rows are built from, so the two tapes join on (as_of_ms, asset,
# lens). `lens` is the D-4 tape's column — the station's lens; the range machine's own
# lens is REGISTER['RANGE_LENS'], which range_layer() enforces by measurement on that
# same frame.
# THE EIGHT FIELDS are the eight OR-1 STEP D appended to the D-4 tape, same names, same
# meaning, so the 2026-09-21 tape's range columns read as this tape's. Every name clears
# the banned-token matcher the wrapper's per-edition self-check runs over this list
# (F-BR-14 re-runs it; "edge" is banned, so nothing here is called that).
RANGE_TAPE_KEYS = ("as_of_ms", "as_of_iso", "asset", "lens")
RANGE_TAPE_COLS = [*RANGE_TAPE_KEYS,
                   "range_state", "range_top", "range_bottom", "range_pos_pct",
                   "range_dist_atr", "range_pending_side", "range_last_event",
                   "range_last_event_age_bars"]
# THE DTYPE PINS — the eight fields, partitioned: five float64, three string.
# float64 even on a day when no roster symbol holds a range: an all-None column would
# land in the parquet as a null-typed column and change dtype from one day to the next.
RANGE_TAPE_FLOATS = ("range_top", "range_bottom", "range_pos_pct", "range_dist_atr",
                     "range_last_event_age_bars")
# THE SAME HAZARD, STRING SIDE (review finding, 2026-09-21 — the two OBJECT columns
# were left out of the guard above). `range_pending_side` is None on every row of any
# day when no roster symbol holds a pending macro breach (today 1 of 18 holds one), and
# `range_last_event` is None on a day when none holds a range at all — the F-BR-14
# EMPTY stub is exactly that day. Plain object dtype lands those in the parquet as type
# `null`, and a multi-day read in DATE ORDER then raises before it returns a row:
# ArrowNotImplementedError: Unsupported cast from string to null using function
# cast_null — which kills pd.read_parquet(<tape dir>), pyarrow.dataset and
# pq.ParquetDataset, i.e. every normal read of the tape these columns exist to feed.
# pandas' nullable string dtype lands as `string` even when every value is NA, so
# the schema does not move from one day to the next. `range_state` is already always a
# string (snapshot and range_empty both return one) and is named here to PIN that.
RANGE_TAPE_STRINGS = ("range_state", "range_pending_side", "range_last_event")


def write_range_tape(view: dict, date_str: str) -> tuple[Path, str, int]:
    """A-OR1-1 v. The range layer's sibling tape: one row per roster symbol, keyed
    as the D-4 tape keys its rows, carrying the eight range fields with their
    dtypes PINNED (RANGE_TAPE_FLOATS / RANGE_TAPE_STRINGS). Overwrites the day's
    file and creates its directory, exactly as write_tape does. RECORDING only.

    One of the range object's permitted readers (F-BR-14's allow-list), and the
    ONLY function that may name TAPE_RANGES_DIR."""
    TAPE_RANGES_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for a in view["assets"]:
        st = a["station"]
        rg = a.get("range") or range_empty(error=RANGE_ABSENT)
        rows.append({
            "as_of_ms": st.as_of_ms,
            "as_of_iso": datetime.fromtimestamp(st.as_of_ms / 1000, timezone.utc).isoformat(),
            "asset": a["symbol"], "lens": st.lens,
            "range_state": rg.get("state"),
            "range_top": rg.get("top"), "range_bottom": rg.get("bottom"),
            "range_pos_pct": rg.get("pos_pct"), "range_dist_atr": rg.get("dist_atr"),
            "range_pending_side": (rg.get("pending") or {}).get("side"),
            "range_last_event": (rg.get("last_event") or {}).get("event"),
            "range_last_event_age_bars": (rg.get("last_event") or {}).get("age_bars"),
        })
    df = pd.DataFrame(rows, columns=RANGE_TAPE_COLS)
    for col in RANGE_TAPE_FLOATS:
        df[col] = df[col].astype("float64")
    for col in RANGE_TAPE_STRINGS:
        df[col] = df[col].astype("string")
    p = TAPE_RANGES_DIR / f"oracle_tape_ranges_{date_str}.parquet"
    df.to_parquet(p, index=False)
    b = p.read_bytes()
    return p, hashlib.sha256(b).hexdigest(), len(b)


# ═══════════════════════════════════════════════ D-7 THE CALIBRATION LOGGER
# A1-4, verbatim: "display-machinery distribution stats ONLY (per-asset level
# counts, cluster widths, collapse events, LIS distances, maturity-withheld
# fractions, window ages). NO outcome fields, NO signal-performance fields —
# enforced by fixture F-BR-10."
#
# THE BANNED VOCABULARY IS DECLARED HERE, IN CODE, so F-BR-10 scans a list and
# not a mood. If a future edit adds an outcome column, the fixture fails.

BANNED_CALIBRATION_KEYS = (
    "win", "loss", "pnl", "r_multiple", "net_r", "gross_r", "return", "outcome",
    "hit_rate", "expectancy", "profit", "equity", "mfe", "mae", "term_h20",
    "term_h100", "sharpe", "edge", "score_of_signal", "accuracy", "precision",
)

# ─────────────────────────────────────── C-0, AND WHY THIS BLOCK EXISTS
# FINDING C-0 (ORACLE_CHAIN_CLOSE_2026-08-16 §C-0, reported-not-fixed; closed
# by queue OR-1 STEP B, 2026-09-21). A1-4 lists "maturity-withheld fractions"
# among the things D-7 logs, and BR-2 WORK(1) recalibrates "family cap 3 ·
# maturity floors 16/60 · target buckets" FROM these files. For five weeks the
# logger wrote the LITERAL 0.0 for maturity on every asset on every run, and
# wrote nothing at all for the other two. A recalibration run on those files
# would have "measured" a constant the code typed and found it perfectly stable.
#
# So the three families are now MEASURED, each by its own small function below,
# and write_calibration only assembles them. The rule that keeps this honest:
# a family that could not be measured records None, NEVER 0.0 — an uncountable
# sample is not evidence of a clean one (the analytics.vwap.maturity() rule for
# `bars is None`, applied one level up).
#
# MEASURING IS NOT WITHHOLDING. Nothing here changes which levels enter the
# registry, any score, heat, station or card. On 7d/30d windows over 1h bars
# the windows hold ~168/~720 bars against floors of 16/60, so the measured
# fraction is EXPECTED to be a true 0.0 on a healthy cache; the per-window bar
# counts are logged beside it as the evidence that it was counted, not typed.
#
# THE CALIBRATION CLOCK RESTARTS HERE. Every calibration JSON written before
# this change is HOLLOW for these three families and is EXCLUDED from any
# recalibration. They are told apart by content, not by file date: a measured
# document carries `schema_version` >= CAL_SCHEMA_VERSION; a hollow one carries
# no `schema_version` at all.
CAL_SCHEMA_VERSION = 2

# The two target-bucket names this logger adds to brief_render's NEAR/MID/FAR.
# They are different facts and are counted apart: an asset with no open admitted
# window has NO CARD; a card that exists but names no target (NOT TAKEN, or no
# scored cluster on the trade's side) has NO TARGET.
BUCKET_NO_CARD = "NONE"
BUCKET_NO_TARGET = "NO_TARGET"
ATR_BASES = ("lens", "daily")


def maturity_withheld(vwap_maturity) -> dict:
    """What the 16/60 floors WOULD withhold from the VWAP family — counted.

    The brief2 `_admit` precedent: the LINE is withheld when `line_ok` is
    False, and each BAND when `band_ok` is False. Candidates are the finite
    lines and bands level_registry actually offered. `fraction` is None when
    nothing was measured (no record, or no candidate) — never a typed 0.0.
    """
    cand = held = 0
    for w in vwap_maturity or []:
        cand += w["line_candidates"] + w["band_candidates"]
        held += ((0 if w["line_ok"] else w["line_candidates"])
                 + (0 if w["band_ok"] else w["band_candidates"]))
    return {"candidates": cand, "withheld": held,
            "fraction": (round(held / cand, 6) if cand else None)}


def family_cap_binding(clusters) -> dict:
    """How often analytics.levels.FAMILY_CAP touches a cluster — two tests.

    `at_cap`   some family has >= FAMILY_CAP members: the cap is REACHED. This
               is the brief_calibration_c4.py precedent ("BINDS on n of N").
    `over_cap` some family has >  FAMILY_CAP members: the cap actually REDUCED
               the score (levels.score() takes min(count, FAMILY_CAP)).
    The two differ exactly when a family sits on the cap, so both are logged and
    BR-2 chooses. `at_cap` includes every `over_cap` cluster. The cap is read
    from analytics.levels — the 3 is never copied here.
    """
    at = over = 0
    for c in clusters:
        per: dict[str, int] = {}
        for m in c["members"]:
            per[m["family"]] = per.get(m["family"], 0) + 1
        top = max(per.values()) if per else 0
        at += int(top >= L.FAMILY_CAP)
        over += int(top > L.FAMILY_CAP)
    return {"clusters": len(clusters), "at_cap": at, "over_cap": over}


def card_target_bucket(a: dict) -> dict:
    """Which brief_render.TARGET_BUCKETS bucket the open Trap Card's target is in.

    distance = card['reward'] (= |target - entry|) over an ATR. 'lens' is the
    ATR the card itself prices its toll in (trap_card: atr_l = st.atr — F-BR-13
    re-derives toll_price from it so a change there cannot pass silently);
    'daily' is the ATR the BRIEF-2 lane measured its buckets in. Both are
    recorded; REGISTER['TARGET_BUCKET_ATR'] [VETO] picks the headline.
    """
    card = a.get("card")
    atrs = {"lens": a["station"].atr, "daily": a["atr_d"]}
    dist: dict[str, float | None] = {}
    bucket: dict[str, str] = {}
    for basis in ATR_BASES:
        atr = atrs[basis]
        reward = card.get("reward") if card else None
        d = (float(reward) / float(atr)
             if reward is not None and atr and np.isfinite(atr) and atr > 0 else None)
        dist[basis] = round(d, 6) if d is not None and np.isfinite(d) else None
        bucket[basis] = (BUCKET_NO_CARD if not card
                         else BUCKET_NO_TARGET if dist[basis] is None
                         else target_bucket(dist[basis]))
    return {"distance_atr": dist, "bucket": bucket}


def _occupancy(names) -> dict:
    """Roster-wide counts, every bucket printed even at zero so a week of files
    lines up column for column."""
    order = [n for n, _lo, _hi in TARGET_BUCKETS] + [BUCKET_NO_TARGET, BUCKET_NO_CARD]
    names = list(names)
    return {n: sum(1 for x in names if x == n) for n in order}



def write_calibration(view: dict, date_str: str, slot: str) -> tuple[Path, str, int]:
    CAL_DIR.mkdir(parents=True, exist_ok=True)
    basis = REGISTER["TARGET_BUCKET_ATR"]["value"]
    per_asset = []
    for a in view["assets"]:
        st = a["station"]
        widths = [ (max(m["level"] for m in c["members"]) -
                    min(m["level"] for m in c["members"])) / a["atr_d"]
                   for c in a["clusters"] if c["member_count"] > 1 ]
        lis = a["lis"] if isinstance(a["lis"], dict) else {}
        mw = maturity_withheld(a.get("vwap_maturity"))
        cap = family_cap_binding(a["clusters"])
        tb = card_target_bucket(a)
        per_asset.append({
            "asset": a["symbol"],
            "level_count": a["n_levels"],
            "cluster_count": len(a["clusters"]),
            "collapse_events": a["n_levels"] - sum(c["member_count"] for c in a["clusters"]),
            "cluster_width_atr_p50": (round(float(np.median(widths)), 6) if widths else None),
            "cluster_width_atr_max": (round(float(np.max(widths)), 6) if widths else None),
            "lis_distance_atr": {k: (round(abs(lis[k]["mean"] - a["price"]) / a["atr_d"], 6)
                                     if lis.get(k) and lis[k].get("mean") is not None else None)
                                 for k in ("above", "below")},
            # REPAIRED 2026-08-21, two defects on one line, both found by the
            # T-3 diagnostic. (1) `lines_in_sand` writes None on a side with no
            # qualifying cluster (levels.py `out[side] = None`), so the key is
            # PRESENT holding None and `.get(k, {})` never reaches its default —
            # `.get("fallback")` on None raised AttributeError and killed every
            # scheduled run from 2026-08-20T10:00Z. The line directly above already
            # guarded this way; this one did not. (2) the flag was read from a
            # "fallback" key that `lines_in_sand` never writes — it marks the
            # fallback with source="fallback" — so this field recorded False for
            # every asset on every side since 2026-08-16 and could not have said
            # otherwise. None here means NO LINE on that side, matching the None
            # convention `lis_distance_atr` above already uses.
            "lis_fallback_used": {k: (None if not lis.get(k)
                                      else lis[k].get("source") == "fallback")
                                  for k in ("above", "below")},
            # C-0 (closed OR-1 STEP B): MEASURED. This line read the literal
            # 0.0 from 2026-08-16 to 2026-09-21. F-BR-13 fails the build if a
            # numeric literal is ever assigned to this key again.
            "maturity_withheld_fraction": mw["fraction"],
            "maturity_candidate_levels": mw["candidates"],
            "maturity_withheld_levels": mw["withheld"],
            "maturity_windows": [{"window_d": w["window_d"], "bars": w["bars"],
                                  "line_ok": w["line_ok"], "band_ok": w["band_ok"]}
                                 for w in (a.get("vwap_maturity") or [])],
            "family_cap_binding": cap,
            "target_bucket": tb["bucket"][basis],
            "target_bucket_by_atr": tb["bucket"],
            "target_distance_atr": tb["distance_atr"],
            "open_window_ages_bars": [w.age_bars for w in st.open_windows],
            "open_window_disp_atr": [round(w.disp, 6) for w in st.open_windows],
            "station": st.board_word,
            "nearest_cluster_atr": (round(a["nearest_d"], 6)
                                    if np.isfinite(a["nearest_d"]) else None),
            "heat": round(a["heat"], 6),
        })
    cand = sum(r["maturity_candidate_levels"] for r in per_asset)
    held = sum(r["maturity_withheld_levels"] for r in per_asset)
    doc = {
        "class": "DISPLAY-MACHINERY DISTRIBUTIONS ONLY — no outcome fields, no "
                 "signal-performance fields (BR-1 Amendment A1-4, enforced by F-BR-10)",
        "schema_version": CAL_SCHEMA_VERSION,
        "schema_note": "C-0 closed at OR-1 STEP B (2026-09-21): maturity, family-cap "
                       "binding and target buckets are MEASURED. A calibration JSON "
                       "with no schema_version is hollow for those three families "
                       "and is excluded from recalibration.",
        "date": date_str, "slot": slot, "lens": view["lens"],
        "as_of_ms": view["as_of_ms"],
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "posture_canon_sha256": PE.canon_sha(),
        "thresholds_in_force": {
            "collapse_atr": L.COLLAPSE_ATR, "cluster_atr": L.CLUSTER_ATR,
            "lis_atr": L.LIS_ATR, "family_cap": L.FAMILY_CAP,
            "maturity_line_min": VW.LINE_MIN_BARS, "maturity_band_min": VW.BAND_MIN_BARS,
            "vwap_windows_d": list(REGISTER["VWAP_WINDOWS_D"]["value"]),
            # [lo, hi) in ATR; the open top of FAR is null — JSON has no infinity
            "target_buckets_atr": {n: [lo, (None if np.isinf(hi) else hi)]
                                   for n, lo, hi in TARGET_BUCKETS},
            "target_bucket_atr_basis": basis,
            "d_displacement": PE.REGISTER["D_DISPLACEMENT"]["value"],
            "dead_memory_bars": PE.REGISTER["DEAD_MEMORY_BARS"]["value"],
        },
        "veto_rows_awaiting_ruling": (
            [k for k, v in PE.REGISTER.items() if not v["ruled"]]
            + [k for k, v in REGISTER.items() if not v["ruled"]]
            + [f"CANON.{k}" for k, v in PE.CANON.items() if not v["ruled"]]),
        "station_distribution": {w: sum(1 for a in view["assets"]
                                        if a["station"].board_word == w)
                                 for w in PE.STATION_WORDS},
        "fired_event_cells": len(view["fired"]["rows"]),
        # the three C-0 families, whole roster — sums of the per-asset records
        "maturity_roster": {"candidate_levels": cand, "withheld_levels": held,
                            "withheld_fraction": (round(held / cand, 6) if cand else None)},
        "family_cap_binding": {k: sum(r["family_cap_binding"][k] for r in per_asset)
                               for k in ("clusters", "at_cap", "over_cap")},
        "target_bucket_occupancy": _occupancy(r["target_bucket"] for r in per_asset),
        "target_bucket_occupancy_by_atr": {
            b: _occupancy(r["target_bucket_by_atr"][b] for r in per_asset)
            for b in ATR_BASES},
        "per_asset": per_asset,
    }
    p = CAL_DIR / f"oracle_calibration_{date_str}_{slot}.json"
    b = json.dumps(doc, indent=1, sort_keys=True).encode("utf-8")
    p.write_bytes(b)
    return p, hashlib.sha256(b).hexdigest(), len(b)


# ═══════════════════════════════════════════════════════════════════ MAIN

def run(slot: str = "full", as_of_ms: int | None = None, log=print) -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PAYLOAD_DIR.mkdir(parents=True, exist_ok=True)
    now_ba = datetime.now(tz=None).astimezone()
    date_str = now_ba.strftime("%Y-%m-%d")

    log(f"ORACLE {slot} · {date_str} · lens {REGISTER['LENS']['value']}")
    canon_p, canon_sha, canon_b = PE.write_canon_json()
    log(f"  posture_canon.json {canon_b} B sha256 {canon_sha}")

    view = build_view(as_of_ms=as_of_ms, log=log)

    for name, pl in view["payloads"].items():
        (PAYLOAD_DIR / name).write_bytes(
            json.dumps(pl, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))

    # OR-1 STEP F: the masthead's number and the edition's name. Counted HERE, not in
    # render_html, which stays a function of what it is handed: a fixture that points
    # TAPE_DIR somewhere else between two renders must get the same page twice.
    # A-OR1-1 vii: the PRINT TIME is `now_ba` above, taken ONCE — the same instant the
    # date comes from — and handed to render_html, which never reads the clock for it;
    # edition_name reads its hour on the Buenos Aires wall clock, whatever the machine's
    # zone. date_str is derived exactly as before (no semantics move).
    edition_no = edition_count(date_str)
    log(f"  edition {REGISTER['MASTHEAD']['value']['volume']} · No. {edition_no} · "
        f"{edition_name(slot, now_ba)}")
    doc = render_html(view, date_str, canon_sha, edition_no=edition_no, slot=slot,
                      printed_at=now_ba)
    out = OUT_DIR / f"oracle_{date_str}.html"
    out.write_text(doc, encoding="utf-8")
    sha = hashlib.sha256(out.read_bytes()).hexdigest()
    log(f"  {out} {out.stat().st_size:,} B sha256 {sha}")

    tape_p, tape_sha, tape_b = write_tape(view, date_str)
    log(f"  {tape_p} {tape_b:,} B sha256 {tape_sha}")
    # A-OR1-1 v: the range layer's sibling tape, beside the D-4 tape and after the
    # render, like it. The D-4 tape above carries no range column.
    rtape_p, rtape_sha, rtape_b = write_range_tape(view, date_str)
    log(f"  {rtape_p} {rtape_b:,} B sha256 {rtape_sha}")
    cal_p, cal_sha, cal_b = write_calibration(view, date_str, slot)
    log(f"  {cal_p} {cal_b:,} B sha256 {cal_sha}")

    return {"html": out, "html_sha": sha, "html_bytes": out.stat().st_size,
            "tape": tape_p, "tape_sha": tape_sha,
            "tape_ranges": rtape_p, "tape_ranges_sha": rtape_sha,
            "calibration": cal_p, "calibration_sha": cal_sha,
            "canon": canon_p, "canon_sha": canon_sha, "view": view}


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    slot = "full"
    if "--slot" in argv:
        slot = argv[argv.index("--slot") + 1]
    run(slot=slot)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
