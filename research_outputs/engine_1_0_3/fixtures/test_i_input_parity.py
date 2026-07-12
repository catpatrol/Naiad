"""I (Engine 1.0.3) — INPUT PARITY. Drift can no longer recur silently.

(a) Every live engine signal constant (both configs, all mandates) equals the
    deployed Pine input default, asserted against the committed manifest
    extracted from pine/SS_Cascade_v11.0.2.pine.
(b) Behavioral pins at the three divergence sites of the 3C break: at
    zone_memory=3 the engine fires NO PRIME (May 23 16:20), NO grade-C
    (May 27 12:45), NO CONFIRMs (Jun 23 17:00/17:45/20:45). These read the
    committed regenerated parity journal (skipped until it exists).

Charter-ratified NON-input divergences are intentionally NOT asserted here:
the per-mandate governor/exec/align TFs (charter §4) and v_births_provisional
(charter §3.2 — a logic policy; v11_faithful=false matches the Pine literal,
naiad_v0=true is the charter override).
"""

import json
from pathlib import Path

import pytest
import yaml

from engine.cells import MANDATES, make_cell
from engine.config import load_config

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = yaml.safe_load(
    (ROOT / "fixtures" / "pine_defaults_manifest.yaml").read_text(encoding="utf-8"))
PARITY_JOURNAL = ROOT / "research_outputs" / "parity" / "journal" / "BTCUSDT_swing"


# ── (a) input-parity conformance ─────────────────────────────────────────────

@pytest.mark.parametrize("config_id", ["v11_faithful", "naiad_v0"])
def test_signal_constants_match_pine_defaults(config_id):
    sig = load_config(config_id)["signal"]
    for key, spec in MANIFEST["signal"].items():
        assert sig[key] == spec["default"], (
            f"{config_id}.signal.{key} = {sig[key]!r} but Pine default "
            f"({spec['pine']}, {MANIFEST['source_file']}:{spec['line']}) "
            f"= {spec['default']!r} — UNRATIFIED INPUT DRIFT")


@pytest.mark.parametrize("mandate", list(MANDATES))
def test_zone_memory_matches_pine_default(mandate):
    spec = MANIFEST["zone_memory"]
    zm = make_cell("BTCUSDT", mandate).zone_memory
    assert zm == spec["default"], (
        f"{mandate} zone_memory = {zm} but Pine default "
        f"({spec['pine']}, {MANIFEST['source_file']}:{spec['line']}) "
        f"= {spec['default']} — the 3C break root cause")


# ── (b) behavioral pins at zone_memory=3 (committed parity journal) ───────────

_skip = pytest.mark.skipif(
    not PARITY_JOURNAL.exists(),
    reason="parity journal not regenerated yet (scripts/parity_pack.py)")


def _rows():
    out = []
    for f in sorted(PARITY_JOURNAL.glob("*.jsonl")):
        for ln in f.read_text(encoding="utf-8").splitlines():
            if ln.strip():
                out.append(json.loads(ln))
    return out


@_skip
def test_no_prime_may23_1620():
    hits = [r for r in _rows()
            if r["evt"] == "PRIME" and r["ts_open"] == "2026-05-23T16:20:00Z"]
    assert not hits, f"zone_memory=3 must fire NO PRIME at 2026-05-23 16:20; found {hits}"


@_skip
def test_no_gradeC_may27_1245():
    hits = [r for r in _rows()
            if r["evt"] == "CONFIRM" and r["grade"] == "C"
            and r["ts_open"] == "2026-05-27T12:45:00Z"]
    assert not hits, f"zone_memory=3 must fire NO grade-C at 2026-05-27 12:45; found {hits}"


@_skip
def test_no_confirms_jun23_break():
    ts = {"2026-06-23T17:00:00Z", "2026-06-23T17:45:00Z", "2026-06-23T20:45:00Z"}
    hits = [r for r in _rows() if r["evt"] == "CONFIRM" and r["ts_open"] in ts]
    assert not hits, f"zone_memory=3 must fire NO CONFIRM at Jun-23 17:00/17:45/20:45; found {hits}"
