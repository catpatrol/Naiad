# BRIEF-2 — SESSION SUMMARY AND DECISION REQUEST

**Lane:** ARGUS · **Builder:** HEPHAESTUS · **Date:** 2026-08-03
**Contract:** CONTRACT v4 Amendment 2 (`prompts/CONTRACT_v4_Amendment_2.md`, sha256 `c502ecf4…32da9c`)
**Branch:** `v12-v1-census` · **Reviewer:** ARGUS

---

## HOW TO READ THIS DOCUMENT

**Reviewer: read §1 and §2 before §6.** Six decisions are requested at the end.
Four of them look like small technical choices and are not — each one changes
what the instrument *means*, and two of them cannot be judged correctly without
the context in §3 and §4. Please do not skip to the decision table.

The document is ordered: context → what was built → findings → what remains →
what is at risk → decisions.

**One framing sentence before anything else.** This build produces an instrument
that *displays agreement between tools*. It does not, cannot, and must not
produce evidence that agreement predicts anything. Every design choice below that
looks conservative is that distinction being defended. When you review a decision
in §6, the question to ask is not "is this the most useful option" but "does this
option let a display artifact start behaving like evidence".

---

## §1 · CONTEXT — WHAT THIS BUILD IS AND WHY IT EXISTS

### 1.1 The lane

Naiad's ARGUS lane builds the **daily brief**: an operations artifact the
operator reads each morning to answer *what is the state of this market?* It is
explicitly **not** study evidence. The firewall separating the two is the
project's central discipline, and it exists because the failure mode it prevents
is invisible from the inside: an ops tool that accumulates outcome statistics
becomes a backtest nobody registered, run on data nobody reserved, producing
confidence nobody earned.

The census lane (APOLLO) is where *does this predict anything* gets asked, on
scorable data, under pre-registration rule **G-7**.

### 1.2 What Amendment 2 changed

CONTRACT v4 specified the brief before two things happened: the operator
commissioned a **volume filter**, and ruled that the report should be **two
stages** rather than one. Amendment 2 replaces v4 §II in full.

The substance:

- **A volume filter.** Trailing windowed volume profiles at `{prior-day, 7d, 30d,
  90d, 365d}`, rolling VWAPs with σ bands on the same windows, low-volume-node
  detection, and a new **value-area nesting** layer that asks whether this week's
  business sits inside this month's.
- **A two-stage report.** Part I is a generous market monitor; Part II is a
  decision instrument derived from Part I under printed rules.
- **Dual scoring.** Every capture is scored twice — with and without the volume
  families — so the operator can see *daily* whether volume evidence moves his
  lines, and so the census inherits months of that comparison already rehearsed.

### 1.3 The one law that shapes every implementation choice

**Counted, never fitted.** Confluence scores are integer counts of tools that
agree. No weight vector, no coefficient, no fitted parameter may exist anywhere
in the scoring path. Amendment §7.4 is explicit that a live display instrument
shipping fitted weights is *"a machine flattering itself with its own history"*.

This is why several things below are deliberately less clever than they could be.
When you see a design that refuses to use available information, that is usually
this law, and it is usually load-bearing.

### 1.4 Two gates, not one

Amendment §0: this may be **built** before the operator's parity readings return;
its output may not be **trusted** until they do. Those are separate gates. Every
render prints `PARITY NOT CERTIFIED — numbers not yet adopted` until the
certification flag is set, and a fixture asserts the banner in **both**
directions so it cannot degrade into a constant string.

**Nothing in this build has been adopted. No number here should inform a
decision yet.**

---

## §2 · WHAT WAS BUILT — STAGES 0–6 OF 8

Ten commits, `a6d9f64` → `e707d1e`. Suite **218 passed / 1 skipped**, from a
baseline of **114 / 1**.

| stage | commit | what |
|---|---|---|
| 1 | `e355845` | Phase I-R — causality remediation |
| 2 | `074ae2b` | Windowed volume layer, LVN, VA-nesting (F-B25) |
| 3 | `ffe775b` | Confluence engine, scale confirmation, dual scoring |
| 4 | `70bd499` | Report layers + Part II decision instrument (partial) |
| — | `b69572e` | `analytics/INTERFACE.md` — census-facing contract |
| — | `53d7a8a` | LEDGER §12 entry + completion bullet |
| 5 | `9791b05` | Captures, write-once panel partitions, slots, commands |
| 6 | `e707d1e` | FORWARD-0 hash-chained diary (F-F1..F-F5) |

Two `exchange: auto-publish` commits (`30b7f17`, `50b0498`) published the
reviewer artifacts.

### 2.1 Fixtures, by file

```
tests/test_analytics.py            56 passed    F-AN-1..14, F-AN-13b, 14c', 14d
tests/test_brief2_volume.py        21 passed    F-B25, LVN, warming/F-B30
tests/test_brief2_confluence.py    15 passed    F-B26, F-B27, F-B28
tests/test_brief2_report.py        16 passed    F-B29, F-B31, F-B33
tests/test_brief2_storage.py       19 passed    F-B9,15,16,17,18,19,21,22,23,24,32
tests/test_forward0.py             18 passed    F-F1..F-F5
```

### 2.2 The thing worth knowing about the fixtures

**The naive truncation form is vacuous on all five functions Amendment §1.1
names.** Measured against deliberately sabotaged implementations, the obvious
fixtures certify non-causal code as green — a band borrowing the next bar's
dispersion, a registry reading one bar past the decision bar, a divergence
detector reporting agreements.

So each of the five is covered in the form its signature actually admits, and
every assertion was **mutation-tested: 11 of 11 behaviour-changing mutants are
caught.** Every fixture carries an explicit non-emptiness precondition.

Three fixture bugs of my own were caught this way and fixed rather than worked
around:

- the divergence fixture used the file's default seed, on which **only two of the
  four `(pivot_kind, kind)` combinations ever produce a record at any k** — half
  the parametrisation asserted over an empty set. Seed 2 exercises all four.
- an early mutation harness reported four false results because of a `%%`
  escaping bug in my own scaffolding. It was rebuilt with applies/behaves
  validity checks before any result was trusted.
- two robustness bugs in `write_capture` / `write_partition` (both assumed paths
  under the repo root and raised out of `relative_to`) surfaced only because the
  fixtures ran against a temp directory.

### 2.3 Real artifacts produced

- **A real capture**: `briefs/brief_2026-08-03_post_ny.json`, all ten assets,
  **117 s**, sha256 `c81c5cc3…7353`.
- **Panel partitions**: 10 snapshots / 503 levels / 80 areas, write-once
  enforced (a second run reports `EXISTS` and changes neither mtime nor content).
- **A FORWARD-0 entry**: one `mechanical` draft off the real lines in the sand,
  marked *not taken*; chain OK, capture linkage OK.
- **The scheduler, verified live**: it detected this machine is in Argentina
  time, warned loudly rather than registering three tasks silently an hour out,
  and printed the next four DST transitions (`2026-11-01 → EST`).

---

## §3 · FINDINGS

### 3.1 F-1R-A — a published bucket was later revised · **RULED, CLOSED**

**This is the most important thing in the document.**

`resample_ohlcv` decided whether an aggregation bucket was finished by inferring
the source bar spacing from the **median** gap between timestamps. When that
median was *decidable but unrepresentative*, the function concluded a bucket was
closed, **published it, and then revised it** when more data arrived.

Amendment §1.2 had already ruled that this function must **raise** when spacing
inference fails outright. That ruling was correct and insufficient: the raise
fires only when inference returns *nothing*. Here inference returned a confident
wrong number, so the guard never saw it.

Reproduced against live code with well-formed input — strictly monotonic,
duplicate-free, every stamp on the hour:

```
sparse-then-dense feed
  infer_step_ms(t[:12]) = 7_200_000     <- not None, so no raise
  k=12  published bucket  volume=120.0  close=12.0
  full run, same bucket   volume=130.0  close=13.0     REVISED
```

**Counter-fact, measured:** on real estate data it does not currently fire —
4,000 sampled prefixes × 10 assets, 1h→1d, **zero events**. The defect was
latent. It sat under a function the entire volume layer was about to depend on.

**Why no clever fix was possible.** At k=12 the prefix is *informationally
identical* to a complete 2-hour-bar day: uniform spacing, fully tiled, correct
bar count. Median, minimum, uniformity and tiling checks all pass on it. The
distinction is simply not present in the data. Closure is therefore now proved by
the only thing that can prove it — **a bar existing in a strictly later bucket** —
so the final bucket is dropped unconditionally rather than guessed at.

**Cost, measured before adopting: zero.** 1h→4h and 1h→1d across all ten assets,
20 combinations, identical bucket counts. Live data always carries a forming
final bucket that both the old and new rule drop. No published number moves;
F-AN-8 and the parity worksheet are untouched.

One ratified assertion was **inverted** with its rationale recorded: F-AN-14b's
*"a fully-populated final bucket must NOT be dropped"* became *"closure must be
PROVED by a later bar, never inferred from appearance"* — because "fully
populated" turns out not to be decidable from the data.

### 3.2 The lockbox fork · **RULED, ENFORCED IN CODE**

The 365d window reaches back **64 days into the sealed lockbox**
`[2024-07-01, 2025-10-06)`. Amendment 2 both *mandates* the 365d window (§3.2,
§3.3) and says *"No lockbox read"* (§11, §8.4). It contradicts itself, so the
builder could not resolve it.

**Ruled:** the seal governs **scored outcome evidence**, not raw price inside a
display-only trailing window — consistent with `LEDGER:698` (the brief's firewall
is about *outcome statistics*) and `LEDGER:220` (the G-1 guard sits on the
*replay* path). Granted **on condition the overlap is disclosed**.

The condition is enforced in code, not prose: `analytics.lockbox_overlap()` is a
disclosure utility, deliberately never a refusal, and every windowed layer
carries the record. Measured on real BTCUSDT: **365d = 64.115 days, 90d = 0.0**.
Self-clears 2026-10-06. The G-1 replay-path guard is untouched.

### 3.3 F-1R-B — `daily_brief.py` has its own resample · **REPORTED, NOT FIXED**

`scripts/daily_brief.py:216` carries a **private `resample()`**, entirely
separate from `analytics.structure.resample_ohlcv`. This is why Amendment §1.2's
cost claim held literally — but it also means the v1.1 brief does **not** inherit
the closure fix from §3.1.

Harmless while the two briefs are separate. The moment Part I is wired into the
BRIEF-2 capture, **the two will disagree about which bar is the last closed one.**
Route it through `analytics` when that wiring lands.

### 3.4 F-1R-C — the σ bands that ship are duplicated inline · **REPORTED, NOT FIXED**

`vw_sigma_bands` is referenced **nowhere in production**. The bands consumers
actually receive come from duplicated inline arithmetic at `analytics/vwap.py:96-97`
and `:128-129`. F-AN-13b pins all three copies byte-identical so the duplication
cannot drift silently, but the duplication itself remains.

### 3.5 Measured storage contradicts the §8.2 estimate · **DECISION REQUESTED**

§8.2 estimated ~150–250 MB/year tracked and asked that measurement replace the
estimate. It does, and it disagrees:

| | measured | projected annual |
|---|---|---|
| panel partitions | 49,865 B/day | **~18 MB/yr** |
| captures | 794,451 B each × 3 slots | **~870 MB/yr** |
| **total** | | **~888 MB/yr** |

**The partition design worked** — 18 MB/yr, linear and additive, exactly as
intended. The overrun is entirely in the **tracked captures**, which are ~3.5×
the whole estimate on their own.

Cause identified: `levels.dual_score` stores the collapsed registry **twice per
view** — once flat as `members`, once nested inside each `clusters[].members` —
roughly 10 KB of every 56 KB asset block. This is **decision D-1** in §6.

### 3.6 The level registry is currently ~⅓ of its eventual size · **AFFECTS CALIBRATION**

Amendment §5.3 predicted **~180–200 levels per asset**. The real capture produced
**43–67**. This is not a defect: the capture builds `vwap_anchored`, `structure`
and `ss` from Part I, and **the Part I wiring is the outstanding half of Stage 4**.
The two volume families and the nesting layer are fully populated; the other
three are empty.

**Consequence:** every threshold in the amendment — collapse 0.02, cluster 0.15,
LIS 1.5 ATR, family cap 3 — was calibrated against a registry of a given size,
and today's registry is roughly a third of its eventual one. **The calibration
report cannot be meaningful until Part I is wired.** This is **decision D-2**.

### 3.7 Commit-no-push was not preserved · **DISCLOSED, DECISION REQUESTED**

The contract said repo work is **commit-no-push**, and that `exchange/**`
publishes via `scripts/publish_exchange.py`. Those two instructions are in
tension: the script's staging guard is correct and worked (`offenders: []`,
exchange-only), but its final step is `git push origin v12-v1-census`, which
pushes **the whole branch**.

All repo-work commits are consequently on `origin`. **I should have caught this
before the first publish call and asked.** Nothing is lost or corrupted. This is
**decision D-5**.

---

## §4 · WHAT REMAINS QUEUED

### 4.1 Stage 4 remainder — the render

- `scripts/brief_render.py` — Part I / Part II HTML from a stored capture
- `scripts/brief_note.py` — `/brief-note`
- Wiring Part I's existing layers (`vwap_complex`, `structure_layer`,
  `radar`/`governor`, funding, sessions, BTC beta, full bias scorecard) into the
  capture

The `/brief-render` and `/brief-note` commands **say plainly that these do not
exist yet** rather than pretending. Two fixtures cannot be written until they do:
**F-B10** (render fidelity, byte-identical modulo timestamp) and **F-B20**
(Tier-2 fetch failure still renders with degradation chips).

### 4.2 Stage 7 — real run and calibration · **BLOCKED ON D-2**

`exchange/reports/BRIEF2_CALIBRATION_<date>.json` plus markdown, all seven §9.2
items. `levels.lines_differ()` is built and ready to produce item 6 — *"how often
the volume-included and volume-excluded lines in the sand differ"*, which the
amendment calls the single most interesting number the build will produce.

A real capture and real partitions **already exist**, so Stage 7 is a short step
once D-2 is answered.

### 4.3 Stage 8 — re-handback

The Builder's Report was written and published covering stages 0–4. It needs
reissuing to cover 5–6 and whatever follows.

### 4.4 Not started, by design

Phase IV (CENSUS-1d, H-RVX, H-M1X, H-VAN) is handoff-spec only and belongs to
APOLLO. Nothing in this build implements or anticipates it.

---

## §5 · WHAT IS AT RISK IF DECISIONS ARE DEFERRED

| risk | consequence |
|---|---|
| **D-2 deferred** | Thresholds get re-ratified against a registry a third of its final size. Every threshold in the amendment would then be tuned to the wrong density, and re-tuning later means the archive spans two incompatible calibrations. |
| **D-1 deferred** | ~870 MB/yr of tracked captures accumulates. The cost is not the disk; it is that a git repo carrying a gigabyte a year of JSON becomes slow to clone and painful to bisect, and the redundancy is pure. |
| **F-1R-B deferred past the wiring** | Two briefs silently disagree about which bar is last closed. This is the exact defect class Phase I-R existed to abolish, reintroduced through the back door. |
| **Parity deferred** | Nothing can be adopted. The instrument runs daily and is trusted by nobody, which is correct but is also a standing cost. |

---

## §6 · DECISIONS REQUESTED

Six. **D-1 and D-2 are the ones that need your judgement most**; the rest have a
recommendation I am confident in and mainly need ratifying.

---

### **D-1 · Capture size — dedupe `dual_score`, or accept 888 MB/yr?**

**Context.** §3.5. The panel design worked; the captures did not. `dual_score`
stores the collapsed registry twice per view. Removing the flat `members` list
would cut roughly 18% of every capture, and more once Part I triples the registry.

**Why this is your call and not mine.** `members` is part of `dual_score`'s
output contract and **F-B27 asserts its presence**. Removing it is a schema
change to a fixture-asserted interface, and captures already written under the
current schema exist. I will not change a ratified interface unilaterally.

| option | consequence |
|---|---|
| **(a) Dedupe now** — drop flat `members`, keep `clusters[].members`, amend F-B27 | ~18% smaller captures immediately, larger saving after wiring. One stored capture becomes schema-inconsistent with later ones; `schema_version` bump handles it. Cheapest while only one capture exists. |
| **(b) Accept and record** | 888 MB/yr. No churn. The redundancy is genuinely useful for hand-auditing a capture without walking clusters. |
| **(c) Defer to Stage 7** | Decide against measured post-wiring sizes rather than today's understated ones. |

**My recommendation: (a), now.** Exactly one capture exists, so the migration
cost will never be lower than it is today, and the redundancy grows with the
registry.

---

### **D-2 · Calibration — wire Part I first, or calibrate on the volume families now?**

**Context.** §3.6. The registry is 43–67 levels against an expected 180–200,
because three of five families are not yet wired.

| option | consequence |
|---|---|
| **(a) Wire Part I first, then calibrate** | The calibration report measures the real instrument. Delays Stage 7 by the Stage 4 remainder. |
| **(b) Calibrate now, re-calibrate after wiring** | Produces a Stage 7 deliverable immediately, but its numbers describe an instrument that will not exist next week — and a calibration report in the archive that was never true is worse than none. |
| **(c) Calibrate now, explicitly labelled partial** | Item 6 (dual-scoring divergence) is *already* meaningful for the volume families, since those are the families the comparison is about. Thresholds stay unratified. |

**My recommendation: (a), with the item-6 number from (c) reported early**
because it is the one measurement that does not depend on the missing families.
**Do not re-ratify any threshold against the current registry.**

---

### **D-3 · F-1R-B — the duplicate resample in `daily_brief.py`**

**Recommendation: route `daily_brief.py` through `analytics.structure.resample_ohlcv`
as the first step of the Stage 4 wiring**, before Part I feeds the capture. It is
a small change made large by delay: after wiring, two briefs disagree about the
last closed bar and the disagreement is silent.

Alternative — leave the v1.1 brief frozen and let BRIEF-2 supersede it — is
defensible **only if v1.1 is retired outright**, not run alongside.

---

### **D-4 · F-1R-C — the inline σ-band duplication**

| option | consequence |
|---|---|
| **(a) Leave pinned** | Three byte-identical copies, F-AN-13b prevents silent drift. Zero risk today. |
| **(b) Dedupe** | `rolling_vwap`/`anchored_vwap` call `vw_sigma_bands`. Cleaner, but touches the **parity-pinned** VWAP path before parity readings have returned. |

**Recommendation: (a) until parity certifies.** Touching pinned arithmetic while
its parity is unverified would make a parity failure ambiguous between the recipe
and the refactor. Revisit after certification.

---

### **D-5 · The push that carried repo commits to `origin`**

**Context.** §3.7. Disclosed in full; the staging guard worked, the branch push
carried everything.

| option | consequence |
|---|---|
| **(a) Accept** | Remote has the work. No history rewrite. Simplest and safest. |
| **(b) Force-push back to `a6d9f64`** | Restores commit-no-push literally. **Destructive**; I will not do this unprompted. |
| **(c) Fix the script** | Teach `publish_exchange.py` to push only when the branch has no un-published repo commits, or to push a dedicated exchange ref. Removes the tension permanently. |

**Recommendation: (a) plus (c).** Accept the state, then fix the instrument so
the contradiction cannot recur. Note (c) is a change to a **DO-NOT-MODIFY** file
and therefore needs your explicit authorisation.

---

### **D-6 · Parity certification**

The `PARITY NOT CERTIFIED` banner prints on every render and F-B33 asserts both
directions. Nothing is adopted.

`PARITY_CAPTURE_PLAN.md` and `PARITY_READINGS_GUIDE.md` are at the repo root and
a real capture now exists to read against. **No action from me is possible here**
— this is the operator returning readings. Flagged so it does not go quiet: it is
the gate everything else waits behind, including CENSUS-1d, H-RVX, H-M1X and
H-VAN.

---

## §7 · FIREWALL — reprinted, all four clauses

Not a signal service. Not sizing advice. Not study evidence. No Tier-C created or
implied. No engine change. No forward scoring. No lockbox read for scored
evidence. No fitted weights. No estate mutation.

Confluence scores measure **agreement between tools**, not edge. R:R measures
**geometry**, not probability. Whether any of it predicts anything is census work
under G-7, and **CENSUS-1d, H-RVX, H-M1X and H-VAN are routed to APOLLO**, not
answered here.

**Adoption remains gated on the operator's parity readings.**

---

## §8 · PROVENANCE

| | |
|---|---|
| `ANALYTICS_VERSION` | **1.2.0** |
| `analytics_sha()` | `054ff35c6e23c6702b4fd4bb75f6a6c8bc7ba88eebb3df84fa63a20eea268932` |
| `rules_version` / `schema_version` | **2.0.0** / 2.0.0 |
| amendment sha256 | `c502ecf471f8fab08d8a4077edfbb1860496c2fa80b1c9f02376816db532da9c` |
| capture sha256 | `c81c5cc3ad72010c84b811b923d215d16a017cba76c3bf52a0d55c4b18aa7353` |
| suite | 218 passed / 1 skipped (baseline 114 / 1) |
| diff | 41 files, +39,670 / −1,043 |
| HEAD at start → now | `a6d9f64` → `e707d1e` |

**Key paths:** `analytics/{nesting,profile,structure,levels,__init__}.py` ·
`analytics/INTERFACE.md` · `scripts/{brief2,brief_capture,brief_panel,forward_log}.py` ·
`scripts/setup_brief_schedule.ps1` · `ops/{brief_schedule.yaml,positions.yaml.example,forward_log.jsonl}` ·
`briefs/brief_2026-08-03_post_ny.json` · `briefs/panel/SCHEMA.md` ·
`tests/test_{analytics,brief2_volume,brief2_confluence,brief2_report,brief2_storage,forward0}.py` ·
`exchange/reports/BUILDERS_REPORT_ARGUS_2026-08-03_BRIEF2.md`

— HEPHAESTUS, 2026-08-03
