# NOTE — ATHENA → ALL LANES · 2026-08-12 · **PROJECT STATUS REFRESH AFTER THE MOVE**

**Supersedes the 2026-08-12 CROSS-LANE RECONCILIATION note on every point where they differ.**
Read once. Every claim is builder-verified with full transcripts in
`exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_QUEUE-004-PHASE-A.md`.

---

## 0 · THE HEADLINE — the move is DONE and GREEN

**The working clone now lives at `C:\Naiad`.** Queue 004 Phase A is **ACCEPTED**: every acceptance
criterion met, so the single-`rmdir` rollback was never needed.

| acceptance gate | result |
|---|---|
| tracked files sha256-equal, old vs new | **562 / 562**, zero differ |
| `git rev-parse HEAD` identical | yes |
| `git status --untracked-files=all` byte-identical | yes |
| gitignored bulk | 213 vs 213 files, **0-byte delta**; all five files >100 MB hashed equal |
| full test suite, run **from `C:\Naiad`** | **287 passed / 1 skipped** — identical to baseline |
| daily routine, from `C:\Naiad` | **exit 0**, all four jobs exit 0 — identical |
| `--workflow` backup, from `C:\Naiad` | **0 mismatches / 0 strays / 0 omissions**, 7/7 fixtures |
| members lost in the move | **ZERO** (349→353 is four *additions*, proven by member-list diff) |
| negative gate test | old path **HALTS**, `C:\Naiad` **PASSES**, unrelated dir **HALTS** |
| scheduled tasks repointed, read back from XML | **18 / 18 assertions PASS**, all three Ready |

**⚠ PHASE B HAS NOT RUN.** The old OneDrive tree is **complete, intact and untouched**. Deleting it
is a separate operator go, days from now, after at least one clean scheduled run from the new
location. Until then **two complete clones coexist** — which is exactly why the identity gate is now
two-sided.

### GREENLIGHT — APOLLO IS CLEAR TO PROCEED

**Nothing blocks study work.** Web lanes reach repo content through the project box, which syncs
from GitHub by **repo and branch**, never by local path — so APOLLO, ARGUS and ATHENA are unaffected
by the move itself. The two conditions on new work are simple and are stated in §3: **contracts use
`C:\Naiad` and the two-sided gate**, and **bulk data goes to `D:\Naiad`**. Census-2 may be drafted.

---

## 1 · WHERE EVERYTHING IS — the table of record

| what | location | protected by |
|---|---|---|
| **The working clone (live)** | **`C:\Naiad`** | GitHub `catpatrol/Naiad`, branch `v12-v1-census` |
| The old clone (abandoned, awaiting Phase B) | `C:\Users\luisf\OneDrive\Desktop\Midas-Claude Code Resources\naiad` | — do not use; its gate now halts |
| Python interpreter | `C:\venvs\naiad\Scripts\python.exe` | outside both trees; **did not move** |
| Raw price estate (irreplaceable) | `C:\Users\luisf\AppData\Local\naiad\data_cache` | dated estate archives, below |
| **Bulk data** — phase archives, `seq8`, `seq8_run2`, mirrors | **`D:\Naiad\...`** mirroring repo paths | `D:` + Drive mirror + tracked sidecars on GitHub |
| 9 phase archives (1,043.6 MB, permanent evidence) | `D:\Naiad\research_outputs\_archive` | `.sha256` sidecars tracked in the repo |
| **Backups** — estate, workflow | **`D:\naiad-backups`** | Google Drive mirror (Computers, not My Drive) |
| `seq8` (MC-1 substrate) | local `research_outputs/seq8` **+** `D:\Naiad\research_outputs\seq8` | 15/15 sha-verified mirror |
| `census` + `mc1` substrates | local **+** `D:\Naiad\...` (37 files / 381.1 MB, mirrored during Phase A) | sha-verified at destination |
| Study results — `MC1_results.json` | `research_outputs/mc1/` + pointer stub on the bus | git history + `D:` mirror |
| Study results — `WF1_discriminants.json` | `research_outputs/wf1/` + pointer stub | **git-tracked** on GitHub |
| The bus | `exchange/{status,queue,reports,drops}` + `DIGEST.md` | GitHub + workflow archive |
| Published analytics interface | `exchange/status/INTERFACE_PUBLISHED.md` | fixture **F-AN-15** enforces byte-identity |
| Atlases | `docs/history/atlases/` | GitHub + workflow archive |
| Memory snapshots | `docs/memory/` | GitHub + workflow archive |
| Old lane primers / handoffs | `docs/primers/`, `docs/history/` | GitHub + workflow archive |
| Claude harness sessions + auto-memory | copied to the `C--Naiad` key; **original left intact** | both keys present, 283 files each |

**Scheduled tasks** — all three repointed, `Start In` now `C:\Naiad`, next runs **13-Aug 07:00**,
**16-Aug 08:00**, **16-Aug 08:30**. `StartWhenAvailable`, the principal SID and `LogonType` were all
preserved and read back from XML to prove it.

---

## 2 · LEFTOVER PATHS — the honest list

**The distinction that matters: 283 of the 340 swept hits are PROSE-HISTORY and were deliberately
left.** A build report dated 2026-08-04 that says the repo is inside OneDrive is a **true record of
that date**. Rewriting it would falsify the archive. **If you read "OneDrive" in a dated document,
it is history, not a live path.** Zero old-form absolute `ROOT` constants remain anywhere in the tree.

Five genuine residuals, each owned:

| # | residual | effect | owner |
|---|---|---|---|
| **R-1** | A **fourth identity gate** at `prompts/PC1_Pre_Census_Consolidation_Builder_Contract.md:55/:151/:155` still asserts an OneDrive working directory | It is a **completed** contract (ran 2026-07-29), so it was classified prose-history. **Re-running it would halt.** Named here so no one discovers it by a halt. | ATHENA |
| **R-2** | The **old tree's remote-tracking ref is stale** at `75b7444` while true origin is `b938e81` | A session opened there reports *"up to date"* and shows **a plausible, wrong picture**. The two-sided gate stops this; Phase B removes it. | operator, Phase B |
| **R-3** | **28 of 138** permission rules in `.claude/settings.local.json` name the old path or slug | Degrade to **fresh permission prompts, not failures**. Reported, not edited. | operator, at leisure |
| **R-4** | Two files resurrected into `exchange/reports/` — `BRIEF2_CALIBRATION_2026-08-05.json`, `EXCURSION_EPISODES_2026-08-06.json` | Importing six worksheet modules to prove their ROOT executed them (no `__main__` guard). +12,850 B, +0.201% of the box. **Byte-identical copies remain in `docs/history/argus/`.** Needs a delete-authorised tidy. | operator / next tidy |
| **R-5** | **O-5 is four-deep** — `naiad_workflow_2026-08-12`, `-01`, `-02`, `-03` | Two are this work's own proof runs, so **one calendar day occupies all four keep-slots** and every genuinely distinct older generation reads as outside the rule. Report-only; nothing has ever been deleted by that code. | ATHENA |

**Carried, unchanged:** O-6 (both Sunday tasks still pass `--dest "G:\My Drive\naiad-backups"` — next
fire 16-Aug) · O-7 · O-8 · and three Phase 0 items (per-process UNREACHABLE memo; F-0-1/F-0-3 not
committed as regression tests; the wake log records only WOKE, so an empty log cannot distinguish
*never asleep* from *budget too short*).

---

## 3 · WHAT EVERY LANE MUST DO DIFFERENTLY

1. **Contracts name `C:\Naiad`.** The old absolute path is dead for live purposes.
2. **The environment gate is TWO-SIDED, and both halves are load-bearing while two clones coexist:**
   **HALT if the path contains `OneDrive`; HALT unless it ends with `C:/Naiad`.** A one-sided gate
   would pass in an unrelated directory — the control case in the negative test proves it.
3. **Bulk data goes to `D:\Naiad`** at creation, mirroring repo paths, with a reachability gate that
   **HALTS if the drive is absent** — never a silent laptop fallback. Call
   `scripts/drive_wait.py::wait_for_drive`, not a bare existence check: it distinguishes a *sleeping*
   disk from a *missing* one (**PRESENT / WOKE / UNREACHABLE**) and logs its own wake latency.
4. **Ruling "append" binds you:** every build document ENDS by appending its lane's
   `exchange/status/LEDGER_<LANE>.md` in the same session. A report without its ledger entry is an
   incomplete deliverable.
5. **A single failed lookup measures that lookup, not absence** — of a file, a task, or a disk. And
   its 2026-08-12 sibling, earned four times over: **a whole-file text match is not a placement
   check.** Assert on normalised meaning, and verify a failing check before acting on its verdict.

### Per lane

- **APOLLO — GREENLIT.** Nothing blocks you. Your session-start sources are unchanged
  (`SS_SYSTEM_SYNTHESIS_2026-08-06.md` · `LEDGER_APOLLO.md` · the MC-1 queue item). Census-2 is the
  first contract to be drafted native to `C:\Naiad` paths **and** `D:\Naiad` residency. Update the
  four moved paths in §1 before citing them.
- **ARGUS.** `INTERFACE_PUBLISHED.md` is the bus copy and F-AN-15 fails the suite on drift. R-4's two
  resurrected files are yours by origin — flag if you want them handled differently.
- **HERMES.** ⚠ **RE-ATTACH YOUR MOUNT AT `C:\Naiad`.** Until the operator does, you would read a
  **frozen tree and report it as current**. Your DIGEST needs §1's table, the truthful queue counters
  (6 total · 0 unratified · 2 ratified-unbuilt: 001 and 003), and the five residuals above. Your own
  scheduled task still does not exist.
- **DIONYSUS.** Same mount warning. The SEQ8 queue contract's identity gate was amended in Phase A.
  Your SEQ8 verdict criteria remain owed.

---

## 4 · OPERATOR ACTIONS OUTSTANDING

1. **Re-attach the Cowork folder at `C:\Naiad`** — HERMES and DIONYSUS cannot detect a stale mount.
2. **Open all future Claude Code sessions in `C:\Naiad`.**
3. Let **one clean scheduled day** pass (13-Aug 07:00) before Phase B.
4. **Phase B** — deleting the old tree — on a separate go. Remember: deleting inside OneDrive fills
   the online recycle bin, and **quota is not reclaimed until it is emptied at onedrive.com.**
5. Second Google Drive account upload — stale since 2026-08-05, predates two estate generations.

*`exchange/` sits at 27.5% of the 6.39 MB box (warn 25%, refuse 40%). Rotation is queue 003,
ratified and unbuilt; it has zero candidates until ~2026-08-28.*

— ATHENA, 2026-08-12
