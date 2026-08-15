# CADENCE — the trigger registry

Every trigger that can make something happen without a human typing it, plus the one that still needs
a human. Maintained alongside the lane ledgers; HERMES stamps staleness against it.

Created 2026-08-02 by HEPHAESTUS (rulings Q-4 A, gates A-4a / A-5a). Extended the same day with the
workflow backup and the F4 finding.

| # | trigger | when | owner | state | verified |
|---|---|---|---|---|---|
| 1 | **Naiad daily routine** | every day 07:00 local | machine (**launchd** `com.naiad.daily`) | **ARMED** | 2026-08-15 |
| 2 | **Naiad weekly backup** (estate) | Sundays 08:00 local | machine (**launchd** `com.naiad.estate`) | **ARMED** | 2026-08-15 |
| 3 | **Naiad weekly workflow backup** | Sundays 08:30 local | machine (**launchd** `com.naiad.workflow`) | **ARMED** | 2026-08-15 |
| 4 | **Hermes scheduled run** | 2×/day | HERMES (Cowork, scheduled) | **NOT ARMED — Hermes-side** | — |
| 5 | **Sync now** (project GitHub sync) | on demand, ~1×/day | **operator** | **MANUAL — no automation exists** | — |

> ### CORRECTION 2026-08-15 (queue 005 M4) — launchd replaces Task Scheduler
>
> Rows 1–3 above previously read **machine (Task Scheduler)**, verified 2026-08-02/04.
> That owner no longer exists: this host is macOS and has no Task Scheduler. Per
> `CONVENTIONS.md`'s own 2026-08-15 note — *"NOTHING is armed today — every job is
> manual until the code lane re-arms it under launchd"* — the three triggers were
> re-armed this session as **user LaunchAgents**, and the rows now name them.
>
> | trigger | label | plist | schedule |
> |---|---|---|---|
> | daily routine | `com.naiad.daily` | `~/Library/LaunchAgents/com.naiad.daily.plist` | `Hour 7, Minute 0` |
> | estate backup | `com.naiad.estate` | `~/Library/LaunchAgents/com.naiad.estate.plist` | `Weekday 0, Hour 8, Minute 0` |
> | workflow backup | `com.naiad.workflow` | `~/Library/LaunchAgents/com.naiad.workflow.plist` | `Weekday 0, Hour 8, Minute 30` |
>
> **The plists are NOT in this repository.** `~/Library/LaunchAgents/` is outside
> `~/Naiad`, so the agents are untracked *by location*, not by omission — the same
> class of fact as the Task Scheduler entries they replace, and the reason this
> registry exists at all. Their verbatim contents are in
> `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-15_M4-LAUNCHD.md`.
>
> **`StartWhenAvailable` came free.** The Windows tasks needed that flag set
> explicitly so a run missed while the machine was off or asleep fired at next
> wake. launchd does this for `StartCalendarInterval` by default: a missed
> calendar job runs when the machine next wakes. The behaviour the old registry
> had to ask for is the behaviour launchd already has.
>
> **The `--dest` problem died with the tasks.** §2 and §3 below record that both
> weekly tasks passed `--dest "G:\My Drive\naiad-backups"` explicitly, outranking
> the code default and targeting a now-empty path. The new agents pass **no
> `--dest` at all**, so `backup_estate.py`'s own default is what applies —
> measured this session as `/Volumes/LaCie/naiad-backups`, and confirmed live by
> the F-M3-6 run. The stale-argument hazard is not fixed so much as removed.
>
> The Windows command lines quoted in §1, §2, §3 and the 2026-08-04 record are
> left verbatim below. They are no longer a description of anything armed; they
> are migration evidence.

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

## 3 · Naiad weekly workflow backup — ARMED

- `backup_estate.py --workflow --dest "G:\My Drive\naiad-backups"`, start-in repo root.
- Weekly, Sundays 08:30 — thirty minutes after the estate backup, so the two never contend
  for the Drive or the repo. **Next run: 2026-08-09 08:30.** Enabled · Ready.
  Registered 2026-08-02; **has never yet fired**, because its first scheduled fire is 2026-08-09.
- Protects the irreplaceable **everything-else**: `docs/memory`, `docs/knowledge`, `skills`,
  `prompts`, `claude`, `exchange`, `docs/primers`, `docs/history`, and the operator-exports drop.
- Same dated + hashed archive shape as the estate mode, same bidirectional verification, same
  no-clobber guard.

> **RECORD 2026-08-04 — a false finding, reversed.** On 2026-08-03 this section was twice edited
> to read NOT ARMED. **That was wrong.** The task has been registered and Ready since 2026-08-02 — verified
> 2026-08-04 by *enumerating* Task Scheduler rather than querying one name: state Ready, next run
> 2026-08-09 08:30, never yet fired, action `C:\venvs\naiad\Scripts\python.exe
> scripts\backup_estate.py --workflow --dest "G:\My Drive\naiad-backups"`.
>
> **Cause of the error:** only the *estate* task was queried by name, and the absence of a result
> for the other was inferred rather than measured. **To claim a thing does not exist, enumerate
> the set — a negative from a single lookup is not a measurement of absence.**
>
> **What was true, and stays true:** the newest workflow archive was dated 2026-08-02 and genuinely
> predated the 08-03/08-04 files, so those files had no off-machine copy until the hand run on
> 2026-08-04. The gap was real; the cause given for it was not. The hand run was the right call.

> **NOTE 2026-08-12 — the archives moved; these two task definitions did NOT.** The command lines
> quoted in §2, §3 and in the 2026-08-04 record above are left verbatim because they are still
> **exactly what Task Scheduler contains** — re-enumerated 2026-08-12, both tasks Ready, both
> passing `--dest "G:\My Drive\naiad-backups"`. They are a true record of a stale configuration,
> which is why they are not rewritten.
>
> What changed around them: the operator moved the backup folder to `D:\naiad-backups`, and
> `G:\My Drive\naiad-backups` is now **empty (0 files, verified 2026-08-12)**. `backup_estate.py`
> gained a default destination of `D:/naiad-backups` the same day — **but an explicit `--dest`
> still wins, and these tasks pass one.** So the next scheduled fire (2026-08-16 08:00 / 08:30)
> writes a fresh generation to the OLD path, splitting the estate across two locations.
> **Editing the two task arguments is an operator decision and is open — see the 2026-08-12
> build report, open item O-2.**
>
> Also correct the §2 guard sentence when those arguments change: the "if `G:` is not mounted"
> wording becomes "if `D:` is not mounted", and the new `backup_dest_root()` halt covers it.
> Last run of both tasks: 2026-08-09, **result 1 (failure)** — unexamined, open item O-3.

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
launchctl bootout gui/501/com.naiad.daily
launchctl bootout gui/501/com.naiad.estate
launchctl bootout gui/501/com.naiad.workflow
```

`bootout` unloads the agent; the plist stays on disk at
`~/Library/LaunchAgents/<label>.plist` and `launchctl bootstrap gui/501 <plist>`
re-arms it. To remove one permanently the operator deletes the plist as well —
that is an operator action, not a scheduled-lane one (§4 no-delete policy).

*(Windows era, superseded 2026-08-15 — kept as migration evidence. These commands
have no effect on macOS and there is no Task Scheduler on this host:)*

```
schtasks /delete /tn "Naiad daily routine" /f
schtasks /delete /tn "Naiad weekly backup" /f
schtasks /delete /tn "Naiad weekly workflow backup" /f
```
