# REVIEWER HANDOFF — Project Naiad / v12 Study / Midas (SSv11.3)
### Close of record: 2026-07-12 · From: Claude (Project reviewer, Fable-mode)
### To: the next session's reviewer instance + operator Ludwig
### Authority: repo LEDGER.md on origin/v12-v1-census. This doc summarizes it;
### on any conflict, the repo wins. New session: verify before acting.

---

## 1. STATE OF RECORD (all reviewer-recomputed from raw artifacts)

**Repo:** branch `v12-v1-census` @ **38b3f66** (pushed, local in sync).
Commit chain of note: d146de6 (halt scope per_cell) → 1d3e498 (hygiene) →
0c51660 (engine 1.0.3 fix) → 38b3f66 (1.0.3 merge). CI green through 4df5387;
fresh runs expected green.

**Closed and verified:**
- **v12 V1 census — CLOSED (PASS).** 26,711,569 candle rows, 60/60 series,
  hash chain intact; gaps: 1 listing_edge + 5 exchange_side + 0 download_hole;
  external anchors (HYPE to the minute, LIT to the day, SOL FTX-week funding).
- **Engine 1.0.2 (no-shrink) — MERGED** (49571c3). Cache truncation class
  closed; N1–N5 fixtures live.
- **Engine 1.0.3 (input-parity) — MERGED** (38b3f66). Root cause of the 3C
  break: engine hardcoded zone_memory=5 (origin: Phase-1 build prompt §5);
  deployed Pine runs zoneMemory=3 (operator-verified both charts). Fix: 3
  everywhere; 8 input-parity fixtures (constants vs committed pine-defaults
  manifest + behavioral pins). Suite **47 passed / 1 skipped** (skip =
  dryrun-scan, journal archived, skipif-guarded). Parity journal REGENERATED:
  run_id 1869ff707385dc4e, SHA 4c7343178af89dc14cd25933a3d5ab76c6b21211d090aad578d81e7413ce92de,
  **5,446 rows**, census {CLUSTER 504, CONFIRM 463, PRIME 1308, REGIME 30,
  REJECT 1845, STAGE 5, TAG 1219, TPW 53, V 1, X 18}. **I3 diff vs validated
  shadow = ZERO** (1790 load-bearing events, 0/0/0). mem=5 journal ARCHIVED at
  research_outputs/parity/journal_mem5_archive/ = "zoneMemory-5" v12 variant seed.
- **Parity evidence, final:** 3A 30/30 · 3B 11/11-by-geometry (0 native prints
  = design) · 3C six windows ALL PASS (Jul 2–6, Jun 14–16, Jun 22–23 [former
  break, resolved], May 16–26 [regrades "-"→C glyph-verified at 05-17 13:50 and
  05-29 21:25], Feb 6 Tier-2, Dec 4–13 Tier-2) · 3D Outcome **C/C** (V census:
  1 firing in 9 months — 2025-12-12 15:25 short @ 90,795). Post-conformance
  float-fork count: **0**. Criterion amendment (bf92eaa) stands as law.
- **Ratifications on ledger:** v12 charter VR-1..VR-5 · halt scope
  **per_cell** (d146de6) · knife-edge criterion (bf92eaa) · v11.3 VR-A Opt 3 /
  VR-B defaults / VR-C docs-only · 1.0.2 V-A/V-B.
- **SSv11.3 — FROZEN terminal v11.** Display-only successor to v11.0.2
  (logic byte-identical, D2-verified). Manual:
  `SSv11_3_Execution_Playbook_and_Field_Manual.md` **v2.0** (element
  dictionary; corrected provisional/E-1/C-gating claims; Inputs Law:
  defaults only, Zone memory = 3 is parity-critical).
- **Registers:** E-1 in SSv12_SPEC_ERRATA.md (tracked) · J-1 (REJECT
  stage=1 dataclass default) parked for next engine touch · B-1 (12H swing
  mode), B-2 (MTF/TPW smear) parked for SSv12 · v12 named-variant seeds:
  zoneMemory-5 (archived journal), provisional-Z1-only, zone-gated CONFIRM adds.

**Sign-off status: EVIDENCE COMPLETE, LEDGER ENTRY NOT YET COMMITTED** (the
paste below). Collector: NOT yet dispatched. Handshake: NOT yet delivered.

---

## 2. CORRECTION (supersedes the sign-off block drafted in the prior chat)

The earlier draft said "v12 Study V2 gate SATISFIED; V3 OPEN." **Wrong per
VR-4**: V2 = parity completion (3B/3C/3D — now done) **PLUS the ETH+FARTCOIN
cross-asset spot check — still outstanding.** V3 opens after that small
session. The block in §3 below is the corrected, authoritative version.

---

## 3. IMMEDIATE NEXT STEPS (verbatim pastes, in order)

**3.1 — Sign-off ledger commit (paste to builder):**

```
Append byte-for-byte to LEDGER.md and commit with message "parity sign-off: step 3 closed", then push:

## 2026-07-12 — TradingView parity sign-off (Runbook Step 3 / F6): CLOSED — PASS
- Instrument: deployed SS Cascade v11.0.2 (= v11.3 logic), inputs at defaults (Zone memory = 3, operator-verified). Engine 1.0.3 (input-parity conformance); parity journal run_id 1869ff70..., SHA 4c734317...ce92de, 5,446 rows; I3 diff vs validated shadow = ZERO.
- 3A: 30/30 4H governor crosses exact. 3B: 11/11 12H by EMA geometry; 0/11 native prints = design.
- 3C, six case windows: Jul 2-6 PASS · Jun 14-16 PASS · Jun 22-23 PASS (former break resolved by 1.0.3; phantom mem=5 events removed; chart == journal) · May 16-26 PASS (two regrades "-"->C glyph-verified: 05-17 13:50, 05-29 21:25) · Feb 6 Tier-2 PASS · Dec 4-13 Tier-2 PASS (lone V verified in campaign context). Tiers: 1 = chart-verified; 2 = past TradingView intraday horizon, covered by I3 shadow equivalence.
- 3D: Outcome C on both doctrine dates (no V printed on any chart or TF; engine agrees). V census: 1 firing in 9 months (2025-12-12 15:25, short @ 90,795).
- Knife-edge criterion (bf92eaa) stands as law; measured float-fork count post-conformance = 0 - every prior divergence traced to the zone_memory constant, corrected in 1.0.3 and fixture-pinned.
- Errata: E-1 on record (SSv12_SPEC_ERRATA.md). J-1 (REJECT stage dataclass default) parked for next engine touch.
- Operator sign-off: Ludwig, 2026-07-12. Reviewer: all headline numbers recomputed from raw artifacts.
- STEP 3 CLOSED. Collector switch-on (Step 5) UNBLOCKED.
- v12 Study V2: parity legs (3B/3C/3D) SATISFIED; remaining V2 item = ETH+FARTCOIN cross-asset spot check (VR-4). V3 opens on its completion.
```

**3.2 — Hygiene commit (paste to builder; drop the v2.0 manual file into the
naiad folder first):**

```
Stage one hygiene commit for review, then show me the diff: (1) add SSv11_3_Execution_Playbook_and_Field_Manual.md (v2.0) at repo root; (2) archive the v1.1 playbook WITH its D6 edit to prompts/ (superseded by v2.0); (3) track pine/SS_Cascade_v11.3.pine; (4) track research_outputs/ssv11_3/ and research_outputs/engine_1_0_3/; (5) move the Engine_1_0_3 contract file to prompts/. Leave the ferry zips untracked.
```
Review diff → commit → push.

**3.3 — Chart switches:** MTF Display toggles back **ON** (all four); parity
layouts move to **v11.3**. One script, one manual, one engine, all verified.

**3.4 — Collector (guide 5.b–5.e condensed):** GitHub branch dropdown — if no
`data` branch, create via the guide's one-liner. Then **Actions → collector →
Run workflow → Branch: v12-v1-census** (carries 1.0.3 by construction). Expect
green in 5–20 min; `data` branch gains a `tick:` commit (warm-up skips
normal). Red = screenshot, stop, do not schedule. Then edit
`.github/workflows/collector.yml` on the site, un-comment the two cron lines
(second line keeps its two leading spaces), commit, `git pull` locally once.
Heartbeat: green run near :07 hourly; one `tick:` commit per run; paper epoch
stamps once per cell.

**3.5 — Handshake ferry (one message to the new chat):** sign-off ledger
diff · hygiene commit hash · collector first green run + first tick commit ·
"collector live." Reviewer then delivers: **UNCONDITIONAL PASS** verdict entry ·
**Phase-2 protocol** (reconciled with the v12 charter: monitoring cadence,
Experiment E1 halt-scope, forward-data/estate division; guardrails: watch
machinery not score; replays outside spent window = evidence spend; configs
frozen) · confirmation that V3 awaits only 3.6.

**3.6 — ETH+FARTCOIN cross-asset spot check (small session; the last V2
item):** builder prints a handful of recent governor crosses per asset from
the engine; operator checks them on TradingView charts (same protocol as 3A,
UTC, defaults). On pass → **v12 Phase V3 (anchor run) OPENS** — reviewer
drafts the V3 contract per the Study Charter Addendum.

---

## 4. OPEN-ITEMS REGISTER (owner · gate)

| Item | Owner | Gates |
|---|---|---|
| 3.1 sign-off commit | Builder+Op | Step-3 formal close |
| 3.2 hygiene commit | Builder+Op | manual/artifacts on remote |
| 3.3 toggles + v11.3 layouts | Operator | — |
| 3.4 collector switch-on | Operator | Phase 1.5 live |
| 3.5 handshake | Reviewer | UNCONDITIONAL verdict + Phase-2 protocol |
| 3.6 ETH+FARTCOIN spot check | All three | **v12 V3** |
| J-1 journal hygiene | Builder | next engine touch (non-blocking) |
| main-branch consolidation | Op+Builder | post-sign-off, non-blocking (main has no engine; collector uses v12-v1-census) |
| B-1, B-2, E-1 disposition, variant seeds | — | SSv12 spec time / v12 slots |

## 5. STANDING DISCIPLINES (unchanged)

Reviewer recomputes every headline from raw artifacts; builder summaries are
never accepted at face value. Regenerate-never-merge on semantic changes.
Ledger appends are builder-typed, byte-for-byte. Operator owns every merge
and gate. Pre-registered predictions, falsification as deliverable (this
chat's score: reviewer 2 confirmed / 5 falsified — and each falsification
narrowed the truth). Spent window: BTC 2025-10-06→2026-07-07,
characterization-only, forever. Evidence spend to date: **zero**.

## 6. FOR THE NEW SESSION'S FIRST MESSAGE

Operator: paste/upload this document (and the builder's handoff if produced)
with "continue from handoff." Reviewer: state LEDGER from this doc, verify
against the repo's LEDGER.md before acting, then resume at the first
unchecked item in §3.
