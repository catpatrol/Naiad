# U8 · THE FORWARD LEDGER, THE ERA TABLES AND THE FERRY (TC12 STAGE L) — scout map

Scout: read-only. Contract read: `scratchpad/tc12/2026-10-08_TC12_APOLLO.md` sha256
`861d6050e80e66995e4f9db2855aaf274d63285249c2549e5a0813582095a7bd` (137 lines, 12,209 B); the same bytes are filed at
`/Users/luis/Naiad/exchange/queue/2026-10-08_TC12_APOLLO.md` (same sha), committed as main `28e006b` ("tierc12(STEP Q)",
commit time 2026-10-08T19:52:13-03:00 = 22:52:13Z).

Trees as measured at this scout's run (2026-10-08T22:58Z):
- MAIN `/Users/luis/Naiad`, branch `v12-v1-census`, HEAD `28e006bc5def421bd65e3835a95a2905c4e21b93`. (It was `a399b47` at the
  session's git snapshot and moved to `28e006b` while this scout ran: the STEP Q commit.)
  Dirty: ` M exchange/status/daily/DAILY_2026-10-08.md`, ` M research_outputs/tierc10/close/FIXTURES_CLOSE_ledger_append_root.txt`,
  plus untracked pine/ and html files. Index clean.
- X `/Users/luis/Naiad/.claude/worktrees/tierc11x`, branch `tierc11x`, HEAD `7b24f835bcbf7430eb0f97b6c39b6b1b233eef11`
  (== CERTIFIED tip); only `?? research_outputs/tierc11x/close/CERTIFIED_TIP`. Merge base with main: `e97ad7390c6212273b0e06daf33a463d4106c9d1`.

Abbreviations: M: = `/Users/luis/Naiad/`, X: = `/Users/luis/Naiad/.claude/worktrees/tierc11x/`.

---------------------------------------------------------------------------------------------------------------
## 1 · FACTS

### 1.1 There are TWO forward ledgers on disk, under TWO chain laws; neither holds a row

| | TC11's ledger (base v6 + 9/12, OF RECORD for those two) | X's ledger (base twin + 9/12 twin + OLD-gated OF RECORD) |
|---|---|---|
| path | `M:research_outputs/tierc11/forward/FORWARD_LEDGER.jsonl` (tracked on v12-v1-census) | `X:research_outputs/tierc11x/forward/FORWARD_LEDGER.jsonl` (tracked on tierc11x ONLY; not in main) |
| bytes · sha256 | 3,442 B · `e53328add9e71f1c6198f724a131565a2a10ad2ad1600c36a74c6676f7ada288` | 5,643 B · `4a6da7e89a3cf5f0127f76aca0d2ae12d218ffc06417c6528c70210092cfa4c5` |
| lines | 2: `GENESIS` (seq 0), `REFRESH` (seq 1) | 4: `book_open` ×3 (v6, trg912, gated-v6-oldtide), `refresh` ×1 |
| line kinds | `GENESIS` / `CAMPAIGN` / `REFRESH` (tierc11_forward_ledger.py:31-34) | `book_open` / `refresh` / `row` (tc11x_forward.py:136) |
| chain fields | `seq`, `prev`, `line_sha256` | `prev_sha256`, `entry_sha256` (tc11x_forward.py:137) |
| hash law | `line_sha256 = sha256(canonical(line without line_sha256))`, the line INCLUDING `prev` (tierc11_forward_ledger.py:133-138) | `entry_sha256 = sha256(forward_log.canonical(line) + prev)`; canonical strips only `entry_sha256` (forward_log.py:67-82) |
| canonical | `json.dumps(sort_keys=True, separators=(",",":"), ensure_ascii=False, allow_nan=False)` (tierc11_forward_ledger.py:128-130) | same dumps WITHOUT `allow_nan=False` (forward_log.py:75-76) |
| bytes on disk | each line == its canonical compact JSON (verify_chain asserts it, :161) | each line == `json.dumps(entry, sort_keys=True, ensure_ascii=False)` — DEFAULT separators `", "` / `": "` (forward_log.py:165) |
| genesis | 64 zeros (`ZERO`, :89) | 64 zeros (`FL.GENESIS`, forward_log.py:52) |
| head | `0db889425ef8e3d2075a2a3cf2d1b500c3b0bbc7f7b4d535ffa3dec3575261cb` | `61ea177fadcc82bad06f4744305b88476e29d801829cdfacc4817878306cd89c` |
| writer | whole file re-written to `.tmp` then `os.replace` (atomic; :409-411); `body.startswith(raw)` asserted (:406) | `forward_log.append_entry`: `open("a")` append, refuses a stale prev or a wrong sha (forward_log.py:152-166) |
| frozen-book record | GENESIS `books.{v6,trg912}` = `{card:"Card:v6-control", roles:{…}, path}` — NO parameter hash; GENESIS line sha `b68a4942b35f6599f8783b02d20dfafc3a72052e88dfaf22055e003b2a105c56` | `BOOK_SPECS.json` (one doc for all three books) sha `72a1f52359c66084d22f8bc99b0cd35e7edd89db2751f4859f559c8b1f51cac3`, named by every `book_open` line |
| report | `FORWARD_LEDGER.md` 2,981 B sha `52e839001f7ad6f1e13533a6d6745488dc587d11db25c3bfe6b0de66823413ec` | `FORWARD_LEDGER.md` 12,475 B sha `64d4529670d1fcc730b194f2e7d885df05f7fb004c9dc45c0cec3b5656eb6572` |
| producer | `M:scripts/tierc11_forward_ledger.py` sha `e33a75fa17971e71f76cc6318ccc88aed74067fd69bfdcc77c5433fcaf3dadfa` (569 lines) | `X:scripts/tc11x_forward.py` sha `33f65b5eca8e50dfce6690bb827270f7de1cf7207ef14245416210ce88bbe80b` (1,148 lines) |
| certified by | TC11 PROGRESS stage `TC11-T-RELAY` COMPLETE-VERIFIED names jsonl `e53328ad…` (3,442 B), md `52e83900…`, script `e33a75fa…` (M:research_outputs/tierc11/PROGRESS.json, stages[].artifact_shas) | X commit 7b24f83; fixtures `X:…/forward/FIXTURES_X5.txt` sha `fa7d4084af6cbb5ff4e42cdda8e1b589c3feed025e73dd608eb3f31ac99de001` ("10 GREEN, 0 RED") |

The schema difference is a KNOWN, FILED finding: AM-X9 (X:research_outputs/tierc11x/LEANS_X_AMENDMENTS.md:189-205): "TC11's ledger
chains on `prev` / `line_sha256` with kinds GENESIS / CAMPAIGN / REFRESH. X's chains on forward_log's `prev_sha256` /
`entry_sha256` with kinds book_open / refresh / row." Twin comparison "NOT LIVE" while both hold 0 rows; option (a) — verify TC11's
ledger by its own law and map CAMPAIGN lines to CTRL_COLS by a declared field map — is "Owed … at the first landing at which
either side holds rows", carried to CLOSE as a finding-not-fixed. LX-X5.4 (X:…/LEANS_X.md:2076-2079) also records why the two
laws cannot be mixed: under forward_log's canonical a field named `line_sha256` "would have been hashed into its own digest …
and could never verify".

`scripts/forward_log.py` is byte-identical in both trees: sha `74e9657fbcf26cce3040ee52d28a96bc1cf60897e375ba26a09b2e13676e1967`
(329 lines). It has no env/substrate dependency (path-parameterised functions).

### 1.2 TC11's ledger, WHOLE (`M:research_outputs/tierc11/forward/FORWARD_LEDGER.jsonl`, 2 lines)

```
{"books":{"trg912":{"card":"Card:v6-control","path":"tierc11_books.trg912_book (T9.replay9)","roles":{"name":"trigger-9/12","tide_f":89,"tide_s":316,"trg_f":9,"trg_s":12,"win_f":12,"win_s":89}},"v6":{"card":"Card:v6-control","path":"tierc11_books.v6_book (TP.run_cell_n)","roles":{"name":"v6-roles","tide_f":89,"tide_s":316,"trg_f":12,"trg_s":26,"win_f":12,"win_s":89}}},"kind":"GENESIS","law":["L-T.6: opens 2026-09-21T16:00:00Z; admits only campaigns whose entry close is > the opening; appends a campaign exactly once, when closed (exit_reason != corridor_end); OPEN campaigns are listed, never appended or counted; a refresh re-rides both frozen books over the whole tape to its pin on the F-CTRL code path and HALTs if any appended row changes; n per book; UNSCORED until n >= 30 per book.","Every v6 row stamps the P-AGE-1 trailing band (B4 OLD refused) and the P-WIN-1 lag (>= 16 refused; 7-15 shadow).","Chain: line_sha256 = sha256(canonical JSON of the line without line_sha256); prev = the previous line's line_sha256 (genesis: 64 zeros); canonical = sort_keys, separators (',', ':'), ensure_ascii False, allow_nan False."],"ledger":"FORWARD LEDGER","line_sha256":"b68a4942b35f6599f8783b02d20dfafc3a72052e88dfaf22055e003b2a105c56","n_score":30,"opening_iso":"2026-09-21T16:00:00Z","opening_ms":1790006400000,"panel":["BTCUSDT","ETHUSDT","SOLUSDT","NEARUSDT","ZECUSDT"],"prev":"0000000000000000000000000000000000000000000000000000000000000000","seq":0,"tier":"TIER-C11"}
{"books":{"trg912":{"appended_now":[],"book_sha":"2c32fd60924336acc7c48852143d47661a5eb83f12c047ac8b041ad90046e030","continuations_not_admitted":[],"n_appended_total":0,"n_rode":199,"open":[{"direction":1,"entry_close_ms":1790280000000,"exit_reason":"corridor_end","key":["SOLUSDT",1790265600000],"net_r_marked_to_pin":-0.03145186341885717}],"status":"UNSCORED (n 0 < 30)"},"v6":{"appended_now":[],"book_sha":"f3c68f544bcda52c909374105dabbdc773c9bffa4b66b2ef7e0f35ac9b369132","continuations_not_admitted":[{"direction":1,"entry_close_ms":1789732800000,"exit_reason":"stop","key":["ETHUSDT",1789718400000],"net_r":2.7071804854309196}],"n_appended_total":0,"n_rode":200,"open":[],"status":"UNSCORED (n 0 < 30)"}},"corridor_lo_ms":1567958400000,"input_sha":{"funding/BTCUSDT.parquet":"a3d21e1f1a78930b9ca27132d4973f4f4cd4d3ab0639d33d949f25ad8722a77b","funding/ETHUSDT.parquet":"31120f82bd515bf664acedacfa86cb0867d309686c2db508f4977edf981767ed","funding/NEARUSDT.parquet":"593ac29381ca6c6432d3ce59f3134de000c7a1a428286a832835733b09adad50","funding/SOLUSDT.parquet":"63f3b205c1a88345c9c72bd4d9694b6349b069ce0ebbff93badebb9eabc37f8d","funding/ZECUSDT.parquet":"19a0080a11c5b3194a7be1a01e61f0f5ae244fc26be9a0e848dfcbeb7c6fa700","klines/BTCUSDT_4h.parquet":"281c3ac3195e5bb8de6b211573f77919bb2af2a342f71162426085f54bf37bfb","klines/ETHUSDT_4h.parquet":"e78895774de7d30ae06528060d97896a846975e26e1ceb7bdc6245ef70993fab","klines/NEARUSDT_4h.parquet":"e3fdd23041ffcdd3a55a8c24c9473389051d2c95d20a8c2d1fcb136144d04098","klines/SOLUSDT_4h.parquet":"6dfc049478f6e5fb8752c6211ebbda3b0c222afd95933d13b12b4d63e541d021","klines/ZECUSDT_4h.parquet":"1e054d71061f18be429907a0331eb43eb1aa26fa511ca01af581f428b8844935"},"kind":"REFRESH","line_sha256":"0db889425ef8e3d2075a2a3cf2d1b500c3b0bbc7f7b4d535ffa3dec3575261cb","pin_iso":"2026-09-25T00:00:00Z","pin_ms":1790294400000,"prev":"b68a4942b35f6599f8783b02d20dfafc3a72052e88dfaf22055e003b2a105c56","seq":1,"snapshot":"tc11_20260925"}
```

Read-off (line 1 GENESIS): `opening_ms 1790006400000` / `opening_iso 2026-09-21T16:00:00Z`; `n_score 30`; `panel
[BTCUSDT, ETHUSDT, SOLUSDT, NEARUSDT, ZECUSDT]`; `tier TIER-C11`; books `v6` = roles `{name v6-roles, tide_f 89, tide_s 316,
trg_f 12, trg_s 26, win_f 12, win_s 89}`, `trg912` = `{name trigger-9/12, … trg_f 9, trg_s 12 …}`, both `card Card:v6-control`.
(line 2 REFRESH): `pin_iso 2026-09-25T00:00:00Z` (`pin_ms 1790294400000`), `snapshot tc11_20260925`, `corridor_lo_ms
1567958400000`; v6: `n_rode 200`, `book_sha f3c68f544bcda52c909374105dabbdc773c9bffa4b66b2ef7e0f35ac9b369132`,
`n_appended_total 0`, `open []`, `continuations_not_admitted` = ETHUSDT long key `[ETHUSDT, 1789718400000]` (entered bar open
2026-09-18T08:00Z, entry_close_ms 1789732800000, exit_reason stop, net_r 2.7071804854309196), status `UNSCORED (n 0 < 30)`;
trg912: `n_rode 199`, `book_sha 2c32fd60924336acc7c48852143d47661a5eb83f12c047ac8b041ad90046e030`, `n_appended_total 0`,
`open` = SOLUSDT long key `[SOLUSDT, 1790265600000]` (bar open 2026-09-24T16:00Z, entry_close_ms 1790280000000,
exit_reason corridor_end, net_r_marked_to_pin -0.03145186341885717), status `UNSCORED (n 0 < 30)`; `input_sha` = the 5 funding
+ 5 4h-kline parquet shas of tc11_20260925.

### 1.3 X's ledger, WHOLE (`X:research_outputs/tierc11x/forward/FORWARD_LEDGER.jsonl`, 4 lines)

```
{"book": "v6", "entry_sha256": "7f33aee65a9d82f833f1d1a7175e7d9318fe0a7c9fc687d789e57e87e1223062", "kind": "book_open", "n_min": 30, "opening_iso": "2026-09-21T16:00:00Z", "opening_ms": 1790006400000, "prev_sha256": "0000000000000000000000000000000000000000000000000000000000000000", "role": "X twin — TC11's ledger not yet opened", "scored": false, "spec_sha256": "72a1f52359c66084d22f8bc99b0cd35e7edd89db2751f4859f559c8b1f51cac3", "tier": "TIER-C11-X"}
{"book": "trg912", "entry_sha256": "2fab0eb76232a74bc43bd362e6a8f9761ceb9659c8eb86f29eb07bbd1474aac1", "kind": "book_open", "n_min": 30, "opening_iso": "2026-09-21T16:00:00Z", "opening_ms": 1790006400000, "prev_sha256": "7f33aee65a9d82f833f1d1a7175e7d9318fe0a7c9fc687d789e57e87e1223062", "role": "X twin — TC11's ledger not yet opened", "scored": false, "spec_sha256": "72a1f52359c66084d22f8bc99b0cd35e7edd89db2751f4859f559c8b1f51cac3", "tier": "TIER-C11-X"}
{"book": "gated-v6-oldtide", "entry_sha256": "f747d827ab6d984da0480268057597321f085b77c466a8cfc7ddfcce70b7d273", "kind": "book_open", "n_min": 30, "opening_iso": "2026-09-21T16:00:00Z", "opening_ms": 1790006400000, "prev_sha256": "2fab0eb76232a74bc43bd362e6a8f9761ceb9659c8eb86f29eb07bbd1474aac1", "role": "of record", "scored": false, "spec_sha256": "72a1f52359c66084d22f8bc99b0cd35e7edd89db2751f4859f559c8b1f51cac3", "tier": "TIER-C11-X"}
{"anchor_x_found_books": {"book_sha": {"trg912": "2c32fd60924336acc7c48852143d47661a5eb83f12c047ac8b041ad90046e030", "v6": "f3c68f544bcda52c909374105dabbdc773c9bffa4b66b2ef7e0f35ac9b369132"}, "held": true}, "as_of": {"as_of_last_closed_4h": "2026-09-25T00:00:00Z", "as_of_last_closed_bar": "2026-09-25T00:00:00Z", "as_of_lens": "4h", "as_of_n_assets": 5, "as_of_panel": "CLASSIC5", "as_of_panel_start": "2019-09-08T16:00:00Z", "as_of_span_days": 2573.3, "as_of_substrate": "tc11_20260925", "warranty": "these numbers are true AS OF the corridor named in this row and of no other; the corridor advances with the cache [TC6V-a]"}, "books": {"gated-v6-oldtide": {"appended_keys_this_refresh": [], "n_appended": 0, "n_appended_this_refresh": 0, "n_min": 30, "n_open": 0, "open_keys": [], "refused_keys": [], "rival_absolute_refused_keys": [], "rival_arm_age_gt_cut_keys": [], "scored": false}, "trg912": {"appended_keys_this_refresh": [], "n_appended": 0, "n_appended_this_refresh": 0, "n_min": 30, "n_open": 1, "open_keys": [["SOLUSDT", 1790265600000]], "scored": false}, "v6": {"appended_keys_this_refresh": [], "n_appended": 0, "n_appended_this_refresh": 0, "n_min": 30, "n_open": 0, "open_keys": [], "scored": false}}, "code_drift_vs_spec": [], "code_shas": {"engine/indicators.py": "91805c04130c3701e16f933b4c4ac258109f8636d9cd8a0ae44787d86f13c113", "engine/s1.py": "eb15690da648c62c96c705f232064086cca931117bfeb5fe0190542d1c5b3e06", "scripts/forward_log.py": "74e9657fbcf26cce3040ee52d28a96bc1cf60897e375ba26a09b2e13676e1967", "scripts/tc11x_books.py": "26870ff97317801fdf9c4874e1f41cdac69bacbf9263198e623e19ab19913b2b", "scripts/tc11x_env.py": "db74225e6fa26bf7e9c2e19f31b6e0c76b379a8de72ef4c0cc9e6b1a2e653928", "scripts/tc11x_forward.py": "33f65b5eca8e50dfce6690bb827270f7de1cf7207ef14245416210ce88bbe80b", "scripts/tierc10_data.py": "2cbf9bb6bcfea3ec6184d5502ba5c530f5c0089d95288ab848a745ad5b3015fc", "scripts/tierc10_panel.py": "40b660cdc943a947f199f2e59f38bfbda04866b44191506de2298d8474d79b0e", "scripts/tierc2_baseline.py": "682044305a9e80695e95c710cfb053ec146a7c40755841bb083748da62ca04c5", "scripts/tierc2_rules.py": "1739b4006b6a01296bb0b9f6bd8b6c22e546b09d5fa3b47b175545156b12fc2a", "scripts/tierc3_rules.py": "c61a9679a369c75a94b4c1ed27c19cc394de7a07f891e16fd80d2309d61a0d6d", "scripts/tierc4_rules.py": "3e56420575d1d87ce92672c471d0a866aef29ff5de625f9d3844ac24426fb9ee", "scripts/tierc5.py": "ad912b385cc8dd2e5291af3b79c520760ae8c91764af8e3eee56c6b3dd295a6f", "scripts/tierc5_rules.py": "c27a5ecb425f0247adbd59fa921e8637900523714eafa69aa5d9453d875a1515", "scripts/tierc6.py": "429f6849708d2f2bee5ec1a74829f09792b0483cb1a80d920f821cd998ceae8e", "scripts/tierc6_rules.py": "777700d42258cbdf4cf7895a8c42d3a092dd46f0a79545de17b8c79496b88d5f", "scripts/tierc7.py": "6abeaf6e662e9a61c1be73ee21f900133869432d7006cbe1b352b9a0f6ef1452", "scripts/tierc7_lab_regime.py": "4d19cf0095ebf2593b3008caf9c9af032a75515dda8507da5154308e977682a5", "scripts/tierc7_rules.py": "fa7d8d4804c82ea6247343a80bbd6d784ba48a60908c2c0efe7912e7495b2092", "scripts/tierc8.py": "148e9a975af75ad4370580d168ff616e3abab18d9f522c91c77dffd7f737cfe0", "scripts/tierc9.py": "663eef3107909221a6a651343363bad5c7d7730dd9adb92495d3f1e262c5b3c3"}, "entry_sha256": "61ea177fadcc82bad06f4744305b88476e29d801829cdfacc4817878306cd89c", "kind": "refresh", "n_reride_differs": 0, "n_reride_differs_whole_tape": 0, "opening_ms": 1790006400000, "opening_rival": {"books": {"gated-v6-oldtide": {"n_closed_admitted": 0, "open_keys": []}, "trg912": {"n_closed_admitted": 0, "open_keys": []}, "v6": {"n_closed_admitted": 0, "open_keys": []}}, "opening_ms": 1790294400000}, "pin_iso": "2026-09-25T00:00:00Z", "pin_ms": 1790294400000, "pool_lo_ms": 1567958400000, "prev_sha256": "f747d827ab6d984da0480268057597321f085b77c466a8cfc7ddfcce70b7d273", "snapshot": {"stage_d_manifest": "research_outputs/tierc11x/data/tc11_rec/data/STAGE_D_MANIFEST.json", "stage_d_manifest_sha256": "0d8da58739bddcbf8c5243ef05bda67151a7b4d3957e10af28a8506c8d0ec712", "substrate": "tc11_20260925", "substrate_verify": "research_outputs/tierc11x/data/SUBSTRATE_VERIFY.json", "substrate_verify_sha256": "f0b450da903632e253fec4ba7031320c5989dd0508dbc4002ea3434629e5d453"}, "spec_sha256": "72a1f52359c66084d22f8bc99b0cd35e7edd89db2751f4859f559c8b1f51cac3"}
```

Read-off: lines 1-3 `book_open` for `v6` (entry_sha `7f33aee65a9d82f833f1d1a7175e7d9318fe0a7c9fc687d789e57e87e1223062`, role
"X twin — TC11's ledger not yet opened"), `trg912` (`2fab0eb76232a74bc43bd362e6a8f9761ceb9659c8eb86f29eb07bbd1474aac1`, same
role), `gated-v6-oldtide` (`f747d827ab6d984da0480268057597321f085b77c466a8cfc7ddfcce70b7d273`, role "of record"); each:
`n_min 30`, `opening_ms 1790006400000`, `scored false`, `spec_sha256 72a1f523…`, `tier TIER-C11-X`. Line 4 `refresh`:
`pin_ms 1790294400000`, `pool_lo_ms 1567958400000`, `anchor_x_found_books.held true` with the SAME two book shas as TC11's
REFRESH line (v6 `f3c68f54…`, trg912 `2c32fd60…`), `n_reride_differs 0`, `n_reride_differs_whole_tape 0`, per book
`n_appended 0`; `trg912.open_keys [[SOLUSDT, 1790265600000]]`; gated `refused_keys []`; `code_shas` of 21 path modules;
`code_drift_vs_spec []`; `opening_rival.opening_ms 1790294400000` (TC11's pin) with 0 closed admitted in every book.

### 1.4 What a "frozen book" is, on disk

There is NO per-book "parameter hash" on disk. What exists:
- **Card id**: `card_name "v6-control"` (`TP.CONTROL_CARD = T8.Card(name="v6-control")`, M:scripts/tierc10_panel.py:816) + a roles
  name: `v6-roles` (`T9.V6_ROLES`) or `trigger-9/12` (`T9.SWEEP_CELLS[-1]`, proven by `tierc11_books.r912()`,
  M:scripts/tierc11_books.py:270-279).
- **Parameters**: `ride_spec = TP.ride_spec(card, roles)` (M:scripts/tierc10_panel.py:874) = card class + every card field as a
  repr string + roles fields; filed per book in `X:…/forward/BOOK_SPECS.json` → `books.<id>.ride_spec`
  (e.g. `trail_arm_after_r "1.0"`, `harvest_frac "0.5"`, `anchor_offset "0.5"`, `trail_l "2"`, `trail_r "2"`, `entry_rail_atr "1.0"`).
- **Gate** (third book only): `books.gated-v6-oldtide.gate` = `{kind: "admission gate, POST-FILTER (TC11 L-1.5) …",
  text_of_record: <P-AGE-1 operative_spec.scored_arm verbatim>, registrations_sha256 648834bf30e20e92713bddef2374ddef1aae843f4d8ba152fc50166c8cc6f1ee,
  p_age_1_payload_sha256 e01a89ea7e6fda864f7002a450abd1a4e92424c44d1a9626f6641814e7d35879, base_book "v6",
  refuse "tide_band == 'B4' …", none_band "HALT", lineage_functions [tierc7_lab_regime.tide_streak, tierc9._trailing_pool,
  tierc9._trailing_edges, tierc7_lab_regime._streak_band], band_quantiles [0.25,0.5,0.75], min_pool_bars 30,
  pool_lo_ms 1567958400000, stamps_only {absolute_cut 206, arm_bar_age}}`.
- **The hash that freezes it**: ONE sha for the whole spec document (`spec_sha256 72a1f523…`), covering all three books, the
  opening, `n_min`, `row_fields`, `ctrl_cols`, the chain law, the X-FOUND book shas and the 21 `path_modules` shas
  (tc11x_forward.py:324-406). Write-once: `freeze_spec` HALTs `FWD-SPEC-FROZEN` if a rebuild differs by a byte — "a changed
  module or text needs an AMENDMENT and a re-opened ledger" (tc11x_forward.py:696-709).
- **Freeze record**: the `book_open` line (one per book, chained from GENESIS): `{book, role, spec_sha256, opening_ms,
  opening_iso, n_min, scored:false, tier}` (tc11x_forward.py:610-613). X's own verifier forbids a 4th: "book_open line(s) after
  the opening block" is a `FWD-CHAIN` finding (tc11x_forward.py:636-638), and the first lines must be exactly one book_open
  per book of `BOOK_ORDER = (v6, trg912, gated-v6-oldtide)` (:131, :633-635).
- **Outcome anchor** (not a parameter hash): `book_sha = TP._book_sha(book)` = sha256 of the sorted
  `[symbol, lane, entry_ms, repr(net_r)]` rows (M:scripts/tierc10_panel.py:1988-1995). At TC11's pin: v6 `f3c68f54…` (200
  campaigns), 9/12 `2c32fd60…` (199) — the SAME values in both ledgers.
- TC11's own freeze = the GENESIS line (books + law + opening), sha `b68a4942…`.

The 21 `path_modules` of X's spec: the 18 lineage files (`engine/indicators.py`, `engine/s1.py`, `scripts/forward_log.py`,
`scripts/tierc10_data.py`, `scripts/tierc10_panel.py`, `scripts/tierc2_baseline.py`, `scripts/tierc2_rules.py`,
`scripts/tierc3_rules.py`, `scripts/tierc4_rules.py`, `scripts/tierc5.py`, `scripts/tierc5_rules.py`, `scripts/tierc6.py`,
`scripts/tierc6_rules.py`, `scripts/tierc7.py`, `scripts/tierc7_lab_regime.py`, `scripts/tierc7_rules.py`, `scripts/tierc8.py`,
`scripts/tierc9.py`) are BYTE-IDENTICAL in the main tree today (18/18 shas equal, measured here against
`BOOK_SPECS.json → path_modules`); the other 3 (`scripts/tc11x_books.py`, `scripts/tc11x_env.py`, `scripts/tc11x_forward.py`)
do not exist in main.

### 1.5 The three existing books and where each lives

| contract word | book id on disk | definition | ledger OF RECORD | also |
|---|---|---|---|---|
| base v6 | `v6` | `TP.run_cell_n(TP.CONTROL_CARD, T9.V6_ROLES, CLASSIC5, lo, hi)` (tierc11_books.py:289-291) | MAIN: TC11's ledger (GENESIS `books.v6`) | X twin (book_open `7f33aee6…`) |
| 9/12 | `trg912` | `T9.replay9(s, TP.CONTROL_CARD, T9.SWEEP_CELLS[-1], lo, hi)` per CLASSIC5 asset (tierc11_books.py:294-303) | MAIN: TC11's ledger (GENESIS `books.trg912`) | X twin (book_open `2fab0eb7…`) |
| OLD-gated | `gated-v6-oldtide` | the v6 ride POST-FILTERED: minus rows with `tide_band == "B4"` (tc11x_forward.py:548-559) | X WORKTREE ONLY: X's ledger (book_open `f747d827…`) | — (nothing in main) |

`research_outputs/tierc11x/` does NOT exist in the main tree, and none of the 161 paths X's merge adds (112 under
`research_outputs/tierc11x/`, 33 `scripts/tc11x_*`, 15 `exchange/rows/…`, 1 `exchange/queue/2026-09-25_TC11X_APOLLO.md`)
exists in main today (checked path by path).
TRAP: the X worktree carries its OWN stale checkout of `research_outputs/tierc11/` (26 tracked files at the merge base e97ad73,
no `forward/`); X's env refuses it as "SUPERSEDED" (X:scripts/tc11x_env.py:239, :1363). TC11 records must be read from MAIN.

### 1.6 The forward origin 2026-09-21T16:00Z — why that instant

- It is **TC10's pin**: `M:research_outputs/tierc10/STEP0_RECORD.json` keys `as_of_last_closed_4h = "2026-09-21T16:00:00Z"`,
  `as_of_last_closed_4h_close_ms = 1790006400000` (file sha `3801e1c72149851de37b12775fe77f103fc47ab3fb1f08349dcbce709a97b5aa`).
- TC11 L-T.6 (M:research_outputs/tierc11/LEANS.md:430-431, file sha `655e1605165e7a66c67f544e5cda421b46aa0b6fcd4cb97a6ad19654479f294f`):
  "It opens at **2026-09-21T16:00:00Z** (TC10's pin), after which both frozen books are unseen."
- Typed in TC11's code: `OPENING_MS = 1_790_006_400_000` (tierc11_forward_ledger.py:80), `TC10_PIN_MS` (tierc11_books.py:151;
  tierc11_env.py:124). X reads it BY OBJECT, never typed: `opening_of_record()` = `B.tc10_pin()` (STEP0_RECORD.json) asserted
  equal to the regex-read L-T.6 text and to `E.TC10_PIN_MS` (tc11x_forward.py:200-222).
- LX-X5.2's reasons (X:…/LEANS_X.md:2036-2045): (i) one identical forward window for all books; (ii) "The gated arm is `pre_seen`
  on the corridor up to TC10's pin, which is exactly TC11's opening"; (iii) "No v6 campaign has an entry close in
  (2026-09-21T16:00Z, 2026-09-25T00:00Z], and the 9/12 book has 1, SOL, still OPEN" — costless, not informed by a forward
  result. Rival printed beside: TC11's pin 2026-09-25T00:00Z (identical membership then).
- It is also the END of TC10's forward strip (`M:research_outputs/tierc10/close/FORWARD_STRIP.md:10`: "this corridor's end …
  2026-09-21T16:00:00Z (last closed 4h bar, close ms 1790006400000)").
- 4h bars after the opening: 20 to TC11's pin (`AS_OF_PIN.json` `bars_4h_past_tc10_pin 20`); 103 to 2026-10-08T20:00Z
  (ms 1791489600000) / 104 to 2026-10-09T00:00Z (ms 1791504000000) — COMPUTED here, to be read from TC12's own pin record.

### 1.7 Rows appended so far, and through which bar

- **Zero rows in both ledgers.** Last (only) refresh pin in both: `2026-09-25T00:00:00Z` (ms 1790294400000) = the close of the 4h
  bar opening 2026-09-24T20:00Z (`M:research_outputs/tierc11/data/AS_OF_PIN.json` `as_of_last_closed_4h_open "2026-09-24T20:00:00Z"`).
- Listed, never counted: v6 CONTINUATION ETHUSDT long (entered 2026-09-18T08:00Z, stop, +2.707180 R — it is TC10's strip row
  "OPEN-AT-CORRIDOR-END … 3.642965" at FORWARD_STRIP.md:34, closed between the two pins); 9/12 OPEN SOLUSDT long (entered
  2026-09-24T16:00Z, marked −0.031452 at the pin). The SOL campaign is admitted (entry close 20:00Z > the opening) and is the
  one row certain to be decided at TC12's refresh (appended iff closed by TC12's pin).
- No snapshot past TC11's pin exists: `~/.cache/naiad/snapshots/` holds only `tc10_20260921` and `tc11_20260925`; the live
  cache's BTCUSDT_4h ends at open 2026-09-23T12:00Z (15,432 rows) — BEHIND the TC11 snapshot (15,440 rows, last open
  2026-09-24T20:00Z). Nothing about the forward window after 2026-09-25T00:00Z is on this disk.

### 1.8 The refresh law (how a forward re-ride is computed) — identical in both scripts

1. **Whole-tape re-ride, never "new bars only"**: `books_at(pin)` rides bar 0 → pin (`B.corridor`; `hi + 1 == pin` asserted)
   on the F-CTRL path (tierc11_forward_ledger.py:220-234; tc11x_forward.py:522-538). LX-X5.3's rival "ride only the bars after
   the opening" is REJECTED: "the ride needs the 316-bar warm-up and the window's arming history" (LEANS_X.md:2065-2066).
2. **Admission**: `entry_close_ms > opening_ms`, STRICT (tierc11_forward_ledger.py:238-240; tc11x_forward.py:562-564). `entry_ms`
   is the entry bar's OPEN; `entry_close_ms = entry_ms + 4h`. So the first admissible entry bar OPENS at 2026-09-21T16:00Z; an
   entry bar closing exactly at the opening is not admitted. (Equivalent on the 4h grid to TC10's strip predicate
   `entry_ms >= as-of`, FORWARD_STRIP.md:20.)
3. **Continuation** (straddles the origin): `entry_close_ms <= opening and exit_ms >= opening` → listed, never counted
   (tierc11_forward_ledger.py:253-257). X does not list continuations at all (it only filters `admitted`).
4. **OPEN at the pin**: `exit_reason == "corridor_end"` (tierc9's reason for a ride the pin cut) → listed with
   `net_r_marked_to_pin` (TC11) / in `open_keys` (X), NOT appended, NOT counted (:243-245; tc11x_forward.py:138, :567-570).
5. **Append exactly once, when closed**, at the first refresh that sees it closed; order of appended lines: TC11 by
   `(exit_close_ms, symbol, entry_ms)` (:371-372), X by `(entry_close_ms, symbol)` (tc11x_forward.py:735-738) — the two differ.
6. **HALTs**: an appended row that re-derives differently or is absent (`REFRESH-CHANGED` :330-341 / `FWD-ROW-CHANGED`
   tc11x_forward.py:776-785); a broken chain; a pin behind the last refresh; a same-pin refresh that would append
   (`:355-358`) / disagrees (`FWD-REFRESH-DISAGREES` :829-841); pool lower bound moved (`FWD-LO-MOVED` :762-765); a `None`
   tide band (`FWD-BAND-NONE` :548-554); gated row without its base row (`FWD-SUBSET` :786-788).
7. **Gated book = post-filter of the base forward rows** (`post_filter`, only `book` changes; tc11x_forward.py:557-559,
   :573-579); "a gated row is appended iff its base row is and its band is not B4". The re-ride rival (`reride_gated`, refused
   candidates dropped BEFORE the one-position-per-asset check so a freed slot can re-enter; :495-519) is recorded on every
   refresh line as `n_reride_differs` / `n_reride_differs_whole_tape` — printed, never held to 0.
8. **Both scripts are HARD-PINNED to TC11's substrate and cannot refresh past 2026-09-25T00:00Z**:
   - TC11: `check_snapshot` requires `--snapshot == NAIAD_CACHE_DIR == E.SNAPSHOT` (tc11_20260925) (:526-539); `B.corridor`
     "may only look back" (tierc11_books.py:254-262); `tierc11_env.guard_substrate` HALTs on any other cache dir
     (tierc11_env.py:192-208; `SNAPSHOT` :117, `PIN_MS = 1_790_294_400_000` :122). The script says so itself: "A refresh on
     bars after 2026-09-25T00:00Z needs the foundation re-rooted on a new snapshot + pin record — operator / foundation work"
     (:43-48; printed at FORWARD_LEDGER.md:38).
   - X: `FWD-PIN` — "the ledger of record refreshes at the substrate's pin … only — no refresh past it (a data spend)"
     (tc11x_forward.py:690-692, :756-757).
9. **Row fields** (as-of-STABLE only):
   - TC11 `ROW_FIELDS` (49 names, :94-106) + `exit_px, haircut_net_r, slip_bps_side, p_age_1_band, p_age_1_refuses,
     p_win_1_lag, p_win_1_refuses, p_win_1_shadow_refuses` (:209-215); excluded by name `AS_OF_DEPENDENT = (window_end_i,
     window_end_close_ms, window_open_at_asof, open_at_asof, continuation, entered_after_tc10_pin)` (:107-108). Gate stamps
     typed: `P_WIN_1_CUT = 16` (:90), `P_WIN_1_SHADOW = (7, 15)` (:91), `P_AGE_1_OLD = "B4"` (:92).
   - X `ROW_FIELDS` (32 names + `B.TIDE_COLS` 11 = 43; tc11x_forward.py:165-174): `kind, book, symbol, entry_ms, direction,
     lane, roles_name, arm_i, arm_ms, lag, entry_i, entry_close_ms, exit_i, exit_ms, exit_close_ms, exit_reason, bars_held,
     entry_px, exit_px, stop_px, r_dist, atr_at_entry, net_r, gross_r, fee_r, funding_r, mfe_r, n_advances, harvested,
     harvest_ms, reached_1r, era_of_entry` + `tide_state_entry, tide_streak_entry, tide_left_censored,
     tide_trailing_edge_q25/q50/q75, tide_band, tide_band_label, tide_abs_gt206, tide_streak_age_arm,
     tide_streak_age_arm_censored` (X:scripts/tc11x_books.py:208-211). `lag = entry_i − arm_i` (:445). The 12 `CTRL_COLS`
     (M:scripts/tierc10_panel.py:2707-2709): `entry_ms, exit_ms, entry_px, exit_px, stop_px, r_dist, net_r, gross_r, fee_r,
     funding_r, mfe_r, n_advances`, carried at full float. Nullable: `ROW_NULLABLE` (:173-174); any other null / NaN HALTs
     (`_native`, :414-434).
10. **n ≥ 30**: TC11 `N_SCORE = 30` (:82), status `"UNSCORED (n {n} < 30)"` else `"n {n} >= 30: scorable"` (:301-302). X reads
    30 by object from L-T.6 (`lt6_n_min`, :207-212) → `n_min`; status else `"n … >= 30: eligible for scoring by a filed
    registration only (not here)"` (:862-864). n is per book, never combined.
11. **The two ledgers DISAGREE on sums**: TC11's report prints "appended ΣR (net) · Σ haircut R" per book
    (tierc11_forward_ledger.py:455-461; FORWARD_LEDGER.md:21); X's law forbids ANY aggregate over row values —
    "A DIARY, NOT A SCOREBOARD" (tc11x_forward.py:16-19), enforced by F-FWD-NOSTAT (FIXTURES_X5.txt:43).

### 1.9 The fourth book's two refusals are BOTH already filed TC11 texts

`M:research_outputs/tierc11/registrations/REGISTRATIONS.json` (sha `648834bf30e20e92713bddef2374ddef1aae843f4d8ba152fc50166c8cc6f1ee`,
identical to X's extraction `X:research_outputs/tierc11x/data/tc11_rec/registrations/REGISTRATIONS.json`):
- `P-AGE-1` (payload sha `e01a89ea7e6fda864f7002a450abd1a4e92424c44d1a9626f6641814e7d35879`) `operative_spec.scored_arm`:
  "v6 book minus the campaigns whose ENTRY-bar tide streak (tierc7_lab_regime.tide_streak) is >= the trailing 75th-percentile
  edge (B4 OLD; tierc9._trailing_edges over CLASSIC5 4h bars with open <= the entry bar, >= 30 bars) [L-G.1]"
- `P-WIN-1` (payload sha `d19a42a329be3bfeea73c3c628bf515f5d0fa2fb8facd3fcac795b0186525084`) `operative_spec.scored_arm`:
  "v6 book minus campaigns with entry_i - arm_i >= 16 (4h bars) [L-G.2]"

Membership on the filed v6 book at TC11's pin (`M:research_outputs/tierc11/books/v6_campaigns.parquet`, sha
`aab06934ae92689ef2e0fcc6b857350cf397ddca7a0a57e180960c51669b28e5`, 200 rows; columns `tide_band`, `lag`; and X's
`books/v6_x_campaigns.parquet` sha `7eb0bf4e552f9462b7532ee612b73c7610870c3f502c3844838054fd4088a05f`, same keys; counts only,
no outcome grouped): OLD (B4) 59 · stale (lag ≥ 16) 63 · both 32 · refused by either 90 · **kept by the combined gate 110**
(holdout: 77 → OLD 17, stale 21, either 30, kept 47). OLD-gated keeps 141 (holdout 60) — matches F-FWD-SUBSET "keeps 141 == 200
− 59" (FIXTURES_X5.txt:37-41) and F-FWD-ONCE "v6 77, trg912 66, gated-v6-oldtide 60" closed forward keys from a 2024-07-01
scratch opening (FIXTURES_X5.txt:26-29). `lag == entry_i − arm_i` on all 200 rows. Σ net_r of the 6-dp file = 40.807566 (the
contract's Stage C figure). 0 `tide_band` nulls. (The contract's "cell 110" coincides with the kept count 110 — noted, not
interpreted; the crossed table is another unit's.)

Inference (labelled, not a record): v6 has ridden 200 campaigns in 2,573.3 days (`as_of_span_days`), i.e. ~0.078/day; n ≥ 30
is ~386 days away for base v6, ~548 for OLD-gated (141/200), ~702 for the combined book (110/200). Every book stays UNSCORED
through TC12 by a wide margin.

### 1.10 TC10's FORWARD_STRIP (the precedent for Stage C's "extension printed separately")

`M:research_outputs/tierc10/close/FORWARD_STRIP.md` (5,786 B, sha `a59e438c690987eb69bf24f805c54a4d36ae533d03e7422d499372c19d3872c4`),
`FORWARD_STRIP.parquet` (sha `4e118dc1e3f0873f655ab9869c647baff8ea0057113eeb6f6d80f5a785abba53`; 4 rows × 33 cols). Producer
`M:scripts/tierc10_close_forward_strip.py` (`TIER = "REPORT-ONLY — FORWARD STRIP — NEVER SCORED"`, :127; `build_strip(journal,
tc9_ms, stem_asset)` :323). Law: window = TC9's as-of 2026-08-22T00:00Z → TC10's pin; ENTERED-IN-STRIP `entry_ms >= as-of`
(4), CONTINUATION `entry_ms < as-of <= exit_ms` (0), OPEN-AT-CORRIDOR-END `exit_reason corridor_end` marked to the pin (1);
"Counts and sums only: no CI, no p, no verdict, no LOAO, no FDR bar" (:3); rows verbatim from the filed journal + an ADDED
haircut twin. Parquet schema: `label, window, tier, scored(bool), asset, lane, direction, arm_ts, entry_ms(int64), entry_ts,
exit_ms(int64), exit_ts, exit_reason, bars_held(int64), entry_px, exit_px, r_dist, gross_r, fee_r, funding_r, net_r,
haircut_twin_net_r (float64), haircut_twin_tier, haircut_twin_charter_round_trip_bps, as_of_last_closed_4h, as_of_panel_start,
as_of_span_days, warranty, as_of_lens, as_of_last_closed_bar, as_of_panel, as_of_n_assets(int64), as_of_substrate`.

### 1.11 X4's era tables (`X:research_outputs/tierc11x/era/`)

Files (parquet is GITIGNORED — `X:research_outputs/tierc11x/.gitignore:3 *.parquet`, `:4 _det_*/` — it exists only on the X
worktree's disk and will NOT arrive with X's merge):

| file | bytes | file sha256 | content sha (manifest `sha`) | tracked |
|---|---:|---|---|---|
| `X4.md` | 422,116 | `aac2be88b8d71f46c232a1976cd5d06dd5ded91b3356976050a48344e9557be8` | — | yes |
| `X4_stamps.parquet` | 177,485 | `e647a9f782a204ba70c8307d8b7fcce744528b433dd7f908a276ca31f0e95683` | `8dd0e6fc0e16b4192e3f16b4244774db99cfa52ed684335a4139be97bdf2d9c7` | NO |
| `X4_tables.parquet` | 164,057 | `fda7a280b76e295b5faf06119061e3243461c50c6d0d941daecf1b4715a1e5b0` | `4f01ec8f6379339bb5b81b65f5b1421e13119387af2ee5f5fafeeb8950df8bfa` | NO |
| `build_manifest.json` | 34,139 | `0ad7f6eac56a003bbcc694115f54f347dcb2d20895da414d1615410cfc34a642` | — | yes |
| `FIXTURES_X4.txt` | 23,285 | `2c942f8c855835ebaa5a3dc778be0f360064673ed27c96d15bdbe857a08e4e58` ("8 GREEN, 0 RED") | — | yes |

Producer `X:scripts/tc11x_era.py` sha `f1b42be4b7012ae3c7166cf0d51195bb9c505abc126b8a68e6af49c7649b597b` (2,546 lines);
percentile helper `X:scripts/tc11x_pct.py` sha `49809c070ed00223a345edc51b5d83355f229a6b1372495038ff42aeba204bb7`
(`trailing_counts(arr, i, window=2000, floor=300)` :71; `WINDOW = 2000` :48, `FLOOR = 300` :49).

**`X4_stamps.parquet`** — 200 rows × 176 cols, key `[symbol, entry_ms]`, one row per v6 campaign; BOOK-INDEPENDENT (each stamp is
a pure function of explicit arrays at the entry bar). Column families: identity (`symbol, entry_ms int64, entry_close_ms int64,
direction int64, entry_i int64`); vol (`vol_window_end_ms, vol_rv30, vol_{lt,eq,n} int64, vol_pct float64, vol_third` and the
same quintet for `vol_w500_*, vol_atr14_*, vol_natr_*, vol_exp_*`; `vol_rel, vol_rel_edge_lo/hi, vol_rel_pool_n, vol_rel_third`);
funding (`fund_hour_ms, fund_rate, fund_r8, fund_gap_h, fund_settlement_coincident bool, fund_window_end_ms, fund_window_lo_ms`
+ quintets `fund_*, fund_signed_*, fund_w90_*, fund_raw_*, fund_exp_*`); edges (`edge_q25/q50/q75 float64, edge_pool_n`); BTC
clock (`btc_i, btc_bar_close_ms, btc_run, btc_state, btc_left_censored bool` + quintets `btc_*, btc_own_*`; `btc_band,
btc_aligned`); own age (`own_run, own_state, own_left_censored, own_band, own_age3`); breadth (`q50_pool17,
breadth_n_listed/n_warm/n_undetermined/n_eff/young int64, breadth_members_warm, breadth_members_undetermined,
breadth_member_hash, breadth_opens_all_entry bool, breadth_warm_idx_ok bool, breadth_min_warm_idx, breadth_window_end_ms,
breadth_share float64, breadth_third` + twins `b10_*, loo_*, p17_*, pa_*, cy_*`); 24 cell labels `cell__<block>` (object);
`era, cal_side, lane`; the collar (`tier, selection_not_a_result, gates, would_read_ci_only, m_looks_this_table int64, m_note,
promotable bool`); the nine as-of stamps.

**`X4_tables.parquet`** — 1,458 rows × 116 cols, key `[table, block, reading, cell, side]` (tc11x_era.py:224). String cols:
`table, block, reading, cell, side, grid_cell, block_kind, parent, reading_id, occ_kind, degenerate_why, loao_line,
support_cells, sentence_word, sentence, overlap, coef, patch_list, tier, selection_not_a_result, gates, would_read_ci_only,
m_note, size_footnote, nan_reason, block_label`; Int64: `n, n_assets, n_b, n_assets_b, n_2024h1, loao_above, loao_below,
occ_bars, occ_total, pre2024_months, n_support_cells, provisional_cells_k, n_trimmed, m_looks_this_table, seed, n_boot,
n_a_<5 assets>`; float64: `w, mean_r, sum_r, p_win, ci_lo, ci_hi, p_mc, nan_share, p_exact, lo_exact, nan_share_exact,
occ_share, delta, delta_ci_lo/hi, delta_nan_share, c_s, w_s, c_s_ci_lo/hi, w_s_ci_lo/hi, c_1, w_1, c_2, w_2, n_term,
offsupport_b/h, poststrat_e, poststrat_ess, w_b, w_h, mean_b, mean_h, c_contrib, w_contrib, e_b_w, e_h_trim, e_b_trim,
composition_part, within_part, ess, occ_share_b/h, occ_ratio, campaign_ratio, s_a_<5 assets>`; boolean: `ci_computed,
provisional, on_support, late_like, no_pre2024, selected_by_campaign_share, converged, promotable`; + nine as-of stamps.

The ten tables, their axes, and what a "refresh with the gated books" touches:

| table | rows | axes (block × cell × side; reading) | content | book-dependent? |
|---|---:|---|---|---|
| **E-1** | 376 | 19 blocks (4 record: `vol, funding, btc_clock, breadth`; 14 twins; 1 rival `btc_clock:own_history`) × cell {T1,T2,T3,unbanded,ALL} (`btc_clock:B1-B4`: B1..B4,unbanded,ALL; `btc_clock:aligned`: aligned,opposed,ALL) × side {tuning, holdout (reading `era`); before_2024, h1_2024 (reading `calendar`)} | v6 E[net R] by fixed third per era: n, w, mean_r, sum_r, p_win, 90% cluster CI, exact p, LOAO, per-asset n/S + all-bar occupancy, pre-2024 months | YES (all outcome/n columns); `occ_*`, `pre2024_months` NO |
| **E-1d** | 188 | same block × cell × side {holdout−tuning (era), late−before (calendar)} | within-cell Δ by `T5.cluster_boot_diff` | YES |
| **E-2** | 44 | 22 blocks (19 + `cross, cross:B1-B4, cross:loo`) × reading {calendar, tuning-twin}; side `decomposition` | Shapley Δ = C_S + W_S + N on SUPPORT; CIs; post-stratified reweight + ESS; `sentence_word` / `sentence` | YES (and SUPPORT itself: cells with ≥ 1 campaign and ≥ 3 assets in BOTH sides) |
| **E-2c** | 236 | block × reading × support cell; side `support` | the decomposition's cells | YES |
| **E-2p** | 2 | block `propensity` × reading | the propensity-reweight rival (point, no CI) | YES |
| **E-3** | 224 | 20 blocks (those with an occupancy kind) × reading × cell; side `occupancy-ratio` | late-like cells: all-bar occupancy ratio ≥ 1.5, "SELECTED FROM COUNTS BEFORE ANY E[R]" | selection (`occ_share_b/h, occ_ratio, late_like, no_pre2024`) NO; `n, n_b, w_b, w_h, campaign_ratio, selected_by_campaign_share` YES |
| **E-3p** | 80 | 20 blocks × reading × side {patches−before_complement, patches−late} | the late-like patches compared by cluster_boot_diff | YES |
| **E-4** | 184 | 3 cross blocks: `cross` (breadth thirds+unbanded × {YE = B1∪B2, MAT = B3, OLD = B4} + own-unbanded + ALL = 14 cells), `cross:B1-B4` (18), `cross:loo` (14) × 4 sides | the breadth × own-tide-age cross, levels | YES — and every `…/OLD` (and `…/B4`) cell is EMPTY BY CONSTRUCTION in both gated books |
| **E-4d** | 92 | 3 cross blocks × cell × {holdout−tuning, late−before} | the cross's Δ | YES |
| **D-1** | 32 | `vol:expanding`, `funding:expanding` × 4 cells × 4 sides | counts-only disclosures (n, occ_bars, occ_total, occ_share) | `n` YES, `occ_*` NO |

(Row arithmetic checked: 376+188+44+236+2+224+80+184+92+32 = 1,458.) Era constants: `ERA_CUT_MS = 1_719_791_999_000`
(2024-06-30T23:59:59Z, "the LAST tuning instant", M:scripts/tierc11_env.py:128); `CAL_2024_ISO = "2024-01-01T00:00:00Z"`
(tc11x_era.py:168); sides n at TC11's pin on v6: "123 / 77 by era; 109 / 77 / 14 on the calendar sides" (PITFALLS,
tc11x_era.py:203); `SEED 20260925`, `N_BOOT 4000` (:142-143); `LATE_LIKE_RATIO = 1.5` (:172); `NAN_SHARE_MAX = 0.05` (:173);
`CLUSTER_FLOOR 3`, `PROVISIONAL_N 30` (:170-171); `BREADTH_FLOOR = 5` over PANEL17 (:164); thirds decided in INTEGERS (LX-X4.7).
Filed result: "0 of 5 sentences resolved" (X4.md:11); all five calendar sentences read "NO RESOLVED LATE-ERA EDGE — UNRESOLVED"
(`build_manifest.json → sentences_calendar`).

Structure that matters for a refresh: `stage_a(inp, book, fresh_bars=True)` (tc11x_era.py:1327) is ALREADY parameterised by a
book frame (`symbol, entry_ms, direction, lane`; "identity only: no outcome"), and `build_tables(A, sf_o)` (:1877) by stage A +
an outcome frame. Only `load_book()` (:1064; hard `len(df) != 200` HALT at :1075), `corridor()` (:1034; `hi + 1 != PIN_MS`
HALT), `tc11_reads()` / `X.record_reads` (:1105-1145) and `compute()` (:2056) wire it to X's v6 book, TC11's pin and X's reads
record. The module imports `tc11x_env` FIRST (:122) and cannot be imported outside the X worktree / tc11_20260925.

### 1.12 The ferry law (`X:scripts/tc11x_ferry.py`, sha `6594bbc27f2f2ed9f1a0261e06b86d1fd26be84fce92a297200f7e9af6478f8f`, 2,664 lines)

Source text: X contract `X:exchange/queue/2026-09-25_TC11X_APOLLO.md:42-44`: "STAGE X6 · THE FERRY LAW (standing, from this build
on): every per-trade and per-asset row file of TC11 and TC11-X exports to exchange/rows/<tier>/<name>.csv, committed with the
build; cap 2 MB per file (beyond it: first 2 MB + parquet pointer + sha). Box budget respected; ATHENA governs." Readings
LX-X6.1…X6.9 (X:…/LEANS_X.md:2099-2273); amendments AM-X13…X17, X21, X22, X26, X27 (LEANS_X_AMENDMENTS.md:291, 318, 346, 377,
410, 478, 507). Fixtures: `FIXTURES_X6_rerun.txt` "7 GREEN, 0 RED" — F-ROWS (EXIST, with HELD) · (FORECAST, AM-X21) · (RT) ·
(CUT) · (SCOPE) · (FRESH leg) · F-TC11-READ.

**Which files qualify (LX-X6.1, the STRICT scope; "by rows, never by name")** — `identity_class(df, asset_cols, book_axes)`
(tc11x_ferry.py:495-513):
- `ASSET_COLS = ("asset", "symbol")` (first present) (:194);
- `INSTANT_COLS = ("entry_ms", "entry_open_ms", "entry_close_ms", "harden_ms", "event_ms", "known_at_ms")` (first present) (:195);
- `BAR_INSTANTS = ("t0", "t0_ms", "open_time", "open_ms", "bar_ms")` never identities (:196);
- `BOOK_AXES` — the frozen 26-word vocabulary (:197-199): `lane, arm, book, cell, cell_id, twin, twin_id, variant, lens, scale,
  scale_kind, era, toll, panel, horizon, direction, side, cls, kind, detector, trade, table, variable, row_label, band, third`
  (any that is a column of the file is an axis); `DRAW_COLS = ("draw",)` (:200).
- Order of tests: a column named `draw` → POINTED ("a draw table"); no ASSET column → POINTED ("no ASSET column");
  unique on (axes, ASSET, INSTANT) → **PER-TRADE**; else unique on (axes, ASSET) → **PER-ASSET**; else POINTED ("rows per
  identity > 1"). PER-TRADE / PER-ASSET → FERRIED.
- Triage before the rule (`triage`, :516-531): any path segment starting `_det_` → EXCLUDED; `TABULAR = (.parquet, .csv,
  .jsonl)` (:212); `FETCH_LOG*` → EXCLUDED (per-request log); manifests (`build_manifest.json, STAGE_D_MANIFEST.json,
  CLONE_ATTEST.json, PRE_STATE.json`, or any `*.json` matching /MANIFEST/i) → EXCLUDED; everything else → EXCLUDED "document";
  five named JSON documents POINTED by path + sha (:223-225).
- X's OWN files carry a TYPED class list fixed before the files existed (`X_TYPED`, :231-299), and the rule is re-derived on
  each; a disagreement, or an X parquet not on the list, is a HALTED ELEMENT (never ferried) until a dated amendment. TC11's
  files are enumerated and classed mechanically, never typed. Relevant typed rows: `forward/FORWARD_LEDGER.jsonl` POINTED
  ("committed in git (LX-X5.4)", "a hash chain of mixed line kinds", :295); `era/X4_stamps.parquet` FERRIED per-campaign
  `(symbol, entry_ms)` (:290); `era/X4_tables.parquet` POINTED "no ASSET column (a per-cell summary …)" (:291-293).
- Vocabulary gaps already cost X two amendments: AM-X22 (`panel` as the ASSET column of va/ tables) and AM-X27 (`measure` as
  a book axis of va/ tables only) (:201-211).

**Names (LX-X6.2)**: `exchange/rows/<tier>/<flat>.csv`, `flat_name(rel)` = source path relative to `research_outputs/<tier>/`,
extension dropped, `/` → `__` (:481-485); HALT on a collision, exact or case-folded (:610-622). One `ROWS_MANIFEST.md` per
tier dir (:165). "Written **only in the worktree**. Never in the main tree's `exchange/`, which the 07:00 routine would sweep
(daily_routine.py:1489)" (LEANS_X.md:2195-2196).

**CSV dialect (LX-X6.3)**: `to_csv_bytes` = `df.to_csv(buf, index=False, lineterminator="\n", encoding="utf-8")` (:543-547),
default float repr, row order the source's own; pandas 2.2.3 (`FERRY_MANIFEST.json → serializer.pandas`). Reader law (AM-X15
(C); :185-191): `pandas.read_csv(<csv>, float_precision="round_trip", keep_default_na=False, na_values=[""], dtype=<the
parquet schema's>)` reads an untruncated CSV back equal to its parquet; the default float parser is NOT lossless.

**The cap (LX-X6.4)**: `CAP_BYTES = 2_000_000` on the CSV alone (:177); rival `CAP_RIVAL = 2_097_152` (:178). Whole rows only:
`cut(csv, n_rows, cap)` keeps the largest k with `len(header) + Σ_{i<k} len(row_i) <= cap`, record ends found quote-aware
(:550-575); the carried file is a pure CSV; its pointer (source path+sha, bytes, mtime, rows carried/total, last carried key,
full-CSV and carried shas) lives in `ferry/FERRY_MANIFEST.json` and is rendered in `ROWS_MANIFEST.md`; `protected_by: NOT
PROTECTED — gitignored parquet` (:179). Example on disk: `sfp__X2_trades_1h.csv` 1,999,149 B, 1,370 of 2,408 rows (CUT).

**The box, and "past WARN" (LX-X6.7)** — constants read by `ast.literal_eval` from `scripts/publish_exchange.py` (never
imported; `publish_constants`, :626-641); that file is byte-identical in both trees, sha
`15eec3d0bf0420200d94fc3087e4868a59eecb5cdb1fc21e01b8c80daae8a65b`:
- `SCOPE = "exchange/"` (publish_exchange.py:48) · `BOX_BYTES = 16_000_000` (:95) · `WARN_FRACTION = 0.40` (:109) ·
  `REFUSE_FRACTION = 0.70` (:110) · `OVERRIDE_ENV = "NAIAD_ALLOW_OVERSIZE_PUBLISH"` (:111) · `TICK_EXTRA = ("LEDGER.md",)`
  (:128) · `FLAG_BYTES = 64_000` (:160).
- Comparators (`budget`, :217-222): `frac > 0.70` → REFUSE; `frac >= 0.40` → WARN. So **WARN line = 6,400,000 B** (exactly
  6,400,000 already reads WARN; `warn_line()`, tc11x_ferry.py:655-663), REFUSE above 11,200,000 B.
- **What is measured: the TICK SET, not `du`** — the tracked `exchange/**` blobs (publish reads the git INDEX,
  `_index_sizes`, publish_exchange.py:523-555) + `LEDGER.md` at HEAD (`tick_extra_bytes`, :269-289). Untracked files
  (`.DS_Store`) and the working copy of a modified file do not count.
- X's basis of record (AM-X15 (B1), AM-X17): the MERGE TARGET — the pinned main HEAD's tick set merged path by path with X's
  index delta — pinned BY VALUE (`merge_target_pin.head_sha`); the worktree index is only a cross-check.
- `project(order, base, C)` (:666-685): `base = tick bytes + ROWS_MANIFEST.md reservation + close reservation`
  (`plan_holds`, :753-761); files in a FIXED order; a file is WRITTEN iff `level(cum + bytes) == "OK"` (i.e. the projection
  stays ≤ 6,399,999 B), else **"HELD FOR ATHENA"** — "not written, not counted" — and the loop CONTINUES (first-fit: a later,
  smaller file may still be written). HALT only if the base alone is past REFUSE. The override env is never set.
- Fixed order (AM-X16): `PRIORITY_X` = `exit/X1_registered`, `sfp/X2_trades_1h`, `exit/X1_cells` (the registered rows first),
  then X's other files by path, then TC11's by path (:331-336, :688-696). Reason filed in AM-X14: "The rows that bear on the
  verdicts come first. File sizes are structural, not outcomes".
- Every bus file over 64,000 B is FLAGGED ("named to the operator at creation, with its home", CONVENTIONS.md:360).

**The HELD list format**: `FERRY_MANIFEST.json` → `athena.held_for_athena` (a list of source paths, 84 at X-FIX), `box.held`,
`box.k_held`, and one `box.projection[]` record per file, e.g. `{"action": "HELD FOR ATHENA", "bytes": 1999590, "key":
"research_outputs/tierc11x/exit/X1_cells.parquet", "level_if_written": "WARN", "projected_after": 5877444, "would_be":
7877034}`; `athena.questions` Q-A1 ("a named exception for exchange/rows/ on the MANIFEST.json precedent …, and which cap: the
contract's 2,000,000 B or the bus's 1,048,576 B") and Q-A2 ("a folder budget and a rotation rule for exchange/rows/"). In
`ROWS_MANIFEST.md`: a section `## HELD FOR ATHENA (k) — declared, not exported (LX-X6.7, LX-X6.9)` with a table
`| would-be bus file | source | class | key (unique) | rows | capped CSV B | source sha256 |`
(X:exchange/rows/tierc11x/ROWS_MANIFEST.md:28-32). F-ROWS prints "GREEN with k HELD", never a bare GREEN (LX-X6.9).

**AM-X21 — "the ferry of record is a CLOSE ACT"** (LEANS_X_AMENDMENTS.md:478-504): `close_acts.sh` runs the ferry AFTER TC10's and
TC11's blocks have landed in LEDGER_APOLLO (by bytes), pinning main's HEAD at that instant; its CSVs and ROWS_MANIFESTs are
committed on `tierc11x` before the merge; the reservation then covers only X's OWN close adds. The executor's own run is a
FORECAST with NAMED reservation parts: X's report, X's LEDGER append, "TC10's pending close adds (161,600 B)", "TC11's pending
close adds (887,648 B build document + 16,572 B stamped append = 904,220 B)", "the swept exchange/ edits (3,293 B)". Reason:
"Tier order lands TC10's and TC11's closes before X's, so a box measured without them is not the box X's publish will see."

**Where `exchange/rows/` exists**:
- MAIN: **no `exchange/rows/` at all** — absent on disk and at HEAD (`git ls-tree -r HEAD -- exchange/rows/` = 0 entries).
  `M:exchange/` holds `DIGEST.md, README.md, drops/, queue/, reports/, status/`. The only main-tree text naming
  `exchange/rows` is the TC12 contract itself. No ATHENA ruling on Q-A1 / Q-A2 is on disk.
- X worktree (tracked at 7b24f83; X-FIX's bus, NOT the ferry of record): `exchange/rows/tierc11x/` = 6 CSV + ROWS_MANIFEST.md
  (12,215 B, sha `39bc9bde50e1a24e84b810b39a50e5562dec81d42ef0ea34f902c74ebe8eb654`), 3,015,136 B in 7 files;
  `exchange/rows/tierc11/` = 7 CSV + ROWS_MANIFEST.md (35,006 B, sha `0efecd69489c9b4bbd0b5f80dabe304691e714002ee3ae0acf6182601f42d678`),
  99,144 B in 8 files. Records: `ferry/FERRY_MANIFEST.json` (951,831 B, sha `604a055ce217421b0186072dec8b2f468a59082e826f1e5e4fc6b1af8342d41f`),
  `ferry/BOX_FORECAST_CLOSE.md` (sha `f577308f58ad99e0ef885a741ac77ddd0a5e0e391c83c2cf2273340c51dcb24b`).

**Ferry law text in main's `exchange/`**: none. What main's bus says instead (the four conflicts LX-X6.8 names for ATHENA, not
fixed): `M:exchange/README.md:20-24` "Text only … 1 MB per-file cap. No single file under `exchange/**` may exceed 1,048,576
bytes … Larger artifacts are referenced, never carried"; `M:exchange/status/CONVENTIONS.md:132` "captures, renders, results
JSONs, substrates, parquet and HTML never enter `exchange/`"; `:415` "Do NOT `git add` or `git commit` exchange files
separately — let the guard do it"; `:478` "1 MB per file"; `:494-498` the only named exception (MANIFEST.json), "Nothing else
inherits it".

### 1.13 The box today (main tree) and the headroom to WARN

| measure | bytes |
|---|---:|
| tracked `exchange/**` at main HEAD 28e006b (116 files): `queue` 154,420 (12) · `reports` 1,662,297 (71) · `status` 820,125 (30) · README 2,163 · DIGEST 561 · drops 561 | 2,640,127 |
| `LEDGER.md` at HEAD | 259,298 |
| **TICK SET at HEAD (what governs)** | **2,899,425** = 18.12% of 16,000,000 |
| working-tree bytes of the same 116 files (DAILY_2026-10-08.md is modified, +2,718) | 2,642,845 |
| `du -sk M:exchange` (filesystem blocks, incl. untracked `.DS_Store` 8,196 + `queue/.DS_Store` 6,148) | 2,844 KiB |
| WARN line | 6,400,000 |
| **headroom to WARN at HEAD** | **3,500,575** (a ferry may add at most 3,500,574 B and stay OK) |
| REFUSE line (>) | 11,200,000 |

History: tick set 2,878,190 B at `6f349395` (the HEAD X's forecast pinned) → 2,887,216 at `a399b47` → 2,899,425 at `28e006b`:
+21,235 B since X's forecast (daily auto-publishes +9,026; the TC12 contract in `exchange/queue/` +12,209).

What is still OUTSIDE the box but ordered to land before a TC12 close (all three closes are PENDING: `LEDGER_APOLLO.md` has 0
occurrences of "TIER-C10" / "TIER-C11"; `exchange/reports/` has no TIERC10 / TIERC11 file):

| pending add | bytes | source |
|---|---:|---|
| TC10's close adds | 161,600 | named figure, AM-X21 (on disk now: `research_outputs/tierc10/BUILD_DRAFT.md` 111,105 + `LEDGER_APOLLO_APPEND.md` 14,925) |
| TC11's close adds | 904,220 | AM-X21 (on disk now: `research_outputs/tierc11/BUILD_DRAFT.md` 887,648 + `LEDGER_APOLLO_APPEND.md` 16,732) |
| X's report + append | 185,925 | `X:…/BUILD_DRAFT.md` 169,771 + `LEDGER_APOLLO_APPEND.md` 16,154 (measured now) |
| X's bus rows at its forecast | 2,251,024 | written CSV 2,203,515 + two ROWS_MANIFEST.md 47,509 (BOX_FORECAST_CLOSE.md:145) |
| X's contract in `exchange/queue/` (X's merge delta; absent from main today) | 5,058 | `X:exchange/queue/2026-09-25_TC11X_APOLLO.md`, measured now; "X's delta +5,058 B" (BOX_FORECAST_CLOSE.md:11) |

X's own forecast: "with the reservation 6,397,755 B (OK) … the slack below it is 2,244 B" (BOX_FORECAST_CLOSE.md:145). Re-added on
today's HEAD: 2,899,425 + 161,600 + 904,220 + 185,925 + 2,251,024 + 5,058 = **6,407,252 B — 7,252 B PAST the WARN line**
(6,402,194 without X's 5,058 B contract file). With the sizes ON DISK today in place of AM-X21's named figures (TC10 111,105 +
14,925 = 126,030; TC11 887,648 + 16,732 = 904,380) the same sum is **6,371,842 B — 28,158 B UNDER the WARN line** (what else
TC10's 161,600 B figure covers is not on this scout's disk reads). Either way: (a) X's ferry of record will not reproduce its
forecast byte for byte — it re-plans on the box it finds, and its first-fit fills whatever is left with whatever fits;
(b) the box TC12's close will meet, on the filed tier order, is within tens of KB of WARN BEFORE TC12 adds its report, its
append or a single row file (a first-fit ends with less slack than its smallest held file).
With only TC10 + TC11 landed: 3,965,245 B (headroom 2,434,755). With TC10 + TC11 + X's documents but none of
X's rows: 4,151,170 B (headroom 2,248,830).

### 1.14 Signatures TC12 can import or must mirror

Importable as-is from MAIN (no env): `scripts/forward_log.py` — `GENESIS` (:52), `canonical(entry) -> str` (:67),
`chain_hash(entry, prev_sha256) -> str` (:79), `read_lines(path) -> list[dict]` (:85), `last_sha(path) -> str` (:106),
`append_entry(entry, path) -> dict` (:152), `verify_chain(path) -> {ok, checked, head, first_bad_line, reason}` (:209).

Lineage (main, reached through whatever env shim TC12 builds — another unit's): `TP.corridor_n(panel, pin_close_iso=None,
floor_bars=WARMUP_BARS) -> (lo, hi, meta)` (tierc10_panel.py:650); `TP.run_cell_n(card, roles, panel, lo_ms, hi_ms, …)`
(:1095); `TP.ride_spec(card, roles) -> dict` (:874); `TP._book_sha(book)` (:1988); `TP.stamp_n(df, meta, lens="4h")` (:2528);
`TP.AS_OF_COLUMNS` (:2557); `TP.make_put(root, meta, lens="4h")` (:2563); `TP.loao_n` (:1234); `TP.CTRL_COLS` (:2707);
`T5.cluster_boot(values, clusters, seed, n_boot=4000)` (tierc5.py:1178), `T5.cluster_boot_diff(va, ca, vb, cb, seed,
n_boot=4000)` (:1200).

To MIRROR (they import a TC11-pinned env at module top, so they cannot be imported under a TC12 snapshot):
- `M:scripts/tierc11_books.py` (sha `e025499d92b25231c676aaac17abffedba4dcc9d4821174fcd9f3566bd821313`): `corridor(pin_close_iso=None)`
  (:254), `r912()` (:270), `v6_book(lo, hi)` (:289), `trg912_book(lo, hi)` (:294), `book_sha(book)` (:306), `tide_pool(lo, hi)`
  (:358), `entry_streak(t)` (:363), `trailing_edges(t, pool)` (:371), `band_of(run, edges)` (:378), `lag_band(lag)` (:389),
  `known_window_end(end_i, hi_i)` (:396), `exit_event(t)` (:409), `campaign_rows(book, roles, lo, hi, pool, name) -> DataFrame`
  (:417); constants `ABS_TIDE_CUT = 206` (:155), `LAG_BANDS` (:157), `BAND_CODES` (:158).
- `M:scripts/tierc11_forward_ledger.py`: `canonical(obj)` (:128), `seal(obj, prev)` (:133), `verify_chain(raw: bytes) ->
  (findings, objs)` (:141), `haircut(sym, net_r, fee_r)` (:190), `book_rows(name, book, roles, lo, hi, pool)` (:197),
  `books_at(pin_ms)` (:220), `admitted(row, opening_ms)` (:238), `is_closed(row)` (:243), `already(appended, book, key)`
  (:248), `continuation(row, opening_ms)` (:253), `genesis(opening_ms)` (:287), `status_word(n)` (:301), `refresh(out_dir,
  pin_ms, opening_ms, snapshot_name)` (:305), `render_md(objs, S, opens, pre)` (:422).
- `X:scripts/tc11x_forward.py`: `opening_of_record()` (:215), `gate_text_of_record() -> (text, payload_sha, file_sha)` (:225),
  `module_shas()` (:255), `spec_doc(opening_ms)` (:324), `row_of(t, c, book)` (:437), `rows_of(book_list, crows, name)` (:466),
  `band_at(sym, i, pool)` (:481), `reride_gated(lo, hi, pool, refuse=None)` (:495), `ride_at(pin_ms)` (:522), `refuses(row)`
  (:548), `post_filter(base)` (:557), `admitted(rows, opening_ms)` (:562), `split_closed(rows)` (:567), `forward_books(R,
  opening_ms)` (:573), `reride_differs(pf, rr)` (:582), `chained(body, prev)` (:590), `append(path, bodies)` (:601),
  `book_open_body(book, spec_sha, opening_ms, n_min)` (:610), `chain_findings(path, spec_sha=None)` (:616),
  `ledger_state(path, spec_sha=None)` (:651), `freeze_spec(out, opening_ms=None)` (:696), `open_books(out)` (:720),
  `refresh(out=OUT, pin_ms=None)` (:741), `render_md(spec, lines, verify)` (:867), `twin_findings(x_lines, tc11_lines)`
  (:1025), `verify_lines(lines)` (:1061).
- `X:scripts/tc11x_ferry.py` pure core (:481-685): `flat_name`, `identity_class`, `triage`, `load_table`, `to_csv_bytes`,
  `record_ends`, `cut`, `csv_facts`, `collisions`, `publish_constants`, `level`, `warn_line`, `project`; plus `fixed_order`
  (:688), `plan_holds` (:753), `render_rows_manifest` (:1940).
- `X:scripts/tc11x_era.py`: `third_midrank` (:399), `third_share` (:405), `tide_law` (:416), `rv30` (:440), `rv_rel` (:451),
  `funding_8h` (:460), `derive(inp)` (:517), `_stamp_one` (:600), `stamp_campaigns(inp, camps)` (:804), `bar_cells(inp,
  replay_at=())` (:831), `occupancy(bars)` (:1217), `support_of(sf, block, b_side)` (:1270), `late_like_of(sf, occ, block,
  b_side)` (:1299), `stage_a(inp, book, fresh_bars=True)` (:1327), `level_stats(sub, side_n)` (:1470), `diff_stats(a, b)`
  (:1519), `decompose(sf_o, block, reading, b_side, support)` (:1584), `sentence_word(...)` (:1710), `propensity(sf_o,
  b_side)` (:1739), `build_tables(A, sf_o)` (:1877), `finish_tables(rows)` (:1979); `BLOCKS` (:244-283), `DISCLOSURES`
  (:284-289), `TABLE_KEY` (:224), `STAMP_KEY` (:223).

---------------------------------------------------------------------------------------------------------------
## 2 · CONTRACT-vs-DISK

C-1. **"fourth frozen book … all four books (base · 9/12 · OLD-gated · combined-gated)" / "the three existing books"** — the
contract presumes ONE ledger holding three books. Disk: TWO ledgers under TWO incompatible chain laws (§1.1). Base and 9/12
are of record in TC11's main-tree ledger and appear again as "X twins" in X's; OLD-gated exists ONLY in X's ledger, in the
unmerged X worktree. Neither ledger can take a fourth book in place: TC11's GENESIS fixes `books` to two and its script
iterates `BOOKS = ("v6", "trg912")` (:83); X's verifier refuses a `book_open` after line 3 (:636-638), its spec is write-once
(:696-709), and the X worktree "must not gain a file or a commit".

C-2. **"F-LEDGER (append-only on the three existing books; the fourth re-hashes)"** — there is no per-book hash to keep or
re-make. X has one spec sha for all three books (`72a1f523…`); TC11 has a GENESIS line sha (`b68a4942…`). "Re-hashes" has no
defined referent on disk (see R-2).

C-3. **"re-ridden on the bars since 2026-09-21T16:00Z"** — disk law (both scripts, and the filed L-T.6 / LX-X5.3): a WHOLE-TAPE
re-ride from the panel start (2019-09-08T16:00Z) to the pin, then admission by `entry_close_ms > opening`. "Ride only the bars
after the opening" is a REJECTED rival (LEANS_X.md:2065-2066).

C-4. **"(first appended rows)"** — true that nothing is appended yet (0 rows in both). But nothing guarantees a closed forward
campaign exists by TC12's pin: at TC11's pin the forward window held 0 closed campaigns in every book and 1 OPEN (9/12 SOL).
The CLOSE's "§0 … the ledger's appended rows" must be printable as "none yet".

C-5. **Neither ledger script can ride past 2026-09-25T00:00Z** (§1.8 item 8). TC11's own §11 Q5 — "The forward ledger: order
the foundation re-rooted on a new snapshot and pin record so it can refresh" (M:research_outputs/tierc11/LEDGER_APOLLO_APPEND.md:226-227)
— is NOT among the contract's "RULINGS ENACTED AS DEFAULTS" (it lists Q1/Q2, Q4, Q6, Q8, Q9; Q3, Q5, Q7 are absent). Stage D +
Stage L presume Q5 without naming it.

C-6. **"unscored until each book's own n ≥ 30"** — matches both (`N_SCORE 30`, `n_min 30`). But the two ledgers disagree on
what "unscored" permits: TC11 prints ΣR per book; X forbids any aggregate over rows (§1.8 item 11).

C-7. **"OLD-gated"** = book id `gated-v6-oldtide` on disk; **"9/12"** = `trg912`; **"base"** = `v6`. The contract's P-ADM-1 says
"refuse a trigger when …", which reads like an entry-time refusal that frees the slot; the filed law for a gate is a
POST-FILTER with "no re-ride into a freed slot" (TC11 L-1.5, LEANS.md:141-148; LX-X5.1), the re-ride being a disclosure count.

C-8. **"X4's era tables refreshed with the gated books (Tier-E)"** — X4 is hard-wired to X's 200-row v6 book, TC11's pin and
X's env (§1.11). Its two parquets are gitignored, on the X worktree's disk only. Under the ferry rule `era/X4_tables` is POINTED
("no ASSET column"), so refreshed era TABLES would not be row files; a refreshed stamps table (per-campaign) would be. With a
gated book every OLD cell of the cross is empty by construction and SUPPORT shrinks.

C-9. **"FERRY: every per-trade and per-asset row file → exchange/rows/tierc12/"** — `exchange/rows/` does not exist in main.
The filed law says the bus rows are written only in a worktree, never in main's `exchange/` (LX-X6.2), because the daily
routine publishes whatever sits under `exchange/` (`daily_routine.py:1489`; auto-publish commits run daily through
2026-10-08). X's contract says "committed with the build"; AM-X21 then made the ferry of record a CLOSE ACT. The TC12 contract
says neither.

C-10. **"2 MB cap"** — disk reading: 2,000,000 B on the CSV (rival 2,097,152). Main's bus rule is 1,048,576 B per file and
text-only-no-data (README.md:20-24; CONVENTIONS.md:132, :478). Q-A1 / Q-A2 are filed for ATHENA and unanswered on disk.

C-11. **"files that would push the box past WARN are held and LISTED for ATHENA"** — disk law: held when the projection would
REACH WARN (≥ 6,400,000), computed on the tick set at a HEAD pinned by value plus reservations, first-fit in a frozen order;
the disk's words are "HELD FOR ATHENA", listed in `FERRY_MANIFEST.json` and `ROWS_MANIFEST.md`. The contract names no basis,
no order and no reservation. On today's numbers the three pending closes alone project to 6.37–6.41 MB (§1.13).

C-12. **"ATHENA's residency rules" / LaCie** — not this unit's; noted only because `exchange/rows/` has no rotation rule
(`rotate_reports.py` never rotates rows/, Q-A2).

C-13. **"confirmation = the ledger's fourth book"** (Stage G, P-ADM-1) — at ~0.043 campaigns/day the combined book needs roughly
two years to reach n = 30 (§1.9, inference). The confirmation is a standing diary, not something TC12 can print.

---------------------------------------------------------------------------------------------------------------
## 3 · READINGS NEEDED (candidate leans)

**R-1 · Where the four-book ledger lives, and under which chain.**
 (a) A NEW file `research_outputs/tierc12/forward/FORWARD_LEDGER.jsonl` whose first 5,643 bytes ARE X's ledger verbatim (sha
     `4a6da7e8…`, asserted), continued under forward_log's law from head `61ea177f…`: one `book_open` for the fourth book,
     then `row` lines, then one `refresh` line at TC12's pin. TC11's ledger untouched and pinned by sha.
 (b) A new TC12 file with a FRESH chain: first lines pin both ancestors by sha and head (`e53328ad…`/`0db88942…`,
     `4a6da7e8…`/`61ea177f…`, spec `72a1f523…`), then four `book_open` lines.
 (c) Append in place to TC11's and/or X's files.
 RECOMMEND (a). It is the only reading under which "append-only on the three existing books" is a literal, testable prefix
 property (`tc12_bytes[:5643] == x_bytes`), it reuses X's filed spec sha and chain head instead of new constants, and it
 keeps one chain law. (c) is excluded: X is certified and frozen; TC11's ledger is cited by line in TC11's staged append
 (H-1). (b) is the fallback if the orchestrator will not carry X's unmerged bytes into a main-tree record.

**R-2 · What "the fourth re-hashes" means.** Options: (i) the fourth book gets its OWN spec document and sha — a
 `BOOK_SPECS_TC12.json` holding the fourth book's ride_spec + gate, embedding `72a1f523…` as the spec of record of the other
 three — named by the fourth `book_open` line, while lines 1-3 keep naming `72a1f523…`; (ii) a new four-book spec replaces
 the old one and all four `book_open` lines are re-issued (a re-opened ledger); (iii) only the chain head moves.
 RECOMMEND (i): the three books' freeze records stay byte-identical (append-only), and the new book's parameters are
 hashed afresh — a fixture plant that bends its gate text must change that sha and break the chain. F-LEDGER legs: prefix
 bytes equal; `X:BOOK_SPECS.json` still hashes `72a1f523…`; lines 1-3 unchanged; line 5 names a different sha that re-derives.

**R-3 · The fourth book's definition.** Options: (i) POST-FILTER of the base forward rows: v6 minus rows refused by P-AGE-1's
 scored arm (`tide_band == "B4"` at the ENTRY bar) OR P-WIN-1's scored arm (`entry_i − arm_i >= 16`), both texts READ from
 `REGISTRATIONS.json` (payload shas `e01a89ea…`, `d19a42a3…`), with `n_reride_differs` (the gate re-ridden as its own card)
 recorded on every refresh line as a disclosure; (ii) the re-ride into freed slots as the book of record.
 RECOMMEND (i): it is L-1.5 / LX-X5.1's filed gate law, needs no new typed constant (16 and B4 are read from the filed
 texts, never typed), and matches Stage G's "they remove trades". A `None` band HALTs. Suggested id: `gated-v6-combined`.

**R-4 · The opening.** Read by object: `STEP0_RECORD.json as_of_last_closed_4h_close_ms` (1790006400000), asserted equal to
 L-T.6's text and to `BOOK_SPECS.json opening.ms`; admission `entry_close_ms > opening` (strict). Rival: type the contract's
 literal. RECOMMEND read-by-object (three filed records agree); the contract literal is compared, never used.

**R-5 · "Re-ridden on the bars since".** RECOMMEND the filed reading: whole-tape re-ride (panel start → TC12's pin) on the
 F-CTRL path + the admission filter; `pool_lo_ms` asserted == 1567958400000 (HALT if the top-up moved the panel start).
 The rival (ride only new bars) is filed as rejected.

**R-6 · Row schema of the four-book ledger.** Options: (i) X's 43 `ROW_FIELDS` exactly (required by R-1 (a)'s chain) plus
 nothing; (ii) X's fields + the two gate booleans and the P-WIN-1 shadow (TC11's `p_age_1_refuses`, `p_win_1_refuses`,
 `p_win_1_shadow_refuses`); (iii) + haircut twin, VA stamps (Stage V5).
 RECOMMEND (ii) for the fourth book's rows and (i) unchanged semantics for the other three (extra keys allowed by
 forward_log, but every field must be refresh-stable). Keep VA stamps, haircut/maker twins and anything fee-schedule- or
 VA-code-dependent OUT of the chained rows — in a side table keyed `(book, symbol, entry_ms)` — so a later code or fee edit
 cannot trip FWD-ROW-CHANGED.

**R-7 · Sums in the ledger report.** TC11 prints ΣR; X forbids aggregates. RECOMMEND X's stricter law for TC12's page (rows
 and per-book n only; no Σ, mean, win share, CI or verdict word) — it cannot flatter and it is the law of the chain reused.

**R-8 · Base and 9/12: of record where?** After TC12 there would be rows for base / 9/12 in TC12's ledger while TC11's own
 ledger (of record for them) still holds 0. Options: (i) TC12's ledger becomes the ledger of record for all four books from
 its first row, TC11's file frozen as an ancestor (sha-pinned, never refreshed); (ii) also refresh TC11's file. RECOMMEND (i),
 stated as an amendment-grade reading and listed for the operator, with the anchor: at TC11's pin TC12's path must reproduce
 `book_sha` v6 `f3c68f54…` (200) and 9/12 `2c32fd60…` (199), the v6 ETH continuation and the 9/12 SOL OPEN entry exactly.
 AM-X9 (a)'s owed adapter stays owed (TC11's ledger gains no row).

**R-9 · How many refresh lines, at which pin.** RECOMMEND exactly one new `refresh` line, at TC12's corridor pin (Stage D's
 printed pin); no intermediate pins (each is a separate look). Same-pin re-runs append nothing and must agree.

**R-10 · Era refresh: which corridor.** Options: (i) TC11's corridor (pin 2026-09-25T00:00Z), so the v6 column must reproduce
 X4's filed tables and only the gated columns are new; (ii) TC12's extended corridor.
 RECOMMEND (i): it gives a mirror anchor (v6 rows vs `X4_tables.parquet` content sha `4f01ec8f…`, stamps vs `8dd0e6fc…`),
 mixes no unscored forward bars into a table, and leaves all-bar occupancy (book-independent) unchanged. The extension stays
 in the never-scored strip.

**R-11 · Era refresh: seed and bootstrap.** X4 drew at seed 20260925, n_boot 4000; TC12's seed is 20261008. Options: (i) the
 mirror leg at X's seed (byte anchor), the gated tables at TC12's seed; (ii) everything at X's seed; (iii) everything at
 TC12's, mirroring only the non-drawn columns. RECOMMEND (i), both seeds printed on the page.

**R-12 · Era refresh: which tables, and the empty cells.** RECOMMEND all ten tables per gated book (E-1, E-1d, E-2, E-2c,
 E-2p, E-3, E-3p, E-4, E-4d, D-1), book as a new key axis (`book`, already in the ferry vocabulary); E-3's late-like
 SELECTION carried unchanged from X4 (it is selected from all-bar counts, book-independent) and asserted equal; SUPPORT
 recomputed per book and printed; the cross's OLD / B4 cells printed as n = 0 "empty by construction", never dropped (grids
 whole). Every row collared Tier-E, `promotable = False`, m logged.

**R-13 · Ferry: when and where the CSVs are written.** Options: (i) build writes straight into `M:exchange/rows/tierc12/`;
 (ii) AM-X21's pattern: the build STAGES the CSVs and the manifests off-bus (`research_outputs/tierc12/ferry/…`), prints a
 FORECAST with named reservations, and the ferry of record is a TC12 close act (the operator's keystroke, per the contract's
 Q6). RECOMMEND (ii): it is the filed law ("draft off-bus" is also a TC12 LAW), it keeps the daily 07:00 publish from
 sweeping half-built rows to the remote, and it keeps TC12 bytes out of the merge target X's pending ferry of record pins.

**R-14 · Ferry: the basis and the reservations.** Options: (i) main's tick set at the pinned HEAD + TC12's own close adds
 only; (ii) + the named pending closes (TC10 161,600; TC11 904,220; X's report + append 185,925; X's bus rows as forecast
 2,251,024). RECOMMEND (ii) for the forecast (the conservative basis; on the named figures it is already past WARN, on
 measured sizes ~28 KB remain — either way effectively every TC12 row file is HELD and LISTED), with (i) printed beside as the rival, and the ferry of record re-measured at the close act on
 whatever has actually landed. HEAD pinned by value (AM-X17).

**R-15 · Ferry: scope and typing.** RECOMMEND the identity rule verbatim (frozen 26-word vocabulary, the six INSTANT columns),
 a TC12 typed class list frozen in LEANS BEFORE any file exists and re-derived on each file, a disagreement = a HALTED
 element. Design TC12's row tables to the vocabulary (e.g. fill-rule twins under `twin`, per-order / MISS rows keyed on
 `event_ms`, the four books under `book`, lenses under `lens`, the maker / taker toll under `toll`) rather than amend it.
 Type the ledger `.jsonl` POINTED (X precedent) and ferry a flat per-trade `ledger_rows` table instead.

**R-16 · Ferry: the fixed order.** RECOMMEND, typed before sizes exist: the ledger's appended rows first, then the per-trade
 files of the five registered rows (P-ADM-1, P-BRD-1, P-DIR-1, P-SFP-VA-1, P-SCALP-3), then the rest by source path. Only
 `tierc12` files (the contract names one bus dir); TC11's and X's rows stay X's ferry's business.

**R-17 · The cap.** RECOMMEND 2,000,000 B on the CSV, whole rows, pointer in the manifest (LX-X6.4 reused); 2,097,152 printed as
 the rival; the 1,048,576 B bus rule named as ATHENA's open conflict (Q-A1), not resolved by the executor.

**R-18 · How TC12 reaches X's records.** RECOMMEND: read from the X worktree by ABSOLUTE path with every sha asserted against
 this map's pins (or `git show 7b24f83:<path>` for tracked files), and keep sha-verified copies under
 `research_outputs/tierc12/x_rec/` — NEVER under `research_outputs/tierc11x/`, never as `scripts/tc11x_*.py` in main (H-2).
 The gitignored parquets (X4_stamps, X4_tables, books) can only come from the X worktree's disk.

**R-19 · Close order.** The filed order is TC10 → TC11 → X. RECOMMEND TC12's close acts refuse until X's block has landed (the
 same by-bytes check X's step 0 uses), and list the alternative (TC12 before X) for the operator — it would change which of
 X's files are held.

---------------------------------------------------------------------------------------------------------------
## 4 · HAZARDS

H-1. **Refreshing TC11's ledger in place breaks TC11's pending close.** TC11's staged append cites
 `research_outputs/tierc11/forward/FORWARD_LEDGER.md:5`, `:7`, `:38` by line (M:research_outputs/tierc11/LEDGER_APOLLO_APPEND.md:166-178;
 append sha `227317d1097c0f4e551ed90b717c09aa559a13006cb29e20c078a3e6d16414e1`), and TC11's `close_acts.sh` step 0 re-runs F-LAR11
 "every «cite» against its source as it stands NOW". Any refresh rewrites that md (pin, head, line count). The jsonl sha
 `e53328ad…` is also certified in TC11's PROGRESS (TC11-T-RELAY) and pinned in ten X records (three `land/TC11_LANDING_*.json`,
 `review/CLOSE_BRIEF.json`, `ferry/FERRY_MANIFEST.json`, `ferry/DRYRUN_FERRY_OF_RECORD.json`, four `data/TC11_READS_*.json`).

H-2. **Three main-tree paths that would make X's close acts refuse** (`X:research_outputs/tierc11x/close/close_acts.sh`): `:185`
 `[ ! -e research_outputs/tierc11x ] || die` (cwd = main) — never create that directory in main; `:108-121` + `:182-183` the
 merge allow-list (X adds `scripts/tc11x_*.py`, `research_outputs/tierc11x/*`, `exchange/rows/tierc11{,x}/*`) — an add/add at
 any of those paths conflicts the merge; `:131` the main index must be clean; `:259-260` the merge must not touch
 `research_outputs/tierc11/`. Also `:140-141`: the X worktree must be clean besides `close/CERTIFIED_TIP` — a stray
 `__pycache__`, `_det_*` run or scratch file there stops the operator.

H-3. **The X worktree is trivially easy to dirty.** Running any `tc11x_*.py` writes into `X:research_outputs/tierc11x/…` by
 default (`OUT`), X's ledger writer appends in place, and Python without `-B` / `PYTHONDONTWRITEBYTECODE=1` writes
 `scripts/__pycache__`. Read X's files; never execute X's builds or fixtures.

H-4. **Main's `exchange/` is swept and pushed daily.** `daily_routine.py:1489` calls `publish_exchange.publish(ROOT, today)`,
 which does `git add -- exchange` (publish_exchange.py:603), commits and pushes. A CSV dropped into `M:exchange/rows/tierc12/`
 mid-build is published at the next 07:00 run — before any verdict, outside the close acts — and enters the box.

H-5. **The box has no room for TC12's rows on the filed tier order.** §1.13: today's HEAD + the three pending closes ≈
 6,407,252 B on AM-X21's named figures, ≈ 6,371,842 B on today's measured sizes, vs WARN 6,400,000 (X's first-fit then fills
 the remainder, so the landed box ends just BELOW WARN). TC12's own report and append then push that box
 to WARN (publish only WARNs; REFUSE is above 11,200,000, so the close is not blocked), and effectively every TC12 row
 file is HELD. TC12's STEP Q (+12,209 B) by itself is larger than the slack X's forecast printed (2,244 B, on the
 forecast's own basis); the ferry of record re-plans on the box it finds. Anything else TC12 lands under `exchange/`
 before X's close takes that many bytes of rows away from X.

H-6. **`pool_lo_ms` must not move.** The trailing tide edges pool bars with open in `[lo, hi]` (tierc9 `_trailing_pool`); "a
 refresh with a different `lo` would re-band past entries" (LEANS_X.md:2025-2028). Pinned: 1567958400000
 (2019-09-08T16:00Z). X's disclosure: a +359-bar move re-bands 1 campaign (FIXTURES_X5.txt:35). If Stage D's top-up changes
 any CLASSIC5 first bar, the OLD band — and with it the third and fourth books — changes silently unless asserted.

H-7. **Substrate drift under an append-only ledger.** An appended row must re-derive byte-equal at every later pin. A top-up
 that re-fetches history and returns one different historical bar or funding print changes `net_r` / `funding_r` of a closed
 campaign → HALT at the next refresh (correct, but it stops the build). The new snapshot must be byte-identical to
 tc11_20260925 on the overlap (the same condition F-CTRL 0.000e+00 needs).

H-8. **Look-ahead seams in the re-ride.** (i) `armings9` scans the WHOLE tape, so a window end index may be a FUTURE bar —
 `known_window_end` (tierc11_books.py:396-401) and the exclusion of `window_end_*`, `open_at_asof`, `hi_i`, `continuation`,
 `entered_after_tc10_pin` from ledger rows exist for this; X's `v6_x_campaigns.parquet` still carries those pin-dependent
 columns. (ii) Symbol-keyed memos (`T5._FRAMES`, `LR._TIDE`) serve full-tape frames, so a refresh at an EARLIER pin in the same
 process is "the append and HALT law, not as-of value causality" (FIXTURES_X5.txt:27, :34; X-FIX X5-R2) — one process per pin.
 (iii) The entry bar's own streak is inside its edge sample (closed bar; causal; P-AGE-1's filed definition) — keep it.
 (iv) An OPEN campaign's `net_r` is a mark at the pin, never a result.

H-9. **Two chain laws, one field name apart.** Hashing a TC11-style line with forward_log, or the reverse, never verifies.
 `forward_log.append_entry` uses default `json.dumps` (NaN would be WRITTEN as `NaN`; X guards with `_native`) and a plain
 append (a crash mid-write leaves a torn line; TC11's writer used tmp + `os.replace`). Build the ledger in a scratch dir and
 move it into place whole.

H-10. **X's parquets are not in git.** `X:research_outputs/tierc11x/.gitignore:3-4` ignores `*.parquet` and `_det_*/`; the era
 tables, the X books and every va/ sfp/ exit/ parquet exist only on that worktree's disk and will not arrive with the merge.
 If the worktree is removed after X's close, TC12's mirrors lose their referee. Copy with shas now (R-18).

H-11. **The "tc11-stamp" default re-pins TC11's registry files.** `REGISTRATIONS.json` is `648834bf…` today, which is the sha
 X's `BOOK_SPECS.json` gate cites. After a re-pin the file sha changes; pin the P-AGE-1 / P-WIN-1 PAYLOAD shas (`e01a89ea…`,
 `d19a42a3…`), or read the texts before the stamp and say which. (The re-pin also meets TC11's own pending close and X's
 FRESH leg — another unit's hazard, flagged here because the fourth book's gate text hangs on it.)

H-12. **`data/fee_schedule.json` will be edited (maker-bps).** TC11's ledger rows carry `haircut_net_r` from `E.fees()`
 (tierc11_forward_ledger.py:190-194). A fee-derived field inside a chained row turns a fee-file edit into a ledger HALT (R-6).

H-13. **No ignore rule covers `research_outputs/tierc12/`** (`git check-ignore` returns nothing; M:.gitignore:284-288 covers
 tierc11 only). Parquet and `_det_*` twins would be picked up by a broad `git add`. TC11 appended its rules at the END of the
 root file "so that line numbers other lanes cite … stay put"; X used a nested `.gitignore` (which its merge allow-list
 permits). A nested `research_outputs/tierc12/.gitignore` touches no cited line.

H-14. **First-fit is order-dependent.** Which files are held depends on the order; an order chosen after sizes (or outcomes)
 are known is a selection. Freeze it in LEANS (R-16).

H-15. **Main is dirty in two tracked files.** `exchange/status/daily/DAILY_2026-10-08.md` (the routine's own appended publish
 block; rides the next publish) — X's ferry law HALTs on a box "measured from the working tree of a dirty exchange/ file",
 so measure blobs at the pinned HEAD, never the working tree. And `research_outputs/tierc10/close/FIXTURES_CLOSE_ledger_append_root.txt`
 (3 lines: the cited shas of `FIXTURES_RESUME.txt` and `PROGRESS.json`, and the F-DET transcript sha) — a TC10 close record
 already differing from HEAD, not TC12's doing. Do not `git add -A`, do not restore it; name it to the operator.

H-16. **The X worktree carries a stale `research_outputs/tierc11/`** (merge-base bytes, 26 files, no `forward/`). Reading TC11
 records from there silently reads superseded bytes.

H-17. **Era percentiles.** Every production percentile is trailing (F-ERA: "a future-inclusive window must FAIL"); the
 expanding windows are counts-only disclosures. A vendored copy must re-run F-ERA's causality legs against ITSELF — a mirror
 that only compares to X4's output on TC11's corridor cannot see a future-inclusive window introduced for new bars.

---------------------------------------------------------------------------------------------------------------
## 5 · REUSE PLAN

IMPORT directly (main tree, env-free):
- `scripts/forward_log.py` — the chain law, used verbatim a third time (`canonical`, `chain_hash`, `append_entry`,
  `verify_chain`, `read_lines`, `last_sha`, `GENESIS`).
- `scripts/publish_exchange.py` — READ by `ast.literal_eval` for the seven box names; never imported (LX-X6.7).
- Lineage through TC12's env shim (another unit builds it): `TP.corridor_n`, `TP.run_cell_n`, `TP.CONTROL_CARD`, `T9.V6_ROLES`,
  `T9.SWEEP_CELLS[-1]`, `T9.replay9`, `T9._trailing_pool`, `T9._trailing_edges`, `T9.card_candidates9`, `LR.tide_streak`,
  `LR._streak_band`, `TP.ride_spec`, `TP._book_sha`, `TP.stamp_n`, `TP.make_put`, `TP.CTRL_COLS`, `T5.cluster_boot`,
  `T5.cluster_boot_diff`, `TP.loao_n`.

VENDOR (copy the function bodies, print the source file's sha beside each; none of these modules can be imported outside its
own env, and none may be copied into main under its `tc11x_*` name):
- From `X:scripts/tc11x_forward.py` (`33f65b5e…`): `row_of`, `rows_of`, `_native`, `band_at`, `refuses_band`, `reride_gated`,
  `post_filter`, `admitted`, `split_closed`, `reride_differs`, `chained`, `append`, `book_open_body`, `ledger_state`,
  `_pending`, the body of `refresh`, `render_md`'s table shapes, `ROW_FIELDS`, `ROW_NULLABLE`, `KINDS`.
- From `X:scripts/tc11x_ferry.py` (`6594bbc2…`): the pure core lines 481-685 (`flat_name`, `identity_class`, `triage`,
  `load_table`, `to_csv_bytes`, `record_ends`, `cut`, `csv_facts`, `collisions`, `publish_constants`, `level`, `warn_line`,
  `project`), `fixed_order`'s shape, `plan_holds`, `render_rows_manifest`; constants `CAP_BYTES`, `CAP_RIVAL`, `ASSET_COLS`,
  `INSTANT_COLS`, `BAR_INSTANTS`, `BOOK_AXES`, `DRAW_COLS`, `TABULAR`, `SERIALIZER_CALL`, `READER_CALL`.
- From `X:scripts/tc11x_era.py` (`f1b42be4…`) + `tc11x_pct.py` (`49809c07…`): the whole stamp and table machinery (`derive`,
  `stamp_campaigns`, `bar_cells`, `occupancy`, `support_of`, `late_like_of`, `stage_a`, `level_stats`, `diff_stats`,
  `decompose`, `sentence_word`, `propensity`, `build_tables`, `finish_tables`, `BLOCKS`, `DISCLOSURES`, the constants of
  :150-201), with ONE new seam: `compute(book, pin)` in place of the hard-wired `load_book()` / `corridor()` / `tc11_reads()`.

MIRROR (re-express against TC12's env; assert equality with the filed record at TC11's pin):
- `tierc11_books.py`'s thin wrappers: `corridor`, `r912`, `v6_book`, `trg912_book`, `book_sha`, `tide_pool`, `campaign_rows`
  — anchor: v6 `f3c68f54…` / 200, 9/12 `2c32fd60…` / 199 at pin 1790294400000, `pool_lo_ms` 1567958400000.
- `tierc11_forward_ledger.py`'s listing of CONTINUATIONS and of OPEN entries marked to the pin (X lists only open keys) — the
  side-by-side page should carry both; and F-FWD's plant design (a planted opening refreshed at three pins; rows planted at
  lag 6 / 7 / 15 / 16 / 17 and band B3 / B4).
- TC10's forward strip (`tierc10_close_forward_strip.py`) for Stage C's never-scored extension: label text, the three
  membership classes, "counts and sums only".

PIN (sha-asserted reads; copies under `research_outputs/tierc12/x_rec/` for the X-worktree ones):

| record | sha256 |
|---|---|
| `M:research_outputs/tierc11/forward/FORWARD_LEDGER.jsonl` | `e53328add9e71f1c6198f724a131565a2a10ad2ad1600c36a74c6676f7ada288` |
| `M:research_outputs/tierc11/forward/FORWARD_LEDGER.md` | `52e839001f7ad6f1e13533a6d6745488dc587d11db25c3bfe6b0de66823413ec` |
| `X:research_outputs/tierc11x/forward/FORWARD_LEDGER.jsonl` | `4a6da7e89a3cf5f0127f76aca0d2ae12d218ffc06417c6528c70210092cfa4c5` |
| `X:research_outputs/tierc11x/forward/BOOK_SPECS.json` | `72a1f52359c66084d22f8bc99b0cd35e7edd89db2751f4859f559c8b1f51cac3` |
| `X:research_outputs/tierc11x/forward/FORWARD_LEDGER.md` | `64d4529670d1fcc730b194f2e7d885df05f7fb004c9dc45c0cec3b5656eb6572` |
| `M:research_outputs/tierc10/STEP0_RECORD.json` (the opening) | `3801e1c72149851de37b12775fe77f103fc47ab3fb1f08349dcbce709a97b5aa` |
| `M:research_outputs/tierc11/registrations/REGISTRATIONS.json` (P-AGE-1 `e01a89ea…`, P-WIN-1 `d19a42a3…`) | `648834bf30e20e92713bddef2374ddef1aae843f4d8ba152fc50166c8cc6f1ee` |
| `M:research_outputs/tierc11/books/v6_campaigns.parquet` | `aab06934ae92689ef2e0fcc6b857350cf397ddca7a0a57e180960c51669b28e5` |
| `X:research_outputs/tierc11x/books/v6_x_campaigns.parquet` | `7eb0bf4e552f9462b7532ee612b73c7610870c3f502c3844838054fd4088a05f` |
| `X:research_outputs/tierc11x/books/trg912_x_campaigns.parquet` | `8c22a9489142b9c54bf13f596d4153e5f9f8b62a87d994ac73a2cbd11f1ddf83` |
| `X:research_outputs/tierc11x/books/build_manifest.json` | `68d4a4a939026584d6b389050f131f99623f83c6fa22fa031260e3ee7a8cef06` |
| `X:research_outputs/tierc11x/era/X4_tables.parquet` (content `4f01ec8f…`) | `fda7a280b76e295b5faf06119061e3243461c50c6d0d941daecf1b4715a1e5b0` |
| `X:research_outputs/tierc11x/era/X4_stamps.parquet` (content `8dd0e6fc…`) | `e647a9f782a204ba70c8307d8b7fcce744528b433dd7f908a276ca31f0e95683` |
| `X:research_outputs/tierc11x/era/build_manifest.json` | `0ad7f6eac56a003bbcc694115f54f347dcb2d20895da414d1615410cfc34a642` |
| `X:research_outputs/tierc11x/era/X4.md` | `aac2be88b8d71f46c232a1976cd5d06dd5ded91b3356976050a48344e9557be8` |
| `M:research_outputs/tierc10/close/FORWARD_STRIP.md` / `.parquet` | `a59e438c…3872c4` / `4e118dc1…abba53` (full values in §1.10) |
| `scripts/forward_log.py` (both trees) | `74e9657fbcf26cce3040ee52d28a96bc1cf60897e375ba26a09b2e13676e1967` |
| `scripts/publish_exchange.py` (both trees) | `15eec3d0bf0420200d94fc3087e4868a59eecb5cdb1fc21e01b8c80daae8a65b` |
| `X:research_outputs/tierc11x/LEANS_X.md` / `LEANS_X_AMENDMENTS.md` | `74a989ee6357e2169f2ad88722b67f1174cf0d080783dc8c77f5f064e3468623` / `af845b95d1c7699f788aa242af6f5bef0d0f86b92a74a938cb7ca14c9d87d059` |
| `M:research_outputs/tierc11/LEANS.md` | `655e1605165e7a66c67f544e5cda421b46aa0b6fcd4cb97a6ad19654479f294f` |
| `X:research_outputs/tierc11x/ferry/FERRY_MANIFEST.json` | `604a055ce217421b0186072dec8b2f468a59082e826f1e5e4fc6b1af8342d41f` |

NEWLY WRITTEN for TC12:
1. The fourth book: the union gate read from the two filed scored-arm texts; its own spec document + sha; its `book_open`.
2. The four-book refresh at TC12's pin (one process), with `n_reride_differs` for BOTH gated books, the OPEN and CONTINUATION
   lists, and a side-by-side page of four columns with rows only (no aggregate).
3. F-LEDGER: prefix bytes == X's ledger; both ancestor files unchanged before and after the run (sha); lines 1-3 unchanged; the
   fourth book's spec sha re-derives and a bent gate text breaks it; every prior row (none today) re-derives; the gated rows
   are subsets of the base rows by key and row; an un-gated fourth book must FAIL; a row planted at lag 15 / 16 and band B3 /
   B4 is refused exactly by the texts.
4. The era refresh driver (`compute(book, pin)`), the v6 mirror leg against X4's content shas, per-book tables with `book` as
   an axis, the empty-OLD cells printed.
5. The TC12 ferry: typed class list, frozen order, off-bus staging, the forecast with named reservations, `FERRY_MANIFEST.json`,
   `ROWS_MANIFEST.md` (rendered, written only at the close act), the HELD list, F-ROWS legs (EXIST with HELD · RT · CUT ·
   SCOPE · FRESH · FORECAST).
6. A TC12 `close_acts.sh` step for the ferry of record (pin HEAD by value, re-measure, write the bus files, `publish()`),
   ordered after X's block.
