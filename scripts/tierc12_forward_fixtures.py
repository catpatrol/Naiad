#!/usr/bin/env python
"""TIER-C12 · THE FORWARD SUITE [LEANS L-L.7, L-L.18; L-0.14; L-0.19 seam 2] — one suite, one transcript per
record (`--stage=<record id>`, never a leg filter).

  --stage=TC12-REG.ledger-spec  ->  research_outputs/tierc12/forward/FIXTURES_LEDGER_SPEC.txt
      The fourth book's spec and the FIVE-LINE ledger, before any bar is read.  At this record the suite
      imports the env-free module tierc12_forward_spec only and prints the pre-substrate header.
        F-LEDGER [PREFIX] · [CHAIN] · [STRUCTURE] · [REHASH] · [ANCESTORS]   the contract's F-LEDGER (:122)
        F-FWD-SPEC      the spec is its sources'; the gate-text selector; the tool is env-free, opens only
                        SPEC_READS_T and is value-area-blind (the ride clause FWD-SPEC-RIDE is TC12-L's)
        F-PORT          every port's label is true of its source text at its pinned sha
        F-TYPED-FLOW [ledger.opening] · [ledger.n_min] · [adm.lag_cut]       each pin bent AT ITS DOOR
  --stage=TC12-L  ->  forward/FIXTURES_LEDGER.txt — the refreshed file and L-L.18's family: filed by the
      TC12-L builder (STAGES below holds one row per record).

THE FIVE-LINE FILE.  The ledger is append-only and TC12-L appends rows and one refresh line to it.  This
record's transcript must re-run byte-identical after that, so at this stage every leg PRINTS only what the
working file's first FIVE lines — the bytes this record files — say.  The real legs of F-LEDGER [CHAIN] and
[STRUCTURE] JUDGE the whole working file as well (working_fx): a line standing after line 5 that breaks the
chain law or S2-S7 is RED here, and a lawful tail prints nothing.

SECOND OBJECTS.  The typed literals below are this suite's commission (L-0.14): the shas, the instants, the
names and the counts are typed here and production is compared against them; no production constant is
read as a referee.  forward_log itself is imported HERE (a fixture is not a decision module) as the
independent verifier of the chain law that tierc12_forward_spec carries as ports.  Scratch copies live
under $TMPDIR and are removed; nothing but the transcript is written under --root.

Run:  export PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/tierc12_forward_fixtures.py \\
          --stage=TC12-REG.ledger-spec [--refile-transcript] [--root=DIR]
Exit 0 = GREEN · 1 = a RED or VOID leg, or a transcript finding.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import forward_log as FLREF                 # the chain law's own module — fixture-side only
import tierc12_forward_spec as SPEC
import tierc12_fx as FX
import tierc12_pins as PINS
import tierc12_progress as PG

ROOT = Path(__file__).resolve().parents[1]
MAIN = PINS.main_tree(ROOT)

# ═══════════════════════════════════════════════════════ THE TYPED COMMISSION (second objects)
STAGE_SPEC_T = "TC12-REG.ledger-spec"
STAGES = {STAGE_SPEC_T: "FIXTURES_LEDGER_SPEC.txt"}       # record id -> its transcript; TC12-L adds its row
T12_T = "research_outputs/tierc12"
T11_T = "research_outputs/tierc11"
XR_T = T12_T + "/x_rec"
FORWARD_T = T12_T + "/forward"
SPEC_T = FORWARD_T + "/BOOK_SPEC_COMBINED.json"
LEDGER_T = FORWARD_T + "/FORWARD_LEDGER.jsonl"
TOOL_T = "scripts/tierc12_forward_spec.py"
FL_T = "scripts/forward_log.py"
REG_T = T12_T + "/registrations/REGISTRATIONS.json"
REG_PIN_T = T12_T + "/registrations/REGISTRY_PIN.json"
LEANS_T = T12_T + "/LEANS.md"
X_MANIFEST_T = XR_T + "/X_REC_MANIFEST.json"
X_LEDGER_T = XR_T + "/tierc11x/forward/FORWARD_LEDGER.jsonl"
X_SPEC_T = XR_T + "/tierc11x/forward/BOOK_SPECS.json"
XF_T = XR_T + "/scripts/tc11x_forward.py"
T11_LEDGER_T = T11_T + "/forward/FORWARD_LEDGER.jsonl"
T11_PAGE_T = T11_T + "/forward/FORWARD_LEDGER.md"
T11_REG_T = T11_T + "/registrations/REGISTRATIONS.json"
T11_PIN_T = T11_T + "/registrations/REGISTRY_PIN.json"
T11_PROGRESS_T = T11_T + "/PROGRESS.json"
STAMP_MAP_T = T12_T + "/close/TC11_STAMP_MAP.json"
R0_KEY_T = "frozen_estate_shas_at_r0"

BOOK4_T = "gated-v6-combined"
X_BOOKS_T = ("v6", "trg912", "gated-v6-oldtide")
KINDS_T = ("book_open", "refresh", "row")
N_X_LINES_T = 4
N5_T = 5
OPEN_KEYS_T = ("book", "kind", "n_min", "opening_iso", "opening_ms", "role", "scored", "spec_sha256", "tier")
LINE5_T = {"kind": "book_open", "tier": "TIER-C12", "book": BOOK4_T, "role": "of record", "scored": False}
ZEROS_T = "0" * 64
X_LEDGER_BYTES_T = 5643
X_LEDGER_SHA_T = "4a6da7e89a3cf5f0127f76aca0d2ae12d218ffc06417c6528c70210092cfa4c5"
X_HEAD_T = "61ea177fadcc82bad06f4744305b88476e29d801829cdfacc4817878306cd89c"
X_SPEC_SHA_T = "72a1f52359c66084d22f8bc99b0cd35e7edd89db2751f4859f559c8b1f51cac3"
T11_LEDGER_SHA_T = "e53328add9e71f1c6198f724a131565a2a10ad2ad1600c36a74c6676f7ada288"
T11_GENESIS_T = "b68a4942b35f6599f8783b02d20dfafc3a72052e88dfaf22055e003b2a105c56"
T11_HEAD_T = "0db889425ef8e3d2075a2a3cf2d1b500c3b0bbc7f7b4d535ffa3dec3575261cb"
T11_REG_HEAD_T = "6772568b31fcfb2d56eb8c80b66dedee4fb5082673369e872972df8f475ec8f9"
OPENING_MS_T = 1790006400000
OPENING_ISO_T = "2026-09-21T16:00:00Z"
SCORE_EDGE_MS_T = 1790294400000
POOL_LO_MS_T = 1567958400000
STEP_Q_T = {"commit": "28e006b", "instant_iso": "2026-10-08T22:52:13Z", "instant_ms": 1791499933000}
N_MIN_T = 30
CUT_T = 16
OLD_T = "B4"
H4_MS_T = 14400000
N_ROW_FIELDS_T = 43
ADDED_T = ("p_age_1_refuses", "p_win_1_refuses", "p_adm_1_refuses", "in_o9_scored_window",
           "entered_before_gate_text_filed", "entered_before_book_frozen")
N_LINEAGE_T = 18
SCORED_RX_T = re.compile(r"^`scored`\s")
N_LAW_T = {"every_book": "in_o9_scored_window == false",
           BOOK4_T: "in_o9_scored_window == false and entered_before_book_frozen == false"}
SPEC_KEYS_T = ("admission", "ancestors", "append_law", "book", "book_order", "books", "chain", "continuation",
               "contract", "ctrl_cols", "existing_books", "flags", "leans_sha256", "n_law", "n_min", "opening",
               "opening_held_equal", "opening_rival", "path_modules", "pool_lo_ms", "refresh_law", "registry",
               "row_fields", "row_fields_added", "row_nullable", "scored_window_end_ms", "stage", "tc11_registry",
               "tier")
SPEC_READS_T = (
    "exchange/queue/2026-10-08_TC12_APOLLO.md",
    "research_outputs/tierc12/progress/STEP_Q.json",
    "research_outputs/tierc12/progress/TC12-R0.json",
    "research_outputs/tierc12/registrations/REGISTRATIONS.json",
    "research_outputs/tierc12/registrations/REGISTRY_PIN.json",
    "research_outputs/tierc12/x_rec/X_REC_MANIFEST.json",
    "research_outputs/tierc12/x_rec/tierc11x/forward/FORWARD_LEDGER.jsonl",
    "research_outputs/tierc12/x_rec/tierc11x/forward/BOOK_SPECS.json",
    "research_outputs/tierc12/x_rec/scripts/tc11x_forward.py",
    "research_outputs/tierc12/x_rec/scripts/tc11x_books.py",
    "research_outputs/tierc11/forward/FORWARD_LEDGER.jsonl",
    "research_outputs/tierc11/registrations/REGISTRATIONS.json",
    "research_outputs/tierc11/registrations/REGISTRY_PIN.json",
    "research_outputs/tierc11/LEANS.md",
    "research_outputs/tierc11/data/AS_OF_PIN.json",
    "research_outputs/tierc11/PROGRESS.json",
    "research_outputs/tierc12/close/TC11_STAMP_MAP.json",
)
IMPORTS_T = ("forward_log", "tierc12_progress", "tierc12_pins")      # beside the stdlib [L-L.18 F-FWD-SPEC]
IO_ATTRS_T = ("read_bytes", "read_text", "write_bytes", "write_text", "open", "unlink", "rmdir", "mkdir",
              "iterdir")
IO_MODULES_T = ("os", "shutil")
OPEN_SITES_T = ("_read", "read_lines", "append_entry", "chain_findings", "sources", "freeze_spec",
                "read_spec", "atomic_append", "open_ledger")
BLIND_TOKENS_T = ("tierc12/va", ".parquet", "klines", "funding/", ".cache")
FL_PORTS_T = ("canonical", "chain_hash", "read_lines", "last_sha", "append_entry", "verify_chain")
PORTS_T = {"canonical": "VERBATIM", "chain_hash": "VERBATIM", "read_lines": "VERBATIM", "last_sha": "CHANGED",
           "append_entry": "VERBATIM", "verify_chain": "VERBATIM", "chained": "VERBATIM", "body_of": "VERBATIM",
           "append": "CHANGED", "book_open_body": "VERBATIM", "render_json": "VERBATIM",
           "chain_findings": "CHANGED"}
LAST_SHA_T = ("lines[-1]", "lines[len(lines) - 1]")
X_LITERALS_T = {"CHAIN_FIELDS": ("prev_sha256", "entry_sha256"), "KINDS": KINDS_T}
PORT_RX = re.compile(r"# PORT (VERBATIM|TEXT-ONLY|CHANGED) <- (\S+):(\d+)-(\d+) sha256 ([0-9a-f]{64})\n"
                     r"(?:#[^\n]*\n)*def (\w+)\(")
FLOW_PINS_T = ("ledger.opening", "ledger.n_min", "adm.lag_cut")
FLOW_WITNESS_T = {"ledger.opening": "the FWD-OPENING assertion of the spec tool (the build HALTs there, L-L.8)",
                  "ledger.n_min": "the FWD-NMIN assertion of the spec tool (the build HALTs there, L-L.14)"}
FLOW_HALT_T = {"ledger.opening": "FWD-OPENING", "ledger.n_min": "FWD-NMIN"}
SHADOW_T = {"ledger.opening": ('    return PINS.iso_ms(PINS.pin("ledger.opening"))\n', "    return COPY_T\n",
                               OPENING_MS_T),
            "ledger.n_min": ('    return PINS.pin("ledger.n_min")\n', "    return COPY_T\n", N_MIN_T),
            "adm.lag_cut": ('    return PINS.pin("adm.lag_cut")\n', "    return COPY_T\n", CUT_T)}
PIN_ISO_T = "%Y-%m-%dT%H:%MZ"
CONTROL_PIN_MS_T = 1791489600000                # the control ledger's refresh pin (any instant past X's)
# the control's typed rows: (book, symbol, entry bar in 4h bars past the opening, lag, band)
CONTROL_BASE_T = (("BTCUSDT", 2, 3, "B2"), ("ETHUSDT", 4, 3, "B4"), ("SOLUSDT", 6, 16, "B2"))
CONTROL_912_T = (("SOLUSDT", 8, 3, "B2"),)
CONTROL_KEPT_T = {"gated-v6-oldtide": ("BTCUSDT", "SOLUSDT"), BOOK4_T: ("BTCUSDT",)}
ROW_T = {
    "kind": "row", "direction": 1, "lane": "card", "arm_i": 15000, "exit_reason": "stop", "bars_held": 5,
    "entry_px": 100.0, "exit_px": 101.5, "stop_px": 98.0, "r_dist": 2.0, "atr_at_entry": 1.25, "net_r": 0.7,
    "gross_r": 0.75, "fee_r": 0.04, "funding_r": 0.01, "mfe_r": 1.1, "n_advances": 0, "harvested": False,
    "harvest_ms": None, "reached_1r": True, "era_of_entry": "holdout", "tide_state_entry": 1,
    "tide_streak_entry": 40, "tide_left_censored": False, "tide_trailing_edge_q25": 20.0,
    "tide_trailing_edge_q50": 60.0, "tide_trailing_edge_q75": 150.0, "tide_abs_gt206": False,
    "tide_streak_age_arm": 30, "tide_streak_age_arm_censored": False,
}

CTX: dict = {}                                   # the run: the record's bytes, the sources, the scratch


def halt(msg: str):
    raise SystemExit(f"HALT: {msg}")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def rd(rel: str) -> bytes:
    """This suite's own read of a file of record (x_rec stands in the main tree only)."""
    return ((MAIN if rel.startswith(XR_T + "/") else ROOT) / rel).read_bytes()


def put(name: str, raw: bytes) -> Path:
    """A scratch file under $TMPDIR, each in a directory of its own."""
    d = Path(tempfile.mkdtemp(prefix="f_", dir=CTX["tmp"]))
    (d / name).write_bytes(raw)
    return d / name


def jl(raw: bytes) -> list:
    """This suite's own split of ledger bytes: on the newline BYTE, never str.splitlines."""
    return [json.loads(x) for x in raw.decode("utf-8").split("\n") if x]


def dump(entries) -> bytes:
    """The bytes forward_log writes: the default-separator dump of each entry and a newline."""
    return b"".join((json.dumps(e, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8") for e in entries)


def own_hash(entry: dict, prev: str) -> str:
    """The chain law by this suite's OWN loop (no forward_log call)."""
    body = {k: v for k, v in entry.items() if k != "entry_sha256"}
    return sha((json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + prev).encode("utf-8"))


def rechain(entries, start: int = 0) -> list:
    """A deep copy with every line from `start` on re-chained by the suite's own loop — a FORGED-THROUGH file."""
    out = copy.deepcopy(list(entries))
    prev = out[start - 1]["entry_sha256"] if start else ZEROS_T
    for e in out[start:]:
        e["prev_sha256"] = prev
        e["entry_sha256"] = own_hash(e, prev)
        prev = e["entry_sha256"]
    return out


def extend(entries, bodies) -> list:
    """`entries` plus `bodies`, each chained on the head before it (own loop)."""
    return rechain(list(entries) + [dict(b) for b in bodies], len(entries))


def bent(entries, i: int, **fields) -> list:
    out = copy.deepcopy(list(entries))
    out[i].update(fields)
    return out


def verdict(found, why: str) -> tuple:
    return (not found), (why if not found else f"{len(found)} finding(s): " + " | ".join(str(x) for x in found))


def judged(real_leg):
    """A HALT of production inside a REAL leg is that leg's FAIL, with the HALT's own text."""
    def leg():
        try:
            return real_leg()
        except SystemExit as e:
            return False, f"production HALTed — {e}"
    return leg


def halted(thunk) -> list:
    """A production call that must HALT: its HALT text as a finding, [] if it did not."""
    try:
        thunk()
    except SystemExit as e:
        return [str(e)]
    return []


def git(*args) -> bytes:
    """A read-only git call on the tree this suite stands in."""
    r = subprocess.run(["git", "--no-optional-locks", "-C", str(ROOT), *args], capture_output=True)
    if r.returncode:
        raise RuntimeError(f"git {args[0]} failed: {r.stderr.decode('utf-8', 'replace').strip()[:200]}")
    return r.stdout


def manifest_row(rel: str) -> dict:
    rows = {r["copy"]: r for r in json.loads(rd(X_MANIFEST_T).decode("utf-8"))["files"]}
    return rows[rel]


def t11_progress() -> dict:
    raw = rd(T11_PROGRESS_T)
    r0 = PG.records(ROOT)["TC12-R0"][R0_KEY_T][T11_PROGRESS_T]["sha256"]
    stamp = ROOT / STAMP_MAP_T
    moved = json.loads(stamp.read_text(encoding="utf-8")) if stamp.is_file() else {}
    ok = sha(raw) == r0 or (moved.get("applied") is True and any(
        r.get("path") == T11_PROGRESS_T and r.get("sha256_after") == sha(raw) for r in moved.get("moved", [])))
    if not ok:
        raise RuntimeError(f"{T11_PROGRESS_T} is neither at its R0 sha nor at a stamped value")
    return json.loads(raw.decode("utf-8"))


def t11_entry(rel: str) -> dict:
    hits = [s["artifact_shas"][rel] for s in t11_progress()["stages"] if rel in s.get("artifact_shas", {})]
    return hits[-1]


# ═══════════════════════════════════════════════════════ THE CONTROL LEDGER (five lines + one lawful block)
def fx_row(book: str, symbol: str, bar: int, lag: int, band: str, roles: str, names) -> dict:
    """One synthetic row line body in X's field order plus the six added names — typed values, no outcome of
    any book.  The three gate booleans are PRODUCTION's predicates on the row's own band and lag."""
    entry_ms = OPENING_MS_T + bar * H4_MS_T
    r = dict(ROW_T, book=book, symbol=symbol, entry_ms=entry_ms, roles_name=roles, lag=lag,
             arm_ms=entry_ms - lag * H4_MS_T, entry_i=ROW_T["arm_i"] + lag, entry_close_ms=entry_ms + H4_MS_T,
             exit_i=ROW_T["arm_i"] + lag + ROW_T["bars_held"], exit_ms=entry_ms + ROW_T["bars_held"] * H4_MS_T,
             exit_close_ms=entry_ms + (ROW_T["bars_held"] + 1) * H4_MS_T, tide_band=band,
             tide_band_label=f"{band} (a typed label)")
    if sorted(r) != sorted(names):
        raise ValueError(f"the typed row names differ from X's row_fields on {sorted(set(r) ^ set(names))}")
    row = {k: r[k] for k in names}
    row["p_age_1_refuses"] = SPEC.p_age_1_refuses(row)
    row["p_win_1_refuses"] = SPEC.p_win_1_refuses(row)
    row["p_adm_1_refuses"] = SPEC.p_adm_1_refuses(row)
    row["in_o9_scored_window"] = OPENING_MS_T < row["entry_close_ms"] <= SCORE_EDGE_MS_T
    row["entered_before_gate_text_filed"] = row["entry_close_ms"] <= STEP_Q_T["instant_ms"]
    row["entered_before_book_frozen"] = True      # no freeze instant exists yet: every typed row predates it
    return row


def control_bodies(names) -> list:
    """The lawful block: base rows, the 9/12 row, each gated book = its base minus what PRODUCTION's
    predicate refuses, in book order then (entry_close_ms, symbol); then one refresh line."""
    base = [fx_row("v6", s, bar, lag, band, "v6-roles", names) for s, bar, lag, band in CONTROL_BASE_T]
    r912 = [fx_row("trg912", s, bar, lag, band, "trigger-9/12", names) for s, bar, lag, band in CONTROL_912_T]
    old = [dict(r, book="gated-v6-oldtide") for r in base if not SPEC.p_age_1_refuses(r)]
    adm = [dict(r, book=BOOK4_T) for r in base if not SPEC.p_adm_1_refuses(r)]
    order = lambda rows: sorted(rows, key=lambda r: (r["entry_close_ms"], r["symbol"]))
    refresh = {"kind": "refresh", "tier": "TIER-C12", "pin_ms": CONTROL_PIN_MS_T,
               "note": "a fixture's control refresh line — not the refresh of record"}
    return order(base) + order(r912) + order(old) + order(adm) + [refresh]


def control() -> list:
    """The control's entries, appended to a scratch copy of the five-line file by PRODUCTION's guarded
    append (forward_log's law as the spec module carries it)."""
    if "control" not in CTX:
        p = put("control.jsonl", CTX["five"])
        SPEC.append(p, control_bodies(CTX["x_spec"]["row_fields"]))
        CTX["control_raw"] = p.read_bytes()
        CTX["control"] = jl(CTX["control_raw"])
    return CTX["control"]


def row_at(book: str, symbol: str) -> int:
    hit = [i for i, e in enumerate(control()) if e.get("kind") == "row" and (e["book"], e["symbol"]) == (book, symbol)]
    return hit[0]


# ═══════════════════════════════════════════════════════ THE DETECTORS (each finding names its detector)
def prefix_fx(raw: bytes, x_bytes: bytes, row: dict, blobs=()) -> list:
    out = []
    if raw[:len(x_bytes)] != x_bytes:
        at = next((i for i, (a, b) in enumerate(zip(raw, x_bytes)) if a != b), min(len(raw), len(x_bytes)))
        out.append(f"PREFIX-BYTES record[:N_X] is not the x_rec copy of X's ledger (first differing byte at "
                   f"offset {at})")
    n = row["bytes"]
    if (n, sha(raw[:n]), row["sha256"]) != (X_LEDGER_BYTES_T, row["sha256"], X_LEDGER_SHA_T) or len(x_bytes) != n:
        out.append(f"PREFIX-SHA the first {n} bytes hash to {sha(raw[:n])}, the manifest row names "
                   f"{row['sha256']} ({n} B) and this suite types {X_LEDGER_SHA_T} ({X_LEDGER_BYTES_T} B)")
    chain = list(blobs) + [raw]
    for i, (a, b) in enumerate(zip(chain, chain[1:])):
        if not b.startswith(a):
            out.append(f"PREFIX-COMMITS the ledger blob of commit {i + 1} is not a byte-prefix of "
                       + ("the next commit's blob" if i + 2 < len(chain) else "the working file"))
    return out


def ledger_blobs() -> list:
    """The ledger's blob at every `tierc12(` commit that touches it, oldest first (read-only git)."""
    log = git("log", "--reverse", "--format=%H%x09%s", "--", LEDGER_T).decode("utf-8")
    shas = [x.split("\t", 1)[0] for x in log.splitlines() if x.split("\t", 1)[1].startswith("tierc12(")]
    return [git("show", f"{c}:{LEDGER_T}") for c in shas]


class BareToken(ValueError):
    pass


def _no_constant(token):
    raise BareToken(token)


def chain_fx(raw: bytes) -> list:
    out = []
    p = put("ledger.jsonl", raw)
    try:
        v = FLREF.verify_chain(p)
        if not v["ok"]:
            out.append(f"CHAIN-FL forward_log.verify_chain breaks at line {v['first_bad_line']}: {v['reason']}")
    except ValueError as e:
        v = f"ValueError: {e}"
        out.append(f"CHAIN-FL forward_log cannot read the file ({e})")
    try:
        w = SPEC.verify_chain(p)
    except ValueError as e:
        w = f"ValueError: {e}"
    if w != v:
        out.append(f"CHAIN-PORT the ported verify_chain returns {w!r}, forward_log's own {v!r}")
    texts = raw.decode("utf-8").split("\n")
    if texts[-1] != "":
        out.append("CHAIN-BYTES the file does not end on a newline")
    prev = ZEROS_T
    for i, t in enumerate(texts[:-1], 1):
        try:
            e = json.loads(t, parse_constant=_no_constant)
        except BareToken as x:
            out.append(f"CHAIN-NAN line {i} holds the bare token {x}")
            e = json.loads(t)
        except ValueError as x:
            out.append(f"CHAIN-BYTES line {i} is not one JSON object ({x})")
            continue
        if len(t.splitlines()) != 1:
            out.append(f"CHAIN-LINE-BREAK line {i} holds a str.splitlines boundary other than its final newline")
        if json.dumps(e, sort_keys=True, ensure_ascii=False) != t:
            out.append(f"CHAIN-BYTES line {i} is not the default-separator dump of its parsed entry")
        if e.get("prev_sha256") != prev or own_hash(e, prev) != e.get("entry_sha256"):
            out.append(f"CHAIN-OWN line {i}: this suite's own hash loop does not reproduce its chain fields")
        prev = e.get("entry_sha256")
    return out


def structure_fx(raw: bytes, spec_bytes=None) -> list:
    """PRODUCTION's structure law (S1-S7) on scratch bytes."""
    return SPEC.chain_findings(put("ledger.jsonl", raw), CTX["spec_bytes"] if spec_bytes is None else spec_bytes,
                               CTX["x_spec_bytes"], CTX["x_ledger"])


def first_five(raw: bytes) -> bytes:
    """The first five whole lines of ledger bytes — the bytes this record files."""
    parts = raw.split(b"\n")
    if len(parts) <= N5_T:
        halt(f"{LEDGER_T} holds fewer than {N5_T} whole lines")
    return b"\n".join(parts[:N5_T]) + b"\n"


def working_fx(fx, raw: bytes) -> list:
    """A detector over a WORKING file as the real legs of [CHAIN] and [STRUCTURE] read it: over its first five
    lines — the bytes this record files — and then over the WHOLE of it, so a line standing after line 5 is
    judged where it stands [L-L.7: FAILS IF the chain is not ok / any of S2-S7 is breached].  A finding the
    five lines already gave is not said twice."""
    base = fx(first_five(raw))
    return base + [f"{x} — judged on the WHOLE working file (past its first {N5_T} lines)"
                   for x in fx(raw) if x not in base]


def rehash_fx(raw: bytes, spec_bytes: bytes, x_spec_bytes: bytes) -> list:
    out, lines = [], jl(raw)
    named = lines[N_X_LINES_T].get("spec_sha256")
    if named in (sha(x_spec_bytes), X_SPEC_SHA_T):
        out.append(f"REHASH FWD-SPEC-REUSED ledger line {N5_T} names X's spec sha — the fourth book must re-hash")
    elif named != sha(spec_bytes):
        out.append(f"REHASH-LINE5 ledger line {N5_T} names {named}, the spec's bytes hash to {sha(spec_bytes)}")
    bad = [i + 1 for i, x in enumerate(lines[:N_X_LINES_T]) if x.get("spec_sha256") != X_SPEC_SHA_T]
    if bad:
        out.append(f"REHASH-X-SHA ledger line(s) {bad} name another spec sha than X's")
    if not sha(x_spec_bytes) == manifest_row(X_SPEC_T)["sha256"] == X_SPEC_SHA_T:
        out.append("REHASH-X-COPY the x_rec copy of X's spec does not hash to its manifest row and the typed sha")
    return out


def frozen_fx(spec_bytes: bytes, S=None) -> list:
    """PRODUCTION's write-once law: the spec rebuilt now from (a copy of) its sources against `spec_bytes`
    standing as the file."""
    d = put("BOOK_SPEC_COMBINED.json", spec_bytes).parent
    return halted(lambda: SPEC.freeze_spec(d, SPEC.render_json(SPEC.spec_doc(CTX["S"] if S is None else S))))


def t11_mirror(raw: bytes) -> tuple:
    """(lines, findings): TC11's chain law by this suite's own mirror — canonical compact JSON, line_sha256
    over the line without it, `prev` inside the line."""
    out, lines, prev = [], [], ZEROS_T
    canon = lambda o: json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    for i, t in enumerate(raw.decode("utf-8", "replace").split("\n")[:-1], 1):
        try:
            e = json.loads(t)
        except ValueError:
            out.append(f"ANCESTOR-TC11-CHAIN line {i} does not parse")
            break
        if canon(e) != t or sha(canon({k: v for k, v in e.items() if k != "line_sha256"}).encode("utf-8")) \
                != e.get("line_sha256") or e.get("prev") != prev:
            out.append(f"ANCESTOR-TC11-CHAIN line {i} does not verify under TC11's own law")
        prev = e.get("line_sha256")
        lines.append(e)
    return lines, out


def fact_fx(t11_lines, x_spec, x_lines) -> list:
    """ANCESTOR-FACT: a fact both ancestors state, held equal and to this suite's typed value."""
    if len(t11_lines) < 2:
        return ["ANCESTOR-FACT TC11's ledger holds fewer than two lines"]
    g, r, xr = t11_lines[0], t11_lines[-1], x_lines[-1]
    facts = {
        "the opening": (g.get("opening_ms"), x_spec["opening"]["ms"], OPENING_MS_T),
        "n_score == n_min": (g.get("n_score"), x_spec["n_min"], N_MIN_T),
        "the panel": (g.get("panel"), x_spec["books"]["v6"]["panel"], x_spec["books"]["trg912"]["panel"]),
        "the line shas": ((g.get("line_sha256"), r.get("line_sha256")), (T11_GENESIS_T, T11_HEAD_T),
                          (T11_GENESIS_T, T11_HEAD_T)),
        "the refresh pin": (r.get("pin_ms"), xr.get("pin_ms"), SCORE_EDGE_MS_T),
        "the corridor's lower bound": (r.get("corridor_lo_ms"), x_spec["pool_lo_ms"], POOL_LO_MS_T),
    }
    for b in ("v6", "trg912"):
        roles = g.get("books", {}).get(b, {}).get("roles", {})
        xb = x_spec["books"][b]
        periods = {k: v for k, v in roles.items() if k != "name"}
        facts[f"{b}: the roles name"] = (roles.get("name"), xb["roles_name"], xb["roles_name"])
        facts[f"{b}: the six periods"] = ({k: repr(v) for k, v in periods.items()}, xb["ride_spec"]["roles_fields"],
                                          xb["ride_spec"]["roles_fields"])
        facts[f"{b}: the book sha at the score edge"] = (r.get("books", {}).get(b, {}).get("book_sha"),
                                                         x_spec["x_found_books"]["book_sha"][b],
                                                         xr["anchor_x_found_books"]["book_sha"][b])
        facts[f"{b}: the open keys"] = ([x.get("key") for x in r.get("books", {}).get(b, {}).get("open", [])],
                                        xr["books"][b]["open_keys"], xr["books"][b]["open_keys"])
    return [f"ANCESTOR-FACT {k}: TC11 states {a!r}, X states {b!r}" for k, (a, b, c) in facts.items()
            if not a == b == c]


def ancestor_fx(files: dict) -> list:
    """ANCESTOR-PIN / ANCESTOR-TC11-CHAIN / ANCESTOR-FACT on the four ancestor files' bytes."""
    out = []
    pins = {X_LEDGER_T: (manifest_row(X_LEDGER_T)["sha256"], X_LEDGER_SHA_T),
            X_SPEC_T: (manifest_row(X_SPEC_T)["sha256"], X_SPEC_SHA_T),
            T11_LEDGER_T: (t11_entry(T11_LEDGER_T)["sha256"], T11_LEDGER_SHA_T,
                           PG.records(ROOT)["TC12-R0"][R0_KEY_T][T11_LEDGER_T]["sha256"]),
            T11_PAGE_T: (t11_entry(T11_PAGE_T)["sha256"],)}
    for rel, want in pins.items():
        if set(want) != {sha(files[rel])}:
            out.append(f"ANCESTOR-PIN {rel} hashes to {sha(files[rel])}, its pin(s) read {sorted(set(want))}")
    t11_lines, bad = t11_mirror(files[T11_LEDGER_T])
    out += bad
    if not bad:
        out += fact_fx(t11_lines, json.loads(files[X_SPEC_T].decode("utf-8")), jl(files[X_LEDGER_T]))
    return out


def ancestor_files() -> dict:
    return {rel: rd(rel) for rel in (X_LEDGER_T, X_SPEC_T, T11_LEDGER_T, T11_PAGE_T)}


def payload_sha_fx(body: dict) -> str:
    b = {k: v for k, v in body.items() if k not in ("text_sha256", "sha256")}
    return sha(json.dumps(b, sort_keys=True, ensure_ascii=False).encode("utf-8"))


def head_fx(bodies) -> str:
    prev = ZEROS_T
    for r in bodies:
        line = {"seq": r.get("seq"), "registration": r.get("registration"), "sha256": payload_sha_fx(r), "prev": prev}
        prev = sha(json.dumps(line, sort_keys=True).encode())
    return prev


def resealed(S: dict, key: str, rid: str, edit) -> dict:
    """A deep copy of the sources with one registration of registry `key` edited and the copy RESEALED —
    payload sha, chain and head recomputed, the pin's head following — so only the text law can see it."""
    S2 = copy.deepcopy(S)
    doc = S2[key]
    body = next(r for r in doc["registrations"] if r["registration"] == rid)
    edit(body["operative_spec"])
    body["sha256"] = payload_sha_fx(body)
    doc["head"] = head_fx(doc["registrations"])
    if key == "registry":
        S2["registry_pin"]["head"] = doc["head"]
    return S2


def scored_index(arms) -> int:
    return next(i for i, x in enumerate(arms) if SCORED_RX_T.match(x))


def spec_value_fx(doc: dict) -> list:
    """SPEC-VALUE / SPEC-PATH: a value of a spec document that is not its source's, by this suite's own read
    of each source and its typed commission."""
    out = []
    xs = json.loads(rd(X_SPEC_T).decode("utf-8"))
    xl = jl(rd(X_LEDGER_T))
    reg, pin = json.loads(rd(REG_T).decode("utf-8")), json.loads(rd(REG_PIN_T).decode("utf-8"))
    t11, t11_pin = json.loads(rd(T11_REG_T).decode("utf-8")), json.loads(rd(T11_PIN_T).decode("utf-8"))
    adm = next(r for r in reg["registrations"] if r["registration"] == "P-ADM-1")
    age = next(r for r in t11["registrations"] if r["registration"] == "P-AGE-1")
    win = next(r for r in t11["registrations"] if r["registration"] == "P-WIN-1")
    scored = [x for x in adm["operative_spec"]["arms"] if SCORED_RX_T.match(x)]
    book = doc.get("books", {}).get(BOOK4_T, {})
    gate = book.get("gate", {})
    old, stale = gate.get("components", {}).get("old", {}), gate.get("components", {}).get("stale", {})
    pre = PINS.prefix()
    xgate = xs["books"]["gated-v6-oldtide"]["gate"]
    want = {
        "the key set": (tuple(sorted(doc)), SPEC_KEYS_T),
        "tier · stage · book": ((doc.get("tier"), doc.get("stage"), doc.get("book")), ("TIER-C12", STAGE_SPEC_T, BOOK4_T)),
        "book_order": (doc.get("book_order"), list(X_BOOKS_T) + [BOOK4_T]),
        "contract": (doc.get("contract"), {"path": pre["path"], "prefix_bytes": pre["prefix_bytes"],
                                           "prefix_sha256": pre["prefix_sha256"]}),
        "leans_sha256": (doc.get("leans_sha256"), sha(rd(LEANS_T))),
        "registry": (doc.get("registry"), {"path": REG_T, "head": pin["head"]}),
        "registry head recomputed": (head_fx(reg["registrations"]), pin["head"]),
        "the v6 ride_spec, card, roles and panel": (
            [book.get(k) for k in ("ride_spec", "card_name", "roles_name", "panel")],
            [xs["books"]["v6"][k] for k in ("ride_spec", "card_name", "roles_name", "panel")]),
        "role · runner": ((book.get("role"), book.get("runner")), ("of record", xs["books"]["gated-v6-oldtide"]["runner"])),
        "the ONE scored element": (len(scored), 1),
        "gate.text_of_record": (gate.get("text_of_record"), scored[0] if len(scored) == 1 else None),
        "gate.text_sha256": (gate.get("text_sha256"), sha(str(gate.get("text_of_record")).encode("utf-8"))),
        "gate.p_adm_1_payload_sha256": (gate.get("p_adm_1_payload_sha256"), adm["sha256"], payload_sha_fx(adm),
                                        pin["registrations"]["P-ADM-1"]["sha256"]),
        "gate.combine · base_book · none_band": ((gate.get("combine"), gate.get("base_book"), gate.get("none_band")),
                                                 ("OR", "v6", "HALT")),
        "gate.kind · stamps_only · rivals": ([gate.get(k) for k in ("kind", "stamps_only", "rivals")],
                                             [xgate[k] for k in ("kind", "stamps_only", "rivals")]),
        "components.old text and payload": ((old.get("text_of_record"), old.get("payload_sha256")),
                                            (age["operative_spec"]["scored_arm"], payload_sha_fx(age)),
                                            (xgate["text_of_record"], xgate["p_age_1_payload_sha256"])),
        "components.old by object": ([old.get(k) for k in ("refuse", "lineage_functions", "band_quantiles",
                                                           "min_pool_bars", "pool_lo_ms")],
                                     [xgate[k] for k in ("refuse", "lineage_functions", "band_quantiles",
                                                         "min_pool_bars", "pool_lo_ms")]),
        "components.old.code": (old.get("code"), OLD_T),
        "components.stale text and payload": ((stale.get("text_of_record"), stale.get("payload_sha256")),
                                              (win["operative_spec"]["scored_arm"], payload_sha_fx(win))),
        "components.stale.cut": ((stale.get("cut", {}).get("value"), stale.get("cut", {}).get("tc11_capture", {}).get("value")),
                                 (CUT_T, CUT_T)),
        "tc11_registry head": (doc.get("tc11_registry", {}).get("head"), t11_pin["head"], head_fx(t11["registrations"]),
                               T11_REG_HEAD_T),
        "tc11_registry payload shas": ((doc.get("tc11_registry", {}).get("p_age_1_payload_sha256"),
                                        doc.get("tc11_registry", {}).get("p_win_1_payload_sha256")),
                                       (age["sha256"], win["sha256"])),
        "existing_books": (doc.get("existing_books"),
                           {"spec": manifest_row(X_SPEC_T)["x_path"], "copy": X_SPEC_T, "sha256": X_SPEC_SHA_T,
                            "book_open_entry_sha256": {x["book"]: x["entry_sha256"] for x in xl[:len(X_BOOKS_T)]}}),
        "ancestors.x_ledger": ({k: doc.get("ancestors", {}).get("x_ledger", {}).get(k)
                                for k in ("bytes", "sha256", "n_lines", "head", "copy")},
                               {"bytes": X_LEDGER_BYTES_T, "sha256": X_LEDGER_SHA_T, "n_lines": N_X_LINES_T,
                                "head": X_HEAD_T, "copy": X_LEDGER_T}),
        "ancestors.tc11_ledger": ({k: doc.get("ancestors", {}).get("tc11_ledger", {}).get(k)
                                   for k in ("path", "sha256", "n_lines", "genesis_line_sha256", "head_line_sha256",
                                             "verified", "continued")},
                                  {"path": T11_LEDGER_T, "sha256": T11_LEDGER_SHA_T, "n_lines": 2,
                                   "genesis_line_sha256": T11_GENESIS_T, "head_line_sha256": T11_HEAD_T,
                                   "verified": True, "continued": False}),
        "opening": (doc.get("opening"), xs["opening"]),
        "opening.ms · iso": ((doc.get("opening", {}).get("ms"), doc.get("opening", {}).get("iso")),
                             (OPENING_MS_T, OPENING_ISO_T)),
        "opening_rival · admission · append_law · refresh_law · ctrl_cols": (
            [doc.get(k) for k in ("opening_rival", "admission", "append_law", "refresh_law", "ctrl_cols")],
            [xs[k] for k in ("opening_rival", "admission", "append_law", "refresh_law", "ctrl_cols")]),
        "scored_window_end_ms": (doc.get("scored_window_end_ms"), SCORE_EDGE_MS_T),
        "n_min": (doc.get("n_min"), N_MIN_T),
        "pool_lo_ms": (doc.get("pool_lo_ms"), POOL_LO_MS_T),
        "row_fields": (doc.get("row_fields"), xs["row_fields"]),
        "the count of X's row names": (len(doc.get("row_fields", [])), N_ROW_FIELDS_T),
        "row_fields_added": (tuple(doc.get("row_fields_added", [])), ADDED_T),
        "row_nullable": (doc.get("row_nullable"),
                         list(ast.literal_eval(PINS.literal_node(rd(XF_T).decode("utf-8"), "ROW_NULLABLE")))),
        "flags.step_q": (doc.get("flags", {}).get("step_q"), STEP_Q_T),
        "flags.book_frozen.record": (doc.get("flags", {}).get("book_frozen", {}).get("record"),
                                     FORWARD_T + "/BOOK4_FREEZE.json"),
        "the three flag definitions": (sorted(k for k in doc.get("flags", {}) if k not in ("step_q", "book_frozen")),
                                       sorted(ADDED_T[3:])),
        "n_law.row_set_of_record": (doc.get("n_law", {}).get("row_set_of_record"), N_LAW_T),
        "n_law.x_n_law": (doc.get("n_law", {}).get("x_n_law"), xs["n_law"]),
        "n_law.chooser": (str(doc.get("n_law", {}).get("chooser", "")).startswith("none"), True),
        "chain": ({k: v for k, v in doc.get("chain", {}).items() if k != "structure_law"}, xs["chain"]),
        "chain.structure_law": ([str(x).split(" ", 1)[0] for x in doc.get("chain", {}).get("structure_law", [])],
                                [f"S{i}" for i in range(1, 8)]),
        "continuation": ({k: doc.get("continuation", {}).get(k) for k in ("x_prefix_bytes", "x_prefix_sha256",
                                                                         "first_tc12_line")},
                         {"x_prefix_bytes": X_LEDGER_BYTES_T, "x_prefix_sha256": X_LEDGER_SHA_T,
                          "first_tc12_line": N5_T}),
    }
    for k, vals in want.items():
        if any(v != vals[0] for v in vals[1:]):
            out.append(f"SPEC-VALUE {k}: the spec reads {vals[0]!r}, its source(s) {list(vals[1:])!r}"[:400])
    paths = doc.get("path_modules", {})
    carried = {p: s for p, s in xs["path_modules"].items() if not p.startswith("scripts/tc11x_")}
    if sorted(paths) != sorted(carried) or len(paths) != N_LINEAGE_T:
        out.append(f"SPEC-PATH path_modules names {len(paths)} files, not the {N_LINEAGE_T} lineage files X's spec names")
    out += [f"SPEC-PATH {p}: the spec reads {paths.get(p)}, X's spec {s}, the file now {sha(rd(p))}"
            for p, s in sorted(carried.items()) if not paths.get(p) == s == sha(rd(p))]
    return out


def step_q_git_fx() -> list:
    """The STEP Q instant the spec files against git's committer time of that commit (read-only)."""
    ct = int(git("show", "-s", "--format=%ct", STEP_Q_T["commit"]).decode("utf-8").strip()) * 1000
    return [] if ct == STEP_Q_T["instant_ms"] else [
        f"SPEC-VALUE flags.step_q: git's committer time of {STEP_Q_T['commit']} is {ct} ms, typed {STEP_Q_T['instant_ms']}"]


def _fn(call: ast.Call) -> str:
    f = call.func
    return f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")


def _io(call: ast.Call) -> bool:
    """A call that opens, writes, moves or lists a file: the path methods of IO_ATTRS_T, the builtin open,
    and anything on the os / shutil modules."""
    f = call.func
    if isinstance(f, ast.Name):
        return f.id == "open"
    if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) and f.value.id in IO_MODULES_T:
        return True
    return isinstance(f, ast.Attribute) and f.attr in IO_ATTRS_T


def spec_ast_fx(src: str) -> list:
    """SPEC-ENV-FREE (imports) · SPEC-READS (the typed read list and the open sites) · SPEC-VA-BLIND."""
    out, tree = [], ast.parse(src)
    for n in ast.walk(tree):
        names = [a.name for a in n.names] if isinstance(n, ast.Import) else \
            [n.module or ""] if isinstance(n, ast.ImportFrom) else []
        for m in names:
            top = m.split(".")[0]
            if top not in sys.stdlib_module_names and top not in IMPORTS_T:
                out.append(f"SPEC-ENV-FREE the spec tool imports {m} — only the stdlib and {list(IMPORTS_T)} are lawful")
    try:
        reads = tuple(FX.literal_from_text(src, "SPEC_READS_T"))
    except (ValueError, SyntaxError, KeyError):
        reads = None
    if reads != SPEC_READS_T:
        out.append("SPEC-READS the tool's SPEC_READS_T is not this suite's typed list"
                   + (f": {sorted(set(reads or ()) ^ set(SPEC_READS_T))}" if reads is not None else ""))
    parents = {c: p for p in ast.walk(tree) for c in ast.iter_child_nodes(p)}
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and _io(n):
            f = n
            while f in parents and not isinstance(f, ast.FunctionDef):
                f = parents[f]
            where = f.name if isinstance(f, ast.FunctionDef) else "<module>"
            if where not in OPEN_SITES_T:
                out.append(f"SPEC-READS {_fn(n)}(…) in {where}() — an open site outside {list(OPEN_SITES_T)}")
    held = [c.value for c in ast.walk(tree) if isinstance(c, ast.Constant) and isinstance(c.value, str)]
    for tok in BLIND_TOKENS_T:
        if any(tok in s for s in held) or any(tok in p for p in (reads or ())):
            out.append(f"SPEC-VA-BLIND the tool's source holds the path token {tok!r} — it may open no tape, "
                       f"book or value-area table")
    return out


def tool_src() -> str:
    return (ROOT / TOOL_T).read_text(encoding="utf-8")


def mut(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise RuntimeError(f"the plant's anchor occurs {text.count(old)} time(s), not once: {old[:60]!r}")
    return text.replace(old, new)


def _blank(node):
    for c in ast.walk(node):
        if isinstance(c, ast.Constant) and isinstance(c.value, str):
            c.value = ""
    return node


def _def(text: str, name: str):
    hit = [n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef) and n.name == name]
    return hit[0] if len(hit) == 1 else None


def port_fx(own: str) -> list:
    """PORT-*: a port whose label is untrue of its source text at its pinned sha."""
    out = []
    xs = json.loads(rd(X_SPEC_T).decode("utf-8"))
    pinned = {FL_T: xs["path_modules"][FL_T], XF_T: manifest_row(XF_T)["sha256"]}
    seen = {}
    for label, src_rel, a, b, hexsha, name in PORT_RX.findall(own):
        seen[name] = label
        if src_rel not in pinned:
            out.append(f"PORT-SHA {name}: the provenance comment names {src_rel}, a source with no pin")
            continue
        text = rd(src_rel).decode("utf-8")
        if not hexsha == pinned[src_rel] == sha(rd(src_rel)):
            out.append(f"PORT-SHA {name}: the provenance comment names sha {hexsha}; the source's pin is "
                       f"{pinned[src_rel]}")
        theirs, ours = _def(text, name), _def(own, name)
        if theirs is None or ours is None:
            out.append(f"PORT-LINES {name}: not one module-level function of that name on both sides")
            continue
        if (theirs.lineno, theirs.end_lineno) != (int(a), int(b)):
            out.append(f"PORT-LINES {name}: the comment names lines {a}-{b}; the source defines it at "
                       f"{theirs.lineno}-{theirs.end_lineno}")
        same = ast.dump(theirs) == ast.dump(ours)
        if label == "VERBATIM" and not same:
            out.append(f"PORT-VERBATIM {name}: labelled VERBATIM and not AST-identical to {src_rel}")
        if label == "TEXT-ONLY" and ast.dump(_blank(theirs)) != ast.dump(_blank(ours)):
            out.append(f"PORT-TEXT-ONLY {name}: labelled TEXT-ONLY and not AST-identical once string constants are blanked")
        if label == "CHANGED" and same:
            out.append(f"PORT-CHANGED {name}: labelled CHANGED and AST-identical to its source — the label is untrue")
        if name == "last_sha" and label == "CHANGED":
            seg = ast.get_source_segment(text, _def(text, name))
            if seg.count(LAST_SHA_T[0]) != 1 or ast.dump(ast.parse(seg.replace(*LAST_SHA_T)).body[0]) != ast.dump(_def(own, name)):
                out.append(f"PORT-CHANGED-DECLARED {name}: differs from forward_log's function by more than the one "
                           f"declared index token")
    if seen != PORTS_T:
        out.append(f"PORT-MISSING the ports and labels found {sorted(seen.items())} are not the typed "
                   f"{sorted(PORTS_T.items())}")
    xf = rd(XF_T).decode("utf-8")
    held = {"CHAIN_FIELDS": tuple(FX.literal_from_text(own, "CHAIN_FIELDS")),
            "KINDS": (SPEC.K_OPEN, SPEC.K_REFRESH, SPEC.K_ROW)}
    for name, want in X_LITERALS_T.items():
        theirs = tuple(ast.literal_eval(PINS.literal_node(xf, name)))
        if not held[name] == theirs == want:
            out.append(f"PORT-LITERAL {name}: the module holds {held[name]}, X's source {theirs}, typed {want}")
    return out


def shadow(pin: str):
    """A SHADOW COPY of the spec module that holds a typed copy of EQUAL value in place of the pin's read."""
    old, new, value = SHADOW_T[pin]
    src = mut(tool_src(), old, new) + f"\nCOPY_T = {value!r}\n"
    name = "shadow_" + pin.replace(".", "_")
    p = put(name + ".py", src.encode("utf-8"))
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.ROOT = ROOT
    return mod


def bent_value(pin: str):
    v = PINS.pin(pin)
    if pin == "ledger.opening":                  # one 4h bar later, in the contract's own form
        t = datetime.strptime(v, PIN_ISO_T).replace(tzinfo=timezone.utc) + timedelta(milliseconds=H4_MS_T)
        return t.strftime(PIN_ISO_T)
    return v - 1


def flow_fx(mod, pin: str) -> list:
    """The flow leg [L-0.17]: the pin bent AT ITS DOOR, the smallest production function that reads it
    re-run.  [] = the witness moved; PIN-NOT-READ = nothing moved; PIN-FLOW-WRONG = the wrong thing moved."""
    kept = PINS.pin(pin)
    if pin == "adm.lag_cut":
        row = {"symbol": "PLANT", "entry_ms": 0, "lag": kept - 1, "tide_band": "B2"}
        before = mod.p_win_1_refuses(row)
        with PINS.bend(pin, bent_value(pin)):
            after = mod.p_win_1_refuses(row)
        out = [] if (before, after) == (False, True) else [
            f"PIN-NOT-READ {pin}: bent down by one at its door, `p_win_1_refuses` on the planted lag = CUT − 1 "
            f"row did not flip ({before} -> {after}) — the predicate holds a copy of the cut"] if before == after \
            else [f"PIN-FLOW-WRONG {pin}: the planted row read {before} -> {after}"]
    else:
        with PINS.bend(pin, bent_value(pin)):
            found = halted(lambda: mod.spec_doc(CTX["S"]))
        out = [] if any(FLOW_HALT_T[pin] in x for x in found) else \
            [f"PIN-NOT-READ {pin}: bent at its door, `spec_doc` did not HALT {FLOW_HALT_T[pin]} — the spec tool "
             f"holds a copy of the value"] if not found else [f"PIN-FLOW-WRONG {pin}: bent at its door, {found[0]}"]
    if PINS.pin(pin) != kept:
        out.append(f"PIN-FLOW-WRONG {pin}: the bend outlived its block")
    return out


def flow_line(pin: str) -> str:
    """L-0.17's fixed line.  Where the register's own witness moved it is the register's line; where the
    consumer's equality assertion is what moves at this record, the line says so in the same form."""
    if pin not in FLOW_WITNESS_T:
        return PINS.flow_line(pin)
    return PINS.FLOW_FORM.format(pin=pin, door=PINS.row(pin)["door"], witness=FLOW_WITNESS_T[pin])


# ═══════════════════════════════════════════════════════ F-LEDGER [PREFIX]
def rewritten() -> list:
    """Planted mutation 1: one digit of ledger line 2's opening_ms changed (nothing re-chained)."""
    return bent(CTX["five_lines"], 1, opening_ms=OPENING_MS_T + 1)


def prefix_break():
    F, x, row = CTX["five_lines"], CTX["x_ledger"], manifest_row(X_LEDGER_T)
    forged = dump(rechain(rewritten(), 1))
    if chain_fx(forged) or prefix_fx(CTX["five"], x, row):
        raise ValueError("the forged-through copy does not verify, or the record is not clean — the plants "
                         "would prove nothing")
    return FX.plants([
        ("a rewritten earlier line: one digit of line 2's opening_ms changed", "PREFIX-BYTES",
         lambda: prefix_fx(dump(rewritten()), x, row)),
        ("the same rewrite FORGED THROUGH — every later prev_sha256 / entry_sha256 recomputed, so the chain "
         "verifies", "PREFIX-BYTES", lambda: prefix_fx(forged, x, row)),
        ("a re-ordered line: lines 2 and 3 swapped", "PREFIX-BYTES",
         lambda: prefix_fx(dump([F[0], F[2], F[1], F[3], F[4]]), x, row)),
        ("a manifest row copy naming another sha for X's ledger", "PREFIX-SHA",
         lambda: prefix_fx(CTX["five"], x, dict(row, sha256=row["sha256"][::-1]))),
        ("a later commit whose ledger blob rewrites an earlier byte", "PREFIX-COMMITS",
         lambda: prefix_fx(CTX["five"], x, row, [x, forged])),
        ("a working file that lost the last committed line", "PREFIX-COMMITS",
         lambda: prefix_fx(x, x, row, [x, CTX["five"]])),
    ])


def prefix_real():
    row = manifest_row(X_LEDGER_T)
    found = prefix_fx(CTX["raw"], CTX["x_ledger"], row, ledger_blobs())
    rec = PG.records(ROOT).get(STAGE_SPEC_T, {}).get("artifact_shas", {}).get(LEDGER_T)
    if rec is not None and rec != {"bytes": len(CTX["five"]), "sha256": sha(CTX["five"])}:
        found.append(f"PREFIX-RECORD the record {STAGE_SPEC_T} names other bytes for the ledger than its first "
                     f"{N5_T} lines")
    if not CTX["raw"].startswith(CTX["five"]) or len(jl(CTX["five"])) != N5_T:
        found.append(f"PREFIX-RECORD the working file does not start with {N5_T} whole lines")
    return verdict(found, f"record[:{X_LEDGER_BYTES_T}] == the x_rec byte copy of X's ledger ({N_X_LINES_T} "
                          f"lines), byte for byte; sha256 of that prefix {X_LEDGER_SHA_T} == its "
                          f"X_REC_MANIFEST row == the typed sha; every `tierc12(` commit's blob of the ledger is "
                          f"a byte-prefix of the next and of the working file (read-only git; their number "
                          f"grows with the build and is not printed); the {N5_T}-line file this record files is "
                          f"the working file's first {N5_T} lines; the forged-through rewrite of line 2 passes "
                          f"every chain check — only the byte law sees it")


# ═══════════════════════════════════════════════════════ F-LEDGER [CHAIN]
def guard_fx(body: dict) -> list:
    """PRODUCTION's guarded append on a scratch copy of the five-line file: it must HALT and write nothing."""
    p = put("guard.jsonl", CTX["five"])
    found = halted(lambda: SPEC.append(p, [body]))
    return found if p.read_bytes() == CTX["five"] else found + ["GUARD-WROTE the guard HALTed after a write"]


def note(text: str) -> dict:
    return {"kind": "refresh", "tier": "TIER-C12", "pin_ms": CONTROL_PIN_MS_T, "note": text}


def chain_break():
    F, C = CTX["five_lines"], control()
    i, j = row_at("v6", "BTCUSDT"), row_at("v6", "ETHUSDT")
    swapped = list(C)
    swapped[i], swapped[j] = C[j], C[i]
    compact = dump(F[:2]) + (json.dumps(F[2], sort_keys=True, separators=(",", ":"), ensure_ascii=False)
                             + "\n").encode("utf-8") + dump(F[3:])
    nan_row = dict(C[i], symbol="NEARUSDT", net_r=float("nan"))
    wrong_law = copy.deepcopy(F)
    wrong_law[4]["entry_sha256"] = sha(json.dumps(body_fx(F[4]), sort_keys=True).encode("utf-8"))
    rows = [
        ("a rewritten earlier line: one digit of line 2's opening_ms changed",
         "entry_sha256 does not match the line's own content", lambda: chain_fx(dump(rewritten()))),
        ("a re-ordered line: lines 2 and 3 swapped", "a line was inserted, removed or reordered",
         lambda: chain_fx(dump([F[0], F[2], F[1], F[3], F[4]]))),
        ("two row lines of the control swapped and left unchained", "a line was inserted, removed or reordered",
         lambda: chain_fx(dump(swapped))),
        ("line 3 re-serialised with compact separators (the same entry, other bytes)", "CHAIN-BYTES",
         lambda: chain_fx(compact)),
        ("a row holding NaN written by bare forward_log (chained)", "CHAIN-NAN",
         lambda: chain_fx(dump(extend(F, [body_fx(nan_row), note("after a NaN row")])))),
        ("a string holding U+2028 written raw (chained)", "CHAIN-LINE-BREAK",
         lambda: chain_fx(dump(extend(F, [note("a b")])))),
        ("line 5 sealed by another hash law (the sha of its default-separator dump)", "CHAIN-OWN",
         lambda: chain_fx(dump(wrong_law))),
        ("a NaN handed to production's guarded append", "FWD-NAN", lambda: guard_fx(body_fx(nan_row))),
        ("a sixth line that is not JSON standing after the five lines of the working file (the real leg's own "
         "read: the five lines, then the whole file)", "CHAIN-FL",
         lambda: working_fx(chain_fx, CTX["five"] + b"not json at all\n")),
        ("a sixth line on the zeros under a made-up entry sha standing after the five lines (the same read)",
         "a line was inserted, removed or reordered",
         lambda: working_fx(chain_fx, CTX["five"] + dump([dict(note("unchained"), prev_sha256=ZEROS_T,
                                                               entry_sha256=ZEROS_T.replace("0", "f"))]))),
    ]
    rows += [(f"U+{ord(c):04X} in a string handed to production's guarded append", "FWD-LINE-BREAK",
              (lambda c=c: guard_fx(note(f"a{c}b")))) for c in ("\u0085", " ", " ")]
    return FX.plants(rows)


def body_fx(line: dict) -> dict:
    return {k: v for k, v in line.items() if k not in ("prev_sha256", "entry_sha256")}


def chain_real():
    control()
    found = working_fx(chain_fx, CTX["raw"]) + [f"(control) {x}" for x in chain_fx(CTX["control_raw"])]
    lines = CTX["five_lines"]
    if lines[-1]["entry_sha256"] != FLREF.last_sha(put("ledger.jsonl", CTX["five"])) \
            or lines[N_X_LINES_T - 1]["entry_sha256"] != X_HEAD_T or lines[N_X_LINES_T]["prev_sha256"] != X_HEAD_T:
        found.append("CHAIN-HEAD line 5 does not chain on X's typed head, or the head is not forward_log.last_sha's")
    return verdict(found, f"forward_log.verify_chain (the law's own module, imported here) is ok over the "
                          f"{N5_T} lines, head {lines[-1]['entry_sha256']}; this suite's own hash loop "
                          f"(hashlib, sorted compact JSON + prev, from the zeros) reproduces every "
                          f"prev_sha256 and entry_sha256; every line's bytes are the default-separator dump of "
                          f"its parsed entry and a newline; no bare NaN / Infinity token; {N5_T} lines == "
                          f"{N5_T} newline bytes == {N5_T} str.splitlines pieces; line {N5_T} chains on X's "
                          f"head {X_HEAD_T}; the spec module's ported verify_chain returns forward_log's own "
                          f"result on every file read here; the control block appended through production's "
                          f"guarded append passes the same checks; the WHOLE working file — whatever stands "
                          f"after line {N5_T}, which grows with the build and is not printed — passes them too "
                          f"(forward_log.verify_chain, this suite's own hash loop, the byte, NaN and line-break "
                          f"laws)")


# ═══════════════════════════════════════════════════════ F-LEDGER [STRUCTURE]
def structure_break():
    F, C = CTX["five_lines"], control()
    a, b = row_at("v6", "BTCUSDT"), row_at("v6", "ETHUSDT")
    swapped = list(C)
    swapped[a], swapped[b] = C[b], C[a]
    last_row = max(i for i, e in enumerate(C) if e["kind"] == "row")
    reused = rechain(bent(F, 4, spec_sha256=X_SPEC_SHA_T), 4)
    again = dict(body_fx(F[4]))
    new_row = dict(body_fx(C[a]), symbol="ZECUSDT")
    planted = copy.deepcopy(C)
    planted[a]["window_end_i"] = 1
    orphan = [e for i, e in enumerate(C) if i != a]
    moved = bent(C, row_at(BOOK4_T, "BTCUSDT"), net_r=ROW_T["net_r"] + 1e-9)
    later = dict(note("a second refresh"), pin_ms=CONTROL_PIN_MS_T + H4_MS_T)
    return FX.plants([
        ("S2: a line of an unknown kind appended (chained)", "FWD-CHAIN S2",
         lambda: structure_fx(dump(extend(C, [{"kind": "note", "text": "x"}])))),
        ("S3: the rewrite of line 2 forged through (the chain verifies)", "FWD-CHAIN S3",
         lambda: structure_fx(dump(rechain(rewritten(), 1)))),
        ("S4: a fourth book_open that REUSES the old spec sha — line 5 rebuilt with X's, re-chained",
         "FWD-CHAIN S4 FWD-SPEC-REUSED", lambda: structure_fx(dump(reused))),
        ("S4: a second book_open for the fourth book appended later (after the control's refresh)",
         "FWD-CHAIN S4", lambda: structure_fx(dump(extend(C, [again])))),
        ("S4: line 5 appended again as line 6 of the working file, chained — a second book_open for the fourth "
         "book (the real leg's own read: the five lines, then the whole file)", "FWD-CHAIN S4",
         lambda: working_fx(structure_fx, dump(extend(F, [again])))),
        ("S4: line 5 opened with n_min one below X's lines, re-chained", "FWD-CHAIN S4",
         lambda: structure_fx(dump(rechain(bent(F, 4, n_min=N_MIN_T - 1), 4)))),
        ("S5: a row carrying a pin-dependent field (window_end_i), re-chained", "FWD-CHAIN S5 FWD-ROW-FIELDS",
         lambda: structure_fx(dump(rechain(planted, a)))),
        ("S5: the last row line appended again under a later refresh (chained)", "FWD-DUP-KEY",
         lambda: structure_fx(dump(extend(C, [body_fx(C[last_row]), later])))),
        ("S6: two row lines swapped and RE-CHAINED", "FWD-CHAIN S6 FWD-ROW-ORDER",
         lambda: structure_fx(dump(rechain(swapped, min(a, b))))),
        ("S6: a second refresh line at the same pin (chained)", "FWD-REFRESH-TWICE",
         lambda: structure_fx(dump(extend(C, [note("the same pin again")])))),
        ("S6: a file ending on a row line (chained)", "FWD-TORN-REFRESH",
         lambda: structure_fx(dump(extend(C, [new_row])))),
        ("S7: a gated row whose base row is absent, re-chained", "FWD-CHAIN S7 FWD-SUBSET",
         lambda: structure_fx(dump(rechain(orphan, a)))),
        ("S7: a gated row's net_r moved off its base row, re-chained", "FWD-CHAIN S7 FWD-SUBSET",
         lambda: structure_fx(dump(rechain(moved, row_at(BOOK4_T, "BTCUSDT"))))),
    ])


def structure_real():
    F, C = CTX["five_lines"], control()
    found = working_fx(structure_fx, CTX["raw"])
    typed = {
        "the kinds": ([x["kind"] for x in F], [KINDS_T[0]] * len(X_BOOKS_T) + [KINDS_T[1], KINDS_T[0]]),
        "the books opened": ([x.get("book") for x in F if x["kind"] == KINDS_T[0]], list(X_BOOKS_T) + [BOOK4_T]),
        "line 5's key set": (tuple(sorted(body_fx(F[4]))), OPEN_KEYS_T),
        "X's book_open key set": (tuple(sorted(body_fx(F[0]))), OPEN_KEYS_T),
        "line 5's typed fields": ({k: F[4].get(k) for k in LINE5_T}, LINE5_T),
        "line 5's opening": ((F[4].get("opening_ms"), F[4].get("opening_iso")), (OPENING_MS_T, OPENING_ISO_T)),
        "line 5's n_min": (F[4].get("n_min"), N_MIN_T),
        "line 5's spec sha": (F[4].get("spec_sha256"), sha(CTX["spec_bytes"])),
        "line 5's prev": (F[4].get("prev_sha256"), X_HEAD_T),
        "X's lines name X's spec": ({x.get("spec_sha256") for x in F[:N_X_LINES_T]}, {X_SPEC_SHA_T}),
    }
    found += [f"STRUCTURE-TYPED {k}: the file reads {a!r}, typed {b!r}" for k, (a, b) in typed.items() if a != b]
    found += [f"STRUCTURE-CONTROL {x}" for x in structure_fx(CTX["control_raw"]) + prefix_fx(
        CTX["control_raw"], CTX["x_ledger"], manifest_row(X_LEDGER_T)) + chain_fx(CTX["control_raw"])
        + rehash_fx(CTX["control_raw"], CTX["spec_bytes"], CTX["x_spec_bytes"])]
    kept = {b: tuple(e["symbol"] for e in C if e["kind"] == "row" and e["book"] == b) for b in CONTROL_KEPT_T}
    if kept != CONTROL_KEPT_T:
        found.append(f"STRUCTURE-CONTROL production's predicates keep {kept}, typed {CONTROL_KEPT_T}")
    n_rows = sum(1 for e in C if e["kind"] == "row")
    return verdict(found, f"S1-S7 hold on the {N5_T}-line file (production's chain_findings, judged against the "
                          f"bytes of the fourth spec, of X's spec and of X's ledger): {len(X_BOOKS_T)} book_open "
                          f"lines in X's book_order naming X's spec sha, X's refresh, then exactly ONE book_open "
                          f"— line {N5_T}, {BOOK4_T}, tier TIER-C12, role `of record`, scored False, opening "
                          f"{OPENING_ISO_T} and n_min {N_MIN_T} as on X's lines, X's book_open key set exactly, "
                          f"spec_sha256 {sha(CTX['spec_bytes'])} != X's; 0 row lines. The WHOLE working file — "
                          f"whatever stands after line {N5_T}, which grows with the build and is not printed — "
                          f"holds S1-S7 under the same chain_findings. CONTROL (must stay GREEN): "
                          f"the {N5_T} lines + one lawful block of {n_rows} typed rows (v6 {len(CONTROL_BASE_T)}, "
                          f"trg912 {len(CONTROL_912_T)}, gated-v6-oldtide {len(CONTROL_KEPT_T['gated-v6-oldtide'])}, "
                          f"{BOOK4_T} {len(CONTROL_KEPT_T[BOOK4_T])} — each gated book = its base minus what "
                          f"production's predicate refuses) + one refresh line passes the prefix, chain, structure "
                          f"and re-hash checks: GREEN")


# ═══════════════════════════════════════════════════════ F-LEDGER [REHASH]
def bent_spec() -> bytes:
    """Planted mutation 6: one character of the fourth spec's gate text bent in a copy."""
    doc = json.loads(CTX["spec_bytes"].decode("utf-8"))
    text = doc["books"][BOOK4_T]["gate"]["text_of_record"]
    doc["books"][BOOK4_T]["gate"]["text_of_record"] = text.replace("POST-FILTER", "POST-FILTEr", 1)
    out = SPEC.render_json(doc)
    if out == CTX["spec_bytes"]:
        raise ValueError("the gate text holds no `POST-FILTER` to bend")
    return out


def rehash_break():
    F, s, x = CTX["five_lines"], CTX["spec_bytes"], CTX["x_spec_bytes"]
    return FX.plants([
        ("a fourth book_open that REUSES the old spec sha — line 5 rebuilt with X's, re-chained",
         "FWD-SPEC-REUSED", lambda: rehash_fx(dump(rechain(bent(F, 4, spec_sha256=X_SPEC_SHA_T), 4)), s, x)),
        ("one character of the fourth spec's gate text bent in a copy: the sha moves off line 5's",
         "REHASH-LINE5", lambda: rehash_fx(CTX["five"], bent_spec(), x)),
        ("the same bent copy standing as the file while the spec is rebuilt from its sources",
         "FWD-SPEC-FROZEN", lambda: frozen_fx(bent_spec())),
        ("X's refresh line naming another spec sha, re-chained", "REHASH-X-SHA",
         lambda: rehash_fx(dump(rechain(bent(F, 3, spec_sha256=ZEROS_T), 3)), s, x)),
        ("one byte of the x_rec copy of X's spec changed in a scratch copy", "REHASH-X-COPY",
         lambda: rehash_fx(CTX["five"], s, x.replace(b"TIER-C11-X", b"TIER-C11-Y", 1))),
    ])


def rehash_real():
    found = rehash_fx(CTX["five"], CTX["spec_bytes"], CTX["x_spec_bytes"]) + frozen_fx(CTX["spec_bytes"])
    return verdict(found, f"ledger line {N5_T} names {sha(CTX['spec_bytes'])} == sha256 of "
                          f"BOOK_SPEC_COMBINED.json as it stands ({len(CTX['spec_bytes'])} B); that document "
                          f"rebuilt now from its sources by production is byte-equal to the file (freeze_spec "
                          f"does not HALT); lines 1-{N_X_LINES_T} name X's spec sha {X_SPEC_SHA_T} and no other; "
                          f"the x_rec copy of X's spec hashes to its manifest row and to the typed sha; the fourth "
                          f"book's sha differs from X's")


# ═══════════════════════════════════════════════════════ F-LEDGER [ANCESTORS]
def resealed_t11(n_score: int) -> bytes:
    """TC11's ledger with GENESIS n_score moved and BOTH lines re-sealed under TC11's own law."""
    lines = [json.loads(x) for x in rd(T11_LEDGER_T).decode("utf-8").split("\n") if x]
    canon = lambda o: json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    lines[0]["n_score"] = n_score
    prev = ZEROS_T
    for e in lines:
        e["prev"] = prev
        e["line_sha256"] = sha(canon({k: v for k, v in e.items() if k != "line_sha256"}).encode("utf-8"))
        prev = e["line_sha256"]
    return "".join(canon(e) + "\n" for e in lines).encode("utf-8")


def ancestors_break():
    files = ancestor_files()
    flipped = files[T11_LEDGER_T].replace(b"\"n_rode\":200", b"\"n_rode\":201", 1)
    if flipped == files[T11_LEDGER_T]:
        raise ValueError("the byte to flip is not in TC11's ledger")
    return FX.plants([
        ("one byte flipped in a scratch copy of TC11's ledger", "ANCESTOR-TC11-CHAIN",
         lambda: ancestor_fx(dict(files, **{T11_LEDGER_T: flipped}))),
        ("the same copy handed to production's own check of the ancestors", "FWD-ANCESTOR",
         lambda: halted(lambda: SPEC.ancestor_facts(dict(CTX["S"], t11_ledger=flipped)))),
        ("a copy of TC11's ledger RE-SEALED under TC11's own law after its n_score moved by one (the chain "
         "verifies)", "ANCESTOR-FACT n_score",
         lambda: ancestor_fx(dict(files, **{T11_LEDGER_T: resealed_t11(N_MIN_T - 1)}))),
        ("one digit changed in a scratch copy of X's ledger", "ANCESTOR-PIN",
         lambda: ancestor_fx(dict(files, **{X_LEDGER_T: files[X_LEDGER_T].replace(b"\"n_min\": 30", b"\"n_min\": 31", 1)}))),
        ("one byte changed in a scratch copy of TC11's FORWARD_LEDGER.md", "ANCESTOR-PIN",
         lambda: ancestor_fx(dict(files, **{T11_PAGE_T: files[T11_PAGE_T] + b" "}))),
    ])


def ancestors_real():
    before = ancestor_files()
    found = ancestor_fx(before)
    out = Path(tempfile.mkdtemp(prefix="build_", dir=CTX["tmp"]))
    r = subprocess.run([sys.executable, "-B", str(ROOT / TOOL_T), f"--out-dir={out}"], capture_output=True, text=True,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    after = ancestor_files()
    if r.returncode:
        found.append(f"ANCESTOR-RUN the production run exited {r.returncode}: {(r.stderr or r.stdout).strip()[-300:]}")
    else:
        if sorted(p.name for p in out.iterdir()) != sorted([Path(SPEC_T).name, Path(LEDGER_T).name]):
            found.append(f"ANCESTOR-RUN the production run left {sorted(p.name for p in out.iterdir())}")
        elif (out / Path(SPEC_T).name).read_bytes() != CTX["spec_bytes"] \
                or (out / Path(LEDGER_T).name).read_bytes() != CTX["five"]:
            found.append("ANCESTOR-RUN a fresh production run does not reproduce the spec and the five-line "
                         "ledger byte for byte")
    found += [f"ANCESTOR-MOVED {rel} hashes differently after the production run" for rel in sorted(before)
              if sha(before[rel]) != sha(after[rel])]
    return verdict(found, f"X's ledger ({X_LEDGER_SHA_T}), X's spec ({X_SPEC_SHA_T}), TC11's ledger "
                          f"({T11_LEDGER_SHA_T}) and TC11's FORWARD_LEDGER.md hash to their pins (the X_REC_MANIFEST "
                          f"rows; the sha TC11's PROGRESS.json certifies, itself at its R0 or stamped sha; "
                          f"TC12-R0's frozen-estate key; the typed shas) BEFORE and AFTER a production run in a "
                          f"fresh process, which reproduces BOOK_SPEC_COMBINED.json and the {N5_T}-line ledger "
                          f"byte for byte into a scratch directory; TC11's two lines (GENESIS {T11_GENESIS_T}, "
                          f"REFRESH {T11_HEAD_T}) verify under this suite's own mirror of TC11's law; every fact "
                          f"both ancestors state is equal — the opening, n_score == n_min == {N_MIN_T}, the panel, "
                          f"each ridden book's roles name and six periods, its book sha and open keys at the "
                          f"score edge, the refresh pin and the corridor's lower bound")


# ═══════════════════════════════════════════════════════ F-FWD-SPEC
def arms_edit(fn):
    return lambda spec: spec.__setitem__("arms", fn(list(spec["arms"])))


def spec_copy(edit) -> dict:
    doc = json.loads(CTX["spec_bytes"].decode("utf-8"))
    edit(doc)
    return doc


def fwd_spec_break():
    S = CTX["S"]

    def one_char(arms):
        i = scored_index(arms)
        arms[i] = arms[i].replace("POST-FILTER", "POST-FILTEr", 1)
        return arms

    def second(arms):
        return arms + ["`scored` a second element beginning with the scored token"]

    def no_token(arms):
        i = scored_index(arms)
        arms[i] = arms[i].replace("`scored`", "`scored_arm`", 1)
        return arms

    def win_17(spec):
        spec["scored_arm"] = spec["scored_arm"].replace(f">= {CUT_T}", f">= {CUT_T + 1}", 1)

    def no_old(spec):
        spec["scored_arm"] = spec["scored_arm"].replace(f"{OLD_T} OLD", "OLD", 1)

    src = tool_src()
    return FX.plants([
        ("the `scored` element changed by one character in a registry copy (resealed)", "FWD-SPEC-FROZEN",
         lambda: frozen_fx(CTX["spec_bytes"], resealed(S, "registry", "P-ADM-1", arms_edit(one_char)))),
        ("a second element beginning `scored` added to a registry copy (resealed)", "FWD-GATE-TEXT",
         lambda: halted(lambda: SPEC.spec_doc(resealed(S, "registry", "P-ADM-1", arms_edit(second))))),
        ("the element's leading token bent so that none matches (resealed)", "FWD-GATE-TEXT",
         lambda: halted(lambda: SPEC.spec_doc(resealed(S, "registry", "P-ADM-1", arms_edit(no_token))))),
        ("P-WIN-1's text with the integer changed in a copy of TC11's registry (resealed)", "FWD-CUT-TEXT",
         lambda: halted(lambda: SPEC.spec_doc(resealed(S, "t11_registry", "P-WIN-1", win_17)))),
        ("P-AGE-1's text with `B4 OLD` removed in a copy of TC11's registry (resealed)", "FWD-OLD-TEXT",
         lambda: halted(lambda: SPEC.spec_doc(resealed(S, "t11_registry", "P-AGE-1", no_old)))),
        ("the fourth book's clause deleted from n_law in a spec copy", "FWD-SPEC-FROZEN",
         lambda: frozen_fx(SPEC.render_json(spec_copy(lambda d: d["n_law"]["row_set_of_record"].pop(BOOK4_T))))),
        ("a lineage file's sha altered in a spec copy", "SPEC-PATH",
         lambda: spec_value_fx(spec_copy(lambda d: d["path_modules"].__setitem__("scripts/tierc9.py", ZEROS_T)))),
        ("a lineage file's sha moved in a copy of the sources", "FWD-SPEC-PATH",
         lambda: halted(lambda: SPEC.spec_doc(dict(S, lineage=dict(S["lineage"], **{"scripts/tierc9.py": ZEROS_T}))))),
        ("n_min bent by one in a spec copy", "SPEC-VALUE n_min",
         lambda: spec_value_fx(spec_copy(lambda d: d.__setitem__("n_min", N_MIN_T - 1)))),
        ("`import numpy` planted in a copy of the spec tool", "SPEC-ENV-FREE",
         lambda: spec_ast_fx(src + "\nimport numpy\n")),
        ("the reader `tierc12_va_stamps` imported in a copy of the spec tool", "SPEC-ENV-FREE",
         lambda: spec_ast_fx(src + "\nimport tierc12_va_stamps\n")),
        ("a value-area stamp table added to a copy's SPEC_READS_T", "SPEC-VA-BLIND",
         lambda: spec_ast_fx(mut(src, '    "research_outputs/tierc12/close/TC11_STAMP_MAP.json",\n',
                                 '    "research_outputs/tierc12/close/TC11_STAMP_MAP.json",\n'
                                 '    "research_outputs/tierc12/va/stamps/VA_STAMPS_v6.parquet",\n'))),
        ("a second open site planted in a copy (a new function calling read_bytes)", "SPEC-READS",
         lambda: spec_ast_fx(src + "\n\ndef peek(p):\n    return Path(p).read_bytes()\n")),
        ("the tool's reader asked for a path outside SPEC_READS_T (TC10's STEP0 record)", "SPEC-READS",
         lambda: halted(lambda: SPEC.Reader()._read("research_outputs/tierc10/STEP0_RECORD.json"))),
    ])


def fwd_spec_real():
    doc = json.loads(CTX["spec_bytes"].decode("utf-8"))
    found = frozen_fx(CTX["spec_bytes"]) + spec_value_fx(doc) + step_q_git_fx() + spec_ast_fx(tool_src())
    gate = doc["books"][BOOK4_T]["gate"]
    return verdict(found, f"BOOK_SPEC_COMBINED.json ({len(CTX['spec_bytes'])} B, sha {sha(CTX['spec_bytes'])}) "
                          f"rebuilt from its sources is the file; each value is its source's by this suite's own "
                          f"read — the v6 card, roles, ride_spec and panel of X's spec by object; the gate text = "
                          f"the ONE element of registrations[P-ADM-1].operative_spec.arms matching ^`scored`\\s "
                          f"({len(gate['text_of_record'])} characters, text_sha256 {gate['text_sha256']}), beside "
                          f"P-ADM-1's payload sha; its components = TC11's P-AGE-1 and P-WIN-1 scored_arm with "
                          f"their payload shas, TC11's registry pinned by its chain head {T11_REG_HEAD_T} "
                          f"(recomputed from the payloads) and by no file sha; the opening {OPENING_ISO_T}, "
                          f"n_min {N_MIN_T}, pool_lo_ms {POOL_LO_MS_T}, the score edge {SCORE_EDGE_MS_T}, the cut "
                          f"{CUT_T} and the OLD code {OLD_T} == the typed values; X's {N_ROW_FIELDS_T} row names "
                          f"and the {len(ADDED_T)} added names; n_law's row set of record == the typed rule; the "
                          f"STEP Q instant {STEP_Q_T['instant_iso']} == git's committer time of "
                          f"{STEP_Q_T['commit']}; the {N_LINEAGE_T} lineage shas == X's values == the files now. "
                          f"AST: the tool imports nothing but the stdlib and members of {list(IMPORTS_T)} (of the "
                          f"three it imports the pin door and tierc12_progress; forward_log's law stands in it as "
                          f"ports, F-PORT); its SPEC_READS_T == the typed {len(SPEC_READS_T)} paths; every open site is "
                          f"one of {list(OPEN_SITES_T)}; it holds no path token of {list(BLIND_TOKENS_T)} "
                          f"(value-area-blind, seam 62). NOT HERE: the clause `a ride's TP.ride_spec differs from "
                          f"its book's` (FWD-SPEC-RIDE) needs the env and is TC12-L's")


# ═══════════════════════════════════════════════════════ F-PORT
def port_break():
    own = tool_src()
    fl = rd(FL_T).decode("utf-8")
    token = mut(own, "    body = {k: v for k, v in entry.items() if k != \"entry_sha256\"}\n"
                     "    return json.dumps(body, sort_keys=True, separators=(\",\", \":\"),\n",
                "    body = {k: v for k, v in entry.items() if k != \"entry_sha256\"}\n"
                "    return json.dumps(body, sort_keys=False, separators=(\",\", \":\"),\n")
    head = "# PORT VERBATIM <- scripts/forward_log.py:209-232 sha256 "
    flipped = mut(mut(own, head, head.replace("VERBATIM", "TEXT-ONLY")),
                  "        if recomputed != e.get(\"entry_sha256\"):\n", "        if recomputed == e.get(\"entry_sha256\"):\n")
    other_sha = mut(own, "# PORT VERBATIM <- scripts/forward_log.py:79-82 sha256 " + fl_pin(),
                    "# PORT VERBATIM <- scripts/forward_log.py:79-82 sha256 " + ZEROS_T)
    relabel = mut(own, "# PORT VERBATIM <- research_outputs/tierc12/x_rec/scripts/tc11x_forward.py:590-594",
                  "# PORT CHANGED <- research_outputs/tierc12/x_rec/scripts/tc11x_forward.py:590-594")
    smuggled = mut(own, "    return lines[len(lines) - 1][\"entry_sha256\"] if lines else GENESIS\n",
                   "    return lines[len(lines) - 1][\"entry_sha256\"] if len(lines) > 1 else GENESIS\n")
    return FX.plants([
        ("one token changed in a copy of a VERBATIM port (canonical: sort_keys False)", "PORT-VERBATIM canonical",
         lambda: port_fx(token)),
        ("the same copy handed to production's own check of its ports", "FWD-FL-PORT canonical",
         lambda: SPEC.fl_port_findings(fl, token)),
        ("a comparator flipped in a copy of a port relabelled TEXT-ONLY (verify_chain)", "PORT-TEXT-ONLY verify_chain",
         lambda: port_fx(flipped)),
        ("a provenance comment naming another sha (chain_hash)", "PORT-SHA chain_hash", lambda: port_fx(other_sha)),
        ("a port relabelled CHANGED while AST-identical to its source (chained)", "PORT-CHANGED chained",
         lambda: port_fx(relabel)),
        ("a second difference smuggled into the CHANGED port last_sha", "PORT-CHANGED-DECLARED last_sha",
         lambda: port_fx(smuggled)),
        ("the same copy handed to production's own check of its ports", "FWD-FL-PORT last_sha",
         lambda: SPEC.fl_port_findings(fl, smuggled)),
    ])


def fl_pin() -> str:
    """The sha X's spec names for scripts/forward_log.py (read here from the x_rec copy)."""
    return json.loads(rd(X_SPEC_T).decode("utf-8"))["path_modules"][FL_T]


def port_real():
    own = tool_src()
    found = port_fx(own) + SPEC.fl_port_findings(rd(FL_T).decode("utf-8"), own)
    if tuple(SPEC.FL_PORTS_T) != FL_PORTS_T or dict(SPEC.FL_CHANGED_T) != {"last_sha": LAST_SHA_T}:
        found.append("PORT-MISSING production's list of forward_log ports or its one declared difference is not "
                     "the typed one")
    labels = sorted(PORTS_T.items())
    return verdict(found, f"{len(PORTS_T)} ports, each under a provenance comment naming its source, its lines "
                          f"and the source's full sha: "
                          + " · ".join(f"{n} {lab}" for n, lab in labels)
                          + f". forward_log.py at {fl_pin()} (the sha X's spec names for it == the file now) "
                            f"and tc11x_forward.py at its X_REC_MANIFEST row: every VERBATIM port is AST-identical "
                            f"to its source function at the lines named; last_sha differs from forward_log's by "
                            f"the one declared index token `{LAST_SHA_T[0]}` -> `{LAST_SHA_T[1]}` and nothing else; "
                            f"append and chain_findings are CHANGED (not AST-identical; the difference is named "
                            f"above each); production's own FWD-FL-PORT check agrees; CHAIN_FIELDS == X's literal "
                            f"by AST")


# ═══════════════════════════════════════════════════════ F-TYPED-FLOW
def flow_break(pin: str):
    def leg():
        return FX.plants([
            (f"a typed copy of EQUAL value in place of the read of {pin} in a shadow copy of the spec module",
             f"PIN-NOT-READ {pin}", lambda: flow_fx(shadow(pin), pin)),
        ])
    return leg


def flow_real(pin: str):
    def leg():
        found = flow_fx(SPEC, pin)
        if pin == "adm.lag_cut" and (PINS.pin(pin), SPEC.p_win_1_refuses({"lag": CUT_T - 1}),
                                     SPEC.p_win_1_refuses({"lag": CUT_T})) != (CUT_T, False, True):
            found.append(f"PIN-FLOW-WRONG {pin}: unbent, the pin is not the typed {CUT_T} or the predicate does not "
                         f"keep lag {CUT_T - 1} and refuse lag {CUT_T}")
        if not found:
            FX.say(flow_line(pin))
        if pin == "adm.lag_cut":
            why = (f"the contract pin {pin} ({PINS.pin(pin)}, == the typed {CUT_T}) bent down by one at its door "
                   f"(tierc12_pins.bend): `p_win_1_refuses` on the planted lag = CUT − 1 = {CUT_T - 1} row flips "
                   f"False -> True; unbent, lag {CUT_T - 1} is kept and lag {CUT_T} is refused (the comparator is "
                   f">=); the bend does not outlive its block")
        else:
            why = (f"the contract pin {pin} ({PINS.pin(pin)}) bent at its door ("
                   + ("one 4h bar later" if pin == "ledger.opening" else "down by one")
                   + f"): production's `spec_doc` HALTs {FLOW_HALT_T[pin]} — the pin is read through the door and "
                     f"held equal to the filed values (the register's `equal_to` row at {STAGE_SPEC_T}); the "
                     f"register's own witness for this pin is TC12-L's scratch ledger, so the [FLOW] line above "
                     f"names the assertion that moved here; the bend does not outlive its block")
        return verdict(found, why)
    return judged(leg)


FLOW_IF_T = {
    "ledger.opening": ("the pin bent by one 4h bar at its door does not HALT the spec tool at FWD-OPENING (the "
                       "admitted set of a scratch ledger is TC12-L's witness)",
                       "a typed copy of the opening in a copy of the spec module is not caught as PIN-NOT-READ"),
    "ledger.n_min": ("the pin bent down by one at its door does not HALT the spec tool at FWD-NMIN (the status "
                     "string of a scratch ledger is TC12-L's witness)",
                     "a typed copy of the count in a copy of the spec module is not caught as PIN-NOT-READ"),
    "adm.lag_cut": ("the pin bent down by one at its door does not flip `p_win_1_refuses` on the planted "
                    "lag = CUT − 1 row",
                    "the cut copied into a module constant of a copy of the spec module is not caught as PIN-NOT-READ"),
}


def spec_fixtures() -> list:
    rows = [
        ("F-LEDGER [PREFIX]", "append-only on the three existing books: the byte-prefix law [L-L.4, L-L.7]",
         "a rewritten earlier line, the same rewrite forged through the chain, a re-ordered line, a manifest row "
         "naming another sha, or a committed blob that is not a byte-prefix of the next is not caught",
         "record[:N_X] != the x_rec bytes of X's ledger; sha256 of that prefix is not its manifest row's; or the "
         "ledger blob of any `tierc12(` commit is not a byte-prefix of the next commit's blob and of the working "
         "file (a fixture-side read-only git call)",
         prefix_break, judged(prefix_real)),
        ("F-LEDGER [CHAIN]", "the chain is forward_log's law, byte for byte [L-L.5, L-L.7]",
         "a rewritten line, a re-ordered line, a re-serialised line, a bare NaN, a raw line-break character or a "
         "line sealed by another hash law passes; production's guarded append writes a NaN or a U+0085 / "
         "U+2028 / U+2029 line instead of HALTing FWD-NAN / FWD-LINE-BREAK; or a line standing after line 5 of "
         "the working file (not JSON, or unchained) is not seen by the real leg's own read",
         "on the five lines or anywhere in the WHOLE working file: forward_log.verify_chain is not ok; this "
         "suite's OWN hash loop (no forward_log call) disagrees with any "
         "entry_sha256; any line's bytes differ from the default-separator dump of its parsed entry plus a newline; "
         "a line holds a bare NaN or Infinity token or a str.splitlines boundary other than its final newline; or "
         "the spec module's ported verify_chain does not return forward_log's own result",
         chain_break, judged(chain_real)),
        ("F-LEDGER [STRUCTURE]", "line kinds and the structure law S2-S7 [L-L.6, L-L.7]",
         "a breach of S2, S3, S4, S5, S6 or S7 planted in a re-chained copy is not reported by production's "
         "chain_findings under its own law, or a second book_open appended after line 5 of the working file is "
         "not seen by the real leg's own read",
         "any of S2-S7 of L-L.6 is breached on the five-line file or anywhere in the WHOLE working file, or line "
         "5 is not this suite's typed line; the control (the file + one lawful row block and refresh line) must "
         "stay GREEN",
         structure_break, judged(structure_real)),
        ("F-LEDGER [REHASH]", "the fourth re-hashes: its own document, its own sha [L-L.3, L-L.7]",
         "a fourth book_open reusing X's spec sha, a spec whose text moved off line 5's sha, a spec that no longer "
         "rebuilds from its sources, an X line naming another sha, or a moved copy of X's spec is not caught",
         "line 5's spec_sha256 is not the sha of BOOK_SPEC_COMBINED.json as it stands; that document rebuilt now "
         "from its sources is not byte-equal to the file; lines 1-4 name any sha but X's; or the x_rec copy of X's "
         "spec no longer hashes to its manifest row",
         rehash_break, judged(rehash_real)),
        ("F-LEDGER [ANCESTORS]", "the two ancestors: X's ledger continued, TC11's cited [L-L.4, L-L.7]",
         "a flipped byte in a copy of an ancestor, or a re-sealed copy of TC11's ledger stating another fact, is "
         "not caught by the pin, by the mirror of TC11's law or by the fact law",
         "X's ledger, X's spec, TC11's ledger or TC11's FORWARD_LEDGER.md hash differently before and after a "
         "production run or differently from their pins; TC11's chain does not verify under this suite's own "
         "mirror of TC11's law; a fact both ancestors state differs; or a fresh production run does not reproduce "
         "the spec and the five-line ledger byte for byte",
         ancestors_break, judged(ancestors_real)),
        ("F-FWD-SPEC", "the fourth spec is its sources'; the tool is env-free, reads only its typed list and is "
                       "value-area-blind [L-L.2, L-L.3, L-L.18; L-0.22 seam 62]",
         "a registry copy whose `scored` element moved, doubled or lost its token, a TC11 text whose cut or OLD "
         "band moved, a spec copy missing the fourth book's n_law clause or carrying another lineage sha, or a "
         "tool copy importing numpy / the reader, reading a value-area table or opening a second site, is not "
         "caught by its named detector",
         "the fourth spec rebuilt from its sources is not the file; a spec value is not its source's; zero or "
         "several elements of P-ADM-1's operative_spec.arms match ^`scored`\\s; one of the 18 lineage shas differs "
         "from X's; or (AST) the spec tool opens a path outside SPEC_READS_T or imports anything but the stdlib, "
         "forward_log, tierc12_progress and tierc12_pins",
         fwd_spec_break, judged(fwd_spec_real)),
        ("F-PORT", "every port's label is true of its source text at its pinned sha [L-L port law; L-D.11]",
         "one token changed in a copy of a VERBATIM port, a comparator flipped in a copy of a TEXT-ONLY port, a "
         "provenance comment naming another sha, a false CHANGED label or an undeclared change is not caught",
         "a port's label is untrue of forward_log.py (at the sha X's spec names) or of tc11x_forward.py (at its "
         "manifest sha): a VERBATIM port not AST-identical, a provenance comment naming other lines or another sha, "
         "a CHANGED port identical to its source, or last_sha differing by more than its one declared token",
         port_break, judged(port_real)),
    ]
    for pin in FLOW_PINS_T:
        real_if, break_if = FLOW_IF_T[pin]
        rows.append((FX.block_id("F-TYPED-FLOW", None, pin), f"the contract pin {pin} flows through its door [L-0.17]",
                     break_if, real_if, flow_break(pin), flow_real(pin)))
    return rows


def typed_lines() -> list:
    return [
        f"--stage={STAGE_SPEC_T} · the record: {SPEC_T} and the first {N5_T} lines of {LEDGER_T} (X's "
        f"{N_X_LINES_T} lines + one book_open); what TC12-L appends after them is its own transcript's to print — "
        f"F-LEDGER [CHAIN] and [STRUCTURE] judge the WHOLE working file here too and print nothing of the tail",
        f"X's ledger {X_LEDGER_BYTES_T} B sha {X_LEDGER_SHA_T} head {X_HEAD_T} · X's spec sha {X_SPEC_SHA_T} · "
        f"X_BOOKS_T {list(X_BOOKS_T)} · KINDS_T {list(KINDS_T)}",
        f"TC11's ledger sha {T11_LEDGER_SHA_T} · GENESIS {T11_GENESIS_T} · REFRESH {T11_HEAD_T} · TC11's registry "
        f"chain head {T11_REG_HEAD_T}",
        f"LINE5_T {LINE5_T} · OPEN_KEYS_T {list(OPEN_KEYS_T)}",
        f"OPENING_MS_T {OPENING_MS_T} ({OPENING_ISO_T}) · SCORE_EDGE_MS_T {SCORE_EDGE_MS_T} · POOL_LO_MS_T "
        f"{POOL_LO_MS_T} · N_MIN_T {N_MIN_T} · CUT_T {CUT_T} · OLD_T {OLD_T} · STEP_Q_T {STEP_Q_T}",
        f"N_ROW_FIELDS_T {N_ROW_FIELDS_T} + ADDED_T {list(ADDED_T)} · N_LINEAGE_T {N_LINEAGE_T} · N_LAW_T {N_LAW_T}",
        f"SPEC_READS_T {len(SPEC_READS_T)} typed paths (the lineage files are added by object from X's spec) · "
        f"IMPORTS_T {list(IMPORTS_T)} beside the stdlib · OPEN_SITES_T {list(OPEN_SITES_T)} · BLIND_TOKENS_T "
        f"{list(BLIND_TOKENS_T)}",
        "PORTS_T " + " · ".join(f"{n} {lab}" for n, lab in sorted(PORTS_T.items())),
        f"the control block: v6 {list(CONTROL_BASE_T)} · trg912 {list(CONTROL_912_T)} as (symbol, entry bar past "
        f"the opening, lag, band) · kept {CONTROL_KEPT_T} · refresh pin {CONTROL_PIN_MS_T} — typed rows, no outcome "
        f"of any book",
        f"FLOW_PINS_T {list(FLOW_PINS_T)} · n = 1 bend per pin (nothing is drawn at this record: no seeded leg)",
    ]


def load_record() -> None:
    """The record this stage verifies, the sources production reads, and this suite's own bytes."""
    spec_p, ledger_p = ROOT / SPEC_T, ROOT / LEDGER_T
    if not spec_p.is_file() or not ledger_p.is_file():
        halt(f"{SPEC_T} and {LEDGER_T} are not both on file — run {TOOL_T} first")
    raw = ledger_p.read_bytes()
    five = first_five(raw)
    CTX.update(spec_bytes=spec_p.read_bytes(), raw=raw, five=five, five_lines=jl(five),
               x_ledger=rd(X_LEDGER_T), x_spec_bytes=rd(X_SPEC_T), S=SPEC.sources())
    CTX["x_spec"] = json.loads(CTX["x_spec_bytes"].decode("utf-8"))


def main(argv) -> int:
    stage = FX.opt(argv, "--stage=")
    if stage not in STAGES:
        halt(f"--stage={stage!r}: this suite serves the records {sorted(STAGES)} (one transcript each; "
             f"`--stage` is never a leg filter)")
    root = Path(FX.opt(argv, "--root=", str(ROOT / FORWARD_T)))
    CTX.clear()
    CTX["tmp"] = tempfile.mkdtemp(prefix="tc12_forward_fx_")
    try:
        load_record()
        return FX.run_suite(
            args=argv, root=root, transcript=STAGES[stage],
            banner=f"TIER-C12 FORWARD FIXTURES at {stage} — the fourth book's spec and the five-line ledger "
                   f"(L-L.1..L-L.8, L-L.17, L-L.18): no bar is read, nothing is ridden — break leg first, RED or void",
            seed=PINS.pin("seed"), fixtures=spec_fixtures(), typed=typed_lines())
    finally:
        shutil.rmtree(CTX["tmp"], ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
