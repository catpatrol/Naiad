"""F-AN-1..15 -- the Phase I fixture suite for `analytics/`.

Run: C:\\venvs\\naiad\\Scripts\\python.exe -m pytest tests/test_analytics.py -q

F-AN-13 is the one that matters most. It is a truncation-prefix test over every
series-returning public function, and it exists because the ENGINE lane reported
a one-sided-window hazard in daily_brief.py: code safe today only because the
caller always passes data ending at "now", which extraction converts into an
unguarded bug. Neither lane located the instance. Rather than hunt one, this
finds the whole class.
"""

import hashlib
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


def test_f_an_6b_every_series_function_is_finite_after_warmup():
    """FINDING F-2R-A: an all-NaN series satisfies F-AN-13 at every k.

    `stoch_rsi` returned all-NaN on every input -- `sma` is cumsum-based, so the
    NaN prefix of the raw stochastic poisoned everything after it -- and the
    truncation fixture passed it via its NaN-equals-NaN branch.  A guard that
    cannot fail is not a guard.  This asserts each series function actually
    PRODUCES numbers, which is the property F-AN-13 silently assumed.
    """
    t, o, h, l, c, v = _series(300)
    src = W.hlc3(h, l, c)
    series = {
        "sma": M.sma(c, 20), "ema": M.ema(c, 21), "rma": M.rma(c, 14),
        "rsi": M.rsi(c, 14),
        "stoch_rsi_k": M.stoch_rsi(c)[0], "stoch_rsi_d": M.stoch_rsi(c)[1],
        "macd_line": M.macd(c)[0], "macd_signal": M.macd(c)[1],
        "macd_hist": M.macd(c)[2],
        "awesome_oscillator": M.awesome_oscillator(h, l),
        "true_range": V.true_range(h, l, c), "atr": V.atr(h, l, c, 14),
        "realised_vol": V.realised_vol(c)[2],
        "rolling_vwap": W.rolling_vwap(t, src, v, 7)["vwap"],
        "rolling_vwap_sd": W.rolling_vwap(t, src, v, 7)["stdev"],
        "anchored_vwap": W.anchored_vwap(src, v, 0)["vwap"],
        "zscore": ST.zscore(c, 20), "correlation": ST.correlation(c, h, 20),
        "beta": ST.beta(np.diff(c, prepend=c[0]), np.diff(h, prepend=h[0]), 20),
        "period_opens": S.period_opens(t, o, "D")[1],
        "prior_period_extremes_h": S.prior_period_extremes(t, h, l, "D")[0],
    }
    for name, arr in series.items():
        arr = np.asarray(arr, dtype=float)
        n_fin = int(np.isfinite(arr).sum())
        assert n_fin > 0, (
            f"{name} is ALL NaN -- it produces no number on any input, and "
            f"F-AN-13's NaN-equals-NaN branch would pass it at every k")
        assert n_fin >= len(arr) // 2, (
            f"{name}: only {n_fin}/{len(arr)} finite -- a warm-up that consumes "
            f"more than half the series is a defect, not a warm-up")
        assert np.isfinite(arr[-1]), f"{name} is NaN at the decision bar"

    # StochRSI specifically: warm-up is exactly what CONVENTIONS records.
    d = np.asarray(series["stoch_rsi_d"], float)
    warm = 14 + 14 + 3 + 3 - 3
    assert np.isnan(d[:warm]).all() and np.isfinite(d[warm]), \
        "stoch_rsi %D warm-up must be rsi+stoch+k+d-3 = 31"
    assert 0.0 <= np.nanmin(d) and np.nanmax(d) <= 100.0, "StochRSI must be 0-100"


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
    # `profile` -> `profile_windowed` under Amendment 2 §5.1: the windowed
    # profiles get their own family so no single tool type dominates diversity.
    for fam, lab, lv in [("profile_windowed", "POC", 100.0), ("structure", "PDH", 100.4),
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


# --------------------------------------------------------------- F-AN-13b
#
# Amendment 2 §1.1: the five public functions that were outside the truncation
# discipline.  Each assertion below is written to FAIL against a deliberately
# non-causal implementation -- the naive prefix form passes vacuously on all five
# of these signatures, so it is not used anywhere in this block.


def _band_producers():
    """The two functions that actually produce a (vwap, stdev) pair."""
    return [("rolling", lambda x: W.rolling_vwap(x["t"], x["src"], x["v"], 7)),
            ("anchored", lambda x: W.anchored_vwap(x["src"], x["v"], 0))]


@pytest.mark.parametrize("pname,produce", _band_producers(),
                         ids=[n for n, _ in _band_producers()])
def test_f_an_13b_vw_sigma_bands(pname, produce):
    """vw_sigma_bands, COMPOSED -- truncating its own arguments is vacuous.

    The function takes already-computed arrays, so `f(vwap[:k], sd[:k])[k-1] ==
    f(vwap, sd)[k-1]` is satisfied by ANY element-wise map, including one handed a
    stdev built with look-ahead: passing `sd[-1:]` broadcasts index 299 across all
    300 positions and still passes that form.  So the raw series is truncated
    FIRST and the pair recomputed -- the path the level registry consumes.
    """
    t, o, h, l, c, v = _series(300)
    full = {"t": t, "o": o, "h": h, "l": l, "c": c, "v": v, "src": W.hlc3(h, l, c)}
    pf = produce(full)
    ref = W.vw_sigma_bands(pf["vwap"], pf["stdev"])
    assert set(ref) == {f"band_{s}_{k}" for s in ("up", "dn") for k in (1, 2, 3)}

    # EVERY k, not five samples.  A band that borrows the NEXT bar's dispersion
    # only diverges at the prefix's own last index, so a sparse k list misses it
    # unless a sample happens to land on the offending residue.
    for k in range(12, 300):
        cut = {kk: vv[:k] for kk, vv in full.items()}
        pc = produce(cut)
        got = W.vw_sigma_bands(pc["vwap"], pc["stdev"])
        for key in ref:
            # shape: vwap.py never checks len(vwap) == len(stdev), and numpy
            # broadcasts a length-1 operand silently rather than raising.
            assert len(got[key]) == k, (
                f"vw_sigma_bands[{key}] via {pname}: returned {len(got[key])}, "
                f"expected {k} -- a length mismatch was broadcast away")
            a_, b_ = got[key][k - 1], ref[key][k - 1]
            assert (np.isnan(a_) and np.isnan(b_)) or a_ == b_, (
                f"CAUSALITY VIOLATION in vw_sigma_bands[{key}] via {pname} at "
                f"k={k}: truncated={a_!r} full={b_!r}")
            # index-locality: banding a prefix IS the prefix of banding.
            assert same(got[key], ref[key][:k]), (
                f"vw_sigma_bands[{key}] via {pname} at k={k}: the helper couples "
                f"indices -- banding a prefix != prefix of banding")

    # ANTI-VACUITY: bands must be finite somewhere, or every assertion above is
    # NaN == NaN.  (A zero-volume series makes them all NaN and passes silently.)
    assert np.isfinite(ref["band_up_1"]).sum() > 100

    # DRIFT PIN: the bands that actually ship are duplicated inline at
    # vwap.py:96-97 and vwap.py:128-129, not routed through this helper.
    for key in ref:
        assert same(ref[key], pf[key]), (
            f"{pname}: inline band arithmetic has drifted from vw_sigma_bands")


@pytest.mark.parametrize("pivot_kind", ["high", "low"])
@pytest.mark.parametrize("kind", ["regular", "hidden"])
def test_f_an_13b_divergences_at_lag(pivot_kind, kind):
    """divergences at lag:5, both regular and hidden (Amendment 2 §1.1).

    A plain prefix-vs-full equality here is a TAUTOLOGY: at N=5 the arrays
    `pivots(px[:k+5])` and `pivots(px)[idx <= k-1]` are bit-identical, so both
    sides are the same function applied to the same values and the assertion
    cannot fail.  Measured: it passes against mutants that report agreements as
    divergences, invert regular/hidden, read the oscillator at the wrong index,
    pair non-adjacent pivots, and emit a from_index five bars in the future.

    So this asserts STRUCTURAL INVARIANTS of each emitted record instead.
    """
    # seed 2, not the file default: on seed 7 only two of the four
    # (pivot_kind, kind) combinations EVER produce a divergence, at any k, so
    # half the parametrisation would assert over an empty set.  Seed 2 yields all
    # four (9 / 20 / 12 / 7 records across the sweep below).
    t, o, h, l, c, v = _series(300, seed=2)
    N = S.CONFIRMATION_LAG
    px = h if pivot_kind == "high" else l
    osc = M.rsi(c, 14)

    seen = 0
    for k in range(60, 296, 5):
        as_of = k - 1
        p_idx, p_val, p_conf = S.confirmed_pivots(px[:k + N], as_of, 5, 5, pivot_kind)
        o_idx, o_val, _ = S.confirmed_pivots(osc[:k + N], as_of, 5, 5, pivot_kind)
        out = M.divergences(p_idx, p_val, o_idx, o_val, pivot_kind, kind=kind)

        omap = dict(zip(o_idx.tolist(), o_val.tolist()))
        usable = [i for i in p_idx.tolist() if i in omap]
        adjacent = set(zip(usable[:-1], usable[1:]))

        assert len(out) <= 2, "max_pairs=2 must bound the output"
        for d in out:
            i0, i1 = d["from_index"], d["to_index"]
            # never name a bar at or beyond the decision bar
            assert i0 <= as_of and i1 <= as_of, (
                f"divergence names bar {max(i0, i1)} > as_of {as_of}")
            assert i0 < i1, "from_index must precede to_index"
            # pivots must be ADJACENT in the usable sequence
            assert (i0, i1) in adjacent, (
                f"({i0},{i1}) are not adjacent confirmed pivots")
            # the oscillator legs must be read at the pivots' own indices
            assert d["osc_from"] == omap[i0] and d["osc_to"] == omap[i1], \
                "oscillator read at the wrong index"
            # it must actually be a DISAGREEMENT
            assert (d["price_to"] > d["price_from"]) != (d["osc_to"] > d["osc_from"]), \
                "an agreement was reported as a divergence"
            # regular/hidden must match the definitional table
            price_up = d["price_to"] > d["price_from"]
            expect = ("regular" if not price_up else "hidden") if pivot_kind == "low" \
                     else ("regular" if price_up else "hidden")
            assert d["kind"] == expect == kind, "regular/hidden mislabelled"
            assert d["direction"] == ("bullish" if pivot_kind == "low" else "bearish")
            assert d["price_level"] == d["price_to"], "price_level must be the LATER pivot"
            seen += 1

        # truncation at lag: recomputing from the full series, filtered to the
        # same decision bar, must reproduce the record set exactly.
        fp_i, fp_v, _ = S.confirmed_pivots(px, as_of, 5, 5, pivot_kind)
        fo_i, fo_v, _ = S.confirmed_pivots(osc, as_of, 5, 5, pivot_kind)
        assert M.divergences(fp_i, fp_v, fo_i, fo_v, pivot_kind, kind=kind) == out

    assert seen > 0, "compared nothing -- the invariants would be vacuous"


def test_f_an_13b_naked_poc_registry_set_stability():
    """naked_poc_registry -- SET-MEMBERSHIP STABILITY (Amendment 2 §1.1).

    Hand-built geometry, because a random series does not discriminate: against
    _series(300) at k in (40,60,120,200,299) a registry that reads one bar PAST
    the decision bar is caught on 0% of seeds, and five bars past on 0%.  The
    minimal series below separates them exactly.
    """
    # level 5.0 is untouched at bars 1-2 and touched at bar 3.
    hi = np.array([10., 10., 10., 10.])
    lo = np.array([0., 9., 9., 0.])
    pocs = [(0, 5.0)]

    at2 = P.naked_poc_registry(pocs, hi, lo, as_of_index=2)
    at3 = P.naked_poc_registry(pocs, hi, lo, as_of_index=3)
    assert [d["level"] for d in at2] == [5.0], \
        "level 5.0 is untested through bar 2 and must be in the registry"
    assert at3 == [], \
        "bar 3 straddles 5.0, so the level is tested and must LEAVE the registry"
    # a registry reading as_of_index+1 would return [] at as_of 2 -- caught above.

    # the as-of guard must drop POCs stamped after the decision bar
    future = P.naked_poc_registry([(3, 5.0)], hi, lo, as_of_index=1)
    assert future == [], "a POC stamped at bar 3 must not appear as-of bar 1"

    # truncation: slicing the arrays to the decision bar changes nothing
    # Two POC families on purpose: levels well above the traded range stay naked
    # (so the comparison is never empty), while levels drawn from the close are
    # revisited (so the touched-and-removed path is exercised too).  Levels at
    # h[i] alone are almost always touched within a few bars, which empties the
    # registry and makes the sweep vacuous.
    t, o, h, l, c, v = _series(300)
    every = ([(i, float(h[i]) + 2000.0) for i in range(10, 200, 17)]
             + [(i, float(c[i])) for i in range(10, 200, 17)])
    compared = 0
    for k in (40, 60, 120, 200, 299):
        cut = P.naked_poc_registry(every, h[:k], l[:k], as_of_index=k - 1)
        ful = P.naked_poc_registry(every, h, l, as_of_index=k - 1)
        key = lambda r: sorted((d["index"], d["level"]) for d in r)
        assert key(cut) == key(ful), (
            f"registry differs between truncated and full input at k={k} -- "
            f"the function reads beyond the decision bar")
        assert cut, f"registry empty at k={k} -- the comparison would be vacuous"
        compared += len(cut)
    assert compared > 0


@pytest.mark.parametrize("left,right", [(5, 5), (3, 7), (7, 3)])
@pytest.mark.parametrize("kind", ["high", "low"])
def test_f_an_13b_confirmed_pivots(left, right, kind):
    """confirmed_pivots -- set stability AND no confirmation from partial windows.

    Equality alone is not enough: it passes against a mutant that admits a pivot
    `right` bars before its window closes, because the prefix physically cannot
    detect index k-1 and only the FULL-array reference leaks.  The two extra
    invariants below bound the reference too.
    """
    t, o, h, l, c, v = _series(300)
    vals = h if kind == "high" else l
    total = 0
    for k in (40, 60, 120, 200, 299):
        as_of = k - 1
        ci, cl, cc = S.confirmed_pivots(vals[:k], as_of, left, right, kind)
        fi, fl, fc = S.confirmed_pivots(vals, as_of, left, right, kind)
        assert list(ci) == list(fi) and same(cl, fl) and list(cc) == list(fc), (
            f"confirmed_pivots differs truncated vs full at k={k} "
            f"({left},{right},{kind})")

        for i, lv, cf in zip(fi, fl, fc):
            # never confirm using a bar at or after the decision bar
            assert cf <= as_of, f"pivot {i} confirmed at {cf} > as_of {as_of}"
            assert cf == i + right, "confirmation lag must be exactly `right`"
            # the pivot must be a strict extreme of its FULL window, measured on
            # the full array -- this is what catches confirmation from a window
            # that was truncated at the array end.
            w = vals[i - left:i + right + 1]
            assert len(w) == left + right + 1, "window must be complete"
            best = np.max(w) if kind == "high" else np.min(w)
            assert lv == best and np.sum(w == lv) == 1, (
                f"pivot {i} is not the unique strict extreme of its window -- "
                f"it was confirmed on partial evidence")
        total += len(fi)
    assert total > 0, "found no pivots -- the assertions would be vacuous"

    # AS-OF AT AND BEYOND THE ARRAY END.  `as_of_index` is an unvalidated free
    # parameter, and the two mutations that matter here are invisible at
    # as_of = n-1: `range(left, n)` (confirm from a window the array cannot fill)
    # and `keep = (conf <= as_of) | (idx == as_of)` (admit before the window
    # closes) both only bite once as_of reaches the end.  Measured: without this
    # block both survive the fixture.
    n = 300
    for as_of in (n - right - 1, n - 2, n - 1, n, n + right):
        ai, al, ac = S.confirmed_pivots(vals, as_of, left, right, kind)
        for i, lv, cf in zip(ai, al, ac):
            assert cf <= as_of, f"pivot {i} confirmed at {cf} > as_of {as_of}"
            assert i + right + 1 <= n, (
                f"pivot {i} confirmed from a window running past the array end "
                f"(as_of={as_of}) -- confirmation on partial evidence")
            w = vals[i - left:i + right + 1]
            assert len(w) == left + right + 1
            best = np.max(w) if kind == "high" else np.min(w)
            assert lv == best and np.sum(w == lv) == 1

    # a pivot may never be confirmed by a bar that does not exist yet
    dense = 0
    for as_of in range(50, n, 3):
        di, _, dc = S.confirmed_pivots(vals, as_of, left, right, kind)
        assert all(cf <= as_of for cf in dc), \
            f"confirmation leaked past as_of={as_of}"
        assert all(i + right <= as_of for i in di), \
            f"a pivot was admitted before its window closed at as_of={as_of}"
        dense += len(di)
    assert dense > 0, "dense sweep found no pivots -- it would be vacuous"


def test_f_an_13b_resample_ohlcv_bucket_prefix():
    """resample_ohlcv -- prefix rule on the BUCKET axis.

    The naive form does not apply: the return is re-keyed onto buckets, so index
    k-1 is bucket k-1, not bar k-1.  The correct statement is that growing the
    input only APPENDS buckets -- it never revises or removes one already
    emitted.  test_f_an_14d asserts the same property on the input that used to
    break it; this one asserts it on the ordinary grid.
    """
    t, o, h, l, c, v = _series(500)
    compared = 0
    for step in (1_800_000, 86_400_000):
        full = S.resample_ohlcv(t, o, h, l, c, v, step)
        for k in (100, 200, 300, 400, 500):
            cut = S.resample_ohlcv(t[:k], o[:k], h[:k], l[:k], c[:k], v[:k], step)
            n = len(cut["open_time"])
            assert n <= len(full["open_time"])
            for col in ("open_time", "open", "high", "low", "close", "volume"):
                assert same(np.asarray(cut[col], float),
                            np.asarray(full[col][:n], float)), (
                    f"{col}: bucket set at k={k} is not a prefix of the full run "
                    f"at step {step} -- a published bucket was revised")
            compared += n
    assert compared > 0, "compared no buckets -- the guard would be vacuous"


# --------------------------------------------------------------- F-AN-14

def test_f_an_14_resample_parity():
    """30m and 1d aggregation identical to scripts/s1_resample.aggregate().

    Asserted from the TEST file -- tests may import both -- so analytics/ keeps
    invariant I-B and never imports a script.

    Compared against the LEGACY entry point on purpose.  Amendment FAN8 changed
    which buckets are EMITTED, not how a bucket is AGGREGATED, and this fixture
    is about the aggregation.  Comparing the legacy form keeps it testing what it
    was written to test; the public form is then checked against the legacy one
    below, which is where the amendment's effect belongs.
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
        got = S._resample_ohlcv_legacy(t, o, h, l, c, v, step)
        assert list(got["open_time"]) == list(ref["open_time"].to_numpy())
        for col in ("open", "high", "low", "close", "volume"):
            assert same(got[col], ref[col].to_numpy()), f"{col} differs at step {step}"


def test_f_an_14b_public_is_legacy_minus_unclosed():
    """The public form differs from legacy by AT MOST the final forming bucket."""
    t, o, h, l, c, v = _series(500)          # hourly bars, 500 of them
    for step in (1_800_000, 86_400_000):
        legacy = S._resample_ohlcv_legacy(t, o, h, l, c, v, step)
        public = S.resample_ohlcv(t, o, h, l, c, v, step)
        n = len(public["open_time"])
        assert n in (len(legacy["open_time"]), len(legacy["open_time"]) - 1)
        for col in ("open_time", "open", "high", "low", "close", "volume"):
            assert same(np.asarray(public[col], float),
                        np.asarray(legacy[col][:n], float)), \
                f"{col}: public is not a prefix of legacy at step {step}"

    # AMENDMENT 2 §1.2 EXTENDED: the public form now emits only buckets PROVED
    # closed by a bar in a strictly later bucket, so it is legacy minus exactly
    # one bucket at EVERY step -- including 30m, where the old median-reach rule
    # kept the final bucket because one hourly bar filled it.
    assert len(S.resample_ohlcv(t, o, h, l, c, v, 1_800_000)["open_time"]) == \
        len(S._resample_ohlcv_legacy(t, o, h, l, c, v, 1_800_000)["open_time"]) - 1

    # 500 hourly bars = 20 days + 20 hours: the final day is NOT closed.
    d_pub = S.resample_ohlcv(t, o, h, l, c, v, 86_400_000)["open_time"]
    d_leg = S._resample_ohlcv_legacy(t, o, h, l, c, v, 86_400_000)["open_time"]
    assert len(d_pub) == len(d_leg) - 1, "the forming day must be dropped"

    # A day that LOOKS fully populated is dropped too, and that is the point.
    # _series starts at 1_600_000_000_000 = 12:26:40 UTC -- NOT a day boundary --
    # so a plain prefix can never end on one. Build a day-aligned span.
    #
    # This assertion INVERTED under Amendment 2 §1.2 as extended.  It previously
    # read "a fully-populated final bucket must NOT be dropped".  Finding F-1R-A
    # showed that "fully populated" is not decidable from the data: a sparse
    # 2h-spaced day is byte-for-byte indistinguishable from a complete one, and
    # trusting the appearance is what published-then-revised a bucket.  Closure
    # is now proved by a witness bar in a later bucket, which the final bucket
    # can never have.  Measured cost on the estate: zero -- 1h->4h and 1h->1d on
    # all ten assets give identical bucket counts, because live data always
    # carries a forming final bucket that both rules drop.
    n = 48
    t2 = (np.arange(n, dtype="int64") * 3_600_000) + (1_600_000_000_000 // DAY_MS) * DAY_MS
    ones = np.ones(n)
    assert t2[0] % DAY_MS == 0 and (t2[-1] + 3_600_000) % DAY_MS == 0, \
        "the aligned fixture must start and end exactly on a day boundary"
    pub2 = S.resample_ohlcv(t2, ones, ones, ones, ones, ones, DAY_MS)["open_time"]
    leg2 = S._resample_ohlcv_legacy(t2, ones, ones, ones, ones, ones, DAY_MS)["open_time"]
    assert len(leg2) == 2, "legacy must still keep the aligned final bucket"
    assert len(pub2) == 1, \
        "closure must be PROVED by a later bar, never inferred from appearance"


def test_f_an_14c_prime_undecidable_step_raises():
    """F-AN-14c' -- Amendment 2 §1.2: refuse, do not keep.

    Replaces test_f_an_14c_undecidable_closure_keeps_the_bucket, which asserted
    the pre-amendment behaviour: a single 1h bar handed to a 1d resample returned
    a "day" holding 1/24 of a day.  The ruling is that a function whose safety
    depends on how it is called is the hazard F-AN-13 exists to abolish.
    """
    one = np.array([1.0])

    # fewer than two timestamps -- spacing unknowable
    t1 = np.array([1_600_000_000_000], dtype="int64")
    with pytest.raises(S.UndecidableStepError):
        S.resample_ohlcv(t1, one, one, one, one, one, 86_400_000)

    # all-identical stamps -- infer_step_ms finds no positive gap
    t2 = np.array([1_600_000_000_000] * 4, dtype="int64")
    four = np.ones(4)
    with pytest.raises(S.UndecidableStepError):
        S.resample_ohlcv(t2, four, four, four, four, four, 86_400_000)

    # it is a ValueError subclass, so existing handlers keep working
    assert issubclass(S.UndecidableStepError, ValueError)

    # the escape hatch is NOT poisoned: legacy mode still reproduces v1.1, which
    # is what lets F-AN-8b prove the dropped bar is the only difference.
    leg = S._resample_ohlcv_legacy(t1, one, one, one, one, one, 86_400_000)
    assert len(leg["open_time"]) == 1

    # ANTI-VACUITY: a decidable step must NOT raise, or the test above would pass
    # against a function that raises unconditionally.
    t3 = np.arange(48, dtype="int64") * 3_600_000 + 1_600_000_000_000
    ok = np.ones(48)
    S.resample_ohlcv(t3, ok, ok, ok, ok, ok, 86_400_000)


def test_f_an_14d_published_bucket_is_never_revised():
    """FINDING F-1R-A, closed: a published bucket must never later change.

    The regression guard for the defect Amendment 2 §1.2 was extended to cover.
    The old rule inferred the final bar's reach from the MEDIAN spacing and
    published the bucket when that reach met the boundary; on a sparse-then-dense
    feed the median was decidable but wrong, so the §1.2 raise never fired and
    the bucket was published and then revised.

    Both inputs below are well-formed: strictly monotonic, duplicate-free, every
    stamp on the hour.  Neither triggers UndecidableStepError.
    """
    HOUR, DAY = 3_600_000, 86_400_000
    DAY0 = (1_600_000_000_000 // DAY) * DAY

    def published(t, vol):
        n = len(t)
        a = np.arange(1, n + 1, dtype=float)
        return S.resample_ohlcv(t, a, a, a, a, np.asarray(vol, float), DAY)

    # sparse first day (2h apparent spacing), then the feed densifies to 1h
    hours = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22] + list(range(23, 48))
    t = np.array(hours, dtype="int64") * HOUR + DAY0
    vol = [10.0] * len(t)
    assert np.all(np.diff(t) > 0), "the fixture input must be strictly monotonic"
    assert S.infer_step_ms(t[:12]) is not None, \
        "the fixture must exercise the DECIDABLE branch, not the §1.2 raise"

    for k in range(2, len(t) + 1):
        cut = published(t[:k], vol[:k])
        full = published(t, vol)
        full_by_key = dict(zip(full["open_time"].tolist(), full["volume"].tolist()))
        for key, v_ in zip(cut["open_time"].tolist(), cut["volume"].tolist()):
            assert key in full_by_key, (
                f"bucket {key} published at k={k} vanishes from the full run")
            assert v_ == full_by_key[key], (
                f"REVISION: bucket {key} published at k={k} with volume {v_}, "
                f"but the full run reports {full_by_key[key]} -- a bucket that "
                f"was published later changed")

    # ANTI-VACUITY: the sweep must actually have published something.
    assert len(published(t, vol)["open_time"]) >= 1


# --------------------------------------------------------------- F-AN-8

def _dp(x):
    """Decimal places the brief actually published for a value."""
    s = repr(float(x))
    return len(s.split(".")[1]) if "." in s else 0


CAPTURE = Path("research_outputs") / "brief" / "brief_2026-07-28.json"
DAY_MS = 86_400_000
STEP_MS = {"1h": 3_600_000, "4h": 14_400_000, "12h": 43_200_000, "1d": DAY_MS}

# How daily_brief.py v1.1 actually sources each layer, which is the whole point:
#   rsi_layer(k["1h"])    -> 1h NATIVE, everything above it RESAMPLED from 1h
#   volatility_layer(k)   -> 1h/4h/12h NATIVE, 1d RESAMPLED from 1h (load_all:1513)
NATIVE = {("rsi14", "1h"), ("atr14", "1h"), ("atr14", "4h"), ("atr14", "12h")}


def _fan8_rows():
    """(rows, capture_name).  Each row carries published / legacy / corrected.

    Built once and shared by 8a, 8b and 8c so the three cannot disagree about
    what they are looking at.
    """
    cap_p = ROOT / CAPTURE
    if not cap_p.exists():
        return None, None
    cap = json.loads(cap_p.read_text(encoding="utf-8"))

    sys.path.insert(0, str(ROOT))
    from engine import data as dl          # test-side only; analytics stays clean

    rows = []
    for sym in ("BTCUSDT", "ETHUSDT", "SOLUSDT"):
        a = cap["assets"][sym]
        end_1h = a["last_bar_utc"].get("1h")
        if end_1h is None:
            continue
        end_1h = int(np.datetime64(end_1h[:-1], "ms").astype("int64"))
        k1h = dl.load_klines(sym, "1h", 0, end_1h)
        base = tuple(k1h[c].to_numpy() for c in
                     ("open_time", "open", "high", "low", "close", "volume"))

        for tf in ("1h", "4h", "12h", "1d"):
            last = a["last_bar_utc"].get(tf)
            if last is None:
                continue
            end = int(np.datetime64(last[:-1], "ms").astype("int64"))

            def hlc(resampler=None, _tf=tf, _end=end):
                if resampler is None:                     # native load
                    k = dl.load_klines(sym, _tf, 0, _end)
                    return (k["high"].to_numpy(), k["low"].to_numpy(),
                            k["close"].to_numpy())
                r = resampler(*base, STEP_MS[_tf])
                return r["high"], r["low"], r["close"]

            for recipe in ("rsi14", "atr14"):
                pub = (a["rsi"]["timeframes"].get(tf, {}).get("value")
                       if recipe == "rsi14"
                       else a["volatility"]["atr_percentile_vs_1y"].get(tf, {}).get("atr"))
                if pub is None:
                    continue
                native = (recipe, tf) in NATIVE
                h1, l1, c1 = hlc(None if native else S.resample_ohlcv)
                h0, l0, c0 = hlc(None if native else S._resample_ohlcv_legacy)

                def val(h_, l_, c_, _r=recipe):
                    return (M.rsi(c_, 14)[-1] if _r == "rsi14"
                            else V.atr(h_, l_, c_, 14)[-1])

                corrected, legacy = float(val(h1, l1, c1)), float(val(h0, l0, c0))
                if corrected != corrected or legacy != legacy:
                    continue
                dp = _dp(pub)
                rows.append({
                    "asset": sym, "timeframe": tf, "recipe": recipe,
                    "source": "native" if native else "resampled from 1h",
                    "convention_changed": not native,
                    "published_v1_1": float(pub), "published_dp": dp,
                    "corrected": corrected, "legacy": legacy,
                    "delta_vs_published": corrected - float(pub),
                    "legacy_matches_published": round(legacy, dp) == float(pub),
                    "corrected_matches_published": round(corrected, dp) == float(pub),
                })
    return rows, cap_p.name


def test_f_an_8a_unchanged_conventions_reproduce_exactly():
    """8a -- every recipe whose closed-bar convention did NOT change reproduces
    its v1.1 published value on the frozen fixture day.

    Published values are rounded in the capture, so agreement is asserted at the
    precision actually published; the raw signed difference goes into the 8c
    table for inspection.
    """
    rows, cap = _fan8_rows()
    if rows is None:
        pytest.skip("no v1.1 capture on disk to compare against")
    unchanged = [r for r in rows if not r["convention_changed"]]
    assert unchanged, "8a compared nothing -- the guard would be vacuous"
    bad = [f"{r['asset']} {r['timeframe']} {r['recipe']}: "
           f"published {r['published_v1_1']} vs ours {r['corrected']}"
           for r in unchanged if not r["corrected_matches_published"]]
    assert not bad, "UNCHANGED CONVENTION MOVED:\n" + "\n".join(bad)


def test_f_an_8b_legacy_mode_reproduces_v1_1_exactly():
    """8b -- reinstating the in-progress bucket must reproduce v1.1 EXACTLY.

    This is the load-bearing fixture of the whole amendment.  If a legacy-mode
    recomputation reproduces the published number, then the dropped bar is the
    ONLY thing that changed.  If it does NOT, something else moved and that is a
    finding, not a tolerance to widen.
    """
    rows, cap = _fan8_rows()
    if rows is None:
        pytest.skip("no v1.1 capture on disk to compare against")
    changed = [r for r in rows if r["convention_changed"]]
    assert changed, "8b compared nothing -- no resampled layer was exercised"
    bad = [f"{r['asset']} {r['timeframe']} {r['recipe']}: "
           f"published {r['published_v1_1']} vs legacy {r['legacy']}"
           for r in changed if not r["legacy_matches_published"]]
    assert not bad, (
        "LEGACY MODE DID NOT REPRODUCE v1.1 -- the dropped bar is NOT the only "
        "difference. HALT and investigate; do not widen a tolerance:\n"
        + "\n".join(bad))


def test_f_an_8b_legacy_is_unreachable_from_production():
    """Legacy mode must not be reachable from the brief, by name or by flag."""
    brief = (ROOT / "scripts" / "daily_brief.py").read_text(encoding="utf-8")
    for token in ("_resample_ohlcv_legacy", "drop_unclosed"):
        assert token not in brief, \
            f"production references legacy resampling: {token!r} in daily_brief.py"
    assert "_resample_ohlcv_legacy" not in S.__all__
    assert "drop_unclosed" not in " ".join(S.__all__)


def test_f_an_8c_documented_diff():
    """8c -- emit the asset x timeframe x recipe diff, with verdict impact.

    Both momentum confluence votes read these layers:
        rsi4h_bull_side  = rsi 4h  > 50      (daily_brief.py:1241)
        rsi12h_bull_side = rsi 12h > 50      (daily_brief.py:1242)
    so a corrected value that crosses 50 flips a published vote.  Any such flip
    is recorded explicitly rather than left for a reader to notice.
    """
    rows, cap = _fan8_rows()
    if rows is None:
        pytest.skip("no v1.1 capture on disk to compare against")

    verdicts = []
    for r in rows:
        if r["recipe"] != "rsi14" or r["timeframe"] not in ("4h", "12h"):
            continue
        flag = f"rsi{r['timeframe']}_bull_side"
        was, now = r["published_v1_1"] > 50, r["corrected"] > 50
        r["verdict_flag"] = flag
        r["verdict_v1_1"] = bool(was)
        r["verdict_corrected"] = bool(now)
        r["verdict_flipped"] = bool(was != now)
        if was != now:
            verdicts.append({"asset": r["asset"], "flag": flag,
                             "from": bool(was), "to": bool(now),
                             "published_v1_1": r["published_v1_1"],
                             "corrected": r["corrected"]})

    changed = [r for r in rows if r["convention_changed"]]
    moved = [r for r in changed if not r["corrected_matches_published"]]
    payload = {
        "fixture": "F-AN-8c",
        "amendment": "prompts/CONTRACT_v4_Amendment_FAN8.md",
        "analytics_version": analytics.ANALYTICS_VERSION,
        "analytics_sha": analytics.analytics_sha(),
        "capture": cap,
        "summary": {
            "compared": len(rows),
            "unchanged_convention": len(rows) - len(changed),
            "changed_convention": len(changed),
            "published_values_that_moved": len(moved),
            "verdict_flips": len(verdicts),
        },
        "verdict_changes": verdicts,
        "rows": rows,
    }
    for d in (ROOT / "_reviewer_box",):
        d.mkdir(exist_ok=True)
        (d / "f_an_8_diff.json").write_text(json.dumps(payload, indent=1),
                                            encoding="utf-8")
    # the historical filename stays too: earlier reports cite it
    (ROOT / "_reviewer_box" / "_f_an_8_diff.json").write_text(
        json.dumps(payload, indent=1), encoding="utf-8")

    assert rows, "8c documented nothing"
    assert (ROOT / "_reviewer_box" / "f_an_8_diff.json").exists()


# --------------------------------------------------------------- F-AN-15

_IFACE_NAME = re.compile(r"^INTERFACE_(\d{4}-\d{2}-\d{2})(?:_.+)?\.md$")


def _newest_published_interface():
    """The newest `exchange/reports/INTERFACE_*.md`, or None if there is none.

    "Newest" is decided by the ISO DATE IN THE FILENAME, never by mtime.  git
    does not preserve mtimes, so a fresh clone would pick a different file than
    this working tree does, and a fixture that compares different files on
    different machines is not a fixture.
    """
    d = ROOT / "exchange" / "reports"
    if not d.is_dir():
        return None
    dated = [(m.group(1), p.name, p)
             for p in d.glob("INTERFACE_*.md")
             if (m := _IFACE_NAME.match(p.name))]
    if not dated:
        return None
    return max(dated, key=lambda row: (row[0], row[1]))[2]


def _sha256_bytes(blob):
    return hashlib.sha256(blob).hexdigest()


def test_f_an_15_published_interface_is_byte_identical():
    """The published contract must be the canonical contract, byte for byte.

    `analytics/INTERFACE.md` is canonical, but it lives under `analytics/` and
    a web lane cannot reach it.  APOLLO cites the `exchange/reports/` copy.  Two
    files, one contract: the moment they diverge, the census-facing lane is
    reading a contract this code no longer honours, and nothing anywhere says so.

    This fixture is the thing that says so.

    IT DOES NOT RE-COPY ON MISMATCH, BY DESIGN.  An automated re-export would
    succeed every single time and would therefore report a green suite for
    exactly the staleness it was built to catch.  The fix is one deliberate
    copy, named in the failure message, made by a human who has decided the
    canonical file is the one to publish.

    It SKIPS -- it does not pass -- when no published copy exists.  A missing
    mirror is an unanswered question, not a satisfied assertion.
    """
    canonical = PKG / "INTERFACE.md"
    assert canonical.is_file(), (
        f"canonical contract missing: {canonical} -- F-AN-15 cannot compare "
        f"against a file that is not there, and must not pretend it can")

    published = _newest_published_interface()
    if published is None:
        pytest.skip(
            "SKIPPED, NOT PASSED: no exchange/reports/INTERFACE_<date>*.md "
            "exists, so there is no published copy to compare against. This is "
            "not a green result -- the census-facing lanes (APOLLO) have no "
            "contract to read at all. Publish one with:\n"
            f"    copy analytics\\INTERFACE.md "
            f"exchange\\reports\\INTERFACE_<YYYY-MM-DD>_C6.md")

    can_bytes = canonical.read_bytes()          # binary: no newline translation
    pub_bytes = published.read_bytes()
    can_sha, pub_sha = _sha256_bytes(can_bytes), _sha256_bytes(pub_bytes)

    assert len(can_bytes) > 0, (
        f"{canonical} is EMPTY -- two empty files hash alike and the comparison "
        f"would pass while saying nothing")

    # Both directions, always reported -- which file is ahead is the operator's
    # first question and the fixture should never make them go and find out.
    if can_sha != pub_sha:
        first_diff = next(
            (i for i, (x, y) in enumerate(zip(can_bytes, pub_bytes)) if x != y),
            min(len(can_bytes), len(pub_bytes)))
        raise AssertionError(
            "PUBLISHED CONTRACT IS STALE -- the two copies are NOT identical.\n"
            f"  canonical  analytics/INTERFACE.md\n"
            f"             sha256 {can_sha}\n"
            f"             bytes  {len(can_bytes)}\n"
            f"  published  exchange/reports/{published.name}\n"
            f"             sha256 {pub_sha}\n"
            f"             bytes  {len(pub_bytes)}\n"
            f"  delta      published - canonical = "
            f"{len(pub_bytes) - len(can_bytes):+d} bytes; "
            f"first differing byte at offset {first_diff}\n"
            "\n"
            "  APOLLO is reading the published copy. It no longer matches the "
            "code.\n"
            "\n"
            "  THIS FIXTURE WILL NOT FIX IT FOR YOU. An automatic re-export "
            "would\n"
            "  turn this test green without anyone deciding the canonical file "
            "was\n"
            "  ready to publish, which is the failure it exists to prevent. "
            "Make\n"
            "  the copy deliberately, from the repo root:\n"
            "\n"
            f"      copy analytics\\INTERFACE.md "
            f"exchange\\reports\\{published.name}\n"
            "\n"
            "  -- or publish under today's date instead, leaving the old "
            "snapshot\n"
            "  in place as history:\n"
            "\n"
            "      copy analytics\\INTERFACE.md "
            "exchange\\reports\\INTERFACE_<YYYY-MM-DD>_C6.md")

    print(f"\nF-AN-15: IDENTICAL\n"
          f"  analytics/INTERFACE.md              "
          f"sha256 {can_sha}  {len(can_bytes)} B\n"
          f"  exchange/reports/{published.name}  "
          f"sha256 {pub_sha}  {len(pub_bytes)} B")
