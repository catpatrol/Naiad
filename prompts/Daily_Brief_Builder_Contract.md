# Builder Contract — `scripts/daily_brief.py`
### The Naiad Daily Brief generator · OPS tier · drafted 2026-07-26, ratified by operator ("proceed as suggested, iterate later")

## §0 What this is
A tracked script that computes the operator's daily market report from the repo's own data estate and emits an Atlas-styled self-contained HTML plus a machine-readable JSON. **OPS artifact, Tier-0, decision-support for discretionary trading.** v1 scope below is deliberately buildable; iteration is expected.

## §1 The firewall (read first, it governs everything)
1. The brief consumes **live/current data**. That is legitimate for operations and **forbidden as study evidence**. Nothing this script computes may seed an engine rule, a study claim, or a pre-registration basis; rules are born only under G-7 on exploration-classic data.
2. The script **never reads trade journals** and **never computes signal-outcome or trade-outcome statistics on any window** — it reports market state, not strategy performance. Trailing indicators (e.g., 365d VWAP) will arithmetically include lockbox-era prices; that is display use, not rule evaluation, and is explicitly permitted. Computing per-signal forward outcomes on the lockbox window is explicitly prohibited.
3. Engine modules are imported **read-only** (`indicators`, `cells`, `signals` via the replay path with trading disabled). `signals.py`, `trading.py`, `cells.py` are not modified. Engine version untouched.

## §2 Data handling
- **Top-up first**: refresh klines for all 10 basket assets to the latest closed bar using the existing loader (LIT floor guard applies as built). Refresh funding series the same way. Record per-asset `last_bar_utc` in the JSON; any layer whose input is staler than one grid interval prints a ⚠ staleness chip instead of silently interpolating.
- **Funding grids are non-uniform** (SOL cadence switches; JTO/TAO 4h — per `DATA_CENSUS.md`). Integrate actual timestamped records; never assume 8h×3/day.
- All distances print in **both bps and ATR(14, 1d) multiples**, with the data timestamp.

## §3 Layers (v1)
**Tier 1 — from the existing estate:**
1. **Structure**: pivots per census convention pivot(5,5); prior D/W/M high-low; W/M/Q/Y open levels; distance table.
2. **Volume profile**: composites {prior day, 5d, 20d} from 1m klines (5m where 1m absent), bar volume spread uniformly across bar range; POC, VAH/VAL at 70%; **naked-POC registry** (untested POCs, 90d). Provenance chip: `approximation` (kline method, not tick).
3. **TPO**: 30m brackets from resampled klines; session + composite value areas. Same chip.
4. **VWAP complex**: rolling 7/30/90/365d on typical price (H+L+C)/3 **and** anchored W/M/Q/Y from period opens; ±1σ bands; distance to each. *(Both variants — [VETO default, ratified by "proceed as suggested"].)*
5. **MTF RSI**: RSI(14, Wilder) on {1h, 2h, 4h, 12h, 1d}: value, 50-side, slope; **divergences** regular + hidden via price-pivot vs RSI-pivot, pivot(5,5), last 2 pivot pairs per TF.
6. **Volatility regime**: ATR(14) percentile vs 1y per TF; RV 7d/30d ratio with expansion/compression flag.
7. **Funding posture**: current, 7d mean, percentile vs full asset history.
8. **Sessions**: Asia/London/NY ranges (00–08 / 07–16 / 13–22 UTC, printed so the convention is visible); which session drove the day's extension.
9. **BTC beta**: 30d correlation + beta per alt.
10. **Secret Sauce governor dashboard** (the spine): per asset × governor {1h, 4h, 12h} — regime direction, stage (1/2), active zone and proximity in gov-ATRs, age of last PRIME, whipsaw state. Computed by running the signal layer with `trading.enabled=false` on a trailing window (last ≈400 governor bars per lens). Intraday-lens rows use 5m exec via the tc5-style patched cell (precedent: `tc5_runner.py` monkey-patch; 5m-floor ruling) — [VETO default].

**Tier 2 — one Binance public fetch each:** 11. Open interest (level, 24h/7d Δ, percentile). 12. Basis/premium index. 13. Top-trader long/short ratio. 14. Next funding time + predicted rate. Fetch failures degrade to a ⚠ chip, never crash the brief.

**Tier 3 — reviewer-side (not this script):** economic calendar and headlines are added by the reviewer in chat via web search. The HTML reserves an empty "Calendar & events — added at review" panel.

## §4 Bias engine
- Each layer emits a vote {−1, 0, +1} per asset per horizon (daily, weekly) under **fixed rules printed in the JSON header** (v1 defaults: location = price vs M-VWAP and value area; momentum = 4h+12h RSI side/slope agreement; crowding = funding >90th pct votes against; trend = governor dashboard majority; volatility = compression mutes all votes to half-weight). Count-based, equal weights, **never fitted** (D9 discipline).
- The scorecard prints **every vote** so the operator can disagree line-by-line. Verdict bands: Long / Lean-long / Neutral-mixed / Lean-short / Short.
- **Every bias prints its invalidation** — the level or event that flips it. No invalidation, no bias printed.

## §5 Output & design
- `research_outputs/brief/brief_YYYY-MM-DD.json` (every number + inputs' timestamps + vote rules) and `brief_YYYY-MM-DD.html`.
- HTML: single self-contained file, no external requests, ≤ ~400 KB. Palette `--ink:#0E1420 --panel:#151D2C --rule:#26324C --tx:#C9D4E6 --mute:#7A8AA5 --warn:#E8853F --ok:#54C6A0`; fonts Space Grotesk / IBM Plex Sans / IBM Plex Mono (system fallbacks, no webfont fetch); narrative Atlas-voice section headings; verdict chips; per-claim provenance chips (`computed / fetched / approximation / stale`); sticky asset nav.
- **`.claude/commands/brief.md`** — a Claude Code slash command so the operator can type `/brief`: it runs the script and reports the two output paths and headline biases.
- `scripts/setup_brief_schedule.ps1` — optional: registers a Windows Task Scheduler job (`schtasks`) for a daily run at an operator-chosen time; prints how to remove it. Not run by default.

## §6 Fixtures
- **F-B1 recompute**: after emitting, independently recompute 3 published numbers (one VWAP distance, one VAH, one RSI) from raw klines inside the same run; assert equality.
- **F-B2 JSON↔HTML identity**: every numeric rendered in HTML is sourced from the JSON (build HTML from JSON only); spot-assert 10 sampled values.
- **F-B3 determinism**: on a frozen input day (fixture kline snapshot committed under `tests/brief_fixture/`), two runs byte-identical modulo `generated_utc`.
- **F-B4 funding grids**: SOL's cadence switches handled — assert per-record integration count matches the recorded timestamps, not 3/day.
- **F-B5 firewall audit**: script imports contain no `journal` module; grep of source proves no read of `research_outputs/**/journals`; no outcome joins exist.
- **F-B6 degradation**: with network fetches mocked to fail, the brief still renders with ⚠ chips on Tier-2 layers.

## §7 Deliverables
1. `scripts/daily_brief.py` + `tests/brief_fixture/` + `.claude/commands/brief.md` + `scripts/setup_brief_schedule.ps1` (committed).
2. One real sample day: both output files (paths reported; outputs dir already ignored — operator opens the HTML directly and may drop the JSON in the reviewer box).
3. Fixture transcript. Commit message: `ops: daily_brief v1 (F-B1..6 pass) — Atlas-styled market brief + /brief command`. **Commit, do not push.**

## §8 Verdict criteria
PASS = 6/6 fixtures + sample HTML opens locally and renders all Tier-1 layers for all 10 assets + reviewer spot-recomputes 3 numbers from the JSON's recorded inputs. FAIL on any → halt, report, no partial adoption.

## §9 What this phase is not
Not a signal service, not sizing advice, not study evidence, not a backtest. No Tier-C is created or implied. The bias engine's vote rules are v1 defaults explicitly expected to be re-ratified after the operator has lived with the report for a week.
