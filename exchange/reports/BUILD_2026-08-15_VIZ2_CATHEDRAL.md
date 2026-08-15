# BUILD — VIZ-2 · CATHEDRAL PAYLOADS

**2026-08-15** · branch `v12-v1-census` · seed 20260814 · **DISPLAY-ONLY / Tier-E exploration · m = 0** · no registrations. Appended to the ORACLE run's close.

`scripts/census2b_viz2.py`. Payloads live local at **`research_outputs/census2b/viz_payloads/`**, copied with the governing contracts into **`research_outputs/census2b/DESIGN_HANDOFF_VIZ3/`** (7 files). `write_payload` is **imported** from `scripts/census2a_viz.py`, so the meta block has one implementation across both viz stages; only the output directory is re-pointed.

| payload | meta.rows | bytes | sha256 |
|---|---:|---:|---|
`v3_may26_tape.json` | 276 | 17,973 | `8435dfbf0f937965…`
`v3_stations.json` | 12 | 25,605 | `bc86c2bb8464ae2e…`
`v3_terrain.json` | 47,852 | 246,310 | `03c38a8cd73150b8…`
`v3_helix.json` | 91,375 | 591,035 | `6ebccf7e263f4963…`
| **total** | | **880,923** | all ≤ the 700 KB cap |

**F-V3 — PASS.** (a) all four round-trip `json.load` and re-hash to their own `meta.sha256`, all under cap. (b) the May-26 timestamps reconcile to the D-CEN2c row — `MC1_results.json` `D3.event_card`, the ops record for May-26: trigger `ts_ms`, `ts_iso`, `close` and `atr_4h` all match exactly, and the four legs match the anatomy printed in `BUILD_APOLLO_2026-08-06_MC1.md`.

## §3 · THE FOUR PAYLOADS  *(payload · schema essentials · the money question)*

**T1 THE MAY-26 TAPE** — `v3_may26_tape.json`: `{stages[], bell, stamps_display_only, spine_4h[]}`. Per stage {ts_ms, ts_iso, px, atr_4h, e9/e12/e25/e89/e200, displacement_atr, hours_from_arming}; 271 4h bars of spine. The anatomy, from the pinned dossier:

```
  arming   2026-05-16T00:00:00Z @ 79,041.7   disp 0.8561 ATR   (= bell)
  relay    2026-05-18T04:00:00Z @ 77,039.4   +52h
  trigger  2026-05-26T16:00:00Z @ 76,028.3   +256h   <- the archetype
  seal     2026-05-27T20:00:00Z @ 74,418.1   +284h   (28h AFTER the decision)
  terrain  2026-06-03T00:00:00Z @ 65,818.4   +432h
  stamps   2/4 — FIRST True · TRAP True · WALL False · SEAL False
```

*Q: the archetype scores 2/4 on the family built to describe it — so what is a 4/4 actually a picture of?*

**T2 THE TWELVE STATIONS** — `v3_stations.json`: `{six_rules, iron_rules, stations[12], provenance_tags}`. Per station {station, class, lifecycle_stage, stage_title, gate_text_verbatim, evidence_class, veto_pins[], n_total, per_lens[]}. Gate text is quoted verbatim, never paraphrased. *Q: which stations are load-bearing and which are only well-lit — i.e. where does evidence class diverge from event count?*

**T3 THE TERRAIN** — `v3_terrain.json`: **columnar**, `{asset_legend, n_records, columns, rank, asset, mfe, terminal, give_back, hold, is_winner}` — **all 6,834 campaigns, no truncation**, sorted by MFE descending. 837 winners (12.2%). *Q: does give-back scale with MFE, or is the tail handing back a constant?*

**T4 THE HELIX** — `v3_helix.json`: **columnar**, BTCUSDT 1h, 60,737 bars 2019-09→2026-08. `{spine{i,w[6]}, state_changes{i,sr,to_state}, transitions{kind,sr,from_i,to_i,bars,dir,open}}`; time axis is a bar index (`ts = t0_ms + i*step_ms`, exact — the series is gap-free, asserted at build). **13,379 state changes and 6,233 transitions, complete**; the spine alone is decimated to every 8h (7,593 points). *Q: do the six sub-ribbons change state together, or does the fast ribbon lead the slow one by a countable lag?*

**Columnar is why T3 and T4 fit.** Object-per-row JSON repeats every key once per record and put the helix at 1.33 MB and the terrain at 812 KB — both over cap, and the terrain would have had to drop 977 campaigns. Column arrays cost nothing in fidelity and both now fit **with every row kept**. Read `n_records`, not `meta.rows`: for a columnar payload `meta.rows` counts array cells.

## §4 · FINDINGS — NOT FIXED

**V-1 · `DESIGN_CONTRACT_VIZ3` does not exist, and never has.** Verified against the working tree and against every blob reachable from every commit on every branch: zero hits for `DESIGN_CONTRACT`, `VIZ3`, `VIZ-3`, `VIZ-2`, `cathedral`, `station card`, `helix`. There is no §3 of it to honour. What governs is a pair: **`DESIGN_BRIEF_CENSUS2A_VIZ_2026-08-12.md`** — whose §3 *is* the payload-spec template (name · payload · schema essentials · money question), the form §3 above follows — and **`BUILD_2026-08-12_CENSUS2A_VIZ1.md`**, which is where the real meta block lives. Both are copied into the handoff. **Ruling needed: name this stage and write its contract, or ratify this document as it.**

**V-2 · No canonical TWELVE exists.** Nothing in the estate names twelve stations, twelve gates, or twelve checks. The estate's own use of the word is `BUILD_2026-08-14 §9 · STATION OCCUPANCY — the six-stage kit, photographed`, and that is **six**. The twelve emitted here are the **twelve ORACLE classes** (`BUILD_2026-08-15_CENSUS2B_ORACLE.md` §4) — the only twelve-item structure the estate has, and this lane's own immediately preceding build. The class→stage mapping is **this pass's reading**, flagged on the payload; the gate text it selects is verbatim, the selection is not.

**V-3 · Two records are 'the six-rules record', so both are carried.** Exactly six numbered rules exist twice: the trade-lifetime **six-stage kit** S1–S6 (the six-rules record, §2) and **IRON RULES** IR1–IR6 (`DESIGN_BRIEF` §2, the display gates). Rather than guess, `v3_stations` carries **both verbatim**. Stations quote the lifecycle gate, because a station is an instant in a trade's life; switching the reference needs no re-run.

**V-4 · Stages S4 and S5 carry no station.** Coverage is S1×6, S2×3, S3×2, S6×1. S4 (agile entry) and S5 (management) are post-entry disciplines and the twelve ORACLE classes are all *events*, so nothing crosses to them. Their gate text is still emitted in full under `six_rules` — **the record is complete even where the mapping is empty.** Forcing a class into an empty stage would have been invention.

**V-5 · `bell` is not a distinct object.** The word occurs exactly once in the estate, and it names the arming: *"the arming — the attention bell, window-opener [verified object]"*. It is emitted as a **role alias** of `arming`, not as a fifth event. The fifth cross family the dossier does carry — 300×450, the terrain class — is emitted under its own name rather than conscripted into the gap.

**V-6 · `fuzz` has no anchor in the estate — zero hits repo-wide.** `veto_pins` is emitted per station, naming the constants each one leans on (pins, not truths). Whatever *fuzz* was to do to those names is not a thing this record can define. **Ruling needed, or drop the word.**

**V-7 · The terrain is slightly survivorship-tilted, and the shape it drops is the stop-out.** 260 resolved WF1 campaigns have no cen5 row and are therefore absent — **257 of them exit on `stop`, all intraday**. They are dropped upstream by cen5's own construction, not here. Named, not corrected: fixing it means rebuilding cen5, which this pass does not touch.

**V-8 · 542 null MFEs were zeros, not gaps.** `cen5_campaigns.mfe_R` is null on 542 rows where the WF1 row reads exactly `0.0` — verified on all 542. Emitted as `0.0`, because left null they sort to an arbitrary end of an MFE ordering and vanish silently. Related: `is_winner` is `outcome_sign == 'win'`, which is exactly `sign(ride_R) > 0` (agreement 1.000); reading it off the size-scaled `realized_r` instead would flip **38 of 6,834**, so the ruler is stated rather than assumed.

**V-9 · The two transition tables mark an open episode differently.** `*_knots` writes `exit_bar_index = -1`; `*_fans` writes `end_bar_index = n_bars`, one past the last index. Both normalised here to `to_i = null, open = 1` (7 episodes). Neither table was changed.

**V-10 · The attached `DESIGN_CONTRACT_VIZ3_TRADE_CATHEDRAL_2026-08-15.md` did not arrive.** The 2026-08-15 box ruling instructed that it be filed to `exchange/reports/` with its sha printed and a copy placed in `DESIGN_HANDOFF_VIZ3/`. **No such file is present anywhere on this machine** — searched `~/Downloads`, `~/Desktop`, `~/Documents`, `/tmp` and the whole repo, by name and by the tokens `VIZ3`, `CATHEDRAL` and `DESIGN_CONTRACT`. The one prior attachment this lane received (`SS_v12_0_1.pine`) was found in `~/Downloads` by exactly this method, so the method is known to work. **Nothing was filed and nothing was reconstructed** — writing the contract from the recon's description of what it *should* say would produce a document that looks ratified and is not, which is the failure mode Iron Rule 1 exists to prevent. **The item stands open: re-attach and it files in one pass.** Note that V-1 above is therefore unchanged — as of this document, `DESIGN_CONTRACT_VIZ3` still does not exist in the estate.

## §5 · DISPOSITION + BOX-COST

| item | disposition |
|---|---|
| four payloads | **emitted**, all ≤ cap, F-V3 PASS |
| DESIGN_HANDOFF_VIZ3 | **7 files** — the four payloads + both governing contracts + the ORACLE build |
| registrations | **none**, as classed; m = 0 |
| payload bytes | **local only** — `research_outputs/`, nothing on the bus |

### BOX-COST — and the ruling that changed it

**This section records both halves of what happened, in order.**

**Before the ruling.** `exchange/**` measured **2,550,554 B = 39.91%** of the then-6,390,000 B box. The REFUSE line was 2,556,000 B, leaving **5,446 B** — and this document plus its two ledger appends did not fit. The publish was attempted honestly and **REFUSED**: *"exchange/ holds 2,566,419 B, 40.2% of the 6,390,000 B project box — above the 40% ceiling… index reset, nothing committed, nothing pushed."* The guard worked exactly as designed. Nothing was force-published; `allow_oversize` exists, and using it without the operator's word would have been this lane overriding a ratified guard on its own authority.

**The ruling.** Operator, 2026-08-15, `["box", VETO]`: **`BOX_BYTES` 6.39 MB → 16 MB, warn 25% → 50%, refuse 40% → 80%.** The 30-day rotation (queue 003, next ~2026-08-28) **remains scheduled** — the ceiling rises, the housekeeping stays, and `AGE_DAYS` was not touched.

**After the ruling.** `exchange/**` is **2,566,419 B = 16.04%** of the 16,000,000 B box — level **OK**, below the new 50% warn line. Boundary semantics are preserved: exactly 80.0% warns, it does not refuse.

**Two dependents were carrying private copies of the constant, and one had already gone stale.** `scripts/rotate_reports.py` imports `publish_exchange.BOX_BYTES` live and needed no change. `scripts/census2b_report.py` held a hand-kept copy (`BOX_BYTES = 6_390_000  # publish_exchange.BOX_BYTES`) which the raise would have made wrong by 2.5× on every occupancy figure it prints — **now imported, one definition in one place.** `scripts/census2b_oracle_report.py` is deliberately **left pinned at 6,390,000**: it regenerates a *filed* document whose BOX-COST records the box as it stood at filing, and importing the live constant would silently rewrite a historical record with a ceiling that did not exist when it was written. Full suite green (214 tests) after all three.

**All four payloads and the handoff were built and verified on disk throughout** — they are local artifacts under `research_outputs/` and were never bus-bound. The refusal delayed the paperwork, never the work.

## §6 · LEDGER + PROBE LINE

Per the standing close, this document ends by appending the session's STATUS entry to `exchange/status/LEDGER_APOLLO.md` and one m = 0 line to `exchange/reports/CENSUS2A_PROBE_LEDGER.md`, in this session. Spine only:

```
=== STATUS_APOLLO — 2026-08-15b ===
NOW: VIZ-2 CATHEDRAL PAYLOADS EMITTED — four payloads, F-V3 PASS, m = 0, all local.
CLASS: DISPLAY-ONLY / Tier-E. NO REGISTRATIONS.
FACTS: [9 — DESIGN_CONTRACT_VIZ3 does not exist and never has · no canonical twelve, the
       ORACLE classes stand in, flagged · both six-rules records carried verbatim · S4/S5
       carry no station · `bell` is a role alias, not an invented event · `fuzz` has no
       anchor · columnar encoding kept every row instead of truncating · the terrain drops
       257 intraday stop-outs upstream · 542 null MFEs were zeros]
PENDING: [name and write this stage's contract · rule on the twelve · rule on `fuzz` ·
         THE BUS IS AT THE REFUSE LINE and needs a rotation, a raise, or an override]
NEXT: the operator reads §4 V-1/V-2 and §5 BOX-COST. Owner: operator.
=== END STATUS ===
```

---

*End of build document. DISPLAY-ONLY / Tier-E exploration. No registrations. m = 0 — four complete extractions of fixed populations, nothing ranked or promoted. The payloads are hypothesis material for a design lane; the MC-1 lockbox header rides with the May-26 stamps.*
