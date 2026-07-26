# Builder Contract — `scripts/reviewer_manifest.py`
### One-paste integrity manifest for the reviewer loop · OPS tier · drafted 2026-07-26, ratified by operator

## §0 What this is
A small tracked script that replaces the multi-screenshot verification dance between operator, builder and reviewer. One run emits one JSON containing everything the reviewer needs to trust the context box: repo state, per-file hashes, HEAD-blob comparisons, and the untracked-root inventory. **This is an OPS artifact — Tier-0. It is not study evidence, needs no G-7, touches no journals, and changes no engine behavior.**

## §1 Invariants
1. **Read-only on everything except its own output.** The script writes exactly one file: `_reviewer_box/MANIFEST.json` (already git-ignored). No other writes, no deletes, no git mutations.
2. **Pure-Python byte handling.** All hashing via `hashlib.sha256` on binary reads (`open(p,'rb')`). No shelling out to `grep`/`sed`/text pipelines for byte questions (msys strips CR — known hazard, 2026-07-26).
3. Git queries via `subprocess` are permitted and read-only: `rev-parse`, `status --porcelain`, `cat-file`, `ls-files`, `branch -a --contains`.
4. Engine modules are **not imported**. Standard library only.

## §2 Manifest content (top-level keys, exact)
- `generated_utc` — ISO timestamp (the only run-varying field).
- `head` — full SHA; `branch`; `ahead_behind` vs `origin/<branch>`; `origin_head` SHA.
- `status_porcelain` — verbatim lines.
- `sources` — for every path in the in-script `SOURCES` list (initial list below): `{path, tracked: bool, size, sha256_worktree, sha256_head_blob (raw bytes of `git cat-file blob HEAD:<path>` hashed), match_head: bool}`. Missing file → `{path, present: false}`.
- `reviewer_box` — same fields for every file currently in `_reviewer_box/` (excluding `MANIFEST.json` itself), plus `source_guess` mapped by the flattening rule (`engine_X.py → engine/X.py`, `configs_X → configs/X`, `scripts_X → scripts/X`).
- `untracked_root` — every untracked file at repo root: `{name, size, sha256}` (the `git clean` exposure inventory).
- `eol_config` — values of `core.autocrlf` and the `.gitattributes` `* -text` presence, so byte-comparison validity is self-documenting.

Initial `SOURCES` (edit in-script, comment says so): all of `engine/*.py`; `configs/*.yaml`; `configs/tc5_*.json`; `scripts/census_build.py`, `scripts/census_analyze.py`, `scripts/census1b_*.py`, `scripts/s2b_decompose.py`, `scripts/s3_*.py`, `scripts/tc1_*.py`, `scripts/tc5_*.py`; `LEDGER.md`; `DATA_CENSUS.md`; `census.json`; `research_outputs/census/build_manifest.json`.

## §3 Fixtures (all must pass; print PASS/FAIL per fixture then exit code)
- **F-M1 self-hash**: the manifest includes `scripts/reviewer_manifest.py` in `sources`; after writing, re-read the script from disk, recompute, assert equality with the recorded value.
- **F-M2 blob-comparison correctness**: assert `engine/cells.py` reports `tracked: true` and `match_head: true`; then, in a temp directory (never the repo), write a one-byte-different copy and assert the comparison helper returns False for it (test double proves the comparator can fail).
- **F-M3 determinism**: run twice back-to-back; the two JSONs must be byte-identical after removing the `generated_utc` line.
- **F-M4 read-only audit**: `git status --porcelain` captured before and after the run must be identical (the output file is ignored, so it never appears).

## §4 Deliverables
1. `scripts/reviewer_manifest.py` (committed).
2. One sample `_reviewer_box/MANIFEST.json` from a real run (not committed — ignored; operator drops it in the reviewer box).
3. Fixture run transcript pasted back.
4. Commit message: `ops: reviewer_manifest.py — one-paste integrity manifest (F-M1..4 pass)`. **Commit, do not push** (push batches remain manual per standing governance).

## §5 Verdict criteria
PASS = 4/4 fixtures + sample manifest parses + reviewer spot-verifies ≥3 sha256 values locally against box copies. Any FAIL → halt and report; no partial adoption.

## §6 What this phase is not
Not a study phase; no predictions, no ledger scorecard. Not a substitute for the ledger — material facts the manifest surfaces (e.g., unexplained origin drift) still get ledger lines. Not a file-sync tool — it reports, never copies.

## §7 Operator run instruction (after builder delivers)
Paste to Claude Code, any time the reviewer asks for state:
```
python scripts/reviewer_manifest.py
```
Expected output: `PASS F-M1..F-M4` lines and `wrote _reviewer_box/MANIFEST.json (<n> sources, <m> box files, <k> untracked root)`. Then drag `MANIFEST.json` into the project context box. That is the whole loop.
