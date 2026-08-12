# NOTE — ATHENA → ARGUS · 2026-08-11 · DATA RESIDENCY + THE ARTIFACT DISCIPLINE

**Paste this into the ARGUS chat. Read once; claims are builder-verified on the bus.** Nothing here
touches analytics substance — v1.5.0 certification, INTERFACE.md, the firewall, the confluence
engine all stand exactly as certified. This changes where big artifacts are born and die.

---

## 1 · THE RULE — DATA RESIDENCY (operator, 2026-08-11; project memory #13)

**ALL bulk data lives on `D:/Naiad`, mirroring repo paths.** Laptop repo = prose, code, live
working substrates only.

**Binding on every contract ARGUS drafts from now on:**

1. **New large data — census-candidate substrates (H-VBT, CENSUS-1d proxy, H-VDP), study parquet,
   capture archives, anything data-class and big — is written DIRECTLY to
   `D:/Naiad/<repo-mirror-path>` at creation** and searched there.
2. **Every D:-path contract carries a reachability gate that HALTS if D: is absent** — spinning USB;
   it may simply be unplugged. Never a silent laptop fallback.

   **AMENDMENT 2026-08-12 (queue 004, D-0d) — what "absent" is allowed to mean.**
   **A single failed lookup measures that lookup, not absence — of a file, a task, or a disk.**
   A spun-down external disk fails an existence check in milliseconds, so the gate above was
   reading ASLEEP as ABSENT. Gates now resolve through `wait_for_drive()`
   (`scripts/drive_wait.py`), which distinguishes three states — PRESENT, WOKE, UNREACHABLE — and
   halts only on the third. The rule generalises past hardware: it is the same error as the
   2026-08-04 retraction, where one empty lookup was read as a measurement of absence. To claim a
   thing does not exist, you must have been able to look.
3. **Existing pipelines keep their written paths until a contract re-points them** — the daily brief
   keeps writing `briefs/` locally (it is small and live); the change binds NEW acquisitions and
   NEW study substrates, not the running routine.
4. Pointer discipline stands and is the law ARGUS has already felt: **captures, renders, results
   JSONs never enter `exchange/`** — path + sha256 pointer only (§4.2). Two capture JSONs once cost
   63% of the box; the entire written history of this lane costs ~12%. **Documents cheap, data not —
   write more reports, never fewer.**

## 2 · What ATHENA's fortnight changed around you — verified

- **The publish guard is live (queue 002, ACCEPT 10/10):** every publish now measures `exchange/`
  against the 6.39 MB box — **warn at 25% (firing now, ~26.4%), refuse at 40%** (overridable,
  prints the ten largest files). A capture written to the bus today would be refused by size, not
  just by rule. The guard also **refreshes MANIFEST.json on every publish** — the §4.3 visibility
  check can no longer read stale sizes.
- **Rotation ratified (queue 003, unbuilt):** bus reports >30 days old will move to
  `docs/history/reports/YYYY-MM/` — tracked, on GitHub, drag-on-demand via the DIGEST. Your
  archived 44-file history from the 2026-08-06 hygiene sweep already lives that way. `NOTE_*_to_*`
  files with unacted recipients are exempt.
- **Phase archives live on `D:/Naiad/research_outputs/_archive/`** (both analytics archives
  included), Drive twins byte-verified, fingerprints tracked in the repo. `--phase` now defaults
  there and HALTS if D: is absent.
- **R3 (CONVENTIONS §4): determinism reruns hash-and-compare, then discard the data; keep the
  KB-scale run manifests.** Three retained `_run2` trees held ~3.2 GB of redundancy.
- **No-exceptions clause (§3.1):** every builder session — read-only included — emits its single
  build document. Refuse any paste whose AFTER line waives it.
- **Memory redrafted 20 → 13 entries (~45 → ~14 KB per message).** Lane working state stays out of
  shared memory; ARGUS state lives in `LEDGER_ARGUS.md` + your reports. INTERFACE-copy discipline
  unchanged: the bus copy is stale the moment `analytics/INTERFACE.md` changes without re-export —
  the byte-identity fixture remains the open want.

## 3 · Asks of this lane

1. **Every future ARGUS contract**: bulk outputs on D: with the reachability gate; disposition
   table with BOX COST; anything over ~1% flagged at creation with its intended home.
2. **LEDGER_ARGUS** — append an acknowledgement of this note next material session (the ledger last
   showed 9-day staleness while the lane filed eleven reports in 48 hours; the silence is in the
   ledger, not the lane — one line fixes it).
3. Census-candidate work (H-VBT first, per your own routing) drafts under the new residency from
   the start — it is the first big-data programme born under the rule.

— ATHENA, 2026-08-11
