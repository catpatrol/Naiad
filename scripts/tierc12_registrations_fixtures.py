#!/usr/bin/env python
"""TIER-C12 · TC12-REG · THE REGISTRY SUITE [LEANS L-X.16 … L-X.22, L-X.13, L-X.18; CANON-24's row;
AMENDMENTS_PROPOSED AP-1 (its DEFAULT)] — eight blocks.

  F-CONTRACT-PIN         the contract is pinned by its PREFIX: an appended `BUILT:` line moves nothing
  F-REG [SLICE]          every text, context and external slice re-cuts from pinned bytes
  F-REG [HASH]           payload shas, the chain from the genesis string, the head, TC11's law by object
  F-REG [WRITE-ONCE]     a second filing changes no byte and does not exit 0
  F-REG [TEMPLATE]       each rule carries the ONE template of its registration id, byte for byte
  F-REG [SPEC-VERBATIM]  spec leaf == plan block == LEANS block; the machine-read fields in one grammar
  F-REG [VERIFIER]       each plant caught by its intended detector, one at a time; the independent
                         re-derivation written in THIS file agrees with the filing
  F-ATTEST-ORDER [REG]   the disk at filing holds nothing outside PRE_REG ∪ REG_SET; ATTEST_REG.json is
                         that listing

AFTER FILING.  The REAL legs judge the FILING and the LISTING OF THE ATTESTED INSTANT, so this
transcript re-passes after every lawful later act [L-0.11's scope law]:
  · a `BUILT:` line appended to the contract [L-X.16] — the prefix is what is read; the whole-file
    sha at filing is compared by nothing;
  · an amendment appended to LEANS_AMENDMENTS.md, a proposal to AMENDMENTS_PROPOSED.md [L-X.19,
    O-35] — a text that only grows is held to a BYTE-PREFIX at the sha on file;
  · a later record's files, the ledger-spec child among them [L-X.21: "filed AFTER the attested
    instant"] — a path the listing does not name is no finding here; ATTEST-ORDER holds it to git
    ancestry at TC12-SCORE and CLOSE;
  · a lawful repair of a REG_SET script under a dated amendment, re-recorded by the record of the
    gate that repairs it [AM-67, ruling on AP-66; L-0.4 (1)].
Every other pinned text (LEANS.md, the review, the plan, the paste, the rulings and the disclosures
frozen from the TC12-REG commit) stays held to its whole-file sha by the filing's own legs; the files
the gate itself writes after the attested instant are LATER_T.

THE LISTING IS A STATEMENT ABOUT THE FILING INSTANT [AM-67].  F-ATTEST-ORDER [REG] holds a listed
path that the registry commit TRACKS — the commit that first adds registrations/REGISTRATIONS.json
(`git log --diff-filter=A --format=%H -- <path>`, read-only, --no-optional-locks) — to the sha of its
BLOB at that commit, never to the working file: the blob is immutable, so a later lawful repair
cannot move it.  A listed path that commit does not track (the git-ignored x_rec/**) is held on the
working file, as before; LATER_T and the append-only byte-prefix rule are unchanged.  A tree that
holds no such commit yet (the tree at its own TC12-REG gate; a scratch tree) is held on the working
file throughout — the form the plants are judged in.  The blob form is proven on scratch
REPOSITORIES by controls that raise (the break leg is then VOID) and print nothing when they hold.

Production is scripts/tierc12_registrations.py and the filed pair under registrations/.  Every BREAK
plant is a mutation INSIDE production's inputs or source — a bent copy of the filed document, the pin,
the plan, the contract prefix (with a scratch STEP Q record so the plant reaches the law it names), a
scratch tree, or a shadow copy of the filer — judged one at a time by the detector the plant names.
The referees below are this suite's typed commission and its own re-derivation (slices, shas, chain,
the template table, the grammar): a second object.  No value is read back from the filer to judge it.

PRE-SUBSTRATE: no bar is read, no book exists, no env is imported, no network is touched.  Git is
asked two read-only verbs of the tree this suite stands in (`log`, `cat-file`, out of process
[L-X.21 clause 3]); a write verb runs only in a scratch repository under this run's temp directory.
The registry must be ON FILE (`tierc12_registrations.py --file`, then `--attest`).

Run (stdlib only; the transcript is registrations/FIXTURES_REG.txt):
  ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/tierc12_registrations_fixtures.py
      [--root=DIR] [--refile-transcript] [<leg filter> ...]
Exit 0 = every leg GREEN, every break RED, the transcript byte-identical to the record.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import tierc12_fx as FX                    # noqa: E402
import tierc12_pins as PINS                # noqa: E402
import tierc12_progress as PROGRESS        # noqa: E402
import tierc12_registrations as REG        # noqa: E402

ROOT = PINS.ROOT
MAIN = PINS.main_tree(ROOT)
T12_REL = "research_outputs/tierc12"
T12 = ROOT / T12_REL
TRANSCRIPT = "FIXTURES_REG.txt"
BANNER = ("TIER-C12 TC12-REG REGISTRY FIXTURES — L-X.16 the prefix pin · L-X.17 the slice law · L-X.18 "
          "the carry law and the field grammar · L-X.19 the hash law · L-X.20 write-once · L-X.21 "
          "text before result · L-X.22 the verifier — break leg first, RED or void")

# ═══════════════════════════════════════════════ THE TYPED COMMISSION (second objects)
SEED_T = 20261008
SEED_SENS_T = 20260816
N_BOOT_T = 4000
SCORED_END_MS_T = 1790294400000
ERA_CUT_MS_T = 1719791999000
CONTRACT_T = "exchange/queue/2026-10-08_TC12_APOLLO.md"
PREFIX_BYTES_T = 12209
PREFIX_SHA_T = "861d6050e80e66995e4f9db2855aaf274d63285249c2549e5a0813582095a7bd"
N_LINES_T = 137
GENESIS_T = "0" * 64
IDS_T = ("P-ADM-1", "P-BRD-1", "P-DIR-1", "P-SFP-VA-1", "P-SCALP-3")
# L-X.17's line map, the rows a filing cuts: (first line, last line, sha256 of the slice)
TEXT_T = {
    "P-ADM-1": (53, 56, "b4f14e60f766ddfd7bf7847fcdccb4b069f6a32fd16816e0a27f7ceacd8281a1"),
    "P-BRD-1": (57, 59, "e049d8d9fb62cc5cf15e1145c696270c5bd369aeae63a5b2570a1d6d5decfd7d"),
    "P-DIR-1": (65, 68, "1b4dec34d1337d49e22266006550421d8e4d88618e639a6581078c3fb0fcaf26"),
    "P-SFP-VA-1": (69, 75, "f6e581da8fe470b9f3fe9e414b466459ec0180af8dbcad3c57cdfcdf2d9d2754"),
    "P-SCALP-3": (83, 106, "fa141ec5d25ab67fbe57a673b676d94152dd287f145f66621e0d23b2e1b52198"),
}
LAWS_T = (5, 9, "3ce9d5f8213a39ca03843fb2c73833dc7854c01115fd92a325d9f945409525d6")
HEADERS_T = {
    "ADMISSION": (52, 52, "9c75b3ec4f751ee0f64143076a3724267328452bdfd791946ae868178d6cf6b0"),
    "RANGE-STATE": (64, 64, "8b1038704f484036362d644634faeba64e5543313f1af007a548b694a687a4bb"),
    "SCALPER": (82, 82, "886cea7d7542363f6b47a16667efb8c1c03f15fce92829c3eb3e3ccacedd2db9"),
}
N_MAP_ROWS_T = 25
# the families [L-X.1, L-X.2]: id -> (family, stage, m, bar text, bar exact, prior %)
Q_T = "0.10"
FAMILY_T = {
    "P-ADM-1": ("ADMISSION", "G", 2, "0.05", "1/20", 50),
    "P-BRD-1": ("ADMISSION", "G", 2, "0.05", "1/20", 40),
    "P-DIR-1": ("RANGE-STATE", "R", 2, "0.05", "1/20", 45),
    "P-SFP-VA-1": ("RANGE-STATE", "R", 2, "0.05", "1/20", 45),
    "P-SCALP-3": ("SCALPER", "S", 1, "0.10", "1/10", 30),
}
R_FAM_T = re.compile(r"^STAGE ([A-Z]) · ([A-Z][A-Z-]*) FAMILY \(m=(\d+), bar (\d+\.\d+)(?=[;)])")
R_Q_T = re.compile(r"bar = (\d+\.\d+) ÷ m per family")
# L-X.13's table, byte for byte: id -> (label key, tag, label, cell template)
_KIN_T = ("<verdict> — NOT CONFIRMATORY (pre_seen · KIN-SEEN: X3 printed value-area swing-failure "
          "outcomes on these bars)")
_HAZARD_T = "<verdict> — NOT CONFIRMATORY (selection_hazard: direction-informed)"
_RESCORE_T = "<verdict> — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (pre_seen: <clause>)"
TEMPLATES_T = {
    "P-ADM-1": ("pre_seen", "none", "IN-SAMPLE RE-SCORE, NOT CONFIRMATORY", _RESCORE_T),
    "P-BRD-1": ("selection_hazard", "direction-informed", "NOT CONFIRMATORY", _HAZARD_T),
    "P-DIR-1": ("selection_hazard", "direction-informed", "NOT CONFIRMATORY", _HAZARD_T),
    "P-SFP-VA-1": ("pre_seen", "KIN-SEEN", "NOT CONFIRMATORY", _KIN_T),
    "P-SCALP-3": ("pre_seen", "KIN-SEEN", "NOT CONFIRMATORY", _KIN_T),
}
RESCORE_IDS_T = ("P-ADM-1",)                 # CANON-01: "re-score" in P-ADM-1's template and label alone
RESCORE_RX_T = re.compile("re-score", re.IGNORECASE)
# AP-1's DEFAULT: the ruler sentence, and the items every printed-beside list must hold
RULER_T = ("verdict_of_record = SUPPORTED iff (a) the cluster-90% CI lower bound (the 5th percentile of "
           "the draws) > 0 AND (b) one-sided p <= q ÷ m, exact, AND (c) every declared asset holds at "
           "least one row in every arm the ruler reads; else NOT SUPPORTED. m is fixed in every case; a "
           "registration closed by its precondition prints 'CLOSED BY PRECONDITION (…) — no number · no "
           "test spent', spends no test and never loosens the bar.")
BESIDE_T = ("the sensitivity seed", "the haircut and all-taker twins", "the tuning and holdout slices",
            "LOAO", "both single-trade shares", "the literal-bar column",
            "the exact enumeration with SEED-FRAGILE", "the month-block twin with TIME-CLUSTER FRAGILE",
            "the drop-OPEN twin with VERDICT RESTS ON OPEN MARKS", "the forward strip unscored")
RULER_WORDS_T = {"P-ADM-1": "two-sample vs v6", "P-BRD-1": "two-sample vs v6",
                 "P-DIR-1": "two-sample vs v6", "P-SFP-VA-1": "vs zero", "P-SCALP-3": "vs zero"}
# L-X.18: the fifteen fields, the nine of the operative_spec, the items per `preconditions`
FIELDS_T = ("id", "family", "family_m", "family_bar", "prior", "mechanism", "population", "arms",
            "statistic", "comparison", "preconditions", "verdict_rule", "labels", "disclosed_beside",
            "failure_conditions")
CHECKED_T = ("id", "family", "family_m", "family_bar", "prior")
SPEC_KEYS_T = ("mechanism", "population", "arms", "statistic", "comparison", "preconditions", "labels",
               "disclosed_beside", "failure_conditions")
PRECOND_T = {"P-ADM-1": 0, "P-BRD-1": 0, "P-DIR-1": 0, "P-SFP-VA-1": 2, "P-SCALP-3": 1}
# the external slices the owners' blocks declare: id -> ((path, file sha256, first, last), ...)
_X4_T = ("research_outputs/tierc12/x_rec/tierc11x/era/X4.md",
         "aac2be88b8d71f46c232a1976cd5d06dd5ded91b3356976050a48344e9557be8")
EXTERNAL_T = {
    "P-ADM-1": (("research_outputs/tierc11/stage_g/STAGE_G.md",
                 "440509bc8c00bc32b48f745a8f76ca1b6c6d6ddb08f708432790ec164e2d0187", 187, 198),),
    "P-BRD-1": ((*_X4_T, 16, 16), (*_X4_T, 28, 28)),
}
# L-X.19 / L-X.20: the keys, in the filed order (the paste's pin `resume_paste` beside the contract)
TOP_KEYS_T = ("tier", "contract", "resume_paste", "leans", "amendments", "review", "plan", "rulings",
              "disclosures", "families", "verdict_law", "statistics", "scored_window", "era_cut",
              "registrations", "chain", "head", "law", "law_source")
BODY_KEYS_T = ("registration", "seq", "family", "family_m", "family_bar", "prior_pct", "seed",
               "text_of_record", "text_lines", "context_of_record", "external_context", "operative_spec",
               "verdict_rule", "text_sha256", "sha256")
PIN_KEYS_T = ("amendments", "chain", "contract", "disclosures", "families", "genesis", "head", "law",
              "law_source", "leans", "n_boot", "order_of_filing", "plan", "registrations",
              "registrations_file", "registry_len", "resume_paste", "review", "rulings", "seed",
              "seed_sens", "spec_carry_law", "text_before_result_law", "tier", "witness_law")
PINNED_T = {"resume_paste": "exchange/queue/2026-10-09_TC12_RESUME_APOLLO.md",
            "leans": T12_REL + "/LEANS.md", "amendments": T12_REL + "/LEANS_AMENDMENTS.md",
            "review": T12_REL + "/review/LEANS_REVIEW_2026-10-09.json",
            "plan": T12_REL + "/REGISTRATION_PLAN.md", "rulings": T12_REL + "/ORCHESTRATOR_RULINGS.md",
            "disclosures": T12_REL + "/DISCLOSURES.md"}
T11_REG_T = "research_outputs/tierc11/registrations/REGISTRATIONS.json"
T11_HEAD_T = "6772568b31fcfb2d56eb8c80b66dedee4fb5082673369e872972df8f475ec8f9"
# L-X.22's nineteen detectors, and the fifteen plants of F-REG [VERIFIER]
DETECTORS_T = ("CONTRACT-PREFIX", "CONTRACT-TAIL", "TEXT-SLICE", "CONTEXT-SLICE", "EXTERNAL-SLICE",
               "PAYLOAD-SHA", "SEED", "FAMILY-PARSE", "FAMILY-BAR", "FAMILY-MEMBER", "FAMILY-M-COUNT",
               "RULER-TEXT", "TEMPLATE", "SPEC-GRAMMAR", "PRECOND-GRAMMAR", "CHAIN", "HEAD-PIN",
               "SPEC-VERBATIM", "PLAN==LEANS")
N_VERIFIER_PLANTS_T = 15
BUILT_LINE_T = ("BUILT: exchange/reports/BUILD_2026-10-08_TIERC12_VALUE_AREA.md · tierc12( commits "
                "first..last (n) · fixture roll GREEN\n")
FLIP_AT_T = 100                              # the prefix byte the contract plant flips
RATIFIED_LINES_T = 4                         # the RATIFIED block ends on contract :4
# L-X.21: the two sets, typed HERE (paths relative to research_outputs/tierc12/ unless they begin scripts/)
PRE_REG_T = ("progress/**", "PROGRESS.json", ".gitignore", "scout/**", "x_rec/**", "leans_draft/**",
             "review/**", "LEANS.md", "LEANS_AMENDMENTS.md", "AMENDMENTS_PROPOSED.md",
             "ORCHESTRATOR_RULINGS.md", "DISCLOSURES.md")
PRE_REG_RECORDS_T = ("STEP_Q.json", "TC12-R0.json", "TC12-LEANS.json")
PRE_REG_SCRIPTS_T = ("scripts/tierc12_progress.py",)
REG_SET_T = ("REGISTRATION_PLAN.md",
             "registrations/REGISTRATIONS.json", "registrations/REGISTRY_PIN.json",
             "registrations/ATTEST_REG.json", "registrations/FIXTURES_REG.txt",
             "pins/CONTRACT_PIN_MAP.json", "pins/CONTRACT_PINS.json", "pins/PIN_REGISTER.json",
             "pins/CONTRACT_TOKENS_UNPINNED.json", "pins/FIXTURES_PINS.txt",
             "frozen/FROZEN_ESTATE.json", "resume/FIXTURES_RESUME_TC12-REG.txt",
             "closure/FIXTURES_CLOSURE_TC12-REG.txt", "progress/TC12-REG.json",
             "scripts/tierc12_fx.py", "scripts/tierc12_units.py", "scripts/tierc12_pins.py",
             "scripts/tierc12_frozen.py", "scripts/tierc12_registrations.py",
             "scripts/tierc12_registrations_fixtures.py", "scripts/tierc12_pins_fixtures.py",
             "scripts/tierc12_resume_fixtures.py", "scripts/tierc12_closure_fixtures.py")
ATTEST_SELF_T = "registrations/ATTEST_REG.json"
# written or rewritten AFTER the attested instant by the gate itself (the stage's transcripts and record,
# and the two files the TC12-REG commit modifies): outside the listing's equality, inside the set law
LATER_T = ("registrations/FIXTURES_REG.txt", "pins/FIXTURES_PINS.txt",
           "resume/FIXTURES_RESUME_TC12-REG.txt", "closure/FIXTURES_CLOSURE_TC12-REG.txt",
           "progress/TC12-REG.json", "PROGRESS.json", "scripts/tierc12_progress.py")
# the listed texts that only GROW after the attested instant (append-only: L-0.5, O-35): held to a
# byte-prefix at the listed sha, never to the whole file
APPEND_ONLY_T = ("LEANS_AMENDMENTS.md", "AMENDMENTS_PROPOSED.md")
X_REC_T = "x_rec/"                           # git-ignored: on disk in the main tree only [CANON-26]
# the leaves of the filing that name a text which only grows after filing [L-X.16 "compared by nothing
# afterwards"; L-X.19 "a later amendment never edits the filing"], and the pin's sha of the file that
# carries them: a twin filed later differs from the filed pair there and nowhere else
GROWS_T = (("contract", "whole_file_sha256_at_filing"), ("amendments", "sha256"))
GROWS_PIN_T = "registrations_file"
SHOWN_T = 12                                 # unnamed paths shown on stdout (never in the transcript)
AM_FIRST_T = "## AM-1 · "                    # L-X.19: the amendments file "holds AM-1 at filing"
# AM-67 (ruling on AP-66): the commit that first adds this path is the registry commit — the filing
# instant on record; a listed path it TRACKS is held to its blob there, never to the working file
REG_FILE_REL_T = T12_REL + "/registrations/REGISTRATIONS.json"
GIT_RO_T = ("log", "cat-file")               # the read-only verbs asked of a tree [L-X.21 clause 3]
COMMIT_RX_T = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")
SCRATCH_GIT_T = (("init", "-q"), ("add", "-A"),
                 ("commit", "-q", "--no-verify", "-m", "scratch: the registry commit"))
SCRATCH_DATE_T = "2026-10-08T00:00:00+0000"  # a scratch repository's one commit: a typed date, never a clock

_TMP: list = []
_N = [0]
_CTX: dict = {}


# ═══════════════════════════════════════════════ SMALL TOOLS
def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def scratch_dir() -> Path:
    _N[0] += 1
    d = Path(_TMP[0]) / f"s{_N[0]}"
    d.mkdir(parents=True)
    return d


def grown_from(raw: bytes, want: str):
    """The byte-prefix of `raw` whose sha256 is `want` — a text that only grows, as it stood when
    `want` was taken.  None when no byte-prefix of `raw` hashes to it (the text was edited, not
    appended to)."""
    h = hashlib.sha256()
    for i in range(len(raw) + 1):
        if h.hexdigest() == want:
            return raw[:i]
        h.update(raw[i:i + 1])
    return None


def swap(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"the plant's anchor {old[:60]!r} stands {text.count(old)} times")
    return text.replace(old, new)


def ctx() -> dict:
    """The filed pair and the bytes the verifier is handed, read once per run."""
    if not _CTX:
        doc, pin, reg_bytes = REG.filed(ROOT)
        _CTX.update(doc=doc, pin=pin, reg_bytes=reg_bytes, inputs=REG.Filing().inputs(doc))
    return _CTX


def copy_of(doc: dict) -> dict:
    return json.loads(json.dumps(doc))                      # key order kept


def body_of(doc: dict, rid: str) -> dict:
    return next(r for r in doc["registrations"] if r["registration"] == rid)


def bent(fn) -> dict:
    """A copy of the filed document with one bend applied."""
    doc = copy_of(ctx()["doc"])
    fn(doc)
    return doc


def verify(doc=None, pin=None, door=None, **over) -> list:
    """Production's verifier on the filed pair, with any input replaced by a bent copy."""
    c = ctx()
    kw = {**c["inputs"], **over}
    return REG.verify_filing(doc if doc is not None else c["doc"], pin if pin is not None else c["pin"],
                             reg_bytes=c["reg_bytes"], door=door, **kw)


def plan_text() -> str:
    return ctx()["inputs"]["plan_bytes"].decode("utf-8")


def plan_bent(old: str, new: str) -> list:
    """Production's verifier handed a scratch plan with ONE anchor rewritten."""
    return verify(plan_bytes=swap(plan_text(), old, new).encode("utf-8"))


def prefix_text() -> str:
    return "\n".join(PINS.Door().prefix()["lines"])


def contract_door(edit, refile=False) -> tuple:
    """(door, contract bytes): a pin door over a scratch contract with a scratch STEP Q record of
    its own bytes and sha, and a scratch copy of pins/ (re-derived when `refile`), so the plant
    reaches the law it names and not the prefix pin."""
    d = scratch_dir()
    (d / "pins").mkdir()
    for name in (PINS.MAP_NAME, PINS.PINS_NAME, PINS.REGISTER_NAME, PINS.UNPINNED_NAME):
        shutil.copyfile(T12 / "pins" / name, d / "pins" / name)
    raw = edit(prefix_text()).encode("utf-8")
    (d / "contract.md").write_bytes(raw)
    (d / "STEP_Q.json").write_text(json.dumps({"artifact_shas": {PINS.CONTRACT_REL: {
        "bytes": len(raw), "sha256": sha(raw)}}}), encoding="utf-8")
    door = PINS.Door(root=ROOT, contract=d / "contract.md", step_q=d / "STEP_Q.json",
                     pins_dir=d / "pins", main=MAIN)
    if refile:
        door.file(refile=True)
    return door, raw


def line_swap(n: int, old: str, new: str):
    def edit(text: str) -> str:
        lines = text.split("\n")
        lines[n - 1] = swap(lines[n - 1], old, new)
        return "\n".join(lines)
    return edit


def judged(real_leg):
    """A HALT inside a REAL leg is that leg's FAIL, with the HALT's own text."""
    def leg():
        try:
            return real_leg()
        except SystemExit as e:
            return False, f"production HALTed — {e}"
    return leg


def verdict(found: list, why: str) -> tuple:
    return (not found), (why if not found else f"{len(found)} finding(s): " + " | ".join(found))


def named(found: list, detectors) -> list:
    return [x for x in found if x.split(" ", 1)[0] in detectors]


# ═══════════════════════════════════════════════ THE INDEPENDENT RE-DERIVATION (this file's own)
def own_prefix() -> list:
    """The prefix lines, cut by this file: N and the sha from STEP_Q.json, held to the typed pair."""
    rec = json.loads((T12 / "progress" / "STEP_Q.json").read_text(encoding="utf-8"))["artifact_shas"][CONTRACT_T]
    raw = (ROOT / CONTRACT_T).read_bytes()
    if (rec["bytes"], rec["sha256"]) != (PREFIX_BYTES_T, PREFIX_SHA_T) or sha(raw[:PREFIX_BYTES_T]) != PREFIX_SHA_T:
        raise ValueError("the contract's prefix is not the typed STEP Q bytes")
    return raw[:PREFIX_BYTES_T].decode("utf-8").split("\n")


def own_cut(lines: list, a: int, b: int) -> str:
    return "\n".join(lines[a - 1:b])


def own_payload_sha(body: dict) -> str:
    b = dict(body)
    b.pop("text_sha256", None)
    b.pop("sha256", None)
    return sha(json.dumps(b, sort_keys=True, ensure_ascii=False).encode("utf-8"))


def own_chain(regs: list) -> tuple:
    prev, out = GENESIS_T, []
    for r in regs:
        line = {"prev": prev, "registration": r["registration"], "seq": r["seq"], "sha256": r["sha256"]}
        prev = sha(json.dumps(line, sort_keys=True).encode())
        out.append({**line, "line_sha256": prev})
    return out, prev


def slice_referee(doc: dict) -> list:
    """REFEREE-SLICE: every text, context and external slice of the filing against this file's own
    cut of the typed line ranges and the typed shas."""
    lines, out = own_prefix(), []
    if [r.get("registration") for r in doc["registrations"]] != list(IDS_T):
        return [f"REFEREE-SLICE the filing holds {[r.get('registration') for r in doc['registrations']]}"]
    for r in doc["registrations"]:
        rid = r["registration"]
        a, b, want = TEXT_T[rid]
        text = own_cut(lines, a, b)
        if (r["text_lines"], r["text_of_record"], r["text_sha256"]) != ([a, b], text, want) \
                or sha(text.encode("utf-8")) != want:
            out.append(f"REFEREE-SLICE {rid}: text_of_record is not contract :{a}-{b} at the typed sha")
        need = [LAWS_T, HEADERS_T[FAMILY_T[rid][0]]]
        got = [(c["lines"][0], c["lines"][1], sha(c["text"].encode("utf-8"))) for c in r["context_of_record"]]
        if got != need or any(c["text"] != own_cut(lines, *c["lines"]) for c in r["context_of_record"]):
            out.append(f"REFEREE-SLICE {rid}: context_of_record is not LAWS and its family header")
        ext = []
        for path, file_sha, a, b in EXTERNAL_T.get(rid, ()):
            raw = (MAIN / path).read_bytes()
            if sha(raw) != file_sha:
                out.append(f"REFEREE-SLICE {rid}: {path} is not at the typed sha")
            ext.append({"path": path, "sha256": file_sha, "lines": [a, b],
                        "text": own_cut(raw.decode("utf-8").split("\n"), a, b)})
        if r.get("external_context", []) != ext:
            out.append(f"REFEREE-SLICE {rid}: external_context is not the typed external slices")
    return out


def map_referee(plan_bytes: bytes) -> list:
    """REFEREE-MAP: every row of the plan's line map re-cut by this file hashes to the row's sha."""
    lines, out, n = own_prefix(), [], 0
    rx = re.compile(r"\| (.+?) \| (\d+)(?:-(\d+))? \| `([0-9a-f]{64})` \|")
    for ln in plan_bytes.decode("utf-8").split("\n"):
        m = rx.fullmatch(ln)
        if m:
            n += 1
            a, b = int(m.group(2)), int(m.group(3) or m.group(2))
            if sha(own_cut(lines, a, b).encode("utf-8")) != m.group(4):
                out.append(f"REFEREE-MAP the plan's row {m.group(1)!r} (:{a}-{b}) does not re-cut to its sha")
    if n != N_MAP_ROWS_T:
        out.append(f"REFEREE-MAP the plan's line map holds {n} rows, not {N_MAP_ROWS_T}")
    return out


def hash_referee(doc: dict, pin: dict, reg_bytes: bytes) -> list:
    """REFEREE-HASH: payload shas, the chain from the typed genesis string, the head, the pin, the
    rendering and the key order — re-derived here."""
    out = []
    for r in doc["registrations"]:
        if r["sha256"] != own_payload_sha(r) or r["text_sha256"] != sha(r["text_of_record"].encode("utf-8")):
            out.append(f"REFEREE-HASH {r['registration']}: a sha of the body does not re-derive")
        keys = tuple(k for k in BODY_KEYS_T if k != "external_context" or r["registration"] in EXTERNAL_T)
        if tuple(r) != keys or tuple(r["operative_spec"]) != SPEC_KEYS_T:
            out.append(f"REFEREE-HASH {r['registration']}: the body's keys are not L-X.19's, in order")
    chain, head = own_chain(doc["registrations"])
    if doc["chain"] != chain or doc["head"] != head or [r["seq"] for r in doc["registrations"]] \
            != list(range(1, len(IDS_T) + 1)):
        out.append("REFEREE-HASH the chain does not re-derive from the genesis string")
    if (pin["head"], pin["genesis"], pin["chain"], pin["order_of_filing"], pin["registry_len"]) != (
            head, GENESIS_T, [c["line_sha256"] for c in chain], list(IDS_T), len(IDS_T)):
        out.append("REFEREE-HASH REGISTRY_PIN.json's head, genesis, chain or order is not the re-derived one")
    if pin["registrations_file"] != {"path": T12_REL + "/registrations/REGISTRATIONS.json",
                                     "bytes": len(reg_bytes), "sha256": sha(reg_bytes)}:
        out.append("REFEREE-HASH REGISTRY_PIN.json's registrations_file is not the filing's bytes")
    if tuple(doc) != TOP_KEYS_T or tuple(sorted(pin)) != PIN_KEYS_T:
        out.append(f"REFEREE-HASH the top keys {list(doc)} or the pin's keys are not the typed lists")
    if reg_bytes != (json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8"):
        out.append("REFEREE-HASH REGISTRATIONS.json is not its own document rendered by L-X.19's law")
    text = reg_bytes.decode("utf-8")
    if "/Users/" in text or "/private/" in text or re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", text):
        out.append("REFEREE-HASH a leaf of the filing carries an absolute path or a clock")
    return out


def pins_referee(doc: dict, pin: dict) -> list:
    """REFEREE-PINS: the texts pinned by a sha read from the file, and the filed statistics, against
    the files and the typed referees.  `amendments` names LEANS_AMENDMENTS.md AS IT STOOD AT FILING
    [L-X.19]: the file only grows, so the pinned sha is held to a byte-prefix of the file on disk,
    and that prefix holds AM-1."""
    out = []
    lines = own_prefix()
    if doc["contract"] != {"path": CONTRACT_T, "prefix_bytes": PREFIX_BYTES_T, "prefix_sha256": PREFIX_SHA_T,
                           "n_lines": N_LINES_T,
                           "whole_file_sha256_at_filing": doc["contract"].get("whole_file_sha256_at_filing")} \
            or len(lines) - 1 != N_LINES_T:
        out.append("REFEREE-PINS the `contract` leaf is not the typed prefix pin")
    for key, path in PINNED_T.items():
        raw = (ROOT / path).read_bytes()
        filed_sha = doc[key].get("sha256")
        if doc[key] != {"path": path, "sha256": filed_sha} or pin[key] != doc[key]:
            out.append(f"REFEREE-PINS `{key}` is not {{path: {path}, sha256}}, the same in the filing and the pin")
        elif (key, "sha256") in GROWS_T:
            at_filing = grown_from(raw, filed_sha)
            if at_filing is None or AM_FIRST_T.encode("utf-8") not in at_filing:
                out.append(f"REFEREE-PINS `{key}` is not {path} as it stood at filing: no byte-prefix of the "
                           f"file on disk that holds `{AM_FIRST_T}` hashes to the filed sha")
        elif filed_sha != sha(raw):
            out.append(f"REFEREE-PINS `{key}` is not {path} at the sha of the file on disk")
    s = doc["statistics"]
    if (s["n_boot"], s["seed"], s["seed_sens"], doc["scored_window"]["end_ms"], doc["era_cut"]["ms"]) != (
            N_BOOT_T, SEED_T, SEED_SENS_T, SCORED_END_MS_T, ERA_CUT_MS_T) \
            or (pin["n_boot"], pin["seed"], pin["seed_sens"]) != (N_BOOT_T, SEED_T, SEED_SENS_T) \
            or any(r["seed"] != SEED_T for r in doc["registrations"]):
        out.append("REFEREE-PINS n_boot, a seed, the scored window's end or the era cut is not the typed value")
    return out


def law_referee(doc: dict) -> list:
    """REFEREE-LAW: the filed `law` is TC11's BY OBJECT, its file named by TC11's chain head (typed
    here, re-derived from TC11's payloads) and by no whole-file sha."""
    raw = (MAIN / T11_REG_T).read_bytes()
    t11 = json.loads(raw.decode("utf-8"))
    out = []
    if own_chain(t11["registrations"])[1] != T11_HEAD_T or any(r["sha256"] != own_payload_sha(r)
                                                               for r in t11["registrations"]):
        out.append("REFEREE-LAW TC11's registry does not re-derive to the typed chain head")
    if doc.get("law") != t11["law"]:
        out.append("REFEREE-LAW the filed `law` is not TC11's REGISTRATIONS.json[\"law\"] by object")
    src = doc.get("law_source") or {}
    if (src.get("path"), src.get("key"), src.get("head")) != (T11_REG_T, "law", T11_HEAD_T):
        out.append("REFEREE-LAW `law_source` does not name TC11's file, key and chain head")
    if sha(raw) in json.dumps(src) or "sha256" in json.dumps(src):
        out.append("REFEREE-LAW `law_source` carries a whole-file sha of a file the tc11-stamp moves")
    return out


def family_referee(doc: dict) -> list:
    """REFEREE-FAMILY: the three families re-parsed by this file's own two expressions."""
    lines, out = own_prefix(), []
    heads = [(i + 1, m) for i, m in ((i, R_FAM_T.match(ln)) for i, ln in enumerate(lines)) if m]
    qs = [m.group(1) for m in (R_Q_T.search(ln) for ln in lines) if m]
    if qs != [Q_T]:
        return [f"REFEREE-FAMILY the prefix states q {qs}, not one {Q_T}"]
    parsed = {}
    for line_no, m in heads:
        bar = Fraction(Decimal(m.group(4)))
        if bar != Fraction(Decimal(Q_T)) / int(m.group(3)):
            out.append(f"REFEREE-FAMILY {m.group(2)}: the header's bar is not q ÷ m")
        parsed[m.group(2)] = (m.group(1), line_no, int(m.group(3)), m.group(4),
                              f"{bar.numerator}/{bar.denominator}")
    filed = {f["family"]: (f["stage"], f["header_line"], f["m"], f["bar"], f["bar_exact"])
             for f in doc["families"]}
    if filed != parsed or any(f["q"] != Q_T or f["header_text"] != lines[f["header_line"] - 1]
                              for f in doc["families"]):
        out.append(f"REFEREE-FAMILY the filed families {filed} are not this file's parse {parsed}")
    for r in doc["registrations"]:
        fam, stage, m, bar, bar_exact, prior = FAMILY_T[r["registration"]]
        if (r["family"], r["family_m"], r["family_bar"], r["prior_pct"]) != (fam, m, bar, prior) \
                or parsed.get(fam, ())[:1] != (stage,) or parsed.get(fam, ())[2:] != (m, bar, bar_exact):
            out.append(f"REFEREE-FAMILY {r['registration']}: family, m, bar or prior is not the typed row")
    if sum(1 for f in doc["families"] for _ in range(f["n_registrations"])) != len(IDS_T):
        out.append("REFEREE-FAMILY the families' n_registrations do not sum to the five rows")
    return out


def own_label(x: str) -> tuple:
    """(key, tag, label, text, items) by plain splits — this file's reading of L-X.18 point 4."""
    key, rest = x.split(" — tag: ", 1)
    tag, rest = rest.split("; label: ", 1)
    label, rest = rest.split('; text: "', 1)
    text, items = rest.split('"; items: ', 1)
    return key.strip("`"), tag, label, text, items


def own_template(rule: str) -> list:
    return [p.split("'", 1)[0] for p in rule.split("prints '")[1:] if p.startswith("<verdict>")]


def template_referee(doc: dict) -> list:
    """REFEREE-TEMPLATE: template, label key, tag and label BY REGISTRATION ID against the typed
    table; "re-score" in P-ADM-1's template and label alone (scoped to templates and labels)."""
    out = []
    for r in doc["registrations"]:
        rid = r["registration"]
        key, tag, label, template = TEMPLATES_T[rid]
        labels = [own_label(x)[:3] for x in r["operative_spec"]["labels"]]
        if own_template(r["verdict_rule"]) != [template] or labels != [(key, tag, label)]:
            out.append(f"REFEREE-TEMPLATE {rid}: the rule's template or the label is not the typed row")
        for field in own_template(r["verdict_rule"]) + [x[2] for x in labels]:
            if bool(RESCORE_RX_T.search(field)) != (rid in RESCORE_IDS_T):
                out.append(f"REFEREE-TEMPLATE {rid}: \"re-score\" stands (or is missing) in a template or label")
    return out


def own_precondition(x: str) -> bool:
    if not x.startswith("{record: ") or "}" not in x:
        return False
    inner, tail = x[1:].split("}", 1)
    parts = re.split(r", (?=certified_by: |selector: |required: )", inner)
    req = parts[3][len("required: "):] if len(parts) == 4 and parts[3].startswith("required: ") else ""
    return (len(parts) == 4 and parts[0].startswith("record: ") and parts[1].startswith("certified_by: ")
            and len(parts[1].split(" ")) == 3 and parts[2].startswith("selector: ")
            and (req == "true" or re.fullmatch(r'(contains )?"[^"]*"', req) is not None)
            and (tail == "" or tail.startswith(" — ")))


def grammar_referee(doc: dict) -> list:
    """REFEREE-GRAMMAR: L-X.18's field grammar and AP-1's ruler sentence on the filed payloads."""
    out = []
    for r in doc["registrations"]:
        rid, spec = r["registration"], r["operative_spec"]
        n_scored = sum(1 for x in spec["arms"] if x.startswith("`scored` "))
        pre = spec["preconditions"]
        n_pre = len(pre) if isinstance(pre, list) else 0
        if n_scored != 1 or not isinstance(spec["arms"], list) or not isinstance(spec["labels"], list):
            out.append(f"REFEREE-GRAMMAR {rid}: `arms` holds {n_scored} `scored` elements, or a list is not one")
        if n_pre != PRECOND_T[rid] or (isinstance(pre, list) and not all(own_precondition(x) for x in pre)) \
                or (isinstance(pre, str) and not (pre == "none" or pre.startswith("none — "))):
            out.append(f"REFEREE-GRAMMAR {rid}: `preconditions` is not {PRECOND_T[rid]} item(s) in the grammar")
        rule = " ".join(r["verdict_rule"].split())
        span = rule.split("Printed beside, deciding nothing:")
        if not rule.startswith(RULER_T) or len(span) != 2 or any(x not in span[1] for x in BESIDE_T):
            out.append(f"REFEREE-GRAMMAR {rid}: the ruler sentence or an item of the printed-beside list is missing")
        if not spec["comparison"].startswith(RULER_WORDS_T[rid]) or (
                RULER_WORDS_T[rid] not in r["text_of_record"]
                and RULER_WORDS_T[rid] not in r["context_of_record"][1]["text"]):
            out.append(f"REFEREE-GRAMMAR {rid}: the ruler `{RULER_WORDS_T[rid]}` is not named by the "
                       f"comparison and by the contract's text or family header")
        if any(str(n) not in rule for n in (N_BOOT_T, SEED_T, SEED_SENS_T)):
            out.append(f"REFEREE-GRAMMAR {rid}: the rule does not state N_BOOT and both seeds")
    return out


def own_blocks(text: str, heading) -> dict:
    """{id: lines} of the blocks under headings `heading(id)`, each up to the next `##` line."""
    lines, out = text.split("\n"), {}
    for rid in IDS_T:
        i = lines.index(heading(rid))
        j = next(k for k in range(i + 1, len(lines)) if lines[k].startswith("##"))
        out[rid] = lines[i + 1:j]
    return out


def own_fields(block: list) -> list:
    """[(field, tokens)] of a spec block: the words of each field, bullet marks dropped."""
    out = []
    for ln in block:
        if not ln.strip() or set(ln) == {"-"}:
            continue
        if ln.startswith("- **"):
            name, rest = ln[len("- **"):].split(":**", 1)
            out.append((name, rest.split()))
        else:
            s = ln.strip()
            out[-1][1].extend((s[len("- "):] if ln.startswith("  - ") else s).split())
    return out


def filed_tokens(v) -> list:
    if isinstance(v, str):
        return v.split()
    if isinstance(v, list):
        return [t for x in v for t in x.split()]
    return v["text"].split() + [t for x in v["items"] for t in x.split()]


def spec_referee(doc: dict, plan_bytes: bytes, leans_bytes: bytes) -> list:
    """REFEREE-SPEC: the plan's five blocks are the frozen LEANS's, line for line; and every filed
    leaf holds exactly the WORDS of its field, in order (a word-level oracle of the carry law)."""
    plan = own_blocks(plan_bytes.decode("utf-8"),
                      lambda rid: f"### 1.{IDS_T.index(rid) + 1} {rid}")
    leans = own_blocks(leans_bytes.decode("utf-8"), lambda rid: f"### REGISTRATION SPEC · {rid}")
    out = []
    for r in doc["registrations"]:
        rid = r["registration"]
        if plan[rid] != leans[rid]:
            out.append(f"REFEREE-SPEC {rid}: the plan's block is not the frozen block, line for line")
        fields = own_fields(leans[rid])
        if tuple(n for n, _ in fields) != FIELDS_T:
            out.append(f"REFEREE-SPEC {rid}: the frozen block's fields are not the fifteen, in order")
            continue
        checked = {"id": r["registration"], "family": r["family"], "family_m": str(r["family_m"]),
                   "family_bar": r["family_bar"], "prior": str(r["prior_pct"])}
        for name, tokens in fields:
            if name in CHECKED_T:
                same = tokens[:1] == [checked[name]]
            elif name == "verdict_rule":
                same = tokens == r["verdict_rule"].split()
            else:
                same = tokens == filed_tokens(r["operative_spec"][name])
            if not same:
                out.append(f"REFEREE-SPEC {rid}: the filed `{name}` does not hold the words of its field")
    return out


def referee(doc: dict, pin: dict, reg_bytes: bytes, plan_bytes: bytes, leans_bytes: bytes) -> list:
    """The whole independent re-derivation; [] iff this file agrees with the filing."""
    return (slice_referee(doc) + map_referee(plan_bytes) + hash_referee(doc, pin, reg_bytes)
            + pins_referee(doc, pin) + law_referee(doc) + family_referee(doc) + template_referee(doc)
            + grammar_referee(doc) + spec_referee(doc, plan_bytes, leans_bytes))


# ═══════════════════════════════════════════════ F-CONTRACT-PIN [L-X.16, L-X.35]
def stamped_door() -> tuple:
    """(door, bytes): the contract with a `BUILT:` line of L-X.35's form appended as its last line,
    under the REAL STEP Q record."""
    d = scratch_dir()
    raw = (ROOT / CONTRACT_T).read_bytes() + BUILT_LINE_T.encode("utf-8")
    (d / "contract.md").write_bytes(raw)
    return PINS.Door(root=ROOT, contract=d / "contract.md", main=MAIN), raw


def progress_bytes(contract_bytes: bytes) -> bytes:
    """PROGRESS.json re-derived by the merge of record over a scratch tree holding `contract_bytes`."""
    d = scratch_dir()
    (d / T12_REL / "progress").mkdir(parents=True)
    (d / "exchange" / "queue").mkdir(parents=True)
    (d / CONTRACT_T).write_bytes(contract_bytes)
    for p in sorted((T12 / "progress").glob("*.json")):
        shutil.copyfile(p, d / T12_REL / "progress" / p.name)
    for rel in ("ORCHESTRATOR_RULINGS.md", "LEANS_AMENDMENTS.md", "registrations/REGISTRY_PIN.json"):
        (d / T12_REL / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(T12 / rel, d / T12_REL / rel)
    return PROGRESS.render(PROGRESS.merge(d)).encode("utf-8")


def contract_pin_break():
    raw = ctx()["inputs"]["contract_bytes"]
    flipped = raw[:FLIP_AT_T] + bytes([raw[FLIP_AT_T] ^ 1]) + raw[FLIP_AT_T + 1:]
    lines = raw.decode("utf-8").split("\n")
    inserted = "\n".join(lines[:RATIFIED_LINES_T] + ["BUILT: x"] + lines[RATIFIED_LINES_T:]).encode("utf-8")
    return FX.plants([
        ("one byte flipped inside the prefix", "CONTRACT-PREFIX",
         lambda: verify(contract_bytes=flipped)),
        ("the `BUILT:` line inserted under RATIFIED", "CONTRACT-PREFIX",
         lambda: verify(contract_bytes=inserted)),
        ("a tail line `NOTE: x`", "CONTRACT-TAIL",
         lambda: verify(contract_bytes=raw + b"NOTE: x\n")),
        ("a `BUILT:` tail line with no final newline", "CONTRACT-TAIL",
         lambda: verify(contract_bytes=raw + BUILT_LINE_T.encode("utf-8").rstrip(b"\n"))),
    ])


def contract_pin_real():
    c = ctx()
    door, raw = stamped_door()
    found = verify(contract_bytes=raw)
    rebuilt = REG.Filing(door=door).build()
    doc = c["doc"]
    same = ("registrations", "chain", "head", "families")
    found += [f"PIN-MOVED `{k}` of a filing re-built on the stamped contract differs from the filed one"
              for k in same if rebuilt[k] != doc[k]]
    moved = [k for k in ("path", "prefix_bytes", "prefix_sha256", "n_lines")
             if rebuilt["contract"][k] != doc["contract"][k]]
    if moved or rebuilt["contract"]["whole_file_sha256_at_filing"] != sha(raw):
        found.append(f"PIN-MOVED the stamped filing's `contract` leaf moved {moved}")
    if progress_bytes(raw) != progress_bytes(c["inputs"]["contract_bytes"]):
        found.append("PIN-MOVED a byte of the re-derived PROGRESS.json moved under the stamp")
    return verdict(found, f"prefix {PREFIX_BYTES_T} B, sha {PREFIX_SHA_T}, {N_LINES_T} lines == the typed STEP Q "
                          f"pair; a `BUILT:` line of L-X.35's form appended as the last line moves no slice, no "
                          f"payload sha, no chain line, the head {doc['head']} and no verifier finding (0), and "
                          f"no byte of a PROGRESS.json re-derived by the merge of record; only the leaf "
                          f"whole_file_sha256_at_filing differs, which nothing compares")


# ═══════════════════════════════════════════════ F-REG [SLICE] [L-X.17]
def slice_break():
    score_rel = "scripts/tierc11_score.py"
    score = (MAIN / score_rel).read_bytes()

    def external_from_a_moved_script():
        def bend(doc):
            body_of(doc, "P-ADM-1")["external_context"].append(
                {"path": score_rel, "sha256": sha(score), "lines": [1, 1],
                 "text": score.decode("utf-8").split("\n")[0]})
        return verify(doc=bent(bend), ext_bytes={**ctx()["inputs"]["ext_bytes"], score_rel: score})

    def text_edit(doc):
        b = body_of(doc, "P-BRD-1")
        b["text_of_record"] = swap(b["text_of_record"], "breadth < 2/5", "breadth < 3/5")

    def context_bend(doc):
        body_of(doc, "P-DIR-1")["context_of_record"][0]["lines"] = [LAWS_T[0], LAWS_T[1] - 1]

    def external_text(doc):
        e = body_of(doc, "P-BRD-1")["external_context"][0]
        e["text"] = e["text"].replace("UNRESOLVED", "RESOLVED", 1)

    return FX.plants([
        ("one character edited in a filed text_of_record (P-BRD-1: 2/5 -> 3/5)", "TEXT-SLICE P-BRD-1",
         lambda: verify(doc=bent(text_edit))),
        ("an external_context item cut from scripts/tierc11_score.py", "EXTERNAL-SLICE P-ADM-1",
         external_from_a_moved_script),
        ("a context range bent (P-DIR-1: the LAWS slice one row short)", "CONTEXT-SLICE P-DIR-1",
         lambda: verify(doc=bent(context_bend))),
        ("one word edited in a filed external slice (P-BRD-1, X4.md:16)", "EXTERNAL-SLICE P-BRD-1",
         lambda: verify(doc=bent(external_text))),
        ("an external file handed with one byte changed (STAGE_G.md)", "EXTERNAL-SLICE P-ADM-1",
         lambda: verify(ext_bytes={k: (v + b" " if k == EXTERNAL_T["P-ADM-1"][0][0] else v)
                                   for k, v in ctx()["inputs"]["ext_bytes"].items()})),
    ])


def slice_real():
    c = ctx()
    found = named(verify(), ("TEXT-SLICE", "CONTEXT-SLICE", "EXTERNAL-SLICE", "CONTRACT-PREFIX",
                             "CONTRACT-TAIL"))
    found += slice_referee(c["doc"]) + map_referee(c["inputs"]["plan_bytes"])
    n_ext = sum(len(v) for v in EXTERNAL_T.values())
    return verdict(found, " · ".join(f"{rid} :{TEXT_T[rid][0]}-{TEXT_T[rid][1]} {TEXT_T[rid][2]}" for rid in IDS_T)
                   + f" — each re-cut here from the pinned prefix by \"\\n\".join(lines[a-1:b]); every "
                     f"registration's context = LAWS :{LAWS_T[0]}-{LAWS_T[1]} and its family header; "
                     f"{n_ext} external slices re-cut from files at their typed shas; all {N_MAP_ROWS_T} rows "
                     f"of the plan's line map re-cut to their shas")


# ═══════════════════════════════════════════════ F-REG [HASH] [L-X.19]
def hash_break():
    def prev_bent(doc):
        doc["chain"][2]["prev"] = GENESIS_T

    def m_changed(doc):
        body_of(doc, "P-SCALP-3")["family_m"] = 2

    def order_swapped(doc):
        regs = doc["registrations"]
        regs[0], regs[1] = regs[1], regs[0]

    def law_edited(doc):
        doc["law"] = doc["law"].replace("sort_keys, ", "")

    def law_by_file_sha(doc):
        doc["law_source"]["sha256"] = sha((MAIN / T11_REG_T).read_bytes())

    return FX.plants([
        ("one `prev` bent (the third chain entry -> the genesis string)", "CHAIN",
         lambda: verify(doc=bent(prev_bent))),
        ("`family_m` of one body changed (P-SCALP-3: 1 -> 2)", "PAYLOAD-SHA P-SCALP-3",
         lambda: verify(doc=bent(m_changed))),
        ("a registration's order swapped (P-BRD-1 before P-ADM-1)", "CHAIN",
         lambda: verify(doc=bent(order_swapped))),
        ("the filed `law` edited by two words", "REFEREE-LAW", lambda: law_referee(bent(law_edited))),
        ("`law_source` carrying the whole-file sha of TC11's REGISTRATIONS.json", "REFEREE-LAW",
         lambda: law_referee(bent(law_by_file_sha))),
    ])


def hash_real():
    c = ctx()
    doc = c["doc"]
    found = named(verify(), ("PAYLOAD-SHA", "CHAIN", "HEAD-PIN", "SEED"))
    found += hash_referee(doc, c["pin"], c["reg_bytes"]) + pins_referee(doc, c["pin"]) + law_referee(doc)
    return verdict(found, " · ".join(f"{r['registration']} {r['sha256']}" for r in doc["registrations"])
                   + f" — each payload sha re-derived here over sorted-keys JSON without the two shas; the "
                     f"chain re-derived from the genesis string ({len(GENESIS_T)} zeros); head {doc['head']} == "
                     f"REGISTRY_PIN.json's; REGISTRATIONS.json sha {sha(c['reg_bytes'])} ({len(c['reg_bytes'])} "
                     f"B) == the pin's registrations_file; n_boot {N_BOOT_T}, seed {SEED_T}, sensitivity seed "
                     f"{SEED_SENS_T}, scored window end {SCORED_END_MS_T}, era cut {ERA_CUT_MS_T} == typed; "
                     f"`law` is TC11's by object under its chain head {T11_HEAD_T}, no whole-file sha")


# ═══════════════════════════════════════════════ F-REG [WRITE-ONCE] [L-X.20]
def shadow_filer():
    """A SHADOW COPY of the filer whose exclusive create is a plain write — the planted mutation."""
    src = swap((ROOT / "scripts" / "tierc12_registrations.py").read_text(encoding="utf-8"),
               'with open(path, "xb") as f:', 'with open(path, "wb") as f:')
    p = Path(_TMP[0]) / "shadow_tierc12_registrations.py"
    p.write_text(src, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("shadow_tierc12_registrations", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_once_findings(mod, out_dir: Path, file_first: bool, probe_create: bool) -> list:
    """WRITE-ONCE: a second filing into `out_dir` returns instead of HALTing, a create() on a file
    that exists succeeds, or either changes a byte.  `probe_create` is given in SCRATCH directories
    only: no leg ever calls create() on a file of record."""
    f = mod.Filing(out_dir=out_dir)
    out = []
    if file_first:
        f.file()
    paths = [out_dir / mod.REG_NAME, out_dir / mod.PIN_NAME]
    if not all(p.is_file() for p in paths):
        return [f"WRITE-ONCE {out_dir.name}/ does not hold both files of the filing"]
    before = [p.read_bytes() for p in paths]
    try:
        f.file()
        out.append("WRITE-ONCE a second filing returned instead of HALTing")
    except SystemExit as e:
        if "HALT WRITE-ONCE" not in str(e):
            out.append(f"WRITE-ONCE a second filing stopped for another reason — {e}")
    for p in paths if probe_create else ():
        try:
            mod.create(p, b"overwritten")
            out.append(f"WRITE-ONCE create() wrote over {p.name}, which was on file — not an exclusive create")
        except FileExistsError:
            pass
    if [p.read_bytes() for p in paths] != before:
        out.append("WRITE-ONCE a second filing or a second create changed a byte of the filing")
    return out


def settled(twin: dict, filed: dict, also=()) -> dict:
    """`twin` with the leaves of GROWS_T (and the top keys `also`) set to the filed values."""
    d = copy_of(twin)
    for key, leaf in GROWS_T:
        d[key][leaf] = filed[key][leaf]
    for key in also:
        d[key] = filed[key]
    return d


def twin_findings(twin_doc: dict, twin_pin: dict) -> list:
    """WRITE-ONCE (the twin): a filing made NOW from the texts on disk is the filed pair byte for
    byte outside the leaves that name a text which only grows after filing — the contract's
    whole-file sha (a `BUILT:` tail [L-X.16]) and the amendments file's sha (a later amendment
    [L-X.19]) — and the pin's sha of the file that carries them; and those leaves of the twin are
    the shas of the texts as they stand."""
    c = ctx()
    out = []
    same_doc = json.dumps(settled(twin_doc, c["doc"]), indent=2, ensure_ascii=False) + "\n"
    same_pin = json.dumps(settled(twin_pin, c["pin"], (GROWS_PIN_T,)), indent=2, sort_keys=True,
                          ensure_ascii=False) + "\n"
    if same_doc.encode("utf-8") != c["reg_bytes"] \
            or same_pin.encode("utf-8") != (T12 / "registrations" / REG.PIN_NAME).read_bytes():
        out.append("WRITE-ONCE a scratch twin filed from the texts on disk differs from the filed pair outside "
                   "the leaves that name a text which only grows after filing")
    now = {"contract": sha((ROOT / CONTRACT_T).read_bytes()),
           "amendments": sha((ROOT / PINNED_T["amendments"]).read_bytes())}
    if any(d[key][leaf] != now[key] for d in (twin_doc, twin_pin) for key, leaf in GROWS_T):
        out.append("WRITE-ONCE a growing leaf of the scratch twin is not the sha of its text as it stands on disk")
    return out


def write_once_break():
    return FX.plants([
        ("`\"xb\"` replaced by `\"wb\"` in a scratch copy of the filer", "WRITE-ONCE create() wrote over",
         lambda: write_once_findings(shadow_filer(), scratch_dir(), True, True)),
    ])


def write_once_real():
    c = ctx()
    found = write_once_findings(REG, T12 / "registrations", False, False)
    try:
        rc = REG.main(["--file"])
        found.append(f"WRITE-ONCE `--file` in the filed directory exited {rc}")
    except SystemExit as e:
        if "HALT WRITE-ONCE" not in str(e):
            found.append(f"WRITE-ONCE `--file` in the filed directory stopped for another reason — {e}")
    twin = scratch_dir()
    found += write_once_findings(REG, twin, True, True)
    found += twin_findings(json.loads((twin / REG.REG_NAME).read_text(encoding="utf-8")),
                           json.loads((twin / REG.PIN_NAME).read_text(encoding="utf-8")))
    if c["reg_bytes"] != (T12 / "registrations" / REG.REG_NAME).read_bytes():
        found.append("WRITE-ONCE the filed REGISTRATIONS.json changed during this run")
    grows = ", ".join(f"{k}.{leaf}" for k, leaf in GROWS_T)
    return verdict(found, f"in the filed directory a second filing HALTs WRITE-ONCE and `--file` does not exit 0; "
                          f"no byte of REGISTRATIONS.json ({sha(c['reg_bytes'])}) or REGISTRY_PIN.json moved; a "
                          f"scratch twin filed now from the texts on disk is the filed pair byte for byte once "
                          f"the leaves that name a text which only grows after filing ({grows} — in both files — "
                          f"and the pin's {GROWS_PIN_T}, the sha of the file that carries them) are set to the "
                          f"filed values, and those leaves of the twin are the shas of the texts on disk; its "
                          f"second filing HALTs too, and a create() on either of its files raises FileExistsError")


# ═══════════════════════════════════════════════ F-REG [TEMPLATE] [L-X.13, CANON-01]
def template_break():
    def none_left(doc):
        b = body_of(doc, "P-BRD-1")
        b["verdict_rule"] = swap(b["verdict_rule"], "The row prints '<verdict>", "The row prints '<the word>")

    def two(doc):
        b = body_of(doc, "P-BRD-1")
        b["verdict_rule"] += f" The row also prints '{_KIN_T}'."

    def label_of_another(doc):
        b = body_of(doc, "P-SCALP-3")
        b["operative_spec"]["labels"][0] = swap(b["operative_spec"]["labels"][0], "tag: KIN-SEEN;",
                                                "tag: direction-informed;")

    return FX.plants([
        ("P-ADM-1's template rewritten to the selection_hazard form (scratch plan)", "TEMPLATE P-ADM-1",
         lambda: plan_bent(f"'{_RESCORE_T}'", f"'{_HAZARD_T}'")),
        ("P-SFP-VA-1's template rewritten to the RE-SCORE form (scratch plan)", "TEMPLATE P-SFP-VA-1",
         lambda: plan_bent(f"prints '{_KIN_T}'", f"prints '{_RESCORE_T}'")),
        ("`DIRECTION-INFORMED` in capitals on P-DIR-1 (scratch plan)", "TEMPLATE P-DIR-1",
         lambda: plan_bent("carries selection_hazard only and prints '" + _HAZARD_T,
                           "carries selection_hazard only and prints '"
                           + _HAZARD_T.replace("direction-informed", "DIRECTION-INFORMED"))),
        ("a filed rule carrying no template (P-BRD-1)", "TEMPLATE P-BRD-1", lambda: verify(doc=bent(none_left))),
        ("a filed rule carrying two templates (P-BRD-1)", "TEMPLATE P-BRD-1", lambda: verify(doc=bent(two))),
        ("a filed label carrying another registration's tag (P-SCALP-3)", "TEMPLATE P-SCALP-3",
         lambda: verify(doc=bent(label_of_another))),
    ])


def template_real():
    c = ctx()
    found = named(verify(), ("TEMPLATE",)) + template_referee(c["doc"])
    table = REG.template_table(c["inputs"]["leans_bytes"].decode("utf-8").split("\n"))
    if {k: (v["key"], v["tag"], v["label"], v["template"]) for k, v in table.items()} != TEMPLATES_T:
        found.append("TEMPLATE-TABLE the table production reads from the frozen L-X.13 is not this file's typed table")
    return verdict(found, " · ".join(f"{rid} [{TEMPLATES_T[rid][0]} · {TEMPLATES_T[rid][1]} · "
                                     f"{TEMPLATES_T[rid][2]}] '{TEMPLATES_T[rid][3]}'" for rid in IDS_T)
                   + f" — each filed rule carries exactly one `prints '<verdict> …'` template and it is its "
                     f"registration's row of the typed table, byte for byte; \"re-score\" stands in "
                     f"{list(RESCORE_IDS_T)}'s template and label alone (the ban is scoped to templates and "
                     f"labels); the table read from the frozen L-X.13 == the typed table")


# ═══════════════════════════════════════════════ F-REG [SPEC-VERBATIM] [L-X.18]
PROSE_T = "  - the licence set of the mirror must hold the 4h taker pair"
ITEM_OLD_T = ('  - {record: research_outputs/tierc12/va/VA_MIRROR.json, certified_by: progress/TC12-V.json '
              'artifact_shas, selector: licence_set, required: contains "4h|taker"}')
_BAR_LINE_T = ('- **family_bar:** 0.05 — parsed from contract :64 ("bar 0.05"); asserted equal to q ÷ m '
               'with q = 0.10 parsed from :9.')
_PRIOR_LINE_T = '- **prior:** 45 — parsed from the text slice ("[45%]", contract :65).'
BAR_THEN_PRIOR_T = _BAR_LINE_T + "\n" + _PRIOR_LINE_T
PRIOR_THEN_BAR_T = _PRIOR_LINE_T + "\n" + _BAR_LINE_T
NUMERIC_AFTER_T = "it is this row's only precondition."
NUMERIC_ITEM_T = ("\n  - {record: research_outputs/tierc12/data/fee_schedule.json, certified_by: "
                  "progress/TC12-D.json artifact_shas, selector: maker_pin.edge_net_h20_at_pin, required: > 0}")


def spec_break():
    def leaf_edited(doc):
        b = body_of(doc, "P-ADM-1")
        b["operative_spec"]["mechanism"] = swap(b["operative_spec"]["mechanism"], "is LATE", "is EARLY")

    return FX.plants([
        ("one word changed in the `arms` field of P-DIR-1 (scratch plan)", "SPEC-VERBATIM P-DIR-1",
         lambda: plan_bent("`base` minus every campaign with `refuse == True`",
                           "`base` minus every trade with `refuse == True`")),
        ("`prior: 30%` (scratch plan, P-SCALP-3)", "SPEC-GRAMMAR P-SCALP-3",
         lambda: plan_bent("- **prior:** 30 — parsed", "- **prior:** 30% — parsed")),
        ("a second `scored` sub-bullet (scratch plan, P-DIR-1)", "SPEC-GRAMMAR P-DIR-1",
         lambda: plan_bent("  - `base` — the v6 book on the scored window, bit-equal",
                           "  - `scored` — the v6 book on the scored window, bit-equal")),
        ("a precondition written as prose (scratch plan, P-SFP-VA-1)", "PRECOND-GRAMMAR P-SFP-VA-1",
         lambda: plan_bent(ITEM_OLD_T, PROSE_T)),
        ("a second item with a numeric `required` (`> 0`) added to a copy of P-SCALP-3's block",
         "PRECOND-GRAMMAR P-SCALP-3", lambda: plan_bent(NUMERIC_AFTER_T, NUMERIC_AFTER_T + NUMERIC_ITEM_T)),
        ("a field renamed (scratch plan, P-SCALP-3: statistic -> stat)", "SPEC-GRAMMAR P-SCALP-3",
         lambda: plan_bent("- **statistic:** mean(`net_r`)", "- **stat:** mean(`net_r`)")),
        ("two fields in the other order (scratch plan, P-DIR-1: prior before family_bar)",
         "SPEC-GRAMMAR P-DIR-1", lambda: plan_bent(BAR_THEN_PRIOR_T, PRIOR_THEN_BAR_T)),
        ("one word changed in a filed operative_spec leaf (P-ADM-1 mechanism)", "SPEC-VERBATIM P-ADM-1",
         lambda: verify(doc=bent(leaf_edited))),
        ("one word of a plan block that the frozen block does not carry (P-BRD-1)", "PLAN==LEANS P-BRD-1",
         lambda: plan_bent("Breadth asks whether trend regimes are NEW", "Breadth asks whether trend regimes are OLD")),
    ])


def spec_real():
    c = ctx()
    found = named(verify(), ("SPEC-VERBATIM", "SPEC-GRAMMAR", "PRECOND-GRAMMAR", "PLAN==LEANS", "PLAN-TABLE",
                             "RULER-TEXT"))
    found += spec_referee(c["doc"], c["inputs"]["plan_bytes"], c["inputs"]["leans_bytes"])
    found += grammar_referee(c["doc"])
    return verdict(found, f"the plan's five blocks are the frozen `### REGISTRATION SPEC · <id>` blocks line for "
                          f"line; each block is the {len(FIELDS_T)} fields in order; every filed leaf holds exactly "
                          f"the words of its field (a word-level oracle written here); the checked fields file "
                          f"their leading token; `arms` holds one `scored` element per row; preconditions "
                          + ", ".join(f"{rid} {PRECOND_T[rid]}" for rid in IDS_T)
                          + f" item(s) in the grammar; the ruler sentence opens all {len(IDS_T)} rules and each "
                            f"printed-beside list holds the {len(BESIDE_T)} common items (AP-1's default)")


# ═══════════════════════════════════════════════ F-REG [VERIFIER] [L-X.22]
def verifier_rows() -> list:
    raw = ctx()["inputs"]["contract_bytes"]

    def doc_plant(fn):
        return lambda: verify(doc=bent(fn))

    def text_char(doc):
        b = body_of(doc, "P-SFP-VA-1")
        b["text_of_record"] = swap(b["text_of_record"], "railed ≥ 1.0 ATR_4h", "railed ≥ 1.5 ATR_4h")

    def context_range(doc):
        body_of(doc, "P-ADM-1")["context_of_record"][1]["lines"] = [HEADERS_T["RANGE-STATE"][0]] * 2

    def payload_leaf(doc):
        body_of(doc, "P-SCALP-3")["prior_pct"] += 1

    def seed(doc):
        body_of(doc, "P-ADM-1")["seed"] = SEED_SENS_T

    def moved(doc):
        body_of(doc, "P-DIR-1")["family"] = "ADMISSION"

    def template_of_another(doc):
        b = body_of(doc, "P-SCALP-3")
        b["verdict_rule"] = swap(b["verdict_rule"], _KIN_T, _HAZARD_T)

    def prose(doc):
        body_of(doc, "P-SFP-VA-1")["operative_spec"]["preconditions"] = "the 4h taker licence must read PASS"

    def chain_prev(doc):
        doc["chain"][1]["prev"] = doc["chain"][1]["line_sha256"]

    def spec_word(doc):
        b = body_of(doc, "P-BRD-1")
        b["operative_spec"]["statistic"] = swap(b["operative_spec"]["statistic"], "kept versus all",
                                                "kept versus refused")

    def header_bar():
        door, bytes_ = contract_door(line_swap(HEADERS_T["ADMISSION"][0], "bar 0.05", "bar 0.10"))
        return verify(contract_bytes=bytes_, door=door)

    def ruler_struck():
        door, bytes_ = contract_door(line_swap(TEXT_T["P-SFP-VA-1"][0], "(vs zero; ", "("), refile=True)
        return verify(contract_bytes=bytes_, door=door)

    def pin_head():
        pin = copy_of(ctx()["pin"])
        pin["head"] = GENESIS_T
        return verify(pin=pin)

    def plan_byte():
        return verify(plan_bytes=swap(plan_text(), "the scorer's first act is verify_filing",
                                      "the scorer's first act is verify_filinG").encode("utf-8"))

    return [
        ("a contract byte", "CONTRACT-PREFIX",
         lambda: verify(contract_bytes=raw[:FLIP_AT_T] + bytes([raw[FLIP_AT_T] ^ 1]) + raw[FLIP_AT_T + 1:])),
        ("a text character (P-SFP-VA-1: the rail 1.0 -> 1.5)", "TEXT-SLICE P-SFP-VA-1", doc_plant(text_char)),
        ("a context range (P-ADM-1's header -> the RANGE-STATE header)", "CONTEXT-SLICE P-ADM-1",
         doc_plant(context_range)),
        ("a payload leaf (P-SCALP-3's prior_pct)", "PAYLOAD-SHA P-SCALP-3", doc_plant(payload_leaf)),
        ("the seed (P-ADM-1 filed at the sensitivity seed)", "SEED P-ADM-1", doc_plant(seed)),
        ("a header's bar (scratch contract: STAGE G reads bar 0.10)", "FAMILY-BAR", header_bar),
        ("a registration moved under another header (P-DIR-1 filed under ADMISSION)", "FAMILY-MEMBER P-DIR-1",
         doc_plant(moved)),
        ("the ruler words struck from a slice (scratch contract: `vs zero` off P-SFP-VA-1's text)",
         "RULER-TEXT P-SFP-VA-1", ruler_struck),
        ("a template of another registration (P-SCALP-3 carrying the selection_hazard form)",
         "TEMPLATE P-SCALP-3", doc_plant(template_of_another)),
        ("a checked field with a trailing `%` (scratch plan: P-SCALP-3's prior)", "SPEC-GRAMMAR P-SCALP-3",
         lambda: plan_bent("- **prior:** 30 — parsed", "- **prior:** 30% — parsed")),
        ("a precondition in prose (P-SFP-VA-1's filed leaf)", "PRECOND-GRAMMAR P-SFP-VA-1", doc_plant(prose)),
        ("a chain `prev` (the second entry)", "CHAIN", doc_plant(chain_prev)),
        ("the pin's head", "HEAD-PIN", pin_head),
        ("a spec word (P-BRD-1's statistic: all -> refused)", "SPEC-VERBATIM P-BRD-1", doc_plant(spec_word)),
        ("one byte of the plan (its §2)", "PLAN==LEANS", plan_byte),
    ]


def verifier_break():
    rows = verifier_rows()
    if len(rows) != N_VERIFIER_PLANTS_T:
        raise ValueError(f"{len(rows)} plants, not L-X.22's {N_VERIFIER_PLANTS_T}")
    return FX.plants(rows)


def verifier_real():
    c = ctx()
    found = verify()
    found += referee(c["doc"], c["pin"], c["reg_bytes"], c["inputs"]["plan_bytes"], c["inputs"]["leans_bytes"])
    found += [f"VERIFIER-API the filed pair read back by production's verify() is not silent — {x}"
              for x in REG.verify(ROOT)]
    for rid in IDS_T:
        b = body_of(c["doc"], rid)
        if len(REG.preconditions_of(b)) != PRECOND_T[rid] or not REG.scored_arm(b).startswith("`scored` ") \
                or REG.template_of(b["verdict_rule"]) != TEMPLATES_T[rid][3] \
                or [(x["key"], x["tag"], x["label"]) for x in REG.labels_of(b)] != [TEMPLATES_T[rid][:3]]:
            found.append(f"VERIFIER-API {rid}: a consumer's reader does not return the typed commission")
    return verdict(found, f"verify_filing on the filed pair is silent on all {len(DETECTORS_T)} detectors "
                          f"({' · '.join(DETECTORS_T)}); the independent re-derivation written in this file — "
                          f"slices, shas, chain, families, the template table, the grammar, the word-level spec "
                          f"oracle, the pinned texts, TC11's law — returns no finding; the consumers' readers "
                          f"(scored_arm, labels_of, preconditions_of, template_of) return the typed commission; "
                          f"registry head {c['doc']['head']}")


# ═══════════════════════════════════════════════ F-ATTEST-ORDER [REG] [L-X.21 clause 3]
def own_in(rel: str, patterns) -> bool:
    return any(rel == p or (p.endswith("/**") and rel.startswith(p[:-2])) for p in patterns)


def own_pre(root: Path) -> tuple:
    out = list(PRE_REG_T) + list(PRE_REG_SCRIPTS_T)
    for name in PRE_REG_RECORDS_T:
        p = root / T12_REL / "progress" / name
        if p.is_file():
            for path in json.loads(p.read_text(encoding="utf-8")).get("artifact_shas", {}):
                out.append(path[len(T12_REL) + 1:] if path.startswith(T12_REL + "/") else path)
    return tuple(out)


def own_walk(root: Path) -> dict:
    out = {}
    base = root / T12_REL
    for d, dirs, names in os.walk(base):
        dirs.sort()
        for x in sorted(names):
            rel = (Path(d) / x).relative_to(base).as_posix()
            if rel != ATTEST_SELF_T:
                with (Path(d) / x).open("rb") as f:
                    out[rel] = hashlib.file_digest(f, "sha256").hexdigest()
    for p in sorted((root / "scripts").glob("tierc12_*.py")):
        out["scripts/" + p.name] = sha(p.read_bytes())
    return out


def set_referee(root: Path, walk: dict) -> list:
    """ATTEST-REG, this file's own judgement of a walk — the disk of a scratch tree at filing, or the
    listing of the attested instant — against its typed sets."""
    pre = own_pre(root)
    out = [f"ATTEST-REG {p}: outside PRE_REG_T ∪ REG_SET_T" for p in sorted(walk)
           if not own_in(p, pre) and not own_in(p, REG_SET_T)]
    out += [f"ATTEST-REG {p}: a .parquet outside x_rec/" for p in sorted(walk)
            if p.endswith(".parquet") and not p.startswith(X_REC_T)]
    return out


def own_listing(root: Path):
    """ATTEST_REG.json as (document, {path: sha256}); (None, {}) when it is not on file."""
    p = root / T12_REL / ATTEST_SELF_T
    if not p.is_file():
        return None, {}
    doc = json.loads(p.read_text(encoding="utf-8"))
    return doc, {r["path"]: r["sha256"] for r in doc["files"]}


def own_path(root: Path, rel: str) -> Path:
    """A listed path on disk: scripts/ under the repo, x_rec/ under the main tree's tier directory
    (git-ignored, absent from a linked worktree), every other under this tree's tier directory."""
    if rel.startswith("scripts/"):
        return root / rel
    return (PINS.main_tree(root) if rel.startswith(X_REC_T) else root) / T12_REL / rel


def git(root, *args, stdin: bytes = b"", ro: bool = True, env=None) -> tuple:
    """(exit code, stdout bytes) of one git call on `root`, out of process.  A tree sees the
    read-only verbs of GIT_RO_T only; a write verb runs in a scratch repository under this run's temp
    directory and nowhere else.  No GIT_* variable of the caller reaches git: `-C root` alone names
    the repository."""
    root = Path(root).resolve()
    if ro and args[0] not in GIT_RO_T:
        raise RuntimeError(f"git {args[0]} is not a read-only verb of this suite")
    if not ro and Path(_TMP[0]).resolve() not in root.parents:
        raise RuntimeError("a write verb of git may run in a scratch repository only")
    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    e.update({"GIT_OPTIONAL_LOCKS": "0", **(env or {})})
    r = subprocess.run(["git", "--no-optional-locks", "-C", str(root), *args], input=stdin,
                       capture_output=True, env=e)
    return r.returncode, r.stdout


def repo_rel(rel: str) -> str:
    """A listed path, repo-relative (the listing's are relative to the tier directory unless scripts/)."""
    return rel if rel.startswith("scripts/") else T12_REL + "/" + rel


def registry_commit(root: Path):
    """The commit that FIRST adds registrations/REGISTRATIONS.json — the filing instant on record
    [AM-67; L-X.21's `REG`] — or None when the tree holds no such commit (a tree at its own TC12-REG
    gate, before the commit; a tree that is no repository)."""
    rc, out = git(root, "log", "--diff-filter=A", "--format=%H", "--", REG_FILE_REL_T)
    shas = [s for s in out.decode("ascii", "replace").split() if COMMIT_RX_T.fullmatch(s)] if rc == 0 else []
    return shas[-1] if shas else None                       # `git log` prints newest first: the last is the first add


def registry_blobs(root: Path) -> tuple:
    """(the registry commit, {listed path: sha256 of its BLOB at that commit}) over the listed paths
    the commit TRACKS, outside LATER_T and the append-only texts — (None, None) when the tree holds no
    registry commit.  One `git cat-file --batch`; a path the commit does not track answers `missing`
    and is left out (it is held on the working file)."""
    commit = registry_commit(root)
    if commit is None:
        return None, None
    _, listed = own_listing(root)
    want = [x for x in sorted(listed) if x not in LATER_T and x not in APPEND_ONLY_T and "\n" not in x]
    rc, out = git(root, "cat-file", "--batch",
                  stdin="".join(f"{commit}:{repo_rel(x)}\n" for x in want).encode("utf-8"))
    if rc:
        raise RuntimeError("git cat-file --batch failed on the registry commit")
    blobs, i = {}, 0
    for x in want:
        j = out.index(b"\n", i)
        head, i = out[i:j].split(b" "), j + 1
        if head[-1] == b"missing":
            continue
        size = int(head[-1])
        if head[-2] == b"blob":
            blobs[x] = sha(out[i:i + size])
        i += size + 1
    if i != len(out):
        raise RuntimeError("git cat-file --batch answered other than one object per listed path")
    return commit, blobs


def listing_findings(root: Path, blobs=None) -> list:
    """ATTEST-LISTING: ATTEST_REG.json is the listing of the attested instant, and it still holds.
    It is sorted, counts right, does not list itself and names as absent exactly the REG_SET members
    it does not list; it was taken after the filing on disk.  Every path it LISTS holds the listed
    sha — a text that only grows (APPEND_ONLY_T) holds a byte-prefix at that sha, and the files the
    gate itself writes after that instant (LATER_T) are not held — and no REG_SET member it lists as
    ABSENT has appeared since, outside LATER_T.  A path on disk that the listing does not name is no
    finding: a later record's file was filed after the attested instant, and ATTEST-ORDER holds it to
    git ancestry at TC12-SCORE and CLOSE [L-X.21].

    WHERE the listed sha is held [AM-67]: `blobs` = {listed path: the sha of its blob at the registry
    commit} (registry_blobs) — a path the registry commit tracks is held THERE, at the filing instant,
    never on the working file; every other listed path (git-ignored x_rec/**) on the working file.
    `blobs=None` — a tree with no registry commit — holds every listed path on the working file."""
    doc, listed = own_listing(root)
    if doc is None:
        return ["ATTEST-LISTING ATTEST_REG.json is not on file — run tierc12_registrations.py --attest"]
    out = []
    for x in sorted(listed):
        if x in LATER_T:
            continue
        if blobs is not None and x in blobs and x not in APPEND_ONLY_T:
            if blobs[x] != listed[x]:
                out.append(f"ATTEST-LISTING {x}: the blob at the registry commit is not the listed sha")
            continue
        f = own_path(root, x)
        if not f.is_file():
            out.append(f"ATTEST-LISTING {x}: listed and not on disk")
        elif x in APPEND_ONLY_T:
            if grown_from(f.read_bytes(), listed[x]) is None:
                out.append(f"ATTEST-LISTING {x}: no byte-prefix of the text on disk is the listed sha — it "
                           f"was edited, not appended to")
        else:
            with f.open("rb") as fh:
                if hashlib.file_digest(fh, "sha256").hexdigest() != listed[x]:
                    out.append(f"ATTEST-LISTING {x}: the bytes on disk are not the listed sha")
    out += [f"ATTEST-LISTING {x}: listed absent at the attested instant and on disk now"
            for x in sorted(doc["absent"]) if x not in LATER_T and own_path(root, x).is_file()]
    if len(listed) != len(doc["files"]) or doc["n_files"] != len(listed) or ATTEST_SELF_T in listed \
            or [r["path"] for r in doc["files"]] != sorted(listed) \
            or sorted(doc["absent"]) != sorted(x for x in REG_SET_T if x not in listed and x != ATTEST_SELF_T):
        out.append("ATTEST-LISTING the listing is not sorted, repeats a path, miscounts, lists itself, or its "
                   "`absent` is not the REG_SET members it does not list")
    if doc["taken_after"].get("registrations_sha256") != listed.get("registrations/REGISTRATIONS.json"):
        out.append("ATTEST-LISTING the listing was not taken after the filing it lists")
    p = root / T12_REL / ATTEST_SELF_T
    if p.read_bytes() != (json.dumps(doc, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"):
        out.append("ATTEST-LISTING ATTEST_REG.json is not its own document rendered with sorted keys")
    return out


AMENDMENTS_AT_T = b"# amendments of record\n## AM-1\n"     # the scratch tree's amendments at the attested instant
AMENDMENT_LATER_T = b"## AM-2\n"                           # an amendment appended after it
# lawful acts AFTER the attested instant, on the scratch tree {repo-relative path: bytes}: the listing
# stays silent on every one (the control of the break leg)
LAWFUL_LATER_T = {
    T12_REL + "/LEANS_AMENDMENTS.md": AMENDMENTS_AT_T + AMENDMENT_LATER_T,   # an amendment appended [O-35]
    T12_REL + "/progress/TC12-D.json": b"{}\n",                              # a later record
    T12_REL + "/forward/BOOK_SPEC_COMBINED.json": b"{}\n",                   # the ledger-spec child [L-X.21]
    "scripts/tierc12_forward_spec.py": b"",
    T12_REL + "/progress/TC12-REG.json": b"{}\n",                            # LATER_T: the stage's own record
    T12_REL + "/PROGRESS.json": b"{\"stage\": \"TC12-REG\"}\n",              # LATER_T: modified by the commit
}


def attest_tree(extra=None) -> Path:
    """A scratch tree in the shape of the estate at filing: a few PRE_REG files, the filed pair, the
    typed scripts — plus `extra` {repo-relative path: bytes}."""
    r = scratch_dir()
    rec = json.dumps({"artifact_shas": {T12_REL + "/LEANS.md": {}, CONTRACT_T: {}}}).encode("utf-8")
    files = {T12_REL + "/LEANS.md": b"readings\n", T12_REL + "/PROGRESS.json": b"{}\n",
             T12_REL + "/LEANS_AMENDMENTS.md": AMENDMENTS_AT_T,
             T12_REL + "/.gitignore": b"**/*.parquet\n", T12_REL + "/scout/U1.md": b"scout\n",
             T12_REL + "/x_rec/tierc11x/va/feasibility.parquet": b"an X record\n",
             T12_REL + "/progress/STEP_Q.json": rec, T12_REL + "/progress/TC12-R0.json": rec,
             T12_REL + "/progress/TC12-LEANS.json": rec, T12_REL + "/REGISTRATION_PLAN.md": b"plan\n",
             T12_REL + "/registrations/REGISTRATIONS.json": b"{}\n",
             T12_REL + "/registrations/REGISTRY_PIN.json": b"{\"head\": \"scratch\"}\n",
             T12_REL + "/pins/CONTRACT_PINS.json": b"{}\n",
             "scripts/tierc12_progress.py": b"", "scripts/tierc12_registrations.py": b"",
             "scripts/tierc12_fx.py": b"", **(extra or {})}
    for rel, body in files.items():
        (r / rel).parent.mkdir(parents=True, exist_ok=True)
        (r / rel).write_bytes(body)
    return r


def attested(extra_after=None) -> list:
    """A scratch tree attested by production, then bent AFTER the attestation."""
    r = attest_tree()
    (r / T12_REL / ATTEST_SELF_T).write_bytes(REG.render_sorted(REG.attest_doc(r)))
    for rel, body in (extra_after or {}).items():
        (r / rel).parent.mkdir(parents=True, exist_ok=True)
        (r / rel).write_bytes(body)
    return listing_findings(r)


def unfiled() -> list:
    r = attest_tree()
    (r / T12_REL / "registrations" / "REGISTRATIONS.json").unlink()
    return REG.attest_findings(r)


def committed(before=None, after=None) -> list:
    """A scratch tree attested by production and then COMMITTED to a scratch repository of its own —
    that one commit is its registry commit — with `before` written between the attestation and the
    commit and `after` written after it; judged in the form the tree of record is judged [AM-67]."""
    r = attest_tree()
    (r / T12_REL / ATTEST_SELF_T).write_bytes(REG.render_sorted(REG.attest_doc(r)))
    env = {"GIT_AUTHOR_NAME": "Scratch Fixture", "GIT_AUTHOR_EMAIL": "fixture@scratch.invalid",
           "GIT_COMMITTER_NAME": "Scratch Fixture", "GIT_COMMITTER_EMAIL": "fixture@scratch.invalid",
           "GIT_AUTHOR_DATE": SCRATCH_DATE_T, "GIT_COMMITTER_DATE": SCRATCH_DATE_T,
           "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CEILING_DIRECTORIES": _TMP[0]}
    for step, files in ((SCRATCH_GIT_T, before), ((), after)):
        for rel, body in (files or {}).items():
            (r / rel).parent.mkdir(parents=True, exist_ok=True)
            (r / rel).write_bytes(body)
        for args in step:
            if git(r, *args, ro=False, env=env)[0]:
                raise RuntimeError(f"scratch git {args[0]} failed")
    commit, blobs = registry_blobs(r)
    if commit is None or not blobs:
        raise RuntimeError("the scratch repository holds no registry commit")
    return listing_findings(r, blobs)


X_REC_SCRATCH_T = "x_rec/tierc11x/va/feasibility.parquet"   # the scratch tree's git-ignored X record
REPAIR_T = {"scripts/tierc12_fx.py": b"# repaired under a dated amendment, after the registry commit\n"}


def blob_form_controls() -> None:
    """AM-67's form on a scratch REPOSITORY, held as controls of the break leg: silent when they hold,
    a raise — the break leg is then VOID — when one does not.  (They are not rows of `plants`: the
    eight rows below are the transcript of record's, judged in the form of a tree with no commit.)"""
    if not attested(REPAIR_T):
        raise ValueError("a tree with NO registry commit does not hold a listed script on the working file — "
                         "the scratch form is not the form before AM-67")
    if committed(after={**LAWFUL_LATER_T, **REPAIR_T}):
        raise ValueError("a lawful repair of a tracked REG_SET script AFTER the registry commit is a finding "
                         "of the listing — AM-67's control is not GREEN")
    want = "ATTEST-LISTING LEANS.md: the blob at the registry commit is not the listed sha"
    if committed(before={T12_REL + "/LEANS.md": b"readings, edited\n"}) != [want]:
        raise ValueError("a listed tracked file changed between the attested instant and the registry commit "
                         "is not caught from the commit's blob [AM-67]")
    want = f"ATTEST-LISTING {X_REC_SCRATCH_T}: the bytes on disk are not the listed sha"
    if committed(after={T12_REL + "/" + X_REC_SCRATCH_T: b"an X record, edited\n"}) != [want]:
        raise ValueError("a git-ignored listed path (x_rec/**) changed on disk is not caught on the working "
                         "file, as before [AM-67]")


def attest_break():
    clean = attest_tree()
    if REG.attest_findings(clean) or set_referee(clean, own_walk(clean)) or attested():
        raise ValueError("the clean scratch tree is not GREEN — the plants would prove nothing")
    if attested(LAWFUL_LATER_T):
        raise ValueError("a lawful later act (an appended amendment, a later record's files, the stage's own "
                         "record, PROGRESS.json re-merged) is a finding of the listing — the control is not GREEN")
    blob_form_controls()
    return FX.plants([
        ("an ignored `books/x.parquet` present at filing", "ATTEST-REG books/x.parquet",
         lambda: REG.attest_findings(attest_tree({T12_REL + "/books/x.parquet": b"a book\n"}))),
        ("a stage script `scripts/tierc12_books.py` present at filing", "ATTEST-REG scripts/tierc12_books.py",
         lambda: REG.attest_findings(attest_tree({"scripts/tierc12_books.py": b"# a stage script\n"}))),
        ("a file outside both sets (`notes/TODO.md`)", "ATTEST-REG notes/TODO.md",
         lambda: REG.attest_findings(attest_tree({T12_REL + "/notes/TODO.md": b"x\n"}))),
        ("a `.parquet` under a PRE_REG directory (`scout/x.parquet`)", "ATTEST-REG scout/x.parquet",
         lambda: REG.attest_findings(attest_tree({T12_REL + "/scout/x.parquet": b"x\n"}))),
        ("an attestation asked for before the registry is filed", "ATTEST-REG registrations/REGISTRATIONS.json",
         unfiled),
        ("one byte of a listed file changed after the attestation (LEANS.md)", "ATTEST-LISTING LEANS.md",
         lambda: attested({T12_REL + "/LEANS.md": b"readings, edited\n"})),
        ("a file added after the attestation (`scripts/tierc12_units.py`)",
         "ATTEST-LISTING scripts/tierc12_units.py", lambda: attested({"scripts/tierc12_units.py": b"X = 1\n"})),
        ("a listed append-only text edited inside its listed bytes, then appended to (LEANS_AMENDMENTS.md)",
         "ATTEST-LISTING LEANS_AMENDMENTS.md",
         lambda: attested({T12_REL + "/LEANS_AMENDMENTS.md": AMENDMENTS_AT_T.upper() + AMENDMENT_LATER_T})),
    ])


def attest_real():
    """The LISTING of the attested instant is what is judged — production's detector and this file's
    typed sets over the paths ATTEST_REG.json lists — never the disk as it stands at a later run.  A
    listed path the registry commit tracks is held to its blob at that commit, never to the working
    file [AM-67]; the words of the transcript of record are unchanged."""
    doc, listed = own_listing(ROOT)
    if doc is None:
        return False, "ATTEST-LISTING ATTEST_REG.json is not on file — run tierc12_registrations.py --attest"
    commit, blobs = registry_blobs(ROOT)
    FX.clock(f"[AM-67] no commit of this tree adds {REG_FILE_REL_T}: every listed path is held on the working file"
             if commit is None else
             f"[AM-67] registry commit {commit}: {len(blobs)} listed path(s) it tracks are held to their blob at "
             f"that commit, never to the working file; the others outside LATER_T (git-ignored x_rec/**; the "
             f"append-only texts, by byte-prefix) on the working file")
    found = REG.attest_findings(ROOT, walk=listed) + set_referee(ROOT, listed) + listing_findings(ROOT, blobs)
    if (REG.PRE_REG, REG.PRE_REG_RECORDS, REG.PRE_REG_SCRIPTS, REG.REG_SET) != (
            PRE_REG_T, PRE_REG_RECORDS_T, PRE_REG_SCRIPTS_T, REG_SET_T):
        found.append("ATTEST-SETS production's PRE_REG / REG_SET are not this file's typed sets")
    if not set(LATER_T) <= set(REG_SET_T) | {"PROGRESS.json"} | set(PRE_REG_SCRIPTS_T):
        found.append("ATTEST-SETS LATER_T names a path outside REG_SET and the two files the commit modifies")
    if not set(APPEND_ONLY_T) <= set(PRE_REG_T):
        found.append("ATTEST-SETS APPEND_ONLY_T names a text outside PRE_REG")
    on_disk = {(Path(d) / x).relative_to(T12).as_posix() for d, _, names in os.walk(T12) for x in names}
    on_disk |= {"scripts/" + p.name for p in (ROOT / "scripts").glob("tierc12_*.py")}
    unnamed = sorted(on_disk - set(listed) - set(doc["absent"]) - {ATTEST_SELF_T})
    FX.clock(f"{len(listed)} files listed at the attested instant under {T12_REL}/ and scripts/tierc12_*.py; "
             f"REG_SET members then absent: {doc['absent']}; on disk now and not named by the listing (filed "
             f"after it; held by ATTEST-ORDER, no finding here): {len(unnamed)} — {unnamed[:SHOWN_T]}")
    return verdict(found, f"ATTEST_REG.json, taken after --file, is the sorted listing of the disk walk at filing "
                          f"except itself, and the LISTING is what is judged, not the disk as it stands at a later "
                          f"run: every listed path is in PRE_REG ∪ REG_SET ({len(PRE_REG_T)} typed patterns and "
                          f"the artifact paths of {len(PRE_REG_RECORDS_T)} records; {len(REG_SET_T)} typed "
                          f"members) by production's detector and by this file's typed sets; no .parquet is "
                          f"listed outside x_rec/; no scripts/tierc12_*.py is listed outside tierc12_progress.py "
                          f"and REG_SET's scripts; every listed path is on disk at its listed sha — the "
                          f"{len(APPEND_ONLY_T)} append-only texts {list(APPEND_ONLY_T)} hold a byte-prefix at "
                          f"that sha, the {len(LATER_T)} paths the gate writes after the attested instant are not "
                          f"held — and no REG_SET member listed absent has appeared outside those "
                          f"{len(LATER_T)}; a path the listing does not name (a later record's file, the "
                          f"ledger-spec child) was filed after the attested instant and is no finding here — "
                          f"ATTEST-ORDER holds it to git ancestry at TC12-SCORE and CLOSE; production's sets == "
                          f"the typed sets (counts and the unnamed paths are printed on stdout only)")


FIXTURES = [
    ("F-CONTRACT-PIN", "the contract is pinned by its prefix [L-X.16, L-X.35]",
     "a prefix byte flipped, a `BUILT:` line inserted under RATIFIED, a foreign tail line or an unterminated "
     "tail passes the verifier — each must stop CONTRACT-PREFIX or CONTRACT-TAIL",
     "a scratch copy of the contract with a `BUILT:` line appended as its last line changes any slice, payload "
     "sha, chain line, the head or a verifier finding, or moves a byte of a re-derived PROGRESS.json; or the "
     "prefix is not the typed STEP Q bytes",
     contract_pin_break, judged(contract_pin_real)),
    ("F-REG [SLICE]", "every text, context and external slice re-cuts from pinned bytes [L-X.17]",
     "a filed text with one character edited, a context range bent, an external slice edited, cut from other "
     "bytes, or cut from a script the tc11-stamp moves is not caught by TEXT-SLICE / CONTEXT-SLICE / "
     "EXTERNAL-SLICE",
     "any text, context or external slice of the filing does not re-cut from pinned bytes, or its sha differs "
     "from the line map's; or this file's own cut of the typed ranges disagrees with the filing",
     slice_break, judged(slice_real)),
    ("F-REG [HASH]", "payload shas, the chain, the head and TC11's law by object [L-X.19]",
     "a bent `prev`, a changed `family_m` or a swapped order is not caught by CHAIN / PAYLOAD-SHA; an edited "
     "`law` or a `law_source` carrying a whole-file sha is not caught by this file's referee",
     "a payload sha or the chain does not re-derive from the filed bodies from the genesis string; the head or "
     "the pin differs; the filed `law` is not TC11's by object, or `law_source` carries a whole-file sha; a "
     "pinned text, n_boot, a seed, the scored window's end or the era cut is not the file's or the typed value "
     "(`amendments`: the file as it stood at filing — a byte-prefix of the file on disk, holding AM-1)",
     hash_break, judged(hash_real)),
    ("F-REG [WRITE-ONCE]", "a second filing changes no byte and does not exit 0 [L-X.20]",
     "a filer whose exclusive create `\"xb\"` is replaced by `\"wb\"` passes — it must be caught writing over a "
     "file on record",
     "a second `--file` changes a byte or exits 0, in the filed directory or in a scratch twin; a create() on a "
     "filed path succeeds; or a scratch twin filed from the texts on disk differs from the filed pair anywhere "
     "but in the leaves that name a text which only grows after filing (the contract's whole-file sha, the "
     "amendments file's sha, the pin's sha of the file that carries them)",
     write_once_break, judged(write_once_real)),
    ("F-REG [TEMPLATE]", "one template per rule, its registration's row of L-X.13 [L-X.13, CANON-01]",
     "P-ADM-1's template rewritten to the selection_hazard form, P-SFP-VA-1's to the RE-SCORE form, "
     "`DIRECTION-INFORMED` in capitals on P-DIR-1, a rule with no template or with two, or a label carrying "
     "another row's tag passes TEMPLATE",
     "a filed rule carries zero or two templates, or a template, label key, tag or label that is not its "
     "registration's row of the table byte for byte; \"re-score\" stands in a template or label other than "
     "P-ADM-1's; or the table read from the frozen readings differs from the typed table",
     template_break, judged(template_real)),
    ("F-REG [SPEC-VERBATIM]", "spec leaf == plan block == LEANS block; one field grammar [L-X.18]",
     "one word changed in a plan's `arms` field or in a filed leaf, `prior: 30%`, a second `scored` sub-bullet, "
     "a precondition in prose, a numeric `required`, a renamed or reordered field, or a plan block the frozen "
     "block does not carry passes SPEC-VERBATIM / SPEC-GRAMMAR / PRECOND-GRAMMAR / PLAN==LEANS",
     "an operative_spec leaf differs from the plan's block, the plan's block from the LEANS's, or a "
     "machine-read field is outside L-X.18's grammar; or the ruler sentence (AP-1's default) does not open a "
     "rule or a printed-beside list lacks a common item",
     spec_break, judged(spec_real)),
    ("F-REG [VERIFIER]", "each plant caught by its intended detector, one at a time [L-X.22]",
     "one of L-X.22's fifteen plants — a contract byte; a text character; a context range; a payload leaf; the "
     "seed; a header's bar; a registration moved under another header; the ruler words struck from a slice; a "
     "template of another registration; a checked field with a trailing %; a precondition in prose; a chain "
     "prev; the pin's head; a spec word; one byte of the plan — is not caught by its intended detector",
     "verify_filing returns a finding on the filed pair, or the independent re-derivation written in this file "
     "(slices, shas, chain, the template table, the grammar) disagrees with the filing",
     verifier_break, judged(verifier_real)),
    ("F-ATTEST-ORDER [REG]", "text before result, at filing: the disk walk and its listing [L-X.21]",
     "an ignored `books/x.parquet`, a stage script `scripts/tierc12_books.py`, a file outside both sets or a "
     "parquet outside x_rec/ present at filing, an attestation before the filing, or — after the attestation — "
     "a listed file changed, a REG_SET member then absent added, or an append-only text edited inside its "
     "listed bytes is not caught by ATTEST-REG / ATTEST-LISTING",
     "the disk walk at filing, as ATTEST_REG.json lists it, holds a file outside PRE_REG ∪ REG_SET, a "
     "`.parquet` outside x_rec/, or a scripts/tierc12_*.py outside the typed set; or ATTEST_REG.json is not "
     "that listing — a listed path is not on disk at its listed sha (an append-only text: a byte-prefix at "
     "it; the files the gate writes after the attested instant are not held) or a REG_SET member it lists "
     "as absent has appeared",
     attest_break, judged(attest_real)),
]


def main(argv) -> int:
    root = Path(FX.opt(argv, "--root=", str(T12 / "registrations")))
    tmp = tempfile.mkdtemp(prefix="tierc12_reg_fx_")
    _TMP[:] = [tmp]
    _CTX.clear()
    typed = [
        f"SEED_T {SEED_T} · SEED_SENS_T {SEED_SENS_T} · N_BOOT_T {N_BOOT_T} · SCORED_END_MS_T {SCORED_END_MS_T} "
        f"· ERA_CUT_MS_T {ERA_CUT_MS_T}",
        f"PREFIX_BYTES_T {PREFIX_BYTES_T} · PREFIX_SHA_T {PREFIX_SHA_T} · N_LINES_T {N_LINES_T} · "
        f"N_MAP_ROWS_T {N_MAP_ROWS_T}",
        "TEXT_T " + "; ".join(f"{rid} :{TEXT_T[rid][0]}-{TEXT_T[rid][1]}" for rid in IDS_T)
        + f" · LAWS_T :{LAWS_T[0]}-{LAWS_T[1]} · HEADERS_T "
        + "; ".join(f"{k} :{v[0]}" for k, v in HEADERS_T.items()),
        f"Q_T {Q_T} · FAMILY_T " + "; ".join(f"{rid} {f} {s} m={m} bar {b} ({e}) [{p}%]"
                                              for rid, (f, s, m, b, e, p) in FAMILY_T.items()),
        "TEMPLATES_T " + "; ".join(f"{rid} {TEMPLATES_T[rid][0]} · {TEMPLATES_T[rid][1]}" for rid in IDS_T)
        + f" · RESCORE_IDS_T {list(RESCORE_IDS_T)}",
        f"RULER_T the ruler sentence of AP-1's default ({len(RULER_T)} characters) · BESIDE_T "
        f"{len(BESIDE_T)} items · RULER_WORDS_T two-sample vs v6 ×3, vs zero ×2",
        f"FIELDS_T {len(FIELDS_T)} fields · SPEC_KEYS_T {len(SPEC_KEYS_T)} · PRECOND_T "
        + "; ".join(f"{rid} {PRECOND_T[rid]}" for rid in IDS_T)
        + " · EXTERNAL_T " + "; ".join(f"{rid} {len(v)}" for rid, v in EXTERNAL_T.items()),
        f"TOP_KEYS_T {len(TOP_KEYS_T)} · BODY_KEYS_T {len(BODY_KEYS_T)} · PIN_KEYS_T {len(PIN_KEYS_T)} · "
        f"PINNED_T {list(PINNED_T)} · T11_HEAD_T {T11_HEAD_T}",
        f"DETECTORS_T {len(DETECTORS_T)} · N_VERIFIER_PLANTS_T {N_VERIFIER_PLANTS_T} · FLIP_AT_T {FLIP_AT_T} · "
        f"RATIFIED_LINES_T {RATIFIED_LINES_T}",
        f"PRE_REG_T {list(PRE_REG_T)} + the artifact paths of {list(PRE_REG_RECORDS_T)} + "
        f"{list(PRE_REG_SCRIPTS_T)}",
        f"REG_SET_T {list(REG_SET_T)}",
        f"LATER_T {list(LATER_T)}",
        f"APPEND_ONLY_T {list(APPEND_ONLY_T)} · GROWS_T " + "; ".join(f"{k}.{leaf}" for k, leaf in GROWS_T)
        + f" · GROWS_PIN_T {GROWS_PIN_T} · AM_FIRST_T {AM_FIRST_T!r}",
        "no seeded draw: every leg reads the whole filing (n = the five registrations)",
    ]
    try:
        return FX.run_suite(args=argv, root=root, transcript=TRANSCRIPT, banner=BANNER, seed=SEED_T,
                            fixtures=FIXTURES, typed=typed)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
