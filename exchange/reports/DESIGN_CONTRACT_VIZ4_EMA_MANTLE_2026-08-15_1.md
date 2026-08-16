# DESIGN CONTRACT · VIZ-4 — "THE EMA MANTLE"
**From:** APOLLO (Project Naiad) · **To:** the Claude Design session · **Date:** 2026-08-15
**Class: DISPLAY-ONLY / Tier-E.** Iron rules of the VIZ-3 contract apply verbatim (payload-only ·
no verdict language · toll bands on outcome axes · dark-mode legible · self-contained HTML, CDN
deps only · provenance footer per artifact · DESIGN_NOTES.md). Supersedes nothing; sits beside
the Cathedral in DESIGN_HANDOFF_VIZ4/.

## §1 · THE METAPHOR, WHICH IS ALSO THE SPEC
The eighteen EMAs are one fabric. The **slow edge (5000) is the rod** — the attachment, heavy,
barely swaying. The **fast edge (12) is the hem** — massless, whipped by every gust. Between them
sixteen threads of increasing inertia. Price is the wind. **Noise is a hem-flutter that dies by
the third fold; a regime change is a wave that climbs the whole fabric until the rod itself
moves.** The client trades the difference. Build him the instrument that shows it.

## §2 · DELIVERABLES
**M1 · THE MANTLE (centerpiece — interactive 3D).** A cloth surface: **x = time · y = EMA length
(log scale, 12 at the hem → 5000 at the rod) · z = displacement (ema − price)/ATR**, colored by z
(diverging, zero-anchored). Time scrub; camera orbit; hover any point → panel {thread length,
time, displacement, thread velocity}. Knot episodes = the fabric pinching flat (render the pinch);
fan-complete = full pleat. three.js; graceful 2D heatmap fallback (same axes, z as color).
**M2 · THE ECHO TRACE.** For the same window: rolling lagged correlation between hem-edge
velocity (mean of 12/26 thread dz/dt) and rod-edge velocity (mean of 2618–5000 threads), lags 0…L
from the payload. Render as ripples on a still pond beneath the mantle or as a lag×time heat
strip: **when does the hem's motion arrive at the rod, and how attenuated?** Mark the payload's
knot→fan transition timestamps on the time axis — the eye should be able to ask "did an echo
precede the fan?" without the chart answering for it (no claims; the marks are marks).
**M3 · THE GALLERY CARD.** One static beauty-shot per asset·lens in the payload set (poster
frame of M1 at its most legible moment) for the project gallery.

## §3 · PAYLOADS (builder stage VIZ-4 emits; meta{sha256, rows, source, toll_lo, toll_hi} each)
`v4_mantle_{ASSET}_{LENS}.json` — default set: BTC·1h and BTC·5m. Columns: ts · 18 displacement
values (ema−price)/ATR (NaN before warm — the fabric simply hasn't been woven there; render the
missing cloth as absent, never as zero) · 18 thread velocities (Δdisplacement per bar, k-smoothed
per the ribbon-state k of that SR) · knot/fan flags · transition marks. Downsampled to ≤ 8,000
time steps, deterministic rule in meta.
`v4_echo_{ASSET}_{LENS}.json` — rolling corr(hem-velocity, rod-velocity) at lags {0…48} bars,
window 96 bars, same downsampling; plus the transition-mark list.
CONTEXT (read, never plot from): `CENSUS2A_CLOSEOUT_2026-08-12.md` · the ORACLE build's §4 header
(the toll table) · `NOMENCLATURE_MAP_v1_2026-08-12.md`.

## §4 · FOOTER (verbatim per artifact)
"DISPLAY-ONLY · Tier-E · payload {name} sha256 {sha} · displacements are (EMA−price)/ATR ·
no claim is made or implied; echoes are shown, not scored; promotion requires registration
(CENSUS2A_CLOSEOUT §5) · Rendered by Claude Design, {date}."

## §5 · FERRY CHECKLIST (operator)
1. Run the VIZ-4 builder block (one paste; emits payloads + copies this contract into
   DESIGN_HANDOFF_VIZ4/). 2. Open a Claude Design session. 3. Drag DESIGN_HANDOFF_VIZ4/ contents
   in. 4. Open with: "Execute this contract exactly; §2 of the VIZ-3 iron rules binding; payloads
   attached." Missing payload → render what exists, list absentees in DESIGN_NOTES.

— APOLLO · the wind is priced; the fabric, at last, is drawn.
