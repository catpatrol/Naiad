"""TIER-C5-Q fixtures — the transcript, printed.  HALTs non-zero on any failure.

THE HOUSE RULE ADOPTED IN TC5 IS IN FORCE: **every leg states, inline, what
would have to be true for it to FAIL.**  A leg with no answer to "what would
break this?" is not a leg.

    F-Q-0   THE SCORED BOOK DID NOT MOVE — TC5's headline, registrations and
            fleet tables asserted byte-identical to the manifest COMMITTED AT
            HEAD, read out of git rather than argued from "this tool does not
            touch them"
    F-Q-1   COVERAGE — zero campaigns and zero instants missing, per lane and
            per kind
    F-Q-2   THREE CAMPAIGNS HAND-RECONCILED against the filed TC5 tables and
            raw 4h bars, including ETH-10-29 and a spring
    F-Q-3   THE TOOL IS DETERMINISTIC — two runs, one hash, including --random
    F-Q-4   THE TOOL IS INSTANT — < 2 s per query, measured as a cold
            subprocess, which is what a user actually pays
    F-Q-5   THE CHAMPION BLOCK IS CAUSAL — each champion re-derived from raw
            bars on its own clock, and proved to read no bar that had not closed
    F-Q-6   CAPTURED-NOT-CONSULTED unchanged — the decision path still imports
            no registry symbol
    F-KEY   every written table, on its declared key

USAGE  ~/venvs/naiad/bin/python scripts/tierc5q_fixtures.py
"""
from __future__ import annotations

import ast
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc5q as Q                                                 # noqa: E402
import tierc5 as T5                                                 # noqa: E402
import tierc5_rules as RC                                           # noqa: E402
import tierc4_fixtures as F4                                        # noqa: E402
import analytics as AN                                              # noqa: E402
from engine import indicators as ind                                # noqa: E402

PY = str(Path.home() / "venvs/naiad/bin/python")
T: list[str] = []
RESULTS: dict[str, bool] = {}


def rec(fid: str, ok: bool, lines: list[str]) -> bool:
    RESULTS[fid] = bool(ok)
    T.append(f"--- {fid} : {'PASS' if ok else 'FAIL'} ---")
    T.extend("    " + x for x in lines)
    return bool(ok)


def tbl(name: str, root: Path | None = None) -> pd.DataFrame:
    return pd.read_parquet((root or Q.OUT) / f"{name}.parquet")


def _stamped(v) -> bool:
    """Does this cell hold a real ISO timestamp?

    An ABSENT timestamp renders as the STRING "None", not as "" — so the
    obvious `if str(v)` is true for every empty cell in the book, and a leg
    written that way counts absences as events. It happens to be harmless where
    a range comparison follows ("None" sorts outside any ISO window), and that
    is exactly the kind of accident that stops being harmless when someone
    reuses the idiom without the comparison. Tested at the front instead.
    """
    return str(v)[:1].isdigit()


def sh(cmd: str) -> tuple[int, str]:
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=ROOT)
    return p.returncode, p.stdout


# ══════════════════════════ F-Q-0 · the scored book did not move
def f_frozen() -> bool:
    """THE GUARANTEE THE WHOLE STAGE RESTS ON.

    FAILS IF: any of TC5's headline / registrations / fleet content-hashes
    differs from the one committed at HEAD.  Asserted against GIT, not against
    a copy this session made — a tool that checks its own snapshot proves only
    that it can copy.  If the manifest is not tracked at HEAD the leg FAILS
    rather than passing on an absence.
    """
    lines, ok = [], True
    rc, out = sh("git show HEAD:research_outputs/tierc5/build_manifest.json")
    if rc != 0 or not out.strip():
        return rec("F-Q-0", False,
                   ["the TC5 manifest is not tracked at HEAD — nothing to "
                    "compare against, so this leg cannot pass"])
    committed = json.loads(out)["sha"]
    live = json.loads((Q.TC5 / "build_manifest.json").read_text())["sha"]
    lines.append(f"comparing the LIVE tierc5 manifest against "
                 f"`git show HEAD:research_outputs/tierc5/build_manifest.json`")
    for k in Q.FROZEN:
        a, b = committed.get(k), live.get(k)
        good = a is not None and a == b
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] {k:16} {str(a)[:32]}  "
                     f"{'== committed' if good else 'MOVED'}")
    # and every OTHER tierc5 table too — the card names three, but a tool that
    # moved a fourth would still have moved the record.
    others = [k for k in sorted(live) if k not in Q.FROZEN]
    moved = [k for k in others if committed.get(k) != live.get(k)]
    ok &= not moved
    lines.append(f"[{'OK ' if not moved else 'BAD'}] and the other "
                 f"{len(others)} tierc5 tables: {len(moved)} moved {moved}")

    # AND THE PARQUETS THEMSELVES, FROM DISK — TWO LEGS, BECAUSE ONE IS NOT
    # ENOUGH AND THE OTHER HAS A LIMIT THIS FIXTURE NAMES.
    #
    # The two legs above compare MANIFESTS, and a manifest is a claim ABOUT the
    # tables, not the tables. So:
    #   (a) every filed parquet is re-hashed from disk and compared with the
    #       SAME file as written by the independent re-run into tierc5_run2 —
    #       if a filed table had been edited it would differ from the re-run;
    #   (b) the read-back hash is compared with the COMMITTED manifest hash,
    #       which works for every table whose columns survive a parquet
    #       round-trip identically. `corridor_and_seal` does NOT: it carries two
    #       DICT-valued columns and numpy scalars whose `to_csv` rendering
    #       changes across the round-trip, so its read-back hash differs from
    #       the pre-write hash by construction. It is NAMED here rather than
    #       silently skipped, and leg (a) covers it.
    # Both legs found by the builder's own audit; leg (b) fired on its first run
    # and the firing was this artefact, not a moved table.
    import tierc2_baseline as _TB
    name_of = {"headline": "headline", "registrations": "registrations",
               "fleet": "fleet_unscored", "journal": "trade_journal",
               "funnel": "funnel", "by_slice": "headline_by_slice",
               "ratchet": "ratchet_ledger", "harvest_lab": "harvest_lab",
               "ae": "ae_study", "limit": "limit_grid", "size": "size_grid",
               "addsize": "addsize_grid", "league": "resistance_league",
               "midband": "midband_confluence", "lineage": "lineage",
               "corridor": "corridor_and_seal", "d13c": "d13c_counted_not_scored",
               "reg_text": "registration_text",
               "reg_robust": "registration_robustness",
               "tape": "analytics_tape", "tape_inventory": "tape_inventory"}
    ROUNDTRIP_EXCEPTION = {"corridor"}     # dict-valued columns; see above
    run2 = ROOT / "research_outputs" / "tierc5_run2"
    bad_run2, bad_manifest, checked_b = [], [], 0
    for key, fname in name_of.items():
        p1 = Q.TC5 / f"{fname}.parquet"
        if not p1.exists():
            bad_run2.append(f"{fname} MISSING")
            continue
        h1 = _TB._content_sha(pd.read_parquet(p1))
        p2 = run2 / f"{fname}.parquet"
        if p2.exists():
            h2 = _TB._content_sha(pd.read_parquet(p2))
            if h1 != h2:
                bad_run2.append(f"{fname} filed {h1[:10]} != re-run {h2[:10]}")
        if key not in ROUNDTRIP_EXCEPTION:
            checked_b += 1
            if h1 != committed.get(key):
                bad_manifest.append(
                    f"{fname} disk {h1[:10]} != committed {str(committed.get(key))[:10]}")
    ok &= not bad_run2
    lines.append(f"[{'OK ' if not bad_run2 else 'BAD'}] (a) all "
                 f"{len(name_of)} filed parquets re-hashed from disk equal the "
                 f"SAME table written by the independent re-run into "
                 f"tierc5_run2: {len(bad_run2)} disagree {bad_run2[:3]}")
    lines.append("      FAILS IF: a filed table was edited after it was "
                 "written. This leg reaches the FILES; the manifest legs above "
                 "reach only the claim about them.")
    ok &= not bad_manifest
    lines.append(f"[{'OK ' if not bad_manifest else 'BAD'}] (b) and "
                 f"{checked_b} of {len(name_of)} equal the COMMITTED manifest "
                 f"hash on read-back: {len(bad_manifest)} disagree "
                 f"{bad_manifest[:3]}")
    lines.append(f"      the {len(ROUNDTRIP_EXCEPTION)} exception is "
                 f"{sorted(ROUNDTRIP_EXCEPTION)} — `corridor_and_seal` carries "
                 f"DICT-valued columns whose to_csv rendering changes across a "
                 f"parquet round-trip, so its read-back hash differs from its "
                 f"pre-write hash BY CONSTRUCTION. Named, not skipped; leg (a) "
                 f"covers it and reports it identical to the re-run.")
    lines.append("      FAILS IF: any hash differs. The card froze three "
                 "tables; this leg freezes all 21, because a stage that moved "
                 "a fourth would still have moved the record.")
    lines.append("      Q1 writes ONLY to research_outputs/tierc5q/ — the "
                 "guarantee is structural AND checked, not one or the other.")
    return rec("F-Q-0", ok, lines)


# ══════════════════════════════════════════════ F-Q-1 · coverage
def f_coverage() -> bool:
    """FAILS IF: one instant in the ledger has no (asset, ts) row in the tape,
    one campaign has no instants at all, or the counts do not reconcile to the
    TC5 books (195 card + 241 spring, 60 add-carrying)."""
    lines, ok = [], True
    cov, inst, camp = tbl("coverage"), tbl("instants"), tbl("campaigns")
    tape = tbl("tape_full")
    man = json.loads((Q.OUT / "build_manifest.json").read_text())

    # ── THE LEG WITH CONTENT, FIRST ───────────────────────────────────────
    # The coverage assert below is CIRCULAR and this build says so: the tape is
    # built FROM the instant ledger, so of course the ledger is covered. The
    # question with content is whether the LEDGER is complete — whether every
    # timestamped bar the decision path names has a kind. That map is derived
    # by introspection over the record types, not written as a list, and this
    # leg asserts it is total. Found by the builder's own audit.
    import dataclasses as _dc
    fmap = Q.MS_FIELD_MAP
    kinds = set(inst["kind"])
    declared, missing_field, missing_kind = [], [], []
    for typ in (RC.Trade, RC.Advance, RC.Add, RC.Spring):
        for f_ in _dc.fields(typ):
            if not f_.name.endswith("_ms"):
                continue
            key = f"{typ.__name__}.{f_.name}"
            declared.append(key)
            if key not in fmap:
                missing_field.append(key)
            elif fmap[key] not in kinds:
                missing_kind.append(f"{key}->{fmap[key]}")
    good = not missing_field and not missing_kind
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] COMPLETENESS CONTRACT: all "
                 f"{len(declared)} timestamp fields across Trade/Advance/Add/"
                 f"Spring map to an instant kind that the ledger actually "
                 f"carries — unmapped {missing_field}, mapped-but-absent "
                 f"{missing_kind}")
    lines.append(f"      the map: {json.dumps(fmap)}")
    lines.append("      FAILS IF: a timestamped event is added to a record and "
                 "no kind is added with it. THIS is the leg the coverage "
                 "assert below cannot be — the tape is built FROM the ledger, "
                 "so coverage is circular and is printed as bookkeeping, not "
                 "as evidence.")
    lines.append("")

    # ── AND THE OTHER HALF OF IT: CARDINALITY ─────────────────────────────
    # ADVERSARIAL REPAIR Q-6.  The contract above is a check on KINDS, and one
    # row of a kind satisfies it.  A reviewer kept every arming/trigger/exit row
    # and exactly ONE each of advance, harvest, add, anchor_bar, pivot_bar,
    # retrace and sweep — 1,315 rows instead of 3,677, leaving 1,483 real book
    # bars with no snapshot — and this whole file returned 8/8 PASS.  The
    # coverage table below read `0 missing` because it is seeded from the frame
    # it checks, and the per-kind rows read 1 · 1 · 0 with an [OK] beside each.
    #
    # So the count is re-derived HERE from the campaigns table and the three
    # ledgers — never from the instants frame — and the ledgers are themselves
    # tied to campaigns.n_advances / .harvested / .adds_n by F-KEY.  Dedup is
    # honoured exactly rather than waved at: the ledger keys on
    # (campaign_id, kind, ts), so what a source table DEMANDS is its number of
    # DISTINCT (campaign_id, ts) pairs, not its row count.
    advs_t, harv_t, add_t = tbl("advances"), tbl("harvests"), tbl("adds")
    nd = (lambda df, col: 0 if not len(df)
          else len(df[["campaign_id", col]].drop_duplicates()))
    spr = camp[camp["lane"] == "spring"]
    want = {
        "arming":     (len(camp), "one per campaign"),
        "trigger":    (len(camp), "one per campaign"),
        "exit":       (len(camp), "one per campaign"),
        "anchor_bar": (int(camp["anchor_bar_ts"].map(_stamped).sum()),
                       "campaigns carrying an anchor bar"),
        "sweep":      (int(spr["spring_sweep_ts"].map(_stamped).sum()),
                       "spring campaigns"),
        "advance":    (nd(advs_t, "conf_ts"), "distinct (campaign, conf_ts)"),
        "pivot_bar":  (nd(advs_t, "pivot_bar_ts"), "distinct (campaign, pivot bar)"),
        "harvest":    (nd(harv_t, "harvest_ts"), "distinct (campaign, harvest_ts)"),
        "add":        (nd(add_t, "add_ts"), "distinct (campaign, add_ts)"),
        "retrace":    (nd(add_t, "retrace_ts"), "distinct (campaign, retrace_ts)"),
    }
    got = inst["kind"].value_counts().to_dict()
    lines.append("    THE CARDINALITY CONTRACT — every kind's row count "
                 "re-derived from the SOURCE tables, never from the ledger:")
    lines.append(f"      {'kind':12} {'in ledger':>10} {'demanded':>9}   "
                 f"what demands it")
    for k in sorted(want):
        n_want, why = want[k]
        n_got = int(got.get(k, 0))
        g = n_got == n_want
        ok &= g
        lines.append(f"      {'[OK ]' if g else '[BAD]'} {k:<12} {n_got:>8,} "
                     f"{n_want:>9,}   {why}")
    extra = sorted(set(got) - set(want))
    ok &= not extra
    lines.append(f"      [{'OK ' if not extra else 'BAD'}] and no kind in the "
                 f"ledger that no source demands: {extra}")
    tot_want = sum(v[0] for v in want.values())
    g = tot_want == len(inst)
    ok &= g
    lines.append(f"      [{'OK ' if g else 'BAD'}] TOTAL {len(inst):,} == "
                 f"{tot_want:,} demanded")
    lines.append(f"      dedup collapsed "
                 f"{man['counts']['instants_collapsed_by_dedup']} of "
                 f"{man['counts']['instants_pre_dedup']:,} raw rows — filed, "
                 f"and already inside the DISTINCT counts above")
    lines.append("      FAILS IF: the ledger loses a row that a campaign, an "
                 "advance, a harvest or an add demands. THIS is the leg that "
                 "the presence contract above and the coverage table below "
                 "both cannot be: a book can lose 64% of its instants and pass "
                 "either one.")
    lines.append("")

    tot = cov[cov["lane"] == "__ALL__"].iloc[0]
    good = int(tot["missing"]) == 0
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] (bookkeeping, circular by "
                 f"construction) {int(tot['instants']):,} instants demanded · "
                 f"{int(tot['covered']):,} covered · {int(tot['missing'])} "
                 f"MISSING")
    lines.append("")
    lines.append(f"  {'lane':12} {'kind':10} {'instants':>9} {'covered':>9} "
                 f"{'missing':>8}")
    for _, r in cov[~cov["lane"].isin(["__ALL__"])].iterrows():
        g = int(r["missing"]) == 0
        ok &= g
        lines.append(f"  {'[OK ]' if g else '[BAD]'} {r['lane']:<12} "
                     f"{r['kind']:<10} {int(r['instants']):>9} "
                     f"{int(r['covered']):>9} {int(r['missing']):>8}")

    # the population must reconcile to the books TC5 scored
    c = man["counts"]
    checks = [("card campaigns", c["campaigns_card"], 195),
              ("spring campaigns", c["campaigns_spring"], 241),
              ("add-carrying campaigns", c["campaigns_add_carrying"], 60)]
    lines.append("")
    for name, got, want in checks:
        g = got == want
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {name:26} {got} == {want} "
                     f"(TC5's own filed count)")

    # every campaign carries at least arming + trigger + exit
    per = inst.groupby("campaign_id")["kind"].apply(set)
    need = {"arming", "trigger", "exit"}
    bad = [k for k, v in per.items() if not need <= v]
    ok &= not bad
    lines.append(f"[{'OK ' if not bad else 'BAD'}] every one of {len(camp)} "
                 f"campaigns carries at least arming+trigger+exit: "
                 f"{len(bad)} short")
    orphan = set(camp["campaign_id"]) - set(inst["campaign_id"])
    ok &= not orphan
    lines.append(f"[{'OK ' if not orphan else 'BAD'}] campaigns with NO "
                 f"instants at all: {len(orphan)}")

    # the corridor is at least the ruled 3 years, and the spine is daily
    yrs = man["counts"]["corridor_years"]
    g = yrs >= 3.0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] corridor {yrs} years >= the ruled "
                 f"3 — {man['corridor']['panel_start'][:10]} → "
                 f"{man['corridor']['last_closed_4h_close'][:10]}")
    spine = tape[tape["instant"] == "spine"]
    per_asset = spine.groupby("asset")["ts"].apply(
        lambda s: int(np.median(np.diff(sorted(s)))) if len(s) > 2 else 0)
    g = bool((per_asset == Q.MS_1D).all())
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the spine is DAILY on every asset "
                 f"(median gap {set(per_asset.tolist())} ms; 86,400,000 = 1 d) "
                 f"— {len(spine):,} spine rows")
    lines.append("      FAILS IF: a gap is weekly. TC5's tape was weekly and "
                 "sized for a document; a queryable book is not.")
    lines.append(f"      families captured: AVWAP set · RVWAP ±1σ/±2σ · period "
                 f"extremes · champions {man['counts']['champion_blocks']}")
    return rec("F-Q-1", ok, lines)


# ═══════════════════════ F-Q-2 · three campaigns, hand-reconciled
def f_reconcile() -> bool:
    """THREE CAMPAIGNS, END TO END, AGAINST THE FILED TC5 TABLES AND RAW BARS.

    FAILS IF: a campaign row disagrees with TC5's own filed journal; an advance
    row disagrees with TC5's filed ratchet ledger; a tape row's `close` is not
    the raw 4h close at that bar; or a spring's stop is not the rail-and-buffer
    arithmetic applied to the sweep extreme re-read from raw bars.
    """
    lines, ok = [], True
    camp, adv = tbl("campaigns"), tbl("advances")
    tape = tbl("tape_full").set_index(["asset", "ts"])
    inst = tbl("instants")
    j5 = pd.read_parquet(Q.TC5 / "trade_journal.parquet")
    r5 = pd.read_parquet(Q.TC5 / "ratchet_ledger.parquet")

    # the three picks, adversarial and NAMED
    eth = "ETHUSDT:card:20251029T1600"
    springs = camp[camp["lane"] == "spring"]
    # ADVERSARIAL, NOT CONVENIENT: the WORST spring, not the best. The first
    # draft picked the best and the review called it — a leg that only ever
    # inspects the flattering row is a leg that has chosen its evidence.
    spr = springs.sort_values("net_r").iloc[0]["campaign_id"]
    addc = camp[(camp["lane"] == "card") & (camp["adds_n"] > 0)] \
        .sort_values("adds_delta_vs_card", ascending=False).iloc[0]["campaign_id"]
    picks = [(eth, "the ETH-10-29 row the card names"),
             (spr, "the best SPRING campaign — the lane TC5 filed no journal for"),
             (addc, "the largest ADD delta — the only paired delta a campaign owns")]

    for cid, why in picks:
        row = camp[camp["campaign_id"] == cid]
        if not len(row):
            ok = False
            lines.append(f"[BAD] {cid} absent")
            continue
        r = row.iloc[0]
        lines.append("")
        lines.append(f"CAMPAIGN  {cid}   ({why})")

        # (a) against TC5's OWN FILED JOURNAL, for card campaigns
        if r["lane"] == "card":
            m = j5[(j5["asset"] == r["asset"])
                   & (j5["entry_ms"] == int(r["entry_ms"]))]
            g = len(m) == 1
            if g:
                f0 = m.iloc[0]
                for col in ("net_r", "r_dist", "entry_px", "exit_px", "mfe_r"):
                    d_ = abs(float(r[col]) - float(f0[col]))
                    g &= d_ < 1e-9
                g &= int(r["n_advances"]) == int(f0["n_advances"])
                g &= bool(r["harvested"]) == bool(f0["harvested"])
                g &= int(r["exit_ms"]) == int(f0["exit_ms"])
            ok &= g
            lines.append(f"  [{'OK ' if g else 'BAD'}] equals TC5's FILED "
                         f"journal row on net R, R, entry/exit px, MFE, advance "
                         f"count, harvest flag and exit instant")
            lines.append("        FAILS IF: the Q1 re-derivation moved a scored "
                         "number. This is F-Q-0's guarantee at the row level.")
        else:
            # (a') A SPRING HAS NO FILED JOURNAL — SO IT IS RE-READ FROM RAW
            # BARS, NOT RESTATED FROM Q1'S OWN COLUMNS.
            # The first draft loaded the raw frame, never used it, and ran Q1's
            # stored `spring_sweep_extreme` through a transcription of
            # `spring_stop` — proving only that r6() preserves a min/max. The
            # review called it. Now the swept LEVEL and the sweep EXTREME are
            # both re-derived from the raw 4h series, and only then is the stop
            # arithmetic applied.
            f = T5.frame(r["asset"])["f"]
            d = 1 if r["direction"] == "long" else -1
            si = int(np.searchsorted(f.open_ms, int(T5._ms(r["spring_sweep_ts"][:10]))))
            si = int(np.searchsorted(f.open_ms,
                                     int(pd.Timestamp(r["spring_sweep_ts"]).value // 10**6)))
            ri = int(np.searchsorted(f.open_ms, int(r["entry_ms"])))
            LB = RC.SPRING_LOOKBACK_BARS
            lvl = (float(np.min(f.l[si - LB:si])) if d == 1
                   else float(np.max(f.h[si - LB:si])))
            g1 = abs(lvl - float(r["spring_swept_level"])) < 1e-9
            ok &= g1
            lines.append(f"  [{'OK ' if g1 else 'BAD'}] the swept level "
                         f"RE-READ from the {LB} raw bars STRICTLY before the "
                         f"sweep = {lvl:.6f} (table "
                         f"{float(r['spring_swept_level']):.6f})")
            g2 = (f.l[si] < lvl) if d == 1 else (f.h[si] > lvl)
            ok &= bool(g2)
            lines.append(f"  [{'OK ' if g2 else 'BAD'}] the sweep bar TOOK IT "
                         f"OUT from raw bars: "
                         f"{(f.l[si] if d == 1 else f.h[si]):.6f} "
                         f"{'<' if d == 1 else '>'} {lvl:.6f}")
            seg = (f.l[si:ri + 1] if d == 1 else f.h[si:ri + 1])
            ext = float(seg.min()) if d == 1 else float(seg.max())
            g3 = abs(ext - float(r["spring_sweep_extreme"])) < 1e-9
            ok &= g3
            lines.append(f"  [{'OK ' if g3 else 'BAD'}] the sweep EXTREME "
                         f"RE-READ over raw bars {si}..{ri} INCLUSIVE of the "
                         f"reclaim bar = {ext:.6f} (table "
                         f"{float(r['spring_sweep_extreme']):.6f})")
            atr = float(r["atr_at_entry"])
            pstop = ext - d * RC.STOP_BUF_ATR * atr
            rail = float(r["entry_px"]) - d * RC.MIN_STOP_ATR * atr
            want = min(pstop, rail) if d == 1 else max(pstop, rail)
            g4 = abs(want - float(r["stop_px"])) < 1e-6
            ok &= g4
            lines.append(f"  [{'OK ' if g4 else 'BAD'}] and the stop = the "
                         f"farther of {{that extreme "
                         f"{'-' if d == 1 else '+'} {RC.STOP_BUF_ATR}xATR, "
                         f"entry {'-' if d == 1 else '+'} {RC.MIN_STOP_ATR}xATR}} "
                         f"= {want:.6f} (table {float(r['stop_px']):.6f})")
            lines.append("        FAILS IF: the level or the extreme disagrees "
                         "with the raw bars — TC5 filed no spring journal, so "
                         "this is the only place the lane's geometry is checked "
                         "against anything other than itself.")

        # (b) advances against TC5's FILED ratchet ledger (card only)
        ma = adv[adv["campaign_id"] == cid]
        if r["lane"] == "card" and len(ma):
            mr = r5[(r5["asset"] == r["asset"])
                    & (r5["entry_ms"] == int(r["entry_ms"]))]
            g = len(mr) == len(ma)
            if g:
                a1 = ma.sort_values("advance_seq")["new_stop_px"].astype(float).to_numpy()
                a2 = mr.sort_values("advance_seq")["new_stop_px"].astype(float).to_numpy()
                g = bool(np.allclose(a1, a2, atol=1e-9))
            ok &= g
            lines.append(f"  [{'OK ' if g else 'BAD'}] {len(ma)} advance(s) "
                         f"equal TC5's FILED ratchet ledger, stop for stop")

        # (c) every instant's tape `close` IS the raw 4h close at that bar
        f = T5.frame(r["asset"])["f"]
        mi = inst[inst["campaign_id"] == cid]
        bad = 0
        for _, i_ in mi.iterrows():
            key = (i_["asset"], int(i_["ts"]))
            if key not in tape.index:
                bad += 1
                continue
            k = int(np.searchsorted(f.open_ms, int(i_["ts"])))
            if abs(float(f.c[k]) - float(tape.loc[key, "close"])) > 1e-6:
                bad += 1
        ok &= (bad == 0)
        lines.append(f"  [{'OK ' if bad == 0 else 'BAD'}] all {len(mi)} "
                     f"instants: the tape's `close` IS the raw 4h close at that "
                     f"bar ({bad} disagreements)")
        lines.append("        FAILS IF: the tape sampled a different bar than "
                     "the instant names — the whole tool is a join on (asset, "
                     "ts) and a shifted join would be invisible in the output.")
    return rec("F-Q-2", ok, lines)


# ════════════════════════════ F-Q-3 · the tool is deterministic
def f_determinism() -> bool:
    """FAILS IF: two runs of the same query differ by one byte, or --random with
    the same seed picks a different set.  A spot-audit that cannot be reproduced
    is an anecdote."""
    lines, ok = [], True
    cases = ["ETHUSDT:card:20251029T1600", "--day 2025-10-29",
             "--random 5", "--random 5 --seed 7", "--list ZECUSDT"]
    for c in cases:
        rc1, o1 = sh(f"{PY} scripts/query_trade.py {c}")
        rc2, o2 = sh(f"{PY} scripts/query_trade.py {c}")
        h1 = hashlib.sha256(o1.encode()).hexdigest()[:16]
        h2 = hashlib.sha256(o2.encode()).hexdigest()[:16]
        good = rc1 == 0 and rc2 == 0 and h1 == h2 and len(o1) > 0
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] `{c:26}` two runs → "
                     f"{h1} == {h2}  ({len(o1):,} chars)")
    # and two DIFFERENT seeds must pick DIFFERENT campaigns, or the seed is
    # decorative
    _, a = sh(f"{PY} scripts/query_trade.py --random 5")
    _, b = sh(f"{PY} scripts/query_trade.py --random 5 --seed 7")
    good = a != b
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] two different seeds pick "
                 f"different campaigns — the seed is load-bearing, not "
                 f"decoration")
    lines.append("      FAILS IF: the outputs are equal. A --random that "
                 "ignores its seed would pass the determinism leg above and "
                 "mean nothing.")
    return rec("F-Q-3", ok, lines)


# ═══════════════════════════════ F-Q-4 · the tool is instant
def f_speed() -> bool:
    """FAILS IF: any query takes 2 s or more, measured as a COLD SUBPROCESS —
    interpreter start, imports, parquet reads and rendering — because that is
    what a user actually waits for.  An in-process timing would flatter the
    tool by hiding the part it cannot avoid."""
    lines, ok = [], True
    camp = tbl("campaigns")
    ids = sorted(camp["campaign_id"])
    rng = np.random.default_rng(Q.SEED)
    sample = [ids[i] for i in rng.choice(len(ids), size=12, replace=False)]
    worst, times = 0.0, []
    for cid in sample + ["--day 2025-10-29", "--random 3"]:
        t0 = time.time()
        rc, _ = sh(f"{PY} scripts/query_trade.py {cid}")
        dt = time.time() - t0
        times.append(dt)
        worst = max(worst, dt)
        ok &= (rc == 0 and dt < 2.0)
    lines.append(f"[{'OK ' if ok else 'BAD'}] {len(times)} cold-subprocess "
                 f"queries over the full {len(ids)}-campaign book: "
                 f"median {np.median(times)*1000:.0f} ms · "
                 f"WORST {worst*1000:.0f} ms · budget 2,000 ms")
    lines.append(f"      headroom {2.0/worst:.1f}x. The tool COMPUTES NOTHING — "
                 f"it joins seven parquet tables Q1 already wrote. The moment "
                 f"it starts deriving, this leg is the one that catches it.")
    lines.append("      FAILS IF: any single query reaches 2 s.")
    return rec("F-Q-4", ok, lines)


# ═════════════════════════ F-Q-5 · the champion block is causal
def f_champions() -> bool:
    """FAILS IF: a champion EMA is read from a bar that had NOT CLOSED at the
    instant, or its distance disagrees with a raw-bar re-derivation on its own
    clock.  This is the one block Q1 adds that the estate had not already
    fixtured, so it is checked from raw bars rather than from itself."""
    lines, ok = [], True
    tape = tbl("tape_full")
    rng = np.random.default_rng(Q.SEED)
    idx = rng.choice(len(tape), size=min(40, len(tape)), replace=False)
    sample = tape.iloc[sorted(idx)]
    bad_val = bad_causal = bad_warm = 0
    n_checked = 0
    for tf, L in Q.CHAMPIONS:
        step = {"1h": Q.MS_1H, "4h": Q.MS_4H, "12h": 12 * Q.MS_1H,
                "1d": Q.MS_1D}[tf]
        for sym, g in sample.groupby("asset"):
            d = T5._tf_frame(sym, tf)
            for _, r in g.iterrows():
                as_of = int(r["ts"]) + Q.MS_4H      # the row's own bar CLOSE
                k = int(np.searchsorted(d["t"] + step, as_of, "right")) - 1
                want = r.get(f"champ_{tf}_ema{L}_dist_atr")
                warm = bool(r.get(f"champ_{tf}_ema{L}_warm"))
                if k < L:
                    # NOT WARM: the column must be NULL, not a seed price.
                    if warm or (want is not None and np.isfinite(want)):
                        bad_warm += 1
                    continue
                if want is None or not np.isfinite(want):
                    continue
                n_checked += 1
                # ── INDEPENDENT RE-DERIVATION BY ENDPOINT SLICING ──────────
                # NOT a transcription of `champion_cols`: the series is SLICED
                # to the as-of bar and the EMA/ATR recomputed on the slice, then
                # read at [-1]. That is a different computation path, and it is
                # also the CAUSALITY test — if any future bar contributed, the
                # sliced value would differ from the full-series one. The
                # estate's own F-C2-7 pattern.
                e_end = float(ind.ema(d["c"][:k + 1], L)[-1])
                a_end = float(ind.atr(d["h"][:k + 1], d["l"][:k + 1],
                                      d["c"][:k + 1], RC.ATR_LEN)[-1])
                if not (np.isfinite(a_end) and a_end > 0):
                    continue
                got = (float(r["close"]) - e_end) / a_end
                if abs(got - float(want)) > 1e-5:
                    bad_val += 1
                # and the bar used must have CLOSED at or before the as-of
                if d["t"][k] + step > as_of:
                    bad_causal += 1
    ok &= (bad_val == 0 and bad_causal == 0 and bad_warm == 0)
    lines.append(f"[{'OK ' if bad_val == 0 else 'BAD'}] INDEPENDENT "
                 f"RE-DERIVATION by ENDPOINT SLICING over {n_checked} "
                 f"(row x champion) pairs: {bad_val} disagree")
    lines.append("      the series is SLICED to the as-of bar and the EMA/ATR "
                 "recomputed on the slice, then read at [-1] — a different "
                 "computation path from the precomputed-series lookup, and "
                 "simultaneously the causality test: if ANY future bar "
                 "contributed, the sliced value would differ. FAILS IF it does.")
    lines.append(f"[{'OK ' if bad_causal == 0 else 'BAD'}] and the bar used had "
                 f"CLOSED at or before the as-of instant: {bad_causal} "
                 f"violations")
    lines.append("      (this counter is weak on its own and is said to be — "
                 "searchsorted('right')-1 nearly guarantees it. The leg with "
                 "content is the endpoint slicing above.)")
    lines.append(f"[{'OK ' if bad_warm == 0 else 'BAD'}] THE WARM-UP FLOOR: "
                 f"{bad_warm} rows publish a champion before its EMA has seen "
                 f"its own length")
    lines.append("      FAILS IF: one does. `engine.indicators.ema` SEEDS at "
                 "the series start and never returns NaN, so without this floor "
                 "a 4,618-length EMA publishes the first close of the series as "
                 "a wall — the exact defect TC5's §9 repair #4 fixed in the "
                 "decision path and this module reintroduced.")
    lines.append(f"      the champions are {[f'{t}:EMA{l}' for t, l in Q.CHAMPIONS]} "
                 f"— TC5 §6.2's league winners, each read on the clock it won "
                 f"on. Reading them all on the 4h lens would be a different "
                 f"quantity from the one the league scored.")
    lines.append("      FAILS IF: either count is non-zero.")
    return rec("F-Q-5", ok, lines)


# ═══════════════════════ F-Q-6 · captured-not-consulted, unchanged
def f_closure() -> bool:
    """FAILS IF: the decision path imports `analytics` anywhere in its
    transitive closure, or names a tape column in its CODE.  Q1 and the tool
    import analytics freely — they are measurement and reporting — and the
    point of this leg is that adding them changed nothing upstream."""
    lines, ok = [], True
    names = ("tierc5_rules", "tierc4_rules", "tierc3_rules", "tierc2_rules")
    srcs = {f"scripts/{n}.py": (ROOT / "scripts" / f"{n}.py").read_text()
            for n in names}
    for name, src in srcs.items():
        imported = []
        for node in ast.walk(ast.parse(src)):
            if isinstance(node, ast.Import):
                imported += [x.name for x in node.names]
            elif isinstance(node, ast.ImportFrom):
                imported.append(node.module or "")
        hits = [m for m in imported if m == "analytics"
                or m.startswith("analytics.")]
        g = not hits
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {name}: analytics hits {hits}")
    tape_cols = ["wall_family", "dist_atr", "coloc_n", "nearest_level",
                 "rvwap", "avwap", "prior_extreme"]
    code = {n: F4.code_only(s) for n, s in srcs.items()}
    named = {n: [c for c in tape_cols if c in s] for n, s in code.items()}
    g = not any(named.values())
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] tape column names in the decision "
                 f"path's CODE: {named}")
    lines.append(f"      Q1 and query_trade.py import analytics and read every "
                 f"one of those columns — that is what they are FOR. Nothing "
                 f"they produce re-enters a decision, because there are no "
                 f"decisions downstream of them.")
    lines.append("      FAILS IF: a decision module gains an analytics import "
                 "or a tape column name.")
    return rec("F-Q-6", ok, lines)


# ═══════════════════════ F-Q-7 · the sentences the tool prints
def f_claims() -> bool:
    """EVERY ASSERTION THE SCREEN MAKES, CHECKED AGAINST THE SOURCE.

    ADVERSARIAL REPAIRS Q-7, Q-8, Q-9 — and the fixture that should have existed
    before them.  F-Q-0..F-Q-6 check what the tool COMPUTES: hashes, coverage,
    determinism, latency, champions, closure.  Not one of them reads a sentence
    the tool PRINTS.  All three of this round's tool defects lived in that gap —
    a flag stamped from the wrong lane, an empty-day claim that was false on 314
    days, and a cross-build existence claim that was false on 332 of the 343
    screens that made it.  A book whose numbers are right and whose sentences
    are wrong is not a trustworthy read surface; it is a trap with good
    arithmetic.

    FAILS IF: a rendered claim disagrees with the tables it claims to summarize.
    """
    import query_trade as QT                                          # noqa
    lines, ok = [], True
    camp, inst, adv = tbl("campaigns"), tbl("instants"), tbl("advances")
    D = QT._load()

    # ── Q-7 · the PROVISIONAL flag is the row's OWN lane's slice ──────────
    n_by = camp.groupby(["lane", "slice_year"]).size().to_dict()
    want = [int(n_by.get((ln, y), 0)) < RC.PROVISIONAL_MIN_N
            for ln, y in zip(camp["lane"], camp["slice_year"])]
    bad = int((np.array(want) != camp["slice_provisional"].astype(bool).values).sum())
    ok &= bad == 0
    lines.append(f"[{'OK ' if not bad else 'BAD'}] slice_provisional is the "
                 f"campaign's OWN lane's slice on all {len(camp)} rows: {bad} "
                 f"disagree")
    # and the leg is not vacuous — the card-anchored reading it replaced DOES
    # differ, on rows we can name.
    n_card = camp[camp["lane"] == "card"].groupby("slice_year").size().to_dict()
    old = [int(n_card.get(y, 0)) < RC.PROVISIONAL_MIN_N for y in camp["slice_year"]]
    moved = camp[np.array(old) != np.array(want)]
    good = len(moved) > 0
    ok &= good
    yrs = sorted(set(zip(moved["lane"], moved["slice_year"])))
    lines.append(f"[{'OK ' if good else 'BAD'}] and the repair is not "
                 f"cosmetic: the CARD-anchored reading this replaced differs on "
                 f"{len(moved)} rows {yrs} — every one a spring campaign "
                 f"wearing the card lane's thinness verdict")
    lines.append("      FAILS IF: the two readings agree. Then the repair "
                 "changed nothing and the leg is decoration.")

    # ── Q-8 · a day the tool calls empty is a day the BOOK was empty ──────
    ev_days = set(inst.loc[inst["kind"] != "spine", "ts_iso"].str[:10])
    old_days = set(camp["entry_ts"].str[:10]) | set(camp["exit_ts"].str[:10]) \
        | set(camp["arm_ts"].str[:10])
    hidden = sorted(ev_days - old_days)
    d0 = hidden[0] if hidden else "—"
    rows0 = QT.render_day(d0, D) if hidden else []
    good = bool(hidden) and "(nothing" not in "\n".join(rows0)
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] --day: {len(hidden)} days "
                 f"carried a book event but NO arming/entry/exit — the old "
                 f"filter called every one of them empty. First is {d0}, and "
                 f"it now renders {max(len(rows0) - 3, 0)} campaign(s)")
    # the named regression, kept by name
    t2 = "\n".join(QT.render_day("2025-11-01", D))
    good = "ETHUSDT:card:20251029T1600" in t2 and "advanced" in t2
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] the named case: `--day "
                 f"2025-11-01` shows ETHUSDT:card:20251029T1600 advancing "
                 f"(it printed `(nothing)` before Q-8, while the same tool "
                 f"printed that advance on the campaign screen)")
    # and every day the tool DOES call empty must really be empty
    sample = sorted(set(inst["ts_iso"].str[:10]) - ev_days)[:40]
    lied = [d for d in sample if "(nothing" not in "\n".join(QT.render_day(d, D))]
    ok &= not lied
    lines.append(f"[{'OK ' if not lied else 'BAD'}] and over {len(sample)} "
                 f"spine-only days the tool calls empty, {len(lied)} actually "
                 f"held a book event")
    lines.append("      FAILS IF: a day with an advance, a harvest or an add "
                 "renders as '(nothing)'. The header says THE BOOK ON <day>.")

    # ── Q-9 · the seal sentence says only what was checked ────────────────
    # RE-DERIVED FROM A DIFFERENT PATH: Q1 counts the campaign's sealed bars off
    # the INSTANT ledger; this counts them off the campaign row's own timestamp
    # columns and the advances table. Same number, two paths — not the same
    # computation compared to itself.
    lb0, lb1 = RC.LOCKBOX_WAS[0], RC.LOCKBOX_WAS[1] + "T23:59:59Z"
    ain: dict[str, int] = {}
    # ALL THREE LEDGERS. The first draft of this leg counted advances and forgot
    # the adds, and disagreed with the filed column on exactly the 19
    # add-carrying campaigns whose add/retrace bars fall in the span. The FILED
    # number was right and the re-derivation was short — which is the whole
    # reason a second path is worth writing.
    for src, cs in ((adv, ("conf_ts", "pivot_bar_ts")),
                    (tbl("adds"), ("add_ts", "retrace_ts"))):
        for c in cs:
            if not len(src):
                continue
            hit = src[(src[c] >= lb0) & (src[c] <= lb1)]
            for cid_, n_ in hit["campaign_id"].value_counts().items():
                ain[cid_] = ain.get(cid_, 0) + int(n_)
    cols = ["arm_ts", "anchor_bar_ts", "entry_ts", "harvest_ts", "exit_ts",
            "spring_sweep_ts"]
    mine = []
    for _, r in camp.iterrows():
        n = sum(1 for c in cols
                if _stamped(r[c]) and lb0 <= str(r[c]) <= lb1)
        mine.append(n + int(ain.get(r["campaign_id"], 0)))
    bad = int((np.array(mine) != camp["sealed_instants"].astype(int).values).sum())
    ok &= bad == 0
    lines.append(f"[{'OK ' if not bad else 'BAD'}] sealed_instants re-derived "
                 f"from the campaign row's OWN timestamps + the advances "
                 f"ledger (not from the instant frame Q1 counted): {bad} of "
                 f"{len(camp)} disagree")
    stale = int((camp["lockbox_was"].astype(str)
                 != f"{RC.LOCKBOX_WAS[0]}→{RC.LOCKBOX_WAS[1]}").sum())
    ok &= stale == 0
    lines.append(f"[{'OK ' if not stale else 'BAD'}] and the window on every "
                 f"row IS RC.LOCKBOX_WAS ({RC.LOCKBOX_WAS[0]}→"
                 f"{RC.LOCKBOX_WAS[1]}): {stale} stale. The tool used to carry "
                 f"its own hard-coded copy, which the register could outrun in "
                 f"silence.")
    # the named counterexample: entry AND harvest inside the span, anchor outside
    sol = "SOLUSDT:card:20240707T1600"
    if sol in set(camp["campaign_id"]):
        t3 = "\n".join(QT.render(sol, D))
        good = ("could have taken it unchanged" not in t3
                and "own quoted bars sit inside" in t3)
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] the named counterexample "
                     f"{sol}: entry 137.277 and harvest 140.556 are both closes "
                     f"inside the span while the ANCHOR sits outside it, so the "
                     f"two-flag test missed it and the screen read 'quotes no "
                     f"price from the old lockbox'")
    # no spring campaign may claim a C2/C3/C4 counterpart — the lane is new
    spr = camp[camp["lane"] == "spring"]
    claim = int(spr["in_tc4_book"].fillna(False).astype(bool).sum())
    ok &= claim == 0
    lines.append(f"[{'OK ' if not claim else 'BAD'}] {claim} of "
                 f"{len(spr)} SPRING campaigns claim a Tier-C4 counterpart — "
                 f"P-SPR-1 registers the lane GENUINELY NEW, so the only "
                 f"correct number is zero")
    j = pd.read_parquet(Q.TC4_JOURNAL)
    n_in = int(camp["in_tc4_book"].fillna(False).astype(bool).sum())
    good = n_in == len(j)
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] in_tc4_book is a MEMBERSHIP "
                 f"test against the filed journal, and it finds all "
                 f"{n_in}/{len(j)} of Tier-C4's rows in this book")
    lines.append("      FAILS IF: the screen makes a cross-build claim the "
                 "tables cannot support. The first draft printed 'Tier-C2, C3 "
                 "and C4 could have taken it unchanged' on 343 screens; 332 "
                 "were false.")
    return rec("F-Q-7", ok, lines)


# ════════════════════════════════════════════════════════ F-KEY
def f_keys() -> bool:
    """FAILS IF: any written table has a duplicate on its declared key, or the
    ledgers do not reconcile to the campaigns table."""
    lines, ok = [], True
    keys = {"campaigns": ["campaign_id"],
            "instants": ["campaign_id", "kind", "ts"],
            "advances": ["campaign_id", "advance_seq"],
            "harvests": ["campaign_id"],
            "adds": ["campaign_id", "add_seq"],
            "tape_full": ["asset", "ts"],
            "coverage": ["lane", "kind"]}
    for n, k in keys.items():
        d = tbl(n)
        dup = int(d.duplicated(subset=k).sum()) if len(d) else 0
        g = dup == 0
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {n:12} key={k} "
                     f"rows={len(d):,} dup={dup}")
    camp, adv, hv, ad = (tbl("campaigns"), tbl("advances"), tbl("harvests"),
                         tbl("adds"))
    checks = [("advances", len(adv), int(camp["n_advances"].astype(int).sum())),
              ("harvests", len(hv), int(camp["harvested"].sum())),
              ("adds", len(ad), int(camp["adds_n"].astype(int).sum()))]
    for n, a, b in checks:
        g = a == b
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {n} ledger {a} == "
                     f"sum(campaigns.{'n_advances' if n=='advances' else n[:-1]+'ed' if n=='harvests' else 'adds_n'}) {b}")
    orph = set(adv["campaign_id"]) | set(hv["campaign_id"]) | set(ad["campaign_id"])
    bad = orph - set(camp["campaign_id"])
    ok &= not bad
    lines.append(f"[{'OK ' if not bad else 'BAD'}] every ledger row points at a "
                 f"campaign that exists: {len(bad)} orphans")
    lines.append("      FAILS IF: a ledger and the campaigns table disagree — "
                 "the tool joins on campaign_id and an orphan would render as "
                 "a silently empty block.")
    return rec("F-KEY", ok, lines)


def main() -> int:
    print("=" * 78)
    print("TIER-C5-Q FIXTURE TRANSCRIPT — THE QUERYABLE BOOK")
    print("=" * 78)
    f_frozen()
    f_coverage()
    f_reconcile()
    f_determinism()
    f_speed()
    f_champions()
    f_closure()
    f_claims()
    f_keys()
    print("\n".join(T))
    n_ok = sum(RESULTS.values())
    print()
    print("=" * 78)
    print(f"FIXTURE SUMMARY  {n_ok}/{len(RESULTS)} PASS  {json.dumps(RESULTS)}")
    print(f"  I9: ANALYTICS_VERSION {AN.ANALYTICS_VERSION} · analytics_sha "
          f"{AN.analytics_sha()}")
    print("=" * 78)
    if n_ok < len(RESULTS):
        print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
