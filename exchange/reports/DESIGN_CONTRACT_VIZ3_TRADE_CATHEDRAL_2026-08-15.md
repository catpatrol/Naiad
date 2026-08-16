# DESIGN CONTRACT · VIZ-3 — "THE TRADE CATHEDRAL"
**From:** APOLLO (Project Naiad) · **To:** the Claude Design session · **Date:** 2026-08-15
**Class: DISPLAY-ONLY / Tier-E.** Nothing here is evidence; every artifact carries the §4 footer.
**Lineage:** the CENSUS-2A gallery (compliant, 9/9 footers) is the floor; exceed it in clarity.

## §1 · THE COMMISSION — four pieces, one language
The client is a discretionary crypto trader. His system ("Secret Sauce") reads eighteen EMAs
braided into six ribbons; trades live as six stations: watchlist → arming (12/89) → trigger
(12/26) → add (pending) → ride → bell (counter-12/89 / 89/316). Purpose of every pixel: sharpen
two sentences — "the system enters when ___, exits when ___."

**P1 · THE TRADE CATHEDRAL (centerpiece — interactive 3D).** Two naves side by side: DEFAULT
(4 stations, as measured) and IDEAL (7 stations; Add + Harvest rendered as scaffolding/ghost —
their registrations are pending and the visual must say so). Floor = time; height = R; columns =
stations. Hovering or clicking any column opens an info panel: stage name, binary gate question,
evidence class {verified · provisional · pending}, and the May-26 value from the payload.
The May-26 short walks the DEFAULT nave as a lit path (its real timestamps). three.js permitted
(CDN); graceful 2.5D fallback if WebGL absent. One self-contained HTML.
**P2 · THE MAY-26 GANN BOARD (design-grade).** Time×price stepped board, six stones descending
(short), the 89/316 seal annotated OFF the path (+28h, "the eulogy"), relay leg May-18 as a
half-stone. Static SVG or light-interactive; print-worthy.
**P3 · THE R-TERRAIN.** 6,834 campaigns as a 3D height field: x = campaign rank by MFE, z =
asset lanes, y = R; MFE ridge in one hue, terminal surface beneath, give-back as the visible gap
("erosion"); the 814 winners lit. Orbit/zoom; hover → campaign card (id, gross_R, mfe, give-back,
hold). three.js.
**P4 · THE BREATH HELIX.** For one asset·lens (payload: BTC 1h), the six ribbons' width over time
wound around a time axis — compression = tight coil, expansion = open coil; knot and fan episodes
tinted; the census's transition timestamps as beads. Interactive scrub.

## §2 · IRON RULES (unchanged from the gallery brief; binding)
Payload-only (no invented numbers; omit gracefully + note) · display-only (no verdict language;
pending stones labeled pending) · toll band visible on any outcome axis · diverging palettes
anchored at zero · dark-mode legible · self-contained HTML, deps via CDN only · provenance footer
per artifact · DESIGN_NOTES.md (≤1 page) listing choices + anything payloads couldn't support.

## §3 · PAYLOADS (produced by builder paste VIZ-2; each carries meta{sha256, rows,
source, toll_lo, toll_hi})
`v3_may26_tape.json` — the May-26 window's event tape ±: arming/relay/trigger/seal/bell
timestamps, prices, displacement at arming, per-stage stamps. · `v3_stations.json` — the twelve
station cards (default 4 + ideal 7 + seal annotation): gate text, evidence class, may26 value,
rule fuzz [VETO] names. · `v3_terrain.json` — per campaign {rank, asset, mfe_r, terminal_r,
give_back_r, hold_h, is_winner} (downsampled ≤6,834 rows, ≤700 KB). · `v3_helix.json` — BTC 1h:
{ts, six ribbon widths in ATR, knot/fan flags, transition marks} (state-change points + hourly
spine). CONTEXT (read, never plot from): `CENSUS2A_CLOSEOUT_2026-08-12.md` ·
`SSV12_PINE_SPEC_2026-08-14.md` · the six-rules message · `NOMENCLATURE_MAP_v1_2026-08-12.md`.

## §4 · FOOTER (verbatim per artifact)
"DISPLAY-ONLY · Tier-E · payload {name} sha256 {sha} · evidence era ≤ 2024-07-01 · pending
stations are unregistered hypotheses; promotion requires registration (CENSUS2A_CLOSEOUT §5) ·
Rendered by Claude Design, {date}."

## §5 · OPERATOR CHECKLIST
Run builder paste VIZ-2 → drag `DESIGN_HANDOFF_VIZ3/` (4 payloads + this contract + the 4 context
docs) into a Claude Design session → open with: "Execute this contract exactly; §2 binding;
payloads attached." Missing payload → Design renders what it has and lists absentees.

— APOLLO · the cathedral is for seeing the debt as clearly as the treasure.
