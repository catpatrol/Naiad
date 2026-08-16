"""VIZ-4 · THE EMA MANTLE — payload builder.  Tier-E, DISPLAY-ONLY, m = 0.

Executes `exchange/reports/DESIGN_CONTRACT_VIZ4_EMA_MANTLE_2026-08-15.md` §3.

    v4_mantle_BTC_1h.json · v4_mantle_BTC_5m.json
    v4_echo_BTC_1h.json   · v4_echo_BTC_5m.json

THE METAPHOR IS THE SPEC (contract §1).  Eighteen EMAs are one fabric: the rod
(5000) barely sways, the hem (12) is whipped by every gust, sixteen threads of
increasing inertia between them.  Displacement is (EMA - price)/ATR -- note the
ORDER, ema minus price, so a thread ABOVE price reads positive.

NOTHING HERE IS A CLAIM.  Every number is a displacement, a velocity, a
correlation or a mark.  Echoes are SHOWN, NOT SCORED.  Selection surface m = 0:
the payloads are complete decimations of fixed series, nothing is ranked, and
no window was chosen on what it contained.

────────────────────────────────────────────────────────────────────────────
WHAT IS REUSED, AND WHAT IS THEREFORE NOT RESTATED HERE
────────────────────────────────────────────────────────────────────────────
* `write_payload` / `jclean` / `src_meta` are IMPORTED from
  `scripts/census2a_viz.py` -- the same posture VIZ-2 took
  (`census2b_viz2.py:16-17`).  The meta block, the sha-of-its-own-data-block
  rule and the NaN->null rule all live in one place.
* The six ribbons and their EMA lengths are IMPORTED from
  `census2b_program.RIBBONS`; the flag codes (`KN_TRUE`, `OR_BULL`, ...) too.
* The per-SR smoothing k is READ from the ORACLE manifest's own pins
  (`research_outputs/census2b/oracle/oracle_manifest.json` -> `pins.state_k`,
  law `k = max(20, round(median_len/8))`).  It is NOT retyped here: R-3 pinned
  it on 2026-08-15 and a copy would be a second source of truth.
* The toll band is READ per (asset, lens) from that cell's own transitions
  tables, where `toll_atr` is already stored.  `census2a_viz` carries VIZ-1's
  single global toll as a module constant; this contract's payloads span two
  lenses whose tolls differ four-fold (1h 0.1355 vs 5m 0.5537), so the emitter
  is re-pointed PER PAYLOAD -- an extension of the same re-point pattern
  VIZ-2 used for `PAY`, `SEED` and `ART`, and it is stated in the build doc.

USAGE
    ~/venvs/naiad/bin/python scripts/census2b_viz4.py            # build + fixtures
    ~/venvs/naiad/bin/python scripts/census2b_viz4.py --fixtures-only
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import census2a_viz as V                                          # noqa: E402
import census2b_program as C2B                                    # noqa: E402

SEED = 20260815
C2A = ROOT / "research_outputs" / "census2a"
C2B_DIR = ROOT / "research_outputs" / "census2b"
PAY = C2B_DIR / "viz_payloads"
HAND = C2B_DIR / "DESIGN_HANDOFF_VIZ4"
REPORTS = ROOT / "exchange" / "reports"

CONTRACT_V4 = "DESIGN_CONTRACT_VIZ4_EMA_MANTLE_2026-08-15.md"
CONTRACT_V3 = "DESIGN_CONTRACT_VIZ3_TRADE_CATHEDRAL_2026-08-15.md"

# ── contract §3: the default payload set ──────────────────────────────────
CELLS = [("BTCUSDT", "BTC", "1h"), ("BTCUSDT", "BTC", "5m")]
MAX_STEPS = 8_000                # contract §3
ECHO_LAGS = list(range(0, 49))   # contract §3: lags {0…48}
ECHO_WINDOW = 96                 # contract §3: window 96 bars
HEM_LENS = (12, 26)              # contract §2: hem-edge = mean of 12/26
ROD_LO = 2618                    # contract §2: rod-edge = mean of 2618…5000

_INV: list[dict] = []


def hr(ch="-", n=100):
    print(ch * n)


def banner(t):
    print()
    hr("=")
    print(t)
    hr("=")


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ═══════════════════════════════════════════════ the pinned, imported facts
def thread_table() -> list[dict]:
    """The eighteen threads, hem to rod, each carrying its SR and that SR's k.

    Contract §2 labels the y-axis "12 at the hem"; the fabric is eighteen EMAs
    (§1) and `RIBBONS` FAST is (9, 12, 26), so the axis actually spans 9 → 5000
    and the hem EDGE used by the echo is 12/26 exactly as §2 defines it.  Both
    facts are emitted so a renderer never has to guess which it got.
    """
    k = state_k()
    out = []
    for fam, lens in C2B.RIBBONS.items():
        for L in lens:
            out.append({"len": int(L), "sr": fam, "k": int(k[fam])})
    out.sort(key=lambda r: r["len"])
    if len(out) != 18:
        raise SystemExit(f"HALT: expected 18 threads, got {len(out)}")
    return out


def state_k() -> dict:
    """Per-SR smoothing k, READ from the ORACLE manifest's pins (R-3, 2026-08-15)."""
    m = json.loads((C2B_DIR / "oracle" / "oracle_manifest.json").read_text())
    k = m["pins"]["state_k"]
    law = m["pins"]["state_k_law"]
    missing = [f for f in C2B.FAMILIES if f not in k]
    if missing:
        raise SystemExit(f"HALT: oracle_manifest pins.state_k missing {missing}")
    print(f"    per-SR k (ORACLE pins, law `{law}`): {k}")
    return k


def toll_band(asset: str, lens: str) -> tuple[float, float]:
    """(toll_lo, toll_hi) for this cell, READ from its own transitions tables.

    `toll_atr` is constant within a cell and differs between knots and fans
    (they anchor on different bars), so the pair is the band, not a spread.
    """
    vals = []
    for kind in ("knots", "fans"):
        p = C2B_DIR / "transitions" / asset / f"{lens}_{kind}.parquet"
        d = pd.read_parquet(p, columns=["toll_atr"])
        if len(d):
            vals += [float(d["toll_atr"].min()), float(d["toll_atr"].max())]
    if not vals:
        raise SystemExit(f"HALT: no toll_atr for {asset} {lens}")
    return round(min(vals), 6), round(max(vals), 6)


# ═══════════════════════════════════════════════════════ the deterministic grid
def decimate(n: int, max_steps: int = MAX_STEPS) -> tuple[np.ndarray, int, str]:
    """Fixed-stride decimation ANCHORED AT THE LAST BAR.

    Anchored at the end rather than the start so the newest bar is always
    present: a mantle whose right edge is a stale bar is a mantle that lies
    about now.  Deterministic and restated in meta.
    """
    stride = max(1, int(np.ceil(n / max_steps)))
    idx = np.arange(n - 1, -1, -stride)[::-1]
    rule = (f"fixed stride {stride}, anchored at the LAST bar: "
            f"indices arange(n-1, -1, -{stride})[::-1] over n={n} source bars "
            f"-> {len(idx)} steps (cap {max_steps})")
    return idx, stride, rule


# ═════════════════════════════════════════════════════════════ the mantle
def build_mantle(asset: str, short: str, lens: str) -> dict:
    print(f"\n  ── v4_mantle_{short}_{lens}")
    em = pd.read_parquet(C2B_DIR / "emas" / asset / f"{lens}.parquet")
    rb = pd.read_parquet(C2B_DIR / "ribbons" / asset / f"{lens}.parquet")
    V.assert_key(em[["open_time"]], ["open_time"], f"emas[{asset}/{lens}]")
    V.assert_key(rb[["open_time"]], ["open_time"], f"ribbons[{asset}/{lens}]")
    if not em["open_time"].equals(rb["open_time"]):
        raise SystemExit(f"HALT (F-KEY): emas/ribbons ts grids differ for {asset} {lens}")

    ot = em["open_time"].to_numpy(np.int64)
    price = em["close"].to_numpy(float)
    atr = em["atr"].to_numpy(float)
    n = len(ot)
    threads = thread_table()

    # displacement = (ema - price)/ATR.  ATR <= 0 is not a zero displacement,
    # it is an undefined one -- NaN, which becomes absent cloth.
    with np.errstate(invalid="ignore", divide="ignore"):
        safe_atr = np.where(np.isfinite(atr) & (atr > 0), atr, np.nan)
    disp, vel = [], []
    for t in threads:
        e = em[f"e{t['len']}"].to_numpy(float)
        d = (e - price) / safe_atr
        # velocity: Delta displacement PER BAR over this SR's k-bar window --
        # census2b's own `_delta_k` shape (x[t] - x[t-k], program.py:686-693),
        # divided by k to make it a per-bar rate as the contract asks.
        k = t["k"]
        v = np.full(n, np.nan)
        if n > k:
            v[k:] = (d[k:] - d[:-k]) / float(k)
        disp.append(d)
        vel.append(v)
    disp = np.vstack(disp)
    vel = np.vstack(vel)

    idx, stride, rule = decimate(n)
    warm = int(np.isfinite(disp[-1]).argmax()) if np.isfinite(disp[-1]).any() else -1
    print(f"    {n:,} source bars -> {len(idx):,} steps (stride {stride})")
    print(f"    rod thread e{threads[-1]['len']} first warm at source bar {warm:,} "
          f"({'absent cloth before it' if warm > 0 else 'warm from bar 0'})")

    # knot / orient per SR, on the same decimated grid
    knot, orient = {}, {}
    for fam in C2B.FAMILIES:
        kv = rb[f"{fam}_knot"].to_numpy()[idx]
        ov = rb[f"{fam}_orient"].to_numpy()[idx]
        knot[fam] = [None if int(x) == C2B.KN_NA else int(x) for x in kv]
        orient[fam] = [None if int(x) == C2B.OR_NA else int(x) for x in ov]

    marks = transition_marks(asset, lens)
    data = {
        "asset": asset, "lens": lens,
        "threads": [t["len"] for t in threads],
        "thread_sr": [t["sr"] for t in threads],
        "thread_k": [t["k"] for t in threads],
        "hem_lens": list(HEM_LENS), "rod_lens": [t["len"] for t in threads
                                                 if t["len"] >= ROD_LO],
        "ts": [int(x) for x in ot[idx]],
        "disp": [[_r3(x) for x in row[idx]] for row in disp],
        "vel": [[_r5(x) for x in row[idx]] for row in vel],
        "knot": knot, "orient": orient,
        "knot_codes": {"no": C2B.KN_FALSE, "knot": C2B.KN_TRUE, "absent": None},
        "orient_codes": {"bear-fanned": C2B.OR_BEAR, "mixed": C2B.OR_MIXED,
                         "bull-fanned": C2B.OR_BULL, "absent": None},
        "marks": marks_columnar(marks),
    }
    return _emit(f"v4_mantle_{short}_{lens}.json", data, asset, lens, rule,
                 note="MANTLE. COLUMNAR: `disp` and `vel` are thread-major -- "
                      "disp[i][j] is thread `threads[i]` at time `ts[j]`, "
                      "displacement (EMA-price)/ATR, so a thread ABOVE price is "
                      "POSITIVE. null = NOT WOVEN (EMA not warm, or ATR "
                      "undefined): render as ABSENT CLOTH, never as zero. "
                      "`vel` is Delta-displacement PER BAR over that thread's "
                      "SR k (thread_k), i.e. (d[t]-d[t-k])/k. `knot`/`orient` "
                      "are per-SR on the same grid; null there means not "
                      "computed, which is not the same as 'no knot'. `marks` "
                      "are knot->fan transitions and are marks, not claims.")


def _r3(x):
    return None if not np.isfinite(x) else round(float(x), 3)


def _r5(x):
    return None if not np.isfinite(x) else round(float(x), 5)


def _r2(x):
    return None if not np.isfinite(x) else round(float(x), 2)


# ═══════════════════════════════════════════════════════════ the echo trace
def build_echo(asset: str, short: str, lens: str) -> dict:
    print(f"\n  ── v4_echo_{short}_{lens}")
    em = pd.read_parquet(C2B_DIR / "emas" / asset / f"{lens}.parquet")
    ot = em["open_time"].to_numpy(np.int64)
    price = em["close"].to_numpy(float)
    atr = em["atr"].to_numpy(float)
    n = len(ot)
    threads = thread_table()
    with np.errstate(invalid="ignore", divide="ignore"):
        safe_atr = np.where(np.isfinite(atr) & (atr > 0), atr, np.nan)

    def edge_velocity(lens_list) -> pd.Series:
        vs = []
        for t in threads:
            if t["len"] not in lens_list:
                continue
            d = (em[f"e{t['len']}"].to_numpy(float) - price) / safe_atr
            k = t["k"]
            v = np.full(n, np.nan)
            if n > k:
                v[k:] = (d[k:] - d[:-k]) / float(k)
            vs.append(v)
        return pd.Series(np.nanmean(np.vstack(vs), axis=0))

    rod_lens = [t["len"] for t in threads if t["len"] >= ROD_LO]
    hem = edge_velocity(HEM_LENS)
    rod = edge_velocity(rod_lens)
    print(f"    hem edge = mean velocity of e{HEM_LENS} · "
          f"rod edge = mean velocity of e{rod_lens}")

    # rolling corr(hem[t], rod[t-L]) over `window` bars, per lag.
    # A LAG ASKS: does the hem's motion arrive at the rod later?  The rod
    # series is shifted FORWARD so lag L pairs hem now with rod L bars ago;
    # the contract's question ("when does the hem's motion arrive at the rod")
    # is read the other way round, so the rod is the LAGGING series.
    corr = []
    for L in ECHO_LAGS:
        c = rod.shift(-L).rolling(ECHO_WINDOW, min_periods=ECHO_WINDOW).corr(hem)
        corr.append(c.to_numpy())
    corr = np.vstack(corr)

    idx, stride, rule = decimate(n)
    nn = int(np.isfinite(corr).sum())
    print(f"    {len(ECHO_LAGS)} lags x {len(idx):,} steps, "
          f"{100.0 * nn / corr.size:.1f}% finite before decimation")

    data = {
        "asset": asset, "lens": lens,
        "lags": ECHO_LAGS, "window": ECHO_WINDOW,
        "hem_lens": list(HEM_LENS), "rod_lens": rod_lens,
        "ts": [int(x) for x in ot[idx]],
        # 2 dp: a correlation lives in [-1, 1], so 0.01 gives 200 distinct
        # levels — more than any colormap or ripple render resolves, and it
        # halves the payload.  Stated here rather than done quietly.
        "corr": [[_r2(x) for x in row[idx]] for row in corr],
        "marks": marks_columnar(transition_marks(asset, lens)),
    }
    return _emit(f"v4_echo_{short}_{lens}.json", data, asset, lens, rule,
                 note="ECHO. corr rounded to 2 dp (200 levels across [-1,1]). "
                      "COLUMNAR: corr[i][j] is lag `lags[i]` at time "
                      f"`ts[j]` -- Pearson corr over a trailing {ECHO_WINDOW}-bar "
                      "window between hem-edge velocity at t and rod-edge "
                      "velocity at t+lag, so a ridge at lag L reads 'the rod "
                      "moved L bars AFTER the hem'. null = window not full or "
                      "an edge not warm. `marks` are the same knot->fan "
                      "transitions carried by the mantle, for the time axis. "
                      "NO CLAIM: an echo is shown, never scored; a visible "
                      "ridge is a picture, and promotion requires registration.")


# ═══════════════════════════════════════════════════ knot -> fan transitions
def transition_marks(asset: str, lens: str) -> list[dict]:
    """The knot->fan transitions, AS ALREADY RECORDED by census-2B Part A.

    `census2b_parta.transitions_for_cell` stores, on every knot episode, the
    bar at which the ribbon first became fully ORDERED after the knot released
    (`sep_bar_index` / `sep_ts_ms`) together with its lag and direction.  That
    IS the knot->fan transition; deriving a second one here would invent a
    definition the estate already owns.  `sep_ts_ms == -1` means the knot never
    resolved into a fan inside the series and is correctly absent from the marks.
    """
    p = C2B_DIR / "transitions" / asset / f"{lens}_knots.parquet"
    d = pd.read_parquet(p)
    fa = pd.read_parquet(C2B_DIR / "transitions" / asset / f"{lens}_fans.parquet")
    d = d[d["sep_ts_ms"] > 0]
    # `at_fan_onset` matters to the renderer and is measured, not assumed: most
    # knots release into a fan that was ALREADY running (F-V4 (d) prints the
    # share).  A mark drawn as "a fan started here" would overstate the data.
    onset = {sr: set(g["onset_bar_index"].astype(int))
             for sr, g in fa.groupby("sr")}
    out = [{"sr": r.sr, "ts_ms": int(r.sep_ts_ms),
            "knot_exit_ts_ms": int(r.exit_ts_ms),
            "lag_bars": int(r.sep_lag_bars), "dir_sign": int(r.exit_dir_sign),
            "at_fan_onset": bool(int(r.sep_bar_index) in onset.get(r.sr, ()))}
           for r in d.itertuples()]
    out.sort(key=lambda m: (m["ts_ms"], m["sr"]))
    return out


def marks_columnar(marks: list[dict]) -> dict:
    """The same marks as parallel arrays — the house columnar shape.

    At 5m there are 37,501 of them and they ride in BOTH payloads of the cell;
    as dicts the repeated key names alone cost ~5 MB across the handoff.  Same
    information, one sixth the bytes, and `n` is stated so a reader never has
    to infer the record count from `meta.rows` (which counts array CELLS).
    """
    return {"n": len(marks),
            "fields": ["sr", "ts_ms", "knot_exit_ts_ms", "lag_bars",
                       "dir_sign", "at_fan_onset"],
            "sr": [m["sr"] for m in marks],
            "ts_ms": [m["ts_ms"] for m in marks],
            "knot_exit_ts_ms": [m["knot_exit_ts_ms"] for m in marks],
            "lag_bars": [m["lag_bars"] for m in marks],
            "dir_sign": [m["dir_sign"] for m in marks],
            "at_fan_onset": [m["at_fan_onset"] for m in marks]}


# ═══════════════════════════════════════════════════════════════ emission
def _emit(name: str, data: dict, asset: str, lens: str, rule: str,
          note: str) -> dict:
    lo, hi = toll_band(asset, lens)
    V.TOLL_LO, V.TOLL_HI = lo, hi        # re-pointed PER PAYLOAD — see docstring
    srcs = [
        _raw("emas/%s/%s" % (asset, lens),
             C2B_DIR / "emas" / asset / f"{lens}.parquet"),
        _raw("ribbons/%s/%s" % (asset, lens),
             C2B_DIR / "ribbons" / asset / f"{lens}.parquet"),
        _raw("transitions/%s/%s_knots" % (asset, lens),
             C2B_DIR / "transitions" / asset / f"{lens}_knots.parquet"),
        _raw("transitions/%s/%s_fans" % (asset, lens),
             C2B_DIR / "transitions" / asset / f"{lens}_fans.parquet"),
        _raw("oracle/oracle_manifest.json",
             C2B_DIR / "oracle" / "oracle_manifest.json"),
    ]
    inv = V.write_payload(name, data, srcs, downsample_rule=rule, note=note)
    inv["toll_lo"], inv["toll_hi"] = lo, hi
    _INV.append(inv)
    return inv


def _raw(label: str, p: Path) -> dict:
    rows = None
    if p.suffix == ".parquet":
        rows = int(len(pd.read_parquet(p, columns=["open_time"]))) \
            if "emas" in label or "ribbons" in label else int(len(pd.read_parquet(p)))
    return {"parquet": label, "sha256": sha_file(p), "rows": rows}


# ═══════════════════════════════════════════════════════ contracts, filed
def file_contracts() -> list[dict]:
    """File the attached contract(s) into exchange/reports/, shas printed."""
    banner("CONTRACTS — filed to exchange/reports/")
    filed = []
    for cname in (CONTRACT_V4, CONTRACT_V3):
        dest = REPORTS / cname
        src = Path.home() / "Downloads" / cname
        if dest.exists():
            print(f"    {cname}")
            print(f"      already filed · sha256 {sha_file(dest)}")
            filed.append({"contract": cname, "state": "already-filed",
                          "sha256": sha_file(dest), "bytes": dest.stat().st_size})
        elif src.exists():
            shutil.copy2(src, dest)
            print(f"    {cname}")
            print(f"      FILED from {src} · sha256 {sha_file(dest)} "
                  f"· {dest.stat().st_size:,} B")
            filed.append({"contract": cname, "state": "filed",
                          "sha256": sha_file(dest), "bytes": dest.stat().st_size,
                          "from": str(src)})
        else:
            print(f"    {cname}")
            print(f"      *** ABSENT — not in exchange/reports/, not in "
                  f"~/Downloads. NOT INVENTED. ***")
            filed.append({"contract": cname, "state": "ABSENT", "sha256": None})
    return filed


# ═══════════════════════════════════════════════════════════════ the ferry
def ferry(filed: list[dict]) -> list[str]:
    """Copy payloads + both contracts into DESIGN_HANDOFF_VIZ4/ (contract §5)."""
    banner("FERRY — DESIGN_HANDOFF_VIZ4/")
    HAND.mkdir(parents=True, exist_ok=True)
    carried = []
    for inv in _INV:
        shutil.copy2(PAY / inv["payload"], HAND / inv["payload"])
        carried.append(inv["payload"])
    for f in filed:
        if f["state"] == "ABSENT":
            print(f"    {f['contract']:56} ABSENT — cannot ferry")
            continue
        shutil.copy2(REPORTS / f["contract"], HAND / f["contract"])
        carried.append(f["contract"])
    for c in carried:
        p = HAND / c
        print(f"    {c:56} {p.stat().st_size:>9,} B")
    return carried


# ═══════════════════════════════════════════════════════════════ F-V4
def f_v4(filed: list[dict]) -> bool:
    banner("F-V4")
    ok = True

    print("  (a) every payload round-trips json.load and its data-block sha holds")
    for inv in _INV:
        p = PAY / inv["payload"]
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            blob = json.dumps(d["data"], sort_keys=True,
                              separators=(",", ":")).encode()
            good = hashlib.sha256(blob).hexdigest() == d["meta"]["sha256"]
        except Exception as e:                                    # noqa: BLE001
            print(f"      {inv['payload']:24s} LOAD FAILED: {e}")
            ok = False
            continue
        sz = p.stat().st_size
        print(f"      {inv['payload']:24s} load OK  sha {'OK' if good else 'DRIFT'}"
              f"  {sz:>10,} B  {'<= 700K cap' if sz <= V.MAX_BYTES else '!! OVER the VIZ-1 700K cap — disclosed'}")
        ok &= good

    print("  (b) shape: 18 threads · <= 8,000 steps · lags 0..48 · window 96")
    for inv in _INV:
        d = json.loads((PAY / inv["payload"]).read_text())["data"]
        T = len(d["ts"])
        if "disp" in d:
            checks = [("threads", len(d["threads"]), 18),
                      ("disp rows", len(d["disp"]), 18),
                      ("vel rows", len(d["vel"]), 18),
                      ("steps <= 8000", T <= MAX_STEPS, True)]
            checks += [(f"disp[{i}] len", len(d["disp"][i]), T) for i in (0, 17)]
        else:
            checks = [("lags", len(d["lags"]), 49),
                      ("window", d["window"], 96),
                      ("corr rows", len(d["corr"]), 49),
                      ("steps <= 8000", T <= MAX_STEPS, True),
                      ("corr[0] len", len(d["corr"][0]), T)]
        for nm, got, want in checks:
            good = got == want
            ok &= good
            print(f"      {'OK ' if good else 'BAD'} {inv['payload']:24s} "
                  f"{nm:16s} {got} == {want}")

    print("  (c) NaN-before-warm is ABSENT (null), never zero")
    for inv in _INV:
        if "mantle" not in inv["payload"]:
            continue
        d = json.loads((PAY / inv["payload"]).read_text())["data"]
        rod = d["disp"][-1]
        nulls = sum(1 for x in rod if x is None)
        zeros = sum(1 for x in rod if x == 0)
        first = next((i for i, x in enumerate(rod) if x is not None), None)
        lead_all_null = first is None or all(x is None for x in rod[:first])
        ok &= lead_all_null
        print(f"      {'OK ' if lead_all_null else 'BAD'} {inv['payload']:24s} "
              f"rod thread e5000: {nulls} null of {len(rod)}, first woven step "
              f"{first}, exact-zero cells {zeros} (nulls lead unbroken: {lead_all_null})")

    print("  (d) transition marks RECONCILE to census2b/transitions")
    for asset, short, lens in CELLS:
        marks = transition_marks(asset, lens)
        kn = pd.read_parquet(C2B_DIR / "transitions" / asset / f"{lens}_knots.parquet")
        fa = pd.read_parquet(C2B_DIR / "transitions" / asset / f"{lens}_fans.parquet")
        # every mark is a knot row with that exact sep stamp
        kset = set(zip(kn["sr"], kn["sep_ts_ms"].astype(np.int64)))
        missing = [m for m in marks if (m["sr"], m["ts_ms"]) not in kset]
        # and every resolving knot produced exactly one mark
        resolving = int((kn["sep_ts_ms"] > 0).sum())
        # and every mark falls INSIDE a fan episode of the same SR.
        #
        # NOT "at a fan onset" -- that was this fixture's first assertion and it
        # FAILED 2,568 of 2,710.  The estate never promised it: `fans` splits an
        # ordered run at every direction change, and a ribbon can be KNOTTED
        # while `orient` is already bull/bear, so a knot commonly releases into
        # a fan that was already running.  Measured below and reported as an
        # inventory fact, because a renderer that draws every mark as "a fan
        # started here" would be drawing a claim the data does not make.
        res = kn[kn["sep_ts_ms"] > 0]
        inside = at_onset = outside = 0
        for sr, g in res.groupby("sr"):
            f = fa[fa["sr"] == sr]
            lo = f["onset_bar_index"].to_numpy()
            hi = f["end_bar_index"].to_numpy()
            for s in g["sep_bar_index"].to_numpy():
                j = int(np.searchsorted(lo, s, "right")) - 1
                if j >= 0 and s < hi[j]:
                    inside += 1
                    at_onset += int(s == lo[j])
                else:
                    outside += 1
        good = (not missing) and len(marks) == resolving and outside == 0
        ok &= good
        print(f"      {'OK ' if good else 'BAD'} {asset} {lens}: {len(marks):,} marks "
              f"= {resolving:,} resolving knots · not-in-knots {len(missing)} "
              f"· inside a same-SR fan episode {inside:,} · outside {outside}")
        print(f"          of those, {at_onset:,} ({100.0 * at_onset / max(inside, 1):.1f}%) "
              f"begin a NEW fan; the rest release into a fan already running "
              f"— stated, not asserted")
        for pay in (f"v4_mantle_{short}_{lens}.json", f"v4_echo_{short}_{lens}.json"):
            pm = json.loads((PAY / pay).read_text())["data"]["marks"]
            same = pm == json.loads(json.dumps(marks_columnar(marks)))
            ok &= same
            print(f"      {'OK ' if same else 'BAD'} {pay:24s} carries the same "
                  f"{pm['n']:,} marks")

    print("  (e) the ferry carries every payload and every filed contract")
    want = [i["payload"] for i in _INV] + [f["contract"] for f in filed
                                           if f["state"] != "ABSENT"]
    have = sorted(p.name for p in HAND.iterdir()) if HAND.exists() else []
    miss = [w for w in want if w not in have]
    ok &= not miss
    print(f"      {'OK ' if not miss else 'BAD'} DESIGN_HANDOFF_VIZ4/ holds "
          f"{len(have)} file(s); missing {miss}")
    absent = [f["contract"] for f in filed if f["state"] == "ABSENT"]
    if absent:
        print(f"      NOTE  absent and therefore NOT ferried: {absent}")

    print("  (f) per-SR k and toll came from the estate, not from this file")
    k = state_k()
    for inv in _INV:
        m = json.loads((PAY / inv["payload"]).read_text())["meta"]
        print(f"      {inv['payload']:24s} toll_lo={m['toll_lo']} "
              f"toll_hi={m['toll_hi']} seed={m['seed']} class={m['class']!r}")
    return ok


# ═══════════════════════════════════════════════════════════════════ main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures-only", action="store_true")
    a = ap.parse_args()

    banner("VIZ-4 · THE EMA MANTLE — payloads (Tier-E · DISPLAY-ONLY · m = 0)")
    PAY.mkdir(parents=True, exist_ok=True)
    V.PAY = PAY
    V.SEED = SEED
    _ART = dict(json.loads((C2B_DIR / "census2b_manifest.json").read_text())
                .get("artifacts", {}))
    V.ART = _ART

    filed = file_contracts()

    if not a.fixtures_only:
        banner("PAYLOADS")
        for asset, short, lens in CELLS:
            build_mantle(asset, short, lens)
            build_echo(asset, short, lens)
        ferry(filed)

    ok = f_v4(filed)

    banner("SUMMARY")
    for inv in _INV:
        print(f"    {inv['payload']:24s} rows={inv['rows']:>9,}  "
              f"{inv['bytes']:>10,} B  sha {inv['sha256'][:16]}")
    man = {"stage": "VIZ-4", "seed": SEED, "class": "DISPLAY-ONLY / Tier-E",
           "m": 0, "contracts": filed, "payloads": _INV,
           "handoff": str(HAND.relative_to(ROOT))}
    (PAY / "viz4_manifest.json").write_text(json.dumps(man, indent=2, sort_keys=True))
    print(f"\n    manifest -> {PAY / 'viz4_manifest.json'}")
    print(f"\n  F-V4: {'PASS' if ok else 'FAIL'}")
    if not ok:
        print("\n*** HALT: F-V4 mismatch. Nothing downstream is trustworthy. ***")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
