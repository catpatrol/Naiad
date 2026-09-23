#!/usr/bin/env python
"""TIER-C10 · CLOSE §3 — THE STAGE D MANIFEST, incl. the F-D-4 / F-D-5 tables.

THE CLAUSE THIS FILE DISCHARGES (contract of record
exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md, CLOSE, line 135):

    · Stage D manifest incl. the F-D-4 / F-D-5 tables

WHAT IT WRITES (and nothing else)
  research_outputs/tierc10/close/S3_STAGE_D.md          the CLOSE section
  research_outputs/tierc10/close/FIXTURES_CLOSE_stage_d.txt   its fixture transcript

WHAT IT DOES
  · SPLICES, BYTE-EXACT BY HEADING SPAN, nine sections of
    research_outputs/tierc10/data/STAGE_D_MANIFEST.md — Venue of record,
    Admission, Contract multipliers, F-D-4 (two-token trap), F-D-5 (data-spend
    audit), the tiered haircut twin, As-of hazards, the publications-disagree
    summary (its lead paragraph + the per-lens "which publication each file
    carries" table) and Operator rulings needed at CLOSE.  A span runs from its
    heading line to the next heading of the same or a higher level ("section")
    or to the next heading of any level ("lead").  Nothing in a span is
    re-worded or re-computed; each span is fenced by HTML-comment markers that
    carry its byte range and sha256 so F-S3-SLICE can re-extract and compare.
  · ADDS a compact per asset x lens table of STAGE_D_MANIFEST.json files[]
    (all 119 entries: 102 kline cells + 17 funding files — every grid whole):
    bars as-of, first / last as-of open, rows past the pin (counted, never
    read), gaps, sha256[:16], and a RE-MEASURED column — the bars are re-read
    through tierc10_data.load_asof (funding through load_funding_asof), the
    file re-hashed, the gaps re-counted.
  · PRINTS F-D-1 AS RED with its operator question.  The status is DERIVED
    from the filed ONLINE Stage D transcript (its "[FAIL] F-D-1" line and its
    FIXTURE SUMMARY), never typed; this build reaches no venue, so F-D-1 is
    also NOT RUN here.
  · RE-HASHES the 15 D-CORE artifacts against their PROGRESS.json record.

REPORT-ONLY · Tier-E.  Nothing here scores, runs a card, consults a
registration's verdict, or imports a scoring / registration module (the
closure leg proves it).  Bars are read ONLY through tierc10_data.load_asof —
never tierc2_baseline.load_klines, which reads the whole file and would pass the
pin on the 5m tapes that hold rows stamped after it.

PREAMBLE (RUN / HALT) — checked before anything is read or written:
  substrate: NAIAD_CACHE_DIR == the TC10 snapshot (never the live cache) ·
  PYTHONDONTWRITEBYTECODE=1 · every input present · the contract of record
  re-hashes to PROGRESS.json contract_of_record and its line 135 carries the
  clause · ONE corridor (AS_OF_PIN == manifest == PROGRESS as_of_of_record,
  close_ms included) · manifest complete, live cache untouched · the D-CORE
  ledger record holds 15 artifacts · every input this file reads that the
  D-CORE record names (the manifest .md/.json, the audit, the pin, both filed
  Stage D transcripts) re-hashes to that record.  Any miss prints
  "PREAMBLE: HALT", writes NOTHING and exits 1 (the family's RUN/HALT
  convention: 0 every leg GREEN · 1 a leg RED or a HALT).

FIXTURE LEGS (each states FAILS IF; each carries planted violations that must
go RED, judged ONE PLANT AT A TIME, every plant on a COPY — no repo file and no
snapshot file is ever written by a plant):
  F-S3-SLICE    FAILS IF a spliced span in S3 differs by one byte from its
                heading span in STAGE_D_MANIFEST.md, a span is missing, or a
                marker's recorded byte range / sha disagrees.
  F-S3-D4       FAILS IF the F-D-4 cell count or pre-floor count printed in S3
                (the tally line AND the spliced sentence) differs from
                STAGE_D_MANIFEST.json two_token_trap, from a recount of its own
                rows, or from a re-measure of the tapes through load_asof.
  F-S3-D5       FAILS IF the class counts printed in S3 differ from
                DATA_SPEND_AUDIT.json counts, from a recount of its rows, from
                its class lists, or from the manifest's data_spend block.
  F-S3-SHA      FAILS IF any of the 15 D-CORE artifacts does not re-hash (sha256
                and byte count) to its PROGRESS.json record, the record does not
                hold exactly 15, a spliced source is not among them, or S3
                prints a sha16 other than the recorded one.
  F-S3-RED      FAILS IF F-D-1 is printed as anything but RED / NOT RUN, or its
                operator question is not printed.
  F-S3-TABLE    FAILS IF the per asset x lens table is not whole (119 rows, in
                files[] order), any printed cell differs from files[], or any
                re-measure (load_asof count / first / last / gaps, file re-hash)
                differs from files[].
  F-S3-CLOSURE  FAILS IF a scoring / registration / range module or the
                whole-file kline loader is imported at run time, or this file's
                own code imports or calls one.
  F-DET         FAILS IF two independent builds of S3 are not byte-identical,
                or S3 / the transcript carries a temp path.

Run:
  export NAIAD_CACHE_DIR=/Users/luis/.cache/naiad/snapshots/tc10_20260921 PYTHONDONTWRITEBYTECODE=1
  ~/venvs/naiad/bin/python scripts/tierc10_close_close_stage_d.py
Exit: 0 every leg GREEN · 1 a leg RED or a PREAMBLE HALT (a HALT writes nothing).
"""
from __future__ import annotations

import ast
import calendar
import copy
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF_REL = "scripts/tierc10_close_close_stage_d.py"
SNAPSHOT = Path.home() / ".cache" / "naiad" / "snapshots" / "tc10_20260921"
LIVE_CACHE = Path.home() / ".cache" / "naiad" / "data_cache"

TC10_REL = "research_outputs/tierc10"
DATA_REL = f"{TC10_REL}/data"
MANIFEST_MD_REL = f"{DATA_REL}/STAGE_D_MANIFEST.md"
MANIFEST_JSON_REL = f"{DATA_REL}/STAGE_D_MANIFEST.json"
SPEND_REL = f"{DATA_REL}/DATA_SPEND_AUDIT.json"
PIN_REL = f"{DATA_REL}/AS_OF_PIN.json"
FILED_ONLINE_REL = f"{DATA_REL}/FIXTURES_STAGE_D.txt"
FILED_OFFLINE_REL = f"{DATA_REL}/FIXTURES_STAGE_D_OFFLINE.txt"
PROGRESS_REL = f"{TC10_REL}/PROGRESS.json"
RULINGS_REL = f"{TC10_REL}/OPERATOR_RULINGS.md"
CONTRACT_REL = "exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md"
CONTRACT_LINE = 135
CONTRACT_CLAUSE = "Stage D manifest incl. the F-D-4 / F-D-5 tables"
OUT_MD_REL = f"{TC10_REL}/close/S3_STAGE_D.md"
OUT_FIX_REL = f"{TC10_REL}/close/FIXTURES_CLOSE_stage_d.txt"
DCORE = "D-CORE"
DCORE_ARTIFACTS = 15

# (id, heading-line prefix, mode) — the auditor's nine sections, in print order.
# "section": to the next heading of the same or a higher level.
# "lead":    to the next heading of ANY level (the section's own lead text).
SPLICES = (
    ("venue", "## Venue of record", "section"),
    ("admission", "## Admission", "section"),
    ("multipliers", "## Contract multipliers", "section"),
    ("fd4", "## The two-token trap", "section"),
    ("fd5", "## Data-spend audit", "section"),
    ("haircut", "## The tiered costs haircut twin", "section"),
    ("asof", "## As-of hazards for downstream loaders", "section"),
    ("pubs_lead", "## The venue's two publications disagree", "lead"),
    ("pubs_carries", "### Which publication each native file carries", "section"),
    ("rulings", "## Operator rulings needed at CLOSE", "section"),
)
CLASSES = ("never-touched", "display-only", "scored")
LENS_ORDER = ("5m", "1h", "4h", "12h", "1d", "1w", "funding")
FORBIDDEN_MODULES = ("tierc10_panel", "tierc10_score", "tierc10_lanes", "tierc10_brk",
                     "tierc10_file_registrations", "tierc10_census", "tierc10_stamps",
                     "tierc10_null", "tierc2_baseline", "engine.rangefinder",
                     "analytics.rangefinder")
FORBIDDEN_CALLS = ("load_klines", "read_parquet", "score", "finish_family", "register")
TEMP_TOKENS = ("/var/folders/", "/private/var/", "/tmp/")
FMT = "%Y-%m-%dT%H:%M:%SZ"


class Halt(Exception):
    pass


# ---------------------------------------------------------------- small helpers
def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def iso_to_ms(s: str) -> int:
    return calendar.timegm(time.strptime(s, FMT)) * 1000


def tilde(p: Path) -> str:
    s = str(p)
    home = str(Path.home())
    return "~" + s[len(home):] if s.startswith(home) else s


def md_cell(s: str) -> str:
    return str(s).replace("|", "\\|")


# ---------------------------------------------------------------- the preamble
def preamble(root: Path) -> tuple[list[tuple[bool, str]], dict]:
    """RUN / HALT, before any bar is read or any file written."""
    checks: list[tuple[bool, str]] = []
    ctx: dict = {}
    env = os.environ.get("NAIAD_CACHE_DIR", "")
    got = Path(env).expanduser().resolve() if env else None
    sub_ok = bool(env) and got != LIVE_CACHE.resolve() and got == SNAPSHOT.resolve() \
        and (SNAPSHOT / "klines").is_dir()
    checks.append((sub_ok, f"substrate: NAIAD_CACHE_DIR == {tilde(SNAPSHOT)} (the TC10 snapshot; "
                           f"the live cache {tilde(LIVE_CACHE)} is READ-NEVER) — "
                           f"{'holds' if sub_ok else 'NOT the snapshot / unset / the live cache'}"))
    pyc = os.environ.get("PYTHONDONTWRITEBYTECODE", "") == "1"
    checks.append((pyc, f"PYTHONDONTWRITEBYTECODE=1 — {'set' if pyc else 'NOT set'}"))
    need = (MANIFEST_MD_REL, MANIFEST_JSON_REL, SPEND_REL, PIN_REL, FILED_ONLINE_REL,
            FILED_OFFLINE_REL, PROGRESS_REL, RULINGS_REL, CONTRACT_REL)
    missing = [r for r in need if not (root / r).is_file()]
    checks.append((not missing, f"inputs present: {len(need) - len(missing)}/{len(need)}"
                                + (f" — MISSING {missing}" if missing else "")))
    if missing:
        return checks, ctx
    prog = json.loads((root / PROGRESS_REL).read_text())
    man = json.loads((root / MANIFEST_JSON_REL).read_text())
    pin = json.loads((root / PIN_REL).read_text())
    csha = sha256_file(root / CONTRACT_REL)
    crec = (prog.get("contract_of_record") or {})
    lines = (root / CONTRACT_REL).read_text().splitlines()
    cline = lines[CONTRACT_LINE - 1] if len(lines) >= CONTRACT_LINE else ""
    c_ok = crec.get("path") == CONTRACT_REL and crec.get("sha256") == csha and CONTRACT_CLAUSE in cline
    checks.append((c_ok, f"contract of record {CONTRACT_REL} sha256 {csha[:16]} "
                         f"{'==' if crec.get('sha256') == csha else '!='} PROGRESS.json contract_of_record; "
                         f"line {CONTRACT_LINE} {'carries' if CONTRACT_CLAUSE in cline else 'LACKS'} "
                         f"'{CONTRACT_CLAUSE}'"))
    a = (pin.get("as_of_last_closed_4h"), man.get("as_of_last_closed_4h"), prog.get("as_of_of_record"))
    c = (pin.get("as_of_last_closed_4h_close_ms"), man.get("as_of_last_closed_4h_close_ms"),
         prog.get("as_of_last_closed_4h_close_ms"))
    one = len(set(a)) == 1 and len(set(c)) == 1 and a[0] is not None
    checks.append((one, f"ONE corridor: AS_OF_PIN / manifest / PROGRESS as_of = {list(a)}, "
                        f"close_ms = {list(c)}"))
    comp = man.get("complete") is True and man.get("live_cache_touched") is False \
        and prog.get("live_cache_touched") is False
    checks.append((comp, f"manifest complete: {man.get('complete')} · live cache touched "
                         f"(manifest / PROGRESS): {man.get('live_cache_touched')} / "
                         f"{prog.get('live_cache_touched')}"))
    recs = [s for s in prog.get("stages", []) if s.get("stage") == DCORE]
    rec = recs[0] if len(recs) == 1 else None
    r_ok = rec is not None and rec.get("artifact_count") == DCORE_ARTIFACTS \
        and len(rec.get("artifact_shas", {})) == DCORE_ARTIFACTS
    checks.append((r_ok, f"PROGRESS.json {DCORE} record: {len(recs)} found; artifact_count "
                         f"{rec.get('artifact_count') if rec else None}, recorded shas "
                         f"{len(rec.get('artifact_shas', {})) if rec else None} (need {DCORE_ARTIFACTS})"))
    if rec is not None:
        read = (MANIFEST_MD_REL, MANIFEST_JSON_REL, SPEND_REL, PIN_REL, FILED_ONLINE_REL,
                FILED_OFFLINE_REL)
        shas = rec.get("artifact_shas", {})
        bad = [r for r in read if r not in shas or sha256_file(root / r) != shas[r]["sha256"]]
        checks.append((not bad, f"inputs read vs the {DCORE} record: "
                                f"{len(read) - len(bad)}/{len(read)} re-hash to PROGRESS.json"
                                + (f" — DIFFER / UNRECORDED {bad}" if bad else "")))
    ctx.update(contract_sha=csha, contract_line=cline)
    return checks, ctx


# ---------------------------------------------------------------- inputs
def load_inputs(root: Path) -> dict:
    prog = json.loads((root / PROGRESS_REL).read_text())
    rec = [s for s in prog["stages"] if s.get("stage") == DCORE][0]
    lines = (root / CONTRACT_REL).read_text().splitlines()
    return {
        "md": (root / MANIFEST_MD_REL).read_bytes(),
        "man": json.loads((root / MANIFEST_JSON_REL).read_text()),
        "spend": json.loads((root / SPEND_REL).read_text()),
        "dcore": rec,
        "as_of_of_record": prog["as_of_of_record"],
        "contract_sha": sha256_file(root / CONTRACT_REL),
        "contract_line": lines[CONTRACT_LINE - 1],
        "rulings": (root / RULINGS_REL).read_text(),
        "online": (root / FILED_ONLINE_REL).read_text(),
        "offline": (root / FILED_OFFLINE_REL).read_text(),
    }


# ---------------------------------------------------------------- spans (extractor A: regex)
def heading_spans_regex(md: bytes) -> list[tuple[int, int, bytes]]:
    return [(m.start(), len(m.group(1)), m.group(0))
            for m in re.finditer(rb"^(#{1,6}) [^\n]*", md, re.M)]


def span_of(md: bytes, prefix: str, mode: str) -> tuple[int, int, str]:
    hs = heading_spans_regex(md)
    pre = prefix.encode()
    hits = [i for i, h in enumerate(hs) if h[2].startswith(pre)]
    if len(hits) != 1:
        raise Halt(f"heading prefix {prefix!r} matched {len(hits)} headings (need exactly 1)")
    i = hits[0]
    start, lvl, line = hs[i]
    end = len(md)
    for s2, l2, _ in hs[i + 1:]:
        if mode == "lead" or l2 <= lvl:
            end = s2
            break
    return start, end, line.decode()


# ---------------------------------------------------------------- spans (extractor B: line walk, for the check)
def span_by_walk(md: bytes, prefix: str, mode: str) -> tuple[int, int] | None:
    pos, heads = 0, []
    for raw in md.split(b"\n"):
        n = len(raw) + 1
        stripped = raw.lstrip(b"#")
        lvl = len(raw) - len(stripped)
        if 1 <= lvl <= 6 and stripped.startswith(b" "):
            heads.append((pos, lvl, raw))
        pos += n
    hits = [k for k, h in enumerate(heads) if h[2].decode().startswith(prefix)]
    if len(hits) != 1:
        return None
    k = hits[0]
    start, lvl, _ = heads[k]
    end = len(md)
    for s2, l2, _ in heads[k + 1:]:
        if mode == "lead" or l2 <= lvl:
            end = s2
            break
    return start, end


# ---------------------------------------------------------------- measurement (bars through load_asof ONLY)
def f_d4_floors(man: dict) -> dict:
    out = {}
    for r in man["two_token_trap"]["rows"]:
        for lens, pl in r["per_lens"].items():
            out[(r["asset"], lens)] = iso_to_ms(pl["floor_open"])
    return out


def frame_stats(D, t, lens: str, floor_ms: int | None) -> dict:
    """Pure: stats of an ascending open_time array (int ms)."""
    import numpy as np
    n = int(len(t))
    rec = {"n": n, "first": D.iso(int(t[0])) if n else None, "last": D.iso(int(t[-1])) if n else None}
    if lens != "funding":
        step = int(D.STEP_MS[lens])
        dt = np.diff(t) if n > 1 else np.array([], dtype=np.int64)
        rec["gaps"] = int((dt > step).sum())
        rec["missing"] = int(((dt[dt > step] // step) - 1).sum()) if len(dt) else 0
        rec["pre_floor"] = int((t < floor_ms).sum()) if floor_ms is not None else None
    return rec


def measure(D, man: dict, snapshot: Path) -> list[dict]:
    floors = f_d4_floors(man)
    out = []
    for f in man["files"]:
        p = snapshot / f["path"]
        if f["kind"] == "klines":
            d = D.load_asof(f["stem"], f["as_of_lens"])
            t = d["open_time"].to_numpy()
            rec = frame_stats(D, t, f["as_of_lens"], floors.get((f["asset"], f["as_of_lens"])))
        else:
            d = D.load_funding_asof(f["stem"])
            t = d["funding_time"].to_numpy()
            rec = frame_stats(D, t, "funding", None)
        rec["sha"] = sha256_file(p)
        out.append(rec)
    return out


def cell_expect(f: dict) -> dict:
    if f["kind"] == "klines":
        return {"lens": f["as_of_lens"], "n": f["rows_as_of"], "first": f["first_open"],
                "last": f["as_of_last_closed_bar_open"], "after": f["rows_after_as_of"],
                "gaps": f"{f['gap_count']} ({f['missing_bars_total']})", "sha16": f["sha256"][:16]}
    return {"lens": "funding", "n": f["rows"] - f["rows_after_as_of"], "first": f["first"],
            "last": f["last"], "after": f["rows_after_as_of"],
            "gaps": "— (coverage " + ("OK" if f["coverage"]["ok"] else "FAULT") + ")",
            "sha16": f["sha256"][:16]}


def cell_faults(f: dict, r: dict) -> list[str]:
    e = cell_expect(f)
    bad = []
    if f["kind"] == "klines":
        if f["complete_to_as_of"] is not True:
            bad.append("complete_to_as_of is not True")
        if r.get("gaps") != f["gap_count"]:
            bad.append(f"gaps {r.get('gaps')} != {f['gap_count']}")
        if r.get("missing") != f["missing_bars_total"]:
            bad.append(f"missing {r.get('missing')} != {f['missing_bars_total']}")
    elif f["rows_after_as_of"] != 0:
        bad.append("funding rows past the pin: the filed 'last' is not an as-of edge")
    if r["n"] != e["n"]:
        bad.append(f"bars {r['n']} != {e['n']}")
    if r["first"] != e["first"]:
        bad.append(f"first {r['first']} != {e['first']}")
    if r["last"] != e["last"]:
        bad.append(f"last {r['last']} != {e['last']}")
    if r["sha"] != f["sha256"]:
        bad.append(f"re-hash {r['sha'][:16]} != {f['sha256'][:16]}")
    return bad


# ---------------------------------------------------------------- F-D-1 status (derived, never typed)
def fd1_status(online: str, offline: str) -> dict:
    lines = online.splitlines()
    fail = [(i, l) for i, l in enumerate(lines, 1) if l.lstrip().startswith("[FAIL] F-D-1:")]
    pas = [(i, l) for i, l in enumerate(lines, 1) if l.lstrip().startswith("[PASS] F-D-1:")]
    summ = [l for l in lines if l.startswith("FIXTURE SUMMARY")]
    failed = []
    if summ:
        m = re.search(r"(\{.*\})\s*$", summ[-1])
        failed = json.loads(m.group(1)).get("failed", []) if m else []
    off_summ = [l for l in offline.splitlines() if l.startswith("FIXTURE SUMMARY")]
    off_not_run = []
    if off_summ:
        m = re.search(r"(\{.*\})\s*$", off_summ[-1])
        off_not_run = json.loads(m.group(1)).get("not_run", []) if m else []
    off_line = [i for i, l in enumerate(offline.splitlines(), 1)
                if l.startswith("F-D-1 — ")]
    if fail and not pas and "F-D-1" in failed:
        status = "RED"
    elif pas and not fail:
        status = "GREEN"
    else:
        status = "UNDETERMINED"
    n_differ, differing = None, []
    if fail:
        m = re.search(r"\((\d+) differ\)", fail[0][1])
        n_differ = int(m.group(1)) if m else None
        differing = re.findall(r"'(\S+ \S+ \d{4}-\d\d-\d\dT[\d:]+Z):", fail[0][1])
    return {"status": status, "fail_line": fail[0][0] if fail else None,
            "n_differ": n_differ, "differing": differing, "summary_failed": failed,
            "offline_not_run": "F-D-1" in off_not_run,
            "offline_line": off_line[0] if off_line else None}


def rulings_bits(text: str) -> dict:
    m5 = re.search(r"^> 5- (.+)\n> (.+)$", text, re.M)
    m6 = re.search(r"^> 6- (.+)\n> (.+)$", text, re.M)
    lines = text.splitlines()
    idx = [i for i, l in enumerate(lines) if l.startswith("- **F-D-1 / R5.**")]
    blocked, span = None, None
    if idx:
        i = idx[0]
        j = i + 1
        while j < len(lines) and lines[j].startswith("  "):
            j += 1
        blocked = " ".join(x.strip() for x in lines[i:j])
        blocked = blocked[2:] if blocked.startswith("- ") else blocked
        span = (i + 1, j)
    return {"r5_q": m5.group(1) if m5 else None, "r5_a": m5.group(2) if m5 else None,
            "r6_q": m6.group(1) if m6 else None, "r6_a": m6.group(2) if m6 else None,
            "blocked": blocked, "blocked_span": span}


# ---------------------------------------------------------------- rendering
LABEL = "REPORT-ONLY · Tier-E"


def render(I: dict, meas: list[dict], fd1: dict, root: Path, volatile: str = "") -> bytes:
    man, spend, md, rec = I["man"], I["spend"], I["md"], I["dcore"]
    tt = man["two_token_trap"]
    out: list[str] = []
    w = out.append
    hz = man["as_of_hazards"]["kline_files_holding_rows_after_as_of"]
    w("# TIER-C10 · CLOSE §3 · STAGE D MANIFEST — incl. the F-D-4 / F-D-5 tables\n\n")
    w(f"**AS OF** `{man['as_of_last_closed_4h']}` (last closed 4h bar: open "
      f"`{man['as_of_last_closed_4h_open']}`) · seed {man['seed']} · ONE corridor: "
      f"`{PIN_REL}` == `{MANIFEST_JSON_REL}` == `{PROGRESS_REL}` as_of_of_record "
      f"`{I['as_of_of_record']}`\n\n")
    w(f"> {man['warranty']}\n\n")
    w(f"**{LABEL}.** This section DESCRIBES the data of record. It scores nothing, runs no "
      f"card, consults no registration's verdict, and reads bars only through "
      f"`tierc10_data.load_asof` (funding through `load_funding_asof`) — never "
      f"`tierc2_baseline.load_klines`, whose whole-file read would pass the pin on the "
      f"{len(hz)} kline files that hold rows stamped after it. Every table below is "
      f"labelled so.\n\n")
    w(f"Contract of record `{CONTRACT_REL}` (sha256 `{I['contract_sha'][:16]}`, == "
      f"PROGRESS.json contract_of_record), line {CONTRACT_LINE}: "
      f"“{I['contract_line'].strip()}”\n\n")
    w(f"Generator `{SELF_REL}` · transcript `{OUT_FIX_REL}` · spliced source "
      f"`{MANIFEST_MD_REL}` (sha256 `{sha256_bytes(md)[:16]}`)\n\n")
    if volatile:
        w(volatile + "\n\n")

    # ---- status
    w("## S3 · STATUS — F-D-1 is RED; D-CORE stays PARTIAL on it\n\n")
    w(f"*{LABEL} · status carried from filed transcripts and the ledger; this CLOSE build "
      f"reaches no venue.*\n\n")
    w("| item | source | reads |\n|---|---|---|\n")
    w(f"| D-CORE ledger status | `{PROGRESS_REL}` stages[{DCORE}].status | "
      f"**{rec['status']}** ({rec['artifact_count']} artifacts) |\n")
    diff_txt = ", ".join(fd1["differing"]) if fd1["differing"] else "—"
    fl = fd1["fail_line"]
    w(f"| F-D-1, filed ONLINE run | `{FILED_ONLINE_REL}`"
      f"{':' + str(fl) if fl else ''} | "
      f"{'`[FAIL]` — ' + str(fd1['n_differ']) + ' bar(s) differ: ' + md_cell(diff_txt) if fl else 'no [FAIL] line'}"
      f"; FIXTURE SUMMARY failed = {md_cell(json.dumps(fd1['summary_failed']))} |\n")
    ol = fd1["offline_line"]
    w(f"| F-D-1, filed OFFLINE run | `{FILED_OFFLINE_REL}`{':' + str(ol) if ol else ''} | "
      f"{'`[NOT RUN]` (listed in not_run)' if fd1['offline_not_run'] else 'not listed as NOT RUN'} |\n")
    w(f"| F-D-1, this CLOSE build | `{SELF_REL}` | NOT RUN — no venue reach |\n\n")
    status_word = {"RED": "**RED**", "GREEN": "**GREEN**"}.get(fd1["status"], "**UNDETERMINED**")
    w(f"F-D-1 STATUS: {status_word} (derived from the filed ONLINE transcript) · **NOT RUN** "
      f"in this CLOSE build\n\n")
    q = man["operator_rulings_needed"][0] if man.get("operator_rulings_needed") else ""
    w(f"OPERATOR QUESTION: {q}\n\n")
    rb = I["rulings_bits"]
    if rb["r5_q"]:
        w(f"Ruling on the record (`{RULINGS_REL}`, verbatim): “{rb['r5_q']}” — “{rb['r5_a']}”. "
          f"It names the pair and permits the venue; it does not choose between the venue's "
          f"REST API and its BULK ARCHIVE.\n\n")
    if rb["blocked"]:
        a, b = rb["blocked_span"]
        w(f"Still blocked (`{RULINGS_REL}`:{a}–{b}, lines joined): {rb['blocked']}\n\n")

    # ---- D-CORE artifacts
    w(f"## S3 · D-CORE artifacts — {len(rec['artifact_shas'])} re-hashed against "
      f"PROGRESS.json\n\n")
    w(f"*{LABEL} · every artifact the {DCORE} ledger record names, re-hashed from disk "
      f"(sha256 and bytes).*\n\n")
    w("| artifact | bytes | sha256[:16] | re-hash |\n|---|---:|---|---|\n")
    for rel, r in rec["artifact_shas"].items():
        p = root / rel
        ok = p.is_file() and p.stat().st_size == r["bytes"] and sha256_file(p) == r["sha256"]
        w(f"| `{rel}` | {r['bytes']} | `{r['sha256'][:16]}` | {'MATCH' if ok else 'MISMATCH'} |\n")
    w("\n")

    def splice(sid: str, prefix: str, mode: str) -> None:
        a, b, line = span_of(md, prefix, mode)
        body = md[a:b]
        w(f"*{LABEL} · spliced BYTE-EXACT from `{MANIFEST_MD_REL}`, heading span "
          f"«{line}» ({mode}), bytes [{a}, {b}), sha256 `{sha256_bytes(body)[:16]}` — "
          f"not re-worded, not re-computed.*\n\n")
        w(f"<!-- S3-SPLICE BEGIN id={sid} mode={mode} src={MANIFEST_MD_REL} bytes=[{a},{b}) "
          f"sha256={sha256_bytes(body)} -->\n")
        w(body.decode("utf-8"))
        if not body.endswith(b"\n"):
            w("\n")
        w(f"<!-- S3-SPLICE END id={sid} -->\n\n")

    sp = {s[0]: s for s in SPLICES}
    splice(*sp["venue"])
    splice(*sp["admission"])

    # ---- the per asset x lens table
    files = man["files"]
    nk = sum(1 for f in files if f["kind"] == "klines")
    nf = len(files) - nk
    w(f"## S3 · Per asset × lens — STAGE_D_MANIFEST.json files[], whole ({len(files)} = "
      f"{nk} kline cells + {nf} funding files)\n\n")
    w(f"*{LABEL} · printed from `{MANIFEST_JSON_REL}` files[]. RE-MEASURED = the bars "
      f"re-read through `tierc10_data.load_asof` (funding: `load_funding_asof`) and their "
      f"count, first / last open and gaps compared to the filed row, the file re-hashed "
      f"against its filed sha256. Rows past the pin are COUNTED from the manifest, never "
      f"read.*\n\n")
    w("<!-- S3-TABLE BEGIN id=cells -->\n")
    w("| asset | stem | lens | bars as-of | first open | last as-of open | past the pin | "
      "gaps (missing) | sha256[:16] | re-measured |\n")
    w("|---|---|---|---:|---|---|---:|---|---|---|\n")
    for f, r in zip(files, meas):
        e = cell_expect(f)
        bad = cell_faults(f, r)
        w(f"| {f['asset']} | {f['stem']} | {e['lens']} | {e['n']} | {e['first']} | {e['last']} | "
          f"{e['after']} | {e['gaps']} | `{e['sha16']}` | "
          f"{'OK' if not bad else 'DIFF: ' + md_cell('; '.join(bad))} |\n")
    w("<!-- S3-TABLE END id=cells -->\n\n")

    splice(*sp["multipliers"])
    splice(*sp["fd4"])

    # ---- F-D-4 tally
    tape_cells = sum(1 for f in files if f["kind"] == "klines")
    tape_pre = sum(r.get("pre_floor") or 0 for f, r in zip(files, meas) if f["kind"] == "klines")
    w("## S3 · F-D-4 tally\n\n")
    w(f"*{LABEL} · read from `{MANIFEST_JSON_REL}` two_token_trap; the re-measure re-reads "
      f"every kline cell through `load_asof` and counts bars opening before that cell's filed "
      f"floor_open.*\n\n")
    w(f"F-D-4 TALLY: cells checked **{tt['cells_checked']}** ({tt['assets']} assets × "
      f"{len(tt['lenses'])} lenses) · bars before a floor **{len(tt['bars_before_a_floor'])}** · "
      f"intended asset confirmed **{tt['intended_asset_confirmed']} / {tt['assets']}** · "
      f"hard-floored every lens **{tt['all_hard_floored']}** · floor bars rebuilt from 5m "
      f"**{tt['floor_bars_rebuilt_from_5m']}** · floor seams that exist "
      f"**{tt['floor_seams_that_exist']}** · discontinuous floor seams "
      f"**{len(tt['discontinuous_floor_seams'])}**\n\n")
    w(f"F-D-4 RE-MEASURED: cells **{tape_cells}** · bars before a floor **{tape_pre}**\n\n")
    rej = "; ".join(f"{x['asset']} `{x['rejected_symbol']}` — {x['reason']}"
                    for x in tt["rejections_carried"])
    w(f"Rejections carried: {rej}\n\n")

    splice(*sp["fd5"])

    # ---- F-D-5 tally
    cnt = spend["counts"]
    w("## S3 · F-D-5 tally\n\n")
    w(f"*{LABEL} · read from `{SPEND_REL}` counts / classes.*\n\n")
    w("F-D-5 COUNTS: " + " · ".join(f"{c} **{cnt[c]}**" for c in CLASSES)
      + f" · assets **{len(spend['rows'])}**\n\n")
    w("| class | count | assets |\n|---|---:|---|\n")
    for c in CLASSES:
        w(f"| {c} | {cnt[c]} | {' '.join(spend['classes'][c])} |\n")
    w(f"\nNEVER-TOUCHED (P-GEN-1's second LOAO panel): **{' '.join(spend['never_touched'])}**\n\n")

    splice(*sp["haircut"])
    splice(*sp["asof"])
    w(f"*{LABEL} · the publications-disagree SUMMARY is the section's lead and its per-lens "
      f"table; the whole-history audit tables stay in `{MANIFEST_MD_REL}` and "
      f"`{man['venue_publications_disagree']['artifact']}` / "
      f"`{man['venue_publications_disagree']['archive_artifact']}`.*\n\n")
    splice(*sp["pubs_lead"])
    splice(*sp["pubs_carries"])
    splice(*sp["rulings"])

    if rb["r6_q"]:
        w("## S3 · Beside the rulings needed — what the operator already said\n\n")
        w(f"*{LABEL} · verbatim from `{RULINGS_REL}`, printed beside item 4 above; no "
          f"inference is drawn from it here.*\n\n")
        w(f"- R6 “{rb['r6_q']}” — “{rb['r6_a']}”. No destination is named in that text.\n\n")
    return "".join(out).encode("utf-8")


# ---------------------------------------------------------------- checks (pure)
BEGIN_RE = re.compile(rb"<!-- S3-SPLICE BEGIN id=(\w+) mode=(\w+) src=(\S+) "
                      rb"bytes=\[(\d+),(\d+)\) sha256=([0-9a-f]{64}) -->\n")


def check_slice(s3: bytes, md: bytes) -> tuple[list[str], int, int]:
    faults: list[str] = []
    found: dict[str, bytes] = {}
    total = 0
    for m in BEGIN_RE.finditer(s3):
        sid = m.group(1).decode()
        end_tok = f"<!-- S3-SPLICE END id={sid} -->".encode()
        e = s3.find(end_tok, m.end())
        if e < 0:
            faults.append(f"{sid}: no END marker")
            continue
        body = s3[m.end():e]
        if sid in found:
            faults.append(f"{sid}: spliced twice")
        found[sid] = body
        want = {s[0]: s for s in SPLICES}.get(sid)
        if want is None:
            faults.append(f"{sid}: not a span of record")
            continue
        sp = span_by_walk(md, want[1], want[2])
        if sp is None:
            faults.append(f"{sid}: heading {want[1]!r} not found exactly once in the manifest")
            continue
        a, b = sp
        src = md[a:b]
        total += len(src)
        if body != src:
            k = next((i for i in range(min(len(body), len(src))) if body[i] != src[i]),
                     min(len(body), len(src)))
            faults.append(f"{sid}: differs from the manifest span at byte {k} "
                          f"(S3 {len(body)} B vs manifest {len(src)} B)")
        if (int(m.group(4)), int(m.group(5))) != (a, b):
            faults.append(f"{sid}: marker range [{m.group(4).decode()},{m.group(5).decode()}) "
                          f"!= manifest span [{a},{b})")
        if m.group(6).decode() != sha256_bytes(src):
            faults.append(f"{sid}: marker sha != sha of the manifest span")
    for sid, _, _ in SPLICES:
        if sid not in found:
            faults.append(f"{sid}: span MISSING from S3")
    return faults, len(found), total


def _grab(pattern: str, text: str) -> list[str]:
    return re.findall(pattern, text, re.M)


def check_d4(s3: str, man: dict, meas: list[dict] | None) -> list[str]:
    tt = man["two_token_trap"]
    faults = []
    j_cells, j_pre = tt["cells_checked"], len(tt["bars_before_a_floor"])
    r_cells = sum(len(r["per_lens"]) for r in tt["rows"])
    r_pre = sum(pl["bars_before_the_floor"] for r in tt["rows"] for pl in r["per_lens"].values())
    if (r_cells, r_pre) != (j_cells, j_pre):
        faults.append(f"manifest summary (cells {j_cells}, pre-floor {j_pre}) != its own rows "
                      f"(cells {r_cells}, pre-floor {r_pre})")
    t_cells = _grab(r"^F-D-4 TALLY: cells checked \*\*(\d+)\*\*", s3)
    t_pre = _grab(r"^F-D-4 TALLY: .*? bars before a floor \*\*(\d+)\*\*", s3)
    if len(t_cells) != 1 or len(t_pre) != 1:
        faults.append(f"S3 prints {len(t_cells)} F-D-4 TALLY cell counts and {len(t_pre)} "
                      f"pre-floor counts (need exactly 1 each)")
    else:
        if int(t_cells[0]) != j_cells:
            faults.append(f"S3 TALLY cells {t_cells[0]} != two_token_trap.cells_checked {j_cells}")
        if int(t_pre[0]) != j_pre:
            faults.append(f"S3 TALLY pre-floor {t_pre[0]} != len(two_token_trap.bars_before_a_floor) "
                          f"{j_pre}")
    s_cells = _grab(r"^(\d+) \(asset, lens\) cells over", s3)
    s_pre = _grab(r"bars before a floor: \*\*(NONE|\d+)\*\*", s3)
    if len(s_cells) != 1 or int(s_cells[0]) != j_cells:
        faults.append(f"spliced F-D-4 sentence cells {s_cells} != {j_cells}")
    if len(s_pre) != 1 or (0 if s_pre[0] == "NONE" else int(s_pre[0])) != j_pre:
        faults.append(f"spliced F-D-4 sentence pre-floor {s_pre} != {j_pre}")
    m_cells = _grab(r"^F-D-4 RE-MEASURED: cells \*\*(\d+)\*\*", s3)
    m_pre = _grab(r"^F-D-4 RE-MEASURED: .*? bars before a floor \*\*(\d+)\*\*", s3)
    if len(m_cells) != 1 or int(m_cells[0]) != j_cells or len(m_pre) != 1 or int(m_pre[0]) != j_pre:
        faults.append(f"S3 RE-MEASURED line (cells {m_cells}, pre-floor {m_pre}) != "
                      f"({j_cells}, {j_pre})")
    if meas is not None:
        files = man["files"]
        k = [(f, r) for f, r in zip(files, meas) if f["kind"] == "klines"]
        tape_pre = sum(r["pre_floor"] for _, r in k)
        unfloored = [f"{f['asset']} {f['as_of_lens']}" for f, r in k if r["pre_floor"] is None]
        if unfloored:
            faults.append(f"cells with no filed floor: {unfloored}")
        if len(k) != j_cells or tape_pre != j_pre:
            faults.append(f"tapes re-measured through load_asof: cells {len(k)}, pre-floor "
                          f"{tape_pre} != ({j_cells}, {j_pre})")
    return faults


def check_d5(s3: str, spend: dict, man: dict) -> list[str]:
    faults = []
    cnt = spend["counts"]
    rec = {c: sum(1 for r in spend["rows"] if r["class"] == c) for c in CLASSES}
    lists = {c: len(spend["classes"].get(c, [])) for c in CLASSES}
    if {c: cnt.get(c) for c in CLASSES} != rec:
        faults.append(f"DATA_SPEND_AUDIT counts {cnt} != recount of its rows {rec}")
    if lists != rec:
        faults.append(f"DATA_SPEND_AUDIT class lists {lists} != recount of its rows {rec}")
    if sorted(spend["never_touched"]) != sorted(r["asset"] for r in spend["rows"]
                                                if r["class"] == "never-touched"):
        faults.append("DATA_SPEND_AUDIT never_touched != its never-touched rows")
    if man["data_spend"]["counts"] != cnt:
        faults.append(f"manifest data_spend counts {man['data_spend']['counts']} != audit {cnt}")
    line = _grab(r"^F-D-5 COUNTS: (.*)$", s3)
    if len(line) != 1:
        faults.append(f"S3 prints {len(line)} F-D-5 COUNTS lines (need 1)")
    else:
        printed = dict((c, int(n)) for c, n in re.findall(r"([a-z-]+) \*\*(\d+)\*\*", line[0])
                       if c in CLASSES)
        if printed != rec or printed != {c: cnt.get(c) for c in CLASSES}:
            faults.append(f"S3 F-D-5 COUNTS {printed} != audit counts {cnt} / rows {rec}")
    sl = _grab(r"^COUNTS: (\{[^}]*\})", s3)
    if len(sl) != 1:
        faults.append(f"spliced COUNTS line found {len(sl)} times (need 1)")
    else:
        spl = ast.literal_eval(sl[0])
        if {c: spl.get(c) for c in CLASSES} != rec:
            faults.append(f"spliced COUNTS {spl} != audit rows {rec}")
    for c in CLASSES:
        row = _grab(rf"^\| {re.escape(c)} \| (\d+) \| ([^|]*) \|$", s3)
        want = " ".join(r["asset"] for r in spend["rows"] if r["class"] == c)
        if len(row) != 1 or int(row[0][0]) != rec[c] or row[0][1].strip() != want:
            faults.append(f"S3 class row '{c}' {row} != audit rows ({rec[c]}: {want})")
    return faults


def check_sha(root: Path, rec: dict, s3: str | None) -> list[str]:
    faults = []
    shas = rec.get("artifact_shas", {})
    if rec.get("artifact_count") != DCORE_ARTIFACTS or len(shas) != DCORE_ARTIFACTS:
        faults.append(f"record holds artifact_count {rec.get('artifact_count')}, {len(shas)} shas "
                      f"(need {DCORE_ARTIFACTS})")
    for need in (MANIFEST_MD_REL, MANIFEST_JSON_REL, SPEND_REL):
        if need not in shas:
            faults.append(f"spliced / read source {need} is not a recorded D-CORE artifact")
    for rel, r in shas.items():
        p = root / rel
        if not p.is_file():
            faults.append(f"{rel}: ABSENT")
            continue
        if p.stat().st_size != r["bytes"]:
            faults.append(f"{rel}: bytes {p.stat().st_size} != {r['bytes']}")
        h = sha256_file(p)
        if h != r["sha256"]:
            faults.append(f"{rel}: sha {h[:16]} != recorded {r['sha256'][:16]}")
        if s3 is not None:
            row = _grab(rf"^\| `{re.escape(rel)}` \| (\d+) \| `([0-9a-f]{{16}})` \| (\w+) \|$", s3)
            if len(row) != 1 or row[0] != (str(r["bytes"]), r["sha256"][:16], "MATCH"):
                faults.append(f"{rel}: S3 prints {row} (need bytes {r['bytes']}, "
                              f"sha16 {r['sha256'][:16]}, MATCH)")
    return faults


def check_red(s3: str) -> list[str]:
    faults = []
    st = _grab(r"^F-D-1 STATUS: (.*)$", s3)
    if len(st) != 1:
        return [f"S3 prints {len(st)} 'F-D-1 STATUS:' lines (need exactly 1)"]
    m = re.match(r"\*\*(RED|NOT RUN)\*\*", st[0])
    if not m:
        faults.append(f"F-D-1 printed as {st[0][:60]!r} — only RED / NOT RUN are legal")
    for tok in ("PASS", "GREEN", "UNDETERMINED", "**OK**"):
        if tok in st[0]:
            faults.append(f"F-D-1 status line carries {tok!r}")
    q = _grab(r"^OPERATOR QUESTION: (.+)$", s3)
    if len(q) != 1 or "which publication is the record" not in q[0]:
        faults.append("F-D-1's operator question ('which publication is the record') is not printed")
    return faults


CELL_HDR = ("| asset | stem | lens | bars as-of | first open | last as-of open | past the pin | "
            "gaps (missing) | sha256[:16] | re-measured |")


def check_table(s3: str, man: dict, meas: list[dict]) -> list[str]:
    faults = []
    a = s3.find("<!-- S3-TABLE BEGIN id=cells -->")
    b = s3.find("<!-- S3-TABLE END id=cells -->")
    if a < 0 or b < 0:
        return ["per asset x lens table markers absent"]
    rows = [l for l in s3[a:b].splitlines() if l.startswith("| ")]
    if not rows or rows[0] != CELL_HDR:
        faults.append("table header differs")
    body = [r for r in rows[1:]]
    files = man["files"]
    if len(body) != len(files):
        faults.append(f"table holds {len(body)} rows, files[] {len(files)} — not whole")
    for i, (f, r) in enumerate(zip(files, meas)):
        e = cell_expect(f)
        want = [f["asset"], f["stem"], e["lens"], str(e["n"]), e["first"], e["last"],
                str(e["after"]), e["gaps"], f"`{e['sha16']}`", "OK"]
        got = [c.strip() for c in body[i].strip().strip("|").split(" | ")] if i < len(body) else []
        if got != want:
            faults.append(f"row {i + 1} ({f['path']}): printed {got} != filed {want}")
        bad = cell_faults(f, r)
        if bad:
            faults.append(f"{f['path']}: re-measure {bad}")
    return faults


def self_ast_faults(src: str) -> list[str]:
    faults = []
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                if n.name in FORBIDDEN_MODULES:
                    faults.append(f"code imports {n.name}")
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "") in FORBIDDEN_MODULES:
                faults.append(f"code imports from {node.module}")
        elif isinstance(node, ast.Call):
            fn = node.func
            name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", None)
            if name in FORBIDDEN_CALLS:
                faults.append(f"code calls {name}()")
    return faults


def check_closure(modules: list[str], src: str) -> list[str]:
    faults = [f"run-time import of {m}" for m in FORBIDDEN_MODULES if m in modules]
    if "tierc10_data" not in modules:
        faults.append("tierc10_data (the only as-of bar reader) was not the reader")
    return faults + self_ast_faults(src)


def check_det(doc1: bytes, doc2: bytes, transcript: str) -> list[str]:
    faults = []
    if doc1 != doc2:
        k = next((i for i in range(min(len(doc1), len(doc2))) if doc1[i] != doc2[i]),
                 min(len(doc1), len(doc2)))
        faults.append(f"two builds differ at byte {k} ({len(doc1)} B vs {len(doc2)} B)")
    toks = TEMP_TOKENS + (tempfile.gettempdir(),)
    hit_doc = [k for k, tok in enumerate(toks) if tok.encode() in doc1]
    hit_tr = [k for k, tok in enumerate(toks) if tok in transcript]
    if hit_doc:
        faults.append(f"S3 carries a temp-path token (token #{hit_doc[0]})")
    if hit_tr:
        faults.append(f"the transcript carries a temp-path token (token #{hit_tr[0]})")
    return faults


# ---------------------------------------------------------------- fixture runner
class Transcript:
    def __init__(self) -> None:
        self.lines: list[str] = []
        self.passed: list[str] = []
        self.failed: list[str] = []

    def p(self, s: str = "") -> None:
        self.lines.append(s)
        print(s, flush=True)

    def leg(self, name: str, title: str, fails_if: str, real: list[str],
            plants: list[tuple[str, list[str]]], detail: str) -> None:
        self.p(f"{name} — {title}")
        blind = [lab for lab, f in plants if not f]
        red = [f"{lab}: red ({f[0][:150]})" for lab, f in plants if f]
        if red:
            self.p("  [BREAK] deliberate violation -> RED (correct): " + " · ".join(red))
        if blind:
            self.p("  [BREAK] plant STAYED GREEN -> the guard is BLIND: " + " · ".join(blind))
        for f in real[:12]:
            self.p(f"      FAULT: {f}")
        if len(real) > 12:
            self.p(f"      ... {len(real) - 12} more fault(s)")
        ok = not real and not blind and len(plants) > 0
        (self.passed if ok else self.failed).append(name)
        self.p(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}.  FAILS IF {fails_if}")
        self.p("")


def flip_one_char(b: bytes, at: int) -> bytes:
    c = b[at:at + 1]
    rep = b"X" if c != b"X" else b"Y"
    return b[:at] + rep + b[at + 1:]


def run_legs(T: Transcript, root: Path, D, I: dict, meas: list[dict], fd1: dict,
             s3: bytes, rebuild) -> None:
    import numpy as np
    s3t = s3.decode("utf-8")
    man, spend, md, rec = I["man"], I["spend"], I["md"], I["dcore"]

    # ---- F-S3-SLICE
    real, n_sp, n_bytes = check_slice(s3, md)
    fm = BEGIN_RE.search(s3)
    inside = fm.end() + 40
    first_venue = span_of(md, SPLICES[0][1], SPLICES[0][2])
    md_at = first_venue[0] + 40
    sid_last = SPLICES[-1][0]
    mm = re.search(rb"<!-- S3-SPLICE BEGIN id=" + sid_last.encode() + rb" [^\n]*\n", s3)
    e_tok = f"<!-- S3-SPLICE END id={sid_last} -->\n".encode()
    e = s3.find(e_tok)
    dropped = s3[:mm.start()] + s3[e + len(e_tok):]
    plants = [
        ("one char changed inside the 'venue' span of a COPY of S3",
         check_slice(flip_one_char(s3, inside), md)[0]),
        ("one char changed inside the 'venue' span of a COPY of the manifest",
         check_slice(s3, flip_one_char(md, md_at))[0]),
        (f"the '{sid_last}' span deleted from a COPY of S3", check_slice(dropped, md)[0]),
        ("one byte appended to the end of the 'rulings' span in a COPY of S3",
         check_slice(s3[:e] + b" " + s3[e:], md)[0]),
    ]
    T.leg("F-S3-SLICE", "every spliced span is its manifest heading span, byte for byte",
          "a spliced span in S3 differs by one byte from its heading span in "
          f"{MANIFEST_MD_REL}, a span of record is missing or doubled, or a marker's byte "
          "range / sha disagrees with the manifest (re-extracted by an independent line walk)",
          real, plants,
          f"{n_sp}/{len(SPLICES)} spans ({', '.join(s[0] for s in SPLICES)}), {n_bytes} manifest "
          f"bytes, byte-identical")

    # ---- F-S3-D4
    real = check_d4(s3t, man, meas)
    # CONSISTENT bends: summary AND its own rows moved together, so only the
    # printed-vs-JSON clause (and the tapes) can catch them
    m_c = copy.deepcopy(man)
    m_c["two_token_trap"]["cells_checked"] -= 1
    del m_c["two_token_trap"]["rows"][0]["per_lens"]["1w"]
    m_p = copy.deepcopy(man)
    m_p["two_token_trap"]["bars_before_a_floor"].append({"asset": "PUMPFUN", "lens": "4h",
                                                         "planted": True})
    [r for r in m_p["two_token_trap"]["rows"] if r["asset"] == "PUMPFUN"][0][
        "per_lens"]["4h"]["bars_before_the_floor"] = 1
    # a summary-only bend: the JSON disagrees with itself
    m1 = copy.deepcopy(man)
    m1["two_token_trap"]["cells_checked"] -= 1
    s3_bent = re.sub(r"(?m)^(F-D-4 TALLY: cells checked \*\*)(\d+)",
                     lambda m: m.group(1) + str(int(m.group(2)) + 1), s3t)
    # a bar planted one step BEFORE a filed floor, on an in-memory copy of one tape
    tt_row = [r for r in man["two_token_trap"]["rows"] if r["asset"] == "PUMPFUN"][0]
    floor_ms = iso_to_ms(tt_row["per_lens"]["4h"]["floor_open"])
    fr = D.load_asof(tt_row["stem"], "4h")
    t = fr["open_time"].to_numpy().copy()
    t_planted = np.concatenate([[floor_ms - int(D.STEP_MS["4h"])], t])
    meas_p = copy.deepcopy(meas)
    idx = [i for i, f in enumerate(man["files"])
           if f["asset"] == "PUMPFUN" and f["as_of_lens"] == "4h"][0]
    meas_p[idx] = {**meas_p[idx], **frame_stats(D, t_planted, "4h", floor_ms)}
    plants = [
        ("cells_checked -1 AND one per-lens row removed, together, in a COPY of the manifest "
         "JSON", check_d4(s3t, m_c, meas)),
        ("a pre-floor bar added to bars_before_a_floor AND to its per-lens row, together, in a "
         "COPY of the manifest JSON", check_d4(s3t, m_p, meas)),
        ("cells_checked -1 alone in a COPY of the manifest JSON (summary != its own rows)",
         check_d4(s3t, m1, meas)),
        ("the TALLY cell count bent +1 in a COPY of S3", check_d4(s3_bent, man, meas)),
        ("a PUMPFUN 4h bar planted one step before its filed floor in a COPY of the load_asof "
         "tape", check_d4(s3t, man, meas_p)),
    ]
    tt = man["two_token_trap"]
    T.leg("F-S3-D4", "the F-D-4 counts S3 prints are the manifest's, and the tapes agree",
          "the F-D-4 cell count or pre-floor count printed in S3 (tally line, spliced sentence, "
          "re-measured line) differs from STAGE_D_MANIFEST.json two_token_trap, from a recount "
          "of its own per-lens rows, or from a re-measure of every kline cell through "
          "tierc10_data.load_asof", real, plants,
          f"cells {tt['cells_checked']} and pre-floor {len(tt['bars_before_a_floor'])} agree "
          f"five ways (JSON summary, JSON rows, S3 tally, S3 spliced sentence, the tapes "
          f"re-read through load_asof)")

    # ---- F-S3-D5
    real = check_d5(s3t, spend, man)
    moved = copy.deepcopy(spend)
    sui = [r for r in moved["rows"] if r["asset"] == "SUI"][0]
    sui["class"] = "display-only"
    moved["classes"]["never-touched"] = [a for a in moved["classes"]["never-touched"] if a != "SUI"]
    moved["classes"]["display-only"] = moved["classes"]["display-only"] + ["SUI"]
    moved["counts"] = {**moved["counts"], "never-touched": moved["counts"]["never-touched"] - 1,
                       "display-only": moved["counts"]["display-only"] + 1}
    moved["never_touched"] = [a for a in moved["never_touched"] if a != "SUI"]
    moved_m = copy.deepcopy(man)
    moved_m["data_spend"]["counts"] = moved["counts"]
    rows_only = copy.deepcopy(spend)
    [r for r in rows_only["rows"] if r["asset"] == "HYPE"][0]["class"] = "scored"
    s3_d5 = re.sub(r"(?m)^(F-D-5 COUNTS: never-touched \*\*)(\d+)",
                   lambda m: m.group(1) + str(int(m.group(2)) + 1), s3t)
    plants = [
        ("SUI moved never-touched -> display-only in a COPY of the audit (rows, class lists, "
         "counts, never_touched and the manifest's data_spend all moved together)",
         check_d5(s3t, moved, moved_m)),
        ("HYPE moved display-only -> scored in the rows of a COPY of the audit only",
         check_d5(s3t, rows_only, man)),
        ("the printed never-touched count bent +1 in a COPY of S3", check_d5(s3_d5, spend, man)),
    ]
    cnt = spend["counts"]
    T.leg("F-S3-D5", "the class counts S3 prints are DATA_SPEND_AUDIT.json's",
          f"the class counts printed in S3 (tally line, class table, spliced COUNTS line) differ "
          f"from {SPEND_REL} counts, from a recount of its rows, from its class lists, or the "
          f"manifest's data_spend counts differ from the audit's", real, plants,
          " · ".join(f"{c} {cnt[c]}" for c in CLASSES)
          + f" — printed == audit counts == row recount == class lists == manifest data_spend")

    # ---- F-S3-SHA
    real = check_sha(root, rec, s3t)
    tmp = Path(tempfile.mkdtemp(prefix="tc10_s3sha_"))
    try:
        for rel in rec["artifact_shas"]:
            (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / rel, tmp / rel)
        victim = tmp / PIN_REL
        b = victim.read_bytes()
        victim.write_bytes(b[:10] + bytes([b[10] ^ 0x01]) + b[11:])
        p_flip = check_sha(tmp, rec, None)
        victim.write_bytes(b)
        gone = tmp / FILED_OFFLINE_REL
        gb = gone.read_bytes()
        gone.unlink()
        p_gone = check_sha(tmp, rec, None)
        gone.write_bytes(gb)
        r_bent = copy.deepcopy(rec)
        s = r_bent["artifact_shas"][MANIFEST_MD_REL]["sha256"]
        r_bent["artifact_shas"][MANIFEST_MD_REL]["sha256"] = ("0" if s[0] != "0" else "1") + s[1:]
        p_bent = check_sha(tmp, r_bent, None)
        r_drop = copy.deepcopy(rec)
        del r_drop["artifact_shas"][SPEND_REL]
        p_drop = check_sha(tmp, r_drop, None)
        p_clean = check_sha(tmp, rec, None)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if p_clean:
        real = real + [f"control: an unplanted COPY of the 15 does not re-hash: {p_clean[0]}"]
    plants = [
        ("one byte flipped in a COPY of AS_OF_PIN.json", p_flip),
        ("FIXTURES_STAGE_D_OFFLINE.txt deleted from the COPY tree", p_gone),
        ("the STAGE_D_MANIFEST.md sha bent in a COPY of the PROGRESS record", p_bent),
        ("DATA_SPEND_AUDIT.json dropped from a COPY of the PROGRESS record", p_drop),
    ]
    T.leg("F-S3-SHA", f"the {DCORE_ARTIFACTS} D-CORE artifacts re-hash to PROGRESS.json",
          f"any of the {DCORE_ARTIFACTS} D-CORE artifacts does not re-hash (sha256 and bytes) "
          f"to its {PROGRESS_REL} record, the record does not hold exactly {DCORE_ARTIFACTS}, a "
          f"spliced / read source is not among them, or S3 prints a sha16 / byte count / MATCH "
          f"other than the record's", real, plants,
          f"{len(rec['artifact_shas'])}/{DCORE_ARTIFACTS} re-hash MATCH (sha256 + bytes); the "
          f"spliced manifest, the manifest JSON and the audit are recorded artifacts; an "
          f"unplanted COPY tree re-hashes clean (control)")

    # ---- F-S3-RED
    real = check_red(s3t)
    if fd1["status"] != "RED":
        real = real + [f"the filed ONLINE transcript no longer reads F-D-1 [FAIL] "
                       f"(derived status {fd1['status']})"]
    online_pass = I["online"].replace("[FAIL] F-D-1:", "[PASS] F-D-1:") \
        .replace('"failed": ["F-D-1"]', '"failed": []')
    fd1_p = fd1_status(online_pass, I["offline"])
    s3_green_derived = rebuild(fd1_p).decode("utf-8")
    s3_green = re.sub(r"(?m)^F-D-1 STATUS: \*\*RED\*\*", "F-D-1 STATUS: **GREEN**", s3t)
    s3_noq = re.sub(r"(?m)^OPERATOR QUESTION: .*$", "OPERATOR QUESTION:", s3t)
    s3_nostatus = re.sub(r"(?m)^F-D-1 STATUS: .*\n", "", s3t)
    plants = [
        ("a COPY of the filed ONLINE transcript reading [PASS] F-D-1, rendered whole",
         check_red(s3_green_derived)),
        ("the status bent RED -> GREEN in a COPY of S3", check_red(s3_green)),
        ("the operator question blanked in a COPY of S3", check_red(s3_noq)),
        ("the status line deleted from a COPY of S3", check_red(s3_nostatus)),
    ]
    T.leg("F-S3-RED", "F-D-1 is printed RED / NOT RUN, with its operator question",
          "F-D-1 is printed as anything but RED / NOT RUN, the status line is absent or doubled, "
          "its operator question is not printed, or the filed ONLINE transcript no longer reads "
          "[FAIL] F-D-1", real, plants,
          f"printed RED (derived from {FILED_ONLINE_REL}:{fd1['fail_line']} [FAIL], "
          f"{fd1['n_differ']} bar(s) differ, FIXTURE SUMMARY failed {fd1['summary_failed']}) and "
          f"NOT RUN here; the operator question is printed verbatim from "
          f"STAGE_D_MANIFEST.json operator_rulings_needed[0]")

    # ---- F-S3-TABLE
    real = check_table(s3t, man, meas)
    f_bent = copy.deepcopy(man)
    f_bent["files"][0]["rows_as_of"] += 1
    small = min((i for i, f in enumerate(man["files"]) if f["kind"] == "klines"),
                key=lambda i: man["files"][i]["bytes"])
    sp = Path(man["snapshot_root"]) / man["files"][small]["path"]
    tmp = Path(tempfile.mkdtemp(prefix="tc10_s3tab_"))
    try:
        cp = tmp / "copy.parquet"
        shutil.copyfile(sp, cp)
        bb = cp.read_bytes()
        cp.write_bytes(bb[:100] + bytes([bb[100] ^ 0x01]) + bb[101:])
        meas_h = copy.deepcopy(meas)
        meas_h[small] = {**meas_h[small], "sha": sha256_file(cp)}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    floors = f_d4_floors(man)
    f0, f1 = man["files"][0], man["files"][1]
    t0 = D.load_asof(f0["stem"], f0["as_of_lens"])["open_time"].to_numpy()
    meas_d = copy.deepcopy(meas)
    meas_d[0] = {**meas_d[0], **frame_stats(D, t0[:-1], f0["as_of_lens"],
                                             floors.get((f0["asset"], f0["as_of_lens"])))}
    t1 = D.load_asof(f1["stem"], f1["as_of_lens"])["open_time"].to_numpy()
    meas_g = copy.deepcopy(meas)
    meas_g[1] = {**meas_g[1], **frame_stats(D, np.delete(t1, 1000), f1["as_of_lens"],
                                             floors.get((f1["asset"], f1["as_of_lens"])))}
    rows_cut = "\n".join(l for l in s3t.splitlines() if not l.startswith("| XMR | XMRUSDT | 1w |"))
    plants = [
        (f"{f0['path']} rows_as_of bent +1 in a COPY of files[]", check_table(s3t, f_bent, meas)),
        (f"one byte flipped in a COPY of {man['files'][small]['path']}",
         check_table(s3t, man, meas_h)),
        (f"the last as-of bar dropped from a COPY of the {f0['path']} load_asof tape",
         check_table(s3t, man, meas_d)),
        (f"one interior bar dropped from a COPY of the {f1['path']} load_asof tape "
         f"(a gap the filing does not list)", check_table(s3t, man, meas_g)),
        ("the XMR 1w row removed from a COPY of S3", check_table(rows_cut, man, meas)),
    ]
    nk = sum(1 for f in man["files"] if f["kind"] == "klines")
    bars = sum(r["n"] for f, r in zip(man["files"], meas) if f["kind"] == "klines")
    T.leg("F-S3-TABLE", "the per asset x lens table is files[], whole, and re-measures",
          "the table is not whole (every files[] entry, in order), any printed cell (bars, "
          "first / last open, past-the-pin, gaps, sha256[:16]) differs from files[], or any "
          "re-measure — load_asof count / first / last / gap count / missing bars, "
          "load_funding_asof count / first / last, the file's re-hash — differs from files[]",
          real, plants,
          f"{len(man['files'])}/{len(man['files'])} rows ({nk} kline cells, "
          f"{len(man['files']) - nk} funding files); {bars} kline bars re-read through load_asof, "
          f"{len(man['files'])} files re-hashed; every cell equal")

    # ---- F-S3-CLOSURE
    src = (root / SELF_REL).read_text()
    mods = sorted(sys.modules)
    real = check_closure(mods, src)
    plants = [
        ("tierc10_panel (TP: score / finish_family / register) planted in a COPY of the module "
         "list", check_closure(mods + ["tierc10_panel"], src)),
        ("tierc2_baseline planted in a COPY of the module list",
         check_closure(mods + ["tierc2_baseline"], src)),
        ("'import tierc2_baseline' + a load_klines() call appended to a COPY of this source",
         check_closure(mods, src + "\nimport tierc2_baseline\ntierc2_baseline.load_klines('X', '5m')\n")),
    ]
    T.leg("F-S3-CLOSURE", "nothing that scores, registers or reads whole files is in the run",
          f"any of {list(FORBIDDEN_MODULES)} is imported at run time, tierc10_data is not the "
          f"bar reader, or this file's code imports one of them or calls "
          f"{list(FORBIDDEN_CALLS)}", real, plants,
          "no forbidden module at run time; tierc10_data present; this file's AST imports none "
          "and calls none")

    # ---- F-DET
    doc2 = rebuild(fd1)
    transcript_so_far = "\n".join(T.lines)
    real = check_det(s3, doc2, transcript_so_far)
    tmpdir = tempfile.gettempdir()
    plants = [
        ("a second build carrying a run clock line",
         check_det(s3, rebuild(fd1, volatile=f"built {time.strftime(FMT, time.gmtime(0))} "
                                             f"(clock planted)"), transcript_so_far)),
        ("a temp path planted in a COPY of S3",
         check_det(s3 + f"\n{tmpdir}/x\n".encode(), s3 + f"\n{tmpdir}/x\n".encode(),
                   transcript_so_far)),
        ("a temp path planted in a COPY of the transcript",
         check_det(s3, doc2, transcript_so_far + "\n/var/folders/zz/planted")),
    ]
    T.leg("F-DET", "S3 is a pure function of the filed inputs",
          "two independent builds of S3 (every input re-read, every tape re-measured) are not "
          "byte-identical, or S3 / the transcript carries a temp path", real, plants,
          f"two builds byte-identical ({len(s3)} B, sha256 {sha256_bytes(s3)[:16]}); no temp "
          f"path in S3 or the transcript")


# ---------------------------------------------------------------- main
def main() -> int:
    root = ROOT
    T = Transcript()
    T.p(f"TIER-C10 · CLOSE §3 · STAGE D MANIFEST (incl. F-D-4 / F-D-5) — FIXTURES · "
        f"{SELF_REL}")
    T.p(f"{LABEL} · no score, no card, no registration verdict consulted · bars through "
        f"tierc10_data.load_asof only")
    T.p("")
    T.p("PREAMBLE")
    checks, _ = preamble(root)
    for ok, txt in checks:
        T.p(f"  [{'RUN ' if ok else 'HALT'}] {txt}")
    if not all(ok for ok, _ in checks):
        T.p("PREAMBLE: HALT — nothing read past the preamble, NOTHING written")
        return 1
    T.p("PREAMBLE: RUN")
    T.p("")

    sys.path.insert(0, str(root))
    sys.path.insert(0, str(root / "scripts"))
    import tierc10_data as D                                        # noqa: E402

    if D.SNAPSHOT.resolve() != SNAPSHOT.resolve():
        T.p("PREAMBLE: HALT — tierc10_data.SNAPSHOT is not the TC10 snapshot")
        return 1

    def build(fd1_override=None, volatile: str = "") -> tuple[bytes, dict, list, dict]:
        I = load_inputs(root)
        I["rulings_bits"] = rulings_bits(I["rulings"])
        if Path(I["man"]["snapshot_root"]).resolve() != SNAPSHOT.resolve():
            raise Halt("manifest snapshot_root is not the TC10 snapshot")
        meas = measure(D, I["man"], SNAPSHOT)
        fd1 = fd1_override or fd1_status(I["online"], I["offline"])
        return render(I, meas, fd1, root, volatile), I, meas, fd1

    try:
        s3, I, meas, fd1 = build()
    except Halt as h:
        T.p(f"PREAMBLE: HALT — {h}")
        return 1

    out_md = root / OUT_MD_REL
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_bytes(s3)
    s3_disk = out_md.read_bytes()
    T.p(f"S3 written: {OUT_MD_REL} · {len(s3_disk)} B · sha256 {sha256_bytes(s3_disk)}")
    T.p(f"inputs: {MANIFEST_MD_REL} {sha256_bytes(I['md'])[:16]} · "
        f"{MANIFEST_JSON_REL} {sha256_file(root / MANIFEST_JSON_REL)[:16]} · "
        f"{SPEND_REL} {sha256_file(root / SPEND_REL)[:16]} · {PROGRESS_REL} [{DCORE}] status "
        f"{I['dcore']['status']}")
    T.p(f"F-D-1 (carried, venue leg): {fd1['status']} — {FILED_ONLINE_REL}:{fd1['fail_line']} "
        f"[FAIL], {fd1['n_differ']} bar(s) differ ({', '.join(fd1['differing'])}); NOT RUN here "
        f"(no venue reach). OPERATOR QUESTION: which publication is the record — REST or ARCHIVE?")
    T.p("")

    def rebuild(fd1_x, volatile: str = "") -> bytes:
        return build(fd1_x, volatile)[0]

    run_legs(T, root, D, I, meas, fd1, s3_disk, rebuild)

    n = len(T.passed) + len(T.failed)
    T.p(f"FIXTURE SUMMARY  {len(T.passed)}/{n} PASS  "
        + json.dumps({"passed": T.passed, "failed": T.failed,
                      "not_run": ["F-D-1 (venue leg; carried RED from the filed ONLINE transcript)"]}))
    text = "\n".join(T.lines) + "\n"
    out_fix = root / OUT_FIX_REL
    prior = out_fix.read_bytes() if out_fix.is_file() else None
    out_fix.write_text(text)
    sys.stderr.write(f"transcript sha256 {sha256_bytes(text.encode())} · prior run: "
                     f"{'absent' if prior is None else ('IDENTICAL' if prior == text.encode() else 'DIFFERS')}\n")
    return 0 if not T.failed else 1


if __name__ == "__main__":
    sys.exit(main())
