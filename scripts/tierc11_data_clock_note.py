#!/usr/bin/env python
"""TIER-C11 · STAGE TC11-D — FETCH_CLOCK_NOTE.json, built from the FILED records.

L-0.1 (research_outputs/tierc11/LEANS.md): "the latest close at fetch time is
printed beside it".  The --all run of 2026-09-25 printed it to stdout and filed
no clock row, so this note records the fetch-time latest closed 4h from what the
filed records show: the sealed FETCH_LOG.jsonl prefix, WRITE_ONCE_SEAL.json and
AS_OF_PIN.json, with the run's stdout capture (filed as a byte copy,
RUN_ALL_STDOUT_20260925.txt) quoted as corroboration.  It also records the one
re-describe of STAGE_D_MANIFEST.json/.md and fee_schedule.json (the repair after
the round-2 verification), diffed against their bytes at commit e97ad73.

This script replaces the session-scratch one-off that wrote the first note
(round-2 verification, finding 3).  No network, no snapshot read, no clock: it
reads research_outputs/tierc11/data/* and `git show e97ad73:<path>` only.
F-D11-CLOCK (scripts/tierc11_data_fixtures.py) re-derives every field of the
note independently and holds the filed bytes to build_note() [note-provenance].

Run:  ~/venvs/naiad/bin/python -B scripts/tierc11_data_clock_note.py [--check | --write]
      --check (default): exit 0 iff the filed note's bytes == build_note()'s
      --write: file the note (prints the old and new sha256)
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research_outputs" / "tierc11" / "data"
REL_OUT = "research_outputs/tierc11/data"
NOTE = "FETCH_CLOCK_NOTE.json"
STDOUT_COPY = "RUN_ALL_STDOUT_20260925.txt"
STDOUT_CAPTURED_AT = ("/private/tmp/claude-501/-Users-luis-Naiad/fa1cb7a0-1726-4409-8f61-bc58ab09398a/"
                      "scratchpad/run_all_1.log")
QUOTED_LINES = (18, 19, 20, 135, 155)
BUILD_REV = "e97ad73"                   # the commit that filed the TC11-D build (tierc11(TC11-D))
REDESCRIBED = ("STAGE_D_MANIFEST.json", "STAGE_D_MANIFEST.md", "fee_schedule.json")
MS_4H = 14_400_000
PIN_MS = 1_790_294_400_000
SEED = 20260924
RELABEL = "by construction (guard + _assert_bound)"


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def iso(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ms_of(s: str) -> int:
    return int(datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
               .timestamp() * 1000)


def git_blob(rel: str, rev: str = BUILD_REV) -> bytes:
    r = subprocess.run(["git", "-C", str(ROOT), "show", f"{rev}:{rel}"], capture_output=True)
    if r.returncode:
        raise SystemExit(f"HALT: git show {rev}:{rel} failed: {r.stderr.decode()[:200]}")
    return r.stdout


def flat(x, p: str = "") -> dict:
    if isinstance(x, dict):
        out = {}
        for k, v in x.items():
            out.update(flat(v, f"{p}.{k}" if p else k))
        return out if x else {p: {}}
    if isinstance(x, list):
        out = {}
        for i, v in enumerate(x):
            out.update(flat(v, f"{p}[{i}]"))
        return out if x else {p: []}
    return {p: x}


def pattern(path: str) -> str:
    """files[i].k -> files[*].k; a leaf under out_of_scope_snapshot_files[i] -> that row."""
    path = re.sub(r"^files\[\d+\]", "files[*]", path)
    return re.sub(r"^(out_of_scope_snapshot_files\[\d+\])\..*$", r"\1", path)


def json_changes(old: bytes, new: bytes) -> dict:
    a, b = flat(json.loads(old)), flat(json.loads(new))
    cnt = lambda keys: {k: n for k, n in sorted(Counter(pattern(x) for x in keys).items())}
    return {"changed": cnt(k for k in a if k in b and a[k] != b[k]),
            "added": cnt(k for k in b if k not in a),
            "removed": cnt(k for k in a if k not in b)}


def md_changes(old: bytes, new: bytes) -> dict:
    a, b = old.decode("utf-8").splitlines(), new.decode("utf-8").splitlines()
    ra, rb = Counter(a), Counter(b)
    gone, came = sum((ra - rb).values()), sum((rb - ra).values())
    return {"lines_before": len(a), "lines_after": len(b), "lines_gone": gone, "lines_new": came}


def build_note() -> dict:
    seal = json.loads((OUT / "WRITE_ONCE_SEAL.json").read_text(encoding="utf-8"))
    pin = json.loads((OUT / "AS_OF_PIN.json").read_text(encoding="utf-8"))
    man_b = (OUT / "STAGE_D_MANIFEST.json").read_bytes()
    man = json.loads(man_b)
    lines = (OUT / "FETCH_LOG.jsonl").read_text(encoding="utf-8").splitlines()
    fl = seal["fetch_log"]
    sealed = lines[: fl["sealed_lines"]]
    sealed_sha = sha_bytes(("\n".join(sealed) + "\n").encode("utf-8"))
    if sealed_sha != fl["sha256_of_sealed_lines"]:
        raise SystemExit("HALT: the fetch log's sealed prefix moved")
    rows = [json.loads(x) for x in sealed]
    clock_lines = [i + 1 for i, r in enumerate(rows) if r.get("phase") == "clock"]
    if len(clock_lines) != 1:
        raise SystemExit(f"HALT: {len(clock_lines)} phase='clock' rows in the sealed log, not 1")
    n = clock_lines[0]
    crow = rows[n - 1]
    if crow.get("endpoint") != "/fapi/v1/time" or crow.get("status") != 200:
        raise SystemExit(f"HALT: the sealed clock row is not a 200 GET /fapi/v1/time: {crow}")
    skew = int(pin["local_clock_skew_ms"])
    floors = set()
    for r in rows:
        t = ms_of(r["wall_clock_utc"])
        floors.update({(t - skew) // MS_4H * MS_4H, (t + 999 - skew) // MS_4H * MS_4H})
    if floors != {PIN_MS}:
        raise SystemExit(f"HALT: the sealed rows floor to {sorted(floors)}, not the pin alone")
    first, last = ms_of(rows[0]["wall_clock_utc"]), ms_of(rows[-1]["wall_clock_utc"])

    cap_b = (OUT / STDOUT_COPY).read_bytes()
    cap = cap_b.decode("utf-8").splitlines()
    quote = {str(k): cap[k - 1] for k in QUOTED_LINES}
    checks = (f"serverTime {pin['venue_server_time_ms']}" in quote["18"],
              f"closeTime of the bar {pin['venue_close_time_of_pinned_bar_ms']}" in quote["18"],
              f"(== pin: {pin['pin_equals_latest_closed_at_pin_run']})" in quote["19"],
              f"+ {fl['sealed_lines']} fetch-log lines" in quote["155"])
    if not all(checks):
        raise SystemExit(f"HALT: the stdout capture disagrees with the filed records {checks}")

    redes, changes = {}, {}
    for name in REDESCRIBED:
        old, new = git_blob(f"{REL_OUT}/{name}"), (OUT / name).read_bytes()
        redes[name] = {"old_sha256": sha_bytes(old), "old_source": f"git {BUILD_REV}:{REL_OUT}/{name}",
                       "new_sha256": sha_bytes(new)}
        changes[name] = md_changes(old, new) if name.endswith(".md") else json_changes(old, new)
    old_man = json.loads(git_blob(f"{REL_OUT}/STAGE_D_MANIFEST.json"))

    return {
        "tier": "TIER-C11", "stage": "TC11-D", "seed": SEED,
        "as_of_last_closed_4h": pin["as_of_last_closed_4h"],
        "as_of_last_closed_4h_close_ms": pin["as_of_last_closed_4h_close_ms"],
        "law": ("L-0.1 (research_outputs/tierc11/LEANS.md): 'the latest close at fetch time is "
                "printed beside it'. The --all run of 2026-09-25 PRINTED it (stdout) but never FILED "
                "it: LOG_LINES is never written and the fetch log's clock row carries no serverTime "
                "(research_outputs/tierc11/review/TC11-D_VERIFY.md defect 8)."),
        "what_this_note_is": (
            "an after-the-fact record, derived ONLY from what the filed records show, with the --all "
            "run's stdout capture (filed as a byte copy) quoted as corroboration. FETCH_LOG.jsonl, "
            "WRITE_ONCE_SEAL.json and AS_OF_PIN.json are write-once records and were NOT rewritten. "
            "STAGE_D_MANIFEST.json/.md and fee_schedule.json are not write-once; they were "
            "RE-DESCRIBED once, by the repair after the round-2 verification, and "
            "manifest_redescribed lists every change."),
        "generated_by": {
            "script": "scripts/tierc11_data_clock_note.py --write",
            "reads": (f"{REL_OUT}/{{WRITE_ONCE_SEAL.json, AS_OF_PIN.json, FETCH_LOG.jsonl, "
                      f"STAGE_D_MANIFEST.json, STAGE_D_MANIFEST.md, fee_schedule.json, {STDOUT_COPY}}} "
                      f"and git {BUILD_REV}; no network, no snapshot read, no clock"),
            "replaces": ("the session-scratch one-off make_clock_note.py that wrote the first note "
                         "(round-2 verification, finding 3)"),
        },
        "fetch_time_latest_closed_4h": iso(PIN_MS),
        "fetch_time_latest_closed_4h_close_ms": PIN_MS,
        "fetch_time_latest_equals_pin": True,
        "venue_server_time_ms_at_fetch_clock_call": crow.get("venue_server_time_ms"),
        "venue_server_time_at_fetch_clock_call_status": (
            "NEVER RECORDED in any filed file. The fetch-time clock call's response (serverTime) "
            "was printed to stdout to the SECOND only ('venue clock 2026-09-25T00:57:47Z', capture "
            "line 20 below) and its millisecond value exists nowhere. It is left null here, not "
            "reconstructed."),
        "fetch_time_clock_call": {
            "fetch_log": f"{REL_OUT}/FETCH_LOG.jsonl",
            "line": n,
            "row": crow,
            "carries_venue_server_time": "venue_server_time_ms" in crow,
            "reading": (f"the only phase='clock' row of the sealed log: GET /fapi/v1/time, status 200, "
                        f"local wall clock {crow['wall_clock_utc']}; the sealed log holds "
                        f"{sum(1 for r in rows if r.get('kind') == 'clock')} kind='clock' rows (the "
                        "code of that run did not write one)"),
        },
        "derivation": {
            "law": ("the latest closed 4h bar at instant t closes at floor(t / 14400000) * 14400000 "
                    "ms (the venue stamps its closeTime at close - 1 ms, so at t >= close the bar is "
                    "closed)"),
            "clock_used": ("each sealed fetch-log row's local wall_clock_utc (1 s resolution: the true "
                           "instant lies in [t, t + 999 ms]) corrected by AS_OF_PIN.local_clock_skew_ms "
                           "(local - venue, measured at the pin call of the same run)"),
            "local_clock_skew_ms": skew,
            "fetch_log_sealed_lines": fl["sealed_lines"],
            "fetch_log_sha256_of_sealed_lines": sealed_sha,
            "first_row_utc": rows[0]["wall_clock_utc"],
            "clock_row_utc": crow["wall_clock_utc"],
            "last_row_utc": rows[-1]["wall_clock_utc"],
            "distinct_4h_floor_close_ms_over_every_sealed_row": sorted(floors),
            "seconds_after_the_pinned_close_at_the_first_row": (first - skew - PIN_MS) // 1000,
            "seconds_before_the_next_4h_close_at_the_last_row":
                (PIN_MS + MS_4H - (last + 999 - skew)) // 1000,
            "margins_law": ("both margins are the CONSERVATIVE bound, floored to the second: the "
                            "first row at its earliest venue instant (t - skew), the last row at its "
                            "latest (t + 999 - skew)"),
            "reading": (f"all {len(rows)} sealed rows (the pin call, the clock call and the whole "
                        "fetch) fall inside one 4h bar, [2026-09-25T00:00:00Z, 2026-09-25T04:00:00Z), "
                        "with ~57 min of margin after the pinned close and ~3 h before the next; a "
                        "clock error of minutes would not move the value. The latest closed 4h at "
                        "every instant of the fetch was 2026-09-25T00:00:00Z == the pin."),
        },
        "pin_run_record": {
            "source": f"{REL_OUT}/AS_OF_PIN.json (write-once, sealed)",
            "venue_server_time_ms": pin["venue_server_time_ms"],
            "venue_server_time": pin["venue_server_time"],
            "latest_closed_4h_at_pin_run": pin["latest_closed_4h_at_pin_run"],
            "latest_closed_4h_at_pin_run_close_ms": pin["latest_closed_4h_at_pin_run_close_ms"],
            "pin_equals_latest_closed_at_pin_run": pin["pin_equals_latest_closed_at_pin_run"],
        },
        "corroboration_stdout": {
            "what": ("stdout of `scripts/tierc11_data.py --all` as captured by the builder session, "
                     "FILED as a byte copy (sha256 equal) so the corroboration outlives session "
                     "scratch; quoted here verbatim. Not a write-once record."),
            "filed_copy": f"{REL_OUT}/{STDOUT_COPY}",
            "captured_at": STDOUT_CAPTURED_AT,
            "sha256": sha_bytes(cap_b),
            "lines": quote,
            "consistency": (f"line 18's serverTime {pin['venue_server_time_ms']} and closeTime "
                            f"{pin['venue_close_time_of_pinned_bar_ms']} == AS_OF_PIN.json; line 19's "
                            f"'(== pin: True)' == AS_OF_PIN.pin_equals_latest_closed_at_pin_run; "
                            f"line 155's {fl['sealed_lines']} fetch-log lines == "
                            "WRITE_ONCE_SEAL.fetch_log.sealed_lines"),
        },
        "live_cache_touched_relabel": {
            "file": f"{REL_OUT}/STAGE_D_MANIFEST.json",
            "key": "live_cache_touched",
            "filed_value": man["live_cache_touched"],
            "reading_of_record": RELABEL,
            "basis_key": "live_cache_touched_basis",
            "basis_filed": man.get("live_cache_touched_basis"),
            "meaning": ("the filed False is NOT a measurement. The build's live-cache claim rests on "
                        "construction: guard_substrate HALTs at import unless NAIAD_CACHE_DIR is the "
                        "TC11 snapshot (F-D11-GUARD, which imports the module in a subprocess), and "
                        "_assert_bound HALTs before every snapshot write unless "
                        "engine.data.cache_dir() still resolves to it (F-D11-BOUND). The live-cache "
                        "stat in F-D11-UNTOUCHED covers a fixture run only."),
            "source": ("research_outputs/tierc11/review/TC11-D_VERIFY.md defect 3; the basis key is "
                       "filed in the manifest since the re-describe (round-2 verification, finding 2)"),
        },
        "l01_lean_erratum": {
            "reading": ("L-0.1 (research_outputs/tierc11/LEANS.md:24-25): 'Every stage reads it, and "
                        "the latest close at fetch time is printed beside it.'"),
            "filed_at_build": old_man["leans"][0],
            "misquote": ("the build's lean said 'the latest close at pin time is filed beside it'; "
                         "the PIN-time close is filed (AS_OF_PIN.latest_closed_4h_at_pin_run), but "
                         "L-0.1 reads the FETCH-time close, printed"),
            "filed_now": man["leans"][0],
            "source": "TC11-D verification round 2, defect 6",
        },
        "code_change_for_future_runs": (
            "scripts/tierc11_data.py record_fetch_clock(): --all (after the pin, before the fetch "
            "and the seal), --pin and --fetch append one kind='clock' row to FETCH_LOG.jsonl "
            "carrying venue_server_time_ms and latest_closed_4h_close_ms beside the pin"),
        "records_not_rewritten_sha256": {
            "AS_OF_PIN.json": sha_bytes((OUT / "AS_OF_PIN.json").read_bytes()),
            "WRITE_ONCE_SEAL.json": sha_bytes((OUT / "WRITE_ONCE_SEAL.json").read_bytes()),
            "FETCH_LOG.jsonl": sealed_sha,
        },
        "records_not_rewritten_law": (
            "whole-file sha256 for AS_OF_PIN.json and WRITE_ONCE_SEAL.json; for the append-only "
            f"FETCH_LOG.jsonl, the sha256 of its sealed {fl['sealed_lines']}-line prefix (the whole "
            "file when this note was written) — a later --pin or --fetch appends kind='clock' rows "
            "past the prefix without moving it (round-2 verification, finding 5)"),
        "manifest_redescribed": {
            "by": "scripts/tierc11_data.py --manifest (no network, no snapshot write)",
            "when": "2026-09-25, the repair of TC11-D after the round-2 verification",
            "why": [
                "defect 6: the L-0.1 lean misquoted the reading (l01_lean_erratum)",
                "defect 7: the snapshot root's stale MANIFEST.json was undisclosed "
                "(out_of_scope_snapshot_files + a standing disclosure)",
                "defect 8: parquet content shas for F-DET (files[*].content_sha, "
                "files[*].derivation_content_sha, content_sha_law) [L-F.1]",
                "finding 1: the maker twin's stop and invalidation legs are taker WITHOUT slippage "
                "[L-1.2] (leans[15], fee_schedule.maker_law)",
                "finding 2: live_cache_touched_basis filed beside live_cache_touched",
            ],
            "files": redes,
            "changes": changes,
            "numbers_moved": ("none — every changed path is a text (leans[0], leans[15], maker_law) "
                              "and every other path is ADDED; `changes` is the whole diff"),
        },
        "verified_by": (
            "F-D11-CLOCK in scripts/tierc11_data_fixtures.py re-derives every field of this note "
            "from the filed records, the filed stdout copy and git e97ad73 ([note-top], [note-row], "
            "[note-server-time], [note-latest], [note-derivation], [note-pin-run], [note-records], "
            "[note-corroboration], [note-relabel], [note-erratum], [note-redescribe]) and holds the "
            "filed bytes to build_note() ([note-provenance])"),
    }


def note_bytes(note: dict) -> bytes:
    return (json.dumps(note, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    args = sys.argv[1:]
    body = note_bytes(build_note())
    p = OUT / NOTE
    if args == ["--write"]:
        old = sha_bytes(p.read_bytes()) if p.exists() else None
        p.write_bytes(body)
        print(f"{p}: {old} -> {sha_bytes(body)}")
        return 0
    if args not in ([], ["--check"]):
        raise SystemExit("usage: tierc11_data_clock_note.py [--check | --write]")
    same = p.exists() and p.read_bytes() == body
    print(f"{p.name}: filed bytes {'==' if same else '!='} build_note() ({sha_bytes(body)[:16]}…)")
    return 0 if same else 1


if __name__ == "__main__":
    sys.exit(main())
