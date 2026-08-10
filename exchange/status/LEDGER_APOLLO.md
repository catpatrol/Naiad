# LEDGER_APOLLO — append-only lane ledger

**Lane:** APOLLO — engine builds · repo operations · integrity & manifest.
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

=== STATUS_APOLLO — 2026-07-27 ===
NOW: Engine 1.0.11 frozen. Repo at manifest snapshot HEAD 60e00c9, ahead 4 / behind 0 vs origin 70a5be0, worktree clean. THE BIG CORRECTION: the raw price estate was never under OneDrive — it sat unprotected in AppData\Local\naiad\data_cache (633.5 MB, 71 files) for the project's whole life, and now has its first offsite backups on two independent Google Drive accounts.
LAST EVENT: 2026-07-27 — Estate protection established; OneDrive root-caused (quota exhaustion, 21.78 GB tree); 19.61 GB reclaimed across six archived phases (13,502 members, 0 mismatches, reviewer re-hashed 6/6 + 90 sampled members; 25 git-tracked files preserved in place); tree down to ~1.9 GB.
FACTS:
- Integrity at snapshot: 46/46 tracked sources match HEAD; box 19 repo copies match + 2 brief artifacts + 1 stale .gitignore [verified]
- Rulings R-A (cloud sessions scoped to Naiad only), R-B (second-cloud dated non-overwriting archives), R-C (corrections folded, 713dfa7→72b921f amended-SHA on record) [ratified]
- Standing rule: every paste-go opens with a hard environment assertion that halts — read-only included — and no write precedes it; gates written from POST-action state [ledger]
- Routing failures final count on 07-26/27: seven, not three; every labelled paste was halted by its header [ledger]
- %G? reports N when SSH verification is impossible, not only when unsigned — not a signature-presence test [verified]
PENDING:
1. PUSH RULING — unpushed commits were then the only asset without an off-machine copy
2. R-A' proposed, not ruled: cloud-session commits must push same-session or they don't count
3. s3_excursion_substrate.jsonl git-tracked while sibling substrates are fenced — exception or drift?
4. Remaining backup steps: six phase archives to the second cloud · .venv relocation · .gitignore sync exclusions
NEXT: Item 1 (push ruling), then a fresh MANIFEST.json to confirm ahead/behind returns to 0. Owner: operator.
METRICS: operator actions this session = not recorded (predates Q-8) · files re-ingested = not recorded
=== END STATUS ===

**Provenance note (HEPHAESTUS, 2026-08-02):** this seed entry is a synthesis of the lane's standing
status document, carried over unmodified in substance at ledger adoption. Source document:
`docs/history/STATUS — ENGINE (engine builds · repo operations · integrity & manifest).txt`
(2,917 B, updated 2026-07-27 late) — it sat at repo root when this ledger was seeded and was **moved
to `docs/history/` later the same day** by the repo filing pass; the pointer is updated here so it
does not rot. It is dated 2026-07-27 and its PENDING items may since have been resolved — several of
them demonstrably were. **Treat as stale until APOLLO appends a current entry.** [handoff]

---

=== STATUS_APOLLO — 2026-08-10 ===
NOW: The 9-day staleness is closed. This entry lands the owed append (re-priming 08-05 + rulings
08-06 + the synthesis filing) and carries the MC-1 v2 run executed locally on branch v12-v1-census
at HEAD 7a3a881. The P-SEQ-ii ledger-entry check owed since 08-04 is discharged with a NEGATIVE
finding: the entry does not exist in `LEDGER.md` and never did.
LAST EVENT: 2026-08-10 — MC-1 v2 (THE MAY-26 PROGRAM) executed end to end by HEPHAESTUS: D-1 D-3
D-4 D-5 D-6 D-7 D-8 built, F-MC1..F-MC11 run, three registrations scored before their result tables.
FACTS:
- Re-priming after context loss recorded 2026-08-05; rulings 2026-08-06 = MC defaults (every *Lean*
  of MC-1..7, §3.4) + rule set v0.2 (§1.2) + the path committed to memory (§3.1) [ratified]
- Amendment 2026-08-06 "continuous queryability before/after the cross" honoured by D-3(a)/(f); the
  offered lockbox change was DECLINED as unnecessary — the dossier is ops-class and the seal was
  NOT modified by this contract [ratified]
- `SS_SYSTEM_SYNTHESIS_2026-08-06.md` was NOT attached to the MC-1 paste; the resident copy is
  filed and hashed sha256 f184f105c0612128c9ed5819d72fe6ff0c2d123378b0923d08b90bc856c4c7f2,
  31,822 B, 0 CR bytes — byte-identical filing re-asserted, not overwritten [verified]
- P-SEQ-ii: `grep -c "P-SEQ" LEDGER.md` -> 0 over 871 lines. The entry is ABSENT, not divergent —
  neither CONFORMS nor a diff. Registration text and the ordering-anomaly note exist only outside
  the evidence ledger and are reproduced verbatim in the build document [verified]
- MC-1 headline: D-1 490 cells (F-MC1 0 diffs on all 56 SEQ8-D6 overlap cells, 3 hand-recomputed);
  D-4 1,569 4H lattice-A crosses, strict core 4/4 = 105; D-6 bridge 301,018 rows, 0 orphans
  join->journal, 286 births never joined (SEQ8's own figure); P-i SUPPORTED 3/5, P-iii SUPPORTED
  (L 52.3% vs W 14.0%, CI [0.316,0.448]), P-iv SUPPORTED 3/5 [verified]
PENDING:
1. P-SEQ-ii ledger entry still UNLANDED — the proposed text (prior 75%, verdict REPLICATES 7/7)
   is the reviewer's to land in `LEDGER.md`; the builder does not write to the evidence ledger
2. P-i and P-iv are VIEW-DEPENDENT: both score 3/5 on `24h|window_chained` but 2/5 on all four
   `direction_consistent` views. The registrations named no view. Operator ruling wanted
3. MC-1's §3.4 feasibility premise ("1M carrying {12,25} only, 1W carrying up to 200") does not
   hold under the exploration ceiling — it assumed full-estate bar counts. D-1 measures 1W to
   EMA25 and 1M to EMA12 only
4. `scripts/mc1_program.py` is uncommitted: `publish_exchange.py` stages only `exchange/**`, so
   the program itself cannot ride the auto-publish
NEXT: Operator rules on PENDING 2 (view selection for P-i/P-iv); reviewer lands PENDING 1. Owner:
operator, then APOLLO.
METRICS: operator actions this session = 1 (the MC-1 paste) · files re-ingested = 0
=== END STATUS ===
