"""F-B9..F-B24 (storage subset) and F-B32 — record and storage (Amendment 2 §8).

Run: C:\\venvs\\naiad\\Scripts\\python.exe -m pytest tests/test_brief2_storage.py -q

These run against the REAL capture in `briefs/` when one exists, and skip with a
stated reason when it does not — a fixture that silently passes because there is
nothing to check is worse than one that says so.
"""

import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import analytics                                                    # noqa: E402
import brief2 as B2                                                 # noqa: E402
import brief_capture as BC                                          # noqa: E402
import brief_panel as BP                                            # noqa: E402

BRIEFS = ROOT / "briefs"


def _captures():
    return sorted(BRIEFS.glob("brief_*_*.json"))


def _one():
    caps = _captures()
    if not caps:
        pytest.skip("no capture in briefs/ — run scripts/brief_capture.py first")
    with caps[-1].open(encoding="utf-8") as fh:
        return caps[-1], json.load(fh)


# --------------------------------------------------------------- F-B9

def test_f_b9_capture_round_trip_and_json_sha256():
    """The stored bytes re-read binary must hash to the index's json_sha256."""
    import hashlib
    path, doc = _one()
    sha = hashlib.sha256(path.read_bytes()).hexdigest()

    idx = BRIEFS / "index.jsonl"
    assert idx.exists(), "no index.jsonl"
    lines = [json.loads(x) for x in idx.read_text(encoding="utf-8").splitlines() if x.strip()]
    row = [r for r in lines if r["json_path"].endswith(path.name)]
    assert row, f"{path.name} is not in the index"
    assert row[-1]["json_sha256"] == sha, \
        "stored capture does not match the sha recorded in the index"

    # round-trip: re-serialising the parsed document reproduces the bytes
    assert BC.serialize(doc) == path.read_text(encoding="utf-8"), \
        "capture does not round-trip through serialize()"


def test_f_b9_envelope_carries_every_required_field():
    _, doc = _one()
    for key in ("schema_version", "rules_version", "rules_sha256",
                "analytics_version", "analytics_sha", "engine_version", "slot",
                "rules", "universe", "parity_certified"):
        assert key in doc, f"capture is missing {key}"
    assert doc["rules_version"] == "2.0.0"
    assert doc["analytics_version"] == analytics.ANALYTICS_VERSION
    assert len(doc["analytics_sha"]) == 64
    assert doc["rules_sha256"] == B2.canonical_rules_sha256(doc["rules"])

    # every input's last_bar_utc, per asset
    for sym, a in doc["assets"].items():
        assert a.get("last_bar_utc"), f"{sym} has no last_bar_utc"
        assert a.get("substrate_used"), f"{sym} does not record its substrate"


# --------------------------------------------------------------- F-B15

FORBIDDEN_SIZING = re.compile(r"\b(size|qty|quantity|notional|leverage|contracts)\b",
                              re.I)


def test_f_b15_no_sizing_anywhere_in_the_capture():
    """§7.1: NO SIZING, EVER — asserted over every key AND every string value."""
    path, doc = _one()
    hits = []

    def walk(node, trail=""):
        if isinstance(node, dict):
            for k, v in node.items():
                if FORBIDDEN_SIZING.search(str(k)):
                    hits.append(f"KEY {trail}.{k}")
                walk(v, f"{trail}.{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{trail}[{i}]")
        elif isinstance(node, str) and FORBIDDEN_SIZING.search(node):
            # `no_sizing: true` and prose that FORBIDS sizing are not violations
            if "no_sizing" not in trail and "sizing" not in node.lower():
                hits.append(f"VALUE {trail} = {node[:60]}")

    walk(doc)
    assert not hits, "sizing language reached the capture:\n" + "\n".join(hits[:10])


# --------------------------------------------------------------- F-B16

def test_f_b16_firewall_no_journal_no_outcome_no_lockbox_statistic():
    """The capture path may not import journals or compute outcome statistics."""
    for name in ("brief2.py", "brief_capture.py", "brief_panel.py"):
        src = (ROOT / "scripts" / name).read_text(encoding="utf-8")
        assert "engine.journal" not in src and "from engine import journal" not in src, \
            f"{name} imports the journal"
        assert "engine.replay" not in src and "engine.trading" not in src, \
            f"{name} imports a trading/replay surface"
        for banned in ("win_rate", "hit_rate", "expectancy", "r_multiple",
                       "pnl", "profit"):
            assert banned not in src.lower(), f"{name} computes {banned}"

    _, doc = _one()
    blob = json.dumps(doc).lower()
    for banned in ("win_rate", "hit_rate", "expectancy", "r_multiple", "pnl"):
        assert banned not in blob, f"capture carries {banned}"


def test_f_b16_lockbox_is_disclosed_not_read_as_evidence():
    _, doc = _one()
    assert "lockbox" in doc
    assert doc["lockbox"]["window"] == [analytics.LOCKBOX_START_MS,
                                        analytics.LOCKBOX_END_MS]
    for sym, a in doc["assets"].items():
        fp = a.get("partition_footprint")
        assert fp and "lockbox_overlap" in fp, f"{sym} has no footprint disclosure"
        w365 = (a["volume_windows"]["windows"].get("365d") or {})
        ov = (w365.get("lockbox_overlap") or {})
        if ov:
            assert "basis" in ov, "overlap recorded without its basis"


# --------------------------------------------------------------- F-B17

def test_f_b17_every_layer_input_bar_is_closed_at_as_of():
    """No layer's newest input bar may extend past the decision bar."""
    from datetime import datetime, timezone
    _, doc = _one()
    as_of = datetime.strptime(doc["as_of_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc)
    for sym, a in doc["assets"].items():
        for tf, stamp in (a.get("last_bar_utc") or {}).items():
            t = datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=timezone.utc)
            assert t <= as_of, f"{sym} {tf} last bar {stamp} is after as_of"


# --------------------------------------------------------------- F-B18

FORBIDDEN_POSITION_KEYS = (
    "pnl", "p_and_l", "realised", "unrealised", "result", "outcome", "win",
    "loss", "r_multiple", "closed_at", "exit", "exit_price", "return", "size",
    "qty", "quantity", "notional", "leverage", "contracts", "risk_pct",
    "history")


def test_f_b18_positions_example_is_state_only():
    p = ROOT / "ops" / "positions.yaml.example"
    assert p.exists(), "ops/positions.yaml.example is missing"
    text = p.read_text(encoding="utf-8")

    # the ALLOWED five, present in the example
    body = "\n".join(l for l in text.splitlines() if not l.strip().startswith("#"))
    for k in ("symbol", "lens", "direction", "entry", "stop"):
        assert f"{k}:" in body, f"the example does not show {k}"

    # forbidden keys must not appear as YAML KEYS outside comments
    for bad in FORBIDDEN_POSITION_KEYS:
        assert not re.search(rf"^\s*-?\s*{bad}\s*:", body, re.M | re.I), \
            f"forbidden key {bad!r} present in the example"

    # ...but the comment block must NAME them, or the operator is not warned
    assert "NO P&L" in text and "NO OUTCOMES" in text


# --------------------------------------------------------------- F-B19 / F-B32

def test_f_b19_panel_rebuilds_from_captures_alone_with_correct_grain():
    caps = _captures()
    if not caps:
        pytest.skip("no capture in briefs/")
    date = caps[-1].name.split("_")[1]
    tables = BP.build_partition(date)
    assert set(tables) == set(BP.TABLES)
    assert tables["snapshots"], "snapshots rebuilt empty"

    grain = [(r["asset"], r["slot"], r["date"]) for r in tables["snapshots"]]
    assert len(grain) == len(set(grain)), "snapshots grain is not (asset, slot, date)"

    snap_keys = set(grain)
    for t in ("levels", "areas"):
        for r in tables[t]:
            assert (r["asset"], r["slot"], r["date"]) in snap_keys, \
                f"{t} row does not join back to a snapshot"


def test_f_b19_schema_documents_every_column_present():
    caps = _captures()
    if not caps:
        pytest.skip("no capture in briefs/")
    schema = (BRIEFS / "panel" / "SCHEMA.md")
    assert schema.exists(), "briefs/panel/SCHEMA.md is missing"
    text = schema.read_text(encoding="utf-8")
    date = caps[-1].name.split("_")[1]
    tables = BP.build_partition(date)
    missing = []
    for t, rows in tables.items():
        if not rows:
            continue
        for col in rows[0]:
            if f"`{col}`" not in text:
                missing.append(f"{t}.{col}")
    assert not missing, "SCHEMA.md does not document: " + ", ".join(missing)


def test_f_b32_partitions_are_written_once_and_never_rewritten(tmp_path):
    import pandas as pd
    tables = {t: [{"date": "2026-01-01", "slot": "ny_am", "asset": "X"}]
              for t in BP.TABLES}
    first = BP.write_partition("2026-01-01", tables, panel_dir=tmp_path)
    assert len(first["written"]) == 3 and not first["refused_existing"]

    stamps = {p: (tmp_path / p.split("/")[-2] / p.split("/")[-1]).stat().st_mtime
              for p in [f"{t}/2026-01-01.parquet" for t in BP.TABLES]}

    tables2 = {t: [{"date": "2026-01-01", "slot": "ny_am", "asset": "MUTATED"}]
               for t in BP.TABLES}
    second = BP.write_partition("2026-01-01", tables2, panel_dir=tmp_path)
    assert not second["written"], "a partition was rewritten"
    assert len(second["refused_existing"]) == 3

    for rel, mtime in stamps.items():
        p = tmp_path / rel.split("/")[0] / rel.split("/")[1]
        assert p.stat().st_mtime == mtime, f"{rel} was touched"
        assert pd.read_parquet(p)["asset"].iloc[0] == "X", \
            "partition content changed despite write-once"

    # --force exists only to repair a known-bad file
    third = BP.write_partition("2026-01-01", tables2, panel_dir=tmp_path, force=True)
    assert len(third["written"]) == 3


def test_f_b32_real_partitions_exist_and_match_the_capture():
    caps = _captures()
    if not caps:
        pytest.skip("no capture in briefs/")
    import pandas as pd
    date = caps[-1].name.split("_")[1]
    for t in BP.TABLES:
        p = BRIEFS / "panel" / t / f"{date}.parquet"
        if not p.exists():
            pytest.skip(f"partition {t}/{date} not built yet")
        df = pd.read_parquet(p)
        assert len(df) == len(BP.build_partition(date)[t]), \
            f"{t} partition row count differs from a fresh rebuild"


# --------------------------------------------------------------- F-B21

def test_f_b21_backfill_is_refused_without_the_flag_and_stamped_with_it():
    with pytest.raises(SystemExit) as e:
        BC.backfill_guard("2026-01-01", "2026-08-03", backfill=False)
    assert "REFUSED" in str(e.value) and "forward-only" in str(e.value)
    assert "census" in str(e.value).lower(), \
        "the refusal must say where historical work belongs"

    ok = BC.backfill_guard("2026-01-01", "2026-08-03", backfill=True)
    assert ok["backfilled"] is True
    assert ok["marker"]["backfilled"] is True
    assert ok["marker"]["not_taken_live"] is True

    forward = BC.backfill_guard("2026-08-04", "2026-08-03")
    assert forward["backfilled"] is False and forward["marker"] is None
    assert BC.backfill_guard("2026-01-01", None)["allowed"] is True


def test_f_b21_partition_footprint_includes_warmups():
    fp = BC.partition_footprint(1_785_000_000_000, [7, 30, 90, 365], warmup_days=30)
    assert fp["longest_window_days"] == 395
    assert fp["warmup_days_included"] == 30
    assert fp["reads_from_ms"] == 1_785_000_000_000 - 395 * 86_400_000
    assert "lockbox_overlap" in fp


# --------------------------------------------------------------- F-B22

def test_f_b22_schedule_resolves_through_the_zone_not_a_stored_offset():
    """Resolving the slots after 2026-11-01 must give UTC one hour LATER."""
    from datetime import datetime
    from zoneinfo import ZoneInfo
    ny = ZoneInfo("America/New_York")

    def utc_of(y, m, d, hh, mm):
        return datetime(y, m, d, hh, mm, tzinfo=ny).astimezone(ZoneInfo("UTC")).hour

    for local_h in (7, 10, 16):
        edt = utc_of(2026, 8, 3, local_h, 0)
        est = utc_of(2026, 12, 1, local_h, 0)
        assert est == (edt + 1) % 24, (
            f"{local_h}:00 NY resolved to {edt}Z in August and {est}Z in "
            f"December — a stored offset would give the same number twice")

    cfg = (ROOT / "ops" / "brief_schedule.yaml").read_text(encoding="utf-8")
    assert "zone: America/New_York" in cfg
    ps1 = (ROOT / "scripts" / "setup_brief_schedule.ps1").read_text(encoding="utf-8")
    assert "ConvertTimeToUtc" in ps1, "the generator must resolve through the zone"
    assert "IsDaylightSavingTime" in ps1, "the generator must print DST transitions"


# --------------------------------------------------------------- F-B23

def test_f_b23_no_capture_contains_a_bar_series():
    """G12: a capture stores numbers, never a series. A capture that embedded
    OHLCV would be a second copy of the estate inside git."""
    _, doc = _one()
    offenders = []

    def walk(node, trail=""):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, f"{trail}.{k}")
        elif isinstance(node, list):
            nums = [x for x in node if isinstance(x, (int, float))]
            if len(nums) > 60:
                offenders.append(f"{trail} ({len(nums)} numbers)")
            for i, v in enumerate(node[:5]):
                walk(v, f"{trail}[{i}]")

    walk(doc)
    assert not offenders, "bar-series-like arrays in the capture: " + ", ".join(offenders)


# --------------------------------------------------------------- F-B24

def test_f_b24_slot_isolation(tmp_path):
    """Two captures on the same date with different slots coexist."""
    base = B2.capture_envelope("2026-08-03", "london")
    base["generated_utc"] = "2026-08-03T11:00:00Z"
    base["assets"] = {}
    other = B2.capture_envelope("2026-08-03", "post_ny")
    other["generated_utc"] = "2026-08-03T20:30:00Z"
    other["assets"] = {}

    p1, s1, l1 = BC.write_capture(base, briefs_dir=tmp_path)
    p2, s2, l2 = BC.write_capture(other, briefs_dir=tmp_path)
    assert p1 != p2 and p1.exists() and p2.exists()
    assert s1 != s2

    idx = [json.loads(x) for x in
           (tmp_path / "index.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    assert {r["slot"] for r in idx} == {"london", "post_ny"}, \
        "the index must carry both slots"

    # a same-slot re-run refuses rather than overwriting
    with pytest.raises(SystemExit) as e:
        BC.write_capture(base, briefs_dir=tmp_path)
    assert "already exists" in str(e.value)
    BC.write_capture(base, briefs_dir=tmp_path, force=True)   # explicit override


# --------------------------------------------------------------- LIT marking

def test_lit_known_wrong_marks_only_percentile_rank_and_bar_count():
    """v4 §II.11 carried forward. Precision is the point: marking a LEVEL would
    train the reader to ignore markers."""
    for kind in ("percentile", "rank", "bar_count"):
        assert BC.lit_known_wrong("LITUSDT", kind) is True
    for kind in ("level", "volume_weighted", "poc", "vwap"):
        assert BC.lit_known_wrong("LITUSDT", kind) is False, \
            f"{kind} must NOT be marked known-wrong"
    for kind in ("percentile", "rank", "level"):
        assert BC.lit_known_wrong("BTCUSDT", kind) is False


def test_lit_capture_carries_the_marker_scope():
    _, doc = _one()
    lit = doc["assets"].get("LITUSDT")
    if lit is None:
        pytest.skip("LITUSDT not in this capture")
    kw = lit.get("known_wrong")
    assert kw, "LITUSDT capture carries no known-wrong scope"
    assert set(kw["applies_to"]) == {"percentile", "rank", "bar_count"}
    assert "level" in kw["not_marked"]


def test_lit_365d_window_is_warming_in_the_real_capture():
    """F-B30 on real data: 222.4 days of history cannot claim a 365d window."""
    _, doc = _one()
    lit = doc["assets"].get("LITUSDT")
    if lit is None:
        pytest.skip("LITUSDT not in this capture")
    w = lit["volume_windows"]["windows"]["365d"]
    assert w["warming"] is True
    assert w["poc"] is None and w["vah"] is None and w["val"] is None
    rv = lit["rvwap"]["windows"]["365d"]
    assert rv["warming"] is True and rv["vwap"] is None
