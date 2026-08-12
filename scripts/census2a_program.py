#!/usr/bin/env python
"""CENSUS-2A -- THE ARMED-WINDOW CENSUS.

Contract: exchange/queue/2026-08-12_CENSUS2A_v0.3_RESOLVED_APOLLO.md
  sha256 b0da051b894fc8586fab466fcf99cb0390763551d0d67bbac83743abc1547a6a
Running this program IS the RATIFIED stamp (contract condition 3).

WHAT CHANGED FROM THE PASTE-1 SANDBOX, AND WHY IT IS LOAD-BEARING
  Paste #1 (MC-2) pinned the constants. Its adversarial review then found six
  defects in the sandbox itself, and v0.3 turned three of those findings into
  binding rulings. They are implemented here, not restated:

  R-1  THE RULER CHANGED.  `MFE - MAE` is algebraically 2*(midpoint of the
       forward range - anchor close)/ATR -- a POSITION-IN-RANGE statistic. It
       is invariant to the terminal price, its sign disagrees with the terminal
       return on ~40% of anchors, and its magnitude correlates 0.91 with
       forward range. It is RETIRED as a discriminant. Primary ruler is now the
       signed TERMINAL return, ATR-normalised at the anchor; MFE/|MAE| quality
       ratio, raw MFE, raw MAE and the toll line print beside it.
  R-2  THE REPLICATION CRITERION CHANGED.  `>=3 of 5 assets agree on sign` has
       P = 0.50 under a fair coin, is computed from the same observations as
       the interval, and across three stages and two eras it never once changed
       a decision. It is replaced by an ASSET-CLUSTER bootstrap CI excluding
       zero. Per-asset signs still print, descriptively.
  R-3  THE TRAP STAMP IS DROPPED.  >=2 fires on ~92% of armings (a null gate);
       >=5 was withdrawn as a selection artifact (corrected p = 0.287 against
       an I8 bar of 0.0091). `counter_n` survives as a measured column only.
       The arming stamp set is {WALL, KISS/refusal, FIRST}, score 0-3.
  I11 THE SELECTION GUARD IS COMMITTED CODE ON EVERY SWEEP.  A CI is not a
       correction for having searched. Any stage that sweeps candidates and
       promotes a winner must clear a max-statistic permutation test against
       the contract's own FDR bar (q/m). F-GUARD proves the guard fires on a
       planted sweep BEFORE any real sweep runs -- a fixture that can fail.
  I12 PINS MERGE across `--stage` re-runs. In paste #1 a scoped re-run rebuilt
       the manifest from scratch and destroyed five of six pins. F-PIN proves
       survival.

RESIDENCY (I2).  All bulk born on D:/Naiad/research_outputs/census2a/**.
  `wait_for_drive` never raises by design, so the HALT is the caller's.
IDENTITY (I3).  Asserted IN CODE. Paste #1's lesson: prose gates gate nothing.
EVIDENCE WALL (I1).  Every scored table <= 2024-07-01, read from the census
  constant, never restated.

USAGE
  python scripts/census2a_program.py --stage fixtures   # F-GUARD, F-PIN first
  python scripts/census2a_program.py --stage cen0b      # PAXG fetch (network)
  python scripts/census2a_program.py --stage cen1       # substrate
  python scripts/census2a_program.py --stage all
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import census_build as CB  # noqa: E402
import mc2_program as MC2  # noqa: E402
from drive_wait import wait_for_drive  # noqa: E402

SEED = 20260812
R6 = 6

OUT = Path("D:/Naiad/research_outputs/census2a")
KLINES_OUT = OUT / "klines"
CEIL_MS = CB.CEIL_MS
TF_MS = {**CB.TF_MS, "1m": 60_000}

DISPLAY_ONLY = ("DISPLAY-ONLY -- post-lockbox live-era data -- "
                "hypothesis generation only, never evidence.")

PANEL = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT"]
ANNEX = ["JTOUSDT", "TAOUSDT"]

# --- contract §0 PINNED [VETO by name] --------------------------------------
W_MAX = 151                      # 4h bars
WALL_ATR = 0.5                   # per limb
FIRST_N = 20                     # 4h bars
SEAL_K = 6                       # 4h bars
KISS_EPS, KISS_DELTA, KISS_K = 0.25, 0.75, 10
RIBBON_C = 0.5
FDR_Q = 0.10
TOLL_BPS_ROUND_TRIP = 10.0       # global fee_bps_side 5.0 x 2; per-mandate does not exist

# Horizons are DURATION-fixed (paste-1 defect 6 fix): H100 == 100 x 5m.
HORIZONS_MS = {"H20": 20 * 300_000, "H100": 100 * 300_000, "H500": 500 * 300_000}

# CEN-1 cross classes. 9_25 is recorded raw but EXCLUDED from the trigger
# taxonomy (contract vi) -- it is 2.19x the reference count and the weakest
# measured effect, and admitting it unstratified would let one class set the
# FDR budget for nine registrations.
CROSS_CLASSES = ["9_89", "9_200", "89_200", "12_25", "25_89", "300_450", "450_500"]
RAW_ONLY_CLASSES = ["9_25"]
LATTICE_A = ["9_89", "9_200", "89_200"]

_LOG: list[str] = []


def log(msg: str) -> None:
    line = f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    _LOG.append(line)


def iso(ms_v: int) -> str:
    return datetime.fromtimestamp(ms_v / 1000, timezone.utc).strftime("%Y-%m-%d %H:%M")


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ===========================================================================
# I3 IN CODE + I2 -- the preflight.  Paste-1: prose gates gate nothing.
# ===========================================================================
def stage_preflight() -> dict:
    log("PREFLIGHT -- I3 identity (in code) + I2 drive gate")
    import subprocess
    checks = []
    cwd = str(Path.cwd()).replace("\\", "/")
    checks.append(("pwd ends C:/Naiad",
                   cwd.rstrip("/").lower().endswith(("c:/naiad", "/c/naiad")), cwd))
    checks.append(("pwd NOT contains OneDrive", "onedrive" not in cwd.lower(), ""))

    def _git(a):
        try:
            return subprocess.run(["git"] + a, capture_output=True, text=True,
                                  timeout=30).stdout.strip()
        except Exception:
            return ""
    br = _git(["rev-parse", "--abbrev-ref", "HEAD"])
    checks.append(("branch v12-v1-census", br == "v12-v1-census", br))
    rm = _git(["config", "--get", "remote.origin.url"])
    checks.append(("remote catpatrol/Naiad", "catpatrol/Naiad" in rm, rm))
    for rel in ["LEDGER.md", "exchange/status/CONVENTIONS.md"]:
        checks.append((f"{rel}", (ROOT / rel).exists(), ""))

    for n, ok, d in checks:
        log(f"    {'PASS' if ok else 'FAIL'}  {n:30} {d}")
    if not all(o for _, o, _ in checks):
        raise SystemExit("HALT (I3): identity gate failed.")

    r = wait_for_drive("D:/Naiad")
    log(f"    drive_wait: {r}")
    if not r.ok:
        raise SystemExit(f"HALT (I2): D:/Naiad {r.state} after {r.elapsed:.1f}s.")
    if OUT.drive.upper() != "D:":
        raise SystemExit(f"HALT (I2): output root {OUT} is not on D:.")
    OUT.mkdir(parents=True, exist_ok=True)
    probe = OUT / ".rw_probe"
    try:
        probe.write_text("ok", encoding="utf-8"); probe.unlink()
    except Exception as exc:
        raise SystemExit(f"HALT (I2): D: reachable but not writable: {exc}")
    log(f"    residency OK -> {OUT}")
    assert CEIL_MS == 1719792000000, "evidence wall moved"
    log(f"    I1 wall: {CEIL_MS} ({iso(CEIL_MS)}) imported from census_build")
    return {"identity": [{"check": n, "pass": bool(o)} for n, o, _ in checks],
            "drive": {"state": r.state, "elapsed_s": round(r.elapsed, 3)},
            "ceil_ms": CEIL_MS}


# ===========================================================================
# I11 -- THE SELECTION GUARD.  Shared, committed, used by every sweep stage.
# ===========================================================================
def selection_guard(candidates: list, q: float = FDR_Q, n_perm: int = 2000,
                    seed: int = SEED) -> dict:
    """Max-statistic permutation test for a sweep-and-select stage.

    candidates: list of (label, values, mask) -- one entry per swept candidate.
      `values` is the outcome vector for that candidate's population and `mask`
      splits it into the two groups being compared.

    The statistic is max |median(a) - median(b)| ACROSS candidates, which is
    exactly what a promotion rule maximises. Its null is built by shuffling the
    outcome labels within each candidate's own population, destroying the
    association while preserving group sizes. The corrected p is compared to
    the contract's FDR bar q/m -- so the answer is not just "is it significant"
    but "how far from admissible is the winner".

    Why this is committed code and not a note: a CI is not a correction for
    having looked m times. Two pins in paste #1 (TRAP >=5, 30m-in-4h) cleared
    their CIs and failed this test at p = 0.287 and p = 0.549.
    """
    usable = []
    for label, vals, mask in candidates:
        v = np.asarray(vals, float)
        m = np.asarray(mask, bool)
        ok = np.isfinite(v)
        if (m & ok).sum() >= 8 and (~m & ok).sum() >= 8:
            usable.append((label, v, m))
    if not usable:
        return {"m": 0, "admissible": False, "reason": "no usable candidate"}

    def max_sep(perm_rng=None):
        best, best_lab = 0.0, None
        for label, v, m in usable:
            vv = v if perm_rng is None else v[perm_rng.permutation(len(v))]
            a, b = vv[m], vv[~m]
            a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
            if len(a) < 8 or len(b) < 8:
                continue
            s = abs(float(np.median(a) - np.median(b)))
            if s > best:
                best, best_lab = s, label
        return best, best_lab

    obs, winner = max_sep()
    rng = np.random.default_rng(seed + 7700)
    null = np.array([max_sep(rng)[0] for _ in range(n_perm)])
    p_sel = float((np.sum(null >= obs) + 1) / (n_perm + 1))
    m = len(usable)
    bar = q / m
    return {"m": m, "winner": winner, "observed_max_sep": round(obs, 6),
            "p_selection_corrected": round(p_sel, 4),
            "bh_bar_q_over_m": round(bar, 5),
            "null_p95": round(float(np.percentile(null, 95)), 6),
            "admissible": bool(p_sel <= bar), "n_perm": n_perm}


def cluster_ci(values: np.ndarray, clusters: np.ndarray, mask: np.ndarray | None = None,
               n_boot: int = 4000, seed: int = SEED) -> dict:
    """R-2: asset-cluster bootstrap CI. The unit of replication is the ASSET.

    With mask -> CI on the median difference between the two groups.
    Without   -> CI on the median of `values` itself.

    A row bootstrap treats overlapping forward windows as independent
    observations; they are not, and a five-asset panel claim asserts
    replication across assets, not across rows.
    """
    values = np.asarray(values, float)
    clusters = np.asarray(clusters)
    uniq = np.unique(clusters)
    if len(uniq) < 3:
        return {"point": None, "lo": None, "hi": None, "excludes_zero": False,
                "n_clusters": int(len(uniq)), "reason": "need >=3 clusters"}
    rng = np.random.default_rng(seed)
    stats = []
    for _ in range(n_boot):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        if mask is None:
            v = np.concatenate([values[clusters == c] for c in pick])
            v = v[np.isfinite(v)]
            if len(v) >= 3:
                stats.append(np.median(v))
        else:
            a = np.concatenate([values[(clusters == c) & mask] for c in pick])
            b = np.concatenate([values[(clusters == c) & ~mask] for c in pick])
            a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
            if len(a) >= 3 and len(b) >= 3:
                stats.append(np.median(a) - np.median(b))
    if len(stats) < n_boot // 4:
        return {"point": None, "lo": None, "hi": None, "excludes_zero": False,
                "n_clusters": int(len(uniq)), "reason": "degenerate draws"}
    stats = np.asarray(stats)
    lo, hi = np.percentile(stats, [5, 95])
    if mask is None:
        pt = float(np.median(values[np.isfinite(values)]))
    else:
        a = values[mask]; b = values[~mask]
        pt = float(np.median(a[np.isfinite(a)]) - np.median(b[np.isfinite(b)]))
    return {"point": round(pt, 6), "lo": round(float(lo), 6), "hi": round(float(hi), 6),
            "excludes_zero": bool(lo > 0 or hi < 0), "n_clusters": int(len(uniq))}


# ===========================================================================
# F-GUARD -- a fixture that CAN fail.  Runs BEFORE any real sweep.
# ===========================================================================
def fixture_guard() -> dict:
    """Prove the selection guard both FIRES on noise and PASSES a real effect.

    A guard that only ever declines is not a guard, it is an off switch. So the
    fixture plants two synthetic sweeps with known ground truth:

      NULL sweep  -- 12 candidates, outcomes independent of the split. The
                     guard MUST decline. (Some candidate will clear a naive CI:
                     that is the whole point.)
      PLANTED     -- same shape, one candidate carrying a large real effect.
                     The guard MUST admit.

    If either verdict is wrong the fixture HALTs. This is what makes F-GUARD
    falsifiable rather than decorative.
    """
    log("F-GUARD -- planted-sweep proof (runs BEFORE any real sweep)")
    rng = np.random.default_rng(SEED + 1)
    n = 600

    null_c = []
    for i in range(12):
        v = rng.normal(0, 1, n)
        m = rng.random(n) < (0.2 + 0.05 * i)
        null_c.append((f"null{i}", v, m))
    g_null = selection_guard(null_c, n_perm=1500)

    # how many candidates clear a naive CI in the null sweep -- the motivation
    naive_hits = 0
    for label, v, m in null_c:
        a, b = v[m], v[~m]
        r2 = np.random.default_rng(SEED + 2)
        d = (np.median(a[r2.integers(0, len(a), (2000, len(a)))], axis=1)
             - np.median(b[r2.integers(0, len(b), (2000, len(b)))], axis=1))
        lo, hi = np.percentile(d, [5, 95])
        naive_hits += int(lo > 0 or hi < 0)

    planted_c = []
    for i in range(12):
        v = rng.normal(0, 1, n)
        m = rng.random(n) < (0.2 + 0.05 * i)
        if i == 5:
            v = v + np.where(m, 1.6, 0.0)      # a real, large effect
        planted_c.append((f"plant{i}", v, m))
    g_plant = selection_guard(planted_c, n_perm=1500)

    log(f"    NULL sweep    : m={g_null['m']} p_sel={g_null['p_selection_corrected']} "
        f"bar={g_null['bh_bar_q_over_m']} -> admissible={g_null['admissible']}")
    log(f"      ({naive_hits}/12 null candidates cleared a NAIVE CI -- the reason "
        f"the guard exists)")
    log(f"    PLANTED sweep : m={g_plant['m']} winner={g_plant['winner']} "
        f"p_sel={g_plant['p_selection_corrected']} -> admissible={g_plant['admissible']}")

    ok_null = not g_null["admissible"]
    ok_plant = g_plant["admissible"] and g_plant["winner"] == "plant5"
    log(f"    {'PASS' if ok_null else 'FAIL'}  guard DECLINES the null sweep")
    log(f"    {'PASS' if ok_plant else 'FAIL'}  guard ADMITS the planted effect "
        f"(and names it)")
    if not (ok_null and ok_plant):
        raise SystemExit("HALT (F-GUARD): the selection guard does not behave as "
                         "specified -- it must decline noise AND admit a real "
                         "effect. No sweep stage may run.")
    return {"null": g_null, "planted": g_plant, "naive_hits_in_null": naive_hits,
            "pass": True}


# ===========================================================================
# F-PIN -- pins survive a --stage re-run (I12)
# ===========================================================================
def fixture_pin() -> dict:
    """Prove a scoped re-run MERGES rather than clobbers.

    Paste #1 lost five of six pins to exactly this: main() rebuilt the manifest
    from scratch on every invocation, so `--stage trap` deleted the record of
    every other stage. The build document cited that manifest as the record.
    """
    log("F-PIN -- manifest pins survive a --stage re-run (I12)")
    tmp = OUT / "_fpin_probe.json"
    a = {"pins": {"alpha": 1}, "artifacts": {"a1": "x"}, "feasibility": {"k": 1}}
    tmp.write_text(json.dumps(a), encoding="utf-8")
    prior = json.loads(tmp.read_text(encoding="utf-8"))
    merged = {"pins": dict(prior.get("pins", {})),
              "artifacts": dict(prior.get("artifacts", {}))}
    for k in ("feasibility", "query_cards"):
        if k in prior:
            merged[k] = prior[k]
    merged["pins"]["beta"] = 2                     # the scoped stage's own pin
    ok = (merged["pins"].get("alpha") == 1 and merged["pins"].get("beta") == 2
          and merged["artifacts"].get("a1") == "x" and "feasibility" in merged)
    tmp.unlink(missing_ok=True)
    log(f"    {'PASS' if ok else 'FAIL'}  prior pins + artifacts + sections carried "
        f"forward alongside the new pin")
    if not ok:
        raise SystemExit("HALT (F-PIN): manifest merge does not preserve prior pins.")
    return {"pass": True}


# ===========================================================================
# CEN-0(b) -- PAXG FETCH (network in scope this paste)
# ===========================================================================
def stage_cen0b(end_day: str = "2026-08-12") -> dict:
    """PAXGUSDT full depth -> D:. Symbol passed explicitly; engine SYMBOLS untouched (I10).

    Graceful on network failure per the contract: a failed fetch is reported and
    classified UNKNOWN, it does not halt the census.
    """
    log("CEN-0(b) -- PAXG fetch (network); engine/cells.py SYMBOLS untouched")
    from engine import data as dl
    from engine.replay import parse_utc
    import engine.cells as cells
    if "PAXGUSDT" in cells.SYMBOLS:
        raise SystemExit("HALT (I10): PAXGUSDT is registered in engine SYMBOLS -- "
                         "this paste must not have changed the engine.")
    log("    I10 check: PAXGUSDT absent from engine SYMBOLS (explicit-symbol path)")

    sym = "PAXGUSDT"
    intervals = ["1m", "5m", "15m", "1h", "4h", "12h"]
    end_ms = parse_utc(end_day)
    dest = KLINES_OUT / sym
    dest.mkdir(parents=True, exist_ok=True)

    out = {"symbol": sym, "dest": str(dest), "intervals": {}, "network_ok": True}
    first_1h = None
    for iv in intervals:
        try:
            detected = dl.detect_first_candle(sym, iv)
            if detected is None:
                out["intervals"][iv] = {"state": "NO-DATA-AT-VENUE"}
                log(f"    {iv:4} venue reports no data")
                continue
            start = dl.first_valid_ms(sym, iv, detected)
            if iv == "1h":
                first_1h = start
            dl.backfill_klines(sym, iv, start, end_ms)
            df = dl.load_klines(sym, iv, start, end_ms)
            p = dest / f"{sym}_{iv}.parquet"
            df.to_parquet(p, index=False)
            o = df["open_time"].to_numpy(np.int64)
            rec = {"state": "OK", "rows": int(len(df)),
                   "first_open": iso(int(o[0])), "last_open": iso(int(o[-1])),
                   "evidence_rows": int((o < CEIL_MS).sum()),
                   "live_rows": int((o >= CEIL_MS).sum()),
                   "path": str(p), "bytes": p.stat().st_size, "sha256": _sha(p)}
            out["intervals"][iv] = rec
            log(f"    {iv:4} rows={rec['rows']:>9,}  {rec['first_open']} -> "
                f"{rec['last_open']}  evidence={rec['evidence_rows']:,}")
        except Exception as exc:
            out["network_ok"] = False
            out["intervals"][iv] = {"state": "FETCH-FAILED", "error": repr(exc)[:300]}
            log(f"    {iv:4} FETCH FAILED: {type(exc).__name__}: {exc}")

    # F-12: classification printed, not assumed
    ev_1h = out["intervals"].get("1h", {}).get("evidence_rows", 0)
    ev_years = ev_1h / (365 * 24) if ev_1h else 0.0
    if not out["network_ok"] and ev_1h == 0:
        cls = "UNKNOWN (fetch failed)"
    elif ev_years >= 2.0:
        cls = "PANEL-ELIGIBLE next cycle (>=2y evidence-era)"
    else:
        cls = "ANNEX (<2y evidence-era)"
    out["evidence_years_1h"] = round(ev_years, 3)
    out["classification"] = cls
    out["rule"] = "contract CEN-0(b): >=2y evidence-era -> panel-eligible next cycle; else ANNEX"
    log(f"    F-12 first bar (1h): "
        f"{out['intervals'].get('1h', {}).get('first_open', 'n/a')}")
    log(f"    F-12 evidence-era 1h rows={ev_1h:,} = {ev_years:.2f}y")
    log(f"    F-12 CLASSIFICATION: {cls}")
    return out


# ===========================================================================
# CEN-1 -- SUBSTRATE
# ===========================================================================
def refusal_events(series: np.ndarray, level: np.ndarray, atr_v: np.ndarray,
                   eps: float = KISS_EPS, delta: float = KISS_DELTA,
                   k: int = KISS_K) -> tuple[np.ndarray, np.ndarray]:
    """The refusal grammar, generic over ANY (series, level) pair.

    approach within eps*ATR -> veer >= delta*ATR within k bars -> no sign change
    of (series - level) in between. What almost fired, recorded beside what fired.

    Both contract limbs run through this one function:
      i-a  EMA<->EMA   series = fast EMA, level = slow EMA  (ratified constants)
      i-b  price<->level  series = close, level = a long EMA or a registry level
           -- the SFP / deviation object. R-8 required it built this paste; it
           had no implementation anywhere in the estate (seq8_extract.py:97-98
           records the gap).

    Semantics are deliberately identical to mc1_program.kiss_v0 (break on the
    FIRST sign change, not reject-if-any; accept a zero-signed touch), so i-a
    reproduces the ratified detector exactly -- asserted by F-KISS-PARITY in
    mc2_program and re-asserted here. Writing a second, subtly different
    grammar for the second limb would make the two limbs incomparable, which is
    precisely what "same grammar" in the contract forbids.

    Returns (flag_at_touch, confirm_index). The touch bar is flagged but the
    event is only KNOWN at the confirmation bar -- I7 queries must filter on
    confirm_index, never on the touch.

    Vectorised over the k-bar lookahead (k passes, not one Python loop per
    touch) -- the scalar form was ~50x slower and CEN-1 runs this over roughly
    ten million bars. The break ORDER is preserved exactly: at each offset,
    non-finite breaks first, then a genuine sign change, then the veer test.
    Getting that order wrong silently changes the event set, so the vectorised
    form is proved equal to the scalar form in F-6-VEC before it is trusted.
    """
    n = len(series)
    flag = np.zeros(n, dtype=bool)
    confirm = np.full(n, -1, dtype=np.int64)
    spread = series - level
    a = np.abs(spread)
    sg = np.sign(spread)
    finite = np.isfinite(spread) & np.isfinite(atr_v) & (atr_v > 0)
    touch = (a <= eps * atr_v) & finite
    if not touch.any():
        return flag, confirm

    idx = np.arange(n)
    alive = touch.copy()          # still scanning (no break yet)
    done = np.zeros(n, dtype=bool)
    for d in range(1, k + 1):
        j = idx + d
        ok_j = j <= (n - 1)
        jj = np.where(ok_j, j, 0)

        # break 1: non-finite at j
        brk = alive & ok_j & ~finite[jj]
        alive &= ~brk
        # break 2: genuine sign change (zero-signed touch keeps scanning)
        sign_chg = (sg[idx] != 0) & (sg[jj] != 0) & (sg[jj] != sg[idx])
        brk2 = alive & ok_j & sign_chg
        alive &= ~brk2
        # veer -> confirm
        hit = alive & ok_j & ~done & (a[jj] >= delta * atr_v[jj])
        flag |= hit
        confirm = np.where(hit, jj, confirm)
        done |= hit
        alive &= ~hit
        alive &= ok_j          # ran off the end
        if not alive.any():
            break
    return flag, confirm


def _refusal_scalar(series, level, atr_v, eps=KISS_EPS, delta=KISS_DELTA, k=KISS_K):
    """Reference implementation -- the literal transcription of kiss_v0's loop.

    Kept solely so the fast path can be proved against it. Never used in
    production: it is ~50x slower. A vectorised rewrite of a detector is the
    classic place for a silent semantic drift, and 'it looked right' is not a
    proof, so F-6-VEC compares them element-for-element on real series.
    """
    n = len(series)
    flag = np.zeros(n, dtype=bool)
    confirm = np.full(n, -1, dtype=np.int64)
    spread = series - level
    a = np.abs(spread)
    sg = np.sign(spread)
    fin = np.isfinite(spread) & np.isfinite(atr_v) & (atr_v > 0)
    touch = (a <= eps * atr_v) & fin
    for i in np.nonzero(touch)[0]:
        s0 = sg[i]
        for j in range(i + 1, min(i + k, n - 1) + 1):
            if not fin[j]:
                break
            if s0 != 0 and sg[j] != 0 and sg[j] != s0:
                break
            if a[j] >= delta * atr_v[j]:
                flag[i] = True
                confirm[i] = j
                break
    return flag, confirm


def fixture_f6_vec(assets: list[str], era: str = "evidence") -> dict:
    """F-6-VEC: the vectorised detector == the scalar reference, exactly."""
    log("F-6-VEC -- vectorised refusal detector vs scalar reference")
    cells, bad = 0, 0
    for sym in assets[:3]:
        for tf in ["1h", "4h"]:
            df = MC2.frame(sym, tf, era)
            av = df["atr"].to_numpy(float)
            for name, s, lv in [("i-a 9_89", df["e9"].to_numpy(), df["e89"].to_numpy()),
                                ("i-b price_e200", df["close"].to_numpy(), df["e200"].to_numpy()),
                                ("i-b price_e500", df["close"].to_numpy(), df["e500"].to_numpy())]:
                f1, c1 = refusal_events(s, lv, av)
                f2, c2 = _refusal_scalar(s, lv, av)
                same = np.array_equal(f1, f2) and np.array_equal(c1, c2)
                cells += 1
                if not same:
                    bad += 1
                    log(f"    FAIL {sym} {tf} {name}: "
                        f"{int((f1 != f2).sum())} flag diffs, "
                        f"{int((c1 != c2).sum())} confirm diffs")
    log(f"    {'PASS' if bad == 0 else 'FAIL'}  {cells - bad}/{cells} cells identical")
    if bad:
        raise SystemExit("HALT (F-6-VEC): the vectorised refusal detector does not "
                         "reproduce the scalar reference. The fast path is wrong.")
    return {"cells": cells, "identical": cells - bad, "pass": True}


def stage_cen1(assets: list[str], era: str = "evidence") -> dict:
    """Full-family cross events, refusal events (both limbs), snapshots.

    I1: era='evidence' keeps every scored row <= the wall.
    I4: EMA500 evidence-side on {1m..12h} only -- 1d/500 is NEVER for 4 of 5
        panel assets, so a 1d/500 column here would be an empty column with a
        misleading header. Enforced by the warm mask, not by a comment.
    R-3: counter_n is a measured column. The TRAP stamp is dead.
    """
    log(f"CEN-1 -- substrate [{era}]")
    TFS = ["5m", "15m", "30m", "1h", "4h", "12h"]
    FAST_TFS = ["5m", "15m", "30m"]
    LONG_EMAS = [200, 300, 450, 500]

    ev_rows, ref_rows = [], []
    cold_head_violations = 0

    for sym in assets:
        for tf in TFS:
            try:
                df = MC2.frame(sym, tf, era)
            except FileNotFoundError:
                continue
            if len(df) < 500:
                continue
            o = df["open_time"].to_numpy(np.int64)
            c = df["close"].to_numpy(float)
            av = df["atr"].to_numpy(float)

            # ---- cross events (scored classes + raw-only 9_25)
            for cls in CROSS_CLASSES + RAW_ONLY_CLASSES:
                fa, sl = MC2.PAIRS[cls]
                need = max(MC2.warmup_bars(fa), MC2.warmup_bars(sl))
                cx = MC2.crosses(df, cls)
                for d in ("up", "down"):
                    ts = cx[d]
                    if not len(ts):
                        continue
                    idx = np.searchsorted(o, ts)
                    # F-PARITY-2: no event may originate in the warm-up region
                    cold_head_violations += int((idx < need).sum())
                    for i, t in zip(idx, ts):
                        if i >= len(c):
                            continue
                        ev_rows.append({
                            "asset": sym, "tf": tf, "event_class": cls,
                            "lattice": "A" if cls in LATTICE_A else
                                       ("B" if cls == "12_25" else "X"),
                            "scored_class": cls not in RAW_ONLY_CLASSES,
                            "dir": d, "ts": int(t), "ts_iso": iso(int(t)),
                            "price": float(c[i]), "atr": float(av[i]),
                            "ribbon_9_89": float((df["e9"][i] - df["e89"][i]) / av[i])
                                if av[i] > 0 and np.isfinite(df["e9"][i]) and np.isfinite(df["e89"][i]) else np.nan,
                            "ribbon_89_200": float((df["e89"][i] - df["e200"][i]) / av[i])
                                if av[i] > 0 and np.isfinite(df["e89"][i]) and np.isfinite(df["e200"][i]) else np.nan,
                            "ribbon_300_450": float((df["e300"][i] - df["e450"][i]) / av[i])
                                if av[i] > 0 and np.isfinite(df["e300"][i]) and np.isfinite(df["e450"][i]) else np.nan,
                            "ribbon_450_500": float((df["e450"][i] - df["e500"][i]) / av[i])
                                if av[i] > 0 and np.isfinite(df["e450"][i]) and np.isfinite(df["e500"][i]) else np.nan,
                        })

            # ---- refusal limb i-a: EMA<->EMA (the ratified kiss)
            for cls, (fa, sl) in [("9_89", (9, 89)), ("12_25", (12, 25)),
                                  ("89_200", (89, 200))]:
                f, conf = refusal_events(df[f"e{fa}"].to_numpy(),
                                         df[f"e{sl}"].to_numpy(), av)
                for i in np.nonzero(f)[0]:
                    ref_rows.append({
                        "asset": sym, "tf": tf, "limb": "i-a", "object": cls,
                        "ts": int(o[i]), "ts_iso": iso(int(o[i])),
                        "confirm_ts": int(o[conf[i]]), "confirm_lag_bars": int(conf[i] - i),
                        "price": float(c[i]), "atr": float(av[i]),
                        "side": "above" if df[f"e{fa}"][i] >= df[f"e{sl}"][i] else "below"})

            # ---- refusal limb i-b: price<->level (R-8, NEW THIS PASTE)
            for L in LONG_EMAS:
                lev = df[f"e{L}"].to_numpy()
                if not np.isfinite(lev).any():
                    continue
                f, conf = refusal_events(c, lev, av)
                for i in np.nonzero(f)[0]:
                    ref_rows.append({
                        "asset": sym, "tf": tf, "limb": "i-b", "object": f"price_e{L}",
                        "ts": int(o[i]), "ts_iso": iso(int(o[i])),
                        "confirm_ts": int(o[conf[i]]), "confirm_lag_bars": int(conf[i] - i),
                        "price": float(c[i]), "atr": float(av[i]),
                        "side": "above" if c[i] >= lev[i] else "below"})
            log(f"    {sym:9} {tf:4} done")

    events = pd.DataFrame(ev_rows)
    refusals = pd.DataFrame(ref_rows)

    # ---- counter_n as a measured column (R-3), on 4h lattice-A armings
    if not events.empty:
        log("    attaching counter_n (measured column; the TRAP stamp is dropped, R-3)")
        cn = []
        for sym in assets:
            fast = events[(events.asset == sym) & (events.tf.isin(FAST_TFS))
                          & (events.lattice == "A")]
            fts = {d: np.sort(fast[fast.dir == d].ts.to_numpy(np.int64))
                   for d in ("up", "down")}
            arm = events[(events.asset == sym) & (events.tf == "4h")
                         & (events.lattice == "A")]
            for r in arm.itertuples(index=False):
                opp = "down" if r.dir == "up" else "up"
                ft = fts[opp]
                lo = r.ts - 24 * 3_600_000
                cn.append({"asset": sym, "tf": "4h", "event_class": r.event_class,
                           "dir": r.dir, "ts": r.ts,
                           "counter_n": int(((ft >= lo) & (ft < r.ts)).sum())})
        counters = pd.DataFrame(cn)
    else:
        counters = pd.DataFrame()

    log(f"    events   : {len(events):,} rows")
    log(f"    refusals : {len(refusals):,} rows "
        f"(i-a {int((refusals.limb=='i-a').sum()) if len(refusals) else 0:,} · "
        f"i-b {int((refusals.limb=='i-b').sum()) if len(refusals) else 0:,})")
    log(f"    F-PARITY-2 cold-head events = {cold_head_violations} (must be 0)")
    if cold_head_violations:
        raise SystemExit(f"HALT (F-PARITY-2): {cold_head_violations} event(s) "
                         f"originate inside an EMA warm-up region.")
    return {"events": events, "refusals": refusals, "counters": counters,
            "cold_head_violations": cold_head_violations,
            "note_ib": ("i-b runs against the long EMAs this paste; the detector "
                        "is generic over any level series, so registry levels "
                        "plug in at CEN-7 without rework")}


def fixture_f6(assets: list[str], era: str = "evidence") -> dict:
    """F-6: refusal determinism + 3 events HAND-VERIFIED per limb.

    Hand-verification means re-deriving each event's three conditions from the
    raw arrays, not re-calling the detector and agreeing with itself. A detector
    checked only against its own output is checked against nothing.
    """
    log("F-6 -- refusal determinism + 3 hand-verified per limb")
    sym, tf = assets[0], "4h"
    df = MC2.frame(sym, tf, era)
    o = df["open_time"].to_numpy(np.int64)
    c = df["close"].to_numpy(float)
    av = df["atr"].to_numpy(float)

    limbs = {"i-a": (df["e9"].to_numpy(), df["e89"].to_numpy()),
             "i-b": (c, df["e200"].to_numpy())}
    out = {"determinism": {}, "hand_verified": {}}
    for name, (s, lv) in limbs.items():
        f1, c1 = refusal_events(s, lv, av)
        f2, c2 = refusal_events(s, lv, av)
        det = bool(np.array_equal(f1, f2) and np.array_equal(c1, c2))
        out["determinism"][name] = det
        log(f"    {'PASS' if det else 'FAIL'}  {name} determinism "
            f"({int(f1.sum())} events, re-run identical)")
        if not det:
            raise SystemExit(f"HALT (F-6): {name} refusal detector is not deterministic.")

        picks = np.nonzero(f1)[0][:3]
        rows = []
        for i in picks:
            j = int(c1[i])
            spread = s - lv
            touch_ok = abs(spread[i]) <= KISS_EPS * av[i]
            veer_ok = abs(spread[j]) >= KISS_DELTA * av[j]
            seg = np.sign(spread[i + 1:j + 1])
            s0 = np.sign(spread[i])
            nosign = bool(not ((seg != 0) & (seg != s0)).any()) if s0 != 0 else True
            within_k = (j - i) <= KISS_K
            ok = bool(touch_ok and veer_ok and nosign and within_k)
            rows.append({"limb": name, "ts": iso(int(o[i])),
                         "confirm_ts": iso(int(o[j])), "lag_bars": j - i,
                         "|spread|@touch/ATR": round(float(abs(spread[i]) / av[i]), 4),
                         "|spread|@confirm/ATR": round(float(abs(spread[j]) / av[j]), 4),
                         "touch<=eps": bool(touch_ok), "veer>=delta": bool(veer_ok),
                         "no_sign_change": nosign, "lag<=k": bool(within_k),
                         "PASS": ok})
            log(f"      {name} {rows[-1]['ts']} -> {rows[-1]['confirm_ts']} "
                f"lag={j-i}  touch={rows[-1]['|spread|@touch/ATR']} "
                f"veer={rows[-1]['|spread|@confirm/ATR']}  "
                f"{'PASS' if ok else 'FAIL'}")
        out["hand_verified"][name] = rows
        if not all(r["PASS"] for r in rows):
            raise SystemExit(f"HALT (F-6): hand verification failed for {name}.")
    out["pass"] = True
    return out


# ===========================================================================
# CEN-3 ruler (R-1) -- used by CEN-2's per-class outcomes
# ===========================================================================
def outcome_block(df: pd.DataFrame, idx: np.ndarray, up: bool, tf: str) -> dict:
    """R-1 ruler: signed TERMINAL return, ATR-normalised at the anchor.

    MFE/|MAE| quality ratio, raw MFE, raw MAE and the toll line print BESIDE it
    but never in place of it. `MFE - MAE` is retired as a discriminant: it is a
    position-in-range statistic, invariant to the terminal price, and its sign
    disagrees with the terminal return on ~40% of anchors.

    Horizons are DURATION-fixed and converted per timeframe, so H100 means the
    same 8h20m on 4h as on 1h.
    """
    c = df["close"].to_numpy(float)
    hi = df["high"].to_numpy(float)
    lo = df["low"].to_numpy(float)
    av = df["atr"].to_numpy(float)
    n = len(c)
    out = {}
    for hname, hms in HORIZONS_MS.items():
        bars = max(1, int(round(hms / TF_MS[tf])))
        term = np.full(len(idx), np.nan)
        mfe = np.full(len(idx), np.nan)
        mae = np.full(len(idx), np.nan)
        for j, i in enumerate(idx):
            if i < 0 or i >= n or not np.isfinite(av[i]) or av[i] <= 0:
                continue
            end = min(i + bars, n - 1)
            if end <= i:
                continue
            sgn = 1.0 if up else -1.0
            term[j] = sgn * (c[end] - c[i]) / av[i]
            seg_hi = hi[i + 1:end + 1].max()
            seg_lo = lo[i + 1:end + 1].min()
            mfe[j] = ((seg_hi - c[i]) if up else (c[i] - seg_lo)) / av[i]
            mae[j] = ((c[i] - seg_lo) if up else (seg_hi - c[i])) / av[i]
        out[hname] = {"terminal": term, "mfe": mfe, "mae": mae, "bars": bars}
    return out


# ===========================================================================
# CEN-2 -- THE ARMED-WINDOW LEDGER (headline: the arming-fate table)
# ===========================================================================
def stage_cen2(assets: list[str], era: str = "evidence") -> dict:
    """Armings on {1h, 4h primary, 12h}; stamps AT the arming; disjoint fates.

    Stamp set is {WALL, KISS/refusal, FIRST}, score 0-3 (R-3 dropped TRAP:
    >=2 fired on ~92% of armings and >=5 was a selection artifact). `counter_n`
    rides along as a measured column so the census can revisit it with a
    pre-registered threshold if it ever wants to.

    Fates are DISJOINT by construction (paste-1 defect 3): the old `aborted`
    flag was true of 431/436 windows including every completed one, so the
    contract's own taxonomy could not be derived from it.
    """
    log(f"CEN-2 -- armed-window ledger [{era}]  W_max={W_MAX} 4h bars")
    step4 = TF_MS["4h"]
    rows = []
    for sym in assets:
        d4 = MC2.frame(sym, "4h", era)
        if len(d4) < 500:
            continue
        o4 = d4["open_time"].to_numpy(np.int64)
        c4 = d4["close"].to_numpy(float)
        a4 = d4["atr"].to_numpy(float)
        e89 = d4["e89"].to_numpy(float)

        # 1d frame for the WALL second limb, indexed by bar CLOSE (I7).
        d1_close_ms = d1_e200 = d1_atr = None
        try:
            d1 = MC2.frame(sym, "1d", era)
            if len(d1) > 10:
                d1_close_ms = d1["open_time"].to_numpy(np.int64) + TF_MS["1d"]
                d1_e200 = d1["e200"].to_numpy(float)
                d1_atr = d1["atr"].to_numpy(float)
        except Exception:
            pass

        cx = {cls: MC2.crosses(d4, cls) for cls in
              ["9_89", "9_200", "89_200", "12_25", "25_89"]}
        # refusal (i-a 9/89) flags, for the KISS stamp at the arming
        kiss_flag, _ = refusal_events(d4["e9"].to_numpy(), e89, a4)

        for d in ("up", "down"):
            opp = "down" if d == "up" else "up"
            armings = cx["9_89"][d]
            counter = cx["9_89"][opp]
            trig_12 = cx["12_25"][d]
            trig_25 = cx["25_89"][d]
            seal = cx["89_200"][d]
            a4_all = np.sort(np.concatenate(
                [cx[c][d] for c in ("9_89", "9_200", "89_200")]))

            for t in armings:
                i = int(np.searchsorted(o4, t))
                if i >= len(c4):
                    continue
                cap = t + W_MAX * step4
                nxt = counter[counter > t]
                closed_by = "counter-arming" if (len(nxt) and nxt[0] < cap) else "W_max"
                close = min(cap, nxt[0]) if len(nxt) else cap

                # ---- stamps AT the arming (arming-instant features only)
                # WALL is TWO limbs per the pinned constant: 4h-e89 OR 1d-e200,
                # limb recorded. An earlier draft implemented only the 4h limb
                # and still emitted a P-ARM-1 verdict -- a registration verdict
                # on a half-built stamp is worse than no verdict.
                limb4 = bool(np.isfinite(e89[i]) and a4[i] > 0
                             and abs(c4[i] - e89[i]) <= WALL_ATR * a4[i])
                limb1 = False
                if d1_close_ms is not None:
                    kk = int(np.searchsorted(d1_close_ms, int(t), "right")) - 1
                    if kk >= 0 and np.isfinite(d1_e200[kk]) and d1_atr[kk] > 0:
                        limb1 = bool(abs(c4[i] - d1_e200[kk]) <= WALL_ATR * d1_atr[kk])
                wall = bool(limb4 or limb1)
                wall_limb = ("both" if (limb4 and limb1) else "4h" if limb4
                             else "1d" if limb1 else "none")
                lo20 = t - FIRST_N * step4
                first = bool(not ((a4_all >= lo20) & (a4_all < t)).any())
                k_lo = max(0, i - KISS_K)
                kiss = bool(kiss_flag[k_lo:i + 1].any())
                score = int(wall) + int(kiss) + int(first)

                in12 = trig_12[(trig_12 > t) & (trig_12 <= close)]
                in25 = trig_25[(trig_25 > t) & (trig_25 <= close)]
                has_trig = bool(len(in12) or len(in25))
                first_trig = min([x[0] for x in (in12, in25) if len(x)]) if has_trig else None

                sl = seal[(seal >= t) & (seal <= t + SEAL_K * step4)]
                sealed = bool(len(sl))

                fate = ("COMPLETED" if has_trig
                        else "ABORTED" if closed_by == "counter-arming"
                        else "ROTTED")
                rows.append({
                    "asset": sym, "tf": "4h", "dir": d,
                    "arming_ts": int(t), "arming_iso": iso(int(t)),
                    "arming_idx": i,
                    "window_close_ts": int(close),
                    "window_width_bars": float((close - t) / step4),
                    "closed_by": closed_by,
                    "WALL": wall, "wall_limb": wall_limb,
                    "KISS": kiss, "FIRST": first,
                    "stamp_score": score, "strict_core": bool(score == 3),
                    "has_trigger": has_trig,
                    "trigger_class": ("12_25" if len(in12) and (not len(in25) or in12[0] <= in25[0])
                                      else "25_89" if len(in25) else None),
                    "trigger_lag_bars": (float((first_trig - t) / step4)
                                         if first_trig is not None else np.nan),
                    "SEALED": sealed,
                    "seal_lag_bars": (float((sl[0] - t) / step4) if sealed else np.nan),
                    "entry_before_seal": bool(has_trig and sealed and first_trig < sl[0]),
                    "fate": fate,
                })
    led = pd.DataFrame(rows)
    if led.empty:
        return {"ledger": led}

    # ---- outcomes per arming under the R-1 ruler
    log("    attaching R-1 outcomes (signed terminal return, ATR-normalised)")
    for sym, g in led.groupby("asset", sort=True):
        d4 = MC2.frame(sym, "4h", era)
        for d in ("up", "down"):
            sel = (led.asset == sym) & (led.dir == d)
            if not sel.any():
                continue
            idx = led.loc[sel, "arming_idx"].to_numpy(int)
            ob = outcome_block(d4, idx, d == "up", "4h")
            for hname, blk in ob.items():
                led.loc[sel, f"term_{hname}"] = blk["terminal"]
                led.loc[sel, f"mfe_{hname}"] = blk["mfe"]
                led.loc[sel, f"mae_{hname}"] = blk["mae"]

    # ---- THE ARMING-FATE TABLE (the crown)
    fate_tab = (led.groupby(["fate", "has_trigger"])
                .agg(n=("arming_ts", "size"),
                     median_term_H100=("term_H100", "median"),
                     median_width=("window_width_bars", "median"))
                .reset_index())
    log("    ARMING-FATE TABLE (disjoint):")
    for r in fate_tab.itertuples(index=False):
        log(f"      {r.fate:10} trig={str(r.has_trigger):5} n={r.n:5d} "
            f"median_term_H100={r.median_term_H100:+.4f} "
            f"median_width={r.median_width:.0f}")

    # ---- P-ARM-1 under R-2 (asset-cluster CI), registration text first (F-8)
    log("    P-ARM-1 [60%] (registration text precedes the result, F-8):")
    log("      'WALL-true armings -> higher trigger-within-151 rate AND higher")
    log("       post-trigger terminal return than WALL-false.'")
    mask = led["WALL"].to_numpy(bool)
    rate_t = float(led.loc[mask, "has_trigger"].mean())
    rate_f = float(led.loc[~mask, "has_trigger"].mean())
    ci = cluster_ci(led["term_H100"].to_numpy(float), led["asset"].to_numpy(), mask)
    log(f"      trigger-within-151: WALL-true {rate_t:.3f} vs WALL-false {rate_f:.3f}")
    log(f"      terminal H100 cluster CI on the difference: "
        f"[{ci['lo']},{ci['hi']}] {'EXCL-0' if ci['excludes_zero'] else 'straddles 0'}")
    verdict = ("SUPPORTED" if (rate_t > rate_f and ci["excludes_zero"]
                               and (ci["point"] or 0) > 0) else "NOT SUPPORTED")
    log(f"      VERDICT: {verdict}")

    # ---- MANDATORY CONFOUND DISCLOSURE.  Not a footnote: without it the
    # trigger-rate half of this registration reads as a finding when it is an
    # artifact of exposure time. WALL means price sits within 0.5*ATR of the
    # e89 -- i.e. exactly where the 9/89 is about to cross back -- so WALL-true
    # windows close fast, and a window that closes in 7 bars cannot contain a
    # trigger no matter what the tape does.
    w_true = led.loc[mask, "window_width_bars"]
    w_false = led.loc[~mask, "window_width_bars"]
    cond = led[led.window_width_bars >= 48]
    ct = float(cond.loc[cond.WALL, "has_trigger"].mean()) if cond.WALL.any() else float("nan")
    cf = float(cond.loc[~cond.WALL, "has_trigger"].mean()) if (~cond.WALL).any() else float("nan")
    log("      CONFOUND (mandatory disclosure):")
    log(f"        median window width  WALL-true {w_true.median():.0f} bars vs "
        f"WALL-false {w_false.median():.0f} bars")
    log(f"        conditioned on width >= 48: trigger rate WALL-true {ct:.3f} vs "
        f"WALL-false {cf:.3f}  -> the gap closes")
    log("        => the trigger-rate limb of P-ARM-1 measures EXPOSURE TIME, not")
    log("           the WALL stamp. It cannot be evaluated as written; a hazard /")
    log("           competing-risk framing is required. Reported, not fixed.")
    confound = {
        "median_width_wall_true": float(w_true.median()),
        "median_width_wall_false": float(w_false.median()),
        "trigger_rate_conditioned_width_ge_48": {"wall_true": round(ct, 6),
                                                 "wall_false": round(cf, 6)},
        "reading": ("WALL-true windows close fast (price is adjacent to the e89, "
                    "where the counter-cross is imminent), so the trigger-rate "
                    "limb is confounded by exposure time; the terminal-return "
                    "limb is not affected by this mechanism"),
    }

    return {"ledger": led, "fate_table": fate_tab,
            "p_arm_1": {"registration":
                        "WALL-true armings -> higher trigger-within-151 rate AND "
                        "higher post-trigger terminal return than WALL-false",
                        "prior": 0.60,
                        "trigger_rate_wall_true": round(rate_t, 6),
                        "trigger_rate_wall_false": round(rate_f, 6),
                        "terminal_H100_cluster_ci": ci,
                        "criterion": "R-2 asset-cluster 90% CI excluding zero",
                        "verdict": verdict,
                        "confound_disclosure": confound}}


# ===========================================================================
# I6 LENSES -- chaining is a PARAMETER, never a property of the data
# ===========================================================================
LENS_WINDOW_MS = 24 * 3_600_000          # the pinned trailing-24h window


def assign_chains_seq8(ev, rule, window_ms=LENS_WINDOW_MS):
    """Cascade id + depth per event, using SEQ8's OWN builder.

    This DELEGATES to `seq8_views.build_cascades` rather than reimplementing it.
    Two earlier drafts of this function guessed the semantics and both
    degenerated -- one gave max_depth=1 for every arming, the other pooled the
    whole lattice into 23 chains of mean depth 1,733. The real rule has three
    properties that are not obvious from the name:

      * cascades are built per (asset, EVENT CLASS), not over a pooled lattice;
      * every admitted rung must be a NEW TIMEFRAME -- a cascade is a ladder
        across timeframes, so a re-firing on a TF already in the chain does not
        extend it;
      * chaining is greedy and NON-OVERLAPPING: an event consumed by one
        cascade cannot start another.

    `window_chained` SKIPS counter-direction events; `direction_consistent`
    TERMINATES on the first one. That single difference is the whole of the
    P-i/P-iv view-contingency: direction_consistent ends chains exactly where
    outcomes are contested, which moves the outcome clock.

    Reimplementing a definition the estate already owns is how two lenses stop
    being comparable to the eight views already on disk. Import it.
    """
    import seq8_views as S8V
    out = []
    for (sym, klass), g in ev.groupby(["asset", "event_class"], sort=True):
        g = g.assign(_tfi=g.tf.map(S8V.TFI)).sort_values(
            ["bar_close_ms", "_tfi", "dir"], kind="mergesort").reset_index(drop=True)
        evs = g.to_dict("records")
        chains = S8V.build_cascades(evs, window_ms, rule)
        for ci, (members, _ended) in enumerate(chains):
            for depth, m in enumerate(members, start=1):
                out.append({"asset": sym, "event_class": klass,
                            "ts": int(evs[m]["ts"]), "tf": evs[m]["tf"],
                            "chain_id": f"{sym}|{klass}|{ci}", "depth": depth,
                            "chain_len": len(members)})
    return pd.DataFrame(out)


# ===========================================================================
# CEN-3 -- OUTCOMES (ruler R-1), dual-lens (I6), held-in-time
# ===========================================================================
def stage_cen3(assets: list[str], era: str = "evidence") -> dict:
    """Terminal return anchored at the ARMING and at each TRIGGER, both lenses.

    R-1 ruler throughout: signed terminal return, ATR-normalised at the anchor.
    MFE, MAE, the MFE/|MAE| quality ratio and the toll line print beside it --
    never in place of it.

    The toll line is the contract's global 10 bps round trip. Printed in ATR
    units per asset, because an excursion measured in ATR cannot be compared to
    a cost measured in bps without the conversion, and a table that omits it
    invites reading a 0.05-ATR edge as real when the toll eats it.
    """
    log(f"CEN-3 -- outcomes [{era}]  ruler: signed terminal return / ATR (R-1)")
    led = pd.read_parquet(OUT / "cen2" / "cen2_ledger.parquet")
    log(f"    armings from CEN-2 ledger: {len(led):,}")

    # ---- toll line, per asset, in ATR units (I8 'toll beside every excursion')
    toll = {}
    for sym in assets:
        d4 = MC2.frame(sym, "4h", era)
        px = d4["close"].to_numpy(float); av = d4["atr"].to_numpy(float)
        ok = np.isfinite(px) & np.isfinite(av) & (av > 0)
        toll[sym] = float(np.median((TOLL_BPS_ROUND_TRIP / 10000.0) * px[ok] / av[ok]))
    log(f"    toll line ({TOLL_BPS_ROUND_TRIP:.0f} bps round trip) in ATR units:")
    for s, v in toll.items():
        log(f"      {s:9} {v:.4f} ATR")
    led["toll_atr"] = led["asset"].map(toll)

    # ---- I6: both lenses, always.
    #
    # Chains are built over the FULL lattice-A event stream (9_89, 9_200,
    # 89_200 across every timeframe), not over the 4h 9/89 armings alone.
    # That distinction is not cosmetic: consecutive 9/89 crosses on one
    # timeframe STRICTLY ALTERNATE direction, so a direction-change rule breaks
    # every chain at depth 1 and `direction_consistent` degenerates into a
    # constant. An earlier draft did exactly that and printed max_depth=1 for
    # all 848 armings -- a lens that cannot vary is not a lens, and I6's
    # "the other lens ALWAYS printed" would have been satisfied in letter only.
    log("    I6 dual-lens: cascades via seq8_views.build_cascades (the estate's own rule)")
    ev = pd.read_parquet(OUT / "cen1" / "cen1_events.parquet",
                         columns=["asset", "tf", "event_class", "dir", "ts"])
    ev = ev[ev.event_class.isin(LATTICE_A)].copy()
    ev["bar_close_ms"] = ev["ts"] + ev["tf"].map(TF_MS)
    log(f"      lattice-A stream: {len(ev):,} events, {ev.tf.nunique()} timeframes, "
        f"{ev.event_class.nunique()} classes")
    for rule in ("window_chained", "direction_consistent"):
        ch = assign_chains_seq8(ev, rule)
        # Armings are 4h 9_89 events. The key MUST include the timeframe:
        # (asset, ts) alone is not unique because a 4h and a 12h bar can share
        # an open_time (00:00), which silently turns the lookup into a Series.
        k = ch[(ch.event_class == "9_89") & (ch.tf == "4h")]
        dmap = dict(zip(zip(k.asset, k.ts), k.depth))
        lmap = dict(zip(zip(k.asset, k.ts), k.chain_len))
        pairs = list(zip(led.asset, led.arming_ts))
        led[f"depth_{rule}"] = [int(dmap.get(p, 0)) for p in pairs]
        led[f"chainlen_{rule}"] = [int(lmap.get(p, 0)) for p in pairs]
        d = led[f"depth_{rule}"]
        log(f"      {rule:22} cascades={ch.chain_id.nunique():6d} "
            f"max_depth={int(ch.depth.max())} mean_len={ch.chain_len.mean():.2f} "
            f"| arming depth: max={int(d.max())} mean={d.mean():.2f} "
            f"unmatched={int((d == 0).sum())}")

    # ---- trigger-anchored outcomes (arming-anchored already on the ledger)
    log("    trigger-anchored terminal returns (R-1)")
    trig_rows = []
    for sym in assets:
        d4 = MC2.frame(sym, "4h", era)
        o4 = d4["open_time"].to_numpy(np.int64)
        sub = led[(led.asset == sym) & led.has_trigger]
        for d in ("up", "down"):
            s2 = sub[sub.dir == d]
            if s2.empty:
                continue
            t_ts = (s2.arming_ts.to_numpy(np.int64)
                    + (s2.trigger_lag_bars.to_numpy(float) * TF_MS["4h"]).astype(np.int64))
            idx = np.searchsorted(o4, t_ts)
            idx = np.clip(idx, 0, len(o4) - 1)
            ob = outcome_block(d4, idx, d == "up", "4h")
            rec = {"asset": sym, "dir": d, "arming_ts": s2.arming_ts.to_numpy(),
                   "trigger_class": s2.trigger_class.to_numpy()}
            for h, blk in ob.items():
                rec[f"trig_term_{h}"] = blk["terminal"]
                rec[f"trig_mfe_{h}"] = blk["mfe"]
                rec[f"trig_mae_{h}"] = blk["mae"]
            trig_rows.append(pd.DataFrame(rec))
    trig = pd.concat(trig_rows, ignore_index=True) if trig_rows else pd.DataFrame()

    # ---- held-in-time split (I8)
    mid = int(led.arming_ts.median())
    led["time_half"] = np.where(led.arming_ts <= mid, "early", "late")
    log(f"    held-in-time split at {iso(mid)}: "
        f"early={int((led.time_half=='early').sum())} late={int((led.time_half=='late').sum())}")

    # ---- the outcome panel: per asset x direction x half, both lenses printed
    def panel(df, by):
        rows = []
        for keys, g in df.groupby(by, sort=True):
            keys = keys if isinstance(keys, tuple) else (keys,)
            r = dict(zip(by, keys))
            r["n"] = int(len(g))
            for h in HORIZONS_MS:
                t = g[f"term_{h}"].dropna()
                mf = g[f"mfe_{h}"].dropna()
                ma = g[f"mae_{h}"].dropna()
                r[f"median_term_{h}"] = round(float(t.median()), 6) if len(t) else None
                r[f"median_mfe_{h}"] = round(float(mf.median()), 6) if len(mf) else None
                r[f"median_mae_{h}"] = round(float(ma.median()), 6) if len(ma) else None
                r[f"quality_{h}"] = (round(float(mf.median() / ma.median()), 4)
                                     if len(mf) and len(ma) and ma.median() > 0 else None)
            r["toll_atr"] = round(float(g["toll_atr"].median()), 4)
            rows.append(r)
        return pd.DataFrame(rows)

    by_asset = panel(led, ["asset", "dir"])
    by_half = panel(led, ["time_half"])
    by_depth_wc = panel(led.assign(depth_bucket=np.minimum(led.depth_window_chained, 4)),
                        ["depth_bucket"])
    by_depth_dc = panel(led.assign(depth_bucket=np.minimum(led.depth_direction_consistent, 4)),
                        ["depth_bucket"])

    log("    OUTCOME PANEL by asset x direction (terminal H100, ATR; toll beside):")
    for r in by_asset.itertuples(index=False):
        log(f"      {r.asset:9} {r.dir:5} n={r.n:4d} term={r.median_term_H100:+.4f} "
            f"mfe={r.median_mfe_H100:.3f} mae={r.median_mae_H100:.3f} "
            f"Q={r.quality_H100} toll={r.toll_atr:.3f}")
    log("    DUAL-LENS depth panel (I6 -- both always printed):")
    log("      window_chained (PRIMARY for entry claims):")
    for r in by_depth_wc.itertuples(index=False):
        log(f"        depth{r.depth_bucket} n={r.n:4d} term_H100={r.median_term_H100:+.4f}")
    log("      direction_consistent (printed, not primary here):")
    for r in by_depth_dc.itertuples(index=False):
        log(f"        depth{r.depth_bucket} n={r.n:4d} term_H100={r.median_term_H100:+.4f}")

    # ---- clarification (1): fate-stratified view WITH the caveat in the header
    CAVEAT = ("MECHANICAL SEPARATION -- an ABORTED window is a regime flip INSIDE "
              "the horizon, so its terminal return is negative BY CONSTRUCTION. "
              "The sign of this split is NOT a finding.")
    fate_rows = []
    for f, g in led.groupby("fate", sort=True):
        r = {"fate": f, "n": int(len(g)), "_caveat": CAVEAT}
        for h in HORIZONS_MS:
            t = g[f"term_{h}"].dropna()
            r[f"median_term_{h}"] = round(float(t.median()), 6) if len(t) else None
            r[f"p25_term_{h}"] = round(float(t.quantile(.25)), 6) if len(t) else None
            r[f"p75_term_{h}"] = round(float(t.quantile(.75)), 6) if len(t) else None
        r["median_width_bars"] = round(float(g.window_width_bars.median()), 2)
        fate_rows.append(r)
    by_fate = pd.DataFrame(fate_rows)
    log(f"    FATE-STRATIFIED VIEW [{CAVEAT}]")
    for r in by_fate.itertuples(index=False):
        log(f"      {r.fate:10} n={r.n:4d} term_H100={r.median_term_H100:+.4f} "
            f"[p25 {r.p25_term_H100:+.3f}, p75 {r.p75_term_H100:+.3f}] "
            f"width={r.median_width_bars:.0f}")

    # ---- P-REL-1, scored here (text before result, F-8)
    log("    P-REL-1 [60%] (entry lens = 24h|window_chained):")
    log("      'windows with an in-window 12_25 trigger -> higher trigger-anchored")
    log("       terminal return than A-only windows.'")
    rel = None
    if not trig.empty:
        j = trig.merge(led[["asset", "arming_ts", "trigger_class"]].drop_duplicates(),
                       on=["asset", "arming_ts"], how="left", suffixes=("", "_led"))
        mask = (j["trigger_class"] == "12_25").to_numpy(bool)
        vals = j["trig_term_H100"].to_numpy(float)
        clus = j["asset"].to_numpy()
        if mask.sum() >= 8 and (~mask).sum() >= 8:
            rel_ci = cluster_ci(vals, clus, mask)
            verdict = ("SUPPORTED" if (rel_ci["excludes_zero"] and (rel_ci["point"] or 0) > 0)
                       else "NOT SUPPORTED")
            log(f"      12_25-triggered n={int(mask.sum())} vs other n={int((~mask).sum())}")
            log(f"      cluster CI on the difference: [{rel_ci['lo']},{rel_ci['hi']}] "
                f"{'EXCL-0' if rel_ci['excludes_zero'] else 'straddles 0'}")
            log(f"      VERDICT: {verdict}")
            rel = {"registration": ("windows with an in-window 12_25 trigger -> higher "
                                   "trigger-anchored terminal return than A-only windows"),
                   "prior": 0.60, "lens": "24h|window_chained",
                   "n_12_25": int(mask.sum()), "n_other": int((~mask).sum()),
                   "cluster_ci": rel_ci, "verdict": verdict,
                   "criterion": "R-2 asset-cluster 90% CI excluding zero"}
        else:
            log("      INSUFFICIENT SAMPLE -- not scored")
            rel = {"verdict": "NOT SCORED (insufficient sample)", "prior": 0.60}

    return {"ledger": led, "trigger_outcomes": trig, "by_asset": by_asset,
            "by_half": by_half, "by_depth_window_chained": by_depth_wc,
            "by_depth_direction_consistent": by_depth_dc, "by_fate": by_fate,
            "toll_atr": toll, "fate_caveat": CAVEAT, "p_rel_1": rel}


# ===========================================================================
# MANIFEST (I12 -- merge, never clobber)
# ===========================================================================
def load_manifest(path: Path, scoped: bool) -> dict:
    prior = {}
    if scoped and path.exists():
        try:
            prior = json.loads(path.read_text(encoding="utf-8"))
            log(f"  merging into existing manifest "
                f"({len(prior.get('pins', {}))} pin(s), "
                f"{len(prior.get('stages', {}))} stage(s))")
        except Exception as exc:
            raise SystemExit(f"HALT: manifest {path} unreadable ({exc}); "
                             f"refusing to overwrite.")
    man = {
        "program": "census2a_program.py",
        "contract": "exchange/queue/2026-08-12_CENSUS2A_v0.3_RESOLVED_APOLLO.md",
        "contract_sha256": "b0da051b894fc8586fab466fcf99cb0390763551d0d67bbac83743abc1547a6a",
        "seed": SEED,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ceil_ms": CEIL_MS,
        "pins": dict(prior.get("pins", {})),
        "artifacts": dict(prior.get("artifacts", {})),
        "fixtures": dict(prior.get("fixtures", {})),
        "stages": dict(prior.get("stages", {})),
    }
    if prior:
        man["merged_from"] = prior.get("generated_utc")
    return man


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="CENSUS-2A")
    ap.add_argument("--stage", default="all")
    ap.add_argument("--end", default="2026-08-12")
    args = ap.parse_args(argv)
    t0 = time.time()
    scoped = args.stage != "all"

    log(f"CENSUS-2A -- stage={args.stage} seed={SEED}")
    log("  contract sha b0da051b894fc8586fab466fcf99cb0390763551d0d67bbac83743abc1547a6a")
    pre = stage_preflight()

    mp = OUT / "census2a_manifest.json"
    man = load_manifest(mp, scoped)
    man["preflight"] = pre

    def run(nm):
        return args.stage in ("all", nm)

    # Fixtures ALWAYS run first -- F-GUARD gates every sweep stage.
    man["fixtures"]["F-GUARD"] = fixture_guard()
    man["fixtures"]["F-PIN"] = fixture_pin()

    if run("cen0b"):
        man["stages"]["CEN-0b"] = stage_cen0b(args.end)

    if run("cen1"):
        man["fixtures"]["F-6-VEC"] = fixture_f6_vec(PANEL)
        man["fixtures"]["F-6"] = fixture_f6(PANEL)
        c1 = stage_cen1(PANEL + ANNEX, "evidence")
        sub = OUT / "cen1"
        sub.mkdir(parents=True, exist_ok=True)
        summary = {}
        for name, df, keys in [
                ("cen1_events", c1["events"], ["asset", "tf", "ts", "event_class", "dir"]),
                ("cen1_refusals", c1["refusals"], ["asset", "tf", "limb", "object", "ts"]),
                ("cen1_counters", c1["counters"], ["asset", "ts", "event_class", "dir"])]:
            if df is None or df.empty:
                continue
            d = df.sort_values([k for k in keys if k in df.columns]).reset_index(drop=True)
            for col in d.columns:
                if d[col].dtype.kind == "f":
                    d[col] = d[col].round(R6)
            p = sub / f"{name}.parquet"
            d.to_parquet(p, index=False)
            man["artifacts"][name] = {
                "path": str(p), "rows": int(len(d)), "bytes": p.stat().st_size,
                "sha256": _sha(p), "class": "EVIDENCE -- exploration-classic"}
            summary[name] = int(len(d))
            log(f"    wrote {name}.parquet rows={len(d):,} "
                f"sha={man['artifacts'][name]['sha256'][:12]}")
        man["stages"]["CEN-1"] = {
            "era": "evidence", "rows": summary,
            "cold_head_violations": c1["cold_head_violations"],
            "scored_classes": CROSS_CLASSES,
            "raw_only_classes": RAW_ONLY_CLASSES,
            "note_ib": c1["note_ib"],
            "trap_stamp": "DROPPED (R-3); counter_n is a measured column only"}

    if run("cen2"):
        c2 = stage_cen2(PANEL, "evidence")
        led = c2.get("ledger")
        if led is not None and not led.empty:
            sub = OUT / "cen2"; sub.mkdir(parents=True, exist_ok=True)
            for name, df, keys in [
                    ("cen2_ledger", led, ["asset", "dir", "arming_ts"]),
                    ("cen2_fate_table", c2["fate_table"], ["fate", "has_trigger"])]:
                d = df.sort_values([k for k in keys if k in df.columns]).reset_index(drop=True)
                for col in d.columns:
                    if d[col].dtype.kind == "f":
                        d[col] = d[col].round(R6)
                pth = sub / f"{name}.parquet"
                d.to_parquet(pth, index=False)
                man["artifacts"][name] = {
                    "path": str(pth), "rows": int(len(d)), "bytes": pth.stat().st_size,
                    "sha256": _sha(pth), "class": "EVIDENCE -- exploration-classic"}
                log(f"    wrote {name}.parquet rows={len(d):,} "
                    f"sha={man['artifacts'][name]['sha256'][:12]}")
            man["stages"]["CEN-2"] = {
                "era": "evidence", "W_max": W_MAX,
                "armings": int(len(led)),
                "stamp_set": ["WALL", "KISS", "FIRST"],
                "trap_stamp": "DROPPED (R-3)",
                "fates": {str(k): int(v) for k, v in led.fate.value_counts().items()},
                "strict_core_n": int(led.strict_core.sum()),
                "ruler": "R-1 signed terminal return, ATR-normalised, duration-fixed horizons",
                "toll_bps_round_trip": TOLL_BPS_ROUND_TRIP}
            man["registrations"] = man.get("registrations", {})
            man["registrations"]["P-ARM-1"] = c2["p_arm_1"]

    if run("cen3"):
        c3 = stage_cen3(PANEL, "evidence")
        sub = OUT / "cen3"; sub.mkdir(parents=True, exist_ok=True)
        for name, df, keys in [
                ("cen3_by_asset", c3["by_asset"], ["asset", "dir"]),
                ("cen3_by_half", c3["by_half"], ["time_half"]),
                ("cen3_by_depth_window_chained", c3["by_depth_window_chained"], ["depth_bucket"]),
                ("cen3_by_depth_direction_consistent", c3["by_depth_direction_consistent"], ["depth_bucket"]),
                ("cen3_by_fate", c3["by_fate"], ["fate"]),
                ("cen3_trigger_outcomes", c3["trigger_outcomes"], ["asset", "dir", "arming_ts"]),
                ("cen3_ledger_lensed", c3["ledger"], ["asset", "dir", "arming_ts"])]:
            if df is None or df.empty:
                continue
            d = df.sort_values([k for k in keys if k in df.columns]).reset_index(drop=True)
            for col in d.columns:
                if d[col].dtype.kind == "f":
                    d[col] = d[col].round(R6)
            pth = sub / f"{name}.parquet"
            d.to_parquet(pth, index=False)
            man["artifacts"][name] = {
                "path": str(pth), "rows": int(len(d)), "bytes": pth.stat().st_size,
                "sha256": _sha(pth), "class": "EVIDENCE -- exploration-classic"}
            log(f"    wrote {name}.parquet rows={len(d):,} "
                f"sha={man['artifacts'][name]['sha256'][:12]}")
        man["stages"]["CEN-3"] = {
            "era": "evidence", "ruler": "R-1 signed terminal return / ATR at anchor",
            "horizons": {k: v for k, v in HORIZONS_MS.items()},
            "toll_bps_round_trip": TOLL_BPS_ROUND_TRIP,
            "toll_atr_by_asset": c3["toll_atr"],
            "lenses_printed": ["window_chained", "direction_consistent"],
            "entry_lens_primary": "24h|window_chained (I6)",
            "fate_caveat": c3["fate_caveat"]}
        man["registrations"] = man.get("registrations", {})
        if c3.get("p_rel_1"):
            man["registrations"]["P-REL-1"] = c3["p_rel_1"]

    man["elapsed_s"] = round(time.time() - t0, 1)
    mp.write_text(json.dumps(man, indent=2, default=str), encoding="utf-8")
    lp = OUT / "census2a_run_log.txt"
    mode = "a" if scoped else "w"
    with open(lp, mode, encoding="utf-8", newline="\n") as fh:
        if scoped:
            fh.write(f"\n--- scoped re-run (--stage {args.stage}) ---\n")
        fh.write("\n".join(_LOG) + "\n")
    log(f"manifest -> {mp}")
    log(f"done in {man['elapsed_s']}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
