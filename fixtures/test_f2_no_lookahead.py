"""F2 — no-lookahead.

(a) Synthetic proof of invariant 2: an HTF value/event becomes visible to an
    exec bar only once the HTF bar's close time <= the exec bar's open time —
    and REGIME events surface exactly at the governor cross bar's close.
(b) Truncation: a replay ended at T equals the T-portion of a longer run
    (same rows, byte-for-byte except run_id, which encodes the args; EXIT
    rows whose enrichment window extends past T are buffered by design and
    may only appear in the longer run).
"""

import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from conftest import SYNTH_END, SYNTH_START

from engine import indicators as ind
from engine.cells import INTERVAL_MS
from engine.config import load_config
from engine.htf import map_htf_to_exec, take
from engine.journal import read_journal
from engine.replay import run_replay


def test_htf_mapping_unit():
    # HTF bars of 1h at 0 and 3600s; exec 1m bars across the boundary.
    htf_open = np.array([0, 3_600_000], dtype=np.int64)
    exec_open = np.array([3_540_000, 3_600_000, 3_660_000, 7_200_000],
                         dtype=np.int64)
    idx = map_htf_to_exec(exec_open, htf_open, "1h")
    # 59min bar: no HTF bar closed yet -> -1. At 60min: bar0 just closed.
    assert list(idx) == [-1, 0, 0, 1]
    vals = take(np.array([10.0, 20.0]), idx)
    assert np.isnan(vals[0]) and vals[1] == 10.0 and vals[3] == 20.0


def _iso_to_ms(s: str) -> int:
    return int(datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
               .replace(tzinfo=timezone.utc).timestamp() * 1000)


def test_regime_visible_only_after_governor_close(synth_env, synth_cell, tmp_path):
    run_replay("naiad_v0", synth_cell.cell_id, SYNTH_START, SYNTH_END,
               tmp_path / "j", log=lambda *_: None)
    rows = read_journal(tmp_path / "j", synth_cell.cell_id)
    regimes = [r for r in rows if r["evt"] == "REGIME"]
    assert regimes, "synthetic data produced no governor crosses in-window"

    from engine.data import load_klines
    p = load_config("naiad_v0")["signal"]
    gov = load_klines("BTCUSDT", synth_cell.tf_gov, 0, 2**62)
    c = gov["close"].to_numpy(float)
    e9 = ind.ema(c, p["len_fast"])
    e89 = ind.ema(c, p["len_slow"])
    bx = ind.crossover(e9, e89)
    sx = ind.crossunder(e9, e89)
    gov_open = gov["open_time"].to_numpy(np.int64)
    step = INTERVAL_MS[synth_cell.tf_gov]

    for r in regimes:
        ts = _iso_to_ms(r["ts_open"])
        # the journal row's bar OPEN must equal some governor cross bar's
        # CLOSE — visible at the first instant afterward, never before
        k = np.where(gov_open + step == ts)[0]
        assert len(k) == 1, f"REGIME at {r['ts_open']} not on a governor close"
        flag = bx[k[0]] if r["dir"] == "long" else sx[k[0]]
        assert flag, f"REGIME at {r['ts_open']} without a confirmed cross"


def test_truncation_prefix(synth_env, synth_cell, tmp_path):
    t_short, t_long = "2024-01-18", SYNTH_END
    run_replay("naiad_v0", synth_cell.cell_id, SYNTH_START, t_short,
               tmp_path / "js", log=lambda *_: None)
    run_replay("naiad_v0", synth_cell.cell_id, SYNTH_START, t_long,
               tmp_path / "jl", log=lambda *_: None)
    short = {(r["evt"], r["ts_open"], r["tranche_id"]): r
             for r in read_journal(tmp_path / "js", synth_cell.cell_id)}
    long_ = {(r["evt"], r["ts_open"], r["tranche_id"]): r
             for r in read_journal(tmp_path / "jl", synth_cell.cell_id)}
    assert short, "short run wrote no rows"

    cutoff = t_short + "T00:00:00Z"   # --end is midnight UTC, inclusive
    for key, row in short.items():
        assert key in long_, f"short-run row missing from long run: {key}"
        a = {k: v for k, v in row.items() if k != "run_id"}
        b = {k: v for k, v in long_[key].items() if k != "run_id"}
        assert a == b, f"row differs between runs: {key}"

    for key, row in long_.items():
        if row["ts_open"] <= cutoff and key not in short:
            # only enrichment-buffered EXITs may appear late
            assert row["evt"] == "EXIT", \
                f"long run added a non-EXIT row inside the short window: {key}"
