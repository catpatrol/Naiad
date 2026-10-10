# TIER-C12 · AMENDMENTS PROPOSED

A builder who meets two readings that cannot both be built files the two texts and the build fact here; the
orchestrator rules and dates the ruling in `LEANS_AMENDMENTS.md` before the stage's gate (O-35). Under the resume
paste's reading cap an entry always carries its DEFAULT, which the build takes and prints until it is ruled; nothing
here is a question that waits. Entries are append-only.

---

## AP-1 · 2026-10-09 (~18:10Z) · L-X.36, the five REGISTRATION SPEC blocks · filed at the freeze by the seam pass (seam 43)

**The two texts.** L-X.36 gives one quoted "common sentence" for every row's `verdict_rule`: the ruler sentence
("verdict_of_record = SUPPORTED iff … never loosens the bar.") followed by the printed-beside list ("Printed beside,
deciding nothing: … Tier-E arms carry no verdict word."). P-ADM-1 and P-BRD-1 carry both contiguously. P-DIR-1,
P-SFP-VA-1 and P-SCALP-3 carry the ruler sentence byte for byte (after the seam pass dropped their inline family
constants and moved their bootstrap clause behind it) but EXTEND the printed-beside list with row-owned items, and
P-DIR-1 and P-SFP-VA-1 place their exhaustive-words sentence before it.

**The fact.** A text detector that demands the whole quoted block contiguous in all five payloads cannot pass, and
making the three blocks carry it would be a re-draft of three registered rows' verdict text, which the reading cap
forbids.

**DEFAULT TAKEN.** The registry's text detector (F-REG, RULER-TEXT) holds the RULER SENTENCE byte for byte in all five
payloads, compared after collapsing runs of whitespace, and holds that each payload's printed-beside list CONTAINS
every item of L-X.36's list. The verdict words, the clauses (a)(b)(c) and the labels are untouched.

**Status.** Default in force; to be ruled as AM-n when the TC12-REG builder reaches the detector.

---

## AP-2 · 2026-10-09 (~21:40Z) · L-0.14, L-0.4, L-0.11, L-0.19 · unit A at TC12-REG (build)

**Title.** NOT BUILT is counted beside C's tally, not inside it

**Readings.** resume paste "tier-e-never-halts" (O-36) vs L-0.14 C and F-FX-FORM; L-0.4 (3), L-0.11, L-0.19

**The texts.** Paste: a Tier-E table that cannot be built 'prints its reason … and the stage CONTINUES; its F-GRID / F-KEY legs print `NOT BUILT <reason>` — a leg state, never PASS — and §9 counts them.' L-0.14 C: 'The tally line is ` N GREEN, M RED, K NOT RUN` … a transcript is GREEN iff zero RED and `GREEN + NOT RUN == legs_total`'; A: '`legs_total` counts blocks'; F-FX-FORM: 'a tally line not of C's form' is RED. LEANS.md never mentions NOT BUILT.

**The fact.** A NOT BUILT block is a block that is neither GREEN, RED nor NOT RUN. Counted in legs_total it breaks C's identity at every record gate and in the sweep, which halts the stage the paste says continues. Counted as NOT RUN it is outside NOT_RUN_FIDS_T and, F-GRID and F-KEY being contract-named, RED at TC12-FIX. A fourth count on the tally line breaks F-FX-FORM's form.

**DEFAULT TAKEN.** The paste governs. `not_built(fid, title, reason)` prints the header and ` [NOT BUILT] <fid>: <reason>`; it is lawful only for the FIDs F-GRID and F-KEY, any other reads FAIL. C's tally line is unchanged and legs_total = GREEN + RED + NOT RUN. NOT BUILT is counted on one more line ` J NOT BUILT` (printed only when J > 0, followed by one ` NOT BUILT: <block id>` line each) and in summary()['legs_not_built']; the exit code is unaffected. NOT SETTLED HERE, for the orchestrator: (a) F-FX-FORM must accept a NOT BUILT block as exactly its header and its line; (b) L-0.19's roll says a contract name is PASS only if every block of its FID is PASS, so F-ROLL needs a rule for a NOT BUILT F-GRID / F-KEY block; (c) the progress record's key list (L-0.9) has no legs_not_built.

**Status.** Ruled at the TC12-REG gate: AM-3.

---

## AP-3 · 2026-10-09 (~21:40Z) · L-0.20, L-0.14, L-0.22 · unit A at TC12-REG (build)

**Title.** F-DET's helper leg holds no subprocess site; the calling suite launches the twins

**Readings.** L-0.20 and L-0.14 (helper legs in tierc12_fx.py) vs L-0.22 points 1, 4, legs (ii) and (iv)

**The texts.** L-0.20: 'F-DET (helper legs in `tierc12_fx.py` …)' and 'the suite runs that directory's one writer script twice, each in a fresh subprocess'. L-0.22: 'THE GLOB = every `scripts/tierc12_*.py` whose stem does not end `_fixtures`'; 'Every other GLOB member is a DECISION module, with no exemption'; (iv) '`subprocess` appears only at the typed call sites `SUBPROC_SITE_T` … Fixture modules may use `subprocess` (… twins …). No other non-fixture module holds a subprocess site'; (ii) 'no `exec` / `eval` / `compile`'.

**The fact.** tierc12_fx is a GLOB member that is not a fixture module and is not on SUBPROC_SITE_T. A twin launcher inside it would be a subprocess site in a non-fixture module (F-HOOK-ESCAPE RED from TC12-ENV), and a shadow-module self-test would need exec / compile (leg (ii) RED).

**DEFAULT TAKEN.** The pessimistic reading: the harness imports no subprocess and calls no exec / eval / compile. `det_twins(launch, directory, stage, seed)` takes the SUITE's launcher (the suite owns the fresh subprocess under PYTHONHASHSEED and returns an exit code or a handle with .wait()); the harness removes stale twin directories, labels the twins and does every comparison of L-0.20. The self-test plants by swapping an object in the production call path and by mutated text copies judged by AST — both lawful forms under L-0.14.

**Status.** Ruled at the TC12-REG gate: AM-4.

---

## AP-4 · 2026-10-09 (~21:40Z) · L-0.14 · unit A at TC12-REG (build)

**Title.** NOT_RUN_FIDS_T holds whole block ids

**Readings.** L-0.14 seam 3 and C; F-FX-FORM; L-D (F-TOLL [data a..g], leg (d))

**The texts.** Seam 3: '`NOT_RUN_FIDS_T`, as assembled at the freeze: L-D's F-MIRROR and the body-file leg of F-TOLL [data].' F-FX-FORM: 'a `not_run` call names an FID outside `NOT_RUN_FIDS_T`'.

**The fact.** F-TOLL is a contract-named FID with seven data legs, a reader leg and a book leg. An FID-level entry would let any of them print NOT RUN. The body-file condition is stated in L-D's leg (d).

**DEFAULT TAKEN.** NOT_RUN_FIDS_T = ("F-MIRROR", "F-TOLL [data d]"), matched on the whole block id and enforced at run time by `not_run`: any other id prints `[FAIL]` and is RED. The closure suite's typed copy should hold the same two strings.

**Status.** Ruled at the TC12-REG gate: AM-5.

---

## AP-5 · 2026-10-09 (~21:40Z) · L-0.14 · unit A at TC12-REG (build)

**Title.** Hand-sample: a category whose first row an earlier category already took

**Readings.** L-0.14 G

**The texts.** 'categories first — the first row of each named category in the reading's stated key order. (1) A category with no member prints `NONE-EXISTS <category>` … its slot is taken by the next unchosen row in key order, printed `FILL`.' The text is silent on two categories sharing a first row, and on the slot count when the categories outnumber k.

**The fact.** A sampler must return distinct rows; with overlapping categories the literal rule returns one row twice.

**DEFAULT TAKEN.** Non-empty categories take their first rows, in category order, before any FILL is drawn. A category whose first row is already chosen prints `SHARED <category>: …` and its slot is FILLed by the next unchosen row in key order. Slots = max(k, number of categories), capped at n. No size or composition case is RED; only a population that does not hold the count handed in as n_asserted returns a problem.

**Status.** Ruled at the TC12-REG gate: AM-6.

---

## AP-6 · 2026-10-09 (~21:40Z) · L-0.17 · unit B at TC12-REG (build)

**Title.** TOTALITY: which lines of the prefix are 'operative'

**Readings.** L-0.17 (TOTALITY; F-PINS 'a digit run of the operative lines is unaccounted'), CANON-25 point 6

**The texts.** "Every digit run in the prefix's operative lines is either inside one map row's capture or listed in CONTRACT_TOKENS_UNPINNED.json with its class" — no reading defines 'operative lines'.

**The fact.** The term has no definition in LEANS, the canon or the dispositions, so the totality check has no stated domain.

**DEFAULT TAKEN.** Pessimistic: every line 1..137 of the prefix is operative. A digit run must lie inside exactly one capture (main or `also`, by `group` where given) or exactly one classed token; never both, never neither.

**Status.** Ruled at the TC12-REG gate: AM-7.

---

## AP-7 · 2026-10-09 (~21:40Z) · L-0.17, L-R.32 · unit B at TC12-REG (build)

**Title.** two_trades.horizons is cited at :79; the token stands on :78

**Readings.** L-0.17 (PIN NAMES OF RECORD), CANON-25 point 3, L-R.32

**The texts.** "`two_trades.horizons` (:79, two groups, asserted equal to X's `pins.laws.horizons`)"; L-R.32: "contract :79 `H20/H100` (two groups)".

**The fact.** On the STEP Q bytes `H20/H100 net of the` is on line 78; a regex for it matches 0 times on :79, so a row built as cited HALTs PIN-PARSE.

**DEFAULT TAKEN.** Map row `two_trades.horizons` lines [78, 78], regex `H(\d+)/H(\d+) net of`, value (20, 100). Every other cited line was built as cited and parses.

**Status.** Ruled at the TC12-REG gate: AM-8.

---

## AP-8 · 2026-10-09 (~21:40Z) · L-0.17, L-0.18, L-X.1, L-0.14 · unit B at TC12-REG (build)

**Title.** The registry clauses of F-PINS and F-FAM-PINS before the registry exists

**Readings.** L-0.17 (F-PINS: 'the text of the filed registry … checked at filing'), L-0.18 (F-FAM-PINS: 'a payload of the filed registry'), L-X.1 ('on disk before --file runs'), L-0.14 C / seam 3

**The texts.** L-X.1: the pin door and its files "are on disk before `--file` runs". L-0.18: F-FAM-PINS "FAILS IF … a payload of the filed registry carries a family, m or bar other than the parse gives its id". Seam 3: a leg that cannot run reads FAIL; NOT RUN is lawful only for F-MIRROR and F-TOLL [data d].

**The fact.** The pins suite must be GREEN before the filer that depends on it can file the registry, so at its first run no registry is on file; the two clauses have no object, and NOT RUN is not lawful for these FIDs.

**DEFAULT TAKEN.** Literal reading: the clauses assert on registrations/REGISTRATIONS.json when it is on file (families[] and every payload's family, family_m, family_bar; the nine stamp-set shas absent from its text). When it is not, each REAL leg prints `registry: NOT ON FILE — the registry clause asserts nothing at this run` and passes on its other clauses. BREAK plants run on the filed registry if present, else on a document built in L-X.19's keys. Consequence: the filed transcript is the pre-registry one and must be re-filed once with --refile-transcript after the registry lands.

**Status.** Ruled at the TC12-REG gate: AM-9.

---

## AP-9 · 2026-10-09 (~21:40Z) · L-0.23, L-0.5 · unit B at TC12-REG (build)

**Title.** How an operator veto files a substituted pin value, and what counts as 'an operator quote'

**Readings.** L-0.23 (EFFECT BY TIMING; F-VETO clause 4), L-0.5 (heading form)

**The texts.** "A value the operator substitutes is filed in the amendment and read from there by the pin door; it is never typed in code." F-VETO "FAILS IF … an amendment that changes a pin names no operator quote". L-0.5 fixes only the heading: `## AM-<n> · <date> · <reading ids> · operator veto "<token>"`.

**The fact.** No reading gives the body grammar by which an amendment states a pin's new value, nor a test for 'names an operator quote', so neither the door's read nor the detector can be built from the text.

**DEFAULT TAKEN.** A pin is changed by a body line `PIN <name> := <value> [<value> …]` (one value per capture group, parsed by the row's types). The heading's basis must be `operator veto "<token>"` with <token> equal to that pin's register `veto`; the body must hold a line where the word `operator` is followed by a double-quoted string (the heading does not count). Otherwise VETO-AMENDMENT. load() overlays the last substitution on a contract pin; amended() exposes it for x_record / stage_d rows. AM-1 has no PIN line, so nothing is overlaid today.

**Status.** Ruled at the TC12-REG gate: AM-10.

---

## AP-10 · 2026-10-09 (~21:40Z) · L-0.17, L-0.24 · unit B at TC12-REG (build)

**Title.** F-PINS census-sha clause: which paths are 'L-0.24's sets (a)-(f)' at filing

**Readings.** L-0.17 (F-PINS), L-0.24 (sets (a)-(f); F-TC11-STAMP (vii))

**The texts.** F-PINS: "a register row, or the text of the filed registry, carries the census sha (whole or abbreviated) of a path in L-0.24's sets (a)-(f)". L-0.24 (d): "REGISTRY_CHECK.json and the other records TC11's own scorer regenerates"; (e): "the transcripts and manifests that print a moved sha".

**The fact.** Sets (d) and (e) are open-ended until the stamp proof at TC12-CLOSE writes TC11_STAMP_MAP.json. progress/TC12-R0.json lists 8 frozen-estate paths and none of the five set-(c) scripts; frozen/FROZEN_ESTATE.json is another unit's and was not on file.

**DEFAULT TAKEN.** The suite types the nine nameable members (STAMP_SETS_T: TC11's REGISTRATIONS.json and REGISTRY_PIN.json, the five set-(c) scripts, scores/REGISTRY_CHECK.json, TC11's PROGRESS.json) and reads each sha from the byte-frozen file. 'Abbreviated' = a hex run of at least 8 characters that is a prefix of the sha (ABBREV_MIN_T). The closed sets remain F-TC11-STAMP (vii)'s at CLOSE.

**Status.** Ruled at the TC12-REG gate: AM-11.

---

## AP-11 · 2026-10-09 (~21:40Z) · L-0.17, L-V.4, L-0.24 · unit B at TC12-REG (build)

**Title.** Register rows that have no name of record

**Readings.** L-0.17 (PIN NAMES OF RECORD 'sections use these and no other'; seam 35; the lineage door), L-V.4 (table column 'register row · kind'), L-0.24 point (1)

**The texts.** Seam 35: the register "carries `lineage` rows … for the literals L-X reads from scripts/tierc11_score.py (the sixteen columns, HAIRCUT_TOL, SUM_TOL, NET_LAW_TOL, EXIT_FLAGS)". L-0.17: the register "lists every pin of EVERY door, one row each". L-V.4 lists bins, ATR length, floor n as `lineage` and null draws, X's return window as `x_record`, with no name.

**The fact.** These rows are ordered but unnamed, and the names-of-record list is closed.

**DEFAULT TAKEN.** 20 door-named rows, typed as DOOR_NAMED_T in the suite: lineage.tierc11_score.{REQUIRED, INT_COLS, FLOAT_COLS, STR_COLS, SORT_KEY, HAIRCUT_TOL, SUM_TOL, NET_LAW_TOL, EXIT_FLAGS} (the literals at :248-255, :264-266, :301); lineage.tierc2_rules.ATR_LEN; lineage.tierc5_rules.{WARMUP_BARS, PROVISIONAL_MIN_N}; lineage.tierc10_panel.{N_BOOT, LENS_MS, ERA_CUT_MS}; lineage.analytics_profile.{PROFILE_ROWS, VALUE_AREA}; lineage.tierc2_baseline._round_floats.nd; x.va.laws.{k_draws, dev_return_bars}. Each carries `named_by` and (lineage) a node sha the door re-asserts. The other lineage objects of L-R.32, L-S.2 and L-L's tables have no 'register row' column and carry no row.

**Status.** Ruled at the TC12-REG gate: AM-12.

---

## AP-12 · 2026-10-09 (~21:40Z) · L-0.17, L-V.4, L-R.32, L-S.2, L-G.3, L-L.8 · unit B at TC12-REG (build)

**Title.** Which 'asserted equal to' comparisons the door makes itself

**Readings.** L-0.17 (the contract door; seam 6; seam 45), L-V.4, L-R.32, L-S.2, L-G.3, L-L.8/14/27

**The texts.** "the door makes that comparison itself when the object is a literal of a frozen file — read as TEXT (ast) or as JSON, with the file's manifest sha or the literal's node sha asserted — and otherwise the pin's consumer makes it at its own stage".

**The fact.** The readings list the second objects but not, object by object, who compares; several are attributes of live objects, parquet rows or TC11 registry texts under L-G.5's chain-head law.

**DEFAULT TAKEN.** Recorded per row as `equal_to` items. By the door (28, PIN-EQUAL): va.accept_n, va.accept_margin_atr, va.sfp_k (member of sfp_k_twins), va.nest_frac, va.value_area_pct and adm.old_quantile (× PCT_PER_UNIT read as text from tierc12_units.py), chop.n_bands (the range argument of DECILES), sfp.rail_atr, sfp.t2_offset_atr, tp1d.approach_atr, two_trades.horizons (X's pins.laws.horizons and tierc10_census HORIZONS), scalp.ema_fast/slow, scalp.stop_beyond_atr, scalp.rail_atr, scalp.t1_fraction, scalp.t2_offset_atr, ledger.opening (ms), ledger.n_min, ferry.cap_mb (× BYTES_PER_MB == CAP_BYTES). By the consumer (21): seed, ctrl.sum_net_r, adm.lag_cut, adm.preseen_cell, adm.abs_cut, brd.cut, the two grid rows, book.trg912_periods, sfp.t1_fraction (CONTROL_CARD.harvest_frac), va.mirror_words, va.licence_set, scalp.era, loao.line and the further objects of the ledger rows.

**Status.** Ruled at the TC12-REG gate: AM-13.

---

## AP-13 · 2026-10-09 (~21:40Z) · L-0.17 · unit B at TC12-REG (build)

**Title.** A class beyond the reading's list for two tokens

**Readings.** L-0.17 (TOTALITY, the class list), CANON-25 point 6, seam 39

**The texts.** "with its class (an id such as a registration or stage label, a date, a prior, a hand-sample count, a quoted history figure, a `lens name`, a `ruling or section id`, a `tier id`)"; seam 39 adds the print-format token.

**The fact.** `t+1` (:115, 'bar t+1') and `L+1` (:46, 'an edge of L+1') carry a digit and fit none of the nine classes.

**DEFAULT TAKEN.** A tenth class `index_offset` holding exactly those two tokens; the suite types the count per class.

**Status.** Ruled at the TC12-REG gate: AM-14.

---

## AP-14 · 2026-10-09 (~21:40Z) · L-0.17, L-0.19, L-0.18 · unit B at TC12-REG (build)

**Title.** Where the family pins' flow bends are hosted

**Readings.** L-0.17 (THE FLOW LEG; F-TYPED-TOTAL), L-0.19 seam 2, L-0.18, resume paste RC-2

**The texts.** Seam 2 lists the records hosting F-TYPED-FLOW blocks and does not name TC12-REG. L-0.17: "Whatever block hosts a bend — F-TYPED-FLOW, or a leg of the owner's own fixture — it prints one line per pin". RC-2: no fixture leg beyond the canon's.

**The fact.** fam.q and fam.G/R/S are contract pins whose smallest production reader is the door's own families(); no reading names a block for their bend, and F-TYPED-TOTAL will demand a [FLOW] line for each.

**DEFAULT TAKEN.** No new block. F-FAM-PINS's REAL leg bends each of the four at the door (families() must HALT FAMILY-BAR, per seam 45) and prints the four [FLOW] lines; its BREAK leg plants a shadow copy of the door holding a typed 1/10 in place of fam.q, caught as PIN-NOT-READ.

**Status.** Ruled at the TC12-REG gate: AM-15.

---

## AP-15 · 2026-10-09 (~21:40Z) · L-0.3, L-0.4, L-0.9, L-0.10, L-0.14, L-X.21 · unit C at TC12-REG (build)

**Title.** The gate form of the resume transcript: it cannot print the gate's own record and stay byte-identical

**Readings.** L-0.3, L-0.4, L-0.9 (the gate, steps 1-6), L-0.10 point 4, L-0.14 I, L-X.21 (REG_SET)

**The texts.** L-0.9: '(1) the builder files its artifacts and its transcripts (--refile-transcript, once) … (3) the builder writes the progress record with the transcript shas before and after … (5) F-RESUME and its sibling legs run at --stage=<record id> --at=<previous tierc12 head>'. L-0.3: F-RESUME 'recomputes the ledger of records … and prints THE RESUME POINT'. L-0.14 I: a transcript is byte-identical over the filing run, the gate's re-run, the TC12-FIX sweep and the reproducibility lens; differing bytes go to _rerun.txt, RED. REG_SET makes resume/FIXTURES_RESUME_TC12-REG.txt an artifact of the TC12-REG record.

**The fact.** The transcript's sha is carried by the gate's own record, so it is filed before that record exists, re-run after it exists, and re-run again at the sweep with later records and commits on disk. A ledger or resume point printed over every record on disk differs in each of those runs.

**DEFAULT TAKEN.** The transcript carries only facts fixed at the gate: git read at --at; the records BEFORE --stage in RESUME_ORDER (each must be COMPLETE-VERIFIED, else GATE-ORDER RED); the resume point 'at this gate' (the gate's id when all before it verify). The gate's own record, and what its commit will add (the registry's pins, its transcripts), are verified WHEN ON FILE and are mandatory from the next gate on; no printed count or name moves with the gate's record, a later record or a later commit. The LIVE ledger and resume point over every record on disk go to stdout only (the suite, and tierc12_progress.py). Checked on a scratch estate: filing run, gate re-run and later sweep give identical PASS lines on all nine repo legs.

**Status.** Ruled at the TC12-REG gate: AM-16.

---

## AP-16 · 2026-10-09 (~21:40Z) · L-0.4, L-0.5 · unit C at TC12-REG (build)

**Title.** L-0.4 (1) before the gate's record exists: the path a gate lawfully re-records

**Readings.** L-0.4 (1), L-0.5

**The texts.** L-0.4 (1): 'Every artifact_shas path exists and verifies under THE LAST RECORD THAT NAMES IT … the working file re-hashes to that record's {bytes, sha256} … Anything else is a moved artifact.' and 'Paths the readings themselves re-record are lawful under (1) and are named as such: … scripts/tierc12_progress.py (R0, then TC12-REG; tracked) …'.

**The fact.** At the TC12-REG filing run scripts/tierc12_progress.py already differs from R0's entry and progress/TC12-REG.json is not on file; by the letter TC12-R0 reads PARTIAL and the derived resume point falls back to TC12-R0. The same holds for an append-only file (AMENDMENTS_PROPOSED.md, LEANS_AMENDMENTS.md) that grows between two gates.

**DEFAULT TAKEN.** Typed RERECORDED (tierc12_progress.py data, second copy RERECORDED_T in the fixture): scripts/tierc12_progress.py [TC12-R0, TC12-REG]; ferry/FERRY_MANIFEST.json [TC12-L, TC12-CLOSE]; va/stamps/build_manifest.json [the three stamps children]. While the NEXT named recorder is not on file, a differing working file is that record's to pin and the earlier entry is still held to the blob at its closing commit. An append-only path that grew is lawful iff the last entry's bytes are a byte-prefix of the working file. Anything else stays a moved artifact — including an UNTRACKED path a gate supersedes: for such a gate the record (with its supersedes entry) must be on file before the resume suite's filing run.

**Status.** Ruled at the TC12-REG gate: AM-17.

---

## AP-17 · 2026-10-09 (~21:40Z) · L-0.8, L-0.9 · unit C at TC12-REG (build)

**Title.** F-OFFBUS / F-COMMIT: the resume paste's own STEP Q commit files a second text under exchange/queue/

**Readings.** L-0.8, L-0.9; the resume paste (STEP Q); O-36

**The texts.** L-0.8 FAILS-IF: 'any path under exchange/ other than the contract in the STEP Q commit'. L-0.9 F-COMMIT: 'a path outside the allow-list (plus the contract, STEP Q only)'. Paste: 'STEP Q: file this paste verbatim to exchange/queue/2026-10-09_TC12_RESUME_APOLLO.md … one commit staging that one path, subject tierc12(STEP Q): resume paste filed verbatim'.

**The fact.** Commit 1e8f8ff `tierc12(STEP Q): resume paste filed verbatim` adds exchange/queue/2026-10-09_TC12_RESUME_APOLLO.md. As written both fixtures are RED on the filed history.

**DEFAULT TAKEN.** The paste governs (O-36): STEP_Q_PATHS_T = (the contract, the resume paste) — the two queue texts a commit whose parsed id is STEP Q may file. Every other path under exchange/ in a tierc12( commit stays RED.

**Status.** Ruled at the TC12-REG gate: AM-18.

---

## AP-18 · 2026-10-09 (~21:40Z) · L-0.5, L-X.20 · unit C at TC12-REG (build)

**Title.** F-FROZEN-TEXT: the registry filer's write-once HALT is not planted in the resume suite

**Readings.** L-0.5 (planted mutations), L-X.20 (F-REG [WRITE-ONCE])

**The texts.** L-0.5: '… the registry filer run against an existing REGISTRATIONS.json must HALT (counted as the catch)'. L-X.20: 'F-REG [WRITE-ONCE] is RED when a second --file changes a byte or exits 0, in the filed directory and in a scratch twin'.

**The fact.** scripts/tierc12_registrations.py was not on file when this unit was built; it files the registry write-once into the tree of record, and the resume suite runs at every later gate — it must never be able to execute that filer against the tree. The same plant already belongs to F-REG [WRITE-ONCE].

**DEFAULT TAKEN.** F-FROZEN-TEXT holds write-once by its stated failure condition — more than one commit in range touches a write-once file, or the working file is not the blob that filed it — with a planted second blob in a scratch repository (detector WRITE-ONCE). The filer's own HALT stays the registry suite's plant; the BREAK line of the transcript says so.

**Status.** Ruled at the TC12-REG gate: AM-19.

---

## AP-19 · 2026-10-09 (~21:40Z) · L-0.5, L-0.12 · unit C at TC12-REG (build)

**Title.** F-FROZEN-TEXT (e): which record is 'the review record's last-pass sha' for LEANS.md

**Readings.** L-0.5, L-0.12

**The texts.** L-0.5: 'sha256(T12/LEANS.md) == REGISTRATIONS.json leans.sha256 == REGISTRY_PIN.json leans_sha256, and the sha the last review pass names (L-0.12)'.

**The fact.** review/LEANS_REVIEW_2026-10-09.json names reviewed_commit 7295ab5 and no sha of LEANS.md (the file did not exist at the review; D-13). The one filed record binding the frozen bytes is the header of review/WORKTREE_ATTEST_LEANS.jsonl (`frozen.sha256`).

**DEFAULT TAKEN.** ONE value is required of: sha256(LEANS.md), the TC12-LEANS record's entry, the attestation header's frozen.sha256, and — when on file at the TC12-REG gate, mandatory after it — REGISTRATIONS.json leans.sha256 and REGISTRY_PIN.json's leans pin (read as `leans_sha256` or `leans.sha256`).

**Status.** Ruled at the TC12-REG gate: AM-20.

---

## AP-20 · 2026-10-09 (~21:40Z) · L-0.10 · unit C at TC12-REG (build)

**Title.** F-ORDER T6 has no machine-readable link from an amendment to the artifact it changes

**Readings.** L-0.10 (T6, T7)

**The texts.** T6: 'an amendment is committed before the artifact it changes is rebuilt.' F-ORDER: 'an ancestry of T1, T2, T3 or T6 fails'.

**The fact.** No filed field says which artifact an AM-n changes; only a record's notes carry ids.

**DEFAULT TAKEN.** T6 is checked where T7 is: when a tierc12( commit changes a regbook manifest's `sha` map, every AM-n id in that record's notes must have its heading in LEANS_AMENDMENTS.md at a commit that is a proper ancestor of the rebuilding commit; an AP-n id must be in the notes (T7). At TC12-REG both print their pre-registry form.

**Status.** Ruled at the TC12-REG gate: AM-21.

---

## AP-21 · 2026-10-09 (~21:40Z) · L-0.6 · unit C at TC12-REG (build)

**Title.** The census holds Finder metadata under a census root

**Readings.** L-0.6

**The texts.** L-0.6: the census covers 'research_outputs/tierc11/**' … 'A moved path with no attributing foreign commit is a finding against TC12 and HALTs the gate.'

**The fact.** research_outputs/tierc11/.DS_Store is on disk. Finder rewrites it when the operator browses the folder; no lane commits it.

**DEFAULT TAKEN.** Built as written (the pessimistic reading): .DS_Store is in the census like any other file and a change to it is FROZEN-CHANGED. If the orchestrator prefers a typed exclusion of that one name, it is a one-line change in tierc12_frozen.estate() plus a re-pinned census (--write --k=1).

**Status.** Ruled at the TC12-REG gate: AM-22.

---

## AP-22 · 2026-10-09 (~21:40Z) · L-0.6, L-0.24, L-X.34 · unit C at TC12-REG (build)

**Title.** The keys of close/TC11_STAMP_MAP.json that F-FROZEN's one typed acceptance reads

**Readings.** L-0.6, L-0.24, L-X.34

**The texts.** L-X.34: the map holds 'head_at_proof, proof, applied (false), old → new sha per replaced pin, each moved file's sha before and after, the historical list' — no key names for the per-file rows.

**The fact.** The acceptance needs a path and its post-image sha from a file another stage writes.

**DEFAULT TAKEN.** tierc12_frozen.stamp_accepts reads `applied` (must be true) and `moved: [{path, sha256_before, sha256_after}]`; a path is accepted only if it is the TC11 contract, of typed sets (a), (b), (c), (f), or under research_outputs/tierc11/ (sets d, e as the map lists them), and never one of SCORES.json / FAMILY.json / BASE_IDENT.json. The census records this rule under `stamp_acceptance`.

**Status.** Ruled at the TC12-REG gate: AM-23.

---

## AP-23 · 2026-10-09 (~21:40Z) · L-X.15, L-0.18, L-0.19 · unit D at TC12-REG (build)

**Title.** F-FAM is NOT hosted in the registry suite — CANON-24's hosting taken over the unit brief

**Readings.** L-X.15, L-0.18, L-0.19, L-X hosting table (LEANS.md:7195-7198), CANON-24; resume paste FIXTURES line and RC-2; unit brief D

**The texts.** Brief: 'Suite: tierc12_registrations_fixtures.py … hosting F-REG (…) and the F-FAM blocks (incl. the planted precondition-closed family that must spend no test)'. L-X.15: 'three blocks whose FID is exactly F-FAM … in scripts/tierc12_score_fixtures.py … F-FAM [PLANTED] — hosted at TC12-ENV.score-build … [PARSE], [REAL] hosted at TC12-SCORE'. L-0.18: 'The parse at the REGISTRATION stage is this section's block F-FAM-PINS (… a different FID, so F-ROLL never counts it as F-FAM)'. Paste: 'FIXTURES: the contract's list whole, hosted as CANON-24 maps them'; RC-2 'no fixture leg beyond the canon's'.

**The fact.** F-FAM [PLANTED] needs a ruler with a call counter, a BUILT row on a synthetic book, tests_spent and the CLOSED cell — scorer objects that exist from TC12-ENV.score-build; nothing at TC12-REG can call a ruler. A block of FID F-FAM in FIXTURES_REG.txt would also be counted by F-ROLL as the contract's F-FAM on a lighter proof.

**DEFAULT TAKEN.** FIXTURES_REG.txt hosts exactly CANON-24's row: F-CONTRACT-PIN, F-REG [SLICE] [HASH] [WRITE-ONCE] [TEMPLATE] [SPEC-VERBATIM] [VERIFIER], F-ATTEST-ORDER [REG] — 8 blocks, no F-FAM block. The registry's half of the law is held inside those legs (PRECOND-GRAMMAR plants: a precondition in prose, a numeric `required`; preconditions_of() returns 0/0/0/2/1 items; family, m and bar per payload) and by Unit B's F-FAM-PINS, which I ran into a scratch --root against the filed registry: GREEN, '5 payloads carry the parse's family, m and bar'. If the orchestrator rules an F-FAM instance must stand at TC12-REG it is an added leg to this suite plus a transcript refile; the registry files do not move.

**Status.** Ruled at the TC12-REG gate: AM-24.

---

## AP-24 · 2026-10-09 (~21:40Z) · L-X.18 · unit D at TC12-REG (build)

**Title.** A spec block's byte-for-byte boundary includes the frozen text's blank lines and section rule

**Readings.** L-X.18 (block = heading to the next line beginning '### ' or '## '; carry law: fifteen top-level bullets, any other field HALTs)

**The texts.** L-X.18: 'Each §1.k block is the frozen LEANS's ### REGISTRATION SPEC · <id> block byte for byte (from that heading to the next line beginning ### or ##)' vs 'a spec block is fifteen top-level bullets … a missing, extra, renamed or reordered field HALTs'.

**The fact.** P-SFP-VA-1's frozen block ends with a blank line and the section rule of hyphens (LEANS.md:11015-11016) before '### OPEN TO OPERATOR'; every block opens and closes with a blank line. Carried byte for byte they are lines that are neither bullets nor wrapped lines.

**DEFAULT TAKEN.** The plan carries every line after the heading byte for byte (the plan's own heading is '### 1.k <id>'; PLAN==LEANS compares the bodies). The carry law drops leading and trailing blank lines and a trailing all-hyphen rule line and HALTs SPEC-GRAMMAR on any other line that is no bullet and no wrapped line. Stated in REGISTRY_PIN.json's spec_carry_law.

**Status.** Ruled at the TC12-REG gate: AM-25.

---

## AP-25 · 2026-10-09 (~21:40Z) · L-X.18, L-X.19 · unit D at TC12-REG (build)

**Title.** A field written with a head sentence AND sub-bullets is filed {text, items}

**Readings.** L-X.18 carry law ('one level of sub-bullets becomes a list'), L-X.19 ('a field written with sub-bullets is a LIST')

**The texts.** L-X.19: 'operative_spec.arms and operative_spec.labels always are [a list], and operative_spec.preconditions is one unless it is the word none'.

**The fact.** P-DIR-1 and P-SFP-VA-1 write `disclosed_beside` and `failure_conditions` as a head sentence ('each Tier-E, no verdict word.' / 'each a fixture leg with its planted mutation.') followed by sub-bullets. A bare list would drop the head's words; the readings name no form for this case.

**DEFAULT TAKEN.** X's carry_spec mirrored (the precedent L-X.18 names): head only -> string; sub-bullets only -> list; head and sub-bullets -> {"text": head, "items": [...]}. `arms` and `labels` must be lists (SPEC-GRAMMAR otherwise); no word is dropped (the suite's word-level oracle holds every filed leaf to the words of its LEANS field). Consumers of disclosed_beside / failure_conditions must accept all three shapes.

**Status.** Ruled at the TC12-REG gate: AM-26.

---

## AP-26 · 2026-10-09 (~21:40Z) · the resume paste and O-36 · unit D at TC12-REG (build)

**Title.** 'The filing asserts the rule states the parsed q, m and bar' cannot be built on two rows

**Readings.** L-X common clauses under '### REGISTRATION SPEC · (none owned by L-X)' (LEANS.md:7256-7258); AP-1

**The texts.** 'The filing asserts the rule states the parsed q, m and bar, N_BOOT, both seeds and the template.' AP-1: the seam pass 'dropped their inline family constants' from P-DIR-1, P-SFP-VA-1 and P-SCALP-3.

**The fact.** P-DIR-1's and P-SFP-VA-1's verdict_rule carry no numeral for q, m or the bar (only 'q ÷ m'); as written the assertion would HALT the filing of two registered rows, and making it pass would be a re-draft of their verdict text.

**DEFAULT TAKEN.** On verdict_rule the filing asserts N_BOOT (4000), the seed (20261008), the sensitivity seed (20260816) — detector RULER-TEXT — and the one template (TEMPLATE). m and the bar are asserted on the block's checked fields family_m / family_bar against the pin door's parse (FAMILY-M-COUNT, FAMILY-BAR). q is not asserted in the rule text. All five rows pass as written.

**Status.** Ruled at the TC12-REG gate: AM-27.

---

## AP-27 · 2026-10-09 (~21:40Z) · L-X.21, L-X.20 · unit D at TC12-REG (build)

**Title.** ATTEST-REG: what 'the listing of every file then on disk' can mean at a gate that writes after it

**Readings.** L-X.21 clause 3 (ATTEST-REG), L-X.20 (the commit ADDS REG_SET, MODIFIES tierc12_progress.py and PROGRESS.json); unit brief D

**The texts.** L-X.21: 'scripts/tierc12_*.py == {tierc12_progress.py} ∪ REG_SET's scripts. registrations/ATTEST_REG.json is the sorted listing (path, sha), taken after --file, of every file then on disk except itself.'

**The fact.** progress/TC12-REG.json carries ATTEST_REG.json's own sha, so it can never be on disk at its final bytes when the listing is taken; the stage's four transcripts are written by the suites run after it; PROGRESS.json and scripts/tierc12_progress.py are modified by the gate. An exact listing-equals-disk test is RED by construction at every gate.

**DEFAULT TAKEN.** `--attest` lists exactly what it sees and HALTs ATTEST-REG (writing nothing) on a file outside PRE_REG ∪ REG_SET, a .parquet outside x_rec/, a tierc12 script outside the typed set, or an unfiled registry; REG_SET members not on disk are listed under `absent` (now: progress/TC12-REG.json). It is re-runnable (not write-once). F-ATTEST-ORDER [REG] holds the set law on the live disk with no exemption, and listing == disk outside seven typed paths LATER_T (the four TC12-REG transcripts, progress/TC12-REG.json, PROGRESS.json, scripts/tierc12_progress.py). Any other file edited or added after the attestation is RED until --attest is re-run.

**Status.** Ruled at the TC12-REG gate: AM-28.

---

## AP-28 · 2026-10-09 (~21:40Z) · L-X.19, L-X.20, L-X.22 · unit D at TC12-REG (build)

**Title.** Keys and signatures beyond L-X.19 / L-X.20 / L-X.22's lists

**Readings.** L-X.19 (top keys 'in this order'), L-X.20 (pin keys), L-X.22 (verify_filing signature); unit brief D ('the resume paste (as `resume_paste`)')

**The texts.** L-X.22: 'verify_filing(doc, pin, contract_bytes, reg_bytes, ext_bytes, plan_bytes, leans_bytes) -> list[str]'.

**The fact.** The brief orders a `resume_paste` pin that L-X.19's list does not hold. The pin door's ONE prefix function reads a path and its family parse needs a door, while the verifier is handed bytes. No reading states where the pin's three law strings or `verdict_law` come from when the filer 'types no text'.

**DEFAULT TAKEN.** REGISTRATIONS.json gains `resume_paste {path, sha256}` directly after `contract` (L-X.19's other keys keep their order); REGISTRY_PIN.json gains `resume_paste` and `tier`. verify_filing keeps the seven positional parameters and adds keyword `door=None` (default: the tree's pin door); it writes the handed contract bytes to a scratch file under $TMPDIR and judges them through a pin door over that file. `verdict_law` and the pin's spec_carry_law / witness_law / text_before_result_law are read verbatim from the plan's §2; each clause of verdict_law is asserted to be a substring of the frozen ruler sentence. At filing only, beyond L-X.22's nineteen detectors: PLAN-TABLE, RECORD-PIN, N-BOOT, LAW-HEAD, PIN-CENSUS-SHA, WRITE-ONCE, ATTEST-REG.

**Status.** Ruled at the TC12-REG gate: AM-29.

---

## AP-29 · 2026-10-09 (~21:40Z) · L-X.17, L-0.24 · unit D at TC12-REG (build)

**Title.** external_context: where a block declares it, and which paths are banned

**Readings.** L-X.17 (external_context, EXTERNAL-SLICE), L-0.24 sets (a)-(f); P-ADM-1 and P-BRD-1 `labels`

**The texts.** L-X.17: 'An external_context item {path, sha256, lines, text} is cut by the same law from another pinned text … its file sha asserted first. The path may not be one of the files TC12's own close acts move (L-0.24's sets (a)-(f) and TC11's contract)'.

**The fact.** No reading gives a machine form for the declaration; the two L-G blocks state it inside the label's `items` as prose: 'external_context `<path>` lines 187-198 (sha256 `<sha>`)' and '… lines 16 and 28 (sha256 `<sha>`)'. The quoted sha is the FILE's sha (measured: STAGE_G.md 440509bc…, X4.md aac2be88…). Sets (d) and (e) are closed only by the stamp proof at TC12-CLOSE.

**DEFAULT TAKEN.** The filer reads the declaration from the label text by one regex; ranges joined by ' and ' are one item each (P-ADM-1: one item, STAGE_G.md:187-198; P-BRD-1: two items, X4.md:16 and :28). The file's sha is asserted against the declared sha, and a copy under x_rec/ also against its X_REC_MANIFEST row. The banned set is tierc12_frozen.STAMP_SETS_T (TC11's contract and sets a, b, c, f); research_outputs/tierc11/stage_g/STAGE_G.md is taken as HISTORICAL (L-0.24: stage documents are untouched).

**Status.** Ruled at the TC12-REG gate: AM-30.

---

## AP-30 · 2026-10-09 (~21:40Z) · L-0.11, L-0.9 · unit E at TC12-REG (build)

**Title.** AP-E1 · the closure scope at a stage's own gate, and UNRECORDED

**Readings.** L-0.11 (SCOPE LAW) · L-0.9 (the gate, steps 1-6)

**The texts.** L-0.11: "its scope is the union of `artifact_shas` paths of the records up to that one in `RESUME_ORDER_T` … the latest record's run additionally flags any matching file on disk that no record names (UNRECORDED)". L-0.9: "(2) the record's suites are re-run … (3) the builder writes the progress record".

**The fact.** At gate steps (1)-(2) the record being gated does not exist, so its own scripts are in no artifact_shas; and an UNRECORDED line inside the transcript would move a filed transcript as soon as the next stage's files appear.

**DEFAULT TAKEN.** While the stage's record is absent, the tierc12 scripts (and build manifests / door tables) on disk that NO record names are in scope as the gated record's own; once the record exists the scope is the records' alone. UNRECORDED is printed on stdout only (a clock line), never in the transcript, never RED. Record files with a known filing stage (data/AS_OF_PIN.json, data/CONTRACT_SPECS.json, env/LINEAGE_PINS.json, analytics/value_area.py) are read by STAGE (typed FILED_AT_T), not by disk state. TC12-D.mirror is in no scope. Consequence: a later record's script must not sit unrecorded on disk when an ORDER-stage closure transcript is filed.

**Status.** Ruled at the TC12-REG gate: AM-31.

---

## AP-31 · 2026-10-09 (~21:40Z) · L-0.14, L-0.9, L-0.11 · unit E at TC12-REG (build)

**Title.** AP-E2 · which transcripts F-FX-FORM reads

**Readings.** L-0.14 (F-FX-FORM) · L-0.9 (gate order) · L-0.11

**The texts.** L-0.14: "or a transcript of record has a block id outside B's grammar, a PASS or FAIL block lacking either `FAILS IF:` line, a NOT RUN block that is not exactly its header and its `[NOT RUN]` line, or a tally line not of C's form".

**The fact.** At a stage's gate its own transcripts are still being written: this run's own, and FIXTURES_RESUME_<id>.txt, which gate step (5) writes after this suite ran. Reading them would make the filed bytes depend on run order.

**DEFAULT TAKEN.** The transcripts scanned are those named by the records strictly BEFORE the stage in RESUME_ORDER_T (a transcript is of record once a record names it); each stage's transcripts are therefore scanned at the next ORDER-stage gate. At TC12-REG the set is empty and printed so; the checker is still proven there on a transcript the harness itself writes in memory (plants and a GREEN control). TC12-CLOSE's own transcripts are scanned by no later run.

**Status.** Ruled at the TC12-REG gate: AM-32.

---

## AP-32 · 2026-10-09 (~21:40Z) · L-0.17 · unit E at TC12-REG (build)

**Title.** AP-E3 · F-TYPED and the unary minus

**Readings.** L-0.17 allow-list (A), (C)

**The texts.** (A) "STRUCTURAL — the integers 0, 1, 2 or the floats 0.0, 1.0 (index, arity, sign, identity)"; (C) "a sub-expression built only from numeric literals must fold to a structural value (no `2 * 2 * 2`)".

**The fact.** Python parses `-1` as UnaryOp(USub, Constant(1)): a sub-expression built only from numeric literals that folds to -1, outside the listed set, although (A)'s parenthesis names "sign".

**DEFAULT TAKEN.** The pessimistic reading: `-1`, `-2`, `-1.0` are TYPED-FOLD findings in a computation module (`x[-1]` is RED; `x[len(x) - 1]` passes). No scanned module at TC12-REG trips it (tierc12_pins is clean). If ruled the other way it is one clause of _structural().

**Status.** Ruled at the TC12-REG gate: AM-33.

---

## AP-33 · 2026-10-09 (~21:40Z) · L-0.22, L-D.1, L-D.23, L-R.24 · unit E at TC12-REG (build)

**Title.** AP-E4 · seam 16: the host block, the pin text scan, the tick detector

**Readings.** L-0.22 seam 16 · L-D.1 / F-D-PIN [e] · L-D.23 / F-TICK [b] · L-R.24

**The texts.** Seam 16: "the closure suite's AST sweep re-runs them … (the same legs on a wider scope; no new block id)". F-TICK [b]: "(AST: a `BinOp` with a name containing `tick` under a `Compare`)". L-D.23 / L-R.24's own lawful expression: "`grid.dec(low) < grid.dec(P) − n_tick·grid.T`".

**The fact.** No block is named for the two detectors; the tick detector as written flags the reading's own exact Decimal expression (n_tick is a tick-named operand of a BinOp under a comparison); before TC12-D neither TC12's pin record nor the tick capture is on file.

**DEFAULT TAKEN.** Hosted in F-CLOSURE [ii] (detectors PIN-LITERAL, TICK-LITERAL, TICK-FLOAT-COMPARE), over every non-fixture source. Pessimistic tick rule: ANY BinOp with a direct tick-named operand under a Compare is RED, so a consumer forms the depth in a statement of its own before comparing. The pin scan is a raw TEXT scan (comments and docstrings included; ms digits with optional underscores; the ISO instant to the minute). Before TC12-D the referee is O-7's printed value in ORCHESTRATOR_RULINGS.md plus TC11's pin record (TC10's pin from its tc10_pin keys); the tick-literal clause has no referee and says so.

**Status.** Ruled at the TC12-REG gate: AM-34.

---

## AP-34 · 2026-10-09 (~21:40Z) · L-0.2, L-V.23 · unit E at TC12-REG (build)

**Title.** AP-E5 · F-SEED: the wrapper list, the scope, X_SEED_MIRROR_T's unnamed member

**Readings.** L-0.2 (F-SEED) · L-V.23 / F-VA-NULL [a] · L-L (tierc12_era.compute)

**The texts.** "a call whose callee is in the fixture-typed ruler list (`cluster_boot`, `cluster_boot_diff`, `loao_n`, `default_rng`, and every TC12 wrapper of them)"; "allowed only inside the functions typed `X_SEED_MIRROR_T` (the F-VA-NULL stream builder; `tierc12_era.compute` with `seed_source = "x"`)".

**The fact.** No reading names the TC12 wrappers (they are born with their builders), and none gives the function name of DOOR 2's F-VA-NULL stream builder.

**DEFAULT TAKEN.** Wrappers are found by AST — a function with a `seed` parameter whose body calls a ruler or another wrapper — and printed in the transcript; the three lineage rulers must be handed `seed=` by keyword. Scope = every non-fixture GLOB member, process tools included (a suite's default_rng form is F-FX-FORM's). X_SEED_MIRROR_T holds (tierc12_era, compute) only; once tierc12_va_trades is in scope F-SEED is RED until its stream builder's name is typed by a dated amendment (first closure gate after TC12-V.trades: TC12-C).

**Status.** Ruled at the TC12-REG gate: AM-35.

---

## AP-35 · 2026-10-09 (~21:40Z) · L-0.2 · unit E at TC12-REG (build)

**Title.** AP-E6 · F-SEED and the sensitivity seed

**Readings.** L-0.2 (F-SEED; "The sensitivity seed printed beside every ruler is `T5.SEED`") · L-X (the `seed_sens` leaf: "the row's ruler at the sensitivity seed"; `E.SEED_SENS`)

**The texts.** F-SEED: "A seed expression resolves iff every leaf is the pin-door seed (or `E.SEED`), an integer draw index, or a `crc32` call". L-X: "`seed_sens` | the row's ruler at the sensitivity seed".

**The fact.** A ruler call at `E.SEED_SENS` or `E.T5.SEED` — which the scorer must make for the seed_sens leaf — does not resolve under F-SEED's rule as written.

**DEFAULT TAKEN.** Built to the letter: only the pin-door seed (a call on tierc12_pins naming `seed`, or a name bound to one) and `E.SEED` exactly resolve; `seed=E.SEED_SENS` is SEED-UNRESOLVED (planted and printed). The scorer filed at TC12-ENV.score-build will read RED at the TC12-V closure gate unless this is ruled first.

**Status.** Ruled at the TC12-REG gate: AM-36.

---

## AP-36 · 2026-10-09 (~21:40Z) · L-0.22 · unit E at TC12-REG (build)

**Title.** AP-E7 · leg (ii) on the lineage, and what a sys.modules reach is

**Readings.** L-0.22 leg (ii) · its SOURCE line (scripts/tierc11_closure_fixtures.py)

**The texts.** "(ii) AST over each decision source and the static repo closure of its imports: … no constant-string `import_module` / `__import__`; no non-constant import site other than a door L-D declares; no `exec` / `eval` / `compile`; no `sys.modules` reach".

**The fact.** scripts/tierc6.py:1160 and scripts/tierc7.py:1044 (frozen lineage, in every shim-armed closure) hold a name-held `__import__(name)`, so the clause applied to the closure is RED by construction; and the shim's own exit check must read sys.modules.

**DEFAULT TAKEN.** The strict clause binds decision sources and doors. For LINEAGE sources TC11's filed law is used: a name-held dynamic import is resolved to the repo modules its literal table names, and a forbidden target or an unresolved site is the finding (dev-run over the real lineage text: 39 modules, no finding). A sys.modules reach is a subscript / get / pop / setdefault with a FORBIDDEN constant key (TC11's form). DYN_DECLARED_T = tierc12_env.tc10_import (L-D.26 hunk 7).

**Status.** Ruled at the TC12-REG gate: AM-37.

---

## AP-37 · 2026-10-09 (~21:40Z) · L-0.17, L-D.25, L-D.26 · unit E at TC12-REG (build)

**Title.** AP-E8 · F-TYPED rule (G) without the hunk list

**Readings.** L-0.17 allow-list (G) · L-D.25 / L-D.26 (the hunks) · L-D F-D-PORT

**The texts.** "(G) REFEREED TEXT — a literal inside vendored text proven byte-identical to its committed referee outside the declared hunks, or inside a function proven AST-identical to its filed source … a literal inside a declared hunk is scanned like any other".

**The fact.** The hunk list is the vendor tool's data (TC12-ENV.vendor) and the port list is read off comments by L-D's suite; neither is on file at TC12-REG, and this suite cannot import them.

**DEFAULT TAKEN.** A STATEMENT of a module with a typed referee whose ast.dump equals a statement of the referee's text is the referee's; every other statement is scanned. REFEREES_T today: tierc12_env -> vendor/tierc11_env@1526093b.py, tierc12_data -> scripts/tierc11_data.py. Referees for later ports (era, forward, ferry) are typed when those modules are filed. A statement that changed in one token is scanned whole, so referee literals inside a hunk-touched multi-line statement will read as findings.

**Status.** Ruled at the TC12-REG gate: AM-38.

---

## AP-38 · 2026-10-09 (~21:40Z) · L-L.3, L-L.5, L-L.18, L-0.22, L-0.17 · unit F at TC12-REG (build)

**Title.** AP-F1 · forward_log imported by the spec tool (L-L) versus the import-closure wall as built (L-0.22 ii)

**Readings.** L-L.3, L-L.5, L-L.18 (F-FWD-SPEC AST clause) vs L-0.22 (ii) and its sentence on --stage=TC12-REG; L-0.17 rule (G)

**The texts.** L-L.3: "Producer. scripts/tierc12_forward_spec.py, a plain process: stdlib, FL, tierc12_progress.certified and the pin door". L-L.5: "The law (FL, called and never re-implemented in production)". L-0.22: "(ii) AST over each decision source and the static repo closure of its imports: no Import / ImportFrom of a forbidden name anywhere (function bodies included)" and "At --stage=TC12-REG the suite runs [ii] and [iii] only (no module then in scope reaches the lineage, asserted)".

**The fact.** scripts/forward_log.py:308-309 (inside main()) holds `import analytics` and `import brief2 as B2`; scripts/brief2.py:37 holds `from analytics import profile as P`. Measured with the closure suite's own static_walk / scan_ii on a scratch probe module holding `import forward_log as FL`: the walk reaches [analytics, analytics.levels, analytics.momentum, analytics.nesting, analytics.structure, analytics.volatility, analytics.vwap, brief2, forward_log] and reports `CLOSURE-IMPORT [lineage] brief2 line 37: imports analytics.profile — the forbidden name analytics.profile` at every stage, plus `CLOSURE-REACH: at <stage> no module in scope may reach the lineage` before TC12-ENV. Separately, F-TYPED's rule (G) table REFEREES_T (tierc12_closure_fixtures.py:176-177) names no referee for tierc12_forward_spec, so forward_log.last_sha's `lines[-1]` reads TYPED-FOLD in a VERBATIM port.

**DEFAULT TAKEN.** The pessimistic reading (the wall holds): tierc12_forward_spec.py does NOT import forward_log. Its six chain functions stand in the module as ports under the section's own port law — canonical, chain_hash, read_lines, append_entry, verify_chain VERBATIM; last_sha CHANGED by the one token `lines[-1]` -> `lines[len(lines) - 1]` — and are exposed as the namespace `FL` so X's ported call sites (chained, append, chain_findings) are unchanged. Every production run HALTs FWD-FL-PORT unless they are AST-identical (under that one declared substitution) to scripts/forward_log.py at the sha X's spec names (74e9657f…1967). The SUITE imports forward_log itself as the independent verifier: F-LEDGER [CHAIN] runs forward_log.verify_chain on every file and requires the port to return forward_log's own result; F-PORT holds every label. No byte of BOOK_SPEC_COMBINED.json or of the ledger depends on the choice. If overruled: the one line `import forward_log as FL` replaces the port block, and the closure suite then needs a forward_log clause (disclosed, not walked).

**Status.** Ruled at the TC12-REG gate: AM-39.

---

## AP-39 · 2026-10-09 (~21:40Z) · L-L.3, L-0.4, L-0.9 · unit F at TC12-REG (build)

**Title.** AP-F2 · "a TC12 file through certified" before the parent record exists

**Readings.** L-L.3 (the sha-first reader), L-0.4 (certified HALTs if no record names the path), L-0.9 (the parent record of TC12-REG is written by the orchestrator's gate step)

**The texts.** L-L.3: "Every read is sha-first: … a TC12 file through `certified`". L-0.4: "`certified(rel_path)` … returns the LAST record naming the path; HALT if none".

**The fact.** At this build research_outputs/tierc12/progress/TC12-REG.json is not on file, so certified('research_outputs/tierc12/registrations/REGISTRATIONS.json') HALTs: `no record under research_outputs/tierc12/progress names that path`.

**DEFAULT TAKEN.** The two registry files are held at EVERY run by the registry's own pin and chain — REGISTRY_PIN.json `registrations_file` {path, bytes, sha256} must be the file, and the head recomputed from the five payloads must equal the head both files carry (HALT FWD-REGISTRY) — and ALSO through certified() from the moment any progress record names them (a mismatch HALTs FWD-READ). Tested on a scratch root: the spec's bytes are identical with and without a TC12-REG record; a record naming another sha HALTs. The transcript prints nothing that depends on which records exist.

**Status.** Ruled at the TC12-REG gate: AM-40.

---

## AP-40 · 2026-10-09 (~21:40Z) · L-L.3, L-0.24 · unit F at TC12-REG (build)

**Title.** AP-F3 · SPEC_READS_T omits two files the same reading's sha law opens

**Readings.** L-L.3 (SPEC_READS_T; "an X file against its manifest row"; "or at the stamped value L-0.24 allows"), L-0.24

**The texts.** L-L.3 lists: the contract; progress/STEP_Q.json and TC12-R0.json; TC12's REGISTRATIONS.json and REGISTRY_PIN.json; under XR/ X's ledger, X's spec and the texts XF, XB; TC11's ledger, registry, registry pin, LEANS.md, AS_OF_PIN.json and PROGRESS.json; the 18 lineage files.

**The fact.** The X sha law cannot run without opening research_outputs/tierc12/x_rec/X_REC_MANIFEST.json, and the stamped-value acceptance of TC11's PROGRESS.json cannot run without opening research_outputs/tierc12/close/TC11_STAMP_MAP.json (when it exists).

**DEFAULT TAKEN.** Both paths are typed in SPEC_READS_T (17 typed paths; the 18 lineage files are added by object from X's `path_modules`). The stamp map is read only if on file and accepted only when it reads applied: true and names the bytes (the form tierc12_frozen.py reads: moved[{path, sha256_before, sha256_after}]). The suite types the same list as its second object; a path outside it HALTs SPEC-READS.

**Status.** Ruled at the TC12-REG gate: AM-41.

---

## AP-41 · 2026-10-09 (~21:40Z) · L-0.17, L-0.19, L-L.18 · unit F at TC12-REG (build)

**Title.** AP-F4 · the flow witness of ledger.opening and ledger.n_min at the ledger-spec record

**Readings.** L-0.17 (the flow leg; "the pin's consumer makes it at its own stage, as that pin's flow-leg witness"), L-0.19 seam 2, L-0.17 seam 63, L-L.18 seam 1 and its three F-TYPED-FLOW rows, PIN_REGISTER.json rows ledger.opening / ledger.n_min / seed

**The texts.** L-L.18: "F-TYPED-FLOW [ledger.opening] | the pin bent by one 4h bar at its door does not change the admitted set of the scratch ledger"; "[ledger.n_min] | on a scratch ledger holding n_min − 1 rows, the pin bent down by one at its door does not flip the first half of the status string". Seam 1: "every flow leg of this section prints L-0.17's fixed line `[FLOW] <pin> @ <door>: <witness> moved`". Seam 2 hosts one block per consumed pin at TC12-REG.ledger-spec.

**The fact.** At this record no row exists and no scratch ledger is ridden; `admitted` and `diary_status` are TC12-L's. What the spec tool does with both pins is compare them (L-L.8: "The file value is what code uses; the contract's is compared"); the register's own `equal_to` row for each names TC12-REG.ledger-spec with HALT FWD-OPENING / FWD-NMIN. The register's witness texts name the scratch ledger, which cannot move here.

**DEFAULT TAKEN.** Three F-TYPED-FLOW blocks are hosted. [adm.lag_cut]: the registered witness moves (p_win_1_refuses flips on the planted lag = CUT − 1 row) and the register's own line is printed. [ledger.opening] and [ledger.n_min]: the pin is bent at its door, production's spec_doc must HALT FWD-OPENING / FWD-NMIN, and the [FLOW] line is printed in L-0.17's form with the witness that actually moved ("the FWD-OPENING assertion of the spec tool (the build HALTs there, L-L.8)", "the FWD-NMIN assertion … L-L.14") — never the register's scratch-ledger sentence, which would be untrue here. Each block's plant is a shadow copy of the spec module holding a typed copy of EQUAL value (PIN-NOT-READ). No F-TYPED-FLOW [seed] block is hosted: nothing is drawn at this record.

**Status.** Ruled at the TC12-REG gate: AM-42.

---

## AP-42 · 2026-10-09 (~21:40Z) · L-L.8, L-L.3 · unit F at TC12-REG (build)

**Title.** AP-F5 · FWD-OPENING at the spec stage: the two TC10 objects

**Readings.** L-L.8, L-L.3 (SPEC_READS_T; no env)

**The texts.** L-L.8: "HALT FWD-OPENING unless it equals every one of: opening_ms on ledger lines 1-3 and 5; E.TC10_PIN_MS (L-D: T11/data/AS_OF_PIN.json → tc10_pin_close_ms); research_outputs/tierc10/STEP0_RECORD.json → as_of_last_closed_4h_close_ms (read through E.tc10_record …); TC11's GENESIS opening_ms; the one capture of … L-T.6; and the contract's own literal".

**The fact.** The spec tool is env-free (no E) and research_outputs/tierc10/STEP0_RECORD.json is not on SPEC_READS_T.

**DEFAULT TAKEN.** At this record the opening (X's spec opening.ms, the value code uses) is held equal to: opening_ms of X's three book_open lines, T11/data/AS_OF_PIN.json tc10_pin_close_ms (the object L-L.8 itself names for E.TC10_PIN_MS), TC11's GENESIS opening_ms, the L-T.6 capture, and the contract pin ledger.opening parsed to ms; line 5 is then written with that value and checked by S4. The shim's TC10 pin and TC10's STEP0 record are left to the TC12-L refresh, and the spec says so in `opening_held_equal`.

**Status.** Ruled at the TC12-REG gate: AM-43.

---

## AP-43 · 2026-10-09 (~21:40Z) · L-L.7, L-L.18, L-L.2, L-L.3 · unit F at TC12-REG (build)

**Title.** AP-F6 · F-FWD-SPEC and F-PORT hosted at the ledger-spec record as well

**Readings.** L-L.7 ("the five blocks on the five-line file"), L-L.18 (its table is read at --stage=TC12-L), L-L.2 / L-L.3 FAILS-IF (name F-FWD-SPEC), the L-L header ("Each suite below carries a leg F-PORT")

**The texts.** L-L.18: "`scripts/tierc12_forward_fixtures.py --stage=TC12-L` … hosts L-L.7's five F-LEDGER blocks on the refreshed file and the blocks below." L-L.3: "FAILS-IF: block F-LEDGER [REHASH] (L-L.7) and F-FWD-SPEC (L-L.18)."

**The fact.** The spec, its gate-text selector and the ports are frozen by THIS record's commit (T3), before TC12-L exists; every clause of F-FWD-SPEC but one (a ride's TP.ride_spec, plant anchor_offset -> FWD-SPEC-RIDE) and every F-PORT clause is evaluable without the env.

**DEFAULT TAKEN.** F-FWD-SPEC (its env-free clauses and eight of its nine listed plants, plus the SPEC-READS / SPEC-VA-BLIND plants of seam 62) and F-PORT are hosted at --stage=TC12-REG.ledger-spec; the block says in its PASS line that the ride clause is TC12-L's. TC12-L hosts both again with the ride clause. 10 blocks at this record instead of 5.

**Status.** Ruled at the TC12-REG gate: AM-44.

---

## AP-44 · 2026-10-09 (~21:40Z) · L-X.19, L-X.20, L-X.18 · unit D at TC12-REG (fix)

**Title.** Unit D (V-9): three mechanics choices in the write-once filing beyond the key lists of L-X.19 and L-X.20

**Readings.** L-X.19, L-X.20, L-X.18 (carry law); O-36

**The texts.** L-X.19: "top keys, in this order: `tier` · `contract {…}` · `leans {path, sha256}` · `amendments` · `review` · `plan` · `rulings` · `disclosures` · `families` · `verdict_law` · `statistics` · `scored_window` · `era_cut` · `registrations [5]` · `chain [5]` · `head` · `law` · `law_source`" (eighteen) and "A field written with sub-bullets is a LIST under L-X.18's carry law". L-X.20's pin list holds neither `tier` nor `resume_paste`. L-X.18: "Carry law (X's SPEC_CARRY_LAW, mirrored from carry_spec) … one level of sub-bullets becomes a list". Against these: the unit brief orders the registry to pin the resume paste "as `resume_paste`", and O-36 makes the paste a text that binds beside the contract.

**The fact.** (1) REGISTRATIONS.json files nineteen top keys: `resume_paste {path, sha256}` stands after `contract`; the readings were frozen without a key for the paste. (2) REGISTRY_PIN.json carries `resume_paste` and `tier` beyond L-X.20's list; X's REGISTRY_PIN_X.json, the precedent L-X.20 cites, carries `tier`. (3) Four leaves — `disclosed_beside` and `failure_conditions` of P-DIR-1 and P-SFP-VA-1 — are frozen with a head sentence AND sub-bullets. L-X.18 does not say where the head goes; X's carry_spec, which the carry law mirrors, files that shape as {text, items} (X's filed P-SFP-RNG-1 `precondition` is such a dict). They are filed {text, items}. Every word is carried verbatim (the suite's word-level oracle REFEREE-SPEC holds it); none of the four is machine-read under L-X.18's grammar; the plan's section 2 and the pin's spec_carry_law state all three choices. No registered row's population, arms, statistic, verdict rule or labels is touched.

**DEFAULT TAKEN.** The filing stands as filed: head bbbc6cab…, REGISTRATIONS.json sha f3bbe260…, nothing re-filed. If the ruling goes for L-X.19's letter, the only window is before the TC12-REG commit: the carry becomes [head] + items and the extra keys drop in tierc12_registrations.py and the plan's section 2, the uncommitted pair is removed and --file re-run. Payload shas and the head then move, and unit F's spec, which pins the head, must be rebuilt.

**Status.** Ruled at the TC12-REG gate: AM-45.

---

## AP-45 · 2026-10-09 (~21:40Z) · L-X.21, L-0.11, L-X.20, L-X.19 · unit D at TC12-REG (fix)

**Title.** Unit D (V-1): how F-ATTEST-ORDER [REG] judges "ATTEST_REG.json is not that listing" after the attested instant

**Readings.** L-X.21 (ATTEST-REG, FAILS-IF), L-0.11 (scope law), L-X.20 (what the commit adds and modifies), L-X.19 and O-35 (append-only amendments)

**The texts.** L-X.21: "`registrations/ATTEST_REG.json` is the sorted listing (path, sha), taken after `--file`, of every file then on disk except itself"; FAILS-IF "… or `ATTEST_REG.json` is not that listing"; "`TC12-REG.ledger-spec` … is filed AFTER the attested instant and is covered by that descendant test". L-0.11: "an earlier record's transcript stays reproducible after later records add files". L-X.20: the commit "modifies only `scripts/tierc12_progress.py` and `PROGRESS.json`" and adds the stage's transcripts and record, which are written after the listing. O-35: proposals and amendments are appended before each gate.

**The fact.** A real leg that compares the listing with the disk as it stands at each later run cannot re-pass: the stage's own transcripts and record, PROGRESS.json, appended amendments and every later record's files all postdate the listing. The readings do not say which listed paths stay held.

**DEFAULT TAKEN.** Built in tierc12_registrations_fixtures.py only; production is unchanged. The real leg judges the LISTING: production's attest_findings and the suite's typed sets run over the listed paths. Every listed path must be on disk at its listed sha, except (a) LATER_T — the four TC12-REG transcripts, progress/TC12-REG.json, PROGRESS.json and scripts/tierc12_progress.py — which are not held, and (b) APPEND_ONLY_T — LEANS_AMENDMENTS.md and AMENDMENTS_PROPOSED.md — where a byte-prefix of the file must hash to the listed sha. A REG_SET member the listing names `absent` must not have appeared, outside LATER_T. A path the listing does not name is no finding here (ATTEST-ORDER holds it to git ancestry at TC12-SCORE and CLOSE). x_rec/ paths resolve through the main tree. The break leg gains a control (an appended amendment, a later record, a ledger-spec file, the stage's record and a re-merged PROGRESS.json leave the listing silent) and an eighth plant (an append-only text edited inside its listed bytes → ATTEST-LISTING); the seven earlier plants are unchanged.

**Status.** Ruled at the TC12-REG gate: AM-46.

---

## AP-46 · 2026-10-09 (~21:40Z) · L-0.2, L-0.14 · unit A at TC12-REG (fix)

**Title.** The harness self-test proves the stream-seed form on integer draws, not on the tier seed

**Readings.** L-0.2 (Seed; F-SEED's resolve rule) against L-0.14 (the harness is stdlib only) and L-0.14 F

**The texts.** L-0.2: a seed expression resolves iff every leaf is the pin-door seed (or E.SEED), an integer draw index, or a crc32 call; a seed read by key from a record is allowed only inside X_SEED_MIRROR_T. L-0.14: scripts/tierc12_fx.py is stdlib only, so it cannot import the pin door.

**The fact.** The self-test read the seed from PROGRESS.json key `seed` and handed it to `_rng_legs(seed)`, which F-SEED classes as a wrapper of a ruler, giving SEED-X-OUTSIDE-MIRROR at tierc12_fx._self_test. The harness has no lawful way to hold the tier seed for a ruler call.

**DEFAULT TAKEN.** Took the verifier's primary fix: `_RNG_DRAWS_T = 3`; `_rng_legs()` takes no argument and runs `_st_rng(draw)` for draw in range(_RNG_DRAWS_T). The leg's law is the FORM [SEED, crc32('<suite tag>|<block id>')], which does not depend on the seed's value; the three plants still go RED by their named detectors. Mechanics only: no registered row is touched. Not changed, because V-3 did not require it: `_self_test` still reads PROGRESS.json key `seed` for its printed header line and for `_det_legs(tmp, seed)` (the PYTHONHASHSEED twin label). Neither is a ruler or wrapper call and F-SEED does not flag them; the orchestrator may want to rule whether that read should stand.

**Status.** Ruled at the TC12-REG gate: AM-47.

---

## AP-47 · 2026-10-09 (~21:40Z) · L-L.7, L-L.5, L-0.9 · unit F at TC12-REG (fix)

**Title.** P7 (new, V-7) — at --stage=TC12-REG.ledger-spec the transcript PRINTS the five-line file; [CHAIN] and [STRUCTURE] JUDGE the whole working file

**Readings.** L-L.7 (the suite's two runs; [CHAIN] / [STRUCTURE] failure conditions; planted mutation 5), L-L.5 (the commit law), L-0.9 (gate step 2: re-run without drift)

**The texts.** L-L.7: at the ledger-spec record 'the five blocks on the five-line file' — against L-L.7: '[CHAIN] FAILS IF FL.verify_chain is not ok' / '[STRUCTURE] FAILS IF any of S2-S7 of L-L.6 is breached' / plant 5 'a second book_open for the fourth book appended later -> STRUCTURE S4'. L-L.5: the working file grows at TC12-L and the earlier record's bytes must remain a byte-prefix of it; the earlier transcript must re-run byte-identical.

**The fact.** With the real legs reading only the first five lines, a breach standing after line 5 of the working file passed: measured on a scratch copy of the tree before the fix, ten tail mutations (the verifier's a, b, c; a torn line; a blank line; an unknown kind; a file ending on a row; a compact-separator line; a bare NaN) each gave exit 0, 10 GREEN and the unchanged transcript a8b3537a…. A transcript that printed anything of the tail would drift at TC12-L's lawful append.

**DEFAULT TAKEN.** The pessimistic reading: the real legs of F-LEDGER [CHAIN] and [STRUCTURE] run their detector over the first five lines AND over the whole working file (working_fx: forward_log.verify_chain, the ported verify_chain, the suite's own hash loop with its byte / NaN / line-break laws; production's chain_findings S1-S7) and fail on any finding; on GREEN nothing tail-dependent is printed. Consequence to rule on: a breach in TC12-L's tail turns THIS record's [CHAIN] / [STRUCTURE] RED as well as TC12-L's own. [PREFIX] already read the whole file for the byte-prefix law; [REHASH] and [ANCESTORS] stay on lines 1-5 (their failure conditions name only those).

**Status.** Ruled at the TC12-REG gate: AM-48.

---

## AP-48 · 2026-10-09 (~23:36Z) · L-0.22, L-D.3, L-D.5, L-D.6, L-D.11, L-D.24 · TC12-D (fix pass)

**Title.** CLOSURE-REACH at TC12-D: the closure suite asserts 'no lineage reach' at every stage before TC12-ENV, but the readings order the Stage D builder to import the lineage (verifier D-1, BLOCKING at the gate)

**Readings.** L-0.22 (FAILS-IF, lines 1456-1459), L-D register of constants (2019, 2024, 2028), L-D.3, L-D.5, L-D.6, L-D.11, L-D.24

**The texts.** L-0.22: "At `--stage=TC12-REG` the suite runs `[ii]` and `[iii]` only (no module then in scope reaches the lineage, asserted); legs (i), (i-b), (iv) and (v) need the shim and first run at TC12-ENV". L-D register: "`MS_4H` and every native step | `engine.cells.INTERVAL_MS`"; "taker bps per side ... the objects `tierc2_rules.FEE_BPS_SIDE`, `FEE_BPS_ROUND_TRIP`"; "drive-wait attempts · delay | the objects `drive_wait.DEFAULT_ATTEMPTS`, `DEFAULT_DELAY`". L-D.3: "Guard `guard_substrate(env)`, at import of `scripts/tierc12_data.py`, before `engine.data` is imported". L-D.6: "`ED._save_cache` (merge, no-shrink ...)", "`ED.backfill_funding`". L-D.24: "`r = wait_for_drive("/Volumes/LaCie")`".

**The fact.** scripts/tierc12_closure_fixtures.py:1387 `if not stage_at_least(stage, SHIM_STAGE_T) and (walk["lineage"] or walk["tc10"])` raises CLOSURE-REACH at every stage before TC12-ENV. Re-measured in the fix pass into a scratch --root: exit 1, 5 GREEN, 1 RED (F-CLOSURE [ii]); the one finding: 'at TC12-D no module in scope may reach the lineage; the static closure holds [drive_wait, engine, engine.cells, engine.data, engine.htf, engine.indicators, engine.journal, engine.s1, engine.shadows, engine.signals, engine.trading, tierc2_rules]'. No tierc10_* / tierc11_* module, no shim and no analytics module is reached; no PIN-LITERAL, TICK-LITERAL, TICK-FLOAT-COMPARE or F-TYPED finding. Nothing in TC12-D's own files can remove the finding without breaking L-D.

**DEFAULT TAKEN.** Stage D built as L-D orders (the four lineage imports stand; tierc12_data.py never imports the shim, tierc10_data or tierc11_data). The closure suite is not this unit's file and was not touched. Proposed mechanics for the orchestrator's ruling: bind the no-reach assertion at --stage=TC12-REG only, or admit a typed, disclosed Stage D lineage set reachable from tierc12_data alone (the twelve names above), keeping the TC12-REG transcript of record byte-identical; then re-run the closure suite at --stage=TC12-D and file its transcript at the gate.

**Status.** Ruled at the TC12-D gate: AM-49.

---

## AP-49 · 2026-10-09 (~23:36Z) · L-D.18, L-D.19, L-D.20, L-D.21 · TC12-D (fix pass)

**Title.** AM-D-FEE-BINANCE_USDTM / AM-D-FEE-BYBIT_V5_LINEAR: NULL grammar for both venues — neither fee page was retrievable with the library's default headers; the maker pin is the figure on file, flagged

**Readings.** L-D.18, L-D.19, L-D.20, L-D.21, O-19, resume paste ["maker-bps"]

**The texts.** L-D.18: "one request per venue through `ED._get` (its transport retries included, each an `http` log row) with the library's default headers — no forged browser identity"; "A failed capture is a filed status — never a HALT"; "UNRETRIEVABLE with a reason from the closed set {`transport`, `http_<status>`, `off_domain_redirect`, `no_entry_tier_label`, `no_rate_in_body`, `ambiguous`}"; "Where the saved body holds no qualifying figure ..., the amendment files a NULL grammar with the reason (`no_entry_tier_label` or `no_rate_in_body`)"; "What is recorded if unretrievable (O-19): ... `maker_kind = "ON FILE — NOT RE-CONFIRMED"` ... For `BYBIT_V5_LINEAR` the same on-file figure is applied and marked "ASSUMPTION — NOT RE-CONFIRMED; no Bybit figure is on file""; "No figure ever enters by keyboard."

**The fact.** data/FEE_SOURCE.json (sealed): https://www.binance.com/en/fee/futureFee answered HTTP 202 on each of the transport's 4 attempts; https://www.bybit.com/en/help-center/article/Trading-Fee-Structure HTTP 403 on each of 4 (8 http rows, phase fee_source, attempt date 2026-10-09). engine.data._get returns a response only on 200 / 404, so NO body exists: body_path / body_sha256 / body_bytes are null, ~/.cache/naiad/provenance/tc12_20261008/ was never created, and there are no bytes to fix a grammar against. The reading's NULL-grammar reasons presuppose a saved body; here the reason is the acceptance set's `http_202` / `http_403`.

**DEFAULT TAKEN.** data/FEE_GRAMMAR.json filed with `venues` {BINANCE_USDTM: null, BYBIT_V5_LINEAR: null}, `amendment` null and `why_null` per venue; --manifest does not HALT (a grammar is required only for a venue captured with HTTP 200). maker_bps_side = 2.0 bps/side on both venues, read from README.md:150 by the regex `maker is (\d+(?:\.\d+)?)%` x pct_to_bps (never typed): BINANCE_USDTM 'ON FILE — NOT RE-CONFIRMED', BYBIT_V5_LINEAR 'ASSUMPTION — NOT RE-CONFIRMED; no Bybit figure is on file'. maker_retrieved_utc_date null, maker_retrieval_attempted_utc_date 2026-10-09. F-TOLL [data d] and [data f] REAL halves assert exactly this from FEE_SOURCE.json. Nothing is mirrored under /Volumes/LaCie/Naiad/provenance/tc12_20261008/ (0 bodies; the directory was not created). The operator's veto "maker-bps" remains the only door for a hand-given figure.

**Status.** Ruled at the TC12-D gate: AM-50.

---

## AP-50 · 2026-10-09 (~23:36Z) · L-D.11, L-D.15 · TC12-D (fix pass)

**Title.** Port labels follow what F-D-PORT can prove against D11; D11's dead helper `_port_tag` is not ported (verifier D-9, first half)

**Readings.** L-D.11 (the port law), L-D.15 (F-D-PORT)

**The texts.** L-D.11: "TEXT-ONLY: `extend_klines`, `extend_funding`, `capture_contract_specs`, `load_pin`. CHANGED, each named: ... `write_pre_state` (TC11 shas per row) ... `seal_provenance` (seven sealed files) ... Everything else D11 defines is VERBATIM." L-D.15 F-D-PORT: "a port labelled VERBATIM is not AST-identical ...; a port labelled TEXT-ONLY differs from it once string constants are blanked; ... or the port set read off the comments is not `PORTS`".

**The fact.** PORTS holds 95 rows: 63 VERBATIM, 22 CHANGED, 10 TEXT-ONLY. By AST against scripts/tierc11_data.py at the sha TC11's PROGRESS certifies: write_pre_state differs from D11's only in string constants (the reading lists it CHANGED); _assert_bound, clone_findings, contract_multiplier_table, cache_manifest_staleness and summarize differ only in strings (the reading's 'everything else is VERBATIM'); seal_provenance is AST-identical and the change sits in its module constant SEALED_FILES (seven files). D11's tc10_expected_shas / tc10_pin_keys / _tc10_manifest are ported under tc11_* names (CHANGED). D11's unused helper `_port_tag` (tierc11_data.py:182, defined once, never called; it formats a TC10 port tag from TC10_SRC_SHA256) is neither ported nor in PORTS.

**DEFAULT TAKEN.** Each label is the strongest one the AST supports: 10 TEXT-ONLY (the reading's four plus write_pre_state, _assert_bound, clone_findings, contract_multiplier_table, cache_manifest_staleness, summarize); seal_provenance VERBATIM with the constant SEALED_FILES labelled CHANGED. `_port_tag` not ported (dead code naming TC10's source sha). No logic differs from what the reading orders; F-D-PORT GREEN.

**Status.** Ruled at the TC12-D gate: AM-51.

---

## AP-51 · 2026-10-09 (~23:36Z) · L-D.22, L-D.11, L-0.17 · TC12-D (fix pass)

**Title.** CONTRACT_SPECS.json keeps the referee's `law` sentence whole — it names TIER-C11 and does not itself say 'point-in-time' (verifier D-4)

**Readings.** L-D.22, L-D.11 (capture_contract_specs TEXT-ONLY), L-0.17 / AM-38 (the statement rule of F-TYPED)

**The texts.** L-D.22: "It is a point-in-time venue spec taken at the fetch run, hours after the pin; the record says so." L-D.11: "TEXT-ONLY: ... `capture_contract_specs`". The quotation law: "A literal inside a function proven AST-identical to its filed source (F-D-PORT) ... is a QUOTATION of that source".

**The fact.** The sealed, write-once data/CONTRACT_SPECS.json `law` reads "...in TIER-C11 the capture is also the proof that every symbol of record is TRADING" (D11's filed sentence). Under AM-38's statement rule a string-changed statement in that function would have the referee's numeric literal read as a typed number (F-TYPED RED), so the statement was kept whole. The record does carry captured_wall_clock_utc 2026-10-09T22:18:03Z (26.3 h after the pin) and its as-of stamps; the point-in-time sentence is in data/TICK_GRID_AUDIT.json `law` and the manifest's tick_of_record block. The file is sealed (WRITE_ONCE_SEAL.json) and cannot be edited without a new fetch.

**DEFAULT TAKEN.** Bytes left as sealed; the sentence is accepted as a TEXT-ONLY quotation of the referee; the fact is returned as a build disclosure for the B-1 entry.

**Status.** Ruled at the TC12-D gate: AM-52.

---

## AP-52 · 2026-10-09 (~23:36Z) · L-D.15, L-D.20 · TC12-D (fix pass)

**Title.** F-D-DET's AST clock leg: which calls count as a clock

**Readings.** L-D.15 (F-D-DET), L-D.20

**The texts.** L-D.15: "OR the call graph of `write_manifest` holds a `time.` / `datetime.` call (AST)". L-D.20: "`--manifest` makes no clock call."

**The fact.** The call graph of write_manifest lawfully holds pure conversions of filed integers and strings (datetime.fromtimestamp of a filed ms stamp, strptime of a filed ISO string) — read literally, the leg would be RED on the real tree by construction.

**DEFAULT TAKEN.** The leg counts time.* and datetime.now / utcnow / today as clock calls; fromtimestamp / strptime conversions of filed values are not clocks. The planted mutation (a fee_schedule() copy stamping datetime.now()'s date) is RED by the AST leg.

**Status.** Ruled at the TC12-D gate: AM-53.

---

## AP-53 · 2026-10-09 (~23:36Z) · L-D.11, L-D.20, L-0.20 · TC12-D (fix pass)

**Title.** The determinism set carries sealed wall-clock STRINGS and the absolute snapshot_root (verifier D-6)

**Readings.** L-D.11 (key-for-key schema; the determinism set), L-D.20, L-0.20

**The texts.** L-D.11: "reproduces TC11's manifest schema KEY FOR KEY (41 top-level keys ...)"; "with no network and no clock call". L-D.20: "The retrieval INSTANT ... lives ONLY in the provenance set"; "The same law covers `CONTRACT_SPECS.json`'s capture stamp ...: the manifest pins that file's BYTES by sha and never carries its clock."

**The fact.** STAGE_D_MANIFEST.json `write_once.disclosure` (TC11's key; seal_provenance / the seal reader are VERBATIM ports and TC11's manifest did the same) holds seven 'last written <stamp>' sentences plus the last fetch-row stamp, copied from the sealed WRITE_ONCE_SEAL.json — among them CONTRACT_SPECS.json's 2026-10-09T22:18:03Z. `snapshot_root` and the .md header hold /Users/luis/.cache/naiad/snapshots/tc12_20261008. No clock call is made (F-D-DET's AST leg and two-seed twins GREEN; rebuilds reproduce the filed bytes on any day), but under another HOME the bytes differ (verifier: byte 475193 of the .json, byte 161 of the .md).

**DEFAULT TAKEN.** L-D.11's key-for-key port kept (TC11's form); the strings are sealed data, not a clock. Any review run must use the same HOME path. If the orchestrator rules L-D.20's 'never carries its clock' to bind this key, the change is a mechanics amendment to --manifest (drop or sha-point the disclosure sentences), moving the manifest sha and the mirror's self-describing copy.

**Status.** Ruled at the TC12-D gate: AM-54.

---

## AP-54 · 2026-10-09 (~23:36Z) · L-0.9, L-0.4, L-D.11 · TC12-D (fix pass)

**Title.** No outside-repo path in artifact_shas: the snapshot is pinned through the tracked manifest

**Readings.** L-0.9 (the record's keys), L-0.4 (tierc12_progress.certified), L-D.11

**The texts.** The unit text: "artifact_shas {repo-relative path (or absolute path for a file outside the repo): {bytes, sha256}}". L-0.4: certified() is "THE ONE HELPER OF EVERY SHA-FIRST READER".

**The fact.** tierc12_progress.certified() resolves a path relative to the repo root; measured: certified('/Users/luis/.cache/naiad/snapshots/tc12_20261008/MANIFEST.json') raises ValueError ('is not in the subpath of /Users/luis/Naiad'). The snapshot is 176 files, 859258689 bytes.

**DEFAULT TAKEN.** No outside-repo path is in TC12-D.json artifact_shas. Every snapshot file's sha256, bytes and content_sha is pinned in the tracked data/STAGE_D_MANIFEST.json (files[] 124 + out_of_scope_snapshot_files[] 52), which the record pins by sha dcddc5f7…e8b8; the fix pass re-hashed all 176 local files and all 176 mirrored files equal to it.

**Status.** Ruled at the TC12-D gate: AM-55.

---

## AP-55 · 2026-10-09 (~23:36Z) · L-0.20, L-0.21, L-D.11, L-D.15 · TC12-D (fix pass)

**Title.** No F-DET / F-KEY helper instance, no build_manifest.json and no STAGE_D.md at this record

**Readings.** L-0.20 (F-DET), L-0.21 (F-KEY), L-D.11, L-D.15

**The texts.** L-0.20: "For every directory a record writes parquet into ...". L-0.21: "per parquet directory". L-D.11: "`data/STAGE_D_MANIFEST.json` (+ `.md`)" and the determinism set of four files; L-D.15 names F-D-DET as the determinism leg of data/FIXTURES_DATA.txt.

**The fact.** Stage D writes no parquet directory under research_outputs/tierc12 (its parquet is the snapshot, outside the repo, pinned by the manifest). The readings name STAGE_D_MANIFEST.json / .md as the directory's tracked manifest and document; no reading of L-D names a build_manifest.json or a STAGE_D.md.

**DEFAULT TAKEN.** F-D-DET (two hash-seed subprocess builds of the four determinism-set files, the filed bytes, the AST clock leg, parquet content shas) is this record's determinism leg; no F-KEY instance; no build_manifest.json and no STAGE_D.md filed.

**Status.** Ruled at the TC12-D gate: AM-56.

---

## AP-56 · 2026-10-09 (~23:36Z) · L-D.6, L-D.5 · TC12-D (fix pass)

**Title.** A resumed --fetch re-asks the thirteen 8h funding tapes

**Readings.** L-D.6 (funding), L-D.5 (F-D-FETCHPATH)

**The texts.** L-D.6: "A tape whose edge already floors to the pin's hour is skipped ("nothing can be due"). ... This is D11's `extend_funding` with its logic unchanged (D11:1359-1383; TEXT-ONLY)." L-D.5 F-D-FETCHPATH: "a `--fetch` resume over the filed snapshot asks or saves anything".

**The fact.** The thirteen 8h tapes end at the 2026-10-08T16:00Z print, one print before the pin's hour (20:00Z is a funding hour of the four 4h tapes only), so D11's skip test is false for them and a resume asks the venue again; the venue returns nothing new and no content moves.

**DEFAULT TAKEN.** D11's logic kept unchanged (TEXT-ONLY). F-D-FETCHPATH holds the resume on CONTENT (nothing saved, no kline asked). --fetch was run exactly once on the real snapshot.

**Status.** Ruled at the TC12-D gate: AM-57.

---

## AP-57 · 2026-10-09 (~23:36Z) · L-D.6, L-D.14, L-D.15, L-D.11 · TC12-D (fix pass)

**Title.** Funding contiguity INSIDE the extension is held by no leg (verifier D-5; a coverage observation, not a breach)

**Readings.** L-D.6 (row accounting), L-D.14 (F-D-3), L-D.15 (F-D-EDGE), L-D.11 (`complete`)

**The texts.** L-D.6: "Row accounting, asserted per native kline file". L-D.14: "`last_ms + FUNDING_JITTER_MS ≥ PIN − ivl × MS_1H`". L-D.15 F-D-EDGE: "a funding tape stops short of the pin's hour, repeats a print or holds a print past pin + jitter".

**The fact.** The readings check a funding tape's edge, duplicates and the funding-hour law, not that the prints TC12 added form an unbroken cadence. The verifier's mutant (funding/ZECUSDT.parquet, print 1790928000000 removed, a 16 h hole) is caught only because the file no longer matches the filed manifest; a manifest rebuilt over the holed tape reads complete and F-D-3 stays GREEN. Re-measured in the fix pass on the filed tapes: one constant floor-hour spacing on each of the 17 (thirteen 8h x 41 prints, four 4h x 83 = 865) and prints added == (last due hour <= the pin − TC11's pin) / cadence on every tape — no hole.

**DEFAULT TAKEN.** Built as the readings state; no leg added. If the orchestrator wants it held: a detector in F-D-EDGE (and a clause of `complete`) — per tape, prints added == (last due floor hour <= pin − TC11 pin) / observed cadence, with one constant spacing — and a plant (one print removed mid-extension, the manifest rebuilt on the copy).

**Status.** Ruled at the TC12-D gate: AM-58.

---

## AP-58 · 2026-10-09 (~23:36Z) · L-D.23 · TC12-D (fix pass)

**Title.** TickGrid.lt / le / gt / ge do not type-check the level n (verifier D-7)

**Readings.** L-D.23, O-20

**The texts.** L-D.23: "The four comparisons against a grid level `n × T`, each an INTEGER comparison, exact for off-grid `x` too"; "No float subtraction, no float comparison, no tolerance."

**The fact.** px(n) HALTs on a non-int n; the four comparisons do not: `TickGrid('0.10').lt(0.3, 3.5)` returns False with no HALT (an int-against-float comparison), `TickGrid('0.10').px(1.5)` -> 'HALT: TickGrid: px(n) takes an int level, got float'. No live path: consumers take n from floor_ticks / ceil_ticks (ints) and F-TICK [a] enumerates int levels.

**DEFAULT TAKEN.** Left as filed, as the verifier advises (the change moves scripts/tierc12_tick.py's sha and F-TICK [a]'s source-copy plants). Proposed for a later ruled change: `if type(n) is not int: halt(...)` at the head of the four comparisons plus one F-TICK [a] case (a float level must HALT); until then a consumer must pass an int level.

**Status.** Ruled at the TC12-D gate: AM-59.

---

## AP-59 · 2026-10-09 (~23:36Z) · L-D.19, L-D.1, L-D.18 · TC12-D (fix pass)

**Title.** Additive keys beyond the readings' tables in fee_schedule.json, AS_OF_PIN.json and FEE_SOURCE.json (verifier D-9, second half)

**Readings.** L-D.19 (the schema), L-D.1 (the pin record's keys), L-D.18 (FEE_SOURCE.json's keys)

**The texts.** L-D.19's venue-block table and `maker_pin` row; L-D.1: "plus: `tc11_pin_close_ms`, `tc11_pin`, `bars_4h_past_tc11_pin`, `step_q` {`commit`, `instant`, `record_path`, `record_sha256`, `contract_path`, `contract_sha256`}, `pin_derivation`, `bybit_server_time_ms`, `bybit_kline_of_pinned_bar`, `bybit_pin_bar_closed`"; L-D.18: "per venue: `url`, `final_url`, `http_status`, `error`, `body_path`, `body_sha256`, `body_bytes`, `retrieved_wall_clock_utc`, `retrieved_utc_date`".

**The fact.** fee_schedule.json: each venues[<VENUE>] block carries maker_retrieval_http_status and maker_unretrievable_reason; maker_pin carries x_assumed_source {path, sha256, certified_by}. AS_OF_PIN.json carries step_q.instant_iso and bybit_closure_law, bybit_kline_endpoint, bybit_server_time, o7_printed. FEE_SOURCE.json carries per venue http_requests_logged, redirects, venue_domain. Every key the readings name is present with the value they define; nothing is renamed or removed.

**DEFAULT TAKEN.** Kept: all additive provenance. AS_OF_PIN.json and FEE_SOURCE.json are write-once and sealed and cannot be rewritten without a new fetch; fee_schedule.json is in the determinism set and reproduces byte for byte.

**Status.** Ruled at the TC12-D gate: AM-60.

---

## AP-60 · 2026-10-09 (~23:36Z) · L-D.24 · TC12-D (fix pass)

**Title.** F-MIRROR's BREAK half plants on a temp copy of the mirror's funding tree, not of the whole mirror

**Readings.** L-D.24

**The texts.** L-D.24: "Mutation: one byte flipped in a TEMP copy of the mirror tree → RED at "sha != manifest"; one file removed from the temp copy → RED at "file set"."

**The fact.** The mirror tree is 859 MB; the BREAK half copies the destination's funding/ subtree (21 files) to $TMPDIR and runs the same comparator (mirror_tree_findings) on it against the manifest's rows for those paths; the REAL half re-reads all 176 destination files.

**DEFAULT TAKEN.** The plants (one flipped byte, one removed file, one altered sha in a copy of the attestation) run on the 21-file temp copy with an unbent control; the comparator is the one the REAL half uses.

**Status.** Ruled at the TC12-D gate: AM-61.

---

## AP-61 · 2026-10-09 (~23:36Z) · L-D.18 · TC12-D (build)

**Title.** A fee page answered with a status other than 200 / 404 leaves no body to save

**Readings.** L-D.18 (Act 1 — CAPTURE)

**The texts.** L-D.18: 'one request per venue through ED._get (its transport retries included...)' and 'The response body is saved byte for byte'.

**The fact.** engine.data._get returns a response only on 200 or 404; on 202 / 403 it retries 4 times and raises RuntimeError, discarding every response. Both pages answered that way.

**DEFAULT TAKEN.** Through ED._get as the reading orders; FEE_SOURCE.json files http_status (the last attempt's, read from the logged http rows), the error text, http_requests_logged = 4, null body_path / body_sha256 / body_bytes. No fee_source body file exists and ~/.cache/naiad/provenance/ was not created.

**Status.** Ruled at the TC12-D gate: AM-62.

---

## AP-62 · 2026-10-09 (~23:36Z) · L-D.5 · TC12-D (build)

**Title.** --all returns 2 before the derivation and the seal when the fetch is incomplete

**Readings.** L-D.5 ('--all = steps 2 -> clock row -> 3a-3f -> 4 -> 5 -> 6 (D11's run_all)')

**The texts.** L-D.5: 'the 3f record is not filed while a venue it must ask cannot be reached'; L-D.11: FLAT_BAR_ATTEST.json is one of the seven SEALED_FILES.

**The fact.** D11's run_all derived, sealed and described even when the fetch was incomplete. With FLAT_BAR_ATTEST.json among the sealed files and filed only after a complete extension, sealing an incomplete fetch would crash on the absent record or seal a partial log.

**DEFAULT TAKEN.** run_all (CHANGED, named in PORTS) returns exit 2 right after an incomplete fetch; nothing is derived, sealed or described until a re-run completes. The build of record ran the subcommands one by one in L-D.5's order (--clone, --pin, --fetch, --derive, --seal, --manifest, fixtures, --mirror, mirror fixture), each once and complete.

**Status.** Ruled at the TC12-D gate: AM-63.

---

## AP-63 · 2026-10-09 (~23:36Z) · L-D.24, L-D.11 · TC12-D (build)

**Title.** MIRROR_ATTEST.json cannot name the volume's filesystem without a second out-of-process site

**Readings.** L-D.24 (step 6: 'destination, volume filesystem, drive_wait state...'), L-D.11 ('exactly ONE out-of-process call')

**The texts.** L-D.11: 'tierc12_data.py holds exactly ONE out-of-process call, a literal argv: cp -cpR'.

**The fact.** Python's os.statvfs does not expose the filesystem type name on macOS; reading it needs `mount` (a subprocess) or a typed ctypes struct.

**DEFAULT TAKEN.** MIRROR_ATTEST.json files `volume_observed`: os.statvfs fields, case_insensitive = True (measured on the destination) and a sentence that the name is not read by the module. The mirror child record's notes carry what `mount` printed in the builder's shell: /dev/disk6s2 on /Volumes/LaCie (exfat).

**Status.** Ruled at the TC12-D gate: AM-64.

---

## AP-64 · 2026-10-09 (~23:36Z) · L-D.23, L-S.11, L-S.15, L-R.24 · TC12-D (build)

**Title.** TickGrid: an inexact quotient under grid.ctx raises MemoryError, not decimal.Inexact

**Readings.** L-D.23 (the trapping context; 'a quotient that is not exact raises at this precision and is a HALT'); consumers L-S.11, L-S.15, L-R.24

**The texts.** L-D.23: 'A decimal signal surfaces as a HALT (SystemExit), never as a rounded value.'

**The fact.** Measured: with prec = decimal.MAX_PREC and Inexact trapped, CPython answers Decimal(1) / Decimal(3) under ctx with MemoryError. It still raises and never rounds, but it is not a decimal.DecimalException.

**DEFAULT TAKEN.** TickGrid's own operations (+, -, x, divmod) catch (decimal.DecimalException, MemoryError) and HALT. A consumer forming its own expression under decimal.localcontext(grid.ctx) must treat MemoryError as the same HALT — stated in the module docstring. lt / gt are written with the level formed in a statement of its own (below = n - 1; above = n + 1), so no BinOp stands under a comparison (AM-34).

**Status.** Ruled at the TC12-D gate: AM-65.

---

## AP-65 · 2026-10-09 (~23:36Z) · L-D.3, L-D.15, L-D.1 · TC12-D (build)

**Title.** F-D-GUARD's equality-removed mutant, and step_q.instant

**Readings.** L-D.3 (FAILS-IF), L-D.15 (F-D-GUARD), L-D.1 (the pin record's keys)

**The texts.** L-D.3: 'a copy of the guard with its final equality test removed ACCEPTS the planted TC11 path'. L-D.1: step_q {commit, instant, ...}; 'this reading's ct_ms, filed as step_q.instant'.

**The fact.** The same reading puts the TC11 snapshot on the guard's refusal list, so removing only the final equality test still refuses the TC11 path (it then accepts a foreign directory holding klines/).

**DEFAULT TAKEN.** Two mutants, both caught: equality removed (GUARD-ACCEPTS a foreign directory), and equality plus the TC11 refusal row removed (GUARD-ACCEPTS the TC11 snapshot). AS_OF_PIN.json step_q.instant = ct_ms 1791499933000 with step_q.instant_iso '2026-10-08T22:52:13Z' beside it; extra provenance keys o7_printed, bybit_server_time, bybit_kline_endpoint, bybit_closure_law were added.

**Status.** Ruled at the TC12-D gate: AM-66.

---

## AP-66 · 2026-10-09 (~23:36Z) · L-X.21, L-X.20, L-0.4 · the orchestrator at TC12-D

**Title.** F-ATTEST-ORDER [REG] holds a listed REG_SET script to its listed sha for good, so a lawful repair of one after the registry commit turns the leg RED

**Readings.** L-X.21, L-X.20, L-0.4

**The texts.** L-X.21 clause 3: ATTEST_REG.json is 'the listing … of every file then on disk …, taken after --file'. As built (AP-45 / AM-46) the leg holds every listed path outside LATER_T and the two append-only texts to its listed sha against the WORKING file.

**The fact.** The registry builder reported it at TC12-REG as a known hazard; at TC12-D it is met: the closure suite (a listed REG_SET script) must be repaired under AM-49, and the leg itself lives in another listed script.

**DEFAULT TAKEN.** (no builder default: an orchestrator ruling)

**Status.** Ruled at the TC12-D gate: AM-67.

---

## AP-67 · 2026-10-10 (~00:05Z) · L-0.23, L-0.14, L-0.9 · the orchestrator at the TC12-D gate

**Title.** A transcript of record that prints the number of amendments on file drifts with every amendment

**Readings.** L-0.23, L-0.14, L-0.9

**The texts.** L-0.14: a transcript of record is byte-identical run to run; L-0.9: a record's fixtures re-pass now. The pins suite's F-VETO PASS line prints '<n> amendment(s) on file, 0 changing a pin', n counted on the working LEANS_AMENDMENTS.md.

**The fact.** Met at the TC12-D gate: after AM-49..AM-67 were appended, `tierc12_pins_fixtures.py` run plain reads 3 GREEN but its transcript differs from the record in that one token (48 → 67), and exits 1 on drift. It would drift again with every amendment, and an earlier record's fixture row cannot be re-filed.

**DEFAULT TAKEN.** (no builder default: an orchestrator ruling)

**Status.** Ruled at the TC12-D gate: AM-68.

---

## AP-68 · 2026-10-10 (~00:05Z) · L-0.4, L-0.9, L-0.11 · the orchestrator at the TC12-D gate

**Title.** The resume suite re-run at an EARLIER gate holds a path to that gate's entry against the working file, so a lawful later re-record turns the earlier gate red

**Readings.** L-0.4, L-0.9, L-0.11

**The texts.** L-0.4 (1): a path recorded by more than one record is governed by its LAST record; an earlier record's entry is held to the blob at the commit that closed it. As built, the suite's walk takes 'last' among the records IN SCOPE of `--stage` (those before the gate and its own).

**The fact.** Met at the TC12-D gate: four REG_SET suites are repaired under AM-49, AM-67, AM-68 and this amendment and re-recorded by TC12-D's record. Re-run at `--stage=TC12-REG` (or `.ledger-spec`), the suite sees TC12-REG as the last record naming them, compares the working files and reports ARTIFACT-MOVED — so the sweep of earlier records' fixture rows (L-0.11) could never be GREEN again.

**DEFAULT TAKEN.** (no builder default: an orchestrator ruling)

**Status.** Ruled at the TC12-D gate: AM-69.

---

## AP-69 · 2026-10-10 (~00:29Z) · L-0.4, L-0.9 · the repair unit at the TC12-D gate

**Title.** AM-69's premise is not what the code does: the resume suite already takes the last record over every record on file

**Readings.** L-0.4 (1), L-0.9

**The texts.** AP-68 and AM-69 say the suite's walk takes 'the last record that names a path' among the records in scope of `--stage`, and order `scripts/tierc12_resume_fixtures.py` repaired.

**The fact.** The suite's `last_naming` iterates every record on disk in walk order, whatever `--stage` is; `Estate.scope` limits only which records' entries are walked. The ARTIFACT-MOVED findings AP-68 reported came from TC12-D's record not yet naming the three suites that WERE repaired (closure, registrations, pins). With those re-recorded and the merger run, all six fixture rows of the committed records pass plain with their transcripts unchanged. The suite is byte-identical to its blob at the registry commit (sha256 240b1a94…214f).

**DEFAULT TAKEN.** No edit was made to the resume suite and none was invented to give AM-69 a diff.

**Status.** Ruled at the TC12-D gate: AM-70.
