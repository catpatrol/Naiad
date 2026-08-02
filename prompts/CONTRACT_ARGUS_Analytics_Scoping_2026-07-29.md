# CONTRACT — ARGUS · Analytics Toolkit Scoping & Design Interview
**From:** APOLLO (reviewer chat, formerly ENGINE) · **To:** ARGUS (formerly BRIEF) — a fresh session
**Date:** 2026-07-29 · **Operator:** Ludwig · **Status of this doc:** priming contract; supersedes nothing on the ledger; extends STATUS_HANDOFF_BRIEF_2026-07-28

---

## 0 · Who you are now

The chat lane formerly titled BRIEF is renamed **ARGUS** — the all-seeing watcher. Your STATUS blocks emit as `=== STATUS_ARGUS — <date> ===` from now on; note the rename in your first block so the ORCHESTRATOR re-files the lane. Your scope, per operator ruling 2026-07-29: **the analytics toolkit, the daily brief, and the new multiTF volume filter** described in §3. The reviewer for your contracts remains the APOLLO chat; the operator remains the only merge authority; the builder remains local Claude Code on the operator's PC.

Everything in this contract is context you must ingest before doing anything. Your **first and only immediate task is §4: the scoping interview.** Do not build, do not commit, do not fire pastes until the operator has answered it.

## 1 · Where the analytics work actually stands (state of record)

- `analytics/` **v1.0.0 exists on disk, uncommitted, unadopted** — nine modules (vwap, volume profile, structure, levels, stats, momentum, et al.), sha `86657c9b…`, `imports_engine=false`, with `tests/test_analytics.py` alongside. Untracked in git; visible in the repo porcelain.
- Fixtures **F-AN-1..7 and 9..14 PASS**. **F-AN-8 FAILED 12/21 and the halt was correct**: the regression guard proved the v1.1 *brief* computed every 4h/12h/1d resampled layer over one extra **unfinished candle** (six of six resampled pairs off by exactly −1 bar; native 1h exact). Every published 4h/12h/1d RSI, ATR-percentile and both momentum votes were computed on partly-formed data.
- **Operator ruling, ratified:** drop the unclosed bar; closed-bar convention wins. The amendment restructures F-AN-8 into **8a** (unchanged conventions reproduce exactly), **8b** (a legacy mode reproduces v1.1 *exactly*, proving the dropped bar is the only change), **8c** (documented diff of every changed published value, since both bias votes are downstream). The amendment paste was drafted in the old BRIEF session and was never fired — **re-issue it fresh from your own session**; do not assume any prior paste reached the builder.
- **Adoption gates (both, no shortcuts):** (i) full fixture suite green including 8a/8b/8c; (ii) the operator's ~28-reading TradingView parity worksheet. The **no-partial-adoption clause** stands: nothing consumes `analytics/` numbers until both gates pass. Downstream consumers waiting on you: CENSUS-2b, CENSUS-1d, H-RVX (all APOLLO-side).
- **Caveat carried honestly:** F-AN-13 clears the extracted toolbox of the one-sided-window hazard; the brief's orchestration layer that Phase II rewrites is not yet cleared.
- **Standing invariants that bind everything you design:** the live-data firewall (brief output is ops display, never study evidence); "a rolling window is a silent lockbox-spending mechanism" — any historical computation on exploration-classic data is legitimate census work, but backfilled output never enters `briefs/`; D-B27 (backfill rule) and the D-B17 RVWAP pin (official TradingView Pine, now in the project box as `Rvwap_pine_code.txt`) remain in force.

## 2 · Why you exist, in the operator's frame

The operator's discretionary method has a mechanical half (where the levels are, which tools agree at each price, regime per timeframe) and a judgment half (what it means, whether to take it). Your job is the mechanical half — and as of today it has a sharper purpose: **the analytics toolkit is project-wide infrastructure**, a knowledge base every lane can eventually draw on, not a brief-only convenience. APOLLO's confluence work (CCL walls, H-RVX, value-area layers in the census) will consume your outputs *after* the adoption gates. Design everything with that dual customer in mind: the operator's daily eye, and the census's measurement machinery.

## 3 · The new commission (operator, 2026-07-29, verbatim intent)

A **toggleable volume-weighted filter** for Secret Sauce readings:

- **Rolling VWAP at four windows: 7, 30, 90, 365 calendar days** — fixed time-period mode, not the Pine's auto mode. The pinned reference implementation is the official TradingView RVWAP Pine (in the box): source `hlc3`; σ-bands computed as volume-weighted variance `E[x²] − E[x]²` clamped at zero (NOT a plain stdev of price — this distinction is why the Pine was pinned); a minimum-bars floor (`minBarsInput=10`) protects gap regions. Note the 365-day window implies ~1 year of warmup before the first honest value.
- **Volume profile over the same four trailing windows** (the operator says "anchored volume profile 7/30/90/365D" — in standard vocabulary these are *trailing/rolling-window* profiles, not event-anchored ones; pin this terminology in the interview so no one builds the wrong object).
- **Superimposed on 4H / 1D / 1W / 1M charts**, hunting **volume-based value areas** that furnish both HTF and LTF actionable levels — support/resistance, supply/demand — and studying how those levels interact with the SS EMA signal generator.
- **A daily tool**: on command, an **HTML report** that lays down this volume filter *plus* computes **and analyzes** RSI, Stoch RSI, MACD, and the other indicators already in the brief (divergences, ATR-percentile regime, funding/OI posture, sessions).
- **Toggleable** is a design requirement, not a UI nicety: the volume layer must be separable so SS-native readings and volume-filtered readings can be compared side by side. APOLLO's census will run exactly that comparison later.

## 4 · Your first task: the exploratory scoping & design interview

Produce, for the operator, a **funnel-type decision interview** — big questions first, details cascading below — with, at every gate, in plain language and assuming **no technical background**: (1) why this decision is required; (2) the conceptual meaning of the decision and of the action it commissions; (3) every available option including your recommendation; (4) the implications of each option — what happens if we do, what happens if we don't. One-word answerable wherever possible. Mine your own lane history for the operator's presentation preferences before writing it.

Axes the interview must cover (add what you find missing; do not silently drop any):
1. **Object definitions:** window semantics (calendar days vs bars; UTC day boundary); VP binning (price-bucket size in ATR or %), value-area percentage (70%? measured?), POC/VAH/VAL vocabulary; which source series; how the four windows nest.
2. **Chart-plane composition:** which of 4H/1D/1W/1M carries which windows; how many levels per report before it stops being readable; level-authority scoring when RVWAP bands, VP edges and prior levels agree (counted, never weighted — project law).
3. **Indicator suite:** exact list beyond RSI/StochRSI/MACD; divergence definitions; closed-bar convention everywhere (the F-AN-8 lesson is the founding law of this toolkit).
4. **Report & cadence:** on-command HTML now — same Atlas style? printed rule set + `rules_version` + sha embedded per capture (self-describing record, JSON as the record, HTML disposable)? relationship to the existing daily brief v1.1 (extend it, or a second report?).
5. **Firewall tagging:** per feature, display-only vs evidence-capable; how a census-side consumer will read your outputs without touching live data.
6. **The adoption path:** fire the F-AN-8 amendment; parity worksheet plan (which ~28 readings, which chart setups — the operator does these by hand on TradingView); what "adopted" unlocks, in what order.
7. **Interface for APOLLO:** what files/JSON schema the census will consume (levels + value areas as timestamped series), so census contracts can cite a stable interface rather than your internals.
8. **Build phasing:** smallest first shippable slice; what stays parked.

## 5 · Rules that bind your sessions (unchanged unless noted)

Paste-go discipline: routing line above every paste; hard environment assertion that halts before any write, read-only pastes included; G-11 explicit destination filenames; G-12 self-contained pastes + one Builder's Report per outcome. **New standing rule (operator, 2026-07-29): at every completed builder cycle, the builder displays on screen the exact filenames the operator must carry to the reviewer chat and the exact repo directory path of each, filenames highlighted in bright colors.** Decision gates follow the presentation rule in §4 — that rule is now project-wide. Commit-no-push remains; pushes only on explicit operator authorization. Live-data firewall in every feature fact you emit ("[display-only]" vs "[evidence]").

## 6 · What NOT to do

Do not build before the interview is answered. Do not import the engine. Do not read the lockbox or let any rolling computation graze it. Do not treat this contract as license to fire old pastes from the dead BRIEF session — re-issue fresh. Do not adopt `analytics/` partially. Do not present the operator a decision without the full context format.

## 7 · First message checklist for your session

Confirm ingestion of this contract → state your lane rename in a STATUS_ARGUS block → verify the box copies you need (`Rvwap_pine_code.txt`, `STATUS_HANDOFF_BRIEF_2026-07-28.md`, `CONTRACT_v4_ANALYTICS1_BRIEF2_FORWARD0.md`, `Daily_Brief_Builder_Contract.md`) → then deliver the §4 interview. Nothing else.

— APOLLO, reviewer of record, 2026-07-29
