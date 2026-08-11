# BUILDERS REPORT — HEPHAESTUS — 2026-08-11 — BULK RELOCATION: seq8_run2 + _unarchived/s3

**Lane:** HEPHAESTUS · **Date:** 2026-08-11 · **Branch:** `v12-v1-census` · **Head at start:** `aeb0777`
**Environment:** LOCAL Windows Claude Code, repo `naiad`
**Ruling executed:** operator, 2026-08-11 — relocate `seq8_run2` to D: with pair-hash report; resolve
`_unarchived/s3_2026-07-27` against its canonical archive; harden CONVENTIONS §3.1; list untracked files.

---

## 0 · Outcome in one paragraph

`research_outputs/seq8_run2/` was proven a byte-for-byte duplicate of the primary `seq8/` by sha256 on
all eight of its largest files, then relocated to D: — 11 files, each copied, hash-verified on D:, and
only then removed locally. `research_outputs/_unarchived/s3_2026-07-27/` was compared against the
canonical archive and came back **NOT EXACT**: the archive is a strict *superset* of the folder
(1551 zip members vs 753 on disk). The delete gate therefore refused, and all 753 files were **MOVED**
to D: instead — nothing was deleted. The local tree fell **5451.9 MB → 2292.3 MB**, reclaiming
**3159.6 MB (3.09 GB)**. Primary `seq8/` was re-measured after the run at 1783.5 MB, unchanged.
The §3.1 no-exceptions clause is in place. **Nothing outside the two authorized paths was removed.**

---

## 1 · Gates and preconditions — all passed before any mutation

| gate | result |
|---|---|
| pwd inside `*OneDrive*naiad*` | ok — `/c/Users/luisf/OneDrive/Desktop/Midas-Claude Code Resources/naiad` |
| branch == `v12-v1-census` | ok |
| `D:/Naiad` reachable | REACHABLE — 3724.7 GB free of 3725.7 GB |
| `D:/Naiad` writable | write probe PASSED |
| `exchange/status/CONVENTIONS.md` present, contains `### 3.1` | YES; clause not yet present |
| `scripts/publish_exchange.py` present | YES — `publish(repo, date_str, remote='origin', log=print)` |
| `D:/Naiad/research_outputs/_archive/s3_2026-07-27.zip` | PRESENT, 257.4 MB |
| `research_outputs/_archive/s3_2026-07-27.zip.sha256` sidecar | PRESENT |
| `_1`-suffix twin sweep (per standing memory) | no `_1` twins on either side; no pre-existing `seq8_run2` on D: (no-clobber safe) |

---

## 2 · Defects found in the reviewer paste, and what was changed before running

Reported-not-fixed is not available here — three of these are safety defects on a delete path, so they
were corrected before execution. **All delete gates were left exactly as authorized.**

**2.1 — `rmtree(U, ignore_errors=True)` could delete unverified files.** In the `_unarchived` MOVE
branch the paste removes each file only after its D: copy hash-matches, then calls
`shutil.rmtree(U, ignore_errors=True)`. Any file present in the tree but absent from the earlier
`os.walk` snapshot would be force-deleted with no D: copy and no hash — contradicting "Anything else:
MOVE, never delete." **Replaced** with a bottom-up `os.rmdir` sweep, which raises `OSError` on any
non-empty directory and so cannot destroy a file. This branch is the one that actually executed.

**2.2 — the CONVENTIONS edit would have rewritten every line ending.** The paste reads the file in
text mode (universal newlines, CRLF→LF on read) and writes back with `newline=''`. On a CRLF file that
converts the whole document and produces a whole-file diff — the identical hazard already on record for
`.gitignore`. **Replaced** with a binary read, dominant-ending detection, and an inserted block built
from the detected ending. Measured: `CRLF=0 LF=821` → inserted with LF → post-write `CRLF=0 LF=827`.
Diff is **6 insertions, 0 deletions**.

**2.3 — unguarded opens plus `sys.exit(1)` would skip the untracked listing.** `open(SC)` and
`ZipFile(Z)` had no existence guard, and a sha mismatch calls `sys.exit(1)`, aborting the whole Python
block before §4. **Guarded** so a HALT in §3 still yields the untracked list and the AFTER accounting.

**2.4 — publish ordering made the mandated document impossible.** Step 5 publishes before the build
document exists, so the document this very paste mandates could never be in that commit. **Reordered**:
§1–4 ran, then this document was written, then a single `publish()` covering both. One commit, not two.

**2.5 — anchor defect found during verification (post-run).** `s.find('### 3.1')` matched the
**table-of-contents** entry at line 79, not the §3.1 body at line 331 — the file carries a full heading
outline before the body. The clause first landed between the 3.2 and 3.3 TOC entries. **Corrected**:
removed from the TOC, inserted into the real §3.1 body after its opening paragraph. Final diff below.

---

## 3 · CONVENTIONS §3.1 — the no-exceptions clause

Final diff, `exchange/status/CONVENTIONS.md`, **6 insertions / 0 deletions**, 47484 → 47941 bytes:

```diff
@@ -329,6 +329,12 @@ block**, to `exchange/reports/BUILDERS_REPORT_<LANE>_<date>_<phase>.md`. Standal
 with **zero prior context**. It is required at the end of any block of work, **and at interim
 stage boundaries when the block is very large**.

+**No exceptions — rule hardened 2026-08-11 by operator instruction, after a reviewer
+waived it for a "read-only" census and the results reached the operator only as a screenshot.**
+EVERY builder session emits the single build document — read-only sessions included: a
+measurement nobody can re-read is a measurement that will be re-run. A reviewer paste may not
+waive this; an AFTER line saying "no document needed" is a drafting defect — refuse it.
+
 It serves two readers at once and must satisfy both:
```

This document is the clause's first application: the 2026-08-11 census that preceded it was run under a
paste whose AFTER line said "No build document needed — read-only." That waiver is what the clause bans.

---

## 4 · The seq8 pair-hash report — VERBATIM

`seq8_run2` held 11 files / 1783.5 MB. The eight largest were hashed with sha256 on **both** sides.
All eight are byte-identical to their `seq8` counterpart — this is a hash result, not a size inference.

```
  seq8_run2: 11 files, 1783.5 MB

  -- pair-hash report (top 8 by size, sha256 both sides) --
  seq8_outcomes.jsonl                                  TWIN of seq8 copy  (5s)
      seq8      sha256 7f096222aac6f33929d0035ab775d0751b12047a2969a375cd9ca5adf50ac6af
      seq8_run2 sha256 7f096222aac6f33929d0035ab775d0751b12047a2969a375cd9ca5adf50ac6af
  seq8_cascades.jsonl                                  TWIN of seq8 copy  (6s)
      seq8      sha256 13195287eceab160263300a15d15f16b42e5a838c06c30f7de2469f16bf3507c
      seq8_run2 sha256 13195287eceab160263300a15d15f16b42e5a838c06c30f7de2469f16bf3507c
  seq8_events.jsonl                                    TWIN of seq8 copy  (1s)
      seq8      sha256 2bdc5c56c054e27cc8aa771b92045bcc69c9eacb1c4b5775b9fb0315b78d54cc
      seq8_run2 sha256 2bdc5c56c054e27cc8aa771b92045bcc69c9eacb1c4b5775b9fb0315b78d54cc
  seq8_cascade_birth_join.jsonl                        TWIN of seq8 copy  (1s)
      seq8      sha256 63777ca872115ba00e1e2e64d6d397cb3fac03cd2d0e066313824c9998fc6f99
      seq8_run2 sha256 63777ca872115ba00e1e2e64d6d397cb3fac03cd2d0e066313824c9998fc6f99
  seq8_arrivals.json                                   TWIN of seq8 copy  (0s)
      seq8      sha256 16fef0c4771633bbd567d2a3268c7539bcae563da41eca38be7f8849aed567e8
      seq8_run2 sha256 16fef0c4771633bbd567d2a3268c7539bcae563da41eca38be7f8849aed567e8
  seq8_d4_route_matrix.json                            TWIN of seq8 copy  (0s)
      seq8      sha256 f45b6d426e19c1044060120d18e49be2a3482ad254b79d06aa3a5f26ac2fa865
      seq8_run2 sha256 f45b6d426e19c1044060120d18e49be2a3482ad254b79d06aa3a5f26ac2fa865
  seq8_event_counts.json                               TWIN of seq8 copy  (0s)
      seq8      sha256 9584aaadf0454e1ae475fd76201853ff15908ba204294c071ac379e4de259cfe
      seq8_run2 sha256 9584aaadf0454e1ae475fd76201853ff15908ba204294c071ac379e4de259cfe
  seq8_warmup.json                                     TWIN of seq8 copy  (0s)
      seq8      sha256 c9a68c6ca0654a531b6adfde35a5113a937e06c187cf37d4c8b6f56bc67be17c
      seq8_run2 sha256 c9a68c6ca0654a531b6adfde35a5113a937e06c187cf37d4c8b6f56bc67be17c
```

**Finding:** `seq8_run2` was never a second run in any meaningful sense — it is a copy. The 1783.5 MB
it occupied was pure redundancy. `seq8/` holds 15 files to `seq8_run2`'s 11, so the primary is also the
superset; nothing existed only in `run2`.

---

## 5 · The relocation — every VERIFIED line, VERBATIM

Protocol per file: sha256 the local file → `copy2` to D: → sha256 the D: copy → compare → remove local
**only on match**. Space gate cleared first: need 1783.5 MB ×1.2 = 2140.2 MB against 3814125.0 MB free.

```
  -- move: copy -> sha256 verify on D: -> remove local --
  VERIFIED ON D: + local removed  seq8_arrivals.json                                   0.6 MB  sha256=16fef0c4771633bb...  (0s)
  VERIFIED ON D: + local removed  seq8_cascade_birth_join.jsonl                      116.7 MB  sha256=63777ca872115ba0...  (3s)
  VERIFIED ON D: + local removed  seq8_cascades.jsonl                                752.9 MB  sha256=13195287eceab160...  (14s)
  VERIFIED ON D: + local removed  seq8_d4_route_matrix.json                            0.2 MB  sha256=f45b6d426e19c104...  (0s)
  VERIFIED ON D: + local removed  seq8_event_counts.json                               0.0 MB  sha256=9584aaadf0454e1a...  (0s)
  VERIFIED ON D: + local removed  seq8_events.jsonl                                  159.4 MB  sha256=2bdc5c56c054e27c...  (3s)
  VERIFIED ON D: + local removed  seq8_extract_manifest.json                           0.0 MB  sha256=697109a69c67bab3...  (0s)
  VERIFIED ON D: + local removed  seq8_outcomes.jsonl                                753.6 MB  sha256=7f096222aac6f339...  (13s)
  VERIFIED ON D: + local removed  seq8_outcomes_manifest.json                          0.0 MB  sha256=67a219befe09b48d...  (0s)
  VERIFIED ON D: + local removed  seq8_views_summary.json                              0.0 MB  sha256=7c619cb0b1763805...  (0s)
  VERIFIED ON D: + local removed  seq8_warmup.json                                     0.0 MB  sha256=c9a68c6ca0654a53...  (0s)
  seq8_run2: 11 files relocated; local dir removed=True. PRIMARY seq8 untouched.
  PRIMARY seq8 check: 1783.5 MB before -> 1783.5 MB after  UNCHANGED
```

11 of 11 verified. Destination `D:/Naiad/research_outputs/seq8_run2` re-measured after the run:
**1783.5 MB across 11 files** — matches the source exactly.

**MC-1 safety:** `research_outputs/seq8/` was measured before and after and is byte-identical in size,
1783.5 MB / 15 files. It was never opened for write.

---

## 6 · `_unarchived/s3_2026-07-27` vs the canonical archive — full verdict

**Gate 1 — archive integrity against the repo sidecar: MATCH.**

```
  sidecar sha256 : 80ac04439e169cf1dfff5bc122b37fb78ddc6a6a79d2201380973006ff4e146f
  archive sha256 : 80ac04439e169cf1dfff5bc122b37fb78ddc6a6a79d2201380973006ff4e146f  (2s)
  archive sha256 vs repo sidecar: MATCH
```

**Gate 2 — bidirectional name + size + CRC32. FAILED in the zip→disk direction.**

```
  member keying used: as-stored
  members: zip=1551 disk=753 common=753  zip-only=798 disk-only=0  crc-mismatch=0  (25s)
  VERDICT: NOT EXACT - folder will be MOVED to D:, nothing deleted
  moved 753 files to D:/Naiad/research_outputs/_unarchived_s3_2026-07-27, each hash-verified; empty dirs removed=True
```

| count | value |
|---|---|
| zip members (files, dirs excluded) | 1551 |
| disk files | 753 |
| common names | 753 |
| **zip-only** | **798** ← why the delete was refused |
| disk-only | 0 |
| size or CRC32 mismatches among the 753 common | **0** |

**What the folder actually was.** A *partial* extraction — only the `journal_s3/` subtree:

| top-level member | on disk | in archive |
|---|---|---|
| `journal_s3` | 753 files, 1376.1 MB | present |
| `journal_s3_run2` | — | 753 members, 1376.1 MB |
| `s3_events` | — | 20 members, 655.9 MB |
| `s3_events_run2` | — | 20 members, 655.9 MB |
| root files (`MANIFEST.json`, `analyze_log.txt`, `analyze_log2.txt`, +2) | — | 5 members, 0.3 MB |

**Interpretation for the operator.** Every one of the 753 local files was present in the archive at a
matching name, size and CRC32 — `disk-only=0`, `crc-mismatch=0`. In substance the data was fully
protected and a delete would not have lost anything. The gate refused because authorization (b) required
the match to hold in **both** directions, and the archive is a strict superset. That is the gate behaving
correctly: "superset" and "identical" are different claims, and only the operator can decide that the
extra 798 members are irrelevant. **Nothing was deleted; the tree was moved.**

**Consequence worth a ruling.** `D:/Naiad/research_outputs/_unarchived_s3_2026-07-27` (1376.1 MB) is now
a second copy of data already inside `D:/Naiad/research_outputs/_archive/s3_2026-07-27.zip` on the same
drive. Deleting it would reclaim 1376.1 MB on D: at no risk to protection. **Not done — outside this
paste's authorization.** See §10.

Also visible: the archive's own `journal_s3` and `journal_s3_run2` are 753 members / 1376.1 MB each — the
same twin pattern as `seq8`/`seq8_run2`. The `_run2` duplication is a repeated habit, not a one-off.

---

## 7 · Before / after, and BOX COST reclaimed

```
=== 0 - BEFORE ===
  working tree (.git excluded) :    5451.9 MB across 1580 files
  research_outputs/seq8                           1783.5 MB across 15 files
  research_outputs/seq8_run2                      1783.5 MB across 11 files
  research_outputs/_unarchived/s3_2026-07-27      1376.1 MB across 753 files

=== 5 - AFTER ===
  working tree (.git excluded) :    2292.3 MB across 816 files
  BOX COST RECLAIMED           :    3159.6 MB  (3.09 GB)
```

| | before | after | delta |
|---|---|---|---|
| working tree (.git excluded) | 5451.9 MB / 1580 files | 2292.3 MB / 816 files | **−3159.6 MB / −764 files** |
| `.git` | 136.2 MB | 136.2 MB (untouched) | 0 |
| **on-disk total** | **5.46 GB** | **2.37 GB** | **−3.09 GB** |

Deletion ledger totals: **764 entries, 3159.6 MB** — 11 under authorization (a), 753 under MOVE.
Ledger rows falling outside `research_outputs/seq8_run2/` or `research_outputs/_unarchived/s3_2026-07-27/`:
**0**, audited by grep over the full run log.

Post-state verification:

```
  PRESENT  research_outputs/seq8                                  1783.5 MB  15 files
  ABSENT   research_outputs/seq8_run2
  PRESENT  research_outputs/_unarchived                               0.0 MB  0 files
  ABSENT   research_outputs/_unarchived/s3_2026-07-27
  PRESENT  D:/Naiad/research_outputs/seq8_run2                    1783.5 MB  11 files
  PRESENT  D:/Naiad/research_outputs/_unarchived_s3_2026-07-27    1376.1 MB  753 files
```

---

## 8 · Untracked files — report only, nothing moved or filed

```
        0.2 MB  Cascade Rewire.html
        0.0 MB  Cascade_Atlas_CENSUS_1b.html
        0.0 MB  Cascade_Atlas_CENSUS_1b_v2_1.html
        0.0 MB  HANDOFF_ATHENA_2026-08-03_FULL_STATE_1.md
        0.0 MB  PRIMER_HERMES_2026-08-03_v2_FIRST_RUN.md
        0.0 MB  SS_Reassessment_Synthesis_2026-08-03.md
        0.0 MB  briefs/panel/excursions/2026-08-03.parquet
        0.1 MB  scripts/mc1_program.py
        0.0 MB  scripts/mc1_report.py
```

Nine files, ~0.5 MB total — negligible as mass, but each needs a filing decision. Note
`HANDOFF_ATHENA_2026-08-03_FULL_STATE_1.md` carries the `_1` suffix flagged in standing memory: it is a
downloaded twin, not a missing file. Three HTML atlases and one parquet sit at repo root or under
`briefs/` and per §3.2 do **not** belong in `exchange/`. `scripts/mc1_program.py` and
`scripts/mc1_report.py` are source and are the only two with a plausible claim to being committed.
**No action taken — awaiting operator ruling.**

---

## 9 · File-disposition table

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `exchange/status/CONVENTIONS.md` | yes | tracked | see §11 | see §11 | GitHub + estate zip | +457 bytes (0.007% of 6.39 MB box) |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-11_BULK-RELOCATION-SEQ8-UNARCHIVED.md` | yes | tracked (new) | see §11 | see §11 | GitHub + estate zip | 19,965 bytes (19.5 KB, 0.298% of box) |
| `research_outputs/seq8/` (PRIMARY, untouched) | yes | ignored — `.gitignore:110` | not committed | no | **local only + no D: copy** | n/a — not in sync selection |
| `research_outputs/seq8_run2/` | **REMOVED** | was ignored — `.gitignore:111` | not committed | no | D: `research_outputs/seq8_run2` (11 files, sha256-verified) **and** identical to primary `seq8/` | n/a |
| `D:/Naiad/research_outputs/seq8_run2/` | yes | n/a (off-repo) | n/a | n/a | D: drive only | n/a — unsynced drive |
| `research_outputs/_unarchived/s3_2026-07-27/` | **REMOVED (moved)** | was ignored — `.gitignore:101` | not committed | no | D: `_unarchived_s3_2026-07-27` (753 files, sha256-verified) **and** `s3_2026-07-27.zip` (sha256 matches sidecar) | n/a |
| `D:/Naiad/research_outputs/_unarchived_s3_2026-07-27/` | yes | n/a (off-repo) | n/a | n/a | D: drive only — **redundant with the zip**, see §10 | n/a — unsynced drive |
| `research_outputs/_archive/s3_2026-07-27.zip.sha256` | yes | unchanged | unchanged | unchanged | GitHub | n/a |
| 9 untracked files (§8) | yes | untracked | not committed | no | **NOT PROTECTED** | n/a — none under `exchange/` |

**Flagged by name per the 1%-of-box rule:** this report at 19.5 KB is 0.298% of the 6.39 MB box — under
the threshold, and it is prose, which §3.2 explicitly says to write more of, not fewer. No data artifact
was placed in `exchange/`.

**`research_outputs/seq8/` is the one exposure on this table.** It is git-ignored, uncommitted, and now
has no D: twin — the copy that used to shadow it was `seq8_run2`, which this run relocated. Losing the
machine loses it. MC-1 depends on it. Recommend a D: copy; not in scope here.

---

## 10 · Open items for the operator

1. **`D:/Naiad/research_outputs/_unarchived_s3_2026-07-27` is redundant.** All 753 files verified present
   in `s3_2026-07-27.zip` on the same drive at matching size+CRC32, and the zip's sha256 matches the repo
   sidecar. Deleting the loose tree reclaims 1376.1 MB on D: with no loss of protection. Needs a ruling —
   this paste authorized no deletion on D:.
2. **`research_outputs/seq8/` now has no second copy.** See §9. Recommend relocating or mirroring to D:.
   1783.5 MB, 15 files, and it is the MC-1 dependency.
3. **The `_run2` duplication is systemic.** `seq8`/`seq8_run2` and the archive's
   `journal_s3`/`journal_s3_run2` and `s3_events`/`s3_events_run2` all show the same pattern. Worth a look
   at whatever produces `_run2` directories before the next study lane fills the disk again.
4. **Nine untracked files (§8) need filing.** None are large; all are currently unprotected.

---

## 11 · Rollback

- **seq8_run2:** copy back from `D:/Naiad/research_outputs/seq8_run2/` → `research_outputs/seq8_run2/`.
  Or don't: it is byte-identical to `research_outputs/seq8/`, proven by sha256 in §4.
- **_unarchived/s3:** copy back from `D:/Naiad/research_outputs/_unarchived_s3_2026-07-27/` →
  `research_outputs/_unarchived/s3_2026-07-27/`. Nothing was deleted, so no re-extraction is needed;
  the zip re-extraction path remains available as a second route.
- **CONVENTIONS:** `git checkout -- exchange/status/CONVENTIONS.md`.

---

## 12 · Publish

Run log retained for this session at the scratchpad path
`…/tasks/btymd293o.output` (857 lines, full 764-row deletion ledger). It is a session-local file and is
**not** in the repo or the box; every figure quoted above is reproduced in this document.

Publish status, commit SHA and push result are recorded in the session close immediately following this
document's creation — `publish_exchange.publish(repo, '2026-08-11')`, staging `exchange/**` only.
