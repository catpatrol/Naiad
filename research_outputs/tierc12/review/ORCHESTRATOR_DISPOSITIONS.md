# TIER-C12 · ORCHESTRATOR DISPOSITIONS ON THE LEANS REVIEW (2026-10-09)

The review of the draft committed at `7295ab5` returned 133 findings
(`review/LEANS_REVIEW_2026-10-09.json`: 30 BLOCKING, 67 MAJOR, 36 MINOR; six lenses). No book exists.
These dispositions bind the reconciler and every section fixer. They are decided on mechanism, contract text
and filed precedent — never on which reading would score better.

**OD-0 DEFAULT.** Every finding is ACCEPTED and its fix applied, unless it is wrong on the FACTS (the fixer
cites the source line that shows it) or it conflicts with a disposition below (then the disposition governs).
Where several findings give different fix texts for one defect, the text below (or, if none, the reconciler's
single canon text) is the one every section carries. A rejection is recorded with its reason; nothing is
silently dropped.

## Cross-section canon (one text, every section)

**OD-1 LABELS** (FID-01, STA-01, BLD-07, CMP-04; O-30). Three cell templates keyed by registration id:
- P-ADM-1: `<verdict> — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (pre_seen: <clause>)`
- P-SFP-VA-1, P-SCALP-3: `<verdict> — NOT CONFIRMATORY (pre_seen · KIN-SEEN: X3 printed value-area swing-failure outcomes on these bars)`
- P-BRD-1, P-DIR-1: `<verdict> — NOT CONFIRMATORY (selection_hazard: direction-informed)`; P-BRD-1 prints D-1 under its cell.
A label must be true; "re-score" appears on P-ADM-1 alone.

**OD-2 THE WALL** (FID-02, BLD-01, CMP-03, CAU-06, FID-09, BLD-32, BLD-16; O-29).
- DOORS_T is exactly two scripts: `scripts/tierc12_va.py` (Stage V: series, V2 states and events, regimes,
  traverse, mirror record) and `scripts/tierc12_va_trades.py` (dotted child `TC12-V.trades`: the Tier-E
  two-trades tables and their nulls — the only place the V2 machine is run on scheduled or permuted boxes).
  They are the only non-fixture modules that import `analytics.value_area` or `analytics.profile`. A door
  writes Stage V tables and collared Tier-E tables only; it never writes under `regbooks/`, files no order,
  gate or score, and is imported by no other module.
- `scripts/tierc12_va_stamps.py` is NOT a door: it is the data-only READER of the door's filed tables
  (`bars`, `events`, `regimes`, `instants_of`, `stamp`, `licence`, `traverse`), each read sha-asserted against
  Stage V's progress record. It recomputes nothing. `traverse(name)` is the fitted-pin door BLD-16 asks for.
- Every other `scripts/tierc12_*.py` is a DECISION module with no exemption. RUNNERS_T, ACCESSORS_T,
  NEVER_RUNNER_T and the accessor law are deleted everywhere. No decision module carries a copy of the V2
  machine (L-R.29's box machine moves into `tierc12_va_trades.py`; L-R keeps the table's definition).
- CUT-TAPE LEGS: no suite outside Stage V imports or spawns a door. Stage V's suite owns PREFIX IDENTITY (a
  filed row at bar k equals a rebuild on tapes cut at close_k, at seeded cuts and at the era cut). Every
  downstream as-of leg cuts the FILED tables by `known_close_ms ≤ cut` and leans on that identity.
- The closure fixture asserts the static import graph AND, at the exit of every stage builder process, that
  neither `analytics.value_area` nor a door is in `sys.modules` (plant: a door import inside a function body).

**OD-3 THE 1w LENS** (FID-05, FID-06, CAU-01, CAU-02, BLD-08, CMP-05, TRD-06; O-28). L-R.27's 1d rows take
the same eight-cell partition with U = 1w, read at the last 1w bar closed ≤ τ; every such row carries
`u_lookback_label = "BORROWED: the 1d pin's bar count; X pins no 1w lookback"`. L-0.25 and F-NOT's 1W leg
allow exactly two reads (the V5 stamp columns; that conditioning axis), both Tier-E, typed by (module, table).

**OD-4 PINS THAT MOVED AT R0** (FID-03, BLD-02, CMP-01). A path recorded by more than one stage is governed by
its LAST record; an earlier record is held to the blob at the commit that closed its own stage.
`ORCHESTRATOR_RULINGS.md` and `DISCLOSURES.md` are APPEND-ONLY until the TC12-REG commit (R0's bytes must be a
byte-prefix), then byte-frozen at the shas `REGISTRATIONS.json` names. The TC12-LEANS progress record
re-records the rulings and `X_REC_MANIFEST.json` at their current shas (the orchestrator writes it at freeze).

**OD-5 THE REGBOOK WRITER** (FID-04, BLD-05, CMP-02). `scripts/tierc12_tables.py` owns two writers: `put`
(the 6-dp table writer through `TB.write_table`, stamps + collar) and `put_regbook` (FULL FLOAT, no rounding,
key asserted unique, mergesort on the key, stamps, collar unless the arm is registered, HALT unless the
directory resolves under `regbooks/`). L-0.13 owns the law; L-X.24/25 and the stage sections cite it.

**OD-6 THE FILL LADDER IS PER ORDER** (BLD-06, TRD-02, STA-04, FID-10; O-32). On each arm's own order ledger
`n_filled_touch ≥ n_filled_tick ≥ n_filled_deep`, else HALT. Book totals across the three separately
sequenced walks are printed and are not a theorem; no HALT on them.

**OD-7 STAGES** (BLD-09, CMP-06, FID-12, BLD-10, CMP-08, FID-11, CMP-09; O-31). The referee and the shim are
`TC12-ENV.vendor`, after TC12-D. The instant stamps are Stage V tables filed by the reader under dotted
children `TC12-V.stamps.c` (after TC12-C), `.r` (after TC12-R), `.s` (after TC12-S), at
`va/stamps/VA_STAMPS_<book>.parquet`; no book builder stamps its own book. A dotted child may depend on a
stage later than its parent; its record names `depends_on`, which the quarantine rule follows. The reconciler
writes the one SUB-STAGE LAW (ids, records, gates, resume point) into L-0.10 and every section conforms.

## The range trades

**OD-8 ONE GEOMETRY LAW FOR BOTH RANGE ROWS** (FID-07, TRD-03, CMP-25). With e the entry (4h close for
P-SFP-VA-1; the limit for P-SCALP-3) and d the direction: REFUSED and counted iff (1) `stop_none`;
(2) `d·(T1 − e) ≤ 0` (`poc_not_ahead`: the contract's "toward the POC" has no object); (3) `d·(T2 − e) ≤ 0`
(`t2_not_ahead`). NOT refusals: a T1 within the fee band of the entry is traded as written and flagged; when
`d·(T2 − T1) ≤ 0` T1 is VOID and the whole position exits at T2 (counted). There is no fee band and no
inverted-targets refusal: the contract's only skip is "rr-min". X's geometry law is kept, by a declared
switch, only where a fixture mirrors X's filed rows, and is printed as a Tier-E twin on P-SFP-VA-1.

**OD-9 ONE GAP LAW, THE PESSIMISTIC ONE** (TRD-01, CMP-25). In both simulators a bar that OPENS at or beyond
the stop exits at the OPEN (the worse price); otherwise the stop fills at the stop and is tested before any
target; a target fills at its LEVEL with no gap improvement. On P-SFP-VA-1 the targets are touch-triggered
taker exits booked at their level. X's record law (stop at the stop through a gap, targets collect the gap)
is run by a declared switch against X's filed rows in the mirror leg and printed as a Tier-E twin.

**OD-10 FUNDING IS NOT CAPPED** (TRD-04). The D12 funding ceiling is a v6-card accounting rule. P-SFP-VA-1
and P-SCALP-3 book funding uncapped.

**OD-11 ONE FILL RULE FOR MAKER LEGS** (TRD-05). P-SFP-VA-1's maker twin fills by the tier's fill of record
(through by one tick, exact tick arithmetic), not by X's tick-less strict trade-through.

**OD-12 P-SCALP-3 HAS ONE PRECONDITION** (FID-08, STA-02, CMP-21, BLD-15; O-17). The mirrored licence word
(1h maker, holdout row) and nothing else. The licence edge re-expressed at Stage D's pinned maker rate is
PRINTED beside the word and decides nothing.

**OD-13 THE KILL TABLE** (FID-14, STA-06). The table stands: TICK and DEEP fail with TOUCH clearing reads
`NOT SUPPORTED — CLOSED`; all three failing reads `NOT SUPPORTED — CLOSED FOR GOOD`. A closure word needs a
MEASURED failure (a book whose ruler is undefined is not a failed book). The verdict text carries the two
booleans `fails_under_deep_too` and `clears_only_under_touch`, and the choice is listed for the operator.

**OD-14 THE STRIP IS FOR EVERY RIDDEN ARM** (CMP-20; O-9 as written). Each ridden arm of every row prints its
strip rows under an `arm` column; counts and a pointer, no statistic.

**OD-15 THE TRAVERSE** (FID-13). T of record uses the regime reading as drafted; the contract's phrase read
strictly (every bar of the leg INSIDE) is a printed twin per lens and enters no book.

## Statistics, records, close

**OD-16** (STA-03) A refile never drops a verdict: superseded leaves go to an append-only
`scores/SUPERSEDED.jsonl`. (STA-05) The REFUSAL-SPREAD qualifier is filed on every two-sample row, count-only,
before any outcome is read; the word stays NOT SUPPORTED with the test spent. (STA-08) The five-cluster size
footnote is printed on all five rows. (STA-09) The row set of any later forward score is fixed now in the
fourth book's spec. (STA-10) Selection-hazard rows print key-overlap counts, no outcome.

**OD-17** (CMP-11) A fixture whose population is the book of a registration closed by precondition runs its
synthetic legs and prints `CLOSED-NO-BOOK <id>` for real-book legs, asserting the STATUS record. (CMP-13,
BLD-28) `NOT RUN` is a third leg state, never counted as PASS; an online leg is never part of a transcript of
record. (BLD-22, CMP-12) One hand-sample law for short or empty populations, written once in L-0.14.

**OD-18** (CMP-17) The report's whole-versus-pointed map is frozen now as the finding gives it; a grid printed
whole in its stage document may be pointed to. (FID-15) `close_acts.sh` is generated from a template module
that holds only its text; the only executions are `bash -n` and runs of a SCRATCH COPY in a sandbox clone
against a local bare origin, cut before publish; the file in the main tree is never executed by the executor.
(CMP-19) F-NOT gains the LICENCE leg. (CMP-07) L-L's ferry list is completed from every section's declared
tables at assembly. (CMP-24) The drafters' and reviewers' disclosures a verdict reader needs are appended to
`DISCLOSURES.md` as D-5… by the assembler.

**OD-19 OPERATOR ITEMS ADDED** (FID-14, FID-20): the CLOSED / CLOSED FOR GOOD choice in the both-clauses cell;
the dead else-clause of the scalper's stop (with the stop measured from the limit at the edge, "0.5 ATR_1h
beyond the edge" is always inside the 1.0 ATR_1h rail, so every cross-triggered order has R = 1.0·ATR_1h).
