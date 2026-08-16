# LEDGER_HEPHAESTUS — append-only lane ledger

**Lane:** HEPHAESTUS — local builder. Sole actor that touches the data estate
(`AppData\Local\naiad\data_cache`). Executes ratified queue items; heavy compute stays local.
**Adopted:** 2026-08-02, ruling Q-3 A (`FUNNEL_DIONYSUS_W1`). Append-only. Never edit a past entry; a
correction is a NEW entry that names what it supersedes. The central `LEDGER.md` remains the
*evidence* ledger and is untouched by this file — this one carries coordination state only.

**Entry template (naiad-eod format):**

```
=== STATUS_<LANE> — <date> ===
NOW: <2-3 sentences>
LAST EVENT: <date> — <one line>
FACTS: <up to 6 lines, each ending with [verified/ledger/ratified/handoff/unconfirmed-live/open]>
PENDING: <numbered items waiting on the operator>
NEXT: <single next action + owner>
METRICS: operator actions this session = <n> · files re-ingested = <n>
=== END STATUS ===
```

---

=== STATUS_HEPHAESTUS — 2026-08-02 ===
NOW: Ledger founded, and founded with work in it. This lane had no prior status document, so nothing before 2026-08-02 is claimed here — but this session's build is recorded in full: exchange v1 skeleton, per-lane ledgers, reviewer-box migration, manifest v1.1, auto-publish, both Windows triggers, and queue item 001.
LAST EVENT: 2026-08-02 — exchange v1 built end to end under gate A-7 authorization; full account in `exchange/reports/2026-08-02_HEPHAESTUS_report_exchange-v1-build.md`.
FACTS:
- `exchange/{status,queue,reports,drops}/` created with a content guard: text only, 1 MB per-file cap, larger artifacts referenced by path + sha256 pointer [verified]
- `_reviewer_box/` retired as a location: reports, `daily/` and `MANIFEST.json` migrated to `exchange/`; a one-line pointer README is left behind [verified]
- `scripts/reviewer_manifest.py` amended to v1.1: BOX_DIR repointed, F-M1 became a round-trip test with the self-hash kept as a secondary assertion, four new fields added [verified]
- Auto-publish added to `daily_routine.py` and `backup_estate.py` via `scripts/publish_exchange.py`: stages `exchange/**` only, refuses to push if anything else is staged [verified]
- Windows triggers armed: "Naiad daily routine" daily 07:00, "Naiad weekly backup" Sundays 08:00, both start-in the repo root, both calling the venv interpreter by full path [verified]
- `backup_estate.py` gained a retention REPORT (keep newest 4 estate generations + 1 phase set); it lists violations and never deletes [verified]
PENDING:
1. Queue item 001 awaits the operator's ratification stamp — it is not executable until stamped
2. The daily routine's brief job is optional and its behaviour under the 07:00 trigger is unproven until the first unattended run
NEXT: Work the queue once item 001 is ratified. Owner: operator (ratification), then HEPHAESTUS.
METRICS: operator actions this session = 1 · files re-ingested = 0
=== END STATUS ===

---

=== STATUS_HEPHAESTUS — 2026-08-15 — QUEUE 005 M2 v2 — RESTORE EXECUTED ===
NOW: M2 RAN TO COMPLETION for the first time, under the operator's DATA RESIDENCY v2 ruling (everything local under ~/Naiad; the LaCie is BACKUP ONLY). All four halts are cleared, the full substrate set is restored and hashed, the estate is live, and the Mac suite is 287 passed / 0 failed — better than the Windows machine it came from. The prior M2 entries live in LEDGER_ATHENA (2026-08-14); this entry is filed here because the session touched the data estate, which is this lane's charter.
LAST EVENT: 2026-08-15 — full restore + audit + sweep on Luiss-MacBook-Pro.local; filed as exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-15_M2-RESTORE-V2.md. Executed as 13 parallel verification agents; every claim in the report was independently re-checked before filing.
FACTS:
- SUBSTRATE RESTORED AND HASHED: 425 files / 7.45 GB across _archive, census, census2a, census2b, mc1, seq8, seq8_run2 — 0 mismatches, 0 missing, 0 genuine extras. The three folders the 2026-08-14 entry called UNRECOVERABLE WITHOUT THE LACIE (census2a 82, census2b 261, seq8_run2 11) are recovered. Every file was hashed on both sides; the >200MB partial-hash allowance was available in four folders and declined in all four [verified]
- BUT ONLY 78.8% IS EXTERNALLY ATTESTED. 89 of 425 files (~21% by count, >=1.58 GB by size) rest on two-witness agreement alone, which detects transit/media corruption and NOTHING ELSE. The largest artifact in the estate, seq8_cascades.jsonl (789,501,107 B), is pinned by neither seq8 manifest. `basis: manifest` is a MAXIMUM, not a coverage claim — it is 8 of 30 files in mc1, 5 of 15 in seq8. seq8's trust chain is circular: its manifests are pinned by nothing external [verified]
- naiad-backups IS THE TWIN, PROVEN NOT INFERRED: 51/51 byte-identical local vs LaCie across ~2.9 GB, plus a third identical copy at /Volumes/LaCie/Repo Clone holding nothing unique — 153 files / ~8.7 GB hashed across three trees, 0 mismatches, nothing sampled. This is the independent second witness the 2026-08-14 sidecar-only check correctly refused to claim it had. NOTHING WAS DELETED; the operator holds the word. RECOMMENDATION IS TO WAIT: both surviving copies are on the SAME LaCie spindle, so retiring the in-repo vault moves the estate from 3 copies on 2 devices to 2 copies on 1 device — one-role and 3-2-1 point in opposite directions here [verified]
- BASELINE RETAKEN AND NO LONGER PROVISIONAL: 287 passed / 0 failed / 1 skipped, vs 282/4/2 on the empty estate and 287/1 on Windows. Totals hold at 288 across all three runs — no test lost or gained in the platform crossing. All four data-starvation failures resolved by the estate restore, exactly as the provisional baseline predicted. Estate verified 73/73 against its own MANIFEST.json, itself attested by the LaCie's sidecar over local bytes. ATHENA PENDING #3 discharged [verified]
- CENSUS2B IGNORE GAP FOUND AND CLOSED BEFORE THE RESTORE RAN: research_outputs/census2b/** was absent from .gitignore while census2a, seq8_run2, mc1 and mc2 were all covered. Restoring 2.1 GB / 261 files would have re-created the 2026-08-05 condition (untracked-but-unignored bulk; that incident cost a rejected branch push). Rule added first, then the restore; git status --porcelain confirms only .gitignore is modified [verified]
- THE ESTATE IS 64 COMMITS STALE AND NOTHING NEWER EXISTS ANYWHERE. SUPERSEDES the 2026-08-14 reasoning that "the LaCie almost certainly holds a newer one" — an exhaustive volume search returns four generations (07-28, 08-02, 08-09, 08-11) and 08-11 is the newest on any medium. Its repo_head e835755 is in our history, 64 commits behind HEAD, predating all census2b work. A current estate must be BUILT on this Mac; it cannot be restored from anywhere [verified]
PENDING:
1. Operator, BLOCKING the vault question: the delete word. Recommendation is DO NOT GIVE IT YET — establish a second-device copy and verify it BEFORE retiring ~/Naiad/naiad-backups, or resilience drops to one device. research_outputs/_archive should be kept regardless (operator ruling B; POINTER.md designates it permanent evidence)
2. Operator: all 9 _archive sidecars are CRLF, so a plain `shasum -a 256 -c` reports 9/9 FAILED on a PERFECT restore. Anyone auditing without reading the report will conclude corruption. Workaround `tr -d '\r'`; rewriting them LF is your call — they are tracked evidence
3. Operator, one line either way: should research_outputs/census2b/**'s manifests be TRACKED (census1b precedent, explicit negation) or stay ignored (census2a precedent, which is what I applied)? I did not newly track files on my own initiative
4. M3, first item: scripts/census2a_program.py:185 and scripts/mc2_program.py:270 assert OUT.drive.upper() == "D:". Path.drive is ALWAYS "" on POSIX, so both HALT UNCONDITIONALLY on this Mac. 43 real drive-literal defects catalogued in the report
5. M3, DO NOT DO THIS: the 15 hits inside research_outputs/**/*.json are SEALED EVIDENCE. Rewriting them falsifies provenance AND destroys the byte-equality with the LaCie that this drill just established. Fix the CONSUMERS to map D:\Naiad\ -> repo root at read time. Likewise the 38 doc-only hits are historical records and must not be "fixed"
6. Reported, no action proposed: seq8_run2 is a strict byte-exact subset of seq8 (~1.87 GB duplicated in the working tree; only 4 small files differ, 22,642 B). research_outputs/_archive/POINTER.md still maps to D:/ and G:/ paths that exist on no medium here
7. Carried: HALT 1 remains degraded-not-blocking — recover requirements-lock-2026-08-14-win.txt from the Windows box before it is wiped, for transitive parity only. cache_dir() still mkdirs on read at engine/data.py:47
NEXT: Answer PENDING 1 and 3 (one word each), then M3 takes the sweep list. Owner: operator.
METRICS: operator actions this session = 0 · files re-ingested = 425 (+74 estate) · bytes hashed = ~16 GB · mismatches = 0 · halts cleared = 2 · deletions = 0 · sources touched = 0
=== END STATUS ===

---

=== STATUS_HEPHAESTUS — 2026-08-15 — RULING 007 — DIGEST RETIRED, HERMES DORMANT ===
NOW: DIGEST.md is retired to docs/history/ with a 561 B tombstone at its old path, HERMES is DORMANT with five duties routed and two named as PARKED, and the residue that lane produced by hand is now measured by publish() and the daily routine's new section 8. Five adversarial agents were run against the finished build and found thirteen defects in my own work, one of them blocking; all are fixed. F-CONV 4/4, suite 324 passed / 1 skipped.
LAST EVENT: 2026-08-15 — ruling 007 executed; filed as exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-15_RULING-007.md.
FACTS:
- THE RULING'S OWN git mv WOULD HAVE DESTROYED ITSELF. `docs/history/DIGEST_RETIRED_2026-08-15.md` is OUTSIDE publish_exchange.SCOPE, so a publish would have FLAGGED, `git reset` would have wiped the staged rename, and the next publish would have committed the tombstone OVER the DIGEST with the final edition never committed at all. Proven end-to-end in a clone. Cured by putting the rename, the tombstone and the fixture in ONE hand commit before any publish — which is also the shape that keeps `--follow` working, itself replayed and confirmed at 9 commits back to 2026-08-02 [verified]
- ROTATION WAS THE ONLY CODE COUPLED TO DIGEST, AND IT WOULD HAVE FAILED SILENTLY, NOT LOUDLY. digest_inbox_names()'s "search it all" fallback scrapes .md names from the whole file, so against a tombstone it returns 2 names and the banner prints "DIGEST inbox : 2 name(s) parsed" — a successful-looking parse of an inbox that no longer exists, six live unacted notes quietly unprotected, first candidate 2026-09-03 (measured by stepping classify() day by day; "date + 30" is one day early). Now raises InboxSourceUnavailable and exits 2. NO ratified policy touched: AGE_DAYS, SCOPE_DIR, NOTE_RE and the `name in inbox` test are exactly as queue 003 ratified them — only what happens when the rule's INPUT is unobtainable changed, from inventing an answer to refusing one [verified]
- CONVENTIONS GREW AND THE LAW STAYED. The edits broke F-CONV-4's shrink clause; the fixture's own docstring rules on exactly that case — re-pin with a dated note, never trim a rule to hit a number. CONV_BYTES_BEFORE was NOT overwritten (it means "size before the collapse" and three filed documents quote it); a new CONV_BYTES_CEILING carries the live clause, with headroom, after §6.4's three legs ran. The census clause was narrowed to frozen evidence and a live rule-count floor of 89 added — 89 at the collapse, 89 now [verified]
- SUITE BASELINE RE-MEASURED AND THE QUOTED FIGURE IS STALE. Ledgers carry "287 passed / 1 skipped = 288 = fixtures 74 + tests 214". Live at 20f23a1 BEFORE this build: 299 / 1 = 300 = fixtures 74 + tests 226, the +12 being tests/test_box_guard.py. A third version, 286/1, sits in LEDGER_ARGUS. After F-BH-1: 324 passed / 1 skipped = 325 = 74 + 251. Do not re-quote 288 [verified]
- THE BLOCK CONTRADICTED THE RULING THAT CREATED IT, UNTIL REVIEW CAUGHT IT. The recency table reported dormant HERMES as the stalest lane in the project by a margin growing one day per day forever, while §5 says nothing waits on HERMES. Now labelled DORMANT. Same class of error: §5 first claimed EVERY duty absorbed when "files drops" had no successor — now named as PARKED alongside the unacted-inbox list [verified]
- MANIFEST.json IS NOT A FILE INVENTORY AND §0 SAID IT WAS. Measured: `sources` is 46 hardcoded engine/script paths, `reviewer_box` is 29 paths ALL under exchange/status/ — it lists no report on the bus. §0, §4.3 and the tombstone now credit it with repo state and point "what the bus is carrying" at the bus-health block [verified]
PENDING (operator):
1. WHERE DOES THE UNACTED-INBOX LIST LIVE? Deadline 2026-09-03, when the first of six notes becomes a rotation candidate. Until ruled, rotate_reports halts rather than guess. Restoring it is a one-line repoint of DIGEST_PATH
2. Queue 003 D-2 named HERMES's DIGEST section as where the rotation-candidate figure is published each cycle. The bus-health block now publishes it, but re-homing a RATIFIED cadence is not the builder's to do
3. `exchange/reports/PRIMER_HERMES_2026-08-11_v4.md:102` still instructs HERMES to rebuild DIGEST every cycle. Superseding it instructs another lane and needs your stamp (§5)
4. `exchange/drops/` — nothing now names and files what you leave there
5. The live Claude project-memory panel still records HERMES's duty as "DIGEST 2x/day, box budget, staleness stamps, inbox". Only you can edit it; the repo snapshots were left alone
6. F-BH-1 does not run in CI — ci.yml runs `pytest fixtures/` only, so tests/ (including F-BOX-1) never executes on push. One-line fix not applied: widening CI scope is an ops call
NEXT: Answer PENDING 1 (one line), then the September sweep can run. Owner: operator.
METRICS: operator actions this session = 0 · files re-ingested = 0 · verification agents = 10 · defects found in own work = 13 · defects fixed = 13
=== END STATUS ===
