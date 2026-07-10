"""F3 — stops never loosen (invariant 5), property-tested.

The campaign stop may only tighten while it exists; it clears (NaN) only on
campaign death or an opposite arming. Checked on the synthetic replay and on
randomized OHLC inputs.
"""

import numpy as np

from conftest import resample, synth_1m

from engine.cells import MTF_SET, make_cell
from engine.config import load_config
from engine.signals import compute_signals


def _assert_ratchet(sig):
    sl, ss = sig.stop_long, sig.stop_short
    for i in range(1, len(sl)):
        if not np.isnan(sl[i - 1]) and not np.isnan(sl[i]):
            assert sl[i] >= sl[i - 1] - 1e-12, f"long stop loosened at bar {i}"
        if not np.isnan(ss[i - 1]) and not np.isnan(ss[i]):
            assert ss[i] <= ss[i - 1] + 1e-12, f"short stop loosened at bar {i}"


def _run(seed: int):
    cell = make_cell("BTCUSDT", "intraday")
    p = load_config("naiad_v0")["signal"]
    df1m = synth_1m(seed)
    frames = {iv: resample(df1m, iv) for iv in ["1m", "5m", "1h", "4h", "12h"]}
    return compute_signals(cell, p, frames["1m"], frames["1h"],
                           {tf: frames[tf] for tf in MTF_SET},
                           v_births_provisional=True)


def test_ratchet_property_randomized():
    for seed in (7, 11, 23, 41):   # seeded => deterministic, still adversarial
        sig = _run(seed)
        assert (sig.dir != 0).any(), f"seed {seed}: no campaigns at all"
        _assert_ratchet(sig)


def test_ratchet_swing_mandate():
    cell = make_cell("BTCUSDT", "swing")
    p = load_config("naiad_v0")["signal"]
    df1m = synth_1m(13)
    frames = {iv: resample(df1m, iv) for iv in ["5m", "1h", "4h", "12h"]}
    sig = compute_signals(cell, p, frames["5m"], frames["4h"],
                          {tf: frames[tf] for tf in MTF_SET},
                          v_births_provisional=True)
    _assert_ratchet(sig)
