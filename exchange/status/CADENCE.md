# CADENCE — the trigger registry

Every trigger that can make something happen without a human typing it, plus the one that still needs
a human. Maintained alongside the lane ledgers; HERMES stamps staleness against it.

Created 2026-08-02 by HEPHAESTUS (rulings Q-4 A, gates A-4a / A-5a).

| # | trigger | when | owner | state | verified |
|---|---|---|---|---|---|
| 1 | **Naiad daily routine** | every day 07:00 local | machine (Windows Task Scheduler) | **ARMED this session** | 2026-08-02 |
| 2 | **Naiad weekly backup** | Sundays 08:00 local | machine (Windows Task Scheduler) | **ARMED this session** | 2026-08-02 |
| 3 | **Hermes scheduled run** | 2×/day | HERMES (Cowork, remote) | **NOT ARMED — Hermes-side, pending F4** | — |
| 4 | **Sync now** (project GitHub sync) | on demand, ~1×/day | operator | **MANUAL — no automation exists** | — |

---

## 1 · Naiad daily routine — ARMED

- **Registered:** 2026-08-02, `schtasks /create /XML`, Task Scheduler name `\Naiad daily routine`.
- **Runs:** `C:\venvs\naiad\Scripts\python.exe scripts\daily_routine.py`
- **Start in:** `C:\Users\luisf\OneDrive\Desktop\Midas-Claude Code Resources\naiad`
- **Schedule:** Daily, every 1 day, 07:00. **Next run at registration: 2026-08-03 07:00.**
- **State:** Enabled · Ready · runs as `luisf` (InteractiveToken, least privilege).
- **Does:** manifest job (required) → brief job (optional) → stages outputs into
  `exchange/status/daily/` → **PUBLISH step**: stages `exchange/**` only, guard-checks the index,
  commits and pushes.
- **Caveat:** InteractiveToken means it runs only when this user is logged on. It does not wake the
  machine (`WakeToRun` false) but it will catch up when available (`StartWhenAvailable` true).

## 2 · Naiad weekly backup — ARMED

- **Registered:** 2026-08-02, `schtasks /create /XML`, Task Scheduler name `\Naiad weekly backup`.
- **Runs:** `C:\venvs\naiad\Scripts\python.exe scripts\backup_estate.py --estate --dest "G:\My Drive\naiad-backups"`
- **Start in:** repo root. **Schedule:** Weekly, Sundays 08:00. **Next run at registration: 2026-08-09 08:00.**
- **State:** Enabled · Ready.
- **Guard:** if `G:` is not mounted at run time, the script's environment assertion fails closed and
  exits non-zero rather than writing a partial archive. A missing Drive shows up as a failed run, not
  a silent no-op.
- **Retention:** the script REPORTS against the rule (keep newest 4 estate generations + 1 phase set)
  and **never deletes**. Acting on the report is the operator's call.

## 3 · Hermes scheduled run — NOT ARMED

Ruled at 2×/day (Q-4 A) but deliberately not armed here: it is a Cowork-side schedule, not a Windows
task, and the F4 experiment — whether a scheduled remote run can see the local folder at all — is
still open. Arming it before that answer would be guessing at what the run can reach.
**Blocked on:** F4 (owner DIONYSUS).

## 4 · Sync now — MANUAL, and it stays manual

The project-box GitHub sync refresh is an operator click. No API, no automation, no way around it
today. This is the one recurring human action the waterwheel cannot absorb: the machine pushes,
the operator clicks, every web lane sees current state.
**Owner:** operator. **Cadence:** on demand, roughly once per cycle.

---

**Removal counterparts**, should either armed trigger need to go:

```
schtasks /delete /tn "Naiad daily routine" /f
schtasks /delete /tn "Naiad weekly backup" /f
```
