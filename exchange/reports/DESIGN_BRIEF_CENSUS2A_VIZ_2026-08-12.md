# DESIGN BRIEF · CENSUS-2A VISUAL EXPLORATION — "ENTRIES & EXITS, SEEN"
**From:** APOLLO (Project Naiad, reviewer of record) · **To:** the Claude Design session
**Date:** 2026-08-12 · **Class:** DISPLAY-ONLY / Tier-E exploration — nothing here is evidence;
every artifact carries the footer defined in §5. **Destined:** `exchange/reports/` (this brief) ·
renders to `D:/Naiad/research_outputs/census2a/viz/`.

## §1 · WHO YOU ARE IN THIS TASK, AND WHAT THE PROJECT IS
You are the visual designer for one session. The client is a discretionary crypto trader (no
programming background) whose mechanical research system — "Secret Sauce" — reads markets through
EMA crosses on multiple timeframes. A completed measurement campaign (CENSUS-2A) produced rich
data about how trades are born and die. **The engine's purpose is profitability; these visuals
exist to sharpen two sentences: "the system enters when ___" and "the system exits when ___."**
Every view must answer a money question printed in its corner. Inspiration lineage: the project's
prior "Cascade Atlas" and "Cascade Rewired" HTML reports — dense, self-contained, interactive,
honest. Surpass them in clarity; never in ornament.

## §2 · IRON RULES
1. **Payload-only.** You may plot ONLY numbers present in the attached JSON payloads. No invented,
   interpolated, or remembered values. If a payload lacks a field a view wants, omit gracefully
   and say so in the footer.
2. **Display-only.** No claims, no "significant," no verdict language. Descriptive titles;
   the money question as a question.
3. **The toll is always visible.** Every outcome axis shades the band ±[toll_lo, toll_hi] from
   the payload meta — profit smaller than cost must LOOK like what it is.
4. **Diverging palettes anchor at zero (or at the toll edge where stated); color = outcome,
   always; shape/size = structure.** Colorblind-safe. Log-time wherever lags span decades of bars.
5. **Provenance footer on every artifact** (§5 text, verbatim), including each payload's sha256
   from its own `meta` block.
6. **Self-contained HTML** (inline data ≤ payload sizes, no external fetches), one file per view
   plus one index. Interactivity welcome (hover detail, asset/direction filters); dependencies
   inlined.

## §3 · THE NINE VIEWS (payload name · schema essentials · the money question)
**V1 ARMING SKY** — `v1_armings.json`: per arming {asset, dir, displacement_atr, terminal_h100,
fate, stamp_score, window_bars}. Scatter constellation; x=displacement, y=terminal, glyph=fate,
halo=stamps, toll band shaded. *Q: where do profitable armings live — and is proximity to the
line really poison?*
**V2 RELAY RIVERS** — `v2_flows.json`: nodes+links {arming → trigger_class → seal_timing → fate →
outcome_bucket, count, median_terminal}. Sankey; thickness=count, color=median outcome; highlight
path flag `is_may26_analog`. *Q: which routes through the window carry the money?*
**V3 LAG CLOCK** — `v3_lags.json`: per trigger {class, lag_bars, terminal_h100, asset}; per seal
{lag_bars}. Polar spiral, angle=log-lag, radius=outcome. *Q: is there a golden hour inside the
window?*
**V4 KNOT→FAN CINEMA** — `v4_braid.json`: per asset, downsampled rank series of the six EMAs
{ts, ranks[6], knot_flag, fan_flag, fwd_h100}. Braid/ribbon; knots shaded, fan stretches tinted by
fwd return. *Q: once 200 and 300 clear the 500, do they really never look back — and is that
persistence paid?*
**V5 REFUSAL WEATHER** — `v5_weather.json`: episodes {kind: reclaim|accept, member, cells[-10..0]
= i-b refusal density}. Row-stacked heatmap, storm palette. *Q: what does the air look like before
a trap versus before a real breakout?*
**V6 TAIL GARDEN** — `v6_campaigns.json`: per campaign {mfe_r, mae_r, terminal_r, give_back_r,
n_reclaims, is_winner, asset}. Stem-glyph field sorted by MFE; winners lit; reclaim ticks on
stems; give-back as wilt shading. *Q: where does the +9.4R tail live, and what does giving it back
look like?*
**V7 CLOCK DUEL** — `v7_anchors.json`: per anchor {name, n, median, distribution_deciles[]}.
Aligned ridgelines, toll band through all. *Q: how much of our clock's edge survives the toll —
and who beats it?*
**V8 WALL SONAR** — `v8_sonar.json`: per arming {levels: [{family, dist_atr}]} + aggregate
{colocation_histogram}. Radial ping small-multiples + the aggregate emptiness. *Q: is confluence a
crowd — or one wall that matters?*
**V9 VERDICT TIDES** — `v9_tides.json`: per member {episodes: [{ts, verdict, depth_atr}]},
hysteresis runs. Tide chart per member. *Q: which close is calm water, and which is chop?*

## §4 · DELIVERABLES
`viz_index.html` (the gallery: nine cards, each with its money question) + `V1.html … V9.html`,
all self-contained, each ≤ ~2 MB target. A `DESIGN_NOTES.md` (≤1 page): what you chose and why,
plus anything the payloads couldn't support. Nothing else.

## §5 · MANDATORY FOOTER (verbatim, per artifact)
*"DISPLAY-ONLY · Tier-E exploration · CENSUS-2A payload {name} sha256 {sha} · evidence era
≤ 2024-07-01 · no claim is made or implied; promotion requires registration (see
CENSUS2A_CLOSEOUT_2026-08-12.md §5). Rendered by Claude Design, {date}."*

## §6 · FILES YOU WILL BE GIVEN (attach checklist for the operator)
Required payloads (produced by the extraction paste; each carries `meta{sha256, rows, source_parquet,
toll_lo, toll_hi}`): `v1_armings.json · v2_flows.json · v3_lags.json · v4_braid.json ·
v5_weather.json · v6_campaigns.json · v7_anchors.json · v8_sonar.json · v9_sonar… v9_tides.json`
from `D:/Naiad/research_outputs/census2a/viz_payloads/`. Context (read, do not plot from):
`CENSUS2A_CLOSEOUT_2026-08-12.md` (the domain + findings) · this brief. Optional inspiration
(style lineage only): the Cascade Atlas (`docs/history/atlases/`) and `Cascade_Rewire.html`.
**If any payload is missing, render the views you have and list the absent ones in DESIGN_NOTES —
never fabricate.**

— APOLLO · the pictures serve the sentences; the sentences serve the P&L.
