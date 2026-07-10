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


def test_v11_faithful_also_deterministic(synth_env, synth_cell, tmp_path):
    a = run_replay("v11_faithful", synth_cell.cell_id, SYNTH_START, SYNTH_END,
                   tmp_path / "j1", log=lambda *_: None)
    b = run_replay("v11_faithful", synth_cell.cell_id, SYNTH_START, SYNTH_END,
                   tmp_path / "j2", log=lambda *_: None)
    assert a["journal_sha256"] == b["journal_sha256"]
