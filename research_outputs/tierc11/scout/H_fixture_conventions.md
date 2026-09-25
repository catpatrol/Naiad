# SCOUT H · Fixture conventions and the resume law, mapped for TIER-C11

Scouted 2026-09-24. HEAD `b9ed953` (`tierc11(STEP Q)`), branch `v12-v1-census`. The contract is
`exchange/queue/2026-09-24_TC11_APOLLO.md`. Its sha256 on disk is `bb38e016a8f3…898f835`, the same value the STEP Q
commit subject records. This scout wrote one file, this one. It ran `scripts/tierc10_resume_fixtures.py` once, with its
transcript redirected to a scratchpad (`--root=<scratch>`): **9 GREEN, 0 RED**, and nothing in the repo was written. It
did not commit.

---

## 0 · Read these first: the facts that bind TC11's fixture work

1. **TC10's modules HALT at import on any substrate but `tc10_20260921`.**
   - `scripts/tierc10_census.py:96` and `scripts/tierc10_data.py:117` call `assert_substrate()` at module level. That
     check requires `NAIAD_CACHE_DIR` to resolve exactly to `~/.cache/naiad/snapshots/tc10_20260921`
     (`tierc10_census.py:70-93`, `tierc10_data.py:94-114`).
   - Everything that imports them is therefore pinned to the TC10 snapshot: `tierc10_stamps` (`:103`), `tierc10_null`
     (`:100`), `tierc10_lanes` (`:125`), `tierc10_brk` (`:122`) and `tierc10_score` (`:144-146`).
   - Only `tierc10_panel.substrate()` (`:161-195`) is snapshot-agnostic. It refuses the live cache and checks the
     loader binding.
2. **`tierc10_panel.corridor_n()` and `control_window()` clamp every corridor to TC10's pin.**
   - `stage_d_pin()` (`tierc10_panel.py:634-647`) reads `research_outputs/tierc10/data/AS_OF_PIN.json`, which pins
     `2026-09-21T16:00:00Z`, close_ms `1790006400000`.
   - `corridor_n` (`:650-744`) clamps to that pin, and `pin_close_iso` "may only look back" (`:690-695`).
   - The TC11 header asks for "full water, latest closed 4h bar, one as-of pin". **No TC10 entry point can produce a
     corridor later than 2026-09-21T16:00Z.** See GAP-1.
3. **`research_outputs/tierc11/**` is NOT gitignored.**
   - `git check-ignore -v --no-index research_outputs/tierc11/foo.txt` returns nothing (exit 1).
   - The tierc10 tree is ignored at `.gitignore:263-264` (`research_outputs/tierc10/**`, `research_outputs/tierc10_run2/**`).
   - Its documents of record were force-added with `git add -f` (59 tracked files, 0 parquet).
4. **TC10 is not closed.**
   - `PROGRESS.json` stage `CLOSE` is `PARTIAL`, blocked on the operator's push and the LaCie destination.
     `research_outputs/tierc10/close/close_acts.sh` is the operator's script and has not been run.
   - `exchange/reports/` holds no `BUILD_2026-09-21_TIERC10_UNSEEN_RANGES.md`, and `exchange/status/LEDGER_APOLLO.md`
     holds 0 TC10 lines.
   - The branch is 50 commits ahead of `origin/v12-v1-census`.
5. **F-C10-RESUME is green at HEAD.**
   - Measured this session: 9 GREEN, 0 RED. 1,090 artifact shas re-hash across 13 COMPLETE-VERIFIED stages.
   - The TC10 corridor is one value. The self-anchor, the ledger anchor and the transcript anchor all hold.
   - Adding `scripts/tierc11_*.py` does NOT turn it red: its scripts sweep globs `tierc10_*.py`
     (`tierc10_resume_fixtures.py:254`).
   - Each of these DOES turn it red:
     - any uncommitted edit to `research_outputs/tierc10/PROGRESS.json`;
     - any new loose file in the `research_outputs/tierc10/` root, which is swept against `TC_ROOT_ALLOWLIST` at `:193-213`;
     - any new file inside a COMPLETE-VERIFIED stage directory of tierc10.
   - **TC11 must write nothing under `research_outputs/tierc10/`.**

---

## 1 · The TC11 LAWS line and where each law lives in TC10 code

| TC11 law (contract line 6-9) | TC10 origin | Enforcing code of record |
|---|---|---|
| resume law: R0 census | TC10 RESUME contract lines 26-33 | procedure only (§4.2); the ledger is `PROGRESS.json` |
| verify-or-quarantine | RESUME LAW 1 + 2 (lines 12-15) | F-C10-RESUME-1 (re-hash), -2 (quarantine), `_partial_<ts>/README.md` |
| frozen texts | RESUME LAW 3 (lines 16-18) | registry chain `tierc10_panel.register()` `:1674`; texts `research_outputs/tierc10/REGISTRATION_TEXTS.json` |
| one corridor | RESUME LAW 4 (lines 19-20) | F-C10-RESUME-3 (`corridor_findings` `:3174`); `TP.stage_d_pin()` |
| draft off-bus | RESUME LAW 5 (lines 21-22) | convention: `research_outputs/tierc10/BUILD_DRAFT.md` moves at CLOSE via `close_acts.sh` |
| PROGRESS.json per stage | RESUME LAW 6 (lines 23-24) | F-C10-RESUME-0/-5 (well-formedness `wellformed_findings` `:4507`) |
| read-only worktrees | review law of 2026-08-17 | F-WORKTREE-ATTEST (`tierc10_panel_fixtures.py:3243`), an attestation, never a check |
| as-of warranties | TC6V-a | `tierc8.stamp` (`scripts/tierc8.py:96`) + `TP.stamp_n` (`tierc10_panel.py:2528`); F-KEY demands all 9 columns |
| every fixture leg states its failure condition | house rule since F-C4-h | `prove(... fails_if ...)` prints `FAILS IF:` (§2) |
| every grid reported whole | F-GRID | `TP.grid_whole` (`tierc10_panel.py:2592`) |
| "a SELECTION, not a result" | CENSUS-R collar | `tierc10_close_regime_prior.py:151-155` (`SELECTION`, `COLLAR_COLS`), `check_collar` `:637-660` |
| ONE family m=9, bar 0.10/9 | TC10 m=6 | `TP.FAMILY_M = 6` (`tierc10_panel.py:103`); `register(..., family_m=...)`, `finish_family(rows, family_m=...)` take it as an argument |

---

## 2 · The fixture leg: how failure is stated, and the break + real pattern

### 2.1 The invariant (every TC10 suite)
- Each fixture has a **BREAK leg that runs FIRST**. It plants one deliberate violation on a COPY (an array, frame, text or
  temp dir) and **must go RED**.
- A break leg that stays GREEN, or that RAISES, makes the fixture **VOID**, which counts as a FAIL.
- Then the **REAL leg** runs. It must be GREEN.
- The string `FAILS IF: <condition>` is printed for every fixture. It is typed as the third element of the leg table.
- **Banned** (verbatim in every header): "self-comparison; one example where cardinality was possible; a tuned magnitude
  bound standing in for an identity; a check whose claim is not the design's claim."
- A break leg is exactly one of two things:
  - a CORRUPTED INPUT handed to the module's own guard, which must refuse it (`attack(fn)`); or
  - a MUTATION of the module, under which the real leg's own checks must go RED (`mutated(...)`).
  - A leg that re-derives a wrong answer locally "proves nothing about the module" (`tierc10_panel_fixtures.py:2-10`).

### 2.2 Four harness dialects. Choose ONE and copy its exact shape.

**(A) Single break leg + `plants()`, the RF and RESUME dialect.** This is the most rigorous, and the TEMPLATE in §8 uses it.
- `scripts/tierc10_rf_fixtures.py`:
  - `say()` `:129`, `clock()` `:134` (stdout only, prefixed `[clock · stdout only]`), `check()` `:139`
  - `prove(fixture, title, fails_if, break_leg, real_leg) -> None` `:144`
  - `plants(rows) -> (bool, str)` `:167`
  - leg table `LEGS` `:1129`, whose tuples are `(id, title, fails_if, break_fn, real_fn)`; `main()` `:1170`
- `scripts/tierc10_resume_fixtures.py` has the same shape with hardened `plants()` at `:946-974`: **a plant that CRASHES
  is a FIXTURE DEFECT, not a catch**, and a `SystemExit` counts as a finding. Its helpers: `say` `:906`, `clock` `:911`,
  `check` `:917`, `prove` `:922-943`, `FIXTURES` table `:5577`, `main` `:5771`.
- Contract of the legs:
  - `break_leg() -> (ok: bool, detail: str)` must return **ok=False**, which is RED and correct.
  - `real_leg() -> (ok, detail)` must return ok=True.
  - `plants([(name, thunk -> list[findings]), ...])` judges ONE plant at a time. It returns `(True, ...)`, meaning VOID,
    if any plant yields no finding or crashes.
- Globals: `LINES/T`, `PASSED`, `FAILED`. Exit is `1 if FAILED else 0`.
- Transcript lines this dialect prints:
  ```
  <FID> — <title>
    FAILS IF: <condition>
    [BREAK] deliberate violation -> RED (correct): <detail>      | GREEN (FIXTURE IS VOID)
    [PASS] <FID>: <detail>                                       | [FAIL]
  ```

**(B) A list of break legs + real lines, the PANEL / LANES / STAMPS dialect.**
- `scripts/tierc10_panel_fixtures.py`: `prove(fid, title, fails_if, breaks: list, real) -> bool` at `:118`, `say` `:81`,
  `mutated(obj, attr, wrong, checks)` `:96`.
- `scripts/tierc10_lanes_fixtures.py`:
  - `prove` at `:150-179`, `_norm()` `:97` (scrubs `f-<leg>-XXXXXXXX` temp names), `say()` `:103` (normalises)
  - `refused(fn)` `:109`, `attack(fn)` `:118`, `mutated(obj, attr, wrong, checks)` `:127-146`
- Leg shapes: `breaks = [(name, fn -> (ok, detail)), ...]`, and `real() -> (ok, [lines])`. Each line is prefixed
  `[OK ]`, `[BAD]` or `[NB ]`.
- `FAILS IF:` is printed AFTER the real lines here. `RESULTS[fid] = ok` and `ok = r_ok and not void and bool(breaks)`.
  **A fixture with zero break legs cannot pass.**
- Transcript: `--- <FID> — <title>`, then `[BREAK] <name> -> RED (correct): …`, then the real lines, then
  `FAILS IF: …`, then `[PASS] <FID>`.
- Summary line: `FIXTURE SUMMARY  n/N PASS  {json RESULTS}`.

**(C) Real + sabotages as precomputed tuples, the CLOSE dialect.**
- `scripts/tierc10_close_p_trg_2_seen_share.py:590` defines `leg(name, fails_if, real: (ok, why), sabotages: [(desc, (ok, why))])`.
- Transcript:
  ```
  F-SS-BOOK · FAILS IF …
    real      GREEN — …
    sabotage  <desc>: RED (as required) — …
    => F-SS-BOOK GREEN
  ```
- It is compact. The sabotage is computed by calling the SAME `chk_*` function on a bent copy, for example
  `chk_book(bent, I)`.

**(D) The leg re-run under a context-manager sabotage of the code, the SCORE dialect.**
- `scripts/tierc10_score_fixtures.py:68`: `@contextmanager mutated(obj, name, value)`.
- Legs are `leg_*()` and re-run themselves inside `with mutated(TP, "score", tripwire): ...`.

### 2.3 Idioms the executor must carry
- **Substrate guard before any engine import.** `tierc2_baseline` binds `KLINES` from `engine.data.cache_dir()` AT
  IMPORT, so the env var must be exported before python starts (`tierc10_panel.py:161-195`).
- Guard forms:
  - `guard_substrate(env)` (`tierc10_close_p_trg_2_seen_share.py:96-113`) tests the live cache on the PATH STRING first,
    then resolved.
  - Its fixture F-SS-SUBSTRATE feeds `None`, `str(LIVE_CACHE)` and a foreign dir, and requires a HALT on each. Its
    sabotage is a guard that accepts anything.
- **Output guard.** `output_guard(paths)` plus `write_out()` (`p_trg_2:208-222`) refuse any write outside the stage dir.
- **F-*-NOWRITE.** `bytes_snapshot()` (`:204`) hashes the protected files before and after the run. Protected:
  `scores/`, `registrations/`, `REGISTRY*`, `PROGRESS.json`, `FIXTURES_RESUME.txt`, and the inputs.
- **Closure-by-AST ban on scoring calls.** `chk_closure(src)` (`p_trg_2`, around `:640`) forbids
  `FORBIDDEN_ATTRS = ("score", "finish_family", "register", "_mark_scored")` in report-only builders. Its sabotage is
  the source plus `"\nTP.score(None)\n"`.
- **Every leg prints totals, never samples.** Counts are totals, as in "every grid whole".
- **LEANS / RULINGS.** An executor reading is tagged `[LEAN-HEPHAESTUS] <id>` and printed in the transcript header. An
  operator ruling is a separate `RULINGS` tuple (`tierc10_resume_fixtures.py:432-456`).

---

## 3 · The named generic fixtures, exact implementations

### 3.1 F-DET: two subprocess runs under different PYTHONHASHSEED
Three variants exist. TC11's contract names bare "F-DET".

**(i) Two subprocess builds into two temp roots, file-set plus byte-identity.** CENSUS uses this:
`scripts/tierc10_census_fixtures.py:1625-1753`.
```python
def _build(root: Path, hash_seed: str) -> str:                      # :1625
    env = dict(os.environ, PYTHONHASHSEED=hash_seed, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([PY, str(ROOT/"scripts"/"tierc10_census.py"), "--assets", ",".join(DET_ASSETS),
                        "--lenses", DET_CELL[1], "--out", str(root)],
                       capture_output=True, text=True, env=env, timeout=3600, cwd=str(ROOT))
```
- `_det_findings(a, b)` (`:1635`) requires:
  - the same sorted file set;
  - identical bytes for every file;
  - for every `.parquet`, `C.content_sha(read_parquet)` equal;
  - the manifest's `sha[name]` equal to the table's content sha.
- `_clock_hits(root)` (`:1657`) uses the regex
  `CLOCK_FIELD = r'"[^"]*(elapsed|wall_clock|perf_counter|_at_run|run_started)[^"]*"\s*:'` over every `*.json`.
- `det_runs()` (`:1662`) builds three times: seed `"1"`, then `"20260921"`, then `"7"` into the first root again, which
  must print `REUSED` once per asset. That third build is the resume-honesty claim.
- `det_break()` plants, on COPIES:
  - one float moved by 1e-6;
  - a cell table edited behind its receipt, where `C.cell_is_current` must refuse;
  - an `elapsed_s` field.

**(ii) The builder re-invokes itself with `--out-dir` under `<stage>/_det_<name>/seed_{1,SEED}/`.** The CLOSE builders
use this:
- `tierc10_close_p_trg_2_seen_share.py:656-667` (`det_runs`) and `:755-767` (the leg). `DET_SEEDS = (1, SEED)` is at `:154`.
- env: `dict(os.environ, PYTHONHASHSEED=str(seed), NAIAD_CACHE_DIR=str(SNAPSHOT), PYTHONDONTWRITEBYTECODE="1")`.
- The command is `[sys.executable, __file__, "--out-dir", d]`.
- GREEN iff:
  - both exit 0;
  - the JSON+MD bytes of seed 1 equal those of seed 20260921;
  - both equal the canonical bytes this run wrote.
- Sabotage: `render_json(dict(M, salt=os.getpid()))` must differ.
- `main()` guards `--out-dir` so it must lie under `DET_ROOT` (`:780-784`).
- The `_det_*` dirs persist on disk. In TC10 they live at `research_outputs/tierc10/close/_det_<name>/`.

**(iii) Canonical root vs a `--rerun` root, the PANEL and STAMPS form.**
- `tierc10_panel_fixtures.py:3037-3121` runs `_build(False)` and `_build(True)`. Each is a subprocess of
  `tierc10_panel.py [--rerun]`. `--rerun` writes to `research_outputs/tierc10_run2/panel`.
- `TP.check_det(root_a, root_b)` (`tierc10_panel.py:2661-2689`) requires:
  - the same `manifest.sha` key set;
  - no content sha moved;
  - an independent byte re-hash of every parquet pair;
  - equal `input_sha` (otherwise "the SUBSTRATE moved").
- Break legs:
  - a 1e-6 value in a copy, with a CONTROL first: an unchanged read→write round trip must stay GREEN;
  - a manifest sha altered;
  - a table dropped.
- **This variant does NOT vary PYTHONHASHSEED.** Use (i) or (ii) when the contract says "two subprocess runs with
  PYTHONHASHSEED".

**The DET law for artifacts** (`tierc10_resume_fixtures.py:124-129`, `tierc10_census.py:374`): the transcript and every
artifact carry "no clock, no temp path, no set iteration order AND NO LIVE VALUE OUT OF A FILE THIS TRACK DOES NOT OWN".
- Wall clock goes to `clock()`, which is stdout only.
- Manifests exclude `VOLATILE_META = ("wall_clock_at_run", "cache_lag_hours")` (`tierc10_panel.py:625`).

### 3.2 F-GRID: every grid whole
- **Helper:** `TP.grid_whole(declared, written, cell_col="cell", require_cols=(), require_false=(), label="grid") -> (bool, [lines])`
  at `tierc10_panel.py:2592-2625`. It requires:
  - exact SET equality between the declared literal cell list and `written[cell_col]`;
  - no duplicate on either side, and equal length;
  - every `require_cols` column present and non-null on every row;
  - every `require_false` flag False on every row ("no promotion").
- **Usage of record:** `tierc10_census_fixtures.py:728-828` (`_grid_findings`). The declared cells are the Cartesian
  product built from FIXTURE-TYPED literals (`DECL_*` at `:103-120`) and joined with `"|"`, so the commission is a
  second object and never the module's own tuple.
- Extra F-GRID laws in that file:
  - `n == 0` ⇔ every stat is NaN AND `nan_reason` is non-empty;
  - the era split is a PARTITION: ALL counts = tuning + holdout;
  - exactly one `chosen` per scale grid, re-derived by the printed tie-break;
  - collar and as-of columns are present on every table;
  - **no VERDICT column** (`VERDICT_COLUMNS = ("verdict","clears_bh_bar","promotable","scored_in_family","p_one_sided","is_the_registered_cell")` at `:121`).
- `grid_break()` (`:840-887`) plants: a missing cell, an undeclared cell, a silent NaN, NaN under n>0, a verdict column,
  a collar removed, an as-of stamp removed, a scale grid not whole, two picks, the wrong pick, and provisional pins
  passed off as frozen.
- `_recompute_grid()` (`:890`) re-derives every grid row from the FILED ledgers with plain numpy.

### 3.3 F-KEY: totality of keys and as-of stamps
- **Build-time (HALT):**
  - `tierc2_baseline.assert_key(df, keys, label)` (`scripts/tierc2_baseline.py:191-201`) and `write_table(df, name, keys, root) -> content_sha`
    (`:170-188`): round to 6 dp, mergesort by key, atomic `.tmp` → `os.replace`.
  - The census variant is `canon()` / `write_table()` (`tierc10_census.py:415-441`), with `content_sha(df) = sha256(df.to_csv(index=False))` (`:410`).
- **Fixture:** `TP.check_keys(root, manifest=None, need_cols=AS_OF_COLUMNS) -> (bool, [4 lines])` at
  `tierc10_panel.py:2628-2658`. It requires:
  - every `*.parquet` in the root has a key in `manifest["keys"]`, and every declared key has its table ("ghosts");
  - no duplicate key rows;
  - every table carries all 9 as-of columns, non-null.
- `TP.AS_OF_COLUMNS` (`:2557`) =
  `("as_of_last_closed_4h","as_of_panel_start","as_of_span_days","warranty","as_of_lens","as_of_last_closed_bar","as_of_panel","as_of_n_assets","as_of_substrate")`.
  The first four come from `tierc8.stamp(df, meta)` (`tierc8.py:96-111`). `TP.stamp_n(df, meta, lens="4h", lens_last_closed_ms=None)`
  (`:2528-2554`) adds the lens-aware five. It HALTs if a lens edge falls after the corridor end.
  `TP.lens_edge(hi_ms, lens)` (`:2515`) uses `LENS_MS` (`:2511`) = `{"5m","1h","4h","12h","1d","1w"}`, with 1w
  Monday-anchored. **There is no `15m` key: GAP-5.**
- **Writer:** `TP.make_put(root, meta, lens="4h") -> (put, W, K, SK)` at `:2563-2589`.
  `put(df, name, key, lens_=None, lens_last_closed_ms=None, meta_=None)` stamps (unless the frame is already stamped),
  writes, and records `W[name]=sha` and `K[name]=key`. An empty frame goes to `SK` (skipped_empty).
  - The manifest must carry `{"sha": W, "keys": K, "skipped_empty": SK, "input_sha": ..., "seed": ..., "as_of": ...}`
    (`tierc10_panel.py:2912-2951`), written with `json.dumps(man, indent=2, sort_keys=True, default=str)`.
- **Fixture of record:** `tierc10_panel_fixtures.py:3123-3240` (`f_key`). Breaks on COPIES:
  - a duplicate row;
  - `as_of_last_closed_4h` dropped, and `as_of_lens` dropped;
  - an undeclared parquet;
  - a nulled stamp;
  - a 17-asset table stamped CLASSIC5/5, and all corridor rows stamped with one meta.

### 3.4 Import-closure
- **Law of record ("CAPTURED, NOT CONSULTED"):** `scripts/tierc10_stamps.py:253-261`.
  - `FORBIDDEN_IN_DECISION = ("tierc10_stamps","tierc10_census","rangefinder")`, matched on any dotted part.
  - `DECISION_MODULES = ("tierc7_rules","tierc6_rules","tierc5_rules","tierc4_rules","tierc3_rules","tierc2_rules","tierc9")`.
  - `STAMP_COLUMN_PREFIX = "rf"`.
- **Fixture:** `scripts/tierc10_stamps_fixtures.py:825-981` (F-STAMP-CLOSURE).
  - `_closure(modname, shadow_src=None) -> set[str]` (`:830`) runs `python -c` in a fresh interpreter:
    `sys.dont_write_bytecode=True`, `before=set(sys.modules)`, `import X`, then prints the sorted new modules as JSON.
    `shadow_src` writes a planted copy into a temp dir placed first on the path, so no repo file is touched.
  - `_reach(closure)` (`:854`) checks each forbidden name as a substring of any dotted part.
  - `_static_hits(src)` (`:867`) is an AST walk that includes function bodies (a lazy import is invisible to a closure).
    It also flags any string constant starting `"rf"+lens+"_"`, and the OR-1 F-BR-14 regex
    `RANGE_IMPORT_LINE = r"(?m)^[ \t]*(?:from|import)[ \t]+[^\n#]*\brangefinder\b"` (`:826`).
  - Plants (`closure_break` `:894`): a top-level range import, placed AFTER `from __future__`; a census import in a
    `*_rules` module; a lazy in-function stamp import; a stamp-column read; an indented range import.
  - The real leg (`:946`) runs the closure of `tierc7_rules` and `tierc9`, AST-scans every `DECISION_MODULES` file, and
    asserts the OTHER side of the wall: `tierc10_stamps` DOES reach the census and the port.
- **Lane variant:** `tierc10_lanes_fixtures.py:2556-2694` (F-LANES-CLOSURE). The runner's closure must reach no range or
  census module. The census is reached by ONE lazy import inside ONE named function,
  `tierc10_lanes.spring_signals_from_census`. Range EVENTS enter a lane as precomputed ARGUMENTS (`springs=[sig]`).
- **Heads-up.** The `\brangefinder\b` regex does NOT match `rangefinder_core` or `rangefinder_census`, because `_` is a
  word character. `_reach()`'s substring test does match them. Use both. `scripts/rangefinder_core.py` is OR-1's
  relocated range module (`3d55988`).

### 3.5 Worktree attestation (read-only worktrees)
- **What TC10 did:** `tierc10_panel_fixtures.py:3242-3261` `f_worktree_attest()` prints four lines and sets
  `RESULTS["F-WORKTREE-ATTEST"] = True` **unconditionally**. Its printed failure clause reads
  "FAILS IF: never — it is an attestation".
- Lineage:
  - `tierc8_fixtures.py:464-482`: the law was enacted 2026-08-17 after a review agent left the sabotage patch
    `return pd.DataFrame()` in `tierc7_lab_regime.regime_table`.
  - `tierc9_fixtures.py:735-745`.
- How reviews ran: workflow agents with `isolation: worktree` under `.claude/worktrees/wf_*`. `.claude/worktrees/` is
  excluded by `.git/info/exclude`.
- **TC10's own finding** (BUILD_DRAFT.md:1184-1187 and §5.11): the attestation is not a check.
  - All 28 registered worktrees sit at `a6da1b9` (2026-07-09) and reach 0 of the tierc10 commits.
  - "Nothing on disk records the worktree each TC10 review ran in."
  - Measurement code: `tierc10_close_close_findings.py:603-643` `m_v(root)` parses `git worktree list --porcelain` and
    computes, for each HEAD, the count of `|commits whose subject startswith TIERC10_SUBJECT_PREFIX ∩ git rev-list <head>|`.
- **Caveat:** `research_outputs/tierc6|tierc9|tierc10` are gitignored. A fresh worktree therefore lacks F-CTRL/b's
  referee journals, and that leg goes RED there (`tierc10_panel_fixtures.py:3254-3256`).

### 3.6 F-CTRL: v6 at 0.000e+00, cross-process anchored
- **F-CTRL/a, exact zero, in-process twin paths:** `tierc10_panel_fixtures.py:153-225`.
  ```python
  lo, hi, meta = TP.corridor_n(TP.CLASSIC5)
  control = TP.run_cell_n(TP.CONTROL_CARD, T9.V6_ROLES, TP.CLASSIC5, lo, hi)   # N-asset path
  want    = T6.run_cell(V6.CARD_V6, lo, hi)                                    # tierc6 path
  ok, worst, why = TP.ctrl_diff(TP.journal_frame(control), TP.journal_frame(want))
  ```
  - `TP.ctrl_diff(got, want) -> (bool, worst: float, str)` (`:2712-2724`) sorts on `(asset, entry_ms)`, requires equal
    n, EXACT zero on `CTRL_COLS` (`:2707`) and identical `exit_reason`. `CTRL_COLS` =
    `("entry_ms","exit_ms","entry_px","exit_px","stop_px","r_dist","net_r","gross_r","fee_r","funding_r","mfe_r","n_advances")`.
  - It also requires `(lo, hi) == TP.control_window()` (`:2727`).
  - Breaks: `net_r` +1e-9; one exit_reason relabelled; one campaign dropped.
  - The same check is a build-time HALT precondition in `tierc10_panel.run()` at `:2847-2858`.
- **F-CTRL/b, the cross-process anchor, prefix-robust:** `tierc10_panel_fixtures.py:229-310`, using
  `TP.ctrl_prefix(live, filed, filed_edge_open_ms, label) -> (bool, [lines])` (`tierc10_panel.py:2737-2824`).
  - The referees are the FILED journals from other processes:
    - `research_outputs/tierc6/trade_journal.parquet`, edge = `exit_ms.max()`;
    - `research_outputs/tierc9/trade_journal_control.parquet`, edge = `_iso_ms(as_of_last_closed_4h) - MS_4H`. It has
      196 rows and as_of 2026-08-22T00:00:00Z.
  - Five claims:
    1. every filed campaign is present live;
    2. entry_px, stop_px and r_dist are EXACT;
    3. closed campaigns have the same exit bar, price and reason;
    4. gross_r, fee_r and mfe_r are exact, and any net_r drift is explained by funding_r at 6 dp;
    5. every live-only campaign entered AFTER the referee's edge.
  - A missing referee is RED and never skipped.
  - Breaks: a lost campaign; BTC prices ×1.005 (the poisoned shared memo); an early extra campaign; gross +1e-6; an
    unexplained net +1e-3; an exit moved one bar.
- **Newest referee on disk for TC11:** `research_outputs/tierc10/panel/control_journal.parquet`. It has 200 rows, as_of
  2026-09-21T16:00:00Z, 53 columns including all 9 as-of stamps. Its sha256 `fcbf5db0…fae64c1c` (70,102 B) is recorded in
  PROGRESS `PANEL/gate`. Anchor on it by sha, the same way `p_trg_2` anchors `CTRL_REL`.

### 3.7 Transcript byte-reproducibility
- The first line is `as_of_last_closed_4h: <ISO>` (lanes, panel and RF: `as_of_last_closed_4h:` plus
  `as_of_record_anchor_bar_open:`). Then a `=`×78 banner, the title, then `substrate … · seed …`.
- Only `say()` lines enter the transcript. `clock()` is stdout only. Temp paths are scrubbed by `_norm()` (lanes/panel)
  or `clean()` (score).
- **Whole run vs filtered run:** a leg-substring invocation writes `FIXTURES_<X>_partial.txt` and NEVER the transcript
  of record (`tierc10_rf_fixtures.py:1199-1201`, `tierc10_lanes_fixtures.py:3650-3652`).
- **No-clobber law** (`tierc10_resume_fixtures.py:5113-5231`, `file_transcript(out, body, refile, quiet=False, of_record=True) -> list[findings]`):
  - identical bytes: silent, not rewritten;
  - different bytes, no `--refile-transcript`: write `<stem>_rerun.txt`, leave the record untouched, return a RED
    finding with `_first_diff`;
  - ABSENT and no refile: a finding, and nothing written;
  - symlink, directory or unreadable path: each a finding.
  - **Only the RESUME suite has this.** The other TC10 suites overwrite on every whole run: RF `:1201`, panel `:3292`,
    lanes `:3652`, p_trg_2 `:800`. The TEMPLATE uses no-clobber.
- **PROGRESS fixture record, the byte-reproducibility evidence.** Run the suite twice. Record `transcript_sha_before`
  and `transcript_sha_after`, set `transcript_drift = before != after`, and record `exit_code`, `legs_red`,
  `legs_total` and `wall_seconds` (may be null). The suite label reads `"… (run 1 of 2)"`.

### 3.8 The as-of prefix-stability pattern, the model for F-NEST-ASOF and F-WARN-ASOF
- `tierc10_census_fixtures.py:233-448` (F-RNG-ASOF):
  - `_law_views()` builds the honest view plus four LEAKY READERS on copies: a leaked redraw (bounds read off
    `Range.top/.bottom`, the end-of-run values), a flip read at its stamp bar, a back-dated left edge, and a naive
    `known_at = i`.
  - `_cuts()` (`:287`) draws seeded random cuts PLUS cuts AIMED at structure: one bar before and at hardens and
    confirms, inside flip-hold windows, at pivot seals.
  - `asof_corpus()` (`:327`) runs, for every cut t, the SAME reader on `tape[:t]` and on the full tape. It compares all
    `C.ASOF_ARRAYS[:t]`, the class events with `known_at <= t-1`, and both known_at-filtered logs, AND the machine's own
    end-of-prefix state `_oracle()` (`:305`, the ENGINE's on 1d).
  - `asof_break()` (`:397`): each leaky reader must be caught on EVERY tape×SCALE run, or it counts as a pass (VOID).
- The contract's "sabotage leg: a leaked redraw must FAIL" is exactly plant #1 above.

---

## 4 · PROGRESS.json, the R0 census, and quarantine

### 4.1 Schema (`research_outputs/tierc10/PROGRESS.json`, 288,648 B, tracked, HEAD blob == disk)

**Top-level keys:**

| key | example / meaning |
|---|---|
| `tier` | `"TIER-C10"` |
| `identity` | `"v2"` |
| `branch` | `"v12-v1-census"` |
| `head` | full sha at the last ledger write (stale by design; BUILD_DRAFT §5.10) |
| `seed` | `20260921` |
| `substrate` | absolute snapshot path |
| `as_of_of_record` | `"2026-09-21T16:00:00Z"` |
| `as_of_last_closed_4h_close_ms` | `1790006400000` |
| `contract_of_record` | `{path, sha256}` |
| `operator_rulings` | `{path, sha256, note}` |
| `live_cache_touched` | `false` (must be False: F-C10-RESUME-5) |
| `r0_census_utc` | |
| `last_sweep_utc` | |
| `sweep_note` | |
| `law_1_note` | |
| `f_c10_resume_law` | |
| `resume_point` | free text: what the next session does first |
| `stages` | a LIST of stage records |

**Stage record.** Required keys are `STAGE_KEYS = ("stage","status","as_of","artifact_shas","fixtures","blockers")`
(`tierc10_resume_fixtures.py:297`). Always present too: `artifact_count` and `one_line`. Optional: `notes`,
`declared_advance`, `artifact_note`.

| field | type / law |
|---|---|
| `stage` | unique name; TC10 names were `STEP 0`, `D-CORE`, `CENSUS-R{4h,1d}`, `NULL/gaps-only`, `NULL/gaps+order`, `A (stamps)`, `PANEL/gate`, `LANES (B mech)`, `BRK (B mech)`, `F-C10-RESUME`, `D-5M`, `CENSUS-R{5m}`, `B-REG (the six filed)`, `B-CORE`, `B-5M`, `CLOSE` |
| `status` | one of `LEGAL_STATUS = ("COMPLETE-VERIFIED","PARTIAL","ABSENT")` (`:296`) |
| `as_of` | the corridor ISO, identical on every stage (F-C10-RESUME-3) |
| `artifact_shas` | dict `{repo-rel path: {"bytes": int>0, "sha256": 64 lowercase hex}}`; the stage dir = commonpath of its parents |
| `artifact_count` | must equal `len(artifact_shas)` |
| `fixtures` | list of records, keys `FIXTURE_KEYS = ("suite","exit_code","legs_red","legs_total","transcript_drift","transcript_sha_before","transcript_sha_after","wall_seconds")` (`:298-300`), plus optional `note`, `re_run_utc` |
| `blockers` | list of strings; **COMPLETE-VERIFIED ⇒ zero blockers, ≥1 fixture record, every exit 0, every legs_red 0** |
| `one_line` | the stage's one-line summary (the draft line LAW 6 asks for) |

- `F-C10-RESUME` records NO artifact sha of its own transcript: "the self-reference does not converge" (`2e92972`).
- F-C10-RESUME-0's "admissions" (anchored, withdrawal-only; `ADMISSION_FIELDS` at `:1132`): `transcript_drift` and the
  two shas, `exit_code`, `legs_red`, `red_leg_names`, `wall_seconds`, blockers by COUNT, and PARTIAL→ABSENT.
- **A known limit:** HEAD records are matched BY INDEX, so inserting or re-ordering fixture records goes FALSE RED. For
  TC11, **append** fixture records and never insert. TC10 filed a per-record id as a cross-track request.

### 4.2 R0 census procedure
- The TC10 RESUME contract lines 26-33 define it. It is read-only and writes only PROGRESS.json.
- It covers:
  - identity v2, branch, HEAD;
  - `git log --since=<start>` of commits touching the tier, rangefinder and data;
  - `git status` with uncommitted files listed;
  - an inventory against the contract per stage: artifacts, bars, first/last ts, shas, gaps, computed rows, fixtures.
- It PRINTS THE STAGE LEDGER (COMPLETE-VERIFIED / PARTIAL / ABSENT) and resumes at the first non-complete stage in a
  declared ORDER.
- How TC10 actually ran it (`f97cded`; BUILD_DRAFT §R0):
  - ten agents RE-RAN every fixture suite (LAW 1: "COMPLETE only if artifacts exist, manifest shas verify, and its
    fixtures RE-PASS now");
  - they re-hashed 1,035 artifact shas independently;
  - they found that everything was UNTRACKED, and committed the whole tree first (`d19f857`, "LAW 6 was breached").
- The stage's `blockers` hold the reasons a stage is PARTIAL.
- After ANY PROGRESS edit (memory note), run `tierc10_resume_fixtures.py`, then `--refile-transcript`, then commit
  `FIXTURES_RESUME.txt`.

### 4.3 Quarantine (LAW 2, never delete)
- `research_outputs/tierc10/_partial_20260922T0955Z/` holds `README.md`, `lanes/FIXTURES_LANES_partial.txt` (4,692 B)
  and `panel/FIXTURES_PANEL_partial.txt` (6,552 B). All three are tracked.
- The README table has columns `file | bytes | what it actually is`, plus a section "DISCLOSED, NOT QUARANTINED" for
  things left in place, with the reason.
- The shas are typed as literals in `QUARANTINED_PARTIALS` (`tierc10_resume_fixtures.py:304-309`) and checked three
  ways: the literal, the disk, and the PROGRESS record.
- The tampered-partial break: one byte appended to a copy must FAIL (F-C10-RESUME-2 `:3069`).
- The directory name format is `_partial_<YYYYMMDD>T<HHMM>Z`.

### 4.4 The F-C10-RESUME machinery, and what a TC11 twin would need
- Its literals are all TC10-specific (`:185-186`, `:193-341`, `:371`):
  - `PINNED_LEDGER_REV="2e92972"` and `PINNED_LEDGER_SHA`;
  - `TC_ROOT_ALLOWLIST`, `TC_SUITE_FILES` (every `scripts/tierc10_*.py` must be listed AND tracked, or leg 4 goes RED);
  - `SEED`, `AS_OF`, `CLOSE_MS`, `QUARANTINED_PARTIALS`, `STEP0_*`, `EXEMPTIONS`.
- The pin order TC10 used:
  1. commit the ledger (`2e92972`);
  2. pin its rev and sha in the fixture module (`41a5070`);
  3. commit the transcript of record (`83f5e29`).
- The anchor exists because PROGRESS.json and FIXTURES_RESUME.txt are TRACKED (force-added).

---

## 5 · Git conventions

### 5.1 .gitignore and force-add
- `research_outputs/tierc10/**` sits at `.gitignore:263` and `tierc10_run2/**` at `:264`, APPENDED at the bottom.
- `.gitignore:267-270` says new rules are appended and never inserted "so every line number above keeps the value other
  lanes cite (TIER-C10's records cite `.gitignore:263`)".
- `!research_outputs/**/build_manifest.json` at `:44` does NOT rescue files under tierc10. The later `**` rule wins:
  `git check-ignore` reports `.gitignore:263` for `tierc10/panel/build_manifest.json`.
- Tracked (59 files, via `git add -f`):
  - the root docs `BUILD_DRAFT.md`, `FIXTURES_RESUME.txt`, `LEDGER_5M.json`, `LEDGER_APOLLO_APPEND.md`,
    `OPERATOR_RULINGS.md`, `PROGRESS.json`, `REGISTRATION_PLAN.md`, `REGISTRATION_TEXTS.json`, `REGISTRY_PIN.json`;
  - the `_partial_*` quarantine;
  - `close/*.md|json|txt`;
  - `scores/*.txt|json`.
  - NO parquet, and NOT the stage transcripts `panel/`, `lanes/` or `census/FIXTURES_*.txt`.
- **`research_outputs/tierc11/**` has no rule** (checked with `git check-ignore -v --no-index`).
- `research_outputs/tierc6|tierc9/**` are ignored (`:234-244`), so the F-CTRL referees exist on this disk only.
- Hazard: the untracked-but-unignored bulk incident of 2026-08-05 (`.gitignore:119-130`).

### 5.2 Commit messages
- Subject: `tierc10(<SCOPE>): <sentence>`. Scopes seen: `F-C10-RESUME` ×13, `LAW 6`, `LAW 2`, `R0`, `STAGE B`,
  `STAGE B mech`, `B-CORE`, `B-5M`, `CENSUS-R`, `BRK`, `CLOSE`, `CLOSE prep`, `round 2`, `STEP Q + rulings recovery`,
  and a bare `tierc10:` ×3. TC11's first commit already follows it:
  `tierc11(STEP Q): contract filed verbatim — <path> sha256 <64hex>`.
- The prefix is machine-read: `TIERC10_SUBJECT_PREFIX = "tierc10"` (`tierc10_close_close_findings.py:139`) selects
  "the build's commits". **TC11 subjects must start `tierc11`.**
- Body: plain prose with the stage's results and numbers (verdicts, CI, p, counts, shas), what was repaired, and what
  was NOT done. Examples: `371123f`, `08a6fce`, `d575a7d`, `f97cded`, `590989d`.
- Trailer: `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>`. Earlier commits carry "Opus 5".
- Rhythm: each stage commit is followed seconds later by
  `tierc10(F-C10-RESUME): transcript of record after <stage> — 9 GREEN, 0 RED`.
- Stage only this tier's paths. A parallel lane (OR-1, OR-2, Oracle) edits the same tree. The working tree has
  `M research_outputs/tierc10/close/FIXTURES_CLOSE_ledger_append_root.txt`: that file reads live git state by design
  and moves with every commit.

---

## 6 · How to call this from a new tierc11 script

```python
# BEFORE python starts:  export NAIAD_CACHE_DIR=<snapshot> PYTHONDONTWRITEBYTECODE=1
import os, sys; from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
# 1 · substrate guard FIRST (copy guard_substrate from the TEMPLATE, §8)
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
import tierc10_panel as TP        # snapshot-agnostic; CLAMPS corridors to TC10's pin (GAP-1)
import tierc9 as T9, tierc6 as T6, tierc6_rules as V6
# importing tierc10_census / _stamps / _lanes / _brk / _score / _null / _data HALTs off tc10_20260921

# F-CTRL/a
lo, hi, meta = TP.corridor_n(TP.CLASSIC5)
got  = TP.journal_frame(TP.run_cell_n(TP.CONTROL_CARD, T9.V6_ROLES, TP.CLASSIC5, lo, hi))
want = TP.journal_frame(T6.run_cell(V6.CARD_V6, lo, hi))
ok, worst, why = TP.ctrl_diff(got, want)                     # want worst == 0.0
# F-CTRL/b — cross-process anchor on the FILED TC10 control journal (sha-check it first)
import pandas as pd
filed = pd.read_parquet(ROOT / "research_outputs/tierc10/panel/control_journal.parquet")
edge  = TP._iso_ms(str(filed["as_of_last_closed_4h"].iloc[0])) - TP.MS_4H
ok_b, lines = TP.ctrl_prefix(got, filed, edge, "FILED tierc10/panel/control_journal")

# writing a stage's tables (F-KEY-ready) + manifest
out = ROOT / "research_outputs/tierc11/<stage>"
put, W, K, SK = TP.make_put(out, meta, lens="4h")
put(df, "nest_vector", ["asset", "campaign_id", "instant", "lens"], lens_="4h")
# ... json.dumps({"seed": 20260924, "as_of": ..., "sha": W, "keys": K, "skipped_empty": SK,
#                 "input_sha": TP.input_sha(TP.CLASSIC5)}, indent=2, sort_keys=True, default=str)

# fixtures
ok, lines = TP.check_keys(out)                                # F-KEY
ok, lines = TP.grid_whole(declared_cells, table.assign(cell=...), "cell",
                          require_cols=("n", "nan_reason"), require_false=("promotable",))  # F-GRID
ok, lines = TP.check_det(out, out_rerun)                      # F-DET (roots) — add PYTHONHASHSEED twins per §3.1(ii)
```

---

## 7 · Gaps: what the existing code CANNOT do today

- **GAP-1 · One corridor at "latest closed 4h bar".** The header reads *"Corridor: full water, latest closed 4h bar, one as-of pin."*
  - The only snapshot is `tc10_20260921`, pinned at `2026-09-21T16:00:00Z`.
  - Seven TC10 modules HALT at import on any other `NAIAD_CACHE_DIR`: `tierc10_census.py:96`, `tierc10_data.py:117`,
    and through them stamps, null, lanes, brk and score.
  - `TP.corridor_n` and `TP.control_window` clamp to TC10's `AS_OF_PIN.json` and forbid a forward pin.
  - To advance, TC11 needs a new frozen snapshot, its own AS_OF_PIN, and either a parameterised substrate guard or TC11
    modules that do not import those seven. It must also never write the live cache (`~/.cache/naiad/data_cache`, owned
    by a live lane).
  - Otherwise TC11 stays on TC10's corridor, which contradicts "latest closed 4h bar".
- **GAP-2 · No TC11 ledger or resume fixture.** No `research_outputs/tierc11/PROGRESS.json`, no `tierc11_resume_fixtures.py`.
  F-C10-RESUME is hard-wired to tierc10: the literals, the `tierc10_*.py` glob, and the 2026-09-21 corridor.
- **GAP-3 · tierc11 is not gitignored** (§5.1). TC11 parquet bulk will show as untracked, and a stray `git add -A`
  sweeps it.
- **GAP-4 · The import-closure law is inverted for TC11.**
  - TC10's closure law forbids the decision path from reaching `rangefinder` or the census/stamps.
  - TC11's lanes are range-CONSULTING by design: nest, breakout, scalp, adds, TP.
  - The existing fixtures can only certify that (a) the v6 control path stays clean, and (b) range code enters a lane
    through one lazy import in one named harness function, or as precomputed event arguments.
  - A TC11 closure fixture must name its new FORBIDDEN / DECISION sets. Nothing today defines them.
- **GAP-5 · The lens vocabulary is short.**
  - `TP.LENS_MS` has no `15m`, so `stamp_n`/`lens_edge` HALT on "unknown lens" for R1's 15m.
  - `tierc10_census.LENS_MS` (`tierc10_census.py:118`) = {"5m","4h","1d"} only, and `tierc10_stamps.LENS_MS = dict(C.LENS_MS)` (`tierc10_stamps.py:118`). The nest vector's
    {1h, 12h, 1w} stamps have no stamping code.
  - The snapshot does hold 15m (20 files), 1h (23), 12h (21) and 1w (17) klines.
- **GAP-6 · Family and registry roots.**
  - `TP.FAMILY_M = 6` and `TP.REG_DIR = research_outputs/tierc10/registrations`.
  - `register()`, `score()` and `finish_family()` accept `family_m=` and `root=`, but `TP.OUT` is hard-coded to
    `research_outputs/tierc10` (`:96`).
  - TC11 must pass `root=` and `family_m=9` everywhere, or it will append to TC10's hash-chained REGISTRY.
- **GAP-7 · Worktree attestation is not a check.** No code records which worktree or HEAD each review ran in. TC10's
  review worktrees (28, at `a6da1b9`) cannot reach any tierc10 or tierc11 commit, and F-CTRL/b is RED in a fresh
  worktree because its referees are gitignored.
- **GAP-8 · No-clobber exists only in the RESUME suite.** Every other TC10 suite overwrites its transcript on a whole
  run, so "transcript byte-reproducibility" is evidenced only by PROGRESS's before/after shas.

## 8 · TEMPLATE: `scripts/tierc11_<stage>_fixtures.py`, dialect (A)

Smoke-tested in a scratchpad copy (`--root=<scratch>`):
- the first run with no transcript gives exit 1 (ABSENT finding, nothing written);
- `--refile-transcript` gives exit 0;
- the rerun is byte-identical (no `_rerun.txt`), exit 0;
- a filtered run writes `_partial.txt`;
- a live-cache env gives a HALT with exit 1;
- F-DET subprocess twins under PYTHONHASHSEED 1 and 20260924 are byte-identical.

The executor replaces `tape`, `feature`, `emit` and `FIXTURES` with the module under trial, and sets `SNAPSHOT`,
`OUT`, `TRANSCRIPT` and `AS_OF_LINE`.

```python
#!/usr/bin/env python
"""TIER-C11 · STAGE <X> — F-<ID> · F-DET.  The fixtures of <what is on trial>.

TWO LEGS PER FIXTURE, the BREAK leg first, and it must go RED or the fixture
is VOID — a guard nobody has seen fail is a guard nobody has seen [the prove()
law of scripts/tierc10_rf_fixtures.py / tierc10_resume_fixtures.py].  Every
plant is made on a COPY (an array, a frame, a temp dir); no real artifact moves.
  F-ASOF-DEMO  FAILS IF the feature at bar t-1 computed on tape[:t] differs from
               the full run's value at t-1 on any seeded cut.  SABOTAGE: a
               centred (look-ahead) window must go RED.
  F-DET        FAILS IF two subprocess emissions (PYTHONHASHSEED 1, 20260924)
               differ by one byte from each other or from this run's bytes.
BANNED: self-comparison; one example where cardinality was possible; a tuned
magnitude bound standing in for an identity; a check whose claim is not the
design's claim.  FROZEN SUBSTRATE: HALTs unless NAIAD_CACHE_DIR is the snapshot
of record.  Seed 20260924.  The transcript carries no clock and no temp path.

Run:  export NAIAD_CACHE_DIR=<snapshot of record> PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_<stage>_fixtures.py \\
          [leg-substring ...] [--refile-transcript] [--root=DIR] [--emit-to=DIR]
Exit 0 = every leg GREEN, every break RED · 1 = a RED or VOID fixture, a transcript
finding, or a HALT (SystemExit carries the reason).
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE_CACHE = Path.home() / ".cache" / "naiad" / "data_cache"
# EXECUTOR: re-point at TC11's snapshot of record once the one as-of pin exists.
SNAPSHOT = Path.home() / ".cache" / "naiad" / "snapshots" / "tc10_20260921"


def guard_substrate(env: str | None) -> Path:
    """HALTS IF NAIAD_CACHE_DIR is unset, names the live cache (path string
    first, then resolved), or is not the snapshot of record.  Runs BEFORE any
    engine import: tierc2_baseline binds KLINES at import time."""
    if not env:
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR is unset — read ONLY {SNAPSHOT}")
    norm = Path(os.path.normpath(os.path.expanduser(env)))
    if norm == LIVE_CACHE or LIVE_CACHE in norm.parents or \
            norm.resolve() == LIVE_CACHE.resolve():
        raise SystemExit("HALT: NAIAD_CACHE_DIR names the LIVE cache — READ-NEVER, WRITE-NEVER")
    if norm.resolve() != SNAPSHOT.resolve():
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR={norm} is not the snapshot {SNAPSHOT}")
    return norm.resolve()


guard_substrate(os.environ.get("NAIAD_CACHE_DIR"))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np                                                   # noqa: E402

SEED = 20260924
DET_SEEDS = (1, SEED)
OUT = ROOT / "research_outputs" / "tierc11" / "<stage>"
RUN_ROOT = OUT                              # --root=DIR redirects transcript + F-DET twins
TRANSCRIPT = "FIXTURES_<STAGE>.txt"
ARTIFACT = "DEMO_TABLE.json"
AS_OF_LINE = "as_of_last_closed_4h: <ISO of the one as-of pin>"
LINES: list[str] = []
PASSED: list[str] = []
FAILED: list[str] = []


def say(line: str = "") -> None:            # deterministic -> transcript
    print(line)
    LINES.append(line)


def clock(line: str) -> None:               # wall clock, temp paths -> stdout ONLY
    print(f"  [clock · stdout only] {line}")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def prove(fid: str, title: str, fails_if: str, break_leg, real_leg) -> None:
    """Break first; it must go RED (ok False) or the fixture is VOID."""
    say(f"\n{fid} — {title}")
    say(f"  FAILS IF: {fails_if}")
    try:
        b_ok, b_why = break_leg()
    except Exception as e:                  # a break leg that errors proved nothing
        b_ok, b_why = True, f"break leg RAISED {type(e).__name__}: {e}"
    say(f"  [BREAK] deliberate violation -> "
        f"{'RED (correct)' if not b_ok else 'GREEN (FIXTURE IS VOID)'}: {b_why}")
    try:
        r_ok, r_why = real_leg()
    except Exception as e:                  # a real leg that errors is a FAIL
        r_ok, r_why = False, f"raised {type(e).__name__}: {e}"
    say(f"  [{'PASS' if r_ok else 'FAIL'}] {fid}: {r_why}")
    if b_ok:
        FAILED.append(f"{fid} (break leg did not go RED — fixture proves nothing)")
    elif not r_ok:
        FAILED.append(fid)
    else:
        PASSED.append(fid)


# ═══════════════════════════════ the thing on trial (replace with the module)
def tape(n: int = 600) -> np.ndarray:
    return 100.0 + np.cumsum(np.random.default_rng(SEED).normal(0, 1, n))


def feature(c: np.ndarray, w: int = 20, centred: bool = False) -> np.ndarray:
    out = np.full(len(c), np.nan)
    for t in range(len(c)):
        lo, hi = (t - w // 2, t + w // 2 + 1) if centred else (t - w + 1, t + 1)
        if lo >= 0 and hi <= len(c):
            out[t] = c[lo:hi].max()
    return out


def emit() -> bytes:                        # the stage artifact, canonical bytes
    f = feature(tape())
    rows = [{"i": i, "v": round(float(v), 6)} for i, v in enumerate(f) if np.isfinite(v)]
    return (json.dumps({"seed": SEED, "rows": rows}, sort_keys=True, indent=1) + "\n").encode()


# ═══════════════════════════════════════════════════════════════ the legs
def asof_findings(centred: bool) -> tuple[list[str], int]:
    c = tape()
    full = feature(c, centred=centred)
    cuts = sorted(set(np.random.default_rng(SEED).integers(40, len(c), 50).tolist()))
    return [f"cut {t}: prefix {feature(c[:t], centred=centred)[t - 1]!r} vs full {full[t - 1]!r}"
            for t in cuts
            if not np.array_equal(feature(c[:t], centred=centred)[t - 1:t], full[t - 1:t],
                                  equal_nan=True)], len(cuts)


def asof_break():
    bad, n = asof_findings(centred=True)
    return (not bad), (f"{len(bad)}/{n} cut(s) caught, e.g. {bad[0]}" if bad else f"0/{n} caught")


def asof_real():
    bad, n = asof_findings(centred=False)
    return (not bad), (f"{n} seeded cuts, prefix == full at t-1 on every one"
                       if not bad else f"{len(bad)}/{n} leak(s): {bad[:2]}")


def det_runs() -> dict:
    outs = {}
    for s in DET_SEEDS:
        d = RUN_ROOT / "_det_<stage>" / f"seed_{s}"
        env = dict(os.environ, PYTHONHASHSEED=str(s), PYTHONDONTWRITEBYTECODE="1")
        r = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()),
                            f"--emit-to={d}"], env=env, capture_output=True, text=True, cwd=ROOT)
        p = d / ARTIFACT
        outs[s] = (r.returncode, p.read_bytes() if p.exists() else b"")
    return outs


def det_break():
    salted = emit().replace(b'"seed"', f'"pid_{os.getpid()}"'.encode())
    return salted == emit(), f"a process-dependent salt byte-identical: {salted == emit()}"


def det_real():
    o = det_runs()
    a, b = o[DET_SEEDS[0]], o[DET_SEEDS[1]]
    ok = a[0] == 0 == b[0] and a[1] == b[1] == emit() and bool(a[1])
    return ok, (f"exit {a[0]}/{b[0]}; sha {sha_bytes(a[1])[:16]}… == {sha_bytes(b[1])[:16]}… "
                f"== this run: {a[1] == b[1] == emit()}")


FIXTURES = (
    ("F-ASOF-DEMO", "causal: a value at bar t uses only bars <= t",
     "on any seeded cut t, feature(tape[:t])[t-1] != feature(tape)[t-1]", asof_break, asof_real),
    ("F-DET", "two subprocess emissions under different hash seeds, one set of bytes",
     "the PYTHONHASHSEED 1 and 20260924 emissions differ from each other or from this "
     "run's bytes, or either exits nonzero", det_break, det_real),
)


def file_transcript(out: Path, body: bytes, refile: bool) -> list[str]:
    """NEVER CLOBBER the transcript of record [tierc10_resume_fixtures.file_transcript]."""
    if not out.exists() and not refile:
        return [f"{out.name} ABSENT — nothing written; re-file with --refile-transcript"]
    if out.exists() and out.read_bytes() == body:
        return []
    if out.exists() and not refile:
        (rr := out.with_name(out.stem + "_rerun.txt")).write_bytes(body)
        return [f"{out.name} NOT byte-identical; this run -> {rr.name}; record untouched"]
    out.write_bytes(body)
    return []


def main() -> int:
    args = sys.argv[1:]
    emit_to = next((a.split("=", 1)[1] for a in args if a.startswith("--emit-to=")), None)
    if emit_to:                              # F-DET's twin: emission only, no legs
        Path(emit_to).mkdir(parents=True, exist_ok=True)
        (Path(emit_to) / ARTIFACT).write_bytes(emit())
        return 0
    global RUN_ROOT
    root = RUN_ROOT = Path(next((a.split("=", 1)[1] for a in args if a.startswith("--root=")), OUT))
    pick = [a.lower() for a in args if not a.startswith("--")]
    say(AS_OF_LINE)
    say("=" * 78)
    say("TIER-C11 <STAGE> FIXTURES — break leg first, RED or void")
    say("=" * 78)
    say(f"seed {SEED} · substrate {SNAPSHOT.name}")
    for fid, title, fails_if, b, r in FIXTURES:
        if not pick or any(q in fid.lower() for q in pick):
            prove(fid, title, fails_if, b, r)
    say(f"\n  {len(PASSED)} GREEN, {len(FAILED)} RED")
    for f in FAILED:
        say(f"    RED: {f}")
    root.mkdir(parents=True, exist_ok=True)
    body = ("\n".join(LINES) + "\n").encode("utf-8")
    name = TRANSCRIPT if not pick else TRANSCRIPT.replace(".txt", "_partial.txt")
    bad = file_transcript(root / name, body, "--refile-transcript" in args or bool(pick))
    for x in bad:
        clock(x)
    if FAILED:
        print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
    return 1 if (FAILED or bad) else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

For several plants per guard, return `plants([(name, lambda: findings_list), ...])` from `break_leg`. Copy the hardened
`plants()` from `tierc10_resume_fixtures.py:946-974`, where a crash is a defect and never a catch.

---

## 9 · Ambiguities: contract phrases quoted

1. **"resume law (R0 census; …)".** TC10's RESUME contract fixed a resume ORDER ("core first, heaviest last"). TC11
   names stages Q, R, W, G, T, S, A, H and CLOSE but gives no R0 resume order and no PROGRESS stage names.
   - Stage letters collide with TC10's: TC10 "A" was TAPE + STAMPS, TC11 "A" is ADDS.
   - "R1..R5" collides with operator rulings R1..R10. `[R1]` is the era cut in `tierc10_panel.py:746`.
   - Stage names must be unique inside ONE ledger. If TC11 keeps its own ledger, that is fine, but the names should be
     unambiguous (e.g. `A (adds)`, `R1 (lenses)`).
2. **"F-CTRL v6 0.000e+00 cross-process-anchored".** The anchor is not named. Candidates: the FILED
   `tierc10/panel/control_journal.parquet` (as_of 2026-09-21T16:00Z, sha in PROGRESS), `tierc9/trade_journal_control.parquet`,
   or both, as TC10 used tierc6 + tierc9.
   - It is also unclear whether "0.000e+00" means F-CTRL/a's in-process exact zero or also cross-process. TC10's
     F-CTRL/b does NOT assert net_r cross-process, only funding-attributed drift.
3. **"import-closure".** No forbidden set is given, and TC11 decisions consult ranges (GAP-4). The TC10 RESUME contract
   said "import-closure extended to analytics/rangefinder.py", a file that never existed (the port is
   `analytics/rangefinder_census.py`; BUILD_DRAFT.md:1181-1183).
4. **"worktree attestation".** Is it an attestation (TC10: unconditional True, "FAILS IF: never") or a check? The TC11
   law line says "every fixture leg states its failure condition". Read strictly, that makes a leg that can never fail
   non-compliant.
5. **"F-DET".** Which variant (§3.1)? The brief says "two subprocess runs with PYTHONHASHSEED". Variant (iii), used by
   panel and stamps, does not vary the hash seed.
6. **"verify-or-quarantine".** Is there anything to quarantine at TC11 start?
   - `research_outputs/tierc11/` holds only `scout/`.
   - TC10's `census/smoke/` and `null/smoke/` are still "disclosed, not quarantined" (BUILD_DRAFT §5.12). Moving them
     is TC10's CLOSE business, and any move turns F-C10-RESUME's sweep red.
7. **"one corridor"** together with "latest closed 4h bar": see GAP-1. A second tension: "frozen base and frozen 9/12
   re-ridden on new bars only at every refresh" (FORWARD LEDGER) implies the corridor ADVANCES at refresh, but LAW 4
   holds one as-of pin per build.
8. **"PROGRESS.json per stage".** Is it a new `research_outputs/tierc11/PROGRESS.json`, or appended stages in TC10's?
   Appending to TC10's is legal for F-C10-RESUME (born stages are "a build advancing", silent). But TC10-RESUME-3
   demands every stage carry TC10's as_of, so a TC11 stage with a new as_of turns it RED. **Use a separate tierc11
   ledger.**
9. **"TIER-C11 builds on TIER-C10"** (brief) while TC10 CLOSE is PARTIAL and operator-blocked. Does the TC11 R0 treat
   TC10-CLOSE-PARTIAL as a blocker, or as a disclosed pre-condition?
10. **"F-DEF (both tide-age definitions computed and printed; a swapped definition must FAIL)".** TC10 held tide-age as
    an EXECUTOR READING with no pin (`tierc10_close_p_age_1_tide_youth.py`; BUILD_DRAFT §2.5, §5.14 on TC9's look-ahead
    band edges). The "TRAILING-quantile" window and quantile are not in the contract text.
