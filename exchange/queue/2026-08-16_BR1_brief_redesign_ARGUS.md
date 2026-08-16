# QUEUE BR-1 — BRIEF_REDESIGN_SPEC_v1 · THE HUNTER'S ORGAN
**Drafted:** ARGUS 2026-08-16 under queue drafting rights. **Status: AWAITING RATIFIED STAMP.**
**Executor:** HEPHAESTUS. **Reviewer:** ARGUS. **Merge authority:** operator.

## §1 PURPOSE
The daily brief was retired from daily_routine 2026-08-05 (ruling 4a); the organ is dark.
This contract rebirths it in the Board/Trap-Cards/Watch architecture with one station engine,
so the discretionary hunter and the TC4 machine read the same tape. Operations-only.

## §2 CLASS & FIREWALL (reprinted, binding)
Operations/display-only. (1) Live data is operations-only, forbidden as study evidence;
rules are born only under G-7 on exploration-classic. (2) No journal reads; no signal-outcome
statistics on any window. (3) Engine modules imported read-only, trading disabled, never
modified. (4) The archive may be mined for hypotheses, never scored. RECORDING an event is
operations; AGGREGATING outcomes is census work under G-7. Fixtures scan code, not prose.

## §3 CONSTANTS — each [VETO], rulings of 2026-08-16 pinned
C-1 CADENCE = 07:00 local America/Argentina/Buenos_Aires full brief + 16:00 local Watch/Board
    refresh [D1c; refresh slot 16:00 is ARGUS-proposed default — veto if another hour serves].
    Delivered via slot-anchored launchd wrapper (launchd has no timezone field).
C-2 TOLL = ORACLE grid per-lens NET toll table, by name and lens [D2a]. No cost-free number
    prints anywhere; net R:R only.
C-3 STATIONS = station canon v1 verbatim (STALKING/ARMED/TRIGGERED/DEAD); one canonical
    module `scripts/station_engine.py` read by Board, Cards, and the Pine-parity fixture.
    No re-derived semantics anywhere [D3].
C-4 SPAGHETTI = event-anchored at each asset's last 89/316 tide flip; ATR-normalized paths;
    one panel [D4, operator's two named pins].
C-5 BOARD = 10 rows, heat-sorted: regime chip · ATR-distance to nearest high-score cluster ·
    two lines in the sand · posture word. Roster = current 10-asset capture set [veto to trim].
C-6 CARD = entry · structural invalidation (4h-lens anchor + min 1.0 ATR rail, per the TC3
    rulings) · target · net R:R (C-2) · "what proves me wrong". Derivation to appendix.
C-7 WATCH = live 12/89 windows (age, displacement, trigger status) + static last-96-bars
    mantle thumbnail per asset, rendered FROM the v4 payload pattern, never recomputed ad hoc.
C-8 ORACLE FOOTER = yesterday's fired events classified against the grid's NET table, per lens.
C-9 ALERTS = R1 only: alert-price blocks formatted for TradingView copy-paste. R2 waits behind
    the parity gate; R3 waits for census-ruled rules.
C-10 TAPE = one event stream, two renders: HTML cards for the operator, parquet for TC4.
     Parquet lives under research_outputs/, path+sha pointer only on the bus.

## §4 FIXTURES (numbered; each shown FAILING on a deliberate break before trusted)
F-BR-1 PARITY: station words on the frozen fixture day match Pine SS v12.1 markers, symbol
       for symbol; mismatch list printed (empty = pass).
F-BR-2 TOLL PRESENCE: code scan proves every outcome column renders with its per-lens toll
       band; a cost-free outcome column fails the build.
F-BR-3 FIREWALL: import graph proves no journal module reachable; no aggregation of live
       outcomes anywhere in brief code.
F-BR-4 THUMBNAIL PROVENANCE: mantle strip bytes derive from a sha-stamped payload; sha printed
       in the strip's own footer.
F-BR-5 ANCHOR DETERMINISM: the C-4 tide-flip anchor recomputed twice from the same substrate
       is identical; anchor timestamp printed per asset.
F-BR-6 REFRESH IDEMPOTENCE: the 16:00 refresh over unchanged data emits byte-identical
       Watch/Board sections.
F-BR-7 R1 FORMAT: alert block parses as price levels only — no prose, no advice, paste-ready.
F-BR-8 PROVENANCE FOOTER on the brief HTML: DISPLAY-ONLY header, payload shas, date, the
       certified/not-certified lists both printed.
F-BR-9 BOX: brief HTML and parquet never enter exchange/; pointer lines only; publish
       bus-health printed.

## §5 DELIVERABLES
D-1 scripts/station_engine.py (canon v1, closed register). D-2 brief generator emitting
Board/Cards/Watch/footer/R1 per §3. D-3 slot-anchored launchd wrapper + two armed slots.
D-4 parquet tape emitter. D-5 ONE build document (single-build-document rule) with full
fixture transcript, disposition table, BOX COST. D-6 LEDGER_ARGUS append.

## §6 VERDICT CRITERIA
ACCEPT iff F-BR-1..9 pass with transcripts, one unattended 07:00 run produces the brief with
zero manual steps, and the operator confirms the Board answers "where is business possible
today" in one glance. Partial adoption forbidden.

## §7 WHAT THIS PHASE IS NOT
Not R2/R3 alerting. Not census work — nothing here scores outcomes. Not new indicators, not
sizing, not Pine changes. Not a resurrection of the 3x/day capture era beyond what C-1 names.

## §8 OPEN AT DRAFT TIME
The 16:00 refresh hour [VETO default] · Board roster trim · render-size constant (carried
from the audit note) · charter amendment (viz estate + brief redesign into CONVENTIONS §5.1)
routed to ATHENA as file owner.
— ARGUS

RATIFIED: operator, 2026-08-16 — "ratify BR-1, refresh 16:00, roster as-is"
BUILT: exchange/reports/BUILD_2026-08-16_ORACLE_REBIRTH.md · code commit a36edc1 · F-BR-1..F-BR-10 10/10 green · two slots armed · one unattended run exit 0

## AMENDMENT A1 (operator rulings 2026-08-16, appended at stamp time)
A1-1 RENAME: the product is THE ORACLE. Disambiguation, binding all lanes: "Oracle"
     unqualified = this daily organ; the census-2B artifact is always "ORACLE GRID",
     fully qualified. All BR-1 deliverables use oracle_* naming.
A1-2 C-1 pinned: refresh slot = 16:00 America/Argentina/Buenos_Aires. Roster as-is.
A1-3 CHAIN PRE-AUTHORIZED (operator verbatim: "proceed bravely ahead to stamp → build →
     live week → recalibrate → parity → R2 — collapse this workflow into the fewest
     possible pastes"): queue BR-2 files this session already ratified, executable only
     when its own gates pass. Constants proposed by BR-2 remain [VETO] — measured and
     proposed by the machine, adopted only by the operator.
A1-4 NEW DELIVERABLE D-7, calibration logger: each run appends one JSON of
     display-machinery distribution stats ONLY (per-asset level counts, cluster widths,
     collapse events, LIS distances, maturity-withheld fractions, window ages) to
     research_outputs/oracle/calibration/. NO outcome fields, NO signal-performance
     fields — enforced by fixture F-BR-10 (code scan; shown failing on a planted
     outcome field first). This is what makes the live week self-instrumenting.
