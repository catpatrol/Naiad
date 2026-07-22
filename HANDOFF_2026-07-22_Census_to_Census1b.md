# Session Handoff — Naiad v12 / Secret Sauce · 2026-07-22
## Priming a new chat to verify the final hygiene commit and drive to CENSUS-1b

**Read this first.** You are the reviewer (Claude, Fable-mode) on a quantitative crypto-trading research project. This document hands off an in-flight session that hit its attachment limit. Your immediate job: (1) receive screenshots of the builder's output for the last git paste, verify the commit landed correctly, then (2) continue to the next analytical phase, **CENSUS-1b**. Everything you need is below; the userMemories attached to this project carry the ratified long-term state and should be trusted as the durable record.

---

## 0. Who's who, and the operating discipline

- **Ludwig** — the operator. Discretionary crypto trader with **no programming background**. Owns every merge and every gate decision. Writes in one-word ratifications or explicit rulings.
- **Claude Code** — the builder. Executes locally on Windows/PowerShell. Never merges without operator sign-off. Has caught **five** shell-level errors in the reviewer's git instructions this session — the reviewer's git muscle-memory is the known weak link; the builder's verify-first discipline is the safety net. Treat builder pushback as signal.
- **You (reviewer, Fable-mode)** — independent verification. Recompute every headline from raw artifacts before believing it. Pre-register predictions with explicit probabilities. Own falsifications on the record. Maintain the append-only ledger discipline. **Never let a cost-free or interval-free number stand alone; always print the strip-best line; treat falsification as a deliverable.**
- **Plain-language rule:** Ludwig has no programming background. Every operational instruction is step-by-step with expected output. Every acronym is expanded on first use. When you give the builder or the terminal *anything* — git commands, one-liner questions, contract go-pastes — you provide the **exact paste-ready text in a code block**, never a paraphrase. This is a ratified standing rule.

## 1. What the project is, in plain terms

Ludwig has a discretionary trading method called **Secret Sauce** (an indicator on TradingView, currently version 11.3). The project **Naiad** is an effort to *systematize* that method — turn his intuition into mechanical rules a computer can backtest — and, having found the current mechanical version loses money, to **redesign it** into a profitable engine (the redesign target is **SSv12**).

The machinery: a **Python replay engine** ports the Secret Sauce logic and runs it over historical data (a "backtest") on **10 crypto perpetual-futures assets** (BTC, ETH, SOL, NEAR, ZEC, JTO, TAO, HYPE, FARTCOIN, LIT) across three trading styles ("mandates"): **swing** (4-hour governor / 5-minute execution), **intraday** (1-hour / 1-minute, being re-specced to 5-minute), and **position** (12-hour / 15-minute). That's a **30-cell grid** (asset × mandate). The repository lives on a Windows/OneDrive path; git branch is `v12-v1-census`.

Two technical terms you'll need constantly:
- **R** = one unit of planned risk = **0.5% of a cell's equity**. All results are quoted in R. "cell-R" = size-weighted realized R across the grid.
- **MFE / MAE** = Maximum Favorable / Adverse Excursion — how far a trade went *in your favor* / *against you* while open. Central to everything the census measured.
- **bps** (basis point) = one hundredth of one percent of price. Costs (the "toll" = fees + slippage) are ~14/20/30 bps per round trip by asset tier. **The cost identity — cost-in-R = cost_bps ÷ stop_bps — is the project's decisive lever:** a stop placed too close in bps means the toll eats the trade.

## 2. The three-tier methodology and the gate discipline

- **Tier A** — arithmetic over existing journals. Free, no pre-registration required.
- **Tier B** — instrumented replay: trading logic unchanged, extra data captured, byte-identity enforced (the traded numbers must not move; a fixture called F-BYTE proves it).
- **Tier C** — actual rule changes. Must be **pre-registered under G-7** (a ledger line with config hash, hypothesis, and prediction) **before** the run.

Every phase produces a **builder contract** — a formal spec with numbered fixtures (integrity checks that halt the run on mismatch), pre-registered predictions with probabilities, deliverables, verdict criteria, and an explicit "what this phase is NOT." The reviewer drafts contracts; the builder executes; nothing merges without Ludwig.

**Evidence spend is irreversible.** There's a sealed "lockbox" data partition (July 2024 – Oct 2025) that must never be looked at until a pre-registered final test. All current work is on the "exploration-classic" partition (through June 2024), which is free to mine but proves nothing out-of-sample.

## 3. The arc of findings that got us here (compressed)

1. **The system loses money** on the current logic (baseline: −1,797 R on the grid).
2. **The pyramid** (stacking adds into a winning trend at flat risk) is the only reliably profitable trade population found — but it depends on a broken mechanism (see #6).
3. **The cost identity is decisive** — re-entries (opening fresh trades after a stop-out) carried 83% of the losses.
4. **TC-1** (a 2×2 factorial, four full re-runs crossing stop-type × exit-type) found the **structural stop** — placing the stop beyond a real 1-hour swing point instead of a fixed tiny distance — is the **dominant architecture**: it turned the grid from −1,797 to −351, made the swing mandate net-positive, and quadrupled gross edge. But the trailing exit was dominated, and the two levers *anti-synergize* (fighting each other, interaction −703).
5. **TC-1 also proved Ludwig's core thesis with a number:** the winning book takes *more* trades than the baseline and still loses — so the disease is now on the **entry side** (too many marginal trades), not the management side.
6. **The circular-topology diagnosis (Ludwig's, then proven):** the "add to a winner" gate depends on the stop ratcheting up, which depends on a new entry signal firing, which depends on a pullback the trend won't give. The serpent eats its tail — the gate is frozen exactly when you want to add. **S-3 measured this at 97.59%** of winning moments having no add signal available.
7. **S-3** (enrichment of the winning book) also found: the confluence value (multi-timeframe agreement) is **real but lives in the slow timeframes** and only showed up once the stop was fixed; the "sniper pocket" entry thesis is **dead at full sample** (demoted to a candidate factor, not a gate); and it built a **permanent cross-run excursion substrate** so no run is ever discarded and future deterioration can be diagnosed.
8. **TC-5** (re-speccing intraday from 1-minute to 5-minute) confirmed the **fractal repair** mechanically (excursions now clear the toll) but not economically (intraday's residual problem is signal quality over a longer life — inherited by the future TC-2). This is why **entries are now floored at 5-minute** — no timeframe below 5m, ever.

## 4. THE MOST RECENT PHASE: CENSUS-1 (just completed and verified)

**What it was.** A **trade-independent** census (it generates no trades and changes no rule) that journals **every EMA cross** — the 9/89 ("regime"), the 89/200 ("stage"), and a **new 9/200 ("momentum-vs-trend")** — across **all seven timeframes** {5m, 15m, 30m, 1H, 4H, 12H, 1D}, plus the full price-vs-EMA state, then measures forward MFE/MAE in both bps and ATR over horizons {20, 100, 500 bars} plus a "regime-scale" horizon (until the governor flips). Analyzed under **four candidate governors** {1H, 4H, 12H, 1D} — a competition, not a single winner, per the fractal lens (different mandates may want different governors). It carried three operator-driven additions from an amendment: **D8** the cascade-ladder (does the time-sequence of crosses up the timeframes constitute an entry-and-add schedule?), **D9** a k-of-N confluence-factor scoring analysis (trade when *enough* factors present, not all), and **D10** the pullback-terminus zone-landing census with a mandatory matched null (do pullbacks land on EMA zones more than chance?).

**Verdict: PASS**, 5/5 fixtures, 7/9 predictions confirmed / 2 falsified — but the **reviewer's deep read of the raw JSON changed the scorecard's meaning** (details in the state-of-project report, companion document). The short version:
- **A units confound** (forward MFE measured over a fixed exec-bar window but denominated in each timeframe's own ATR) makes the per-timeframe gradients mechanically artifactual and neutralizes the trigger ranking as delivered — **the honest ranking must be re-done in bps net-of-toll**, which is what CENSUS-1b does.
- **The cascade ladder's add-alpha is ~zero** at this horizon (symmetric MFE/MAE per rung) — survives as a possible *timing* schedule, not an *edge*.
- **The durable, null-survived findings:** the **zone-landing mechanism** (pullbacks land within 0.35 lens-ATR of an EMA at ~2× the random rate, on all four governor lenses — Ludwig's capitalized question answered YES) and the **maturation clock** (the 9/89→9/200 lag is a usable trend-age distribution, quartiles 10/52/150 timeframe-bars).
- **The reconciliation that redirects the redesign:** slow-timeframe agreement was *falsified* as an excursion-*magnitude* lifter but was *confirmed* on the winning book as a *realized-outcome* lifter — so it's a **survival / stay-in-and-add variable, not an entry-magnitude variable.**
- **The macro-lesson:** everywhere the census looked with light conditioning, **gross forward excursion is near-symmetric** — entry-side cross combinatorics do not tilt raw price. The measured edge lives in **exit asymmetry, toll-space scaling, and location-specific structure (the EMA-terminus mechanism)**. The census disciplined the redesign by telling it where *not* to dig.

## 5. EXACTLY WHERE WE ARE RIGHT NOW — the pending git operation

The session ended mid-way through a **repository hygiene cleanup** (not analysis — housekeeping to make the repo's own history tell the complete story). Context: a `git status` found 14,011 untracked files (mostly large journal payloads and 5 binary "packet" zips) plus 14 loose documents. The builder and reviewer triaged them. The rulings Ludwig just gave:
- **Commit** the 7 genuinely-untracked forensics/findings/handoff records (they exist nowhere in git history — a provenance gap).
- **Commit** the two missing pre-registration contracts (RC-Recompute, V3-Recompute) with an honest "added after the fact" note — the committed *result* files reference "contract §4/§5" that currently resolve to nothing in-repo, so those two phases' pre-registration was unauditable.
- **Move** the three loose `s3_*log*.txt` run logs under `research_outputs/s3/` to match how every other phase's run logs are tracked, then commit.
- **`.gitignore`** was extended to fence the journal payloads and packet zips (charter §10 — journals live on an orphan `data` branch only), with exact-path negations so 19 already-tracked analysis products and the pinned manifests stay tracked. This is verified correct.

**Four commits were issued as paste blocks, in this order:**
1. `.gitignore` hygiene fix, alone.
2. The 7 untracked records.
3. The two missing pre-registration contracts (with the after-the-fact note).
4. Move + commit the S-3 run logs — **this one was NOT yet confirmed complete.** Before committing it, the reviewer asked the builder to list the actual `research_outputs/s3_*log*.txt` filenames (there may be a third with an unguessed name) and to check that the new `research_outputs/s3/**` ignore rule doesn't fence the moved logs (run logs should stay tracked like the other phases').

### YOUR FIRST ACTION IN THE NEW CHAT
Ludwig will attach **screenshots of the builder's output** for the git pastes — most importantly the **last paste (Paste 4, the S-3 log move)** and the filename listing. **Verify:**
- Commits 1–3 landed with only their intended files (each had a `git status --porcelain` checkpoint that should show *only* the expected paths).
- The S-3 log listing shows the real filenames; confirm the third file's handling.
- The moved S-3 logs are **tracked** (not caught by the `research_outputs/s3/**` ignore rule) — if the ignore rule fences them, a `!research_outputs/s3/*log*.txt` (or equivalent run-log negation) is needed, matching how s1/s2/tc* run logs are handled. **Verify how the other phases' run logs are actually tracked before ruling** — do not guess the negation; ask the builder to show `git ls-files research_outputs/s1/ | grep log` or similar.
- Then **`git push`**, and confirm the branch is in sync with origin.

Give Ludwig the exact paste-ready commit line for Paste 4 once the filenames are confirmed. Keep the "verify before the rule, not after" discipline — it's the lesson of this whole cleanup.

## 6. THEN: CENSUS-1b — the next analytical artifact

Once the repo is clean and pushed, draft the **CENSUS-1b contract**. It is a **Tier-A addendum on the existing census substrate** (no re-run — the four `.jsonl` files totaling ~430k rows are on disk, sha-pinned in the committed manifest; runtime is minutes). Its job is to fix the units confound and produce the honest, decision-grade output the redesign needs. Deliverables:
- **Re-rank the continuation-moment trigger candidates (D4) and the cascade-ladder rungs (D8) in bps net-of-toll** at the captured horizons — the correct basis, replacing the ATR-denominated artifact. This produces the honest ranking of what could actually serve as a decoupled add trigger.
- **Pair D5 (the confluence-combination result) with its MAE** — the +597 bps net-of-toll figure has no downside partner yet; at regime-scale, MAE runs ~90% of MFE everywhere, so "clears the toll on peak excursion" is not yet tradeable. Make it tradeable-or-not with the MAE beside it.
- **Pooled-lens power analysis for the zone-landing outcome (P-C7b):** the mechanism (2× clustering) is proven, but the *outcome edge* (do EMA-terminating pullbacks lead to bigger moves?) was point-estimate-only, every confidence interval spanning zero, on thin slow-lens samples (n=215 and 103). Pool the lenses to test whether the outcome edge is real or just underpowered.
- **The D9 factor-decorrelation table:** the nine confluence factors are collinear (they mostly say "trend on" together — the k-distribution is bimodal), so the dose-response test was starved of independent variation. Decorrelate the factor list so the k-of-N framework (Ludwig's flexible-entry idea) gets a fair test.

Pre-register the addendum's predictions before running the re-score (it's Tier-A, but the discipline holds). Byte-identity to the existing substrate where applicable. Standing contract format.

**After CENSUS-1b:** the first **v12 logic candidate** (a Tier-C, pre-registered) gets designed from the two null-survived findings — entries/re-entries keyed to **slow-lens EMA-terminating pullbacks** inside a **trend-age window** from the maturation clock, with the **structural stop** and **regime-break exits**. That is the redesign beginning to take concrete shape.

## 7. Parked threads (queued, none blocking)

- **D-2 adoption ruling** — whether TC-1's arm B (structural stop) formally becomes the new reference architecture. Reviewer's lean: yes, with the ratcheting-structural variant as the next test.
- **TC-2** — the re-entry quality bar, now sharpened by S-3 and TC-5 (intraday's residual = per-trade expectancy over a long life).
- **SSv11.4 display report (Report 5)** — decisions D-SS-1..7 open: a display-only harvest of the research findings for Ludwig's *discretionary* TradingView chart (structural-stop line, payability readout, MTF dashboard, corrected tooltips). Kept separate from the v12 engine redesign. Includes a Law-4 rewording that needs Ludwig's own words.
- **S-1 / arm-A excursion back-fill** — a byte-safe re-emission to extend the cross-run substrate to the older runs (named in S-3).
- **The v12 logic ledger** — the accumulated list of engine changes routed to SSv12 (structural stop, timeframe re-pointing with a resolution-floor clause, MTF machinery specified in governor-relative steps, the decoupled add, re-entry bar, zone redesign).

## 8. The governance principle this cleanup reinforced (carry it forward)

**The repo holds source and the pinned hashes of derived data; it never holds opaque binaries, and it never holds a run whose inputs aren't regenerable from what's committed.** Completion commits must let a clean checkout reproduce the run. This is the lesson of the earlier S-2 provenance incident (`81b29f3`) and now the census cleanup. Every future contract should state it.

---

*Handoff prepared by the reviewer under Fable-mode, 2026-07-22. The immediate task is small and mechanical — verify one commit, push — but it must be done with the same verify-first care the whole session ran on. Then CENSUS-1b turns the census from "observed" into the redesign's actual entry/add/governor specification. The companion document (state-of-project report) explains the findings in full plain-language detail.*
