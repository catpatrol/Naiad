"""F-AN-1..14 -- the Phase I fixture suite for `analytics/`.

Run: C:\\venvs\\naiad\\Scripts\\python.exe -m pytest tests/test_analytics.py -q

F-AN-13 is the one that matters most. It is a truncation-prefix test over every
series-returning public function, and it exists because the ENGINE lane reported
a one-sided-window hazard in daily_brief.py: code safe today only because the
caller always passes data ending at "now", which extraction converts into an
unguarded bug. Neither lane located the instance. Rather than hunt one, this
finds the whole class.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import analytics                                                    # noqa: E402
from analytics import momentum as M                                 # noqa: E402
from analytics import profile as P                                  # noqa: E402
from analytics import stats as ST                                   # noqa: E402
from analytics import structure as S                                # noqa: E402
from analytics import volatility as V                               # noqa: E402
from analytics import vwap as W                                     # noqa: E402
from analytics import levels as L                                   # noqa: E402

PKG = ROOT / "analytics"


# --------------------------------------------------------------- helpers

def _series(n=400, seed=7):
    rng = np.random.default_rng(seed)
    close = 60000 + np.cumsum(rng.normal(0, 120, n))
    high = close + np.abs(rng.normal(0, 60, n))
    low = close - np.abs(rng.normal(0, 60, n))
    open_ = close + rng.normal(0, 30, n)
    vol = np.abs(rng.normal(1000, 200, n))
    t = np.arange(n, dtype="int64") * 3_600_000 + 1_600_000_000_000
    return t, open_, high, low, close, vol


def same(a, b):
    """Exact equality, with NaN treated as equal to NaN."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if a.shape != b.shape:
        return False
    both_nan = np.isnan(a) & np.isnan(b)
    return bool(np.all(both_nan | (a == b)))


# --------------------------------------------------------------- F-AN-1

def test_f_an_1_golden_values():
    """Hand-checkable arrays with independently derived expectations, 1e-9."""
    x = np.array([1., 2., 3., 4., 5., 6.])
    assert np.isnan(M.sma(x, 3)[:2]).all()
    assert abs(M.sma(x, 3)[2] - 2.0) < 1e-9
    assert abs(M.sma(x, 3)[5] - 5.0) < 1e-9

    # EMA seeded with SMA(3)=2 at index 2, alpha=0.5
    e = M.ema(x, 3)
    assert abs(e[2] - 2.0) < 1e-9
    assert abs(e[3] - (2.0 + 0.5 * (4.0 - 2.0))) < 1e-9

    # RMA seeded with mean(first 3)=2, alpha=1/3
    r = M.rma(x, 3)
    assert abs(r[2] - 2.0) < 1e-9
    assert abs(r[3] - (2.0 + (4.0 - 2.0) / 3.0)) < 1e-9

    # a monotonically rising close has no losses -> RSI pinned at 100
    assert abs(M.rsi(x, 3)[-1] - 100.0) < 1e-9

    # TR on a known bar
    h = np.array([10., 12.]); lo = np.array([8., 9.]); c = np.array([9., 11.])
    assert abs(V.true_range(h, lo, c)[1] - 3.0) < 1e-9   # max(3, |12-9|, |9-9|)

    # AO: SMA(1)-SMA(2) of midpoint, chosen so the arithmetic is checkable by hand
    mid_h = np.array([2., 4., 6.]); mid_l = np.array([0., 0., 0.])
    ao = M.awesome_oscillator(mid_h, mid_l, 1, 2)
    assert abs(ao[2] - (3.0 - 2.5)) < 1e-9

    # VWAP on a two-bar slice with known weights
    src = np.array([10., 20.]); vol = np.array([1., 3.])
    m, var = W._vw_moments(src, vol)
    assert abs(m - 17.5) < 1e-9
    assert abs(var - (0.25 * 100 + 0.75 * 400 - 17.5 ** 2)) < 1e-9

    # pivot(1,1) high at the obvious peak
    idx, lvl, conf = S.pivots([1., 5., 1., 0., 1.], 1, 1, "high")
    assert list(idx) == [1] and abs(lvl[0] - 5.0) < 1e-9 and list(conf) == [2]


# --------------------------------------------------------------- F-AN-2

def test_f_an_2_determinism():
    t, o, h, l, c, v = _series()
    pairs = [
        (M.rsi(c, 14), M.rsi(c, 14)),
        (M.ema(c, 21), M.ema(c, 21)),
        (V.atr(h, l, c, 14), V.atr(h, l, c, 14)),
        (W.rolling_vwap(t, W.hlc3(h, l, c), v, 7)["vwap"],
         W.rolling_vwap(t, W.hlc3(h, l, c), v, 7)["vwap"]),
        (ST.zscore(c, 20), ST.zscore(c, 20)),
    ]
    for a, b in pairs:
        assert same(a, b)


# --------------------------------------------------------------- F-AN-3 / 4

def _sources():
    return {p.name: p.read_text(encoding="utf-8") for p in sorted(PKG.glob("*.py"))}


def test_f_an_3_no_engine_imports():
    bad = {n: s for n, s in _sources().items()
           if re.search(r"^\s*(from|import)\s+engine\b", s, re.M)}
    assert not bad, f"analytics must not import engine: {list(bad)}"


def _code_only(source):
    """Source with comments and string literals removed.

    Scanning raw text is not good enough: this package's own docstrings discuss
    the banned tokens (the no-I/O rule is documented where it is enforced), so a
    naive scan reports the documentation as a violation. Tokenising and dropping
    STRING/COMMENT tokens tests the executable code, which is what the invariant
    is actually about.
    """
    import io
    import tokenize
    out = []
    for tok in tokenize.generate_tokens(io.StringIO(source).readline):
        if tok.type in (tokenize.STRING, tokenize.COMMENT):
            continue
        out.append(tok.string)
    return " ".join(out)


def test_f_an_4_no_io():
    banned = ["read_parquet", "requests", "urllib", "os.environ", "socket"]
    problems = []
    for n, s in _sources().items():
        body = _code_only(s)
        for tok in banned:
            if tok in body:
                problems.append(f"{n}: {tok}")
        # `open(` is banned as a CALL -- `open_` (the OHLC field) and `open_time`
        # are legitimate identifiers throughout this package.
        if re.search(r"\bopen\s*\(", body):
            problems.append(f"{n}: open( call")
    assert not problems, f"I/O found in analytics: {problems}"


# --------------------------------------------------------------- F-AN-5

def test_f_an_5_analytics_sha_reproducible():
    import hashlib
    h = hashlib.sha256()
    for name in analytics._MODULES:
        p = PKG / name
        if p.exists():
            h.update(name.encode("utf-8"))
            h.update(p.read_bytes())
    assert h.hexdigest() == analytics.analytics_sha()
    assert len(analytics.analytics_sha()) == 64


# --------------------------------------------------------------- F-AN-6

def test_f_an_6_warmup_lengths():
    t, o, h, l, c, v = _series(120)
    checks = [
        (M.sma(c, 10), 9), (M.ema(c, 10), 9), (M.rma(c, 10), 9),
        (M.rsi(c, 14), 14),
        # ATR warm-up is length-1, not length: true_range defines index 0 as H-L
        # rather than NaN, so the Wilder average has a full window one bar earlier
        # than RSI, whose diff() costs it a bar. CONVENTIONS records both.
        (V.atr(h, l, c, 14), 13),
        (M.awesome_oscillator(h, l, 5, 34), 33),
        (ST.zscore(c, 20), 19),
    ]
    for arr, warm in checks:
        assert np.isnan(arr[:warm]).all(), "warm-up must be NaN, never a seeded number"
        assert np.isfinite(arr[warm]), "must be finite immediately after warm-up"


# --------------------------------------------------------------- F-AN-7

def test_f_an_7_edge_cases():
    flat = np.full(60, 100.0)
    assert not np.isnan(M.rsi(flat, 14)[-1])          # documented: 50 on a flat series
    assert abs(M.rsi(flat, 14)[-1] - 50.0) < 1e-9

    t = np.arange(60, dtype="int64") * 3_600_000
    zero_vol = np.zeros(60)
    rv = W.rolling_vwap(t, flat, zero_vol, 7)
    assert np.isnan(rv["vwap"]).all(), "zero volume must be NaN, not a divide-by-zero"

    short = np.array([1., 2., 3.])
    assert np.isnan(M.rsi(short, 14)).all()           # shorter than warm-up: all NaN
    assert np.isnan(M.sma(short, 14)).all()

    vp = P.volume_profile(np.array([]), np.array([]), np.array([]))
    assert np.isnan(vp["poc"])


# --------------------------------------------------------------- F-AN-9

def test_f_an_9_cluster_reproducibility():
    reg = L.LevelRegistry()
    for fam, lab, lv in [("profile", "POC", 100.0), ("structure", "PDH", 100.4),
                         ("vwap_rolling", "R7", 100.8), ("vwap_anchored", "AM", 105.0),
                         ("ss", "Z1", 105.3), ("structure", "PIV", 130.0)]:
        reg.add(fam, lab, lv, "test")
    atr = 4.0
    m1 = L.collapse_same_family(reg.as_list(), atr)
    a = L.cluster(m1, atr)
    b = L.cluster(L.collapse_same_family(reg.as_list(), atr), atr)
    assert [x["mean"] for x in a] == [x["mean"] for x in b]
    assert [x["score"] for x in a] == [x["score"] for x in b]
    for cl in a:
        assert cl["score"] == L.score(cl["members"]), "score must recompute from members"


# --------------------------------------------------------------- F-AN-10

def test_f_an_10_rvwap_window_and_floor():
    # 20 hourly bars, then a 40-day gap, then 5 more: the 7d window would hold
    # only the 5 post-gap bars, so the 10-bar floor must engage.
    t = list(np.arange(20, dtype="int64") * 3_600_000)
    base = t[-1] + 40 * W.DAY_MS
    t += [base + i * 3_600_000 for i in range(5)]
    t = np.array(t, dtype="int64")
    src = np.arange(25, dtype=float) + 100.0
    vol = np.ones(25)

    rv = W.rolling_vwap(t, src, vol, 7)
    last = rv["vwap"][-1]
    mean_5 = float(np.mean(src[-5:]))
    mean_10 = float(np.mean(src[-10:]))
    assert abs(last - mean_10) < 1e-9, "the 10-bar floor must engage across the gap"
    assert abs(last - mean_5) > 1e-9


# --------------------------------------------------------------- F-AN-11

def test_f_an_11_variance_stability():
    """One-pass vs two-pass volume-weighted variance at BTC price scales."""
    rng = np.random.default_rng(3)
    src = 65000 + rng.normal(0, 5, 500)        # high price, low dispersion
    vol = np.abs(rng.normal(1000, 100, 500))
    _, one = W._vw_moments(src, vol)
    two = W.two_pass_vw_variance(src, vol)
    rel = abs(one - two) / max(two, 1e-12)
    assert rel < 1e-6, f"one-pass vs two-pass relative discrepancy {rel:.3e}"
    Path(ROOT / "_reviewer_box").mkdir(exist_ok=True)
    (ROOT / "_reviewer_box" / "_f_an_11.json").write_text(
        json.dumps({"one_pass": one, "two_pass": two, "relative": rel,
                    "price_scale": 65000, "tolerance": 1e-6}), encoding="utf-8")


# --------------------------------------------------------------- F-AN-12

def test_f_an_12_pivot_confirmation_lag():
    assert S.CONFIRMATION_LAG > 0
    idx, lvl, conf = S.pivots(np.array([1., 2., 9., 2., 1., 0., 1., 2., 3., 4., 5.]),
                              5, 5, "high")
    if len(idx):
        assert np.all(conf == idx + 5)
    _, _, c2 = S.confirmed_pivots(_series(200)[3], as_of_index=100, kind="low")
    assert np.all(c2 <= 100), "confirmed_pivots must never return a future confirmation"


# --------------------------------------------------------------- F-AN-13

def _series_cases():
    t, o, h, l, c, v = _series(300)
    src = W.hlc3(h, l, c)
    return [
        ("sma", lambda x: M.sma(x["c"], 20), "causal"),
        ("ema", lambda x: M.ema(x["c"], 21), "causal"),
        ("rma", lambda x: M.rma(x["c"], 14), "causal"),
        ("rsi", lambda x: M.rsi(x["c"], 14), "causal"),
        ("stoch_rsi_k", lambda x: M.stoch_rsi(x["c"])[0], "causal"),
        ("stoch_rsi_d", lambda x: M.stoch_rsi(x["c"])[1], "causal"),
        ("macd_line", lambda x: M.macd(x["c"])[0], "causal"),
        ("macd_signal", lambda x: M.macd(x["c"])[1], "causal"),
        ("macd_hist", lambda x: M.macd(x["c"])[2], "causal"),
        ("awesome_oscillator", lambda x: M.awesome_oscillator(x["h"], x["l"]), "causal"),
        ("true_range", lambda x: V.true_range(x["h"], x["l"], x["c"]), "causal"),
        ("atr", lambda x: V.atr(x["h"], x["l"], x["c"], 14), "causal"),
        ("realised_vol", lambda x: V.realised_vol(x["c"])[2], "causal"),
        ("rolling_vwap", lambda x: W.rolling_vwap(x["t"], x["src"], x["v"], 7)["vwap"], "causal"),
        ("rolling_vwap_sd", lambda x: W.rolling_vwap(x["t"], x["src"], x["v"], 7)["stdev"], "causal"),
        ("anchored_vwap", lambda x: W.anchored_vwap(x["src"], x["v"], 0)["vwap"], "causal"),
        ("zscore", lambda x: ST.zscore(x["c"], 20), "causal"),
        ("correlation", lambda x: ST.correlation(x["c"], x["h"], 20), "causal"),
        ("beta", lambda x: ST.beta(np.diff(x["c"], prepend=x["c"][0]),
                                   np.diff(x["h"], prepend=x["h"][0]), 20), "causal"),
        ("period_opens", lambda x: S.period_opens(x["t"], x["o"], "D")[1], "causal"),
        ("prior_period_extremes_h",
         lambda x: S.prior_period_extremes(x["t"], x["h"], x["l"], "D")[0], "causal"),
    ]


@pytest.mark.parametrize("name,fn,cls", _series_cases(),
                         ids=[n for n, _, _ in _series_cases()])
def test_f_an_13_causality_truncation_prefix(name, fn, cls):
    """f(x[:k])[k-1] must equal f(x)[k-1] exactly, at 5 truncation points."""
    t, o, h, l, c, v = _series(300)
    src = W.hlc3(h, l, c)
    full = {"t": t, "o": o, "h": h, "l": l, "c": c, "v": v, "src": src}
    ref = np.asarray(fn(full), dtype=float)

    for k in (40, 60, 120, 200, 299):
        cut = {kk: vv[:k] for kk, vv in full.items()}
        got = np.asarray(fn(cut), dtype=float)
        assert len(got) == k, f"{name}: truncated call returned {len(got)}, expected {k}"
        a, b = got[k - 1], ref[k - 1]
        ok = (np.isnan(a) and np.isnan(b)) or a == b
        assert ok, (f"CAUSALITY VIOLATION in {name} at k={k}: "
                    f"truncated={a!r} full={b!r} -- the function reads beyond index k-1")


def test_f_an_13_endpoint_only_raises():
    """endpoint_only functions are exempt, but MUST raise when misused."""
    sample = np.arange(100, dtype=float)
    V.percentile_rank(sample, as_of_index=99)                  # the end: fine
    with pytest.raises(ValueError):
        V.percentile_rank(sample, as_of_index=50)              # mid-array: must raise


def test_f_an_13_lag_functions_at_lag():
    """lag:N functions are tested as f(x[:k+N])[k-1] == f(x)[k-1]."""
    t, o, h, l, c, v = _series(300)
    N = S.CONFIRMATION_LAG
    full_idx, full_lvl, _ = S.pivots(h, 5, 5, "high")
    for k in (60, 120, 200, 250, 290):
        idx, lvl, _ = S.pivots(h[:k + N], 5, 5, "high")
        keep_full = [(i, x) for i, x in zip(full_idx, full_lvl) if i <= k - 1]
        keep_cut = [(i, x) for i, x in zip(idx, lvl) if i <= k - 1]
        assert keep_cut == keep_full, f"pivot lag violation at k={k}"


# --------------------------------------------------------------- F-AN-14

def test_f_an_14_resample_parity():
    """30m and 1d resampling identical to scripts/s1_resample.aggregate().

    Asserted from the TEST file -- tests may import both -- so analytics/ keeps
    invariant I-B and never imports a script.
    """
    import pandas as pd
    sys.path.insert(0, str(ROOT / "scripts"))
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "s1_resample", ROOT / "scripts" / "s1_resample.py")
    s1r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(s1r)

    t, o, h, l, c, v = _series(500)
    df = pd.DataFrame({"open_time": t, "open": o, "high": h,
                       "low": l, "close": c, "volume": v})
    for step in (1_800_000, 86_400_000):
        ref = s1r.aggregate(df, step)
        got = S.resample_ohlcv(t, o, h, l, c, v, step)
        assert list(got["open_time"]) == list(ref["open_time"].to_numpy())
        for col in ("open", "high", "low", "close", "volume"):
            assert same(got[col], ref[col].to_numpy()), f"{col} differs at step {step}"


# --------------------------------------------------------------- F-AN-8

def _dp(x):
    """Decimal places the brief actually published for a value."""
    s = repr(float(x))
    return len(s.split(".")[1]) if "." in s else 0


def test_f_an_8_brief_equivalence():
    """THE REGRESSION GUARD.

    Every recipe daily_brief.py v1.1 already computes must reproduce its
    PUBLISHED values from analytics/. A refactor that silently changes an
    already-accepted number is the worst available outcome, so this compares
    against the capture on disk rather than against a re-run.

    Published values are rounded in the capture, so agreement is asserted at the
    precision actually published and the raw signed difference is carried into
    the diff table for inspection.
    """
    cap_p = ROOT / "research_outputs" / "brief" / "brief_2026-07-28.json"
    if not cap_p.exists():
        pytest.skip("no v1.1 capture on disk to compare against")
    cap = json.loads(cap_p.read_text(encoding="utf-8"))

    sys.path.insert(0, str(ROOT))
    from engine import data as dl          # test-side only; analytics stays clean

    rows, failures = [], []
    for sym in ("BTCUSDT", "ETHUSDT", "SOLUSDT"):
        a = cap["assets"][sym]
        for tf in ("1h", "4h", "12h", "1d"):
            last = a["last_bar_utc"].get(tf)
            if last is None:
                continue
            end = int(np.datetime64(last[:-1], "ms").astype("int64"))
            if tf == "1d":
                src = dl.load_klines(sym, "1h", 0, end + 3_600_000 - 1)
                r = S.resample_ohlcv(src["open_time"].to_numpy(), src["open"].to_numpy(),
                                     src["high"].to_numpy(), src["low"].to_numpy(),
                                     src["close"].to_numpy(), src["volume"].to_numpy(),
                                     86_400_000)
                h, l, c = r["high"], r["low"], r["close"]
            else:
                k = dl.load_klines(sym, tf, 0, end)
                h, l, c = (k["high"].to_numpy(), k["low"].to_numpy(), k["close"].to_numpy())

            for name, ours, pub in (
                ("rsi14", M.rsi(c, 14)[-1],
                 a["rsi"]["timeframes"].get(tf, {}).get("value")),
                ("atr14", V.atr(h, l, c, 14)[-1],
                 a["volatility"]["atr_percentile_vs_1y"].get(tf, {}).get("atr")),
            ):
                if pub is None or ours != ours:
                    continue
                dp = _dp(pub)
                ok = round(float(ours), dp) == float(pub)
                rows.append({"asset": sym, "timeframe": tf, "recipe": name,
                             "published": float(pub), "ours": float(ours),
                             "diff": float(ours) - float(pub),
                             "published_dp": dp, "match": bool(ok)})
                if not ok:
                    failures.append(f"{sym} {tf} {name}: published {pub} vs ours {ours}")

    (ROOT / "_reviewer_box").mkdir(exist_ok=True)
    (ROOT / "_reviewer_box" / "_f_an_8_diff.json").write_text(
        json.dumps({"compared": len(rows), "mismatches": len(failures),
                    "capture": cap_p.name, "rows": rows}, indent=1), encoding="utf-8")

    assert rows, "F-AN-8 compared nothing -- the guard would be vacuous"
    assert not failures, "BRIEF EQUIVALENCE BROKEN:\n" + "\n".join(failures)
