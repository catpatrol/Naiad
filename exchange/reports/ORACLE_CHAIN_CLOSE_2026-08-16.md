# ORACLE CHAIN — CLOSE ATTEMPTED 2026-08-16 · **CHAIN NOT CLOSED**

**Contract:** queue BR-2 `ORACLE: RECALIBRATION · PARITY VERDICT · R2 SECOND EYE`, RATIFIED
operator 2026-08-16 (pre-authorized per BR-1 Amendment A1-3). **Executor:** HEPHAESTUS.
**Reviewer:** ARGUS. **Class:** operations. **BR-2 remains BUILT: PENDING.**

---

## 0 · THE ONE THING TO READ FIRST

**All three of BR-2's hard gates fail, so no BR-2 work ran.** The contract opens with "GATES
(all HARD, checked before any work)", and the reason they fail is simply that the live week has
not happened yet: the whole Oracle estate was built today, 2026-08-16. There is one render, one
day of self-checks, and no operator parity line.

This is not a defect and nothing is broken. It is the gate doing precisely its job — refusing to
let a recalibration be computed from a day of data and called a week.

**What ran:** this halt record, the ledger append and the publish.
**What halted:** WORK (1) recalibration, (2) parity verdict, (3) the R2 build.
**BR-2 is NOT stamped BUILT.** It stays PENDING until its own gates open.

Two boundary notes, stated rather than glossed. First, this document occupies WORK (4)'s named
path `ORACLE_CHAIN_CLOSE_<date>.md`, but it is a **halt record, not the chain close**: the path
is date-parameterised, so the real WORK (4) artifact will be `ORACLE_CHAIN_CLOSE_2026-08-22.md`
or later and will not collide with this one. Second, WORK (4) bundles three components — report,
ledger append, BUILT stamps — and the third is **deliberately dropped**, because stamping BUILT
on work that did not run is precisely the false record the estate's discipline exists to
prevent. That is a considered omission, not a partial adoption.

**Earliest possible execution: 2026-08-22, and only with the operator's PARITY line.**

---

## 1 · THE GATES, WITH EVIDENCE

### G-BR2-1 · NOT-BEFORE — **FAIL**
> "≥7 dated `oracle_*.html` files exist in `briefs/oracle/`."

```
briefs/oracle/oracle_2026-08-16.html
COUNT = 1 / 7 required
```

The 07:00 full run and the 16:00 refresh both write `oracle_<date>.html`, so the estate accrues
**one file per calendar day**. Seven distinct dates starting today lands on **2026-08-22**.

### G-BR2-2 · SELF-CHECKS — **FAIL**
> "`selfcheck_log.jsonl` shows PASS on ≥5 of the last 7 days; print the log verbatim."

The gate's own imperative is "print the log verbatim", so the log is reproduced here in the
artifact rather than left in terminal scrollback:

```json
{"checks": {"refresh_idempotence": {"detail": "Board 4,741 B and Watch 5,426 B byte-identical across two renders over unchanged data", "pass": true}, "tape_append_integrity": {"detail": "1 tape file(s), newest oracle_tape_2026-08-16.parquet with 10 rows, 24 columns; missing=[]; outcome_columns=[]", "pass": true}, "thumbnail_provenance": {"detail": "10 strips; each canvas binds a payload whose meta.sha256 recomputes from its own data block and is printed in that strip's footer (the shipped VIZ-4 convention: data-block sha, not file sha)", "pass": true}}, "date": "2026-08-16", "html_sha": "8e1fb36612f27d79a80a07a334d439e16150c45cd0fb1a6a2685e2a43ae32e2c", "seconds": 5.6, "slot": "full", "ts": "2026-08-16T05:12:25.525473+00:00", "verdict": "PASS", "zone_agree": true}
{"checks": {"refresh_idempotence": {"detail": "Board 4,805 B and Watch 5,426 B byte-identical across two renders over unchanged data", "pass": true}, "tape_append_integrity": {"detail": "1 tape file(s), newest oracle_tape_2026-08-16.parquet with 10 rows, 24 columns; missing=[]; outcome_columns=[]", "pass": true}, "thumbnail_provenance": {"detail": "10 strips; each canvas binds a payload whose meta.sha256 recomputes from its own data block and is printed in that strip's footer (the shipped VIZ-4 convention: data-block sha, not file sha); and the paint routine (divRGB/heatCanvas/putImageData/paintStrips + its DOMContentLoaded hook) is present in the document", "pass": true}}, "date": "2026-08-16", "html_sha": "174002547fbfee8674f73a8c74d9365c9cee3f228398c29187345f9714e2b9bb", "seconds": 5.6, "slot": "full", "ts": "2026-08-16T05:49:15.209072+00:00", "verdict": "PASS", "zone_agree": true}
{"checks": {"refresh_idempotence": {"detail": "Board 4,806 B and Watch 5,274 B byte-identical across two renders over unchanged data", "pass": true}, "tape_append_integrity": {"detail": "1 tape file(s), newest oracle_tape_2026-08-16.parquet with 10 rows, 24 columns; missing=[]; outcome_columns=[]", "pass": true}, "thumbnail_provenance": {"detail": "10 strips; each canvas binds a payload whose meta.sha256 recomputes from its own data block and is printed in that strip's footer (the shipped VIZ-4 convention: data-block sha, not file sha); and the paint routine (divRGB/heatCanvas/putImageData/paintStrips + its DOMContentLoaded hook) is present in the document", "pass": true}}, "date": "2026-08-16", "html_sha": "343e4acea6c1516cc0d75f868fc80e9142d702f5076f4a17a818e36f012b6c86", "seconds": 5.7, "slot": "full", "ts": "2026-08-16T07:40:16.024343+00:00", "verdict": "PASS", "zone_agree": true}
```

Summarised:

| date | verdicts | |
|---|---|---|
| 2026-08-16 | PASS · PASS · PASS | three runs, all green, but **one date** |

```
rows = 3 · distinct dates = 1
DAYS WITH A PASS = 1 / 5 required
```

Three PASS rows on one calendar day is not five days. Every check inside them is green —
refresh idempotence, tape append integrity, thumbnail provenance — so the organ is healthy;
there simply has not been enough of it yet. **Opens 2026-08-20 at the earliest.**

### G-BR2-3 · HUMAN PARITY — **FAIL**
> "a line `PARITY: OK <date>` or `PARITY: mismatches: ...` exists in
> `exchange/status/LEDGER_ARGUS.md` dated within the live week."

No such line exists. Every "parity" occurrence in the ledger is either the BR-1 V-3 disclosure
(Pine SS v12.1 absent from the repo) or a PENDING/NEXT item naming this very gate as owed. The
near-miss check was run with a looser regex and found nothing that a stricter one dropped.

**This gate is not mine to satisfy.** It is the operator's one mid-week chart glance, relayed
through the ARGUS lane. No date can be computed for it.

---

## 2 · WHY THE HALT IS TOTAL, INCLUDING RECALIBRATION

BR-2's G-BR2-3 carries a clause that deserves an explicit reading, because it is the one place
the contract lets work survive a failure:

> "Mismatches ⇒ R2 HALTS, **recalibration still runs**, mismatch autopsy becomes the deliverable."

That clause describes a **specific** state: the parity line **exists** and **reports
mismatches**. Today's state is different — there is **no parity line at all**, which is an
absence of evidence rather than adverse evidence, and the clause does not reach it.

More decisively, the clause could not rescue the recalibration anyway. WORK (1) is defined as
measuring "every v1 threshold … **against a week of measured distributions**". G-BR2-1 and
G-BR2-2 fail independently of parity, and they fail *because that week does not exist*: there is
exactly **one** calibration JSON on disk. A recalibration computed from one day would be a
number fitted to a single sample and presented as a measurement — which is precisely what BR-2's
own "NOTHING self-adopts" clause exists to prevent, and what the estate's standing discipline
forbids.

So: **not one of WORK (1), (2) or (3) may run.** Halting all three is the contract being
obeyed, not the executor being timid.

---

## 3 · WHAT THE CHAIN LOOKS LIKE FROM HERE

| link | state | evidence |
|---|---|---|
| BR-1 THE ORACLE | **BUILT · ACCEPTED** | `BUILD_2026-08-16_ORACLE_REBIRTH.md`; A2-1 discharged §6 clause 3 |
| BR-1b THE TOP-UP | **BUILT** | `BUILD_2026-08-16_ORACLE_TOPUP.md`; F-TU 6/6; 2 slots armed |
| BR-1 Amendment A2 | **EXECUTED** | `BUILD_2026-08-16_ORACLE_A2_CLOSE.md`; posture canon v1 |
| **BR-2** | **PENDING — gates shut** | this report |

Four launchd agents remain armed and will keep accruing the evidence BR-2 needs without any
further instruction: `oracle-topup-0645` → `oracle-0700` → `oracle-topup-1545` → `oracle-1600`,
all at Buenos Aires wall-clock. Each morning adds one render, one tape parquet, one calibration
JSON and one self-check row.

### 3.1 What the operator owes the chain

One line, appended to `exchange/status/LEDGER_ARGUS.md` during the live week, in exactly this
form so G-BR2-3's matcher finds it:

```
PARITY: OK 2026-08-1X
   or
PARITY: mismatches: <symbol> <expected> vs <seen>; ...
```

It is one chart glance: open the Board, open TradingView on the same symbols at the 4h lens, and
confirm the posture words agree with the Pine markers. Mismatches are **not** a failure of the
paste — BR-2 explicitly turns them into the deliverable (recalibration still runs, the autopsy
becomes the product, R2 waits).

---

## 4 · CARRYOVER RECORDED FOR BR-2's EXECUTOR

**The rename — now recorded ON BR-2 itself.** BR-1 Amendment A2-2 renamed
`station_canon.json` → `posture_canon.json`, and BR-2's ratified body still names the old file
in F-R2-1. The previous paste left that dangling and recorded the mapping only in a report; an
adversarial audit of this halt argued, correctly, that the operator had **already ruled** the
mapping in the execution paste, and that recording an existing ruling on the contract is
contract hygiene rather than a gated WORK item — the same act by which A1 and A2 were appended
to a ratified BR-1.

So **`AMENDMENT A-BR2-1` is appended to BR-2**, quoting the operator's note verbatim and
attributed to the 2026-08-16 execution paste. It rules nothing new, leaves gates, WORK items and
fixtures untouched, and leaves `BUILT: PENDING` standing. Revert that one block if you disagree.
Per that note and `BUILD_2026-08-16_ORACLE_A2_CLOSE.md` §2:

> **F-R2-1 discharges against `posture_canon.json`.** The tape's `station` column is unchanged
> **by design** — renaming it would be a schema change to an artifact accruing daily for TC4.

Verified ready today, so nothing but the gates blocks it:

```
research_outputs/oracle/posture_canon.json   9,548 B   TRACKED
file sha256   c085a9392b4109dd5c497b5acd4ef61c656832bd383131b09e39fbf5e0d84fad
canon_sha()   c085a9392b4109dd5c497b5acd4ef61c656832bd383131b09e39fbf5e0d84fad   MATCH
```

Both sides already agree on one sha, which is exactly what F-R2-1 will assert once there is a JS
surface to assert it from.

**The deferred rows.** A2-6 deferred nine register rows to BR-2's measured proposals —
`CANON.STALKING` wording · `DEAD_MEMORY_BARS` · `BOARD_PRECEDENCE` · `HEAT_KEY` / `HEAT` ·
`GRID_TOLL_KEY` · `FIRED_WINDOW_HOURS` · `TRIGGER_FRESH_BARS` · `OVERLAP_BARS`. All nine print
as DEFERRED-TO-BR2 in the render's own appendix and are written into every calibration JSON, so
the week of distributions BR-2 needs is accruing on its own.

---

## 5 · FINDINGS — REPORTED, NOT FIXED

**C-0 · TIME-CRITICAL — THE LIVE WEEK IS ABOUT TO PRODUCE UNUSABLE DATA FOR HALF OF WHAT BR-2
MUST RECALIBRATE.** Surfaced by an adversarial audit of this halt and verified independently.

BR-1 Amendment A1-4 requires the D-7 logger to record "maturity-withheld fractions". It does
not compute one. `scripts/oracle_daily.py` writes the **literal** `"maturity_withheld_fraction":
0.0` for every asset, every run:

```
logged values : all ten assets 0.0
distinct set  : {0.0}          <- a constant, never computed
```

`analytics.vwap.maturity(bars, line_min=16, band_min=60)` already returns
`line_ok / band_ok / thin_sample` and is one call away. Two further threshold families BR-2's
WORK (1) enumerates are absent from the calibration document altogether: **no family-cap binding
count** (the older lane's `brief_calibration_c4.py` does count it) and **no target buckets**.

Measured against A1-4's six families:

| family | key present | actually measured |
|---|---|---|
| per-asset level counts | yes | **yes** |
| cluster widths | yes | **yes** |
| collapse events | yes | **yes** |
| LIS distances | yes | **yes** |
| maturity-withheld fractions | yes | **NO — hardcoded 0.0** |
| window ages | yes | **yes** |
| family-cap binding | — | **NO — absent** |
| target buckets | — | **NO — absent** |

**Waiting out the week does not fix this.** On 2026-08-22 the corpus will hold seventy hardcoded
zeros, no cap-binding counts and no bucket records, and three of the six threshold families BR-2
is contracted to recalibrate will have **no measured support at all**. Every morning that passes
writes another useless row.

**NOT FIXED HERE, deliberately.** The remedy is a small patch to `scripts/oracle_daily.py` — a
BR-1-owned file, outside this paste's "execute BR-2" scope, and one whose sha256 the top-up
pins, so it would force a re-pin exactly as the A2 rename did. **This is an operator decision and
it is the one on this page that has a clock on it.** The cheapest version is: compute
`maturity_withheld_fraction` from `analytics.vwap.maturity`, add a family-cap binding count, add
target buckets, re-pin the top-up in the same commit, re-run the fixtures.

**C-1 · THE PASTE'S PREMISE AND THE REPO DISAGREE.** The instruction was addressed to a session
"after 7 mornings + your PARITY line relayed". The repo says day one. Nothing was forced to fit
the premise; the gates were read against the real state and reported. If seven mornings *have*
elapsed on your side and the estate simply did not accrue them, that is a separate and more
serious problem — the launchd agents would not be firing — and the first thing to check is
`launchctl print gui/501/com.naiad.oracle-0700` for a rising `runs` count.

**C-2 · T-3 REMAINS OPEN**, unchanged by this paste: a laptop asleep at 06:45 fetches on wake,
possibly after the 07:00 Oracle has rendered. A2-7's staleness banner reports the condition; it
does not resolve the wake-order race. Relevant here because a sleeping machine is also how a
seven-morning week silently becomes a three-morning week.

**C-3 · V-7 REMAINS APOLLO'S**, unchanged: the rails, `min_stop_atr` 0.5 in the engine config
versus 1.0 on the TC3 card, is ruling F-C3-e. The Oracle uses 1.0 per BR-1 C-6.

---

## 6 · DISPOSITION

BOX constants by import from `publish_exchange` (`BOX_BYTES` 16,000,000; `FLAG_BYTES` 64,000).
Warn at 40%, refuse ABOVE 70%; the wire flags files strictly over 64,000 B.

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `exchange/reports/ORACLE_CHAIN_CLOSE_2026-08-16.md` | yes | yes | publish | yes | publish guard, `exchange/**` scope | this file |
| `exchange/status/LEDGER_ARGUS.md` | yes | yes | publish | yes | same, append-only | +~1.3 KB |
| `exchange/queue/2026-08-16_BR2_…_ARGUS.md` | yes | yes | publish | yes | publish guard; **body untouched, `AMENDMENT A-BR2-1` appended, still `BUILT: PENDING`** | +1,227 B |
| `briefs/oracle/oracle_2026-08-16.html` | yes | no — gitignored | — | — | residency block, F-BR-9 | 233,224 B OFF-BUS |
| `research_outputs/oracle/**` | yes | no — gitignored (2 exceptions) | — | — | same | OFF-BUS |
| `~/Library/LaunchAgents/com.naiad.oracle-*.plist` (4) | yes | no — outside the repo | — | — | CADENCE registry | unchanged |

**No code changed in this paste** — `git status` shows no modification under `scripts/` or
`research_outputs/oracle/`, and `posture_canon.json` is byte-identical to its HEAD blob. No R2
HTML was produced, so there is nothing local to delete; the rollback is a `git revert` of the
publish commit alone, which also removes `AMENDMENT A-BR2-1`.

### 6.1 BOX-COST
This paste adds roughly **5 KB to the bus at 16,000,000 B** — this report and the ledger append.
Nothing produced is over the 64,000 B naming wire.

---

## 7 · WHAT THIS PASTE IS NOT

Not a recalibration — there is no week to recalibrate against. Not a parity verdict — the
operator's line has not been relayed. Not an R2 build — parity is not green, and BR-2 gates R2
behind it explicitly. Not a BUILT stamp on BR-2. No threshold was adopted, proposed or fitted.
No census scoring, no Pine change, no sizing.

— HEPHAESTUS, 2026-08-16. Gates read against the real repo state and reported unmet.
