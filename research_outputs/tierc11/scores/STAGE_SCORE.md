as_of_last_closed_4h: 2026-09-25T00:00:00Z

# TIER-C11 · STAGE TC11-SCORE — the scorer of the nine (build report, REPAIRED)

Executor HEPHAESTUS · seed 20260924 (sensitivity 20260816) · N_BOOT 4000 · registry head `6772568b31fcfb2d…` (verified) · readings L-1.4, L-1.5, L-1.3, L-R.2, L-S.1, L-W.4, AM-3, AM-7 · the REGBOOK INTERFACE of the stage wave.

**This stage computes no registered result.** The scorer was proven on PLANTED synthetic regbooks. On the real regbooks it ran as a DRY RUN (book facts only, labelled "book, not a verdict") and through its full path with the bootstrap STUBBED to NaN draws, which exercises every code path and computes no interval, no p and no verdict. The scoring of record is the orchestrator's run of `scripts/tierc11_score.py` once all nine regbooks are filed.

This report replaces the build report of the first build. The repair followed VERIFY TC11-SCORE (0 BLOCKER, 2 MAJOR, 20 MINOR). The section "Repair" lists every defect and what was done with it.

## Files

| file | sha256 |
|---|---|
| `scripts/tierc11_score.py` | `79a2c216bd3083b5db8add785357c9787631dbd50cc26dd45eb77d432215f0bd` |
| `scripts/tierc11_score_fixtures.py` | `c591e748d9cb2cd8209d0287a2de8a616e9ff3e01ff1f91b3d01928b556bf5ea` |
| `research_outputs/tierc11/scores/FIXTURES_SCORE.txt` | `dbcc36ad8818812261478c822fe195d0b73223dd6ba59e450b2dfed08bd56a3f` |

F-DET twin output (planted run, `research_outputs/tierc11/scores/_det_score/seed_1/`, gitignored; seed 1 == seed 20260924 == in-process render; the regbooks root is printed as the fixed token `PLANTED/planted_regbooks`):

| file | sha256 |
|---|---|
| `BASE_IDENT.json` | `40feb06e52fd43d55f107ea1c7ba2a8137bdd4739d964584b7bf79877e763f6b` |
| `FAMILY.json` | `f786269d33c83e93ff16750bf0e64648004093af49a0085b7a5a59a13a3c47fd` |
| `REGISTRY_CHECK.json` | `601c9195bdc82f130fe64d462a9def584dce8fc9616d7f6a0e034d8e61bc3b22` |
| `S0_VERDICTS.md` | `ff969ed6931c4f4d641b3b740959a389c439d00a466ae17962e751ba1f9e0b0d` |
| `SCORES.json` | `755bb8164dd4e61d1db8cdef5343cfbc0c8975015f15ab304eb6630154529340` |
| `SCORE_MANIFEST.json` | `7d78bad70677e6a37aa7cfffa818ae206f5d7621b3c9e31a46cc6793780b7a32` |

## Repair (VERIFY TC11-SCORE: 2 MAJOR, 20 MINOR)

No rule was changed after a number was seen. Every repair below adds a check or a print that a frozen reading already required. None of them moves a registered statistic.

| defect | outcome | what was done |
|---|---|---|
| MAJOR-1 pick stability not flagged (L-R.2) | FIXED | SC-14. The lens each SCALE row consumes is typed from its text of record (P-BRK-4H 4h, P-ADD-BRK and P-ADD-SFP 1h, P-TP-RNG 12h). The per-CLASSIC5 change is read from `ranges/SCALE_PICKS.json` (first half of tuning vs tuning). It is printed in the §0 SCALE cell ("pick stability (…): CHANGED on …", with the count of campaigns on a changed asset) and on every Tier-E row of that registration that consumes the calibrated pick. Frozen-3.0 arms say "no calibrated pick consumed". A regbook `stability_changed[_<lens>]` column that disagrees with the record is a disclosure note; on the real books none disagrees. |
| MAJOR-2 F-VERDICT checked SCALE by substring only | FIXED | `scale_findings` in F-VERDICT. On each of the 4 SCALE rows: the printed holdout-slice n and point == this file's own era=='holdout' (by close) ruling; the frozen twin == the typed arm, with n and point == this file's (ABSENT where none is filed); pick stability flags exactly the typed changes (1h BTC SOL NEAR · 4h NEAR · 12h BTC ETH SOL, also re-read from SCALE_PICKS.json and required equal) on the §0 cell and on every consuming Tier-E row; the in-sample holdout count == this file's; the fallback label (below). New plants: holdout→tuning, frozen twin dropped, stability dropped, P-TP-RNG's lens read as 4h, fallback label dropped. |
| m-1 stale report (P-WARN-1 re-filed 02:35) | FIXED | This report is regenerated. The dry run is re-run on the regbooks as filed now. F-BASE-IDENT is OK and exit is 8 (ABSENT, the new bit-flag word). Old Finding 1 is marked resolved. |
| m-2 `canonical_csv` does no quoting | FIXED (HALT form) | SC-19. A string field that holds `,` `"` CR or LF HALTs the arm (REGBOOK-STR), so it can no longer surface as a spurious BOOK-SHA. The builders' own CSV laws already ban these characters. F-KEY plant: a `,` in a lane. |
| m-3 dtypes looser than the interface | FIXED | entry_ms, entry_close_ms and exit_close_ms must be int64 and direction int8 exactly. F-KEY plants: int64 direction, int32 exit_close_ms. |
| m-4 entry_ms semantics unchecked | FIXED | 0 < entry_close_ms − entry_ms ≤ one lens step: the sidecar's optional `lens`, else 4h (the lens bar of every TC11 registered book; the relay's 1h entries sit inside their 4h bar). F-KEY plant: an 8h entry bar. |
| m-5 L-1.5 identity law not asserted | FIXED | SC-15. On every paired arm ruled against its own base (the scored arm and paired Tier-E arms; never a base_arm head-to-head), rows whose `acted_by` is blank must equal the base exactly on net_r, exit_close_ms and exit_reason. A regbook without `acted_by` HALTs too. It is also checked in the dry run. Real books: 158 / 148 / 191 / 164 unacted rows hold (P-WARN-1 / P-ADD-BRK / P-ADD-SFP / P-TP-RNG), and every paired Tier-E arm holds. |
| m-6 gate post-filter not enforced | FIXED | SC-16. A gate's scored arm with a key outside the base, or a kept row that differs from the base on any of the 16 columns, HALTs (it used to be a note). Checked in the dry run too. Both real gates hold. |
| m-7 gating status words trusted | FIXED | SC-17. P-WARN-1's STATUS must agree with its `condition.json`: BUILT iff met True, CONDITION_NOT_MET iff met False, met == (ci_hi < 0), and the record must exist. P-SCALP-2's STATUS must agree with `stage_r/R2_LENS_VERDICTS.json` lenses['1h']['verdict']: BUILT iff PASS. P-SCALP-2's §0 cell prints the tuning-era R2 1h word beside it, collared [§10], in every state (ABSENT included). New fixture F-STATUS. |
| m-8 AM-3 ignored `v6_funding_absorbed_r` | FIXED | The v6 leg's own absorption is taken from the add book's `v6_funding_absorbed_r` when carried, else from the base's uncapped − capped, and the source is printed. The planted add books now carry a nonzero v6-leg absorption, so F-VERDICT's AM-3 check detects the old law. |
| m-9 exit codes mask each other | FIXED | SC-10. The exit code is a bit-flag word: +2 registered HALT, +4 Tier-E halted, +8 ABSENT, +16 no-clobber. Every condition is printed on an `EXIT` line, and the dry run uses the same word. New fixture F-EXIT covers all 16 subsets, and the dry run on a family with all three row conditions exits 14. |
| m-10 LOAO per-panel tables uncollared | FIXED | Every LOAO per-panel table in S0_VERDICTS.md carries tier / selection_not_a_result / gates, and so does every per-panel dict in SCORES.json. |
| m-11 P-BRK-4H holdout slice not fully causal | FIXED | SC-4. Beside the holdout slice the cell prints how many of its campaigns carry a range read at or before the era cut. This is read from the regbook's `scale_in_sample*`, `n_adds_scale_in_sample` and `die_close_ms` columns. Real P-BRK-4H: 1 of 112. |
| m-12 LEANS_AMENDMENTS.md not hashed | FIXED | Its sha is recorded in REGISTRY_CHECK.json, S0_VERDICTS.md and SCORE_MANIFEST.json, beside the sha of every plain-JSON record read (SCALE_PICKS.json, R2_LENS_VERDICTS.json, condition.json). |
| m-13 panel17 Tier-E row lacks the IN-SAMPLE label | FIXED | SC-14. Every row that holds an asset whose pick at the consumed lens fell back to the whole tape carries "IN-SAMPLE everywhere (whole-tape pick fallback [L-R.2]): …". Real P-BRK-4H `tierE__panel17`: HYPEUSDT 4h and PUMPUSDT 4h (26 of 762 campaigns). |
| m-14 adds head-to-head never derived | FIXED | SC-18. When neither add registration files a Tier-E arm whose base_arm is the other's scored arm, the scorer derives `derived__head_to_head_vs_<other>` (paired, collared). Stage A has since filed both head-to-heads (base_arm set), so on the real books nothing is derived. The planted P-ADD-SFP exercises the derivation. |
| f-1 no straddling entry bar planted (m1 survived) | FIXED | The planted P-BRK-4H lane holds one BTC campaign whose 4h entry bar opens 2024-06-30T20:00Z and closes 2024-07-01T00:00Z. F-KEY requires it to read 'holdout' and to be counted 1. Plant: the era judged by the open. |
| f-2 m4 m5 m6 m8 survived; missing plants | FIXED | F-KEY plants: sidecar sum_net_r, sidecar era_scope, REGBOOK-TIME ×2, REGBOOK-RDIST, REGBOOK-STR, REGBOOK-DTYPE ×2. F-STATUS covers STATUS-ILLEGAL. F-VERDICT covers the sensitivity-seed verdict, using a harness T5 whose draws are +1 at the seed of record and −1 at the sensitivity seed, on 3 rulers. F-EXIT covers the exit flags. |
| f-3 SC-3 caught only by F-DET | FIXED | F-RULER (i). A holdout-scoped paired arm (P-ADD-SFP) and a holdout-scoped two-sample arm (P-WIN-1, new) must be ruled against the base's 77 holdout rows, with point == this file's. Plant: the base not restricted. |
| f-4 single examples where more were possible | FIXED | The paired premise and identity law are checked on all 4 paired registrations (P-WARN-1 through its Tier-E rule book), the identical-key flag on all 3 two-sample registrations, and the base-ident row halt and scope on all 7. The vs-zero base check stays on P-BRK-4H alone: it is the only vs-zero registration the planted family can BUILD, because P-SCALP-2 is closed by the R2 record it must agree with. |
| f-5 F-RULER plants caught indirectly | FIXED | "Two-sample read as paired" and "vs zero read as two-sample" are now expected at RULER-TABLE, the property they name. The identical-key flag and "vs zero reads its base" get their own plants (SC-6 flag suppressed; `_uses_base` forced). |
| f-6 transcript not reproducible under `--root` | FIXED | The scorer takes `--regbooks-label=`, and the fixtures pass the fixed token `PLANTED/planted_regbooks` in-process and in F-DET, so the outputs no longer embed the run root. |

**Mutation check (scratch).** The real fixture file was run against 20 mutated copies of the repaired scorer (the verifier's m1..m8 re-cut on the new source, plus 12 for the new checks) and one unmutated control. All fixtures ran except F-DET. The copies were cut from the repaired scorer before a final edit that touched the docstring only; no code line differs. The results are in the table below.

**f-6 checked directly.** A whole run (13 fixtures, F-DET included) under a scratch `--root` gave a transcript byte-identical to the filed one (sha `dbcc36ad8818812261478c822fe195d0b73223dd6ba59e450b2dfed08bd56a3f`), and its F-DET outputs were byte-identical to `_det_score/seed_1/`.

| # | mutation | tally (12 fixtures, F-DET excluded) | result | RED fixtures |
|---|---|---|---|---|
| m0 | none (control) | 12 GREEN / 0 RED | control: all GREEN | — |
| m1 | era judged by entry_ms (the open) | 5 GREEN / 7 RED | CAUGHT | F-RULER; F-BOOT; F-VERDICT; F-COLLAR; F-GRID; F-KEY; F-DRYRUN |
| m2 | frozen-3.0 twin dropped from the SCALE cell | 11 GREEN / 1 RED | CAUGHT | F-VERDICT |
| m3 | Tier-E base not restricted to the arm's era_scope | 11 GREEN / 1 RED | CAUGHT | F-RULER |
| m4 | sidecar sum_net_r check disabled | 11 GREEN / 1 RED | CAUGHT | F-KEY |
| m5 | STATUS-ILLEGAL guard removed | 11 GREEN / 1 RED | CAUGHT | F-STATUS |
| m6 | sensitivity-seed verdict copied from the main seed | 11 GREEN / 1 RED | CAUGHT | F-VERDICT |
| m7 | SCALE 'holdout slice' computed on the tuning era | 11 GREEN / 1 RED | CAUGHT | F-VERDICT |
| m8 | no exit flag when a registered row HALTs | 11 GREEN / 1 RED | CAUGHT | F-EXIT |
| m9 | pick stability omitted from the §0 SCALE cell | 11 GREEN / 1 RED | CAUGHT | F-VERDICT |
| m10 | identity law not asserted on registered paired rows | 11 GREEN / 1 RED | CAUGHT | F-RULER |
| m11 | gate post-filter check off (registered rows) | 11 GREEN / 1 RED | CAUGHT | F-RULER |
| m12 | BUILT accepted while condition.json says NOT MET | 11 GREEN / 1 RED | CAUGHT | F-STATUS |
| m13 | scale flags dropped from filed Tier-E rows | 11 GREEN / 1 RED | CAUGHT | F-VERDICT |
| m14 | REGBOOK-STR check off | 11 GREEN / 1 RED | CAUGHT | F-KEY |
| m15 | any integer dtype accepted | 11 GREEN / 1 RED | CAUGHT | F-KEY |
| m16 | entry-bar bound off (only a negative gap refused) | 11 GREEN / 1 RED | CAUGHT | F-KEY |
| m17 | tuning-era R2 word not printed | 11 GREEN / 1 RED | CAUGHT | F-STATUS |
| m18 | adds head-to-head never derived | 10 GREEN / 2 RED | CAUGHT | F-COLLAR; F-GRID |
| m19 | AM-3 ignores v6_funding_absorbed_r | 11 GREEN / 1 RED | CAUGHT | F-VERDICT |
| m20 | fallback IN-SAMPLE label off on Tier-E rows | 11 GREEN / 1 RED | CAUGHT | F-VERDICT |

## What the scorer does

1. **Verifies REGISTRATIONS.json before any read or score, and HALTS on any mismatch** (nothing is written). It checks the contract sha (typed `bb38e016…`), re-cuts each of the 9 text slices and their contexts from the contract by line number, recomputes the 9 payload shas by the file's own law, and re-walks the hash chain from the zero genesis. The head must equal the last chain line, `REGISTRY_PIN.json` and the typed `6772568b…`. It checks the family (m 9 / q 0.10 / bar 0.011111 / seed) and the LEANS and file shas, and hashes LEANS_AMENDMENTS.md.
2. **Reads only the REGBOOK INTERFACE** (plus the plain-JSON records named in SC-14 and SC-17) and validates every arm: the 16 columns, exact dtypes, no nulls, no CSV-hostile strings, unique keys, direction ±1, era == `E.era_of(entry_close_ms)`, the entry-bar bound, the AM-7 haircut law, and the sidecar's n / sum / book_sha256 / ruler / panel / era_scope / collar. A failure HALTS that row only.
3. **Cross-checks the status word** against the spec and its gating record, and asserts the identity law and the gate post-filter before any ruler.
4. **Rules** each BUILT registration by the ruler its SPEC names: vs_zero `T5.cluster_boot`; two_sample `T5.cluster_boot_diff`; paired `T5.cluster_boot` of deltas keyed (symbol, entry_ms).
5. **Prints the verdict and what sits beside it.** verdict_of_record = SUPPORTED iff ci_lo > 0 AND p ≤ 1/90, judged exactly (SC-1). Beside it, deciding nothing: the deciding bound, the sensitivity seed, LOAO (both seeds), the haircut twin, D15 and the named risk, the gate cohort and appendix, the AM-3 adds print, the honesty labels, SCALE-IN-SAMPLE (holdout slice, in-sample count, frozen-3.0 twin, pick stability, fallback label), the Tier-E slices, and the tuning-era R2 word beside P-SCALP-2.
6. **CLOSED_BY_PRECONDITION / CONDITION_NOT_MET** print their reason, no number and "no slot spent". Tier-E rows are collared and carry no verdict word.
7. **F-BASE-IDENT**: the seven base arms must share one sha and equal `books/v6_campaigns.parquet` at 6 dp. A row whose base fails HALTS.
8. **Writes** REGISTRY_CHECK.json, SCORES.json, FAMILY.json, BASE_IDENT.json, S0_VERDICTS.md and SCORE_MANIFEST.json, with no clobber (`--refile`). `--dry-run` writes nothing and rules nothing. The exit code is the SC-10 bit-flag word.

## Executor sub-readings (the frozen text is silent; printed in every transcript and S0_VERDICTS.md)

- [LEAN-HEPHAESTUS] L-1.4 rulers from the SPEC (paired: P-WARN-1, P-ADD-BRK, P-ADD-SFP, P-TP-RNG · two-sample: P-AGE-1, P-WIN-1, P-RELAY-1 · vs zero: P-BRK-4H, P-SCALP-2); T5.cluster_boot / cluster_boot_diff / _ci_from, asset clusters, seed 20260924 (20260816 beside), n_boot 4000 passed explicitly
- [LEAN-HEPHAESTUS] L-1.4 verdict_of_record = SUPPORTED iff ci_lo > 0 AND p <= 0.10/9, else NOT SUPPORTED ('— CI wholly below zero' when ci_hi < 0); m = 9 in every case
- [LEAN-HEPHAESTUS] SC-1 clause (b) exact: p = (k+1)/(B+1) <= 1/90 <=> 90(k+1) <= B+1; deciding bound = the floor((B+1)/90)-th smallest finite draw (44th of 4000); numpy's 1.111th percentile beside
- [LEAN-HEPHAESTUS] SC-2 LOAO = TP.loao_n's law keyed (symbol, entry_ms): N = declared panel, unbootstrappable panel counts against, above-only, bar ceil((N+1)/2); decides nothing
- [LEAN-HEPHAESTUS] SC-3 Tier-E paired / two-sample arm: vs the registration's base restricted to its era_scope, or the sidecar's optional base_arm
- [LEAN-HEPHAESTUS] SC-4 SCALE-IN-SAMPLE: holdout slice derived from the scored arm (a tierE 'holdout*' arm beside); frozen-3.0 twin = tierE arm slugged '*frozen*'; the holdout campaigns whose range read fell <= the era cut counted beside
- [LEAN-HEPHAESTUS] SC-5 refused cohort = base keys absent from the scored arm; 'on per-campaign expectancy only; the gate forfeits +X R total' iff mean(refused) > 0
- [LEAN-HEPHAESTUS] SC-6 two-sample on identical key sets: FLAGGED, not halted
- [LEAN-HEPHAESTUS] SC-7 F-BASE-IDENT: one book_sha256 across the base arms AND equal to books/v6_campaigns.parquet on 13 columns at its 6 dp; a row halts if its base fails v6 or the v6-equal bases split
- [LEAN-HEPHAESTUS] SC-8 honesty <hazard> = '<key>: <text up to its first top-level ;>'
- [LEAN-HEPHAESTUS] SC-9 Tier-E: would_read_ci_only in {CI above zero (lo > 0) | CI includes zero | CI wholly below zero (hi < 0) | no interval}; collar tier/selection_not_a_result/gates
- [LEAN-HEPHAESTUS] SC-10 registry mismatch halts the scorer before any write; a book / premise / identity failure halts its row only; exit = bit flags: +2 registered HALT, +4 Tier-E halted, +8 ABSENT, +16 no-clobber; every condition printed
- [LEAN-HEPHAESTUS] SC-11 era-full registrations: tuning + holdout slices beside, Tier-E [L-1.3]
- [LEAN-HEPHAESTUS] SC-12 sidecar sum_net_r at 1e-6; AM-7 haircut law at 1e-12 (HALT on scored/base, disclosure on Tier-E)
- [LEAN-HEPHAESTUS] SC-13 book_sha256 = sha256(canonical CSV of the 16 required columns sorted (symbol, entry_close_ms), floats repr)
- [LEAN-HEPHAESTUS] SC-14 pick stability [L-R.2]: lens consumed P-BRK-4H 4h, P-ADD-BRK / P-ADD-SFP 1h, P-TP-RNG 12h (texts of record); the per-CLASSIC5-asset change (SCALE_PICKS.json first half of tuning vs tuning) flagged on the §0 SCALE cell and every Tier-E row consuming the calibrated pick; whole-tape fallback cells labelled IN-SAMPLE
- [LEAN-HEPHAESTUS] SC-15 identity law [L-1.5]: paired arms vs their own base — rows with acted_by blank equal the base exactly on net_r, exit_close_ms, exit_reason, else HALT
- [LEAN-HEPHAESTUS] SC-16 gate = post-filter [L-1.5]: no key outside the base, every kept row equal to the base on the 16 columns, else HALT
- [LEAN-HEPHAESTUS] SC-17 gating status cross-checked: P-WARN-1 vs condition.json (met, ci_hi < 0), P-SCALP-2 vs R2_LENS_VERDICTS.json 1h; the tuning-era R2 1h word printed beside P-SCALP-2, collared [§10]
- [LEAN-HEPHAESTUS] SC-18 adds head-to-head: derived (paired, collared) when not filed with a base_arm
- [LEAN-HEPHAESTUS] SC-19 regbook strictness: int64 times, int8 direction, no ',', '"', CR, LF in a string field, 0 < entry_close_ms - entry_ms <= one lens step (4h unless the sidecar names a lens)

## Fixture tally — 13 GREEN, 0 RED

Transcript `research_outputs/tierc11/scores/FIXTURES_SCORE.txt` (sha `dbcc36ad8818812261478c822fe195d0b73223dd6ba59e450b2dfed08bd56a3f`), exit 0.

- [PASS] F-SCORE-REG: scorer verifier: 0 finding(s); this file's re-derivation: slices 9/9, payload shas 9/9, chain links 9/9, head 6772568b31fcfb2d… == REGISTRY_PIN.json == typed; contract bb38e016a8f3e55c…; REGISTRY_CHECK.json 9 rows all re-cut-equal and payload-equal: True
  - [BREAK] RED (correct): all 9 plants caught by their named detector, one at a time: one character of P-AGE-1's text_of_record -> TEXT-SLICE: P-AGE-1 lines 45-46 re-cut from the contract != text_of_record · P-WIN-1 operative_spec.era -> holdout -> PAYLOAD-SHA: P-WIN-1 payload hashes to 40156208ee4da9ba… != filed d19a42a329be3bfe… · chain line 5 prev replaced -> CHAIN: line 5 prev ffffffffffffffff… != the previous line's sha 627442c219dcb587… · chain line 9 line_sha256 replaced -> CHAIN: line 9 line_sha256 eeeeeeeeeeeeeeee… != recomputed 6772568b31fcfb2d… · REGISTRY_PIN head replaced -> HEAD: REGISTRY_PIN.json head dddddddddddddddd… != REGISTRATIONS.json head 6772568b31fcfb2d… · one contract byte flipped -> CONTRACT-SHA: the contract hashes to 06dfd4821e9ba95acf665864eee79fe8c11848915e9e240480155569fd93405d != STEP Q bb38e016a8f3e55ca3bcc09fec53ba6b8dc40accb60d054f8163d033a8 · P-SCALP-2 dropped -> ORDER: registrations ['P-WARN-1', 'P-AGE-1', 'P-WIN-1', 'P-BRK-4H', 'P-RELAY-1', 'P-ADD-BRK', 'P-ADD-SFP', 'P-TP-RNG'] != the typed nine ['P-WARN-1', 'P-AGE-1', 'P-WIN-1' · family_m 8 -> FAMILY: (m, q, bar, seed) = (8, 0.1, 0.011111, 20260924) != (9, 0.1, 0.011111, 20260924) · a tampered REGISTRATIONS.json in a temp root (P-TP-RNG ruler -> two-sample) -> HALT: HALT (REGISTRY): REGISTRATIONS.json does not … PAYLOAD-SHA: P-TP-RNG payload hashes to a3f2bf34f773ab50… != filed ad12a44cd8aeb27c…
- [PASS] F-RULER: the nine rulers/eras == the typed L-1.4 table; on EACH of the 4 paired registrations (P-ADD-BRK, P-ADD-SFP, P-TP-RNG registered; P-WARN-1's Tier-E rule book) one key moved, one row dropped, an unacted row off the base and acted_by dropped each HALT (paired premise / identity law, no number, no slot); two-sample on identical keys FLAGGED on all 3 (P-AGE-1, P-WIN-1, P-RELAY-1), the planted rows not; P-BRK-4H vs zero identical with and without its garbage base; the 3 BUILT paired rows n == n_base == 200, point == this file's delta mean, unacted count == this file's (P-TP-RNG 50); both gates HALT on a new campaign and on a kept row moved; SC-3: P-ADD-SFP/tierE__holdout_slice (paired) and P-WIN-1/tierE__holdout_shadow (two-sample) ruled vs the base's 77 holdout rows, point == this file's
  - [BREAK] RED (correct): all 10 plants caught by their named detector, one at a time: the paired premise check disabled -> PAIRED-PREMISE-NOT-ENFORCED: P-ADD-BRK one key moved -> NOT SUPPORTED (NOT SUPPORTED · SCALE-IN-SAMPLE (holdout slice, derived: n 77, +0.0670 [+0.0009,) · the identity law disabled (SC-15) -> IDENTITY-LAW-NOT-ENFORCED: P-ADD-BRK an unacted row off the base by +0.25 R -> NOT SUPPORTED halts [] · the two-sample ruler read as paired -> RULER-TABLE: P-AGE-1 reads (paired, full) != typed (two_sample, full) · the vs-zero ruler read as two-sample -> RULER-TABLE: P-BRK-4H reads (two_sample, full) != typed (vs_zero, full) · the identical-key two-sample flag suppressed (SC-6) -> TWO-SAMPLE-FLAG-MISSING: P-AGE-1 identical key sets -> NOT SUPPORTED — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (pre_seen: the scored cohort IS TC10  · the vs-zero row reading its base -> VS-ZERO-IGNORES-BASE: the vs-zero row moved when its base arm was removed (SUPPORTED vs HALT) · the pairing key taken WITH lane -> PAIRED-ROW: P-ADD-BRK n 0 / base 200 point None vs this file's 0.06849999999999998 · the gate post-filter check disabled (SC-16) -> GATE-POSTFILTER-NOT-ENFORCED: P-AGE-1 a campaign the base never held -> NOT SUPPORTED — CI wholly below zero · a Tier-E base not restricted to the arm's era_scope (SC-3) -> SC-3: P-ADD-SFP/tierE__holdout_slice (paired, holdout) n_base None point None halted PAIRED-PREMISE: paired premise failed — n scored 77 vs n bas != this file's base hold · corrupted input: P-TP-RNG with one entry_ms moved, handed to the scorer -> PAIRED-PREMISE: paired premise failed — n scored 200 vs n base 200; 1 key(s) only in scored [('BTCUSDT', 1580068800000)], 1 only in base [('BTCUSDT', 1580083200000)]
- [PASS] F-BOOT: 4 planted books x (seed 20260924, sens 20260816, haircut) at B 499: point, CI, p = (#<=0+1)/(B+1), deciding bound (rank floor((B+1)/90) = 5) == this file's hand computation EXACTLY; the rows of record at B 4000 == hand exactly (P-ADD-BRK p 86/4001, deciding rank 44); LOAO per-panel == TP.loao_n at 6 dp on 4 books
  - [BREAK] RED (correct): all 4 plants caught by their named detector, one at a time: the p law bent to #draws<0 / B -> BOOT-P[P-ADD-BRK/paired/main/B499] p_one_sided: scorer 0.02004008016032064 != hand 0.022 · the CI bent to the 2.5th..97.5th percentile -> BOOT-CI[P-ADD-BRK/paired/main/B499] lo: scorer 0.0006315789473684263 != hand 0.005082762296330144 · the seed of record bent to 20260921 -> BOOT-CI[P-ADD-BRK/paired/main/B499] lo: scorer 0.004696969696969707 != hand 0.005082762296330144 · the draw unit bent from assets to rows -> BOOT-CI[P-ADD-BRK/paired/main/B499] lo: scorer 0.061 != hand 0.005082762296330144
- [PASS] F-VERDICT: 11 typed cases read as typed (lo>0 & p 0.03 -> NOT SUPPORTED; 44/4001 -> SUPPORTED; 45/4001 -> NOT); planted P-ADD-BRK lo +0.0051 > 0, p 86/4001 > 1/90 -> NOT SUPPORTED; P-ADD-SFP SUPPORTED; P-TP-RNG '— CI wholly below zero'; labels pre_seen / selection_hazard x2 / SCALE-IN-SAMPLE x4 / forfeits on P-AGE-1 only; AM-3 ΣΔ / Σ add_r / absorbed funding on both add rows == this file's sums exactly; P-SCALP-2 and P-WARN-1 print no number, 'no slot spent'; FAMILY m 9, bar 0.011111 (1/90), 7 tests spent; SCALE-IN-SAMPLE x4: the holdout slice n / point == this file's era=='holdout' (by close) ruling, the frozen twin == typed (3 filed, P-TP-RNG ABSENT) with n / point == this file's, pick stability flags exactly the typed changes (1h BTC SOL NEAR; 4h NEAR; 12h BTC ETH SOL) on the §0 cell and every consuming Tier-E row, frozen rows say so, the in-sample holdout count == this file's, the 17-asset view labelled IN-SAMPLE for HYPE / PUMP 4h; the sensitivity-seed verdict ruled on its own draws on 3 rulers
  - [BREAK] RED (correct): all 11 plants caught by their named detector, one at a time: the SCALE 'holdout slice' computed on the tuning era -> SCALE-CONTENT: P-BRK-4H holdout slice printed n 70 point 0.2859482960021747 != this file's era=='holdout' (by close) n 51 point 0.5118605321345906 · the frozen-3.0 twin dropped from the SCALE cell -> SCALE-CONTENT: P-BRK-4H frozen-3.0 twin None != typed 'tierE__frozen_3_0_twin' · the pick-stability flag dropped (L-R.2) -> SCALE-STABILITY: P-BRK-4H (4h) flags [] / clause 'pick stability (4h): printed)' != exactly typed ['NEARUSDT'] · P-TP-RNG's consumed lens read as 4h -> SCALE-STABILITY: P-TP-RNG (12h) flags ['NEARUSDT'] / clause 'pick stability (4h, first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on NEARUSDT 2.0->1.75 (40 of 2 · the whole-tape fallback IN-SAMPLE label dropped -> SCALE-FALLBACK: P-BRK-4H/tierE__17_asset_view flags 'pick stability 4h: CHANGED on NEARUSDT (10 of 170 campaigns)' lack 'IN-SAMPLE everywhere (whole-tape pick fallback [L · the sensitivity seed collapsed onto the seed of record -> SENS-VERDICT: P-ADD-SFP (draws +1 at 20260924, -1 at 20260816) reads 'SUPPORTED' / sens 'SUPPORTED' / stable True · a CI-only verdict (clause (b) dropped) -> VERDICT-CASE: (lo 0.05, hi 0.3, p 0.03) reads 'SUPPORTED' != typed 'NOT SUPPORTED' · the bar loosened to 0.10/7 (tests actually run) -> VERDICT-CASE: (lo 0.05, hi 0.3, p 45/4001) reads 'SUPPORTED' != typed 'NOT SUPPORTED' · a closed row printing a number -> CLOSED-NUMBER: P-SCALP-2 prints ['0', '+0.0000', '[+0.0000, +0.0000]', '1.000000', '0/5 above', '+0.0000'] / spent False · the honesty label dropped -> LABEL: P-AGE-1 lacks '— IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (pre_seen: the scored' · the AM-3 beside-print dropped -> ADDS: P-ADD-BRK beside-print (None, None, None) != this file's (ΣΔ, Σ add_r, absorbed) (13.699999999999996, 13.660000000000002, 0.040000000000000015)
- [PASS] F-STATUS: CLOSED_BY_PRECONDITION on each of the 8 registrations without a precondition and CONDITION_NOT_MET on each of the 8 without a condition HALT STATUS-ILLEGAL (16/16); P-WARN-1 HALTs CONDITION-RECORD on BUILT vs met False, NOT MET vs met True, met False with ci_hi < 0 and an absent record (4/4), and the planted NOT MET row agrees with its record; P-SCALP-2 HALTs PRECONDITION-RECORD on BUILT vs R2 1h FAIL, CLOSED vs PASS and no readable record (3/3); its closed cell prints the tuning-era R2 1h word FAIL beside, collared [§10]
  - [BREAK] RED (correct): all 4 plants caught by their named detector, one at a time: the STATUS-ILLEGAL guard removed -> STATUS-NOT-ENFORCED: P-WARN-1 CLOSED_BY_PRECONDITION -> CLOSED_BY_PRECONDITION [] · the condition record not cross-checked -> CONDITION-NOT-ENFORCED: P-WARN-1 BUILT while the record says NOT MET -> NOT SUPPORTED — CI wholly below zero [] · the R2 precondition record not cross-checked -> PRECONDITION-NOT-ENFORCED: P-SCALP-2 BUILT while the R2 1h word is FAIL -> HALT ['ARM-ABSENT: P-SCALP-2 is BUILT but STATUS lists no scored arm'] · the tuning-era R2 word not printed beside P-SCALP-2 -> R2-TUNING-WORD: P-SCALP-2 cell "CLOSED BY PRECONDITION: CLOSED BY R2 (1h: FAIL) — PLANTED (the R2 record's own 1h word) — report-only · no number · no slot spent" lacks '
- [PASS] F-COLLAR: 27 Tier-E rows == the 27 declared; every one collared exactly, no verdict word or verdict field, would_read_ci_only == the reading of its own interval ({'CI above zero (lo > 0)': 15, 'CI includes zero': 6, 'CI wholly below zero (hi < 0)': 6}); the S0_VERDICTS.md Tier-E table carries the collar on every line; the scorer's guard agrees
  - [BREAK] RED (correct): all 8 plants caught by their named detector, one at a time: a verdict word in a Tier-E note (this file's law) -> F-COLLAR: P-AGE-1/tierE__shadow_absolute.note carries a verdict word 'reads SUPPORTED on the CI alone' · a verdict word in a Tier-E note (the scorer's guard) -> COLLAR-VERDICT-WORD: P-AGE-1/tierE__shadow_absolute.note = 'reads SUPPORTED on the CI alone' · the gates column dropped (this file) -> F-COLLAR: P-AGE-1/tierE__shadow_absolute gates None != 'nothing' · the gates column dropped (the scorer's guard) -> COLLAR-MISSING: P-AGE-1/tierE__shadow_absolute lacks gates · gates re-worded (the scorer's guard) -> COLLAR-VALUE: P-AGE-1/tierE__shadow_absolute gates 'NOTHING — Tier-E' != 'nothing' · would_read_ci_only = a verdict (this file) -> F-COLLAR: P-AGE-1/tierE__shadow_absolute would_read_ci_only 'SUPPORTED (CI-only)' != the reading of its own interval · the module's Tier-E row builder dropping the collar -> COLLAR-MISSING: P-BRK-4H/tierE__frozen_3_0_twin lacks selection_not_a_result · a Tier-E sidecar without its collar (input) -> SIDECAR-COLLAR: P-WIN-1/tierE__shadow_cut gates None != 'nothing'
- [PASS] F-BASE-IDENT: the 7 base arms carry ONE book_sha256 3295673b21eb21d1… and equal books/v6_campaigns.parquet on the 13 typed columns at 6 dp (this file's own join, n 200); BASE_IDENT.json agrees; each of the 7 bases bent in turn halts ITS row only (a clean neighbour is ruled); SC-13: the scorer's canonical CSV == pandas to_csv on all 27 planted arms
  - [BREAK] RED (correct): all 5 plants caught by their named detector, one at a time: one base net_r +1e-6 (P-TP-RNG) -> BASE-IDENT: the base arms carry 2 different book_sha256: 3295673b21eb21d1… ['P-ADD-BRK', 'P-ADD-SFP', 'P-AGE-1', 'P-RELAY-1', 'P-WARN-1', 'P-WIN-1']; 15f87263aa5d93f0… [' · one base row dropped (P-RELAY-1) -> BASE-V6: P-RELAY-1/base keys != books/v6 (n 199 vs 200; only in base [], only in v6 [('BTCUSDT', 1625140800000)]) · every base's first exit_close_ms moved -3h (1h-resolved style) -> BASE-V6: P-ADD-BRK/base exit_close_ms differs from books/v6 exit_close_ms on 1 row(s), e.g. BTCUSDT 1580083200000: 1580619600000 vs 1580630400000 · a base sidecar claiming a wrong book_sha256 -> BOOK-SHA: P-WIN-1/base sidecar claims 0000000000000000… but the parquet hashes to 3295673b21eb21d1… · a registration whose base differs: its row must HALT -> F-BASE-IDENT halts the bent row on 7/7: ['P-AGE-1', 'P-WIN-1', 'P-WARN-1', 'P-ADD-BRK', 'P-ADD-SFP', 'P-TP-RNG', 'P-RELAY-1']
- [PASS] F-GRID: 10 grids WHOLE by TP.grid_whole against typed declared cells: §0 9/9, FAMILY 9/9, Tier-E 27/27, 7 LOAO grids x 5 panels
  - [BREAK] RED (correct): all 4 plants caught by their named detector, one at a time: a §0 row dropped -> GRID: §0 table: [BAD] §0 table: declared 9 cells, written 8; missing ['P-WARN-1'], undeclared none, duplicated none · a FAMILY row duplicated -> GRID: FAMILY: [BAD] FAMILY: declared 9 cells, written 10; missing none, undeclared none, duplicated ['P-WARN-1'] · an undeclared Tier-E row -> GRID: Tier-E table: [BAD] Tier-E table: declared 27 cells, written 28; missing none, undeclared ['P-X|tierE__x'], duplicated none · a LOAO panel dropped -> GRID: LOAO P-AGE-1: [BAD] LOAO P-AGE-1: declared 5 cells, written 4; missing ['ZECUSDT'], undeclared none, duplicated none
- [PASS] F-KEY: all 27 planted arms pass the interface (16 columns, exact dtypes, no nulls, no ',' '"' CR LF in strings, unique keys, direction +-1, era by close — the planted 2024-06-30T20:00Z straddle reads 'holdout' and is counted 1 in P-BRK-4H/scored —, 0 < entry_close - entry_ms <= 4h, AM-7 haircut law, sidecar n/sum/sha/era_scope/collar); score rows keyed uniquely (9 registrations, 27 Tier-E), required fields non-null
  - [BREAK] RED (correct): all 18 plants caught by their named detector, one at a time: the era judged by the entry bar's OPEN (L-1.3 broken) -> REGBOOK-ERA: P-BRK-4H/scored 1 row(s) whose era != E.era_of(entry_close_ms) [L-1.3: era by the entry bar's CLOSE] · a sidecar sum_net_r off by 1e-3 -> SIDECAR: P-ADD-SFP/scored sum_net_r 100.508566 != np.float64(100.507566) at 1e-6 · a sidecar era_scope 'holdout' on a full-corridor book -> SIDECAR: P-ADD-SFP/scored era_scope holdout but 123 row(s) carry another era · an entry bar longer than the 4h lens -> REGBOOK-TIME: P-ADD-SFP/scored 1 row(s) with entry_close_ms - entry_ms outside (0, 4h] — entry_ms is the open of the lens bar holding the entry close [SC-19] · an exit before the entry close -> REGBOOK-TIME: P-ADD-SFP/scored 1 row(s) with exit_close_ms < entry_close_ms · r_dist 0 -> REGBOOK-RDIST: P-ADD-SFP/scored r_dist <= 0 on some row · a ',' inside a lane string -> REGBOOK-STR: P-ADD-SFP/scored string field(s) holding ',', '"', CR or LF {'lane': 1} — the canonical CSV (SC-13) does no quoting [SC-19] · direction as int64 -> REGBOOK-DTYPE: P-ADD-SFP/scored direction is int64, not int8 [SC-19] · exit_close_ms as int32 -> REGBOOK-DTYPE: P-ADD-SFP/scored exit_close_ms is int32, not int64 [SC-19] · a duplicated (symbol, entry_close_ms) key -> REGBOOK-KEY: P-ADD-SFP/scored 1 duplicated (symbol, entry_close_ms) key(s) · a null net_r -> REGBOOK-NULL: P-ADD-SFP/scored nulls in required columns {'net_r': 1} · the lane column dropped -> REGBOOK-COLS: P-ADD-SFP/scored lacks required column(s) ['lane'] · one row's era flipped -> REGBOOK-ERA: P-ADD-SFP/scored 1 row(s) whose era != E.era_of(entry_close_ms) [L-1.3: era by the entry bar's CLOSE] · a direction 0 -> REGBOOK-DIR: P-ADD-SFP/scored direction values [0] outside {+1, -1} · the haircut law broken by 1e-6 on one row -> REGBOOK-HAIRCUT: P-ADD-SFP/scored 1 row(s) break the AM-7 law haircut_net_r = net_r - fee_r*slip/taker (worst 1.000e-06) · net_r as float32 -> REGBOOK-DTYPE: P-ADD-SFP/scored net_r is float32, not float64 · a sidecar n one too many -> SIDECAR: P-ADD-SFP/scored n 201 != 200 rows · a stray asset outside the declared panel -> STRAY-ASSET: P-ADD-SFP/scored holds ['DOGEUSDT'] outside its declared panel
- [PASS] F-CLOSURE: fresh interpreter: 747 modules loaded, none range / census / stamps / null / nest (none); static scan + E.hook_escapes on the source: clean
  - [BREAK] RED (correct): all 3 plants caught by their named detector, one at a time: a top-level census import -> STATIC: tierc10_census · a lazy in-function nest import -> STATIC: tierc11_nest · a subprocess import (an I/O escape) -> HOOK-ESCAPE line 2514: import subprocess
- [PASS] F-DRYRUN: the dry run completes with every ruler tripwired (ruled, stats_block, loao), exit 0 ('EXIT 0 = 0 (no condition)'); 9 registration lines in the typed order, every arm line labelled (book, not a verdict); no interval, p, LOAO or verdict token; the P-ADD-SFP scored n / ΣR == this file's
  - [BREAK] RED (correct): all 6 plants caught by their named detector, one at a time: the dry run's facts calling a ruler -> DRYRUN-RULED: TRIPWIRE: a ruler was called · the dry run printing an interval -> DRYRUN-OUTCOME: '\\bCI\\b' found ('R +0.198288 · tuning 123 / holdout 77 · CI [+0.1000, +0.2000] ') · corrupted input: a paired key moved (the dry run must HALT the row) ->     HALT: PAIRED-PREMISE: paired premise failed — n scored 200 vs n base 200; 1 key(s) only in scored [('BTCUSDT', 1585771200000)], 1 only in base [('BTCUSDT', 1585756800 · corrupted input: an unacted P-TP-RNG campaign moved off v6 (identity law) ->     HALT: IDENTITY-LAW: P-TP-RNG/scored unacted rows differ from the base net_r on 1 row(s) (e.g. BTCUSDT 1580083200000) [L-1.5: exact, 0.000e+00] · corrupted input: a kept P-WIN-1 gate row changed (post-filter) ->     HALT: GATE-POSTFILTER: P-WIN-1/scored kept rows differ from the base on {'net_r': 1, 'gross_r': 92, 'haircut_net_r': 1} — a gate keeps each admitted campaign unchange · corrupted input: P-WARN-1's condition record flipped to MET under NOT MET ->     HALT: CONDITION-RECORD: P-WARN-1 STATUS CONDITION_NOT_MET but the condition record says MET
- [PASS] F-EXIT: all 16 subsets of (registered HALT 2, Tier-E halted 4, ABSENT 8, no-clobber 16) exit the OR of their typed bits with an EXIT line naming each; the dry run on a family with all three row conditions exits 14 and names all three
  - [BREAK] RED (correct): all 3 plants caught by their named detector, one at a time: the masking precedence law (2 hides 5, 3 hides 5, 4 only when 0) -> EXIT-FLAGS: {'halt': False, 'tier_e': True, 'absent': False, 'noclobber': False} -> exit 3 / 'EXIT 4 = 4 (a Tier-E row halted)' != typed 4 / 'EXIT 4 = 4 (a Tier-E row hal · a registered HALT dropped from the exit word -> EXIT-FLAGS: {'halt': True, 'tier_e': False, 'absent': False, 'noclobber': False} -> exit 0 / 'EXIT 0 = 0 (no condition)' != typed 2 / 'EXIT 2 = 2 (a registered row HALTed · the flag bits permuted (Tier-E 8, ABSENT 4) -> EXIT-FLAGS: {'halt': False, 'tier_e': True, 'absent': False, 'noclobber': False} -> exit 8 / 'EXIT 8 = 8 (a Tier-E row halted)' != typed 4 / 'EXIT 4 = 4 (a Tier-E row hal
- [PASS] F-DET: exit 0/0; file set == typed 6 files; every file byte-identical seed 1 == seed 20260924 == this process's render (BASE_IDENT.json 40feb06e52fd…, FAMILY.json f786269d33c8…, REGISTRY_CHECK.json 601c9195bdc8…, S0_VERDICTS.md ff969ed6931c…, SCORES.json 755bb8164dd4…, SCORE_MANIFEST.json 7d78bad70677…)
  - [BREAK] RED (correct): all 3 plants caught by their named detector, one at a time: one byte bent in a copy of S0_VERDICTS.md -> seed 1 vs seed 20260924: S0_VERDICTS.md bytes differ at byte 35633 · a process-dependent salt in FAMILY.json -> seed 1 vs seed 20260924: FAMILY.json bytes differ at byte 259 · a hash-order-dependent line (set iteration) under the two seeds -> seed 1 vs seed 20260924: S0_VERDICTS.md bytes differ at byte 71218

## The planted run (PLANTED — synthetic regbooks; NOT A RESULT of any registration)

Every scored and Tier-E arm below is a SYNTHETIC transform of books/v6 (a typed delta or index filter) or a seeded synthetic lane, written by the fixture file. The words in the verdict column are the scorer's law exercised on synthetic data. They say nothing about any registration. The pick-stability flags and fallback labels are real, because they are read from the filed SCALE_PICKS.json record.

### §0 table (planted)

| # · registration · prior · scored arm · panel · era · ruler | n | point | 90% CI | verdict under its own text (with labels) | p · clears bar | LOAO | haircut twin | D15 |
|---|---|---|---|---|---|---|---|---|
| 1 · P-WARN-1 · 40% · scored (CONDITIONAL exit rule) · CLASSIC5 · full · paired | — | — | — | CONDITION NOT MET: PLANTED: condition cohort delta cluster-90% hi >= 0 — report-only · no number · no slot spent | — | — | — | — |
| 2 · P-AGE-1 · 50% · scored (admission gate (post-filter)) · CLASSIC5 · full · two_sample | 187 (base 200); refused n 13, mean +2.6807, ΣR +34.8490; ΣR scored +5.9586 vs base +40.8076 | -0.1722 | [-0.2640, -0.0860] | NOT SUPPORTED — CI wholly below zero — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (pre_seen: the scored cohort IS TC10 P_AGE_1_TIDE_YOUTH B4 (same function, same trailing edges, same 200 campaigns, anchored by F-CTRL(b))); on per-campaign expectancy only; the gate forfeits +34.8490 R total | 1.000000 · clears bar: no | 0/5 above, 5/5 BELOW (bar 3/5; short) · sens 0/5 above, 5/5 BELOW | -0.1724 [-0.2640, -0.0860] p 1.000000 | tail 0.9157 · paired n 187 · max Δ share None |
| 3 · P-WIN-1 · 50% · scored (admission gate (post-filter)) · CLASSIC5 · full · two_sample | 175 (base 200); refused n 25, mean -0.8918, ΣR -22.2945; ΣR scored +63.1021 vs base +40.8076 | +0.1565 | [+0.1335, +0.1813] | SUPPORTED — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (selection_hazard: direction informed by TC6V L-LAG deciles on the same corridor (lag-0 +0.4149, 56-bar decile -0.5796)) | 0.000250 · clears bar: yes | 5/5 above (bar 3/5; clears) · sens 5/5 above | +0.1571 [+0.1343, +0.1816] p 0.000250 | tail 1.0891 · paired n 175 · max Δ share None |
| 4 · P-BRK-4H · 45% · scored (lane) · CLASSIC5 · full · vs_zero | 121 | +0.3812 | [+0.3033, +0.4708] | SUPPORTED — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (selection_hazard: the best of 7,920 TC10 census cells (4h retest-hold-tap89, CLASSIC5 NET H20 +0.681 ALL n 236 / +0.706 holdout n 88; UNSEEN12 +0.064 / +0.272)) · SCALE-IN-SAMPLE (holdout slice, derived: n 51, +0.5119 [+0.4740, +0.5483] p 0.000250; 1 of 51 of its campaigns carry a range read <= the era cut (in-sample; die_close_ms<=cut); filed tierE__holdout_slice: n 51, +0.5119 [+0.4740, +0.5483] p 0.000250; frozen-3.0 twin tierE__frozen_3_0_twin: n 120, +0.1329 [+0.0348, +0.2883] p 0.000250; pick stability (4h, first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on NEARUSDT 2.0->1.75 (24 of 121 campaigns on a changed asset)) | 0.000250 · clears bar: yes | 5/5 above (bar 3/5; clears) · sens 5/5 above | +0.3642 [+0.2864, +0.4503] p 0.000250 | — (vs zero: no base) |
| 5 · P-RELAY-1 · 45% · scored (trigger lane) · CLASSIC5 · full · two_sample | 100 (base 200) | -0.0011 | [-0.1044, +0.0955] | NOT SUPPORTED | 0.513122 · clears bar: no | 0/5 above (bar 3/5; short) · sens 0/5 above | -0.0019 [-0.1058, +0.0949] p 0.516621 | tail 0.9081 · paired n 100 · max Δ share 4.2156 |
| 6 · P-SCALP-2 · 30% · scored (lane (range trade)) · CLASSIC5 · holdout · vs_zero | — | — | — | CLOSED BY PRECONDITION: CLOSED BY R2 (1h: FAIL) — PLANTED (the R2 record's own 1h word) — report-only · no number · no slot spent · beside, Tier-E [§10] (tier TIER-E · a SELECTION, not a result · gates nothing): the tuning-era R2 1h word FAIL (holdout word of record FAIL) | — | — | — | — |
| 7 · P-ADD-BRK · 40% · scored (add rule) · CLASSIC5 · full · paired | 200 (base 200); ΣΔ +13.7000, Σ add_r +13.6600, absorbed funding +0.0400 (AM-3) | +0.0685 | [+0.0051, +0.1000] | NOT SUPPORTED · SCALE-IN-SAMPLE (holdout slice, derived: n 77, +0.0670 [+0.0057, +0.1004] p 0.032492; in-sample range reads in the holdout slice: not determinable from the regbook; frozen-3.0 twin tierE__frozen_3_0_twin: n 200, +0.0500 [+0.0500, +0.0500] p 0.000250; pick stability (1h, first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on BTCUSDT 2.0->1.75, SOLUSDT 2.0->1.75, NEARUSDT 2.0->1.75 (115 of 200 campaigns on a changed asset)) | 0.021495 · clears bar: no | 1/5 above (bar 3/5; short) · sens 1/5 above | +0.0685 [+0.0051, +0.1000] p 0.021495 | tail 1.0089 · paired n 200 · max Δ share 0.008 |
| 8 · P-ADD-SFP · 40% · scored (add rule) · CLASSIC5 · full · paired | 200 (base 200); ΣΔ +59.7000, Σ add_r +59.6600, absorbed funding +0.0400 (AM-3) | +0.2985 | [+0.2956, +0.3010] | SUPPORTED · SCALE-IN-SAMPLE (holdout slice, derived: n 77, +0.3006 [+0.2980, +0.3035] p 0.000250; in-sample range reads in the holdout slice: not determinable from the regbook; filed tierE__holdout_slice: n 77, +0.3006 [+0.2980, +0.3035] p 0.000250; frozen-3.0 twin tierE__frozen_3_0_twin: n 200, +0.1000 [+0.1000, +0.1000] p 0.000250; pick stability (1h, first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on BTCUSDT 2.0->1.75, SOLUSDT 2.0->1.75, NEARUSDT 2.0->1.75 (115 of 200 campaigns on a changed asset)) | 0.000250 · clears bar: yes | 5/5 above (bar 3/5; clears) · sens 5/5 above | +0.2985 [+0.2956, +0.3010] p 0.000250 | tail 1.0524 · paired n 200 · max Δ share 0.0075 |
| 9 · P-TP-RNG · 35% · scored (exit rule) · CLASSIC5 · full · paired | 200 (base 200) | -0.1500 | [-0.1504, -0.1495] | NOT SUPPORTED — CI wholly below zero · SCALE-IN-SAMPLE (holdout slice, derived: n 77, -0.1538 [-0.1569, -0.1506] p 1.000000; in-sample range reads in the holdout slice: not determinable from the regbook; frozen-3.0 twin: ABSENT — no tierE__*frozen* arm filed; pick stability (12h, first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on BTCUSDT 1.75->2.0, ETHUSDT 2.0->1.5, SOLUSDT 1.75->2.25 (123 of 200 campaigns on a changed asset)) | 1.000000 · clears bar: no | 0/5 above, 5/5 BELOW (bar 3/5; short) · sens 0/5 above, 5/5 BELOW | -0.1500 [-0.1504, -0.1495] p 1.000000 | tail 0.9728 · paired n 200 · max Δ share 0.008 · named risk: the wall-exit lesson: P-WALL-1 (TC6) delta -0.0331, tail ratio 0.9329 — loses by cutting the tail |

### Family (planted)

m = 9 · q = 0.1 · bar = 0.10/9 = 0.011111 (exact 1/90) · tests spent 7 · SUPPORTED: P-WIN-1, P-BRK-4H, P-ADD-SFP

| # | registration | status | verdict_of_record | spent a test | p | clears bar |
|---|---|---|---|---|---|---|
| 1 | P-WARN-1 | CONDITION_NOT_MET | CONDITION_NOT_MET | no | — | — |
| 2 | P-AGE-1 | BUILT | NOT SUPPORTED — CI wholly below zero | yes | 1.000000 | no |
| 3 | P-WIN-1 | BUILT | SUPPORTED | yes | 0.000250 | yes |
| 4 | P-BRK-4H | BUILT | SUPPORTED | yes | 0.000250 | yes |
| 5 | P-RELAY-1 | BUILT | NOT SUPPORTED | yes | 0.513122 | no |
| 6 | P-SCALP-2 | CLOSED_BY_PRECONDITION | CLOSED_BY_PRECONDITION | no | — | — |
| 7 | P-ADD-BRK | BUILT | NOT SUPPORTED | yes | 0.021495 | no |
| 8 | P-ADD-SFP | BUILT | SUPPORTED | yes | 0.000250 | yes |
| 9 | P-TP-RNG | BUILT | NOT SUPPORTED — CI wholly below zero | yes | 1.000000 | no |

Law: m = 9 in every case; bar = 0.10/9 fixed, no ranks, no step-up; a registration closed by its own precondition or condition spends no test and never loosens the bar; a HALTed or ABSENT row spends no test [L-1.4]

### Tier-E rows (planted) — a SELECTION, not a result · gates nothing · no verdict word

27 rows, every one collared (tier / selection_not_a_result / gates); would_read_ci_only is the CI-only reading.

| registration | arm | ruler | era_scope | panel | n | point | 90% CI | p | would_read_ci_only | LOAO | haircut twin | scale (L-R.2) | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P-WARN-1 | scored | paired | full | CLASSIC5 | 200 (base 200) | -0.0058 | [-0.0061, -0.0054] | 1.000000 | CI wholly below zero (hi < 0) | 0/5 above, 5/5 BELOW (bar 3) | -0.0058 [-0.0061, -0.0054] | — | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | derived__slice_tuning | two_sample | tuning | CLASSIC5 | 115 (base 123) | -0.1386 | [-0.1876, -0.0852] | 1.000000 | CI wholly below zero (hi < 0) | 0/5 above, 5/5 BELOW (bar 3) | -0.1389 [-0.1880, -0.0860] | — | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | derived__slice_holdout | two_sample | holdout | CLASSIC5 | 72 (base 77) | -0.2259 | [-0.3901, -0.0592] | 1.000000 | CI wholly below zero (hi < 0) | 0/5 above, 2/5 BELOW (bar 3) | -0.2260 [-0.3906, -0.0591] | — | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | tierE__shadow_absolute | two_sample | full | CLASSIC5 | 171 (base 200) | +0.0409 | [-0.0476, +0.1231] | 0.231692 | CI includes zero | 1/5 above (bar 3) | +0.0408 [-0.0473, +0.1232] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | derived__slice_tuning | two_sample | tuning | CLASSIC5 | 109 (base 123) | +0.1117 | [+0.0847, +0.1306] | 0.000250 | CI above zero (lo > 0) | 5/5 above (bar 3) | +0.1120 [+0.0850, +0.1310] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | derived__slice_holdout | two_sample | holdout | CLASSIC5 | 66 (base 77) | +0.2422 | [+0.1551, +0.3999] | 0.000250 | CI above zero (lo > 0) | 5/5 above (bar 3) | +0.2431 [+0.1557, +0.4004] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__holdout_shadow | two_sample | holdout | CLASSIC5 | 70 (base 77) | -0.2912 | [-0.9373, +0.0742] | 0.666083 | CI includes zero | 1/5 above (bar 3) | -0.2908 [-0.9362, +0.0744] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__shadow_cut | two_sample | full | CLASSIC5 | 181 (base 200) | -0.1157 | [-0.3428, +0.0412] | 0.829793 | CI includes zero | 0/5 above (bar 3) | -0.1156 [-0.3423, +0.0415] | — | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | derived__slice_tuning | vs_zero | tuning | CLASSIC5 | 70 | +0.2859 | [+0.1311, +0.4530] | 0.000250 | CI above zero (lo > 0) | 5/5 above (bar 3) | +0.2689 [+0.1202, +0.4326] | pick stability 4h: CHANGED on NEARUSDT (14 of 70 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | derived__slice_holdout | vs_zero | holdout | CLASSIC5 | 51 | +0.5119 | [+0.4740, +0.5483] | 0.000250 | CI above zero (lo > 0) | 5/5 above (bar 3) | +0.4950 [+0.4536, +0.5352] | pick stability 4h: CHANGED on NEARUSDT (10 of 51 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__17_asset_view | vs_zero | full | PANEL17 | 170 | +0.1876 | [+0.0261, +0.3336] | 0.030742 | CI above zero (lo > 0) | 15/17 above (bar 9) | +0.1507 [-0.0108, +0.2963] | pick stability 4h: CHANGED on NEARUSDT (10 of 170 campaigns) · IN-SAMPLE everywhere (whole-tape pick fallback [L-R.2]): HYPEUSDT 4h, PUMPUSDT 4h (20 of 170 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__frozen_3_0_twin | vs_zero | full | CLASSIC5 | 120 | +0.1329 | [+0.0348, +0.2883] | 0.000250 | CI above zero (lo > 0) | 5/5 above (bar 3) | +0.1158 [+0.0192, +0.2657] | frozen 3.0: no calibrated pick consumed | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__holdout_slice | vs_zero | holdout | CLASSIC5 | 51 | +0.5119 | [+0.4740, +0.5483] | 0.000250 | CI above zero (lo > 0) | 5/5 above (bar 3) | +0.4950 [+0.4536, +0.5352] | pick stability 4h: CHANGED on NEARUSDT (10 of 51 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-RELAY-1 | derived__slice_tuning | two_sample | tuning | CLASSIC5 | 60 (base 123) | -0.0764 | [-0.3097, +0.1822] | 0.688328 | CI includes zero | 0/5 above, 1/5 BELOW (bar 3) | -0.0766 [-0.3113, +0.1819] | — | TIER-E | a SELECTION, not a result | nothing |
| P-RELAY-1 | derived__slice_holdout | two_sample | holdout | CLASSIC5 | 40 (base 77) | +0.0909 | [-0.4307, +0.5553] | 0.383154 | CI includes zero | 0/5 above (bar 3) | +0.0892 [-0.4322, +0.5528] | — | TIER-E | a SELECTION, not a result | nothing |
| P-RELAY-1 | tierE__late_relay_twin | two_sample | full | CLASSIC5 | 100 (base 200) | +0.0195 | [-0.1626, +0.1847] | 0.366408 | CI includes zero | 0/5 above (bar 3) | +0.0203 [-0.1625, +0.1855] | — | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | derived__slice_tuning | paired | tuning | CLASSIC5 | 123 (base 123) | +0.0694 | [+0.0071, +0.0999] | 0.018245 | CI above zero (lo > 0) | 1/5 above (bar 3) | +0.0694 [+0.0071, +0.0999] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (72 of 123 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | derived__slice_holdout | paired | holdout | CLASSIC5 | 77 (base 77) | +0.0670 | [+0.0057, +0.1004] | 0.032492 | CI above zero (lo > 0) | 1/5 above (bar 3) | +0.0670 [+0.0057, +0.1004] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (43 of 77 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__frozen_3_0_twin | paired | full | CLASSIC5 | 200 (base 200) | +0.0500 | [+0.0500, +0.0500] | 0.000250 | CI above zero (lo > 0) | 5/5 above (bar 3) | +0.0500 [+0.0500, +0.0500] | frozen 3.0: no calibrated pick consumed | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__head_to_head_vs_p_add_sfp | paired | full | CLASSIC5 | 200 (base 200) | -0.2300 | [-0.2930, -0.1966] | 1.000000 | CI wholly below zero (hi < 0) | 0/5 above, 5/5 BELOW (bar 3) | -0.2300 [-0.2930, -0.1966] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (115 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | derived__slice_tuning | paired | tuning | CLASSIC5 | 123 (base 123) | +0.2972 | [+0.2936, +0.3004] | 0.000250 | CI above zero (lo > 0) | 5/5 above (bar 3) | +0.2972 [+0.2936, +0.3004] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (72 of 123 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | derived__slice_holdout | paired | holdout | CLASSIC5 | 77 (base 77) | +0.3006 | [+0.2980, +0.3035] | 0.000250 | CI above zero (lo > 0) | 5/5 above (bar 3) | +0.3006 [+0.2980, +0.3035] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (43 of 77 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__frozen_3_0_twin | paired | full | CLASSIC5 | 200 (base 200) | +0.1000 | [+0.1000, +0.1000] | 0.000250 | CI above zero (lo > 0) | 5/5 above (bar 3) | +0.1000 [+0.1000, +0.1000] | frozen 3.0: no calibrated pick consumed | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__holdout_slice | paired | holdout | CLASSIC5 | 77 (base 77) | +0.3006 | [+0.2980, +0.3035] | 0.000250 | CI above zero (lo > 0) | 5/5 above (bar 3) | +0.3006 [+0.2980, +0.3035] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (43 of 77 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | derived__head_to_head_vs_p_add_brk | paired | full | CLASSIC5 | 200 (base 200) | +0.2300 | [+0.1966, +0.2930] | 0.000250 | CI above zero (lo > 0) | 5/5 above (bar 3) | +0.2300 [+0.1966, +0.2930] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (115 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | derived__slice_tuning | paired | tuning | CLASSIC5 | 123 (base 123) | -0.1476 | [-0.1500, -0.1456] | 1.000000 | CI wholly below zero (hi < 0) | 0/5 above, 5/5 BELOW (bar 3) | -0.1476 [-0.1500, -0.1456] | pick stability 12h: CHANGED on BTCUSDT, ETHUSDT, SOLUSDT (78 of 123 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | derived__slice_holdout | paired | holdout | CLASSIC5 | 77 (base 77) | -0.1538 | [-0.1569, -0.1506] | 1.000000 | CI wholly below zero (hi < 0) | 0/5 above, 5/5 BELOW (bar 3) | -0.1538 [-0.1569, -0.1506] | pick stability 12h: CHANGED on BTCUSDT, ETHUSDT, SOLUSDT (45 of 77 campaigns) | TIER-E | a SELECTION, not a result | nothing |

## The real regbooks (book facts only; every number is a book, not a verdict)

### Dry run

`scripts/tierc11_score.py --dry-run` against `research_outputs/tierc11/regbooks/` as filed when this repair finished. No ruler was called, and no interval, p or verdict is printed. Exit 8.

```
DRY RUN · regbooks root research_outputs/tierc11/regbooks · registry head 6772568b31fcfb2d… verified · books/v6 n 200 · every number below is a book, not a verdict
1 P-WARN-1: BUILT · spec ruler paired · era full · arms ['scored', 'base', 'tierE__holdout', 'tierE__tuning']
    scored                             n  200 · ΣR +41.923243 · mean R +0.209616 · tuning 123 / holdout 77 · ruler paired · era_scope full · CLASSIC5 · sha 956e15390419f8ab… (book, not a verdict)
    base                               n  200 · ΣR +40.807565 · mean R +0.204038 · tuning 123 / holdout 77 · ruler paired · era_scope full · CLASSIC5 · sha f41bfaf02b86dfb0… (book, not a verdict)
    tierE__holdout                     n   77 · ΣR +41.582228 · mean R +0.540029 · tuning 0 / holdout 77 · ruler paired · era_scope holdout · CLASSIC5 · sha 9dd70a94cb2b2923… (book, not a verdict)
    tierE__tuning                      n  123 · ΣR +0.341015 · mean R +0.002772 · tuning 123 / holdout 0 · ruler paired · era_scope tuning · CLASSIC5 · sha c41450b34294d820… (book, not a verdict)
    paired premise: key sets identical, n == n_base; identity law held on 158 unacted campaign(s) (42 acted)
2 P-AGE-1: BUILT · spec ruler two_sample · era full · arms ['scored', 'base', 'tierE__holdout', 'tierE__refused_cohort', 'tierE__shadow_abs206', 'tierE__tuning']
    scored                             n  141 · ΣR +63.464131 · mean R +0.450100 · tuning 81 / holdout 60 · ruler two_sample · era_scope full · CLASSIC5 · sha d008fa5086ce14f5… (book, not a verdict)
    base                               n  200 · ΣR +40.807565 · mean R +0.204038 · tuning 123 / holdout 77 · ruler two_sample · era_scope full · CLASSIC5 · sha f41bfaf02b86dfb0… (book, not a verdict)
    tierE__holdout                     n   60 · ΣR +52.001614 · mean R +0.866694 · tuning 0 / holdout 60 · ruler two_sample · era_scope holdout · CLASSIC5 · sha f7331ba523636425… (book, not a verdict)
    tierE__refused_cohort              n   59 · ΣR -22.656566 · mean R -0.384010 · tuning 42 / holdout 17 · ruler vs_zero · era_scope full · CLASSIC5 · sha 0569170404a1d10c… (book, not a verdict)
    tierE__shadow_abs206               n   80 · ΣR +48.803986 · mean R +0.610050 · tuning 45 / holdout 35 · ruler two_sample · era_scope full · CLASSIC5 · sha 2c1e47eec765be4a… (book, not a verdict)
    tierE__tuning                      n   81 · ΣR +11.462516 · mean R +0.141513 · tuning 81 / holdout 0 · ruler two_sample · era_scope tuning · CLASSIC5 · sha 4acc5b91b27e1a93… (book, not a verdict)
    two-sample keys: shared 141, only scored 0, only base 59
    gate: a post-filter of the base (no new key, every kept row unchanged)
3 P-WIN-1: BUILT · spec ruler two_sample · era full · arms ['scored', 'base', 'tierE__holdout', 'tierE__ratr_admission', 'tierE__ratr_priority', 'tierE__refused_cohort', 'tierE__shadow_lag7_15', 'tierE__tuning']
    scored                             n  137 · ΣR +51.974019 · mean R +0.379372 · tuning 81 / holdout 56 · ruler two_sample · era_scope full · CLASSIC5 · sha fd3f407ad6b18670… (book, not a verdict)
    base                               n  200 · ΣR +40.807565 · mean R +0.204038 · tuning 123 / holdout 77 · ruler two_sample · era_scope full · CLASSIC5 · sha f41bfaf02b86dfb0… (book, not a verdict)
    tierE__holdout                     n   56 · ΣR +43.951452 · mean R +0.784847 · tuning 0 / holdout 56 · ruler two_sample · era_scope holdout · CLASSIC5 · sha 7cdb206beff5ae4d… (book, not a verdict)
    tierE__ratr_admission              n  147 · ΣR +19.115450 · mean R +0.130037 · tuning 92 / holdout 55 · ruler two_sample · era_scope full · CLASSIC5 · sha dcfffefbddad3896… (book, not a verdict)
    tierE__ratr_priority               n  165 · ΣR +18.392480 · mean R +0.111470 · tuning 99 / holdout 66 · ruler two_sample · era_scope full · CLASSIC5 · sha a10416bd49c47a08… (book, not a verdict)
    tierE__refused_cohort              n   63 · ΣR -11.166454 · mean R -0.177245 · tuning 42 / holdout 21 · ruler vs_zero · era_scope full · CLASSIC5 · sha 7a97b32895c78324… (book, not a verdict)
    tierE__shadow_lag7_15              n  196 · ΣR +43.085655 · mean R +0.219825 · tuning 121 / holdout 75 · ruler two_sample · era_scope full · CLASSIC5 · sha f624bffc3baea057… (book, not a verdict)
    tierE__tuning                      n   81 · ΣR +8.022567 · mean R +0.099044 · tuning 81 / holdout 0 · ruler two_sample · era_scope tuning · CLASSIC5 · sha 862fc6fd0a237ed4… (book, not a verdict)
    two-sample keys: shared 137, only scored 0, only base 63
    gate: a post-filter of the base (no new key, every kept row unchanged)
4 P-BRK-4H: BUILT · spec ruler vs_zero · era full · arms ['scored', 'tierE__frozen3', 'tierE__holdout', 'tierE__memline_first_hold', 'tierE__memline_oneshot_flip', 'tierE__oneshot_first_touch', 'tierE__panel17', 'tierE__tuning']
    scored                             n  322 · ΣR +16.185338 · mean R +0.050265 · tuning 210 / holdout 112 · ruler vs_zero · era_scope full · CLASSIC5 · sha c76358dfaeb034dd… (book, not a verdict)
    tierE__frozen3                     n  232 · ΣR +38.306089 · mean R +0.165112 · tuning 149 / holdout 83 · ruler vs_zero · era_scope full · CLASSIC5 · sha ce34edb784fd5c62… (book, not a verdict)
    tierE__holdout                     n  112 · ΣR +25.023127 · mean R +0.223421 · tuning 0 / holdout 112 · ruler vs_zero · era_scope holdout · CLASSIC5 · sha 8ef3e6119006c58c… (book, not a verdict)
    tierE__memline_first_hold          n  186 · ΣR +66.723800 · mean R +0.358730 · tuning 123 / holdout 63 · ruler vs_zero · era_scope full · CLASSIC5 · sha 9e11902a3d933cb7… (book, not a verdict)
    tierE__memline_oneshot_flip        n  166 · ΣR +48.809599 · mean R +0.294034 · tuning 109 / holdout 57 · ruler vs_zero · era_scope full · CLASSIC5 · sha 2212c4d117181da1… (book, not a verdict)
    tierE__oneshot_first_touch         n  289 · ΣR +18.789452 · mean R +0.065015 · tuning 189 / holdout 100 · ruler vs_zero · era_scope full · CLASSIC5 · sha 60cfab3678b01936… (book, not a verdict)
    tierE__panel17                     n  762 · ΣR +89.248622 · mean R +0.117124 · tuning 428 / holdout 334 · ruler vs_zero · era_scope full · PANEL17 · sha 761922c7fc32f0ef… (book, not a verdict)
    tierE__tuning                      n  210 · ΣR -8.837788 · mean R -0.042085 · tuning 210 / holdout 0 · ruler vs_zero · era_scope tuning · CLASSIC5 · sha 831c53b34fc2ae1a… (book, not a verdict)
5 P-RELAY-1: BUILT · spec ruler two_sample · era full · arms ['scored', 'base', 'tierE__holdout_slice', 'tierE__late_relay', 'tierE__miss_v6', 'tierE__tuning_slice']
    scored                             n  173 · ΣR +78.479726 · mean R +0.453640 · tuning 114 / holdout 59 · ruler two_sample · era_scope full · CLASSIC5 · sha 57d8bbef8190492d… (book, not a verdict)
    base                               n  200 · ΣR +40.807565 · mean R +0.204038 · tuning 123 / holdout 77 · ruler two_sample · era_scope full · CLASSIC5 · sha f41bfaf02b86dfb0… (book, not a verdict)
    tierE__holdout_slice               n   59 · ΣR +42.394155 · mean R +0.718545 · tuning 0 / holdout 59 · ruler two_sample · era_scope holdout · CLASSIC5 · sha 7e975ad781e3e31f… (book, not a verdict)
    tierE__late_relay                  n  283 · ΣR +131.643918 · mean R +0.465173 · tuning 181 / holdout 102 · ruler two_sample · era_scope full · CLASSIC5 · sha 9e295b903e0c6e37… (book, not a verdict)
    tierE__miss_v6                     n  131 · ΣR +53.941312 · mean R +0.411766 · tuning 77 / holdout 54 · ruler vs_zero · era_scope full · CLASSIC5 · sha 306b9ceebecb9e51… (book, not a verdict)
    tierE__tuning_slice                n  114 · ΣR +36.085571 · mean R +0.316540 · tuning 114 / holdout 0 · ruler two_sample · era_scope tuning · CLASSIC5 · sha 10ac7ec867fab087… (book, not a verdict)
    two-sample keys: shared 0, only scored 173, only base 200
6 P-SCALP-2: ABSENT (no STATUS.json)
7 P-ADD-BRK: BUILT · spec ruler paired · era full · arms ['scored', 'base', 'tierE__frozen3', 'tierE__head_to_head_vs_p_add_sfp', 'tierE__holdout', 'tierE__refuse_below_entry', 'tierE__refuse_post_harvest', 'tierE__tuning']
    scored                             n  200 · ΣR +36.770865 · mean R +0.183854 · tuning 123 / holdout 77 · ruler paired · era_scope full · CLASSIC5 · sha 15ba415b7a30f20f… (book, not a verdict)
    base                               n  200 · ΣR +40.807565 · mean R +0.204038 · tuning 123 / holdout 77 · ruler paired · era_scope full · CLASSIC5 · sha f41bfaf02b86dfb0… (book, not a verdict)
    tierE__frozen3                     n  200 · ΣR +44.391987 · mean R +0.221960 · tuning 123 / holdout 77 · ruler paired · era_scope full · CLASSIC5 · sha b854c1c6ef8903d6… (book, not a verdict)
    tierE__head_to_head_vs_p_add_sfp   n  200 · ΣR +36.770865 · mean R +0.183854 · tuning 123 / holdout 77 · ruler paired · era_scope full · CLASSIC5 · sha 15ba415b7a30f20f… (book, not a verdict)
    tierE__holdout                     n   77 · ΣR +38.645247 · mean R +0.501886 · tuning 0 / holdout 77 · ruler paired · era_scope holdout · CLASSIC5 · sha a4854282ba7253e0… (book, not a verdict)
    tierE__refuse_below_entry          n  200 · ΣR +36.770865 · mean R +0.183854 · tuning 123 / holdout 77 · ruler paired · era_scope full · CLASSIC5 · sha 15ba415b7a30f20f… (book, not a verdict)
    tierE__refuse_post_harvest         n  200 · ΣR +36.768779 · mean R +0.183844 · tuning 123 / holdout 77 · ruler paired · era_scope full · CLASSIC5 · sha dbd4dbac8f4f28dc… (book, not a verdict)
    tierE__tuning                      n  123 · ΣR -1.874382 · mean R -0.015239 · tuning 123 / holdout 0 · ruler paired · era_scope tuning · CLASSIC5 · sha a8dc8371e22a4f28… (book, not a verdict)
    paired premise: key sets identical, n == n_base; identity law held on 148 unacted campaign(s) (52 acted)
8 P-ADD-SFP: BUILT · spec ruler paired · era full · arms ['scored', 'base', 'tierE__frozen3', 'tierE__head_to_head_vs_p_add_brk', 'tierE__holdout', 'tierE__refuse_below_entry', 'tierE__refuse_post_harvest', 'tierE__tuning']
    scored                             n  200 · ΣR +36.811969 · mean R +0.184060 · tuning 123 / holdout 77 · ruler paired · era_scope full · CLASSIC5 · sha ee2d19250f3e3d74… (book, not a verdict)
    base                               n  200 · ΣR +40.807565 · mean R +0.204038 · tuning 123 / holdout 77 · ruler paired · era_scope full · CLASSIC5 · sha f41bfaf02b86dfb0… (book, not a verdict)
    tierE__frozen3                     n  200 · ΣR +40.129503 · mean R +0.200648 · tuning 123 / holdout 77 · ruler paired · era_scope full · CLASSIC5 · sha 227a062b2ed99c28… (book, not a verdict)
    tierE__head_to_head_vs_p_add_brk   n  200 · ΣR +36.811969 · mean R +0.184060 · tuning 123 / holdout 77 · ruler paired · era_scope full · CLASSIC5 · sha ee2d19250f3e3d74… (book, not a verdict)
    tierE__holdout                     n   77 · ΣR +39.634377 · mean R +0.514732 · tuning 0 / holdout 77 · ruler paired · era_scope holdout · CLASSIC5 · sha fb0f47b8604ac1ee… (book, not a verdict)
    tierE__refuse_below_entry          n  200 · ΣR +37.006164 · mean R +0.185031 · tuning 123 / holdout 77 · ruler paired · era_scope full · CLASSIC5 · sha eccbbcbd9afbaa55… (book, not a verdict)
    tierE__refuse_post_harvest         n  200 · ΣR +37.733492 · mean R +0.188667 · tuning 123 / holdout 77 · ruler paired · era_scope full · CLASSIC5 · sha 80276294f3ce4cbd… (book, not a verdict)
    tierE__tuning                      n  123 · ΣR -2.822408 · mean R -0.022946 · tuning 123 / holdout 0 · ruler paired · era_scope tuning · CLASSIC5 · sha 011c58ba0964a713… (book, not a verdict)
    paired premise: key sets identical, n == n_base; identity law held on 191 unacted campaign(s) (9 acted)
9 P-TP-RNG: BUILT · spec ruler paired · era full · arms ['scored', 'base', 'tierE__frozen3', 'tierE__holdout', 'tierE__tp_post_harvest', 'tierE__tuning', 'tierE__unguarded']
    scored                             n  200 · ΣR +36.816470 · mean R +0.184082 · tuning 123 / holdout 77 · ruler paired · era_scope full · CLASSIC5 · sha a10c667b26932948… (book, not a verdict)
    base                               n  200 · ΣR +40.807565 · mean R +0.204038 · tuning 123 / holdout 77 · ruler paired · era_scope full · CLASSIC5 · sha f41bfaf02b86dfb0… (book, not a verdict)
    tierE__frozen3                     n  200 · ΣR +45.673724 · mean R +0.228369 · tuning 123 / holdout 77 · ruler paired · era_scope full · CLASSIC5 · sha 8ff7213a76ecf1c2… (book, not a verdict)
    tierE__holdout                     n   77 · ΣR +38.853474 · mean R +0.504591 · tuning 0 / holdout 77 · ruler paired · era_scope holdout · CLASSIC5 · sha 8bd94584706ed92f… (book, not a verdict)
    tierE__tp_post_harvest             n  200 · ΣR +41.196408 · mean R +0.205982 · tuning 123 / holdout 77 · ruler paired · era_scope full · CLASSIC5 · sha 3d2c34a4fcdcc709… (book, not a verdict)
    tierE__tuning                      n  123 · ΣR -2.037004 · mean R -0.016561 · tuning 123 / holdout 0 · ruler paired · era_scope tuning · CLASSIC5 · sha ec8eb28167758a8d… (book, not a verdict)
    tierE__unguarded                   n  200 · ΣR +36.798296 · mean R +0.183991 · tuning 123 / holdout 77 · ruler paired · era_scope full · CLASSIC5 · sha b2c0794eaca8409e… (book, not a verdict)
    paired premise: key sets identical, n == n_base; identity law held on 164 unacted campaign(s) (36 acted)
F-BASE-IDENT OK · checked ['P-ADD-BRK', 'P-ADD-SFP', 'P-AGE-1', 'P-RELAY-1', 'P-TP-RNG', 'P-WARN-1', 'P-WIN-1'] · absent []
EXIT 8 = 8 (a registration is ABSENT (no STATUS.json))
```

### Arm facts

| registration | arm | status | n | ΣR | mean R | tuning/holdout | sidecar ruler | book_sha256 | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P-WARN-1 | scored | BUILT | 200 | +41.923243 | +0.209616 | 123/77 | paired | `956e15390419f8ab…` | TIER-E | a SELECTION, not a result | nothing |
| P-WARN-1 | base | BUILT | 200 | +40.807565 | +0.204038 | 123/77 | paired | `f41bfaf02b86dfb0…` | TIER-E | a SELECTION, not a result | nothing |
| P-WARN-1 | tierE__holdout | BUILT | 77 | +41.582228 | +0.540029 | 0/77 | paired | `9dd70a94cb2b2923…` | TIER-E | a SELECTION, not a result | nothing |
| P-WARN-1 | tierE__tuning | BUILT | 123 | +0.341015 | +0.002772 | 123/0 | paired | `c41450b34294d820…` | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | scored | BUILT | 141 | +63.464131 | +0.450100 | 81/60 | two_sample | `d008fa5086ce14f5…` | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | base | BUILT | 200 | +40.807565 | +0.204038 | 123/77 | two_sample | `f41bfaf02b86dfb0…` | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | tierE__holdout | BUILT | 60 | +52.001614 | +0.866694 | 0/60 | two_sample | `f7331ba523636425…` | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | tierE__refused_cohort | BUILT | 59 | -22.656566 | -0.384010 | 42/17 | vs_zero | `0569170404a1d10c…` | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | tierE__shadow_abs206 | BUILT | 80 | +48.803986 | +0.610050 | 45/35 | two_sample | `2c1e47eec765be4a…` | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | tierE__tuning | BUILT | 81 | +11.462516 | +0.141513 | 81/0 | two_sample | `4acc5b91b27e1a93…` | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | scored | BUILT | 137 | +51.974019 | +0.379372 | 81/56 | two_sample | `fd3f407ad6b18670…` | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | base | BUILT | 200 | +40.807565 | +0.204038 | 123/77 | two_sample | `f41bfaf02b86dfb0…` | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__holdout | BUILT | 56 | +43.951452 | +0.784847 | 0/56 | two_sample | `7cdb206beff5ae4d…` | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__ratr_admission | BUILT | 147 | +19.115450 | +0.130037 | 92/55 | two_sample | `dcfffefbddad3896…` | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__ratr_priority | BUILT | 165 | +18.392480 | +0.111470 | 99/66 | two_sample | `a10416bd49c47a08…` | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__refused_cohort | BUILT | 63 | -11.166454 | -0.177245 | 42/21 | vs_zero | `7a97b32895c78324…` | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__shadow_lag7_15 | BUILT | 196 | +43.085655 | +0.219825 | 121/75 | two_sample | `f624bffc3baea057…` | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__tuning | BUILT | 81 | +8.022567 | +0.099044 | 81/0 | two_sample | `862fc6fd0a237ed4…` | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | scored | BUILT | 322 | +16.185338 | +0.050265 | 210/112 | vs_zero | `c76358dfaeb034dd…` | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__frozen3 | BUILT | 232 | +38.306089 | +0.165112 | 149/83 | vs_zero | `ce34edb784fd5c62…` | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__holdout | BUILT | 112 | +25.023127 | +0.223421 | 0/112 | vs_zero | `8ef3e6119006c58c…` | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__memline_first_hold | BUILT | 186 | +66.723800 | +0.358730 | 123/63 | vs_zero | `9e11902a3d933cb7…` | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__memline_oneshot_flip | BUILT | 166 | +48.809599 | +0.294034 | 109/57 | vs_zero | `2212c4d117181da1…` | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__oneshot_first_touch | BUILT | 289 | +18.789452 | +0.065015 | 189/100 | vs_zero | `60cfab3678b01936…` | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__panel17 | BUILT | 762 | +89.248622 | +0.117124 | 428/334 | vs_zero | `761922c7fc32f0ef…` | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__tuning | BUILT | 210 | -8.837788 | -0.042085 | 210/0 | vs_zero | `831c53b34fc2ae1a…` | TIER-E | a SELECTION, not a result | nothing |
| P-RELAY-1 | scored | BUILT | 173 | +78.479726 | +0.453640 | 114/59 | two_sample | `57d8bbef8190492d…` | TIER-E | a SELECTION, not a result | nothing |
| P-RELAY-1 | base | BUILT | 200 | +40.807565 | +0.204038 | 123/77 | two_sample | `f41bfaf02b86dfb0…` | TIER-E | a SELECTION, not a result | nothing |
| P-RELAY-1 | tierE__holdout_slice | BUILT | 59 | +42.394155 | +0.718545 | 0/59 | two_sample | `7e975ad781e3e31f…` | TIER-E | a SELECTION, not a result | nothing |
| P-RELAY-1 | tierE__late_relay | BUILT | 283 | +131.643918 | +0.465173 | 181/102 | two_sample | `9e295b903e0c6e37…` | TIER-E | a SELECTION, not a result | nothing |
| P-RELAY-1 | tierE__miss_v6 | BUILT | 131 | +53.941312 | +0.411766 | 77/54 | vs_zero | `306b9ceebecb9e51…` | TIER-E | a SELECTION, not a result | nothing |
| P-RELAY-1 | tierE__tuning_slice | BUILT | 114 | +36.085571 | +0.316540 | 114/0 | two_sample | `10ac7ec867fab087…` | TIER-E | a SELECTION, not a result | nothing |
| P-SCALP-2 | (no STATUS.json) | ABSENT | — | — | — | — | — | — | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | scored | BUILT | 200 | +36.770865 | +0.183854 | 123/77 | paired | `15ba415b7a30f20f…` | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | base | BUILT | 200 | +40.807565 | +0.204038 | 123/77 | paired | `f41bfaf02b86dfb0…` | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__frozen3 | BUILT | 200 | +44.391987 | +0.221960 | 123/77 | paired | `b854c1c6ef8903d6…` | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__head_to_head_vs_p_add_sfp | BUILT | 200 | +36.770865 | +0.183854 | 123/77 | paired | `15ba415b7a30f20f…` | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__holdout | BUILT | 77 | +38.645247 | +0.501886 | 0/77 | paired | `a4854282ba7253e0…` | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__refuse_below_entry | BUILT | 200 | +36.770865 | +0.183854 | 123/77 | paired | `15ba415b7a30f20f…` | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__refuse_post_harvest | BUILT | 200 | +36.768779 | +0.183844 | 123/77 | paired | `dbd4dbac8f4f28dc…` | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__tuning | BUILT | 123 | -1.874382 | -0.015239 | 123/0 | paired | `a8dc8371e22a4f28…` | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | scored | BUILT | 200 | +36.811969 | +0.184060 | 123/77 | paired | `ee2d19250f3e3d74…` | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | base | BUILT | 200 | +40.807565 | +0.204038 | 123/77 | paired | `f41bfaf02b86dfb0…` | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__frozen3 | BUILT | 200 | +40.129503 | +0.200648 | 123/77 | paired | `227a062b2ed99c28…` | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__head_to_head_vs_p_add_brk | BUILT | 200 | +36.811969 | +0.184060 | 123/77 | paired | `ee2d19250f3e3d74…` | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__holdout | BUILT | 77 | +39.634377 | +0.514732 | 0/77 | paired | `fb0f47b8604ac1ee…` | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__refuse_below_entry | BUILT | 200 | +37.006164 | +0.185031 | 123/77 | paired | `eccbbcbd9afbaa55…` | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__refuse_post_harvest | BUILT | 200 | +37.733492 | +0.188667 | 123/77 | paired | `80276294f3ce4cbd…` | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__tuning | BUILT | 123 | -2.822408 | -0.022946 | 123/0 | paired | `011c58ba0964a713…` | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | scored | BUILT | 200 | +36.816470 | +0.184082 | 123/77 | paired | `a10c667b26932948…` | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | base | BUILT | 200 | +40.807565 | +0.204038 | 123/77 | paired | `f41bfaf02b86dfb0…` | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | tierE__frozen3 | BUILT | 200 | +45.673724 | +0.228369 | 123/77 | paired | `8ff7213a76ecf1c2…` | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | tierE__holdout | BUILT | 77 | +38.853474 | +0.504591 | 0/77 | paired | `8bd94584706ed92f…` | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | tierE__tp_post_harvest | BUILT | 200 | +41.196408 | +0.205982 | 123/77 | paired | `3d2c34a4fcdcc709…` | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | tierE__tuning | BUILT | 123 | -2.037004 | -0.016561 | 123/0 | paired | `ec8eb28167758a8d…` | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | tierE__unguarded | BUILT | 200 | +36.798296 | +0.183991 | 123/77 | paired | `b2c0794eaca8409e…` | TIER-E | a SELECTION, not a result | nothing |

### Full path with the bootstrap stubbed (NaN draws): no interval, no p, no verdict computed

It exercises the premises, identity law, gate law, status records, SCALE prints, Tier-E rows and collar guard on the real books. 56 Tier-E rows; 0 findings; `EXIT 8 = 8 (a registration is ABSENT (no STATUS.json))`.

| registration | status | row | Tier-E rows | Tier-E halted | halts |
|---|---|---|---|---|---|
| P-WARN-1 | BUILT | ruled (stubbed) | 4 | 0 | — |
| P-AGE-1 | BUILT | ruled (stubbed) | 6 | 0 | — |
| P-WIN-1 | BUILT | ruled (stubbed) | 8 | 0 | — |
| P-BRK-4H | BUILT | ruled (stubbed) | 9 | 0 | — |
| P-RELAY-1 | BUILT | ruled (stubbed) | 6 | 0 | — |
| P-SCALP-2 | ABSENT | — | 0 | 0 | — |
| P-ADD-BRK | BUILT | ruled (stubbed) | 8 | 0 | — |
| P-ADD-SFP | BUILT | ruled (stubbed) | 8 | 0 | — |
| P-TP-RNG | BUILT | ruled (stubbed) | 7 | 0 | — |

SCALE-IN-SAMPLE beside-prints on the real books. These are record facts, not results:

| registration | lens | pick stability | in-sample range reads in the holdout slice | filed holdout arm | frozen-3.0 twin | fallback label | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|
| P-BRK-4H | 4h | pick stability (4h, first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on NEARUSDT 2.0->1.75 (63 of 322 campaigns on a changed asset) | 1 of 112 (scale_in_sample, die_close_ms<=cut) | tierE__holdout | tierE__frozen3 | — | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | 1h | pick stability (1h, first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on BTCUSDT 2.0->1.75, SOLUSDT 2.0->1.75, NEARUSDT 2.0->1.75 (115 of 200 campaigns on a changed asset) | 0 of 77 (n_adds_scale_in_sample) | tierE__holdout | tierE__frozen3 | — | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | 1h | pick stability (1h, first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on BTCUSDT 2.0->1.75, SOLUSDT 2.0->1.75, NEARUSDT 2.0->1.75 (115 of 200 campaigns on a changed asset) | 0 of 77 (n_adds_scale_in_sample) | tierE__holdout | tierE__frozen3 | — | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | 12h | pick stability (12h, first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on BTCUSDT 1.75->2.0, ETHUSDT 2.0->1.5, SOLUSDT 1.75->2.25 (123 of 200 campaigns on a changed asset) | 0 of 77 (scale_in_sample_12h) | tierE__holdout | tierE__frozen3 | — | TIER-E | a SELECTION, not a result | nothing |

Tier-E scale flags on the real books:

| registration | arm | scale flags (L-R.2) | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|
| P-BRK-4H | derived__slice_tuning | pick stability 4h: CHANGED on NEARUSDT (39 of 210 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | derived__slice_holdout | pick stability 4h: CHANGED on NEARUSDT (24 of 112 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__frozen3 | frozen 3.0: no calibrated pick consumed | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__holdout | pick stability 4h: CHANGED on NEARUSDT (24 of 112 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__memline_first_hold | pick stability 4h: CHANGED on NEARUSDT (28 of 186 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__memline_oneshot_flip | pick stability 4h: CHANGED on NEARUSDT (28 of 166 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__oneshot_first_touch | pick stability 4h: CHANGED on NEARUSDT (59 of 289 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__panel17 | pick stability 4h: CHANGED on NEARUSDT (63 of 762 campaigns) · IN-SAMPLE everywhere (whole-tape pick fallback [L-R.2]): HYPEUSDT 4h, PUMPUSDT 4h (26 of 762 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__tuning | pick stability 4h: CHANGED on NEARUSDT (39 of 210 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | derived__slice_tuning | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (72 of 123 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | derived__slice_holdout | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (43 of 77 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__frozen3 | frozen 3.0: no calibrated pick consumed | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__head_to_head_vs_p_add_sfp | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (115 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__holdout | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (43 of 77 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__refuse_below_entry | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (115 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__refuse_post_harvest | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (115 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__tuning | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (72 of 123 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | derived__slice_tuning | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (72 of 123 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | derived__slice_holdout | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (43 of 77 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__frozen3 | frozen 3.0: no calibrated pick consumed | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__head_to_head_vs_p_add_brk | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (115 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__holdout | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (43 of 77 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__refuse_below_entry | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (115 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__refuse_post_harvest | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (115 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__tuning | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (72 of 123 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | derived__slice_tuning | pick stability 12h: CHANGED on BTCUSDT, ETHUSDT, SOLUSDT (78 of 123 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | derived__slice_holdout | pick stability 12h: CHANGED on BTCUSDT, ETHUSDT, SOLUSDT (45 of 77 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | tierE__frozen3 | frozen 3.0: no calibrated pick consumed | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | tierE__holdout | pick stability 12h: CHANGED on BTCUSDT, ETHUSDT, SOLUSDT (45 of 77 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | tierE__tp_post_harvest | pick stability 12h: CHANGED on BTCUSDT, ETHUSDT, SOLUSDT (123 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | tierE__tuning | pick stability 12h: CHANGED on BTCUSDT, ETHUSDT, SOLUSDT (78 of 123 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | tierE__unguarded | pick stability 12h: CHANGED on BTCUSDT, ETHUSDT, SOLUSDT (123 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |

- P-SCALP-2 (ABSENT) prints beside it: beside, Tier-E [§10] (tier TIER-E · a SELECTION, not a result · gates nothing): the tuning-era R2 1h word FAIL (holdout word of record FAIL)
- P-WARN-1 condition record (agrees with STATUS BUILT): `{"ci_hi": -0.5277942972642365, "delta": -0.728646908214193, "met": true, "path": "P-WARN-1/condition.json", "sha256": "41670c5ac533253ae4c2239253784344d262fe529aeb20be2ce1a36fcd7dc86d"}`
- Records read: r2_lens_verdicts `research_outputs/tierc11/stage_r/R2_LENS_VERDICTS.json` `82cc3ec6ddd588c9fbd8402def471438a0c931590606b9a2a6cc3a97572f3087` · scale_picks `research_outputs/tierc11/ranges/SCALE_PICKS.json` `cb5319c975e44df610c05f5917759b7b47d819fa095b8af26d174d79fcef454f` · LEANS_AMENDMENTS.md `b1c6275b5008fa684af9bebdaeefa2c41a99f40e60f033db71d085c9ba3e10fb`

### F-BASE-IDENT on the real regbooks: OK

| registration | base book_sha256 |
|---|---|
| P-ADD-BRK | `f41bfaf02b86dfb0b57dcffaf3c5f5e4bb05eda5c305b361322bc334369468a8` |
| P-ADD-SFP | `f41bfaf02b86dfb0b57dcffaf3c5f5e4bb05eda5c305b361322bc334369468a8` |
| P-AGE-1 | `f41bfaf02b86dfb0b57dcffaf3c5f5e4bb05eda5c305b361322bc334369468a8` |
| P-RELAY-1 | `f41bfaf02b86dfb0b57dcffaf3c5f5e4bb05eda5c305b361322bc334369468a8` |
| P-TP-RNG | `f41bfaf02b86dfb0b57dcffaf3c5f5e4bb05eda5c305b361322bc334369468a8` |
| P-WARN-1 | `f41bfaf02b86dfb0b57dcffaf3c5f5e4bb05eda5c305b361322bc334369468a8` |
| P-WIN-1 | `f41bfaf02b86dfb0b57dcffaf3c5f5e4bb05eda5c305b361322bc334369468a8` |

## Findings (not fixed here; each names its owner)

1. **RESOLVED since the first build: F-BASE-IDENT on the real regbooks.** Stage W re-filed P-WARN-1 at 02:35, and its base now carries v6's 4h `exit_close_ms`. All seven bases share `f41bfaf0…` and equal books/v6 on 13 columns at 6 dp. P-WARN-1's STATUS is BUILT ("condition MET"), and its `condition.json` agrees (met True, ci_hi < 0). This is L-W.4's Tier-E condition, not a registered result.
2. **P-SCALP-2 has no STATUS.json under the regbooks root yet. Owner: Stage S.** The scorer prints it ABSENT and exits with bit 8 (family incomplete). When Stage S files, its STATUS must agree with the R2 1h lens word of record, which reads FAIL today, so the only word that passes SC-17 is CLOSED_BY_PRECONDITION. Its §0 cell already prints the tuning-era R2 1h word (FAIL), collared.
3. **Reading scope, L-W.4 vs L-1.4** (unchanged; the verifier agreed that it is an operator question). L-W.4's sentence "The condition block is the only Tier-E place a CI is printed" is read here as scoped to Stage W's W2 tables. L-1.4 prescribes `would_read_ci_only` on every Tier-E row, so the scorer prints intervals on Tier-E arms.
4. **Stage A now files both adds head-to-heads** (`tierE__head_to_head_vs_p_add_sfp` / `_brk`, base_arm set), so the scorer derives none on the real books (SC-18). Disclosure: Stage A's `P-ADD-BRK/tierE__refuse_below_entry` hashes identical to its scored arm (`15ba415b…`). That is the stage's fact, reported, not judged here.
5. **The interface contract holds on real data under the stricter checks.** Exact dtypes, no CSV-hostile strings, entry bars within 4h, the identity law on every paired arm, and the gate post-filter law on both gates all hold. Every real arm's sidecar book_sha256 equals the scorer's canonical CSV, and no stability column disagrees with SCALE_PICKS.json.
6. **Planted-only NET-LAW disclosures.** They come from the planted base being books/v6 at 6 dp, where net ≠ gross − fee − funding by ≤ 1e-6.

## AMENDMENT CANDIDATES

None. Every repair builds a reading as it is written: L-R.2 (pick stability, the fallback label, the holdout slice), L-1.5 (the identity law, gates as post-filters), L-W.4 / L-S.1 / §10 (the gating records, the tuning-era R2 word), L-1.3 (era by close) and AM-3 (the v6-leg absorption). Where the frozen text is silent, the executor sub-readings SC-1..SC-19 are printed above and in every output. The lens map of SC-14 is taken from the texts of record.
