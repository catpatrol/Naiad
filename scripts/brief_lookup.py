#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Search the daily-brief archive (A1.5).

Reads research_outputs/brief/brief_index.jsonl — one line per date — and prints
matching lines plus the full paths of that day's JSON and HTML snapshots.

FIREWALL: this tool contains NO outcome joins of any kind (A1.1 clause 4). It
filters and locates archived state; it never scores how a flagged setup
subsequently performed, and it never reads a trade journal. Adding such a join
here would be a governance act, not a patch.

    .venv/Scripts/python.exe scripts/brief_lookup.py --from 2026-07-01 --state ZONE_ACTIVE
    .venv/Scripts/python.exe scripts/brief_lookup.py --asset SOLUSDT --flag funding_p90_plus
    .venv/Scripts/python.exe scripts/brief_lookup.py --verdict Long --text divergence
"""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INDEX = ROOT / "research_outputs" / "brief" / "brief_index.jsonl"


def load_index(path):
    if not path.exists():
        return []
    out = []
    for raw in path.read_bytes().decode("utf-8").splitlines():
        if not raw.strip():
            continue
        try:
            out.append(json.loads(raw))
        except json.JSONDecodeError:
            continue
    return sorted(out, key=lambda l: l.get("date", ""))


def asset_blobs(line, asset=None):
    per = line.get("per_asset") or {}
    if asset:
        return {asset: per[asset]} if asset in per else {}
    return per


def keep(line, args, raw):
    if args.date and line.get("date") != args.date:
        return False
    if args.date_from and line.get("date", "") < args.date_from:
        return False
    if args.date_to and line.get("date", "") > args.date_to:
        return False
    blobs = asset_blobs(line, args.asset)
    if args.asset and not blobs:
        return False
    if args.state:
        states = set()
        for b in blobs.values():
            states.add(b.get("radar_best_state"))
            states.update((b.get("radar_states") or {}).values())
        if args.state not in states:
            return False
    if args.flag:
        if not any(args.flag in (b.get("flags_true") or []) for b in blobs.values()):
            return False
    if args.verdict:
        vs = {b.get("daily_verdict") for b in blobs.values()} | \
             {b.get("weekly_verdict") for b in blobs.values()}
        if args.verdict not in vs:
            return False
    if args.text and args.text.lower() not in raw.lower():
        return False
    return True


def main():
    ap = argparse.ArgumentParser(description="Search the daily-brief archive")
    ap.add_argument("--date", help="exact UTC date, YYYY-MM-DD")
    ap.add_argument("--from", dest="date_from", help="inclusive lower bound")
    ap.add_argument("--to", dest="date_to", help="inclusive upper bound")
    ap.add_argument("--asset", help="restrict to one symbol, e.g. SOLUSDT")
    ap.add_argument("--state", help="radar state, e.g. ZONE_ACTIVE")
    ap.add_argument("--flag", help="confluence flag name, e.g. funding_p90_plus")
    ap.add_argument("--verdict", help="bias verdict, e.g. Long")
    ap.add_argument("--text", help="free-text substring over the index line")
    ap.add_argument("--index", default=str(DEFAULT_INDEX), help="index path")
    ap.add_argument("--full", action="store_true", help="print the whole line")
    args = ap.parse_args()

    index_path = Path(args.index)
    lines = load_index(index_path)
    if not lines:
        print(f"no archive index at {index_path}")
        return 1

    hits = [l for l in lines
            if keep(l, args, json.dumps(l, sort_keys=True, ensure_ascii=True))]
    print(f"{len(hits)} of {len(lines)} archived days match  ({index_path})")
    for l in hits:
        base = index_path.parent
        jp = base / f"brief_{l['date']}.json"
        hp = base / f"brief_{l['date']}.html"
        print(f"\n{l['date']}  rules v{l.get('rules_version')}  "
              f"json_sha256 {str(l.get('json_sha256'))[:12]}  "
              f"generated {l.get('generated_utc')}")
        print(f"  json: {jp}{'' if jp.exists() else '   (snapshot absent)'}")
        print(f"  html: {hp}{'' if hp.exists() else '   (snapshot absent)'}")
        if args.full:
            print("  " + json.dumps(l, indent=1, sort_keys=True).replace("\n", "\n  "))
            continue
        for sym, b in asset_blobs(l, args.asset).items():
            states = b.get("radar_states") or {}
            flags = b.get("flags_true") or []
            print(f"  {sym:<14} daily {str(b.get('daily_verdict')):<14}"
                  f"weekly {str(b.get('weekly_verdict')):<14}"
                  f"radar {'/'.join(f'{k}:{v}' for k, v in states.items())}"
                  f"  poi {b.get('poi_count')}"
                  + (f"  flags {','.join(flags)}" if flags else ""))
        if l.get("staleness"):
            print(f"  staleness: {len(l['staleness'])} asset(s) with stale inputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
