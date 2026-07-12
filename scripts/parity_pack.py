"""D5: the parity pack for operator sign-off (fixture F6).

Produces, under research_outputs/parity/:
- crosses_4h.csv / crosses_12h.csv — every confirmed BTC governor 9/89 cross
  in the parity window (2025-10-06 -> 2026-07-07): confirm timestamp (the
  cross bar's CLOSE, UTC — the moment the arrow's bar closes on TradingView),
  direction, tier (full = stage-aligned, provisional = counter-structure).
- case_windows.md — the engine's event sequences for the six named case
  windows, from a v11_faithful replay of BTCUSDT_swing over the full parity
  window, formatted for bar-by-bar TradingView comparison.

Acceptance is the OPERATOR's: check the lists and windows against
TradingView with the chart timezone set to UTC. Tolerances (F6): cross
timestamps exact to the bar; EMA/ATR values within 0.05% after warm-up.

  python scripts/parity_pack.py [--backfill]
"""

import argparse
import csv
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine import data as dl
from engine import indicators as ind
from engine.config import load_config
from engine.journal import iso, read_journal
from engine.replay import parse_utc, run_replay

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "research_outputs" / "parity"
WINDOW_START, WINDOW_END = "2025-10-06", "2026-07-07"

CASE_WINDOWS = [
    ("May 16 -> 26 '26 — the marquee short",   "2026-05-15", "2026-05-27"),
    ("Jul 2 -> 6 '26 — provisional longs",     "2026-07-01", "2026-07-07"),
    ("Jun 14 - 16 '26 — the provisional trap", "2026-06-13", "2026-06-17"),
    ("Jun 22 '26 — Capitulation V",            "2026-06-21", "2026-06-23"),
    ("Feb 6 '26 — Capitulation V",             "2026-02-05", "2026-02-07"),
    ("Dec 4 - 13 '25 — chop / whipsaw",        "2025-12-04", "2025-12-14"),
]
# events worth eyeballing on the chart (REJECT/CLUSTER excluded as noise)
CASE_EVENTS = ["REGIME", "STAGE", "PRIME", "CONFIRM", "V", "TPW", "X"]


def write_cross_list(interval: str, p: dict) -> int:
    first = dl.detect_first_candle("BTCUSDT", interval)
    gov = dl.load_klines("BTCUSDT", interval, first, parse_utc(WINDOW_END) + 86_400_000)
    c = gov["close"].to_numpy(float)
    e9 = ind.ema(c, p["len_fast"])
    e89 = ind.ema(c, p["len_slow"])
    e200 = ind.ema(c, p["len_trend"])
    bx = ind.crossover(e9, e89)
    sx = ind.crossunder(e9, e89)
    open_ms = gov["open_time"].to_numpy(np.int64)
    step = {"4h": 14_400_000, "12h": 43_200_000}[interval]
    lo, hi = parse_utc(WINDOW_START), parse_utc(WINDOW_END) + 86_400_000

    rows = []
    for i in np.nonzero(bx | sx)[0]:
        close_ms = int(open_ms[i]) + step
        if not (lo <= close_ms <= hi):
            continue
        is_long = bool(bx[i])
        aligned = (e89[i] > e200[i]) if is_long else (e89[i] < e200[i])
        rows.append({
            "ts_close_utc": iso(close_ms),
            "direction": "long" if is_long else "short",
            "tier": "full" if aligned else "provisional",
            "close_px": round(float(c[i]), 2),
            "e9": round(float(e9[i]), 2),
            "e89": round(float(e89[i]), 2),
            "e200": round(float(e200[i]), 2),
        })
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"crosses_{interval}.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"-> {path}  ({len(rows)} crosses)")
    return len(rows)


def write_case_windows(journal_root: Path) -> None:
    rows = read_journal(journal_root, "BTCUSDT_swing")
    lines = [
        "# D5 case windows — engine event sequences (v11_faithful, BTCUSDT_swing)",
        "",
        f"Replay window {WINDOW_START} -> {WINDOW_END} (the spent window — "
        "plumbing check only, never evidence). Exec = 5m chart, governor = "
        "4H, per the swing mandate.",
        "",
        "**How to check (operator sign-off for F6):** open BTCUSDT.P "
        "(Binance) on TradingView, 5m chart, SS Cascade v11.0.2 with the verified inputs "
        "(**Zone memory = 3** — the input default — all other inputs at "
        "their .pine defaults; see fixtures/pine_defaults_manifest.yaml), "
        "**chart timezone UTC**. For each table below, step through "
        "the bars and confirm the same events print on the same bars (a "
        "REGIME row here = the bar where the governor cross first becomes "
        "visible on the exec chart; TradingView may paint the arrow across "
        "the whole following governor bar). Grades and zones must match "
        "exactly; stop levels within 0.05%.",
        "",
        "Whipsaw-suppressed arrows: REGIME rows carry `arrow_visible` — when "
        "false, TradingView shows no arrow (the tint still flips; that is "
        "the whipsaw display filter, arming is unaffected).",
        "",
    ]
    for title, lo, hi in CASE_WINDOWS:
        lines += [f"## {title}", "",
                  "| bar open (UTC) | evt | dir | grade | zone | rc | tier | stage | retr | stop | arrow |",
                  "|---|---|---|---|---|---|---|---|---|---|---|"]
        n = 0
        for r in rows:
            if r["evt"] not in CASE_EVENTS:
                continue
            if not (lo <= r["ts_open"][:10] <= hi):
                continue
            flags = r.get("engagement_flags") or {}
            arrow = ("shown" if flags.get("arrow_visible") else "hidden") \
                if r["evt"] == "REGIME" else ""
            lines.append(
                f"| {r['ts_open']} | {r['evt']} | {r['dir']} | {r['grade']} "
                f"| {r['zone']} | {r['rc']} | {r['tier']} | {r['stage']} "
                f"| {r['retr'] if r['retr'] is not None else '-'} "
                f"| {r['stop'] if r['stop'] is not None else '-'} | {arrow} |")
            n += 1
        lines += ["", f"*{n} events in this window.*", ""]
    lines += [
        "---", "",
        "## Known open parity question for sign-off: the two V signatures",
        "",
        "This 5m replay prints **no Capitulation V on Feb 6 or Jun 22**. The "
        "builder's diagnostic found the climax bars present on both days "
        "(Feb 5–6: multiple red bars ≥3.5× volume MA, lows 6–9 governor-ATRs "
        "beyond the governor 89), but the far-band reclaim can then never "
        "arrive within capWindow = 10 **5m** bars (50 minutes) — in this "
        "engine *and* in the Pine's arithmetic, which are line-identical for "
        "this gate. On a **4H exec chart** the same 10-bar window is 40 "
        "hours, and the doctrine's Feb 6 observation predates the study's 5m "
        "era (Playbook §12: 5m evidence from Apr 26 '26 on).",
        "",
        "**Operator: please check Feb 6 and Jun 22 on BOTH charts** — the 5m "
        "(governor input 240) and the plain 4H chart — and note which one "
        "actually prints the V arrow. If the V only prints on the 4H chart, "
        "this engine is faithful and the signature list simply refers to the "
        "governor-chart view; if TradingView prints it on the 5m chart, "
        "paste the bar timestamp and the builder will trace the gate "
        "bar-by-bar.",
        "",
        "*Numeric tolerance (F6): cross timestamps exact to the bar; EMA/ATR "
        "within 0.05% after F7 warm-up. Sign-off = the operator confirms the "
        "two cross lists and these six windows against TradingView.*",
    ]
    path = OUT / "case_windows.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"-> {path}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--backfill", action="store_true")
    ap.add_argument("--journal-root", default=str(ROOT / "research_outputs" / "parity" / "journal"))
    args = ap.parse_args()

    p = load_config("v11_faithful")["signal"]
    write_cross_list("4h", p)
    write_cross_list("12h", p)

    print("replaying BTCUSDT_swing (v11_faithful) over the parity window...")
    summary = run_replay("v11_faithful", "BTCUSDT_swing", WINDOW_START,
                         WINDOW_END, Path(args.journal_root),
                         backfill=args.backfill)
    print(f"   {summary['signal_events']} signal events, "
          f"journal {summary['journal_sha256'][:16]}...")
    write_case_windows(Path(args.journal_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
