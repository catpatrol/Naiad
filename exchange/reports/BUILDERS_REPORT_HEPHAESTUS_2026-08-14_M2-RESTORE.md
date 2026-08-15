# BUILDER'S REPORT — HEPHAESTUS — QUEUE 005 M2 — THE RESTORE DRILL

**Date:** 2026-08-14 (executed 2026-08-15 local) · **Operator go:** 2026-08-14
**Machine:** Luiss-MacBook-Pro.local · Mac17,6 · Apple M5 Max · macOS 26.3 (25D2125) · arm64
**Branch:** v12-v1-census · **Verdict:** **HALT AT GATE 0 — NOTHING ADOPTED**

---

## VERDICT IN ONE LINE

The restore drill did not run. Three of Gate 0's preconditions failed independently,
and the one that matters most is physical: **the LaCie is not attached to this machine** —
not asleep, not mis-mounted, not renamed. **Zero bytes were adopted. Zero bytes were
written to any source. The ADOPTED ledger below is empty by design, not by omission.**

A fourth blocker surfaced at close: **this Mac has no GitHub credentials**, so the
`publish()` at §6 committed locally (`35c293f`) but could not push. **The branch is 1 commit
ahead of origin and this report is not yet on the remote.**

---

## 0 — IDENTITY GATE

| Check | Required | Observed | Result |
|---|---|---|---|
| pwd | `$HOME/Naiad` | `/Users/luis/Naiad` | **PASS** |
| cloud-sync path | absent | no OneDrive / CloudDocs / Mobile Documents component | **PASS** |
| user / os | — | `luis` · `Darwin arm64` | recorded |
| branch | `v12-v1-census` | `v12-v1-census` | **PASS** |
| HEAD == origin tip | equal | `db63b8c` == `db63b8c` | **PASS** |
| `requirements-lock-2026-08-14-win.txt` | present | **absent** | **HALT 1** |
| `/Volumes/LaCie` mounted | present | **absent** | **HALT 2** |
| `~/venvs/naiad/bin/python` executable | present | **absent** | **HALT 3** |

The operator's own gate script exits 1 at HALT 1 and never reaches steps 1–6.
I honoured that exit rather than improvising past it.

### HALT 1 — M0's lock file did not cross

`requirements-lock-2026-08-14-win.txt` is absent from the working tree **and from all of
git history**: `git log --all --oneline -- 'requirements-lock*'` returns nothing. The only
requirements artefact in the repo is the unpinned `requirements.txt`.

This is not a fetch problem. `git fetch origin` succeeded and the clone is exactly at the
origin tip. The file was never committed and pushed. **M0's push did not cross** — the
gate's own wording is correct.

### HALT 2 — the LaCie is not attached

`/Volumes` contains exactly one entry: `Macintosh HD`.

I did not stop at the mount table, because a spun-down disk and an absent disk look alike
to a single `ls` — the exact conflation `scripts/drive_wait.py` was written to end. I
checked three layers deeper:

- `diskutil list` — only `disk0` (internal 2.0 TB) and its APFS synthesised container. **No external physical device.**
- `mount` — nine entries, all internal APFS / devfs / autofs. **No external filesystem.**
- `system_profiler SPUSBDataType SPThunderboltDataType` — **no LaCie, no Seagate, no external media of any kind.**

And then the project's own helper, which is the authoritative answer (§5 probe, run early
because it doubles as evidence for this gate):

```
$ python3 -c "import scripts.drive_wait as d; print(d.wait_for_drive('/Volumes/LaCie'))"
UNREACHABLE root=/Volumes/LaCie attempts=6 elapsed=18.02s budget=18.0s
```

Six attempts across an 18-second budget, including the spin-up poke. The disk is
**genuinely absent**, not asleep. This is UNREACHABLE in the helper's precise sense, and
it is the strongest available negative: the one tool built to distinguish ASLEEP from
ABSENT was given its full budget and returned ABSENT.

**Consequence:** steps 1, 2, 3 (restore half) and 4 have no source. They are not deferred
by choice; they have nothing to read.

### HALT 3 — no venv, and no interpreter that could host one

`~/venvs` does not exist at all. The only interpreter on this machine is
`/usr/bin/python3` → **Python 3.9.6** (Apple system Python).

This is worse than a missing venv, and it is the finding M1 needs most:

> `engine/data.py:63` declares `def _get(url: str, params: dict | None = None, ...)`.
> PEP 604 `X | None` annotations in a runtime signature require **Python 3.10+**.
> Python 3.9.6 cannot import this module. The repo has no interpreter it can run on.

So M1 step 6 is not a one-command fix on this machine — it needs a Python 3.10+ toolchain
installed first, and it needs the lock file from HALT 1 to pin against. **Two blockers
compose here.**

---

## THE ADOPTED LEDGER

```
(empty)
```

**Files adopted: 0. Files written into ~/Naiad by this session: 1** — this report.
Nothing was copied, extracted, renamed or overwritten. No source was touched: the
COPY-ONLY and NO-CLOBBER constraints were never exercised, because no copy was attempted.

Per-folder counts (adopted / sidecar / manifest / two-witness / single-witness / mismatches)
are **0/0/0/0/0/0** for every folder in §2's list. There is no mismatch to report and no
folder to stop adopting from.

---

## WHAT I ESTABLISHED ANYWAY (all read-only, all free)

The drill is blocked, but four questions could be answered without the LaCie, and three of
them are things M3 will otherwise have to discover the hard way.

### A — The tracked tree needs no restore drill at all

| Measure | Value |
|---|---|
| Tracked files | **598** |
| Modified or deleted tracked files | **0** |
| HEAD vs origin/v12-v1-census | identical (`db63b8c`) |
| Untracked entries | 3 — `.DS_Store`, `.claude/settings.local.json`, `naiad-backups/` |

A clean status at the origin tip is cryptographic proof that all 598 tracked files are
byte-correct. **Git is a stronger witness than any sidecar or two-witness comparison**, and
it already covers the tracked half of the estate for free. The restore drill's real scope
is narrower than §2 implies: it is the *untracked* artefacts and the estate cache, nothing
more.

### B — The working tree was already transplanted, unverified, before this session

This machine's home directory was created **2026-08-14 22:46:37** and it first booted
**22:42:47** — a genuinely new Mac, set up last night. Yet `~/Naiad` is fully populated,
and `git reflog` still shows `clone: from https://github.com/catpatrol/naiad.git` at
**2026-07-09 21:14:32**.

A fresh clone cannot carry a five-week-old reflog. **The entire `~/Naiad` tree — `.git`,
tracked files and untracked files together — was copied onto this Mac wholesale before
this session began.** File mtimes are preserved from July and August, consistent with a
bulk copy tool.

This is the finding the operator most needs to see: **the bulk restore M2 was chartered to
perform carefully has already happened carelessly.** No per-file hash was printed, no
verification basis was recorded, no ledger exists. It landed correct for the tracked half
(proven in A above, after the fact, by git). For the untracked half there is currently
**no evidence either way** — and that half is precisely what the LaCie was to witness.

### C — `cache_dir()` on this platform — resolved, not assumed

Read from `engine/data.py:39-48`, as instructed:

```python
env = os.environ.get("NAIAD_CACHE_DIR")     # unset on this machine (verified)
elif os.name == "nt":  LOCALAPPDATA/naiad/data_cache      # not this platform
else:                  Path.home()/".cache"/"naiad"/"data_cache"
```

**Resolved path on this machine: `/Users/luis/.cache/naiad/data_cache`**

Current state: **`/Users/luis/.cache/naiad` does not exist.** The estate cache is empty —
there is nothing here to no-clobber against, and nothing restored.

One note for whoever does run §3: `cache_dir()` is **not a pure resolver** — line 47 calls
`base.mkdir(parents=True, exist_ok=True)`. Merely asking where the cache is *creates* it.
I therefore resolved the path by reading the source rather than by calling the function, so
that this session left no directory behind. **The `MANIFEST.json` / `manifest.json`
case-collision hazard is unexercised and still live** — APFS is case-insensitive here, so
it carries to this platform exactly as the brief predicts.

### D — The local `naiad-backups/` archives verify clean against their sidecars

`~/Naiad/naiad-backups/` (untracked, carried in by the transplant) holds 18 archives.
Fifteen have sidecars; all fifteen were re-hashed at rest, read-only:

| Archive | sha256 (16) | Result |
|---|---|---|
| analytics_tests_v1.0.0_2026-07-29.zip | `0a1ffc941032acbf` | OK |
| analytics_v1.0.0_2026-07-29.zip | `d3fcd786881dc202` | OK |
| naiad_estate_2026-07-28.zip | `ad94dc6e1e6750bb` | OK |
| naiad_estate_2026-08-02.zip | `f1e901d23fee7126` | OK |
| naiad_estate_2026-08-09.zip | `1b4b4c9f0fd92d45` | OK |
| **naiad_estate_2026-08-11.zip** | `f0cfdb2a56ad4853` | **OK — newest estate present** |
| naiad_workflow_2026-08-02.zip | `fcc260f8c50daeb9` | OK |
| naiad_workflow_2026-08-04.zip | `37d60eda6997ec81` | OK |
| naiad_workflow_2026-08-09.zip | `aa5af72c1be64624` | OK |
| naiad_workflow_2026-08-11.zip | `b2bfbb1649fcd3fa` | OK |
| naiad_workflow_2026-08-12.zip | `b083ccd066bc8d53` | OK |
| naiad_workflow_2026-08-12-01.zip | `21056413e2bd00dc` | OK |
| naiad_workflow_2026-08-12-02.zip | `b286c5d8ae64d3bc` | OK |
| naiad_workflow_2026-08-12-03.zip | `6dfea70d8890a900` | OK |
| tc5_2026-08-02.zip | `68942d6261bf8ca8` | OK |

**15 verified · 0 mismatches.** Three archives carry no sidecar and are unverifiable:
`analytics_tests_v1.0.0_2026-07-29 (1).zip`, `analytics_v1.0.0_2026-07-29 (1).zip`,
`naiad_workflow_2026-08-02 (1).zip` — the ` (1)` suffix is a browser re-download pattern;
each is byte-identical in size to its sidecar'd twin.

**I did not extract any of these.** Two reasons, and I want them on the record rather than
inferred:

1. **The sidecar is not an independent witness here.** It is untracked and sits in the same
   directory as the archive it attests to, carried by the same unverified bulk copy. If the
   transplant corrupted the pair, it corrupted both. This satisfies neither basis (1)
   *repo-tracked sidecar* nor basis (3) *two-witness*. It proves the archive is internally
   self-consistent — genuinely useful, and worth having — but it is **not** the standard
   this drill was written to.
2. **The newest local estate is 2026-08-11.** The ledger records Queue 004 Phase A work
   through 2026-08-12 and M0/M1 ran on 2026-08-14. This set is **at least three days stale**
   and predates the work M2 exists to carry forward. Extracting it would restore a known-old
   estate under a verification basis the brief does not accept, and the LaCie almost
   certainly holds a newer one.

Adopting bytes of unproven provenance is the precise failure this drill exists to prevent.
I verified them and left them where they lie.

### E — What the transplant did *not* bring

Of §2's restore list, checked against the working tree:

| Folder | State | Tracked? |
|---|---|---|
| `_archive` | present — 10 files | tracked |
| `seq8` | present — 15 files | tracked |
| `mc1` | present — 30 files | tracked |
| `census` | present — 7 files | tracked |
| **`seq8_run2`** | **ABSENT** | never tracked |
| **`census2a`** (29 artifacts, manifest-pinned) | **ABSENT** | never tracked |
| **`census2b`** | **ABSENT** | never tracked |

`git check-ignore` returns nothing for these paths and git reports no deletions, so the
three absent folders were **never tracked** — they exist only as untracked artefacts on the
mirror and the carried copy. **They are unrecoverable without the LaCie.** This is the
material loss the halt is protecting, and it is why §2 is not a formality.

---

## 5 — THE MAC SUITE BASELINE

**NOT RECORDED — blocked, not skipped.**

`source ~/venvs/naiad/bin/activate` cannot run (HALT 3), and no interpreter on this machine
can import the codebase (Python 3.9.6 vs the 3.10+ floor at `engine/data.py:63`). Running
the suite under system Python would produce a `SyntaxError` at collection — a number that
looks like a baseline and measures nothing. **There is no Mac baseline yet. M3 must not
treat any figure as one.**

The `drive_wait` probe *was* run and is recorded above (§HALT 2) — the one §5 deliverable
that survived, and the M3-relevant reading is this: **the helper handles a POSIX path
correctly.** It resolved `/Volumes/LaCie`, polled it six times across its full 18-second
budget, poked for spin-up, never raised, and returned a well-formed `UNREACHABLE` result
whose `%`-formatting did not explode. Its docstring worries about surviving a move to
`C:/Naiad`; the answer for the reverse crossing is that the path handling is already
platform-neutral. No drive-letter assumption fired. **`drive_wait` is not an M3 item.**

No suite failure is listed below, and none is tagged `[expect-windows-ism]`, because none
was observed. Per the brief: classify nothing, fix nothing. I have classified nothing.

---

## 6 — CLOSE / PUBLISH

One `publish()` was attempted, as instructed. It got **most of the way and then failed on a
fourth blocker nobody had listed** — HALT 4.

First, a note for M3 on how it is invoked. `scripts/publish_exchange.py` has **no
`__main__` guard**: running it as a script exits 0 and prints nothing at all — a silent
no-op that looks exactly like success. It is a library. The entry point is
`publish(repo, date_str, remote="origin", ...)` at line 228.

It imports and runs cleanly under Python 3.9.6 — `publish_exchange` does not touch the
3.10+ syntax that blocks `engine/data.py`, so HALT 3 did **not** stop it. The result:

| Stage | Outcome |
|---|---|
| branch resolve | OK — `v12-v1-census`, not detached |
| `git add -- exchange` | OK |
| scope guard | **PASS** — exactly 2 staged paths, both inside `exchange/` |
| D3 size budget | PASS — not tripped, no override used |
| commit | **OK — `35c293f`** `exchange: auto-publish 2026-08-14` |
| **push** | **FAILED** |

Staged and committed: `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-14_M2-RESTORE.md`
and `exchange/status/LEDGER_ATHENA.md`. Nothing outside `exchange/` was touched — the
untracked `.DS_Store`, `.claude/settings.local.json` and `naiad-backups/` were correctly
left alone by the scope guard.

### HALT 4 — this Mac has no GitHub credentials

```
$ git push origin v12-v1-census
fatal: could not read Username for 'https://github.com': Device not configured
```

The remote is HTTPS (`https://github.com/catpatrol/Naiad.git`) and no credential helper,
token or SSH alternative is configured on this machine. `Device not configured` is git
finding no TTY to prompt on — it cannot ask, so it dies.

**This is not a Windows-ism.** `publish()` behaved correctly on macOS at every stage it
could control: path handling, scope guard, size budget and commit all worked, and it
returned rather than raising, exactly as its contract promises. The failure is environmental
and belongs to the operator, not to M3's portability work.

**Current state: the branch is 1 commit ahead of origin.** The report and the ledger are
committed locally at `35c293f` and are **not on the remote**. I cannot complete the push —
it needs credentials only the operator can supply.

**Net finding: `publish()` survives macOS as far as this machine let it be tested. Commit
works; push is blocked on credentials, not on code.**

---

## DISPOSITION TABLE

| # | Step | Disposition | Basis | BOX COST |
|---|---|---|---|---|
| 0 | Identity gate | **PASS** (4 of 7 checks) | direct observation | 0 B |
| 0 | Lock file present | **HALT 1** | absent from tree and all history | 0 B |
| 0 | LaCie mounted | **HALT 2** | 4 independent probes incl. `drive_wait` UNREACHABLE | 0 B |
| 0 | venv present | **HALT 3** | `~/venvs` absent; py3.9.6 < 3.10 floor | 0 B |
| 1 | LaCie inventory | **BLOCKED** | no source | 0 B |
| 2 | Substrates restore | **BLOCKED** | no source · 0 adopted | 0 B |
| 3 | `cache_dir()` resolution | **DONE** | read from source, not called | 0 B |
| 3 | Estate restore | **BLOCKED** | no source; local set stale + weak basis | 0 B |
| 4 | Untracked handoff zip | **BLOCKED** | no source | 0 B |
| 5 | Suite baseline | **BLOCKED** | no interpreter | 0 B |
| 5 | `drive_wait` POSIX probe | **DONE — passes** | executed, 18.02 s | 0 B |
| 6 | `publish()` — commit | **DONE** | scope guard + D3 passed; commit `35c293f` | 0 B |
| 6 | `publish()` — push | **HALT 4** | no GitHub credentials on this Mac | 0 B |
| — | Tracked-tree integrity | **VERIFIED 598/598** | git, clean at origin tip | 0 B |
| — | Local archive integrity | **VERIFIED 15/15** | co-located sidecars (weak basis) | 0 B |
| — | This report | committed `35c293f`, push blocked | — | 19.7 KB |

**TOTAL BOX COST: 19.7 KB — this document alone** (plus the LEDGER_ATHENA append). No archive extracted, no cache directory
created, no artefact adopted, no source byte read-modified. `~/.cache/naiad` still does not
exist.

**ROLLBACK:** `git reset --hard db63b8c` drops the local publish commit; then delete this
report and revert the LEDGER_ATHENA append. Nothing left this machine — the push never landed —
so rollback is purely local. No source was touched.

---

## LEDGER_ATHENA — APPENDED

See `exchange/status/LEDGER_ATHENA.md`.

---

# 🔴 BRIGHT COLOURS — WHAT THE OPERATOR MUST DO NEXT

## 🔴 NOTHING ON THE LACIE MAY BE REORGANISED UNTIL M3 ACCEPTS.

That instruction now carries far more weight than when it was written. **Three substrate
folders — `seq8_run2`, `census2a` (29 manifest-pinned artifacts) and `census2b` — exist
nowhere on this Mac and are not in git.** The LaCie mirror and the carried clone are the
only copies in the world. Until they are restored and verified, the LaCie is not a backup
of this machine — **it is the sole original.**

### 🔴 1 — ATTACH THE LACIE. It is not connected to this Mac.
Not asleep, not renamed: no external device is present at the USB or Thunderbolt layer, and
`drive_wait` spent its full 18-second budget confirming it. If you believe it is plugged in,
the cable, the port or the enclosure has failed — **check that before assuming data loss,
and do not reformat or "repair" anything.**

### 🔴 2 — M0's LOCK FILE NEVER REACHED THE REPO.
`requirements-lock-2026-08-14-win.txt` is not in the tree and not in any commit on any
branch. It is still on the Windows machine, uncommitted. **Recover it from that machine
before it is wiped.** If the PC is already gone, the pinned environment M1 and M3 depend on
must be rebuilt from scratch.

### 🔴 3 — THIS MAC HAS NO USABLE PYTHON.
Only Apple's system Python 3.9.6, which **cannot import this codebase** — the repo requires
3.10+. M1 step 6 is not "make a venv"; it is "install a modern Python toolchain, *then*
make a venv, *then* pin it against the lock file from item 2." Three blockers in sequence.

### 🟠 4 — SOMEONE ALREADY BULK-COPIED `~/Naiad` ONTO THIS MAC, UNVERIFIED.
The tracked 598 files happen to be correct — git proves it after the fact. **The untracked
files have no such proof, and three of them are missing entirely.** Please tell M3 what
performed that copy and from which source; if that tool skipped or truncated files silently,
its other output cannot be trusted either.

### 🔴 5 — THIS REPORT IS NOT ON THE REMOTE. Push it.
`publish()` committed cleanly at **`35c293f`** but the push died on
`could not read Username for 'https://github.com': Device not configured` — **this Mac has
no GitHub credentials.** Configure a credential helper, a PAT, or switch the remote to SSH,
then `git push origin v12-v1-census`. Until you do, the branch sits 1 commit ahead of
origin and **everything in this report exists only on this machine** — the same
single-copy exposure described in item 4, now applied to the report about it.

### 🟢 6 — THREE PIECES OF GOOD NEWS.
`drive_wait` handles POSIX paths correctly and is **not** an M3 portability item. All 15
sidecar'd archives in `naiad-backups/` hash clean — the carried backup set is internally
intact, merely stale (newest estate 2026-08-11) and resting on a weaker witness than this
drill accepts. And `publish()`'s scope guard, size budget and commit path all work on
macOS — only the push is blocked, and only on credentials.

---

**M2 is NOT complete. It has not started.** Re-run this drill from Gate 0 once items 1–3
are resolved. Nothing in it was partially applied, so the re-run begins from a clean board.

*— HEPHAESTUS, 2026-08-14 · 0 files adopted · 0 sources touched · 0 mismatches · 4 halts*
