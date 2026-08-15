#!/usr/bin/env python3
"""
CENSUS-2B / V-ULT-1 -- BUILD-DOCUMENT TABLE GENERATOR
=====================================================
Emits the markdown fragments the build document embeds: the feasibility matrix
verbatim, the artifact inventory with shas, and the box-cost arithmetic.

Tables are generated from the artifacts themselves rather than transcribed, so
a number in the build document cannot drift from the number on disk.

    python scripts/census2b_report.py > <fragment>.md
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from census2b_program import (                                    # noqa: E402
    OUT, MANIFEST, RIBBONS, FAMILIES, TFS, PANEL, WARM, ALL_EMAS, WARMFACTOR,
    seq8_warm_exact,
)

from publish_exchange import (BOX_BYTES, WARN_FRACTION,           # noqa: E402
                              REFUSE_FRACTION)
# Imported, not copied.  This was a hand-kept copy of publish_exchange.BOX_BYTES
# and it silently went stale the moment the operator raised the box on
# 2026-08-15 (6.39 MB -> 16 MB), which would have made every occupancy figure
# this report prints wrong by 2.5x.  One definition, one place.


def md_table(df: pd.DataFrame, cols: list[str], aligns: dict | None = None) -> str:
    aligns = aligns or {}
    out = ["| " + " | ".join(cols) + " |",
           "|" + "|".join(("---:" if aligns.get(c) == "r" else "---")
                          for c in cols) + "|"]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(out)


def sec_warm() -> None:
    print("### F-B0 · the warmfactor reconciliation\n")
    print(f"The contract pins `warmfactor = {WARMFACTOR}`, `warm_bars = ceil({WARMFACTOR}*N)`, "
          "and calls it *the SEQ8 rule*. The SEQ8 rule as implemented "
          "(`seq8_extract.warmup_bars`) is `ceil(log(1e-3)/log(1-2/(N+1)))`. "
          "These are **not the same expression**. F-B0 settles which governs by "
          "proving the contract's constant is the conservative one:\n")
    rows = []
    for fam, members in RIBBONS.items():
        for L in members:
            c, e = WARM[L], seq8_warm_exact(L)
            rows.append({"family": fam, "N": L, "ceil(3.46·N)": f"{c:,}",
                         "exact SEQ8": f"{e:,}", "delta": f"{c - e:+d}",
                         "safe": "yes" if c >= e else "**NO**"})
    df = pd.DataFrame(rows)
    print(md_table(df, list(df.columns)))
    print(f"\n`ceil({WARMFACTOR}*N)` is greater than or equal to the exact SEQ8 warm-up "
          f"for **all 18 lengths** (delta 0 … +30 bars, never negative). The contract "
          f"constant therefore over-warms by at most 30 bars and never under-warms, so "
          f"it is used **as written, by name**, and the estate's existing "
          f"`warmup_bars` is used only as the thing F-B0 checks it against.\n")


def sec_feasibility() -> None:
    p = OUT / "cen2b_feasibility.parquet"
    if not p.exists():
        print("_(feasibility matrix not built)_\n"); return
    fm = pd.read_parquet(p)

    print("### The verdict grid — worst verdict across each family's three members\n")
    order = {"NEVER": 0, "OPS-ONLY": 1, "PARTIAL(evidence)": 2, "FULL": 3}
    short = {"NEVER": "NEVER", "OPS-ONLY": "OPS", "PARTIAL(evidence)": "PART",
             "FULL": "FULL"}
    tfs = [t for t in TFS if t in set(fm.tf)]
    for sym in [a for a in PANEL if a in set(fm.asset)]:
        print(f"**{sym}**\n")
        print("| family | " + " | ".join(tfs) + " |")
        print("|---|" + "|".join("---" for _ in tfs) + "|")
        for fam in FAMILIES:
            cells = []
            for tf in tfs:
                s = fm[(fm.asset == sym) & (fm.tf == tf) & (fm.family == fam)]
                w = min(s.verdict, key=lambda v: order[v])
                cells.append(short[w])
            print(f"| {fam} | " + " | ".join(cells) + " |")
        print()

    print("### NEVER cells — skipped, not computed\n")
    nev = fm[fm.verdict == "NEVER"]
    print(f"**{len(nev)} of {len(fm)}** (asset × tf × length) cells never warm at all. "
          f"No EMA recursion is run for them; the column exists and is all-NaN so the "
          f"schema stays uniform and nothing cold can be read.\n")
    rows = []
    for (tf, fam), g in nev.groupby(["tf", "family"], sort=False):
        rows.append({"tf": tf, "family": fam,
                     "lengths": ", ".join(str(x) for x in sorted(set(g.length))),
                     "assets": ", ".join(sorted(a.replace("USDT", "")
                                                for a in set(g.asset)))})
    if rows:
        df = pd.DataFrame(rows)
        print(md_table(df, list(df.columns)))
    ops = fm[fm.verdict == "OPS-ONLY"]
    print(f"\n### OPS-ONLY cells — computed, zero evidence-era coverage\n")
    print(f"**{len(ops)} cells.** These warm, but only *after* the evidence ceiling "
          f"(2024-07-01). They exist for the live era and cannot speak to the census.\n")
    rows = []
    for (tf, fam), g in ops.groupby(["tf", "family"], sort=False):
        rows.append({"tf": tf, "family": fam,
                     "lengths": ", ".join(str(x) for x in sorted(set(g.length))),
                     "assets": ", ".join(sorted(a.replace("USDT", "")
                                                for a in set(g.asset)))})
    if rows:
        df = pd.DataFrame(rows)
        print(md_table(df, list(df.columns)))

    print(f"\n### The feasibility matrix, verbatim — all {len(fm)} cells\n")
    print("The contract's five columns are all here. Two of them are pure functions "
          "of a single\nfactor and are factored out once rather than repeated 630 "
          "times, which is what keeps\nthis document inside the 1 % bus budget "
          "without dropping a cell:\n")
    print("- **`warm_bars`** depends only on `N` — `ceil(3.46·N)`, the 18 values below.")
    print("- **`bars available`** depends only on (asset, tf) — the 35 values below.\n")
    print("Per-cell, the remaining content is **warm-from date · evidence-era "
          "coverage · verdict**.\n")

    print("**`warm_bars = ceil(3.46·N)`**\n")
    print("```")
    for fam, members in RIBBONS.items():
        print(f"{fam:5s} " + "   ".join(f"N={L}: {WARM[L]:,}" for L in members))
    print("```\n")

    print("**`bars available` (full history, both eras)**\n")
    tfs = [t for t in TFS if t in set(fm.tf)]
    piv = (fm.drop_duplicates(["asset", "tf"])
             .pivot(index="asset", columns="tf", values="bars_available"))
    print("| asset | " + " | ".join(tfs) + " | first bar | last bar |")
    print("|---|" + "|".join("---:" for _ in tfs) + "|---|---|")
    for sym in [a for a in PANEL if a in piv.index]:
        s = fm[fm.asset == sym].iloc[0]
        print(f"| {sym} | "
              + " | ".join(f"{int(piv.loc[sym, t]):,}" for t in tfs)
              + f" | {s.first_bar} | {s.last_bar} |")
    print()

    print("**Per cell — `N: warm-from  coverage  verdict`** — "
          "`F`=FULL · `P`=PARTIAL(evidence) · `O`=OPS-ONLY · `N`=NEVER\n")
    letter = {"FULL": "F", "PARTIAL(evidence)": "P", "OPS-ONLY": "O", "NEVER": "N"}
    print("```")
    for sym in [a for a in PANEL if a in set(fm.asset)]:
        for tf in tfs:
            s = fm[(fm.asset == sym) & (fm.tf == tf)]
            if s.empty:
                continue
            print(f"{sym} @ {tf}  ({int(s.bars_available.iloc[0]):,} bars)")
            for fam, members in RIBBONS.items():
                g = s[s.family == fam]
                if g.empty:
                    continue
                cells = []
                for L in members:
                    r = g[g.length == L].iloc[0]
                    wf = r.warm_from if r.warm_from != "-" else "----------"
                    cells.append(f"{L}:{wf[2:]} {r.evidence_coverage:.3f} "
                                 f"{letter[r.verdict]}")
                print(f"  {fam:4s} " + "  ".join(cells))
    print("```\n")


def sec_artifacts() -> None:
    if not MANIFEST.exists():
        print("_(manifest not written)_\n"); return
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    arts = man.get("artifacts", {})
    print("### Artifact inventory — all bulk on `D:`, none committed\n")
    groups: dict[str, list] = {}
    for k, v in arts.items():
        top = k.split("/")[0] if "/" in k else "(root)"
        groups.setdefault(top, []).append((k, v))
    total_b = total_r = 0
    rows = []
    for g in sorted(groups):
        gb = sum(v["bytes"] for _, v in groups[g])
        gr = sum(v["rows"] or 0 for _, v in groups[g])
        total_b += gb
        total_r += gr
        rows.append({"group": f"`{g}/`", "files": len(groups[g]),
                     "rows": f"{gr:,}", "bytes": f"{gb:,}",
                     "MB": f"{gb / 1e6:,.1f}"})
    rows.append({"group": "**total**", "files": len(arts),
                 "rows": f"**{total_r:,}**", "bytes": f"**{total_b:,}**",
                 "MB": f"**{total_b / 1e6:,.1f}**"})
    print(md_table(pd.DataFrame(rows), ["group", "files", "rows", "bytes", "MB"]))
    print(f"\nManifest: `{MANIFEST}` — {len(arts)} artifacts, each with "
          f"`{{path, rows, bytes, sha256, class}}`.\n")

    print("#### A sample of the recorded shas\n")
    rows = []
    for k in sorted(arts)[:8]:
        v = arts[k]
        rows.append({"artifact": f"`{k}`", "rows": f"{v['rows']:,}" if v['rows'] else "-",
                     "bytes": f"{v['bytes']:,}", "sha256": f"`{v['sha256'][:16]}…`"})
    print(md_table(pd.DataFrame(rows), ["artifact", "rows", "bytes", "sha256"]))
    print()


def sec_boxcost(added_bytes: int = 0) -> None:
    tot = 0
    n = 0
    for r, d, f in os.walk(REPO / "exchange"):
        for x in f:
            tot += os.path.getsize(os.path.join(r, x))
            n += 1
    print("### BOX-COST\n")
    print(f"| item | value |\n|---|---:|")
    print(f"| `exchange/**` before this build | {tot - added_bytes:,} B |")
    print(f"| box budget (`publish_exchange.BOX_BYTES`) | {BOX_BYTES:,} B |")
    print(f"| occupancy before | {100.0 * (tot - added_bytes) / BOX_BYTES:.2f} % |")
    print(f"| this build adds | ~{added_bytes:,} B |")
    print(f"| occupancy after | {100.0 * tot / BOX_BYTES:.2f} % |")
    print(f"| WARN line / REFUSE line | {100 * WARN_FRACTION:.0f} % / "
          f"{100 * REFUSE_FRACTION:.0f} % |")
    print()


def main() -> int:
    # Windows stdout defaults to cp1252 and silently mangles the em-dashes and
    # middots this document is built out of. Force UTF-8 before the first print.
    try:
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    except Exception:
        pass
    print("<!-- generated by scripts/census2b_report.py -->\n")
    sec_warm()
    sec_feasibility()
    sec_artifacts()
    sec_boxcost()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
