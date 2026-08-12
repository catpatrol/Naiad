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
