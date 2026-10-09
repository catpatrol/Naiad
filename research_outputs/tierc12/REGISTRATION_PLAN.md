# TIER-C12 · REGISTRATION PLAN — the design document the filing is cut from

Stage TC12-REG (LEANS L-X.16 … L-X.22). `scripts/tierc12_registrations.py --file` reads THIS document, the pinned
prefix of the contract and the frozen readings, and writes the write-once registry
`research_outputs/tierc12/registrations/REGISTRATIONS.json` with its pin `REGISTRY_PIN.json`. The filing script
types no text, no spec and no number: it slices, parses, carries and hashes. No outcome stands anywhere in this
document: no bar has been read and no book exists when it is filed.

- §0 — the slice law and the verified line map (L-X.17).
- §1 — one table row per registration and five blocks headed `1.k <id>`, each the frozen LEANS's
  `REGISTRATION SPEC · <id>` block byte for byte: every line after that heading up to the next line that begins a
  heading of level two or three (L-X.18). The filing HALTs (`PLAN==LEANS`) on any difference.
- §2 — the keys of the filing (L-X.19, L-X.20) and the law strings the filing reads from this document.

**Bound texts**, each pinned in the filing by a sha read from the file at filing: the contract by its PREFIX
(`exchange/queue/2026-10-08_TC12_APOLLO.md`; the byte count and the sha are read from `progress/STEP_Q.json`,
L-X.16); the resume paste (`exchange/queue/2026-10-09_TC12_RESUME_APOLLO.md`, filed as `resume_paste`); `LEANS.md`;
`LEANS_AMENDMENTS.md` (AM-1 on file); `ORCHESTRATOR_RULINGS.md` and `DISCLOSURES.md` (byte-frozen from the TC12-REG
commit); the review record; this plan.

## 0 · The slice law and the verified line map

**The slice law** (TC11's, unchanged). `lines` = the contract's prefix bytes decoded as UTF-8 and split on `\n`;
`text_of_record = "\n".join(lines[a − 1 : b])` — 1-indexed, inclusive, leading whitespace kept, no trailing newline;
`text_sha256 = sha256(text_of_record)`. A `BUILT:` line appended later as the contract's last line lies after the
prefix and moves no slice, no payload sha and no chain head.

**Guards.** A registration's slice must begin, after its leading whitespace, with its id and a space, and hold
`[<prior>%]`, the prior parsed from the slice and compared with the block's. A slice is filed — as a text, a context
or a family header — only if it is a row of the map below and its bytes hash to the row's sha.

**The line map** — L-X.17's table, row for row. The filing re-cuts every row from the prefix and HALTs on a sha that
differs, and HALTs (`PLAN==LEANS`) if this table is not the frozen reading's:

| object | lines | sha256 of the slice |
|---|---|---|
| header (RATIFIED, the "maker" ruling, SAIL HELD, seed) | 1-4 | `e7da6d25d78b0a1b59e41e24268c9f9b4c6fa5e55da3513d7e9a89a32a682970` |
| LAWS (families, bar, precondition law) | 5-9 | `3ce9d5f8213a39ca03843fb2c73833dc7854c01115fd92a325d9f945409525d6` |
| STEP Q | 10 | `749506fcfabefd44f6333677c7c8294511191a464d861d751676fed82acd1872` |
| RULINGS ENACTED | 12-16 | `112c0980974b71b0f21f28a5316e7a14d658a91622f2af00df2a43085e7fab67` |
| V1 source and lookback | 27-31 | `9a3a3cde19a580692578af2969fbecbe6af6ca2f3b908dba7924ac2b986da8e8` |
| V2 the state machine | 32-38 | `36b8321302c5acff8a22be1e4fa419345d7d357d06c7029d6896bf8949552bc2` |
| V3 the licence | 39-41 | `91dbee3e59bbacca550ffcc7996fed56c0c09099f0c84c811b469977074a9489` |
| V4 the traverse | 42-43 | `6d10f07b48a811958a83630d3bdbca8336511d4679835b9d4206c38fc8268b96` |
| V5 the stamps | 44-46 | `66b10dc908a7267afd65a5c5d74407e22aa3c4a354bc67755817ebf5496e421a` |
| STAGE C | 48-50 | `74af3673db2f3ed61186d23bea699ea04f00f09cdf3eaa817442d16a0b485714` |
| STAGE G header (family) | 52 | `9c75b3ec4f751ee0f64143076a3724267328452bdfd791946ae868178d6cf6b0` |
| **P-ADM-1 [50%]** | 53-56 | `b4f14e60f766ddfd7bf7847fcdccb4b069f6a32fd16816e0a27f7ceacd8281a1` |
| **P-BRD-1 [40%]** | 57-59 | `e049d8d9fb62cc5cf15e1145c696270c5bd369aeae63a5b2570a1d6d5decfd7d` |
| STAGE G Tier-E | 60-62 | `6c64124bfda63121fbde7eabbb5f3812f347b2dd6f293a961528ca1c48447cd6` |
| STAGE R header (family) | 64 | `8b1038704f484036362d644634faeba64e5543313f1af007a548b694a687a4bb` |
| **P-DIR-1 [45%]** | 65-68 | `1b4dec34d1337d49e22266006550421d8e4d88618e639a6581078c3fb0fcaf26` |
| **P-SFP-VA-1 [45%]** | 69-75 | `f6e581da8fe470b9f3fe9e414b466459ec0180af8dbcad3c57cdfcdf2d9d2754` |
| STAGE R Tier-E | 76-80 | `7a82e7ce2e6fcd4076c45a683414b79bd64b6a4d1e77148f7a5ea833d4ff632e` |
| STAGE S header (family) | 82 | `886cea7d7542363f6b47a16667efb8c1c03f15fce92829c3eb3e3ccacedd2db9` |
| **P-SCALP-3 [30%]** | 83-106 | `fa141ec5d25ab67fbe57a673b676d94152dd287f145f66621e0d23b2e1b52198` |
| STAGE L | 108-112 | `23c6297b424a32bb5204aa1ac64bb956d1f351f948482f18a30b0384a89a8036` |
| FIXTURES | 114-124 | `8499991137046a971f905bcbf0f2491c3eb859c6db987ff0ce755c8630ebc452` |
| CLOSE | 126-131 | `5f964a172c49ae509b69819a10bed8de40a7cf2c12e4793e980db395895a9737` |
| WHAT THIS IS NOT | 132-134 | `ce1c5b703a5364fc4c96f6c47e97129872313f320a6f30c7cb2c6cfba29cd64e` |
| VETOES BY NAME | 135-137 | `b1f2ee3a9f117dee14354cf90bd4f1bc1b8c63dd764a667b9e7b1276c1058235` |

**Roles, read from the table by the filing.** The text of a registration is the row whose object is
`**<id> [<prior>%]**`. A family header is a row whose object reads `STAGE <letter> header (family)`; the filing HALTs
(`FAMILY-PARSE`) unless those rows are exactly the header lines the pin door parses. The LAWS slice is the row whose
object begins `LAWS`; the line stating `bar = q ÷ m` must lie inside it.

**Filing order** (`seq`) = ascending first text line: P-ADM-1, P-BRD-1, P-DIR-1, P-SFP-VA-1, P-SCALP-3.

**Context of record.** Every registration files two contract slices: the LAWS slice and its own family header (the
minimum of L-X.17; no owner's block adds a contract slice).

**External context.** An `external_context` item `{path, sha256, lines, text}` is cut by the same law from another
pinned text, the file's sha asserted first. It is declared by the owner's block, inside the `items` of its label, in
the form ``external_context `<path>` lines <a>-<b> (sha256 `<file sha>`)``; ranges joined by `and` are one item
each. On the blocks below P-ADM-1 declares one (TC11's `stage_g/STAGE_G.md`) and P-BRD-1 declares two lines of
`x_rec/tierc11x/era/X4.md`; a copy under `x_rec/` is also held to its `X_REC_MANIFEST.json` row. The path may not be
a file TC12's own close acts move (L-0.24's sets and TC11's contract): the filing HALTs `EXTERNAL-SLICE` on one.

## 1 · The five registrations

Families, `m` and bars are the pin door's parse of the contract's three stage headers (`scripts/tierc12_pins.py`).
The filing HALTs (`PLAN-TABLE`) unless every cell of this table equals the parse and the block beneath it.

| seq | registration | family | m | bar | prior | text lines | comparison | preconditions | labels |
|---:|---|---|---:|---|---:|---|---|---|---|
| 1 | P-ADM-1 | ADMISSION | 2 | 0.05 | 50 | 53-56 | two-sample vs v6 | none | pre_seen |
| 2 | P-BRD-1 | ADMISSION | 2 | 0.05 | 40 | 57-59 | two-sample vs v6 | none | selection_hazard |
| 3 | P-DIR-1 | RANGE-STATE | 2 | 0.05 | 45 | 65-68 | two-sample vs v6 | none | selection_hazard |
| 4 | P-SFP-VA-1 | RANGE-STATE | 2 | 0.05 | 45 | 69-75 | vs zero | 2 items | pre_seen |
| 5 | P-SCALP-3 | SCALPER | 1 | 0.10 | 30 | 83-106 | vs zero | 1 item | pre_seen |

### 1.1 P-ADM-1

- **id:** P-ADM-1
- **family:** ADMISSION (the family name parsed from the header line, contract :52: "STAGE G · ADMISSION FAMILY
  (m=2, bar 0.05; both two-sample vs v6 — they remove trades):")
- **family_m:** 2 (parsed from contract :52; two registrations stand under the header, :53 and :57)
- **family_bar:** 0.05 (parsed from contract :52; asserted equal, as fractions, to q ÷ m with q = 0.10 parsed from
  contract :9: "bar = 0.10 ÷ m per family")
- **prior:** 50 (contract :53: "P-ADM-1 [50%]")
- **mechanism:** A card-v6 entry is a trend-continuation entry: it buys a pullback inside an established 4h tide.
  Two clocks say independently that such an entry is LATE. The tide clock: the tide it rides has already run long
  measured against every tide run the home panel has shown up to that bar (its age at the entry bar is in the top
  trailing quartile, the OLD band). The window clock: the pullback window that armed the entry has stood open for
  many bars before the trigger came (the arm-to-entry lag is at or above the filed cut). An entry late on either
  clock joins a move with less of its course ahead of it and with the same structural stop behind it. The claim is
  that refusing every entry that is late on at least one clock leaves a book whose per-campaign expectancy exceeds
  the whole book's. The mechanism is declared here and in the contract (:53-54) before this row's interval exists;
  the book's kept count and mean were already printed by TC11, which is what the label says.
- **population:** assets: the five home assets `tierc2_rules.UNIVERSE` (BTC, ETH, SOL, NEAR, ZEC USDT perpetuals,
  contract :18). Lens: 4h. Scored window (O-9): campaigns of card v6 whose ENTRY bar closes at or before TC11's pin,
  read from `research_outputs/tierc11/data/AS_OF_PIN.json` key `as_of_last_closed_4h_close_ms`. Era: the full
  corridor inside that window (the text names no era); the tuning and holdout slices by the entry bar's close are
  Tier-E. The forward strip (entry close after TC11's pin, through TC12's pin) is ridden and printed for every arm
  and is scored by nothing.
- **arms:**
  - `base` — the filed v6 book on the scored window: `tierc10_panel.run_cell_n(CONTROL_CARD, tierc9.V6_ROLES,
    UNIVERSE, lo, hi)` with `(lo, hi) = tierc10_panel.corridor_n(UNIVERSE, pin_close_iso=<TC11's pin>)`, on the TC12
    snapshot (L-C.2). The build HALTs unless its `TP._book_sha` equals `research_outputs/tierc11/books/build_manifest.json`
    key `book_sha.v6`, its n equals that file's `n.v6`, and its regbook `book_sha256` equals
    `research_outputs/tierc11/scores/BASE_IDENT.json` key `book_sha256["P-AGE-1"]`.
  - `scored` (the treated arm) — `base` minus the refused set, a POST-FILTER: the same Trade objects in the base's
    order, keyed (symbol, entry_ms), and no entry admitted into a slot a refusal frees (no re-ride). A base
    campaign is refused iff (i) its tide band at the ENTRY bar is OLD — the two-state tide run
    `tierc7_lab_regime.tide_streak(symbol)[1][entry_i]` (EMA periods `tierc7_rules.TIDE_FAST` and
    `tierc7_rules.TIDE_SLOW`; the flip bar counts as bar 1) is `>=` the top edge of
    `tierc9._trailing_edges(pool, open_ms[entry_i])["streak_bar"]`, the quantiles
    `tierc7_lab_regime.STREAK_BAND_QUANTILES` of the home-panel bar pool `tierc9._trailing_pool(pool_lo_ms, pin − 1)`
    (`pin` = the as-of pin of the ride; the edge at an entry does not depend on it) restricted to bars with open
    `<=` the entry bar's open, defined once that prefix holds `tierc7_rules.PROVISIONAL_MIN_N` bars, `pool_lo_ms`
    read from `research_outputs/tierc12/x_rec/tierc11x/forward/BOOK_SPECS.json` key `pool_lo_ms` — OR (ii) its
    window age `entry_i − arm_i` (4h bars) is `>=` the cut read from the text of record of TC11's registration
    P-WIN-1 (`research_outputs/tierc11/registrations/REGISTRATIONS.json`) and asserted equal to the contract's
    (:54). The OR is inclusive: a campaign both OLD and stale is refused once. An entry bar whose trailing edges
    are undefined HALTs — it is never 'not refused'.
  - An entry bar with undefined edges HALTs the build (it is never 'not refused').
  - The scored arm must reproduce TC11's filed cell `age:on|win:on|ratr:off` of
    `research_outputs/tierc11/stage_g/g_grid_books.parquet` (its `n` and `n_refused`, and the key set implied by
    `g_campaign_gates.parquet`); otherwise the build HALTs.
  - `strip` — the extended ride's campaigns with entry close after TC11's pin, per arm under the column `arm`; rows
    and counts only.
  - `tierE__shadow_old_alone` — Tier-E: `base` minus the campaigns refused by clause (i) alone.
  - `tierE__shadow_stale_alone` — Tier-E: `base` minus the campaigns refused by clause (ii) alone.
  - `tierE__shadow_abs206` — Tier-E: `base` minus the campaigns whose entry-bar tide run is strictly above the
    absolute cut read from the text of record of TC11's registration P-AGE-1 and asserted equal to the contract's
    (:56); a whole-corridor cut, look-ahead on the scored window.
  - `tierE__shadow_abs206_or_stale` — Tier-E: `base` minus the campaigns above that absolute cut OR refused by
    clause (ii); the OLD clause of this arm reads the corridor ahead; only its stale clause is causal.
  - inputs pinned: HALT-grade pins, not closures (a failed pin prints no number and no word, spends no test and
    blocks CLOSE). `research_outputs/tierc11/books/build_manifest.json` (sha256
    `04f129b7731f700a3cf5eea0775e0a05792e7abd2ec458585feb4768a196bd24`);
    `research_outputs/tierc11/scores/BASE_IDENT.json` (`29f795dcae5c3994f8cc09d742c7480e989f09afe72113b95e2e8859a8ca5581`);
    `research_outputs/tierc11/stage_g/g_grid_books.parquet` (`b2c786e0e7204e1be49c31c0ed7eae7e61365e61ae608dd0efcbe0f4e3b7b51b`);
    `research_outputs/tierc11/stage_g/g_campaign_gates.parquet` (`c5a5f486df5709c0386e8733c9cc2490b1a15e6416b6f5adf45efcae608674d6`)
    — each also the sha TC11's `PROGRESS.json` certifies for it, asserted on every read;
    `research_outputs/tierc11/registrations/REGISTRATIONS.json` by TC11's chain head
    `6772568b31fcfb2d56eb8c80b66dedee4fb5082673369e872972df8f475ec8f9`
    (`research_outputs/tierc11/registrations/REGISTRY_PIN.json` key `head`, recomputed from the payloads) and the
    payload shas of the two registrations read, P-WIN-1
    `d19a42a329be3bfeea73c3c628bf515f5d0fa2fb8facd3fcac795b0186525084` and P-AGE-1
    `e01a89ea7e6fda864f7002a450abd1a4e92424c44d1a9626f6641814e7d35879` — never by that file's whole sha, which
    TC12's own close act moves; `research_outputs/tierc12/x_rec/tierc11x/forward/BOOK_SPECS.json`
    (`72a1f52359c66084d22f8bc99b0cd35e7edd89db2751f4859f559c8b1f51cac3`, the sha of its row in
    `research_outputs/tierc12/x_rec/X_REC_MANIFEST.json`); and Stage D's pin, manifest and fee schedule by the shas
    `research_outputs/tierc12/progress/TC12-D.json` certifies.
  - VA columns read (declared for F-VA-PINS (e)): none.
- **statistic:** `mean(net_r of the scored arm) − mean(net_r of the base arm)` — kept versus all, per campaign, in R
  net of the taker toll and funding (the TC-series toll of record).
- **comparison:** two-sample vs v6 (contract :52). The bootstrap of record (O-22; L-X.3, L-X.5, L-X.6): whole-asset
  clusters; `tierc5.cluster_boot_diff(kept values, kept assets, base values, base assets, seed, n_boot)` — one asset
  draw per replicate indexes both arms; N_BOOT draws; the interval is `tierc5._ci_from`'s 5th and 95th percentiles;
  `p = (#draws <= 0 + 1) / (N_BOOT + 1)` as a fraction; the seed of record is the contract's (:4), passed explicitly;
  the sensitivity seed `tierc5.SEED` printed beside.
- **preconditions:** none — the row has no precondition and cannot read CLOSED BY PRECONDITION
- **verdict_rule:** verdict_of_record = SUPPORTED iff (a) the cluster-90% CI lower bound (the 5th percentile of the
  draws) > 0 AND (b) one-sided p <= q ÷ m, exact, AND (c) every declared asset holds at least one row in every arm
  the ruler reads; else NOT SUPPORTED. m is fixed in every case; a registration closed by its precondition prints
  'CLOSED BY PRECONDITION (…) — no number · no test spent', spends no test and never loosens the bar. Printed
  beside, deciding nothing: the sensitivity seed, the haircut and all-taker twins, the tuning and holdout slices,
  LOAO, both single-trade shares, the literal-bar column, the exact enumeration with SEED-FRAGILE, the month-block
  twin with TIME-CLUSTER FRAGILE, the drop-OPEN twin with VERDICT RESTS ON OPEN MARKS, the forward strip unscored.
  Tier-E arms carry no verdict word. For this row q = 0.10 (contract :9), m = 2 and the bar = 0.05 (contract :52),
  N_BOOT = 4000 (`research_outputs/tierc11/scores/SCORES.json` key `n_boot`), the seed of record 20261008 (contract
  :4) and the sensitivity seed 20260816 (the same file's `seed_sens`). The verdict words this row can print are
  exactly two: SUPPORTED (all of (a), (b), (c)) and NOT SUPPORTED (any other outcome of a built row, with the
  qualifier PANEL INCOMPLETE or EMPTY BOOK when (c) fails, TWO-SAMPLE-PREMISE when the gate refuses nothing,
  REFUSALS ON a/N ASSETS when the refusals sit on too few assets for the ruler to clear, "CI wholly below zero"
  when the 95th percentile is below zero); CLOSED BY PRECONDITION is unreachable (no precondition); HALT and
  ABSENT are scorer statuses, not verdicts. The REFUSALS ON a/N ASSETS qualifier is decided on counts alone, before
  any outcome is read: with a = the number of declared assets holding at least one refused campaign and N the
  number declared, the exact probability that a draw holds no refusing asset and is identically zero is ((N − a) ÷
  N) to the power N; when that is at or above the bar the ruler cannot clear, the word is NOT SUPPORTED, the test
  is spent, and the cell is never cited as evidence against the gate (a = 0 is TWO-SAMPLE-PREMISE). The contract
  pre-names no kill for this row. The row prints
  '<verdict> — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (pre_seen: <clause>)'.
- **labels:**
  - `pre_seen` — tag: none; label: IN-SAMPLE RE-SCORE, NOT CONFIRMATORY; text: "TC11's crossed gate-book table
    printed this exact book before the contract was drafted — research_outputs/tierc11/stage_g/STAGE_G.md:197, row
    age:on¦win:on¦ratr:off (g_grid_books.parquet cell age:on|win:on|ratr:off), kept n 110 at mean net R +0.5146,
    the contract's 'cell 110 @ +0.515'; the same 200 campaigns, the same two refusals, a post-filter; both halves
    have filed verdicts of their own (P-AGE-1, P-WIN-1; DISCLOSURES D-4); the new information is the interval of
    the difference from v6; the point estimate of this row's statistic is fixed by filed numbers before scoring
    (the kept book's mean on file minus the v6 mean on file); the bar of this family (q ÷ 2) is looser than the bar
    under which both halves were scored on these campaigns in TC11 (q ÷ 9); a SUPPORTED here adds an interval to a
    seen effect and no evidence beyond TC11's; confirmation, if any, is the forward ledger's fourth book — nothing
    in this tier confirms this row"; items: external_context `research_outputs/tierc11/stage_g/STAGE_G.md` lines
    187-198 (sha256 `440509bc8c00bc32b48f745a8f76ca1b6c6d6ddb08f708432790ec164e2d0187`); disclosures: D-4.
- **disclosed_beside:**
  - L-X.14's common beside leaves — `seed_sens`, `haircut`, `haircut_sens`, `taker_twin`, `taker_twin_haircut`,
    `tuning_slice`, `holdout_slice`, `loao`, `loao_sens`, `concentration`, `share_x`, `literal_bar`, `exact`,
    `month_block`, `drop_open`, `strip` — each Tier-E, no verdict word. On this all-taker row the taker twin is
    the record's own book. The `strip` leaf prints n per arm and one pointer, no statistic.
  - `tierE__shadow_old_alone` — base minus the OLD campaigns; Tier-E, no verdict word; must equal TC11's filed
    `regbooks/P-AGE-1/scored` by `book_sha256`; TC11's own filed verdict cell quoted beside by JSON path with
    TC11's bar; ruled by the beside leaf `arm__shadow_old_alone` (the interval of the arm against `base` at the
    seed of record; `would_read_ci_only`; no p, no bar, no second seed, no slice, no LOAO).
  - `tierE__shadow_stale_alone` — base minus the stale campaigns; Tier-E, no verdict word; must equal TC11's filed
    `regbooks/P-WIN-1/scored` by `book_sha256`; TC11's own filed verdict cell quoted beside by JSON path with
    TC11's bar; ruled by the beside leaf `arm__shadow_stale_alone`, in the same form.
  - `tierE__shadow_abs206` — base minus the campaigns whose entry-bar run is above the absolute cut read from
    P-AGE-1's text of record; Tier-E, no verdict word; must equal TC11's filed `regbooks/P-AGE-1/tierE__shadow_abs206`
    by `book_sha256`; carries TC11's look-ahead caveat; ruled by the beside leaf `arm__shadow_abs206`, in the same
    form.
  - `tierE__shadow_abs206_or_stale` — the rival reading of 'the absolute-206 cut': base minus (above the absolute
    cut OR stale); Tier-E, no verdict word; carries TC11's look-ahead caveat; no filed twin; ruled by the beside
    leaf `arm__shadow_abs206_or_stale`, in the same form.
  - the refusal spread of the row — `refused_n`, `refused_assets`, `p_draw_identically_zero`,
    `n_draws_exact_zero` — count-only, filed before any outcome is read.
  - the refused cohort and the stale-only increment (refused by stale and not OLD): n, ΣR, mean on the gate row;
    Tier-E, no verdict word.
  - the re-ride disclosure — counts on the gate row (`rival_count_rejection_log`, `reride_n`,
    `reride_admitted_not_in_v6`, `reride_v6_not_taken`, `n_reride_differs`) and the differing campaigns in
    `research_outputs/tierc12/stage_g/g_reride_diff.parquet`; never an arm, no interval; Tier-E, no verdict word.
  - the crossed table 2×2×2×2 (contract :60) in both forms, partition and gate books, and the slot-arbitration
    event count; Tier-E, no verdict word.
  - the five-cluster size footnote, in the verdict text and as the last line under the row.
  - the forward ledger's fourth book `gated-v6-combined` — its spec
    `research_outputs/tierc12/forward/BOOK_SPEC_COMBINED.json` (sha filed at TC12-REG.ledger-spec); every row
    appended at TC12's pin entered before the book was frozen (flagged on the row) and none is a row of record for
    confirmation; `n` appended at TC12's pin, UNSCORED until its own n ≥ n_min; Tier-E, no verdict word; it is the
    contract's 'confirmation' (:55-56) and none of it is scored here.
- **failure_conditions:** F-CTRL (the base is TC11's filed book, trade by trade; RED if any CTRL column differs or
  the book sha is not the filed one — plant: a one-tick stop move). F-BASE-IDENT [P-ADM-1] (RED if the base arm's
  canonical sha is not TC11's, or the scored arm holds a foreign key or an altered kept row — plant: one base
  `net_r` moved by one ulp). F-GATE [SET · P-ADM-1], [POSTFILTER · P-ADM-1], [ANCHOR · P-ADM-1],
  [BOUND · P-ADM-1], [SUBSET · P-ADM-1] (RED if the refused set is not the text's, the scored arm is not a
  post-filter, the pre-seen cell or a shadow is not reproduced, a cut or the registry pin is not the filed object,
  or a gated key or strip row is not the extended book's — plants: the un-gated book, the intersection, the
  arm-bar age, whole-corridor edges, the one-bar-ahead prefix, the lag cut raised by one, a registration body
  altered in a copy of the registry, a key added to a copy of a gated book). F-EDGE-G (RED if a comparator is
  wrong at its boundary — plants: OLD strict, the lag cut strict, the absolute cut inclusive). F-TYPED-FLOW (RED
  if a bent cut moves nothing — plant: each cut bent at its door). F-REGBOOK [P-ADM-1] (RED if an arm breaks the
  regbook interface or the directory's arms are not exactly the named ones — plants: a duplicate key or a row
  past the score edge planted in a copy of the scored arm). F-VA-PINS [e · P-ADM-1] (RED if the builder reads a
  value-area column — plant: a state column read in a copy of the builder). F-KEY and F-DET on `stage_g/` and
  `regbooks/P-ADM-1/` (RED on an undeclared table, a duplicate or null key, a missing stamp, or a rebuild that is
  not hash-identical — plants: a duplicated key row; a table rebuilt in another row order). F-GRID on the two
  crossed grids (RED if the written cells are not the typed list or the partition does not sum to the base —
  plant: a dropped cell). F-BOOT (RED if the persisted draws are not the fixture's own loop, or an arm emptied on
  one asset reads anything but NOT SUPPORTED with PANEL INCOMPLETE — plant: clause (c) removed). F-VERDICT (RED
  if a typed case maps to another word, a gate whose refusals sit on too few assets and lacks its qualifier among
  them — plant: the row scored at another family's bar). F-SCORE-ANCHOR (RED if the mirrored rulers do not
  reproduce TC11's filed leaves on TC11's filed arms at TC11's seed — plant: the base arm replaced by the refused
  cohort).

### 1.2 P-BRD-1

- **id:** P-BRD-1
- **family:** ADMISSION (the family name parsed from the header line, contract :52: "STAGE G · ADMISSION FAMILY
  (m=2, bar 0.05; both two-sample vs v6 — they remove trades):")
- **family_m:** 2 (parsed from contract :52; two registrations stand under the header, :53 and :57)
- **family_bar:** 0.05 (parsed from contract :52; asserted equal, as fractions, to q ÷ m with q = 0.10 parsed from
  contract :9: "bar = 0.10 ÷ m per family")
- **prior:** 40 (contract :57: "P-BRD-1 [40%]")
- **mechanism:** Breadth asks whether trend regimes are NEW across the home panel at the moment of an entry. When at
  least two of the five home assets are in the first half of a tide run (YOUNG or EARLY by the trailing median of
  all tide runs seen so far), fresh tides are present in the panel and a card-v6 continuation entry rides a regime
  the market is still establishing. When fewer than two are, the panel's tides are mature, old, unformed or of
  unknown age, and a continuation entry is late or isolated. The claim is that refusing entries taken when
  panel-wide youth is absent leaves a book whose per-campaign expectancy exceeds the whole book's. The quantity is
  near-collinear with the campaign's own tide age by construction (the own asset is one of the five and the assets
  co-move), which is why the overlap with the OLD refusal is printed beside the row.
- **population:** assets: the five home assets `tierc2_rules.UNIVERSE` (contract :18), which are both the traded
  panel and the breadth panel. Lens: 4h. Scored window (O-9): campaigns of card v6 whose ENTRY bar closes at or
  before TC11's pin, read from `research_outputs/tierc11/data/AS_OF_PIN.json` key `as_of_last_closed_4h_close_ms`.
  Era: the full corridor inside that window (the text names no era); the tuning and holdout slices are Tier-E. The
  forward strip (entry close after TC11's pin, through TC12's pin) is ridden and printed for every arm and is
  scored by nothing.
- **arms:**
  - `base` — the filed v6 book on the scored window: `tierc10_panel.run_cell_n(CONTROL_CARD, tierc9.V6_ROLES,
    UNIVERSE, lo, hi)` with `(lo, hi) = tierc10_panel.corridor_n(UNIVERSE, pin_close_iso=<TC11's pin>)`, on the TC12
    snapshot (L-C.2) — the one base of the family (O-21), the same book as P-ADM-1's. The build HALTs unless its
    `TP._book_sha` equals `research_outputs/tierc11/books/build_manifest.json` key `book_sha.v6`, its n equals that
    file's `n.v6`, and its regbook `book_sha256` equals `research_outputs/tierc11/scores/BASE_IDENT.json` key
    `book_sha256["P-AGE-1"]`.
  - `scored` (the treated arm) — `base` minus the refused set, a POST-FILTER: the same Trade objects in the base's
    order, keyed (symbol, entry_ms), and no entry admitted into a slot a refusal frees (no re-ride). For a campaign
    with entry bar open `e` and decision instant `e + 4h`: each of the five home assets (the campaign's own
    included) is read at its bar closing at that instant (as-of join by time; a listed asset with no bar closing
    there HALTs); a member is DETERMINED YOUNG iff its tide is warm at that bar, its two-state tide run
    (`tierc7_lab_regime.tide_streak`; EMA periods `tierc7_rules.TIDE_FAST` and `tierc7_rules.TIDE_SLOW`; the flip
    bar counts as bar 1) is strictly below the YOUNG-or-EARLY edge — the edge that closes the bands labelled YOUNG
    and EARLY in `tierc7_lab_regime.STREAK_LABELS`, taken from `tierc9._trailing_edges(pool, e)["streak_bar"]`, the
    same home-panel bar pool, prefix (bars with open `<=` `e`), floor and `pool_lo_ms` as P-ADM-1's banding — and
    its streak is not the left-censored first one; `y5` = the number of determined-young members; the denominator
    is fixed at `N`, the number of home assets (a member not listed, not warm or of undetermined age is in the
    denominator and is not young). The campaign is refused iff `y5 · den < num · N` in integers, with `num/den` the
    contract's fraction (:58, "2/5") and `den` required to equal `N`; a campaign exactly at the cut is kept. An
    entry bar whose trailing edges are undefined HALTs — it is never 'not refused'.
  - An entry bar with undefined edges HALTs the build.
  - `strip` — the extended ride's campaigns with entry close after TC11's pin, per arm under the column `arm`; rows
    and counts only.
  - `tierE__brd_face` — Tier-E: the same rule with a left-censored member below the edge counted young.
  - `tierE__brd_neff` — Tier-E: the effective-denominator rule on the five (X4's law): undetermined members leave
    numerator and denominator; defined iff the edges are defined and the effective count is at least X's breadth
    floor (read from `research_outputs/tierc12/x_rec/scripts/tc11x_era.py`); refused iff defined and `y5 · den <
    num · n_eff5`; an undefined campaign is kept and flagged.
  - `tierE__brd_loo` — Tier-E: the same member classes on the home assets other than the campaign's own, the
    denominator fixed at `N − 1`.
  - `tierE__brd17` — Tier-E: X4's seventeen-asset breadth of record at the contract's cut (effective denominator,
    X's floor; an undefined campaign kept and flagged); the outcome of this split was seen at R0 (DISCLOSURES
    D-1).
  - inputs pinned: HALT-grade pins, not closures (a failed pin prints no number and no word, spends no test and
    blocks CLOSE). `research_outputs/tierc11/books/build_manifest.json` (sha256
    `04f129b7731f700a3cf5eea0775e0a05792e7abd2ec458585feb4768a196bd24`) and
    `research_outputs/tierc11/scores/BASE_IDENT.json` (`29f795dcae5c3994f8cc09d742c7480e989f09afe72113b95e2e8859a8ca5581`)
    — each also the sha TC11's `PROGRESS.json` certifies for it, asserted on every read;
    `research_outputs/tierc12/x_rec/tierc11x/forward/BOOK_SPECS.json`
    (`72a1f52359c66084d22f8bc99b0cd35e7edd89db2751f4859f559c8b1f51cac3`),
    `research_outputs/tierc12/x_rec/tierc11x/era/X4_stamps.parquet` and
    `research_outputs/tierc12/x_rec/scripts/tc11x_era.py` by the shas of their rows in
    `research_outputs/tierc12/x_rec/X_REC_MANIFEST.json`; the tide series
    `research_outputs/tierc12/tide/tide_bars_4h.parquet` and `breadth_4h.parquet` by the shas
    `research_outputs/tierc12/progress/TC12-C.tide.json` certifies; and Stage D's pin, manifest and fee schedule by
    the shas `research_outputs/tierc12/progress/TC12-D.json` certifies. The scored arm reads no cut from TC11's
    registry; the stale flag of the overlaps and the stale and far-stop bits of the crossed table printed beside
    it do (P-WIN-1), and the stage's one builder reads P-AGE-1 for the other row's shadows; so
    `research_outputs/tierc11/registrations/REGISTRATIONS.json` is pinned here too, by TC11's chain head
    `6772568b31fcfb2d56eb8c80b66dedee4fb5082673369e872972df8f475ec8f9`
    (`research_outputs/tierc11/registrations/REGISTRY_PIN.json` key `head`, recomputed from the payloads) and the
    payload shas of P-WIN-1 `d19a42a329be3bfeea73c3c628bf515f5d0fa2fb8facd3fcac795b0186525084` and P-AGE-1
    `e01a89ea7e6fda864f7002a450abd1a4e92424c44d1a9626f6641814e7d35879` — never by that file's whole sha, which
    TC12's own close act moves.
  - VA columns read (declared for F-VA-PINS (e)): none.
- **statistic:** `mean(net_r of the scored arm) − mean(net_r of the base arm)` — kept versus all, per campaign, in R
  net of the taker toll and funding.
- **comparison:** two-sample vs v6 (contract :52). The bootstrap of record (O-22; L-X.3, L-X.5, L-X.6): whole-asset
  clusters; `tierc5.cluster_boot_diff` on one asset draw per replicate; N_BOOT draws; the interval is
  `tierc5._ci_from`'s 5th and 95th percentiles; `p = (#draws <= 0 + 1) / (N_BOOT + 1)` as a fraction; the seed of
  record is the contract's (:4), passed explicitly; the sensitivity seed `tierc5.SEED` printed beside.
- **preconditions:** none — the row has no precondition and cannot read CLOSED BY PRECONDITION
- **verdict_rule:** verdict_of_record = SUPPORTED iff (a) the cluster-90% CI lower bound (the 5th percentile of the
  draws) > 0 AND (b) one-sided p <= q ÷ m, exact, AND (c) every declared asset holds at least one row in every arm
  the ruler reads; else NOT SUPPORTED. m is fixed in every case; a registration closed by its precondition prints
  'CLOSED BY PRECONDITION (…) — no number · no test spent', spends no test and never loosens the bar. Printed
  beside, deciding nothing: the sensitivity seed, the haircut and all-taker twins, the tuning and holdout slices,
  LOAO, both single-trade shares, the literal-bar column, the exact enumeration with SEED-FRAGILE, the month-block
  twin with TIME-CLUSTER FRAGILE, the drop-OPEN twin with VERDICT RESTS ON OPEN MARKS, the forward strip unscored.
  Tier-E arms carry no verdict word. For this row q = 0.10 (contract :9), m = 2 and the bar = 0.05 (contract :52),
  N_BOOT = 4000 (`research_outputs/tierc11/scores/SCORES.json` key `n_boot`), the seed of record 20261008 (contract
  :4) and the sensitivity seed 20260816 (the same file's `seed_sens`). The verdict words this row can print are
  exactly two: SUPPORTED (all of (a), (b), (c)) and NOT SUPPORTED (any other outcome of a built row, with the
  qualifier PANEL INCOMPLETE or EMPTY BOOK when (c) fails, TWO-SAMPLE-PREMISE when the gate refuses nothing,
  REFUSALS ON a/N ASSETS when the refusals sit on too few assets for the ruler to clear, "CI wholly below zero"
  when the 95th percentile is below zero); CLOSED BY PRECONDITION is unreachable (no precondition); HALT and
  ABSENT are scorer statuses, not verdicts. The REFUSALS ON a/N ASSETS qualifier is decided on counts alone, before
  any outcome is read: with a = the number of declared assets holding at least one refused campaign and N the
  number declared, the exact probability that a draw holds no refusing asset and is identically zero is ((N − a) ÷
  N) to the power N; when that is at or above the bar the ruler cannot clear, the word is NOT SUPPORTED, the test
  is spent, and the cell is never cited as evidence against the gate (a = 0 is TWO-SAMPLE-PREMISE). The contract
  pre-names no kill for this row. DISCLOSURES D-1 and the key overlap of the refused set with the seventeen-asset
  twin (counts only) are printed directly under the cell. The row prints
  '<verdict> — NOT CONFIRMATORY (selection_hazard: direction-informed)'.
- **labels:**
  - `selection_hazard` — tag: direction-informed; label: NOT CONFIRMATORY; text: "direction informed by TC11-X's
    X4 breadth tables on these same 200 campaigns — the E-2 composition term of the breadth block and the E-1
    breadth thirds (research_outputs/tierc12/x_rec/tierc11x/era/X4.md:28 and :576 ff.; X4_tables.parquet tables
    E-2 and E-1, block breadth); X4's breadth is a seventeen-asset share with an effective denominator, not this
    row's five-asset count; X4's own sentence for breadth reads UNRESOLVED (X4.md:16); X4 prints that breadth is
    near-collinear with the campaign's own tide age (X4.md:1581); a scout computed a split of that seventeen-asset
    breadth at this cut before the readings were frozen (DISCLOSURES D-1)"; items: external_context
    `research_outputs/tierc12/x_rec/tierc11x/era/X4.md` lines 16 and 28 (sha256
    `aac2be88b8d71f46c232a1976cd5d06dd5ded91b3356976050a48344e9557be8`); disclosures: D-1, printed directly under
    the cell, and under it the cell counts of `research_outputs/tierc12/stage_g/g_brd17.parquet` (the key overlap
    of this row's refused set with the cohort whose outcome D-1 records as seen; counts only, no outcome).
- **disclosed_beside:**
  - L-X.14's common beside leaves — `seed_sens`, `haircut`, `haircut_sens`, `taker_twin`, `taker_twin_haircut`,
    `tuning_slice`, `holdout_slice`, `loao`, `loao_sens`, `concentration`, `share_x`, `literal_bar`, `exact`,
    `month_block`, `drop_open`, `strip` — each Tier-E, no verdict word. On this all-taker row the taker twin is
    the record's own book. The `strip` leaf prints n per arm and one pointer, no statistic.
  - `tierE__brd_face` — the face-value twin (a left-censored member below the edge counted young); Tier-E, no
    verdict word; ruled by the beside leaf `arm__brd_face` (the interval of the arm against `base` at the seed of
    record; `would_read_ci_only`; no p, no bar, no second seed, no slice, no LOAO).
  - `tierE__brd_neff` — the effective-denominator twin on the five (X4's law; undefined campaigns kept and
    flagged); Tier-E, no verdict word; ruled by the beside leaf `arm__brd_neff`, in the same form.
  - `tierE__brd_loo` — the leave-own-out twin (the home assets other than the campaign's own, the denominator
    fixed at their number, `N − 1`); Tier-E, no verdict word; ruled by the beside leaf `arm__brd_loo`, in the same
    form.
  - `tierE__brd17` — the breadth-17 twin (X4's seventeen-asset breadth of record at the contract's cut); Tier-E, no
    verdict word; its counts held equal to X's filed stamps; ruled by the beside leaf `arm__brd17`, in the same
    form, which carries the note 'outcome of this split seen at R0 (D-1)'.
  - the refusal spread of the row — `refused_n`, `refused_assets`, `p_draw_identically_zero`,
    `n_draws_exact_zero` — count-only, filed before any outcome is read.
  - the overlaps of the refused set with OLD, with stale and with the combined refusal: n, ΣR, mean on the gate
    row; Tier-E, no verdict word.
  - the whole breadth {0..5} × own-band grid (contract :59) and the breadth-17 agreement table, each printed
    whole; Tier-E, no verdict word.
  - the crossed table 2×2×2×2 (contract :60) in both forms, partition and gate books; Tier-E, no verdict word.
  - the re-ride disclosure — counts on the gate row (`rival_count_rejection_log`, `reride_n`,
    `reride_admitted_not_in_v6`, `reride_v6_not_taken`, `n_reride_differs`) and the differing campaigns in
    `research_outputs/tierc12/stage_g/g_reride_diff.parquet`; never an arm, no interval; Tier-E, no verdict word.
  - the five-cluster size footnote, in the verdict text and as the last line under the row.
- **failure_conditions:** F-CTRL (the base is TC11's filed book, trade by trade; RED if any CTRL column differs or
  the book sha is not the filed one — plant: a one-tick stop move). F-BASE-IDENT [P-BRD-1] (RED if the base arm's
  canonical sha is not TC11's, or the scored arm holds a foreign key or an altered kept row — plant: one base
  `net_r` moved by one ulp). F-TIDE-SERIES [ORACLE], [ASOF], [GRID], [ROUND], [X] (RED if the per-bar series
  differs from the lineage's arrays, from a fresh cut-tape rebuild, or from X's filed seventeen-asset stamps, a
  tape is off the grid, or an edge does not round-trip — plants: whole-corridor edges, the one-bar-ahead prefix,
  the run counted from bar 0, a tape with a bar removed). F-BRD [THREE], [ALL], [JOIN], [ORDER] (RED if breadth
  recomputed independently differs on the three rule-chosen bars or on any entry bar, or a join or ordering
  identity fails — plants: members read one bar ahead, an index join, an unwarm member counted, the denominator
  taken as the warm count, an undetermined member counted, the own asset left out). F-GATE [SET · P-BRD-1],
  [POSTFILTER · P-BRD-1], [BOUND · P-BRD-1], [OVERLAP · P-BRD-1], [SUBSET · P-BRD-1] (RED if the
  refused set is not `y5 · den < num · N`, the scored arm is not a post-filter, the fraction used is not the
  contract's, an overlap count or a breadth-17 agreement count does not re-derive, or a gated key or strip row is
  not the extended book's — plants: the un-gated book, one campaign moved between two overlap cells, a key added
  to a copy of a gated book). F-EDGE-G (RED if the cut is inclusive — plant: `<=`). F-TYPED-FLOW (RED if the bent
  fraction moves nothing — plant: the numerator bent at the pin door). F-GRID on the breadth grid and the
  breadth-17 table (RED if the written cells are not the typed list or the grid does not sum to the base — plant:
  a dropped cell). F-REGBOOK [P-BRD-1] (RED if an arm breaks the regbook interface or the directory's arms are not
  exactly the named ones — plants: a duplicate key or a row past the score edge planted in a copy of the scored
  arm). F-VA-PINS [e · P-BRD-1] (RED if the builder reads a value-area column — plant: a state column read in a
  copy of the builder). F-KEY and F-DET on `tide/`, `stage_g/` and `regbooks/P-BRD-1/` (RED on an undeclared
  table, a duplicate or null key, a missing stamp, or a rebuild that is not hash-identical — plants: a duplicated
  key row; a table rebuilt in another row order). F-BOOT (RED if the persisted draws are not the fixture's own
  loop, or an arm emptied on one asset reads anything but NOT SUPPORTED with PANEL INCOMPLETE — plant: clause (c)
  removed). F-VERDICT (RED if a typed case maps to another word, a gate whose refusals sit on too few assets and
  lacks its qualifier among them — plant: the row scored at another family's bar). F-SCORE-ANCHOR (RED if the
  mirrored rulers do not reproduce TC11's filed leaves on TC11's filed arms at TC11's seed — plant: the base arm
  replaced by the refused cohort).

### 1.3 P-DIR-1

- **id:** P-DIR-1
- **family:** RANGE-STATE — the family name of the contract's STAGE R header (:64).
- **family_m:** 2 — parsed from contract :64 ("m=2") by L-X.1; two registrations stand under that header (:65, :69).
- **family_bar:** 0.05 — parsed from contract :64 ("bar 0.05"); asserted equal to q ÷ m with q = 0.10 parsed from :9.
- **prior:** 45 — parsed from the text slice ("[45%]", contract :65).
- **mechanism:** A v6 trend entry taken while the 4h lens stands ACCEPTED outside value on the side opposite to the trade is an entry against a price the market has already accepted away from value in the other direction: the entry bar's 12/26 trigger fires inside a move the value-area machine reads as established against it. The gate removes those entries and nothing else. It is a statement about the STATE of value at the entry close (acceptance needs eight consecutive closes beyond the edge or one close a large multiple of ATR beyond it), not about distance, tide or range position; it is independently failable from P-SFP-VA-1, which trades a different event on a different book.
- **population:** the five home assets (contract :18); lens 4h; the base book = card v6 as TC11 filed it, every campaign (L-R.1); era of record the full corridor (no era is named; TC11 L-1.3); scored window per O-9: campaigns whose entry bar closes at or before TC11's pin, read by object from `research_outputs/tierc11/data/AS_OF_PIN.json["as_of_last_closed_4h_close_ms"]`; campaigns entered in the forward strip are printed beside, unscored.
- **arms:**
  - `base` — the v6 book on the scored window, bit-equal on the sixteen regbook columns to TC11's filed v6 (canonical `book_sha256` == `research_outputs/tierc11/scores/BASE_IDENT.json["book_sha256"]["P-AGE-1"]`).
  - `scored` — the treated arm; two arms and no re-ride (O-21; L-R.4, L-R.5): `base` minus every campaign with `refuse == True`, where `refuse ⇔ (direction == +1 AND state == "ACCEPTED_BELOW") OR (direction == −1 AND state == "ACCEPTED_ABOVE")` and `state` is the filed 4h state after the entry bar's close: row `k = asof_index(4h closes, entry_close_ms)` of `research_outputs/tierc12/va/va_bars_4h.parquet`, with `close_ms[k] == entry_close_ms` asserted (L-R.2, L-R.3). Every other state — INSIDE, PROBING on either side, ACCEPTED on the trade's own side, UNDEFINED — is kept. Kept rows are identical to their base rows; no campaign is re-ridden.
  - `strip` — the extended ride's campaigns with entry close after TC11's pin, per arm under the column `arm` (`base`: all of them; `scored`: those the same predicate keeps at their own entry close); rows and counts only.
  - inputs pinned: `research_outputs/tierc12/va/va_bars_4h.parquet` (certified by `progress/TC12-V.json`); the `base` arm (`regbooks/P-DIR-1/base.parquet`, certified by `progress/TC12-R.dir.json`; its book identity held to TC11's by F-BASE-IDENT); `research_outputs/tierc12/va/stamps/VA_STAMPS_v6.parquet` (certified by `progress/TC12-V.stamps.c.json`; the entry-row equality); `research_outputs/tierc11/stage_r/R5_CHOP_DIRECTION.parquet` (sha256 `a73b4894998e326a7264619ddd012f37bdf8c193fd512b90b082792c524846f1`) and `research_outputs/tierc11/stage_r/NEST_v6.parquet` (each certified by TC11's progress record). These are HALT-grade pins, not closures: a pin that does not verify stops the build and prints no word.
  - VA columns read (declared for F-VA-PINS (e)): by the gate, from `research_outputs/tierc12/va/va_bars_4h.parquet` — `asset`, `close_ms`, `state`; printed only — `pct`, `edge_dist_atr`, `accept_age`, `armed_top`, `armed_bottom`, `L`, `l_label`; by the Tier-E chop tables of the same builder, deciding nothing, from `va_bars_4h.parquet` and `va_bars_1d.parquet` — `asset`, `close_ms`, `state`, `pct`, `val`, `vah`, `L`, `l_label`; from `va/stamps/VA_STAMPS_v6.parquet` — the `4h_` block of the `entry` rows, for the equality assertion only. No `1w_` column.
- **statistic:** `mean(net_r of the kept book) − mean(net_r of the whole v6 base)` (kept versus all, never kept versus refused).
- **comparison:** two-sample vs v6 (contract :65). Bootstrap of record per O-22: whole-asset clusters; `N_BOOT` draws (on file 4000, `research_outputs/tierc11/scores/SCORES.json["n_boot"]`); `tierc5.cluster_boot_diff` with one asset pick per draw indexing both arms; the interval is `tierc5._ci_from`'s 5th / 95th percentile; `p = (#draws ≤ 0 + 1) / (N_BOOT + 1)` as a Fraction; seed 20261008 (contract :4) passed explicitly, the sensitivity seed (on file 20260816) printed beside.
- **preconditions:** none — the gate trades no range and no licence word governs it; the row has no precondition and cannot read CLOSED BY PRECONDITION
- **verdict_rule:** verdict_of_record = SUPPORTED iff (a) the cluster-90% CI lower bound (the 5th percentile of the draws) > 0 AND (b) one-sided p <= q ÷ m, exact, AND (c) every declared asset holds at least one row in every arm the ruler reads; else NOT SUPPORTED. m is fixed in every case; a registration closed by its precondition prints 'CLOSED BY PRECONDITION (…) — no number · no test spent', spends no test and never loosens the bar. Bootstrap of record: asset-cluster bootstrap by scripts/tierc12_score.py, T5 primitives, N_BOOT 4000, seed 20261008, sensitivity seed 20260816 beside. The exhaustive words of this row: SUPPORTED (a, b and c hold); NOT SUPPORTED (any of a, b, c fails; with the qualifier PANEL INCOMPLETE or EMPTY BOOK when c fails, TWO-SAMPLE-PREMISE when the gate refuses nothing, REFUSALS ON a/N ASSETS when the refusals sit on too few assets for the ruler to clear, 'CI wholly below zero' when hi < 0); CLOSED BY PRECONDITION is unreachable (no precondition). The REFUSALS ON a/N ASSETS qualifier is decided on counts alone, before any outcome is read: with a = the number of declared assets holding at least one refused campaign and N the number declared, the exact probability that a draw holds no refusing asset and is identically zero is ((N − a) ÷ N) to the power N; when that is at or above the bar the ruler cannot clear, the word is NOT SUPPORTED, the test is spent, and the cell is never cited as evidence against the gate (a = 0 is TWO-SAMPLE-PREMISE). A cell scored again after a dated refile, or on a regbook rebuilt after its first build, carries the scorer's refile or rebuild qualifier with the superseded line printed under it; neither changes the rule of the word. The contract pre-names no kill for this row. Printed beside, deciding nothing: the sensitivity seed, the haircut and all-taker twins, the tuning and holdout slices, LOAO, both single-trade shares, the literal-bar column, the exact enumeration with SEED-FRAGILE, the month-block twin with TIME-CLUSTER FRAGILE, the drop-OPEN twin with VERDICT RESTS ON OPEN MARKS, the forward strip unscored; the five-cluster size footnote; the refusal spread; directly under the cell, the key overlap of the refused set with TC11 R5's two expansion cells, counts only; the refused cohort's n, mean and ΣR with ΣR of both books, and, iff mean(refused) > 0, 'on per-campaign expectancy only; the gate forfeits +X R total'. Tier-E arms carry no verdict word. This registration carries selection_hazard only and prints '<verdict> — NOT CONFIRMATORY (selection_hazard: direction-informed)'.
- **labels:**
  - `selection_hazard` — tag: direction-informed; label: NOT CONFIRMATORY; text: "the direction of this gate (refuse an entry taken against an acceptance) was informed by TC11's R5 alignment table on this same v6 book and corridor, by pivot state: expansion aligned +0.491349 mean net R over 47 campaigns against expansion counter −0.493933 over 12; the value-area state itself was not tabulated against v6 outcomes in any filed table; new here are the detector and the interval"; items: `research_outputs/tierc11/stage_r/R5_CHOP_DIRECTION.parquet` (sha256 `a73b4894998e326a7264619ddd012f37bdf8c193fd512b90b082792c524846f1`), cells `calibrated|4h|alignment|EXP_ALIGNED` and `calibrated|4h|alignment|EXP_COUNTER`; `research_outputs/tierc11/stage_r/R5_CHOP.md:120-121`; contract :67.
- **disclosed_beside:** each Tier-E, no verdict word.
  - L-X.14's common leaves: `seed_sens`, `haircut`, `haircut_sens`, `taker_twin`, `taker_twin_haircut`, `tuning_slice`, `holdout_slice`, `loao`, `loao_sens`, `concentration`, `share_x`, `literal_bar`, `exact`, `month_block`, `drop_open`, `strip` (`n` per arm and one pointer).
  - Directly under the cell, counts only, no outcome: `n_refused` and, of those, the number in TC11 R5's `EXP_COUNTER` cell and in its `EXP_ALIGNED` cell (`research_outputs/tierc12/stage_r/dir/build_manifest.json` → `r5_overlap`; the pivot state at the entry instant from `research_outputs/tierc11/stage_r/NEST_v6.parquet`, calibrated 4h; L-R.6).
  - The refusal spread, counts only: `refused_n`, `refused_assets`, `p_draw_identically_zero`, `n_draws_exact_zero`.
  - The 4h lookback is tuning-fit (`l_label`: in-sample for tuning-era VA bars); the holdout slice is printed beside for that reason.
  - The re-ride disclosure counts and `stage_r/dir/dir_reride_diff.parquet` (L-R.5): `rival_count_rejection_log`, `reride_n`, `reride_admitted_not_in_v6`, `reride_v6_not_taken`, `n_reride_differs`; no arm, no interval.
  - The with-vs-against acceptance table `research_outputs/tierc12/stage_r/dir/VA_CHOP_ALIGNMENT.parquet` (L-R.9), whose 4h ACCEPTED_AGAINST cell is the refused cohort; printed whole in the report's §0.2.
  - The full VA chop table `research_outputs/tierc12/stage_r/dir/VA_CHOP.parquet` — v6 by 4h and 1d state × fixed %-of-value band (L-R.8); printed whole in `stage_r/dir/STAGE_R_dir.md`.
  - Counts only, no outcome: the campaigns the prior-bar as-of reading would refuse instead; refusals with both sides disarmed; refusals whose entry close lies inside the rolling value area.
- **failure_conditions:** each a fixture leg with its planted mutation.
  - F-DIR [a] set equality, post-filter identity and the key-subset law (plant: a refused campaign restored); [b] three refusals and two kept witnesses hand-verified by the frozen key-order rule, every refusal when fewer than three exist (plant: the sides swapped); [c] the as-of on the filed 4h table cut at the entry close (plant: the state read one row late); [d] the un-gated book must FAIL; [e] the synthetic truth table (plant: PROBING counted as ACCEPTED); [f] the re-ride identity (plant: a refused trigger that holds the slot); [g] the label's quoted cells and the overlap counts (plant: one digit changed).
  - F-BASE-IDENT, F-REGBOOK, F-KEY, F-BOOT, F-VERDICT, F-SCORE-ANCHOR, F-GRID, F-DET (L-X, L-0).
  - F-CHOP and F-GRID on the two chop tables; F-CLOSURE with the gate builder in the decision set; F-VA-PINS (e); F-NOT leg 1W (no `1w_` column read by this builder).

### 1.4 P-SFP-VA-1

- **id:** P-SFP-VA-1
- **family:** RANGE-STATE — the family name of the contract's STAGE R header (:64).
- **family_m:** 2 — parsed from contract :64 ("m=2") by L-X.1.
- **family_bar:** 0.05 — parsed from contract :64 ("bar 0.05"); asserted equal to q ÷ m with q = 0.10 parsed from :9.
- **prior:** 45 — parsed from the text slice ("[45%]", contract :69).
- **mechanism:** A probe beyond a value-area edge that closes back inside within three closes is a failed auction at that edge: the market tested prices outside value and did not accept them. Inside an unaccepted value area the next reference prices are the point of control and then the opposite edge, so the failure is faded toward them with a stop beyond the extreme the probe reached, a time stop at the lens's own edge-to-edge traverse, and an exit if the lens does accept beyond the faded edge after all. The trade needs no trend and no tide; it stands on the range being respected, which is what the value-area feasibility licence at 4h (taker) asserts. It is independently failable from P-DIR-1.
- **population:** the five home assets (contract :69-70), both directions pooled; lens 4h; every V2 swing failure at VAH or VAL (L-R.10); era of record the full corridor (contract :69) inside the scored window per O-9: trades whose entry bar closes at or before TC11's pin, read by object from `research_outputs/tierc11/data/AS_OF_PIN.json["as_of_last_closed_4h_close_ms"]`; a trade open at that instant is marked there (`corridor_end`) and listed OPEN; the forward strip is ridden and printed beside, unscored.
- **arms:**
  - `scored` — the one arm the ruler reads; no base (vs zero). Per swing-failure row of `research_outputs/tierc12/va/va_events.parquet` (lens 4h, kind `swing_failure`, the five home assets), in bar order per asset, four tests in this order, the first that fails naming the row's disposition: (1) one position per asset — an event at bar b is skipped iff `entry_i < b ≤ exit_i` of the trade open on that asset; (2) geometry; (3) rr-min; (4) the walk. ENTRY: `entry_px = e` = the close of the return bar, taker; direction = the event's sign (a failure at VAH short, at VAL long). STOP: `tierc10_brk.brk_stop` (= `tierc5_rules.spring_stop`) on `ext` = the probe's extreme including the return bar: long `min(ext − B·A, e − RAIL·A)`, short mirrored; `B` = `STOP_BUF_ATR`, `RAIL` = the contract's 1.0 (:71), `A` = ATR_4h of the return bar; `R = |e − stop|`, fixed for life. TARGETS, frozen at entry on the profile whose edge was probed, VA(t0−1): `T1` = its POC (`poc_f`), the card's harvest fraction ("half") off; `T2` = its far edge − d·0.25·A (contract :72), the remainder; both are touch-triggered taker exits booked at their level. GEOMETRY: Refused (geometry) iff the stop is undefined, or `d·(T1 − e) ≤ 0` (the POC is not ahead of the entry), or `d·(T2 − e) ≤ 0`. Not a refusal: `d·(T2 − T1) ≤ 0` voids T1 and the whole position exits at T2. Skipped (rr-min) iff `d·(T2 − e) / R < 1.5` (contract :73). A T1 within the round-trip taker fee of the entry price is traded as written and flagged. WALK on 4h bars from the bar after entry: a bar opening at or beyond the stop exits at the open; else the stop, adverse-first, at the stop price; then T1 at T1; then T2 at T2, same bar if reached; a target books its level with no gap improvement; then at the close the invalidation — the first V2 acceptance row of the 4h lens on the faded side — then the time stop at the close of bar `entry_i + T`, T the fitted 4h traverse read by object (`research_outputs/tierc12/va/TRAVERSE.json by_lens.4h.T_of_record`); a position still open at the last 4h bar closing at or before TC11's pin is marked at that close (`corridor_end`). No trail, no stop move, no tide read, no 5m bar. BOOKING: `tierc10_brk.account_l` on the 4h lens frame with T1 as the harvest slice; taker on every leg; interval-sum funding, uncapped (the D12 ceiling is a v6-card rule and is not a rule of this trade); `net_r = gross_r − fee_r − funding_r` in units of R.
  - `strip` — each ridden arm's own ride past TC11's pin: its trades with entry close after TC11's pin and at or before TC12's pin, per arm under the column `arm`; rows and counts only.
  - `tierE__unfiltered` — the scored construction without the rr-min skip and with nothing else changed (the three geometry refusals stand), re-walked with its own one-position sequence (contract :74).
  - `tierE__cell_1d` — the scored construction on the 1d lens (contract :74): V2 swing failures of lens 1d, ATR_1d, the fitted 1d traverse (`research_outputs/tierc12/va/TRAVERSE.json by_lens.1d.T_of_record`), the same constants; its sidecar carries pointers to the three era rows of the `1d|taker` licence and booleans, never the words.
  - `tierE__guard_1d` — the scored construction with one added refusal after the one-position test: the event is refused when the filed 1d state at the last 1d bar closed at or before the entry close is accepted against the trade (contract :75); re-walked.
  - `tierE__maker_conditioned` — the maker twin, fill-conditioned (contract :75): maker bps on entry, T1 and T2, taker on the stop, the time stop, the invalidation and the mark; the conditioned arm books only if the first 5m bar after the entry close trades through the entry price by the fill of record (one tick, exact); its maker targets fill by the same rule; otherwise a MISS, counted, never a trade.
  - `tierE__maker_assumed` — the scored arm's own walk and rows, re-booked at maker bps on entry, T1 and T2.
  - `tierE__x_geometry` — the scored construction under TC11-X's geometry law in place of this row's: an event is refused when T1 or T2 lies within the round-trip taker fee of the entry price or when T2 is not beyond T1, and no T1 is void; re-walked.
  - `tierE__x_gaplaw` — the scored construction under TC11-X's record gap law in place of this row's: the open decides first for stop and targets, a stop books the stop price through a gap, a target books the better of its level and the open; re-walked.
  - inputs pinned: `research_outputs/tierc12/va/va_events.parquet`, `research_outputs/tierc12/va/va_bars_1d.parquet`, `research_outputs/tierc12/va/TRAVERSE.json` and `research_outputs/tierc12/va/VA_MIRROR.json` (each certified by `progress/TC12-V.json`); `scripts/tierc12_rangewalk.py` (certified by `progress/TC12-R.sfp.json`, with F-SFP-MIRROR GREEN against TC11-X's filed `research_outputs/tierc12/x_rec/tierc11x/sfp/X2_trades_4h.parquet`, `X2_trades_1h.parquet` and `X2_twins.parquet`). These are HALT-grade pins, not closures: a pin that does not verify stops the build and prints no word.
  - VA columns read (declared for F-VA-PINS (e)): by the scored arm — from `va_events.parquet`, swing-failure rows: `lens`, `asset`, `kind`, `side`, `t0`, `i`, `bars_out`, `E`, `extreme`, `sgn`, `val_f`, `poc_f`, `vah_f`, `close_i`, `atr_i`, `known_close_ms`, `era`, `in_strip`, `ret_inside_frozen`, `ret_inside_rolling`, `from_state`, and for one printed count `val_n`, `poc_n`, `vah_n`; acceptance rows (the invalidation): `lens`, `asset`, `kind`, `side`, `i`, `E`, `known_close_ms`; from `va/TRAVERSE.json`, through the reader's `traverse` — `by_lens.4h.T_of_record`; from `va/VA_MIRROR.json`, through the reader's `licence` — the leaf `licence["4h|taker"].by_era["ALL"]`. By the Tier-E arms of the same builder — from `va_bars_1d.parquet`: `asset`, `open_ms`, `close_ms`, `close`, `atr`, `state`; the same event fields on lens 1d; `by_lens.1d.T_of_record`; the leaves `licence["1d|taker"].by_era` for `ALL`, `tuning` and `holdout`. No `1w_` column.
- **statistic:** `mean(net_r of the scored book)`.
- **comparison:** vs zero (contract :69). Bootstrap of record per O-22: whole-asset clusters; `N_BOOT` draws (on file 4000, `research_outputs/tierc11/scores/SCORES.json["n_boot"]`); `tierc5.cluster_boot`; the interval is `tierc5._ci_from`'s 5th / 95th percentile; `p = (#draws ≤ 0 + 1) / (N_BOOT + 1)` as a Fraction; seed 20261008 (contract :4) passed explicitly, the sensitivity seed (on file 20260816) printed beside.
- **preconditions:**
  - {record: research_outputs/tierc12/va/VA_MIRROR.json, certified_by: progress/TC12-V.json artifact_shas, selector: licence["4h|taker"].by_era["ALL"].would_read, required: "PASS"} — the licence row of the row's own scoring era (O-17); the record quotes `research_outputs/tierc12/x_rec/tierc11x/va/feasibility.parquet` (sha256 `ea8573b3240bb1112521c55f0a52ee2ed7156c598b7665685d0b86eefbecb6f0`) and computes nothing.
  - {record: research_outputs/tierc12/va/VA_MIRROR.json, certified_by: progress/TC12-V.json artifact_shas, selector: licence_set, required: contains "4h|taker"} — the contract's word of record (:39-41).
- **verdict_rule:** verdict_of_record = SUPPORTED iff (a) the cluster-90% CI lower bound (the 5th percentile of the draws) > 0 AND (b) one-sided p <= q ÷ m, exact, AND (c) every declared asset holds at least one row in every arm the ruler reads; else NOT SUPPORTED. m is fixed in every case; a registration closed by its precondition prints 'CLOSED BY PRECONDITION (…) — no number · no test spent', spends no test and never loosens the bar. Bootstrap of record: asset-cluster bootstrap by scripts/tierc12_score.py, T5 primitives, N_BOOT 4000, seed 20261008, sensitivity seed 20260816 beside. The exhaustive words of this row: CLOSED BY PRECONDITION (a precondition item is not met; checked first, before any arm is built; no ruler is called; STATUS only, no arm; the cell reads 'CLOSED BY PRECONDITION (research_outputs/tierc12/va/VA_MIRROR.json#<selector> reads <found>; required <required>) — no number · no test spent'); SUPPORTED (the preconditions are met and a, b and c hold); NOT SUPPORTED (the preconditions are met and any of a, b, c fails; with the qualifier PANEL INCOMPLETE or EMPTY BOOK when c fails, 'CI wholly below zero' when hi < 0). A cell scored again after a dated refile, or on a regbook rebuilt after its first build, carries the scorer's refile or rebuild qualifier with the superseded line printed under it; neither changes the rule of the word. The contract pre-names no kill for this row. Printed beside, deciding nothing: the sensitivity seed, the haircut and all-taker twins, the tuning and holdout slices, LOAO, both single-trade shares, the literal-bar column, the exact enumeration with SEED-FRAGILE, the month-block twin with TIME-CLUSTER FRAGILE, the drop-OPEN twin with VERDICT RESTS ON OPEN MARKS, the forward strip unscored; the five-cluster size footnote; the licence words of the three eras; under the cell, the label's text with DISCLOSURES D-2 and D-3. Tier-E arms carry no verdict word. This registration carries pre_seen (KIN-SEEN) and prints '<verdict> — NOT CONFIRMATORY (pre_seen · KIN-SEEN: X3 printed value-area swing-failure outcomes on these bars)'.
- **labels:**
  - `pre_seen` — tag: KIN-SEEN; label: NOT CONFIRMATORY; text: "TC11-X's X3 printed value-area swing-failure outcomes at 4h on these five assets for every bar at or before 2026-09-25T00:00Z before this row was drafted, and this trade form (stop, split targets, time stop, invalidation, minimum reward) was never scored; X's standing ledger line marks any later value-area registration pre_seen on those bars; the K = 3 and one-close-acceptance variants are among the printed tables"; items: `research_outputs/tierc12/x_rec/tierc11x/va/two_trades.parquet` (sha256 `a03ef1343cc93c9bc093c4f34960978daac51ca24d5160480546d40bf76f91b0`; detector `va`, trade `swing_failure`, variants `k3` and `die_parity`, lens `4h`); `research_outputs/tierc12/x_rec/tierc11x/va/X3.md`; `research_outputs/tierc12/x_rec/tierc11x/LEANS_X.md:1816-1818, :2468-2470`; `research_outputs/tierc12/DISCLOSURES.md` D-2, D-3.
- **disclosed_beside:** each Tier-E, no verdict word.
  - L-X.14's common leaves: `seed_sens`, `haircut` (the charter twin, TC11 AM-7), `haircut_sens`, `taker_twin` (on this all-taker arm it reads IDENTICAL TO THE RECORD), `taker_twin_haircut`, `tuning_slice`, `holdout_slice`, `loao`, `loao_sens`, `concentration`, `share_x`, `literal_bar`, `exact`, `month_block`, `drop_open`, `strip` (`n` per ridden arm and one pointer); and one leaf `arm__<slug>` per Tier-E arm below — the row's ruler on that arm at the seed of record, an interval and no p, no bar, no word.
  - The holdout slice (contract :74), with the sentence "causal for the tuning-fit T and lookback only; the class was pre_seen; the era of record is the full corridor".
  - `tierE__unfiltered` — the book without the rr-min skip, re-walked with its own one-position sequence (contract :74).
  - `tierE__cell_1d` — the same law on the 1d lens (contract :74); the three era words of the `1d|taker` licence are printed in §0 beside the row, the arm's sidecar carrying pointers and booleans only; where the full-corridor word is not PASS the cell is labelled ERA NOT LICENSED there and its holdout slice is printed first.
  - `tierE__guard_1d` — the 4h book refusing an event when the 1d state at the entry close is accepted against the trade (contract :75).
  - `tierE__maker_conditioned` and `tierE__maker_assumed` — the maker twin (contract :75): maker bps on entry, T1 and T2, taker on the stop, the time stop, the invalidation and the mark; the conditioned arm books only if the first 5m bar after the entry close trades through the entry price by the fill of record (one tick, exact); the number of fills TC11-X's tick-less law would add is printed as a count; the feasibility word of the `4h|maker` pair is printed beside both.
  - `tierE__x_geometry` — the book under TC11-X's geometry law (its fee-band and inverted-targets refusals), re-walked, with the rows that differ from the record listed.
  - `tierE__x_gaplaw` — the book under TC11-X's record gap law (a stop at the stop price through a gap; a target at the better of its level and the open), re-walked, with the rows that differ from the record listed.
  - `research_outputs/tierc12/stage_r/sfp/SFP_EVENTS.parquet` — every swing failure of every ridden book with its disposition (`traded`, `one_position`, `stop_none`, `poc_not_ahead`, `t2_not_ahead`, `rr_min`) and geometry, the flags `t1_void` and `t1_within_fee_band`, and the continuation of each trade open at TC11's pin; counts only for the rivals not carried as books (the entry-time profile; re-entry at an intrabar exit close).
  - Disclosures on the row: the label's text; D-2 and D-3; "T tuning-fit (regime reading; the strict-INSIDE twin is printed in Stage V); in-sample for tuning-era trades"; the lookback label; `n_open_at_w`; the count of rows on which the card's funding ceiling would have bound, with the lineage's booking `tc_series_net_r` filed beside `net_r`; invalidation exits split by whether the accepted edge had moved from the faded one.
- **failure_conditions:** each a fixture leg with its planted mutation.
  - F-SFP [a] three trades hand-walked by the frozen key-order rule — the first POC fill, the first other time-stop exit, the first other stop; every trade when fewer than three exist (plant: T1 from the entry-time profile); [b] the row identities on every arm (plant: the invalidation ignored); [c] one position (plant: an overlapping trade); [d] the scored-window identity of the two rides and the strip, per ridden arm (plant: a T1 fill after TC11's pin on a scored OPEN row); [f] fees, uncapped funding and net (plant: the capped funding booked); [g] the synthetic geometry and same-bar sets (plants: a gap stop booked at the stop price; a target credited above its level; a void T1 refused); [h] the closed row on a planted licence leaf; [i] the guarded twin (plant: the 1d bar still forming read).
  - F-SFP-ASOF on cut tapes and cut filed tables; F-SFP-MIRROR against TC11-X's filed X2 trades under TC11-X's own laws, with the typed call sites of the two switches; F-TRAV (a), (e) (L-V); F-TYPED-FLOW on `sfp.rail_atr`, `sfp.t2_offset_atr`, `sfp.t1_fraction`, `rr_min`, `traverse.4h`.
  - F-FAM (PLANTED), F-REGBOOK, F-KEY, F-BOOT, F-VERDICT, F-SCORE-ANCHOR, F-GRID, F-DET (L-X, L-0); F-VA-PINS (e); F-CLOSURE with the builder in the decision set; F-NOT (no trail, no add, the edge is a VA edge, no 5m signal, no `1w_` column, the licence leg).

---------------------------------------------------------------------------------------------------------------
### 1.5 P-SCALP-3

- **id:** P-SCALP-3
- **family:** SCALPER — the family header is contract :82, "STAGE S · SCALPER FAMILY (m=1, bar 0.10) — exists by
  the "maker" ruling:"; text of record :83-106 (slice sha `fa141ec5…2198`, L-X.17).
- **family_m:** 1 — parsed from :82 by L-X.1's `R_FAM` (group 3); never typed.
- **family_bar:** 0.10 — parsed from :82 (`bar 0.10`, group 4) and asserted equal to q ÷ m with q parsed from :9
  ("bar = 0.10 ÷ m per family"); at m = 1 the bar is on record and does not bind (L-X.8).
- **prior:** 30 — parsed from the text slice's `[30%]` (:83).
- **mechanism:** Inside a 1h value area that the 1h machine reports INSIDE, price that reaches the outer third
  near an edge tends to rotate back toward the POC and the far edge — the "edges respected" leg TC11-X licensed for
  the 1h lens at the maker toll and at no other. A limit resting AT the edge is the only entry that pays the maker
  fee, which is the only toll at which the 1h lens may trade a range. The 5m clock supplies timing and nothing
  else: an EMA cross toward value near the edge, or a failed 5m excursion beyond it. The trade is falsified by 1h
  acceptance beyond the faded edge and is bounded in time by the tuning-fit 1h traverse. The hazard is the fill
  itself — a resting limit is filled preferentially when price is going through it — so the row is judged on the
  book whose fills require a trade-through and is closed if it clears only when a touch is taken as a fill.
- **population:** the five home assets (L-D's home panel), pooled, both directions; lens of the clock 5m, lens of
  the value area 1h, permission from 1h and 4h; era HOLDOUT by the fill bar's close, `ERA_CUT < entry_close_ms`,
  with `ERA_CUT` = `research_outputs/tierc12/x_rec/tierc11x/pins/PINS_X.json["era_cut_ms"]`; scored window per
  O-9: `entry_close_ms ≤ W` and `exit_close_ms ≤ W` with `W` = TC11's pin
  (`research_outputs/tierc11/data/AS_OF_PIN.json["as_of_last_closed_4h_close_ms"]`), a position open at `W` marked
  there as `corridor_end`; the bars in (W, TC12's pin] are the forward strip — ridden for every arm, printed,
  never scored [L-S.25].
- **arms:**
  - `scored` — the THROUGH-TICK book; there is no base arm (the row is ruled vs zero). Decision at a 5m close τ
    on row `k1` of `va_bars_1h` and row `k4` of `va_bars_4h`, the last lens bars with close ≤ τ, read as filed
    [L-S.3]. PERMISSION: 1h `state == INSIDE` and 4h state neither UNDEFINED nor accepted against the direction
    (ACCEPTED_BELOW for a long, ACCEPTED_ABOVE for a short), read once at τ [L-S.4]. SETUP: the 5m close's
    %-of-value against the in-force 1h profile between 0 and 33 inclusive for a long, between 67 and 100 inclusive
    for a short (33 / 67: contract :87; 0 and 100: the edges of value) [L-S.5]. TRIGGER: the engine EMA12 / EMA89
    (:89) of the 5m close crossing in the direction on that bar with the close within 0.25·ATR_1h (:90) of the
    edge on the value side, OR that close back inside value after the previous 5m close beyond the edge; a double
    trigger is a swing failure [L-S.6 … L-S.8]. ORDER: one unit at the edge snapped to the tick grid away from the
    market (a BUY limit floored, a SELL limit ceiled), all geometry frozen at τ; stop by `BK.brk_stop` from the
    limit — 0.5·ATR_1h (:97) beyond the swing failure's deviation extreme (every 5m low / high since the first
    close beyond, the return bar included), else from the limit, railed at 1.0·ATR_1h (:98; so R is exactly
    1.0·ATR_1h on cross orders); T1 = POC and T2 = far edge − 0.25·ATR_1h (:99) on the grid; REFUSED, with the
    first reason that holds, when the stop is undefined (`stop_none`), when T1 is not ahead of the limit
    (`poc_not_ahead`: `d·(n_T1 − n_L) ≤ 0`) or when T2 is not ahead of the limit (`t2_not_ahead`: `d·(n_T2 − n_L) ≤
    0`); T1 void when it lies at or beyond T2, the whole position then exiting at T2; a T1 within the round-trip
    taker fee of the limit is traded as written and flagged; SKIPPED (`rr_min`) iff `d·(T2 − L) / R < 1.5` (:100);
    valid for bars t+1 … t+12 (:92); cancelled at a 1h acceptance on the faded side; one resting order and one
    position per asset, a trigger meanwhile refused, never a replacement [L-S.9 … L-S.14]. FILL: the first valid
    bar with `low < limit − 1 tick` (long; :94) in exact integer ticks, at the limit price; no fill on a
    zero-volume bar [L-S.15]. WALK: on the fill bar the stop is tested and no target credited; then per 5m bar: a
    bar opening at or beyond the stop exits at the open; else the stop, adverse-first, at the stop price; then T1
    (half) at its level; then T2 (the rest) at its level, on the same bar if reached; a target fills by the same
    through-tick rule and books its level with no gap improvement; then at the close the invalidation at a 1h
    acceptance on the faded side, then the time stop at the fill bar + the tuning-fit 1h traverse in 5m bars, then
    the corridor end; no trail, no stop move, no add [L-S.17 … L-S.20]. COST: maker bps on entry, T1, T2; taker on
    stop, time stop, invalidation and mark; interval-sum funding from the fill bar by `BK.account_l`, uncapped (the
    D12 ceiling is a v6-card rule and is not a rule of this trade); `net_r = gross_r − fee_r − funding_r` in R
    [L-S.21].
  - `ladder__touch` — the same simulator with every resting limit filled on a touch (`low ≤ limit` for a long;
    :94), its own order sequence [L-S.15, L-S.16].
  - `ladder__deep` — the same with every resting limit filled only through by `max(0.05·ATR_1h, 1 tick)` (:94-95;
    the floor is ruling O-32's), rounded up to whole ticks and frozen at τ, its own order sequence [L-S.15,
    L-S.16].
  - `tierE__full_corridor` — every row of the `scored` walk with `entry_close_ms ≤ W`, the tuning era included
    [L-S.25].
  - `tierE__panel17` — the `scored` simulator on the seventeen assets of the snapshot, holdout by fill; the five
    home assets' rows equal `scored`'s; the twelve run on the CLASSIC5 lookback and traverse and carry no licence
    (`licence = none — CLASSIC5 word transplanted`) [L-S.26].
  - `tierE__rr_unfiltered` — the `scored` simulator without the reward test and with nothing else removed (the
    three refusals stand), its own order sequence [L-S.12, L-S.26].
  - `tierE__live_edge` — the `scored` simulator in which an order still unfilled and not cancelled at the one 1h
    close inside its window is re-priced for the later bars from the row of that close (limit, stop, targets,
    the refusals and the reward test again; same direction, trigger kind and extreme; the window not extended)
    and is cancelled if the new limit is marketable against that close or the new geometry is refused or
    skipped; everything frozen once filled; its own order sequence [L-S.26].
  - `strip` — for every ridden arm, under the column `arm`, the rows of that arm's second ride with `W <
    entry_close_ms ≤ PIN`; `tierE__full_corridor` shares `scored`'s rows and is not repeated; rows and counts only
    [L-S.25].
  - inputs pinned: Stage V's `va/va_bars_1h.parquet`, `va/va_bars_4h.parquet`, `va/va_events.parquet`,
    `va/VA_MIRROR.json` and `va/TRAVERSE.json`; Stage D's `data/fee_schedule.json`, `data/CONTRACT_SPECS.json` and
    the 5m and funding tapes of its manifest; `tide/tide_bars_4h.parquet` and `tide/breadth_4h.parquet`;
    `scripts/tierc12_rangewalk.py`; `scripts/tierc12_regbook.py` — each held to the sha that the last progress
    record naming it certifies (`tierc12_progress.certified`); X's `tierc11x/exit/build_manifest.json`,
    `tierc11x/sfp/build_manifest.json` and `scripts/tc11x_pct.py` by their `X_REC_MANIFEST.json` rows. A mismatch
    HALTs the stage.
  - VA columns read (declared for F-VA-PINS (e)): from `va_bars_1h`: `close_ms`, `state`, `val`, `poc`, `vah`,
    `atr`, `va_age`; from `va_bars_4h`: `close_ms`, `state`; from `va_events`: `lens`, `kind`, `side`,
    `known_close_ms`, `by`, `bars_out`, `E` (rows selected by the key column `asset`). Read beside, deciding
    nothing: `inside_frozen_only` of `va_bars_1h` (one printed count, L-S.4) and `l_label` of `va_bars_1h` (the
    lookback's label, carried on every order row and in every arm's sidecar `description`, L-S.29). No 12h, 1d or
    1w column.
- **statistic:** mean(`net_r`) of the `scored` book (L-X's common clause).
- **comparison:** vs zero. The bootstrap of record (O-22; L-X.3, L-X.4, L-X.6): whole-asset clusters,
  `tierc5.cluster_boot`, `N_BOOT` draws read from `research_outputs/tierc11/scores/SCORES.json["n_boot"]` (4000 on
  file), the 5th / 95th percentile interval of `tierc5._ci_from`, `p = (#draws ≤ 0 + 1) / (N_BOOT + 1)` as a
  Fraction, seed 20261008 (contract :4) passed explicitly, sensitivity seed 20260816 (`SCORES.json["seed_sens"]`)
  printed beside. The two ladder books are ruled with the same ruler, seed, draws and bar.
- **preconditions:**
  - {record: research_outputs/tierc12/va/VA_MIRROR.json, certified_by: progress/TC12-V.json artifact_shas,
    selector: licence["1h|maker"].by_era["holdout"].would_read, required: "PASS"} — X's filed word for
    POOLED:CLASSIC5 · holdout · va_regime · 1h · maker, mirrored from
    research_outputs/tierc12/x_rec/tierc11x/va/feasibility.parquet (sha256
    ea8573b3240bb1112521c55f0a52ee2ed7156c598b7665685d0b86eefbecb6f0); it is this row's only precondition.
- **verdict_rule:** verdict_of_record = SUPPORTED iff (a) the cluster-90% CI lower bound (the 5th percentile of
  the draws) > 0 AND (b) one-sided p <= q ÷ m, exact, AND (c) every declared asset holds at
  least one row in every arm the ruler reads; else NOT SUPPORTED. m is
  fixed in every case; a registration closed by its precondition prints 'CLOSED BY PRECONDITION (…) — no number ·
  no test spent', spends no test and never loosens the bar. Bootstrap of record: asset-cluster bootstrap by scripts/tierc12_score.py, T5 primitives, N_BOOT 4000, seed 20261008, sensitivity seed 20260816 beside. At m = 1 the bar does not bind and the bar cell prints
  '0.10 (not binding at m = 1; decided at the 5th percentile, clause (a))'. THE PRE-NAMED KILL (L-X.9's table,
  verbatim in content). For each fill book X ∈ {TOUCH, TICK, DEEP}, at the seed of record and this bar, exactly
  one of three states holds: U(X) = X is not PANEL COMPLETE (clause (c) fails on X; its ruler is undefined; an
  EMPTY BOOK is the limiting case); C(X) = X is PANEL COMPLETE and clauses (a) and (b) hold on X; F(X) = X is
  PANEL COMPLETE and (a) or (b) fails on X. D = fewer than 3 of 5 leave-one-asset-out panels of the TICK book
  exclude zero from above (contract :106; L-X.11). A closure word needs a MEASURED failure: a book whose ruler is
  undefined is not a failed book. The ten cases, exhaustive, written TICK · D · DEEP · TOUCH → word, qualifier:
  (1) C · false · C · any → SUPPORTED; (2) C · false · F · any → SUPPORTED, qualifier FILL-SENSITIVE (does not
  clear under DEEP); (3) C · false · U · any → SUPPORTED, qualifier FILL-SENSITIVE (DEEP PANEL INCOMPLETE); (4) C ·
  true · any · any → NOT SUPPORTED, qualifier LOAO BELOW THE LINE (k/N above; passing when dropped: <assets>;
  failing when dropped: <assets>); (5) U · any · any · any → NOT SUPPORTED, qualifiers PANEL INCOMPLETE (…) or
  EMPTY BOOK, and TICK PANEL INCOMPLETE — closure not ruled; (6) F · any · C · any → NOT SUPPORTED; (7) F · any ·
  U · any → NOT SUPPORTED, qualifier DEEP PANEL INCOMPLETE — closure not ruled; (8) F · any · F · C → NOT
  SUPPORTED — CLOSED, qualifier (clears only under TOUCH); (9) F · any · F · U → NOT SUPPORTED — CLOSED, qualifier
  TOUCH PANEL INCOMPLETE — "for good" not ruled; (10) F · any · F · F → NOT SUPPORTED — CLOSED FOR GOOD. The words
  this row can read are exactly five: SUPPORTED, NOT SUPPORTED, NOT SUPPORTED — CLOSED, NOT SUPPORTED — CLOSED
  FOR GOOD, CLOSED BY PRECONDITION. One test is spent, by the TICK book; TOUCH and DEEP are ruled with the same
  ruler, seed, draws and bar and can never produce SUPPORTED. The verdict text is the cell (word, qualifiers,
  label) followed by the fill-sensitivity row, which opens with the fixed sentence "TOUCH and DEEP are fill-model
  twins, not tests: they are ruled at the family bar without a test of their own and can only qualify a SUPPORTED
  cell or choose among the failure words; an interval that excludes zero on either is not a result." and prints
  per fill rule the book's own n, point, interval, p and its state C / F / U, then the two booleans
  fails_under_deep_too = F(TICK) and F(DEEP), and clears_only_under_touch = F(TICK) and F(DEEP) and C(TOUCH);
  then the LOAO line k/N with the fixed sentence "the contract reads one-asset dependence by this line (:106); a
  panel that fails when an asset is DROPPED leans on that asset, a panel that fails while an asset is KEPT is
  dragged by it"; then the single-trade share of record (no threshold; it decides nothing); then the per-order
  ladder counts of the TICK ledger and, where the three books' own n are not ordered, the line
  BOOK-N-NOT-MONOTONE (the books are sequenced separately; their n are not comparable order for order). Printed
  beside the licence word, deciding nothing: the scorer's collared leaf licence_at_maker_pin — the licence row's
  edge leg re-derived at Stage D's pinned maker rate from the columns VA_MIRROR.json quotes, labelled "a
  re-derivation of one leg from printed columns; not a licence"; if its edge_net_h20_at_pin <= 0 the cell carries
  the qualifier LICENCE EDGE ≤ 0 AT THE PINNED MAKER RATE (X assumed <x> bps round trip; pinned <y>), and the row
  is still built, scored, and spends its test. Printed beside, deciding nothing: the sensitivity seed, the haircut
  and all-taker twins and the all-taker haircut twin — with the sentence "No cost twin prices a maker fill's
  adverse selection — a maker leg carries zero slippage in both. The only proxy in this row is the fill ladder
  (TICK against DEEP)." —, the tuning and holdout slices, LOAO, both single-trade shares, the literal-bar column,
  the exact enumeration with SEED-FRAGILE, the month-block twin with TIME-CLUSTER FRAGILE, the drop-OPEN twin with
  VERDICT RESTS ON OPEN MARKS, the forward strip unscored. Tier-E arms carry no verdict word. This registration
  carries pre_seen (KIN-SEEN) and prints '<verdict> — NOT CONFIRMATORY (pre_seen · KIN-SEEN: X3 printed
  value-area swing-failure outcomes on these bars)'.
- **labels:**
  - pre_seen — tag: KIN-SEEN; label: NOT CONFIRMATORY; text: "TC11-X printed outcomes of fading 1h value-area
    edges on these same bars — the 1h maker feasibility row this trade is licensed by (outer 20% of value, H20
    exit, both legs at X's assumed maker toll, holdout) and X3's 1h value-area swing-failure table — while this
    trade form (a resting limit at the 1h edge on the 5m clock, through-tick fill, split targets, taker stop) was
    never scored; X's standing ledger line marks any later value-area registration pre_seen for bars ≤
    2026-09-25T00:00Z and every scored bar of this row is at or before that instant; the feasibility word was
    earned on X's record machine, not on V2 (DISCLOSURES D-2, D-3); the lookback and the traverse are tuning-fit
    and out-of-sample on the holdout."; items:
    `research_outputs/tierc12/x_rec/tierc11x/va/feasibility.parquet` (sha `ea8573b3…b6f0`; row POOLED:CLASSIC5 ·
    holdout · va_regime · 1h · maker), `research_outputs/tierc12/x_rec/tierc11x/va/two_trades.parquet` (sha
    `a03ef134…91b0`; lens 1h, detector va, trade swing_failure), the standing line at :2468-2470 of
    `research_outputs/tierc12/x_rec/tierc11x/LEANS_X.md`, and `research_outputs/tierc12/DISCLOSURES.md` D-2, D-3.
- **disclosed_beside:**
  - `ladder__touch`, `ladder__deep` — the contract's fill-sensitivity row: ruled at the family bar without a test
    of their own, part of the verdict text (L-X.9's named exception to the collar), no verdict word of their own.
  - the all-taker twin `taker_twin_net_r` (the TC-series toll, uncapped funding), with `tc_series_net_r` (the
    lineage's own booking, funding ceiling included) and the count of rows the ceiling binds — Tier-E, no verdict
    word.
  - the charter-slippage twin `haircut_net_r` (AM-7, taker legs only) and `taker_twin_haircut_net_r` (AM-7 on
    every fill of the all-taker twin) — Tier-E, no verdict word.
  - `licence_at_maker_pin` (the licence row's edge leg re-derived at the pinned maker rate from printed columns;
    not a licence) — Tier-E, no verdict word.
  - `tierE__full_corridor` (five home assets, every era inside the scored window; lookback and traverse in-sample
    on its tuning rows), by the leaf `arm__full_corridor` — Tier-E, an interval and no p, no verdict word.
  - `tierE__panel17` (seventeen assets; CLASSIC5 pins transplanted; no licence for the twelve), by the leaf
    `arm__panel17` — Tier-E, an interval and no p, no verdict word.
  - `tierE__rr_unfiltered` (the book without the "rr-min" skip, re-walked), by the leaf `arm__rr_unfiltered` —
    Tier-E, an interval and no p, no verdict word.
  - `tierE__live_edge` (the limit re-priced at the 1h close inside its window), by the leaf `arm__live_edge` —
    Tier-E, an interval and no p, no verdict word.
  - the MISS table and grid (every unfilled order of the scored window; the would-have at the trigger close as a
    taker, at T1, at T2 and split) — Tier-E, no interval, no verdict word, never netted into a book.
  - the per-order ladder counts, the funnel, the regime-column occupancy, the descriptive slices (per asset, per
    direction, per trigger kind, triggers on a 1h close, void T1) and the printed counts (rail binding on cross
    orders, T1 within the fee band, gap stops and gap targets, targets marketable at placement, invalidations by
    moved edge, orders on an hour that is INSIDE by the frozen edge only) — Tier-E, no verdict word.
  - `strip` (every ridden arm's fills after TC11's pin through TC12's) — unscored: n per arm and a pointer only.
  - L-X.14's common set (`seed_sens`, `haircut`, `haircut_sens`, `taker_twin`, `taker_twin_haircut`,
    `tuning_slice`, `holdout_slice`, `loao`, `loao_sens`, `concentration`, `share_x`, `literal_bar`, `exact`,
    `month_block`, `drop_open`, `strip`) — Tier-E, no verdict word.
- **failure_conditions:** F-SCALP [L-S.31], one block per leg, each FAILS IF: [a HAND-3] a rule-chosen trade
  re-derived end to end by independent code differs from production; [b MISS-3] a rule-chosen miss is not a miss
  under an independent bar-by-bar test, or its class or would-have differs; [c LADDER] the per-order inclusion
  TOUCH ⊇ TICK ⊇ DEEP, the fill-bar order or a ledger's four counts fail — an inverted order must FAIL; [d
  TICK-FILL] the snap or a fill test differs from exact rational arithmetic, or a zero-volume bar fills; [e ASOF]
  a boundary read, an act-boundary prefix on cut tapes and cut filed tables, or the W-versus-PIN prefix differs;
  [f FROZEN] a level of an order changes after the trigger; [g GATES · READ-SET] a gate recomputed independently
  differs, or a path outside the declared read set was opened; [h SEQUENCE] two orders or positions overlap, or a
  refusal's reason is not the first that held; [i WALK-TABLE] production differs from the synthetic walk table;
  [j STOP] a stop, R or rail flag differs, or a stop moved; [k RR] the geometry refusals or the reward test
  differ from their law; [l MISS-TABLE] the MISS partition or grid does not re-derive; [m REGIME] a regime stamp
  reads past its as-of bar; [n FLOW] a pin bent at its door moves nothing; [o VIEWS] an arm identity, a label, a
  fill rule or a strip row is wrong; [p GATE] a failed licence word does not close the row. F-TOLL, book half
  [L-S.32]: [book t1] a fee rate is typed; [book t2] the taker twin is not the TC-series toll (a two-case
  identity on the funding ceiling); [book t3] a leg's rate, the fee split, the net law or the uncapped funding
  fails; [book t4] the maker rate bent at its door does not move net_r exactly; [book t5] a haircut law fails —
  with L-D's F-TOLL [data a..g] and [reader]. L-V's F-TRAV [a · tierc12_scalp] and [e · <each arm>] (a typed
  time stop, or a row's T not the pinned traverse), F-VA-PINS [e · P-SCALP-3] (a 1w column read) and F-NEST-ASOF
  [P-SCALP-3__<arm>] (a leaked future profile in a stamp). L-0's F-NOT legs 5M, TRAIL-OFFSET, ADDS, PIVOT-RANGE,
  1W and LICENCE, F-CLOSURE with this builder in the decision set, F-HOOK-ESCAPE, F-WALL, F-TYPED. The common
  F-REGBOOK [P-SCALP-3], F-KEY, F-BOOT, F-VERDICT, F-SCORE-ANCHOR, F-GRID, F-DET, F-COLLAR. Every leg's planted
  mutations are stated in the reading cited; when this row is closed by precondition the real-book legs print
  CLOSED-NO-BOOK P-SCALP-3.

## 2 · The keys of the filing

`REGISTRATIONS.json` — top keys, in this order: `tier` · `contract {path, prefix_bytes, prefix_sha256, n_lines,
whole_file_sha256_at_filing}` · `resume_paste {path, sha256}` · `leans {path, sha256}` · `amendments {path, sha256}` ·
`review {path, sha256}` · `plan {path, sha256}` · `rulings {path, sha256}` · `disclosures {path, sha256}` ·
`families [{family, stage, header_line, header_text, header_text_sha256, m, q, bar, bar_exact, n_registrations}]` ·
`verdict_law {clause_a, clause_b, clause_c, reading, rival}` · `statistics {n_boot, n_boot_source, seed, seed_source,
seed_sens, seed_sens_source}` · `scored_window {end_ms, source}` · `era_cut {ms, source}` · `registrations [5]` ·
`chain [5]` · `head` · `law` · `law_source`.

Each registration body: `registration`, `seq`, `family`, `family_m`, `family_bar`, `prior_pct`, `seed`,
`text_of_record`, `text_lines`, `context_of_record [{lines, text}]`, `external_context [{path, sha256, lines, text}]`
(omitted when empty), `operative_spec {mechanism, population, arms, statistic, comparison, preconditions, labels,
disclosed_beside, failure_conditions}`, `verdict_rule`, `text_sha256`, `sha256`.

- **payload sha** = `sha256(json.dumps(body without text_sha256 and sha256, sort_keys=True, ensure_ascii=False))`
  over the UTF-8 bytes.
- **chain**: for each registration in `seq` order `line = {seq, registration, sha256, prev}` and `line_sha256 =
  sha256(json.dumps(line, sort_keys=True))`; `prev` of the first is the genesis string (the character `0` repeated to
  the length of a sha256 hex digest, that length taken from `hashlib`); `head` = the last `line_sha256`.
- **rendering**: `json.dumps(doc, indent=2, ensure_ascii=False)` and a trailing newline, insertion order, UTF-8; no
  clock, no host, no path outside the repo in any leaf.
- **where the values come from**: `families` — the pin door's parse of the prefix; `statistics.n_boot` and
  `statistics.seed_sens` — `research_outputs/tierc11/scores/SCORES.json` keys `n_boot` and `seed_sens`, the file held
  to the sha `progress/TC12-R0.json` records for it and `n_boot` asserted equal to
  `x_rec/tierc11x/registrations/REGISTRY_PIN_X.json` key `n_boot`; `statistics.seed` — the pin door's `seed`, asserted
  equal to `PROGRESS.json` key `seed`; `scored_window.end_ms` — `research_outputs/tierc11/data/AS_OF_PIN.json` key
  `as_of_last_closed_4h_close_ms`; `era_cut.ms` — `x_rec/tierc11x/pins/PINS_X.json` key `era_cut_ms`; `law` —
  `research_outputs/tierc11/registrations/REGISTRATIONS.json` key `law`, that file pinned by TC11's chain head (its
  `REGISTRY_PIN.json` key `head`, asserted equal to the head recomputed from the payloads) and never by a whole-file
  sha.

`REGISTRY_PIN.json` (sorted keys): `registrations_file {path, bytes, sha256}`, `order_of_filing`, `registry_len`,
`genesis`, `head`, `chain` (the line shas), `registrations {<id>: {seq, sha256, text_sha256, text_lines, prior_pct,
family, family_m, family_bar}}`, `families`, `contract`, `resume_paste`, `leans`, `amendments`, `plan`, `review`,
`rulings`, `disclosures`, `seed`, `seed_sens`, `n_boot`, `law`, `law_source`, `spec_carry_law`, `witness_law`,
`text_before_result_law`, `tier`.

The filing reads the four entries below from this section, verbatim (each on one line):

- `verdict_law` {clause_a: "(a) the cluster-90% CI lower bound (the 5th percentile of the draws) > 0", clause_b: "(b) one-sided p <= q ÷ m, exact", clause_c: "(c) every declared asset holds at least one row in every arm the ruler reads", reading: "L-X.8", rival: "the literal bar alone, p <= the family bar, printed beside as the column literal_bar and deciding nothing"}
- `spec_carry_law`: "each operative_spec is this plan's §1.k block, which is the frozen LEANS's REGISTRATION SPEC block byte for byte; a block is fifteen top-level bullets in this order — id, family, family_m, family_bar, prior, mechanism, population, arms, statistic, comparison, preconditions, verdict_rule, labels, disclosed_beside, failure_conditions; a bullet's wrapped lines are joined by one space and nothing else changes (markdown kept); one level of sub-bullets is a list, and a bullet with both a head and sub-bullets is {text, items}; the five checked fields file the text up to the first space as body keys (family_m and prior as integers), verdict_rule is a body key, and the other nine fields are the operative_spec; the blank lines and the trailing rule line of the frozen text carry nothing"
- `witness_law`: "research_outputs/tierc12/registrations/ is tracked (the nested .gitignore excludes only parquet, _det_*/ and x_rec/**), so the one commit tierc12(TC12-REG) witnesses REGISTRATIONS.json and REGISTRY_PIN.json; both are created by exclusive create and are never overwritten; the scorer's first act is verify_filing — the contract's prefix, every slice, every payload sha, the chain and this head — before any number"
- `text_before_result_law`: "(1) write-once — --file HALTs if either file exists and creates both by exclusive create; (2) the head and the filing's sha are stamped into every regbook STATUS, arm sidecar and book manifest as registry_head and registrations_sha256, and the scorer HALTs a row (HEAD-STAMP) that lacks them or carries other values; (3) a git-order attestation keyed on TC12's own paths — ATTEST-REG at filing (the disk walk under research_outputs/tierc12/ holds no file outside PRE_REG ∪ REG_SET, no parquet outside x_rec/, and no tierc12 script outside the typed set) and ATTEST-ORDER at TC12-SCORE, at CLOSE and in close_acts.sh step 0 (the commit that adds REGISTRATIONS.json adds exactly REG_SET, and every other tracked TC12 path is first added by a proper descendant of it)"
