# BUILDERS REPORT — HEPHAESTUS — 2026-08-04
## Six sidecars written, verified and mirrored; queue 002 D4 reduced to a fixture; ATHENA lane closed

**Lane:** HEPHAESTUS (local Windows Claude Code)
**Repo:** naiad · **Branch:** `v12-v1-census` · **HEAD at start:** `f93af2b`
**Python:** 3.12.10 (`C:/venvs/naiad/Scripts/python.exe`)
**Operator rulings carried:** G1-a … G6-a; **D4 reduced to fixture F-R1** on the strength of this
lane's own §4a finding.
**Write authority used:** `G:` for `.sha256` sidecars **only** — no `.zip` was created, modified,
moved or deleted. One authorised commit of six local sidecars outside `exchange/`. No script edited.

---

## 0 · What this session was for, in plain language

Three jobs, all closing work opened earlier.

1. **Give six archives a fingerprint.** Six of the nine phase archives on Drive had no `.sha256`
   sidecar. They could be verified only by comparing against the laptop's copy — so if the laptop
   were lost, the very copies meant to survive it could not be checked at all. Each now has a
   fingerprint written locally, committed to GitHub, and mirrored to Drive beside the archive.
2. **Amend queue item 002.** Its D4 asked for retention code that this lane found already built.
   The operator ruled it reduced to a confirmation fixture.
3. **Close the ATHENA lane** with a status entry recording what is verified and what is pending.

**Jargon, defined once.** *Sidecar* = a small `.sha256` text file beside an archive holding its
64-character fingerprint. *Mirror* = copy to a second location and prove the copy correct by reading
it back from that location. *Tracked* = under git's control, so it reaches GitHub. *No-clobber* =
refuse to overwrite an existing file rather than replace it.

---

## 1 · Gates and probes, as printed

```
pwd=/c/Users/luisf/OneDrive/Desktop/Midas-Claude Code Resources/naiad  branch=v12-v1-census  head=f93af2b
  NOTE: this paste WRITES to G: (sidecars only).
```

Pre-flight check added before writing anything — a new `.sha256` under `research_outputs/_archive/`
must be trackable, or the whole plan fails silently at the commit step:

```
--- would a new .sha256 there be gitignored? (dry test) ---
  not ignored - trackable
```

`.gitignore:38` is `*.zip`. It does not cover `.sha256`, which is the entire reason this approach
works: **the archive stays out of git; its fingerprint goes in.**

---

## 2 · The sidecar format, read rather than invented

```
--- step 2: the existing sidecar format, read not invented ---
  model    : research_outputs/_archive/tc5_2026-08-02.zip.sha256  (86 bytes)
  verbatim : '68942d6261bf8ca8d551e52aa6e4d374f8c9fb6e0ac5be5da96b188e928b4357  tc5_2026-08-02.zip\r\n'
  inferred : "<hash>__<filename>CRLF"
```

Format: **`<64-char lowercase hash>` + two spaces + `<archive filename>` + CRLF.** Matches the
`sha256sum` convention, and matches what `backup_estate.py:1063` produces on Windows.

### 2a · One correction to the inference, made before writing

The paste inferred the trailing terminator as:

```python
trailing = '\n' if txt.endswith('\n') else ''
```

The model ends with **`\r\n`**, not `\n`. `str.endswith('\n')` is true for a CRLF string, so this
detects *that* a newline exists but not *which one* — and would have written six LF-terminated
sidecars while claiming to match a CRLF model. I made the test CR-aware:

```python
trailing = '\r\n' if txt.endswith('\r\n') else ('\n' if txt.endswith('\n') else '')
```

**Why it was worth fixing rather than ignoring.** Functionally nothing depends on it — every parser
in this project splits on whitespace. But the step is titled *"the existing sidecar format, read not
invented"*, and writing a terminator different from the model contradicts that. It also matters for
stability: `core.autocrlf=true` on this machine, so git normalises CRLF→LF in the index and restores
CRLF on checkout. LF-in-worktree is therefore the *unstable* state — a fresh clone would render these
files CRLF regardless. Writing CRLF now means the worktree already matches what any clone produces.

---

## 3 · The six sidecars — write and verify, verbatim

```
--- steps 3+4: write locally, then verify by re-reading ---
  s1_2026-07-27.zip            WRITTEN + VERIFIED
      4d14ea48066dcf8b3548030551778323683ef76612702ea8205eb10bdd18f825   (106239157 B archive)
  s2_2026-07-27.zip            WRITTEN + VERIFIED
      df5c1c196fef822537788e290e64f0c8dc9ef896694b73c91dab38fb0d5ce5ce   (246355294 B archive)
  s3_2026-07-27.zip            WRITTEN + VERIFIED
      80ac04439e169cf1dfff5bc122b37fb78ddc6a6a79d2201380973006ff4e146f   (269919602 B archive)
  tc1_2026-07-27.zip           WRITTEN + VERIFIED
      e673a158b5b1388d8e521769b460937153c691368766afda70af6d6d8f4caff8   (242926299 B archive)
  tc4_2026-07-27.zip           WRITTEN + VERIFIED
      794036c2d613528530272864aa866421af0cbf9de2db5a2423fa7e0b25eb1933   (68700167 B archive)
  v3_anchor_2026-07-27.zip     WRITTEN + VERIFIED
      69d9cc989cb4054e7aa88cd5dfd7828863aad494f33423602010ced7f6cd757a   (91049070 B archive)
```

"VERIFIED" here is a three-way identity: the hash written to the file, the hash read back off disk,
and a *fresh re-hash of the archive* all agree (`back == h == sha(lz)`). A sidecar that failed to
read back as written would have halted before any mirroring.

**Independent corroboration:** every one of these six hashes is **identical to the value measured in
the previous session's verification pass**, which computed them from scratch. Two independent
measurements, hours apart, agreeing exactly.

---

## 4 · The mirror to Drive — verbatim

```
--- step 5: mirror to Drive, verify by reading back OFF Drive ---
  s1_2026-07-27.zip            MIRRORED + VERIFIED against the Drive archive
  s2_2026-07-27.zip            MIRRORED + VERIFIED against the Drive archive
  s3_2026-07-27.zip            MIRRORED + VERIFIED against the Drive archive
  tc1_2026-07-27.zip           MIRRORED + VERIFIED against the Drive archive
  tc4_2026-07-27.zip           MIRRORED + VERIFIED against the Drive archive
  v3_anchor_2026-07-27.zip     MIRRORED + VERIFIED against the Drive archive

  sidecars written and mirrored: 6
```

**The verification is the strong form, and the distinction matters.** Each mirrored sidecar was
checked two ways: the sidecar text read back *off Drive* equals the expected hash, **and** a fresh
full re-hash of the archive *on Drive* equals that same hash (`(drive_txt == h) and (dh == h)`). So
this does not merely prove the sidecar copied correctly — it proves **the sidecar on Drive correctly
describes the archive sitting next to it on Drive.** That re-hashed roughly 1,025 MB off the
streaming mount.

A weaker check — copying the file and confirming the bytes arrived — would have proved nothing about
whether the fingerprint matches its subject.

---

## 5 · The sidecar commit

```
  staged: research_outputs/_archive/s1_2026-07-27.zip.sha256 research_outputs/_archive/s2_2026-07-27.zip.sha256
          research_outputs/_archive/s3_2026-07-27.zip.sha256 research_outputs/_archive/tc1_2026-07-27.zip.sha256
          research_outputs/_archive/tc4_2026-07-27.zip.sha256 research_outputs/_archive/v3_anchor_2026-07-27.zip.sha256
[v12-v1-census ccbfd2d] chore: add sha256 sidecars for the six 2026-07-27 phase archives - fingerprints are tracked (gitignore covers *.zip only) so archives stay verifiable if the machine is lost
 6 files changed, 6 insertions(+)
 create mode 100644 research_outputs/_archive/s1_2026-07-27.zip.sha256
 create mode 100644 research_outputs/_archive/s2_2026-07-27.zip.sha256
 create mode 100644 research_outputs/_archive/s3_2026-07-27.zip.sha256
 create mode 100644 research_outputs/_archive/tc1_2026-07-27.zip.sha256
 create mode 100644 research_outputs/_archive/tc4_2026-07-27.zip.sha256
 create mode 100644 research_outputs/_archive/v3_anchor_2026-07-27.zip.sha256
To https://github.com/catpatrol/Naiad.git
   f93af2b..ccbfd2d  v12-v1-census -> v12-v1-census
  SIDECAR PUSH SUCCEEDED
```

**SIDECAR COMMIT SHA: `ccbfd2d`.** Exactly six paths, all under `research_outputs/_archive/`, none
under `exchange/`, `scripts/` or `engine/` — the staging guard was checked before committing.

---

## 6 · Finding: the claim of "all 9" is false — it is 7 of 9

The script's closing message reads *"Every phase archive now has a fingerprint in TWO independent
places."* **That is true for seven of the nine, not all nine.**

```
  analytics_v1.0.0_2026-07-29.zip          local=NO      drive=yes
  analytics_tests_v1.0.0_2026-07-29.zip    local=NO      drive=yes
```

`git ls-files research_outputs/_archive/` returns **seven** sidecars, not nine.

**How this arose.** The two `analytics` archives were taken off-machine in an earlier session, and
their sidecars were generated **at the Drive destination only** — that session's scope forbade
writing into `research_outputs/`. They have never had a local sidecar, so nothing about them reaches
GitHub. This session's six-file mandate did not include them.

| archive group | local sidecar → GitHub | Drive sidecar | verifiable without the laptop? |
|---|---|---|---|
| `s1`, `s2`, `s3`, `tc1`, `tc4`, `v3_anchor` | **yes** (`ccbfd2d`) | **yes** | **yes — two places** |
| `tc5` | **yes** (pre-existing) | **yes** | **yes — two places** |
| `analytics_v1.0.0`, `analytics_tests_v1.0.0` | **no** | yes | **Drive only** |

**Practical exposure is small but real.** Both files are tiny (19,641 B and 6,816 B) and both are
verifiable *on Drive* against their Drive sidecars. What is missing is the second, independent
fingerprint on GitHub. If Drive were lost or a Drive copy silently corrupted, there would be no
external record to detect it — which is precisely the argument that justified this whole session for
the other six.

**Why I did not simply fix it.** The contract authorised *"the six new `.sha256` files in one
commit"*, and its ROLLBACK line names six. Writing two more and pushing them would have exceeded an
unusually specific authorisation, on my own initiative, after the authorised commit had already been
made. **Reported for a one-line ruling instead.** The remedy is the same code path, two more files.

### 6a · The ATHENA closing status was corrected before publishing

The status block as drafted asserted, tagged `[verified]`:

> `- All 9 now have sidecars: local ones are git-TRACKED (.gitignore:38 covers *.zip only) [verified]`

and, in NOW, *"every one now carries a fingerprint in two independent places."* Both are false in the
way §6 describes. Publishing a false `[verified]` fact into a lane's closing ledger — the document
future sessions treat as settled ground truth — is exactly the failure mode this project has spent
the day removing. Three corrections were made:

- NOW now reads *"7 of the 9 now carry a fingerprint in two independent places."*
- The FACTS line now states all 9 have a Drive sidecar, 7 of 9 also have a tracked local one pushed
  as `ccbfd2d`, and the two analytics archives' fingerprints are **not** on GitHub.
- A fifth PENDING item was added naming the two missing sidecars and the one-paste remedy.

---

## 7 · Queue 002 D4 reduced to a fixture

```
  OK  D4 reduced to fixture F-R1; original text struck through, not deleted
```

As it now reads:

> **D4 REDUCED TO A FIXTURE — operator ruling 2026-08-04.** The executor of this contract read the
> retention code before it was filed and found it **ALREADY IMPLEMENTED**; nothing has aged out yet,
> which is why the observed MANIFEST duplication is not a retention failure. **Do not rebuild it.**
> Deliver only fixture F-R1 below as confirmation that the existing behaviour reports and never
> deletes. The original D4 text is retained beneath for provenance and is NOT a work item.
>
> ~~**D4 · Manifest retention.**~~ Keep the newest 7 `exchange/status/daily/` artifacts; older ones
> are REPORTED, never auto-deleted …

The original text is **struck through, not removed**, so the contract's history stays legible: a
future reader can see what was asked, what was found, and why it changed. The
`PRE-EXECUTION FINDING` block beneath it — recorded before any code was written — carries the
evidence: `routine_jobs.json:8` already sets `"keep_daily": 7`, and
`daily_routine.py:632 apply_rolling_window()` already keeps the newest N of both artifact kinds and
moves the rest rather than deleting them.

**D1, D2 and D3 stand unchanged.** Queue 002 remains a real contract; it is one deliverable lighter.

---

## 8 · Fixture-equivalent transcript

| # | assertion | result |
|---|---|---|
| G1 | working directory is the local clone | **PASS** |
| G2 | branch is `v12-v1-census` | **PASS** |
| G3 | `phases/` reachable | **PASS** |
| G4 | a new `.sha256` is not gitignored | **PASS** — checked before writing |
| G5 | sidecar format read from the existing model, not invented | **PASS** — CRLF terminator, two-space separator |
| G6 | terminator inference is CR-aware | **PASS** — *corrected; the paste's test was CR-blind* |
| G7 | each sidecar reads back equal to a fresh archive re-hash | **PASS** — 6/6 |
| G8 | no-clobber honoured locally and on Drive | **PASS** — no existing file overwritten |
| G9 | each Drive sidecar verified against the Drive archive | **PASS** — 6/6, ~1,025 MB re-hashed |
| G10 | hashes agree with the previous session's independent measurement | **PASS** — 6/6 identical |
| G11 | only `.sha256` written to `G:` | **PASS** — no `.zip` created, modified, moved or deleted |
| G12 | commit contains exactly the six sidecars | **PASS** — staging guard checked; `ccbfd2d` |
| G13 | no script edited | **PASS** |
| G14 | closing-status claims match measured reality | **CORRECTED** — see §6a |
| G15 | no literal backslash in any path used | **PASS** |

---

## 9 · Rollback

- **Local sidecars:** `rm research_outputs/_archive/{s1,s2,s3,tc1,tc4,v3_anchor}_2026-07-27.zip.sha256`
- **Drive sidecars:** delete the same six `.sha256` names under `G:/My Drive/naiad-backups/phases`.
  The nine `.zip` archives are untouched and must be left alone.
- **Sidecar commit:** already pushed, so `git revert ccbfd2d` (the `git reset HEAD~1` in the contract
  applied only while unpushed).
- **`exchange/` changes:** `git checkout -- exchange/` pre-publish, or `git revert <publish sha>`.

---

## 10 · FILE DISPOSITION TABLE

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY |
|---|---|---|---|---|---|
| `research_outputs/_archive/s1_2026-07-27.zip.sha256` | yes | tracked | **`ccbfd2d`** | yes (`origin/v12-v1-census`) | GitHub + Drive mirror |
| `research_outputs/_archive/s2_2026-07-27.zip.sha256` | yes | tracked | **`ccbfd2d`** | yes (`origin/v12-v1-census`) | GitHub + Drive mirror |
| `research_outputs/_archive/s3_2026-07-27.zip.sha256` | yes | tracked | **`ccbfd2d`** | yes (`origin/v12-v1-census`) | GitHub + Drive mirror |
| `research_outputs/_archive/tc1_2026-07-27.zip.sha256` | yes | tracked | **`ccbfd2d`** | yes (`origin/v12-v1-census`) | GitHub + Drive mirror |
| `research_outputs/_archive/tc4_2026-07-27.zip.sha256` | yes | tracked | **`ccbfd2d`** | yes (`origin/v12-v1-census`) | GitHub + Drive mirror |
| `research_outputs/_archive/v3_anchor_2026-07-27.zip.sha256` | yes | tracked | **`ccbfd2d`** | yes (`origin/v12-v1-census`) | GitHub + Drive mirror |
| `G:/My Drive/naiad-backups/phases/*.sha256` (6 new) | yes | n/a — **outside the repo** | n/a | n/a | Google Drive |
| `G:/My Drive/naiad-backups/phases/*.zip` (9 archives) | yes | n/a — **outside the repo** | n/a | n/a | **Google Drive — all 9 hash-verified, all 9 now sidecarred** |
| `research_outputs/_archive/*.zip` (9 archives) | yes | **ignored** — `.gitignore:38:*.zip` | never | no | Drive `phases/`; fingerprints on GitHub for 7 of 9 |
| `research_outputs/_archive/analytics_v1.0.0_2026-07-29.zip.sha256` | **no — not created** | — | — | — | **NOT PROTECTED** — no GitHub fingerprint (§6) |
| `research_outputs/_archive/analytics_tests_v1.0.0_2026-07-29.zip.sha256` | **no — not created** | — | — | — | **NOT PROTECTED** — no GitHub fingerprint (§6) |
| `exchange/queue/002_backup-and-publish-guards.md` | yes | tracked | see publish sha in on-screen close | yes (`origin/v12-v1-census`) | GitHub + `--workflow` archive |
| `exchange/status/LEDGER_ATHENA.md` | yes | tracked | see publish sha | yes (`origin/v12-v1-census`) | GitHub + `--workflow` archive |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_SIDECARS-AND-LANE-CLOSE.md` | yes | tracked on publish | see publish sha | yes (`origin/v12-v1-census`) | GitHub + `--workflow` archive |
| `scripts/backup_estate.py`, `scripts/daily_routine.py`, `scripts/routine_jobs.json` | yes | tracked | unchanged this run | unchanged | GitHub + `--workflow` archive |

**Read this table as:** *committed is not pushed, pushed is not backed up.* The nine `.zip` archives
are git-ignored by design and live off-machine only on Drive. Their fingerprints are what makes that
copy auditable — and after `ccbfd2d`, seven of those nine fingerprints are on GitHub, independent of
both the laptop and Drive. The two rows marked **NOT PROTECTED** are the remaining gap.

**Per §3.1, this document does not state its own sha256** — that value is stale the moment it is
written.

---

## 11 · What remains open, with owners

| # | open item | owner |
|---|---|---|
| 1 | **Two missing local sidecars** for the analytics archives — one paste closes it (§6) | operator to authorise |
| 2 | Execute queue 002 (D1, D2, D3 + fixture F-R1) — its own session, its own build document | HEPHAESTUS |
| 3 | ARGUS (8 files) and APOLLO (1) to rule on the orphan memo | ARGUS, APOLLO |
| 4 | ~18.7 MB of redundant copies in `naiad-backups/` — apply §3.2 before removing anything | operator |
| 5 | Trigger-2 line in the naiad-custodian skill, then the ROLLBACK-canary probe | operator |
| 6 | Confirm Drive upload completed — **click Sync now** | operator |
