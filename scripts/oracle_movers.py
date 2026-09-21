"""THE MOVERS ORGAN — STEP E (fetch half) of queue OR-1 "THE DAILY ORACLE".
Fetch-and-write-one-json, and nothing else.

OR-1 STEP E, verbatim:

    MARKET PAGE: scripts/oracle_movers.py, FETCH-ONLY, its own organ: universe
    from exchangeInfo (PERPETUAL·TRADING·USDT quote; count printed, never
    asserted); overnight = Binance /fapi/v1/ticker/24hr priceChangePercent
    [VETO]; weekly = close_now / close of the 1d bar 7 back − 1 from 1d klines
    limit=8 [VETO]; write research_outputs/oracle/movers/movers_<date>.json
    (off-bus). NEVER writes the kline cache (fixture F-MV-1: cache dir
    sha-identical before/after; F-MV-2: firewall scan; F-MV-3: universe count
    ≥ 150 and enumerated). oracle_daily reads the json only (cache-only stays
    true). [...] if the fetch failed, the page prints "WIRE DOWN — no movers
    this edition", never stale numbers.

════════════════════════════════════════════════════════════════════════════
WHY THIS IS ITS OWN PROCESS. The Oracle is CACHE-ONLY BY DESIGN (BR-1b: "it
may never fetch inside a firewalled run"), and operator ruling 7 of 2026-09-21
asks for a list that cannot be built from the cache: the top 50 of ~530
contracts, of which the cache holds a roster of about twenty. So the fetching
lives here, in a separate organ that the Oracle never imports. The ONLY thing
that crosses the wall is one json file, read by path. Same shape as the top-up
(BR-1b), one step further out: the top-up may write the kline cache; this organ
may not even name it.

CLASS: DISPLAY-ONLY. Live data is operations-only and forbidden as study
evidence (BR-1 §2 clause 1). OR-1 extends the wall: NO gate, filter, heat,
station, card or sizing computation may read a range or a mover. A mover is a
line on the Market Page and a row in this json. It is never an input.

════════════════════════════════════════════════════════════════════════════
THE READER'S CONTRACT (for the render half, which is another step's work).

    A reader may print numbers ONLY from a document whose `status` is "OK" AND
    whose `date` is the edition's own date. Anything else is WIRE DOWN.

This organ makes that rule hard to get wrong from the writing side:
  · THE PLACEHOLDER COMES FIRST. Before the first byte goes over the wire,
    main() writes today's file as status "FAIL", `in_flight` true, EMPTY tables.
    So the day's earlier success is given up the moment a newer fetch STARTS,
    and a run that does not live to see its own failure — SIGKILL by the
    wrapper's timeout, Ctrl-C, a power cut — still leaves a document no reader
    can print. (The FIRST BUILD of this organ wrote only at the END of main(); the
    verifier killed a run mid-sweep and the earlier success was still on disk,
    status OK, dated today. F-MV-6 now does that kill on every suite run.)
  · a fetch that FAILS and lives to say so replaces the placeholder with its own
    FAIL document — `in_flight` false, EMPTY tables, the reasons and the
    per-symbol errors kept — so a careless reader of a FAIL document finds no
    numbers to print; an interrupt (KeyboardInterrupt, SystemExit) does the
    same and is then re-raised;
  · A DEAD WIRE IS NOTICED EARLY. The weekly sweep stops taking symbols the
    moment enough fetches have failed that WEEKLY_SUCCESS_FLOOR can no longer be
    reached (27 of 528), and the whole run gives up waiting at RUN_DEADLINE_S —
    so FAIL is written in about a minute, not the quarter-hour that ~530
    four-attempt backoffs take, and well inside the wrapper's own timeout;
  · every write is atomic (tmp + os.replace), so a reader never sees half a file;
  · every symbol of the universe is ACCOUNTED FOR in each table of an OK
    document: it is either a row, or it is listed in `overnight_null` /
    `weekly_null` with a reason. Nothing is guessed, nothing is silently dropped.

What is NOT claimed: while a fetch is in flight (~30 s) today's file says FAIL
even if the wire is fine — a reader in that window prints WIRE DOWN, which is
true of what it can know. The wrapper runs the organ and the Oracle in sequence,
so an edition never reads inside that window.

THE DOCUMENT (json, sort_keys, one file per machine-local date — the date the
run STARTED on). EVERY document — OK, FAIL or placeholder — carries EVERY key
below (DOC_KEYS; F-MV-3 and F-MV-5 compare the key sets), so the render half
never has to import this module to learn the shape and never meets a KeyError
on a FAIL document. What a stage never reached is null, 0 or an empty list:

    class · date · date_basis · fetched_utc · fetched_local · status ·
    in_flight · fail_reasons[] · universe_count · universe[] (every symbol,
    sorted) · exchange_symbols_total · excluded_counts[{class_tag, count}] ·
    ticker_rows_total · ticker_quietest_symbol · ticker_quietest_age_seconds ·
    top_n · overnight[] · overnight_top[] · overnight_null[] ·
    weekly[] · weekly_top[] · weekly_null[] ·
    weekly_fetch{attempted, succeeded, failed, not_fetched, fraction, floor,
    stopped_early} · errors[] · method{} · endpoints{} · register{} (this file's
    REGISTER, so the [VETO] rows can be surfaced from the json) ·
    organ{path, sha256} · used_weight_1m_peak · weight_brakes_taken ·
    runtime_seconds

    a table row  = {symbol, pct, last_price}   pct is PERCENT, signed
    a null       = {symbol, reason}
    an error     = {symbol | null, stage, error}
    *_top        = the first top_n rows of the same table, already in print order

The number is called `pct` everywhere. No key in this document carries an
outcome word (F-MV-4 scans them with F-BR-10's matcher).

WHAT THIS MODULE NEVER DOES: it never writes (or names) the kline cache, never
imports the Oracle, the posture engine, the top-up, analytics, a journal or the
trading module, never aggregates anything, never publishes, never writes under
the bus, and writes exactly one path: MOVERS_DIR (at most three times a run —
the placeholder, the result, and an interrupt's FAIL — always today's one file,
always inside write_doc()). The F-MV suite (scripts/oracle_movers_fixtures.py)
scans this file's AST for all of that.

Run:      ~/venvs/naiad/bin/python scripts/oracle_movers.py
Dry run:  ~/venvs/naiad/bin/python scripts/oracle_movers.py --dry-run
Exit:     0 if the document written is status OK; 1 otherwise. An interrupt
          (Ctrl-C) writes its FAIL document and is then re-raised, so the
          shell sees the signal and not a tidy 1.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import queue
import sys
import threading
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

# The HTTP layer is the estate's own: requests.get, timeout 60 s, 4 attempts,
# linear backoff 1.5/3/4.5/6 s (as read 2026-09-21; engine/data.py is not this
# step's file). It returns the Response on 200 AND on 404, so every caller below
# checks the status itself. ONE CALL ON A DEAD WIRE THEREFORE COSTS 15 s when
# the connection is refused at once and up to 255 s when it hangs to the 60 s
# timeout — the arithmetic behind floor_unreachable() and RUN_DEADLINE_S below.
# NOTHING ELSE is imported from engine.data — in particular not the cache
# helpers (F-MV-1 scans for them).
from engine.data import _get, REST_BASE                       # noqa: E402

# THE ONE WRITE PATH. Gitignored by `.gitignore` `research_outputs/oracle/**`
# and therefore OFF-BUS: the json is pointed at by path + sha256, never carried
# (CONVENTIONS §4.2 pointer discipline). F-MV-2 asserts that the file's path
# literals are of exactly three kinds — this directory, the three /fapi/
# endpoints, and the organ's own name (ORGAN_REL, READ for its sha) — and that
# every write-capable call sits inside write_doc().
MOVERS_REL = "research_outputs/oracle/movers"
MOVERS_DIR = ROOT / MOVERS_REL
ORGAN_REL = "scripts/oracle_movers.py"

EP_EXCHANGE_INFO = "/fapi/v1/exchangeInfo"
EP_TICKER_24H = "/fapi/v1/ticker/24hr"
EP_KLINES = "/fapi/v1/klines"

DAY_MS = 86_400_000

# ═══════════════════════════════════════════════════════ THE CLOSED REGISTER
# Same law as oracle_daily / oracle_topup / posture_engine: nothing invented
# without saying so. 'ruled': False rows are [VETO] — operator defaults by
# ruling 6 of 2026-09-21 ("6-defaults"), standing until the operator vetoes
# them. The whole REGISTER is copied into every json this organ writes, so the
# render can surface the unruled rows WITHOUT importing a module that fetches.

TOP_N = 50
WEEKLY_BARS = 8                       # klines limit; index 0 is WEEKLY_SPAN_DAYS back
WEEKLY_SPAN_DAYS = WEEKLY_BARS - 1    # derived, never typed twice
WEEKLY_SUCCESS_FLOOR = 0.95
KLINE_WORKERS = 8
WEIGHT_SOFT_CAP = 1200
WEIGHT_BRAKE_S = 5.0
RUN_DEADLINE_S = 420.0
SWEEP_POLL_S = 0.5                    # how often the waiting main thread looks up;
                                      # plumbing, not a definition — no REGISTER row

_VETO = "OPERATOR — OR-1 [VETO] default (ruling 6 of 2026-09-21: 'defaults')"

REGISTER: dict[str, dict] = {
    "TOP_N": {
        "value": TOP_N,
        "ruled": True,
        "source": "OR-1 ratification line, operator ruling 7 (2026-09-21), verbatim: "
                  "'7-add a list at the end of the oracle with the top 50 coins by "
                  "%change overnight and weekly'. Contract STEP E: 'Render two tables, "
                  "top 50 by signed % change each'. SIGNED, descending: the top of each "
                  "table is the largest gain, not the largest absolute move.",
    },
    "UNIVERSE_FILTER": {
        "value": {"contractType": "PERPETUAL", "status": "TRADING", "quoteAsset": "USDT"},
        "ruled": True,
        "source": "OR-1 STEP E verbatim: 'universe from exchangeInfo "
                  "(PERPETUAL·TRADING·USDT quote; count printed, never asserted)'. Read "
                  "LITERALLY: contractType must EQUAL 'PERPETUAL', so Binance's separate "
                  "contractType 'TRADIFI_PERPETUAL' (stock/commodity perps, 198 TRADING "
                  "USDT symbols when this was written) is OUTSIDE the universe, as are "
                  "SETTLING and PENDING_TRADING symbols and the USDC/USD1/BTC quotes. The "
                  "count of what was excluded is recorded in every json.",
    },
    "OVERNIGHT_DEFINITION": {
        "value": "/fapi/v1/ticker/24hr priceChangePercent — ONE call, all symbols",
        "ruled": False,
        "deferred_to": _VETO,
        "source": "OR-1 STEP E: 'overnight = Binance /fapi/v1/ticker/24hr "
                  "priceChangePercent [VETO]'. UNRULED. Said plainly: this is a ROLLING "
                  "24 hours ending at the fetch, as the exchange computes it — not a "
                  "session-anchored 'overnight' and not a calendar day. The column is "
                  "called OVERNIGHT because the ruling calls it that.",
    },
    "WEEKLY_DEFINITION": {
        "value": f"(close_now / close of the 1d bar {WEEKLY_SPAN_DAYS} back - 1) x 100, "
                 f"1d klines limit={WEEKLY_BARS}",
        "ruled": False,
        "deferred_to": _VETO,
        "source": "OR-1 STEP E: 'weekly = close_now / close of the 1d bar 7 back − 1 from "
                  "1d klines limit=8 [VETO]'. UNRULED. "
                  f"Of the {WEEKLY_BARS} bars returned, index 0 is "
                  f"'{WEEKLY_SPAN_DAYS} back' and the last bar is the FORMING UTC day, "
                  "whose close is close_now. A symbol with fewer than "
                  f"{WEEKLY_BARS} daily bars, a hole in them, or a "
                  "last bar that is not the current UTC day gets weekly NULL and is "
                  "LISTED with its reason — never guessed, never back-filled from a "
                  "shorter span.",
    },
    "WEEKLY_BARS": {
        "value": WEEKLY_BARS,
        "ruled": False,
        "deferred_to": _VETO,
        "source": "The number inside WEEKLY_DEFINITION, as its own row so that the "
                  "definition's prose, the klines `limit`, the contiguity test and the "
                  "json's method string are all DERIVED from one constant and cannot "
                  "drift apart (verifier finding on the first build: the 8 was typed in four "
                  "places). OR-1 STEP E says 'limit=8 [VETO]'; UNRULED with the "
                  "definition it belongs to.",
    },
    "WEEKLY_SUCCESS_FLOOR": {
        "value": WEEKLY_SUCCESS_FLOOR,
        "ruled": False,
        "deferred_to": _VETO,
        "source": "PROPOSED by the OR-1 build 2026-09-21 — UNRULED [VETO]. The run is "
                  "status OK only if exchangeInfo AND the 24hr ticker succeeded AND at "
                  "least this fraction of the per-symbol weekly fetches came back HTTP "
                  "200 with a parseable body. A symbol too young for a weekly number is a "
                  "SUCCESSFUL fetch with a null result, not a failure. Below the floor the "
                  "weekly table would be a top-50 of whatever happened to answer, which "
                  "is not the table the ruling asked for — so the document is FAIL.",
    },
    "KLINE_WORKERS": {
        "value": KLINE_WORKERS,
        "ruled": False,
        "deferred_to": _VETO,
        "source": "PROPOSED by the OR-1 build 2026-09-21 — UNRULED [VETO]. A BOUNDED "
                  "thread pool for the ~530 weekly calls (weight 1 each at limit=8; the "
                  "whole run is ~570 weight against the exchange's 2400/min). Serial "
                  "would take minutes; unbounded would be rude.",
    },
    "WEIGHT_SOFT_CAP": {
        "value": WEIGHT_SOFT_CAP,
        "ruled": False,
        "deferred_to": _VETO,
        "source": "PROPOSED by the OR-1 build 2026-09-21 — UNRULED [VETO]. The exchange "
                  "reports the IP's used weight on every response "
                  "(X-MBX-USED-WEIGHT-1M). This IP is SHARED with the top-up and the "
                  "backfill, so when the header reads at or above this cap (half the "
                  "2400/min limit) each worker pauses WEIGHT_BRAKE_S before its next call.",
    },
    "WEIGHT_BRAKE_S": {
        "value": WEIGHT_BRAKE_S,
        "ruled": False,
        "deferred_to": _VETO,
        "source": "PROPOSED by the OR-1 build 2026-09-21 — UNRULED [VETO]. The pause "
                  "taken while the used-weight header is at or above WEIGHT_SOFT_CAP.",
    },
    "RUN_DEADLINE_S": {
        "value": RUN_DEADLINE_S,
        "ruled": False,
        "deferred_to": _VETO,
        "source": "PROPOSED by the OR-1 build 2026-09-21 (fix round 1) — UNRULED [VETO]. "
                  "Seconds from the start of the run after which the weekly sweep stops "
                  "WAITING: symbols not fetched by then are listed as such and count "
                  "against WEEKLY_SUCCESS_FLOOR like any other fetch that did not "
                  "succeed. A healthy run takes ~30 s. The number exists for the wire "
                  "that HANGS rather than refuses: one hung call is 4 x 60 s + 15 s of "
                  "backoff inside engine.data._get, and the on-demand wrapper SIGKILLs "
                  "this organ at its own MOVERS_TIMEOUT_S (600 when this was written; "
                  "F-MV-6 reads the live value by AST and goes RED if this deadline is "
                  "not below it). Even past this deadline the placeholder written before "
                  "the first call keeps a killed run from ever leaving printable numbers.",
    },
}

CLASS_LINE = ("DISPLAY-ONLY — movers tables written by a FETCH-ONLY organ "
              "(scripts/oracle_movers.py). Operations data, never study evidence "
              "(BR-1 §2). No gate, filter, heat, station, card or sizing computation "
              "may read a mover (OR-1). A reader prints numbers only when status is "
              "OK and date is the edition's date; otherwise WIRE DOWN.")

METHOD = {
    "universe": "exchangeInfo symbols with contractType == PERPETUAL, status == TRADING, "
                "quoteAsset == USDT; enumerated and sorted; the count is recorded, "
                "never asserted by the organ",
    "overnight": "pct = priceChangePercent and last_price = lastPrice from ONE "
                 "/fapi/v1/ticker/24hr call (rolling 24h ending at the fetch); units: "
                 "percent",
    "weekly": f"pct = (close_now / close_{WEEKLY_SPAN_DAYS}_back - 1) x 100 from "
              f"/fapi/v1/klines interval=1d limit={WEEKLY_BARS} per symbol; of the "
              f"{WEEKLY_BARS} bars index 0 is '{WEEKLY_SPAN_DAYS} back', the "
              "last bar is the forming UTC day and its close is close_now = last_price; "
              "rounded to 3 decimals like the exchange's own percent; units: percent",
    "sort": "each table holds EVERY universe symbol that has a number, sorted by signed "
            "pct DESCENDING, ties broken by symbol ascending; *_top is the first top_n "
            "rows of the same list",
    "nulls": "a universe symbol with no number in a table is listed in overnight_null / "
             "weekly_null with its reason; rows + nulls == universe, both tables",
    "status": "OK only if exchangeInfo and the 24hr ticker answered AND succeeded / "
              "attempted of the weekly fetches is at or above WEEKLY_SUCCESS_FLOOR; "
              "otherwise FAIL, and a FAIL document carries EMPTY tables. The file is "
              "first written as FAIL with in_flight true BEFORE any call, and replaced "
              "by the run's own result: a reader that finds in_flight true is looking "
              "at a run that is still going or that never finished",
}

ENDPOINTS = {"base": REST_BASE, "universe": EP_EXCHANGE_INFO,
             "overnight": EP_TICKER_24H, "weekly": EP_KLINES}

# EVERY top-level key of EVERY document this organ writes — OK, FAIL, placeholder
# alike (verifier finding on the first build: a FAIL document lacked up to ten keys
# the docstring promised, so a WIRE DOWN line printing doc['fetched_local'] would
# have died on a crash document). _base_doc() is the one place a document is
# born; F-MV-3 and F-MV-5 compare what is on disk against these two tuples.
DOC_KEYS = (
    "class", "date", "date_basis", "fetched_utc", "fetched_local", "status",
    "in_flight", "fail_reasons", "universe_count", "universe",
    "exchange_symbols_total", "excluded_counts", "ticker_rows_total",
    "ticker_quietest_symbol", "ticker_quietest_age_seconds", "top_n",
    "overnight", "overnight_top", "overnight_null",
    "weekly", "weekly_top", "weekly_null", "weekly_fetch", "errors", "method",
    "endpoints", "register", "organ", "used_weight_1m_peak",
    "weight_brakes_taken", "runtime_seconds",
)
WEEKLY_FETCH_KEYS = ("attempted", "succeeded", "failed", "not_fetched", "fraction",
                     "floor", "stopped_early")


# ═══════════════════════════════════════════════════════════ SMALL HELPERS

def now_ms() -> int:
    return int(time.time() * 1000)


def day_open(ms: int) -> int:
    return ms - ms % DAY_MS


def iso_ms(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, timezone.utc).isoformat()


def local_date() -> str:
    """The MACHINE-LOCAL date — the same clock the Oracle names its edition by."""
    return datetime.now().astimezone().strftime("%Y-%m-%d")


def doc_path(date_str: str) -> Path:
    return MOVERS_DIR / f"movers_{date_str}.json"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _rel(p: Path) -> str:
    """For PRINTING only. MOVERS_DIR may be redirected outside ROOT (every fixture
    does it); the first build's --dry-run called relative_to() bare and died there."""
    return str(p.relative_to(ROOT) if p.is_relative_to(ROOT) else p)


def sort_rows(rows: list[dict]) -> list[dict]:
    """Signed pct DESCENDING, symbol ascending on ties — on the STORED values, so
    a reader (and F-MV-3) can re-derive the order from the file alone."""
    return sorted(rows, key=lambda r: (-r["pct"], r["symbol"]))


class _Weight:
    """The exchange's own used-weight header, remembered across the pool."""

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.last = 0
        self.peak = 0
        self.brakes = 0

    def note(self, resp) -> None:
        try:
            w = int(resp.headers.get("X-MBX-USED-WEIGHT-1M", ""))
        except (TypeError, ValueError):
            return
        with self.lock:
            self.last = w
            self.peak = max(self.peak, w)

    def brake(self) -> None:
        with self.lock:
            hot = self.last >= WEIGHT_SOFT_CAP
            if hot:
                self.brakes += 1
        if hot:
            time.sleep(WEIGHT_BRAKE_S)


def _json_200(resp, what: str):
    # engine.data._get hands back a 404 as a normal Response; it is not one here.
    if resp.status_code != 200:
        raise RuntimeError(f"HTTP {resp.status_code} for {what}")
    return resp.json()


# ══════════════════════════════════════════════════════════ THE THREE FETCHES

def fetch_universe(weight: _Weight) -> tuple[list[str], dict]:
    """ONE exchangeInfo call. Returns the sorted universe and what was left out."""
    resp = _get(REST_BASE + EP_EXCHANGE_INFO)
    weight.note(resp)
    info = _json_200(resp, EP_EXCHANGE_INFO)
    want = REGISTER["UNIVERSE_FILTER"]["value"]
    syms = info["symbols"]
    universe = sorted({s["symbol"] for s in syms
                       if all(s.get(k) == v for k, v in want.items())})
    # What the literal filter excluded, by (contractType, status, quoteAsset) —
    # recorded so that "count printed, never asserted" includes the other side.
    excluded: dict[str, int] = {}
    for s in syms:
        if not all(s.get(k) == v for k, v in want.items()):
            tag = "|".join(str(s.get(k)) for k in want)
            excluded[tag] = excluded.get(tag, 0) + 1
    facts = {"exchange_symbols_total": len(syms),
             "excluded_counts": [{"class_tag": k, "count": n}
                                 for k, n in sorted(excluded.items(),
                                                    key=lambda kv: (-kv[1], kv[0]))]}
    return universe, facts


def fetch_overnight(universe: list[str], weight: _Weight) -> tuple[list[dict], list[dict], dict]:
    """ONE ticker/24hr call for every symbol on the exchange; filtered to the universe."""
    resp = _get(REST_BASE + EP_TICKER_24H)
    weight.note(resp)
    got_ms = now_ms()
    tick = {t["symbol"]: t for t in _json_200(resp, EP_TICKER_24H)}
    rows, nulls = [], []
    oldest = None
    for sym in universe:
        t = tick.get(sym)
        if t is None:
            nulls.append({"symbol": sym, "reason": "absent from the 24hr ticker response"})
            continue
        try:
            pct, last = float(t["priceChangePercent"]), float(t["lastPrice"])
        except (KeyError, TypeError, ValueError) as e:
            nulls.append({"symbol": sym, "reason": f"unparseable ticker row ({e.__class__.__name__})"})
            continue
        if not (math.isfinite(pct) and math.isfinite(last)):
            nulls.append({"symbol": sym, "reason": "non-finite ticker value"})
            continue
        rows.append({"symbol": sym, "pct": pct, "last_price": last})
        ct = t.get("closeTime")
        if isinstance(ct, int) and (oldest is None or ct < oldest[1]):
            oldest = (sym, ct)
    # NOT a filter — a fact. The ticker's closeTime is the symbol's last trade; a
    # TRADING symbol that has not traded for hours still prints the exchange's
    # number, and the age of the quietest one is recorded so it can be seen.
    facts = {"ticker_rows_total": len(tick),
             "ticker_quietest_symbol": oldest[0] if oldest else None,
             "ticker_quietest_age_seconds": (round((got_ms - oldest[1]) / 1000, 1)
                                             if oldest else None)}
    return sort_rows(rows), nulls, facts


def weekly_from_bars(bars, t_before_ms: int, t_after_ms: int) -> tuple[float | None, float | None, str | None]:
    """REGISTER['WEEKLY_DEFINITION'] as a PURE function, so a fixture can drive it.

    Returns (pct, last_price, reason). reason is None exactly when pct is a number.
    `bars` is the raw klines payload: [[open_time, o, h, l, c, ...], ...] oldest first.
    """
    if not isinstance(bars, list):
        return None, None, "klines payload is not a list"
    if len(bars) < WEEKLY_BARS:
        return None, None, f"fewer than {WEEKLY_BARS} daily bars ({len(bars)})"
    bars = bars[-WEEKLY_BARS:]
    try:
        opens = [int(b[0]) for b in bars]
        c_then, c_now = float(bars[0][4]), float(bars[-1][4])
    except (IndexError, TypeError, ValueError) as e:
        return None, None, f"unparseable daily bar ({e.__class__.__name__})"
    # "7 back" must MEAN seven days back (WEEKLY_SPAN_DAYS). A hole in the dailies
    # (a halt, a relisting) would make index 0 older than that and the number a lie.
    if opens[-1] - opens[0] != WEEKLY_SPAN_DAYS * DAY_MS or \
            any(b - a != DAY_MS for a, b in zip(opens, opens[1:])):
        return None, None, f"daily bars are not {WEEKLY_BARS} contiguous UTC days"
    # ...and close_now must be NOW: the last bar has to be the forming UTC day.
    # Two clocks are accepted so a call that straddles 00:00Z is not penalised.
    if opens[-1] not in (day_open(t_before_ms), day_open(t_after_ms)):
        return None, None, f"last daily bar opens {iso_ms(opens[-1])} — not the current UTC day"
    if not (math.isfinite(c_then) and math.isfinite(c_now)) or c_then <= 0:
        return None, None, "non-finite or non-positive close"
    return round((c_now / c_then - 1.0) * 100.0, 3), c_now, None


def floor_unreachable(total: int, failed: int) -> bool:
    """True once NOTHING the rest of the sweep can do lifts succeeded / total back
    to WEEKLY_SUCCESS_FLOOR — the same arithmetic fetch() judges the finished
    sweep by, asked early. 528 symbols at 0.95: true from the 27th failure."""
    return total > 0 and (total - failed) / total < WEEKLY_SUCCESS_FLOOR


class _Sweep:
    """What the pool shares: the failure count, and the flag that stops it."""

    def __init__(self, total: int) -> None:
        self.lock = threading.Lock()
        self.total = total
        self.failed = 0
        self.stop = threading.Event()

    def note_failure(self) -> None:
        # The WORKER that records the fatal failure raises the flag itself, so no
        # other worker takes a symbol after it: on a wire where every call fails,
        # at most (failures the floor tolerates + KLINE_WORKERS) calls are ever
        # started. F-MV-5 counts them.
        with self.lock:
            self.failed += 1
            if floor_unreachable(self.total, self.failed):
                self.stop.set()


def fetch_weekly(universe: list[str], weight: _Weight, log=print,
                 deadline: float | None = None) -> tuple[list[dict], list[dict], list[dict], dict]:
    """One 1d-klines call per symbol through a BOUNDED pool. Failures are per symbol.

    Returns (rows, nulls, errors, sweep) with sweep = {failed, not_fetched,
    stopped_early}. `deadline` is a time.monotonic() instant or None.

    WHY DAEMON THREADS AND NOT ThreadPoolExecutor (which the first build used): a worker
    inside engine.data._get on a dead wire sleeps through 15 s of backoff, or
    hangs for minutes, and cannot be interrupted. An executor JOINS its workers
    — at shutdown and again at interpreter exit — so neither an early stop nor a
    Ctrl-C could end the process until every stuck call had given up (measured
    by the verifier: 375 s for 200 symbols, ~990 s for the real universe, against
    the wrapper's 600 s SIGKILL). Daemon workers can be walked away from: the
    main thread stops waiting, writes FAIL, exits, and they die with the process.
    """
    total = len(universe)
    sweep = _Sweep(total)
    todo: queue.SimpleQueue = queue.SimpleQueue()
    done: queue.SimpleQueue = queue.SimpleQueue()
    for sym in universe:
        todo.put(sym)

    def one(sym: str) -> dict:
        weight.brake()
        t0 = now_ms()
        try:
            resp = _get(REST_BASE + EP_KLINES,
                        params={"symbol": sym, "interval": "1d", "limit": WEEKLY_BARS})
            weight.note(resp)
            bars = _json_200(resp, f"{EP_KLINES} {sym}")
        except Exception as e:                      # recorded per symbol, never raised
            sweep.note_failure()
            return {"symbol": sym, "error": f"{e.__class__.__name__}: {e}"[:300]}
        pct, last, reason = weekly_from_bars(bars, t0, now_ms())
        return {"symbol": sym, "pct": pct, "last_price": last, "reason": reason}

    def worker() -> None:
        while not sweep.stop.is_set():
            try:
                sym = todo.get_nowait()
            except queue.Empty:
                return
            done.put(one(sym))

    for i in range(min(KLINE_WORKERS, total)):
        threading.Thread(target=worker, name=f"movers-weekly-{i}", daemon=True).start()

    got: dict[str, dict] = {}
    why = None
    while len(got) < total:
        try:
            res = done.get(timeout=SWEEP_POLL_S)       # a timeout, so Ctrl-C lands here
        except queue.Empty:
            res = None
        if res is not None:
            got[res["symbol"]] = res
            if len(got) % 100 == 0:
                log(f"    weekly {len(got)}/{total}  (used weight {weight.last} per min)")
        if sweep.stop.is_set():
            why = "floor"
            break
        if deadline is not None and time.monotonic() >= deadline:
            why = "deadline"
            sweep.stop.set()
            break
    while True:                                        # what had already landed
        try:
            res = done.get_nowait()
        except queue.Empty:
            break
        got[res["symbol"]] = res

    rows, nulls, errors = [], [], []
    for sym in universe:                               # universe order: reproducible lists
        res = got.get(sym)
        if res is None:
            nulls.append({"symbol": sym, "reason": "not fetched — the sweep stopped early"})
        elif "error" in res:
            errors.append({"symbol": sym, "stage": "weekly", "error": res["error"]})
            nulls.append({"symbol": sym, "reason": "fetch failed — see errors"})
        elif res["pct"] is None:
            nulls.append({"symbol": sym, "reason": res["reason"]})
        else:
            rows.append({"symbol": sym, "pct": res["pct"], "last_price": res["last_price"]})
    not_fetched = total - len(got)
    stopped = None
    if not_fetched and why == "floor":
        stopped = (f"weekly sweep STOPPED EARLY after {len(errors)} failed fetch(es) of "
                   f"{total}: WEEKLY_SUCCESS_FLOOR {WEEKLY_SUCCESS_FLOOR} could no longer "
                   f"be reached; {not_fetched} symbol(s) were not fetched")
    elif not_fetched:
        stopped = (f"weekly sweep ABANDONED at RUN_DEADLINE_S {RUN_DEADLINE_S} s from the "
                   f"start of the run; {not_fetched} symbol(s) were not fetched")
    if stopped:
        errors.append({"symbol": None, "stage": "weekly", "error": stopped})
    return sort_rows(rows), nulls, errors, {"failed": len(errors) - (1 if stopped else 0),
                                            "not_fetched": not_fetched,
                                            "stopped_early": stopped}


# ═══════════════════════════════════════════════════════════════ THE RUN

def _base_doc(started: datetime) -> dict:
    """WHERE EVERY DOCUMENT IS BORN: all of DOC_KEYS, defaulted to 'nothing, and
    FAIL'. The date and both fetch stamps come from ONE instant, the START of the
    run, so they cannot disagree across a local midnight (the first build stamped the
    date at the end and the fetch time at the start)."""
    local = started.astimezone()
    try:
        own_sha = sha256_file(Path(__file__).resolve())
    except OSError:
        own_sha = None
    return {
        "class": CLASS_LINE,
        "date": local.strftime("%Y-%m-%d"),
        "date_basis": ("machine-local date at the START of the run, "
                       f"UTC offset {local.strftime('%z')}"),
        "fetched_utc": started.isoformat(timespec="seconds"),
        "fetched_local": local.isoformat(timespec="seconds"),
        "status": "FAIL",
        "in_flight": False,
        "fail_reasons": [],
        "universe_count": 0,
        "universe": [],
        "exchange_symbols_total": None,
        "excluded_counts": [],
        "ticker_rows_total": None,
        "ticker_quietest_symbol": None,
        "ticker_quietest_age_seconds": None,
        "top_n": TOP_N,
        "overnight": [], "overnight_top": [], "overnight_null": [],
        "weekly": [], "weekly_top": [], "weekly_null": [],
        "weekly_fetch": {"attempted": 0, "succeeded": 0, "failed": 0, "not_fetched": 0,
                         "fraction": None, "floor": WEEKLY_SUCCESS_FLOOR,
                         "stopped_early": None},
        "errors": [],
        "method": METHOD,
        "endpoints": ENDPOINTS,
        "register": REGISTER,
        "organ": {"path": ORGAN_REL, "sha256": own_sha},
        "used_weight_1m_peak": 0,
        "weight_brakes_taken": 0,
        "runtime_seconds": None,
    }


def placeholder_doc(started: datetime) -> dict:
    """WRITTEN BEFORE THE FIRST CALL. If this is what a reader finds, the run is
    still going or never finished — either way there is nothing to print."""
    doc = _base_doc(started)
    doc["in_flight"] = True
    doc["fail_reasons"] = [
        f"fetch IN FLIGHT or NEVER FINISHED — started {doc['fetched_utc']}. This "
        "placeholder is written before the first call and replaced by the run's own "
        "result; if it is still here the run was killed, timed out, interrupted or "
        "lost power before it could say how it ended (or is running right now)."]
    return doc


def fail_doc(started: datetime, reason: str, tb: str) -> dict:
    """The document for a run that died outside the three guarded fetches."""
    doc = _base_doc(started)
    doc["fail_reasons"] = [reason]
    doc["errors"] = [{"symbol": None, "stage": "unhandled", "error": tb[-1200:]}]
    doc["runtime_seconds"] = round(
        (datetime.now(timezone.utc) - started).total_seconds(), 2)
    return doc


def fetch(log=print, started: datetime | None = None) -> dict:
    """Fetch everything and return the document. Writes NOTHING — see write_doc()."""
    t_start = time.time()
    started = started or datetime.now(timezone.utc)
    deadline = time.monotonic() + RUN_DEADLINE_S
    weight = _Weight()
    doc = _base_doc(started)
    fail: list[str] = doc["fail_reasons"]
    errors: list[dict] = doc["errors"]
    universe: list[str] = []
    overnight: list[dict] = []
    overnight_null: list[dict] = []
    weekly: list[dict] = []
    weekly_null: list[dict] = []

    try:
        universe, ufacts = fetch_universe(weight)
        doc.update(ufacts)
        # COUNT PRINTED, NEVER ASSERTED (contract). The floor lives in F-MV-3.
        log(f"  universe  {len(universe)} symbol(s)  "
            f"[PERPETUAL · TRADING · USDT]  of {ufacts['exchange_symbols_total']} on the exchange")
    except Exception as e:
        fail.append("exchangeInfo failed")
        errors.append({"symbol": None, "stage": "exchangeInfo",
                       "error": f"{e.__class__.__name__}: {e}"[:300]})

    if not fail:
        try:
            overnight, overnight_null, ofacts = fetch_overnight(universe, weight)
            doc.update(ofacts)
            log(f"  overnight {len(overnight)} row(s), {len(overnight_null)} null  (one call)")
        except Exception as e:
            fail.append("24hr ticker failed")
            errors.append({"symbol": None, "stage": "ticker_24hr",
                           "error": f"{e.__class__.__name__}: {e}"[:300]})

    # No weekly sweep into a run that is already FAIL: ~530 calls for a document
    # that will carry no numbers would be weight spent on nothing. The same
    # reasoning, applied INSIDE the sweep, is floor_unreachable().
    if not fail:
        weekly, weekly_null, werr, sweep = fetch_weekly(universe, weight, log=log,
                                                        deadline=deadline)
        errors.extend(werr)
        attempted = len(universe)
        succeeded = attempted - sweep["failed"] - sweep["not_fetched"]
        frac = succeeded / attempted if attempted else 0.0
        doc["weekly_fetch"] = {"attempted": attempted, "succeeded": succeeded,
                               "failed": sweep["failed"],
                               "not_fetched": sweep["not_fetched"],
                               "fraction": round(frac, 6) if attempted else None,
                               "floor": WEEKLY_SUCCESS_FLOOR,
                               "stopped_early": sweep["stopped_early"]}
        log(f"  weekly    {len(weekly)} row(s), {len(weekly_null)} null, "
            f"{sweep['failed']} fetch error(s), {sweep['not_fetched']} not fetched  "
            f"({succeeded} of {attempted} = {frac:.4f}, floor {WEEKLY_SUCCESS_FLOOR})")
        # ONE RULE judges the sweep, stopped early or not: a symbol that was never
        # fetched did not succeed. (A deadline that cuts off three symbols of 528
        # is still an honest table, with the three listed; a dead wire is not.)
        if frac < WEEKLY_SUCCESS_FLOOR:
            fail.append(sweep["stopped_early"] or
                        f"weekly fetch fraction {frac:.4f} is below "
                        f"WEEKLY_SUCCESS_FLOOR {WEEKLY_SUCCESS_FLOOR}")

    ok = not fail
    doc["status"] = "OK" if ok else "FAIL"
    doc["universe_count"] = len(universe)
    doc["universe"] = universe
    if ok:
        # NEVER STALE, NEVER PARTIAL: only an OK document carries numbers. A FAIL
        # document keeps _base_doc()'s EMPTY tables even when the ticker answered.
        doc["overnight"], doc["overnight_top"] = overnight, overnight[:TOP_N]
        doc["overnight_null"] = overnight_null
        doc["weekly"], doc["weekly_top"] = weekly, weekly[:TOP_N]
        doc["weekly_null"] = weekly_null
    doc["used_weight_1m_peak"] = weight.peak
    doc["weight_brakes_taken"] = weight.brakes
    doc["runtime_seconds"] = round(time.time() - t_start, 2)
    return doc


def write_doc(doc: dict) -> tuple[Path, str, int]:
    """THE ONLY WRITE IN THIS FILE. Atomic: a reader sees the old file or the new
    one, never half of either. The directory is created here and nowhere else."""
    MOVERS_DIR.mkdir(parents=True, exist_ok=True)
    p = doc_path(doc["date"])
    b = json.dumps(doc, indent=1, sort_keys=True, ensure_ascii=False).encode("utf-8")
    tmp = p.with_name(f"{p.name}.{os.getpid()}.tmp")
    tmp.write_bytes(b)
    os.replace(tmp, p)
    return p, hashlib.sha256(b).hexdigest(), len(b)


def _print_top(title: str, rows: list[dict], k: int, log) -> None:
    log(f"  {title} — top {k} of {len(rows)} by signed pct")
    for i, r in enumerate(rows[:k], 1):
        log(f"    {i:>2}. {r['symbol']:18} {r['pct']:>+10.3f} %   last {r['last_price']:g}")


def print_register(log=print) -> None:
    for name, row in REGISTER.items():
        chip = "RULED " if row["ruled"] else "[VETO]"
        log(f"  {chip} {name} = {row['value']!r}")
        if not row["ruled"]:
            log(f"         deferred_to: {row['deferred_to']}")
        log(f"         {row['source']}")


# ═══════════════════════════════════════════════════════════════════ MAIN

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Oracle movers organ (fetch-only; writes one json; display-only)")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the REGISTER, the endpoints and the output path; fetch nothing")
    a = ap.parse_args(argv)

    if a.dry_run:
        print("ORACLE MOVERS · DRY RUN — nothing is fetched, nothing is written")
        print_register()
        print("  endpoints:")
        print(f"    universe   GET {REST_BASE}{EP_EXCHANGE_INFO}                  (1 call)")
        print(f"    overnight  GET {REST_BASE}{EP_TICKER_24H}                   (1 call, all symbols)")
        print(f"    weekly     GET {REST_BASE}{EP_KLINES}?symbol=<S>&interval=1d&limit={WEEKLY_BARS}"
              f"   (1 call per universe symbol, {KLINE_WORKERS} workers)")
        print(f"  would write  {_rel(doc_path(local_date()))}  (gitignored, off-bus)")
        print("  order of writes: (1) a status-FAIL in_flight placeholder BEFORE the first "
              "call, (2) the run's own result over it")
        return 0

    started = datetime.now(timezone.utc)
    print(f"ORACLE MOVERS · fetch-only organ · {started.isoformat(timespec='seconds')}")
    # WRITE 1 — THE PLACEHOLDER, before anything can go wrong on the wire. From
    # here until the second write, today's file is a FAIL document: whatever
    # happens to this process, no reader can print an earlier run's numbers.
    p0, _, _ = write_doc(placeholder_doc(started))
    print(f"  placeholder -> {_rel(p0)}  (status FAIL · in_flight — this run's result replaces it)")
    try:
        doc = fetch(started=started)
    except BaseException as e:
        # Exception: a crash outside the three guarded fetches. KeyboardInterrupt /
        # SystemExit: someone stopped the run. Either way the placeholder is already
        # there; this replaces its "never finished" with what actually happened.
        tb = traceback.format_exc()
        print("MOVERS FETCH FAILED:\n" + tb)
        doc = fail_doc(started, f"fetch() ended by {e.__class__.__name__} — "
                                f"{'unhandled exception' if isinstance(e, Exception) else 'interrupted'}",
                       tb)
        if not isinstance(e, Exception):
            write_doc(doc)
            raise
    # WRITE 2 — the result, over the placeholder.
    p, sha, nb = write_doc(doc)
    if doc["status"] == "OK":
        _print_top("OVERNIGHT", doc["overnight"], 5, print)
        _print_top("THE WEEK", doc["weekly"], 5, print)
        if doc["weekly_null"]:
            print(f"  weekly NULL ({len(doc['weekly_null'])}), listed, never guessed: "
                  + ", ".join(f"{n['symbol']}" for n in doc["weekly_null"][:12])
                  + (" …" if len(doc["weekly_null"]) > 12 else ""))
    else:
        print(f"  STATUS FAIL — {'; '.join(doc['fail_reasons'])}")
        print("  today's json is written as FAIL with EMPTY tables: WIRE DOWN, never stale numbers")
    print(f"  status {doc['status']} · universe {doc['universe_count']} · "
          f"{len(doc['errors'])} error(s) · runtime {doc['runtime_seconds']} s · "
          f"peak used weight {doc['used_weight_1m_peak']} per min")
    print(f"  movers json -> {_rel(p)}\n"
          f"  {nb} B  sha256 {sha}")
    return 0 if doc["status"] == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
