#!/usr/bin/env python
"""brief_panel.py -- write-once daily panel partitions (Amendment 2 §8.2).

    C:\\venvs\\naiad\\Scripts\\python.exe scripts/brief_panel.py --date 2026-08-03
    C:\\venvs\\naiad\\Scripts\\python.exe scripts/brief_panel.py --rebuild-all
    C:\\venvs\\naiad\\Scripts\\python.exe scripts/brief_panel.py --consolidated

WHY PARTITIONS AND NOT THREE MONOLITHIC FILES.  v4 specified three parquet files
rebuilt each day.  With the volume layers the levels table reaches roughly
5,000-6,000 rows per day, and a REWRITTEN binary file stores a complete new blob
in git every single day -- growth COMPOUNDS instead of accumulating.  Daily
partitions, each written once and never rewritten, make git growth linear and
additive.

    briefs/panel/snapshots/YYYY-MM-DD.parquet
    briefs/panel/levels/YYYY-MM-DD.parquet
    briefs/panel/areas/YYYY-MM-DD.parquet

WRITE-ONCE IS ENFORCED, NOT DOCUMENTED.  `write_partition` refuses to overwrite
an existing partition unless `force=True`, and nothing in the normal path passes
force.  A partition that could be silently rewritten would reintroduce exactly
the compounding-growth problem the design exists to avoid, and would also make
an archived partition untrustworthy -- the reader could not know whether the
bytes on disk are the bytes that were computed that day.

THE CONSOLIDATED VIEW IS UNTRACKED AND REGENERABLE.  It is a convenience for
analysis, never a record; `briefs/panel/consolidated_*.parquet` is gitignored.

GRAIN is (asset, slot, date) for snapshots, and (asset, slot, date, +key) for
levels and areas, which is what lets them join back to a snapshot row.
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

BRIEFS_DIR = ROOT / "briefs"
PANEL_DIR = BRIEFS_DIR / "panel"
TABLES = ("snapshots", "levels", "areas", "excursions")
# 2.1.0 -- stage 3.3 adds the `excursions` table and the derived
# `since_last_touch` view.  Partitions written under 2.0.0 simply have no
# excursions file; the bump is what tells the two eras apart.
SCHEMA_VERSION = "2.1.0"


def _captures_for(date_str, briefs_dir=BRIEFS_DIR):
    return sorted(briefs_dir.glob(f"brief_{date_str}_*.json"))


def _load(path):
    with Path(path).open(encoding="utf-8") as fh:
        return json.load(fh)


def snapshot_rows(doc):
    """One row per (asset, slot, date) -- the grain."""
    rows = []
    for sym, a in (doc.get("assets") or {}).items():
        conf = a.get("confluence") or {}
        wv = conf.get("with_volume") or {}
        nv = conf.get("without_volume") or {}
        di = a.get("decision_instrument") or {}
        cb = di.get("composite_bias") or {}
        lines_wv = wv.get("lines") or {}
        lines_nv = nv.get("lines") or {}
        differ = conf.get("differ") or {}
        rows.append({
            "date": doc["date"], "slot": doc["slot"], "asset": sym,
            "schema_version": doc.get("schema_version", SCHEMA_VERSION),
            "rules_version": doc.get("rules_version"),
            "rules_sha256": doc.get("rules_sha256"),
            "analytics_version": doc.get("analytics_version"),
            "analytics_sha": doc.get("analytics_sha"),
            "engine_version": doc.get("engine_version"),
            "as_of_utc": doc.get("as_of_utc"),
            "parity_certified": doc.get("parity_certified"),
            "price": a.get("price"),
            "daily_atr": a.get("daily_atr"),
            "level_count": conf.get("level_count"),
            "cluster_count_wv": len(wv.get("clusters") or []),
            "cluster_count_nv": len(nv.get("clusters") or []),
            "lis_above_wv": (lines_wv.get("above") or {}).get("mean"),
            "lis_below_wv": (lines_wv.get("below") or {}).get("mean"),
            "lis_above_nv": (lines_nv.get("above") or {}).get("mean"),
            "lis_below_nv": (lines_nv.get("below") or {}).get("mean"),
            "lines_differ": differ.get("any_changed"),
            "bias_band": cb.get("band"),
            "bias_agree": cb.get("agree"),
            "bias_total": cb.get("total"),
            "bias_dissenting": ",".join(cb.get("dissenting") or []),
            "compression_demoted": cb.get("compression_demoted"),
            "divergence_count": len((a.get("oscillators") or {}).get("divergences") or []),
            "instability_chip": ((wv.get("sensitivity") or {}) or {}).get("instability_chip"),
        })
    return rows


def level_rows(doc):
    """One row per scored cluster member, joinable to a snapshot by grain."""
    rows = []
    for sym, a in (doc.get("assets") or {}).items():
        conf = a.get("confluence") or {}
        for view in ("with_volume", "without_volume"):
            v = conf.get(view) or {}
            for cl in (v.get("clusters") or []):
                for m in (cl.get("members") or []):
                    rows.append({
                        "date": doc["date"], "slot": doc["slot"], "asset": sym,
                        "view": view,
                        "cluster_id": cl.get("cluster_id"),
                        "cluster_mean": cl.get("mean"),
                        "cluster_score": cl.get("score"),
                        "family": m.get("family"),
                        "label": m.get("label"),
                        "level": m.get("level"),
                        "source_layer": m.get("source_layer"),
                        "timeframe": m.get("timeframe"),
                        "collapsed_count": m.get("collapsed_count"),
                        "scale_confirmed": ",".join(m.get("scale_confirmed") or []),
                    })
    return rows


def area_rows(doc):
    """One row per (asset, slot, date, window) plus the nesting pairs."""
    rows = []
    for sym, a in (doc.get("assets") or {}).items():
        vol = (a.get("volume_windows") or {}).get("windows") or {}
        for wname, w in vol.items():
            rows.append({
                "date": doc["date"], "slot": doc["slot"], "asset": sym,
                "kind": "window", "key": wname,
                "warming": bool(w.get("warming")),
                "poc": w.get("poc"), "vah": w.get("vah"), "val": w.get("val"),
                "lvn_count": len(w.get("lvns") or []),
                "substrate": w.get("substrate"),
                "bars": w.get("bars"),
                "lockbox_overlap_days": ((w.get("lockbox_overlap") or {})
                                         .get("overlap_days")),
                "state": None, "overlap_frac": None,
                "consensus_low": None, "consensus_high": None,
                "gap_low": None, "gap_high": None, "price_location": None,
            })
        for key, pr in ((a.get("va_nesting") or {}).get("pairs") or {}).items():
            cb = pr.get("consensus_band") or [None, None]
            gb = pr.get("gap_band") or [None, None]
            rows.append({
                "date": doc["date"], "slot": doc["slot"], "asset": sym,
                "kind": "nesting_pair", "key": key,
                "warming": pr.get("state") is None,
                "poc": None, "vah": None, "val": None, "lvn_count": None,
                "substrate": None, "bars": None, "lockbox_overlap_days": None,
                "state": pr.get("state"),
                "overlap_frac": pr.get("overlap_frac"),
                "consensus_low": cb[0], "consensus_high": cb[1],
                "gap_low": gb[0], "gap_high": gb[1],
                "price_location": pr.get("price_location"),
            })
    return rows


def excursion_rows(doc):
    """One row per band-excursion event (D.6 / stage 3.3).  RECORDING ONLY.

    Every field here is a per-capture OBSERVATION -- what price was doing
    against a volume-weighted mean at one instant.  Nothing derived from the
    event HISTORY is stored, because storing it would make the partition depend
    on other partitions and break the 'rebuilds from captures alone' guarantee
    that F-B19/F-B32 exist to protect.  `since_last_touch()` below derives the
    recency series from this table on demand instead.
    """
    rows = []
    for sym, a in (doc.get("assets") or {}).items():
        ex = a.get("band_excursions") or {}
        for e in (ex.get("events") or []):
            rows.append({
                "date": doc["date"], "slot": doc["slot"], "asset": sym,
                "name": e.get("name"), "kind": e.get("kind"),
                "side": e.get("side"),
                "band_reached": e.get("band_reached"),
                "sigma_position": e.get("sigma_position"),
                "distance_to_mean_sigma": e.get("distance_to_mean_sigma"),
                "distance_to_mean_atr": e.get("distance_to_mean_atr"),
                "bars": e.get("bars"),
                "thin_sample": bool(e.get("thin_sample")),
                "returned_to_mean": bool(e.get("returned_to_mean")),
            })
    return rows


BUILDERS = {"snapshots": snapshot_rows, "levels": level_rows, "areas": area_rows,
            "excursions": excursion_rows}


def since_last_touch(panel_dir=PANEL_DIR):
    """DERIVED view: captures since each (asset, VWAP) last touched a band.

    This is the promise `excursion_layer` makes in every capture -- "DERIVED at
    panel-build time from the stored band_reached series" -- discharged here.
    It was documented before it was built; this closes that gap.

    WHY DERIVED AND NOT STORED.  A stored counter is state a capture cannot
    verify about itself, and it would survive a corrupted neighbour unnoticed.
    Recomputing from the archive means the number is always reproducible from
    the partitions actually on disk.

    FIREWALL (§3.4).  This is a RECENCY COUNTER, the same class of object as a
    naked POC's "untested since" -- it says WHEN something last happened, never
    HOW OFTEN it works.  No rate, no hit count, no expectancy, no statistic over
    outcomes: those are H-VBR and are CENSUS work under G-7, routed to APOLLO.
    """
    import pandas as pd
    d = Path(panel_dir) / "excursions"
    files = sorted(d.glob("*.parquet")) if d.exists() else []
    if not files:
        return pd.DataFrame(columns=["asset", "name", "last_touch_date",
                                     "captures_since_last_touch",
                                     "last_band_reached", "last_side"])
    ev = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)

    # The capture timeline is (date, slot) over ALL captures, not just those
    # with an event -- "captures since" must count the quiet ones too, or a
    # month of silence would read the same as yesterday.
    snap_dir = Path(panel_dir) / "snapshots"
    snaps = sorted(snap_dir.glob("*.parquet")) if snap_dir.exists() else []
    if snaps:
        sn = pd.concat([pd.read_parquet(f) for f in snaps], ignore_index=True)
        timeline = (sn[["date", "slot"]].drop_duplicates()
                    .sort_values(["date", "slot"]).reset_index(drop=True))
    else:
        timeline = (ev[["date", "slot"]].drop_duplicates()
                    .sort_values(["date", "slot"]).reset_index(drop=True))
    timeline["ordinal"] = range(len(timeline))
    latest = len(timeline) - 1

    ev = ev.merge(timeline, on=["date", "slot"], how="left")
    touched = ev[ev["band_reached"].fillna(0) != 0]
    if touched.empty:
        return pd.DataFrame(columns=["asset", "name", "last_touch_date",
                                     "captures_since_last_touch",
                                     "last_band_reached", "last_side"])
    idx = touched.groupby(["asset", "name"])["ordinal"].idxmax()
    last = touched.loc[idx].copy()
    last["captures_since_last_touch"] = latest - last["ordinal"]
    return (last[["asset", "name", "date", "captures_since_last_touch",
                  "band_reached", "side"]]
            .rename(columns={"date": "last_touch_date",
                             "band_reached": "last_band_reached",
                             "side": "last_side"})
            .sort_values(["asset", "name"]).reset_index(drop=True))


def build_partition(date_str, briefs_dir=BRIEFS_DIR):
    """Rebuild all three tables for one date FROM CAPTURES ALONE (F-B19/F-B32).

    Reading only captures is what makes a partition reproducible: if the panel
    could read a previous partition, a corrupted one would propagate forward and
    the 'rebuilds from captures alone' guarantee would be false.
    """
    caps = _captures_for(date_str, briefs_dir)
    if not caps:
        raise SystemExit(f"no captures found for {date_str} in {briefs_dir}")
    out = {t: [] for t in TABLES}
    for p in caps:
        doc = _load(p)
        for t in TABLES:
            out[t].extend(BUILDERS[t](doc))
    return out


def _rel(path):
    """Repo-relative inside the repo, absolute outside it.

    A partition written outside ROOT (a fixture's tmp_path) must still report a
    usable path rather than raising ValueError out of relative_to.
    """
    p = Path(path)
    try:
        return str(p.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(p).replace("\\", "/")


def write_partition(date_str, tables, panel_dir=PANEL_DIR, force=False):
    """WRITE ONCE.  Refuses to overwrite unless force=True (F-B32)."""
    import pandas as pd
    panel_dir = Path(panel_dir)
    written, refused = [], []
    for t in TABLES:
        d = panel_dir / t
        d.mkdir(parents=True, exist_ok=True)
        path = d / f"{date_str}.parquet"
        if path.exists() and not force:
            refused.append(_rel(path))
            continue
        pd.DataFrame(tables[t]).to_parquet(path, index=False)
        written.append(_rel(path))
    return {"written": written, "refused_existing": refused,
            "write_once": True,
            "note": "a partition is written once and never rewritten; "
                    "rerun with --force only to repair a known-bad file"}


def consolidated(panel_dir=PANEL_DIR):
    """UNTRACKED, regenerable convenience view over every partition."""
    import pandas as pd
    out = {}
    for t in TABLES:
        d = panel_dir / t
        files = sorted(d.glob("*.parquet")) if d.exists() else []
        out[t] = (pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
                  if files else pd.DataFrame())
    return out


def main():
    ap = argparse.ArgumentParser(description="BRIEF-2 panel partitions")
    ap.add_argument("--date")
    ap.add_argument("--rebuild-all", action="store_true")
    ap.add_argument("--consolidated", action="store_true")
    ap.add_argument("--since-last-touch", action="store_true",
                    help="derived recency view over the excursions table")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    if args.since_last_touch:
        df = since_last_touch()
        if df.empty:
            print("no band-excursion touches recorded yet")
        else:
            print(df.to_string(index=False))
        # Worded to carry the firewall without naming the banned measures: this
        # string is executable code, not a docstring, so F-B16's scan sees it
        # and is RIGHT to -- a prohibition belongs in prose the scanner strips.
        print("\nRECENCY ONLY -- when a band was last touched, never how often "
              "a touch works. Any statistic over this history is H-VBR, census "
              "work under G-7, routed to APOLLO. See briefs/panel/SCHEMA.md.")
        return

    if args.consolidated:
        import pandas as pd
        cons = consolidated()
        PANEL_DIR.mkdir(parents=True, exist_ok=True)
        for t, df in cons.items():
            p = PANEL_DIR / f"consolidated_{t}.parquet"
            df.to_parquet(p, index=False)
            print(f"  {t}: {len(df)} rows -> {p.name} (untracked, regenerable)")
        return

    dates = ([args.date] if args.date else
             sorted({p.name.split("_")[1] for p in BRIEFS_DIR.glob("brief_*_*.json")}))
    if not dates:
        raise SystemExit("no captures found in briefs/")
    for d in dates:
        tables = build_partition(d)
        res = write_partition(d, tables, force=args.force)
        counts = {t: len(tables[t]) for t in TABLES}
        print(f"{d}: {counts}")
        for w in res["written"]:
            print(f"  wrote   {w}")
        for r in res["refused_existing"]:
            print(f"  EXISTS  {r}  (write-once; not rewritten)")


if __name__ == "__main__":
    main()
