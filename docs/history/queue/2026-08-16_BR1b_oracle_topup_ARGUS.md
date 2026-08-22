# QUEUE BR-1b — ORACLE DATA FRESHNESS
Drafted ARGUS 2026-08-16. Executor HEPHAESTUS. Reviewer ARGUS.
RATIFIED: operator, 2026-08-16 (chain auth A1-3)
BUILT: exchange/reports/BUILD_2026-08-16_ORACLE_TOPUP.md · code commits 3bdc4c5 + 20f4a36 (post-review repairs) · F-TU-1..F-TU-6 6/6 green · two slots armed · one unattended run exit 0 · +2,521 rows across 40 pairs, 0 gaps

QUEUE BR-1b — ORACLE DATA FRESHNESS. RATIFIED: operator, 2026-08-16 (chain auth
A1-3). Fetch-and-store ONLY: scope = EXACTLY the (symbol, interval) set enumerated
from oracle_daily.py's cache reads this session — to claim the set, enumerate the
set. Slots 06:45 + 15:45 America/Argentina/Buenos_Aires via the slot-anchored
wrapper. No journal import, no aggregation, no publish, no exchange/ writes.
Network failure: log to research_outputs/oracle/calibration/topup_log.jsonl, exit
nonzero; the Oracle is unaffected and stamps its as-of. Not this contract: no
schema change, no new intervals, no touch of com.naiad.daily.

## ORIGIN
Finding V-8 of BUILD_2026-08-16_ORACLE_REBIRTH: "THE KLINE ESTATE IS ~1 DAY STALE AND
NOTHING SCHEDULED REFRESHES IT ... A top-up job is owed if the 07:00 Oracle is to read
yesterday's close." The Oracle is cache-only by design and must stay that way — it may
never fetch inside a firewalled run. This contract puts the fetching in a separate
organ that runs 15 minutes ahead of each Oracle slot.

## GATES (HARD, checked before any work)
G-TU-1 SCOPE IS ENUMERATED, NEVER ASSERTED: the (symbol, interval) set is obtained by
       instrumenting oracle_daily.py's own cache reads on a real run, pinned to a
       manifest that records the enumerating file's sha256. If oracle_daily.py has
       changed since the pin, the top-up HALTS and demands re-enumeration.
G-TU-2 NO-CLOBBER: history never shrinks and no pre-existing bar changes value. Proven
       per pair, both directions, every run.
G-TU-3 THE ORACLE IS UNAFFECTED BY FAILURE: a network fault logs, exits nonzero, and
       leaves the cache exactly as it found it.

## FIXTURES (each shown FAILING on a deliberate break before trusted)
F-TU-1 SCOPE IDENTITY: the manifest equals a fresh instrumented enumeration, pair for
       pair; any drift is printed as a set difference.
F-TU-2 NO-CLOBBER: pre-existing rows are byte-identical after a top-up; row count is
       monotone non-decreasing.
F-TU-3 FIREWALL: import graph proves no journal read, no aggregation, no publish
       module reachable from the top-up.
F-TU-4 NO exchange/ WRITE: the top-up's write set is confined to the kline cache and
       research_outputs/oracle/.
F-TU-5 CONTIGUITY: after a top-up every series is gap-free at its own interval, or the
       gap list is printed with each gap's span.
F-TU-6 FAILURE PATH: a simulated network fault logs to topup_log.jsonl, exits nonzero,
       and leaves the cache unchanged.

## DELIVERABLES
D-1 scripts/oracle_topup.py. D-2 the scope manifest. D-3 two armed slots at 06:45 and
15:45 via the existing slot-anchored wrapper. D-4 ONE build document with the fixture
transcript, the enumerated scope, the arming proof and the disposition table.
D-5 LEDGER_ARGUS append.

## VERDICT CRITERIA
ACCEPT iff F-TU-1..6 pass with transcripts, one unattended run completes with the cache
advanced and contiguity intact, and the Oracle's next run reads the fresher bars without
any change to the Oracle itself.
— ARGUS
