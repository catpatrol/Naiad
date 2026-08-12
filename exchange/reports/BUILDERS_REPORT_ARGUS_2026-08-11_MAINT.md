# BUILDERS' REPORT — ARGUS maintenance cycle, 2026-08-11

**Lane:** ARGUS (analytics). **Builder:** HEPHAESTUS.
**Contract:** small maintenance cycle under `NOTE_ATHENA_to_ARGUS_2026-08-11_DATA-RESIDENCY.md`.
**Branch:** `v12-v1-census`. **HEAD at start:** `04d05ab`.

**What this cycle changed:** one new test, one ledger entry, one document. **No analytics behaviour
changed. No published number moved.** `analytics/` was not touched — not a line — and the whole of
`scripts/`, `engine/`, `configs/`, `study/`, `briefs/`, `publish_exchange.py`, `reviewer_manifest.py`
and `backup_estate.py` were left alone as the contract required.

**Environment gate: PASSED.** Branch `v12-v1-census`; working directory
`C:\Users\luisf\OneDrive\Desktop\Midas-Claude Code Resources\naiad` (contains both `\Users\` and
`OneDrive`); `analytics/`, `tests/` and `exchange/` all present.

---

## 0. Data residency — why there is NO D: gate in this document

The 2026-08-11 residency note requires every contract that writes bulk data to write it **directly**
to `D:/Naiad/<repo-mirror-path>`, and to carry a reachability gate that HALTS if `D:` is absent
rather than silently falling back to the laptop.

**This cycle writes no bulk data, so no `D:` reachability gate applies, and none was run.** Saying
so explicitly rather than leaving it inferred: the three files this cycle touched are a Python test
module, a Markdown ledger and this Markdown report — exact sizes in §5. Nothing here is data-class,
nothing is a capture, render, results JSON, substrate, parquet or HTML, and nothing was written to
`D:` or needed to be. The rule is adopted and live for this lane — it simply had no work to do
today.

---

## 1. ITEM 1 — F-AN-15, the interface byte-identity fixture

### 1.1 What it is and why it exists

There are two copies of the same contract:

| copy | path | who reads it |
|---|---|---|
| **canonical** | `analytics/INTERFACE.md` | the code lane; this is the contract `analytics/` honours |
| **published** | `exchange/reports/INTERFACE_2026-08-06_C6.md` | **APOLLO** and every other web lane |

The web lanes reach repo content only through the context box, and the standing tick set is
`LEDGER.md` and `exchange/` **only** (CONVENTIONS §3.2). `analytics/INTERFACE.md` is therefore
unreachable to APOLLO — the `exchange/` copy is the only one it can open. The moment the two drift,
the census-facing lane is reading a contract this code no longer honours, **and nothing anywhere
says so.**

F-AN-15 is the thing that says so. It closes ATHENA's standing open want; the code is ARGUS's, so
closing it was ours to do.

**Location:** `tests/test_analytics.py`, `test_f_an_15_published_interface_is_byte_identical`.
It reads both files in **binary** (no newline translation) and compares sha256 over the raw bytes.

### 1.2 Current result — IDENTICAL

```
F-AN-15: IDENTICAL
  analytics/INTERFACE.md
      sha256 70c3f36894684442871f57c6435380fbcea9ca9e23680e356ce610f16f93c61e   48,885 B
  exchange/reports/INTERFACE_2026-08-06_C6.md
      sha256 70c3f36894684442871f57c6435380fbcea9ca9e23680e356ce610f16f93c61e   48,885 B
```

Both directions reported, as the contract asked: same hash, same byte count, canonical → published
and published → canonical. **The published contract APOLLO is reading is the contract this code
honours.** As of this cycle they have not drifted.

### 1.3 Three design decisions, and the reason for each

**It does NOT auto-copy on mismatch.** This was the contract's instruction and it is the right one.
An automated re-export would succeed every single time it ran, so the suite would go green for
exactly the staleness the fixture exists to catch — it would launder a stale publication into a
passing test. The fix is one deliberate copy, made by a human who has decided the canonical file is
ready to publish. The failure message names the command:

```
copy analytics\INTERFACE.md exchange\reports\INTERFACE_2026-08-06_C6.md
```

and offers the alternative of publishing under a fresh date, leaving the old snapshot as history.

**It SKIPS — it does not pass — when no published copy exists.** A missing mirror is an unanswered
question, not a satisfied assertion. The skip message says so in those words, and says that a
missing published copy means APOLLO has no contract to read at all.

**"Newest" is decided by the ISO date in the FILENAME, never by mtime.** git does not preserve
mtimes. A fresh clone would pick a different "newest" file than this working tree does, and a
fixture that compares different files on different machines is not a fixture. There is also an
explicit non-empty guard: two empty files hash alike, and that comparison would pass while saying
nothing.

### 1.4 THE MUTATION DEMONSTRATION — proof it can fail

This lane has now shipped one fixture that **could not fail** (`stoch_rsi` all-NaN, satisfying
`NaN == NaN` at every truncation point) and one fixture family that was **vacuous against sabotaged
code**. A fixture is not trusted here because it passes. It is trusted because it has been watched
to fail. Three runs, in order:

**Run A — one byte changed, file length unchanged → FAILED, correctly.**
The published copy was backed up bytewise, then the single byte at offset 20,000 was changed from
`' '` (0x20) to `'X'`. Length stayed at 48,885 B, so a size-only check would have missed it
entirely. F-AN-15 caught it:

```
E   AssertionError: PUBLISHED CONTRACT IS STALE -- the two copies are NOT identical.
E     canonical  analytics/INTERFACE.md
E                sha256 70c3f36894684442871f57c6435380fbcea9ca9e23680e356ce610f16f93c61e
E                bytes  48885
E     published  exchange/reports/INTERFACE_2026-08-06_C6.md
E                sha256 02937680f64339459711d02a24b8638cb5980686e0743e7634bfce120cc04ce0
E                bytes  48885
E     delta      published - canonical = +0 bytes; first differing byte at offset 20000
E
E     APOLLO is reading the published copy. It no longer matches the code.
E
E     THIS FIXTURE WILL NOT FIX IT FOR YOU. ...
E         copy analytics\INTERFACE.md exchange\reports\INTERFACE_2026-08-06_C6.md
=========================== short test summary info ===========================
FAILED tests/test_analytics.py::test_f_an_15_published_interface_is_byte_identical
```

Note what the failure reports without being asked: both hashes, both byte counts, the signed byte
delta, and the exact offset of the first difference.

**Run B — published copy removed entirely → SKIPPED, not passed.**

```
SKIPPED [1] tests\test_analytics.py:1092: SKIPPED, NOT PASSED: no
exchange/reports/INTERFACE_<date>*.md exists, so there is no published copy to compare
against. This is not a green result -- the census-facing lanes (APOLLO) have no contract to
read at all. Publish one with:
    copy analytics\INTERFACE.md exchange\reports\INTERFACE_<YYYY-MM-DD>_C6.md
```

pytest reported `s`, not `.`. The vacuous-pass path is closed.

**Run C — restored → PASSED, and the restore was sha-verified.**

```
restored INTERFACE_2026-08-06_C6.md  sha256 70c3f368...f6f93c61e  48885 B
RESTORE VERIFIED: True
```

The published copy is byte-for-byte what it was before the demonstration — confirmed both by sha256
against the pre-mutation backup and by `git status`, which reports
`exchange/reports/INTERFACE_2026-08-06_C6.md` as **unmodified**. The mutation script and the backup
live in the session scratchpad, outside the repo, and are not committed.

### 1.5 Suite state

**287 passed, 1 skipped** (`pytest` with the configured `testpaths = fixtures tests`), up from the
286 passed / 1 skipped baseline by exactly the one test added here. The single skip is pre-existing
and unrelated: `fixtures/test_f8_journal.py:110`, "dry-run journal not generated yet (D7)".

---

## 2. ITEM 2 — LEDGER_ARGUS acknowledgement, appended

The acknowledgement was appended **verbatim** to `exchange/status/LEDGER_ARGUS.md`, unedited.

| | bytes | sha256 |
|---|---|---|
| before | 3,894 | `362220e0…` (12-char prefix; the full prior hash is not this document's to pin) |
| appended | 3,771 | — |
| after | 7,665 | `2bc7a95290a16dc836d525a9cab0f0fda11e69c13b4124d765a7c79c599ef6c2` |

**Append-only verified mechanically, not assumed:** the post-append bytes were asserted to *start
with* the complete pre-append bytes. Not one prior byte changed. Line endings are LF throughout, as
the file already was — zero CR bytes before, zero after.

The entry carries nine bullets. One is a **⚠ RAISED TO ATHENA** item and is the live open question
out of this cycle; see §4.

---

## 3. Findings reported, NOT fixed

**`pytest.ini` now carries a stale comment.** Its explanatory comment reads "the whole F-AN-1..14
regression guard" and "adds exactly 41 items". With F-AN-15 the suite is F-AN-1..15 and
`tests/test_analytics.py` collects 42 items. **The comment is stale; the configuration is correct
and nothing is broken by it** — `testpaths = fixtures tests` still collects the new test, which is
how it was run above. `pytest.ini` sits outside this cycle's authorized set, so it was not edited.
One-line fix for whoever holds that file next.

**The ledger's own LANE STATE line says "suite 286 passed / 1 skipped".** That was true when the
contract text was written and is now 287 / 1 because of this cycle. The contract required the entry
**verbatim**, so it was appended verbatim rather than silently corrected. The ledger is append-only:
a correction is a new entry, never an edit. Flagging it here so the next ARGUS entry can carry the
current figure.

**The publish commit will carry other lanes' pending `exchange/` files.** `publish_exchange.py`
stages all of `exchange/**`, and at the time of this run the tree also held untracked HERMES and
ATHENA files plus a modified `exchange/DIGEST.md`. That is the script's designed behaviour, not a
defect, but it means the publish commit below is not exclusively this lane's work. Listed in §5 so
the record is not misleading.

---

## 4. Open, with owners

1. **⚠ ROTATION CONFLICT — owner: ATHENA, decision required.** Queue 003 rotates bus reports older
   than 30 days into `docs/history/reports/YYYY-MM/`, exempting only `NOTE_*_to_*` files.
   `INTERFACE_2026-08-06_C6.md` is neither a note nor a report — it is the **living census-facing
   contract APOLLO cites**, and the only copy a web lane can reach. Under the current rule it leaves
   APOLLO's reading surface on **2026-09-05**. ARGUS proposes relocating it to `exchange/status/`,
   which does not rotate and already holds `LEDGER_ARGUS.md`. Fallback: drop the date from the
   filename and exempt undated files from rotation. **ATHENA rules.**
   *Note the interaction with F-AN-15:* if the file is relocated out of `exchange/reports/`, F-AN-15
   will SKIP rather than fail — loudly, with a message saying no published copy exists. It will not
   pass vacuously. Whoever executes the relocation should widen the fixture's search path in the
   same change.
2. **`pytest.ini` comment refresh** — owner: whoever next holds that file. Cosmetic.
3. **Residency refinement for `briefs/panel/**/*.parquet`** — owner: ARGUS, not urgent. Recorded in
   the ledger entry: those partitions are 100% regenerable from the captures via `brief_panel.py`,
   making them the free candidate for `D:` when archive volume justifies a contract. Captures are
   the record and stay tracked.

---

## 5. File disposition

Box = **6,390,000 B** (the ~6.39 MB context box). The standing tick set is `LEDGER.md` and
`exchange/` **only**, so files outside `exchange/` cost the box nothing and are marked `n/a` with
their location named.

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `tests/test_analytics.py` | yes | tracked (modified: 48,745 → 53,866 B, +5,121) | `d93bba1` | yes — `origin/v12-v1-census` | GitHub + estate zip | **n/a** — `tests/` is outside the tick set (`LEDGER.md` and `exchange/` only), so it never enters the box |
| `exchange/status/LEDGER_ARGUS.md` | yes | tracked (appended: 3,894 → 7,665 B, +3,771) | `45775d2` | yes — `origin/v12-v1-census` | GitHub + estate zip | 7,665 B — **0.12%** |
| `exchange/reports/BUILDERS_REPORT_ARGUS_2026-08-11_MAINT.md` | yes | tracked (new) | draft in `45775d2`; **this final text in the follow-up publish commit** (see §6 — a document cannot name the commit that carries it) | yes — `origin/v12-v1-census` | GitHub + estate zip | 16,401 B — **0.26%** |

**Nothing here is over the ~1% flag threshold.** The two `exchange/` files together add **24,066 B,
0.38% of the box** — the largest single artifact is this document at well under a tenth of the
threshold. DOCUMENTS ARE CHEAP, DATA IS NOT: this cycle produced no data.

Files created outside the repo and deliberately **not** committed: the mutation script and the
pre-mutation backup of `INTERFACE_2026-08-06_C6.md`, both in the session scratchpad under
`%LOCALAPPDATA%\Temp\claude\...\scratchpad`. They are demonstration scaffolding, not artifacts.
**NOT PROTECTED**, and intentionally so.

---

## 6. Publish

`scripts/publish_exchange.py` has **no `__main__` block** — it is a library, and its documented
callers (`scripts/daily_routine.py:1048`, `scripts/backup_estate.py:943`) invoke
`publish_exchange.publish(ROOT, date)`. Running the file directly is a silent no-op, which is worth
knowing before anyone reports a publish that never happened. It was driven the documented way, from
a scratchpad driver; **`publish_exchange.py` itself was not modified.**

```
publish: committed 45775d2 (7 path(s)) and pushed to origin/v12-v1-census

- committed `45775d2` on `v12-v1-census` and pushed to origin
- 7 path(s) published, all inside `exchange/`
- `exchange/` size budget: 1,777,190 B, 27.8% of 6,390,000 B (WARN)
```

**Push: SUCCEEDED.** Verified against the actual remote, not just the local tracking ref —
`git ls-remote origin v12-v1-census` returns `45775d2a521f1bd9d06e69e1097c3106b3eb2e28`, matching
local `HEAD`. The earlier commit `d93bba1` (the F-AN-15 fixture) is an ancestor and went up with it.

### ⚠ THE SIZE BUDGET IS AT **WARN**

**1,777,190 B — 27.8% of the 6,390,000 B box.** Thresholds are WARN at ≥ 25%, REFUSE above 40%. The
publish proceeded and was not blocked, but `exchange/` has crossed the warning line and there is
about **12 percentage points of headroom left**. This is not caused by this cycle: the two files
added here are 0.4% of the box between them. It is the standing level of `exchange/`, now 101 files.
Recorded here so the next lane to add something large sees the number before it does, not after.

**The seven paths published were not all ARGUS's.** `publish_exchange.py` stages all of
`exchange/**`, so this commit also carried a modified `exchange/DIGEST.md` and four pending files
from the HERMES and ATHENA lanes that were sitting untracked in the tree. Designed behaviour, listed
in §3 and again here so the commit is not misread as one lane's work.

**Two publishes, and why.** The commit above was made while §5 and §6 of this document still held
placeholders, because the commit SHA and the budget line do not exist until the publish runs. This
final text was carried by a second publish immediately after. That second commit's SHA is
necessarily absent from the file it commits — the same reason a file never contains its own sha256.
It is reported to the operator on screen.

---

## 7. Honest summary for the operator

Two small things were asked for and both are done. The interface fixture now exists and has been
watched to fail before being trusted to pass — a one-byte change to the published contract, with the
file length left identical, was caught and reported with the exact offset. The two copies of the
contract are currently byte-identical, so APOLLO is reading the right thing today. The ledger has a
current entry for the first time in nine days, appended without touching a byte of what came before.

The one thing that needs a decision from someone other than this lane: the census-facing contract
`INTERFACE_2026-08-06_C6.md` is scheduled to rotate off APOLLO's reading surface on 2026-09-05 by a
rule that was never written with it in mind. ATHENA rules on where it should live. Until then it
stays where it is and F-AN-15 watches it.

*ARGUS lane, built by HEPHAESTUS, 2026-08-11.*
