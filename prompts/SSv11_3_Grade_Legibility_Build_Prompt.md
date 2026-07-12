# BUILD PROMPT — SSv11.3 "Grade Legibility" + Break Diagnostics (display-only Pine patch)
### Feed this file to Claude Code. It is a self-contained contract. · v1.1 consolidated 2026-07-11
### SUPERSEDES SSv11_0_3_Grade_Legibility_Build_Prompt.md (operator renamed 11.0.3 → 11.3)
### Line: Midas (Pine) · Builder: Claude Code · Reviewer: Claude (Project) · Operator: Ludwig
### Ratified: VR-A = Option 3 · VR-B = defaults · VR-C = docs-only (2026-07-11)

---

## 0. Mission

Two jobs in one session, strictly ordered. FIRST, diagnostics: capture the
deployed v11.0.2 source, report its delta against the v11.0.0 project copy,
and print two read-only journal/estate queries — this serves a live,
confirmed parity-break investigation (§1). SECOND, the patch: ship SSv11.3,
same machine, same alerts, same logic — grade-differentiated glyphs on every
PRIME, plus playbook corrections for erratum E-1.

Definition of done: D0 delta + Q1/Q3 printouts delivered; a diff proving only
display lines changed in the Pine; the playbook erratum edits (D6); a
compiled SS_Cascade_v11.3.pine; operator A/B pass on Jun 22 '26.

## 1. Pre-check and diagnostics — BEFORE any patch work

**Break context (reviewer-confirmed 2026-07-11):** the engine journaled three
CONFIRM events at 2026-06-23 17:00 / 17:45 / 20:45 UTC (all zone "-") and
ratcheted the short stop 63041.35 → 62590.61 → 62586.80 → 62490.50. The
deployed v11.0.2 chart printed no glyphs there and its stop line stayed FLAT
— it processed none of the three. First confirmed parity break of the record.
Prime suspect (H1): deployed v11.0.2 zone-gates the CONFIRM trigger itself;
the engine implements the older ungated form, making the engine the deviant.

**1a — Source capture.** The operator saves the deployed source into the repo
as `pine/SS_Cascade_v11.0.2.pine` (runbook §7 step 1). Diff it against the
v11.0.0 project copy and report the FULL delta (D0), with special attention
to: the CONFIRM trigger condition and the CONFIRM plotshape conditions
("Confirm Long/Short" diamonds, C markers), `gradeCL/gradeCS`, `hadPrimeEp`
lifecycle, zone gating of glyphs, and the zone-arming lines
(`z23Armed` / `stageAligned`) — the operator confirmed by tint check
(2026-06-16, faint green) that deployed v11.0.2 fires Z2-labeled PRIMEs in a
stage-1 provisional campaign; cite the exact line permitting it and state
whether Z3 is likewise armed (its band is hidden in stage 1, so a provisional
Z3 entry would fire from a zone the operator cannot see).

**Expected-delta rule:** a CONFIRM zone-gate delta is EXPECTED — it is H1.
Report it prominently; do NOT stop for it. STOP and report (no patching) only
for logic deltas beyond {provisional arming incl. zone-arming, C-grade
gating, CONFIRM gating}.

**1b — Read-only diagnostics (print in full; no code changes):**
- **Q1 — phantom sweep:** every CONFIRM row with zone "-" across the ENTIRE
  dev-window parity journal (BTCUSDT_swing, v11_faithful): timestamps, stop
  values, total count. This sizes the contamination if H1 holds.
- **Q3 — estate candles:** OHLC for BTCUSDT 5m, 2026-06-23 14:00 → 21:00
  UTC, from the verified estate. (Arms the operator's data cross-check.)
- The V census (former Q2) is already delivered — skip it.

## 2. Invariants (violating any is a failed phase)

- **I1 — Display-only in Pine.** State machine, triggers, grades logic,
  zones, stops, failure, TPW, V, and every `alert()`/`alertcondition()`
  block byte-identical to v11.0.2. The Pine diff may touch only:
  plotshape/plotchar lines, const color/size literals, banner/changelog,
  Display-group input text. The D6 playbook edits are Markdown, outside the
  Pine, and are the ONLY permitted doc/logic-adjacent change.
- **I2 — Pine output budget** ≤ 64 under Option 3; count stated before/after
  in the banner.
- **I3 — Version discipline.** Banner v11.0.2 → **v11.3** (changelog notes
  the operator renumbering from the 11.0.x scheme); filename
  `SS_Cascade_v11.3.pine`.
- **I4 — Parity freeze.** Parity chart layouts stay on v11.0.2 until 3C
  closes; v11.3 loads on a separate layout only.
- **I5 — Const-color discipline.** Colors remain const hex literals
  (Style-tab overridable), per the banner's budget rules.
- **I6 — No E-1 logic revert (VR-C, ratified).** Provisional Z2 arming stays
  as deployed; its disposition is a named-variant question for the v12
  Study. v11.3 corrects the DOCUMENTS, not the behavior.

## 3. Ratified design decisions (recorded; veto window closed 2026-07-11)

- **VR-A = Option 3:** keep the six R1 grade markers; add six graded R2+
  shapes (per-grade colors/sizes below); delete the two generic R2+ circles;
  retire the two "89x200 Stage 2" circles (deep tint already carries that
  cue). Net +2 outputs → 62/64 worst case.
- **VR-B = default scheme:** A+ = #FFD700 gold, R1 size.normal / R2+
  size.small · A = full direction color, R1 size.small / R2+ size.tiny ·
  B = direction color at 60% transparency, R1 size.small / R2+ size.tiny.
- **VR-C = E-1 docs-only:** see I6 and D6.

## 4. Deliverables

- **D0** — v11.0.2 delta report per §1a, explicitly answering: the deployed
  CONFIRM trigger and glyph conditions (H1 verdict line), whether zoneless
  CONFIRMs draw anything, which line arms Z2 (and Z3?) under provisional.
  Also create `SSv12_SPEC_ERRATA.md` at repo root recording **E-1**:
  deployed v11.0.2 arms Z2 during provisional (stage-1) campaigns,
  contradicting spec §4.2 ("Stage 1 arms Z1 only") and the playbook's
  "Z2 … Stage 2 only" row — confirmed by operator tint check 2026-06-16 and
  the engine journal; cite the source line; note Z3 status; disposition
  deferred to SSv12 spec time (named-variant candidate: "provisional-Z1-only").
- **D1** — `pine/SS_Cascade_v11.3.pine` implementing VR-A/VR-B.
- **D2** — diff v11.0.2 → v11.3 proving I1 (display lines only).
- **D3** — banner/changelog updated; output budget stated before/after.
- **D4** — operator A/B instructions: v11.3 on a fresh layout, jump to
  2026-06-22 12:00–20:00 UTC; the rc 31/32/33 A+ adds must be instantly
  distinguishable (gold, larger) from neighboring B adds; parity layout
  still shows v11.0.2.
- **D5** — session packet zip: D0 report, Q1/Q3 printouts, both .pine files,
  diff, changelog, D6 diff.
- **D6** — playbook erratum edits (`SSv11_Execution_Playbook.md`): correct
  the Z2 glyph-dictionary row ("Stage 2 only" → "Stage 2; ALSO armed during
  provisional campaigns per erratum E-1 — entries there are real, grade
  ceiling B") and add one sentence to the §3 zone-bands cue row pointing at
  E-1. Nothing else in the playbook changes.

## 5. Verdict criteria (pre-registered)

Phase passes iff: D0 + Q1 + Q3 delivered; D0 clean of out-of-scope logic
deltas per §1's stop rule; the D2 Pine diff touches only I1-permitted lines;
every alert block byte-identical; budget ≤ 64 and documented; the script
paste-compiles with no errors; the operator's Jun 22 A/B check passes; D6
diff confined to the two named playbook spots. Phase fails pending report if
the §1 stop rule triggers.

## 6. What this phase is not

No Pine logic, gate, grade, stop, or alert changes. No E-1 code revert
(I6). No engine changes — if D0 confirms the CONFIRM zone-gate, the engine
fix is a SEPARATE Naiad-line contract after reviewer ruling. No new glyph
for zoneless CONFIRMs. No MTF smear fix (B-2 parked). No 12H swing mode
(B-1 parked). Anything not in §4: stop and report instead of building.

---

## 7. Operator runbook (for Ludwig — the builder skips this section)

**Step 1 — Export the deployed source (skip if already done).** TradingView →
open the SS CAS v11 chart → Pine Editor tab (script loads there) → click in
the code → Ctrl+A, Ctrl+C → Notepad → Ctrl+V → File → Save As → into the
Naiad folder's `pine` subfolder → name `SS_Cascade_v11.0.2.pine` → "Save as
type": All files → Save. *You should see: the file in the pine folder.*

**Step 2 — This contract into the repo.** Move
`SSv11_3_Grade_Legibility_Build_Prompt.md` into the Naiad folder. The old
SSv11_0_3 file is superseded — delete it or ignore it.

**Step 3 — Fresh builder session.** Close the old Claude Code window (the
Q&A history isn't needed — this contract is self-contained). New PowerShell →
`cd ` + drag Naiad folder + Enter → `claude` → paste the handover block from
the chat. *You should see: D0 delta first (with the CONFIRM-condition line
called out), then Q1 and Q3 printed, then the patch work, then the packet.*

**Step 4 — Your two chart minutes (while the builder works).**
(a) 5m chart, Jun 23 15:00–17:00: hover 2–3 candles, compare O/H/L/C against
the Q3 printout. (b) Hover the red stop line near Jun 23 10:00 and note the
exact value it reads (journal says 63,041.35).

**Step 5 — Compile and glance.** Pine Editor → new script → paste v11.3 →
"Add to chart". *You should see: no red errors.* Load it on a NEW layout,
jump to 2026-06-22 afternoon. *You should see: the three Z3 A+ adds (14:10,
15:50, 18:30) in gold, visibly larger than the muted B circles.* Parity
layouts stay on v11.0.2.

**Step 6 — Ferry.** Attach the D5 packet zip here; paste as text: the D0
report, the Q1 and Q3 printouts, and your two hover readings from Step 4.
The reviewer then rules on the break hypotheses and, if H1 confirms, drafts
the Engine 1.0.3 fix contract.
