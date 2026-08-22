# PARITY READINGS — step-by-step guide
### For the operator · ARGUS · 2026-08-02
### Keep this open beside your TradingView chart. The worksheet has the *what*; this has the *how*.

---

## Part 1 — What you are doing and why

We rebuilt every indicator from scratch in Python: RSI, StochRSI, MACD, Awesome Oscillator, ATR, anchored VWAP, rolling VWAP with its bands. The recipes are public and decades old, and our versions pass 41 internal tests.

**But an internal test only proves our code agrees with itself.** It cannot prove our RSI is the same RSI you see on your chart. If our version silently uses a different smoothing method — and there are two defensible ones — it produces numbers that are perfectly "correct" and never match your screen. You would slowly stop trusting the report and never know why.

**The parity session is the one moment where your eyes certify the machine.** You read roughly 28 values off your own charts; we compare them to ours. Where they match, that recipe is certified. Where they don't, we stop and find out why — we never adjust our number to fit.

**This is the gate.** Until these readings come back, the whole toolkit is plumbing that works rather than numbers that are trusted, and four census phases are queued behind it. It is roughly half an hour of work and it is the only thing in the project that nobody but you can do.

---

## Part 2 — Set up the chart once

Do these five things before reading anything. Four of the five most likely causes of a false mismatch live here.

**1 · Use the perpetual contract, not spot.** In the symbol box type exactly:

```
BINANCE:BTCUSDT.P
```

The `.P` matters. `BINANCE:BTCUSDT` is the spot market — different volume, different wicks, different VWAP. Our data is the USDT-margined perpetual. If your chart says "BTCUSDT" without `.P`, every volume-weighted number will disagree for a reason that has nothing to do with our code.

**2 · Set the chart timezone to UTC.** Right-click the time axis at the bottom → **Settings** → **Symbol** tab → **Timezone** → **UTC**. (Or click the clock in the bottom-right toolbar.)

Every candle in the worksheet is named by its **UTC open time**. If your chart is on Buenos Aires time you will read the wrong candle — and it will look like a plausible number, which is worse than an obviously wrong one.

**3 · Never read the candle at the right edge.** The rightmost candle is still forming; its values change every second. **Always read the last *closed* candle**, or better, the specific candle the worksheet names. This is exactly the defect we just spent two days correcting — the old brief was computing on unfinished candles.

**4 · Use the Data Window, not hovering.** Press **Alt+D** (or right-click → Data Window). A small panel opens showing the exact values of every indicator for whichever candle your cursor is over. This is far more precise than reading a number off the indicator pane, and it shows all indicators at once.

**5 · Widen the price scale if numbers look rounded.** Right-click the price axis → check that decimals aren't being truncated. We compare to the precision TradingView displays, so if it shows 2 decimals we compare 2 decimals.

---

## Part 3 — Set up each indicator

Add each of these to the chart once. **The settings must match exactly** — a length of 14 versus 21 produces a completely different number.

| Indicator | Where to find it | Settings to check |
|---|---|---|
| **RSI** | Indicators → "Relative Strength Index" | Length **14**, Source **close** |
| **Stochastic RSI** | Indicators → "Stochastic RSI" | K **3**, D **3**, RSI Length **14**, Stochastic Length **14**, Source **close** |
| **MACD** | Indicators → "MACD" | Fast **12**, Slow **26**, Signal **9**, Source **close**, Method **EMA** for both |
| **Awesome Oscillator** | Indicators → "Awesome Oscillator" | No settings — it is fixed at 5 and 34 |
| **ATR** | Indicators → "Average True Range" | Length **14**, Smoothing **RMA** (this is Wilder's method — if it says SMA or EMA, change it) |
| **Anchored VWAP** | Indicators → "VWAP" (the anchored one) | Source **hlc3**, anchor as named in the worksheet row (month / quarter) |
| **Rolling VWAP** | Indicators → "Rolling VWAP" — **the official TradingView one** | See below |

**Rolling VWAP needs special care.** This is the one whose source code you gave us, and it is the one we pinned our implementation to. Configure it as:

- **Source:** `hlc3`
- **"Use a fixed time period":** ✅ **checked** — this is the critical box. Left unchecked, the indicator picks its own window based on your chart timeframe, and you would be reading a completely different window than the worksheet asks for.
- **Days:** set to **7**, then **30**, then **90**, then **365** — one at a time, reading each before changing to the next.
- **Bands multiplier 1:** set to **1** where the worksheet asks for a σ band; otherwise 0.

**A note on your private rolling-VWAP script:** the worksheet has an optional extra column for it. We are certifying against TradingView's *official* Rolling VWAP because that is the algorithm we hold the source for. If your private script disagrees with the official one, that is genuinely useful to know — it would mean the numbers you have been reading differ from the ones we pinned. Filling that column is optional and costs one extra glance.

---

## Part 4 — Reading a value, one row at a time

Each worksheet row names four things: the **asset**, the **timeframe**, the **candle's UTC open time**, and the **measure** (e.g. "RSI(14)"). There is a column with our value already filled, and a blank column for yours.

**A worked example.** Suppose a row says:

> BTCUSDT · 4h · candle open 2026-08-02 08:00 UTC · RSI(14) · our value **52.4705** · yours: ______

1. Set the symbol to `BINANCE:BTCUSDT.P` and the timeframe to **4h**.
2. Confirm the timezone reads **UTC**.
3. Find the candle whose open time is **08:00** on 2026-08-02. Hovering over it shows the time in the Data Window or in the top-left OHLC readout.
4. **Check that candle is closed** — there must be at least one candle to its right.
5. Open the Data Window (Alt+D) with your cursor on that candle and read the RSI value.
6. Write it in the blank column, **exactly as displayed** — do not round it, do not tidy it.

Repeat down the list. The worksheet groups rows by asset and timeframe so you can do all of one chart setup at once rather than jumping around — read every BTC 4h row before switching to 12h.

**Four historical rows.** Four rows ask for candles roughly 30 days back. These exist because an indicator can be right on the newest candle and wrong further back — that would mean its warm-up or its window is subtly off. Scroll back to the named date and read them the same way.

**Three band-geometry pairs.** These ask for a VWAP line and its +1σ band on the same candle. We are checking the *distance between them*, which is the part of the algorithm we pinned most carefully. Read both numbers on the same candle.

---

## Part 5 — What to do when a number does not match

**Do not adjust anything.** Do not change our number, do not round yours to fit, do not change the indicator settings to try to make it agree. A mismatch is information and we want it exactly as it appeared.

**Write down what you saw**, and add one line noting anything unusual: the symbol you had loaded, the timeframe, and whether you were sure the candle was closed.

Then send it. On my side the diagnostic order is fixed: symbol (`.P` versus spot), timezone, closed-versus-forming candle, indicator settings, and only then our arithmetic. Roughly four out of five mismatches are one of the first three, which is why Part 2 exists.

**One recipe already carries a known question mark.** The *anchored* VWAP's σ bands are marked in the worksheet as **"to be confirmed by reading."** We know TradingView's rolling VWAP band formula exactly because you gave us the source; we *inferred* that the anchored version uses the same formula, but we never read that code. Your reading on those rows is the only thing that will settle it. If those specific rows disagree, that is the expected place for a disagreement and nothing is wrong with the build.

**Volume profiles are not on the worksheet, deliberately.** Our profiles spread each candle's volume across its range; TradingView's do something similar but not identical. Comparing two different approximations certifies nothing, so profiles are certified by internal fixtures instead. If you want to eyeball them side by side that is welcome — it just isn't a gate.

---

## Part 6 — When you are done

Send the worksheet back with your column filled — either drop the file in the project box, or paste the filled table into chat if that is quicker.

Then:

- **Every row matches** → the toolkit is **adopted**. The brief rebuild can consume it, and CENSUS-1d, H-RVX, H-M1X and H-VAN become registrable by APOLLO.
- **Some rows disagree** → adoption pauses for those specific recipes only. Everything else proceeds. We find the cause, fix it, and you re-read only the affected rows — not all 28.

**A practical suggestion:** do it in one sitting with the worksheet open on one side and the chart on the other. Reading 28 values across three days invites setting drift — a timezone left on local, a length changed and forgotten — and drift produces mismatches that cost more to diagnose than the readings cost to take.

---

## Quick reference card

```
SYMBOL      BINANCE:BTCUSDT.P     (the .P is not optional)
TIMEZONE    UTC                   (right-click time axis → Settings → Symbol)
CANDLE      the named UTC open time, and it must be CLOSED
READ WITH   Data Window, Alt+D
RSI         14, close
STOCH RSI   3, 3, 14, 14, close
MACD        12, 26, 9, close, EMA
AO          fixed 5 / 34
ATR         14, smoothing RMA (Wilder)
ANCH VWAP   hlc3, anchor per row
ROLL VWAP   official "Rolling VWAP" · hlc3 · FIXED TIME PERIOD ✅ · Days 7/30/90/365 · band ×1
ON MISMATCH change nothing, write what you saw, send it
```
