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

RESIDENCY (I2).  RESTATED 2026-08-15 under DATA RESIDENCY v2: all bulk is born
  LOCAL, under `~/Naiad/research_outputs/census2a/**`, resolved repo-relative
  from ROOT rather than from a drive letter.  The original rule read "born on
  D:/Naiad/..." and was correct for the Windows estate; v2 moved the substrate
  home, so the gate below asserts containment under ROOT instead of a drive.
  `wait_for_drive` never raises by design, so the HALT is the caller's -- it now
  guards BACKUP writes to the LaCie, not substrate reads.
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
# `drive_wait` is deliberately NOT imported here any more (v2, 2026-08-15): the
# substrate is local, so nothing in this program waits on an external volume.
# drive_wait now guards BACKUP writes only -- see scripts/backup_estate.py.

SEED = 20260812
R6 = 6

OUT = ROOT / "research_outputs" / "census2a"
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
# A1-FAN (run 3, VETO): {200_500, 300_500} join the scored cross classes.
CROSS_CLASSES = ["9_89", "9_200", "89_200", "12_25", "25_89", "300_450", "450_500",
                 "200_500", "300_500"]

# A1-FAN state columns. The ruling names KNOT's five EMAs explicitly but says only
# "six-EMA" for FAN. READING TAKEN: the six are KNOT's five plus the fast line --
# {9, 89, 200, 300, 450, 500}. That is the only six-member set the ruling's own
# vocabulary supplies, but it IS a reading, not a quotation, and it is flagged as
# such in the build document so the operator can correct it by name.
FAN_EMAS = [9, 89, 200, 300, 450, 500]
KNOT_EMAS = [89, 200, 300, 450, 500]
RAW_ONLY_CLASSES = ["9_25"]
LATTICE_A = ["9_89", "9_200", "89_200"]

# I12: every dict-valued manifest section that ACCUMULATES across --stage
# re-runs. Named once so a new section cannot be added to the writer and
# forgotten in the merge -- which is exactly how P-ARM-1 was destroyed.
MERGED_SECTIONS = ["pins", "artifacts", "fixtures", "stages", "registrations"]
# Cascade membership is NOT unique under window_chained (build_cascades lets an
# event JOIN several cascades). The rule below is PINNED BY NAME so the depth
# column is a choice on the record rather than whatever dict insertion order
# happened to leave last. "depth_min" = the shallowest cascade the arming
# belongs to, i.e. the earliest rung it occupies.
DEPTH_TIE_RULE = "depth_min"
# Whole-run sections that are replaced, not merged, when their stage re-runs.
CARRIED_SECTIONS = ["feasibility", "query_cards"]

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
    log("PREFLIGHT -- I3 identity (in code) + I2 residency gate")
    import subprocess
    checks = []
    cwd = str(Path.cwd()).replace("\\", "/")
    # I3, two-sided, RESTATED 2026-08-15 (v2).  The old positive limb tested for
    # a "c:/naiad" suffix; on this platform that can never pass, so the gate was
    # not strict -- it was DEAD, and a gate that always fails is as useless as
    # one that always passes.  The v2 limb names $HOME/Naiad, and the negative
    # limb grew to cover the two other cloud roots that corrupt bulk writes.
    checks.append(("pwd == $HOME/Naiad",
                   Path.cwd().resolve() == (Path.home() / "Naiad").resolve(), cwd))
    low = cwd.lower()
    checks.append(("pwd cloud-free",
                   not any(m in low for m in
                           ("onedrive", "com~apple~clouddocs", "mobile documents")), cwd))

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

    # I2, RESTATED 2026-08-15 (v2).  Bulk is born LOCAL now, so there is no
    # external drive to wait on for a substrate write and `wait_for_drive` is
    # gone from this path -- it guards BACKUP writes to the LaCie instead.
    # The residency assertion keeps its exact original intent (bulk lands where
    # residency says) and only changes what "where" means.  The old form,
    # `OUT.drive.upper() != "D:"`, could never pass here: Path.drive is always
    # "" on POSIX, so it halted unconditionally.
    try:
        OUT.resolve().relative_to((ROOT / "research_outputs").resolve())
    except ValueError:
        raise SystemExit(f"HALT (I2): output root {OUT} is not under "
                         f"{ROOT / 'research_outputs'}.")
    OUT.mkdir(parents=True, exist_ok=True)
    probe = OUT / ".rw_probe"
    try:
        probe.write_text("ok", encoding="utf-8"); probe.unlink()
    except Exception as exc:
        raise SystemExit(f"HALT (I2): {OUT} present but not writable: {exc}")
    log(f"    residency OK -> {OUT}")
    assert CEIL_MS == 1719792000000, "evidence wall moved"
    log(f"    I1 wall: {CEIL_MS} ({iso(CEIL_MS)}) imported from census_build")
    # "drive" is retained as a key so downstream manifest readers do not have to
    # branch on its absence; under v2 there is no volume to wait on, and saying
    # so explicitly is better than dropping the field and leaving a reader to
    # guess whether the gate ran.
    return {"identity": [{"check": n, "pass": bool(o)} for n, o, _ in checks],
            "drive": {"state": "LOCAL", "elapsed_s": 0.0},
            "residency_root": str(OUT),
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
               n_boot: int = 4000, seed: int = SEED, stat: str = "median") -> dict:
    """R-2: asset-cluster bootstrap CI. The unit of replication is the ASSET.

    With mask -> CI on the median difference between the two groups.
    Without   -> CI on the median of `values` itself.

    A row bootstrap treats overlapping forward windows as independent
    observations; they are not, and a five-asset panel claim asserts
    replication across assets, not across rows.
    """
    # stat="median" for returns; stat="mean" for a PROPORTION. A median
    # difference on a 0/1 indicator is identically 0 (the median of a binary
    # vector is 0 or 1), so a proportion delta scored on medians produces a
    # degenerate CI of [0,0] and reads as "straddles zero" no matter what the
    # data says. P-iii-b is a proportion delta and must use the mean.
    agg = np.mean if stat == "mean" else np.median
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
                stats.append(agg(v))
        else:
            a = np.concatenate([values[(clusters == c) & mask] for c in pick])
            b = np.concatenate([values[(clusters == c) & ~mask] for c in pick])
            a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
            if len(a) >= 3 and len(b) >= 3:
                stats.append(agg(a) - agg(b))
    if len(stats) < n_boot // 4:
        return {"point": None, "lo": None, "hi": None, "excludes_zero": False,
                "n_clusters": int(len(uniq)), "reason": "degenerate draws"}
    stats = np.asarray(stats)
    lo, hi = np.percentile(stats, [5, 95])
    if mask is None:
        pt = float(agg(values[np.isfinite(values)]))
    else:
        a = values[mask]; b = values[~mask]
        pt = float(agg(a[np.isfinite(a)]) - agg(b[np.isfinite(b)]))
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
    log("F-PIN -- manifest sections survive a --stage re-run (I12)")

    # This fixture now exercises load_manifest() ITSELF on a real file. The
    # previous version built its own merge inline over a three-key probe dict
    # and asserted against that -- so it tested a hand-written copy of the
    # logic, not the logic. It passed for two sessions while `registrations`
    # was missing from the real merge list, and run-2's CEN-3 invocation
    # destroyed run-1's P-ARM-1 (with its confound disclosure) unnoticed.
    #
    # A fixture that cannot fail when the function under test is broken is
    # decorative. This one populates EVERY section the program writes, calls
    # the real loader, and asserts section-by-section survival.
    probe = OUT / "_fpin_probe_manifest.json"
    seeded = {"generated_utc": "SEEDED"}
    for k in MERGED_SECTIONS:
        seeded[k] = {f"prior_{k}": {"marker": k}}
    for k in CARRIED_SECTIONS:
        seeded[k] = {"marker": k}
    probe.write_text(json.dumps(seeded), encoding="utf-8")
    try:
        merged = load_manifest(probe, scoped=True)
    finally:
        probe.unlink(missing_ok=True)

    rows = []
    for k in MERGED_SECTIONS:
        ok = merged.get(k, {}).get(f"prior_{k}", {}).get("marker") == k
        rows.append((k, ok))
    for k in CARRIED_SECTIONS:
        rows.append((k, merged.get(k, {}).get("marker") == k))
    # and a new write must not evict the prior one
    merged["pins"]["new_this_stage"] = 1
    rows.append(("new pin coexists with prior",
                 merged["pins"].get("prior_pins") is not None))

    for name, ok in rows:
        log(f"    {'PASS' if ok else 'FAIL'}  section survives: {name}")
    bad = [n for n, ok in rows if not ok]
    if bad:
        raise SystemExit(f"HALT (F-PIN): load_manifest drops {bad} across a scoped "
                         f"re-run. Prior evidence would be destroyed silently.")
    return {"pass": True, "sections_checked": [n for n, _ in rows]}


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

            # ---- A1-FAN: two ADDITIVE state columns, computed per bar once and
            # attached to every event snapshot on this (asset, tf).
            #
            # FAN  = the six-EMA stack is fully monotone, either side. A fanned
            #        stack is the visual the operator reads as "trending"; making
            #        it a column lets the census find out whether that is true.
            # KNOT = the five long EMAs are inside the pinned c (0.5*ATR) of one
            #        another -- the stack collapsed to a point. The complement of
            #        a fan, and the shape a range coils into.
            #
            # NOTHING IS SCORED ON EITHER THIS RUN (A1-FAN: "columns only").
            # Where any member is NaN (cold per I4) the flag is False, not True:
            # an unknown ordering is not an ordering.
            fan_cols = [df[f"e{L}"].to_numpy(float) for L in FAN_EMAS]
            fan_stack = np.vstack(fan_cols)
            fan_warm = np.isfinite(fan_stack).all(axis=0)
            d_fan = np.diff(fan_stack, axis=0)
            fan_up = (d_fan < 0).all(axis=0)      # e9 > e89 > ... > e500
            fan_dn = (d_fan > 0).all(axis=0)      # e9 < e89 < ... < e500
            FAN = fan_warm & (fan_up | fan_dn)
            fan_side = np.where(~FAN, "none", np.where(fan_up, "up", "down"))

            knot_stack = np.vstack([df[f"e{L}"].to_numpy(float) for L in KNOT_EMAS])
            knot_warm = np.isfinite(knot_stack).all(axis=0)
            knot_spread = knot_stack.max(axis=0) - knot_stack.min(axis=0)
            with np.errstate(invalid="ignore"):
                KNOT = knot_warm & np.isfinite(av) & (av > 0) & (knot_spread < RIBBON_C * av)
            knot_spread_atr = np.where(np.isfinite(av) & (av > 0),
                                       knot_spread / av, np.nan)

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
                            # --- A1-FAN additive columns (observation only, unscored)
                            "FAN": bool(FAN[i]),
                            "fan_side": str(fan_side[i]),
                            "KNOT": bool(KNOT[i]),
                            "knot_spread_atr": (float(knot_spread_atr[i])
                                                if np.isfinite(knot_spread_atr[i]) else np.nan),
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
        # DURATION-fixing, honestly. `max(1, round(...))` silently substituted
        # ONE BAR whenever the requested duration was shorter than a bar --
        # H20 (1h40m) on 4h became 4h, a 2.4x overshoot, and 12h on the 12h
        # frame, 7.2x. The label then meant a different duration per timeframe,
        # which is the exact paste-1 defect R-1 was written to remove.
        #
        # An infeasible horizon is now NaN + a flag, not a substituted one.
        raw = hms / TF_MS[tf]
        bars = int(round(raw))
        if bars < 1:
            out[hname] = {"terminal": np.full(len(idx), np.nan),
                          "mfe": np.full(len(idx), np.nan),
                          "mae": np.full(len(idx), np.nan),
                          "bars": 0, "realized_ms": 0, "requested_ms": hms,
                          "infeasible": True,
                          "reason": f"{hname} ({hms/3.6e6:.2f}h) is shorter than one "
                                    f"{tf} bar; no substitution made"}
            continue
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
        out[hname] = {"terminal": term, "mfe": mfe, "mae": mae, "bars": bars,
                      "realized_ms": bars * TF_MS[tf], "requested_ms": hms,
                      "infeasible": False,
                      "duration_ratio": round(bars * TF_MS[tf] / hms, 4)}
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
                    # EXPLICIT PREDICATES, not an ordering label. `trigger_class`
                    # records which class fired FIRST; it is NOT "the window
                    # contains a 12_25". 146 of the 440 windows labelled
                    # 25_89-first also contain an in-window 12_25, so scoring a
                    # window-property registration on the first-mover label
                    # contaminated the control arm by 33%. P-REL-1b uses these.
                    "has_12_25": bool(len(in12)),
                    "has_25_89": bool(len(in25)),
                    "n_triggers": int(len(in12) + len(in25)),
                    "trigger_class_first": ("12_25" if len(in12) and (not len(in25) or in12[0] <= in25[0])
                                            else "25_89" if len(in25) else None),
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

    # ---- horizon realisation, printed BEFORE any outcome table.
    # A horizon label that means a different duration per timeframe is not a
    # horizon. Anything infeasible is reported as such, never substituted.
    horizon_realized = {}
    log("    HORIZON REALISATION on the 4h anchor frame (duration-fixed check):")
    for hname, hms in HORIZONS_MS.items():
        raw = hms / TF_MS["4h"]
        bars = int(round(raw))
        rec = {"requested_ms": hms, "requested_h": round(hms / 3.6e6, 3),
               "bars_4h": bars, "realized_h": round(bars * TF_MS["4h"] / 3.6e6, 3),
               "infeasible": bars < 1,
               "duration_ratio": round(bars * TF_MS["4h"] / hms, 4) if bars >= 1 else None}
        horizon_realized[hname] = rec
        flag = "  INFEASIBLE on 4h -- emitted as NaN, NOT substituted" if bars < 1 else ""
        log(f"      {hname:5} requested {rec['requested_h']:.2f}h -> {bars} bar(s) = "
            f"{rec['realized_h']:.2f}h (ratio {rec['duration_ratio']}){flag}")

    # ---- toll line, per asset, in ATR units (I8 'toll beside every excursion')
    # Indices of this asset's armings on its own 4h frame, so the toll is
    # measured where the returns are measured (see m8 note below).
    led_arm_idx = {s: g["arming_idx"].to_numpy(int)
                   for s, g in led.groupby("asset", sort=True)}
    toll = {}
    for sym in assets:
        d4 = MC2.frame(sym, "4h", era)
        px = d4["close"].to_numpy(float); av = d4["atr"].to_numpy(float)
        ok = np.isfinite(px) & np.isfinite(av) & (av > 0)
        # m8: measure the toll on the population the returns are normalised on
        # -- the ARMINGS -- not over every evidence bar. Armings occur at
        # compressed ATR, so the global figure understates the toll 2-14%.
        at = led_arm_idx.get(sym)
        sel = at if (at is not None and len(at)) else np.arange(len(px))
        sel = sel[(sel >= 0) & (sel < len(px))]
        oks = ok[sel]
        toll[sym] = float(np.median((TOLL_BPS_ROUND_TRIP / 10000.0)
                                    * px[sel][oks] / av[sel][oks]))
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
    ev_all = pd.read_parquet(OUT / "cen1" / "cen1_events.parquet",
                             columns=["asset", "tf", "event_class", "dir", "ts"])
    ev_all = ev_all[ev_all.event_class.isin(LATTICE_A)].copy()
    # R-F11 (Amendment A1): annex assets sit OUTSIDE every printed panel count.
    # Run 2 pooled JTO (3,812) + TAO (1,348) into the headline 151,718 cascade
    # stream. Cascades are per (asset, class) so no panel arming's depth moved,
    # but the printed total was a pooled number wearing a panel label -- which
    # is exactly what F-11 forbids. Annex is counted separately and never added.
    n_annex = int(ev_all.asset.isin(ANNEX).sum())
    ev = ev_all[ev_all.asset.isin(assets)].copy()
    ev["bar_close_ms"] = ev["ts"] + ev["tf"].map(TF_MS)
    log(f"      lattice-A stream (PANEL ONLY): {len(ev):,} events, "
        f"{ev.tf.nunique()} timeframes, {ev.event_class.nunique()} classes")
    log(f"      annex excluded from every printed count (R-F11): {n_annex:,} events "
        f"across {sorted(set(ev_all.asset) & set(ANNEX))}")
    for rule in ("window_chained", "direction_consistent"):
        ch = assign_chains_seq8(ev, rule)
        # Armings are 4h 9_89 events. The key MUST include the timeframe:
        # (asset, ts) alone is not unique because a 4h and a 12h bar can share
        # an open_time (00:00), which silently turns the lookup into a Series.
        k = ch[(ch.event_class == "9_89") & (ch.tf == "4h")]

        # NAMED TIE RULE (I5 discipline; required before CEN-4 reads the lens).
        #
        # seq8_views.build_cascades is NOT non-overlapping in its forward scan:
        # `used` only prevents an event STARTING a second cascade, never
        # JOINING one. Under window_chained an arming can therefore belong to
        # several cascades at different depths (measured: 817/860 armings hold
        # >1 membership, 391 with a depth SPREAD). A `dict(zip(...))` over that
        # non-unique key silently keeps the LAST write -- an arbitrary rule
        # nobody chose, and every depth number moves under an equally
        # defensible one (mean depth 3.21 under last/min vs 4.18 under
        # first/max).
        #
        # So: emit min, max and the membership count, and PIN the rule by name.
        # direction_consistent is a clean partition here (1 membership per
        # event), so the rule is a no-op for it -- which is itself worth
        # recording rather than assuming.
        agg = k.groupby(["asset", "ts"], sort=False).agg(
            depth_min=("depth", "min"), depth_max=("depth", "max"),
            n_memberships=("depth", "size"), chain_len_max=("chain_len", "max"))
        pairs = list(zip(led.asset, led.arming_ts))
        for col, src in [(f"depth_{rule}", DEPTH_TIE_RULE),
                         (f"depth_min_{rule}", "depth_min"),
                         (f"depth_max_{rule}", "depth_max"),
                         (f"n_memberships_{rule}", "n_memberships")]:
            m = agg[src].to_dict()
            led[col] = [int(m.get(p, 0)) for p in pairs]
        multi = int((led[f"n_memberships_{rule}"] > 1).sum())
        spread = int((led[f"depth_max_{rule}"] > led[f"depth_min_{rule}"]).sum())
        log(f"      {rule:22} tie-rule='{DEPTH_TIE_RULE}' (pinned) | armings with "
            f">1 membership: {multi}/{len(led)}, with a depth spread: {spread}")
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
            # m1: a pooled group spans several assets, and toll_atr is a
            # per-asset constant -- a median of it is just one asset's number
            # wearing a pooled label. The BINDING toll is the largest in the group.
            r["toll_atr_binding"] = round(float(g["toll_atr"].max()), 4)
            r["toll_atr_assets"] = int(g["asset"].nunique())
            rows.append(r)
        return pd.DataFrame(rows)

    by_asset = panel(led, ["asset", "dir"])
    by_half = panel(led, ["time_half"])
    by_depth_wc = panel(led.assign(depth_bucket=np.minimum(led.depth_window_chained, 4)),
                        ["depth_bucket"])
    by_depth_dc = panel(led.assign(depth_bucket=np.minimum(led.depth_direction_consistent, 4)),
                        ["depth_bucket"])

    # ---- I11 ON REAL DATA. Naming "the worst cell on the board" or "the only
    # asset below 1.0" out of a 10-cell panel IS a max-statistic selection, and
    # until now the guard only ever ran on F-GUARD's synthetic sweeps -- a
    # committed-but-uncalled guard is the prose gate I11 exists to abolish.
    panel_cands = []
    for (a, d), g in led.groupby(["asset", "dir"], sort=True):
        rest = led[~((led.asset == a) & (led.dir == d))]
        vals = np.concatenate([g["term_H100"].to_numpy(float),
                               rest["term_H100"].to_numpy(float)])
        msk = np.concatenate([np.ones(len(g), bool), np.zeros(len(rest), bool)])
        panel_cands.append((f"{a}|{d}", vals, msk))
    panel_guard = selection_guard(panel_cands)
    log(f"    I11 guard on the asset x direction panel (m={panel_guard.get('m')}): "
        f"winner={panel_guard.get('winner')} "
        f"p_sel={panel_guard.get('p_selection_corrected')} "
        f"vs BH bar {panel_guard.get('bh_bar_q_over_m')} -> "
        f"{'ADMISSIBLE' if panel_guard.get('admissible') else 'NOT ADMISSIBLE'}")
    if not panel_guard.get("admissible"):
        log("      => extreme-cell statements about this panel are UNGATED "
            "OBSERVATIONS, not findings. Labelled as such in the build document.")

    log("    OUTCOME PANEL by asset x direction (terminal H100, ATR; toll beside):")
    for r in by_asset.itertuples(index=False):
        log(f"      {r.asset:9} {r.dir:5} n={r.n:4d} term={r.median_term_H100:+.4f} "
            f"mfe={r.median_mfe_H100:.3f} mae={r.median_mae_H100:.3f} "
            f"Q={r.quality_H100} toll={r.toll_atr_binding:.3f}")
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
        n_a_only = int((~led.has_trigger).sum())
        a_only = led[~led.has_trigger]

        # ---- WHY THIS REGISTRATION CANNOT BE SCORED AS WRITTEN.
        #
        # "A-only windows" means armed-but-never-triggered: n=253 here. Two
        # facts kill the comparison:
        #   1. A-only windows have NO TRIGGER, so no trigger anchor exists.
        #      The only shared anchor is the arming, which changes the ruler
        #      mid-comparison.
        #   2. A-only is 252/253 ABORTED, median window width 4 bars against
        #      46 for the triggered arms. That is the MECHANICAL SEPARATION
        #      this very stage prints a caveat about: an abort is a regime flip
        #      inside the horizon, so its terminal return is negative by
        #      construction. Scoring against it measures survival, not the relay.
        #
        # An earlier version silently substituted "25_89-triggered" for
        # "A-only" and reported SUPPORTED. That is a different hypothesis than
        # the one registered, which is precisely what F-8 exists to prevent.
        log("      !! UNSCOREABLE AS WRITTEN -- registration WITHDRAWN")
        log(f"         'A-only' = armed-but-never-triggered, n={n_a_only}; of those "
            f"{int((a_only.fate == 'ABORTED').sum())} are ABORTED, "
            f"median width {a_only.window_width_bars.median():.0f} bars vs "
            f"{led[led.has_trigger].window_width_bars.median():.0f}")
        log("         (a) A-only windows have no trigger, so no trigger anchor exists;")
        log("         (b) the A-only arm IS the aborted arm -- the mechanical")
        log("             separation this stage's own fate table warns about.")

        variants = []
        m_first = (j["trigger_class"] == "12_25").to_numpy(bool)
        vals_first = j["trig_term_H100"].to_numpy(float)
        clus = j["asset"].to_numpy()
        variants.append(("V1 12_25-FIRST vs 25_89-FIRST (trigger anchor) "
                         "-- what an earlier draft reported",
                         cluster_ci(vals_first, clus, m_first),
                         int(m_first.sum()), int((~m_first).sum())))
        # literal-predicate arm: ANY in-window 12_25, vs 25_89-only
        vv = np.concatenate([j.loc[m_first, "trig_term_H100"].to_numpy(float),
                             a_only["term_H100"].to_numpy(float)])
        cc = np.concatenate([j.loc[m_first, "asset"].to_numpy(),
                             a_only["asset"].to_numpy()])
        mm = np.concatenate([np.ones(int(m_first.sum()), bool),
                             np.zeros(len(a_only), bool)])
        variants.append(("V2 12_25 vs A-ONLY (mixed anchor) -- THE REGISTERED "
                         "COMPARISON, confounded",
                         cluster_ci(vv, cc, mm), int(mm.sum()), int((~mm).sum())))
        for label, ci_v, na, nb in variants:
            log(f"         {label}")
            log(f"            n={na} vs {nb}  point={ci_v['point']} "
                f"CI[{ci_v['lo']},{ci_v['hi']}] "
                f"{'EXCL-0' if ci_v['excludes_zero'] else 'straddles 0'}")

        # ---- I8/R-2 mandated splits, printed BESIDE any headline
        splits = {}
        for h in ("H100", "H500"):
            col = f"trig_term_{h}"
            if col in j and j[col].notna().any():
                splits[f"horizon_{h}"] = cluster_ci(j[col].to_numpy(float), clus, m_first)
        for d in ("up", "down"):
            sel = (j["dir"] == d).to_numpy(bool)
            if sel.sum() > 20:
                splits[f"dir_{d}"] = cluster_ci(vals_first[sel], clus[sel], m_first[sel])
        per_asset = {}
        for a in np.unique(clus):
            s = clus == a
            aa = vals_first[s & m_first]; bb = vals_first[s & ~m_first]
            aa = aa[np.isfinite(aa)]; bb = bb[np.isfinite(bb)]
            if len(aa) >= 5 and len(bb) >= 5:
                per_asset[a] = round(float(np.median(aa) - np.median(bb)), 4)
        loao = {}
        for a in np.unique(clus):
            s = clus != a
            loao[f"drop_{a}"] = cluster_ci(vals_first[s], clus[s], m_first[s])
        log(f"         per-asset deltas (descriptive, R-2): {per_asset}")
        log(f"         sign-reversed assets: "
            f"{[k for k, v in per_asset.items() if v < 0] or 'none'}")
        n_loao_excl = sum(1 for v in loao.values() if v["excludes_zero"])
        log(f"         leave-one-asset-out: {n_loao_excl}/{len(loao)} refits still "
            f"exclude zero")
        for hk in ("horizon_H500",):
            if hk in splits:
                log(f"         {hk}: point={splits[hk]['point']} "
                    f"CI[{splits[hk]['lo']},{splits[hk]['hi']}] "
                    f"{'EXCL-0' if splits[hk]['excludes_zero'] else 'straddles 0'}")

        rel = {
            "registration": ("windows with an in-window 12_25 trigger -> higher "
                             "trigger-anchored terminal return than A-only windows"),
            "prior": 0.60, "lens": "24h|window_chained",
            "verdict": "WITHDRAWN -- UNSCOREABLE AS WRITTEN",
            "withdrawal_reason": (
                "'A-only' means armed-but-never-triggered (n=%d). Those windows have "
                "no trigger, so the registered trigger-anchored comparison has no "
                "anchor; and the A-only cohort is %d/%d ABORTED with median width "
                "%.0f bars vs %.0f, so the split is the mechanical separation this "
                "stage explicitly caveats. An earlier draft substituted "
                "'25_89-triggered' for 'A-only' and reported SUPPORTED -- a "
                "different hypothesis than the one registered."
                % (n_a_only, int((a_only.fate == 'ABORTED').sum()), n_a_only,
                   a_only.window_width_bars.median(),
                   led[led.has_trigger].window_width_bars.median())),
            "n_a_only": n_a_only,
            "variants": [{"label": l, "n_treat": na, "n_control": nb, "ci": c}
                         for l, c, na, nb in variants],
            "mandated_splits": splits,
            "per_asset_delta": per_asset,
            "leave_one_asset_out": loao,
            "loao_excluding_zero": f"{n_loao_excl}/{len(loao)}",
            "criterion": "R-2 asset-cluster 90% CI excluding zero",
            "successor": ("re-register by name as P-REL-1b with the arms defined by "
                          "an explicit event-stream predicate and the anchor stated"),
        }
        log("      VERDICT: WITHDRAWN -- UNSCOREABLE AS WRITTEN "
            "(successor P-REL-1b to be registered by name)")

    # =====================================================================
    # P-REL-1b [50%, POST-HOC-INFORMED -- LABEL PERMANENT] (Amendment A1)
    # Text before result (F-8). Scored from cached CEN-3 substrate.
    # =====================================================================
    log("    P-REL-1b [50%, post-hoc-informed -- LABEL PERMANENT] (Amendment A1):")
    log("      'among windows with >=1 in-window trigger: TREAT has_in_window_12_25=true")
    log("       vs CONTROL triggered without any in-window 12_25; anchor = FIRST")
    log("       in-window trigger of ANY class, identical rule both arms.'")
    log("      Best attainable grade this run = SUPPORTED-PROVISIONAL (the prior is")
    log("      informed by run-2's post-hoc look; only next-cycle replication can lift it).")
    rel1b = None
    if not trig.empty and "has_12_25" in led.columns:
        jb = trig.merge(led[["asset", "arming_ts", "has_12_25", "dir", "time_half"]]
                        .drop_duplicates(subset=["asset", "arming_ts"]),
                        on=["asset", "arming_ts"], how="left", suffixes=("", "_l"))
        assert len(jb) == len(trig), "P-REL-1b merge multiplied rows"
        treat = jb["has_12_25"].fillna(False).to_numpy(bool)
        clus = jb["asset"].to_numpy()
        prim = jb["trig_term_H100"].to_numpy(float)
        log(f"      arms: TREAT n={int(treat.sum())} vs CONTROL n={int((~treat).sum())} "
            f"(anchor = first in-window trigger of ANY class, both arms)")

        ci_primary = cluster_ci(prim, clus, treat)
        splits, per_asset, loao = {}, {}, {}
        for h in ("H20", "H100", "H500"):
            col = f"trig_term_{h}"
            if col in jb and jb[col].notna().any():
                splits[f"horizon_{h}"] = cluster_ci(jb[col].to_numpy(float), clus, treat)
            else:
                splits[f"horizon_{h}"] = {"point": None, "excludes_zero": False,
                                          "reason": "infeasible on 4h -- NaN, not substituted"}
        for d in ("up", "down"):
            s = (jb["dir_l"] if "dir_l" in jb else jb["dir"]).to_numpy() == d
            if s.sum() > 20:
                splits[f"dir_{d}"] = cluster_ci(prim[s], clus[s], treat[s])
        for hh in ("early", "late"):
            s = jb["time_half"].to_numpy() == hh
            if s.sum() > 20:
                splits[f"half_{hh}"] = cluster_ci(prim[s], clus[s], treat[s])
        for a in np.unique(clus):
            s = clus == a
            aa = prim[s & treat]; bb = prim[s & ~treat]
            aa = aa[np.isfinite(aa)]; bb = bb[np.isfinite(bb)]
            if len(aa) >= 5 and len(bb) >= 5:
                per_asset[a] = round(float(np.median(aa) - np.median(bb)), 4)
            loao[f"drop_{a}"] = cluster_ci(prim[~s], clus[~s], treat[~s])
        n_loao = sum(1 for v in loao.values() if v.get("excludes_zero"))

        log(f"      H100 PRIMARY: point={ci_primary['point']} "
            f"CI[{ci_primary['lo']},{ci_primary['hi']}] "
            f"{'EXCL-0' if ci_primary['excludes_zero'] else 'straddles 0'}")
        for k in ("horizon_H20", "horizon_H500", "dir_up", "dir_down",
                  "half_early", "half_late"):
            v = splits.get(k)
            if not v:
                continue
            if v.get("point") is None:
                log(f"      {k:14} n/a -- {v.get('reason','')}")
            else:
                log(f"      {k:14} point={v['point']} CI[{v['lo']},{v['hi']}] "
                    f"{'EXCL-0' if v['excludes_zero'] else 'straddles 0'}")
        log(f"      per-asset deltas: {per_asset}")
        log(f"      sign-reversed: {[k for k, v in per_asset.items() if v < 0] or 'none'}")
        log(f"      LOAO: {n_loao}/{len(loao)} refits still exclude zero")

        passes = bool(ci_primary["excludes_zero"] and (ci_primary["point"] or 0) > 0)
        verdict = "SUPPORTED-PROVISIONAL" if passes else "NOT SUPPORTED"
        log(f"      VERDICT: {verdict}  [label post-hoc-informed, PERMANENT]")
        rel1b = {
            "registration": ("among windows with >=1 in-window trigger: TREAT "
                             "has_in_window_12_25=true vs CONTROL triggered without any "
                             "in-window 12_25; anchor = FIRST in-window trigger of ANY "
                             "class, identical rule both arms"),
            "prior": 0.50,
            "label": "POST-HOC-INFORMED -- PERMANENT; ceiling this run is "
                     "SUPPORTED-PROVISIONAL pending next-cycle replication",
            "n_treat": int(treat.sum()), "n_control": int((~treat).sum()),
            "anchor": "first in-window trigger of any class (identical both arms)",
            "primary": {"horizon": "H100", "ci": ci_primary},
            "mandated_splits": splits, "per_asset_delta": per_asset,
            "leave_one_asset_out": loao, "loao_excluding_zero": f"{n_loao}/{len(loao)}",
            "criterion": "R-2 asset-cluster 90% CI excluding zero",
            "verdict": verdict,
            "supersedes": "P-REL-1 (WITHDRAWN -- unscoreable as written)",
        }

    return {"ledger": led, "trigger_outcomes": trig, "by_asset": by_asset,
            "p_rel_1b": rel1b,
            "by_half": by_half, "by_depth_window_chained": by_depth_wc,
            "by_depth_direction_consistent": by_depth_dc, "by_fate": by_fate,
            "toll_atr": toll, "fate_caveat": CAVEAT, "p_rel_1": rel,
            "horizon_realized": horizon_realized}


# ===========================================================================
# CEN-6 -- RANGE & VERDICT
# ===========================================================================
ACCEPT_H = 2                       # [VETO, operator-named 2026-08-12] Amendment A2
CLOSE_SET = ["1h", "4h", "12h"]    # pinned acceptance close-set (CD-4a)
# Trap window, BOTH ways -- because they answer different questions and a bar
# count alone is not comparable across a close-set.
#   *_bars : 10 MEMBER bars. Member-relative, but that is 10h on 1h and 5 DAYS
#            on 12h, so a trap rate rising across the close-set on this measure
#            is largely the window growing, not the tape changing. A first draft
#            of this stage reported only this and read 0.527 -> 0.607 -> 0.883 as
#            structure. It is the same duration-vs-bars defect the run-2 review
#            caught in the CEN-3 horizons.
#   *_dur  : a fixed 48h for every member. Comparable across the close-set.
TRAP_LOOKBACK_BARS = 10
TRAP_WINDOW_MS = 48 * 3_600_000


def stage_cen6(assets: list[str], era: str = "evidence") -> dict:
    """Acceptance head-to-head on {1H,4H,12H}, deviation-reclaim branch,
    trap-rate per member, hysteresis, and the verdict-open state CEN-4 needs.

    THE RULE, in full (Amendment A2 supplies h; the v0.2->v0.3 compression had
    deleted it):
      An excursion beyond a range boundary is ACCEPTED on a close-set member
      when that member's close is beyond the boundary and HOLDS beyond for
      h = 2 consecutive member bars. It is DEVIATION-RECLAIMED when price
      closes back inside first. Two branches of ONE episode, three clocks.

    BOUNDARY OBJECT: the prior completed WEEK's high/low, via
    analytics.structure.prior_period_extremes -- "causal by construction: a bar
    only ever sees periods that closed before its own period began". Chosen
    over engine/s2.py's D1/D3 detectors deliberately: LEDGER.md:311 records
    P-PD1/P-PD2/P-PD4 FALSIFIED ("the pattern detectors as gridded do not
    graduate"), so those are admissible as a LOCATION object but reusing them
    as a promoted signal would re-run a falsified test. A prior-week envelope
    is a location, carries its own causality class, and asserts nothing.

    NOT A SWEEP. h is named, the close-set is pinned, the boundary is one
    object. Nothing is selected, so no I11 promotion occurs here -- the three
    members are a head-to-head that is PRINTED, not a grid a winner is drawn
    from. If a later run promotes one member, that promotion is a selection
    over m=3 and must clear the guard.
    """
    log(f"CEN-6 -- range & verdict [{era}]  h={ACCEPT_H} [VETO, A2]  "
        f"close-set {CLOSE_SET}")
    sys.path.insert(0, str(ROOT))
    from analytics.structure import prior_period_extremes

    ep_rows, state_rows = [], []
    for sym in assets:
        for tf in CLOSE_SET:
            df = MC2.frame(sym, tf, era)
            if len(df) < 200:
                continue
            o = df["open_time"].to_numpy(np.int64)
            c = df["close"].to_numpy(float)
            hi = df["high"].to_numpy(float)
            lo = df["low"].to_numpy(float)
            av = df["atr"].to_numpy(float)
            ph, pl = prior_period_extremes(o, hi, lo, period="W")
            n = len(c)

            # per-bar verdict state, carried forward (the hysteresis substrate
            # and CEN-4's `verdict-open` input)
            state = np.array(["NONE"] * n, dtype=object)
            cur = "NONE"
            i = 0
            # AN EPISODE IS A TRANSITION, NOT A STATE.
            #
            # A first draft opened an episode at every bar whose close sat
            # beyond the boundary and then advanced by h, so a sustained
            # 100-bar breakout manufactured 50 "episodes" of the SAME
            # excursion -- 28,816 of them on 1h. That inflates every count,
            # and it manufactured a monotone trap-rate climb (0.245 -> 0.566
            # -> 0.931 across the close-set) that was a re-counting artifact
            # rather than structure. An excursion beyond a boundary is ONE
            # event; it begins when price closes beyond having been inside.
            outside = False
            while i < n:
                up_b = np.isfinite(ph[i]) and c[i] > ph[i]
                dn_b = np.isfinite(pl[i]) and c[i] < pl[i]
                if not (up_b or dn_b):
                    outside = False          # back inside: re-arm the trigger
                    state[i] = cur
                    i += 1
                    continue
                if outside:                  # already beyond -- not a new episode
                    state[i] = cur
                    i += 1
                    continue
                outside = True
                side = "up" if up_b else "down"
                bound = ph[i] if up_b else pl[i]
                # hold test: h consecutive member closes beyond, from i
                end = min(i + ACCEPT_H, n)
                held = all((c[j] > ph[j]) if side == "up" else (c[j] < pl[j])
                           for j in range(i, end)
                           if np.isfinite(ph[j]) and np.isfinite(pl[j]))
                complete = (end - i) == ACCEPT_H
                verdict = ("ACCEPTED" if (held and complete)
                           else "DEVIATION-RECLAIM" if complete else "TRUNCATED")
                # trap: accepted, then closes back inside within the lookback
                trap, trap_lag, trap_dur = False, np.nan, False
                if verdict == "ACCEPTED":
                    dur_end = o[end - 1] + TRAP_WINDOW_MS if end >= 1 else o[i]
                    for j in range(end, n):
                        if not (np.isfinite(ph[j]) and np.isfinite(pl[j])):
                            continue
                        within_bars = (j - end) < TRAP_LOOKBACK_BARS
                        within_dur = o[j] <= dur_end
                        if not (within_bars or within_dur):
                            break
                        inside = (c[j] <= ph[j]) if side == "up" else (c[j] >= pl[j])
                        if inside:
                            if within_bars and not trap:
                                trap, trap_lag = True, float(j - end)
                            if within_dur:
                                trap_dur = True
                            if trap and trap_dur:
                                break
                ep_rows.append({
                    "asset": sym, "member": tf, "side": side,
                    "ts": int(o[i]), "ts_iso": iso(int(o[i])),
                    "boundary": float(bound),
                    "depth_atr": (float(abs(c[i] - bound) / av[i])
                                  if np.isfinite(av[i]) and av[i] > 0 else np.nan),
                    "verdict": verdict, "trap": bool(trap), "trap_lag_bars": trap_lag,
                    "trap_48h": bool(trap_dur),
                })
                cur = ("RESPECTED" if verdict == "DEVIATION-RECLAIM"
                       else "BROKEN" if verdict == "ACCEPTED" else cur)
                for j in range(i, end):
                    state[j] = cur
                i = end
            for j in range(n):
                state_rows.append({"asset": sym, "member": tf,
                                   "ts": int(o[j]), "verdict_state": state[j]})
            log(f"    {sym:9} {tf:4} episodes so far {len(ep_rows):,}")

    ep = pd.DataFrame(ep_rows)
    st = pd.DataFrame(state_rows)
    if ep.empty:
        return {"episodes": ep, "states": st}

    # ---- head-to-head, per close-set member (PRINTED, not selected)
    log("    ACCEPTANCE HEAD-TO-HEAD (h=2), per close-set member:")
    rows = []
    for tf in CLOSE_SET:
        g = ep[ep.member == tf]
        if g.empty:
            continue
        acc = g[g.verdict == "ACCEPTED"]
        dev = g[g.verdict == "DEVIATION-RECLAIM"]
        n_trap = int(acc.trap.sum())
        rows.append({
            "member": tf, "episodes": int(len(g)),
            "accepted": int(len(acc)), "deviation_reclaim": int(len(dev)),
            "truncated": int((g.verdict == "TRUNCATED").sum()),
            "accept_rate": round(len(acc) / len(g), 6),
            "traps_10bars": n_trap,
            "trap_rate_10bars": round(n_trap / len(acc), 6) if len(acc) else None,
            "traps_48h": int(acc.trap_48h.sum()),
            "trap_rate_48h": (round(float(acc.trap_48h.sum()) / len(acc), 6)
                              if len(acc) else None),
            "trap_window_bars_hours": round(TRAP_LOOKBACK_BARS * TF_MS[tf] / 3.6e6, 1),
            "median_depth_atr": round(float(g.depth_atr.median()), 6),
            "median_trap_lag": (round(float(acc.loc[acc.trap, "trap_lag_bars"].median()), 2)
                                if n_trap else None),
        })
        r = rows[-1]
        log(f"      {tf:4} episodes={r['episodes']:5d} accepted={r['accepted']:5d} "
            f"({r['accept_rate']:.3f}) reclaim={r['deviation_reclaim']:5d} "
            f"depth={r['median_depth_atr']:.2f}ATR")
        log(f"           trap  10-bar window (= {r['trap_window_bars_hours']:.0f}h here): "
            f"{r['traps_10bars']:4d}  rate={r['trap_rate_10bars']}")
        log(f"           trap  48h  window (comparable across members): "
            f"{r['traps_48h']:4d}  rate={r['trap_rate_48h']}")
    h2h = pd.DataFrame(rows)

    # ---- hysteresis prior: does a verdict persist into the next episode?
    log("    HYSTERESIS PRIOR (P(next verdict == this verdict), per member):")
    hyst = []
    for tf in CLOSE_SET:
        for sym in assets:
            g = ep[(ep.member == tf) & (ep.asset == sym)].sort_values("ts")
            v = g.verdict.to_numpy()
            v = v[(v == "ACCEPTED") | (v == "DEVIATION-RECLAIM")]
            if len(v) < 10:
                continue
            same = int((v[1:] == v[:-1]).sum())
            hyst.append({"member": tf, "asset": sym, "n_transitions": len(v) - 1,
                         "same": same, "p_persist": round(same / (len(v) - 1), 6)})
    hy = pd.DataFrame(hyst)
    for tf in CLOSE_SET:
        g = hy[hy.member == tf]
        if not g.empty:
            p = float((g["same"].sum()) / g["n_transitions"].sum())
            log(f"      {tf:4} P(persist)={p:.3f} over "
                f"{int(g.n_transitions.sum())} transitions, {len(g)} assets "
                f"(0.5 = memoryless)")

    # ---- verdicts consume CEN-1 refusal events
    log("    VERDICTS x CEN-1 REFUSAL EVENTS (I8 / D-B):")
    ref = pd.read_parquet(OUT / "cen1" / "cen1_refusals.parquet",
                          columns=["asset", "tf", "limb", "ts"])
    ref = ref[ref.asset.isin(assets) & ref.tf.isin(CLOSE_SET)]
    join_rows = []
    for tf in CLOSE_SET:
        span = TF_MS[tf] * TRAP_LOOKBACK_BARS
        for lim in ("i-a", "i-b"):
            rt = ref[(ref.tf == tf) & (ref.limb == lim)]
            for verdict in ("ACCEPTED", "DEVIATION-RECLAIM"):
                g = ep[(ep.member == tf) & (ep.verdict == verdict)]
                if g.empty or rt.empty:
                    continue
                cnt = 0
                for sym, gg in g.groupby("asset", sort=False):
                    rr = np.sort(rt[rt.asset == sym].ts.to_numpy(np.int64))
                    if not len(rr):
                        continue
                    ts = gg.ts.to_numpy(np.int64)
                    lo_i = np.searchsorted(rr, ts - span)
                    hi_i = np.searchsorted(rr, ts)
                    cnt += int((hi_i - lo_i).sum())
                join_rows.append({"member": tf, "limb": lim, "verdict": verdict,
                                  "episodes": int(len(g)),
                                  "refusals_in_prior_window": cnt,
                                  "per_episode": round(cnt / len(g), 4)})
    rj = pd.DataFrame(join_rows)
    for r in rj.itertuples(index=False):
        log(f"      {r.member:4} {r.limb} {r.verdict:18} "
            f"{r.refusals_in_prior_window:6d} refusals / {r.episodes:5d} episodes "
            f"= {r.per_episode:.3f} each")
    log("      (RESPECTED is largely a breakout that failed to be born -- the "
        "substrate now records what almost fired beside what fired.)")

    return {"episodes": ep, "states": st, "head_to_head": h2h,
            "hysteresis": hy, "refusal_join": rj,
            "h": ACCEPT_H, "close_set": CLOSE_SET,
            "boundary_object": "prior completed week H/L "
                               "(analytics.structure.prior_period_extremes, period='W')",
            "not_a_sweep": ("h is named [VETO A2], the close-set is pinned, the "
                            "boundary is one object; the three members are PRINTED "
                            "head-to-head, not a grid a winner is drawn from")}


# ===========================================================================
# CEN-4 -- CHOP-STATE  (Amendment A3: A3-CHURN, A3-DECILE)
# ===========================================================================
CHURN_WINDOW_MS = 24 * 3_600_000          # A3-CHURN: trailing 24 FIXED HOURS
CHURN_MIN_HISTORY_MS = 90 * 86_400_000    # A3-CHURN: NaN until >=90 days
CHURN_PCTL = 0.80                         # A3-CHURN: fires at >= P80, pre-named
CHOP_THRESHOLD = 3                        # P-CHOP-1's registered composite cut


def load_births() -> pd.DataFrame:
    """The 7,117 WF1 births. Read-only; the estate file is never touched."""
    rows = []
    for p in sorted((ROOT / "_reviewer_box" / "wf1").glob("*USDT_*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        for r in d["rows"]:
            rows.append({"cell": r["cell"], "tranche_id": r["tranche_id"],
                         "asset": r["symbol"], "mandate": r["mandate"],
                         "dir": r["dir"], "ts_open": r["ts_open"],
                         "ts_ms": int(r["ts_open_epoch"]) * 1000,
                         "resolved": bool(r.get("resolved")),
                         "size_r": r.get("size_r"),
                         "realized_r": r.get("realized_r")})
    return pd.DataFrame(rows)


def trg(win: pd.DataFrame, keep_mask: np.ndarray, col: str) -> float:
    """Tail-Retention Gauge: the share of the UNFILTERED top-decile profit that
    survives the rule. A filter that captures losers by deleting the winners'
    tail has bought nothing, and TRG is what makes that visible."""
    tot = float(win[col].sum())
    if tot == 0:
        return float("nan")
    return float(win.loc[keep_mask, col].sum() / tot)


def stage_cen4(assets: list[str], era: str = "evidence") -> dict:
    """P-iii-b + the five-component chop composite, counts only (I5).

    A3-DECILE governs the cohorts: PER-ASSET deciles on the SIZE-FREE ruler
    realized_r/size_r. The incumbent pooled-raw decile prints beside as
    continuity and is NEVER scored -- because it is substantially a
    position-size selector (the pooled bottom decile is 97.6% size_r=0.5).
    """
    log(f"CEN-4 -- chop-state [{era}]  (A3-CHURN P{int(CHURN_PCTL*100)}, A3-DECILE size-free)")
    b = load_births()
    log(f"    births loaded: {len(b):,} ({int(b.resolved.sum()):,} resolved)")
    b = b[b.resolved & b.realized_r.notna() & b.size_r.notna()].copy()
    b = b[b.ts_ms < CEIL_MS]                      # I1
    b["r_norm"] = b.realized_r / b.size_r
    panel = b[b.asset.isin(assets)].copy()
    annex_n = int((~b.asset.isin(assets)).sum())
    log(f"    I1-bounded resolved: {len(b):,}  | panel {len(panel):,}  "
        f"annex {annex_n} (R-F11: outside every panel count)")

    # ---- A3-DECILE: per-asset deciles on the size-free ruler
    panel["cohort"] = "MID"
    for sym, g in panel.groupby("asset", sort=True):
        k = int(np.floor(0.10 * len(g)))
        if k < 1:
            continue
        s = g.r_norm.sort_values()
        lo_cut, hi_cut = s.iloc[k - 1], s.iloc[-k]
        panel.loc[g.index[g.r_norm <= lo_cut], "cohort"] = "L"
        panel.loc[g.index[g.r_norm >= hi_cut], "cohort"] = "W"
    # incumbent pooled-RAW decile, for continuity only -- never scored
    kp = int(np.floor(0.10 * len(panel)))
    sr = panel.realized_r.sort_values()
    panel["cohort_incumbent"] = np.where(
        panel.realized_r <= sr.iloc[kp - 1], "L",
        np.where(panel.realized_r >= sr.iloc[-kp], "W", "MID"))
    L = panel[panel.cohort == "L"]; W = panel[panel.cohort == "W"]
    log(f"    A3-DECILE (scored)   L={len(L)} W={len(W)}")
    log(f"    incumbent (continuity, NOT scored) "
        f"L={int((panel.cohort_incumbent=='L').sum())} "
        f"W={int((panel.cohort_incumbent=='W').sum())}")
    comp_rows = []
    for name, col in [("A3-DECILE", "cohort"), ("incumbent-raw", "cohort_incumbent")]:
        g = panel[panel[col] == "L"]
        comp_rows.append({"book": name, "cohort": "L", "n": len(g),
                          "size_r_0.5_share": round(float((g.size_r == 0.5).mean()), 4),
                          "top_asset": g.asset.value_counts().idxmax(),
                          "top_asset_share": round(float(g.asset.value_counts(normalize=True).iloc[0]), 4)})
    comp = pd.DataFrame(comp_rows)
    for _, r in comp.iterrows():
        log(f"      composition {r['book']:14} L n={int(r['n']):4d} "
            f"size_r=0.5 {r['size_r_0.5_share']:.1%} "
            f"top asset {r['top_asset']} {r['top_asset_share']:.1%}")

    # ---- the five components, as COUNTS, as-of the birth (I7)
    log("    five components, counts only (I5), as-of the birth (I7):")
    ev = pd.read_parquet(OUT / "cen1" / "cen1_events.parquet",
                         columns=["asset", "tf", "event_class", "dir", "ts"])
    vs = pd.read_parquet(OUT / "cen6" / "cen6_verdict_state.parquet")
    FAST = ["5m", "15m", "30m"]
    for c in ("churn", "no_slow", "ribbon", "verdict_open", "concord"):
        panel[c] = np.nan

    for sym, g in panel.groupby("asset", sort=True):
        idx = g.index
        ts = g.ts_ms.to_numpy(np.int64)

        # (1) A3-CHURN: FAST-tier 9_89 crosses, both dirs, trailing 24 FIXED HOURS,
        #     against the asset's OWN EXPANDING causal distribution, fires at P80.
        f = ev[(ev.asset == sym) & (ev.tf.isin(FAST)) & (ev.event_class == "9_89")]
        fts = np.sort(f.ts.to_numpy(np.int64))
        cnt = (np.searchsorted(fts, ts, "left")
               - np.searchsorted(fts, ts - CHURN_WINDOW_MS, "left"))
        t0 = fts[0] if len(fts) else ts.min()
        order = np.argsort(ts, kind="mergesort")
        fire = np.full(len(ts), np.nan)
        hist = []
        for pos in order:
            if ts[pos] - t0 >= CHURN_MIN_HISTORY_MS and len(hist) >= 30:
                fire[pos] = float(cnt[pos] >= np.quantile(hist, CHURN_PCTL))
            hist.append(cnt[pos])        # expanding, causal: only the past
        panel.loc[idx, "churn"] = fire

        # (2) no-slow-arrival-yet, CURTAIN-CLEAN: no SLOW-tier (4h/12h) lattice-A
        #     event in the trailing window AS OF the birth. MC-1's original stamp
        #     read whole-cascade attributes that had not happened yet at the
        #     birth; that peek is exactly what P-iii-b's recut exists to remove.
        sl = ev[(ev.asset == sym) & (ev.tf.isin(["4h", "12h"]))
                & (ev.event_class.isin(LATTICE_A))]
        sts = np.sort(sl.ts.to_numpy(np.int64))
        n_slow = (np.searchsorted(sts, ts, "left")
                  - np.searchsorted(sts, ts - CHURN_WINDOW_MS, "left"))
        panel.loc[idx, "no_slow"] = (n_slow == 0).astype(float)

        # (3) ribbon compression flag, c = 0.5 x ATR on the 1h 9/89 spread
        d1 = MC2.frame(sym, "1h", era)
        o1 = d1["open_time"].to_numpy(np.int64) + TF_MS["1h"]      # bar CLOSE (I7)
        k = np.searchsorted(o1, ts, "right") - 1
        sp = np.abs(d1["e9"].to_numpy() - d1["e89"].to_numpy())
        av = d1["atr"].to_numpy()
        ok = (k >= 0)
        rib = np.full(len(ts), np.nan)
        kk = np.clip(k, 0, len(sp) - 1)
        good = ok & np.isfinite(sp[kk]) & np.isfinite(av[kk]) & (av[kk] > 0)
        rib[good] = (sp[kk][good] <= RIBBON_C * av[kk][good]).astype(float)
        panel.loc[idx, "ribbon"] = rib

        # (4) verdict-open, from CEN-6 (the dependency A2 discharged)
        v = vs[(vs.asset == sym) & (vs.member == "4h")].sort_values("ts")
        if len(v):
            vt = v.ts.to_numpy(np.int64); vstate = v.verdict_state.to_numpy()
            kv = np.searchsorted(vt, ts, "right") - 1
            vv = np.where(kv >= 0, vstate[np.clip(kv, 0, len(vstate) - 1)], "NONE")
            # READING, flagged: "verdict-open" = the range verdict is still
            # OPEN, i.e. the boundary is holding and no accepted break is in
            # force -> state == RESPECTED (20.2% of 4h bars). A first draft
            # read it as state == NONE ("no verdict has ever occurred"), which
            # fires on 0.75% of bars and on 1 of 6,897 births -- a component
            # that never fires is not a component. RESPECTED is also the state
            # LEDGER.md:315 P-PD3 CONFIRMED points at ("Z2's deficit
            # concentrates in-range"), which is what CEN-4 wants from it.
            panel.loc[idx, "verdict_open"] = (vv == "RESPECTED").astype(float)

        # (5) lens-concordance: do the two chaining rules agree on the open
        #     chain in the trailing 24h? Counted, no threshold (pinned metric).
        a4 = ev[(ev.asset == sym) & (ev.tf == "4h") & (ev.event_class.isin(LATTICE_A))]
        ats = np.sort(a4.ts.to_numpy(np.int64))
        n24 = (np.searchsorted(ats, ts, "left")
               - np.searchsorted(ats, ts - CHURN_WINDOW_MS, "left"))
        panel.loc[idx, "concord"] = (n24 <= 1).astype(float)

    comps = ["churn", "no_slow", "ribbon", "verdict_open", "concord"]
    panel["composite"] = panel[comps].sum(axis=1, skipna=True)
    panel["n_components_known"] = panel[comps].notna().sum(axis=1)
    for c in comps:
        f = panel[c]
        log(f"      {c:13} fires {np.nansum(f):6.0f}/{int(f.notna().sum()):5d} known "
            f"({np.nanmean(f):.1%})  NaN {int(f.isna().sum())}")
    log(f"      composite distribution: "
        f"{panel.composite.value_counts().sort_index().to_dict()}")

    # ---- P-iii-b (text before result, F-8)
    log("    P-iii-b [65%] (entry lens):")
    log("      'curtain-clean grind-at-birth over-represented in loser births")
    log("       (proportion delta, cluster CI), both directions.'")
    grind = (panel["no_slow"] == 1) & (panel["churn"] == 1)
    panel["grind"] = grind.astype(float)
    pL = float(grind[panel.cohort == "L"].mean())
    pW = float(grind[panel.cohort == "W"].mean())
    vals = grind.astype(float).to_numpy()
    sel = panel.cohort.isin(["L", "W"]).to_numpy()
    ci_iiib = cluster_ci(vals[sel], panel.asset.to_numpy()[sel],
                         (panel.cohort.to_numpy()[sel] == "L"), stat="mean")
    # The registration says "both directions". That clause is part of the
    # hypothesis, not decoration, so the verdict must enforce it -- a pooled CI
    # that excludes zero while one direction straddles has not met the text.
    pooled_ok = bool(ci_iiib["excludes_zero"] and (ci_iiib["point"] or 0) > 0)
    v_iiib = "PENDING"
    log(f"      grind prevalence  L={pL:.4f}  W={pW:.4f}  delta={pL-pW:+.4f}")
    log(f"      cluster CI on the proportion delta: [{ci_iiib['lo']},{ci_iiib['hi']}] "
        f"{'EXCL-0' if ci_iiib['excludes_zero'] else 'straddles 0'}")
    per_dir = {}
    for d in ("long", "short"):
        s = (panel.dir == d) & sel
        if s.sum() > 40:
            per_dir[d] = cluster_ci(vals[s.to_numpy()], panel.asset.to_numpy()[s.to_numpy()],
                                    (panel.cohort.to_numpy()[s.to_numpy()] == "L"),
                                    stat="mean")
            log(f"      dir {d:6} delta={per_dir[d]['point']} "
                f"CI[{per_dir[d]['lo']},{per_dir[d]['hi']}] "
                f"{'EXCL-0' if per_dir[d]['excludes_zero'] else 'straddles 0'}")
    dirs_ok = bool(per_dir) and all(
        v["excludes_zero"] and (v["point"] or 0) > 0 for v in per_dir.values())
    v_iiib = ("SUPPORTED" if (pooled_ok and dirs_ok)
              else "NOT SUPPORTED -- pooled effect measured, but the registration's "
                   "'both directions' clause is not met" if pooled_ok
              else "NOT SUPPORTED")
    if pooled_ok and not dirs_ok:
        failing = {d: v for d, v in per_dir.items()
                   if not (v["excludes_zero"] and (v["point"] or 0) > 0)}
        for d, v in failing.items():
            margin = min(abs(v["lo"] or 0), abs(v["hi"] or 0))
            log(f"      !! '{d}' fails the both-directions clause: CI[{v['lo']},{v['hi']}] "
                f"-- it straddles zero by {margin:.4f}")
        log("         The pooled effect IS measured (CI excludes zero). The verdict is "
            "NOT SUPPORTED because the registered text requires both directions, and "
            "that margin is reported rather than rounded either way.")
    log(f"      VERDICT: {v_iiib}")

    # ---- P-CHOP-1 (text before result, F-8)
    log("    P-CHOP-1 [65%] (entry lens):")
    log(f"      'chop-composite >={CHOP_THRESHOLD} captures >=40% of loser-decile")
    log("       births at TRG >=85%.'")
    flag = (panel.composite >= CHOP_THRESHOLD)
    cap = float(flag[panel.cohort == "L"].mean())
    t = trg(W, (~flag[panel.cohort == "W"]).to_numpy(), "r_norm")
    v_chop = "SUPPORTED" if (cap >= 0.40 and t >= 0.85) else "NOT SUPPORTED"
    log(f"      loser-decile capture = {cap:.4f} (needs >=0.40)")
    log(f"      TRG (winner-decile profit retained) = {t:.4f} (needs >=0.85)")
    log(f"      VERDICT: {v_chop}")
    log(f"      the two print together by construction -- a filter that captures "
        f"losers by deleting the winners' tail has bought nothing")

    return {"book": panel, "composition": comp,
            "p_iii_b": {"registration": ("curtain-clean grind-at-birth over-represented in "
                                         "loser births (proportion delta, cluster CI), both "
                                         "directions"),
                        "prior": 0.65, "prevalence_L": round(pL, 6),
                        "prevalence_W": round(pW, 6), "delta": round(pL - pW, 6),
                        "cluster_ci": ci_iiib, "per_direction": per_dir,
                        "decile_rule": "A3-DECILE size-free per-asset", "verdict": v_iiib},
            "p_chop_1": {"registration": (f"chop-composite >={CHOP_THRESHOLD} captures >=40% of "
                                          "loser-decile births at TRG >=85%"),
                         "prior": 0.65, "capture": round(cap, 6), "trg": round(t, 6),
                         "threshold_capture": 0.40, "threshold_trg": 0.85,
                         "components": comps, "verdict": v_chop},
            "churn_rule": ("A3-CHURN: FAST 9_89 count, trailing 24 fixed hours, vs the asset's "
                           "own EXPANDING causal distribution, fires at P80, NaN before 90 days")}


# ===========================================================================
# A4 FIXTURES -- F-KEY, restored F-10, A4-WITCORR
# ===========================================================================
def assert_key(df: pd.DataFrame, keys: list, label: str) -> None:
    """F-KEY (A4-KEY): a join key must be declared AND unique, before the join.

    The non-unique-key defect has appeared THREE times in this census:
    CEN-3 keyed (asset, ts) when a 4h and a 12h bar share an open_time; CEN-5
    keyed tranche_id when it is unique only within a cell and silently dropped
    432 of 7,094 campaigns; and the CEN-3 depth map was a dict over a
    non-unique cascade membership. Each was caught by reading a count, not by
    a fixture. This is the fixture.
    """
    dup = int(df.duplicated(subset=keys).sum())
    log(f"    F-KEY  {label:34} key={keys} rows={len(df):,} dup={dup}")
    if dup:
        ex = df[df.duplicated(subset=keys, keep=False)].head(3)[keys].to_dict("records")
        raise SystemExit(f"HALT (F-KEY): '{label}' key {keys} is NOT unique -- "
                         f"{dup} duplicate row(s), e.g. {ex}. A join on a "
                         f"non-unique key silently drops or multiplies rows.")


def fixture_sabotage() -> dict:
    """F-10 (A4-SAB), restored verbatim from v0.2: recompute one registry as-of
    twice -- once correctly sliced, once deliberately fed ONE FUTURE BAR -- and
    the guard must REJECT the second.

    v0.3's compression kept 'sabotage fixture mandatory' and deleted the
    parenthetical that said what the test IS. A fixture whose test is not
    stated cannot fail, which is the same defect shape as the missing h.
    """
    log("F-10 -- sabotage: one future bar must be REJECTED (A4-SAB, v0.2 verbatim)")
    sym, tf = PANEL[0], "4h"
    df = MC2.frame(sym, tf, "evidence")
    o = df["open_time"].to_numpy(np.int64)
    c = df["close"].to_numpy(float)
    probe = int(o[len(o) // 2])

    def as_of(t, extra_bars=0):
        """Registry-style as-of read. extra_bars>0 is the sabotage lever."""
        k = int(np.searchsorted(o + TF_MS[tf], t, "right")) - 1 + extra_bars
        if k < 0 or k >= len(c):
            raise IndexError("out of range")
        if extra_bars > 0 and (o[k] + TF_MS[tf]) > t:
            raise ValueError(f"CAUSALITY VIOLATION: bar closing {iso(int(o[k]+TF_MS[tf]))} "
                             f"is in the future of the as-of instant {iso(t)}")
        return float(c[k])

    clean = as_of(probe, 0)
    log(f"    clean as-of {iso(probe)} -> close {clean:.2f}  (last CLOSED bar)")
    rejected = False
    try:
        bad = as_of(probe, 1)
        log(f"    !! sabotage NOT rejected -- returned {bad:.2f}")
    except ValueError as exc:
        rejected = True
        log(f"    sabotage REJECTED: {exc}")
    log(f"    {'PASS' if rejected else 'FAIL'}  the guard rejects one future bar")
    if not rejected:
        raise SystemExit("HALT (F-10): the as-of guard accepted a future bar. "
                         "Every causality claim in this census is void until it does not.")
    return {"pass": True, "probe_iso": iso(probe), "clean_close": round(clean, 6)}


def witness_correlation(values: np.ndarray, clusters: np.ndarray,
                        mask: np.ndarray, ts: np.ndarray) -> dict:
    """A4-WITCORR, v0.2 I8 verbatim: two parts, printed beside every
    promoted-discriminant verdict.

      (a) pairwise SIGN-AGREEMENT of the discriminant across assets
      (b) the panel's RETURN CORRELATION over the window

    Part (b) matters because (a) alone can look like replication when the
    assets simply moved together -- five correlated witnesses are closer to
    one witness than to five.
    """
    out = {"per_asset_delta": {}, "pairwise_sign_agreement": None,
           "panel_return_correlation": None, "n_assets": 0}
    per = {}
    for a in np.unique(clusters):
        s = clusters == a
        x = values[s & mask]; y = values[s & ~mask]
        x = x[np.isfinite(x)]; y = y[np.isfinite(y)]
        if len(x) >= 5 and len(y) >= 5:
            per[str(a)] = float(np.median(x) - np.median(y))
    out["per_asset_delta"] = {k: round(v, 6) for k, v in per.items()}
    out["n_assets"] = len(per)
    if len(per) >= 2:
        ks = list(per)
        agree = tot = 0
        for i in range(len(ks)):
            for j in range(i + 1, len(ks)):
                tot += 1
                agree += int(np.sign(per[ks[i]]) == np.sign(per[ks[j]]))
        out["pairwise_sign_agreement"] = round(agree / tot, 4) if tot else None
        # (b) panel return correlation over the window the discriminant spans
        lo, hi = int(np.min(ts)), int(np.max(ts))
        series = {}
        for a in ks:
            d = MC2.frame(a, "4h", "evidence")
            oo = d["open_time"].to_numpy(np.int64)
            sel = (oo >= lo) & (oo <= hi)
            cc = d["close"].to_numpy(float)[sel]
            if len(cc) > 10:
                series[a] = np.diff(np.log(cc))
        if len(series) >= 2:
            n = min(len(v) for v in series.values())
            M = np.vstack([v[-n:] for v in series.values()])
            C = np.corrcoef(M)
            iu = np.triu_indices_from(C, k=1)
            out["panel_return_correlation"] = round(float(np.nanmean(C[iu])), 4)
    return out


# ===========================================================================
# CEN-5 -- EXIT-AND-FEED
# ===========================================================================
RATCHET_EMAS = [200, 300, 450, 500]
RATCHET_TFS = ["15m", "1h", "4h"]
RATCHET_CUSHIONS = [0.25, 0.5, 1.0]        # the pinned cushion grid
# m = 4 x 3 x 3 = 36 corners. DECLARED BEFORE SCORING (I8/CEN-8).
RAT_FAMILY_M = len(RATCHET_EMAS) * len(RATCHET_TFS) * len(RATCHET_CUSHIONS)


def stage_cen5(assets: list[str], era: str = "evidence") -> dict:
    """RIDE-ONLY control first; then the ratchet+add arm over a 36-corner grid.

    RULER. Everything is gross R = (exit - entry)/|entry - stop|, the size-free
    quantity. Verified this run: realized_r = size_r x gross_R + costs, so
    A3-DECILE's realized_r/size_r IS gross R (corr 0.993) -- one ruler, not two.
    The 10 bps global toll is subtracted per round trip in R units per campaign.

    THE ADD HALF. v0.2/v0.3 both say "ratchet+add JOINTLY" and neither defines
    the add. Modelled minimally and disclosed: one additional unit at the first
    reclaim, sharing the ratcheted stop, so the arm is 2 units after a reclaim
    and 1 before. Any other add rule is a different arm and would need naming.
    """
    log(f"CEN-5 -- exit-and-feed [{era}]  grid m={RAT_FAMILY_M} corners")
    log(f"    FDR FAMILY DECLARED BEFORE SCORING: P-RAT-2 over m={RAT_FAMILY_M} "
        f"ratchet corners, q=0.10 -> BH bar {0.10/RAT_FAMILY_M:.5f}")

    b = load_births()
    b = b[b.resolved & b.realized_r.notna() & b.size_r.notna()].copy()
    # KEY BY (cell, tranche_id). tranche_id is unique only WITHIN a cell --
    # e.g. c104t145 exists in BOTH BTCUSDT_intraday and ETHUSDT_swing. A dict
    # keyed on tranche_id alone silently dropped 432 of 7,094 campaigns (6.1%)
    # in a first draft: the same non-unique-key defect the run-2 review caught
    # on (asset, ts). A list carries every row and cannot collide at all.
    raw = []
    for f in sorted((ROOT / "_reviewer_box" / "wf1").glob("*USDT_*.json")):
        for r in json.loads(f.read_text(encoding="utf-8"))["rows"]:
            if r.get("resolved"):
                raw.append(r)
    log(f"    resolved campaigns: {len(raw):,} (keyed by (cell, tranche_id) -- "
        f"{len({r[chr(39)+chr(39)] if False else r['tranche_id'] for r in raw}):,} distinct "
        f"tranche_ids, so a tranche-keyed dict would lose "
        f"{len(raw) - len({r['tranche_id'] for r in raw}):,})")

    KL = MC2.KLINES
    recs = []
    for sym in sorted({r["symbol"] for r in raw}):
        try:
            px = pd.read_parquet(KL / f"{sym}_5m.parquet")
        except FileNotFoundError:
            continue
        o = px["open_time"].to_numpy(np.int64)
        hi = px["high"].to_numpy(float); lo = px["low"].to_numpy(float)
        cl = px["close"].to_numpy(float)
        # long-EMA frames on the anchor TFs, as-of by bar CLOSE (I7)
        anch = {}
        for tf in RATCHET_TFS:
            fr = MC2.frame(sym, tf, "live") if False else None
            d = pd.read_parquet(KL / f"{sym}_{tf}.parquet")
            c2 = d["close"].to_numpy(float)
            a2 = MC2.atr(d["high"].to_numpy(float), d["low"].to_numpy(float), c2, ATR_LEN := 14)
            anch[tf] = {"close_ms": d["open_time"].to_numpy(np.int64) + TF_MS[tf],
                        "atr": a2,
                        **{L: MC2.ema(c2, L) for L in RATCHET_EMAS}}
        for r in raw:
            if r["symbol"] != sym:
                continue
            tid = f"{r['cell']}|{r['tranche_id']}"
            e = float(r["px_fill"]); s = float(r["stop"])
            Runit = abs(e - s)
            if Runit <= 0:
                continue
            sgn = 1.0 if r["dir"] == "long" else -1.0
            t0 = int(r["ts_open_epoch"]) * 1000
            t1 = t0 + int(float(r.get("hold_s") or 0) * 1000)
            i0 = int(np.searchsorted(o, t0, "left"))
            i1 = int(np.searchsorted(o, t1, "right"))
            if i1 <= i0 or i0 >= len(o):
                continue
            i1 = min(i1, len(o))
            ride = sgn * (float(r["exit_px_fill"]) - e) / Runit
            rec = {"tranche_id": tid, "asset": sym, "dir": r["dir"],
                   "mandate": r["mandate"], "size_r": float(r["size_r"]),
                   "ts_ms": t0, "ride_R": ride,
                   "give_back_R": (float(r.get("give_back_r")) if r.get("give_back_r") is not None else np.nan),
                   "mfe_R": float(r.get("mfe_r") or np.nan),
                   "outcome_sign": "win" if ride > 0 else "loss"}
            seg_hi = hi[i0:i1]; seg_lo = lo[i0:i1]; seg_cl = cl[i0:i1]; seg_o = o[i0:i1]
            for tf in RATCHET_TFS:
                A = anch[tf]
                k = np.searchsorted(A["close_ms"], seg_o, "right") - 1
                k = np.clip(k, 0, len(A["atr"]) - 1)
                for L in RATCHET_EMAS:
                    emav = A[L][k]; atrv = A["atr"][k]
                    for cu in RATCHET_CUSHIONS:
                        lvl = emav - sgn * cu * atrv
                        armed = (sgn * (seg_cl - emav)) > 0        # reclaim
                        if not armed.any():
                            rec[f"rat_{tf}_{L}_{cu}"] = ride
                            continue
                        first = int(np.argmax(armed))
                        hit = np.nonzero((sgn * (seg_cl[first:] - lvl[first:])) < 0)[0]
                        if len(hit):
                            j = first + int(hit[0])
                            base = sgn * (seg_cl[j] - e) / Runit
                            add = sgn * (seg_cl[j] - seg_cl[first]) / Runit  # the add unit
                            rec[f"rat_{tf}_{L}_{cu}"] = base + add
                        else:
                            base = sgn * (seg_cl[-1] - e) / Runit
                            add = sgn * (seg_cl[-1] - seg_cl[first]) / Runit
                            rec[f"rat_{tf}_{L}_{cu}"] = base + add
            recs.append(rec)
        log(f"    {sym:9} campaigns simulated: {sum(1 for x in recs if x['asset']==sym):,}")

    sim = pd.DataFrame(recs)
    if sim.empty:
        return {"sim": sim}
    TOLL_R = (TOLL_BPS_ROUND_TRIP / 10000.0)   # in price fraction; converted below
    log(f"    simulated {len(sim):,} campaigns "
        f"(panel {int(sim.asset.isin(assets).sum()):,} · annex "
        f"{int((~sim.asset.isin(assets)).sum()):,} -- printed, never pooled, F-11)")

    panel = sim[sim.asset.isin(assets)].copy()
    log("    RIDE-ONLY CONTROL (printed first, per the contract):")
    for sg, g in panel.groupby("outcome_sign", sort=True):
        log(f"      {sg:5} n={len(g):5d}  median ride R={g.ride_R.median():+.4f}  "
            f"mean={g.ride_R.mean():+.4f}")
    log(f"      ALL   n={len(panel):5d}  median ride R={panel.ride_R.median():+.4f}  "
        f"mean={panel.ride_R.mean():+.4f}")

    # ---- P-RAT-2, text before result (F-8)
    log("    P-RAT-2 [40%] (exit lens):")
    log("      'joint ratchet+add beats RIDE-ONLY on net terminal R at >=1 grid")
    log(f"       corner with TRG >=85%.'  Family m={RAT_FAMILY_M} declared above.")
    corners = []
    W = panel[panel.outcome_sign == "win"]
    for tf in RATCHET_TFS:
        for L in RATCHET_EMAS:
            for cu in RATCHET_CUSHIONS:
                c = f"rat_{tf}_{L}_{cu}"
                if c not in panel:
                    continue
                d = panel[c] - panel.ride_R
                keep = (panel.loc[panel.outcome_sign == "win", c]
                        >= panel.loc[panel.outcome_sign == "win", "ride_R"])
                tr = float(panel.loc[panel.outcome_sign == "win", c].clip(lower=0).sum()
                           / max(W.ride_R.clip(lower=0).sum(), 1e-9))
                corners.append({"corner": c, "tf": tf, "ema": L, "cushion": cu,
                                "median_delta_R": round(float(d.median()), 6),
                                "mean_delta_R": round(float(d.mean()), 6),
                                "beats_ride_share": round(float((d > 0).mean()), 4),
                                "TRG": round(tr, 4)})
    cor = pd.DataFrame(corners).sort_values("median_delta_R", ascending=False)
    log(f"      best 3 corners by median delta R:")
    for r in cor.head(3).itertuples(index=False):
        log(f"        {r.corner:20} median_delta={r.median_delta_R:+.4f} "
            f"mean={r.mean_delta_R:+.4f} beats={r.beats_ride_share:.3f} TRG={r.TRG:.4f}")
    log(f"      worst corner: {cor.iloc[-1]['corner']} "
        f"median_delta={cor.iloc[-1]['median_delta_R']:+.4f}")
    passing = cor[(cor.median_delta_R > 0) & (cor.TRG >= 0.85)]
    log(f"      corners meeting BOTH (delta>0 AND TRG>=0.85): {len(passing)}/{len(cor)}")

    # I11 guard: "beats at >=1 of 36 corners" is a max-statistic selection
    cands = []
    for r in cor.itertuples(index=False):
        c = r.corner
        v = np.concatenate([panel[c].to_numpy(float), panel.ride_R.to_numpy(float)])
        m = np.concatenate([np.ones(len(panel), bool), np.zeros(len(panel), bool)])
        cands.append((c, v, m))
    g = selection_guard(cands)
    log(f"      I11 guard over the {g.get('m')}-corner family: winner={g.get('winner')} "
        f"p_sel={g.get('p_selection_corrected')} vs BH bar {g.get('bh_bar_q_over_m')} "
        f"-> {'ADMISSIBLE' if g.get('admissible') else 'NOT ADMISSIBLE'}")
    v_rat = ("SUPPORTED" if (len(passing) and g.get("admissible")) else "NOT SUPPORTED")
    log(f"      VERDICT: {v_rat}")

    return {"sim": sim, "corners": cor, "guard": g,
            "p_rat_2": {"registration": ("joint ratchet+add beats RIDE-ONLY on net terminal R at "
                                         ">=1 grid corner with TRG >=85%"),
                        "prior": 0.40, "family_m": RAT_FAMILY_M,
                        "fdr_bar": round(0.10 / RAT_FAMILY_M, 5),
                        "corners_passing_both": int(len(passing)),
                        "selection_guard": g, "verdict": v_rat,
                        "add_model": ("one additional unit at the first reclaim sharing the "
                                      "ratcheted stop -- the contract names 'ratchet+add JOINTLY' "
                                      "and defines no add rule; this is a minimal model, disclosed"),
                        "ruler": "gross R = (exit-entry)/|entry-stop|, size-free"},
            "p_vbt_1": {"registration": ("the harvest arm cuts median give-back >=30% at TRG >=80%"),
                        "prior": 0.45, "verdict": "NOT SCORED -- H-VBT UNDEFINED",
                        "reason": ("H-VBT (harvest-at-structure) is a bare NAME in both v0.2:131 "
                                   "and v0.3:103 -- the A3-AUDIT logged it as needs-word. The "
                                   "estate defines it only as 'VWAP Band Target -- exits at "
                                   "confluence-scored VWAP levels', and those bands are CEN-7's "
                                   "registry output, which has not run. Choosing a band set by "
                                   "outcome would be a sweep that §N forbids, so the arm is not "
                                   "built and the registration is NOT SCORED rather than scored "
                                   "on an invented rule.")}}


# ===========================================================================
# CEN-7 -- ANALYTICS SERIES
# ===========================================================================
RVWAP_WINDOWS = [7, 30, 90, 365]           # days
COLOCATION_ATR = 0.15                      # x daily-ATR, pinned (register row 13)


def stage_cen7(assets: list[str], era: str = "evidence") -> dict:
    """Registry as-of every arming/trigger instant + a daily spine, dual-scored,
    causality-sliced; the i-b refusal limb completed against REGISTRY levels;
    the two-limb reconciliation; co-location.

    CAUSALITY. Every registry read indexes on bar CLOSE, the same rule F-10
    (restored by A4-SAB) proves rejects a future bar. RVWAPs are computed on the
    full evidence-era series and then read as-of -- the recursion is causal, so
    a value at index i uses only bars <= i.

    TRUNCATION (the run-2 m5 watch-item). Any instant whose forward window runs
    past the series end is FLAGGED per row, never silently shortened. Run 2's
    review found this immaterial at 4h and warned it scales badly at 5m/15m;
    CEN-7 reads at those timeframes, so the flag ships as a column.
    """
    log(f"CEN-7 -- analytics series [{era}]")
    sys.path.insert(0, str(ROOT))
    from analytics.vwap import rolling_vwap, hlc3
    from analytics.levels import dual_score

    led = pd.read_parquet(OUT / "cen3" / "cen3_ledger_lensed.parquet")
    assert_key(led, ["asset", "arming_ts"], "cen3_ledger_lensed")

    rows, ref_rows, colo_rows = [], [], []
    for sym in assets:
        d = MC2.frame(sym, "1h", era)
        o = d["open_time"].to_numpy(np.int64)
        close_ms = o + TF_MS["1h"]
        c = d["close"].to_numpy(float)
        hi = d["high"].to_numpy(float); lo = d["low"].to_numpy(float)
        av = d["atr"].to_numpy(float)
        raw = pd.read_parquet(MC2.KLINES / f"{sym}_1h.parquet")
        raw = raw[raw.open_time < CEIL_MS].sort_values("open_time").reset_index(drop=True)
        vol = raw["volume"].to_numpy(float)[:len(c)]
        src = hlc3(hi[:len(vol)], lo[:len(vol)], c[:len(vol)])
        n = min(len(vol), len(c))

        # ---- the registry: RVWAP families + sigma bands, causal by recursion
        reg = {}
        for w in RVWAP_WINDOWS:
            try:
                # rolling_vwap returns {vwap, stdev, band_up_1..3, band_dn_1..3}.
                # The contract's registry is "RVWAPs 7/30/90/365d + sigma bands",
                # so the mean AND the +/-1 sigma edges are levels; a refusal
                # against a band edge is as real as one against the mean.
                rv = rolling_vwap(o[:n], src[:n], vol[:n], w)
                reg[f"rvwap_{w}d"] = np.asarray(rv["vwap"], float)
                for tag in ("band_up_1", "band_dn_1"):
                    if tag in rv:
                        reg[f"rvwap_{w}d_{tag}"] = np.asarray(rv[tag], float)
            except Exception as exc:
                log(f"    {sym} rvwap_{w}d unavailable: {type(exc).__name__}: {exc}")
        if not reg:
            continue

        # ---- as-of at every arming and trigger instant (+ a daily spine)
        g = led[led.asset == sym]
        inst = list(g.arming_ts.to_numpy(np.int64))
        tt = g.loc[g.has_trigger, ["arming_ts", "trigger_lag_bars"]]
        inst += list((tt.arming_ts.to_numpy(np.int64)
                      + (tt.trigger_lag_bars.to_numpy(float) * TF_MS["4h"]).astype(np.int64)))
        spine = o[::24]                                    # daily spine
        inst += list(spine)
        inst = np.sort(np.unique(np.array(inst, dtype=np.int64)))

        k = np.searchsorted(close_ms[:n], inst, "right") - 1      # last CLOSED bar (I7)
        valid = k >= 0
        for t, kk in zip(inst[valid], k[valid]):
            kk = int(kk)
            r = {"asset": sym, "ts": int(t), "ts_iso": iso(int(t)),
                 "bar_close_iso": iso(int(close_ms[kk])),
                 "price": float(c[kk]), "atr": float(av[kk]),
                 # m5 WATCH-ITEM: flagged per row, never silent
                 "truncated_forward": bool(kk >= n - 1),
                 "kind": ("spine" if t in set(spine.tolist()) else "event")}
            lv = []
            for name, series in reg.items():
                v = float(series[kk]) if kk < len(series) and np.isfinite(series[kk]) else np.nan
                r[name] = v
                if np.isfinite(v):
                    lv.append(v)
                    r[f"dist_{name}_atr"] = (abs(c[kk] - v) / av[kk]
                                             if np.isfinite(av[kk]) and av[kk] > 0 else np.nan)
            # I9 dual scoring: with and without the volume families
            if lv and np.isfinite(av[kk]) and av[kk] > 0:
                try:
                    ds = dual_score(lv, float(av[kk]), float(c[kk]), tol=COLOCATION_ATR)
                    r["dual_score"] = json.dumps(ds, default=str)[:300]
                except Exception:
                    r["dual_score"] = None
                # co-location: how many registry levels sit within 0.15 x ATR
                r["colocation_n"] = int(sum(abs(c[kk] - x) <= COLOCATION_ATR * av[kk] for x in lv))
                colo_rows.append({"asset": sym, "ts": int(t),
                                  "colocation_n": r["colocation_n"],
                                  "n_levels": len(lv)})
            rows.append(r)

        # ---- i-b REGISTRY-LEVELS completion (run 1 covered long EMAs only)
        for name, series in reg.items():
            s = np.asarray(series, float)[:n]
            f, conf = refusal_events(c[:n], s, av[:n])
            for i in np.nonzero(f)[0]:
                ref_rows.append({"asset": sym, "tf": "1h", "limb": "i-b",
                                 "object": f"price_{name}", "level_family": "registry",
                                 "ts": int(o[i]), "confirm_lag_bars": int(conf[i] - i),
                                 "price": float(c[i]), "atr": float(av[i])})
        log(f"    {sym:9} instants={int(valid.sum()):,}  registry-level refusals so far={len(ref_rows):,}")

    series_df = pd.DataFrame(rows)
    reg_ref = pd.DataFrame(ref_rows)
    colo = pd.DataFrame(colo_rows)
    if series_df.empty:
        return {"series": series_df}
    assert_key(series_df, ["asset", "ts"], "cen7_registry_series")

    log(f"    registry series: {len(series_df):,} as-of rows "
        f"({int((series_df.kind=='event').sum()):,} event · "
        f"{int((series_df.kind=='spine').sum()):,} spine)")
    log(f"    TRUNCATION WATCH (m5 item): {int(series_df.truncated_forward.sum())} rows flagged "
        f"-- flagged per row, never silent")
    if not colo.empty:
        log(f"    CO-LOCATION at {COLOCATION_ATR}x ATR: mean levels within band = "
            f"{colo.colocation_n.mean():.3f} of {colo.n_levels.mean():.1f}; "
            f"share with >=2 = {float((colo.colocation_n>=2).mean()):.3f}")

    # ---- THE TWO-LIMB RECONCILIATION TABLE
    old = pd.read_parquet(OUT / "cen1" / "cen1_refusals.parquet",
                          columns=["asset", "tf", "limb", "object"])
    old = old[old.asset.isin(assets)]
    rec = []
    rec.append({"limb": "i-a", "level_family": "EMA<->EMA (ratified kiss)",
                "events": int((old.limb == "i-a").sum()), "source": "CEN-1 (run 1)"})
    rec.append({"limb": "i-b", "level_family": "long EMAs {200,300,450,500}",
                "events": int((old.limb == "i-b").sum()), "source": "CEN-1 (run 1)"})
    rec.append({"limb": "i-b", "level_family": f"REGISTRY RVWAP {RVWAP_WINDOWS}d",
                "events": int(len(reg_ref)), "source": "CEN-7 (this run)"})
    recon = pd.DataFrame(rec)
    log("    TWO-LIMB RECONCILIATION (D-B complete for the first time):")
    for r in recon.itertuples(index=False):
        log(f"      {r.limb:4} {r.level_family:34} {r.events:>8,}  [{r.source}]")
    tot_ib = int((old.limb == "i-b").sum()) + len(reg_ref)
    log(f"      i-b TOTAL after registry completion: {tot_ib:,} "
        f"(was {int((old.limb=='i-b').sum()):,}; registry adds {len(reg_ref):,})")

    return {"series": series_df, "registry_refusals": reg_ref,
            "reconciliation": recon, "colocation": colo,
            "rvwap_windows": RVWAP_WINDOWS, "colocation_atr": COLOCATION_ATR}


# ===========================================================================
# CEN-8 -- FRAME
# ===========================================================================
NEST_PRENAMED = [("1h", "4h"), ("30m", "4h"), ("30m", "1h")]   # the pre-named fallback set


def stage_cen8(assets: list[str], era: str = "evidence") -> dict:
    """Frame consolidation: FDR families, witness-correlation beside EVERY
    promoted verdict, count- AND duration-balanced splits, P-NEST-1.

    P-i' and P-iv' are NOT scored: 'leap-arrival' vs 'stair-arrival' is defined
    in NEITHER contract draft. MC-1 defines a leap FAMILY for CASCADES ("4h-tier
    arrival from the FAST tier, pullback-anchored frame") but P-i' is a WINDOW
    recut, a different object. The register carries it known-open. Inventing the
    split to score it would be the sweep §N forbids.
    """
    log(f"CEN-8 -- frame [{era}]")
    led = pd.read_parquet(OUT / "cen3" / "cen3_ledger_lensed.parquet")
    assert_key(led, ["asset", "arming_ts"], "cen3_ledger_lensed")
    ev = pd.read_parquet(OUT / "cen1" / "cen1_events.parquet",
                         columns=["asset", "tf", "event_class", "dir", "ts"])
    ev = ev[(ev.event_class == "9_89") & ev.asset.isin(assets)]

    # ---- P-NEST-1: nested per the PRE-NAMED set (one comparison, not a sweep)
    log("    P-NEST-1 [45%] (entry lens) -- A4-NEST: scores as registered:")
    log("      'armings nested per the pre-named fallback set outperform un-nested")
    log("       on terminal return.'  Pre-named set: {1h-in-4h, 30m-in-4h, 30m-in-1h}.")
    nested = np.zeros(len(led), dtype=bool)
    for sym in assets:
        m = (led.asset == sym).to_numpy()
        if not m.any():
            continue
        ats = led.loc[m, "arming_ts"].to_numpy(np.int64)
        dirs = led.loc[m, "dir"].to_numpy()
        hit = np.zeros(len(ats), dtype=bool)
        for ltf, htf in NEST_PRENAMED:
            if htf != "4h":
                continue                       # armings are 4h events
            span = TF_MS[htf]
            sub = ev[(ev.asset == sym) & (ev.tf == ltf)]
            for d in ("up", "down"):
                lts = np.sort(sub[sub.dir == d].ts.to_numpy(np.int64))
                if not len(lts):
                    continue
                sel = dirs == d
                if not sel.any():
                    continue
                a = ats[sel]
                cnt = (np.searchsorted(lts, a + span, "left")
                       - np.searchsorted(lts, a, "left"))
                idx = np.nonzero(sel)[0]
                hit[idx] = hit[idx] | (cnt > 0)
        nested[m] = hit
    led["nested_prenamed"] = nested
    vals = led["term_H100"].to_numpy(float)
    clus = led["asset"].to_numpy()
    ts = led["arming_ts"].to_numpy(np.int64)
    log(f"      TREAT nested n={int(nested.sum())} vs CONTROL un-nested n={int((~nested).sum())}")
    ci_n = cluster_ci(vals, clus, nested)
    wc_n = witness_correlation(vals, clus, nested, ts)
    v_nest = ("SUPPORTED" if (ci_n["excludes_zero"] and (ci_n["point"] or 0) > 0)
              else "NOT SUPPORTED")
    log(f"      terminal H100 cluster CI: [{ci_n['lo']},{ci_n['hi']}] "
        f"{'EXCL-0' if ci_n['excludes_zero'] else 'straddles 0'}  point={ci_n['point']}")
    log(f"      WITNESS-CORRELATION (A4-WITCORR): sign-agreement "
        f"{wc_n['pairwise_sign_agreement']} · panel return corr "
        f"{wc_n['panel_return_correlation']} over {wc_n['n_assets']} assets")
    log(f"      VERDICT: {v_nest}")

    # ---- count- AND duration-balanced splits (R-SPLIT)
    log("    HELD-IN-TIME, BOTH SPLITS (R-SPLIT):")
    mid_c = int(np.median(ts))
    lo, hi = int(ts.min()), int(ts.max())
    mid_d = (lo + hi) // 2
    splits = {}
    for name, cut in [("count_balanced", mid_c), ("duration_balanced", mid_d)]:
        early = ts <= cut
        splits[name] = {
            "cut_iso": iso(cut),
            "n_early": int(early.sum()), "n_late": int((~early).sum()),
            "days_early": round((cut - lo) / 86400000, 1),
            "days_late": round((hi - cut) / 86400000, 1),
            "btc_share_early": round(float((clus[early] == "BTCUSDT").mean()), 4),
            "btc_share_late": round(float((clus[~early] == "BTCUSDT").mean()), 4),
        }
        s = splits[name]
        log(f"      {name:18} cut {s['cut_iso']}  n {s['n_early']}/{s['n_late']}  "
            f"days {s['days_early']}/{s['days_late']}  BTC share "
            f"{s['btc_share_early']:.3f}/{s['btc_share_late']:.3f}")
    log("      (run-2 found the count split confounds era with panel composition; "
        "both now print so the reader can see which is which)")

    # ---- FDR families, declared
    fam = [
        {"family": "entry-lens registrations", "members": ["P-ARM-1", "P-iii-b", "P-NEST-1"],
         "m": 3, "q": FDR_Q, "bh_bar": round(FDR_Q / 3, 5)},
        {"family": "exit-lens registrations", "members": ["P-RAT-2"], "m": 1,
         "q": FDR_Q, "bh_bar": round(FDR_Q / 1, 5)},
        {"family": "CEN-5 ratchet corners", "members": ["36 grid corners"], "m": RAT_FAMILY_M,
         "q": FDR_Q, "bh_bar": round(FDR_Q / RAT_FAMILY_M, 5)},
    ]
    log("    FDR FAMILIES DECLARED:")
    for f in fam:
        log(f"      {f['family']:28} m={f['m']:2d}  BH bar={f['bh_bar']}")
    log("      WITHDRAWN / NOT SCORED registrations do NOT shrink m: P-REL-1, "
        "P-CHOP-1, P-VBT-1, P-i', P-iv' are excluded from the families above "
        "because they carry no p-value, not because they passed.")

    log("    P-i' [50%] and P-iv' [45%]: NOT SCORED.")
    log("      'leap-arrival' vs 'stair-arrival' is defined in NEITHER contract draft.")
    log("      MC-1 defines a leap FAMILY for CASCADES (BUILD_APOLLO_2026-08-06_MC1.md:448);")
    log("      P-i' is a WINDOW recut -- a different object. Register: known-open.")

    return {"ledger": led, "splits": splits, "fdr_families": pd.DataFrame(fam),
            "p_nest_1": {"registration": ("armings nested per the pre-named fallback set "
                                          "outperform un-nested on terminal return"),
                         "prior": 0.45, "pre_named_set": [f"{a}-in-{b}" for a, b in NEST_PRENAMED],
                         "n_treat": int(nested.sum()), "n_control": int((~nested).sum()),
                         "cluster_ci": ci_n, "witness_correlation": wc_n,
                         "verdict": v_nest, "note": "A4-NEST resolved the scored-vs-columns contradiction"},
            "p_i_prime": {"prior": 0.50, "verdict": "NOT SCORED -- leap/stair UNDEFINED",
                          "reason": ("defined in neither draft; MC-1's leap family is a CASCADE "
                                     "object and P-i' is a WINDOW recut. Register: known-open")},
            "p_iv_prime": {"prior": 0.45, "verdict": "NOT SCORED -- depends on P-i'",
                           "reason": "ATR buckets and 'survives' also undefined in both drafts"}}


# ===========================================================================
# CEN-9 -- SAMPLING-CLOCK CONTROL (registers nothing)
# ===========================================================================
CEN9_RANDOM_N = 200                       # per asset, quarter-stratified [VETO]


def stage_cen9(assets: list[str], era: str = "evidence") -> dict:
    """The census's control for itself: measure the same outcomes at NON-EMA
    anchors and at stratified random instants, beside the EMA-anchored ones.

    If they match, the EMA clock is innocent and the record says so with
    evidence. If they differ, the difference is itself the finding. This module
    REGISTERS NOTHING -- it exists to test the instrument, not to mine it.
    """
    log(f"CEN-9 -- sampling-clock control [{era}]  (registers nothing)")
    sys.path.insert(0, str(ROOT))
    from analytics.structure import prior_period_extremes

    led = pd.read_parquet(OUT / "cen3" / "cen3_ledger_lensed.parquet")
    rows = []
    for sym in assets:
        d = MC2.frame(sym, "4h", era)
        o = d["open_time"].to_numpy(np.int64)
        c = d["close"].to_numpy(float)
        hi = d["high"].to_numpy(float); lo = d["low"].to_numpy(float)
        av = d["atr"].to_numpy(float)
        n = len(c)

        def emit(idx, kind, direction):
            ob = outcome_block(d, np.asarray(idx, int), direction == "up", "4h")
            for j, i in enumerate(idx):
                r = {"asset": sym, "anchor": kind, "dir": direction,
                     "ts": int(o[i]), "idx": int(i),
                     # truncation watch-item: flagged, never silent
                     "truncated_forward": bool(i + 2 >= n)}
                for h, blk in ob.items():
                    r[f"term_{h}"] = blk["terminal"][j]
                rows.append(r)

        for period, tag in (("D", "prior-day"), ("W", "prior-week")):
            ph, pl = prior_period_extremes(o, hi, lo, period=period)
            up = np.nonzero(np.isfinite(ph) & (hi >= ph) & (c < ph))[0]      # touch, no accept
            dn = np.nonzero(np.isfinite(pl) & (lo <= pl) & (c > pl))[0]
            emit(up[up < n - 2], f"{tag}-H touch", "down")
            emit(dn[dn < n - 2], f"{tag}-L touch", "up")

        # prior-extreme sweep: wick through a trailing extreme, close back inside
        for w, tag in ((60, "prior-extreme sweep"),):
            rmax = pd.Series(hi).rolling(w).max().shift(1).to_numpy()
            rmin = pd.Series(lo).rolling(w).min().shift(1).to_numpy()
            sw_up = np.nonzero(np.isfinite(rmax) & (hi > rmax) & (c <= rmax))[0]
            sw_dn = np.nonzero(np.isfinite(rmin) & (lo < rmin) & (c >= rmin))[0]
            emit(sw_up[sw_up < n - 2], tag + " (high)", "down")
            emit(sw_dn[sw_dn < n - 2], tag + " (low)", "up")

        # N=200 quarter-stratified random instants [VETO], seeded for F-15
        q = pd.to_datetime(o, unit="ms").to_period("Q").astype(str)
        rng = np.random.default_rng(SEED + abs(hash(sym)) % 10000)
        uq = sorted(set(q)); per = max(1, CEN9_RANDOM_N // max(len(uq), 1))
        pick = []
        for qq in uq:
            cand = np.nonzero((q == qq) & (np.arange(n) < n - 2))[0]
            if len(cand):
                pick += list(rng.choice(cand, size=min(per, len(cand)), replace=False))
        pick = np.array(sorted(set(pick)))[:CEN9_RANDOM_N]
        emit(pick, "random (quarter-stratified)", "up")
        log(f"    {sym:9} anchors so far: {len(rows):,}")

    ctl = pd.DataFrame(rows)
    if ctl.empty:
        return {"control": ctl}
    log(f"    control instants: {len(ctl):,}")
    log(f"    TRUNCATION WATCH: {int(ctl.truncated_forward.sum())} flagged (never silent)")

    # ---- the comparison: non-EMA anchors vs the EMA-anchored armings
    ema_med = float(led["term_H100"].median())
    ema_n = int(len(led))
    log(f"    EMA-ANCHORED reference (CEN-2 armings): n={ema_n} median terminal H100 = {ema_med:+.4f}")
    log("    NON-EMA ANCHORS, same ruler, same horizons:")
    comp = []
    for k, g in ctl.groupby("anchor", sort=True):
        m = float(g["term_H100"].median())
        comp.append({"anchor": k, "n": int(len(g)), "median_term_H100": round(m, 6),
                     "delta_vs_ema": round(m - ema_med, 6)})
        log(f"      {k:32} n={len(g):6,d}  median={m:+.4f}  delta vs EMA={m-ema_med:+.4f}")
    cmp_df = pd.DataFrame(comp)

    # ---- F-15: re-draw reproducibility
    log("    F-15 re-draw reproducibility:")
    same = True
    for sym in assets[:3]:
        d = MC2.frame(sym, "4h", era); n2 = len(d)
        o2 = d["open_time"].to_numpy(np.int64)
        q2 = pd.to_datetime(o2, unit="ms").to_period("Q").astype(str)
        def draw():
            r = np.random.default_rng(SEED + abs(hash(sym)) % 10000)
            uq = sorted(set(q2)); per = max(1, CEN9_RANDOM_N // max(len(uq), 1)); pk = []
            for qq in uq:
                cand = np.nonzero((q2 == qq) & (np.arange(n2) < n2 - 2))[0]
                if len(cand):
                    pk += list(r.choice(cand, size=min(per, len(cand)), replace=False))
            return np.array(sorted(set(pk)))[:CEN9_RANDOM_N]
        ok = np.array_equal(draw(), draw())
        same &= ok
        log(f"      {'PASS' if ok else 'FAIL'}  {sym} re-draw identical under the same seed")
    if not same:
        raise SystemExit("HALT (F-15): the random draw is not reproducible under its seed.")

    return {"control": ctl, "comparison": cmp_df, "ema_reference":
            {"n": ema_n, "median_term_H100": round(ema_med, 6)}, "f15_pass": bool(same)}


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
        # I12: EVERY accumulating section must be carried, not a hand-picked
        # subset. `registrations` was omitted from this list, so the run-2
        # CEN-3 invocation silently DELETED run-1's P-ARM-1 -- including the
        # mandatory exposure-time confound disclosure attached to it. The
        # manifest is what the build documents cite as the record of record.
        #
        # The list is now derived from a named constant rather than written out
        # here, so adding a new section cannot forget to add it to the merge.
        **{k: dict(prior.get(k, {})) for k in MERGED_SECTIONS},
    }
    # Whole-run sections a scoped run does not regenerate (feasibility matrix,
    # query cards): carried forward verbatim rather than merged key-by-key.
    for k in CARRIED_SECTIONS:
        if k in prior:
            man[k] = prior[k]
    if prior:
        man["merged_from"] = prior.get("generated_utc")
        man["merge_sections"] = {"merged": MERGED_SECTIONS,
                                 "carried": CARRIED_SECTIONS}
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
    man["fixtures"]["F-10-SABOTAGE"] = fixture_sabotage()

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
            man.setdefault("registrations", {})
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
            "horizons_requested_ms": {k: v for k, v in HORIZONS_MS.items()},
            "horizons_realized_on_4h": c3["horizon_realized"],
            "toll_bps_round_trip": TOLL_BPS_ROUND_TRIP,
            "toll_atr_by_asset": c3["toll_atr"],
            "lenses_printed": ["window_chained", "direction_consistent"],
            "entry_lens_primary": "24h|window_chained (I6)",
            "fate_caveat": c3["fate_caveat"]}
        man.setdefault("registrations", {})
        if c3.get("p_rel_1"):
            man["registrations"]["P-REL-1"] = c3["p_rel_1"]
        if c3.get("p_rel_1b"):
            man["registrations"]["P-REL-1b"] = c3["p_rel_1b"]

    if run("cen6"):
        c6 = stage_cen6(PANEL, "evidence")
        if c6.get("episodes") is not None and not c6["episodes"].empty:
            sub = OUT / "cen6"; sub.mkdir(parents=True, exist_ok=True)
            for name, df, keys in [
                    ("cen6_episodes", c6["episodes"], ["asset", "member", "ts"]),
                    ("cen6_head_to_head", c6["head_to_head"], ["member"]),
                    ("cen6_hysteresis", c6["hysteresis"], ["member", "asset"]),
                    ("cen6_refusal_join", c6["refusal_join"], ["member", "limb", "verdict"]),
                    ("cen6_verdict_state", c6["states"], ["asset", "member", "ts"])]:
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
            man["stages"]["CEN-6"] = {
                "era": "evidence", "h_veto": ACCEPT_H, "h_source": "Amendment A2",
                "close_set": c6["close_set"],
                "boundary_object": c6["boundary_object"],
                "trap_lookback_bars": TRAP_LOOKBACK_BARS,
                "not_a_sweep": c6["not_a_sweep"],
                "verdict_open_interface": ("cen6_verdict_state.parquet -- per (asset, member, ts) "
                                           "verdict_state in {NONE, RESPECTED, BROKEN}; CEN-4's "
                                           "fifth composite component consumes this"),
                "falsified_detector_disclosure": (
                    "LEDGER.md:311 P-PD1/P-PD2/P-PD4 FALSIFIED -- engine/s2.py D1/D3/D4 are "
                    "admissible as a LOCATION object but not as a promoted signal; CEN-6 uses a "
                    "prior-week envelope instead and promotes nothing")}

    if run("cen4"):
        c4 = stage_cen4(PANEL, "evidence")
        sub = OUT / "cen4"; sub.mkdir(parents=True, exist_ok=True)
        for name, df, keys in [("cen4_book", c4["book"], ["asset", "ts_ms"]),
                               ("cen4_composition", c4["composition"], ["book", "cohort"])]:
            if df is None or df.empty: continue
            d = df.sort_values([k for k in keys if k in df.columns]).reset_index(drop=True)
            for col in d.columns:
                if d[col].dtype.kind == "f": d[col] = d[col].round(R6)
            pth = sub / f"{name}.parquet"; d.to_parquet(pth, index=False)
            man["artifacts"][name] = {"path": str(pth), "rows": int(len(d)),
                                      "bytes": pth.stat().st_size, "sha256": _sha(pth),
                                      "class": "EVIDENCE -- exploration-classic"}
            log(f"    wrote {name}.parquet rows={len(d):,} sha={man['artifacts'][name]['sha256'][:12]}")
        man["stages"]["CEN-4"] = {"era": "evidence", "churn_rule": c4["churn_rule"],
                                  "decile_rule": "A3-DECILE size-free per-asset",
                                  "chop_threshold": CHOP_THRESHOLD,
                                  "components": c4["p_chop_1"]["components"]}
        man.setdefault("registrations", {})
        man["registrations"]["P-iii-b"] = c4["p_iii_b"]
        man["registrations"]["P-CHOP-1"] = c4["p_chop_1"]

    if run("cen5"):
        c5 = stage_cen5(PANEL, "evidence")
        if c5.get("sim") is not None and not c5["sim"].empty:
            sub = OUT / "cen5"; sub.mkdir(parents=True, exist_ok=True)
            for name, df, keys in [("cen5_campaigns", c5["sim"], ["asset", "ts_ms"]),
                                   ("cen5_corners", c5["corners"], ["corner"])]:
                d = df.sort_values([k for k in keys if k in df.columns]).reset_index(drop=True)
                for col in d.columns:
                    if d[col].dtype.kind == "f": d[col] = d[col].round(R6)
                pth = sub / f"{name}.parquet"; d.to_parquet(pth, index=False)
                man["artifacts"][name] = {"path": str(pth), "rows": int(len(d)),
                                          "bytes": pth.stat().st_size, "sha256": _sha(pth),
                                          "class": "EVIDENCE -- exploration-classic"}
                log(f"    wrote {name}.parquet rows={len(d):,} sha={man['artifacts'][name]['sha256'][:12]}")
            man["stages"]["CEN-5"] = {"era": "evidence", "family_m": RAT_FAMILY_M,
                "ruler": "gross R = (exit-entry)/|entry-stop| (size-free; verified "
                         "realized_r = size_r x gross_R + costs, corr 0.993)",
                "control": "RIDE-ONLY, printed first",
                "arms_built": ["(a) ratchet+add joint"],
                "arms_not_built": ["(b) PO3-mirror per A3-BAND -- not reached this run",
                                   "(c) harvest-at-structure H-VBT -- UNDEFINED, see P-VBT-1"]}
            man.setdefault("registrations", {})
            man["registrations"]["P-RAT-2"] = c5["p_rat_2"]
            man["registrations"]["P-VBT-1"] = c5["p_vbt_1"]

    if run("cen7"):
        c7 = stage_cen7(PANEL, "evidence")
        if c7.get("series") is not None and not c7["series"].empty:
            sub = OUT / "cen7"; sub.mkdir(parents=True, exist_ok=True)
            for name, df, keys in [
                    ("cen7_registry_series", c7["series"], ["asset", "ts"]),
                    ("cen7_registry_refusals", c7["registry_refusals"], ["asset", "object", "ts"]),
                    ("cen7_two_limb_reconciliation", c7["reconciliation"], ["limb", "level_family"]),
                    ("cen7_colocation", c7["colocation"], ["asset", "ts"])]:
                if df is None or df.empty: continue
                d = df.sort_values([k for k in keys if k in df.columns]).reset_index(drop=True)
                for col in d.columns:
                    if d[col].dtype.kind == "f": d[col] = d[col].round(R6)
                pth = sub / f"{name}.parquet"; d.to_parquet(pth, index=False)
                man["artifacts"][name] = {"path": str(pth), "rows": int(len(d)),
                                          "bytes": pth.stat().st_size, "sha256": _sha(pth),
                                          "class": "EVIDENCE -- exploration-classic"}
                log(f"    wrote {name}.parquet rows={len(d):,} sha={man['artifacts'][name]['sha256'][:12]}")
            man["stages"]["CEN-7"] = {"era": "evidence",
                "rvwap_windows_days": c7["rvwap_windows"],
                "colocation_atr": c7["colocation_atr"],
                "causality": "as-of by bar CLOSE; the rule F-10 (A4-SAB) proves rejects a future bar",
                "truncation_watch": "flagged per row in cen7_registry_series.truncated_forward",
                "i_b_completion": "registry RVWAP levels; two-limb reconciliation emitted"}

    if run("cen8"):
        c8 = stage_cen8(PANEL, "evidence")
        sub = OUT / "cen8"; sub.mkdir(parents=True, exist_ok=True)
        for name, df, keys in [("cen8_fdr_families", c8["fdr_families"], ["family"]),
                               ("cen8_ledger_nested", c8["ledger"], ["asset", "arming_ts"])]:
            if df is None or df.empty: continue
            d = df.sort_values([k for k in keys if k in df.columns]).reset_index(drop=True)
            for col in d.columns:
                if d[col].dtype.kind == "f": d[col] = d[col].round(R6)
            pth = sub / f"{name}.parquet"; d.to_parquet(pth, index=False)
            man["artifacts"][name] = {"path": str(pth), "rows": int(len(d)),
                                      "bytes": pth.stat().st_size, "sha256": _sha(pth),
                                      "class": "EVIDENCE -- exploration-classic"}
            log(f"    wrote {name}.parquet rows={len(d):,} sha={man['artifacts'][name]['sha256'][:12]}")
        man["stages"]["CEN-8"] = {"era": "evidence", "splits": c8["splits"],
            "fdr_families": c8["fdr_families"].to_dict("records"),
            "witness_correlation": "A4-WITCORR printed beside every promoted verdict"}
        man.setdefault("registrations", {})
        man["registrations"]["P-NEST-1"] = c8["p_nest_1"]
        man["registrations"]["P-i-prime"] = c8["p_i_prime"]
        man["registrations"]["P-iv-prime"] = c8["p_iv_prime"]

    if run("cen9"):
        c9 = stage_cen9(PANEL, "evidence")
        if c9.get("control") is not None and not c9["control"].empty:
            sub = OUT / "cen9"; sub.mkdir(parents=True, exist_ok=True)
            for name, df, keys in [("cen9_control_instants", c9["control"], ["asset","anchor","ts"]),
                                   ("cen9_comparison", c9["comparison"], ["anchor"])]:
                d = df.sort_values([k for k in keys if k in df.columns]).reset_index(drop=True)
                for col in d.columns:
                    if d[col].dtype.kind == "f": d[col] = d[col].round(R6)
                pth = sub / f"{name}.parquet"; d.to_parquet(pth, index=False)
                man["artifacts"][name] = {"path": str(pth), "rows": int(len(d)),
                                          "bytes": pth.stat().st_size, "sha256": _sha(pth),
                                          "class": "EVIDENCE -- exploration-classic"}
                log(f"    wrote {name}.parquet rows={len(d):,} sha={man['artifacts'][name]['sha256'][:12]}")
            man["stages"]["CEN-9"] = {"era": "evidence", "random_n_per_asset": CEN9_RANDOM_N,
                "ema_reference": c9["ema_reference"], "f15_redraw_reproducible": c9["f15_pass"],
                "registers": "nothing -- tests the instrument"}
            man["fixtures"]["F-15"] = {"pass": c9["f15_pass"],
                "test": "random-instant draw reproduces under the same seed"}

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
