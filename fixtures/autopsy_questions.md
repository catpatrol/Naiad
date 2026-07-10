# Autopsy question list — the journal schema is derived from THIS (charter §8)

Every question below maps to named journal columns. F8 fails the build if any
question is unmapped or any mapped column is dead (always null / always zero /
type-trapped) in the dry-run autopsy journal. Field definitions and unit
conventions live in the docstrings of `engine/journal.py` and
`engine/shadows.py`; per-unit R vs campaign-R (`realized_r`, sized by
`size_r`) is the one distinction to keep straight when answering.

Event rows referenced: REGIME, STAGE, TAG, PRIME, CONFIRM, V, TPW, CLUSTER,
X, REJECT, ENTRY_FILL, ADD_FILL, STOP_FILL, EXIT, HALT.

## Loss anatomy (charter seeds)

**Q1. Where does the loss live by cohort** (NEVER_GREEN ≤0 · STILLBORN <0.5R ·
FADED 0.5–1R · PROTECTED ≥1R)?
Columns: `EXIT.cohort`, `EXIT.realized_r`, `EXIT.size_r`, `EXIT.mfe_r`.

**Q2. What are the entry set's MFE/MAE distributions** per cell, grade, zone,
tier, and `retr` band?
Columns: `EXIT.mfe_r`, `EXIT.mae_r` × `cell_id`, `grade`, `zone`, `tier`,
`retr`.

**Q3. What fraction of trades die before each candidate harvest mechanism
engages** (pre-engagement death share — the X0 lesson)?
Columns: `EXIT.engagement_flags.xa_engaged_before_exit`,
`.tpw_before_exit`, `.ext_before_exit`, `EXIT.exit_reason`, `EXIT.cohort`.

**Q4. What is each exit's capture ratio** (realized ÷ MFE)?
Columns: per-unit realized = `EXIT.mfe_r − EXIT.give_back_r`; incumbent
capture = that ÷ `EXIT.mfe_r`; candidates = `shadow.exit_XA..XD` ÷ `mfe_r`.

**Q5. What is each exit's tail capture** (of trades with MFE > 5R, share
realized above 3R) — the line that outranks give-back in every exit report?
Columns: `EXIT.mfe_r`, `EXIT.give_back_r`, `shadow.exit_XA`, `exit_XB`,
`exit_XC`, `exit_XD`.

**Q6. Did volatility expand between ratchet and exit on stopped winners, and
what did post-exit continuation do** (the never-loosen/vol-expansion
question)?
Columns: `ENTRY_FILL.atr_exec` (entry), last in-campaign
`PRIME/CONFIRM/V.atr_exec` before exit (ATR at final ratchet — join on
campaign/time), `EXIT.atr_exec` (exit), `EXIT.postexit_cont_1/5/20`,
`EXIT.cohort`.

**Q7. Per tranche: did adds improve or worsen campaign outcomes vs both
sizing shadows?**
Columns: `EXIT.tranche_id`, `rc`, `size_r`, `realized_r`,
`shadow.size_full_r1`, `shadow.size_big_adds`.

**Q8. What did every shadow line return on identical data?**
Columns: `shadow.entry_alt_px`, `entry_alt_t`, `entry_alt_stop`,
`shadow.ladder_strict`, `ladder_unthrottled_grade`,
`ladder_unthrottled_size_r`, `stop_alt_anchor`, `stop_alt_anchor_exit_r`,
`stop_alt_volbuf`, `stop_alt_volbuf_exit_r`, `size_full_r1`,
`size_big_adds`, `exit_XA`, `exit_XB`, `exit_XC`, `exit_XD`.

## Entry quality

**Q9. How much open profit does the survival stop surrender vs each
candidate exit** (give-back by variant)?
Columns: `EXIT.give_back_r`, `shadow.exit_XA..XD`, `EXIT.mfe_r`.

**Q10. What share of PRIMEs converted to fills, and what blocked the rest**
(the funnel)?
Columns: `PRIME` rows vs `ENTRY_FILL/ADD_FILL` rows (join on ts+1 bar),
`REJECT.reject_reason`, `REJECT.tranche_id` (gate family subkey).

**Q11. What is the reject-reason mix by gate** (zone, structure, bar-range,
ribbon, cooldown, C-gate, halt, add-ineligibility, tranche cap, risk cap)?
Columns: `REJECT.reject_reason`, `REJECT.tranche_id`, `REJECT.zone`, `dir`.

**Q12. What is expectancy by zone at equal grade** (is Z3 > Z2 > Z1 real)?
Columns: `EXIT.zone` × `grade` × `realized_r`, `size_r`, `tier`.

**Q13. The sniper-pocket question: what is the winning-depth distribution —
expectancy by `retr` band, from ALL entries, not just winners?**
Columns: `PRIME.retr` (every PRIME journals it), `EXIT.retr`,
`EXIT.realized_r`, `EXIT.mfe_r`, `grade`.

**Q14. What does the provisional throttle cost and save** (B-cap, half size
vs the uncapped counterfactual)?
Columns: `EXIT.tier`, `realized_r`, `shadow.ladder_unthrottled_grade`,
`shadow.ladder_unthrottled_size_r`, `grade` vs shadow grade.

**Q15. Which fills would v11.0.0 strictness have skipped, and what did they
return** (the tiered-arming trade-off, May-26 vs Jun-14 archetypes)?
Columns: `shadow.ladder_strict` × `EXIT.realized_r`, `tier`, `ts_open`.

**Q16. How do entries before vs after a mid-campaign stage confirm perform**
(upgrade dynamics)?
Columns: `STAGE` rows (timing), `ENTRY/ADD_FILL.stage`, `tier`,
`EXIT.realized_r`.

**Q17. How often do gated C-entries fire, and in what context** (probation
bookkeeping; outcome simulation is Phase 2, re-fetching candles against the
journaled `px_signal`/`stop`)?
Columns: `CONFIRM` rows with `grade="C"` (`zone`, `stage`, `tier`,
`px_signal`, `stop`), `REJECT` rows with `reject_reason=c_gate_*`.

## Risk rails and costs

**Q18. How often do halts fire, at which scope, and what loss sequences
precede them?**
Columns: `HALT` rows (`tranche_id`=scope, `size_r`=R total,
`reject_reason`=calendar key), preceding `EXIT.realized_r` sequence,
`REJECT.reject_reason=halted_day/halted_week`.

**Q19. What share of gross PnL goes to fees, slippage, and funding, per cell
and tier — and on what notional?**
Columns: `EXIT.fees`, `EXIT.slippage`, `EXIT.funding_cum`, `EXIT.pnl_usd`,
`EXIT.qty`, `px_fill`, `cell_id`, `tier`.

**Q20. After stop exits, does price continue favorably (re-entry evidence)
or confirm the exit** at +1/+5/+20 bars?
Columns: `EXIT.postexit_cont_1`, `postexit_cont_5`, `postexit_cont_20` ×
`exit_reason`, `cohort`.

## Signals and telemetry

**Q21. How often does Capitulation V fire, in what context, and what do
V-born campaigns return?**
Columns: `V` rows, `ENTRY_FILL.grade="V"`, linked `EXIT.realized_r`,
`tier`, `stage`.

**Q22. Does banking at TPW improve capture** (TPW as exit input)?
Columns: `TPW` rows, `shadow.exit_XB` vs `shadow.exit_XA`,
`engagement_flags.tpw_before_exit`, `EXIT.give_back_r`.

**Q23. What is time-in-trade by cohort** (the aging-rule question Prometheus
left open)?
Columns: `ENTRY/ADD_FILL.ts_open` vs `EXIT.ts_open` per `tranche_id`,
`EXIT.cohort`, `exit_reason`.

**Q24. Do whipsaw-suppressed arrows mark worse campaigns** (filter value)?
Columns: `REGIME.engagement_flags.arrow_visible`, `tier`, subsequent
`EXIT.realized_r` per campaign.

**Q25. What does the per-cell equity trajectory and drawdown look like?**
Columns: `EXIT.equity_after`, `EXIT.ts_open`, `pnl_usd`, `cell_id`.

**Q26. How far are stops at entry (in exec/governor ATR and in price), and
does initial stop distance predict outcome** (the birth-structural-stop
lever)?
Columns: `ENTRY/ADD_FILL.stop`, `px_fill`, `atr_exec`, `atr_gov`, linked
`EXIT.realized_r`, `mae_r`, `cohort`, and `shadow.stop_alt_anchor`,
`stop_alt_anchor_exit_r`, `stop_alt_volbuf`, `stop_alt_volbuf_exit_r` for
the two pre-registered anchor variants.

---

*26 questions; every column named above exists in `engine/journal.py`
MIN_FIELDS / SHADOW_FIELDS. F8 (fixtures/test_f8_journal.py) parses this file,
extracts every mapped column, and fails on unmapped questions, unknown
columns, or dead columns in the dry-run journal.*
