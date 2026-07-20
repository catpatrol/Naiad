# TC-5 — Intraday Re-Spec 1H/5m (Fractal Repair) — Builder Contract

**Phase:** v12 Study · **Tier C** (new pre-registered study arm — G-7 before any run). **Engine: 1.0.10, byte-untouched — this phase is config-only.** (Baseline trading behavior has been byte-identical since 1.0.8; 1.0.9/1.0.10 were instrumentation, proven by F-BYTE. TC-5 does not wait for, and does not use, TC-1's 1.0.11 keys.)
**Operator ruling in force (2026-07-20):** TC-5 runs **in parallel with TC-1, now** — the structural stop improved intraday 4.7× and still left it negative (−307.43, gross only +92.65), so the mandate's re-spec is tested as its own variable.
**The thesis being tested (fractal repair):** costs are scale-invariant in bps while excursions scale with timeframe. Intraday at 1H/1m has a median peak excursion of ~10 bps against a ~19.6 bps toll — structurally unpayable. Re-spec the exec chart to 5m and the same logic should produce excursions that clear the toll. **Single-variable isolation: baseline architecture only** — no structural stop, no trail, no floor. Crossing re-spec × architecture is a later phase *if both win*.

---

## 0. Operator instructions

Save this contract into the repo → `claude` → `git status` clean → paste §8. *What you should see, in order:* (a) definitions restatement; (b) the **G-7 pre-registration commit** — the five config shas, the pinned v1 same-asset comparison numbers (computed from `journal_pass2` and printed **before** any v2 run), and all five prediction rows; (c) five cells run **twice** (5m exec ≈ 5× fewer bars than 1m — faster than pass2's intraday portion; under an hour is plausible); (d) fixtures, all MATCH; (e) the five-row scorecard and the comparison tables. Any fixture MISMATCH: halt, report. Send back `tc5_results.json`, `TC5_RESULTS.md`, fixture table, scorecard.

## 1. The cells

Five new cells: **{BTC, ETH, SOL, NEAR, ZEC}USDT_intraday_v2** — governor **1H**, exec **5m**, `tf_align` **15m** (role-preserving one-step-above-exec, per FH-3's RELATIVE verdict — veto V1), MTF_SET unchanged {5m, 1h, 4h, 12h}, all signal parameters unchanged (ATR-relative by construction — the fractal port is the point), G-8 guards, $10k initial equity per cell, exploration-classic window, standard fee/slip tier per asset. ZEC included knowing it may halt again — **halts are data**, and the halt calendar is a deliverable.

## 2. What this phase is NOT

Not an architecture test (baseline exits and stops only) · not a retirement of v1 intraday (the chartered 1H/1m cells remain; this is a candidate replacement being priced, not a replacement) · not a sizing or gate change · not comparable to v1's full 7-cell book — **every comparison is same-asset, five-cell subset, pinned at pre-registration** · not free of the era confound (the 2022–23 chop that halted v1 intraday sits inside the window; the era-split deliverable addresses it, not a caveat-waiver).

## 3. Comparison basis — pinned before running

At pre-registration, compute and print from `journal_pass2` (read-only) the **v1 same-asset subset**: {BTC, ETH, SOL, NEAR, ZEC}USDT_intraday — net 1×, gross 0×, campaign count, tranche count, median `mfe_bps`, the `mfe_bps`/toll ratio, halt dates. These pinned numbers are the denominators of every prediction below; they enter the G-7 ledger entry verbatim.

## 4. Fixtures — any MISMATCH halts

| # | Fixture | Expected |
|---|---|---|
| F-CFG | Five config shas match the pre-registration commit | exact |
| F-SPEC | Every v2 journal header: gov=1h, exec=5m, tf_align=15m, MTF_SET unchanged | exact, all 5 |
| F-ENG | Engine tree diff vs `6fdab03` | empty (config-only phase) |
| F-GUARDS | G-8 a–d hold in every v2 cell | 0 violations |
| F-DET | Double-run identity, all five cells | identical |

## 5. Pre-registered predictions (v1 = pinned same-asset subset from §3)

| # | Prediction | Prior | Falsified if |
|---|---|---|---|
| P-TC5-a | Median `mfe_bps`/toll ratio (v2) ≥ **2×** the v1 ratio — the TC-4-chartered form | 60% | < 2× |
| P-TC5-b | v2 five-cell net 1× ≥ v1 pinned net 1× **+ 500** | 55% | below |
| P-TC5-c | v2 campaign count ∈ **[30%, 60%]** of v1 pinned count (5× fewer bars → fewer, better-formed births) | 60% | outside |
| P-TC5-d | Fewer v2 cells halt than v1 same-asset halted, and any v2 halts occur later in calendar time | 60% | either half |
| P-TC5-e | v2 signal-mix per 100 governor bars lands nearer swing's census than v1-intraday's (the fractal-repair signature; FH-1 method, PRIME rate ± TPW/CLUSTER rates) | 55% | nearer v1 |

## 6. Deliverables

Per cell and pooled: headline (0×/1×/2×, strip-best, win rate, campaigns/tranches, cost stack, `fills_without_exit_row`), the `mfe_bps` distribution against toll (the thesis table, v2 vs pinned v1 side by side), signal-mix census per 100 governor bars (v2 vs v1-intraday vs swing — three columns), holding-time medians, halt calendar with equity paths, **era split** (pre/post the 2023 boundary used in the standing intraday-era caveat), adds funnel. Every table: in-sample caveat, same-asset-subset note, era note.

## 7. Verdict, artifacts, ledger

**PASS** — 5/5 fixtures, 5/5 predictions scored falsifications-first, deliverables with caveats, determinism proven. **HALT** — any fixture MISMATCH; F-ENG especially (an engine diff in a config-only phase means the isolation is broken). Artifacts: `configs/tc5_*.json` · `research_outputs/tc5/` roots · `tc5_results.json` · `TC5_RESULTS.md` · two ledger entries (G-7 pre-registration with pinned v1 numbers **before** any run; completion with fixtures, scorecard, and the line *"single-variable: re-spec only; architecture cross deferred"*). Commit; **do not push, do not merge.**

## 8. The go-paste

```
CONTRACT: TC-5 — Intraday Re-Spec 1H/5m (Tier C; engine 1.0.10 byte-untouched, config-only)

Read TC5_Intraday_Respec_Builder_Contract.md in the repo in full first. The contract is
the authority; this paste is the trigger.

Scope in one line: five new cells {BTC,ETH,SOL,NEAR,ZEC}USDT_intraday_v2 at governor 1H
/ exec 5m / tf_align 15m, baseline architecture, G-8 guards, exploration-classic window
— the fractal repair priced as a single variable against the pinned same-asset v1
subset.

Order of work — mandatory:

1. DEFINITIONS (contract §§1–3). Restate in your own words: why this phase is
   single-variable and what is deliberately NOT in it; the role-preserving tf_align=15m
   choice; why every comparison is the pinned same-asset subset and never v1's full
   book; why halts are data.

2. G-7 PRE-REGISTRATION — compute the §3 pinned v1 numbers from journal_pass2
   (read-only), print them, commit them with the five config shas and all five
   prediction rows BEFORE creating any v2 config run.

3. RUN the five cells twice into research_outputs/tc5/. Do not touch the engine tree.

4. FIXTURES (§4) — F-ENG first: the engine diff must be EMPTY.

   *** ANY MISMATCH: HALT. F-ENG failure means the single-variable isolation is
       broken and nothing in this phase attributes cleanly. ***

5. DELIVERABLES (§6) — the thesis table (mfe_bps vs toll, v2 beside pinned v1) first,
   then the three-column signal-mix census, era split, halt calendar.

6. PREDICTIONS (§5) — all five, falsifications first. ARTIFACTS + completion ledger
   (§7). Commit. Do not push, do not merge.

Do NOT, even if it seems helpful: modify the engine or any existing config · apply the
structural stop, trail, or bps floor to these cells · compare against v1's full
seven-cell book · retire or modify the v1 intraday cells · touch the lockbox.

Report back: definitions restatement, pre-registration confirmation with the pinned v1
numbers, fixture table, the thesis table, per-cell headlines, the five-row scorecard,
both hashes, tc5_results.json.
```

---

*Contract prepared by the reviewer under Fable-mode, 2026-07-20. One variable, five cells, five predictions against numbers pinned before the first bar is read. If the fractal thesis is right, the same logic at 1H/5m clears the toll that 1H/1m structurally could not; if it is wrong, the falsification is exactly as valuable — it would say intraday's problem is not scale but signal, and TC-2's re-entry bar inherits the mandate. Either answer moves the study.*
