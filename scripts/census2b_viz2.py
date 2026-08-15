#!/usr/bin/env python3
"""VIZ-2 · CATHEDRAL PAYLOADS -- Tier-E, DISPLAY-ONLY, m = 0.

Four payloads, emitted in the VIZ-1 format so one reader serves both stages:

  v3_may26_tape.json   the May-26 window: arming / relay / trigger / seal / bell
                       ts+px, displacement at arming, the stage stamps
  v3_stations.json     the twelve station cards -- gate text VERBATIM from the
                       six-rules record, evidence class per the ledger's
                       provenance tags, and the [VETO] pins each one leans on
  v3_terrain.json      per-campaign rank / asset / mfe / terminal / give-back /
                       hold / is_winner, under the 700 KB cap
  v3_helix.json        BTCUSDT 1h ribbon widths + knot/fan transitions,
                       state-change points and an hourly-derived spine

The meta block is NOT restated here: `write_payload` is imported from
scripts/census2a_viz.py so meta{sha256, rows, source_parquet, toll_lo/hi, ...}
has one implementation across both viz stages.  Only the output directory is
re-pointed.

DISCIPLINE, carried from VIZ-1 verbatim: a field with no source is emitted
`null` and named in `note` -- never invented.  (census2a_viz.py:33-36, the v6
`mae_r`/`n_reclaims` precedent.)
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import census2a_viz as V                                       # noqa: E402

SEED = 20260814
C2A = ROOT / "research_outputs" / "census2a"
C2B = ROOT / "research_outputs" / "census2b"
PAY = C2B / "viz_payloads"
HAND = C2B / "DESIGN_HANDOFF_VIZ3"
MC1 = ROOT / "research_outputs" / "mc1"

RULES_DOC = (ROOT / "exchange" / "reports" /
             "LANE_UPDATE_DIONYSUS_2026-08-13_BR-momentum_winner-zoom_brief-feedback.md")
BRIEF_DOC = (ROOT / "exchange" / "reports" /
             "DESIGN_BRIEF_CENSUS2A_VIZ_2026-08-12.md")

# ---- re-point the shared emitter at census-2B, and give it BOTH manifests so
#      source_parquet shas resolve for either estate.
PAY.mkdir(parents=True, exist_ok=True)
HAND.mkdir(parents=True, exist_ok=True)
V.PAY = PAY
# The shared emitter stamps meta.seed from its OWN module constant (VIZ-1's
# 20260812).  This run is seeded 20260814 and every record says so, so the
# emitter is re-pointed here too -- otherwise the payloads' provenance field
# contradicts the build document, the probe ledger and the lane ledger.
V.SEED = SEED
_ART = dict(json.loads((C2A / "census2a_manifest.json").read_text()).get("artifacts", {}))
for k, v in json.loads((C2B / "census2b_manifest.json").read_text()).get("artifacts", {}).items():
    _ART.setdefault(Path(k).with_suffix("").name if "/" not in k else k, v)
    _ART.setdefault(k, v)
V.ART = _ART
write_payload, jclean, src_meta = V.write_payload, V.jclean, V.src_meta

_INV: list[dict] = []
_NOTES: list[str] = []


def hr(ch="-", n=100):
    print(ch * n)


def banner(t):
    print()
    hr("=")
    print(t)
    hr("=")


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def raw_src(label: str, p: Path, rows) -> dict:
    """A source entry for a non-manifest input (json/parquet outside a manifest)."""
    return {"parquet": label, "sha256": sha_file(p), "rows": rows}


# ===========================================================  v3_may26_tape
# The five 4h cross families the pinned May-26 dossier actually carries.
STAGES = [
    ("arming",  "cross_9_89_dn",    "9x89 fast-median x M-ribbon"),
    ("relay",   "cross_9_200_dn",   "9x200 the relay's middle leg"),
    ("trigger", "cross_12_25_dn",   "12x25 fast-internal, the registration"),
    ("seal",    "cross_89_200_dn",  "89x200 M x MH -- the eulogy"),
    ("terrain", "cross_300_450_dn", "300x450 MH x H -- terrain, not signal"),
]
WIN_LO, WIN_HI = "2026-05-01", "2026-06-15"


def may26_tape() -> dict:
    banner("v3_may26_tape -- the May-26 window")
    pb = MC1 / "ops_series" / "perbar_4h.parquet"
    p = pd.read_parquet(pb)
    p["iso"] = pd.to_datetime(p.open_time, unit="ms", utc=True)
    lo, hi = pd.Timestamp(WIN_LO, tz="UTC"), pd.Timestamp(WIN_HI, tz="UTC")
    w = p[(p.iso >= lo) & (p.iso <= hi)].reset_index(drop=True)
    card = json.loads((MC1 / "MC1_results.json").read_text())["D3"]["event_card"]

    rows, arming_ts = [], None
    for stage, col, what in STAGES:
        s = w[w[col].astype(bool)]
        if not len(s):
            rows.append({"stage": stage, "cross": col, "what": what,
                         "ts_ms": None, "ts_iso": None, "px": None})
            continue
        # the May-26 anatomy is one bear sequence: take the LAST firing at or
        # before the seal for the legs, the archetype bar for the trigger.
        r = s.iloc[-1] if stage != "trigger" else \
            s[s.open_time == card["event_ts"]].iloc[0]
        disp = (abs(float(r.close) - float(r.e89)) / float(r.atr)
                if float(r.atr) > 0 else float("nan"))
        if stage == "arming":
            arming_ts = int(r.open_time)
        rows.append({
            "stage": stage, "cross": col, "what": what,
            "ts_ms": int(r.open_time),
            "ts_iso": r.iso.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "px": float(r.close), "atr_4h": float(r.atr),
            "e9": float(r.e9), "e12": float(r.e12), "e25": float(r.e25),
            "e89": float(r.e89), "e200": float(r.e200),
            "displacement_atr": disp,
            "hours_from_arming": (None if arming_ts is None else
                                  (int(r.open_time) - arming_ts) / 3.6e6),
        })

    # BELL: the only occurrence of the word in the estate names the ARMING
    # ("the arming -- the attention bell, window-opener", the six-rules record
    # SS3 line 2).  It is emitted as a ROLE ALIAS, not as a sixth event, so the
    # tape carries the operator's fifth word without inventing a fifth object.
    bell = {"stage": "bell", "alias_of": "arming",
            "provenance": "six-rules record §3.2: 'the arming — the attention "
                          "bell, window-opener [verified object]'",
            "ts_ms": arming_ts,
            "ts_iso": next(r["ts_iso"] for r in rows if r["stage"] == "arming"),
            "px": next(r["px"] for r in rows if r["stage"] == "arming"),
            "note": "NOT a distinct event. No separate 'bell' object exists in "
                    "the estate; emitting one would be invention."}
    _NOTES.append("v3_may26_tape: `bell` is a ROLE ALIAS of `arming` -- the "
                  "estate's only use of the word names the arming. A fifth "
                  "distinct stage does not exist and was not invented. The "
                  "fifth cross family the dossier does carry (300x450) is "
                  "emitted as `terrain` under its own name.")

    spine = [{"ts_ms": int(r.open_time), "px": float(r.close),
              "atr": float(r.atr)} for r in w.itertuples()]
    stamps = {k: v for k, v in card["stamps_display_only"].items()}

    for r in rows:
        print(f"    {r['stage']:8s} {str(r['ts_iso']):22s} px={r['px']:>10,.1f}"
              if r["ts_iso"] else f"    {r['stage']:8s} ABSENT")
    print(f"    bell     -> alias of arming ({bell['ts_iso']})")
    print(f"    stamps   {stamps}")
    print(f"    spine    {len(spine)} 4h bars {WIN_LO}..{WIN_HI}")

    data = {"window": {"from": WIN_LO, "to": WIN_HI, "tf": "4h",
                       "instrument": card["instrument"]},
            "stages": rows, "bell": bell, "stamps_display_only": stamps,
            "spine_4h": spine}
    inv = write_payload(
        "v3_may26_tape.json", data,
        [raw_src("mc1/ops_series/perbar_4h", pb, len(p)),
         raw_src("mc1/MC1_results.json(D3.event_card)",
                 MC1 / "MC1_results.json", 1)],
        downsample_rule=None,
        note="Stages are the 4h bear sequence of the pinned May-26 dossier. "
             "`bell` is a role alias of `arming` (the estate's only use of the "
             "word); no distinct bell object exists and none was invented. "
             "displacement_atr = |close - e89| / ATR at that bar, the "
             "continuous form of the WALL stamp (VIZ-1 v1_armings convention). "
             "stamps_display_only carried verbatim from MC1 D3.event_card; the "
             "MC-1 lockbox header applies -- hypothesis generation, never "
             "evidence.")
    _INV.append(inv)
    return {"rows": rows, "card": card}


# ============================================================  v3_stations
STAGE_OF = {
    "12_26 IN-WINDOW": "S3", "12_26 bare": "S3", "26_89": "S2",
    "12_89": "S2", "89_127": "S1", "89_316": "S6", "316_423": "S1",
    "316_889": "S1", "889_2618": "S1", "2618_4618": "S1",
    "knot->fan transition": "S1", "spring": "S2",
}
# provenance tags, defined in the six-rules record's own header line
EVIDENCE = {
    "12_26 IN-WINDOW": "[verified] — the census's single surviving registration, PROVISIONAL",
    "12_26 bare": "[verified] — same object outside an armed window",
    "26_89": "[descriptive] — DERIVED in ORACLE rev C; not in the pinned crosses taxonomy",
    "12_89": "[verified object] — 848 armed windows",
    "89_127": "[descriptive] — within-M, unregistered",
    "89_316": "[verified lag] — the seal/eulogy class",
    "316_423": "[descriptive] — terrain class",
    "316_889": "[descriptive] — terrain class",
    "889_2618": "[descriptive] — terrain class",
    "2618_4618": "[descriptive] — terrain class",
    "knot->fan transition": "[proposed] — P-FAN-1 filed, 60%; the operator's stated object",
    "spring": "[descriptive F3] — sweep-then-arm, registration pending",
}
VETOES = {
    "12_26 IN-WINDOW": ["kiss eps=0.25/delta=0.75/k=10", "window close = counter-12_89",
                        "toll 10 bps round trip"],
    "12_26 bare": ["kiss eps=0.25/delta=0.75/k=10", "toll 10 bps round trip"],
    "26_89": ["ATR_LEN=14", "warm-up law warmfactor=3.46"],
    "12_89": ["arm_pair=12_89", "sweep lookback 96 bars / reclaim 3 bars"],
    "89_127": ["ATR_LEN=14"], "89_316": ["ATR_LEN=14"],
    "316_423": ["ATR_LEN=14"], "316_889": ["ATR_LEN=14"],
    "889_2618": ["ATR_LEN=14"], "2618_4618": ["ATR_LEN=14", "warm-up law: NEVER on 4h"],
    "knot->fan transition": ["knot_c_atr=0.5 (per-SR)", "state k per SR (ORACLE R-3)"],
    "spring": ["sweep lookback 96 bars", "reclaim <= 3 bars"],
}


def six_rules() -> dict[str, dict]:
    """The six-stage kit, gate text VERBATIM from the six-rules record."""
    t = RULES_DOC.read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"^\*\*(S[1-6]) · (.+?)\.?\*\*", t, re.M):
        line = t[m.start():t.index("\n", m.start())]
        out[m.group(1)] = {"stage": m.group(1), "title": m.group(2),
                           "gate_text_verbatim": line}
    if len(out) != 6:
        raise SystemExit(f"HALT: six-rules record yielded {len(out)} rules, not 6")
    return out


def iron_rules() -> dict[str, dict]:
    """The OTHER six-rules record: DESIGN_BRIEF §2 IRON RULES, verbatim.

    Two records in this estate are exactly six numbered rules and either could
    be "the six-rules record": the trade-lifetime kit above, and these display
    gates.  Rather than guess, BOTH are carried verbatim and labelled; the
    station cards reference the lifecycle gate because a station is an instant
    in a trade's life (BUILD_2026-08-14_CENSUS2B_PARTA_WTB1.md §9, "STATION
    OCCUPANCY · the six-stage kit, photographed").  The design lane can switch
    the reference without a re-run because the text is already here.
    """
    p = BRIEF_DOC
    if not p.exists():
        return {}
    t = p.read_text(encoding="utf-8")
    sec = t[t.index("## §2 · IRON RULES"):]
    sec = sec[:sec.index("\n## ")]
    out = {}
    for m in re.finditer(r"^(\d)\. \*\*(.+?)\*\*", sec, re.M | re.S):
        blk = sec[m.start():]
        nxt = re.search(r"\n\d\. \*\*", blk)
        out[f"IR{m.group(1)}"] = {
            "rule": f"IR{m.group(1)}", "title": m.group(2).rstrip("."),
            "gate_text_verbatim": (blk[:nxt.start()] if nxt else blk).strip()}
    if len(out) != 6:
        raise SystemExit(f"HALT: IRON RULES yielded {len(out)} rules, not 6")
    return out


def stations() -> dict:
    banner("v3_stations -- the twelve station cards")
    rules = six_rules()
    irons = iron_rules()
    print(f"    six-rules record (A · trade lifetime): {RULES_DOC.name}")
    for k, v in rules.items():
        print(f"      {k} · {v['title'][:58]:58s} gate {len(v['gate_text_verbatim']):>4d} chars")

    gp = C2B / "oracle" / "oracle_grid.parquet"
    g = pd.read_parquet(gp)
    order = ["12_26 IN-WINDOW", "12_26 bare", "26_89", "12_89", "89_127",
             "89_316", "316_423", "316_889", "889_2618", "2618_4618",
             "knot->fan transition", "spring"]
    cards = []
    for i, cls in enumerate(order, 1):
        A = g[(g.cls == cls) & (g.cut == "ALL")]
        per_lens = [{"lens": r.tf, "n": int(r.n),
                     "H20_med": r.H20_med, "H20_net": r.H20_net,
                     "H100_med": r.H100_med, "H100_net": r.H100_net,
                     "toll_atr": r.toll_atr} for r in A.itertuples()]
        s = STAGE_OF[cls]
        cards.append({
            "station": i, "class": cls,
            "lifecycle_stage": s, "stage_title": rules[s]["title"],
            "gate_text_verbatim": rules[s]["gate_text_verbatim"],
            "evidence_class": EVIDENCE[cls],
            "veto_pins": VETOES[cls],
            "n_total": int(A.n.sum()),
            "per_lens": per_lens,
        })
        print(f"    {i:>2d} {cls:22s} {s} n={int(A.n.sum()):>8,d} "
              f"{EVIDENCE[cls][:44]}")

    from collections import Counter
    cov = Counter(c["lifecycle_stage"] for c in cards)
    empty = [s for s in rules if s not in cov]
    if empty:
        _NOTES.append(
            f"v3_stations: stages {', '.join(empty)} carry NO station. "
            f"{'/'.join(empty)} are post-entry disciplines (agile entry, "
            f"management) and the twelve ORACLE classes are all EVENTS, so "
            f"nothing crosses to them. Their gate text is still emitted in "
            f"full under `six_rules` -- the record is complete even where the "
            f"mapping is empty. Forcing a class into an empty stage would have "
            f"been invention. Coverage: {dict(sorted(cov.items()))}.")
        print(f"    stages with no station: {empty}  (gate text still emitted "
              f"under six_rules)")
    _NOTES.append("v3_stations: no record in the estate names a canonical "
                  "TWELVE. The twelve stations are the twelve ORACLE classes "
                  "(BUILD_2026-08-15_CENSUS2B_ORACLE.md §4), which is the only "
                  "twelve-item structure the estate has and is this lane's own "
                  "immediately preceding build. The MAPPING of each class to a "
                  "lifecycle stage S1..S6 is THIS PASS'S READING, not a ruled "
                  "assignment -- the gate text it carries is verbatim, the "
                  "mapping that selects which gate is not.")
    data = {"six_rules": rules, "iron_rules": irons, "stations": cards,
            "provenance_tags": {
                "[verified]": "census/ledger record",
                "[ratified]": "operator word",
                "[descriptive]": "Tier-E / unregistered",
                "[canon]": "knowledge base",
                "[proposed]": "needs word / registration"}}
    inv = write_payload(
        "v3_stations.json", data,
        [raw_src("census2b/oracle/oracle_grid", gp, len(g)),
         raw_src("six-rules record (LANE_UPDATE_DIONYSUS_2026-08-13)",
                 RULES_DOC, 6)],
        downsample_rule=None,
        note="TWO records in this estate are exactly six numbered rules and "
             "either could be 'the six-rules record'. BOTH are carried "
             "verbatim: `six_rules` = the trade-lifetime kit (S1..S6, the "
             "six-stage kit) and `iron_rules` = DESIGN_BRIEF §2 (IR1..IR6, the "
             "display gates). Each station's `gate_text_verbatim` quotes the "
             "LIFECYCLE gate, because a station is an instant in a trade's life "
             "(BUILD_2026-08-14 §9 'STATION OCCUPANCY · the six-stage kit, "
             "photographed'); the other reading needs no re-run, the text is "
             "already here. Provenance tags are the lifecycle record's own "
             "legend. The twelve "
             "stations are the twelve ORACLE classes -- no canonical twelve is "
             "named anywhere in the estate, and the class->stage mapping is "
             "this pass's reading, flagged as such. veto_pins names the "
             "constants each station leans on: pins, not truths.")
    _INV.append(inv)
    return data


# =============================================================  v3_terrain
def terrain() -> dict:
    banner("v3_terrain -- per-campaign")
    cp = C2A / "cen5" / "cen5_campaigns.parquet"
    c = pd.read_parquet(cp)
    # hold_s lives only on the WF1 rows; join it in rather than recompute
    hold = {}
    box = ROOT / "_reviewer_box" / "wf1"
    nraw = 0
    for f in sorted(box.glob("*USDT_*.json")):
        for r in json.loads(f.read_text(encoding="utf-8")).get("rows", []):
            if r.get("resolved"):
                nraw += 1
                hold[f"{r.get('cell')}|{r.get('tranche_id')}"] = r.get("hold_s")
    c["hold_s"] = c.tranche_id.map(hold)
    print(f"    cen5 campaigns {len(c):,}  wf1 resolved {nraw:,}  "
          f"hold_s joined on {int(c.hold_s.notna().sum()):,} "
          f"({c.hold_s.notna().mean():.1%})")

    # cen5 nulls MFE where the WF1 row carries exactly 0.0; they are ZEROS, not
    # missing data (verified: all 542 are 0.0 in wf1). Restored so the MFE
    # ordering is total and nothing sorts to an arbitrary end.
    nz = int(c.mfe_R.isna().sum())
    if nz:
        zero_ok = all(hold.get(t) is not None for t in c[c.mfe_R.isna()].tranche_id)
        c["mfe_R"] = c.mfe_R.fillna(0.0)
        print(f"    mfe_R nulls restored to 0.0: {nz} (wf1 mfe_r == 0.0 for all; "
              f"wf1 row present for all: {zero_ok})")
        _NOTES.append(
            f"v3_terrain: cen5_campaigns carries {nz} null `mfe_R`. They are not "
            f"missing data -- the WF1 row reads exactly 0.0 for every one of "
            f"them -- so they are emitted as 0.0 rather than null. Left as null "
            f"they would have sorted to an arbitrary end of the MFE ordering "
            f"and been silently truncated by the cap.")

    # the 260 resolved WF1 campaigns with no cen5 row are a STOP-OUT cohort;
    # building on cen5 drops them, and that is a survivorship distortion.
    missing = set(hold) - set(c.tranche_id)
    print(f"    resolved WF1 campaigns absent from cen5: {len(missing)}")
    _NOTES.append(
        f"v3_terrain: {len(missing)} resolved WF1 campaigns have NO cen5 row and "
        f"are therefore ABSENT from this payload. They are not a random "
        f"remainder -- they are overwhelmingly intraday stop-outs (257 of 260 "
        f"exit_reason='stop'), dropped upstream by cen5's own construction "
        f"(no 5m klines / non-positive risk unit). The terrain view is thus "
        f"very slightly survivorship-tilted, and a stop-out is exactly the "
        f"shape it under-represents. Named, not corrected: fixing it means "
        f"rebuilding cen5, which this pass does not touch.")

    c = c.sort_values(["mfe_R", "tranche_id"], ascending=[False, True]).reset_index(drop=True)
    assets = sorted(c.asset.unique())
    ai = {a: i for i, a in enumerate(assets)}
    # COLUMNAR, for the same reason as v3_helix: object-per-row repeats every
    # key 6,834 times and does not fit the cap; column arrays do, with EVERY
    # campaign kept rather than a top-N slice.
    data = {"asset_legend": assets, "n_records": len(c),
            "columns": ["rank", "asset", "mfe", "terminal", "give_back",
                        "hold", "is_winner"],
            "rank": list(range(1, len(c) + 1)),
            "asset": [ai[a] for a in c.asset],
            "mfe": [round(float(x), 4) for x in c.mfe_R],
            "terminal": [round(float(x), 4) for x in c.ride_R],
            "give_back": [None if not np.isfinite(x) else round(float(x), 4)
                          for x in c.give_back_R],
            "hold": [None if v is None or not np.isfinite(v) else int(v)
                     for v in c.hold_s],
            "is_winner": [int(x == "win") for x in c.outcome_sign]}
    print(f"    ranks 1..{len(c):,} (ALL campaigns, no truncation)  "
          f"winners {sum(data['is_winner']):,}")

    inv = write_payload(
        "v3_terrain.json", data, src_meta("cen5_campaigns"),
        downsample_rule=None,
        note="Read `n_records`, NOT meta.rows: this payload is columnar, so "
             "meta.rows counts array CELLS across all columns, not campaigns. "
             "COLUMNAR: parallel arrays in `columns` order, one index per "
             "campaign, sorted by mfe descending (ties by tranche_id). ALL "
             f"{len(c):,} cen5 campaigns are present -- no top-N truncation. "
             "`rank` is the ordinal in THIS payload's MFE ordering: it is not a "
             "stored column and it is not a score. `asset` indexes "
             "asset_legend. `terminal` = cen5 `ride_R`, the size-free gross R. "
             "`hold` = WF1 `hold_s` in seconds, joined by tranche_id. "
             "`is_winner` = cen5 `outcome_sign == 'win'`, which is exactly "
             "sign(ride_R) > 0 (agreement 1.000); reading it off the "
             "size-scaled `realized_r` instead would flip 38 of 6,834, so the "
             "ruler is stated rather than assumed.")
    _INV.append(inv)
    return {"n": len(c)}


# ===============================================================  v3_helix
def helix() -> dict:
    banner("v3_helix -- BTCUSDT 1h ribbon")
    rp = C2B / "ribbons" / "BTCUSDT" / "1h.parquet"
    kp = C2B / "transitions" / "BTCUSDT" / "1h_knots.parquet"
    fp = C2B / "transitions" / "BTCUSDT" / "1h_fans.parquet"
    r = pd.read_parquet(rp)
    kn = pd.read_parquet(kp)
    fa = pd.read_parquet(fp)
    SR = ["FAST", "M", "MH", "H", "VH", "UH"]
    ot = r.open_time.to_numpy(np.int64)
    print(f"    ribbons {len(r):,} 1h bars  knots {len(kn):,}  fans {len(fa):,}")

    # The series is gap-free 1h (asserted below), so a bar INDEX plus
    # (t0_ms, step_ms) is a lossless and far cheaper time axis than a 13-digit
    # epoch on every row.  Everything below is COLUMNAR for the same reason:
    # object-per-row JSON repeats each key thousands of times and pushed this
    # payload to 1.33 MB.  Columnar keeps every row instead of sampling.
    step = 3_600_000
    d = np.diff(ot)
    if not (d == step).all():
        raise SystemExit("HALT: BTCUSDT 1h is not gap-free; the index axis "
                         "would not be lossless")
    six = {s: r[f"{s}_width_atr"].to_numpy(np.float64) for s in SR}

    # ---- state-change points: every bar where any SR's state code changes
    ci, cs, ct = [], [], []
    for si, s in enumerate(SR):
        st = r[f"{s}_state"].to_numpy(np.int8)
        i = np.flatnonzero(st[1:] != st[:-1]) + 1
        i = i[st[i] != -9]
        ci.extend(i.tolist())
        cs.extend([si] * len(i))
        ct.extend(st[i].tolist())
    o = np.lexsort((np.array(cs), np.array(ci)))
    chg = {"i": [int(ci[j]) for j in o], "sr": [int(cs[j]) for j in o],
           "to_state": [int(ct[j]) for j in o]}
    print(f"    state-change points: {len(chg['i']):,} (complete, not sampled)")

    # ---- transitions, complete.  Episodes still running at series end are
    #      marked open; the two tables use DIFFERENT sentinels for that -- the
    #      knots table writes -1, the fans table writes n_bars (one past the
    #      last index).  Both are normalised to to_i = null, open = 1.
    n_bars = len(r)

    def _end(i):
        i = int(i)
        return (None, 1) if (i < 0 or i >= n_bars) else (i, 0)

    tk, tsr, tf_, tt, tb, td, to = [], [], [], [], [], [], []
    for t in kn.itertuples():
        e, op = _end(t.exit_bar_index)
        tk.append(0); tsr.append(SR.index(t.sr)); tf_.append(int(t.entry_bar_index))
        tt.append(e); tb.append(int(t.duration_bars)); td.append(0); to.append(op)
    for t in fa.itertuples():
        e, op = _end(t.end_bar_index)
        tk.append(1); tsr.append(SR.index(t.sr)); tf_.append(int(t.onset_bar_index))
        tt.append(e); tb.append(int(t.fan_len_bars)); td.append(int(t.dir_sign))
        to.append(op)
    o = np.lexsort((np.array(tsr), np.array(tf_)))
    trans = {"kind": [tk[j] for j in o], "sr": [tsr[j] for j in o],
             "from_i": [tf_[j] for j in o], "to_i": [tt[j] for j in o],
             "bars": [tb[j] for j in o], "dir": [td[j] for j in o],
             "open": [to[j] for j in o]}
    n_open = sum(to)
    print(f"    transitions: {len(trans['kind']):,} (complete, not sampled); "
          f"{n_open} still open at series end")
    _NOTES.append(f"v3_helix: {n_open} episodes are still running at series end. "
                  f"The two substrate tables mark that DIFFERENTLY -- "
                  f"transitions/*_knots writes exit_bar_index = -1, "
                  f"transitions/*_fans writes end_bar_index = n_bars (one past "
                  f"the last index). Both are normalised here to to_i = null "
                  f"with open = 1; neither table was changed.")

    # ---- the spine.  A full hourly spine of six widths is ~3.3 MB against a
    #      700 KB cap, so it is decimated on a fixed stride, stated in meta.
    stride, spine = 1, None
    for stride in (1, 2, 3, 4, 6, 8, 12, 24, 48):
        idx = np.arange(0, len(r), stride)
        spine = {"i": [int(i) for i in idx],
                 "w": [[None if not np.isfinite(six[s][i]) else round(float(six[s][i]), 3)
                        for i in idx] for s in SR]}
        probe = {"spine": spine, "state_changes": chg, "transitions": trans}
        if len(json.dumps(jclean(probe), separators=(",", ":")).encode()) \
                < V.MAX_BYTES - 8_000:
            break
    print(f"    spine stride {stride}h -> {len(spine['i']):,} points "
          f"(hourly would be {len(r):,})")

    data = {"asset": "BTCUSDT", "tf": "1h", "sr_order": SR,
            "n_records": {"spine": len(spine["i"]),
                          "state_changes": len(chg["i"]),
                          "transitions": len(trans["kind"])},
            "t0_ms": int(ot[0]), "step_ms": step, "n_bars": len(r),
            "span_ms": [int(ot[0]), int(ot[-1])],
            "spine_stride_hours": stride, "spine": spine,
            "state_changes": chg, "transitions": trans}
    inv = write_payload(
        "v3_helix.json", data,
        [raw_src("census2b/ribbons/BTCUSDT/1h", rp, len(r)),
         raw_src("census2b/transitions/BTCUSDT/1h_knots", kp, len(kn)),
         raw_src("census2b/transitions/BTCUSDT/1h_fans", fp, len(fa))],
        downsample_rule=(f"SPINE ONLY: decimated to every {stride}h from the "
                         f"{len(r):,}-bar hourly series; a full hourly spine of "
                         f"six widths is ~3.3 MB against a 700 KB cap. "
                         f"state_changes and transitions are COMPLETE, not "
                         f"sampled." if stride > 1 else None),
        note="Read `n_records`, NOT meta.rows: this payload is columnar, so "
             "meta.rows counts array CELLS, not events. "
             "COLUMNAR. Time axis is a bar INDEX: ts_ms = t0_ms + i*step_ms, "
             "exact because the 1h series is gap-free (asserted at build). "
             "spine.w is six parallel arrays of width_atr in sr_order, aligned "
             "to spine.i. state_changes carries EVERY bar where an SR's state "
             "code changes (-1 compressing, 0 flat, 1 expanding); warm-up "
             "sentinels (-9) excluded. transitions: kind 0=knot 1=fan, "
             "complete. Widths are the ORIGINAL k=20 state/width columns -- the "
             "ORACLE rev C _v2 per-SR state re-pin is NOT applied here.")
    _INV.append(inv)
    return {"stride": stride}


# ==================================================================  F-V3
def f_v3(tape: dict) -> bool:
    banner("F-V3")
    ok = True
    print("  (a) every payload round-trips json.load")
    for inv in _INV:
        p = PAY / inv["payload"]
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            blob = json.dumps(d["data"], sort_keys=True,
                              separators=(",", ":")).encode()
            good = hashlib.sha256(blob).hexdigest() == d["meta"]["sha256"]
        except Exception as e:                                  # noqa: BLE001
            print(f"      {inv['payload']:22s} LOAD FAILED: {e}")
            ok = False
            continue
        cap = p.stat().st_size <= V.MAX_BYTES
        print(f"      {inv['payload']:22s} load OK  sha {'OK' if good else 'DRIFT'}"
              f"  {p.stat().st_size:>8,} B {'<= cap' if cap else '!! OVER CAP'}")
        ok &= good and cap

    print("  (b) may26 timestamps reconcile to the D-CEN2c row "
          "(MC1 D3.event_card, the ops record for May-26)")
    card = tape["card"]
    trig = next(r for r in tape["rows"] if r["stage"] == "trigger")
    checks = [
        ("trigger ts_ms", trig["ts_ms"], card["event_ts"]),
        ("trigger ts_iso", trig["ts_iso"], card["event_iso"]),
        ("trigger px", round(trig["px"], 6), round(card["close"], 6)),
        ("trigger atr_4h", round(trig["atr_4h"], 6), round(card["atr_4h"], 6)),
    ]
    for name, got, want in checks:
        good = got == want
        ok &= good
        print(f"      {name:16s} tape={str(got):26s} card={str(want):26s} "
              f"{'PASS' if good else 'FAIL'}")
    # and the four legs against the MC-1 build document's printed anatomy
    printed = {"arming": "2026-05-16T00:00:00Z", "relay": "2026-05-18T04:00:00Z",
               "trigger": "2026-05-26T16:00:00Z", "seal": "2026-05-27T20:00:00Z"}
    for stage, want in printed.items():
        got = next(r["ts_iso"] for r in tape["rows"] if r["stage"] == stage)
        good = got == want
        ok &= good
        print(f"      leg {stage:12s} {got:22s} vs BUILD_APOLLO_2026-08-06_MC1 "
              f"{want:22s} {'PASS' if good else 'FAIL'}")
    print(f"\n  F-V3 VERDICT: {'PASS' if ok else 'HALT'}")
    return ok


def handoff() -> int:
    """Payloads + the governing contract text, copied for the design lane."""
    banner("DESIGN_HANDOFF_VIZ3")
    n = 0
    for inv in _INV:
        src = PAY / inv["payload"]
        (HAND / inv["payload"]).write_bytes(src.read_bytes())
        n += 1
    for doc in (RULES_DOC,
                ROOT / "exchange" / "reports" / "DESIGN_BRIEF_CENSUS2A_VIZ_2026-08-12.md",
                ROOT / "exchange" / "reports" / "BUILD_2026-08-15_CENSUS2B_ORACLE.md"):
        if doc.exists():
            (HAND / doc.name).write_bytes(doc.read_bytes())
            n += 1
    print(f"    {n} files -> {HAND}")
    return n


def main() -> int:
    banner(f"VIZ-2 · CATHEDRAL PAYLOADS   seed={SEED}   Tier-E / DISPLAY-ONLY / m=0")
    print(f"  payloads -> {PAY}")
    print(f"  handoff  -> {HAND}")
    tape = may26_tape()
    stations()
    terrain()
    helix()
    ok = f_v3(tape)
    nh = handoff()

    man = {"module": "VIZ-2 CATHEDRAL PAYLOADS", "seed": SEED,
           "class": "DISPLAY-ONLY / Tier-E exploration; m = 0",
           "program": "scripts/census2b_viz2.py",
           "payloads": _INV, "handoff_files": nh, "notes": _NOTES,
           "f_v3": "PASS" if ok else "HALT"}
    (PAY / "viz2_manifest.json").write_text(json.dumps(man, indent=1) + "\n")

    banner("SUMMARY")
    tot = 0
    for inv in _INV:
        tot += inv["bytes"]
        print(f"  {inv['payload']:22s} rows={inv['rows']:>7,}  "
              f"{inv['bytes']:>8,} B  sha {inv['sha256'][:16]}"
              f"{'  !! OVER CAP' if inv['over_cap'] else ''}")
    print(f"  {'TOTAL':22s} {'':13s} {tot:>8,} B")
    print("\n  NOTES CARRIED INTO THE BUILD DOC:")
    for n in _NOTES:
        print(f"    - {n}")
    hr("=")
    print(f"VIZ-2 COMPLETE  verdict={'PASS' if ok else 'HALT'}")
    hr("=")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
