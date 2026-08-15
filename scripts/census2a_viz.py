#!/usr/bin/env python
"""CENSUS-2A · VIZ-1 -- payload extraction + first-pass renders.

CLASS: DISPLAY-ONLY / Tier-E exploration. No scored tables, no claims, no
registrations. Selection surface m = 0 -- nothing here is compared for promotion.

WHY THE RENDERS ARE HAND-ROLLED SVG. Neither matplotlib nor plotly is installed
in this environment, and installing a package to draw a picture is not a thing to
do unasked. Raw SVG has no dependency to inline and no external fetch to block,
which is what the brief's iron rule 6 actually asks for. The cost is that these
are first-pass renders: honest, legible, unornamented. Design's versions sit
BESIDE them and never replace them.

THE TOLL IS ALWAYS VISIBLE (brief rule 3): every outcome axis shades
+/-[toll_lo, toll_hi] = [0.0263, 0.0594] ATR, the per-asset band measured at
armings in CEN-3. Profit smaller than cost must LOOK like what it is.
"""
from __future__ import annotations
import hashlib, json, math, os, shutil, sys
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
SEED = 20260812
B = ROOT / "research_outputs" / "census2a"
PAY = B / "viz_payloads"; VIZ = B / "viz"; HAND = B / "DESIGN_HANDOFF"
TOLL_LO, TOLL_HI = 0.0263, 0.0594
GEN = datetime.now(timezone.utc).strftime("%Y-%m-%d")
MAX_BYTES = 700_000
V6_GAP = ("v6 TAIL GARDEN: `mae_r` and `n_reclaims` do not exist in cen5_campaigns.parquet. "
          "Emitted as null. The spec's reclaim ticks on stems cannot be drawn, and the "
          "MFE/|MAE| quality glyph is unavailable for this view.")
PANEL = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT"]

MAN = json.loads((B / "census2a_manifest.json").read_text(encoding="utf-8"))
ART = MAN.get("artifacts", {})


def src_meta(*names):
    return [{"parquet": n, "sha256": ART.get(n, {}).get("sha256"),
             "rows": ART.get(n, {}).get("rows")} for n in names]


def assert_key(df, keys, label):
    dup = int(df.duplicated(subset=keys).sum())
    print(f"    F-KEY  {label:30} key={keys} rows={len(df):,} dup={dup}")
    if dup:
        raise SystemExit(f"HALT (F-KEY): {label} key {keys} not unique ({dup} dups)")


def jclean(o):
    """NaN/inf are not JSON. Emit null so a payload always round-trips."""
    if isinstance(o, dict):
        return {k: jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating, float)):
        f = float(o)
        return None if (math.isnan(f) or math.isinf(f)) else round(f, 6)
    if isinstance(o, (np.bool_, bool)):
        return bool(o)
    return o


def write_payload(name, data, sources, downsample_rule=None, note=None):
    """Emit one payload with meta{sha256 OF ITS OWN DATA BLOCK, ...}."""
    data = jclean(data)
    blob = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    sha = hashlib.sha256(blob).hexdigest()
    def _n(o):
        if isinstance(o, list):
            return len(o)
        if isinstance(o, dict):
            return sum(_n(v) for v in o.values())
        return 0
    rows = _n(data)
    doc = {"meta": {"payload": name, "sha256": sha, "rows": rows,
                    "source_parquet": sources,
                    "toll_lo": TOLL_LO, "toll_hi": TOLL_HI,
                    "generated": GEN, "seed": SEED,
                    "class": "DISPLAY-ONLY / Tier-E exploration",
                    "downsample_rule": downsample_rule, "note": note},
           "data": data}
    p = PAY / name
    p.write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")
    sz = p.stat().st_size
    flag = "  !! OVER CAP" if sz > MAX_BYTES else ""
    print(f"    {name:20} rows={rows:>7,}  {sz:>9,} B  sha {sha[:12]}{flag}")
    return {"payload": name, "rows": rows, "bytes": sz, "sha256": sha,
            "over_cap": sz > MAX_BYTES}


# ===========================================================================
# SVG primitives -- no dependency, no external fetch
# ===========================================================================
W, H = 1180, 620
PADL, PADR, PADT, PADB = 78, 34, 58, 62
BG, FG, GRID, MUT = "#0e1117", "#e6edf3", "#232b36", "#7d8896"
POS, NEG = "#3fb950", "#f85149"          # diverging, anchored at zero
TOLLC = "#f0b72f"


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def lerp_col(t):
    """Diverging at zero: red (t=-1) -> muted (0) -> green (+1)."""
    t = max(-1.0, min(1.0, t))
    if t >= 0:
        a = t
        return f"rgb({int(125+(63-125)*a)},{int(136+(185-136)*a)},{int(150+(80-150)*a)})"
    a = -t
    return f"rgb({int(125+(248-125)*a)},{int(136+(81-136)*a)},{int(150+(73-150)*a)})"


class Canvas:
    def __init__(self, w=W, h=H):
        self.w, self.h, self.p = w, h, []
    def add(self, s): self.p.append(s)
    def rect(self, x, y, w, h, fill, op=1.0, stroke="none"):
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w,0):.1f}" height="{max(h,0):.1f}" '
                 f'fill="{fill}" fill-opacity="{op}" stroke="{stroke}"/>')
    def line(self, x1, y1, x2, y2, c=GRID, w=1, op=1.0, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'stroke="{c}" stroke-width="{w}" stroke-opacity="{op}"{d}/>')
    def circ(self, x, y, r, fill, op=0.85, stroke="none", sw=0):
        self.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{fill}" '
                 f'fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>')
    def text(self, x, y, s, c=FG, size=12, anchor="start", weight="normal", op=1.0):
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" '
                 f'text-anchor="{anchor}" font-weight="{weight}" fill-opacity="{op}" '
                 f'font-family="ui-monospace,Menlo,Consolas,monospace">{esc(s)}</text>')
    def path(self, d, fill="none", stroke=FG, w=1, op=1.0):
        self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" '
                 f'fill-opacity="{op}" stroke-opacity="{op}"/>')
    def svg(self):
        return (f'<svg viewBox="0 0 {self.w} {self.h}" width="100%" '
                f'xmlns="http://www.w3.org/2000/svg" style="background:{BG}">'
                + "".join(self.p) + "</svg>")


def frame(c, title, q, xlab, ylab):
    c.rect(0, 0, c.w, c.h, BG)
    c.text(PADL - 56, 26, title, size=17, weight="600")
    c.text(c.w - PADR, 26, "Q: " + q, c=TOLLC, size=12, anchor="end")
    c.text(PADL - 56, 44, "DISPLAY-ONLY · Tier-E · no claim is made or implied",
           c=MUT, size=10)
    c.text(c.w / 2, c.h - 20, xlab, c=MUT, size=11, anchor="middle")
    c.add(f'<text x="18" y="{c.h/2:.0f}" fill="{MUT}" font-size="11" '
          f'text-anchor="middle" transform="rotate(-90 18 {c.h/2:.0f})" '
          f'font-family="ui-monospace,monospace">{esc(ylab)}</text>')


def axes(c, x0, x1, y0, y1, xmin, xmax, ymin, ymax, xticks=6, yticks=6, xfmt="{:.2f}"):
    for i in range(yticks + 1):
        v = ymin + (ymax - ymin) * i / yticks
        y = y1 - (y1 - y0) * i / yticks
        c.line(x0, y, x1, y, GRID, 1, 0.7)
        c.text(x0 - 8, y + 4, f"{v:.2f}", c=MUT, size=10, anchor="end")
    for i in range(xticks + 1):
        v = xmin + (xmax - xmin) * i / xticks
        x = x0 + (x1 - x0) * i / xticks
        c.line(x, y0, x, y1, GRID, 1, 0.45)
        c.text(x, y1 + 16, xfmt.format(v), c=MUT, size=10, anchor="middle")


def toll_band(c, x0, x1, y0, y1, ymin, ymax, horizontal=True):
    """Rule 3: shade +/-[toll_lo, toll_hi] on every outcome axis."""
    def sy(v): return y1 - (y1 - y0) * (v - ymin) / (ymax - ymin + 1e-12)
    for sgn in (1, -1):
        a, b = sy(sgn * TOLL_LO), sy(sgn * TOLL_HI)
        c.rect(x0, min(a, b), x1 - x0, abs(a - b), TOLLC, 0.16)
    c.line(x0, sy(0), x1, sy(0), MUT, 1.4, 0.9, dash="4 3")
    c.text(x1 - 4, sy(0) - 6, "toll band ±0.026–0.059 ATR", c=TOLLC, size=10, anchor="end")


FOOTER = ('DISPLAY-ONLY · Tier-E exploration · CENSUS-2A payload {name} sha256 {sha} · '
          'evidence era ≤ 2024-07-01 · no claim is made or implied; promotion requires '
          'registration (see CENSUS2A_CLOSEOUT_2026-08-12.md §5). '
          'Rendered by HEPHAESTUS first-pass, {date}.')


def page(fn, title, q, svg, payload_name, sha, note=""):
    foot = FOOTER.format(name=payload_name, sha=sha, date=GEN)
    html = f"""<!doctype html><meta charset="utf-8"><title>{esc(title)}</title>
<style>body{{background:{BG};color:{FG};font-family:ui-monospace,Menlo,Consolas,monospace;
margin:0;padding:22px}}.w{{max-width:1240px;margin:0 auto}}h1{{font-size:19px;margin:0 0 4px}}
.q{{color:{TOLLC};font-size:13px;margin:0 0 14px}}.n{{color:{MUT};font-size:12px;margin:12px 0}}
.f{{color:{MUT};font-size:10.5px;line-height:1.6;border-top:1px solid {GRID};
margin-top:18px;padding-top:12px}}a{{color:{TOLLC}}}</style>
<div class="w"><h1>{esc(title)}</h1><p class="q">Q: {esc(q)}</p>{svg}
<p class="n">{esc(note)}</p><p class="f">{esc(foot)}</p>
<p class="f"><a href="viz_index.html">← back to the nine views</a></p></div>"""
    (VIZ / fn).write_text(html, encoding="utf-8")
    return fn


# ===========================================================================
# THE NINE PAYLOADS
# ===========================================================================
def extract():
    PAY.mkdir(parents=True, exist_ok=True); VIZ.mkdir(parents=True, exist_ok=True)
    inv, gaps = [], []
    print("VIZ-1 -- payload extraction (Tier-E, selection surface m=0)")
    import mc2_program as MC2

    led = pd.read_parquet(B / "cen3" / "cen3_ledger_lensed.parquet")
    assert_key(led, ["asset", "arming_ts"], "cen3_ledger_lensed")

    # ---- V1 ARMING SKY
    disp = {}
    for sym in PANEL:
        d = MC2.frame(sym, "4h", "evidence")
        c = d["close"].to_numpy(float); e = d["e89"].to_numpy(float); a = d["atr"].to_numpy(float)
        with np.errstate(invalid="ignore", divide="ignore"):
            disp[sym] = np.abs(c - e) / a
    v1 = []
    for r in led.itertuples(index=False):
        arr = disp.get(r.asset)
        dv = float(arr[r.arming_idx]) if (arr is not None and r.arming_idx < len(arr)) else None
        v1.append({"asset": r.asset, "dir": r.dir, "displacement_atr": dv,
                   "terminal_h100": r.term_H100, "fate": r.fate,
                   "stamp_score": int(r.stamp_score), "window_bars": r.window_width_bars})
    inv.append(write_payload("v1_armings.json", v1, src_meta("cen3_ledger_lensed"), None,
        "displacement_atr recomputed as |close-e89|/ATR at the arming (the continuous form of "
        "the WALL stamp); it is not stored in any parquet"))

    # ---- V2 RELAY RIVERS
    seen = {}
    for r in led.itertuples(index=False):
        st = ("sealed<=6" if (r.SEALED and (r.seal_lag_bars or 99) <= 6)
              else "sealed-late" if r.SEALED else "unsealed")
        tc = r.trigger_class or "no-trigger"
        t = r.term_H100
        ob = ("loss" if (t or 0) < -TOLL_HI else "flat(in-toll)" if abs(t or 0) <= TOLL_HI else "win")
        for a, b in (("arming", tc), (tc, st), (st, r.fate), (r.fate, ob)):
            seen.setdefault((a, b), []).append(t)
    lk = []
    for (a, b), t in seen.items():
        tt = [x for x in t if x is not None and not math.isnan(x)]
        lk.append({"source": a, "target": b, "count": len(t),
                   "median_terminal": float(np.median(tt)) if tt else None,
                   "is_may26_analog": bool(a == "12_25" or b == "12_25")})
    nodes = sorted({x["source"] for x in lk} | {x["target"] for x in lk})
    inv.append(write_payload("v2_flows.json", {"nodes": [{"id": n} for n in nodes], "links": lk},
        src_meta("cen3_ledger_lensed"), None,
        "may26 analog flagged on any path through the 12_25 trigger class"))

    # ---- V3 LAG CLOCK
    v3t = [{"class": r.trigger_class, "lag_bars": r.trigger_lag_bars,
            "terminal_h100": r.term_H100, "asset": r.asset}
           for r in led.itertuples(index=False)
           if r.has_trigger and r.trigger_lag_bars is not None]
    v3s = [{"lag_bars": r.seal_lag_bars} for r in led.itertuples(index=False)
           if r.SEALED and r.seal_lag_bars is not None]
    inv.append(write_payload("v3_lags.json", {"triggers": v3t, "seals": v3s},
        src_meta("cen3_ledger_lensed")))

    # ---- V4 KNOT->FAN CINEMA
    FAN6 = [9, 89, 200, 300, 450, 500]
    v4 = {}; rule = "rank-change points only"
    for sym in PANEL:
        d = MC2.frame(sym, "4h", "evidence")
        o = d["open_time"].to_numpy(np.int64)
        stack = np.vstack([d["e%d" % L].to_numpy(float) for L in FAN6])
        warm = np.isfinite(stack).all(axis=0)
        ranks = np.argsort(np.argsort(-stack, axis=0), axis=0)
        c = d["close"].to_numpy(float); av = d["atr"].to_numpy(float)
        fwd = np.full(len(c), np.nan)
        with np.errstate(invalid="ignore", divide="ignore"):
            fwd[:-2] = (c[2:] - c[:-2]) / np.where(av[:-2] > 0, av[:-2], np.nan)
        kn = np.vstack([d["e%d" % L].to_numpy(float) for L in [89, 200, 300, 450, 500]])
        kw = np.isfinite(kn).all(axis=0)
        spread = kn.max(axis=0) - kn.min(axis=0)
        knot = kw & np.isfinite(av) & (av > 0) & (spread < 0.5 * av)
        dfan = np.diff(stack, axis=0)
        fan = warm & (((dfan < 0).all(axis=0)) | ((dfan > 0).all(axis=0)))
        chg = np.ones(len(o), bool)
        chg[1:] = (ranks[:, 1:] != ranks[:, :-1]).any(axis=0)
        idx = np.nonzero(warm & chg)[0]
        if len(idx) > 3000:
            idx = idx[np.linspace(0, len(idx) - 1, 3000).astype(int)]
            rule = ("rank-change points, then evenly-spaced cap at 3000/asset "
                    "(deterministic, order-preserving)")
        v4[sym] = [{"ts": int(o[i]), "ranks": [int(x) for x in ranks[:, i]],
                    "knot_flag": bool(knot[i]), "fan_flag": bool(fan[i]),
                    "fwd_h100": (None if not np.isfinite(fwd[i]) else float(fwd[i]))}
                   for i in idx]
    inv.append(write_payload("v4_braid.json", v4, src_meta("cen1_events"), rule,
        "ranks recomputed from the 4h frames; cen1_events carries FAN/KNOT but not ranks"))

    # ---- V5 REFUSAL WEATHER
    ep = pd.read_parquet(B / "cen6" / "cen6_episodes.parquet")
    ref = pd.read_parquet(B / "cen1" / "cen1_refusals.parquet",
                          columns=["asset", "tf", "limb", "ts"])
    ref = ref[(ref.limb == "i-b") & ref.asset.isin(PANEL)]
    TFMS = {"1h": 3600000, "4h": 14400000, "12h": 43200000}
    v5 = []
    for member in ["1h", "4h", "12h"]:
        g = ep[ep.member == member]; span = TFMS[member]
        for sym, gg in g.groupby("asset", sort=True):
            rt = np.sort(ref[(ref.asset == sym) & (ref.tf == member)].ts.to_numpy(np.int64))
            if not len(rt):
                continue
            for r in gg.itertuples(index=False):
                cells = []
                for k in range(-10, 1):
                    lo_t = r.ts + (k - 1) * span; hi_t = r.ts + k * span
                    cells.append(int(np.searchsorted(rt, hi_t, "left")
                                     - np.searchsorted(rt, lo_t, "left")))
                v5.append({"kind": ("accept" if r.verdict == "ACCEPTED" else "reclaim"),
                           "member": member, "asset": sym, "ts": int(r.ts),
                           "depth_atr": r.depth_atr, "cells": cells})
    r5 = None
    if len(v5) > 4500:
        v5 = [v5[i] for i in np.linspace(0, len(v5) - 1, 4500).astype(int)]
        r5 = "evenly-spaced cap at 4500 episodes (deterministic, order-preserving)"
    inv.append(write_payload("v5_weather.json", v5,
        src_meta("cen6_episodes", "cen1_refusals"), r5,
        "cells[-10..0] = i-b refusal COUNT per member bar in the 10 bars before the episode"))

    # ---- V6 TAIL GARDEN
    camp = pd.read_parquet(B / "cen5" / "cen5_campaigns.parquet")
    assert_key(camp, ["tranche_id"], "cen5_campaigns")
    v6 = [{"asset": r.asset, "dir": r.dir, "mandate": r.mandate, "mfe_r": r.mfe_R,
           "mae_r": None, "terminal_r": r.ride_R, "give_back_r": r.give_back_R,
           "n_reclaims": None, "is_winner": bool(r.outcome_sign == "win")}
          for r in camp.itertuples(index=False)]
    r6 = None
    if len(v6) > 4000:
        v6 = sorted(v6, key=lambda x: -(x["mfe_r"] if x["mfe_r"] is not None else -9e9))[:4000]
        r6 = "top 4000 by MFE (the view sorts by MFE and the tail is its subject); cap set by the 700 KB payload limit"
    inv.append(write_payload("v6_campaigns.json", v6, src_meta("cen5_campaigns"), r6,
        "mae_r and n_reclaims are NOT in cen5_campaigns -- emitted null, never invented"))
    gaps.append(V6_GAP)

    # ---- V7 CLOCK DUEL
    ctl = pd.read_parquet(B / "cen9" / "cen9_control_instants.parquet")
    cmpd = pd.read_parquet(B / "cen9" / "cen9_comparison.parquet")
    v7 = []
    for r in cmpd.itertuples(index=False):
        s = ctl.loc[ctl.anchor == r.anchor, "term_H100"].dropna()
        v7.append({"name": r.anchor, "n": int(r.n), "median": r.median_term_H100,
                   "distribution_deciles": ([float(np.percentile(s, q)) for q in range(10, 100, 10)]
                                            if len(s) > 20 else [])})
    s = led["term_H100"].dropna()
    v7.append({"name": "EMA-anchored armings (reference)", "n": int(len(s)),
               "median": float(s.median()),
               "distribution_deciles": [float(np.percentile(s, q)) for q in range(10, 100, 10)]})
    inv.append(write_payload("v7_anchors.json", v7,
        src_meta("cen9_comparison", "cen9_control_instants", "cen3_ledger_lensed")))

    # ---- V8 WALL SONAR
    reg = pd.read_parquet(B / "cen7" / "cen7_registry_series.parquet")
    colo = pd.read_parquet(B / "cen7" / "cen7_colocation.parquet")
    assert_key(reg, ["asset", "ts"], "cen7_registry_series")
    dcols = [c for c in reg.columns if c.startswith("dist_") and c.endswith("_atr")]
    ev = reg[reg.kind == "event"]
    r8 = None
    if len(ev) > 700:
        ev = ev.iloc[np.linspace(0, len(ev) - 1, 700).astype(int)]
        r8 = "evenly-spaced cap at 700 event instants (deterministic)"
    pings = []
    for _, r in ev.iterrows():
        lv = []
        for cn in dcols:
            val = r[cn]
            if val is not None and np.isfinite(val) and val < 6:
                lv.append({"family": cn[5:-4], "dist_atr": float(val)})
        pings.append({"asset": r["asset"], "ts": int(r["ts"]), "levels": lv})
    hist = colo.colocation_n.value_counts().sort_index()
    inv.append(write_payload("v8_sonar.json",
        {"armings": pings, "band_atr": 0.15,
         "colocation_histogram": [{"n_levels_in_band": int(k), "count": int(v)}
                                  for k, v in hist.items()]},
        src_meta("cen7_registry_series", "cen7_colocation"), r8))

    # ---- V9 VERDICT TIDES
    v9 = {}
    for member in ["1h", "4h", "12h"]:
        g = ep[ep.member == member].sort_values("ts")
        eps = [{"ts": int(r.ts), "asset": r.asset, "verdict": r.verdict,
                "depth_atr": r.depth_atr, "trap_48h": bool(r.trap_48h)}
               for r in g.itertuples(index=False)]
        runs, cur, n = [], None, 0
        for e in eps:
            if e["verdict"] == cur:
                n += 1
            else:
                if cur:
                    runs.append({"verdict": cur, "length": n})
                cur, n = e["verdict"], 1
        if cur:
            runs.append({"verdict": cur, "length": n})
        v9[member] = {"episodes": eps, "hysteresis_runs": runs}
    inv.append(write_payload("v9_tides.json", v9, src_meta("cen6_episodes")))

    # ---- F-V1
    print("\n  F-V1 payload integrity:")
    for it in inv:
        doc = json.loads((PAY / it["payload"]).read_text(encoding="utf-8"))
        blob = json.dumps(doc["data"], sort_keys=True, separators=(",", ":")).encode("utf-8")
        ok = hashlib.sha256(blob).hexdigest() == doc["meta"]["sha256"]
        print("    %s  %-20s round-trip + sha verify" % ("PASS" if ok else "FAIL", it["payload"]))
        if not ok:
            raise SystemExit("HALT (F-V1): %s sha mismatch" % it["payload"])
    over = [i["payload"] for i in inv if i["over_cap"]]
    print("    %s  size cap <= %s B  %s" % ("PASS" if not over else "FAIL",
          format(MAX_BYTES, ","), "(all under)" if not over else over))
    return inv, gaps


# ===========================================================================
# RENDERS -- V1..V9 + index.  Hand-rolled SVG, self-contained, no fetches.
# ===========================================================================
def load(name):
    d = json.loads((PAY / name).read_text(encoding="utf-8"))
    return d["meta"], d["data"]


VIEWS = [
    ("V1", "ARMING SKY", "where do profitable armings live — and is proximity to the line really poison?"),
    ("V2", "RELAY RIVERS", "which routes through the window carry the money?"),
    ("V3", "LAG CLOCK", "is there a golden hour inside the window?"),
    ("V4", "KNOT→FAN CINEMA", "once 200 and 300 clear the 500, do they really never look back — and is that persistence paid?"),
    ("V5", "REFUSAL WEATHER", "what does the air look like before a trap versus before a real breakout?"),
    ("V6", "TAIL GARDEN", "where does the +9.4R tail live, and what does giving it back look like?"),
    ("V7", "CLOCK DUEL", "how much of our clock's edge survives the toll — and who beats it?"),
    ("V8", "WALL SONAR", "is confluence a crowd — or one wall that matters?"),
    ("V9", "VERDICT TIDES", "which close is calm water, and which is chop?"),
]


def clampq(vals, lo=2, hi=98):
    v = [x for x in vals if x is not None and not math.isnan(x)]
    if not v:
        return -1.0, 1.0
    return float(np.percentile(v, lo)), float(np.percentile(v, hi))


def render_all():
    out = []

    # ---------- V1 ARMING SKY ----------
    m, d = load("v1_armings.json")
    c = Canvas(); frame(c, "V1 · ARMING SKY", VIEWS[0][2],
                        "displacement at the arming  |close − e89| / ATR",
                        "terminal return H100 (ATR)")
    x0, x1, y0, y1 = PADL, c.w - PADR, PADT, c.h - PADB
    xs = [r["displacement_atr"] for r in d]; ys = [r["terminal_h100"] for r in d]
    xmin, xmax = 0.0, min(3.0, clampq(xs)[1]); ymin, ymax = clampq(ys, 1, 99)
    ymax = max(ymax, 0.6); ymin = min(ymin, -0.6)
    axes(c, x0, x1, y0, y1, xmin, xmax, ymin, ymax)
    toll_band(c, x0, x1, y0, y1, ymin, ymax)
    GL = {"COMPLETED": 3.6, "ABORTED": 2.4, "ROTTED": 5.0}
    for r in d:
        if r["displacement_atr"] is None or r["terminal_h100"] is None:
            continue
        px = x0 + (x1 - x0) * (min(r["displacement_atr"], xmax) - xmin) / (xmax - xmin)
        py = y1 - (y1 - y0) * (max(min(r["terminal_h100"], ymax), ymin) - ymin) / (ymax - ymin)
        col = lerp_col(max(-1, min(1, r["terminal_h100"] / 1.5)))
        if r["stamp_score"] >= 2:
            c.circ(px, py, GL.get(r["fate"], 3) + 3.4, TOLLC, 0.13)
        c.circ(px, py, GL.get(r["fate"], 3), col, 0.8)
    lx = x1 - 250
    c.text(lx, y0 + 14, "glyph size = fate  ·  halo = stamp score ≥2", c=MUT, size=10)
    for i, (k, r_) in enumerate(GL.items()):
        c.circ(lx + 10, y0 + 32 + i * 16, r_, MUT, 0.75)
        c.text(lx + 24, y0 + 36 + i * 16, k, c=MUT, size=10)
    out.append(page("V1.html", "V1 · ARMING SKY", VIEWS[0][2], c.svg(), m["payload"], m["sha256"],
                    "Colour = terminal outcome, diverging at zero. The toll band is the "
                    "horizontal gold stripe: anything inside it is smaller than its own cost."))

    # ---------- V2 RELAY RIVERS ----------
    m, d = load("v2_flows.json")
    c = Canvas(); frame(c, "V2 · RELAY RIVERS", VIEWS[1][2],
                        "arming → trigger class → seal timing → fate → outcome bucket",
                        "flow width = count")
    cols = [["arming"],
            sorted({l["target"] for l in d["links"] if l["source"] == "arming"}),
            sorted({l["target"] for l in d["links"]
                    if l["source"] in {"12_25", "25_89", "no-trigger"}}),
            ["COMPLETED", "ABORTED", "ROTTED"],
            ["win", "flat(in-toll)", "loss"]]
    xpos = [PADL + i * ((c.w - PADL - PADR) / 4) for i in range(5)]
    ypos = {}
    for ci, col in enumerate(cols):
        for i, nd in enumerate(col):
            ypos[nd] = PADT + 60 + i * ((c.h - PADT - PADB - 80) / max(len(col), 1))
    mx = max(l["count"] for l in d["links"])
    for l in d["links"]:
        if l["source"] not in ypos or l["target"] not in ypos:
            continue
        si = next((i for i, col in enumerate(cols) if l["source"] in col), None)
        ti = next((i for i, col in enumerate(cols) if l["target"] in col), None)
        if si is None or ti is None or ti != si + 1:
            continue
        xa, xb = xpos[si] + 60, xpos[ti]
        ya, yb = ypos[l["source"]], ypos[l["target"]]
        wdt = 1 + 13 * (l["count"] / mx)
        mt = l["median_terminal"]
        col = lerp_col(0 if mt is None else max(-1, min(1, mt / 1.0)))
        op = 0.85 if l["is_may26_analog"] else 0.42
        c.path(f"M{xa:.0f},{ya:.0f} C{(xa+xb)/2:.0f},{ya:.0f} {(xa+xb)/2:.0f},{yb:.0f} {xb:.0f},{yb:.0f}",
               "none", col, wdt, op)
    for ci, col in enumerate(cols):
        for nd in col:
            c.rect(xpos[ci], ypos[nd] - 9, 58, 18, "#1b222c", 1, GRID)
            c.text(xpos[ci] + 4, ypos[nd] + 4, str(nd)[:9], size=10)
    c.text(PADL, c.h - PADB + 34, "bright = path through 12_25 (the May-26 analog) · "
           "colour = median terminal outcome", c=MUT, size=10)
    out.append(page("V2.html", "V2 · RELAY RIVERS", VIEWS[1][2], c.svg(), m["payload"], m["sha256"],
                    "Thickness is population, not profit. A fat pale river is a common route "
                    "that pays nothing."))

    # ---------- V3 LAG CLOCK ----------
    m, d = load("v3_lags.json")
    c = Canvas(); frame(c, "V3 · LAG CLOCK", VIEWS[2][2],
                        "log10 lag from arming (4h bars) — angle", "terminal H100 (ATR) — radius")
    cx, cy, R = c.w / 2, c.h / 2 + 8, 232
    lags = [t["lag_bars"] for t in d["triggers"] if t["lag_bars"]]
    lmax = max(lags) if lags else 1
    for rr, lab in ((R * 0.34, "toll"), (R * 0.62, ""), (R, "")):
        c.add(f'<circle cx="{cx}" cy="{cy}" r="{rr:.0f}" fill="none" stroke="{GRID}" '
              f'stroke-width="1" stroke-opacity="0.8"/>')
    c.add(f'<circle cx="{cx}" cy="{cy}" r="{R*0.34:.0f}" fill="{TOLLC}" fill-opacity="0.13"/>')
    c.text(cx, cy - R * 0.34 - 6, "inside this ring the move is smaller than the toll",
           c=TOLLC, size=10, anchor="middle")
    for t in d["triggers"]:
        lg, tm = t["lag_bars"], t["terminal_h100"]
        if not lg or tm is None or lg <= 0:
            continue
        ang = 2 * math.pi * (math.log10(lg + 1) / math.log10(lmax + 1)) - math.pi / 2
        rad = R * 0.34 + (R - R * 0.34) * min(abs(tm) / 1.5, 1.0)
        px, py = cx + rad * math.cos(ang), cy + rad * math.sin(ang)
        c.circ(px, py, 3.0 if t["class"] == "12_25" else 2.2,
               lerp_col(max(-1, min(1, tm / 1.5))), 0.8)
    seals = [s["lag_bars"] for s in d["seals"] if s["lag_bars"]]
    if seals:
        ms = float(np.median(seals))
        ang = 2 * math.pi * (math.log10(ms + 1) / math.log10(lmax + 1)) - math.pi / 2
        c.line(cx, cy, cx + R * math.cos(ang), cy + R * math.sin(ang), "#58a6ff", 2, 0.9, "5 4")
        c.text(cx + (R + 8) * math.cos(ang), cy + (R + 8) * math.sin(ang),
               f"median seal lag {ms:.0f} bars", c="#58a6ff", size=10, anchor="middle")
    c.text(PADL - 40, c.h - PADB + 30, f"angle = log lag (1 → {lmax:.0f} bars, clockwise from top) · "
           f"radius = |terminal| · colour = sign · larger dot = 12_25", c=MUT, size=10)
    out.append(page("V3.html", "V3 · LAG CLOCK", VIEWS[2][2], c.svg(), m["payload"], m["sha256"],
                    "Radius is absolute size; colour carries the sign. A green dot far out is a "
                    "big win, a red dot far out is a big loss at the same lag."))

    # ---------- V4 KNOT->FAN CINEMA ----------
    m, d = load("v4_braid.json")
    c = Canvas(h=680); frame(c, "V4 · KNOT→FAN CINEMA", VIEWS[3][2],
                             "time (rank-change points, evidence era)", "EMA rank  (0 = highest)")
    assets = list(d.keys())
    lane = (c.h - PADT - PADB - 20) / len(assets)
    EMAN = ["9", "89", "200", "300", "450", "500"]
    ECOL = ["#e6edf3", "#8b949e", "#58a6ff", "#a371f7", "#db6d28", "#f0b72f"]
    for ai, sym in enumerate(assets):
        rows = d[sym]
        yb = PADT + 16 + ai * lane
        c.text(PADL - 68, yb + 12, sym.replace("USDT", ""), c=MUT, size=11)
        n = len(rows)
        if not n:
            continue
        for j, r in enumerate(rows):
            x = PADL + (c.w - PADL - PADR) * j / max(n - 1, 1)
            if r["knot_flag"]:
                c.rect(x, yb, max((c.w - PADL - PADR) / n, 1.1), lane - 12, TOLLC, 0.30)
            elif r["fan_flag"]:
                f = r["fwd_h100"]
                c.rect(x, yb, max((c.w - PADL - PADR) / n, 1.1), lane - 12,
                       lerp_col(0 if f is None else max(-1, min(1, f / 1.5))), 0.26)
        step = max(1, n // 900)
        for k in range(6):
            pts = []
            for j in range(0, n, step):
                x = PADL + (c.w - PADL - PADR) * j / max(n - 1, 1)
                y = yb + 4 + (lane - 20) * rows[j]["ranks"][k] / 5
                pts.append(f"{x:.1f},{y:.1f}")
            c.path("M" + " L".join(pts), "none", ECOL[k], 1.0, 0.75)
    for k in range(6):
        c.circ(PADL + 150 + k * 78, PADT - 12, 4, ECOL[k], 1)
        c.text(PADL + 160 + k * 78, PADT - 8, "e" + EMAN[k], c=MUT, size=10)
    c.text(PADL - 68, c.h - PADB + 30, "gold column = KNOT (the five long EMAs inside 0.5×ATR) · "
           "tinted column = FAN (all six monotone), tint = forward H100", c=MUT, size=10)
    out.append(page("V4.html", "V4 · KNOT→FAN CINEMA", VIEWS[3][2], c.svg(), m["payload"], m["sha256"],
                    "Lines are ranks, not prices: a crossing is an order change. Knots are where "
                    "the stack collapses; fans are where it commits."))

    # ---------- V5 REFUSAL WEATHER ----------
    m, d = load("v5_weather.json")
    c = Canvas(); frame(c, "V5 · REFUSAL WEATHER", VIEWS[4][2],
                        "member bars before the episode  (−10 → 0)",
                        "episodes, grouped: reclaim above / accept below")
    x0, y0 = PADL, PADT + 10
    gw = (c.w - PADL - PADR) / 11
    for kind, ybase, lab in (("reclaim", y0, "RECLAIM (the breakout that failed to be born)"),
                             ("accept", y0 + 250, "ACCEPT (the breakout that held)")):
        sub = [e for e in d if e["kind"] == kind]
        c.text(PADL, ybase - 8, f"{lab}   n={len(sub):,}", c=MUT, size=11)
        if not sub:
            continue
        prof = []
        for k in range(11):
            vals = [e["cells"][k] for e in sub if len(e["cells"]) == 11]
            prof.append(float(np.mean(vals)) if vals else 0.0)
        mx = max(max(prof), 1e-9)
        for k in range(11):
            h = 150 * prof[k] / mx
            c.rect(x0 + k * gw + 6, ybase + 160 - h, gw - 12, h,
                   "#58a6ff" if kind == "reclaim" else TOLLC, 0.72)
            c.text(x0 + k * gw + gw / 2, ybase + 176, f"{k-10}", c=MUT, size=10, anchor="middle")
            c.text(x0 + k * gw + gw / 2, ybase + 160 - h - 5, f"{prof[k]:.2f}",
                   c=MUT, size=9, anchor="middle")
    c.text(PADL, c.h - PADB + 30, "bar height = MEAN i-b (price↔level) refusal count in that bar. "
           "Higher bars = more 'almost' before the moment.", c=MUT, size=10)
    out.append(page("V5.html", "V5 · REFUSAL WEATHER", VIEWS[4][2], c.svg(), m["payload"], m["sha256"],
                    "Two profiles, same axis. The question is whether the air before a reclaim is "
                    "thicker than the air before an acceptance."))

    # ---------- V6 TAIL GARDEN ----------
    m, d = load("v6_campaigns.json")
    c = Canvas(); frame(c, "V6 · TAIL GARDEN", VIEWS[5][2],
                        "campaigns, sorted by MFE (descending)", "R")
    x0, x1, y0, y1 = PADL, c.w - PADR, PADT, c.h - PADB
    ds = sorted(d, key=lambda r: -(r["mfe_r"] if r["mfe_r"] is not None else -9e9))
    ymin, ymax = -4.0, min(30.0, clampq([r["mfe_r"] for r in ds], 1, 99.6)[1])
    axes(c, x0, x1, y0, y1, 0, len(ds), ymin, ymax, xfmt="{:.0f}")
    def sy(v): return y1 - (y1 - y0) * (max(min(v, ymax), ymin) - ymin) / (ymax - ymin)
    c.rect(x0, sy(TOLL_HI), x1 - x0, abs(sy(TOLL_HI) - sy(-TOLL_HI)), TOLLC, 0.16)
    c.line(x0, sy(0), x1, sy(0), MUT, 1.4, 0.9, dash="4 3")
    n = len(ds); step = max(1, n // 1400)
    for i in range(0, n, step):
        r = ds[i]
        x = x0 + (x1 - x0) * i / max(n - 1, 1)
        mfe = r["mfe_r"] or 0; term = r["terminal_r"] or 0
        c.line(x, sy(0), x, sy(mfe), "#30363d", 1, 0.75)
        if mfe > term:
            c.line(x, sy(term), x, sy(mfe), NEG, 1, 0.30)     # give-back wilt
        c.circ(x, sy(term), 1.9, lerp_col(max(-1, min(1, term / 3.0))),
               0.95 if r["is_winner"] else 0.55)
    c.text(x1 - 340, y0 + 16, "stem = MFE reached · dot = terminal R · red stem = given back",
           c=MUT, size=10)
    out.append(page("V6.html", "V6 · TAIL GARDEN", VIEWS[5][2], c.svg(), m["payload"], m["sha256"],
                    "The gap between stem-top and dot IS the give-back. mae_r and n_reclaims are "
                    "absent from the source parquet, so the spec's reclaim ticks are omitted."))

    # ---------- V7 CLOCK DUEL ----------
    m, d = load("v7_anchors.json")
    c = Canvas(h=660); frame(c, "V7 · CLOCK DUEL", VIEWS[6][2],
                             "terminal H100 (ATR)", "anchor family")
    x0, x1 = PADL + 200, c.w - PADR
    rows = sorted(d, key=lambda r: -(r["median"] or -9))
    lane = (c.h - PADT - PADB - 30) / max(len(rows), 1)
    allv = [v for r in rows for v in (r["distribution_deciles"] or [])]
    xmin, xmax = (min(allv), max(allv)) if allv else (-1, 1)
    xmin, xmax = min(xmin, -0.6), max(xmax, 0.6)
    def sx(v): return x0 + (x1 - x0) * (max(min(v, xmax), xmin) - xmin) / (xmax - xmin)
    for sgn in (1, -1):
        c.rect(min(sx(sgn * TOLL_LO), sx(sgn * TOLL_HI)), PADT,
               abs(sx(TOLL_HI) - sx(TOLL_LO)), c.h - PADT - PADB, TOLLC, 0.16)
    c.line(sx(0), PADT, sx(0), c.h - PADB, MUT, 1.4, 0.9, dash="4 3")
    for k in range(7):                                   # readable outcome axis
        v = xmin + (xmax - xmin) * k / 6
        c.line(sx(v), c.h - PADB, sx(v), c.h - PADB + 5, GRID, 1, 1)
        c.text(sx(v), c.h - PADB + 18, f"{v:.2f}", c=MUT, size=10, anchor="middle")
    c.line(x0, c.h - PADB, x1, c.h - PADB, GRID, 1, 1)
    for i, r in enumerate(rows):
        y = PADT + 24 + i * lane
        ref = "EMA-anchored" in r["name"]
        c.text(x0 - 12, y + 5, f"{r['name'][:26]}", c=(TOLLC if ref else FG),
               size=11, anchor="end")
        c.text(x0 - 12, y + 18, f"n={r['n']:,}", c=MUT, size=9, anchor="end")
        dec = r["distribution_deciles"] or []
        if len(dec) >= 9:
            c.line(sx(dec[0]), y, sx(dec[-1]), y, MUT, 1.2, 0.55)
            c.rect(sx(dec[2]), y - 7, sx(dec[6]) - sx(dec[2]), 14,
                   "#58a6ff" if ref else "#30363d", 0.55)
        if r["median"] is not None:
            c.circ(sx(r["median"]), y, 4.6, lerp_col(max(-1, min(1, r["median"] / 0.3))), 1)
    c.text(PADL, c.h - PADB + 32, "bar = p30–p70 · whisker = p10–p90 · dot = median · "
           "gold = the toll band. An anchor whose whole box sits inside gold pays for nothing.",
           c=MUT, size=10)
    out.append(page("V7.html", "V7 · CLOCK DUEL", VIEWS[6][2], c.svg(), m["payload"], m["sha256"],
                    "The EMA clock is the highlighted row. Read how much of its median sits "
                    "outside the toll band — and which anchor sits further out."))

    # ---------- V8 WALL SONAR ----------
    m, d = load("v8_sonar.json")
    c = Canvas(); frame(c, "V8 · WALL SONAR", VIEWS[7][2],
                        "distance from price to registry level (ATR)", "count")
    x0, x1, y0, y1 = PADL, c.w - PADR - 330, PADT, c.h - PADB
    dists = [l["dist_atr"] for a in d["armings"] for l in a["levels"]]
    bins = np.linspace(0, 6, 49)
    hist, _ = np.histogram(dists, bins=bins)
    hmax = max(hist.max(), 1)
    axes(c, x0, x1, y0, y1, 0, 6, 0, float(hmax), xticks=6, yticks=5)
    c.rect(x0, y0, (x1 - x0) * (0.15 / 6), y1 - y0, TOLLC, 0.20)
    c.text(x0 + (x1 - x0) * (0.15 / 6) + 6, y0 + 14,
           "← the pinned 0.15×ATR co-location band", c=TOLLC, size=10)
    bw = (x1 - x0) / (len(bins) - 1)
    for i, h in enumerate(hist):
        hh = (y1 - y0) * h / hmax
        c.rect(x0 + i * bw, y1 - hh, bw - 1, hh, "#58a6ff", 0.75)
    hx = c.w - PADR - 300
    c.text(hx, y0 + 4, "How many levels sit inside the band at once?", c=FG, size=12)
    tot = sum(r["count"] for r in d["colocation_histogram"])
    for i, r in enumerate(d["colocation_histogram"][:6]):
        y = y0 + 34 + i * 30
        frac = r["count"] / tot
        c.rect(hx, y, 250 * frac, 20, TOLLC if r["n_levels_in_band"] >= 2 else "#30363d", 0.8)
        c.text(hx + 256, y + 15, f"{r['n_levels_in_band']} → {frac:.1%}", c=MUT, size=11)
    c.text(hx, y0 + 34 + 6 * 30 + 12, "Confluence would be the bars at 2+.", c=MUT, size=10)
    out.append(page("V8.html", "V8 · WALL SONAR", VIEWS[7][2], c.svg(), m["payload"], m["sha256"],
                    "Left: how far the nearest registry walls actually are. Right: how often two "
                    "or more are close enough to be called confluence."))

    # ---------- V9 VERDICT TIDES ----------
    m, d = load("v9_tides.json")
    c = Canvas(h=680); frame(c, "V9 · VERDICT TIDES", VIEWS[8][2],
                             "episodes in time order (evidence era)",
                             "depth beyond the boundary (ATR)")
    mems = ["1h", "4h", "12h"]
    lane = (c.h - PADT - PADB - 20) / 3
    for mi, mem in enumerate(mems):
        eps = d[mem]["episodes"]; runs = d[mem]["hysteresis_runs"]
        yb = PADT + 20 + mi * lane
        mid = yb + lane / 2 - 14
        n = len(eps)
        acc = sum(1 for e in eps if e["verdict"] == "ACCEPTED")
        rl = [r["length"] for r in runs]
        c.text(PADL - 68, mid, mem, c=FG, size=13)
        c.text(PADL, yb + 6, f"n={n:,} · accepted {acc/max(n,1):.0%} · "
               f"mean run {np.mean(rl):.2f} episodes (1.0 = memoryless)", c=MUT, size=10)
        c.line(PADL, mid, c.w - PADR, mid, GRID, 1, 0.9)
        step = max(1, n // 1100)
        for j in range(0, n, step):
            e = eps[j]
            x = PADL + (c.w - PADL - PADR) * j / max(n - 1, 1)
            dep = min(e["depth_atr"] or 0, 2.0)
            h = (lane / 2 - 22) * (dep / 2.0)
            up = e["verdict"] == "ACCEPTED"
            col = TOLLC if e.get("trap_48h") else (POS if up else "#58a6ff")
            c.line(x, mid, x, mid - h if up else mid + h, col, 1.1, 0.7)
    c.text(PADL - 68, c.h - PADB + 32, "up = ACCEPTED · down = deviation-reclaim · "
           "gold = trapped within 48h · height = depth beyond the boundary", c=MUT, size=10)
    out.append(page("V9.html", "V9 · VERDICT TIDES", VIEWS[8][2], c.svg(), m["payload"], m["sha256"],
                    "Mean run length is the hysteresis: 1.0 would be a coin. Gold spikes are "
                    "acceptances that did not hold."))

    # ---------- INDEX ----------
    cards = []
    for (code, name, q), fn in zip(VIEWS, out):
        mm, _ = load(f"{code.lower()}_{['armings','flows','lags','braid','weather','campaigns','anchors','sonar','tides'][int(code[1])-1]}.json")
        cards.append(f"""<a class="card" href="{fn}"><div class="c">{code}</div>
<div class="t">{esc(name)}</div><div class="q">{esc(q)}</div>
<div class="m">{mm['rows']:,} rows · sha {mm['sha256'][:12]}…</div></a>""")
    idx = f"""<!doctype html><meta charset="utf-8"><title>CENSUS-2A · the nine views</title>
<style>body{{background:{BG};color:{FG};font-family:ui-monospace,Menlo,Consolas,monospace;
margin:0;padding:30px}}.w{{max-width:1240px;margin:0 auto}}h1{{font-size:23px;margin:0 0 6px}}
.s{{color:{MUT};font-size:12.5px;margin:0 0 6px;line-height:1.7}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:14px;margin-top:22px}}
.card{{display:block;background:#151b23;border:1px solid {GRID};border-radius:9px;padding:15px;
text-decoration:none;color:{FG}}}.card:hover{{border-color:{TOLLC}}}
.c{{color:{TOLLC};font-size:11px;letter-spacing:.13em}}.t{{font-size:15px;margin:5px 0 8px}}
.q{{color:{MUT};font-size:12px;line-height:1.55;min-height:52px}}
.m{{color:#5a6472;font-size:10px;margin-top:9px}}
.f{{color:{MUT};font-size:10.5px;line-height:1.65;border-top:1px solid {GRID};
margin-top:26px;padding-top:14px}}</style>
<div class="w"><h1>CENSUS-2A · ENTRIES &amp; EXITS, SEEN</h1>
<p class="s"><b>DISPLAY-ONLY · Tier-E exploration.</b> Nine views over a spent measurement
contract. Nothing here is evidence; the census's own yield was one provisional result out of
nine scored hypotheses, and these pictures exist to sharpen two sentences — "the system enters
when ___" and "the system exits when ___" — not to settle them.</p>
<p class="s">Every outcome axis shades the <span style="color:{TOLLC}">toll band ±0.026–0.059 ATR</span>.
Profit smaller than cost is drawn as what it is. Colour = outcome, diverging at zero;
shape and size = structure. Evidence era ≤ 2024-07-01.</p>
<p class="s"><b>These are HEPHAESTUS first-pass renders</b> — hand-rolled SVG, self-contained,
no external fetches. Design's versions sit beside them and never replace them.</p>
<div class="g">{''.join(cards)}</div>
<p class="f">DISPLAY-ONLY · Tier-E exploration · CENSUS-2A · evidence era ≤ 2024-07-01 · no claim
is made or implied; promotion requires registration (see CENSUS2A_CLOSEOUT_2026-08-12.md §5).
Rendered by HEPHAESTUS first-pass, {GEN}.</p></div>"""
    (VIZ / "viz_index.html").write_text(idx, encoding="utf-8")
    out.append("viz_index.html")
    return out


def handoff():
    HAND.mkdir(parents=True, exist_ok=True)
    n = 0
    for p in sorted(PAY.glob("*.json")):
        shutil.copy2(p, HAND / p.name); n += 1
    for f in ["DESIGN_BRIEF_CENSUS2A_VIZ_2026-08-12.md", "CENSUS2A_CLOSEOUT_2026-08-12.md"]:
        s = ROOT / "exchange" / "reports" / f
        if s.exists():
            shutil.copy2(s, HAND / f); n += 1
    return n


if __name__ == "__main__":
    import sys
    render_only = "--render-only" in sys.argv
    if render_only:
        inv = sorted(p.name for p in PAY.glob("*.json"))
        gaps = [V6_GAP]
    else:
        inv, gaps = extract()
    print("\n  VIZ-1 renders (hand-rolled SVG, self-contained):")
    files = render_all()
    for f in files:
        sz = (VIZ / f).stat().st_size
        print("    %-18s %9s B" % (f, format(sz, ",")))
    n = handoff()
    print("\n  DESIGN_HANDOFF: %d files -> %s" % (n, HAND))
    print("  viz_index.html  -> %s" % (VIZ / "viz_index.html"))
    print("\n  payloads=%d  renders=%d  gaps=%d" % (len(inv), len(files), len(gaps)))
    for g in gaps:
        print("   GAP:", g)
