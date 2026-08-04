# SESSION SUMMARY — ATHENA · Memory workstream, closed · 2026-08-03

**For every lane, APOLLO especially.** Zero context assumed. Provenance: `[verified]` = computed or
read this session · `[ratified]` = operator decision · `[handoff]` = builder-reported · `[open]`.

## 1 · What changed for you, in four lines
1. **`exchange/status/CONVENTIONS.md` now exists and is AUTHORITATIVE.** Read it at session start.
   It holds the operating rules, several of which used to live in project memory. `[verified]`
2. **Project memory went 30 → 23 entries.** Eight rules moved into that file, full text. `[verified]`
3. **Memory does NOT reach Cowork.** HERMES, DIONYSUS and HEPHAESTUS have never seen a memory
   entry. CONVENTIONS.md is the only surface reaching all six actors. `[verified]`
4. **A repo file is confirmed visible only when a project-knowledge search returns it WITH a folder
   path.** A bare filename may be a hand-upload and proves nothing. `[verified]`

## 2 · What was done
Operator ruled the memory snapshot first, everything else parked (2026-08-03). Delivered:
the 30-entry verbatim snapshot (`docs/memory/claude_project_memory_2026-08-03.md`, `a58b2bb`);
a pre-registered acceptance contract; `CONVENTIONS.md` (`dde8523`); a sha256 reconciliation of the
project box against the repo; eight memory relocations, one correction, one pointer added; this
report and the closing snapshot.

Rulings taken: Q-0 B (legacy memory experience) · G-1 c (tiered: memory = identity, operator
style, behaviour-critical rules, pointer; repo = state, reference, procedure) · G-2 a (one
workstream) · G-3 a (fresh-session probe as acceptance) · G-4 a (pointer + custodian ritual +
Hermes staleness) · G-5 a (reviewer-executed, snapshot-bracketed). `[ratified]`

## 3 · Findings that change what other lanes should believe
- **The "project memory is not in data exports" claim is contradicted** by current Anthropic
  support documentation, which says all memory data IS included. Resolution is empirical — inspect
  the first export (T-6). The `docs/memory/` snapshots stand regardless: they are the copy under
  our verification standard and the restore path. `[verified]`
- **A global "Reset memory" deletes project memories too, irreversibly.** `[verified]`
- **The GitHub sync does not reach the repo root.** `SCHED_TEST_RESULT_2026-08-02.md` is tracked
  and pushed at root and is not retrievable. Anything a web lane must read goes under `exchange/`
  or `docs/`. `[verified]`
- **🔴 The weekly `--workflow` backup trigger is NOT ARMED and never was**, despite `CADENCE.md`,
  memory entry #24 and `CONVENTIONS.md` §8 all claiming Sundays 08:30. Three documents copied the
  claim; none verified it. Same mechanism as the retention-rule failure. Both documents corrected
  this session; the backup is run by this paste. `[verified]`
- **The daily brief had been silently halting since `d622b20`** — caught during the retention fix.
  Cause: an optional job that fails still lets the routine exit 0, and F-B1..8 run inside
  `daily_brief.py` rather than pytest, so a green suite said nothing. Fixed, 8/8. **Generalises:
  an optional job that fails silently is indistinguishable from one that works.** `[handoff]`

## 4 · Reviewer errors this session, on the record
Four, none analytical: a verification gate written against prose the same author wrote in the same
act (Class B — gates now match distinctive fragments, case-insensitively); a publish command with
bash-destroying backslashes calling a module with no entry point, when the working invocation was
already on record from the previous session (Class A); an insurance archive handed over without
saying to keep it outside the repo; and **nine of twenty-one box-file calls wrong**, every one from
reading *around* the repo instead of reading it. That last is why the box question was settled by
sha256 measurement rather than inference. The builder halted correctly on the first two.

## 5 · What remains
1. **Acceptance probe** — operator opens one fresh chat, pastes the registered prompt, returns the
   reply. Pass = 5 of 6 behaviours with B6 (conventions consulted) among them. `[open]`
2. **Phase-boundary audit** — move #1, #15, #19 and execute four merges → 16 entries. `[open]`
3. **T-2 arm HERMES** — `DIGEST.md` still a placeholder; his is the only unarmed CADENCE trigger.
   Constraints: no network egress, git untested, no deletions ever. `[open]`
4. **T-5 `OPERATOR_PREFERENCES.md` Part 1** and the portable operator layer. `[open]`
5. **T-6 data export** — settles the export dispute permanently. `[open]`
6. Box cleanup: 23 of 26 files now safe to remove; the 3 orphans are filed by this paste, making
   it 26 of 26. `boxrescue/` should be moved outside the repo tree. `[open]`

## 6 · For APOLLO specifically
Nothing in your lane was touched. Memory entries #1 (SS Pine backlog) and #19 (SS interview
rulings Q1c–Q11) were **deliberately left in place** rather than relocated, because they are yours
and the enforcement hook has not been tested yet. Your study state — research inversion,
discriminant frame, tail-retention gauge, W-F1 — is untouched in entry #30. The one thing to adopt:
**read `exchange/status/CONVENTIONS.md` at session start.** It is where paste construction,
reporting format and the manual-task rule now live.

— ATHENA, 2026-08-03
