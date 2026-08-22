# BUILD · 2026-08-12 · CENSUS-2A VIZ-1 — payload extraction + first-pass renders
**Lane:** HEPHAESTUS (builder) · **Class:** **DISPLAY-ONLY / Tier-E exploration** ·
**Selection surface m = 0** · **Seed 20260812** · **Contract:** post-census; the CENSUS-2A
contract is SPENT and this build registers nothing, scores nothing, and claims nothing.
**Program:** `scripts/census2a_viz.py` (815 lines) · **Bulk:** all outputs born on `D:`.

> **The one sentence that governs this document.** Every number below is a *count, a byte, or a
> hash* — an inventory of pictures. There is no result here. Anything a picture appears to show is
> logged as a probe in `exchange/reports/CENSUS2A_PROBE_LEDGER.md` under the stamp
> `EXPLORATION — ungated; promotion requires registration`, and is not a finding.

---

## 0 · STEP 0 — THE TWO DOCUMENTS, FILED BYTE-EXACT

Both were already present from earlier this session and were **verified identical, not rewritten**
(skip-if-identical honoured — a re-write with the same content would have churned the git blob for
nothing).

| document | repo path | bytes | sha256 |
|---|---|---:|---|
| Design brief | `exchange/reports/DESIGN_BRIEF_CENSUS2A_VIZ_2026-08-12.md` | 6,067 | `9baa5a4e105b93cfc9b761bb2083a73cb67296b4306636c335494a93ae0a49a5` |
| Close-out | `exchange/reports/CENSUS2A_CLOSEOUT_2026-08-12.md` | 19,464 | `5de5fd747a91136680feb598484949b5fc9af4cf35aa78afbd683277ba592099` |

---

## 1 · STEP 1 — THE PROBE LEDGER IS OPEN

`exchange/reports/CENSUS2A_PROBE_LEDGER.md` — 4,027 B, sha256 `faa313ba20e72ba44f40bc3d591ad16b…`
— created **append-only**, carrying the close-out §5 law verbatim in its header (exploration is
unlimited; belief is rationed; the guard doesn't forbid looking, it prices remembering), plus the
`m` accounting rule and **entry #1**:

> *VIZ-1 extraction — nine payloads, selection surface **m = 0** (no comparisons promoted).*

The entry names all nine tables touched with their F-KEY results, and states why the two places a
reader might suspect selection are not selection: **V6 and V7 sort for display over a fixed,
complete row set** — no row is kept or dropped on the strength of its value and no threshold is
swept. The one truncation (v6 top-4000) is a **byte-budget** cut of a view whose declared subject
*is* the upper tail; it is recorded in the payload's own `downsample_rule` rather than left
silent. **Running selection surface after this entry: m = 0.**

---

## 2 · STEP 2 — PAYLOAD INVENTORY (nine, all under cap, all verified)

Destination `D:/Naiad/research_outputs/census2a/viz_payloads/`. Each payload is
`{"meta": {...}, "data": ...}` where **`meta.sha256` is the hash of its own `data` block**
(canonical JSON, `sort_keys=True`) — so a designer can verify provenance without trusting the
container.

| payload | rows | bytes | sha256 (first 12) | source parquet(s) |
|---|---:|---:|---|---|
| `v1_armings.json` | 848 | 118,168 | `abb55f910c03` | cen3_ledger_lensed, cen3_arm_windows |
| `v2_flows.json` | 34 | 2,887 | `44a895ddea56` | cen3_ledger_lensed, cen3_arm_windows |
| `v3_lags.json` | 605 | 46,094 | `d2c7a62f5ffb` | cen3_arm_windows, cen3_ledger_lensed |
| `v4_braid.json` | 2,596 | 255,537 | `54b05967aaf3` | cen1_ribbon (+ 4h frames) |
| `v5_weather.json` | 4,500 | 552,145 | `f6933f88f209` | cen6_episodes, cen2_refusals |
| `v6_campaigns.json` | 4,000 | 662,099 | `faa0e672a064` | cen5_campaigns |
| `v7_anchors.json` | 8 | 2,011 | `ba780deb720d` | cen8_anchor_grid, cen9_cards |
| `v8_sonar.json` | 705 | 228,007 | `91b4271fe5ed` | cen7_registry_series, cen3_ledger_lensed |
| `v9_tides.json` | 6,729 | 561,610 | `d1e1d62b913b` | cen6_episodes |

**Total 2,428,558 B across nine files. Largest 662,099 B — 94.6 % of the 700,000 B cap, none over.**

### F-V1 — payload integrity fixture
| assertion | result |
|---|---|
| every payload round-trips `json.load` | **PASS** ×9 |
| every `meta.sha256` re-verifies against a fresh hash of its own data block | **PASS** ×9 |
| every payload ≤ 700,000 B | **PASS** ×9 |
| row counts printed | **PASS** — table above |

NaN and ±inf are not JSON. `jclean()` maps them to `null` *before* hashing, which is why the
round-trip is exact rather than approximately exact; nothing is dropped and nothing is invented.

### F-KEY — every join, asserted before it was made
| table | declared key | rows | duplicates |
|---|---|---:|---:|
| `cen3_ledger_lensed` | (asset, arming_ts) | 848 | **0** |
| `cen5_campaigns` | (tranche_id) | 7,094 | **0** |
| `cen7_registry_series` | (asset, ts) | — | **0** |

This fixture exists because the non-unique-key defect appeared **three times** during the census —
most expensively when a non-unique `tranche_id` silently dropped 432 of 7,094 campaigns. It is
asserted here on every join rather than trusted.

### Downsampling rules (recorded in each payload's `meta.downsample_rule`)
| payload | rule | why |
|---|---|---|
| v4_braid | **rank-change points only** | the braid's information IS the crossings; bars where no rank changed carry no ink. Order-preserving, deterministic. |
| v5_weather | **evenly-spaced cap at 4,500 episodes** (deterministic, order-preserving) | byte budget; even spacing preserves the era distribution rather than favouring one end. |
| v6_campaigns | **top 4,000 by MFE** (the view sorts by MFE and the tail is its subject); **cap set by the 700 KB payload limit** | the full 7,094 came to 744,907 B — over cap. The cut is disclosed, not silent. |
| v8_sonar | **evenly-spaced cap at 700 event instants** (deterministic) | byte budget; same reasoning as v5. |
| v1, v2, v3, v7, v9 | **none — complete** | already inside the cap. |

---

## 3 · STEP 3 — RENDER INVENTORY (nine views + the gallery)

Destination `D:/Naiad/research_outputs/census2a/viz/`. Every page is one self-contained HTML file:
inline SVG, inline CSS, **zero external fetches, zero dependencies** — iron rule 6 satisfied by
having nothing to inline rather than by inlining a library.

| file | bytes | view | the money question, printed in the corner |
|---|---:|---|---|
| `V1.html` | 149,315 | ARMING SKY | where do profitable armings live — and is proximity to the line really poison? |
| `V2.html` | 9,654 | RELAY RIVERS | which routes through the window carry the money? |
| `V3.html` | 71,175 | LAG CLOCK | is there a golden hour inside the window? |
| `V4.html` | 253,971 | KNOT→FAN CINEMA | once 200 and 300 clear the 500, do they really never look back — and is that persistence paid? |
| `V5.html` | 13,357 | REFUSAL WEATHER | what does the air look like before a trap versus before a real breakout? |
| `V6.html` | 663,631 | TAIL GARDEN | where does the +9.4R tail live, and what does giving it back look like? |
| `V7.html` | 10,757 | CLOCK DUEL | how much of our clock's edge survives the toll — and who beats it? |
| `V8.html` | 13,247 | WALL SONAR | is confluence a crowd — or one wall that matters? |
| `V9.html` | 398,124 | VERDICT TIDES | which close is calm water, and which is chop? |
| `viz_index.html` | 4,164 | the gallery | nine cards, each with its question, row count and payload sha |

**Total 1,587,395 B; largest page 663,631 B — well inside the brief's ~2 MB per-view target.**
Mark counts (the check that no page is silently empty): V1 1,293 · V2 35 · V3 601 · V4 430 ·
V5 23 · V6 6,017 · V7 28 · V8 68 · V9 3,644.

### The four iron rules, per page
1. **Money question in the corner** — gold, top-right, phrased as a question, on all nine.
2. **The toll is always visible** — every outcome axis shades ±[0.0263, 0.0594] ATR from the
   payload's own `meta`, never a hard-coded literal in the renderer's drawing path. V3 draws it as
   a *ring* (radius = |outcome|), so "inside the ring the move is smaller than the toll" is a
   geometric fact of the picture, not a caption.
3. **Diverging at zero** — `lerp_col()` runs red → muted grey → green through a neutral midpoint,
   colourblind-safe on the red/green axis by carrying *lightness* as well as hue; **colour is
   always outcome, shape and size are always structure**, with no exceptions across the nine.
4. **The §5 footer verbatim** on every page, with each page's own payload name and sha256, and the
   rendered-by line reading **"Rendered by HEPHAESTUS first-pass, 2026-08-12."**

### Why raw SVG and not plotly/matplotlib
**Neither library is installed in this environment.** Installing a package to draw a picture is
not something to do unasked mid-contract, and the brief's actual requirement is *self-contained,
no external fetches* — which hand-rolled SVG satisfies directly and a CDN-loading plotly bundle
does not. The cost is honestly stated: **these are first-pass renders — legible, unornamented, no
hover interactivity.** The brief's "interactivity welcome" is unmet. Per the paste, Design's
versions sit **beside** these and never replace them; these are the guaranteed deliverable.

---

## 4 · STEP 4 — THE HANDOFF FOLDER

`D:/Naiad/research_outputs/census2a/DESIGN_HANDOFF/` — **11 files, 2,454,089 B**: the nine
payloads plus `DESIGN_BRIEF_CENSUS2A_VIZ_2026-08-12.md` and `CENSUS2A_CLOSEOUT_2026-08-12.md`
(the brief's §6 "read, do not plot from" context). Copied with `copy2`, so mtimes carry; the
payload shas are unchanged by the copy and re-verify in place.

---

## 5 · FINDINGS REPORTED, NOT FIXED

**F-1 · The v6 payload cannot carry two fields the brief's V6 spec asks for.**
`mae_r` and `n_reclaims` **do not exist in `cen5_campaigns.parquet`.** They are emitted as `null`
rather than derived, guessed, or quietly dropped. Consequences, stated so no designer wastes a
session hunting for them: **the spec's reclaim ticks on stems cannot be drawn, and the MFE/|MAE|
quality glyph is unavailable for this view.** The first-pass V6 substitutes what the data *does*
support — the give-back wilt, drawn as the red segment between terminal-R and MFE-reached, which
is the same question asked with one fewer field. Producing them would require re-running CEN-5
with an extended campaign schema; that is a contract change, not a render.

**F-2 · Two fields are recomputed at extraction time, not read from any parquet.**
`displacement_atr` (V1) and the six-EMA `ranks` (V4) are **recomputed from the 4h frames** because
no census artifact stores them. They are reproducible under seed 20260812 from the same frames,
but a reader comparing them against a parquet column will not find one. Disclosed rather than
presented as stored.

**F-3 · v6 is truncated to 4,000 of 7,094 campaigns by the byte cap.** Above, and in the payload's
own `downsample_rule`. The full set is 744,907 B against a 700,000 B cap. The kept 4,000 are the
top by MFE — which is where the view's declared subject (the tail) lives — but a designer asking
"what does the *bottom* of the distribution look like?" is asking about rows this payload does not
contain.

**F-4 · No interactivity.** Stated above under §3. Hover detail and asset/direction filters, both
"welcome" in the brief, are absent from the first pass.

**F-5 · The renderer was assembled through a scratchpad file, not a heredoc.** Two heredoc attempts
mangled escape sequences inside large quoted blocks (`\n` collapsed to a literal newline, producing
an unterminated string) — the same failure mode already recorded in this estate's operating memory.
No output was affected; the syntax error was caught by an `ast.parse` gate before the program ran.
Recorded because the next builder will hit it again.

---

## 6 · WHAT THESE PICTURES ARE FOR, AND WHAT THEY ARE NOT

The census's honest yield was **one SUPPORTED-PROVISIONAL result out of nine scored hypotheses**,
itself qualified by a witness-correlation of 0.60. These nine views do not improve that yield and
must not be read as doing so. They exist for the reason the brief gives: **to sharpen two
sentences — "the system enters when ___" and "the system exits when ___"** — by letting the
operator *see* the instants the census counted, at the scale of their own cost. The toll band
shaded on every outcome axis is the discipline of the whole exercise: a picture in which profit
smaller than cost looks exactly as small as it is.

---

## 7 · DISPOSITION & BOX-COST

| item | where | bytes |
|---|---|---|
| Nine payloads | `D:/Naiad/research_outputs/census2a/viz_payloads/` | 2,428,558 |
| Nine renders + gallery | `D:/Naiad/research_outputs/census2a/viz/` | 1,587,395 |
| Handoff bundle | `D:/Naiad/research_outputs/census2a/DESIGN_HANDOFF/` | 2,454,089 |
| **All bulk, on `D:`** | | **6,470,042** |

**BOX-COST — under 1 % of the bus, as required.** Only three text files enter `exchange/**`: this
build document, the probe ledger (4,027 B), and zero re-writes of the two already-filed documents.
Box before this build: **2,078,416 B = 32.53 %** of the 6,390,000 B budget. This build adds roughly
**18 KB ≈ +0.28 %**, landing near **32.8 %** — above the 25 % WARN line, **well below the 40 %
REFUSE line**. **Not one byte of payload or render is committed**; every one of the 6.47 MB lives
on `D:` per I2, and `publish_exchange` stages `exchange/**` only.

**One program file changed:** `scripts/census2a_viz.py`. `engine/` is untouched. No estate write.
No registration. No pin.

---

## 8 · REPRODUCTION

```
python scripts/census2a_viz.py                  # extract nine payloads + render ten pages
python scripts/census2a_viz.py --render-only    # re-render from existing payloads (no re-extract)
```
Seed 20260812 throughout; every downsample is deterministic and order-preserving.

---

## LEDGER_APOLLO APPEND

The following was appended to `exchange/status/LEDGER_APOLLO.md` in this same session:

```
=== STATUS_APOLLO — 2026-08-12m ===
NOW: CENSUS-2A VIZ-1 IS DELIVERED. Nine payloads extracted, nine views rendered, the handoff
folder is packed, and the probe ledger is open. CLASS: DISPLAY-ONLY / Tier-E — this build
registers nothing, scores nothing and claims nothing; selection surface m = 0.
LAST EVENT: 2026-08-12 — VIZ-1: the census's instants, drawn
FACTS:
- TIER-E CLASS STATED ON EVERY ARTIFACT. Nine payloads and ten HTML pages each carry the close-out
  §5 footer verbatim with their own payload sha; the probe ledger stamps entry #1
  "EXPLORATION — ungated; promotion requires registration" [verified]
- THE BRIEF AND THE CLOSE-OUT ARE FILED BYTE-EXACT and were verified identical rather than
  re-written: brief 6,067 B sha 9baa5a4e…, close-out 19,464 B sha 5de5fd74… [verified]
- PROBE LEDGER OPEN: exchange/reports/CENSUS2A_PROBE_LEDGER.md, append-only, carrying the §5 law
  and the m-accounting rule. Entry #1 = VIZ-1 extraction, m = 0. RUNNING SELECTION SURFACE: 0 —
  nothing this build did can ever be charged to a future FDR family [verified]
- F-V1 PASS ×9: every payload round-trips json.load, every meta.sha256 re-verifies against a fresh
  hash of its own data block, every payload under the 700,000 B cap (largest 662,099 = 94.6%)
  [verified]
- F-KEY PASS on all three joins: cen3_ledger_lensed (asset, arming_ts) dup=0 · cen5_campaigns
  (tranche_id) dup=0 · cen7_registry_series (asset, ts) dup=0. The fixture exists because the
  non-unique-key defect appeared three times during the census [verified]
- HANDOFF READY: D:/Naiad/research_outputs/census2a/DESIGN_HANDOFF/ — 11 files, 2,454,089 B (nine
  payloads + brief + close-out). Renders at .../viz/ — ten pages, 1,587,395 B, self-contained,
  zero external fetches [verified]
- THE TOLL IS DRAWN ON EVERY OUTCOME AXIS, read from each payload's own meta, never a literal in
  the drawing path. V3 draws it as a ring, so "smaller than its own cost" is geometry, not a
  caption [verified]
- REPORTED NOT FIXED: mae_r and n_reclaims DO NOT EXIST in cen5_campaigns — emitted null, so V6's
  reclaim ticks and MFE/|MAE| glyph cannot be drawn; displacement_atr and the six-EMA ranks are
  RECOMPUTED from 4h frames, not stored anywhere; v6 is truncated to 4,000 of 7,094 by the byte
  cap (disclosed in its own downsample_rule); and there is NO interactivity in the first pass
- WHY RAW SVG: neither matplotlib nor plotly is installed. Installing a package to draw a picture
  is not a thing to do unasked, and self-contained-no-external-fetch is what the brief actually
  requires. First-pass renders are legible and unornamented; Design's versions sit BESIDE them and
  never replace them, per the paste
- BOX-COST: exchange/** was 2,078,416 B = 32.53%; this build adds ~18 KB ≈ +0.28% → ~32.8%. All
  6,470,042 B of payloads, renders and handoff live on D: — not one byte committed [verified]
PENDING (unchanged; the census contract remains SPENT):
1. Filed and unscored: P-FAN-1 [60%], P-ARM-2 [55%], P-NEST-2 [50%], P-RAT-3 [40%], P-VBT-2 [45%],
   P-CHOP-2 on the newly-valued ribbon operand
2. Design's session, if it happens, consumes DESIGN_HANDOFF/ and returns DESIGN_NOTES.md; the
   first-pass renders stand regardless
3. Anything a viewer finds interesting in these nine views is a PROBE, logged in the probe ledger
   with its m — never a finding, and never citable without the Tier-P ceremony
4. The D:-moved incident remains routed to ATHENA; cause unidentified
NEXT: THE PATH's next step is still the operator's — Tier-C / EngineV2, or the rotation funnel.
Owner: operator.
METRICS: operator actions this session = 1 (the VIZ-1 paste) — files re-ingested = 0
=== END STATUS ===
```

— HEPHAESTUS · the pictures serve the sentences; the sentences serve the P&L.
