## L-L · THE FORWARD LEDGER, THE ERA AND THE FERRY

This section reads contract lines 108-112 (STAGE L) and the fixture F-LEDGER (:122). It governs: (A) the four frozen
books and what freezes each; (B) the ledger file of record, its two ancestors and the byte-level law by which the
chain continues; (C) the refresh — the forward origin, the admission filter, the re-ride, the row, what is listed and
not counted, the one refresh line at TC12's pin, the unscored law, the page, and the overlap of the ledger with
O-9's scored window; (D) the era tables refreshed with the gated books; (E) the ferry — scope, dialect, cap, box
measure, forecast, hold order, the HELD list and the ferry of record as a close act. It owns NO registered row. It
conforms to ORCHESTRATOR_RULINGS O-1..O-32 as written (O-3, O-4, O-9, O-21, O-24, O-28, O-29, O-31 and O-32 bind it
most); no objection to a ruling is filed. Every cite below uses the line numbers of the STEP Q bytes of the contract
(the prefix pinned in `T12/progress/STEP_Q.json`): STAGE L is lines 108-112; lines 104-106 are the scalper's
pre-named kill.

**Abbreviations.** `M` = `/Users/luis/Naiad` (main tree, branch `v12-v1-census`). `T12` = `research_outputs/tierc12`.
`T11` = `research_outputs/tierc11`. `XR` = `research_outputs/tierc12/x_rec` (the byte copies of TC11-X, in the MAIN
tree; every read asserted against its row of `XR/X_REC_MANIFEST.json`, O-4; the manifest's own sha is read through
`certified`). `certified(p)` = `tierc12_progress.certified(p)` (L-0.4): the `{record, bytes, sha256}` of the LAST
progress record that names the path `p`; HALT if none. "contract :n" = line n of the STEP Q bytes of
`exchange/queue/2026-10-08_TC12_APOLLO.md`. `E` = the TC12 env shim `scripts/tierc12_env.py` (L-D.25); `E.TP`, `E.T9`,
`E.T5`, `E.TB`, `E.LAB`, `E.R7` = `tierc10_panel`, `tierc9`, `tierc5`, `tierc2_baseline`, `tierc7_lab_regime`,
`tierc7_rules` as the shim exposes them. `W` = `E.TC11_PIN_MS` (the score edge); `PIN` = `E.PIN_MS`. `FL` =
`scripts/forward_log.py` (sha256 `74e9657f…1967`, 329 lines; stdlib only). `XF` =
`XR/scripts/tc11x_forward.py` (`33f65b5e…e80b`), `XE` = `XR/scripts/tc11x_era.py` (`f1b42be4…597b`), `XP` =
`XR/scripts/tc11x_pct.py` (`49809c07…4bb7`), `XY` = `XR/scripts/tc11x_ferry.py` (`6594bbc2…8f8f`), `XB` =
`XR/scripts/tc11x_books.py` (`26870ff9…3b2b`) — all read as TEXT, never imported, never executed. `LX` =
`XR/tierc11x/LEANS_X.md` (`74a989ee…8623`); `AMX` = `XR/tierc11x/LEANS_X_AMENDMENTS.md` (`af845b95…d059`). A sha
written `abcd…wxyz` is abbreviated orientation; the build reads the full value from the record named beside it.
**Tags.** [read here] = the cited source was opened while drafting. [measured here] = a sha, byte count, line count,
key name or row count taken from a filed record while drafting. [checked here] = re-opened while this text was
revised after the review. No outcome of any book was computed for this section: the only table values read were key
names, as-of stamps, row counts per table and the campaign counts `n` already printed in filed records.
**The fixture dialect** is L-0.14's. A leg is one `prove` call and one transcript block; a block id is `<FID>` or
`<FID> [<qualifier>]`, the qualifier a leg name, an instance (a directory or a grid) or `<leg> · <instance>`; a flow
leg of L-0.17 is the block `F-TYPED-FLOW [<pin name>]`. Inside a block the BREAK leg of named plants runs first and
each plant must be caught by its NAMED detector; then the REAL leg. A leg that cannot run prints NOT RUN, which is
never PASS; the tally line is `N GREEN, M RED, K NOT RUN`. No leg of this section makes a network call. Every suite
accepts `--root=DIR` and takes `--stage=<record id>` where it serves more than one record (never a leg filter). A
suite run at a record before `TC12-D` prints
`as_of_last_closed_4h: (pre-substrate stage)` and `substrate: none`. Fixture randomness is
`numpy.random.default_rng([E.SEED, crc32("<suite tag>|<block id>")])`, suite tags `forward`, `era`, `ferry`; the one
seeded draw of this section is F-ERA's pseudo-entries (count stated in L-L.23) — every other leg runs on the WHOLE of
a stated object and draws nothing.
**The port law** is L-D.11's, applied to three X sources: a ported function carries a provenance comment (source
file, lines, sha) and one label — VERBATIM (AST-identical to the X function), TEXT-ONLY (AST-identical once string
constants are blanked), CHANGED (the difference named in this section) or NEW. A literal inside a VERBATIM or
TEXT-ONLY port is the referee's (L-0.17 rule (G)); a module-level literal of an X source is READ from that source's
text by `ast.literal_eval`, never retyped; every CHANGED or NEW function holds structural literals only. Each suite
below carries a leg **F-PORT** that FAILS IF a port's label is untrue of the X text at its manifest sha (plants: one
token changed in a copy of a VERBATIM port; a comparator flipped in a copy of a TEXT-ONLY port; a provenance comment
naming another sha).

**The register of constants — every one READ, none typed.** The middle column is orientation only.

| constant | on file (orientation) | read at run time from | asserted equal to (HALT otherwise) |
|---|---|---|---|
| the opening `OPENING_MS` | 1790006400000 = 2026-09-21T16:00:00Z | `XR/tierc11x/forward/BOOK_SPECS.json` → `opening.ms` | `opening_ms` of ledger lines 1-3; `E.TC10_PIN_MS`; `research_outputs/tierc10/STEP0_RECORD.json` → `as_of_last_closed_4h_close_ms`; TC11's GENESIS line `opening_ms`; the L-T.6 text; contract :109 (L-L.8) |
| `n_min` | 30 | each book's own `book_open` line → `n_min` | `BOOK_SPECS.json` → `n_min`; TC11's GENESIS `n_score`; the L-T.6 text; contract :110 (L-L.14) |
| `pool_lo_ms` | 1567958400000 = 2019-09-08T16:00:00Z | `BOOK_SPECS.json` → `pool_lo_ms` | `books.gated-v6-oldtide.gate.pool_lo_ms`; `XR/tierc11x/books/build_manifest.json` → `pool_lo_ms`; the refresh's own `lo` (L-L.9) |
| the score edge (TC11's pin) | 1790294400000 | `E.TC11_PIN_MS` (L-D.26 hunk 3) | `BOOK_SPECS.json` → `opening_rival.ms` and `x_found_books.as_of_close_ms` |
| the pin (TC12's) | 1791489600000 | `E.PIN_MS` (L-D.1) | — |
| the OLD band code `OLD` | `B4` | the last element of `BAND_CODES`, the tuple read by `ast.literal_eval` from `XB`:181 (the port law) | the one capture of `tide_band == '([^']+)'` in `BOOK_SPECS.json` → `books.gated-v6-oldtide.gate.refuse`; the code L-C.4's campaign frame writes for the top band, by data (F-FWD-SUBSET, L-L.18) |
| band quantiles · pool floor | (0.25, 0.5, 0.75) · 30 | `E.LAB.STREAK_BAND_QUANTILES` · `E.R7.PROVISIONAL_MIN_N` | `gate.band_quantiles` · `gate.min_pool_bars` of the same record |
| the window-age cut `CUT` | 16 | the contract pin `adm.lag_cut` (:54; L-G files the row) through the pin door (L-0.17) | the one capture of `entry_i - arm_i >= (\d+)` in TC11's P-WIN-1 `operative_spec.scored_arm`; the fourth spec's `gate.components.stale.cut.value` (L-L.2, L-L.3) |
| the absolute stamp cut | 206 | `tierc12_books.abs_tide_cut()` (L-C.4: regex on TC11's P-AGE-1 text; X's law, `XB`:347-362) | `BOOK_SPECS.json` → `books.gated-v6-oldtide.gate.stamps_only.absolute_cut.value` |
| X's ledger | 5,643 B · 4 lines · sha `4a6da7e8…a4c5` · head `61ea177f…d89c` | `XR/X_REC_MANIFEST.json` row (`bytes`, `sha256`); the head by `FL.last_sha` | lines re-hashed by `FL.verify_chain` (L-L.5) |
| X's spec sha | `72a1f523…cac3` | the manifest row of `XR/tierc11x/forward/BOOK_SPECS.json` | `spec_sha256` of ledger lines 1-4 |
| TC11's ledger | 3,442 B · 2 lines · sha `e53328ad…a288` · head `0db88942…61cb` | `T12/progress/TC12-R0.json` → `frozen_estate_shas_at_r0["research_outputs/tierc11/forward/FORWARD_LEDGER.jsonl"]` | the file re-hashed; its chain re-verified by TC11's law (L-L.4) |
| filed book shas at the score edge | v6 `f3c68f54…9132` · 9/12 `2c32fd60…e030` | `BOOK_SPECS.json` → `x_found_books.book_sha` | TC11's REFRESH line `books.<b>.book_sha`; `XR/tierc11x/books/build_manifest.json` → `book_sha` |
| the STEP Q instant | 2026-10-08T22:52:13Z | L-D.1's object: `T12/progress/STEP_Q.json` → `commit` and the instant in `one_line` (from TC12-D on also `T12/data/AS_OF_PIN.json` → `step_q.instant`), as epoch ms | git's committer time of that commit (L-D's F-D-PIN) |
| the fourth book's freeze instant | (does not exist at drafting) | `T12/forward/BOOK4_FREEZE.json` → `committer_time_ms` (L-L.17) | the committer time of the commit that first adds line 5 of the ledger, by a fixture-side read-only git call (F-FWD-OVERLAP) |
| tier seed · X's era seed · draws | 20261008 · 20260925 · 4000 | `E.SEED` (contract :4) · `XR/tierc11x/era/build_manifest.json` → `seed` · `E.N_BOOT` | the pin door (pin `seed`) · — · the same manifest's `n_boot` |
| X4's content shas | tables `4f01ec8f…8bfa` · stamps `8dd0e6fc…d9c7` | `XR/tierc11x/era/build_manifest.json` → `sha.X4_tables`, `sha.X4_stamps` | `TB._content_sha` of the two `x_rec` parquet read back (L-L.21) |
| the era's own constants | 2000 / 300 / 500 / 365 / 90 / 90 / 8.0 / 5 / 1.5 / 0.05 / (0.05, 0.95) / 400 | `XE`, `XP` by AST (module literals) or inside VERBATIM ports | — |
| the CSV cap | 2 MB (:112) → 2,000,000 B | the pin `ferry.cap_mb` (:112) × `BYTES_PER_MB` (`scripts/tierc12_units.py`, L-0.17) | `CAP_BYTES` read by AST from `XY`:177 |
| the box constants | 16,000,000 · 0.40 · 0.70 · 64,000 | `ast.literal_eval` of seven module assignments of `scripts/publish_exchange.py` (sha `15eec3d0…a65b`) | `XR/tierc11x/ferry/FERRY_MANIFEST.json` → `box.constants` |
| the named reservations | — | the same record → `forecast_close.box_reservation.parts[]`, `forecast_close.box_after`, `forecast_close.worksheet.merge_target.x_delta_bytes` (L-L.29) | — |
| the identity vocabulary | six instant names, 26 axis words | `XY`:194-200, :212 by AST | — |

---------------------------------------------------------------------------------------------------------------
### A · The four frozen books

**L-L.1 THE FOUR BOOKS AND WHAT FREEZES EACH** — "fourth frozen book = v6 with P-ADM-1's refusal; all four books
(base · 9/12 · OLD-gated · combined-gated)" (contract :108-109)
READING: "frozen" means: the book's definition is a filed text whose sha is carried by a line of the hash chain, and
no later act may change that text without re-opening the ledger. No per-book parameter hash exists on disk; what
exists is one spec document for the first three books and, from TC12, one more for the fourth. The freeze INSTANT
of a book is the committer time of the commit that first carries its `book_open` line; for the fourth book that
instant is filed once, in `T12/forward/BOOK4_FREEZE.json` (L-L.17), and every row is flagged against it.

| contract word | book id | card · roles (read by object) | gate text (read by object) | spec document · sha | freeze record in the chain |
|---|---|---|---|---|---|
| base | `v6` | `card_name` "v6-control" · `roles_name` "v6-roles"; `ride_spec` = the 29 card fields and 6 roles fields of `BOOK_SPECS.json` → `books.v6.ride_spec` | none (`gate: null`) | `XR/tierc11x/forward/BOOK_SPECS.json` · `72a1f523…cac3` | line 1, `book_open`, `entry_sha256` `7f33aee6…3062` |
| 9/12 | `trg912` | "v6-control" · "trigger-9/12" (`roles_fields.trg_f` / `trg_s` differ from v6's; every other field equal) | none | the same document | line 2, `2fab0eb7…aac1` |
| OLD-gated | `gated-v6-oldtide` | "v6-control" · "v6-roles" | `books.gated-v6-oldtide.gate.text_of_record` = TC11's P-AGE-1 `operative_spec.scored_arm`, verbatim, payload sha `e01a89ea…5879` | the same document | line 3, `f747d827…d273` |
| combined-gated | `gated-v6-combined` | "v6-control" · "v6-roles" (the v6 `ride_spec`, copied by object) | the ONE element of TC12's `registrations[P-ADM-1].operative_spec.arms` that matches `` ^`scored`\s `` (L-G's payload), with its two components read by object from TC11's P-AGE-1 and P-WIN-1 payloads (L-L.2) | `T12/forward/BOOK_SPEC_COMBINED.json` · its own sha (L-L.3) | line 5, `book_open` (L-L.5); freeze instant in `forward/BOOK4_FREEZE.json` |

- The first three are frozen by X and are NOT re-frozen: TC12 writes no byte of their spec, their `book_open` lines
  or X's refresh line. Their definitions are read from `BOOK_SPECS.json` by key at every run.
- The role text on lines 1-2 ("X twin — TC11's ledger not yet opened") is frozen bytes. From TC12's first refresh
  line on, base and 9/12 are OF RECORD in TC12's ledger (O-24; L-L.4); the page says so in words and the frozen
  role text is printed beside, unedited.
- Before any ride, the refresh asserts `E.TP.ride_spec(E.TP.CONTROL_CARD, E.T9.V6_ROLES)` equals
  `books.v6.ride_spec` and the same call with the 9/12 roles object (`tierc12_books.r912()`, L-C.3) equals
  `books.trg912.ride_spec`, key for key (HALT `FWD-SPEC-RIDE`): the card that rides is the card the spec froze.
SOURCE: `XR/tierc11x/forward/BOOK_SPECS.json` (12,535 B; keys `books`, `book_order`, `opening`, `n_min`, `n_law`,
`pool_lo_ms`, `row_fields`, `path_modules`, `x_found_books`) [read here]; `XR/tierc11x/forward/FORWARD_LEDGER.jsonl`
lines 1-4 [read here; chain re-verified, L-L.5]; `XF`:324-406 (`spec_doc`), :610-613 (`book_open_body`);
`LX`:2047-2053 (LX-X5.3); scout U8 §1.4, §1.5; O-24.
RIVALS: re-issue four `book_open` lines under one new four-book spec — not taken: it re-opens the three existing
books, which the contract's F-LEDGER forbids ("append-only on the three existing books", :122). Freeze base and 9/12
by TC11's GENESIS line instead of X's lines — not taken: TC11's file is a different chain law and cannot be
continued (L-L.4); it is cited as an ancestor and held equal on every fact both files state.
FAILS-IF: blocks `F-LEDGER [PREFIX]` and `F-LEDGER [REHASH]` (L-L.7); F-FWD-SPEC (L-L.18) — plant: one card field
changed in a copy of the control card before the ride must HALT `FWD-SPEC-RIDE`.

**L-L.2 THE FOURTH BOOK — `gated-v6-combined`** — "fourth frozen book = v6 with P-ADM-1's refusal" (contract :108);
"refuse a trigger when the tide age at the entry bar is in the OLD band (trailing q75, the cut of record) OR the
window age (entry_i − arm_i) ≥ 16 bars" (:53-54)
READING: the fourth book is a POST-FILTER of the base book's forward rows (O-21; TC11 L-1.5): the v6 rows minus the
rows P-ADM-1 refuses, row for row, only the field `book` changed. No entry is admitted into a slot a refusal frees.
On a ledger row `r` of the v6 ride (L-L.10):
- `p_age_1_refuses(r) := (r.tide_band == OLD)`, where `tide_band` is the campaign's ENTRY-bar band: `run` =
  `E.LAB.tide_streak(sym)[1][entry_i]` (the two-state 89/316 tide's run, in 4h bars, the flip bar counted as 1);
  `edges` = `E.T9._trailing_edges(pool, f.open_ms[entry_i])["streak_bar"]` over `pool =
  E.T9._trailing_pool(pool_lo_ms, hi_ms)` — every CLASSIC5 4h bar with `run > 0` and open in `[pool_lo_ms, entry
  open]`, the entry bar's own row included, `None` below the pool floor; band index =
  `E.LAB._streak_band(run, edges)` (`numpy.digitize`, right-open), so OLD ⇔ `run ≥ q75`. **A `None` band HALTs**
  (`FWD-BAND-NONE`): the gate cannot decide, and the third book's frozen spec says `none_band: "HALT"`.
- `p_win_1_refuses(r) := (r.lag >= CUT)`, `lag = entry_i − arm_i` in 4h bars (a row field); `CUT` is the pin
  `adm.lag_cut`, read through the pin door at each call and never copied into a module constant.
- `p_adm_1_refuses(r) := p_age_1_refuses(r) or p_win_1_refuses(r)`.
- `book4 = {key: dict(r, book="gated-v6-combined") for key, r in v6_forward.items() if not p_adm_1_refuses(r)}`.
  The OLD-gated book is the same construction with `p_age_1_refuses` alone (`XF`:548-559, ported VERBATIM).
- **One implementation, in a module that never sees the value area.** The three predicates live in the env-free
  module `scripts/tierc12_forward_spec.py` (no env, no numpy, no pandas; on L-0.22's `VA_BLIND_T`) as pure
  functions of a row's `tide_band` and `lag`; `OLD` is bound there from the sha-asserted text `XB`:181 by
  `ast.literal_eval` (X's `OLD_BAND` form, `XF`:139).
  `scripts/tierc12_forward.py` (the ledger and the page) and `scripts/tierc12_era.py` (L-L.19) import them from it
  and hold no copy; the era module therefore never imports the ledger module, which opens the stamp tables
  (L-L.16). They are held equal to the registered row by data, not by wording: on the scored window, the keys they
  keep on the v6 book ridden to the score edge must equal the key set of L-G's `regbooks/P-ADM-1/scored.parquet`
  (written at full float by `tierc12_regbook.write_arm`, L-X.24; its sha through `certified`) — block
  `F-FWD-SUBSET [GATE-EQ]` — and the kept COUNTS must equal the `n` TC11 filed for the cells with (`age_gate_on`,
  `win_gate_on`, `ratr_gate_on`) = (True, True, False) and (True, False, False) in
  `T11/stage_g/g_grid_books.parquet` (read by those three boolean columns through `E.tc11_record`). P-ADM-1 has no
  precondition, so that regbook always exists and the leg is never CLOSED-NO-BOOK.
- **The texts of record, by object.** The fourth book's gate text of record is the ONE element of
  `registrations[P-ADM-1].operative_spec.arms` in `T12/registrations/REGISTRATIONS.json` (a list under L-X.18's
  carry law) that matches `` ^`scored`\s ``; HALT `FWD-GATE-TEXT` unless exactly one matches. It is filed as
  `gate.text_of_record` with `gate.text_sha256` (the sha256 of that element's UTF-8 bytes) beside
  `p_adm_1_payload_sha256` (the registration's payload sha). `operative_spec.scored_arm` is TC11's key and is read
  only from TC11's two payloads, the gate's components, in `T11/registrations/REGISTRATIONS.json`: P-AGE-1
  (payload `e01a89ea…5879`; HALT `FWD-OLD-TEXT` unless the text contains `B4 OLD` and `tierc9._trailing_edges` —
  X's own two assertions, `XF`:235) and P-WIN-1 (payload `d19a42a3…5084`; HALT `FWD-CUT-TEXT` unless
  `entry_i - arm_i >= (\d+)` matches exactly once and the integer equals the pin `adm.lag_cut`). TC11's registry
  is pinned by its chain head VALUE (`T11/registrations/REGISTRY_PIN.json["head"]`, asserted equal to the head
  recomputed from the payloads) and by the payload sha of each registration read — never by its whole-file sha,
  which the "tc11-stamp" close act moves while the payloads stay (L-0.24). X's third-book gate carries a
  whole-file key `registrations_sha256`; it is not carried into the fourth spec.
SOURCE: contract :53-54, :108; `T11/registrations/REGISTRATIONS.json` P-AGE-1 / P-WIN-1 `operative_spec.scored_arm`
and payload shas [read here]; `BOOK_SPECS.json` → `books.gated-v6-oldtide.gate` (`refuse`, `none_band`,
`lineage_functions`, `band_quantiles`, `min_pool_bars`, `pool_lo_ms`, `registrations_sha256`) [read here; keys
checked here]; `XF`:139, :225-237 (`gate_text_of_record`), :481-492, :548-559 [checked here]; `XB`:181 [checked
here]; `scripts/tierc9.py`:207-232 (`card_candidates9`: a candidate is `(ti, direction, arming)` with
`arming.arm_i`) [read here]; TC11 L-1.5 (`T11/LEANS.md`:141-150); L-X.18 (the carry law and its field grammar),
L-X.19; L-0.22, L-0.24; O-21; scout U5 §1.1-§1.3, §1.6; scout U8 R-3.
RIVALS: (a) the re-ride as the book of record (a refused candidate dropped before the one-position check, so a
later candidate may enter) — not taken: O-21; it is a disclosure count on every refresh line (L-L.12). (b) an
unbanded campaign "not refused" (TC11 Stage G's `old_refused`) — not taken: the frozen third book HALTs, and one
pass computes both gated books. (c) the arm-bar three-state age, or the absolute cut, as the OLD test — not taken:
both are stamps only in the frozen third spec. (d) type the cut — not taken: contract :8. (e) the predicates in
the ledger module, imported by the era — not taken: the era module is on `VA_BLIND_T` and the ledger module is not.
(f) the whole `arms` field, or TC11's key `scored_arm`, as the gate text — not taken: TC12's payload has no such
key (L-X.19), and the one `scored` element is the registered construction.
FAILS-IF: F-FWD-SUBSET and F-FWD-SPEC (L-L.18) — the gate-text plants: a second element beginning `` `scored` ``
added to a registry copy, and the leading token of the one element bent, must each HALT `FWD-GATE-TEXT`.

**L-L.3 THE FOURTH BOOK'S SPEC DOCUMENT AND ITS SHA** — "F-LEDGER (append-only on the three existing books; the
fourth re-hashes)" (contract :122); O-24 "The fourth book has its own spec document and sha"
READING: "the fourth re-hashes" = the fourth book's definition is hashed AFRESH into its own document, and its
`book_open` line names THAT sha; it never reuses X's spec sha, and X's document is never rewritten to hold four
books.
- **File.** `T12/forward/BOOK_SPEC_COMBINED.json`, rendered as X renders its spec (`json.dumps(doc, indent=2,
  sort_keys=True, ensure_ascii=False) + "\n"`, `XF`:409-410). Its sha256 is the fourth book's `spec_sha256`.
- **Content** (every value read from a named source; nothing typed): `tier`; `stage`; `contract` {path, prefix
  bytes, prefix sha}; `leans_sha256` and `registry` {path, `head`} (from TC12's filed registry); `book` =
  `gated-v6-combined`; `book_order` (X's three ids by object, then the fourth); `books.gated-v6-combined` {`role`
  "of record", `title`, `card_name`, `roles_name`, `ride_spec`, `panel` — the four last copied by object from
  `BOOK_SPECS.json` → `books.v6`; `runner` "the v6 ride, post-filtered" (X's key name for the ride function, kept
  so the four books share one page layout); `gate` {`kind` (X's sentence by object), `base_book` "v6",
  `text_of_record` and `text_sha256` (L-L.2's one `scored` element and its sha), `p_adm_1_payload_sha256`,
  `combine` "OR", `components.old` {the P-AGE-1 text, its payload sha, `refuse`, `lineage_functions`,
  `band_quantiles`, `min_pool_bars`, `pool_lo_ms` — by object from X's third-book gate; `code`, the one capture of
  `tide_band == '([^']+)'` in that `refuse`}, `components.stale` {the P-WIN-1 text, its payload sha, `refuse`,
  `cut` {`value` (the pin `adm.lag_cut`), the contract line, the TC11 capture}}, `none_band` "HALT", `stamps_only`
  (by object), `rivals`}}; `tc11_registry` {path, chain `head`, the two payload shas — no whole-file sha};
  `existing_books` {X's spec path of record and sha; the three `book_open` `entry_sha256` values, read from the
  lines}; `ancestors` (L-L.4); `opening`, `opening_rival`, `scored_window_end_ms` (the score edge, read from
  `T11/data/AS_OF_PIN.json["as_of_last_closed_4h_close_ms"]` and asserted equal to X's `opening_rival.ms`),
  `admission`, `append_law`, `n_min`, `pool_lo_ms`, `refresh_law`; `row_fields` (X's names by object from
  `BOOK_SPECS.json` → `row_fields`; 43 on file), `row_fields_added` — the six names (`p_age_1_refuses`,
  `p_win_1_refuses`, `p_adm_1_refuses`, `in_o9_scored_window`, `entered_before_contract_filed`,
  `entered_before_book_frozen`) (L-L.10), `row_nullable` (X's tuple by AST, `XF`:173-174), `ctrl_cols`; `flags`
  {the three flag definitions of L-L.17 as text; `step_q` {`commit`, `instant_ms`, `instant_iso`, read from
  `T12/progress/STEP_Q.json`}; `book_frozen` {`rule` "the committer time (ms) of the commit that first adds line 5
  of forward/FORWARD_LEDGER.jsonl", `record` "research_outputs/tierc12/forward/BOOK4_FREEZE.json"} — the instant
  itself cannot stand in a document that its own commit freezes}; `n_law` {`x_n_law` (X's sentence by object: `n`
  is counted per book and never combined); `row_set_of_record` {`every_book`: "in_o9_scored_window == false";
  `gated-v6-combined`: "in_o9_scored_window == false and entered_before_book_frozen == false"}; `beside`: "the
  all-rows figure, printed beside under the collar"; `chooser`: "none — the row set of record for any later score
  is fixed here; no later registration chooses"} (L-L.17); `chain` (X's block by object, plus the structure law of
  L-L.6 as text); `continuation` {X's prefix bytes and sha, the first TC12 line number, the declared difference
  from X's verifier}; `path_modules` = {path: sha256} of the 18 main-tree lineage files that X's `path_modules`
  names (hashed now; each must equal X's value; the three `tc11x_*` keys are not carried). TC12's own modules are
  not hashed into the spec (the ledger and era modules do not exist when it is filed); their shas are recorded on
  every refresh line (L-L.12).
- **Write-once.** `freeze_spec` writes the file once; an existing file must be rebuilt byte-equal from its
  sources, else HALT `FWD-SPEC-FROZEN` — "a changed module or text needs an AMENDMENT and a re-opened ledger"
  (`XF`:696-709). A re-opened ledger is a NEW file whose first bytes are again X's, the superseded one kept and
  cited; nothing is rewritten.
- **When.** At `TC12-REG.ledger-spec` — the dotted child of TC12-REG that L-0.10's `SUBSTAGES_T` lists for this
  section (blocking; `depends_on` `TC12-REG`). It is filed after the registry (it names P-ADM-1's payload sha and
  the registry head), has its own record and its own commit `tierc12(TC12-REG.ledger-spec): …`, and that commit
  is a PROPER DESCENDANT of the TC12-REG commit: it lands after the instant ATTEST-REG attests and is covered by
  ATTEST-ORDER's descendant test (L-X.21). It precedes `TC12-D` in `RESUME_ORDER_T`: the spec and the fourth
  `book_open` line (L-L.5) are committed before the build's substrate holds one bar past the score edge.
- **Producer.** `scripts/tierc12_forward_spec.py`, a plain process: stdlib, `FL`, `tierc12_progress.certified` and
  the pin door `scripts/tierc12_pins.py` (both filed at TC12-REG and importable with no env — the registry filer
  calls the same door there); no env, no numpy, no pandas; it reads no bar. The files it may open are typed in
  the module (`SPEC_READS_T`): the contract; `T12/progress/STEP_Q.json` and `TC12-R0.json` (and, through
  `certified`, the records it walks); TC12's `registrations/REGISTRATIONS.json` and
  `REGISTRY_PIN.json`; under `XR/`, X's ledger, X's spec and the texts `XF`, `XB`; TC11's
  `forward/FORWARD_LEDGER.jsonl`, `registrations/REGISTRATIONS.json`, `registrations/REGISTRY_PIN.json`,
  `LEANS.md`, `data/AS_OF_PIN.json` and `PROGRESS.json`; the 18 lineage files. Every read is sha-first: an X file
  against its manifest row (the manifest's own sha through `certified`); a TC11 file against the sha TC11's
  `PROGRESS.json` certifies, that file itself accepted at the sha
  `T12/progress/TC12-R0.json["frozen_estate_shas_at_r0"]` holds or at the stamped value L-0.24 allows (TC11's
  ledger is also held to the sha that key holds for it); TC11's two registry files are NOT asserted by file sha —
  the `head` in `REGISTRY_PIN.json` must equal the head recomputed from the payloads, and each payload read must
  hash to its filed payload sha (L-L.2); a TC12 file through `certified`. The tool never imports the
  shim, so it has no open log and writes no `READ_SET.json`: its value-area blindness (L-0.22 `VA_BLIND_T`) is
  held by AST and by `SPEC_READS_T` (F-FWD-SPEC). `forward/READ_SET.json` is the read set of that directory's one
  parquet writer, `scripts/tierc12_forward.py`, which is not on `VA_BLIND_T` (L-L.16). Where the module's
  functions run inside an ARMED process (the ledger at TC12-L, and its suite), they take every TC11, TC10 and X
  path from the shim's verified readers — `E.tc11_record`, `E.tc10_record`, `E.x_rec` — passed in by the caller;
  the module's own sha-first reader serves only the env-free run, so every such read in an armed process is a
  verified read (L-D.27).
- **After the commit.** The orchestrator writes `T12/forward/BOOK4_FREEZE.json` (L-L.17) immediately after the
  ledger-spec commit; no builder runs git.
SOURCE: contract :122; O-24, O-31; L-0.10 (T3; `SUBSTAGES_T` row `TC12-REG.ledger-spec`; `RESUME_ORDER_T`); L-0.4
(`certified`); L-X.21 (ATTEST-REG, ATTEST-ORDER); `XF`:324-410, :696-709 [read here]; `BOOK_SPECS.json` → `n_law`
(a sentence) [checked here]; L-D.29 (the 18 lineage files equal X's values, 18 of 18); scout U8 R-2, H-11.
RIVALS: (i) one new four-book spec replacing X's — re-opens three books. (ii) only the chain head moves, no new
document — then nothing freezes the fourth book's gate. (iii) freeze at TC12-L with TC12's own module shas inside
(X's form) — not taken: the earlier freeze is the stronger property (no strip bar is on disk yet), and code that
does not exist cannot be hashed into it; the code is held to the spec by F-FWD-SPEC and F-FWD-ANCHOR instead.
(iv) leave the row set of a later score to that score's registration — not taken: every appended row's `net_r` is
printed on the page, so no later choice can precede its look (L-L.17).
FAILS-IF: block `F-LEDGER [REHASH]` (L-L.7) and F-FWD-SPEC (L-L.18).

---------------------------------------------------------------------------------------------------------------
### B · The ledger file and its chain

**L-L.4 THE LEDGER OF RECORD AND ITS TWO ANCESTORS** — "all four books … re-ridden … and printed side by side"
(contract :109-110); O-24
READING:
- **Of record:** `T12/forward/FORWARD_LEDGER.jsonl` (tracked). It is TC12's own file. Its first bytes ARE X's
  ledger: `record[:N_X] == x_bytes`, `N_X` and the sha read from the manifest row of
  `XR/tierc11x/forward/FORWARD_LEDGER.jsonl`. X's file and TC11's file are never opened for writing (O-3; the shim
  refuses it, L-D.27).
- **Ancestor 1 — X's ledger** (same chain law; continued): four lines — `book_open` ×3, one `refresh` at the
  score edge — holding 0 rows. Cited in the fourth spec's `ancestors.x_ledger` {path of record
  `research_outputs/tierc11x/forward/FORWARD_LEDGER.jsonl`, the copy's path, bytes, sha256, `n_lines`, head}.
- **Ancestor 2 — TC11's ledger** (a different chain law; CITED, never appended, never continued):
  `T11/forward/FORWARD_LEDGER.jsonl`, two lines (`GENESIS`, `REFRESH`), 0 CAMPAIGN lines. Its law hashes
  `line_sha256 = sha256(canonical(line without line_sha256))` with `prev` INSIDE the line and `allow_nan=False`,
  and writes compact separators; under `FL.canonical` a field named `line_sha256` would be hashed into its own
  digest and could never verify (`LX`:2076-2079). So its head cannot be a `prev_sha256` of TC12's chain. It is
  cited in `ancestors.tc11_ledger` {path, bytes, sha256, `n_lines`, `genesis_line_sha256`, `head_line_sha256`, the
  chain law as text, `verified`}: the spec tool re-verifies it by TC11's OWN law, re-implemented with no TC11
  import (each line's bytes equal its canonical compact JSON; each `line_sha256` recomputes; each `prev` is the
  previous `line_sha256`, the first 64 zeros), and holds every fact the two ancestors both state EQUAL: the
  opening, `n_score` = `n_min`, the panel, each book's roles name and six periods (TC11's integers against X's
  repr strings), TC11's REFRESH `book_sha` per book against X's `x_found_books.book_sha`, and TC11's `open` key of
  the 9/12 book against X's `books.trg912.open_keys`.
- **What is of record where, from now on.** TC12's file is the ledger of record for all four books from its first
  refresh line (O-24; TC11 §11 Q5 enacted in fact, L-0.29). TC11's file stays at 0 rows; TC12 never refreshes it.
  X's owed adapter (AM-X9 (a): TC11's CAMPAIGN lines mapped to the control columns "at the first landing at which
  either side holds rows") stays not live: neither ancestor file gains a row. Listed for the operator.
SOURCE: both ledgers, whole [read here; measured here]; `scripts/tierc11_forward_ledger.py`:128-138 (`canonical`,
`seal`) [read here]; `AMX`:189-207 (AM-X9); `LX`:2070-2080 (LX-X5.4); `T12/progress/TC12-R0.json` →
`frozen_estate_shas_at_r0` [read here]; scout U8 §1.1-§1.3, R-1, R-8, H-1, H-9; O-3, O-24.
RIVALS: (b) a fresh chain whose first lines pin both ancestors — not taken: "append-only on the three existing
books" would then be a claim about copied content, not a byte-prefix property. (c) append in place to X's or
TC11's file — excluded by O-3 and by the three pending close acts, which re-verify those bytes.
FAILS-IF: blocks `F-LEDGER [PREFIX]` and `F-LEDGER [ANCESTORS]` (L-L.7).

**L-L.5 THE CONTINUATION, BYTE FOR BYTE** — "append-only on the three existing books" (contract :122); O-24
"continued under `scripts/forward_log.py`'s law"
READING: verified on the bytes while drafting [measured here]: X's ledger is 5,643 B, four lines of 457, 461, 441
and 4,284 B, each ending `\n`, no `\r`; every line's bytes equal `json.dumps(entry, sort_keys=True,
ensure_ascii=False) + "\n"` (default separators `", "` and `": "`); every `prev_sha256` is the previous line's
`entry_sha256` (line 1: 64 zeros); every `entry_sha256` recomputes; the head is `61ea177f…d89c`.
- **The law** (`FL`, called and never re-implemented in production): `canonical(entry)` = `json.dumps(body,
  sort_keys=True, separators=(",", ":"), ensure_ascii=False)` over the entry WITHOUT `entry_sha256` (the body
  INCLUDES `prev_sha256`) (:67-76); `chain_hash(entry, prev)` = `sha256((canonical(entry) + prev).encode("utf-8"))`
  (:79-82); `append_entry(entry, path)` refuses unless `entry["prev_sha256"] == last_sha(path)` and
  `entry["entry_sha256"] == chain_hash(entry, entry["prev_sha256"])`, then appends the default-separator dump and
  `"\n"` (:152-166); `verify_chain(path)` walks from 64 zeros (:209-232).
- **`FL`'s law permits the continuation.** `append_entry` and `verify_chain` test the two chain fields and nothing
  else: no field list, no kind list, no book count. A line whose `prev_sha256` is X's head is a lawful fifth line.
  What forbids a fourth `book_open` is X's OWN verifier (`XF`:636-638), a three-book law; TC12's structure law
  (L-L.6) admits exactly one more and says so.
- **Line 5** = `chained(body5, FL.last_sha(path))` (`XF`:590-594, VERBATIM), `body5` = X's `book_open_body` key set
  exactly: `kind` "book_open", `tier` "TIER-C12", `book` "gated-v6-combined", `role` "of record", `spec_sha256` =
  the sha of `BOOK_SPEC_COMBINED.json`, `opening_ms` and `opening_iso` (copied by object from line 1), `n_min`
  (L-L.14), `scored` false. Its `prev_sha256` is `61ea177f…d89c`. Written at `TC12-REG.ledger-spec` by the spec
  tool. Lines 6 onward — rows, then one refresh line — are written at TC12-L (L-L.11, L-L.12).
- **Two guards `FL` does not have**, applied by TC12's `append` (a CHANGED port of `XF`:601-607) before each
  `FL.append_entry`: (i) the line must serialise under `allow_nan=False` (`FL` would write a bare `NaN`); (ii) no
  string value anywhere in the line may contain a character `c` for which `("a" + c + "b").splitlines()` has more
  than one element — `FL.read_lines` splits on `str.splitlines()`, and with `ensure_ascii=False` the characters
  U+0085, U+2028 and U+2029 are written raw and would split one line into two [measured here]. HALT `FWD-NAN` /
  `FWD-LINE-BREAK`.
- **Atomic write.** `FL.append_entry` appends in place and can leave a torn line. Every TC12 write therefore works
  on a scratch copy `T12/forward/_det_build/FORWARD_LEDGER.jsonl` (git-ignored): the record's bytes (X's bytes when
  the record is absent) are copied there; the lines are appended through the guards; the scratch is verified
  (`FL.verify_chain`, L-L.6, and `scratch_bytes.startswith(record_bytes)`); then `os.replace(scratch, record)`.
  This is TC11's writer law (`scripts/tierc11_forward_ledger.py`:406-411).
- **The commit law.** The ledger is append-only across commits (L-0.5 lists it APPEND-ONLY THROUGHOUT). It is
  recorded by two records — `TC12-REG.ledger-spec` (five lines), then `TC12-L` (rows and one refresh line) — which
  L-0.4's last-record law names as lawful: the working file verifies under `TC12-L`'s entry, and the earlier
  entry is held to the blob at the ledger-spec commit, whose bytes must also be a byte-prefix of the working file.
  A refresh that fails its suites before the TC12-L commit is quarantined (L-0.4) and the record restored to its
  last committed bytes, which the spec tool reproduces byte for byte. After the commit a wrong line is never
  edited: the remedy is an amendment and a re-opened ledger (L-L.3).
SOURCE: `FL` [read here, whole]; the byte checks above [measured here, by an independent hash loop, no module of
the estate imported]; `XF`:590-613; `scripts/tierc11_forward_ledger.py`:406-411; scout U8 H-9.
RIVALS: call `FL.append_entry` on the record directly — a crash mid-write leaves a torn tracked line. Re-serialise
X's four lines instead of copying bytes — a re-serialisation is a rewrite; the prefix law is on bytes.
FAILS-IF: blocks `F-LEDGER [PREFIX]` and `F-LEDGER [CHAIN]` (L-L.7); F-FWD-HALT plants `FWD-NAN` and
`FWD-LINE-BREAK` (L-L.18).

**L-L.6 LINE KINDS AND THE STRUCTURE LAW** — "append-only on the three existing books; the fourth re-hashes"
(contract :122)
READING: `chain_findings(path)` — a CHANGED port of `XF`:616-648 — lives, with `chained`, the guarded `append` and
`book_open_body`, in the env-free module `scripts/tierc12_forward_spec.py` (the chain must be verifiable at
TC12-REG, before any env exists); `scripts/tierc12_forward.py` imports them from it. It returns a finding unless
ALL hold:
- S1 `FL.verify_chain(path)["ok"]`.
- S2 every `kind` is one of `BOOK_SPECS.json` → `chain.kinds` (`book_open`, `refresh`, `row`).
- S3 the raw bytes of lines 1-4 are X's ledger (the prefix law); lines 1-3 open X's `book_order` in order and name
  X's spec sha; line 4 is X's refresh.
- S4 exactly ONE `book_open` follows line 4; it is line 5; its `book` is the fourth id; its `spec_sha256` equals
  the sha of the bytes of `BOOK_SPEC_COMBINED.json` and differs from X's spec sha; its `opening_ms` and `n_min`
  equal those of lines 1-3.
- S5 every `row` line names one of the four books, carries exactly the row field set of L-L.10 plus the two chain
  fields, and no `(book, symbol, entry_ms)` occurs twice (`FWD-DUP-KEY`).
- S6 the pins of the `refresh` lines strictly increase (`FWD-REFRESH-TWICE`); the file never ends on a `row` line
  (`FWD-TORN-REFRESH`); inside one refresh block rows stand in book order, then `(entry_close_ms, symbol)`.
- S7 every row of a gated book has, earlier in the file, the base row of the same key, equal on every field but
  `book` (`FWD-SUBSET`).
**The declared difference from X's verifier:** X's `chain_findings` reports any `book_open` at index ≥ 3; run on
TC12's file it reports line 5, by design. X's file and X's module are untouched. The difference is recorded in the
fourth spec (`continuation.declared_difference_from_x_verifier`) and printed on the page.
SOURCE: `XF`:131, :136-137, :616-676 [read here]; `BOOK_SPECS.json` → `chain`, `book_order` [read here].
RIVALS: keep X's three-book verifier and store the fourth book in a second file — two chains for books the
contract prints side by side; not taken.
FAILS-IF: block `F-LEDGER [STRUCTURE]` (L-L.7).

**L-L.7 F-LEDGER** — "F-LEDGER (append-only on the three existing books; the fourth re-hashes)" (contract :122)
READING: five blocks whose FID is exactly `F-LEDGER` — `F-LEDGER [PREFIX]`, `[CHAIN]`, `[STRUCTURE]`, `[REHASH]`,
`[ANCESTORS]` — in `scripts/tierc12_forward_fixtures.py`. L-0.19's map matches the contract name to these five by
exact FID (never to L-X's `F-LEDGER-FMT`); the name is PASS only if every one of the five is PASS in every
transcript of record. The suite is run twice, each run a transcript of its own record:
`tierc12_forward_fixtures.py --stage=TC12-REG.ledger-spec` → `T12/forward/FIXTURES_LEDGER_SPEC.txt` (the five
blocks on the five-line file; at that record the suite imports the env-free module `tierc12_forward_spec` only
and prints the pre-substrate header), and `--stage=TC12-L` → `T12/forward/FIXTURES_LEDGER.txt` (the five blocks
again on the refreshed file, with L-L.18's family). Each block states its failure condition:
- **`F-LEDGER [PREFIX]`** — FAILS IF `record[:N_X] != x_bytes`, or sha256 of that prefix is not the manifest
  row's, or the ledger blob of any `tierc12(` commit is not a byte-prefix of the next commit's blob (a
  fixture-side read-only git call).
- **`F-LEDGER [CHAIN]`** — FAILS IF `FL.verify_chain` is not ok; the fixture's OWN hash loop (no `FL` call)
  disagrees with any `entry_sha256`; any line's bytes differ from the default-separator dump of its parsed entry
  plus `"\n"`; a line holds a bare `NaN` or `Infinity` token or a `splitlines` boundary other than its final
  newline.
- **`F-LEDGER [STRUCTURE]`** — FAILS IF any of S2-S7 of L-L.6 is breached.
- **`F-LEDGER [REHASH]`** — FAILS IF line 5's `spec_sha256` is not the sha of `BOOK_SPEC_COMBINED.json` as it
  stands; that document rebuilt now from its sources is not byte-equal to the file; lines 1-4 name any sha but
  X's; or the `x_rec` copy of X's spec no longer hashes to its manifest row.
- **`F-LEDGER [ANCESTORS]`** — FAILS IF X's ledger, X's spec, TC11's ledger or TC11's `FORWARD_LEDGER.md` hash
  differently before and after a production run or differently from their pins; TC11's chain does not verify
  under the fixture's own mirror of TC11's law; or a fact both ancestors state differs (L-L.4).
PLANTED MUTATIONS (scratch copies under `T12/forward/_det_fixtures/`, or under `--root`; each must be caught by the
named block):
1. *a rewritten earlier line* — one digit of line 2's `opening_ms` changed → CHAIN ("entry_sha256 does not match
   the line's own content") and PREFIX;
2. *the same rewrite forged through* — line 2 changed and every later `prev_sha256` / `entry_sha256` recomputed, so
   the chain verifies → PREFIX alone must catch it (this is why the prefix law is on bytes);
3. *a re-ordered line* — lines 2 and 3 swapped → CHAIN ("a line was inserted, removed or reordered") and PREFIX;
   two row lines swapped and left unchained → CHAIN; two row lines swapped and re-chained → STRUCTURE S6;
4. *a fourth `book_open` that reuses the old spec sha* — line 5 rebuilt with `spec_sha256` = X's, re-chained →
   REHASH (`FWD-SPEC-REUSED`) and STRUCTURE S4;
5. a second `book_open` for the fourth book appended later → STRUCTURE S4;
6. one character of the fourth spec's gate text bent in a copy → REHASH (the sha moves off line 5's);
7. one byte flipped in a scratch copy of TC11's ledger → ANCESTORS.
Control that must stay GREEN and is printed: the five-line file with one lawful row block and refresh line
appended.
SOURCE: contract :122; L-0.14 (blocks, leg states, the pre-substrate header); L-0.19 (the exact-FID map; the
hosting rows `TC12-REG.ledger-spec` and `TC12-L`); `XR/tierc11x/forward/FIXTURES_X5.txt`:21-23 (F-FWD-CHAIN's six
plants) [read here]; `FL`:209-232.
RIVALS: prove "append-only" by re-deriving X's four lines from sources — a comparison of content, blind to a
re-serialisation. A chain check alone — passes plant 2.
FAILS-IF: as stated; a plant not caught makes the fixture VOID and RED (L-0.14).

---------------------------------------------------------------------------------------------------------------
### C · The refresh

**L-L.8 THE FORWARD ORIGIN AND THE ADMISSION FILTER** — "re-ridden on the bars since 2026-09-21T16:00Z" (contract
:109)
READING:
- **The origin, by object.** `OPENING_MS` is read from `XR/tierc11x/forward/BOOK_SPECS.json` → `opening.ms` — the
  document the chain's first three lines name by sha. It is the same instant for all four books. HALT
  `FWD-OPENING` unless it equals every one of: `opening_ms` on ledger lines 1-3 and 5; `E.TC10_PIN_MS` (L-D:
  `T11/data/AS_OF_PIN.json` → `tc10_pin_close_ms`); `research_outputs/tierc10/STEP0_RECORD.json` →
  `as_of_last_closed_4h_close_ms` (read through `E.tc10_record`; the record is on the shim's TC10 allow-list);
  TC11's GENESIS `opening_ms`; the one capture of `It opens at \*\*(…Z)\*\* \(TC10's pin\)` in `T11/LEANS.md`
  (L-T.6); and the contract's own literal — the pin row `ledger.opening` (:109, `since (\d{4}-\d\d-\d\dT\d\d:\d\dZ)`,
  type iso, minutes precision) parsed to ms. The file value is what code uses; the contract's is compared.
- **Why that instant.** It is TC10's pin: the instant after which the base and 9/12 books were unseen when TC11
  opened its ledger (L-T.6), and the end of the corridor on which the OLD gate was pre-seen (LX-X5.2). The fourth
  book's gate was pre-seen on campaigns up to the score edge, four days later; L-L.17 shows the two openings admit
  the same v6-family campaigns.
- **Admission.** A campaign is admitted to a forward book iff `entry_close_ms > OPENING_MS`, strictly;
  `entry_close_ms = entry_ms + 4h` (`entry_ms` is the entry bar's open). An entry bar closing exactly at the
  opening is not admitted. Ported VERBATIM (`XF`:562-564).
SOURCE: contract :109; `BOOK_SPECS.json` → `opening`, `admission` [read here]; `research_outputs/tierc10/
STEP0_RECORD.json` [read here]; `T11/data/AS_OF_PIN.json` → `tc10_pin_close_ms` [read here]; `T11/LEANS.md`:430-431;
`scripts/tierc11_env.py`:140-158 (STEP0_RECORD on `TC10_ALLOW`) [read here]; `XF`:200-222, :562-564; `LX`:2036-2045;
L-D INTERFACE (L-L: `E.TC10_PIN_MS`).
RIVALS: type the contract's literal — contract :8. Open the fourth book at the score edge (the end of its own
pre-seen corridor) — not taken: the contract names one origin for "all four books"; membership is identical
(L-L.17) and the rival is printed on every refresh line (`opening_rival`).
FAILS-IF: F-FWD-ONCE (the admission plants) and `F-TYPED-FLOW [ledger.opening]` (L-L.18).

**L-L.9 THE RE-RIDE LAW** — "all four books … re-ridden on the bars since 2026-09-21T16:00Z" (contract :109)
READING: "re-ridden on the bars since" is the filed law of L-T.6 and LX-X5.3: **ride the WHOLE tape to the pin,
then filter.**
- `lo, hi, meta = corridor()` = `E.TP.corridor_n(CLASSIC5)` on the bound snapshot, HALT unless `hi + 1 ==
  E.PIN_MS`. **`lo` must equal `pool_lo_ms`** (the register's row), else HALT `FWD-LO-MOVED`: the trailing pool
  keeps bars with open in `[lo, hi]`, so a moved `lo` re-bands past entries.
- v6 = `E.TP.run_cell_n(E.TP.CONTROL_CARD, E.T9.V6_ROLES, CLASSIC5, lo, hi)`; 9/12 = `E.T9.replay9(s,
  E.TP.CONTROL_CARD, <the 9/12 roles>, lo, hi)` per CLASSIC5 asset in panel order — the two ride functions X's
  spec names under its key `books.<id>.runner`, reached through `tierc12_books.v6_book` / `trg912_book` (L-C.4).
  The campaign frame is L-C.4's `campaign_rows(book, roles, lo, hi, pool, name)` — the mirror of
  `scripts/tierc11_books.py:417-504`. This section reads `lag`, `entry_close_ms`, `exit_close_ms`, `era_of_entry`
  and the eleven tide columns from it; there is no port of `XB`:607.
- Then, in this order: `rows_of` (L-L.10) → `admitted` (L-L.8) → the two post-filters (L-L.2), applied to the
  ADMITTED v6 rows → `split_closed` (L-L.11).
- **Gated = post-filter.** The re-ride rival is run for BOTH gated books by `reride_gated(lo, hi, pool, refuse)`,
  which holds no replay loop of its own: it adapts this section's `refuse(band, lag)` predicate to the one hook of
  the estate, `tierc12_books.replay_h(sym, lo_ms, hi_ms, *, refuse=None)` (L-G.18), called per CLASSIC5 asset in
  panel order. The hook receives `ctx` (TC11's keys `sym`, `arm`, `ti`, `d`, `stp`, `atr`, `r_over_atr`); the
  adapter computes the candidate's entry-bar band `band_at(ctx["sym"], ctx["ti"], pool)` (a port of `XF`:481-487
  on `tierc12_books.band_of`) and `lag = ctx["ti"] − ctx["arm"].arm_i`; OLD-gated passes a predicate that ignores
  `lag`. Its rows are compared with the post-filter rows by `reride_differs` (VERBATIM, `XF`:582-586) and the two
  counts per book go on the refresh line. They are a disclosure of counts — printed, never held to zero, never an
  arm, never scored.
- **One process, one pin.** The ride of record runs once, at `E.PIN_MS`, in one process. Look-back rides in the
  same process (L-L.12's anchors) are index bounds on the same tape (L-D.28); they prove the append law and the
  cross-process anchor, and the transcript says they do not prove as-of causality of a memoised frame.
- **Snapshot read set, declared:** the five CLASSIC5 4h kline files and the five CLASSIC5 funding files (the ten
  `input_sha` paths of TC11's REFRESH line). `T12/forward/READ_SET.json` — written beside the directory's
  `build_manifest.json` by L-0.13's helper from `E.read_set()` — must hold no other snapshot path.
- **What the manifest carries for L-0.30.** `forward/build_manifest.json` holds, per ridden book and per re-ride,
  `ride_spec` (the control card and roles, by object) and `roles_name`, so F-NOT's ENTRY-CROSS, TRAIL-OFFSET and
  ADDS legs can read them.
SOURCE: contract :109; `T11/LEANS.md`:432-433 (L-T.6); `LX`:2054-2066 (LX-X5.3, with the rejected rival);
`XF`:481-538, :573-586 [read here]; `scripts/tierc11_books.py`:192-209 (`CAMPAIGN_COLUMNS`: it holds `lag`, the two
close instants, `era_of_entry` and every name of X's `TIDE_COLS`, `XB`:208-211) [checked here, by `ast`];
`BOOK_SPECS.json` → `books.<id>.runner`, `refresh_law` [read here]; `scripts/tierc9.py`:207-232 [read here]; L-C.4,
L-G.18; L-D.27, L-D.28; L-0.13 (`READ_SET.json`); scout U8 §1.8, H-6, H-8.
RIVALS: ride only the bars after the opening — REJECTED on file: "the ride needs the 316-bar warm-up and the
window's arming history" (`LX`:2065-2066). Gate inside the replay as the book of record — O-21. A second replay
loop in the ledger module (X's `reride_gated`, which swaps `card_candidates9` by global name) — not taken: one
function carries the refusal hook for every gate of the tier.
FAILS-IF: F-FWD-HALT (the moved-`lo` plant must HALT `FWD-LO-MOVED`), F-FWD-SUBSET and F-FWD-READS (L-L.18) — a
snapshot path outside the declared ten planted in a copy of `READ_SET.json` must be caught as `FWD-READ-SET`.

**L-L.10 THE ROW** — "printed side by side (first appended rows)" (contract :109-110)
READING: one `row` line per appended campaign per book.
- **Fields.** X's `row_fields`, read by object from `BOOK_SPECS.json` → `row_fields` (43 names on file) — `kind`,
  `book`, `symbol`, `entry_ms`, `direction`, `lane`, `roles_name`, `arm_i`, `arm_ms`, `lag`, `entry_i`,
  `entry_close_ms`, `exit_i`, `exit_ms`, `exit_close_ms`, `exit_reason`, `bars_held`, `entry_px`, `exit_px`,
  `stop_px`, `r_dist`, `atr_at_entry`, `net_r`, `gross_r`, `fee_r`, `funding_r`, `mfe_r`, `n_advances`,
  `harvested`, `harvest_ms`, `reached_1r`, `era_of_entry`, and the eleven tide columns — PLUS the six booleans the
  fourth spec names in `row_fields_added`:
  - three gate booleans, `p_age_1_refuses`, `p_win_1_refuses`, `p_adm_1_refuses` (L-L.2's predicates on the row's
    own `tide_band` and `lag`);
  - three freeze flags (L-L.17), `in_o9_scored_window`, `entered_before_contract_filed`,
    `entered_before_book_frozen` — functions of the row's `entry_close_ms` and of frozen instants only.
  The row's field count is `len(row_fields) + len(row_fields_added)`, computed and never typed; a `row` line is
  that set and the two chain fields.
- **Every row of every book carries the whole set.** On base rows the gate booleans say which campaigns each gate
  refuses — the out-of-sample record L-T.6 asks of every v6 row; on gated-book rows they are false by
  construction; on 9/12 rows they are stamps (no gate is applied to that book). The three flags are chained on
  every row because a later score's row set is defined on them (L-L.17): a flag that lived in a rebuildable side
  table could be recomputed after the rows' outcomes were public. No row line exists in either ancestor, so no
  row of an older schema stands in the chain; the extension is declared in the fourth spec and nowhere else.
- **Values.** `row_of` is ported from `XF`:437-463 (CHANGED only by the six booleans): the Trade's key, the
  twelve control columns at FULL float from the Trade object, the tide columns from the campaign frame before any
  rounding, `lag = entry_i − arm_i`. `_native` (VERBATIM, `XF`:414-434) HALTs on a NaN or a null outside
  `row_nullable` (`harvest_ms` and five tide columns; the six booleans are never null).
- **Pin-dependent fields are kept out.** No row carries a column of the campaign frame whose value depends on
  where the tape ends — in L-C.4's `CAMPAIGN_COLUMNS`: `open_at_asof`, `window_end_i`, `window_end_close_ms`,
  `window_open_at_asof` (X's own frame also held `hi_i` and `bound_i`) — nor that frame's two TC10-pin columns
  `continuation` and `entered_after_tc10_pin`, which restate the admission law (L-L.8, L-L.11). The field set is
  X's by object plus the six, so the exclusion holds by construction. Every row field is fixed once the campaign
  has closed — the three flags are pin-independent: the freeze instant is written once (L-L.17) — so an appended
  row re-derives byte-equal at every later pin, PROVIDED the tape's history and `pool_lo_ms` do not move (L-D's
  prefix identity; `FWD-LO-MOVED`).
- **No fee-schedule- or value-area-dependent field is chained.** The haircut twin, the fee decomposition and the
  VA vector live in the unchained side table (L-L.16), so a later fee-file or VA-code change can never HALT the
  ledger.
SOURCE: `BOOK_SPECS.json` → `row_fields` (43 names), `ctrl_cols` [read here]; `XF`:162-174, :414-478; `XB`:208-211
(`TIDE_COLS`); `scripts/tierc11_books.py`:192-209 (`CAMPAIGN_COLUMNS`, the as-of-dependent columns named above)
[checked here]; `XR/tierc11x/books/v6_x_campaigns.parquet` columns (`hi_i`, `bound_i`) [measured here];
`scripts/tierc11_forward_ledger.py`:94-108 (TC11's `ROW_FIELDS`, `AS_OF_DEPENDENT`) and :209-215 (its gate stamps
and chained haircut) [read here]; `T11/LEANS.md`:438-439; O-32 ("every pre-filing row flagged"); scout U8 R-6, H-12.
RIVALS: X's fields only on the three existing books and the booleans on fourth-book rows only — the booleans would
then sit where they are constant and be absent where they inform. The flags in the unchained side table — not
taken: they decide which rows a later score may read. TC11's 49-field row with the chained haircut — a fee edit
would HALT the ledger. A 7-15 shadow boolean (TC11's) — the TC12 contract names no such shadow, and its bounds
would be numbers no TC12 source supplies.
FAILS-IF: F-FWD-HALT (a row with a planted `window_end_i` → STRUCTURE S5; a planted NaN → `FWD-NAN`); block
`F-FWD-ANCHOR [PREFIX-STABLE]`; F-FWD-OVERLAP (the three flags) (L-L.18).

**L-L.11 OPEN, CONTINUATION, APPEND-ONCE, ORDER** — "printed side by side (first appended rows)" (contract :109-110)
READING: among the admitted campaigns of a book at the refresh pin:
- **CLOSED** ⇔ `exit_reason != "corridor_end"` (`XF`:138, :567-570, VERBATIM). A closed campaign not yet on the
  ledger is appended, exactly once, at the first refresh that sees it closed.
- **OPEN** ⇔ `exit_reason == "corridor_end"` (the ride the pin cut). Listed by key in the refresh line's
  `open_keys`; not appended; not counted in `n`. Its marked R is a mark, not an exit: it is never chained and never
  printed on the page (it is a column of the unchained listing table, L-L.16, labelled as a mark).
- **CONTINUATION** ⇔ `entry_close_ms <= OPENING_MS and exit_ms >= OPENING_MS` (TC11's predicate,
  `scripts/tierc11_forward_ledger.py`:253-257, mirrored): a campaign that straddles the origin. Never admitted, at
  any pin. Listed by key in `continuation_keys` for the two ridden books.
- **Order of appended lines** inside one refresh: books in `book_order`; within a book by `(entry_close_ms,
  symbol)` (`XF`:735-738, VERBATIM); then the one refresh line.
- **Every earlier row re-derives.** Before anything is appended, every row line already on the ledger must equal,
  under `FL.canonical`, the row the present ride gives for its key, and that campaign must still be closed; else
  HALT `FWD-ROW-CHANGED`, naming the moved fields. (No row line exists yet; the law binds every later refresh.)
- **Every earlier OPEN key is carried.** Each key in the previous refresh line's `open_keys` of a book must be
  among that book's admitted campaigns now — closed (appended in this refresh) or still open (listed again) — with
  the same `direction` and `entry_close_ms`; else HALT `FWD-OPEN-VANISHED`. This check is TC12's (X never ran a
  second refresh); it follows from the causality of an entry.
- A second refresh at the pin of the last refresh appends nothing and must agree with that line on every
  pin-determined field (HALT `FWD-REFRESH-DISAGREES`; `XF`:829-841, ported with TC12's added keys).
SOURCE: `XF`:562-570, :735-738, :772-788, :829-845 [read here]; `scripts/tierc11_forward_ledger.py`:238-257 [read
here]; `T11/LEANS.md`:434-435.
RIVALS: TC11's order by `(exit_close_ms, symbol, entry_ms)` — a different filed order; X's is taken because TC12
continues X's chain. Append an OPEN campaign with its mark — a mark is not a result.
FAILS-IF: F-FWD-ONCE and F-FWD-HALT (L-L.18).

**L-L.12 THE REFRESH LINE — ONE, AT TC12's PIN** — "re-ridden on the bars since 2026-09-21T16:00Z and printed side
by side (first appended rows)" (contract :109-110)
READING: exactly ONE `refresh` line is appended by this build, at `pin_ms = E.PIN_MS`. No intermediate pin is
refreshed: each pin is a separate look at the forward window. A refresh behind the last pin HALTs (`FWD-PIN-BACK`);
the ledger of record refuses any pin but the bound snapshot's (`FWD-PIN`); only a fixture's scratch ledger may take
another pin or opening.
Body, in X's key set (`XF`:812-828) with TC12's additions marked (+):
- `kind`, (+) `tier`, `pin_ms`, `pin_iso`, `opening_ms`, `pool_lo_ms`;
- `spec_sha256` (X's, with X's meaning) and (+) `spec_sha256_by_book` (four entries);
- `snapshot` {`substrate` (the Stage D manifest's snapshot name), `stage_d_manifest` + sha, `substrate_verify` +
  sha (L-D's `T12/env/SUBSTRATE_VERIFY.json`)};
- `code_shas` {path: sha} — the 18 lineage files of the spec's `path_modules` plus TC12's own path modules (the
  shim, the books module, `scripts/tierc12_forward_spec.py`, `scripts/tierc12_forward.py`); `code_drift_vs_spec` —
  the lineage paths whose sha differs from the fourth spec's (empty, or the shim's lineage pin has already
  HALTed);
- (+) `freeze` {`book4_freeze` (the path of `forward/BOOK4_FREEZE.json`), its `sha256`, `committer_time_ms`;
  `step_q_instant_ms`} — the two instants the row flags of this refresh were computed against (L-L.17);
- `as_of` — the nine `TP.AS_OF_COLUMNS` of the refresh's corridor (`XF`:541-544, VERBATIM), stamped with the PIN
  (L-0.13);
- `anchor_x_found_books` {`held`, `at_pin_ms`, `book_sha`}: **a look-back ride at `x_found_books.as_of_close_ms`
  (the score edge) must reproduce both filed book shas**, else HALT `FWD-ANCHOR` — the rides are then on the path
  TC11 and X filed, on a tape another process ended at that instant;
- (+) `prefix` {X's ledger bytes and sha, `held`} and (+) `ancestors` {TC11's ledger sha, `held`};
- `books.<id>` for the four ids: `n_appended`, (+) `n_record` (the count of appended rows in the row set of
  record, L-L.17 — a count, like `n`), `n_appended_this_refresh`, `appended_keys_this_refresh`,
  `open_keys`, `n_open`, `n_min`, `scored` false; (+) `continuation_keys` on the two ridden books; on each gated
  book `refused_keys` (the admitted base keys it refuses); on OLD-gated X's two rival key lists; (+) on the
  combined book `refused_by` {`old_only`, `stale_only`, `both`} as key lists. Keys only — no outcome value;
- `n_reride_differs`, `n_reride_differs_whole_tape` (the OLD-gated book's, X's meaning kept) and (+) the same two
  counts `_by_book` for both gated books;
- `opening_rival` {`opening_ms` = the score edge; per book `n_closed_admitted`, `open_keys`} — membership under
  O-9's strip start, printed beside, deciding nothing;
- (+) `overlap` (L-L.17) and (+) `carried_open` {`from_pin_ms`; per book each carried key and `appended` or
  `open`}.
No clock, worker count or load is written. The refresh line of the same pin is byte-identical across two builds
(F-DET, L-0.20; the twin starts from the record truncated after line 5).
SOURCE: line 4 of X's ledger (its body keys) [read here]; `XF`:741-845; `AMX`:163-185 (AM-X8: the nine stamps stay
on the refresh line; the chain's lines carry no collar); scout U8 R-9; L-D.28, L-D.30.
RIVALS: several refresh lines (one per day of the strip) — each is a look; not taken. Reuse X's scalar keys for
two books' counts — a key whose type changes between lines 4 and N; the scalars keep X's meaning and the new keys
carry both books.
FAILS-IF: F-FWD-ANCHOR; F-FWD-ONCE (the same-pin plant); `F-DET [forward]` (L-L.18).

**L-L.13 WHAT WAS "LISTED, NOT COUNTED" AT TC11's PIN, AND HOW EACH RESOLVES** — "(first appended rows)" (contract
:110)
READING: two campaigns were listed and not counted at the score edge.
- **The v6 ETH continuation** — key `[ETHUSDT, 1789718400000]` (entry bar open 2026-09-18T08:00Z), listed in
  TC11's REFRESH line under `books.v6.continuations_not_admitted`. It entered before the origin and closed between
  the two pins. **Resolution: it is never a ledger row.** Its entry close is not after the opening, at any pin. It
  appears in TC12's refresh line under `books.v6.continuation_keys`, and the continuation key sets of both ridden
  books must EQUAL the key sets TC11's REFRESH line filed (HALT `FWD-CONT-MOVED`): which campaigns straddle a
  fixed instant cannot change. It is a row of TC11's scored v6 book and of TC12's base arm; the page prints it as
  CONTINUATION — not counted, cited to TC11's line 2.
- **The 9/12 SOL open** — key `[SOLUSDT, 1790265600000]` (entry bar open 2026-09-24T16:00Z; entry close after the
  origin), listed in TC11's REFRESH `books.trg912.open` and in X's refresh `books.trg912.open_keys`. It is
  admitted. **Resolution, decided by the tape and stated either way:** if it is CLOSED at TC12's pin it is appended
  in this refresh as the 9/12 book's first row; if it is still OPEN it is listed again in `open_keys` and not
  counted. `carried_open` records which. Its `direction` and `entry_close_ms` must equal those TC11 filed (HALT
  `FWD-OPEN-VANISHED`).
- Nothing else was listed: at the score edge v6 held no open campaign, 9/12 no continuation, and the gated book
  no refused forward key (X's line 4).
- **"(first appended rows)" is a description, not a quota.** If no forward campaign of a book has closed by the
  pin, that book appends nothing; the refresh line still lands; the page and the report's §0.4 print "none yet".
  No row is manufactured and no pin is moved to find one.
SOURCE: TC11's REFRESH line and X's refresh line [read here]; `T11/forward/FORWARD_LEDGER.md` (the two listings)
[read here]; scout U8 §1.7, C-4.
RIVALS: admit the ETH continuation because it closed inside the forward window — breaks the admission law of
every book since L-T.6.
FAILS-IF: blocks `F-FWD-ANCHOR [CARRY]` and `F-FWD-ANCHOR [CONT]` (L-L.18).

**L-L.14 "UNSCORED UNTIL EACH BOOK'S OWN n ≥ 30"** — "unscored until each book's own n ≥ 30" (contract :110)
READING:
- `n_b` = the number of `row` lines of book `b` on the verified chain = its closed, admitted, appended campaigns.
  OPEN campaigns and continuations are not in `n`. `n` is counted per book and never combined, added across books
  or pooled (`n_law.x_n_law`, by object from X's spec). It is the contract's count (:110).
- `n_record_b` = the number of those row lines that lie in the row set of record the fourth spec's `n_law` fixes
  (L-L.17): rows with `in_o9_scored_window == false` and, for `gated-v6-combined`, `entered_before_book_frozen ==
  false`. Both are counts of row lines; neither reads a row's outcome.
- **Where 30 is read from:** at run time, from the book's own `book_open` line (`n_min`). On lines 1-3 that is X's
  filed value. On line 5 it is filed from the contract pin `ledger.n_min` (:110, `own n ≥ (\d+)`). HALT `FWD-NMIN`
  unless the four line values, `BOOK_SPECS.json` → `n_min`, TC11's GENESIS `n_score`, the one capture of `unscored
  until its own n ≥ (\d+)` in L-T.6 and the contract pin are one integer.
- **Status, per book** (`diary_status`, a CHANGED port of `XF`:862-864 — the one change is the clause after the
  dash): below `n_min`, "UNSCORED (n <n> < <n_min>) — of which <n_record> are rows of record for a forward
  score"; at or above it, "n <n> >= <n_min>: eligible for scoring by a filed registration only (not here) — of
  which <n_record> are rows of record for a forward score". The first half follows the contract's `n`; the clause
  says how many of those rows a later score may read. Reaching `n_min` changes a status string and nothing else:
  TC12 scores no forward book, and `scored` stays false on every line.
- **At this refresh, stated before any row exists:** every entry closes at or before TC12's pin, which precedes
  both the STEP Q instant and the fourth book's freeze instant, so `n_record` of `gated-v6-combined` is 0 whatever
  its `n`; for the other three books `n_record` is `n` less the rows flagged `in_o9_scored_window`.
- **Who scores, later.** Only a registration filed by a later tier, with its own family and bar, may score a
  forward book, and only on that book's rows of record; the same figure on all rows is printed beside under the
  collar. For P-ADM-1 that is the contract's "confirmation = the ledger's fourth book" (:55-56): the fourth
  book's rows of record are the only out-of-sample evidence for the combined refusal, none exists at this refresh,
  and TC12 prints no forward row as confirmation.
SOURCE: contract :110, :55-56; lines 1-3 (`n_min` 30) [read here]; `XF`:207-212, :862-864 [checked here];
`T11/LEANS.md`:436; `LX`:2082-2085; O-32.
RIVALS: `n` counts OPEN campaigns — a mark would count as a result. One `n` across the four books — three of them
share campaigns. `n_record` in place of `n` in the unscored-until test — not taken: the contract's count is `n`;
both are printed, and the row set a score may read is fixed either way.
FAILS-IF: `F-TYPED-FLOW [ledger.n_min]` (a scratch ledger holding `n_min − 1` rows must flip the first half of its
status string when the pin is bent down by one at its door), F-FWD-OVERLAP (`n_record` re-counted from the chain's
flags) and F-FWD-NOSTAT (L-L.18).

**L-L.15 NO AGGREGATE; THE PAGE "SIDE BY SIDE"** — "printed side by side (first appended rows)" (contract
:109-110); "the ledger's appended rows" (:127)
READING:
- **The diary law is X's, and it is the law of the chain TC12 continues:** no sum, mean, rate, win share,
  interval, p or any other quantity is computed over ledger row values — per book or across books — in the two
  forward modules, on the page, in the report or in the ledger append. `FL`'s own header prohibits it
  (:12-17). Per-row net R is diary-keeping and is printed. TC11's page printed "appended ΣR" per book; that print
  is NOT carried: of the two filed laws the stricter is taken, it is the law of the reused chain, and it cannot
  flatter an unscored book.
- **The page** `T12/forward/FORWARD_LEDGER.md` is a pure function of the two spec documents and the chain. Tables,
  each under the collar line of L-0.16:
  - `LEDGER-BOOKS` — four columns (base v6 · 9/12 · OLD-gated · combined-gated), X's rows (`XF`:896-919) extended:
    role (the frozen text) and "of record in this file" · card and roles · ride function (the spec's `runner`
    key) · gate · spec sha · opening · `book_open` line sha · freeze instant (the fourth book's, from
    `BOOK4_FREEZE.json`) · rows appended `n` · rows of record `n_record` · status · OPEN at the last refresh
    (keys) · CONTINUATION (keys) · `n_reride_differs` (forward window · whole tape) · refused in the forward
    window (keys) · under the rival opening: closed admitted · OPEN.
  - `LEDGER-ROWS` — the appended rows SIDE BY SIDE: one line per distinct `(symbol, entry_ms)` over the four books,
    in `(entry_close_ms, symbol)` order; identity columns (asset, direction, entry close, exit close, band, lag,
    the three flags of L-L.17); then one cell per book: the row's `exit_reason` and `net_r` where that key is a
    row of that book, suffixed "(not of record)" where the row is outside that book's row set of record;
    "refused (OLD)", "refused (stale)" or "refused (OLD + stale)" where a gated book refuses a base row; "—"
    otherwise. No totals line, no count line. With no row: one line "(none yet)".
  - `LEDGER-CARRIED` — the two listings of L-L.13, each with its resolution in words.
  - `LEDGER-REFRESHES` — per refresh line: pin, substrate, appended now per book, `n` and `n_record` per book,
    line sha.
  - The page prints the fourth spec's `n_law` whole, under `LEDGER-BOOKS`.
- §0.4 of the report prints `LEDGER-BOOKS` and `LEDGER-ROWS` WHOLE (L-X.28's frozen map); the other two tables
  are reached by one pointer row to this page.
SOURCE: `FL`:7-17; `XF`:16-19, :867-919; `XR/tierc11x/forward/FIXTURES_X5.txt`:43-45 (F-FWD-NOSTAT);
`scripts/tierc11_forward_ledger.py`:455-461 (TC11's ΣR print) [read here]; `LX`:2082-2094; L-X.14 (the `strip` leaf
carries no statistic); scout U8 §1.8 item 11, R-7.
RIVALS: TC11's ΣR per book — an aggregate over an unscored book. A totals line under `LEDGER-ROWS` — the same by
another name.
FAILS-IF: F-FWD-NOSTAT (L-L.18).

**L-L.16 THE SIDE TABLES — UNCHAINED** — "printed side by side (first appended rows)" (contract :109-110); "V5
STAMPS: every funnel instant of every book (base v6, 9/12, the gated books …)" (:44)
READING: three parquet files under `T12/forward/`, written by `scripts/tierc12_forward.py` (the one writer of that
directory's parquet) through L-0.13's `put` — the 6-dp table writer: declared key, the nine stamps, the collar
(L-0.16; none of the three is a registered table) — stamped with the PIN and recorded in
`forward/build_manifest.json` (which carries `registrations_sha256`), with `forward/READ_SET.json` beside it. None
is hashed into the chain; any may be rebuilt.
- `ledger_rows.parquet`, key `[book, symbol, entry_ms]` — the chain's row lines as a table (the row field set of
  L-L.10, the three flags included; the chain holds full float, this view the table law's rounding; the chain is
  of record).
- `ledger_side.parquet`, key `[book, symbol, entry_ms]`, one row per appended row — the twins and stamps that
  depend on a fee file or on Stage V and nothing else (the three freeze flags are row fields, L-L.10, and are not
  repeated here): `haircut_net_r`, `slip_bps_side`, `taker_bps_side`; the regbook interface's four fee columns
  `fee_taker_r`, `fee_maker_r`, `fee_all_taker_r`, `taker_twin_net_r` (L-X.24); the fee file's sha; and the V5
  vector AT THE ENTRY INSTANT.
  - **The V5 vector is read from Stage V's filed stamp tables.** `T12/va/stamps/VA_STAMPS_v6.parquet` and
    `T12/va/stamps/VA_STAMPS_trg912.parquet` are filed by L-V's reader at `TC12-V.stamps.c` (L-V.19), key `[book,
    symbol, entry_ms, instant_kind, instant_ms]`. The ledger module asserts each file's sha through `certified`
    before its first read, takes the row whose `instant_kind` is `entry` for the campaign's `(symbol, entry_ms)`
    — a `v6` row for the three v6-family books (a gated book is a key subset of `v6` and is never re-stamped), a
    `trg912` row for the 9/12 book — asserts its `instant_ms` equals the row's `entry_close_ms`, and copies the
    lens blocks of the typed tuple `SIDE_LENSES_T` = (`1h`, `4h`, `12h`, `1d`) (lens names; each block is the
    columns prefixed `<lens>_`) and `nest_gap_reason`, with the stamp table's path and sha. An appended row with
    no entry stamp HALTs `SIDE-VA-MISSING`.
  - **The 1w block is not copied.** The 1w value area is built on a borrowed lookback and may be read in exactly
    two places (O-28; L-0.25's `ONEW_READERS_T`), and the ledger module is neither. The side row carries the key
    and sha that point to the stamp row, where the `1w_*` block stands for whoever may read it. `SIDE_LENSES_T` is
    this stage's declared VA read list. (The 1d block's own nest columns — its boundary coincidence against the
    lens above — are 1d columns of the stamp table and are copied as filed; no `1w_` column is opened to copy
    them.)
  - The ledger module is a decision module (L-0.22): it joins filed columns and imports neither
    `analytics.value_area`, nor a door, nor the reader, and recomputes no state. It is not on `VA_BLIND_T`, because
    it opens these two files.
  - All four books are all-taker (the TC-series toll): by the fee identities of `tierc12_regbook` (L-X.24; the
    one implementation, called here and in F-FWD-SIDE) `fee_taker_r = fee_r`, `fee_maker_r = 0`,
    `fee_all_taker_r = fee_r`, `taker_twin_net_r = net_r`, and `haircut_net_r = net_r − fee_taker_r ×
    slip_bps_side / taker_bps_side`, the two rates per stem from `E.fees()` (`slippage_bps_side`,
    `taker_bps_side`).
  - **No maker twin of a v6-family row is built.** The "maker" ruling (contract :2-3, :101) is the scalper's toll;
    no filed law prices a 4h trend campaign's legs at the maker rate. The fee-decomposition columns above are the
    whole of this table's toll content.
- `ledger_listed.parquet`, key `[book, symbol, entry_ms]` — the OPEN campaigns and continuations at the last
  refresh: `listed_as`, `direction`, `entry_close_ms`, `entry_px`, `stop_px`, `pin_ms`, and for an OPEN campaign
  `mark_net_r_at_pin` with `mark_note` = "a MARK at the pin — not an exit, not a result".
- A table with no row is not written and is listed under `skipped_empty` — outside `regbooks/` the lineage's
  skip-empty law stands (L-0.13); the directory's fixture-typed file set is the typed set minus `skipped_empty`,
  each skipped name asserted empty by the fixture's own count (L-0.20).
SOURCE: L-X.24 (the sixteen and four columns, the fee identities, the haircut law); L-V.19, L-V.20 (the stamp
tables, their kinds and blocks); L-0.13, L-0.20, L-0.22, L-0.25; O-28, O-29, O-31; `scripts/
tierc11_forward_ledger.py`:190-194 (TC11's chained haircut); scout U8 R-6, H-12; contract :44, :101.
RIVALS: chain the twins (TC11) — refused in L-L.10. Compute a VA vector in the ledger module — it would import the
module the contract walls off (:25-26). Copy all five lens blocks — not taken: a third reader of the 1w block
(O-28).
FAILS-IF: F-FWD-SIDE (L-L.18); L-0.30's F-NOT leg 1W.

**L-L.17 THE LEDGER AND O-9's STRIP: THE OVERLAP WINDOW** — "re-ridden on the bars since 2026-09-21T16:00Z"
(contract :109); "the extension printed separately (the forward strip, never scored)" (:50); O-9
READING: the ledger opens at TC10's pin; O-9's strip opens at TC11's pin. The window between them,
`(OPENING_MS, E.TC11_PIN_MS]` — 2026-09-21T16:00Z to 2026-09-25T00:00Z, the 20 4h bars `T11/data/AS_OF_PIN.json`
counts under `bars_4h_past_tc10_pin` — lies INSIDE the scored window. A campaign whose entry bar closes in it is
both inside the window every registered row is scored on and admissible to the ledger. Stated plainly:
- **base v6, OLD-gated, combined-gated: NO such campaign exists.** TC11's filed v6 book holds 200 campaigns and
  none entered after TC10's pin; X's refresh line at the score edge reports, for `v6` and for `gated-v6-oldtide`,
  0 rows appended and no open key under the origin of record, and 0 closed admitted and no open key under the
  rival opening; the combined book is a subset of v6's rows. The base arm of P-ADM-1, P-BRD-1 and P-DIR-1 is that
  filed book, bit for bit (O-21). So no row of any registered arm is, or can become, a ledger row. The refresh
  asserts it — a v6 key with `OPENING_MS < entry_close_ms ≤ E.TC11_PIN_MS` HALTs `FWD-OVERLAP-V6` (it would
  contradict the filed book).
- **9/12: exactly ONE — the SOL campaign of L-L.13.** Its entry close (2026-09-24T20:00Z) is inside the scored
  window; it is admitted to the ledger. It belongs to NO registered arm of TC10, TC11, X or TC12: the 9/12 book's
  one registration was scored to TC10's pin, before this entry. What was seen of it is a mark at the score edge
  (filed in TC11's REFRESH line), not an exit. Under O-9 it is a row of the 9/12 book's scored-window table marked
  `corridor_end` at the score edge and is continued in the strip print; in the ledger it is a row when it closes.
- **The three flags — pin-independent, CHAINED on every row** (L-L.10; each a function of the row's
  `entry_close_ms` and of frozen instants):
  - `in_o9_scored_window` := `OPENING_MS < entry_close_ms ≤ W` (`W = E.TC11_PIN_MS`, the score edge);
  - `entered_before_contract_filed` := `entry_close_ms ≤` the STEP Q instant (L-D.1's object);
  - `entered_before_book_frozen` := `entry_close_ms ≤` the committer time (ms) of the commit that first adds line 5
    of `forward/FORWARD_LEDGER.jsonl`.
- **The freeze instant is filed ONCE,** in the write-once provenance record `T12/forward/BOOK4_FREEZE.json`
  `{commit, committer_time_ms, committer_time_iso, path, line}` — written by the orchestrator immediately after the
  `tierc12(TC12-REG.ledger-spec)` commit (the `STEP_Q.json` pattern: no builder runs git) and recorded by
  `TC12-D`'s record (L-0.5). The TC12-L builder reads it through `certified` and HALTs `FWD-FREEZE-ABSENT` if it
  is absent; F-FWD-OVERLAP holds it equal to git by a fixture-side read-only call (the F-D-PIN pattern).
- **What the refresh records:** `overlap` {`window` (the two instants), per book the admitted keys inside it};
  `freeze` (L-L.12); the three flags on every row line; `n_record` per book; the page's flag columns.
- **THE ROW SET OF RECORD FOR ANY LATER SCORE IS FIXED HERE,** in `BOOK_SPEC_COMBINED.json` → `n_law`, before a
  strip bar is on disk: rows with `in_o9_scored_window == false` and, for `gated-v6-combined`,
  `entered_before_book_frozen == false`. The all-rows figure is printed beside under the collar. No later
  registration chooses. The flagged rows count in `n` (the contract's count, :110) and not in `n_record`
  (L-L.14). The rule is fixed now because every appended row's `net_r` is printed on the page (L-L.15): a choice
  left to a later registration could not precede its look.
- **How TC11 and X handled the same overlap.** TC11 opened at TC10's pin "after which both frozen books are
  unseen" (L-T.6) while scoring to its own pin; its books carry the column `entered_after_tc10_pin`, and its ledger
  listed the one open campaign. X kept the opening and filed the argument: the gated arm is `pre_seen` up to TC10's
  pin; no v6 campaign enters in the overlap and the 9/12 book has one, still open — "So the choice is costless at
  the pin and cannot have been informed by any forward result"; and X printed the rival opening (TC11's pin) on its
  refresh line. TC12 keeps all three devices and adds the chained row flag and the fixed row set, because the 9/12
  campaign may now close.
- **For the fourth book specifically:** its gate was pre-seen on campaigns up to the score edge (O-23, O-30).
  Because v6 has no entry in the overlap window, the fourth book's forward membership is the same under the origin
  of record and under the score edge as origin; none of its forward rows was inside TC11's crossed table.
- **The fourth book's origin is BACKDATED, and that is flagged on every row** (O-32). Its gate text was filed with
  the contract at STEP Q and its definition was frozen on the chain later still — at the ledger-spec commit, when
  the spec's pool law, its HALT on an unbanded entry and its post-filter law were first carried by a line of the
  chain — yet it admits entries from the origin of record, more than two weeks before either. TC12's pin precedes
  the STEP Q instant, which precedes the freeze instant, so EVERY row any book appends at this refresh carries
  `entered_before_contract_filed` and `entered_before_book_frozen` both true. What stands behind those rows: no
  snapshot on this disk held a bar after the score edge when the contract was filed (scout U8 §1.7), and the
  fourth spec and its `book_open` line are committed before Stage D fetches one (L-L.3). That is evidence about
  the build, not about what was visible on a chart, and it earns no row a place in the row set of record: the
  binding flag for `gated-v6-combined` is `entered_before_book_frozen`, and `entered_before_contract_filed` is
  printed beside it. The fourth book's record that is forward of its own freeze begins with entries that close
  after the freeze instant — at a later refresh, not this one.
SOURCE: O-9, O-32; contract :55-56, :110; `T11/data/AS_OF_PIN.json` → `bars_4h_past_tc10_pin` [read here]; TC11's
REFRESH line (`n_rode`, `open`, `continuations_not_admitted`) and X's refresh line (`books.*`, `opening_rival`)
[read here]; `T11/LEANS.md`:430-431; `LX`:2036-2045; `T12/progress/STEP_Q.json` (`commit`, the instant in
`one_line`) [checked here]; L-D.1; L-0.5 (the write-once record); scout U5 §1.16 (`entered_after_tc10_pin` 0 of
200), H15; scout U8 §1.6.
RIVALS: move every book's origin to the score edge so that ledger and strip coincide — not taken: the contract
names the origin (:109), and the 9/12 campaign entered after the last instant any 9/12 score saw. Leave the
exclusion to the registration that later scores a book, or let it "print both ways" — not taken: that names no
score of record and lets the choice follow the rows' printed outcomes. Flag the fourth book's rows against the
STEP Q instant alone — not taken: between STEP Q and the ledger-spec commit the frozen spec was not yet on the
chain, and a row entered there would otherwise count as forward-of-freeze evidence.
FAILS-IF: F-FWD-OVERLAP (L-L.18).

**L-L.18 THE LEDGER'S OTHER FIXTURES** — "FIXTURES (each states its failure condition)" (contract :114)
READING: `scripts/tierc12_forward_fixtures.py --stage=TC12-L`, transcript `T12/forward/FIXTURES_LEDGER.txt` (the
record `TC12-L`). It hosts L-L.7's five `F-LEDGER` blocks on the refreshed file and the blocks below. The suite
imports no door, not `analytics.value_area` and not the reader. Scratch ledgers live under
`T12/forward/_det_fixtures/` (or under `--root`) and are built by the production functions with a scratch origin
= the first 4h close after the era cut (`E.ERA_CUT_MS`, by object), so that many forward campaigns exist. They are
refreshed at three look-back pins fixed by rule (the count is the fixture's commission): `P3` = the score edge
`W`; `P1` and `P2` = the 4h closes one third and two thirds of the way from the scratch origin to `W`, counted in
whole 4h bars (floor). Nothing in this suite is drawn at random.

| block | FAILS IF | planted mutations (each caught by its named detector) |
|---|---|---|
| **F-FWD-SPEC** | the fourth spec rebuilt from its sources is not the file; a spec value is not its source's (the v6 `ride_spec`; the gate text and its `text_sha256`; the two component texts and payload shas; TC11's chain head; the opening, `n_min`, `pool_lo_ms`; X's row names and the six added names; `n_law`); zero or several elements of P-ADM-1's `operative_spec.arms` match `` ^`scored`\s ``; one of the 18 lineage shas differs from X's; a ride's `TP.ride_spec` differs from its book's; (AST) the spec tool opens a path outside `SPEC_READS_T` or imports anything but the stdlib, `FL`, `tierc12_progress` and `tierc12_pins` | the `scored` element changed by one character in a registry copy → `FWD-SPEC-FROZEN`; a second element beginning `` `scored` `` added → `FWD-GATE-TEXT`; the element's leading token bent so that none matches → `FWD-GATE-TEXT`; P-WIN-1's text with the integer changed → `FWD-CUT-TEXT`; P-AGE-1's text with `B4 OLD` removed → `FWD-OLD-TEXT`; the fourth book's clause deleted from `n_law` in a spec copy → `FWD-SPEC-FROZEN`; a lineage file's sha altered in a spec copy → `SPEC-PATH`; `anchor_offset` changed on a card copy → `FWD-SPEC-RIDE`; `import numpy` planted in a copy of the spec tool → `SPEC-ENV-FREE` |
| **F-FWD-ONCE** | on the scratch ledger a closed campaign is appended twice, or not at the first refresh that sees it closed; an OPEN campaign is appended or counted; a campaign with `entry_close_ms == opening` is admitted; a same-pin refresh appends a line | the last row line appended again, re-chained → `FWD-DUP-KEY`; `is_closed` bent to admit `corridor_end` → `ONCE-OPEN`; the admission comparator bent to `>=` → `ONCE-ADMIT` (a row planted at the opening); a second refresh at one pin made to append → `FWD-REFRESH-TWICE` |
| **F-FWD-HALT** | a planted change to an appended row does not HALT; a moved `pool_lo_ms` does not HALT; a NaN or a line-break character is written; a pin behind the last refresh is accepted | `net_r` of one appended row moved by one ulp, re-chained → `FWD-ROW-CHANGED`; `lo` moved one bar → `FWD-LO-MOVED` (the count of re-banded campaigns printed as a disclosure, AM-X5); a NaN in a row → `FWD-NAN`; U+2028 in a string field → `FWD-LINE-BREAK`; an earlier pin → `FWD-PIN-BACK`; a row carrying `window_end_i` → STRUCTURE S5 |
| **F-FWD-SUBSET [KEYS]** | a gated book is not "base minus its refused" by key and row; the combined book is not a subset of the OLD-gated book; a boundary row is misjudged; the predicates are not the functions of `tierc12_forward_spec` (AST: a second definition in the ledger or era module) | an UN-GATED fourth book (the predicate refusing nothing) → `SUBSET-KEYS`; the OR bent to AND → `SUBSET-KEYS`; rows planted at `lag = CUT − 1` (kept) and `lag = CUT` (refused), and at the bands just below OLD (kept) and OLD (refused) → `SUBSET-EDGE` when either comparator is bent; the band read at the arm bar → `SUBSET-KEYS`; a `None` band → `FWD-BAND-NONE`; a copy of the predicate planted in a copy of the era module → `SUBSET-ONE-IMPL` |
| **F-FWD-SUBSET [GATE-EQ]** | at the score edge the keys the predicate keeps on the v6 book differ from the key set of `regbooks/P-ADM-1/scored.parquet` (L-G; sha through `certified`), or the kept counts differ from TC11's two filed `n` (L-L.2) | one key dropped from a regbook copy → `GATE-EQ-KEYS`; the window-age comparator bent to `>` → `GATE-EQ-KEYS` |
| **F-FWD-ANCHOR [ANCHOR]** | the look-back rides at the score edge do not reproduce the two filed book shas | a one-tick stop perturbation in the ride → `FWD-ANCHOR` |
| **F-FWD-ANCHOR [PREFIX-STABLE]** | a campaign closed at the score edge has a row that differs, on any field of the row set, between the look-back ride and the ride of record | a pin-dependent column (`window_end_i`) smuggled into `row_of` → `PREFIX-STABLE` |
| **F-FWD-ANCHOR [CARRY]** | a key of the previous `open_keys` is absent now or changed its `direction` or `entry_close_ms` | the SOL key removed from a ride copy → `FWD-OPEN-VANISHED` |
| **F-FWD-ANCHOR [CONT]** | the continuation key sets differ from the sets TC11's REFRESH line filed | the ETH continuation admitted → `FWD-CONT-MOVED` |
| **F-FWD-READS** | `forward/READ_SET.json` holds a snapshot path outside the declared ten (L-L.9), a path under `T12/va/` other than the two stamp tables of L-L.16, or differs from the set the F-DET twin re-derives | one undeclared snapshot path planted in a copy → `FWD-READ-SET`; `va/va_bars_4h.parquet` planted in a copy → `FWD-READ-SET` |
| **F-FWD-OVERLAP** | a v6-family key lies in the overlap window; the 9/12 overlap key set is not exactly the one key X's line 4 lists; on any row line one of the three flags differs from the fixture's own re-derivation from `entry_close_ms` and the instants (`OPENING_MS`, `W`, the STEP Q instant, the freeze instant); `forward/BOOK4_FREEZE.json` is absent, its `commit` is not the commit that first adds the ledger file with line 5 (a fixture-side read-only git call, the F-D-PIN pattern), or its `committer_time_ms` is not that commit's committer time; an `n_record` on the refresh line or the page is not the count of the chain's rows in the row set `n_law` fixes; the page does not print `n_law` | a v6 row planted in the window → `FWD-OVERLAP-V6`; the overlap flag computed with the pin in place of the score edge → `OVERLAP-FLAG`; the contract flag computed against the origin in place of the STEP Q instant (every row would read false) → `BACKDATE-FLAG`; the freeze flag computed against the STEP Q instant, on synthetic rows planted between the two instants → `FREEZE-FLAG`; one digit of `committer_time_ms` changed in a copy of the freeze record → `FREEZE-RECORD`; `n_record` counted without the fourth book's freeze clause → `RECORD-SET` |
| **F-FWD-NOSTAT** | the source of `tierc12_forward.py` or of `tierc12_forward_spec.py` holds an aggregate over row values (AST and token scan: `sum(`, `.sum(`, `.mean(`, `np.mean`, `statistics`, a division by a row count, a cumulative op); the page holds a total, an average or a share | a planted `sum(` over `net_r`; a planted `np.mean`; a "Σ" line added to a page copy → each `NOSTAT` |
| **F-FWD-SIDE** | a side row breaks one of `tierc12_regbook`'s fee identities or the haircut law at the rates of `E.fees()`; a VA column differs from its stamp-table source row, or that row's `instant_ms` is not the row's `entry_close_ms`; a stamp table is read before its sha is asserted through `certified`; the side table holds a column outside the blocks of `SIDE_LENSES_T` (a `1w_` column) or one of the three flags; a chained line holds a side column; a bent fee rate moves a chained byte | the taker rate bent at its door → the side table moves and the chain's bytes do not (`SIDE-UNCHAINED` if they do); a VA column taken at `instant_kind == "exit"` → `SIDE-VA`; a fifth lens block copied → `SIDE-1W`; one byte bent in a stamp-table copy → `SIDE-SHA`; `haircut_net_r` added to `row_of` → STRUCTURE S5 |
| **F-FWD-STRIP** | the ledger's closed v6 and 9/12 rows are not, key for key and on the twelve control columns at the table law's rounding, the closed strip rows of L-C's `books/strip.parquet` (sha through `certified`) plus, for 9/12, the overlap key | one strip row dropped in a copy → `STRIP-KEYS` |
| `F-DET [forward]` · `F-KEY [forward]` · `F-COLLAR [forward]` · `F-PORT` | L-0.20 on the TC12-L writer's outputs — the fixture-typed file set is `FORWARD_LEDGER.jsonl`, `FORWARD_LEDGER.md`, the three side tables less `skipped_empty`, `build_manifest.json` and `READ_SET.json`; the twin starts from the record truncated after line 5, and `BOOK_SPEC_COMBINED.json` and `BOOK4_FREEZE.json` are its INPUTS, copied in and required byte-unchanged after it (a twin that rewrites either is RED) / L-0.21 / L-0.16 on `forward/`; the port law above | L-0's plants; the three port plants; a twin made to rewrite the freeze record → `DET-INPUT` |
| `F-TYPED-FLOW [ledger.opening]` | the pin bent by one 4h bar at its door does not change the admitted set of the scratch ledger | a typed copy of the opening in a copy of `admitted`'s caller → `PIN-NOT-READ` |
| `F-TYPED-FLOW [ledger.n_min]` | on a scratch ledger holding `n_min − 1` rows, the pin bent down by one at its door does not flip the first half of the status string (L-L.14) | a typed copy of the count in a copy of `diary_status`'s caller → `PIN-NOT-READ` |
| `F-TYPED-FLOW [adm.lag_cut]` | the pin bent down by one at its door does not flip `p_win_1_refuses` on the planted `lag = CUT − 1` row | the cut copied into a module constant of a copy of the spec module → `PIN-NOT-READ` |

SOURCE: `XR/tierc11x/forward/FIXTURES_X5.txt` (X's ten fixtures and their plant designs) [read here]; `AMX`:95-109
(AM-X5); `LX`:2352 (the F-FWD row of X's roll); L-0.14, L-0.17 (the flow leg), L-0.19 (the hosting row), L-0.13.
RIVALS: none.
FAILS-IF: n/a (this reading is the roll).

---------------------------------------------------------------------------------------------------------------
### D · The era

**L-L.19 "X4's ERA TABLES REFRESHED WITH THE GATED BOOKS"** — "X4's era tables refreshed with the gated books
(Tier-E)" (contract :110-111)
READING:
- **The gated books** are the two gated books of the sentence that precedes the clause: OLD-gated and
  combined-gated. Three books are tabled — `v6` (the mirror of X4's own tables), `gated-v6-oldtide`,
  `gated-v6-combined` — with `book` as a key axis. The 9/12 book is not a gated book and is not tabled.
- **The corridor is the scored window** (O-9): campaigns with `entry_close_ms ≤ W` (`W = E.TC11_PIN_MS`), tapes
  cut at that instant; `era = E.era_of(entry_close_ms)`. The tables hold intervals, and O-9 forbids pooling a
  strip campaign into a CI; an extended-corridor twin is therefore not built. On this corridor the v6 tables must
  reproduce X4's.
- **Membership.** `v6` = the scored-window v6 campaign table L-C files, `T12/books/v6_campaigns.parquet` (the
  filed book, O-21; its sha through `certified`). Each gated book = the v6 campaigns kept by L-L.2's predicates —
  the functions of `tierc12_forward_spec`, the same ones the ledger uses — on the campaign table's `tide_band` and
  `lag`; the rows are v6's rows (same `net_r`). Held equal by key to `regbooks/P-ADM-1/scored` (L-G; through
  `certified`) for the combined book and to TC11's filed `regbooks/P-AGE-1/scored.parquet` (through
  `E.tc11_record`) for the OLD-gated book.
- **All ten tables, per book:** E-1, E-1d, E-2, E-2c, E-2p, E-3, E-3p, E-4, E-4d, D-1 — X4's table set, with X4's
  blocks, cells, sides and readings (`XE`:244-293), by the mirrored build of L-L.20. The row count per book is the
  row count of X's filed table (1,458 on file), read from it and re-derived from the block table; it is not typed.
- **Tier-E.** Every row carries the collar and `promotable` false; no row carries a verdict word; the templated
  era sentence (`XE`:1710 ff.) is printed per book with X's prefix "TIER-E — a SELECTION, not a result —". Nothing
  here is registered, promoted or scored (O-13).
- **Outputs** under `T12/era/` (one writer, `scripts/tierc12_era.py`, through L-0.13's `put`):
  `ERA_tables.parquet`, key `[book, table, block, reading, cell, side]`; `ERA_stamps.parquet`, key `[symbol,
  entry_ms]` (X4's stamp columns for the v6 campaigns of the filed book — 200 on file — plus two membership
  booleans, `in_gated_oldtide`, `in_gated_combined`); `ERA.md`; `build_manifest.json`; `READ_SET.json`;
  `FIXTURES_ERA.txt`. All stamped with the SCORE EDGE (L-0.13).
- **`ERA.md` is the stage document of record.** It prints every table whole for every book (L-L.22); the report
  does not reprint the grid and carries one pointer row for `ERA_tables` — path, sha, cell count (L-X.28's frozen
  map; L-0.15: a pointer to a grid printed whole in its stage document is not an abbreviation).
SOURCE: contract :108-111; O-9, O-13; `XR/tierc11x/era/X4_tables.parquet` (1,458 rows × 116 columns; table counts
E-1 376 · E-1d 188 · E-2 44 · E-2c 236 · E-2p 2 · E-3 224 · E-3p 80 · E-4 184 · E-4d 92 · D-1 32) and
`X4_stamps.parquet` (200 × 176) [measured here: counts, columns, stamps only]; `XE`:216-293; `LX`:1821-2013
(LX-X4.1 … X4.12); L-X.28 (the whole-versus-pointed map), L-0.15; scout U8 §1.11, R-10, R-12.
RIVALS: the extended corridor — pools strip campaigns into intervals (O-9). "The gated books" = every TC12 gate's
kept book (P-BRD-1's, P-DIR-1's) — not taken: the clause sits inside Stage L's sentence about its four books, and
tabling a breadth-gated book by breadth thirds is circular; listed for the operator. Include 9/12 — not a gated
book. Reprint the three books' tables in the report — not taken: the report has a per-file cap and the map of
what it prints whole is frozen before any verdict (L-0.10 T4).
FAILS-IF: F-ERA-BOOKS and `F-GRID [ERA_tables]` (L-L.23).

**L-L.20 THE MIRRORED BUILD** — "X4's era tables refreshed" (contract :110); O-4 "MIRRORED into `tierc12_*` code,
with the X function it mirrors named, and held equal to X's filed records by a fixture"
READING: `scripts/tierc12_era.py` and `scripts/tierc12_pct.py` are PORTS of `XE` and `XP` under the port law; no
`tc11x_*` module is imported. Both are decision modules on L-0.22's `VA_BLIND_T`: they import nothing under
`analytics`, not the reader and not the ledger module, and `era/READ_SET.json` must hold no path under `T12/va/`.
- VERBATIM: `third_midrank`, `third_share`, `_bar_at`, `tide_law`, `rv30`, `rv_rel`, `funding_8h`, `_counts`,
  `_pool`, `derive`, every `_stamp_one` helper and `_stamp_one`, `cells_of`, `stamp_campaigns`, `_hq`, `bar_cells`,
  `breadth10_members`, `stamps_frame`, `_sides_of_bars`, `occupancy`, `occ_law_findings`, `support_of`,
  `_side_mask`, `late_like_of`, `quantile_replay_findings`, `compositions` and the exact-enumeration helpers,
  `level_stats`, `diff_stats`, `_draw_matrix`, `decompose`, `sentence_word`, `propensity`, `_base_row`,
  `_occ_cols`, `build_tables`, `finish_tables`, `nan_reason`; the dataclasses; `XP`'s `trailing_counts` and its
  helpers. The block table, the table-statistics table and the column tuples are VERBATIM assignments. X's
  module-level numeric literals are read from the X text by AST.
- CHANGED, each named:
  - `corridor()` → `E.TP.corridor_n(CLASSIC5, pin_close_iso=E.TC11_PIN_ISO)`, HALT unless `hi + 1 ==
    E.TC11_PIN_MS` (the look-back corridor, L-D.28) and `lo ==` the register's `pool_lo_ms`.
  - `load_inputs(lo)` → the seventeen 4h tapes by `E.load_asof_at(stem, "4h", E.TC11_PIN_MS)` and the five funding
    tapes by `E.load_funding_asof_at(stem, E.TC11_PIN_MS)`, as fresh explicit arrays, X's two grid HALTs kept.
    Declared snapshot read set: exactly those files (the `E.PANEL17` 4h klines and the CLASSIC5 funding tapes);
    `era/READ_SET.json` must hold no other snapshot path.
  - `load_book()` → the v6 scored-window campaign table `T12/books/v6_campaigns.parquet` (L-C.4), its file sha
    asserted through `certified` and its content sha against `books/build_manifest.json`; X's row law kept with the
    count read from TC11's filed book; `join_tc11` kept, reading TC11's certified `books/v6_campaigns.parquet`
    through `E.tc11_record`; and a NEW assertion that the frame equals the `x_rec` copy of X's
    `books/v6_x_campaigns.parquet` on X's fifteen `BOOK_COLS` (the mirror's input anchor; L-C.4's
    `CAMPAIGN_COLUMNS` hold all fifteen names).
  - the gated books' keys → L-L.2's predicates, imported from `tierc12_forward_spec` (never from the ledger
    module); `OLD` and the pin `adm.lag_cut` are read as that module reads them.
  - `stage_a` is split, nothing else: `stage_a_shared(inp, v6_ids)` does X's lines for the stamps, the bars, the
    two replay HALTs and the occupancy (all book-independent); `stage_a_book(sf_v6, occ, keys)` filters the
    campaign frame to a book's keys and calls `support_of` and `late_like_of` on it. For `v6` the two together are
    X's `stage_a`.
  - `compute(book, seed_source)` replaces X's `compute()`: stage A holds no outcome column; stage B joins `net_r`
    from the FILED campaign table (the table law's rounding, as X did — `XE`:2070-2072), never from Trade objects.
  - The module's `SEED` is bound once per process from `seed_source` ∈ {`tier` → `E.SEED`; `x` → the X era
    manifest's `seed`}. The statistics memos are per process: one process per seed. `compute` with `seed_source =
    "x"` is one of the two functions L-0.2 types in `X_SEED_MIRROR_T` — the only place in this section where a
    seed is read by key from a sha-pinned X record; every other seed expression resolves to the pin-door seed.
- NEW: the `book` axis, `era_cell`, the empty-by-construction wording, the cross-book assertions (L-L.22).
- X's builder resolutions ruled in by AM-X23 (the lineage cluster floor; warm-up bars in the occupancy
  denominator) arrive inside the VERBATIM functions and are printed on `ERA.md` as X printed them.
SOURCE: `XE` function list and lines (:399-2077) [read here]; `XE`:227 (`BOOK_COLS`), :1034-1084, :1327-1353,
:2056-2077 [read here]; `scripts/tierc11_books.py`:192-209 [checked here, by `ast`: X's fifteen `BOOK_COLS` are a
subset]; `AMX`:518-529 (AM-X23); L-D.11 (the port law), L-D.27, L-D.28; L-0.2 (F-SEED), L-0.22; O-4; scout U8 §1.11,
§5.
RIVALS: import `tc11x_era` — it arms X's shim and guards TC11's snapshot (O-4). Re-write the tables from the
readings — a second implementation with no referee; the port has X's text as its referee function by function.
FAILS-IF: F-PORT and F-ERA-MIRROR (L-L.23).

**L-L.21 THE v6 MIRROR AGAINST X4's FILED CONTENT SHA; THE SEEDS** — "X4's era tables refreshed" (contract :110)
READING:
- **The mirror leg** — the fixture suite (never the era module, which holds no subprocess site) spawns one process
  that runs the production `compute("v6", seed_source="x")` (X's seed) — requires:
  (a) the v6 table, with the column `as_of_substrate` REPLACED by the value X's table carries and the TC12-only
  columns (`book`, `era_cell`) dropped, hashes under `E.TB._content_sha` to
  `XR/tierc11x/era/build_manifest.json` → `sha.X4_tables`; (b) the stamps table, the same substitution made and
  the two membership booleans dropped, hashes to `sha.X4_stamps`; (c) before the substitution, `as_of_substrate`
  is the Stage D manifest's snapshot name on TC12's side and one constant value on X's side, and every other as-of
  column is equal cell for cell. The one substituted column is typed in the fixture as `MIRROR_SUBST_T`; nothing
  else may differ. [measured here: both filed content shas recompute from the `x_rec` parquet as
  `sha256(df.to_csv(index=False))`; the only as-of column that names the snapshot is `as_of_substrate`.]
- **The tables of record are at the TIER seed** (contract :4; L-0.2), for all three books, with `seed` and
  `n_boot` on every row as X wrote them. A second leg holds the tier-seed v6 rows equal to X4's on every column
  the seed cannot move; the seed-dependent columns are the fixture-typed set `SEED_DEPENDENT_T` (the Monte Carlo
  interval and p columns, the three LOAO columns, `would_read_ci_only`, the sentence columns, `seed`).
- Both seeds are printed in the header of `ERA.md`. No sensitivity seed is added: X4's tables carry one, and a
  second would double `m`.
SOURCE: `XR/tierc11x/era/build_manifest.json` (`seed`, `n_boot`, `sha`, `keys`, `substrate`) [read here];
`scripts/tierc2_baseline.py`:155-188 (`_content_sha`, `write_table`) [read here]; `scripts/tierc10_panel.py`:2528-2555
(`stamp_n`: `as_of_substrate`) [read here]; L-0.21 (stamp truth); L-D.12 (prefix identity); scout U8 R-10, R-11.
RIVALS: everything at X's seed — the tier's seed is the contract's. A mirror that compares statistics columns only
— it would not see a moved key, cell label or collar string. Literal content-sha equality with no substitution —
impossible: the snapshot's name is a column, and L-0.21 requires it to be true of TC12's substrate.
FAILS-IF: F-ERA-MIRROR (L-L.23).

**L-L.22 BOOK AS AN AXIS; EMPTY CELLS; WHAT MOVES WITH THE BOOK AND WHAT MAY NOT** — "refreshed with the gated
books (Tier-E)" (contract :110-111); "every grid printed WHOLE" (:7)
READING:
- **The grid** is the product of two declared axes: `book` (three levels) × `x4_key` (the key tuples of X's filed
  table, read by object). `era_cell` = `book:<b>¦table:<t>¦block:<blk>¦reading:<rd>¦cell:<c>¦side:<sd>`. Every cell
  is a row for every book.
- **Empty by construction.** In both gated books every own-age OLD cell of the three cross blocks (the cells
  ending `/OLD`, and `/B4` in the four-band twin) holds no campaign on any side. Those rows are printed with
  `n = 0`, statistics null, and `nan_reason` prefixed "absent by construction: the book refuses B4 OLD at entry —
  " before X's own reason. They are never dropped.
- **Recomputed per book, from counts only, before any outcome is joined:** E-2's SUPPORT (`support_of` on the
  book's campaigns) and the campaign-count columns of E-3. Printed per book with `n_support_cells` and the list.
- **Must NOT move with the book** (asserted row by row against the v6 row of the same key): the all-bar occupancy
  columns (`occ_bars`, `occ_total`, `occ_share`, `pre2024_months`, `occ_share_b`, `occ_share_h`, `occ_ratio`) and
  E-3's selection flags `late_like` and `no_pre2024` — selected from bar counts before any E[R], on tapes no book
  touches.
- **The outcome rows of a gated book are v6's rows:** every campaign of a gated book carries v6's `net_r` for its
  key (asserted before stage B), so the per-process statistics memo, keyed on a campaign key set, is sound.
- **`m`.** `m_looks_this_table` is counted per book and table family as X counts it; `ERA.md` prints the total
  number of interval-bearing rows across the three books beside it.
- `ERA.md`, the stage document of record (L-L.19), prints every table whole for every book (L-0.15) — this is
  where the contract's "every grid printed WHOLE" is met for the era grid; the report points to it — and X's
  pitfall list verbatim with one line added: "the gated books are subsets of v6 chosen by gates that were scored
  in-sample on these same campaigns (P-AGE-1; P-ADM-1, `pre_seen`)".
SOURCE: `XE`:241-293 (the cross cells), :1270-1324 (`support_of`, `late_like_of`: which columns read counts of
campaigns and which read bars), :1453-1516 (the memo), :1838-1851 (X's null reasons) [read here]; L-0.15, L-0.16;
L-X.28; scout U8 §1.11 (book-dependence per table), R-12.
RIVALS: drop the empty OLD cells — a missing cell and an empty cell would look alike (L-0.15). Carry v6's SUPPORT
into the gated books — a cell with no gated campaign has no within-cell term.
FAILS-IF: F-ERA-BOOKS and `F-GRID [ERA_tables]` (L-L.23).

**L-L.23 THE ERA'S FIXTURES** — "FIXTURES (each states its failure condition)" (contract :114)
READING: `scripts/tierc12_era_fixtures.py`, run at the record `TC12-L`, transcript `T12/era/FIXTURES_ERA.txt`. The
suite imports no door, not `analytics.value_area` and not the reader.

| block | FAILS IF | planted mutations |
|---|---|---|
| **F-ERA-MIRROR** | (a), (b) or (c) of L-L.21 fails; a seed-free column of the tier-seed v6 rows differs from X4's; the input frame differs from X's on a `BOOK_COL` | a one-ulp nudge of a third's boundary inside the port → RED; `load_inputs` reading whole-file tapes (to TC12's pin) → RED (the holdout occupancy totals move — the unbounded read of L-D.28); `net_r` joined from Trade objects at full float → RED; a second column added to a copy of `MIRROR_SUBST_T` → the fixture's own typed-set check |
| **F-ERA** | on the PORT ITSELF, for every v6 campaign: a stamp value differs between production on the look-back tapes and production on tapes cut at the entry close by `E.load_asof_at` (fresh arrays; E1) or spiked after it (E2); a window ends after the entry close (E3); a member bar read does not open at the entry open (E7); the per-bar law differs from the entry law at an entry or at a seeded pseudo-entry (E8) — 40 warm bars per CLASSIC5 asset, direction +1 (the count X filed for this leg, `XR/scripts/tc11x_era_fixtures.py`:615-623), drawn from the block's own stream under the dialect's RNG law (suite tag `era`, block id `F-ERA`) and printed in the block header | X's sabotages planted INSIDE the ported functions (a vol window ending after the bar; the percentile over the full history; funding admitting the first print after the close; the BTC clock read one bar late; whole-pool edges; a member read at the bar opening at the entry close) — each must turn E1 or E2 RED on the plant sample, which is fixed by X's rule (`…era_fixtures.py`:430-446): in `(symbol, entry_ms)` order, the first two campaigns of each asset in each era, plus each asset's first settlement-coincident entry (22 campaigns on X's transcript, `XR/tierc11x/era/FIXTURES_X4.txt`:24) |
| **F-ERA-BOOKS** | a gated book's key set is not v6's minus the keys L-L.2's predicates refuse, or differs from its regbook referee; a gated row's `net_r` is not v6's; an occupancy column or a selection flag differs across books; an own-age OLD cell of a gated book holds a campaign or lacks the "absent by construction" reason; SUPPORT was computed with an outcome column in scope; (AST) the era module defines a refusal predicate of its own or imports the ledger module; `era/READ_SET.json` holds a snapshot path outside the declared set or any path under `T12/va/` | an un-gated book passed as `gated-v6-combined` → `ERA-BOOK-KEYS`; one OLD campaign left in a gated book → `ERA-OLD-CELL`; `late_like` recomputed from campaign shares → `ERA-SELECTION`; `net_r` attached before `stage_a_book` → `ERA-STAGE-A`; `import tierc12_forward` planted in a copy of the era module → `ERA-IMPORT`; a `va/` path planted in a copy of `READ_SET.json` → `ERA-READ-SET` |
| **F-INT-THIRDS** | a third is decided by a float comparison (X's law and AST leg, on the port) | the float comparison planted in a copy of `third_share` |
| **`F-GRID [ERA_tables]`** | L-0.15 on `ERA_tables`: a missing, undeclared or duplicate `era_cell` against {three books} × {X's filed keys}; the per-book row count is not X's table's; a null statistic without `nan_reason`; `promotable` true; a verdict-like column; `ERA.md` does not print every cell | a dropped empty OLD row; a fourth book level; a row with its `nan_reason` nulled |
| `F-TYPED-FLOW [seed]` | in a fresh process the tier seed is bent by one at its door (`E.SEED`, monkeypatched before the module binds `SEED` under `seed_source = "tier"`) and `level_stats` is re-run on the v6 E-1 rows of the first block of X's block table: no `SEED_DEPENDENT_T` column moves, or a seed-free column moves | `seed_source = "tier"` resolved to a typed copy of the seed in a copy of `compute` → `PIN-NOT-READ` |
| `F-DET [era]` · `F-KEY [era]` · `F-COLLAR [era]` · `F-PORT` | L-0's laws on `era/` (`READ_SET.json` is in the determinism set); the port law | L-0's plants; the three port plants |

SOURCE: `XR/tierc11x/era/FIXTURES_X4.txt`:22-58 (F-ERA's legs and sabotages; F-INT-THIRDS; F-GRID) [read here];
`XR/scripts/tc11x_era_fixtures.py`:430-446 (`sab_sample`), :615-623 (`pseudo_entries`) [checked here]; L-0.14 (the
fixture RNG and the stated count), L-0.17 (the flow leg), L-0.19 (the hosting row); scout U8 H-17 (a mirror that
only compares outputs cannot see a future-inclusive window — hence F-ERA on the port).
RIVALS: none.
FAILS-IF: n/a (this reading is the roll).

---------------------------------------------------------------------------------------------------------------
### E · The ferry

**L-L.24 SCOPE — WHICH FILES ARE ROW FILES** — "FERRY: every per-trade and per-asset row file → exchange/rows/tierc12/"
(contract :111)
READING: X's standing ferry law, STRICT scope, decided by ROWS and never by name. Only files under `T12/` are
candidates: the contract names one bus directory, and TC11's and X's rows are X's ferry's business.
- **Triage** (`triage`, ported from `XY`:516-531, CHANGED by its first clause and by the by-type list): a path
  under `x_rec/` → EXCLUDED; any path segment starting `_det_` → EXCLUDED — that covers every twin, the staging
  directory of L-L.32 and the quarantine directories `_det_partial_<…>/` of L-0.4; an extension outside
  `.parquet`, `.csv`, `.jsonl` → EXCLUDED (document or manifest), or POINTED by path and sha if it is one of the
  typed JSON documents with per-asset arrays (`data/fee_schedule.json`, `data/CONTRACT_SPECS.json`,
  `va/TRAVERSE.json` — X's class for the like documents, `XY`:223-225); a name starting `FETCH_LOG` → EXCLUDED (a
  per-request log).
- **POINTED BY TYPE — never passed to the rule** (the typed tuple `BY_TYPE_T`, four paths):
  `forward/FORWARD_LEDGER.jsonl`, "a hash chain of mixed line kinds, committed in git" (X's typed row, `XY`:295; its
  rows are ferried as `forward/ledger_rows`); and the three event listings `stage_g/g_arbitration.parquet`,
  `stage_g/g_reride_diff.parquet` and `stage_r/dir/dir_reride_diff.parquet`, "an event listing with a placeholder
  row; class not row-stable" — each is a single placeholder row when no event happened, so the class the rule
  would return depends on whether any event exists (and, for the arbitration listing, which has no identity
  instant, on whether an asset has two); a class that moves with the outcome of the build is typed, not derived.
- **The identity rule** (`identity_class`, VERBATIM, `XY`:495-513), on a table's columns and rows: the ASSET
  column is the first present of `asset`, `symbol`; the identity INSTANT is the first present of `entry_ms`,
  `entry_open_ms`, `entry_close_ms`, `harden_ms`, `event_ms`, `known_at_ms`; bar instants (`t0`, `t0_ms`,
  `open_time`, `open_ms`, `bar_ms`) are never identities; the BOOK AXES are whichever of the frozen 26 words are
  columns of the file. In order: a column named `draw` → POINTED ("a draw table"); no ASSET column → POINTED ("no
  ASSET column"); rows unique on (axes, ASSET, INSTANT) → **PER-TRADE**; else rows unique on (axes, ASSET) →
  **PER-ASSET**; else POINTED ("rows per identity > 1"). PER-TRADE and PER-ASSET are FERRIED.
- The vocabulary is read by AST from `XY`:194-200 and is FROZEN: X's two scoped extensions (AM-X22, AM-X27) were
  for X's own tables and are not carried. A TC12 table that wants to be ferried is built to the vocabulary, and
  the other sections' tables are: an order table is keyed on `known_at_ms` (the trigger close; no column named
  `trigger_close_ms`, `entry_ms`, `entry_open_ms`, `entry_close_ms`, `harden_ms` or `event_ms` stands in
  `S_orders_*`, `S_refusals_*` or `S_miss`); a MISS row's target is the axis `variant`; a grid whose axes include
  the assets names that column `panel` — an axis word here, never an ASSET column — so it classes POINTED "no
  ASSET column". `va/va_stack` is the declared exception (key `[asset, lens, era]`, FERRIED per-asset).
SOURCE: contract :111; `XY`:193-225, :495-531 [read here; the six instant names and the 26 axis words checked
here]; `LX`:2099-2182 (LX-X6.1); `AMX`:291-314, :507-514, :575-589; L-S.30 (the order-table keys); scout U8 §1.12,
R-15.
RIVALS: the broad reading (every file whose key holds a trade or asset identity, timelines included) — X's
rejected rival; printed as one byte count beside the forecast, deciding nothing. Class by file name — refused by
LX-X6.1's first sentence.
FAILS-IF: `F-ROWS [SCOPE]` (L-L.33).

**L-L.25 THE TYPED LIST, FROZEN BEFORE ANY FILE EXISTS** — "every per-trade and per-asset row file" (contract :111)
READING: every tabular TC12 file has a TYPED class, fixed in this text before the file exists. The list below is
COMPLETE: it was derived by L-L.24's rule from the key and columns every section declares for every tabular file
it writes, and nothing is left to assembly. At build the rule is re-derived on each file's rows; a disagreement,
or a tabular file not on the list, is a HALTED ELEMENT — never ferried, listed, and the ferry exits non-zero —
until a dated amendment.
- **What is held is the CLASS** — FERRIED, POINTED or EXCLUDED (X's comparison, `XY`:1422: the typed class
  against the class of the rule's word, PER-TRADE and PER-ASSET both being FERRIED). The words after the dot are
  the typed kind, carried as orientation; the manifest records the word and the reason the rule itself returns
  (`scores/DRAWS.parquet` keys its draws on `draw_idx`: if it carries no column named `draw` the rule returns "no
  ASSET column", and the class is POINTED either way). The four `BY_TYPE_T` paths are not passed to the rule
  (L-L.24).
- **A parameterised row is expanded over a closed set read by object, never by a glob of the disk:** `<ID>` over
  the registry's ids; `<arm>` over the `arms` of that registration's `regbooks/<ID>/STATUS.json` (L-X.24's arms
  of record — an arm with no row is a zero-row parquet and is FERRIED as a header-only CSV; a registration CLOSED
  BY PRECONDITION lists no arm and expands to nothing); `<lens>` over the lens keys of `va/VA_PINS.json`;
  `<book>` in `S_orders_<book>`, `S_refusals_<book>` and `VA_STAMPS_<book>` over the table names the directory's
  `build_manifest.json` declares; the braces as written.
- **A typed file that does not exist at a run** — not yet filed at that stage (`scores/`, `review/` at TC12-L),
  listed under its directory's `skipped_empty`, or of a closed registration — is printed `ABSENT (<reason>)` and
  is no finding; the run at TC12-CLOSE re-enumerates (L-L.32).

| file (relative to `T12/`) | declared key | typed class · reason |
|---|---|---|
| `books/{v6,trg912}{,_ext}_journal.parquet` | `[asset, entry_ms]` | FERRIED · per-trade |
| `books/{v6,trg912}{,_ext}_campaigns.parquet` | `[symbol, entry_ms]` | FERRIED · per-trade |
| `books/strip.parquet`, `books/ctrl_prefix.parquet` | `[book, symbol, entry_ms]` | FERRIED · per-trade × book |
| `books/arming_log.parquet`, `books/arming_counts.parquet` | `[book, window, symbol, arm_ms, direction]`, `[book, window, symbol, reject]` | POINTED · rows per identity > 1 |
| `tide/tide_bars_4h.parquet` | `[asset, open_ms]` | POINTED · rows per identity > 1 |
| `tide/breadth_4h.parquet` | `[open_ms]` | POINTED · no ASSET column |
| `stage_g/g_campaign_gates.parquet`, `stage_g/g_strip_gates.parquet` | `[symbol, entry_ms]` | FERRIED · per-trade |
| `stage_g/g_book_keys.parquet` | `[book, symbol, entry_ms]` | FERRIED · per-trade × book |
| `stage_g/{g_gate_rows, g_brd_grid, g_brd17, g_grid_partition, g_grid_books}.parquet` | `[gate]` / `[cell]` | POINTED · no ASSET column |
| `stage_g/g_arbitration.parquet`, `stage_g/g_reride_diff.parquet`, `stage_r/dir/dir_reride_diff.parquet` | `[window, symbol, trigger_ms, arm_ms]`; `[gate, window, symbol, entry_ms]` | POINTED · by type ("an event listing with a placeholder row; class not row-stable") |
| `stage_r/dir/VA_CHOP_ROWS.parquet` | `[symbol, entry_ms]` | FERRIED · per-trade |
| `stage_r/dir/dir_book_keys.parquet` | `[book, symbol, entry_ms]` | FERRIED · per-trade × book |
| `stage_r/dir/{VA_CHOP, VA_CHOP_ALIGNMENT, VA_CHOP_MARGINS}.parquet` | `[cell]` | POINTED · no ASSET column |
| `stage_r/sfp/SFP_EVENTS.parquet` | `[lens, book, asset, entry_ms]` | FERRIED · per-trade × axes |
| `stage_r/tables/TP1D_CAMPAIGNS.parquet` | `[symbol, entry_ms]` | FERRIED · per-trade |
| `stage_r/tables/TP1D_SUMMARY.parquet` | `[era, asset]` | FERRIED · per-asset × era |
| `stage_r/tables/TP1D_BARS.parquet` | `[symbol, entry_ms, bar_open_ms]` | POINTED · rows per identity > 1 |
| `stage_s/S_orders_<book>.parquet`, `stage_s/S_refusals_<book>.parquet` | `[book, symbol, known_at_ms]` | FERRIED · per-trade × book |
| `stage_s/S_miss.parquet` | `[book, symbol, known_at_ms, variant]` | FERRIED · per-trade × axes |
| `stage_s/open_at_w_continued.parquet` | `[symbol, entry_close_ms]` | FERRIED · per-trade |
| `stage_s/{S_FUNNEL, S_FILL_SENSITIVITY, S_REGIME, S_SLICES, S_MISS_GRID}.parquet` | `[cell]` | POINTED · no ASSET column |
| `va/va_bars_<lens>`, `va/va_events`, `va/va_regimes`, `va/traverse_legs` | as L-V.24 declares them | POINTED · rows per identity > 1 |
| `va/va_stack.parquet` | `[asset, lens, era]` | FERRIED · per-asset × axes |
| `va/trades/{va_null_events, va_null_go_events, NULL_BOXES_VA, TWO_TRADES_NULL_DRAWS}.parquet` | … + `draw` | POINTED · a draw table |
| `va/trades/TWO_TRADES_EVENTS.parquet` | `[lens, asset, trade, side, anchor_i, i]` | POINTED · rows per identity > 1 |
| `va/trades/{TWO_TRADES_VA, TWO_TRADES_VA_UNCOND, TWO_TRADES_BASE, TWO_TRADES_NULL}.parquet` | `[cell]` | POINTED · no ASSET column |
| `va/stamps/VA_STAMPS_<book>.parquet` | `[book, symbol] + kind.key + [instant_kind, instant_ms]` | POINTED · rows per identity > 1 |
| `regbooks/<ID>/<arm>.parquet` (L-X.24's arms of record, by object) | `(symbol, entry_close_ms)`; `strip`: `(arm, symbol, entry_close_ms)` | FERRIED · per-trade (× `arm` on `strip`) |
| `forward/ledger_rows`, `forward/ledger_side`, `forward/ledger_listed` | `[book, symbol, entry_ms]` | FERRIED · per-trade × book |
| `forward/FORWARD_LEDGER.jsonl` | a hash chain | POINTED · by type |
| `era/ERA_stamps.parquet` | `[symbol, entry_ms]` | FERRIED · per-campaign |
| `era/ERA_tables.parquet` | `[book, table, block, reading, cell, side]` | POINTED · no ASSET column |
| `scores/DRAWS.parquet` | `(registration, draw_set, draw_idx)` | POINTED · a draw table |
| `scores/REFILE_LOG.jsonl`, `scores/SUPERSEDED.jsonl`, `review/*.jsonl` | — | POINTED · no ASSET column |
| `data/FETCH_LOG.jsonl` | — | EXCLUDED · per-request log |

Notes on single rows, each a consequence of the rule and stated so that the build's re-derivation is not a
surprise: a regbook arm is keyed by the rule on `symbol`, its first identity instant `entry_ms`, and the axis
columns it carries (`lane`, `direction`, `era`; `arm` on `strip`) — unique wherever `(symbol, entry_close_ms)` is;
a stamp table holds `entry_ms` or `known_at_ms` and many instants per identity, hence "rows per identity > 1";
`va_bars` and `va_events` carry bar instants and close columns outside the frozen six; `ERA_tables` is X's AM-X13
class for `era/X4_tables`.
SOURCE: `XY`:227-299 (`X_TYPED`, with its `amended_by` / `was` fields), :1392-1440 (typed class against the rule's
class) [read here; :1422 checked here]; `LX`:2119-2150; the declaring readings — L-C.4 (`books/`), L-G.10, L-G.19
(`tide/`, `stage_g/`), L-R.31 (`stage_r/dir|sfp|tables/`), L-S.30 (`stage_s/`), L-V.19, L-V.23, L-V.24 (`va/`,
`va/trades/`, `va/stamps/`), L-X.24, L-X.26, L-X.27 (`regbooks/`, `scores/`); `AMX`:561-571 (AM-X26, a new file
turned the SCOPE leg RED by design).
RIVALS: class at build from the rows alone — a class chosen after the contents exist. Leave the other sections'
rows to assembly — not taken: the list is frozen text (L-0.10 T4) and an untyped table would HALT the ferry at
TC12-L.
FAILS-IF: `F-ROWS [SCOPE]` (L-L.33).

**L-L.26 NAMES, THE CSV DIALECT, THE READER LAW** — "→ exchange/rows/tierc12/ as CSV" (contract :111-112)
READING:
- **Bus path** `exchange/rows/tierc12/<name>.csv`; `<name>` = `flat_name(rel)` (VERBATIM, `XY`:481-485): the source
  path relative to `T12/`, extension dropped, each `/` written `__` (e.g. `forward__ledger_rows.csv`,
  `regbooks__P-ADM-1__scored.csv`). HALT `FERRY-NAME-COLLISION` on an exact or case-folded collision (`XY`:610-622).
  One `ROWS_MANIFEST.md` in the directory. The directory string is the contract pin `ferry.bus_dir` (:111, the
  one capture of `row file → (\S+)`, type str), read through the pin door and never typed.
- **Serializer** (`to_csv_bytes`, VERBATIM, `XY`:543-547): `df.to_csv(buf, index=False, lineterminator="\n",
  encoding="utf-8")`, the default float repr, the source's own row order, the source's own columns. The pandas
  version is recorded in the manifest.
- **Reader law** (X's AM-X15 (C), carried as text into the manifest and `ROWS_MANIFEST.md`): an untruncated CSV
  reads back equal to its parquet under `pandas.read_csv(<csv>, float_precision="round_trip",
  keep_default_na=False, na_values=[""], dtype=<the parquet schema's>)` — cell for cell, a null equal to a null,
  floats bit-equal; a string column's empty string reads back as a null. The default float parser is not lossless.
SOURCE: `XY`:181-191, :481-485, :543-547, :610-622 [read here]; `LX`:2184-2202; `AMX`:357-360;
`XR/tierc11x/ferry/FERRY_MANIFEST.json` → `serializer` [read here].
RIVALS: the bare stem as the name — collides (five registrations each hold a `scored.parquet`).
FAILS-IF: `F-ROWS [RT]`, `F-ROWS [SCOPE]` and `F-TYPED-FLOW [ferry.bus_dir]` (L-L.33).

**L-L.27 THE CAP** — "as CSV, 2 MB cap" (contract :112)
READING: `CAP_BYTES` = the contract pin `ferry.cap_mb` (:112, `(\d+) MB cap`) × `BYTES_PER_MB`
(`scripts/tierc12_units.py`: decimal megabytes, X's filed reading), asserted equal to `CAP_BYTES` read by AST from
`XY`:177. The cap is on the CSV alone. **Whole rows only** (`record_ends`, `cut`, `csv_facts`, VERBATIM,
`XY`:550-583): the carried file is the full serialisation's prefix through the largest `k` records with
`len(header) + Σ_{i<k} len(row_i) ≤ CAP_BYTES`, record ends found quote-aware; HALT if the header alone exceeds
the cap. The carried file is a pure CSV. Its pointer lives in the manifest and is rendered in `ROWS_MANIFEST.md`:
source path and sha, bytes, rows carried and total, the last carried key, the full-CSV sha and the carried sha,
and `protected_by`. No file carries its own sha. No source mtime is recorded (a clock under L-0.20; X recorded
one). The binary megabyte (`CAP_RIVAL`, `XY`:178, by AST) is printed as the rival and decides nothing.
SOURCE: contract :112; `XY`:176-179, :550-583 [read here]; `LX`:2204-2216; L-0.17 (`UNITS_T`, and the note that the
cap's digit collides with the structural set and is held by the flow leg).
RIVALS: a trailing comment block in the CSV — breaks strict readers. The bus's own 1,048,576 B per-file rule
(`exchange/README.md`:21) — the ratified contract names 2 MB; the conflict is ATHENA's (Q-A1), named and not
decided here.
FAILS-IF: `F-ROWS [CUT]` and `F-TYPED-FLOW [ferry.cap_mb]`: bent at its door, the rows carried of a synthetic frame
larger than the cap must change (L-L.33).

**L-L.28 THE BOX MEASURE AND THE THRESHOLDS** — "files that would push the box past WARN" (contract :112)
READING:
- **What is measured is the TICK SET, not `du`:** the tracked blobs under `SCOPE` (`exchange/`) plus `TICK_EXTRA`
  (`LEDGER.md`), at a PINNED commit of the main branch. Untracked files and the working copy of a modified file are
  not in it. The blobs are read in process from the git object store by ports of X's readers (`git_dir`,
  `read_ref`, `head_of`, the object reader and `tree_files`, VERBATIM, `XY`:764-1160); no TC12 module runs git.
  CHANGED: `box_at(head_sha)` sums the pinned commit's tree — TC12 builds in the target tree, so there is no merge
  target to compute. X's index cross-check is NOT carried: it HALTs whenever a tracked `exchange/` file is dirty,
  and the daily routine leaves one dirty every day.
- **The constants** — `SCOPE`, `BOX_BYTES`, `WARN_FRACTION`, `REFUSE_FRACTION`, `OVERRIDE_ENV`, `TICK_EXTRA`,
  `FLAG_BYTES` — are read by `ast.literal_eval` of their module-level assignments in `scripts/publish_exchange.py`
  (`publish_constants`, VERBATIM, `XY`:626-641); the module is never imported; its sha must be the census value
  (L-0.6).
- **The comparators** are `publish_exchange.budget`'s own (`level`, VERBATIM, `XY`:644-652): REFUSE iff the
  fraction is strictly above `REFUSE_FRACTION`; WARN iff it is at or above `WARN_FRACTION`; else OK. The WARN line
  in bytes is found on `level()` itself (`warn_line`, VERBATIM) and never typed.
- **"Past WARN"** is read as: the projection would leave OK — i.e. `publish()` would print its warning. A file is
  written iff `level(projection + its bytes) == "OK"`.
- `OVERRIDE_ENV` is never set; REFUSE is never overridden.
SOURCE: `scripts/publish_exchange.py`:48, :95, :109-111, :128, :160, :201-222 [read here]; `XY`:352, :626-663, :764
ff. [read here]; `LX`:2233-2260 (LX-X6.7); `AMX`:410-425 (AM-X17); scout U8 §1.12, §1.13, H-15; scout U1 §1.9.
RIVALS: `du` on `exchange/` — counts untracked files and filesystem blocks; not what `publish()` budgets. "Past
WARN" as strictly above the WARN line — differs at one byte and would let a write produce a WARN publish; the
stricter reading is taken.
FAILS-IF: `F-ROWS [BOX]` (L-L.33).

**L-L.29 THE FORECAST BASIS** — "files that would push the box past WARN are held" (contract :112); O-24 "staged
off-bus under `research_outputs/tierc12/ferry/` with a forecast"
READING: during the build the ferry writes nothing on the bus; it files a FORECAST. Two are filed: F1 at TC12-L and
F2 at TC12-CLOSE (when the draft and the staged append exist). Both use one law.
- **The pin.** `--pin` reads the main branch's HEAD sha from the ref files in process and writes it ONCE per stage
  to `T12/ferry/BOX_PIN_<STAGE>.json` — a provenance record — with the tick bytes at that commit and the measured
  parts below. Every forecast run and every fixture re-derives against the RECORDED sha, never the live HEAD; a
  moved HEAD is one printed line with no pass condition (AM-X17's law).
- **The projection base** = tick bytes at the pinned HEAD + the NAMED RESERVATIONS + the bytes of
  `ROWS_MANIFEST.md` (rendered in memory and reserved by X's monotone fixed point, `XY`:2233-2247). HALT if any
  `exchange/rows/tierc12/` path is in the pinned tree.
- **The named reservations for the three pending closes**, each read by key from X's filed record
  `XR/tierc11x/ferry/FERRY_MANIFEST.json` (sha asserted through `E.x_rec`) and DROPPED once that predecessor's
  report path (the three paths of L-X.33 step 0) is in the pinned tree:
  - `tc10` = `forecast_close.box_reservation.parts[id == "tc10"].reserved_bytes`;
  - `tc11` = `…parts[id == "tc11"].reserved_bytes`;
  - `x` = `…parts[id == "report"].reserved_bytes` + `…parts[id == "append"].reserved_bytes` +
    `forecast_close.worksheet.merge_target.x_delta_bytes` (X's contract arriving with the merge) +
    `forecast_close.box_after.written_csv_bytes` + `forecast_close.box_after.rows_manifest_bytes` (X's bus rows as
    X's own forecast wrote them).
- **`swept`** — what the next `publish()` will sweep in besides: measured at the pinning run, the sum over the
  pinned tree's `exchange/` paths whose working copy differs from its blob of (working bytes − blob bytes) when
  positive, plus the bytes of every working file under `exchange/` that is not in the pinned tree (counted whether
  or not git ignores it — an over-reservation, each file listed).
- **`own`** — TC12's own close adds:
  - at F1: the report at the per-file cap the close generator HALTs above (the `(\d+) MB per file` capture of
    `POINTER_RULE` × `BYTES_PER_MB`, L-X.28) — an upper bound; the append at X's filed allowance `APPEND_UNSTAGED`
    (`XY`:2140, by AST); two `BUILT:` stamp lines, each at the byte length of the longest `BUILT:` line among the
    queue files of the pinned tree;
  - at F2: the report at the measured bytes of `T12/BUILD_DRAFT.md`; the append at the measured bytes of the
    staged `T12/LEDGER_APOLLO_APPEND.md`; the two stamp lines as at F1. Each measure is recorded with its sha. The
    staged bytes ARE the stamped bytes: L-X.32 renders every stamp bracket at a fixed byte width and pads or
    truncates its fill to exactly that width, so the stamped report and append have the staged byte counts.
- **Printed beside, deciding nothing:** the box if X's ferry of record fills to one byte under the WARN line (it
  re-plans on the box it finds; X's forecast is not a promise); the broad-scope byte count; the FLIPPED set between
  F1 and F2.
- The forecast is written into `T12/ferry/FERRY_MANIFEST.json` (`forecast_<stage>`) and rendered as
  `T12/ferry/BOX_FORECAST_<STAGE>.md`. Given the pin record it is byte-deterministic.
- **Stated before any size exists:** on the filed figures the three pending closes alone bring the box to within
  a few kilobytes of the WARN line (scout U8 §1.13; O-24), so the expected forecast is that every TC12 row file is
  HELD. That is the contract's own provision, not a defect of the ferry.
UNVERIFIED: that X's filed figures equal what the three closes will add. They need not; the ferry of record
measures the landed box (L-L.32).
SOURCE: `XR/tierc11x/ferry/FERRY_MANIFEST.json` (keys `forecast_close.box_reservation.parts` — five parts with ids
`report`, `append`, `tc10`, `tc11`, `swept` — `forecast_close.box_after`, `forecast_close.worksheet.merge_target`)
[read here, keys and structure]; `XY`:2132-2247 [read here]; `AMX`:318-342, :346-355, :410-425, :478-503 (AM-X14,
AM-X15, AM-X17, AM-X21); L-X.28 (the cap), L-X.31; scout U8 §1.13, R-14; scout U1 §1.9, H-9.
RIVALS: the tick set plus TC12's own adds only — ignores three closes ordered to land first. Typed reservation
figures (X's constants) — contract :8; they are read from X's filed record instead. One forecast, at close only —
L-0.10 asks TC12-L for a forecast; the upper-bound reservation makes F1 the conservative one.
FAILS-IF: `F-ROWS [FORECAST]` (L-L.33).

**L-L.30 THE HOLD LAW AND THE FROZEN ORDER** — "files that would push the box past WARN are held" (contract :112)
READING:
- **First-fit in a fixed order** (`project`, VERBATIM, `XY`:666-685): starting from the base, each FERRIED file in
  order is WRITTEN iff `level(cumulative + its carried bytes) == "OK"`, else it is **HELD FOR ATHENA** — not
  written, not counted — and the loop CONTINUES (a later, smaller file may still be written). If the base alone
  reads WARN, every file is held. HALT `FERRY-REFUSE`, writing nothing, only if the base alone is past REFUSE.
- **The order, frozen here before any size exists** (file sizes are structural, but an order chosen after they
  are known is a selection):
  1. `forward/ledger_rows.parquet` — the ledger's appended rows (the contract's §0 item, :127);
  2. the `scored` arm of each registration, in the registry's `seq` order (read from the registry, not typed);
  3. every `base` arm that a `STATUS.json` lists (the two-sample registrations), in `seq` order, then
     P-SCALP-3's `ladder__touch` and `ladder__deep` (the fill-sensitivity row is part of that verdict's text);
  4. every other FERRIED file — the `strip` and `tierE__*` arms among them — by source path, ascending bytewise.
  A file of positions 1-3 that does not exist (a row closed by precondition lists no arm; a ledger with no
  appended row writes no `ledger_rows`) is skipped and printed `ABSENT (<reason>)`.
- Every WRITTEN bus file over `FLAG_BYTES` is FLAGGED: named to the operator, with its home, in the forecast, in
  `ROWS_MANIFEST.md` and in the report's file-disposition table.
SOURCE: `XY`:329-336, :666-696 [read here]; `AMX`:318-342 (AM-X14: "The rows that bear on the verdicts come first";
"File sizes are structural, not outcomes"), :377-406 (AM-X16); `LX`:2247-2256; `exchange/status/CONVENTIONS.md`:360
(the naming duty; scout U1 §1.9); scout U8 R-16, H-14.
RIVALS: path order throughout (X's first build) — it held the registered books' rows while ferrying Tier-E tables;
X amended it. Smallest-first — maximises the file count, an order chosen by size. HALT the whole ferry at WARN —
holds files that fit (X's rejected rival).
FAILS-IF: `F-ROWS [ORDER]` (L-L.33).

**L-L.31 THE HELD LIST — "LISTED for ATHENA"** — "are held and LISTED for ATHENA" (contract :112)
READING: a held file is DECLARED, not exported. The status word on every record is X's filed one, `HELD FOR
ATHENA`, so that ATHENA reads one vocabulary across tiers. The LIST exists in four places, all generated from the
manifest:
1. `T12/ferry/FERRY_MANIFEST.json`: `athena.held_for_athena` (the source paths, in hold order); `box.held`,
   `box.k_held`; one `box.projection[]` record per file — `{key, bytes, action, projected_after,
   level_if_written, would_be}` for a held file, `{key, bytes, action, projected_after, level_after}` for a written
   one; `athena.questions` (X's Q-A1 — a named exception for `exchange/rows/` and which cap — and Q-A2 — a folder
   budget and a rotation rule — re-filed, not decided); `athena.conflicts_named_not_fixed` (the four of LX-X6.8).
2. `exchange/rows/tierc12/ROWS_MANIFEST.md` (rendered by a TEXT-ONLY port of `XY`:1940-2020): sections Ferried ·
   the pointer of every cut file · `## HELD FOR ATHENA (k) — LISTED for ATHENA: declared, not exported` with X's
   seven columns (would-be bus file · source · class · key · rows · capped CSV B · source sha256) · HALTED ·
   Pointed to by path and sha · Excluded (counts by reason) · ATHENA.
3. The report: §8's file-disposition table and §7's findings (L-X.30 harvests the list, owner ATHENA).
4. The ledger append: the stamp with the ferry of record's WRITTEN / HELD FOR ATHENA / FLAGGED counts (L-X.32).
`ROWS_MANIFEST.md` is the list itself, not a row file: the hold law does not apply to it. It is written at the
ferry of record even when every CSV is held, and its bytes are part of TC12's own reservation.
SOURCE: contract :112; `XR/tierc11x/ferry/FERRY_MANIFEST.json` → `athena`, `box.projection[0]` (keys) [read here];
`XY`:1940-2020 [read here]; `LX`:2262-2277 (LX-X6.8, LX-X6.9); L-X.30, L-X.32, L-X.36.
RIVALS: a new status word "LISTED" — two vocabularies for one state. Hold `ROWS_MANIFEST.md` too when the box
reads WARN — ATHENA would then have no list on the bus.
FAILS-IF: `F-ROWS [EXIST]` (L-L.33).

**L-L.32 STAGING OFF-BUS, AND THE FERRY OF RECORD AS A CLOSE ACT** — O-24 "the ferry of record into
`exchange/rows/tierc12/` is a close act"; "Q6 the close acts remain the operator's keystrokes" (contract :14-15)
READING: `scripts/tierc12_ferry.py` (shim-armed; a decision module; it holds no subprocess site and runs no git)
has three modes. In none of them does a python source write under `exchange/`: the shim refuses it (L-D.27) and
L-0.8's F-OFFBUS scans for it. The ferry is a carrier: it reads each table whole through pandas, derives a class
from column NAMES of the frozen vocabulary and from row uniqueness, and serialises FERRIED tables as they stand.
It selects no value-area column by name, hands no lens to the reader, and its declared VA read list is empty.
- `--stage=<TC12-L | TC12-CLOSE>`: enumerate `T12/` (never typed), triage, class each tabular file (typed list and
  rule), serialise and cut each FERRIED file, and write the carried CSV to `T12/ferry/_det_staged/<name>.csv` — a
  directory the nested ignore rule already keeps out of git and the triage excludes from enumeration. Each source
  is hashed, read once, hashed again. `FERRY_MANIFEST.json` records per file: tier, rel, source sha and bytes,
  rows, columns, declared key, typed class, the rule's class, kind, reason, and the CSV facts (the carried sha
  among them). The run at TC12-CLOSE re-enumerates (files written after TC12-L exist then) and re-stages any
  source whose sha moved.
- **How the staging is pinned.** `ferry/FERRY_MANIFEST.json` is tracked and is recorded by two records — `TC12-L`,
  then `TC12-CLOSE` (re-filed with `forecast_TC12-CLOSE`) — which L-0.4's last-record law names as lawful: the
  working file verifies under the later entry and the earlier entry is held to the blob at the TC12-L commit. The
  staged CSVs are NOT entries of a record's `artifact_shas`: they are scratch derivations under a `_det_`
  directory, pinned by their carried sha in that tracked manifest and re-derivable byte for byte from their
  sources. (A review worktree stages parquet and never a `_det_*` path, L-0.12; a recorded path it cannot stage
  would read RECORDED NOT STAGED.) `F-ROWS [EXIST]` re-derives each of them and `F-ROWS [FRESH]` re-hashes them
  where they stand.
- `--pin` then `--forecast` (L-L.29, L-L.30): the pin record, the manifest's forecast block, the forecast page.
- `--of-record` — run ONLY by the operator's `close_acts.sh`, at its step 2, after its step 0 has proven the
  TC10, TC11 and X blocks landed by bytes in that order (L-X.33): it pins the HEAD of that instant; measures the
  tick set with the three closes inside it; reserves ONLY TC12's own close adds (the draft, the staged append, the
  two stamp lines, `ROWS_MANIFEST.md`) and that instant's `swept`; re-hashes every source and every staged CSV
  against the tracked manifest (a moved or missing file STOPS the act); runs the first-fit; and writes, under
  `T12/ferry/` only, `OF_RECORD.json` (the pin, the measure, the projection, the WRITTEN / HELD / FLAGGED sets) and
  `of_record/ROWS_MANIFEST.md` and `of_record/COPY_LIST.txt`.
- **The copy is the shell's.** `close_acts.sh` creates `exchange/rows/tierc12/`, copies each listed staged CSV and
  the rendered `ROWS_MANIFEST.md` there, and compares shas; then runs the suite in its act mode,
  `scripts/tierc12_ferry_fixtures.py --of-record` (L-L.33), whose transcript `ferry/of_record/F_ROWS_AT_CLOSE.txt`
  belongs to no progress record. On any failure the files it wrote are moved aside (nothing deleted) and the
  script STOPS. `publish()` at its own step stages the bus files; the script stages no `exchange/` path itself.
- The executor never runs `--of-record` in the main tree and never creates `exchange/rows/` (O-12). Its only
  executions of `--of-record` are inside fixtures, against scratch repositories (`F-ROWS [ACT]`); in the acts'
  sandbox proof the planner call is stubbed (L-X.33) — that proof holds the ORDER and the STOP guards of the
  script, and `F-ROWS [ACT]` holds the planner itself.
- The closing order is TC10 → TC11 → X → TC12. A TC12 ferry that ran before X's would take box room from X's
  certified ferry; the act refuses until X's block has landed.
SOURCE: O-1, O-12, O-24; L-0.4 (the last-record law), L-0.8 (F-OFFBUS), L-0.12 (what a review worktree stages),
L-0.26; L-D.27 (`exchange-write`), L-X.33 (the step list; step 2); `T12/.gitignore` (`**/_det_*/`) [read here];
`XY`:162 (`_det_snap`, X's precedent for a non-twin `_det_` directory), :1308 (hash, read once, hash again);
`XR/tierc11x/close/close_acts.sh`:196-230 (X's ferry step and its fixture call) [checked here]; `AMX`:478-503
(AM-X21); `LX`:2195-2196 ("Never in the main tree's `exchange/`, which the 07:00 routine would sweep"); scout U8
R-13, H-4, H-5; scout U1 H-9.
RIVALS: write the CSVs to `exchange/rows/tierc12/` during the build — the 07:00 routine would publish them the
next morning, before any verdict, and shrink the box X's ferry will measure. A python writer for the bus — would
need an exception to F-OFFBUS for no gain. Track the staged CSVs — tens of megabytes on a branch the routine
pushes. Record each staged CSV in the stage's progress record — not taken: a `_det_` path is never staged into a
review worktree, and the tracked manifest already pins every carried sha.
FAILS-IF: `F-ROWS [EXIST]`, `[FRESH]` and `[ACT]` (L-L.33); L-0's F-OFFBUS; L-X's F-CLOSE-SCRIPT.

**L-L.33 F-ROWS** — "FIXTURES (each states its failure condition)" (contract :114); a fixture these readings add
beyond the contract's list (L-0.19)
READING: `scripts/tierc12_ferry_fixtures.py`. Two invocations are of record, each with its own transcript:
`--stage=TC12-L` → `T12/ferry/FIXTURES_FERRY_TC12-L.txt` and `--stage=TC12-CLOSE` →
`T12/ferry/FIXTURES_FERRY_TC12-CLOSE.txt`; each runs every block of the table but the of-record instances. A third
invocation, `--of-record`, is the suite's ACT MODE: it is run only by `close_acts.sh` at step 2 (and, in
fixtures, against scratch repositories), selects the instances `F-ROWS [EXIST · of_record]`, `[FRESH · of_record]`,
`[SCOPE · of_record]`, `[RT · of_record]` and `[CUT · of_record]`, and writes
`T12/ferry/of_record/F_ROWS_AT_CLOSE.txt`, which belongs to no progress record. No leg makes a network call; the
git reads are local, read-only and fixture-side. Synthetic frames are built deterministically (no draw). The PASS
line of `F-ROWS [EXIST]` and of `F-ROWS [FORECAST]` reads "GREEN with k HELD", never a bare GREEN, whenever k > 0;
the suite's tally line is L-0.14's.

| block | FAILS IF | planted mutations |
|---|---|---|
| **F-ROWS [SCOPE]** | a tabular file under `T12/` is absent from the manifest or from the typed list; the rule re-derived by the fixture's own implementation disagrees with a record's class; a `BY_TYPE_T` path was passed to the rule; a FERRIED record's rows are not unique on its rule key; a path under `x_rec/` or under a `_det_*` segment (a quarantine directory `_det_partial_*` among them) is classed; a bus name collides; the vocabulary differs from X's text | a new untyped parquet in a scratch tree → HALTED ELEMENT; a per-bar table typed FERRIED → `SCOPE-DISAGREE`; a duplicated row in a FERRIED table copy → `SCOPE-KEY`; a 27th axis word added to a vocabulary copy → `SCOPE-VOCAB`; an order-table copy keyed on `trigger_close_ms` typed FERRIED → `SCOPE-DISAGREE` (the rule reads it POINTED) |
| **F-ROWS [EXIST]** | for a FERRIED record, the staged CSV the fixture re-derives from the source (serialise, cut) does not hash to the manifest's carried sha; where `ferry/_det_staged/<name>.csv` stands (the main tree) its bytes do not hash to the same value — where the directory is absent (a detached review worktree) the block prints `STAGED COPY ABSENT — re-derived from source` and holds the re-derivation alone; anything exists at `exchange/rows/tierc12`. Instance `[EXIST · of_record]`: a WRITTEN record lacks its bus CSV, sha-equal; a HELD record has a bus file or lacks its entry in the manifest or in `ROWS_MANIFEST.md`; a bus file exists that no record names | a staged CSV with one row dropped → `EXIST-STAGED`; a carried sha changed in a manifest copy → `EXIST-STAGED`; a held file copied to a scratch bus → `EXIST-HELD`; a stray CSV on a scratch bus → `EXIST-STRAY` |
| **F-ROWS [RT]** | an untruncated staged CSV, read under the reader law, is not its source cell for cell | a float column re-read with the default parser (must differ on a planted double) → `RT-FLOAT`; a nullable integer read without the schema → `RT-DTYPE` |
| **F-ROWS [CUT]** | a truncated file is not the source's first `k` whole rows; it exceeds the cap; row `k + 1` would have fit; a recorded sha or the last carried key does not re-derive (the synthetic frame is grown, row by row, until its full CSV is at least twice `CAP_BYTES`) | the cut made mid-row → `CUT-ROW`; `k` taken one too many → `CUT-K` |
| **F-ROWS [ORDER]** | the projection order is not L-L.30's, re-derived by the fixture from the registry, the `STATUS.json` arms and the paths | two entries swapped in a manifest copy → `ORDER`; the order sorted by size → `ORDER` |
| **F-ROWS [BOX]** | a constant is not `publish_exchange.py`'s; the tick bytes at the pinned sha do not re-derive from the object store by the fixture's own read-only `git cat-file` loop; the WARN line is not where `level()` turns; the base alone reads REFUSE and something is written | a constant typed in a copy of the ferry → `BOX-CONST`; the working tree's bytes used in place of the pinned blob's → `BOX-BASIS`; a tree with one extra tracked `exchange/` blob → `BOX-BASIS` |
| **F-ROWS [FORECAST]** | the forecast does not re-derive from the pin record; a reservation part is not the key it names in X's record; a landed predecessor is still reserved; the hold of any file is not `level(cum + bytes) != "OK"` | a part's bytes changed in a pin-record copy → `FORECAST-PART`; the first-fit made to stop at the first hold → `FORECAST-FIT`; a scratch tree holding one predecessor's report with its reservation kept → `FORECAST-LANDED` |
| **F-ROWS [FRESH]** | a source re-hashes differently from the manifest, or a staged CSV that stands re-hashes differently from its carried sha. Instance `[FRESH · of_record]` (the leg the act re-runs): the same, and a missing staged CSV is RED | one byte bent in a staged CSV copy → `FRESH`; one byte bent in a source copy → `FRESH` |
| **F-ROWS [ACT]** (scratch repositories only) | `--of-record` reserves a predecessor's adds; pins anything but the scratch HEAD; writes outside `T12/ferry/`; or the copy list is not exactly the WRITTEN set | a predecessor's reservation left in a copy of the of-record planner → `ACT-RESERVE`; a write target under a scratch `exchange/` planted in the copy → `ACT-WRITE`; one HELD file added to a copy of the copy list → `ACT-COPY` (the refusal of a run before X's block has landed is L-X's F-CLOSE-SCRIPT leg, where the planner is stubbed) |
| `F-TYPED-FLOW [ferry.cap_mb]` | the pin bent by one megabyte at its door does not change the rows carried of the synthetic frame of `[CUT]` | a typed copy of the cap in a copy of `cut`'s caller → `PIN-NOT-READ` |
| `F-TYPED-FLOW [ferry.bus_dir]` | the pin bent at its door (another directory string) does not change every would-be bus path of a scratch manifest and of a scratch copy list | the directory typed in a copy of the name builder → `PIN-NOT-READ` |
| `F-DET [ferry]` · `F-PORT` | two builds of the deterministic set (the manifest, the forecast page, the staged CSVs — given the pin record) differ in a byte, or a clock-like key exists (L-0.20); the port law | an `mtime` key planted in a record; the three port plants |

SOURCE: `XR/tierc11x/ferry/FIXTURES_X6_rerun.txt`:31-66 (X's seven legs) [read here]; `LX`:2270-2277 (LX-X6.9:
"GREEN with k HELD"); `AMX`:561-571; L-0.14 (blocks, the tally line, no network leg), L-0.17 (the flow leg), L-0.19
(the hosting rows), L-0.12.
RIVALS: EXIST stays RED until ATHENA rules — X's rejected rival: the hold is ATHENA's act, and a RED fixture would
block the stage on an act that is not the executor's. X's leg filter at the act (`'(EXIST' '(RT)' …`) — not taken:
a transcript is never produced by a leg filter (L-0.9); the act mode is a mode of the suite with its own file.
FAILS-IF: as stated.

---------------------------------------------------------------------------------------------------------------
### What this section files, and when

| record | producer | artifacts |
|---|---|---|
| `TC12-REG.ledger-spec` — this section's one dotted child in L-0.10's `SUBSTAGES_T` (blocking; `depends_on` `TC12-REG`; its own commit; before `TC12-D` in `RESUME_ORDER_T`) | `scripts/tierc12_forward_spec.py` (plain process) | `forward/BOOK_SPEC_COMBINED.json`; `forward/FORWARD_LEDGER.jsonl` (five lines: X's four, the fourth `book_open`); `scripts/tierc12_forward_spec.py`; `scripts/tierc12_forward_fixtures.py`; `forward/FIXTURES_LEDGER_SPEC.txt` |
| (no record of its own: recorded by `TC12-D`'s record, L-0.5) | the orchestrator, immediately after the ledger-spec commit; no builder runs git | `forward/BOOK4_FREEZE.json` — write-once (L-L.17) |
| `TC12-L` | `scripts/tierc12_forward.py`, then `scripts/tierc12_era.py`, then `scripts/tierc12_ferry.py --stage`, `--pin`, `--forecast` (in that order; one process each) | `forward/FORWARD_LEDGER.jsonl` (rows and one refresh line appended), `forward/FORWARD_LEDGER.md`, the three side tables, `forward/build_manifest.json`, `forward/READ_SET.json`, `forward/FIXTURES_LEDGER.txt`; `era/ERA_tables.parquet`, `era/ERA_stamps.parquet`, `era/ERA.md`, `era/build_manifest.json`, `era/READ_SET.json`, `era/FIXTURES_ERA.txt`; `ferry/FERRY_MANIFEST.json`, `ferry/BOX_PIN_TC12-L.json`, `ferry/BOX_FORECAST_TC12-L.md`, `ferry/FIXTURES_FERRY_TC12-L.txt`; the scripts `tierc12_forward.py`, `tierc12_era.py`, `tierc12_pct.py`, `tierc12_ferry.py` and the era and ferry suites. Not artifacts of the record: the staged CSVs under `ferry/_det_staged/` (scratch, pinned by carried sha in the tracked manifest, L-L.32) |
| `TC12-CLOSE` (L-X's record) | `scripts/tierc12_ferry.py --stage`, `--pin`, `--forecast` | the manifest re-recorded with `forecast_TC12-CLOSE` (lawful under L-0.4's last-record law, L-L.32); `ferry/BOX_PIN_TC12-CLOSE.json`; `ferry/BOX_FORECAST_TC12-CLOSE.md`; `ferry/FIXTURES_FERRY_TC12-CLOSE.txt` |
| the operator's close act (no record) | `scripts/tierc12_ferry.py --of-record`, the shell copy, then `tierc12_ferry_fixtures.py --of-record` | `ferry/OF_RECORD.json`, `ferry/of_record/{ROWS_MANIFEST.md, COPY_LIST.txt, F_ROWS_AT_CLOSE.txt}`; `exchange/rows/tierc12/*` |

`TC12-L` is not in L-0.10's parallel set: it starts only when every earlier entry of `RESUME_ORDER_T` is
COMPLETE-VERIFIED. Its record's `depends_on` names every blocking record from `TC12-REG` on that precedes it — the
ferry stages every stage's row files; the ledger reads the records `TC12-REG.ledger-spec`, `TC12-D`, `TC12-ENV`,
`TC12-ENV.score-build`, `TC12-C`, `TC12-V.stamps.c` and `TC12-G`; the era reads `TC12-C` and `TC12-G` — so a
quarantine of any of them makes `TC12-L` PARTIAL with it. The stage has three producers: each returns its artifact
map and the record `progress/TC12-L.json` is written from the three by the orchestrator's gate step (L-0.10's rule
for a record with several producers), with one fixture entry per suite (`forward`, `era`, `ferry`).

Compute: no worker pool in any of the three; the ledger rides twice per book family (the pin and the look-back
anchor) plus two re-ride rivals, in one process. Fixture subprocesses — the era's mirror process, the F-DET twins —
run one at a time (O-5).

**Unverified at drafting — each checked at build, each a HALT or a printed fact:**
- UNVERIFIED: that any forward campaign of any book has closed by the pin. Not looked at. `LEDGER-ROWS` and §0.4
  print "none yet" if none has (L-L.13).
- UNVERIFIED: that the look-back rides on the TC12 snapshot reproduce the two filed book shas, and that the rows
  of campaigns closed at the score edge are pin-stable. Both rest on L-D's prefix identity; F-FWD-ANCHOR decides,
  and a failure HALTs the refresh before any line is appended.
- UNVERIFIED: that the ported era build reproduces X4's two content shas under the build's numpy and pandas.
  F-ERA-MIRROR decides; on a failure no era table is filed and an amendment proposal names the first differing
  cell.
- UNVERIFIED: that the ported object-store reader reads the main repository's packs as they stand at a pinning
  run. `F-ROWS [BOX]` compares its tick bytes with a `git cat-file` loop; a difference HALTs the forecast.
- UNVERIFIED: that exactly one element of P-ADM-1's filed `operative_spec.arms` matches `` ^`scored`\s `` — the
  registry does not exist yet. The spec tool HALTs `FWD-GATE-TEXT` otherwise, at `TC12-REG.ledger-spec`, before any
  bar is read.
- UNVERIFIED: that the class L-L.25 types for each of the other sections' tables is the class the rule returns on
  the built rows (the classes were derived from declared keys and columns; no table exists). `F-ROWS [SCOPE]`
  decides; a disagreement is a HALTED ELEMENT and a dated amendment, never a re-typing at build.
- UNVERIFIED: that X's filed reservation figures equal what the three closes will add (L-L.29).
CHECKED at this revision, no longer open: L-C.4's campaign frame carries `lag`, both close instants,
`era_of_entry`, X's eleven `TIDE_COLS` and X's fifteen `BOOK_COLS` under those names (`scripts/tierc11_books.py`
:192-209 against `XB`:208-211 and `XE`:227, by `ast`).

---------------------------------------------------------------------------------------------------------------
### REGISTRATION SPEC · (none owned by L-L)

L-L owns no registered row and files no registration: Stage L files a diary, Tier-E tables and row files; none
carries a hypothesis, a family, a bar or a verdict word, and no spec block of this section is carried into the
registry. One clause of an owner's spec is worded here, and L-G's P-ADM-1 block carries it verbatim:
- **P-ADM-1 (L-G), `disclosed_beside`:** "the forward ledger's fourth book `gated-v6-combined` — its spec
  `research_outputs/tierc12/forward/BOOK_SPEC_COMBINED.json` (sha filed at TC12-REG.ledger-spec); every row
  appended at TC12's pin entered before the book was frozen (flagged on the row) and none is a row of record for
  confirmation; `n` appended at TC12's pin, UNSCORED until its own n ≥ n_min; Tier-E, no verdict word; it is the
  contract's 'confirmation' (:55-56) and none of it is scored here."
- **No precondition is offered to P-ADM-1.** The fourth spec is filed after the registry and cannot be a
  precondition of a registration in it; the tie between the two runs the other way — the spec carries
  `p_adm_1_payload_sha256` and the sha of the one `scored` element (L-L.2), and F-FWD-SPEC holds both to the filed
  registry.

---------------------------------------------------------------------------------------------------------------
### OPEN TO OPERATOR

1. **Which ledger is of record for base v6 and 9/12 from now on.** Default if silent: TC12's file, from its first
   refresh line (O-24); TC11's file stays at 0 rows and is never refreshed; X's two lines keep their frozen role
   text "X twin — TC11's ledger not yet opened", printed beside TC12's statement.
2. **The one campaign that is both inside the scored window and on the ledger** (9/12, SOL, entered
   2026-09-24T16:00Z). Default if silent: when it closes it is appended, counts in the 9/12 book's `n`, carries
   the chained flag `in_o9_scored_window`, and is NOT a row of record for any later score — the rows of record are
   fixed in `n_law` (L-L.17); the all-rows figure is printed beside. Keeping it off the ledger altogether, or
   counting it as a row of record, is the operator's order.
3. **"The gated books" of the era clause.** Default if silent: the ledger's two gated books (OLD-gated,
   combined-gated) beside v6. Tabling the kept books of P-BRD-1 or P-DIR-1 as well is an order, not a reading.
4. **The box.** On the filed figures the three pending closes alone bring the box to the WARN line. Default if
   silent: every TC12 row file that would leave OK is HELD FOR ATHENA and listed; `ROWS_MANIFEST.md` and the report
   land under `publish()`'s warning; REFUSE is never overridden. Releasing held files, the cap (the contract's
   2 MB against the bus's 1,048,576 B per file) and a rotation rule for `exchange/rows/` are ATHENA's (Q-A1, Q-A2).
5. **The closing order.** Default if silent: TC12's ferry of record refuses until X's block has landed. Closing
   TC12 before X would change which of X's files are held; only the operator can order it.
6. **The next refresh.** Each refresh is a data spend at a new pin. Default if silent: none after the one line at
   TC12's pin; the ledger waits for a later tier or an operator order.
7. **The fourth book's backdated origin.** The contract opens all four books at 2026-09-21T16:00Z; the fourth
   book's gate text was filed at STEP Q and its spec was frozen on the chain at the ledger-spec commit, both after
   TC12's pin, so every row of this refresh predates both (L-L.17). Default if silent (O-32): the contract's
   origin stands; every such row is appended, counted in `n`, and carries the chained flags
   `entered_before_contract_filed` and `entered_before_book_frozen`; the rows of record are fixed in `n_law`
   (L-L.17) — for the fourth book, rows entered after the freeze instant — so its `n_record` is 0 at this
   refresh; the all-rows figure is printed beside. Moving the origin itself, or taking STEP Q in place of the
   freeze instant as the binding flag, is the operator's order.
8. **The row set of record for a later forward score is fixed now.** It is the contract's "confirmation" of
   P-ADM-1 (:55-56) that is at stake. Default if silent: `n_law` as L-L.17 words it — a row inside O-9's scored
   window is never of record for any book, a fourth-book row entered before the book was frozen is never of record
   — and no later registration may choose otherwise. Changing the rule after this text is frozen needs an
   amendment and a re-opened ledger (L-L.3).
9. **The 1w block is left out of the ledger's side table.** Default if silent: `ledger_side` copies the 1h, 4h,
   12h and 1d blocks of the entry stamp and points to the stamp row for the rest (O-28: the 1w block has exactly
   two readers). Carrying it into a table that reaches the bus is an order that would amend O-28.

---------------------------------------------------------------------------------------------------------------
### INTERFACE ASSUMPTIONS

Each line names where the other section's text supplies what this one leans on.
- **L-0 (laws, process).** `TC12-REG.ledger-spec` is a row of L-0.10's `SUBSTAGES_T` (blocking, `depends_on`
  `TC12-REG`, before `TC12-D` in `RESUME_ORDER_T`), with its own record, gate and commit; T3 and T4 are met by
  L-L.3 and L-L.30. L-0.19's map matches the contract name `F-LEDGER` to blocks by EXACT FID, so L-X's
  `F-LEDGER-FMT` is never one of them. `scripts/tierc12_forward_spec.py`, `tierc12_forward.py`, `tierc12_era.py`,
  `tierc12_pct.py` and `tierc12_ferry.py` are decision modules; none is a door; `tierc12_forward_spec`,
  `tierc12_era` and `tierc12_pct` are on `VA_BLIND_T` (L-0.22), `tierc12_forward` and `tierc12_ferry` are not (the
  first opens the two stamp tables of L-L.16, the second enumerates `T12/`); none is a process tool (they are
  scanned by F-TYPED); none holds a subprocess site. `tierc12_progress.certified` (L-0.4) exists from the TC12-REG
  commit and is stdlib-only. The pin map holds this section's four rows — `ledger.opening` (:109, iso),
  `ledger.n_min` (:110, int), `ferry.bus_dir` (:111, str), `ferry.cap_mb` (:112, int) — and L-G's `adm.lag_cut`
  (:54), which the predicates read; `seed` is the tier's. `BYTES_PER_MB` is in `UNITS_T`. None of this section's
  tables is a registered table: every parquet it writes goes through `put` and is collared; the chain's lines are
  a diary and carry no collar (X's AM-X8 (a1)). L-0.5 lists `forward/FORWARD_LEDGER.jsonl` append-only throughout
  and `forward/BOOK4_FREEZE.json` write-once from `TC12-D`'s record; the orchestrator writes that file.
  L-0.4's last-record law makes the two re-recorded paths lawful (`forward/FORWARD_LEDGER.jsonl`,
  `ferry/FERRY_MANIFEST.json`). L-0.14 gives the block grammar, the leg states, the fixture RNG, `--root` and the
  pre-substrate header the ledger-spec transcript prints; L-0.13 writes `READ_SET.json` beside each
  `build_manifest.json`; L-0.17 hosts a flow leg per pin in the consuming suite.
- **L-D (substrate, env).** `E.TC10_PIN_MS`, `E.TC11_PIN_MS`, `E.TC11_PIN_ISO`, `E.PIN_MS`, `E.ERA_CUT_MS`,
  `E.SEED`, `E.N_BOOT`, `E.CLASSIC5`, `E.PANEL17`, `E.era_of`, `E.fees()`, `E.load_asof_at` (any instant at or
  before the pin), `E.load_funding_asof_at`, `E.x_rec`, `E.tc11_record`, `E.tc10_record` (the referee's function;
  `STEP0_RECORD.json` is on its allow-list), `E.read_set()`; the lineage aliases `E.LAB` and `E.R7`; the prefix
  identity of the snapshot (L-D.12), without which no appended row could re-derive;
  `T12/env/SUBSTRATE_VERIFY.json`; the STEP Q instant as L-D.1's object. Reads of `.git/` objects and of
  `exchange/` are ordinary repo reads under the shim (L-D.27 lists neither as read-never). `TC11_ALLOW_FILE`
  holds the rows this section needs: `PROGRESS.json`, `LEANS.md`, `data/AS_OF_PIN.json`,
  `forward/{FORWARD_LEDGER.jsonl, FORWARD_LEDGER.md}`, `registrations/{REGISTRATIONS.json, REGISTRY_PIN.json}`,
  `books/v6_campaigns.parquet`, `stage_g/g_grid_books.parquet`, `regbooks/P-AGE-1/scored.{parquet, json}`. `x_rec`
  rows: `tierc11x/forward/{FORWARD_LEDGER.jsonl, BOOK_SPECS.json}`, `tierc11x/books/{build_manifest.json,
  v6_x_campaigns.parquet}`, `tierc11x/era/{X4_tables.parquet, X4_stamps.parquet, build_manifest.json}`,
  `tierc11x/ferry/FERRY_MANIFEST.json`, and the texts `scripts/tc11x_{forward, era, pct, ferry, books}.py` with
  their fixture files. TC12's ferry carries `T12/` files only and lists no TC11 directory.
- **L-C (control).** `scripts/tierc12_books.py` (L-C.4's API): `corridor`, `r912`, `v6_book`, `trg912_book`,
  `book_sha`, `tide_pool`, `band_of`, `abs_tide_cut`, `replay_h(sym, lo_ms, hi_ms, *, refuse=None)` and
  `campaign_rows(book, roles, lo, hi, pool, name)` — the mirror of TC11's function, whose columns hold `lag`, both
  close instants, `era_of_entry`, X's eleven tide columns and X's fifteen `BOOK_COLS`; there is no port of X's
  `campaign_rows`. The filed scored-window table `books/v6_campaigns.parquet`; the extended frames
  `books/{v6,trg912}_ext_campaigns.parquet` that the stamps child reads; `books/strip.parquet`. The module is on
  `VA_BLIND_T`. **One request stands:** L-C's strip prints rows and `n` only (L-X.14's `strip` law) — a ΣR over
  the v6 strip would be an aggregate over the ledger's v6 rows by another name.
- **L-G (admission).** The gate text of the fourth book is the one `` `scored` `` element of P-ADM-1's `arms`
  (L-G.7 cites the same selector), and P-ADM-1's `disclosed_beside` carries the clause above verbatim. Its refused
  set is exactly L-L.2's `p_adm_1_refuses` on the scored window (OLD by the entry-bar trailing band; `lag ≥` the
  pin `adm.lag_cut`; a `None` band HALTs). `regbooks/P-ADM-1/scored` exists when TC12-L runs (the row has no
  precondition). `tierc12_books.replay_h` is the one refusal hook (L-G.18).
- **L-V (value area).** `va/stamps/VA_STAMPS_v6.parquet` and `VA_STAMPS_trg912.parquet` are filed by the reader at
  `TC12-V.stamps.c`, keyed `[book, symbol, entry_ms, instant_kind, instant_ms]`, with an `entry` instant stamped
  at the entry bar's close and the lens blocks of L-V.20; their shas are in that child's record. The classes of
  the Stage V files are typed in L-L.25: `va_bars_*`, `va_events`, `va_regimes`, `traverse_legs`, `va/trades/*`
  and `va/stamps/*` are POINTED; `va_stack` is FERRIED.
- **L-R, L-S.** Their tables' classes are typed in L-L.25 from the keys they declare: the order tables on
  `known_at_ms`, the MISS table with `variant`, the grids with `panel`, the directories `stage_r/dir|sfp|tables/`
  and `stage_s/`. Nothing is left for assembly.
- **L-X (statistics, registrations, close).** `close_acts.sh` hosts the ferry at step 2 as L-L.32 words it (python
  plans, the shell copies, then `tierc12_ferry_fixtures.py --of-record`); the sandbox proof of the script stubs
  the planner call; the close stage runs the second forecast after the draft and the append exist; L-X.32 renders
  each stamp bracket at a fixed byte width, so the staged bytes are the stamped bytes; BOX_COST reads the forecast;
  §0.4 prints `LEDGER-BOOKS` and `LEDGER-ROWS` whole and the report points to `ERA.md` for `ERA_tables` (L-X.28's
  frozen map); the three predecessor report paths are L-X's objects; `tierc12_regbook` (filed at
  `TC12-ENV.score-build`) holds the fee identities the side table uses and writes every regbook arm, empty arms
  included; ATTEST-ORDER covers the ledger-spec commit by its descendant test (L-X.21).

---------------------------------------------------------------------------------------------------------------
### OBJECTIONS

None against a ruling. O-1 … O-32 were checked against the files this section cites, and section H (O-25..O-32)
is conformed to: O-28 (the ledger's side table leaves the 1w block where the reader filed it, L-L.16), O-29 (the
ledger joins filed stamp rows and imports no door, L-L.16), O-31 (`TC12-REG.ledger-spec` is a dotted child,
L-L.3), O-32 (the fourth book keeps the contract's origin with every pre-filing row flagged, L-L.17). O-24's facts
hold on the bytes (X's ledger verifies under `forward_log`'s law and that law admits a fifth line; TC11's chain is
a different law and cannot be continued). Two things a reader of O-24 should know, stated in the readings and not
objected to: X's OWN verifier refuses a fourth `book_open` (a three-book law, L-L.6), so TC12's structure law is a
declared difference from it; and opening on X's bytes makes X's two "twin" lines the freeze records of base and
9/12 in TC12's chain (L-L.1, OPEN TO OPERATOR 1).
