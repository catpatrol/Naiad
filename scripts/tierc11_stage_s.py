#!/usr/bin/env python
"""TIER-C11 · STAGE S — THE SCALPER RETUNED, GATED BY R2 AT 1H [LEANS L-S.1, L-S.2,
L-1.2, L-R.4, §10; AMENDMENTS AM-2, AM-7].

Contract of record: exchange/queue/2026-09-24_TC11_APOLLO.md (sha256 bb38e016…,
STEP Q b9ed953), STAGE S: "Preconditions: R2 must PASS at 1h (the 1h range is the
target; if 1h ranges are not respected net of toll, the mode is closed and the
stage prints that verdict and stops)."  Executor HEPHAESTUS; seed 20260924
(sensitivity 20260816), N_BOOT 4000.  Registration: P-SCALP-2 (REGISTRATIONS.json
seq 6, payload sha c4e7ea00…), vs zero, CLASSIC5, holdout era, taker.

L-S.1 PRECONDITION (frozen text): "Stage S runs only if the R2 lens verdict of
record at 1h is PASS. Otherwise it prints "CLOSED BY R2 (1h: <verdict>)" and
stops. P-SCALP-2's §0 row reads that verdict, with no number and no slot spent."

A RUNNER, RANGE-FREE.  It imports tierc11_env (E: the substrate guard, the audit
hook, the constants of record) and reads Stage R's filed records; it reads no
range fact, so it never imports tierc11_nest.  Parquet is read and written only
through pandas on path strings [AM-2]; no subprocess here (the F-DET harness lives
in the fixtures).

WHAT IT DOES
  1. THE GATE [L-S.1 ← L-R.4].  Reads research_outputs/tierc11/stage_r/
     R2_LENS_VERDICTS.json (the file of record; the scorer reads it too, SC-17),
     takes lenses['1h'] and RE-DERIVES its word from its PRINTED COLUMNS by the
     [Q-R3] law typed here — height leg n_ranges >= 30, ratio_median >= 3.0,
     share_ratio_lt_1 <= 0.10; edge leg edge_n_ranges >= 30, edge_n >= 30,
     edge_net_h20 > 0; both legs; under a floor -> 'FAIL (provisional, n<30)'.
     The printed net must be its printed parts' difference (round 8, the census's
     arithmetic).  A label that disagrees with its own columns HALTs (LABEL-LAW):
     neither the label nor the re-derivation is trusted alone.  The row must be the
     lens verdict of record: its (pool, era, scale, toll), the file's record block,
     and its member set exactly CLASSIC5 (RECORD-SPEC).
  2. CROSS-FILE, ON EVERY PATH, BEFORE THE DECISION IS ACTED ON [SS-5]: the JSON
     row is cross-checked against R2_FEASIBILITY.parquet's record row (every
     shared field), the parquet's content sha and 1h word against Stage R's
     build_manifest, the maker / charter / tuning / ALL words against this stage's
     re-derivation of the matching parquet rows, and every row of the 1h CLASSIC5
     block (its word and its collar, R2-ROW-WORD / R2-COLLAR).  Only a gate the
     JSON, the parquet and the manifest AGREE on is acted on.
  3. IF THE VERDICT OF RECORD IS NOT 'PASS' (the case when this runner was
     written: 1h FAIL) — the stage STOPS.  It writes
       research_outputs/tierc11/stage_s/
         S_GATE.json          the gate record: the 1h R2 row whole, the clause
                              table, the re-derived word, the maker-twin word (the
                              reopening path), the tuning-era word beside (Tier-E).
         S_R2_1H.parquet      the whole 1h CLASSIC5 R2 block (POOLED:CLASSIC5 + the
                              five members x {ALL, tuning, holdout} x {calibrated,
                              frozen3.0} x {taker, maker, charter} = 108 cells),
                              re-derived, `would_read` only; every row but the
                              record row collared Tier-E (gates nothing), the record
                              row carrying Stage R's record collar verbatim [L-1.4];
                              the gate is S_GATE.json.  Key: cell.
         STAGE_S.md           the stage report, every table whole.
         build_manifest.json  shas, keys, inputs, readings.
       research_outputs/tierc11/regbooks/P-SCALP-2/STATUS.json
                              {registration, status CLOSED_BY_PRECONDITION,
                              reason 'CLOSED BY R2 (1h: <verdict>)', arms [], the R2
                              row, the maker-twin word, the tuning-era word beside}.
     NO scalper book, NO twin, NO regime gate, NO Tier-E arm is built [L-S.1].
  4. IF THE VERDICT OF RECORD IS 'PASS' (and the three files agree on it, step 2)
     — this runner HALTs GATE-OPEN and writes NOTHING.  STEP 2 (the L-S.2
     scalper, its twins and F-SCALP / F-SCALP-ASOF) is built only on a PASS, and
     the verdict of record was FAIL when this runner was written; a PASS must
     re-dispatch Stage S STEP 2.  The runner therefore never files CLOSED on a
     PASS and never files a book it was not written to build.  A PASS printed in
     the JSON alone (the parquet or the manifest still FAIL) HALTs its cross-file
     detector (R2-MANIFEST / JSON-PARQUET), never GATE-OPEN.

THE READINGS BUILT (LEANS, quoted by id; the frozen text governs)
  L-S.1  the precondition: the R2 lens verdict of record at 1h == PASS, else
         "CLOSED BY R2 (1h: <verdict>)" and stop; the rival (gating on the
         tuning-era R2) was rejected [§10] — its word is printed beside, Tier-E.
  L-R.4  the lens verdict of record = the CLASSIC5 pooled row, HOLDOUT era,
         calibrated scale, taker toll; two words PASS / FAIL; an under-floor FAIL
         reads 'FAIL (provisional, n<30)'; a taker FAIL with a maker-twin PASS reads
         'FAIL — maker twin PASSES (the reopening path; needs a toll-model change
         the operator rules)'.
  L-1.2  the maker twin (4.0 bps round trip in R2) is the only reopening path.
  §10    "The §0 row prints the tuning-era R2 word beside it as Tier-E".
  L-S.2  the form — NOT BUILT (the precondition failed).
  AM-7   the haircut twin law — no trade row exists, nothing to price.

SUB-READINGS (the frozen text is silent; disclosed, printed in the lean block)
  SS-1 THE GATE READS THE JSON OF RECORD.  R2_LENS_VERDICTS.json lenses['1h'] is
       re-derived from its printed columns by the law typed HERE (not imported from
       the census or Stage R).  Its printed `word` (taker), `provisional` and
       `verdict` must equal the re-derivation, the verdict read with the printed
       maker-twin word under L-R.4's reopening clause; any disagreement HALTs
       LABEL-LAW.  Its (pool, era, scale, toll) and the file's `record` block must
       be the lens verdict of record, and it must pool exactly CLASSIC5 (`members`
       == 'BTCUSDT,ETHUSDT,SOLUSDT,NEARUSDT,ZECUSDT', `fallback_members` a subset of
       CLASSIC5) (RECORD-SPEC); no '1h' lens HALTs NO-1H.  A non-empty
       `fallback_members` is NOT off-record: L-R.2 keeps a whole-tape fallback pick
       as the calibrated scale of record (labelled IN-SAMPLE), and Stage R's own 1w
       verdict of record pools five fallback members.
  SS-2 THE NET IDENTITY.  The printed edge_net_h20 must equal round(round(median,
       8) − round(toll, 8), 8) EXACTLY (the census's printed arithmetic, SR-3;
       exact on every finite R2 row); else HALT NET-ARITH — the sign decision
       reads a net whose parts are printed beside it.
  SS-3 THE GATE OPENS ONLY ON THE EXACT WORD 'PASS' [L-S.1 "only if … PASS"]:
       'FAIL', 'FAIL (provisional, n<30)' and 'FAIL — maker twin PASSES (…)' all
       keep it closed; the reason prints the verdict of record VERBATIM.
  SS-4 THE OPEN PATH HALTs GATE-OPEN and writes nothing (above, 4) — only after
       SS-5 has passed, so GATE-OPEN fires only on a PASS the JSON, the parquet and
       Stage R's manifest agree on.
  SS-5 CROSS-FILE BEFORE ACTING, ON BOTH PATHS.  The JSON row == R2_FEASIBILITY.parquet's record
       row on every shared field (JSON-PARQUET); the parquet's content sha ==
       Stage R's build_manifest sha['R2_FEASIBILITY'] and the manifest's 1h lens
       word == the JSON's verdict (R2-MANIFEST); the JSON's maker_twin /
       charter_twin / tier_e_tuning_word / tier_e_all_word == this stage's
       re-derivation of the matching parquet rows (MAKER-TWIN, CHARTER-TWIN,
       TUNING-WORD, ALL-WORD); every block row's re-derived word == its printed
       word (R2-ROW-WORD), and every block row's printed collar is L-1.4's
       (R2-COLLAR).  The maker-twin word of record is the maker row of the SAME
       (panel, lens, era, scale) as the record row.
  SS-6 THE BLOCK PRINTED is the whole 1h R2 block for CLASSIC5 (108 cells).  It is
       a re-derivation view, `would_read` only, no verdict column.  Its collar
       follows L-1.4 ("every non-registered table and every R2 row except the lens
       verdict of record"): every row but the record row carries the Tier-E
       collar (TIER-E · a SELECTION, not a result · gates nothing); the record row
       (flagged `is_lens_verdict_of_record`) carries Stage R's record collar
       VERBATIM (tier 'R2 LENS VERDICT OF RECORD [L-R.4]' · 'n/a — the lens
       verdict of record, not a selection' · gates 'range trading on this lens …;
       at 1h also Stage S [L-S.1]').  Each row's collar is R2's own, checked
       against the typed pair (R2-COLLAR).  Its word of record lives in
       S_GATE.json / STATUS.json, not in this table.
  SS-7 NO BOOK.  A CLOSED registration holds no arm: regbooks/P-SCALP-2 holds
       STATUS.json only; anything else there HALTs STRAY-BOOK (never deleted by
       this runner).

WHAT WOULD MAKE THIS WRONG: trusting the printed word without its columns (a
mislabelled PASS would open the stage); reading the tuning-era word as the gate
(§10 rejected it); opening on the reopening-path word (it is a FAIL until the
operator rules a toll-model change); filing CLOSED on a PASS; building any book
on a FAIL.

REPAIR (2026-09-25, the Stage S verifier's report; no rule moved after a number):
  D1 the record row of S_R2_1H carried the Tier-E collar, against L-1.4's "except
     the lens verdict of record" — it now carries Stage R's record collar verbatim
     (SS-6, R2-COLLAR).  D2 the cross-file checks ran on the CLOSED path only — they
     now run before GATE-OPEN too (SS-4, SS-5).  D3 STAGE_S.md §5 said the verdict
     did not depend on the exact pooled median — true of the gate, false of the
     verdict word (the maker twin); reworded, the raw-bar zero block cited.  D4
     RECORD-SPEC now also requires the CLASSIC5 member set (the fallback half of
     the suggestion rejected: see SS-1).

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_s.py                  # the build
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_s.py --out-dir=DIR    # F-DET twin
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_env as E                                              # noqa: E402  (guards first)

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

# ══════════════════════════════════════════════════════ 0 · CONSTANTS OF RECORD
PIN_MS, PIN_ISO, SEED = E.PIN_MS, E.PIN_ISO, E.SEED
SUBSTRATE = E.SNAPSHOT.name
CLASSIC5 = tuple(E.CLASSIC5)
REG = "P-SCALP-2"
REG_PAYLOAD_SHA = "c4e7ea0064bf0355804f311b8a2c91af1178de0ac9e705a417a1cc09b90bd250"
OUT = E.OUT / "stage_s"
DET_ROOT = OUT / "_det_stage_s"
REG_DIR = E.OUT / "regbooks" / REG
R2_JSON = E.OUT / "stage_r" / "R2_LENS_VERDICTS.json"
R2_FEAS = E.OUT / "stage_r" / "R2_FEASIBILITY.parquet"
R2_MANIFEST = E.OUT / "stage_r" / "build_manifest.json"
REL = {"r2_json": "research_outputs/tierc11/stage_r/R2_LENS_VERDICTS.json",
       "r2_feas": "research_outputs/tierc11/stage_r/R2_FEASIBILITY.parquet",
       "r2_manifest": "research_outputs/tierc11/stage_r/build_manifest.json",
       "gate": "research_outputs/tierc11/stage_s/S_GATE.json",
       "block": "research_outputs/tierc11/stage_s/S_R2_1H.parquet",
       "report": "research_outputs/tierc11/stage_s/STAGE_S.md",
       "regdir": f"research_outputs/tierc11/regbooks/{REG}",
       "status": f"research_outputs/tierc11/regbooks/{REG}/STATUS.json",
       "script": "scripts/tierc11_stage_s.py"}
GATE_LENS = "1h"                                  # L-S.1: the 1h range is the target
POOL_C5 = "POOLED:CLASSIC5"
# L-R.4: the lens verdict of record — in the JSON's own field names and the parquet's
RECORD_ROW = {"pool": POOL_C5, "era": "holdout", "scale": "calibrated", "toll": "taker"}
RECORD_BLOCK = {"panel": POOL_C5, "era": "holdout", "scale_kind": "calibrated",
                "toll": "taker"}
# THE [Q-R3] LAW [L-R.4], typed here: the height leg AND the edge-fade leg, a leg
# under its floor FAILS
LAW = {"height_n_ranges_min": 30, "height_ratio_median_min": 3.0,
       "height_share_lt1_max": 0.10, "edge_n_ranges_min": 30, "edge_n_min": 30,
       "edge_net_gt": 0.0}
ROUND_ND = 8                                      # the census's printed precision (SR-3)
WORD_PASS, WORD_FAIL, WORD_PROV = "PASS", "FAIL", "FAIL (provisional, n<30)"
REOPEN = ("FAIL — maker twin PASSES (the reopening path; needs a toll-model change the "
          "operator rules)")
COLLAR = {"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
          "gates": "nothing"}
# L-1.4: the collar is on "every R2 row except the lens verdict of record"; the record
# row carries Stage R's record collar (tierc11_stage_r.RECORD_COLLAR), typed here
# verbatim — this runner is range-free and never imports Stage R
RECORD_COLLAR = {"tier": "R2 LENS VERDICT OF RECORD [L-R.4]",
                 "selection_not_a_result": "n/a — the lens verdict of record, not a selection",
                 "gates": ("range trading on this lens in this and every later tier unless the "
                           "toll model changes [contract R2]; at 1h also Stage S [L-S.1]")}
CLASSIC5_MEMBERS = ",".join(CLASSIC5)             # the record row pools exactly these [L-R.4]
# D3 disclosure, CITED (not computed here: this runner is range-free): the raw-bar
# re-derivation of the 1h record row by the Stage S verifier (2026-09-25), re-run at
# the repair — ATR re-computed from raw 1h klines, the range machine supplying only
# the confirmed-range list at the filed pick.  Printed only when the row matches.
ZERO_BLOCK = {"edge_n": 12044, "edge_n_ranges": 771, "edge_median_term_h20": 0.0,
              "negative": 6012, "zero": 15, "positive": 6017, "middle_idx": (6021, 6022),
              "zeros_by_member": (("NEARUSDT", 10), ("ZECUSDT", 4), ("SOLUSDT", 1),
                                  ("BTCUSDT", 0), ("ETHUSDT", 0))}
AS_OF = {"as_of_last_closed_4h": PIN_ISO, "as_of_substrate": SUBSTRATE}
STATUS_CLOSED = "CLOSED_BY_PRECONDITION"
# the whole 1h CLASSIC5 block [SS-6]
BLOCK_PANELS = (POOL_C5,) + tuple(f"ASSET:{s}" for s in CLASSIC5)
BLOCK_ERAS = ("ALL", "tuning", "holdout")
BLOCK_SCALES = ("calibrated", "frozen3.0")
BLOCK_TOLLS = ("taker", "maker", "charter")
BLOCK_KEY = ["cell"]
BLOCK_COLUMNS = (
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
ROLES = {
    (POOL_C5, "holdout", "calibrated", "taker"):
        "the 1h lens verdict of record [L-R.4] — its word of record is in S_GATE.json / "
        "STATUS.json, not in this table",
    (POOL_C5, "holdout", "calibrated", "maker"):
        "maker twin of the record row — the reopening path [L-R.4, L-1.2]",
    (POOL_C5, "holdout", "calibrated", "charter"): "charter twin of the record row [L-1.1]",
    (POOL_C5, "tuning", "calibrated", "taker"):
        "the tuning-era word printed beside the verdict of record [LEANS §10]",
    (POOL_C5, "ALL", "calibrated", "taker"): "the ALL-era word printed beside",
}
ROLE_OTHER = "a twin of the block (Tier-E)"
# JSON 1h row field -> parquet record-row column [SS-5]
JSON_TO_PARQUET = (
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
L_S_1 = ("Stage S runs only if the R2 lens verdict of record at 1h is PASS. Otherwise it "
         "prints \"CLOSED BY R2 (1h: <verdict>)\" and stops. P-SCALP-2's §0 row reads that "
         "verdict, with no number and no slot spent.")
READINGS = (
    f"{E.LEAN_TAG} L-S.1 the precondition: the R2 lens verdict of record at 1h (CLASSIC5 "
    f"pooled, holdout, calibrated, taker) == PASS, else 'CLOSED BY R2 (1h: <verdict>)' and "
    f"STOP — no book, no twin, no Tier-E arm; the tuning-era word printed beside, Tier-E "
    f"[§10].",
    f"{E.LEAN_TAG} L-R.4 the [Q-R3] law typed here: height n_ranges >= 30, ratio_median >= "
    f"3.0, share_ratio_lt_1 <= 0.10; edge edge_n_ranges >= 30, edge_n >= 30, edge_net_h20 > "
    f"0; both legs; under a floor -> '{WORD_PROV}'; taker FAIL + maker PASS -> the "
    f"reopening-path word.",
    f"{E.LEAN_TAG} SS-1 the gate re-derives the JSON of record's 1h word from its printed "
    f"columns; a label that disagrees with its columns HALTs LABEL-LAW; a row that is not "
    f"the verdict of record (pool / era / scale / toll, the record block, members == "
    f"CLASSIC5, fallback_members within CLASSIC5) HALTs RECORD-SPEC.",
    f"{E.LEAN_TAG} SS-2 the printed net must be round(round(median,8) - round(toll,8), 8) "
    f"exactly (NET-ARITH).",
    f"{E.LEAN_TAG} SS-3 the gate opens only on the exact word 'PASS'; the reason prints the "
    f"verdict of record verbatim.",
    f"{E.LEAN_TAG} SS-4 on a PASS this runner HALTs GATE-OPEN and writes nothing (STEP 2, "
    f"the L-S.2 scalper, is built only on a PASS — re-dispatch) — only after SS-5 passes.",
    f"{E.LEAN_TAG} SS-5 before acting on the gate, on both paths: JSON row == "
    f"R2_FEASIBILITY record row, the parquet's content sha and 1h word == Stage R's "
    f"manifest, the maker / charter / tuning / ALL words == this stage's re-derivation, "
    f"every block row's word and collar == the law's.",
    f"{E.LEAN_TAG} SS-6 S_R2_1H.parquet = the whole 1h CLASSIC5 R2 block (108 cells), "
    f"re-derived, would_read only; every row but the record row collared Tier-E (gates "
    f"nothing), the record row carrying Stage R's record collar verbatim [L-1.4].",
    f"{E.LEAN_TAG} SS-7 a CLOSED registration holds no arm: regbooks/{REG} holds "
    f"STATUS.json only (STRAY-BOOK HALT otherwise).",
)


REPAIR_LOG = (
    "Verifier verdict: the stage's result holds (CLOSED BY R2 (1h: FAIL), no book); 0 "
    "BLOCKER, 0 MAJOR, 4 MINOR implementation / report defects, 7 MINOR fixture gaps. No "
    "rule moved after a number: the gate, its words, S_GATE.json and STATUS.json are "
    "unchanged by the repair.",
    "D1 FIXED — the ★ row of S_R2_1H carried the Tier-E collar ('gates nothing'), against "
    "L-1.4 ('every R2 row except the lens verdict of record'). It now carries Stage R's "
    "record collar verbatim; every block row's collar is checked against the typed pair "
    "(R2-COLLAR).",
    "D2 FIXED — the cross-file checks (SS-5) ran on the CLOSED path only, so a PASS printed "
    "in the JSON alone reached GATE-OPEN. They now run before the gate is acted on; "
    "GATE-OPEN fires only on a PASS the JSON, the parquet and Stage R's manifest agree on.",
    "D3 FIXED — §5 said the result did not depend on the exact pooled median. True of the "
    "gate state, false of the verdict word: a pooled median above the maker twin's binding "
    "toll would have read the reopening-path word. Reworded, and the raw-bar zero block "
    "cited.",
    "D4 FIXED IN PART — RECORD-SPEC now requires the CLASSIC5 member set and a "
    "fallback_members list within CLASSIC5. NOT required: an empty fallback_members (L-R.2 "
    "keeps a whole-tape fallback pick as the calibrated scale of record, labelled "
    "IN-SAMPLE; Stage R's own 1w verdict of record pools five fallback members).",
    "F1-F7 CLOSED in the fixtures: plants for an edge_n_ranges-only floor, the charter and "
    "ALL words, each of the 21 JSON / parquet field pairs, a net off by 1e-8, a second "
    "flagged row, a stray scored.json; the transcript root-independent; the F-DET plant "
    "labels name what they compare. The block-level record-flag check has no plant of its "
    "own: the flagged-count check implies it (an equivalent mutant).",
)


def _halt(msg: str) -> None:
    raise SystemExit(f"HALT: {msg}")


# ══════════════════════════════════════════════════════ 1 · THE LAW, RE-DERIVED
def _count(x, name: str) -> int:
    if x is None or (not isinstance(x, (int, np.integer)) and pd.isna(x)):
        _halt(f"LABEL-LAW — count column {name} is null; the law needs a count")
    if isinstance(x, (bool, np.bool_)):
        _halt(f"LABEL-LAW — count column {name} is a boolean")
    v = float(x)
    if not v.is_integer():
        _halt(f"LABEL-LAW — count column {name} = {x!r} is not an integer")
    return int(v)


def _real(x) -> float:
    if x is None or (not isinstance(x, (int, float, np.integer, np.floating)) and pd.isna(x)):
        return float("nan")
    return float(x)


def legs_of(r) -> dict:
    """The [Q-R3] law on ONE row's printed columns (a dict or a Series).
    Returns every clause, both legs, the floor flag, the re-derived net, the
    net identity and the word.  Reads LAW at call time."""
    nr, en, enr = (_count(r["n_ranges"], "n_ranges"), _count(r["edge_n"], "edge_n"),
                   _count(r["edge_n_ranges"], "edge_n_ranges"))
    ratio, share = _real(r["ratio_median"]), _real(r["share_ratio_lt_1"])
    m, t, net = (_real(r["edge_median_term_h20"]), _real(r["edge_toll_atr"]),
                 _real(r["edge_net_h20"]))
    if math.isfinite(m) and math.isfinite(t):
        net_re = round(round(m, ROUND_ND) - round(t, ROUND_ND), ROUND_ND)
        identity = math.isfinite(net) and net_re == net
    else:
        net_re = float("nan")
        identity = not math.isfinite(net)
    c = {
        "height_n_ranges_ok": nr >= LAW["height_n_ranges_min"],
        "height_ratio_ok": math.isfinite(ratio) and ratio >= LAW["height_ratio_median_min"],
        "height_share_ok": math.isfinite(share) and share <= LAW["height_share_lt1_max"],
        "edge_n_ranges_ok": enr >= LAW["edge_n_ranges_min"],
        "edge_n_ok": en >= LAW["edge_n_min"],
        "edge_net_ok": math.isfinite(net) and net > LAW["edge_net_gt"],
    }
    height = c["height_n_ranges_ok"] and c["height_ratio_ok"] and c["height_share_ok"]
    edge = c["edge_n_ranges_ok"] and c["edge_n_ok"] and c["edge_net_ok"]
    under = (nr < LAW["height_n_ranges_min"] or enr < LAW["edge_n_ranges_min"]
             or en < LAW["edge_n_min"])
    word = WORD_PASS if (height and edge) else (WORD_PROV if under else WORD_FAIL)
    return {**c, "height_leg_holds": bool(height), "edge_leg_holds": bool(edge),
            "under_floor": bool(under), "net_rederived": net_re,
            "net_identity_holds": bool(identity), "word": word,
            "values": {"n_ranges": nr, "ratio_median": ratio, "share_ratio_lt_1": share,
                       "edge_n_ranges": enr, "edge_n": en, "edge_median_term_h20": m,
                       "edge_toll_atr": t, "edge_net_h20": net}}


def record_verdict(taker_word: str, maker_word: str) -> str:
    """L-R.4: PASS on a taker PASS; the reopening-path word on a taker FAIL with a
    maker-twin PASS; else the taker word."""
    if taker_word == WORD_PASS:
        return WORD_PASS
    if maker_word == WORD_PASS:
        return REOPEN
    return taker_word


def gate_opens(verdict: str) -> bool:
    """SS-3: the gate opens only on the exact word 'PASS'."""
    return verdict == WORD_PASS


def clause_rows(L: dict) -> list[dict]:
    v = L["values"]
    return [
        {"leg": "height", "clause": "n_ranges >= 30", "column": "n_ranges",
         "value": v["n_ranges"], "bound": ">= 30", "holds": L["height_n_ranges_ok"]},
        {"leg": "height", "clause": "median(height / toll) >= 3.0", "column": "ratio_median",
         "value": v["ratio_median"], "bound": ">= 3.0", "holds": L["height_ratio_ok"]},
        {"leg": "height", "clause": "share(ratio < 1) <= 0.10", "column": "share_ratio_lt_1",
         "value": v["share_ratio_lt_1"], "bound": "<= 0.10", "holds": L["height_share_ok"]},
        {"leg": "edge", "clause": "edge_n_ranges >= 30", "column": "edge_n_ranges",
         "value": v["edge_n_ranges"], "bound": ">= 30", "holds": L["edge_n_ranges_ok"]},
        {"leg": "edge", "clause": "edge_n >= 30", "column": "edge_n",
         "value": v["edge_n"], "bound": ">= 30", "holds": L["edge_n_ok"]},
        {"leg": "edge", "clause": "median H20 term - toll > 0", "column": "edge_net_h20",
         "value": v["edge_net_h20"], "bound": "> 0", "holds": L["edge_net_ok"]},
    ]


# ══════════════════════════════════════════════════════ 2 · THE GATE [L-S.1]
def gate(r2: dict) -> dict:
    """SS-1..SS-3 on the JSON of record.  HALTs NO-1H / RECORD-SPEC / NET-ARITH /
    LABEL-LAW; returns the decision (open iff the verdict of record is PASS)."""
    lenses = r2.get("lenses") if isinstance(r2, dict) else None
    if not isinstance(lenses, dict) or GATE_LENS not in lenses:
        _halt(f"NO-1H — the R2 verdicts file holds no '{GATE_LENS}' lens verdict; L-S.1 "
              f"cannot be read")
    rec = r2.get("record")
    if rec != RECORD_BLOCK:
        _halt(f"RECORD-SPEC — the file's record block {rec!r} is not the lens verdict of "
              f"record {RECORD_BLOCK!r} [L-R.4]")
    v = lenses[GATE_LENS]
    spec = {k: v.get(k) for k in RECORD_ROW}
    if spec != RECORD_ROW:
        _halt(f"RECORD-SPEC — the {GATE_LENS} row is {spec!r}, not the lens verdict of "
              f"record {RECORD_ROW!r} [L-R.4]")
    if v.get("members") != CLASSIC5_MEMBERS:
        _halt(f"RECORD-SPEC — the {GATE_LENS} row pools {v.get('members')!r}, not CLASSIC5 "
              f"{CLASSIC5_MEMBERS!r} [L-R.4: the CLASSIC5 pooled row]")
    fb = v.get("fallback_members")
    if not isinstance(fb, str) or any(x not in CLASSIC5 for x in fb.split(",") if x):
        _halt(f"RECORD-SPEC — the {GATE_LENS} row's fallback_members {fb!r} is not a subset "
              f"of CLASSIC5 [L-R.4]")
    L = legs_of(v)
    if not L["net_identity_holds"]:
        _halt(f"NET-ARITH — printed edge_net_h20 {v.get('edge_net_h20')!r} != round(round("
              f"{v.get('edge_median_term_h20')!r}, 8) - round({v.get('edge_toll_atr')!r}, 8), "
              f"8) = {L['net_rederived']!r}")
    if v.get("word") != L["word"]:
        _halt(f"LABEL-LAW — the {GATE_LENS} taker word is printed {v.get('word')!r} but its "
              f"columns read {L['word']!r} under the [Q-R3] law")
    if not isinstance(v.get("provisional"), bool) or v["provisional"] != L["under_floor"]:
        _halt(f"LABEL-LAW — printed provisional {v.get('provisional')!r} but the floor law "
              f"reads {L['under_floor']!r}")
    mk = v.get("maker_twin")
    if mk not in (WORD_PASS, WORD_FAIL, WORD_PROV):
        _halt(f"LABEL-LAW — the printed maker-twin word {mk!r} is not one of the two words")
    want = record_verdict(L["word"], mk)
    if v.get("verdict") != want:
        _halt(f"LABEL-LAW — the {GATE_LENS} verdict is printed {v.get('verdict')!r} but the "
              f"re-derived taker word {L['word']!r} with the printed maker twin {mk!r} reads "
              f"{want!r} [L-R.4]")
    opened = gate_opens(want)
    return {"open": bool(opened), "lens": GATE_LENS, "row": v, "legs": L,
            "clauses": clause_rows(L), "verdict": want, "taker_word": L["word"],
            "reason": f"CLOSED BY R2 ({GATE_LENS}: {want})"}


# ══════════════════════════════════════════════════════ 3 · CROSS-FILE [SS-5]
def content_sha(df: pd.DataFrame) -> str:
    """The lineage's content hash (tierc2_baseline._content_sha): sha256 of the
    frame's CSV, not the parquet bytes."""
    return hashlib.sha256(df.to_csv(index=False).encode("utf-8")).hexdigest()


def _row(feas: pd.DataFrame, panel: str, lens: str, era: str, scale: str, toll: str,
         tag: str) -> pd.Series:
    z = feas[(feas["panel"] == panel) & (feas["lens"] == lens) & (feas["era"] == era)
             & (feas["scale_kind"] == scale) & (feas["toll"] == toll)]
    if len(z) != 1:
        _halt(f"{tag} — R2_FEASIBILITY holds {len(z)} rows for {panel}|{lens}|{era}|{scale}|"
              f"{toll}, not one")
    return z.iloc[0]


def _same(a, b) -> bool:
    if isinstance(a, bool) or isinstance(b, (bool, np.bool_)):
        return isinstance(a, bool) and bool(b) == a
    if isinstance(a, str) or isinstance(b, str):
        return a == b
    if a is None or b is None:
        return a is None and (b is None or bool(pd.isna(b)))
    fa, fb = float(a), float(b)
    return (fa == fb) or (math.isnan(fa) and math.isnan(fb))


def printed_word(r: pd.Series) -> str | None:
    """A row's own printed word: `word` on the record row, `would_read` on Tier-E."""
    return r["word"] if bool(r["is_lens_verdict_of_record"]) else r["would_read"]


def cross_check(r2: dict, feas: pd.DataFrame, man: dict) -> dict:
    v = r2["lenses"][GATE_LENS]
    sha = content_sha(feas)
    if (man.get("sha") or {}).get("R2_FEASIBILITY") != sha:
        _halt(f"R2-MANIFEST — R2_FEASIBILITY.parquet content sha {sha[:16]}… is not the "
              f"sha Stage R's build_manifest vouches for "
              f"({str((man.get('sha') or {}).get('R2_FEASIBILITY'))[:16]}…)")
    if (man.get("lens_verdicts") or {}).get(GATE_LENS) != v.get("verdict"):
        _halt(f"R2-MANIFEST — Stage R's manifest reads the {GATE_LENS} lens "
              f"{(man.get('lens_verdicts') or {}).get(GATE_LENS)!r}, the JSON {v.get('verdict')!r}")
    rec = _row(feas, POOL_C5, GATE_LENS, "holdout", "calibrated", "taker", "JSON-PARQUET")
    if not bool(rec["is_lens_verdict_of_record"]):
        _halt("JSON-PARQUET — the parquet does not flag the record cell as the lens verdict "
              "of record")
    flagged = feas[(feas["lens"] == GATE_LENS) & feas["is_lens_verdict_of_record"].astype(bool)]
    if len(flagged) != 1:
        _halt(f"JSON-PARQUET — {len(flagged)} {GATE_LENS} rows flagged as the verdict of record")
    bad = [f"{j}={v.get(j)!r} vs {p}={rec[p]!r}" for j, p in JSON_TO_PARQUET
           if not _same(v.get(j), rec[p])]
    if bad:
        _halt(f"JSON-PARQUET — the JSON {GATE_LENS} row differs from R2_FEASIBILITY's record "
              f"row: {bad[:4]}")
    twins = {}
    for key, era, toll, jfield, tag in (
            ("maker_twin", "holdout", "maker", "maker_twin", "MAKER-TWIN"),
            ("charter_twin", "holdout", "charter", "charter_twin", "CHARTER-TWIN"),
            ("tuning_word", "tuning", "taker", "tier_e_tuning_word", "TUNING-WORD"),
            ("all_word", "ALL", "taker", "tier_e_all_word", "ALL-WORD")):
        r = _row(feas, POOL_C5, GATE_LENS, era, "calibrated", toll, tag)
        L = legs_of(r)
        if not L["net_identity_holds"]:
            _halt(f"{tag} — NET-ARITH on {r['cell']}")
        if L["word"] != v.get(jfield) or L["word"] != printed_word(r):
            _halt(f"{tag} — the JSON's {jfield} {v.get(jfield)!r} / the row's printed word "
                  f"{printed_word(r)!r} != this stage's re-derivation {L['word']!r} of "
                  f"{r['cell']}")
        twins[key] = {"cell": str(r["cell"]), "word": L["word"], "legs": _legs_json(L),
                      "clauses": clause_rows(L)}
    return {"feas_content_sha": sha, "twins": twins,
            "record_row": {c: _jsonable(rec[c]) for c in feas.columns}}


# ══════════════════════════════════════════════════════ 4 · THE BLOCK [SS-6]
def block_table(feas: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for panel in BLOCK_PANELS:
        for era in BLOCK_ERAS:
            for scale in BLOCK_SCALES:
                for toll in BLOCK_TOLLS:
                    r = _row(feas, panel, GATE_LENS, era, scale, toll, "BLOCK")
                    cell = "|".join((panel, GATE_LENS, era, scale, toll))
                    if r["cell"] != cell:
                        _halt(f"BLOCK — R2 cell {r['cell']!r} != {cell!r}")
                    rec = (panel, era, scale, toll) == tuple(RECORD_BLOCK.values())
                    if bool(r["is_lens_verdict_of_record"]) != rec:
                        _halt(f"BLOCK — {cell}: is_lens_verdict_of_record "
                              f"{bool(r['is_lens_verdict_of_record'])} but the record is "
                              f"{RECORD_BLOCK}")
                    want_collar = RECORD_COLLAR if rec else COLLAR
                    got_collar = {k: r[k] for k in COLLAR}
                    if got_collar != want_collar:
                        _halt(f"R2-COLLAR — {cell}: R2 prints the collar {got_collar!r}, but "
                              f"L-1.4 gives "
                              f"{'the lens verdict of record' if rec else 'every other R2 row'} "
                              f"{want_collar!r}")
                    L = legs_of(r)
                    pw = printed_word(r)
                    if not L["net_identity_holds"]:
                        _halt(f"R2-ROW-WORD — NET-ARITH on {cell}")
                    if L["word"] != pw:
                        _halt(f"R2-ROW-WORD — {cell}: printed {pw!r}, re-derived {L['word']!r}")
                    rows.append({
                        "cell": cell, "panel": panel, "lens": GATE_LENS, "era": era,
                        "scale_kind": scale, "toll": toll,
                        "role": ROLES.get((panel, era, scale, toll), ROLE_OTHER),
                        "is_lens_verdict_of_record": bool(rec),
                        "n_ranges": L["values"]["n_ranges"],
                        "ratio_median": L["values"]["ratio_median"],
                        "share_ratio_lt_1": L["values"]["share_ratio_lt_1"],
                        "edge_n": L["values"]["edge_n"],
                        "edge_n_ranges": L["values"]["edge_n_ranges"],
                        "edge_median_term_h20": L["values"]["edge_median_term_h20"],
                        "edge_toll_atr": L["values"]["edge_toll_atr"],
                        "edge_net_h20": L["values"]["edge_net_h20"],
                        "toll_bps_rt_min": float(r["toll_bps_rt_min"]),
                        "toll_bps_rt_max": float(r["toll_bps_rt_max"]),
                        "net_rederived": L["net_rederived"],
                        "net_identity_holds": L["net_identity_holds"],
                        **{k: bool(L[k]) for k in (
                            "height_n_ranges_ok", "height_ratio_ok", "height_share_ok",
                            "height_leg_holds", "edge_n_ranges_ok", "edge_n_ok", "edge_net_ok",
                            "edge_leg_holds", "under_floor")},
                        "would_read": L["word"], "r2_printed_word": pw,
                        "agrees_with_r2": L["word"] == pw,
                        "pick_window": str(r["pick_window"]),
                        "scale_in_sample": str(r["scale_in_sample"]),
                        "stability_changed_members": str(r["stability_changed_members"]),
                        **want_collar, **AS_OF})
    d = pd.DataFrame(rows, columns=list(BLOCK_COLUMNS))
    for c in ("n_ranges", "edge_n", "edge_n_ranges"):
        d[c] = d[c].astype(np.int64)
    for c in ("ratio_median", "share_ratio_lt_1", "edge_median_term_h20", "edge_toll_atr",
              "edge_net_h20", "toll_bps_rt_min", "toll_bps_rt_max", "net_rederived"):
        d[c] = d[c].astype(np.float64)
    if d["cell"].duplicated().any():
        _halt("BLOCK — duplicated cell")
    return d


# ══════════════════════════════════════════════════════ 5 · RECORDS AND REPORT
def _jsonable(x):
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, np.integer):
        return int(x)
    if isinstance(x, (np.floating, float)):
        f = float(x)
        return None if math.isnan(f) else f
    if x is None or (not isinstance(x, (str, list, dict, tuple)) and pd.isna(x)):
        return None
    return x


def _legs_json(L: dict) -> dict:
    return {k: (_jsonable(v) if not isinstance(v, dict) else {a: _jsonable(b)
                                                             for a, b in v.items()})
            for k, v in L.items()}


def reopening_text(maker_word: str) -> str:
    if maker_word == WORD_PASS:
        return ("the maker twin of the record row PASSES — the reopening path [L-R.4]: it "
                "needs a toll-model change the operator rules; until then the lens stays "
                "closed")
    return (f"none — the maker twin of the record row reads {maker_word} too, so no "
            f"reopening path exists at 1h ('{REOPEN}' is read only when the maker twin "
            f"of the same row passes) [L-R.4, L-1.2]")


def beside_text(tw: str, verdict: str) -> str:
    return (f"beside, Tier-E [LEANS §10] (tier {COLLAR['tier']} · "
            f"{COLLAR['selection_not_a_result']} · gates {COLLAR['gates']}): the tuning-era R2 "
            f"{GATE_LENS} word {tw} (holdout word of record {verdict})")


def gate_record(G: dict, X: dict, r2_sha: str, reg: dict) -> dict:
    mk, tw = X["twins"]["maker_twin"]["word"], X["twins"]["tuning_word"]["word"]
    return {
        "registration": REG, "registration_payload_sha256": reg["sha256"], "stage": "TC11-S",
        "as_of": PIN_ISO, "as_of_close_ms": PIN_MS, "seed": SEED,
        "reading": {"L-S.1": L_S_1},
        "lens": GATE_LENS, "record": RECORD_BLOCK,
        "source": {"r2_verdicts": {"path": REL["r2_json"], "sha256": r2_sha},
                   "r2_feasibility": {"path": REL["r2_feas"],
                                      "content_sha256": X["feas_content_sha"]},
                   "r2_manifest": {"path": REL["r2_manifest"],
                                   "vouches_for_feasibility_content_sha": True}},
        "r2_row": G["row"],
        "r2_record_row_parquet": X["record_row"],
        "law": LAW,
        "rederivation": {"clauses": [{k: _jsonable(v) for k, v in c.items()}
                                     for c in G["clauses"]],
                         "height_leg_holds": G["legs"]["height_leg_holds"],
                         "edge_leg_holds": G["legs"]["edge_leg_holds"],
                         "under_floor": G["legs"]["under_floor"],
                         "net_rederived": _jsonable(G["legs"]["net_rederived"]),
                         "net_identity_holds": G["legs"]["net_identity_holds"],
                         "taker_word": G["taker_word"]},
        "printed": {"word": G["row"].get("word"), "verdict": G["row"].get("verdict"),
                    "provisional": G["row"].get("provisional"),
                    "maker_twin": G["row"].get("maker_twin")},
        "labels_agree_with_columns": True,
        "verdict_of_record": G["verdict"],
        "gate": "OPEN" if G["open"] else "CLOSED",
        "reason": G["reason"],
        "maker_twin": {**X["twins"]["maker_twin"], "reopening_path": reopening_text(mk)},
        "charter_twin": X["twins"]["charter_twin"],
        "beside_tier_e": {"tuning_era_word": tw,
                          "tuning_row": X["twins"]["tuning_word"],
                          "all_era_word": X["twins"]["all_word"]["word"],
                          "all_row": X["twins"]["all_word"],
                          **COLLAR, "reading": "LEANS §10",
                          "text": beside_text(tw, G["verdict"])},
        "stage_stops": ("Stage S STOPS [L-S.1]: no scalper book, no maker twin (fill assumed "
                        "or fill conditioned), no 17-asset view, no regime gate, no tuning "
                        "slice, no frozen-3.0 twin, no refused-entry count and no "
                        "target/stop ratio distribution were built; P-SCALP-2's §0 row reads "
                        "the verdict, with no number and no slot spent."),
    }


def status_record(G: dict, X: dict, r2_sha: str) -> dict:
    mk, tw = X["twins"]["maker_twin"]["word"], X["twins"]["tuning_word"]["word"]
    return {
        "registration": REG,
        "status": STATUS_CLOSED,
        "reason": G["reason"],
        "arms": [],
        "as_of": PIN_ISO, "seed": SEED,
        "ruler": "vs_zero", "panel": list(CLASSIC5), "era_scope": "holdout",
        "precondition": ("R2 lens verdict of record at 1h (CLASSIC5 pooled, holdout, "
                         "calibrated, taker) == PASS [L-S.1]"),
        "precondition_word": G["verdict"],
        "rederived_taker_word": G["taker_word"],
        "r2_source": {"path": REL["r2_json"], "sha256": r2_sha},
        "r2_row": G["row"],
        "maker_twin_word": mk,
        "reopening_path": reopening_text(mk),
        "tier_e_beside": {"tuning_era_word": tw, **COLLAR, "reading": "LEANS §10",
                          "text": beside_text(tw, G["verdict"])},
        "verdict_cell_reads": (f"{G['reason']} — no number, no slot spent (m = 9 unchanged, "
                               f"the bar 0.10/9 not loosened) [L-S.1, L-1.4]"),
        "no_book": ("a CLOSED registration holds no arm: no scored, base or Tier-E book was "
                    "built [L-S.1, SS-7]"),
        "gate_record": REL["gate"],
        "source_script": REL["script"],
    }


def _fmt(x) -> str:
    if isinstance(x, (bool, np.bool_)):
        return "True" if bool(x) else "False"
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    if isinstance(x, (float, np.floating)):
        f = float(x)
        return "nan" if math.isnan(f) else repr(f)
    if x is None or (not isinstance(x, (str, list, dict, tuple)) and pd.isna(x)):
        return "null"
    s = str(x) if not isinstance(x, (list, dict, tuple)) else json.dumps(x, sort_keys=True)
    return s.replace("|", "\\|")


def _f8(x) -> str:
    f = float(x)
    return "nan" if math.isnan(f) else f"{f:+.8f}"


def render_md(G: dict, X: dict, T: pd.DataFrame, gr: dict, st: dict) -> str:
    v = G["row"]
    mk, ch = X["twins"]["maker_twin"], X["twins"]["charter_twin"]
    tw, aw = X["twins"]["tuning_word"], X["twins"]["all_word"]
    L = []
    a = L.append
    a(f"# TIER-C11 · STAGE S — THE SCALPER RETUNED: {G['reason']}")
    a("")
    a(f"as_of_last_closed_4h: {PIN_ISO} · substrate {SUBSTRATE} · seed {SEED} · pin {PIN_MS}")
    a("")
    a("Contract of record: `exchange/queue/2026-09-24_TC11_APOLLO.md` (sha256 bb38e016…), "
      "STAGE S. Registration P-SCALP-2 (seq 6, payload sha "
      f"{REG_PAYLOAD_SHA[:12]}…): vs zero, CLASSIC5, holdout era, taker. Readings built: "
      "L-S.1 (the precondition), L-R.4 (the lens verdict of record and its two words), "
      "L-1.2 (the maker twin, the reopening path), LEANS §10 (the tuning-era word beside). "
      "Not built: L-S.2 (the form) and AM-7 (no trade row exists to price). Source: "
      f"`{REL['script']}`.")
    a("")
    a("## 0 · The verdict")
    a("")
    a(f"**{G['reason']}.** The R2 lens verdict of record at 1h (CLASSIC5 pooled, holdout "
      f"era, calibrated scale, taker toll) is **{G['verdict']}**. Stage S re-derived it from "
      "the row's printed columns under the [Q-R3] law (§2); the printed labels agree with "
      "the columns.")
    a("")
    a(f"- **{gr['stage_stops']}**")
    a(f"- **P-SCALP-2's §0 cell reads:** {st['verdict_cell_reads']}.")
    a(f"- **The maker-twin word (the reopening path):** {mk['word']}. "
      f"Reopening path: {reopening_text(mk['word'])}.")
    a(f"- **Beside, Tier-E [LEANS §10]** (tier {COLLAR['tier']} · "
      f"{COLLAR['selection_not_a_result']} · gates {COLLAR['gates']}): the tuning-era R2 "
      f"{GATE_LENS} word {tw['word']} (holdout word of record {G['verdict']}). It decides "
      "nothing.")
    a(f"- `regbooks/{REG}/STATUS.json`: status `{STATUS_CLOSED}`, reason "
      f"`{G['reason']}`, arms `[]`.")
    a("")
    a("## 1 · The 1h R2 row of record, whole")
    a("")
    a(f"From `{REL['r2_json']}` (sha256 `{gr['source']['r2_verdicts']['sha256']}`), "
      f"`lenses['1h']`, all {len(v)} fields; the file's `record` block is "
      f"`{json.dumps(RECORD_BLOCK, sort_keys=True)}`.")
    a("")
    a("| field | value |")
    a("|---|---|")
    for k in sorted(v):
        a(f"| {k} | {_fmt(v[k])} |")
    a("")
    rr = X["record_row"]
    a(f"The same row in `{REL['r2_feas']}` (content sha256 `{X['feas_content_sha']}`, equal "
      f"to Stage R's build_manifest), all {len(rr)} columns; it equals the JSON row on every "
      f"shared field ({len(JSON_TO_PARQUET)} checked).")
    a("")
    a("| column | value |")
    a("|---|---|")
    for k, x in rr.items():
        a(f"| {k} | {_fmt(x)} |")
    a("")
    a("## 2 · The re-derivation [L-S.1 ← L-R.4, the [Q-R3] law]")
    a("")
    a("| leg | clause | printed column | printed value | law | holds |")
    a("|---|---|---|---|---|---|")
    for c in G["clauses"]:
        a(f"| {c['leg']} | {c['clause']} | {c['column']} | {_fmt(c['value'])} | {c['bound']} "
          f"| {'yes' if c['holds'] else 'NO'} |")
    Lg = G["legs"]
    a("")
    a(f"- Net identity [SS-2]: round(round({_fmt(v['edge_median_term_h20'])}, 8) − "
      f"round({_fmt(v['edge_toll_atr'])}, 8), 8) = {_fmt(Lg['net_rederived'])} == printed "
      f"edge_net_h20 {_fmt(v['edge_net_h20'])}: "
      f"{'holds' if Lg['net_identity_holds'] else 'FAILS'}.")
    a(f"- Height leg: {'holds' if Lg['height_leg_holds'] else 'FAILS'}. Edge leg: "
      f"{'holds' if Lg['edge_leg_holds'] else 'FAILS'}. Under a floor: "
      f"{'yes' if Lg['under_floor'] else 'no'}. Re-derived taker word: **{Lg['word']}**.")
    a(f"- Printed: word `{v.get('word')}` · provisional `{v.get('provisional')}` · maker_twin "
      f"`{v.get('maker_twin')}` · verdict `{v.get('verdict')}`. L-R.4 reads the verdict as "
      f"record_verdict(taker {Lg['word']}, maker {v.get('maker_twin')}) = "
      f"`{G['verdict']}`. The labels agree with the columns.")
    a(f"- The gate opens only on the exact word `PASS` [SS-3]: **{G['verdict']} → gate "
      f"{'OPEN' if G['open'] else 'CLOSED'}**.")
    a("")
    a("## 3 · The words beside the verdict of record")
    a("")
    a("Each row re-derived by Stage S from R2_FEASIBILITY.parquet's printed columns and "
      "matched against the JSON field that prints it. Only the first row is the verdict of "
      "record; the others are Tier-E (tier TIER-E · a SELECTION, not a result · gates "
      "nothing).")
    a("")
    a("| role | panel · era · scale · toll | n_ranges | ratio_median | share<1 | edge_n "
      "| edge ranges | median H20 | toll ATR | net H20 | re-derived | printed in JSON |")
    a("|---|---|---|---|---|---|---|---|---|---|---|---|")
    items = [("verdict of record [L-R.4]", G["row"], Lg["word"], "word", v.get("word"))]
    for lab, t, jf in (("maker twin — the reopening path [L-1.2]", mk, "maker_twin"),
                       ("charter twin [L-1.1]", ch, "charter_twin"),
                       ("tuning-era word beside [§10], Tier-E", tw, "tier_e_tuning_word"),
                       ("ALL-era word beside, Tier-E", aw, "tier_e_all_word")):
        items.append((lab, t, t["word"], jf, v.get(jf)))
    for lab, t, w, jf, pw in items:
        if "clauses" in t:
            vals = {c["column"]: c["value"] for c in t["clauses"]}
            vv = t["legs"]["values"]
            cell = t["cell"].split("|")
            desc = f"{cell[0]} · {cell[2]} · {cell[3]} · {cell[4]}"
        else:
            vals, vv = {c["column"]: c["value"] for c in G["clauses"]}, Lg["values"]
            desc = f"{POOL_C5} · holdout · calibrated · taker"
        a(f"| {lab} | {desc} | {_fmt(vals['n_ranges'])} | {_fmt(vals['ratio_median'])} | "
          f"{_fmt(vals['share_ratio_lt_1'])} | {_fmt(vals['edge_n'])} | "
          f"{_fmt(vals['edge_n_ranges'])} | {_f8(vv['edge_median_term_h20'])} | "
          f"{_f8(vv['edge_toll_atr'])} | {_f8(vv['edge_net_h20'])} | {w} | `{jf}` = {pw} |")
    a("")
    a("## 4 · The 1h CLASSIC5 R2 block, re-derived, whole — Tier-E but the ★ row")
    a("")
    a(f"`{REL['block']}` — {len(T)} cells = {len(BLOCK_PANELS)} panels × {len(BLOCK_ERAS)} "
      f"eras × {len(BLOCK_SCALES)} scales × {len(BLOCK_TOLLS)} tolls. `would_read` = the "
      "[Q-R3] law on the row's printed columns; `R2 word` = the word R2 printed for that row "
      "(`word` on the record row, `would_read` elsewhere). Collar [L-1.4]: every row but ★ "
      f"carries tier {COLLAR['tier']} · {COLLAR['selection_not_a_result']} · gates "
      f"{COLLAR['gates']}. The ★ row is the lens verdict of record and carries Stage R's "
      f"record collar verbatim: tier `{RECORD_COLLAR['tier']}` · "
      f"`{RECORD_COLLAR['selection_not_a_result']}` · gates `{RECORD_COLLAR['gates']}`. "
      "Its word of record lives in S_GATE.json / STATUS.json, and Stage S reads its gate "
      "from the JSON of record, never from this table.")
    a("")
    a("| ★ | panel | era | scale | toll | n_ranges | ratio_median | share<1 | edge_n | "
      "edge ranges | median H20 | toll ATR | net H20 | height | edge | floor | would_read "
      "| R2 word | agree |")
    a("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in T.itertuples(index=False):
        a(f"| {'★' if r.is_lens_verdict_of_record else ''} | {r.panel} | {r.era} | "
          f"{r.scale_kind} | {r.toll} | {r.n_ranges} | {r.ratio_median:.8f} | "
          f"{r.share_ratio_lt_1:.8f} | {r.edge_n} | {r.edge_n_ranges} | "
          f"{_f8(r.edge_median_term_h20)} | {_f8(r.edge_toll_atr)} | {_f8(r.edge_net_h20)} | "
          f"{'holds' if r.height_leg_holds else 'fails'} | "
          f"{'holds' if r.edge_leg_holds else 'fails'} | "
          f"{'under' if r.under_floor else '—'} | {r.would_read} | {r.r2_printed_word} | "
          f"{'yes' if r.agrees_with_r2 else 'NO'} |")
    a("")
    cnt = T.groupby("would_read").size().to_dict()
    a(f"Block tally (all {len(T)} rows, the ★ row included; the others Tier-E, a SELECTION, "
      f"not a result): would_read "
      + ", ".join(f"{k} {cnt[k]}" for k in sorted(cnt))
      + f"; agrees with R2 on {int(T['agrees_with_r2'].sum())}/{len(T)} rows.")
    a("")
    a("## 5 · Disclosures")
    a("")
    hc = (T["era"] == "holdout") & (T["scale_kind"] == "calibrated")
    mem = T[hc & (T["toll"] == "taker") & (T["panel"] != POOL_C5)]
    pooled = {t: T[hc & (T["toll"] == t) & (T["panel"] == POOL_C5)].iloc[0] for t in BLOCK_TOLLS}
    pk = pooled["taker"]
    pm = float(pk.edge_median_term_h20)
    srt = mem.sort_values(["edge_median_term_h20", "panel"], ascending=[False, True])
    top, bot = srt.iloc[0], srt.iloc[-1]
    hi = float(top.edge_median_term_h20)

    def above(t: str) -> pd.DataFrame:
        return srt[srt["edge_median_term_h20"] > float(pooled[t].edge_toll_atr)]

    def others_hold(t: str) -> bool:        # every clause but the edge net holds
        p = pooled[t]
        return bool(p.height_leg_holds and p.edge_n_ranges_ok and p.edge_n_ok)

    def names(d: pd.DataFrame) -> str:
        return ", ".join(f"{r.panel.split(':', 1)[1]} {_f8(r.edge_median_term_h20)}"
                         for r in d.itertuples(index=False))

    gate_free = above("taker").empty
    word_free = gate_free and (above("maker").empty or not others_hold("maker"))
    head = ("The gate state rests on its exact value." if not gate_free else
            "Neither the gate state nor the verdict word depends on its exact value."
            if word_free else
            "The gate state does not depend on its exact value; the verdict word does.")
    a(f"- **The pooled holdout median H20 term prints {_f8(pm)}. {head}**"
      f" A pooled median lies within the range of its members' medians (up to the averaging "
      f"of two middle values), here [{bot.panel} {_f8(bot.edge_median_term_h20)}, {top.panel} "
      f"{_f8(hi)}]. Each pooled edge toll is the binding (largest) member toll.")
    for t, row_lab, short in (("taker", "the record row (the gate)", "the record row"),
                              ("maker", "the maker twin (the reopening path, L-R.4)",
                               "the maker twin"),
                              ("charter", "the charter twin (Tier-E)", "the charter twin")):
        tt, ab = float(pooled[t].edge_toll_atr), above(t)
        if ab.empty:
            txt = (f"above every member's median, so the {t} edge net is negative for any "
                   f"value the pooled median could take")
        elif not others_hold(t):
            txt = (f"below the medians of {names(ab)}, but another clause of the row fails, so "
                   f"the row fails for any pooled value")
        else:
            txt = (f"below the medians of {names(ab)}: a pooled median in ({_f8(tt)}, "
                   f"{_f8(float(ab.edge_median_term_h20.max()))}] would have made {short} "
                   f"PASS")
            if t == "maker" and gate_free:
                txt += (f", and the verdict of record would have read '{REOPEN}'. The verdict "
                        f"WORD therefore rests on the printed pooled value, not only on its "
                        f"sign")
            elif t == "taker":
                txt += ". The gate state therefore rests on the printed pooled value"
        a(f"  - {row_lab}: toll {_f8(tt)} ATR, {txt}.")
    zb = ZERO_BLOCK
    if (int(pk.edge_n) == zb["edge_n"] and int(pk.edge_n_ranges) == zb["edge_n_ranges"]
            and pm == zb["edge_median_term_h20"]):
        a(f"- **The printed pooled median is exactly {_f8(pm)}, verified from raw bars "
          f"(cited, not computed here).** This runner is range-free and reads the median as "
          f"Stage R printed it. The Stage S verifier's independent re-derivation from the raw "
          f"1h klines (2026-09-25, re-run at this repair; ATR re-computed, the range machine "
          f"supplying only the confirmed-range list at the filed pick) reproduced the record "
          f"row exactly: n {zb['edge_n']} over {zb['edge_n_ranges']} ranges, "
          f"{zb['negative']} negative, {zb['zero']} exactly-zero and {zb['positive']} positive "
          f"H20 terms. Both middle order statistics (0-based indices {zb['middle_idx'][0]} and "
          f"{zb['middle_idx'][1]}) fall in the zero block, so the median is 0.0 exactly "
          f"(zeros by member: "
          + ", ".join(f"{s} {k}" for s, k in zb["zeros_by_member"]) + ").")
    else:
        a(f"- **The raw-bar re-derivation cited at the repair (n {zb['edge_n']}, "
          f"{zb['edge_n_ranges']} ranges, median 0.0) does not describe this row**; its printed "
          f"pooled median is Stage R's, not re-derived from raw bars.")
    a("- Members at the record cell (Tier-E): "
      + "; ".join(f"{r.panel} median {_f8(r.edge_median_term_h20)} · toll "
                  f"{_f8(r.edge_toll_atr)} · net {_f8(r.edge_net_h20)} · {r.would_read}"
                  for r in mem.itertuples(index=False)) + ".")
    a("- **Holdout scale.** The record row's scale is the tuning-era pick, out of sample on "
      f"the holdout ({v.get('scale_in_sample')}); stability-changed members: "
      f"{v.get('stability_changed_members') or 'none'}.")
    a("- **Provenance.** The JSON of record is the file the scorer reads for P-SCALP-2 "
      "(SC-17). R2_FEASIBILITY.parquet's content sha equals Stage R's build_manifest, and "
      f"the manifest's 1h lens word is `{v.get('verdict')}`.")
    a("")
    a("## 6 · Not built, and why")
    a("")
    a("- **STEP 2, the L-S.2 scalper, is not built.** L-S.1 runs it only on a 1h PASS. Not "
      "built: the scored arm (holdout, vs zero, taker), the Tier-E arms (maker fill-assumed, "
      "maker fill-conditioned, the 17-asset view, the regime gate of 5m ATR tercile × 1h "
      "boundary-age tercile, the tuning slice, the frozen-3.0 twin), the refused-entry "
      "counts, and the (target − entry)/(entry − stop) distribution.")
    a("- **F-SCALP and F-SCALP-ASOF are not run.** They test a book that does not exist. "
      "F-SCALP-GATE, F-GRID, F-KEY and F-DET are run (`FIXTURES_STAGE_S.txt`).")
    a("- **The open path [SS-4].** On a 1h verdict of record of `PASS`, this runner halts "
      "with GATE-OPEN and writes nothing — only after the cross-file checks [SS-5] pass, so "
      "only on a PASS the JSON, R2_FEASIBILITY.parquet and Stage R's manifest agree on (a "
      "PASS in the JSON alone halts R2-MANIFEST or JSON-PARQUET). It never files CLOSED on "
      "a PASS, and a PASS must re-dispatch Stage S STEP 2.")
    a(f"- **Findings not fixed.** The 1h lens is closed for range trading in this and every "
      f"later tier unless the operator changes the toll model [contract R2]. The maker twin "
      f"at the record cell reads {mk['word']}, so no reopening path is open.")
    a("")
    a("## 7 · Lean block")
    a("")
    for ln in READINGS:
        a(f"- {ln}")
    a("")
    a("## 8 · Repair log (2026-09-25, the Stage S verifier's report)")
    a("")
    for ln in REPAIR_LOG:
        a(f"- {ln}")
    a("")
    return "\n".join(L)


# ════════════════════════════════════════════════════════════════ WRITING
def _inside(p: Path, root: Path) -> bool:
    return p == root or root in p.parents


def _guard_out(out: Path) -> Path:
    o = Path(out).resolve()
    if o == OUT.resolve() or o.parent == DET_ROOT.resolve():
        return o
    trees = {ROOT.resolve(), Path(E.MAIN_TREE).resolve()}
    if o.parent.name == DET_ROOT.name and not any(_inside(o, t) for t in trees):
        return o
    _halt(f"OUT-GUARD — output dir {o} is neither {OUT}, an F-DET run dir under {DET_ROOT}, "
          f"nor one under a {DET_ROOT.name}/ scratch outside the repo")
    return o


def reg_dir_for(out: Path) -> Path:
    o = Path(out).resolve()
    return REG_DIR if o == OUT.resolve() else o / "regbooks" / REG


def _write_parquet(d: pd.DataFrame, p: Path) -> None:
    tmp = p.with_name(p.name + ".tmp")
    d.to_parquet(str(tmp), index=False)
    os.replace(tmp, p)


def _write_text(p: Path, s: str) -> None:
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(s, encoding="utf-8")
    os.replace(tmp, p)


def _jdump(x) -> str:
    return json.dumps(x, indent=2, sort_keys=True, default=str, ensure_ascii=False) + "\n"


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def registration_check() -> dict:
    """The registration of record is the one this stage answers for (payload sha
    pinned), and its operative spec names the L-S.1 precondition."""
    regs = json.loads((E.OUT / "registrations" / "REGISTRATIONS.json").read_text(
        encoding="utf-8"))
    r = next((x for x in regs["registrations"] if x["registration"] == REG), None)
    if r is None or r["sha256"] != REG_PAYLOAD_SHA:
        _halt(f"REGISTRATION — {REG}'s payload sha is not {REG_PAYLOAD_SHA[:12]}…")
    sp = r["operative_spec"]
    if (sp.get("era") != "holdout" or sp.get("ruler") != "vs zero"
            or sp.get("panel") != "CLASSIC5"
            or "R2 lens verdict of record at 1h" not in str(sp.get("precondition"))):
        _halt(f"REGISTRATION — {REG}'s operative spec is not the L-S.1 precondition row")
    return r


def build(out: Path = OUT, r2_path: Path = R2_JSON, feas_path: Path = R2_FEAS,
          r2_manifest_path: Path = R2_MANIFEST) -> dict:
    out = _guard_out(out)
    rdir = reg_dir_for(out)
    reg = registration_check()
    raw = Path(r2_path).read_bytes()
    r2 = json.loads(raw.decode("utf-8"))
    G = gate(r2)
    # SS-5 on BOTH paths: the gate is acted on only when the JSON, the parquet and
    # Stage R's manifest agree on it (a JSON-only PASS HALTs its cross-file detector)
    feas = pd.read_parquet(str(feas_path))
    man = json.loads(Path(r2_manifest_path).read_text(encoding="utf-8"))
    X = cross_check(r2, feas, man)
    T = block_table(feas)
    if G["open"]:
        _halt(f"GATE-OPEN — the R2 lens verdict of record at {GATE_LENS} re-derives "
              f"{G['verdict']!r}, and the JSON, R2_FEASIBILITY and Stage R's manifest agree "
              f"on it: L-S.1 opens Stage S. STEP 2 (the L-S.2 scalper, its twins, "
              f"F-SCALP, F-SCALP-ASOF) is built only on a PASS and is not in this runner — "
              f"re-dispatch Stage S STEP 2. Nothing written (a CLOSED status is never filed "
              f"on a PASS).")
    if rdir.exists():
        stray = sorted(p.name for p in rdir.iterdir() if p.name != "STATUS.json")
        if stray:
            _halt(f"STRAY-BOOK — {rdir} holds {stray}: a CLOSED registration holds no arm "
                  f"[SS-7]; nothing deleted")
    r2_sha = sha_bytes(raw)
    gr = gate_record(G, X, r2_sha, reg)
    st = status_record(G, X, r2_sha)
    md = render_md(G, X, T, gr, st)
    out.mkdir(parents=True, exist_ok=True)
    rdir.mkdir(parents=True, exist_ok=True)
    _write_parquet(T, out / "S_R2_1H.parquet")
    gtxt, stxt = _jdump(gr), _jdump(st)
    _write_text(out / "S_GATE.json", gtxt)
    _write_text(out / "STAGE_S.md", md)
    _write_text(rdir / "STATUS.json", stxt)
    man_s = {
        "tier": "TIER-C11", "stage": "TC11-S", "seed": SEED, "n_boot": E.N_BOOT,
        "as_of": PIN_ISO, "as_of_close_ms": PIN_MS, "substrate": SUBSTRATE,
        "registration": {"id": REG, "payload_sha256": reg["sha256"]},
        "gate": {"lens": GATE_LENS, "verdict_of_record": G["verdict"],
                 "rederived_taker_word": G["taker_word"],
                 "state": "OPEN" if G["open"] else "CLOSED", "reason": G["reason"],
                 "maker_twin_word": X["twins"]["maker_twin"]["word"],
                 "tuning_era_word_tier_e": X["twins"]["tuning_word"]["word"]},
        "inputs": {REL["r2_json"]: {"sha256": r2_sha},
                   REL["r2_feas"]: {"content_sha256": X["feas_content_sha"]},
                   REL["r2_manifest"]: {"sha_R2_FEASIBILITY": X["feas_content_sha"],
                                        "lens_verdict_1h": man["lens_verdicts"][GATE_LENS]}},
        "sha": {"S_R2_1H": content_sha(T)},
        "keys": {"S_R2_1H": BLOCK_KEY},
        "rows": {"S_R2_1H": int(len(T))},
        "files": {"S_GATE.json": sha_bytes(gtxt.encode("utf-8")),
                  "STAGE_S.md": sha_bytes(md.encode("utf-8")),
                  "regbooks/P-SCALP-2/STATUS.json": sha_bytes(stxt.encode("utf-8"))},
        "regbooks": {"dir": REL["regdir"], "status": STATUS_CLOSED, "arms": []},
        "collar": COLLAR,
        "record_collar": RECORD_COLLAR,
        "readings": list(READINGS),
        "writer": "pandas.DataFrame.to_parquet on a path string [AM-2]; content sha = "
                  "sha256(DataFrame.to_csv(index=False)) (tierc2_baseline._content_sha law)",
    }
    _write_text(out / "build_manifest.json", _jdump(man_s))
    return {"gate": G, "cross": X, "table": T, "gate_record": gr, "status": st,
            "manifest": man_s, "out": out, "regdir": rdir}


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    od = next((a.split("=", 1)[1] for a in args if a.startswith("--out-dir=")), None)
    R = build(Path(od) if od else OUT)
    G = R["gate"]
    print(f"STAGE S · {G['reason']} · re-derived taker word {G['taker_word']} · maker twin "
          f"{R['cross']['twins']['maker_twin']['word']} · tuning-era word (Tier-E) "
          f"{R['cross']['twins']['tuning_word']['word']} · STATUS {R['status']['status']} · "
          f"arms [] — no book built [L-S.1]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
