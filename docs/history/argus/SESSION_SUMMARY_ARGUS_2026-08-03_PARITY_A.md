# PARITY RUN — SETUP A — SESSION SUMMARY

**Lane:** ARGUS · **Builder:** HEPHAESTUS · **Date:** 2026-08-03 · **Reviewer:** ARGUS

---

## THE RESULT, IN ONE LINE

**Everything matched. 36 of 36 raw bar fields identical; 72 of 72 indicator
comparisons agree at the precision TradingView displays.**

There were no disagreements to explain, so most of this document is about what
that does and — more importantly — **does not** mean.

---

## §1 · WHAT WAS ACTUALLY COMPARED

The operator read nine closed candles off TradingView (`BINANCE:<SYM>USDT.P`,
chart timezone UTC) across BTC, ETH and SOL, on 1h / 4h / 12h / 1d, including two
historical candles from late June and early July. For each he supplied eight
oscillator readings: RSI(14), StochRSI %K and %D, MACD line / signal /
histogram, Awesome Oscillator, and ATR(14).

This was a **measurement cycle**. No recipe was changed, no tolerance applied,
nothing tuned toward agreement, and no pass/fail emitted. A disagreement would
have been a finding, not a defect to close.

---

## §2 · THE PART THAT MATTERS MOST — THE RAW BARS

Before computing a single indicator, we compared **our stored OHLC against the
operator's** for each of the nine candles.

**All 36 fields identical.** Not close — identical to the stored precision.

This is the discriminator, and it was run first deliberately: if the bars had
disagreed, every indicator below would have inherited the difference and the
cause would have been the *data*, not the recipes. That ambiguity is now removed.

### The unplanned bonus

**Eight of the nine candles are not native bars — they are resampled from 1h**
under our closed-bar rule. They match TradingView's own aggregation exactly:
bucket boundaries, first/max/min/last, and which bucket is allowed to exist at
all.

That makes this **the first external check `resample_ohlcv` has ever had.** It is
the function that finding F-1R-A rewrote (it used to publish a bucket and then
revise it), and the one D-3 later routed `daily_brief.py` through. An independent
implementation now agrees with it on real bars. That is worth more than the
oscillator agreement.

Two internal identities also hold exactly, and the operator's readings satisfy
them too:

- A2's 4h close == A1's 1h close (both windows end at 20:00)
- A3's 12h open == A4's daily close

---

## §3 · THE 72 COMPARISONS

Every comparison agrees at the operator's displayed precision. Every residual is
a rounding artifact:

| |delta| as % of operator's value | count |
|---|---|
| < 0.01% | 22 |
| 0.01 – 0.05% | 36 |
| 0.05 – 0.10% | 11 |
| 0.10 – 1.00% | 3 |
| ≥ 1.00% | **0** |

The three above 0.10% are all SOLUSDT rows where the displayed value is small
(ATR 0.93, AO −0.33), so a single display digit is worth a large percentage.
Their absolute deltas are 0.0023, 0.0028 and 0.0001. Nothing is hiding there.

---

## §4 · THE TWO THINGS THE REVIEWER FLAGGED

### 4.1 The ATR "discrepancy" was never a discrepancy

The concern: the operator reads BTC 1d ATR = **1,649.6**, while a recent builder
figure for what looked like the same quantity was **~1,700** — about 3% higher.

Our value for the requested candle is **1,649.5778 → 1,649.6. It matches.**

The earlier figure was ATR as-of the **2026-08-01** daily bar — the last *closed*
daily bar at the moment that capture ran. The operator read the **2026-08-02**
bar. One bar apart:

```
ATR14 as-of 2026-08-01  = 1,699.7992
ATR14 as-of 2026-08-02  = 1,649.5778
```

**Same recipe, different as-of bar.** Not a recipe finding.

Worth noting *why* this was easy to confuse and how it is now prevented: the
parity tool prints the exact bar it evaluated on every row, so an as-of mismatch
announces itself instead of looking like a recipe error. That is the single most
common way a parity check goes wrong, and it is the reason the tool was built
that way.

Also confirmed: the **2026-08-03 daily bucket is not emitted at all**, because no
1h bar exists in a later bucket. The forming daily bar cannot reach the
calculation — excluded by construction, not by a filter someone has to remember
to apply.

### 4.2 StochRSI — the highest-risk row, and it passed

StochRSI returned **all-NaN on every input** until the F-2R-A repair earlier
today. These nine candles are its first external test.

**All 18 values (%K and %D across nine candles) are finite and match**, on four
timeframes and three assets. Warm-up is 31 bars of the evaluated timeframe,
exactly as CONVENTIONS records; every candle is far past it.

This is the strongest evidence available that the repair is correct. A fix
verified only by our own fixtures proves the fixtures pass; a fix that agrees
with an independent implementation on nine real candles is a different class of
confidence.

---

## §5 · WHAT THIS CERTIFIES — AND WHAT IT DOES NOT

**Certified on these nine candles:** RSI(14) · StochRSI %K/%D · MACD line,
signal, histogram · Awesome Oscillator · ATR(14) · and `resample_ohlcv` against
TradingView's aggregation.

**NOT certified — Setup B, the VWAP / volume pack:**

- rolling VWAP on 7/30/90/365d and its σ bands
- windowed volume profiles: POC, VAH, VAL
- low-volume nodes, value-area nesting

**This is the half of the instrument most likely to diverge**, and none of it was
touched today. Two reasons it is the riskier half:

1. **RVWAP uses a volume-weighted *population* variance with no (n−1)
   correction**, pinned from TradingView's published source. An ordinary standard
   deviation produces plausible numbers that never match his chart — a
   disagreement here would be subtle, not obvious.
2. **The volume profile is an approximation by construction.** Volume is spread
   uniformly across each bar's range because the estate stores no tick data. Real
   tick data would move POC/VAH/VAL somewhat. We may find a systematic offset
   that is *correct behaviour for our inputs* rather than a bug — and telling
   those two apart will be a judgement call, not an arithmetic one.

**Adoption does not open on Setup A.** The `PARITY NOT CERTIFIED` banner stays on
every render until Setup B is returned and matched.

---

## §6 · DECISIONS

**None requested from this run.** Nothing disagreed, so there is nothing to rule
on and nothing to fix.

Two items for the queue, neither urgent:

| item | owner | note |
|---|---|---|
| **Setup B readings** | operator | The VWAP/volume pack. `scripts/parity_check.py` already supports `rvwap`, `poc`, `vah`, `val` with a window parameter, so the run is the same one-paste shape. |
| **Cycle-2 decisions D2-1 … D2-5** | reviewer | Still open from the previous summary; unaffected by this run. |

---

## §7 · A NOTE ON WHAT A CLEAN RESULT IS WORTH

A parity run that matches everywhere is a weaker signal than it feels like. It
confirms the recipes we *implemented* agree with TradingView on the candles we
*chose*, using bars that turned out to be identical. It does not confirm the
recipes are the right ones to be using, and it says nothing at all about whether
any of these numbers predict anything — that remains census work under G-7.

What it does buy is specific and real: **when Setup B is run and something
disagrees, we will know the bars and the resample are not the cause.** That is
the value of having run the raw-bar check first, and it is why the next
disagreement will be diagnosable in one step instead of three.

---

## §8 · PROVENANCE

`analytics` **1.3.0** · sha `da81034d…c731` · `rules_version` 2.0.0
Full record: `exchange/reports/PARITY_SETUP_A_2026-08-03.json` (40,559 B, all 72
rows with deltas, evaluated bar and exact-match flag).
Paired artifact: `BUILDERS_REPORT_ARGUS_2026-08-03_PARITY_A.md`.

**No source file was modified in this cycle.** The only writes were an additive
1h kline top-up through the sanctioned loader and the exchange artifacts.

— HEPHAESTUS, 2026-08-03
