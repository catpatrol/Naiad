# BUILDERS REPORT — HEPHAESTUS — 2026-08-11 — RULINGS R1 / R2 / R3

**Lane:** HEPHAESTUS · **Date:** 2026-08-11 · **Branch:** `v12-v1-census` · **Head at start:** `2cd6f53`
**Environment:** LOCAL Windows Claude Code, repo `naiad`
**Executed:** operator rulings R1 / R2 / R3 of 2026-08-11 ("defaults"), raised as open items §10 of
`BUILDERS_REPORT_HEPHAESTUS_2026-08-11_BULK-RELOCATION-SEQ8-UNARCHIVED.md`.

---

## 0 · Outcome

All three rulings executed, none partially. **R1** — the canonical archive was re-verified against the
repo sidecar *in this run*, then the redundant loose tree on D: was removed bottom-up: 753 files, 23
directories, 1376.1 MB reclaimed on D:. **R2** — `research_outputs/seq8/` was mirrored to D: as a
copy-only operation: 15 of 15 files hash-verified on arrival, and the local tree proven untouched by an
independent re-walk comparing name + size + mtime\_ns on every file. **R3** — the anti-`_run2` rule is in
`CONVENTIONS.md`, 6 insertions, at the end of §4. The MC-1 substrate now has an off-machine copy for the
first time; that was the standing exposure this report closes.

---

## 1 · Gates

| gate | result |
|---|---|
| pwd inside `*OneDrive*naiad*` | ok |
| branch == `v12-v1-census` | ok |
| `D:/Naiad` reachable + writable | REACHABLE, write probe PASSED, 3721.5 GB free |
| R1 target present | `_unarchived_s3_2026-07-27` — 753 files, 1376.1 MB |
| R1 canonical zip present | `s3_2026-07-27.zip` — 257.4 MB |
| R1 repo sidecar present | `research_outputs/_archive/s3_2026-07-27.zip.sha256` |
| R2 source present | `research_outputs/seq8` — 15 files, 1783.5 MB |
| R2 destination absent (no-clobber) | `D:/Naiad/research_outputs/seq8` — **ABSENT**, safe to create |

---

## 2 · One defect in the paste, corrected before running

**The R3 anchor would have inserted the rule mid-sentence, in the wrong section.** The paste anchors on
the string `Every item carries the` and guards only on it occurring exactly once. It does occur exactly
once — so the guard passes — but it sits at the **end of line 561**, mid-sentence, inside this paragraph
in **§5 · Lane charters**:

> **Queue drafting rights (ruling Q-5, 2026-08-02):** APOLLO, ATHENA and ARGUS may draft builder
> work orders. DIONYSUS and HERMES may not — they critique and verify. `Every item carries the`
> operator's RATIFIED stamp before HEPHAESTUS works it.

Inserting before that anchor severs the Q-5 sentence from its own paragraph and files a **data-retention**
rule inside the section governing **who may draft queue items**. The occurrence-count guard cannot catch
this, because the count was never the problem — the *position* was.

**Corrected:** the rule was placed at the end of **§4 · Where things live, and who can see what**, which
is the section that governs where data lives and what it costs, immediately before the `---` closing §4.
Anchor used: the end-of-§4 separator, asserted unique in-run (`count != 1` → HALT-SOFT). The Q-5 paragraph
is byte-identical to before. Rule text is the operator's verbatim, hard-wrapped to ~100 columns to match
the file's dominant style; no word changed.

This is the second consecutive paste whose CONVENTIONS anchor was wrong — last session it was
`find('### 3.1')` hitting the table of contents. The lesson generalises: **an occurrence count is not a
placement check.** Anchoring on a string proves the string exists; only reading the surrounding lines
proves it is the right place.

Two further hardenings, carried forward from the previous session and applied again here:

- **R3 written binary with detected line endings.** The paste's text-mode read + `newline=''` write would
  convert a CRLF file wholesale. Measured `CRLF=0 LF=827` → written LF → post-write `CRLF=0 LF=833`.
- **R2's local-unchanged proof strengthened.** The paste re-sums the *same* file list it built before
  copying, so a deleted file raises `FileNotFoundError` rather than reporting a difference. Replaced with
  two independent `os.walk` manifests compared on name + size + mtime\_ns — see §4.

---

## 3 · R1 — remove the redundant loose tree on D:

Gate first: the canonical archive was re-hashed **in this run**, not trusted from the previous session.

```
=== R1 - REMOVE THE REDUNDANT LOOSE TREE ON D: (verify canonical first) ===
  loose tree before: 753 files, 1376.1 MB
  sidecar sha256 : 80ac04439e169cf1dfff5bc122b37fb78ddc6a6a79d2201380973006ff4e146f
  archive sha256 : 80ac04439e169cf1dfff5bc122b37fb78ddc6a6a79d2201380973006ff4e146f
  canonical zip sha256 vs repo sidecar: MATCH  (9s)
  R1: removed 753 files + 23 dirs. Tree gone: True
  Canonical remains: D:/Naiad/research_outputs/_archive/s3_2026-07-27.zip (sha-verified this run)
```

| | value |
|---|---|
| files removed | **753** |
| directories removed | **23** |
| bytes reclaimed on D: | **1376.1 MB** |
| removal method | bottom-up `os.walk(topdown=False)` + `os.remove` / `os.rmdir`, **no `ignore_errors`** |
| tree confirmed gone | yes — `os.path.exists` → False |
| protection retained | `s3_2026-07-27.zip`, sha256 verified against the repo sidecar in this run |

Every one of those 753 files was proven present in the archive at matching name, size and CRC32 during
the previous session, and the archive's sha256 was re-confirmed here before a single file was touched.

---

## 4 · R2 — mirror the MC-1 substrate, copy-only

All fifteen lines verbatim. Protocol per file: sha256 local → `copy2` → sha256 the D: copy → compare.
**No local file was opened for write and none was removed.**

```
=== R2 - MIRROR THE MC-1 SUBSTRATE: COPY seq8 -> D:, LOCAL UNTOUCHED ===
  seq8: 15 files, 1783.5 MB. D: free: 3723.0 GB
  MIRRORED + VERIFIED  seq8_outcomes.jsonl                              753.6 MB  sha256=7f096222aac6f339...  (12s)
  MIRRORED + VERIFIED  seq8_cascades.jsonl                              752.9 MB  sha256=13195287eceab160...  (12s)
  MIRRORED + VERIFIED  seq8_events.jsonl                                159.4 MB  sha256=2bdc5c56c054e27c...  (3s)
  MIRRORED + VERIFIED  seq8_cascade_birth_join.jsonl                    116.7 MB  sha256=63777ca872115ba0...  (2s)
  MIRRORED + VERIFIED  seq8_arrivals.json                                 0.6 MB  sha256=16fef0c4771633bb...  (0s)
  MIRRORED + VERIFIED  seq8_d4_route_matrix.json                          0.2 MB  sha256=f45b6d426e19c104...  (0s)
  MIRRORED + VERIFIED  seq8_event_counts.json                             0.0 MB  sha256=9584aaadf0454e1a...  (0s)
  MIRRORED + VERIFIED  seq8_warmup.json                                   0.0 MB  sha256=c9a68c6ca0654a53...  (0s)
  MIRRORED + VERIFIED  seq8_atlas_replication.json                        0.0 MB  sha256=c4ecf5dcf76c0303...  (0s)
  MIRRORED + VERIFIED  seq8_views_summary.json                            0.0 MB  sha256=6379f734dade0d25...  (0s)
  MIRRORED + VERIFIED  seq8_fixtures.json                                 0.0 MB  sha256=408cd8387cdf83a5...  (0s)
  MIRRORED + VERIFIED  seq8_fixture_transcript.txt                        0.0 MB  sha256=0a6f4f4b205a7398...  (0s)
  MIRRORED + VERIFIED  seq8_extract_manifest.json                         0.0 MB  sha256=07aa3fde63f7c049...  (0s)
  MIRRORED + VERIFIED  seq8_outcomes_manifest.json                        0.0 MB  sha256=ca883a49e4fc69d2...  (0s)
  MIRRORED + VERIFIED  seq8_extract_run1.log                              0.0 MB  sha256=5f998f59119fa77a...  (0s)
  local seq8 after: 1783.5 MB across 15 files - UNCHANGED (copy-only proven: name+size+mtime_ns identical for all 15)
  D: mirror: 15 files, 1783.5 MB  (source 15 files, 1783.5 MB)  MATCH
```

**The copy-only proof.** Two independent `os.walk` manifests of `research_outputs/seq8` were taken, one
before the first copy and one after the last, each recording `(size, mtime_ns)` per relative path. The
dicts compare **equal on all 15 entries** — identical names, identical sizes, identical nanosecond mtimes.
An mtime match is the strong half: any write, truncate or re-create would move it even if the size held.

**Destination cross-check.** `D:/Naiad/research_outputs/seq8` re-walked independently after the run:
15 files / 1783.5 MB against source 15 files / 1783.5 MB — **MATCH** on both count and total bytes.

### 4a · Correction to the previous report — `seq8_run2` is **not** identical file-for-file

The 2026-08-11 bulk-relocation report concluded `seq8_run2` "is a copy" and its 1783.5 MB "was pure
redundancy." That is right about the **data** and wrong as a blanket statement. This session's digests for
`seq8` can be compared against last session's digests for `seq8_run2`, and the three files the top-8
pair-hash never reached **all differ**:

| file | `seq8_run2` (2026-08-11, prior session) | `seq8` (this session) | |
|---|---|---|---|
| `seq8_extract_manifest.json` | `697109a69c67bab3…` | `07aa3fde63f7c049…` | **DIFFERS** |
| `seq8_outcomes_manifest.json` | `67a219befe09b48d…` | `ca883a49e4fc69d2…` | **DIFFERS** |
| `seq8_views_summary.json` | `7c619cb0b1763805…` | `6379f734dade0d25…` | **DIFFERS** |

The prior report's pair-hash covered the **eight largest** files and stated that scope, so nothing it
printed was false — but the summary sentence generalised past its evidence. The precise finding:

**`seq8_run2` matches `seq8` byte-for-byte on all 8 data files and differs on all 3 of its metadata
files.** That is exactly the signature of a determinism rerun — identical outputs, fresh run manifests
carrying that run's timestamps and identifiers. The 1783.5 MB of *data* was genuinely redundant; the few
KB of *run-2 provenance* was not, and is the only thing a discard would cost. This bears directly on
open item 2 below.

Note also `seq8` holds 15 files to `seq8_run2`'s 11: `seq8_atlas_replication.json`, `seq8_fixtures.json`,
`seq8_fixture_transcript.txt` and `seq8_extract_run1.log` exist only in the primary. Nothing exists only
in `run2` except the three metadata variants above.

---

## 5 · R3 — the anti-`_run2` rule

Inserted at the end of §4, 47941 → 48410 bytes, **6 insertions / 0 deletions**, LF preserved
(`CRLF=0 LF=833`):

```diff
@@ -541,6 +541,12 @@ never a directory listing.**

 **The live tick set is `LEDGER.md` and `exchange/` ONLY** (operator, 2026-08-06; see §3.2). …

+**Determinism reruns: hash-and-compare, then discard — rule R3, operator 2026-08-11.**
+A rerun exists to prove byte-identity, and the hash IS that proof. Print both digests in the build
+document, then delete the rerun copy in the same session. Never retain it: three retained _run2
+trees held ~3.2 GB of pure redundancy (seq8_run2 relocated 2026-08-11; journal_s3_run2 and
+s3_events_run2 live inside the s3 phase archive). Every study contract inherits this clause.
+
 ---

 ## §5 · Lane charters
```

---

## 6 · Before / after

| | before this session | after | delta |
|---|---|---|---|
| local working tree (excl. `.git`) | 2292.3 MB / 816 files | 2292.3 MB / 816 files | **0 — nothing local was added or removed** |
| local `research_outputs/seq8` | 1783.5 MB / 15 files | 1783.5 MB / 15 files | 0 (copy-only) |
| `D:` `_unarchived_s3_2026-07-27` | 1376.1 MB / 753 files | **gone** | −1376.1 MB |
| `D:` `research_outputs/seq8` | absent | 1783.5 MB / 15 files | +1783.5 MB |
| `D:` `research_outputs` total | 4155.0 MB / 782 files | 4562.3 MB / 44 files | +407.3 MB, −738 files |

Final D: layout:

```
  DIR   _archive                                         995.2 MB  18 files
  DIR   seq8                                            1783.5 MB  15 files
  DIR   seq8_run2                                       1783.5 MB  11 files
```

Local:

```
  PRESENT  research_outputs/seq8                          1783.5 MB  15 files
  ABSENT   research_outputs/seq8_run2
  PRESENT  research_outputs/_unarchived                       0.0 MB  0 files
```

---

## 7 · File-disposition table

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `exchange/status/CONVENTIONS.md` | yes | tracked | see §10 | see §10 | GitHub + estate zip | +469 bytes (0.007% of 6.39 MB box) |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-11_R1-R2-R3.md` | yes | tracked (new) | see §10 | see §10 | GitHub + estate zip | 16,624 bytes (16.2 KB, 0.248% of box) |
| `research_outputs/seq8/` | yes | ignored — `.gitignore:110` | not committed | no | **D: `research_outputs/seq8`, 15/15 sha256-verified this run** — exposure closed | n/a — not in sync selection |
| `D:/Naiad/research_outputs/seq8/` | yes (new) | n/a (off-repo) | n/a | n/a | D: drive only | n/a — unsynced drive |
| `D:/Naiad/research_outputs/_unarchived_s3_2026-07-27/` | **REMOVED (R1)** | n/a (off-repo) | n/a | n/a | `s3_2026-07-27.zip`, sha256 == repo sidecar, verified this run | n/a |
| `D:/Naiad/research_outputs/_archive/s3_2026-07-27.zip` | yes | n/a (off-repo) | n/a | n/a | D: drive only — sidecar tracked on GitHub | n/a |
| `research_outputs/_archive/s3_2026-07-27.zip.sha256` | yes | tracked, unchanged | unchanged | unchanged | GitHub | n/a |
| `D:/Naiad/research_outputs/seq8_run2/` | yes | n/a (off-repo) | n/a | n/a | D: drive only — **now redundant under R3, see §8** | n/a |
| 9 untracked repo files | yes | untracked | not committed | no | **NOT PROTECTED** | n/a — none under `exchange/` |

No data artifact was placed in `exchange/`. Both files added here are prose.

---

## 8 · Open items

1. **Queue 002 has NOT been executed as its own session — it remains the standing next build.**
   `exchange/queue/002_backup-and-publish-guards.md` is RATIFIED (operator 2026-08-04, rulings G1-a/G5-a,
   amended 2026-08-06 ruling B). The only reports touching it — `…_ARCHIVE-VERIFY-AND-QUEUE-002.md` and
   `…_SIDECARS-AND-LANE-CLOSE.md` — *filed* it and reduced its D4 to a fixture; neither executed it. The
   2026-08-04 report's own next-step 5 reads "Execute queue item 002 — **its own session, its own build
   document**." That session has not happened. Its three defects are still live: `--phase` cannot write
   off-machine, `--phase --dest` exits 0 while writing inside the repo, and `publish_exchange.py` has no
   size guard at all. `DIGEST.md` line 114 also shows its **verdict criteria: NOT FOUND**.

2. **R3 points at `D:/Naiad/research_outputs/seq8_run2` (1783.5 MB) — but see §4a before ruling.**
   R3 says a rerun is discarded once its hash has proved byte-identity, and as of R2 `seq8` is itself on
   D:, so that tree's 8 data files are now duplicated on the same drive. **However, §4a shows the twin
   claim does not hold file-for-file:** its 3 metadata files differ, and they are the only record of what
   run 2 actually did. Two clean options, operator's call:
   **(a)** extract the 3 manifests into the build record or a small `seq8_run2_manifests/` folder, then
   delete the tree — reclaims 1783.5 MB and loses nothing that a hash has not already proved redundant;
   **(b)** keep the tree until a full 11-file hash comparison is run, if run-2 provenance is load-bearing
   for MC-1. **Nothing deleted — this paste authorized removal of the `_unarchived` tree only, and
   "nothing else is deleted anywhere."**

3. **Nine untracked repo files still need filing** (unchanged from the previous report): three HTML
   atlases, three markdown handoffs, one parquet under `briefs/`, and `scripts/mc1_program.py` +
   `scripts/mc1_report.py`. ~0.5 MB total, all currently unprotected.

4. **CONVENTIONS anchors keep failing.** Two consecutive pastes, two wrong insertion points — a TOC hit,
   then a mid-sentence hit in the wrong section. Worth adding to §2 that a paste editing `CONVENTIONS.md`
   must print the surrounding lines of its anchor before writing, since occurrence counting demonstrably
   does not catch placement.

---

## 9 · Publish

`publish_exchange.publish(repo, '2026-08-11')`, staging `exchange/**` only. Publish result, commit SHA,
push confirmation and the remote-presence checks are recorded in §10 below, written after the publish
returned — a document cannot contain its own commit hash, so a second commit carries this section.

---

## 10 · Publish result

```
publish: committed 5c15a59 (2 path(s)) and pushed to origin/v12-v1-census
status= PUBLISHED commit= 5c15a59 pushed= True offenders= []
```

Verified after the fact, not assumed:

| check | result |
|---|---|
| files in `5c15a59` | 2 — `exchange/status/CONVENTIONS.md` (+6), this report (+285) |
| paths outside `exchange/` in the commit | **none** |
| local head vs `origin/v12-v1-census` | both `5c15a59` |
| report present at `origin/v12-v1-census` | yes (`git cat-file -e`) |
| R3 rule present in the **remote** CONVENTIONS copy | yes (1 match) |

A second commit carries §10 itself, for the reason given in §9.

**Session chain:** `2cd6f53` (previous session close) → `5c15a59` (R1/R2/R3 + this report).

---

## 11 · Rollback

- **R1:** re-extract `D:/Naiad/research_outputs/_archive/s3_2026-07-27.zip` case-sensitively to restore
  the loose tree. The archive was sha256-verified against the repo sidecar in this run.
- **R2:** `rm -r D:/Naiad/research_outputs/seq8` — copies only; the local tree was never modified.
- **R3:** `git checkout -- exchange/status/CONVENTIONS.md`.
