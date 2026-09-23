# QUEUE OR-1 — THE DAILY ORACLE · on-demand edition, roster, ranges, market page

RATIFIED: operator, 2026-09-21 — by firing; rulings verbatim: "1-watchlist: drop symbols
without data from a binance contract // 2-5-agreed // 6-defaults // 7-add a list at the
end of the oracle with the top 50 coins by %change overnight and weekly".
Executor HEPHAESTUS, reviewer ARGUS. Class operations/display-only; firewall clauses of
BR-1 §2 reprinted and binding; no gate, filter, or sizing reads a range or a mover.
BUILT: exchange/reports/BUILD_2026-09-21_DAILY_ORACLE.md · code commits 3a5e6e7 (T-7, prerequisite) + 1695a69 D1 + d8fa962/7ce235c A + 31da6d0 E1 + 34e19e8 B + d63592f C + ee93644 D2 + 7a1df59 E2 + fa1bf80 F + 26a27c7 (five-lens review repairs) · F-BR-1..17 17/17 · F-SK 11/11 · F-MV 9/9 · F-TU 6/6 · F-RF 8/8 + 8/8 on the frozen tape · pytest 261 · roster 18 kept / 4 dropped · first on-demand edition briefs/oracle/oracle_2026-09-21.html 451,533 B exit 0, self-checks 3/3 PASS · RECOVERED 2026-09-23 under AMENDMENT A-OR1-1 (spec of record below): or1 commits 3d55988 D (iv, v) + ff74a90 F (vii) · recovery edition briefs/oracle/oracle_2026-09-23.html 452,747 B exit 0, self-checks 3/3 PASS, F-BR 17/17 default mode · R6 complete (72/72 at parity) · build doc §9

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

## SPECIFICATION OF RECORD

Filed 2026-09-22 by the recovery session (R4 of the operator's OR-1 recovery paste). Until
now OR-1's full text lived only in a chat paste, so a fresh session could not resume it.
From now on any recovery reads the repo, not a chat: the amendment and the steps below are
the authoritative text, copied exactly as the operator wrote them.

AMENDMENT A-OR1-1 (recovery, 2026-09-22) [VETO-by-firing]
 i   Backfill order, destination unchanged: new pairs' 1h/4h to BTC-parity depth now;
     5m/15m to 120 days now; the rest of 5m/15m to BTC parity runs LAST (R6), resumable
     via research_outputs/oracle/backfill_state.json, holding the wrapper's single-flight
     lock so no two writers ever touch one parquet; honour Binance weight headers, back
     off at 80%.
 ii  /oracle routes through scripts/oracle_wrapper.py with an on-demand slot, so
     self-checks, the T-7 ORACLE_DOWN.flag and the single-flight lock cover every edition.
 iii The Oracle's roster is its OWN named constant; engine/cells.py SYMBOLS is the
     engine's universe and is never edited by this contract.
 iv  The range module lives at scripts/rangefinder_core.py; engine/ is outside this
     lane's write authority (BR-1 §2 clause 3); promotion into engine/ is APOLLO's call.
 v   Range records go to a sibling tape, research_outputs/oracle/tape_ranges/; the TC4
     event tape's schema is untouched (A-BR2-1b doctrine).
 vi  One commit per step, "or1: step X — <what>": the repo is its own progress log.
 vii Edition word follows verb and hour: full before 12:00 BA = Morning, after = Evening;
     refresh = Refresh. A paper printed at night does not call itself the morning's.

THE STEPS OF RECORD (authoritative; execute only what R2 did not mark DONE)
S  SUSPEND: launchctl bootout gui/$(id -u)/<label> for com.naiad.oracle-topup-0645,
   -0700, -topup-1545, -1600, -catchup (idempotent); plists stay; write the five
   bootstrap commands to research_outputs/oracle/SUSPENDED_2026-09-21.txt; ledger line
   "ORACLE SCHEDULE SUSPENDED 2026-09-21 by operator ruling; on-demand /oracle replaces
   it; five agents booted out, plists retained".
1  QUEUE: exchange/queue/2026-09-21_OR1_daily_oracle_ondemand_ARGUS.md —
   "# QUEUE OR-1 — THE DAILY ORACLE · on-demand edition, roster, ranges, market page /
   RATIFIED: operator, 2026-09-21 — by firing; rulings verbatim: '1-watchlist: drop
   symbols without data from a binance contract // 2-5-agreed // 6-defaults // 7-add a
   list at the end of the oracle with the top 50 coins by %change overnight and weekly'
   / Executor HEPHAESTUS, reviewer ARGUS. Operations/display-only; BR-1 §2 firewall
   binding; no gate, filter or sizing reads a range or a mover. / BUILT: PENDING".
A  SKILL: .claude/skills/oracle/SKILL.md, frontmatter name: oracle, description "Print an
   edition of The Daily Oracle on demand". Verbs: /oracle (full) · /oracle refresh
   (Watch/Board) · /oracle --no-fetch (cache-only; LATE EDITION band tells the truth).
   Chain, each step with expected output: identity gate → ORACLE_DOWN.flag printed first
   if present → movers fetch (E) → in-scope top-up → oracle_wrapper.py with slot
   on-demand-full|on-demand-refresh → open the edition → print the Front Page's top rows
   + the self-check verdict. F-SK-1 two-leg: parses; dry run prints the chain; a planted
   missing step fails.
B  C-0: the calibration logger measures maturity_withheld_fraction via
   analytics.vwap.maturity() and records family-cap binding counts and target-bucket
   occupancy. Any oracle_daily.py change ⇒ re-pin the top-up in the SAME commit.
   F-BR-13 two-leg: planted literal 0.0 ⇒ red; real run ⇒ values differ across assets.
   Name the commit: calibration JSONs before it are hollow for three families and are
   excluded from any recalibration — the calibration clock restarts here.
C  ROSTER: one probe of Binance USDT-M exchangeInfo (PERPETUAL, TRADING) for BTC NPC ETH
   ENA SOL PUMPFUN USELESS NEAR 1000PEPE LIT FARTCOIN HYPE XPL ZEC MNT UNI LTC ZCAT BNB
   XMR DOGE 1000BONK (as <X>USDT); keep what exists, drop the rest by ruling, print both
   lists by name; save research_outputs/oracle/roster_probe_2026-09-21.json; write the
   kept list as the Oracle-owned roster constant (A-OR1-1 iii). Re-enumerate top-up
   scope (roster × the Oracle's intervals), rebind pairs_sha256, backfill per A-OR1-1 i
   (no-clobber, contiguity verified, one line per pair), re-pin, F-TU green.
D  RANGES: scripts/rangefinder_core.py = the RangeFinder v2 state machine as an
   importable module (same pins, same event log); rangefinder_twin.py becomes a thin
   caller; F-RF-1 byte-identical. oracle_daily runs it per roster symbol on 4h and
   emits: macro state · macro top/bottom · % position · ATR-distance to nearest macro
   boundary · pending-breach flag · last event + age. Board row gains a RANGE cell;
   TIDE TABLES lists all; EDGE WATCH = distance <= 0.5 ATR [VETO] OR an open breach,
   sorted by distance. Records to the sibling tape (A-OR1-1 v). F-BR-14 two-leg:
   posture_engine.py unchanged (sha printed); range objects reachable only from render
   and sibling tape, never a gate path (component-wise scan); planted gate read ⇒ red.
E  MOVERS: scripts/oracle_movers.py, fetch-only, its own organ. Universe = exchangeInfo
   PERPETUAL·TRADING·USDT-quote (count printed, never asserted). Overnight =
   /fapi/v1/ticker/24hr priceChangePercent [VETO]; week = last close ÷ close 7 daily
   bars back − 1, from 1d klines limit=8 [VETO]. Writes research_outputs/oracle/movers/
   movers_<date>.json (off-bus); never the kline cache. F-MV-1 cache dir sha-identical
   before/after · F-MV-2 firewall scan · F-MV-3 universe >= 150, enumerated. Render THE
   MARKET PAGE: two tables, OVERNIGHT and THE WEEK, top 50 by signed % change, footnote
   universe + fetch time; failed fetch ⇒ "WIRE DOWN — no movers this edition", never
   stale numbers.
F  THE PAPER (template only; no semantics move): paper #F4ECD8, ink #1A1A1A, one red
   #B3261E; "Iowan Old Style", Palatino, Georgia, serif; hairline rules; small-caps
   heads; drop cap on the lead. Masthead THE DAILY ORACLE; ears "Vol. I · No. <edition
   count>" | "Buenos Aires · <date> · <edition word per A-OR1-1 vii> Edition · Price: one
   toll". Sections in order: FRONT PAGE (the Board; headline answers "where is business
   possible today") · THE DOCKET · THE WATCH (each strip captioned "rows = threads, rod
   5000 top → hem 9 bottom · columns = last 96 bars · hue = thread above/below price in
   ATR · dark pinch = knot · hole = unwoven") · TIDE TABLES · TELEGRAMS · THE MARKET PAGE
   · YESTERDAY'S RETURNS · COLOPHON (DISPLAY-ONLY, payload shas, certified/not-certified,
   as-of). Stale ⇒ red band "LATE EDITION — wire stale since <as-of>". F-BR-15 two-leg
   (captions, eight sections in order, colophon fragment); F-BR-1..12 still green.
G  BR-2: append A-BR2-2 — gates in RUNS: G-BR2-1 >= 7 dated editions; G-BR2-2 PASS on
   >= 5 of the last 7 runs (on-demand slots count; fixture rows excluded); G-BR2-3 the
   PARITY line, unchanged and owed; WORK(1) reads only calibration JSONs after the step-B
   commit (sha named). Body untouched.
H  CLOSE: print one real edition by following SKILL.md's chain (a skill created
   mid-session may not register until the next session; say which path ran): path ·
   bytes · sha · as-of · banner state · Edge Watch count · movers universe · roster
   count. ONE build doc: complete BUILD_2026-09-21_DAILY_ORACLE.md if a partial one
   exists (add a §0 line: interrupted 2026-09-21, completed 2026-09-22), else create
   BUILD_2026-09-22_DAILY_ORACLE.md stating it completes OR-1. Zero-context: the R2 table
   before and after; roster kept/dropped; fixture transcripts two-leg; findings
   reported-not-fixed; disposition + BOX COST (renders, movers, tapes off-bus). Stamp
   OR-1 BUILT. LEDGER_ARGUS STATUS block: schedule suspended · /oracle live · C-0 closed
   · roster N · ranges + Market Page in · A-BR2-2 · R6 state · PENDING: PARITY line ·
   first-edition verdict · V-7. Publish per CONVENTIONS §3.4; result plainly; box line.
