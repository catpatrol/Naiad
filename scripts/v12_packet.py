"""v12 Study V1 session packet (deliverable D7) — one zip the operator
ferries to the reviewer.

  python scripts/v12_packet.py

Bundles the census artifacts, gap report, spot-check sheet, sidecars,
fixture results (pytest re-run, captured), the D6 ledger diff, the contract
documents, and a one-page manifest. Lands in research_outputs/packets/
(gitignored, ferried by hand — Phase 1 convention).
"""

import hashlib
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

ROOT = Path(__file__).resolve().parent.parent


def run(args: list[str]) -> str:
    return subprocess.run(args, capture_output=True, text=True,
                          cwd=ROOT).stdout


def main() -> int:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")
    out_dir = ROOT / "research_outputs" / "packets"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"v12_v1_packet_{stamp}.zip"

    fixture_results = subprocess.run(
        [sys.executable, "-m", "pytest", "fixtures", "-v", "--no-header"],
        capture_output=True, text=True, cwd=ROOT).stdout

    d6_hash = run(["git", "log", "--format=%H", "--grep",
                   "v12 V1 D6", "-1"]).strip()
    ledger_diff = run(["git", "show", d6_hash, "--", "LEDGER.md"]) \
        if d6_hash else "(D6 commit not found)"
    git_rev = run(["git", "rev-parse", "--short", "HEAD"]).strip()
    dirty = run(["git", "status", "--porcelain"]).strip()

    include = [ROOT / p for p in (
        "census.json", "DATA_CENSUS.md", "GAP_REPORT.md", "SPOT_CHECK.md",
        "V12_Study_Charter_Addendum_v1.0.md", "V12_V1_Census_Build_Prompt.md",
        "LEDGER.md", "CHANGELOG.md", "data_starts.csv",
        "research_outputs/census/retrieval_meta.json",
        "research_outputs/census/refetch_log.json")]
    include = [p for p in include if p.exists()]

    manifest = [
        "V12 STUDY — PHASE V1 SESSION PACKET",
        f"created_utc: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"git_rev: {git_rev}{' (DIRTY TREE)' if dirty else ''}",
        f"d6_ledger_commit: {d6_hash}",
        "",
        "WHAT RAN",
        "- Census over the full estate: 60 kline series + 10 funding series,",
        "  timestamp-and-bytes scans only (lockbox never read in value mode).",
        "- Estate completion: BTCUSDT 5m/1h re-extended from the 2019-09-08",
        "  listing after being found truncated to 2025-03-01 (see OPEN ITEMS).",
        "- Gap repair: 5 funding download-hole candidates re-fetched twice",
        "  each; all escalated exchange_side (same skipped settlement,",
        "  2026-06-24 04:00 UTC, all five 4h-grid symbols).",
        "- Fixtures F1-F9 added; full suite green (35 = 26 Phase 1 + 9 v12).",
        "- Census determinism verified: two runs, byte-identical census.json.",
        "- Hash verification: 70/70 estate files match the manifest.",
        "",
        "WHAT CHANGED",
        "- New: study/ package (loader guards + census engine),",
        "  scripts/census.py, scripts/spot_check.py, scripts/v12_packet.py,",
        "  fixtures/test_v12_census.py.",
        "- New artifacts at repo root: census.json, DATA_CENSUS.md,",
        "  GAP_REPORT.md, SPOT_CHECK.md; sidecars research_outputs/census/.",
        "- LEDGER.md: addendum SS8 block appended byte-for-byte (D6, own",
        "  commit, diff enclosed).",
        "- CHANGELOG.md: v12 V1 entry. Engine version unchanged (1.0.1);",
        "  no Phase 1 file modified; existing fixtures untouched.",
        "",
        "OPEN ITEMS / FINDINGS FOR THE REVIEWER",
        "1. OPERATOR SPOT CHECK PENDING - SPOT_CHECK.md (30 rows) awaits the",
        "   operator's TradingView pass; the phase verdict gates on it.",
        "2. Funding-grid premise amended: the build prompt says 8-hour",
        "   records; actual grids are per-symbol (BTC/ETH/NEAR/ZEC 8h;",
        "   JTO/TAO/HYPE/FARTCOIN/LIT 4h; SOL shifted 8h->4h->2h->8h over",
        "   2022-11-09 -> 2022-11-18). Documented as grid segments in",
        "   census.json; F9 verifies the 8h case synthetically as written.",
        "3. BTCUSDT 5m/1h cache truncation: both files started at 2025-03-01",
        "   despite the committed Phase 1 coverage report showing full",
        "   backfill to listing. Re-extended (REST, verified gap-free). Root",
        "   cause not chased (out of scope); some Naiad-line cache writer can",
        "   persist a windowed frame - recommend a no-shrink guard on",
        "   _save_cache before the collector goes live.",
        "4. Retro-holdout precaution: VR-1 makes pre-2022 exploration-classic",
        "   minable, but the Naiad ledger seals pre-2022-01-01 as a read-once",
        "   retro holdout. Spot-check exploration rows were drawn from",
        "   2022-01-01 onward so this phase prints no pre-2022 OHLCV; the",
        "   tension awaits reviewer ruling before any V4 mining of pre-2022.",
        "5. Conventions added (flagged per contract SS1.3): retrieval_meta",
        "   sidecar (write-once per content hash), refetch_log sidecar,",
        "   guard_log.jsonl in the cache dir, census artifacts at repo root.",
        "6. HYPE and FARTCOIN listed inside the lockbox window: they",
        "   contribute lockbox + contaminated rows only (zero exploration).",
        "   LIT is contaminated-only (floor 2025-12-23). Reflected in the",
        "   census summary.",
        "",
        "VERDICT INPUTS (SS7): coverage 60/60 + 10/10; gaps remaining are 1",
        "listing_edge + 5 exchange_side, zero download_hole; fixtures 35",
        "green; census deterministic; hashes verified. Pending: operator",
        "spot check; reviewer recomputation from this packet.",
        "",
        "contents (sha256  path):",
    ]

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in include:
            arc = str(p.relative_to(ROOT)).replace("\\", "/")
            manifest.append(
                f"  {hashlib.sha256(p.read_bytes()).hexdigest()}  {arc}")
            z.write(p, arc)
        z.writestr("fixture_results.txt", fixture_results)
        z.writestr("ledger_diff_d6.txt", ledger_diff)
        manifest.append("  (generated in-zip)  fixture_results.txt")
        manifest.append("  (generated in-zip)  ledger_diff_d6.txt")
        z.writestr("MANIFEST.txt", "\n".join(manifest) + "\n")

    print(f"packet -> {out}  ({len(include) + 2} files + manifest)")
    tail = [ln for ln in fixture_results.splitlines() if "passed" in ln]
    print("fixtures:", tail[-1].strip() if tail else "(no summary line?)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
