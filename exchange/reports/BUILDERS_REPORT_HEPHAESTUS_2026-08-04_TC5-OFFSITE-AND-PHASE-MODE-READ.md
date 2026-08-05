# BUILDERS REPORT — HEPHAESTUS — 2026-08-04
## TC5 taken off-machine, legacy snapshot spot-checked, `--phase` mode read, one stale Drive claim corrected

**Lane:** HEPHAESTUS (local Windows Claude Code)
**Repo:** naiad · **Branch:** `v12-v1-census` · **HEAD at start:** `2bb8841`
**Python:** 3.12.10 (`C:/venvs/naiad/Scripts/python.exe`)
**Operator ruling carried into this run (2026-08-04):** *"naiad (local folder) BACKUP" is a ONE-OFF
snapshot, not maintained.*

---

## 0 · What this session was for, in plain language

Four jobs, none of which change how the trading research works — they all concern **whether the
evidence behind that research would survive losing this laptop.**

1. **Get `tc5` off the machine.** `tc5_2026-08-02.zip` is the archived evidence for research phase
   tc5. It existed in exactly one place: this laptop. A single disk failure would have destroyed it.
   It is now also on Google Drive, and the copy was proved byte-identical rather than assumed to be.
2. **Spot-check the legacy snapshot.** There is an older, one-off copy of the whole project folder
   sitting on Drive. Nobody had ever checked whether its contents were actually readable and intact,
   as opposed to merely present. One archive was fully hashed to find out.
3. **Read `backup_estate.py`'s `--phase` mode.** This is the deliverable that matters most. The
   backup script has three modes; two of them write to Drive automatically and one — the phase mode
   — apparently does not. This report contains the full source so the wiring instruction can be
   written from evidence rather than from memory.
4. **Correct a stale claim.** A report from 2026-07-28 states flatly that there is no Google Drive
   on this machine. There is. That line has been annotated in place.

**Jargon, defined once.** *Archive* = a `.zip` holding one research phase's evidence files.
*Sidecar* = a small `.sha256` text file next to an archive holding its fingerprint. *sha256 hash* =
a 64-character fingerprint; two files with the same hash are byte-for-byte identical, and any
single-byte corruption produces a completely different hash. *Off-machine* = a copy that survives
this laptop dying. *Porcelain* = `git status` in its script-readable form.

---

## 1 · Gates and probes, as printed

```
pwd=/c/Users/luisf/OneDrive/Desktop/Midas-Claude Code Resources/naiad  branch=v12-v1-census  head=2bb8841
  G: reachable
```

All four preconditions passed: correct clone (path contains `OneDrive`…`naiad`), correct branch
(`v12-v1-census`), `G:/My Drive/naiad-backups` reachable, source archive and its sidecar both
present.

Destination pre-state, checked before any write — this is what made the no-clobber guard meaningful
rather than decorative:

```
ls: cannot access 'G:/My Drive/naiad-backups/phases': No such file or directory
```

`G:/My Drive/naiad-backups` before this run:

```
  naiad_estate_2026-07-28.zip        492,306,779      + .sha256
  naiad_estate_2026-08-02.zip        493,542,600      + .sha256
  naiad_workflow_2026-08-02.zip        1,132,236      + .sha256
  naiad_workflow_2026-08-04.zip        1,794,646      + .sha256
  operator-exports/                   (directory)
```

That is 988,776,261 B ≈ **988 MB** of estate and workflow archives — and **zero phase archives**,
which is precisely the gap this session closed.

---

## 2 · TC5 taken off-machine — the three-way hash, verbatim

```
--- source ---
  research_outputs\_archive\tc5_2026-08-02.zip  18375498 bytes
  sidecar recorded hash : 68942d6261bf8ca8d551e52aa6e4d374f8c9fb6e0ac5be5da96b188e928b4357
  fresh local hash      : 68942d6261bf8ca8d551e52aa6e4d374f8c9fb6e0ac5be5da96b188e928b4357   (18375498 bytes, 0.0s)
  local integrity       : OK (matches sidecar)
  CREATED destination folder: G:/My Drive/naiad-backups/phases
--- copying ---
  COPIED in 0.1s
  fresh hash RE-READ FROM DRIVE : 68942d6261bf8ca8d551e52aa6e4d374f8c9fb6e0ac5be5da96b188e928b4357   (18375498 bytes, 0.1s)

  HASH MATCH (3-way: sidecar / local / drive) : YES
  tc5 IS NOW OFF-MACHINE AND VERIFIED.
```

**The three values that must agree, stated separately so they can be checked independently:**

| # | what was measured | value |
|---|---|---|
| 1 | hash recorded in the sidecar on 2026-08-02 | `68942d6261bf8ca8d551e52aa6e4d374f8c9fb6e0ac5be5da96b188e928b4357` |
| 2 | hash computed fresh from the local file today | `68942d6261bf8ca8d551e52aa6e4d374f8c9fb6e0ac5be5da96b188e928b4357` |
| 3 | hash computed fresh by **re-reading the file back off Drive** | `68942d6261bf8ca8d551e52aa6e4d374f8c9fb6e0ac5be5da96b188e928b4357` |

Size agreed at **18,375,498 B** on all three. **Copy time: 0.1 s. Verification read-back: 0.1 s.**

**Why value 3 is the one that matters.** Copying a file and then hashing the *source* again proves
nothing about the destination — it just re-reads the file you already had. The hash here was taken
by opening the file **on `G:` and reading it back**, so it tests what actually landed on Drive.
Value 1 additionally proves the local file had not silently rotted since 2026-08-02.

**Caveat, stated honestly:** `G:` is a Google Drive *streaming* mount. A read-back immediately after
a write can in principle be served from the local Drive cache rather than from Google's servers, so
this proves the file was written correctly through the Drive client — not that it has finished
uploading. Confirming the upload requires checking the Drive web UI or waiting for the client to
report sync complete. **That is the one action left to the operator: click Sync now.**

---

## 3 · Legacy snapshot spot-check — and a correction to the check itself

### 3a · The check as specified did not test anything

The paste specified spot-checking `analytics_v1.0.0_2026-07-29.zip` inside the legacy snapshot. It
printed:

```
  analytics_v1.0.0_2026-07-29.zip not present in the legacy folder
```

That is not a fault in the snapshot. **The legacy snapshot is the 2026-07-27 archive set; the
`analytics` archive is dated 2026-07-29 and was created two days after the snapshot was taken.** It
was never going to be there. Had I stopped at that line, the report would have recorded a null
result and the operator's actual question — *is the legacy snapshot intact?* — would still be open.

A second obstacle: **the legacy folder contains no `.sha256` sidecars at all**, so there is nothing
inside it to check an archive against. Full listing, confirming both facts:

```
  legacy folder contents:
    s1_2026-07-27.zip                                   106239157
    s2_2026-07-27.zip                                   246355294
    s3_2026-07-27.zip                                   269919602
    tc1_2026-07-27.zip                                  242926299
    tc4_2026-07-27.zip                                   68700167
    v3_anchor_2026-07-27.zip                             91049070
```

```
  --- does the legacy folder hold ANY sidecar? ---
  .  ..  s1_2026-07-27.zip  s2_2026-07-27.zip  s3_2026-07-27.zip
  tc1_2026-07-27.zip  tc4_2026-07-27.zip  v3_anchor_2026-07-27.zip
```

Six archives, no sidecars, 1,025,189,589 B ≈ **1,025 MB**.

### 3b · The check I ran instead, and its verdict

With no sidecars available, the only valid comparison basis is the local copy of the same archive.
I ran two checks — cheap size parity across **all six**, then a **full hash** of one:

```
--- size parity across ALL 6 legacy archives (cheap full check) ---
  s1_2026-07-27.zip            legacy=   106239157  local=   106239157  SAME
  s2_2026-07-27.zip            legacy=   246355294  local=   246355294  SAME
  s3_2026-07-27.zip            legacy=   269919602  local=   269919602  SAME
  tc1_2026-07-27.zip           legacy=   242926299  local=   242926299  SAME
  tc4_2026-07-27.zip           legacy=    68700167  local=    68700167  SAME
  v3_anchor_2026-07-27.zip     legacy=    91049070  local=    91049070  SAME
  all six size-identical to local: YES

--- FULL hash spot-check: tc4_2026-07-27.zip (legacy vs local) ---
  legacy(Drive) : 794036c2d613528530272864aa866421af0cbf9de2db5a2423fa7e0b25eb1933  (68700167 bytes, 4.9s)
  local         : 794036c2d613528530272864aa866421af0cbf9de2db5a2423fa7e0b25eb1933  (68700167 bytes, 0.1s)
  verdict       : MATCH - legacy snapshot content verified intact
```

**Verdict: the legacy snapshot is intact** — one 68.7 MB archive proved byte-identical to its local
twin, and all six match on size.

**How strong this evidence is, stated precisely.** One of six archives was hashed in full; the other
five were checked on size only. Size parity catches truncation and failed copies but *not*
silent single-byte corruption. So: **tc4 is proven; the other five are consistent with being
intact but are not proven.** Hashing all six would take roughly 75 s of Drive reads and is cheap if
the operator wants certainty.

Note the read-time asymmetry — **4.9 s from Drive against 0.1 s locally**, a ~50× difference. That
is real network/streaming cost and is the practical reason full verification of all six was not done
unasked.

### 3c · What the legacy snapshot does and does not cover

It holds the **2026-07-27** set. Comparing against the current local archive folder:

| archive | in legacy snapshot | in `naiad-backups` |
|---|---|---|
| `s1`, `s2`, `s3`, `tc1`, `tc4`, `v3_anchor` (all 2026-07-27) | yes | no |
| `tc5_2026-08-02.zip` | **no** | **yes — as of this run** |
| `analytics_v1.0.0_2026-07-29.zip` | **no** | **no** |
| `analytics_tests_v1.0.0_2026-07-29.zip` | **no** | **no** |

**Finding, reported not fixed:** two archives — `analytics_v1.0.0_2026-07-29.zip` (19,641 B) and
`analytics_tests_v1.0.0_2026-07-29.zip` (6,816 B) — exist **only on this laptop**. They are small
and were outside this paste's scope, so I did not move them. Per the operator ruling the legacy
snapshot is a one-off and will not pick them up on its own. **Owner: operator, to rule on.**

---

## 4 · `backup_estate.py` `--phase` mode — the full read

**This is the section the wiring instruction should be written from.** Nothing here was edited; the
file is untouched at **1,184 lines**.

### 4a · The finding in one sentence

**`--phase` writes its archive to a hardcoded folder inside the repo and has no concept of an
off-machine destination. It silently ignores `--dest`.** That is the entire reason `tc5` had to be
copied to Drive by hand today.

### 4b · Every line mentioning "phase", as printed

```
  7:directions -> only then consider the source releasable, per-phase atomic, with
  23:  --phase <name>      one research_outputs/<name> subtree.
  35:DELETION -- deliberately opt-in.  The spec for --phase permits deleting
  64:  generations plus 1 phase set".  The phase clause was WRONG and is removed:
  65:  phase archives are not generations of one thing, so keeping only the newest
  67:  is now "keep the newest 4 estate + 4 workflow generations; phase archives are
  78:  PUBLISH.  --estate and --phase runs end by staging exchange/** ONLY, checking
  108:# CORRECTED 2026-08-03.  `KEEP_PHASE_SETS = 1` is REMOVED, not retuned.
  110:# The old rule grouped phase archives by date and kept only the newest dated
  113:# direction: PHASE ARCHIVES ARE NOT GENERATIONS OF ONE THING.  s1, s2, s3, tc1,
  114:# tc4, tc5 and v3_anchor each hold a DIFFERENT phase's evidence.  An older phase
  119:# as "outside the rule", including every study phase except the most recently
  128:# Phase archives have no keep-count. They are permanent evidence.
  567:    the Drive.  It is NOT true for --phase, which writes into
  570:    asserts nothing changed.  F-K3 failed on the first live --phase run
  724:    PHASE ARCHIVES ARE NEVER PRUNABLE.  Each holds a different phase's evidence,
  737:                 f"**Phase archives are permanent evidence and are never prunable.**")
  772:    # --- phase archives: PERMANENT ------------------------------------------
  775:    lines.append("## PHASE ARCHIVES — PERMANENT EVIDENCE, NEVER PRUNE")
  777:    lines.append("Each phase archive holds a DIFFERENT phase's evidence, so an older "
  787:    phases = sorted((p for p in arch.glob("*.zip") if p.is_file()),
  789:    if not phases:
  793:    total = sum(p.stat().st_size for p in phases)
  794:    lines.append(f"{len(phases)} archive(s), {total:,} B "
  799:    for p in phases:
  804:    lines.append("There is no keep-count for phase archives and no circumstance "
  1023:def run_phase(name: str, args) -> int:
  1027:        sys.stderr.write(f"no such phase directory: {src}\n")
  1042:    print(f"phase      : {name}")
  1051:        "mode": "phase",
  1052:        "phase": name,
  1077:    # --phase writes its archive INSIDE the repo, so F-K3 must be told which
  1129:          f"{'/' + man['phase'] if man.get('phase') else ''}")
  1155:    g.add_argument("--phase", metavar="NAME",
  1162:                    help="--phase only: release untracked sources after zero mismatches")
  1172:    if args.phase:
  1173:        return run_phase(args.phase, args)
```

### 4c · Argument parsing and destination defaults, as printed

```
  85:import argparse
  655:    SIDESTEP without overwriting. Asserting only the refusal would let the new
  1030:    dest = REPO / "research_outputs" / "_archive"
  1147:    ap = argparse.ArgumentParser(description=__doc__,
  1148:                                 formatter_class=argparse.RawDescriptionHelpFormatter)
  1150:    g.add_argument("--estate", action="store_true",
  1152:    g.add_argument("--workflow", action="store_true",
  1155:    g.add_argument("--phase", metavar="NAME",
  1157:    g.add_argument("--verify", metavar="ZIP",
  1159:    ap.add_argument("--dest", metavar="DIR",
  1161:    ap.add_argument("--delete-source", action="store_true",
  1163:    ap.add_argument("--force-same-day", action="store_true",
```

**Line 1030 is the whole finding:** `dest = REPO / "research_outputs" / "_archive"`.

### 4d · `run_phase()` in full — source lines 1023–1117

```python
1023  def run_phase(name: str, args) -> int:
1024      env = assert_environment(None, need_writable=False)
1025      src = REPO / "research_outputs" / name
1026      if not src.is_dir():
1027          sys.stderr.write(f"no such phase directory: {src}\n")
1028          return 2
1029
1030      dest = REPO / "research_outputs" / "_archive"
1031      dest.mkdir(parents=True, exist_ok=True)
1032      date = datetime.now().strftime("%Y-%m-%d")
1033      target = dest / f"{name}_{date}.zip"
1034      sidecar = target.with_suffix(".zip.sha256")
1035      force_sd = bool(getattr(args, "force_same_day", False))
1036      target = assert_no_clobber(target, force_sd)
1037      sidecar = assert_no_clobber(target.with_suffix(".zip.sha256"), force_sd)
1038
1039      rel_dir = f"research_outputs/{name}"
1040      tracked = git_tracked_under(rel_dir)
1041      members = walk_members(src)
1042      print(f"phase      : {name}")
1043      print(f"source     : {src}")
1044      print(f"members    : {len(members)}  (git-tracked among them: {len(tracked)})")
1045
1046      before_status = git_porcelain()
1047      sample = [(rel, ap, sha256_file(ap)) for rel, ap in members[:20]]
1048
1049      meta = {
1050          "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
1051          "mode": "phase",
1052          "phase": name,
1053          "estate_root": str(src),
1054          "repo_root": str(REPO),
1055          "naiad_cache_dir_override": os.environ.get("NAIAD_CACHE_DIR"),
1056          "inside_onedrive": inside(src, env["onedrive_root"]),
1057          "repo_head": env["head"],
1058      }
1059
1060      print("  compressing...")
1061      manifest = build_archive(members, target, meta)
1062      archive_sha = sha256_file(target)
1063      sidecar.write_text(f"{archive_sha}  {target.name}\n", encoding="utf-8")
1064
1065      print("  verifying (bidirectional)...")
1066      res = verify_archive(target, src, None, check_sources=True)
1067
1068      print("\nFIXTURES")
1069      fx = Fixtures()
1070      clean = (not res["mismatches"] and not res["strays"]
1071               and not res["omissions"] and res["verified"] == res["members"])
1072      fx.record("F-K1", clean,
1073                f"{res['verified']}/{res['members']} members verified both directions; "
1074                f"{len(res['mismatches'])} mismatches, {len(res['strays'])} strays, "
1075                f"{len(res['omissions'])} omissions")
1076      fx.na("F-K2", "completeness vs census.json applies to --estate only")
1077      # --phase writes its archive INSIDE the repo, so F-K3 must be told which
1078      # paths are this run's own output (see _porcelain_minus_outputs).
1079      fk3_source_untouched(fx, sample, before_status, outputs=[
1080          target.relative_to(REPO).as_posix(),
1081          sidecar.relative_to(REPO).as_posix(),
1082      ])
1083      fk4_restore_rehearsal(fx, target)
1084      fk5_destination_verification(fx, target, archive_sha, sidecar)
1085      fk6_no_clobber(fx, target)
1086      fk7_tracked_preserved(fx, tracked)
1087
1088      releasable = [rel for rel, _ in members if f"{rel_dir}/{rel}" not in tracked]
1089      if not fx.ok:
1090          print("\nfixtures failed -- source kept, nothing released")
1091      elif args.delete_source:
1092          if not clean:
1093              print("\nmismatches present -- source kept, run aborted")
1094              return 1
1095          freed = 0
1096          for rel, ap in members:
1097              if f"{rel_dir}/{rel}" in tracked:
1098                  continue
1099              freed += ap.stat().st_size
1100              ap.unlink()
1101          print(f"\nreleased {len(releasable)} untracked files, {freed:,} B; "
1102                f"{len(tracked)} tracked files preserved in place")
1103      else:
1104          print(f"\n--delete-source not given: source kept intact. "
1105                f"{len(releasable)} untracked files ({len(members) - len(releasable)} tracked) "
1106                f"would be releasable.")
1107
1108      print(f"\narchive   : {target}")
1109      print(f"size      : {target.stat().st_size:,} B")
1110      print(f"sha256    : {archive_sha}")
1111      print(f"members   : {manifest['file_count']}")
1112      print(f"\n{sum(1 for _, p, _ in fx.rows if p)}/{len(fx.rows)} fixtures pass")
1113
1114      pub = publish_step()
1115      if pub["status"] in ("FLAGGED", "ERROR"):
1116          return 1
1117      return 0 if fx.ok else 1
```

### 4e · The CLI dispatcher in full — source lines 1146–1180

```python
1146  def main() -> int:
1147      ap = argparse.ArgumentParser(description=__doc__,
1148                                   formatter_class=argparse.RawDescriptionHelpFormatter)
1149      g = ap.add_mutually_exclusive_group()
1150      g.add_argument("--estate", action="store_true",
1151                     help="archive the price estate (default)")
1152      g.add_argument("--workflow", action="store_true",
1153                     help="archive the workflow estate (memory, knowledge, skills, "
1154                          "prompts, claude, exchange, primers, history, operator exports)")
1155      g.add_argument("--phase", metavar="NAME",
1156                     help="archive one research_outputs/<NAME> subtree")
1157      g.add_argument("--verify", metavar="ZIP",
1158                     help="verify an existing archive against its embedded manifest")
1159      ap.add_argument("--dest", metavar="DIR",
1160                      help="destination directory (required for --estate and --workflow)")
1161      ap.add_argument("--delete-source", action="store_true",
1162                      help="--phase only: release untracked sources after zero mismatches")
1163      ap.add_argument("--force-same-day", action="store_true",
1164                      help="if the target exists AND was written TODAY, append -NN "
1165                           "instead of halting. Both files are kept; nothing is "
1166                           "overwritten. Does NOT apply to archives from an "
1167                           "earlier day, which still refuse.")
1168      args = ap.parse_args()
1169
1170      if args.verify:
1171          return run_verify(Path(args.verify))
1172      if args.phase:
1173          return run_phase(args.phase, args)
1174      if args.workflow:
1175          if not args.dest:
1176              ap.error("--workflow requires --dest")
1177          return run_workflow(Path(args.dest), args)
1178      if not args.dest:
1179          ap.error("--estate requires --dest")
1180      return run_estate(Path(args.dest), args)
```

### 4f · The design comment that explains why it is this way — lines 561–578

```python
561  def _porcelain_minus_outputs(text: str, outputs: list) -> list:
562      """Porcelain lines with THIS RUN'S OWN outputs removed.
563
564      F-K3 asks "were the sources touched?".  It answered that by comparing raw
565      `git status` before and after, which works only while every output lands
566      outside the repo -- true for --estate and --workflow, whose destination is
567      the Drive.  It is NOT true for --phase, which writes into
568      research_outputs/_archive/.  There the .zip is ignored by *.zip but the
569      .sha256 sidecar is not, so the run creates a new untracked entry and then
570      asserts nothing changed.  F-K3 failed on the first live --phase run
571      (2026-08-02, tc5) for exactly that reason -- and because releasing sources
572      is gated on fx.ok, --delete-source could never have fired either.
573
574      Two forms are dropped, and only these two: a line naming an output exactly,
575      and a collapsed directory entry (git prints `?? dir/` rather than listing a
576      wholly-untracked directory's contents) that CONTAINS an output.  Everything
577      the run did not write stays in the comparison and still fails the fixture.
578      """
```

### 4g · What the source proves — analysis for the wiring instruction

**1. `--phase` cannot write off-machine. There is no code path for it.**
Line 1030 assigns `dest` unconditionally. `args.dest` is **never read** inside `run_phase`. Line
1173 passes `args` through, so the value is available — it is simply not consulted.

**2. `--dest` is silently ignored for `--phase`. This is a live footgun.**
`--dest` is defined at 1159 on the top-level parser, not inside the mutually-exclusive group, so
`--phase tc5 --dest "G:/My Drive/naiad-backups/phases"` **parses cleanly, exits 0, prints success —
and writes only inside the repo.** No error, no warning. An operator would reasonably believe the
archive went to Drive. Compare `--estate`/`--workflow`, which hard-fail via `ap.error()` at 1176 and
1179 when `--dest` is missing. **`--phase` is the one mode where the destination flag lies.**

**3. The asymmetry is deliberate and documented, not an oversight in intent.**
The docstring at 566–567 states it outright: `--estate` and `--workflow` have "the Drive" as their
destination; `--phase` "writes into `research_outputs/_archive/`". The in-repo destination is a
design decision. What is missing is any *second* step taking the result off-machine.

**4. There is a known consequence already paid once.**
Lines 570–572: F-K3 failed on the first live `--phase` run (2026-08-02, tc5) because the run's own
sidecar appeared as a new untracked file. Because source release is gated on `fx.ok` (line 1089),
`--delete-source` could never have fired. That was fixed by teaching F-K3 to ignore the run's own
outputs (1079–1082) — a fix that exists **only because** the destination is inside the repo.

**5. The gitignore split matters for any rewiring.**
Verified this run: `research_outputs/_archive/tc5_2026-08-02.zip` is **ignored** by
`.gitignore:38:*.zip`, while `research_outputs/_archive/tc5_2026-08-02.zip.sha256` is **tracked**.
So today the fingerprint travels to GitHub while the archive does not. Any change to `dest` must
keep that asymmetry in mind — moving the archive out of the repo also moves the sidecar out, and
the sidecar is currently the only part of a phase archive that is backed up by GitHub.

**6. F-K5 already exists and would carry over.**
`fk5_destination_verification(fx, target, archive_sha, sidecar)` at line 1084 already verifies the
written destination. Pointing `--phase` at a Drive folder would reuse it rather than need new
verification logic — the three-way check performed manually today is close to what F-K5 does.

**Options for the wiring instruction, with implications — operator's call, nothing implemented:**

| option | what it does | implication |
|---|---|---|
| **A — add an optional `--mirror DIR`** | after F-K5 passes, copy archive + sidecar off-machine | in-repo behaviour and F-K3's output-exclusion stay exactly as they are; smallest change; the archive lands in both places |
| **B — honour `--dest` for `--phase`** | write the archive straight to Drive | removes the need for the F-K3 exclusion for the `.zip`, but the tracked `.sha256` sidecar's location must be decided separately, and `--delete-source` semantics need re-reading |
| **C — make `--phase --dest` an error** | `ap.error()` like the other two modes | fixes only the silent-lie footgun, closes nothing on backup; cheap and could ship alongside A |
| **D — leave it, copy by hand** | what happened today | works, but depends on someone remembering; this is the status quo that left tc5 exposed for two days |

**My recommendation: A plus C.** A closes the backup gap with the least disturbance to fixtures that
were only recently stabilised; C removes a flag that currently reports success while doing nothing.

---

## 5 · The stale Drive claim — corrected, but not where the paste aimed

### 5a · Deviation from the paste, and why

The paste selected its target with
`grep -rl "no Google Drive on this machine" --include="*.md" . | grep -v boxrescue | head -1`.
**Three files match. `head -1` picks the wrong one.**

```
  ./exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_CONVENTIONS-MERGE-AND-ARCHIVE-AUDIT.md:230
  ./exchange/reports/FIXUP_2026-07-28.md:111
  ./exchange/reports/SETUP_2026-07-28.md:124
```

| file | what the line actually is | correct action |
|---|---|---|
| `BUILDERS_REPORT…ARCHIVE-AUDIT.md:230` | **what `head -1` selected.** Narrates the audit by *quoting* SETUP's finding, then notes it contradicted a `[verified]` FACT line | **leave alone** — the sentence is true; it accurately reports what another document said |
| `FIXUP_2026-07-28.md:111` | already records the supersession: *"is superseded — it was correct when written"* | **leave alone** — already correct |
| `SETUP_2026-07-28.md:124` | **the actual stale assertion:** *"Finding: there is no Google Drive on this machine…"* | **correct this one** |

Running the paste as written would have **overwritten a true sentence in the audit report** — the
fragment appears there exactly once, so the `n != 1` guard would have passed and let it through —
while leaving the genuinely false claim standing. I corrected `SETUP_2026-07-28.md:124` instead and
left the other two untouched. **Authority: the task line "correct one stale Drive claim"; there is
exactly one stale claim and this is it.** Fully reversible — see rollback below.

### 5b · A factual error in the supplied correction text, fixed

The supplied text asserted *"Between 2026-07-28 and 2026-08-04 Drive was installed or reconnected."*
**That span is wrong.** `FIXUP_2026-07-28.md` — dated the *same day* as the SETUP report — already
records Drive for Desktop installed and running with two `GoogleDriveFS` processes. The install
happened **on 2026-07-28, shortly after the SETUP report was written**, not at some unknown point
across the following week. I wrote the accurate version rather than commit a knowingly false
sentence into a correction notice.

I also narrowed one clause: the blocker is resolved **for `--estate` and `--workflow`**, but
`--phase` is still unwired to Drive for the separate reason established in §4. Declaring the blocker
resolved outright would have contradicted this same report.

### 5c · The line as it now stands

`exchange/reports/SETUP_2026-07-28.md` line 124, replacing the bare finding:

> **CORRECTED 2026-08-04 — this is no longer true.** `G:` IS mounted and holds 988 MB of estate and
> workflow archives under `G:/My Drive/naiad-backups`, plus a separate one-off legacy snapshot and,
> as of 2026-08-04, a `phases/` folder. Drive for Desktop was installed on **2026-07-28, the same
> day as this report and shortly after it was written** — see `FIXUP_2026-07-28.md`, which recorded
> two `GoogleDriveFS` processes running and correctly noted that this finding "was correct when
> written". The blocker this line recorded on `backup_estate.py`'s offsite target is RESOLVED for
> `--estate` and `--workflow`; `--phase` remains unwired to Drive by a separate cause (it hardcodes
> an in-repo destination — see the 2026-08-04 TC5-OFFSITE build report). Superseded text: “**Finding:
> there is no Google Drive on this machine. Not a streaming mount, not a local folder, not
> installed.**”

The original wording is preserved verbatim inside the annotation, so nothing was destroyed.

**Finding, reported not fixed:** the same document's line 139 carries the downstream conclusion —
*"PENDING item 3 (`backup_estate.py`) is blocked… there is no Drive path for Part B to supply"* —
and the surrounding evidence table still reads "Google Drive path | **none found**". The correction
at 124 addresses this in substance, but line 139 was outside the "one stale claim" scope and remains
uncorrected. **Owner: operator.**

---

## 6 · Fixture-equivalent transcript for this run

This paste ran no `Fixtures()` harness; these are the equivalent assertions it made and their
results.

| # | assertion | result |
|---|---|---|
| G1 | working directory is the local clone (`*OneDrive*naiad*`) | **PASS** |
| G2 | branch is `v12-v1-census` | **PASS** |
| G3 | `G:/My Drive/naiad-backups` reachable | **PASS** |
| G4 | source archive `tc5_2026-08-02.zip` exists | **PASS** (18,375,498 B) |
| G5 | local archive matches its own sidecar before copying | **PASS** |
| G6 | destination does not already exist (no-clobber) | **PASS** — `phases/` did not exist; folder created |
| G7 | Drive copy re-read matches local hash and byte count | **PASS** |
| G8 | 3-way agreement sidecar / local / drive | **PASS** |
| G9 | legacy snapshot spot-check | **PASS with substitution** — specified file absent by design; `tc4` hashed instead, MATCH |
| G10 | `backup_estate.py` unmodified by this run | **PASS** — read-only, 1,184 lines, no writes |
| G11 | `research_outputs/` treated as read-only source | **PASS** — nothing moved, deleted or rewritten |
| G12 | stale-claim fragment appears exactly once in the corrected file | **PASS** — one occurrence in `SETUP_2026-07-28.md` |
| G13 | corrected file is LF-only, so `newline=''` rewriting cannot reflow it | **PASS** — CR=0, LF=328 |
| G14 | no literal backslash in any path used by this paste | **PASS** — forward slashes throughout |

**Line-ending note.** The supplied step-5 editor read with universal newlines and wrote with
`newline=''`, which silently converts a CRLF file to LF **across its whole length** — turning a
one-line correction into a whole-file diff. I checked first (CR=0) and confirmed it was safe here.
Flagging it because the pattern recurs in these pastes and will eventually meet a CRLF file.

---

## 7 · What changed, and what is still exposed

**Closed today:** `tc5_2026-08-02.zip` now exists off-machine, hash-verified. The phase-archive
backup gap is closed *for tc5 specifically*.

**Still exposed — the honest list:**

| item | where it lives | risk |
|---|---|---|
| `analytics_v1.0.0_2026-07-29.zip` (19,641 B) | **this laptop only** | lost with the machine |
| `analytics_tests_v1.0.0_2026-07-29.zip` (6,816 B) | **this laptop only** | lost with the machine |
| `s1/s2/s3/tc1/tc4/v3_anchor` 2026-07-27 | laptop + legacy one-off snapshot | covered, but by a snapshot the operator has ruled **not maintained** |
| every *future* phase archive | laptop only until copied by hand | `--phase` still has no off-machine wiring (§4) |

**The structural point:** today's fix was manual. Until `--phase` is wired (§4g option A), every new
phase archive repeats this exposure by default, and the legacy snapshot — being a one-off — will not
catch it.

---

## 8 · Publishing

`git status --porcelain -- exchange/` before publish:

```
   M exchange/reports/SETUP_2026-07-28.md
```

The corrected document lives **inside `exchange/`**, so the publish guard carries it. The paste's
conditional branch for an authorized commit of a doc outside `exchange/` **did not fire and was not
needed**. Publish result is recorded in the session's on-screen close.

---

## 9 · Rollback

- **Drive copy:** delete `G:/My Drive/naiad-backups/phases` (removes the archive and its sidecar;
  the local originals are untouched).
- **Corrected document:** `git checkout -- exchange/reports/SETUP_2026-07-28.md` while unpushed;
  after publish, `git revert <publish sha>`.
- **`backup_estate.py`:** nothing to roll back — read-only this session.
- **`research_outputs/`:** nothing to roll back — read-only this session.

---

## 10 · FILE DISPOSITION TABLE

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY |
|---|---|---|---|---|---|
| `exchange/reports/SETUP_2026-07-28.md` | yes | tracked | see publish sha in on-screen close | yes (`origin/v12-v1-census`) | GitHub + `--workflow` archive |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_TC5-OFFSITE-AND-PHASE-MODE-READ.md` | yes | tracked on publish | see publish sha in on-screen close | yes (`origin/v12-v1-census`) | GitHub + `--workflow` archive |
| `G:/My Drive/naiad-backups/phases/tc5_2026-08-02.zip` | yes | n/a — **outside the repo** | n/a | n/a | **Google Drive (this is the off-machine copy)** |
| `G:/My Drive/naiad-backups/phases/tc5_2026-08-02.zip.sha256` | yes | n/a — **outside the repo** | n/a | n/a | Google Drive |
| `research_outputs/_archive/tc5_2026-08-02.zip` | yes | **ignored** — `.gitignore:38:*.zip` | never | no | phase archive on Drive **as of today**; not GitHub |
| `research_outputs/_archive/tc5_2026-08-02.zip.sha256` | yes | tracked | previously committed | yes (`origin/v12-v1-census`) | GitHub |
| `scripts/backup_estate.py` | yes | tracked | unchanged this run | unchanged | GitHub + `--workflow` archive |

**Read this table as:** *committed is not pushed, pushed is not backed up.* The two `G:` rows are the
only ones that survive losing this laptop **and** losing GitHub. The `.zip` row is ignored by git by
design — GitHub protects its fingerprint, not its contents.

**Per §3.1, this document does not state its own sha256** — that value is stale the instant it is
written.

---

## 11 · What remains open, with owners

| # | open item | owner |
|---|---|---|
| 1 | Wire `--phase` for off-machine output — recommend §4g **A + C** | operator to rule, HEPHAESTUS to build |
| 2 | Two `analytics` archives exist only on this laptop | operator |
| 3 | Five of six legacy archives verified on size only, not hashed (~75 s to close) | operator |
| 4 | `SETUP_2026-07-28.md:139` still states the offsite target is blocked | operator |
| 5 | Confirm Drive upload actually completed — **click Sync now** | operator |
