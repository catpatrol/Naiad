#!/usr/bin/env python
"""TIER-C10 · STAGE D FIXTURES — F-D-1 .. F-D-3 and the guards around them.

The law of the prove() lineage (rangefinder / oracle fixtures): every fixture
runs BOTH legs, and a fixture whose BREAK leg passes is VOID — a check that
cannot be made to fail is not evidence of anything.  Every leg states inline
what would make it fail ("FAILS IF ...").  Where one guard has several ways to
be wrong, each plant is judged ONE AT A TIME and every plant must go RED.

BANNED HERE (tierc8/9 fixture header, carried): SELF-COMPARISON (F-D-1 and the
attribution leg of F-D-2 ask the VENUE with plain `requests` and share no
parser with engine.data or tierc10_data; F-D-L1 rebuilds the derived lenses
with a plain loop that shares nothing with derive_1d/derive_1w); ONE EXAMPLE
where cardinality was possible (grid, flat-bar recount, funding coverage, sha
re-hash and admission run over EVERY panel file); a TUNED BOUND standing in
for an identity (venue bars must be EQUAL, field for field, not "close").

NOTHING HERE DAMAGES THE SNAPSHOT.  Every sabotage operates on an in-memory
COPY of a frame, a COPY of a file under a TemporaryDirectory, or a COPY of a
source text.  No real artifact is ever the target of a plant.

NETWORK: F-D-1, F-D-1b and F-D-2(d) read the public venue APIs (Binance
USDT-M fapi, Bybit v5 for MNT) one bar at a time, and F-D-1b / F-D-2(d) ask
the venue's OTHER publication too — its bulk archive (data.binance.vision
daily zips) — for EVERY sampled bar, so each bar is named rest-only,
archive-only or both.  `--offline` skips F-D-1 / F-D-1b and the attribution
leg of F-D-2 and reports them NOT RUN (never PASS).

ADDED BY THE REVIEW REPAIR: F-D-SEAL (write-once is code, not a word),
F-D-CLOSURE (importing the data module drags no range machine along), the
funding-hour law inside F-D-3, the edge-only exemption inside F-D-ASOF, and
break legs that judge the PLANTED item ALONE (F-D-1's old break was RED on
the real leg's own mismatches whether or not it saw the plant).

F-D-1 IS KEPT CONTRACT-LITERAL ("vs the venue API ... FAILS IF any OHLCV field
differs") even though the first run found the venue's two publications
disagree on incident bars: a fixture whose claim was re-cut after the result
to make it pass would be a check whose CLAIM is not the design's claim.
F-D-1b is the separate, ADDED claim (every sampled bar is field-equal to at
least ONE of the venue's own two publications; no REST-sourced row differs
from REST at all; and the manifest's per-file publication label agrees with
what the venue answers) — it attributes the difference, it does not excuse
F-D-1.  REPAIRED after review: the first filing claimed "pre-existing files
carry the ARCHIVE's bar"; the review measured REST for the classics.  The
label is now MEASURED both ways and this fixture holds it to the venue.

Run:  NAIAD_CACHE_DIR=~/.cache/naiad/snapshots/tc10_20260921 \\
        ~/venvs/naiad/bin/python scripts/tierc10_data_fixtures.py [--offline] [leg ...]
Exit: 0 if every fixture is green on REAL and red on BREAK; 1 otherwise.
"""
from __future__ import annotations

import ast
import copy
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc10_data as D                       # noqa: E402  (runs the substrate guard first)

import numpy as np                             # noqa: E402
import pandas as pd                            # noqa: E402
import requests                                # noqa: E402

SEED = D.SEED
PY = str(Path.home() / "venvs" / "naiad" / "bin" / "python")

FAILED: list[str] = []
PASSED: list[str] = []
NOT_RUN: list[str] = []
T: list[str] = []


def say(msg: str = "") -> None:
    print(msg, flush=True)
    T.append(msg)


def prove(fixture: str, title: str, break_leg, real_leg) -> None:
    say(f"\n{fixture} — {title}")
    b_ok, b_detail = break_leg()
    say(f"  [BREAK] deliberate violation -> "
        f"{'RED (correct)' if not b_ok else 'GREEN (FIXTURE IS VOID)'}: {b_detail}")
    r_ok, r_detail = real_leg()
    say(f"  [{'PASS' if r_ok else 'FAIL'}] {fixture}: {r_detail}")
    if b_ok:
        FAILED.append(f"{fixture} (break leg passed — fixture proves nothing)")
    elif not r_ok:
        FAILED.append(fixture)
    else:
        PASSED.append(fixture)


def plants(results: list[tuple[str, bool, str]]) -> tuple[bool, str]:
    """One plant per guard, judged ONE AT A TIME.  The break leg is RED only
    if EVERY plant was caught; a single plant that passes voids the fixture."""
    green = [n for n, ok, _ in results if ok]
    detail = " · ".join(f"{n}: {'GREEN(!)' if ok else 'red'} ({d})" for n, ok, d in results)
    return bool(green), detail


MAN = D.load_manifest()
PIN = D.load_pin()
CLOSE_MS = int(PIN["as_of_last_closed_4h_close_ms"])
PRE = json.loads((D.OUT / "PRE_STATE.json").read_text())
PANEL = list(MAN["panels"]["PANEL17_stems"])
VENUE = {v["stem"]: v for v in MAN["venues"] if v["stem"]}
ALL_IVS = D.NATIVE_IVS + D.DERIVED_IVS


# ══════════════════════════ the venue, asked directly (zero shared code)
_VENUE_MEMO: dict = {}


def venue_bar(stem: str, iv: str, open_ms: int) -> list | None:
    """ONE native bar straight from the venue of record: [open_ms, o, h, l, c, v]
    as the venue's own strings, or None if the venue serves no bar there."""
    key = (stem, iv, int(open_ms))
    if key in _VENUE_MEMO:
        return _VENUE_MEMO[key]
    v = VENUE[stem]
    for attempt in range(5):
        try:
            if v["venue"] == "BINANCE_USDTM":
                r = requests.get("https://fapi.binance.com/fapi/v1/klines",
                                 params={"symbol": v["symbol"], "interval": iv,
                                         "startTime": int(open_ms), "endTime": int(open_ms),
                                         "limit": 1}, timeout=30)
                if r.status_code != 200:
                    raise RuntimeError(f"HTTP {r.status_code}")
                rows = r.json()
            else:
                r = requests.get("https://api.bybit.com/v5/market/kline",
                                 params={"category": "linear", "symbol": v["symbol"],
                                         "interval": D.BYBIT_IV[iv], "start": int(open_ms),
                                         "end": int(open_ms), "limit": 1}, timeout=30)
                j = r.json()
                if r.status_code != 200 or j.get("retCode") != 0:
                    raise RuntimeError(f"HTTP {r.status_code} retCode {j.get('retCode')}")
                rows = j["result"]["list"]
            out = None
            for row in rows:
                if int(row[0]) == int(open_ms):
                    out = [int(row[0])] + [str(x) for x in row[1:6]]
            _VENUE_MEMO[key] = out
            time.sleep(0.12)
            return out
        except (requests.RequestException, RuntimeError, ValueError) as e:
            last = e
            time.sleep(3.0 * (attempt + 1))
    raise RuntimeError(f"venue unreachable for {key}: {last!r}")


def bar_equal(cached: dict, venue: list | None) -> tuple[bool, str]:
    """EQUAL, field for field: float(venue string) == cached float64."""
    if venue is None:
        return False, "venue serves NO bar at this stamp"
    bad = [f"{k}: cache {cached[k]!r} != venue {venue[i]}"
           for i, k in enumerate(D.KLINE_COLS[1:], 1) if float(venue[i]) != float(cached[k])]
    return (not bad), "; ".join(bad)


_ARCHIVE_MEMO: dict = {}


def archive_bar(stem: str, iv: str, open_ms: int, monthly: bool = False) -> list | None:
    """The SAME native bar from the venue's OTHER publication: the bulk archive
    (data.binance.vision) — its DAILY zip by default, its MONTHLY zip on
    request (the two forms disagree with each other on a few BTC incident
    bars; the estate's backfill and the whole-history census read the monthly
    one).  Parsed here with the csv module — zero shared code with
    engine.data.  None if the venue publishes no archive for that day / month
    (or the venue is not Binance)."""
    import csv
    import io
    import zipfile
    v = VENUE[stem]
    if v["venue"] != "BINANCE_USDTM":
        return None
    day = time.strftime("%Y-%m" if monthly else "%Y-%m-%d", time.gmtime(int(open_ms) // 1000))
    key = (v["symbol"], iv, day)
    if key not in _ARCHIVE_MEMO:
        url = (f"https://data.binance.vision/data/futures/um/{'monthly' if monthly else 'daily'}/klines/"
               f"{v['symbol']}/{iv}/{v['symbol']}-{iv}-{day}.zip")
        rows, last = None, None
        for attempt in range(5):
            try:
                r = requests.get(url, timeout=60)
                if r.status_code == 404:
                    rows = {}
                    break
                if r.status_code != 200:
                    raise RuntimeError(f"HTTP {r.status_code}")
                with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                    text = z.read(z.namelist()[0]).decode("utf-8")
                rows = {}
                for rec in csv.reader(io.StringIO(text)):
                    if rec and rec[0].isdigit():
                        ts = int(rec[0])
                        ts = ts // 1000 if ts > 10_000_000_000_000_000 else ts
                        rows[ts] = [ts] + rec[1:6]
                break
            except (requests.RequestException, RuntimeError, zipfile.BadZipFile) as e:
                last = e
                time.sleep(3.0 * (attempt + 1))
        if rows is None:
            raise RuntimeError(f"archive unreachable for {key}: {last!r}")
        _ARCHIVE_MEMO[key] = rows
    return _ARCHIVE_MEMO[key].get(int(open_ms))


def rest_sourced(stem: str, iv: str, open_ms: int) -> bool:
    """True if TC10 itself fetched this row over REST (the file did not exist
    before TC10, or the row lies past the file's PRE_STATE edge)."""
    was = PRE["files"].get(f"klines/{stem}_{iv}.parquet")
    return was is None or int(open_ms) > int(was["last_ms"])


def venue_published(stem: str, iv: str, cached: dict, open_ms: int) -> tuple[bool, str]:
    """A cached bar is the VENUE's if it is field-equal to the venue's REST bar
    or to its BULK ARCHIVE bar.  BOTH publications are asked for EVERY bar, so
    the answer names which one(s) the cache carries.  A row TC10 fetched over
    REST gets NO archive fallback.  Returns (ok, kind) with kind one of
      'both' · 'rest' (the archive publishes no bar there) ·
      'rest-only: ARCHIVE differs (...)' · 'archive-only: REST differs (...)' · why-not."""
    ok, d = bar_equal(cached, venue_bar(stem, iv, open_ms))
    if not ok and rest_sourced(stem, iv, open_ms):
        return False, f"REST-sourced row differs from REST: {d}"
    arch = archive_bar(stem, iv, open_ms)
    ok_a, d_a = bar_equal(cached, arch) if arch is not None else (False, "archive publishes NO bar here")
    if ok and ok_a:
        return True, "both"
    if ok:
        return True, "rest" if arch is None else f"rest-only: ARCHIVE differs ({d_a})"
    if ok_a:
        return True, f"archive-only: REST differs ({d})"
    arch_m = archive_bar(stem, iv, open_ms, monthly=True)      # the archive's OTHER form, asked LAST
    if arch_m is not None and bar_equal(cached, arch_m)[0]:
        return True, f"archive-only: the MONTHLY zip only — REST differs ({d}) · DAILY zip differs ({d_a})"
    return False, f"equal to NEITHER venue publication — REST: {d} · ARCHIVE (daily and monthly): {d_a}"


# ══════════════════════════════════ F-D-0 · THE SUBSTRATE GUARD
def _guard(env_value: str | None) -> tuple[bool, str]:
    env = {k: v for k, v in os.environ.items() if k != "NAIAD_CACHE_DIR"}
    if env_value is not None:
        env["NAIAD_CACHE_DIR"] = env_value
    p = subprocess.run([PY, "-c", "import sys; sys.path.insert(0, 'scripts'); "
                                  "import tierc10_data as D; print('IMPORTED', D.SNAPSHOT)"],
                       cwd=ROOT, env=env, capture_output=True, text=True, timeout=120)
    ok = p.returncode == 0 and "IMPORTED" in p.stdout
    return ok, (p.stdout.strip() or p.stderr.strip().splitlines()[-1])[:160]


def fd0_break():
    return plants([("live cache", *_guard(str(D.LIVE_CACHE))),
                   ("env unset", *_guard(None)),
                   ("some other dir", *_guard(tempfile.gettempdir()))])


def fd0_real():
    ok, d = _guard(str(D.SNAPSHOT))
    same = Path(os.environ["NAIAD_CACHE_DIR"]).resolve() == D.SNAPSHOT.resolve() \
        and D.ED.cache_dir().resolve() == D.SNAPSHOT.resolve()
    return ok and same, (f"module imports ONLY under the snapshot; engine.data.cache_dir() == "
                         f"{D.ED.cache_dir()}.  FAILS IF the module imports with NAIAD_CACHE_DIR "
                         f"unset, == the live cache, or == any other directory (the guard HALTs "
                         f"before engine.data is imported, so the live cache is never even stat'd)")


# ══════════════════════════════════ F-D-1 · BARS vs THE VENUE, native-vs-native
INCIDENT_DAYS_MS = [1_730_073_600_000, 1_699_574_400_000, 1_653_696_000_000]   # 2024-10-28, 2023-11-10, 2022-05-28
INCIDENT_4H_MS = 1_730_145_600_000            # 2024-10-28T20:00Z — every asset's venue intervals disagree here
FD1_ASSETS = ("SUIUSDT", "MNTUSDT_BYBIT", "XMRUSDT")   # new fetch · non-default venue · incident-adjacent


def _fd1_samples() -> list[tuple[str, str, int, str]]:
    rng = np.random.default_rng(SEED)
    out = []
    for stem in FD1_ASSETS:
        if stem not in PANEL:
            continue
        for iv in D.NATIVE_IVS:
            t = D.load_asof(stem, iv)["open_time"].to_numpy(np.int64)
            day = t // D.DAY_MS * D.DAY_MS
            calm = t[~np.isin(day, INCIDENT_DAYS_MS)]
            picks = sorted(set(int(x) for x in rng.choice(calm[1:-1], size=3, replace=False)))
            out += [(stem, iv, int(t[0]), "first bar"), (stem, iv, int(t[-1]), "last as-of bar")]
            out += [(stem, iv, p, "seeded, off-incident") for p in picks]
    if "XMRUSDT" in PANEL:
        out += [("XMRUSDT", "4h", INCIDENT_4H_MS - D.MS_4H, "incident-ADJACENT (the bar before)"),
                ("XMRUSDT", "4h", INCIDENT_4H_MS, "THE incident bar 2024-10-28T20:00Z"),
                ("XMRUSDT", "4h", INCIDENT_4H_MS + D.MS_4H, "incident-ADJACENT (the bar after)"),
                ("XMRUSDT", "1h", INCIDENT_4H_MS, "incident hour (venue zero-volume flat)"),
                ("XMRUSDT", "5m", INCIDENT_4H_MS, "incident 5m")]
    return out


def _fd1(perturb: bool) -> tuple[bool, str]:
    samples = _fd1_samples()
    frames: dict = {}
    bad, n = [], 0
    if perturb:
        # The plant is judged ALONE.  The real leg has mismatches of its own (the
        # venue's publications disagree), so "any sample differs" would be RED
        # whether or not the plant was seen: the verdict is the PLANTED bar's.
        for stem, iv, t, _ in samples:
            row = D.load_asof(stem, iv).set_index("open_time").loc[t].to_dict()   # a COPY
            if not bar_equal(row, venue_bar(stem, iv, t))[0]:
                continue                        # a bar already differing proves nothing about a plant
            row["close"] = float(np.nextafter(row["close"], np.inf))   # one ULP — far under a tick
            ok, d = bar_equal(row, venue_bar(stem, iv, t))
            return ok, (f"{stem} {iv} {D.iso(t)} is EQUAL to the venue untouched; its close moved by ONE "
                        f"ULP in a COPY, judged ALONE -> {'NOT DETECTED' if ok else 'DIFFERS: ' + d}")
        return True, "no sampled bar equals the venue, so nothing could be planted on — VOID"
    for k, (stem, iv, t, why) in enumerate(samples):
        if (stem, iv) not in frames:
            frames[(stem, iv)] = D.load_asof(stem, iv).set_index("open_time")
        row = frames[(stem, iv)].loc[t].to_dict()          # a COPY of the cached row
        ok, d = bar_equal(row, venue_bar(stem, iv, t))
        n += 1
        say(f"      {'[OK ]' if ok else '[BAD]'} {stem:14s} {iv:3s} {D.iso(t)}  {why}"
            f"{'' if ok else '  ' + d}")
        if not ok:
            bad.append(f"{stem} {iv} {D.iso(t)}: {d}")
    if "XMRUSDT" in PANEL:
        f4 = frames[("XMRUSDT", "4h")].loc[INCIDENT_4H_MS]
        h1 = frames[("XMRUSDT", "1h")]
        kids = h1[(h1.index >= INCIDENT_4H_MS) & (h1.index < INCIDENT_4H_MS + D.MS_4H)]
        say(f"      THE VENUE'S OWN INTERVALS DISAGREE on the incident bar (printed, not asserted): "
            f"XMR native 4h open {f4['open']} low {f4['low']} vol {f4['volume']} · its "
            f"{len(kids)} native 1h children: open {kids['open'].iloc[0]} low {kids['low'].min()} "
            f"vol {kids['volume'].sum():.3f} — which is why F-D-1 compares SAME-interval only and "
            f"why 1d/1w derive from native 4h alone [LEAN L1]")
    assets = sorted({s[0] for s in samples})
    FD1_BAD[:] = bad
    return (not bad and len(assets) == 3), (
        f"{n} bars x {len(assets)} assets {assets} x lenses {list(D.NATIVE_IVS)}: every O,H,L,C,V "
        f"EQUAL to the venue's own native bar at the SAME interval ({len(bad)} differ)."
        f"  FAILS IF any OHLCV field of any sampled bar differs from the venue, the venue serves "
        f"no bar at a cached stamp, or fewer than three assets could be checked"
        + (f".  DIFFERING: {bad} — the manifest's MEASURED publication label of each differing file: "
           f"{ {b.split(':')[0].rsplit(' ', 1)[0]: _labels(MAN).get(tuple(b.split(' ')[:2])) for b in bad} }"
           f" (a file that carries the venue's ARCHIVE bar cannot equal its REST API on an incident stamp; "
           f"attribution is F-D-1b's claim, not this one's, and THIS leg stays RED until the operator rules "
           f"which publication is the record)" if bad else ""))


# ══════════════════════════════════ F-D-1b · WHERE THE PUBLICATIONS DIFFER, WHOSE BAR IS IT?
WHOLE_LIST_IVS = ("4h", "12h")                 # every listed stamp; other lenses a seeded three per entry
LABEL_FORBIDS = {"REST": "archive-only", "ARCHIVE": "rest-only"}


def _labels(man: dict) -> dict[tuple[str, str], str]:
    vd = man.get("venue_publications_disagree") or {}
    out = {}
    for path, c in vd.get("carries", {}).items():
        stem, _, iv = path[len("klines/"):-len(".parquet")].rpartition("_")
        out[(stem, iv)] = c["carries"]
    return out


def _fd1b_todo() -> list[tuple[str, str, int]]:
    """Every F-D-1 sample, plus EVERY 4h/12h stamp EITHER whole-history census
    lists as differing (cardinality where possible), plus a seeded three per
    audited 1h / 5m entry of either census."""
    rng = np.random.default_rng(SEED + 1)
    todo = [(s, iv, t) for s, iv, t, _ in _fd1_samples()]
    for name in (D.REST_AUDIT, D.ARCHIVE_AUDIT):
        ap = D.OUT / name
        aud = json.loads(ap.read_text())["entries"] if ap.exists() else {}
        for key in sorted(aud):
            e = aud[key]
            stamps = sorted(set(e["price_mismatch_stamps"] + e["volume_only_mismatch_stamps"]
                                + e.get("only_in_snapshot_stamps", [])))
            ms = [int(pd.Timestamp(x).value // 1_000_000) for x in stamps]
            if e["as_of_lens"] not in WHOLE_LIST_IVS and len(ms) > 3:
                ms = sorted(int(x) for x in rng.choice(ms, size=3, replace=False))
            todo += [(e["stem"], e["as_of_lens"], t) for t in ms]
    return sorted(set(todo))


def _fd1b(perturb: bool, labels: dict | None = None) -> tuple[bool, str]:
    """Each sampled bar must be the venue's by venue_published() — asked of BOTH
    publications with parsers that share nothing with engine.data — and the
    manifest's MEASURED label for its file must not be contradicted by it."""
    labels = _labels(MAN) if labels is None else labels
    todo = _fd1b_todo()
    frames, bad, kinds, wrong_label, hit = {}, [], {}, [], []
    for stem, iv, t in todo:
        if (stem, iv) not in frames:
            frames[(stem, iv)] = D.load_asof(stem, iv).set_index("open_time")
        row = frames[(stem, iv)].loc[t].to_dict()
        if perturb and (stem, iv, t) == PERTURB_AT.get("key"):
            row["close"] = float(np.nextafter(row["close"], np.inf))
        ok, d = venue_published(stem, iv, row, t)
        kind = d.split(":")[0] if ok else "neither"
        kinds.setdefault(kind, []).append(f"{stem} {iv} {D.iso(t)}")
        if not ok:
            bad.append(f"{stem} {iv} {D.iso(t)}: {d}")
            if (stem, iv, t) == PERTURB_AT.get("key"):
                hit.append(bad[-1])
        lab = labels.get((stem, iv))
        if lab is None:
            wrong_label.append(f"{stem} {iv}: NO publication label in the manifest")
        elif kind == LABEL_FORBIDS.get(lab) or (lab == "BOTH" and kind in ("rest-only", "archive-only")):
            wrong_label.append(f"{stem} {iv} {D.iso(t)}: manifest says {lab}, the venue says {kind}")
            if (stem, iv) == PERTURB_AT.get("label"):
                hit.append(wrong_label[-1])
    if perturb:                                 # the PLANTED item, judged ALONE
        return (not hit), (f"{hit[0][:230] if hit else 'NOT DETECTED'}"
                           f"  (whole run: {len(bad)} neither, {len(wrong_label)} label contradictions)")
    for name in (D.REST_AUDIT, D.ARCHIVE_AUDIT):
        ap = D.OUT / name
        aud = json.loads(ap.read_text())["entries"] if ap.exists() else {}
        tot = {iv: [sum(e[k] for e in aud.values() if e["as_of_lens"] == iv) for k in
                    ("bars_compared", "price_mismatch", "volume_only_mismatch", "only_in_snapshot")]
               for iv in sorted({e["as_of_lens"] for e in aud.values()})}
        say(f"      WHOLE-HISTORY CENSUS {name} ({len(aud)} entries; per lens: compared, price-mismatch, "
            f"volume-only, publication-lacks-the-bar): {tot}")
    for kind in ("rest-only", "archive-only"):
        for x in kinds.get(kind, []):
            say(f"      [{kind.upper()}] {x}")
    by_pub = (MAN.get("venue_publications_disagree") or {}).get("panel_by_publication", {})
    say(f"      MANIFEST LABELS, 4h: {by_pub.get('4h')}")
    rest_src_bad = [b for b in bad if "REST-sourced" in b]
    n = {k: len(v) for k, v in sorted(kinds.items())}
    return (not bad and not wrong_label), (
        f"{len(todo)} bars asked of BOTH venue publications: {n} — every bar is field-equal to at least "
        f"one of them (equal to NEITHER: {len(bad)}; REST-sourced rows differing from REST: "
        f"{len(rest_src_bad)}), and no file's MEASURED publication label is contradicted by a sampled bar "
        f"({len(wrong_label)} contradictions{': ' + str(wrong_label[:2]) if wrong_label else ''}).  THE PANEL "
        f"IS PUBLICATION-HETEROGENEOUS — Naiad changed nothing; the record is the operator's ruling."
        f"  FAILS IF any bar is equal to neither venue publication, a row TC10 itself fetched over REST "
        f"differs from REST (no archive fallback there), a sampled file has no label, or a file labelled "
        f"REST / ARCHIVE / BOTH holds a bar only the OTHER publication carries")


PERTURB_AT: dict = {}
FD1_BAD: list[str] = []


def fd1b_break():
    res = []
    todo = _fd1b_todo()
    PERTURB_AT["key"] = next((x for x in todo if x == ("XMRUSDT", "1h", INCIDENT_4H_MS)), todo[0])
    ok, d = _fd1b(True)
    res.append(("an ARCHIVE-ONLY bar moved one ULP in a COPY (equal to neither now)", ok, d))
    PERTURB_AT["key"] = next(x for x in todo if rest_sourced(*x))
    ok, d = _fd1b(True)
    res.append(("a REST-sourced bar moved one ULP in a COPY (no archive fallback)", ok, d))
    PERTURB_AT.clear()
    lab = dict(_labels(MAN))
    flip = {"ARCHIVE": "REST", "REST": "ARCHIVE"}
    victim = next((k for k in sorted(lab) if lab[k] in flip and k[1] == "4h"), None)
    if victim is None:
        res.append(("a file's publication label flipped (COPY of the manifest)", True,
                    "no REST- or ARCHIVE-labelled 4h file to flip — VOID"))
    else:
        lab[victim] = flip[lab[victim]]
        PERTURB_AT["label"] = victim
        ok, d = _fd1b(True, lab)
        PERTURB_AT.clear()
        res.append((f"{victim[0]} 4h label flipped to {lab[victim]} in a COPY of the manifest — the first "
                    f"filing's false provenance, replayed", ok, d))
    return plants(res)


# ══════════════════════════════════ F-D-2 · NO SYNTHETIC BARS (Naiad inserted none)
BANNED_TOKENS = ("ffill", "bfill", "fillna", "interpolate", "reindex", "resample", "asfreq", ".pad(")
FETCH_PATH_SOURCES = (ROOT / "engine" / "data.py", ROOT / "scripts" / "tierc10_data.py")


def code_only(src: str) -> str:
    """AST round-trip: comments gone, docstrings stripped, string literals KEPT
    (tierc4_fixtures.code_only idiom)."""
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            b = node.body
            if b and isinstance(b[0], ast.Expr) and isinstance(getattr(b[0], "value", None), ast.Constant) \
                    and isinstance(b[0].value.value, str):
                node.body = b[1:] or [ast.Pass()]
    return ast.unparse(tree)


def _token_scan(sources: dict[str, str]) -> list[str]:
    hits = []
    for name, src in sources.items():
        code = code_only(src)
        hits += [f"{name}: '{tok}'" for tok in BANNED_TOKENS if tok in code]
    return hits


def _grid_faults(df: pd.DataFrame, iv: str) -> list[str]:
    """Independent of D.scan_klines: plain diff/mod on the stamps."""
    t = df["open_time"].to_numpy(np.int64)
    step, anchor = D.STEP_MS[iv], D.GRID_ANCHOR_MS.get(iv, 0)
    out = []
    if ((t - anchor) % step != 0).any():
        out.append(f"{int(((t - anchor) % step != 0).sum())} off-grid")
    if len(t) > 1 and (np.diff(t) <= 0).any():
        out.append(f"{int((np.diff(t) <= 0).sum())} duplicate/backward")
    return out


def _flat0(df: pd.DataFrame) -> np.ndarray:
    o, h, l, c, v = (df[k].to_numpy(np.float64) for k in D.KLINE_COLS[1:])
    return (o == h) & (h == l) & (l == c) & (v == 0)


ARCHIVE_ONLY: list[str] = []


def _attributed(stem: str, iv: str, df: pd.DataFrame, stamps: list[int]) -> list[str]:
    """Every listed bar must be the VENUE's: published natively, field-equal,
    by its REST API or (archive-assembled rows only) by its bulk archive."""
    ix = df.set_index("open_time")
    bad = []
    for t in stamps:
        ok, d = venue_published(stem, iv, ix.loc[t].to_dict(), t)
        if not ok:
            bad.append(f"{stem} {iv} {D.iso(t)}: {d}")
        elif d.startswith("archive-only"):
            ARCHIVE_ONLY.append(f"{stem} {iv} {D.iso(t)}")
    return bad


def fd2_break():
    res = []
    f = D.load_asof("BTCUSDT", "1h")                                   # COPIES from here on
    a = pd.concat([f, f.iloc[[100]].assign(open_time=f["open_time"].iloc[100] + 1_800_000)])
    a = a.sort_values("open_time")
    g = _grid_faults(a, "1h")
    res.append(("off-grid bar planted in a COPY", not g, f"grid leg: {g or 'NOT DETECTED'}"))
    if not OFFLINE:
        b = f.copy()
        k = len(b) // 2
        t_k, prev_c = int(b["open_time"].iloc[k]), float(b["close"].iloc[k - 1])
        b.loc[b.index[k], ["open", "high", "low", "close", "volume"]] = [prev_c] * 4 + [0.0]
        bad = _attributed("BTCUSDT", "1h", b, [t_k])
        res.append(("carried-forward flat bar planted over a real bar in a COPY", not bad,
                    f"attribution leg: {bad[0] if bad else 'NOT DETECTED'}"))
        c = D.load_asof("SUIUSDT", "4h") if "SUIUSDT" in PANEL else D.load_asof("ENAUSDT", "4h")
        stem_c = "SUIUSDT" if "SUIUSDT" in PANEL else "ENAUSDT"
        t_pre = int(c["open_time"].iloc[0]) - D.MS_4H
        c2 = pd.concat([c.iloc[[0]].assign(open_time=t_pre), c]).reset_index(drop=True)
        bad = _attributed(stem_c, "4h", c2, [t_pre])
        res.append(("manufactured bar planted BEFORE the venue's first bar in a COPY", not bad,
                    f"attribution leg: {bad[0] if bad else 'NOT DETECTED'}"))
    src = {p.name: p.read_text(encoding="utf-8") for p in FETCH_PATH_SOURCES}
    src["tierc10_data.py"] += "\n\ndef _planted(df):\n    return df.ffill()\n"
    hits = _token_scan(src)
    res.append(("fill token planted in a COPY of the fetch-path source", not hits,
                f"token leg: {hits or 'NOT DETECTED'}"))
    return plants(res)


def fd2_real():
    ARCHIVE_ONLY.clear()
    faults, flat_rows, mism, attributed_bad, n_attr = [], [], [], [], 0
    rng = np.random.default_rng(SEED)
    by_path = {f["path"]: f for f in MAN["files"]}
    for stem in PANEL:
        for iv in ALL_IVS:
            df = pd.read_parquet(D.kline_path(stem, iv))
            g = _grid_faults(df, iv)
            if g:
                faults.append(f"{stem} {iv}: {g}")
            z = _flat0(df)
            filed = by_path[f"klines/{stem}_{iv}.parquet"]["venue_zero_volume_flat_bars"]
            if int(z.sum()) != filed:
                mism.append(f"{stem} {iv}: recount {int(z.sum())} != manifest {filed}")
            if iv in D.NATIVE_IVS:
                flat_rows.append((stem, iv, int(z.sum()), len(df)))
            if iv == "5m" and z.any() and not OFFLINE:
                t = df["open_time"].to_numpy(np.int64)[z]
                pick = [int(x) for x in rng.choice(t, size=min(2, len(t)), replace=False)]
                attributed_bad += _attributed(stem, iv, df, pick)
                n_attr += len(pick)
    hits = _token_scan({p.name: p.read_text(encoding="utf-8") for p in FETCH_PATH_SOURCES})
    say("      venue zero-volume FLAT bars, COUNTED and attributed to the venue (never removed, "
        "never made):")
    for iv in D.NATIVE_IVS:
        say(f"        {iv:3s} " + " · ".join(f"{s.replace('USDT', '')} {n}" for s, i, n, _ in flat_rows if i == iv))
    ok = not faults and not mism and not hits and not attributed_bad
    attr = ("attribution leg NOT RUN (--offline)" if OFFLINE else
            f"{n_attr} seeded 5m flat bars re-asked of the venue: {len(attributed_bad)} not the venue's "
            f"({attributed_bad[:2]}); {len(ARCHIVE_ONLY)} of them are flat ONLY in the venue's bulk archive "
            f"(REST serves a traded bar there now): {ARCHIVE_ONLY}")
    return ok, (f"{len(PANEL)} assets x {len(ALL_IVS)} lenses: grid faults {faults or 0}; flat-bar "
                f"recount vs manifest {mism or 'identical'}; fill tokens in the fetch path "
                f"{hits or 'none'} (scanned: {[p.name for p in FETCH_PATH_SOURCES]}, code only); {attr}."
                f"  THE CLAIM IS 'Naiad inserted no bar', NOT 'the venue published no flat bar' "
                f"(it did — counted above).  FAILS IF any open_time is off its lens grid, duplicated "
                f"or backward; a fill/interpolate token appears in the fetch-path code; a recount "
                f"of flat bars differs from the manifest; or a sampled flat bar is not published, "
                f"field-equal, by the venue itself (REST, or for archive-assembled rows its bulk archive)")


# ══════════════════════════════════ F-D-L1 · THE DERIVED LENSES (independent rebuild)
def _l1_rebuild(f4: pd.DataFrame) -> tuple[list, list]:
    """Plain loops, zero shared code with derive_1d / derive_1w."""
    rows = [tuple(r) for r in f4[D.KLINE_COLS].itertuples(index=False)]
    days: dict[int, list] = {}
    for r in rows:
        days.setdefault(int(r[0]) // 86_400_000, []).append(r)
    d1 = []
    for day in sorted(days):
        b = sorted(days[day])
        if [int(x[0]) for x in b] == [day * 86_400_000 + k * 14_400_000 for k in range(6)]:
            d1.append((day * 86_400_000, b[0][1], max(x[2] for x in b), min(x[3] for x in b),
                       b[-1][4], float(np.sum([x[5] for x in b]))))
    have = {r[0]: r for r in d1}
    w1 = []
    monday = 4 * 86_400_000                       # 1970-01-05
    if d1:
        t = monday + ((d1[0][0] - monday) // 604_800_000) * 604_800_000
        while t <= d1[-1][0]:
            wk = [have.get(t + k * 86_400_000) for k in range(7)]
            if all(x is not None for x in wk):
                w1.append((t, wk[0][1], max(x[2] for x in wk), min(x[3] for x in wk),
                           wk[-1][4], float(np.sum([x[5] for x in wk]))))
            t += 604_800_000
    return d1, w1


def _l1_same(filed: pd.DataFrame, rebuilt: list) -> str:
    got = [tuple(r) for r in filed[D.KLINE_COLS].itertuples(index=False)]
    if len(got) != len(rebuilt):
        return f"rows {len(got)} != rebuilt {len(rebuilt)}"
    for a, b in zip(got, rebuilt):
        if int(a[0]) != int(b[0]) or any(float(x) != float(y) for x, y in zip(a[1:5], b[1:5])) \
                or not np.isclose(a[5], b[5], rtol=1e-12, atol=0.0):
            return f"first difference at {D.iso(b[0])}: filed {a} rebuilt {b}"
    return ""


def fdl1_break():
    f4 = D.load_asof("BTCUSDT", "4h")
    d_ok, w_ok = _l1_rebuild(f4)
    hole = f4.drop(f4.index[len(f4) // 2])                      # a COPY with one 4h bar missing
    sloppy_d, _ = D.derive_1d(f4)
    why1 = _l1_same(sloppy_d, _l1_rebuild(hole)[0])             # filed-from-whole vs a holed tape
    day = hole["open_time"] // D.DAY_MS
    g = hole.groupby(day).agg(open=("open", "first"), high=("high", "max"), low=("low", "min"),
                              close=("close", "last"), volume=("volume", "sum"))
    kept5 = pd.DataFrame({"open_time": g.index.to_numpy(np.int64) * D.DAY_MS, **{
        k: g[k].to_numpy() for k in ("open", "high", "low", "close", "volume")}})
    why2 = _l1_same(kept5, _l1_rebuild(hole)[0])                # a derivation that KEEPS the 5-bar day
    d1, _ = D.derive_1d(f4)
    thu = d1.groupby(d1["open_time"] // D.WEEK_MS).agg(
        n=("open_time", "size"), open=("open", "first"), high=("high", "max"), low=("low", "min"),
        close=("close", "last"), volume=("volume", "sum"))
    thu = thu[thu["n"] == 7]
    thu_w = pd.DataFrame({"open_time": thu.index.to_numpy(np.int64) * D.WEEK_MS, **{
        k: thu[k].to_numpy() for k in ("open", "high", "low", "close", "volume")}})
    why3 = _l1_same(thu_w, w_ok)                                # THURSDAY-anchored weeks
    return plants([("1d filed from a tape the rebuild sees holed", not why1, why1 or "NOT DETECTED"),
                   ("1d that KEEPS an incomplete (5-bar) day", not why2, why2 or "NOT DETECTED"),
                   ("1w anchored on the epoch (Thursday), not Monday", not why3, why3 or "NOT DETECTED")])


def fdl1_real():
    bad, n_d, n_w = [], 0, 0
    for stem in PANEL:
        d_re, w_re = _l1_rebuild(D.load_asof(stem, "4h"))
        d_f, w_f = pd.read_parquet(D.kline_path(stem, "1d")), pd.read_parquet(D.kline_path(stem, "1w"))
        for iv, filed, re_ in (("1d", d_f, d_re), ("1w", w_f, w_re)):
            why = _l1_same(filed, re_)
            if why:
                bad.append(f"{stem} {iv}: {why}")
        wd = pd.to_datetime(w_f["open_time"], unit="ms", utc=True).dt.dayofweek
        if len(w_f) and (wd != 0).any():
            bad.append(f"{stem} 1w: {int((wd != 0).sum())} weeks do not open on a Monday")
        n_d, n_w = n_d + len(d_f), n_w + len(w_f)
    return (not bad), (f"{len(PANEL)} assets: {n_d} filed days and {n_w} filed weeks EQUAL an independent "
                       f"plain-loop rebuild from native 4h closed as-of (stamps and O,H,L,C exact; volume "
                       f"to summation order); every week opens Monday 00:00Z: {bad or 'no difference'}."
                       f"  FAILS IF a filed 1d bar lacks any of its six native 4h children, a filed 1w "
                       f"lacks any of its seven complete days, a week is not Monday-anchored, or any "
                       f"value differs from the rebuild")


# ══════════════════════════════════ F-D-3 · FUNDING COVERAGE
def _fd3(root: Path | None, funding_dir_for_tb: Path | None = None) -> tuple[bool, str, list[str]]:
    import tierc2_baseline as TB
    lines, bad = [], []
    old = TB.FUNDING
    try:
        if funding_dir_for_tb is not None:
            TB.FUNDING = funding_dir_for_tb
        for stem in PANEL:
            cov = D.funding_coverage(stem, CLOSE_MS, root)
            lf = TB.load_funding(stem)
            if not cov["ok"]:
                bad.append(f"{stem}: {cov['why']}")
            if not lf:
                bad.append(f"{stem}: tierc2_baseline.load_funding returned {{}} — zero funding, silently")
            lines.append(f"      {'[OK ]' if cov['ok'] and lf else '[BAD]'} {stem:16s} rows {cov.get('rows')} "
                         f"{cov.get('first')} -> {cov.get('last')}  tail grid {cov.get('interval_hours_tail')}h "
                         f"floor {cov.get('floor')}  load_funding keys {len(lf)}")
    finally:
        TB.FUNDING = old
    return (not bad), "; ".join(bad), lines


def _hour_faults(d: pd.DataFrame, what: str) -> list[str]:
    """LEAN D-g, re-measured with plain arithmetic: every print's FLOOR hour is
    its NEAREST hour (no stamp sits before its hour), the loader's column IS
    that hour, and nothing past the AS_OF close hour comes out of the loader."""
    t = d["funding_time"].to_numpy(np.int64)
    floor_h, near_h = t // 3_600_000 * 3_600_000, (t + 1_800_000) // 3_600_000 * 3_600_000
    bad = []
    if (floor_h != near_h).any():
        k = int(np.argmax(floor_h != near_h))
        bad.append(f"{what}: {int((floor_h != near_h).sum())} print(s) whose floor hour is not the nearest "
                   f"hour (first {D.iso(t[k])}) — snap-to-hour would be AMBIGUOUS")
    if "funding_hour_ms" not in d.columns:
        bad.append(f"{what}: loader returned no funding_hour_ms column")
    elif (d["funding_hour_ms"].to_numpy(np.int64) != floor_h).any():
        bad.append(f"{what}: funding_hour_ms is not the floor hour")
    elif len(d) and int(d["funding_hour_ms"].max()) > CLOSE_MS:
        bad.append(f"{what}: a print of an hour AFTER the AS_OF close came out of the loader")
    return bad


def fd3_break():
    res = []
    base = D.load_funding_asof(PANEL[0])                                    # COPIES from here on
    early = base.copy()
    early.loc[early.index[5], "funding_time"] -= 10                         # 10 ms BEFORE its hour
    r = _hour_faults(early, "planted")                                      # the fixture's own arithmetic
    res.append(("a print stamped 10 ms BEFORE its hour in a COPY (floor != nearest)", not r,
                str(r[:1]) if r else "NOT DETECTED"))
    try:
        late = base[D.FUNDING_COLS].copy()
        late.loc[late.index[5], "funding_time"] += 1_800_000               # half an hour off any hour
        D.with_funding_hour(late, "planted")
        res.append(("a print stamped 30 min past its hour in a COPY", True, "returned instead of HALTing"))
    except SystemExit as e:
        res.append(("a print stamped 30 min past its hour in a COPY", False, str(e)[:110]))
    with tempfile.TemporaryDirectory(prefix="tc10_fd3_") as td:
        root = Path(td)
        shutil.copytree(D.SNAPSHOT / "funding", root / "funding")          # a COPY (< 2 MB)
        victim = PANEL[-1]
        (root / "funding" / f"{victim}.parquet").unlink()
        ok, why, _ = _fd3(root, root / "funding")
        res.append((f"{victim} funding file ABSENT in a COPY", ok, why[:150] or "NOT DETECTED"))
        shutil.copy(D.funding_path(victim), root / "funding" / f"{victim}.parquet")
        stale = PANEL[0]
        d = pd.read_parquet(root / "funding" / f"{stale}.parquet").sort_values("funding_time")
        d.iloc[:-4].to_parquet(root / "funding" / f"{stale}.parquet", index=False)
        ok, why, _ = _fd3(root, root / "funding")
        res.append((f"{stale} funding tail cut by 4 prints in a COPY", ok, why[:150] or "NOT DETECTED"))
        try:
            old_path = D.funding_path
            D.funding_path = lambda stem, root_=None: root / "funding" / "NOPE.parquet"
            D.load_funding_asof(victim)
            res.append(("load_funding_asof on a missing file", True, "returned instead of HALTing"))
        except SystemExit as e:
            res.append(("load_funding_asof on a missing file", False, str(e)[:80]))
        finally:
            D.funding_path = old_path
    return plants(res)


def fd3_real():
    ok, why, lines = _fd3(None)
    for x in lines:
        say(x)
    hour_bad, past, late_print = [], [], []
    for stem in PANEL:
        d = D.load_funding_asof(stem)
        hour_bad += _hour_faults(d, stem)
        off = (d["funding_time"] - d["funding_hour_ms"]).to_numpy(np.int64)
        past.append(int(off.max()))
        if int(d["funding_time"].max()) > CLOSE_MS:
            late_print.append(f"{stem} +{int(d['funding_time'].max()) - CLOSE_MS} ms")
    say(f"      THE FUNDING HOUR [LEAN D-g]: largest stamp offset PAST its hour over the panel {max(past)} ms, "
        f"none before its hour; prints stamped after the AS_OF close yet OF the AS_OF hour (kept, and "
        f"placed AT the close by funding_hour_ms): {late_print or 'none'}")
    return (ok and not hour_bad), (
        f"{len(PANEL)} panel assets: funding present, non-empty, last stamp within ONE observed "
        f"funding interval of the kline edge {PIN['as_of_last_closed_4h']}, and "
        f"tierc2_baseline.load_funding non-empty for every one ({why or 'no fault'}); the funding-hour "
        f"law holds on every print ({hour_bad[:2] or 'floor hour == nearest hour everywhere'})."
        f"  FAILS IF (HALT-grade) any panel asset's funding file is absent or empty, its last "
        f"stamp is older than the kline edge minus one funding interval, load_funding "
        f"returns {{}} for a panel asset, any print's floor hour differs from its nearest hour, the "
        f"loader's funding_hour_ms is missing or not that hour, or the loader returns a print of an "
        f"hour after the AS_OF close")


# ══════════════════════════════════ F-D-ASOF · NOTHING READ PAST THE PIN
def _asof_faults(frames: dict[tuple[str, str], pd.DataFrame], pre_files: dict,
                 funding: dict[str, pd.DataFrame] | None = None) -> list[str]:
    """A row TC10 WROTE is a row past the file's PRE_STATE edge, or any row of a
    file that did not exist before TC10.  Only the rows at or before the old
    edge are exempt (they pre-date TC10 and are never deleted) — NOT the whole
    file: a forward extension of a pre-existing file is TC10's own writing."""
    bad = []
    for (stem, iv), df in frames.items():
        rel = f"klines/{stem}_{iv}.parquet"
        t = df["open_time"].to_numpy(np.int64)
        edge = pre_files[rel]["last_ms"] if rel in pre_files else None
        mine = np.ones(len(t), dtype=bool) if edge is None else t > int(edge)
        after = int((mine & (t + D.STEP_MS[iv] > CLOSE_MS)).sum())
        if after:
            bad.append(f"{rel}: {after} bar(s) not closed at AS_OF among the rows TC10 itself wrote"
                       f"{'' if edge is None else ' past the old edge ' + str(D.iso(edge))}")
    for stem, df in (funding or {}).items():
        rel = f"funding/{stem}.parquet"
        t = df["funding_time"].to_numpy(np.int64)
        edge = pre_files[rel]["last_ms"] if rel in pre_files else None
        mine = np.ones(len(t), dtype=bool) if edge is None else t > int(edge)
        after = int((mine & (t // 3_600_000 * 3_600_000 > CLOSE_MS)).sum())
        if after:
            bad.append(f"{rel}: {after} print(s) of an hour after the AS_OF close among the rows TC10 wrote")
    return bad


def fdasof_break():
    f = D.load_asof("BTCUSDT", "4h")
    leak = pd.concat([f, f.iloc[[-1]].assign(open_time=f["open_time"].iloc[-1] + D.MS_4H)])
    r1 = _asof_faults({("PLANTED", "4h"): leak}, {})
    rel = "klines/BTCUSDT_12h.parquet"                       # pre-existing AND extended by TC10
    g = pd.read_parquet(D.SNAPSHOT / rel).sort_values("open_time")
    ext = pd.concat([g, g.iloc[[-1]].assign(open_time=g["open_time"].iloc[-1] + D.STEP_MS["12h"])])
    r2 = _asof_faults({("BTCUSDT", "12h"): ext}, PRE["files"])
    fu = pd.read_parquet(D.funding_path("BTCUSDT")).sort_values("funding_time")
    fu2 = pd.concat([fu, fu.iloc[[-1]].assign(funding_time=fu["funding_time"].iloc[-1] + 8 * D.MS_1H)])
    r3 = _asof_faults({}, PRE["files"], {"BTCUSDT": fu2})
    return plants([("a bar stamped after AS_OF in a file TC10 wrote whole (COPY)", not r1, str(r1[:1])),
                   ("a PRE-EXISTING file extended by TC10 past the pin (COPY) — the whole-file exemption "
                    "the review found would have let this through", not r2, str(r2[:1])),
                   ("a funding print one interval past the pin appended to a COPY", not r3, str(r3[:1]))])


def fdasof_real():
    frames = {(s, iv): pd.read_parquet(D.kline_path(s, iv)) for s in PANEL for iv in ALL_IVS}
    raw_f = {s: pd.read_parquet(D.funding_path(s)) for s in PANEL}
    bad = _asof_faults(frames, PRE["files"], raw_f)
    cut, carried = [], []
    for (s, iv), df in frames.items():
        a = D.load_asof(s, iv)
        if len(a) and int(a["open_time"].max()) + D.STEP_MS[iv] > CLOSE_MS:
            cut.append(f"{s} {iv}")
        if len(df) != len(a):
            carried.append(f"{s}_{iv} +{len(df) - len(a)}")
    fu = [s for s in PANEL if int(D.load_funding_asof(s)["funding_hour_ms"].max()) > CLOSE_MS]
    pin_ok = PIN["venue_close_time_of_pinned_bar_ms"] < PIN["venue_server_time_ms"] \
        and PIN["as_of_last_closed_4h_close_ms"] - PIN["as_of_last_closed_4h_open_ms"] == D.MS_4H \
        and PIN["as_of_last_closed_4h_open_ms"] % D.MS_4H == 0
    ext = sum(1 for rel, was in PRE["files"].items() if rel.startswith("klines/") and
              int(pd.read_parquet(D.SNAPSHOT / rel, columns=["open_time"])["open_time"].max()) > was["last_ms"])
    return (not bad and not cut and not fu and pin_ok), (
        f"pin {PIN['as_of_last_closed_4h_open']} closed on the VENUE clock before it was pinned: {pin_ok}; "
        f"rows TC10 wrote (whole new files AND the forward extensions of {ext} pre-existing kline files, "
        f"funding included) holding anything past the pin: {bad or 0}; load_asof leaks: {cut or 0}; funding "
        f"of an hour past the pin via load_funding_asof: {fu or 0}; PRE-EXISTING rows past the pin — at or "
        f"before their file's old edge — counted and cut by load_asof, never deleted: {carried or 'none'}."
        f"  FAILS IF the pinned bar was not closed by the venue's own closeTime, any row TC10 fetched or "
        f"derived — in a new file or past a pre-existing file's old edge — is not closed at AS_OF, or "
        f"load_asof / load_funding_asof returns anything stamped after it")


# ══════════════════════════════════ F-D-PREFIX · EXTENDED, NEVER REWRITTEN
def fdprefix_break():
    res = []
    rel = "klines/BTCUSDT_12h.parquet"
    with tempfile.TemporaryDirectory(prefix="tc10_fdp_") as td:
        root = Path(td)
        (root / "klines").mkdir()
        one = {"law": PRE["law"], "files": {rel: PRE["files"][rel]}}
        d = pd.read_parquet(D.SNAPSHOT / rel).sort_values("open_time").reset_index(drop=True)
        a = d.copy()
        a.loc[10, "close"] = float(np.nextafter(a.loc[10, "close"], np.inf))
        a.to_parquet(root / rel, index=False)
        r = D.verify_prefixes(one, root)[0]
        res.append(("one OLD close moved by one ULP in a COPY", r["ok"], r["why"] or "NOT DETECTED"))
        d.drop(index=20).to_parquet(root / rel, index=False)
        r = D.verify_prefixes(one, root)[0]
        res.append(("one OLD row deleted in a COPY", r["ok"], r["why"] or "NOT DETECTED"))
        mid = d.iloc[[30]].assign(open_time=d["open_time"].iloc[30] + 1)
        pd.concat([d, mid]).sort_values("open_time").to_parquet(root / rel, index=False)
        r = D.verify_prefixes(one, root)[0]
        res.append(("a row INSERTED behind the old edge in a COPY", r["ok"], r["why"] or "NOT DETECTED"))
    return plants(res)


def fdprefix_real():
    rows = D.verify_prefixes(PRE)
    bad = [f"{r['file']}: {r['why']}" for r in rows if not r["ok"]]
    ext = [r for r in rows if r.get("extended_by")]
    same = [r for r in rows if r.get("untouched_file")]
    return (not bad and len(rows) == len(PRE["files"]) and len(rows) > 0), (
        f"{len(rows)} files that existed before TC10 fetched: every OLD prefix re-read from the CURRENT file "
        f"hashes to its PRE_STATE content sha ({len(bad)} moved); {len(ext)} extended forward "
        f"(+{sum(r['extended_by'] for r in ext)} rows), {len(same)} byte-identical files."
        f"  FAILS IF any pre-existing row at or before a file's old edge changed value, vanished, or "
        f"gained a neighbour behind the edge")


# ══════════════════════════════════ F-D-VENUE · ONE VENUE PER ASSET, NEVER SPLICED
def _venue_faults(man: dict, fetch_rows: list[dict], names: list[str]) -> list[str]:
    bad = []
    v_by_stem = {v["stem"]: v["venue"] for v in man["venues"] if v["stem"]}
    for f in man["files"]:
        if f["venue"] != v_by_stem.get(f["stem"]):
            bad.append(f"{f['path']}: venue {f['venue']} != asset venue {v_by_stem.get(f['stem'])}")
    for r in fetch_rows:
        if v_by_stem.get(r["stem"]) and r["venue"] != v_by_stem[r["stem"]]:
            bad.append(f"FETCH_LOG: {r['stem']} {r.get('iv', 'funding')} fetched from {r['venue']}")
    for stem, venue in v_by_stem.items():
        if venue != "BINANCE_USDTM":
            if not stem.endswith(D.BYBIT_STEM_SUFFIX):
                bad.append(f"{stem}: alternate venue without the venue in its file stem")
            twin = stem[: -len(D.BYBIT_STEM_SUFFIX)]
            clash = [n for n in names if (n.startswith(twin + "_") or n == twin + ".parquet")
                     and not n.startswith(stem)]
            if clash:
                bad.append(f"{twin}: a default-venue-named file coexists with the alternate tape: {clash}")
    return bad


def _fetch_rows() -> list[dict]:
    p = D.OUT / "FETCH_LOG.jsonl"
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []


def _snapshot_names() -> list[str]:
    return sorted(q.name for sub in ("klines", "funding") for q in (D.SNAPSHOT / sub).glob("*.parquet"))


def fdvenue_break():
    alt = [v["stem"] for v in MAN["venues"] if v["stem"] and v["venue"] != "BINANCE_USDTM"]
    if not alt:
        rows = _fetch_rows() + [{"stem": PANEL[0], "iv": "4h", "venue": "BYBIT_V5_LINEAR", "kind": "klines"}]
        bad = _venue_faults(MAN, rows, _snapshot_names())
        return (not bad), f"a second-venue fetch row planted in a COPY of the log: {bad[:1] or 'NOT DETECTED'}"
    stem = alt[0]
    twin = stem[: -len(D.BYBIT_STEM_SUFFIX)]
    r1 = _venue_faults(MAN, _fetch_rows() + [{"stem": stem, "iv": "5m", "venue": "BINANCE_USDTM"}],
                       _snapshot_names())
    r2 = _venue_faults(MAN, _fetch_rows(), _snapshot_names() + [f"{twin}_4h.parquet"])
    m = copy.deepcopy(MAN)
    next(f for f in m["files"] if f["stem"] == stem and f["as_of_lens"] == "1h")["venue"] = "BINANCE_USDTM"
    r3 = _venue_faults(m, _fetch_rows(), _snapshot_names())
    return plants([("a Binance fetch row for the alternate-venue stem (COPY of the log)", not r1, str(r1[:1])),
                   (f"a bare {twin}_4h.parquet beside the alternate tape (COPY of the listing)", not r2, str(r2[:1])),
                   ("one file re-labelled to the other venue (COPY of the manifest)", not r3, str(r3[:1]))])


def fdvenue_real():
    rows = _fetch_rows()
    bad = _venue_faults(MAN, rows, _snapshot_names())
    unresolved = [v["asset"] for v in MAN["venues"] if not v["stem"]]
    named = {e["asset"] for e in MAN["admission"]["excluded"]}
    if any(a not in named for a in unresolved):
        bad.append(f"assets without a venue not NAMED as excluded: {unresolved}")
    n12 = len([v for v in MAN["venues"] if v["asset"] in MAN["panels"]["UNSEEN12_contract"]])
    if n12 != 12:
        bad.append(f"venue table covers {n12} of the contract's twelve")
    alt = {v["asset"]: v["venue"] for v in MAN["venues"] if v["venue"] not in ("BINANCE_USDTM", None)}
    return (not bad), (f"{len(MAN['venues'])} assets, ONE venue each; alternate venues: {alt or 'none'}; "
                       f"{len(rows)} fetch-log rows all from the asset's own venue; no default-named twin "
                       f"of an alternate tape exists: {bad or 'no fault'}."
                       f"  FAILS IF any file's venue differs from its asset's venue of record, any fetch "
                       f"for a stem came from another venue (a splice), an alternate-venue tape lacks the "
                       f"venue in its stem or has a default-named twin, or one of the twelve is unprinted")


# ══════════════════════════════════ F-D-ADMIT · 316 + 400, RECOUNTED
def _admit_faults(man: dict, pin_source: Path | None = None) -> list[str]:
    import tierc2_rules as R2
    from engine import rangefinder as RNG          # the LIVE object — fixtures are not a decision path
    floor = int(R2.TIDE_SLOW) + int(RNG.PINS_V2["MEM_TTL_BARS"])
    bad = []
    read = int(D.pin_literal(pin_source or D.RANGE_PINS_SOURCE, "PINS_V2", "MEM_TTL_BARS"))
    if read != int(RNG.PINS_V2["MEM_TTL_BARS"]):
        bad.append(f"MEM_TTL_BARS read from the SOURCE ({read}) != the live pin "
                   f"({RNG.PINS_V2['MEM_TTL_BARS']}) — the import-free read drifted")
    if pin_source is None and D.ADMISSION_MIN_4H != floor:
        bad.append(f"tierc10_data.ADMISSION_MIN_4H {D.ADMISSION_MIN_4H} != TIDE_SLOW + MEM_TTL_BARS = {floor}")
    for r in man["admission"]["rows"]:
        t = pd.read_parquet(D.kline_path(r["stem"], "4h"), columns=["open_time"])["open_time"].to_numpy(np.int64)
        n = int(np.count_nonzero(t + 14_400_000 <= CLOSE_MS))
        if n != r["closed_4h_bars"]:
            bad.append(f"{r['stem']}: recount {n} != filed {r['closed_4h_bars']}")
        if r["admitted"] != (n >= floor):
            bad.append(f"{r['stem']}: admitted={r['admitted']} but {n} vs floor {floor}")
    adm = [r["stem"] for r in man["admission"]["rows"] if r["admitted"]]
    if adm != man["panels"]["PANEL17_stems"]:
        bad.append("PANEL17_stems is not exactly the admitted set")
    if man["admission"]["rows"] and man["admission"]["rows"][0]["admission_min"] != floor:
        bad.append(f"filed floor != TIDE_SLOW + MEM_TTL_BARS = {floor}")
    return bad


def fdadmit_break():
    m = copy.deepcopy(MAN)
    m["admission"]["rows"][-1]["closed_4h_bars"] -= 1
    r1 = _admit_faults(m)
    m = copy.deepcopy(MAN)
    m["panels"]["PANEL17_stems"] = m["panels"]["PANEL17_stems"][:-1]
    r2 = _admit_faults(m)
    m = copy.deepcopy(MAN)
    for r in m["admission"]["rows"]:
        r["admission_min"] = 700
    r3 = _admit_faults(m)
    with tempfile.TemporaryDirectory(prefix="tc10_fdadmit_") as td:
        src = D.RANGE_PINS_SOURCE.read_text(encoding="utf-8")
        drift = re.sub(r'("MEM_TTL_BARS":\s*)\d+', r"\g<1>401", src, count=1)
        (Path(td) / "rangefinder.py").write_text(drift, encoding="utf-8")
        r4 = _admit_faults(MAN, Path(td) / "rangefinder.py") if drift != src else []
    return plants([("a filed count off by one (COPY)", not r1, str(r1[:1])),
                   ("an admitted asset dropped from the panel (COPY)", not r2, str(r2[:1])),
                   ("a TYPED floor of 700 (COPY)", not r3, str(r3[:1])),
                   ("the pin of record moved to 401 in a COPY of the source the data module READS "
                    "(it no longer imports the range machine)", not r4, str(r4[:1]))])


def fdadmit_real():
    bad = _admit_faults(MAN)
    rows = MAN["admission"]["rows"]
    thin = min(rows, key=lambda r: r["closed_4h_bars"])
    return (not bad), (f"{len(rows)} assets recounted from the parquet: {sum(r['admitted'] for r in rows)} "
                       f"admitted, excluded {[e['asset'] for e in MAN['admission']['excluded']] or 'none'}; "
                       f"thinnest {thin['stem']} {thin['closed_4h_bars']} bars (1d {thin['bars_1d']}, 1w "
                       f"{thin['bars_1w']}); floor {D.ADMISSION_MIN_4H} DERIVED from the two pins — "
                       f"MEM_TTL_BARS READ from engine/rangefinder.py's literal table WITHOUT importing it, "
                       f"and equal to the live object: {bad or 'no fault'}.  FAILS IF a filed count differs "
                       f"from a recount of closed 4h bars, an admission flag disagrees with count >= floor, "
                       f"the panel is not exactly the admitted set, the floor is not TIDE_SLOW + "
                       f"MEM_TTL_BARS, or the source-read pin differs from the live pin")


# ══════════════════════════════════ F-D-MANIFEST · EVERY SHA, EVERY FIELD
KLINE_FIELDS = ("path", "sha256", "rows", "rows_as_of", "rows_after_as_of", "first_open", "last_open",
                "as_of_lens", "as_of_last_closed_bar_open", "gap_count", "gaps", "duplicates", "off_grid",
                "venue", "listing", "venue_zero_volume_flat_bars", "complete_to_as_of")
FUNDING_FIELDS = ("path", "sha256", "rows", "first", "last", "venue", "listing",
                  "interval_hours_observed_tail", "spacing_hours_histogram", "coverage")
TOP_FIELDS = ("as_of_last_closed_4h", "as_of_last_closed_4h_open", "as_of_last_closed_bar_per_lens",
              "warranty", "snapshot_root", "venues", "panels", "admission", "gap_policy", "files",
              "prefix_attestation", "mirror", "leans", "seed", "complete",
              "venue_publications_disagree", "contract_premise_checks", "operator_rulings_needed",
              "as_of_hazards", "write_once")


def _manifest_faults(man: dict, root: Path) -> list[str]:
    bad = [f"top-level field MISSING: {k}" for k in TOP_FIELDS if k not in man]
    for f in man.get("files", []):
        if not f.get("present"):
            bad.append(f"{f['path']}: ABSENT")
            continue
        need = KLINE_FIELDS if f["kind"] == "klines" else FUNDING_FIELDS
        bad += [f"{f['path']}: field MISSING: {k}" for k in need if k not in f]
        if f["kind"] == "klines" and not f["native"] and "derived_from" not in f:
            bad.append(f"{f['path']}: derived lens without a derived_from note")
        q = root / f["path"]
        if not q.exists() or D.file_sha256(q) != f.get("sha256"):
            bad.append(f"{f['path']}: sha256 does not re-hash")
    for f in man.get("files", []):
        if f.get("present") and f["kind"] == "klines" and f["native"]:
            lab = (f.get("publication") or {}).get("carries")
            if lab not in D.PUB_LABELS:
                bad.append(f"{f['path']}: no MEASURED publication label")
            elif lab == "UNAUDITED":
                bad.append(f"{f['path']}: publication UNAUDITED — a census is missing for it")
    xmr = next((v for v in man.get("venues", []) if v["asset"] == "XMR"), {})
    chk = next((c for c in man.get("contract_premise_checks", []) if c["asset"] == "XMR"), None)
    if chk is None:
        bad.append("contract_premise_checks: the XMR 'post-delisting' premise is not held against the probe")
    elif (xmr.get("venue") == "BINANCE_USDTM") != chk["verdict"].startswith("STALE"):
        bad.append(f"XMR premise verdict {chk['verdict'][:24]!r} disagrees with venue {xmr.get('venue')}")
    if not (man.get("write_once") or {}).get("all_ok"):
        bad.append(f"write_once: {(man.get('write_once') or {}).get('faults')}")
    for f in man.get("out_of_scope_snapshot_files", []):
        if D.file_sha256(root / f["path"]) != f["sha256"]:
            bad.append(f"{f['path']}: out-of-scope sha moved (another writer touched the snapshot)")
    listed = {f["path"] for f in man.get("files", [])} | {f["path"] for f in man.get("out_of_scope_snapshot_files", [])}
    on_disk = {f"{sub}/{q.name}" for sub in ("klines", "funding") for q in (root / sub).glob("*.parquet")}
    if on_disk - listed:
        bad.append(f"snapshot files in NO manifest row: {sorted(on_disk - listed)[:4]}")
    return bad


STAMPED_ARTIFACTS = ("STAGE_D_MANIFEST.json", "fee_schedule.json", "VENUE_PROBE.json", "PRE_STATE.json",
                     D.REST_AUDIT, D.ARCHIVE_AUDIT, D.ARCHIVE_FORMS, D.SEAL)


def _md_faults(md: str, man: dict) -> list[str]:
    """What the BUILD doc is cut from must SAY the findings, not only hold them
    in JSON: the stale premise, the heterogeneity, the rulings, the disclosure."""
    need = [c["verdict"] for c in man.get("contract_premise_checks", [])]
    need += ["PUBLICATION-HETEROGENEOUS", "Operator rulings needed at CLOSE", "RE-STAMPED",
             "As-of hazards for downstream loaders"]
    return [f"STAGE_D_MANIFEST.md does not say: {x[:60]!r}" for x in need if x not in md]


def _stamp_faults(docs: dict[str, dict]) -> list[str]:
    """AS-OF WARRANTY [HARD LAW 6]: every filed JSON artifact names the pinned bar."""
    bad = []
    for name, j in docs.items():
        for k, want in (("as_of_last_closed_4h", PIN["as_of_last_closed_4h"]),
                        ("as_of_last_closed_4h_open", PIN["as_of_last_closed_4h_open"])):
            if j.get(k) != want:
                bad.append(f"{name}: {k} = {j.get(k)!r}, the pin says {want!r}")
        if not j.get("warranty"):
            bad.append(f"{name}: no warranty text")
    return bad


def _stamped_docs() -> dict[str, dict]:
    return {n: json.loads((D.OUT / n).read_text()) for n in STAMPED_ARTIFACTS if (D.OUT / n).exists()}


def fdmanifest_break():
    m = copy.deepcopy(MAN)
    k = next(i for i, f in enumerate(m["files"]) if f.get("present"))
    m["files"][k]["sha256"] = m["files"][k]["sha256"][:-1] + ("0" if m["files"][k]["sha256"][-1] != "0" else "1")
    r1 = _manifest_faults(m, D.SNAPSHOT)
    m = copy.deepcopy(MAN)
    del m["files"][k]["gaps"]
    r2 = _manifest_faults(m, D.SNAPSHOT)
    m = copy.deepcopy(MAN)
    del m["warranty"]
    r3 = _manifest_faults(m, D.SNAPSHOT)
    m = copy.deepcopy(MAN)
    m["files"] = [f for f in m["files"] if f["path"] != m["files"][k]["path"]]
    r4 = _manifest_faults(m, D.SNAPSHOT)
    docs = copy.deepcopy(_stamped_docs())
    docs["fee_schedule.json"].pop("as_of_last_closed_4h")
    r5 = _stamp_faults(docs)
    docs = copy.deepcopy(_stamped_docs())
    docs["STAGE_D_MANIFEST.json"]["as_of_last_closed_4h"] = "2026-09-21T20:00:00Z"
    r6 = _stamp_faults(docs)
    m = copy.deepcopy(MAN)
    m["contract_premise_checks"] = [c for c in m["contract_premise_checks"] if c["asset"] != "XMR"]
    r7 = _manifest_faults(m, D.SNAPSHOT)
    m = copy.deepcopy(MAN)
    next(f for f in m["files"] if f.get("publication"))["publication"]["carries"] = "UNAUDITED"
    r8 = _manifest_faults(m, D.SNAPSHOT)
    md = (D.OUT / "STAGE_D_MANIFEST.md").read_text(encoding="utf-8")
    xv = next(c["verdict"] for c in MAN["contract_premise_checks"] if c["asset"] == "XMR")
    r9 = _md_faults(md.replace(xv, ""), MAN)
    return plants([("one sha nibble flipped (COPY)", not r1, str(r1[:1])),
                   ("the XMR stale-premise check deleted from a COPY of the manifest", not r7, str(r7[:1])),
                   ("one file's publication left UNAUDITED (COPY)", not r8, str(r8[:1])),
                   ("the stale-premise sentence cut from a COPY of the FILED .md (it used to live only "
                    "in a run log)", not r9, str(r9[:1])),
                   ("an artifact's as-of stamp deleted (COPY)", not r5, str(r5[:1])),
                   ("an artifact stamped with a bar that is not the pin (COPY)", not r6, str(r6[:1])),
                   ("a file's gaps field deleted (COPY)", not r2, str(r2[:1])),
                   ("the warranty deleted (COPY)", not r3, str(r3[:1])),
                   ("a file row dropped — silence must not read as health (COPY)", not r4, str(r4[:1]))])


def fdmanifest_real():
    bad = _manifest_faults(MAN, D.SNAPSHOT)
    n = len(MAN["files"])
    fees = json.loads((D.OUT / "fee_schedule.json").read_text())
    stems = {a["stem"] for a in fees["assets"]}
    if stems != {v["stem"] for v in MAN["venues"] if v["stem"]}:
        bad.append("fee_schedule.json does not cover exactly the assets with a venue")
    for k in ("as_of_last_closed_4h", "as_of_last_closed_4h_open", "warranty"):
        if fees.get(k) != MAN.get(k):
            bad.append(f"fee_schedule.json as-of field {k} missing or different")
    if not MAN.get("complete"):
        bad.append("manifest says complete == False")
    docs = _stamped_docs()
    bad += _stamp_faults(docs)
    bad += [f"{n}: artifact not filed" for n in STAMPED_ARTIFACTS if n not in docs]
    bad += _md_faults((D.OUT / "STAGE_D_MANIFEST.md").read_text(encoding="utf-8"), MAN)
    return (not bad), (f"{n} in-scope rows + {len(MAN['out_of_scope_snapshot_files'])} out-of-scope files: every "
                       f"sha256 re-hashes from the snapshot, every required field present, every snapshot parquet "
                       f"is in some row, and all {len(docs)} filed JSON artifacts {sorted(docs)} carry the pin's as-of "
                       f"stamp + warranty: {bad[:3] or 'no fault'}."
                       f"  FAILS IF any sha does not re-hash, ANY required field is missing (a missing field is "
                       f"itself a fail), a snapshot file is unlisted, a panel file is absent, an artifact lacks the as-of "
                       f"stamp or names a bar that is not the pin, a native file has no MEASURED publication label "
                       f"or is UNAUDITED, the XMR premise is not held against the probe, the write-once seal has a "
                       f"fault, the filed .md omits the stale premise / the heterogeneity / the rulings / the "
                       f"re-stamp disclosure / the as-of hazards, or complete is False")


# ══════════════════════════════════ F-D-SEAL · WRITE-ONCE, IN CODE
WRITE_ONCE_WRITERS = ("pin_as_of", "probe_venues", "write_pre_state", "seal_provenance")


def _plain_dump_calls(src: str) -> list[str]:
    """A write-once writer may only write through _dump_once."""
    out = []
    for fn in ast.walk(ast.parse(src)):
        if isinstance(fn, ast.FunctionDef) and fn.name in WRITE_ONCE_WRITERS:
            out += [f"{fn.name}() calls _dump()" for c in ast.walk(fn) if isinstance(c, ast.Call)
                    and isinstance(c.func, ast.Name) and c.func.id == "_dump"]
    return out


def fdseal_break():
    res = []
    with tempfile.TemporaryDirectory(prefix="tc10_fdseal_") as td:
        root = Path(td)
        for n in D.SEALED_FILES + (D.FETCH_LOG,):
            shutil.copy(D.OUT / n, root / n)                                # COPIES
        q = root / "PRE_STATE.json"
        q.write_text(q.read_text().replace("write-once", "write-once ", 1))
        r = D.verify_seal(D.OUT, root)
        res.append(("one byte added to a COPY of PRE_STATE.json — the post-hoc re-stamp, replayed", not r,
                    str(r[:1])))
        shutil.copy(D.OUT / "PRE_STATE.json", q)
        lines = (root / D.FETCH_LOG).read_text().splitlines()
        (root / D.FETCH_LOG).write_text("\n".join([lines[0].replace("BINANCE", "BYBIT", 1)] + lines[1:]) + "\n")
        r = D.verify_seal(D.OUT, root)
        res.append(("one sealed fetch-log row edited in a COPY", not r, str(r[:1])))
        (root / D.FETCH_LOG).write_text("\n".join(lines[:-1]) + "\n")
        r = D.verify_seal(D.OUT, root)
        res.append(("the last sealed fetch-log row dropped in a COPY", not r, str(r[:1])))
        try:
            D._dump_once({"x": 1}, root / "AS_OF_PIN.json")                 # exists (a COPY)
            res.append(("_dump_once over an existing record (COPY)", True, "overwrote instead of HALTing"))
        except SystemExit as e:
            res.append(("_dump_once over an existing record (COPY)", False, str(e)[:70]))
    src = (ROOT / "scripts" / "tierc10_data.py").read_text(encoding="utf-8")
    planted = src.replace("    _dump_once(pre, p)", "    _dump(pre, p)", 1)
    r = _plain_dump_calls(planted) if planted != src else []
    res.append(("write_pre_state() writing through plain _dump in a COPY of the source", not r, str(r[:1])))
    return plants(res)


def fdseal_real():
    bad = D.verify_seal(D.OUT)
    bad += _plain_dump_calls((ROOT / "scripts" / "tierc10_data.py").read_text(encoding="utf-8"))
    seal = json.loads((D.OUT / D.SEAL).read_text()) if (D.OUT / D.SEAL).exists() else {}
    for x in seal.get("disclosure", []):
        say(f"      DISCLOSED: {x}")
    grown = len((D.OUT / D.FETCH_LOG).read_text().splitlines()) - seal.get("fetch_log", {}).get("sealed_lines", 0)
    return (not bad and bool(seal)), (
        f"{len(seal.get('files', {}))} provenance records re-hash to the seal of {seal.get('sealed_utc')}; the fetch "
        f"log keeps its {seal.get('fetch_log', {}).get('sealed_lines')} sealed lines (+{grown} since); every "
        f"write-once writer {list(WRITE_ONCE_WRITERS)} writes ONLY through _dump_once: {bad or 'no fault'}.  "
        f"WHAT THIS DOES NOT PROVE: that nothing moved BEFORE the seal — two of the three records were "
        f"re-stamped after the fetch, DISCLOSED above; their row content is re-proven from the snapshot by "
        f"F-D-PREFIX.  FAILS IF a sealed record's bytes moved or vanished, a sealed fetch-log line changed or "
        f"is gone, the seal is absent, or a write-once writer can overwrite")


# ══════════════════════════════════ F-D-CLOSURE · THE DATA MODULE IS RANGE-FREE
RANGE_IMPORT_LINE = re.compile(          # OR-1 F-BR-14's regex, verbatim
    r"(?m)^[ \t]*(?:from|import)[ \t]+[^\n#]*\brangefinder\b")
TIER_RUN_MODULE = re.compile(r"^(tierc\d+[a-z_0-9]*|tierc2_baseline|analytics(\..*)?|posture_engine)$")
CLOSURE_ALLOWED = {"tierc2_rules", "tierc10_data"}


def _closure(shadow_src: str | None = None) -> set[str]:
    """Modules a CLEAN interpreter loads by importing tierc10_data.  With
    `shadow_src`, a PLANTED copy shadows the real module in a throwaway
    directory FIRST on the subprocess's path — no repo file is touched."""
    with tempfile.TemporaryDirectory(prefix="tc10_fdclosure_") as td:
        if shadow_src is not None:
            (Path(td) / "tierc10_data.py").write_text(shadow_src, encoding="utf-8")
        code = ("import sys, json; sys.dont_write_bytecode = True; "
                f"sys.path.insert(0, {str(ROOT)!r}); sys.path.insert(0, {str(ROOT / 'scripts')!r}); "
                + (f"sys.path.insert(0, {td!r}); " if shadow_src is not None else "")
                + "before = set(sys.modules); import tierc10_data; "
                "print(json.dumps(sorted(set(sys.modules) - before)))")
        out = subprocess.run([PY, "-c", code], cwd=ROOT, env=dict(os.environ), capture_output=True,
                             text=True, timeout=600)
    if out.returncode != 0:
        raise RuntimeError(out.stderr[-400:])
    return set(json.loads(out.stdout.strip().splitlines()[-1]))


def _closure_faults(closure: set[str], src: str) -> list[str]:
    bad = [f"closure reaches {m}" for m in sorted(closure)
           if any("rangefinder" in part for part in m.split("."))
           or (TIER_RUN_MODULE.match(m) and m not in CLOSURE_ALLOWED)]
    bad += [f"F-BR-14 line: {m.group(0).strip()}" for m in RANGE_IMPORT_LINE.finditer(src)]
    return bad


def fdclosure_break():
    src = (ROOT / "scripts" / "tierc10_data.py").read_text(encoding="utf-8")
    anchored = src.replace("ROOT = Path(__file__).resolve().parents[1]", f"ROOT = Path({str(ROOT)!r})", 1)
    hook = "import tierc2_rules as R2"
    p1 = anchored.replace(hook, "from engine import rangefinder as RNG\n" + hook, 1)
    p2 = anchored.replace(hook, "import tierc2_baseline as TB\n" + hook, 1)
    lazy = anchored + "\n\ndef _planted():\n    from engine.rangefinder import PINS_V2\n    return PINS_V2\n"
    r1 = _closure_faults(_closure(p1), p1) if p1 != anchored else []
    r2 = _closure_faults(_closure(p2), p2) if p2 != anchored else []
    r3 = _closure_faults(_closure(lazy), lazy)
    return plants([("the range machine imported at module level — the filed state before the repair "
                    "(shadow COPY)", not r1, str(r1[:2])),
                   ("a tier RUN module imported (shadow COPY)", not r2, str(r2[:1])),
                   ("a LAZY in-function range import — invisible to sys.modules, caught by the line "
                    "scan (shadow COPY)", not r3, str(r3[:1]))])


def fdclosure_real():
    src = (ROOT / "scripts" / "tierc10_data.py").read_text(encoding="utf-8")
    c = _closure()
    bad = _closure_faults(c, src)
    mine = sorted(m for m in c if m.split(".")[0] in ("engine", "tierc2_rules", "tierc10_data", "analytics")
                  or m.startswith("tierc"))
    return (not bad), (f"importing tierc10_data in a clean interpreter loads {len(c)} modules; the estate's among "
                       f"them: {mine}; range / analytics / tier-run modules reached: {bad or 'none'} — a decision "
                       f"module may import it for load_asof / panel without dragging the range machine into its "
                       f"closure.  FAILS IF the closure holds any module with 'rangefinder' in its name, "
                       f"`analytics`, tierc2_baseline or any tier run module, or the source holds a line "
                       f"F-BR-14's regex flags (a lazy import included)")


# ══════════════════════════════════ F-D-FEE · READ, NEVER TYPED
def _fee_faults(src_text: str, fees: dict) -> list[str]:
    import tierc2_rules as R2
    bad = []
    tree = ast.parse(src_text)
    fn = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "fee_schedule")
    lits = [n.value for n in ast.walk(fn) if isinstance(n, ast.Constant)
            and isinstance(n.value, (int, float)) and not isinstance(n.value, bool)]
    if lits:
        bad.append(f"numeric literal(s) typed inside fee_schedule(): {lits}")
    for a in fees["assets"]:
        if a["taker_bps_side_used"] != float(R2.FEE_BPS_SIDE) or \
                a["round_trip_bps_used"] != float(R2.FEE_BPS_ROUND_TRIP):
            bad.append(f"{a['asset']}: filed fee != tierc2_rules ({R2.FEE_BPS_SIDE}/{R2.FEE_BPS_ROUND_TRIP})")
        if "ASSUMPTION" not in a["kind"]:
            bad.append(f"{a['asset']}: not marked ASSUMPTION")
        for s in a["source"]:
            path, _, line = s.rpartition(":")
            if not line.isdigit() or "fee_bps" not in (ROOT / path).read_text().splitlines()[int(line) - 1].lower():
                bad.append(f"{a['asset']}: source line {s} does not hold the fee object")
        if a["funding_interval_hours_observed_tail"] is None:
            bad.append(f"{a['asset']}: no OBSERVED funding interval")
    return bad


def fdfee_break():
    src = (ROOT / "scripts" / "tierc10_data.py").read_text(encoding="utf-8")
    fees = json.loads((D.OUT / "fee_schedule.json").read_text())
    planted = src.replace('"taker_bps_side_used": float(R2.FEE_BPS_SIDE),', '"taker_bps_side_used": 5.0,')
    r1 = _fee_faults(planted, fees) if planted != src else []
    f2 = copy.deepcopy(fees)
    f2["assets"][0]["taker_bps_side_used"] = 4.0
    r2 = _fee_faults(src, f2)
    f3 = copy.deepcopy(fees)
    f3["assets"][0]["source"] = ["scripts/tierc2_rules.py:1"]
    r3 = _fee_faults(src, f3)
    return plants([("a TYPED 5.0 planted in a COPY of the source", not r1, str(r1[:1])),
                   ("a filed fee that is not the estate's (COPY)", not r2, str(r2[:1])),
                   ("a source line that does not hold the fee (COPY)", not r3, str(r3[:1]))])


def fdfee_real():
    fees = json.loads((D.OUT / "fee_schedule.json").read_text())
    bad = _fee_faults((ROOT / "scripts" / "tierc10_data.py").read_text(encoding="utf-8"), fees)
    grid = {a["stem"]: a["funding_interval_hours_observed_tail"] for a in fees["assets"]}
    return (not bad), (f"{len(fees['assets'])} assets: taker {fees['assets'][0]['taker_bps_side_used']} bps/side "
                       f"READ from tierc2_rules (no numeric literal inside fee_schedule()), marked ASSUMPTION, "
                       f"sources {fees['assets'][0]['source']} each hold the fee object; funding interval "
                       f"OBSERVED (tail, hours): {grid}: {bad[:3] or 'no fault'}."
                       f"  FAILS IF the fee is typed rather than read, differs from the estate's FEE_BPS_SIDE, "
                       f"is not marked ASSUMPTION, cites a line that does not hold it, or an asset has no "
                       f"observed funding interval")


# ══════════════════════════════════ F-DET · SAME SNAPSHOT, SAME BYTES (last)
DET_FILES = ("STAGE_D_MANIFEST.json", "STAGE_D_MANIFEST.md", "fee_schedule.json")
_DET: dict = {}


def _det_run() -> Path:
    if "dir" not in _DET:
        td = Path(tempfile.mkdtemp(prefix="tc10_fdet_"))
        p = subprocess.run([PY, str(ROOT / "scripts" / "tierc10_data.py"), "--offline", "--out", str(td)],
                           cwd=ROOT, env=dict(os.environ), capture_output=True, text=True, timeout=3600)
        _DET.update(dir=td, rc=p.returncode, tail=(p.stdout.strip().splitlines() or [""])[-1])
    return _DET["dir"]


CLOCK_KEYS = ("wall_clock", "sealed_utc", "probed_utc", "audited_", "elapsed")
PROVENANCE_FILES = ("AS_OF_PIN.json", "VENUE_PROBE.json", "PRE_STATE.json", "FETCH_LOG.jsonl",
                    D.REST_AUDIT, D.ARCHIVE_AUDIT, D.ARCHIVE_FORMS, D.SEAL)   # run-time clocks BY DESIGN


def _det_diff(filed_dir: Path, rerun_dir: Path) -> list[str]:
    out = [f"{n}: a PROVENANCE file (run-time clocks) is in the determinism set" for n in DET_FILES
           if n in PROVENANCE_FILES]
    for n in DET_FILES:
        a, b = filed_dir / n, rerun_dir / n
        hits = [k for k in CLOCK_KEYS if a.exists() and k in a.read_text(encoding="utf-8")]
        if hits:
            out.append(f"{n}: run-time clock key(s) {hits} inside a deterministic artifact")
        if not b.exists():
            out.append(f"{n}: rerun did not write it")
        elif D.file_sha256(a) != D.file_sha256(b):
            out.append(f"{n}: {D.file_sha256(a)[:12]} != {D.file_sha256(b)[:12]}")
    return out


def fdet_break():
    rerun = _det_run()
    with tempfile.TemporaryDirectory(prefix="tc10_fdet_b_") as td:
        cp = Path(td)
        for n in DET_FILES:
            shutil.copy(D.OUT / n, cp / n)
        m = json.loads((cp / DET_FILES[0]).read_text())
        m["files"][0]["rows"] = (m["files"][0].get("rows") or 0) + 1
        (cp / DET_FILES[0]).write_text(json.dumps(m, indent=2, sort_keys=True, default=str) + "\n")
        diff = _det_diff(cp, rerun)
        shutil.copy(D.OUT / DET_FILES[0], cp / DET_FILES[0])
        m = json.loads((cp / DET_FILES[0]).read_text())
        m["refiled_wall_clock_utc"] = "2026-09-21T00:00:00Z"
        (cp / DET_FILES[0]).write_text(json.dumps(m, indent=2, sort_keys=True, default=str) + "\n")
        clock = [x for x in _det_diff(cp, rerun) if "clock" in x]
    return plants([("one row count moved in a COPY of the filed manifest", not diff, str(diff[:1])),
                   ("a run-time clock key planted in a COPY of the filed manifest", not clock, str(clock[:1]))])


def fdet_real():
    rerun = _det_run()
    diff = _det_diff(D.OUT, rerun)
    digests = {n: D.file_sha256(D.OUT / n)[:16] for n in DET_FILES}
    ok = _DET["rc"] in (0,) and not diff
    shutil.rmtree(rerun, ignore_errors=True)
    return ok, (f"an --offline re-description of the same snapshot in a fresh process (exit {_DET['rc']}) wrote "
                f"BYTE-identical {list(DET_FILES)}: {digests}; differences {diff or 'none'}; rerun data deleted "
                f"this session; no run-time clock key {list(CLOCK_KEYS)} inside them (the provenance files "
                f"{list(PROVENANCE_FILES)} hold clocks BY DESIGN and are never in this set).  FAILS IF any of "
                f"the three artifacts differs by one byte between the filed run and a re-run (wall-clock, dict "
                f"order or set order leaked into an artifact), holds a run-time clock key, a provenance file "
                f"is in the determinism set, or the re-run does not exit 0")


LEGS = [
    ("F-D-0", "the substrate guard: snapshot only, live cache never", fd0_break, fd0_real, False),
    ("F-D-1", "three assets' bars hand-checked vs the venue API, native-vs-native", lambda: _fd1(True),
     lambda: _fd1(False), True),
    ("F-D-1b", "every bar is ONE of the venue's two publications, and the measured labels hold", fd1b_break,
     lambda: _fd1b(False), True),
    ("F-D-2", "no synthetic bars: Naiad inserted none; the venue's flat bars counted", fd2_break, fd2_real, False),
    ("F-D-L1", "derived 1d / 1w = six complete 4h bars / seven complete days, Monday", fdl1_break, fdl1_real, False),
    ("F-D-3", "funding coverage per asset; load_funding == {} unreachable", fd3_break, fd3_real, False),
    ("F-D-ASOF", "nothing fetched, derived or loaded is stamped after the pin", fdasof_break, fdasof_real, False),
    ("F-D-PREFIX", "pre-existing files extended forward only, never rewritten", fdprefix_break, fdprefix_real, False),
    ("F-D-VENUE", "one venue of record per asset, never spliced", fdvenue_break, fdvenue_real, False),
    ("F-D-ADMIT", "admission >= 316 + 400 closed 4h bars, recounted", fdadmit_break, fdadmit_real, False),
    ("F-D-MANIFEST", "every sha re-hashes; a missing field is itself a fail", fdmanifest_break, fdmanifest_real, False),
    ("F-D-SEAL", "write-once records: sealed, re-hashed, and unwritable in code", fdseal_break, fdseal_real, False),
    ("F-D-CLOSURE", "the data module's import closure is range-free", fdclosure_break, fdclosure_real, False),
    ("F-D-FEE", "fee schedule read from the estate's object, never typed", fdfee_break, fdfee_real, False),
    ("F-DET", "same snapshot -> byte-identical artifacts (last)", fdet_break, fdet_real, False),
]

OFFLINE = False


def main() -> int:
    global OFFLINE
    args = [a for a in sys.argv[1:]]
    OFFLINE = "--offline" in args
    want = [a.lower().replace("_", "-") for a in args if not a.startswith("--")]
    say(f"as_of_last_closed_4h: {PIN['as_of_last_closed_4h']}")
    say(f"TIER-C10 STAGE D FIXTURES · seed {SEED} · snapshot {D.SNAPSHOT} · panel {len(PANEL)}: {' '.join(PANEL)}")
    say(f"as_of_last_closed_4h_open: {PIN['as_of_last_closed_4h_open']} · warranty: {MAN['warranty']}")
    for fid, title, brk, real, needs_net in LEGS:
        if want and not any(w in fid.lower() for w in want):
            continue
        if needs_net and OFFLINE:
            say(f"\n{fid} — {title}\n  [NOT RUN] --offline: this leg asks the venue; NOT counted as a pass")
            NOT_RUN.append(fid)
            continue
        try:
            prove(fid, title, brk, real)
        except Exception as e:                                  # a crash is a FAIL, never a skip
            say(f"  [FAIL] {fid}: leg raised {type(e).__name__}: {e}")
            FAILED.append(f"{fid} (raised {type(e).__name__})")
    say(f"\nFIXTURE SUMMARY  {len(PASSED)}/{len(PASSED) + len(FAILED)} PASS  "
        f"{json.dumps({'passed': PASSED, 'failed': FAILED, 'not_run': NOT_RUN})}")
    if not want:                                 # an --offline run never overwrites the FULL transcript
        name = "FIXTURES_STAGE_D_OFFLINE.txt" if OFFLINE else "FIXTURES_STAGE_D.txt"
        (D.OUT / name).write_text("\n".join(T) + "\n", encoding="utf-8")
    if FAILED:
        say("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
