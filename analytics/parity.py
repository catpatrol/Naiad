"""Parity worksheet text generation. Returns strings; writes nothing.

The worksheet is the TRUST GATE. Until the operator's own chart readings come
back and match, a PASS means the plumbing works -- not that the numbers are
right. §X keeps ADOPTION a separate gate from PASS for exactly this reason.
"""

__all__ = ["ROWS", "INSTRUCTIONS", "worksheet"]

INSTRUCTIONS = """\
## How to fill this in

1. Chart the **perpetual**, not spot: symbol `BINANCE:<SYM>USDT.P`.
2. Set the chart timezone to **UTC**. A timezone mismatch is the single most
   common cause of a "wrong" reading here.
3. Read **closed candles only**. Hover the named candle and read the indicator
   value from the status line.
4. Write what you see, including all displayed digits. Do not round to make a
   number agree.
5. Leave a cell blank if you do not chart that instrument. Blank is a fine
   answer; a guess is not.

**Rolling VWAP rows** target TradingView's official **"Rolling VWAP" (RVWAP)**
indicator with *Use a fixed time period* checked, Days set as stated, source
`hlc3`, bands multiplier 1. That is the indicator whose source we hold. Your
private rolling-VWAP script is **not** the target -- but if you have it on the
chart, put its reading in the optional column, because a divergence between
private and official is itself informative.

**Acceptance:** a reading matches if it agrees to the precision TradingView
displays. Any mismatch **halts adoption of that recipe** and is reported with
the observed difference -- never patched around, never rounded into agreement.
"""

# (id, symbol, timeframe, quantity, when)
ROWS = [
    # --- 24 current-bar cells -------------------------------------------------
    ("R01", "BTCUSDT", "1h",  "RSI(14)", "current"),
    ("R02", "BTCUSDT", "4h",  "RSI(14)", "current"),
    ("R03", "BTCUSDT", "12h", "RSI(14)", "current"),
    ("R04", "BTCUSDT", "1d",  "RSI(14)", "current"),
    ("R05", "ETHUSDT", "4h",  "RSI(14)", "current"),
    ("R06", "ETHUSDT", "1d",  "RSI(14)", "current"),
    ("R07", "SOLUSDT", "4h",  "RSI(14)", "current"),
    ("R08", "BTCUSDT", "1h",  "StochRSI %K", "current"),
    ("R09", "BTCUSDT", "4h",  "StochRSI %K", "current"),
    ("R10", "BTCUSDT", "1d",  "StochRSI %K", "current"),
    ("R11", "BTCUSDT", "4h",  "StochRSI %D", "current"),
    ("R12", "BTCUSDT", "4h",  "MACD line", "current"),
    ("R13", "BTCUSDT", "4h",  "MACD histogram", "current"),
    ("R14", "BTCUSDT", "4h",  "Awesome Oscillator", "current"),
    ("R15", "BTCUSDT", "1d",  "Awesome Oscillator", "current"),
    ("R16", "BTCUSDT", "1d",  "ATR(14)", "current"),
    ("R17", "BTCUSDT", "1h",  "Anchored VWAP (month)", "current"),
    ("R18", "BTCUSDT", "1h",  "Anchored VWAP (month) +1 sigma", "current"),
    ("R19", "ETHUSDT", "1h",  "Anchored VWAP (quarter)", "current"),
    ("R20", "BTCUSDT", "1h",  "RVWAP 7d", "current"),
    ("R21", "BTCUSDT", "1h",  "RVWAP 30d", "current"),
    ("R22", "BTCUSDT", "1h",  "RVWAP 7d +1 sigma", "current"),
    ("R23", "BTCUSDT", "1h",  "RVWAP 365d", "current"),
    ("R24", "ETHUSDT", "1h",  "RVWAP 30d", "current"),
    # --- 4 historical cells, ~30 days back ------------------------------------
    ("H01", "BTCUSDT", "4h",  "RSI(14)", "~30 days back"),
    ("H02", "BTCUSDT", "1h",  "RVWAP 7d", "~30 days back"),
    ("H03", "BTCUSDT", "1h",  "Anchored VWAP (month)", "~30 days back"),
    ("H04", "BTCUSDT", "4h",  "Awesome Oscillator", "~30 days back"),
]

OPTIONAL = {"R05", "R06", "R07", "R19", "R24"}


def worksheet(date_str, ours, bar_times=None, version=None, sha=None):
    """Build the worksheet markdown.

    `ours` maps row id -> our computed value (or None if unavailable).
    `bar_times` maps row id -> the UTC open time of the candle to hover.
    """
    bar_times = bar_times or {}
    lines = [f"# Parity worksheet — {date_str}", ""]
    if version or sha:
        lines += [f"`analytics_version` **{version}** · `analytics_sha` `{sha}`", ""]
    lines += [
        "Canonical instrument: **Binance USDT-M perpetuals**, `BINANCE:<SYM>USDT.P`, "
        "chart timezone **UTC**, **closed** candles only.",
        "",
        INSTRUCTIONS,
        "",
        "## Cells",
        "",
        "| id | symbol | TF | quantity | candle (UTC open) | ours | **yours** | private RVWAP (optional) | match? |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for rid, sym, tf, qty, when in ROWS:
        v = ours.get(rid)
        shown = "—" if v is None else (f"{v:.6f}" if isinstance(v, float) else str(v))
        bt = bar_times.get(rid, when)
        opt = " *(optional)*" if rid in OPTIONAL else ""
        lines.append(f"| {rid} | {sym}{opt} | {tf} | {qty} | {bt} | `{shown}` |  |  |  |")

    lines += [
        "",
        f"**{len(ROWS)} cells.** 24 current-bar, 4 historical (~30 days back, to catch "
        "warm-up and window drift rather than testing only the newest value).",
        "",
        "> **Anchored-VWAP band caveat.** Rows R18 uses the same volume-weighted "
        "population variance as the rolling form. That is a reasoned inference from "
        "shared TradingView band machinery — **to be confirmed by reading the "
        "anchored-VWAP source**, never asserted. If R18 mismatches while R22 matches, "
        "this inference is the first thing to suspect.",
        "",
        "> **If an RVWAP row mismatches by a small amount**, test the window boundary "
        "first (membership is `bar_open_time > current_bar_open_time − W`, current bar "
        "included) and the 10-bar floor at gaps second.",
    ]
    return "\n".join(lines) + "\n"
