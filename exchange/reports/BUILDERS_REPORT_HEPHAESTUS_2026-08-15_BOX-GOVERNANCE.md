# BUILDERS REPORT — HEPHAESTUS · 2026-08-15 · BOX GOVERNANCE

**Task:** box-governance transfer implementation · **Operator go** 2026-08-15 (*"edit these limits to proportions reasonable to new capabilities"*) · **Basis:** `NOTE_APOLLO_2026-08-15_TO_ATHENA_box-governance-handoff.md` · **HEAD at start** `6f2c79a` · branch `v12-v1-census` · macOS, `~/Naiad`.

**Identity gate v2:** `pwd == $HOME/Naiad`, no cloud-tree marker, branch `v12-v1-census`, remote `catpatrol/Naiad`. All pass.

**§1.4 of the note — the named-constant protocol — governed this session, applied to itself.** Its three legs are run in §2 below and its dependents table is §3.

## 1 · THE HANDOFF'S FACTS, VERIFIED BEFORE GOVERNING ON THEM

Config location: **`scripts/publish_exchange.py:86-88`**.

| fact | note claims | verified | verdict |
|---|---:|---:|---|
| `BOX_BYTES` | 16,000,000 | 16,000,000 | **MATCH** |
| `WARN_FRACTION` | 0.50 | 0.50 | **MATCH** |
| `REFUSE_FRACTION` | 0.80 | 0.80 | **MATCH** |
| boundary | exactly 80.0% warns | exactly 80.0% → WARN | **MATCH** |
| `exchange/**` | 2,568,320 B / 16.05% | 2,598,669 B / 16.24% | delta **+30,349 B** |

**The byte delta is not a mismatch and is not governed around — it is accounted for.** The note's figure was measured before two later publishes landed on the bus; tracked `exchange/**` reads 2,550,554 B at `8e49527`, 2,571,952 at `905b9fc`, 2,574,270 at `8c26dcd`, 2,582,258 at `2925ebe` and 2,586,954 at `6f2c79a`. Every byte of the delta is attributable commit by commit. **The three governing facts — the constants — match exactly, so the session proceeds.** Had any constant differed, this report would end here.

## 2 · THE NEW THRESHOLDS — the protocol, applied to itself

### 2a · all three legs

**NAME** (`BOX_BYTES`, `WARN_FRACTION`, `REFUSE_FRACTION`, `BOX_CAPACITY`, `TICK_EXTRA`) · **VALUE** (`16000000`, `0.50`, `0.80`, and legacy `6390000`/`0.25`/`0.40`) · **THRESHOLD TEXT** (`warn at`, `refuse`, `25%`, `40%`, `50%`, `80%`) — across `scripts/`, `exchange/status/CONVENTIONS.md`, `tests/`.

**The third leg earned its place again.** The NAME grep is clean on `rotate_reports.py` — it imports. The **TEXT** grep caught its docstring asserting *"raised to 16 MB (warn 50%, refuse 80%)"* as current policy, which the recalibration makes false. One live site, invisible to two of the three legs.

### 2b · dependents table — pin-vs-import, per site

| site | holds | decision | why |
|---|---|---|---|
| `publish_exchange.py:86-115` | `BOX_BYTES`, `WARN_/REFUSE_FRACTION`, `TICK_EXTRA` | **THE ONE DEFINITION** | the guard itself |
| `census2b_report.py:31` | imports all three | **IMPORT** | live report; a copy here was already wrong by 2.5× once |
| `rotate_reports.py:195,237` | imports `BOX_BYTES` | **IMPORT** | live; both changes reached it for free — docstring prose corrected |
| `census2b_oracle_report.py:26` | `BOX_BYTES = 6_390_000` | **PINNED + labelled** | regenerates a FILED document; its `warn 25% / refuse 40%` text is self-consistent with the pin |
| `mc1_report.py:25` | `BOX_CAPACITY = 6_390_000` | **PINNED + labelled, as APOLLO left it** | regenerates the MC-1 document filed 2026-08-06 |
| `tests/test_box_guard.py` | derives edges from the constants | **DERIVE** | so the next re-pin re-tests itself |

*A historical report reproduces history.* Both pinned sites keep their 6.39 MB era intact and labelled; neither was touched by this pass beyond confirming the label.

### 2c · the thresholds, and the boundary

`WARN_FRACTION` 0.50 → **0.40** · `REFUSE_FRACTION` 0.80 → **0.70**. **Warn 6.4 MB · refuse 11.2 MB.**

The raise moved the ceiling but carried the fractions up proportionally from a 6.39 MB box. At 0.50/0.80 the first warning arrives at 8 MB — the bus would have tripled from here with nothing said. 0.40/0.70 warns while there is still room to act.

**Boundary semantics are the comparators, not the constants**, and they are unchanged: `frac > REFUSE` → REFUSE, `frac >= WARN` → WARN. So exactly 70.0% warns and does not refuse, exactly as exactly 80.0% did.

```
  BOX 16,000,000 = 16 MB   warn 0.40 = 6.4 MB   refuse 0.70 = 11.2 MB
   just under warn         39.99%    6.40 MB -> OK
   EXACTLY warn            40.00%    6.40 MB -> WARN
   just under refuse       69.99%   11.20 MB -> WARN
   EXACTLY refuse line     70.00%   11.20 MB -> WARN
   just over               70.01%   11.20 MB -> REFUSE
```

### 2d · the D3 metering gap, CLOSED

The box holds **`LEDGER.md` and `exchange/`** (DIGEST §1). The guard metered `exchange/` alone and under-reported true occupancy by the ledger's size — the gap ATHENA raised on 2026-08-11 and APOLLO transferred with the governance. **The thresholds now govern on the TICK SET.**

```
  exchange-only    2,598,669 B   2.60 MB  16.24%   [continuity]
  + LEDGER.md        255,011 B   0.26 MB   1.59 pts
  = TICK SET       2,853,680 B   2.85 MB  17.84%   [governs] -> OK
```

`TICK_EXTRA` is measured **at HEAD, not in the index**, deliberately: publish only ever commits `exchange/` — the scope guard forbids anything else — so reading the index would report 0 and silently re-open the gap. Both figures print on **every** publish, not only on warn/refuse, and every percentage carries its absolute MB, because a percentage against a ceiling that has just moved is exactly the number a reader mis-reads.

**No consumer was handed a silent redefinition.** `result["bytes"]` and `result["fraction"]` keep their historical exchange-only meaning; the governing values are new `tick_bytes` / `tick_fraction` keys, and `budget` derives from those. The REFUSE messages were moved to the tick figure too — a refusal that under-reported itself by the size of the ledger would be the gap wearing a different hat.

## 3 · F-BOX-1

`tests/test_box_guard.py`, **12 assertions, new** — the guard had no test at all, which is how a threshold can move and a boundary quietly invert.

```
tests/test_box_guard.py ............                                     [100%]
============================== 12 passed in 0.03s ==============================
```

Pins: the three constants · warn edge inclusive at exactly 0.40 · refuse edge exclusive at exactly 0.70 · all three levels reachable · **edges derived from the constants**, so a future re-pin re-tests itself · `TICK_EXTRA` declared and measuring a real tracked file · the tick set strictly exceeds exchange-only · both figures + MB in `budget_lines` · `report_lines` carries the tick set · **a REFUSE quotes the tick figure, not the scope figure**.

One assertion failed on first run and the test was wrong, not the guard: it expected 4 MB to WARN, but 4/16 = 25%, comfortably OK under a 40% line. Corrected and recorded rather than quietly amended.

**Suite: 226 passed / 0 failed / 0 skipped**, from 214 — **delta +12, all F-BOX-1.** (The task quoted 287/0/1 from the Mac-crossing note; that figure counted a different tree. The measured baseline on this branch immediately before this session was 214.)

## 4 · CONVENTIONS ADOPTIONS

**(a) §6.4 · The named-constant change protocol** — new numbered rule in the error-taxonomy neighbourhood, credited *APOLLO handoff 2026-08-15*, text per §1.4 of the note: grep NAME + VALUE + TEXT · per-site pin-vs-import recorded · *a historical report reproduces history*, with the `mc1_report.py` / `census2b_report.py` exemplar both ways. Added to the TOC and the body. Carries the corollary this week's defects earned: **after editing a document, re-read the document.**

**(b) §4.2 · Threshold custody** — one line: the ceiling, the fractions and the metered set are **ATHENA's**; changes route **ATHENA-first**; no lane edits them on its own authority; any such change runs §6.4.

**(c) §3.2 · Dated correction** — the raise paragraph asserted *"warn 25→50%, refuse 40→80%"*. Per the standing rule at the head of CONVENTIONS, **the correction REPLACES the assertion** — the sentence now states warn 40% / refuse 70% and the tick-set metering — and the dated note follows *beneath* it explaining what changed and why, quoting the old text rather than leaving it in place for a reader to meet first.

## 5 · DISPOSITION + BOX COST

| file | disposition |
|---|---|
| `scripts/publish_exchange.py` | thresholds 0.40/0.70 · `TICK_EXTRA` · `tick_extra_bytes()` · `budget_lines()` · dual-figure output |
| `scripts/rotate_reports.py` | docstring corrected; **no value change — it imports** |
| `tests/test_box_guard.py` | **new**, F-BOX-1, 12 assertions |
| `exchange/status/CONVENTIONS.md` | §6.4 adopted (TOC + body) · §4.2 custody · §3.2 dated correction |
| `exchange/reports/NOTE_APOLLO_…_box-governance-handoff.md` | **filed verbatim**, sha `e7cfae19…b7af` |
| `exchange/status/LEDGER_ATHENA.md` | acknowledgment appended |
| `scripts/census2b_oracle_report.py`, `scripts/mc1_report.py` | **untouched** — pinned historical |

### BOX COST — in both figures, as the metering now requires

**Tick set 2,853,680 B / 2.85 MB = 17.84%** of 16,000,000 B (16 MB) — **OK**, against warn 6.4 MB and refuse 11.2 MB. `exchange/` only: 2,598,669 B / 2.60 MB = 16.24%. Headroom to refuse: **8,346,320 B / 8.3 MB.** This document and the ledger append are the bulk of this paste; the four payload-scale artifacts of the day stayed local under `research_outputs/`, per pointer discipline.

---

*Class: infrastructure / governance transfer. No registrations. The guard now warns at 6.4 MB and refuses at 11.2 MB, meters the whole box rather than part of it, and has a fixture for the first time.*
