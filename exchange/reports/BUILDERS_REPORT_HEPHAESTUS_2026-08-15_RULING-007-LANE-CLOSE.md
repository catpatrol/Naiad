# BUILDERS REPORT — HEPHAESTUS — 2026-08-15 — RULING 007 + PIN — ATHENA LANE CLOSE

**Lane:** HEPHAESTUS (builder) · **Commissioned by:** operator, ruling 007 + "pin", 2026-08-15 ·
**Branch:** `v12-v1-census` · **Base:** `13c089a` · **Supersedes:** queue/006 (never filed)

---

## 0 · What this session is

Ruling 007 — retire DIGEST, hibernate HERMES, automate the residue — **landed and published in the
previous session** (`7176b6d` + `af6ebf4`). Verified still intact here, path by path. **This session
adds part 2(d), the PIN**, and closes the ATHENA infrastructure programme.

**The pin in one sentence:** the BOX-COST naming trip-wire stops being a *fraction* of the box and
becomes an **absolute 64,000 B**, because a fraction moved with the ceiling and the 6.39 MB → 16 MB
raise had quietly loosened it 2.5×.

**The one finding to read:** the first version of this pin metered `exchange/` alone while the rule
it implements says *"any BOX-BOUND file"* — and the box is `exchange/` **+ `LEDGER.md`**. That hid
`LEDGER.md`, 259,298 B, the single largest box-bound file in the project and **four times over the
wire**. It also made the correction notice's headline number false. That is the D3 metering gap —
closed at aggregate level on 2026-08-15 — **re-opened at file level by the very session that pinned
the wire.** Caught in adversarial review, fixed, and pinned by a fixture. §5, finding V-1.

---

## 1 · The pin

### 1.1 What the number is, and why absolute
| | |
|---|---|
| was | *"over ~1% of the budget"* — a fraction |
| effect of the raise | ~63,900 B → **~160,000 B**, a 2.5× loosening nobody separately asked for |
| now | **64,000 B, absolute**, `publish_exchange.FLAG_BYTES` |

**The trigger, cited as the ruling required** — APOLLO's consequence note, `LEDGER_APOLLO.md`
2026-08-15, quoted verbatim in both the CONVENTIONS correction and the constant's comment:

> *"each of this lane's last three build documents would have tripped the old wire and none trips
> the new one"*

APOLLO flagged it rather than burying it and handed it to ATHENA, who carried it as *"the one box
question still open"*. The operator has now ruled.

### 1.2 The pin is a RESTORATION, and that is measured, not asserted
Measured 2026-08-15 on the **tracked tick set** (`exchange/` + `LEDGER.md`):

| wire | files over it |
|---|---:|
| old, pre-raise ~63,900 B | **7** |
| new, pinned 64,000 B | **7** — the same seven |
| raised ~1% = ~160,000 B | **1** |

No file falls in the 100 B gap between old and new. The raised wire found **1 of 7**; the pinned
wire finds all seven. So the pin restores a sensitivity that had been all but switched off — it does
not invent a limit. *(A snapshot of a moving quantity. The live count prints on every publish, which
is the point of giving it a consumer.)*

### 1.3 Named-constant protocol, §6.4, all three legs

**Leg 1 — NAME, VALUE, THRESHOLD TEXT**, swept exhaustively and independently re-run in review.
Searched: `trip-wire` · `tripwire` · `BOX COST` · `flagged at creation` · `63,900` · `63900` ·
`160,000` · `160000` · `64,000` · `64000` · `0.01` · `ONE_PCT` · `~1%` · `1% of the box` · `1% of
the budget` · `<1%` — across `exchange/`, `scripts/`, `tests/`, `fixtures/`, `docs/`, `prompts/`,
`.claude/`, `.github/`, and all `*.json` / `*.yml` / `*.plist` / `*.toml`.

**Leg 2 — every dependent, pin-vs-import recorded:**

| site | disposition |
|---|---|
| `scripts/publish_exchange.py` | **THE ONE DEFINITION** — `FLAG_BYTES = 64_000` |
| `CONVENTIONS.md` §3.2 rule | rewritten to the absolute; **describes, does not define** |
| `CONVENTIONS.md` §3.2 BOX COST column | now asks for the FLAG too, and imports both constants |
| `CONVENTIONS.md` §4.2 custody | names `FLAG_BYTES`; preamble gained a fourth noun to match |
| `PRIMER_HERMES_..._v4.md` §6 step 2 | **the one live instruction surface** carrying `~160,000 B` / `~63,900 B` — corrected |
| `scripts/mc1_report.py:34` `ONE_PCT` | **PINNED, historical** — regenerates a document filed 2026-08-06; §6.4's own named exemplar. Untouched |
| `scripts/census2b_oracle_report.py` | **PINNED, historical** at 6,390,000. Untouched |
| lane ledgers, filed reports, ratified queue items, `docs/history/**` | **HISTORICAL — not rewritten.** A correction is a NEW entry |

**Leg 3 — historical regenerators stay pinned.** Confirmed: `git diff --stat` touches no file under
`docs/`, no queue item, and no ledger except by append.

**Wrong-section citations: clean.** `LEDGER_APOLLO.md:1113` records that this rule was once cited as
§4.2 when it lives in §3.2, and that the error propagated to two live surfaces. Both are now correct
(`PRIMER_HERMES:101` reads §3.2; the DIGEST is retired). The only surviving wrong pairings are inside
the superseded APOLLO entry, already corrected by a later entry — append-only, and left alone.

### 1.4 The pin got a consumer, deliberately
A named constant in the guard module with **nothing reading it** is worse than prose, because a
reader infers the guard enforces it and a clean publish reads as compliance. So `publish()` now reads
the wire on every publish and **names what is over it** — from `sized` and `extra_rows`, both already
computed for the budget, so **zero new git calls**.

This also closes a real gap: the rule binds *"at the moment it is created"*, which never binds a file
that **grew** across the wire. Three of the seven are append-only with no moment of creation at their
current size, and `BUILDERS_REPORT_..._M4-LAUNCHD.md` demonstrably entered the bus at 55,536 B —
correctly unflagged — and reached 68,524 B with nothing said. The publish-time read names it once
rather than never.

**It discharges half the duty and says so.** §3.2 asks for the name **and the intended home**. A
publish cannot know a file's intended home — that is the disposition table's job — so the block
supplies the naming half and points at the other, rather than redefining the duty down to what was
easy to implement.

---

## 2 · Proof

```
F-CONV: 4/4 PASS
  F-CONV-1  9 tokens, all count==2; repo-unique outside CONVENTIONS: yes
  F-CONV-2  section 0 = 5,334 B of 6,000 B budget (88.9%), headroom 666 B
  F-CONV-3  5 memory-pointer tokens, 5 resolve to a section header
  F-CONV-4  zero rules lost IN THE 2026-08-15 COLLAPSE (frozen evidence): census 422 -> 422, LOST 0
            · size within ceiling: 67,752 B of 68,500 B (headroom 748 B)
            · every narrative backlinked: 27 cases · every case cited both ways
            · rule count holds: 89 top-level rules, floor 89 (+0)
```

**SUITE — count and scope, both stated.**

```
pytest             334 passed, 1 skipped        335 collected
pytest fixtures     73 passed, 1 skipped         74
pytest tests       261 passed                   261        74 + 261 = 335  ✓
```

Ruling 007 closed at 325 (74 + 251). This session adds **10** clauses to F-BOX-1, all in `tests/`.
*(The baseline quoted in older ledgers — 288 — has been stale since 2026-08-15; it propagates by
copying, which is the argument for ruling 007 in miniature. Do not re-quote it.)*

`CONV_BYTES_CEILING` re-pinned 66,500 → 68,500 with a dated note, per the fixture's own written
instruction: re-pin with a note saying what grew and why, **never trim law to hit a number**. Growth
is the rewritten rule, the dated correction, the trip-wire-of-record sentence, the three-limits
distinction and the custody amendment — all rule or dated correction.

---

## 3 · The lane close

**ATHENA's infrastructure programme is CLOSED. Custody is RETAINED.** That distinction is the whole
content of the close, and it is what stops this from orphaning the estate:

| retained | why it cannot be dissolved |
|---|---|
| **threshold custody** (§4.2 — now five constants incl. `FLAG_BYTES`) | `publish_exchange.py` says *"moving this number is a separate operator ruling"*, and §4.2 routes that ruling through ATHENA. Dissolve the lane and the escape hatch has no channel |
| **`CONVENTIONS.md` drafting** (§ header, MAINTENANCE) | the file names ATHENA as its only drafter and its escalation address |
| **phase-boundary audits** (MAINTENANCE) | the live memory-panel re-read has no other owner |

So ATHENA is **not** dormant and is deliberately **not** added to `DORMANT_LANES` — unlike HERMES,
whose ledger would otherwise age like neglect in the bus-health table. What closed is the
construction programme: the bus, the guards, the manifest ritual, the routines, the collapse, the
box governance and now the pin. **Operation is automated; nothing waits on a lane to run it.**

**Every carried item is disposed of, because a lane that closes with unlisted open items is the
defect.** Full disposition in the `LEDGER_ATHENA` append; summary:

- **CLOSED by this session** — the ~1% trip-wire (PENDING 2, carried twice).
- **CLOSED by ruling 007** — "DIGEST.md is stale in a way that bites" (the carried NEXT); it is retired.
- **CARRIED, operator-owned** — Sync now (GUI); the HALT-gate question; the unacted-inbox home
  (**deadline 2026-09-03**); queue-003 D-2's cadence re-home; `exchange/drops/` ownership; the live
  memory panel; F-BH-1/F-BOX-1 not running in CI.

`LEDGER_HERMES` receives its dormancy entry, which closes that ledger's 11-day staleness as a
byproduct — the gap ruling 007's own bus-health table had been reporting.

---

## 4 · Findings from adversarial review

Ten agents across two workflows. Thirteen defects found in this session's own work; all fixed.

| # | finding | sev | status |
|---|---|---|---|
| **V-1** | **Trip-wire metered `exchange/` only while the rule says "box-bound".** Hid `LEDGER.md` (259,298 B, 4× over). Made the correction's headline false: "zero over the raised wire" — `LEDGER.md` trips even that. The D3 gap re-opened at file level. | **blocking** | fixed — reads the tick set; figures corrected to 7/7/1 in all three places; fixture added |
| **V-2** | `test_..._does_not_scale_with_the_box` was **itself derived from `BOX_BYTES`** and would go RED if the box were *lowered* to 6.4 MB — telling a future operator to move `FLAG_BYTES` with the box, the exact opposite of the pin | important | fixed — independence now tested by independence, under three pretend ceilings |
| **V-3** | `report_lines()` ignored `over_flag`, so the naming reached only stdout — a launchd log. §3.2 says *flagged to the operator*; this module already carries the scar of a 3-day unseen outage | important | fixed — `_flag_report_lines()` puts it in the DAILY report |
| **V-4** | §3.2's **BOX COST column** — the nearest dependent of all, three lines above the rewritten rule — still said "% of the box, take the capacity from `BOX_BYTES`", producing a number that answers the retired question | important | fixed |
| **V-5** | Advisory printed *"nothing is refused"* **inside a refused publish** | important | fixed — "naming only; this wire never refuses a publish" |
| **V-6** | Advisory did not run on the `NOTHING` path, while PRIMER claimed "every publish". `LEDGER.md` is in the tick set and moves without `exchange/` moving | important | fixed — prints there too, matching the head-pair precedent |
| **V-7** | `flag_lines` docstring said *"naming is the whole duty"*, contradicting §3.2's "with its intended home" — redefining the duty to match the implementation | important | fixed — concedes the half it cannot discharge, points at the disposition table |
| **V-8** | The only **uncapped** list in a module that slices every other one at 10/20; the pin guarantees it only grows (6 → 28 at WARN → 69 at REFUSE) | minor | fixed — capped at 10 with an overflow line |
| **V-9** | The 7/7/1 measurement written into law with no refresh path | minor | fixed — date-stamped as a snapshot in all three homes; the live number is the advisory |
| **V-10** | CONVENTIONS claimed the OPEN item was closed in **`LEDGER_APOLLO`** too, which this session does not append | important | fixed — names `LEDGER_ATHENA`, which holds custody and carried it |
| **V-11** | PRIMER banner asserted DAILY §8 exists; the routine has not run since ruling 007 committed, so the newest DAILY still ends at §9 | important | fixed — "from the next routine run onward", with the current state stated |
| **V-12** | Closing ATHENA would orphan CONVENTIONS drafting, five-constant custody and the phase-boundary audit | **blocking** | resolved — the close is *programme closed, custody retained*; §3 |
| **V-13** | Missing build document / ledger appends / publish | — | this document, the two appends, and the publish below |

### Reported, NOT fixed
1. **`exchange/.DS_Store` is TRACKED** (6,148 B, binary) and rides every publish — a Finder visit
   alone makes `git add -- exchange` stage a binary diff into a box whose §4.2 rule is *text only*.
   Pre-existing; the fix (`git rm --cached` + `.gitignore`) is a non-exchange commit and outside this
   ruling.
2. **On the REFUSE path** the advisory's named files are re-listed by `_oversize_lines` with
   percentages that all read under 1% — the retired wire's own unit. The wording fix removes the
   contradiction; re-designing the REFUSE table is not this ruling's business.
3. **F-BOX-1 and F-BH-1 do not run in CI.** `.github/workflows/ci.yml` runs `pytest fixtures/` only.
   One-line fix; widening CI scope is an ops decision.
4. **Carried from ruling 007:** the unacted-inbox home (**2026-09-03**), queue-003 D-2's cadence,
   `exchange/drops/`, the live memory panel.

---

## 5 · File disposition

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `exchange/status/CONVENTIONS.md` | yes | tracked | publish | yes | GitHub | 67,752 B · 0.423% · **FLAGGED** (over 64,000 B) |
| `exchange/reports/PRIMER_HERMES_2026-08-11_v4.md` | yes | tracked | publish | yes | GitHub | 8,822 B · 0.055% |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-15_RULING-007-LANE-CLOSE.md` | yes | tracked | publish | yes | GitHub | this file · **under** the wire |
| `exchange/status/LEDGER_ATHENA.md` | yes | tracked | publish | yes | GitHub | appended · **FLAGGED** (98,920 B before append) |
| `exchange/status/LEDGER_HERMES.md` | yes | tracked | publish | yes | GitHub | appended · 5,156 B before append |
| `scripts/publish_exchange.py` | yes | tracked | hand commit | yes | GitHub | n/a — outside `exchange/` |
| `scripts/fixtures_conventions.py` | yes | tracked | hand commit | yes | GitHub | n/a |
| `tests/test_box_guard.py` | yes | tracked | hand commit | yes | GitHub | n/a |

**Intended homes, per §3.2, for the flagged files:** both stay on the bus. `CONVENTIONS.md` is the
tick set's reason for existing and every lane reads it; `LEDGER_ATHENA.md` is append-only lane state
that §5 rules must live on the bus. Neither is a candidate for relocation — the flag is doing its
job by making the choice explicit rather than by demanding a move.

**Rollback:** `git revert <hand-commit>` then `git revert <publish>`. Nothing deleted.

**Noted:** other sessions are writing to this repo concurrently (five untracked `exchange/reports/`
files at commit time). `publish()` stages all of `exchange/` by design, so they ride this publish.
The hand commit lists explicit paths only.
