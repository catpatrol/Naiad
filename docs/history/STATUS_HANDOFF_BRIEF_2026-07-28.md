# BRIEF LANE — STATUS, HANDOFF AND LINES OF WORK
### Naiad v12 · compiled 2026-07-28 by Claude (Project reviewer, BRIEF lane, Fable-mode)
### Three audiences in one document: **Part 1** plain language for the operator · **Part 2** technical state of record for a successor BRIEF chat · **Part 3** lines of work for the ORCHESTRATOR · **Part 4** the F-AN-8 ruling · **Part 5** pending decisions

Provenance tags: `[verified]` recomputed or read first-hand · `[builder]` from a builder report with fixtures · `[ratified]` operator ruling · `[agent]` single-sourced cross-lane claim · `[open]` unresolved.

---

# PART 1 — Plain-language status for the operator

## Where the Brief actually is

The daily brief **v1.1 works and runs every day.** It computes ten assets, passes its eight fixtures, and now runs inside a job runner that stages its outputs and writes a dated summary. That is real and it is not going away.

Everything discussed in this chat since yesterday morning is a **rebuild** of that brief into what your Notion review actually does — levels, confluence, lines in the sand, if-then trades — and that rebuild is **one third done and currently halted on purpose.**

Three phases were specified. Phase 0 (housekeeping and diagnostics) is **finished and committed**. Phase I (the analytics toolbox) is **written and tested but deliberately not adopted**, because one test failed. Phase II (the confluence engine and the new report) and Phase III (the trade diary) **have not started**.

The builder stopped rather than pushing through, which is exactly what the contract told it to do.

## What the failed test found — and why it is good news

The failing test is the **regression guard**. Its job was narrow: make sure that when we move the indicator maths out of the big brief script into a clean toolbox, not a single already-published number changes. If a number moves, either the new code is wrong or something was wrong before.

It found something wrong before.

On the **1-hour** timeframe, the new toolbox reproduces the old brief's RSI **exactly** — 52.4705 for Bitcoin, 56.9922 for Ether, 50.7759 for Solana, matching to every decimal. The arithmetic is right.

On the **4-hour and 12-hour** timeframes, every single value disagrees. The bar counts explain it: the old brief computed those layers over **one bar more** than actually exists in our stored price data. Six out of six asset-timeframe pairs, all off by exactly one, all in the same direction. Widening the search does not find that bar, because it is not in the data at all.

The likely mechanism: the brief builds its 4-hour and 12-hour candles by stitching together smaller ones, and that stitching produces one extra candle for the period **currently in progress**. A 4-hour candle that opened at 04:00 is not finished until 08:00, but the stitching emits it anyway, containing whatever has traded so far.

**So every 4-hour, 12-hour and daily number the brief has ever published has included an unfinished candle.** That reaches further than it sounds: the momentum vote in the daily bias is built from 4-hour and 12-hour RSI, and the weekly momentum vote from 12-hour and daily. Those verdicts have been computed on partly-formed data.

This is the second time in two days that a fixture has caught a real defect rather than a refactor slip. It is the strongest argument yet for the discipline: we did not find this by looking, we found it because the machine was told to prove nothing changed.

## Your ruling on it, and why I agree

You said: **drop the unfinished candle — the closed-bar rule wins.** That is right, for three reasons.

First, we had already decided it. Gap fix G1 and fixture F-B17 both exist precisely to enforce closed bars; keeping the unfinished candle to make a test pass would mean writing a known defect into the permanent record to protect a number we now know is wrong.

Second, it makes the numbers **reproducible**. A value computed on an unfinished candle changes every minute. Two people running the brief ten minutes apart get different answers, and an archived number cannot be re-derived later. That destroys the whole point of the archive.

Third — and this is the part worth pausing on — it makes the **TradingView comparison** meaningful. The parity worksheet asks you to read values off **closed candles only**. If our maths kept the unfinished candle, our numbers would match your live chart mid-candle but never match a closed reading, and the parity session would produce confusing mismatches we would waste days chasing.

One honest trade-off: when you glance at a 4-hour RSI on your chart mid-candle, TradingView shows you the live value, and after this change the brief will not. The brief will show the last **finished** 4-hour reading. That is the correct choice for a written record, but it is a real difference from what your eyes see, and you should expect it.

I am adding one thing to your ruling. Rather than simply switching the test off, the rebuilt toolbox must **prove** that dropping the candle is the *only* thing that changed — by running in a "legacy mode" that reinstates the extra candle and showing it then reproduces the old numbers exactly. If it does, we know nothing else moved. If it does not, something else is wrong and we want to find out now rather than in three months.

## Everything else the builder found

**Two of my recent conclusions were wrong, and the builder corrected both.**

I said the manifest had a monitoring blind spot — reporting a clean worktree while three files were modified. Wrong on two counts: the field comes from `daily_routine.py`, not the manifest script, its scope really is the whole tracked tree, and it was accurate when written because the files were modified *afterwards*. Nothing to fix.

I said the "no Google Drive" finding was a probe artifact caused by a known quirk in the Windows bash layer. Also wrong. The builder checked from five different contexts and all five see the drive fine. The real cause is a timestamp: **Drive for Desktop was installed at 19:59:11**, after the earlier check ran. The earlier check tested four independent things from two different shells and was correct at the time. My explanation was plausible and false, and I had already written it into the contract's permanent ledger text as fact — which the builder caught and refused to record. That is the correct instinct and I want it on the record.

**The archive audit found something worse than what we were looking for.** The rule you adopted produced a document mapping 114 places in the code that read archived data. Two findings came out of it. `research_outputs/dryrun/` is read by two files, exists nowhere on disk, and is in **none** of the six archives — it was never archived, it is simply gone. One test skips silently around it; one script would fail outright. And the reason the earlier archiving looked safe is that the archived folders **still exist as thin shells** — `s1/` holds 5 of its 1,563 files, `tc1/` holds 3 of 5,274 — so a naive check reports them as present. That is exactly the illusion that cost us two retrievals.

**Two smaller settlements.** The Tier-2 market data feed is fine — a real, successful fetch with open interest 103,793.9 and basis −4.1 bps; the "all fetches failed" message came from the test that deliberately fakes failure. And the hazard the engine lane warned about — code that is safe only because of how it is called — **does not exist in the extracted toolbox**: 23 tests across 21 functions found no violation. That is a clean result, though it only clears the toolbox, not the brief code being rebuilt next.

**Something on your Google Drive that nobody in this lane put there:** a folder called `naiad (local folder) BACKUP`, 1,028 files, 1.66 GB, created minutes after the estate archive. Worth knowing whose it is.

## What happens next

The builder needs one short instruction to unhalt: your ruling plus the proof requirement. Then Phase I finishes, Phase II builds the confluence engine and the new report, Phase III adds the trade diary.

After that, one task needs your eyes and nobody else's: **28 readings off your TradingView charts** to certify the numbers. Until that happens the toolbox is plumbing that works, not numbers that are trusted.

Then roughly a week of living with the report, and we re-set every threshold using what actually happened rather than what I guessed.

---

# PART 2 — Technical state of record (handoff for a successor BRIEF chat)

## 2.1 What this lane is

The BRIEF lane owns the daily market brief: specification, contracts, independent acceptance, and falsification on record. It does not execute (the local builder does) and does not decide (the operator does).

**Purpose, four objectives in order** `[ratified 2026-07-27]`:
1. **Serve the trade** — reproduce the grammar of the operator's manual Notion review: every layer produces levels → levels earn authority through multi-tool confluence → output collapses to two lines-in-the-sand per asset plus if-then hypotheses. Analysis is never an end in itself.
2. **Build a compounding record** — identical printed rules every day make captures comparable across months; each capture embeds the rule set and version that produced it, so an old number still explains itself.
3. **Feed Naiad through the correct door only** — the archive is a hypothesis mine and the proving ground for shared measurement tools. It is never evidence.
4. **Force tacit skill into explicit rules** — the same mechanism by which Secret Sauce became a Pine script and then a replay engine.

**Firewall, four clauses, reprinted in every artifact** `[ratified]`: live data is ops-only and forbidden as study evidence · no journal reads, no signal- or trade-outcome statistics on any window · engine modules imported read-only with trading disabled and never modified · the archive may be mined for hypotheses but is never a scoring window.

**Governing tension:** the confluence engine is the sharpest edge, because a high-scoring area *feels* like a discovery when it is only a statement that tools agree. Whether agreement predicts anything is a study question, answerable only on exploration-classic data under G-7.

## 2.2 Chronology of this chat

| When | What |
|---|---|
| 2026-07-27 | Daily Brief v1.1 built by the builder: 8/8 fixtures, commit `76cc314`; hygiene `60e00c9b`. Two builder halts ruled and ratified (POST_X precedence; fixture fencing under charter §10). |
| 2026-07-27 | Reviewer acceptance on `brief_2026-07-27.json`: 15 independent checks pass, 12 gaps registered. Reviewer-edition HTML delivered. |
| 2026-07-27 | Lane re-scoped by the operator to continuous improvement of the automated brief, anchored to the Notion template's grammar. Interview D-B9..D-B16 ruled. |
| 2026-07-27 | Contract v2 after the operator supplied TradingView's Rolling-VWAP Pine source — a material correction to the σ-band specification. Interview D-B17..D-B26 ruled. |
| 2026-07-27 | Contract v3 issued as a go-paste. Census handoff delivered. **Never executed.** |
| 2026-07-28 | ENGINE lane replied to the census handoff: LIT escalation upheld with corrected diagnosis; four reviewer errors accepted. Amendment 1 issued. **Never executed.** |
| 2026-07-28 | Builder reports arrived for unrelated work (venv migration, daily routine, fixture restore). Housekeeping paste halted correctly on a reviewer gate-design flaw. Groups A–D ruled. |
| 2026-07-28 | **Contract v4** consolidated and issued — hash-verified, executed to Phase I, halted on F-AN-8. |

## 2.3 Build state as of this document

| Item | State |
|---|---|
| Branch / HEAD at last gate | `v12-v1-census` / `837c635`, plus Phase 0 commits `49e2f87`, `629930e` `[builder]` |
| Contract of record | `prompts/CONTRACT_v4_ANALYTICS1_BRIEF2_FORWARD0.md` — 39,857 B, sha256 `edc5b8e103afa458f368cccbd48f76f765b8b81d281f3f314fd0c86dbd5f23ea`, LF-only, hash re-verified after move `[verified]` |
| Phase 0 | **COMPLETE, COMMITTED** — diagnostics, repo-root filing (3 files hash-verified), archive-dependency audit |
| Phase I | **BUILT, TESTED, NOT ADOPTED, NOT COMMITTED** — `analytics/` 9 modules, `tests/test_analytics.py`, F-AN-1..14 with F-AN-8 failing |
| Phase I remainder | Not started: `scripts/parity_worksheet.py`, the worksheet, `ANALYTICS1_REPORT.json` |
| Phase II | Not started |
| Phase III | Not started |
| Pushed | Nothing. Engine files, configs, `LIT_FLOOR_MS` and the data cache untouched. |

**Fixture results** `[builder]`: F-AN-1,2,3,4,5,6,7,9,10,11,12,**13**,14 all PASS. F-AN-8 FAIL, 12 of 21 comparisons mismatch. Full repo suite 73 passed / 1 skipped, no regression from `analytics/`.

**F-AN-13 detail** — 23 tests, 21 series functions × truncation points k ∈ {40, 60, 120, 200, 299}, plus endpoint-only and lag cases. `pivots` satisfies the lag form; `percentile_rank` raises on a mid-array `as_of_index`. **Scope caveat:** this clears the extracted toolbox only. The one-sided-window hazard reported by ENGINE could still live in `daily_brief.py`'s orchestration layer — the code Phase II rewrites. Phase II needs its own causality discipline before the class can be called closed.

**Three build defects found and fixed by the builder during Phase I** `[builder]`: F-AN-4 tripped on its own docstring (fixed by tokenising rather than raw-text scanning); ATR warm-up is `length−1` not `length`, because `true_range` defines index 0 as H−L (the test expectation was wrong, `CONVENTIONS` was right); F-AN-14 failed by 1 ULP from numpy pairwise summation versus pandas `groupby`, resolved by adopting the pandas reduction rather than negotiating a tolerance — correctly refusing to lower a byte-identity bar this project applies everywhere else.

## 2.4 Ratified decisions

**D-B9..D-B16** `[ratified 2026-07-27]` — tracked `briefs/` storage with JSON as record and HTML as disposable view · `/brief` auto-commits, never pushes · anchored VWAPs developing W/M/Q/Y plus prior M/Q/Y with σ1/σ2/σ3 · composites and single-print/LVN detectors **PARKED** on the operator's methodological point that a composite is a *conclusion* of judgment, not a mechanical window · TradingView-default recipes, parity-fixtured · operator-notes command plus mechanical scenario drafts · run time · state-only `ops/positions.yaml`.

**D-B17..D-B26** `[ratified 2026-07-27]` — MACD added · canonical parity chart `BINANCE:<SYM>USDT.P`, UTC, closed candles · 24 current + 4 historical parity rows · rolling-VWAP parity target is TradingView's *official* RVWAP, algorithm pinned from source · confluence parameters with the vwap family split · forward-log scope manual + mechanical + actual, strictly tagged · G-10 timing · three-table panel for sequence analysis · one contract, one paste.

**D-B27..D-B29** `[ratified 2026-07-27/28]` — backfill rule amended after operator challenge: historical confluence on exploration-classic is legitimate census work, the lockbox stays sealed, and backfilled output never enters `briefs/` · three session-anchored captures (`london` 12:00 / `ny_am` 15:00 / `post_ny` 21:30 UTC, times held in America/New_York) · stored OHLC dropped.

**Groups A–D** `[ratified 2026-07-28]` — v3 proceeds next · one runner three triggers (`daily_routine.py --slot`, no second scheduler) · Google Drive exists at `G:\My Drive\naiad-backups` · repo-root discipline and archive-dependency audit adopted as standing rules.

## 2.5 Known-wrong and open defects

| ID | Item | State |
|---|---|---|
| **F-AN-8** | v1.1's 4h/12h/1d layers computed over one extra, unclosed bar; propagates to ATR percentile and both momentum votes | **ruling made, amendment pending** |
| LIT | Six kline stores begin exactly at `LIT_FLOOR_MS` with 40,832 rows of flat synthetic padding (o=h=l=c=0.592, vol=0). Percentile/rank/bar-count wrong; **levels and volume-weighted quantities unaffected** (ATR level 0.19983 unchanged; percentile 63.2→61.5) | `[verified by ENGINE]` remediation needs operator authorisation; purge **then** refloor |
| `dryrun/` | `research_outputs/dryrun/` read by `fixtures/test_f8_journal.py:21` and `scripts/dryrun_autopsy.py:26`; resolves nowhere; in **zero** archives | `[builder]` genuinely lost, not archived |
| Thin shells | Six archived phase dirs still exist on disk holding 2–10 of 1,500–5,300 files each, so naive audits report them present | `[builder]` now documented in `docs/ARCHIVE_DEPENDENCIES.md` |
| G1–G12 | The twelve v1 gap fixes | specified in contract v4, unbuilt |
| Overwrite | Same-date re-runs silently overwrite; happened in the wild 2026-07-28 | F-B24 + G11 specified, unbuilt |
| Archive integrity | Captures untracked, no tamper-evident record, no off-machine copy | Phase II fixes; `backup_estate.py` scope excludes `briefs/` `[builder]` |

## 2.6 Reviewer errors logged in this chat

Kept because the pattern matters more than any single item: **every one was an error about what the machinery actually contains, or an over-strong inference stated as fact.**

1. **RVWAP σ-band prose spec** — "standard deviation of typical price" would have produced plausible numbers that never matched the operator's chart. Caught by the operator supplying the Pine source. Now pinned line-by-line.
2. **"22 days of Litentry"** — it is flat synthetic padding, not another asset's history; the remediation differs.
3. **Ten-asset study sizing** — exploration-classic is a **five-asset panel** (BTC/ETH/ZEC/SOL/NEAR) with two thin annexes and three assets at zero. The storage estimate was harmlessly conservative; the statistical-power claim was not.
4. **"CENSUS-1c"** — an occupied phase slot; proposing phase names from a lane that does not own the index was avoidable. Renamed CENSUS-1d.
5. **As-of invariant too strong** — "single forward pass, never vectorised" conflated *causal* with *streaming* and would have discarded proven causal machinery.
6. **Engine-version overclaim** — asserted `[verified]` consistency with a lane whose record this lane cannot read. Retracted; later confirmed properly by ENGINE.
7. **Exact-HEAD environment gate** — conflated environment identity with state freshness and produced a false halt. Corrected in v4 §0.1.
8. **Manifest "blind spot"** — the field is `daily_routine.py:119`, its scope *is* the whole tracked tree, and it was accurate when written.
9. **"Probe artifact" for Google Drive** — DriveFS was installed at 19:59:11, after the probe; the probe was correct at the time. Worse than being wrong: it was written into the ledger text as fact, and the builder refused to record it.
10. **Runtime estimate** off by ~5×.

## 2.7 Artifact index

**In-repo** — `prompts/CONTRACT_v4_ANALYTICS1_BRIEF2_FORWARD0.md` · `prompts/Daily_Brief_Builder_Contract.md` · `prompts/Daily_Brief_Contract_Amendment_1.md` · `prompts/CONTRACT_ANALYTICS1_BRIEF2_FORWARD0_draft.md` · `docs/handoffs/HANDOFF_2026-07-27_BRIEF_to_ENGINE.md` · `docs/handoffs/HANDOFF_2026-07-27_BRIEF_to_CENSUS_1.md` · `docs/ARCHIVE_DEPENDENCIES.md` · `scripts/archive_dependencies.py` · `analytics/` (uncommitted) · `tests/test_analytics.py` (uncommitted).

**Reviewer-side, produced in this chat** — `Naiad_Daily_Brief_Review_2026-07-27.html` (v1 reviewer edition, 12-gap register) · `Naiad_Daily_Brief_Review_v2_2026-07-27.html` (confluence-engine prototype computed live) · `HANDOFF_2026-07-27_BRIEF_to_CENSUS.md` · `REPLY_2026-07-28_BRIEF_to_ENGINE_errata_and_amendment.md` · `CONTRACT_v4_…md` · this document.

---

# PART 3 — Lines of work (ORCHESTRATOR)

## 3.1 Active line — BRIEF-2 build

**Owner:** BRIEF lane specifies, local builder executes, operator rules.
**State:** halted at Phase I on F-AN-8, ruling made, amendment paste pending.
**Critical path:** F-AN-8 amendment → Phase I completes → Phase II (largest) → Phase III → reviewer acceptance → **operator parity session (28 readings)** → one week live → threshold re-ratification.
**Only operator-labour item on the path:** the parity session. It is the adoption gate; without it the toolbox is verified plumbing, not trusted numbers.

## 3.2 Dependency this lane has on ENGINE

| Item | Why it matters here |
|---|---|
| LIT purge-and-refloor authorisation | The brief prints known-wrong LIT fields until it lands. Order is not optional: purge the six parquets **first**, then `engine/cells.py:42`; reversed order hard-fails every LIT load. |
| `backup_estate.py` scope | `briefs/` and `research_outputs/brief/` are outside it `[builder]`. One-line change identified, not made — it belongs to ENGINE, and it is only meaningful once `briefs/` exists in Phase II. |
| One-sided-window hazard | ENGINE reported it in `daily_brief.py`; F-AN-13 finds no instance in the extracted toolbox. Either it lives in the orchestration layer Phase II rewrites, or the report was mistaken. A specific `file:line` would settle it. |

## 3.3 Handoffs this lane has issued

| Document | To | State |
|---|---|---|
| `HANDOFF_2026-07-27_BRIEF_to_ENGINE.md` | ENGINE | filed, superseded in part |
| `HANDOFF_2026-07-27_BRIEF_to_CENSUS_1.md` | census lane | **answered** — ENGINE replied 2026-07-28, four errors accepted |
| `REPLY_2026-07-28_BRIEF_to_ENGINE_errata_and_amendment.md` | ENGINE | **awaiting relay by the operator** |

## 3.4 Proposals parked for the census lane

- **CENSUS-1d** (renamed from the colliding CENSUS-1c) — confluence matrix over exploration-classic, as-of correct, joined to census signals. Deferred pending frozen `analytics/`, a budgeted un-archive of the S-3 fill estate, and Q-1/Q-2.
- **H-RVX** — do RVWAP crosses confluence with the Secret Sauce EMA crosses? Returned as a named G-7 candidate pending a drafted contract with priors, a numeric agreement window, a sample definition and a numeric deflation threshold.
- **Phase 0 proxy** — re-labelled "Tier-A with a journal read": `census_outcomes.jsonl` carries `event_price` and `p0` on all 149,802 rows, but `s3_excursion_substrate.jsonl` lacks timestamp and asset columns, so the join key must be recovered from archived S-3 journals.
- **Standing invariant contributed by ENGINE and adopted here:** *a rolling window is a silent lockbox-spending mechanism* — trailing-window statistics extend an analysis's data footprint by their window length, and partition boundaries bind on the footprint, not the evaluation point.

## 3.5 Cross-lane facts worth propagating

1. **Drive for Desktop installed 2026-07-28 19:59:11.** Earlier "no Drive" findings were correct at the time. `G:\My Drive\naiad-backups` holds `naiad_estate_2026-07-28.zip` (492 MB) plus its sha256.
2. **An unattributed 1.66 GB / 1,028-file folder** named `naiad (local folder) BACKUP` sits on the Drive, created 21:22–21:23, placed by no known lane.
3. **`scripts/orchestrator_state.py`** appeared in the working tree mid-session, matching nothing under `_reviewer_box/` or `claude/` — it did not arrive through either channel.
4. **Thin-shell illusion:** archived phase directories still exist on disk with a handful of git-tracked files, so any audit checking mere existence will report archived data as present.
5. **`research_outputs/dryrun/` is genuinely lost** — in none of the six archives.

## 3.6 Parked, so they are not mistaken for forgotten

Composite building and the single-print/LVN detectors that rode with it (the operator's methodological point stands: a composite is a conclusion of judgment; the real automation target when revisited is mergeable-balance detection, not fixed N-day windows) · tick-based TPO, since profiles are kline approximations · any forward-validation protocol, which needs G-10 ratified separately · the v2×architecture cross · sizing work, formally deferred post-TC-1.

---

# PART 4 — The F-AN-8 ruling

## 4.1 What was found `[builder, verified arithmetic]`

| asset | TF | published RSI | analytics | bars published / estate | verdict |
|---|---|---|---|---|---|
| BTC | 1h | 52.4705 | 52.4705 | 60365 / 60365 | exact |
| ETH | 1h | 56.9922 | 56.9922 | 58455 / 58455 | exact |
| SOL | 1h | 50.7759 | 50.7759 | 51447 / 51447 | exact |
| BTC | 4h | — | mismatch | 15092 / 15091 | **−1** |
| BTC | 12h | — | mismatch | 5031 / 5030 | **−1** |
| ETH | 4h | — | mismatch | 14615 / 14614 | **−1** |
| ETH | 12h | — | mismatch | 4872 / 4871 | **−1** |
| SOL | 4h | — | mismatch | 12863 / 12862 | **−1** |
| SOL | 12h | — | mismatch | 4288 / 4287 | **−1** |

Six of six resampled pairs off by exactly one bar in the same direction; widening the load window does not produce it. Native 1h reproduces exactly. **The arithmetic is correct; the input window was not.**

## 4.2 Ruling `[ratified by operator 2026-07-28]`

**Drop the unclosed bar. F-B17 wins.** Reasoning on the record:

1. **It was already decided.** G1 and F-B17 exist to enforce closed bars. Preserving the extra bar to make a test pass would enshrine a known defect to protect a number we now know is wrong.
2. **Reproducibility.** A value computed on a forming bar changes minute to minute and cannot be re-derived later — fatal for an archive whose worth depends on comparability.
3. **Parity coherence.** The worksheet specifies readings on **closed candles only**. Keeping the forming bar would match TradingView's *live* display but never a closed reading, producing mismatches we would waste days chasing.

**Disclosed cost:** the brief will show the last *finished* 4h/12h/1d reading, not the live one the operator sees mid-candle. Correct for a written record, and a real difference from the chart.

## 4.3 Amendment — F-AN-8 restructured rather than waived

Switching the guard off would discard its value. It becomes three parts:

- **F-AN-8a — unchanged conventions must still reproduce exactly.** Every recipe whose closed-bar convention did not change reproduces its v1.1 published value to 1e-9. Native 1h already passes.
- **F-AN-8b — legacy-mode proof.** For every recipe whose convention deliberately changed, run the toolbox in a legacy mode that reinstates the in-progress bucket and assert it reproduces v1.1 **exactly**. This proves the dropped bar is the *only* difference and no other arithmetic moved. **If 8b fails, something else is wrong and the halt stands.**
- **F-AN-8c — documented diff.** Emit `_reviewer_box/_f_an_8_diff.json`: asset × timeframe × recipe, old value, new value, delta, and any resulting **verdict change**, since both momentum votes are downstream.

Legacy mode exists solely for this fixture. It is never reachable from `/brief` and a fixture asserts so.

## 4.4 Scope of what changes

Affected: MTF RSI on 2h/4h/12h/1d · ATR and ATR percentile on 4h/12h/1d · volatility regime · divergences on 4h and above · confluence flags `rsi4h_bull_side` and `rsi12h_bull_side` · **the daily momentum vote** (4h + 12h) · **the weekly momentum vote** (12h + 1d).

Unaffected: everything on native 1h · volume-weighted quantities · structure levels · the Secret Sauce radar, which reads the engine directly.

**Consequence for the archive:** captures published before this change are computed under a different convention. Every capture already carries `rules_version`; that version must bump, and the diff table becomes the bridge between the two eras.

---

# PART 5 — Pending decisions

## 5.1 Immediate — unblocks the build

| # | Decision | Recommendation |
|---|---|---|
| **1** | Issue the F-AN-8 amendment paste (ruling + 8a/8b/8c) | **Yes** — the builder is halted and correct to be |
| **2** | Does `rules_version` bump to 2.0.0 at BRIEF-2, marking the closed-bar era boundary? | **Yes** — a convention change that moves published numbers is a major bump; the diff table is the bridge |

## 5.2 Operator-owned, routed from ENGINE

| # | Decision |
|---|---|
| **3** | **LIT purge-and-refloor** — destructive and engine-touching. Purge the six parquets **first**, then `engine/cells.py:42`. Reversed order hard-fails every LIT load. |
| **4** | **G-2 disposition**, including correcting its "pre-Lighter (Litentry)" register text, which carries the same wrong diagnosis this lane made. |
| **5** | **Q-1 / Q-2** — block CENSUS-1d Phases 1–3. |
| **6** | **Phase 0 registration route** — standalone Tier-A now, or folded into CENSUS-2/CCL. |
| **7** | **G-9 → G-10 renumber** for the Forward Validation Protocol, before ANALYTICS-1 is ratified. Rests on an `[agent]` claim; cheap and reversible. |
| **8** | **Padding-provenance diagnostic** alongside the purge, so the mechanism is found and not only the symptom — otherwise it recurs at the next mid-month listing. |

## 5.3 Operator-owned, this lane

| # | Decision |
|---|---|
| **9** | **`research_outputs/dryrun/` is gone.** Re-generate it, retire `dryrun_autopsy.py`, or accept the permanent skip. |
| **10** | **The unattributed 1.66 GB Drive folder** — whose is it, and does it stay? |
| **11** | **`backup_estate.py` gains `briefs/`** — one line, ENGINE's file, meaningful once Phase II lands. |
| **12** | **Parity session scheduling** — 28 readings; the adoption gate for the whole toolbox. |
| **13** | **Relay** `REPLY_2026-07-28_BRIEF_to_ENGINE_errata_and_amendment.md` and this document's §3.5 to ENGINE. |

## 5.4 Deferred by design

Threshold re-ratification after ~one week of live use (cluster tolerance, family cap, POI budgets, confluence dictionary, bias vote rules) · composites and SP/LVN detectors · G-10 ratification when a real forward hypothesis exists · CENSUS-1d and H-RVX contracts.

---

## Closing note for whoever picks this up

Two habits are worth preserving above any particular finding.

**The fixtures are earning their keep by failing.** F-AN-8 was written to catch a refactor slip and instead found a defect in the accepted baseline. The archive-dependency audit was adopted to prevent a third retrieval cost and instead found permanently-lost data and the thin-shell illusion that hid it. Both times the instrument found something better than what it was aimed at.

**Errors get logged with their mechanism, not just their correction.** Ten reviewer errors are recorded in §2.6, and nine of them share one shape: an inference about machinery, stated with more confidence than the evidence carried. The custodian rule that moves verification earlier — read the code before writing the contract clause — exists because of that pattern, and the two errors the builder caught on 2026-07-28 show it is not yet fully internalised.
