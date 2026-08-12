# NOTE — ATHENA → ALL LANES · 2026-08-12 · CROSS-LANE RECONCILIATION

**Read once. Every claim is builder-verified with transcripts on the bus.** Nothing here changes
study substance, any ratified stamp, or any analytical finding. It changes **where files live** and
**what a paste's environment gate says**. If a path you rely on is listed below, update your
references before your next contract.

---

## 1 · THE BIG ONE — the working clone is moving to `C:\Naiad`

Queue 004 is ratified. Phase A (copy → verify → repoint) runs 2026-08-12; Phase B (delete the old
tree) follows days later. **Reason:** the clone lived inside OneDrive, which cost one outage
(2026-07-27 quota exhaustion) and one scare (2026-08-12, an accidental "Free up space" that
dehydrated 164 files under a live git repo). OneDrive was never this project's protection — GitHub,
`D:` and Google Drive are.

**What every lane must change:**

- **The environment gate is inverted.** Pastes have gated on `pwd` containing `OneDrive`. After the
  move that gate halts on the CORRECT clone and passes on the stale one. New form, two-sided:
  **HALT if the path contains `OneDrive`; HALT unless it ends with `C:/Naiad`.**
- **Three documents carry the old definition and are amended in Phase A:**
  `exchange/status/CONVENTIONS.md` (the project's definition of "Local"),
  `prompts/CONTRACT_v4_ANALYTICS1_BRIEF2_FORWARD0.md`, and the **SEQ8 queue contract** (DIONYSUS's).
  If your lane quotes the OneDrive test anywhere else, fix it.
- **COWORK LANES — HERMES and DIONYSUS: your mount breaks and you cannot tell.** The attached
  `naiad` folder points at the old path. After the move you would read a **frozen tree** and file
  confident reports about a bus that stopped moving. The operator re-attaches at `C:\Naiad`;
  until he confirms it, treat any repo read as suspect.
- **Web lanes (APOLLO, ARGUS, ATHENA) are unaffected** — the project box syncs from GitHub by repo
  and branch, not by local path.

## 2 · Files that MOVED today — update citations

| was | now | whose |
|---|---|---|
| `exchange/reports/MC1_results.json` | `research_outputs/mc1/MC1_results.json` (+ `.pointer.md` stub on the bus) | APOLLO |
| `exchange/reports/WF1_discriminants.json` | `research_outputs/wf1/WF1_discriminants.json` (+ stub) — **now git-tracked** | APOLLO |
| `exchange/reports/INTERFACE_2026-08-06_C6.md` | `exchange/status/INTERFACE_PUBLISHED.md` (status/ never rotates) | ARGUS |
| `Cascade_Atlas_CENSUS_1b.html`, `..._v2_1.html` (repo root) | `docs/history/atlases/` | APOLLO |
| `HANDOFF_ATHENA_2026-08-03_FULL_STATE_1.md` (root) | `docs/history/` | ATHENA |
| `PRIMER_HERMES_2026-08-03_v2_FIRST_RUN.md` (root) | `docs/primers/` | HERMES |
| `Cascade Rewire.html` (root) | **DELETED** — byte-identical twin at `docs/reports/Cascade Rewire.html` | DIONYSUS |
| `SS_Reassessment_Synthesis_2026-08-03.md` (root) | **DELETED** — twin at `exchange/reports/` | APOLLO |

Both deletions were made only after four checks each: sha256 equal to twin · twin tracked · twin's
blob present on origin · twin's worktree bytes equal that blob. **Nothing unique was removed.**

`scripts/mc1_program.py` and `scripts/mc1_report.py` were already in place and are now **tracked** —
they had existed on one machine only.

## 3 · Rules that now bind every lane

- **Ruling "append" (operator, 2026-08-12):** every build document ENDS by appending its session's
  STATUS to the commissioning lane's `exchange/status/LEDGER_<LANE>.md`, in the same session.
  **A report without its ledger entry is an incomplete deliverable.** This also restores the
  inbox test: *acted* = the recipient's ledger references the note.
- **`BUILT:` stamp (queue/README.md rule 6):** a queue item carries `BUILT: <artifact or commit>`
  once delivered. **Partially built is not built.** Current truthful counters: **6 total · 0
  unratified · 2 ratified-unbuilt** (001 condensed history, 003 rotation) — that is the real backlog.
- **§4.2 named exception:** `exchange/status/MANIFEST.json` and `status/daily/MANIFEST_*.json` are
  exempt from the text-only rule — bus-resident by purpose. **No other data file inherits this.**
- **A single failed lookup measures that lookup, not absence** — of a file, a task, or a disk.
- **R3, data residency, pointer discipline** — unchanged, see the 2026-08-11 notes.

## 4 · Machinery that changed underneath you

- **`publish()` now prints when the ROUTINE last completed** (F-P6), read from `HEARTBEAT.md`, which
  publish never writes. A dead routine can no longer hide behind a freshly refreshed manifest — it
  printed `*** STALE >36h ***` on its first live run and was right.
- **Backups now default to `D:/naiad-backups`** (moved off `G:` by the operator; Drive mirrors it).
  The two Sunday tasks still override with an explicit `--dest` to `G:` — open item O-6.
- **`WORKFLOW_SOURCES` widened** to `briefs/`, `docs/reports/`, `docs/handoffs/` — 343 members,
  0 mismatches. `research_outputs/` remains OUT: widening it pulls in the multi-GB study estate.
- **The retention report can now tell "I looked and found nothing" from "I could not look"** — an
  unmounted drive prints `NOT ENUMERABLE`, never `none found`, and falls back to the nine tracked
  sidecars.
- **`scripts/drive_wait.py` exists** (queue 004 D-0a): three states — PRESENT / WOKE / UNREACHABLE —
  and it logs its own wake latency. **Not yet wired into other scripts** (D-0b). Any NEW contract
  touching `D:` should call it rather than a bare existence check.
- **Rotation is built but idle:** `scripts/rotate_reports.py` moves `exchange/reports/*.md` older
  than 30 days to `docs/history/reports/YYYY-MM/`. **Zero candidates until ~2026-08-28** (oldest
  reports are dated 07-28). Your ledgers, queue items and unacted notes are exempt by scope.

## 5 · What each lane owes

- **APOLLO** — update the four moved paths above; acknowledge in `LEDGER_APOLLO.md`. Census-2 is the
  first contract to be written native to `D:` residency and to call `drive_wait`.
- **ARGUS** — `INTERFACE_PUBLISHED.md` is the bus copy and fixture **F-AN-15** now enforces
  byte-identity with `analytics/INTERFACE.md`; a drift will fail the suite, not go unnoticed.
- **HERMES** — your DIGEST needs the moved paths, the truthful queue counters, and the new gate.
  **Your scheduled task still does not exist.** Re-attach your mount after Phase A.
- **DIONYSUS** — the SEQ8 queue contract's identity gate is amended in Phase A; `Cascade Rewire.html`
  now lives only at `docs/reports/`. Your SEQ8 verdict criteria remain owed.

— ATHENA, 2026-08-12
