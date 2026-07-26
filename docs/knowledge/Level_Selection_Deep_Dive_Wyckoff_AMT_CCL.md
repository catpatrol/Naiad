# Level Selection — Wyckoff, Auction Logic, and the Cross-Cluster Hypothesis
### Where to favor entering and exiting: the canon applied to Secret Sauce, and a quant design for the operator's clustering idea
**Reviewer deep-dive · 2026-07-26 · handoff-ready: a new chat can pick this up cold**

**Grades:** `[verified]` = Naiad's own measured record · `[established]` = replicated literature · `[contested]` = live dispute · `[synthesis]` = reviewer hypothesis connecting the two. Rules: nothing here becomes an engine rule without its own G-7 pre-registration on exploration-classic data; canon summarized in my own words; where canon and Naiad's measurements disagree, the measurements win for this market.

---

## 0. Scope, and one distinction that organizes everything

The operator's ask: get better at **selecting the levels and points** where we favor entering or exiting. Two words, two different problems:

- A **level** is *where to wait* — a price area assigned elevated prior probability of reaction before price arrives. Levels are computed in advance.
- A **point** is *the trigger at the level* — the bar-level event that converts waiting into a fill. Secret Sauce already owns the point machinery (PRIME reclaims, grades, the arming state machine) and the census verdict says point-level cleverness is not where edge lives: entry combinatorics do not tilt raw price `[verified, D9/CENSUS-1b]`.

So this document is almost entirely about **levels** — for entries (where PRIME fills should be *favored*), for stops (which structure to hide behind), and for exits (the underdeveloped third leg: the harvest mechanism is the study's primary measured failure — 90.35% of +1R-touching trades exiting at a gross loss `[verified, PROTECTED paradox]`, and the winning book's median peak-capture *worse* than baseline `[verified, S-3]`). **Targets into opposing levels are the canon's answer to exactly that failure, and nothing in Naiad currently implements one.**

A second organizing fact from the in-house record: **timing-confluence is falsified, location-confluence survived.** D9 killed k-of-N signal stacking (gradient ρ ≈ 0.02–0.05) `[verified]`; the zone-landing result — pullback termini land in SS zones at ~2× matched-null chance across all four lenses — is the strongest structural survivor `[verified]`, and P-F1 showed the biggest *location* gate (no_zone rejection) filters genuinely worse fills (−1.205 vs −0.577 per unit) `[verified]`. Every proposal below is built as a *location* tool for exactly this reason — including the operator's clustering idea, which in its naive timing form would be a re-run of D9, and in its location form is untested and aligned with everything that survived. That reframe is the document's core move.

---

## 1. Wyckoff, applied specifically to levels and points

Wyckoff's method `[established as a descriptive framework]` reads campaigns as phases (A accumulation-stopping through E markup/markdown) and derives *specific, orderable locations* from them. What follows is each Wyckoff location, its Secret Sauce counterpart, what is already measured, and the test each one suggests.

### 1.1 The spring — the highest-grade entry *point*, already half-mechanized
A spring is a flush below defined support that fails and reclaims: trapped shorts + cleared stops = fuel. Naiad's structural stop is a spring-*survival* policy — sit behind real structure so the flush happens without you — and the measurement is emphatic: **52% of 4,167 shakeouts convert to ≥1R** under struct-1h `[verified, S-2b]`.

Wyckoff grades springs by depth and volume: a shallow undercut on drying volume (his #2/#3) is high quality; a deep, high-volume break that barely reclaims is suspect. Operationalized for **TC-2's re-entry bar** `[synthesis]`:
- flush depth beyond the structural low, in ATR;
- reclaim speed (bars to close back above);
- flush-bar volume percentile.
Three inputs → a graded spring test. Hypothesis: spring-qualified re-entries carry positive expectancy while unqualified re-entries carry the cost identity's 83%-of-loss burden `[verified burden; synthesis on the split]`. This gives TC-2 a mechanism instead of a bare threshold, and it is measurable on existing shakeout/journal rows before any rule is written.

### 1.2 The LPS — the canonical entry *level* after strength
The Last Point of Support: after the spring and the first show of strength, the *first higher-low pullback* is the textbook entry, because it proves the spring's low is now defended. SS counterpart: PRIME-in-zone after regime birth. The refinement Wyckoff adds: **the pullback low must hold above the spring low.** Test `[synthesis, Tier-A on existing journals]`: split historical R1 fills into LPS-qualified (entry pullback low > preceding structural flush low) vs not; compare expectancy. Cheap, journal arithmetic, no new machinery.

### 1.3 Creek and ice — the band SS already draws
Wyckoff's creek (resistance band over accumulation) and ice (support under distribution) are the e89/e200 band in SS clothing — Z3 territory. The "jump across the creek" and its back-test map to what the winning book already does: B's wins migrate to `opposite_cross` / `failure_x` flatten exits — **riding to the regime break, not managing winners** `[verified, S-3]`. The canon and the measured winning behavior agree here; no new test needed, but the vocabulary earns its place in the report and in v12 design language.

### 1.4 Tested vs untested lows — a stop-*placement* refinement
Struct-1h anchors at pivot(5,5) swing lows. Wyckoff prefers stops under **defended** lows — ones that have been revisited and held — over virgin pivots. Test `[synthesis]`: classify each historical stop-anchor pivot as tested (≥1 prior touch within b×ATR that held) vs untested; compare shakeout-conversion and terminal-stopout rates across the S-2b population. If the split is real, the ratcheting-structural named-follow-up inherits a selection rule, not just a mechanism.

### 1.5 Upthrust, LPSY, effort-vs-result
The short side mirrors (upthrust = bull-trap spring; LPSY = last rally before markdown) and need no separate machinery — the tests above run direction-symmetric. Effort-vs-result (heavy volume, no progress = absorption) enters as a **terminus-quality flag** in the brief: flush-bar volume percentile printed at every new swing extreme `[synthesis; volume's engine role stays earned-not-assumed]`.

### 1.6 Phase context
Regime birth ≈ the C→D transition; D8's 4H-rung add-edge `[verified, ratio 1.0711]` is phase-D continuation in Wyckoff terms. The mapping's value is narrative coherence for SSv12's design doc, not a new test.

---

## 2. Auction Market Theory — the exit half of the problem

AMT `[established as framework]` supplies what Wyckoff under-specifies: **where to take profit**. Its levels: value-area edges (VAH/VAL), points of control, and **naked POCs** (prior acceptance points never revisited — magnets with unusually good revisit statistics in desk practice `[contested magnitude, established direction]`).

The connection to Naiad's #1 failure is direct `[synthesis]`: the PROTECTED paradox is what "no target" looks like in data. The guiding philosophy's priority #3 — *a working take-profit that keeps profit* — currently has no candidate mechanism. AMT's is: **harvest into the opposing value edge / naked POC**, scaled or full, while the trend-following exit (ride to regime break) continues on the remainder. That two-sink design (structure-target partial + regime-break runner) is the standard resolution of the capture-vs-ride tension in the CTA literature `[established]` and composes with, rather than replaces, the F4-structural architecture.

Pre-registrable when its turn comes: on historical campaigns, the counterfactual "50% off at first opposing naked POC / VAH-VAL edge, remainder rides" vs pure ride — Tier-A on journals + klines once a profile engine exists (the daily-brief build delivers exactly that engine as a by-product).

A second AMT-adjacent candidate: **measured objectives from balance width** (the Point-&-Figure count concept — wider pre-breakout balance → larger move) `[contested as stated; testable core]`: pre-birth consolidation width/duration vs subsequent campaign MFE, Tier-A. Prior modest; cheap.

---

## 3. The rest of the level canon, graded and filtered

| Family | Claim | Grade | Testable core for Naiad |
|---|---|---|---|
| Period levels (W/M/Q/Y opens, prior H/L) | Orders cluster at salient references | `[established]` | Terminus-attractor test vs matched null (same machinery as zone-landing) |
| Liquidity pools (equal highs/lows, prior extremes) | Stop clusters attract sweeps, then reverse | `[established direction]` | **Widens S-2's F7**: redefine sweep-reclaim events as sweep-of-*level*-reclaim over the set {prior D/W H-L, equal extremes within tolerance} — fixes F7's n=60 sample-starvation `[verified problem; synthesis fix]` |
| Order blocks / supply-demand zones | Origin candle of an impulse that broke structure gets defended | `[contested; popularized without stats]` | Extract the falsifiable core — last opposite-color bar range before a structure break — and run it through the same terminus-attractor test; low prior, cheap, keeps us honest with the internet's favorite level family |
| Round numbers | Salience attracts orders | `[established, small]` | Include as one families-column in the composite test; never standalone |
| VWAP bands | Institutional benchmark reversion | `[established as benchmark use]` | Already in the brief; terminus test optional |
| Chart patterns (H&S, flags…) | — | `[contested → excluded]` | Stays in the anti-library; unreplicated genre |

The composition rule for all of it, learned in-house: levels compose by **counting independent families within a band — never by fitted weights** `[verified lesson, D9]`, and composition is tested as a *location conditioner*, never a timing tilt.

---

## 4. The Cross-Cluster Hypothesis (CCL) — the operator's idea, made falsifiable

**The idea as stated:** probabilistically narrow the areas where we trade by observing the clustering of multi-timeframe EMA crosses.

**The conscientious scrutiny, up front.** Three things must be said before any enthusiasm:

1. **The timing version of this idea is already dead in-house.** "When many TFs cross together, enter" is k-of-N confluence — D9 falsified the genre at ρ ≈ 0.02–0.05, and RC-7r additionally showed TPW/CLUSTER's window logic is clock-anchored (an artifact) `[verified]`. Any CCL design must therefore be a **price-location** tool: *where in price* do crosses from many scales co-locate — not *when* do they co-fire.
2. **The confound that could deflate it entirely:** an EMA cross occurs, by construction, where price has oscillated around the ribbon — i.e., where price has *spent time*. Cross-price density may therefore be nothing but a noisy re-derivation of **time-at-price**, which the volume profile already measures directly and better. This is not a footnote; it is the null hypothesis. The design below measures the equivalence explicitly, and if CCL ≈ VP, the honest verdict is "the simpler tool wins" and CCL retires with a clean falsification on the record.
3. **What would make it *more* than VP** `[synthesis]`: the fractal lens (standing frame). VP weights all time equally; CCL samples only *inflection* moments (momentum crossing trend) and stacks them **across scales**. If important shelves are scale-invariant — the fractal hypothesis — then crosses from different TFs should co-locate at real levels and scatter elsewhere, giving CCL peaks a *sharpness* and a *recency structure* that raw time-at-price lacks. That is the specific, testable value-add.

### 4.1 Methodology (v0, every constant [VETO]-flagged for pre-registration time)

- **Event universe:** all three cross types (9/89, 9/200, 89/200 — the census already emits them) × 7 TFs (5m…1d) × both directions, per asset, on the frozen exploration-classic substrate. *Free-proxy note: `census_outcomes.jsonl` / termini rows already carry cross events with timestamps and prices — CCL v0 is likely **Tier-A arithmetic on the existing byte-pinned substrate**, no new walk.* `[expect — one schema check confirms]`
- **Price stamp:** the cross bar's close [VETO default; alternative: EMA value at cross].
- **Density estimate:** per asset and per lens window, kernel density over price with bandwidth h = 0.25 × ATR(1d) [VETO]; trailing window scaled per lens (e.g., last 500 governor bars) [VETO].
- **Weights:** equal across TFs and cross types at v0 [VETO; TF-weighted = named variant, never fitted].
- **Level extraction:** local maxima above θ× the uniform-density baseline [θ VETO, e.g. 2×]; each peak carries width (where density falls to half) → a **CCL band**, not a line.
- **Decay:** recompute daily on the trailing window; a peak that stops being re-fed fades naturally — no ad-hoc expiry constant.

### 4.2 Pre-registered predictions (census style; priors stated; falsification is a deliverable)

- **P-CCL-1 (terminus attraction):** pullback termini land within b×ATR of a CCL band at ≥1.5× the matched-null rate (CENSUS-1's seeded null machinery, null_mult=10, reused verbatim), replicated on ≥5/7 assets and ≥3/4 lenses. Prior: **55%**.
- **P-CCL-2 (incrementality over SS zones):** among termini *outside* any armed SS zone, CCL-band landings still exceed null ≥1.3×. Prior: **40%** — deliberately low; SS zones are EMA-built and crosses happen at EMAs, so heavy overlap is expected.
- **P-CCL-3 (the VP equivalence, measured not hoped):** rank correlation between CCL peaks and volume-profile POCs over matched windows. This prediction has no "success" direction — it is the deflation gauge. ρ > 0.8 → CCL is VP in disguise; report it and retire CCL in favor of the direct tool. ρ in 0.3–0.8 → partially distinct; proceed. Stated in advance so the outcome cannot be spun.
- **P-CCL-4 (approach reaction):** first touch of a CCL band from either side shows reaction (fade MFE within k bars) above null. Prior: **45%**.
- **Graduation bars:** cross-asset (≥5/7 sign-consistent), cross-lens replication mandatory, survives strip-best, and P-CCL-2 or P-CCL-3-distinctness must hold — attraction alone that duplicates VP does not graduate.

### 4.3 If it graduates — three application slots, in priority order
1. **Exit targets** (priority #3 of the guiding philosophy, the unmet one): harvest partials into opposing CCL/VP levels — the two-sink design of §2.
2. **Entry-admission conditioner** (the family that survived): PRIME favored within b×ATR of a CCL band — a P-F1-style location gate, tested as enrichment, never as a standalone signal.
3. **Brief layer:** auto-drawn CCL bands beside VP levels, with their P-CCL-3 correlation printed so the operator sees daily whether the two tools are saying one thing or two.

### 4.4 Sequencing — this does not jump the queue
CENSUS-1c runs first, as ratified. CCL is drafted here as **CENSUS-2's headline candidate**: trade-independent, measure-only, Tier-A-or-B on the frozen substrate, zero lockbox spend, anti-fishing protocol inherited from CENSUS-1 (confirmatory predictions + quarantined exploratory annex). The free-proxy on existing census rows means its cost is closer to CENSUS-1b's than CENSUS-1's.

---

## 5. The unified level stack (where this all lands)

End state `[synthesis]`: one composite level map per asset — families = {SS zones `[verified]`, CCL bands (if graduated), VP value edges + naked POCs, period levels, liquidity-pool extremes, spring/LPS structural lows} — each contributing **one count** within a band, composed by counting, displayed in the brief, and consumed by the engine only through individually pre-registered gates: entry-favor (location conditioner), stop-anchor selection (tested-low rule), and harvest targets (opposing-level partials). Points remain SS's business; levels become a measured, versioned asset of their own.

## 6. What this document is not
Not a pre-registration (every constant above is a [VETO] placeholder until a contract pins it). Not a promise that CCL survives its own P-CCL-3. Not a reordering of the queue: 1c → (TC-C for D5/D8, TC-2 with the spring test as design input) → CENSUS-2/CCL is the working sequence, operator's call at each gate.

## 7. First actions for the chat that picks this up
1. One schema check: confirm census substrate rows carry cross price + timestamp per event (decides Tier-A vs re-walk for CCL v0).
2. Draft the two cheapest journal-arithmetic tests as a mini-contract: LPS-qualified split (§1.2) and tested-vs-untested stop anchors (§1.4) — both free, both feed TC-2 and the ratcheting-structural follow-up.
3. When CENSUS-2's slot arrives: convert §4 into the contract, constants pinned, priors as stated here unless the operator re-rules.
