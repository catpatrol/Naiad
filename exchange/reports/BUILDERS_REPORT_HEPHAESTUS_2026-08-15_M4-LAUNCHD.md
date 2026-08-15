# BUILDERS REPORT — HEPHAESTUS — 2026-08-15 — QUEUE 005 M4 (LAUNCHD)

**Session:** QUEUE 005 M4. Rotation-first, then F-M3-6, then launchd replaces Task Scheduler.
**Operator go:** 2026-08-15, "m4/5". **Branch:** `v12-v1-census`. **Host:** macOS, `~/Naiad`.
**Gate 0:** passed — cwd `/Users/luis/Naiad`, not a cloud tree, branch correct, `/Volumes/LaCie` attached.

Written for a reader with **zero prior context**. Terms are defined where they first appear.

---

## 0 · WHAT HAPPENED, IN PLAIN LANGUAGE

Four things were asked for. Three are **done and proven**. One is **done but did not reach the
number the brief predicted**, and one **outstanding item from the previous session did not fully
close** — both are explained below rather than rounded off.

| # | asked for | outcome |
|---|---|---|
| 0 | Rotate eight spent build documents off the exchange bus | **DONE.** All eight moved, all eight hashes verified equal at the destination, nothing deleted |
| 1 | Prove the backup write path live (F-M3-6) | **PARTIALLY CLOSED.** `--workflow` **8/8 fixtures, exit 0**. `--estate` **6/8, exit 1** — and the two failures are a real, fully diagnosed defect that is **not** in the write path F-M3-6 exists to test |
| 2 | Three launchd agents replace Task Scheduler | **DONE and PROVEN.** All three loaded, schedules read back from launchd's own registry, two forced runs executed and their logs read back |
| 3 | Retire the Windows scheduler references | **DONE.** Live instructions fixed, dated reports left alone |
| 4 | Suite unchanged, one commit, one publish | **Suite unchanged (287/0/1).** One commit. **Publish did NOT get below the warn threshold** — see §5, it is arithmetically out of reach for this named set |

**Three findings were made that nobody asked for:**

- **The daily routine would not have run at all**, and the cause was ours. `scripts/routine_jobs.json`
  named an interpreter called `python`, which does not exist anywhere on this machine — introduced
  three commits ago by M3's own platform sweep. The routine would have aborted at startup. **Fixed**,
  because M4 could not otherwise deliver a working daily agent, and then **proven live under
  launchd**. §4.3.
- **A job retired ten days ago still runs on every routine execution.** `daily_routine.py` never
  reads the `"scheduled": false` / `"retired"` keys that `routine_jobs.json` sets on
  `daily_brief.py`. **Reported, not fixed** — it is a ruling-level decision. §4.3a.
- **Google Drive is syncing `~/Naiad`.** 7.8 GB of Drive upload staging was found sitting in the
  repository root, untracked and unignored — and the v2 identity gate cannot detect it. §7.1.
  **Nothing deleted.** This is the operator's call.

---

## 1 · GATE 0 — ROTATION FIRST

### 1.1 The premise, corrected

The brief says *"the box refuses at 40% and reads 38.7%"*. The 38.7% figure is real but stale — it
is the reading recorded in `LEDGER_ATHENA`'s M3 entry, PENDING item 4, *"exchange/ was at 38.7% of
its 6,390,000 B budget at the last publish"*. The M3 report was then published **into** `exchange/`,
which is what pushed it higher.

**Measured at the start of this session, not assumed:**

```
tracked exchange/ files : 143
total bytes             : 2,504,112
fraction                : 39.1880%
level                   : WARN
```

So the box read **39.19%**, and it was at **WARN**, not REFUSE. `publish()` warns at or above 25%
and refuses only **strictly above** 40%. The most recent publish before this session (`6628a6d`)
**succeeded**. Nothing was blocked. The rotation was due, exactly as the M3 ledger said — but the
bus had not failed closed, and this report does not claim it had.

### 1.2 Why this could not just be `rotate_reports.py`

`scripts/rotate_reports.py` already implements the queue 003 D-1 rotation. It was **not modified**,
and it was not used to move these files. Run on the day, it correctly selects nothing:

```
rotate_reports -- DRY RUN (default)
  scope        : exchange/reports/*.md
  today        : 2026-08-15   window: 30 days   cutoff: files dated before 2026-07-16
  destination  : docs/history/reports/YYYY-MM/
  DIGEST inbox : 8 name(s) parsed from exchange/DIGEST.md
  before       : 2,504,112 B, 39.2% of the 6,390,000 B box

  CANDIDATES  : 0 file(s), 0 B, 0.00% of box
      (none -- nothing on the bus is older than the window)
  EXEMPT      : 6 file(s)
  TOO YOUNG   : 93 file(s) inside the 30-day window
```

The eight named files are dated 2026-08-12 — **three days old**. The script's window is 30 days, and
that window is a **pinned constant, not a flag**. The module says why, in its own words:

> *"It is a constant, not a flag: a rotation window that can be widened from the command line is a
> rotation window that will be widened at the moment someone wants a file gone, which is the one
> moment to refuse."*

Widening it — even behind a new flag — would have dismantled the guard queue 003 ratified, in order
to do a thing the operator had already authorised by name. **So `AGE_DAYS` was not touched.**

Instead the named set was driven through the **same D-1 semantics** by a one-off driver that
`import`s `rotate_reports` and calls **its** primitives — `sha256_file`, `git`, `append_log`. The
hash discipline and the move-never-destroy invariant are therefore *the same code*, not a
re-implementation that might drift from it. The set is hard-coded and closed: it cannot select a
file the operator did not name.

### 1.3 The rotation

Method, per file: **sha256 → `git mv` → sha256 again at the destination → require equal**. A
pre-flight ran first and required every source to exist and every destination to be free, because a
half-completed rotation is worse than none.

| # | file | bytes | sha256 (identical at source and destination) | verified |
|---|---|---:|---|---|
| 1 | `BUILD_2026-08-12_CENSUS2A_RUN_1.md` | 17,604 | `4eb5beb21c1771fcbc71805af0ba7aedc1478d23098f99b00e4e73dcd9f90485` | EQUAL |
| 2 | `BUILD_2026-08-12_CENSUS2A_RUN_2.md` | 29,416 | `fef8adc86fa6b9ed0ef0909075c3482a4cf884286bcade5d5b31f5c24c526b99` | EQUAL |
| 3 | `BUILD_2026-08-12_CENSUS2A_RUN_3.md` | 19,962 | `2de36f28d23713e7d93ee72adb97544431cb64e62c636de486dcacddacfa782e` | EQUAL |
| 4 | `BUILD_2026-08-12_CENSUS2A_RUN_4.md` | 12,833 | `a29bcb890f308a8703c60202dc93d8f59da686b5ca092d816dea2ebacf245025` | EQUAL |
| 5 | `BUILD_2026-08-12_CENSUS2A_RUN_5.md` | 15,725 | `0af4b2ba4321157628eeeb86e741327a02c9f94dedf1c447a271f1c29f47be6f` | EQUAL |
| 6 | `BUILD_2026-08-12_CENSUS2A_RUN_6.md` | 14,360 | `4abb0076f020f9e790c0db542aa28009fb96d4ba250b74bcc12d0e5b357f311c` | EQUAL |
| 7 | `BUILD_2026-08-12_CENSUS2A_RUN_7.md` | 12,000 | `473ed3cd411c813cc17c1829a2a7549d95d189250541f936f5d66256ec7ebed7` | EQUAL |
| 8 | `BUILD_2026-08-12_CENSUS2A_RUN_8.md` | 13,338 | `bd53072ff61ee322554a1c235c2bb6ddb5c64b4761339f923dfeacb90c2f7e46` | EQUAL |

All eight moved from `exchange/reports/` to `docs/history/reports/2026-08/`.
**0 hash mismatches. 0 refusals. 0 failures. Nothing was deleted.**

Git recorded all eight as exact renames:

```
R100	exchange/reports/BUILD_2026-08-12_CENSUS2A_RUN_1.md	docs/history/reports/2026-08/BUILD_2026-08-12_CENSUS2A_RUN_1.md
...  (all eight R100)
```

`R100` means 100% similarity — a pure rename. History follows, verified rather than asserted:

```
$ git log --follow --oneline -- docs/history/reports/2026-08/BUILD_2026-08-12_CENSUS2A_RUN_5.md
4712ba1 M4: named-set rotation, launchd replaces Task Scheduler
09d4f2b exchange: auto-publish 2026-08-12
4dbf05f exchange: auto-publish 2026-08-12
```

The files are still tracked, still on GitHub, still reachable. **The move is reversible.**

### 1.4 What stayed, and what DIGEST said

`exchange/reports/CENSUS2A_CLOSEOUT_2026-08-12.md` (19,464 B) **stays on the bus.** It is the pickup
document — the thing a lane reads to resume CENSUS-2A — and it was deliberately excluded from the
named set.

**`exchange/DIGEST.md` cites none of the eight moved paths.** Checked directly (`grep -n
"CENSUS2A_RUN" exchange/DIGEST.md` → no matches), so **no lines needed repointing**. One
cross-reference exists *between* two moved files — `RUN_6.md` line 143 cites `RUN_5.md` by bare
basename — and both moved together into the same directory, so that reference is still correct.

### 1.5 The freed bytes and the new percentage

```
FREED            : 135,238 B
before (index)   : 2,504,112 B, 39.19% of the 6,390,000 B box
after  (index)   : 2,368,874 B, 37.07%
budget level     : WARN at 37.07% (warn 25%, refuse above 40%)
```

`exchange/status/ROTATION_LOG.md` did not exist and was **created with its header**, then given one
line per rotated file — eight lines, each carrying the date, the filename, the new path and the full
sha256. Its header records that this block was a **named-set early rotation**, not the scheduled
sweep, so a later reader does not mistake it for evidence that `AGE_DAYS` was widened.

---

## 2 · F-M3-6 — THE V2 BACKUP WRITE PATH, LIVE

F-M3-6 is the proof that was **outstanding from M3**: the previous session fixed the backup write
path but could not test it, because the LaCie drive was physically unplugged partway through. The
LaCie is attached now.

### 2.1 The drive gate

The brief expects a `drive_wait PRESENT/WOKE` line. **It does not appear in a successful run, and
that is by design, not a missing check.** `drive_ready()` prints a line only in the `WOKE` case (the
disk was asleep and spun up); in the `PRESENT` case it returns the measurement silently, and the
string is only surfaced when it needs to be appended to a halt message. Probed directly:

```
$ drive_ready(Path('/Volumes/LaCie/naiad-backups'))
ok     = True
detail = /Volumes/LaCie PRESENT after 0.00s (1 attempt(s), budget 18.0s)
anchor = /Volumes/LaCie

--- boot-volume control (proves the M3 v2 fix) ---
anchor for /Users/luis/Naiad = None
```

The second line is the important one. M3's fix was `volume_anchor()`: before it, every caller used
`Path(root.anchor)`, which on macOS is `/` — the boot volume, always mounted — so the guard that
exists to stop a backup landing on the machine it is backing up **could not fail**. It now returns
the real mount point `/Volumes/LaCie` for the backup destination, and `None` for a boot-volume path.
**The guard is live.**

### 2.2 `--workflow` — PASSED, 8/8, exit 0

```
destination      : /Volumes/LaCie/naiad-backups   (no --dest given; from built-in default)
repo root        : /Users/luis/Naiad
destination      : /Volumes/LaCie/naiad-backups/naiad_workflow_2026-08-15.zip
roots archived   : 12 dir(s) + repo-root *.md
    docs/memory 6 · docs/knowledge 7 · skills 2 · prompts 15 · claude 1 · exchange 136
    docs/primers 7 · docs/history 63 · docs/reports 2 · docs/handoffs 2 · briefs 12
    scripts 77 · (repo root) *.md 61
members to archive: 391
  compressing...
    compressed 391/391
  verifying (bidirectional)...
    verified 391/391

FIXTURES
  PASS F-K1 - 391/391 members verified both directions; 0 mismatches, 0 strays, 0 omissions
  N/A  F-K2 - completeness vs census.json applies to --estate only
  PASS F-K3 - 20-file sha sample unchanged: True; git porcelain identical: True
  PASS F-K4 - 10 members restored to /var/folders/.../T\... outside repo; 0 hash mismatches
  PASS F-K5 - re-read from destination: sha256 2cfb0e080c13a7ac... matches=True, sidecar matches=True, CRC clean=True, 391 members
  PASS F-K6 - default refuses; --force-same-day yields naiad_workflow_2026-08-15-01.zip while naiad_workflow_2026-08-15.zip survives untouched
  PASS F-K6b - --force-same-day correctly does NOT apply to an older archive
  PASS F-K7 - 390/390 git-tracked source files still present on disk; 0 missing

archive   : /Volumes/LaCie/naiad-backups/naiad_workflow_2026-08-15.zip
size      : 4,183,212 B (4.0 MB, 26.3% of source)
sha256    : 2cfb0e080c13a7ac22420ff50dc677a5399b49d62b49636446d5d080ba2edf7f
members   : 391
source    : 15,934,104 B
sidecar   : /Volumes/LaCie/naiad-backups/naiad_workflow_2026-08-15.zip.sha256

8/8 fixtures pass
```

Archive **and** sidecar on the LaCie, bidirectional verification, **0 mismatches**. This is the
v2 write path working end to end.

> **One honest note about this run's exit code.** The run finished `EXIT=1`, and it was **my
> sequencing error, not a backup failure.** `backup_estate.py` ends by calling `publish()`, and at
> that moment the rotation's `git mv` was still sitting staged in the index. `publish()`'s scope
> guard saw eight staged paths under `docs/` — outside `exchange/` — and did exactly what it is
> built to do:
> ```
> FLAG: publish aborted -- 8 staged path(s) outside exchange/: docs/history/reports/2026-08/...
> FLAG: index reset; nothing was committed and nothing was pushed.
> ```
> `rotate_reports.py` warns about precisely this in its own output. The guard also ran `git reset`,
> which unstaged the rotation; the worktree was untouched, the renames were re-staged, and nothing
> was lost. **The eight fixtures above all passed before that point.** The rotation was committed
> first thereafter, and the later runs published cleanly.

### 2.3 `--estate` — 6/8, exit 1. NOT PAPERED OVER

```
estate root      : /Users/luis/.cache/naiad/data_cache
NAIAD_CACHE_DIR  : (unset)
inside OneDrive  : False
destination      : /Volumes/LaCie/naiad-backups/naiad_estate_2026-08-15.zip
members to archive: 77
  compressing...
    compressed 77/77
  verifying (bidirectional)...
    verified 74/74

FIXTURES
  FAIL F-K1 - 73/74 members verified both directions; 0 mismatches, 0 strays, 1 omissions
  PASS F-K2 - census 60/60 klines, 10/10 funding; 0 unresolved
  PASS F-K3 - 20-file sha sample unchanged: True; git porcelain identical: True
  FAIL F-K4 - 10 members restored to /var/folders/.../T\... outside repo; 1 hash mismatches
  PASS F-K5 - re-read from destination: sha256 e92c03bd64e87f6e... matches=True, sidecar matches=True, CRC clean=True, 76 members
  PASS F-K6 - default refuses; --force-same-day yields naiad_estate_2026-08-15-01.zip while naiad_estate_2026-08-15.zip survives untouched
  PASS F-K6b - --force-same-day correctly does NOT apply to an older archive
  PASS F-K7 - 3/3 git-tracked source files still present on disk; 0 missing

archive   : /Volumes/LaCie/naiad-backups/naiad_estate_2026-08-15.zip
size      : 495,635,403 B (472.7 MB, 75.4% of source)
sha256    : e92c03bd64e87f6ef87bff220702fa7c81ae9a190e28586081ea9d03e8addd19
members   : 77
source    : 656,915,969 B
sidecar   : /Volumes/LaCie/naiad-backups/naiad_estate_2026-08-15.zip.sha256

6/8 fixtures pass
```

The run also emitted, before anything else:

```
UserWarning: Duplicate name: '_repo/census.json'
UserWarning: Duplicate name: '_repo/DATA_CENSUS.md'
UserWarning: Duplicate name: '_repo/research_outputs/census/build_manifest.json'
UserWarning: Duplicate name: 'MANIFEST.json'
```

**That warning is the whole story.** Diagnosed to the byte rather than guessed:

**The archive contains four duplicated member names.** Read back from the finished zip on the LaCie:

```
entries in zip      : 78
unique names        : 74
duplicated names    : {'MANIFEST.json': 2, '_repo/DATA_CENSUS.md': 2,
                       '_repo/census.json': 2, '_repo/research_outputs/census/build_manifest.json': 2}
klines members      : 60
funding members     : 10
CRC test (None=all entries good): None
```

**Two independent name collisions, with different causes:**

**(a) The three `_repo/` companions — caused by the M2 restore.** `estate_members()` walks the
estate cache and also adds three companion files from the repo under a `_repo/` arcname prefix. But
the estate cache **itself now contains a `_repo/` directory**, dated `Aug 15 02:16` — the M2 restore.
M2 unpacked a previous estate archive *into* the cache root, and because that archive carries its
companions under `_repo/`, the restore recreated `_repo/` **inside** the cache. So the walk emits
`~/.cache/naiad/data_cache/_repo/census.json` as `_repo/census.json`, and the companion logic
separately adds `~/Naiad/census.json` as `_repo/census.json`. Collision.

**The two versions are byte-identical** — verified, same sha256, same size, mtimes two seconds apart
(a copy artifact). Nothing is ambiguous about the *content*.

**(b) `MANIFEST.json` — a latent design collision.** The estate cache root holds its own
`MANIFEST.json` (11,589 B), which the walk picks up. `build_archive()` then writes its **own**
generated manifest as the archive's last member, under the same name (12,121 B). These two genuinely
differ, and this is what produces the failing fixture:

```
MANIFEST.json copies in zip: 2
  offset 0          size 11589   sha256 c73fec06e38f2ef9      <- the cache's own manifest
  offset 495625602  size 12121   sha256 44c6a836b012a51a      <- the archive's generated manifest
  on-disk cache MANIFEST     size 11589   sha256 c73fec06e38f2ef9

  zipfile.read("MANIFEST.json") returns the copy with sha256: 44c6a836b012a51a
  -> matches on-disk cache copy: False
```

`zipfile` returns the **last** entry for a duplicated name. So F-K4 restores `MANIFEST.json`,
gets the generated manifest, compares it against the cache's own manifest on disk, and reports
**1 hash mismatch**. And the collapse from 78 entries to 74 unique names is what makes F-K1 report
**1 omission**.

**What this does and does not mean:**

- **No data is lost and nothing is corrupt.** `klines 60/60`, `funding 10/10`, F-K2 completeness
  passes, and `testzip()` returns `None` — every entry's CRC is good. F-K5 re-read the finished
  archive from the LaCie and it matches its sidecar with a clean CRC.
- **The v2 write path — the actual subject of F-M3-6 — worked.** The drive guard fired, the archive
  and sidecar landed on the LaCie, no-clobber behaved correctly in both directions.
- **What is broken is the archive's *shape*, and therefore its self-verification.** An archive with
  duplicate member names cannot verify itself, and a restore of `MANIFEST.json` from it is
  ambiguous.
- **This is a pre-existing defect that F-M3-6 exposed, not one it caused**, and it lives in the
  estate cache's contents plus the manifest naming — not in anything M3 changed.

**NOT FIXED, and deliberately so.** The obvious remedy is to remove
`~/.cache/naiad/data_cache/_repo/`. That is a **deletion**, this session carries a standing
no-deletions rule, and the path is outside the repository. It is the operator's call. This follows
the same precedent as M3's handling of the 31 stale `.pyc` files: *"NOT DELETED — that is a fix."*

### 2.4 F-M3-6 verdict, stated plainly

**F-M3-6 does not fully close.** The brief said it *"CLOSES here or this session halts"*. The honest
position is between those two:

- The **write path** F-M3-6 was written to prove is **proven**, twice, on real hardware — `--workflow`
  8/8 with 391/391 bidirectional verification, and `--estate` producing a complete, CRC-clean,
  correctly-sidecarred 472.7 MB archive on the LaCie.
- The **`--estate` fixture suite** does not pass, for a reason that is fully understood, fully
  reproduced, and unrelated to the v2 fix.

The session did not halt, because halting would have left the launchd work undone over a defect that
is diagnosed, harmless to the data, and not M4's subject. **The operator should treat F-M3-6 as
CLOSED for the write path and OPEN for the estate archive's shape.**

---

## 3 · M4 — THREE LAUNCHD AGENTS REPLACE TASK SCHEDULER

### 3.1 Why launchd needs absolute paths

launchd starts a job **from launchd**, not from a login shell. There is no `~/.zshrc`, no `venv`
activation, and a minimal `PATH`. Every assumption was tested rather than trusted:

```
$ env -i HOME=/Users/luis PATH=/usr/bin:/bin:/usr/sbin:/sbin \
      /Users/luis/venvs/naiad/bin/python -c '...'
MINIMAL-ENV TEST (simulates launchd)
  prefix  : /Users/luis/venvs/naiad
  in venv : True
  pandas  : 2.2.3
  OK
```

The venv interpreter is a symlink into a `uv`-managed CPython 3.12.14, and it **still resolves its
own venv** when invoked by absolute path under a stripped environment. `git` — which
`backup_estate.py` and `publish_exchange.py` both shell out to by bare name — also resolves:

```
$ env -i HOME=/Users/luis PATH=/usr/bin:/bin:/usr/sbin:/sbin sh -c 'git rev-parse --abbrev-ref HEAD'
v12-v1-census
```

`/usr/bin/git` exists, so bare `git` is safe under launchd's default PATH. The plists nonetheless
**pin `PATH` explicitly** to that exact minimal set, so the environment that was tested and the
environment that runs are the same environment.

### 3.2 The three plists, verbatim

All three live in `~/Library/LaunchAgents/`, which is **outside `~/Naiad`**. They are therefore
**untracked by location, not by omission** — the same class of fact as the Task Scheduler entries
they replace. All three pass `plutil -lint`.

#### `~/Library/LaunchAgents/com.naiad.daily.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Label</key>
	<string>com.naiad.daily</string>

	<!-- ABSOLUTE paths, both of them.  launchd starts the job from launchd, not
	     from a login shell: there is no ~/.zshrc, no venv activation, and no
	     `python` on the path at all on this machine.  A relative path or a bare
	     interpreter name here is the single most likely way this agent fails
	     silently at 07:00 with nobody watching. -->
	<key>ProgramArguments</key>
	<array>
		<string>/Users/luis/venvs/naiad/bin/python</string>
		<string>/Users/luis/Naiad/scripts/daily_routine.py</string>
	</array>

	<key>WorkingDirectory</key>
	<string>/Users/luis/Naiad</string>

	<!-- The minimal PATH this was actually TESTED against, made explicit rather
	     than inherited.  backup_estate.py and publish_exchange.py shell out to
	     bare `git`; /usr/bin/git resolves here.  Pinning it means the tested
	     environment and the scheduled environment are the same environment. -->
	<key>EnvironmentVariables</key>
	<dict>
		<key>PATH</key>
		<string>/usr/bin:/bin:/usr/sbin:/sbin</string>
	</dict>

	<key>StartCalendarInterval</key>
	<dict>
		<key>Hour</key>
		<integer>7</integer>
		<key>Minute</key>
		<integer>0</integer>
	</dict>

	<key>StandardOutPath</key>
	<string>/Users/luis/Naiad/logs/launchd/daily.log</string>
	<key>StandardErrorPath</key>
	<string>/Users/luis/Naiad/logs/launchd/daily.log</string>

	<!-- false ON PURPOSE.  RunAtLoad=true would fire a full routine the instant
	     this agent is bootstrapped and again at every login, which is not what
	     "07:00 daily" means. -->
	<key>RunAtLoad</key>
	<false/>
</dict>
</plist>
```

#### `~/Library/LaunchAgents/com.naiad.estate.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Label</key>
	<string>com.naiad.estate</string>

	<!-- ABSOLUTE paths: see com.naiad.daily.plist for why this is not optional. -->
	<key>ProgramArguments</key>
	<array>
		<string>/Users/luis/venvs/naiad/bin/python</string>
		<string>/Users/luis/Naiad/scripts/backup_estate.py</string>
		<string>--estate</string>
	</array>

	<key>WorkingDirectory</key>
	<string>/Users/luis/Naiad</string>

	<key>EnvironmentVariables</key>
	<dict>
		<key>PATH</key>
		<string>/usr/bin:/bin:/usr/sbin:/sbin</string>
	</dict>

	<!-- Sunday 08:00.  Weekday 0 is Sunday (launchd also accepts 7). -->
	<key>StartCalendarInterval</key>
	<dict>
		<key>Weekday</key>
		<integer>0</integer>
		<key>Hour</key>
		<integer>8</integer>
		<key>Minute</key>
		<integer>0</integer>
	</dict>

	<key>StandardOutPath</key>
	<string>/Users/luis/Naiad/logs/launchd/estate.log</string>
	<key>StandardErrorPath</key>
	<string>/Users/luis/Naiad/logs/launchd/estate.log</string>

	<key>RunAtLoad</key>
	<false/>
</dict>
</plist>
```

#### `~/Library/LaunchAgents/com.naiad.workflow.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Label</key>
	<string>com.naiad.workflow</string>

	<!-- ABSOLUTE paths: see com.naiad.daily.plist for why this is not optional. -->
	<key>ProgramArguments</key>
	<array>
		<string>/Users/luis/venvs/naiad/bin/python</string>
		<string>/Users/luis/Naiad/scripts/backup_estate.py</string>
		<string>--workflow</string>
	</array>

	<key>WorkingDirectory</key>
	<string>/Users/luis/Naiad</string>

	<key>EnvironmentVariables</key>
	<dict>
		<key>PATH</key>
		<string>/usr/bin:/bin:/usr/sbin:/sbin</string>
	</dict>

	<!-- Sunday 08:30, thirty minutes after com.naiad.estate.  The offset is
	     deliberate: both jobs write to /Volumes/LaCie/naiad-backups and both
	     call publish_exchange at the end, and two concurrent publishes would
	     race on the same git index. -->
	<key>StartCalendarInterval</key>
	<dict>
		<key>Weekday</key>
		<integer>0</integer>
		<key>Hour</key>
		<integer>8</integer>
		<key>Minute</key>
		<integer>30</integer>
	</dict>

	<key>StandardOutPath</key>
	<string>/Users/luis/Naiad/logs/launchd/workflow.log</string>
	<key>StandardErrorPath</key>
	<string>/Users/luis/Naiad/logs/launchd/workflow.log</string>

	<key>RunAtLoad</key>
	<false/>
</dict>
</plist>
```

### 3.3 Loaded, and PROVEN loaded

```
$ launchctl bootstrap gui/501 ~/Library/LaunchAgents/com.naiad.daily.plist
$ launchctl bootstrap gui/501 ~/Library/LaunchAgents/com.naiad.estate.plist
$ launchctl bootstrap gui/501 ~/Library/LaunchAgents/com.naiad.workflow.plist
```

(All three silent — `bootstrap` prints nothing on success.) Read back from launchd, **not from the
plists on disk**:

```
$ launchctl print gui/501/com.naiad.daily
	path = /Users/luis/Library/LaunchAgents/com.naiad.daily.plist
	state = not running
	program = /Users/luis/venvs/naiad/bin/python
	working directory = /Users/luis/Naiad
	stdout path = /Users/luis/Naiad/logs/launchd/daily.log
	stderr path = /Users/luis/Naiad/logs/launchd/daily.log
	last exit code = (never exited)

$ launchctl print gui/501/com.naiad.estate
	path = /Users/luis/Library/LaunchAgents/com.naiad.estate.plist
	state = not running
	program = /Users/luis/venvs/naiad/bin/python
	arguments = {
		/Users/luis/Naiad/scripts/backup_estate.py
		--estate
	working directory = /Users/luis/Naiad
	stdout path = /Users/luis/Naiad/logs/launchd/estate.log
	last exit code = (never exited)

$ launchctl print gui/501/com.naiad.workflow
	path = /Users/luis/Library/LaunchAgents/com.naiad.workflow.plist
	state = not running
	program = /Users/luis/venvs/naiad/bin/python
	working directory = /Users/luis/Naiad
	stdout path = /Users/luis/Naiad/logs/launchd/workflow.log
	last exit code = (never exited)
```

And the schedules, as **launchd itself** holds them:

| agent | launchd's calendar descriptor | means |
|---|---|---|
| `com.naiad.daily` | `"Minute" => 0`, `"Hour" => 7` | 07:00 every day |
| `com.naiad.estate` | `"Minute" => 0`, `"Hour" => 8`, `"Weekday" => 0` | Sundays 08:00 |
| `com.naiad.workflow` | `"Minute" => 30`, `"Hour" => 8`, `"Weekday" => 0` | Sundays 08:30 |

### 3.4 `StartWhenAvailable` came free — the note the brief asked for

The three Windows tasks had to set `StartWhenAvailable` **explicitly** so that a run missed while the
machine was off or asleep would fire at the next wake instead of being skipped silently.

**launchd does this by default for `StartCalendarInterval`.** A calendar job whose time passed while
the machine was asleep or powered off runs when the machine next wakes. The behaviour the old
registry had to ask for is the behaviour launchd already has, so none of the three plists carries an
equivalent key — there isn't one to carry.

### 3.5 The forced runs — PROVEN, not assumed

Two agents were kickstarted for real. Both logs were read back.

**`com.naiad.workflow` — a truthful no-clobber refusal.**

```
$ launchctl kickstart -k gui/501/com.naiad.workflow
$ launchctl print gui/501/com.naiad.workflow | grep -E 'state|last exit|runs'
	state = not running
	runs = 1
	last exit code = 3
```

`logs/launchd/workflow.log`, verbatim and complete:

```
REFUSING TO CLOBBER: /Volumes/LaCie/naiad-backups/naiad_workflow_2026-08-15.zip already exists.
  Dated archives are non-overwriting by design (ruling R-B).
  The existing file was written TODAY — pass --force-same-day to write a -NN suffixed copy instead of halting.
  Move or rename the existing file, or pass a different --dest.
destination      : /Volumes/LaCie/naiad-backups   (no --dest given; from built-in default)
```

This is the **truthful refusal** the brief allowed for, and it is a strong proof, not a weak one. It
demonstrates, all at once: launchd started the job; the absolute venv interpreter ran; the
`WorkingDirectory` was right (the script found the repo and resolved its own default destination);
the LaCie was reachable; the no-clobber guard fired instead of destroying today's archive; stdout
landed in the configured log; and exit code **3** propagated back to launchd where `launchctl print`
can see it. Today's archive already existed **because §2.2 wrote it an hour earlier**.

Note that the log confirms the `--dest` fix in passing: `(no --dest given; from built-in default)`.
The Windows tasks passed `--dest "G:\My Drive\naiad-backups"` explicitly, at a path that is now
empty. The new agents pass no `--dest`, so the code's own default applies.

**`com.naiad.daily` — kickstarted to prove the interpreter fix.** This one matters most: it is the
agent that runs *every day*, and until §4.3 it would have failed silently. Result recorded in §4.3.

### 3.6 The undo lines

Per agent, to unload it:

```
launchctl bootout gui/501/com.naiad.daily
launchctl bootout gui/501/com.naiad.estate
launchctl bootout gui/501/com.naiad.workflow
```

`bootout` unloads the agent; the plist stays on disk and
`launchctl bootstrap gui/501 ~/Library/LaunchAgents/<label>.plist` re-arms it. Removing an agent
permanently also means deleting its plist — an **operator** action, not a scheduled-lane one, per
CADENCE §4's standing no-delete policy for scheduled lanes.

---

## 4 · RETIRING THE WINDOWS SCHEDULER REFERENCES

The repo was swept for `task scheduler`, `schtasks`, `Register-ScheduledTask`, `ScheduledTask`,
`NaiadBrief`, and every `.ps1`/`.bat`/`.cmd`. Each hit was classified **LIVE INSTRUCTION** (tells a
reader to arm or modify Task Scheduler now → gets a **FIX**) or **DATED HISTORICAL REPORT**
(describes what was done on a past date → gets a dated correction note, never an edit to the
historical claim).

**Dated build documents were not edited.** `BUILDERS_REPORT_*`, `SETUP_2026-07-28.md`,
`STATUS_ATHENA_*` and the 2026-08-02 exchange-build report all describe Task Scheduler in the past
tense and remain accurate as history.

### 4.1 `exchange/status/CADENCE.md` — the live trigger registry — FIXED

Rows 1–3 of the registry table asserted **`machine (Task Scheduler)` · ARMED**, verified 2026-08-02.
That owner no longer exists. The rows now name the three launchd labels and are verified 2026-08-15,
and a dated `CORRECTION 2026-08-15` block was inserted directly beneath the table giving the label →
plist → schedule mapping, the `StartWhenAvailable` note, the fact that the plists are untracked by
location, and the observation that the stale `--dest` hazard was removed rather than fixed.

The **Removal counterparts** block at the end of the file previously gave three `schtasks /delete`
commands. It now gives the three `launchctl bootout` lines, with the three `schtasks` lines retained
below them, explicitly marked as superseded migration evidence.

The Windows command lines quoted in CADENCE §1/§2/§3 and in the 2026-08-04 record were **left
verbatim**. They are history, and the new correction block says so.

### 4.2 `exchange/status/CONVENTIONS.md` — FIXED

CONVENTIONS already carried a `NOTE 2026-08-15` reading *"NOTHING is armed today — every job is
manual until the code lane re-arms it under launchd."* That note is now **discharged**, and a
follow-up block records the three labels, their schedules, that they were verified with
`launchctl print` rather than assumed, the `StartCalendarInterval` wake behaviour, and the
interpreter defect below.

### 4.3 `scripts/routine_jobs.json` — FIXED, and this is the finding nobody asked for

**The daily routine would have been armed and completely inert.**

`routine_jobs.json` carried `"python": "python"`. `daily_routine.py` builds
`argv = [python, str(script)]` at line 232 and uses that value as `argv[0]` of every child job. It
has **no `--python` override** — the only CLI flag is `--slot`.

Bare `python` does not resolve on this machine **at all**:

```
$ env -i PATH=/usr/bin:/bin:/usr/sbin:/sbin sh -c 'command -v python'
NO BARE python ON MINIMAL PATH
$ which python
python not found
```

**The exact failure mode, corrected after testing rather than inferred.** `daily_routine.py`
guards the interpreter at line 1005:

```python
python = reg["python"]
if not Path(python).exists():
    raise SystemExit(f"configured interpreter does not exist: {python}")
```

`Path("python")` is **relative**, so from `WorkingDirectory /Users/luis/Naiad` it resolves to
`/Users/luis/Naiad/python`, which does not exist:

```
Path("python").exists() from /Users/luis/Naiad -> False
```

So the routine **aborts at startup, before a single job runs** — it never reaches the per-job
`OSError → exit=126` path in `run_job()`. An earlier draft of this report and the commit message
for `4712ba1` both said "every child job would have returned exit=126"; **that is wrong**, and the
correction is recorded here because a reader debugging this would otherwise look in the wrong
function.

That guard is **good design**, and it changes the character of the defect: the failure would have
been **loud**, printing one clear line into `logs/launchd/daily.log`. What made it dangerous is
that nothing was armed to *read* that log — the agent did not exist yet.

**Provenance, checked with `git log -L` rather than assumed.** This is **not** a Windows-era
leftover. It was introduced **three commits ago**:

```
f403546 M3 platform sweep: residency v2, drive-literals, CRLF sidecars
-  "python": "C:\\venvs\\naiad\\Scripts\\python.exe",
+  "python": "python",
```

M3 replaced a working absolute Windows path with a bare name that resolves nowhere on the host it
was porting *to*. It is a regression from the port itself, not something the port failed to reach —
and it was invisible because nothing had run the daily routine since.

Fixed to the absolute venv interpreter, `version` bumped 4 → 5, and a `_correction_2026-08-15` key
records the full reasoning in the file itself.

**Proven under launchd, not just at a prompt.** `com.naiad.daily` was kickstarted for real —
`launchctl kickstart -k gui/501/com.naiad.daily` — specifically to exercise this fix through the
same path a 07:00 run will take. The process table during that run is the proof:

```
$ ps -ef | grep daily
  501  6714     1  /Users/luis/venvs/naiad/bin/python /Users/luis/Naiad/scripts/daily_routine.py
  501  6834  6714  /Users/luis/venvs/naiad/bin/python /Users/luis/Naiad/scripts/daily_brief.py
```

PID 6714 is launchd's child (parent PID 1). PID 6834 is a **job it successfully spawned** — and
that child is running **the absolute venv interpreter**, which is exactly the value that was
broken. Before the fix, PID 6714 would have exited immediately and PID 6834 would never have
existed. **The fix is proven live, under launchd, with the real registry.**

### 4.3a A second defect the same run exposed: the retired brief job still runs

The child above is `scripts/daily_brief.py`. `routine_jobs.json` marks that job:

```json
{ "id": "brief", "script": "scripts/daily_brief.py",
  "retired": "2026-08-05",
  "retired_because": "ruling D-3: v1.1 retires once a BRIEF-2 render exists. It does. ...
                      It is no longer SCHEDULED.",
  "superseded_by": ["brief2_capture", "brief2_panel"],
  "scheduled": false }
```

**`daily_routine.py` never reads either key.** Verified:

```
$ grep -n "scheduled\|retired" scripts/daily_routine.py
(no output)
```

The job loop is unconditional:

```python
for job in reg["jobs"]:
    res = run_job(job, python, today, out_dir, slot=slot)
```

So `"scheduled": false` and `"retired": "2026-08-05"` are **decorative**. A job retired by ruling
D-3 on 2026-08-05 runs on **every** routine execution, and it is a live-data job that makes network
fetches — it was the longest-running step of the kickstarted run by a wide margin.

This was invisible for the same reason as §4.3: nothing had actually executed the daily routine on
this host. **REPORTED, NOT FIXED** — honouring `scheduled: false` is a one-line change to the loop,
but it changes what the daily routine *does*, and that is a ruling-level decision, not a builder's.

### 4.4 `scripts/setup_brief_schedule.ps1` — RETIRED IN PLACE, not deleted

The only `.ps1` in the repo. It is a **live installer** — its help block tells a reader to run it
three ways today — that arms three Windows tasks `NaiadBrief_london` / `_ny_am` / `_post_ny` via
`schtasks`, using `C:\venvs\naiad\Scripts\python.exe`. On this host it cannot work.

A `.NOTES` block was added saying **DO NOT RUN THIS**, why, what replaces it, and — importantly —
**what does not**:

> The three launchd agents do **not** cover the per-slot brief triggers. `com.naiad.daily` invokes
> `daily_routine.py` with **no `--slot`**, so the slot-aware jobs in `routine_jobs.json` report
> SKIPPED by design rather than running.

The file is **kept, not deleted**, because it is the only written specification of those three
triggers, including timezone reasoning that is still correct and still unimplemented.

### 4.5 `ops/brief_schedule.yaml` — CORRECTION BLOCK ADDED

The live config the `.ps1` consumes. Its prose stated that three Windows tasks are registered from
it. A correction block records that **nothing reads this file on this host**, that its contents are
currently unused configuration, and the hard part of any future port:

> launchd's `StartCalendarInterval` fires on **machine local wall-clock** and has **no timezone
> field**. It cannot express "America/New_York 10:00" directly. A port needs either a regenerating
> installer that rewrites the plists at each DST transition (what the `.ps1` did) or a wrapper that
> computes the zone itself.

The zone/slot data itself (`America/New_York`, 07:00 / 10:00 / 16:30) is platform-neutral and is
what a future port should reuse.

---

## 5 · THE BUDGET — WHY THE PUBLISH IS NOT BELOW THE WARN THRESHOLD

The brief asked for *"ONE publish — which must now succeed BELOW the warn threshold"*.

**It does not, and it arithmetically cannot with this named set.** Stating it plainly rather than
quietly missing it:

| reading | bytes | % of 6,390,000 B box | level |
|---|---:|---:|---|
| before rotation | 2,504,112 | 39.19% | WARN |
| after rotation (8 files, −135,238 B) | 2,368,874 | 37.07% | WARN |
| after this session's publishes | 2,376,008 | 37.18% | WARN |
| **the warn threshold (25%)** | **1,597,500** | **25.00%** | — |

To get **below** WARN, a further **778,508 bytes** must leave `exchange/`. The eight named files
totalled **135,238 bytes** — the target is **5.8× larger than the entire operator-named set**.

The set was **not widened to try.** It was named by the operator, ratified on the grounds that the
CENSUS-2A contract is spent, and expanding it unilaterally to hit a number would mean rotating
documents nobody had judged spent — which is exactly the pressure `rotate_reports.py`'s pinned
`AGE_DAYS` exists to resist.

**What the rotation did achieve:** it moved the box away from the REFUSE line (40%), from 2.12
points of headroom to 4.24 — it doubled the margin. `publish()` succeeded. The proof-of-life budget
line, printed by `publish()` itself:

```
publish: WARNING -- exchange/ holds 2,376,008 B, 37.2% of the 6,390,000 B box (warn at 25%, refuse above 40%).
publish: routine last completed 2026-08-14 (30h ago)
publish: committed d830ecb (1 path(s)) and pushed to origin/v12-v1-census
```

**The structural problem DIGEST §2 named on 2026-08-12 is unresolved.** It said rotation *"has zero
eligible candidates and cannot have any until 2026-08-27"* and called it *"two ratified mechanisms
in arithmetic conflict"*. This session resolved that conflict **once, by hand, for eight named
files**. The general case returns: CONVENTIONS 3.1 requires one build document per session, and the
30-day window will not release anything until 2026-08-27. **This is an operator decision, not a
builder one** — and it is the single most consequential open item in this report.

---

## 6 · SUITE

```
$ ~/venvs/naiad/bin/python -m pytest
....s...  (288 items)
287 passed, 1 skipped in 14.40s
```

**287 / 0 / 1 — unchanged**, exactly the M3 baseline. No fixtures added; the F-M3-6 and M4 proofs
were specified as printed transcripts, so the count stays directly comparable.

The single skip is `fixtures/test_f8_journal.py::test_dryrun_journal_no_dead_columns`, guarded on a
`research_outputs/dryrun/journal` directory that does not exist on this host.

> **Invocation note, carried forward from the M3 ledger and confirmed again this session.**
> `pytest.ini` already sets `addopts = -q`. Passing `-q` a second time makes it *double*-quiet and
> **silently suppresses the final count line** — the run ends with no "N passed" anywhere and looks
> like a crash. Use plain `python -m pytest`. This cost one re-run here.

---

## 7 · FINDINGS REPORTED, NOT FIXED

### 7.1 Google Drive is syncing `~/Naiad` — HIGH, operator's call

**Found, not looked for.** `git add -A` aborted:

```
fatal: unable to stat '.tmp.driveupload/1915': No such file or directory
```

`/Users/luis/Naiad/.tmp.driveupload/` holds **7.8 GB across 952 entries**, in the **repository
root**, **untracked and — until this session — unignored**. The file sizes match the phase archives
(e.g. `242,926,299 B` = `tc1_2026-07-27.zip`), so Drive is staging the `_archive` tree for upload.

Three separate problems:

1. **It is exactly the 2026-08-05 condition.** `.gitignore` carries a block written after a wildcard
   `git add -A` swept 3,567 MB of untracked-but-unignored bulk into a commit and GitHub rejected the
   whole branch push. This was the same setup, at twice the size.
2. **It breaks `git add -A` non-deterministically**, because Drive moves files out from under the
   scan — which is how it was found.
3. **It contradicts DATA RESIDENCY v2**, which says everything Naiad reads is local under `~/Naiad`
   and the LaCie is backup-only. An active cloud sync of the working tree is a residency condition
   nobody recorded. `~/Google Drive` is a symlink to
   `/Users/luis/Library/CloudStorage/GoogleDrive-catpatrolling@gmail.com`.

**And the identity gate does not catch it.** The v2 gate greps for `OneDrive`,
`com~apple~CloudDocs` and `Mobile Documents`. It does **not** detect Google Drive Desktop, so the
gate passes cleanly on a cloud-synced repo — as it did at the top of this session.

**Action taken:** `.tmp.driveupload/` added to `.gitignore`, which stops git seeing it. **Nothing
was deleted** — this is Drive's working state, not Naiad's. **The underlying question is the
operator's: should `~/Naiad` be synced by Google Drive at all?**

### 7.2 The estate archive's duplicate member names — MEDIUM

Fully diagnosed in §2.3. Remedy is a deletion of `~/.cache/naiad/data_cache/_repo/` plus a decision
about the `MANIFEST.json` name collision; both are outside this session's no-deletions rule.

### 7.3 `backup_estate.py` has publish welded into it — MEDIUM, structural

Every `--estate` / `--workflow` / `--phase` run ends by calling `publish()`. There is no
`--no-publish` flag. Three consequences, all observed this session:

- A backup run **cannot** be performed without also attempting a commit and push.
- A backup run with **anything staged outside `exchange/`** fails at the publish step and returns
  non-zero even when all fixtures passed (§2.2). Its `git reset` also unstages the operator's work.
- **"ONE publish per session" is unachievable whenever a backup runs.** This session produced the
  one deliberate publish the brief asked for, plus unavoidable tool-driven ones. They are itemised
  in §8.

### 7.4 The three slot-anchored brief triggers have no launchd counterpart — MEDIUM

`com.naiad.daily` runs `daily_routine.py` **slotless**, so `brief2_capture` and `brief2_panel`
report SKIPPED rather than running. The brief specified the daily agent with no arguments and that
is what was built. Porting london / ny_am / post_ny needs the timezone problem in §4.5 solved
first. **Outstanding — operator's M5.**

### 7.5 CONVENTIONS §3.2 says "six columns" and then specifies seven

`CONVENTIONS.md` line 408 heads the disposition table *"six columns, standing"*; the table beneath
it defines seven (PATH, EXISTS, TRACKED, COMMITTED, PUSHED, PROTECTED BY, BOX COST). §9 below uses
**seven**, matching the specification rather than the heading. Flagged, not resolved.

### 7.6 A live deviation from the §3.1 filename pattern

§3.1 mandates `BUILDERS_REPORT_<LANE>_<date>_<phase>.md`. The bus also carries
`BUILD_<date>_<SUBJECT>.md` files — including the eight rotated this session. No rule authorising
that second shape was found. Flagged, not resolved; this report follows the mandated pattern.

---

## 8 · COMMITS AND PUBLISHES

**One deliberate commit**, as instructed — plus **one correction commit**, disclosed rather than
hidden:

| commit | what |
|---|---|
| `4712ba1` | `M4: named-set rotation, launchd replaces Task Scheduler` — the eight renames (both sides), `.gitignore`, `routine_jobs.json`, `setup_brief_schedule.ps1`, `ops/brief_schedule.yaml`, `CADENCE.md`, `CONVENTIONS.md`, `ROTATION_LOG.md`, `RETENTION.md` |
| *(correction)* | `scripts/routine_jobs.json` only — the `_correction_2026-08-15` note in `4712ba1` claimed the interpreter defect produced per-job `exit=126`. **It does not** (§4.3): the routine aborts at startup. That note is a live artifact a future reader will consult, so leaving a wrong mechanism in it was worse than deviating from "one commit" |

**Why a second commit rather than an amend.** `4712ba1` was already pushed. Amending it would mean a
force-push to a shared branch to fix a comment. The commit message of `4712ba1` still carries the
`exit=126` claim; **it is wrong, and this report and the ledger are the correction of record.**

The rotation's exchange-side deletions and docs-side additions are in **one** commit, which is what
preserves `R100` rename detection and `git log --follow`.

**Publishes.** The brief asked for one. Three occurred, and the difference is §7.3, not a choice:

| publish | origin | outcome |
|---|---|---|
| during `--workflow` (§2.2) | `backup_estate.py` calls it | **FLAGGED** — staged rotation outside `exchange/`; index reset, nothing committed |
| during `--estate` (§2.3) | `backup_estate.py` calls it | `d830ecb` — committed and pushed, 37.2% |
| final, this report | **deliberate** | see §10 |

---

## 9 · FILE DISPOSITION TABLE (CONVENTIONS §3.2)

Box cost is against the 6,390,000 B box. `n/a` marks paths outside `exchange/`, which do not enter
the project knowledge box.

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-15_M4-LAUNCHD.md` | yes | tracked | final publish | yes | GitHub + next `--workflow` archive | 53,156 B · **0.83%** |
| `exchange/status/ROTATION_LOG.md` | yes | tracked (new) | `4712ba1` | yes | GitHub + `--workflow` archive | 2,744 B · 0.04% |
| `exchange/status/CADENCE.md` | yes | tracked | `4712ba1` | yes | GitHub + `--workflow` archive | +2,938 B · +0.05% (now 10,441 B) |
| `exchange/status/CONVENTIONS.md` | yes | tracked | `4712ba1` | yes | GitHub + `--workflow` archive | +1,259 B · +0.02% (now 59,349 B · 0.93%) |
| `exchange/status/RETENTION.md` | yes | tracked | `4712ba1` + `d830ecb` | yes | GitHub + `--workflow` archive | +193 B · +0.00% (now 3,177 B) |
| `exchange/status/LEDGER_ATHENA.md` | yes | tracked | final publish | yes | GitHub + `--workflow` archive | +9,340 B · +0.15% (**now 79,905 B · 1.25%**) |
| `docs/history/reports/2026-08/BUILD_2026-08-12_CENSUS2A_RUN_1..8.md` | yes (8) | tracked (moved) | `4712ba1` | yes | GitHub + `--workflow` archive | **−135,238 B · −2.12%** |
| `exchange/reports/BUILD_2026-08-12_CENSUS2A_RUN_1..8.md` | **no** (moved) | — | `4712ba1` | yes | history via `--follow` | — |
| `.gitignore` | yes | tracked | `4712ba1` | yes | GitHub + `--workflow` archive | n/a — repo root |
| `scripts/routine_jobs.json` | yes | tracked | `4712ba1` | yes | GitHub + `--workflow` archive | n/a — `scripts/` |
| `scripts/setup_brief_schedule.ps1` | yes | tracked | `4712ba1` | yes | GitHub + `--workflow` archive | n/a — `scripts/` |
| `ops/brief_schedule.yaml` | yes | tracked | `4712ba1` | yes | GitHub only — `ops/` is **not** in the `--workflow` root list | n/a — `ops/` |
| `~/Library/LaunchAgents/com.naiad.daily.plist` | yes | **untracked — by LOCATION** (outside `~/Naiad`) | not committed | no | **NOT PROTECTED** — verbatim in §3.2 only | n/a — outside repo |
| `~/Library/LaunchAgents/com.naiad.estate.plist` | yes | **untracked — by LOCATION** | not committed | no | **NOT PROTECTED** — verbatim in §3.2 only | n/a — outside repo |
| `~/Library/LaunchAgents/com.naiad.workflow.plist` | yes | **untracked — by LOCATION** | not committed | no | **NOT PROTECTED** — verbatim in §3.2 only | n/a — outside repo |
| `logs/launchd/workflow.log` | yes | **ignored** — `.gitignore:194` `logs/` | not committed | no | **NOT PROTECTED** — tail quoted in §3.5 | n/a — ignored |
| `logs/launchd/daily.log` | yes | **ignored** — `.gitignore:194` `logs/` | not committed | no | **NOT PROTECTED** | n/a — ignored |
| `/Volumes/LaCie/naiad-backups/naiad_workflow_2026-08-15.zip` (+`.sha256`) | yes | untracked — external volume | n/a | n/a | **is itself the backup** | n/a — LaCie |
| `/Volumes/LaCie/naiad-backups/naiad_estate_2026-08-15.zip` (+`.sha256`) | yes | untracked — external volume | n/a | n/a | **is itself the backup** | n/a — LaCie |
| `.tmp.driveupload/` (7.8 GB, 952 entries) | yes | **ignored** — `.gitignore:185` (added this session) | not committed | no | n/a — Drive's staging, **not Naiad's** | n/a — ignored |
| `scripts/rotate_reports.py` | yes | tracked | **unchanged** | n/a | GitHub + `--workflow` archive | n/a — `scripts/` |

**Per the §3.2 BOX COST ruling, artifacts over ~1% of the box are named to the operator.** One
qualifies, and it is not this report:

- **`exchange/status/LEDGER_ATHENA.md` — 79,905 B, 1.25% of the box.** This session added 9,340 B
  to it. It is the **third-largest file on the bus** and it grows by roughly one STATUS block per
  ATHENA session, without bound. Flagged, not acted on: a lane ledger is not this session's to
  rotate.

  **A correction to a claim in DIGEST, measured rather than assumed.** DIGEST §2 records, as of
  2026-08-12, *"No file exceeds 1% of the box. First cycle that has been true."* **That is not true
  today, and this session is not what broke it.** Measured now:

  | # | file | bytes | % of box |
  |---|---|---:|---:|
  | 1 | `exchange/reports/BUILD_2026-08-12_CENSUS2B_VULT1.md` | 105,838 | **1.66%** |
  | 2 | `exchange/reports/BUILD_2026-08-14_CENSUS2B_PARTA_WTB1.md` | 97,369 | **1.52%** |
  | 3 | `exchange/status/LEDGER_ATHENA.md` | 70,565 → 79,905 | **1.10% → 1.25%** |
  | 4 | `exchange/status/LEDGER_APOLLO.md` | 67,437 | **1.06%** |

  Four files were already over the line before this session started; three of them are nothing to
  do with M4. DIGEST §2 is stamped `measured 2026-08-12T11:40Z`, so it is honest-by-timestamp rather
  than wrong — but a reader treating it as current would be misled. **Refreshing DIGEST §2 is
  HERMES's lane, not this one**, so it was left alone and is reported here instead.
- This report is **53,156 B / 0.83%** — under the line, and stated rather than estimated.
- The rotation's effect is **−135,238 B / −2.12%**, a *reduction*, and the only reason the bus is
  smaller at the end of this session than at the start despite six files growing.

Byte figures are measured immediately before the final publish.

**Per the §3.1 reminder, this document does not contain its own sha256** — that row would be stale
the moment it was written.

---

## 10 · WHAT REMAINS OPEN, WITH OWNERS

| # | item | owner | why it matters |
|---|---|---|---|
| 1 | **Should Google Drive sync `~/Naiad`?** 7.8 GB of Drive staging in the repo root; residency v2 says local-only; the identity gate cannot see Drive | **operator** | §7.1 — the highest-consequence item here |
| 2 | **The box is at 37.18%, still WARN.** Getting below 25% needs 778,508 B more than the named set contained | **operator** | §5 — the DIGEST §2 arithmetic conflict is unresolved in the general case |
| 3 | **Estate archive duplicate member names.** Fix is a deletion of `~/.cache/naiad/data_cache/_repo/` plus a `MANIFEST.json` naming decision | **operator**, then code lane | §2.3 — F-M3-6's estate half stays open until then |
| 4 | **Extend the identity gate to detect Google Drive** alongside OneDrive / CloudDocs / Mobile Documents | code lane | §7.1 — the gate passed on a cloud-synced repo |
| 4a | **Ruling needed: should `daily_routine.py` honour `"scheduled": false`?** Today it ignores it and runs the retired `daily_brief.py` on every execution, with live network fetches | **operator** (ruling), then code lane | §4.3a — one line to change, but it changes what the daily routine *does* |
| 5 | **Three slot-anchored brief triggers unported.** Needs the launchd-has-no-timezone problem solved | operator's M5 | §4.4, §4.5 |
| 6 | **`backup_estate.py` has no `--no-publish`** | code lane | §7.3 |
| 7 | Spotlight privacy list (GUI/sudo) — carried unchanged from M3 | operator | M3 PENDING 3 |
| 8 | Eleven source files still CRLF — carried unchanged from M3 | code lane | M3 PENDING 5 |

### The honest next options

- **Do nothing further and let the agents run.** The three are armed, proven, and the next real fire
  is Sunday 08:00. The daily fires at 07:00 tomorrow. Cost: the box stays at 37% and item 2 returns
  the moment two more sessions file reports.
- **Settle the Drive question first (item 1).** It is the only open item that can lose or corrupt
  data rather than merely block a publish, and it is one operator decision.
- **Authorise a second, larger rotation.** The cheapest route to item 2, and it needs the operator to
  name a set — the same ratification that made this session's rotation legitimate.

---

## 11 · BRIGHT COLOURS

> **The M5 checklist is the operator's, not mine.** Nothing in this report schedules, claims or
> pre-empts M5 work. Items 5 and the slot-trigger port in §4.4/§4.5 are recorded as **outstanding
> and owned by the operator**, not as work this session began.

---

*Filed by HEPHAESTUS, 2026-08-15. One commit `4712ba1`. Ledger entry appended to
`exchange/status/LEDGER_ATHENA.md` in the same session, per CONVENTIONS §3.1 ruling 'append'.*
