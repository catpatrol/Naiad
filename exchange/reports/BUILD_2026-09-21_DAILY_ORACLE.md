# BUILD — OR-1 · THE DAILY ORACLE · on-demand edition, roster, ranges, market page

**Lane** ARGUS · **Executor** HEPHAESTUS · **Reviewer** ARGUS · **Branch** `v12-v1-census`
**Window** 2026-09-21, one session · **Queue** `exchange/queue/2026-09-21_OR1_daily_oracle_ondemand_ARGUS.md`
**RATIFIED** operator, 2026-09-21 — by firing; rulings verbatim in the queue file's header.
**Class** operations / display-only. BR-1 §2 firewall reprinted in the queue file and binding,
extended by OR-1's own clause: *no gate, filter, or sizing reads a range or a mover.*

---

## 0 · THE ONE THING TO READ FIRST

> **§0 · RECOVERY LINE, 2026-09-22.** Built 2026-09-21 under the original text. **Re-opened
> 2026-09-22 by AMENDMENT A-OR1-1, completed 2026-09-23** — see **§9**. The recovery paste
> presumed the 2026-09-21 session was interrupted; the repo says it was not (it ended on its
> own publish, `088d475`). What A-OR1-1 superseded here — `engine/rangefinder.py` as the
> Oracle's machine, range columns on the D-4 tape, "Morning" for every full edition — is
> repaired in §9. §1–§8 stay as the record of what was built that day.

The Oracle's clock is off. Five launchd agents used to print the paper at 06:45, 07:00, 15:45
and 16:00 Buenos Aires time, plus a catch-up at every login. On 2026-09-21 the operator
suspended them. They are booted out of `gui/501` **and** persistently disabled, and their five
plists sit unedited in `~/Library/LaunchAgents`. Nothing was deleted.

In their place there is now one command the operator fires when he wants the paper: **`/oracle`**.
It runs the same chain the clock ran — movers fetch, top-up, render, self-checks — as one
command, under one lock, with one exit code, and it prints the Front Page back to him.

Around that, four things changed inside the paper itself:

1. **The roster went from 10 symbols to 18**, chosen by a single live probe of Binance's
   USDT-M contract list against the operator's own 22-name watchlist. Four names have no
   Binance perpetual and were dropped by his ruling.
2. **Finding C-0 is closed.** The calibration logger had been writing a literal `0.0` for
   `maturity_withheld_fraction` on every asset of every run since the Oracle was born, and had
   never recorded family-cap binding or target buckets at all. It measures all three now.
   **Every calibration JSON written before this build is hollow for those three families.**
3. **The paper gained a range layer and a market page.** Each symbol now shows where price sits
   inside its macro range, and the last two pages list the top 50 movers overnight and over the week.
4. **It is typeset as a newspaper** — eight sections in a fixed order, on paper-coloured stock,
   with one red reserved for alarms.

Everything in item 3 and 4 is display. No gate, filter, station, heat, card, alert price or
sizing computation reads a range or a mover, and three fixtures exist to keep it that way —
one of which was found to have three holes in it, by review, and was repaired.

**What is still owed to the operator:** the PARITY line (unchanged, still the last human gate),
his verdict on this first edition, and rulings on eight `[VETO]` constants this build had to
default. They are listed in §6.

---

## 1 · WHAT WAS BUILT, STEP BY STEP

Eleven commits, base `cc82ca1`, 11,784 insertions across 11 files. Each step was built by one
agent, then refused or passed by a second agent that did not write the code, then committed by a
third that staged by explicit path. Four steps were refused on the first pass and repaired.

| commit | step | what landed |
|---|---|---|
| `3a5e6e7` | *(prerequisite)* | The T-7 alarm, built 2026-08-22, never committed |
| `1695a69` | D1 | `engine/rangefinder.py` — the v2 machine lifted out of the twin |
| `d8fa962` → `7ce235c` | A | The `/oracle` skill and the wrapper's `ondemand` job |
| `31da6d0` | E1 | `scripts/oracle_movers.py` — the fetch-only movers organ |
| `34e19e8` | B | The C-0 fix in the D-7 calibration logger |
| `d63592f` | C | The roster as a named constant; scope re-enumerated; 10 symbols backfilled |
| `ee93644` | D2 | The RANGE layer: Board cell, Tide Tables, Edge Watch, 8 tape columns |
| `7a1df59` | E2 | THE MARKET PAGE, reading the movers json only |
| `fa1bf80` | F | The newspaper typesetting |
| `26a27c7` | *(review)* | 22 repairs from the five-lens adversarial review |

### 1.0 · The prerequisite nobody had committed

Before OR-1 touched anything, `scripts/oracle_wrapper.py` and `scripts/oracle_fixtures.py` were
sitting **modified and uncommitted** in the working tree, +186 and +95 lines. That diff is the
W2 "flagfile" alarm (T-7), built on 2026-08-22, which the ledger records as `BUILT … GREEN 12/12
[verified]`. The publish was held that night for an unrelated index collision and the change was
never committed. It has been running from the working tree, under launchd, for thirty days —
the production logs show it raising and clearing `ORACLE_DOWN.flag`.

It was committed **on its own, first**, byte-for-byte as it ran (`3a5e6e7`), so that a month of
someone else's proven work would not ride into the repository under OR-1's name.

### 1.1 · STEP A — the `/oracle` skill and the on-demand job

`scripts/oracle_wrapper.py` gains one new job, `ondemand`, alongside the clock's untouched
`oracle` / `topup` / `catchup`. The diff is insert-only where it matters: an AST comparison
against HEAD shows 30 of 34 pre-existing functions byte-identical.

The chain, under **one** lock acquisition, driven by a single named constant `ONDEMAND_STEPS`
that is the only source of truth for the order:

| step | who | what |
|---|---|---|
| 1 `identity-gate` | wrapper | CONVENTIONS §0, both sides: ROOT is `$HOME/Naiad` and no cloud-tree marker. HALT exit 2, nothing touched |
| 2 `flag-first` | wrapper | a standing `ORACLE_DOWN.flag` is printed **verbatim, before any work** |
| 3 `movers-fetch` | wrapper | `oracle_movers.py` in its **own process**, 600 s timeout |
| 4 `scope-topup` | wrapper | the pinned-scope top-up, slot string `on-demand` |
| 5 `oracle-render` | wrapper | `oracle_daily`, cache-only, + 3 self-checks + one selfcheck row |
| 6 `front-page` | wrapper | the Board's top rows by heat, verdict, path/bytes/sha, banner state |
| 7 `alarm` | wrapper | one rc, one flag decision, **no schedule check** |
| 8 `open-render` | skill | `open <path>` |
| 9 `report-back` | skill | what the operator is told |

Three decisions inside it are worth naming:

- **The schedule-drift check is never run for this job.** On the clock's jobs that check reads
  the five retained plists and, on drift, calls `arm()` — which *rewrites a plist and runs
  `launchctl bootout` + `bootstrap`*. With the schedule suspended that is exactly the action
  the operator forbade. The on-demand job logs one line saying the check is skipped and why.
- **`--install` is refused by name**, twice over: `main()` dispatches the on-demand job before it
  looks at `--install`, and the job itself refuses it as its first act. Exit 2, nothing touched.
  (`--install` typed *alone* is still the clock's arming verb and is still unguarded — see §6.)
- **A failed top-up no longer has its alarm erased by the render that follows it.** Under the
  clock, a top-up that failed at 06:45 raised the flag and the clean 07:00 render cleared it
  seven minutes later — measured on 2026-09-21. The on-demand chain exits nonzero and **leaves
  the flag standing** while still printing the edition (ruling T-3). Fixture F-SK-2c drives the
  old two-command morning through the real `main()` to show the hazard it closes.

`.claude/skills/oracle/SKILL.md` documents the three verbs, walks the nine steps quoting the
wrapper's **real** log lines, and orders the run detached — `run_in_background`, `python -u`,
appending to `logs/launchd/oracle-ondemand.log` — because a wire-down full edition outlives any
foreground timeout, and a run cut off mid-chain used to die silently holding the lock.

### 1.2 · STEP B — the C-0 fix

`write_calibration` wrote `"maturity_withheld_fraction": 0.0` as a **typed literal** for every
asset on every run. Family-cap binding counts and target-bucket occupancy were absent entirely.
A1-4 requires them measured. The finding was filed on 2026-08-16 and had stood open since.

All three are now measured:

- **Maturity** — bar counts per rolling VWAP window, counted with the same membership rule
  `rolling_vwap` itself uses, then `analytics.vwap.maturity(bars)`, and the withheld fraction
  computed from what the 16/60 floors *would* withhold. Nothing about which levels enter the
  registry changed: measuring is display, withholding would be a semantic change.
- **Family-cap binding** — per asset, clusters where a family sits *at* the cap and, separately,
  *over* it (only the second actually reduces the score). `FAMILY_CAP` is imported from
  `analytics.levels`, never copied.
- **Target buckets** — NEAR / MID / FAR, on both ATR bases, with a NONE bucket for assets
  carrying no card.

**The honest result, stated because it matters to BR-2:** `maturity_withheld_fraction` measures
a true **0.0** on every asset. The 7-day and 30-day windows hold about 168 and 720 1h bars
against floors of 16 and 60, so the floors cannot bind. The contract's phrase *"measured values
differ across assets"* is discharged by the measured block as a whole — cap binding takes 10
distinct values across the roster and target occupancy 7 — not by that number. F-BR-13's motion
leg proves the number itself moves: at 168 bars it is 0.0, at 20 bars 0.4, at 12 bars 0.5.

**Hollow files are told apart by content, not by date.** A measured document carries
`schema_version >= 2`; a hollow one carries no `schema_version` at all. This matters because
`oracle_calibration_2026-09-21_full.json` — written by the clock's last 07:00 run, hours before
this commit — is dated today and is hollow. All 57 pre-existing files lack the key.

### 1.3 · STEP C — the roster

**One** GET of `https://fapi.binance.com/fapi/v1/exchangeInfo` at `2026-09-21T15:45:56Z`
(HTTP 200, 1,123,065 B, response sha256 `289fe905…`, 905 symbols, 528 of them
PERPETUAL·TRADING·USDT). The raw body was kept so nothing needed a second call.

**KEPT — 18, in the operator's order:**
`BTCUSDT ETHUSDT ENAUSDT SOLUSDT USELESSUSDT NEARUSDT 1000PEPEUSDT LITUSDT FARTCOINUSDT
HYPEUSDT XPLUSDT ZECUSDT UNIUSDT LTCUSDT BNBUSDT XMRUSDT DOGEUSDT 1000BONKUSDT`

**DROPPED — 4, by ruling, all absent from exchangeInfo:** `NPCUSDT PUMPFUNUSDT MNTUSDT ZCATUSDT`

**LEAVING THE ROSTER — 2:** `JTOUSDT` and `TAOUSDT` are in the old 10-symbol roster and are
cached, but they are not among the operator's 22. Their 12 cache files are retained untouched.

The roster is now a literal tuple in `oracle_daily.REGISTER['ROSTER']`, `ruled: True`, citing the
operator's ruling verbatim. **`engine/cells.py` `SYMBOLS` was not touched** — that is the frozen
study basket and the Oracle no longer borrows it. The full §6.4 dependents table (NAME, VALUE and
THRESHOLD-TEXT greps, with a PIN-or-IMPORT decision recorded per site) is at
`research_outputs/oracle/or1_transcripts/CCODE_dependents.md`.

**Backfill.** The ten new symbols had no cache at all. Each was backfilled from its own first
candle across the Oracle's four intervals — 40 new parquet files, **6,504,861 rows**, 40/40 on
the first attempt, 0 retries, 0 throttle events, 15 min 58 s with four parallel processes.
Verified afterwards: **0 gaps** (by `oracle_topup.contiguity`), 0 duplicates, 0 NaN, monotonic.
All 60 pre-existing cache files unchanged by `(size, mtime_ns)` against a snapshot taken first.
The cache grew 632 MB → 792 MB.

`scripts/backfill.py` was deliberately **not** used: it rewrites `research_outputs/coverage/coverage.json`,
which is git-tracked, and parallel runs would have clobbered it. `engine.data.backfill_klines`
was called directly instead.

### 1.4 · STEP D — the range layer

**D1, the lift.** The pure machine — `ATR_LEN`, `PINS`, `PINS_V2`, `MEM_CAP_PER_SIDE`, `Range`,
`run_machine`, `_span`, `_span_at`, `containment`, `flips_and_leash`, `run_v2` — moved verbatim
into `engine/rangefinder.py`. The twin keeps its loaders, KEY tables, scoring and exports and
imports the machine back.

Two traps were live and both were handled:

- F-RF-10's break leg monkeypatches `rangefinder_twin.MEM_CAP_PER_SIDE` and then calls the twin's
  `flips_and_leash`. A plain re-export would have made that patch inert — the break leg would go
  green and the fixture would prove nothing. The twin keeps a thin wrapper that reads **its own**
  global at call time.
- `tierc2/3/4` fixtures raw-text-scan every file in `engine/` for the substrings `import analytics`
  and `from analytics`, comments included. Neither appears anywhere in the new file.

Two additive functions are new: `tape_from_klines` (the rename/ts logic, no IO) and `snapshot`,
which is what the Oracle displays.

**D2, the layer.** Per roster symbol, from the h4 frame already loaded — no new `load_lens` calls,
no new intervals. The Board gains a RANGE cell; a new **Tide Tables** section lists every symbol;
**Edge Watch** is the sub-list within 0.5 ATR of a macro boundary or carrying an open pending
breach. Eight `range_*` columns are appended to the tape. No range data reaches the calibration
JSON at all.

Two honest footnotes ride on the page: the pins were calibrated on BTC and are **uncalibrated on
every other symbol**, and the machine's event log rounds to 2 dp, which distorts *micro*
containment on sub-dollar assets — this layer reads only full-precision *macro* fields.

### 1.5 · STEP E — the market page

`scripts/oracle_movers.py` is its own organ in its own process. Universe from exchangeInfo
(PERPETUAL · TRADING · USDT, **printed, never asserted**). Overnight is the exchange's 24 h
`priceChangePercent` in one call; the week is `close_now / close of the 1d bar 7 back − 1` from
`limit=8` daily klines per symbol, about 530 calls through a bounded pool.

It **never writes the kline cache** — F-MV-1 fingerprints all 662 MB of it around a real run —
and it writes a `status: FAIL` document with empty tables over any earlier same-day success
rather than leave a stale one readable. A placeholder is on disk *before* the first call, so even
SIGKILL cannot leave yesterday's numbers looking like today's.

`oracle_daily` reads the json **only**, for the edition's date only. Absent, wrong-dated,
`status != OK` or unparseable all print `WIRE DOWN — no movers this edition` and zero rows.
There is no fallback to the latest file, and F-MV-8's break leg plants exactly that fallback.

### 1.6 · STEP F — the typesetting

Paper `#F4ECD8`, ink `#1A1A1A`, one red `#B3261E`. Each hex appears exactly once in the page.
Serif stack `"Iowan Old Style", Palatino, Georgia, serif`. Eight bare `<h2>` sections in the
contract's order: **Front Page · The Docket · The Watch · Tide Tables · Telegrams · The Market
Page · Yesterday's Returns · Colophon.** The Spaghetti SVG became an `h3` inside The Watch and
the `[VETO]` appendix an `h3` inside the Colophon, so nothing from the old page was lost.

All 18 mantle strips carry the caption verbatim. The staleness banner became the red
`LATE EDITION — wire stale since <as-of>` band under the masthead.

**Semantics untouched, proven twice.** The builder wrote `semantic_diff.py`; the verifier
distrusted it and wrote its own, rendering one view through both templates at three different
as-of times. Result: the only two rows that appear in the new page and not the old are the two
new `[VETO]` register names. The tape is identical cell for cell. Function-level AST diff shows
the changes confined to the template, the edition count and the banner.

**One hazard closed on the way.** `oracle_fixtures._sec` finds sections by heading text, and
"The Board" became "Front Page". Had the selector not been updated, both renders would have
returned the empty string, compared equal, and `refresh_idempotence` would have **passed
vacuously — in the daily production self-check as well as the fixture.** The selectors were
updated and the helper hardened so an empty or missing section is now a FAIL with a stated reason.

---

## 2 · THE FIXTURE TRANSCRIPT

Two-leg throughout: the BREAK leg runs first and must go RED **for its own named reason**; a
break leg that passes is reported as `FIXTURE IS VOID`. Full verbatim transcripts — 924 KB, 12
files — are at `research_outputs/oracle/or1_transcripts/` (off-bus, gitignored), sha256 below.

### 2.1 · Final state of every suite

| suite | command | result |
|---|---|---|
| F-BR (sandboxed, fresh render by current code) | `scratchpad/sandbox_suite.py` | **GREEN 17/17 · RED 0** |
| on-demand | `scripts/oracle_ondemand_fixtures.py` | **GREEN 11/11 · RED 0** |
| movers | `scripts/oracle_movers_fixtures.py` | **GREEN 9/9 · RED 0** |
| top-up | `scripts/oracle_topup_fixtures.py` | **GREEN 6/6 · RED 0** |
| rangefinder v1, frozen tape | `scripts/rangefinder_fixtures.py` | **8/8 GREEN**, before and after the lift |
| rangefinder v2, frozen tape | `scripts/rangefinder_fixtures_v2.py` | **8/8 GREEN**, before and after the lift |
| unit tests | `pytest tests -q` | **261 passed** |

### 2.2 · The new fixtures, and what each break leg plants

```
F-BR-13 — C-0 — the D-7 logger MEASURES maturity, family-cap binding and target buckets
  [BREAK] RED (correct): SOURCE PLANT (literal 0.0 replanted) -> 'maturity_withheld_fraction'
          is assigned the typed constant 0.0 — finding C-0 replanted
  [PASS]  no constant is assigned to any of the 16 C-0 record keys, every one is seen being
          written, VW.maturity() is called, FAMILY_CAP imported

F-BR-14 — THE RANGE LAYER RENDERS, NEVER RULES
  [BREAK] RED (correct): SHA PLANT (one comment appended to a copy of posture_engine.py)
  [BREAK] RED (correct): BYPASS A — the range machine imported a second way (rangefinder_twin)
  [BREAK] RED (correct): BYPASS B — bare `import engine`, reachable by attribute walk
  [BREAK] RED (correct): BYPASS C — a sys.modules[...] lookup
  [BREAK] RED (correct): RENDER PLANT — an allow-listed reader MUTATED the view during
          render_html, symbol order ['ETH','BTC','ENA'] -> ['ENA','BTC','ETH']
  [BREAK] RED (correct): VALUE PLANT — the box is upside down: top 100.0 is not above bottom 120.0
  [PASS]  posture_engine.py sha256 1e3b3ba2… == the pinned constant: byte-unchanged;
          no `rangefinder` and no `oracle_movers` component in any decision closure

F-BR-15 — the eight sections, the captions, the LATE EDITION band
  [BREAK] RED (correct): caption removed from one strip / two sections swapped /
          DISPLAY-ONLY stripped from the Colophon / A2-7 threshold plant (2 -> 2000)

F-BR-16 — ROSTER — one literal definition, in the operator's order
  [BREAK] RED (correct): the old binding replanted — ROSTER reads `tuple(SYMBOLS)`
  [PASS]  REGISTER['ROSTER'] is a LITERAL tuple of 18, equal IN ORDER to the probe's KEPT list

F-BR-17 — the Oracle never fetches and never writes the cache
  [BREAK] RED (correct): module-level `import requests` / REST_BASE imported INSIDE build_view /
          backfill_klines in build_view / cache_dir outside its disclosed homes / fail-closed

F-SK-1 … F-SK-3 (on-demand, 11 legs)
  [BREAK] RED (correct): a skill copy with one step removed; a planted altered log line;
          a dry run that takes the lock; a lock stamped 31 min old whose pid was ALIVE
          being reclaimed; a flat denial that an edition was written

F-MV-1 — THE CACHE IS NEVER WRITTEN — sha-identical across a real run
  [BREAK] RED (correct): all 3 plants caught, each alone — a new parquet dropped in;
          an in-place rewrite with the same size and mtime; …
  [PASS]  71 files, 662,869,833 B, fingerprint sha256 255832f7… identical before and after

F-MV-2 — FIREWALL — import closure, source AST, one write path
F-MV-3 — universe ENUMERATED: 528 == len(universe) == distinct >= 150
F-MV-5/6 — a dead wire writes FAIL over success; SIGKILL cannot leave a stale success
F-MV-8/9 — WIRE DOWN honesty; the Market Page is the only mover reader

F-TU-1 — SCOPE IDENTITY — 72 pair(s), 18 symbols × [15m,1h,4h,5m], both directions

F-RF-1 / F-RF-1v2 — DETERMINISM — byte-identical event logs through the module lift
```

### 2.3 · G-5 — byte-identical through the lift

On the tape frozen at `open_time <= 1787371200000` (2026-08-22T04:00Z), all five event-log
sha256 values are **identical before and after** the lift:

| artifact | events | sha256 |
|---|---|---|
| v2 macro | 92 | `2145418831a00be710fb401c3a7c16722c0857feda4a29d58d503f3dc2b09ed4` |
| v2 micro | 573 | `73798d744a377d6f2398020b0ae891d2f34efab2e48fda1c0e745243e2b04c72` |
| v2 leash | 153 | `824cdff43675053a54f5c2cbbec9ba8b87c2e3661fca20c00459880bd17ec54e` |
| v2 suppressed | 17 | `e7b0de6a072ea9ba0c5bb0b7dc2c0ebba72d68e2730b1e6056f26fa7189dba70` |
| v1 body | 152 | `af2485e664bf822492e8bb86ef4c45afb05844bed5e342f4a9aa30588dba5404` |

`G-5 diff: IDENTICAL — 140 lines compared, 0 differ.` Both suites 8/8 on that tape.

**Pre-existing and not OR-1's to fix:** on the *live* tape both suites are red from tape drift —
the windows are `tail(N)` of a cache that has moved a month past the KEY literals (v1 5/8 with
F-RF-1's break leg void, F-RF-2 and F-RF-7; v2 7/8 with F-RF-7c). The pass/fail sets are
**identical before and after the lift**. The concurrent TIER-C10 lane is addressing it with a
record anchor.

### 2.4 · The re-pin chain

Any byte change to `scripts/oracle_daily.py` makes `oracle_topup.load_scope()` HALT until the
scope is re-enumerated. Five steps edited that file, and each re-pinned **last**, in its own
commit, in the house order:

```
1. edits land                   -> oracle_daily.py sha changes
2. load_scope() BEFORE re-pin   -> "HALT: oracle_daily.py has changed since the scope
                                    was enumerated."          <- the guard works
3. oracle_topup.py --enumerate  -> 72 pair(s), 18 symbols x [15m,1h,4h,5m]
4. load_scope() AFTER re-pin    -> 72 pairs OK
   pinned 6f456576…   current 6f456576…   MATCH
```

Final state: `scripts/oracle_daily.py` sha256 `6f456576092e5fca19d443ea89bf38caed5469cdcb78c73e15211b60c2dd8dc4`,
equal to `topup_scope.json` `oracle_daily_sha256`. `oracle_topup.py --dry-run` exits 0 with no HALT.

---

## 3 · THE ADVERSARIAL REVIEW, WHICH RAN IN FRONT OF THE PUBLISH

Five lenses over the whole OR-1 diff — the firewall, the `/oracle` chain as it will actually be
run, fixture honesty, whether any number moved, and stale words. **32 findings raised.** Every
one was then handed to an independent skeptic told to *refute* it and default to "not real".

**7 refuted and dropped. 25 confirmed. 22 repaired in `26a27c7`. 3 reported, not fixed.**

### 3.1 · The three that mattered

**The range wall had three live bypasses.** F-BR-14 proved a range never reaches a gate — but
only for code reaching the machine through the fenced `RNG` alias. A gate reaching it via
`import rangefinder_twin`, via a bare `import engine` attribute walk, or via `sys.modules` passed
**both** legs. Worse, the raw-text scan that is the *only* guard on the 14 decision-side files the
fixture never imports missed `import rangefinder_twin` outright, because `\b` does not match
before an underscore. The wall now fences the machine by substring, tests all three routes, and
plants STEP D's own forbidden sentence — *"it is 0.4 ATR from the top, so damp the heat"* — down
each one.

**F-BR-14 wrote the ledgers before it rendered**, the reverse of `run()`'s own order. An
allow-listed reader that mutated the view in place — `view["assets"].sort(...)` where
`sorted(...)` was meant, one keystroke — would have been invisible to the fixture while
corrupting the real tape and the real D-7 record. The leg now runs in `run()`'s order and proves
the view unmutated across the render, through a side channel the comparison dict cannot carry.

**Nothing enforced the Oracle's never-fetch rule.** `oracle_daily.py` could have imported
`requests` and called `backfill_klines` inside `build_view` with the suite 16/16 green — the
sandbox gate's "live lane untouched" line did not even watch the kline cache. New **F-BR-17**
AST-scans both Oracle sources for 8 network names and 7 cache-writing names, including names
inside imports, so a lazy in-function import is caught where an import-closure check is blind.
The sandbox gate now fingerprints the cache too.

### 3.2 · The other 19 repairs, in brief

The range layer's **numbers** were entirely unfixtured — F-BR-14 proved only that a range never
*gates*, so corrupt boundaries, positions and ATR distances would have printed and taped with the
suite green. Three value legs were added. `LOCK_STALE_MIN` at 30 minutes sits *inside* a
wire-down edition's own measured worst case, and the age reclaim never checked whether the holder
was alive, so two editions could have run concurrently over one `oracle_<date>.html`; a live pid
is now never reclaimed at any age. A cut-off run printed `NO EDITION WAS PRINTED` one line below
the log line naming the edition it had just written. F-BR-8's payload-sha floor counted the
posture-canon sha, so an edition missing a strip stamp passed. The Colophon told the reader in
prose that every open constant is BR-2's problem when 5 of the 14 rows beneath it are OR-1's own
defaults awaiting the **operator**. Nine stale-prose repairs across the wrapper, the top-up
REGISTER, the fixtures and the skill.

### 3.3 · Refuted by the skeptics — recorded so they are not re-raised

Seven findings did not survive: a claimed `--job` typo escape, a claimed mis-framing of the
wrapper's FRONT PAGE block, an orphan-log-line claim, a stale-movers claim against F-MV-3/4, a
claim that "No. N" counts days rather than editions, a commit-message forward-reference claim,
and a claim about this ledger's own head entry.

---

## 4 · THE FIRST EDITION — `/oracle` RUN FOR REAL

The skill was invoked as the operator would invoke it, and it was followed as written: detached,
`python -u`, appending to `logs/launchd/oracle-ondemand.log`, the run's own block read from the
last wrapper header down to its `=== exit` line.

```
~/venvs/naiad/bin/python -u scripts/oracle_wrapper.py --job ondemand --slot on-demand-full \
    >> logs/launchd/oracle-ondemand.log 2>&1
```

**Exit 0. 139 log lines** — the skill's own text predicts "about 139 lines" for a full edition on
the pinned 72-pair scope, written before the first run existed.

| | |
|---|---|
| started | `2026-09-22T01:22:51Z` (`2026-09-21T22:22:51-03:00`, Buenos Aires) |
| STEP 1 identity-gate | **PASS** — ROOT is `$HOME/Naiad`, no cloud-tree marker in ROOT or cwd |
| STEP 2 flag-first | no `ORACLE_DOWN.flag` standing |
| STEP 3 movers-fetch | **OK**, exit 0, 27.1 s · universe **528** · 0 errors · peak used weight 385/min |
| STEP 4 scope-topup | **PASS** — `+2,745 rows across 72 pair(s), 0 gap(s)` |
| STEP 5 oracle-render | 3/3 self-checks **PASS**; one row appended, `slot="on-demand-full"` |
| STEP 6 front-page | verdict PASS, banner none |
| STEP 7 alarm | `rc_topup=0 rc_oracle=0 -> exit 0`; schedule check **skipped**; no flag to clear |
| total | 234.4 s |

**The edition**

```
/Users/luis/Naiad/briefs/oracle/oracle_2026-09-21.html
  451,533 B  sha256 241d401b7a9bba9447e328a6cea9d561341a79172047c26153a18c8943a568b2
  edition Vol. I · No. 35 · Morning Edition · as-of 2026-09-21T20:00Z · roster 18
  BANNER none — no staleness band in this render
```

```
research_outputs/oracle/tape/oracle_tape_2026-09-21.parquet
   21,579 B  sha256 eb6991a33e056baa9eeb350c17392668c95e5e40e3563a432ebcbdbc296895cf
research_outputs/oracle/calibration/oracle_calibration_2026-09-21_on-demand-full.json
   21,434 B  sha256 6598fd2e05100de14e42d87cd1bdd6240480b324720a03f9cabdfd691b92550a
research_outputs/oracle/movers/movers_2026-09-21.json
  104,855 B  sha256 33f789b56b2e88544433c802e43e2ea01d2d92d2da91694161bd81b82d7e04d2
```

**FRONT PAGE, as logged**

```
  FRONT PAGE — top 5 of 18 Board rows by heat
     1  LITUSDT        STALKING   heat= 6.507
     2  USELESSUSDT    STALKING   heat= 3.956
     3  BNBUSDT        STALKING   heat= 2.920
     4  1000BONKUSDT   STALKING   heat= 2.843
     5  BTCUSDT        ARMED      heat= 1.992
  SELF-CHECK VERDICT: PASS — refresh_idempotence PASS · tape_append_integrity PASS ·
                             thumbnail_provenance PASS (row slot=on-demand-full)
  BANNER none — no staleness band in this render
```

Stations across the 18: 4 TRIGGERED · 4 ARMED · 9 STALKING · 1 DEAD. 417 fired events in the
last 24 h across 12 (lens, class) cells.

**The eight sections, as they printed**

```
1  Front Page — where is business possible today
2  The Docket — Trap Cards, pre-framed if-thens
3  The Watch — living 12/89 windows
4  Tide Tables — macro ranges, display-only
5  Telegrams — R1 alert prices, paste-ready
6  The Market Page — overnight and the week, display-only
7  Yesterday's Returns — the ORACLE GRID footer, the last 24h of fired events
8  Colophon — display-only: the provenance, and the rows still open
```

18 mantle strips, 18 captions.

**EDGE WATCH — 1 of 18**

```
asset  dist ATR  boundary  position  why it is here
BNB       1.19      top      118.3%  breach PENDING — top · 3 bar(s) out · 4 close(s) beyond ·
                                     opened 2026-09-21T08:00Z
```

**The measured calibration record** (`schema_version: 2`, the first non-hollow file):

- `maturity_withheld_fraction` is **0.0 on all 18** — measured, not typed. Every rolling window
  holds 168 (7 d) or 720 (30 d) 1h bars against floors of 16 and 60, so the floors cannot bind.
- `family_cap_binding` takes **16 distinct values across 18 assets**: `at_cap` ranges 0–5,
  `over_cap` 0–1. This is the block that carries the information BR-2's WORK(1) needs.
- `target_bucket`: NEAR 9 · NONE 8 · NO_TARGET 1 — every open card buckets NEAR, which is
  structural (the card's target is the nearest scored cluster beyond entry) and is itself a
  finding for BR-2.

**The suite that could only go green after a real edition.** `scripts/oracle_fixtures.py` run
bare audits the newest edition on disk. Through the whole build it read RED 4 against the
pre-OR-1 page of 2026-09-20, which was the declared expected state. Against this edition:

```
GREEN 17/17 · RED 0
```

`selfcheck_log.jsonl` is now 69 rows; the last is
`{"date":"2026-09-21","ts":"2026-09-22T01:26:46Z","slot":"on-demand-full","verdict":"PASS",
"catchup":false,"seconds":234.4,"zone_agree":true}` — the first row any run-based gate under
A-BR2-2b will count.

The render was opened for the operator (STEP 8).

---

## 5 · FINDINGS — REPORTED, NOT FIXED

**OR1-a · The page's as-of stamp reads only the hottest asset.** `view["as_of_ms"]` is the as-of
of whichever asset the heat sort put first, and the LATE EDITION band compares only that one bar
against the limit. Every other roster symbol is computed at its own last cached bar with no age
test anywhere. A skeptic reproduced it: with one symbol's tape cut back 3 days in memory, the
dateline still read `as-of bar 2026-09-21T12:00Z · roster 18`, the band stayed **silent**, and
that symbol's Board row, Trap Card and **R1 alert prices** printed from an 84-hour-old bar with
no mark. The operator pastes those prices into alerts. This predates OR-1, but STEP C took the
roster from 10 to 18 and widened the exposure. Only Tide Tables says rows are measured at each
symbol's own bar. **A per-symbol age column and a roster-wide staleness rule are a semantic
change and need an operator ruling.**

**OR1-b · `--install` typed alone is still unguarded.** Beside the on-demand job it is refused,
but alone it still calls `arm()` on all five labels: it rewrites each retained plist, runs
`bootout` + `bootstrap`, and prints `ARMED <label>` whatever happens, since `bootstrap_rc` never
reaches the exit code. The `disable` overrides should refuse each bootstrap, so the likely result
is not five armed agents but **five rewritten plists** — same bytes, new mtimes — which is exactly
what the suspension audit checks. Guarding it changes legacy behaviour and needs a ruling.

**OR1-c · `STEP 7 alarm: rc_topup=0` is printed on runs where the top-up never ran**, and reads
identically to a run whose 72-pair top-up came back clean. Reproduced: a `--no-fetch` chain and a
clean-top-up chain emit byte-identical alarm lines. Cosmetic, but it is the same class of
conflation the module's own comments cite from the D1/D2 findings.

**OR1-d · An interrupted sandbox-gate run leaves a look-alike artifact set.** `sandbox_suite.py`
creates its temp dir *under* `research_outputs/oracle/` so F-BR-9's `relative_to(ROOT)` does not
raise. On SIGKILL the cleanup does not run, leaving ~864 KB of fixture files — a
`posture_canon.json`, a calibration record and a tape parquet all dated today and named exactly
like the live lane's, two levels below it. Gitignored, and no current glob reaches them, but they
accumulate silently. One such orphan was on disk during this build.

**OR1-e · Pre-existing, from the scouts:** `engine.data._get` retries every non-200/404 status
including 429/418, ignores `Retry-After`, sleeps even after the last attempt and hides the
response, so the movers organ's used-weight brake never sees a 429. `analytics/INTERFACE.md`'s
maturity section still documents the superseded 10/30 floors against the code's ruled 16/60.
`scripts/oracle_topup.py`'s ABSENT message points at `scripts/backfill.py`, which without
`--symbols` walks the 10-symbol study basket, not the Oracle's 18.

**OR1-f · Data findings.** `data.binance.vision` monthly archives for LTCUSDT are short in
2022-02 and 2022-04; the REST remainder filled them and the final series is gap-free.
`1000PEPEUSDT`'s exchangeInfo `onboardDate` is `2023-05-05T00:00Z` but its first real candle is
`16:30Z` — not a gap. Four dropped names have near-name live contracts in the same response —
notably **PUMPFUN → `PUMPUSDT`**, a live perpetual. Mapping a dropped name onto a different
ticker is an operator ruling and was **not** made.

**OR1-g · Queue hygiene, standing debt.** RF-1, RF-2 and RF-3 all still read `BUILT: PENDING`
although all three build documents exist; `MANIFEST.json` counts `queue_ratified_unbuilt 6`.

---

## 6 · WHAT IS OPEN, AND WHO OWNS IT

**Eight `[VETO]` constants defaulted by this build and awaiting the operator.** Six surface in
`/oracle --dry-run` every run, two in the edition's own Colophon appendix:

| constant | default | what it decides |
|---|---|---|
| `TOPUP_SLOT` | `'on-demand'` | the slot string the on-demand top-up logs |
| `MOVERS_TIMEOUT_S` | `600` | how long the movers organ may take |
| `MOVERS_LOG_TAIL` | `12` | how much of the organ's output is echoed |
| `FRONT_PAGE_ROWS` | `5` | how many Board rows are reported back |
| `MOVERS_FAILURE_HOLDS_FLAG` | `False` | whether a failed movers fetch holds the alarm |
| `CUT_OFF_SIGNALS` | `SIGTERM, SIGHUP` | which signals get a clean cut-off |
| `EDITION_COUNT` | distinct tape dates | what "No. N" on the masthead counts |
| `FRONT_PAGE_HEADLINE` | see below | the rule and wording of the headline |

`RANGE_LENS` (`4h`), `RANGE_WATCH_ATR` (`0.5`) and `TARGET_BUCKET_ATR` (`lens`) also stand
unruled; the operator's ratification said "6-defaults", which this build did **not** read as a
ruling on constants invented after it was written.

**The headline is new prose the operator has not seen.** It restates Board words and stale marks
only — *"Business possible: …"*, *"No fresh trigger on the roster: …"*, *"No business possible
today: …"* — but it is the paper's lead and he should rule on its voice.

**Still owed, unchanged:** the PARITY line (G-BR2-3, the last human gate, still absent from
`LEDGER_ARGUS.md`); the operator's TV-eyeball verdict on `SS12_RangeFinder_v2.pine`; BR-2 on
gates; V-7 rails (APOLLO F-C3-e).

**Honest next options.** (1) Rule the eight constants and the headline, and the paper is settled.
(2) Rule on OR1-a — a per-symbol age column is a small change with a real payoff, since R1 alert
prices are the output most likely to be acted on. (3) Leave both; nothing is broken, and every
default is disclosed on the page and in `--dry-run`.

---

## 7 · WHAT THIS BUILD IS NOT

It is not a signal, a filter or a sizing change. Not one gate, station, heat, cluster, level,
Trap Card field, net R:R or R1 price computes differently than it did before OR-1 for the same
symbol at the same as-of — proven by rendering one view through the old and the new code and
comparing cell by cell. The roster changed because the operator ruled it; the calibration record
gained measured fields that had been literals; the page gained two display sections and a
typeface. The range layer and the Market Page **render and never rule**, and three fixtures plus
an AST scan exist to keep them that way.

It is not a re-arming of the clock. The five plists are unedited, the five `disable` overrides
stand, and rolling back is the operator's action from a card he can read.

---

## 8 · DISPOSITION

BOX constants read LIVE from `publish_exchange`: `BOX_BYTES` = 16,000,000 · `FLAG_BYTES` = 64,000 ·
warn at 40% (6.40 MB) · refuse ABOVE 70% (11.20 MB). The wire flags any box-bound file strictly
over 64,000 B. The tick set is `exchange/**` plus `LEDGER.md`.

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `exchange/reports/BUILD_2026-09-21_DAILY_ORACLE.md` | yes | tracked | by `publish()` | yes | GitHub + estate zip | **see below** |
| `exchange/queue/2026-09-21_OR1_daily_oracle_ondemand_ARGUS.md` | yes | tracked | by `publish()` | yes | GitHub + estate zip | 8,297 B · 0.05% |
| `exchange/queue/2026-08-16_BR2_oracle_calibration_parity_R2_ARGUS.md` | yes | tracked | by `publish()` | yes | GitHub + estate zip | +1,818 B → 6,143 B · 0.04% |
| `exchange/status/CADENCE.md` | yes | tracked | by `publish()` | yes | GitHub + estate zip | +2,219 B → 14,010 B · 0.09% |
| `exchange/status/LEDGER_ARGUS.md` | yes | tracked | by `publish()` | yes | GitHub + estate zip | see the STATUS append |
| `scripts/oracle_daily.py` | yes | tracked | `34e19e8`→`26a27c7` | yes | GitHub + estate zip | n/a — `scripts/`, non-box |
| `scripts/oracle_fixtures.py` | yes | tracked | `3a5e6e7`→`26a27c7` | yes | GitHub + estate zip | n/a — non-box |
| `scripts/oracle_wrapper.py` | yes | tracked | `3a5e6e7`→`26a27c7` | yes | GitHub + estate zip | n/a — non-box |
| `scripts/oracle_topup.py` | yes | tracked | `26a27c7` | yes | GitHub + estate zip | n/a — non-box |
| `scripts/oracle_movers.py` | yes | tracked | `31da6d0` | yes | GitHub + estate zip | n/a — non-box |
| `scripts/oracle_movers_fixtures.py` | yes | tracked | `31da6d0`, `7a1df59` | yes | GitHub + estate zip | n/a — non-box |
| `scripts/oracle_ondemand_fixtures.py` | yes | tracked | `d8fa962`→`26a27c7` | yes | GitHub + estate zip | n/a — non-box |
| `scripts/rangefinder_twin.py` | yes | tracked | `1695a69` | yes | GitHub + estate zip | n/a — non-box |
| `engine/rangefinder.py` | yes | tracked (new) | `1695a69` | yes | GitHub + estate zip | n/a — non-box |
| `.claude/skills/oracle/SKILL.md` | yes | tracked (new) | `d8fa962`→`26a27c7` | yes | GitHub + estate zip | n/a — non-box |
| `research_outputs/oracle/topup_scope.json` | yes | tracked (negation) | `34e19e8`→`26a27c7` | yes | GitHub + estate zip | n/a — non-box |
| `research_outputs/oracle/roster_probe_2026-09-21.json` | yes | **ignored** `.gitignore:222` | not committed | no | **NOT PROTECTED** | n/a — off-bus, 16,791 B |
| `research_outputs/oracle/movers/movers_2026-09-21.json` | yes | **ignored** `.gitignore:222` | not committed | no | **NOT PROTECTED** | n/a — off-bus, 104,855 B |
| `research_outputs/oracle/or1_transcripts/` (13 files) | yes | **ignored** `.gitignore:222` | not committed | no | **NOT PROTECTED** | n/a — off-bus, 924 KB |
| `research_outputs/oracle/SUSPENDED_2026-09-21.txt` | yes | **ignored** `.gitignore:222` | not committed | no | **NOT PROTECTED** | n/a — off-bus, 3,189 B |
| `briefs/oracle/oracle_2026-09-21.html` | yes | **ignored** `.gitignore:221` | not committed | no | **NOT PROTECTED** | n/a — off-bus, 451,533 B |
| `research_outputs/oracle/tape/oracle_tape_2026-09-21.parquet` | yes | **ignored** `.gitignore:222` | not committed | no | **NOT PROTECTED** | n/a — off-bus, 21,579 B |
| `research_outputs/oracle/calibration/oracle_calibration_2026-09-21_on-demand-full.json` | yes | **ignored** | not committed | no | **NOT PROTECTED** | n/a — off-bus, 21,434 B |
| `logs/launchd/oracle-ondemand.log` | yes | **ignored** | not committed | no | **NOT PROTECTED** | n/a — off-bus |
| `~/.cache/naiad/data_cache/klines/*.parquet` (40 new) | yes | **no — outside the repo** | n/a | no | **NOT PROTECTED** | n/a — 632 MB → 792 MB |
| `~/Library/LaunchAgents/com.naiad.oracle-*.plist` (5) | yes | **no — outside the repo** | n/a | no | **NOT PROTECTED** | n/a — retained, unedited |

**NAMING TRIP-WIRE — no file created by this build trips it.** The wire flags box-bound files
strictly over 64,000 B. This build document is **43,963 B**, the OR-1 queue file 8,297 B, the
CADENCE edit +2,219 B and the BR-2 amendment +1,818 B: all four are under the wire. The ten files
the publish named are the standing list and none of them is new here (`LEDGER.md` 259,298 B ·
`LEDGER_APOLLO.md` 174,090 · `LEDGER_ATHENA.md` 143,605 · four CENSUS/TIERC build documents ·
`CONVENTIONS.md` 67,814 · `queue/008_sail-skeleton.md` 66,843). Every OR-1 file's intended home is
`exchange/reports/` or `exchange/queue/`, where the lane's documents live and where the operator
and APOLLO read them; they are prose, not data, and they stay.

> **CORRECTION, 2026-09-21, same session.** The first published version of this section asserted
> that this build document was over 64,000 B and tripped the naming wire. It is 43,963 B and does
> not. The claim was written before the document was finished and was never re-measured; the
> paragraph above replaces it. Nothing else in §8 changed. (CONVENTIONS §0 correction rule: the
> assertion is rewritten where it was made, and this note records what changed and why.)

Two off-bus artifacts are large enough to name: the edition (451,533 B) and the transcript set
(924 KB). Both are correctly off-bus — the edition is regenerable from the cache in minutes
(`.gitignore:221`, ratified under BR-1), and the transcripts are this build's evidence, pointed
at by path and sha256, never carried. **They are NOT PROTECTED:** `research_outputs/oracle/**` is
gitignored, so if that directory is lost the verbatim fixture transcripts behind §2 go with it.
Flagged for the operator; moving them under an estate-backed path is a ruling, not a builder's call.

### 8.1 · BOX-COST — before and after

| | exchange/** | LEDGER.md | TICK SET | % of 16,000,000 | level |
|---|---|---|---|---|---|
| before OR-1 (`cc82ca1`) | 2,486,908 B | 259,298 B | 2,746,206 B | 17.16% | OK |
| after OR-1 (publish `ea3be0b`) | 2,520,574 B in 110 files | 259,298 B | **2,779,872 B** | **17.37%** | **OK — below warn** |

Warn is 6,400,000 B (40%) and refuse is above 11,200,000 B (70%). The build added 33,666 B of
prose to a 2.75 MB tick set: **0.21 of a percentage point.** G-11 holds with a wide margin.
The publish line, verbatim: `publish: box OK -- TICK SET 2,779,872 B (2.78 MB) = 17.37% of
16,000,000 B (16.00 MB) [governs]`.

### 8.2 · Transcript pointers — path + sha256, never copied onto the bus

All under `research_outputs/oracle/or1_transcripts/` (off-bus, gitignored):

| file | sha256 |
|---|---|
| `STEP_A.txt` | `5d1cdcc2a732f126786ebffc15606d243530b853d7d63913423cc600c3c72395` |
| `STEP_B.txt` | `0957e519c05352cd9f289b5a446a61632979c61addc1c27b5b86e195b750fb09` |
| `CDATA.txt` | `e25a5b3be6cad391a81e502c846bc3a3cbffdb3c1303d7b0088b2a4d7c9ff2a6` |
| `CDATA_fetchlog_full.txt` | `2561eb1d27446f9a2050b2fe7de255e7b09aeed434f8d563da7d8c437809ffb9` |
| `CCODE.txt` | `b17adbaa27dc5a02ec4d56430c472ddf3eee4a257353dcee87e2efbd27a6fd9d` |
| `CCODE_dependents.md` | `1d6a00eb7dfcd40b74bd33a0c91c358975c170e923f2637a838a38efb6511ef7` |
| `DLIFT.txt` | `165c490dac68190c8d88a1b350159b3e1223dab3a64bc78202d2900d9e3310fc` |
| `DRANGE.txt` | `c2d61ecc5052d4b3b1f8079b26d3fa1189acd4a926b99f697b9769f04029cdf6` |
| `E1_MOVERS.txt` | `9f3f16774bd4717089d9623249314a62869c0070d39434ff2bdb83d518950126` |
| `E2_MARKET.txt` | `f060057bfd92b3206ae752e1f421e72691b2c07c949fdbf35a9b49c51d3644bf` |
| `STEP_F.txt` | `9c9e6207b117d5fbb96d45b4ec7918251bcd6df9dfd7b174110190577f1492ea` |
| `sandbox_suite.py` | `1c0992e8ba2718847b7cd25bd0bdfec33742f47aa06b0b832aebda2d8697564d` |
| `semantic_diff.py` | `c49752718b11c25509e395b97b023867ffa7318a1701d47745002a367eaad14a` |

---

*End of build document. The Oracle's clock is off and its paper is printed on demand; the roster
is the operator's own eighteen; the calibration record measures what it had been asserting; the
page shows where price sits in its range and what moved overnight, and neither of those numbers
can reach a gate. What it still wants is the operator's eye on the first edition, his ruling on
eight defaults, and the PARITY line it has been owed since August.*

---

## 9 · RECOVERY, 2026-09-22 — AMENDMENT A-OR1-1

**Why this section exists.** On 2026-09-22 the operator fired a recovery paste. It carried
**AMENDMENT A-OR1-1** [VETO-by-firing] and ordered a fresh session to audit the repo, then finish
the work. Until then OR-1's full text lived only in a chat paste. It now lives in the repo: the
queue file ends with `## SPECIFICATION OF RECORD`, which holds A-OR1-1 and the steps S–H verbatim.
Any future recovery reads that section, not a chat.

**What the audit found about "interrupted".** The paste assumed that the 2026-09-21 session had
been cut off mid-step. The repo says it was not. That session committed every step
(`3a5e6e7`..`26a27c7`), stamped OR-1 BUILT, and ended on its publish (`088d475`, 22:31 BA). It
left no uncommitted hunk and no stash. R3 (half-applied triage) therefore had nothing to act on.
What A-OR1-1 changed is the **spec**. Three things built on 2026-09-21 are superseded by it and
are repaired below. §1–§8 above stay as the record of what was built that day.

### 9.1 · The completion table (R2), before and after

| step | BEFORE (audit, 2026-09-22 22:17Z) | AFTER | evidence |
|---|---|---|---|
| S | DONE | DONE | 0 oracle labels loaded · 5 plists retained · 5 `=> disabled` · SUSPENDED file 5 bootstrap lines · LEDGER_ARGUS:433 |
| 1 | DONE (A-OR1-1 recorded nowhere) | DONE | queue RATIFIED line; `## SPECIFICATION OF RECORD` appended (R4) |
| A | DONE | DONE | SKILL.md tracked, `name: oracle`; all 3 verbs run `oracle_wrapper.py --job ondemand`; F-SK 11/11 |
| B | DONE | DONE | `VW.maturity()` call, no literal; schema_version 2; F-BR-13 green; pin == sha(oracle_daily.py) |
| C | DONE | DONE | probe json; REGISTER['ROSTER'] the one literal; engine/cells.py = `4257067`; 72 pairs, pairs_sha256 recomputes; 72/72 series 0 gaps; F-TU 6/6 |
| D | **PARTIAL** — machine in `engine/`; 8 range columns on the D-4 tape; F-BR-14 tested the superseded design | **DONE** `3d55988` | see 9.2 |
| E | DONE | DONE | F-MV 9/9; `movers_2026-09-23.json` universe 528 |
| F | **PARTIAL** — every full edition said "Morning" (vii); F-BR-15 locked the old rule | **DONE** `ff74a90` | see 9.2 |
| G | DONE | DONE | BR-2 queue:47 `A-BR2-2`, append-only |
| H | **PARTIAL** — owed a re-run once D/F moved | **DONE** | this section; edition 9.4; ledger STATUS; publish below (push withheld) |
| R6 | **no state file** | **COMPLETE** | `backfill_state.json`: 72/72 AT_PARITY; R6 scope (the new pairs' 5m/15m) 20/20; remaining NONE |

### 9.2 · What changed, one commit per step (A-OR1-1 vi)

- **R4 — the spec of record.** Appended to the queue file (exchange/, so it rides this section's
  publish). **`or1: step X` cannot be the subject of an exchange/ commit.** CONVENTIONS §3.4
  routes exchange/ files only through `publish()`, whose subject is fixed. The code steps carry
  the `or1:` form; the exchange changes carry `exchange: auto-publish`.
- **`3d55988` or1: step D** (A-OR1-1 iv, v).
  - New `scripts/rangefinder_core.py`: the v2 machine, copied byte for byte from
    `engine/rangefinder.py` from its `from __future__` line down. `oracle_daily` now runs
    `import rangefinder_core as RNG`.
  - New `scripts/rangefinder_core_fixtures.py`:
    - F-RF-1c: the five event shas of record (92/573/153/17/152), equal to engine.rangefinder's
      and to a second run.
    - F-RF-1d: snapshot parity on all 18 symbols.
    - F-RF-1e: source equivalence.
  - The D-4 tape is again exactly the pre-OR-1 24 columns and the pre-OR-1 `write_tape`. The new
    `write_range_tape()` writes `research_outputs/oracle/tape_ranges/oracle_tape_ranges_<date>.parquet`:
    one row per roster symbol, keyed (as_of_ms, as_of_iso, asset, lens), eight range fields with
    their dtypes pinned.
  - F-BR-14 is re-pointed at the Oracle's own machine (`ORACLE_RANGE_MODULE`), with legs (e)–(h):
    the machine, the D-4 schema, the sibling schema, and no gate reads the sibling tape.
  - The wrapper self-check fails a D-4 tape wider than 24 columns and checks the sibling tape.
  - `oracle_topup.enumerate_scope` redirects the sibling directory too. Without that, every
    re-pin would have written a live sibling tape.
  - Re-pinned in the same commit.
- **`ff74a90` or1: step F** (A-OR1-1 vii).
  - `edition_name(slot, printed_at)`: refresh prints Refresh; the full verb prints Morning
    before 12:00 Buenos Aires and Evening from 12:00:00 on. The hour is read after an explicit
    zone conversion; a naive time is refused.
  - `run()` takes the print time once.
  - The Colophon carries `Printed <date HH:MM> Buenos Aires (<word> Edition: <verb>, slot <slot>
    · A-OR1-1 vii)`.
  - F-BR-15 gains the page leg, the law table (07:00, 11:59, 12:00, 19:17, 22:26 and both
    refresh slots), and ten break plants.
  - Re-pinned in the same commit.
- **R6.** Read-only: nothing was fetched and the lock was not needed. Step C had already
  backfilled every new symbol from its first candle. `research_outputs/oracle/backfill_state.json`
  (38,241 B, sha `eafa6b02…`) records all 72 pairs:
  - parity target = max(BTC's first bar, onboardDate floored to the bar), or the venue's first
    candle where it is later (1000PEPE: +0.67 d vs onboardDate, confirmed by GET);
  - 0 gaps, 0 duplicates, 0 off-grid bars, 11,988,059 rows.
  - A future roster addition resumes from its SHORT rows.

**FROZEN, NOT TOUCHED — and why A-OR1-1 iv could only be half-applied.** Between OR-1 and this
recovery, the TIER-C10 lane made `engine/rangefinder.py` its machine of record. Its filed
registrations pin that file's bytes (`bbae464f…`, F-C10-RESUME-6) and the twin's (`168d6229…`).
They read `RANGE_MACHINE="engine.rangefinder"` and four sibling constants out of
`oracle_fixtures.py` by AST, and REGISTER['ROSTER'] out of `oracle_daily.py` by AST and regex.
Deleting or editing either file breaks a ratified lane, and the paste's own FOREIGN rule and G-2
forbid it. So:

- the Oracle now runs its own copy of the machine, held to the engine's by F-RF-1c/d/e;
- `engine/rangefinder.py` stays byte-identical. Whether it is retired or its promotion ratified is **APOLLO's call**;
- `rangefinder_twin.py` stays byte-identical and **still calls engine.rangefinder**. The step's
  "twin becomes a thin caller [of the core]" is **reported, not done**.

OR-1's `1695a69` engine hunk is recorded at
`research_outputs/oracle/recovery/D1_engine_rangefinder_1695a69.patch` (51,672 B, sha `ed6d5170…`,
off-bus). Nothing was removed.

### 9.3 · Roster (unchanged by the recovery)

- **KEPT 18**, in the operator's order: BTCUSDT ETHUSDT ENAUSDT SOLUSDT USELESSUSDT NEARUSDT
  1000PEPEUSDT LITUSDT FARTCOINUSDT HYPEUSDT XPLUSDT ZECUSDT UNIUSDT LTCUSDT BNBUSDT XMRUSDT
  DOGEUSDT 1000BONKUSDT.
- **DROPPED 4** by ruling 1: NPCUSDT PUMPFUNUSDT MNTUSDT ZCATUSDT.

### 9.4 · The recovery edition — `/oracle`, run for real

**Path that ran:** the registered `/oracle` skill, loaded in this session through the Skill
tool, following SKILL.md's chain: `oracle_wrapper.py --job ondemand --slot on-demand-full`, run
detached. It was not a hand-run of `oracle_daily`.

| | |
|---|---|
| edition | `briefs/oracle/oracle_2026-09-23.html` · **452,747 B** · sha256 `622b64200a5e50c413cbd9e044a2f95fcfb049f2ab703374c9e4c12874085d5f` |
| ear | `Vol. I · No. 36` · `Buenos Aires · 2026-09-23 · Morning Edition · Price: one toll` |
| Colophon | `Printed 2026-09-23 00:27 Buenos Aires (Morning Edition: full, slot on-demand-full · A-OR1-1 vii)`. Before 12:00 is Morning, as vii rules; this paper crossed midnight |
| as-of · banner | as-of bar `2026-09-22T20:00Z` (4h lens) · **BANNER none** |
| Edge Watch | **2 of 18** |
| movers | OK · universe **528** · 0 errors · 27.1 s · `movers_2026-09-23.json` 104,845 B |
| top-up | PASS · +136 rows · 72 pairs · 0 gaps |
| self-checks | 3/3 PASS, row `slot=on-demand-full` · exit **0** · flag none, before and after |
| roster | **18** |
| D-4 tape | `oracle_tape_2026-09-23.parquet` 16,487 B · sha `6230e46e…` · **24 columns** |
| sibling tape | `tape_ranges/oracle_tape_ranges_2026-09-23.parquet` 7,996 B · sha `8c856b66…` · 18 rows |
| calibration | `oracle_calibration_2026-09-23_on-demand-full.json` 21,440 B · sha `cd79693b…` |
| G-4 on the page | eight `<h2>` in the contract's order · 18 strips / 18 captions · DISPLAY-ONLY in the Colophon · both Market Page tables present |

The Front Page's top five by heat, as logged:

- XPLUSDT STALKING 5.415
- USELESSUSDT STALKING 3.608
- ZECUSDT TRIGGERED 3.376
- SOLUSDT TRIGGERED 2.438
- LTCUSDT TRIGGERED 2.263

**The first print was reprinted.** The first run started at 23:48 BA on 2026-09-22.
- The cache was 26 hours stale, so its top-up (+7,937 rows) ran about 33 minutes, and the render
  landed at 00:22 BA on **2026-09-23**.
- Its movers json was dated 2026-09-22, so the Market Page honestly printed **WIRE DOWN** rather
  than stale numbers.
- It was reprinted at 00:24 BA, following the skill's same-day rule. Its F-BR default run is kept as
  `H_default_mode_2026-09-23_first_print_wire_down.txt` (17/17).
- See finding 12.

### 9.5 · Fixture transcripts — two-leg, every break RED for its own named reason

All transcripts are under `research_outputs/oracle/or1_transcripts/recovery_2026-09-22/` (off-bus).
The `D_verify_*`/`F_verify_*` rounds (`.r1`, `.r2`, final) are kept beside them.

| suite | result | transcript · sha256 |
|---|---|---|
| F-BR-1..17, sandbox fresh render, after F | **17/17**, live lane untouched | `F_final_sandbox.txt` · `1cf12ceb…` |
| F-BR-1..17, default mode, on the recovery edition | **17/17** · 17 RED (correct) · 0 VOID · wall 29 min 43 s | `H_default_mode_2026-09-23_reprint.txt` · `b826b10f…` |
| F-RF-1c/d/e (core ≡ engine) | **3/3** | `F_final_rfcore.txt` · `85973dea…` |
| F-TU-1..6 (pin) | **6/6** | `F_final_topup.txt` · `96feae7a…` |
| F-SK-1..3 | **11/11** | `F_final_ondemand.txt` · `8679cc4b…` |
| F-MV-1..9 | **9/9** | `F_verify_oracle_movers_fixtures.txt` |
| pytest tests | **261** passed | `F_final_pytest.txt` · `f1bac951…` |
| re-pin after F | pin `6c03af96…` == sha(oracle_daily.py) | `F_final_repin.txt` · `149ac0bd…` |
| TC10 read-only checks | F-RF-WALLS/PINS, F-C10-RESUME-6, F-D-5/ADMIT: break RED, real PASS · F-DET proxy **IDENTICAL** (24cd11f1…), before the ledger append | this session, after D and after F |
| R2 audit baseline (before any change) | F-BR 17/17 · F-SK 11/11 · F-MV 9/9 · F-TU 6/6 · RF v1/v2 8/8 · pytest 261 | `audit_*.txt` |

**F-BR-14 was hardened across three adversarial verify rounds**, ending at 83 break plants.
The rounds found real bypasses: a gate in `run()` exempt from the text scan, a side channel
out of an allow-listed reader, dynamic imports, derived paths to the sibling tape, and
decision-side dependencies no scan covered. Each was reproduced, then repaired. The third round
still reached a gate by **deliberate obfuscation**:

- a private copy of the machine compiled from source;
- a range read by value;
- the tape read through `pyarrow.fs` via a path spelt in fragments;
- `exec`.

These are **disclosed residuals, written into the fixture**. No static-plus-behavioural fixture
closes them; a diff that spells one is a review finding on sight.

### 9.6 · Findings — reported, not fixed

1. **Main-tape parquet carrying new columns, REPORTED, never rewritten.**
   - The file: `research_outputs/oracle/tape/oracle_tape_2026-09-21.parquet`, 21,579 B, sha
     `eb6991a33e056baa9eeb350c17392668c95e5e40e3563a432ebcbdbc296895cf`, 18 rows, 32 columns.
   - The extra columns: the pre-OR-1 24 plus range_state · range_top · range_bottom ·
     range_pos_pct · range_dist_atr · range_pending_side · range_last_event ·
     range_last_event_age_bars.
   - It overwrote in place the 07:00 scheduled run's 24-column file of the same name (15,524 B,
     sha `5fc17119…`). That file's bytes equal `oracle_tape_2026-09-20.parquet`, so the 07:00
     edition carried a stale as-of. Cause unverified.
2. **The 2026-09-21 edition says "Morning Edition"**, but it was printed at 22:26 Buenos Aires.
   It stays as printed. Run bare against that set, F-BR-14 (f)/(g) and F-BR-15 (vii) are RED by
   design; the recovery edition is the set of record.
3. **`engine/rangefinder.py` and the twin**: see 9.2. APOLLO's call.
4. **A-OR1-1 i machinery is unbuilt.** No Oracle fetch path honours `X-MBX-USED-WEIGHT` or backs
   off at 80%: `engine/data._get` ignores headers and retries 429/418 blindly, and step C's
   backfill ran outside the wrapper lock. Nothing is owed today, because R6 found no pair short.
   A future roster addition needs a lane-local, header-aware backfiller under `scripts/`.
5. **Latent bypass of A-OR1-1 ii.** `names_ondemand` (oracle_wrapper.py) sends `--job=ondemand`,
   or a bare `--slot on-demand-full`, without `--install` down the legacy path. That path skips
   the identity gate, flag-first, movers and top-up, and uses an age-only lock. The T-7 flag
   decision also runs just after the lock is released. Both are low severity; they need a
   ruling to harden.
6. **The as-of stamp reads only the hottest asset** (§5 of this document). Still open; it is
   semantic.
7. **The sandbox suite of record is gitignored.** `research_outputs/oracle/or1_transcripts/sandbox_suite.py`
   runs F-BR on a fresh render; it lives only on disk.
8. **Corrections to §8.**
   - The before-row is 2,458,674 B, so OR-1 added **+61,900 B**, not +33,666.
   - At publish this document was 45,048 B, not 43,963.
   - The queue file was 8,770 B, not 8,297.
9. **TC10 coupling, for that lane.** TC10's four "verbatim" copies of `RANGE_IMPORT_LINE` spell
   `\brangefinder\b`; OR-1's spells `\brangefinder\w*\b`. That drift is older than this recovery.
10. **The audit wrote into another lane's file.** Running `rangefinder_fixtures_v2.py`'s main
    rewrote `research_outputs/rangefinder/FIXTURES_v2.txt`:
    - before: `RF v2 FIXTURES: 6/8 GREEN`, sha `43c9e331…`, mtime 2026-09-21 14:39;
    - after: `8/8 GREEN`, sha `68d5d3b3…`.
    - TC10 records only `{lines: 1}` for it, so the F-DET proxy stayed IDENTICAL.
    - Restoring it was refused by this session's permission guard. The operator's one-liner is in the ledger STATUS.
11. **The ledger append moves TC10's F-DET.** TC10's `DATA_SPEND_AUDIT.json` records
    `LEDGER_ARGUS.md` at 565 lines. The STATUS block below is appended by operator ruling
    (2026-09-22) and names no asset, so only the line count moves. TIER-C10 must re-file F-DET.

12. **An edition whose run crosses BA midnight loses its Market Page.** The movers json is dated at
    STEP 3 and the edition at STEP 5. If the wall clock passes 00:00 BA in between, `load_movers`
    finds no json for the edition's date and prints WIRE DOWN. That is honest, but avoidable: pin
    one date at the wrapper's start, or date the movers fetch by the edition. Operator rules.
13. **F-BR default mode is slow.** The run of record took 29 min 43 s (00:43 to 01:13 BA), almost
    all of it in F-BR-14's hardened legs; the sandbox suite's whole F-BR run takes about 90 s.
    Not diagnosed.

### 9.7 · Disposition and BOX COST

- **On the bus**, through `publish()`: this document, the queue file (spec of record + BUILT
  stamp) and the LEDGER_ARGUS STATUS. The tick set goes from 2,784,027 B (17.40%) to about 2,811,500 B (**17.57%**), a delta of about
  +27.5 KB: this document +16.8 KB (to about 61.8 KB, under the 64,000 B naming wire), the queue
  file +8.5 KB, and the ledger +2.2 KB. Warn is 6,400,000 B (40%): **below warn, with a wide margin**.
- **Code**, in `3d55988` and `ff74a90` (tracked, non-box): `scripts/rangefinder_core.py`,
  `scripts/rangefinder_core_fixtures.py`, `oracle_daily.py`, `oracle_fixtures.py`,
  `oracle_wrapper.py`, `oracle_topup.py`, `SKILL.md`, `topup_scope.json`.
- **Off-bus, NOT PROTECTED** (gitignored): the recovery edition and its two tapes, calibration
  and movers json; `backfill_state.json`; the recovery patch; about 80 transcripts.
- **PUSH WITHHELD by operator ruling (2026-09-22).** `publish()` always pushes the whole branch,
  and the branch carries TIER-C10's unpushed commits, whose push awaits the operator's word at
  that lane's CLOSE. This publish committed locally and pushed nothing.
