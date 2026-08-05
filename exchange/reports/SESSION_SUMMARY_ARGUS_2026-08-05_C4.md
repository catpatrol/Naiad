# ARGUS CYCLE 4 — SESSION SUMMARY

**Builder:** HEPHAESTUS · **Date:** 2026-08-05 · **Reviewer:** ARGUS
Stages 0–8 executed in full. The scope valve was not needed.

---

## HOW TO READ THIS

**§1 is the headline** — a question open for five cycles is now closed.
**§2** is what you can use. **§3** is what is still gated, and the single thing
you can do to close the last gate. **§4** is where I was wrong or where an
earlier number was overstated. **§5** has the decisions. **§6** routes census
work to APOLLO.

**Nothing is adopted.** `PARITY NOT CERTIFIED` still prints on every render, and
§3 explains why that is still correct even though everything matched.

---

## §1 · THE 1h PATH PASSES PARITY — the five-cycle gap is closed

Every parity check ever run compared a **1D chart** reading to a **1D
computation**. The instrument publishes on **1h**. So the path that actually
runs had never been checked against anything.

**You supplied a 1H capture. It passes.**

BTCUSDT.P, closed bar `2026-08-05T17:00Z`:

| | worst disagreement |
|---|---|
| RVWAP 7d (168 bars) | 0.0453 |
| RVWAP 30d (720 bars) | 0.0496 |
| RVWAP 90d (2,160 bars) | 0.0494 |
| RVWAP 365d (8,760 bars) | 0.0429 |

**All 28 values — four means and twenty-four band levels — agree within
0.0496.** That is the rounding half-step of your chart's one-decimal display, so
what is left is your display precision, not our arithmetic.

**The raw bar matched first**, to every decimal, before any indicator ran — so
nothing downstream inherited a bad input.

**Rolling VWAP is now certified on both substrates.** The old "0.377 daily-ATR"
1h-vs-1D figure was never a defect; it measured a real property of
bar-granularity weighting. Both are now independently confirmed against their
own charts, which was the only way that number could ever be interpreted.

### The 1D confirmation also held, and it held *predictively*

Anchored Month came in at **63,112.2671** against your 63,112.3. The addendum
computed that number **before** you changed the Source setting and predicted the
reading would move there. It did, to **0.005 bps**. That matters more than the
match: a recipe whose behaviour you can predict is understood; one that merely
agrees today is not.

**RVWAP 365 is byte-identical to the ohlc4-era capture**, as it must be —
rolling VWAP was always hlc3. No finding.

**A small correction to the reviewer:** our σ is 319.8884 against your observed
band-1 distance of 319.9, off by **0.0036%**. The back-solved 320.13 misses by
**0.072%** — so the back-solve was slightly off, not our arithmetic.

---

## §2 · WHAT IS NOW CERTIFIED AND USABLE BY APOLLO

| recipe | status |
|---|---|
| oscillators (RSI, StochRSI, MACD, AO) + ATR | **CERTIFIED** — 72/72 |
| `resample_ohlcv` | **CERTIFIED** — 40/40 |
| **`rolling_vwap`** | **CERTIFIED, BOTH SUBSTRATES** — 1D 14/14 and 1h 28/28 |
| `vw_sigma_bands` geometry | **VERIFIED** — 36 triples, exactly symmetric at exact integer multiples |
| `anchored_vwap` variance | **VERIFIED** (was "inferred" for four cycles) |
| `anchored_vwap` σ **on 1h** | **UNVERIFIED** — see §3 |

**The variance question is settled on evidence, not assumption.** The
2026-08-01 Month anchor was **two bars** wide — the smallest sample that can
tell the two candidate definitions apart, because they differ there by **41.4%**.
The population form landed within **0.003%**. It could only have come out one
way.

### What shipped this cycle

**The REVERSION archetype** — the half of the R:R board that was missing. Enter
at a σ2/σ3 band price has **actually reached**, target the **VWAP mean**,
invalidate one band further out. **12 drafts across 7 of 10 assets today.**

**It did exactly what it was built to do.** Cycle 4 measured all 40 continuation
targets under 2 ATR with the MID and FAR buckets **empty**, because the next
opposing cluster is always close in a 160-level registry. Reversion targets the
mean, and the mean is where the distance lives:

| bucket | n | median target distance |
|---|---|---|
| NEAR (<2 ATR) | 6 | 0.55 ATR |
| MID (2–6) | 3 | 4.29 ATR |
| FAR (>6) | 3 | **15.52 ATR** |

**RVOL** (ruling B-7) — built; it was genuinely absent, not merely unreported.
Current volume against the trailing 20-day average **for the same hour of day**,
with the current bar excluded from its own baseline. It casts no vote.

**The excursion table** — which had been *documented* for a full cycle and never
actually built. Every capture claimed the since-last-touch series was "derived at
panel-build time" and no such derivation existed. It does now.

**`analytics/INTERFACE.md` regenerated** with a **certification table**, because
"verified" and "certified" are different claims and APOLLO had no way to tell
them apart.

**v1.1 retired** — ruling D-3's condition is met. Not deleted (it still supplies
the Part I layers and bridges every pre-2026-08 archive), just no longer
scheduled.

---

## §3 · WHAT IS STILL GATED — and the one thing that closes it

### ⭐ THE ONE OPERATOR ACTION

**Take one 1H chart capture of BTCUSDT.P with ANCHORED VWAP BANDS ENABLED.**

The anchored **means** matched on 1h this cycle (Month 63,602.4452 vs 63,602.4;
Quarter 63,486.3109 vs 63,486.3). But your 1H capture had anchored **bands**
switched off, so the anchored **σ on the 1h substrate** is the last unverified
quantity in the VWAP family. The recipe and the variance definition are already
verified — only the substrate is untested, and the substrate delta on the Month
anchor was measured at up to **0.186 daily-ATR**, which is too large to wave
through.

**This is NOT blocking.** Everything else proceeds. It is one screenshot.

### ⚠ A WARNING THAT NOW BINDS EVERY CONSUMER

Read the same bar on TradingView's **BTCUSD INDEX** instead of the Binance
perpetual and RVWAP 7d comes out **63,786.76** against our **63,737.7**.

The 49-point gap is **1.51× the collapse tolerance**. That means the wrong
instrument does not produce a rounding difference — it produces a **separate
registry level**. In a system that scores by counting agreement, that is one
tool counted twice. Every number we publish is the **Binance perpetual**. This
is now a standing warning in INTERFACE.md.

### Still open

- **Maturity stabilisation** — the *measured* replacement for R3's interim 10/30
  bar floors. It needs a walk-forward across the estate; it is the one stage-7
  item I did not deliver, and it is cycle-5 work.
- **`PARITY NOT CERTIFIED`** — stays up. Rolling VWAP passing on both substrates
  does not certify the instrument as a whole. That call is yours, not a
  builder's.

---

## §4 · WHERE I WAS WRONG, OR WHERE A NUMBER WAS OVERSTATED

### 4.1 "None of them ran" — they ran

The instruction said the three previous blocks never executed. They did, on
2026-08-03: both reports are on disk and three commits are in history. I checked
before rebuilding anything, which is the only reason this cycle did not redo work
that already existed. What genuinely remained was the reversion archetype and the
1h reading — both now delivered.

### 4.2 R1 and R2 changed no code, and no number moved

The 1h substrate and hlc3 source were **already** what the code did, in all
three places. The rulings promote them from implementation detail to pinned
convention — which is worth doing, because an unpinned coincidence can drift —
but stage 1.1's premise that "returned numbers change" was false. I took the
version bump anyway, on the existing precedent that a contract change earns one.

### 4.3 Item 6 was overstated TWICE — it is 6 of 20, not 20 of 20

Cycle 2's headline was *"a line moved on 20 of 20 sides."* Cycle 4 re-bucketed
that to 12 relocations. On the full registry:

| | count |
|---|---|
| **relocations** (≥ one cluster width) | **6** |
| refinements (< one cluster width) | 14 |

Median move **0.044 ATR** against a cluster width of 0.15. **Seventy per cent of
what was originally counted as movement is the same structure re-centred inside
its own cluster.** You called this the first time and you were right; the full
registry makes it starker still.

### 4.4 Sixth and seventh instances of the same fixture bug — one was mine

A firewall guard failed because a docstring *stated which statistics the function
refuses to compute*. The guard was scanning prose. Then my own new fixture hit
it: a field literally named `contains_no_probability_claim` was flagged for
containing "probability" — the promise read as the offence.

Both fixed by scanning **code**, not prose. Where the flagged text was genuinely
executable, I reworded the text and left the guard strict. That is now seven
occurrences of one pattern, and the rule is written into the fixtures: **scan
what the code does, never what it mentions, and never the prose that disclaims a
thing.**

### 4.5 I committed another lane's files by mistake

A `git add -A scripts` swept five untracked `scripts/seq8_*.py` files — DIONYSUS
lane work, outside my authorized scope — into a commit. Reverted with
`git rm --cached`: the files are **unchanged on disk** and back to untracked.
Nothing lost. Disclosed rather than left in.

### 4.6 The environment was broken and I fixed it before starting

The Python install had **only `pip`** — numpy, pandas, pytest and pyarrow all
missing, though `requirements.txt` pins them and the suite last ran 2026-08-03.
Restored from the repo's own pin file. Recorded so a future session recognises it
in one step rather than debugging import errors.

---

## §5 · DECISIONS

### D5-1 · Reversion ranking — flagged for your veto ⭐

**Reversion R:R cannot rank anything, and this cycle proved it with data.**
Across the whole estate, R:R took **exactly two values: 2.0 and 3.0**. That is
not a coincidence — it is forced by the construction. A σ2 entry targeting the
mean always earns 2σ against a 1σ stop; a σ3 entry always earns 3σ.

So reversion drafts are ranked by the **confluence score of the band level
itself**, which ranged **2 to 16** on the same capture. The band is already a
registry member, so the score is a lookup rather than a new invention.

**This directly answers your question of whether confluent VWAPs and standard
deviations better define the objective** — it makes confluence the discriminator
rather than a decoration. **Say if you want it ranked another way.**

### D5-2 · R6 is vindicated by measurement

The overruled ±3 ATR filter would have discarded **567 of 1,381 levels (41.1%)**
— including the 192-ATR level that is FARTCOIN's prior-year anchor. Worth
recording that the `ss` family is the one family with **zero** levels beyond 3
ATR, because a governor band is an entry-side object by construction. That
asymmetry is exactly what the filter mistook for a general rule.

### D5-3 · A calibration fact that should change your priors

Over 365 days of hourly bars across ten assets, price sits:

| beyond | measured | what a normal distribution would say |
|---|---|---|
| ±1σ | **~50%** | 31.7% |
| ±2σ | **~9.5%** | 4.6% |
| ±3σ | **~0.4%** | 0.27% |

**The 1σ band holds far less than intuition expects, and the 2σ tail is roughly
double.** If you have been treating a 2σ excursion as rare, it is about twice as
common as that. This describes the distribution only — it says nothing about
whether a touch pays, which is §6.

### D5-4 · §5.3's registry forecast should be amended to the measurement

Measured **131–169, median 160**, against §5.3's 180–200. The forecast was made
before the layers existed. Recommend amending the spec to the measured range
rather than adding levels to reach a number.

---

## §6 · CENSUS CANDIDATES — ROUTED TO APOLLO, NOT IMPLEMENTED

### H-VBR — VWAP Band Reversion

Do fills entered at σ2/σ3 of an anchored or rolling VWAP, targeting the mean,
differ in expectancy from the base book? **Cross-scale replication required**
across weekly/monthly/quarterly/yearly.

**DEFLATION GAUGE, STATED IN ADVANCE:** a σ2 touch is *by construction* "price
is far from its recent volume-weighted mean." If it does not beat a plain
distance-from-mean or ATR-extension baseline, it is a **redundant dressing of a
simpler fact** and must be filed as such.

*This cycle's §5 calibration sharpens that gauge: σ2 excursions occur on ~9.5% of
bars, not the ~4.6% a normal prior implies. The baseline to beat is
correspondingly less exotic than it looks.*

### H-VBT — VWAP Band Target

Do exits at confluence-scored VWAP levels retain more of peak excursion than
riding to regime break?

Aims at the study's **PRIORITY #3 HARVEST PROBLEM**, still unsolved: **73.67% of
trades reaching +1R round-trip into loss**, and the winning book wins by riding
to regime break rather than managing winners. **A target-based exit must BEAT
that, not merely exist.**

### The firewall, unchanged

Confluence measures **agreement between tools**, not edge. R:R measures
**geometry**, not probability. Recording band excursions is **OPS**; aggregating
them into rates or expectancy is **census work under G-7**. The new
`since_last_touch` view is a **recency counter** — the same class of object as a
naked POC's "untested since" — and a fixture now enforces that distinction on the
**code**, not on the documentation.

---

## §7 · PROVENANCE

`analytics` **1.4.0** · sha `e8a4959b…d20d66` · `rules_version` 2.0.0 ·
`schema_version` 2.1.0 · panel schema **2.1.0** · suite **262 passed / 1
skipped** (was 248).

Capture `briefs/brief_2026-08-05_post_ny.json`, sha256 `a93998f3…8185de`.
All four write-once partitions built (snapshots 10 · levels 2,269 · areas 80 ·
excursions 54). Render 158 KB.

Commits `38602a2` · `96f56e3` · `316d810` · `c46bffb` · `fd86aa9` · `7af9ad4`
(+ the seq8 un-track).

Paired with **`BUILDERS_REPORT_ARGUS_2026-08-05_C4.md`**.

— HEPHAESTUS, 2026-08-05
