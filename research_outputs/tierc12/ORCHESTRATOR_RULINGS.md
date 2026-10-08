# TIER-C12 · ORCHESTRATOR RULINGS (O-1 … O-24)

Filed 2026-10-08 after the R0 scout (nine maps, `research_outputs/tierc12/scout/U1…U9`), BEFORE any executor
reading is drafted and before any book exists. These are the cross-cutting rulings every LEANS section must
conform to. They are executor readings of the contract (`exchange/queue/2026-10-08_TC12_APOLLO.md`, sha256
`861d6050e80e66995e4f9db2855aaf274d63285249c2549e5a0813582095a7bd`, commit `28e006b`), not operator rulings:
each is vetoable by the operator and each is carried into the build report as a reading. A LEANS drafter who
finds one wrong on the facts files an `OBJECTION O-n` block in their section; nobody silently diverges.

The one operator ruling taken in-session (2026-10-08, by question): **TC12 is built in the MAIN tree
`/Users/luis/Naiad` on `v12-v1-census`, addressed by absolute path** (the session's shell is pinned inside the
X worktree; no `cd` to the repo root, `git -C /Users/luis/Naiad` only).

## A · Where and how

**O-1 HOME AND NAMES.** Scripts `scripts/tierc12_*.py`; records `research_outputs/tierc12/`; the module
`analytics/value_area.py`; commit subjects `tierc12(<STAGE>): …`; stage ids `TC12-…`. Never the prefixes
`tierc10_`, `tierc11_`, `tc11x_` in `scripts/` (their sweeps glob by prefix; X's merge allow-list and close act
refuse on `scripts/tc11x_*.py` and `research_outputs/tierc11x` in main). Nothing is written under `exchange/`
before CLOSE except STEP Q (the 07:00 −03 daily routine stages and publishes `exchange/**`).

**O-2 STAGING.** Explicit pathspecs only. Never `git add -A`, `git commit -a`, or a stash. The two files
already dirty in main at R0 (`exchange/status/daily/DAILY_2026-10-08.md`,
`research_outputs/tierc10/close/FIXTURES_CLOSE_ledger_append_root.txt`) are not TC12's and are never staged.
The nested `research_outputs/tierc12/.gitignore` keeps parquet, `_det_*/` and `x_rec/**` out of git; the root
`.gitignore` is not edited. An untracked artifact is pinned by sha in its stage's progress record.

**O-3 THE FROZEN ESTATE.** Byte-frozen for the whole build: `research_outputs/tierc10/**`,
`research_outputs/tierc11/**`, `scripts/tierc10_*`, `scripts/tierc11_*`, the X worktree
(`.claude/worktrees/tierc11x`, certified tip `7b24f835…`), the three earlier contracts in `exchange/queue/`,
`LEDGER.md`, `LEDGER_APOLLO.md`, both forward ledgers, both snapshots `tc10_20260921` and `tc11_20260925`, and
the live cache. Three operator close acts (TC10 → TC11 → X) are pending and each re-verifies bytes and line
citations in those files at its step 0. No TC10/TC11/X suite, scorer or builder is ever RUN in place (they write
`_det_*`, `_rerun` and `__pycache__` under their own records). TC12's env shim write-protects all of them.

**O-4 READING X.** X is unmerged. Its records and sources are read ONLY from the byte copies under
`research_outputs/tierc12/x_rec/` (APFS clones taken at R0 from the X worktree at tip `7b24f835…`; 490 files,
343,737,312 B, 345 of them untracked at X's tip and therefore single-copy), each read asserted against
`x_rec/X_REC_MANIFEST.json` (path + sha256). No `tc11x_*` module is imported or executed — importing arms its
hooks and can write. Where TC12 needs X's logic it is MIRRORED into `tierc12_*` code, with the X function it
mirrors named, and held equal to X's filed records by a fixture.

**O-5 ONE PROCESS, ONE SUBSTRATE.** `NAIAD_CACHE_DIR` is exported as an absolute path before python starts
(unset, `cache_dir()` falls back to the LIVE cache; mistyped, it mkdirs). Lineage memos are keyed by bare symbol,
so a process binds exactly one snapshot. `PYTHONDONTWRITEBYTECODE=1` always. Compute: ≤ 6 workers while the
1-minute load is < 10, else 2; merges in a fixed order.

**O-6 PROGRESS.** Each stage builder writes `research_outputs/tierc12/progress/<STAGE>.json` (stage, status ∈
{COMPLETE-VERIFIED, PARTIAL, ABSENT}, as_of, artifact_shas, fixtures, blockers, one_line, notes) and never
`PROGRESS.json`; `scripts/tierc12_progress.py` merges them verbatim. A stage is COMPLETE only if its artifacts
exist, their shas verify and its fixtures re-pass now. The durable record is the repo, never a scratchpad.

## B · The corridor

**O-7 THE PIN.** The corridor pin is the latest 4h bar closed when STEP Q was committed
(2026-10-08T22:52:13Z): close `1791489600000` = **2026-10-08T20:00:00Z**, 83 4h bars past TC11's pin. It is
taken by value at STEP Q (TC11's L-0.1 law), proven closed against the venue clock at fetch, and the
latest-at-fetch bar is printed beside it. Stage D writes it once to `data/AS_OF_PIN.json`; every later read is
by object.

**O-8 THE SNAPSHOT.** `~/.cache/naiad/snapshots/tc12_20261008` = an APFS clone of `tc11_20260925`, re-hashed
against TC11's filed manifest BEFORE extension, then extended by REST from each tape's edge (TC11's fetch
superset: 17 stems × {5m, 1h, 4h, 12h} native + funding; 1d and 1w derived from native 4h exactly as TC10 L1 /
TC11 did — that is what X's verdicts were measured on). The contract's "twelve new assets 1h/4h/1d only" binds
which lenses Stage V stamps, not which tapes the snapshot carries. PREFIX IDENTITY is a Stage D fixture: every
row with close ≤ TC11's pin is bit-identical to the TC11 snapshot. The live cache is never read or written.

**O-9 THE SCORED WINDOW AND THE STRIP.** Every registered row (all five) is scored on trades whose ENTRY bar
closes at or before TC11's pin `1790294400000` (2026-09-25T00:00Z). The bars in (TC11's pin, TC12's pin] are
THE FORWARD STRIP for every book and every arm: ridden, printed beside, never scored, never pooled into a CI.
Reason: Stage C says so for the control ("the extension printed separately (the forward strip, never scored)");
P-ADM-1's pre-seen cell reproduces exactly only on TC11's corridor; and the strip is the only water no table
has read, which is what the forward ledger exists to accumulate. "Full corridor" (P-SFP-VA-1) and "HOLDOUT era"
(P-SCALP-3) name ERAS inside that window (holdout = entry-bar close after `1719791999000`). Open-at-TC11's-pin
trades follow TC11's `corridor_end` law in the scored book and are continued in the strip print.

## C · Rulings enacted from TC11 §11

**O-10 "tc11-stamp" IS A CLOSE ACT.** Stamping TC11's contract BUILT moves sha `bb38e016…`, which TC11's
pending close re-verifies and its generator HALTs on. So during the build NO TC11 byte moves. The stamp + the
re-pin of its registry files are written as steps of TC12's `close_acts.sh`, ordered after the TC10, TC11 and X
blocks have landed, with the BUILT line APPENDED as the contract's last line (never under RATIFIED — the
registration payloads cite contract lines 1–103). CLOSE proves the whole cascade GREEN in a scratch clone and
files that transcript. `SCORES.json` keeps its leaves: its sha is asserted unmoved at R0, at CLOSE and inside
the cascade (Q1).

**O-11 "1w".** No 1w range cell exists anywhere in TC12: no trade, no feasibility row, no licence. The 1w VA is
a captured-only stamp column (V5), Tier-E.

**O-12 CLOSE ACTS (Q6).** The executor writes `research_outputs/tierc12/close/close_acts.sh` and never runs it;
never pushes, publishes, merges, moves a report onto the bus, or appends to `LEDGER_APOLLO.md`. Its step 0
requires the TC10, TC11 and X ledger blocks by bytes, in that order.

**O-13 NO POST-HOC CANDIDATE (Q8).** Nothing discovered in a TC12 Tier-E table is registered, promoted or given
a verdict word. P-ADM-1 alone is pre-named from TC11's crossed table and carries `pre_seen`.

**O-14 CROSS-LENS VISIBILITY (Q9).** A lens-L quantity is visible at an instant τ iff its bar's CLOSE ≤ τ
(`asof_index`, close ≤ instant). Tier-E rows print `would_read` wording and no verdict word.

## D · The value area

**O-15 SOURCE AND LOOKBACK.** The profile is `analytics.profile.volume_profile` exactly as X called it (120
range-relative bins, uniform spread over the bar's range, POC = first max, 70% expansion, levels at bin
centres; TPO twin). Lookbacks are READ from `x_rec/tierc11x/pins/PINS_X.json` (`L.by_lens.<lens>.L_of_record`)
and frozen as integer bars. ATR_L is `engine.indicators.atr(h, l, c, 14)` on the lens's own tape, handed into
the module as data. `analytics/value_area.py` is pure (numpy only; no engine import, no I/O), stays OUT of
`analytics/__init__` / `_MODULES` / INTERFACE (so `analytics_sha` does not move), and is imported by no
decision module — the closure fixture asserts exactly that.

**O-16 THE STATE MACHINE IS THE CONTRACT'S V2, AND THE DIFFERENCE FROM X IS DATED.** The module implements V2
as written (ACCEPTED on 8 consecutive closes beyond the edge OR one close ≥ 1.5 ATR_L beyond; swing failure =
back inside within K = 3 closes; decay when the re-rolled VA contains the close). X's machine OF RECORD is a
different law (8 closes only; return within 7); V2 equals X's `die_parity` and `k3` twins combined, which X
never ran together. So: (a) every close at bar t is judged against VA(t−1), the profile in force before that
close (X's convention; VA(t) itself uses bars ≤ t and is stamped as in force from t); (b) equality with X is
asserted on the 4h holdout against X's filed twin rows where the two laws must agree; (c) the differences are
filed as a dated amendment at freeze; (d) the report says plainly that the feasibility words licensing the
range trades were earned on X's record machine, not on V2.

**O-17 THE MIRROR READS, NEVER RECOMPUTES.** F-VA-MIRROR compares the five words against
`x_rec/tierc11x/va/feasibility.parquet` (sha `ea8573b3…`) at POOLED:CLASSIC5 · holdout · va_regime, and HALTs
on any disagreement. Each range trade reads the licence row of its own scoring era and the report prints the
rows beside it that do not pass (1d taker fails on ALL and on tuning).

**O-18 THE TRAVERSE IS FITTED ON THE TUNING ERA.** V4's edge-to-edge median is measured on tuning-era bars only
(close ≤ `1719791999000`), frozen as an integer per lens before any range book exists, and read by object ever
after. The whole-corridor figure is printed beside as a twin. Reason: P-SCALP-3 is scored on the holdout and a
time stop fitted there would be a look-ahead.

## E · Costs

**O-19 FEES.** TC12 writes its own `research_outputs/tierc12/data/fee_schedule.json` (the contract's
"`data/fee_schedule.json`" is the tier's data directory, as in TC10 and TC11); TC11's file is not edited. It
carries `maker_bps_side` per venue, taken from the venue's published USDT-M schedule with URL + retrieval date
in the manifest; if the page cannot be retrieved it carries the figure on file (2.0, README) flagged NOT
RE-CONFIRMED. Taker and charter tiers are asserted equal to TC11's file. TC12's env reads TC12's file and a
fixture proves it (no typed bps anywhere). If the published maker rate differs from the 2.0 bps/side X assumed,
that is printed beside the "1h maker PASS" word, which was earned at 4.0 bps round trip.

**O-20 TICK.** The tick of record is `price_tick` from Stage D's own `CONTRACT_SPECS.json` capture, applied
across the whole corridor. It is coarser than the historical tick on part of the tape, so "through by one
tick" is stricter than history, never looser. Tick arithmetic is exact (integer ticks), never float compare.

## F · Books, statistics, labels

**O-21 GATES ARE POST-FILTERS.** P-ADM-1, P-BRD-1 and P-DIR-1 remove campaigns from the filed v6 book (TC11's
L-1.5 law); a re-ride twin is Tier-E disclosure. The base arm is ONE book, held equal to TC11's filed v6
(`TP._book_sha` `f3c68f54…`, n 200).

**O-22 STATISTICS OF RECORD.** `tierc5.cluster_boot_diff` / its vs-zero sibling: whole-asset clusters, 4000
draws, 5th/95th percentile interval, p = (#≤0 + 1)/(B + 1), seed 20261008 passed explicitly with 20260816
printed beside. Verdict: SUPPORTED iff CI lo > 0 AND p ≤ the family bar (0.10 ÷ m, parsed from the contract's
stage headers, never typed). A row closed by precondition writes STATUS only, carries no number and spends no
test; F-FAM proves it on a planted family.

**O-23 LABELS CARRIED IN THE VERDICT TEXT.** P-ADM-1: `pre_seen` — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (cited
to `research_outputs/tierc11/stage_g/` by file and cell). P-BRD-1 and P-DIR-1: `selection_hazard`
(direction-informed), NOT CONFIRMATORY. P-SFP-VA-1 and P-SCALP-3: additionally `pre_seen` for bars ≤
2026-09-25T00:00Z under X's standing ledger line (X3 already printed value-area swing-failure outcomes on those
bars) — the contract is silent on this and the label cannot flatter.

## G · Ledger, ferry, close

**O-24 LEDGER AND FERRY.** The forward ledger of record for TC12 is its OWN file
`research_outputs/tierc12/forward/FORWARD_LEDGER.jsonl`, opened on the bytes of X's ledger (three books) and
continued under `scripts/forward_log.py`'s law; TC11's and X's ledgers are sha-pinned ancestors, never
appended in place. The fourth book has its own spec document and sha. Row files are staged off-bus under
`research_outputs/tierc12/ferry/` with a forecast; the ferry of record into `exchange/rows/tierc12/` is a close
act (the box is within a few KB of WARN once the three earlier closes land, so most files will be HELD and
LISTED for ATHENA).
