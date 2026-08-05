# 002 · Off-machine phase archives, a publish size budget, and manifest retention

RATIFIED: operator, 2026-08-04, rulings G1-a / G5-a. Drafted: ATHENA. Executor: HEPHAESTUS.

## Why this exists
Three defects, all measured, none guessed:
1. `backup_estate.py:1030` sets `dest = REPO / "research_outputs" / "_archive"` unconditionally.
   `run_phase` never reads `args.dest`. **`--phase` cannot write off-machine.** Every phase archive
   so far reached Drive because a human ran a paste.
2. `--dest` is defined on the top-level parser, so `--phase X --dest "G:/..."` **parses cleanly,
   exits 0, prints success, and writes only inside the repo.** `--estate`/`--workflow` hard-fail via
   `ap.error()` when `--dest` is missing; `--phase` is the one mode where the flag lies.
3. `publish_exchange.py` has no size guard at all — its only check is path scope, so the
   `offenders= []` printed on every run means "nothing outside `exchange/`", never anything about
   size. `exchange/` reached **51.4% of the project box** while **nine of its ten data files were
   individually under the 1 MB cap.** A per-file limit would not have caught it.

## Deliverables
**D1 · `--mirror DIR` for `--phase`.** After F-K5 passes, copy archive AND sidecar to `DIR`, then
verify by re-reading FROM `DIR` — never by re-hashing the source. No-clobber: refuse an existing
destination file rather than overwrite. In-repo behaviour, F-K3's output exclusion and
`--delete-source` semantics all stay exactly as they are.
**D2 · `--phase --dest` becomes an error.** `ap.error()` with a message naming `--mirror`.
**D3 · Total-size budget in `publish_exchange.py`.** Compute tracked bytes under `exchange/` after
staging. WARN at 25% of 6,390,000 B; REFUSE above 40%, printing the ten largest files with their
percentages and quoting §4.2's pointer rule. Refusal must be overridable by an explicit flag so it
never becomes an unbypassable block on legitimate work.
**D4 REDUCED TO A FIXTURE — operator ruling 2026-08-04.** The executor of this contract read the retention code before it was filed and found it **ALREADY IMPLEMENTED**; nothing has aged out yet, which is why the observed MANIFEST duplication is not a retention failure. **Do not rebuild it.** Deliver only fixture F-R1 below as confirmation that the existing behaviour reports and never deletes. The original D4 text is retained beneath for provenance and is NOT a work item.

~~**D4 · Manifest retention.**~~ Keep the newest 7 `exchange/status/daily/` artifacts; older ones are
REPORTED, never auto-deleted — the same posture as the estate/workflow rule. Implement wherever the
existing writer lives; read it first, do not assume.

> ### PRE-EXECUTION FINDING on D4 — recorded by HEPHAESTUS, 2026-08-04, before any code was written
>
> **D4 is already implemented. Do not build it.** D4 says "read it first, do not assume"; this is
> the result of that reading, filed here so the 002 session does not rebuild working code.
>
> - `scripts/routine_jobs.json:8` already sets **`"keep_daily": 7`** — exactly the number D4 asks
>   for — with `"daily_archive_dir": "research_outputs/_daily_archive"`.
> - `scripts/daily_routine.py:632` `apply_rolling_window(out_dir, archive_dir, keep)` keeps the
>   newest `keep` of **both** `DAILY_*.md` and `MANIFEST_*.json` and **MOVES** the rest to the
>   archive dir. Its docstring states the intent directly: *"MOVED, never deleted… not to lose the
>   history."* It sorts lexically on the ISO date in the filename rather than trusting filesystem
>   timestamps, dedups by sha256 when an identical copy is already archived, renames on collision
>   rather than overwriting, and records per-file errors without aborting the run.
> - `daily_routine.py:1026` reads `keep = reg.get("keep_daily", 7)` — 7 is also the code default.
>
> **One real difference from D4's letter, and it is the safer behaviour:** D4 asks for aged-out
> files to be *reported, never auto-deleted*. The existing code *moves* them out of `exchange/`
> into `research_outputs/_daily_archive` — off the sync bus, still on disk, still readable. The one
> `unlink()` on line 665 fires only when a **byte-identical copy already exists** in the archive
> (sha256-verified), which is deduplication, not loss.
>
> **Current state:** `exchange/status/daily/` holds 3 `DAILY_*.md` and 3 `MANIFEST_*.json` — 6 files
> against a window of 7 each, so **the window has never fired.** Nothing has aged out yet.
>
> **Recommended disposition:** close D4 as ALREADY SATISFIED, or reduce it to a one-line
> confirmation fixture (F-R1 below already serves as that). **Operator ruling required before the
> 002 session treats D4 as work.** D1, D2 and D3 are unaffected by this finding and stand as written.

## Fixtures — HALT loudly on any failure
- **F-M1** `--phase` with `--mirror` writes to both destinations; the mirrored bytes re-read from
  the mirror hash equal to the source.
- **F-M2** `--mirror` refuses an existing destination file and exits non-zero without writing.
- **F-M3** `--phase --dest X` exits non-zero with a message naming `--mirror`.
- **F-M4** `--phase` with no `--mirror` behaves byte-identically to today (regression guard).
- **F-P1** a staged set under the warn threshold publishes normally.
- **F-P2** a staged set over the refuse threshold is refused, and names the ten largest files.
- **F-P3** the override flag permits the refused publish and says so on screen.
- **F-P4** existing path-scope behaviour is unchanged — the `exchangeable/` lookalike is still
  rejected.
- **F-R1** with 9 daily artifacts present, exactly 2 are reported as outside the rule and **0 files
  are deleted**.
- **F-REG** the full existing suite still passes.

## Invariants
Nothing under `research_outputs/` is deleted. Nothing writes to `_reviewer_box/`. Commit-no-push
except `exchange/**` via the guard. `signals.py`, `trading.py` and the engine are untouched.

## What this phase is NOT
Not a change to what gets archived, when, or to retention *policy* — phase archives remain permanent
and never prunable. Not a change to estate or workflow modes. Not a placement decision for any other
lane's files.

## Deliverable document
ONE build document per `CONVENTIONS.md` §3.1, carrying the full fixture transcript and the
six-column disposition table.
