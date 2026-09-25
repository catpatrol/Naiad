# TIER-C11 · AMENDMENTS TO THE EXECUTOR READINGS

`LEANS.md` (sha256 `655e1605165e7a66c67f544e5cda421b46aa0b6fcd4cb97a6ad19654479f294f`) stays byte-frozen, because
`REGISTRATIONS.json` pins its sha. This file carries every later amendment. Each amendment is dated, gives its
reason, and names what was redone.

**Law:** an amendment may follow from a build fact (the code cannot do what a reading says) or from a verifier's
finding. It may never follow from a registered rule's outcome.

---------------------------------------------------------------------------------------------------------------
## FOUNDATION WAVE — 2026-09-25, filed before any stage runner or registered-rule statistic existed

**AM-1 · L-0.3 allow-list (env build + verifier MAJOR-1).**
- The audit hook allows reads, by absolute main-tree path, of exactly these TC10 records:
  - the six named in L-0.3 (`panel/control_journal.parquet`, `registrations/P-TRG-2.scored.json`,
    `census/TUNING_RESULT.json`, `STEP0_RECORD.json`, `stamps/control_entry_by_state.parquet`,
    `close/P_AGE_1_TIDE_YOUTH.parquet`);
  - **plus two disclosure references:** `census/height_toll_verdict.parquet` (TC10's per-era Q-R3 verdicts,
    printed beside TC11's R2 as the continuity column) and `census/outcome_grid.parquet` (TC10's R4-style grid,
    printed beside TC11's R4 at frozen 3.0 one-shot as the continuity anchor, and the source of P-BRK-4H's
    selection-hazard figures).
- `data/STAGE_D_MANIFEST.json` is read only inside tierc10_panel's import window, because it binds at import;
  it is declared as `IMPORT_TC10_READS`.
- Every other read under `research_outputs/tierc10/` HALTs.
- Redone: the env allow-list constant and its fixture (F-SUBSTRATE).

**AM-2 · L-0.3 hook limit (env build).**
- A Python audit hook sees only Python-level opens. It cannot see pyarrow's native readers and writers
  (`pq.read_table`, `pq.ParquetFile`, `pq.write_table`, `pa.memory_map`, `pyarrow.dataset`, `pyarrow.fs`),
  `pd.read_parquet(filesystem=…)`, subprocess, `os.system` or ctypes.
- **TC11 code reads and writes parquet only through pandas on a path string.** That path fires the hook, which
  was tested.
- These escapes are banned in every tierc11 module, and the ban is enforced by `E.hook_escapes` in the L-F.2
  closure scan.
- Subprocesses are allowed only for the fixture harness (F-DET, fresh-interpreter scans), whose children
  re-import the shim and so re-arm the hook.

**AM-3 · L-1.5 wording for the add books (ride verifier).**
- L-1.5's "for adds, the v6 leg is identical and Δ = the tranches' net R" cannot hold together with L-A.1's "the
  D12 funding ceiling applies once to the campaign's total funding including tranches" whenever the ceiling
  binds. On the fixture's planted case, Δ = 3.730034 while add_r = 3.515701; the difference is the funding the
  cap absorbed.
- **Reading of record: L-A.1.** The paired Δ is scored on `net_r` from `tierc7._account_chain`.
- Each add row prints add_r and the absorbed funding (funding_uncapped − funding_capped) beside Δ.
- Runners never assert Δ == add_r. F-ADD-ACCT checks Δ − add_r == the absorbed funding.

**AM-4 · Two mechanical readings made explicit (nest build; verifier ruled both valid).**
- `C.LENSES` is a tuple, so it is **rebound** to the seven lenses rather than extended in place. The three dicts
  are extended in place.
- The `calibrated_in_sample` flag is written as text per window, with two booleans beside it:
  - `in_sample_tuning`
  - `in_sample_holdout`

  A single boolean cannot say "in-sample for tuning, out-of-sample for holdout".
- Every nest, event and range-fact row carries `pick_window`, `scale_in_sample` and `stability_changed` per lens.

**AM-5 · L-W.0 disclosure (ride verifier, reading level).**
- Whether a 4h bar is walked on its 1h children is decided from all four children and the parent's H/L/C, so the
  walk-or-defer choice on a mismatch bar uses prices later in the same 4h bar.
- It touches 16 corridor bars across CLASSIC5: every asset has 2023-11-10T12:00Z (close) and 2024-10-28T20:00Z
  (low), plus the assets' first frame bars. On those bars, 1h-only events are taken at the parent's close.
- Kept as written, because v6 identity (F-WALK-IDENT at 0.000e+00) depends on the parent deciding STOP and +1R
  on those bars. Each book prints its mismatch-bar count, and a finding-not-fixed names the bars.

**AM-6 · L-R.5 stamps and sub-readings the builders disclosed (ride, nest, books).** All are printed in the
lean blocks. They are sub-readings where the frozen text is silent:
- **(s1)** On a stop bar under the walk, mfe keeps v6's adverse-first law.
- **(s2)** On a TP exit bar, mfe is capped at the fill price.
- **(s3)** For a relay stopped inside its entry bar J, the stop child is the stop unit.
- **(s4)** Twin refusals on the add books are judged before the 2-add cap.
- **Coincidence** is inclusive (≤ 0.25 × ATR_L).
- **In-range mid** is pct ∈ [25, 75] inclusive.
- **Base-rate coincidence** is `coin_top OR coin_bot` (R-BASE-COIN), with per-side twins beside it.
- **Out-of-range deviations** carry the dead range's final counts.
- **Parent-decided intrabar events** are stamped at the bar's open (`exit_stamp_ms`, `latch_stamp_ms`). The
  close stamp is the post-event twin.
- **The +1R latch has two readings**, and both are output:
  - L-W.3: the first child touching +1R;
  - L-W.5: the child order stop → latch.

  They agree on 200/200 v6 campaigns (`latch_on_stop_child` = 0).

---------------------------------------------------------------------------------------------------------------
## STAGE WAVE — 2026-09-25, filed before any stage runner existed

**AM-7 · L-1.1 the haircut twin law, generalised.**
- TC10's `haircut_twin_net_r` charges (fee + slippage) on entry_px + exit_px once. It ignores the harvest split,
  adds and funding, so it cannot price a v6 campaign that harvested or added.
- **TC11's law:** `haircut_net_r = net_r − fee_r × (slip_bps_side / taker_bps_side)`.
  - `fee_r` is the ride's own taker fee over EVERY fill (entry, harvest, final exit, add entries and exits), each
    at 5.0 bps per side of its notional, divided by r_dist.
  - `slip_bps_side` is the charter tier of the stem (A 2 / B 5 / C 10; `fee_schedule.json`).
- Slippage is a per-notional charge like the fee, so it scales the fee exactly. Funding stays in, because
  `net_r` carries it.
- A maker leg (scalper twins) carries zero slippage (L-1.2), so the maker twins apply the law to their taker legs
  only.
- Printed on every trade row beside `net_r`. It never replaces `net_r` (the veto "tiers").

---------------------------------------------------------------------------------------------------------------
## FINAL-REVIEW WAVE — 2026-09-25, filed after the five-lens worktree-attested review of 04067a0

These two amendments correct the record's wording and scope. Neither moves a registered number. Every verdict of
record was already scored (04067a0), and no reading that decides a verdict changes here.

**AM-5 ERRATUM · the mismatch-bar list (causality review MINOR-1).**
- AM-5 described the 16 L-W.0 mismatch bars as "2023-11-10T12:00Z and 2024-10-28T20:00Z on every asset, plus
  the assets' first frame bars". That description is wrong. The 16 bars are:
  - **10 shared bars:** those two instants on each of CLASSIC5.
  - **3 first-frame bars:** BTC 2019-09-08T16:00Z (3 children), ETH 2019-11-27T04:00Z (1 child),
    SOL 2020-09-14T04:00Z (1 child).
  - **3 ordinary bars** whose 4h high/low disagrees with the children: BTC 2019-09-09T00:00Z (high),
    BTC 2019-09-24T16:00Z (high and low), ETH 2019-12-11T16:00Z (high and low).
- All 6 extras fall before each asset's bar 316. Among the REGISTERED books, only ZEC 2024-10-28T20:00Z is
  ridden by a 1h-walked book (one v6 campaign), and no registered book's W1 event, add or relay falls on a
  mismatch bar.
- **Tier-E exceptions** (the W1 stamps of the other 4h books, added in TC11-FIX):
  - the 9/12 re-ride walks BTC 2023-11-10T12:00Z and ZEC 2024-10-28T20:00Z;
  - P-BRK-4H's walks BTC and SOL 2024-10-28T20:00Z;
  - one Tier-E W1 event (P-BRK-4H, SOL) is taken at the parent's close, 2024-10-29T00:00Z.
- The ride's `child_mismatch` reason column names the FIRST failing check only. BTC 2019-09-24T16:00Z and ETH
  2019-12-11T16:00Z fail on both high and low but read "high".
- Impact on any number: none.

**AM-8 · AM-2's subprocess clause, scoped to its real uses (reproducibility review MINOR-6).**
- AM-2 allowed subprocesses "only for the fixture harness". Three non-fixture uses exist. All three are
  outside any decision path and are allowed by name:
  - `scripts/tierc11_data.py`: the `cp -cpR` APFS clone of the TC10 snapshot (TC11-D `--clone`, run once,
    before the guard).
  - `scripts/tierc11_data_clock_note.py`: `git show e97ad73:…`, a read of the committed record.
  - `scripts/tierc11_worktree_attest.py`: `git worktree` / `git rev-parse` / `git status` / `git show` (the
    reviewed commit's PROGRESS record) for L-F.3. No other git subcommand is allowed.
- Any other subprocess use in a tierc11 module is a defect. The import-closure suite enforces this over every
  non-fixture tierc11 module.
