# HANDOFF — BRIEF lane → ENGINE lane · 2026-07-27
Author: Claude (Project reviewer, BRIEF chat, Fable-mode) · For: ENGINE Claude · Relay: operator via project box
Purpose: make the ENGINE lane aware of a parallel workstream that now touches the repo daily. Zero BRIEF-context assumed. Provenance tags per project convention: [verified] independently recomputed · [ledger] on the append-only record · [ratified] operator ruling · [open] unresolved.

## 1. What this workstream is
The Daily Brief is an OPS-tier artifact: a script (`scripts/daily_brief.py`) that computes the operator's daily market report for his ten-asset basket from the repo's own kline/funding estate plus four public Binance fetches, emitting a machine-readable JSON and an Atlas-styled HTML. It exists for **discretionary trading decision support and daily data capture** — explicitly NOT study evidence. Firewall (4 clauses, printed inside every artifact) [ratified]:
1. Live data is operations-only, forbidden as study evidence; rules are born only under G-7 on exploration-classic data.
2. The script never reads trade journals and never computes signal- or trade-outcome statistics on any window.
3. Engine modules are imported read-only with trading disabled; `signals.py` / `trading.py` / `cells.py` untouched.
4. Hypothesis-mine clause: the accumulating archive MAY seed hypotheses; it is NEVER a scoring window; radar-outcome tracking is prohibited; a forward-validation protocol would be a separate governance act (none exists).

## 2. State of record (what has already landed in the shared repo)
- v1.1 build complete: `scripts/daily_brief.py`, `scripts/brief_lookup.py`, `/brief` + `/brief-history` commands, fixtures F-B1..F-B8 all PASS; commit **76cc314** (11 files, 3,372 insertions) [verified — builder fixture transcript].
- Hygiene commit **60e00c9b**: `.gitignore` +2 (brief outputs + fixture out), `reviewer_manifest.py` SOURCES +2 (`daily_brief.py`, `brief_lookup.py`), LEDGER entry appended. Branch `v12-v1-census`, **ahead 4, NOT pushed** as of that commit [verified].
- Reviewer acceptance completed 2026-07-27 on the real sample day `brief_2026-07-27.json` (sha256 78f264d4…): 15 independent checks PASS — index↔JSON round-trip, 20/20 bias verdicts reproduced from printed rules, 120 confluence-flag assertions, 120 distance recomputations, 30/30 radar invalidations, zero sizing keys [verified]. Raw indicator values were NOT re-derived in chat (no klines there); that leg rests on builder F-B1 plus an out-of-band second implementation [open by design].
- The brief's signal runs report **engine_version 1.0.11** — consistent with the ENGINE lane's frozen-version record; no discrepancy [verified].
- MANIFEST ritual honored: fresh `_reviewer_box/MANIFEST.json` produced at each completion (last: 46 sources, F-M1..4 PASS) [verified].

## 3. ENGINE-relevant flags — the part to actually read
1. **LIT floor contradiction [open — escalated, estate-side, EVIDENCE-relevant].** Charter invariant I1 fixes LITUSDT's first valid candle at **2025-12-23 00:00 UTC** (Lighter listing; earlier history = Litentry, a different asset). The brief's bar counts imply klines beginning **2025-12-01** (239×1d, 5,700×1h back-solve exactly to it), while LIT **funding** history starts 2025-12-23T20:00Z — matching the charter, not the klines. A status doc records the floor as 2025-12-01 "[verified]", so the project currently holds two floors in two places and the estate follows the looser one. The same back-solve method reproduces BTC's first bar as 2019-09-08 dead-on, so the method is sound. One-line check: print the first kline open-time per interval for LITUSDT and reconcile against I1. This belongs to ENGINE/SYSTEM because it is estate integrity, not display.
2. **Repo cadence changes now ratified [ratified 2026-07-27, D-B9/D-B10].** Daily captures move to a new **tracked** folder `briefs/` (JSON ≈250–400 KB/day raw; realistic git growth ~15–30 MB/yr), and `/brief` **auto-commits** its own capture daily (fixed message, never pushes). Expect ordinary daily ops commits on `v12-v1-census` from now on; push batching stays operator-manual. Ahead-count will grow between pushes — not an anomaly.
3. **New tracked package `analytics/` incoming (ANALYTICS-1) [ratified].** Indicator recipes (RSI, StochRSI, AO, VWAP complex, ATR/RV, divergence detector, level clustering) extracted from the 2,760-line brief script into a small versioned toolbox — **deliberately OUTSIDE `engine/`** so ops iteration never shares a blast radius with frozen, hash-cited engine files. Every artifact prints `analytics_version`; future census work may import the same functions, entering the study only under G-7. Engine bytes remain untouched; F-SIG-style guarantees unaffected.
4. **Backup scope**: `briefs/` and `research_outputs/brief/` should join `backup_estate.py`'s scope under ruling R-B when that build happens [open].
5. **No engine changes requested.** The brief resamples its own 30m/2h/1d frames (engine has no such intervals); the 1h lens reuses the TC-5 cell-construction precedent read-only.

## 4. Today's re-scope and rulings (context for the dashboard)
Operator re-scoped the BRIEF lane to continuous improvement of the automated brief, anchored to his manual Notion review's grammar: **every layer produces levels → levels gain authority through confluence → the report ends in lines-in-the-sand and if-then trade hypotheses**. Interview D-B9..D-B16 ruled [ratified]:
- D-B9 tracked `briefs/` storage (JSON=record, HTML=disposable view, `brief_render.py` rebuilds any day) — yes.
- D-B10 auto-commit (no push) — yes. · D-B11 anchored VWAPs dev W/M/Q/Y + prior M/Q/Y with 1/2/3σ bands — yes.
- D-B12 composites + single-print/LVN detectors — **PARKED** on a methodological point worth recording: the operator's 10-week composite is a *conclusion* of analysis (a judgment about which balance areas merge), not a mechanical window; naive automation would counterfeit the judgment. Return-note filed; SP/LVN are separable and can lead when revisited; the real automation target is mergeable-balance detection.
- D-B13 TradingView-default recipes, parity-fixtured against TV — confirmed. · D-B14 operator-notes command (`/brief-note`, journaling into the capture) + auto-drafted mechanical scenarios — yes to both.
- D-B15 scheduled run 11:00 America/Argentina (14:00 UTC, no DST); daily metrics anchor on the last complete day regardless. · D-B16 hand-maintained state-only `ops/positions.yaml` (no P&L ever — firewall clause 2).
A reviewer-side **confluence-engine prototype** was computed today from the real snapshot (level registry → 0.15-ATR clustering → count+diversity scoring → lines in the sand) and is the reference behavior for the next contract. Two standing process rules were also adopted lane-wide [ratified]: decision-tree contracts with plain-language interviews at true forks only, and machine-readable handbacks into `_reviewer_box/` instead of screenshots.

## 5. Next in this lane
Reviewer issues the single combined go-paste (ANALYTICS-1 + confluence engine + storage migration + accepted gap fixes) to the LOCAL builder; no operator input pending. After that build: first tracked capture, then daily cadence begins.

— end of handoff. Questions route through the operator or the ORCHESTRATOR dashboard; chats cannot read each other.
