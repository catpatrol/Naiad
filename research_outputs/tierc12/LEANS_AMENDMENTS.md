# TIER-C12 · AMENDMENTS OF RECORD to LEANS

The readings of record are `research_outputs/tierc12/LEANS.md`, frozen at the `tierc12(TC12-LEANS)` commit; the registry
filed at TC12-REG pins its sha. That file is never edited again (O-35). Each change is filed here as a dated AMENDMENT
with its reason, ruled by the orchestrator on a proposal in `AMENDMENTS_PROPOSED.md` — except AM-1, which is the
contract's own order and has no proposal. An amendment is never chosen on an outcome number, and it may never change a
registered row's population, arms, statistic, verdict rule or labels: that is a re-registration, visible to the
operator, with the earlier payload and any number computed under it kept beside. Every artifact an amendment touches
is redone. Heading grammar and sources: L-0.5 (CANON-34).

---

## AM-1 · 2026-10-09 (~18:10Z) · L-V.9..L-V.15 · contract :32-33 (no AP) · AM-V2

**Text amended.** The contract's V2 (:32-37) as it bears on "X's semantics asserted equal on the 4h holdout sample,
amendments dated if they differ" (:32-33); readings L-V.9 to L-V.15.

**Amended to.** TC12's value-area machine is the contract's V2 and differs from TC11-X's machine of record in two fields. (1) Acceptance: X's record accepts on the 8th consecutive close strictly beyond the frozen edge only; V2 also accepts on one close at or beyond 1.5·ATR_L of the same bar beyond the edge, the probe's first bar included — X's `die_parity` twin. (2) The swing-failure return window: X's record is t − t0 ≤ 7; V2 is t − t0 ≤ 3 — X's `k3` twin. V2 therefore has an outcome X's record cannot reach, the LAPSE (a return on closes 4..7), which is neither a swing failure nor an acceptance and feeds no trade. X never ran the two fields together; V2 equals X's filed `die_parity` stream with returns of bars_out > 3 relabelled lapse, held by F-STATE-X on the 4h holdout and on every other lens and era. Everything else is X's law unchanged: each idle close judged against VA(t−1); the edge frozen at the probe's first close and every pending close judged against it; decay on the first idle close inside the rolling VA(t−1); one resolution per bar. Declared against the contract's letter: (i) a close while a probe is pending is judged against that probe's frozen edge, not against the rolling VA(t−1); (ii) on a bar that resolves a probe the state is INSIDE by the frozen edge even where the close lies outside the rolling VA(t−1), counted per cell and filed per bar as `inside_frozen_only`. New in TC12 with no X counterpart: the per-bar state column, the signed edge distance, the POC distance, the VA age column, the value-area traverse, the lens-ladder coincidence, the 1w block on a borrowed lookback. The feasibility words that license the range trades (F-VA-MIRROR) were earned on X's record machine, not on V2; they are read, not re-earned (DISCLOSURES D-2).

**Reason.** The contract's own order (:33) and ruling O-16 (c): the contract's V2 is not the machine TC11-X filed of
record, so the difference is dated here, before any value-area table exists. Source (iv) of L-0.5; no outcome exists.

**Redone.** Nothing: no artifact exists at the freeze.

---

## AM-2 · 2026-10-09 (~21:40Z) · L-X.36 · ruling on AP-1

**Text amended.** L-X.36's quoted common sentence as a contiguous block in every payload's `verdict_rule`.

**Amended to.** RULER-TEXT holds: (1) squeeze(verdict_rule) starts with the ruler sentence; (2) exactly one 'Printed beside, deciding nothing:' mark, followed by 'Tier-E arms carry no verdict word.', and each of the ten common items is a substring of the span between them; (3) the `comparison` field opens with 'two-sample vs v6' or 'vs zero' and the contract's text slice or its family header reads the same words; (4) the rule states N_BOOT and both seeds. GREEN on the five rows; the plant 'vs zero struck from P-SFP-VA-1's slice' is caught.

**Reason.** AP-1's default, ruled as the registry builder built it. Mechanics of a text detector only: no registered
row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the registry was filed under this default.

---

## AM-3 · 2026-10-09 (~21:40Z) · L-0.14, L-0.4, L-0.11, L-0.19 · ruling on AP-2

**Text amended.** resume paste "tier-e-never-halts" (O-36) vs L-0.14 C and F-FX-FORM; L-0.4 (3), L-0.11, L-0.19 — NOT BUILT is counted beside C's tally, not inside it

**Amended to.** The paste governs. `not_built(fid, title, reason)` prints the header and ` [NOT BUILT] <fid>: <reason>`; it is lawful only for the FIDs F-GRID and F-KEY, any other reads FAIL. C's tally line is unchanged and legs_total = GREEN + RED + NOT RUN. NOT BUILT is counted on one more line ` J NOT BUILT` (printed only when J > 0, followed by one ` NOT BUILT: <block id>` line each) and in summary()['legs_not_built']; the exit code is unaffected. NOT SETTLED HERE, for the orchestrator: (a) F-FX-FORM must accept a NOT BUILT block as exactly its header and its line; (b) L-0.19's roll says a contract name is PASS only if every block of its FID is PASS, so F-ROLL needs a rule for a NOT BUILT F-GRID / F-KEY block; (c) the progress record's key list (L-0.9) has no legs_not_built.

**Reason.** A build fact met by unit A at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-4 · 2026-10-09 (~21:40Z) · L-0.20, L-0.14, L-0.22 · ruling on AP-3

**Text amended.** L-0.20 and L-0.14 (helper legs in tierc12_fx.py) vs L-0.22 points 1, 4, legs (ii) and (iv) — F-DET's helper leg holds no subprocess site; the calling suite launches the twins

**Amended to.** The pessimistic reading: the harness imports no subprocess and calls no exec / eval / compile. `det_twins(launch, directory, stage, seed)` takes the SUITE's launcher (the suite owns the fresh subprocess under PYTHONHASHSEED and returns an exit code or a handle with .wait()); the harness removes stale twin directories, labels the twins and does every comparison of L-0.20. The self-test plants by swapping an object in the production call path and by mutated text copies judged by AST — both lawful forms under L-0.14.

**Reason.** A build fact met by unit A at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-5 · 2026-10-09 (~21:40Z) · L-0.14 · ruling on AP-4

**Text amended.** L-0.14 seam 3 and C; F-FX-FORM; L-D (F-TOLL [data a..g], leg (d)) — NOT_RUN_FIDS_T holds whole block ids

**Amended to.** NOT_RUN_FIDS_T = ("F-MIRROR", "F-TOLL [data d]"), matched on the whole block id and enforced at run time by `not_run`: any other id prints `[FAIL]` and is RED. The closure suite's typed copy should hold the same two strings.

**Reason.** A build fact met by unit A at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-6 · 2026-10-09 (~21:40Z) · L-0.14 · ruling on AP-5

**Text amended.** L-0.14 G — Hand-sample: a category whose first row an earlier category already took

**Amended to.** Non-empty categories take their first rows, in category order, before any FILL is drawn. A category whose first row is already chosen prints `SHARED <category>: …` and its slot is FILLed by the next unchosen row in key order. Slots = max(k, number of categories), capped at n. No size or composition case is RED; only a population that does not hold the count handed in as n_asserted returns a problem.

**Reason.** A build fact met by unit A at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-7 · 2026-10-09 (~21:40Z) · L-0.17 · ruling on AP-6

**Text amended.** L-0.17 (TOTALITY; F-PINS 'a digit run of the operative lines is unaccounted'), CANON-25 point 6 — TOTALITY: which lines of the prefix are 'operative'

**Amended to.** Pessimistic: every line 1..137 of the prefix is operative. A digit run must lie inside exactly one capture (main or `also`, by `group` where given) or exactly one classed token; never both, never neither.

**Reason.** A build fact met by unit B at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-8 · 2026-10-09 (~21:40Z) · L-0.17, L-R.32 · ruling on AP-7

**Text amended.** L-0.17 (PIN NAMES OF RECORD), CANON-25 point 3, L-R.32 — two_trades.horizons is cited at :79; the token stands on :78

**Amended to.** Map row `two_trades.horizons` lines [78, 78], regex `H(\d+)/H(\d+) net of`, value (20, 100). Every other cited line was built as cited and parses.

**Reason.** A build fact met by unit B at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-9 · 2026-10-09 (~21:40Z) · L-0.17, L-0.18, L-X.1, L-0.14 · ruling on AP-8

**Text amended.** L-0.17 (F-PINS: 'the text of the filed registry … checked at filing'), L-0.18 (F-FAM-PINS: 'a payload of the filed registry'), L-X.1 ('on disk before --file runs'), L-0.14 C / seam 3 — The registry clauses of F-PINS and F-FAM-PINS before the registry exists

**Amended to.** Literal reading: the clauses assert on registrations/REGISTRATIONS.json when it is on file (families[] and every payload's family, family_m, family_bar; the nine stamp-set shas absent from its text). When it is not, each REAL leg prints `registry: NOT ON FILE — the registry clause asserts nothing at this run` and passes on its other clauses. BREAK plants run on the filed registry if present, else on a document built in L-X.19's keys. Consequence: the filed transcript is the pre-registry one and must be re-filed once with --refile-transcript after the registry lands.

**Reason.** A build fact met by unit B at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-10 · 2026-10-09 (~21:40Z) · L-0.23, L-0.5 · ruling on AP-9

**Text amended.** L-0.23 (EFFECT BY TIMING; F-VETO clause 4), L-0.5 (heading form) — How an operator veto files a substituted pin value, and what counts as 'an operator quote'

**Amended to.** A pin is changed by a body line `PIN <name> := <value> [<value> …]` (one value per capture group, parsed by the row's types). The heading's basis must be `operator veto "<token>"` with <token> equal to that pin's register `veto`; the body must hold a line where the word `operator` is followed by a double-quoted string (the heading does not count). Otherwise VETO-AMENDMENT. load() overlays the last substitution on a contract pin; amended() exposes it for x_record / stage_d rows. AM-1 has no PIN line, so nothing is overlaid today.

**Reason.** A build fact met by unit B at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-11 · 2026-10-09 (~21:40Z) · L-0.17, L-0.24 · ruling on AP-10

**Text amended.** L-0.17 (F-PINS), L-0.24 (sets (a)-(f); F-TC11-STAMP (vii)) — F-PINS census-sha clause: which paths are 'L-0.24's sets (a)-(f)' at filing

**Amended to.** The suite types the nine nameable members (STAMP_SETS_T: TC11's REGISTRATIONS.json and REGISTRY_PIN.json, the five set-(c) scripts, scores/REGISTRY_CHECK.json, TC11's PROGRESS.json) and reads each sha from the byte-frozen file. 'Abbreviated' = a hex run of at least 8 characters that is a prefix of the sha (ABBREV_MIN_T). The closed sets remain F-TC11-STAMP (vii)'s at CLOSE.

**Reason.** A build fact met by unit B at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-12 · 2026-10-09 (~21:40Z) · L-0.17, L-V.4, L-0.24 · ruling on AP-11

**Text amended.** L-0.17 (PIN NAMES OF RECORD 'sections use these and no other'; seam 35; the lineage door), L-V.4 (table column 'register row · kind'), L-0.24 point (1) — Register rows that have no name of record

**Amended to.** 20 door-named rows, typed as DOOR_NAMED_T in the suite: lineage.tierc11_score.{REQUIRED, INT_COLS, FLOAT_COLS, STR_COLS, SORT_KEY, HAIRCUT_TOL, SUM_TOL, NET_LAW_TOL, EXIT_FLAGS} (the literals at :248-255, :264-266, :301); lineage.tierc2_rules.ATR_LEN; lineage.tierc5_rules.{WARMUP_BARS, PROVISIONAL_MIN_N}; lineage.tierc10_panel.{N_BOOT, LENS_MS, ERA_CUT_MS}; lineage.analytics_profile.{PROFILE_ROWS, VALUE_AREA}; lineage.tierc2_baseline._round_floats.nd; x.va.laws.{k_draws, dev_return_bars}. Each carries `named_by` and (lineage) a node sha the door re-asserts. The other lineage objects of L-R.32, L-S.2 and L-L's tables have no 'register row' column and carry no row.

**Reason.** A build fact met by unit B at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-13 · 2026-10-09 (~21:40Z) · L-0.17, L-V.4, L-R.32, L-S.2, L-G.3, L-L.8 · ruling on AP-12

**Text amended.** L-0.17 (the contract door; seam 6; seam 45), L-V.4, L-R.32, L-S.2, L-G.3, L-L.8/14/27 — Which 'asserted equal to' comparisons the door makes itself

**Amended to.** Recorded per row as `equal_to` items. By the door (28, PIN-EQUAL): va.accept_n, va.accept_margin_atr, va.sfp_k (member of sfp_k_twins), va.nest_frac, va.value_area_pct and adm.old_quantile (× PCT_PER_UNIT read as text from tierc12_units.py), chop.n_bands (the range argument of DECILES), sfp.rail_atr, sfp.t2_offset_atr, tp1d.approach_atr, two_trades.horizons (X's pins.laws.horizons and tierc10_census HORIZONS), scalp.ema_fast/slow, scalp.stop_beyond_atr, scalp.rail_atr, scalp.t1_fraction, scalp.t2_offset_atr, ledger.opening (ms), ledger.n_min, ferry.cap_mb (× BYTES_PER_MB == CAP_BYTES). By the consumer (21): seed, ctrl.sum_net_r, adm.lag_cut, adm.preseen_cell, adm.abs_cut, brd.cut, the two grid rows, book.trg912_periods, sfp.t1_fraction (CONTROL_CARD.harvest_frac), va.mirror_words, va.licence_set, scalp.era, loao.line and the further objects of the ledger rows.

**Reason.** A build fact met by unit B at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-14 · 2026-10-09 (~21:40Z) · L-0.17 · ruling on AP-13

**Text amended.** L-0.17 (TOTALITY, the class list), CANON-25 point 6, seam 39 — A class beyond the reading's list for two tokens

**Amended to.** A tenth class `index_offset` holding exactly those two tokens; the suite types the count per class.

**Reason.** A build fact met by unit B at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-15 · 2026-10-09 (~21:40Z) · L-0.17, L-0.19, L-0.18 · ruling on AP-14

**Text amended.** L-0.17 (THE FLOW LEG; F-TYPED-TOTAL), L-0.19 seam 2, L-0.18, resume paste RC-2 — Where the family pins' flow bends are hosted

**Amended to.** No new block. F-FAM-PINS's REAL leg bends each of the four at the door (families() must HALT FAMILY-BAR, per seam 45) and prints the four [FLOW] lines; its BREAK leg plants a shadow copy of the door holding a typed 1/10 in place of fam.q, caught as PIN-NOT-READ.

**Reason.** A build fact met by unit B at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-16 · 2026-10-09 (~21:40Z) · L-0.3, L-0.4, L-0.9, L-0.10, L-0.14, L-X.21 · ruling on AP-15

**Text amended.** L-0.3, L-0.4, L-0.9 (the gate, steps 1-6), L-0.10 point 4, L-0.14 I, L-X.21 (REG_SET) — The gate form of the resume transcript: it cannot print the gate's own record and stay byte-identical

**Amended to.** The transcript carries only facts fixed at the gate: git read at --at; the records BEFORE --stage in RESUME_ORDER (each must be COMPLETE-VERIFIED, else GATE-ORDER RED); the resume point 'at this gate' (the gate's id when all before it verify). The gate's own record, and what its commit will add (the registry's pins, its transcripts), are verified WHEN ON FILE and are mandatory from the next gate on; no printed count or name moves with the gate's record, a later record or a later commit. The LIVE ledger and resume point over every record on disk go to stdout only (the suite, and tierc12_progress.py). Checked on a scratch estate: filing run, gate re-run and later sweep give identical PASS lines on all nine repo legs.

**Reason.** A build fact met by unit C at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-17 · 2026-10-09 (~21:40Z) · L-0.4, L-0.5 · ruling on AP-16

**Text amended.** L-0.4 (1), L-0.5 — L-0.4 (1) before the gate's record exists: the path a gate lawfully re-records

**Amended to.** Typed RERECORDED (tierc12_progress.py data, second copy RERECORDED_T in the fixture): scripts/tierc12_progress.py [TC12-R0, TC12-REG]; ferry/FERRY_MANIFEST.json [TC12-L, TC12-CLOSE]; va/stamps/build_manifest.json [the three stamps children]. While the NEXT named recorder is not on file, a differing working file is that record's to pin and the earlier entry is still held to the blob at its closing commit. An append-only path that grew is lawful iff the last entry's bytes are a byte-prefix of the working file. Anything else stays a moved artifact — including an UNTRACKED path a gate supersedes: for such a gate the record (with its supersedes entry) must be on file before the resume suite's filing run.

**Reason.** A build fact met by unit C at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-18 · 2026-10-09 (~21:40Z) · L-0.8, L-0.9 · ruling on AP-17

**Text amended.** L-0.8, L-0.9; the resume paste (STEP Q); O-36 — F-OFFBUS / F-COMMIT: the resume paste's own STEP Q commit files a second text under exchange/queue/

**Amended to.** The paste governs (O-36): STEP_Q_PATHS_T = (the contract, the resume paste) — the two queue texts a commit whose parsed id is STEP Q may file. Every other path under exchange/ in a tierc12( commit stays RED.

**Reason.** A build fact met by unit C at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-19 · 2026-10-09 (~21:40Z) · L-0.5, L-X.20 · ruling on AP-18

**Text amended.** L-0.5 (planted mutations), L-X.20 (F-REG [WRITE-ONCE]) — F-FROZEN-TEXT: the registry filer's write-once HALT is not planted in the resume suite

**Amended to.** F-FROZEN-TEXT holds write-once by its stated failure condition — more than one commit in range touches a write-once file, or the working file is not the blob that filed it — with a planted second blob in a scratch repository (detector WRITE-ONCE). The filer's own HALT stays the registry suite's plant; the BREAK line of the transcript says so.

**Reason.** A build fact met by unit C at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-20 · 2026-10-09 (~21:40Z) · L-0.5, L-0.12 · ruling on AP-19

**Text amended.** L-0.5, L-0.12 — F-FROZEN-TEXT (e): which record is 'the review record's last-pass sha' for LEANS.md

**Amended to.** ONE value is required of: sha256(LEANS.md), the TC12-LEANS record's entry, the attestation header's frozen.sha256, and — when on file at the TC12-REG gate, mandatory after it — REGISTRATIONS.json leans.sha256 and REGISTRY_PIN.json's leans pin (read as `leans_sha256` or `leans.sha256`).

**Reason.** A build fact met by unit C at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-21 · 2026-10-09 (~21:40Z) · L-0.10 · ruling on AP-20

**Text amended.** L-0.10 (T6, T7) — F-ORDER T6 has no machine-readable link from an amendment to the artifact it changes

**Amended to.** T6 is checked where T7 is: when a tierc12( commit changes a regbook manifest's `sha` map, every AM-n id in that record's notes must have its heading in LEANS_AMENDMENTS.md at a commit that is a proper ancestor of the rebuilding commit; an AP-n id must be in the notes (T7). At TC12-REG both print their pre-registry form.

**Reason.** A build fact met by unit C at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-22 · 2026-10-09 (~21:40Z) · L-0.6 · ruling on AP-21

**Text amended.** L-0.6 — The census holds Finder metadata under a census root

**Amended to.** Built as written (the pessimistic reading): .DS_Store is in the census like any other file and a change to it is FROZEN-CHANGED. If the orchestrator prefers a typed exclusion of that one name, it is a one-line change in tierc12_frozen.estate() plus a re-pinned census (--write --k=1).

**Reason.** A build fact met by unit C at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-23 · 2026-10-09 (~21:40Z) · L-0.6, L-0.24, L-X.34 · ruling on AP-22

**Text amended.** L-0.6, L-0.24, L-X.34 — The keys of close/TC11_STAMP_MAP.json that F-FROZEN's one typed acceptance reads

**Amended to.** tierc12_frozen.stamp_accepts reads `applied` (must be true) and `moved: [{path, sha256_before, sha256_after}]`; a path is accepted only if it is the TC11 contract, of typed sets (a), (b), (c), (f), or under research_outputs/tierc11/ (sets d, e as the map lists them), and never one of SCORES.json / FAMILY.json / BASE_IDENT.json. The census records this rule under `stamp_acceptance`.

**Reason.** A build fact met by unit C at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-24 · 2026-10-09 (~21:40Z) · L-X.15, L-0.18, L-0.19 · ruling on AP-23

**Text amended.** L-X.15, L-0.18, L-0.19, L-X hosting table (LEANS.md:7195-7198), CANON-24; resume paste FIXTURES line and RC-2; unit brief D — F-FAM is NOT hosted in the registry suite — CANON-24's hosting taken over the unit brief

**Amended to.** FIXTURES_REG.txt hosts exactly CANON-24's row: F-CONTRACT-PIN, F-REG [SLICE] [HASH] [WRITE-ONCE] [TEMPLATE] [SPEC-VERBATIM] [VERIFIER], F-ATTEST-ORDER [REG] — 8 blocks, no F-FAM block. The registry's half of the law is held inside those legs (PRECOND-GRAMMAR plants: a precondition in prose, a numeric `required`; preconditions_of() returns 0/0/0/2/1 items; family, m and bar per payload) and by Unit B's F-FAM-PINS, which I ran into a scratch --root against the filed registry: GREEN, '5 payloads carry the parse's family, m and bar'. If the orchestrator rules an F-FAM instance must stand at TC12-REG it is an added leg to this suite plus a transcript refile; the registry files do not move.

**Reason.** A build fact met by unit D at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-25 · 2026-10-09 (~21:40Z) · L-X.18 · ruling on AP-24

**Text amended.** L-X.18 (block = heading to the next line beginning '### ' or '## '; carry law: fifteen top-level bullets, any other field HALTs) — A spec block's byte-for-byte boundary includes the frozen text's blank lines and section rule

**Amended to.** The plan carries every line after the heading byte for byte (the plan's own heading is '### 1.k <id>'; PLAN==LEANS compares the bodies). The carry law drops leading and trailing blank lines and a trailing all-hyphen rule line and HALTs SPEC-GRAMMAR on any other line that is no bullet and no wrapped line. Stated in REGISTRY_PIN.json's spec_carry_law.

**Reason.** A build fact met by unit D at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-26 · 2026-10-09 (~21:40Z) · L-X.18, L-X.19 · ruling on AP-25

**Text amended.** L-X.18 carry law ('one level of sub-bullets becomes a list'), L-X.19 ('a field written with sub-bullets is a LIST') — A field written with a head sentence AND sub-bullets is filed {text, items}

**Amended to.** X's carry_spec mirrored (the precedent L-X.18 names): head only -> string; sub-bullets only -> list; head and sub-bullets -> {"text": head, "items": [...]}. `arms` and `labels` must be lists (SPEC-GRAMMAR otherwise); no word is dropped (the suite's word-level oracle holds every filed leaf to the words of its LEANS field). Consumers of disclosed_beside / failure_conditions must accept all three shapes.

**Reason.** A build fact met by unit D at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-27 · 2026-10-09 (~21:40Z) · the resume paste and O-36 · ruling on AP-26

**Text amended.** L-X common clauses under '### REGISTRATION SPEC · (none owned by L-X)' (LEANS.md:7256-7258); AP-1 — 'The filing asserts the rule states the parsed q, m and bar' cannot be built on two rows

**Amended to.** On verdict_rule the filing asserts N_BOOT (4000), the seed (20261008), the sensitivity seed (20260816) — detector RULER-TEXT — and the one template (TEMPLATE). m and the bar are asserted on the block's checked fields family_m / family_bar against the pin door's parse (FAMILY-M-COUNT, FAMILY-BAR). q is not asserted in the rule text. All five rows pass as written.

**Reason.** A build fact met by unit D at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-28 · 2026-10-09 (~21:40Z) · L-X.21, L-X.20 · ruling on AP-27

**Text amended.** L-X.21 clause 3 (ATTEST-REG), L-X.20 (the commit ADDS REG_SET, MODIFIES tierc12_progress.py and PROGRESS.json); unit brief D — ATTEST-REG: what 'the listing of every file then on disk' can mean at a gate that writes after it

**Amended to.** `--attest` lists exactly what it sees and HALTs ATTEST-REG (writing nothing) on a file outside PRE_REG ∪ REG_SET, a .parquet outside x_rec/, a tierc12 script outside the typed set, or an unfiled registry; REG_SET members not on disk are listed under `absent` (now: progress/TC12-REG.json). It is re-runnable (not write-once). F-ATTEST-ORDER [REG] holds the set law on the live disk with no exemption, and listing == disk outside seven typed paths LATER_T (the four TC12-REG transcripts, progress/TC12-REG.json, PROGRESS.json, scripts/tierc12_progress.py). Any other file edited or added after the attestation is RED until --attest is re-run.

**Reason.** A build fact met by unit D at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-29 · 2026-10-09 (~21:40Z) · L-X.19, L-X.20, L-X.22 · ruling on AP-28

**Text amended.** L-X.19 (top keys 'in this order'), L-X.20 (pin keys), L-X.22 (verify_filing signature); unit brief D ('the resume paste (as `resume_paste`)') — Keys and signatures beyond L-X.19 / L-X.20 / L-X.22's lists

**Amended to.** REGISTRATIONS.json gains `resume_paste {path, sha256}` directly after `contract` (L-X.19's other keys keep their order); REGISTRY_PIN.json gains `resume_paste` and `tier`. verify_filing keeps the seven positional parameters and adds keyword `door=None` (default: the tree's pin door); it writes the handed contract bytes to a scratch file under $TMPDIR and judges them through a pin door over that file. `verdict_law` and the pin's spec_carry_law / witness_law / text_before_result_law are read verbatim from the plan's §2; each clause of verdict_law is asserted to be a substring of the frozen ruler sentence. At filing only, beyond L-X.22's nineteen detectors: PLAN-TABLE, RECORD-PIN, N-BOOT, LAW-HEAD, PIN-CENSUS-SHA, WRITE-ONCE, ATTEST-REG.

**Reason.** A build fact met by unit D at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-30 · 2026-10-09 (~21:40Z) · L-X.17, L-0.24 · ruling on AP-29

**Text amended.** L-X.17 (external_context, EXTERNAL-SLICE), L-0.24 sets (a)-(f); P-ADM-1 and P-BRD-1 `labels` — external_context: where a block declares it, and which paths are banned

**Amended to.** The filer reads the declaration from the label text by one regex; ranges joined by ' and ' are one item each (P-ADM-1: one item, STAGE_G.md:187-198; P-BRD-1: two items, X4.md:16 and :28). The file's sha is asserted against the declared sha, and a copy under x_rec/ also against its X_REC_MANIFEST row. The banned set is tierc12_frozen.STAMP_SETS_T (TC11's contract and sets a, b, c, f); research_outputs/tierc11/stage_g/STAGE_G.md is taken as HISTORICAL (L-0.24: stage documents are untouched).

**Reason.** A build fact met by unit D at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-31 · 2026-10-09 (~21:40Z) · L-0.11, L-0.9 · ruling on AP-30

**Text amended.** L-0.11 (SCOPE LAW) · L-0.9 (the gate, steps 1-6) — AP-E1 · the closure scope at a stage's own gate, and UNRECORDED

**Amended to.** While the stage's record is absent, the tierc12 scripts (and build manifests / door tables) on disk that NO record names are in scope as the gated record's own; once the record exists the scope is the records' alone. UNRECORDED is printed on stdout only (a clock line), never in the transcript, never RED. Record files with a known filing stage (data/AS_OF_PIN.json, data/CONTRACT_SPECS.json, env/LINEAGE_PINS.json, analytics/value_area.py) are read by STAGE (typed FILED_AT_T), not by disk state. TC12-D.mirror is in no scope. Consequence: a later record's script must not sit unrecorded on disk when an ORDER-stage closure transcript is filed.

**Reason.** A build fact met by unit E at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-32 · 2026-10-09 (~21:40Z) · L-0.14, L-0.9, L-0.11 · ruling on AP-31

**Text amended.** L-0.14 (F-FX-FORM) · L-0.9 (gate order) · L-0.11 — AP-E2 · which transcripts F-FX-FORM reads

**Amended to.** The transcripts scanned are those named by the records strictly BEFORE the stage in RESUME_ORDER_T (a transcript is of record once a record names it); each stage's transcripts are therefore scanned at the next ORDER-stage gate. At TC12-REG the set is empty and printed so; the checker is still proven there on a transcript the harness itself writes in memory (plants and a GREEN control). TC12-CLOSE's own transcripts are scanned by no later run.

**Reason.** A build fact met by unit E at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-33 · 2026-10-09 (~21:40Z) · L-0.17 · ruling on AP-32

**Text amended.** L-0.17 allow-list (A), (C) — AP-E3 · F-TYPED and the unary minus

**Amended to.** The pessimistic reading: `-1`, `-2`, `-1.0` are TYPED-FOLD findings in a computation module (`x[-1]` is RED; `x[len(x) - 1]` passes). No scanned module at TC12-REG trips it (tierc12_pins is clean). If ruled the other way it is one clause of _structural().

**Reason.** A build fact met by unit E at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-34 · 2026-10-09 (~21:40Z) · L-0.22, L-D.1, L-D.23, L-R.24 · ruling on AP-33

**Text amended.** L-0.22 seam 16 · L-D.1 / F-D-PIN [e] · L-D.23 / F-TICK [b] · L-R.24 — AP-E4 · seam 16: the host block, the pin text scan, the tick detector

**Amended to.** Hosted in F-CLOSURE [ii] (detectors PIN-LITERAL, TICK-LITERAL, TICK-FLOAT-COMPARE), over every non-fixture source. Pessimistic tick rule: ANY BinOp with a direct tick-named operand under a Compare is RED, so a consumer forms the depth in a statement of its own before comparing. The pin scan is a raw TEXT scan (comments and docstrings included; ms digits with optional underscores; the ISO instant to the minute). Before TC12-D the referee is O-7's printed value in ORCHESTRATOR_RULINGS.md plus TC11's pin record (TC10's pin from its tc10_pin keys); the tick-literal clause has no referee and says so.

**Reason.** A build fact met by unit E at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-35 · 2026-10-09 (~21:40Z) · L-0.2, L-V.23 · ruling on AP-34

**Text amended.** L-0.2 (F-SEED) · L-V.23 / F-VA-NULL [a] · L-L (tierc12_era.compute) — AP-E5 · F-SEED: the wrapper list, the scope, X_SEED_MIRROR_T's unnamed member

**Amended to.** Wrappers are found by AST — a function with a `seed` parameter whose body calls a ruler or another wrapper — and printed in the transcript; the three lineage rulers must be handed `seed=` by keyword. Scope = every non-fixture GLOB member, process tools included (a suite's default_rng form is F-FX-FORM's). X_SEED_MIRROR_T holds (tierc12_era, compute) only; once tierc12_va_trades is in scope F-SEED is RED until its stream builder's name is typed by a dated amendment (first closure gate after TC12-V.trades: TC12-C).

**Reason.** A build fact met by unit E at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-36 · 2026-10-09 (~21:40Z) · L-0.2 · ruling on AP-35

**Text amended.** L-0.2 (F-SEED; "The sensitivity seed printed beside every ruler is `T5.SEED`") · L-X (the `seed_sens` leaf: "the row's ruler at the sensitivity seed"; `E.SEED_SENS`) — AP-E6 · F-SEED and the sensitivity seed

**Amended to.** Built to the letter: only the pin-door seed (a call on tierc12_pins naming `seed`, or a name bound to one) and `E.SEED` exactly resolve; `seed=E.SEED_SENS` is SEED-UNRESOLVED (planted and printed). The scorer filed at TC12-ENV.score-build will read RED at the TC12-V closure gate unless this is ruled first.

**Reason.** A build fact met by unit E at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-37 · 2026-10-09 (~21:40Z) · L-0.22 · ruling on AP-36

**Text amended.** L-0.22 leg (ii) · its SOURCE line (scripts/tierc11_closure_fixtures.py) — AP-E7 · leg (ii) on the lineage, and what a sys.modules reach is

**Amended to.** The strict clause binds decision sources and doors. For LINEAGE sources TC11's filed law is used: a name-held dynamic import is resolved to the repo modules its literal table names, and a forbidden target or an unresolved site is the finding (dev-run over the real lineage text: 39 modules, no finding). A sys.modules reach is a subscript / get / pop / setdefault with a FORBIDDEN constant key (TC11's form). DYN_DECLARED_T = tierc12_env.tc10_import (L-D.26 hunk 7).

**Reason.** A build fact met by unit E at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-38 · 2026-10-09 (~21:40Z) · L-0.17, L-D.25, L-D.26 · ruling on AP-37

**Text amended.** L-0.17 allow-list (G) · L-D.25 / L-D.26 (the hunks) · L-D F-D-PORT — AP-E8 · F-TYPED rule (G) without the hunk list

**Amended to.** A STATEMENT of a module with a typed referee whose ast.dump equals a statement of the referee's text is the referee's; every other statement is scanned. REFEREES_T today: tierc12_env -> vendor/tierc11_env@1526093b.py, tierc12_data -> scripts/tierc11_data.py. Referees for later ports (era, forward, ferry) are typed when those modules are filed. A statement that changed in one token is scanned whole, so referee literals inside a hunk-touched multi-line statement will read as findings.

**Reason.** A build fact met by unit E at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-39 · 2026-10-09 (~21:40Z) · L-L.3, L-L.5, L-L.18, L-0.22, L-0.17 · ruling on AP-38

**Text amended.** L-L.3, L-L.5, L-L.18 (F-FWD-SPEC AST clause) vs L-0.22 (ii) and its sentence on --stage=TC12-REG; L-0.17 rule (G) — AP-F1 · forward_log imported by the spec tool (L-L) versus the import-closure wall as built (L-0.22 ii)

**Amended to.** The pessimistic reading (the wall holds): tierc12_forward_spec.py does NOT import forward_log. Its six chain functions stand in the module as ports under the section's own port law — canonical, chain_hash, read_lines, append_entry, verify_chain VERBATIM; last_sha CHANGED by the one token `lines[-1]` -> `lines[len(lines) - 1]` — and are exposed as the namespace `FL` so X's ported call sites (chained, append, chain_findings) are unchanged. Every production run HALTs FWD-FL-PORT unless they are AST-identical (under that one declared substitution) to scripts/forward_log.py at the sha X's spec names (74e9657f…1967). The SUITE imports forward_log itself as the independent verifier: F-LEDGER [CHAIN] runs forward_log.verify_chain on every file and requires the port to return forward_log's own result; F-PORT holds every label. No byte of BOOK_SPEC_COMBINED.json or of the ledger depends on the choice. If overruled: the one line `import forward_log as FL` replaces the port block, and the closure suite then needs a forward_log clause (disclosed, not walked).

**Reason.** A build fact met by unit F at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-40 · 2026-10-09 (~21:40Z) · L-L.3, L-0.4, L-0.9 · ruling on AP-39

**Text amended.** L-L.3 (the sha-first reader), L-0.4 (certified HALTs if no record names the path), L-0.9 (the parent record of TC12-REG is written by the orchestrator's gate step) — AP-F2 · "a TC12 file through certified" before the parent record exists

**Amended to.** The two registry files are held at EVERY run by the registry's own pin and chain — REGISTRY_PIN.json `registrations_file` {path, bytes, sha256} must be the file, and the head recomputed from the five payloads must equal the head both files carry (HALT FWD-REGISTRY) — and ALSO through certified() from the moment any progress record names them (a mismatch HALTs FWD-READ). Tested on a scratch root: the spec's bytes are identical with and without a TC12-REG record; a record naming another sha HALTs. The transcript prints nothing that depends on which records exist.

**Reason.** A build fact met by unit F at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-41 · 2026-10-09 (~21:40Z) · L-L.3, L-0.24 · ruling on AP-40

**Text amended.** L-L.3 (SPEC_READS_T; "an X file against its manifest row"; "or at the stamped value L-0.24 allows"), L-0.24 — AP-F3 · SPEC_READS_T omits two files the same reading's sha law opens

**Amended to.** Both paths are typed in SPEC_READS_T (17 typed paths; the 18 lineage files are added by object from X's `path_modules`). The stamp map is read only if on file and accepted only when it reads applied: true and names the bytes (the form tierc12_frozen.py reads: moved[{path, sha256_before, sha256_after}]). The suite types the same list as its second object; a path outside it HALTs SPEC-READS.

**Reason.** A build fact met by unit F at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-42 · 2026-10-09 (~21:40Z) · L-0.17, L-0.19, L-L.18 · ruling on AP-41

**Text amended.** L-0.17 (the flow leg; "the pin's consumer makes it at its own stage, as that pin's flow-leg witness"), L-0.19 seam 2, L-0.17 seam 63, L-L.18 seam 1 and its three F-TYPED-FLOW rows, PIN_REGISTER.json rows ledger.opening / ledger.n_min / seed — AP-F4 · the flow witness of ledger.opening and ledger.n_min at the ledger-spec record

**Amended to.** Three F-TYPED-FLOW blocks are hosted. [adm.lag_cut]: the registered witness moves (p_win_1_refuses flips on the planted lag = CUT − 1 row) and the register's own line is printed. [ledger.opening] and [ledger.n_min]: the pin is bent at its door, production's spec_doc must HALT FWD-OPENING / FWD-NMIN, and the [FLOW] line is printed in L-0.17's form with the witness that actually moved ("the FWD-OPENING assertion of the spec tool (the build HALTs there, L-L.8)", "the FWD-NMIN assertion … L-L.14") — never the register's scratch-ledger sentence, which would be untrue here. Each block's plant is a shadow copy of the spec module holding a typed copy of EQUAL value (PIN-NOT-READ). No F-TYPED-FLOW [seed] block is hosted: nothing is drawn at this record.

**Reason.** A build fact met by unit F at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-43 · 2026-10-09 (~21:40Z) · L-L.8, L-L.3 · ruling on AP-42

**Text amended.** L-L.8, L-L.3 (SPEC_READS_T; no env) — AP-F5 · FWD-OPENING at the spec stage: the two TC10 objects

**Amended to.** At this record the opening (X's spec opening.ms, the value code uses) is held equal to: opening_ms of X's three book_open lines, T11/data/AS_OF_PIN.json tc10_pin_close_ms (the object L-L.8 itself names for E.TC10_PIN_MS), TC11's GENESIS opening_ms, the L-T.6 capture, and the contract pin ledger.opening parsed to ms; line 5 is then written with that value and checked by S4. The shim's TC10 pin and TC10's STEP0 record are left to the TC12-L refresh, and the spec says so in `opening_held_equal`.

**Reason.** A build fact met by unit F at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-44 · 2026-10-09 (~21:40Z) · L-L.7, L-L.18, L-L.2, L-L.3 · ruling on AP-43

**Text amended.** L-L.7 ("the five blocks on the five-line file"), L-L.18 (its table is read at --stage=TC12-L), L-L.2 / L-L.3 FAILS-IF (name F-FWD-SPEC), the L-L header ("Each suite below carries a leg F-PORT") — AP-F6 · F-FWD-SPEC and F-PORT hosted at the ledger-spec record as well

**Amended to.** F-FWD-SPEC (its env-free clauses and eight of its nine listed plants, plus the SPEC-READS / SPEC-VA-BLIND plants of seam 62) and F-PORT are hosted at --stage=TC12-REG.ledger-spec; the block says in its PASS line that the ride clause is TC12-L's. TC12-L hosts both again with the ride clause. 10 blocks at this record instead of 5.

**Reason.** A build fact met by unit F at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-45 · 2026-10-09 (~21:40Z) · L-X.19, L-X.20, L-X.18 · ruling on AP-44

**Text amended.** L-X.19, L-X.20, L-X.18 (carry law); O-36 — Unit D (V-9): three mechanics choices in the write-once filing beyond the key lists of L-X.19 and L-X.20

**Amended to.** The filing stands as filed: head bbbc6cab…, REGISTRATIONS.json sha f3bbe260…, nothing re-filed. If the ruling goes for L-X.19's letter, the only window is before the TC12-REG commit: the carry becomes [head] + items and the extra keys drop in tierc12_registrations.py and the plan's section 2, the uncommitted pair is removed and --file re-run. Payload shas and the head then move, and unit F's spec, which pins the head, must be rebuilt.

**Reason.** A build fact met by unit D at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-46 · 2026-10-09 (~21:40Z) · L-X.21, L-0.11, L-X.20, L-X.19 · ruling on AP-45

**Text amended.** L-X.21 (ATTEST-REG, FAILS-IF), L-0.11 (scope law), L-X.20 (what the commit adds and modifies), L-X.19 and O-35 (append-only amendments) — Unit D (V-1): how F-ATTEST-ORDER [REG] judges "ATTEST_REG.json is not that listing" after the attested instant

**Amended to.** Built in tierc12_registrations_fixtures.py only; production is unchanged. The real leg judges the LISTING: production's attest_findings and the suite's typed sets run over the listed paths. Every listed path must be on disk at its listed sha, except (a) LATER_T — the four TC12-REG transcripts, progress/TC12-REG.json, PROGRESS.json and scripts/tierc12_progress.py — which are not held, and (b) APPEND_ONLY_T — LEANS_AMENDMENTS.md and AMENDMENTS_PROPOSED.md — where a byte-prefix of the file must hash to the listed sha. A REG_SET member the listing names `absent` must not have appeared, outside LATER_T. A path the listing does not name is no finding here (ATTEST-ORDER holds it to git ancestry at TC12-SCORE and CLOSE). x_rec/ paths resolve through the main tree. The break leg gains a control (an appended amendment, a later record, a ledger-spec file, the stage's record and a re-merged PROGRESS.json leave the listing silent) and an eighth plant (an append-only text edited inside its listed bytes → ATTEST-LISTING); the seven earlier plants are unchanged.

**Reason.** A build fact met by unit D at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-47 · 2026-10-09 (~21:40Z) · L-0.2, L-0.14 · ruling on AP-46

**Text amended.** L-0.2 (Seed; F-SEED's resolve rule) against L-0.14 (the harness is stdlib only) and L-0.14 F — The harness self-test proves the stream-seed form on integer draws, not on the tier seed

**Amended to.** Took the verifier's primary fix: `_RNG_DRAWS_T = 3`; `_rng_legs()` takes no argument and runs `_st_rng(draw)` for draw in range(_RNG_DRAWS_T). The leg's law is the FORM [SEED, crc32('<suite tag>|<block id>')], which does not depend on the seed's value; the three plants still go RED by their named detectors. Mechanics only: no registered row is touched. Not changed, because V-3 did not require it: `_self_test` still reads PROGRESS.json key `seed` for its printed header line and for `_det_legs(tmp, seed)` (the PYTHONHASHSEED twin label). Neither is a ruler or wrapper call and F-SEED does not flag them; the orchestrator may want to rule whether that read should stand.

**Reason.** A build fact met by unit A at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-48 · 2026-10-09 (~21:40Z) · L-L.7, L-L.5, L-0.9 · ruling on AP-47

**Text amended.** L-L.7 (the suite's two runs; [CHAIN] / [STRUCTURE] failure conditions; planted mutation 5), L-L.5 (the commit law), L-0.9 (gate step 2: re-run without drift) — P7 (new, V-7) — at --stage=TC12-REG.ledger-spec the transcript PRINTS the five-line file; [CHAIN] and [STRUCTURE] JUDGE the whole working file

**Amended to.** The pessimistic reading: the real legs of F-LEDGER [CHAIN] and [STRUCTURE] run their detector over the first five lines AND over the whole working file (working_fx: forward_log.verify_chain, the ported verify_chain, the suite's own hash loop with its byte / NaN / line-break laws; production's chain_findings S1-S7) and fail on any finding; on GREEN nothing tail-dependent is printed. Consequence to rule on: a breach in TC12-L's tail turns THIS record's [CHAIN] / [STRUCTURE] RED as well as TC12-L's own. [PREFIX] already read the whole file for the byte-prefix law; [REHASH] and [ANCESTORS] stay on lines 1-5 (their failure conditions name only those).

**Reason.** A build fact met by unit F at TC12-REG, with the default the precedence gives already built
(reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-49 · 2026-10-09 (~23:36Z) · L-0.22, L-D.3, L-D.5, L-D.6, L-D.11, L-D.24 · ruling on AP-48

**Text amended.** L-0.22 (FAILS-IF, lines 1456-1459), L-D register of constants (2019, 2024, 2028), L-D.3, L-D.5, L-D.6, L-D.11, L-D.24 — CLOSURE-REACH at TC12-D: the closure suite asserts 'no lineage reach' at every stage before TC12-ENV, but the readings order the Stage D builder to import the lineage (verifier D-1, BLOCKING at the gate)

**Amended to.** RULED BY THE ORCHESTRATOR (not the builder's default): the no-lineage-reach assertion of the closure suite binds at `--stage=TC12-REG` ONLY, as L-0.22's FAILS-IF line states it ('At --stage=TC12-REG the suite runs [ii] and [iii] only (no module then in scope reaches the lineage, asserted)'). From `--stage=TC12-D` on, the static reach of each non-fixture module is PRINTED as a disclosed set and a module of TC12-D may reach only `engine.*`, `tierc2_rules` and `drive_wait` (the lineage L-D.3, L-D.5, L-D.11 and L-D.24 name); a reach into a `tierc10_*` / `tierc11_*` module, the shim or a value-area module from a Stage D source stays RED. `scripts/tierc12_closure_fixtures.py` is repaired under this amendment; its `--stage=TC12-REG` behaviour does not change.

**Reason.** A build fact met at TC12-D; the orchestrator's ruling replaces the builder's default here. Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** The artifact named is repaired under this amendment before the TC12-D gate; its transcripts are re-filed and re-recorded by TC12-D's record.

---

## AM-50 · 2026-10-09 (~23:36Z) · L-D.18, L-D.19, L-D.20, L-D.21 · ruling on AP-49

**Text amended.** L-D.18, L-D.19, L-D.20, L-D.21, O-19, resume paste ["maker-bps"] — AM-D-FEE-BINANCE_USDTM / AM-D-FEE-BYBIT_V5_LINEAR: NULL grammar for both venues — neither fee page was retrievable with the library's default headers; the maker pin is the figure on file, flagged

**Amended to.** data/FEE_GRAMMAR.json filed with `venues` {BINANCE_USDTM: null, BYBIT_V5_LINEAR: null}, `amendment` null and `why_null` per venue; --manifest does not HALT (a grammar is required only for a venue captured with HTTP 200). maker_bps_side = 2.0 bps/side on both venues, read from README.md:150 by the regex `maker is (\d+(?:\.\d+)?)%` x pct_to_bps (never typed): BINANCE_USDTM 'ON FILE — NOT RE-CONFIRMED', BYBIT_V5_LINEAR 'ASSUMPTION — NOT RE-CONFIRMED; no Bybit figure is on file'. maker_retrieved_utc_date null, maker_retrieval_attempted_utc_date 2026-10-09. F-TOLL [data d] and [data f] REAL halves assert exactly this from FEE_SOURCE.json. Nothing is mirrored under /Volumes/LaCie/Naiad/provenance/tc12_20261008/ (0 bodies; the directory was not created). The operator's veto "maker-bps" remains the only door for a hand-given figure.

**Reason.** A build fact met at TC12-D, with the default the precedence gives already built (reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-51 · 2026-10-09 (~23:36Z) · L-D.11, L-D.15 · ruling on AP-50

**Text amended.** L-D.11 (the port law), L-D.15 (F-D-PORT) — Port labels follow what F-D-PORT can prove against D11; D11's dead helper `_port_tag` is not ported (verifier D-9, first half)

**Amended to.** Each label is the strongest one the AST supports: 10 TEXT-ONLY (the reading's four plus write_pre_state, _assert_bound, clone_findings, contract_multiplier_table, cache_manifest_staleness, summarize); seal_provenance VERBATIM with the constant SEALED_FILES labelled CHANGED. `_port_tag` not ported (dead code naming TC10's source sha). No logic differs from what the reading orders; F-D-PORT GREEN.

**Reason.** A build fact met at TC12-D, with the default the precedence gives already built (reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-52 · 2026-10-09 (~23:36Z) · L-D.22, L-D.11, L-0.17 · ruling on AP-51

**Text amended.** L-D.22, L-D.11 (capture_contract_specs TEXT-ONLY), L-0.17 / AM-38 (the statement rule of F-TYPED) — CONTRACT_SPECS.json keeps the referee's `law` sentence whole — it names TIER-C11 and does not itself say 'point-in-time' (verifier D-4)

**Amended to.** Bytes left as sealed; the sentence is accepted as a TEXT-ONLY quotation of the referee; the fact is returned as a build disclosure for the B-1 entry.

**Reason.** A build fact met at TC12-D, with the default the precedence gives already built (reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-53 · 2026-10-09 (~23:36Z) · L-D.15, L-D.20 · ruling on AP-52

**Text amended.** L-D.15 (F-D-DET), L-D.20 — F-D-DET's AST clock leg: which calls count as a clock

**Amended to.** The leg counts time.* and datetime.now / utcnow / today as clock calls; fromtimestamp / strptime conversions of filed values are not clocks. The planted mutation (a fee_schedule() copy stamping datetime.now()'s date) is RED by the AST leg.

**Reason.** A build fact met at TC12-D, with the default the precedence gives already built (reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-54 · 2026-10-09 (~23:36Z) · L-D.11, L-D.20, L-0.20 · ruling on AP-53

**Text amended.** L-D.11 (key-for-key schema; the determinism set), L-D.20, L-0.20 — The determinism set carries sealed wall-clock STRINGS and the absolute snapshot_root (verifier D-6)

**Amended to.** L-D.11's key-for-key port kept (TC11's form); the strings are sealed data, not a clock. Any review run must use the same HOME path. If the orchestrator rules L-D.20's 'never carries its clock' to bind this key, the change is a mechanics amendment to --manifest (drop or sha-point the disclosure sentences), moving the manifest sha and the mirror's self-describing copy.

**Reason.** A build fact met at TC12-D, with the default the precedence gives already built (reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-55 · 2026-10-09 (~23:36Z) · L-0.9, L-0.4, L-D.11 · ruling on AP-54

**Text amended.** L-0.9 (the record's keys), L-0.4 (tierc12_progress.certified), L-D.11 — No outside-repo path in artifact_shas: the snapshot is pinned through the tracked manifest

**Amended to.** No outside-repo path is in TC12-D.json artifact_shas. Every snapshot file's sha256, bytes and content_sha is pinned in the tracked data/STAGE_D_MANIFEST.json (files[] 124 + out_of_scope_snapshot_files[] 52), which the record pins by sha dcddc5f7…e8b8; the fix pass re-hashed all 176 local files and all 176 mirrored files equal to it.

**Reason.** A build fact met at TC12-D, with the default the precedence gives already built (reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-56 · 2026-10-09 (~23:36Z) · L-0.20, L-0.21, L-D.11, L-D.15 · ruling on AP-55

**Text amended.** L-0.20 (F-DET), L-0.21 (F-KEY), L-D.11, L-D.15 — No F-DET / F-KEY helper instance, no build_manifest.json and no STAGE_D.md at this record

**Amended to.** F-D-DET (two hash-seed subprocess builds of the four determinism-set files, the filed bytes, the AST clock leg, parquet content shas) is this record's determinism leg; no F-KEY instance; no build_manifest.json and no STAGE_D.md filed.

**Reason.** A build fact met at TC12-D, with the default the precedence gives already built (reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-57 · 2026-10-09 (~23:36Z) · L-D.6, L-D.5 · ruling on AP-56

**Text amended.** L-D.6 (funding), L-D.5 (F-D-FETCHPATH) — A resumed --fetch re-asks the thirteen 8h funding tapes

**Amended to.** D11's logic kept unchanged (TEXT-ONLY). F-D-FETCHPATH holds the resume on CONTENT (nothing saved, no kline asked). --fetch was run exactly once on the real snapshot.

**Reason.** A build fact met at TC12-D, with the default the precedence gives already built (reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-58 · 2026-10-09 (~23:36Z) · L-D.6, L-D.14, L-D.15, L-D.11 · ruling on AP-57

**Text amended.** L-D.6 (row accounting), L-D.14 (F-D-3), L-D.15 (F-D-EDGE), L-D.11 (`complete`) — Funding contiguity INSIDE the extension is held by no leg (verifier D-5; a coverage observation, not a breach)

**Amended to.** Built as the readings state; no leg added. If the orchestrator wants it held: a detector in F-D-EDGE (and a clause of `complete`) — per tape, prints added == (last due floor hour <= pin − TC11 pin) / observed cadence, with one constant spacing — and a plant (one print removed mid-extension, the manifest rebuilt on the copy).

**Reason.** A build fact met at TC12-D, with the default the precedence gives already built (reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-59 · 2026-10-09 (~23:36Z) · L-D.23 · ruling on AP-58

**Text amended.** L-D.23, O-20 — TickGrid.lt / le / gt / ge do not type-check the level n (verifier D-7)

**Amended to.** RULED BY THE ORCHESTRATOR (not the builder's default): hardened now, before any consumer exists — the four level comparisons `lt`, `le`, `gt`, `ge` HALT unless the level `n` is an `int` (`type(n) is int`), as `px` does, and F-TICK [a] gains the case 'a float level must HALT'. L-D.23 calls each an INTEGER comparison; a float level silently decided by a float compare is the hazard the tick grid exists to remove.

**Reason.** A build fact met at TC12-D; the orchestrator's ruling replaces the builder's default here. Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** The artifact named is repaired under this amendment before the TC12-D gate; its transcripts are re-filed and re-recorded by TC12-D's record.

---

## AM-60 · 2026-10-09 (~23:36Z) · L-D.19, L-D.1, L-D.18 · ruling on AP-59

**Text amended.** L-D.19 (the schema), L-D.1 (the pin record's keys), L-D.18 (FEE_SOURCE.json's keys) — Additive keys beyond the readings' tables in fee_schedule.json, AS_OF_PIN.json and FEE_SOURCE.json (verifier D-9, second half)

**Amended to.** Kept: all additive provenance. AS_OF_PIN.json and FEE_SOURCE.json are write-once and sealed and cannot be rewritten without a new fetch; fee_schedule.json is in the determinism set and reproduces byte for byte.

**Reason.** A build fact met at TC12-D, with the default the precedence gives already built (reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-61 · 2026-10-09 (~23:36Z) · L-D.24 · ruling on AP-60

**Text amended.** L-D.24 — F-MIRROR's BREAK half plants on a temp copy of the mirror's funding tree, not of the whole mirror

**Amended to.** The plants (one flipped byte, one removed file, one altered sha in a copy of the attestation) run on the 21-file temp copy with an unbent control; the comparator is the one the REAL half uses.

**Reason.** A build fact met at TC12-D, with the default the precedence gives already built (reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-62 · 2026-10-09 (~23:36Z) · L-D.18 · ruling on AP-61

**Text amended.** L-D.18 (Act 1 — CAPTURE) — A fee page answered with a status other than 200 / 404 leaves no body to save

**Amended to.** Through ED._get as the reading orders; FEE_SOURCE.json files http_status (the last attempt's, read from the logged http rows), the error text, http_requests_logged = 4, null body_path / body_sha256 / body_bytes. No fee_source body file exists and ~/.cache/naiad/provenance/ was not created.

**Reason.** A build fact met at TC12-D, with the default the precedence gives already built (reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-63 · 2026-10-09 (~23:36Z) · L-D.5 · ruling on AP-62

**Text amended.** L-D.5 ('--all = steps 2 -> clock row -> 3a-3f -> 4 -> 5 -> 6 (D11's run_all)') — --all returns 2 before the derivation and the seal when the fetch is incomplete

**Amended to.** run_all (CHANGED, named in PORTS) returns exit 2 right after an incomplete fetch; nothing is derived, sealed or described until a re-run completes. The build of record ran the subcommands one by one in L-D.5's order (--clone, --pin, --fetch, --derive, --seal, --manifest, fixtures, --mirror, mirror fixture), each once and complete.

**Reason.** A build fact met at TC12-D, with the default the precedence gives already built (reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-64 · 2026-10-09 (~23:36Z) · L-D.24, L-D.11 · ruling on AP-63

**Text amended.** L-D.24 (step 6: 'destination, volume filesystem, drive_wait state...'), L-D.11 ('exactly ONE out-of-process call') — MIRROR_ATTEST.json cannot name the volume's filesystem without a second out-of-process site

**Amended to.** MIRROR_ATTEST.json files `volume_observed`: os.statvfs fields, case_insensitive = True (measured on the destination) and a sentence that the name is not read by the module. The mirror child record's notes carry what `mount` printed in the builder's shell: /dev/disk6s2 on /Volumes/LaCie (exfat).

**Reason.** A build fact met at TC12-D, with the default the precedence gives already built (reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-65 · 2026-10-09 (~23:36Z) · L-D.23, L-S.11, L-S.15, L-R.24 · ruling on AP-64

**Text amended.** L-D.23 (the trapping context; 'a quotient that is not exact raises at this precision and is a HALT'); consumers L-S.11, L-S.15, L-R.24 — TickGrid: an inexact quotient under grid.ctx raises MemoryError, not decimal.Inexact

**Amended to.** TickGrid's own operations (+, -, x, divmod) catch (decimal.DecimalException, MemoryError) and HALT. A consumer forming its own expression under decimal.localcontext(grid.ctx) must treat MemoryError as the same HALT — stated in the module docstring. lt / gt are written with the level formed in a statement of its own (below = n - 1; above = n + 1), so no BinOp stands under a comparison (AM-34).

**Reason.** A build fact met at TC12-D, with the default the precedence gives already built (reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-66 · 2026-10-09 (~23:36Z) · L-D.3, L-D.15, L-D.1 · ruling on AP-65

**Text amended.** L-D.3 (FAILS-IF), L-D.15 (F-D-GUARD), L-D.1 (the pin record's keys) — F-D-GUARD's equality-removed mutant, and step_q.instant

**Amended to.** Two mutants, both caught: equality removed (GUARD-ACCEPTS a foreign directory), and equality plus the TC11 refusal row removed (GUARD-ACCEPTS the TC11 snapshot). AS_OF_PIN.json step_q.instant = ct_ms 1791499933000 with step_q.instant_iso '2026-10-08T22:52:13Z' beside it; extra provenance keys o7_printed, bybit_server_time, bybit_kline_endpoint, bybit_closure_law were added.

**Reason.** A build fact met at TC12-D, with the default the precedence gives already built (reading cap, O-35). Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** Nothing: the stage was built under this default.

---

## AM-67 · 2026-10-09 (~23:36Z) · L-X.21, L-X.20, L-0.4 · ruling on AP-66

**Text amended.** L-X.21, L-X.20, L-0.4 — F-ATTEST-ORDER [REG] holds a listed REG_SET script to its listed sha for good, so a lawful repair of one after the registry commit turns the leg RED

**Amended to.** RULED BY THE ORCHESTRATOR: the attestation is a statement about the FILING INSTANT. For a listed path that is tracked, the leg holds the listed sha equal to the sha of the blob of that path at the commit that first adds `registrations/REGISTRATIONS.json` (read-only git) — immutable, so a later lawful repair cannot move it; for a listed path that is git-ignored (`x_rec/**`) it holds the working file, as before. LATER_T and the append-only prefix rule are unchanged. A repaired REG_SET script is re-recorded by the record of the gate that repairs it (L-0.4 (1), the last-record law). `scripts/tierc12_registrations_fixtures.py` is repaired under this amendment.

**Reason.** A build fact met at TC12-D; the orchestrator's ruling replaces the builder's default here. Mechanics only: no registered row's population, arms, statistic, verdict rule or labels moves.

**Redone.** The artifact named is repaired under this amendment before the TC12-D gate; its transcripts are re-filed and re-recorded by TC12-D's record.
