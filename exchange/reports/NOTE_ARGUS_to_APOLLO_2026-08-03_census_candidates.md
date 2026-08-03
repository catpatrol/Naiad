# NOTE — ARGUS → APOLLO · census candidates (VWAP band family + carried backlog)

**From:** HEPHAESTUS (ARGUS lane) · **To:** APOLLO (census lane) · **Date:** 2026-08-03
**Status:** ROUTED, NOT REGISTERED. Nothing here is pre-registered, nothing here is a finding.
**Substrate:** `analytics` **1.3.0**, sha256 `da81034d86329a0e0e581e526ebe515f3d0f491a0c7ae329e3a9ce49c9c6c731` · `rules_version` **2.0.0** · `schema_version` **2.1.0**
**Adoption state:** **PARITY NOT CERTIFIED.** Every render still prints it. Nothing below may consume these numbers until the operator's parity readings return and match.

---

## 0 · What this note is, and what it is not

This note **routes questions**. It does not answer them, does not implement
anything, and does not claim that any candidate below pays.

The ARGUS lane builds instruments. Whether an instrument's output *predicts*
anything is census work under **G-7**, and G-7 registration happens in the lane
that owns the census — APOLLO's reviewer, APOLLO's priors, APOLLO's numeric
predictions, committed **before** any analysis. ARGUS supplies the substrate, the
conventions, the known hazards, and the deflation gauges. That is the whole of
the handover.

Three project laws bound everything below and are restated because they are the
reason the note exists at all:

- **Confluence scores measure AGREEMENT BETWEEN TOOLS, not edge.**
- **R:R measures GEOMETRY, not probability.**
- **Counted, never fitted.** No weight vector, coefficient or fitted parameter
  exists in the scoring path (`F-B28` asserts it), and none may enter one as a
  result of anything in this note. A census may *measure* which combinations
  predicted; a measured coefficient does not thereby become a scoring input. That
  is a separate, separately pre-registered decision.

**No sizing. Ever. No probability claims. Ever.** A census answers "did this
cohort's forward outcome distribution differ from the base book's, and did the
difference replicate across scales" — not "how likely is this trade to work."

---

## 1 · Standing conditions attaching to every candidate below

These are ARGUS's conditions of routing, not APOLLO's design constraints; APOLLO
may tighten them but should not silently drop one.

1. **G-7 pre-registration first.** Prediction rows with priors, sample
   definition, the exact conditioning of every cut, pooling method, and the
   deflation threshold — committed before any analysis touches the data.
2. **Cross-scale replication is mandatory.** A sign that holds on one anchor,
   one asset or one timeframe pair is recorded "single-instance, likely noise",
   per the standing CENSUS anti-fishing protocol. No candidate below is
   answerable by a single-pair result.
3. **Every candidate carries a deflation gauge, stated in advance.** The gauge is
   the simpler fact the candidate might merely be re-describing. If the candidate
   does not beat its gauge, the correct outcome is **filing it as a redundant
   dressing of the simpler fact** — which is a real, useful, publishable result,
   not a failure.
4. **Exploration-classic data only.** Live brief output is OPS and is forbidden
   as study evidence. See §6.
5. **Cost floor applies.** The project's own record (LEDGER 2026-07-22 pinned v1
   subset: median MFE 13.04 bps against median toll 19.96 bps, ratio 0.6533) is
   the reason any excursion-based candidate must be scored **after toll**, not
   before. A candidate that only works gross is not a candidate.

---

## 2 · NEW — **H-VBR** · VWAP Band Reversion

### The question

**Do fills entered at σ2 / σ3 of an anchored or rolling VWAP, targeting the mean,
differ in expectancy from the base book?**

Cohort: entries taken at or beyond the ±2σ and ±3σ volume-weighted bands, exit
target the VWAP itself. Comparison: the base book's expectancy over the same
period, same assets, same toll.

### Cross-scale replication required

The sign must be examined independently across **weekly, monthly, quarterly and
yearly anchors**, and separately for the **rolling** VWAP. Anchored and rolling
are different objects and must not be pooled to reach significance. A result that
appears on the monthly anchor and nowhere else is a single-instance result.

### DEFLATION GAUGE — STATED IN ADVANCE

> **A σ2 touch is, BY CONSTRUCTION, the statement "price is far from its recent
> volume-weighted mean." Nothing more is smuggled in by the fact that we compute
> it with volume weights and call it a band.**
>
> **H-VBR must therefore be scored against a plain distance-from-mean baseline
> and an ATR-extension baseline, on the identical cohort definition and the
> identical toll.**
>
> **If σ-band entries do not beat both baselines by the pre-registered margin,
> H-VBR is a REDUNDANT DRESSING OF A SIMPLER FACT and must be filed as such —
> explicitly, in those terms, in the ledger.**

This gauge is the point of routing H-VBR at all. The band is visually
compelling, it is already drawn on the instrument, and it will *look* like a
discovery the moment anyone measures it. The only defence against that is to
name, before the measurement, exactly which simpler fact would explain the whole
result. ARGUS names it here so it cannot be renamed afterwards.

Two secondary deflations APOLLO should carry:

- **Mean-reversion-to-a-moving-target.** The VWAP moves toward price while the
  trade is open, so "reached the mean" is partly the target coming to the entry.
  A fixed-at-entry target and a live target are different hypotheses and should
  be scored separately.
- **Survivorship in the anchor.** Long anchors (yearly) contain few independent
  events per asset. Effective n, not row count, governs.

### What ARGUS is NOT claiming

Nothing about whether band reversion pays. `vw_sigma_bands` is a drawn level
family, computed under the verified conventions in §5. That is all it is.

---

## 3 · NEW — **H-VBT** · VWAP Band Target

### The question

**Do exits at confluence-scored VWAP levels retain more of peak excursion than
riding to regime break?**

### Why this one matters more than the others

It aims directly at the study's **PRIORITY #3, the HARVEST PROBLEM, which is
still unsolved.** The measured record (LEDGER 2026-07-20, S-3 anatomy, commit
`f656dbd`, Cell-B, 7,094 tranches):

| measured fact | value |
|---|---|
| tranches reaching ≥ +1R MFE (PROTECTED cohort) | **43.90%** |
| of those, share reversing to gross loss | **73.67%** (baseline 47.96%) |
| median peak-capture vs baseline | **−43.65% — WORSE** |
| `stop` exits that win | **0.0%** (pure loss-cap, static by construction) |
| where the wins actually live | flatten exits: `opposite_cross` 719 @ 67.0%, `failure_x` 1352 @ 23.6% |

Read plainly: **the winning book wins by riding to regime break, not by managing
individual winners** — and three quarters of the trades that show a profit give
it all back.

### The bar H-VBT must clear

**A target-based exit must BEAT riding to regime break. It is not enough for it
to exist, to be implementable, or to raise the hit rate.**

The failure mode is specific and predictable: any take-profit rule mechanically
raises win rate and mechanically cuts the right tail. Because the book's entire
positive expectancy currently lives in the right tail (`opposite_cross` at 67%),
a harvest rule that improves win rate while shortening the tail can **destroy the
book while appearing to fix it.** The scorecard must therefore be **net-after-toll
expectancy on the full book**, with the excursion distribution shown, not hit rate
and not median peak-capture alone.

### Deflation gauges — stated in advance

- **Any-target baseline.** Score confluence-scored VWAP targets against a fixed
  R-multiple target and against a plain ATR-multiple target. If a dumb fixed
  target does as well, the confluence scoring contributed nothing and H-VBT files
  as *"harvesting helps / hurts; the level choice is decoration."*
- **Opposing-structure baseline.** The already-named opposing-wall / measured-move
  harvest line is the incumbent alternative and must be in the comparison.
- **The score is agreement, not edge.** A high-confluence VWAP level means several
  tools point at the same price. Whether tool agreement locates a place price
  actually stops is exactly the open question — it must not be assumed by using
  the score as a ranking key without testing the key itself.

### Substrate note

`D-1` dedupe removed the flat `members` list from `dual_score`; `member_count`
replaces it and **`clusters[].members` is the single source** of membership. Any
census join must go through `clusters[].members`, or counts will silently differ
between two apparently equivalent paths.

---

## 4 · CARRIED FORWARD — already routed, still open

Restated so this note is a complete backlog, not a delta. All four remain behind
the adoption gate.

| id | question | status / carried notes |
|---|---|---|
| **CENSUS-1d** | which layer combinations actually predicted anything, on exploration-classic data | The named home for *learned weights*. Nothing may enter a bias print from it except pre-registered and after the fact. Behind BOTH gates: fixtures green **and** operator parity readings matched. |
| **H-RVX** | do rolling-VWAP crosses confluence with the Secret Sauce EMA crosses? | Returned as a named G-7 candidate pending a drafted contract with **priors, a numeric agreement window, a sample definition and a numeric deflation threshold** — all four still owed. |
| **H-M1X** | 1m lattice (300/450) × 5m — does the fast-lattice observation layer carry information the 5m frame does not already hold? | Routed 2026-08-02. Deflation gauge implied and here made explicit: it must beat the 5m frame alone. |
| **H-VAN** | scale-confirmed value-area edges | **B-10 was ruled (a):** scale-confirmed VA edges **merge for scoring and carry a badge; they do not add score**, because nested windows are partially dependent and the law is counted-never-weighted. The census question is whether the badge marks anything; the ruling is what stops the instrument from pre-judging it. |

---

## 5 · What the BRIEF lane is providing as substrate

**Recording begins this cycle.** From now the daily capture records:

- **band-excursion events** — occurrences of price reaching and leaving the σ
  bands, with the anchor identity, the scale, and the surrounding structure;
- **the stretch layer** — the standing distance measurements between price and
  the volume-weighted means, per scale.

These accumulate as a forward record with a start date. They are exactly the raw
material H-VBR and H-VBT would need, and they are being written now so that the
census, whenever it is registered, is not starting its clock from zero.

### The firewall, stated plainly

> **Recording is OPS. Scoring is census under G-7.**
>
> The daily brief is an OPS artifact and is **NEVER study evidence**. The
> firewall between the two is this project's central discipline. That the BRIEF
> lane writes band-excursion events daily does **not** make those events
> scorable, does **not** create a Tier-C, and does **not** shorten any
> pre-registration. Forward live data is operations-only; rules are born only
> under G-7 on **exploration-classic** data.
>
> If APOLLO wants these events scored, the route is a G-7 registration that names
> the sample and the predictions in advance — not a read of the ops record after
> seeing it.

### Pinned conventions APOLLO inherits (verified, not inferred)

- **Rolling VWAP uses `hlc3`** and matches TradingView **to the cent on 1D bars**.
- **Anchored VWAP ALSO uses `hlc3`.** An earlier reading suggesting `ohlc4` was a
  TradingView **Source-setting difference** and is resolved.
- **Variance is volume-weighted POPULATION**, one-pass, **no (n−1) correction**.
  This is **VERIFIED, no longer inferred** — proved by a 2-bar anchor, where the
  population and sample forms differ by √2.
- **Level registry** currently carries **~126–165 levels per asset** across five
  families, after prior M/Q/Y anchors and `confirmed_pivots` were wired in.
- **Invalidation** is the **far edge of the NEXT CLUSTER BEYOND the entry
  cluster** — structure-derived, **not** a function of cluster width.
  `MIN_INVAL_ATR = 0.25` is a **CAUTION CHIP, not an exclusion gate**: a census
  that treats it as a filter would be measuring a cohort the instrument does not
  actually exclude.

---

## 6 · Hazards APOLLO inherits — read before designing the sample

Each of these has already bitten this lane once. They are listed so they do not
bite the census silently.

- **F-2R-A (closed).** `stoch_rsi` returned **all-NaN on every input**: `sma` is
  cumsum-based and one leading NaN poisoned everything downstream. Fixed via
  `_sma_after_warmup`; **F-AN-6b now asserts every series function is FINITE
  after warm-up.** Any census reading of stoch-RSI taken before 1.3.0 is void.
- **F-1R-A (closed).** `resample_ohlcv` now emits **only buckets PROVED closed by
  a bar in a strictly later bucket**, and **raises `UndecidableStepError`** on an
  undecidable step rather than guessing. Cost measured at zero — no published
  number moved. The consequence for census work: **do not build your own
  resampler.** Route through `analytics`, or two paths will disagree about which
  bar is last closed.
- **F-1R-B (open, reported not fixed).** `scripts/daily_brief.py:216` carries a
  private `resample()` that does not inherit the closure discipline. Until it is
  routed through `analytics`, two briefs can disagree about the last closed bar.
- **F-1R-C (open, contained).** The σ bands that ship are **duplicated inline**;
  `vw_sigma_bands` is referenced nowhere in production. `F-AN-13b` pins the three
  copies byte-identical so they cannot drift silently — but a census reading σ
  bands should know it is reading a function the production path does not call.
- **THE 1h PATH HAS NEVER BEEN EXTERNALLY TESTED.** The **RULED substrate for
  computation is 1h**. Every parity check performed so far compared **1D readings
  to 1D computation**. The 1h path is therefore fixtured but **not externally
  validated against any outside reference.** Any census whose substrate is 1h is
  standing on an untested parity leg, and should say so in its own pre-registration
  rather than inherit the 1D certification by association.

---

## 7 · What ARGUS is NOT claiming

For the avoidance of any later doubt, this lane asserts **none** of the
following, and this note must not be cited as support for any of them:

- that σ-band entries pay, or that band reversion has an edge;
- that confluence-scored VWAP targets solve the harvest problem;
- that any candidate here will replicate across scales;
- that tool agreement locates prices where price actually reacts;
- that any number in the daily brief is evidence of anything.

What ARGUS asserts is narrower and entirely mechanical: **these objects are now
computed under verified conventions, their hazards are enumerated, and their
substrate is being recorded from this date.**

---

## 8 · What ARGUS asks of APOLLO

1. **Acknowledge the routing** and take ownership of H-VBR and H-VBT as named
   candidates, or decline them with a reason on the record.
2. **Draft the missing numeric furniture** — for H-RVX specifically, the four
   items still owed (priors, agreement window, sample definition, deflation
   threshold); for H-VBR and H-VBT, the same set from the start.
3. **Sequence honestly.** Nothing here jumps the adoption gate. CENSUS-1d, H-RVX,
   H-M1X and H-VAN already wait on the operator's parity readings; H-VBR and
   H-VBT join the same queue rather than overtaking it.
4. **Carry the deflation gauges verbatim into the G-7 commit.** A gauge written
   after the result is not a gauge.

---

**Firewall.** Not a signal service. Not sizing advice. **Not study evidence.** No
Tier-C created or implied. No engine change. No forward scoring. No fitted
weights. No estate mutation. No lockbox read.

**PARITY NOT CERTIFIED.**

*Filed by HEPHAESTUS, ARGUS lane, 2026-08-03. Read-only cycle: no code was
written, no `analytics/` or `scripts/` file was touched, nothing was implemented.*

---

## ADDENDUM — three hazards in the substrate, added by the builder

These are not caveats about the questions; they are properties of the DATA we are
handing you, and each one can manufacture a false positive on its own.

**1. `thin_sample` is load-bearing — filter or stratify on it.**
A sigma computed over very few bars is the spread between two numbers:
arithmetically exact, informationally empty as a dispersion estimate. Every
stretch row carries its bar count and a `thin_sample` flag below 30 bars.

This matters specifically and predictably for H-VBR: **a freshly opened monthly,
quarterly or yearly anchor produces a sigma-2 touch trivially**, because its
sigma is tiny. On 2026-08-03, the Month anchor held 2 daily bars on a 1D chart
and the weekly anchor 21 hourly bars. An unfiltered band-touch study would
harvest those and read them as signal. They are not signal; they are the anchor
being new.

**2. "Captures since last touch" is DERIVED, never stored.**
The panel computes it from the stored `band_reached` series at build time. A
capture is a point in time and must stay self-describing, and `brief_panel.py`
rebuilds every partition FROM CAPTURES ALONE. So the series is reproducible from
the archive rather than trusted from a counter — but it means you must build it,
not read it.

**3. The substrate is 1h and has NEVER been externally parity-checked.**
The ruled spec pins 1h. Every parity comparison to date read a **1D chart**
against **1D computation**, and on the rolling VWAP the 1h-vs-1D difference
reached **0.377 daily-ATR** on the 7-day window. The 1h path is what the census
would consume and it is currently unverified against any external reference.
This is open and is stated in the cycle-3 and cycle-4 session summaries.

Record shapes for all of the above are in `analytics/INTERFACE.md`.
