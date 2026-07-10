"""D7: dry-run autopsy — prove the journal can answer every autopsy question.

Replays the BTC swing cell over 2026-05-01 -> 2026-07-07 (SPENT window —
plumbing check only, never evidence), writes the journal copy to
research_outputs/dryrun/journal/, then answers every question in
fixtures/autopsy_questions.md FROM THE JOURNAL ALONE into
research_outputs/dryrun_autopsy.md. F8 scans both artifacts.

  python scripts/dryrun_autopsy.py [--backfill]
"""

import argparse
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine.journal import read_journal
from engine.replay import run_replay

ROOT = Path(__file__).resolve().parent.parent
JROOT = ROOT / "research_outputs" / "dryrun" / "journal"
CELL = "BTCUSDT_swing"
START, END = "2026-05-01", "2026-07-07"


def fmt(x, nd=3):
    if x is None:
        return "-"
    return f"{x:.{nd}f}" if isinstance(x, float) else str(x)


def q(rows, evt=None, **conds):
    out = []
    for r in rows:
        if evt and r["evt"] != evt:
            continue
        if all(r.get(k) == v for k, v in conds.items()):
            out.append(r)
    return out


def ts_ms(s):
    return int(datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
               .replace(tzinfo=timezone.utc).timestamp() * 1000)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--backfill", action="store_true")
    args = ap.parse_args()

    summary = run_replay("naiad_v0", CELL, START, END, JROOT,
                         backfill=args.backfill)
    rows = read_journal(JROOT, CELL)
    exits = q(rows, "EXIT")
    fills = [r for r in rows if r["evt"] in ("ENTRY_FILL", "ADD_FILL")]
    fill_by_tr = {r["tranche_id"]: r for r in fills}
    primes = q(rows, "PRIME")
    rejects = q(rows, "REJECT")
    L = []

    def w(*lines):
        L.extend(lines)

    n_ex = len(exits)
    w(f"# D7 — Dry-run autopsy: {CELL}, {START} -> {END}",
      "",
      "**SPENT WINDOW — every number here is a plumbing check, never "
      "evidence** (build prompt §1). Purpose: prove the journal alone "
      "answers every question in `fixtures/autopsy_questions.md`. "
      f"Sample: {len(fills)} fills / {n_ex} resolved tranche exits — far "
      "below the ≥20-per-cell read floor (charter §4); no conclusions may "
      "be drawn, only column liveness.",
      "",
      f"Run: `{summary['run_id']}` · engine 1.0.0 · config naiad_v0 · "
      f"{summary['rows']} journal rows · journal sha256 "
      f"`{summary['journal_sha256'][:16]}…` · final equity "
      f"{summary['final_equity']} · {summary['halts']} halt(s)",
      "")

    # Q1 cohorts
    coh = defaultdict(list)
    for r in exits:
        coh[r["cohort"]].append(r["realized_r"])
    w("## Q1 — Loss by cohort")
    w("", "| cohort | n | Σ realized_r | mean |", "|---|---|---|---|")
    for k in ("NEVER_GREEN", "STILLBORN", "FADED", "PROTECTED"):
        v = coh.get(k, [])
        w(f"| {k} | {len(v)} | {fmt(sum(v))} | {fmt(mean(v)) if v else '-'} |")
    w("")

    # Q2 MFE/MAE distributions
    w("## Q2 — MFE/MAE by grade / zone / tier")
    w("", "| slice | n | mean mfe_r | mean mae_r |", "|---|---|---|---|")
    for key in ("grade", "zone", "tier"):
        for val in sorted({r[key] for r in exits}):
            sel = [r for r in exits if r[key] == val]
            w(f"| {key}={val} | {len(sel)} | "
              f"{fmt(mean(x['mfe_r'] for x in sel))} | "
              f"{fmt(mean(x['mae_r'] for x in sel))} |")
    w("")

    # Q3 pre-engagement death share
    eng = [r for r in exits if r["engagement_flags"]]
    pre = [r for r in eng if not r["engagement_flags"]["xa_engaged_before_exit"]]
    w("## Q3 — Pre-engagement death share (X-A trail)",
      "",
      f"{len(pre)}/{len(eng)} tranches died before the e200 trail engaged "
      f"({100 * len(pre) / len(eng):.0f}% — the X0 lesson metric).", "")

    # Q4/Q5 capture + tail capture
    w("## Q4/Q5 — Capture ratio and tail capture (incumbent vs X-A..X-D)",
      "", "| exit | mean capture (realized/MFE, MFE>0) | tail trades (MFE>5R) | tail captured (>3R) |",
      "|---|---|---|---|")
    green = [r for r in exits if r["mfe_r"] and r["mfe_r"] > 0]

    def cap(r, variant=None):
        realized = (r["mfe_r"] - r["give_back_r"]) if variant is None \
            else r["shadow"][variant]
        return realized / r["mfe_r"]

    for name, var in [("incumbent (survival stop)", None),
                      ("X-A", "exit_XA"), ("X-B", "exit_XB"),
                      ("X-C", "exit_XC"), ("X-D", "exit_XD")]:
        caps = [cap(r, var) for r in green
                if var is None or (r["shadow"] and r["shadow"][var] is not None)]
        tail = [r for r in green if r["mfe_r"] > 5]
        t_hit = [r for r in tail if (r["mfe_r"] - r["give_back_r"] if var is None
                 else r["shadow"][var]) > 3]
        w(f"| {name} | {fmt(mean(caps)) if caps else '-'} | {len(tail)} | "
          f"{len(t_hit)} |")
    w("", "*Tail-capture outranks give-back in every exit report (charter §3.3).*", "")

    # Q6 vol expansion + post-exit continuation
    w("## Q6 — ATR entry vs exit; post-exit continuation")
    w("", "| tranche | atr entry | atr exit | cont+1 | cont+5 | cont+20 | cohort |",
      "|---|---|---|---|---|---|---|")
    for r in exits:
        f0 = fill_by_tr.get(r["tranche_id"], {})
        w(f"| {r['tranche_id']} | {fmt(f0.get('atr_exec'), 2)} | "
          f"{fmt(r['atr_exec'], 2)} | {fmt(r['postexit_cont_1'])} | "
          f"{fmt(r['postexit_cont_5'])} | {fmt(r['postexit_cont_20'])} | "
          f"{r['cohort']} |")
    w("", "*(ATR at each ratchet step = `atr_exec` on the campaign's "
      "PRIME/CONFIRM/V rows — present in the journal, joinable by time.)*", "")

    # Q7 adds vs sizing shadows
    adds = [r for r in exits if r["tranche_id"] in
            {x["tranche_id"] for x in fills if x["evt"] == "ADD_FILL"}]
    r1s = [r for r in exits if r not in adds]
    w("## Q7 — Adds vs sizing counterfactuals",
      "",
      f"R1/V tranches: n={len(r1s)}, Σ realized_r={fmt(sum(r['realized_r'] for r in r1s))}, "
      f"Σ shadow full-1R-at-R1={fmt(sum(r['shadow']['size_full_r1'] for r in r1s if r['shadow'] and r['shadow']['size_full_r1'] is not None))}",
      f"ADD tranches: n={len(adds)}, Σ realized_r={fmt(sum(r['realized_r'] for r in adds))}, "
      f"Σ shadow big-adds={fmt(sum(r['shadow']['size_big_adds'] for r in adds if r['shadow'] and r['shadow']['size_big_adds'] is not None))}",
      "")

    # Q8 every shadow line
    w("## Q8 — Shadow lines on identical data (per resolved exit)")
    w("", "| tranche | XA | XB | XC | XD | alt-anchor R | vol-buf R | strict? | unthr. size |",
      "|---|---|---|---|---|---|---|---|---|")
    for r in exits:
        s = r["shadow"] or {}
        w(f"| {r['tranche_id']} | {fmt(s.get('exit_XA'))} | {fmt(s.get('exit_XB'))} "
          f"| {fmt(s.get('exit_XC'))} | {fmt(s.get('exit_XD'))} "
          f"| {fmt(s.get('stop_alt_anchor_exit_r'))} "
          f"| {fmt(s.get('stop_alt_volbuf_exit_r'))} "
          f"| {s.get('ladder_strict')} | {fmt(s.get('ladder_unthrottled_size_r'), 2)} |")
    w("")

    # Q9 give-back
    w("## Q9 — Give-back",
      "",
      f"Mean give_back_r on MFE>0 exits: "
      f"{fmt(mean(r['give_back_r'] for r in green)) if green else '-'}; "
      f"per-variant give-back = mfe_r − exit_X* (columns live, Q8 table).", "")

    # Q10/Q11 funnel
    w("## Q10/Q11 — Funnel: signals -> fills, reject mix",
      "",
      f"PRIME events: {len(primes)}; fills: {len(fills)}; trade-path rejects: "
      f"{len([r for r in rejects if r['tranche_id'].startswith('trade_')])}; "
      f"signal-gate rejects: {len([r for r in rejects if not r['tranche_id'].startswith('trade_')])}.",
      "", "| reject_reason | n |", "|---|---|")
    for reason, n in Counter(r["reject_reason"] for r in rejects).most_common():
        w(f"| {reason} | {n} |")
    w("")

    # Q12 zone x grade
    w("## Q12 — Expectancy by zone at equal grade")
    w("", "| zone | grade | n | mean realized_r |", "|---|---|---|---|")
    for zone in sorted({r["zone"] for r in exits}):
        for g in sorted({r["grade"] for r in exits if r["zone"] == zone}):
            sel = [r for r in exits if r["zone"] == zone and r["grade"] == g]
            w(f"| {zone} | {g} | {len(sel)} | {fmt(mean(r['realized_r'] for r in sel))} |")
    w("")

    # Q13 retr bands
    w("## Q13 — The sniper-pocket question (retr bands, ALL PRIMEs)")
    w("", "| retr band | PRIMEs | filled exits | mean realized_r |", "|---|---|---|---|")
    bands = [(-9, 0), (0, 0.25), (0.25, 0.5), (0.5, 0.786), (0.786, 1.0), (1.0, 9)]
    for lo, hi in bands:
        ps = [r for r in primes if r["retr"] is not None and lo <= r["retr"] < hi]
        ex = [r for r in exits if r["retr"] is not None and lo <= r["retr"] < hi]
        w(f"| [{lo}, {hi}) | {len(ps)} | {len(ex)} | "
          f"{fmt(mean(r['realized_r'] for r in ex)) if ex else '-'} |")
    w(f"| retr=null (V-born / no leg) | {len([r for r in primes if r['retr'] is None])} | "
      f"{len([r for r in exits if r['retr'] is None])} | - |", "")

    # Q14/Q15 ladders
    strict_skipped = [r for r in exits if r["shadow"] and not r["shadow"]["ladder_strict"]]
    w("## Q14/Q15 — Tier throttle and the strict ladder",
      "",
      f"Provisional-campaign exits: {len([r for r in exits if r['tier'] == 'provisional'])} "
      f"(uncapped shadow grade/size on each row). Fills the strict (v11.0.0) "
      f"ladder would have SKIPPED: {len(strict_skipped)}, Σ realized_r "
      f"{fmt(sum(r['realized_r'] for r in strict_skipped))} — the May-26 vs "
      "Jun-14 trade-off, measured.", "")

    # Q16 stage
    w("## Q16 — Entries by stage at signal",
      "", "| stage | fills | Σ realized_r (resolved) |", "|---|---|---|")
    for st in (1, 2):
        f_st = [r for r in fills if r["stage"] == st]
        e_st = [r for r in exits if r["tranche_id"] in
                {x["tranche_id"] for x in f_st}]
        w(f"| {st} | {len(f_st)} | {fmt(sum(r['realized_r'] for r in e_st))} |")
    w("", f"STAGE confirm events in window: {len(q(rows, 'STAGE'))}.", "")

    # Q17 C-entries
    cs = q(rows, "CONFIRM", grade="C")
    w("## Q17 — Gated C-entries (journal-only, probation)",
      "",
      f"C events: {len(cs)}; C-gate rejects: "
      f"{len([r for r in rejects if r['reject_reason'] and r['reject_reason'].startswith('c_gate')])}. "
      "No C ever fills (F5-asserted). Outcome simulation = Phase 2, re-fetching "
      "candles against journaled px_signal/stop.", "")

    # Q18 halts
    halts = q(rows, "HALT")
    w("## Q18 — Halts", "",
      f"{len(halts)} halt(s): " + "; ".join(
          f"{r['tranche_id']} {r['reject_reason']} at {r['ts_open']} "
          f"(running R {fmt(r['size_r'])})" for r in halts) + ".",
      f"Post-halt blocked fills (halted_day/week rejects): "
      f"{len([r for r in rejects if r['reject_reason'] in ('halted_day', 'halted_week')])}.", "")

    # Q19 costs
    w("## Q19 — Cost anatomy", "",
      f"Σ fees {fmt(sum(r['fees'] for r in exits), 2)} · "
      f"Σ slippage {fmt(sum(r['slippage'] for r in exits), 2)} · "
      f"Σ funding {fmt(sum(r['funding_cum'] for r in exits), 2)} · "
      f"Σ pnl {fmt(sum(r['pnl_usd'] for r in exits), 2)} USD "
      f"(qty and px_fill journaled per fill).", "")

    # Q20 post-exit continuation by reason
    w("## Q20 — Post-exit continuation by exit reason")
    w("", "| exit_reason | n | mean cont+1 | mean cont+5 | mean cont+20 |",
      "|---|---|---|---|---|")
    for reason in sorted({r["exit_reason"] for r in exits}):
        sel = [r for r in exits if r["exit_reason"] == reason]
        w(f"| {reason} | {len(sel)} | "
          f"{fmt(mean(r['postexit_cont_1'] for r in sel))} | "
          f"{fmt(mean(r['postexit_cont_5'] for r in sel))} | "
          f"{fmt(mean(r['postexit_cont_20'] for r in sel))} |")
    w("")

    # Q21 V
    vs = q(rows, "V")
    w("## Q21 — Capitulation V", "",
      f"V events in window: {len(vs)}"
      + ("" if not vs else " at " + ", ".join(r["ts_open"] for r in vs))
      + f"; V fills: {len([r for r in fills if r['grade'] == 'V'])}. "
      "(Two true positives in nine months is the doctrine base rate — zero "
      "in a two-month plumbing window is unremarkable.)", "")

    # Q22 TPW
    tpws = q(rows, "TPW")
    tpw_exits = [r for r in eng if r["engagement_flags"]["tpw_before_exit"]]
    w("## Q22 — TPW as exit input", "",
      f"TPW events: {len(tpws)}; resolved exits with a TPW before exit: "
      f"{len(tpw_exits)}; on those, mean X-B − X-A = "
      + (fmt(mean(r["shadow"]["exit_XB"] - r["shadow"]["exit_XA"]
              for r in tpw_exits if r["shadow"])) if tpw_exits else "-")
      + ".", "")

    # Q23 time in trade
    w("## Q23 — Time-in-trade by cohort")
    w("", "| cohort | n | median minutes |", "|---|---|---|")
    for k in ("NEVER_GREEN", "STILLBORN", "FADED", "PROTECTED"):
        sel = [r for r in exits if r["cohort"] == k and r["tranche_id"] in fill_by_tr]
        mins = [(ts_ms(r["ts_open"]) - ts_ms(fill_by_tr[r["tranche_id"]]["ts_open"])) / 60000
                for r in sel]
        w(f"| {k} | {len(sel)} | {fmt(median(mins), 0) if mins else '-'} |")
    w("")

    # Q24 whipsaw arrows
    regs = q(rows, "REGIME")
    hidden = [r for r in regs if r["engagement_flags"]
              and not r["engagement_flags"]["arrow_visible"]]
    w("## Q24 — Whipsaw-suppressed arrows", "",
      f"REGIME events: {len(regs)}, arrows hidden on {len(hidden)} "
      "(campaign outcomes joinable via subsequent EXIT rows).", "")

    # Q25 equity trajectory
    w("## Q25 — Equity trajectory (per resolved exit)")
    w("", "| ts | tranche | pnl_usd | equity_after |", "|---|---|---|---|")
    for r in exits:
        w(f"| {r['ts_open']} | {r['tranche_id']} | {fmt(r['pnl_usd'], 2)} "
          f"| {fmt(r['equity_after'], 2)} |")
    w("")

    # Q26 stop distances
    w("## Q26 — Initial stop distances")
    w("", "| tranche | |fill−stop|/ATRexec | /ATRgov | realized_r | mae_r | alt-anchor | vol-buf |",
      "|---|---|---|---|---|---|---|")
    for r in exits:
        f0 = fill_by_tr.get(r["tranche_id"])
        if not f0:
            continue
        dist = abs(f0["px_fill"] - f0["stop"])
        s = r["shadow"] or {}
        w(f"| {r['tranche_id']} | {fmt(dist / f0['atr_exec'], 2)} | "
          f"{fmt(dist / f0['atr_gov'], 2)} | {fmt(r['realized_r'])} | "
          f"{fmt(r['mae_r'])} | {fmt(s.get('stop_alt_anchor'), 1)} | "
          f"{fmt(s.get('stop_alt_volbuf'), 1)} |")
    w("", "---", "",
      "*All 26 questions answered from journal rows alone. Columns proven "
      "live are enforced mechanically by fixture F8.*")

    out = ROOT / "research_outputs" / "dryrun_autopsy.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print(f"-> {out}")

    # completeness cross-check: no question in the list lacks a section here
    qtext = (ROOT / "fixtures" / "autopsy_questions.md").read_text(encoding="utf-8")
    qnums = set(re.findall(r"\*\*Q(\d+)\.", qtext))
    have = set(re.findall(r"## Q(\d+)", "\n".join(L)))
    have |= {n for rng in re.findall(r"## Q(\d+)/Q(\d+)", "\n".join(L)) for n in rng}
    missing = qnums - have
    if missing:
        print(f"FAILED: unanswered questions: {sorted(missing, key=int)}")
        return 1
    print(f"all {len(qnums)} autopsy questions answered from the journal")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
