# BUILDERS REPORT — HEPHAESTUS — 2026-08-04
## The last two machine-only archives taken off-machine; SETUP line 139 superseded; `exchange/` measured by file

**Lane:** HEPHAESTUS (local Windows Claude Code)
**Repo:** naiad · **Branch:** `v12-v1-census` · **HEAD at start:** `58561d3`
**Python:** 3.12.10 (`C:/venvs/naiad/Scripts/python.exe`)
**Standing constraints honoured:** `research_outputs/` read-only; `backup_estate.py` not edited
(the `--mirror` wiring is a separate contract); forward slashes throughout.

---

## 0 · What this session was for, in plain language

Three jobs. Two of them finish work opened earlier today; one is a measurement taken so a later
decision can be made on evidence.

1. **Get the last two machine-only archives off the laptop.** The previous session
   (`…_TC5-OFFSITE-AND-PHASE-MODE-READ.md`) reported two archives that existed in exactly one place
   on earth — this laptop. They are small (19,641 B and 6,816 B) but they are the *only* copies of
   the analytics evidence. Both are now on Google Drive, proved identical rather than assumed so.
2. **Finish correcting the stale Drive document.** Earlier today line 124 of `SETUP_2026-07-28.md`
   was corrected. Its downstream conclusion at line 139 — which declared the offsite backup target
   *blocked* — was left standing and flagged as open. It is now superseded too.
3. **Measure `exchange/` file by file.** The `exchange/` folder is what syncs to the project box.
   Nobody had a per-file picture of what is consuming that space. This is read-only: nothing was
   moved, compressed or deleted.

**Jargon, defined once.** *Archive* = a `.zip` holding one phase's evidence. *Sidecar* = a small
`.sha256` text file beside an archive holding its 64-character fingerprint. *Hash / sha256* = that
fingerprint; identical hashes mean byte-identical files, and a single flipped bit changes the hash
completely. *Off-machine* = a copy that survives this laptop dying. *The box* = the project-box
storage `exchange/` syncs into, measured at roughly 6.39 MB capacity. *Porcelain* = `git status` in
its script-readable form. *CR pair* = the two-byte `\r\n` Windows line ending; counting them before
and after an edit proves the edit did not silently reflow the whole file.

---

## 1 · Gates and probes, as printed

```
pwd=/c/Users/luisf/OneDrive/Desktop/Midas-Claude Code Resources/naiad  branch=v12-v1-census  head=58561d3
  phases/ present
```

All four preconditions passed: correct clone, correct branch, `G:/My Drive/naiad-backups/phases`
present (created by this morning's tc5 run), and both source archives present.

Destination pre-state, checked before any write:

```
  tc5_2026-08-02.zip                                   18375498
  tc5_2026-08-02.zip.sha256                                  86
```

Neither analytics archive was present, so the no-clobber guard was clear for both.

---

## 2 · The two archives taken off-machine — hash blocks verbatim

```
--- analytics_v1.0.0_2026-07-29.zip
  source            : research_outputs/_archive/analytics_v1.0.0_2026-07-29.zip  (19641 bytes)
  sidecar recorded  : none
  fresh local hash  : d3fcd786881dc20224fc51e168f60ace00d57749586b9cd60c28b54f4c9ba3d9
  destination       : G:/My Drive/naiad-backups/phases\analytics_v1.0.0_2026-07-29.zip
  re-read FROM DRIVE: d3fcd786881dc20224fc51e168f60ace00d57749586b9cd60c28b54f4c9ba3d9  (19641 bytes)
  HASH MATCH (3-way): YES

--- analytics_tests_v1.0.0_2026-07-29.zip
  source            : research_outputs/_archive/analytics_tests_v1.0.0_2026-07-29.zip  (6816 bytes)
  sidecar recorded  : none
  fresh local hash  : 0a1ffc941032acbf7144f4c7af77ad1d54967a40a4e5eb36fa200ae078e99999
  destination       : G:/My Drive/naiad-backups/phases\analytics_tests_v1.0.0_2026-07-29.zip
  re-read FROM DRIVE: 0a1ffc941032acbf7144f4c7af77ad1d54967a40a4e5eb36fa200ae078e99999  (6816 bytes)
  HASH MATCH (3-way): YES

  archives copied and verified: 2
```

| archive | bytes | sha256 (local == Drive read-back) |
|---|---|---|
| `analytics_v1.0.0_2026-07-29.zip` | 19,641 | `d3fcd786881dc20224fc51e168f60ace00d57749586b9cd60c28b54f4c9ba3d9` |
| `analytics_tests_v1.0.0_2026-07-29.zip` | 6,816 | `0a1ffc941032acbf7144f4c7af77ad1d54967a40a4e5eb36fa200ae078e99999` |

### 2a · Correction to the label: this was a 2-way check, not 3-way

**The script printed `HASH MATCH (3-way)`. That label is wrong for these two files, and it matters.**

The three legs are meant to be (1) the hash recorded in a sidecar when the archive was made, (2) a
fresh hash of the local file, (3) a fresh hash read back off Drive. Leg 1 did not exist —
`sidecar recorded : none` for both. The code's test is:

```python
ok = (dh == lh and dn == ln and (not rec or rec == dh))
```

With `rec = None`, the clause `(not rec or rec == dh)` is **vacuously true**. It contributed nothing.
So what was actually proven is a **2-way** match: fresh local vs Drive read-back.

**What that does and does not establish.** It fully proves the copy landed on Drive intact. It does
**not** prove the local file was itself uncorrupted beforehand — there was no historical fingerprint
to compare against, so if the local archive had rotted since 2026-07-29, this run would have
faithfully copied the rot and reported success. That risk is unavoidable for a file that never had a
sidecar; it is recorded here rather than hidden behind a "3-way" label.

By contrast, this morning's `tc5` copy genuinely was 3-way — it had a sidecar written 2026-08-02.

### 2b · The missing sidecars — gap found and closed at the destination

The paste's ROLLBACK line reads *"delete the 4 new files under `G:/My Drive/naiad-backups/phases`"*,
which anticipates 2 archives **plus 2 sidecars**. But the copy step is conditional:

```python
if os.path.exists(s + '.sha256'): shutil.copy2(s + '.sha256', d + '.sha256')
```

Neither source has a sidecar, so **the branch never fired and only 2 files would have landed.**

That left a real gap: the Drive copies would carry **no fingerprint of their own**. If this laptop
were lost tomorrow — the exact scenario the copy exists to survive — there would be nothing on Drive
to verify those archives against. The backup would be unverifiable precisely when it was needed.

I closed it by generating the sidecars **at the destination**, hashing the file *as read from Drive*:

```
  WROTE analytics_v1.0.0_2026-07-29.zip.sha256
        d3fcd786881dc20224fc51e168f60ace00d57749586b9cd60c28b54f4c9ba3d9
  WROTE analytics_tests_v1.0.0_2026-07-29.zip.sha256
        0a1ffc941032acbf7144f4c7af77ad1d54967a40a4e5eb36fa200ae078e99999
```

Then re-verified all three archives in `phases/` against their sidecars:

```
--- read back and re-verify each Drive archive against its new sidecar ---
  analytics_v1.0.0_2026-07-29.zip          sidecar=d3fcd786881dc202...  computed=d3fcd786881dc202...  MATCH
  analytics_tests_v1.0.0_2026-07-29.zip    sidecar=0a1ffc941032acbf...  computed=0a1ffc941032acbf...  MATCH
  tc5_2026-08-02.zip                       sidecar=68942d6261bf8ca8...  computed=68942d6261bf8ca8...  MATCH
```

**Why this respects the read-only rule.** `research_outputs/` was not touched — no sidecar was
written there, nothing was moved, deleted or rewritten. The new files live only under
`G:/My Drive/naiad-backups/phases/`, which is a destination, not a source. Format matches `tc5`'s
exactly (`<hash>  <filename>`, LF-terminated), so the folder is internally consistent.

**Authority:** the paste's own ROLLBACK line, which specifies four files. The result now matches it.

### 2c · `phases/` final state

```
    analytics_tests_v1.0.0_2026-07-29.zip                    6816
    analytics_tests_v1.0.0_2026-07-29.zip.sha256              104
    analytics_v1.0.0_2026-07-29.zip                         19641
    analytics_v1.0.0_2026-07-29.zip.sha256                     98
    tc5_2026-08-02.zip                                   18375498
    tc5_2026-08-02.zip.sha256                                  86
```

Three phase archives, each with a sidecar beside it. **Every one is self-verifying without the
laptop.**

**Streaming-mount caveat, unchanged from this morning:** `G:` is a Google Drive streaming mount, so
a read-back immediately after a write may be served from the local Drive cache. This proves the
bytes went through the Drive client correctly; it does not prove the upload to Google's servers has
completed. **That is what Sync now confirms, and it remains the operator's one action.**

---

## 3 · SETUP line 139 superseded — with CR-pair proof

```
  exchange/reports/SETUP_2026-07-28.md : CR pairs=0  (a CRLF file must keep its CRLFs)
  OK  corrected line 139
      was: **This contradicts a FACT line in the Part D status text** — *"a local Google Drive sync folder exists so offs
  CR pairs after: 0  (must equal 0)
```

| measurement | value |
|---|---|
| CR pairs **before** the edit | **0** |
| CR pairs **after** the edit | **0** |
| verdict | **equal — no line-ending reflow** |

The file is LF-only, so `eol` resolved to `'\n'` and the split/join round-tripped exactly. This
matters because the previous session flagged that an editor writing with `newline=''` will silently
convert a CRLF file to LF across its whole length, turning a one-line edit into a whole-file diff.
**This paste's editor was written to be line-ending safe** — it reads bytes, counts `\r\n`, splits on
the detected terminator and writes bytes back. That is the correct pattern and it is now demonstrated
on a live edit.

**Encoding verified separately.** The console echo of the superseded text rendered em-dashes as `�`,
which is cp1252 terminal rendering of the *print statement*, not file damage. Checked directly
against the stored bytes:

```
  U+FFFD count: 0
  em-dashes   : 66
  file decodes as UTF-8: OK
```

Zero replacement characters. The document is intact.

### 3a · The line as it now stands

`exchange/reports/SETUP_2026-07-28.md` line 139:

> **SUPERSEDED 2026-08-04.** G: is mounted; `G:/My Drive/naiad-backups` holds 988 MB and a `phases/`
> folder now carries phase archives. The blocker recorded here is RESOLVED. Remaining real gap:
> `backup_estate.py --phase` writes only inside the repo (line 1030, `dest` hardcoded) and silently
> ignores `--dest` — wiring is a separate contract. Superseded text: "**This contradicts a FACT line
> in the Part D status text** — *"a local Google Drive sync folder exists so offsite archiving can be
> automated [verified]."* I appended your block verbatim as instructed and did not alter it, but the
> claim does not hold on this machine. Consequently **PENDING item 3 (`backup_estate.py`) is blocked
> on more than Amendment 1** — there is no Drive path for Part B to supply. Either Drive for Desktop
> needs installing, or the offsite target needs to be something else."

The full original paragraph is preserved verbatim inside the annotation. **Open item 4 from this
morning's report is now closed.**

**Observation, reported not fixed:** the evidence table at lines 133–137 of the same document still
reads `Google Drive path | **none found**` and `real local folder or streaming mount | **neither —
not present**`. Those rows are now false. They were outside the fragment this paste targeted and I
did not widen scope to reach them. A reader who skims the table without reading lines 124 and 139
would still be misled. **Owner: operator** — this would be a third correction to the same document,
and at some point annotating a superseded report is worth less than marking the whole document
historical.

---

## 4 · `exchange/` measured by file — full table

Read-only. Nothing was moved, compressed or deleted.

```
  exchange/ : 88 tracked files, 3284184 bytes (3.13 MB)
    documents  :   74 files     909173 bytes  =  14.2% of a 6.09 MB box
    DATA files :   14 files    2375011 bytes  =  37.2% of the box

  === 25 LARGEST FILES UNDER exchange/ ===
  DATA    1879133   29.4%  exchange/reports/CAPTURE_2026-08-03_post_ny.json
  DATA     144574    2.3%  exchange/reports/RENDER_2026-08-03_post_ny.html
  DATA     113355    1.8%  exchange/reports/WF1_discriminants.json
  DATA      54427    0.9%  exchange/reports/PARITY_C3_2026-08-03.json
  doc       46324    0.7%  exchange/reports/2026-08-02_HEPHAESTUS_report_exchange-v1-build.md
  DATA      40559    0.6%  exchange/reports/PARITY_SETUP_A_2026-08-03.json
  doc       37522    0.6%  exchange/status/CONVENTIONS.md
  doc       35526    0.6%  exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_TC5-OFFSITE-AND-PHASE-MODE-READ.md
  doc       34971    0.5%  exchange/reports/BUILDERS_REPORT_APOLLO_2026-08-03_WF1.md
  doc       34283    0.5%  exchange/reports/INTERFACE_2026-08-03.md
  doc       33748    0.5%  exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_SEQ8.md
  doc       33556    0.5%  exchange/reports/2026-08-02_HEPHAESTUS_report_disposition-inventory.md
  doc       29660    0.5%  exchange/reports/WF1_tables.md
  doc       26774    0.4%  exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-03_CONVENTIONS.md
  DATA      26000    0.4%  exchange/status/daily/MANIFEST_2026-07-28.json
  DATA      25351    0.4%  exchange/reports/BRIEF2_CALIBRATION_2026-08-03.json
  doc       22795    0.4%  exchange/reports/SESSION_SUMMARY_ARGUS_2026-08-03_BRIEF2.md
  doc       22478    0.4%  exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-03_T4-SNAPSHOT.md
  doc       22201    0.3%  exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-03_WRAPUP.md
  doc       21659    0.3%  exchange/reports/BUILDERS_REPORT_ARGUS_2026-08-03_BRIEF2.md
  DATA      21115    0.3%  exchange/status/daily/MANIFEST_2026-08-03.json
  DATA      21115    0.3%  exchange/status/MANIFEST.json
  doc       19934    0.3%  exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_CONVENTIONS-MERGE-AND-ARCHIVE-AUDIT.md
  DATA      19644    0.3%  exchange/status/daily/MANIFEST_2026-08-02.json
  doc       19504    0.3%  exchange/reports/BUILDERS_REPORT_ARGUS_2026-08-02_ANALYTICS1_PHASE_I.md

  Percentages are against a measured box capacity of ~6.39 MB
  (calibrated two ways: LEDGER.md 255,011 B = 4%; s3_excursion_substrate.jsonl 6,007,227 B = 94%).
```

### 4a · Headline numbers

| measure | files | bytes | % of the ~6.39 MB box |
|---|---|---|---|
| **documents** (`.md` and other prose) | 74 | 909,173 | **14.2%** |
| **DATA** (`.json`, `.jsonl`, `.csv`, `.parquet`, `.html`, `.zip`, `.png`) | 14 | 2,375,011 | **37.2%** |
| **total tracked under `exchange/`** | **88** | **3,284,184** | **51.4%** |

### 4b · What the table actually shows

**One file is the story.** `CAPTURE_2026-08-03_post_ny.json` is **1,879,133 B — 29.4% of the entire
box on its own.** That single file is **more than double the combined weight of all 74 prose
documents** (14.2%). It is also **79% of all DATA bytes** in `exchange/`.

**Documents are not the problem.** 74 documents — every builders report, every convention, every
session summary written across the project — total 909,173 B, under one seventh of the box. The
largest single document is 46,324 B, 0.7%. Writing more reports is cheap.

**The top 4 DATA files carry most of the weight.** `CAPTURE` (29.4%), `RENDER…html` (2.3%),
`WF1_discriminants.json` (1.8%) and `PARITY_C3` (0.9%) together are 34.4% of the box — roughly
two-thirds of everything currently stored.

**Manifests are quietly accumulating.** Four `MANIFEST*.json` files appear in the top 25
(26,000 + 21,115 + 21,115 + 19,644 = 87,874 B). `exchange/status/MANIFEST.json` and
`exchange/status/daily/MANIFEST_2026-08-03.json` are **byte-identical in size at 21,115** — very
likely the same content stored twice, one being the current pointer to the other. That is a small
duplication now and a growing one if a daily manifest is added each day.

**Headroom:** the box is **51.4% consumed, leaving ~3.11 MB**. At the current document rate this is
not urgent; a second `CAPTURE`-class artifact would consume roughly another 29% and change that.

### 4c · A unit inconsistency in the script's own output — reported, not fixed

The script prints `= 14.2% of a 6.09 MB box` in one place and `~6.39 MB` in another. **Both describe
the same capacity.** `CAP` is `6390000.0` bytes; the header divides by `1048576.0`, which converts to
**MiB** (6.09) while labelling the result "MB", whereas the footer states the decimal figure
(6.39 MB). The percentages are computed directly against the byte value and are **correct and
unaffected**. Only the printed unit label is inconsistent. Flagging it because a reader comparing the
two lines would reasonably think one of them is a typo. **Owner: whoever next edits the sizing
script — this report is not that contract.**

### 4d · Scope note on the measurement

`git ls-files exchange` lists **tracked** files only, so anything untracked under `exchange/` is
excluded. The snapshot was taken **before** this report and before the publish, so it does not
include this document. This report is roughly 20 KB, about **0.3%** of the box — the totals above
should be read as a floor, not a ceiling.

---

## 5 · Fixture-equivalent transcript

No `Fixtures()` harness ran; these are the assertions this paste made and their results.

| # | assertion | result |
|---|---|---|
| G1 | working directory is the local clone | **PASS** |
| G2 | branch is `v12-v1-census` | **PASS** |
| G3 | `G:/My Drive/naiad-backups/phases` exists | **PASS** |
| G4 | both source archives present | **PASS** (19,641 B and 6,816 B) |
| G5 | local archive matches its own sidecar before copy | **N/A — neither has a sidecar** (see §2a) |
| G6 | destinations do not already exist (no-clobber) | **PASS** — neither present |
| G7 | Drive read-back matches local hash and byte count | **PASS** on both |
| G8 | 3-way agreement | **DOWNGRADED to 2-way** — leg 1 absent, clause vacuous (§2a) |
| G9 | destination sidecars written and re-verified | **PASS** — all 3 archives in `phases/` MATCH |
| G10 | `research_outputs/` unmodified | **PASS** — porcelain shows only the pre-existing `seq8` entries |
| G11 | `backup_estate.py` unmodified | **PASS** — not opened for write |
| G12 | line-139 fragment appears exactly once | **PASS** |
| G13 | CR pairs preserved across the edit | **PASS** — 0 before, 0 after |
| G14 | corrected file still decodes as UTF-8, no U+FFFD | **PASS** — 0 replacement chars, 66 em-dashes |
| G15 | `exchange/` measurement is read-only | **PASS** — `git ls-files` + `getsize` only |
| G16 | no literal backslash in any path used | **PASS** |

---

## 6 · Backup position after this session

**Every phase archive in the project now exists off-machine.** That was not true this morning.

| archive | laptop | Drive `phases/` | legacy one-off snapshot |
|---|---|---|---|
| `tc5_2026-08-02.zip` | yes | **yes + sidecar** | no |
| `analytics_v1.0.0_2026-07-29.zip` | yes | **yes + sidecar** | no |
| `analytics_tests_v1.0.0_2026-07-29.zip` | yes | **yes + sidecar** | no |
| `s1/s2/s3/tc1/tc4/v3_anchor` (2026-07-27) | yes | no | yes (verified intact this morning) |

**The structural gap is unchanged and is the next contract.** `backup_estate.py --phase` still writes
only inside the repo (line 1030) and still silently ignores `--dest`. Every archive listed above
reached Drive because a human ran a paste. **The next phase archive created will be machine-only by
default,** exactly as these three were, until the `--mirror` wiring lands.

---

## 7 · Publishing

`git status --porcelain -- exchange/` before publish:

```
   M exchange/reports/SETUP_2026-07-28.md
```

Both artifacts are inside `exchange/`, so `publish_exchange.publish()` carries them. Publish result
is recorded in the session's on-screen close.

---

## 8 · Rollback

- **Drive:** delete the **4** new files under `G:/My Drive/naiad-backups/phases` —
  `analytics_v1.0.0_2026-07-29.zip`, `analytics_v1.0.0_2026-07-29.zip.sha256`,
  `analytics_tests_v1.0.0_2026-07-29.zip`, `analytics_tests_v1.0.0_2026-07-29.zip.sha256`.
  `tc5_2026-08-02.zip` and its sidecar are from the earlier session and must be left in place.
  Local originals are untouched either way.
- **Corrected document:** `git checkout -- exchange/reports/SETUP_2026-07-28.md` while unpushed;
  after publish, `git revert <publish sha>`.
- **`research_outputs/`, `backup_estate.py`:** nothing to roll back — read-only this session.

---

## 9 · FILE DISPOSITION TABLE

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY |
|---|---|---|---|---|---|
| `exchange/reports/SETUP_2026-07-28.md` | yes | tracked | see publish sha in on-screen close | yes (`origin/v12-v1-census`) | GitHub + `--workflow` archive |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_ANALYTICS-ARCHIVES-AND-EXCHANGE-SIZING.md` | yes | tracked on publish | see publish sha in on-screen close | yes (`origin/v12-v1-census`) | GitHub + `--workflow` archive |
| `G:/My Drive/naiad-backups/phases/analytics_v1.0.0_2026-07-29.zip` | yes | n/a — **outside the repo** | n/a | n/a | **Google Drive (the off-machine copy)** |
| `G:/My Drive/naiad-backups/phases/analytics_v1.0.0_2026-07-29.zip.sha256` | yes | n/a — **outside the repo** | n/a | n/a | Google Drive |
| `G:/My Drive/naiad-backups/phases/analytics_tests_v1.0.0_2026-07-29.zip` | yes | n/a — **outside the repo** | n/a | n/a | **Google Drive (the off-machine copy)** |
| `G:/My Drive/naiad-backups/phases/analytics_tests_v1.0.0_2026-07-29.zip.sha256` | yes | n/a — **outside the repo** | n/a | n/a | Google Drive |
| `research_outputs/_archive/analytics_v1.0.0_2026-07-29.zip` | yes | **ignored** — `.gitignore:38:*.zip` | never | no | Drive `phases/` **as of today**; not GitHub |
| `research_outputs/_archive/analytics_tests_v1.0.0_2026-07-29.zip` | yes | **ignored** — `.gitignore:38:*.zip` | never | no | Drive `phases/` **as of today**; not GitHub |
| `scripts/backup_estate.py` | yes | tracked | unchanged this run | unchanged | GitHub + `--workflow` archive |

**Read this table as:** *committed is not pushed, pushed is not backed up.* The four `G:` rows are the
only ones surviving loss of both this laptop and GitHub. The two local `.zip` rows are git-ignored by
design — and unlike `tc5`, these two have **no tracked sidecar in the repo**, so GitHub protects
neither their contents nor their fingerprints. Their fingerprints now exist only on Drive, which is
why §2b's sidecars mattered.

**Per §3.1, this document does not state its own sha256** — that value is stale the moment it is
written.

---

## 10 · What remains open, with owners

| # | open item | owner |
|---|---|---|
| 1 | Wire `--phase` for off-machine output (recommend `--mirror DIR` + make `--phase --dest` an error) — **separate contract, not touched here** | operator to rule, HEPHAESTUS to build |
| 2 | `SETUP_2026-07-28.md` lines 133–137 evidence table still reads "none found" | operator |
| 3 | Five of six legacy archives verified on size only, not hashed (~75 s to close) | operator — carried from this morning |
| 4 | Sizing script labels 6,390,000 B as both "6.09 MB" and "6.39 MB" (MiB vs MB); percentages unaffected | next editor of that script |
| 5 | `MANIFEST.json` and `MANIFEST_2026-08-03.json` both 21,115 B — probable duplication, growing daily | operator |
| 6 | Confirm Drive upload completed — **click Sync now** | operator |

**Closed this session:** open item 2 from this morning (two analytics archives machine-only) and open
item 4 (SETUP line 139).
