"""Trading layer — naiad_v0 only (build prompt §6).

Chronology per exec bar i (the "wake"):
  1. stop-guarantee-and-repair FIRST: verify the working stop for every open
     tranche exists and matches the ratchet (charter §3.1).
  2. Funding due at this bar's open accrues to tranches opened earlier.
  3. Fills at the OPEN: flattens (X / opposite cross / V-reversal) first, then
     gap-through stop exits, then pending entries (halt-gated at fill time).
  4. Intra-bar stop check: fill at the stop price, or at the open when gapped
     through (invariant 3).
  5. At the CLOSE: MFE/MAE update, then this bar's signal events become
     pending actions for bar i+1 — gate-checked, with funnel REJECT rows for
     everything that fails a gate, and independent in-path assertions (F5)
     that the traded set equals the eligible set.

Risk rails (invariant 6): per-cell halts at -2R/day and -4R/week (UTC
calendar; FLAGGED DECISION #1 default), sizing table charter §3.4, <=3
tranches, open campaign risk <= 1R asserted in-path.

Accounting decisions (flagged in the Phase 1 summary):
- equity = realized book value (initial + closed-tranche PnL); 1R = 0.5% of
  equity at fill time.
- funding accrues per tranche at each funding timestamp on qty x last closed
  price, realized into PnL at exit.
- realized_r = net PnL / 1R$ at entry; halts sum realized_r by UTC day/week
  of the exit fill.
- an R2+ PRIME while flat mid-campaign trades as an ADD (0.5R): the add
  eligibility clause is vacuously true with no open tranches, and the May-26
  marquee signature requires post-stopout re-entries to trade. CONFIRM adds
  require an open position (charter: "while positioned").
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone

import numpy as np

from engine.cells import Cell
from engine.signals import SignalEvent, SignalResult


class GateViolation(AssertionError):
    """An in-path gate assertion failed — the build is wrong (F5)."""


@dataclass
class Tranche:
    tranche_id: str
    campaign: int
    dir: int
    kind: str                 # R1 | ADD | V
    grade: str
    tier: str
    zone: str
    retr: float | None
    rc: int
    signal_i: int
    fill_i: int
    raw_px: float
    fill_px: float
    qty: float
    stop_at_entry: float
    one_r_usd: float
    size_r: float
    grade_uncapped: str
    born_aligned: bool
    fees: float = 0.0
    funding: float = 0.0
    slippage_usd: float = 0.0
    peak: float = np.nan      # favorable price extreme since fill
    trough: float = np.nan    # adverse price extreme since fill
    exited: bool = False
    exit_i: int | None = None
    exit_px: float | None = None
    exit_raw_px: float | None = None
    exit_reason: str | None = None
    pnl_usd: float = 0.0
    realized_r: float = 0.0
    equity_after: float = 0.0        # cell equity after this exit realized
    first_tpw_i: int | None = None   # first TPW after fill (shadow exits)


@dataclass
class PendingEntry:
    kind: str
    family: str               # prime | confirm | v — journal reject subkeys
    dir: int
    size_r: float
    grade: str
    tier: str
    zone: str
    retr: float | None
    rc: int
    signal_i: int
    stop_at_signal: float
    grade_uncapped: str
    born_aligned: bool
    campaign: int


@dataclass
class TradeReject:
    i: int
    reason: str
    kind: str
    family: str               # prime | confirm | v (engine 1.0.1): same-bar
    dir: int                  # rejects of different families never collide


@dataclass
class HaltEvent:
    i: int
    scope: str        # "day" | "week"
    key: str          # the UTC day / ISO week that halted
    r_total: float


@dataclass
class TradeResult:
    tranches: list[Tranche] = field(default_factory=list)
    rejects: list[TradeReject] = field(default_factory=list)
    halts: list[HaltEvent] = field(default_factory=list)
    final_equity: float = 0.0
    campaign_born_aligned: dict = field(default_factory=dict)


def _day_key(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%d")


def _week_key(ms: int) -> str:
    d = datetime.fromtimestamp(ms / 1000, timezone.utc).isocalendar()
    return f"{d.year}-W{d.week:02d}"


def admit_entry(pe: PendingEntry) -> PendingEntry | None:
    """The final gate an eligible entry passes before joining the pending
    queue. Production behavior: pass-through. Exists so F5 can install a
    deliberately broken gate (a test double that admits ineligible entries)
    and prove the independent in-path fill assertions fail loudly."""
    return pe


def size_for(kind: str, grade: str, tier: str, t: dict) -> float:
    """Charter §3.4 sizing table, as amended at ratification."""
    if kind == "ADD":
        return t["size_add"]
    if kind == "V":
        return t["size_v"]
    # R1 PRIME
    if tier == "provisional":
        return t["size_r1_provisional"]
    if grade in ("A+", "A"):
        return t["size_r1_a_full"]
    return t["size_r1_b_full"]


def run_trading(cell: Cell, cfg: dict, sig: SignalResult,
                funding_df, start_ms: int = 0) -> TradeResult:
    """start_ms: the paper book starts FLAT at the window start — warm-up
    bars drive the signal state machine but are never traded (F7)."""
    t = cfg["trading"]
    if not t.get("enabled", False):
        return TradeResult(final_equity=0.0)
    if t["halt_scope"] != "per_cell":
        raise NotImplementedError(
            "halt_scope=portfolio is a reserved config flag (FLAGGED DECISION "
            "#1); Phase 1 implements the per-cell default.")

    n = len(sig.c)
    o, h, l, c = sig.o, sig.h, sig.l, sig.c
    open_ms = sig.exec_open_ms
    slip = cell.slippage_bps / 10_000.0
    fee = t["fee_bps_side"] / 10_000.0
    r_pct = t["r_pct"]
    max_tranches = t["max_tranches"]
    max_risk_r = t["max_open_campaign_risk_r"]

    # Binance funding timestamps jitter by a few ms past the hour
    # (e.g. 16:00:00.012) — floor to the hour so they land on the exec bar
    # that OPENS at the funding time; rates on the same hour sum defensively.
    funding_by_ms: dict[int, float] = {}
    if funding_df is not None and len(funding_df):
        for ft, fr in zip(funding_df["funding_time"].astype(np.int64),
                          funding_df["funding_rate"].astype(float)):
            key = int(ft) // 3_600_000 * 3_600_000
            funding_by_ms[key] = funding_by_ms.get(key, 0.0) + fr

    events_by_bar: dict[int, list[SignalEvent]] = {}
    for ev in sig.events:
        events_by_bar.setdefault(ev.i, []).append(ev)

    res = TradeResult()
    equity = t["initial_equity"]
    open_tranches: list[Tranche] = []
    pending_entries: list[PendingEntry] = []
    pending_flatten: str | None = None    # reason, set at close of prior bar
    day_r: dict[str, float] = {}
    week_r: dict[str, float] = {}
    halted_days: set[str] = set()
    halted_weeks: set[str] = set()
    tranche_seq = 0
    campaign_tranche_count: dict[int, int] = {}

    # Track campaign births for the strict-ladder shadow.
    for ev in sig.events:
        if ev.evt == "REGIME":
            res.campaign_born_aligned[int(sig.campaign_id[min(ev.i + 1, n - 1)])] = \
                ev.tier == "full"
        elif ev.evt == "V":
            res.campaign_born_aligned.setdefault(
                int(sig.campaign_id[min(ev.i + 1, n - 1)]), False)

    def stop_level(i: int, d: int) -> float:
        """The working stop order during bar i = ratchet confirmed at i-1."""
        if i == 0:
            return np.nan
        return sig.stop_long[i - 1] if d == 1 else sig.stop_short[i - 1]

    def close_tranche(tr: Tranche, i: int, raw_px: float, reason: str):
        nonlocal equity
        px = raw_px * (1 - slip) if tr.dir == 1 else raw_px * (1 + slip)
        exit_fee = abs(px * tr.qty) * fee
        tr.fees += exit_fee
        tr.slippage_usd += abs(px - raw_px) * tr.qty
        tr.exited = True
        tr.exit_i = i
        tr.exit_px = px
        tr.exit_raw_px = raw_px
        tr.exit_reason = reason
        tr.pnl_usd = (px - tr.fill_px) * tr.qty * tr.dir - tr.fees - tr.funding
        tr.realized_r = tr.pnl_usd / tr.one_r_usd
        equity += tr.pnl_usd
        tr.equity_after = equity
        dk, wk = _day_key(open_ms[i]), _week_key(open_ms[i])
        day_r[dk] = day_r.get(dk, 0.0) + tr.realized_r
        week_r[wk] = week_r.get(wk, 0.0) + tr.realized_r

    def check_halts(i: int):
        nonlocal pending_entries
        dk, wk = _day_key(open_ms[i]), _week_key(open_ms[i])
        if day_r.get(dk, 0.0) <= t["halt_day_r"] and dk not in halted_days:
            halted_days.add(dk)
            res.halts.append(HaltEvent(i, "day", dk, day_r[dk]))
            pending_entries = []          # F4: nothing pending survives a halt
        if week_r.get(wk, 0.0) <= t["halt_week_r"] and wk not in halted_weeks:
            halted_weeks.add(wk)
            res.halts.append(HaltEvent(i, "week", wk, week_r[wk]))
            pending_entries = []

    def open_risk_r(stop: float, extra=None) -> float:
        """Open campaign risk in R against a given stop level."""
        total = 0.0
        items = list(open_tranches) + ([extra] if extra else [])
        for tr in items:
            if tr.qty <= 0:
                continue
            risk = max(0.0, (tr.fill_px - stop) * tr.dir) * tr.qty
            total += risk / tr.one_r_usd
        return total

    def assert_entry_legal(pe: PendingEntry, i: int, fill_px: float,
                           qty: float, one_r: float):
        """Independent in-path gate assertions (F5) — deliberately NOT the
        same code that admitted the entry; a broken gate fails loudly here."""
        if pe.grade == "C":
            raise GateViolation("C-grade signal reached a fill — C never trades")
        if campaign_tranche_count.get(pe.campaign, 0) >= max_tranches:
            raise GateViolation("tranche cap breached in-path")
        dk, wk = _day_key(open_ms[i]), _week_key(open_ms[i])
        if dk in halted_days or wk in halted_weeks:
            raise GateViolation("entry filled during an active halt")
        if pe.kind == "ADD" and open_tranches:
            stop_now = stop_level(i, pe.dir)
            for tr in open_tranches:
                # 1.0.6 (G-5, ruled): the breakeven doctrine sequences adds
                # across signal events — within-wake siblings (fill_i == i)
                # do not breakeven-test each other (a just-filled sibling
                # sits above the standing ratchet by construction). Full
                # force retained against all earlier-bar tranches.
                if tr.fill_i < i and (tr.fill_px - stop_now) * tr.dir > 1e-9:
                    raise GateViolation("add filled with a prior tranche below breakeven")
        probe = Tranche("probe", pe.campaign, pe.dir, pe.kind, pe.grade,
                        pe.tier, pe.zone, pe.retr, pe.rc, pe.signal_i, i,
                        fill_px, fill_px, qty, pe.stop_at_signal, one_r,
                        pe.size_r, pe.grade_uncapped, pe.born_aligned)
        if open_risk_r(pe.stop_at_signal, extra=probe) > max_risk_r + 1e-9:
            raise GateViolation("open campaign risk exceeds 1R in-path")

    for i in range(n):
        if open_ms[i] < start_ms:
            continue  # warm-up: state machine only, no book, no ledgers

        # 0. Campaign-death net (1.0.5, G-4; design ruling of 2026-07-13).
        # The signals arming block re-arms on every exec bar of the
        # cross-visibility window (Pine-literal), so a counter-window V
        # campaign can be silently overwritten one bar after birth — dir
        # flips, the dying side's stop clears, and NO X / REGIME / V event
        # fires. The book follows the campaign: a direction mismatch at the
        # prior close with no event-queued flatten exits at THIS open,
        # uniform with the three event-based death modes. Event-queued
        # flattens keep their reasons (failure_x / opposite_cross /
        # v_reversal); this net never overrides them.
        if open_tranches and pending_flatten is None \
                and sig.dir[i - 1] != open_tranches[0].dir:
            pending_flatten = "campaign_died"

        # 1. Stop-guarantee-and-repair (first action of every wake).
        # 1.0.4 (G-3): the one-bar death transition is exempt — signals clear
        # the dying side's ratchet ON the death bar (opposite cross / X /
        # V-reversal) and the flatten is already queued for THIS wake's open
        # (step 3a). A NaN stop with NO queued flatten stays a hard failure.
        if open_tranches and pending_flatten is None:
            d = open_tranches[0].dir
            if np.isnan(stop_level(i, d)):
                raise GateViolation(
                    f"bar {i}: open tranche(s) with no working stop — "
                    "stop-guarantee-and-repair failed")

        # 2. Funding due at this bar's open (positions opened earlier pay).
        rate = funding_by_ms.get(int(open_ms[i]))
        if rate is not None and i > 0:
            for tr in open_tranches:
                if tr.fill_i < i:
                    tr.funding += rate * tr.qty * c[i - 1] * tr.dir

        # 3a. Flatten fills (X / opposite cross / V-reversal) at the open.
        if pending_flatten is not None and open_tranches:
            for tr in list(open_tranches):
                close_tranche(tr, i, o[i], pending_flatten)
            open_tranches.clear()
            check_halts(i)
        pending_flatten = None

        # 3b. Gap-through stop exits at the open.
        if open_tranches:
            d = open_tranches[0].dir
            stop = stop_level(i, d)
            if not np.isnan(stop) and (o[i] - stop) * d <= 0:
                for tr in list(open_tranches):
                    close_tranche(tr, i, o[i], "stop_gap")
                open_tranches.clear()
                check_halts(i)

        # 3c. Entry fills at the open (halt-gated at fill time).
        for pe in pending_entries:
            dk, wk = _day_key(open_ms[i]), _week_key(open_ms[i])
            if dk in halted_days:
                res.rejects.append(TradeReject(i, "halted_day", pe.kind, pe.family, pe.dir))
                continue
            if wk in halted_weeks:
                res.rejects.append(TradeReject(i, "halted_week", pe.kind, pe.family, pe.dir))
                continue
            if i == 0 or sig.dir[i - 1] != pe.dir:
                # campaign died between signal and fill (defensive; the gate
                # at pending-creation already checks the signal bar's dir)
                res.rejects.append(TradeReject(i, "campaign_died_before_fill",
                                               pe.kind, pe.family, pe.dir))
                continue
            raw = o[i]
            fill_px = raw * (1 + slip) if pe.dir == 1 else raw * (1 - slip)
            stop = pe.stop_at_signal
            unit_risk = (fill_px - stop) * pe.dir
            if unit_risk <= 0:
                res.rejects.append(TradeReject(i, "gap_through_stop", pe.kind, pe.family, pe.dir))
                continue
            one_r = r_pct * equity
            risk_usd = pe.size_r * one_r
            qty = risk_usd / unit_risk
            assert_entry_legal(pe, i, fill_px, qty, one_r)
            tranche_seq += 1
            tr = Tranche(
                tranche_id=f"c{pe.campaign}t{tranche_seq}", campaign=pe.campaign,
                dir=pe.dir, kind=pe.kind, grade=pe.grade, tier=pe.tier,
                zone=pe.zone, retr=pe.retr, rc=pe.rc, signal_i=pe.signal_i,
                fill_i=i, raw_px=raw, fill_px=fill_px, qty=qty,
                stop_at_entry=stop, one_r_usd=one_r, size_r=pe.size_r,
                grade_uncapped=pe.grade_uncapped, born_aligned=pe.born_aligned,
                peak=fill_px, trough=fill_px)
            tr.fees += abs(fill_px * qty) * fee
            tr.slippage_usd += abs(fill_px - raw) * qty
            campaign_tranche_count[pe.campaign] = \
                campaign_tranche_count.get(pe.campaign, 0) + 1
            open_tranches.append(tr)
            res.tranches.append(tr)
        pending_entries = []

        # 4. Intra-bar stop check (stop is an order — invariant 3).
        if open_tranches:
            d = open_tranches[0].dir
            stop = stop_level(i, d)
            # tranches filled THIS bar use the same level (their signal-bar ratchet)
            if not np.isnan(stop):
                hit = (l[i] <= stop) if d == 1 else (h[i] >= stop)
                if hit:
                    for tr in list(open_tranches):
                        close_tranche(tr, i, stop, "stop")
                    open_tranches.clear()
                    check_halts(i)

        # 5. Close of bar i: excursion tracking, then signals -> pendings.
        for tr in open_tranches:
            if tr.dir == 1:
                tr.peak = max(tr.peak, h[i])
                tr.trough = min(tr.trough, l[i])
            else:
                tr.peak = min(tr.peak, l[i])
                tr.trough = max(tr.trough, h[i])

        for ev in events_by_bar.get(i, []):
            if ev.evt == "TPW":
                for tr in open_tranches:
                    if tr.first_tpw_i is None and tr.dir == ev.dir:
                        tr.first_tpw_i = i
                continue
            if ev.evt == "X":
                if open_tranches:
                    pending_flatten = "failure_x"
                continue
            if ev.evt == "REGIME":
                if open_tranches and open_tranches[0].dir != ev.dir:
                    pending_flatten = "opposite_cross"
                continue
            if ev.evt not in ("PRIME", "CONFIRM", "V"):
                continue

            # --- entry gate evaluation (the eligible set) ---
            if ev.evt == "CONFIRM" and ev.grade == "C":
                continue  # journal-only by design; fixture asserts no fill
            if ev.evt == "V":
                if open_tranches and open_tranches[0].dir != ev.dir:
                    pending_flatten = "v_reversal"
                elif open_tranches and open_tranches[0].dir == ev.dir:
                    res.rejects.append(TradeReject(i, "v_already_positioned", "V", "v", ev.dir))
                    continue
                kind = "V"
            elif ev.evt == "PRIME":
                kind = "R1" if ev.is_r1 else "ADD"
            else:  # CONFIRM add
                if not ev.is_add:
                    continue
                if not open_tranches:
                    res.rejects.append(TradeReject(i, "not_positioned", "ADD", "confirm", ev.dir))
                    continue
                kind = "ADD"

            family = "v" if ev.evt == "V" else ev.evt.lower()
            if sig.dir[i] != ev.dir:
                res.rejects.append(TradeReject(i, "campaign_died_same_bar", kind, family, ev.dir))
                continue
            camp = int(sig.campaign_id[i])
            # 1.0.7 (G-6, ruled): queued same-wake siblings of the same
            # campaign count toward the cap — the over-cap later sibling
            # lands as a graceful REJECT (last-slot allocation follows the
            # ratified PRIME-then-CONFIRM order), never a fill-time crash.
            # The fill-time cap assert is untouched and remains the floor.
            queued_same_camp = sum(1 for p in pending_entries if p.campaign == camp)
            if campaign_tranche_count.get(camp, 0) + queued_same_camp >= max_tranches:
                res.rejects.append(TradeReject(i, "max_tranches", kind, family, ev.dir))
                continue
            stop_now = sig.stop_long[i] if ev.dir == 1 else sig.stop_short[i]
            if np.isnan(stop_now):
                res.rejects.append(TradeReject(i, "no_stop", kind, family, ev.dir))
                continue
            if kind == "ADD" and open_tranches:
                bad = any((tr.fill_px - stop_now) * tr.dir > 1e-9
                          for tr in open_tranches)
                if bad:
                    res.rejects.append(TradeReject(i, "add_ineligible", kind, family, ev.dir))
                    continue
            size_r = size_for(kind, ev.grade, ev.tier, t)
            # projected open risk with the new tranche (rails: <= 1R);
            # tranches being flattened at the next open don't carry forward.
            # 1.0.6 (G-5b, ruled): queued same-wake siblings count toward the
            # projection, so an over-cap later sibling lands as a graceful
            # risk_cap REJECT instead of a fill-time crash. Unreachable at
            # baseline sizes (max two adds/bar x 0.5R, eligible priors carry
            # zero risk) — hardening for future sizing variants.
            carried = [] if pending_flatten else open_tranches
            queued_r = sum(p.size_r for p in pending_entries)
            projected = (open_risk_r(stop_now) if carried else 0.0) + queued_r + size_r
            if projected > max_risk_r + 1e-9:
                res.rejects.append(TradeReject(i, "risk_cap", kind, family, ev.dir))
                continue
            pe = admit_entry(PendingEntry(
                kind=kind, family=family, dir=ev.dir, size_r=size_r, grade=ev.grade,
                tier=ev.tier, zone=ev.zone, retr=ev.retr, rc=ev.rc,
                signal_i=i, stop_at_signal=stop_now,
                grade_uncapped=ev.grade_uncapped,
                born_aligned=res.campaign_born_aligned.get(camp, ev.tier == "full"),
                campaign=camp))
            if pe is not None:
                pending_entries.append(pe)

    res.final_equity = equity
    return res
