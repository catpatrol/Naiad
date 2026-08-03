# BRIEF-2 — CYCLE 2 SESSION SUMMARY AND DECISION REQUEST

**Lane:** ARGUS · **Builder:** HEPHAESTUS · **Date:** 2026-08-03
**Contract:** CONTRACT v4 Amendment 2 · **Branch:** `v12-v1-census` · **Reviewer:** ARGUS

---

## HOW TO READ THIS

**Read §1 and §2 before §6.** Five decisions are requested. Two of them look
like tuning knobs and are not — they change what the instrument *means*.

This is an **INTERIM** summary: the stage-G scope valve was exercised, so the
render is deferred to cycle 3 rather than pushed through at the end of a very
large cycle. §5 says exactly what is left.

**The framing sentence, unchanged from cycle 1.** This build produces an
instrument that *displays agreement between tools*. It cannot produce evidence
that agreement predicts anything. When you review a decision below, the question
is not "is this most useful" but "does this let a display artifact start
behaving like evidence".

---

## §1 · WHERE THIS CYCLE STARTED

Cycle 1 built stages 0–6 and left four reviewer rulings (D-1..D-4), one reviewer
finding (R-1), and three operator rulings to execute. All ten were carried out.
Two of them turned out to be **wrong as literally specified** — not wrong in
intent, but unachievable as written — and both are explained below, because
those are the two places where I changed something the contract did not
literally authorise and you need to agree with the reasoning.

Suite went **114/1 → 229 passed / 1 skipped** across the two cycles.

---

## §2 · WHAT HAPPENED THIS CYCLE, IN PLAIN LANGUAGE

### 2.1 An indicator that had never once produced a number

You asked me to mutation-test the original 21 causality fixtures, because I had
shown the *new* five were vacuous and you suspected the old ones shared the flaw.

They mostly did not — 19 of 21 caught their mutant. But the two that failed
uncovered something worse than a weak test: **`stoch_rsi` returned all-NaN on
every input, always.** 100% of StochRSI values in the previous capture were
null, across every asset and every timeframe. It is one of the four oscillators
the contract commissions, and it had never worked.

The fixture could not catch it because an all-NaN series satisfies
`NaN == NaN` at every truncation point. **A guard that cannot fail is not a
guard.** There is now a fixture asserting each series function actually
*produces numbers*, which is the property the causality test silently assumed.

Cause: `sma` is cumsum-based, so a single leading NaN poisons everything after
it. I fixed it inside `stoch_rsi` rather than in `sma`, because making `sma`
NaN-tolerant would move every other consumer's published numbers.

**I also have to report that my own audit harness was wrong the first time** —
it reused stale bytecode and reported three failures instead of two, one of them
entirely fictitious. That is the second harness bug in this project. Nothing was
reported until it was rebuilt and every verdict re-derived.

### 2.2 A stop that could never survive, and a floor that could never pass

Your R-1 finding was right: R:R is reward ÷ risk, so the *tightest* stops score
highest, and the top of the board was a 0.096-ATR invalidation scoring 11.23.

I added the floor you asked for (0.25 ATR). **It excluded every row on every
asset.** Investigating why produced the second finding: the contract says
invalidation is *"beyond the cluster's far edge"*, and it was implemented *as*
the far edge. Since clusters are bounded by 0.15 ATR from their own mean, a
far-edge stop can **never** reach 0.25 ATR. **A floor no geometry can satisfy is
an off switch, not a filter.**

Moving invalidation to one cluster-tolerance *beyond* the far edge — reusing an
already-ratified number rather than inventing one — makes the board sane:
R:R falls from 11.23 to **1.35–2.35**, invalidations land at 0.244–0.276 ATR,
and the floor now excludes 2 of 12 rather than 12 of 12.

**The 11.23 was a symptom, not a separate bug.**

### 2.3 The volume filter demonstrably moves the lines

The headline number the contract asked for:

> **A line in the sand moved on 10 of 10 assets, on 20 of 20 sides.**
> Median move **0.127 daily-ATR**; largest **0.946**.

That is the whole point of the dual-scoring design, measured on real data. It
says volume evidence changes where the operator's decisive levels sit — on every
asset in the basket. It says **nothing** about whether that helps; that is census
work under G-7.

### 2.4 A marking that had become an error

The LIT known-wrong marking existed because early LITUSDT history is a different
asset. I audited the estate directly: the floor is respected, coverage is
**100.00%** with zero gaps, and the 14 zero-volume bars are scattered no-trade
minutes — not padding. (My first pass called them a "padding signature"; that
was too crude and I corrected it.)

LIT has **222 days of correct data**. A percentile over 222 days is a correct
percentile over a short sample, not a wrong one — and **marking correct data as
wrong trains the reader to ignore markers**. The marking is withdrawn; the
shortness is still disclosed by the `warming` chip and by the sample size.

### 2.5 The two briefs can no longer disagree

`daily_brief.py` had its own private resample that did not inherit the closed-bar
rule. It now routes through `analytics`. **Published v1.1 values shift** — RSI on
12h moves by up to 6.4 points, daily ATR on BTC from 1,638 to 1,700 — because
mid-period a resampled oscillator was reading a fraction of a period as the whole
one. That is the correction, not a regression, and it is disclosed rather than
absorbed quietly.

---

## §3 · FINDINGS

| id | what | status |
|---|---|---|
| **F-2R-A** | `stoch_rsi` all-NaN on every input; 100% null in the capture | **FIXED**, analytics → 1.3.0 |
| **§7.2 conformance** | invalidation sat ON the far edge, not beyond it; made the R-1 floor unsatisfiable | **FIXED** |
| **F-1R-B** | `daily_brief.py` private resample | **FIXED** (D-3) |
| **LIT marking** | obsolete; correct data marked wrong | **WITHDRAWN** on evidence |
| **F-1R-C** | σ-band arithmetic duplicated inline | **NOT FIXED** — ruling D-4, leave pinned until parity |
| **INTERFACE.md** | stale: predates 1.3.0, the dedupe, and the §7.2 change | **NOT FIXED** — cycle 3 |
| **push scope** | publishing carries the whole branch | **ROUTED TO ATHENA**; operator accepted the state |

---

## §4 · NUMBERS YOU SHOULD SEE

| | before | after |
|---|---|---|
| registry per asset | 43–67, three families empty | **93–117, all five populated** |
| top R:R row | 11.23 at 0.096 ATR | **2.35 at 0.263 ATR** |
| StochRSI values | 100% null | finite everywhere |
| capture size | 794,451 B | 1,425,913 B *(D-1 saved 18%; Part I roughly doubled it)* |
| projected storage | 888 MB/yr | **1,584 MB/yr** vs a 150–250 MB estimate |
| capture runtime | 117 s | **199 s** (budget ~15 min) |
| suite | 114 / 1 | **229 / 1** |

Registry is **still below** §5.3's ~180–200, because that estimate assumed prior
M/Q/Y anchors `daily_brief` does not compute. Reported, not padded to hit a
number.

---

## §5 · WHAT REMAINS — cycle 3

Stage-G scope valve exercised. Deferred, with nothing half-built:

- `scripts/brief_render.py` — Part I / Part II HTML from a stored capture
- `scripts/brief_note.py` — `/brief-note`
- chart-plane rendering (§3.5), and **F-B10** (render fidelity) + **F-B20**
  (Tier-2 degradation), which cannot be written until a renderer exists
- `analytics/INTERFACE.md` regeneration
- v1.1 retirement, which ruling D-3 ties to the render landing

The `/brief-render` and `/brief-note` commands **say plainly that these do not
exist yet** rather than pretending.

---

## §6 · DECISIONS REQUESTED

### **D2-1 · Storage: 1,584 MB/yr against a 150–250 MB estimate**

D-1's dedupe worked (−18%), but wiring Part I roughly doubled the capture, so the
total went **up**. Partitions remain tiny (23 MB/yr) — the panel design is fine.
The cost is tracked capture JSON.

| option | consequence |
|---|---|
| **(a) Accept and record** | Simplest. ~1.6 GB/yr of tracked JSON makes clone and bisect slower over time. |
| **(b) Externalise Part I** | Part I duplicates what `daily_brief` already emits. Capture would carry a reference + hash. Saves ~50%, but a capture stops being self-describing — which is the property that makes archives comparable. |
| **(c) Compress captures** (`.json.gz`, tracked) | ~80–90% saving on JSON, no schema change, still self-describing. Costs: no longer diffable in git, and `jq` needs a decompress step. |
| **(d) Trim the layers** | Decide which of `cross_state`, `chart_planes`, `oscillators` need to be *stored* vs recomputed on render. |

**Recommendation: (c), then revisit (d) after the render exists.** Compression
keeps every property that matters (self-description, one file per capture,
tracked) and costs only diffability, which nobody uses on a 1.4 MB machine-written
JSON. I did not do it unilaterally because it changes the artifact's on-disk form.

### **D2-2 · The R-1 floor: re-ratify 0.25 against the measured distribution?**

Measured `inval_atr`: min 0.244, p25 0.257, median 0.263, p75 0.272, max 0.276 —
a very tight band, because invalidation is now mechanically
`cluster half-width + 0.15 ATR`.

| option | consequence |
|---|---|
| **(a) Keep 0.25** | Excludes 2 of 12. But the distribution sits so close to the floor that small cluster-width changes will flip rows in and out. |
| **(b) Lower to ~0.20** | Nothing excluded; the floor becomes decorative. |
| **(c) Raise to ~0.30** | Excludes nearly everything again. |
| **(d) Re-derive invalidation instead** | The real issue may be that invalidation is *mechanically* derived from cluster width, so `inval_atr` has almost no spread. A stop based on structure (e.g. beyond the nearest opposing level) would vary meaningfully. |

**Recommendation: (a) for now, and put (d) on the cycle-3 list.** Per your ruling
D-2 I have re-ratified nothing. But I want to flag that a threshold applied to a
quantity with a 0.03-ATR spread is not really filtering — it is thresholding
noise, and (d) is the honest fix.

### **D2-3 · Registry is 93–117, not §5.3's 180–200**

The gap is prior M/Q/Y anchored VWAPs, which `daily_brief` does not compute
(it does developing W/M/Q/Y only).

| option | consequence |
|---|---|
| **(a) Add prior M/Q/Y anchors** | Reaches ~140–160; matches the contract's model of the registry. New computation in the capture path. |
| **(b) Accept 93–117 and amend §5.3** | The estimate was made before the layers existed. Cheapest. |
| **(c) Leave and decide after the render** | — |

**Recommendation: (b).** The number in the contract was a forecast, not a
requirement, and thresholds are being re-ratified against measurement anyway.

### **D2-4 · F-B15 exceptions — is the doctrine chip acceptable?**

Wiring Part I brought v1.1's ratified `doctrine_chip` into the capture:
*'playbook 5.5: "half size, Z1/Z2 only, grade ≤ B"'*. It contains the words
"half size".

The contract's literal F-B15 is **zero KEYS**, and the key scan passes with **no
exceptions**. My stricter value scan now carries two enumerated exceptions (this
chip; the phrase "sample size"). **I did not widen the regex to make the failure
disappear.**

| option | consequence |
|---|---|
| **(a) Keep the exception** | The chip is the operator's own doctrine label, not the brief prescribing size. |
| **(b) Strip the chip from BRIEF-2 captures** | Firewall-purest, but edits the operator's doctrine out of his own report. |
| **(c) Reword the chip in v1.1** | Touches ratified v1.1 output for a cosmetic reason. |

**Recommendation: (a).** Naming which playbook rule applies is not sizing advice.
Flagged because it is a firewall-adjacent judgement and yours to confirm.

### **D2-5 · Parity — the tool is ready and waiting**

`scripts/parity_check.py` is built and demonstrated. It takes
`(symbol, timeframe, candle_open_utc, measure)` and prints our value, the exact
bar evaluated, and the pinned recipe. Asking for a forming bar returns
`exact_candle_match: NO` with the reason, so the most common false mismatch
explains itself.

It applies **no tolerance and emits no pass/fail** — what counts as a match is
the operator's call, not the builder's.

**No action from me is possible.** When the chart captures arrive the comparison
is one paste. This is the gate everything waits behind — CENSUS-1d, H-RVX,
H-M1X and H-VAN included.

---

## §7 · FIREWALL

Not a signal service. Not sizing advice. Not study evidence. No engine change.
No forward scoring. No lockbox read for scored evidence. No fitted weights. No
estate mutation.

Confluence scores measure **agreement between tools**, not edge. R:R measures
**geometry**, not probability. **Adoption remains gated on parity.**

---

## §8 · PROVENANCE

`analytics` **1.3.0** · sha `da81034d…c731` · `rules_version` **2.0.0** ·
`schema_version` **2.1.0** · capture sha `3c65e44b…c7ad` ·
suite **229 passed / 1 skipped**.

Commits: `6313807 · cc0003d · 9db5fc9 · d622b20 · 0ab827d`.

Paired artifact: `BUILDERS_REPORT_ARGUS_2026-08-03_BRIEF2_C2.md`.

— HEPHAESTUS, 2026-08-03
