# PARITY CAPTURE PLAN — exactly what to screenshot
### For the operator · ARGUS · 2026-08-02 · supersedes the *how-to* sections of PARITY_READINGS_GUIDE.md

**Twelve screenshots. Two chart setups. You can stop after any block and resume later.**

You do **not** need any file from your repo to do this. You do not need to find specific historical candles. You read whatever candle is current when you sit down, and I recompute our numbers for exactly the candles you read.

---

## Before anything — three settings that decide whether this works

**1 · The symbol must be the Binance USDT-margined perpetual.**

```
BINANCE:BTCUSDT.P
BINANCE:ETHUSDT.P
BINANCE:SOLUSDT.P
```

⚠️ **Your last chart screenshot was `BTCUSD` on OKX.** That is a different exchange and a different instrument — different volume, different wicks, different VWAP. Reading parity from it would make every single row disagree for a reason that has nothing to do with our code. The `.P` suffix and the `BINANCE:` prefix both matter.

**2 · Chart timezone must be UTC.** Right-click the time axis at the bottom → **Settings** → **Symbol** tab → **Timezone** → **UTC**.

**3 · Never hover the candle at the right edge.** It is still forming and its values change every second. **Hover the last *closed* candle** — the one with at least one candle to its right. This is precisely the defect we just spent two days correcting.

---

## The tool that makes this fast

Press **Alt+D** to open the **Data Window** (or right-click the chart → Data Window). A panel opens on the right showing the exact value of **every loaded indicator** for whichever candle your cursor is on, plus that candle's date and time.

This is why twelve screenshots is enough: one hover captures eight or more values at once, and the timestamp comes with them.

---

## Chart setup A — the oscillator pack

Add these five indicators to the chart **once**. Check every setting; a length of 14 versus 21 produces a completely different number.

| Indicator | Settings |
|---|---|
| **RSI** | Length **14** · Source **close** |
| **Stochastic RSI** | K **3** · D **3** · RSI Length **14** · Stochastic Length **14** · Source **close** |
| **MACD** | Fast **12** · Slow **26** · Signal **9** · Source **close** · both methods **EMA** |
| **Awesome Oscillator** | no settings — fixed at 5/34 |
| **ATR** | Length **14** · Smoothing **RMA** ← this is Wilder's method. If it says SMA or EMA, change it. |

*If your TradingView plan limits how many indicators you can load at once, split this into two passes — RSI + StochRSI first, then MACD + AO + ATR — and take twice as many screenshots. Nothing is lost.*

### Take these nine screenshots

Each time: set the symbol, set the timeframe, hover the **last closed candle**, capture the window.

| # | Symbol | Timeframe | Which candle |
|---|---|---|---|
| **A1** | BTCUSDT.P | **1h** | last closed |
| **A2** | BTCUSDT.P | **4h** | last closed |
| **A3** | BTCUSDT.P | **12h** | last closed |
| **A4** | BTCUSDT.P | **1D** | last closed |
| **A5** | ETHUSDT.P | **4h** | last closed |
| **A6** | ETHUSDT.P | **1D** | last closed |
| **A7** | SOLUSDT.P | **4h** | last closed |
| **A8** | BTCUSDT.P | **4h** | any candle **roughly 30 days back** |
| **A9** | BTCUSDT.P | **1D** | any candle **roughly 30 days back** |

**Why A8 and A9 exist.** An indicator can be right on the newest candle and wrong further back — that would mean its warm-up or its starting seed is subtly off. Any candle around a month ago works; you don't need a specific one, just tell me nothing and I'll read the timestamp from the screenshot.

**What A1–A9 certify:** RSI, StochRSI, MACD, Awesome Oscillator and ATR across five timeframes and three assets — the entire oscillator surface of the toolkit.

---

## Chart setup B — the VWAP pack

Remove the oscillators (or start a fresh layout) and add these six.

**Four instances of Rolling VWAP.** Indicators → search **"Rolling VWAP"** → add the **official TradingView one** (the one whose source code you sent me). Add it **four times**, and configure each:

| instance | Source | "Use a fixed time period" | Days | Bands multiplier 1 |
|---|---|---|---|---|
| 1 | hlc3 | ✅ **checked** | **7** | **1** |
| 2 | hlc3 | ✅ **checked** | **30** | **1** |
| 3 | hlc3 | ✅ **checked** | **90** | **1** |
| 4 | hlc3 | ✅ **checked** | **365** | **1** |

⚠️ **The "Use a fixed time period" checkbox is the critical one.** Left unchecked, the indicator picks its own window based on your chart timeframe — you would be reading a completely different window than the one we computed, and it would look like our code was wrong.

**Two instances of anchored VWAP.** Indicators → **"VWAP"** → add twice:

| instance | Source | Anchor Period |
|---|---|---|
| 5 | hlc3 | **Month** |
| 6 | hlc3 | **Quarter** |

### Take these three screenshots

| # | Symbol | Timeframe | Which candle |
|---|---|---|---|
| **B1** | BTCUSDT.P | **1D** | last closed |
| **B2** | ETHUSDT.P | **1D** | last closed |
| **B3** | BTCUSDT.P | **1D** | any candle **roughly 30 days back** |

**What B1–B3 certify:** all four rolling VWAP windows *and* their ±1σ bands, plus both anchored VWAPs. The bands matter most — the band formula is the piece we pinned line-by-line from the Pine source you gave us.

**Optional extra column:** if you also run your private rolling-VWAP script, add it to the B1 chart and it will appear in the same Data Window capture. If it disagrees with TradingView's official one, that is genuinely worth knowing — it would mean the numbers you have been reading differ from the ones we pinned. Costs you nothing but one extra glance.

---

## What must be visible in every screenshot

Four things. A full-window capture normally gets all of them:

1. **The symbol** — top-left of the chart, must read `BTCUSDT.P` etc.
2. **The timeframe** — highlighted in the top toolbar
3. **The candle's date and time** — appears at the top of the Data Window as you hover
4. **The Data Window values** — the whole panel

If the hovered timestamp isn't legible in the capture, just say in your message which candle you were on. Don't retake the screenshot for that alone.

---

## When a number looks wrong

**Change nothing.** Don't adjust settings to make things agree, don't retake with different values. Send it exactly as it appeared. A mismatch is information, and I want it uncontaminated.

My diagnostic order is fixed: exchange and symbol first, then timezone, then closed-versus-forming candle, then indicator settings, and only then our arithmetic. Roughly four out of five mismatches live in the first three, which is why the top of this document is what it is.

**One recipe carries a known question mark going in.** The **anchored** VWAP's σ bands are the one thing we *inferred* rather than read. We know TradingView's *rolling* VWAP band formula exactly because you gave us the source; we assumed the anchored version uses the same formula and never read that code. If a disagreement appears anywhere, that is the expected place — and nothing is wrong with the build if it does.

**Volume profiles are deliberately not in this plan.** Our profiles spread each candle's volume across its range; TradingView's does something similar but not identical. Comparing two different approximations certifies nothing, so profiles are certified by internal fixtures instead. Eyeballing them side by side is welcome, it just isn't a gate.

---

## Stopping and resuming

| you completed | what it certifies | gate status |
|---|---|---|
| A1–A4 | the full oscillator suite on BTC across four timeframes | in progress |
| A1–A7 | oscillators across all three assets | in progress |
| A1–A9 | oscillators including warm-up drift | in progress |
| + B1–B3 | **everything — the VWAP complex and its bands** | **gate closes** |

You can stop after any block. Progress isn't lost and I can start checking the moment the first block arrives. But the adoption gate only opens when all twelve are in — the no-partial-adoption rule means the toolkit isn't trusted piecemeal.

---

## Then send them

Drop the screenshots in chat. I recompute our side for exactly the candle timestamps visible in your captures and compare value by value.

- **Everything matches** → the toolkit is **adopted**, the brief rebuild can consume it, and four census phases (CENSUS-1d, H-RVX, H-M1X, H-VAN) become registrable.
- **Something disagrees** → we diagnose it, fix the cause, and you re-shoot **only the affected screenshot** — not all twelve.

---

## Quick card

```
SYMBOL       BINANCE:BTCUSDT.P / ETHUSDT.P / SOLUSDT.P   (NOT OKX, NOT spot)
TIMEZONE     UTC
CANDLE       the last CLOSED one — never the right edge
PANEL        Alt+D (Data Window)
IN FRAME     symbol · timeframe · candle timestamp · Data Window

SETUP A  RSI 14 close · StochRSI 3/3/14/14 close · MACD 12/26/9 EMA close
         · AO (fixed) · ATR 14 RMA
   A1 BTC 1h   A2 BTC 4h   A3 BTC 12h   A4 BTC 1D
   A5 ETH 4h   A6 ETH 1D   A7 SOL 4h
   A8 BTC 4h ~30d back     A9 BTC 1D ~30d back

SETUP B  Rolling VWAP ×4 — hlc3 · FIXED TIME PERIOD ✅ · Days 7/30/90/365 · band ×1
         VWAP ×2 — hlc3 · Anchor Month, Anchor Quarter
   B1 BTC 1D   B2 ETH 1D   B3 BTC 1D ~30d back

ON MISMATCH  change nothing, send it as it appeared
```
