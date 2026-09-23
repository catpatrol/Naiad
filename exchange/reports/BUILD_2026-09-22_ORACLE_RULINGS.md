# BUILD — OR-2 · THE DAILY ORACLE · the first edition's rulings

Lane: the Oracle (operations / display-only) · Executor HEPHAESTUS · Reviewer ARGUS ·
Branch `v12-v1-census` · Window 2026-09-23 12:30–14:59 BA · Queue
`exchange/queue/2026-09-22_OR2_oracle_rulings_ARGUS.md` (spec of record: the operator's paste
verbatim + the in-session rulings Q-1..Q-3) · RATIFIED operator 2026-09-22, verbatim "leans",
adopting ARGUS's stated leans on R-1..R-8 · BR-1 §2 firewall and OR-1's clause (no gate, filter
or sizing reads a range or a mover) binding.

## §0 THE ONE THING TO READ FIRST

The eight rulings on OR-1's first edition are built, each in its own commit, each proved by a
two-legged fixture. Today's edition — `briefs/oracle/oracle_2026-09-23.html`, Evening, 19 rows, 0 stale, posture-first — printed by the skill's own command, exit 0, self-checks 3/3 PASS.

Three parts of the paste collided with work already built by the OR-1 recovery (A-OR1-1,
3d55988 / ff74a90, drafted after the paste's baseline 26a27c7). The operator was asked at STEP 0
and ruled in-session (Q-1..Q-3, filed verbatim in the queue before any code moved):
**engine/rangefinder.py is NOT touched** (R-5's docstring went on `scripts/rangefinder_core.py`),
**no range column went back into the main tape** (R-6 registers v1, v2-by-name and the sibling),
R-7 ran with TIER-C10's F-D-5 going RED as reported, and **the push is WITHHELD**.

What the operator should look at: the edition (§5); the findings (§7), above all **F-6** —
TIER-C10's F-D-5 fallout is larger than a re-file and its pending close append now says
something no longer true; and the three near-name matches printed for a ruling (§1, R-7).

## §1 THE RULINGS, VERBATIM, AND HOW EACH WAS EXECUTED

The operator's ratification, verbatim: **"leans"** (2026-09-22) — adopting ARGUS's stated leans
on R-1..R-8. The ruling texts are the paste's STEP texts, quoted from the spec of record.

| Ruling | Paste text (abridged; verbatim in the queue) | Executed as | Commit |
|---|---|---|---|
| R-4 | guard the stray arming command: sentinel; `--install` alone refuses (exit 2, nothing touched) naming `--install --rearm`; explicit path enable → bootstrap → verify via `launchctl list`, every rc to the exit code, ARMED only on rc 0; F-SK-4 against a fake-launchctl shim only | as written; the drift re-arm is held by the same sentinel | 5d15d04 (+11bec23) |
| R-1 | per-symbol staleness: own as-of + AGE per row; STALE chip + age on Board and Docket header; stale R1 lines LEAVE the paste block → "HELD — stale wire", struck through; dateline newest AND oldest; band "LATE EDITION — N of R rows on a stale wire (oldest <as-of>)"; report-back prints the count; F-BR-18 | as written; rows aged against the print time run() hands the render (a proof: against its own newest row, no clock) | 862c9f8 |
| R-2 | BOARD_ORDER = (TRIGGERED, ARMED, STALKING, DEAD); heat descending within; Board, Docket, report-back ONLY; heat values unchanged; F-BR-19 | as written; every heat-sort consumer enumerated | 21e70b3 (+11bec23) |
| R-3 | Morning before EDITION_NOON = 12 BA, else Evening; refresh keeps Refresh; F-BR-20 | the rule was ALREADY built by or1 step F (ff74a90); this step named the constant (EDITION_NOON_BA → EDITION_NOON) and added F-BR-20 | 76fc19a |
| R-7 | PUMPFUN → PUMPUSDT: one probe; the mapping record; roster 19 at PUMPFUN's place; F-BR-16 amended; re-enumerate, rebind pairs_sha256, backfill to parity, re-pin; PRINT the other three near-names, NOT mapped | as written | 7797827 (+11bec23) |
| R-6 | tape schema v2: SCHEMA.json v1/v2 + reader rule; new tapes carry naiad_tape_schema; 09-21 by name, not rewritten; F-BR-21 | **as ruled Q-1**: v1 = files before 09-21 AND from 09-23 on; v2 = the one 09-21 file; ranges-1 = the sibling; new tapes stamped '1' / 'ranges-1'; no column moved | b372cb7 (+11bec23) |
| R-5 | docstring on engine/rangefinder.py; F-RF-1 + F-BR-14 green; exception recorded; six-line APOLLO note | **as ruled Q-1**: the docstring heads `scripts/rangefinder_core.py`'s existing docstring; engine/ untouched (bbae464f… before and after); exception recorded in the queue; the note names both copies and says the 8 columns are on the ONE 09-21 file | d71b2fc (+11bec23) |
| R-8 | rule the eleven: register + Colophon read "ruled: operator 2026-09-22 (R-8)"; FRONT_PAGE_HEADLINE "voice under operator review"; unruled count before/after | as written: 28 → 17 | 1b1b4b6 (+11bec23) |
| OR1-g | stamp RF-1..3 BUILT from their build docs; MANIFEST before/after | as written; commits read from git log (the build docs name none) | 5c5167e |

**The in-session rulings (operator, 2026-09-23), verbatim selections:**
- **Q-1** "A-OR1-1 stands (Recommended)" — engine/rangefinder.py is NOT touched; R-5's docstring on
  scripts/rangefinder_core.py; the APOLLO note names both copies; R-6 registers v1 (before 09-21 and
  from 09-23), v2 for 09-21 only, and the sibling; no column back in the main tape.
- **Q-2** "Now; report F-D-5 (Recommended)" — STEP 6 as written; TIER-C10's F-D-5 RED, reported.
- **Q-3** "Withhold push (Recommended)" — commit exchange/** locally; report the push WITHHELD.

**R-7's three near-name matches, printed for the operator, NOT mapped** (one probe,
2026-09-23T16:52Z, HTTP 200, 1,125,460 B, sha 742a7158…, 907 symbols, weight 1/2400):
NPCUSDT → **NXPCUSDT** (PERPETUAL·TRADING) · MNTUSDT → **MANTAUSDT** (PERPETUAL·TRADING) ·
ZCATUSDT → **1000CATUSDT** (PERPETUAL·TRADING; also CATIUSDT, POPCATUSDT; CATUSDT is
TRADIFI_PERPETUAL). A string likeness is not an identity: each is the operator's to rule.

## §2 WHAT WAS BUILT — ONE COMMIT PER STEP

STEP 0 (no commit): HEAD 68cde3e · pwd /Users/luis/Naiad · branch v12-v1-census · no cloud path ·
no Oracle-owned path modified · 0 com.naiad.oracle-* loaded · G-1 baseline, the five plist mtimes:
0700 / 1600 / topup-0645 / topup-1545 = 1786862922 (2026-08-16T03:48:42), catchup = 1787367695
(2026-08-22T00:01:35) — filed in the queue's STEP 0 RECORD.

| Commit | Step | What landed |
|---|---|---|
| 00de4e0 | 1 | spec of record: the paste verbatim + Q-1..Q-3 + the STEP 0 record |
| 5d15d04 | 2 (R-4) | `SCHEDULE_SUSPENDED` (tracked); `install_refusal`, rc-honest `arm`/`arm_ok`, drift guard; F-SK-4 |
| 862c9f8 | 3 (R-1) | `row_ages`, age cells, STALE marks, `r1_split` + HELD block, newest/oldest dateline, counted band, lead span; wrapper `stale_state`; F-BR-18; F-BR-15/F-BR-7 amended |
| 21e70b3 | 4 (R-2) | `BOARD_ORDER`, `board_rows` (Board + Docket); wrapper `board_order`/`front_page_rows`; F-BR-19 |
| 76fc19a | 5 (R-3) | `EDITION_NOON`; F-BR-20 |
| 7797827 | 6 (R-7) | `scripts/oracle_roster_backfill.py`; ROSTER 19; 76-pair scope; F-BR-16 amended |
| b372cb7 | 7 (R-6) | `tape/SCHEMA.json` (tracked); `tape_schema` metadata on both writers; F-BR-21 |
| d71b2fc | 8 (R-5) | the docstring; the clause-3 exception in the queue; the APOLLO note |
| 1b1b4b6 | 9 (R-8) | the eleven flipped; the Colophon's R-8 table; the three pins re-pointed |
| 5c5167e | 10 | RF-1..3 BUILT |
| 11bec23 | 11 | the pre-proof review's repairs (§7) |
| publish | 12 | this document, the OR-2 stamp, the LEDGER_ARGUS STATUS block — through publish() |

Every commit that changed `scripts/oracle_daily.py` re-pinned the top-up IN THE SAME COMMIT
(G-3; the pinned sha equals `git show <c>:scripts/oracle_daily.py` at each): 862c9f8 e87d51bd… ·
21e70b3 4590a82d… · 76fc19a 2c745f47… · 7797827 1f74876d… (76 pairs, pairs_sha256 507cc14e…) ·
b372cb7 241a74a5… · 1b1b4b6 fc4e5d65… · 11bec23 3a2dcbd1…. F-TU 6/6 after each.

**Deviation, disclosed:** CONVENTIONS §3.4 says exchange/ files go through publish(). The
contract's law is one commit per step, "or2: step N — …"; steps 1, 8, 10 and 11 committed their
exchange/ files by hand under that law (explicit paths, guard-clean index). STEP 12 uses publish().

## §3 WHAT PROVABLY DID NOT CHANGE

**STEP 11(a), the semantic diff** (`or2_transcripts/semantic_diff_or2.py`; transcript
`STEP11a_semantic_diff.txt` sha a892263ddb58c7fe). ONE frozen view (built by the new code with the roster
held at the old 18, a kline loader frozen at the pinned as-of, one frozen clock) rendered by three
modules — OR1 = 26a27c7 (sha 6f456576…), REC = ff74a90 (6c03af96…), NEW = the tree — in three
scenes (FRESH-EVE as-of 2026-09-22T20:00Z printed 21:30 BA; FRESH-MOR as-of 08:00Z printed 09:00 BA;
STALE = FRESH-EVE with LTCUSDT cut back 3 days), plus PUMP (NEW@19 vs NEW@18):

| Class | vs 26a27c7 | vs ff74a90 |
|---|---|---|
| heat values + posture words + every other Board cell | MATCH ×3 | MATCH ×3 |
| card fields | MATCH ×3 | MATCH ×3 |
| non-stale R1 prices | MATCH ×3 | MATCH ×3 |
| row order (Board + Docket) | DECLARED | DECLARED |
| stale marks and age cells | DECLARED (STALE only on LTC in STALE) | DECLARED |
| the HELD block | MATCH / DECLARED (STALE: LTC's 4 lines, byte-identical) | same |
| band text | MATCH / DECLARED (STALE: '' → "LATE EDITION — 1 of 18 …") | same |
| dateline (+ the footer's and the lead's as-of words) | DECLARED | DECLARED |
| edition word | RECOVERY (A-OR1-1 vii, ff74a90's) / MATCH | MATCH |
| register rows (Colophon appendix) | DECLARED | DECLARED |
| the PUMPUSDT row | MATCH (not in scope) | MATCH |
| everything else (text) | RECOVERY (exactly ff74a90's own change) | MATCH |
| PUMP scene: the PUMPUSDT row · everything else | DECLARED: Board row + Trap Card; 26 changed spans, each carrying PUMPUSDT or a count it moves | — |

Page text outside the listed blocks is undone by a rule stated in the script before the exact
comparison, each edit named: the Board footnote's AS-OF · AGE sentence (stale marks) · the Board
footnote's and the creed's order sentences (row order) · the EDGE WATCH "[VETO]"→"(R-8)" and the
Tide Tables note (register rows) · the footer's and the lead's as-of words (dateline). The CSS
(`pre.held`, `td.asof`, `.ruled td.num`) is outside the text compare. BREAK leg: one heat digit,
one posture word, one card field, one non-stale R1 price planted into NEW's page — each DIFFERS.
**Result: CLEAN.**

**Pins that did not move:** `engine/rangefinder.py` sha256 bbae464f… and `scripts/rangefinder_twin.py`
168d6229… (TIER-C10's) unchanged; `posture_engine.py` 1e3b3ba2… (F-BR-14 (a)); the five F-BR-14
constants TIER-C10 reads by AST unchanged; below its docstring `scripts/rangefinder_core.py` is
byte-identical to the engine copy (F-RF-1e); F-RF-1 (the twin's determinism) 8/8; the 2026-09-21
tape eb6991a3… (21,579 B) not rewritten; the five plists' mtimes equal the STEP 0 baseline.

## §4 FIXTURE TRANSCRIPTS — TWO LEGS

Transcripts are OFF-BUS in `research_outputs/oracle/or2_transcripts/` (gitignored; path + sha only).

### 4.1 Final tallies (STEP 11(b), after the edition)
Run by `or2_transcripts/run_11b.sh` AFTER the edition, so default mode audits the real 19-row
edition (before it, F-BR-8/14/15/16/19 are RED by design against OR-1's 18-row artifact set).

| Suite | Tally | Transcript · sha256[:16] | Time |
|---|---|---|---|
| F-BR-1..21, default mode (the real edition) | **21/21** | STEP11b_F_BR_default.txt · c43a3950ba63994f | 93 s |
| F-BR-1..21, sandbox (a fresh render, live lane fingerprinted) | **21/21** | STEP11b_F_BR_sandbox.txt · 590a5dd674e18b35 | 99 s |
| F-SK-1..4 (F-SK-1, 2a..2i, 3, 4) | **12/12** | STEP11b_F_SK.txt · fce2aeb28adacee7 | 10 s |
| F-MV-1..9 (F-MV-1's one real fetch included) | **9/9** | STEP11b_F_MV.txt · 59fe15e8abf12a36 | 141 s |
| F-TU-1..6 | **6/6** | STEP11b_F_TU.txt · 10917fbe51341b1a | 14 s |
| F-RF core (F-RF-1c/d/e, 19 symbols) | **3/3** | STEP11b_F_RF_core.txt · 4ad8a39c4caa8904 | 2 s |
| F-RF v1 (F-RF-1 determinism … F-RF-8) | **8/8** | STEP11b_F_RF_v1.txt · bc80ece7c531d0df | 0 s |
| F-RF v2 (in-process, RF.OUT redirected: FIXTURES_v2.txt untouched) | **8/8** | STEP11b_F_RF_v2.txt · 488da7c77184b3fa | 0 s |
| pytest | **261 passed** | STEP11b_pytest.txt · d1a24190f27c7a6a | 9 s |
| STEP 11(a) semantic diff | **CLEAN** | STEP11a_semantic_diff.txt · a892263ddb58c7fe | — |

Per-step runs (every step re-ran F-TU after its re-pin and F-BR in the sandbox, plus the suites its
change touched) are `STEP<n>_*.txt` in the same directory. The TIER-C10 F-D-5 run of record
(read-only, a leg selector so no transcript was written): STEP6_TC10_F-D-5.txt · e2839aa8b3d4d29e.

### 4.2 The new and amended fixtures — every break plant RED for its own reason
- **F-SK-4 (R-4)** — the real main() in a CHILD whose PATH holds only two recording shims and whose
  HOME is a sandbox (refuses to start otherwise); the real plists stamped before/after. REAL: six
  argvs (`--install`, `--install --job oracle --slot full`, `--install --dry-run`, `--slot full
  --install`, `--rearm`, `--install --rearm --dry-run`) each exit 2, 0 launchctl calls, 0 plists
  written, naming `--install --rearm`; the explicit path with a bootstrap answering 5 → exit 1,
  4 ARMED + 1 NOT ARMED; clean → exit 0, 5 ARMED; enable → bootout → bootstrap → list per label; no
  sentinel → `--install` arms against the shim (the guard is keyed on the file). BREAK: the guard
  removed → the shim records bootout/bootstrap ×5 (the contract's) · ARMED rc-blind → ARMED printed
  for a label whose bootstrap answered 5.
- **F-BR-18 (R-1)** — OR1-a replayed: one symbol cut back 3 days below the others' common bar
  (the others held there too, so a ragged cache cannot leak in), printed at +1 lens period.
  Scenes REPLAY (1 of R), HOTTEST (the victim made the hottest row), CARDLESS (a card-less row set
  back too: 2 of R), FRESH (0 of R) + A2-7's arithmetic (at the limit fresh, 1 ms past stale, the
  limit follows STALE_LENS_PERIODS). 12 plants: the hottest-asset-only as-of restored (the
  contract's) · the lines left in the paste block · only carded rows held · OR-1's band wording ·
  the dateline's newest from the hottest · fresh rows' age cells · every card STALE · the card chip
  without its age · only one HELD line struck · the report-back quiet · the boundary as >= · the limit
  retyped.
- **F-BR-19 (R-2)** — the edition's Board parsed by its own header; the Docket by the Board's word;
  a HARD render (heat inverted against posture, all four postures present) with every heat value
  held to the view; the helper AND the wrapper's real printer; The Watch, the Spaghetti legend and
  the Telegrams still in heat order; the constant typed from the queue. 6 plants: the printer
  re-sorting on heat · the Telegrams in Board order · the heat-only sort (the contract's) · the
  helper on heat · a Docket-on-view-order source mutant · BOARD_PRECEDENCE's order.
- **F-BR-20 (R-3)** — process zone forced to UTC; 09:00 and 22:22 BA (01:22Z next day) on full,
  on-demand-full and on-demand-refresh, each from edition_name AND a real render's ear and print
  line; EDITION_NOON == 12 and read, no number typed. 3 plants: hardcoded Morning (the contract's)
  · EDITION_NOON = 23 · the noon typed in a source copy.
- **F-BR-16 amended (R-7)** — ROSTER == KEPT ∪ ruled mappings in operator order; the record's MAP
  pairs must equal the pairs the TRACKED source rules. 17 plants: the ten OR-1 plants + the mapping
  applied without its record (the contract's) · the near-name NXPCUSDT typed in · the record
  SETTLING · a KEPT name mapped · PUMPUSDT out of place · a near-name in roster + record + source ·
  the record ABSENT.
- **F-BR-21 (R-6)** — the registry held to TAPE_COLS / RANGE_TAPE_COLS and F-BR-14's witnesses;
  every live tape + the edition under test matches exactly the version its date assigns; the v2
  sha; metadata; both writers. 11 plants: an unregistered column (the contract's) · v2 under a 09-23
  name · v2 bytes changed · a sibling column · a v1 file stamped '2' · two columns swapped · heat
  dropped from the registry · an off-pattern name · the writer stamping '2' · the registry ABSENT ·
  the v2 file gone.
- **Amended in place:** F-BR-15 (band driven by print time; the three R-8 rows via `_r8_faults`),
  F-BR-14 (the two R-8 range rows), F-BR-7 (reads the HELD block; both empty is RED), F-SK-2e (its
  B1 plant lifts the new guard too), F-SK-2g (all six R-8 wrapper rows).

### 4.3 The re-pin chain
Each re-pin: `load_scope()` HALTs on the edited file → `oracle_topup.py --enumerate` → `load_scope()`
OK, pin == live, pairs_sha256 recomputed → F-TU 6/6 (STEP*_repin.txt, STEP*_F_TU.txt).

## §5 THE EDITION (STEP 11(c))
Run exactly as the skill runs it: `~/venvs/naiad/bin/python -u scripts/oracle_wrapper.py --job
ondemand --slot on-demand-full >> logs/launchd/oracle-ondemand.log 2>&1`, detached, started
2026-09-23T17:46:26Z (14:46 BA). The recovery edition it overwrote (`oracle_2026-09-23.html`
452,747 B sha 622b6420…, its two tapes, calibration and movers json) was COPIED first to
`research_outputs/oracle/or2_transcripts/preserved_recovery_edition_2026-09-23/` (SHA256SUMS.txt).

| Field | Value |
|---|---|
| exit code | **0** (rc_topup 0, rc_oracle 0) · flag: none standing, nothing to clear |
| path | `briefs/oracle/oracle_2026-09-23.html` (opened) |
| bytes · sha256 | 472,646 B · 95e4b107ace62c1b1105a2c0539e026a0996cc857f668fe68d4eb5228113ce20 |
| masthead | Vol. I · No. 36 · Buenos Aires · 2026-09-23 · **Evening Edition** — printed 14:50 BA (≥ 12:00 BA → Evening, R-3) |
| as-of newest · oldest | 2026-09-23T12:00Z · 2026-09-23T12:00Z (every row on one bar after the top-up) |
| stale count | **0 of 19** rows on a stale wire · band none · no HELD block · report-back "STALE 0 of 19 Board rows on a stale wire" |
| Front Page top 5, posture order | 1 LTCUSDT TRIGGERED 5.586 · 2 XMRUSDT TRIGGERED 3.913 · 3 ZECUSDT TRIGGERED 3.591 · 4 ETHUSDT TRIGGERED 2.669 · 5 SOLUSDT TRIGGERED 1.820 — the Board runs TRIGGERED ×5 → ARMED ×6 → STALKING ×8, heat within (XPL, the hottest at 5.760, is STALKING and prints 12th) |
| headline | "No fresh trigger on the roster: LTC, XMR, ZEC, ETH and SOL triggered but stale; BTC, 1000PEPE, DOGE, PUMP, ENA and HYPE armed and waiting" (the triggers are older than TRIGGER_FRESH_BARS — a posture fact, not a wire fact) |
| Edge Watch | **1 of 19** — LIT, 0.34 ATR from the top (93.8%) |
| roster | **19** (PUMPUSDT on the Board, ARMED, heat 1.889) |
| top-up | PASS: +4,482 rows across 76 pairs, 0 gaps |
| movers | OK, universe 528, 27.5 s |
| self-checks | refresh_idempotence PASS · thumbnail_provenance PASS · tape_append_integrity PASS (row slot=on-demand-full) |
| tapes | D-4 `oracle_tape_2026-09-23.parquet` 16,731 B sha 2217ebc2… (v1, metadata naiad_tape_schema=1) · sibling `oracle_tape_ranges_2026-09-23.parquet` 8,054 B sha 17c79d81… (ranges-1) · D-7 calibration 22,427 B sha df17ad7a… |

The Colophon carries the R-8 table (5 rows) under its own heading, beneath the open [VETO] table
(9 rows, all DEFERRED-TO-BR2). The edition number stays 36: EDITION_COUNT counts DATES, and
2026-09-23 already had the recovery edition.

## §6 QUEUE HYGIENE (STEP 10, OR1-g)
| Queue | BUILT stamp (own line) | Commit read from git log |
|---|---|---|
| RF-1 | exchange/reports/BUILD_2026-08-22_RANGEFINDER_V0.md · 974e9be | 974e9be 05:22:59; published 7e7bec0 |
| RF-2 | …/BUILD_2026-08-22_RANGEFINDER_V1.md · 6c21a05 | 6c21a05 07:26:38; published 366701e |
| RF-3 | …/BUILD_2026-08-22_RANGEFINDER_V2.md · 374b9ef | 374b9ef 11:36:01; published 1d10bd9; follow-ups 70ca5c1, fab5e67, 6837ce0 |

MANIFEST `queue_ratified_unbuilt`: filed 7 (MANIFEST.json of 2026-09-23T10:11:52Z at fea73bd) ·
live, same parser: 8 before → 5 after STEP 10 → 4 after OR-2's own stamp.
On RF-2 and RF-3 the old "BUILT: PENDING" sat mid-line, where the parser does not count it; the
stamps are on their own lines.

## §7 FINDINGS, REPORTED NOT FIXED
Two adversarial reviews ran before anything was claimed: STEP 3's diff (3 lenses, before its
commit) and steps 2-10 (5 lenses, before the proof). Neither found a BLOCKER. Everything they
found inside the Oracle lane was repaired (in 862c9f8 and 11bec23; the list is in
`or2_transcripts/FINDINGS.md`, sha 7a8f5717f3021a5d). What follows is REPORTED, NOT FIXED.

- **F-6 (MAJOR, TIER-C10's) — F-D-5's fallout is larger than "TC10 re-files".** The roster change
  (Q-2) turns F-D-5's real leg RED, as ruled. But (i) its break leg is now vacuous: every plant
  reads red on the same roster mismatch; (ii) a re-derived audit files PUMPUSDT as display-only
  (it is on the Oracle's roster now), so the plant "PUMPFUN re-classified display-only … DROPPED
  from the roster by ruling" can no longer be caught — TIER-C10 must edit its FIXTURE, not only
  re-file; (iii) the never-touched set shrinks from [PUMPFUN, MNT, SUI] to [MNT, SUI], the set
  P-GEN-1's LOAO clause was scored on; (iv) the TIER-C10 close append close_acts.sh will put on
  LEDGER_APOLLO (`research_outputs/tierc10/LEDGER_APOLLO_APPEND.md`) says "never-touched =
  PUMPFUN, MNT, SUI" in the present tense. APOLLO / TIER-C10 to act; OR-2 touched no TC10 file.
- **F-1 — staleness is judged on the 4h bar only** (R-1: "its bar"). R1 prices also read the 1h
  tape (daily ATR, levels): a 1h-only gap moves a row's LIS/INVAL/TARGET with no mark (reviewer:
  ETH's 1h cut 3 days moved LIS_ABOVE 2776.64 → 2806.76, row fresh, lines pasteable). Operator.
- **F-2 — the headline can say "Business possible: X triggered"** for a row whose wire is stale
  (its lines HELD, band up): front_page judges trigger freshness in bars at the row's own bar,
  not wire staleness. Outside R-1's text and STEP 11(a)'s classes. Operator (with the headline's
  voice, already under review).
- **F-3 / F-7 — the view's (hottest row's) as-of still feeds** an UNTIMED proof's ear and
  Colophon note, and the D-7 record's `as_of_ms`. Proofs only for the first; every edition is
  timed. The D-7 field silently carries the hottest row's bar.
- **F-4 — negative ages are not clamped** (a print time before a row's bar prints "-1 bars").
  Unreachable in run(); reachable in F-BR-15's 'fresh' proof on a cache ragged by more than ~8h.
- **F-5 — page text outside G-5's listed classes** (the Board footnote and creed sentences, the
  footer's and lead's as-of words, the Tide Tables' R-8 notes, CSS) — classed and undone by
  named rules in STEP 11(a) (§3).
- **F-8 — the wire-down lock arithmetic at 76 pairs** is ~29.9 min against LOCK_STALE_MIN = 30:
  the next roster addition crosses the age-only reclaim (the on-demand job is protected by
  live_lock_holder; the clock jobs are suspended).
- **F-9 — the Colophon names the six ruled wrapper constants by count**, not by name
  (render_html may not import the wrapper, F-BR-14); `--dry-run` lists them. The step-9 commit
  message says the Colophon names them — it does not.
- **F-10 — step 8's default-mode F-BR-14 transcript is RED** (the 18-row 09-23 artifact set, by
  design until a 19-row edition printed); the step-8 gate was proved in the sandbox (21/21), and
  11(b) proves it on the real edition.
- **F-11 — run()'s now_ba is the MACHINE's zone**: on a machine not set to Buenos Aires the ear's
  date and file name follow the machine while the word and the Colophon follow BA (pre-OR-2).
- **F-12 — a noon boundary off by one** (hour <= EDITION_NOON) passes F-BR-20 alone; F-BR-15
  (ii)'s 12:00 row catches it, so the suite guards it.
- **F-13 — the "withheld" push is fragile**: `com.naiad.daily` (loaded) calls publish() with a
  real push at 07:00; the 2026-09-23 run's push failed only because SSH did. Tomorrow's may push
  TIER-C10's and OR-2's commits before close_acts.sh runs.
- **F-14 — publish() stages all of exchange/**: STEP 12's publish also carries the daily
  routine's §10 residue in `exchange/status/daily/DAILY_2026-09-23.md` (designed to ride the next
  publish, daily_routine.py). A FOREIGN path under the paste's G-2; disclosed, not avoidable
  through publish().
- **F-15 — the probe of record is untracked** (`roster_probe_2026-09-21.json`, OR-1's CC-4): F-BR-16
  needs it; a fresh clone is RED on it. OR-2's own mapping record IS tracked (11bec23).

## §8 WHAT IS OPEN, AND WHO OWNS IT
- **The PARITY line** (BR-2's G-BR2-3) — still owed; today's edition exists, so the gate can close
  today. Operator.
- **The headline's voice** — FRONT_PAGE_HEADLINE was ruled "voice under operator review". Operator.
- **V-7** (APOLLO F-C3-e). APOLLO.
- **The push** — WITHHELD (Q-3); `research_outputs/tierc10/close/close_acts.sh` step 1 pushes
  TIER-C10's and OR-2's commits together. Operator. NOTE: `com.naiad.daily` (loaded) runs
  publish() with a REAL push at 07:00 daily; if SSH works tomorrow morning it pushes the branch
  before close_acts.sh does.
- **TIER-C10's F-D-5, F-DET and the close append** (F-6). APOLLO / TIER-C10.
- **engine/rangefinder.py** — keep, retire or promote (the APOLLO note). APOLLO.
- **R-7's three near-names** (NXPC, MANTA, 1000CAT) — map or leave dropped. Operator.
- Carried from OR-1: restore `research_outputs/rangefinder/FIXTURES_v2.txt` to
  `RF v2 FIXTURES: 6/8 GREEN\n` (OR-2 did not run the v2 CLI and did not touch it).

## §9 WHAT THIS BUILD IS NOT
Not a study: nothing is scored, registered or promoted. No gate, filter or sizing reads a range, a
mover, a staleness mark or the Board's order (F-BR-14, F-MV-9). The schedule stays SUSPENDED; the
explicit re-arm path was never run against the real gui domain. engine/ was not written.

## §10 DISPOSITION + BOX COST
BOX constants read LIVE from `publish_exchange`: BOX_BYTES 16,000,000 · warn at 40% (6.40 MB) ·
refuse ABOVE 70% (11.20 MB) · FLAG_BYTES 64,000 (naming wire). This document is ≈30 KB — under
the naming wire.

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| exchange/queue/2026-09-22_OR2_oracle_rulings_ARGUS.md | yes | yes | 00de4e0, d71b2fc, + the STEP 12 stamp (publish) | **no — WITHHELD (Q-3)** | git, local only | 14,220 B |
| exchange/reports/BUILD_2026-09-22_ORACLE_RULINGS.md (this) | yes | yes | publish (STEP 12) | **no — WITHHELD** | git, local only | ≈30 KB |
| exchange/reports/NOTE_ARGUS_to_APOLLO_2026-09-22_rangefinder_engine_tape.md | yes | yes | d71b2fc, 11bec23 | **no — WITHHELD** | git, local only | 1,766 B |
| exchange/queue/2026-08-22_RF{1,2,3}_*.md (stamps) | yes | yes | 5c5167e | **no — WITHHELD** | git, local only | +~1.2 KB |
| exchange/status/LEDGER_ARGUS.md (the STATUS block) | yes | yes | publish (STEP 12) | **no — WITHHELD** | git, local only | +1,864 B |
| scripts/oracle_{daily,wrapper,fixtures,ondemand_fixtures,topup,roster_backfill}.py, scripts/rangefinder_core.py, .claude/skills/oracle/SKILL.md, .gitignore | yes | yes | the or2 step commits | **no — WITHHELD** | git, local only | 0 (non-box) |
| research_outputs/oracle/{SCHEDULE_SUSPENDED, tape/SCHEMA.json, roster_mapping_2026-09-22.json, topup_scope.json} | yes | yes | 5d15d04 / b372cb7 / 11bec23 / each re-pin | **no — WITHHELD** | git, local only | 0 (non-box) |
| briefs/oracle/oracle_2026-09-23.html (the edition, 472,646 B) | yes | no (gitignored) | — | — | **NOT PROTECTED** (off-bus, regenerable from the cache) | 0 |
| research_outputs/oracle/{tape, tape_ranges, calibration, movers, backfill_state.json} | yes | no | — | — | **NOT PROTECTED** | 0 |
| research_outputs/oracle/or2_transcripts/** (transcripts, semantic_diff_or2.py, run_11b.sh, the preserved recovery edition) | yes | no | — | — | **NOT PROTECTED** | 0 |
| ~/.cache/naiad/data_cache/klines/PUMPUSDT_{4h,1h,15m,5m}.parquet | yes | outside the repo | — | — | NOT PROTECTED (refetchable) | 0 |

**BOX COST.** Before STEP 12 (at 11bec23, the probe `budget_lines`): `publish: box OK -- TICK SET
2,833,496 B (2.83 MB) = 17.71% of 16,000,000 B (16.00 MB) [governs]`. After: the publish line is
recorded in the executor's report and the ledger's LAST EVENT; projected ≈ 2,833,496 + this document
+ the ledger block + the stamp ≈ 2,865,740 B (≈17.91%) — below warn.

**PUBLISH.** `publish(R, '2026-09-23', remote='__push_withheld__')` — CONVENTIONS §3.4's own
function, the push pointed at a remote that does not exist, OR-1's method (fea73bd): it stages
exchange/**, guard-checks the index, commits, and the push fails by design. **PUSH WITHHELD by
operator ruling Q-3.** Its commit is the one that carries this file (`git log -1 --
exchange/reports/BUILD_2026-09-22_ORACLE_RULINGS.md`). publish() also carries the daily routine's
§10 residue in exchange/status/daily/DAILY_2026-09-23.md (F-14).

## §11 GATES
| Gate | Verdict | Evidence |
|---|---|---|
| G-1 | PASS | 0 com.naiad.oracle-* loaded; SCHEDULE_SUSPENDED present and tracked; the five plist mtimes equal the STEP 0 baseline (1786862922 ×4, 1787367695); F-SK-4's stamp check |
| G-2 | PASS, with a disclosure | one commit per step 1..10 ("or2: step N — …") + 11bec23 (step 11's repairs) + publish; no FOREIGN path in any or2 commit (review lens 5 listed every path); publish() carries the daily residue (F-14) |
| G-3 | PASS | topup_scope.json pins oracle_daily.py 3a2dcbd1… == the live file; 76 pairs; pairs_sha256 507cc14e…; every oracle_daily.py commit re-pinned in the same commit |
| G-4 | PASS | F-BR 21/21 (default + sandbox) · F-SK 12/12 · F-MV 9/9 · F-TU 6/6 · F-RF 3/3 + 8/8 + 8/8 · pytest 261; every break leg RED for its own reason (§4) |
| G-5 | PASS | STEP 11(a) CLEAN against 26a27c7 and ff74a90 (§3) |
| G-6 | PASS | briefs/oracle/oracle_2026-09-23.html: Evening Edition printed 14:50 BA; Board TRIGGERED → ARMED → STALKING, heat within; report-back posture-first |
| G-7 | at publish | LEDGER_ARGUS.md ends "=== END STATUS ===" (checked in the tree and in the publish commit) |
| G-8 | at publish | the publish commit and its result (PUSH WITHHELD) — the executor's report |
| G-9 | PASS | box 17.71% before; ≈17.91% after — below warn (40%) |
