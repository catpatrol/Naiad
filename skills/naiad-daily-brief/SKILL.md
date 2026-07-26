---
name: naiad-daily-brief
description: Produce or review the Naiad daily market brief — an Atlas-styled HTML report covering price structure, volume profile / TPO value areas, rolling and anchored VWAP distances, multi-timeframe RSI and divergences, funding/derivatives posture, the Secret Sauce cascade dashboard, the economic calendar, and a scored daily + weekly bias. Use whenever the user says "daily brief", "morning report", "market report", "bias today", asks what the market looks like today, or drops a brief JSON/HTML into the conversation. Also use when designing, amending, or verifying the brief pipeline. If the builder-side generator does not exist yet, this skill's bootstrap section issues the build contract.
---

# Naiad Daily Brief

A decision-support report for the operator's discretionary trading, in the visual language of the Cascade Atlas. It is an **operations artifact, firewalled from the v12 study**: it consumes live/current data, which is fine for trading decisions and forbidden as study evidence. Nothing in the brief may seed a study rule without independent pre-registration under G-7 on exploration-classic data.

## Architecture (two halves, honest about who can compute what)

- **Builder half (all heavy computation).** Claude-in-chat has no market-data network access; the repo already has the Binance USDT-M pipeline, klines 1m–12h, funding series, and `indicators.py`. Therefore a tracked script, `scripts/daily_brief.py`, computes every quantitative layer from a fresh kline top-up and emits two files into `research_outputs/brief/`: `brief_YYYY-MM-DD.json` (every number, machine-readable) and `brief_YYYY-MM-DD.html` (the Atlas-styled render). One paste runs it; Windows Task Scheduler (`schtasks`) can automate it daily.
- **Reviewer half (this skill).** When the JSON (preferred) or HTML lands in chat or the box: verify internal consistency (spot-recompute ≥3 numbers from the JSON's embedded inputs), add the **calendar & events layer via web search** (the one layer the builder can't do reliably/licitly by scraping), write the **bias synthesis** over the mechanical scorecard, and flag any layer whose data looks stale (every layer carries its data timestamp; staleness > 1 grid interval = flag, don't interpolate).

## Layers (v1 scope; each row prints value, distance in bps AND ATRs, and data timestamp)

**Tier 1 — computable today from the existing estate:**
1. **Price structure** — swing pivots per the census convention (5,5), prior day/week/month high-low, weekly/monthly/quarterly open levels, distance to each.
2. **Volume profile** — composite {prior day, 5d, 20d}: POC, VAH/VAL (70% value area), and a **naked-POC registry** (untested POCs, 90d lookback). Method: volume-at-price from 1m klines (5m where 1m absent), bar volume distributed uniformly across bar range. *Stated honestly as the standard kline approximation — not tick data.*
3. **TPO** — 30-minute brackets built from 30m-resampled klines; letters = periods touching each price bin; value area + POC per session and composite. Same approximation caveat.
4. **VWAP complex** — rolling 7d/30d/90d/365d on typical price (H+L+C)/3, **plus** anchored W/M/Q/Y from period opens (both are cheap; "rolling" as literally requested, anchored because it is the standard desk tool). Distance to each; band = ±1σ.
5. **MTF RSI** — RSI(14, Wilder) on {1h, 2h, 4h, 12h, 1d}; per-TF: value, 50-line side, slope; **divergences** regular + hidden, price-pivot vs RSI-pivot using pivot(5,5), last 2 pivot pairs per TF.
6. **Volatility regime** — ATR(14) percentile vs 1y per TF; realized-vol 7d/30d ratio (expansion/compression flag).
7. **Funding posture** — current rate, 7d mean, percentile vs asset history (the data already exists per `DATA_CENSUS.md`; integrate actual timestamps — the grid is NOT uniform: SOL switches cadence, JTO/TAO are 4h).
8. **Session decomposition** — Asia/London/NY ranges and who drove the day's extension.
9. **BTC beta** — 30d correlation and beta for each alt vs BTC.
10. **Secret Sauce cascade dashboard** — per asset × mandate: governor regime direction, stage (1/2), active zone and proximity in gov-ATRs, age of last PRIME, whipsaw state. Computed by running the signal layer (signals-only, trading disabled) on the recent window. *This is the bridge layer between the study and the screen — the report's spine, not an afterthought.*

**Tier 2 — one new fetch each (builder has network; Binance public endpoints):**
11. Open interest (level + 24h/7d change, percentile). 12. Basis / premium index. 13. Top-trader long/short ratio. 14. Next funding time + predicted rate.

**Tier 3 — reviewer-side or manual (licensing/reliability limits):**
15. **Economic calendar** — today + week ahead: FOMC/CPI/NFP-class releases, crypto-specific events (unlocks, upgrades, ETF flows), added via web search at review time with sources cited. 16. Major headlines affecting the basket. 17. *(deferred candidates: options DVOL/max-pain for BTC/ETH; exchange-flow on-chain; CVD from aggTrades — each named, none in v1.)*

## Bias engine (mechanical first, narrative second)

- Every layer emits a **vote** {−1, 0, +1} per asset per horizon (daily, weekly) under fixed, pre-ratified rules (e.g. price above M-VWAP AND above VAH → +1 location vote; RSI 4h/12h both >50 rising → +1 momentum vote; funding >90th percentile → −1 crowding vote). Weights are **count-based and ratified by the operator before first live use — never fitted** (D9's falsification of fitted confluence applies here in spirit).
- Scorecard prints every vote so the operator can disagree with any line.
- Verdict bands: Long / Lean-long / Neutral-mixed / Lean-short / Short, daily and weekly.
- Every bias states its **invalidation**: the specific level or event that flips it ("above X the short bias is wrong"). A bias without an invalidation is not printed.
- The reviewer's written synthesis may dissent from the scorecard, but must say so and say why.

## Design language (inherit the Atlas exactly)

Single self-contained HTML, no external requests. Palette: `--ink:#0E1420 --panel:#151D2C --rule:#26324C --tx:#C9D4E6 --mute:#7A8AA5 --warn:#E8853F --ok:#54C6A0`. Fonts: Space Grotesk (display), IBM Plex Sans (body), IBM Plex Mono (all numbers). Narrative section headings in the Atlas voice ("Where price is paying rent", "Who's crowded"), verdict chips, per-claim provenance chips (`computed` / `fetched` / `searched` / `approximation`), sticky asset nav. Target ≤ ~300 KB.

## TradingView parity (the report and the chart must reconcile)

The layout mirrors the report layer-for-layer so any number can be checked on screen: anchored VWAP (built-in, W/M/Q/Y anchors) + a rolling-VWAP script for the 7/30/90/365d lines; fixed-range + visible-range Volume Profile and the TPO study for value areas; RSI(14) panes at the five TFs; session boundaries and W/M opens via built-ins. **Parity ritual:** each day, spot-check three numbers (one VWAP distance, one VA edge, one RSI) report-vs-chart; tolerance = rounding + one bar of staleness; a persistent mismatch is a bug report, not a shrug — F-BYTE culture applied to operations. Parameter parity is part of the spec: same lengths, same anchor conventions, same price basis, listed in the JSON header.

## Bootstrap (if `scripts/daily_brief.py` does not exist)

Issue the build as a standard builder contract: invariants (engine untouched; signals imported read-only; live-data firewall clause; every number carries units + timestamp), numbered fixtures (F-B1 recompute three published numbers from raw klines inside the run; F-B2 JSON↔HTML value identity; F-B3 determinism on a frozen input day; F-B4 funding-grid handling proven on SOL's cadence switches), deliverables (script + one sample day's JSON/HTML), and a "what this is not" section (not study evidence, not a signal service, no sizing advice). Draft goes to the operator for ratification before any paste.

## Review checklist (when a brief arrives in chat)

1. Timestamps fresh? 2. Spot-recompute 3 numbers. 3. Any layer stale or absent → flag, never silently omit. 4. Add calendar/events with citations. 5. Bias synthesis with explicit invalidations. 6. One-line delta vs yesterday's brief ("what changed"). 7. Keep total reviewer commentary under ~300 words — the report carries the detail.
