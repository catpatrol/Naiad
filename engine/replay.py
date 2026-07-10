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


def run_replay(config_id: str, cell_id: str, start: str, end: str,
               journal_root: Path, backfill: bool = False, log=print) -> dict:
    cfg = load_config(config_id)
    cell = cell_by_id(cell_id)
    start_ms, end_ms = parse_utc(start), parse_utc(end)
    if end_ms <= start_ms:
        raise ValueError("end must be after start")
    run_id = make_run_id(config_id, cell_id, start, end)

    data = load_cell_data(cell, start_ms, end_ms, backfill=backfill, log=log)
    assert_warmup(cell, data, start_ms)

    sig = compute_signals(
        cell, cfg["signal"], data[cell.tf_exec], data[cell.tf_gov],
        {tf: data[tf] for tf in MTF_SET},
        v_births_provisional=cfg["signal"]["v_births_provisional"])

    trades = run_trading(cell, cfg, sig, data["funding"], start_ms=start_ms)

    base = dict(run_id=run_id, engine_version=ENGINE_VERSION,
                config_id=config_id, cell_id=cell.cell_id, symbol=cell.symbol,
                tf_gov=cell.tf_gov, tf_exec=cell.tf_exec)
    open_ms = sig.exec_open_ms
    exec_step = INTERVAL_MS[cell.tf_exec]
    in_window = lambda i: start_ms <= int(open_ms[i]) <= end_ms

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
            **base, ts_open=ts_open, ts_close=ts_close, evt=ev.evt,
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

        for tr in trades.tranches:
            if in_window(tr.fill_i):
                ts_open, ts_close = bar_times(tr.fill_i)
                rows.append(make_row(
                    **base, ts_open=ts_open, ts_close=ts_close,
                    evt="ENTRY_FILL" if tr.kind in ("R1", "V") else "ADD_FILL",
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
                    **base, ts_open=ts_open, ts_close=ts_close, evt="EXIT",
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
    }
