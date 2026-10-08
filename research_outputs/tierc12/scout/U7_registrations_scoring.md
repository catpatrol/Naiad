# U7 · REGISTRATIONS AND SCORING — scout map for TIER-C12 (five rows, three families)

Read-only scout, 2026-10-08. Nothing was written in either tree; no repo module was imported; no build or
fixture suite was run. Every value below was read from the file cited. Abbreviations:
`M` = `/Users/luis/Naiad` (branch v12-v1-census) · `X` = `/Users/luis/Naiad/.claude/worktrees/tierc11x`
(branch tierc11x, tip `7b24f835bcbf7430eb0f97b6c39b6b1b233eef11`, `git status`: only the pre-existing untracked
`research_outputs/tierc11x/close/CERTIFIED_TIP`).

TC12 contract read verbatim: scratchpad copy sha256 `861d6050e80e66995e4f9db2855aaf274d63285249c2549e5a0813582095a7bd`
(137 lines by `wc -l`, 12,209 B, ends with a newline). **It is already filed and committed**:
`M/exchange/queue/2026-10-08_TC12_APOLLO.md` has the same sha, commit `28e006b` "tierc12(STEP Q): contract filed
verbatim". Main HEAD moved from `a399b47` to `28e006b` while this scout ran.

---------------------------------------------------------------------------------------------------------------
## 1 · FACTS

### 1.0 State of the three earlier tiers (it bounds what TC12 may touch)
- TC11 commits, in order (`git -C M log --grep=tierc11`): STEP Q `b9ed953` (2026-09-24 21:09) → TC11-REG `4ed4e67`
  (22:03:26) → TC11-D `e97ad73` → FOUNDATION `ba66d95` (first books, 2026-09-25 01:48) → … → SCORE `04067a0` →
  FIX `d307829` → CLOSE `6f34939`.
- X commits: STEP Q `6948316` → X-LEANS `c2da417` → X-D `df0b5c4` → X-REG `4a47a63` (05:10:29) → X-FOUND `7de8a42`
  (first books, 06:08:04) → … → X-SCORE `8ccbe18` → X-CLOSE `7b24f83`.
- **No close act has run for TC10, TC11 or X.** `M/exchange/reports/` holds no `BUILD_*TIERC10*`, `*TIERC11*`;
  `M/exchange/status/LEDGER_APOLLO.md` (2,426 lines, mtime Aug 22) has no TIER-C10/11 block. TC11's
  `M/research_outputs/tierc11/close/close_acts.sh:47-52` (step 0) STOPS until TC10's report is tracked and its
  block committed ("run $TC10_ACTS first", :50).
- Main tree is dirty in two tracked files: `exchange/status/daily/DAILY_2026-10-08.md` and
  `research_outputs/tierc10/close/FIXTURES_CLOSE_ledger_append_root.txt` (both ` M`).
- No `scripts/tierc12_*` and no `research_outputs/tierc12/` exist. `M/.gitignore` has **no rule for tierc12**
  (`git check-ignore` prints nothing for `research_outputs/tierc12/regbooks/P-ADM-1/scored.parquet`); TC11's rule
  is the last two lines of `.gitignore` (`research_outputs/tierc11/**/*.parquet`, `…/_det_*/`), X's is the nested
  `X/research_outputs/tierc11x/.gitignore` (`*.parquet`, `_det_*/`).

### 1.1 TC11's filing — `M/scripts/tierc11_registrations.py` (252 lines, sha256 `55cc090e…2800`)
- Constants typed in the script: `CONTRACT_SHA` `bb38e016…f835` (:24), `FAMILY_M = 9` (:27), `FAMILY_Q = 0.10`
  (:28), `BAR = FAMILY_Q / FAMILY_M` (:29), `SEED = 20260924` (:30), one `VERDICT_RULE` string shared by all nine
  (:32-39), `REGS` = a typed list of `(reg_id, prior_pct, (lo, hi), [context ranges], operative_spec dict)` (:47-177).
- Slice law (:194-195): `"\n".join(lines[lo-1:hi])` of `raw.decode("utf-8").split("\n")`. Guards: the slice must
  `lstrip().startswith(rid)` (:200) and contain `f"[{prior}%"` (:202).
- Hash law (:204-221): body = {registration, seq, prior_pct, family_m, family_bar, seed, text_of_record, text_lines,
  context_of_record, operative_spec, verdict_rule}; `payload = json.dumps(body, sort_keys=True,
  ensure_ascii=False)`; `sha256` = sha of that payload (computed BEFORE `text_sha256`/`sha256` are added);
  `text_sha256 = sha256(text)`. Chain line = `{seq, registration, sha256, prev}`, `line_sha256 =
  sha256(json.dumps(line, sort_keys=True))`, genesis `"0"*64`, `head` = the last `line_sha256`.
- Write-once (:241-247): `--file` HALTs if `REGISTRATIONS.json` exists. **The script writes REGISTRATIONS.json
  only**; nothing in `M/scripts/tierc11_*.py` writes `REGISTRY_PIN.json` (grep) — the 308-byte pin was filed by
  hand in the same commit `4ed4e67`.
- Records: `M/research_outputs/tierc11/registrations/REGISTRATIONS.json` sha256
  `648834bf30e20e92713bddef2374ddef1aae843f4d8ba152fc50166c8cc6f1ee` (34,228 B). Top keys: `tier, contract{path,
  sha256}, leans{path, sha256}, family_m 9, family_q 0.1, family_bar 0.011111, seed 20260924, registrations[9],
  chain[9], head, law`. `head` = `6772568b31fcfb2d56eb8c80b66dedee4fb5082673369e872972df8f475ec8f9` (:583).
  `REGISTRY_PIN.json` sha256 `ea77921a…748f` = `{head, contract_sha256, leans_sha256, n 9, family_m 9, family_bar
  0.011111}`.
- **No timestamp of any kind** is carried in either file.
- Layout exemplar (P-AGE-1, `REGISTRATIONS.json:66` onward): `registration "P-AGE-1"`, `seq 2`, `prior_pct 50`,
  `family_m 9`, `family_bar 0.011111`, `seed 20260924`, `text_of_record` (contract lines 45-46), `text_lines
  [45,46]`, `context_of_record [{lines [44,44], text "STAGE G · ADMISSION GATES (registrations; each removes
  trades → two-sample)"}]`, `operative_spec {kind "admission gate (post-filter)", panel "CLASSIC5", era "full
  corridor", ruler "two-sample", base "card-v6", scored_arm "v6 book minus the campaigns whose ENTRY-bar tide
  streak … >= the trailing 75th-percentile edge (B4 OLD; tierc9._trailing_edges …) [L-G.1]", tier_e_arms [6],
  pre_seen "<free text>", leans [..]}`, `verdict_rule`, `text_sha256 eeb05871…`, `sha256 e01a89ea…`.
  P-SCALP-2 adds `operative_spec.precondition` ("R2 lens verdict of record at 1h … == PASS; otherwise CLOSED BY R2,
  not scored, no slot spent [L-S.1]") and `era "holdout"`, `ruler "vs zero"`, `base null`.
- Spec vocabulary the TC11 scorer accepts (`M/scripts/tierc11_score.py`): rulers `"paired (set kept; HALT unless
  key sets identical)" | "two-sample" | "vs zero"` (:240-241); eras `"full corridor" | "holdout"` (:242); panels
  `CLASSIC5 | PANEL17` (:541); a gate is `kind.startswith("admission gate")` (:549); label keys `("pre_seen",
  "selection_hazard")` (:246); status words `BUILT | CLOSED_BY_PRECONDITION | CONDITION_NOT_MET` (:245).

### 1.2 X's filing — `X/scripts/tc11x_registrations.py` (1,054 lines, sha256 `6bf4bf4e…9fc6`)
- The design document is `X/research_outputs/tierc11x/REGISTRATION_PLAN.md` (410 lines, sha256
  `a887ea64a5099b8b27b5433d263969911ea7795c0fade2af9b40a5b92b8c3d15`): §0 the slice law and a VERIFIED line map
  with a text sha per object (:18-48), §1 a table `seq | registration | family | m | bar | prior | text lines |
  ruler | precondition | honesty label` (:53-57) and one §1.k block per registration (text, context, bullet-list
  operative_spec, one `verdict_rule:` line), §2 what the filing must hold (:304-331), §3 the stage plan.
- The script types no text and no spec: it slices texts from the contract by the plan's lines and checks each
  slice's sha against the plan's map (`build`, :523-670); it carries each operative_spec from the plan's block
  verbatim (`carry_spec` :329; `SPEC_CARRY_LAW` :111-116); families and q are PARSED from the contract
  (`families_from_contract` :488-493: regexes `FAMILY ([A-Z][A-Z-]*) \(m=(\d+)\)` and `bar (\d+\.\d+) ÷ m per
  family`, taken from the two lines starting at the single line beginning `FAMILIES (`, `_families_text` :808-812).
- Hash law identical to TC11's (`payload_sha` :496-499, `chain_of` :502-509); the doc's `law` string is read by
  object from TC11's filing (:668).
- Write-once by exclusive create: `file_filing` (:714-727) HALTs if either file exists, then `open(p, "xb")` for
  `REGISTRATIONS_X.json` and `REGISTRY_PIN_X.json` (the pin is GENERATED: `pin_of` :682-711).
- Records (`X/research_outputs/tierc11x/registrations/`): `REGISTRATIONS_X.json` sha256 `6b0eb52d…b0a4` (26,862 B);
  top keys `tier, contract, leans, review, plan, families, verdict_law, seed, registrations, chain, head, law`;
  `families = [{family EXIT, m 2, q 0.1, bar 0.05}, {family SFP-RANGE, m 1, q 0.1, bar 0.1, bar_binding false}]`;
  `verdict_law = {clause_a "cluster-90% CI lo (5th percentile) > 0 (the lineage law)", clause_b "p_one_sided <=
  bar", reading "LX-1.2", rival "p <= bar alone, printed as a column"}`; `seed 20260925`; `head`
  `2aafebc8f2bf5e393a8ca07435dddf8e6e23c58347c2a90f937c29520f9e1810`. `REGISTRY_PIN_X.json` sha256 `6a445afe…2e73`
  carries the filing's own `{path, bytes, sha256}`, `order_of_filing`, `chain` (3 line shas), per-registration
  `{seq, sha256, text_sha256, text_lines, prior_pct, family, family_m, family_bar}`, `families`, contract / leans
  / plan / review shas, `seed 20260925, seed_sens 20260816, n_boot 4000`, `witness_law`.
- Per-registration keys in X: `registration, seq, family, family_m, family_bar, prior_pct, seed, text_of_record,
  text_lines, context_of_record[, external_context], operative_spec, verdict_rule, text_sha256, sha256`.
  `operative_spec` keys: `kind, panel, era, ruler, base, precondition, scored_arm, tier_e_arms, [pre_seen],
  [selection_hazard], [disclosures], leans`. `pre_seen` / `selection_hazard` are objects `{tag, label, text,
  items}` (tags on disk: `None`, `DIRECTION-INFORMED`, `KIN-SEEN`). `precondition` is `"none"` or `{text, items}`.
  `external_context` = `[{path, sha256, lines, text}]` (P-SFP-RNG-1 cites TC11's contract lines 16-18 at sha
  `bb38e016…`).
- Each `verdict_rule` is a per-registration sentence that states the bar arithmetic, seeds, m, and **exactly one**
  `prints '<verdict> — …'` template (REGISTRATION_PLAN.md:132, :175, :301); the scorer builds the §0 cell from it
  (`label_cell`, `X/scripts/tc11x_score.py:316-321`, HALT unless exactly one template).
- Verifier `verify_filing(doc, pin, contract_b, reg_bytes=None, ext_b=None, plan_b=None) -> list[str]` (:731-805):
  detectors CONTRACT-SHA, TEXT-SLICE, CONTEXT-SLICE, EXTERNAL-SLICE, PAYLOAD-SHA, SEED, FAMILY-BAR, CHAIN, HEAD-PIN,
  SPEC-VERBATIM.

### 1.3 "Text before result" — what actually enforces it on disk
There is **no timestamp check and no chain head pinned into any book manifest** in either tier. What exists:
1. Write-once filing — TC11 `tierc11_registrations.py:244-245`; X exclusive create `tc11x_registrations.py:714-727`.
   Fixture: X's F-REG-X sabotage "a second --file must HALT, in the filed directory (bytes unchanged) and in the
   scratch twin" (`X/scripts/tc11x_registrations_fixtures.py:36-37`).
2. Commit order (§1.0): the REG commit precedes the first book commit in both tiers. Stage law in words:
   REGISTRATION_PLAN.md:362 "X-D → X-REG, and **no book of any kind before X-REG**".
3. **The one fixture that tests the order: X's WORKTREE ATTESTATION (X-REG)** — `attest_findings`
   (`tc11x_registrations.py:916-958`): "ATTEST HEAD-LAW" fails unless HEAD at filing is the freeze commit
   `c2da417` or a descendant whose added files are all in the X-D file set (:929-940; sabotage "a HEAD adding a
   file past X-D", fixtures :58, plant :939). Git facts are gathered out of process by the fixture module.
4. The scorer refuses to score an unverified filing: TC11 `load_registry` → `verify_registrations`
   (`tierc11_score.py:391-492`, :495-505; typed `CONTRACT_SHA` :220, `LEANS_SHA` :222, `REGISTRATIONS_SHA` :224,
   `REGISTRY_HEAD` :226); X `verify()` (`tc11x_score.py:339-358`) additionally binds both filing files to the shas
   `progress/X-REG.json` files (:345-348), and `compute()` calls `verify()` first (asserted by AST in F-SCORE-X).
5. The book builders carry a `registered_as` label only (`X/scripts/tc11x_exit.py:1191`, `tc11x_sfp.py:1250`); no
   builder reads or stamps the registry head (grep of `REGISTRY_PIN|registry_head|6772568b|2aafebc8` over both
   script sets: only registrations / score / close / env / progress modules).

### 1.4 The statistics of record
- **Primitives** — `M/scripts/tierc5.py` (sha256 `ad912b38…5a6f`), reached as `E.T5`:
  - `cluster_boot(values, clusters, seed=SEED, n_boot=4000)` (:1178-1197): `uniq = np.unique(c)`; `rng =
    np.random.default_rng(seed)`; each draw `pick = rng.choice(uniq, size=len(uniq), replace=True)`, all rows of
    each picked cluster concatenated, the MEAN taken. Unit resampled = the ASSET cluster, whole; no time blocks.
  - `cluster_boot_diff(va, ca, vb, cb, seed=SEED, n_boot=4000)` (:1200-1224): `uniq = np.unique(concat(ca, cb))`;
    the SAME pick indexes both arms; draw = `mean(va[ta]) − mean(vb[tb])` (NaN when an arm's take is empty).
  - `_ci_from(draws, point)` (:1227-1235): finite draws only; `lo = np.percentile(d, 5)`, `hi = np.percentile(d,
    95)`; `p_one_sided = (np.sum(d <= 0) + 1) / (len(d) + 1)`.
  - **`tierc5.SEED = 20260816` (:86) is the DEFAULT seed of both functions** — the estate's sensitivity seed.
- **Seed use** — no derivation: the tier seed is passed as-is to every ruler call, and each call builds a fresh
  `default_rng(seed)`. TC11: `SEED = 20260924`, `SEED_SENS = 20260816`, `N_BOOT = 4000`
  (`tierc11_score.py:235-237`; `tierc11_env.py:125-127`). X: 20260925 / 20260816 / 4000 (`tc11x_env.py:144-146`).
  LOAO and every twin reuse the same seed. The TC11 shim asserts `T5.SEED == SEED_SENS == TP.SEED_LINEAGE and
  TP.N_BOOT == N_BOOT` (`tierc11_env.py:993`).
- **Rulers** (`tierc11_score.py:973-1006`, `ruled(ruler, a, b, col, seed, n_boot)`):
  - `vs_zero`: point `mean(net_r)`, draws `T5.cluster_boot(net_r, symbol)`.
  - `two_sample` (a refusal that removes trades): `va` = the KEPT book's net_r, `vb` = the WHOLE base book's net_r;
    point `mean(kept) − mean(base)`; draws `T5.cluster_boot_diff` (same asset draw in both arms); `n_clusters` over
    the union. So the statistic is kept-vs-all, not kept-vs-refused.
  - `paired`: per-campaign Δ keyed `(symbol, entry_ms)`; not needed by TC12.
  - Rows are sorted `(symbol, entry_close_ms)` mergesort before any ruler (`load_arm` :794-796).
- **p and the exact bar** (`ci_of` :955-970, SC-1 :71-73): `p_num = k+1`, `p_den = n_finite+1`; clause (b) is
  evaluated on a `Fraction` (`clears_bar` :1151-1157, `BAR_FRAC = Fraction(1,10)/FAMILY_M` :233); the deciding
  bound is the `floor((B+1)·bar)`-th smallest finite draw (the 44th of 4000 at 1/90). X evaluates clause (b) in
  floats (`verdict_of`, `tc11x_score.py:202-206`).
- **Verdict law.** TC11 L-1.4 (`M/research_outputs/tierc11/LEANS.md:115`): "verdict_of_record = SUPPORTED iff (a)
  CI lo > 0 AND (b) p ≤ 0.10/9 = 0.011111, else NOT SUPPORTED"; code `verdict_of_record(lo, hi, p)`
  (`tierc11_score.py:1160-1167`), "NOT SUPPORTED — CI wholly below zero" when `hi < 0`. X LX-1.2
  (`X/research_outputs/tierc11x/LEANS_X.md:657-685`): the same conjunction with the FAMILY bar, "a NAMED READING of
  'bar 0.10 ÷ m per family'"; "At m = 2 the clauses coincide to within one draw (lo > 0 ⟹ p ≤ 201/4001 = 0.0502)"
  (:668); "At m = 1, clause (a) decides … the bar 0.10 is on record but does not decide" (:669-670); the bar cell
  reads "0.10 (not binding at m = 1; decided at the 5th percentile, clause (a))" (:671; `SFP_BAR_CELL`
  `tc11x_score.py:141`). The rival "p ≤ bar alone" is printed as `literal_bar_p / literal_bar_pctile_10 /
  clears_literal_bar`, deciding nothing (`literal_bar` :209-218).
- **Printed beside, deciding nothing** — TC11 (`stats_block` :1185-1203): the sensitivity-seed ruling and verdict,
  the haircut twin at both seeds, LOAO at both seeds, D15 (paired only), the SC-22 concentration, tuning/holdout
  slices. X adds (`exit_row` :475-563, `sfp_row` :600-698): the exact enumeration `exact_cluster` (:221-255: every
  multinomial composition of |U| draws over |U| clusters, 126 atoms at 5; `p_exact`, `lo_exact`, `hi_exact` in
  integers), `seed_fragile` (:281-286), the 32-pattern `sign_flip_p` (:258-278), the calendar-month block twin
  (`month_of` :289, cluster = UTC month of the entry close, "TIME-CLUSTER FRAGILE"), the drop-OPEN twin ("VERDICT
  RESTS ON OPEN MARKS"), the size footnote (:139-140), and every draw set persisted with `draw_hex`
  (`draws_frame` :729-750).
- **LOAO** — `TP.loao_n(new, base, panel, two_sample=False, seed=SEED, label="", n_boot=N_BOOT)`
  (`M/scripts/tierc10_panel.py:1234-1339`, file sha256 `40b660cd…0b0e`): for each asset of the DECLARED panel, drop
  it and re-run the SAME ruler as the headline (vs zero / `cluster_boot_diff` / paired); a panel "excludes above"
  iff its CI lo > 0; `N = len(panel)`; an unbootstrappable panel counts against; the bar is `above_half_bar(N) =
  ceil((N+1)/2)` (`tierc11_score.py:1009-1010`) = **3 of 5**; BELOW panels are counted apart; the line reads
  "k/5 above[, j/5 BELOW]"; `loao_zero_campaign_assets` and the count without them ride beside. TC11's own
  re-implementation over frames: `loao(...)` (`tierc11_score.py:1013-1048`). "LOAO (bar 3/5; 9/17 for a 17-asset
  view) is printed beside and decides nothing" (LEANS.md:118; LEANS_X.md:719-720). On disk: P-AGE-1 "5/5 above"
  (`scores/SCORES.json` rows[1].stats.loao.line), P-WIN-1 "2/5 above", X P-OFF-1 "0/5 above, 1/5 BELOW".
- **Single-trade share** — two definitions on disk:
  - X LX-X1.9 (`LEANS_X.md:1019`): `max|Δ| / |ΣΔ|` with the arg-max key, can exceed 1, `None` iff `|ΣΔ| <= 1e-12`,
    `sum_delta_ex_argmax` beside (`harvest_rival`, `tc11x_score.py:459-472`). Defined on paired Δ.
  - TC11 SC-22 `concentration(ruler, a, b)` (`tierc11_score.py:1076-1118`) for two-sample and vs-zero rows: the top
    trade by `|net_r|` (ties → first in `(symbol, entry_ms)` order), its SIGNED share of the scored ΣR, the point
    with it removed from every book holding its key, the point without its asset and that asset's share, per-asset
    Δ / mean. On disk for P-AGE-1: top ZECUSDT entry close 1777622400000, +25.0605 R = 39.5% of ΣR 63.4641; point
    without it +0.1952 (`S0_VERDICTS.md:12`).
  - No threshold on either share exists anywhere.
- **Honesty wording.** TC11: one template for both labels — `cell += f" — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY
  ({label_of(spec, facts)})"` (`tierc11_score.py:1894-1900`), where `<hazard>` = `'<key>: <text up to its first
  top-level ;>'` (SC-8, `hazard_of` :571-578) and a `pre_seen` label also carries SC-21's facts "point known before
  filing; new campaigns since 2026-09-21T16:00Z: scored <n> / base <n>" counted by entry CLOSE > the TC10 pin
  `1_790_006_400_000` (:279, :587-600). P-AGE-1's filed cell: "SUPPORTED — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY
  (pre_seen: the scored cohort IS TC10 P_AGE_1_TIDE_YOUTH B4 (…); point known before filing; new campaigns since
  2026-09-21T16:00Z: scored 0 / base 0)" (`SCORES.json` rows[1].verdict_cell). X LX-1.3 (`LEANS_X.md:731-737`)
  DEPARTS: with `pre_seen` → "<verdict> — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (<hazards>)"; with
  `selection_hazard` only → "<verdict> — NOT CONFIRMATORY (selection_hazard: <tag>)" ("RE-SCORE is dropped because
  neither form was ever scored"). A CLOSED row carries no label ("the label qualifies a verdict; none is computed
  while CLOSED", `tc11x_score.py:631-632`).
- **Gates are post-filters** (LEANS.md:147-150): `gate_findings` (SC-16, `tierc11_score.py:914-942`) HALTs the row
  if the scored arm holds a key absent from the base or a kept row differs from the base on any of the 16 required
  columns; `gate_block` (SC-5, :1206-1220) prints refused n / mean / ΣR and, iff `mean(refused) > 0`, appends "on
  per-campaign expectancy only; the gate forfeits +X R total". A two-sample row on identical key sets is FLAGGED,
  not halted, and still spends its test (SC-6, :856-866).
- **Era** — one law: era = the entry bar's CLOSE; tuning ≤ `1_719_791_999_000` (2024-06-30T23:59:59Z), holdout
  after (`tierc11_env.py:128-129`, `era_of` :1047-1055; LEANS.md:95-101). "A registration naming no era is scored
  on the full corridor" (LEANS.md:99).

### 1.5 Family accounting
- TC11: one family, m = 9, bar 1/90 (`tierc11_score.py:230-234`). `family(rows)` (:2075-2092) writes
  `tests_spent = sum(spent_test)`. A CLOSED row: `verdict_of_record = status`, no stats, `spent_test False`, cell
  "CLOSED BY PRECONDITION (builder's stage status: …) — report-only · no number · no slot spent" (:1813-1827); a
  HALTed or ABSENT row spends no test (:2056-2071). On disk `M/research_outputs/tierc11/scores/FAMILY.json`:
  `family_m 9, bar 0.011111111111111112, bar_exact "1/90", tests_spent 8, supported ["P-AGE-1"]`; the unspent row
  is P-SCALP-2 (`status CLOSED_BY_PRECONDITION`, `p_one_sided null`, `spent_test false`). P-WARN-1's condition was
  MET, so it was BUILT and spent.
- X: per-family bars read from the filing (`fams = {f["family"]: f}` `tc11x_score.py:775`; row-level `family_m /
  family_bar` cross-checked :784-785); `spent[family] = count(test_spent)` (:798-800). On disk
  `SCORED_X.json.tests_spent = {"EXIT": 2, "SFP-RANGE": 0}`; `m_law`: "m is declared and never loosened; a
  registration closed by its precondition prints its reason, spends no test, and leaves m and the bar unchanged".
  P-SFP-RNG-1's row is number-free (`number_free true`, `verdict_of_record null`, `cell_text "CLOSED BY R2 (1h:
  FAIL)"`); the CLOSED book's CI appears only in a collared `tier_e` block. "Each registration is independently
  failable … no best-of" (LEANS_X.md:723-724).
- TC11 numbers that matter for TC12's bar (`SCORES.json` rows): P-AGE-1 n 141/200, Δ +0.246062, CI [+0.191190,
  +0.296656], p 1/4001; **P-WIN-1 n 137/200, Δ +0.175335, CI [+0.002964, +0.339256], p 146/4001 = 0.0365 — NOT
  SUPPORTED at 1/90**.

### 1.6 How scorer inputs are pinned, and `--refile`
- TC11: contract / LEANS / REGISTRATIONS / head typed in the scorer (§1.3 item 4); `LEANS_AMENDMENTS.md` hashed, not
  pinned (:284, :516-522). Books are NOT pinned by an external sha: each arm's sidecar `book_sha256` must equal
  the scorer's own canonical-CSV sha of the parquet (SC-13, `canonical_csv` :618-635; check :759-762), and
  `SCORE_MANIFEST.json` records `{book_sha256, sidecar_sha256}` per arm (57 inputs) plus `registry_head`, the R2 and
  scale-pick record shas, and the output shas (`render` :2577-2608). The v6 base is anchored: `v6_frame` (:1257-1267)
  HALTs unless `TB._content_sha(v6)` equals `books/build_manifest.json`'s; `base_ident` (SC-7) requires ONE
  `book_sha256` across all base arms and equality with `books/v6_campaigns.parquet` on 13 columns at 6 dp.
- X: filing files bound to `progress/X-REG.json`; each input bound to the sha its stage's progress record files
  (`load_inputs` :361-373); the precondition comes only from a landing record named by path + sha (:376-390);
  `build_manifest.json` carries `input_sha`, `code_sha256` of the scorer, `sha` of the draws table.
- `--refile` (TC11 only, `write_outputs` :2648-2665): identical bytes → left alone; different bytes without
  `--refile` → written beside as `<stem>_rerun<suffix>`, the record untouched, exit flag +16; with `--refile` →
  atomic replace (`.tmp` + `os.replace`). Exit code is a bit word: +2 registered HALT, +4 Tier-E halted, +8 ABSENT,
  +16 no-clobber (:301-302, :2611-2634). `--dry-run` validates everything and calls no ruler (:2450-2574).
  Fixture transcripts have their own `--refile-transcript`. **X's scorer has no refile law: `build()` overwrites
  with `write_text` (:995-999).** Registrations have no refile in either tier.

### 1.7 The score records, and the "added leaves" of MINOR-9 / §11 Q1-Q2
- `M/research_outputs/tierc11/scores/` (all tracked): `SCORES.json` sha256 `2c1a664a…f856` (236,946 B; top keys
  `as_of_last_closed_4h, banner, findings, n_boot, readings[24], regbooks_root, rows[9], seed, seed_sens`; 5,261
  leaves counted here; row keys include `verdict_of_record, verdict_cell, spent_test, clears_bar, stats{main, sens,
  haircut, haircut_sens, loao, loao_sens, d15}, gate, premise, concentration, pre_seen_new_campaigns, tier_e[],
  provenance, halts, notes`), `FAMILY.json` `3fa36bd4…2d73`, `BASE_IDENT.json` `29f795dc…5581`, `REGISTRY_CHECK.json`
  `aea83bf1…8ed0`, `S0_VERDICTS.md` `ea728250…70aa`, `SCORE_MANIFEST.json` `4cde52cd…65b2`, `STAGE_SCORE.md`
  `9d491e38…bbc`, `FIXTURES_SCORE.txt` `0d762abe…8225` (15 GREEN, 0 RED, :117).
- `BASE_IDENT.json`: `ok true`; ONE `book_sha256` `f41bfaf02b86dfb0b57dcffaf3c5f5e4bb05eda5c305b361322bc334369468a8`
  for all seven base arms; `v6 = {path research_outputs/tierc11/books/v6_campaigns.parquet, n 200, content_sha
  a5d0c57087c9b9bb95b61341e798b98eb41a8dc135d07c2eb279db8683ca96dd, sum_net_r_6dp 40.807566}`.
- **MINOR-9 / Q1**: `M/research_outputs/tierc11/BUILD_DRAFT.md:5943` — "SCORES.json between the reviewed commit
  04067a0 (the lens reviews) and HEAD d307829: 156 leaves added, 0 removed, 3 changed — each changed leaf a string
  label (.rows[1].verdict_cell, .rows[5].verdict_cell, .rows[8].status_reason); 0 numeric, bool or null leaf moved."
  Q1 (:5988): "keep them, or re-file the scorer's record?" **Q2** (:5989): "The contract's BUILT stamp: stamp it
  and re-pin REGISTRATIONS.json, REGISTRY_CHECK.json and PROGRESS.json, or leave the contract byte-frozen?" The
  reason is FN-M-QUEUE-STAMP (:5945): "stamping BUILT into the file would change those bytes and break every pin."
- X: `X/research_outputs/tierc11x/registrations/SCORED_X.json` `dd9b6e2d…04ae`, `SCORED_X.md` `6191bc8e…0481`,
  `SCORED_X_DRAWS.parquet` `2521ea25…48a8`, `build_manifest.json` `fdbb5ba2…4d9b`, `FIXTURES_REG_X.txt` (2 GREEN),
  `FIXTURES_SCORE_X.txt` (5 GREEN). There is no `scores/` directory in X.

### 1.8 The regbook interface (the table schema the TC11 scorer reads)
- Layout: `regbooks/<REG>/{STATUS.json, <arm>.parquet, <arm>.json}`; arms `scored | base | tierE__<slug>`
  (`ARM_RX` :257). `STATUS.json` = `{registration, status, reason, arms[]}` (`load_status` :803-830).
- 16 REQUIRED columns, exact dtypes (:248-255, :294-299): `symbol` str · `entry_ms` int64 · `entry_close_ms` int64
  · `direction` int8 · `entry_px, stop_px, r_dist` float64 · `exit_close_ms` int64 · `exit_reason` str · `net_r,
  gross_r, fee_r, funding_r, haircut_net_r` float64 · `era` str · `lane` str. Sort key `(symbol, entry_close_ms)`,
  pairing key `(symbol, entry_ms)`.
- Laws enforced (`validate_book` :646-770): no nulls; unique keys; direction ±1; `era == E.era_of(entry_close_ms)`;
  `0 < entry_close_ms − entry_ms <= one lens step` with the lens from the sidecar's optional `lens`, default `4h`
  (:692-703; `LENS_STEP_MS` has 5m…1d, **no 1w**); `exit_close_ms >= entry_close_ms`; `r_dist > 0`; symbols are
  fee-schedule stems; **AM-7 haircut law `haircut_net_r = net_r − fee_r × slip/taker` at 1e-12 — a HALT on scored
  and base arms, a note on Tier-E arms** (:713-721); no `, " CR LF` in strings; sidecar `registration, arm, kind,
  ruler, era_scope, panel[], n, sum_net_r (1e-6), book_sha256, description, source_script`, plus the collar on
  Tier-E sidecars.
- On disk `regbooks/P-AGE-1/scored.parquet` is (141, 47): the 16 plus extras (`arm_ms, arm_i, entry_i, …, lag,
  r_over_atr, tide_streak_entry, tide_edge_q75, tide_band, tide_streak_age_arm, …` and nine as-of stamp columns).
  `books/v6_campaigns.parquet` is (200, 64) (file sha256 `aab06934…28e5`) with `direction` **int64**, `lane` all
  `"card"`, `lag`, `lag_band`, `tide_band` ∈ {B1 25, B2 60, B3 56, B4 59}, `tide_band_label` ∈ {"B1 YOUNG tide",
  "B2 EARLY tide", "B3 MATURE tide", "B4 OLD tide"}, `tide_abs_gt206`, `era_of_entry` (tuning 123 / holdout 77),
  `entered_after_tc10_pin`; per-asset n BTC 39, ETH 48, NEAR 40, SOL 36, ZEC 37; latest entry close
  2026-09-18T12:00Z.
- Two different sums of the same book are on disk: `books/v6_campaigns.parquet` Σ net_r = `40.807566` (6-dp file)
  and the regbook base arm Σ net_r = `40.807564574147555` (full precision; `regbooks/P-AGE-1/base.json`).

### 1.9 The combined refusal, as TC11 already printed it
- `M/research_outputs/tierc11/stage_g/STAGE_G.md:197` and `stage_g/g_grid_books.parquet` (sha256 `b2c786e0…b51b`,
  8 rows, key `cell`): cell `age:on|win:on|ratr:off` → n **110**, mean_net_r **0.514611** (printed +0.5146),
  sum_net_r 56.607236, n_refused 90, sum_net_r_refused −15.799671. Recounted here from `books/v6_campaigns.parquet`:
  B4 59, `lag >= 16` 63, union 90, kept 110, kept mean 0.5146112636.
- Same table, cell `age:off|win:off|ratr:on`: n 147, n_refused 53, **sum_net_r_refused +21.692115** (the contract's
  "refusing forfeited +21.69R").
- Filed arms TC12's shadows can be held equal to (`SCORE_MANIFEST.json.inputs`): `P-AGE-1/scored` book_sha256
  `d008fa50…22d8` (OLD alone, n 141), `P-WIN-1/scored` `fd3f407a…bbfe` (stale alone, n 137),
  `P-AGE-1/tierE__shadow_abs206` `2c1e47ee…d169` (n 80).

### 1.10 Fixture families named by the TC12 contract — nearest code
Common harness (copied per file in TC11; shared in X as `tc11x_env_fixtures.say/clock/prove/plants`, :130-168):
`prove(fid, title, fails_if, break_leg, real_leg)` prints `FAILS IF:`, runs the BREAK leg first, which must go RED
or the fixture is VOID; `plants(rows)` judges `(name, expected detector substring, thunk)` one at a time — CAUGHT
only if a finding names the intended detector; a crash is a FIXTURE DEFECT (`tierc11_score_fixtures.py:330-388`).
Plants run on copies or under `mutated(obj, name, value)` restored in `finally` (:391-399). Referees are typed in
the fixture file as "a second object" (:253-304).

| TC12 fixture | nearest existing implementation | structure |
|---|---|---|
| **F-FAM** | **no fixture of that name exists in either tree** (grep). Nearest: TC11 F-VERDICT's family leg (`tierc11_score_fixtures.py:1521-1535`: a closed row with a number / spent test → "CLOSED-NUMBER"; `(family_m, bar_filed, tests_spent, len(rows)) != (9, 0.011111, 7, 9)`; sabotage "the bar loosened to 0.10/7 (tests actually run)" :1630) on a PLANTED family; X F-SCORE-X "BAR-OF-FAMILY" (`tc11x_score_fixtures.py:852`), "TESTS-SPENT" (:1281-1282), sabotages (i) "an EXIT row scored at bar 0.10" and (ii) "the m = 1 rule with clause (a) removed, fed p = 0.07 and lo < 0" (:1152-1154); X `verify_filing`'s FAMILY-BAR detector | typed referee table of (family, m, bar, rows, spent) |
| **F-KEY** | `key_break` / `key_real` (`tierc11_score_fixtures.py:2133-2300`): 18 plants on the regbook interface (era by OPEN, duplicate key, null net_r, dropped column, direction 0, haircut law broken, float32, sidecar n/sum/era_scope, entry bar longer than the lens, exit before entry, r_dist 0, a comma in a string, wrong int dtypes, stray asset); X `TP.check_keys(root, manifest)` (`tierc10_panel.py:2628`) on the draws table | interface validator + per-directory key check |
| **F-GRID** | `grid_tables` / `grid_findings` (`tierc11_score_fixtures.py:2072-2129`) through `TP.grid_whole(declared, written, cell_col, require_cols, require_false, label)` (`tierc10_panel.py:2592`): typed declared cells vs written; transcript "declared 9 cells, written 8; missing […], undeclared …, duplicated …" (`FIXTURES_SCORE.txt:79-80`: §0 9/9, FAMILY 9/9, Tier-E 27/27, 7 LOAO grids × 5) | counts asserted against a typed declaration; plants: row dropped / duplicated / undeclared |
| **F-DET** | `det_build` / `det_findings` (`tierc11_score_fixtures.py:3239-3313`): two SUBPROCESS scorer runs under `PYTHONHASHSEED` 1 and the tier seed into `_det_score/seed_<n>`, byte-equal to each other and to the in-process render, typed file set; plants: one byte bent, a pid salt, a set-iteration line; X adds `TP.check_det(root_a, root_b)` (`tierc10_panel.py:2661`) and "the seeded draws held byte-equal" | hash-identical files |
| **F-GATE** | `M/scripts/tierc11_stage_g_fixtures.py`: `gate_findings(scored, base, refused, label)` (:779-796) with detectors GATE-FOREIGN, **GATE-MISSED** (typed-refused campaigns still in the book), GATE-UNNAMED (removed but not named by the rule), GATE-ROW (kept row not row-identical to the base on EVERY column); `cohort_findings` (:799-808); `gate_break` (:1073-1143) — first plant "an UN-GATED book (scored == base)" must be caught by GATE-MISSED; also "the module's apply_gate returning the base (the module must HALT)"; `gate_real` (:1146-1213) recomputes the refused set from the fixture's own typed derivation (`typed_set`, `own_facts`) | refused set == the text, by an independent derivation |
| registry | TC11 F-SCORE-REG (`reg_break` :816 / `reg_real` :878; 9 plants incl. family_m 8, a contract byte, a chain prev); X F-REG-X + WORKTREE ATTESTATION (`tc11x_registrations_fixtures.py:19-56`) | production verifier AND an independent re-derivation |
| scorer arithmetic | TC11 F-BOOT (`hand_draws` :1127, `hand_draws_diff` :1142; plants: p bent to `#<0/B`, CI to 2.5/97.5, seed bent, draw unit bent to rows); X F-SCORE-X re-derives lo / p from `draw_hex` | hand computation with the same rng draws |

### 1.11 The TC12 line map (computed here by TC11's slice law on the filed bytes, sha `861d6050…`)
`raw.decode("utf-8").split("\n")` gives 138 elements (the last empty). Every text slice begins with its id + space
and carries its prior in `[NN%]`.

| object | lines | sha256 of the slice |
|---|---|---|
| P-ADM-1 [50%] | 53-56 | `b4f14e60f766ddfd7bf7847fcdccb4b069f6a32fd16816e0a27f7ceacd8281a1` |
| P-BRD-1 [40%] | 57-59 | `e049d8d9fb62cc5cf15e1145c696270c5bd369aeae63a5b2570a1d6d5decfd7d` |
| P-DIR-1 [45%] | 65-68 | `1b4dec34d1337d49e22266006550421d8e4d88618e639a6581078c3fb0fcaf26` |
| P-SFP-VA-1 [45%] | 69-75 | `f6e581da8fe470b9f3fe9e414b466459ec0180af8dbcad3c57cdfcdf2d9d2754` |
| P-SCALP-3 [30%] | 83-106 | `fa141ec5d25ab67fbe57a673b676d94152dd287f145f66621e0d23b2e1b52198` |
| LAWS (families, bar, precondition law) | 5-9 | `3ce9d5f8213a39ca03843fb2c73833dc7854c01115fd92a325d9f945409525d6` |
| RULINGS (Q8 pre_seen exception) | 12-16 | `112c0980974b71b0f21f28a5316e7a14d658a91622f2af00df2a43085e7fab67` |
| V2 state machine | 32-38 | `36b8321302c5acff8a22be1e4fa419345d7d357d06c7029d6896bf8949552bc2` |
| V3 the licence (Q-R3) | 39-41 | `91dbee3e59bbacca550ffcc7996fed56c0c09099f0c84c811b469977074a9489` |
| V4 traverse / time stop | 42-43 | `6d10f07b48a811958a83630d3bdbca8336511d4679835b9d4206c38fc8268b96` |
| STAGE C control | 48-50 | `74af3673db2f3ed61186d23bea699ea04f00f09cdf3eaa817442d16a0b485714` |
| STAGE G header (family) | 52 | `9c75b3ec4f751ee0f64143076a3724267328452bdfd791946ae868178d6cf6b0` |
| STAGE G Tier-E | 60-62 | `6c64124bfda63121fbde7eabbb5f3812f347b2dd6f293a961528ca1c48447cd6` |
| STAGE R header (family) | 64 | `8b1038704f484036362d644634faeba64e5543313f1af007a548b694a687a4bb` |
| STAGE R Tier-E | 76-80 | `7a82e7ce2e6fcd4076c45a683414b79bd64b6a4d1e77148f7a5ea833d4ff632e` |
| STAGE S header (family) | 82 | `886cea7d7542363f6b47a16667efb8c1c03f15fce92829c3eb3e3ccacedd2db9` |
| STAGE L (the fourth book) | 108-112 | `23c6297b424a32bb5204aa1ac64bb956d1f351f948482f18a30b0384a89a8036` |
| FIXTURES | 114-124 | `8499991137046a971f905bcbf0f2491c3eb859c6db987ff0ce755c8630ebc452` |
| VETOES BY NAME | 135-137 | `b1f2ee3a9f117dee14354cf90bd4f1bc1b8c63dd764a667b9e7b1276c1058235` |

Families as the contract states them (stage headers, regex `^STAGE ([A-Z]) · ([A-Z][A-Z-]*) FAMILY \(m=(\d+), bar
(\d+\.\d+)` matched here): `G ADMISSION m=2 bar 0.05` · `R RANGE-STATE m=2 bar 0.05` · `S SCALPER m=1 bar 0.10`;
q from line 8-9 "bar = 0.10 ÷ m per family". `P-ADM-1` also occurs on line 108.

### 1.12 Records TC12 will pin (path · sha256)
| record | sha256 |
|---|---|
| `M/exchange/queue/2026-10-08_TC12_APOLLO.md` | `861d6050e80e66995e4f9db2855aaf274d63285249c2549e5a0813582095a7bd` |
| `M/exchange/queue/2026-09-24_TC11_APOLLO.md` (103 lines) | `bb38e016a8f3e55ca3bcc09fec53ba6b8dc40accb60d054f8163d033a898f835` |
| `M/research_outputs/tierc11/registrations/REGISTRATIONS.json` | `648834bf30e20e92713bddef2374ddef1aae843f4d8ba152fc50166c8cc6f1ee` |
| `M/research_outputs/tierc11/registrations/REGISTRY_PIN.json` | `ea77921a410db962376412a5f179fd3d9225f81fb5405a788c8077cd46de748f` |
| `M/research_outputs/tierc11/LEANS.md` | `655e1605165e7a66c67f544e5cda421b46aa0b6fcd4cb97a6ad19654479f294f` |
| `M/research_outputs/tierc11/LEANS_AMENDMENTS.md` | `85f57ce7832b2754cff70fe052dc87dcf4bcf4182f61112c7a1d227df84f0c07` |
| `M/research_outputs/tierc11/scores/SCORES.json` | `2c1a664a27abfc320355dcb89b2eff8a7f7637ddc26843e72ab3baf30cbef856` |
| `M/research_outputs/tierc11/scores/FAMILY.json` | `3fa36bd482eac4de729b0e1ff2a66e7becbc30f2646ce16fc0df8fc369b2fd73` |
| `M/research_outputs/tierc11/scores/BASE_IDENT.json` | `29f795dcae5c3994f8cc09d742c7480e989f09afe72113b95e2e8859a8ca5581` |
| `M/research_outputs/tierc11/scores/REGISTRY_CHECK.json` | `aea83bf10b5bbe62ff6c0af542870cd60f5ad8773b6bb61fab45ea465d8f8ed0` |
| `M/research_outputs/tierc11/scores/SCORE_MANIFEST.json` | `4cde52cd5c019d663bdec4a2c74f4ce2e1812193066b379cf031411b886865b2` |
| `M/research_outputs/tierc11/scores/S0_VERDICTS.md` | `ea728250249e1f1f548faf315fac22515d653743075d64155c47f1ea06f670aa` |
| `M/research_outputs/tierc11/books/v6_campaigns.parquet` (file) | `aab06934ae92689ef2e0fcc6b857350cf397ddca7a0a57e180960c51669b28e5` |
| `M/research_outputs/tierc11/regbooks/P-AGE-1/base.parquet` (file) / canonical book sha | `dbfe4788610b11cc70ef64be31aac95949b921f086eaeb66b4535fbbad7af4ce` / `f41bfaf0…68a8` |
| `M/research_outputs/tierc11/regbooks/P-AGE-1/scored.parquet` (file) / canonical | `6440a6e0d14cfbf1c62df19246a066d0f7086a1e64aae3bb0ced8c2b2a624dca` / `d008fa50…22d8` |
| `M/research_outputs/tierc11/regbooks/P-WIN-1/scored.parquet` (file) / canonical | `824c5e08ca79511fea96b98d65b74e8e7209f36379d881a2ff02f927db08241c` / `fd3f407a…bbfe` |
| `M/research_outputs/tierc11/stage_g/g_grid_books.parquet` | `b2c786e0e7204e1be49c31c0ed7eae7e61365e61ae608dd0efcbe0f4e3b7b51b` |
| `M/scripts/tierc11_registrations.py` | `55cc090e811337100ed63a3c66aab28774579ce8b97bb0d685be933c84a82800` |
| `M/scripts/tierc11_score.py` | `81d99d63f9367268780fe9ec37a0c6af058b03670a83aaff010a93090eab5d68` |
| `M/scripts/tierc11_score_fixtures.py` | `ea30a40f25879143ee1a8ab7654eea9e2d4a0a499284ba592376a43a9fa20c22` |
| `M/scripts/tierc5.py` | `ad912b385cc8dd2e5291af3b79c520760ae8c91764af8e3eee56c6b3dd295a6f` |
| `M/scripts/tierc10_panel.py` | `40b660cdc943a947f199f2e59f38bfbda04866b44191506de2298d8474d79b0e` |
| `X/…/registrations/REGISTRATIONS_X.json` | `6b0eb52d63ce6823c35f27010705e04263b21e7bfc1603f241c9a7b4b7deb0a4` |
| `X/…/registrations/REGISTRY_PIN_X.json` | `6a445afe147f8e36eceeb03cc1b41c906b0c8102b0f36d2a4a32af6b42b72e73` |
| `X/…/registrations/SCORED_X.json` | `dd9b6e2db8b03377d30c3479504bc1510331582c459598813aca5a10adf804ae` |
| `X/…/registrations/build_manifest.json` | `fdbb5ba2095ca6aebb26085d662bc9b4b8ec67b7d8d1c002cd8b6506ae184d9b` |
| `X/research_outputs/tierc11x/REGISTRATION_PLAN.md` | `a887ea64a5099b8b27b5433d263969911ea7795c0fade2af9b40a5b92b8c3d15` |
| `X/research_outputs/tierc11x/LEANS_X.md` | `74a989ee6357e2169f2ad88722b67f1174cf0d080783dc8c77f5f064e3468623` |
| `X/research_outputs/tierc11x/LEANS_X_AMENDMENTS.md` | `af845b95d1c7699f788aa242af6f5bef0d0f86b92a74a938cb7ca14c9d87d059` |
| `X/scripts/tc11x_registrations.py` | `6bf4bf4e722477458dcc1cde44f3184581b6754392583b0cb40e27249ac09fc6` |
| `X/scripts/tc11x_registrations_fixtures.py` | `fdcc362f1bfc5029b4242521761673bedf4f5aff7c0322d1a31ce085ca48367e` |
| `X/scripts/tc11x_score.py` | `da7035a9ddbfe4a707a57a534c352ca79f5cac39ecc4a6c8b04102bf49620d92` |
| `X/scripts/tc11x_score_fixtures.py` | `a65fa3ebcd6c85d5ce3d62cebecd9931304007691b9410ad5457f92be7cdc884` |
| `X/research_outputs/tierc11x/va/feasibility.parquet` (the licence words; U-V's record) | `ea8573b3240bb1112521c55f0a52ee2ed7156c598b7665685d0b86eefbecb6f0` |

---------------------------------------------------------------------------------------------------------------
## 2 · CONTRACT-vs-DISK

1. **"bar = 0.10 ÷ m per family" (line 9) names a bar, not a verdict law.** The contract never says "CI lo > 0";
   "fails the bar" (line 104) is its only verdict phrase. Disk: both prior tiers decide by a conjunction that the
   executor froze as a reading (LEANS.md:115; LEANS_X.md:657-666 "The X contract names a bar. It does not name a
   new verdict law").
2. **No N_BOOT, no CI level, no p law in the contract.** Disk: 4000 draws, 5th/95th percentile, `(#<=0 + 1)/(B+1)`
   (`tierc5.py:1227-1235`; `tierc11_score.py:237`).
3. **"families declared by MECHANISM"** — the contract has no `FAMILIES (` line. Disk: X's parser needs one
   (`tc11x_registrations.py:488-493`, :808-812); both X regexes return nothing on the TC12 bytes (tested here). The
   families live in three stage headers (lines 52, 64, 82) and each header ALSO types its bar.
4. **"a registration closed by precondition spends no test" / F-FAM "a precondition-closed row spends no test"** —
   no TC12 row names a precondition. The nearest clause is V3 (lines 39-41), and it orders a HALT on disagreement,
   not a closure. Disk: both precedents name the precondition inside the operative spec and gate it on a record
   (`PRECONDITION_LENS` `tierc11_score.py:290`; X's landing record).
5. **"Label pre_seen (TC11 crossed table cell 110 @ +0.515)"** — disk has no cell called 110. `110` is the kept n
   and `+0.515` is `mean_net_r 0.514611` of cell `age:on|win:on|ratr:off` (`STAGE_G.md:197`, printed `+0.5146`).
   That table is a 2×2×2 over age / win / **ratr**, not the contract's new 2×2×2×2.
6. **"refuse … OR the window age (entry_i − arm_i) ≥ 16 bars"** — matches L-G.2 (LEANS.md:371) and the `lag` column;
   L-G.2 also records "The 16 cut has no on-disk provenance, and v6 lag 7–15 holds 4/200" (:373-374).
7. **"the tide age … in the OLD band (trailing q75, the cut of record)"** — matches L-G.1 (LEANS.md:357-361) and
   `tide_band == "B4"`. "the absolute-206 cut" is `tide_abs_gt206`, which "reads the corridor ahead" (:362-363).
8. **"breadth = share of the five home assets whose tide band is YOUNG or EARLY"** — disk bands are `B1 YOUNG`,
   `B2 EARLY`, `B3 MATURE`, `B4 OLD`, stamped per v6 CAMPAIGN at its entry bar. No per-bar band table for all five
   assets was found in this unit's files (TC10's `close/P_AGE_1_BAR_BANDS.parquet` exists; not inspected — another
   unit's).
9. **"refuse an anchor entry"** (P-DIR-1) — every v6 campaign has `lane == "card"`; no "anchor" lane value exists
   in `books/v6_campaigns.parquet`.
10. **"TC11 R5 (+0.49 with / −0.49 against, pivot states)"** — `M/research_outputs/tierc11/stage_r/R5_CHOP.md:120-121`
    (4h · calibrated · alignment): EXP_ALIGNED n 47 mean +0.4913; EXP_COUNTER n **12** mean −0.4939. The refused
    analogue is 12 of 200 campaigns.
11. **P-SFP-VA-1 and P-SCALP-3 carry no honesty label in the text.** Disk: X3 already printed VA `swing_failure`
    outcomes (H20/H100, eras ALL / tuning / holdout, CLASSIC5 and per asset) at 1h, 4h, 12h, 1d
    (`X/research_outputs/tierc11x/va/two_trades.parquet`, columns `lens, detector, trade, era, horizon, net, …`),
    and the 1h maker feasibility row (edge_net_h20 +0.038001, `va/feasibility.parquet`). Both precedents labelled
    such kin (TC11 P-BRK-4H; X KIN-SEEN, LEANS_X.md:753-772).
12. **"V3 … 4h taker PASS · 1d taker PASS · 1h maker PASS · 12h FAIL · 1h taker FAIL"** — disk carries FOUR rows of
    record (`of_record_for_detector == True`, `va_regime`, POOLED:CLASSIC5, holdout, taker): 4h `PASS`, 1d `PASS`,
    12h `FAIL`, 1h `"FAIL — maker twin PASSES (the reopening path; needs a toll-model change the operator rules)"`.
    "1h maker PASS" is a separate non-record row (`toll == "maker"`, `verdict_pass True`, toll 4.0 bps round trip
    from `research_outputs/tierc11/data/fee_schedule.json[BTCUSDT].maker_round_trip_bps`).
13. **"a probe that closes back inside within K=3 closes"** — X's SFP of record is K = 7 ("t − t0 <= 7 (RC.PINS
    DEV_RETURN_BARS)", `X/…/va/X3.md:16`); "k in [1, 3]" is a twin there.
14. **"COSTS OF RECORD: maker bps per side on entry and targets; taker on the stop"** vs the regbook interface: the
    AM-7 haircut law is a HALT on a scored arm and assumes every fee leg is taker (`tierc11_score.py:713-721`;
    LEANS_AMENDMENTS.md AM-7: "the maker twins apply the law to their taker legs only"). A maker-toll SCORED arm
    cannot pass the interface as written.
15. **"`data/fee_schedule.json` must carry maker_bps_side per venue"** — `M/data/fee_schedule.json` does not exist;
    TC11's is `research_outputs/tierc11/data/fee_schedule.json`, per ASSET, key `maker_bps_per_side` (the shim
    renames it `maker_bps_side`, `tierc11_env.py:1037`), 2.0 bps, "an ASSUMPTION" (LEANS.md:86-87). (U-D's unit;
    it is the scorer's `fees()` input.)
16. **"F-CTRL … Σ net_r 40.807566"** — that is the 6-dp `books/v6_campaigns.parquet`; the base arm every two-sample
    row was ruled against sums to 40.807564574147555.
17. **"Q1/Q2 keep SCORES.json leaves; stamp TC11 BUILT and re-pin its registry files"** — disk: the contract sha
    `bb38e016…` is named in 18 `scripts/tierc11_*.py` files (5 of them in a long form, `bb38e016a8f3…`) and in at
    least 11 TC11 records (the top level, `scores/`, `registrations/` and `close/` were searched) including the
    frozen `LEANS.md`, `BUILD_DRAFT.md`, `PROGRESS.json`, `REGISTRY_CHECK.json`, `S0_VERDICTS.md`;
    `REGISTRATIONS.json`'s own sha `648834bf…` is typed in `tierc11_score.py:224`, `tierc11_stage_g.py` and
    `tierc11_stage_t_brk.py`. `tierc11_close.py:609-612, :957` HALT when the contract sha is not the pinned one.
    No queue file's `BUILT:` line is at the end: on disk they sit on lines 4-12 (`exchange/queue/*.md`; convention
    `exchange/queue/README.md` item 6, "on a line of its own").
18. **"the extension printed separately (the forward strip, never scored)"** (line 50) while P-SFP-VA-1 is scored on
    the "full corridor" (line 69) and P-SCALP-3 on the "HOLDOUT era" (line 83): the contract does not say whether
    those two end at TC11's pin or at the new pin. Disk: one pin per tier (`PIN_MS = 1_790_294_400_000`,
    `tierc11_env.py:122`); X's VA records end at that pin.
19. **"LOAO 3/5 and the single-trade share"** — "read by" is not defined; on disk LOAO "decides nothing" and the
    share has two definitions and no threshold (§1.4).
20. **"NOT SUPPORTED if the through-tick book fails the bar; CLOSED FOR GOOD if it fails under DEEP too; CLOSED if
    it clears only under TOUCH"** — on disk a twin is Tier-E and "Tier-E arms carry no verdict word"
    (`VERDICT_RULE`, `tierc11_registrations.py:38-39`; collar guard `tierc11_score.py:262-263`). Here two twins
    decide the verdict text.

---------------------------------------------------------------------------------------------------------------
## 3 · READINGS NEEDED (candidate leans; freeze before any book)

**R1 · Filing architecture.** (a) TC11's: specs typed in the script; (b) X's: a frozen plan document carried
verbatim, families in the filing, a generated pin. → **(b)**. It is the only multi-family precedent, its verifier
exists (`verify_filing`), and its fixture checks every spec leaf against the plan.

**R2 · Verdict law.** (a) p ≤ family bar alone; (b) CI lo > 0 AND p ≤ family bar. → **(b)**, the L-1.4 / LX-1.2
conjunction, with the literal bar printed as a rival column. It is the stricter reading and reuses a filed law.
Consequence to state before the look: ADMISSION and RANGE-STATE (0.05) decide at lo and p together; SCALPER (0.10)
is decided by clause (a), bar cell worded as X's (`tc11x_score.py:141`).

**R3 · Families and m, read not typed.** Parse the three stage headers (lines 52, 64, 82) for name, m and bar; parse
q from line 9; HALT unless each header's bar equals q ÷ m. → file `families = [{ADMISSION, 2, 0.1, 0.05},
{RANGE-STATE, 2, 0.1, 0.05}, {SCALPER, 1, 0.1, 0.1, bar_binding false}]`.

**R4 · B, CI, p, exactness.** → N_BOOT 4000, 5th/95th percentile, `p = (k+1)/(B+1)` (TC11/X pins), seed 20261008
passed explicitly to every call, 20260816 beside. Clause (b) on a `Fraction` per family (SC-1): deciding rank
`floor((B+1)·bar)` = 200 at 0.05, 400 at 0.10, printed.

**R5 · Rulers.** P-ADM-1, P-BRD-1, P-DIR-1: two-sample, kept book vs the WHOLE v6 base, `T5.cluster_boot_diff`;
gates are post-filters (SC-16), never re-rides; the re-ride rival is a disclosure count. P-SFP-VA-1, P-SCALP-3: vs
zero, `T5.cluster_boot`. → as stated; this is the contract's own wording plus L-1.5.

**R6 · Corridor of record for the five rows.** (a) all five end at TC11's pin 2026-09-25T00:00Z, the bars after it
printed as a strip for every row; (b) gates at TC11's pin, the two lanes on the extended corridor; (c) all on the
extended corridor. → **(a)**. It reuses a filed pin, keeps the three gate bases byte-equal to TC11's v6 base
(`f41bfaf0…`), keeps X's VA records as the source of every stamp, and leaves all new bars to the forward ledger.
Era by the entry bar's close (L-1.3); P-SCALP-3's holdout = closes in (1_719_791_999_000, that pin].

**R7 · The base of the two-sample rows.** → ONE base arm for the three gates, asserted equal to TC11's regbook base
by canonical `book_sha256` `f41bfaf0…68a8` and to `books/v6_campaigns.parquet` on SC-7's 13 columns (F-BASE-IDENT
carried). Depends on R6.

**R8 · Preconditions.** (a) none anywhere; (b) P-SFP-VA-1: the mirrored word "VA-4h taker" == PASS; P-SCALP-3: the
mirrored "VA-1h maker" == PASS AND the maker fee of record is pinned with its source; the three gates: none. →
**(b)**, each read from the F-VA-MIRROR record by path + sha, cross-checked by the scorer as SC-17 does. Since V3
HALTs on a mirror disagreement, a closed row cannot arise in the real run: F-FAM proves "spends no test" on a
PLANTED family (TC11's method).

**R9 · Honesty labels and their wording.** → X's two templates. P-ADM-1: `pre_seen` → "<verdict> — IN-SAMPLE
RE-SCORE, NOT CONFIRMATORY (pre_seen …)", with SC-21's count of campaigns entered after 2026-09-21T16:00Z, and the
sentence that confirmation is the ledger's fourth book. P-BRD-1 and P-DIR-1: `selection_hazard
(DIRECTION-INFORMED)` → "<verdict> — NOT CONFIRMATORY (selection_hazard: DIRECTION-INFORMED)". P-SFP-VA-1 and
P-SCALP-3: the executor ADDS `selection_hazard (KIN-SEEN)` (item 2.11); the bar is unchanged, so the label costs no
power and cannot flatter.

**R10 · The pre_seen citation.** → cite the cell by its name and file: `stage_g/g_grid_books.parquet`, cell
`age:on|win:on|ratr:off`, n 110, mean_net_r 0.514611, n_refused 90; say that "110" is the n.

**R11 · LOAO and the share on P-SCALP-3.** (a) both printed, deciding nothing; (b) LOAO below 3/5 changes the
verdict word; (c) the verdict word stands, and the §0 cell appends a pre-named qualifier "ONE-ASSET DEPENDENT (LOAO
k/5 < 3/5)" when a SUPPORTED row fails the line. → **(c)**; LOAO = `TP.loao_n`'s law on the declared five, bar 3.
The share is printed in both filed forms (SC-22's block and LX-X1.9's `max|x|/|Σx|` with its key) with no
threshold, because none exists on disk.

**R12 · The scalper's fill ladder.** The twins TOUCH and DEEP are ruled by the same ruler, seed and bar as the
TICK book of record; m stays 1 and one test is spent. The eight outcomes need a frozen table. → recommended:
TICK clears → SUPPORTED (cell adds "FILL-SENSITIVE" if DEEP does not clear); TICK fails and DEEP fails and TOUCH
fails → NOT SUPPORTED — CLOSED FOR GOOD; TICK fails, DEEP fails, TOUCH clears → NOT SUPPORTED — CLOSED (clears only
under TOUCH); TICK fails, DEEP clears → NOT SUPPORTED. The two twin rows are filed as "fill-sensitivity rows of the
verdict text", a named exception to the no-verdict-word collar.

**R13 · The interface for a maker-toll scored arm.** → add `fee_taker_r` (the taker legs' fee over r_dist) and hold
`haircut_net_r = net_r − fee_taker_r × slip/taker` as the HALT law on P-SCALP-3 (AM-7's own maker clause); the
all-taker twin must satisfy the unchanged AM-7 law. Sidecar `lens`: `5m` for P-SCALP-3, `4h` for the other four.

**R14 · A gate that refuses nothing, or empties an asset.** → TC11's SC-6: FLAG "the difference is 0 by
construction", NOT SUPPORTED, test spent. No free closure.

**R15 · Proof of text-before-result.** → three clauses: exclusive-create filing; the registry head and the
filing's sha stamped into every regbook `STATUS.json` and stage manifest (new — neither tier did it), checked by
the scorer; a git-order attestation run out of process: at the REG commit no path exists under
`research_outputs/tierc12/{books,regbooks,stage_*,scores}`, and each such path's first-adding commit descends
from it. Keyed on paths, because the main branch receives daily `exchange: auto-publish` commits.

**R16 · Scorer write law.** → TC11's no-clobber + `--refile` + bit-flag exit, with X's persisted draws
(`draw_hex`).

**R17 · The beside-prints.** → carry all of X's (exact enumeration, SEED-FRAGILE, sign-flip, month-block twin,
drop-OPEN twin, size footnote), deciding nothing. `exact_cluster` is one-sample; a two-arm enumeration must be
written for the gates. It matters at 0.05: "The Monte Carlo SE of p near 0.05 at B = 4000 is 0.0034"
(LEANS_X.md:697).

**R18 · P-ADM-1's shadows.** → three Tier-E arms held byte-equal (canonical sha) to TC11's filed books (§1.9).

**R19 · "tc11-stamp".** (a) stamp and re-pin now; (b) stage it for after the operator's close acts; (c) leave
byte-frozen and file a sibling stamp. → **(b)**: staged as an operator step that runs after TC11's `close_acts.sh`,
the `BUILT:` line APPENDED as line 104 so all nine text slices keep their line numbers, payload shas and the head
`6772568b…`, with a fixture proving the head did not move. See H1.

**R20 · "anchor entry" in P-DIR-1.** → every v6 card campaign (the 4h anchor lens), i.e. the whole base book;
there is no narrower population on disk.

---------------------------------------------------------------------------------------------------------------
## 4 · HAZARDS

**H1 · The tc11-stamp breaks TC11's pending close and rewrites write-once records.** Changing one byte of TC11's
contract moves `bb38e016…`; `tierc11_close.py:609-612, :957` then HALT, and `close_acts.sh` step 0 re-runs F-LAR11
before anything is pushed. A re-pinned `REGISTRATIONS.json` moves `648834bf…`, which three TC11 scripts type, and
those scripts' shas are pinned in `PROGRESS.json`. If the stamp were inserted near the top like every other queue
file, all nine `text_lines` shift, every payload sha and the chain head change — a re-filing of registrations.
The frozen `LEANS.md` (sha `655e1605…`) also names the contract sha.

**H2 · TC11's scorer cannot be imported.** `tierc11_score` imports `tierc11_env`, which HALTs unless
`NAIAD_CACHE_DIR` is the tc11 snapshot and re-roots TC10 modules; it types m = 9, the nine ids, TC11's shas.
Importing it under TC12's substrate either HALTs or scores at TC11's bar.

**H3 · X is not merged and must not gain a file.** `tc11x_score` and `tc11x_registrations` import `tc11x_env` (an
audit hook, the tc11 snapshot). Running any X script writes `_det_*` or transcripts in the certified worktree.
X code can only be read at its sha and mirrored.

**H4 · The default seed is the sensitivity seed.** `T5.cluster_boot(...)` without `seed=` scores at 20260816
(`tierc5.py:86, :1178`). X plants this as sabotage (iii). `TP.loao_n`'s default seed is TC10's 20260921
(`tierc10_panel.py:91, :1235`).

**H5 · In-sample numbers clear the new bar.** P-WIN-1's filed p is 146/4001 = 0.0365 with lo +0.002964: NOT
SUPPORTED at 1/90, but it would read SUPPORTED at 0.05. The combined refusal is built from that and from P-AGE-1 on
the same 200 campaigns. A SUPPORTED P-ADM-1 is an in-sample re-score and must carry its label into §0, FAMILY and
the ledger append.

**H6 · NaN draws change the denominator.** In `cluster_boot_diff` a draw is NaN when an arm has no row in any
picked asset; `_ci_from` drops non-finite draws, so `p_den` falls below 4001 and the deciding rank moves. It can
happen when a gate or a lane leaves an asset empty (P-SCALP-3 on the holdout; a per-asset slice). `ci_of` records
`n_draws_finite`; a fixture should assert it is 4000 on every row of record.

**H7 · Look-ahead in the refused sets.** The trailing q75 edge uses bars with open ≤ the entry bar
(`tierc9._trailing_edges`; F-DEF's sabotage "a ONE-BAR-AHEAD trailing pool"); the absolute-206 cut reads the whole
corridor and is a shadow only. Breadth at the entry bar must use each asset's band as of that bar. Era and the
pre_seen count are judged by the entry bar's CLOSE; a bar closing AT a pin was seen.

**H8 · Row order is part of determinism.** The mean inside a draw sums rows in cluster order; the TC11 scorer sorts
`(symbol, entry_close_ms)` mergesort before ruling and hashes a canonical CSV with `repr(float)`. A book ruled
unsorted, or a set iterated into output, breaks F-DET under `PYTHONHASHSEED`.

**H9 · The main tree is a shared, moving branch.** HEAD moved during this scout; `exchange: auto-publish` commits
land daily and sweep `exchange/**`. Two tracked files are modified and uncommitted (§1.0). A TC12 commit made with
a broad `git add` would carry TC10's modified fixture transcript; an attestation that says "HEAD only adds TC12
files" would fail on an auto-publish commit.

**H10 · No ignore rule for tierc12.** Parquet under `research_outputs/tierc12/` would be committed. A root rule must
be appended at the END (TC10's records cite `.gitignore:263`), or nested as X did.

**H11 · Re-running TC11's fixtures or scorer is not free.** They write `_det_score/`, `_rerun` files and
transcripts under `research_outputs/tierc11/scores/`; `--refile` would replace the record whose leaves Q1 keeps.

**H12 · Two different "R2 FAIL at 1h".** X's P-SFP-RNG-1 closed on the PIVOT-range R2 (`SCORED_X.json`: "CLOSED BY
R2 (1h: FAIL)"); the licence TC12 mirrors is the VA detector's table (item 2.12). And TC12's K = 3 swing failure is
X's twin, not X's event of record.

**H13 · The maker toll is an assumption in the mirrored record.** "1h maker PASS" was computed at 4.0 bps round
trip. If Stage D pins a different maker fee, the mirrored word and the book's toll disagree.

---------------------------------------------------------------------------------------------------------------
## 5 · REUSE PLAN

**Import (through a TC12 env shim, never directly from TC11's or X's env):**
- `tierc5.cluster_boot`, `cluster_boot_diff`, `_ci_from` (:1178, :1200, :1227) — always with `seed=` and `n_boot=`.
- `tierc10_panel.loao_n` (:1234), `grid_whole` (:2592), `check_keys` (:2628), `check_det` (:2661), `make_put`
  (:2563), `stamp_n` (:2528), `above_half_bar` (:1193).

**Mirror from X (read at sha `6bf4bf4e…` / `da7035a9…`; do not import):**
- Filing: `contract_lines`, `cut`, `payload_sha`, `chain_of`, `render`, `render_pin`, `pin_of`, `file_filing`
  (exclusive create), `verify_filing`, `carry_spec` + the plan-document method; the pin's `witness_law`.
- Scoring: `verdict_of(lo, p, bar)` generalised, `literal_bar`, `exact_cluster`, `sign_flip_p`, `seed_fragile`,
  `month_of` and the month-block twin, `label_cell`, per-family `spent`, `draws_frame` with `draw_hex`, the CLOSED
  row's number-free form.
- Fixtures: F-REG-X's two-checker structure and its plants; the WORKTREE ATTESTATION's git-facts-out-of-process
  method; F-SCORE-X's re-derivation from persisted draws and sabotages (i)-(v).

**Mirror from TC11 (read at sha `81d99d63…`):**
- `canonical_csv` / `book_sha256` (SC-13), `validate_book`, `load_arm`, `load_status`, `two_sample_premise` (SC-6),
  `gate_findings` (SC-16), `gate_block` (SC-5), `ci_of` with the Fraction bar, `ruled` (vs_zero and two_sample
  branches), `loao`, `concentration` (SC-22), `preseen_facts` (SC-21), `base_ident` (SC-7), `write_outputs` and the
  exit bit word, `dry_run`, the collar guard.
- Fixtures: F-BOOT (`hand_draws`, `hand_draws_diff`), F-VERDICT's typed cases and family leg, F-KEY's 18 plants,
  F-GRID, F-DET, F-BASE-IDENT, F-COLLAR, F-DRYRUN, F-EXIT; from `tierc11_stage_g_fixtures.py` F-GATE
  (`gate_findings`, `cohort_findings`, `gate_break`, `gate_real`).

**Newly written:**
- `REGISTRATION_PLAN` for five rows in three families and `tierc12_registrations.py` with a families parser for the
  stage-header form (R3).
- `tierc12_score.py`: families from the filing; two-sample + vs-zero; the precondition records of R8; the fill
  ladder of R12; the maker interface of R13; a two-arm exact enumeration (R17); the head check against every
  regbook's stamp (R15).
- F-FAM (no code exists): typed (family, m, bar, rows, spent) referee on the real filing and on a planted family
  holding one precondition-closed row; plants: a bar scored at another family's value, m loosened to the tests
  run, a closed row printing a number or spending a test.
- The staged tc11-stamp step and its head-unchanged fixture (R19).
