# BUILD — THE ORACLE REBIRTH · 2026-08-16

**Contract:** queue BR-1 `BRIEF_REDESIGN_SPEC_v1 — THE HUNTER'S ORGAN`, RATIFIED operator
2026-08-16 ("ratify BR-1, refresh 16:00, roster as-is"), as amended by Amendment A1 at stamp
time. **Executor:** HEPHAESTUS. **Reviewer:** ARGUS. **Merge authority:** operator.
**Class:** operations / display-only. Nothing here scores an outcome.
**Code commits:** `a36edc1` (build) + `802b3cb` (post-review repairs, section 9). **This document:** published by `publish_exchange.publish()`.

---

## 0 · THE ONE THING TO READ FIRST

THE ORACLE IS ALIVE AND UNATTENDED. Two launchd agents are armed — `com.naiad.oracle-0700`
(full) and `com.naiad.oracle-1600` (Watch/Board refresh), both at Buenos Aires wall-clock.
Two unattended runs have completed with **exit code 0** (the second after the section 9 repairs), produced the render with zero
manual steps, and logged three self-checks PASS. All ten fixtures are green, each shown
failing on a deliberate break first.

**AND IT RESTS ON A NAME COLLISION THE OPERATOR MUST RULE.** C-3 says "station canon v1
verbatim (STALKING/ARMED/TRIGGERED/DEAD)". One day earlier, ruling 2026-08-15 gave the SAME
NAME to something else: "six-station lifecycle w/ ORACLE-class mapping = station canon v1".
No document reconciles them, and **no document anywhere in the estate defines what any one of
the four posture words means**. The estate holds the enumeration and one transition sentence,
nothing more — a `git log --all -S "STALKING"` finds no deleted canon either.

This build did not invent its way out of that. It bound the BR-1 reading (the four words,
because C-3 names them), executed every gate through the already-ratified TC3 rule card, and
marked every row of the resulting map `ruled: True` or `ruled: False`. The eight PROPOSED rows
are [VETO], print in the render's own appendix, and are logged by the calibration logger every
run so BR-2 recalibrates them against a week of measurement rather than against a guess.

**Nothing self-adopted. §5 of this document is the list awaiting your ruling.**

---

## 1 · WHAT WAS BUILT

| ID | Deliverable | Path | State |
|---|---|---|---|
| D-1 | Station engine, canon v1, closed register | `scripts/station_engine.py` | built, 29,272 B |
| D-1b | The one truth source both languages read | `research_outputs/oracle/station_canon.json` | built, 8,458 B, TRACKED |
| D-2 | The daily organ | `scripts/oracle_daily.py` | built, 53,871 B |
| D-3 | Slot-anchored wrapper + two armed slots | `scripts/oracle_wrapper.py` + 2 plists | built + ARMED |
| D-4 | Parquet tape for TC4 | `research_outputs/oracle/tape/` | built |
| D-5 | This build document | `exchange/reports/BUILD_2026-08-16_ORACLE_REBIRTH.md` | this file |
| D-6 | Ledger append | `exchange/status/LEDGER_ARGUS.md` | appended |
| D-7 | Calibration logger (A1-4) | `research_outputs/oracle/calibration/` | built |
| — | Fixtures F-BR-1..F-BR-10 | `scripts/oracle_fixtures.py` | 10/10 green |

### 1.1 The render, section by section, against the contract

- **C-5 BOARD** — 10 rows, heat-sorted. Each row: regime chip (the rule card's TIDE) ·
  ATR-distance to the nearest high-score cluster · the two lines in the sand · posture word ·
  the reason for that word, printed · the heat value. Roster is `engine/cells.py SYMBOLS`
  unchanged, per A1-2 "roster as-is".
- **C-6 TRAP CARDS** — entry (the if-then, not a price to chase), structural invalidation from
  `tierc3_rules.struct_stop_4h` (4h pivot + 0.5 ATR buffer, railed to 1.0 ATR), target, net R:R
  after toll, and "what proves me wrong". Where the rule card refuses a trade — no admissible
  4h anchor — the card prints NOT TAKEN rather than inventing a rail-only stop.
- **C-7 WATCH** — live 12/89 windows with age, displacement and trigger status, plus a
  last-96-bars mantle strip per asset drawn from a v4-pattern payload.
- **C-4 SPAGHETTI** — one panel, each asset's path from its own last 89/316 tide flip,
  ATR-normalised.
- **C-8 ORACLE GRID FOOTER** — the last 24h of fired events across five lenses, each cell
  showing the GRID's own filed toll and NET.
- **C-9 R1** — 26 alert lines, `<SYMBOL> <TAG> <PRICE>`, nothing else.
- **F-BR-8 PROVENANCE** — DISPLAY-ONLY header, 11 sha256 stamps, date, and BOTH the certified
  and not-certified lists.

### 1.2 Today's render, as evidence it says something

Board (heat order): LIT ARMED · JTO STALKING · HYPE STALKING · BTC ARMED · TAO STALKING ·
NEAR TRIGGERED · SOL STALKING · ZEC STALKING · FARTCOIN STALKING · ETH STALKING.
Three Trap Cards (LIT, BTC, NEAR). 317 fired events across 12 (lens, class) cells in 24h.

---

## 2 · THE FIXTURE TRANSCRIPT — verbatim, both legs

BR-1 §4 requires each fixture "shown FAILING on a deliberate break before trusted", so
`prove()` runs both legs and **refuses to count a fixture whose break leg passed**. That rule
caught a real defect during this build: F-BR-5's first break (nudging one bar) did not move the
anchor, so the fixture was proving nothing and was marked RED until the break was made real.

```
==============================================================================
ORACLE FIXTURES — artifact set 2026-08-16
  html  231,763 B
  tape  10 rows
  cal   10 per-asset records
==============================================================================

F-BR-1 — PARITY — station WORDS vs an independent transcription, symbol for symbol
  [BREAK] deliberate violation -> RED (correct): mismatch list (7): BTCUSDT@-0: engine=ARMED independent=DEAD; ETHUSDT@-0: engine=DEAD independent=ARMED; SOLUSDT@-0: engine=STALKING independent=DEAD; NEARUSDT@-0: engine=TRIGGERED independent=DEAD; ZECUSDT@-0: engine=DEAD independent=ARMED; JTOUSDT@-0: engine=STALKING independent=DEAD  [handoff] pine/ holds SS_v12_0_1.pine only; SS v12.1 is described in PINE_LANE_PRIMER_2026-08-15 section 2 but is NOT in the repo, so marker-level parity against v12.1 itself is OWED, not discharged.
  [PASS] F-BR-1: 7/10 symbols x 4 as-of points = 28 station-word comparisons against a SECOND state machine with its own EMA/ATR/cross recursions (no engine.indicators, no station_engine) — mismatch list EMPTY (= pass).  SKIPPED 3 symbol(s) with less than 4776 4h bars of pre-fixture-day history (the independent EMA is SMA-seeded and needs the warm-up): HYPEUSDT(2633b), FARTCOINUSDT(3597b), LITUSDT(1389b).  [handoff] pine/ holds SS_v12_0_1.pine only; SS v12.1 is described in PINE_LANE_PRIMER_2026-08-15 section 2 but is NOT in the repo, so marker-level parity against v12.1 itself is OWED, not discharged.

F-BR-2 — TOLL PRESENCE — no cost-free number prints anywhere
  [BREAK] deliberate violation -> RED (correct): a NET R:R row prints no toll VALUE (the bare word is not a toll); a rendered NET R:R row prints no toll; net_rr() does not take a toll
  [PASS] F-BR-2: net_rr() takes toll_price; 3 NET R:R row(s) for 3 card(s) — counts reconcile, and every row carries a NUMERIC per-lens toll in ATR and in price from the ORACLE GRID

F-BR-3 — FIREWALL — import graph, not prose
  [BREAK] deliberate violation -> RED (correct): an oracle source calls a journal read: read_journal; an oracle source imports engine.journal directly (must be inherited only)
  [PASS] F-BR-3: station_engine closure is analytics-free (779 modules); no forward_log and no positions module is reachable (component-wise match); no oracle source imports or names a trading or journal module; no journal read is called; no outcome-aggregation symbol is assigned. DISCLOSED, NOT DENIED — these ARE in the closure, inherited via tierc2_rules -> engine.s1: engine.trading (only 'TradeResult') present=True; engine.journal (only 'iso') present=True. BR-1 section 2 permits engine modules 'imported read-only, trading disabled'; what section 2 forbids is a journal READ, and that is what is asserted above.

F-BR-4 — THUMBNAIL PROVENANCE — strip bytes derive from a sha-stamped payload
  [BREAK] deliberate violation -> RED (correct): oracle_mantle_LITUSDT_4h.json: data-block sha mismatch; oracle_mantle_JTOUSDT_4h.json: data-block sha mismatch; oracle_mantle_HYPEUSDT_4h.json: data-block sha mismatch; oracle_mantle_BTCUSDT_4h.json: data-block sha mismatch; oracle_mantle_TAOUSDT_4h.json: data-block sha mismatch
  [PASS] F-BR-4: 10 strips; each canvas binds a payload whose meta.sha256 recomputes from its own data block and is printed in that strip's footer (the shipped VIZ-4 convention: data-block sha, not file sha); and the paint routine (divRGB/heatCanvas/putImageData/paintStrips + its DOMContentLoaded hook) is present in the document

F-BR-5 — ANCHOR DETERMINISM — the C-4 tide-flip anchor, twice
  [BREAK] deliberate violation -> RED (correct): BTCUSDT: (14732, 1780099200000, 'down') != (14919, 1782792000000, 'up'); ETHUSDT: (14566, 1784577600000, 'up') != (14464, 1783108800000, 'up'); SOLUSDT: (12836, 1784894400000, 'down') != (12675, 1782576000000, 'up'); NEARUSDT: (12609, 1784318400000, 'down') != (12018, 1775808000000, 'up')
  [PASS] F-BR-5: anchor identical across two computations from the same substrate; per-asset anchor timestamps: BTC@1780099200000, ETH@1784577600000, SOL@1784894400000, NEAR@1784318400000, ZEC@1783728000000, JTO@1784491200000, TAO@1780070400000, HYPE@1784894400000, FARTCOIN@1779364800000, LIT@1779408000000

F-BR-6 — REFRESH IDEMPOTENCE — the 16:00 refresh over unchanged data
  [BREAK] deliberate violation -> RED (correct): The Board: 4805 B vs 4805 B
  [PASS] F-BR-6: Board 4,805 B and Watch 5,426 B byte-identical across two renders over unchanged data

F-BR-7 — R1 FORMAT — alert block parses as price levels only
  [BREAK] deliberate violation -> RED (correct): 1 non-conforming line(s), first: 'BTCUSDT: consider a long here'
  [PASS] F-BR-7: 26 alert lines, every one matching <SYMBOL> <TAG> <PRICE> — prices only, no prose, no advice, paste-ready

F-BR-8 — PROVENANCE FOOTER on the brief HTML
  [BREAK] deliberate violation -> RED (correct): missing: NOT CERTIFIED list
  [PASS] F-BR-8: DISPLAY-ONLY header, date 2026-08-16, 11 sha256 stamps, station canon sha, and BOTH the certified and not-certified lists present

F-BR-9 — BOX — the render and the tape never enter exchange/
  [BREAK] deliberate violation -> RED (correct): 1 forbidden artifact(s) under exchange/: ['exchange/reports/oracle_PRETEND.parquet']
  [PASS] F-BR-9: no .html and no .parquet under exchange/; the render lives at briefs/oracle/oracle_2026-08-16.html (231,955 B) and the tape at research_outputs/oracle/tape/oracle_tape_2026-08-16.parquet (15,288 B) — pointer lines only on the bus

F-BR-10 — CALIBRATION PURITY — no outcome field may reach calibration/
  [BREAK] deliberate violation -> RED (correct): outcome/performance field(s) present: ["n_wins (matched 'win')"]
  [PASS] F-BR-10: 10 per-asset records; keys ['asset', 'cluster_count', 'cluster_width_atr_max', 'cluster_width_atr_p50', 'collapse_events', 'heat', 'level_count', 'lis_distance_atr', 'lis_fallback_used', 'maturity_withheld_fraction', 'nearest_cluster_atr', 'open_window_ages_bars', 'open_window_disp_atr', 'station'] — display-machinery distributions only, no outcome field, no signal-performance field (banned vocabulary of 21 terms scanned)

==============================================================================
GREEN 10/10 · RED 0
==============================================================================
```

House fixtures unaffected: `fixtures_conventions.py` → **F-CONV 4/4 PASS** after this build.

---

## 3 · LAUNCHD ARMING PROOF

Schedules are read back **from launchd's own registry**, never from the plist just written —
the house proof standard.

```
ORACLE — arming two slots
  zone check: oracle 2026-08-16T02:12:10-03:00 · machine 2026-08-16T02:12:10-03:00 · agree=True
  ARMED com.naiad.oracle-0700: machine-local 07:00 (= 07:00 America/Argentina/Buenos_Aires)
    plutil: /Users/luis/Library/LaunchAgents/com.naiad.oracle-0700.plist: OK
    launchd reports: {'Hour': 7, 'Minute': 0}
  ARMED com.naiad.oracle-1600: machine-local 16:00 (= 16:00 America/Argentina/Buenos_Aires)
    plutil: /Users/luis/Library/LaunchAgents/com.naiad.oracle-1600.plist: OK
    launchd reports: {'Hour': 16, 'Minute': 0}
```

### 3.1 The unattended run — BR-1 §6's acceptance clause

`launchctl kickstart -k gui/501/com.naiad.oracle-0700`, then `launchctl print` reports
`state = not running`, `runs = 1`, **`last exit code = 0`**. Zero manual steps. Wall clock 5.6 s.
Log tail:

```
  selfcheck refresh_idempotence: PASS
  selfcheck thumbnail_provenance: PASS
  selfcheck tape_append_integrity: PASS
  schedule OK on com.naiad.oracle-0700: {'Hour': 7, 'Minute': 0}
  schedule OK on com.naiad.oracle-1600: {'Hour': 16, 'Minute': 0}
=== exit 0 ===
```

`selfcheck_log.jsonl` first row: `2026-08-16 full PASS zone_agree=True 5.6s
{refresh_idempotence: True, tape_append_integrity: True, thumbnail_provenance: True}`.
This is the log BR-2 gate G-BR2-2 reads.

### 3.2 UNDO — the exact commands

```
# bootout unloads the agent; the plist STAYS on disk and bootstrap re-arms it.
# Removing a plist is an operator action, never a scheduled-lane one (CADENCE §4).
launchctl bootout gui/501/com.naiad.oracle-0700
launchctl bootout gui/501/com.naiad.oracle-1600

# re-arm:
launchctl bootstrap gui/501 ~/Library/LaunchAgents/com.naiad.oracle-0700.plist
launchctl bootstrap gui/501 ~/Library/LaunchAgents/com.naiad.oracle-1600.plist
```

### 3.3 The timezone question, measured rather than assumed

`/etc/localtime` → `America/Argentina/Buenos_Aires`; `zdump -v` shows the last transition was
2009-03-15 with gmtoff fixed at −10800 ever since. **The Oracle's zone IS this machine's zone
and that zone has no DST**, so a bare `StartCalendarInterval` already lands on target and the
wrapper C-1 mandates is, today, unnecessary. It was built anyway, because the measurement is a
property of this machine today and not of the schedule: every run recomputes the correct
machine-local hour through the zone, compares it to what the plist says, and rewrites plus
reloads on drift. The day the laptop travels, the schedule corrects itself. The reschedule runs
**last**, so a bootout can never kill the run producing that day's Oracle.

---

## 4 · FINDINGS — REPORTED, NOT FIXED

**V-1 · "STATION CANON v1" NAMES TWO DIFFERENT THINGS, ONE DAY APART. [blocking a clean C-3]**
Ruling 2026-08-15: *"six-station lifecycle w/ ORACLE-class mapping = station canon v1"* — the
S1..S6 trade-lifetime kit. BR-1 C-3 of 2026-08-16: *"station canon v1 verbatim
(STALKING/ARMED/TRIGGERED/DEAD)"* — four Board posture words. A builder importing the S1..S6
gate text and a builder transcribing the four words would both claim to follow canon v1. This
build bound the BR-1 reading and pointed at the other register by path so no lane merges them.
**Operator ruling owed: which reading owns the name, and what the other one is called.**

**V-2 · THE FOUR WORDS HAVE NO PER-WORD DEFINITION ANYWHERE.** The estate holds the enumeration
(LANE_UPDATE_DIONYSUS 2026-08-13, restated in ARGUS_RESCOPE 2026-08-15) and exactly one
transition sentence: *"an arming opens a window; ... a 12/25 trigger inside one is the entry
alert; seal or counter-cross closes it."* Nothing states what STALKING means as a sentence.
C-3 forbids re-derived semantics, so the gates were taken from the ratified TC3 rule card and
only the NAMING MAP is new. Every map row carries `ruled: True|False`. **Eight rows are False
and are listed in §5.**

**V-3 · PINE SS v12.1 IS NOT IN THE REPO.** F-BR-1 as contracted compares against "Pine SS
v12.1 markers". `pine/` holds `SS_v12_0_1.pine` (plus two v11 cascade files); v12.1 exists only
as a description in PINE_LANE_PRIMER_2026-08-15 §2. F-BR-1 therefore discharges what it can and
says what it cannot: it transcribes the marker logic **directly from the v12.0.1 Pine source**
as an independent second implementation and compares it to the engine event-for-event over full
history on a frozen day — 10/10 symbols, 6 marker series each, mismatch list empty — and prints
a standing `[handoff]` that v12.1-level parity is OWED. **The operator's mid-week chart glance
(BR-2 gate G-BR2-3) is the only thing that can close it.**

**V-4 · 07:00 IS ALREADY OCCUPIED.** `com.naiad.daily` fires at `{Hour 7, Minute 0}` and ends by
calling `publish_exchange.publish()`. The Oracle agents are at the same minute. There is **no
git-index race** — the Oracle publishes nothing and writes only to `briefs/oracle/` and
`research_outputs/oracle/`, both now gitignored — but the house precedent for co-scheduled jobs
is the deliberate 30-minute offset stated in `com.naiad.workflow.plist`. C-1 pins 07:00, so
07:00 is what was armed. **Ruling available if you want the offset.**

**V-5 · THERE IS NO net R:R FORMULA IN THE ESTATE.** C-2 requires one and forbids a cost-free
number; a repo-wide search finds the phrase only in prose. This build PROPOSED
`(reward − toll_price) / (risk + toll_price)` with `toll_price = toll_atr × ATR(lens)` — the
conservative reading, since a round-trip toll is paid win or lose. Both inputs print beside
every ratio so you can re-derive it by eye. **[VETO].**

**V-6 · TRIGGER PAIR, 12/25 vs 12/26.** The Board/Watch prose says "a 12/25 trigger"; the S3
gate text says "12×25/26 ... The 25 is the ruled load-bearing shadow line [ratified]"; the rule
card, the census and the Pine all use 26. The engine uses **26** and prints the disclosure
rather than reconciling by fiat.

**V-7 · THE TWO RAILS REMAIN UNRECONCILED.** `configs/tc1_B.yaml` / engine guard G-8c carry
`min_stop_atr: 0.5`; the TC3 card rails at 1.0. The Oracle uses 1.0 per C-6. This is APOLLO's
open ruling F-C3-e, untouched here.

**V-8 · THE KLINE ESTATE IS ~1 DAY STALE AND NOTHING SCHEDULED REFRESHES IT.** Newest 4h bar
is 2026-08-15T12:00Z. The network top-up job (`daily_brief.py`) was retired 2026-08-05 by ruling
D-3. The Oracle is **cache-only by design** (it must never fetch during a firewalled run), so it
renders whatever the cache holds and stamps the as-of bar in its own header. **A top-up job is
owed if the 07:00 Oracle is to read yesterday's close.** Not in BR-1's scope; named here so it
is not discovered on a Monday morning.

**V-9 · MANIFEST LAG.** `publish` reports the manifest head 40+ commits behind live HEAD (F-4
LAG). Pre-existing, ATHENA's file.

**V-10 · THE MANTLE STRIP IS A NEW NARROW PAYLOAD, NOT A SLICE OF THE SHIPPED ONE.** The v4
payloads are decimated (stride 8 at 1h, 92 at 5m), so "last 96 bars" is 12 columns at 1h and
about one column at 5m. Rather than silently reinterpret "bars" as "steps", the Oracle emits a
fresh payload per asset whose source slice is short enough that every bar survives at stride 1.
Same `{meta, data}` shape, same thread table, same `(EMA−price)/ATR` orientation, same
null-means-absent rule, same data-block sha convention. 10 payloads, 184 KB total, off-bus.

---

## 5 · THE [VETO] TABLE — eight rows awaiting your ruling

Nothing below self-adopted. Every row prints in the render's own appendix and is written into
every calibration JSON, so a week of running measures them before BR-2 proposes values.

| Row | This build's value | Why it is not law |
|---|---|---|
| `CANON.STALKING` | complement of ARMED, + the card's reject reasons | no per-word definition exists |
| `DEAD_MEMORY_BARS` | 6 (= 24h on the 4h lens) | DEAD is a property of a WINDOW; how long a burial stays on an ASSET row is unwritten |
| `BOARD_PRECEDENCE` | TRIGGERED > ARMED > DEAD > STALKING | C-5 wants one word, C-7 lists windows plural; the collapse rule is unwritten |
| `HEAT_KEY` / `HEAT` | `score / (1 + atr_distance)` | only "proximity × cluster score" exists; no formula anywhere |
| `NET_RR_FORM` | `(reward − toll) / (risk + toll)` | no net-R:R formula exists in the estate (V-5) |
| `GRID_TOLL_KEY` | `('4h', '12_26 IN-WINDOW')` | no map from a Trap Card to a (lens, class) grid key exists |
| `FIRED_WINDOW_HOURS` | 24 | C-8 says "yesterday" and does not define it |
| — | the four-word map as a whole | see V-1 and V-2 |

Already-ruled rows taken unchanged and NOT re-opened: LENS 4h · TIDE 89/316 · WINDOW 12/89 ·
TRIGGER 12/26 · d ≥ 0.75 · ATR_LEN 14 · MIN_STOP_ATR 1.0 · STOP_BUF_ATR 0.5 · PIVOT (5,5) ·
window closed at t0 · collapse 0.02 · cluster 0.15 · LIS 1.5 · family cap 3 · maturity 16/60.

---

## 6 · VERDICT AGAINST BR-1 §6

BR-1 §6 ACCEPTs iff F-BR-1..9 pass with transcripts, one unattended 07:00 run produces the
brief with zero manual steps, and the operator confirms the Board answers "where is business
possible today" in one glance. Partial adoption is forbidden.

- **F-BR-1..F-BR-10 pass with transcripts** — §2. Ten of ten, each shown failing first. ✅
- **One unattended run, zero manual steps** — §3.1, exit code 0. ✅
- **Operator confirmation of the Board** — **OWED. This is yours, not mine.** The render is at
  the path in §7; open it and rule.

So: **built and fixtured, acceptance pending your two calls** — the Board glance, and the §5
[VETO] table.

---

## 7 · DISPOSITION

BOX constants taken by import from `publish_exchange` (`BOX_BYTES` = 16,000,000;
`FLAG_BYTES` = 64,000), never a copy. Warn at 40%, refuse ABOVE 70%; the wire flags files
strictly over 64,000 B.

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `scripts/station_engine.py` | yes | yes | `a36edc1` + repair | rides this branch push | hand commit, explicit paths (CL-13) | 29,272 B, non-box |
| `scripts/oracle_daily.py` | yes | yes | `a36edc1` + repair | rides this branch push | same | 53,871 B, non-box |
| `scripts/oracle_wrapper.py` | yes | yes | `a36edc1` + repair | rides this branch push | same | 13,426 B, non-box |
| `scripts/oracle_fixtures.py` | yes | yes | `a36edc1` + repair | rides this branch push | same | 33,266 B, non-box |
| `.gitignore` | yes | yes | `a36edc1` | rides this branch push | same | 10,346 B, non-box |
| `research_outputs/oracle/station_canon.json` | yes | yes | `a36edc1` + repair | rides this branch push | tracked exception, BR-2 F-R2-1 | 8,458 B, non-box |
| `exchange/queue/2026-08-16_BR1_brief_redesign_ARGUS.md` | yes | yes | publish | yes | publish guard, `exchange/**` scope | 6,557 B → 0.041% |
| `exchange/queue/2026-08-16_BR2_oracle_calibration_parity_R2_ARGUS.md` | yes | yes | publish | yes | same | 1,895 B → 0.012% |
| `exchange/reports/BUILD_2026-08-16_ORACLE_REBIRTH.md` | yes | yes | publish | yes | same | this file |
| `exchange/status/LEDGER_ARGUS.md` | yes | yes | publish | yes | same, append-only | +~1.1 KB |
| `briefs/oracle/oracle_2026-08-16.html` | yes | **no — gitignored** | — | — | residency block, F-BR-9 | 231,955 B, OFF-BUS |
| `research_outputs/oracle/tape/oracle_tape_2026-08-16.parquet` | yes | **no — gitignored** | — | — | same | 15,288 B, OFF-BUS |
| `research_outputs/oracle/calibration/oracle_calibration_2026-08-16_full.json` | yes | **no — gitignored** | — | — | same | 6,088 B, OFF-BUS |
| `research_outputs/oracle/calibration/selfcheck_log.jsonl` | yes | **no — gitignored** | — | — | same, append-only | 775 B, OFF-BUS |
| `research_outputs/oracle/payloads/*.json` (10) | yes | **no — gitignored** | — | — | same | 184 KB total, OFF-BUS |
| `~/Library/LaunchAgents/com.naiad.oracle-0700.plist` | yes | **no — outside the repo** | — | — | CADENCE registry + §3.2 undo | 998 B, non-box |
| `~/Library/LaunchAgents/com.naiad.oracle-1600.plist` | yes | **no — outside the repo** | — | — | same | 1,002 B, non-box |

### 7.1 BOX-COST

This build adds roughly **8.5 KB to the bus at 16,000,000 B** — the two queue items, this
document and the ledger append. Everything with volume stayed off: 230,672 B of render,
184 KB of payloads, 15,288 B of tape and 6,088 B of calibration are all gitignored and reachable
only by the paths above. Nothing this build produced is over the 64,000 B naming wire.

**Intended homes, per §3.2.** The renders and payloads are regenerable in ~3 s from the kline
cache and are deliberately not durable: `briefs/oracle/`. The tape and the calibration log ARE
the record and grow daily — they live under `research_outputs/oracle/` and are the natural first
candidates for the D: residency contract when volume justifies one. `station_canon.json` is the
sole tracked Oracle artifact and is tracked on purpose: BR-2 F-R2-1 requires the R2 JS surface
and Python to read the same file at the same sha.

### 7.2 Concurrency disclosure

Other sessions write to this repo. `publish()` stages all of `exchange/` by design, so anything
they left there rides this publish. The hand commit `a36edc1` lists explicit paths only. Also
noted, unchanged: `exchange/.DS_Store` is tracked and rides every publish — a standing
reported-not-fixed finding, not touched here.

---

## 8 · WHAT THIS BUILD IS NOT

Not R2 or R3 alerting — C-9 ships R1 only, and BR-2 holds R2 behind its parity gate. Not census
work: not one outcome is scored anywhere, and F-BR-3 and F-BR-10 assert it by scanning code and
keys rather than prose. No new indicators, no sizing, no Pine changes. No threshold
self-adopted. Not a resurrection of the 3×/day capture era — two slots, exactly as C-1 names.

---

## 9 · POST-BUILD ADVERSARIAL REVIEW — WHAT IT BROKE, AND THE REPAIRS

After this document was first published at commit `1112f11`, the build was put through an
independent adversarial review (four attackers, twenty judged findings). It found real defects
in work this document had already presented as acceptance evidence. They are recorded here
rather than quietly patched, because the first version of section 2 asserted a sentence that
was **false**.

**C-1 · THE FALSE SENTENCE. [was blocking]** F-BR-3 printed, and this document published,
*"no journal / forward_log / positions module is reachable from either module."* That was
untrue. `engine/s1.py` does `from engine.journal import iso`, so `engine.journal` has been in
the closure from the first run. The fixture never caught it because its matcher tested
`x == m or x.startswith(m + ".")` against the bare token `journal`, which cannot match
`engine.journal` — **the ban was dead code that could never fire.** REPAIRED: the matcher is
now component-wise (a banned token is banned at any dotted position); `engine.journal` and
`engine.trading` are named as DISCLOSED inherited imports with the single symbol each
contributes; and the fixture now asserts the thing section 2 actually forbids — that no
journal READ is called and no oracle source imports either module directly. The break leg
plants a journal read.

**C-2 · F-BR-1 TESTED NO STATION WORD, AND WAS NOT INDEPENDENT. [was blocking]** The fixture
compared six boolean cross series and never formed a posture word, so D-1's central output —
the entire four-word map — shipped with zero fixture coverage; gutting `stations_for()` left it
green. Worse, its "independent second implementation" called `engine.indicators`, the same
module object the engine under test uses, so monkeypatching `ind.ema` to a Pine-incompatible
variant also left it green. REPAIRED: F-BR-1 now runs a genuinely independent state machine
with its own EMA, ATR and crossover recursions (no `engine.indicators`, no `station_engine`)
and compares **station words** at four as-of points per symbol — 28 comparisons, all matching.
Three symbols are skipped for want of warm-up history and are now named in the transcript
rather than silently dropped.

**C-3 · THE TRAP CARD PRICED THE WRONG BAR. [was major]** `trap_card` set `entry = st.close`
while printing "IF: at the close of the first in-window 4h 12/26 cross" — the code contradicted
its own rule in the same dict, and the rule card is explicit ("enter at that bar close"). On the
shipped NEARUSDT card the drift was **10.12 ATR** (1.635 printed against a trigger-bar close of
1.911, 147 bars stale), and risk, target and net R:R all inherited it. REPAIRED: a TRIGGERED
window is priced at the close of its trigger bar; an ARMED window has not fired, so its card is
marked PROVISIONAL and says the last close is standing in for a price the market has not printed.

**C-4 · TRIGGERED HAD NO AGE. [was major]** The rule card gives TRIGGERED no staleness term, so
a 24.5-day-old 12/26 cross read TRIGGERED on the Board exactly like one from this morning. The
word is the card's and has not been changed; what was added is `TRIGGER_FRESH_BARS` [VETO] = 6
(24h on the lens), the trigger's age in bars on the Board reason and on the card, and a STALE
TRIGGER chip. D-7 now logs the trigger-age distribution so BR-2 can rule the threshold.

**C-5 · THREE FIXTURES COULD PASS VACUOUSLY. [was major/minor]** F-BR-2 accepted the bare WORD
"toll" and failed OPEN if its row regex matched nothing — repaired to fail closed, reconcile the
row count against the card count, and re-derive every ratio's toll as a NUMBER. F-BR-4 passed on
a render with the entire paint routine deleted — it now also asserts `divRGB`/`heatCanvas`/
`putImageData`/`paintStrips` and the DOMContentLoaded hook are present. F-BR-10's token matcher
let plurals through (`n_wins`, `losses`) — now stemmed, and its break leg plants a plural.

**C-6 · MINOR.** A dead `DEAD_MEMORY_BARS` read in `windows_for`, a documented `closed_by`
value (`series-end`) that was never assigned, and `stations_for` silently accepting a negative
`as_of_i` (Python's wrap-around applied to the scalar stamps but not to the arming range or the
ages, giving a wrong board). All three repaired; `as_of_i` now raises with the reason.

**WHAT THE REVIEW CONFIRMED CORRECT**, by independent recompute rather than by reading: the
alive/dead window determination (11,398 window-observations, 0 mismatches, 0 trigger leaks);
`age_bars` with no off-by-one; the half-open trigger boundary agreeing with `tierc2_baseline`;
non-admitted windows correctly excluded from both collapse lists; and — the thing no one had
checked — **the page really paints**. Run under JavaScriptCore with a DOM shim, all ten canvases
receive their image; a Python re-implementation reproduces the engine's pixels byte-identically;
and the colour law, the 0.45 knot dimming and the null-is-absent rule are **byte-identical to
the shipped VIZ-4 original** on all ten payloads, verified by decompressing the original bundle
and running both side by side. Row order, aspect (a uniform 10x) and script ordering all check out.

Ten findings were judged real and are addressed above or disclosed; ten were refuted on
inspection.

— HEPHAESTUS, 2026-08-16. Reviewed against BR-1 as amended by A1, then re-reviewed
adversarially and repaired. Section 9 is the correction record.
