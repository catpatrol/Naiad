#!/usr/bin/env python
"""daily_routine.py -- run the day's jobs, stage their outputs, write one report.

Composable by design: the job list lives in scripts/routine_jobs.json, so a new
job is added by editing that file, never by editing this code.

Contract:
  * repo root is resolved from this file's own location -- never hardcoded
  * jobs run in registry order, via the interpreter named in the registry
  * a REQUIRED job that fails stops the run; an optional one is recorded and
    the run continues
  * each job's declared outputs are staged into output_dir with {date} filled in
  * the report is written to <output_dir>/DAILY_<yyyy-mm-dd>.md
  * NO git operations of any kind, ever -- repo state is read only from the
    manifest that the manifest job produces
  * exit code is non-zero if any required job failed
"""

import json
import shutil
import subprocess
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = Path(__file__).resolve().parent / "routine_jobs.json"


# --------------------------------------------------------------- registry


def load_registry():
    with REGISTRY.open(encoding="utf-8") as fh:
        reg = json.load(fh)
    for key in ("python", "output_dir", "jobs"):
        if key not in reg:
            raise SystemExit(f"routine_jobs.json: missing required key {key!r}")
    return reg


def subst(text, today):
    return text.replace("{date}", today)


# --------------------------------------------------------------- job runner


def run_job(job, python, today, out_dir):
    """Run one job. Returns a result dict; never raises on job failure."""
    jid = job.get("id", "<unnamed>")
    script = ROOT / job["script"]
    res = {
        "id": jid,
        "script": job["script"],
        "required": bool(job.get("required", False)),
        "exit": None,
        "elapsed": 0.0,
        "staged": [],
        "missing": [],
        "error": None,
    }

    if not script.exists():
        res["exit"] = 127
        res["error"] = f"script not found: {job['script']}"
        return res

    t0 = time.monotonic()
    try:
        proc = subprocess.run(
            [python, str(script)],
            cwd=str(ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        res["exit"] = proc.returncode
        if proc.returncode != 0:
            tail = (proc.stdout or b"").decode("utf-8", "replace").strip().splitlines()
            res["error"] = tail[-1] if tail else "no output"
    except OSError as exc:
        res["exit"] = 126
        res["error"] = f"could not launch: {exc}"
    res["elapsed"] = round(time.monotonic() - t0, 1)

    if res["exit"] != 0:
        return res

    for item in job.get("stage", []):
        src = ROOT / subst(item["from"], today)
        dst = out_dir / subst(item["to"], today)
        if src.exists():
            shutil.copy2(src, dst)
            res["staged"].append(dst.name)
        else:
            res["missing"].append(subst(item["from"], today))
    return res


# --------------------------------------------------------------- report parts


def repo_state(manifest):
    """Section 3 -- repo state, read from the manifest, never from git."""
    if not manifest:
        return ["Repo state unavailable -- no manifest was staged this run."]

    ab = manifest.get("ahead_behind") or {}
    porcelain = manifest.get("status_porcelain") or []
    tracked_dirty = [p for p in porcelain if not p.lstrip().startswith("??")]
    drifted = [s["path"] for s in manifest.get("sources", []) if not s.get("match_head", True)]
    untracked = manifest.get("untracked_root") or []

    lines = [
        f"- HEAD: `{manifest.get('head', '?')}`",
        f"- branch: `{manifest.get('branch', '?')}`",
        f"- ahead / behind: {ab.get('ahead', '?')} / {ab.get('behind', '?')}",
        f"- worktree clean (tracked files): {'yes' if not tracked_dirty else 'NO'}"
        + (f" -- {len(tracked_dirty)} tracked entr{'y' if len(tracked_dirty) == 1 else 'ies'} dirty" if tracked_dirty else ""),
    ]
    if drifted:
        lines.append(f"- sources with `match_head: false` ({len(drifted)}):")
        lines += [f"    - `{p}`" for p in drifted]
    else:
        lines.append("- sources with `match_head: false`: none")

    if untracked:
        lines.append(f"- untracked files at repo root ({len(untracked)}):")
        lines += [f"    - `{u.get('name', u) if isinstance(u, dict) else u}`" for u in untracked]
    else:
        lines.append("- untracked files at repo root: none")
    return lines


def _untracked_names(manifest):
    out = set()
    for u in manifest.get("untracked_root") or []:
        out.add(u.get("name") if isinstance(u, dict) else str(u))
    return out


def _source_shas(manifest):
    return {
        s["path"]: s.get("sha256_worktree")
        for s in manifest.get("sources", []) + manifest.get("reviewer_box", [])
        if "path" in s
    }


def change_since_last(manifest, out_dir, today):
    """Section 4 -- diff today's manifest against the most recent earlier one."""
    if not manifest:
        return ["Not computed -- no manifest this run."]

    prior = sorted(
        p for p in out_dir.glob("MANIFEST_*.json")
        if p.stem.replace("MANIFEST_", "") < today
    )
    if not prior:
        return ["No earlier manifest in the archive -- this is the first recorded run."]

    prev_path = prior[-1]
    prev_date = prev_path.stem.replace("MANIFEST_", "")
    try:
        with prev_path.open(encoding="utf-8") as fh:
            prev = json.load(fh)
    except (OSError, ValueError) as exc:
        return [f"Could not read {prev_path.name}: {exc}"]

    lines, changed = [], False

    old_head, new_head = prev.get("head"), manifest.get("head")
    if old_head != new_head:
        changed = True
        lines.append(f"- HEAD moved: `{old_head}` -> `{new_head}`")
        lines.append(
            "    - commits added: not enumerable -- this routine performs no git "
            "operations by contract, and the manifest records only the HEAD sha."
        )
    else:
        lines.append(f"- HEAD unchanged: `{new_head}`")

    old_shas, new_shas = _source_shas(prev), _source_shas(manifest)
    moved = sorted(p for p in old_shas.keys() & new_shas.keys() if old_shas[p] != new_shas[p])
    added = sorted(new_shas.keys() - old_shas.keys())
    dropped = sorted(old_shas.keys() - new_shas.keys())
    if moved:
        changed = True
        lines.append(f"- files whose sha256 changed ({len(moved)}):")
        lines += [f"    - `{p}`" for p in moved]
    if added:
        changed = True
        lines.append(f"- files newly tracked by the manifest ({len(added)}):")
        lines += [f"    - `{p}`" for p in added]
    if dropped:
        changed = True
        lines.append(f"- files no longer tracked by the manifest ({len(dropped)}):")
        lines += [f"    - `{p}`" for p in dropped]
    if not (moved or added or dropped):
        lines.append("- no sha256 changes among manifest sources")

    u_old, u_new = _untracked_names(prev), _untracked_names(manifest)
    u_add, u_del = sorted(u_new - u_old), sorted(u_old - u_new)
    if u_add:
        changed = True
        lines.append(f"- untracked added ({len(u_add)}):")
        lines += [f"    - `{n}`" for n in u_add]
    if u_del:
        changed = True
        lines.append(f"- untracked removed ({len(u_del)}):")
        lines += [f"    - `{n}`" for n in u_del]
    if not (u_add or u_del):
        lines.append("- untracked set unchanged")

    if not changed:
        return [f"no change since {prev_date}"]
    return [f"Compared against `{prev_path.name}` ({prev_date}).", ""] + lines


def brief_biases(out_dir, today):
    """Section 5 -- headline daily/weekly bias per asset, if the brief ran."""
    staged = out_dir / f"brief_{today}.json"
    if not staged.exists():
        return None
    try:
        with staged.open(encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        return [f"Brief JSON staged but unreadable: {exc}"]

    assets = data.get("assets") or {}
    if not assets:
        return ["Brief JSON staged but carried no assets block."]

    rows = ["| asset | daily bias | weekly bias |", "|---|---|---|"]
    for sym in sorted(assets):
        bias = (assets[sym] or {}).get("bias") or {}
        d = (bias.get("daily") or {}).get("verdict", "?")
        w = (bias.get("weekly") or {}).get("verdict", "?")
        rows.append(f"| {sym} | {d} | {w} |")
    return rows


# --------------------------------------------------------------- main


def main():
    reg = load_registry()
    today = date.today().strftime("%Y-%m-%d")
    out_dir = ROOT / reg["output_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)

    python = reg["python"]
    if not Path(python).exists():
        raise SystemExit(f"configured interpreter does not exist: {python}")

    results, halted = [], None
    for job in reg["jobs"]:
        res = run_job(job, python, today, out_dir)
        results.append(res)
        print(f"  {res['id']}: exit={res['exit']} elapsed={res['elapsed']}s")
        if res["exit"] != 0 and res["required"]:
            halted = res["id"]
            break

    manifest = None
    staged_manifest = out_dir / f"MANIFEST_{today}.json"
    if staged_manifest.exists():
        try:
            with staged_manifest.open(encoding="utf-8") as fh:
                manifest = json.load(fh)
        except (OSError, ValueError):
            manifest = None

    failures = [r for r in results if r["exit"] != 0]
    skipped = [j["id"] for j in reg["jobs"] if j["id"] not in {r["id"] for r in results}]

    out = [f"# DAILY -- {today}", ""]
    out.append(f"Generated {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} "
               f"by `scripts/daily_routine.py` (registry version {reg.get('version')}).")
    out.append("")

    # 1. failures first, in plain language
    out.append("## 1. Failures")
    out.append("")
    if not failures:
        out.append("all jobs OK")
    else:
        for r in failures:
            kind = "required" if r["required"] else "optional"
            out.append(f"- **{r['id']}** ({kind}) failed with exit code {r['exit']}.")
            if r["error"]:
                out.append(f"  Last thing it said: {r['error']}")
            if r["required"]:
                out.append("  This job is required, so the run stopped here.")
            else:
                out.append("  This job is optional, so the run continued without it.")
        if skipped:
            out.append(f"- Not attempted because the run stopped: {', '.join(skipped)}.")
    out.append("")

    # 2. per-job detail
    out.append("## 2. Jobs")
    out.append("")
    out.append("| job | exit code | elapsed (s) | staged |")
    out.append("|---|---:|---:|---|")
    for r in results:
        staged = ", ".join(f"`{s}`" for s in r["staged"]) if r["staged"] else "--"
        out.append(f"| {r['id']} | {r['exit']} | {r['elapsed']} | {staged} |")
    for r in results:
        if r["missing"]:
            out.append("")
            out.append(f"Declared outputs missing for **{r['id']}**: "
                       + ", ".join(f"`{m}`" for m in r["missing"]))
    out.append("")

    # 3. repo state
    out.append("## 3. Repo state")
    out.append("")
    out += repo_state(manifest)
    out.append("")

    # 4. change since last run
    out.append("## 4. Change since last run")
    out.append("")
    out += change_since_last(manifest, out_dir, today)
    out.append("")

    # 5. brief biases
    out.append("## 5. Headline bias")
    out.append("")
    biases = brief_biases(out_dir, today)
    out += biases if biases else ["The brief did not run, so there is no bias table today."]
    out.append("")

    report = out_dir / f"DAILY_{today}.md"
    report.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {report.relative_to(ROOT).as_posix()}")

    required_failed = [r["id"] for r in results if r["exit"] != 0 and r["required"]]
    if required_failed:
        print(f"FAILED (required): {', '.join(required_failed)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
