#!/usr/bin/env python
"""CEN-0(a) -- PANEL READINESS INVENTORY for CENSUS-2A.

The contract's CEN-0(a): "Panel readiness inventory (estate, read-only;
delivered in paste #1)."  This is that inventory.

WHAT IT ANSWERS
  For every panel asset {BTC, ETH, SOL, NEAR, ZEC}USDT and annex {JTO, TAO},
  per timeframe: how many bars exist, over what span, split at the evidence
  wall (2024-07-01), with gap detection and the per-EMA warm state.  Plus the
  CEN-0(b) PAXG question, answered honestly: absent.

READ-ONLY.  Touches no estate file, fetches nothing, writes only its own two
artifacts to D:.  A readiness inventory that mutates the thing it inventories
is not an inventory.

GAPS
  A "gap" here is a missing bar in an otherwise regular grid -- consecutive
  open_times differing by more than one interval.  This matters more than it
  looks: a census that anchors outcome horizons in BAR counts silently
  shortens every horizon that spans a gap, and the shortening is invisible in
  any summary statistic.  So gaps are counted, sized, and located.

USAGE
  python scripts/cen0_inventory.py
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import census_build as CB  # noqa: E402
from drive_wait import wait_for_drive  # noqa: E402
from mc2_program import (EMAS, PANEL, ANNEX, KLINES, D_ROOT, iso,  # noqa: E402
                         warmup_bars, _sha, stage_preflight)

OUT = D_ROOT
CEIL_MS = CB.CEIL_MS
# census_build's grid starts at 5m (its exec TF); the cache also holds 1m, which
# the contract's I4 gives its own reduced EMA set, so the inventory must cover it.
TF_MS = {**CB.TF_MS, "1m": 60_000}
CACHE_TFS = ["1m", "5m", "15m", "1h", "4h", "12h"]
DERIVED = {"30m": "15m (resampled, s1 algorithm)", "1d": "1h (resampled)"}


def inventory_one(sym: str, tf: str) -> dict | None:
    p = KLINES / f"{sym}_{tf}.parquet"
    if not p.exists():
        return {"asset": sym, "tf": tf, "present": False, "n_bars": 0,
                "n_evidence": 0, "n_live": 0, "first": None, "last": None,
                "n_gaps": 0, "missing_bars": 0, "largest_gap_bars": 0,
                "dupes": 0, "monotonic": None}
    df = pd.read_parquet(p, columns=["open_time"])
    o = np.sort(df["open_time"].to_numpy(np.int64))
    step = TF_MS[tf]
    d = np.diff(o)
    gaps = d[d > step]
    return {
        "asset": sym, "tf": tf, "present": True, "n_bars": int(len(o)),
        "n_evidence": int((o < CEIL_MS).sum()),
        "n_live": int((o >= CEIL_MS).sum()),
        "first": iso(int(o[0])), "last": iso(int(o[-1])),
        "n_gaps": int(len(gaps)),
        "missing_bars": int((gaps // step - 1).sum()) if len(gaps) else 0,
        "largest_gap_bars": int(gaps.max() // step) if len(gaps) else 0,
        "dupes": int(len(o) - len(np.unique(o))),
        "monotonic": bool((np.diff(df["open_time"].to_numpy(np.int64)) > 0).all()),
    }


def main() -> int:
    print("CEN-0(a) -- panel readiness inventory")
    pre = stage_preflight()

    rows = []
    for sym in PANEL + ANNEX + ["PAXGUSDT"]:
        for tf in CACHE_TFS:
            r = inventory_one(sym, tf)
            if r:
                rows.append(r)
    inv = pd.DataFrame(rows).sort_values(["asset", "tf"]).reset_index(drop=True)

    print(f"\n{'asset':10}{'tf':>5}{'bars':>10}{'evidence':>10}{'live':>9}"
          f"{'gaps':>6}{'miss':>6}  {'first':16}{'last':16}")
    for r in inv.itertuples(index=False):
        if not r.present:
            print(f"{r.asset:10}{r.tf:>5}{'-- ABSENT --':>25}")
            continue
        print(f"{r.asset:10}{r.tf:>5}{r.n_bars:>10}{r.n_evidence:>10}{r.n_live:>9}"
              f"{r.n_gaps:>6}{r.missing_bars:>6}  {r.first:16}{r.last:16}")

    # --- readiness verdict per asset, against the contract's own requirements
    verdict = []
    for sym in PANEL + ANNEX + ["PAXGUSDT"]:
        g = inv[inv.asset == sym]
        present = g[g.present]
        if present.empty:
            verdict.append({"asset": sym, "role": "panel" if sym in PANEL else
                            ("annex" if sym in ANNEX else "requested"),
                            "state": "ABSENT", "note": "no series in the cache"})
            continue
        ev4 = int(g[(g.tf == "4h")].n_evidence.iloc[0]) if (g.tf == "4h").any() else 0
        warm500_4h = ev4 - warmup_bars(500)
        # >=2y of evidence-era 4h bars is the contract's panel-eligibility rule
        two_years_4h = 2 * 365 * 6
        verdict.append({
            "asset": sym,
            "role": "panel" if sym in PANEL else ("annex" if sym in ANNEX else "requested"),
            "state": "READY" if ev4 >= two_years_4h else "SHORT-HISTORY",
            "evidence_4h_bars": ev4,
            "evidence_years_4h": round(ev4 / (365 * 6), 2),
            "ema500_4h_warm_bars": int(max(warm500_4h, 0)),
            "ema500_4h": "WARM" if warm500_4h > 0 else "NEVER",
            "tfs_present": int(present.shape[0]),
            "total_gaps": int(present.n_gaps.sum()),
            "note": "",
        })
    ver = pd.DataFrame(verdict)
    print("\nREADINESS")
    for r in ver.itertuples(index=False):
        print(f"  {r.asset:10} {r.role:9} {r.state:14} "
              f"{getattr(r, 'evidence_years_4h', '')}y evidence-era 4h, "
              f"ema500_4h={getattr(r, 'ema500_4h', 'n/a')}")

    # --- CEN-0(b): PAXG, answered rather than assumed
    paxg = inv[(inv.asset == "PAXGUSDT")]
    paxg_present = bool(paxg.present.any())
    cen0b = {
        "asset": "PAXGUSDT",
        "present_in_cache": paxg_present,
        "classification": None if not paxg_present else "pending",
        "rule": ("contract CEN-0(b): >=2y evidence-era -> panel-eligible; "
                 "else annex"),
        "state": "BLOCKED -- requires a network fetch, which paste #1 was "
                 "scoped to exclude by operator decision 2026-08-12",
        "engine_note": ("PAXGUSDT is absent from engine/cells.py SYMBOLS; the "
                        "contract's I10 forbids an engine change, so the fetch "
                        "must pass the symbol explicitly and registration is a "
                        "separate queue item"),
    }
    print(f"\nCEN-0(b) PAXG: {'present' if paxg_present else 'ABSENT'} -- {cen0b['state']}")

    OUT.mkdir(parents=True, exist_ok=True)
    p_inv = OUT / "cen0_panel_inventory.parquet"
    inv.to_parquet(p_inv, index=False)
    p_ver = OUT / "cen0_readiness.parquet"
    ver.to_parquet(p_ver, index=False)
    man = {
        "module": "CEN-0(a)", "generated_utc":
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "class": "EVIDENCE -- inventory of the estate as it stands",
        "ceil_ms": CEIL_MS, "ceil_iso": iso(CEIL_MS),
        "cache_root": str(KLINES),
        "native_tfs": CACHE_TFS, "derived_tfs": DERIVED,
        "preflight": pre,
        "cen0b_paxg": cen0b,
        "artifacts": {
            "cen0_panel_inventory": {"path": str(p_inv), "rows": int(len(inv)),
                                     "sha256": _sha(p_inv)},
            "cen0_readiness": {"path": str(p_ver), "rows": int(len(ver)),
                               "sha256": _sha(p_ver)},
        },
    }
    p_man = OUT / "cen0_manifest.json"
    p_man.write_text(json.dumps(man, indent=2, default=str), encoding="utf-8")
    print(f"\nwrote {p_inv}\n      {p_ver}\n      {p_man}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
