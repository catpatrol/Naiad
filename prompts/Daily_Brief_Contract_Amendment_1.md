==================== AMENDMENT 1 — Daily Brief Builder Contract ====================
Ratified 2026-07-26 by operator paste (D1–D6). Extends prompts/Daily_Brief_Builder_Contract.md; where they conflict, this amendment wins. Purpose recap: (P1) daily discretionary decision support ending in an actionable-setups summary per the SSv11 playbook; (P2) capture of confluence layerings to feed hypothesis generation; (P3) the brief is designed from day one as a durable, searchable, self-describing daily archive.

A1.1 — Firewall clause 4 (append to §1):
"4. HYPOTHESIS-MINE CLAUSE. The brief's accumulated archive (daily JSON snapshots + brief_index.jsonl) is an operations journal. It MAY be mined for hypotheses; any resulting rule change still enters the study only through G-7 pre-registration and is scored only on exploration-classic data. The archive itself is never a scoring window. Computing signal-outcome or trade-outcome statistics on the archive — including how radar-flagged setups subsequently performed — remains prohibited under clause 2. A forward-validation protocol (scoring pre-registered predictions on post-registration data) would be a separate governance act; none exists."

A1.2 — New Tier-1 layers (Tier-2 renumbers to 13–16):

LAYER 11 — SETUP RADAR (the SSv11.0.2 playbook state machine as a table; D2: v11 semantics only, no v12 study content).
Per asset x lens {1h, 4h, 12h} (intraday/swing/position framing), computed from the layer-10 signal run (same trailing window, trading disabled; 1h lens uses the 5m-exec patched cell per gate item iii):
  STATES (exactly the playbook §3 machine):
    DORMANT        — no live campaign (dir = 0).
    ARMED          — campaign live (tier full|provisional), price outside all armed bands.
    ZONE_ACTIVE    — price inside an armed band; name it (Z1|Z2|Z3). Armed-band logic per v11.0.2: Z1 and Z2 arm with EVERY live campaign, provisional included; Z3 only when stage-aligned (stage 2). Read zone half-widths from the same parameters the signal layer uses (v11 defaults Z1 ±0.25, Z2 ±0.35, Z3 pad ±0.35 gov-ATR) — do not hardcode independently.
    ENTERED        — live ratchet stop line present at the latest bar (out_sl/out_ss non-NaN); report last entry grade and current stop level.
    DEFENSE        — ENTERED and a TPW event within the last 12 exec bars on that lens.
    POST_X         — X (failure) event within the last 10 governor bars: stand-aside note ("never negotiate with an X").
  ROW FIELDS (every row): state; dir; stage (1|2); tier (full|provisional); active-or-nearest armed zone + distance in bps AND gov-ATR; whipsaw-arrow-hidden flag (arrows suppressed, arming unaffected — print so the operator trusts tint over arrow); age + grade of last PRIME; last event type/age; live stop level if ENTERED; INVALIDATION (mandatory): setup invalidation = active zone's far edge; campaign invalidation = far governor band edge (the X reference level); and a one-phrase "needs next" hint (e.g. "needs: zone tag", "needs: stage confirm for Z3").
  Provisional-tier rows carry a static doctrine chip quoting playbook §5.5 ("half size, Z1/Z2 only, grade ≤ B") — quoted doctrine, never a computed size. NO sizing fields exist anywhere (F-B7).
  Cold-start: if a lens window contains no governor cross yet, print a cold_start chip instead of trusting dir=0.
  Placeholders printed in the JSON rules header, re-ratified after ~1 week of use (D3): watch_proximity_gov_atr = 1.0; post_x_window_gov_bars = 10.

LAYER 12 — POINTS OF INTEREST. Fixed detectors over already-computed layers, each with a printed rule id and its numbers; ranked by a fixed severity table (printed in JSON); cap 12 overall, grouped per asset:
  POI-1 funding percentile ≥90 or ≤10 · POI-2 RSI divergence (regular or hidden) on 4h or above · POI-3 naked POC within 1.0 daily-ATR of price · POI-4 price crossed an anchored VWAP (M/Q/Y) within the last 24h · POI-5 compression flag ≥5 consecutive days · POI-6 session extension >1.5x the 20d median session range · POI-7 OI 24h-change percentile ≥90 (Tier-2; degrades) · POI-8 radar state changed vs the previous index line (skip on first run).

A1.3 — ACTIONABLE SUMMARY (HTML section directly under the masthead, and mirrored at the foot; D6):
  "Actionable now": all ZONE_ACTIVE rows, full-tier first, provisional flagged; then ENTERED/DEFENSE rows as "manage per §5–§7".
  "Watch": ARMED rows whose nearest armed band is within watch_proximity_gov_atr.
  "Stand aside": POST_X rows, one line each.
  Each line: asset · lens · dir · state · zone + distance · invalidation. Empty state prints exactly: "No playbook-valid setups today — standing aside is a position."
  Bias verdicts render adjacent but visually separate; when radar direction and bias verdict disagree for an asset, print a disagreement chip — never reconcile silently (radar = playbook mechanics; bias = market context).

A1.4 — CONFLUENCE FLAGS (P2 capture instrument; D3). Per asset per day, a fixed boolean dictionary, stored in JSON and rendered as chips. v1 dictionary (exactly these 18): above_M_vwap, above_Y_vwap, in_prior_day_value, above_VAH, below_VAL, naked_poc_above_1atr, naked_poc_below_1atr, rsi4h_bull_side, rsi12h_bull_side, rsi_div_bear_active, rsi_div_bull_active, funding_p90_plus, funding_p10_minus, gov4h_long_regime, gov12h_long_regime, stage2_4h, compression_flag, oi_surge_p90. Dictionary changes require a contract amendment and a rules_version bump — archive comparability depends on it.

A1.5 — ARCHIVE & RETRIEVAL (P3; D4).
  Snapshots: research_outputs/brief/brief_YYYY-MM-DD.{json,html} — untracked (data-estate precedent; OneDrive is the persistence layer; the standing OneDrive integrity risk is acknowledged, mitigated by per-day hashes below).
  Index: research_outputs/brief/brief_index.jsonl — one line per date; a same-date re-run REPLACES that date's line. Line schema: {date, generated_utc, script_version, rules_version, rules_sha256, json_sha256, per_asset: {daily_verdict, weekly_verdict, radar_best_state, poi_count, flags_true:[names]}, staleness:[...]}. json_sha256 computed via Python hashlib binary read (never shell tools — msys hazard).
  Self-description: every JSON embeds the complete rule set that produced it (bias rules, radar placeholders, POI severity table, confluence dictionary, staleness table) under a rules header with rules_version.
  scripts/brief_lookup.py: filters --date --from --to --asset --state --flag --verdict --text; prints matching index lines + full file paths. Contains no outcome joins of any kind (clause 4). .claude/commands/brief-history.md wraps it as /brief-history.

A1.6 — BIAS-ENGINE CORRECTIONS (applied before first run; D5):
  (a) Volatility no longer half-weights votes (contradicted count-based purity): the compression flag instead demotes the final verdict one band toward Neutral-mixed.
  (b) Crowding symmetric: funding ≥ p90 votes −1; funding ≤ p10 votes +1.
  (c) Staleness defined per layer: a table in the JSON rules header maps each layer to its native reference TF; input older than one such interval prints the ⚠ chip.
  (d) All rolling AND anchored VWAPs computed on 1h klines, typical price (H+L+C)/3, volume-weighted. Pinned.

A1.7 — FIXTURES (adds to F-B1..6; F-B3 clarified: the frozen fixture day includes canned Tier-2 responses so determinism covers the whole artifact):
  F-B7 RADAR/NO-SIZING: within the run, independently recompute every radar row's state from the layer-10 arrays and assert equality; assert the JSON contains no key matching size|qty|notional|leverage|contracts.
  F-B8 INDEX ROUND-TRIP: rebuild the sample day's index line from its JSON alone and assert byte equality; verify json_sha256 by binary re-read; run one brief_lookup.py query and assert it returns the sample day.

A1.8 — DELIVERABLES (supersedes contract §7 list): scripts/daily_brief.py · scripts/brief_lookup.py · tests/brief_fixture/ (incl. canned Tier-2) · .claude/commands/brief.md · .claude/commands/brief-history.md · scripts/setup_brief_schedule.ps1 · prompts/Daily_Brief_Contract_Amendment_1.md · the ledger entry below appended to LEDGER.md · one real sample day generated (files reported, untracked). Completion commit contains every file required to reproduce from clean checkout (standing rule). Commit message: "ops: daily_brief v1.1 (F-B1..8 pass) — Atlas brief + setup radar + archive/index + /brief + /brief-history". Commit, do not push. Then run scripts/reviewer_manifest.py and place the fresh MANIFEST.json in _reviewer_box/.

LEDGER ENTRY (append verbatim, then add your completion bullet beneath it with fixture results, sample-day paths, HTML byte size, per-asset VP substrate used, runtime, and commit hash):
"## 2026-07-26 — Daily Brief v1.1 build launched (Amendment 1: setup radar, archive, hypothesis-mine clause)
- Amendment 1 filed at prompts/Daily_Brief_Contract_Amendment_1.md; operator ratified D1–D6 by routed paste. Firewall gains clause 4 (archive = hypothesis mine, never a scoring window; radar-outcome tracking prohibited; forward-validation would need separate governance). New: Setup Radar (SSv11.0.2 playbook state machine, no sizing) + Points of Interest + actionable summary + 18-flag confluence dictionary + brief_index.jsonl + brief_lookup.py + /brief-history. Bias-engine corrections A1.6. Fixtures F-B1..8. Commit-no-push."

A1.9 — VERDICT (supersedes contract §8): PASS = 8/8 fixtures + sample HTML opens locally rendering all Tier-1 layers including the radar for all 10 assets + every radar row prints an invalidation + reviewer spot-recomputes 3 numbers from the JSON's recorded inputs. Any FAIL → halt, report, no partial adoption.

A1.10 — WHAT THIS IS NOT (extends §9): not a signal service — the radar reports playbook STATE under printed rules and the operator owns every trade decision; no sizing, no alerts/notifications in v1, not study evidence, no Tier-C created or implied; radar/POI thresholds and the confluence dictionary are v1 placeholders expected to be re-ratified after the operator has lived with the report for about a week; no radar-outcome scoring, ever, absent a separately ratified forward-validation protocol.
==================== END AMENDMENT 1 ====================
