# INCIDENT — THE ORACLE DAILY, 2026-08-20 → 2026-08-22

**Lane** ARGUS · **Branch** `v12-v1-census` · **HEAD at diagnosis** `4b9c68c` · **Host** local Mac, `~/Naiad`
**Opened** 2026-08-22 (BA) under the ARGUS diagnostic contract · **State** REPAIRED, PROVEN, awaiting two [VETO] words

---

## §0 · WHAT THIS IS, TO SOMEONE WHO KNOWS NOTHING

The Oracle is the daily organ. Two launchd agents render it: `com.naiad.oracle-0700` at 07:00
America/Argentina/Buenos_Aires (the full brief) and `com.naiad.oracle-1600` at 16:00 (the refresh).
Two more, `com.naiad.oracle-topup-0645` and `-1545`, fetch bars 15 minutes ahead of each so the
cache is fresh before it is read. Each Oracle run renders `briefs/oracle/oracle_<date>.html`,
appends a row to `research_outputs/oracle/tape/oracle_tape_<date>.parquet`, writes
`research_outputs/oracle/calibration/oracle_calibration_<date>_<slot>.json`, runs three
self-checks, and appends one verdict row to
`research_outputs/oracle/calibration/selfcheck_log.jsonl`.

**From 2026-08-20T10:00:03Z the Oracle crashed on every run and kept doing so for two days.**
It crashed *after* writing the brief and the tape and *before* writing the calibration record, so
a brief kept appearing on disk every day and nothing on screen said anything was wrong. The
calibration lane stopped dead on 2026-08-19 and the three self-checks — which are gated behind a
clean run — went dark with it.

Nothing reported it. It was found on 2026-08-21 by the PINE lane, by accident, while verifying an
unrelated debt: `exchange/reports/BUILD_2026-08-16_PINE_ESTATE_V12_6.md` §5A, headed
**"THE ORACLE DAILY HAS BEEN FAILING FOR TWO DAYS AND NOTHING HAS REPORTED IT."** That accident is
the most important fact in this document and §8 is about it.

---

## §1 · TIMELINE

Every row of `selfcheck_log.jsonl`, with the machine's own local (BA) time alongside UTC.

| # | ts (UTC) | BA | slot | verdict | s | what it means |
|---|---|---|---|---|---|---|
| 1–3 | 2026-08-16 05:12 / 05:49 / 07:40 | 02:12 / 02:49 / 04:40 | full | PASS | 5.6–5.7 | build-day runs |
| 4 | 2026-08-16 19:00 | 16:00 | refresh | PASS | 5.8 | |
| 5 | 2026-08-17 10:00 | 07:00 | full | PASS | 5.8 | |
| 6 | 2026-08-17 19:00 | 16:00 | refresh | PASS | 5.9 | |
| — | *2026-08-18 06:45 + 07:00* | | | *no run* | | host powered off 05:05→15:30 |
| 7 | 2026-08-18 19:00 | 16:00 | refresh | PASS | 6.2 | |
| 8 | 2026-08-19 10:00 | 07:00 | full | **PASS** | 5.8 | **the last healthy run** |
| — | *2026-08-19 15:45 + 16:00* | | | *no run* | | host powered off 14:21→18:40 |
| 9 | 2026-08-20 10:00:03 | 07:00 | full | **FAIL** | 3.0 | **the break** |
| 10 | 2026-08-20 19:03:20 | 16:03 | refresh | FAIL | 3.3 | late — launchd's on-wake replay |
| 11 | 2026-08-21 10:00:03 | 07:00 | full | FAIL | 3.0 | |
| 12 | 2026-08-21 19:08:23 | 16:08 | refresh | FAIL | 3.1 | late — on-wake replay |
| 13 | 2026-08-22 02:49:39 | 08-21 23:49 | full | FAIL | 2.9 | diagnostic reproduction |
| 14–16 | 2026-08-22 03:00 / 03:02 / 03:04 | 00:00 / 00:02 / 00:04 | full/refresh | **PASS** | 5.7–5.8 | after the repair |
| 17 | 2026-08-22 04:20 | 01:20 | full | **PASS** | 5.7 | contract proof-of-life |

**Four PASS days (08-16, 17, 18, 19). Four scheduled FAIL slots (08-20 ×2, 08-21 ×2), plus one
diagnostic reproduction. The 3.0 s runtime against a healthy 5.8 s is the crash signature: the run
died before the self-checks, which is the whole ~2.8 s difference.**

The two gaps on 08-18 morning and 08-19 evening are **not** part of this incident. The host was
powered off across both (`last reboot`: shutdown 08-18 05:05 → boot 15:30; shutdown 08-19 14:21 →
boot 18:40). Measured behaviour, worth recording on its own: **launchd replays a missed
`StartCalendarInterval` job on WAKE — 08-20 16:00 ran at 16:03 and 08-21 16:00 at 16:08, each on
the DarkWake logged the same second — but never on BOOT.** The 08-18 15:30 boot fired neither the
06:45 top-up nor the 07:00 Oracle.

---

## §2 · THE CORPSE

`com.naiad.oracle-0700` merges stdout and stderr into
`/Users/luis/Naiad/logs/launchd/oracle-0700.log` (`StandardOutPath` and `StandardErrorPath` are the
same path in the plist; `-1600` likewise). The failure was never silent to disk — only to the
operator. All four scheduled FAIL slots carry a byte-identical traceback:

```
=== ORACLE WRAPPER · job=oracle slot=full · 2026-08-20T10:00:00.198927+00:00 ===
  RUN FAILED:
Traceback (most recent call last):
  File "/Users/luis/Naiad/scripts/oracle_wrapper.py", line 322, in main
    result = OD.run(slot=slot, log=log)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/luis/Naiad/scripts/oracle_daily.py", line 1095, in run
    cal_p, cal_sha, cal_b = write_calibration(view, date_str, slot)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/luis/Naiad/scripts/oracle_daily.py", line 1029, in write_calibration
    "lis_fallback_used": {k: bool(lis.get(k, {}).get("fallback", False))
                                  ^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'get'
```

The same run, immediately above that traceback, printed a full ten-symbol lens summary and then
successfully wrote `posture_canon.json` (9,548 B), `oracle_2026-08-20.html` (229,068 B) and
`oracle_tape_2026-08-20.parquet` (15,412 B). **The read path and the write path were both healthy.
This matters for §4.**

### Reproduction

The working tree is now repaired, so re-running cannot crash. Two things were done instead.

1. **The literal committed text was executed.** `git show HEAD:scripts/oracle_daily.py`, lines
   1029–1030 taken verbatim and evaluated against the `lis` shape that
   `analytics/levels.py:219` produces:

   ```
   input:  {'above': None, 'below': {'mean': 100.0, 'score': 6, 'source': 'primary'}}
   result: AttributeError: 'NoneType' object has no attribute 'get'
   ```

2. **The same text was run against a live view built today — and did NOT raise, on any of the ten
   assets.** The market moved; every asset now has a qualifying cluster on both sides. **The defect
   has already gone latent again.** On 2026-08-21 it was live on three of ten (BTCUSDT, ETHUSDT,
   ZECUSDT all had `lis["above"] = None`). This is why the new fixture forces the condition rather
   than waiting for the market to supply it (§5, F-BR-11).

---

## §3 · THE CONVICTION

**CONVICTED: a latent data-triggered defect in Oracle-owned code, `scripts/oracle_daily.py:1029`,
in `write_calibration`. One expression, two defects.**

```python
"lis_fallback_used": {k: bool(lis.get(k, {}).get("fallback", False))
                      for k in ("above", "below")},
```

**Defect 1 — the crash.** `analytics/levels.py:219` sets `out[side] = None` when neither the
primary rule nor the fallback finds a qualifying cluster on that side. The key is therefore
**present, holding `None`**, and `lis.get(k, {})` never reaches its `{}` default. `.get("fallback")`
is then called on `None`. The line immediately above it, `lis_distance_atr`, already guards this
correctly with `if lis.get(k) and ...` — the two lines were written together and only one of them
was defended.

**Defect 2 — the dead field.** `lines_in_sand` marks a fallback line with `source="fallback"`. It
never writes a key called `"fallback"`. So `lis_fallback_used` recorded `False` for every asset on
every side from the day it shipped and was structurally incapable of recording anything else.
Verified against the last surviving pre-break record,
`oracle_calibration_2026-08-19_full.json`: twenty sides, all `False`.

**Why 08-20 and not 08-16.** The defect entered at `a36edc1`, 2026-08-16 02:14:04 -0300, and
survived four consecutive PASS runs on identical bytes. Its counterpart, `levels.py:219`, dates to
2026-08-02. Nothing changed on 08-20 except the market: new price data left three assets with no
qualifying cluster above, `lines_in_sand` returned `None` for that side, and the expression met the
input it could not survive.

---

## §4 · RULED OUT, EXPLICITLY

Each alternative was investigated independently and each finding was then put through an
adversarial pass whose instruction was to refute it.

| suspect | verdict | evidence |
|---|---|---|
| **code / config change** | **RULED OUT** | No code and no config entered the repo between the last PASS (08-19T10:00:06Z) and the first FAIL (08-20T10:00:03Z). The only two commits in the window, `5f28d2a` and `97760b9`, are `exchange: auto-publish` touching `exchange/status/*` only — and the Oracle never reads `exchange/`. Every file in `oracle_daily.py`'s complete import closure is git-clean with a newest mtime of 2026-08-16T07:38:05Z. All four plists share mtime 2026-08-16T06:48:42Z. **Same code, same config, same schedule, different data** — positive proof of the data trigger, not merely absence of evidence. |
| **cache / parquet state** | **RULED OUT as fault** | The 08-20 top-up at 09:47:23Z recorded all 40 pairs `status=OK`, `shrank=0`, `lost_newest=0`, `gap_count=0`, `min_rows_after=1438` — thirteen minutes before the crash. The 10:00:00Z run then read every lens, printed all ten symbol summaries, and wrote 253 KB across three files before raising at line 1029. No file was missing, truncated or unreadable. **The cache's structural health and freshness signature were unchanged across the boundary (40/40 OK, oldest newest-bar 04:00Z, 4h lag 5.79 h on both 08-19 and 08-20). Its CONTENTS did change, as they do every day, and that is precisely the trigger** — BTCUSDT went DEAD heat 5.453 clusters 12 → STALKING heat 1.438 clusters 17; TAOUSDT 12 → 11 clusters; fired events 284/14 cells → 175/15. Cache *health* is ruled out; cache *content* is the data trigger, exactly as §3 states. |
| **disk exhaustion** | **RULED OUT** | `/dev/disk3s5`, which holds both the repo and `~/.cache/naiad/data_cache`, is at 6% capacity — 1.7 Ti available, 0% inode use. Zero `ENOSPC`/`OSError`/`ArrowInvalid`/`corrupt`/`truncated` tokens in any of the oracle launchd logs. Two APFS local snapshots from 08-18 and 08-20 survive, and macOS thins those first under pressure. A full volume would also have raised `OSError` on the 229 KB brief write, which succeeded. |
| **top-up failure** | **RULED OUT** | Eleven real top-up runs over the log's life, every one `verdict PASS`, 40/40 pairs, `gaps=0`, `failures=[]`, launchd exit 0 — including the three that immediately preceded Oracle crashes. The only FAIL rows are eight synthetic fixture rows tagged `slot="fixture-F-TU-6"`, written 2026-08-16 by `oracle_topup_fixtures.py`, which monkey-patches `backfill_klines` to raise a simulated `ConnectionError`. Four days before the incident, and not real runs. |
| **R-4 ABSENT-is-failure semantics** | **RULED OUT — and R-4 is CLOSED, not open** | R-4 is a repair record in the 2026-08-16 ARGUS block, tagged `[verified]`, not a pending ruling: *"ABSENT is now a failure; still never created here."* `oracle_topup.py:379` puts ABSENT in the same bucket as ERROR and CLOBBER and :397 flips the run's verdict to FAIL. No pair has ever been ABSENT in a real run. An ABSENT pair would have raised `FileNotFoundError` at `oracle_daily.py:177`, hundreds of lines earlier, with a different traceback. It could not have caused or masked this. |
| **environment / interpreter** | **RULED OUT** | The plists name an absolute interpreter, `/Users/luis/venvs/naiad/bin/python` (3.12.14). Reproduced under `env -i PATH=/usr/bin:/bin:/usr/sbin:/sbin`: interpreter resolves, numpy 2.1.3 / pandas 2.2.3 / pyarrow import clean. `zones_agree = True` on every run. |
| **schedule drift / persistence** | **RULED OUT** | All four plists installed in `~/Library/LaunchAgents` since 2026-08-16 06:48, surviving four reboots; every run logs `schedule OK` on all labels; `reschedule_if_drifted` reports `drift: False`. |

**One live hazard, adjacent but not guilty.** R-4 made the *top-up* loud; it did not connect the
top-up's exit code to the Oracle. `run_topup`'s own docstring says so: *"the Oracle 15 minutes
later is unaffected and stamps whatever as-of it finds."* If a parquet ever did go missing the
operator would get two separate alarms, not a prevented outage. Recorded, not fixed.

---

## §5 · THE REPAIR

Two waves. The second exists because the first was audited adversarially and did not survive
intact.

### Wave 1 — the fault

**`scripts/oracle_daily.py`** — the convicted line, both defects:

```python
"lis_fallback_used": {k: (None if not lis.get(k)
                          else lis[k].get("source") == "fallback")
                      for k in ("above", "below")},
```

`None` now means *no line on that side*, matching the `None` convention `lis_distance_atr` already
used one line above. No named constant moved, so the named-constant protocol is not engaged. There
are no downstream readers of the field (grepped), so widening `bool` to `None | bool` is safe.
First run after the repair recorded `FARTCOINUSDT.below = True` — **the first `true` that field has
ever held.**

**`scripts/oracle_fixtures.py`** — **F-BR-11 · CALIBRATION TOTALITY**, in the house two-leg
`prove()` form. It forces a `None` side onto `assets[0]` of the real view rather than waiting for
the market, and writes into a throwaway `CAL_DIR` so nothing lands in the real lane. Its break leg
replays the pre-repair behaviour and goes red naming both defects by asset and side. Suite is
**GREEN 11/11 · RED 0**.

**`research_outputs/oracle/topup_scope.json`** — re-enumerated, because `oracle_topup.py` pins
`oracle_daily.py`'s sha256 and HALTS if it moves. This was caught by testing, not by luck: the next
06:45 top-up would have halted. The check that matters is that **`pairs_sha256` came back
byte-identical (`48f1b0de…`)** — the source pin moved, the read scope did not.

**A fifth launchd agent, `com.naiad.oracle-catchup`** — no `StartCalendarInterval`, `RunAtLoad`
true, so it fires once per login/boot. It exists because launchd replays a missed slot on wake but
not on boot (§1), so a host that was shut down over a slot lost it silently, twice in six days.

### Wave 2 — the repair's own defects

An adversarial audit of Wave 1 found six defects, all in the catch-up agent. Two of them were
themselves overstated by the auditor and corrected on a second pass; the corrections are reflected
below. **The parts that were sound: the one-line calibration fix, F-BR-11, and the scope pin.**

- **D1 + D2 (HIGH, both fixed).** The catch-up decided whether a slot was covered from
  **the brief file's mtime**. That is wrong for the exact failure it was built after:
  `oracle_daily.run()` writes the brief **before** it calls `write_calibration`, so each of the
  four crashed runs left a freshly stamped brief on disk. **Replayed against the real incident,
  the Wave-1 catch-up reports `covered=True` straight through the outage and does nothing.** A file
  that a failed run also writes cannot be the evidence that the run succeeded. D1 was a second face
  of the same mistake: the filename was built from the *oracle-zone boundary date* while
  `oracle_daily.run()` names its output from the *machine-local date*, so between 00:00 and 07:00 BA
  the catch-up checked a file its own run would never create — and for 12 h/day on a travelled host.
  **Fixed together** by moving the evidence to `selfcheck_log.jsonl`: a boundary is covered iff a row
  with `verdict == PASS` exists at or after it. No filename is involved, so D1 dissolves; a crashed
  run and a missed slot now both read as *not covered*. A boundary is tried **at most once** — if a
  catch-up already ran for it and still did not reach PASS, the fault is not a missed wake-up and
  retrying on every login would bury the operator's evidence.
- **D4 (fixed).** No mutual exclusion. A login landing mid-slot could run two Oracle jobs at once,
  both appending to the same dated tape parquet; a top-up takes ~130 s wall-clock. Added a
  single-flight `O_EXCL` lock at `logs/launchd/.oracle.lock` (gitignored) with a 30-minute stale
  reclaim. Verified: a held lock makes the second run stand down at exit 0 doing nothing; a
  backdated lock is reclaimed; the lock is released on every path.
- **D5 (fixed).** The clockless agent's `installed` flag was computed and printed but nothing acted
  on it. A vanished catch-up plist now logs `AGENT MISSING` and drives the run's exit code non-zero.
- **D3 (no change — working as designed).** The 20-minute grace correctly yields to launchd's own
  on-wake replay: `due=False` at 07:10 and 16:19, `due=True` at 07:21 and 16:21.
- **D6 (no change — inherent).** One brief file per calendar day means a missed 07:00 becomes
  invisible once the 16:00 run writes the same file. This is the same property the ledger already
  records under G-BR2-1. The move to selfcheck-log evidence narrows it: the *runs* are now
  distinguishable even though the *files* are not.
- **Not closed:** the same-class scan for other `x.get(k, {}).get(...)` hazards found none across
  the sixteen modules in the Oracle import closure, but both the original scan and its independent
  reproduction only detect the *chained* form. A two-statement `v = d.get(k)` then `v["x"]` is
  invisible to it. Reported as **no chained instances found**, not as ruled out.

### Diff, scoped

```
research_outputs/oracle/topup_scope.json |   4 +-
scripts/oracle_daily.py                  |  15 +-
scripts/oracle_fixtures.py               | 101 +++++-
scripts/oracle_wrapper.py                | 275 +++++++++++++++-------  (Wave 1)
                                         +   ~120 more                 (Wave 2)
```

Uncommitted on `v12-v1-census` at the time of filing. **A second lane (`naiad-e7`, APOLLO/TIERC9)
was working in this repo concurrently and holds unrelated uncommitted changes to
`scripts/tierc6*.py`; those are not part of this repair and were not touched.**

---

## §6 · PROOF OF LIFE

Run through launchd itself, top-up first then the Oracle, on 2026-08-22 (BA 01:18 / 01:20):

```
com.naiad.oracle-topup-0645   last exit code = 0   top-up PASS: +223 rows across 40 pair(s), 0 gap(s)
com.naiad.oracle-0700         last exit code = 0
  render      briefs/oracle/oracle_2026-08-22.html
              221,018 B  sha256 86bf0fca78c2ed7f433204af1b08d352048b51366d1da48cd80446fab7b45d85
  calibration oracle_calibration_2026-08-22_full.json  6,042 B
              sha256 9eaeeda5a339a1759935c7414a8f3f1091459972522048711f4d06b6ab2a49f6
  selfcheck   refresh_idempotence PASS · thumbnail_provenance PASS · tape_append_integrity PASS
  as-of bar   2026-08-22T00:00Z
  STALE DATA banner  ABSENT — the cache is fresh
```

Fixtures `F-BR-1 … F-BR-11`: **GREEN 11/11 · RED 0**, exit 0.

The self-checks had not executed since 2026-08-19: they are gated on a clean render
(`oracle_wrapper.py`, `if rc == 0`), which is a deliberate choice — checking the idempotence of a
render that did not happen proves nothing — but its cost is that a render failure takes the checks
dark with it. The A2-7 STALE DATA banner also earned its `[VETO-by-firing]` during this work: it
fired correctly on a 14.8 h-old 4h bar during the diagnosis and stood down once the top-up ran.

---

## §7 · WHAT THE SILENCE COST

- **Two days, four scheduled slots, no calibration record.** `oracle_calibration_*` stops at
  `2026-08-19_full` and resumes at `2026-08-22`. 08-20 and 08-21 are gone and cannot be recovered —
  the view is rebuilt from a cache that has since moved.
- **Six runs with all three self-checks dark**, so refresh idempotence, thumbnail provenance and
  tape append integrity are unattested across the whole window.
- **The brief kept appearing.** Anyone reading `briefs/oracle/` saw a fresh file every day.
- **BR-2's G-BR2-2 evidence took the damage**, and it is the gate that reads this log.
- **It was found by another lane, by accident.** No alarm exists. That is §8.

---

## §8 · PREVENTION — [VETO] PROPOSALS, NOT BUILDS

Neither of these is built. Both await one word.

### [VETO] T-7 · CRASH SURFACING — *the cheapest honest alarm*

The failure ran for two days in a log nobody reads. The catch-up agent now recovers a **missed or
failed slot** automatically, but it is silent when it succeeds and it cannot speak at all if the
fault is persistent — by design, it tries a boundary once and stops. Something must reach the
operator. Three candidates, cheapest first; **the drafter's lean is A+B**:

- **A · A red flag-file the next session cannot miss.** On any non-zero Oracle exit, write
  `ORACLE_UNHEALTHY.md` at the repo root naming the date, slot, exit code and the last traceback
  line; delete it on the next PASS. Zero infrastructure, survives reboots, and is in the path of
  anyone who opens the repo. **~15 lines in `oracle_wrapper.py`.**
- **B · The daily routine prints Oracle health.** `com.naiad.daily` already runs. Have it read the
  last 24 h of `selfcheck_log.jsonl` and print one line —
  `ORACLE: 2/2 slots PASS` or `ORACLE: 2 FAIL since 2026-08-20 — <first line of traceback>`. Puts
  the state where a human already looks. **~20 lines.**
- **C · A gate on the exchange bus.** Add the same one-liner to the published `DAILY_*.md` so the
  web lanes see it too. Larger blast radius; only worth it if A and B prove insufficient.

**Also proposed under T-7, and cheaper than all three:** `self_checks()` currently never asserts
that a **calibration record exists for the run just made**. Had it done so, this incident would
have been a loud FAIL on 08-20 instead of a quiet one — the crash would still have happened, but
the *verdict row* would have named a missing artifact rather than a bare `"run failed"`.
`oracle_fixtures.load_artifacts` also sets `CAL = None` silently when the file is absent.
**~6 lines, and it closes the exact hole this incident fell through.**

### [VETO] T-3 · THE WAKE-ORDER RULING — *still owed a word*

T-3's diagnostic half is now closed with measurement: persistence, environment and reschedule are
ruled out; launchd replays on wake but not on boot; the shutdown half is handled by the catch-up
agent. **The ruling itself is untouched and still open:** should the Oracle **refuse to render** on
a stale cache, rather than render with the A2-7 banner? This incident produced the exact case the
ruling governs — a brief rendered on a 14.8 h-old 4h bar with the banner showing. The banner works.
Whether working is enough is not the drafter's call.

### Recorded, not proposed

`exchange/status/CADENCE.md` — the trigger registry — lists three armed agents
(`com.naiad.daily`, `.estate`, `.workflow`) and **has no row for any of the five Oracle agents**,
including the one added by this repair. The registry does not describe the machine. Operator-owned;
not edited here.

---

## §9 · POINTERS

Per the exchange CONTENT GUARD, artifacts are referenced, never carried.

- `briefs/oracle/oracle_2026-08-22.html`
  - `size: 221,018 B`  `sha256: 86bf0fca78c2ed7f433204af1b08d352048b51366d1da48cd80446fab7b45d85`
- `research_outputs/oracle/tape/oracle_tape_2026-08-22.parquet`
  - `size: 15,243 B`  `sha256: 4dbb3c2168d9a588a413e8841de8a07e72519ea61da0b0f03290612f725b5438`
- `research_outputs/oracle/calibration/oracle_calibration_2026-08-22_full.json`
  - `size: 6,042 B`  `sha256: 9eaeeda5a339a1759935c7414a8f3f1091459972522048711f4d06b6ab2a49f6`
- `research_outputs/oracle/calibration/selfcheck_log.jsonl`
  - `size: 11,815 B`  `sha256: 433d37ced73ef35894ce70253d91b1ff5d091f11bcc0a0b6aae66ba4c9866dca`
- `research_outputs/oracle/topup_scope.json`
  - `size: 2,928 B`  `sha256: dc828aed726dab71de80294392d05caa128312706cbb3f87f00cd85dfbf8f25a`
- `logs/launchd/oracle-0700.log` — the corpse, all four scheduled FAIL slots
  - `size: 24,855 B`  `sha256: 59d9b43de17f4327393bafbf87438ca43853175cca5046d3153fb433886634d6`
- `logs/launchd/oracle-1600.log`
  - `size: 15,178 B`  `sha256: 529e12119a752d58dc1819f7e073231d42fa23ff9da20302b5df8509750205ee`
- `exchange/reports/BUILD_2026-08-16_PINE_ESTATE_V12_6.md` §5A — the accidental discovery

---

## §10 · DISPOSITION

| item | state | owner |
|---|---|---|
| `oracle_daily.py:1029` crash + dead field | **FIXED, proven** | ARGUS |
| F-BR-11 fixture pinning the property | **BUILT, 11/11 green** | ARGUS |
| Catch-up agent (shutdown half of T-3) | **BUILT + repaired after audit, 7/7 scenarios** | ARGUS |
| Single-flight lock (D4) | **BUILT, verified** | ARGUS |
| Two days of calibration records | **LOST, unrecoverable** | — |
| T-7 crash surfacing | **RULED "flagfile" 2026-08-22 — BUILT, F-BR-12 green** | ARGUS |
| T-3 wake-order ruling | **RULED 2026-08-22 — renders on a stale cache, banner showing; CLOSED on all four faces** | ARGUS |
| CADENCE.md has no Oracle rows | **REPORTED, not fixed** | operator |
| Top-up exit code not wired to the Oracle | **REPORTED, not fixed** | operator |
| Non-chained `None` hazards | **NOT CLOSED — scan cannot see them** | ARGUS |

---

## ADDENDUM 2026-08-22 — OPERATOR RULINGS

(verbatim 'W1 fire, W2 flagfile, W3 banner, W4 yes')

T-7 RULED = flag-file alarm, built this session (F-BR-12). C-0/T-3 RULED = the Oracle RENDERS on a
stale cache, banner showing; refusal rejected — a stale brief that confesses beats a missing one.
T-3 is now CLOSED on all four faces: wake replay (measured), boot coverage (catch-up agent), alarm
(T-7 flag), disclosure (A2-7 banner). Repair committed at `88850e0`.

### What the rulings changed on disk

**W1 · the repair is committed.** `88850e0` on `v12-v1-census`, pushed: the four paths the §5 diff
names and no others. The concurrent lane's `scripts/tierc6*.py` were not staged, stashed or checked
out — the reconciliation was printed before anything was added to the index.

**W2 · T-7 is candidate A of §8, not A+B.** One file, `ORACLE_DOWN.flag`, at the repo root, written
by `oracle_wrapper.py` on any run ending `rc != 0` and carrying the UTC stamp, the job and slot, the
exit code, and the last 15 traceback lines. It is **gitignored** — an alarm on the bus would tell
every reader that a laptop in Buenos Aires had a bad morning, and the alarm is for the operator
standing at the machine. Three things the build decided that §8's sketch did not:

- **The all-clear is not `rc == 0`, it is a clean run.** The lock stand-down exits 0 having done no
  work, `--install` exits 0 without running the Oracle, and a catch-up that finds nothing missed
  exits 0 by design. Had any of those cleared the flag, a login could silently cancel a live alarm —
  the same class of error as D1/D2, where a file a FAILED run also writes was read as proof the run
  succeeded. The flag is cleared only by a run that performed a job AND reached `rc == 0`.
- **The alarm has an outermost net.** `main()` carried no top-level `try`: argv parsing,
  `zone_report()` and `acquire_lock()` all sat outside one, so a crash in any of them exited nonzero
  with the alarm silent. That is the failure T-7 exists to end, so the entry point now nets it.
  `KeyboardInterrupt` is deliberately not caught — an operator who stops a manual run has not
  discovered an outage.
- **Failures that raise nothing still speak.** A red self-check and a vanished agent plist both drive
  `rc` nonzero without an exception, so both now write a line the flag can carry.

**W3 · this addendum**, and the two §10 rows above.

**W4 · CADENCE.md** now carries a row for each of the five Oracle agents, cited to this ruling.

### Superseded above, left as written

Two §10 rows predate this session and were outside the ruling's scope, so they were not edited:
**CADENCE.md has no Oracle rows** — five rows were added under W4 on 2026-08-22 and the row is now
discharged; and **F-BR-11 ... 11/11 green**, which reads **12/12** with F-BR-12 in the suite.
