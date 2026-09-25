#!/usr/bin/env python
"""TIER-C11 · STAGE S — F-SCALP-GATE · F-GRID · F-KEY · F-DET.  The fixtures of
scripts/tierc11_stage_s.py (the scalper's R2 gate at 1h, and the CLOSED record it
files when the gate does not open) [LEANS L-S.1, L-R.4, L-1.2, §10].

TWO LEGS PER FIXTURE, the BREAK leg first, and it must go RED or the fixture is
VOID — a guard nobody has seen fail is a guard nobody has seen [the prove() law
of scripts/tierc10_rf_fixtures.py / tierc10_resume_fixtures.py; house style of
scripts/tierc11_books_fixtures.py].  A break leg is a set of PLANTS judged one at
a time; a plant counts as CAUGHT only if a finding NAMES THE INTENDED DETECTOR
(its expected substring).  A plant that crashes is a FIXTURE DEFECT, never a
catch.  Every plant is made on a COPY (a planted verdicts file, a planted
feasibility parquet and manifest, a copied table, a scratch run dir under
RUN_ROOT/_det_stage_s) or under a MUTATION of the module restored in `finally`;
no artifact of record moves.  The REFEREES are typed HERE (a second object): the
[Q-R3] law (30 / 3.0 / 0.10 / 30 / 30 / net > 0, round 8), the three words and
the reopening-path word, the record's (pool, era, scale, toll), the status word
and the reason format, the collar, the banned verdict columns, the 108 declared
cells, the table's column commission and the file sets.  The fixture RE-DERIVES
every word it judges from the printed columns by its own code (fx_word) —
never through the module's law.

  F-SCALP-GATE  FAILS IF the fixture's own reading of R2_LENS_VERDICTS.json's 1h
                row (the [Q-R3] law on its printed columns, the net identity,
                L-R.4's reopening clause with the maker twin re-derived from
                R2_FEASIBILITY.parquet) disagrees with the row's printed word /
                verdict / provisional / maker_twin / charter_twin /
                tier_e_tuning_word; or the module, run from the files of record
                into a scratch dir AND as filed of record, does not file exactly
                the CLOSED record the fixture derives: STATUS.json {registration
                P-SCALP-2, status CLOSED_BY_PRECONDITION, reason 'CLOSED BY R2
                (1h: <verdict>)', arms [], the 1h R2 row whole, the maker-twin
                word, the tuning-era word beside with the collar, the source sha
                of the verdicts file now on disk}, S_GATE.json (gate CLOSED, the
                clause truth values, the words), STAGE_S.md (the title, every
                field of the 1h row printed whole, the stop, the maker-twin word,
                the tuning-era word beside) and regbooks/P-SCALP-2 holding
                STATUS.json only; or it files CLOSED on a PASS; or a
                reopening-path label opens the gate; or a PASS the JSON, the
                parquet and the manifest do not all print opens it.  SABOTAGE —
                planted verdicts files: the real 1h columns labelled PASS; a
                passing row broken at EACH of the six clauses at its boundary
                (n_ranges 29, ratio 2.99999999, share 0.10000001, edge_n_ranges
                29, edge_n 29, net exactly 0) labelled PASS; a printed net that
                is not its parts' difference (off by 0.178, and off by 1e-8); an
                under-floor row labelled plain FAIL (n_ranges 29, and
                edge_n_ranges 29 alone); a provisional flag that lies; a
                maker-twin PASS without the reopening-path verdict; the row's
                pool / era / scale / toll, the file's record block and the
                row's member set (four members, six members, a non-CLASSIC5
                fallback member) moved off the verdict of record; no 1h lens
                (each must HALT its named detector); a GENUINE PASS set and a
                PASS at the law's inclusive boundaries (30 / 3.0 / 0.10 / 30 /
                30 / net 1e-8), JSON + parquet + manifest agreeing — the gate
                must OPEN (GATE-OPEN: the gate is not stuck); a PASS in the JSON
                only (R2-MANIFEST) and in the JSON + manifest only (JSON-PARQUET)
                — it must NOT open.  Planted feasibility parquets: the record row
                moved (median + net), and moved at EACH of the 21 typed JSON /
                parquet field pairs one at a time (JSON-PARQUET); a second 1h row
                flagged of record (JSON-PARQUET); the maker / charter / tuning /
                ALL rows lifted to PASS (MAKER-TWIN / CHARTER-TWIN / TUNING-WORD
                / ALL-WORD); a block row's printed word flipped (R2-ROW-WORD);
                the record row under the Tier-E collar and a Tier-E row under the
                record collar (R2-COLLAR); a parquet the manifest does not vouch
                for and a manifest whose 1h word differs (R2-MANIFEST).
                Mutations: a gate stuck open on the files of record (GATE-OPEN);
                a gate stuck CLOSED on the genuine PASS set (CLOSED-ON-PASS, the
                fixture's own detector); the edge law read as net > -1
                (LABEL-LAW); the reopening clause removed (LABEL-LAW); a stray
                scored.parquet and a stray scored.json in the regbook dir
                (STRAY-BOOK).
  F-GRID        FAILS IF S_R2_1H.parquet is not the 108 declared cells exactly
                (TP.grid_whole: no missing, undeclared or duplicated cell, every
                typed column non-null), a row's collar is not L-1.4's (the
                Tier-E collar on every row but the record row, Stage R's record
                collar on it — typed here) or a row carries a verdict column,
                any printed value (the collar included) differs from R2_FEASIBILITY's
                row for its cell, any clause truth value / net_rederived /
                would_read differs from the fixture's own re-derivation, the R2
                word is not the row's printed word, the record flag is not on
                exactly the typed record cell, a typed role label is missing, an
                as-of stamp is not the typed one, or STAGE_S.md does not print
                every cell's row exactly once.  SABOTAGE (copies): a dropped
                cell; an undeclared cell; a duplicated cell; the collar removed
                on one row; the record row under the Tier-E collar; a verdict
                column added; one would_read flipped; one
                ratio_median moved 1e-9; one clause flag flipped; the maker-twin
                role blanked; the record flag moved to the maker row; an as-of
                stamp changed.
  F-KEY         FAILS IF S_R2_1H.parquet's column list / dtypes are not the typed
                ones, its cell key or (panel, lens, era, scale_kind, toll) repeats,
                a typed-required column holds a null, the manifest's key / row
                count / content sha / file shas are not the table's and the
                files', STATUS.json or S_GATE.json lacks a typed field or carries
                it with the wrong type or null, the status word is not one of the
                three, or regbooks/P-SCALP-2 holds anything but STATUS.json (a
                CLOSED registration holds no arm).  SABOTAGE (copies): a
                duplicated row; a nulled would_read; as_of_last_closed_4h
                dropped; the manifest content sha altered; STATUS.json without
                its reason; STATUS.arms a string; a stray scored.parquet beside
                STATUS.json; the module dropping `role` from its column list.
  F-DET         FAILS IF two subprocess builds (PYTHONHASHSEED 1, 20260924) —
                written under RUN_ROOT/_det_stage_s (--root redirects them) —
                differ from each other or from the files of record (stage_s/ +
                regbooks/P-SCALP-2/STATUS.json) in the file set, any file's bytes
                or any parquet's content sha, or either exits nonzero.  Each
                comparison is labelled by what it compares.  SABOTAGE:
                one byte bent in a copy of STAGE_S.md; a parquet copy with one
                float moved; a hash-order-dependent line emitted under the two
                seeds.
BANNED: self-comparison; one example where cardinality was possible; a tuned
magnitude bound standing in for an identity; a check whose claim is not the
design's claim.  FROZEN SUBSTRATE: HALTs unless NAIAD_CACHE_DIR is the TC11
snapshot (tierc11_env's guard).  Seed 20260924.  The transcript carries no clock,
no temp path and no run-root path (the scratch area prints as <RUN_ROOT>/_det_stage_s).  Parquet is read by path string only [AM-2].

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_s.py            # the build first
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_s_fixtures.py \\
          [leg-substring ...] [--refile-transcript] [--root=DIR]
      --root=DIR redirects the transcript AND the scratch / F-DET runs
      (DIR/_det_stage_s/); the files judged as filed are always the record.
Exit 0 = every leg GREEN, every break RED · 1 = a RED or VOID fixture, a
transcript finding, or a HALT.
"""
from __future__ import annotations

import contextlib
import copy
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_stage_s as S                                          # noqa: E402  (guards first)

import pandas as pd                                                  # noqa: E402

E = S.E
TP = E.TP

# ── FIXTURE-TYPED LITERALS: the commission, a second object, never S's own ──
TC11_SNAP = Path.home() / ".cache" / "naiad" / "snapshots" / "tc11_20260925"
PIN = 1790294400000                      # 2026-09-25T00:00:00Z [L-0.1]
SEED = 20260924
DET_SEEDS = (1, SEED)
AS_OF_LINE = "as_of_last_closed_4h: 2026-09-25T00:00:00Z"
REG = "P-SCALP-2"
REG_PAYLOAD_SHA_TYPED = "c4e7ea0064bf0355804f311b8a2c91af1178de0ac9e705a417a1cc09b90bd250"
TC11 = ROOT / "research_outputs" / "tierc11"
R2_JSON = TC11 / "stage_r" / "R2_LENS_VERDICTS.json"
R2_FEAS = TC11 / "stage_r" / "R2_FEASIBILITY.parquet"
R2_MAN = TC11 / "stage_r" / "build_manifest.json"
R2_JSON_REL = "research_outputs/tierc11/stage_r/R2_LENS_VERDICTS.json"
OUT = TC11 / "stage_s"
REG_DIR = TC11 / "regbooks" / REG
# THE [Q-R3] LAW [L-R.4], typed here
N_RANGES_MIN, RATIO_MIN, SHARE_MAX, EDGE_NR_MIN, EDGE_N_MIN, NET_GT = 30, 3.0, 0.10, 30, 30, 0.0
ND = 8
PASS, FAIL, PROV = "PASS", "FAIL", "FAIL (provisional, n<30)"
REOPEN_TYPED = ("FAIL — maker twin PASSES (the reopening path; needs a toll-model change the "
                "operator rules)")
POOL = "POOLED:CLASSIC5"
RECORD_ROW_TYPED = {"pool": POOL, "era": "holdout", "scale": "calibrated", "toll": "taker"}
RECORD_BLOCK_TYPED = {"panel": POOL, "era": "holdout", "scale_kind": "calibrated",
                      "toll": "taker"}
STATUS_WORDS_TYPED = ("BUILT", "CLOSED_BY_PRECONDITION", "CONDITION_NOT_MET")
REASON_FMT = "CLOSED BY R2 (1h: {verdict})"
COLLAR_TYPED = {"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
                "gates": "nothing"}
# L-1.4: "every R2 row except the lens verdict of record" — the record row carries Stage
# R's record collar (its build_manifest's `record_collar`), typed here
RECORD_COLLAR_TYPED = {
    "tier": "R2 LENS VERDICT OF RECORD [L-R.4]",
    "selection_not_a_result": "n/a — the lens verdict of record, not a selection",
    "gates": ("range trading on this lens in this and every later tier unless the toll model "
              "changes [contract R2]; at 1h also Stage S [L-S.1]")}
CLASSIC5_MEMBERS_TYPED = "BTCUSDT,ETHUSDT,SOLUSDT,NEARUSDT,ZECUSDT"
# the JSON 1h row field -> R2_FEASIBILITY record-row column pairs the cross-file check
# must compare (SS-5), typed here: every pair gets its own plant
JSON_PARQUET_TYPED = (
    ("n_ranges", "n_ranges"), ("ratio_median", "ratio_median"),
    ("share_ratio_lt_1", "share_ratio_lt_1"), ("edge_n", "edge_n"),
    ("edge_n_ranges", "edge_n_ranges"), ("edge_median_term_h20", "edge_median_term_h20"),
    ("edge_toll_atr", "edge_toll_atr"), ("edge_net_h20", "edge_net_h20"),
    ("members", "members"), ("pick_window", "pick_window"),
    ("scale_in_sample", "scale_in_sample"), ("fallback_members", "fallback_members"),
    ("stability_changed_members", "stability_changed_members"),
    ("toll_bps_rt", "toll_bps_rt_max"), ("word", "word"), ("verdict", "verdict"),
    ("provisional", "under_floor"), ("pool", "panel"), ("era", "era"),
    ("scale", "scale_kind"), ("toll", "toll"))
# a PASS at the law's inclusive boundaries (30 / 3.0 / 0.10 / 30 / 30 / net 1e-8)
BOUNDARY = {"n_ranges": 30, "ratio_median": 3.0, "share_ratio_lt_1": 0.10, "edge_n_ranges": 30,
            "edge_n": 30, "edge_median_term_h20": 0.16760526, "edge_toll_atr": 0.16760525,
            "edge_net_h20": round(round(0.16760526, 8) - round(0.16760525, 8), 8)}
VERDICT_COLUMNS_TYPED = ("verdict", "word", "verdict_of_record", "clears_bh_bar", "promotable",
                         "scored_in_family", "p_one_sided", "is_the_registered_cell")
FILES_TYPED = ("STAGE_S.md", "S_GATE.json", "S_R2_1H.parquet", "build_manifest.json")
REG_FILE = "regbooks/P-SCALP-2/STATUS.json"
PANELS_TYPED = (POOL, "ASSET:BTCUSDT", "ASSET:ETHUSDT", "ASSET:SOLUSDT", "ASSET:NEARUSDT",
                "ASSET:ZECUSDT")
ERAS_TYPED = ("ALL", "tuning", "holdout")
SCALES_TYPED = ("calibrated", "frozen3.0")
TOLLS_TYPED = ("taker", "maker", "charter")
DECLARED_CELLS = ["|".join((p, "1h", e, s, t)) for p in PANELS_TYPED for e in ERAS_TYPED
                  for s in SCALES_TYPED for t in TOLLS_TYPED]
RECORD_CELL = f"{POOL}|1h|holdout|calibrated|taker"
ROLE_TYPED = {RECORD_CELL: "verdict of record",
              f"{POOL}|1h|holdout|calibrated|maker": "reopening path",
              f"{POOL}|1h|holdout|calibrated|charter": "charter twin",
              f"{POOL}|1h|tuning|calibrated|taker": "tuning-era word",
              f"{POOL}|1h|ALL|calibrated|taker": "ALL-era word"}
ROLE_OTHER_TYPED = "a twin of the block (Tier-E)"
AS_OF_TYPED = {"as_of_last_closed_4h": "2026-09-25T00:00:00Z", "as_of_substrate": "tc11_20260925"}
INT_COLS = ("n_ranges", "edge_n", "edge_n_ranges")
FLOAT_COLS = ("ratio_median", "share_ratio_lt_1", "edge_median_term_h20", "edge_toll_atr",
              "edge_net_h20", "toll_bps_rt_min", "toll_bps_rt_max", "net_rederived")
BOOL_COLS = ("is_lens_verdict_of_record", "net_identity_holds", "height_n_ranges_ok",
             "height_ratio_ok", "height_share_ok", "height_leg_holds", "edge_n_ranges_ok",
             "edge_n_ok", "edge_net_ok", "edge_leg_holds", "under_floor", "agrees_with_r2")
CLAUSE_COLS = ("height_n_ranges_ok", "height_ratio_ok", "height_share_ok", "height_leg_holds",
               "edge_n_ranges_ok", "edge_n_ok", "edge_net_ok", "edge_leg_holds", "under_floor",
               "net_identity_holds")
VALUE_COLS = ("n_ranges", "ratio_median", "share_ratio_lt_1", "edge_n", "edge_n_ranges",
              "edge_median_term_h20", "edge_toll_atr", "edge_net_h20", "toll_bps_rt_min",
              "toll_bps_rt_max", "pick_window", "scale_in_sample", "stability_changed_members",
              "tier", "selection_not_a_result", "gates")
COLUMNS_TYPED = (
    "cell", "panel", "lens", "era", "scale_kind", "toll", "role",
    "is_lens_verdict_of_record",
    "n_ranges", "ratio_median", "share_ratio_lt_1",
    "edge_n", "edge_n_ranges", "edge_median_term_h20", "edge_toll_atr", "edge_net_h20",
    "toll_bps_rt_min", "toll_bps_rt_max",
    "net_rederived", "net_identity_holds",
    "height_n_ranges_ok", "height_ratio_ok", "height_share_ok", "height_leg_holds",
    "edge_n_ranges_ok", "edge_n_ok", "edge_net_ok", "edge_leg_holds",
    "under_floor", "would_read", "r2_printed_word", "agrees_with_r2",
    "pick_window", "scale_in_sample", "stability_changed_members",
    "tier", "selection_not_a_result", "gates",
    "as_of_last_closed_4h", "as_of_substrate")
STATUS_TYPED = {"registration": str, "status": str, "reason": str, "arms": list,
                "r2_row": dict, "r2_source": dict, "maker_twin_word": str,
                "reopening_path": str, "tier_e_beside": dict, "precondition": str,
                "precondition_word": str, "rederived_taker_word": str, "as_of": str,
                "seed": int, "source_script": str}
GATE_TYPED = {"registration": str, "lens": str, "record": dict, "r2_row": dict,
              "rederivation": dict, "verdict_of_record": str, "gate": str, "reason": str,
              "maker_twin": dict, "charter_twin": dict, "beside_tier_e": dict, "source": dict,
              "stage_stops": str, "as_of": str}
PASS_MEDIAN = 0.25                       # a median H20 term that clears every 1h toll here

DET_ROOT = S.DET_ROOT
RUN_ROOT = OUT
TRANSCRIPT = "FIXTURES_STAGE_S.txt"
PY = sys.executable
LINES: list[str] = []
PASSED: list[str] = []
FAILED: list[str] = []
_TMP_RX = re.compile(r"(/private)?/(var/folders|tmp)/[^\s'\"]+")


def _norm(line: str) -> str:
    """The scratch area first (it moves with --root), then temp paths, then the repo —
    applied BEFORE any truncation, so a printed finding never depends on the root."""
    line = line.replace(str(det_dir()), f"<RUN_ROOT>/{DET_ROOT.name}")
    return _TMP_RX.sub("<tmp>", line).replace(str(ROOT), "<ROOT>")


def say(line: str = "") -> None:            # deterministic -> transcript
    line = _norm(line)
    print(line)
    LINES.append(line)


def clock(line: str) -> None:               # wall clock, temp paths -> stdout ONLY
    print(f"  [clock · stdout only] {line}")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def csv_sha(df: pd.DataFrame) -> str:       # the lineage's content-sha law, typed here
    return hashlib.sha256(df.to_csv(index=False).encode("utf-8")).hexdigest()


def prove(fid: str, title: str, fails_if: str, break_leg, real_leg) -> None:
    """Break first; it must go RED (ok False) or the fixture is VOID."""
    say(f"\n{fid} — {title}")
    say(f"  FAILS IF: {fails_if}")
    try:
        b_ok, b_why = break_leg()
    except BaseException as e:              # a break leg that errors proved nothing
        if isinstance(e, KeyboardInterrupt):
            raise
        b_ok, b_why = True, f"break leg RAISED {type(e).__name__}: {e}"
    say(f"  [BREAK] deliberate violation -> "
        f"{'RED (correct)' if not b_ok else 'GREEN (FIXTURE IS VOID)'}: {b_why}")
    try:
        r_ok, r_why = real_leg()
    except SystemExit as e:                 # a HALT in the real leg is a FAIL
        r_ok, r_why = False, f"HALT {e}"
    except Exception as e:                  # a real leg that errors is a FAIL
        r_ok, r_why = False, f"raised {type(e).__name__}: {e}"
    say(f"  [{'PASS' if r_ok else 'FAIL'}] {fid}: {r_why}")
    if b_ok:
        FAILED.append(f"{fid} (break leg did not go RED — fixture proves nothing)")
    elif not r_ok:
        FAILED.append(fid)
    else:
        PASSED.append(fid)


def plants(rows) -> tuple[bool, str]:
    """rows = (name, expected detector substring, thunk -> list of findings).
    Judged ONE AT A TIME.  CAUGHT only if a finding names the intended detector.
    No finding = the plant PASSED (VOID); a finding without the substring = the
    WRONG detector (VOID); a crash = a FIXTURE DEFECT (VOID).  A SystemExit (a
    module HALT) is a finding."""
    passed, wrong, caught, crashed = [], [], [], []
    for name, want, thunk in rows:
        try:
            found = [_norm(str(x)) for x in thunk()]
        except SystemExit as e:
            found = [_norm(f"HALT: {e}")]
        except Exception as e:
            crashed.append(_norm(f"{name} -> RAISED {type(e).__name__}: {e}"))
            continue
        if not found:
            passed.append(name)
        elif not any(want in str(f) for f in found):
            wrong.append(f"{name} -> {str(found[0])[:160]} (wanted {want!r})")
        else:
            hit = next(str(f) for f in found if want in str(f))
            i = hit.index(want)
            shown = hit[:150] if i + len(want) <= 150 else (hit[:40] + " … " + hit[i:i + 110])
            caught.append(f"{name} -> {shown}")
    if crashed:
        return True, (f"{len(crashed)} plant(s) CRASHED — a FIXTURE DEFECT, not a "
                      f"finding: " + " · ".join(crashed))
    if passed or wrong:
        return True, (f"{len(passed)} plant(s) PASSED {passed}; {len(wrong)} caught by the "
                      f"WRONG detector {wrong}")
    return False, (f"all {len(caught)} plants caught by their named detector, one at a "
                   f"time: " + " · ".join(caught))


@contextlib.contextmanager
def mutated(obj, name: str, value):
    """A MUTATION of the module under trial, restored in `finally`."""
    old = getattr(obj, name)
    setattr(obj, name, value)
    try:
        yield
    finally:
        setattr(obj, name, old)


def _env() -> dict:
    return dict(os.environ, NAIAD_CACHE_DIR=str(TC11_SNAP), PYTHONDONTWRITEBYTECODE="1")


def det_dir() -> Path:
    """Scratch and F-DET runs live under RUN_ROOT (--root redirects them) [H §8]."""
    return RUN_ROOT / DET_ROOT.name


# ═══════════════════════════════════════════════ THE FIXTURE'S OWN READING
def _i(x) -> int:
    return int(x)


def _f(x) -> float:
    return float("nan") if x is None or (not isinstance(x, (int, float)) and pd.isna(x)) \
        else float(x)


def fx_word(r) -> tuple[str, dict]:
    """The [Q-R3] law on one row's printed columns, by THIS file's code."""
    nr, en, enr = _i(r["n_ranges"]), _i(r["edge_n"]), _i(r["edge_n_ranges"])
    ratio, share = _f(r["ratio_median"]), _f(r["share_ratio_lt_1"])
    m, t, net = _f(r["edge_median_term_h20"]), _f(r["edge_toll_atr"]), _f(r["edge_net_h20"])
    fin = math.isfinite
    net_re = round(round(m, ND) - round(t, ND), ND) if fin(m) and fin(t) else float("nan")
    ident = (net_re == net) if fin(net_re) else not fin(net)
    cl = {"height_n_ranges_ok": nr >= N_RANGES_MIN,
          "height_ratio_ok": fin(ratio) and ratio >= RATIO_MIN,
          "height_share_ok": fin(share) and share <= SHARE_MAX,
          "edge_n_ranges_ok": enr >= EDGE_NR_MIN,
          "edge_n_ok": en >= EDGE_N_MIN,
          "edge_net_ok": fin(net) and net > NET_GT}
    cl["height_leg_holds"] = cl["height_n_ranges_ok"] and cl["height_ratio_ok"] \
        and cl["height_share_ok"]
    cl["edge_leg_holds"] = cl["edge_n_ranges_ok"] and cl["edge_n_ok"] and cl["edge_net_ok"]
    under = nr < N_RANGES_MIN or enr < EDGE_NR_MIN or en < EDGE_N_MIN
    cl["under_floor"] = under
    cl["net_identity_holds"] = ident
    w = PASS if (cl["height_leg_holds"] and cl["edge_leg_holds"]) else (PROV if under else FAIL)
    return w, {**cl, "net_re": net_re, "ident": ident, "under": under}


def fx_verdict(taker: str, maker: str) -> str:
    return PASS if taker == PASS else (REOPEN_TYPED if maker == PASS else taker)


def fx_row(feas: pd.DataFrame, panel: str, era: str, scale: str, toll: str) -> pd.Series:
    z = feas[(feas["panel"] == panel) & (feas["lens"] == "1h") & (feas["era"] == era)
             & (feas["scale_kind"] == scale) & (feas["toll"] == toll)]
    if len(z) != 1:
        raise RuntimeError(f"fixture: {len(z)} R2 rows for {panel}|1h|{era}|{scale}|{toll}")
    return z.iloc[0]


def fx_printed(r: pd.Series):
    return r["word"] if bool(r["is_lens_verdict_of_record"]) else r["would_read"]


def fx_fmt(x) -> str:
    if isinstance(x, bool):
        return "True" if x else "False"
    if isinstance(x, int):
        return str(x)
    if isinstance(x, float):
        return "nan" if math.isnan(x) else repr(x)
    if x is None:
        return "null"
    return str(x).replace("|", "\\|")


def real_r2() -> dict:
    return json.loads(R2_JSON.read_text(encoding="utf-8"))


def real_feas() -> pd.DataFrame:
    return pd.read_parquet(str(R2_FEAS))


def real_man() -> dict:
    return json.loads(R2_MAN.read_text(encoding="utf-8"))


def _idx(feas: pd.DataFrame, panel: str, era: str, scale: str, toll: str):
    z = feas.index[(feas["panel"] == panel) & (feas["lens"] == "1h") & (feas["era"] == era)
                   & (feas["scale_kind"] == scale) & (feas["toll"] == toll)]
    assert len(z) == 1
    return z[0]


def lift(feas: pd.DataFrame, i, median: float) -> None:
    """Set a feasibility row's median H20 term and its printed net by the census's
    printed arithmetic (so the plant is ONLY the named change)."""
    feas.loc[i, "edge_median_term_h20"] = median
    feas.loc[i, "edge_net_h20"] = round(round(median, ND)
                                        - round(float(feas.loc[i, "edge_toll_atr"]), ND), ND)


def plant_files(name: str, r2: dict | None = None, feas: pd.DataFrame | None = None,
                man: dict | None = None, vouch: bool = True) -> tuple[Path, Path, Path]:
    """Planted inputs under the scratch root.  With vouch, the planted manifest
    carries the planted parquet's content sha (read back by path) — so the plant
    is only the change it names."""
    d = det_dir() / f"in_{name}"
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    rj, fp, mp = R2_JSON, R2_FEAS, R2_MAN
    if r2 is not None:
        rj = d / "R2_LENS_VERDICTS.json"
        rj.write_text(json.dumps(r2, indent=1, sort_keys=True, ensure_ascii=False),
                      encoding="utf-8")
    if feas is not None:
        fp = d / "R2_FEASIBILITY.parquet"
        feas.to_parquet(str(fp), index=False)
        if vouch:
            man = copy.deepcopy(man if man is not None else real_man())
            man["sha"]["R2_FEASIBILITY"] = csv_sha(pd.read_parquet(str(fp)))
    if man is not None:
        mp = d / "build_manifest.json"
        mp.write_text(json.dumps(man, indent=1, sort_keys=True, ensure_ascii=False),
                      encoding="utf-8")
    return rj, fp, mp


def _files_under(d: Path) -> set:
    return {str(p.relative_to(d)) for p in d.rglob("*") if p.is_file()} if d.exists() else set()


def gate_run(name: str, rj: Path = R2_JSON, fp: Path = R2_FEAS, mp: Path = R2_MAN,
             pre=None) -> list[str]:
    """The module's build into a scratch run dir.  A HALT is a finding (and a HALT
    that left a file behind is a second one); a build that filed is judged by the
    fixture's own reading of the inputs it was given (filed_findings)."""
    out = det_dir() / f"run_{name}"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    if pre:
        pre(out)
    before = _files_under(out)
    try:
        S.build(out, rj, fp, mp)
    except SystemExit as e:
        f = [str(e)]
        extra = sorted(_files_under(out) - before)
        if extra:
            f.append(f"WROTE-ON-HALT: {extra}")
        return f
    return filed_findings(out, out / "regbooks" / REG, rj, fp)


def filed_findings(stage_dir: Path, reg_dir: Path, rj: Path, fp: Path) -> list[str]:
    """THE CLAIM: what the module filed is exactly the CLOSED record the fixture
    derives from the verdicts file and the feasibility parquet it was given."""
    f = []
    raw = Path(rj).read_bytes()
    v = json.loads(raw.decode("utf-8"))["lenses"]["1h"]
    feas = pd.read_parquet(str(fp))
    tw, ti = fx_word(v)
    mw, _ = fx_word(fx_row(feas, POOL, "holdout", "calibrated", "maker"))
    cw, _ = fx_word(fx_row(feas, POOL, "holdout", "calibrated", "charter"))
    uw, _ = fx_word(fx_row(feas, POOL, "tuning", "calibrated", "taker"))
    aw, _ = fx_word(fx_row(feas, POOL, "ALL", "calibrated", "taker"))
    verdict = fx_verdict(tw, mw)
    reason = REASON_FMT.format(verdict=verdict)
    if not ti["ident"]:
        f.append(f"NET-ARITH (fixture): printed net {v.get('edge_net_h20')!r} != "
                 f"{ti['net_re']!r}")
    for fld, want in (("word", tw), ("verdict", verdict), ("maker_twin", mw),
                      ("charter_twin", cw), ("tier_e_tuning_word", uw),
                      ("tier_e_all_word", aw), ("provisional", ti["under"])):
        if v.get(fld) != want:
            f.append(f"LABEL-LAW (fixture): printed {fld} {v.get(fld)!r} != the fixture's "
                     f"reading {want!r}")
    if {k: v.get(k) for k in RECORD_ROW_TYPED} != RECORD_ROW_TYPED:
        f.append("RECORD-SPEC (fixture): the 1h row is not the verdict of record")
    if verdict == PASS:
        f.append("CLOSED-ON-PASS: the fixture reads the 1h verdict of record PASS, yet the "
                 "module filed a CLOSED record [L-S.1]")
    sp = reg_dir / "STATUS.json"
    if not sp.exists():
        return f + [f"STATUS: {REG}/STATUS.json absent"]
    st = json.loads(sp.read_text(encoding="utf-8"))
    exp = {"registration": REG, "status": "CLOSED_BY_PRECONDITION", "reason": reason,
           "arms": [], "maker_twin_word": mw, "precondition_word": verdict,
           "rederived_taker_word": tw}
    for k, want in exp.items():
        if st.get(k) != want:
            f.append(f"STATUS: {k} {st.get(k)!r} != the fixture's {want!r}")
    if st.get("r2_row") != v:
        f.append("STATUS: r2_row is not the 1h R2 row whole")
    if st.get("r2_source") != {"path": R2_JSON_REL, "sha256": sha_bytes(raw)}:
        f.append(f"STATUS: r2_source {st.get('r2_source')!r} is not the verdicts file on disk")
    tb = st.get("tier_e_beside") or {}
    if tb.get("tuning_era_word") != uw or any(tb.get(k) != x for k, x in COLLAR_TYPED.items()):
        f.append(f"STATUS: the tuning-era word beside {tb.get('tuning_era_word')!r} / its "
                 f"collar is not the fixture's {uw!r} + {COLLAR_TYPED}")
    if str(st.get("reopening_path", "")).startswith("none") != (mw != PASS):
        f.append(f"STATUS: reopening_path {str(st.get('reopening_path'))[:40]!r} vs maker "
                 f"twin {mw}")
    got = sorted(p.name for p in reg_dir.iterdir())
    if got != ["STATUS.json"]:
        f.append(f"REGBOOK-FILES: {REG}/ holds {got} — a CLOSED registration holds no arm")
    gp = stage_dir / "S_GATE.json"
    if not gp.exists():
        return f + ["GATE-RECORD: S_GATE.json absent"]
    g = json.loads(gp.read_text(encoding="utf-8"))
    for k, want in (("registration", REG), ("lens", "1h"), ("reason", reason),
                    ("verdict_of_record", verdict), ("gate", "CLOSED"),
                    ("record", RECORD_BLOCK_TYPED)):
        if g.get(k) != want:
            f.append(f"GATE-RECORD: {k} {g.get(k)!r} != {want!r}")
    if g.get("r2_row") != v:
        f.append("GATE-RECORD: r2_row is not the 1h R2 row whole")
    want_cl = [ti[k] for k in ("height_n_ranges_ok", "height_ratio_ok", "height_share_ok",
                               "edge_n_ranges_ok", "edge_n_ok", "edge_net_ok")]
    got_cl = [c.get("holds") for c in (g.get("rederivation") or {}).get("clauses", [])]
    if got_cl != want_cl:
        f.append(f"GATE-RECORD: clause truth values {got_cl} != the fixture's {want_cl}")
    if (g.get("maker_twin") or {}).get("word") != mw \
            or (g.get("beside_tier_e") or {}).get("tuning_era_word") != uw \
            or any((g.get("beside_tier_e") or {}).get(k) != x for k, x in COLLAR_TYPED.items()):
        f.append("GATE-RECORD: the maker-twin word / tuning-era word beside / collar differ")
    if ((g.get("source") or {}).get("r2_verdicts") or {}).get("sha256") != sha_bytes(raw):
        f.append("GATE-RECORD: source sha is not the verdicts file on disk")
    mdp = stage_dir / "STAGE_S.md"
    if not mdp.exists():
        return f + ["REPORT: STAGE_S.md absent"]
    md = mdp.read_text(encoding="utf-8")
    lines = md.splitlines()
    if not md.startswith(f"# TIER-C11 · STAGE S — THE SCALPER RETUNED: {reason}\n"):
        f.append("REPORT: the title does not state the verdict")
    # the JSON row's own table: from the §1 heading to the parquet row's paragraph
    h1 = next((i for i, x in enumerate(lines)
               if x.startswith("## 1 · The 1h R2 row of record, whole")), None)
    h2 = next((i for i, x in enumerate(lines) if h1 is not None and i > h1
               and x.startswith("The same row in ")), None)
    sec = [x for x in lines[h1:h2] if x.startswith("| ") and x != "| field | value |"] \
        if h1 is not None and h2 else []
    want_rows = [f"| {k} | {fx_fmt(v[k])} |" for k in sorted(v)]
    if sec != want_rows:
        miss = [k for k, w in zip(sorted(v), want_rows) if w not in sec]
        f.append(f"REPORT: the 1h R2 row is not printed whole in §1 ({len(sec)} rows vs "
                 f"{len(want_rows)} fields; missing {miss[:4]})")
    for needle, lab in (("Stage S STOPS [L-S.1]: no scalper book", "the stop"),
                        (f"**The maker-twin word (the reopening path):** {mw}.",
                         "the maker-twin word"),
                        (f"the tuning-era R2 1h word {uw} (holdout word of record {verdict})",
                         "the tuning-era word beside")):
        if needle not in md:
            f.append(f"REPORT: {lab} not printed")
    books = sorted(p.name for p in stage_dir.iterdir()
                   if p.is_file() and p.suffix == ".parquet" and p.name != "S_R2_1H.parquet")
    if books:
        f.append(f"REGBOOK-FILES: a book-like parquet in the stage dir {books}")
    return f


# ═══════════════════════════════════════════════════════════ F-SCALP-GATE
def with_1h(**kv) -> dict:
    r2 = real_r2()
    r2["lenses"]["1h"].update(kv)
    return r2


def pass_row(v: dict) -> dict:
    r = dict(v)
    r["edge_median_term_h20"] = PASS_MEDIAN
    r["edge_net_h20"] = round(round(PASS_MEDIAN, ND) - round(float(r["edge_toll_atr"]), ND), ND)
    r.update(word=PASS, verdict=PASS, maker_twin=PASS, provisional=False)
    return r


def with_pass(**kv) -> dict:
    r2 = real_r2()
    r2["lenses"]["1h"] = pass_row(r2["lenses"]["1h"])
    r2["lenses"]["1h"].update(kv)
    return r2


def pass_set(name: str, over: dict | None = None,
             lift_parquet: bool = True) -> tuple[Path, Path, Path]:
    """A GENUINE, self-consistent PASS: the 1h record row and its maker twin lifted
    in the JSON, the parquet and the manifest together; `over` (JSON field ==
    parquet column) is applied to the JSON row AND the parquet record row.  With
    lift_parquet False the JSON and the manifest's 1h word read PASS while the
    parquet stays as filed (a PASS the parquet does not print)."""
    over = dict(over or {})
    r2 = with_pass(**over)
    feas = real_feas()
    ri = _idx(feas, POOL, "holdout", "calibrated", "taker")
    mi = _idx(feas, POOL, "holdout", "calibrated", "maker")
    if lift_parquet:
        lift(feas, ri, PASS_MEDIAN)
        lift(feas, mi, PASS_MEDIAN)
        for k, x in over.items():
            feas.loc[ri, k] = x
        feas.loc[ri, "word"] = PASS
        feas.loc[ri, "verdict"] = PASS
        feas.loc[mi, "would_read"] = PASS
    man = real_man()
    man["lens_verdicts"]["1h"] = PASS
    return plant_files(name, r2=r2, feas=feas if lift_parquet else None, man=man)


def _moved(col: str, x):
    """One record-row value moved, by its field class (typed here)."""
    if col in ("n_ranges", "edge_n", "edge_n_ranges"):
        return int(x) + 1
    if col in ("ratio_median", "share_ratio_lt_1", "edge_median_term_h20", "edge_toll_atr",
               "edge_net_h20", "toll_bps_rt_max"):
        return float(x) + 1e-9                  # exactness, not a tolerance
    if col == "under_floor":
        return not bool(x)
    if col in ("word", "verdict"):
        return PASS
    return {"members": "BTCUSDT,ETHUSDT,SOLUSDT,NEARUSDT", "fallback_members": "ZECUSDT",
            "panel": "POOLED:PANEL17", "era": "tuning", "scale_kind": "frozen3.0",
            "toll": "maker"}.get(col, f"{x} (planted)")


def feas_plant(name: str, edit, vouch: bool = True, man: dict | None = None):
    feas = real_feas()
    edit(feas)
    return plant_files(name, feas=feas, man=man, vouch=vouch)


def gate_break():
    def js(name, r2):
        return lambda: gate_run(name, *plant_files(name, r2=r2))

    def net_off_1e8():
        v = real_r2()["lenses"]["1h"]
        return with_1h(edge_net_h20=round(float(v["edge_net_h20"]) + 1e-8, ND))

    def rec_block():
        r2 = real_r2()
        r2["record"] = dict(r2["record"], era="tuning")
        return r2

    def no_1h():
        r2 = real_r2()
        del r2["lenses"]["1h"]
        return r2

    def rec_moved(feas):
        lift(feas, _idx(feas, POOL, "holdout", "calibrated", "taker"), 0.01)

    def maker_up(feas):
        i = _idx(feas, POOL, "holdout", "calibrated", "maker")
        lift(feas, i, PASS_MEDIAN)
        feas.loc[i, "would_read"] = PASS

    def tuning_up(feas):
        i = _idx(feas, POOL, "tuning", "calibrated", "taker")
        lift(feas, i, PASS_MEDIAN)
        feas.loc[i, "would_read"] = PASS

    def charter_up(feas):
        i = _idx(feas, POOL, "holdout", "calibrated", "charter")
        lift(feas, i, PASS_MEDIAN)
        feas.loc[i, "would_read"] = PASS

    def all_up(feas):
        i = _idx(feas, POOL, "ALL", "calibrated", "taker")
        lift(feas, i, PASS_MEDIAN)
        feas.loc[i, "would_read"] = PASS

    def second_flag(feas):
        feas.loc[_idx(feas, "POOLED:PANEL17", "holdout", "calibrated", "taker"),
                 "is_lens_verdict_of_record"] = True

    def rec_tier_e(feas):
        i = _idx(feas, POOL, "holdout", "calibrated", "taker")
        for k, x in COLLAR_TYPED.items():
            feas.loc[i, k] = x

    def tier_e_rec(feas):
        i = _idx(feas, "ASSET:BTCUSDT", "holdout", "calibrated", "taker")
        for k, x in RECORD_COLLAR_TYPED.items():
            feas.loc[i, k] = x

    def field_moved(pcol):
        def edit(feas):
            i = _idx(feas, POOL, "holdout", "calibrated", "taker")
            feas.loc[i, pcol] = _moved(pcol, feas.loc[i, pcol])
        return edit

    def flip_block(feas):
        i = _idx(feas, POOL, "ALL", "frozen3.0", "taker")
        feas.loc[i, "would_read"] = PASS if feas.loc[i, "would_read"] == FAIL else FAIL

    def unrelated(feas):
        i = _idx(feas, "ASSET:ZECUSDT", "ALL", "calibrated", "charter")
        feas.loc[i, "ratio_d1"] = float(feas.loc[i, "ratio_d1"]) + 1e-6

    def man_pass():
        m = real_man()
        m["lens_verdicts"]["1h"] = PASS
        return m

    def stuck_open():
        with mutated(S, "gate_opens", lambda verdict: True):
            return gate_run("mut_open")

    def stuck_closed():
        paths = pass_set("mut_closed")
        with mutated(S, "gate_opens", lambda verdict: False):
            return gate_run("mut_closed", *paths)

    def loose_law():
        with mutated(S, "LAW", dict(S.LAW, edge_net_gt=-1.0)):
            return gate_run("mut_law")

    def no_reopen():
        paths = plant_files("mut_reopen", r2=with_1h(maker_twin=PASS, verdict=REOPEN_TYPED))
        with mutated(S, "record_verdict", lambda t, m: t):
            return gate_run("mut_reopen", *paths)

    def stray(out: Path):
        d = out / "regbooks" / REG
        d.mkdir(parents=True)
        (d / "scored.parquet").write_bytes(b"")

    def stray_json(out: Path):
        d = out / "regbooks" / REG
        d.mkdir(parents=True)
        (d / "scored.json").write_text("{}\n", encoding="utf-8")

    fields = [(f"the parquet's record row moved at {p} (JSON {j}; one field only, manifest "
               f"vouching)", "JSON-PARQUET",
               (lambda p=p: gate_run(f"jp_{p}", *feas_plant(f"jp_{p}", field_moved(p)))))
              for j, p in JSON_PARQUET_TYPED]
    return plants([
        ("the real 1h columns labelled PASS (word + verdict)", "LABEL-LAW",
         js("relabel", with_1h(word=PASS, verdict=PASS))),
        ("a passing row broken at n_ranges 29, labelled PASS", "LABEL-LAW",
         js("n29", with_pass(n_ranges=29))),
        ("a passing row broken at ratio_median 2.99999999, labelled PASS", "LABEL-LAW",
         js("ratio", with_pass(ratio_median=2.99999999))),
        ("a passing row broken at share_ratio_lt_1 0.10000001, labelled PASS", "LABEL-LAW",
         js("share", with_pass(share_ratio_lt_1=0.10000001))),
        ("a passing row broken at edge_n_ranges 29, labelled PASS", "LABEL-LAW",
         js("enr29", with_pass(edge_n_ranges=29))),
        ("a passing row broken at edge_n 29, labelled PASS", "LABEL-LAW",
         js("en29", with_pass(edge_n=29))),
        ("a passing row with net exactly 0 (median == toll), labelled PASS", "LABEL-LAW",
         js("net0", with_pass(edge_median_term_h20=0.16760525, edge_net_h20=0.0))),
        ("a printed net +0.01 that is not its parts' difference, labelled PASS", "NET-ARITH",
         js("arith", with_1h(edge_net_h20=0.01, word=PASS, verdict=PASS))),
        ("a printed net off by 1e-8 from its parts' difference (labels kept FAIL)",
         "NET-ARITH", js("arith8", net_off_1e8())),
        ("an under-floor row (n_ranges 29) labelled plain FAIL", "LABEL-LAW",
         js("floor", with_1h(n_ranges=29))),
        ("an under-floor row (edge_n_ranges 29, n_ranges and edge_n above 30) labelled plain "
         "FAIL", "LABEL-LAW", js("enrfloor", with_1h(edge_n_ranges=29))),
        ("a provisional flag that lies (True on a row above every floor)", "LABEL-LAW",
         js("prov", with_1h(provisional=True))),
        ("a maker-twin PASS printed without the reopening-path verdict", "LABEL-LAW",
         js("reopen", with_1h(maker_twin=PASS))),
        ("the 1h row's pool moved to POOLED:PANEL17", "RECORD-SPEC",
         js("pool", with_1h(pool="POOLED:PANEL17"))),
        ("the 1h row's era moved to tuning", "RECORD-SPEC", js("era", with_1h(era="tuning"))),
        ("the 1h row's scale moved to frozen3.0", "RECORD-SPEC",
         js("scale", with_1h(scale="frozen3.0"))),
        ("the 1h row's toll moved to maker", "RECORD-SPEC", js("toll", with_1h(toll="maker"))),
        ("the file's record block names the tuning era", "RECORD-SPEC",
         js("recblock", rec_block())),
        ("the 1h row pools four members (ZEC dropped)", "RECORD-SPEC",
         js("mem4", with_1h(members="BTCUSDT,ETHUSDT,SOLUSDT,NEARUSDT"))),
        ("the 1h row pools six members (SUI added)", "RECORD-SPEC",
         js("mem6", with_1h(members=CLASSIC5_MEMBERS_TYPED + ",SUIUSDT"))),
        ("the 1h row's fallback_members names a non-CLASSIC5 asset (SUI)", "RECORD-SPEC",
         js("fbsui", with_1h(fallback_members="SUIUSDT"))),
        ("no 1h lens in the verdicts file", "NO-1H", js("no1h", no_1h())),
        ("a GENUINE PASS set (JSON + parquet + manifest agree) — the gate must open",
         "GATE-OPEN", lambda: gate_run("pass", *pass_set("pass"))),
        ("a PASS at the law's inclusive boundaries (30 / 3.0 / 0.10 / 30 / 30 / net 1e-8), "
         "JSON + parquet + manifest agreeing — the gate must open", "GATE-OPEN",
         lambda: gate_run("boundary", *pass_set("boundary", over=BOUNDARY))),
        ("a PASS printed in the JSON only (parquet and manifest as filed) — must not open",
         "R2-MANIFEST", lambda: gate_run("jsonpass", *plant_files("jsonpass", r2=with_pass()))),
        ("a PASS printed in the JSON and the manifest, the parquet as filed — must not open",
         "JSON-PARQUET",
         lambda: gate_run("jsonmanpass", *pass_set("jsonmanpass", lift_parquet=False))),
        ("the parquet's record row moved (median +0.01), manifest vouching", "JSON-PARQUET",
         lambda: gate_run("recmoved", *feas_plant("recmoved", rec_moved))),
        *fields,
        ("a second 1h row flagged the lens verdict of record (POOLED:PANEL17 holdout "
         "calibrated taker)", "JSON-PARQUET",
         lambda: gate_run("secondflag", *feas_plant("secondflag", second_flag))),
        ("the parquet's maker row lifted to PASS, JSON maker_twin FAIL", "MAKER-TWIN",
         lambda: gate_run("makerup", *feas_plant("makerup", maker_up))),
        ("the parquet's charter row lifted to PASS, JSON charter_twin FAIL", "CHARTER-TWIN",
         lambda: gate_run("charterup", *feas_plant("charterup", charter_up))),
        ("the parquet's tuning row lifted to PASS, JSON tuning word FAIL", "TUNING-WORD",
         lambda: gate_run("tuningup", *feas_plant("tuningup", tuning_up))),
        ("the parquet's ALL-era row lifted to PASS, JSON ALL word FAIL", "ALL-WORD",
         lambda: gate_run("allup", *feas_plant("allup", all_up))),
        ("a block row's printed word flipped (POOLED ALL frozen3.0 taker)", "R2-ROW-WORD",
         lambda: gate_run("flip", *feas_plant("flip", flip_block))),
        ("the parquet's record row printed with the Tier-E collar", "R2-COLLAR",
         lambda: gate_run("rectiere", *feas_plant("rectiere", rec_tier_e))),
        ("a Tier-E row (BTC holdout calibrated taker) printed with the record collar",
         "R2-COLLAR", lambda: gate_run("tierereq", *feas_plant("tierereq", tier_e_rec))),
        ("a parquet the manifest does not vouch for (one ratio_d1 +1e-6)", "R2-MANIFEST",
         lambda: gate_run("unvouched", *feas_plant("unvouched", unrelated, vouch=False))),
        ("a manifest whose 1h lens word is PASS", "R2-MANIFEST",
         lambda: gate_run("manpass", *plant_files("manpass", man=man_pass()))),
        ("MUTATION: a gate stuck open, on the files of record", "GATE-OPEN", stuck_open),
        ("MUTATION: a gate stuck CLOSED, on the genuine PASS set", "CLOSED-ON-PASS",
         stuck_closed),
        ("MUTATION: the edge law read as net > -1, on the files of record", "LABEL-LAW",
         loose_law),
        ("MUTATION: the reopening clause removed, on a reopening-path label", "LABEL-LAW",
         no_reopen),
        ("a stray scored.parquet already in the regbook dir", "STRAY-BOOK",
         lambda: gate_run("stray", pre=stray)),
        ("a stray scored.json sidecar already in the regbook dir", "STRAY-BOOK",
         lambda: gate_run("strayjson", pre=stray_json)),
    ])


def gate_real():
    f_run = gate_run("real")
    f_rec = filed_findings(OUT, REG_DIR, R2_JSON, R2_FEAS)
    v = real_r2()["lenses"]["1h"]
    tw, ti = fx_word(v)
    feas = real_feas()
    mw, _ = fx_word(fx_row(feas, POOL, "holdout", "calibrated", "maker"))
    uw, _ = fx_word(fx_row(feas, POOL, "tuning", "calibrated", "taker"))
    verdict = fx_verdict(tw, mw)
    # SS-3 control: the reopening-path word keeps the gate closed (the module's gate on
    # a copy whose maker twin passes and whose verdict carries the reopening word)
    ro = with_1h(maker_twin=PASS, verdict=REOPEN_TYPED)
    g = S.gate(ro)
    ro_ok = (not g["open"]) and g["reason"] == REASON_FMT.format(verdict=REOPEN_TYPED)
    reg = json.loads((TC11 / "registrations" / "REGISTRATIONS.json").read_text(
        encoding="utf-8"))
    rp = next(x for x in reg["registrations"] if x["registration"] == REG)
    reg_ok = rp["sha256"] == REG_PAYLOAD_SHA_TYPED and S.REOPEN == REOPEN_TYPED
    ok = not f_run and not f_rec and ro_ok and reg_ok
    fails = [k for k in ("height_n_ranges_ok", "height_ratio_ok", "height_share_ok",
                         "edge_n_ranges_ok", "edge_n_ok", "edge_net_ok") if not ti[k]]
    return ok, (f"the fixture reads the 1h row of record (sha "
                f"{sha_bytes(R2_JSON.read_bytes())[:12]}…): taker {tw} (height leg "
                f"{'holds' if ti['height_leg_holds'] else 'fails'}, edge leg "
                f"{'holds' if ti['edge_leg_holds'] else 'fails'}; failing clauses {fails}; "
                f"net {v['edge_net_h20']!r} == round(round({v['edge_median_term_h20']!r},8) - "
                f"round({v['edge_toll_atr']!r},8),8): {ti['ident']}), maker twin {mw}, "
                f"verdict {verdict!r} == printed {v['verdict']!r}; tuning-era word beside "
                f"{uw}. The module's gate: CLOSED; a scratch build from the files of record "
                f"and the files of record both file exactly the fixture's CLOSED record "
                f"(STATUS {REASON_FMT.format(verdict=verdict)!r}, arms [], r2_row whole, maker "
                f"word, tuning word + collar, source sha; S_GATE clause values; STAGE_S.md "
                f"prints all {len(v)} fields; regbooks/{REG} = STATUS.json only): "
                f"{not f_run and not f_rec}; a reopening-path label keeps the gate CLOSED "
                f"(SS-3): {ro_ok}; registration payload sha and the module's reopening word "
                f"are the typed ones: {reg_ok}"
                + (f"; findings {(f_run + f_rec)[:4]}" if (f_run or f_rec) else ""))


# ═══════════════════════════════════════════════════════════════════ F-GRID
def grid_findings(T: pd.DataFrame, md: str) -> list[str]:
    f = []
    ok, lines = TP.grid_whole(DECLARED_CELLS, T, cell_col="cell",
                              require_cols=tuple(c for c in COLUMNS_TYPED if c in T.columns),
                              label="S_R2_1H")
    if not ok:
        f.append("GRID-WHOLE: " + " · ".join(x for x in lines if x.startswith("[BAD]")))
    for k in COLLAR_TYPED:                  # L-1.4: every row but the record row, typed
        if k not in T.columns:
            f.append(f"COLLAR: `{k}` absent")
            continue
        bad = [c for c, got in zip(T["cell"], T[k])
               if got != (RECORD_COLLAR_TYPED[k] if c == RECORD_CELL else COLLAR_TYPED[k])]
        if bad:
            f.append(f"COLLAR: `{k}` is not L-1.4's on {len(bad)} row(s) {bad[:2]} (the "
                     f"Tier-E collar on every row but the record row; Stage R's record collar "
                     f"on it)")
    vc = [c for c in VERDICT_COLUMNS_TYPED if c in T.columns]
    if vc:
        f.append(f"VERDICT-COLUMN: {vc}")
    for k, want in AS_OF_TYPED.items():
        if k not in T.columns or (T[k] != want).any():
            f.append(f"AS-OF: `{k}` is not {want!r} on every row")
    feas = real_feas()
    bad_v, bad_w, bad_c, bad_r = [], [], [], []
    for r in T.itertuples(index=False):
        c = r.cell.split("|")
        if len(c) != 5 or r.cell not in DECLARED_CELLS:
            continue
        q = fx_row(feas, c[0], c[2], c[3], c[4])
        for col in VALUE_COLS:
            a, b = getattr(r, col), q[col]
            same = (a == b) or (isinstance(a, float) and math.isnan(a) and pd.isna(b))
            if not same:
                bad_v.append(f"{r.cell}.{col}")
        w, info = fx_word(q)
        if r.would_read != w or r.r2_printed_word != fx_printed(q) \
                or bool(r.agrees_with_r2) != (w == fx_printed(q)):
            bad_w.append(r.cell)
        if any(bool(getattr(r, k)) != bool(info[k]) for k in CLAUSE_COLS) \
                or not (r.net_rederived == info["net_re"]
                        or (math.isnan(r.net_rederived) and math.isnan(info["net_re"]))):
            bad_c.append(r.cell)
        want_role = ROLE_TYPED.get(r.cell)
        if (want_role and want_role not in str(r.role)) or \
                (not want_role and r.role != ROLE_OTHER_TYPED):
            bad_r.append(r.cell)
    if bad_v:
        f.append(f"VALUE: {len(bad_v)} printed value(s) differ from R2_FEASIBILITY: "
                 f"{bad_v[:3]}")
    if bad_w:
        f.append(f"WORD: {len(bad_w)} row(s) whose would_read / R2 word / agreement differ "
                 f"from the fixture's reading: {bad_w[:3]}")
    if bad_c:
        f.append(f"CLAUSE: {len(bad_c)} row(s) whose clause flags / net_rederived differ: "
                 f"{bad_c[:3]}")
    if bad_r:
        f.append(f"ROLE: {len(bad_r)} row(s) whose role label is not the typed one: "
                 f"{bad_r[:3]}")
    flagged = sorted(T.loc[T["is_lens_verdict_of_record"].astype(bool), "cell"].tolist())
    if flagged != [RECORD_CELL]:
        f.append(f"RECORD-FLAG: flagged {flagged}, typed [{RECORD_CELL}]")
    md_lines = md.splitlines()
    unprinted = []
    for r in T.itertuples(index=False):
        pre = (f"| {'★' if r.cell == RECORD_CELL else ''} | {r.panel} | {r.era} | "
               f"{r.scale_kind} | {r.toll} | {r.n_ranges} | ")
        if sum(1 for x in md_lines if x.startswith(pre)) != 1:
            unprinted.append(r.cell)
    if unprinted:
        f.append(f"REPORT: {len(unprinted)} cell(s) not printed exactly once in STAGE_S.md: "
                 f"{unprinted[:3]}")
    return f


def _T() -> pd.DataFrame:
    return pd.read_parquet(str(OUT / "S_R2_1H.parquet"))


def _md() -> str:
    return (OUT / "STAGE_S.md").read_text(encoding="utf-8")


def grid_break():
    T, md = _T(), _md()

    def edit(fn):
        def run():
            d = T.copy()
            d = fn(d)
            return grid_findings(d, md)
        return run

    def drop(d):
        return d[d["cell"] != f"ASSET:NEARUSDT|1h|tuning|frozen3.0|charter"]

    def undeclared(d):
        x = d.iloc[[0]].copy()
        x["cell"] = x["cell"].str.replace("|1h|", "|5m|", regex=False)
        return pd.concat([d, x], ignore_index=True)

    def dup(d):
        return pd.concat([d, d.iloc[[5]]], ignore_index=True)

    def collar(d):
        d.loc[d.index[7], "tier"] = "TIER-A"
        return d

    def rec_collar(d):                      # the record row under the Tier-E collar (D1)
        for k, x in COLLAR_TYPED.items():
            d.loc[d["cell"] == RECORD_CELL, k] = x
        return d

    def verdict_col(d):
        d["verdict"] = d["would_read"]
        return d

    def flip(d):
        i = d.index[d["cell"] == f"ASSET:BTCUSDT|1h|ALL|calibrated|taker"][0]
        d.loc[i, "would_read"] = FAIL if d.loc[i, "would_read"] == PASS else PASS
        return d

    def value(d):
        i = d.index[d["cell"] == f"ASSET:ETHUSDT|1h|holdout|calibrated|maker"][0]
        d.loc[i, "ratio_median"] = float(d.loc[i, "ratio_median"]) + 1e-9
        return d

    def clause(d):
        i = d.index[d["cell"] == f"ASSET:SOLUSDT|1h|tuning|calibrated|taker"][0]
        d.loc[i, "edge_net_ok"] = not bool(d.loc[i, "edge_net_ok"])
        return d

    def role(d):
        d.loc[d["cell"] == f"{POOL}|1h|holdout|calibrated|maker", "role"] = ROLE_OTHER_TYPED
        return d

    def flag(d):
        d.loc[d["cell"] == RECORD_CELL, "is_lens_verdict_of_record"] = False
        d.loc[d["cell"] == f"{POOL}|1h|holdout|calibrated|maker",
              "is_lens_verdict_of_record"] = True
        return d

    def asof(d):
        d.loc[d.index[3], "as_of_last_closed_4h"] = "2026-09-21T16:00:00Z"
        return d

    return plants([
        ("a dropped cell (NEAR tuning frozen3.0 charter)", "GRID-WHOLE", edit(drop)),
        ("an undeclared cell (a 5m row)", "GRID-WHOLE", edit(undeclared)),
        ("a duplicated cell", "GRID-WHOLE", edit(dup)),
        ("the collar removed on one row (tier TIER-A)", "COLLAR", edit(collar)),
        ("the record row carrying the Tier-E collar (gates nothing)", "COLLAR",
         edit(rec_collar)),
        ("a verdict column added", "VERDICT-COLUMN", edit(verdict_col)),
        ("one would_read flipped (BTC ALL calibrated taker)", "WORD", edit(flip)),
        ("one ratio_median moved 1e-9 (ETH holdout calibrated maker)", "VALUE", edit(value)),
        ("one clause flag flipped (SOL tuning calibrated taker edge_net_ok)", "CLAUSE",
         edit(clause)),
        ("the maker-twin role blanked to the generic label", "ROLE", edit(role)),
        ("the record flag moved to the maker row", "RECORD-FLAG", edit(flag)),
        ("an as-of stamp moved to the TC10 pin on one row", "AS-OF", edit(asof)),
    ])


def grid_real():
    T, md = _T(), _md()
    f = grid_findings(T, md)
    ok, lines = TP.grid_whole(DECLARED_CELLS, T, cell_col="cell", require_cols=COLUMNS_TYPED,
                              label="S_R2_1H")
    cnt = T.groupby("would_read").size().to_dict()
    return (not f), (f"S_R2_1H.parquet: {len(T)} rows == the {len(DECLARED_CELLS)} declared "
                     f"cells ({len(PANELS_TYPED)} panels x {len(ERAS_TYPED)} eras x "
                     f"{len(SCALES_TYPED)} scales x {len(TOLLS_TYPED)} tolls); "
                     f"{lines[0][6:]}; all {len(COLUMNS_TYPED)} typed columns non-null; L-1.4's "
                     f"collar (Tier-E on {int((T['cell'] != RECORD_CELL).sum())} rows, Stage R's "
                     f"record collar on {RECORD_CELL}), no verdict column, as-of typed; every printed value == "
                     f"R2_FEASIBILITY's row for its cell; every clause flag, net_rederived and "
                     f"would_read == the fixture's reading (would_read "
                     + ", ".join(f"{k} {cnt[k]}" for k in sorted(cnt))
                     + f"); record flag on {RECORD_CELL} only; the 5 typed role labels; every "
                       f"cell printed once in STAGE_S.md"
                     + (f"; findings {f[:4]}" if f else ""))


# ═══════════════════════════════════════════════════════════════════ F-KEY
def key_findings(stage_dir: Path, reg_dir: Path, T: pd.DataFrame | None = None,
                 man: dict | None = None, st: dict | None = None) -> list[str]:
    f = []
    T = pd.read_parquet(str(stage_dir / "S_R2_1H.parquet")) if T is None else T
    man = json.loads((stage_dir / "build_manifest.json").read_text(encoding="utf-8")) \
        if man is None else man
    st = json.loads((reg_dir / "STATUS.json").read_text(encoding="utf-8")) if st is None else st
    if tuple(T.columns) != COLUMNS_TYPED:
        f.append(f"COLUMNS: {sorted(set(COLUMNS_TYPED) ^ set(T.columns))[:4]} / order differs "
                 f"from the typed commission")
    for c in INT_COLS:
        if c in T.columns and str(T[c].dtype) != "int64":
            f.append(f"COLUMNS: {c} dtype {T[c].dtype}")
    for c in FLOAT_COLS:
        if c in T.columns and str(T[c].dtype) != "float64":
            f.append(f"COLUMNS: {c} dtype {T[c].dtype}")
    for c in BOOL_COLS:
        if c in T.columns and str(T[c].dtype) != "bool":
            f.append(f"COLUMNS: {c} dtype {T[c].dtype}")
    if "cell" in T.columns and T["cell"].duplicated().any():
        f.append(f"KEY-DUP: {int(T['cell'].duplicated().sum())} duplicated cell key(s)")
    k5 = ["panel", "lens", "era", "scale_kind", "toll"]
    if all(c in T.columns for c in k5) and T.duplicated(k5).any():
        f.append("KEY-DUP: (panel, lens, era, scale_kind, toll) repeats")
    nulls = {c: int(T[c].isna().sum()) for c in COLUMNS_TYPED if c in T.columns
             and T[c].isna().any()}
    if nulls:
        f.append(f"NULL: required columns holding nulls {nulls}")
    if man.get("keys", {}).get("S_R2_1H") != ["cell"]:
        f.append(f"MANIFEST: key {man.get('keys', {}).get('S_R2_1H')!r}")
    if man.get("rows", {}).get("S_R2_1H") != len(T):
        f.append(f"MANIFEST: rows {man.get('rows', {}).get('S_R2_1H')!r} != {len(T)}")
    if man.get("sha", {}).get("S_R2_1H") != csv_sha(T):
        f.append("MANIFEST: content sha is not the table's")
    for name, p in (("S_GATE.json", stage_dir / "S_GATE.json"),
                    ("STAGE_S.md", stage_dir / "STAGE_S.md"),
                    (REG_FILE, reg_dir / "STATUS.json")):
        if man.get("files", {}).get(name) != sha_bytes(p.read_bytes()):
            f.append(f"MANIFEST: file sha of {name} is not the file's")
    if man.get("regbooks", {}).get("arms") != []:
        f.append("MANIFEST: regbooks.arms is not []")
    for k, typ in STATUS_TYPED.items():
        if k not in st or st[k] is None or not isinstance(st[k], typ) or \
                (typ is str and not st[k]):
            f.append(f"STATUS: field {k} absent / null / not {typ.__name__}")
    if st.get("status") not in STATUS_WORDS_TYPED:
        f.append(f"STATUS: word {st.get('status')!r}")
    if st.get("registration") != REG:
        f.append(f"STATUS: registration {st.get('registration')!r}")
    g = json.loads((stage_dir / "S_GATE.json").read_text(encoding="utf-8"))
    for k, typ in GATE_TYPED.items():
        if k not in g or g[k] is None or not isinstance(g[k], typ):
            f.append(f"GATE-RECORD: field {k} absent / null / not {typ.__name__}")
    files = sorted(p.name for p in reg_dir.iterdir())
    if files != ["STATUS.json"]:
        f.append(f"REGBOOK-FILES: {REG}/ holds {files} — a CLOSED registration holds no arm")
    return f


def key_break():
    T = pd.read_parquet(str(OUT / "S_R2_1H.parquet"))
    man = json.loads((OUT / "build_manifest.json").read_text(encoding="utf-8"))
    st = json.loads((REG_DIR / "STATUS.json").read_text(encoding="utf-8"))

    def dup():
        d = pd.concat([T, T.iloc[[9]]], ignore_index=True)
        m = copy.deepcopy(man)
        m["rows"]["S_R2_1H"] = len(d)
        m["sha"]["S_R2_1H"] = csv_sha(d)
        return key_findings(OUT, REG_DIR, T=d, man=m)

    def null():
        d = T.copy()
        d.loc[d.index[11], "would_read"] = None
        return key_findings(OUT, REG_DIR, T=d)

    def asof():
        return key_findings(OUT, REG_DIR, T=T.drop(columns=["as_of_last_closed_4h"]))

    def mansha():
        m = copy.deepcopy(man)
        m["sha"]["S_R2_1H"] = "0" * 64
        return key_findings(OUT, REG_DIR, man=m)

    def noreason():
        s = copy.deepcopy(st)
        del s["reason"]
        return key_findings(OUT, REG_DIR, st=s)

    def arms_str():
        s = copy.deepcopy(st)
        s["arms"] = "scored"
        return key_findings(OUT, REG_DIR, st=s)

    def stray():
        d = det_dir() / "key_stray" / "regbooks" / REG
        if d.parent.parent.exists():
            shutil.rmtree(d.parent.parent)
        d.mkdir(parents=True)
        shutil.copy2(REG_DIR / "STATUS.json", d / "STATUS.json")
        (d / "scored.parquet").write_bytes(b"")
        return key_findings(OUT, d)

    def module_drops_role():
        out = det_dir() / "key_mut"
        if out.exists():
            shutil.rmtree(out)
        with mutated(S, "BLOCK_COLUMNS", tuple(c for c in S.BLOCK_COLUMNS if c != "role")):
            S.build(out)
        return key_findings(out, out / "regbooks" / REG)

    return plants([
        ("a duplicated row (manifest re-struck to match)", "KEY-DUP", dup),
        ("a nulled would_read", "NULL", null),
        ("as_of_last_closed_4h dropped", "COLUMNS", asof),
        ("the manifest content sha altered", "MANIFEST", mansha),
        ("STATUS.json without its reason", "STATUS", noreason),
        ("STATUS.arms a string", "STATUS", arms_str),
        ("a stray scored.parquet beside STATUS.json (a copy of the regbook dir)",
         "REGBOOK-FILES", stray),
        ("MUTATION: the module drops `role` from its column list", "COLUMNS",
         module_drops_role),
    ])


def key_real():
    f = key_findings(OUT, REG_DIR)
    T = _T()
    st = json.loads((REG_DIR / "STATUS.json").read_text(encoding="utf-8"))
    return (not f), (f"S_R2_1H.parquet: the typed {len(COLUMNS_TYPED)} columns in order with "
                     f"typed dtypes; {len(T)} unique cell keys, (panel, lens, era, scale_kind, "
                     f"toll) unique; 0 nulls in the typed-required columns; manifest key "
                     f"['cell'], rows {len(T)}, content sha {csv_sha(T)[:12]}… and the three "
                     f"file shas match; STATUS.json: {len(STATUS_TYPED)} typed fields present, "
                     f"typed, non-null, status {st['status']!r} in the three words, arms "
                     f"{st['arms']!r}; S_GATE.json: {len(GATE_TYPED)} typed fields; "
                     f"regbooks/{REG} = [STATUS.json] only — no arm parquet exists to key"
                     + (f"; findings {f[:4]}" if f else ""))


# ═══════════════════════════════════════════════════════════════════ F-DET
def _files(d: Path) -> dict:
    """{published-relative path: Path} for a build dir; the canonical record is
    stage_s/<FILES_TYPED> + regbooks/P-SCALP-2/STATUS.json."""
    return {str(p.relative_to(d)): p for p in sorted(d.rglob("*")) if p.is_file()}


def _canon() -> dict:
    c = {n: OUT / n for n in FILES_TYPED if (OUT / n).exists()}
    if (REG_DIR / "STATUS.json").exists():
        c[REG_FILE] = REG_DIR / "STATUS.json"
    return c


def det_findings(a: tuple, b: tuple, canon: dict, la: str = "seed 1",
                 lb: str = f"seed {SEED}") -> list[str]:
    """a, b = (exit code, {path: Path}) labelled la / lb (the two seed builds, or the
    copies a plant compares); canon = the files of record."""
    out = []
    want = sorted(FILES_TYPED + (REG_FILE,))
    for lab, (rc, _) in ((la, a), (lb, b)):
        if rc != 0:
            out.append(f"{lab} exit {rc}")
    for lab, x in ((la, a[1]), (lb, b[1]), ("canonical", canon)):
        if sorted(x) != want:
            out.append(f"{lab}: file set {sorted(set(x) ^ set(want))} differs from typed")
    for lab, x, y in ((f"{la} vs {lb}", a[1], b[1]), (f"{la} vs canonical", a[1], canon)):
        for name in sorted(set(x) & set(y)):
            bx, by = x[name].read_bytes(), y[name].read_bytes()
            if bx != by:
                k = next((i for i in range(min(len(bx), len(by))) if bx[i] != by[i]),
                         min(len(bx), len(by)))
                out.append(f"{lab}: {name} bytes differ at byte {k}")
            if name.endswith(".parquet"):
                ca = csv_sha(pd.read_parquet(str(x[name])))
                cb = csv_sha(pd.read_parquet(str(y[name])))
                if ca != cb:
                    out.append(f"{lab}: {name} content sha {ca[:12]}… != {cb[:12]}…")
    return out


def det_build(d: Path, seed: int, hashorder: bool = False) -> tuple[int, dict]:
    if d.exists():
        shutil.rmtree(d)
    env = dict(_env(), PYTHONHASHSEED=str(seed))
    if not hashorder:
        cmd = [PY, "-B", str(ROOT / "scripts" / "tierc11_stage_s.py"), f"--out-dir={d}"]
    else:                                   # SABOTAGE twin: a set-order line appended
        code = (f"import sys\nsys.dont_write_bytecode = True\n"
                f"sys.path.insert(0, {str(ROOT)!r})\n"
                f"sys.path.insert(0, {str(ROOT / 'scripts')!r})\n"
                f"from pathlib import Path\nimport tierc11_stage_s as S\n"
                f"d = Path({str(d)!r})\nS.build(d)\n"
                f"p = d / 'STAGE_S.md'\n"
                f"p.write_text(p.read_text() + 'set order: ' + ','.join(set(S.E.PANEL17)) "
                f"+ '\\n')\n")
        cmd = [PY, "-B", "-c", code]
    r = subprocess.run(cmd, env=env, capture_output=True, text=True, cwd=str(ROOT),
                       timeout=1800)
    if r.returncode != 0:
        clock(f"det build {d.name} exit {r.returncode}: {r.stderr[-400:]}")
    return r.returncode, (_files(d) if d.exists() else {})


def det_break():
    canon = _canon()
    bd = det_dir() / "bent"
    if bd.exists():
        shutil.rmtree(bd)
    (bd / "regbooks" / REG).mkdir(parents=True)
    bent = {}
    for name, p in canon.items():
        q = bd / name
        shutil.copy2(p, q)
        bent[name] = q
    md = bytearray(bent["STAGE_S.md"].read_bytes())
    md[len(md) // 2] ^= 0x01
    bent["STAGE_S.md"].write_bytes(bytes(md))

    def float_moved():
        fd = det_dir() / "floatmoved"
        if fd.exists():
            shutil.rmtree(fd)
        (fd / "regbooks" / REG).mkdir(parents=True)
        c2 = {}
        for name, p in canon.items():
            shutil.copy2(p, fd / name)
            c2[name] = fd / name
        d = pd.read_parquet(str(canon["S_R2_1H.parquet"]))
        d.loc[d.index[0], "ratio_median"] = float(d["ratio_median"].iloc[0]) + 1e-6
        d.to_parquet(str(c2["S_R2_1H.parquet"]), index=False)
        return det_findings((0, c2), (0, c2), canon, la="moved copy", lb="moved copy")

    def hashorder():
        o = {s: det_build(det_dir() / f"hashorder_{s}", s, hashorder=True) for s in DET_SEEDS}
        a, b = o[DET_SEEDS[0]], o[DET_SEEDS[1]]
        return [x for x in det_findings(a, b, a[1]) if x.startswith(f"seed 1 vs seed {SEED}")]

    return plants([
        ("one byte bent in a copy of STAGE_S.md", "canonical vs bent copy: STAGE_S.md bytes differ",
         lambda: det_findings((0, canon), (0, bent), canon, la="canonical", lb="bent copy")),
        ("one ratio_median moved 1e-6 in a parquet copy",
         "moved copy vs canonical: S_R2_1H.parquet content sha", float_moved),
        ("a hash-order-dependent line (set iteration) under the two seeds",
         f"seed 1 vs seed {SEED}: STAGE_S.md bytes differ", hashorder),
    ])


def det_real():
    canon = _canon()
    o = {s: det_build(det_dir() / f"seed_{s}", s) for s in DET_SEEDS}
    a, b = o[DET_SEEDS[0]], o[DET_SEEDS[1]]
    bad = det_findings(a, b, canon)
    shas = ", ".join(f"{k} {sha_bytes(v.read_bytes())[:12]}…" for k, v in sorted(a[1].items()))
    return (not bad), (f"exit {a[0]}/{b[0]}; file set == the typed {len(FILES_TYPED) + 1} files "
                       f"in both builds and in the record; every file byte-identical seed 1 == "
                       f"seed {SEED} == canonical, the parquet content sha equal: {not bad} "
                       f"({shas})" + (f"; findings {bad[:4]}" if bad else ""))


FIXTURES = (
    ("F-SCALP-GATE", "the R2 gate at 1h: re-derived from its printed columns, CLOSED, and "
     "the CLOSED record filed exactly [L-S.1, L-R.4, L-1.2, §10]",
     "the fixture's reading of the 1h R2 row (the [Q-R3] law on its printed columns, the net "
     "identity, the reopening clause with the maker twin re-derived from R2_FEASIBILITY) "
     "disagrees with its printed labels; or a build from the files of record, or the files "
     "of record themselves, are not exactly the CLOSED record the fixture derives (STATUS "
     "CLOSED_BY_PRECONDITION, reason 'CLOSED BY R2 (1h: <verdict>)', arms [], the 1h row "
     "whole, the maker-twin word, the tuning-era word beside + collar, the source sha; "
     "S_GATE's clause values; STAGE_S.md's title, row, stop and words; STATUS.json alone in "
     "regbooks/P-SCALP-2); or CLOSED is filed on a PASS; or a reopening-path label opens "
     "the gate; or a PASS the JSON, the parquet and the manifest do not all print opens it; "
     "or a planted mislabel is not HALTed by its named detector; or a genuine / boundary "
     "PASS does not open the gate",
     gate_break, gate_real),
    ("F-GRID", "S_R2_1H — the whole 1h CLASSIC5 R2 block, re-derived, collared [SS-6]",
     "S_R2_1H.parquet is not the 108 declared cells exactly, a typed column holds a null, "
     "a row's collar is not L-1.4's (Tier-E on every row but the record row, Stage R's "
     "record collar on it) or a row carries a verdict column, a printed value differs from "
     "R2_FEASIBILITY, a clause flag / net_rederived / would_read differs from the fixture's "
     "reading, the record flag is not on the typed record cell only, a typed role is "
     "missing, an as-of stamp is not typed, or STAGE_S.md does not print every cell once",
     grid_break, grid_real),
    ("F-KEY", "every written table and record: the typed columns, unique keys, no null, "
     "the manifest, and no arm under a CLOSED registration",
     "S_R2_1H's column list / dtypes are not typed, a key repeats, a required column holds "
     "a null, the manifest's key / rows / content sha / file shas are not the files', "
     "STATUS.json or S_GATE.json lacks a typed field (or it is null / mistyped), the status "
     "word is not one of the three, or regbooks/P-SCALP-2 holds anything but STATUS.json",
     key_break, key_real),
    ("F-DET", "two subprocess builds under different hash seeds, one set of bytes",
     "the PYTHONHASHSEED 1 and 20260924 builds (under RUN_ROOT/_det_stage_s) differ from "
     "each other or from the files of record (stage_s/ + regbooks/P-SCALP-2/STATUS.json) in "
     "the file set, any byte or the parquet's content sha, or either exits nonzero",
     det_break, det_real),
)


def file_transcript(out: Path, body: bytes, refile: bool) -> list[str]:
    """NEVER CLOBBER the transcript of record [tierc10_resume_fixtures.file_transcript]."""
    if not out.exists() and not refile:
        return [f"{out.name} ABSENT — nothing written; re-file with --refile-transcript"]
    if out.exists() and out.read_bytes() == body:
        return []
    if out.exists() and not refile:
        (rr := out.with_name(out.stem + "_rerun.txt")).write_bytes(body)
        return [f"{out.name} NOT byte-identical; this run -> {rr.name}; record untouched"]
    out.write_bytes(body)
    return []


def main() -> int:
    args = sys.argv[1:]
    global RUN_ROOT
    root = RUN_ROOT = Path(next((a.split("=", 1)[1] for a in args if a.startswith("--root=")),
                                OUT)).resolve()
    pick = [a.lower() for a in args if not a.startswith("--")]
    t0 = time.time()
    say(AS_OF_LINE)
    say("=" * 78)
    say("TIER-C11 STAGE S FIXTURES — scripts/tierc11_stage_s.py (the scalper's R2 gate at "
        "1h and the CLOSED record) — break leg first, RED or void")
    say("=" * 78)
    say(f"seed {SEED} · substrate {TC11_SNAP.name} · pin {PIN} · registration {REG}")
    for ln in S.READINGS:
        say(ln)
    for fid, title, fails_if, b, r in FIXTURES:
        if not pick or any(q in fid.lower() for q in pick):
            prove(fid, title, fails_if, b, r)
    say(f"\n  {len(PASSED)} GREEN, {len(FAILED)} RED")
    for f in FAILED:
        say(f"    RED: {f}")
    root.mkdir(parents=True, exist_ok=True)
    body = ("\n".join(LINES) + "\n").encode("utf-8")
    name = TRANSCRIPT if not pick else TRANSCRIPT.replace(".txt", "_partial.txt")
    bad = file_transcript(root / name, body, "--refile-transcript" in args or bool(pick))
    for x in bad:
        clock(x)
    clock(f"wall {time.time() - t0:.1f}s · transcript sha {sha_bytes(body)}")
    if FAILED:
        print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
    return 1 if (FAILED or bad) else 0


if __name__ == "__main__":
    raise SystemExit(main())
