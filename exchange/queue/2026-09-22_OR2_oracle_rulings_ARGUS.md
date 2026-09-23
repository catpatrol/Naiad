# QUEUE OR-2 — THE DAILY ORACLE · the first edition's rulings
RATIFIED: operator, 2026-09-22 — verbatim "leans", adopting ARGUS's stated leans on
R-1..R-8 of 2026-09-22. Executor HEPHAESTUS, reviewer ARGUS. Operations/display-only;
BR-1 §2 firewall and OR-1's clause (no gate, filter or sizing reads a range or a
mover) binding. BUILT: PENDING

## SPECIFICATION OF RECORD (the operator's paste, verbatim)

ENVIRONMENT: local Mac builder, repo ~/Naiad, branch v12-v1-census. Fresh session.
LAW (OR-1's lesson): SPEC FIRST; ONE COMMIT PER STEP ("or2: step N — <what>"); terse
terminal output, full transcripts to the build doc. If budget runs low, stop at a step
boundary, append a ledger checkpoint naming the steps remaining, publish. Never leave a
step half-applied. Every oracle_daily.py change re-pins the top-up in the SAME commit
(F-TU-1 green before moving on).

STEP 0 — HARD GATE: git rev-parse --short HEAD; pwd. HALT unless pwd == $HOME/Naiad;
HALT on OneDrive / com~apple~CloudDocs / Mobile Documents / .tmp.driveupload; branch
v12-v1-census (HARD). git status --short: if any Oracle-owned path is already modified,
HALT and report — this contract starts clean. FOREIGN paths (other lanes,
scripts/tierc6*.py) are never staged, stashed or restored. Confirm no com.naiad.oracle-*
agent is loaded; record the mtimes of the five retained plists as the baseline for G-1.

STEP 1 — SPEC OF RECORD: file exchange/queue/2026-09-22_OR2_oracle_rulings_ARGUS.md —
header below, then this ENTIRE paste verbatim, so any interruption resumes from the repo:
  # QUEUE OR-2 — THE DAILY ORACLE · the first edition's rulings
  RATIFIED: operator, 2026-09-22 — verbatim "leans", adopting ARGUS's stated leans on
  R-1..R-8 of 2026-09-22. Executor HEPHAESTUS, reviewer ARGUS. Operations/display-only;
  BR-1 §2 firewall and OR-1's clause (no gate, filter or sizing reads a range or a
  mover) binding. BUILT: PENDING
Commit.

STEP 2 — R-4 · GUARD THE STRAY ARMING COMMAND (safety first). Create the sentinel
research_outputs/oracle/SCHEDULE_SUSPENDED (date, ruling, the exact re-arm command).
In oracle_wrapper.py: while the sentinel exists, `--install` alone REFUSES — exit 2,
nothing touched, a message naming the explicit path `--install --rearm`. On the explicit
path: enable, bootstrap, verify via launchctl list, and every bootstrap rc reaches the
exit code — "ARMED" prints only on rc 0 (closes OR1-b's false-ARMED half). The explicit
path is NEVER exercised against the real gui domain in this build. F-SK-4 runs against
a fake-launchctl shim only: sentinel present → exit 2, plist mtimes unchanged, shim
records zero calls; break leg removes the guard → shim records bootout/bootstrap → RED.
Commit.

STEP 3 — R-1 · PER-SYMBOL STALENESS. Every Board row carries its own as-of bar and AGE
(4h bars and hours). A row is STALE when its bar is older than the A2-7 limit (import
the existing constant; never retype it). Stale rows: STALE chip + age on the Board and
on the Docket card header. TELEGRAMS: a stale symbol's R1 lines LEAVE the paste-ready
block entirely and appear beneath it under "HELD — stale wire", struck through, for
reference only (formatting dies on copy-paste; exclusion does not). Dateline prints the
newest AND the oldest row as-of (no longer the hottest asset's). The LATE EDITION band
fires when ANY row is stale and names the count: "LATE EDITION — N of R rows on a stale
wire (oldest <as-of>)". The wrapper's front-page report-back prints the stale count.
F-BR-18 two-leg, replaying the skeptic's OR1-a plant (one symbol's tape cut back 3 days
in memory): its row reads STALE with its age; its R1 lines are absent from the paste
block and present under HELD; the band names 1 of R. Break leg restores the hottest-
asset-only as-of → RED. Re-pin. Commit.

STEP 4 — R-2 · POSTURE-FIRST BOARD. Named constant BOARD_ORDER = (TRIGGERED, ARMED,
STALKING, DEAD); heat descending within each posture. Enumerate every consumer of the
heat sort (grep NAME + call sites; print the table) and apply posture-first to the
Board, the Docket order and the front-page report-back only. Heat VALUES unchanged and
still printed. F-BR-19 two-leg: on a real edition no row sits above a row of higher
posture, and heat descends within each posture; break leg plants heat-only sort → RED.
Re-pin. Commit.

STEP 5 — R-3 · EDITION WORD. Full editions: "Morning" when render time in
America/Argentina/Buenos_Aires is before EDITION_NOON = 12, else "Evening"; the refresh
verb keeps "Refresh". F-BR-20 two-leg: planted 09:00 BA → Morning, planted 22:22 BA →
Evening; break leg hardcodes "Morning" → RED. Re-pin. Commit.

STEP 6 — R-7 · PUMPFUN → PUMPUSDT. One exchangeInfo probe confirms PUMPUSDT is
PERPETUAL·TRADING; write research_outputs/oracle/roster_mapping_2026-09-22.json
{PUMPFUNUSDT → PUMPUSDT, ruling R-7}; insert PUMPUSDT into ROSTER at PUMPFUN's place in
the operator's watchlist order (roster 19). Amend F-BR-16: ROSTER == probe KEPT ∪ ruled
mappings, in operator order; break leg applies a mapping without its record → RED.
Re-enumerate top-up scope (+PUMPUSDT × the Oracle's intervals), rebind pairs_sha256,
backfill to BTC-parity depth or listing, whichever is later (no-clobber, contiguity
verified, one line per pair); re-pin; F-TU green. PRINT the other three near-name
matches (dropped name → live contract) for the operator — NOT mapped. Commit.

STEP 7 — R-6 · TAPE SCHEMA v2. The eight range columns stay. Write
research_outputs/oracle/tape/SCHEMA.json registering v1 (through 2026-09-20: its
columns) and v2 (from 2026-09-21: +8 columns, each named with its meaning), plus the
reader rule: concatenate by column union; v1 rows read null. New tapes carry parquet
key-value metadata naiad_tape_schema=2; the 2026-09-21 file is registered by name and
NOT rewritten. F-BR-21 two-leg: every tape file's column set matches exactly one
registered version for its date; a planted unregistered column → RED. Commit.

STEP 8 — R-5 · THE RANGE MODULE STAYS IN engine/. Prepend a module docstring to
engine/rangefinder.py — no code change: "Owner ARGUS · display-only · no gate, filter or
sizing may import this module without an APOLLO registration under G-7 · exception to
BR-1 §2 clause 3 recorded in OR-2". F-RF-1 byte-identical and F-BR-14 green after the
edit. Record the exception in the OR-2 queue file. FILE
exchange/reports/NOTE_ARGUS_to_APOLLO_2026-09-22_rangefinder_engine_tape.md, six lines:
the module's home and commit (1695a69); display-only status proven by F-BR-14; any gate
use is APOLLO's to register under G-7; the TC4 tape carries eight range columns from
2026-09-21 (schema v2, SCHEMA.json pointer); those are range coordinates at event time,
ready for P-RNG wording; nothing is registered. Commit.

STEP 9 — R-8 · RULE THE ELEVEN. In the register and the Colophon appendix, flip to
"ruled: operator 2026-09-22 (R-8)": TOPUP_SLOT · MOVERS_TIMEOUT_S · MOVERS_LOG_TAIL ·
FRONT_PAGE_ROWS · MOVERS_FAILURE_HOLDS_FLAG · CUT_OFF_SIGNALS · EDITION_COUNT ·
RANGE_LENS · RANGE_WATCH_ATR · TARGET_BUCKET_ATR; FRONT_PAGE_HEADLINE ruled with the
note "voice under operator review". Print the unruled-row count before and after.
Re-pin if oracle_daily.py changed. Commit.

STEP 10 — QUEUE HYGIENE (OR1-g): stamp RF-1, RF-2, RF-3 "BUILT: <build document> ·
<commit>", read from BUILD_2026-08-22_RANGEFINDER_V0/V1/V2.md. Print MANIFEST's
queue_ratified_unbuilt before and after. Commit.

STEP 11 — PROOF.
(a) SEMANTIC DIFF: render one frozen view through the OR-1 code (26a27c7) and the new
    code. The diff must be confined to: row order · stale marks and age cells · the HELD
    block · dateline · band text · edition word · register rows · the PUMPUSDT row.
    Heat values, posture words, card fields and non-stale R1 prices byte-identical.
    Print the diff classes.
(b) FULL SUITE: F-BR-1..21 · F-SK-1..4 · F-MV · F-TU · F-RF — tallies only in the
    terminal; transcripts to the build doc.
(c) ONE REAL EDITION, run exactly as the skill runs it (detached, python -u, appended to
    logs/launchd/oracle-ondemand.log): exit code · path · bytes · sha · as-of newest and
    oldest · edition word · stale count · Front Page top 5 in posture order · Edge Watch
    · roster 19.

STEP 12 — CLOSE: ONE build doc exchange/reports/BUILD_2026-09-22_ORACLE_RULINGS.md —
zero-context; rulings verbatim; what changed and what provably did not; fixture
transcripts two-leg; findings reported-not-fixed; disposition + BOX COST. Stamp OR-2
BUILT. LEDGER_ARGUS STATUS block: R-1..R-8 executed · roster 19 · tape schema v2
registered · APOLLO note filed · RF-1..3 stamped · PENDING: PARITY line (today's edition
exists; the gate can close today) · headline voice verdict · V-7 (APOLLO F-C3-e).
Publish per CONVENTIONS §3.4; state the push result plainly; bus-health/box line.

GATES: G-1 no com.naiad.oracle-* loaded · sentinel present · plist mtimes equal the
STEP 0 baseline · G-2 one commit per step, FOREIGN paths untouched · G-3 top-up pin
matches · G-4 suite green with break transcripts · G-5 semantic diff confined to the
listed classes · G-6 today's edition exists with a posture-first Front Page and the
correct edition word · G-7 ledger ends "END STATUS" · G-8 publish names commit + result
· G-9 box below warn. Print the final table; IN BRIGHT COLOURS: the edition path (open
it) + the build document name.

## IN-SESSION RULINGS OF RECORD (operator, 2026-09-23, answering the executor's STEP 0 questions)

The executor found, at STEP 0, that three parts of the paste collide with work already
committed. The operator was asked; the answers below are the operator's selections,
verbatim, and they GOVERN wherever they differ from the paste above.

Q-1 (R-5 / R-6 vs AMENDMENT A-OR1-1 iv, v — already built by the OR-1 recovery, 3d55988):
    the Oracle imports scripts/rangefinder_core.py, not engine/; the main tape's 2026-09-23
    file already carries no range columns (they live in research_outputs/oracle/tape_ranges/);
    TC10's research_outputs/tierc10/STEP0_RECORD.json pins engine/rangefinder.py at sha256
    bbae464fdc8e0e01…
    ANSWER: "A-OR1-1 stands (Recommended)" — engine/rangefinder.py is NOT touched. R-5's
    docstring goes on scripts/rangefinder_core.py, and the APOLLO note names both copies.
    R-6: SCHEMA.json registers v1 (the files before 09-21 and from 09-23 on), v2 for the
    2026-09-21 file only (not rewritten), and the tape_ranges/ sibling schema. No columns
    go back into the main tape.

Q-2 (R-7 vs TC10 F-D-5 — scripts/tierc10_data_fixtures.py compares the filed Oracle roster
    with the ROSTER regex-read from scripts/oracle_daily.py):
    ANSWER: "Now; report F-D-5 (Recommended)" — STEP 6 runs as written; TC10's F-D-5 goes
    RED and is recorded as a finding for TC10 to re-file (close_acts.sh does not re-run it).

Q-3 (STEP 12 publish() pushes the whole branch, including TC10's unpushed commits that
    research_outputs/tierc10/close/close_acts.sh step 1 is meant to push):
    ANSWER: "Withhold push (Recommended)" — commit exchange/** locally, as OR-1 did; report
    the push as WITHHELD; the operator's close_acts.sh pushes everything in one go.

Also carried (no question needed): R-3 (STEP 5) was already built by or1 step F (ff74a90,
A-OR1-1 vii); STEP 5 verifies it, names EDITION_NOON and adds F-BR-20 where missing.
STEP 11(a) diffs against BOTH 26a27c7 (the paste's baseline) and ff74a90 (the last Oracle
code before OR-2), so OR-2's own changes are isolated from the recovery's.

## STEP 0 RECORD (2026-09-23)

HEAD 68cde3e · pwd /Users/luis/Naiad · branch v12-v1-census · no cloud-sync path.
git status at start: M exchange/status/daily/DAILY_2026-09-23.md (auto-publish, not Oracle)
· M research_outputs/tierc10/close/FIXTURES_CLOSE_ledger_append_root.txt (TC10, FOREIGN)
· untracked: .claude/worktrees/, pine/*, research_outputs/{CENSUS-2A…, Cascade…, Naiad Daily
Brief v2…, VIZ3-4/} — all FOREIGN. No Oracle-owned path modified → gate PASS.
launchctl: 0 com.naiad.oracle-* loaded (loaded: com.naiad.daily, .estate, .workflow).
G-1 BASELINE — plist mtimes (epoch · local):
  com.naiad.oracle-0700.plist        1786862922 · 2026-08-16T03:48:42
  com.naiad.oracle-1600.plist        1786862922 · 2026-08-16T03:48:42
  com.naiad.oracle-catchup.plist     1787367695 · 2026-08-22T00:01:35
  com.naiad.oracle-topup-0645.plist  1786862922 · 2026-08-16T03:48:42
  com.naiad.oracle-topup-1545.plist  1786862922 · 2026-08-16T03:48:42

## EXCEPTION OF RECORD — BR-1 §2 clause 3 (R-5, as ruled in-session: Q-1, A-OR1-1 stands)

BR-1 §2 clause 3: "Engine modules imported read-only, trading disabled, never modified."
OR-1 STEP D1 (commit 1695a69, 2026-09-21) CREATED engine/rangefinder.py (960 lines, 49,981 B,
sha256 bbae464fdc8e0e01…) — the one write into engine/ by this lane. It is RECORDED, not undone:
A-OR1-1 iv moved the Oracle's machine to scripts/rangefinder_core.py (3d55988), and the engine
copy stays byte-frozen because TIER-C10 pins it (research_outputs/tierc10/STEP0_RECORD.json,
F-C10-RESUME). The Oracle no longer imports it (F-BR-14 (e)); F-RF-1c/d/e hold the two copies
to one machine. Its disposition — keep, retire or promote — is APOLLO's
(exchange/reports/NOTE_ARGUS_to_APOLLO_2026-09-22_rangefinder_engine_tape.md). R-5's docstring
("Owner ARGUS · display-only · no gate, filter or sizing may import this module without an
APOLLO registration under G-7 · exception to BR-1 §2 clause 3 recorded in OR-2") stands at the
head of scripts/rangefinder_core.py's docstring (OR-2 STEP 8), where it moves no byte below it;
engine/rangefinder.py is untouched (sha256 bbae464f… before and after).
