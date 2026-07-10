"""F1 — determinism: two replay runs with identical args produce
byte-identical journals (SHA-256), and re-running into the same journal is a
no-op (idempotent merge)."""

from pathlib import Path

from conftest import SYNTH_END, SYNTH_START

from engine.replay import run_replay


def test_bit_identical_reruns(synth_env, synth_cell, tmp_path):
    a = run_replay("naiad_v0", synth_cell.cell_id, SYNTH_START, SYNTH_END,
                   tmp_path / "j1", log=lambda *_: None)
    b = run_replay("naiad_v0", synth_cell.cell_id, SYNTH_START, SYNTH_END,
                   tmp_path / "j2", log=lambda *_: None)
    assert a["rows"] > 0, "synthetic window produced no journal rows"
    assert a["journal_sha256"] == b["journal_sha256"]
    assert a["run_id"] == b["run_id"]

    files1 = sorted((tmp_path / "j1" / synth_cell.cell_id).glob("*.jsonl"))
    files2 = sorted((tmp_path / "j2" / synth_cell.cell_id).glob("*.jsonl"))
    assert [f.name for f in files1] == [f.name for f in files2]
    for f1, f2 in zip(files1, files2):
        assert f1.read_bytes() == f2.read_bytes()


def test_idempotent_remerge(synth_env, synth_cell, tmp_path):
    a = run_replay("naiad_v0", synth_cell.cell_id, SYNTH_START, SYNTH_END,
                   tmp_path / "j", log=lambda *_: None)
    b = run_replay("naiad_v0", synth_cell.cell_id, SYNTH_START, SYNTH_END,
                   tmp_path / "j", log=lambda *_: None)   # same root again
    assert a["journal_sha256"] == b["journal_sha256"]


def test_f1b_summary_derived_from_persisted_bytes(synth_env, synth_cell, tmp_path):
    """F1b (reviewer ticket D-1): summary `rows` and `journal_sha256` must be
    reproducible from the written files alone, by an independent code path —
    sha256 over the byte concatenation of the run's monthly files in
    chronological (filename) order; rows = newline count."""
    import hashlib

    summary = run_replay("naiad_v0", synth_cell.cell_id, SYNTH_START,
                         SYNTH_END, tmp_path / "j", log=lambda *_: None)
    files = sorted((Path(p) for p in summary["files"]), key=lambda p: p.name)
    assert files, "run wrote no files"

    h = hashlib.sha256()
    lines = 0
    for f in files:
        b = f.read_bytes()
        h.update(b)
        lines += b.count(b"\n")
    assert summary["rows"] == lines, \
        f"summary rows {summary['rows']} != persisted line count {lines}"
    assert summary["journal_sha256"] == h.hexdigest(), \
        "summary sha256 does not match the documented on-disk formula"


def test_v11_faithful_also_deterministic(synth_env, synth_cell, tmp_path):
    a = run_replay("v11_faithful", synth_cell.cell_id, SYNTH_START, SYNTH_END,
                   tmp_path / "j1", log=lambda *_: None)
    b = run_replay("v11_faithful", synth_cell.cell_id, SYNTH_START, SYNTH_END,
                   tmp_path / "j2", log=lambda *_: None)
    assert a["journal_sha256"] == b["journal_sha256"]
