# BUILDERS REPORT — HEPHAESTUS — 2026-08-11 — QUEUE 003 FILED

**Lane:** HEPHAESTUS · **Date:** 2026-08-11 · **Branch:** `v12-v1-census` · **Head at start:** `684f7ec`
**Scope of this session:** file the contract. **No rotation ran, no script was built, `CONVENTIONS.md`
was not edited.** One file written: `exchange/queue/003_report-rotation-and-provenance.md`, 4,640 B,
LF-only, no-clobber gate confirmed 003 absent beforehand.

---

## 1 · The five standard fields, confirmed present

| field | present | value |
|---|---|---|
| stamp | yes | `RATIFIED: **PENDING** — operator ratifies with one word.` Drafted ATHENA 2026-08-11, executor HEPHAESTUS |
| deliverables | yes | D-1 `scripts/rotate_reports.py` · D-2 cadence via HERMES's DIGEST section · D-3 R3 refinement in §4 · D-4 anchor-context rule in §2.3 |
| fixtures | yes | F-303-1 … F-303-7 plus F-REG |
| verdict criteria | yes | ACCEPT conditions enumerated; `D-1+D-2` ship together, `D-3`/`D-4` independent |
| scope boundary | yes | "What this phase is NOT" — not deletion, not `publish_exchange.py`/`backup_estate.py`, not LEDGER/CONVENTIONS/queue/DIGEST rotation, not automation |

**Worth recording:** 002 shipped *without* verdict criteria and had to have them retrofitted on
2026-08-06 by its drafter. 003 carries them from the moment it was filed. The defect did not recur.

---

## 2 · Queue 002 status — stated plainly, because it gates 003's order

**002 has executed.** It ran earlier today as its own session and was accepted.

| | |
|---|---|
| contract | `exchange/queue/002_backup-and-publish-guards.md`, ratified operator 2026-08-04 (G1-a/G5-a), amended 2026-08-06 ruling B |
| executed | 2026-08-11, this machine, its own session |
| verdict | **ACCEPT** — 10/10 fixtures (F-M1..M4, F-P1..P4, F-R1, F-REG 213 passed) |
| code commit | `c32ffa5` — `scripts/backup_estate.py`, `scripts/publish_exchange.py` |
| build document | `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-11_QUEUE-002.md` |

So 003's ordering precondition is **satisfied**: D3's size guard exists, and 003 need not build it
first. The guard is live — it warned on this session's own publish, which is how the percentages in
§3 below were produced.

---

## 3 · Two findings on the filed contract

Neither was corrected in the file. 003 is PENDING ratification and the text is its drafter's; a
builder editing a contract's substance before the operator has ratified it would be the same defect
in the other direction. Both are raised here for the ratification pass.

### 3.1 · An unresolved `[VETO]` marker ships inside D-1

Line 17 of the contract reads:

```
filename date (YYYY-MM-DD; fall back to first `git log` date if unparseable) is older than
**30 days [VETO]**. For each: sha256 → `git mv` to `docs/history/reports/YYYY-MM/<name>` → sha256
```

`[VETO]` sits on the one number that decides what D-1 moves. It reads as an editorial marker — either
a threshold the drafter flagged for the operator to overrule, or a token that should not have shipped.
It is the difference between rotating everything older than a month and rotating nothing, so it cannot
be left to the executor's reading. **Resolve at ratification.**

### 3.2 · The box-trajectory figures are overstated; the conclusion survives

The contract's "Why this exists" cites **~21% on 2026-08-05 → ~31% on 2026-08-11**. Measured from git,
summing tracked blob sizes under `exchange/` at each commit against the 6,390,000 B box:

| date | commit | tracked bytes | % of box | files | contract said |
|---|---|---|---|---|---|
| 2026-08-05 | `d223801` | 1,146,621 | **17.9%** | 76 | ~21% |
| 2026-08-11 | `684f7ec` | 1,676,490 | **26.2%** | 90 | ~31% |

Both endpoints are high by 3–5 points. **The argument does not depend on them.** `exchange/` grew
**+8.3 points in six days**, which reaches the 40% refuse line in roughly ten more days of comparable
activity — sooner than the contract's own "within weeks". Corrected numbers make the case for D-1
stronger, not weaker. The 2026-08-05 and 2026-08-06 rows resolve to the same commit; there were no
commits between those dates.

*(Measurement is `git ls-tree -r -l` per commit, so it counts committed blob bytes — the same quantity
002's D3 guard measures from the index.)*

---

## 4 · File-disposition table

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `exchange/queue/003_report-rotation-and-provenance.md` | yes | tracked (new) | `e1c4e2d` | yes — `origin/v12-v1-census` | GitHub + estate zip | 4,640 B (0.073% of the 6.39 MB box) |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-11_QUEUE-003-FILED.md` | yes | tracked (new) | `e1c4e2d`, §5 follows | yes — `origin/v12-v1-census` | GitHub + estate zip | 5,739 B (0.086% of box) |
| `exchange/status/CONVENTIONS.md` | yes | tracked, **unchanged** | unchanged | unchanged | GitHub + estate zip | 0 — this paste edits nothing |
| `scripts/rotate_reports.py` | **no** | — | — | — | — | 0 — D-1 is not built here |
| `exchange/status/ROTATION_LOG.md` | **no** | — | — | — | — | 0 — created by D-1, not by this paste |
| `exchange/reports/**` (existing) | yes | tracked | unchanged | unchanged | GitHub + estate zip | **0 — nothing rotated, nothing moved** |

Both new files are prose. No data artifact entered `exchange/`. Combined box cost is well under the
1%-of-budget flag threshold, and the filing adds ~0.15 points to a bus already at 26.2% — which is
itself the reason 003 exists.

---

## 5 · Publish

```
publish: WARNING -- exchange/ holds 1,686,869 B, 26.4% of the 6,390,000 B box
         (warn at 25%, refuse above 40%).
publish: committed e1c4e2d (2 path(s)) and pushed to origin/v12-v1-census
status= PUBLISHED commit= e1c4e2d pushed= True offenders= []
bytes= 1686869 fraction=26.4% budget= WARN
```

Verified, not assumed:

| check | result |
|---|---|
| files in `e1c4e2d` | 2 — the 003 contract (+65), this report (+110) |
| paths outside `exchange/` | **none** |
| local vs `origin/v12-v1-census` | both `e1c4e2d` |
| 003 contract present on the remote | yes (`git cat-file -e`) |

**The D3 guard from 002 warned on the act of filing 003** — the contract that exists to stop that
number rising was itself measured by the guard 002 delivered, at 26.4%. Filing cost 0.2 points.

Box cost, final: contract 4,640 B (0.073%), this report 5,739 B (0.086%). A second commit carries §5.

---

## 6 · Rollback

`git checkout -- exchange/queue/` restores the queue to `684f7ec`. Nothing else was written: no
script, no `CONVENTIONS.md` edit, no file moved, no file deleted.
