# 003 · Report rotation, rerun provenance, and the anchor-context rule

RATIFIED: **operator, 2026-08-11** — "ratify 003", issued after verifying the filing report.
Drafted: ATHENA, 2026-08-11. Executor: HEPHAESTUS. Ratification resolves both findings of
`BUILDERS_REPORT_HEPHAESTUS_2026-08-11_QUEUE-003-FILED.md` (3.1 and 3.2, both applied below).
Runs AFTER queue 002 (D-1's box arithmetic assumes 002's D3 guard exists; if 002 is unbuilt,
build it first and say so).

## Why this exists
`exchange/` is ticked into the ~6.39 MB project box and grows with every session by design (one
build document each, no exceptions — CONVENTIONS §3.1). Measured trajectory: **17.9% of the box on
2026-08-05 → 26.2% on 2026-08-11** (builder-measured from git, finding 3.2). The drafted ~21%/~31%
were not wrong, they were the wrong subject: they are whole-**box** readings — `exchange/` plus
`LEDGER.md`, the tick set — which measure 21.9% and 30.4% at those same commits, verified. The
figures above are `exchange/`-only, which is what 002's D3 guard actually meters. Growth of +8.3
points in six days reaches the 40% refuse line in roughly ten more days of comparable activity.
Queue 002 D3 warns at 25% and refuses at 40%: without rotation, normal reporting hits the refuse
line within weeks. Rotation makes the box steady-state — the
current month's record hot on the bus, everything older archived, tracked, and findable.

## Deliverables
**D-1 · `scripts/rotate_reports.py`.** Scope: `exchange/reports/*.md` ONLY. Selects files whose
filename date (YYYY-MM-DD; fall back to first `git log` date if unparseable) is older than
**30 days** — constant PINNED at ratification 2026-08-11; the `[VETO]` marker was finding 3.1 and
the drafted default stands. For each: sha256 → `git mv` to `docs/history/reports/YYYY-MM/<name>` → sha256
at destination must match → append one line (name, new path, sha256, date) to
`exchange/status/ROTATION_LOG.md`. **Moves only — the script contains no delete call of any
kind.** Exemptions, checked per file: **any `NOTE_*` file that is the NEWEST note of its
lane pair** — sender→recipient parsed from the filename, broadcasts grouped as
`<LANE>→ALL-LANES`, newest by filename date with mtime as tie-break; anything under
`exchange/status/`, `queue/`, or `DIGEST.md` (out of scope by construction). `--dry-run`
is the default; `--execute` required to move.
**D-2 · Cadence.** The bus-health block lists rotation candidates (count +
bytes + % of box) on every publish and in `status/daily/DAILY_<date>.md` §8 — it replaced HERMES's
DIGEST box-budget section when ruling 007 (2026-08-15) retired the DIGEST and put that lane dormant — within his existing charter, no new instruction surface. The
operator says "rotate" roughly monthly; the builder runs D-1 with `--execute` in its own session.
Nothing rotates unattended.
**D-3 · R3 refinement in CONVENTIONS §4.** The determinism-rerun rule gains: after the hash-proof,
discard the rerun's DATA files; **retain its run manifests and logs** (KB-scale) beside the build
document or in the phase archive — they are the second run's provenance and the only thing a
discard costs (finding §4a, R1-R2-R3 report: seq8_run2 = 8/8 data files identical, 3/3 manifests
distinct).
**D-4 · Anchor-context rule in CONVENTIONS §2.3.** Any paste editing CONVENTIONS.md prints ≥3
lines either side of its anchor BEFORE writing, and the build document shows them. Earned by two
consecutive placement misses that occurrence-count guards passed: `### 3.1` matching the index
copy, and a once-occurring string sitting mid-sentence in the wrong section.

## Fixtures — HALT loudly on any failure; F-303-1..5 run on a fabricated temp tree
- **F-303-1** dry-run selects exactly the >30d set; <30d files and exempt notes excluded, printed.
- **F-303-2** `--execute`: files land under `docs/history/reports/YYYY-MM/`, destination sha256 =
  source sha256, originals absent, ROTATION_LOG carries one line per file.
- **F-303-3** history follows: `git log --follow` on a rotated file returns its pre-move commits.
- **F-303-4** idempotence: an immediate second `--execute` selects nothing.
- **F-303-5** a file 29 days old never moves, even with `--execute`.
- **F-303-6** real tree: dry-run output printed in the build document; then one real `--execute`
  sweep in the same session, before/after `exchange/` box % printed. (Near-empty result is
  expected today and is not a failure.)
- **F-303-7** D-3 and D-4 edits: anchor context printed pre-write per D-4's own rule; diff shown;
  line endings preserved (CRLF/LF counted before and after).
- **F-REG** publish still works; the 002 D3 guard (if built) sees the post-sweep size.

## Verdict criteria
ACCEPT only if: every fixture passes with output printed · the script provably contains no delete
path (grep for os.remove/rmtree/unlink printed empty) · every rotated file is sha-identical at its
destination AND reachable via `git log --follow` · nothing outside `exchange/reports/` moved ·
D-3/D-4 landed at the positions their printed context shows. REJECT and halt on any miss.
D-1+D-2 ship together; D-3 and D-4 may ship independently.

## What this phase is NOT
Not deletion or retention-policy change — rotated reports remain tracked, on GitHub, and
drag-on-demand. Not a change to `publish_exchange.py` or `backup_estate.py` (002's ground). Not
rotation of LEDGER.md, lane ledgers, CONVENTIONS, queue items, or the DIGEST. Not automation —
every sweep is operator-triggered.

## Deliverable document
ONE build document per CONVENTIONS §3.1, full fixture transcript, disposition table with BOX COST.


---

## CORRECTION 2026-08-22 — D-1's exemption input, and D-2's cadence surface

**RATIFIED: operator, 2026-08-22** — root-adjudication brief, *"Amend queue 003 D-1 per its own
recommended fix: the unacted-inbox exemption = the newest-NOTE-per-lane-pair rule (as implemented in
the 08-18 sweep), replacing the DIGEST read."* Drafted and executed: HEPHAESTUS.

**WHAT D-1 SAID BEFORE THIS CORRECTION, quoted once and asserted nowhere:** *"Exemptions, checked
per file: any `NOTE_*_to_*` file listed as unacted inbox in the newest DIGEST."*

**WHY IT HAD TO CHANGE.** Ruling 007 (2026-08-15) retired `exchange/DIGEST.md` and left a tombstone
at its path. The exemption's only input died with it, and from that day
`rotate_reports.py --dry-run` **halted with exit 2** rather than classifying anything — correctly,
since it will not guess which notes are live, but with the consequence that **no rotation could run
at all**. That was finding F-2 of
`BUILDERS_REPORT_HEPHAESTUS_2026-08-18_BOX-CLEANUP-MAILBOX.md`, and it went unnoticed for seven days
because nothing calls the script on a schedule.

**WHAT BINDS NOW.** The exemption is **computed from the bus itself** — the newest `NOTE_*` of each
lane pair is live and exempt; anything older in the same pair has been superseded by it and may
rotate. **The rule has no external input, so it cannot become unavailable the way the DIGEST did.**
It was applied to all 15 notes in the 2026-08-18 sweep before it was written down here.

**TWO SUBSTANTIVE WIDENINGS, NAMED RATHER THAN SLIPPED IN:**

1. **The note pattern widens from `^NOTE_.+_to_.+` to `^NOTE_`.** The old pattern only ever matched
   `NOTE_<FROM>_to_<TO>_…`. Broadcasts — `NOTE_HERMES_2026-08-12_ALL-LANES_…`,
   `NOTE_DIONYSUS_2026-08-12_PANTHEON_…` — never matched it, so **they were never exemptible at all**,
   even while the DIGEST worked. The new rule protects them.
2. **The exemption no longer depends on anyone maintaining a list.** D-2's cadence surface is
   corrected in the same act: it named "HERMES's box-budget section in the DIGEST", and HERMES has
   been dormant since ruling 007. The bus-health block already does that job.

**WHAT DID NOT CHANGE:** `AGE_DAYS = 30`, `SCOPE_DIR`, `DEST_ROOT`, the sha256→`git mv`→sha256
discipline, the no-delete invariant, `--dry-run` as the default, and the out-of-scope-by-construction
list. This correction replaces one input and one stale pointer; it is not a retention-policy change.

**Both assertions above are REWRITTEN in place, not annotated** — §0's correction rule — and this
note records what changed and why.