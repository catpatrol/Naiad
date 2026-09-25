# SCOUT F: CLOSE, LEDGER, PUBLISH (for the TIER-C11 executor)

Scouted 2026-09-24 on branch `v12-v1-census`, HEAD `b9ed953`. The contract of record is `exchange/queue/2026-09-24_TC11_APOLLO.md` (8,442 B, sha256 `bb38e016…f835`, verified). This scout was read-only. The only file written is this one. All paths are repo-relative unless absolute.

---

## 0 · The facts that bite first

1. **TC10's CLOSE has not run. All of it is pending on the operator.**
   - `exchange/reports/BUILD_2026-09-21_TIERC10_UNSEEN_RANGES.md` does not exist. The draft is still `research_outputs/tierc10/BUILD_DRAFT.md`: 111,105 B, sha `244ad5a4…`.
   - `exchange/status/LEDGER_APOLLO.md` is still 2,426 lines, 174,090 B, sha `cd6ad43a…`. Its last block is TIER-C9 (2026-08-22, lines 2355-2426).
   - The TC10 append `research_outputs/tierc10/LEDGER_APOLLO_APPEND.md` (14,925 B, sha `1288b59b…`) still carries its `⟦STAMP AT CLOSE …⟧` placeholder at line 213.
   - HEAD is 50 commits ahead of `origin/v12-v1-census` and 0 behind. Nothing from TC10, OR-1, OR-2 or TC11 STEP Q has been pushed.
   - The worktree holds an uncommitted `M research_outputs/tierc10/close/FIXTURES_CLOSE_ledger_append_root.txt`. It is F-LAR's re-run at 9/9 GREEN, and `close_acts.sh` step 6 commits it.
2. **Name every new script `scripts/tierc11_*.py`, never `scripts/tierc10_*.py`.**
   - Evidence: `scripts/tierc10_resume_fixtures.py:254` `TC_SUITE_GLOB = "tierc10_*.py"`, and `:3685` `scripts_sweep_findings`.
   - Any `scripts/tierc10_*.py` on disk that is not in the 33-name `TC_SUITE_FILES` literal (`:255`) turns F-C10-RESUME RED.
   - Write nothing under `research_outputs/tierc10/**`. The root sweep and the stage sweeps (`:2844`, `:2857`) flag unrecorded files.
3. **The TC10 close tooling cannot be re-pointed.**
   - Every TC10 close builder hard-codes `research_outputs/tierc10`, the TC10 contract and the six REGS.
   - Most of them also HALT at import unless `NAIAD_CACHE_DIR == ~/.cache/naiad/snapshots/tc10_20260921`: `box_cost:160`, `forward_strip:100`, `regime_prior:110`, `p_age_1:101`, `ledger_append_root:64`, and `v6_control_twin`, which imports `tierc10_data` and HALTs through `tierc10_data.py:115`.
   - Three modules are import-safe on any env (stdlib only at import): `tierc10_close_close_ledger_append` (LA), `tierc10_close_close_s0_verdicts` and `tierc10_close_close_findings`.
   - Consequence: TC11 forks its own `scripts/tierc11_close_*.py`.

---

## 1 · The build document: its structure and the §0 verdict row

### 1a · TC10 (the draft of record; LAW 5 moves it at close)

The file is `research_outputs/tierc10/BUILD_DRAFT.md`. Its headings, by line:

- `:1` `# BUILD — TIER-C10 · "<NAME>": …`, then a DRAFT banner and a header bullet list: contract of record with sha, rulings sha, drafted/executor/seed, AS-OF OF RECORD, substrate, reading rule, and "SIZE — named, as CONVENTIONS §3.2 asks".
- `:35` `## 0 · VERDICTS` opens with a bold one-line headline, then:
  - `:54` `### 0.1 · The six, in order of filing` (the table)
  - `:80` `### 0.2 · Each row, read under its own text`, one `#### <REG> [<prior>%] — <VERDICT>` per registration
  - `:240` `0.3` the selection hazard · `:314` `0.4` the family + LAW 3 · `:327` `0.5` the admitted list · `:361` `0.6` the forward strip
- `:391` `## R0 · WHAT THE INTERRUPTION LEFT` (R0.1–R0.5)
- `:546` `## 1 · STAGE B — …` · `:662` `## 2 · CENSUS-R` (`2.1` height-vs-toll GATE · `2.2` acceptance · `2.3` outcome-after-event · `2.4` coverage · `2.5` P-AGE-1/boundary-fade/regime-prior)
- `:985` `## 3 · STAGE D MANIFEST` · `:1148` `## 4 · FIXTURES` · `:1191` `## 5 · FINDINGS — REPORTED, NOT FIXED` · `:1264` `## 6 · OPERATOR QUESTIONS STILL OPEN` · `:1304` `## 7 · WHAT THIS BUILD IS NOT` · `:1323` `## 8 · DISPOSITION · BOX-COST`

The §0.1 row format (`BUILD_DRAFT.md:62`), verbatim header:

```
| # | registration · prior | scored arm · panel · era · ruler | n | point (R / campaign) | 90% CI | verdict under its own text | p · `clears_bh_bar` (bar 0.016667) | LOAO line of record (bar) | equal-asset-risk co-headline | haircut twin |
```

Row example:

```
| 4 | P-TRG-2 · 40% | trg-9/12 vs card v6 · CLASSIC5 · full · two-sample | 198 (base 200) | Δ +0.257697 | [+0.108587, +0.383892] | **SUPPORTED** (CI-only). … | 0.005249 · **true** | 5/5 above (3) | Δ +0.250885 [+0.092816, +0.397402] | Δ +0.258438 |
```

A HALTed slot prints `—` in every numeric cell and puts the HALT text in the verdict cell.

The machine-transcribed twin is `research_outputs/tierc10/close/S0_VERDICTS.md`, built by `scripts/tierc10_close_close_s0_verdicts.py`:
- `VCOLS` at `:119`: `("#","registration","prior","arm","panel","era","ruler","n","point","[CI lo, CI hi]","p (one-sided)","verdict","clears BH bar","LOAO above / present vs bar · line","haircut twin E[R]","height-vs-toll (BRK)")`.
- Every value is copied string-for-string from `scores/<REG>.rows.json` → `rows[j].score_row` (the arm with `scored_in_family` true) and from `scores/FAMILY.json rows[k].clears_bh_bar`. JSON is parsed with `parse_float = parse_int = Tok`, so no float is ever made. F-S0-READ re-reads each value.
- Legs: F-S0-READ/SIX/BAR/HALT/ADMIT/STRIP/NOTYPE/CLOSURE/WRITES + F-DET. **F-S0-SIX hard-codes exactly 6 rows**, and `FIXED_SOURCES` (`:106`) hard-codes the tierc10 paths. Fork it for nine rows.

Where the §0 numbers come from:
- `score_row` holds 124 keys. The ones the §0 uses are `n`, `ci_point`, `ci_lo`, `ci_hi`, `p_one_sided`, `verdict`, `ruler`, `arm_era`, `panel_name`, `loao_above_of_record`, `loao_assets_present`, `loao_bar_above_half`, `loao_line`, `ear_ci_point/lo/hi`, `expectancy_r`, `net_r`, `tail_exit_ratio` (**the D15 tail ratio that P-TP-RNG wants "printed on the row"**), `max_single_trade_delta_share`, `paired_delta_expectancy_r`, `two_sample_ci_*`, `unpaired_base_n`, `unpaired_cell_n` and `prior_pct`.
- `beside` holds `haircut_twin` (`twin_expectancy_r`, plus `twin_difference_r` on two-sample rows), `per_asset_n` and `per_asset_rows`. BRK rows add `brk_sealed_row.height_vs_toll.{lens,verdict_pass,reason}`.
- FAMILY.json keys are `family_m_declared` (6), `fdr_bar_q_over_m` (0.016666…), `law`, `rows[]` (score_row plus `clears_bh_bar`, `fdr_m_declared`, `fdr_m_tests_actually_run`, `fdr_note`), `rows_files_sha256` and `scored_slots_halted` (a {reg: HALT text} map).

### 1b · TC9, a finished build document

`exchange/reports/BUILD_2026-08-18_TIERC9_HABITAT_PAIRS.md` (21,478 B):

```
# BUILD — TIER-C9 · <NAME>
**Lane** … · **Branch** … · **Seed** … · **AS OF** …
**RATIFIED** …
## §0 · <REFRAME> — AND VERDICTS FIRST      (### The registered verdict — one table; ### where the sweep lit up; ### habitat)
## §1 · STAGE A …   ## §2 · STAGE B …   ## §3 · THE OWED BATCH   ## §4 · FIXTURES — 13/13 · F-CTRL …
## §4b · THE REVIEW   ## §5 · FINDINGS — NOT FIXED (TC9-a … TC9-e, one bold paragraph each)
## §6 · DISPOSITION + BOX-COST (disposition table + "### BOX-COST — constants read LIVE from publish_exchange": before/after exchange/** and tick set, level, headroom)
--- *End of build document. <one-paragraph recap>*
```

TC9's §0 verdict header: `| registration | prior | ruler | Δ (2-sample) | 90% CI | p | verdict | LOAO |`.

### 1c · What TC11 asks for (contract :96-100)

`exchange/reports/BUILD_2026-09-24_TIERC11_EVENTS.md`, laid out as:
- §0: nine rows, R5's chop table, and the feasibility verdicts per lens
- the nesting grid, whole
- the warnings tables
- the gates crossed
- the scalper's twins
- the adds head-to-head
- findings-not-fixed
- BOX-COST
- the LEDGER append

LAW 5 applies (the draft lives off-bus and moves at close), so draft at `research_outputs/tierc11/BUILD_DRAFT.md`.

---

## 2 · BOX-COST: what it measures and how

**The rule.** CONVENTIONS §3.2 (`exchange/status/CONVENTIONS.md:341`) requires a table of every file the build created, modified or moved. It has seven columns: `PATH · EXISTS · TRACKED · COMMITTED · PUSHED · PROTECTED BY · BOX COST`.
- BOX COST is bytes plus % of the box for box-bound paths (under `exchange/`, or `LEDGER.md`, the tick set), and **FLAGGED** when a file is strictly over `FLAG_BYTES`.
- Anything not synced reads `n/a — unsynced (<root>)`.
- "Committed is not pushed. Pushed is not backed up."

**The constants** (`scripts/publish_exchange.py`, verified today):

| constant | value | line |
|---|---|---|
| `SCOPE` | `"exchange/"` | :48 |
| `SUBJECT` | `"exchange: auto-publish {date}"` | :49 |
| `BOX_BYTES` | `16_000_000` | :95 |
| `WARN_FRACTION` | `0.40` | :109 |
| `REFUSE_FRACTION` | `0.70` (the check is strictly `>`; exactly 70% only warns) | :110 |
| `OVERRIDE_ENV` | `"NAIAD_ALLOW_OVERSIZE_PUBLISH"` | :111 |
| `TICK_EXTRA` | `("LEDGER.md",)` | :128 |
| `FLAG_BYTES` | `64_000` (a naming trip-wire, never a refusal) | :160 |
| `HEARTBEAT_PATH` | `exchange/status/HEARTBEAT.md` | :67 |
| `MANIFEST_REL` | `exchange/status/MANIFEST.json` | :329 |

Pure helpers you can reuse: `budget(total_bytes)` returns `("OK"|"WARN"|"REFUSE", frac)` (:201); `over_flag(sized)` (:360); `_index_sizes(repo)` returns `[(size, path)]` for index blobs under exchange/ (:523); `tick_extra_bytes(repo)` (:269).

**How TC10 built it.** `scripts/tierc10_close_close_box_cost.py` produced `close/S8_DISPOSITION_BOX_COST.{md,json}` and `FIXTURES_CLOSE_box_cost.txt`.
- It reads the constants by `ast.literal_eval` and never imports `publish_exchange` (F-BC-CONST).
- Rows come from four sets:
  - (a) every path in a commit whose subject starts `tierc10`, found with `git log --grep=^tierc10 --name-only` and the subject re-checked;
  - (b) every PROGRESS.json artifact, with `cells` directories collapsed to one row each;
  - (c) the PLANNED build document, sized from the draft;
  - (d) the frozen snapshot, marked `n/a — outside repo; NOT PROTECTED until the LaCie mirror`.
- Git access is limited to `log`, `ls-files`, `check-ignore`, `branch -r --contains` and `rev-parse`, with no fetch (F-BC-GIT).
- PUSHED means `git branch -r --contains <sha>`. PROTECTED BY reads "GitHub only" if pushed and unmodified, otherwise NOT PROTECTED.
- F-DET runs inside a "quiet window" input fingerprint.
- Section layout: 8.0 at-a-glance counts · 8.1–8.5 the four sets · 8.6 BOX COST table · 8.7 findings BC-1…BC-6 · 8.8 volatile fields.
- The S8 on disk is a PRE-CLOSE snapshot, stale at HEAD `3d55988`.

**TC10's build-doc §8 also carried a compute cost.** That is a table of workflows and agents from `~/.claude/projects/-Users-luis-Naiad/<session>/workflows/wf_*.json`: session · role · workflows · agentCount · wall hours from `durationMs` (`BUILD_DRAFT.md:1334-1347`). TC9's version was the before/after tick-set table only.

**Measured today, read-only.**
- exchange/ index: 2,615,220 B across 115 files. Plus `LEDGER.md` at 259,298 B, the tick set is **2,874,518 B = 17.97% · OK**. WARN starts at 6,400,000 B.
- Files already over the wire: `LEDGER.md` 259,298 · `LEDGER_APOLLO.md` 174,090 · `LEDGER_ATHENA.md` 143,605 · several BUILD docs.
- **The TC11 build doc will be FLAGGED (over 64,000 B).** CONVENTIONS §3.2 requires naming it to the operator, with its home, at creation.
- TC10's pending close will add about 161.6 KB: draft 111,105 + builder's report 35,597 + append 14,925.

---

## 3 · The findings-not-fixed format

The full artifact is `research_outputs/tierc10/close/S5_FINDINGS_NOT_FIXED.{md,json}`, built by `scripts/tierc10_close_close_findings.py`. That script is import-safe, but its paths are hard-coded at `:113-135`.

The JSON has these top-level keys: `schema, label, status_law, tier, as_of_of_record, contract, built_by, inputs, git_volatile_fields, git, cross_references, counts, measured{i..vi}, findings[]`.
- Each `findings[]` entry has `id, class ∈ {HARVESTED, MEASURED, LEAN}, harvest_key, label ("REPORT-ONLY · Tier-E"), owner ∈ {operator, executor}, owner_basis, source, status ("REPORTED, NOT FIXED"), text, text_form`.
- Id conventions: `FN-PROG-<stage#>-B<k>|N<k>` (PROGRESS blockers/notes) · `FN-RUL-L1-<k>` · `FN-M-<i..vi>` · `LEAN-<SURFACE>-<id>`.
- MD sections: `## 0 · Inputs` (path | bytes | sha256) · `## 1 · Counts and index` · `## 2 · Measured` · `## 3 · Harvested — verbatim, by source` · `## 4 · LEANS` · `## 5 · git-volatile fields` · `## 6 · What this document is not`.

Each MD finding block looks like this:

```
#### FN-PROG-01-B1

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · stage **D-CORE** (PARTIAL) · …
- source: `research_outputs/tierc10/PROGRESS.json` · `stages[1].blockers[0]`
- owner basis: `<path>` — "<verbatim quote>" — *<reading>*

~~~text
<verbatim text>
~~~
```

The build-doc condensation (`BUILD_DRAFT.md:1191`) points to the full harvest by path and sha, then gives a numbered list of the findings that bear on reading the build: bold lead sentence plus 1–4 lines. TC9 used `**TC9-a · …**` paragraphs.

---

## 4 · The LEDGER_APOLLO append: format and destination

- **Destination:** `exchange/status/LEDGER_APOLLO.md`, the commissioning lane's ledger (CONVENTIONS §3.1). It is append-only; a correction is a new entry.
- **Not** `LEDGER.md`. That file is the "Data-Spend Ledger — Maintained by the REVIEWER only". Its last edit was `cf0240b` on 2026-08-15, and no TC tier has appended to it.
- **Staging file:** TC10 staged its append at `research_outputs/tierc10/LEDGER_APOLLO_APPEND.md` (force-added, tracked), and the operator appends it with `cat "$APP" >> "$LEDGER"` (`close_acts.sh:98`). Mirror this at `research_outputs/tierc11/LEDGER_APOLLO_APPEND.md`.

**Byte format.** Mechanised by `check_format` in `scripts/tierc10_close_ledger_append_root.py:554-567`. Copy it; the module cannot be imported off the TC10 snapshot.
- The block opens with `SEP = "\n---\n\n"`. The ledger currently ends in `=== END ===\n`.
- The body must match `=== STATUS_APOLLO — \d{4}-\d{2}-\d{2} — TIER-C\d+ · [^\n]+ ===\nLANE      [^\n]+\nCLASS     ` (LANE and CLASS padded to col 11).
- It ends with `\n=== END ===\n`, with exactly one `=== END ===` and nothing after it.
- `"Operator: click Sync now."` must NOT appear inside the appended bytes. It is the session's final line, not ledger content.

Content style (TC10 root append):
- A two-space-indented section per theme: VERDICTS · the one that clears, priced · rulings cited · the named question · ALSO FILED · INTEGRITY · OPEN FOR THE OPERATOR · NEXT · THE TIER LINE.
- The block ends on the tier line, e.g. "TEN TIERS. … SAIL stays HELD (Q6). SAIL-READY remains card_spec freeze at v6 PLAIN."

The cite syntax, parsed by `LA.parse_quotes` / `LA.verify_quote` in `scripts/tierc10_close_close_ledger_append.py:978/:1012`:
- A cite line: `CITE_RE = ^( *)«path:L1[-L2]»$` or `«path#selector»` (`:964`).
- Quote lines follow at indent+2, beginning `| ` (one per source line) or `+ ` (a wrapped continuation, rejoined with one space).
- JSON selectors are `.key`, `[N]` and `[key=value]` (`resolve`, `:212`).
- `render_quote(indent, q)` (`:626`) with `q = {"path","l1","l2","sel","text"}`. Wrap width is `QUOTE_WIDTH - indent - 4`, with `QUOTE_WIDTH = 78`. Lines up to `NO_WRAP_UP_TO = 104` characters are not wrapped.
- F-LAR also demands that every digit in the prose is covered by a trace, a masked token or an exemption (F-LAR-COVER). A number whose value is only known after the push goes in a `⟦STAMP AT CLOSE …⟧` placeholder, filled after the push.

TC11's contract requires the append to carry: "m=9; SAIL still HELD; the forward ledger opened".

---

## 5 · `publish_exchange.publish(repo, date_str, remote="origin", log=print, allow_oversize=None)` (:565)

This is the only invocation of record (CONVENTIONS §3.4):

```
~/venvs/naiad/bin/python -c "import sys; from pathlib import Path; R=Path('.').resolve(); sys.path.insert(0,str(R/'scripts')); import publish_exchange as p; r=p.publish(R,'<YYYY-MM-DD>'); print(r['status'], r['commit'], r['pushed'], r['offenders'])"
```

What it does, step by step:

1. `git rev-parse --abbrev-ref HEAD`. A detached HEAD returns ERROR (:600).
2. **`git add -- exchange`** (:603). This stages *every* change under exchange/, including untracked files. A `.git/index.lock` produces a specific message and is never deleted.
3. It reads the index back (`git diff --cached --name-only -z`) and applies `guard()`: every staged path must start `exchange/`. If one does not, it runs `git reset` (mixed, no paths, worktree untouched), returns **FLAGGED**, and does not push (:623-631).
4. If nothing is staged it returns **NOTHING** and pushes nothing. It still prints the head-pair and flag lines.
5. D3 budget: exchange index bytes plus `LEDGER.md`, run through `budget()`. A REFUSE (over 70%) resets and returns **REFUSED** unless overridden. A WARN only prints. It also prints bus-health, the over-FLAG_BYTES list and the heartbeat line.
6. `git commit -m "exchange: auto-publish <date>"` (:737). There is **no Co-Authored-By trailer**.
7. **`git push origin <branch>`** (:745, timeout 600 s).
   - On failure: **ERROR**, "committed X but push failed", and the local commit stays.
   - On success: **PUBLISHED**, `pushed=True`.
8. `finally` (:765): `mailbox_refresh.refresh(repo)` rebuilds `MAILBOX/`, a gitignored folder of symlinks plus `000_README.txt`. It runs on every return path.

The return dict holds `status, commit, branch, pushed, offenders, staged, error, bytes, fraction, tick_bytes, tick_fraction, budget, heartbeat, bus_health, over_flag, mailbox`.

**Yes, it pushes, and it pushes the whole branch.** That includes TC10's, OR-1's, OR-2's and TC11's unpushed local commits (50 today).

Push hazards:
- TC10's builder `git push` was **refused by the local permission classifier ("Out-of-Place Publication")**, and the builder did not route around it (`BUILDERS_REPORT…TC10-STAGE-B-CLOSE.md` §4 Q0). That is why TC10's acts were handed to the operator as `close_acts.sh`.
- OR-2's ruling Q-3 was "push WITHHELD; the operator's TC10 close_acts.sh pushes" (memory `or2-execution-state.md`).
- TC10's R6 granted "Permission to push" for **TC10**, with the destination never named (`research_outputs/tierc10/OPERATOR_RULINGS.md:36-37,64`). No TC11 ruling grants a push.
- **The last real push attempt failed.** The 2026-09-24 07:00 daily auto-publish logged "committed a33a513 but push failed: ssh: connect to host github.com port 22: Undefined error: 0" (`exchange/status/daily/DAILY_2026-09-24.md:122`). The same failure applies to e63f922.
- **The daily routine (07:00 launchd) calls publish().** It will sweep any uncommitted `exchange/**` change the executor leaves behind (a TC11 draft or a half-made ledger append) into an "exchange: auto-publish" commit, and push it if SSH works.

**"STATE push" means state the push result on screen.**
- TC10's contract reads "publish_exchange; STATE push result" (`exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:139`).
- OR-2's reads "state the push result plainly" (`exchange/queue/2026-09-22_OR2_oracle_rulings_ARGUS.md:130`).
- CONVENTIONS §3.3 says "states on screen whether the push SUCCEEDED."
- Print `status`, `commit`, `pushed`, `offenders` and the error text. Then list the bright paths, then the final line `Operator: click Sync now.`

---

## 6 · P-AGE-1: the tide-age definitions (TC10 close) and what TC11 must pin

**The TC10 table.** `research_outputs/tierc10/close/P_AGE_1_TIDE_YOUTH.md` (+ `.parquet`, 5×54), `P_AGE_1_BAR_BANDS.parquet` (8×37), `P_AGE_1_EDGES.parquet` (7×19). Builder: `scripts/tierc10_close_p_age_1_tide_youth.py`. It is Tier-E and in-sample, and its fixtures are 7/7.

**The age.** `tierc7_lab_regime.tide_streak(sym)` returns `(state, run, start)` (`scripts/tierc7_lab_regime.py:306-349`).
- `state = +1 if e89 > e316 else -1` on the 4h frame (`T7.frame(sym)["f"]`), counted only from `TIDE_WARM_BARS = RC.WARMUP_BARS = 316` (`:179`).
- `run[j]` is the number of consecutive bars ending at j with an unchanged state; the flip bar is bar 1.
- `run = -1` below the floor. `start[j] == 316` marks a left-censored streak, whose age is a lower bound.
- The age is read **at the campaign's ENTRY bar** `i = t.entry_i` (`scripts/tierc9.py:1353-1360`).

**The trailing-quantile definition, which is the one of record.**
- `STREAK_BAND_QUANTILES = (0.25, 0.50, 0.75)` (`tierc7_lab_regime.py:181`).
- `STREAK_LABELS = ("B1 YOUNG tide","B2 EARLY tide","B3 MATURE tide","B4 OLD tide")` (`:446`).
- `_trailing_pool(lo_ms, hi_ms)` (`scripts/tierc9.py:1290`) pools `run[j]>0` over the bars of every `RC.UNIVERSE` asset (CLASSIC5) inside [lo, hi], sorted by `open_ms`.
- `_trailing_edges(pool, at_ms)` (`:1318`) gives `np.quantile(pool["sk_v"][:i2], (0.25,0.5,0.75))` over the prefix `open_ms <= at_ms` (inclusive), and returns None while that prefix is under `RC.PROVISIONAL_MIN_N = 30`.
- `_streak_band(run, edges)` (`tierc7_lab_regime.py:456`) is `np.digitize(run, edges)` and returns None if `run <= 0`.
- **The OLD band is band index 3 = "B4 OLD tide" = `run >= q75_trailing(entry bar)`.** The edge is inclusive at q75 because digitize uses `right=False`.
- The trailing q75 edge at the year-ends 2020…2026 was 199.5, 363.5, 472, 453, 402, 402, 404 bars.
- `tc7g_tables(lo_ms, hi_ms)` (`scripts/tierc9.py:1331`) installs `_tag_trailing` over `LR._tag_book`. It HALTs if a campaign is against the tide, or is unbanded under warm edges.
- The per-campaign tag frame is NOT filed. `capture(lo, hi)` (`p_age_1:356`) records it in memory only. Its columns: `symbol, lane, entry_ms, entry_iso, direction, net_r, n_reentries, rv_rel, rv_ann_pct, vol_band, vol_band_label, streak_bars, streak_band, streak_band_label, tide_state, left_censored`.

**The absolute definition, "age > 206 bars".**
- 206.0 is the **whole-corridor bar-pooled q50** (the B2|B3 edge; whole-corridor edges are `[88.0, 206.0, 396.0]`, `P_AGE_1_BAR_BANDS`). It is not the OLD band's edge.
- Under whole-corridor edges B3+B4 hold 62+58 = **120 of 200** v6 campaigns with streak ≥ 206, so the shadow refuses about 120 against the trailing OLD band's 59.
- The trailing-edge median streak inside B4 is 549 bars (range 216–1246); inside B3 it is 298.5 (98–474).

**The results** (v6 control, CLASSIC5, 4h, corridor 2019-09-08T16:00Z → 2026-09-21T16:00Z, 200 campaigns):

| band (trailing) | n | net R | E[R] | win % | left-censored |
|---|---:|---:|---:|---:|---:|
| B1 YOUNG | 25 (provisional) | +11.7692 | +0.4708 | 52.0 | 0 |
| B2 EARLY | 60 | +34.6369 | +0.5773 | 40.0 | 2 |
| B3 MATURE | 56 | +17.9938 | +0.3213 | 35.7 | 0 |
| **B4 OLD** | **59** | **−22.6566** | **−0.3840** | 20.3 | 2 |
| ALL | 200 | +41.7433 | +0.2087 | 34.5 | 4 |

Refusing the OLD band is worth +22.6566 R in-sample: the remaining 141 campaigns net +64.3999 R. **P-AGE-1 is therefore selected on this very table.** It is an in-sample re-score, like P-TRG-2. Only bars after 2026-09-21T16:00Z are unseen.

**A second, different "tide age" exists.** `tierc9.tide_streak_age(t, roles)` (`scripts/tierc9.py:537`) counts at the **ARM bar**. Its state comes from role arrays with a close filter (+1 iff `tide_f>tide_s and close>tide_s`, −1 mirrored, else 0), and its floor is `roles.floor_bars`. F-DEF must name which function it uses, and must fail if the other one is swapped in.

---

## 7 · REGIME_PRIOR and "the five-row table"

**"The five-row table" is `research_outputs/tierc10/stamps/control_entry_by_state.parquet`** (5×28, built by `scripts/tierc10_stamps.py:1093 entry_state_crosstab`).
- Rows: `macro_state_at_entry` ∈ {BEAR_EXP, BULL_EXP, NEUTRAL, NONE, __ALL__}.
- Columns: `macro_state_at_entry, n, n_assets, net_r_sum, expectancy_r, median_net_r, win_rate_pct, median_mfe_r, median_pct_of_range, median_dist_boundary_atr, n_in_range, provisional, provisional_note, tier, gates, m_looks_this_table, m_note, in_sample, scored_in_family, as_of_*` (8), `warranty`.
- Values: NEUTRAL n 94, +27.884748 R, E +0.296646 · BULL_EXP 66, +14.509604, +0.219842 · BEAR_EXP 40, −0.651001, −0.016275 · NONE 0 · ALL 200, +41.743351, +0.208717.
- `REGIME_PRIOR.md` Table 2 reproduces it exactly as its "Entry-state marginal" (F-RP-ANCHOR).

**REGIME_PRIOR itself** is `research_outputs/tierc10/close/REGIME_PRIOR.md`, built by `scripts/tierc10_close_regime_prior.py` with fixtures in `…_fixtures.py`, 8/8.
- Table 1, `REGIME_PRIOR_TIME_IN_RANGE.parquet` (102×26): time-in-range per asset × lens {5m,4h,1d} × scale_kind {calibrated, frozen3.0}, copied from `census/coverage.parquet`.
- Table 2, `REGIME_PRIOR_V6_BY_STATE.parquet` (73×31): the v6 book by rf4h macro state at entry × at exit (a 64-cell grid plus marginals).
  - Columns: `table, cut, entry_rf4h_macro_state, entry_rf4h_in_range, exit_rf4h_macro_state, exit_rf4h_in_range, n, n_assets, net_r_sum, expectancy_r, win_rate_pct, provisional, provisional_note, rf_lens, rf_scale_mult, book, tier, selection_not_a_result, m_selections_this_table, m_note, in_sample, gates, as_of_*, warranty`.
  - The chop signal: NEUTRAL→NEUTRAL has n 68, −31.751314 R, E −0.466931.
- `rf4h_in_range == (macro_state == 'NEUTRAL')` on 200/200 campaigns. The stamps' four-valued collapse means "in range" is exactly NEUTRAL.

**The stamps source** is `research_outputs/tierc10/stamps/control_v6_stamped.parquet` (5,745×45; its `instant_kind` values include entry and exit, 200 each).
- It carries `rf4h_{macro_state, in_range, range_id, pct_of_range, dist_boundary_atr, nearest_side, boundary_age, range_age, dev_top, dev_bot, inception_top, inception_bot, last_flip, last_flip_age, state_latch, bar_open_ms, bar_close_ms, bar_lag, bar_lag_ms}`.
- `stamps/build_manifest.json`: `stamp_lenses ["4h"]`, `scale_mult 3.0`.

**Gaps for R5.**
- **There is no 12h lens anywhere.** `tierc10_census.LENSES = ("5m","4h","1d")` (`scripts/tierc10_census.py:117`), and `tierc10_stamps.LENS_OF_RECORD = "4h"` (`:119`).
- `pct_of_range` is NaN outside NEUTRAL, so "%-of-range decile" exists only for in-range entries: 94 at 4h, about 9 per decile, all under n 30 and provisional.

---

## 8 · FORWARD_STRIP: the precursor of TC11's forward ledger

`scripts/tierc10_close_forward_strip.py` produced `close/FORWARD_STRIP.{md,parquet}` (4×33) with fixtures 9 legs.
- **Book:** v6 only, read from `panel/control_journal.parquet`, which is sha-anchored to PROGRESS `PANEL/gate`.
- **Window:** TC9's as-of `2026-08-22T00:00:00Z` (ms 1787356800000) to TC10's pin `2026-09-21T16:00:00Z`.
- **Membership predicates:**
  - `ENTERED-IN-STRIP`: `entry_ms >= start`
  - `CONTINUATION`: `entry_ms < start <= exit_ms`
  - `OPEN-AT-CORRIDOR-END`: `exit_reason == 'corridor_end'` (marked to the pin, not realized)
- **Columns:** `label, window, tier, scored, asset, lane, direction, arm_ts, entry_ms, entry_ts, exit_ms, exit_ts, exit_reason, bars_held, entry_px, exit_px, r_dist, gross_r, fee_r, funding_r, net_r, haircut_twin_net_r, haircut_twin_tier, haircut_twin_charter_round_trip_bps, as_of_*` (8), `warranty`.
- **Result:** 4 campaigns. 3 closed for −0.689692 R; 1 ETH long is open, marked +3.642965 R; the total is +2.953273 R. It is never scored. One ETH campaign was armed inside TC9's window and entered after it.
- **What TC11 adds:** the frozen 9/12 book side by side; a standing, refreshable ledger (nothing like it exists); "unscored until n ≥ 30".
- **The frozen 9/12 book** is P-TRG-2's arm (`research_outputs/tierc10/registrations/P-TRG-2.json` `book_spec.arms[0]`):
  - `tierc8.Card` with the v6 fields;
  - `tierc9.Roles(tide_f=89, tide_s=316, trg_f=9, trg_s=12, win_f=12, win_s=89)`;
  - arm `"trg-9/12 vs card v6 · CLASSIC5 · full"`, era full, runner `run_cell_n`.
- **The v6 book** is `tierc8.CARD_V6_CONTROL` (`scripts/tierc8.py:267`) with `tierc9.V6_ROLES` (`scripts/tierc9.py:119`).

---

## 9 · TC10's pending close, and how TC11 avoids breaking it

**What is pending.** The operator's `research_outputs/tierc10/close/close_acts.sh` has 120 lines and has not been run. Its steps:

| step | what it does | TC11 hazard |
|---|---|---|
| 0 | preconditions: on `v12-v1-census`; **index clean** (`git diff --cached --quiet`); DRAFT, RPT_SRC, APP and LEDGER exist; **`exchange/reports/BUILD_2026-09-21_TIERC10_UNSEEN_RANGES.md` and `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-09-23_TC10-STAGE-B-CLOSE.md` must NOT exist**; the stamp is pending | never leave staged files; never create those two paths |
| 1 | `git push origin v12-v1-census` (the whole branch, TC11's commits included) | TC11 commits ride along; this is harmless |
| 2 | `cp` the draft to the DOC, `git rm` the draft, commit, push | — |
| 3 | `mv` the builder's report into `exchange/reports/` | — |
| 4 | fill the stamp with the count of HEAD commits **whose subject starts `tierc10`** and how many of those are on a remote, then re-run F-LAR | **TC11 commit subjects must never start with "tierc10"** |
| 5 | `cat APP >> exchange/status/LEDGER_APOLLO.md` | if TC11 appends first, TC10's block lands after TC11's (ORDER) |
| 6 | `git add` APP and `FIXTURES_CLOSE_ledger_append_root.txt`, commit | do not commit or revert that transcript (it is `M` now) |
| 7 | `publish()` stages ALL of exchange/**, commits and pushes | **any uncommitted TC11 exchange/ file is swept into TC10's publish commit** |
| 8 | bright paths, then "Operator: click Sync now." | — |

**Pins and cites that TC11 must leave intact.**
- **F-LAR** (`scripts/tierc10_close_ledger_append_root.py`) verifies cites by content at the line numbers given.
  - `exchange/status/LEDGER_APOLLO.md:2371-2374` and `:2422-2423` (`REQUIRED`, `:581`).
  - `LEDGER.md:829, :834, :835, :836`.
  - `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:2-3, :137, :139`.
  - It reads `ERA_CUT_ISO` from `scripts/tierc10_panel.py:746`.
  - An append at the END of LEDGER_APOLLO leaves every cite valid. Inserting or editing above line 2426, or anywhere in `LEDGER.md` at or before :836, breaks it.
  - It pins no ledger sha across runs. F-LAR-NOWRITE compares within one run only.
- **Ledger line counts are pinned** in `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` and `DATA_SPEND_AUDIT.json` (corpus, 65 files):
  - `exchange/status/LEDGER_APOLLO.md` `"lines": 2426`, still matching;
  - `exchange/status/LEDGER_ARGUS.md` `"lines": 565`, **now 612, already a mismatch**.
  - `scripts/tierc10_data_fixtures.py` F-DET (`DET_FILES` at `:2121`) re-describes the snapshot offline and demands byte-identity, so it is **already RED** from the ARGUS appends. TC10's own step 5 will add the LEDGER_APOLLO mismatch.
  - D-CORE is PARTIAL, so F-C10-RESUME does not re-run it. It is disclosed, not blocking.
  - The corpus (`tierc10_data.py:1676 _spend_corpus`) also covers every `exchange/status/LEDGER_*.md`, every repo-root `*.md`/`*.json` and `research_outputs/rangefinder/*`. **TC11 must not add a root-level .md/.json or a new LEDGER_*.md.** A root file containing PUMP, PUMPFUN, MNT or SUI tokens would also turn F-D-5's never-touched grep RED.
- **F-C10-RESUME** (`scripts/tierc10_resume_fixtures.py`) re-hashes 1,090 artifact shas across 13 COMPLETE-VERIFIED stages, anchors on committed `research_outputs/tierc10/PROGRESS.json` (`PINNED_LEDGER_REV = "2e92972"`, `:185`), and sweeps `scripts/tierc10_*.py` and the tierc10 root.
- **The registry:** `research_outputs/tierc10/REGISTRY_PIN.json` (len 6, head `7621a857…`) and `research_outputs/tierc10/registrations/`. TC11 must never `register()` into it.
- **`.gitignore:263`** = `research_outputs/tierc10/**` is cited. Any new ignore line goes at the END (283 lines today), as OR-2 did.

**Files TC11 must not touch:**
- `research_outputs/tierc10/**`, including PROGRESS.json, BUILD_DRAFT.md, LEDGER_APOLLO_APPEND.md, close/*, scores/, registrations/, data/AS_OF_PIN.json and stamps/
- `scripts/tierc10_*.py`
- `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md` (sha `8a0bf279…`)
- `LEDGER.md`
- `exchange/status/LEDGER_APOLLO.md` above line 2426
- the two exchange/reports paths above
- `.gitignore` lines 1–283
- `engine/rangefinder.py` and `scripts/rangefinder_twin.py` (shas pinned by TC10 registrations, per memory `or1-recovery-state.md`)
- the snapshot `~/.cache/naiad/snapshots/tc10_20260921`

**The safe order.** The operator runs `close_acts.sh` before TC11's CLOSE. If TC11 reaches CLOSE first, it should HALT its LEDGER append and its publish until TC10's block has landed, or ask the operator. Otherwise TC11's block lands before TC10's in an append-only ledger, and TC11's publish pre-empts the operator's TC10 push.

**TC10 executor debt left after the operator's run** (named, not TC11's): record the CLOSE run in PROGRESS.json; regenerate S8; retire or re-render `REGISTRATION_TEXTS.md`. One stale fact: `BUILD_DRAFT.md:1373` (and `:1166`) cite the append's pre-stamp sha as `d6a58f5c…`, but the certified append is `1288b59b…`.

---

## 10 · Gaps: what the existing code cannot do today

- **G1. No reusable close tooling.** See §0.3. Fork `s0_verdicts`, `findings`, `box_cost` and the ledger certifier into `scripts/tierc11_close_*.py`.
- **G2. `import tierc10_data` HALTs off the TC10 snapshot** (`tierc10_data.py:90,115`). That makes `haircut_twin_net_r` (`:1408`) and `load_asof` unusable on a new "latest closed 4h bar" corridor.
- **G3. The TC10 pin caps the corridor.** `tierc10_panel.corridor_n` caps the corridor at TC10's write-once `research_outputs/tierc10/data/AS_OF_PIN.json` (2026-09-21T16:00Z) through `stage_d_pin()` (`tierc10_panel.py:634-647, 685-689`). `pin_close_iso` can only look back. `run_cell_n` HALTs past it (`:1173-1179`). The forward ledger and the TC11 corridor need `TP.AS_OF_PIN` re-pointed (a module global read at call time) or a fork.
- **G4. The canonical registry is TC10's `REG_DIR`** (`tierc10_panel.py:99`).
  - `run_cell_n` refuses non-control books from any other registry on real bars (`:1157-1163`).
  - `finish_family(rows, family_m=FAMILY_M, canonical_only=True)` (`:2465`) HALTs on non-canonical rows.
  - `FAMILY_M = 6` (`:103`). Pass `family_m=9` to `register(…, family_m, root)` (`:1674`) and to `finish_family`. The bar is `FDR_Q/9 = 0.10/9 = 0.011111` (`tierc5.py:1156 FDR_Q = 0.10`).
- **G5. No 12h lens** (for R3, R5 and P-TP-RNG's "12h boundary") and no 12h stamps. See §7.
- **G6. No maker toll model.** Only the taker fee exists: `tierc2_rules.FEE_BPS_SIDE` (`:122`), round trip 10 bps. That blocks Stage S's "maker twin" and the §0 "scalper's twins".
- **G7. No forward-ledger machinery.** There is no persistence, no refresh and no n≥30 trigger. FORWARD_STRIP is one-shot, v6-only and TC10-pinned.
- **G8. The per-campaign tide-age tag frame is not filed.** P-AGE-1 must recompute it through `T9.tc7g_tables` / `_trailing_edges`.
- **G9. Push authority.** No TC11 ruling grants a push. The classifier refused the TC10 builder's push, the SSH push failed at 07:00 today, and publish() always pushes.

## 11 · Ambiguities (contract phrases quoted)

- **A1.** "LEDGER append (m=9; SAIL still HELD; the forward ledger opened)" (:98-99). This is LEDGER_APOLLO by CONVENTIONS §3.1 and the TC9/TC10 precedent, not `LEDGER.md`, which is reviewer-only.
- **A2.** "publish_exchange; STATE push" (:99). Read it as *state the push result* (TC10 :139). Whether this line is the operator's word to push is unclear given the TC10 refusal. The TC10 pattern was an operator-run script.
- **A3.** "§0 verdicts first (nine rows + R5's chop table + the feasibility verdicts per lens)" (:96-97) against R5's "the 'killed in chop' test, printed first in §0" (:31). It is unclear which leads §0.
- **A4.** "P-WARN-1 … ELSE report-only, no slot spent, stated" (:41-42) against "m = 9 independently-failable hypotheses (bar 0.10/9)" (:9). TC10's law is that m is declared and fewer tests never loosen the bar (`finish_family` docstring), so the bar stays 0.10/9 either way. Say so on the row. The same applies if P-SCALP-2 stops on its R2 precondition (:62-63): a HALT row, as P-BE-1 was.
- **A5.** "FORWARD LEDGER (standing, unscored until n ≥ 30): frozen base and frozen 9/12 re-ridden on new bars only at every refresh" (:58-59). Open points:
  - the start instant: TC10's 2026-09-21T16:00Z, which the builder's report §5 proposes, or TC11's pin;
  - whether n ≥ 30 counts per book or both combined;
  - how to treat campaigns armed before the start;
  - where the ledger lives and who refreshes it.
- **A6.** "TRAILING-quantile definition (refuse the OLD band) … absolute definition (refuse age > 206 bars)" (:45-46). 206 is the whole-corridor median, not the OLD edge (about 400), so the shadow refuses about 2× as many campaigns. The contract does not name which age function applies (entry-bar `LR.tide_streak` or arm-bar `T9.tide_streak_age`).
- **A7.** "the five-row table extended" (:30) is not named by file. §7 identifies it as `stamps/control_entry_by_state.parquet`. "×%-of-range decile" only exists for in-range entries.
- **A8.** "BOX-COST" (:98). TC10's §8 carried both the seven-column disposition/box table and a workflow/agent compute-cost table. TC9 carried the box figures only.

---

## 12 · How to call these from a new tierc11 script

```python
#!/usr/bin/env python
# scripts/tierc11_close_<x>.py   — NEVER scripts/tierc10_*.py (F-C10-RESUME scripts sweep)
# Run: export NAIAD_CACHE_DIR=<the TC11 snapshot> PYTHONDONTWRITEBYTECODE=1  (BEFORE python starts)
import os, sys, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))

# ── (1) cite / quote helpers: import-safe on ANY env (stdlib only at import)
import tierc10_close_close_ledger_append as LA
q = {"path": "exchange/queue/2026-09-24_TC11_APOLLO.md", "l1": 99, "l2": 99, "sel": None,
     "text": " (m=9; SAIL still HELD; the forward ledger opened). publish_exchange; STATE push; final line:"}
block_lines = LA.render_quote(4, q)                  # ['    «…:99»', '      | …']
src = {q["path"]: (ROOT / q["path"]).read_bytes()}
for qq in LA.parse_quotes("\n".join(block_lines)):
    ok, why = LA.verify_quote(qq, src)               # (True, "ok")
# JSON cite: {"path": rel, "l1": None, "l2": None, "sel": "rows[0].score_row.verdict", "text": "SUPPORTED"}

# ── (2) the LEDGER_APOLLO format check (copy; F-LAR is NOT importable off the TC10 snapshot)
SEP = "\n---\n\n"
HDR = re.compile(r"=== STATUS_APOLLO — \d{4}-\d{2}-\d{2} — TIER-C\d+ · [^\n]+ ===\nLANE      [^\n]+\nCLASS     ")
def append_ok(block: str) -> bool:
    return (block.startswith(SEP) and HDR.match(block[len(SEP):]) is not None
            and block.endswith("\n=== END ===\n") and block.count("=== END ===") == 1
            and "Operator: click Sync now." not in block)

# ── (3) box constants and the box measure (publish_exchange is import-safe; NEVER call publish() in a build)
import publish_exchange as PX
sized = PX._index_sizes(ROOT)                        # [(bytes, 'exchange/…')], index blobs
extra_total, extra_rows = PX.tick_extra_bytes(ROOT)  # LEDGER.md
level, frac = PX.budget(sum(b for b, _ in sized) + extra_total)
flagged = PX.over_flag(sized + extra_rows)           # files > PX.FLAG_BYTES (64,000)

# ── (4) P-AGE-1 tide age, both definitions (needs the substrate env; imports bind cache paths)
import tierc7_lab_regime as LR, tierc9 as T9
pool = T9._trailing_pool(lo_ms, hi_ms)               # CLASSIC5 bars, run>0, sorted by open_ms
state, run, start = LR.tide_streak(sym)              # entry-bar age, sign(e89−e316), warm floor 316
f = T9.frame(sym)["f"]; i = entry_index               # i = the campaign's entry bar (t.entry_i)
ed = T9._trailing_edges(pool, int(f.open_ms[i]))     # {"vol_rel": […]|None, "streak_bar": [q25,q50,q75]|None}
band = LR._streak_band(int(run[i]), ed["streak_bar"]) if ed["streak_bar"] else None
refuse_trailing = (band == 3)                        # 3 == LR.STREAK_LABELS[3] == "B4 OLD tide"
refuse_absolute = int(run[i]) > 206                  # shadow; strict '>' per the contract text
left_censored = int(start[i]) == LR.TIDE_WARM_BARS   # age is a LOWER bound

# ── (5) family bar for m = 9 (pass it; the module default is 6)
import tierc10_panel as TP
# TP.REG_DIR / TP.AS_OF_PIN are TC10's — re-point (module globals) or fork BEFORE register/run_cell_n/finish_family;
# never write into research_outputs/tierc10/registrations.
fam = TP.finish_family(rows, family_m=9)             # bar = TP.FDR_Q / 9 = 0.011111
```

The close sequence the executor should mirror (TC10 `close_acts.sh`, adapted):
1. Push the committed work. This needs the operator's word.
2. `cp` the draft to `exchange/reports/BUILD_2026-09-24_TIERC11_EVENTS.md`, with the sha checked across the copy. `git rm` the draft and commit on its own.
3. Fill any `⟦STAMP AT CLOSE⟧` after the push, then re-certify.
4. `cat research_outputs/tierc11/LEDGER_APOLLO_APPEND.md >> exchange/status/LEDGER_APOLLO.md`, after TC10's block.
5. Commit the non-exchange residue explicitly.
6. Run `publish()` and STATE its push result.
7. List the bright paths.
8. End on the final line: `Operator: click Sync now.`
