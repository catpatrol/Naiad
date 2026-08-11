# 003 · Report rotation, rerun provenance, and the anchor-context rule

RATIFIED: **PENDING** — operator ratifies with one word. Drafted: ATHENA, 2026-08-11.
Executor: HEPHAESTUS. Runs AFTER queue 002 (D-1's box arithmetic assumes 002's D3 guard exists;
if 002 is unbuilt, build it first and say so).

## Why this exists
`exchange/` is ticked into the ~6.39 MB project box and grows with every session by design (one
build document each, no exceptions — CONVENTIONS §3.1). Measured trajectory: ~21% of the box on
2026-08-05 → ~31% on 2026-08-11. Queue 002 D3 warns at 25% and refuses at 40%: without rotation,
normal reporting hits the refuse line within weeks. Rotation makes the box steady-state — the
current month's record hot on the bus, everything older archived, tracked, and findable.

## Deliverables
**D-1 · `scripts/rotate_reports.py`.** Scope: `exchange/reports/*.md` ONLY. Selects files whose
filename date (YYYY-MM-DD; fall back to first `git log` date if unparseable) is older than
**30 days [VETO]**. For each: sha256 → `git mv` to `docs/history/reports/YYYY-MM/<name>` → sha256
at destination must match → append one line (name, new path, sha256, date) to
`exchange/status/ROTATION_LOG.md`. **Moves only — the script contains no delete call of any
kind.** Exemptions, checked per file: any `NOTE_*_to_*` file listed as unacted inbox in the
newest DIGEST; anything under `exchange/status/`, `queue/`, or `DIGEST.md` (out of scope by
construction). `--dry-run` is the default; `--execute` required to move.
**D-2 · Cadence.** HERMES's box-budget section in the DIGEST lists rotation candidates (count +
bytes + % of box) each cycle — within his existing charter, no new instruction surface. The
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
