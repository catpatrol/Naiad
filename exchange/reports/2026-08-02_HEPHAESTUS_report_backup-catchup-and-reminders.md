# HEPHAESTUS — estate catch-up, reminder engine, heartbeat

**Filed:** 2026-08-02 · **Lane:** HEPHAESTUS (local Windows Claude Code, working Naiad clone).

---

## STEP 0 — ASSERT

| check | result |
|---|---|
| OS is Windows | PASS — `Windows_NT` |
| pwd is repo root | PASS — `…\Midas-Claude Code Resources\naiad`, `LEDGER.md` present |
| branch | PASS — `v12-v1-census` |
| **HEAD at start** | **`a654418`** |
| porcelain at start | 0 — clean and synced |
| `G:` reachable | yes |

Assert satisfied; proceeded.

---

## 1 · ESTATE GAP CLOSED — **7/7 FIXTURES PASS**

```
estate root      : C:\Users\luisf\AppData\Local\naiad\data_cache
NAIAD_CACHE_DIR  : (unset)
inside OneDrive  : False
members to archive: 73

PASS F-K1 - 73/73 members verified both directions; 0 mismatches, 0 strays, 0 omissions
PASS F-K2 - census 60/60 klines, 10/10 funding; 0 unresolved
PASS F-K3 - 20-file sha sample unchanged: True; git porcelain identical: True
PASS F-K4 - 10 members restored outside repo; 0 hash mismatches
PASS F-K5 - re-read from destination: matches=True, sidecar matches=True, CRC clean=True, 73 members
PASS F-K6 - guard refuses to overwrite the archive just written
PASS F-K7 - 3/3 git-tracked source files still present on disk; 0 missing
```

| field | value |
|---|---|
| **archive** | `G:\My Drive\naiad-backups\naiad_estate_2026-08-02.zip` |
| **size** | **493,542,600 B** (470.7 MB, 75.5% of source) |
| **sha256** | **`f1e901d23fee71266e8db01ca7bd9436764b18cfd2786fa2588bc4ce4a7873d6`** |
| members | 73 |
| elapsed | 93.7 s |

**The gap is closed.** The previous generation was 2026-07-28; the next automatic one was not due
until 2026-08-09, leaving the estate on a single five-day-old copy.

### Reconciliation against the 2026-07-28 baseline

The baseline's own embedded manifest reads **73 members / 652,451,079 B** — which resolves the
figure in the instruction: **70 estate files (652,375,055 B) + 3 repo companion files (76,024 B)**.
The companions are `_repo/census.json`, `_repo/DATA_CENSUS.md` and
`_repo/research_outputs/census/build_manifest.json`.

| | 2026-07-28 | 2026-08-02 | delta |
|---|---:|---:|---:|
| file_count | 73 | 73 | **0** |
| total_bytes | 652,451,079 | 654,038,380 | **+1,587,301** |
| repo_head | `97f0eee0f0f7` | `a65441894c6d` | — |

**Added: 0. Removed: 0. Changed: 70. Identical: 3.**

Every byte of the delta is accounted for: `+1,587,301` from changed files, `+0` from added, `+0` from
removed — matching the manifest total exactly. The 3 identical files are the repo companions, which
have not moved since. **No symbol was gained or lost; the estate is the same 70 files, five days
further along.**

**Why it changed, precisely — and one of the two reasons is not "more data":**

- **68 of 70 files grew**, by amounts proportional to their timeframe: `BTCUSDT_1m` +194,215 B,
  `ETHUSDT_1m` +149,723 B, the 12h files a few hundred bytes each. That is five days of new closed
  candles appended, exactly as expected.
- **3 LITUSDT files SHRANK**: `LITUSDT_1m` **−61,335 B**, `LITUSDT_5m` **−21,665 B**,
  `LITUSDT_15m` **−379 B**. This is not data loss. The baseline was created 2026-07-29T00:18Z; the
  **LIT estate remediation** landed after it, in commits `4257067` and `f1dc026` (*"enforce the
  symbol floor at the cache persistence boundary; LIT estate remediation; engine 1.0.12"*, both
  2026-07-29 03:45–03:46). The baseline is therefore the **last archive containing the contaminated
  LIT rows**, and this generation is the first clean one. The shrinkage is the remediation showing up
  in the backup record, five days late.

That second point is worth keeping: **`naiad_estate_2026-07-28.zip` is now the only archived copy of
the pre-remediation LIT data.** If it is ever pruned under the retention rule, that state is gone.

---

## 2 · REMINDER ENGINE — `## 0. ACTION REQUIRED`

`DAILY_<date>.md` now **opens** with the only section that asks the operator to do something.
Everything below it is a record; section 0 is a request. When nothing is overdue it says exactly
`nothing overdue — all cadences current`.

All eight checks are computed from real state, never assumed. Thresholds live in
`scripts/routine_jobs.json` under `reminders`, so tuning them is a config change.

| # | check | source of truth | alert when |
|---|---|---|---|
| a | estate age | newest `naiad_estate_*.zip` in the dest, date parsed from the filename | > 8 days |
| b | workflow age | newest `naiad_workflow_*.zip` | > 8 days |
| c | preference blocks | fenced blocks under PART 1 of `OPERATOR_PREFERENCES.md` | while any is whitespace-only — **naming which** |
| d | operator export | newest file in `<dest>\operator-exports\` | > 35 days, **or empty** |
| e | retention | estate/workflow generations + phase sets vs the rule | any outside — **listed, never pruned** |
| f | OneDrive | `tasklist` process check | not running |
| g | queue | `NNN_*.md` under `exchange/queue/` lacking a real `RATIFIED:` stamp | any — **with item numbers** |
| h | stale published state | mtime of top-level `exchange/status/` files vs the newest estate date | any older |

### An unreachable destination is its own alert

Checks a, b, d and e all read the backup destination. If it cannot be read, they do **not** report
zero days — they report **UNKNOWN**, and a dedicated alert fires. Verified against a bogus drive:

```
**backup destination unreachable** — `Q:\no-such-drive\backups` is not readable.
Estate, workflow, operator-export and retention checks could NOT run;
their state is UNKNOWN, not healthy.
```

Also verified with `backup_dest` removed from the registry entirely — same alert, naming
`(not configured)`. A missing drive must never read as a healthy one.

### One scoping decision, disclosed

Check (h) examines **top-level files of `exchange/status/` only**, not `daily/`. `daily/` is an
append-only archive whose older entries are *supposed* to be old; including it would fire a large
alert on every run and bury the signal the check exists to raise. The check as scoped answers
"is the published lane state older than the last data snapshot?" — which is the useful question.

---

## 3 · HEARTBEAT

`exchange/status/HEARTBEAT.md` — five lines, the single file to eyeball.

**It is written BEFORE the publish step, deliberately.** The whole premise is that a stale timestamp
on GitHub is itself the alert; a heartbeat that always lagged one publish could not do that job. The
cost is that the exit code it carries is the pre-publish one — which the file **says plainly** rather
than implying otherwise, and the publish outcome is one line away in the day's report. A publish
failure also still surfaces as a non-zero scheduled-task result.

---

## 4 · VERIFICATION RUN — end to end

```
  manifest: exit=0 elapsed=4.6s
  brief: exit=0 elapsed=246.0s
  ACTION REQUIRED: 5 item(s) overdue
wrote exchange/status/daily/DAILY_2026-08-02.md
publish: committed 3e3c54f (4 path(s)) and pushed to origin/v12-v1-census
ROUTINE_EXIT=0
```

### `## 0. ACTION REQUIRED` — verbatim

```
## 0. ACTION REQUIRED

**5 item(s) need attention.**

1. **no operator data export yet** — `G:\My Drive\naiad-backups\operator-exports` is empty. Project memory, preferences, instructions and custom style are not in any export, so this folder is the only route for the rest.
2. **retention — generations outside the rule** (listed, never pruned): phase set 2026-07-29: 2 archive(s); phase set 2026-07-27: 6 archive(s)
3. **operator preferences not captured** — 3 of 3 PART 1 blocks still empty: User preferences, Project instructions, Custom style. These exist only in Claude's cloud settings, are excluded from data exports, and can only be pasted by hand.
4. **OneDrive.exe is not running** — the repo lives inside the OneDrive tree, so nothing here is syncing to the cloud right now.
5. **1 queue item(s) awaiting your ratification stamp**: 001. They are requests, not work, until stamped.
```

### `exchange/status/HEARTBEAT.md` — verbatim

```
# HEARTBEAT
run: 2026-08-02T21:38:16Z
exit: 0 (jobs + window; publish outcome in the day's DAILY report)
overdue: 5
archives — estate: 2026-08-02 · workflow: 2026-08-02 · phase: 2026-08-02
```

**Every one of the five alerts is a true outstanding item**, and each has been carried in a report's
"items for the operator" list for several cycles. The difference is that they now appear at the top
of the daily report automatically, every morning, computed rather than remembered — and they will
disappear on their own as each is dealt with.

Checks (a), (b) and (h) correctly stayed **silent**: all three archive classes are dated today, and no
top-level `exchange/status/` file predates them. Silence there is the engine working, not the engine
failing.

---

## 5 · COMMIT AND PUSH

```
[v12-v1-census 109ae61] ops: estate catch-up generation; reminder engine and heartbeat in daily routine
 2 files changed, 299 insertions(+)
To https://github.com/catpatrol/Naiad.git
   3e3c54f..109ae61  v12-v1-census -> v12-v1-census
```

```
$ git log --oneline -3
109ae61 ops: estate catch-up generation; reminder engine and heartbeat in daily routine
3e3c54f exchange: auto-publish 2026-08-02
e994f2d exchange: auto-publish 2026-08-02

$ git status -sb
## v12-v1-census...origin/v12-v1-census
 M exchange/status/daily/DAILY_2026-08-02.md
```

The single dirty file is the documented pattern: sections 8 and 9 are appended to the day's report
*after* the publish step commits it, so those bytes ride the next publish.

`e994f2d` and `3e3c54f` are the estate run's and the routine's own publish steps — both
`exchange/`-only, guard clean, and both authored `catpatrol <catpatrolling@gmail.com>`, confirming
yesterday's identity fix is holding.

**One process note:** the first commit attempt failed. The message contained a quoted section name,
and the inner double quotes broke native-command argument parsing — git read the fragments as
pathspecs (`error: pathspec '0.' did not match any file(s)`). Nothing was committed and staging was
untouched; the commit was re-made with `git commit -F <file>`. Worth remembering as the robust form
for any message containing quotes.

---

## SUMMARY OF VERDICTS

| step | verdict |
|---|---|
| 0 | **PASS** — Windows, repo root, `v12-v1-census`, HEAD `a654418` |
| 1 | **DONE — 7/7** — estate `f1e901d23fee7126…`, 73 members, 0 added / 0 removed, +1,587,301 B fully reconciled; LIT shrinkage explained by the post-baseline remediation |
| 2 | **DONE** — 8 checks, all from real state; unreachable dest raises its own alert (verified two ways) |
| 3 | **DONE** — `HEARTBEAT.md`, 5 lines, written pre-publish so a stale timestamp is the alert |
| 4 | **DONE** — end-to-end run, exit 0; section 0 and heartbeat pasted verbatim above |
| 5 | **DONE** — `109ae61` pushed; clean and synced |

## ITEMS FOR THE OPERATOR

The five live alerts now appear in the daily report automatically, so this list is only what sits
outside it:

1. **`naiad_estate_2026-07-28.zip` is the only archived copy of the pre-remediation LIT data.**
   Consider whether that generation should be exempt from pruning.
2. **Two phase sets (978 MB) remain outside the retention rule** — including 26 KB of analytics
   archives whose only fault is not being newest. The phase rule's shape may deserve revisiting.
3. **The first unattended run is tomorrow 07:00.** Section 0 and the heartbeat will be produced
   without a human present for the first time.
4. Still outstanding, and now self-reporting daily: **configure GitHub sync and click Sync now**.

---

## FILE DISPOSITION TABLE

| path | on disk | git status | committed | pushed | protected by |
|---|---|---|---|---|---|
| `scripts/daily_routine.py` | yes | tracked | `109ae61` | yes (`origin/v12-v1-census`) | GitHub — ⚠ newest `--workflow` archive predates this edit |
| `scripts/routine_jobs.json` | yes | tracked | `109ae61` | yes (`origin/v12-v1-census`) | GitHub — ⚠ same |
| `exchange/status/HEARTBEAT.md` | yes | tracked | `3e3c54f` | yes (`origin/v12-v1-census`) | GitHub — ⚠ created after the newest workflow archive |
| `exchange/status/daily/DAILY_2026-08-02.md` | yes | tracked, **modified** | `3e3c54f` (older content) | partly — appended tail not yet pushed | GitHub |
| `exchange/status/MANIFEST.json` | yes | tracked | `3e3c54f` | yes (`origin/v12-v1-census`) | GitHub — ⚠ workflow copy stale |
| `exchange/status/daily/MANIFEST_2026-08-02.json` | yes | tracked | `3e3c54f` | yes (`origin/v12-v1-census`) | GitHub — ⚠ workflow copy stale |
| `exchange/status/RETENTION.md` | yes | tracked | `e994f2d` | yes (`origin/v12-v1-census`) | GitHub — ⚠ workflow copy stale |
| `exchange/reports/2026-08-02_HEPHAESTUS_report_backup-catchup-and-reminders.md` *(this file)* | yes | untracked | not committed | no | **NOT PROTECTED** until committed |
| `G:\My Drive\naiad-backups\naiad_estate_2026-08-02.zip` | yes | outside repo | n/a | n/a | is itself the backup; sha `f1e901d2…` |
| `G:\My Drive\naiad-backups\naiad_estate_2026-08-02.zip.sha256` | yes | outside repo | n/a | n/a | integrity pin for the above |

**The honest caveat, same as last cycle and now visibly recurring:** every file this paste touched is
**GitHub-only right now**. The newest `--workflow` archive (`fcc260f8…`, taken at 18:22) predates all
of these edits, so its copies of `scripts/daily_routine.py` and the status files are stale, and
`HEARTBEAT.md` is not in it at all. They enter archive coverage at the next `--workflow` run —
Sunday 08:30, or sooner on demand. **A weekly archive cannot be current for daily-churn files; that
is a property of the cadence, not a defect, and it is exactly why check (h) exists.**

---

## METRICS (Q-8)

**Operator actions this session = 1** (one paste).
**Files re-ingested = 0.**
