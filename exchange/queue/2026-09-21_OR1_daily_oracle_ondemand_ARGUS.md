# QUEUE OR-1 — THE DAILY ORACLE · on-demand edition, roster, ranges, market page

RATIFIED: operator, 2026-09-21 — by firing; rulings verbatim: "1-watchlist: drop symbols
without data from a binance contract // 2-5-agreed // 6-defaults // 7-add a list at the
end of the oracle with the top 50 coins by %change overnight and weekly".
Executor HEPHAESTUS, reviewer ARGUS. Class operations/display-only; firewall clauses of
BR-1 §2 reprinted and binding; no gate, filter, or sizing reads a range or a mover.
BUILT: exchange/reports/BUILD_2026-09-21_DAILY_ORACLE.md · code commits 3a5e6e7 (T-7, prerequisite) + 1695a69 D1 + d8fa962/7ce235c A + 31da6d0 E1 + 34e19e8 B + d63592f C + ee93644 D2 + 7a1df59 E2 + fa1bf80 F + 26a27c7 (five-lens review repairs) · F-BR-1..17 17/17 · F-SK 11/11 · F-MV 9/9 · F-TU 6/6 · F-RF 8/8 + 8/8 on the frozen tape · pytest 261 · roster 18 kept / 4 dropped · first on-demand edition briefs/oracle/oracle_2026-09-21.html 451,533 B exit 0, self-checks 3/3 PASS

## §2 CLASS & FIREWALL (BR-1 §2, reprinted verbatim, binding)
Source of record: `docs/history/queue/2026-08-16_BR1_brief_redesign_ARGUS.md:10-15`.

Operations/display-only. (1) Live data is operations-only, forbidden as study evidence;
rules are born only under G-7 on exploration-classic. (2) No journal reads; no signal-outcome
statistics on any window. (3) Engine modules imported read-only, trading disabled, never
modified. (4) The archive may be mined for hypotheses, never scored. RECORDING an event is
operations; AGGREGATING outcomes is census work under G-7. Fixtures scan code, not prose.

OR-1 extension of the same wall, from the ratification line above: **no gate, filter, or
sizing reads a range or a mover.** The range layer (STEP D) and the Market Page (STEP E) exist
in the render and the tape only. The movers organ is fetch-only and is its own process; the
Oracle itself stays cache-only (BR-1b: "it may never fetch inside a firewalled run").

## THE CONTRACT (the operator's execution paste of 2026-09-21, verbatim)

STEP A — THE /oracle SKILL (repo-tracked): .claude/skills/oracle/SKILL.md with
frontmatter {name: oracle, description: "Print an edition of The Daily Oracle on demand"}.
Verbs: `/oracle` full edition · `/oracle refresh` (Watch/Board only) · `/oracle --no-fetch`
(cache-only; LATE EDITION band tells the truth). Body = the chain the clock ran, step by
step with expected outputs: identity gate → if ORACLE_DOWN.flag exists print it FIRST →
movers fetch (STEP E) → in-scope top-up → oracle_daily (full|refresh) → open the render →
print the Front Page's top rows + the self-check verdict. Selfcheck rows tagged
slot="on-demand-full"|"on-demand-refresh" so run-based gates can read them. Fixture
F-SK-1: skill file parses; a dry invocation prints the step list; a planted missing
step fails.

STEP B — C-0 FIX (integrity before features): in the D-7 calibration logger, measure
maturity_withheld_fraction via analytics.vwap.maturity() (no more literal 0.0); record
family-cap binding counts and target-bucket occupancy. oracle_daily.py changes ⇒ RE-PIN
the top-up in the SAME commit (F-TU-1). Fixture F-BR-13: planted literal 0.0 ⇒ red;
measured values differ across assets on a real run. Record in the build doc: calibration
JSONs dated BEFORE this commit are hollow for three families and are EXCLUDED from any
future recalibration — the calibration clock restarts today, honestly.

STEP C — ROSTER: probe Binance USDT-M exchangeInfo ONCE (contractType PERPETUAL, status
TRADING) for the operator's 22: BTC NPC ETH ENA SOL PUMPFUN USELESS NEAR 1000PEPE LIT
FARTCOIN HYPE XPL ZEC MNT UNI LTC ZCAT BNB XMR DOGE 1000BONK (as <X>USDT). Keep what
exists; DROP the rest by ruling; print both lists by name. Write the roster as a named
constant in the Oracle's config (named-constant protocol: grep NAME+VALUE+THRESHOLD; one
source of truth) and save research_outputs/oracle/roster_probe_2026-09-21.json. Re-
enumerate top-up scope (new pairs × the Oracle's intervals); backfill new symbols to the
SAME depth per interval as BTC currently holds [VETO default]; print rows fetched per
pair, 0 gaps, 0 clobbers. Re-pin. F-TU suite green.

STEP D — RANGE LAYER: lift the RangeFinder twin into engine/rangefinder.py as an importable
module (same v2 pins, same event log; the twin becomes a thin caller; determinism fixture
F-RF-1 must still pass byte-identical). oracle_daily runs it per roster symbol on the 4h
lens [VETO default — the system's lens] and emits per symbol: macro state · macro top/
bottom · %position · ATR-distance to nearest macro boundary · PENDING-breach flag ·
last event + age. Board row gains a RANGE cell; new section TIDE TABLES lists all; EDGE
WATCH sub-list = distance ≤ 0.5 ATR [VETO] OR pending breach open, sorted by distance.
Fixture F-BR-14: posture_engine.py byte-unchanged (sha printed); the range object appears
only in render + tape, never in any gate path (component-wise import scan); planted gate
read ⇒ red.

STEP E — MARKET PAGE: scripts/oracle_movers.py, FETCH-ONLY, its own organ: universe from
exchangeInfo (PERPETUAL·TRADING·USDT quote; count printed, never asserted); overnight =
Binance /fapi/v1/ticker/24hr priceChangePercent [VETO]; weekly = close_now / close of the
1d bar 7 back − 1 from 1d klines limit=8 [VETO]; write research_outputs/oracle/movers/
movers_<date>.json (off-bus). NEVER writes the kline cache (fixture F-MV-1: cache dir
sha-identical before/after; F-MV-2: firewall scan; F-MV-3: universe count ≥ 150 and
enumerated). oracle_daily reads the json only (cache-only stays true). Render two tables,
top 50 by signed % change each: OVERNIGHT and THE WEEK; footnote universe size + fetch
time; if the fetch failed, the page prints "WIRE DOWN — no movers this edition", never
stale numbers.

STEP F — THE DAILY ORACLE typesetting (semantics untouched, template only): paper #F4ECD8,
ink #1A1A1A, one red #B3261E for alarms; serif stack "Iowan Old Style", Palatino, Georgia,
serif; hairline column rules; small-caps section heads; drop cap on the lead. MASTHEAD
"THE DAILY ORACLE" · ears: left "Vol. I · No. <edition count>", right "Buenos Aires ·
<date> · <Morning|Refresh> Edition · Price: one toll". Sections in order: FRONT PAGE (the
Board; headline = the day's answer to "where is business possible today") · THE DOCKET
(Trap Cards) · THE WATCH (windows + mantle strips, EACH with a caption: "rows = threads,
rod 5000 top → hem 9 bottom · columns = last 96 bars · hue = thread above/below price in
ATR · dark pinch = knot · hole = unwoven") · TIDE TABLES (STEP D + Edge Watch) · TELEGRAMS
(R1 blocks) · THE MARKET PAGE (STEP E) · YESTERDAY'S RETURNS (ORACLE GRID footer) ·
COLOPHON (DISPLAY-ONLY line, payload shas, certified/not-certified lists, as-of).
Staleness banner ⇒ red band under the masthead "LATE EDITION — wire stale since <as-of>".
Light paper only [D-7a]. Fixtures: F-BR-15 every mantle strip has its caption; all eight
sections present in order; colophon carries the DISPLAY-ONLY fragment; F-BR-1..12 all
still green (no semantics moved).

STEP G — BR-2 AMENDMENT A-BR2-2 (append to the BR-2 queue file, body untouched): gates
restated in RUNS by ruling D-1a — G-BR2-1 ≥7 dated editions; G-BR2-2 PASS on ≥5 of the
last 7 RUNS (on-demand slots count; fixture rows excluded as last_real_run() does);
G-BR2-3 the PARITY line, unchanged and still owed; WORK(1) uses only calibration JSONs
dated after the STEP B commit.

STEP H — CLOSE: run `/oracle` once for real (movers fetch, top-up, full edition); print
path, bytes, sha, as-of, banner state, Edge Watch count, movers universe size, roster
final count. ONE build document exchange/reports/BUILD_2026-09-21_DAILY_ORACLE.md (zero-
context; the month's ledger tail summarized; roster kept/dropped; all fixture transcripts
two-leg; findings reported-not-fixed; disposition + BOX COST — movers json and renders
off-bus). LEDGER_ARGUS append: schedule suspended; /oracle live; C-0 closed; roster N;
range layer + Market Page in; BR-2 A-BR2-2; PENDING: PARITY line · first-edition operator
verdict · V-7. Publish per §3.4; result plainly; box line. Stamp OR-1 BUILT.

GATES: G-1 five agents absent; G-2 skill file exists, F-SK-1 green; G-3 C-0 fixture green
+ re-pin in same commit (both shas); G-4 roster probe json exists, kept/dropped printed;
G-5 F-RF-1 byte-identical through the module lift; G-6 movers json exists, universe ≥150,
cache sha unchanged; G-7 edition renders with all eight sections + captions; G-8 BR-2 tail
contains "A-BR2-2"; G-9 ledger ends "END STATUS"; G-10 publish names commit + result; G-11
box below warn. Disposition table; IN BRIGHT COLOURS: the edition's path (open this) + the
build doc name.
