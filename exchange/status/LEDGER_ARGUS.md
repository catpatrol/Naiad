# LEDGER_ARGUS — append-only lane ledger

**Lane:** ARGUS — daily market brief · Atlas HTML report · live laboratory · analytics scoping.
**Adopted:** 2026-08-02, ruling Q-3 A (`FUNNEL_DIONYSUS_W1`). Append-only. Never edit a past entry; a
correction is a NEW entry that names what it supersedes. The central `LEDGER.md` remains the
*evidence* ledger and is untouched by this file — this one carries coordination state only.

**Entry template (naiad-eod format):**

```
=== STATUS_<LANE> — <date> ===
NOW: <2-3 sentences>
LAST EVENT: <date> — <one line>
FACTS: <up to 6 lines, each ending with [verified/ledger/ratified/handoff/unconfirmed-live/open]>
PENDING: <numbered items waiting on the operator>
NEXT: <single next action + owner>
METRICS: operator actions this session = <n> · files re-ingested = <n>
=== END STATUS ===
```

---

=== STATUS_ARGUS — 2026-07-27 ===
NOW: Brief v1.1 build PASS at commit 76cc314, reviewer acceptance PENDING. Amendment 1 was ratified before the build (Setup Radar state machine, Points of Interest, 18-flag confluence dictionary, archive + firewall clause 4: archive = hypothesis mine, never a scoring window). Fixtures F-B1..F-B8 came in 8/8 on the live 10-asset day AND 8/8 on the frozen fixture day.
LAST EVENT: 2026-07-27 — build PASS entry + hygiene commit 60e00c9: .gitignore rules for the brief archive, manifest SOURCES extended to the two new scripts, box copies written and sha-asserted.
FACTS:
- Radar day 1: ENTERED 15 · DORMANT 6 · ARMED 5 · POST_X 4; POI 27 fired / 12 shown / 15 dropped, drop count printed [ledger]
- Two HALTs resolved by operator ruling: POST_X precedence (an X's authority ends at the NEXT arming) · fixture substrate FENCED and sha-pinned, charter §10 beats contract F-B3 [ratified]
- 5 builder defects caught pre-adoption by inspecting real output (zone-distance basis, staleness-from-open, current-day naked POC, POI cap hogging, `contracts` renamed governed_by) [ledger]
- Firewall posture: no journal read OR written — compute_signals called directly, trading layer never imported, F-B5 proves it [verified]
- Grade caveat: NOT comparable across the three lens columns (1h lens runs align=governor per TC-5 Amendment 1 — A-grade tautology); footnote due in Amendment 2 [open]
- Sample day pinned: brief_2026-07-27.json 249,983 B sha 78f264d4… matches the reviewer-box copy exactly; html 144,479 B; runtime 312 s [verified]
PENDING:
1. Reviewer acceptance of v1.1: independent recompute from brief_2026-07-27.json — no partial adoption
2. Draft Amendment 2 from the four logged spec errors (ENTERED semantics · zone-occupancy unmask · POI cap shape · grade footnote)
3. Named G-7 candidate handed to SYSTEM: are post-X re-arms empirically weaker? (exploration-classic only)
4. v1.2 economy: skip top-up when cache is already at the latest closed bar (132 s of 312 s); thresholds re-ratified after ~1 week
5. /brief registers after a session restart (diagnosed; not a defect)
NEXT: Independent recompute in the BRIEF lane → acceptance → Amendment 2. Owner: ARGUS.
METRICS: operator actions this session = not recorded (predates Q-8) · files re-ingested = not recorded
=== END STATUS ===

**Provenance note (HEPHAESTUS, 2026-08-02):** this seed entry is a synthesis of the lane's standing
status document, carried over unmodified in substance at ledger adoption. Source document:
`docs/history/STATUS — BRIEF (daily market brief · Atlas HTML report · live laboratory).txt`
(3,008 B, updated 2026-07-27 late) — it sat at repo root when this ledger was seeded and was **moved
to `docs/history/` later the same day** by the repo filing pass; the pointer is updated here so it
does not rot. It is dated 2026-07-27; `prompts/CONTRACT_ARGUS_Analytics_Scoping_2026-07-29.md`
post-dates it and is not reflected here. **Treat as stale until ARGUS appends a current entry.** [handoff]

## 2026-08-11 — ARGUS acknowledges NOTE_ATHENA_to_ARGUS_2026-08-11_DATA-RESIDENCY
- DATA RESIDENCY ADOPTED for every ARGUS contract from this date: bulk outputs written DIRECTLY to D:/Naiad/<repo-mirror-path> at creation, every D:-path contract carrying a reachability gate that HALTS if D: is absent (never a silent laptop fallback), a disposition table with a BOX COST column, and any artifact over ~1% of the 6.39 MB box flagged at creation with its intended home stated. Existing pipelines keep their written paths: the daily brief continues writing briefs/ locally per §1.3.
- CENSUS CANDIDATES drafted under the rule from the first line. H-VBT is the first big-data programme born under it — its substrate joins excursion episodes to census outcomes and is data-class by construction. Routing priority unchanged and reaffirmed: H-VBT first (it aims at the study's PRIORITY #3 harvest problem, still unsolved — 73.67% of trades reaching +1R round-trip into loss, and the winning book wins by riding to regime break rather than by managing winners), then CENSUS-1d Phase 0 (the free Tier-A proxy: census_outcomes.jsonl carries event_price and p0 on all 149,802 rows, so price-space clustering needs no new walk), then H-VDP.
- POINTER DISCIPLINE acknowledged and already felt by this lane: captures, renders and results JSONs never enter exchange/ — path + sha256 pointer only (CONVENTIONS §4.2). The 2026-08-06 hygiene sweep moved 44 ARGUS artifacts (4,795,123 B) to docs/history/argus/, sha-verified both directions on 44 of 44, taking exchange/reports/ from 87 files / 5,624,631 B to 43 files / 829,508 B — an 85.3% reduction of which 84% was two capture JSONs alone. DOCUMENTS ARE CHEAP, DATA IS NOT.
- LEDGER STALENESS OWNED: this lane filed eleven reports in 48 hours while the ledger sat nine days silent. The bus carried everything and the index carried nothing, which is exactly backwards. Acknowledged, not explained away.
- ⚠ RAISED TO ATHENA — ROTATION CONFLICT. Queue 003 rotates bus reports older than 30 days to docs/history/reports/YYYY-MM/, exempting only NOTE_*_to_* files. INTERFACE_<date>_C6.md is neither a note nor a report: it is the LIVING CENSUS-FACING CONTRACT APOLLO cites, and it is the only copy a web lane can reach, since the canonical analytics/INTERFACE.md sits under analytics/ and the standing rule is that anything a web lane must read belongs under exchange/ or docs/. Under rotation it leaves the surface APOLLO reads on 2026-09-05. ARGUS PROPOSES: relocate it to exchange/status/, which does not rotate and already holds LEDGER_ARGUS.md, so the lane's two permanent artifacts sit together. FALLBACK: drop the date from the filename and exempt undated files from rotation. ATHENA rules.
- RESIDENCY REFINEMENT PROPOSED, not urgent: briefs/panel/{snapshots,levels,areas,excursions}/*.parquet are 100% REGENERABLE from the captures via brief_panel.py — derived data occupying tracked space to no durable end. Captures are the record and must stay tracked; the partitions are the free candidate for D: when archive volume makes it worth a contract. Recorded now so it is not rediscovered later.
- LANE STATE UNCHANGED: analytics 1.5.0, sha ea5f02f2…, suite 286 passed / 1 skipped. Certified against the operator's charts: oscillators + ATR (72/72), resample_ohlcv (40/40), rolling VWAP both substrates (14/14 and 28/28), anchored VWAP including sigma (42/42), band geometry (54 triples). volume_profile / LVN / va_nesting remain FIXTURE-VERIFIED and NOT chart-certified BY DESIGN — comparing our kline approximation against TradingView's different approximation certifies nothing whichever way it comes out. Scope travels with every number: BINANCE perpetuals, 1h substrate, hlc3 source.
- ARGUS, 2026-08-11.

=== STATUS_ARGUS — 2026-08-16 ===
NOW: Lane re-primed and re-scoped. Render audit filed; BRIEF_REDESIGN_SPEC_v1 drafted to the
     queue awaiting the RATIFIED stamp. Rulings D1c D2a D3 D4(event/ATR) D5c taken.
LAST EVENT: 2026-08-16 — BR-1 drafted; audit note filed; this append.
FACTS:
- VIZ-4 render shas 4/4 match BUILD_2026-08-15_VIZ4_MANTLE §2 [verified]
- VIZ3_Gallery_dc.html is the VIZ-4 M3 gallery misnamed; rename proposed [verified]
- Brief job retired 2026-08-05 per ruling 4a; BR-1 is a rebirth not a facelift [ledger]
- VIZ-3 payload shas printed, emitter cross-check owed [handoff]
- Primer two-artifact rule superseded by single-build-document; CONVENTIONS wins [ratified-lean, flagged]
PENDING: 1. Operator RATIFIED stamp on queue BR-1  2. 16:00 refresh-hour veto  3. Charter
amendment to ATHENA  4. VIZ-3 sha cross-check + verdict-language sweep
NEXT: On the stamp — HEPHAESTUS executes BR-1. Owner: operator.
METRICS: operator actions this session = 2 · files re-ingested = 10
=== END STATUS ===

=== STATUS_ARGUS — 2026-08-16 (ORACLE REBIRTH) ===
NOW: BR-1 stamped + built + armed. THE ORACLE lives: 07:00 full / 16:00 refresh, tape
     + calibration self-instrumenting. BR-2 filed pre-ratified behind gates G-BR2-1..3.
LAST EVENT: 2026-08-16 — BR-1 executed; BR-2 filed; agents armed.
FACTS:
- Fixtures F-BR-1..F-BR-10: 10/10 GREEN, each shown FAILING on a deliberate break first;
  F-CONV 4/4 still green. Transcripts in BUILD_2026-08-16_ORACLE_REBIRTH §2 [verified]
- Agents armed, schedules read back FROM launchd: com.naiad.oracle-0700 {Hour 7, Minute 0}
  and com.naiad.oracle-1600 {Hour 16, Minute 0}; one unattended run exit code 0 in 5.6 s,
  three self-checks PASS [verified]
- First render briefs/oracle/oracle_2026-08-16.html 230,672 B
  sha256 8e1fb36612f27d79a80a07a334d439e16150c45cd0fb1a6a2685e2a43ae32e2c; station_canon.json
  7,813 B sha256 73331bed77484f2f0337907bb0f0827b804070caaeed849784bf203dfb5fe693 [verified]
- A1-1 RECORDED AND BINDING: the daily organ is THE ORACLE; the census-2B artifact is always
  ORACLE GRID, fully qualified; all deliverables are oracle_* [ratified]
- V-1/V-2 REPORTED NOT FIXED: "station canon v1" names TWO things one day apart, and no
  per-word definition of STALKING/ARMED/TRIGGERED/DEAD exists anywhere in the estate. Gates
  taken from the ratified TC3 card; only the naming map is new, and its 8 unruled rows are
  [VETO], printed in the render and logged every run [handoff]
- V-3 Pine SS v12.1 is NOT in the repo; F-BR-1 discharges parity against SS_v12_0_1.pine
  (10/10 symbols, 6 marker series, mismatch list empty) and prints the v12.1 handoff [verified]
PENDING: 1. seven live mornings  2. operator mid-week PARITY line  3. BR-2 on gates
NEXT: live week runs unattended. Owner: launchd, then operator (parity glance).
=== END STATUS ===

=== STATUS_ARGUS — 2026-08-16 (ORACLE REBIRTH · CORRECTION) ===
NOW: Post-build adversarial review run against the shipped ORACLE. It found real defects in
     work the build document had already published as acceptance evidence. Repaired at
     802b3cb; BUILD_2026-08-16_ORACLE_REBIRTH section 9 is the correction record.
LAST EVENT: 2026-08-16 — adversarial review; six repairs; fixtures re-run 10/10; second
     unattended run exit 0.
FACTS:
- CORRECTION, published claim was FALSE: F-BR-3 printed "no journal ... module is reachable"
  as acceptance evidence. engine/s1.py does `from engine.journal import iso`, so engine.journal
  was always in the closure; the ban was dead code (bare token vs dotted module). Matcher now
  component-wise; both inherited imports DISCLOSED; the fixture now asserts no journal READ,
  which is what BR-1 section 2 actually forbids [verified]
- F-BR-1 tested no station word and called engine.indicators — the module under test — so it
  was blind twice over. Rebuilt: an independent state machine with its own EMA/ATR/cross,
  compared on WORDS, 28 comparisons, 0 mismatches, 3 skipped symbols named [verified]
- Trap Card priced today's close while printing "at the close of the 12/26 cross": 10.12 ATR
  drift on the shipped NEAR card. TRIGGERED now prices the trigger bar; ARMED is PROVISIONAL
  [verified]
- TRIGGER_FRESH_BARS [VETO] added: a 24.5-day-old trigger read like this morning's. Age and a
  STALE chip print; the word is unchanged because the card rules the word [ratified-lean]
- CONFIRMED CORRECT by independent recompute: alive/dead over 11,398 window-observations, 0
  mismatches; and the strip PAINTS — all 10 canvases render under JavaScriptCore, colour law
  and 0.45 knot dimming byte-identical to the shipped VIZ-4 original [verified]
PENDING: 1. seven live mornings  2. operator mid-week PARITY line  3. BR-2 on gates
     4. the nine [VETO] rows, now including TRIGGER_FRESH_BARS
NEXT: live week runs unattended. Owner: launchd, then operator (parity glance).
=== END STATUS ===

=== STATUS_ARGUS — 2026-08-16 (ORACLE TOP-UP · BR-1b) ===
NOW: V-8 closed. The kline estate is no longer stale and nothing about the Oracle changed to
     make it so. Two more slots armed at 06:45 and 15:45 BA, 15 minutes ahead of each Oracle
     slot; the Oracle stays cache-only and the fetching lives in its own organ.
LAST EVENT: 2026-08-16 — BR-1b filed, built, armed; F-TU-1..6 6/6; unattended run exit 0.
FACTS:
- SCOPE ENUMERATED, NOT ASSERTED: 10 symbols x {5m,15m,1h,4h} = 40 pairs, obtained by
  instrumenting oracle_daily.load_lens on a real run and pinned with that file's sha256.
  The top-up HALTS if oracle_daily.py changes. 30m is absent on purpose (resampled from
  15m); 1m and 12h are absent because the Oracle never reads them [verified]
- First real run +2,521 rows across 40 pairs, 0 gaps, 0 clobbers, 1m49s — inside the 15
  minute head start. Unattended run +10 rows, exit 0 [verified]
- THE CHAIN WORKS: the Oracle's as-of advanced 2026-08-15T12:00Z -> 2026-08-16T00:00Z with
  oracle_daily.py byte-identical, and the BR-1 fixtures stayed 10/10 green [verified]
- Fixtures F-TU-1..6 6/6, each shown failing on a deliberate break first. Two were RED at
  first and both times the FIXTURE was wrong, not the code — recorded in the build doc [verified]
- topup_log.jsonl carries fixture rows tagged slot="fixture-F-TU-6"; anything reading that
  log, BR-2 included, must filter them as last_real_run() does [handoff]
- T-3 OPEN: launchd runs a missed calendar job on wake, so a laptop asleep at 06:45 may fetch
  after the 07:00 Oracle has rendered. No staleness alarm exists; a ruling is available [open]
PENDING: 1. seven live mornings  2. operator mid-week PARITY line  3. BR-2 on gates
     4. the [VETO] rows, now including OVERLAP_BARS  5. the T-3 staleness-alarm ruling
NEXT: live week runs unattended, now on fresh data. Owner: launchd, then operator.
=== END STATUS ===
