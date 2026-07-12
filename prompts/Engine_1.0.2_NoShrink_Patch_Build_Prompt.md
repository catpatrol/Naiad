# BUILD PROMPT — Engine 1.0.2 "Cache No-Shrink Invariant" (hotfix phase)
### Feed this file to Claude Code. It is a self-contained contract. · 2026-07-10
### Builder: Claude Code · Reviewer: Claude (Project, Fable-mode) · Operator: Ludwig
### Closes: v12 V1 census packet open item #3. Does NOT close V1 itself.
### Amended same day: fixture-count expectations made relative to the
### pre-patch suite; V-A and V-B recorded as operator-confirmed.

---

## 0. Mission

Make "a kline or funding cache file never loses rows through the save path" a
**structural, fixture-enforced engine invariant** — the data-side twin of the
stop ratchet. Implement the reviewed two-hunk fix to `engine/data.py`
(merge-in-save + atomic replace + loud load failures), mirror it onto the
funding writer, add fixtures N1–N5 to the engine suite, bump the engine to
1.0.2, and append the incident entry to LEDGER.md.

Definition of done: the full fixture suite is green (all 26 existing + N1–N5),
the diff touches only what §4 permits, the changelog and ledger entries are
committed, and the packet lets the reviewer confirm all of it from raw bytes.

## 1. Read these before writing any code

1. `CACHE_TRUNCATION_HANDOFF.md` — the investigation and the reviewed diff.
   The diff in its §4 is the approved design; this contract adds the
   amendments from review (loud-load coverage, atomicity fixture, funding
   mirror, no-delete documentation, corrected cost note).
2. `engine/data.py` as it exists at the branch head — confirm the quoted
   patterns (`if path.exists(): …`, `frames = [cache] if len(cache) else []`,
   in-place `to_parquet`) are present as described. If the real code differs
   from the handoff's quotes, STOP and report the diff before patching.
3. `LEDGER.md` — for the append in D5.

## 2. Context the builder must honor

- Incident of record: on 2026-07-10, `parity_pack.py --backfill` stamped the
  494-day parity window [2025-03-01, 2026-07-08) over the full-history
  BTCUSDT 5m and 1h caches. Attribution recomputed and verified by the
  reviewer. The estate was already repaired by the census; **no cache file
  needs data changes in this phase.**
- Fixture suite is hermetic via `NAIAD_CACHE_DIR`; all new fixtures use it.
  The real cache is never touched by tests.
- This is infrastructure, not strategy: no signal logic, no rule, no
  parameter changes. Both consumers (Naiad paper line and v12 Study) inherit
  the fix.

## 3. Frozen invariants

- **I1 — No shrink.** After this patch, no call to `_save_cache` (klines) or
  the funding save path can produce a file whose row set is missing any
  `open_time` (or funding timestamp) that was durably on disk when the save
  began. New rows win at identical timestamps (`keep="last"` semantics
  preserved).
- **I2 — Loud failure.** "File absent" is the only condition that yields an
  empty cache on load (`FileNotFoundError`). Any other read failure —
  corrupt file, transient stat/sharing error — raises and aborts the run.
  Silent-empty is abolished on both the load path and the merge-read inside
  the save path.
- **I3 — Atomic persistence.** Every cache write goes to a same-directory
  temp file (pid-suffixed) and lands via `os.replace`. An interrupted run
  cannot leave a truncated or corrupt destination file.
- **I4 — Minimal blast radius.** The code diff is confined to the cache
  load/save functions for klines and funding. `backfill_klines`'s
  `frames = [cache] if len(cache) else []` line is left unchanged (harmless
  once I1 holds). No changes to `replay.py`, `parity_pack.py`, `tick.py`,
  fetch logic, or any script.
- **I5 — No deletion primitive.** This patch deliberately removes the ability
  to shrink a file via the save path, for every caller including
  `census.py --repair`. Row *removal*, should it ever be needed, is:
  delete the file, re-extend via `census.py --extend` (which fetches from the
  listing). This property is documented, not merely implied (see D3).
- **I6 — Version discipline.** Engine version 1.0.1 → **1.0.2**, changelog
  entry describing the invariant, on a dedicated fix branch. The operator
  owns the merge.

## 4. Deliverables

- **D1 — The klines patch.** The handoff §4 diff, applied to
  `_load_cache` / `_save_cache` in `engine/data.py`, with one calibration
  amendment to its comments/notes: the extra read costs **up to a few hundred
  MB of transient memory for full-history 1m majors** (~3.6 M rows), not
  ~35 MB — acceptable, but stated honestly.
- **D2 — The funding mirror.** The identical two-part treatment
  (FileNotFoundError-only empty on load; merge-in-save + atomic replace on
  save) applied to `backfill_funding`'s cache read/write path.
- **D3 — Documentation of the no-delete property.** A short comment block at
  `_save_cache` and one paragraph in the repo's data README (or module
  docstring if no README section exists): the no-shrink invariant, the
  escape hatch for genuine row removal (delete + `census.py --extend`), and
  the two accepted residuals (concurrent last-writer may drop the *other*
  writer's freshly fetched rows — refetchable; a deleted file recreated via
  an engine path starts at the warm-up anchor — `coverage_ok` vs
  `data_starts.csv` is the detector).
- **D4 — Fixtures N1–N5** (see §5), added to the engine suite. Existing 26
  fixtures unmodified.
- **D5 — LEDGER.md append**, byte-for-byte:

```
## 2026-07-10 — Engine 1.0.2: cache no-shrink invariant
- Incident: BTCUSDT 5m/1h kline caches truncated to [2025-03-01, 2026-07-08) by parity_pack --backfill; attribution recomputed and verified by reviewer; estate repaired by census same day; evidence spend: zero.
- Root cause: exists()-masked load failure + conditional history merge + non-atomic whole-file save (engine/data.py).
- Fix: merge-in-save + atomic replace + loud load failures, klines and funding; invariant "caches never shrink via the save path" fixture-enforced (N1-N5). Engine 1.0.1 -> 1.0.2.
- Accepted residuals: concurrent last-writer may drop the other writer's fresh rows (refetchable); deleted file recreated via engine path starts at warm-up anchor (coverage_ok is the detector); row deletion = delete file + census --extend.
- V1 packet review: still PENDING. This entry does not close V1.
```

- **D6 — Session packet.** One zip: the diff, fixture run output (full suite),
  changelog, ledger diff, one-page manifest.

## 5. Fixtures (all hermetic via NAIAD_CACHE_DIR; numbered N for no-shrink)

- **N1 — Merge-preserve (the invariant itself).** Save a full synthetic
  multi-month series; then save a one-month windowed slice with altered
  values in the overlap. Assert: first timestamp, last timestamp, and total
  row count unchanged; overlapping timestamps carry the *new* values;
  repeating the windowed save changes nothing (idempotent).
- **N2 — Loud load.** Create a file at the cache path containing garbage
  bytes (not valid parquet). Assert `_load_cache` raises (any exception
  except a silent empty frame) — "unreadable" must never masquerade as
  "absent".
- **N3 — Atomic abort.** With a healthy pre-existing cache file, monkeypatch
  the parquet write to raise mid-save. Assert the original file's bytes are
  unchanged after the failed save (hash before == hash after), and the save
  raised.
- **N4 — First save.** With no file present, a save creates the file
  correctly (regression guard for the FileNotFoundError branch on the
  merge-read).
- **N5 — Funding mirror.** N1's scenario replayed against the funding cache
  path: full series, then a windowed slice; bounds and count unchanged,
  overlap takes new values.

## 6. Verdict criteria (pre-registered)

The phase **passes** iff: every pre-existing fixture remains green with zero
modifications to any of them (the suite may number more than the 26 anchored
at engine 1.0.1 — the census F-series was contracted to join it; the builder
states the pre-patch count in the manifest); N1–N5 green; the code diff is confined to the
functions named in §4 within `engine/data.py` (plus the D3 documentation);
engine version string reads 1.0.2 with a changelog entry; ledger diff shows
exactly the D5 block appended and nothing else changed in that file; packet
delivered. The phase **fails pending report** if §1 item 2 finds the real
code diverging from the handoff's quotes, or if any pre-existing fixture goes
red — in which case: no patching around it; stop and hand the divergence to
the reviewer.

## 7. What this phase is not

No lock-file serialization of concurrent writers. No rewrite of
`backfill_klines`' frame-assembly line. No changes to `tick.py`, the Phase
1.5 collector, or any replay/parity script. No census re-run (the estate is
already repaired and committed; the fixture suite is the verification here).
No deletion primitive. No strategy, signal, or parameter change of any kind.
No v12 analysis. Anything not in §4: stop and report instead of building.

---

## 8. Operator runbook (for Ludwig — the builder skips this section)

Rough time: ~10 minutes of attention. No long downloads this time.

**Step 1 — Put this file and the handoff where the builder can see them.**
Move `Engine_1.0.2_NoShrink_Patch_Build_Prompt.md` (this file) into the Naiad
project folder. `CACHE_TRUNCATION_HANDOFF.md` should already be there from
the investigation session — if not, move it in too. *What you should see:
both files listed in the folder that contains `LEDGER.md`.*

**Step 2 — Open PowerShell in the project folder.** Windows key → type
`powershell` → Enter, then `cd ` + drag the Naiad folder into the window +
Enter. *What you should see: the prompt ends in `...\Naiad>`.*

**Step 3 — Start the builder and hand over the contract.** Type `claude`,
Enter, then exactly: `Read Engine_1.0.2_NoShrink_Patch_Build_Prompt.md in the
project root and execute it as this session's contract. Operator decisions:
V-A confirmed (funding writer included), V-B confirmed.` *What you should
see: the builder restates the mission, checks the real code against the
handoff's quotes first, then makes a small edit and runs the test suite.*

**Step 4 — Watch for two numbers.** When the builder runs the tests, the
summary must show **zero failed**, and the passed count must equal the
pre-patch suite count **plus 5** (V-A confirmed: the funding fixture N5 is
in). The builder states the pre-patch count before touching any code. Any
red test: the builder must stop and report, not patch around it — that stop
is the contract working, not failing.

**Step 5 — Ferry.** Attach the session packet zip here, and paste as text:
the test summary line, the engine version line, and the LEDGER diff. The
patch is merged by you, and only after this review confirms the packet.
While you're at it: the **V1 census packet itself is still owed** to this
review — send it alongside if you have it, since V1 stays open until its
headline numbers are recomputed here from the raw artifacts.
