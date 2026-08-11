# BUILDERS REPORT — HEPHAESTUS — 2026-08-11 — QUEUE 003 RATIFIED

**Lane:** HEPHAESTUS · **Date:** 2026-08-11 · **Branch:** `v12-v1-census` · **Head at start:** `b729cb8`
**Scope:** `exchange/queue/003_report-rotation-and-provenance.md` ONLY. This paste stamps; it builds
nothing. No script written, no `CONVENTIONS.md` edit, nothing rotated, nothing moved, nothing deleted.

**Operator instruction, 2026-08-11:** *"if everything in order ratify 003."* Conditional. The filing
report's two open findings were the only things not in order; both are resolved in the stamp below, so
the condition is met and the stamp carries the operator's authority. What "in order" was taken to mean
is stated plainly in §4 so it can be overruled if that reading is wrong.

---

## 1 · Anchor context, printed BEFORE any write

D-4's rule, applied to the paste that files D-4. All three blocks were printed before a single byte
reached disk.

**Anchor 1 — stamp line (1 hit):**
```
      1| # 003 · Report rotation, rerun provenance, and the anchor-context rule
      2|
 >    3| RATIFIED: **PENDING** — operator ratifies with one word. Drafted: ATHENA, 2026-08-11.
      4| Executor: HEPHAESTUS. Runs AFTER queue 002 (D-1's box arithmetic assumes 002's D3 guard exists;
      5| if 002 is unbuilt, build it first and say so).
      6|
```

**Anchor 2 — threshold (1 hit):**
```
     14| ## Deliverables
     15| **D-1 · `scripts/rotate_reports.py`.** Scope: `exchange/reports/*.md` ONLY. Selects files whose
     16| filename date (YYYY-MM-DD; fall back to first `git log` date if unparseable) is older than
 >   17| **30 days [VETO]**. For each: sha256 → `git mv` to `docs/history/reports/YYYY-MM/<name>` → sha256
     18| at destination must match → append one line (name, new path, sha256, date) to
     19| `exchange/status/ROTATION_LOG.md`. **Moves only — the script contains no delete call of any
     20| kind.** Exemptions, checked per file: any `NOTE_*_to_*` file listed as unacted inbox in the
```

**Anchor 3 — figures (1 hit):**
```
      6|
      7| ## Why this exists
      8| `exchange/` is ticked into the ~6.39 MB project box and grows with every session by design (one
 >    9| build document each, no exceptions — CONVENTIONS §3.1). Measured trajectory: ~21% of the box on
     10| 2026-08-05 → ~31% on 2026-08-11. Queue 002 D3 warns at 25% and refuses at 40%: without rotation,
     11| normal reporting hits the refuse line within weeks. Rotation makes the box steady-state — the
     12| current month's record hot on the bus, everything older archived, tracked, and findable.
```

**D-4 earned its keep on its own filing paste.** Anchors 1 and 3 are hard-wrapped sentences spanning
two lines. Printing the context is what made that visible — and it is exactly what the line-oriented
edit that followed could not handle. See §2.

---

## 2 · Two defects in the paste, and one console failure

### 2.1 · The figures edit silently did nothing while reporting success

The paste splits the file into lines, then calls `.replace()` on a **single line** with a search string
that spans a **line break**:

```python
lines[h[0]].replace('~21% of the box on 2026-08-05 → ~31% on 2026-08-11', ...)
```

Line 9 ends at `~21% of the box on`; the rest lives on line 10. The replace matched nothing, returned
the line unchanged — and `edits += 1` incremented regardless, printing `OK figures corrected`. The
run reported **3/3 edits applied** with the old figures still in the file.

This is the same defect class this project has now hit three times: **a guard that counts instead of
verifying.** The occurrence-count check (`len(h) == 1`) confirmed the anchor existed and proved nothing
about whether the edit took. The fix is a post-write assertion, which §3 now carries.

### 2.2 · The stamp edit orphaned its continuation line

Replacing line 3 wholesale — with a string that itself contains `Executor: HEPHAESTUS.` — left line 4's
`Executor: HEPHAESTUS. Runs AFTER queue 002 (…` in place. Result: the phrase twice, and a dangling
half-sentence from the original.

**Recovery:** `git checkout -- exchange/queue/003_…md` restored the file to its committed state
(confirmed clean), and all three edits were re-applied against the **full multi-line spans**, preserving
the "Runs AFTER queue 002" sentence intact on its own line.

### 2.3 · The context print crashed on a UTF-8 arrow

The first run died with `UnicodeEncodeError: 'charmap' codec can't encode '→'` while printing
anchor 2 — the Windows console is cp1252 and line 17 contains `→`. **The crash landed inside `ctx()`,
before the single write at the end of the script, so nothing was written**; verified with
`git diff --quiet` before proceeding. Re-run under `PYTHONIOENCODING=utf-8`, which is also why the
context blocks in §1 are legible rather than full of replacement characters.

Worth noting for future pastes: this file's own §7 in the 002 report already flagged cp1252 mangling
`§` in transcripts. There it was cosmetic. Here it was fatal, because a print of file content sits on
the path to the write.

---

## 3 · The three edits, verified after writing

| # | finding | edit | verified |
|---|---|---|---|
| 1 | — | `RATIFIED: **PENDING**` → `RATIFIED: **operator, 2026-08-11**`, naming the instruction and the report it resolves | stamp present ✔ · `**PENDING**` absent ✔ · `Executor: HEPHAESTUS` appears exactly once ✔ |
| 2 | 3.1 | `**30 days [VETO]**` → `**30 days**` + PINNED note recording that the marker was finding 3.1 and the drafted default stands | pin text present ✔ · no bare `[VETO]` left ✔ |
| 3 | 3.2 | drafter's `~21%/~31%` → measured `17.9%/26.2%`, **plus the reason** | new figures present ✔ · `~21% of the box on` absent ✔ |

```
  PASS  stamp applied          PASS  threshold pinned      PASS  figures corrected
  PASS  PENDING gone           PASS  [VETO] marker gone    PASS  old figures gone
  PASS  no duplicate Executor
  bytes=5374  CRLF=0 LF=73     (line endings preserved: LF)
```

Diff: **15 insertions, 7 deletions**, one file, `exchange/queue/` only.

### 3.1 · The paste's explanation for finding 3.2 was checked, not assumed

The paste asserts the drafter's numbers "were whole-box readings mis-stated as `exchange/`-only." That
is a causal claim going into a ratified contract, so it was tested against git before being written:

| hypothesis | 2026-08-05 | 2026-08-11 |
|---|---|---|
| `exchange/` tracked only | 1,146,621 B — **17.9%** | 1,687,792 B — **26.4%** |
| **`exchange/` + `LEDGER.md` (the tick set)** | 1,401,632 B — **21.9%** | 1,942,803 B — **30.4%** |
| `exchange/` + `docs/` | 103.6% | 113.0% |
| whole repo tracked | 491.1% | 500.8% |

**Confirmed exactly.** The tick set reads 21.9% and 30.4%, which round to the drafter's ~21% and ~31%.
The figures were never sloppy — they measured the right thing under the wrong label. The contract now
carries both numbers and says which is which, because both are true and they answer different
questions.

**A finding that falls out of this, for a future queue item, not fixed here:** 002's D3 guard meters
`exchange/` **only** against the 6.39 MB box, so it under-reports true box occupancy by ~4 points —
the box is at 30.4% while the guard says 26.4%. D3 will refuse when `exchange/` alone hits 40%, by
which point the actual box is nearer 44%. Out of scope for this paste, which touches one queue file.

---

## 4 · What "in order" was taken to mean

The instruction was conditional. Recorded so the reading is auditable:

- the contract's five standard fields were confirmed present at filing (`…QUEUE-003-FILED.md` §1);
- its ordering precondition is satisfied — **queue 002 executed 2026-08-11, ACCEPT, 10/10 fixtures**,
  code at `c32ffa5`, so D3's guard exists and 003 need not build it;
- the two findings that filing raised are the two things resolved above, both by applying the
  drafter's own defaults rather than by substituting the builder's judgement: the 30-day constant
  **stands as drafted**, and the trajectory sentence gains the measurement plus the reason.

Nothing else was judged. If the operator's "in order" was meant to include something outside those
three, the stamp is one `git checkout` from reversal.

---

## 5 · Disposition table

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `exchange/queue/003_report-rotation-and-provenance.md` | yes | tracked | `8ce3b11` | yes — `origin/v12-v1-census` | GitHub + estate zip | 5,374 B (0.080% of box); **+734 B** from the stamp |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-11_QUEUE-003-RATIFIED.md` | yes | tracked (new) | `ec53796` | yes — `origin/v12-v1-census` | GitHub + estate zip | 10,438 B (0.156% of box) |
| `exchange/status/CONVENTIONS.md` | yes | tracked, **unchanged** | unchanged | unchanged | GitHub + estate zip | 0 — D-3/D-4 are 003's work, not this paste's |
| `scripts/rotate_reports.py` | **no** | — | — | — | — | 0 — D-1 not built here |
| `exchange/status/ROTATION_LOG.md` | **no** | — | — | — | — | 0 — created by D-1 |
| `exchange/reports/**` (existing) | yes | tracked | unchanged | unchanged | GitHub + estate zip | **0 — nothing rotated** |

---

## 6 · Publish

```
publish: WARNING -- exchange/ holds 1,688,526 B, 26.4% of the 6,390,000 B box
         (warn at 25%, refuse above 40%).
publish: committed 8ce3b11 (1 path(s)) and pushed to origin/v12-v1-census
status= PUBLISHED commit= 8ce3b11 pushed= True offenders= []
bytes= 1688526 fraction=26.4% budget= WARN
```

The D3 budget line is the guard 002 delivered, metering the ratification of the contract written to
bring that number back down.

This report itself published as `ec53796`, taking `exchange/` to **1,698,964 B / 26.6%** — still WARN.
A third commit carries these two lines, for the usual reason that a document cannot contain its own
SHA. Session chain: `b729cb8` → `8ce3b11` (stamp) → `ec53796` (this report) → this correction.

---

## 7 · Status

**003 is ratified and buildable.** It was not begun here and must not be — it runs as its own session
on the operator's "build 003", per its own deliverable-document clause and the standing rule that a
ratified contract gets its own build.

Order of work when that session opens: D-1 + D-2 ship together; D-3 and D-4 may ship independently.
D-4 — the anchor-context rule — is the one this session would have most liked to already exist.

---

## 8 · Rollback

`git checkout -- exchange/queue/` restores 003 to its unstamped state at `b729cb8`. Nothing else was
written: no script, no `CONVENTIONS.md` edit, no file moved, no file deleted.
