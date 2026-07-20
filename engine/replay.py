"""Replay orchestration: data -> signals -> trading -> shadows -> journal.

One engine, every mode (charter §10): scripts/replay.py and scripts/tick.py
both call run_replay(); tick just picks a rolling window and commits the
journal to the data branch. Identical fill model, identical gates.

Warm-up (F7): a replay REFUSES to emit signals unless >= 2000 exec bars AND
>= 200 governor bars of history precede the window. Independently of that
floor, indicators are computed from a deterministic warm-up anchor well
before the window (~1000 governor bars, floored to a UTC month boundary) so
EMA seeding effects stay far inside the F6 parity tolerance and the anchor
never slides between overlapping runs (idempotent journal merges).

Emission window: journal rows are written for events with open time inside
[start, end]. The paper book starts flat at --start; warm-up bars drive the
state machine but are never journaled and never traded.
"""

import os
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from engine import data as dl
from engine.cells import INTERVAL_MS, MTF_SET, Cell, cell_by_id
from engine.config import load_config, make_run_id
from engine.journal import (count_lines, files_sha256, iso, make_row,
                            write_journal)
from engine.shadows import build_shadow_context, enrich_tranche
from engine.signals import compute_signals
from engine.trading import run_trading
from engine.version import ENGINE_VERSION


class WarmupError(RuntimeError):
    """F7: not enough history precedes the requested window."""


class LockboxViolation(RuntimeError):
    """G-1 (engine 1.0.9): the replay path refuses any run whose requested
    [start, end] window intersects the sealed lockbox. Warm-up traversal
    (loading history before `start`) is not emission and is not gated here;
    journal rows can only carry open times inside [start, end]."""


# Sealed holdout (v3_anchor manifest partitions, registered G-1).
LOCKBOX_START_MS = 1_719_792_000_000   # 2024-07-01T00:00:00Z
LOCKBOX_END_MS = 1_759_708_799_000     # 2025-10-05T23:59:59Z


def parse_utc(s: str) -> int:
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%SZ"):
        try:
            return int(datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
                       .timestamp() * 1000)
        except ValueError:
            continue
    raise ValueError(f"unparseable UTC time: {s}")


def month_floor_ms(ms: int) -> int:
    d = datetime.fromtimestamp(ms / 1000, timezone.utc)
    return int(d.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
               .timestamp() * 1000)


def warmup_anchor_ms(cell: Cell, start_ms: int) -> int:
    """Deterministic in (cell, start) only — never slides with `end`, so a
    truncated run is a byte-prefix of a longer one (F2)."""
    need = max(2000 * INTERVAL_MS[cell.tf_exec], 1000 * INTERVAL_MS[cell.tf_gov])
    return month_floor_ms(start_ms - need - 35 * 86_400_000)


def load_cell_data(cell: Cell, start_ms: int, end_ms: int,
                   backfill: bool = False, log=print) -> dict:
    anchor = warmup_anchor_ms(cell, start_ms)
    tfs = sorted({cell.tf_exec, cell.tf_gov, *MTF_SET})
    out = {}
    for tf in tfs:
        if backfill:
            out[tf] = dl.backfill_klines(cell.symbol, tf, anchor, end_ms, log=log)
        else:
            out[tf] = dl.load_klines(cell.symbol, tf, anchor, end_ms)
    if backfill:
        out["funding"] = dl.backfill_funding(cell.symbol, anchor, end_ms, log=log)
    else:
        out["funding"] = dl.load_funding(cell.symbol, anchor, end_ms)
    return out


def assert_warmup(cell: Cell, data: dict, start_ms: int) -> None:
    exec_bars = int((data[cell.tf_exec]["open_time"] < start_ms).sum())
    gov_bars = int((data[cell.tf_gov]["open_time"] < start_ms).sum())
    if exec_bars < 2000 or gov_bars < 200:
        raise WarmupError(
            f"{cell.cell_id}: warm-up floor not met before "
            f"{iso(start_ms)} — {exec_bars} exec bars (need >= 2000), "
            f"{gov_bars} governor bars (need >= 200). Refusing to emit signals.")


def _tc1_arch_data(cell, cfg, sig, data) -> dict | None:
    """TC-1 (engine 1.0.11): governor e200 (exec-mapped) + confirmed 1h
    (5,5) pivots for the structural stop / gov-e200 trail. Computed only when
    an architecture config key is present; None on baseline configs (so cell
    A's run_trading receives arch_data=None and takes the baseline path)."""
    t = cfg["trading"]
    if t.get("stop_mode", "native") == "native" and \
            t.get("exit_trail", "none") == "none":
        return None
    from engine import indicators as ind
    from engine.htf import map_htf_to_exec, take
    from engine.s1 import _pivots
    p = cfg["signal"]
    # cell's governor e200, mapped to exec (confirmed-HTF rule)
    gov = data[cell.tf_gov]
    ge200 = ind.ema(gov["close"].to_numpy(float), p["len_trend"])
    gidx = map_htf_to_exec(sig.exec_open_ms,
                           gov["open_time"].to_numpy(np.int64), cell.tf_gov)
    gov_e200 = take(ge200, gidx)
    # 1h frame confirmed (5,5) pivots
    oneh = data["1h"]
    idx1h = map_htf_to_exec(sig.exec_open_ms,
                            oneh["open_time"].to_numpy(np.int64), "1h")
    lc, lv = _pivots(oneh["low"].to_numpy(float), 5, 5, low=True)
    hc, hv = _pivots(oneh["high"].to_numpy(float), 5, 5, low=False)
    # conf_exec = first exec bar whose mapped 1h index reaches the pivot's
    # confirmation 1h bar (pivot+5); pivot's own 1h bar = conf - 5.
    plow_conf = np.searchsorted(idx1h, lc, side="left")
    phigh_conf = np.searchsorted(idx1h, hc, side="left")
    return {
        "gov_e200": gov_e200, "exec_1h": idx1h,
        "plow_conf": plow_conf.astype(np.int64),
        "plow_1h": (lc - 5).astype(np.int64), "plow_val": lv,
        "phigh_conf": phigh_conf.astype(np.int64),
        "phigh_1h": (hc - 5).astype(np.int64), "phigh_val": hv,
    }


def run_replay(config_id: str, cell_id: str, start: str, end: str,
               journal_root: Path, backfill: bool = False, log=print,
               s1_sidecar_root: Path | None = None,
               s1_resampled_dir: Path | None = None,
               s2_sidecar_root: Path | None = None,
               s2_resampled_dir: Path | None = None) -> dict:
    cfg = load_config(config_id)
    cell = cell_by_id(cell_id)
    start_ms, end_ms = parse_utc(start), parse_utc(end)
    if end_ms <= start_ms:
        raise ValueError("end must be after start")
    # G-1 (1.0.9): no emission window may touch the sealed lockbox.
    if start_ms <= LOCKBOX_END_MS and end_ms >= LOCKBOX_START_MS \
            and not os.environ.get("NAIAD_LOCKBOX_ACK"):
        raise LockboxViolation(
            f"requested window [{start}, {end}] intersects the sealed "
            "lockbox [2024-07-01T00:00:00Z, 2025-10-05T23:59:59Z]; "
            "unlocking is an operator act (NAIAD_LOCKBOX_ACK).")
    run_id = make_run_id(config_id, cell_id, start, end)

    data = load_cell_data(cell, start_ms, end_ms, backfill=backfill, log=log)
    assert_warmup(cell, data, start_ms)

    sig = compute_signals(
        cell, cfg["signal"], data[cell.tf_exec], data[cell.tf_gov],
        {tf: data[tf] for tf in MTF_SET},
        v_births_provisional=cfg["signal"]["v_births_provisional"])

    arch_data = _tc1_arch_data(cell, cfg, sig, data)
    trades = run_trading(cell, cfg, sig, data["funding"], start_ms=start_ms,
                         arch_data=arch_data)

    base = dict(run_id=run_id, engine_version=ENGINE_VERSION,
                config_id=config_id, cell_id=cell.cell_id, symbol=cell.symbol,
                tf_gov=cell.tf_gov, tf_exec=cell.tf_exec)
    open_ms = sig.exec_open_ms
    exec_step = INTERVAL_MS[cell.tf_exec]
    in_window = lambda i: start_ms <= int(open_ms[i]) <= end_ms

    # ── S-1 instrumentation (1.0.9, measure-only). Computed AFTER the
    # trading pass, attached to rows the replay was already going to emit —
    # emission neutrality is structural, F-BYTE enforces it behaviorally. ──
    s1res = None
    if s1_sidecar_root is not None:
        from engine.s1 import compute_s1
        s1res = compute_s1(cell, cfg, sig, trades, data, s1_resampled_dir,
                           in_window)
    s2res = None
    if s2_sidecar_root is not None:
        from engine.s2 import compute_s2
        s2res = compute_s2(cell, cfg, sig, trades, data, s2_resampled_dir,
                           in_window)

    def s2_sig(ev):
        if s2res is None:
            return {}
        v = s2res["sig_s2"].get((ev.i, ev.evt, ev.dir, ev.subkey))
        return {"s2": v} if v is not None else {}

    def s2_fill(tr):
        if s2res is None:
            return {}
        v = s2res["fill_s2"].get(tr.tranche_id)
        return {"s2": v} if v is not None else {}

    def s2_exit(tr):
        if s2res is None:
            return {}
        v = s2res["exit_s2"].get(tr.tranche_id)
        return {"s2": v} if v is not None else {}

    def s1_sig(ev):
        if s1res is None:
            return {}
        if ev.evt in ("PRIME", "CONFIRM") or \
                (ev.evt == "REJECT" and ev.subkey in ("prime", "confirm")):
            z = s1res["zone_s1"].get(ev.i)
            if z is not None:
                return {"s1": {"zone": z}}
        return {}

    def s1_fill(tr):
        if s1res is None:
            return {}
        v = s1res["fill_s1"].get(tr.tranche_id)
        return {"s1": v} if v is not None else {}

    def s1_exit(tr):
        if s1res is None:
            return {}
        v = s1res["exit_s1"].get(tr.tranche_id)
        return {"s1": v} if v is not None else {}

    def bar_times(i):
        return iso(int(open_ms[i])), iso(int(open_ms[i]) + exec_step)

    def f(x, nd=8):
        if x is None or (isinstance(x, float) and np.isnan(x)):
            return None
        return round(float(x), nd) + 0.0  # +0.0 normalizes -0.0

    rows = []
    # ── signal events (all configs) ──
    for ev in sig.events:
        if not in_window(ev.i):
            continue
        ts_open, ts_close = bar_times(ev.i)
        rows.append(make_row(
            **base, **s1_sig(ev), **s2_sig(ev),
            ts_open=ts_open, ts_close=ts_close, evt=ev.evt,
            dir="long" if ev.dir == 1 else "short" if ev.dir == -1 else "-",
            tier=ev.tier, grade=ev.grade, rc=ev.rc, zone=ev.zone,
            stage=ev.stage, retr=f(ev.retr, 6), px_signal=f(sig.c[ev.i]),
            stop=f(ev.stop), atr_exec=f(sig.atr_x[ev.i]),
            atr_gov=f(sig.g_atr[ev.i]),
            tranche_id=ev.subkey, reject_reason=ev.reject_reason,
            # REGIME rows record the whipsaw filter's arrow visibility so the
            # operator can match TradingView's chart (arrows only — arming is
            # unaffected).
            engagement_flags=({"arrow_visible": ev.arrow_visible}
                              if ev.evt == "REGIME" else None)))

    trading_enabled = cfg["trading"].get("enabled", False)
    if trading_enabled:
        sh_cfg = cfg.get("shadows", {})
        shadows_on = sh_cfg.get("enabled", False)
        entry_bars, rib_cross = (build_shadow_context(sig, trades)
                                 if shadows_on else ({}, {}))
        stop_buf = cfg["signal"]["stop_buf_atr"]

        # 1.0.8 (TC-4, additive): concurrency + fill class, per the RC
        # definition — same-bar same-campaign siblings count; an earlier
        # sibling counts iff still open strictly past this fill's bar.
        # Evaluated on engine truth (a tranche whose EXIT row is buffered at
        # data end still counts by its true exit bar; one still open at data
        # end counts as open).
        camp_members: dict[int, list] = {}
        for tr in trades.tranches:
            camp_members.setdefault(tr.campaign, []).append(tr)
        conc_at_fill: dict[str, int] = {}
        for members in camp_members.values():
            for a in members:
                conc = 0
                for b in members:
                    if b is a:
                        continue
                    if b.fill_i == a.fill_i:
                        conc += 1
                    elif b.fill_i < a.fill_i and \
                            (not b.exited or b.exit_i > a.fill_i):
                        conc += 1
                conc_at_fill[a.tranche_id] = conc

        for tr in trades.tranches:
            if in_window(tr.fill_i):
                ts_open, ts_close = bar_times(tr.fill_i)
                conc = conc_at_fill[tr.tranche_id]
                rows.append(make_row(
                    **base, **s1_fill(tr), **s2_fill(tr),
                    ts_open=ts_open, ts_close=ts_close,
                    evt="ENTRY_FILL" if tr.kind in ("R1", "V") else "ADD_FILL",
                    concurrent_open_at_fill=conc,
                    fill_class=("r1" if tr.kind == "R1" else
                                "v" if tr.kind == "V" else
                                "true_add" if conc >= 1 else "re_entry"),
                    dir="long" if tr.dir == 1 else "short",
                    tier=tr.tier, grade=tr.grade, rc=tr.rc, zone=tr.zone,
                    stage=int(sig.stage[tr.signal_i]), retr=f(tr.retr, 6),
                    px_signal=f(sig.c[tr.signal_i]), px_fill=f(tr.fill_px),
                    stop=f(tr.stop_at_entry), atr_exec=f(sig.atr_x[tr.signal_i]),
                    atr_gov=f(sig.g_atr[tr.signal_i]),
                    tranche_id=tr.tranche_id, size_r=tr.size_r,
                    qty=f(tr.qty, 8),
                    fees=f(abs(tr.fill_px * tr.qty) * cfg["trading"]["fee_bps_side"] / 1e4, 6),
                    slippage=f(abs(tr.fill_px - tr.raw_px) * tr.qty, 6)))
            if tr.exited and in_window(tr.exit_i):
                ts_open, ts_close = bar_times(tr.exit_i)
                if tr.exit_reason in ("stop", "stop_gap"):
                    # fills need no enrichment — emit immediately
                    rows.append(make_row(
                        **base, ts_open=ts_open, ts_close=ts_close,
                        evt="STOP_FILL",
                        dir="long" if tr.dir == 1 else "short",
                        tier=tr.tier, grade=tr.grade, rc=tr.rc,
                        px_fill=f(tr.exit_px), stop=f(tr.exit_raw_px),
                        atr_exec=f(sig.atr_x[tr.exit_i]),
                        atr_gov=f(sig.g_atr[tr.exit_i]),
                        tranche_id=tr.tranche_id, size_r=tr.size_r,
                        exit_reason=tr.exit_reason))
                enr = (enrich_tranche(sig, tr, sh_cfg, stop_buf, entry_bars,
                                      rib_cross) if shadows_on else None)
                if enr is not None and not enr.resolved:
                    continue  # EXIT buffered: a later (longer) run emits it
                rows.append(make_row(
                    **base, **s1_exit(tr), **s2_exit(tr),
                    ts_open=ts_open, ts_close=ts_close, evt="EXIT",
                    dir="long" if tr.dir == 1 else "short",
                    tier=tr.tier, grade=tr.grade, rc=tr.rc, zone=tr.zone,
                    retr=f(tr.retr, 6), px_fill=f(tr.exit_px),
                    stop=f(tr.exit_raw_px if tr.exit_reason.startswith("stop") else None),
                    atr_exec=f(sig.atr_x[tr.exit_i]), atr_gov=f(sig.g_atr[tr.exit_i]),
                    tranche_id=tr.tranche_id, size_r=tr.size_r,
                    qty=f(tr.qty, 8),
                    fees=f(tr.fees, 6), funding_cum=f(tr.funding, 6),
                    slippage=f(tr.slippage_usd, 6),
                    pnl_usd=f(tr.pnl_usd, 6), realized_r=f(tr.realized_r, 6),
                    equity_after=f(tr.equity_after, 2),
                    mfe_r=enr.mfe_r if enr else None,
                    mae_r=enr.mae_r if enr else None,
                    give_back_r=enr.give_back_r if enr else None,
                    postexit_cont_1=enr.postexit_cont_1 if enr else None,
                    postexit_cont_5=enr.postexit_cont_5 if enr else None,
                    postexit_cont_20=enr.postexit_cont_20 if enr else None,
                    exit_reason=tr.exit_reason,
                    cohort=enr.cohort if enr else None,
                    engagement_flags=enr.engagement_flags if enr else None,
                    shadow=enr.shadow if enr else None))

        for hv in trades.halts:
            if in_window(hv.i):
                ts_open, ts_close = bar_times(hv.i)
                rows.append(make_row(
                    **base, ts_open=ts_open, ts_close=ts_close, evt="HALT",
                    dir="-", tranche_id=hv.scope, size_r=round(hv.r_total, 6),
                    # namespaced (ticket D-2): never a bare date in an
                    # enum-like field
                    reject_reason=f"halt_{hv.scope}:{hv.key}"))

        for rj in trades.rejects:
            if in_window(rj.i):
                ts_open, ts_close = bar_times(rj.i)
                rows.append(make_row(
                    **base, ts_open=ts_open, ts_close=ts_close, evt="REJECT",
                    dir="long" if rj.dir == 1 else "short",
                    # engine 1.0.1: subkey carries the signal family so
                    # same-bar rejects of different families never collide
                    tranche_id=f"trade_{rj.kind}_{rj.family}",
                    reject_reason=rj.reason))

    written = write_journal(rows, journal_root)
    sidecar_sha = sidecar_rows = None
    if s1res is not None:
        from engine.s1 import write_sidecar
        sidecar_rows = len(s1res["sidecar"])
        sidecar_sha = write_sidecar(
            s1res["sidecar"], s1_sidecar_root / f"{cell.cell_id}.jsonl",
            cell.cell_id, base)
    if s2res is not None:
        from engine.s1 import write_sidecar
        sidecar_rows = len(s2res["sidecar"])
        sidecar_sha = write_sidecar(
            s2res["sidecar"], s2_sidecar_root / f"{cell.cell_id}.jsonl",
            cell.cell_id, base)
    # Summary metrics come from the PERSISTED bytes, re-read after writing
    # (reviewer ticket D-1) — never from the in-memory stream: same-bar
    # same-kind events can share a journal key and merge to one row.
    return {
        "run_id": run_id,
        "rows": count_lines(written),
        "files": [str(p) for p in written],
        "journal_sha256": files_sha256(written),
        "signal_events": sum(1 for ev in sig.events if in_window(ev.i)),
        "tranches": len(trades.tranches) if trading_enabled else 0,
        "final_equity": round(trades.final_equity, 2) if trading_enabled else None,
        "halts": len(trades.halts) if trading_enabled else 0,
        "sidecar_rows": sidecar_rows,
        "sidecar_sha256": sidecar_sha,
    }
