# BUILD — ORACLE A2 CLOSE · 2026-08-16

**Contract:** queue BR-1 `BRIEF_REDESIGN_SPEC_v1`, Amendment A2 (operator rulings 2026-08-16,
verbatim "BOARD OK, Rb posture, Rc 26, Rd yes, Re keep, Rf defer"). **Executor:** HEPHAESTUS.
**Reviewer:** ARGUS. **Class:** operations / display-only. **Code commit:** `22c94d4`.

---

## 0 · WHAT THIS DOCUMENT IS

**This corrects a half-executed paste.** The previous instruction carried BR-1b (the cache
top-up) *and* Amendment A2. **BR-1b landed and is BUILT** — `BUILD_2026-08-16_ORACLE_TOPUP.md`,
commits `3bdc4c5` + `20f4a36`, F-TU 6/6, two slots armed. **A2 did not.** This paste executes A2
only. The top-up was verified BUILT at the gate and **was not rebuilt or touched**, except for
one thing it forced and which is the single most important line in this document:

> **THE RENAME CHANGED `oracle_daily.py`, WHICH THE TOP-UP PINS BY sha256.**
> The pin was re-pinned in the same commit. Without that, the 06:45 job would have HALTed
> tomorrow morning. Old `45f44015…` → new `5f0338c1…`, verified matching after re-enumeration.

**BR-1 IS NOW ACCEPTED IN FULL.** A2-1 discharges §6's third clause — the operator's Board
confirmation — which was the one acceptance criterion the build could not satisfy for itself.

---

## 1 · THE RULINGS, AND WHAT EACH ONE CLOSED

| Ruling | Closes | Effect |
|---|---|---|
| A2-1 BOARD ACCEPTED | BR-1 §6 clause 3 | **BR-1 VERDICT: ACCEPT** |
| A2-2 posture canon v1 | **V-1** (one name, two meanings) | rename sweep, 71 substitutions |
| A2-3 trigger pair = 26 | **V-6** | 1 prose correction, 2 quotes preserved |
| A2-4 NET_RR_FORM ratified | **V-5** (no formula existed) | register row `ruled: True` |
| A2-5 07:00 kept | **V-4** (slot collision) | no change; top-up precedes at 06:45 |
| A2-6 defer nine rows | the [VETO] table | DEFERRED-TO-BR2 in code and render |
| A2-7 staleness banner | **T-3, partially** | banner installed; T-3 still open |

Four of the ten findings the ORACLE REBIRTH build reported are now closed by ruling. V-2 (the
four words have no per-word definition) is closed in substance by A2-2 naming them and A2-6
deferring the wording to measurement. **V-7 (the two rails, 0.5 vs 1.0) is APOLLO's F-C3-e and
remains open** — the Oracle uses 1.0 per C-6 and has not touched the engine config. **T-3's
wake-order race remains open** and A2-7 is explicitly a partial remedy.

---

## 2 · THE RENAME — occurrence table, by ownership

Enumerated BEFORE any edit, with `git grep` over the whole repo.

| FILE | HITS | DISPOSITION |
|---|---:|---|
| `scripts/station_engine.py` | 14 | **RENAMED** → `scripts/posture_engine.py` (git mv) |
| `scripts/oracle_daily.py` | 10 | **REWRITTEN** (28 substitutions incl. the `PE` alias) |
| `scripts/oracle_fixtures.py` | 9 | **REWRITTEN** (20 substitutions) |
| `scripts/oracle_topup.py` | 2 | **REWRITTEN** (6 substitutions) |
| `research_outputs/oracle/station_canon.json` | 2 | **RENAMED** → `posture_canon.json` (git mv) |
| `.gitignore` | 2 | **REWRITTEN** (the tracked-exception negation) |
| `exchange/reports/BUILD_2026-08-16_ORACLE_REBIRTH.md` | 14 | left as written — historical |
| `exchange/queue/2026-08-16_BR1_brief_redesign_ARGUS.md` | 3 | left as written — ratified contract |
| `exchange/queue/2026-08-16_BR2_oracle_calibration_parity_R2_ARGUS.md` | 2 | left as written — ratified contract |
| `exchange/status/LEDGER_ARGUS.md` | 2 | left as written — append-only record |
| `docs/memory/NAIAD_MEMORY_VERBATIM_2026-08-15.md` | 2 | left as written — other lane |
| `exchange/reports/ARGUS_RESCOPE_2026-08-15.md` | 1 | left as written — historical |

**39 ARGUS-owned occurrences renamed · 24 other-lane and historical occurrences left as written.**
Residual `station_canon` / `station_engine` in ARGUS-owned sources after the sweep: **0**.

### 2.1 What was deliberately NOT renamed, and why

The instruction enumerated three tokens — `station_canon`, `station_engine`, `"station canon"`.
These identifiers contain the word "station" but are **outside that set**, and two of them are
live data schemas that BR-2 reads mid-week:

- `stations_for()`, `AssetStations`, `STATION_WORDS` — internal Python names, not the enumerated
  tokens.
- the tape's `station` column and the calibration JSON's `station_distribution` key — **renaming
  these is a schema change** to artifacts accruing daily for TC4 and for BR-2's recalibration.
  A naming paste is not the place for a schema change; it belongs in BR-2 if wanted at all.

Stated here rather than done silently, so nobody later reads the omission as an oversight.

### 2.2 A2-3, and why two occurrences of "12/25" survive

Oracle-owned "12/25" prose lived in exactly one file, `posture_engine.py`, at three sites. One
was **our** disclosure prose and is rewritten to record the ruling. **Two are verbatim quotes of
the 2026-08-13 canon document.** A quote that is edited is no longer a quote, so both are
preserved exactly and carry an A2-3 rider outside the quotation. Every other `12/25` in the repo
(21 occurrences across census2a, mc2, seq8, brief2, census2b) belongs to other lanes and is
untouched, as A2-3 directs.

---

## 3 · FIXTURES — all suites, after the change

```
F-BR-1..F-BR-10   GREEN 10/10 · RED 0
F-TU-1..F-TU-6    GREEN  6/6  · RED 0
F-CONV            4/4 PASS
                  ----------------------
TOTAL             20/20 green
```

F-TU-1's sha-pin leg is the one that mattered: it passes **against the re-pinned sha**, and the
HALT was observed firing against the stale one first (recorded in §4).

---

## 4 · THE RE-PIN, IN ORDER

```
1. rename edits land            -> oracle_daily.py sha changes
2. load_scope() BEFORE re-pin   -> "HALT: oracle_daily.py has changed since the scope
                                    was enumerated."          <- the guard works
3. oracle_topup.py --enumerate  -> 40 pair(s), 10 symbols x [15m,1h,4h,5m]
4. load_scope() AFTER re-pin    -> 40 pairs OK
   pinned  5f0338c1ea737c578d2ed4c7a87fae76eeeef4947946beff516e2e678c608a3c
   current 5f0338c1ea737c578d2ed4c7a87fae76eeeef4947946beff516e2e678c608a3c   MATCH
```

The enumerated scope is unchanged by the rename — 40 pairs before, 40 after — which is the
expected result and is itself a small check that the rename did not alter behaviour.

---

## 5 · THE REVIEW RENDER

```
launchctl kickstart -k gui/501/com.naiad.oracle-0700   ->  runs = 1, last exit code = 0
path    briefs/oracle/oracle_2026-08-16.html
bytes   233,224
sha256  343e4acea6c1516cc0d75f868fc80e9142d702f5076f4a17a818e36f012b6c86
as-of   2026-08-16T00:00Z
staleness banner   ABSENT (correct)
"posture canon" in the appendix   4 occurrences
DEFERRED-TO-BR2 chips             19
```

---

## 6 · FINDINGS — REPORTED, NOT FIXED

**A-1 · THE A2-7 BANNER HAS HAND-RUN WINDOWS, AND THEY ARE NOT A BUG.** A2-7 says the banner
fires when the newest cache bar is "older than 2 lens periods at render time", and age is
measured from the bar's own `open_time`. At **both scheduled slots a healthy system is silent**
with margin — 6.0h at the 10:00Z render and 7.0h at the 19:00Z render, against an 8.0h limit.
But between a 4h bar closing and the next top-up the cache is *legitimately* one bar behind, so
a **hand-run** render in those windows shows STALE while nothing is wrong:

| window (UTC) | length | why |
|---|---|---|
| 16:00Z → 18:45Z | 2.75h | the 08:00Z bar closed at 12:00Z; next top-up 18:45Z |
| 00:00Z → 09:45Z | 9.75h | the 16:00Z bar closed at 20:00Z; next top-up 09:45Z |

This is faithful to the ruling as written, and A2-7 is explicitly **[VETO-by-firing]** — the
threshold earns its keep the first time it fires. The two remedies, if you want one, are a third
top-up slot or measuring age from the bar's close rather than its open. **Not chosen here; the
ruling is yours.**

**A-2 · BR-2 NOW CARRIES A DANGLING POINTER.** `exchange/queue/2026-08-16_BR2_…ARGUS.md` is a
RATIFIED contract and was correctly left as written, but its fixture F-R2-1 reads *"JS reads the
same station_canon.json sha as Python"* and that file is now `posture_canon.json`. **A ratified
contract is not the executor's to edit**, so the mapping is recorded here and in the APOLLO note
instead: **BR-2's `station_canon.json` means `posture_canon.json`.** BR-2's executor must read
this line, or amend BR-2 by operator ruling first.

**A-3 · T-3 IS STILL OPEN.** A2-7 is a display-only partial remedy. The wake-order race — a
laptop asleep at 06:45 fetches on wake, possibly after the 07:00 Oracle has rendered — is
unaddressed, and the standing question is whether the Oracle should refuse to render on a cache
older than N hours rather than merely say so.

**A-4 · UNCHANGED, INHERITED.** V-7 rails remain APOLLO's F-C3-e; the manifest F-4 LAG and the
tracked `exchange/.DS_Store` remain as previously reported. `com.naiad.daily` untouched.

---

## 7 · DISPOSITION

BOX constants by import from `publish_exchange` (`BOX_BYTES` 16,000,000; `FLAG_BYTES` 64,000).
Warn at 40%, refuse ABOVE 70%; the wire flags files strictly over 64,000 B.

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `scripts/posture_engine.py` | yes | yes | `22c94d4` (R from station_engine.py) | rides this branch push | hand commit, explicit paths (CL-13) | 31,039 B, non-box |
| `scripts/oracle_daily.py` | yes | yes | `22c94d4` | rides this branch push | same | 57,005 B, non-box |
| `scripts/oracle_fixtures.py` | yes | yes | `22c94d4` | rides this branch push | same | 33,266 B, non-box |
| `scripts/oracle_topup.py` | yes | yes | `22c94d4` | rides this branch push | same | 21,948 B, non-box |
| `.gitignore` | yes | yes | `22c94d4` | rides this branch push | same | non-box |
| `research_outputs/oracle/posture_canon.json` | yes | yes | `22c94d4` (R from station_canon.json) | rides this branch push | tracked exception, BR-2 F-R2-1 | 9,548 B, non-box |
| `research_outputs/oracle/topup_scope.json` | yes | yes | `22c94d4` **re-pinned** | rides this branch push | tracked exception; G-TU-1 | 2,928 B, non-box |
| `exchange/queue/2026-08-16_BR1_brief_redesign_ARGUS.md` | yes | yes | publish | yes | publish guard, `exchange/**` scope | 8,152 B → 0.051% |
| `exchange/reports/NOTE_ARGUS_to_APOLLO_2026-08-16_rulings_relay.md` | yes | yes | publish | yes | same; exempt from queue-003 rotation | 2,627 B → 0.020% |
| `exchange/reports/BUILD_2026-08-16_ORACLE_A2_CLOSE.md` | yes | yes | publish | yes | same | this file |
| `exchange/status/LEDGER_ARGUS.md` | yes | yes | publish | yes | same, append-only | +~1.4 KB |
| `briefs/oracle/oracle_2026-08-16.html` | yes | **no — gitignored** | — | — | residency block, F-BR-9 | 233,224 B, OFF-BUS |
| `research_outputs/oracle/tape/`, `calibration/`, `payloads/` | yes | **no — gitignored** | — | — | same | OFF-BUS |
| `~/Library/LaunchAgents/com.naiad.oracle-*.plist` (4) | yes | **no — outside the repo** | — | — | CADENCE registry | unchanged this paste |

### 7.1 BOX-COST

This paste adds roughly **6 KB to the bus at 16,000,000 B** — the A2 append, the APOLLO note,
this document and the ledger append. No artifact it produced is over the 64,000 B naming wire.
The render, tape, payloads and calibration remain off-bus by the residency block; the kline
cache is outside the repo entirely.

**Intended homes, per §3.2.** `posture_canon.json` and `topup_scope.json` stay tracked — the
first because BR-2 F-R2-1 needs both languages on one sha, the second because the top-up's whole
claim is that its scope is enumerated, and a tracked manifest makes a scope change a diff.

---

## 8 · WHAT THIS PASTE IS NOT

Not a rebuild of BR-1b — it was verified BUILT and left alone but for the forced re-pin. Not a
schema change: the tape and calibration keys are untouched. Not census work: nothing scored,
nothing aggregated. Not an edit to any ratified contract or any other lane's file. Not a closure
of T-3, and not a ruling on the rails.

— HEPHAESTUS, 2026-08-16. Reviewed against BR-1 Amendment A2.
