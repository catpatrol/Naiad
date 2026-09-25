#!/usr/bin/env python
"""TIER-C11 · THE FORWARD LEDGER — the frozen base and the frozen 9/12, re-ridden at
every refresh, each campaign appended exactly once when it closes [LEANS L-T.6].

Contract of record: exchange/queue/2026-09-24_TC11_APOLLO.md (sha256 bb38e016…).
Executor HEPHAESTUS; seed 20260924.  "FORWARD LEDGER (standing, unscored until n ≥
30): frozen base and frozen 9/12 re-ridden on new bars only at every refresh; both
books printed side by side."

THE READING BUILT (L-T.6)
  OPENING    2026-09-21T16:00:00Z (TC10's pin), after which both frozen books are
             unseen.  Only campaigns whose ENTRY CLOSE is > the opening are admitted.
  BOOKS      base v6 = TP.CONTROL_CARD + T9.V6_ROLES (tierc11_books.v6_book: TP.run_cell_n);
             frozen 9/12 = T9.SWEEP_CELLS[-1] (tierc11_books.trg912_book: T9.replay9) —
             the F-CTRL code path, never a fork.
  REFRESH    `--refresh` re-rides each book over the WHOLE tape (bar 0 to the refresh
             pin: tierc11_books.corridor(pin)).  A campaign is APPENDED EXACTLY ONCE,
             WHEN CLOSED (exit_reason != corridor_end), at the first refresh that sees
             it closed.  One still open at the pin is listed OPEN (marked to the pin),
             not appended and not counted.  A campaign entered at or before the opening
             is never admitted (a continuation is listed, not counted).
  HALT       a refresh whose re-ride CHANGES any appended row (any field, bit for bit)
             or no longer holds an appended campaign HALTs (REFRESH-CHANGED); so does a
             broken chain, a pin earlier than the last refresh, and a refresh at the
             SAME pin that would append anything (the substrate moved).
  COUNT      n per book; each book is 'UNSCORED until n >= 30' on its own n.
  CHAIN      research_outputs/tierc11/forward/FORWARD_LEDGER.jsonl — one canonical JSON
             object per line (sort_keys, separators (',', ':'), no NaN); each line
             carries seq, prev (the previous line's line_sha256; the genesis's is 64
             zeros) and line_sha256 = sha256 of the line's canonical JSON WITHOUT
             line_sha256.  Line kinds: GENESIS (seq 0: the opening, the frozen books'
             definitions, the law), CAMPAIGN (one per appended campaign), REFRESH (one
             per refresh at a new pin: the pin, the substrate, book shas, n, OPEN list,
             the continuations not admitted, the status).
  STAMPS     every v6 row carries the P-AGE-1 trailing band (tide streak at the ENTRY
             bar banded on trailing CLASSIC5 quartile edges, B4 OLD refused) and the
             P-WIN-1 lag (entry_i − arm_i, >= 16 refused; 7–15 the shadow) — the gates'
             out-of-sample record.  The 9/12 rows carry the same stamps (disclosure).
  ROW FIELDS are the as-of-STABLE fields of tierc11_books.campaign_rows (a closed
             campaign's row cannot move when the tape grows); the as-of-dependent
             window_end_* / open_at_asof fields are excluded by name.

LIMIT, SAID OUT LOUD (a finding, not a fix): the foundation is pinned to the TC11
snapshot (tierc11_env guards NAIAD_CACHE_DIR == tc11_20260925; TP.corridor_n clamps to
research_outputs/tierc11/data/AS_OF_PIN.json).  `--snapshot` must therefore name the
snapshot this process was started on, which must be TC11's, and `--pin` may only look
back.  A refresh on bars after 2026-09-25T00:00Z needs the foundation re-rooted on a new
snapshot + pin record — operator / foundation work.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_forward_ledger.py --refresh \\
          --snapshot $NAIAD_CACHE_DIR [--pin <close ms>] [--out-dir=DIR]
      ~/venvs/naiad/bin/python -B scripts/tierc11_forward_ledger.py          # verify + print
      (DIR must be a direct child of research_outputs/tierc11/forward/_det_forward/, or of a
       `_det_forward/` directory OUTSIDE the repo tree)
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import math
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_books as B                   # noqa: E402  (tierc11_env first: guard + shim + hook)

import pandas as pd                         # noqa: E402

E = B.E
TP, T9, TB = E.TP, E.T9, E.TB
iso = TB.iso
MS_4H = 14_400_000

# ══════════════════════════════════════════════════════════ CONSTANTS OF RECORD
OPENING_MS = 1_790_006_400_000              # 2026-09-21T16:00:00Z [L-T.6]
OPENING_ISO = "2026-09-21T16:00:00Z"
N_SCORE = 30                                # "unscored until n >= 30", per book
BOOKS = ("v6", "trg912")
BOOK_LABEL = {"v6": "base v6 (12/26 trigger)", "trg912": "frozen 9/12"}
OUT = E.OUT / "forward"
DET_ROOT = OUT / "_det_forward"
LEDGER = "FORWARD_LEDGER.jsonl"
REPORT = "FORWARD_LEDGER.md"
ZERO = "0" * 64
P_WIN_1_CUT = 16                            # L-G.2: refuse lag >= 16
P_WIN_1_SHADOW = (7, 15)                    # L-G.2: the shadow cut 7-15
P_AGE_1_OLD = "B4"                          # L-G.1: OLD = streak >= trailing q75
# the as-of-STABLE campaign fields (tierc11_books.campaign_rows) a ledger row carries
ROW_FIELDS = (
    "symbol", "entry_ms", "book", "roles_name", "lane", "direction",
    "arm_i", "arm_open_ms", "arm_close_ms", "entry_i", "entry_open_ms", "entry_close_ms",
    "exit_i", "exit_ms", "exit_close_ms", "exit_event_ms", "exit_event_stamp", "exit_reason",
    "entry_px", "stop_px", "r_dist", "atr_at_entry", "r_over_atr", "r_over_atr_gt_2p2",
    "lag", "lag_band", "harvested", "harvest_i", "harvest_close_ms",
    "reached_1r", "latch_1r_i", "latch_1r_open_ms",
    "net_r", "gross_r", "fee_r", "funding_r", "era_of_entry", "entry_bar_straddles_era_cut",
    "tide_state_entry", "tide_streak_entry", "tide_left_censored",
    "tide_trailing_edge_q25", "tide_trailing_edge_q50", "tide_trailing_edge_q75",
    "tide_band", "tide_band_label", "tide_abs_gt206", "tide_streak_age_arm",
    "tide_streak_age_arm_censored",
)
AS_OF_DEPENDENT = ("window_end_i", "window_end_close_ms", "window_open_at_asof",
                   "open_at_asof", "continuation", "entered_after_tc10_pin")
LAW = (
    "L-T.6: opens 2026-09-21T16:00:00Z; admits only campaigns whose entry close is > the "
    "opening; appends a campaign exactly once, when closed (exit_reason != corridor_end); "
    "OPEN campaigns are listed, never appended or counted; a refresh re-rides both frozen "
    "books over the whole tape to its pin on the F-CTRL code path and HALTs if any appended "
    "row changes; n per book; UNSCORED until n >= 30 per book.",
    "Every v6 row stamps the P-AGE-1 trailing band (B4 OLD refused) and the P-WIN-1 lag "
    "(>= 16 refused; 7-15 shadow).",
    "Chain: line_sha256 = sha256(canonical JSON of the line without line_sha256); prev = the "
    "previous line's line_sha256 (genesis: 64 zeros); canonical = sort_keys, separators "
    "(',', ':'), ensure_ascii False, allow_nan False.",
)


def _halt(msg: str) -> None:
    raise SystemExit(f"HALT: {msg}")


# ═══════════════════════════════════════════════════════════════ THE CHAIN
def canonical(obj: dict) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False)


def seal(obj: dict, prev: str) -> dict:
    """Attach prev and line_sha256 (over the canonical JSON without line_sha256)."""
    o = {k: v for k, v in obj.items() if k != "line_sha256"}
    o["prev"] = prev
    o["line_sha256"] = hashlib.sha256(canonical(o).encode("utf-8")).hexdigest()
    return o


def verify_chain(raw: bytes) -> tuple[list[str], list[dict]]:
    """CHAIN findings over the ledger's BYTES: every line is its object's canonical
    JSON; seq runs 0, 1, 2, …; line 0 is GENESIS with prev = 64 zeros; each prev is
    the previous line_sha256; each line_sha256 re-derives."""
    out, objs = [], []
    if not raw:
        return ["CHAIN: the ledger is empty"], []
    if not raw.endswith(b"\n"):
        out.append("CHAIN: the ledger does not end with a newline (a torn write)")
    prev = ZERO
    text = raw.decode("utf-8").split("\n")
    if raw.endswith(b"\n"):
        text = text[:-1]
    for n, ln in enumerate(text):
        try:
            o = json.loads(ln)
        except ValueError as e:
            out.append(f"CHAIN line {n}: not JSON ({e})")
            break
        objs.append(o)
        if canonical(o) != ln:
            out.append(f"CHAIN line {n}: not the canonical JSON of its object")
        if o.get("seq") != n:
            out.append(f"CHAIN line {n}: seq {o.get('seq')!r} != {n}")
        if n == 0 and o.get("kind") != "GENESIS":
            out.append("CHAIN line 0: not the GENESIS line")
        if o.get("prev") != prev:
            out.append(f"CHAIN line {n}: prev {str(o.get('prev'))[:16]}… != the previous line's "
                       f"line_sha256 {prev[:16]}…")
        body = {k: v for k, v in o.items() if k != "line_sha256"}
        sha = hashlib.sha256(canonical(body).encode("utf-8")).hexdigest()
        if o.get("line_sha256") != sha:
            out.append(f"CHAIN line {n}: line_sha256 {str(o.get('line_sha256'))[:16]}… does not "
                       f"re-derive ({sha[:16]}…)")
        prev = str(o.get("line_sha256"))
    return out, objs


# ═══════════════════════════════════════════════════════ THE BOOKS AT A PIN
def _native(v):
    if v is None or v is pd.NA:
        return None
    if hasattr(v, "item"):
        v = v.item()
    if isinstance(v, float) and math.isnan(v):
        return None
    return v


def haircut(sym: str, net_r: float, fee_r: float) -> tuple[float, float]:
    """AM-7: net_r − fee_r × slip / taker (the stem's charter tier, E.fees())."""
    fz = E.fees()[sym]
    slip, taker = float(fz["slippage_bps_side"]), float(fz["taker_bps_side"])
    return float(net_r) - float(fee_r) * slip / taker, slip


def book_rows(name: str, book, roles, lo: int, hi: int, pool: dict) -> dict:
    """{(symbol, entry_ms): row} — the as-of-stable fields at FULL precision (the
    campaign frame is built from the Trade objects; nothing here is rounded), plus
    exit_px, the haircut twin and the two gates' stamps."""
    df = B.campaign_rows(book, roles, lo, hi, pool, name)
    tr = {(t.symbol, int(t.entry_ms)): t for t in book}
    out = {}
    for rec in df.to_dict("records"):
        k = (str(rec["symbol"]), int(rec["entry_ms"]))
        t = tr[k]
        row = {f: _native(rec[f]) for f in ROW_FIELDS}
        hc, slip = haircut(k[0], float(t.net_r), float(t.fee_r))
        row.update({"exit_px": float(t.exit_px), "haircut_net_r": hc, "slip_bps_side": slip,
                    "p_age_1_band": row["tide_band"],
                    "p_age_1_refuses": row["tide_band"] == P_AGE_1_OLD,
                    "p_win_1_lag": row["lag"],
                    "p_win_1_refuses": int(row["lag"]) >= P_WIN_1_CUT,
                    "p_win_1_shadow_refuses": P_WIN_1_SHADOW[0] <= int(row["lag"])
                    <= P_WIN_1_SHADOW[1]})
        out[k] = row
    return out


def books_at(pin_ms: int) -> dict:
    """Both frozen books re-ridden over the whole tape to `pin_ms` (a 4h close),
    on tierc11_books' F-CTRL path."""
    pin_iso = iso(int(pin_ms))
    lo, hi, meta = B.corridor(None if int(pin_ms) == int(E.PIN_MS) else pin_iso)
    if hi + 1 != int(pin_ms):
        _halt(f"the corridor ends {iso(hi + 1)}, not the pin {pin_iso}")
    v6 = B.v6_book(lo, hi)
    b912 = B.trg912_book(lo, hi)
    pool = B.tide_pool(lo, hi)
    return {"lo": lo, "hi": hi, "meta": meta, "pin_ms": int(pin_ms), "pin_iso": pin_iso,
            "books": {"v6": v6, "trg912": b912},
            "sha": {"v6": B.book_sha(v6), "trg912": B.book_sha(b912)},
            "rows": {"v6": book_rows("v6", v6, T9.V6_ROLES, lo, hi, pool),
                     "trg912": book_rows("trg912", b912, B.r912(), lo, hi, pool)}}


# ════════════════════════════════════════════════════════ FIXTURE SEAMS (named)
def admitted(row: dict, opening_ms: int) -> bool:
    """L-T.6: entry close strictly after the opening."""
    return int(row["entry_close_ms"]) > int(opening_ms)


def is_closed(row: dict) -> bool:
    """L-T.6: appended when closed — any exit but corridor_end."""
    return str(row["exit_reason"]) != "corridor_end"


def already(appended: dict, book: str, key: tuple) -> bool:
    """Append exactly once: a (book, key) already on the ledger is never re-appended."""
    return (book, key) in appended


def continuation(row: dict, opening_ms: int) -> bool:
    """Entered at or before the opening and still open at it (exit bar opens at or
    after the opening) — listed, never counted."""
    return (int(row["entry_close_ms"]) <= int(opening_ms)
            and int(row["exit_ms"]) >= int(opening_ms))


# ════════════════════════════════════════════════════════════════ THE REFRESH
def _inside(p: Path, root: Path) -> bool:
    return p == root or root in p.parents


def guard_out(out: Path) -> Path:
    o = Path(out).resolve()
    if o == OUT.resolve() or o.parent == DET_ROOT.resolve():
        return o
    trees = {ROOT.resolve(), Path(E.MAIN_TREE).resolve()}
    if o.parent.name == DET_ROOT.name and not any(_inside(o, t) for t in trees):
        return o
    _halt(f"output dir {o} is neither {OUT}, an F-DET run dir under {DET_ROOT}, nor one "
          f"under a {DET_ROOT.name}/ scratch outside the repo")
    return o


def read_ledger(path: Path) -> tuple[bytes, list[dict]]:
    if not path.exists():
        return b"", []
    raw = path.read_bytes()
    bad, objs = verify_chain(raw)
    if bad:
        _halt(f"the ledger chain does not verify — nothing is refreshed: {bad[:3]}")
    return raw, objs


def genesis(opening_ms: int) -> dict:
    card = TP.CONTROL_CARD
    return {"kind": "GENESIS", "seq": 0, "tier": "TIER-C11", "ledger": "FORWARD LEDGER",
            "opening_ms": int(opening_ms), "opening_iso": iso(int(opening_ms)),
            "n_score": N_SCORE,
            "books": {"v6": {"card": type(card).__name__ + ":" + str(card.name),
                             "roles": dataclasses.asdict(T9.V6_ROLES),
                             "path": "tierc11_books.v6_book (TP.run_cell_n)"},
                      "trg912": {"card": type(card).__name__ + ":" + str(card.name),
                                 "roles": dataclasses.asdict(B.r912()),
                                 "path": "tierc11_books.trg912_book (T9.replay9)"}},
            "panel": list(E.CLASSIC5), "law": list(LAW)}


def status_word(n: int) -> str:
    return f"UNSCORED (n {n} < {N_SCORE})" if n < N_SCORE else f"n {n} >= {N_SCORE}: scorable"


def refresh(out_dir: Path = OUT, pin_ms: int | None = None, opening_ms: int = OPENING_MS,
            snapshot_name: str | None = None) -> dict:
    """One refresh.  Returns the summary; writes the ledger (append-only) and the
    report unless the pin equals the last refresh's (then it only verifies)."""
    out_dir = guard_out(out_dir)
    pin = int(E.PIN_MS if pin_ms is None else pin_ms)
    if pin % MS_4H:
        _halt(f"the pin {pin} is not a 4h close")
    if pin <= int(opening_ms):
        _halt(f"the pin {iso(pin)} is not after the opening {iso(int(opening_ms))}")
    path = out_dir / LEDGER
    raw, lines = read_ledger(path)
    last_pin = None
    if lines:
        g = lines[0]
        if int(g["opening_ms"]) != int(opening_ms):
            _halt(f"the ledger opens at {g['opening_iso']}, not {iso(int(opening_ms))}")
        pins = [int(o["pin_ms"]) for o in lines if o["kind"] == "REFRESH"]
        last_pin = max(pins) if pins else None
        if last_pin is not None and pin < last_pin:
            _halt(f"the refresh pin {iso(pin)} is before the last refresh {iso(last_pin)} — "
                  f"the ledger only moves forward")
    S = books_at(pin)
    appended = {(o["book"], (o["key"][0], int(o["key"][1]))): o for o in lines
                if o["kind"] == "CAMPAIGN"}
    changed = []
    for (b, k), o in sorted(appended.items()):
        now = S["rows"][b].get(k)
        if now is None:
            changed.append(f"{b} {k[0]} {iso(k[1])}: appended, absent from the re-ride")
        elif canonical(now) != canonical(o["row"]):
            diff = sorted(f for f in set(now) | set(o["row"])
                          if canonical({"v": now.get(f)}) != canonical({"v": o["row"].get(f)}))
            changed.append(f"{b} {k[0]} {iso(k[1])}: fields {diff[:6]} changed")
    if changed:
        _halt("REFRESH-CHANGED — a re-ride changed an appended row; nothing is written: "
              + " | ".join(changed[:4]))
    new, opens, pre = {b: [] for b in BOOKS}, {b: [] for b in BOOKS}, {b: [] for b in BOOKS}
    for b in BOOKS:
        for k, row in sorted(S["rows"][b].items()):
            if not admitted(row, opening_ms):
                if continuation(row, opening_ms):
                    pre[b].append(row)
                continue
            if not is_closed(row):
                opens[b].append(row)
                continue
            if not already(appended, b, k):
                new[b].append(row)
    n_new = sum(len(v) for v in new.values())
    if last_pin is not None and pin == last_pin:
        if n_new:
            _halt(f"a refresh at the SAME pin {iso(pin)} would append {n_new} campaign(s) — the "
                  f"substrate moved under the ledger")
        return {"written": False, "pin_ms": pin, "S": S, "lines": lines, "new": new,
                "open": opens, "pre": pre, "raw": raw}
    objs = list(lines) if lines else []
    add = []
    prev = objs[-1]["line_sha256"] if objs else ZERO
    if not objs:
        gl = seal(genesis(opening_ms), ZERO)
        add.append(gl)
        prev = gl["line_sha256"]
    seq = len(objs) + len(add)
    count = {b: sum(1 for (bb, _) in appended if bb == b) for b in BOOKS}
    for b in BOOKS:
        for row in sorted(new[b], key=lambda r: (int(r["exit_close_ms"]), r["symbol"],
                                                 int(r["entry_ms"]))):
            count[b] += 1
            ln = seal({"kind": "CAMPAIGN", "seq": seq, "book": b,
                       "key": [row["symbol"], int(row["entry_ms"])], "row": row,
                       "appended_at_pin_ms": pin, "appended_at_pin_iso": iso(pin),
                       "n_book_after": count[b]}, prev)
            add.append(ln)
            prev = ln["line_sha256"]
            seq += 1

    def brief(r: dict, marked: bool) -> dict:
        return {"key": [r["symbol"], int(r["entry_ms"])], "direction": int(r["direction"]),
                "entry_close_ms": int(r["entry_close_ms"]), "exit_reason": r["exit_reason"],
                ("net_r_marked_to_pin" if marked else "net_r"): r["net_r"]}

    rl = seal({"kind": "REFRESH", "seq": seq, "pin_ms": pin, "pin_iso": iso(pin),
               "snapshot": str(snapshot_name or E.SNAPSHOT.name),
               "input_sha": TP.input_sha(E.CLASSIC5),
               "corridor_lo_ms": int(S["lo"]),
               "books": {b: {"book_sha": S["sha"][b], "n_rode": len(S["books"][b]),
                             "n_appended_total": count[b],
                             "appended_now": [[r["symbol"], int(r["entry_ms"])]
                                              for r in sorted(new[b], key=lambda r: (
                                                  int(r["exit_close_ms"]), r["symbol"],
                                                  int(r["entry_ms"])))],
                             "open": [brief(r, True) for r in opens[b]],
                             # a continuation still OPEN at the pin is marked to it, never
                             # labelled as a closed net_r (verifier m8)
                             "continuations_not_admitted": [
                                 brief(r, not is_closed(r)) for r in pre[b]],
                             "status": status_word(count[b])} for b in BOOKS}}, prev)
    add.append(rl)
    body = raw + "".join(canonical(o) + "\n" for o in add).encode("utf-8")
    bad, all_objs = verify_chain(body)
    if bad or not body.startswith(raw):
        _halt(f"the ledger being written does not verify: {bad[:3]}")
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(body)
    os.replace(str(tmp), str(path))
    (out_dir / REPORT).write_text(render_md(all_objs, S, opens, pre), encoding="utf-8")
    return {"written": True, "pin_ms": pin, "S": S, "lines": all_objs, "new": new,
            "open": opens, "pre": pre, "raw": body}


# ═══════════════════════════════════════════════════════════════════ RENDER
def _f(x, nd: int = 6) -> str:
    return "—" if x is None else f"{float(x):+.{nd}f}"


def render_md(objs: list[dict], S: dict, opens: dict, pre: dict) -> str:
    g = objs[0]
    last = [o for o in objs if o["kind"] == "REFRESH"][-1]
    camps = [o for o in objs if o["kind"] == "CAMPAIGN"]
    L = []
    A = L.append
    A("as_of_last_closed_4h: " + iso(int(last["pin_ms"])))
    A("")
    A("# TIER-C11 · THE FORWARD LEDGER — base v6 and frozen 9/12, side by side")
    A("")
    A(f"opening {g['opening_iso']} (entry close must be after it) · last refresh pin "
      f"{last['pin_iso']} · substrate {last['snapshot']} · chain head "
      f"`{objs[-1]['line_sha256']}` · {len(objs)} line(s)")
    A("")
    A("**Standing and UNSCORED until each book's own n >= 30.** No CI, no p, no verdict. A "
      "campaign is appended exactly once, when it closes; an OPEN campaign is listed, never "
      "appended or counted; a continuation (entered at or before the opening) is listed, "
      "never counted.")
    A("")
    for ln in g["law"]:
        A(f"- {ln}")
    A("")
    A("## Both books, side by side")
    A("")
    b6, b9 = last["books"]["v6"], last["books"]["trg912"]
    A(f"| | {BOOK_LABEL['v6']} | {BOOK_LABEL['trg912']} |")
    A("|---|---|---|")
    A(f"| definition | {g['books']['v6']['path']} · roles {g['books']['v6']['roles']['name']} | "
      f"{g['books']['trg912']['path']} · roles {g['books']['trg912']['roles']['name']} |")
    A(f"| campaigns ridden to the pin (whole tape) | {b6['n_rode']} | {b9['n_rode']} |")
    A(f"| book sha (TP._book_sha) at the pin | {b6['book_sha'][:16]}… | {b9['book_sha'][:16]}… |")
    A(f"| appended (closed after the opening) — n | {b6['n_appended_total']} | "
      f"{b9['n_appended_total']} |")
    sums = {}
    for b_ in BOOKS:
        rows = [o["row"] for o in camps if o["book"] == b_]
        sums[b_] = (sum(float(r["net_r"]) for r in rows), sum(float(r["haircut_net_r"])
                                                               for r in rows))
    A(f"| appended ΣR (net) · Σ haircut R | {_f(sums['v6'][0], 4)} · {_f(sums['v6'][1], 4)} | "
      f"{_f(sums['trg912'][0], 4)} · {_f(sums['trg912'][1], 4)} |")
    A(f"| status | {b6['status']} | {b9['status']} |")

    def lst(xs, marked):
        # `marked` is the list's kind; each entry says itself which it is (a continuation
        # still open at the pin carries net_r_marked_to_pin — verifier m8)
        if not xs:
            return "none"
        return "; ".join(f"{x['key'][0]} {'long' if x['direction'] == 1 else 'short'} entered "
                         f"{iso(int(x['key'][1]))} (bar open) · "
                         f"{'marked to the pin ' + _f(x['net_r_marked_to_pin']) if 'net_r_marked_to_pin' in x else x['exit_reason'] + ' ' + _f(x['net_r'])}"
                         for x in xs)

    A(f"| OPEN at the pin (listed, not appended, not counted) | {lst(b6['open'], True)} | "
      f"{lst(b9['open'], True)} |")
    A(f"| continuations entered at/before the opening (listed, not counted) | "
      f"{lst(b6['continuations_not_admitted'], False)} | "
      f"{lst(b9['continuations_not_admitted'], False)} |")
    A("")
    A("## Appended campaigns (whole)")
    A("")
    A("| seq | book | asset | dir | entry (bar open) | exit (bar open) | exit_reason | net R | "
      "haircut R | era | P-AGE-1 band | refuses | P-WIN-1 lag | refuses | shadow 7-15 | "
      "appended at |")
    A("|---:|---|---|---:|---|---|---|---:|---:|---|---|---|---:|---|---|---|")
    if not camps:
        A("| — | (none yet) | | | | | | | | | | | | | | |")
    for o in camps:
        r = o["row"]
        A(f"| {o['seq']} | {o['book']} | {r['symbol']} | {int(r['direction']):+d} | "
          f"{iso(int(r['entry_ms']))} | {iso(int(r['exit_ms']))} | {r['exit_reason']} | "
          f"{_f(r['net_r'])} | {_f(r['haircut_net_r'])} | {r['era_of_entry']} | "
          f"{r['p_age_1_band']} | {r['p_age_1_refuses']} | {r['p_win_1_lag']} | "
          f"{r['p_win_1_refuses']} | {r['p_win_1_shadow_refuses']} | "
          f"{o['appended_at_pin_iso']} |")
    A("")
    A("## Refreshes")
    A("")
    A("| seq | pin | snapshot | v6 appended now | 9/12 appended now | v6 n | 9/12 n | line sha |")
    A("|---:|---|---|---:|---:|---:|---:|---|")
    for o in objs:
        if o["kind"] != "REFRESH":
            continue
        A(f"| {o['seq']} | {o['pin_iso']} | {o['snapshot']} | "
          f"{len(o['books']['v6']['appended_now'])} | "
          f"{len(o['books']['trg912']['appended_now'])} | "
          f"{o['books']['v6']['n_appended_total']} | {o['books']['trg912']['n_appended_total']} "
          f"| {o['line_sha256'][:16]}… |")
    A("")
    A("LIMIT (finding, not fixed): the foundation is pinned to the TC11 snapshot and pin; a "
      "refresh on bars after 2026-09-25T00:00Z needs the foundation re-rooted on a new "
      "snapshot + pin record (operator / foundation work).")
    return "\n".join(L) + "\n"


# ═════════════════════════════════════════════════════════════════════ MAIN
def _arg(args, name):
    for i, a in enumerate(args):
        if a.startswith(name + "="):
            return a.split("=", 1)[1]
        if a == name and i + 1 < len(args):
            return args[i + 1]
    return None


def check_snapshot(snap: str | None) -> str:
    """--snapshot must name the substrate this process was started on, and that must
    be the foundation's snapshot (the shim already HALTed on any other env)."""
    if snap is None:
        _halt("--refresh needs --snapshot <path> (the substrate of the re-ride)")
    s = Path(os.path.expanduser(snap)).resolve()
    envp = Path(os.path.expanduser(os.environ.get("NAIAD_CACHE_DIR", ""))).resolve()
    if s != envp:
        _halt(f"--snapshot {s} is not NAIAD_CACHE_DIR {envp} — the loaders bind the "
              f"environment's substrate at import; start the process on the snapshot you name")
    if s != E.SNAPSHOT.resolve():
        _halt(f"--snapshot {s} is not the foundation's {E.SNAPSHOT} — a later snapshot needs "
              f"the foundation re-rooted (operator / foundation work)")
    return s.name


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    od = _arg(args, "--out-dir")
    out = Path(od) if od else OUT
    if "--refresh" in args:
        name = check_snapshot(_arg(args, "--snapshot"))
        pin = _arg(args, "--pin")
        R = refresh(out, None if pin is None else int(pin), OPENING_MS, name)
        last = [o for o in R["lines"] if o["kind"] == "REFRESH"][-1] if R["written"] else None
        print(f"refresh at {iso(R['pin_ms'])}: {'written' if R['written'] else 'verified, nothing new'}")
        for b in BOOKS:
            n = sum(1 for o in R["lines"] if o["kind"] == "CAMPAIGN" and o["book"] == b)
            print(f"  {BOOK_LABEL[b]:24} appended n {n} (+{len(R['new'][b])} now) · OPEN "
                  f"{[(r['symbol'], iso(int(r['entry_ms']))) for r in R['open'][b]]} · "
                  f"continuations not admitted "
                  f"{[(r['symbol'], iso(int(r['entry_ms']))) for r in R['pre'][b]]} · "
                  f"{status_word(n)}")
        if last is not None:
            print(f"  chain head {last['line_sha256']}")
        return 0
    raw, objs = read_ledger(guard_out(out) / LEDGER)
    print(f"{LEDGER}: {len(objs)} line(s), chain verifies; head "
          f"{objs[-1]['line_sha256'] if objs else '(none)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
