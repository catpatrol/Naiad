#!/usr/bin/env python
"""TIER-C12 · THE ENV SUITE [LEANS L-D.31, L-D.25; L-0.14] — one suite, one transcript per record
(`--stage=<record id>`, never a leg filter).

  --stage=TC12-ENV.vendor  ->  research_outputs/tierc12/env/FIXTURES_ENV_VENDOR.txt
      F-VENDOR [referee]   the vendored referee, before any hunk is applied: the three shas, the tag,
                           the hunk laws on the referee text.  NO SHIM IMPORT, no shim file needed,
                           no tape; the header's pin is read from data/AS_OF_PIN.json.
  (no --stage) = TC12-ENV  ->  env/FIXTURES_ENV.txt — F-VENDOR, F-SUBSTRATE, F-REROOT, F-ENV-ASOF,
      F-LINEAGE, F-TOLL [reader], F-CLOSURE-ENV, F-ENV-DET: filed by the TC12-ENV record, which adds
      its row to STAGES below.  ONE BLOCK LIST PER RECORD: a row is {transcript, banner, load,
      fixtures, typed}; the shim is imported inside the TC12-ENV row's `load` only, so the vendor
      stage never loads it.

A TRANSCRIPT OF RECORD STATES THE ESTATE AS OF ITS GATE.  This suite and scripts/tierc12_vendor.py are
both extended at the TC12-ENV record (the shim's legs; the hunk table).  The vendor transcript must
re-run byte-identical after that, so at --stage=TC12-ENV.vendor every line PRINTS only what is fixed at
this gate: the referee's bytes, the sha TC11's PROGRESS certifies, this suite's typed literals.  The
hunk laws are proven on a CONTROL TABLE typed here (a second object: one entry per declared hunk
number) through PRODUCTION's build_env_text.  The table of record (`ENV_HUNKS`) is JUDGED by the same
laws whenever it holds an entry — a breach turns this leg RED — and nothing of it is printed.  A caught
plant prints the DETECTOR production named in this suite's own words (CAUGHT_T), never production's
message text.  What this stage stands on in scripts/tierc12_vendor.py is therefore its API and its
detector names — referee_findings, three_shas, referee_tag, REFEREE_REL, hunk_numbers, ENV_HUNKS,
build_env_text; `sha != certified`, HUNK-NUMBER, HUNK-OLD, HUNK-UNUSED, HUNK-REVERT — and no wording.

SECOND OBJECTS.  The typed literals below are this suite's commission (L-0.14): the paths, the tag,
the stage name, the counts and the control table are typed here and production is compared against
them.  The three shas are read here by this suite's own code, never through production's functions.

`tracked and equal to its blob` (L-D.25's second block; L-0.9: read at --at, at the TC12-ENV gate,
after the vendor commit) is `referee_git_findings`, written here for that block.  At the vendor stage
the referee is not committed yet: the clause is held only when --at names a commit whose tree holds
the referee, and a fixed sentence says so.

Scratch copies live under $TMPDIR and are removed; nothing but the transcript is written under --root.

Run:  export PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/tierc12_env_fixtures.py \\
          --stage=TC12-ENV.vendor [--at=<sha>] [--refile-transcript] [--root=DIR]
Exit 0 = GREEN · 1 = a RED or VOID leg, a transcript finding, or a HALT.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import tierc12_fx as FX
import tierc12_pins as PINS
import tierc12_progress as PG
import tierc12_vendor as V

ROOT = Path(__file__).resolve().parents[1]

# ═══════════════════════════════════════════════════════ THE TYPED COMMISSION (second objects)
STAGE_VENDOR_T = "TC12-ENV.vendor"
DEFAULT_STAGE_T = "TC12-ENV"                 # L-D.31: the parent's invocation carries no --stage
T12_T = "research_outputs/tierc12"
T11_T = "research_outputs/tierc11"
ENV_T = T12_T + "/env"
TOOL_T = "scripts/tierc12_vendor.py"
REFEREE_T = T12_T + "/vendor/tierc11_env@1526093b.py"
TAG_T = "1526093b"                           # the label in the file name; must prefix the sha
SOURCE_T = "scripts/tierc11_env.py"
SOURCE_STAGE_T = "TC11-ENV"
T11_PROGRESS_T = T11_T + "/PROGRESS.json"
R0_T = T12_T + "/progress/TC12-R0.json"
R0_KEY_T = "frozen_estate_shas_at_r0"
STAMP_MAP_T = T12_T + "/close/TC11_STAMP_MAP.json"
PIN_T = T12_T + "/data/AS_OF_PIN.json"
MANIFEST_T = T12_T + "/data/STAGE_D_MANIFEST.json"
SNAPSHOT_KEYS_T = ("snapshot_root", "snapshot_name", "snapshot")
N_LINES_T = 1381                             # L-D.25: "1,381 lines"
N_HUNKS_T = 10                               # L-D.26: the ten hunks
# THE CONTROL TABLE: one entry per declared hunk number.  Each `old` is a line that stands exactly once
# in the referee; each `new` is that line with a marker.  It proves the laws GREEN on a lawful table,
# and every hunk plant is this table plus ONE bad entry.
CONTROL_ANCHORS_T = (
    "HOME = Path.home()\n",
    'OUT = ROOT / "research_outputs" / "tierc11"\n',
    "SEED = 20260924\n",
    "N_BOOT = 4000\n",
    'LEAN_TAG = "[LEAN-HEPHAESTUS]"\n',
    'ERA_CUT_ISO = "2024-06-30T23:59:59Z"\n',
    '_ENV_OF_RECORD = os.environ.get("NAIAD_CACHE_DIR")\n',
    "REROOTS: list[dict] = []\n",
    "CLASSIC5 = tuple(TP.CLASSIC5)\n",
    "PANEL17 = tuple(TP.PANEL17)\n",
)
TWICE_ANCHOR_T = '    "research_outputs/tierc10/data/STAGE_D_MANIFEST.json":\n'    # twice in the referee
ELEVENTH_ANCHOR_T = "MAIN_TREE = _main_tree(ROOT)\n"                               # once; in no control entry
# the DETECTORS of production this stage's plants must be caught by, each with the words printed for it
CAUGHT_T = {
    "sha != certified": "production's referee_findings refused the bent copy: it does not hash to the sha "
                        "TC11's PROGRESS certifies",
    "HUNK-OLD": "production's build_env_text refused the table: an `old` that does not occur exactly once",
    "HUNK-NUMBER": "production's build_env_text refused the table: a hunk number that is not declared",
}
GIT_T = ("git", "--no-optional-locks", "-C")

CTX: dict = {}                               # the run: stage, --at, the referee's bytes, scratch


def halt(msg: str):
    raise SystemExit(f"HALT: {msg}")


# ═══════════════════════════════════════════════════════ THIS SUITE'S OWN READS (never production's)
def own_certified() -> str:
    """The sha TC11's PROGRESS certifies for scripts/tierc11_env.py under stage TC11-ENV, read by key —
    PROGRESS held to the sha TC12's R0 census recorded for it, or to the applied stamp map's."""
    raw = (ROOT / T11_PROGRESS_T).read_bytes()
    want = json.loads((ROOT / R0_T).read_text(encoding="utf-8"))[R0_KEY_T][T11_PROGRESS_T]["sha256"]
    stamp = ROOT / STAMP_MAP_T
    if stamp.is_file():
        doc = json.loads(stamp.read_text(encoding="utf-8"))
        if doc.get("applied") is True:
            want = next((m["sha256_after"] for m in doc.get("moved", []) if m.get("path") == T11_PROGRESS_T), want)
    if FX.sha_bytes(raw) != want:
        halt(f"{T11_PROGRESS_T} is not at the sha TC12's R0 census (or the applied stamp map) holds for it")
    stages = [s for s in json.loads(raw)["stages"] if s.get("stage") == SOURCE_STAGE_T]
    if len(stages) != 1:
        halt(f"{T11_PROGRESS_T} holds {len(stages)} stage(s) named {SOURCE_STAGE_T}")
    return stages[0]["artifact_shas"][SOURCE_T]["sha256"]


def own_three_shas() -> dict:
    return {"certified": own_certified(), "live": FX.sha_bytes((ROOT / SOURCE_T).read_bytes()),
            "vendored": FX.sha_bytes((ROOT / REFEREE_T).read_bytes())}


def substrate_header() -> dict:
    """The header's pin and snapshot name, from Stage D's records at their certified shas [L-D.31]."""
    pin = json.loads(PG.read_certified(PIN_T, ROOT))
    manifest = json.loads(PG.read_certified(MANIFEST_T, ROOT))
    name = next((manifest[k] for k in SNAPSHOT_KEYS_T if isinstance(manifest.get(k), str)), None)
    if name is None:
        halt(f"{MANIFEST_T} names no snapshot")
    return {"substrate": Path(name).name, "as_of_iso": pin["as_of_last_closed_4h"],
            "pin": pin["as_of_last_closed_4h_close_ms"]}


# ═══════════════════════════════════════════════════════ THE HUNK LAWS, THROUGH PRODUCTION
def control_table() -> list:
    return [(k + 1, f"CONTROL: hunk {k + 1}", old, old[:-1] + f"  # F-VENDOR control {k + 1}\n")
            for k, old in enumerate(CONTROL_ANCHORS_T)]


def own_revert(text: str, table) -> str:
    """This suite's own reading of "the hunks reverted in reverse order": each `new` exactly once at
    its step, replaced by its `old`."""
    for no, what, old, new in table[::-1]:
        if text.count(new) != 1:
            raise ValueError(f"hunk {no} ({what}): its `new` stands {text.count(new)}x at its revert step")
        text = text.replace(new, old, 1)
    return text


def hunk_law_findings(table) -> list:
    """PRODUCTION's build_env_text on the referee text with `table` — its HALT is the finding
    (HUNK-NUMBER, HUNK-OLD, HUNK-UNUSED, HUNK-REVERT).  On a build, the built text reverted by THIS
    suite's own loop must be the referee byte for byte (HUNK-REVERT)."""
    ref = CTX["referee"]
    try:
        built = V.build_env_text(ref.decode("utf-8"), table)
    except SystemExit as e:
        return [str(e)]
    try:
        back = own_revert(built, table)
    except ValueError as e:
        return [f"HUNK-REVERT (this suite's own loop): {e}"]
    return [] if back.encode("utf-8") == ref else [
        "HUNK-REVERT (this suite's own loop): the built text, its hunks reverted in reverse order, is not the "
        "referee byte for byte"]


def caught(found: list, want: str) -> list:
    """What a plant PRINTS: the detector production named, in this suite's own fixed words — never
    production's message text, which the TC12-ENV record may reword when it extends the tool (a
    transcript of record does not move with it).  A finding that does not name `want` is handed back
    as it is: the harness then reads the wrong detector."""
    return [f"{want} — {CAUGHT_T[want]}" if want in x else x for x in found]


def table_plant(bad_entry, want: str):
    """A HUNK-TABLE COPY with ONE bad entry appended: the control table always, and a copy of the table
    of record too whenever it holds an entry — the plant is caught on both or it passed."""
    def thunk():
        found = hunk_law_findings(control_table() + [bad_entry])
        of_record = list(V.ENV_HUNKS)
        if of_record and not any(want in x for x in hunk_law_findings(of_record + [bad_entry])):
            return []
        return caught(found, want)
    return thunk


# ═══════════════════════════════════════════════════════ `tracked and equal to its blob` [L-D.25; L-0.9]
def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([*GIT_T, str(ROOT), *args], capture_output=True, timeout=60)


def referee_git_findings(at, required: bool) -> list:
    """VENDOR-GIT: the referee is not in the tree of the commit `--at` names, or differs from its blob
    there (read-only git).  `required` = the TC12-ENV gate, where the vendor commit precedes --at and
    the clause is mandatory; False = the vendor stage, where it is held only when that tree holds the
    referee.  [] is GREEN."""
    if at is None:
        return [f"VENDOR-GIT: no --at was given — the clause reads the referee's blob at the gate's --at"] \
            if required else []
    if _git("cat-file", "-e", f"{at}:{REFEREE_T}").returncode != 0:
        return [f"VENDOR-GIT: {REFEREE_T} is not in the tree of --at — the referee is untracked there"] \
            if required else []
    blob = _git("show", f"{at}:{REFEREE_T}")
    if blob.returncode != 0 or blob.stdout != (ROOT / REFEREE_T).read_bytes():
        return [f"VENDOR-GIT: {REFEREE_T} differs from its blob at --at"]
    return []


# ═══════════════════════════════════════════════════════ F-VENDOR [referee]
def referee_break():
    ref = CTX["referee"]
    text = ref.decode("utf-8")
    if V.referee_findings() or hunk_law_findings(control_table()):
        raise RuntimeError("the unbent referee or the control table is not GREEN — the plants would prove nothing")
    if text.count(TWICE_ANCHOR_T) != 2 or text.count(ELEVENTH_ANCHOR_T) != 1 \
            or ELEVENTH_ANCHOR_T in CONTROL_ANCHORS_T:
        raise RuntimeError("a plant's anchor does not stand in the referee as this suite types it")
    bent = bytearray(ref)
    bent[len(bent) // 2] ^= 1
    copy = Path(CTX["tmp"]) / Path(REFEREE_T).name
    copy.write_bytes(bytes(bent))
    return FX.plants([
        ("a one-byte edit of a COPY of the referee", "sha != certified",
         lambda: caught(V.referee_findings(referee=copy.read_bytes()), "sha != certified")),
        ("a hunk-table copy whose `old` occurs twice in the referee", "HUNK-OLD",
         table_plant((1, "PLANT: an `old` that stands twice", TWICE_ANCHOR_T, TWICE_ANCHOR_T + "# planted\n"),
                     "HUNK-OLD")),
        ("an eleventh hunk number in a hunk-table copy", "HUNK-NUMBER",
         table_plant((N_HUNKS_T + 1, "PLANT: an eleventh hunk", ELEVENTH_ANCHOR_T,
                      ELEVENTH_ANCHOR_T[:-1] + "  # planted\n"), "HUNK-NUMBER")),
    ])


def referee_real():
    ref, own = CTX["referee"], own_three_shas()
    bad = list(V.referee_findings())
    prod = V.three_shas()
    if {k: prod[k] for k in own} != own:
        bad.append(f"VENDOR-SHA: production's three shas {prod} are not this suite's own reads {own}")
    equal = len(set(own.values())) == 1
    if not equal:
        bad.append(f"VENDOR-SHA: sha != certified — by this suite's own reads the three shas are not equal: {own}")
    tagged = (Path(REFEREE_T).name == f"tierc11_env@{TAG_T}.py" and V.REFEREE_REL == REFEREE_T
              and V.referee_tag() == TAG_T and own["certified"].startswith(TAG_T))
    if not tagged:
        bad.append(f"VENDOR-TAG: the tag {TAG_T!r} is not the file name's label or does not prefix "
                   f"{own['certified']}")
    n_lines = ref.count(b"\n")
    if n_lines != N_LINES_T:
        bad.append(f"VENDOR-LINES: the referee holds {n_lines} lines, not the reading's {N_LINES_T}")
    if tuple(V.hunk_numbers()) != tuple(range(1, N_HUNKS_T + 1)):
        bad.append(f"HUNK-NUMBER: production declares the hunk numbers {list(V.hunk_numbers())}, not 1..{N_HUNKS_T}")
    bad += hunk_law_findings(control_table())
    of_record = list(V.ENV_HUNKS)
    if of_record:                                # judged whenever it holds an entry; nothing of it is printed
        bad += hunk_law_findings(of_record)
    bad += referee_git_findings(CTX["at"], required=False)
    return (not bad), (
        f"the referee {REFEREE_T}: sha256 {own['vendored']} ({len(ref)} bytes, {N_LINES_T} lines) == the sha "
        f"{T11_PROGRESS_T} certifies for {SOURCE_T} under stage {SOURCE_STAGE_T} (read by key; that file held to "
        f"TC12's R0 census or the applied stamp map) == the live {SOURCE_T}'s — three shas equal: {equal}; the "
        f"tag {TAG_T!r} prefixes it: {tagged}; the file is read as bytes and never imported. THE HUNK LAWS on the "
        f"referee text, through production's build_env_text: the control table typed here ({N_HUNKS_T} entries, "
        f"one per declared hunk number 1..{N_HUNKS_T}, each `old` exactly once in the referee and in the text it "
        f"is applied to) builds, and its text with the hunks reverted in reverse order by this suite's own loop "
        f"is the referee byte for byte. THE TABLE OF RECORD (ENV_HUNKS of {TOOL_T}) is held to the same laws and "
        f"the same revert whenever it holds an entry — it is filed with the shim at {DEFAULT_STAGE_T}, whose "
        f"F-VENDOR block makes all {N_HUNKS_T} mandatory — and nothing of it is printed here. `tracked and equal "
        f"to its blob` is that block's clause, read at --at after the vendor commit [L-0.9]; at this stage it is "
        f"held only when --at names a commit whose tree holds the referee"
        + (f" — {len(bad)} finding(s): " + " | ".join(bad) if bad else ""))


def vendor_fixtures() -> list:
    return [
        ("F-VENDOR [referee]", "the vendored referee before any hunk is applied: three shas, the tag, the hunk "
                               "laws on the referee text [L-D.25]",
         "a one-byte edit of a COPY of the referee is not caught as `sha != certified`; or a hunk-table copy "
         "whose `old` occurs twice in the referee, or one holding an eleventh hunk number, builds",
         "the three shas are not equal — the vendored copy's, the one TC11's PROGRESS certifies for "
         "scripts/tierc11_env.py under stage TC11-ENV, the live file's; the tag in the file name does not prefix "
         "that sha; build_env_text(referee) breaks one of its own laws (an `old` that does not occur exactly "
         "once, a hunk number outside 1-10, a declared number unused); or the text it builds, with the hunks "
         "reverted in reverse order, is not the referee byte for byte",
         referee_break, referee_real),
    ]


def vendor_typed() -> list:
    return [
        f"--stage={STAGE_VENDOR_T} · the record: {REFEREE_T}, its README, {TOOL_T}, {ENV_T}/LINEAGE_PINS.json — "
        f"no shim import, no tape; the header's pin is read from {PIN_T}",
        f"REFEREE_T {REFEREE_T} · TAG_T {TAG_T} · SOURCE_T {SOURCE_T} · SOURCE_STAGE_T {SOURCE_STAGE_T} of "
        f"{T11_PROGRESS_T} · N_LINES_T {N_LINES_T} · N_HUNKS_T {N_HUNKS_T}",
        f"the control table: {len(CONTROL_ANCHORS_T)} anchors, one per declared hunk number, each a line standing "
        f"once in the referee, e.g. {CONTROL_ANCHORS_T[0]!r} — typed entries, no hunk of record",
        f"plant anchors: TWICE_ANCHOR_T {TWICE_ANCHOR_T!r} (twice in the referee) · ELEVENTH_ANCHOR_T "
        f"{ELEVENTH_ANCHOR_T!r} (once; in no control entry)",
        "n = 1 referee, 3 plants (nothing is drawn at this record: no seeded leg)",
    ]


def load_vendor() -> None:
    """The record this stage verifies: the referee's bytes.  Nothing of the shim is loaded."""
    p = ROOT / REFEREE_T
    if not p.is_file():
        halt(f"{REFEREE_T} is not on file — run {TOOL_T} --vendor first")
    CTX["referee"] = p.read_bytes()


# ═══════════════════════════════════════════════════════ THE ROLL — one row per record
STAGES = {
    STAGE_VENDOR_T: {
        "transcript": "FIXTURES_ENV_VENDOR.txt",
        "banner": f"TIER-C12 ENV FIXTURES at {STAGE_VENDOR_T} — the vendored referee before any hunk is applied "
                  f"(L-D.25): no shim import, no tape — break leg first, RED or void",
        "load": load_vendor, "fixtures": vendor_fixtures, "typed": vendor_typed},
}


def main(argv) -> int:
    stage = FX.opt(argv, "--stage=", DEFAULT_STAGE_T)
    if stage not in STAGES:
        halt(f"--stage={stage!r}: this suite serves the records {sorted(STAGES)} (one transcript each; "
             f"`--stage` is never a leg filter; no --stage means {DEFAULT_STAGE_T})")
    at = FX.opt(argv, "--at=")
    if at is not None and not re.fullmatch(r"[0-9a-f]+", at):
        halt(f"--at={at!r} is not a commit sha")
    root = Path(FX.opt(argv, "--root=", str(ROOT / ENV_T)))
    row = STAGES[stage]
    CTX.clear()
    CTX.update(stage=stage, at=at, tmp=tempfile.mkdtemp(prefix="tc12_env_fx_"))
    try:
        row["load"]()
        return FX.run_suite(args=argv, root=root, transcript=row["transcript"], banner=row["banner"],
                            seed=PINS.pin("seed"), fixtures=row["fixtures"](), typed=row["typed"](),
                            **substrate_header())
    finally:
        shutil.rmtree(CTX["tmp"], ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
