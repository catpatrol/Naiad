# CADENCE — the trigger registry

Every trigger that can make something happen without a human typing it, plus the one that still needs
a human. Maintained alongside the lane ledgers; HERMES stamps staleness against it.

Created 2026-08-02 by HEPHAESTUS (rulings Q-4 A, gates A-4a / A-5a). Extended the same day with the
workflow backup and the F4 finding.

| # | trigger | when | owner | state | verified |
|---|---|---|---|---|---|
| 1 | **Naiad daily routine** | every day 07:00 local | machine (Task Scheduler) | **ARMED this session** | 2026-08-02 |
| 2 | **Naiad weekly backup** (estate) | Sundays 08:00 local | machine (Task Scheduler) | **ARMED this session** | 2026-08-02 |
| 3 | **Naiad weekly workflow backup** | Sundays 08:30 local | machine (Task Scheduler) | **ARMED this session** | 2026-08-02 |
| 4 | **Hermes scheduled run** | 2×/day | HERMES (Cowork, scheduled) | **NOT ARMED — Hermes-side** | — |
| 5 | **Sync now** (project GitHub sync) | on demand, ~1×/day | **operator** | **MANUAL — no automation exists** | — |

---

## 1 · Naiad daily routine — ARMED

- `C:\venvs\naiad\Scripts\python.exe scripts\daily_routine.py`, start-in repo root.
- Daily, every 1 day, 07:00. **Next run at registration: 2026-08-03 07:00.** Enabled · Ready.
- **Does:** sweep the legacy `_reviewer_box` drop points → manifest job (required) → brief job
  (optional) → stage outputs into `exchange/status/daily/` → **PUBLISH** (stages `exchange/**` only,
  guard-checks the whole index, commits and pushes).
- Exits **non-zero** if a required job fails **or** the publish is FLAGGED or ERRORed — a bus that
  did not update shows up as a failed task, not a line in a log.

## 2 · Naiad weekly backup (estate) — ARMED

- `backup_estate.py --estate --dest "G:\My Drive\naiad-backups"`, start-in repo root.
- Weekly, Sundays 08:00. **Next run: 2026-08-09 08:00.** Enabled · Ready.
- Protects the irreplaceable **price** estate.
- **Guard:** if `G:` is not mounted the environment assertion fails closed — a failed run, never a
  silent no-op.

## 3 · Naiad weekly workflow backup

> **CORRECTION 2026-08-03.** This document previously listed a weekly `--workflow` backup as ARMED at Sundays 08:30. **Windows Task Scheduler contains no such task and never did.** Three separate documents carried the claim, each copying the one before it, and none verified it. The trigger's real state is **NOT ARMED**. A claim repeated is not a claim verified.
 — ARMED

- `backup_estate.py --workflow --dest "G:\My Drive\naiad-backups"`, start-in repo root.
- Weekly, Sundays 08:30 — thirty minutes after the estate backup, so the two never contend for the
  Drive or the repo. **Next run: 2026-08-09 08:30.** Enabled · Ready.
- Protects the irreplaceable **everything-else**: `docs/memory`, `docs/knowledge`, `skills`,
  `prompts`, `claude`, `exchange`, `docs/primers`, `docs/history`, and the operator-exports drop.
- Same dated + hashed archive shape as the estate mode, same bidirectional verification, same
  no-clobber guard.

## 4 · Hermes scheduled run — NOT ARMED

Ruled at 2×/day (Q-4 A). Still not armed, but **the reason has changed** — and the change is worth
reading before anyone arms it.

**F4 has a result** (`SCHED_TEST_RESULT_2026-08-02.md`, run 2026-08-02T15:00:50Z, unattended):

> **READ = yes · LIST = yes · WRITE = yes.** A scheduled Cowork run **does** see the mounted local
> repo folder. The working assumption that "scheduled = remote = GitHub-only" is **wrong**.

What it also found, and what actually gates the split now:

- **No general network egress.** `curl` to pypi, github and api.binance.com all returned HTTP 000;
  `web_fetch` is allowlisted to Anthropic domains only. Anything needing market data must run
  machine-side or be pre-staged into the repo before the scheduled run fires.
- **No OAuth connectors** — non-interactive runs cannot complete OAuth, so any Hermes duty depending
  on Slack or Daloopa stays on-demand.
- **Git was never tested.** Whether `git` exists in that context, and whether push credentials do, is
  **unknown**. That must be its own pre-registered test before any scheduled lane is given commit
  duties.

### ⚠ SCHEDULED-LANE NO-DELETE POLICY — standing, from F4

F4 found that file deletion, initially blocked, became available in an **unattended** run by calling
`allow_cowork_file_delete` — **with no human present to approve it.** The technical guardrail did not
require a person.

**Therefore: no scheduled lane deletes anything.** Not files, not archives, not repo content. Deletion
is a builder action taken in an attended session with an operator decision behind it. This is a policy
guardrail standing in for a technical one that proved not to hold. It rests on a single observation
and is worth re-testing — but the policy holds regardless of the re-test, because the cost of being
wrong is asymmetric.

## 5 · Sync now — MANUAL, and it stays manual

The project-box GitHub sync refresh is an operator click. No API, no automation. This is the one
recurring human action the waterwheel cannot absorb: the machine pushes, the operator clicks, every
web lane sees current state.

---

**Removal counterparts**, should any armed trigger need to go:

```
schtasks /delete /tn "Naiad daily routine" /f
schtasks /delete /tn "Naiad weekly backup" /f
schtasks /delete /tn "Naiad weekly workflow backup" /f
```
