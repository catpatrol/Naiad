# BUILDERS REPORT — HEPHAESTUS — 2026-08-04
## Enforcing the §4.2 content guard on `exchange/reports/` — one file removed, two removals refused, seven orphans reported

**Lane:** HEPHAESTUS (local Windows Claude Code)
**Repo:** naiad · **Branch:** `v12-v1-census` · **HEAD at start:** `a97cee6`
**Python:** 3.12.10 (`C:/venvs/naiad/Scripts/python.exe`)
**Basis:** `CONVENTIONS.md` §4.2 — verified verbatim, quoted in §1 below.
**Scope honoured:** `exchange/reports/` only. `exchange/status/`, `research_outputs/`, `briefs/`,
`_reviewer_box/` and `backup_estate.py` were **read but never written**.

---

## 0 · What this session was for, in plain language

`exchange/` is the folder that syncs to the project box — the shared surface every lane reads. It
has a ratified size rule: **text only, 1 MB per file.** Anything bigger is supposed to be referenced
by a pointer, not copied in. That rule had never been enforced, and a measurement yesterday found
`exchange/` sitting at 51.4% of the box with a **single 1.88 MB file consuming 29.4% of it alone**.

This session enforced the rule on `exchange/reports/`. The method: for each data file, look for a
byte-identical copy elsewhere in the repo. If one exists **and is genuinely protected**, remove the
`exchange/` copy and leave behind a small text pointer recording where it lives and its fingerprint.
If no copy exists, leave the file alone and report it — deciding where an orphan should live is the
owning lane's call, not this contract's.

**The headline result: one file removed, 29.4% of the box reclaimed, and two removals refused
because the "duplicate" they would have relied on turns out to be a file git is instructed never to
commit.** Details in §3.

**Jargon, defined once.** *The box* = the project-box storage `exchange/` syncs into, ~6.39 MB
capacity. *Data file* = `.json`, `.jsonl`, `.csv`, `.parquet`, `.html`, `.png`, `.zip` — machine
artifacts, as opposed to prose documents. *sha256* = a 64-character fingerprint; identical hashes
mean byte-identical files. *Tracked* = under git's control, so it travels to GitHub. *Ignored* =
git has been explicitly told to pretend the file does not exist; it lives only on this laptop.
*Orphan* = a file with no copy anywhere else. *Pointer* = a small markdown stub replacing a removed
artifact, recording its path and hash.

---

## 1 · The basis, verified before acting

The paste cited `CONVENTIONS.md §4.2`. I read it rather than take it on trust. It exists at line 360
and says, verbatim:

> **Content guard:** text only, 1 MB per file. Larger artifacts are referenced by path + sha256
> pointer, never copied in.

The authority is real and says what the paste claimed. Proceeded.

---

## 2 · Gates and probes, as printed

```
pwd=/c/Users/luisf/OneDrive/Desktop/Midas-Claude Code Resources/naiad  branch=v12-v1-census  head=a97cee6
```

Both preconditions passed. **Ten data files** were found tracked under `exchange/reports/`, totalling
**2,287,137 B**; `exchange/reports/` as a whole held **3,092,747 B = 48.4% of the box**.

```
=== TARGETS (data files in exchange/reports/) ===
     1879133   29.4%  exchange/reports/CAPTURE_2026-08-03_post_ny.json
      144574    2.3%  exchange/reports/RENDER_2026-08-03_post_ny.html
      113355    1.8%  exchange/reports/WF1_discriminants.json
       54427    0.9%  exchange/reports/PARITY_C3_2026-08-03.json
       40559    0.6%  exchange/reports/PARITY_SETUP_A_2026-08-03.json
       25351    0.4%  exchange/reports/BRIEF2_CALIBRATION_2026-08-03.json
       11549    0.2%  exchange/reports/ANALYTICS1_REPORT_2026-08-02.json
       10870    0.2%  exchange/reports/f_an_8_diff_2026-08-02.json
        6713    0.1%  exchange/reports/PARITY_ANCHORED_2026-08-03.json
          606    0.0%  exchange/reports/STORAGE_MEASUREMENT_2026-08-03.json
  total tracked bytes in exchange/reports/: 3092747

  size-matched candidates hashed: 6
```

**Note on the §4.2 threshold.** Only one of these ten exceeds the 1 MB per-file limit — `CAPTURE` at
1.88 MB. The other nine are individually legal under §4.2. They were still examined, because §4.2's
second clause ("referenced by path + sha256 pointer, never copied in") applies to *copies* regardless
of size, and because the operator's contract asked for duplicates to be removed.

---

## 3 · Per-file verdict table, verbatim from the dry run

I ran the detection **read-only first**, before any `git rm`. That decision is what caught the
problem in §3b.

```
=== DRY RUN - VERDICTS (nothing removed) ===

  exchange/reports/CAPTURE_2026-08-03_post_ny.json  (1879133 B, 29.4%)
    sha256: c60eac9a330ef9d51f2b41621a9f99caf4fe62f6f3cdbd9490cbfb15b0619bc2
    VERDICT: DUPLICATE - 1 twin(s)
      twin: briefs/brief_2026-08-03_post_ny.json                          [TRACKED]

  exchange/reports/RENDER_2026-08-03_post_ny.html  (144574 B, 2.3%)
    sha256: 5acf1f5e1a05bf645cdb6d6be9bd4a78f4889c6e3d41c049578a687402c7eead
    VERDICT: DUPLICATE - 1 twin(s)
      twin: research_outputs/brief/brief2_2026-08-03_post_ny.html         [IGNORED by .gitignore:83]

  exchange/reports/WF1_discriminants.json  (113355 B, 1.8%)
    sha256: 06d2bcfd6498185db0f641614e3b7e8d21922758d369abe4b32846051e9e36b4
    VERDICT: ORPHAN - no copy outside exchange/

  exchange/reports/PARITY_C3_2026-08-03.json  (54427 B, 0.9%)
    sha256: f3c9cd3c5bf3fd2ed1a65c7f8d9e46ae60b14e89bf8111166ddc3835026dde59
    VERDICT: ORPHAN - no copy outside exchange/

  exchange/reports/PARITY_SETUP_A_2026-08-03.json  (40559 B, 0.6%)
    sha256: fdcb7b88cba1db2cbcc44d2b65243db6c8e5d4112dbe053cb60f9e84dcaebfe0
    VERDICT: ORPHAN - no copy outside exchange/

  exchange/reports/BRIEF2_CALIBRATION_2026-08-03.json  (25351 B, 0.4%)
    sha256: 3f99dc3c9272af5c49b2537ecaaa6fe3944978d09bd7ec827420f041bfa5994d
    VERDICT: ORPHAN - no copy outside exchange/

  exchange/reports/ANALYTICS1_REPORT_2026-08-02.json  (11549 B, 0.2%)
    sha256: 258ec96f62c378c9378ad53826bc1a6ef7794732d6ae717f09b053afb0f6b3a2
    VERDICT: DUPLICATE - 1 twin(s)
      twin: _reviewer_box/ANALYTICS1_REPORT.json                          [IGNORED by .gitignore:80]

  exchange/reports/f_an_8_diff_2026-08-02.json  (10870 B, 0.2%)
    sha256: 4bdc51fa2e9378b1a67dfcf27e58c215410ca60356cd4edfba809eec2892f655
    VERDICT: ORPHAN - no copy outside exchange/

  exchange/reports/PARITY_ANCHORED_2026-08-03.json  (6713 B, 0.1%)
    sha256: 2986c6022eabbe700064b5f5e5fd35bf031c237b35f982aedf14fdac420af2c5
    VERDICT: ORPHAN - no copy outside exchange/

  exchange/reports/STORAGE_MEASUREMENT_2026-08-03.json  (606 B, 0.0%)
    sha256: adafaba25295d292124258f58f2c4999ae8636829f0f5ee20b7a2fa95c847568
    VERDICT: ORPHAN - no copy outside exchange/

  duplicates: 3   orphans: 7
```

### 3a · The one file removed

`exchange/reports/CAPTURE_2026-08-03_post_ny.json`, 1,879,133 B, **29.4% of the box**.

Its twin `briefs/brief_2026-08-03_post_ny.json` was checked three ways before removal — the paste
checked none of these:

| check | result |
|---|---|
| present in `HEAD`? | **yes** |
| present on `origin/v12-v1-census`? | **yes** |
| working copy identical to the committed blob? | **yes — both `d7c24f67`** |

So the content is committed, pushed, and on GitHub independent of this laptop. Removal is safe, and
the pointer's claim that a copy "lives at" that path is true in the sense that matters.

```
  pointer written: exchange/reports/CAPTURE_2026-08-03_post_ny.json.pointer.md
  REMOVED from exchange/: exchange/reports/CAPTURE_2026-08-03_post_ny.json
  freed: 1879133 bytes (29.4% of the box)
  sha256 recorded: c60eac9a330ef9d51f2b41621a9f99caf4fe62f6f3cdbd9490cbfb15b0619bc2
```

### 3b · Two removals refused — the paste would have made things worse

**This is the finding of the session.** The paste's rule was: if a byte-identical file exists
anywhere outside `exchange/`, remove the `exchange/` copy and point at the twin. It never asked
whether the twin was **under version control**. Two of the three twins are not:

| removed-by-the-paste | twin it would have pointed at | twin's real state |
|---|---|---|
| `RENDER_2026-08-03_post_ny.html` (144,574 B, 2.3%) | `research_outputs/brief/brief2_2026-08-03_post_ny.html` | **IGNORED** — `.gitignore:83` |
| `ANALYTICS1_REPORT_2026-08-02.json` (11,549 B, 0.2%) | `_reviewer_box/ANALYTICS1_REPORT.json` | **IGNORED** — `.gitignore:80` |

The `.gitignore` lines are not incidental. They are emphatic:

```
# Reviewer hand-off staging — local-only, never committed.
_reviewer_box/

# Daily Brief archive — ops artifacts, untracked by design (A1.5); ignored so `git clean -fd` cannot remove them
research_outputs/brief/
```

**"local-only, never committed"** and **"untracked by design"**. These paths are deliberately outside
git. Had the paste run as written, it would have removed the *only version-controlled copy* of both
files and written a pointer stating — in the stub's own words — *"A byte-identical copy exists in the
repo"*. A future reader would take that as reassurance. It would be false in the way that matters:
the named copy is not in the repo's history, is not on GitHub, and dies with this laptop.

That is precisely the failure the last two sessions were spent closing ("committed is not pushed,
pushed is not backed up"). I refused both removals and left the files in place.

**A second reason for refusing the `ANALYTICS1_REPORT` removal:** its twin lives in `_reviewer_box/`,
which this contract's own SCOPE line forbids touching. Making that directory the canonical home for
an `exchange/` artifact would quietly place project evidence in a directory declared local-only
staging.

**What I did not do:** I did not give these two files a tracked home. Doing so would mean writing to
`research_outputs/` or `_reviewer_box/`, both explicitly out of scope. They are reported below for a
ruling.

### 3c · Summary by category

| category | files | bytes | % of box | action taken |
|---|---|---|---|---|
| **REMOVED** — duplicate of a tracked, pushed copy | 1 | 1,879,133 | **29.4%** | removed; pointer written |
| **DUPLICATE BUT UNPROTECTED** — twin is git-ignored | 2 | 156,123 | 2.4% | **left in place**, reported |
| **ORPHAN** — no copy anywhere outside `exchange/` | 7 | 251,881 | 3.9% | **left in place**, reported |
| total data files examined | 10 | 2,287,137 | 35.8% | — |

---

## 4 · Before and after

| measure | before | after | change |
|---|---|---|---|
| `exchange/reports/` bytes | **3,092,747** | **1,214,674** | **−1,879,133** |
| `exchange/reports/` as % of the ~6.39 MB box | **48.4%** | **19.0%** | **−29.4 points** |
| data files tracked under `exchange/reports/` | 10 | 9 | −1 |
| largest single file under `exchange/reports/` | 1,879,133 B | 144,574 B | −92.3% |

**The after figure includes the 1,060 B pointer stub and excludes this report** (~24 KB, about 0.4%
of the box), which is added by the same publish. Read the after number as a floor.

**Proportion of the available win captured: 92.4%.** Of the 2,034,577 B that the paste would have
removed across all three "duplicates", the single safe removal accounts for 1,879,133 B. Refusing the
two unsafe removals cost 156,123 B — **2.4% of the box** — to avoid making two files machine-only.
That is a good trade and it is the operator's to reverse if he disagrees.

---

## 5 · The orphans — seven files, with the lane that owns each

Ownership below is **evidence-based**, not inferred from filenames: each orphan was traced to the
report or queue item that produced it.

| # | file | bytes | % box | traced to | **recommended owner** |
|---|---|---|---|---|---|
| 1 | `WF1_discriminants.json` | 113,355 | 1.8% | `queue/2026-08-03_WF1_winner_forensics_APOLLO.md`, `BUILDERS_REPORT_APOLLO_2026-08-03_WF1.md` | **APOLLO** |
| 2 | `PARITY_C3_2026-08-03.json` | 54,427 | 0.9% | `BUILDERS_REPORT_ARGUS_2026-08-03_C3.md`, `DIGEST.md` | **ARGUS** |
| 3 | `PARITY_SETUP_A_2026-08-03.json` | 40,559 | 0.6% | `BUILDERS_REPORT_ARGUS_2026-08-03_PARITY_A.md`, `SESSION_SUMMARY_ARGUS_2026-08-03_PARITY_A.md` | **ARGUS** |
| 4 | `BRIEF2_CALIBRATION_2026-08-03.json` | 25,351 | 0.4% | `BUILDERS_REPORT_ARGUS_2026-08-03_BRIEF2_C2.md`, `..._C4.md`, `DIGEST.md` | **ARGUS** |
| 5 | `f_an_8_diff_2026-08-02.json` | 10,870 | 0.2% | `BUILDERS_REPORT_ARGUS_2026-08-02_ANALYTICS1_PHASE_I.md`, `CONTRACT_V4_2026-07-28.md` | **ARGUS** |
| 6 | `PARITY_ANCHORED_2026-08-03.json` | 6,713 | 0.1% | `BUILDERS_REPORT_ARGUS_2026-08-03_PARITY_ANCHORED.md` | **ARGUS** |
| 7 | `STORAGE_MEASUREMENT_2026-08-03.json` | 606 | 0.0% | `BUILDERS_REPORT_ARGUS_2026-08-03_C3.md`, `SESSION_SUMMARY_ARGUS_2026-08-03_C3.md` | **ARGUS** |
| | **total** | **251,881** | **3.9%** | | **6 ARGUS, 1 APOLLO** |

**Recommendation.** All seven are legal under §4.2 individually (each well under 1 MB) and together
cost only 3.9% of the box, so **there is no urgency**. The real question is not size but *home*: an
orphan in `exchange/` means `exchange/` is acting as primary storage for a machine artifact rather
than as a bus. If the operator wants that closed, the cheapest route is for **ARGUS** — which owns
six of the seven — to state in one ruling where its parity/calibration JSON belongs, and for those
files to move there with pointers left behind. **This contract should not make that choice for
another lane**, which is why nothing was moved.

---

## 6 · Would `publish_exchange.publish()` have rejected the 1.88 MB file?

**No. It has no size guard of any kind.** This was checked directly in `scripts/publish_exchange.py`
(186 lines). Its only guard is a **path-scope** check:

```python
offenders = [p for p in staged if p and not p.startswith(SCOPE)]
return (not offenders), offenders
```

The `offenders` list that every publish reports — and which has read `offenders= []` on every run
this week — means **"no staged path fell outside `exchange/`"**. It says nothing whatsoever about
file size. A 100 MB file inside `exchange/` publishes cleanly and reports `offenders= []`.

**So the answer to the operator's question is unambiguous: the 1.88 MB `CAPTURE` file was committed
and pushed without objection, and would be again tomorrow.** §4.2 has been a documented rule with
**no mechanical enforcement** behind it. The only thing that caught this file was a human running a
measurement.

**Is the follow-up contract worth writing? Yes — and it is small.** The guard function already
receives the staged path list and already has a rejection path wired to `status="FLAGGED"`, index
reset and skipped push. Adding a size check means extending one list comprehension and one message.
Concretely:

- reject any staged file over 1 MB, reusing the existing `FLAGGED` machinery;
- report offending paths **with their sizes**, so the message says what to do;
- consider a lower warn-only threshold (say 256 KB) for data files, since ten legal-but-accumulating
  files are what produced a 48.4% folder — no single one of them ever broke the rule.

**That last point is the real lesson.** Only one of ten files ever violated §4.2's per-file limit.
The folder reached half the box through nine files that were each individually compliant. **A
per-file guard alone would not have prevented this.** A total-size check on `exchange/` would.

---

## 7 · Fixture-equivalent transcript

| # | assertion | result |
|---|---|---|
| G1 | working directory is the local clone | **PASS** |
| G2 | branch is `v12-v1-census` | **PASS** |
| G3 | `CONVENTIONS.md §4.2` exists and says what the paste claimed | **PASS** — quoted verbatim in §1 |
| G4 | detection run read-only before any removal | **PASS** — dry run in §3 |
| G5 | every candidate twin checked for tracked/ignored state | **PASS** — *added; the paste omitted this* |
| G6 | removal twin present in `HEAD` | **PASS** |
| G7 | removal twin present on `origin/v12-v1-census` | **PASS** |
| G8 | removal twin blob-identical to worktree copy | **PASS** — both `d7c24f67` |
| G9 | unsafe removals refused | **2 REFUSED** — git-ignored twins (§3b) |
| G10 | pointer written before removal | **PASS** |
| G11 | nothing outside `exchange/` modified | **PASS** — porcelain shows only pre-existing untracked entries |
| G12 | `research_outputs/`, `briefs/`, `_reviewer_box/`, `exchange/status/` unwritten | **PASS** — read only |
| G13 | `backup_estate.py` untouched | **PASS** — not opened |
| G14 | no literal backslash in any path used | **PASS** |

---

## 8 · Findings reported, not fixed

1. **Two `exchange/` data files have no protected counterpart** (§3b). `RENDER_2026-08-03_post_ny.html`
   and `ANALYTICS1_REPORT_2026-08-02.json` are duplicated only into git-ignored directories. They are
   safe **today** precisely because the `exchange/` copy — the one the paste would have deleted — is
   the tracked one. **Owner: operator / ARGUS.**
2. **`publish_exchange.publish()` has no size guard** (§6). **Owner: operator to commission.**
3. **A per-file guard would not have prevented this situation** (§6). Nine of ten files were
   individually compliant. A total-size check on `exchange/` is the guard that actually bites.
4. **Seven orphans need a home ruling** (§5), six of them ARGUS's. **Owner: ARGUS, then APOLLO.**
5. **`exchange/status/MANIFEST.json` and `exchange/status/daily/MANIFEST_2026-08-03.json` are both
   21,115 B** — probable duplication, carried over from yesterday's report. Out of scope here
   (`exchange/status/` is excluded by this contract). **Owner: operator.**

---

## 9 · Rollback

- **Pre-publish:** `git checkout -- exchange/` restores the removed file and drops the staged
  deletion; delete `exchange/reports/CAPTURE_2026-08-03_post_ny.json.pointer.md`.
- **Post-publish:** `git revert <publish sha>`.
- **Nothing outside `exchange/` needs rolling back** — nothing outside it was written.
- The removed file's content is additionally recoverable from git history at any time, and lives at
  `briefs/brief_2026-08-03_post_ny.json` on `origin/v12-v1-census`.

---

## 10 · FILE DISPOSITION TABLE

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY |
|---|---|---|---|---|---|
| `exchange/reports/CAPTURE_2026-08-03_post_ny.json` | **no — removed** | deletion staged | see publish sha in on-screen close | yes (`origin/v12-v1-census`) | **git history + `briefs/brief_2026-08-03_post_ny.json` (tracked, pushed)** |
| `exchange/reports/CAPTURE_2026-08-03_post_ny.json.pointer.md` | yes | tracked on publish | see publish sha in on-screen close | yes (`origin/v12-v1-census`) | GitHub + `--workflow` archive |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_EXCHANGE-GUARD-ENFORCEMENT.md` | yes | tracked on publish | see publish sha in on-screen close | yes (`origin/v12-v1-census`) | GitHub + `--workflow` archive |
| `briefs/brief_2026-08-03_post_ny.json` | yes | tracked | unchanged this run | yes (`origin/v12-v1-census`) | GitHub + `--workflow` archive |
| `exchange/reports/RENDER_2026-08-03_post_ny.html` | yes | tracked — **left in place** | unchanged | yes | **GitHub only** — its twin is git-ignored |
| `exchange/reports/ANALYTICS1_REPORT_2026-08-02.json` | yes | tracked — **left in place** | unchanged | yes | **GitHub only** — its twin is git-ignored |
| `exchange/reports/WF1_discriminants.json` | yes | tracked — **left in place** | unchanged | yes | GitHub only (orphan) |
| `exchange/reports/PARITY_C3_2026-08-03.json` | yes | tracked — **left in place** | unchanged | yes | GitHub only (orphan) |
| `exchange/reports/PARITY_SETUP_A_2026-08-03.json` | yes | tracked — **left in place** | unchanged | yes | GitHub only (orphan) |
| `exchange/reports/BRIEF2_CALIBRATION_2026-08-03.json` | yes | tracked — **left in place** | unchanged | yes | GitHub only (orphan) |
| `exchange/reports/f_an_8_diff_2026-08-02.json` | yes | tracked — **left in place** | unchanged | yes | GitHub only (orphan) |
| `exchange/reports/PARITY_ANCHORED_2026-08-03.json` | yes | tracked — **left in place** | unchanged | yes | GitHub only (orphan) |
| `exchange/reports/STORAGE_MEASUREMENT_2026-08-03.json` | yes | tracked — **left in place** | unchanged | yes | GitHub only (orphan) |
| `research_outputs/brief/brief2_2026-08-03_post_ny.html` | yes | **ignored** — `.gitignore:83` | never | no | **NOT PROTECTED** — machine-only by design |
| `_reviewer_box/ANALYTICS1_REPORT.json` | yes | **ignored** — `.gitignore:80` | never | no | **NOT PROTECTED** — machine-only by design |
| `scripts/publish_exchange.py` | yes | tracked | unchanged this run | unchanged | GitHub + `--workflow` archive |

**Read this table as:** *committed is not pushed, pushed is not backed up.* The last two rows are the
ones that matter for §3b — they are the files the paste would have relied on, and neither is
protected by anything at all.

**Per §3.1, this document does not state its own sha256** — that value is stale the moment it is
written.

---

## 11 · What remains open, with owners

| # | open item | owner |
|---|---|---|
| 1 | Rule on `RENDER_…html` and `ANALYTICS1_REPORT…json` — give them a tracked home, or accept `exchange/` as their home | operator / ARGUS |
| 2 | Commission the publish size guard — **recommend a total-`exchange/` check, not only per-file** (§6) | operator |
| 3 | Home ruling for 7 orphans, 6 of them ARGUS's (§5) | ARGUS, then APOLLO |
| 4 | `MANIFEST.json` / `MANIFEST_2026-08-03.json` both 21,115 B — probable duplication in `exchange/status/`, out of scope here | operator |
| 5 | Wire `backup_estate.py --phase` for off-machine output — separate contract, untouched | operator / HEPHAESTUS |
| 6 | Confirm Drive upload completed — **click Sync now** | operator |
