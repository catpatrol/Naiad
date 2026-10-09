## L-X · STATISTICS, REGISTRATIONS, SCORING AND CLOSE

This section governs everything that turns a book into a word and a word into a published record: (A) the three
families and the statistic of record (ruler, draws, interval, p, verdict law, the verdict vocabulary, LOAO, the
single-trade share, the in-sample labels, the beside-prints); (B) the registration architecture (how the contract is
pinned, how the five texts are sliced, what `REGISTRATIONS.json` holds, how it is written once, and how
text-before-result is proven); (C) the scorer (`scripts/tierc12_score.py` and the interface module
`scripts/tierc12_regbook.py`: the pinned inputs, the regbook interface Stages G / R / S build to, the outputs and the
write law); (D) CLOSE (the report's order, the number-tracing law, findings-not-fixed, BOX-COST, the ledger append,
and `close_acts.sh` — every step an operator keystroke, O-12). It owns no registered row; the five rows are owned by
L-G (P-ADM-1, P-BRD-1), L-R (P-DIR-1, P-SFP-VA-1) and L-S (P-SCALP-3). Each owner's REGISTRATION SPEC states the
common clauses at the end of this section in its own text: a spec block is carried verbatim into the write-once
registry and refers to nothing outside itself. This section conforms to ORCHESTRATOR_RULINGS O-1..O-32.

Conventions used below. Paths are relative to `/Users/luis/Naiad` unless absolute; `x_rec/` abbreviates
`research_outputs/tierc12/x_rec/`. "The contract" is `exchange/queue/2026-10-08_TC12_APOLLO.md` (prefix sha256
`861d6050e80e66995e4f9db2855aaf274d63285249c2549e5a0813582095a7bd`), cited `:<line>`. `E` is L-D's env shim
`scripts/tierc12_env.py`; `W` = `E.TC11_PIN_MS` (the score edge), `PIN` = `E.PIN_MS`, `ERA_CUT` = `E.ERA_CUT_MS`.
"Certified" means the sha that `tierc12_progress.certified(path)` returns: the entry of the LAST progress record
that names the path (L-0.4). A fixture block id is `<FID>` or `<FID> [<qualifier>]` (L-0.14). A value written "(on
file: v)" is information for the reader; the constant the build uses is the named object, read at run time. Every
sha, line number and line-slice sha printed here was re-hashed or re-read while drafting [measured here]; no outcome
of any TC12 book was computed, and no `tc11x_*`, `tierc10_*` or `tierc11_*` module was imported or run.

---------------------------------------------------------------------------------------------------------------
### A · Families, the statistic of record, the verdict vocabulary

**L-X.1 THE THREE FAMILIES, PARSED** — "families declared by MECHANISM before the look, each independently failable,
bar = 0.10 ÷ m per family" (contract :8-9); "STAGE G · ADMISSION FAMILY (m=2, bar 0.05; …" (:52); "STAGE R ·
RANGE-STATE FAMILY (m=2, bar 0.05):" (:64); "STAGE S · SCALPER FAMILY (m=1, bar 0.10)" (:82)
READING:
- Nothing about a family is typed. The parse is rows of L-0.17's pin map (pins `fam.q` and `fam.<stage letter>`),
  run by the pin door (`scripts/tierc12_pins.py`) over the PREFIX lines of the contract (L-X.16) and called by the
  registry filer (`scripts/tierc12_registrations.py`); L-0.18 states the law, this reading the exact rule. The pin
  door, its map and its derived files (`pins/CONTRACT_PIN_MAP.json`, `pins/CONTRACT_PINS.json`,
  `pins/PIN_REGISTER.json`) are members of `REG_SET` (L-X.21): they are on disk before `--file` runs and are added
  by the same commit as the registry. Two regular expressions:
  - `R_FAM = ^STAGE ([A-Z]) · ([A-Z][A-Z-]*) FAMILY \(m=(\d+), bar (\d+\.\d+)(?=[;)])`, applied with `re.match` to
    each line; group 1 is the stage letter, group 2 the family name of record, group 3 `m`, group 4 the bar text;
  - `R_Q = bar = (\d+\.\d+) ÷ m per family`, applied with `re.search` to each line; group 1 is the q text.
- HALT `FAMILY-PARSE` unless the lines matching `R_FAM` are exactly the lines the plan's verified line map marks
  as family headers (L-X.17; on the filed bytes :52, :64, :82), exactly one line matches `R_Q` and it lies inside
  the map's LAWS slice (on the filed bytes :9), and the family names and the stage letters are each distinct.
- Exact arithmetic, no float: `q = Fraction(Decimal(q_text))`, `bar_f = Fraction(Decimal(bar_text_f))`,
  `m_f = int(m_text_f)`. **HALT `FAMILY-BAR` unless `bar_f == q / m_f` for every family.** The header's bar and
  q ÷ m are thereby asserted equal; the bar the scorer reads at run time is `REGISTRATIONS.json
  families[].bar_exact` (filed from this parse), and the scorer re-runs the parse on the contract prefix and asserts
  the two equal before any number (detector FAMILY-BAR, L-X.22).
- Filed as `families[]` (L-X.19) carrying `q` and `bar` as the contract's own decimal strings and `bar_exact` as
  `"<num>/<den>"`.
SOURCE: contract :9, :52, :64, :82 (parse re-run on bytes of sha `861d6050…`: three `R_FAM` hits at 52 / 64 / 82, one
`R_Q` hit at 9) [measured here]; `scout/U7_registrations_scoring.md` §1.11, §2.3; precedent parser
`x_rec/scripts/tc11x_registrations.py:488-493` (written for a `FAMILIES (` line, which this contract does not
carry); exact-bar precedent `scripts/tierc11_score.py:233` (`BAR_FRAC`); ruling O-22.
RIVALS: type (family, m, bar) in the script — breaks "no number typed that a file can supply" (:8). Compute the bar
as q ÷ m and ignore the header's own bar — drops the contract's cross-check. One pooled family over five rows —
contradicts three headers. Float bars (X files `0.05` as a float) — loses exactness at the bar.
FAILS-IF: `F-FAM [PARSE]` (L-X.15, at TC12-SCORE) is RED when a header's bar ≠ q ÷ m or the parsed families are not
the line map's; the same parse is held at filing by the pins suite's `F-FAM-PINS` (L-0.18) and by the verifier's
detectors `FAMILY-PARSE` and `FAMILY-BAR` (L-X.22). Planted mutation: the STAGE G header of a scratch copy rewritten
with the SCALPER header's bar text must HALT `FAMILY-BAR`.

**L-X.2 MEMBERSHIP, m, AND WHAT A FAMILY SPENDS** — "each independently failable … a registration closed by
precondition spends no test" (:8-9); "F-FAM (m and bars printed per family; a precondition-closed row spends no
test)" (:122-123)
READING:
- A registration belongs to the family whose header line `h` is the greatest `R_FAM` line below the registration's
  first text line, provided no other line matching `^STAGE [A-Z] · ` lies in `(h, first text line]`; otherwise HALT
  `FAMILY-MEMBER`. HALT `FAMILY-M-COUNT` unless the number of registrations in each family equals its parsed `m`.
- `m` is declared and never loosened: no ranks, no step-up, no pooling of bars across families, no best-of. Each
  registration is scored alone against its own family's bar; a sibling's failure promotes nothing.
- `tests_spent_f` = the number of registrations of family f whose scorer row has status BUILT and no HALT. A row
  CLOSED BY PRECONDITION (L-X.10), a HALTed row and an ABSENT row spend no test. The bar is `q ÷ m_f` whatever
  `tests_spent_f` is.
- A BUILT row always spends its test, including the degenerate ones (L-X.7): no free closure.
- The tier declares three families, so the tier-wide chance of at least one false SUPPORTED is not q. The report's
  §1 says so in one sentence beside the three bars and prints `Σ_f m_f · bar_f` — computed from the parse as a
  Fraction, the nominal union bound over the registered tests — beside the five-cluster size footnote of L-X.14 (a
  disclosure, deciding nothing).
SOURCE: `research_outputs/tierc11/LEANS.md:122-124` (L-1.4, "spends no test, and never loosens the bar");
`x_rec/tierc11x/LEANS_X.md:721-724`; `scripts/tierc11_score.py:2075-2092` (`family`, `tests_spent`);
`research_outputs/tierc11/scores/FAMILY.json` key `law` (sha `3fa36bd4…2d73`); O-22.
RIVALS: bar = q ÷ (tests actually run) — loosens the bar after a closure; refused by both precedents. A HALTed row
counted as a spent NOT SUPPORTED — prints a verdict the ruler never produced.
FAILS-IF: `F-FAM [REAL]` is RED when a family's count ≠ its parsed m, a row's bar is not its family's, or
`tests_spent_f` ≠ the BUILT un-halted rows of f; `F-FAM [PLANTED]` is RED when the planted closed row spends a test
or the planted bar moves (L-X.15). Planted mutations: the bar recomputed as q ÷ (tests spent) → `M-LOOSENED`; the
closed row counted as spent → `TESTS-SPENT`.

**L-X.3 THE BOOTSTRAP OF RECORD: UNIT, DRAWS, SEEDS** — "bar = 0.10 ÷ m per family" (:9); "Seed 20261008." (:4)
READING:
- **Unit.** The whole asset: every trade of an asset (`symbol`) moves together. Each draw picks |U| assets from the
  |U| distinct labels with replacement (`rng.choice(uniq, size=len(uniq), replace=True)`), `uniq = np.unique(labels)`
  (sorted). No time blocks, no per-trade resampling.
- **Primitives, called and never re-implemented:** `tierc5.cluster_boot`, `tierc5.cluster_boot_diff`,
  `tierc5._ci_from`, reached as `E.T5` through L-D's env shim (the module's sha asserted by the shim against
  `env/LINEAGE_PINS.json` before the first call; on file `ad912b38…5a6f`).
- **Draws B.** The registry is filed before the env exists (L-0.10's order), so the FILING reads `N_BOOT` from
  filed records: `research_outputs/tierc11/scores/SCORES.json["n_boot"]` (on file: 4000; the file's sha asserted
  against `progress/TC12-R0.json["frozen_estate_shas_at_r0"]` — Q1 keeps that file unmoved), asserted equal to
  `x_rec/tierc11x/registrations/REGISTRY_PIN_X.json["n_boot"]` (its sha asserted against its `X_REC_MANIFEST.json`
  row). The SCORER reads the lineage object `E.TP.N_BOOT` (L-0.17's door) and HALTs unless it equals the filing's
  `statistics.n_boot`, the shim's `E.N_BOOT` and `inspect.signature(E.T5.cluster_boot).parameters["n_boot"].default`.
- **Seed of record.** The pin door's row `seed` for contract :4 (`Seed (\d{8})\.`, exactly one hit), asserted equal
  to `research_outputs/tierc12/PROGRESS.json["seed"]` and, in the scorer, to `E.SEED`. **Sensitivity seed:** filed
  from `SCORES.json["seed_sens"]` (on file 20260816); the scorer HALTs unless `E.T5.SEED` (`scripts/tierc5.py:86`)
  and `E.SEED_SENS` equal it. Printed beside, deciding nothing.
- **Seed handling.** Every ruler call passes `seed=` and `n_boot=` as keywords; a call relying on a default scores
  at the sensitivity seed (`tierc5.py:86`, `:1178`) or at TC10's seed (`scripts/tierc10_panel.py:91`, `:1235`) and
  is a defect. Each call builds its own `np.random.default_rng(seed)` inside T5, so no stream is shared and the
  order of calls moves no draw. The same integer, underived, rules the row, each LOAO panel, each slice, each twin.
- **Input order.** Every arm is sorted `(symbol, entry_close_ms)` by mergesort before any ruler (the mean inside a
  draw sums rows in that order; an unsorted arm breaks F-DET).
SOURCE: `scripts/tierc5.py:86`, `:1178-1197`, `:1200-1224`, `:1227-1235` [read here]; `scripts/tierc11_score.py:794-796`
(the sort), `:973-1006` (`ruled`); `x_rec/scripts/tc11x_score.py:192-194` (`boot`, seed and B explicit); the
estate's `N_BOOT` as typed in code, for the reader: `scripts/tierc10_panel.py:94`, `scripts/tierc11_env.py:127`; O-22;
`scout/U7_registrations_scoring.md` §1.4, H4, H8.
RIVALS: per-trade or month-block resampling as the unit of record — printed as the `month_block` twin (L-X.14), not
of record (the lineage's unit is the asset). A seed derived per row — no precedent, and it makes rows incomparable.
FAILS-IF: `F-BOOT [synthetic]` (at `TC12-ENV.score-build`, on arms the fixture builds — no Naiad data) is RED when
the draws the scorer's ruler call returns differ from the fixture's own `default_rng(seed).choice` loop; `F-BOOT
[real]` (at TC12-SCORE) is RED when a row's persisted draws differ from that loop run on the row's own arms.
Planted mutations, each inside a shadow copy of the scorer's ruler call: `cluster_boot` called without `seed=`; the
draw unit bent to rows; the seed bent by one.

**L-X.4 THE VS-ZERO FORM (P-SFP-VA-1, P-SCALP-3)** — "(vs zero; full corridor; …" (:69); "(vs zero; HOLDOUT era …"
(:83)
READING: values `v` = `net_r` of the scored arm (L-X.24), labels `c` = its `symbol`; point = `mean(v)`; draws =
`T5.cluster_boot(v, c, seed=SEED, n_boot=N_BOOT)`; `n_clusters = len(np.unique(c))`. P-SFP-VA-1's scored arm is the
4h book of record on the full corridor inside the scored window (every era, `entry_close_ms ≤ W`; O-9); P-SCALP-3's
is the through-tick (TICK) book on the holdout era inside the scored window (`ERA_CUT < entry_close_ms ≤ W`). The
filing asserts the text slice contains `vs zero` (detector RULER-TEXT).
SOURCE: `scripts/tierc5.py:1178-1197`; `scripts/tierc11_score.py:977-985`; contract :69, :83; O-9.
RIVALS: none on the ruler (the contract names it). Per-direction or per-asset rulers — Tier-E slices of the owning
stage.
FAILS-IF: `F-SCORE-ANCHOR [VS-ZERO]` (at `TC12-ENV.score-build`) is RED unless the mirrored ruler on TC11's filed
`regbooks/P-BRK-4H/scored.parquet` (read through `E.tc11_record`) at TC11's seed reproduces `SCORES.json
rows[registration=P-BRK-4H].stats.main`; planted mutation: `seed=` omitted.

**L-X.5 THE TWO-SAMPLE FORM (P-ADM-1, P-BRD-1, P-DIR-1)** — "both two-sample vs v6 — they remove trades" (:52);
"(two-sample vs v6)" (:65)
READING:
- `va`, `ca` = `net_r` and `symbol` of the KEPT book (the scored arm: v6 minus the refused campaigns, O-21);
  `vb`, `cb` = `net_r` and `symbol` of the WHOLE base book (kept and refused together).
- point = `mean(va) − mean(vb)`; draws = `T5.cluster_boot_diff(va, ca, vb, cb, seed=SEED, n_boot=N_BOOT)`: ONE asset
  pick per draw indexes both arms, and the draw is `mean(kept rows of the picked assets) − mean(base rows of the
  picked assets)`. `uniq` is the sorted union of both arms' labels.
- The statistic is kept-versus-all, never kept-versus-refused. The refused cohort is printed beside (n, mean, ΣR,
  and ΣR of both books); iff `mean(refused) > 0` the §0 cell appends "on per-campaign expectancy only; the gate
  forfeits +X R total".
- The filing asserts each gate's text or its family header contains `two-sample vs v6` (detector RULER-TEXT).
SOURCE: `scripts/tierc5.py:1200-1224`; `scripts/tierc11_score.py:986-994` (`ruled`, two_sample), `:1206-1220`
(`gate_block`); `research_outputs/tierc11/LEANS.md:147-150` (L-1.5); O-21, O-22.
RIVALS: kept versus refused — a different claim, and it double-counts the gate's effect. Paired Δ on a re-ride — a
gate removes trades; the re-ride is a Tier-E disclosure of counts and diff rows, never an arm and never a scorer
leaf (O-21; L-G.18, L-R.5).
FAILS-IF: `F-SCORE-ANCHOR [TWO-SAMPLE]` (at `TC12-ENV.score-build`) is RED unless the mirrored ruler on TC11's filed
`regbooks/P-AGE-1/{scored,base}.parquet` (read through `E.tc11_record`) at TC11's seed reproduces `SCORES.json
rows[registration=P-AGE-1].stats.main` (point, lo, hi, p_num, p_den, n_draws_finite, n, n_base, n_clusters);
planted mutation: the base arm replaced by the refused cohort.

**L-X.6 THE INTERVAL, p AS A FRACTION, THE DECIDING BOUND** — "bar = 0.10 ÷ m per family" (contract :9; the contract
names no interval, no draw count and no p law — these are O-22's: "5th/95th percentile interval, p = (#≤0 + 1)/(B +
1)")
READING:
- `ci = T5._ci_from(draws, point)`: `lo = np.percentile(d, 5)`, `hi = np.percentile(d, 95)` over the finite draws
  `d`, numpy's default linear interpolation between order statistics. The two levels are `_ci_from`'s own; the
  scorer types neither and never re-implements the interval.
- `k = #{b : d_b ≤ 0}` (an exact zero counts); **`p = Fraction(k + 1, B + 1)`** with `B = len(d)`, and `B == N_BOOT`
  is asserted on every row of record (L-X.7). `p_num`, `p_den`, `n_draws_finite`, `n_draws_le_0` are filed; the
  float `p_one_sided` from `_ci_from` is printed and decides nothing.
- Clause (b) of L-X.8 is evaluated on Fractions: `p ≤ bar_f`.
- **Deciding rank and bound, printed per row:** `r_f = floor((B + 1) · bar_f)` in integer arithmetic;
  `deciding_bound` = the `r_f`-th smallest draw (1-indexed); clause (b) holds iff `deciding_bound > 0`.
- `hi < 0` appends the description "— CI wholly below zero" to a NOT SUPPORTED cell; it is not a separate word.
SOURCE: `scripts/tierc5.py:1227-1235`; `scripts/tierc11_score.py:955-970` (`ci_of`, SC-1), `:1151-1157`
(`clears_bar` on a Fraction), `:1160-1167`; `research_outputs/tierc11/scores/SCORES.json
rows[registration=P-AGE-1].stats.main` (keys `p_num`, `p_den`, `deciding_rank`, `deciding_bound` on file).
RIVALS: clause (b) in floats (X's `verdict_of`, `x_rec/scripts/tc11x_score.py:202-206`) — inexact at the bar.
`p = #<0 / B` — drops the +1 and the zeros; a planted mutation of F-BOOT.
UNVERIFIED: that `np.percentile`'s default method in `~/venvs/naiad` is "linear" in the installed numpy; `F-BOOT
[synthetic]` re-derives `lo` and `hi` from the draws by its own order-statistic interpolation and compares
`float.hex` values, which settles it at `TC12-ENV.score-build`, before any book exists.
FAILS-IF: `F-BOOT [synthetic]` and `F-BOOT [real]` are RED when `lo`, `hi` or `p` re-derived from the draws (on the
real rows: from the persisted `draw_hex`, never from printed values) differ from the scorer's; planted mutations,
each in a shadow copy of the scorer: `p` bent to `#<0 / B`; the interval bent to the 2.5th / 97.5th; `<` used on a
draw set holding exact zeros.

**L-X.7 WHEN THE RULER IS NOT DEFINED OR CANNOT CLEAR: THE PANEL-COMPLETE CLAUSE, EMPTY ARMS, THE REFUSAL SPREAD,
`N_BOOT` FINITE DRAWS** — O-22; contract "five home assets" (:69-70, :84)
READING:
- A two-sample draw is NaN when an arm has no row in any picked asset (`tierc5.py:1220-1222`); a vs-zero book
  holding fewer assets than the declared panel is ruled on fewer clusters than registered. Both are decided before
  any outcome is read, on counts alone:
  - **Clause (c), PANEL COMPLETE:** every asset of the declared panel holds ≥ 1 row in every arm the ruler reads —
    the scored arm, and the base arm for a two-sample row. The declared panel of all five rows is the home panel:
    L-D's object `E.CLASSIC5` for the five stems of contract :18, which the `panel` of every `scored`, `base` and
    `ladder` sidecar must equal (L-X.24).
  - **If (c) fails the row cannot read SUPPORTED.** It reads NOT SUPPORTED with the qualifier `PANEL INCOMPLETE
    (<asset> holds no <arm> row)`, its test is spent, and whatever the ruler returns on the finite draws is printed
    as `not_of_record` with `n_draws_finite`. An empty scored arm (`n = 0`; on disk a zero-row parquet under
    L-X.24's empty-arm form, never a missing file) is the limiting case, qualifier `EMPTY BOOK`.
  - **If (c) holds, `n_draws_finite == N_BOOT` is ASSERTED at the seed of record and at the sensitivity seed;** a
    failure is HALT `DRAWS-NONFINITE` (with every asset present in every arm no take can be empty, so a non-finite
    draw is a code defect, not a result). A HALTed row prints no number, no word, spends no test, and blocks CLOSE
    (F-S0-FIVE).
- A gate that refuses nothing (`kept == base` by key): flagged `TWO-SAMPLE-PREMISE: key sets identical — the
  difference is 0 by construction`, ruled as it stands (every draw 0, `p = 1`), NOT SUPPORTED, test spent.
- **REFUSAL SPREAD (count-only, decided before any outcome is read; every two-sample row).** A refused campaign is
  a base key `(symbol, entry_ms)` absent from the kept arm. `N` = the number of declared assets; `a` = the number
  of declared assets holding ≥ 1 refused campaign; `z = Fraction((N − a)**N, N**N)` — the exact probability that a
  draw picks no refusing asset. Such a draw indexes the same rows in both arms, in the same order (L-X.3), so it is
  identically 0 and counts in `#draws ≤ 0`. Filed on every two-sample row: `refused_n`, `refused_assets` (the
  sorted stems), `p_draw_identically_zero` (`z` as `"<num>/<den>"`) and `n_draws_exact_zero` (the count of draws
  equal to 0.0 at the seed of record — the one field read from the draws; it decides nothing). **If `z ≥ bar_f` the
  row carries the qualifier `REFUSALS ON a/N ASSETS — the ruler cannot clear (P(draw ≡ 0) = z ≥ bar)`; the word is
  NOT SUPPORTED and the test is spent** (the undefined-counts-against law: the word follows from the counts and
  does not wait for the draws); the ruler's numbers are printed as they come; the cell is never cited as evidence
  against the gate. `a = 0` is TWO-SAMPLE-PREMISE.
- Beside-prints (L-X.14) carry no clause (c): a leaf with non-finite draws prints `n_draws_finite` and
  `nonfinite_draws = k`, is ruled on the finite draws by `_ci_from`, and decides nothing.
- Clause (c) applies to each fill-ladder book of P-SCALP-3: a book that fails it is `U(X)`, which never closes
  (L-X.9).
SOURCE: `scripts/tierc5.py:1218-1222`, `:1227-1229`; `scripts/tierc10_panel.py:1241-1242` ("a declared asset whose
leave-out panel cannot be bootstrapped counts AGAINST the line" — the lineage's undefined-counts-against law);
`scripts/tierc11_score.py:856-866` (SC-6, the identical-key flag), `:955-970` (`n_draws_finite`);
`scout/U7_registrations_scoring.md` H6, R14.
RIVALS: drop the NaN draws and rule on the rest (`_ci_from`'s own behaviour) — the denominator falls below B + 1 and
the deciding rank moves silently. HALT the row with no verdict when an arm is empty on an asset — a free closure. A
count-against completion with NaN ranked below every draw — needs an interval law on infinities that no file
supplies. Of the faithful readings this is the one that cannot flatter: an undefined ruler never supports. A bare
NOT SUPPORTED on a gate whose refusals sit on too few assets — reads as evidence against the gate when the ruler
could not have said yes; the REFUSAL SPREAD qualifier says so, and its rule is fixed here, before the refused
cohort is seen (OD-16).
FAILS-IF: `F-BOOT [EMPTY-ARM]` (at `TC12-ENV.score-build`, synthetic arms) is RED when a planted kept arm emptied on
one asset reads anything but NOT SUPPORTED · PANEL INCOMPLETE, when a zero-row scored arm reads anything but NOT
SUPPORTED · EMPTY BOOK, or when a row with (c) true carries `p_den ≠ N_BOOT + 1`; planted mutation: clause (c)
removed from the rule (the planted arm must then be caught reading on a denominator below B + 1). The REFUSAL
SPREAD is held by `F-VERDICT [CASES]` (L-X.8).

**L-X.8 THE VERDICT LAW** — "bar = 0.10 ÷ m per family" (:9); "NOT SUPPORTED if the through-tick book fails the bar"
(:104)
READING:
- **`SUPPORTED` iff (a) `lo > 0` (the 5th percentile of the B draws, strictly) AND (b) `p ≤ bar_f` (exact, L-X.6)
  AND (c) PANEL COMPLETE (L-X.7); else `NOT SUPPORTED`.** Evaluated at the seed of record on the scored arm. Two
  laws sit on top, and each can only take `SUPPORTED` away or choose among the failure words: on a two-sample row,
  L-X.7's REFUSAL SPREAD (decided on counts: with `z ≥ bar_f` the word is NOT SUPPORTED); on P-SCALP-3, the
  contract's pre-named kill (L-X.9). No other row adds anything.
- This is a named reading: the contract names a bar and not a verdict law. (a) is the lineage's law, (b) the
  family's multiplicity bar, joined as TC11 L-1.4 and X LX-1.2 join them and as O-22 rules.
- **Stated before the look.** Which clause binds follows from B, `_ci_from`'s lower level and the bar, and is
  computed by the scorer and printed per family (`F-VERDICT [IMPLIED]` enumerates `k = 0..B`, it types nothing):
  at the two m = 2 families the clauses differ by one draw, (b) being the stricter; at the m = 1 SCALPER family
  clause (a) implies clause (b), so the bar is on record and does not decide, and P-SCALP-3's bar cell reads
  "`<q>` (not binding at m = 1; decided at the 5th percentile, clause (a))" — X's filed wording with q read from
  the contract.
- **The rival is printed, deciding nothing:** the literal bar alone, `p ≤ bar_f` (leaf `literal_bar`, L-X.14).
- **Seed stability, on all five rows.** `stable_across_seeds` and the flag `SEED-FRAGILE` (L-X.14) are defined on
  `C(scored)` = (a) ∧ (b) ∧ (c) of the scored arm, at the two seeds and on the exact enumeration.
  `stable_across_seeds` is the boolean "`C(scored)` at the seed of record equals `C(scored)` at the sensitivity
  seed"; the sensitivity seed's word is never filed. P-SCALP-3 also files `fill_ladder.<book>.C_sens`,
  `one_asset.D_sens` and `word_stable_across_seeds` (L-X.9's table evaluated on the sensitivity-seed tuple equals
  the word of record); a book that is `U` is `U` at both seeds, being decided on counts.
- **The size of the rule is stated on every row** (L-X.14's size footnote and `size_measured`): with five clusters
  the percentile bootstrap is anti-conservative, and each row prints the figure of its own ruler.
SOURCE: `research_outputs/tierc11/LEANS.md:114-121`; `x_rec/tierc11x/LEANS_X.md:657-685` (the reading, its
consequences at m = 2 and m = 1, `:668-672`), `:675-678` (why (a) is kept at m = 1);
`x_rec/scripts/tc11x_score.py:141` (`SFP_BAR_CELL`), `:209-218` (`literal_bar`); O-22;
`scout/U7_registrations_scoring.md` §2.1, R2.
RIVALS: `p ≤ bar` alone — looser at m = 1 (it would decide at the 10th percentile); printed as a column. CI-only
(TC10's form) — drops the family bar the contract names.
FAILS-IF: `F-VERDICT [CASES]` is RED when any fixture-typed case (a synthetic draw set, a family bar, panel counts
and — for a gate — refused counts per asset) maps to another word or qualifier set than the fixture's own table;
the cases include a synthetic gate refusing on two of five assets, which must read NOT SUPPORTED and carry the
REFUSALS qualifier whatever its draws. `F-VERDICT [IMPLIED]` is RED when the binding clause printed per family is
not the one the fixture's enumeration of `k = 0..B` gives. Planted mutations, each in a shadow copy of the rule: (i)
an ADMISSION row scored at the SCALPER's bar (detector `BAR-OF-FAMILY`); (ii) the m = 1 rule with clause (a)
removed, fed a draw set with `lo < 0` and `p` between the two clauses' limits (the mutant reads SUPPORTED where the
table reads NOT SUPPORTED → RED); (iii) the REFUSAL SPREAD removed, fed the two-of-five gate with an all-positive
synthetic draw set (the mutant reads SUPPORTED → RED).

**L-X.9 THE VERDICT VOCABULARY, AND THE SCALPER'S PRE-NAMED KILL** — "PRE-NAMED KILL: NOT SUPPORTED if the
through-tick book fails the bar; CLOSED FOR GOOD if it fails under DEEP too; CLOSED if it clears only under TOUCH
(the fill-sensitivity row is part of the verdict text); one-asset dependence read by LOAO 3/5 and the single-trade
share." (:104-106)
SEAM SETTLEMENTS (`review/SEAM_PASS.json`, 2026-10-09 — part of this reading; each line governs where the text below is silent or differs):
- [seam 61] the filed `verdict_rule` of P-SCALP-3 governs the scorer's verdict text, which prints: each fill book's state C / F / U, the booleans `fails_under_deep_too` and `clears_only_under_touch`, both fixed sentences, `licence_at_maker_pin` beside the licence word, and the adverse-selection sentence beside the cost twins (L-S.28).
- [seam 42] CANON-01's ban on 're-score' is scoped to cell TEMPLATES and LABELS; the refile qualifier `RE-SCORED AFTER <id>` is a scorer qualifier, never a label and never in a registry payload, so no scan of payloads or label fields can meet it.
READING:
- **Five words, exhaustive.** `verdict_of_record` ∈ { `SUPPORTED` · `NOT SUPPORTED` · `NOT SUPPORTED — CLOSED` ·
  `NOT SUPPORTED — CLOSED FOR GOOD` · `CLOSED BY PRECONDITION` }. The scalper's two closure words (`CLOSED`,
  `CLOSED FOR GOOD`) exist on P-SCALP-3 only. They are always printed behind `NOT SUPPORTED — `, so a closure can
  never be read without the failure it rests on, and the bare word `CLOSED` never stands as a verdict.
- **Qualifiers are not words.** They qualify a cell and are filed in `qualifiers[]`. The closed list: `FILL-SENSITIVE
  (does not clear under DEEP)` · `FILL-SENSITIVE (DEEP PANEL INCOMPLETE)` · `LOAO BELOW THE LINE (k/N above; passing
  when dropped: <assets>; failing when dropped: <assets>)` · `PANEL INCOMPLETE (<asset> holds no <arm> row)` · `EMPTY
  BOOK` · `TICK PANEL INCOMPLETE — closure not ruled` · `DEEP PANEL INCOMPLETE — closure not ruled` · `(clears only
  under TOUCH)` · `TOUCH PANEL INCOMPLETE — "for good" not ruled` · `TWO-SAMPLE-PREMISE` · `REFUSALS ON a/N ASSETS —
  the ruler cannot clear (P(draw ≡ 0) = z ≥ bar)` (L-X.7) · "on per-campaign expectancy only; the gate forfeits +X R
  total" (L-X.5) · "CI wholly below zero" (L-X.6) · `SEED-FRAGILE` · `TIME-CLUSTER FRAGILE` · `VERDICT RESTS ON OPEN
  MARKS` (L-X.14) · `LICENCE EDGE ≤ 0 AT THE PINNED MAKER RATE (X assumed <x> bps round trip; pinned <y>)`
  (P-SCALP-3 only, L-X.14) · `RE-SCORED AFTER <id>` · `REBUILT AFTER FIRST BUILD (AP-n)` (L-X.27). `HALT` and
  `ABSENT` are scorer statuses, never verdicts.
- **P-SCALP-3's table.** For each fill book X ∈ {TOUCH, TICK, DEEP}, at the seed of record and the SCALPER bar —
  the same ruler, seed, B and bar on all three: `U(X)` = X is not PANEL COMPLETE (its ruler is undefined; an EMPTY
  BOOK is the limiting case); `C(X)` = PANEL COMPLETE and clauses (a) ∧ (b) hold; `F(X)` = PANEL COMPLETE and (a) or
  (b) fails. Exactly one of the three holds. `D` = fewer than `above_half_bar(N)` leave-one-asset-out panels of the
  TICK book exclude zero from above (L-X.11). **A closure word needs a MEASURED failure:** "fails the bar" is
  `F(X)`, and a book whose ruler is undefined is not a failed book (OD-13). The ten cases partition every outcome:

  | TICK | D | DEEP | TOUCH | `verdict_of_record` | qualifier |
  |---|---|---|---|---|---|
  | C | false | C | any | `SUPPORTED` | — |
  | C | false | F | any | `SUPPORTED` | `FILL-SENSITIVE (does not clear under DEEP)` |
  | C | false | U | any | `SUPPORTED` | `FILL-SENSITIVE (DEEP PANEL INCOMPLETE)` |
  | C | true | any | any | `NOT SUPPORTED` | `LOAO BELOW THE LINE (k/N above; passing when dropped: <assets>; failing when dropped: <assets>)` |
  | U | any | any | any | `NOT SUPPORTED` | `PANEL INCOMPLETE (…)` / `EMPTY BOOK` and `TICK PANEL INCOMPLETE — closure not ruled` |
  | F | any | C | any | `NOT SUPPORTED` | — |
  | F | any | U | any | `NOT SUPPORTED` | `DEEP PANEL INCOMPLETE — closure not ruled` |
  | F | any | F | C | `NOT SUPPORTED — CLOSED` | `(clears only under TOUCH)` |
  | F | any | F | U | `NOT SUPPORTED — CLOSED` | `TOUCH PANEL INCOMPLETE — "for good" not ruled` |
  | F | any | F | F | `NOT SUPPORTED — CLOSED FOR GOOD` | — |

- Why the rows F · F · C and F · F · F split that way: "fails under DEEP too" and "clears only under TOUCH" both
  hold when TICK and DEEP fail and TOUCH clears; the clause that names that event exactly ("only under TOUCH")
  governs it, and "FOR GOOD" is left for the book with a MEASURED failure under every fill model. Every clause of
  the kill then has a live, disjoint event. Both clause truths are printed (the two booleans below), and the choice
  between the two words in that cell is listed for the operator (OPEN TO OPERATOR 7).
- **One test.** TOUCH and DEEP are ruled at the family bar and can never produce `SUPPORTED`; only the TICK book
  can. m stays 1 and one test is spent. The two twins are the contract's "fill-sensitivity row": they are arms of
  kind `ladder` (L-X.24), arms a registered row's `verdict_rule` reads and therefore on L-0.16's
  `REGISTERED_TABLES_T`, and their states are filed inside the row. The fill-sensitivity row opens with the fixed
  sentence: "TOUCH and DEEP are fill-model twins, not tests: they are ruled at the family bar without a test of
  their own and can only qualify a SUPPORTED cell or choose among the failure words; an interval that excludes zero
  on either is not a result."
- **The verdict text of P-SCALP-3** = its cell (word, qualifiers, label per L-X.13) followed, in this order, by:
  1. the fill-sensitivity row — the fixed sentence above; then per fill rule `n`, point, interval, `p_num/p_den`
     and the state (`C` / `F` / `U`); then the two booleans `fails_under_deep_too = F(TICK) ∧ F(DEEP)` and
     `clears_only_under_touch = F(TICK) ∧ F(DEEP) ∧ C(TOUCH)`, both also filed in `SCORES.json rows[].fill_ladder`;
  2. the LOAO line `k/N` with its bar and the fixed sentence: "the contract reads one-asset dependence by this line
     (:106); a panel that fails when an asset is DROPPED leans on that asset, a panel that fails while an asset is
     KEPT is dragged by it";
  3. the single-trade share of record (L-X.12);
  4. the per-order ladder counts of the TICK ledger and, where the three books' own n are not ordered, the line
     `BOOK-N-NOT-MONOTONE` (L-X.24);
  5. the collared leaf `licence_at_maker_pin`, under its own label and L-0.16's inline collar string (L-X.14);
  6. the lines every row carries under its cell (L-X.13): `disclosures[]`, `superseded[]`, the size footnote.
- What a closure forbids afterwards is L-S's text and the ledger append's; this section fixes only the word and
  its condition.
SOURCE: contract :93-96 (the three fill rules), :104-106; `scripts/tierc11_score.py:1160-1167`;
`scripts/tierc11_registrations.py:38-39` and `scripts/tierc11_score.py:262-263` (the collar the ladder arms are
exempt from); `x_rec/tierc11x/LEANS_X.md:695-696` (a single strongly negative asset fails every leave-out panel
that contains it — why the LOAO qualifier names both lists); `research_outputs/tierc12/ORCHESTRATOR_RULINGS.md:220-223`
(O-32: the LOAO kill and the per-order ladder stand); `scout/U7_registrations_scoring.md` §2.20, R11, R12.
RIVALS: (i) `CLOSED FOR GOOD` whenever TICK and DEEP both fail, whatever TOUCH reads — the literal order of the two
clauses; not the default, because it leaves the contract's CLOSED clause with no event; it is the operator's to
name (OPEN TO OPERATOR 7). (ii) One-asset dependence as a printed qualifier on a `SUPPORTED` cell (LOAO deciding
nothing, as on every earlier tier) — the clause sits inside "PRE-NAMED KILL", so the two readings are equally
faithful, and the one taken is the one that cannot flatter: a book below the LOAO line does not read SUPPORTED
(O-32). (iii) Twins as ordinary Tier-E arms — the contract makes them part of the verdict text. (iv) An undefined
ladder book counted as a failed one (`not C(X)`) — not taken: a permanent closure would then rest on a book with no
row on one asset rather than on an interval (OD-13). (v) The qualifier worded `ONE-ASSET DEPENDENT` — not taken: the
line cannot tell a result carried by one asset from a book dragged by one, so the qualifier states what was
measured and lists both sets of assets.
FAILS-IF: `F-VERDICT [LADDER]` (at `TC12-ENV.score-build`) is RED when any member of the product set (TICK ∈ {C, F,
U}) × (D ∈ {true, false}) × (DEEP ∈ {C, F, U}) × (TOUCH ∈ {C, F, U}) — every combination, enumerated by the fixture
— maps to another word or qualifier than the table's, or either boolean differs from its definition; planted
mutations, each in a shadow copy of the rule: TOUCH and DEEP swapped; the D column dropped; a closure word produced
on a U book; a `SUPPORTED` produced with TICK not C.

**L-X.10 CLOSED BY PRECONDITION** — "a registration closed by precondition spends no test" (:9)
READING:
- A registration's `preconditions` field is written in L-X.18's field grammar: the bare word `none` (optionally
  followed by commentary that is never evaluated), or a list of items `{record: <path>, certified_by: <progress
  record> <key>, selector: <selector>, required: <"string" | contains "string" | true>}`. An item is MET iff the
  selected leaf equals the string, or the selected list holds the string, or the selected leaf is the JSON `true`.
  A record built after the filing is named by path and by the progress record that certifies its sha; every reader
  asserts the file's sha equals the certified one before use. None is a statistic of the row's own book.
- On the filed specs every item reads L-V's `va/VA_MIRROR.json`, certified by `progress/TC12-V.json`: P-SFP-VA-1
  carries two items (the 4h taker licence word of its scoring era, and membership of the licence set); **P-SCALP-3
  carries ONE — the mirrored licence word of the 1h maker holdout row — and nothing else** (O-17, OD-12); P-ADM-1,
  P-BRD-1 and P-DIR-1 read `none`. No item reads a fee file, and no item compares a number: the licence edge
  re-expressed at Stage D's pinned maker rate is PRINTED beside the word as the collared leaf `licence_at_maker_pin`
  (L-X.14) and decides nothing (O-19).
- The owning stage evaluates the items BEFORE building any arm. If any item is not met it writes
  `regbooks/<ID>/STATUS.json` (through `tierc12_regbook.write_status`) with `status = "CLOSED_BY_PRECONDITION"`, the
  `reason`, `arms = []`, and each item as `{record, certified_by, selector, required, found, met}` — and nothing
  else: no parquet, no sidecar, no manifest, no number of the book (O-22).
- The scorer re-evaluates every item itself from the same record. Builder and scorer disagreeing is HALT
  `PRECONDITION-MISMATCH`. Not met: `verdict_of_record = "CLOSED BY PRECONDITION"`, cell `CLOSED BY PRECONDITION
  (<record>#<selector> reads <found>; required <required>) — no number · no test spent`, every numeric leaf null,
  `spent_test = false`, no ruler called, the label filed in its own field and absent from the cell (a label
  qualifies a verdict; none is computed).
- A CLOSED regbook directory holding any arm file is HALT `CLOSED-HAS-ARM`.
- A fixture whose population is the book of a closed registration runs its synthetic legs unchanged and, for each
  real-book leg, prints `CLOSED-NO-BOOK <id>` and asserts from files that this STATUS says `CLOSED_BY_PRECONDITION`
  and lists no arm (L-0.14; a PASS, not a fourth leg state).
- The items' text is the owners' (L-R, L-S), in the grammar above. On the records as filed no item fails (V3 HALTs
  the tier on a mirror disagreement), so F-FAM proves the law on a planted family.
SOURCE: `scripts/tierc11_score.py:1813-1827` (the closed row), `:290` (`PRECONDITION_LENS`);
`research_outputs/tierc11/regbooks/P-SCALP-2/STATUS.json` (the filed form); `x_rec/tierc11x/registrations/SCORED_X.json
rows[2]` (`number_free true`, `test_spent false`, `cell_text "CLOSED BY R2 (1h: FAIL)"`); O-17, O-19, O-22.
RIVALS: build the book of a closed row and print it collared (X's departure) — O-22 rules STATUS only. A second,
closing item on a re-derived licence edge — not taken: the mirror reads and never recomputes (O-17), a difference
in the maker rate is printed beside the word (O-19), and a row closed that way would spend no test (OD-12).
FAILS-IF: `F-FAM [PLANTED]` (L-X.15) is RED when the planted closed row carries a number, an arm or a spent test, or
a ruler runs for it; planted mutations: a `point` planted on the closed row → `CLOSED-NUMBER`; a `scored.parquet`
planted in the closed regbook → `CLOSED-HAS-ARM`; builder and scorer fed records that disagree →
`PRECONDITION-MISMATCH`. The grammar is held at filing by `F-REG [VERIFIER]` (detector `PRECOND-GRAMMAR`, L-X.22).

**L-X.11 "LOAO 3/5"** — "one-asset dependence read by LOAO 3/5 and the single-trade share" (:106)
READING:
- **Definition** (`TP.loao_n`'s law, mirrored over frames as `tierc11_score.loao` mirrors it): for each asset A of
  the DECLARED panel in sorted order, drop A from every arm and re-run the SAME ruler as the headline (vs zero:
  `cluster_boot`; two-sample: `cluster_boot_diff` of kept-minus-A against base-minus-A) with the same seed and B.
  A panel "excludes above" iff its `lo > 0` (clause (a) alone; no bar on a panel) and "excludes below" iff its
  `hi < 0`. A panel under `loao_n`'s own floors — too few rows or too few clusters in an arm, the literals at
  `scripts/tierc10_panel.py:1286`, `:1295`, mirrored and held equal by F-SCORE-ANCHOR — is "too few clusters" and
  counts AGAINST. `N = len(panel)` always.
- **The line** reads `k/N above[, j/N BELOW]` with `k` = panels excluding above; it clears iff `k ≥
  above_half_bar(N) = ceil((N + 1) / 2)`. The contract's "3/5" is the pin `loao.line` (:106, regex `LOAO
  (\d+)/(\d+)`, two capture groups, a tuple of two ints) and is asserted equal to `(above_half_bar(N), N)` for the
  five home assets. BELOW panels never count toward the line.
- **Seed.** The seed of record, passed explicitly (`TP.loao_n`'s default is TC10's seed); the sensitivity seed's
  table is printed beside, and on P-SCALP-3 it gives `one_asset.D_sens` (L-X.8).
- **A declared asset with no trade** reproduces the headline when dropped. The lineage's line counts it; the count
  excluding such panels (`above_excl_zero_campaign`) is printed beside.
- **What it decides.** On P-ADM-1, P-BRD-1, P-DIR-1 and P-SFP-VA-1: nothing — printed beside under the collar. On
  P-SCALP-3, and only there, the contract's kill names it: `D` (L-X.9) is true iff `above_excl_zero_campaign <
  above_half_bar(N)` on the TICK book at the seed of record. The excluding count is the one used because a panel
  that merely reproduces the headline is no evidence of breadth. (Where `D` can change the word, `C(TICK)` holds,
  clause (c) leaves no zero-trade asset, and the two counts coincide; the excluding count is named so the rule
  reads the same on any book.)
- **What the line cannot tell apart, and how it is worded.** A book CARRIED by one asset fails the panel that drops
  it; a book DRAGGED by one losing asset fails every panel that keeps it and passes only the one that drops it.
  Both read below the line. The qualifier therefore states what was measured — `LOAO BELOW THE LINE (k/N above;
  passing when dropped: <assets>; failing when dropped: <assets>)`, the first list holding the assets whose
  leave-out panel excludes above and the second the rest of the declared panel — and the verdict text carries
  L-X.9's fixed sentence. The rule for `D` and the word are as stated above.
SOURCE: `scripts/tierc10_panel.py:1193-1199` (`above_half_bar`), `:1234-1339` (`loao_n`; `:1241-1242`, `:1316-1338`);
`scripts/tierc11_score.py:1009-1048` (`loao` over frames); `research_outputs/tierc11/LEANS.md:118`;
`x_rec/tierc11x/LEANS_X.md:695-696`, `:719-720`; contract :106.
RIVALS: LOAO deciding nothing on P-SCALP-3 too (L-X.9 rival ii). The declared-panel count `k` for the kill — it can
credit a panel that is the headline itself.
FAILS-IF: `F-SCORE-ANCHOR [LOAO]` (at `TC12-ENV.score-build`) is RED unless the mirror on TC11's filed P-AGE-1 arms
reproduces `SCORES.json rows[registration=P-AGE-1].stats.loao` (line, bar, per panel); planted mutations: a BELOW
panel counted toward the line; `N` taken as the panels that bootstrapped; the panels ruled vs zero under a
two-sample headline. The two lists of the qualifier are held by `F-VERDICT [LADDER]`'s D cases (L-X.9).

**L-X.12 THE SINGLE-TRADE SHARE** — "and the single-trade share" (:106)
READING:
- Two definitions are on disk. **Of record: TC11's SC-22 `concentration`**, the one written for two-sample and
  vs-zero rows, which are the only rulers TC12 has: the top trade = the scored arm's largest `|net_r|` (ties → the
  first in `(symbol, entry_ms)` order); `top_share` = its signed `net_r` ÷ the scored arm's Σ `net_r` (`None` iff
  `|Σ| ≤` the constant at `scripts/tierc11_score.py:1108`); the point with it removed from every book holding its
  key; its asset's share of ΣR; the point without that asset; per-asset means (two-sample: per-asset Δ).
- **Printed beside: X's LX-X1.9 form** applied to the scored arm's `net_r`: `max|x| / |Σx|` with the arg-max key
  and `sum_ex_argmax = Σx − x_argmax`. X defined it on paired Δ; TC12 has no paired row, so on these rows it equals
  `|top_share|` and the scorer asserts that equality.
- **No threshold exists on either, in the contract or on file, and none is typed.** Both are printed on all five
  rows; on P-SCALP-3 the share of record is part of the verdict text; neither decides a word (O-32; OPEN TO
  OPERATOR 1).
SOURCE: `scripts/tierc11_score.py:1076-1118` [read here]; `research_outputs/tierc11/scores/SCORES.json
rows[registration=P-AGE-1].concentration` (keys on file); `x_rec/tierc11x/LEANS_X.md:1019-1025`;
`x_rec/scripts/tc11x_score.py:437` (`harvest_rival`); `scout/U7_registrations_scoring.md` §1.4.
RIVALS: X's form of record — defined on paired Δ, which no TC12 row has. A typed cut (a share above one half kills)
— a number no file supplies.
FAILS-IF: `F-SCORE-ANCHOR [CONCENTRATION]` (at `TC12-ENV.score-build`) is RED unless the mirror reproduces
`SCORES.json rows[registration=P-AGE-1].concentration` on TC11's filed arms, or when `share_x ≠ |top_share|` on a
row; planted mutation: the top trade taken by `net_r` instead of `|net_r|`.

**L-X.13 THE IN-SAMPLE LABELS IN THE VERDICT TEXT** — "Label pre_seen …" (:54-55); "Label: direction informed by …"
(:58-59, :67); "§0 VERDICTS FIRST: the five rows with their labels" (:126-127); "in-sample labels carried" (:130)
SEAM SETTLEMENTS (`review/SEAM_PASS.json`, 2026-10-09 — part of this reading; each line governs where the text below is silent or differs):
- [seam 52] CANON-01's ban on 're-score' is scoped to cell TEMPLATES and LABELS; the refile qualifier `RE-SCORED AFTER <id>` is a scorer qualifier, never a label and never in a registry payload, so no scan of payloads or label fields can meet it.
- [seam 44] under P-BRD-1's cell the key overlap prints the cell COUNTS (`n`) of `stage_g/g_brd17.parquet` alone — no sum, no mean.
READING:
- Label keys are `pre_seen` and `selection_hazard`, each filed in the spec's `labels` field as one sub-bullet `<key>
  — tag: <TAG|none>; label: <label>; text: "<text>"; items: <items>` (L-X.18's grammar). Per O-23 as amended by
  O-30:

  | registration | label key | tag | label | cell template (bytes of record; the `<verdict>` slot takes the word and its qualifiers) |
  |---|---|---|---|---|
  | P-ADM-1 | `pre_seen` | `none` | `IN-SAMPLE RE-SCORE, NOT CONFIRMATORY` | `<verdict> — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (pre_seen: <clause>)` |
  | P-BRD-1 | `selection_hazard` | `direction-informed` | `NOT CONFIRMATORY` | `<verdict> — NOT CONFIRMATORY (selection_hazard: direction-informed)` · D-1 printed directly under the cell |
  | P-DIR-1 | `selection_hazard` | `direction-informed` | `NOT CONFIRMATORY` | `<verdict> — NOT CONFIRMATORY (selection_hazard: direction-informed)` |
  | P-SFP-VA-1 | `pre_seen` | `KIN-SEEN` | `NOT CONFIRMATORY` | `<verdict> — NOT CONFIRMATORY (pre_seen · KIN-SEEN: X3 printed value-area swing-failure outcomes on these bars)` |
  | P-SCALP-3 | `pre_seen` | `KIN-SEEN` | `NOT CONFIRMATORY` | `<verdict> — NOT CONFIRMATORY (pre_seen · KIN-SEEN: X3 printed value-area swing-failure outcomes on these bars)` |

- Three templates, keyed by registration id (OD-1, O-30). RE-SCORE is printed only where the kept book's mean is on
  file (P-ADM-1). A label must be true.
- The dash is U+2014 with one space each side; the dot is U+00B7; `direction-informed` is lower case (O-30's
  bytes). "re-score" (any case) appears in P-ADM-1's template and label alone.
- `<clause>` exists on P-ADM-1 ONLY: its `pre_seen.text` up to the first top-level `;` (TC11 SC-8) — the file and
  cell under `research_outputs/tierc11/stage_g/`. The KIN-SEEN and selection_hazard templates have no slot.
- The owners' long `pre_seen.text` of P-SFP-VA-1 and P-SCALP-3 stays as the label's `text` and `items` and is
  printed UNDER the cell (in the row's `disclosures[]`) with D-2 and D-3 — for P-SCALP-3 including its sentence that
  the 1h maker licence row was measured on these same holdout bars.
- P-BRD-1's cell is followed by disclosure D-1 (`research_outputs/tierc12/DISCLOSURES.md`), carried in the row's
  `disclosures[]` and printed directly under the cell wherever the cell is printed.
- **Key overlaps under the two `selection_hazard` cells (counts only, no outcome).** A label that cites a filed
  cohort outcome is sufficient only if the reader can see how much of the row's refused set IS that cohort. Under
  P-BRD-1, below D-1: the six cells of `stage_g/g_brd17.parquet` (the agreement of the 17-asset twin with the row
  of record; the scorer reads the columns `cell` and `n` and nothing else). Under P-DIR-1: `n_refused` and, of
  those, the number in TC11 R5's `EXP_COUNTER` and `EXP_ALIGNED` cells (the pivot state at the entry instant: a
  mirror of `align_of`, `scripts/tierc11_stage_r.py:1650-1661`, on `research_outputs/tierc11/stage_r/NEST_v6.parquet`,
  calibrated 4h), filed by `tierc12_stage_r_dir.py` in `stage_r/dir/build_manifest.json` under `r5_overlap`. The
  scorer reads both records at their certified shas, carries each as one line of the row's `disclosures[]`, and
  computes nothing on them. The leaf `arm__brd17` carries the note "outcome of this split seen at R0 (D-1)".
- **What stands under a cell, in this order.** The row's `disclosures[]` lines (the key-overlap line; D-1 on
  P-BRD-1; the long `pre_seen.text` with D-2 and D-3 on the two KIN-SEEN rows); its `superseded[]` lines (L-X.27);
  and last its `size_footnote` (L-X.14). The row's `verdict_text` is the cell followed by those lines; P-SCALP-3
  inserts the lines of its kill between the cell and them (L-X.9).
- **Mechanics (X's `label_cell` law):** each filed `verdict_rule` carries exactly one substring `prints '<verdict>
  …'`, and that template equals this table's row FOR ITS REGISTRATION ID, byte for byte; HALT otherwise (detector
  `TEMPLATE`, at filing and in the scorer). The scorer builds the cell by substituting the word and its qualifiers
  into the template.
- The family bar applies unchanged to a labelled row; a labelled row is never cited as confirmation, in §0, in
  FAMILY.json or in the ledger append. A CLOSED BY PRECONDITION row prints no label in its cell (L-X.10).
SOURCE: `research_outputs/tierc12/ORCHESTRATOR_RULINGS.md:156-160` (O-23), `:210-214` (O-30: the three forms, byte
for byte); D-1, D-2, D-3, D-4; `x_rec/tierc11x/LEANS_X.md:728-737` (X's two templates), `:2468-2470` (the standing
pre_seen line); `x_rec/tierc11x/LEANS_X_AMENDMENTS.md:429-441` (AM-X18, tags on `selection_hazard`-only rows);
`x_rec/scripts/tc11x_score.py:316-321` (`label_cell`), `x_rec/scripts/tc11x_registrations.py:512-520`
(`honesty_prints`); `scripts/tierc11_score.py:560-578` (SC-8), `:1894-1900`; `scripts/tierc11_stage_r.py:1650-1661`
(`align_of`, read as text); contract :54-55, :58-59, :67.
RIVALS: TC11's single template on all five (prints "RE-SCORE" on four rows whose form or cohort was never scored).
The RE-SCORE template on the two lanes — not taken: O-30 (neither trade form was ever scored). Templates keyed on
the label key — not taken: P-ADM-1 and the two lanes carry the same key and different templates (OD-1). The
`selection_hazard` cells with no overlap count — not taken: if a refused set is mostly a cohort whose mean was
already printed, "direction-informed" would be true only by omission.
FAILS-IF: `F-REG [TEMPLATE]` is RED when a filed rule carries zero or two templates, or a template that is not its
registration's row of the table byte for byte; planted mutations: P-ADM-1's template rewritten to the
`selection_hazard` form → RED; P-SFP-VA-1's rewritten to the RE-SCORE form → RED; `DIRECTION-INFORMED` in capitals
on P-DIR-1 → RED. F-S0-FIVE (L-X.28) is RED when a label, D-1 under P-BRD-1's cell, or either key-overlap line is
absent; planted mutation: the `r5_overlap` line removed from a copy of `S0_VERDICTS.md`.

**L-X.14 THE BESIDE-PRINTS EVERY ROW CARRIES (Tier-E)** — ""a SELECTION, not a result" on every non-registered
table" (:7); "no promotion from any Tier-E table" (:133)
READING:
- Every leaf below carries L-0.16's collar (`tier`, `selection_not_a_result`, `gates`, `would_read_ci_only` — one
  of TC11's four readings — `m_looks_this_table`, `m_note`, `promotable = False`), no verdict word, and no key
  matching `verdict|clears|spent_test` (L-0.16's pattern, widened from TC11's `verdict|clears_bar|spent_test` so
  that no leaf can carry a boolean named for a cleared bar). The scorer DERIVES the common leaves from the arms of
  record; a stage ships an arm only where another book is needed (its own `tierE__<slug>` arms, named in its
  spec's `arms` and `disclosed_beside` and listed in its STATUS), and the scorer writes exactly one leaf
  `arm__<slug>` for each.
- **What L-X contributes to L-0.16's `REGISTERED_TABLES_T`** (collar-exempt): `scores/SCORES.json rows`,
  `scores/FAMILY.json`, `scores/S0_VERDICTS.md`'s table; each regbook's `scored` and `base` arm; P-SCALP-3's
  `ladder__touch` and `ladder__deep` arms (the arms a registered row's `verdict_rule` reads, L-0.16). Everything
  else this section writes is collared: every `tierE__*` and `strip` arm, `SCORES.json beside`, `scores/BESIDE.md`,
  `DRAWS.parquet`.

  | slug | what the scorer computes |
  |---|---|
  | `seed_sens` | the row's ruler at the sensitivity seed |
  | `haircut`, `haircut_sens` | the row's ruler on `haircut_net_r` (charter slippage on the taker legs of the record) at both seeds |
  | `taker_twin` | the row's ruler on `taker_twin_net_r`; on an all-taker arm the leaf reads `IDENTICAL TO THE RECORD (every leg taker)` and repeats no number |
  | `taker_twin_haircut` | the row's ruler on `taker_twin_haircut_net_r` (charter slippage on every fill of the all-taker twin — the harshest cost row); on an all-taker arm it reads `IDENTICAL TO haircut` |
  | `tuning_slice`, `holdout_slice` | the row's ruler on the rows of each era (`era`, L-X.24), in every arm the ruler reads. P-SCALP-3, whose era of record is the holdout: `tuning_slice` is computed on the tuning rows of `tierE__full_corridor` (the one slice taken on a Tier-E arm) and `holdout_slice` reads `IDENTICAL TO THE RECORD (era of record)` |
  | `loao`, `loao_sens` | L-X.11's table at both seeds |
  | `concentration`, `share_x` | L-X.12, both definitions |
  | `literal_bar` | the rival of L-X.8: `literal_bar_p`, `literal_bar_pctile` (the (100 · bar)-th percentile of the record's draws) and `would_read_ci_only`; no boolean |
  | `exact` | the enumerated cluster bootstrap, with `u` = the number of clusters: every composition `k` of `u` picks over the sorted clusters, weight `u! / Π k_a!` of `u^u`; vs zero the atom is `Σ k_a S_a / Σ k_a n_a` (X's `exact_cluster`); two-sample it is that ratio on the kept arm minus the same ratio on the base arm, over the union's clusters; `p_exact`, `lo_exact`, `hi_exact` decided in integers at the levels X fixes (`CI_LO_Q`, `CI_HI_Q`) |
  | `month_block` | the row's ruler with the cluster = the UTC calendar month of the entry close, same seed and B |
  | `drop_open` | the row's ruler with every `exit_reason == "corridor_end"` row removed from every arm; `n_open_at_pin` per asset |
  | `strip` | the forward strip arm: `n` per arm (the strip sidecar's `n_by_arm`, with `same_rows_as` where an arm is another's walk) and one pointer (path, file sha, book sha). NO statistic — no mean, no sum, no interval (O-9, OD-14) |
  | `arm__<slug>` — one per `tierE__<slug>` arm the row's STATUS lists | the arm's sidecar `ruler` at the seed of record with `N_BOOT` draws (two_sample: the arm against that registration's `base`; vs_zero: the arm alone), clusters = the sidecar's `panel`; filed `n`, `n_base` (two-sample), `n_clusters`, `point`, `lo`, `hi`, `n_draws_finite`, `would_read_ci_only`, `seed`, `draws_sha256`. No p, no bar, no sensitivity seed, no slice, no LOAO, no verdict word |
  | `licence_at_maker_pin` (P-SCALP-3 only) | no ruler: `{maker_bps_side, round_trip_bps, x_toll_bps, differs_from_x_assumption, edge_net_h20_at_pin}`, defined below |

- **The common slugs** are `seed_sens`, `haircut`, `haircut_sens`, `taker_twin`, `taker_twin_haircut`,
  `tuning_slice`, `holdout_slice`, `loao`, `loao_sens`, `concentration`, `share_x`, `literal_bar`, `exact`,
  `month_block`, `drop_open`, `strip`; P-SCALP-3 adds `licence_at_maker_pin`. **The declared beside set of a row** =
  the common slugs ∪ {`arm__<slug>` for exactly the Tier-E arms in its STATUS}; an arm without a leaf, or a leaf
  without an arm, is F-GRID RED. P-SCALP-3's full-corridor view IS `arm__full_corridor`. A `strip` arm gets the
  `strip` leaf only. No leaf exists for a re-ride (a disclosure of counts and diff rows, L-G.18, L-R.5) and none
  for a table attached to no registered row (L-R.30's take-profit venue is descriptive).
- **`licence_at_maker_pin` — printed beside the licence word, deciding nothing (O-19, OD-12).** `maker_bps_side` is
  read from `E.fees()`, one maker rate over the five home stems asserted; `round_trip_bps = 2 · maker_bps_side`;
  `x_toll_bps`, `edge_median_term_h20` and `edge_toll_atr` are the values `va/VA_MIRROR.json` QUOTES from X's row at
  `licence["1h|maker"].by_era["holdout"]` (`toll_bps` and the two edge columns; TC12 computes no number in that
  file); `differs_from_x_assumption` is Stage D's flag `data/fee_schedule.json maker_pin.differs_from_x_assumption`;
  `edge_net_h20_at_pin = round(edge_median_term_h20, ND) − round(edge_toll_atr × round_trip_bps / x_toll_bps, ND)`,
  `ND` = X's `pins.laws.round_nd` (`x_rec/tierc11x/va/build_manifest.json`). Where the pinned rate equals X's
  assumption the figure must equal the quoted `edge_net_h20`; if it does not, the LEAF is halted (`LICENCE-LEAF`,
  the Tier-E flag of L-X.27's exit word) and the row is untouched. The leaf carries no word, is labelled "a
  re-derivation of one leg from printed columns; not a licence", and is printed in P-SCALP-3's verdict text and in
  §0.3. If `edge_net_h20_at_pin ≤ 0` the cell carries the qualifier `LICENCE EDGE ≤ 0 AT THE PINNED
  MAKER RATE (X assumed <x> bps round trip; pinned <y>)`; the row is still built, scored, and spends its test.
  Closing the row on that figure is the operator's order, by name, before Stage D's fee capture (L-S's item).
- **Flags on the row, deciding nothing:** `SEED-FRAGILE` iff `C(scored)` (L-X.8) at either seed differs from the
  same conjunction on the exact enumeration (`lo_exact > 0 AND p_exact ≤ bar`, with clause (c)); `TIME-CLUSTER
  FRAGILE` iff the `month_block` `lo ≤ 0` while the record's `lo > 0`; `VERDICT RESTS ON OPEN MARKS` iff
  `C(scored)` on the `drop_open` twin differs from the record's (a boolean; the twin's word is never filed).
- **The five-cluster size footnote, on every row.** `size_footnote` is X's `SIZE_FOOTNOTE`, read by `ast` from
  `x_rec/scripts/tc11x_score.py`, printed on every one of the five rows (in `verdict_text` and as the last line
  under each §0 row) and in §1 beside the three bars. Each row also carries `size_measured {ruler, n_clusters,
  nominal, one_sided_size}` — the figure of ITS ruler and cluster count: `nominal` is the level the frozen rule
  decides at, `_ci_from`'s lower percentile (the same on all five rows; filed as the fraction one over X's
  `CI_LO_Q`), and `one_sided_size` is the share of synthetic exchangeable nulls on which the frozen rule (clauses
  (a) ∧ (b) at the row's family bar, on the exact enumeration) reads SUPPORTED. X's figure was measured for the
  one-sample form; the kept-versus-all form is measured here for the first time, so that X's sentence is never the
  only statement on a two-sample row.
- **Where `size_measured` comes from.** `F-VERDICT [SIZE]` (at `TC12-ENV.score-build`; no Naiad data, no outcome
  read) regenerates the size deterministically from the tier seed, separately for the two forms the rows use — vs
  zero on N clusters, and kept-versus-all on N clusters at a fixture-typed refusal share — for N = the home
  panel's size and every parsed family bar. Its generator is a mirror of X's `size_regen` extended to the second
  form: equal cluster sizes, iid standard-normal values, the exact weighted enumeration over compositions. The
  design's fixture-typed literals, printed in the transcript header (L-0.14): the number of nulls, X's
  `SIZE_N_NULL` (on file 20,000, `x_rec/scripts/tc11x_score_fixtures.py:174`); the rows per cluster, X's value in
  `size_regen` (on file 40, `:815`); and the refusal share, one half, each synthetic row refused independently by
  the leg's seeded stream (no file supplies a share; it is the fixture's commission and reads no book). A null in
  which a cluster keeps no row counts as not SUPPORTED (clause (c)). The suite files the figures as
  `research_outputs/tierc12/env/SIZE_MEASURED.json` (`design`, `seed`, and one entry per `(ruler, n_clusters,
  bar_exact)` with `one_sided_size` and `n_null`), an artifact of the `TC12-ENV.score-build` record written under
  the transcript's no-clobber law. The scorer copies the entry of the row's `(ruler, size of its declared panel,
  bar_exact)` from that file at its certified sha and computes nothing; the lookup depends on no book, and an
  absent entry is HALT `SIZE-ENTRY` (a build defect).
- `m_looks_this_table` = the number of intervals (`lo`, `hi` pairs) in `SCORES.json beside[]`, every LOAO panel
  counted; §1 prints the tier total over all collared tables beside the five tests.
SOURCE: `scripts/tierc11_score.py:1185-1203` (`stats_block`), `:258-263` (collar and TC11's forbidden-key pattern);
`x_rec/scripts/tc11x_score.py:136`, `:139-140` (`SIZE_FOOTNOTE`), `:221-255`, `:281-286`, `:289`;
`x_rec/scripts/tc11x_score_fixtures.py:173-174` (`SIZE_RANGE_TYPED`, `SIZE_N_NULL`), `:806-827` (`size_regen`; the
rows per cluster at `:815`); `x_rec/tierc11x/va/build_manifest.json` key `pins.laws.round_nd` [read here];
`x_rec/tierc11x/LEANS_X.md:675-678` (the measured one-sample size), `:686-718`, `:814-830`, `:1529-1531`,
`:1566-1569`; `x_rec/tierc11x/LEANS_X_AMENDMENTS.md:211-219` (AM-X10 items 2-5); O-9, O-13, O-17, O-19.
RIVALS: slices shipped by the stages — a second builder for the same rows. A two-arm enumeration left out — X's
`exact_cluster` is one-sample, and the Monte Carlo error of p is material at the two m = 2 bars
(`x_rec/tierc11x/LEANS_X.md:697`). A p, both seeds or LOAO on an owner-shipped twin — not taken: of the faithful
forms this one prints least that could be mistaken for a test. `clears_literal_bar` as a boolean — not taken: at
m = 1 it could read true beside a NOT SUPPORTED cell. X's footnote alone on the two-sample rows — not taken: it was
never measured on that form.
FAILS-IF: F-COLLAR `[scores]` is RED when a beside leaf lacks a collar key, carries a verdict word or a key matching
the forbidden pattern; F-GRID `[scores]` is RED when the written leaves are not the declared set per row, or
`m_looks_this_table` is not the fixture's own count of intervals; `F-VERDICT [SIZE]` is RED when a vs-zero figure
at the home panel's size lies outside X's typed range for that nominal (`SIZE_RANGE_TYPED`, read by `ast`), two
regenerations in fresh processes differ, or `env/SIZE_MEASURED.json` is not the leg's figures.
Planted mutations: a leaf dropped; a leaf written for an arm STATUS does not list; a `strip` leaf given a mean; a
`verdict` key planted in a leaf; a `clears_literal_bar` key planted in a leaf; an `arm__` leaf given a `p_num`; the
size rule's deciding level moved to the 10th percentile (X's sabotage — the figure must leave the range); a
`size_measured` bent on one row (F-S0-FIVE, L-X.28).

**L-X.15 F-FAM** — "F-FAM (m and bars printed per family; a precondition-closed row spends no test)" (:122-123)
READING: three blocks whose FID is exactly `F-FAM` (L-0.19's map), each with its named detectors, in
`scripts/tierc12_score_fixtures.py`.
- **`F-FAM [PLANTED]`** — hosted at `TC12-ENV.score-build` (transcript `env/FIXTURES_SCORE_BUILD.txt`), synthetic,
  before any book: a scratch filing built from a scratch contract carrying one header in the same grammar (a
  family of m = 2), with one BUILT row on a synthetic book (no Naiad data) and one row whose precondition item
  reads a planted record that fails. Expected: `tests_spent = 1`; the bar stays q ÷ 2; the closed row is
  number-free with cell `CLOSED BY PRECONDITION (…) — no number · no test spent`; a call counter proves no ruler
  ran for it.
- **`F-FAM [PARSE]`** (L-X.1) — hosted at TC12-SCORE (transcript `scores/FIXTURES_SCORE.txt`): the three families
  re-parsed by the fixture's own regex from the contract prefix and compared with the filing and with
  `scores/FAMILY.json`; prints family · stage · header line · m · bar · bar_exact · deciding rank.
- **`F-FAM [REAL]`** — hosted at TC12-SCORE: on the scored tier, each row's `family`, `m`, `bar_exact` are its
  family's; `tests_spent_f` = the rows of f with status BUILT and no HALT; `tests_spent_f ≤ m_f`; a row with
  `spent_test = false` has every numeric leaf null.
- The parse against the fixture-typed referee AT FILING is a different block, `F-FAM-PINS`, in the pins suite at
  TC12-REG (L-0.18); it is rolled after the contract's fixtures and is not one of F-FAM's blocks.
SOURCE: nearest code `scripts/tierc11_score_fixtures.py:1521-1535`, `:1630` (TC11's family leg on a planted family);
`x_rec/scripts/tc11x_score_fixtures.py:852`, `:1152-1154`, `:1281-1282`; no fixture named F-FAM exists in either tree
(`scout/U7_registrations_scoring.md` §1.10).
RIVALS: prove "spends no test" on a real row — none of the five can close on the records as filed. One block for
the three legs — not taken: a leg is one `prove` call and one transcript block (L-0.14), and the PLANTED leg must
be GREEN before any book exists.
FAILS-IF: `[PARSE]` is RED when a header's bar ≠ q ÷ m, or the fixture's parse differs from the filing or from
`FAMILY.json`; `[REAL]` when a family's count ≠ m, a row's bar is not its family's, tests spent ≠ the BUILT
un-halted rows, or a row that spent no test carries a number; `[PLANTED]` when the planted closed row carries a
number, an arm or a spent test, the planted bar moves, or a ruler runs for the closed row. Planted mutations, each
caught by its named detector: the planted bar recomputed as q ÷ (tests spent) → `M-LOOSENED`; the closed row
counted as spent → `TESTS-SPENT`; a `point` planted on the closed row → `CLOSED-NUMBER`; a `scored.parquet` planted
in the closed regbook → `CLOSED-HAS-ARM`; a row scored at another family's bar → `BAR-OF-FAMILY`; a header's bar
text changed in a scratch contract (`[PARSE]`) → `FAMILY-BAR`.

---------------------------------------------------------------------------------------------------------------
### B · The registration architecture

**L-X.16 THE CONTRACT IS PINNED BY ITS PREFIX** — "STEP Q: file this paste verbatim to
exchange/queue/2026-10-08_TC12_APOLLO.md (sha printed)" (:10); "Q1/Q2 … stamp TC11 BUILT and re-pin its registry
files" (:13)
READING: the prefix pin is L-0.1's law; this reading fixes its exact function, adds the TAIL law, and applies both
to the registry.
- `N_Q` and `S_Q` are read from `research_outputs/tierc12/progress/STEP_Q.json
  artifact_shas["exchange/queue/2026-10-08_TC12_APOLLO.md"]` (`bytes`, `sha256`; on file 12,209 B and `861d6050…`).
- Every reader of the contract (the filing, its verifier, the scorer, the close generator, `close_acts.sh` step 0)
  applies one function: `raw = read(path)`; HALT `CONTRACT-PREFIX` unless `len(raw) ≥ N_Q`, `sha256(raw[:N_Q]) ==
  S_Q` and `raw[N_Q − 1 : N_Q] == b"\n"`; HALT `CONTRACT-TAIL` unless `raw[N_Q:]` is empty or consists only of
  whole lines matching `^BUILT: \S.*$`, each ending in `\n`.
- `lines = raw[:N_Q].decode("utf-8").split("\n")`; every slice, every family parse and every line cite is cut from
  those lines. A `BUILT:` line appended later as the file's last line therefore moves no slice, no payload sha, no
  chain head and no verifier's result. A line inserted anywhere above byte `N_Q`, or any other change, HALTs.
- The whole-file sha at filing is recorded as `whole_file_sha256_at_filing` and compared by nothing afterwards.
  `PROGRESS.json` likewise names the contract by `{path, prefix_bytes, prefix_sha256}` (L-0.9), so TC12's own BUILT
  stamp (L-X.35) moves no byte of it.
SOURCE: `research_outputs/tierc12/progress/STEP_Q.json` (sha `8da374a7…1c27c`); the contract re-hashed [measured
here: 12,209 B, 137 `\n`, ends on `\n`]; `exchange/queue/README.md:8-12` (rule 6: "`BUILT: <artifact or commit>` on a
line of its own"); `scout/U1_rulings_close_state.md` §1.4, R-18 (a whole-file pin is what made TC11's stamp a
cascade); O-10.
RIVALS: pin the whole file (TC11, X) — the queue's own stamp then breaks every pin, which is the question the
contract's `"tc11-stamp"` ruling had to answer for TC11. Accept any tail — leaves the text open below the pin.
FAILS-IF: F-CONTRACT-PIN (the registry suite's block at TC12-REG, beside L-0.1's F-CONTRACT) is RED when a scratch
copy with `BUILT: x\n` appended changes any slice, payload sha, chain head or verifier finding; planted mutations:
one byte flipped inside the prefix (must HALT `CONTRACT-PREFIX`); the `BUILT:` line inserted under `RATIFIED` (must
HALT `CONTRACT-PREFIX`); a tail line `NOTE: x` (must HALT `CONTRACT-TAIL`).

**L-X.17 THE SLICE LAW AND THE VERIFIED LINE MAP** — "frozen texts" (:5)
READING:
- TC11's law, unchanged: `text_of_record = "\n".join(lines[a − 1 : b])` — 1-indexed, inclusive, leading whitespace
  kept, no trailing newline, UTF-8; `text_sha256 = sha256(text_of_record)`.
- Guards: a registration's slice must `lstrip().startswith(<id> + " ")` and contain `[<prior>%]`, the prior being
  parsed from the slice with `\[(\d+)%\]` and compared with the spec's.
- A slice may be filed (as a text, a context or a family header) only if it is a row of the plan's line map and its
  bytes hash to the map's sha. The map, verified on the filed bytes [measured here]:

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

- Filing order (`seq`) = ascending first text line: P-ADM-1, P-BRD-1, P-DIR-1, P-SFP-VA-1, P-SCALP-3. `P-ADM-1` also
  occurs on :108 (Stage L); only the slice beginning with the id is a text.
- Minimum `context_of_record` on every registration: LAWS (5-9) and its family header. Owners add theirs.
- An `external_context` item `{path, sha256, lines, text}` is cut by the same law from another pinned text (TC11's
  `stage_g/STAGE_G.md`, `x_rec/tierc11x/LEANS_X.md`), its file sha asserted first. The path may not be one of the
  files TC12's own close acts move (L-0.24's sets (a)-(f) and TC11's contract): no TC12 pin is a whole-file sha of
  such a path, and the filing HALTs `EXTERNAL-SLICE` on one.
SOURCE: `x_rec/tierc11x/REGISTRATION_PLAN.md:20-27` (the law, verified against TC11's own filing);
`scripts/tierc11_registrations.py:194-202`; `scout/U7_registrations_scoring.md` §1.11 (the same map, independently).
RIVALS: cite by quoted text instead of lines — no hash to verify. Cut from the live whole file — moved by a stamp.
FAILS-IF: `F-REG [SLICE]` is RED when any text, context or external slice does not re-cut from pinned bytes or its
sha differs from the map; planted mutations: one character edited in a filed `text_of_record` → `TEXT-SLICE`; an
`external_context` item cut from `scripts/tierc11_score.py` → `EXTERNAL-SLICE`.

**L-X.18 THE PLAN CARRIES THE SPECS VERBATIM** — "families declared by MECHANISM before the look" (:8)
READING:
- `research_outputs/tierc12/REGISTRATION_PLAN.md` is the design document the filing is cut from: §0 the slice law
  and L-X.17's map; §1 one table row per registration (`seq | registration | family | m | bar | prior | text lines |
  comparison | preconditions | labels`) and five blocks `### 1.k <id>`; §2 the keys of L-X.19; no outcome anywhere.
- Each §1.k block is the frozen LEANS's `### REGISTRATION SPEC · <id>` block byte for byte (from that heading to the
  next line beginning `### ` or `## `). The filing HALTs (detector PLAN==LEANS) on any difference.
- **Carry law** (X's `SPEC_CARRY_LAW`, mirrored from `carry_spec`): a spec block is fifteen top-level bullets
  `- **<field>:** <text>` in this order and with these names: `id`, `family`, `family_m`, `family_bar`, `prior`,
  `mechanism`, `population`, `arms`, `statistic`, `comparison`, `preconditions`, `verdict_rule`, `labels`,
  `disclosed_beside`, `failure_conditions`. A bullet's wrapped lines join with one space; one level of sub-bullets
  becomes a list; markdown is kept; a missing, extra, renamed or reordered field HALTs.
- `id`, `family`, `family_m`, `family_bar`, `prior` are checked against the contract parse (L-X.1, L-X.2, L-X.17)
  and filed as body keys; `verdict_rule` is filed as a body key; the other nine fields are the `operative_spec`.
- **FIELD GRAMMAR** — the fields the filer or the scorer machine-reads are written in ONE dialect; the five blocks
  are written to it, and the filing HALTs on any other form:
  1. **Checked fields** `id`, `family`, `family_m`, `family_bar`, `prior`: the value is the text up to the first
     space; anything after it is citation, kept in the plan and dropped from the body key. `prior` is digits only
     (`30`, not `30%`). HALT `SPEC-GRAMMAR` otherwise.
  2. **`preconditions`:** either the bare word `none`, optionally followed by ` — <commentary>` (never evaluated),
     or sub-bullets each of the form `{record: <path>, certified_by: <progress record> <key>, selector: <selector>,
     required: <"string" | contains "string" | true>}` optionally followed by ` — <commentary>`; HALT
     `PRECOND-GRAMMAR` otherwise. The separator is space, U+2014, space. No numeric comparator exists in the
     grammar: a precondition is never a number TC12 computes (L-X.10).
  3. **`arms`:** sub-bullets. Exactly one begins `` `scored` `` followed by a space (regex `` ^`scored`\s ``) and
     holds the whole construction of the scored arm; HALT `SPEC-GRAMMAR` unless exactly one. The others begin with
     their arm's name in backticks, or with `inputs pinned:` (the HALT-grade input pins — by certifying record,
     chain head or payload sha, never a whole-file sha of a file the close acts move, L-0.24), or with `VA columns
     read (declared for F-VA-PINS (e)):`, or are further sentences of the construction that do not match the
     selector. The filer checks the selector and nothing else in this field; the two prefixed sub-bullets are read
     from the filed list by their consumers (L-V's F-VA-PINS (e); the stage builders' input assertions).
  4. **`labels`:** one sub-bullet per key: `<key> — tag: <TAG|none>; label: <label>; text: "<text>"; items:
     <items>`; the text is the first double-quoted string (quotes inside it are single). Keys, tags and labels are
     those of L-X.13's table for the registration id (detector `TEMPLATE`).
- The filing script types no text, no spec and no number: it slices, parses, carries and hashes.
SOURCE: `x_rec/tierc11x/REGISTRATION_PLAN.md` (sha `a887ea64…3d15`; §0 `:18-48`, §1 `:53-301`, §2 `:304-331`);
`x_rec/scripts/tc11x_registrations.py:111-116`, `:329-360`, `:523-670`; `scout/U7_registrations_scoring.md` R1.
RIVALS: specs typed in the script (TC11) — nothing to diff the filing against, and a single family assumed. Each
owner's own dialect for the machine-read fields — not taken: the write-once filing would HALT on a dialect or file
fields the scorer cannot parse the same way twice.
FAILS-IF: `F-REG [SPEC-VERBATIM]` is RED when an `operative_spec` leaf differs from the plan's block, the plan's
block from the LEANS's, or a machine-read field is outside the grammar; planted mutations, each in a scratch plan:
one word changed in the `arms` field of one registration → `SPEC-VERBATIM`; `prior: 30%` → `SPEC-GRAMMAR`; a
second `` `scored` `` sub-bullet → `SPEC-GRAMMAR`; a precondition written as prose → `PRECOND-GRAMMAR`; a second
item with a numeric `required` (`> 0`) added to a copy of P-SCALP-3's block → `PRECOND-GRAMMAR`.

**L-X.19 WHAT `REGISTRATIONS.json` HOLDS, AND THE HASH LAW** — "frozen texts" (:5)
READING: `scripts/tierc12_registrations.py --file` writes
`research_outputs/tierc12/registrations/REGISTRATIONS.json`:
- top keys, in this order: `tier` · `contract {path, prefix_bytes, prefix_sha256, n_lines,
  whole_file_sha256_at_filing}` · `leans {path, sha256}` · `amendments {path, sha256}` · `review {path, sha256}` ·
  `plan {path, sha256}` · `rulings {path, sha256}` · `disclosures {path, sha256}` · `families [{family, stage,
  header_line, header_text, header_text_sha256, m, q, bar, bar_exact, n_registrations}]` · `verdict_law {clause_a,
  clause_b, clause_c, reading, rival}` · `statistics {n_boot, n_boot_source, seed, seed_source, seed_sens,
  seed_sens_source}` · `scored_window {end_ms, source}` · `era_cut {ms, source}` · `registrations [5]` · `chain [5]`
  · `head` · `law` · `law_source`;
- each registration body: `registration`, `seq`, `family`, `family_m`, `family_bar`, `prior_pct`, `seed`,
  `text_of_record`, `text_lines`, `context_of_record [{lines, text}]`, `external_context [{path, sha256, lines,
  text}]` (omitted when empty), `operative_spec {mechanism, population, arms, statistic, comparison, preconditions,
  labels, disclosed_beside, failure_conditions}`, `verdict_rule`, `text_sha256`, `sha256`. A field written with
  sub-bullets is a LIST under L-X.18's carry law: `operative_spec.arms` and `operative_spec.labels` always are, and
  `operative_spec.preconditions` is one unless it is the word `none`;
- **payload sha** = `sha256(json.dumps(body without text_sha256 and sha256, sort_keys=True,
  ensure_ascii=False).encode("utf-8"))`;
- **chain**: for each registration in `seq` order `line = {seq, registration, sha256, prev}`, `line_sha256 =
  sha256(json.dumps(line, sort_keys=True).encode())`, `prev` of the first = the genesis string — the character `0`
  repeated to the length of a sha256 hex digest, that length taken from `hashlib` and never typed (L-0.17) — and
  `head` = the last `line_sha256`;
- `law` is read by object from `research_outputs/tierc11/registrations/REGISTRATIONS.json["law"]`, the file pinned
  by TC11's chain head (`research_outputs/tierc11/registrations/REGISTRY_PIN.json["head"]`, asserted equal to the
  head recomputed from the payloads), and `law_source` names that path, head and key. No whole-file sha of that
  file is filed: the tc11-stamp close act moves it (L-0.24);
- `scored_window.end_ms` is read from `research_outputs/tierc11/data/AS_OF_PIN.json
  ["as_of_last_closed_4h_close_ms"]` and `era_cut.ms` from `x_rec/tierc11x/pins/PINS_X.json["era_cut_ms"]`; the
  scorer HALTs unless they equal L-D's objects `E.TC11_PIN_MS` and `E.ERA_CUT_MS` (O-9);
- `amendments` names `LEANS_AMENDMENTS.md` as it stands at filing: it holds AM-1 at filing — the dated V2-versus-X
  statement of L-V.15 (O-16; heading `## AM-1 · …`, nickname AM-V2, filed at the TC12-LEANS freeze with no AP,
  L-0.5). A later amendment never edits the filing — the scorer pins the then-current file separately (L-X.23);
- `rulings` and `disclosures` are the FREEZE PINS of L-0.5: `ORCHESTRATOR_RULINGS.md` and `DISCLOSURES.md` are
  append-only until the TC12-REG commit (R0's bytes a byte-prefix of every later version; only the orchestrator
  appends — section H, and D-5 … D-12), and from that commit they are byte-frozen at the shas these two leaves
  name. A build-time disclosure after the freeze goes to `DISCLOSURES_BUILD.md` (entries `B-1 …`), which no leaf of
  the filing pins;
- rendering: `json.dumps(doc, indent=2, ensure_ascii=False) + "\n"`, insertion order, UTF-8; no clock, no host, no
  path outside the repo in any leaf.
SOURCE: `x_rec/scripts/tc11x_registrations.py:496-509` (`payload_sha`, `chain_of`), `:658-670`, `:673-675`;
`scripts/tierc11_registrations.py:204-221`; `x_rec/tierc11x/registrations/REGISTRATIONS_X.json` (keys read here);
`research_outputs/tierc11/data/AS_OF_PIN.json`, `x_rec/tierc11x/pins/PINS_X.json` (keys read here).
RIVALS: bars as floats; a timestamp in the filing (breaks F-DET; neither precedent carries one).
FAILS-IF: `F-REG [HASH]` is RED when a payload sha or the chain does not re-derive from the filed bodies from the
genesis string, the filed `law` is not TC11's by object, or `law_source` carries a whole-file sha; planted
mutations: one `prev` bent → `CHAIN`; `family_m` of one body changed → `PAYLOAD-SHA`; a registration's order
swapped → `CHAIN`.

**L-X.20 WRITE-ONCE, AND `REGISTRY_PIN.json`** — "frozen texts" (:5)
READING:
- `--file` HALTs if `REGISTRATIONS.json` or `REGISTRY_PIN.json` exists, then creates both with `open(path, "xb")`;
  nothing is ever overwritten; there is no refile flag and no `_rerun` twin for the registry. A second `--file`
  leaves both files' bytes unchanged.
- `REGISTRY_PIN.json` (generated; `json.dumps(pin, indent=2, sort_keys=True, ensure_ascii=False) + "\n"`):
  `registrations_file {path, bytes, sha256}`, `order_of_filing`, `registry_len`, `genesis`, `head`, `chain` (the
  line shas), `registrations {<id>: {seq, sha256, text_sha256, text_lines, prior_pct, family, family_m,
  family_bar}}`, `families`, `contract`, `leans`, `amendments`, `plan`, `review`, `rulings`, `disclosures`, `seed`,
  `seed_sens`, `n_boot`, `law`, `law_source`, `spec_carry_law`, `witness_law`, `text_before_result_law`.
- Both files are tracked (the nested `.gitignore` excludes only parquet, `_det_*/` and `x_rec/**`). They are
  committed in the one commit `tierc12(TC12-REG): …`, and that commit ADDS exactly `REG_SET` (L-X.21) — the plan,
  the two registry files, `ATTEST_REG.json`, the pin files, the census, the stage's transcripts and record, and
  the scripts the filing needs — and modifies only `scripts/tierc12_progress.py` and `PROGRESS.json`. The frozen
  `LEANS.md` and the review record were committed earlier, at TC12-LEANS.
SOURCE: `x_rec/scripts/tc11x_registrations.py:682-711` (`pin_of`), `:714-727` (`file_filing`);
`scripts/tierc11_registrations.py:241-247`; `research_outputs/tierc12/.gitignore`; O-2.
RIVALS: `write_text` behind an exists-check (TC11) — a race between check and write; exclusive create has none.
FAILS-IF: `F-REG [WRITE-ONCE]` is RED when a second `--file` changes a byte or exits 0, in the filed directory and
in a scratch twin; planted mutation: `"xb"` replaced by `"wb"` in a scratch copy of the filer.

**L-X.21 TEXT BEFORE RESULT** — "families declared by MECHANISM before the look" (:8)
READING: three clauses, each checked.
1. **Write-once** (L-X.20).
2. **The head is stamped into every book.** Every `regbooks/<ID>/STATUS.json`, every arm sidecar, every
   `regbooks/<ID>/build_manifest.json` and every stage `build_manifest.json` that holds a book carries
   `registry_head` and `registrations_sha256` (the latter a key of L-0.13's manifest list); the scorer HALTs a row
   (`HEAD-STAMP`) whose STATUS or sidecar lacks them or carries other values than `REGISTRY_PIN.json`'s.
3. **A git-order attestation, run out of process** (git facts gathered by a subprocess of the fixture module;
   `--no-optional-locks`; read-only verbs), keyed on TC12's own paths (`research_outputs/tierc12/`,
   `scripts/tierc12_*`, `analytics/value_area.py`, `exchange/rows/tierc12/`) because the branch takes an
   `exchange: auto-publish` commit every day. Two sets are typed in the fixture, paths relative to
   `research_outputs/tierc12/` unless they begin `scripts/`:
   - **`PRE_REG`** = the artifact paths of STEP Q, TC12-R0 and TC12-LEANS; `progress/**`; `PROGRESS.json`;
     `.gitignore`; `scout/**`; `x_rec/**`; `leans_draft/**`; `review/**`; `LEANS.md`, `LEANS_AMENDMENTS.md`,
     `AMENDMENTS_PROPOSED.md`, `ORCHESTRATOR_RULINGS.md`, `DISCLOSURES.md`.
   - **`REG_SET`** (exactly what the TC12-REG commit ADDS) = `REGISTRATION_PLAN.md`;
     `registrations/{REGISTRATIONS.json, REGISTRY_PIN.json, ATTEST_REG.json, FIXTURES_REG.txt}`;
     `pins/{CONTRACT_PIN_MAP.json, CONTRACT_PINS.json, PIN_REGISTER.json, CONTRACT_TOKENS_UNPINNED.json,
     FIXTURES_PINS.txt}`; `frozen/FROZEN_ESTATE.json`; `resume/FIXTURES_RESUME_TC12-REG.txt`;
     `closure/FIXTURES_CLOSURE_TC12-REG.txt`; `progress/TC12-REG.json`; the scripts `tierc12_{fx, units, pins,
     frozen, registrations}.py` and `tierc12_{registrations, pins, resume, closure}_fixtures.py`. The commit also
     MODIFIES (does not add) `scripts/tierc12_progress.py` and `PROGRESS.json`. The vendored referee is not in
     `REG_SET` (it is `TC12-ENV.vendor`'s).
   - **ATTEST-REG (at filing).** The disk walk under `research_outputs/tierc12/` — ignored and untracked files
     included — holds no file outside `PRE_REG ∪ REG_SET` and no `.parquet` outside `x_rec/`, and
     `scripts/tierc12_*.py == {tierc12_progress.py} ∪ REG_SET`'s scripts. `registrations/ATTEST_REG.json` is the
     sorted listing (path, sha), taken after `--file`, of every file then on disk except itself.
   - **ATTEST-ORDER (at TC12-SCORE, at CLOSE and in `close_acts.sh` step 0).** `REG` = the unique commit adding
     `registrations/REGISTRATIONS.json` (`git log --diff-filter=A --format=%H -- <path>`), whose blob equals the
     working file and the pin's sha. The paths first added by `REG` are exactly `REG_SET`; every tracked TC12 path
     P outside `PRE_REG ∪ REG_SET` has `first_add(P)` a PROPER descendant of `REG` (`first_add(P) ≠ REG` and `git
     merge-base --is-ancestor REG first_add(P)`). `TC12-REG.ledger-spec` (`forward/**`,
     `scripts/tierc12_forward_spec.py`, `scripts/tierc12_forward_fixtures.py`) is filed AFTER the attested instant
     and is covered by that descendant test. Ignored parquet is bound through clause 2 and through its record, a
     tracked path under this test.
SOURCE: `x_rec/scripts/tc11x_registrations.py:916-958` (`attest_findings`, HEAD-LAW; the one order fixture on
disk); `x_rec/tierc11x/REGISTRATION_PLAN.md:362` ("no book of any kind before X-REG");
`scout/U7_registrations_scoring.md` §1.3 (no builder stamps the head in either tier), R15, H9.
RIVALS: a timestamp in the filing — a clock is not evidence and breaks F-DET. An attestation on `HEAD` adding only
tier files — fails on the first auto-publish commit. `PRE_REG` read from the progress records of the stages before
TC12-REG alone — not taken: the stage's own files (the pin files the filer calls, the census, the harness, the
transcripts) exist at filing and are first added by `REG`, so that test is RED by construction; they are typed as
`REG_SET`.
FAILS-IF: `F-ATTEST-ORDER [REG]` (registry suite, TC12-REG) is RED when the disk walk at filing holds a file outside
`PRE_REG ∪ REG_SET`, a `.parquet` outside `x_rec/`, or a `scripts/tierc12_*.py` outside the typed set, or
`ATTEST_REG.json` is not that listing. `F-ATTEST-ORDER [ORDER]` (score suite at TC12-SCORE; close suite at
TC12-CLOSE) is RED when the paths first added by `REG` are not exactly `REG_SET`, a tracked TC12 path outside the
two sets was first added at `REG`, before it or off its descendants, or a STATUS, sidecar or regbook manifest
lacks the head. Planted mutations, in scratch repositories: a `STATUS.json` committed before the filing commit
(`ORDER`); a member of `REG_SET` first added one commit later (`ORDER`); a STATUS carrying another head
(`HEAD-STAMP`); an ignored `books/x.parquet` present at filing (`ATTEST-REG`); a stage script
`scripts/tierc12_books.py` present at filing (`ATTEST-REG`).

**L-X.22 THE VERIFIER** — "frozen texts" (:5)
READING: `verify_filing(doc, pin, contract_bytes, reg_bytes, ext_bytes, plan_bytes, leans_bytes) -> list[str]` is the
scorer's first act and F-REG's production side; `[]` iff every detector is silent: `CONTRACT-PREFIX` ·
`CONTRACT-TAIL` · `TEXT-SLICE` · `CONTEXT-SLICE` · `EXTERNAL-SLICE` · `PAYLOAD-SHA` · `SEED` · `FAMILY-PARSE` ·
`FAMILY-BAR` · `FAMILY-MEMBER` · `FAMILY-M-COUNT` · `RULER-TEXT` · `TEMPLATE` · `SPEC-GRAMMAR` · `PRECOND-GRAMMAR` ·
`CHAIN` · `HEAD-PIN` · `SPEC-VERBATIM` · `PLAN==LEANS`. `TEMPLATE` compares each registration's template, label key,
tag and label with L-X.13's table BY REGISTRATION ID; `SPEC-GRAMMAR` and `PRECOND-GRAMMAR` hold L-X.18's field
grammar. F-REG runs the verifier and, beside it, an independent re-derivation written in the fixture file (slices,
shas, chain, the template table, the grammar), so the production verifier is never compared with itself.
SOURCE: `x_rec/scripts/tc11x_registrations.py:731-805`; `scripts/tierc11_score.py:391-492`;
`x_rec/scripts/tc11x_registrations_fixtures.py:19-56`.
RIVALS: none.
FAILS-IF: `F-REG [VERIFIER]` is RED unless each plant is caught by its intended detector, one at a time: a contract
byte; a text character; a context range; a payload leaf; the seed; a header's bar; a registration moved under
another header; the ruler words struck from a slice; a template of another registration; a checked field with a
trailing `%`; a precondition in prose; a chain `prev`; the pin's head; a spec word; one byte of the plan.

---------------------------------------------------------------------------------------------------------------
### C · The scorer

**L-X.23 SCORER INPUTS, EACH PINNED BY SHA** — "no number typed that a file can supply" (:8)
READING:
- **Where the code is filed.** `scripts/tierc12_score.py`, the interface module `scripts/tierc12_regbook.py`
  (L-X.24) and `scripts/tierc12_score_fixtures.py` are filed at the dotted child `TC12-ENV.score-build` (blocking;
  `depends_on` `TC12-ENV`; own commit `tierc12(TC12-ENV.score-build): …`; L-0.10) — after the env, before any
  book, reading no TC12 book. Its suite run (`--stage=TC12-ENV.score-build` → `env/FIXTURES_SCORE_BUILD.txt`)
  proves the rule, the rulers and the regbook validator on synthetic arms and on TC11's filed arms, and files
  `env/SIZE_MEASURED.json` (L-X.14). Stages G, R and S can therefore validate their regbooks with the scorer's own
  module, and none writes a validator of its own. The run of record is TC12-SCORE, which starts only when TC12-C,
  -G, -R, -S, -L and the three stamps children are COMPLETE-VERIFIED (L-0.10).
- **Inputs.** `scripts/tierc12_score.py [--regbooks-root=DIR] [--out-dir=DIR] [--dry-run] [--refile=<AM-n|FIX-n>]`
  imports `tierc12_env` first and reads, in this order, HALTing the run on the first failure. Every sha below is
  the certified one — the entry of the LAST record that names the path, parent or dotted child — never a record
  typed by name:
  1. the contract through L-X.16;
  2. `registrations/REGISTRATIONS.json` and `REGISTRY_PIN.json` at their certified shas; `verify_filing` returns
     `[]`;
  3. `LEANS.md`: sha equal to the filing's `leans.sha256`;
  4. `LEANS_AMENDMENTS.md`: sha equal to `PROGRESS.json["amendments_of_record"].sha256`; the sha is filed in the
     manifest, so a reader sees which amendments were in force when the row was scored;
  5. L-D's fee schedule and pins at their certified shas;
  6. per registration, `regbooks/<ID>/STATUS.json`, `build_manifest.json` and each arm STATUS lists: the file sha
     of every parquet and sidecar equal to the certified one (on the stage plan the owning records are `TC12-G`
     for P-ADM-1 and P-BRD-1, `TC12-R.dir` for P-DIR-1, `TC12-R.sfp` for P-SFP-VA-1, `TC12-S` for P-SCALP-3 — found
     by `certified()`, not typed); `validate_book` silent; the canonical `book_sha256` recomputed from the parquet
     equal to the sidecar's; `registry_head` per L-X.21;
  7. each precondition record named by a spec — on the filed specs L-V's `va/VA_MIRROR.json` — at its certified
     sha (L-X.10);
  8. the two count records printed under the `selection_hazard` cells: `stage_g/g_brd17.parquet` (columns `cell`,
     `n`) and `stage_r/dir/build_manifest.json` key `r5_overlap` (L-X.13);
  9. `env/SIZE_MEASURED.json` (L-X.14).
- **TC11 and X.** The scorer reads no TC11 or X file except, through `E.tc11_record`: `scores/SCORES.json`
  (`n_boot`, `seed_sens`), `scores/BASE_IDENT.json`, `data/AS_OF_PIN.json`; through `E.x_rec`:
  `tierc11x/pins/PINS_X.json["era_cut_ms"]`, `tierc11x/va/build_manifest.json` key `pins.laws.round_nd`, and by
  `ast` from the text of `scripts/tc11x_score.py` the literals `SIZE_FOOTNOTE`, `CI_LO_Q`, `CI_HI_Q`; by `ast` from
  the text of `scripts/tierc11_score.py` the literals this section names (the sixteen columns, the three
  tolerances, the exit flags), each pinned by the sha of its AST node in `pins/PIN_REGISTER.json` and never by that
  file's sha (L-0.24); and, in F-SCORE-ANCHOR only, TC11's filed `regbooks/P-AGE-1/{base, scored}` and
  `regbooks/P-BRK-4H/scored`. Those TC11 paths are this section's rows of L-D's `TC11_ALLOW_FILE`.
SOURCE: `x_rec/scripts/tc11x_score.py:339-373` (`verify`, `load_inputs`: each input bound to its stage's progress
record); `scripts/tierc11_score.py:495-505`, `:2577-2608`; O-3, O-4, O-6.
RIVALS: shas typed in the scorer (TC11) — a re-pin then edits code. Books pinned only by their own sidecars (TC11) —
a sidecar can be rewritten with its book. A record name typed per input (`progress/TC12-R.json`) — not taken: a
path recorded by more than one record is governed by its last record, and Stage R's books are certified by its
children. The scorer filed at TC12-SCORE — not taken: Stages G, R and S list F-REGBOOK and F-BASE-IDENT among their
failure conditions and need the validator before any book.
FAILS-IF: F-SCORE-INPUTS (score suite, TC12-SCORE) is RED when the scorer scores with a pinned input changed;
planted mutations: one LEANS byte; one byte of a regbook parquet (sidecar left alone); an arm on disk that STATUS
does not list scored anyway; a regbook file whose sha is the one an EARLIER record filed and not its last record's.

**L-X.24 THE REGBOOK INTERFACE (what Stages G, R and S write and the scorer reads)** — no contract line — the
regbook interface (F-KEY, :124, is L-0.21's)
SEAM SETTLEMENTS (`review/SEAM_PASS.json`, 2026-10-09 — part of this reading; each line governs where the text below is silent or differs):
- [seam 48] F-REGBOOK accepts `fill_rule = "touch"` on `tierE__maker_assumed` (it re-books the record's touch fills) and `"tick"` on `tierE__maker_conditioned`.
- [seam 58] `validate_book` accepts `fill_rule = null` on kind `strip` (P-SCALP-3's strip holds rows of three fill rules).
- [seam 59] the 'no comma, quote, CR or LF in a string' law covers EVERY string column of a regbook row, extra columns included; an owner-supplied label must comply or stay out of the rows.
READING: the directory-level F-KEY (declared keys, as-of stamps, collar totality) is L-0.21's and runs on every
regbook directory; the ROW-level laws below are the scorer's, proven by F-REGBOOK.
- **Module.** `scripts/tierc12_regbook.py` (filed at `TC12-ENV.score-build`, L-X.23) holds the interface every
  book stage and the scorer share: `ARM_RX`, `COLS16`, `COLS20`, `canonical_csv(df, cols)`, `book_sha256(df)`,
  `book_ext_sha256(df)`, `validate_book(reg_dir, arm) -> findings`, the fee identities, `write_arm(reg_dir, arm,
  df, *, meta, lens, sidecar) -> None`, `write_status(reg_dir, …)`, `write_manifest(reg_dir, …)`. **Arms are
  written by `tierc12_regbook.write_arm`, which calls L-0.13's `tierc12_tables.put_regbook` and then writes
  `<arm>.json`.** `put_regbook` is the tier's second and last parquet writer — FULL FLOAT, no rounding, the key
  asserted unique, rows mergesorted on the key, the nine stamps, the collar unless the arm is registered, a HALT
  unless the directory resolves under `regbooks/` — and `write_arm` is its only caller. It is TC11's
  `write_regbook` law, which is what lets a TC12 arm hash to a TC11 arm's canonical sha (L-X.25). The scorer
  imports this module; no stage writes a validator or a regbook writer of its own.
- **Layout.** `research_outputs/tierc12/regbooks/<ID>/` = `STATUS.json`, `build_manifest.json` (declared key per
  arm, content shas, `registry_head`, `registrations_sha256`), and per arm `<arm>.parquet` + `<arm>.json`. Arm
  names match `^(scored|base|ladder__(touch|deep)|strip|tierE__[a-z0-9_]+)$`. The arm of record is `scored`
  (TC11's name; "treated" is not a name on disk).
- **`STATUS.json` keys:** `registration`, `status ∈ {"BUILT", "CLOSED_BY_PRECONDITION"}`, `reason`, `arms` (sorted;
  every arm on disk and no other; `[]` when closed), `registry_head`, `registrations_sha256`, `source_script`,
  `source_script_sha256`, `preconditions` (each item `{record, certified_by, selector, required, found, met}`). A
  parquet on disk that `arms` does not list is a note and is not read.
- **The arms of record** (STATUS lists exactly these when BUILT; an arm with no row is written EMPTY, below):

  | registration | arms |
  |---|---|
  | P-ADM-1 | `base`, `scored`, `strip`, `tierE__shadow_old_alone`, `tierE__shadow_stale_alone`, `tierE__shadow_abs206`, `tierE__shadow_abs206_or_stale` |
  | P-BRD-1 | `base`, `scored`, `strip`, `tierE__brd_face`, `tierE__brd_neff`, `tierE__brd_loo`, `tierE__brd17` |
  | P-DIR-1 | `base`, `scored`, `strip` |
  | P-SFP-VA-1 | `scored`, `strip`, `tierE__unfiltered`, `tierE__cell_1d`, `tierE__guard_1d`, `tierE__maker_conditioned`, `tierE__maker_assumed`, `tierE__x_geometry`, `tierE__x_gaplaw` |
  | P-SCALP-3 | `scored` (TICK), `ladder__touch`, `ladder__deep`, `strip`, `tierE__full_corridor`, `tierE__panel17`, `tierE__rr_unfiltered`, `tierE__live_edge` |

  `base` exists on the three two-sample rows and only there; `ladder__touch` and `ladder__deep` on P-SCALP-3 only,
  where `scored` is the TICK book. No registration ships a re-ride arm: a re-ride is a disclosure of counts and
  diff rows in its stage's own tables (L-G.18, L-R.5).
- **Columns, exact dtypes, in this order.** TC11's sixteen, unchanged (read by `ast` from
  `scripts/tierc11_score.py:248-255`; the literal is pinned by `sha256(ast.dump(node))`, recorded in
  `pins/PIN_REGISTER.json` (kind `lineage`) at TC12-REG — never by that file's sha, which the tc11-stamp moves,
  L-0.24): `symbol` str · `entry_ms` int64 · `entry_close_ms` int64 · `direction` int8 · `entry_px`, `stop_px`,
  `r_dist` float64 · `exit_close_ms` int64 · `exit_reason` str · `net_r`, `gross_r`, `fee_r`, `funding_r`,
  `haircut_net_r` float64 · `era` str · `lane` str. Then TC12's four, all float64: `fee_taker_r` (the fee of the
  taker legs ÷ `r_dist`) · `fee_maker_r` (the fee of the maker legs ÷ `r_dist`) · `fee_all_taker_r` (the fee of
  every leg priced at the taker rate ÷ `r_dist`) · `taker_twin_net_r` (the all-taker twin's net R). These twenty
  are required on every arm. Conditional columns: `taker_twin_haircut_net_r` float64 — required iff the sidecar's
  `toll == "maker_entry_targets__taker_stop"`; `funding_ceiling_bound` bool and `tc_series_net_r` float64 —
  required on every range arm (lanes `sfp-va-4h`, `sfp-va-1d`, `scalp_va_1h`); `arm` str — required on `strip` and
  only there. Extra columns are allowed and ignored by the scorer. `lane` values: `card` (v6 and its gates),
  `sfp-va-4h`, `sfp-va-1d`, `scalp_va_1h`.
- **Meaning.** `symbol` is the asset (a fee-schedule stem). `entry_close_ms` is the close of the lens bar in which
  the position was entered (v6: the 4h entry bar; P-SFP-VA-1: the return bar; P-SCALP-3: the 5m fill bar);
  `entry_ms` is that bar's open. `net_r` is the toll of record in R. `funding_r` is the journaled funding, positive
  = paid — capped by the card's D12 rule on v6-derived arms, UNCAPPED on range arms (OD-10: the ceiling is a
  v6-card accounting rule and is not a rule of the range trades). On a range arm `tc_series_net_r` is the
  lineage's own booking of the all-taker trade, D12 ceiling included, and `funding_ceiling_bound` says whether that
  ceiling bound on the row. `haircut_net_r` is the charter-slippage twin of the record (slippage on its taker
  legs); `taker_twin_net_r` is the all-taker twin at the row's own funding; `taker_twin_haircut_net_r` is charter
  slippage on every fill of the all-taker twin.
- **Laws, each a HALT on `scored`, `base` and `ladder__*` arms** (a NOTE on `tierE__*` arms where TC11 notes):
  no null in a required column; unique `(symbol, entry_close_ms)` — on `strip`, `(arm, symbol, entry_close_ms)`;
  `base` also unique on `(symbol, entry_ms)`; `direction` ∈ {+1, −1}; `era == E.era_of(entry_close_ms)` (`tuning`
  iff `entry_close_ms ≤ ERA_CUT`, else `holdout`) and consistent with the sidecar's `era_scope`; `0 <
  entry_close_ms − entry_ms ≤` one bar of the sidecar's `lens` (required, no default; the step read from
  `E.LENS_MS`, of which TC11's `LENS_STEP_MS` at `scripts/tierc11_score.py:294-295` is the filed form);
  `exit_close_ms ≥ entry_close_ms`; `r_dist > 0`; every symbol in the sidecar's `panel`, and that `panel` equal to
  the home panel `E.CLASSIC5` on every `scored`, `base` and `ladder` arm; no `,`, `"`, CR or LF in a string;
  - **the scored window (O-9):** on every arm but `strip`, `entry_close_ms ≤ W` and `exit_close_ms ≤ W` (`W` equal
    to the filing's `scored_window.end_ms`). The book is ridden with `hi` = the last bar of its own clock closing
    `≤ W`; a position still open there is marked at that bar's close with `exit_reason = "corridor_end"`.
    P-SCALP-3's scored and ladder rows: `ERA_CUT < entry_close_ms ≤ W`; the gates and P-SFP-VA-1: every era,
    `entry_close_ms ≤ W`;
  - **the strip (O-9, OD-14):** `strip.parquet` holds, under the column `arm`, the rows with `W < entry_close_ms ≤
    PIN` of EVERY other arm of the regbook, taken from a second ride with `hi` = the last bar closing `≤ PIN` (for
    a post-filter gate: the v6 strip campaigns each arm's rule keeps, `base` = all of them; for a ridden book:
    that arm's own ride to PIN). An arm that is the same walk as another (P-SFP-VA-1 `tierE__maker_assumed` ≡
    `scored`; P-SCALP-3 `tierE__full_corridor` ≡ `scored`) is not repeated: it appears in the strip sidecar's
    `n_by_arm` with `same_rows_as`. Ridden, printed beside, never scored, never pooled: counts and a pointer only —
    no statistic over strip rows anywhere;
  - **the fee identities:** `|fee_r − (fee_taker_r + fee_maker_r)| ≤ HAIRCUT_TOL`; `|taker_twin_net_r − (net_r +
    fee_r − fee_all_taker_r)| ≤ HAIRCUT_TOL`; on an arm whose sidecar `toll` is `taker`: `fee_maker_r == 0`,
    `fee_taker_r == fee_r`, `fee_all_taker_r == fee_r` and `taker_twin_net_r == net_r` exactly;
  - **the haircut laws (TC11's AM-7 with its maker clause):** `|haircut_net_r − (net_r − fee_taker_r × slip /
    taker)| ≤ HAIRCUT_TOL`, and, where the column is required, `|taker_twin_haircut_net_r − (taker_twin_net_r −
    fee_all_taker_r × slip / taker)| ≤ HAIRCUT_TOL`, with `slip` = `slippage_bps_side` and `taker` =
    `taker_bps_side` read per symbol from `E.fees()` (L-D); a maker leg carries no slippage;
  - **the funding identity on range arms:** `|taker_twin_net_r − tc_series_net_r| ≤ HAIRCUT_TOL` on every row with
    `funding_ceiling_bound == False`, and `taker_twin_net_r < tc_series_net_r` on the others; the bound count per
    arm is printed;
  - **the net law, a disclosure only:** rows with `|net_r − (gross_r − fee_r − funding_r)| > NET_LAW_TOL` are
    counted and printed.
  `HAIRCUT_TOL`, `SUM_TOL`, `NET_LAW_TOL` are read by `ast` from `scripts/tierc11_score.py:264-266`, each pinned by
  its node sha as above.
- **Sidecar `<arm>.json` keys:** `registration`, `arm`, `kind ∈ {base, scored, ladder, strip, tierE}`, `ruler ∈
  {two_sample, vs_zero}`, `era_scope ∈ {full, holdout, tuning}`, `panel` [stems], `lens`, `toll ∈ {"taker",
  "maker_entry_targets__taker_stop"}`, `fill_rule` (`tick` / `touch` / `deep` on P-SCALP-3's arms and on the two
  SFP maker twins; else null), `n`, `sum_net_r` (within `SUM_TOL` of the parquet's), `book_sha256`,
  `book_ext_sha256`, `registry_head`, `registrations_sha256`, `fee_schedule {path, sha256}`, `description`,
  `source_script`, `source_script_sha256`. Added by kind: P-SCALP-3's `scored`, `ladder__touch` and `ladder__deep`
  carry `n_orders`, `n_filled_touch`, `n_filled_tick`, `n_filled_deep`; `strip` carries `n_by_arm {arm: n}` and,
  for an arm that is the same walk as another, `same_rows_as`; `tierE` and `strip` sidecars carry the collar keys;
  `tierE__cell_1d` carries `licence_pointers = {era:
  "research_outputs/tierc12/va/VA_MIRROR.json#licence[1d|taker].by_era[<era>]"}` and the booleans
  `licence_ok_by_era` — never the words (the words are printed only in §0 beside the row).
- **The empty-arm form.** Every arm a spec names is written even when empty: a zero-row parquet with the columns
  above at their dtypes, the nine stamps and (if collared) the collar; its sidecar with `n = 0`, `sum_net_r = 0.0`
  and the `book_sha256` of the header-only canonical CSV; STATUS `arms` lists it. An arm STATUS lists whose parquet
  or sidecar is absent is HALT `ARM-MISSING`, never read as empty; that a BUILT STATUS lists every arm of the table
  above is held by `F-REGBOOK [<ID>]` against the fixture's own typed copy of that table.
- **Two hashes.** `book_sha256` = TC11's SC-13 law over the sixteen columns (canonical CSV: rows sorted `(symbol,
  entry_close_ms)`, header, `,`-joined, ints `str(int)`, floats `repr(float)`, `\n` after every line), so a TC12 arm
  is comparable with a TC11 arm; `book_ext_sha256` = the same law over the twenty.
- **Ladder law on P-SCALP-3 (per order, O-32).** Each of the three ladder-class sidecars (`scored`,
  `ladder__touch`, `ladder__deep`) carries `n_orders`, `n_filled_touch`, `n_filled_tick`, `n_filled_deep` — the
  three entry tests of L-S.15 evaluated on THAT arm's own order ledger (L-S.16). The scorer HALTs `LADDER-ORDER`
  unless `n_orders ≥ n_filled_touch ≥ n_filled_tick ≥ n_filled_deep` on every one of the three. The arm totals
  `n(ladder__touch)`, `n(scored)`, `n(ladder__deep)` are printed in the fill-sensitivity row and are not ordered by
  law (three separately sequenced books); when they are not ordered the row's `disclosures[]` carries
  `BOOK-N-NOT-MONOTONE` — a disclosure, never a HALT and never a qualifier.
- **Fixtures.** F-REGBOOK's plant legs and its production side live with the scorer (`tierc12_score_fixtures.py`,
  hosted at `TC12-ENV.score-build`, on arms the fixture builds to this interface — no TC12 book is read there);
  the real-book instances `F-REGBOOK [<ID>]` and `F-BASE-IDENT [<ID>]` are helper legs — functions of that module —
  which each book stage's suite runs on its own regbook directory (TC12-G: P-ADM-1, P-BRD-1; TC12-R.dir: P-DIR-1;
  TC12-R.sfp: P-SFP-VA-1; TC12-S: P-SCALP-3).
SOURCE: `scripts/tierc11_score.py:245-266`, `:294-299`, `:618-635` (`canonical_csv`), `:646-770` (`validate_book`),
`:773-830`; `scripts/tierc11_stage_g.py:1168-1178` (`write_regbook`: `TP.stamp_n`, then `to_parquet`, no rounding)
[read here]; `scripts/tierc10_brk.py:1322-1324` (`account_l` returns `funding_r_uncapped` and
`funding_ceiling_bound`) [read here]; `research_outputs/tierc11/regbooks/P-AGE-1/base.json` (the sidecar's filed
form, `book_sha256_law`); `research_outputs/tierc11/LEANS_AMENDMENTS.md:86-97` (AM-7); contract :101-102, :120-121;
O-9, O-19, O-32; `scout/U7_registrations_scoring.md` §1.8, §2.14, R13.
RIVALS: TC11's sixteen alone with AM-7 as written — a maker-toll scored arm cannot pass it (it assumes every fee leg
taker). A `fee_taker_r`-only extension (U7 R13) — leaves the all-taker twin unverifiable by identity. Arms written
through the 6-dp table writer — not taken: a rounded arm cannot hash to TC11's full-float canonical sha. A HALT on
the three arm totals `n(ladder__touch) ≥ n(scored) ≥ n(ladder__deep)` — not taken: the three books are sequenced
separately, the totals are not a theorem, and a HALT with no defect behind it would stop a registered row (O-32).
An empty arm left unwritten (the lineage's skip-empty law) — not taken inside `regbooks/`: a missing file and an
empty book would look alike.
FAILS-IF: `F-REGBOOK [plants]` (at `TC12-ENV.score-build`) is RED unless each plant on a copy of an arm the fixture
builds is caught by its named detector: era by the open; a duplicate key; a null `net_r`; a dropped column;
`direction` 0; float32; the haircut law broken on a maker arm; `taker_twin_haircut_net_r` bent on a maker arm;
`taker_twin_net_r` bent on a taker arm; `tc_series_net_r` bent on an unbound range row; an entry bar longer than
the lens; an exit before entry; a row past `W` in `scored`; a strip row at or before `W`; a strip row with no
`arm`; a stray asset; a comma in a string; a sidecar `n`, `sum_net_r` or `era_scope` bent; a missing
`registry_head`; an arm STATUS lists absent from disk → `ARM-MISSING`; an empty arm whose sidecar hash is not the
header-only CSV's; the TICK and DEEP counts swapped in a sidecar copy → `LADDER-ORDER`; an arm written at 6 dp
(its `book_sha256` no longer the full-float one). `F-REGBOOK [<ID>]` (each book stage) is RED when
`validate_book` returns a finding on any arm of the real regbook, STATUS does not list exactly the arms of record,
or — the row closed by precondition — the directory is not STATUS-only (it then prints `CLOSED-NO-BOOK <ID>`);
planted mutations on a copy of the real `scored` arm: a duplicate key; a row past `W`; the `registry_head`
removed.

**L-X.25 GATES AT THE SCORER: ONE BASE, POST-FILTERS ONLY** — "both two-sample vs v6 — they remove trades" (:52)
READING:
- **F-BASE-IDENT.** The three `base` arms carry ONE `book_sha256`, and it equals
  `research_outputs/tierc11/scores/BASE_IDENT.json["book_sha256"]["P-AGE-1"]` (on file `f41bfaf0…68a8`; the file is
  read through `E.tc11_record`, which asserts its sha — on file `29f795dc…5581`; Q1's cascade never moves it): the
  base is TC11's filed v6 book, bit for bit on the sixteen columns (O-21). A difference HALTs all three rows. The
  identity is reachable only because every arm is written at FULL FLOAT by `tierc12_regbook.write_arm` (L-0.13's
  `put_regbook`, L-X.24): TC11 wrote its arms unrounded, and the canonical sha is taken over `repr(float)`.
- **GATE-POSTFILTER (TC11's SC-16).** HALT a gate's row if its scored arm holds a key `(symbol, entry_ms)` absent
  from the base, or if a kept row differs from the base's on any of the sixteen columns (floats and ints compared
  exactly).
- The refused set equalling the contract's text is the owners' F-GATE, F-BRD and F-DIR, not the scorer's.
SOURCE: `scripts/tierc11_score.py:914-942` (`gate_findings`), `:1302` (`base_ident`);
`research_outputs/tierc11/scores/BASE_IDENT.json`; `research_outputs/tierc11/regbooks/P-AGE-1/base.json`; O-21.
RIVALS: one shared base file outside the regbooks — breaks the per-registration interface the contract's F-KEY
checks. Equality at 6 dp (TC11's SC-7 against `books/v6_campaigns.parquet`) — printed beside; the canonical sha is
the stricter and is of record.
FAILS-IF: `F-BASE-IDENT [P-ADM-1]`, `[P-BRD-1]` (run by Stage G's suite) and `[P-DIR-1]` (run by `TC12-R.dir`'s) are
RED when the base arm's `book_sha256`, recomputed from the parquet, differs from TC11's filed value, or the gate's
scored arm holds a foreign key or an altered kept row; planted mutations, each on a copy of the real arm: one base
`net_r` moved by one ulp; one base row dropped; a gate's kept row altered; a campaign added to a gate; the base arm
rewritten through the 6-dp table writer.

**L-X.26 WHAT THE SCORER WRITES** — "§0 VERDICTS FIRST: the five rows with their labels" (:126-127)
READING: under `research_outputs/tierc12/scores/`:
- `SCORES.json`: `tier`, `stage`, `inputs` (every sha of L-X.23), `seed`, `seed_sens`, `n_boot`, `scored_window`,
  `era_cut`, `verdict_law`, `families`, then
  - `rows` — exactly one leaf per registration, in `seq` order: `registration`, `seq`, `family`, `m`, `bar`,
    `bar_exact`, `bar_cell`, `prior_pct`, `status`, `status_reason`, `ruler`, `era_scope`, `panel`, `lens`,
    `preconditions`, `n`, `n_base`, `n_clusters`, `point`, `lo`, `hi`, `p_num`, `p_den`, `p_one_sided`,
    `n_draws_finite`, `n_draws_le_0`, `deciding_rank`, `deciding_bound`, `clause_a`, `clause_b`, `clause_c`,
    `verdict_of_record`, `qualifiers`, `labels`, `disclosures`, `superseded`, `size_footnote`, `size_measured
    {ruler, n_clusters, nominal, one_sided_size}`, `verdict_cell`, `verdict_text`, `stable_across_seeds`,
    `spent_test`, `premise`, `gate` (gates), `draw_sets`, `provenance`, `halts`, `notes`; on the two-sample rows
    also `refused_n`, `refused_assets`, `p_draw_identically_zero`, `n_draws_exact_zero` (L-X.7); on P-SCALP-3 also
    `fill_ladder` — per book (`touch`, `tick`, `deep`) its state `C` / `F` / `U`, `n`, `n_clusters`, `point`, `lo`,
    `hi`, `p_num`, `p_den`, `C_sens` and the four per-order counts of that ledger, then `fails_under_deep_too`,
    `clears_only_under_touch` and `book_n_not_monotone` — `one_asset` (`above`, `above_excl_zero_campaign`,
    `below`, `N`, `bar`, `D`, `D_sens`, `passing_when_dropped`, `failing_when_dropped`) and
    `word_stable_across_seeds` (L-X.8, L-X.9, L-X.11);
  - `beside` — exactly one leaf per member of the row's DECLARED BESIDE SET (L-X.14: the common slugs ∪
    {`arm__<slug>` for exactly the Tier-E arms in its STATUS}), keyed `(registration, slug)`, collared.
- `FAMILY.json`: `q`, `n_boot`, `families [{family, stage, header_line, m, bar, bar_exact, deciding_rank,
  registrations, tests_spent, supported, rows [{registration, seq, status, verdict_of_record, spent_test, p_num,
  p_den, clause_a, clause_b, clause_c, label}]}]`, `tests_spent_total`, `nominal_union_bound` (`Σ_f m_f · bar_f`,
  L-X.2), `law`.
- `BASE_IDENT.json` (L-X.25) · `REGISTRY_CHECK.json` (L-X.22's findings and every sha it read) · `S0_VERDICTS.md`
  (the five rows as a table in L-X.28's columns, each followed by the lines that stand under its cell — the bytes
  the report's §0.1 quotes) · `BESIDE.md` (every beside leaf, whole and collared — the stage document of record
  the report points to) · `SCORE_MANIFEST.json` (inputs, outputs, the scorer's own sha) · `DRAWS.parquet` ·
  `REFILE_LOG.jsonl` and `SUPERSEDED.jsonl` (both append-only and tracked, L-0.5; L-X.27) · `build_manifest.json`
  with `READ_SET.json` beside it (L-0.13) · `FIXTURES_SCORE.txt`. No file exists under `scores/` before TC12-SCORE
  (L-0.10 T5): the score-build child's transcript and its size record live under `env/`.
- **Draws persisted.** `DRAWS.parquet` (written through L-0.13's `put`, hence 6 dp), key `(registration, draw_set,
  draw_idx)`, holds every draw of the sets that bear on a word or on a filed seed-stability key: `record` and
  `sens` for each row; for P-SCALP-3 also `ladder_touch`, `ladder_deep`, the five `loao_<asset>` sets, and their
  sensitivity-seed twins `ladder_touch_sens`, `ladder_deep_sens` and `loao_<asset>_sens`. Columns: `draw` (6 dp),
  `draw_hex` (`float.hex`, exact), `seed`, `n_boot`, `cluster_kind`, `n_values`, `n_clusters`, `values_sha256`,
  `draws_sha256`, the collar and the as-of columns. Every other beside-print files its `seed` and `draws_sha256`
  only. `F-BOOT [real]` re-derives `lo` and `p` from `draw_hex`.
SOURCE: `research_outputs/tierc11/scores/` (file set and keys read here: `SCORES.json`, `FAMILY.json`,
`SCORE_MANIFEST.json`); `x_rec/tierc11x/registrations/SCORED_X.json`, `SCORED_X_DRAWS.parquet` (columns read here),
`build_manifest.json` (`float_precision`); `x_rec/scripts/tc11x_score.py:729-750` (`draws_frame`);
`scripts/tierc2_baseline.py:162-188` (the estate's table writer: floats rounded by `_round_floats`, hence
`draw_hex` beside `draw`).
RIVALS: draws not persisted (TC11) — `lo` and `p` can then only be compared with their own printed values. The
ladder and LOAO sets persisted at the seed of record only — not taken: P-SCALP-3's seed-stability keys would then
rest on draws nobody can re-derive.
FAILS-IF: F-GRID `[scores]` (score suite, TC12-SCORE) is RED when `rows` is not the filing's registrations in `seq`
order, `families` not the filing's families, `beside` not the declared set of each row, a row lacks
`size_footnote` or `size_measured`, or a two-sample row lacks one of the four refusal keys; F-DET, F-KEY and
F-COLLAR `[scores]` hold the directory (L-0.20, L-0.21, L-0.16). Planted mutations: a row dropped; a row duplicated;
an undeclared beside leaf; an `arm__` leaf for an arm STATUS does not list; `size_measured` removed from one row.

**L-X.27 THE WRITE LAW: NO CLOBBER, A LOGGED REFILE THAT DROPS NO VERDICT, AN EXIT WORD** — no contract line — the
scorer's write law (answers the question TC11 left as Q1; contract :13 is read by L-0.24)
READING:
- Each output: identical bytes → left alone; absent → written atomically (`.tmp` then `os.replace`); different
  bytes and no `--refile` → written beside as `<stem>_rerun<suffix>`, the record untouched. `DRAWS.parquet` is
  compared by content sha.
- `--refile=<id>` replaces the records only if `<id>` is `AM-<n>` — the id of a heading `## AM-<integer> · …` of
  `LEANS_AMENDMENTS.md` (a section's nickname in a heading is never an id, L-0.5) — or `FIX-<n>`, a key of
  `progress/TC12-FIX.json`. It appends one line to `REFILE_LOG.jsonl`: the id, each replaced file's sha before and
  after, and for `SCORES.json` the counts of leaves added, removed and changed, the changed leaves split into
  numeric and non-numeric with their JSON paths. The question TC11 left open as Q1 is thereby answered by a file.
- **A refile never drops a verdict.** Before a record is replaced under `--refile=<id>`, every `rows[]` leaf whose
  `verdict_of_record`, `n`, `point`, `lo`, `hi` or `p_num` will change is appended whole to `scores/SUPERSEDED.jsonl`
  (append-only, tracked) with the refile id and the scorer and regbook shas. The fresh leaf carries `superseded[] =
  [{id, verdict_of_record, n, point, lo, hi, p_num, p_den, book_sha256}]`, the qualifier `RE-SCORED AFTER <id>`,
  and one §0 line per entry under its cell: `before <id>: <word> · n … · point … · [lo, hi] · p …`.
- **A regbook rebuilt before TC12-SCORE is not silent either** (L-0.10 T7): `superseded[]` also lists every
  quarantined `regbooks/<ID>/scored.json` sidecar under `research_outputs/tierc12/_det_partial_*/` with its
  `book_sha256`, `n`, `sum_net_r` and AP id (the sidecar's own numbers, no ruler), printed the same way with the
  qualifier `REBUILT AFTER FIRST BUILD (AP-n)`. The point estimate of a registered book is visible before
  TC12-SCORE — a sidecar files `n` and `sum_net_r` — so a rebuild after that look leaves its trace on the row.
- The exit code is the bitwise OR of TC11's flags, read by `ast` from `scripts/tierc11_score.py:301-302` (the
  literal pinned by its node sha, L-0.24): a registered row HALTed · a Tier-E leaf halted · a registration ABSENT ·
  a no-clobber refusal; nothing masks another. `--dry-run` validates every input and interface, calls no ruler and
  writes nothing.
- Two subprocess runs into `_det_score/`, under the two `PYTHONHASHSEED` values of the estate's F-DET law (TC11
  L-F.1's first literal and the tier's seed of record), are byte-equal to each other and to the records; no clock,
  worker count or load average appears in any output.
SOURCE: `scripts/tierc11_score.py:2611-2634`, `:2648-2665`, `:2450`; `research_outputs/tierc11/LEANS.md:520-521`
(L-F.1); `research_outputs/tierc11/BUILD_DRAFT.md:5943`, `:5988` (MINOR-9 and Q1);
`x_rec/scripts/tc11x_score.py:995-999` (X overwrites — not taken);
`exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:16-18` (resume law item 3: a verdict computed before is printed
BESIDE the fresh value, never re-worded, never re-chosen), carried by contract :5.
RIVALS: X's overwrite; TC11's unlogged `--refile` — the cause of Q1. A refile that logs shas and leaf counts only —
not taken: the old word, point and interval would survive in no record, and a fix chosen after a look would leave
no trace on the row.
FAILS-IF: F-EXIT (score suite, TC12-SCORE) is RED when a differing output is overwritten without `--refile`, a
`--refile` with an unknown id or a nickname is accepted, a refiled leaf whose word or numbers changed has no line
in `SUPERSEDED.jsonl` or no `superseded[]` entry, or a flag is masked; F-DET `[scores]` is RED on any byte; planted
mutations: one byte bent in a record before a re-run; `--refile=AM-V2`; a refile in a scratch twin with the
append to `SUPERSEDED.jsonl` removed; a pid salt; a set-iteration line.

---------------------------------------------------------------------------------------------------------------
### D · CLOSE

**L-X.28 THE REPORT AND ITS ORDER** — "CLOSE: exchange/reports/BUILD_2026-10-08_TIERC12_VALUE_AREA.md — §0 VERDICTS
FIRST: the five rows with their labels, the VA chop table (with-vs-against), the feasibility mirror, the ledger's
appended rows · the families · Stage V pins and the traverse table · the VA stack whole · the scalper's
fill-sensitivity and twins · findings-not-fixed · BOX-COST · LEDGER_APOLLO append" (:126-129)
READING:
- Drafted OFF-BUS at `research_outputs/tierc12/BUILD_DRAFT.md` by the close generator — two modules,
  `scripts/tierc12_close.py` (the deterministic renderer) and `scripts/tierc12_close_acts_template.py` (the text of
  the acts and nothing else, L-X.33) — which writes only its named outputs (the draft, the staged append,
  `close/S5_FINDINGS_NOT_FIXED.{json,md}`, `close/BOX_COST.{json,md}`, `close/TRACES.json`,
  `close/COMPUTE_LEDGER.json`, `close/close_acts.sh`), never under `exchange/`, and never commits, pushes or calls
  `publish()`. It reaches its destination only through `close_acts.sh` (LAW 5). Both modules are RENDERERS under
  L-0.17: they are held on their output by the trace law of L-X.29.
- The contract's named parts keep the contract's order; sections the standing conventions require are placed
  where they break none of it:

  | § | content |
  |---|---|
  | header | title = contract :1; the contract path and prefix sha; executor, seed, branch; the scored window and both pins; the reading rule; the size line (FLAGGED when over the wire); a status stamp filled at close |
  | **0 · VERDICTS FIRST** | 0.1 the five rows with their labels — `scores/S0_VERDICTS.md` byte for byte, in filing order, in the columns frozen below; under each row the lines that stand under its cell (L-X.13), under P-SCALP-3 the lines of its kill first (L-X.9) · 0.2 the VA chop table, the with-vs-against cut: `VA_CHOP_ALIGNMENT` whole, collared · 0.3 the feasibility mirror whole: the five words against X's record, the rows of the other eras beside (O-17), the collared leaf `licence_at_maker_pin` beside the 1h maker word (O-19), and the sentence that the licence was earned on X's record machine, not on V2 (O-16, D-2) · 0.4 the ledger's appended rows: `LEDGER-BOOKS` and `LEDGER-ROWS` whole, the four books side by side, unscored |
  | 1 · THE FAMILIES | `FAMILY.json` rendered: q; per family m, bar, deciding rank, registrations, tests spent; the verdict law and its rival; the three-families sentence of L-X.2 with `Σ_f m_f · bar_f`; the size footnote beside the three bars; the tier total of `m_looks_this_table` over all collared tables beside the five tests |
  | 2 · STAGE V — PINS AND THE TRAVERSE TABLE | `VA_PINS` and `TRAVERSE` whole, the strict-INSIDE twin beside T of record |
  | 3 · THE VA STACK WHOLE | `va_stack`, every cell (L-V.24) |
  | 4 · THE SCALPER — FILL-SENSITIVITY AND TWINS | the P-SCALP-3 verdict text re-quoted under the registered marker (L-X.29); `S_FILL_SENSITIVITY`, the twins' leaves (`taker_twin`, `haircut`, `taker_twin_haircut`), `S_MISS_GRID` and `S_REGIME` whole; pointers to `stage_s/STAGE_S.md` for `S_FUNNEL` and `S_SLICES` |
  | 5 · THE OTHER STAGES | D (substrate, fees, pins) · C (the control and the strip) · G (its four grids whole: `G-BRD`, `G-BRD17`, `G-X16P`, `G-X16B`) · R and L (pointers to their stage documents) |
  | 6 · FIXTURES | the roll: suite, tally (GREEN · RED · NOT RUN), transcript sha; the contract's names first |
  | 7 · FINDINGS — REPORTED, NOT FIXED | L-X.30 |
  | 8 · BOX-COST AND COMPUTE COST | L-X.31, with the seven-column file-disposition table |
  | 9 · DISCLOSURES, AMENDMENTS, RULINGS, VETOES, OPEN QUESTIONS, WHAT THIS BUILD IS NOT | every line of `DISCLOSURES.md` (D-1 … D-12) and of `DISCLOSURES_BUILD.md`; one line per amendment; O-1..O-32, one line each ("each is carried into the build report as a reading"); O-32's defaults that stand; the veto tokens of :135-137, each with the value in force (from `pins/PIN_REGISTER.json`) and "no veto received" or the operator's quote; every OPEN TO OPERATOR item of the frozen LEANS with its default; contract :132-134 quoted |
  | 10 · THE LEDGER APPEND | the staged append, verbatim, inside one fence |
  | 11 · STATE PUSH AND THE CLOSE ACTS | the push stamp; the acts' step list; the last line `Operator: click Sync now.` |

- **§0.1's columns, frozen now:** `seq | registration | family · m · bar_cell | era · n (n_base) · n_clusters |
  point | 90% [lo, hi] | p_num/p_den | LOAO line | verdict_cell`; then, under each row, its `disclosures[]` lines,
  its `superseded[]` lines, and its `size_footnote` as the last line (L-X.13, L-X.14, L-X.27). A Tier-E statistic
  printed inside a §0 row — the LOAO line on the four rows where it decides nothing, and the leaf
  `licence_at_maker_pin` in P-SCALP-3's verdict text — carries L-0.16's inline string "TIER-E — a SELECTION, not a
  result — gates nothing". Which numbers §0 shows per row is not a choice left to render time.
- **"Whole", frozen by KIND, not by size:** a grid (a table whose cells F-GRID declares) prints every cell in a
  document of record; a per-trade, per-instant, per-bar or per-draw table is pointed to by path, file sha, row
  count and key, never inlined. The kind of every table is typed in the generator before any book exists.
- **The whole-versus-pointed map, frozen now (OD-18).** Printed WHOLE IN THE REPORT: §0.2 `VA_CHOP_ALIGNMENT`; §0.3
  the mirror; §0.4 `LEDGER-BOOKS`, `LEDGER-ROWS`; §1 the families; §2 `VA_PINS`, `TRAVERSE` (with the strict-INSIDE
  twin); §3 `va_stack` (L-V.24, nothing else); §4 `S_FILL_SENSITIVITY`, the twins' leaves, `S_MISS_GRID`,
  `S_REGIME`; §5 `G-BRD`, `G-BRD17`, `G-X16P`, `G-X16B`. Every other grid is printed whole in its STAGE DOCUMENT OF
  RECORD and the report carries one pointer row per grid (path, sha, cell count): `VA_CHOP` →
  `stage_r/dir/STAGE_R_dir.md`; the `TWO_TRADES_*` family → `va/trades/TWO_TRADES.md`; `ERA_tables` → `era/ERA.md`;
  `S_FUNNEL`, `S_SLICES` → `stage_s/STAGE_S.md`; `SCORES.json beside` → `scores/BESIDE.md`. A report may point to a
  grid printed whole in its stage document; that is not an abbreviation (L-0.15). No operator choice is made at
  render.
- **Cap.** The generator still HALTs if the draft exceeds the per-file cap parsed from
  `publish_exchange.POINTER_RULE` (`(\d+) MB per file`, decimal MB — TC11's reading, the stricter of the two caps
  on disk); under the frozen map that is a build defect to report, not a choice of what to show.
- **Precedence where conventions collide.** CONVENTIONS §3.2 ends a document on the file-disposition table and
  §3.1 on the ledger entry; the contract names a final line. The operator's ratified contract outranks both: the
  table sits in §8, the append in §10, and the last line of the report is the contract's.
SOURCE: contract :126-131; `scripts/tierc11_close.py:24-45` (the generator's output law), `:2507-2514` (the cap);
`x_rec/tierc11x/LEANS_X.md:2361-2405` (LX-C.1), `x_rec/tierc11x/LEANS_X_AMENDMENTS.md:593-606` (AM-X28);
`exchange/status/CONVENTIONS.md:13`, `:324`, `:342`; `exchange/README.md:21`; `exchange/reports/README.md:6`;
`exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:21-22` (LAW 5); `scout/U9_process_close_fixtures.md` §1.8, U9-19.
RIVALS: the contract's eight parts only — drops sections two standing rules require. Per-instant tables inlined
(TC11's report grew past the wire many times over). A whole-or-pointed choice made per table at render, or left to
the operator when the cap HALTs — a choice made after the verdicts are known; the map is frozen here instead
(L-0.10 T4). Every grid whole in the report — not taken: the era tables and the two-trades family alone exceed the
per-file cap (X's era document for one book is on file at 422,116 B, `x_rec/tierc11x/era/X4.md`).
FAILS-IF: F-S0-FIVE (close suite) is RED when §0.1 is not `S0_VERDICTS.md` byte for byte, its rows are not the
filing's registrations in filing order or not in the frozen columns, a word disagrees with `FAMILY.json`, a label
is absent, a row lacks its `size_footnote` or carries a `size_measured` that is not its entry of
`env/SIZE_MEASURED.json`, a row with a `REFILE_LOG.jsonl` entry or a quarantined sidecar lacks its `superseded`
line, D-1 or either key-overlap line is absent under its `selection_hazard` cell, or P-SCALP-3's fill-sensitivity
row is absent. F-FORM (close suite) is RED when a named part is missing or out of order, a grid on the WHOLE list
is not printed whole (its marker's cell count ≠ its data rows), a pointed grid has no pointer row or its stage
document does not print it whole, or the last line is not the contract's. Planted mutations: a label stripped from
one §0 cell; the footnote removed under one row; §1 and §2 swapped; `G-BRD17` replaced by a pointer; a line added
after the final line.

**L-X.29 THE NUMBER-TRACING LAW AND THE VERDICT-WORD LAW** — "no number typed that a file can supply" (:8); "§0
VERDICTS FIRST" (:126)
READING:
- A number enters the report or the append in exactly one of four ways: (1) `T(key, spec, fmt)` — resolved from
  its record (`spec.kind` ∈ json · parquet · text · git · ast · filesha, with path and selector; a `git` trace is
  resolved through the generator's one read-only git helper `tierc12_close.git_ro`, L-0.22's typed site), formatted
  by a named format, and filed in `close/TRACES.json` with its uses per region; (2) a VERBATIM block behind `<!--
  verbatim: <path>:<line spans> -->`; (3) a `«path:L1-L2»` or `«path#selector»` cite with its `| ` / `+ ` quote
  lines; (4) a marked table `<!-- draft-table: <ID> -->` whose every cell equals its source at the printed precision.
- **F-NUM** scans every digit token of the whole document and of the append's prose. Each is a traced literal used
  exactly its declared number of times, inside a verified block, cite or marked table, a masked token (the mask
  classes — shas, ISO instants, section and reading ids, registration ids, lens names, tier names, repo paths —
  are typed in the fixture and listed in `TRACES.json masks`), or a counted exemption listed with its reason.
- The transcript prints `traces: N · tokens checked: T · mismatches: M`, and CLOSE requires `M = 0`. The three
  counts are filed in `close/FIXTURES_CLOSE.txt` and in `progress/TC12-CLOSE.json`, never only in a commit subject.
- **The verdict-word pattern** (the one L-0's F-COLLAR and F-NOT also use): X's `VERDICT_RX` with X's own closure
  phrase replaced by TC12's two —
  `\b(?:SUPPORTED|PASS|PASSES|FAIL|FAILS|FAILED|[Vv]erdicts?|VERDICTS?)\b|CLOSED BY PRECONDITION|CLOSED FOR GOOD`.
  The bare closure word needs no alternative of its own: it is only ever printed behind `NOT SUPPORTED — ` (L-X.9).
- **F-WORDS.** No line of the report matches that pattern outside (i) §0, (ii) a block under L-0.16's registered
  marker `<!-- registered: <id> -->` whose bytes equal that row's `verdict_text` in `SCORES.json` (§4's re-quote of
  P-SCALP-3 is the one such block outside §0; L-0.16 allows the marker in score documents, in §0 and in that
  verbatim re-quote), (iii) §10's fence, whose bytes equal the staged append, (iv) a verified verbatim block or
  cite quote of a pinned source (§9's lines of the rulings and the disclosures are such quotes).
SOURCE: `scripts/tierc11_close.py:32-41`; `scripts/tierc11_close_fixtures.py:11-14` (F-NUM);
`research_outputs/tierc11/close/TRACES.json` (schema, 231 traces on file per `scout/U9` §1.8);
`x_rec/scripts/tc11x_close_draft_fixtures.py:55` (`VERDICT_RX`), `:151-152`, `:316-329`, `:436`;
`scout/U9_process_close_fixtures.md` H13 (X's count lived only in a commit subject).
RIVALS: digit scan on §0 and the append only (TC11) — leaves the body untraced. Marked tables only (X) — no record
of what was traced.
FAILS-IF: F-NUM is RED on any untraced digit or any trace that does not re-derive; F-WORDS on any stray word;
planted mutations: one digit of a §3 cell changed; a trace's source value moved; `SUPPORTED` written into §5.

**L-X.30 FINDINGS — REPORTED, NOT FIXED** — "findings-not-fixed" (:129)
READING: `close/S5_FINDINGS_NOT_FIXED.{json,md}`, TC11's schema as X extended it: each finding has `id`, `class` ∈
{HARVESTED, MEASURED, LEAN}, `owner` ∈ {operator, executor, ATHENA}, `owner_basis`, `source` (path, field, locator),
`status = "REPORTED, NOT FIXED"`, `text`, `rank`, `also_reported_by`. Laws: the status records what THIS build did;
operator-owned findings rank first; one fact is one finding. Harvest sources, typed in the generator: every
progress record's `blockers` and `notes`, and the non-blocking record `TC12-D.mirror` when it is PARTIAL;
`LEANS_AMENDMENTS.md` and `AMENDMENTS_PROPOSED.md`; `DISCLOSURES_BUILD.md` (the build-time disclosures filed
after the registry froze `DISCLOSURES.md`); the review and judge records' items carried to close; every fixture
transcript's findings, its `FINDING:` lines (a hand sample shorter than the contract's count, or an empty
contract-named category — operator-owned, L-0.14) and its NOT RUN blocks; `scores/REFILE_LOG.jsonl` and
`scores/SUPERSEDED.jsonl`; the ferry's HELD FOR ATHENA list; every OBJECTION and OPEN TO OPERATOR item of the
frozen LEANS; the frozen-estate census `frozen/FROZEN_ESTATE.json` re-asserted path by path (L-0.6; a moved sha
with no attributing foreign commit is a finding against TC12). The md is rendered from the json.
SOURCE: `research_outputs/tierc11/close/S5_FINDINGS_NOT_FIXED.json` (schema `tierc11.close.S5_FINDINGS_NOT_FIXED.v1`,
per `scout/U9` §1.8); `x_rec/scripts/tc11x_close_findings.py:2-46`; `x_rec/tierc11x/LEANS_X.md:2407-2410`.
RIVALS: a free-text section — no owner, no locator, no dedup.
FAILS-IF: F-FNF (close suite) is RED when the md is not the json, a finding lacks a field, an id repeats, a
harvested text does not re-extract from its locator, a typed harvest source holding an item yields no finding, or
an executor-owned finding outranks an operator-owned one; planted mutations: a harvested text edited; a blocker
left unharvested; a `B-1` entry of a scratch `DISCLOSURES_BUILD.md` left unharvested.

**L-X.31 BOX-COST: WHAT IS MEASURED** — "BOX-COST" (:129)
READING: `close/BOX_COST.{json,md}` measures, with `os.lstat` and with git facts read only through
`tierc12_close.git_ro` — the generator's one typed subprocess site (L-0.22: the read-only verbs `rev-parse`, `log`,
`ls-files`, `ls-tree`, `cat-file`, `show`, `merge-base`, each with `--no-optional-locks`) — never a fetch:
- **the file-disposition table** — PATH · EXISTS · TRACKED · COMMITTED · PUSHED · PROTECTED BY · BOX COST — over
  (a) every path in a commit whose subject starts `tierc12(`; (b) every `artifact_shas` path of `PROGRESS.json` not
  in (a); (c) the planned report, sized from the draft; (d) the planned append; (e) every planned
  `exchange/rows/tierc12/**` file and every HELD file; (f) the snapshot, `n/a — outside repo`; (g) the close's own
  uncommitted files; and the two contract files a close step stamps;
- **the box**: the tick set (the `exchange/` index plus `TICK_EXTRA`) now; projected after TC10's, TC11's and X's
  pending closes (their adds sized from their staged files); and after TC12's own adds; each with its level by
  `budget()`'s rule (WARN at or above `WARN_FRACTION`, REFUSE strictly above `REFUSE_FRACTION`) and every box-bound
  file strictly over `FLAG_BYTES` FLAGGED by name;
- **the constants** — `BOX_BYTES`, `WARN_FRACTION`, `REFUSE_FRACTION`, `FLAG_BYTES`, `SCOPE`, `TICK_EXTRA`,
  `POINTER_RULE` — read by `ast.literal_eval` from `scripts/publish_exchange.py` (sha `15eec3d0…a65b`), the module
  never imported;
- **compute cost**: per workflow, agents · tokens · tool calls · wall, read from the harness journals whose
  workflow name starts `tc12-` and filed with each journal's path and sha in `close/COMPUTE_LEDGER.json`; every
  COMPUTE note of the progress records quoted verbatim. Worker counts and load averages appear here and in
  progress records only.
`NAIAD_ALLOW_OVERSIZE_PUBLISH` is never set and REFUSE is never overridden; what crosses WARN is ATHENA's.
SOURCE: `exchange/status/CONVENTIONS.md:342-360`; `scripts/publish_exchange.py:48`, `:95`, `:109-111`, `:128`, `:160`,
`:164`, `:201-220`; `x_rec/scripts/tc11x_close_box_cost.py:19-40`; `scripts/tierc11_close.py:2495-2514`;
`scout/U9_process_close_fixtures.md` §1.8, §1.12.
RIVALS: constants copied — "Take both constants from `publish_exchange` … never a copy" (CONVENTIONS :354).
FAILS-IF: F-BOXCOST (close suite) is RED when the table differs from a re-derivation, a file over the wire is not
FLAGGED, the projection does not re-derive, the md is not the json, or the generator holds a git call outside
`git_ro` or a verb outside its typed list; planted mutations: a constant typed in the generator; a row dropped; a
FLAG removed; a `git fetch` added to a copy of the generator.

**L-X.32 THE LEDGER APPEND** — "LEDGER_APOLLO append (the "maker" ruling verbatim; SAIL HELD; families declared;
in-sample labels carried)" (:129-130)
READING:
- Staged at `research_outputs/tierc12/LEDGER_APOLLO_APPEND.md`; appended to `exchange/status/LEDGER_APOLLO.md` only
  by `close_acts.sh`. The executor never appends (O-12).
- **Format = TC10's `check_format`, mirrored into `scripts/tierc12_close_fixtures.py` and held text-equal to its
  source by a fixture leg:** the block opens with `SEP` (`"\n---\n\n"`); then `=== STATUS_APOLLO — <YYYY-MM-DD> —
  TIER-C12 · <title> ===`, the `LANE      ` line, the `CLASS     ` line; it ends on exactly one `=== END ===`
  followed by one newline; **`Operator: click Sync now.` occurs nowhere in it.** The header regex of record is
  `=== STATUS_APOLLO — \d{4}-\d{2}-\d{2} — TIER-C\d+ · [^\n]+ ===\nLANE      [^\n]+\nCLASS     `. The date is the
  UTC date of TC12's corridor pin (L-D's `AS_OF_PIN.json`); `<title>` is contract :1 after `TIER-C12 · `.
- **Required content, each a `«cite»` verified against its source:**
  1. the "maker" ruling verbatim — `«exchange/queue/2026-10-08_TC12_APOLLO.md:2-4»`;
  2. SAIL HELD — the same lines, with the standing basis `«exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:2-3»`
     and `«exchange/queue/2026-09-24_TC11_APOLLO.md:99»`, contract :133 ("no SAIL act"), and the sentence that
     nothing in this tier is a SAIL act;
  3. families declared — `«…TC12_APOLLO.md:8-9»`, `:52`, `:64`, `:82`, and per family m, bar and tests spent from
     `scores/FAMILY.json`;
  4. the five rows, each under its own text (the contract's lines by `text_lines`) with `«scores/SCORES.json
     #rows[registration=<id>].verdict_cell»` — the cell carries the label (L-X.13's template of that registration);
     P-BRD-1's cell is followed by D-1, cited from `DISCLOSURES.md` (the disclosure stands under that cell wherever
     the cell is printed); P-SCALP-3 also its fill-sensitivity row with the two booleans; one line pointing to the
     report's §0.1 for the other lines under each cell (the key overlaps, the superseded values, the size
     footnote); a CLOSED BY PRECONDITION cell stays number-free;
  5. X's standing pre_seen line, and the licence sentence of O-16 (d);
  6. the rulings enacted (`:12-16`) and what was done under each; the forward ledger's fourth book and the appended
     rows, unscored; the ferry;
  7. INTEGRITY (the fixture roll, F-CTRL, text-before-result, the review attestations); OPEN FOR THE OPERATOR; and
     THE TIER LINE, citing X's landed block.
- Every digit of the prose is traced, cited or masked (L-X.29). Exactly three single-line `⟦STAMP AT CLOSE — …⟧`
  brackets, filled by step 5 of the acts: the commit count and remote state; the ferry of record's WRITTEN / HELD
  FOR ATHENA / FLAGGED counts; the tc11-stamp's result. **Each bracket is rendered at a fixed byte width and its
  fill is padded or truncated to exactly that width, so the stamped append and report have the staged byte
  counts** — the ferry of record reserves the append at its staged size against a box that sits near WARN. The
  width of each bracket is read from the staged file (the length of the pending bracket), never typed, and
  `F-LEDGER-FMT --stamped` STOPS on a stamped file whose byte count differs from the staged one.
- The cite into X's block names the path of record `research_outputs/tierc11x/LEDGER_APOLLO_APPEND.md`, absent
  from the main tree until X merges; at draft time the verifier resolves it through one declared alias to
  `x_rec/tierc11x/LEDGER_APOLLO_APPEND.md` (sha `c63f7a18…b9e3`), and at close (`--check`, `--stamped`) with no
  alias, against the merged file. The line span is located by text at render, never typed.
SOURCE: `scripts/tierc10_close_ledger_append_root.py:84`, `:554-567` [read here];
`scripts/tierc10_close_close_ledger_append.py` (`render_quote`, `parse_quotes`, `verify_quote`; sha `ed286d20…ca47`);
`x_rec/scripts/tc11x_close_fixtures.py:124`, `:171`, `:205` (X's copies); `research_outputs/tierc11/LEDGER_APOLLO_APPEND.md`
(the form; sha `227317d1…14e1`); `x_rec/tierc11x/LEANS_X.md:2444-2478`; `exchange/status/CONVENTIONS.md:324`;
`scout/U1_rulings_close_state.md` §1.9, §1.10, C-5, R-21.
RIVALS: import TC10's modules for the format law (TC11's way) — O-3 and O-4 rule mirror-and-hold-equal. A header
`TIER-C12-…` variant — fails the regex.
UNVERIFIED: that the line span of X's tier line survives X's own stamp fill; step 0 re-verifies every cite against
the sources as they stand then and STOPS on a moved line.
FAILS-IF: F-LEDGER-FMT (close suite; a reading's addition — the contract's F-LEDGER is L-L's and is matched by exact
FID) is RED when the format law fails, a cite does not verify, a required item is absent, the stamp count is not
three, a filled bracket changes the file's byte count, or §10 of the draft is not the append byte for byte;
planted mutations: the final line written inside the block; the LANE line removed; one quoted character changed;
the "maker" cite dropped; D-1 dropped from under P-BRD-1's cell; a stamp fill one byte longer than its bracket.

**L-X.33 CLOSE ACTS: THE STEP LIST** — "Q6 the close acts remain the operator's keystrokes" (:14-15);
"publish_exchange; STATE push; bright paths; final line" (:130)
SEAM SETTLEMENTS (`review/SEAM_PASS.json`, 2026-10-09 — part of this reading; each line governs where the text below is silent or differs):
- [seam 64] step 2 names the invocation: `tierc12_ferry_fixtures.py --of-record` (act mode), transcript `ferry/of_record/F_ROWS_AT_CLOSE.txt`, belonging to no record.
READING: the generator writes `research_outputs/tierc12/close/close_acts.sh` (tracked; `set -euo pipefail`; no
force, no reset, no stash, no clean). The executor never runs it, never pushes, never calls `publish()`, never
merges, never moves a report onto the bus and never appends to the ledger (O-12). `--check` runs step 0 only.
- **Where the acts' text lives.** In `scripts/tierc12_close_acts_template.py`: string constants holding the text
  of `close_acts.sh` and nothing else — no call, no subprocess, no import beyond `__future__` — imported only by
  `scripts/tierc12_close.py`, which substitutes the generated lists (the sources, the paths, the step-2 and step-4
  calls) into it. The push string and the `publish()` invocation are therefore TEXT in exactly one module; L-0.26's
  F-NOT leg ACTS exempts, by a typed list of one, the string constants of that module and the generated
  `close/close_acts.sh`, and is RED on such a string, an `import publish_exchange` or a call named `publish`
  anywhere else in TC12's sources, fixtures included.
- **Step 0 · refusals — nothing changes, each prints its reason:**
  a. the main tree, on `v12-v1-census`; the index clean;
  b. **the three prior blocks landed BY BYTES, in order:** for TC10, TC11 and X, the append committed at `HEAD`
     carries no pending stamp and its committed bytes occur exactly once in the committed
     `exchange/status/LEDGER_APOLLO.md`, at offsets TC10 < TC11 < X; the ledger's working copy equals `HEAD`; no
     `TIER-C12 · ` header is in it yet. A header grep is never used (X's header reads `TIER-C11 · TC11-X`);
  c. the three predecessors' reports are tracked under `exchange/reports/`;
  d. **SOURCES == HEAD:** every TC12 close source is present, tracked and identical to `HEAD`; the list is
     generated (the draft, the append, the `close/` files, `scores/*`, `registrations/*`, the ferry's staged
     manifest, `LEANS.md`, `LEANS_AMENDMENTS.md`, `DISCLOSURES.md`, `DISCLOSURES_BUILD.md` where it exists,
     `PROGRESS.json`, the close generator's two modules, the ferry and stamp scripts);
  e. the destination report and `exchange/rows/tierc12/` are absent; the draft has no open placeholder; the three
     stamps and the report's push stamp are pending;
  f. both contracts are as pinned: TC12's prefix with an empty tail (L-X.16); TC11's contract at the `bytes` and
     `sha256` that `progress/TC12-R0.json["frozen_estate_shas_at_r0"]` files for its path, with no `BUILT` line;
     `research_outputs/tierc11/scores/SCORES.json` at the sha the same key files for it (Q1);
  g. ATTEST-ORDER (L-X.21) and `F-LEDGER-FMT --check` on the pre-stamp append as the sources stand now.
- **Step 1 ·** `git push origin v12-v1-census`, then `origin` verified equal to `HEAD`. On failure STOP: nothing
  has changed.
- **Step 2 · the ferry of record** (O-24; L-L's law): pinned at the then-`HEAD` by sha, the box measured with the
  three closes inside it, only TC12's own close adds reserved; the WRITTEN set copied sha-equal from the off-bus
  staging into `exchange/rows/tierc12/`, the rest listed HELD FOR ATHENA; then its FRESH leg and F-ROWS. On failure
  the files it wrote are moved aside (nothing deleted) and the script STOPS.
- **Step 3 · LAW 5:** the draft copied to `exchange/reports/BUILD_2026-10-08_TIERC12_VALUE_AREA.md`, sha equal
  across the copy; `git rm` of the draft committed alone as `tierc12(CLOSE): LAW 5 — …`.
- **Step 4 · the two BUILT stamps:** the tc11-stamp (L-X.34; the step exists in the generated script only when the
  build-time proof was GREEN), then TC12's own (L-X.35).
- **Step 5 ·** every `⟦STAMP AT CLOSE⟧` filled from git and the ferry manifest, then `F-LEDGER-FMT --stamped`.
- **Step 6 ·** `cat` the append onto the ledger; the ledger's tail checked equal to the append byte for byte.
- **Step 7 ·** the non-exchange residue staged by explicit path with `git add -f` and committed in the same
  command sequence, `tierc12(CLOSE): …`. No exchange path is ever staged by the script (CONVENTIONS :415).
- **Step 8 ·** `publish()` by the invocation of record (CONVENTIONS §3.4), and the push result STATED.
- **Step 9 ·** bright paths, then the final line.
Every commit subject starts `tierc12(`; none starts `tierc10`, `tierc11(` or `tc11x(`, which feed the other
tiers' stamp counts.
**The scratch proof of the script (F-CLOSE-SCRIPT).** The acts' only executions are `bash -n` and runs of a SCRATCH
COPY with every path and cwd asserted outside both trees: step 0 (`--check`) against scratch repositories, and
steps 1-7 against a sandbox clone with a local bare origin, cut before `publish()`. The generated file in the main
tree is never executed by the executor (L-0.26). The scratch copy is produced by the same generator with two typed
substitution points — the step-2 ferry planner call and the step-4 stamp call are replaced by stubs that write
their expected outputs (a copy list naming one planted CSV; a planted `BUILT:` line with no re-pin) — and proves
ORDER and the STOP guards only: the planner of record needs the git-ignored sources and the off-bus staging, which
no clone holds, and the stamp's proof is a roll of TC11's suites. The real planner is proven by L-L's F-ROWS
`[ACT]` and the real stamp by F-TC11-STAMP. Four blocks: `[SYNTAX]` (`bash -n` on the generated file); `[STATIC]`
(the push only at step 1, `publish()` only at step 8 and only by the invocation of record, the final line last and
nowhere else, the template module holding text only); `[STEP0]` (the planted gates below); `[SANDBOX]` (the order
of steps 1-7, with the real repository's `HEAD`, index and porcelain equal before and after). The sandbox run is
TC11's F-CLOSE-ORDER form and performs no operator act.
SOURCE: `research_outputs/tierc11/close/close_acts.sh` (sha `7f601f81…e2ba`; step 0 `:47-67`, LAW 5 `:75-89`, the
stamp `:91-109`, the residue `:117-122`); `x_rec/tierc11x/close/close_acts.sh` (sha `02191457…1940`; by-bytes tier
check `:142-180`, the ferry `:198-253`, the tail check `:295-303`, `git add -f` `:307`);
`exchange/status/CONVENTIONS.md:399`, `:413`, `:415`, `:419`; `scripts/tierc11_close_fixtures.py:34-41`
(F-CLOSE-ORDER); `x_rec/scripts/tc11x_close_fixtures.py:40-48` (F-CLOSE-SCRIPT); O-10, O-12, O-24;
`scout/U1_rulings_close_state.md` §1.7, R-17, H-8; `scout/U9_process_close_fixtures.md` U9-21.
RIVALS: a CERTIFIED_TIP pin (X) — meaningful only on a branch of its own; the main branch moves every day. Header
greps for tier order (TC11) — cannot tell TC11 from TC11-X. The acts' text as a constant inside the generator — not
taken: OD-18 keeps it in a module that holds only text, so the exemption from F-NOT covers no code. The sandbox run
with the real planner and the real stamp — not taken: it STOPS at step 2 in any clone and would cost two more rolls
of TC11's suites per run. The order held by the static law alone — not taken: a static law does not prove that a
STOP at one step leaves the later ones unrun.
FAILS-IF: `F-CLOSE-SCRIPT [SYNTAX]` is RED when `bash -n` fails; `[STATIC]` when the push, `publish()` or the final
line stand anywhere but their step, or the template module holds a call or an import beyond `__future__`;
`[STEP0]` when a planted gate does not STOP at step 0 before any push — today's ledger (the three blocks absent);
TC11's block before TC10's; a block with a pending stamp; a dirty index; a source differing from `HEAD`; the
destination present; TC11's contract already stamped; `SCORES.json` moved; `[SANDBOX]` when the stubbed scratch
copy does not push, ferry, move sha-equal, stamp, append and commit in that order, a path or cwd of the run lies
inside either tree, or the real repository changes. Planted mutations of the script itself: the by-bytes check
replaced by a header grep; `publish()` moved ahead of the append; the final line printed twice; a call added to a
copy of the template module (UNEARNED); the generated file of the main tree handed to the sandbox runner.

**L-X.34 THE TC11-STAMP, AND ITS SCRATCH PROOF TREE** — "stamp TC11 BUILT and re-pin its registry files
["tc11-stamp"]" (:13)
READING: under O-10 — a close act, the line appended last, the cascade proven GREEN in a scratch tree outside both
trees. The LAW of the stamp (where the line goes, which bytes move, what stays historical, what GREEN means) is
L-0.24's; this reading fixes how CLOSE and the acts HOST it, and restates the law only as far as the host needs it.
- **The line.** `BUILT: exchange/reports/BUILD_2026-09-24_TIERC11_EVENTS.md · <the commits whose subject starts
  tierc11(, read from git at the act>`, appended as the last line of `exchange/queue/2026-09-24_TC11_APOLLO.md`, the
  file required to end in `\n` first. Lines 1-103 stay byte-identical, so TC11's nine text slices, nine payload
  shas and its chain head (`research_outputs/tierc11/registrations/REGISTRY_PIN.json["head"]`) do not move; only
  the whole-file sha does. **Because the commit range is read at the act** (TC11's own close adds `tierc11(`
  commits), the stamped file's sha is known only then: a build-time proof proves the mechanism, and the act must
  re-prove on the very bytes it will write.
- **The re-pin** is a replacement of pinned shas, old → new, to a fixed point, inside an ALLOWED set and nowhere
  else — the contract and L-0.24's sets (a)-(f): `research_outputs/tierc11/registrations/{REGISTRATIONS.json,
  REGISTRY_PIN.json}` (the top-level contract-sha leaf only); the module-level string constants of
  `scripts/tierc11_*.py` that equal a moved sha (located by `ast`; on file: `tierc11_registrations.py:24`,
  `tierc11_score.py:220`, `:224`, `tierc11_score_fixtures.py:263`, `tierc11_stage_g.py:170`,
  `tierc11_stage_t_brk.py:141`); the records TC11's own scorer and suites regenerate from them
  (`scores/REGISTRY_CHECK.json` and the scorer's other refiled outputs, and the transcripts and manifests that
  print a moved sha); `research_outputs/tierc11/PROGRESS.json`. Q2 names three of these; the others are the pins
  TC11's verifier reads, without which "re-pin" leaves that verifier RED.
- **NEVER moved** (a HALT if the cascade touches one): `scores/SCORES.json`, `scores/FAMILY.json`,
  `scores/BASE_IDENT.json`, any regbook, any parquet, TC11's `LEANS.md` and `LEANS_AMENDMENTS.md`, anything under
  `research_outputs/tierc10/` or `research_outputs/tierc11x/`, any other file under `exchange/`. Every other file
  that quotes an old sha is HISTORICAL and is listed, not edited.
- **TC12 pins none of the moved files by their whole-file sha** (L-0.24): the literals this section reads from
  `scripts/tierc11_score.py` are pinned by AST node (L-X.24, L-X.27), TC11's registry by its chain head (L-X.19),
  and the shim's `E.tc11_record` accepts TC11's `PROGRESS.json` at its R0 sha or at the value this reading's map
  names for it once the map reads `applied: true`. TC12's scorer, Stage G builder and resume suite therefore
  re-pass after the operator's keystrokes.
- **Two phases, both in `scripts/tierc12_tc11_stamp.py`** — a tool that never imports `E`, whose one typed
  subprocess site is `tierc12_tc11_stamp.run` (L-0.22: `git worktree add --detach` and `git worktree remove
  --force` on the scratch proof tree, and the interpreter running TC11's suites with cwd asserted inside that
  tree). The line's text is handed to it as an argument: composed at build time by the close generator through
  `git_ro`, and at the act by the script from the same read-only verb.
  - `--prove`: the proof tree is a DETACHED LINKED WORKTREE of the main repository at `HEAD` under a scratch
    directory outside both trees (`git worktree add --detach`; removed with `--force` at the end; no ref and no
    main-tree file moves), so that TC11's `_main_tree()` resolves the real main tree and the TC10 allow-list is
    read there read-only, as in TC11's certified lens runs; TC11's ignored parquet and `TC10_STAGED` are staged by
    the attest tool's globs. A `[PRE]` leg first runs TC11's sweep on the UNSTAMPED proof tree and must be GREEN; a
    RED PRE leg is reported `PROOF ENVIRONMENT DEFECT` and is not a tc11-stamp result. Then the line is appended,
    the replacement run to its fixed point, and TC11's scorer and the suites of TC11's last sweep run THERE, under
    TC11's snapshot read-only. GREEN iff the PRE leg is GREEN, every suite is GREEN with byte-identical
    transcripts on a second run, the changed set ⊆ ALLOWED, the three NEVER-moved score files are byte-identical,
    TC11's chain head is unchanged, and the main tree's `HEAD`, index and porcelain are equal before and after. It
    writes a transcript and a map: `head_at_proof`, `proof ∈ {GREEN, RED, PROOF ENVIRONMENT DEFECT}`, `applied`
    (false), old → new sha per replaced pin, each moved file's sha before and after, the historical list.
  - `--apply`: only after a GREEN `--prove` at the same `HEAD`; asserts each pre-image in the main tree equals the
    proof tree's pre-image, copies the proven post-images byte for byte, and rewrites the map with `applied: true`.
    No TC11 code runs in the main tree.
- **When.** At TC12-CLOSE the executor runs `--prove` once and files `close/TC11_STAMP_PROOF.txt` and
  `close/TC11_STAMP_MAP.json`. **If that build-time proof is not GREEN, the generated `close_acts.sh` carries no
  stamp step at all**, the map stays `applied: false` with its `proof` word, the finding says which of the two it
  was — the cascade RED, or a PROOF ENVIRONMENT DEFECT that says nothing about the cascade — and the ruling returns
  to the operator (L-0.24). If it is GREEN, step 4 of the acts (after the three blocks have landed) runs `--prove`
  again at the then-`HEAD`, then `--apply`; the non-exchange paths, the map among them, are committed as
  `tierc12(CLOSE): tc11-stamp — …`, and the contract itself is left for `publish()`.
  Each proof costs three rolls of TC11's suites — the PRE leg, the stamped run and its repeat (their per-suite
  walls are on file in `research_outputs/tierc11/PROGRESS.json stages[].fixtures[].wall_seconds`); the acts print
  that before starting it.
- **If the act-time `--prove` is RED** nothing is applied — no partial re-pin is ever written — the acts continue,
  and the append's third stamp reads `tc11-stamp NOT APPLIED — proof RED` with the transcript's path (see OPEN TO
  OPERATOR).
- TC11's close generator and its fixtures stand outside the cascade: that generator refuses a contract that
  carries a `BUILT` line, and its HALT in the proof tree is printed as EXPECTED (L-0.24).
SOURCE: L-0.24; O-10; contract :13; `research_outputs/tierc11/BUILD_DRAFT.md:5943-5945`, `:5989` (Q1, Q2,
FN-M-QUEUE-STAMP); `scripts/tierc11_registrations.py:24`, `:186-188`, `:244-245`; `scripts/tierc11_score.py:220-226`,
`:418-446`; `scripts/tierc11_worktree_attest.py:65`, `:70-71`, `:113` (the staging globs and `TC10_STAGED`);
`scripts/tierc11_env.py:218-230` (`_main_tree`: the tree itself unless `.git` is a `gitdir:` file), `:1170-1176`
(`tc10_record` returns `MAIN_TREE / rel`) [read here, as text]; `exchange/queue/README.md:8-12`;
`scout/U1_rulings_close_state.md` §1.4-§1.6, R-1 … R-5, H-7; `scout/U9_process_close_fixtures.md` C5, U9-8, H10.
RIVALS: stamp under RATIFIED, where every earlier queue stamp sits — shifts every line TC11's registry cites. Q2's
three files alone — TC11's verifier then HALTs on its typed constants. Run TC11's scorer `--refile` in the main
tree — executes frozen code in place. A `git clone --local` as the proof tree (O-10's "scratch clone" read
literally) — not taken: in a clone `.git` is a directory, TC11's `_main_tree()` then resolves the clone itself,
and the TC10 records TC11's suites read through `tc10_record` are untracked in main and absent from any clone, so
TC11's sweep would go RED before a stamp is tested; O-10 is read as "a scratch tree outside both trees" (listed
for the orchestrator).
UNVERIFIED: (i) that TC11's scorer, re-run after the replacement, leaves `SCORES.json`, `FAMILY.json` and
`BASE_IDENT.json` byte-identical — asserted inside `--prove`, a HALT otherwise; (ii) that the suites of TC11's last
sweep re-pass in a detached linked worktree with the staged parquet — the PRE leg's subject before the stamp and
the proof's own subject after it; (iii) the full ALLOWED closure (which transcripts and manifests print a moved
sha) — enumerated by `--prove`, and anything outside ALLOWED is RED. None of the three was run while drafting (no
TC11 module may be executed here).
FAILS-IF: F-TC11-STAMP (legs defined in L-0.24; hosted by the close suite) is RED when (0) PRE: the unstamped sweep
is not GREEN in the proof tree — reported `PROOF ENVIRONMENT DEFECT`, never as a stamp result — or when, in the
proof tree, TC11's chain head moves, a NEVER-moved file changes, the changed set leaves ALLOWED, a suite is RED,
`--apply` runs without a GREEN proof at the same `HEAD`, the proof tree or the cwd of a run lies inside either
tree, or the main tree's `HEAD`, index or porcelain changes; planted mutations: the line inserted at line 5; a
replacement applied to `SCORES.json`; `--apply` against a tree whose pre-image differs by one byte; one staged
parquet removed from the proof tree before the PRE leg (the tool must report `PROOF ENVIRONMENT DEFECT` and no
stamp result).

**L-X.35 TC12's OWN BUILT STAMP** — no contract line — the queue's rule 6 (`exchange/queue/README.md:8-12`)
READING: at step 4 the acts append `BUILT: exchange/reports/BUILD_2026-10-08_TIERC12_VALUE_AREA.md · <the first and
last tierc12( commits and their count, read from git> · <the fixture roll's tally>` as the last line of TC12's
contract. L-X.16's prefix pin makes this free: no slice, sha or head moves, `PROGRESS.json` names the contract by
its prefix and does not move either, and the question TC11's contract left open is not asked of TC12. The line
reaches the record through `publish()`.
SOURCE: `exchange/queue/README.md:8-12`; `research_outputs/tierc11/BUILD_DRAFT.md:5945` (FN-M-QUEUE-STAMP);
`scout/U1_rulings_close_state.md` §1.6, R-18.
RIVALS: leave it unstamped — the queue counts it as ratified-unbuilt and the finding recurs.
FAILS-IF: F-CONTRACT-PIN (L-X.16) is RED when a scratch copy of the contract with a `BUILT:` line of this form
appended as its last line changes any slice, payload sha, chain head or verifier finding, or moves a byte of a
re-derived `PROGRESS.json`; planted mutation: the same line inserted under `RATIFIED` (must HALT
`CONTRACT-PREFIX`).

**L-X.36 "publish_exchange", "STATE push", "bright paths", THE FINAL LINE** — "publish_exchange; STATE push; bright
paths; final line: "Operator: click Sync now."" (:130-131)
READING:
- **publish_exchange** = `publish(repo, date)` of `scripts/publish_exchange.py`, called only by the acts at step 8,
  only through the invocation written out in CONVENTIONS §3.4; it stages `exchange/**`, guard-checks the whole
  index, commits `exchange: auto-publish <date>` and pushes the branch. In TC12's sources that invocation exists
  only as text in the acts' template module (L-X.33); no TC12 module imports `publish_exchange` (its constants are
  read as text, L-X.31).
- **STATE push** = the push result stated plainly, never a push by the executor: the acts print `PUSH RESULT:
  SUCCEEDED — …` or `PUSH RESULT: FAILED — …` after step 1 and after step 8, and the report's §11 carries a
  `⟦STAMP AT CLOSE⟧` filled with step 1's result (a fixed-width bracket, L-X.32). The report also states that the
  daily routine pushes the whole branch whenever the route works, so "no push without the operator's word" cannot
  be enforced in the main tree — a finding, not hidden.
- **bright paths** = the on-screen close of CONVENTIONS §3.3: the exact filenames and full repo paths the operator
  must carry, printed in bright colour (`printf '\033[1;33m%s\033[0m\n'`, one per line): the report; the ledger; the
  two stamped contracts; `exchange/rows/tierc12/ROWS_MANIFEST.md`; the findings; BOX_COST; the stamped append; the
  stamp map; `PROGRESS.json`; and `origin/v12-v1-census = <short sha>`.
- **The final line** `Operator: click Sync now.` is the last line the acts print and the last line of the report,
  and occurs nowhere in the ledger append.
SOURCE: `research_outputs/tierc11/LEANS.md:542` ("STATE push" = state the push result plainly);
`x_rec/tierc11x/LEANS_X.md:2499-2502`; `exchange/status/CONVENTIONS.md:399` ("states on screen whether the push
SUCCEEDED"), `:407` (BRIGHT COLOURS), `:413`; `research_outputs/tierc11/close/close_acts.sh:126-140`;
`x_rec/tierc11x/LEANS_X_AMENDMENTS.md:593-606` (AM-X28); `scripts/publish_exchange.py:565`;
`scout/U1_rulings_close_state.md` §1.9, C-14, H-2.
RIVALS: the executor pushes or publishes — no ruling grants it, and Q6 keeps the acts the operator's.
FAILS-IF: `F-CLOSE-SCRIPT [STATIC]` (L-X.33) is RED when `publish()` stands anywhere but step 8 or outside the
invocation of record, a `PUSH RESULT:` line is missing after step 1 or step 8, a bright path is missing, or the
final line is not the last line the acts print; F-FORM (L-X.28) is RED when it is not the report's last line.
Planted mutation: the final line moved inside the append (F-LEDGER-FMT must turn RED as well).

---------------------------------------------------------------------------------------------------------------
### FIXTURES DEFINED BY THIS SECTION

Harness: L-0's `scripts/tierc12_fx.py` (`prove`: the BREAK leg first, and a break that does not go RED voids the
fixture; `plants`: one at a time, CAUGHT only when a finding names the intended detector; a crash is a fixture
defect). A leg is one `prove` call and one transcript block, with the block id `<FID> [<qualifier>]`; a leg that
cannot run prints NOT RUN, which is never PASS; a real-book leg on a registration closed by precondition prints
`CLOSED-NO-BOOK <id>` and asserts its STATUS (L-0.14). No leg makes a network call. Every suite accepts
`--root=DIR`. Fixture streams are `numpy.random.default_rng([SEED, crc32("<suite tag>|<block id>")])`, the suite
tags here being `registrations`, `score` and `close`. F-DET, F-KEY, F-GRID and F-COLLAR are L-0's laws (L-0.20,
L-0.21, L-0.15, L-0.16); the rows below naming them are this section's INSTANCES. F-TC11-STAMP's legs are
L-0.24's. Of the contract's fixtures (:114-124) this section owns F-FAM, matched by exact FID, and hosts the
`[scores]` instances of F-DET, F-GRID and F-KEY, which are L-0's; every other FID below is a reading's addition and
is rolled after the contract's.

Hosting — one transcript per invocation, paths under `research_outputs/tierc12/`:

| invocation | record | transcript | hosts |
|---|---|---|---|
| `tierc12_registrations_fixtures.py` | TC12-REG | `registrations/FIXTURES_REG.txt` | F-CONTRACT-PIN, F-REG, F-ATTEST-ORDER [REG] |
| `tierc12_score_fixtures.py --stage=TC12-ENV.score-build` | TC12-ENV.score-build | `env/FIXTURES_SCORE_BUILD.txt` | F-VERDICT, F-BOOT [synthetic], F-BOOT [EMPTY-ARM], F-SCORE-ANCHOR (TC11's filed arms), F-REGBOOK [plants], F-FAM [PLANTED] |
| the helper legs `F-REGBOOK [<ID>]` and `F-BASE-IDENT [<ID>]` (functions of `tierc12_score_fixtures.py`) | TC12-G · TC12-R.dir · TC12-R.sfp · TC12-S | each book stage's own transcript | one instance per regbook directory; F-BASE-IDENT on the three gates |
| `tierc12_score_fixtures.py --stage=TC12-SCORE` | TC12-SCORE | `scores/FIXTURES_SCORE.txt` | F-FAM [PARSE], F-FAM [REAL], F-BOOT [real], F-SCORE-INPUTS, F-EXIT, F-DET / F-KEY / F-COLLAR / F-GRID [scores], F-ATTEST-ORDER [ORDER] |
| `tierc12_close_fixtures.py` | TC12-CLOSE | `close/FIXTURES_CLOSE.txt` | F-S0-FIVE, F-FORM, F-NUM, F-WORDS, F-FNF, F-BOXCOST, F-LEDGER-FMT, F-CLOSE-SCRIPT, F-TC11-STAMP, F-ATTEST-ORDER [ORDER] |

The legs — each states its failure condition and the planted mutation that must turn it RED:

| fixture · blocks | FAILS IF | planted mutation that must turn it RED |
|---|---|---|
| F-FAM `[PARSE]` · `[REAL]` · `[PLANTED]` | `[PARSE]` a header's bar ≠ q ÷ m, or the fixture's parse differs from the filing or from `FAMILY.json`; `[REAL]` a family's count ≠ m, a row's bar is not its family's, tests spent ≠ BUILT un-halted rows; `[PLANTED]` a closed row carries a number, an arm or a spent test, or the planted bar moves | L-X.15's six: the bar recomputed as q ÷ (tests spent); the closed row counted as spent; a `point` on the closed row; a `scored.parquet` in the closed regbook; a row scored at another family's bar; a header's bar text changed |
| F-CONTRACT-PIN | an appended `BUILT:` line moves a slice, payload sha, head, verifier finding or a byte of a re-derived `PROGRESS.json`; a prefix byte or a foreign tail line passes | L-X.16's three: a prefix byte flipped; the `BUILT:` line inserted under `RATIFIED`; a tail line `NOTE: x` |
| F-REG `[SLICE]` · `[HASH]` · `[WRITE-ONCE]` · `[TEMPLATE]` · `[SPEC-VERBATIM]` · `[VERIFIER]` | `[SLICE]` a text, context or external slice does not re-cut from pinned bytes; `[HASH]` a payload sha or the chain does not re-derive; `[WRITE-ONCE]` a second `--file` changes a byte or exits 0; `[TEMPLATE]` a rule carries zero or two templates, or one that is not its registration's row of L-X.13's table; `[SPEC-VERBATIM]` a spec leaf differs from the plan or the plan from the LEANS, or a machine-read field is outside L-X.18's grammar; `[VERIFIER]` a detector of L-X.22 is silent on its plant, or the independent re-derivation disagrees with the filing | L-X.17 … L-X.22's plants, among them: one text character edited; one `prev` bent; `"xb"` replaced by `"wb"`; P-ADM-1's template rewritten to the `selection_hazard` form; P-SFP-VA-1's rewritten to the RE-SCORE form; `DIRECTION-INFORMED` in capitals on P-DIR-1; `prior: 30%`; a precondition in prose; a numeric `required` added to P-SCALP-3's block; one word changed in a plan's `arms` field |
| F-ATTEST-ORDER `[REG]` · `[ORDER]` | `[REG]` a file outside `PRE_REG ∪ REG_SET`, a `.parquet` outside `x_rec/` or a stage script exists at filing, or `ATTEST_REG.json` is not the listing; `[ORDER]` the paths first added by `REG` are not exactly `REG_SET`, a TC12 path outside the two sets was first added at `REG`, before it or off its descendants, or a STATUS, sidecar or regbook manifest lacks the head | L-X.21's five: a `STATUS.json` committed before the filing commit; a member of `REG_SET` first added one commit later; a STATUS carrying another head; an ignored `books/x.parquet` at filing; a stage script at filing |
| F-BOOT `[synthetic]` · `[EMPTY-ARM]` · `[real]` | `[synthetic]` the ruler's draws on fixture-built arms ≠ the fixture's own loop, or `lo`, `hi`, `p` re-derived from them differ; `[EMPTY-ARM]` an arm emptied on one asset reads anything but NOT SUPPORTED · PANEL INCOMPLETE, a zero-row arm anything but EMPTY BOOK, or `p_den ≠ N_BOOT + 1` with clause (c) true; `[real]` a row's persisted draws ≠ that loop on the row's arms, or `lo`, `hi`, `p` re-derived from `draw_hex` differ | L-X.3, L-X.6, L-X.7's plants: `seed=` omitted; the draw unit bent to rows; the seed bent by one; `p` bent to `#<0 / B`; the interval bent to the 2.5th / 97.5th; `<` on exact zeros; clause (c) removed |
| F-VERDICT `[CASES]` · `[IMPLIED]` · `[LADDER]` · `[SIZE]` | `[CASES]` a fixture-typed case maps to another word or qualifier set (the two-of-five gate must read NOT SUPPORTED with the REFUSALS qualifier); `[IMPLIED]` the binding clause per family is not the enumerated one; `[LADDER]` a member of the (TICK, D, DEEP, TOUCH) product over C / F / U maps off L-X.9's table, or a boolean differs from its definition; `[SIZE]` the vs-zero figure leaves X's typed range, two regenerations differ, or `env/SIZE_MEASURED.json` is not the leg's figures | L-X.8, L-X.9, L-X.14's plants: an ADMISSION row at the SCALPER's bar; clause (a) removed at m = 1; the REFUSAL SPREAD removed; TOUCH and DEEP swapped; the D column dropped; a closure word on a U book; a `SUPPORTED` with TICK not C; the size rule's level moved to the 10th percentile |
| F-SCORE-ANCHOR `[VS-ZERO]` · `[TWO-SAMPLE]` · `[LOAO]` · `[CONCENTRATION]` | the mirrored rulers, LOAO and concentration do not reproduce TC11's filed leaves on TC11's filed arms at TC11's seed (integers equal, floats equal as `float.hex`) | L-X.4, L-X.5, L-X.11, L-X.12's plants: `seed=` omitted; the base arm replaced by the refused cohort; a BELOW panel counted; `N` taken as the panels that bootstrapped; panels ruled vs zero under a two-sample headline; the top trade taken by `net_r` |
| F-SCORE-INPUTS | a row is scored with a pinned input changed, or with a sha that is not the path's last record's | L-X.23's four: one LEANS byte; one byte of a regbook parquet; an unlisted arm scored; an earlier record's sha accepted |
| F-REGBOOK `[plants]` · `[<ID>]` | `[plants]` a plant on the interface's row-level, sidecar or ladder laws is not caught by its named detector; `[<ID>]` `validate_book` returns a finding on a real arm, STATUS does not list exactly the arms of record, or a closed directory is not STATUS-only | L-X.24's list, among them: a duplicate key; a row past `W` in `scored`; a strip row with no `arm`; an arm STATUS lists absent from disk; the TICK and DEEP counts swapped in a sidecar; an arm written at 6 dp |
| F-BASE-IDENT `[<ID>]` (the three gates) | the base arm's canonical sha ≠ TC11's filed value; the gate holds a foreign key or an altered kept row | L-X.25's five: one base `net_r` moved by one ulp; one base row dropped; a kept row altered; a campaign added; the base rewritten through the 6-dp writer |
| F-COLLAR · F-GRID · F-KEY · F-DET `[scores]` | a beside leaf lacks the collar, carries a verdict word or a forbidden key; rows, families or beside leaves are not the declared sets; a row lacks its size keys; `DRAWS.parquet` lacks its declared key; two runs differ in a byte | L-X.14, L-X.26, L-X.27's plants: a leaf dropped; an undeclared leaf; a `strip` leaf given a mean; a `clears_literal_bar` key; an `arm__` leaf given a `p_num`; a row duplicated; a pid salt |
| F-EXIT | a record is clobbered without a logged `--refile`; an unknown id or a nickname is accepted; a refiled leaf has no superseded line; a flag is masked | L-X.27's: one byte bent in a record before a re-run; `--refile=AM-V2`; the append to `SUPERSEDED.jsonl` removed |
| F-S0-FIVE · F-FORM | §0.1 is not `S0_VERDICTS.md` in the frozen columns; a label, D-1, a key-overlap line, a superseded line or a size footnote is absent; a named part is missing or out of order; a grid on the WHOLE list is not whole or a pointed grid has no pointer; the last line is not the contract's | L-X.13, L-X.28's: a label stripped; the `r5_overlap` line removed; the footnote removed under one row; §1 and §2 swapped; `G-BRD17` replaced by a pointer; a line after the final line |
| F-NUM · F-WORDS | an untraced digit; a trace that does not re-derive; a verdict word outside its four regions | L-X.29's three: one digit of a §3 cell changed; a trace's source value moved; `SUPPORTED` written into §5 |
| F-FNF · F-BOXCOST | F-FNF: the md is not the json, a finding lacks a field, an id repeats, a harvest source is skipped, an executor finding outranks an operator one; F-BOXCOST: the table or projection does not re-derive, a file over the wire is not FLAGGED, a git call stands outside `git_ro` | L-X.30's: a harvested text edited; a blocker or a `B-1` entry unharvested; L-X.31's: a constant typed in the generator; a row dropped; a FLAG removed; a `git fetch` added |
| F-LEDGER-FMT | the format law, a cite, a required item or the stamp count fails; a stamp fill changes the byte count; §10 ≠ the append | L-X.32's six: the final line inside the block; the LANE line removed; one quoted character changed; the "maker" cite dropped; D-1 dropped; a fill one byte too long |
| F-CLOSE-SCRIPT `[SYNTAX]` · `[STATIC]` · `[STEP0]` · `[SANDBOX]` | `bash -n` fails; the push, `publish()` or the final line stand off their step, or the template module holds code; a planted gate does not STOP at step 0; the stubbed sandbox order is wrong, a path lies inside either tree, or the real repository changes | L-X.33's lists: the eight planted gates; the by-bytes check replaced by a header grep; `publish()` moved ahead of the append; the final line printed twice; a call added to the template module; the main tree's generated file handed to the runner |
| F-TC11-STAMP (L-0.24's legs, (0) PRE first) | the unstamped sweep is not GREEN in the proof tree (an environment defect, not a stamp result); TC11's head moves; a NEVER-moved file changes; the changed set leaves ALLOWED; a suite is RED; `--apply` without a GREEN proof; the main tree changes | L-X.34's four: the line inserted at line 5; a replacement applied to `SCORES.json`; `--apply` on a pre-image differing by one byte; a staged parquet removed before the PRE leg |

---------------------------------------------------------------------------------------------------------------
### REGISTRATION SPEC · (none owned by L-X)

L-X owns no registered row. The five blocks are L-G's (P-ADM-1, P-BRD-1), L-R's (P-DIR-1, P-SFP-VA-1) and L-S's
(P-SCALP-3). Each block is written in L-X.18's field grammar and STATES the common clauses below in its own
`family`, `family_m`, `family_bar`, `statistic`, `comparison`, `verdict_rule` and `labels` fields — a filed block
refers to no reading — and the filing HALTs where a block's text and these clauses disagree (detectors
`FAMILY-BAR`, `RULER-TEXT`, `TEMPLATE`, `SPEC-GRAMMAR`, `PRECOND-GRAMMAR`).

| seq | id | family (header) | m · bar | text | comparison | era of record (inside the scored window, O-9) | arms the scorer rules | label keys | preconditions (items) |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | P-ADM-1 | ADMISSION (:52) | 2 · 0.05 | :53-56 | two-sample vs v6 | full corridor (no era named; TC11 L-1.3) | `scored`, `base` | `pre_seen` | `none` |
| 2 | P-BRD-1 | ADMISSION (:52) | 2 · 0.05 | :57-59 | two-sample vs v6 | full corridor | `scored`, `base` | `selection_hazard (direction-informed) + D-1` | `none` |
| 3 | P-DIR-1 | RANGE-STATE (:64) | 2 · 0.05 | :65-68 | two-sample vs v6 | full corridor | `scored`, `base` | `selection_hazard (direction-informed)` | `none` |
| 4 | P-SFP-VA-1 | RANGE-STATE (:64) | 2 · 0.05 | :69-75 | vs zero | full corridor (:69) | `scored` | `pre_seen (KIN-SEEN)` | two (the 4h taker licence word; the licence set) |
| 5 | P-SCALP-3 | SCALPER (:82) | 1 · 0.10 | :83-106 | vs zero | holdout (:83) | `scored` (TICK), `ladder__touch`, `ladder__deep` | `pre_seen (KIN-SEEN)` | one (the 1h maker licence word, holdout row) |

(m and bar are the contract's header text, quoted; the build reads them by L-X.1's parse.)

- **statistic (two-sample rows):** `mean(net_r of the kept book) − mean(net_r of the whole v6 base)`.
  **statistic (vs-zero rows):** `mean(net_r of the scored book)`.
- **comparison and the bootstrap of record (O-22):** whole-asset clusters; `N_BOOT` draws (L-X.3);
  `tierc5.cluster_boot_diff` on the same asset draw (two-sample) or `tierc5.cluster_boot` (vs zero); the interval
  is `tierc5._ci_from`'s 5th / 95th percentile; `p = (#draws ≤ 0 + 1) / (N_BOOT + 1)` as a Fraction; the seed of
  record is the contract's (:4), passed explicitly, the sensitivity seed `tierc5.SEED` printed beside.
- **verdict_rule, common sentence:** "verdict_of_record = SUPPORTED iff (a) the cluster-90% CI lower bound (the 5th
  percentile of the draws) > 0 AND (b) one-sided p <= q ÷ m, exact, AND (c) every declared asset holds at least one
  row in every arm the ruler reads; else NOT SUPPORTED. m is fixed in every case; a registration closed by its
  precondition prints 'CLOSED BY PRECONDITION (…) — no number · no test spent', spends no test and never loosens
  the bar. Printed beside, deciding nothing: the sensitivity seed, the haircut and all-taker twins, the tuning and
  holdout slices, LOAO, both single-trade shares, the literal-bar column, the exact enumeration with SEED-FRAGILE,
  the month-block twin with TIME-CLUSTER FRAGILE, the drop-OPEN twin with VERDICT RESTS ON OPEN MARKS, the forward
  strip unscored. Tier-E arms carry no verdict word." — followed by exactly one `prints '<verdict> …'` template,
  the one L-X.13 fixes for the registration id. The filing asserts the rule states the parsed q, m and bar,
  `N_BOOT`, both seeds and the template.
- **verdict_rule, the words, exhaustive:** every block names every word its row can print and no other. On the
  four rows other than P-SCALP-3: `SUPPORTED`, `NOT SUPPORTED`, `CLOSED BY PRECONDITION` (the last only on a row
  that carries a precondition item — P-ADM-1, P-BRD-1 and P-DIR-1 carry none and say so). On P-SCALP-3 also `NOT
  SUPPORTED — CLOSED` and `NOT SUPPORTED — CLOSED FOR GOOD`. Qualifiers are named as qualifiers (L-X.9's list),
  never as words.
- **verdict_rule, the three two-sample rows, added:** the REFUSAL SPREAD of L-X.7 in the block's own words — with
  `a` the number of declared assets holding at least one refused campaign and `N` the number of declared assets,
  if `((N − a)/N)^N` is at or above the family bar the row reads NOT SUPPORTED with the qualifier `REFUSALS ON a/N
  ASSETS` (the refusals sit on too few assets for the ruler to clear), its test is spent, and the cell is never
  cited as evidence against the gate; a gate that refuses nothing reads NOT SUPPORTED with `TWO-SAMPLE-PREMISE`.
- **verdict_rule, P-SCALP-3 only, added:** the definitions of `C`, `F`, `U` and `D` and L-X.9's table verbatim —
  its ten cases — with the sentence "a closure word needs a measured failure: a book whose ruler is undefined is
  not a failed book"; "one test is spent; TOUCH and DEEP can never produce SUPPORTED"; the two booleans
  `fails_under_deep_too` and `clears_only_under_touch`; the two fixed sentences of L-X.9 (the fill-model twins;
  the reading of the LOAO line); the order of the verdict text (the fill-sensitivity row, the LOAO line, the
  single-trade share of record, the per-order ladder counts of the TICK ledger and, where the three books' own n
  are not ordered, the line BOOK-N-NOT-MONOTONE, then the leaf `licence_at_maker_pin` with its qualifier `LICENCE
  EDGE ≤ 0 AT THE PINNED MAKER RATE` where the figure is not above zero); and the bar cell of L-X.8.
- **preconditions:** L-X.18's grammar, with the items of the table above and no other; the sentence of what a
  closed row prints stands in `verdict_rule`, never as a sub-bullet of `preconditions`.
- **labels:** one sub-bullet per key in L-X.18's form, with the tag and label L-X.13's table gives the
  registration; on P-SFP-VA-1 and P-SCALP-3 the long `pre_seen` text is the label's `text` and is printed under
  the cell.
- **disclosed_beside, common set:** L-X.14's common slugs, each Tier-E, no verdict word, and one `arm__<slug>` leaf
  (interval only: no p, no bar, no second seed, no LOAO) for each `tierE__` arm the block names; owners name their
  own arms and tables.
- **failure_conditions, common:** F-REGBOOK and F-KEY (L-0.21) on the regbook directory, F-BOOT, F-VERDICT,
  F-SCORE-ANCHOR, F-GRID, F-DET, and for gates F-BASE-IDENT; owners append theirs (F-GATE, F-BRD, F-DIR, F-SFP,
  F-SCALP, F-TOLL).

### OPEN TO OPERATOR

Each item states the default the build takes if the operator is silent; every item is carried into the report's §9.

1. **The single-trade share has no threshold** in the contract (:106) or on any file, and the executor may not type
   one. DEFAULT if silent: none; both shares are printed in every row and in P-SCALP-3's verdict text and decide
   no word (O-32). LOAO alone carries the one-asset reading on P-SCALP-3, as part of the kill (L-X.9, L-X.11);
   naming rival (ii) of L-X.9 makes it a printed qualifier on a SUPPORTED cell instead.
2. **The push route.** Step 1 of the acts is a push, and the SSH route has failed on every daily run since
   2026-09-27 (`exchange/status/daily/DAILY_2026-10-08.md:123`). DEFAULT if silent: the acts STOP at step 1 with
   nothing changed until the route works.
3. **A tc11-stamp proof that is not GREEN.** DEFAULT if silent, at build time: the acts carry no stamp step, the
   finding says whether the cascade was RED or the proof environment was defective, and the ruling returns to the
   operator (L-0.24). DEFAULT, at the act: nothing is applied, TC12's close continues, the append says so with the
   transcript's path, and the item is an operator-owned finding. Vetoing `"tc11-stamp"` by name removes step 4's
   first half altogether.
4. **X's frozen records name TC11's old shas for good** once the stamp lands (thirty tracked X records,
   `scout/U1_rulings_close_state.md` §1.4). DEFAULT if silent: listed as HISTORICAL in the stamp map, none edited.
5. **The box.** After the three pending closes the forecast leaves the box within a few KB of WARN, so TC12's
   report alone crosses it; `publish()` prints the warning and still publishes. DEFAULT if silent: published under
   WARN, REFUSE never overridden, every held file listed for ATHENA.
6. (settled: the whole-versus-pointed map is frozen in L-X.28.)
7. **CLOSED versus CLOSED FOR GOOD when TICK and DEEP fail and TOUCH clears.** Both contract clauses hold there
   (:104-105). DEFAULT if silent: `NOT SUPPORTED — CLOSED` (clears only under TOUCH), so that each clause has a
   live event; the literal-order rival (CLOSED FOR GOOD whenever TICK and DEEP fail) is the operator's to name.
   Both clause truths are printed on the row either way (`fails_under_deep_too`, `clears_only_under_touch`).
8. **The proof tree of the tc11-stamp.** SETTLED by O-33, which annotates O-10 (a clone cannot run TC11's suites,
   L-X.34): a detached linked worktree under a scratch directory outside both trees, removed after the proof; no
   ref and no main-tree file moves. Not an open item.

### INTERFACE ASSUMPTIONS

Each line names what this section takes from another and the reading that supplies it. This section's modules:
`scripts/tierc12_registrations.py` (filed at TC12-REG, in `REG_SET`; env-free), `scripts/tierc12_regbook.py` and
`scripts/tierc12_score.py` (filed at `TC12-ENV.score-build`), `scripts/tierc12_close.py`,
`scripts/tierc12_close_acts_template.py` and `scripts/tierc12_tc11_stamp.py` (filed at TC12-CLOSE); suites
`scripts/tierc12_{registrations, score, close}_fixtures.py`. None is a door and none imports
`analytics.value_area`, `analytics.profile` or the Stage V reader; the scorer and the close read Stage V's FILED
records only (`va/VA_MIRROR.json` and the files the report quotes).

- **L-0 (laws, process):**
  - L-0.10: the record order `RESUME_ORDER_T` — TC12-REG directly after TC12-LEANS and before TC12-D; this
    section's blocking child `TC12-ENV.score-build` after TC12-ENV; TC12-SCORE only when TC12-C, -G, -R, -S, -L
    and the three stamps children are COMPLETE-VERIFIED; T1's text-before-result test and L-X.21's clause 3 are the
    one fixture F-ATTEST-ORDER on the typed sets `PRE_REG` and `REG_SET`; T4's whole-versus-pointed freeze is
    L-X.28's map; T5 (no file under `scores/` before the regbooks).
  - L-0.4, L-0.9: `tierc12_progress.certified(rel_path)` (the last record naming a path); the record keys;
    `PROGRESS.json["amendments_of_record"]`; `contract_of_record` by prefix; the quarantine directories
    `_det_partial_*/`.
  - L-0.5: the amendment law (never from an outcome) and the ids `AM-<n>` / `FIX-<n>`; AM-1 on file at filing; the
    append-only files `scores/REFILE_LOG.jsonl` and `scores/SUPERSEDED.jsonl`; the freeze of
    `ORCHESTRATOR_RULINGS.md` and `DISCLOSURES.md` at the shas the filing names, and `DISCLOSURES_BUILD.md` after
    it; the freeze of `LEANS.md` by sha and the review record's path.
  - L-0.13: the two table writers — `put` (6 dp; `DRAWS.parquet`) and `put_regbook` (full float; called only by
    `tierc12_regbook.write_arm`); the manifest key `registrations_sha256`; `READ_SET.json` beside each manifest.
  - L-0.14, L-0.19: the harness `scripts/tierc12_fx.py`; one block per leg with the id grammar; the NOT RUN state;
    CLOSED-NO-BOOK; `--root`; the fixture RNG; the exact-FID map under which F-FAM's three blocks carry the
    contract's name and `F-FAM-PINS`, `F-LEDGER-FMT` and `F-ATTEST-ORDER` do not.
  - L-0.16: the collar helper; `REGISTERED_TABLES_T` holding the ladder arms; the forbidden-key pattern
    `verdict|clears|spent_test`; the registered marker allowed in §4's verbatim re-quote.
  - L-0.17, L-0.18: the pin door `scripts/tierc12_pins.py` and its map with multi-group rows — `fam.q`,
    `fam.<stage letter>`, `seed`, `loao.line`; the `lineage` rows of `pins/PIN_REGISTER.json` holding the node shas
    of the AST literals this section reads; `F-FAM-PINS`. The two close modules are L-0.17's RENDERERS; the filer,
    the regbook module, the scorer and the stamp tool are computation modules under F-TYPED and hold structural
    literals only.
  - L-0.22: `SUBPROC_SITE_T` holding `tierc12_close.git_ro` and `tierc12_tc11_stamp.run`. L-0.24: the stamp's law,
    its PRE leg, and "no TC12 pin is a whole-file sha of a file the close acts move". L-0.26: the acts' executions
    (the scratch copy) and F-NOT leg ACTS's typed exemption of the template module. L-0.1: the prefix pin. L-0.6:
    the census `frozen/FROZEN_ESTATE.json`. L-0.15, L-0.20, L-0.21: F-GRID, F-DET, F-KEY.
- **L-D (substrate, env):** the shim `E` (`scripts/tierc12_env.py`) with `E.T5`, `E.TP`, `E.N_BOOT`, `E.SEED`,
  `E.SEED_SENS`, `E.era_of`, `E.CLASSIC5`, `E.LENS_MS`, `E.PIN_MS`, `E.TC11_PIN_MS`, `E.ERA_CUT_MS`, and `E.fees()`
  with `taker_bps_side`, `slippage_bps_side`, `maker_bps_side` per stem; `E.tc11_record(rel)` over
  `TC11_ALLOW_FILE`, whose rows for this section are `scores/SCORES.json`, `scores/BASE_IDENT.json`,
  `data/AS_OF_PIN.json`, `registrations/REGISTRATIONS.json`, `registrations/REGISTRY_PIN.json`,
  `regbooks/P-BRK-4H/scored.{parquet, json}` and `regbooks/P-AGE-1/{scored, base}.{parquet, json}`, and which
  accepts TC11's `PROGRESS.json` at the stamped value once `close/TC11_STAMP_MAP.json` reads `applied: true`;
  `E.x_rec(rel)`; `env/LINEAGE_PINS.json`; `data/AS_OF_PIN.json`, `data/fee_schedule.json` (with
  `maker_pin.differs_from_x_assumption`) and `STAGE_D_MANIFEST.json` at their certified shas; write-protection of
  the frozen estate. The registry is filed before `E` exists, so the filer imports no env and reads only the
  files L-X.3 and L-X.19 name.
- **L-V (value area):** `va/VA_MIRROR.json` — a registered record certified by `progress/TC12-V.json`, holding
  `licence["<lens>|<toll>"].by_era[<era>]` with the quoted `would_read`, `edge_net_h20`, `toll_bps`,
  `edge_median_term_h20` and `edge_toll_atr`, and `licence_set`; no number in it is computed by TC12; `VA_PINS`,
  `TRAVERSE` (with the strict-INSIDE twin) and `va_stack` for §2 and §3; `va/trades/TWO_TRADES.md` for the pointer
  row; AM-1's text (L-V.15).
- **L-C (control):** the v6 frame the three `base` arms are written from, bit-equal to TC11's on the sixteen
  columns; the strip campaigns.
- **L-G (admission):** the REGISTRATION SPECs of P-ADM-1 and P-BRD-1 in L-X.18's grammar, incl. their label texts
  and `external_context`; the arms of L-X.24's table; `stage_g/g_brd17.parquet` with the columns `cell` and `n`;
  the refused sets and F-GATE / F-BRD; `F-REGBOOK` and `F-BASE-IDENT` instances run by Stage G's suite.
- **L-R (range-state):** the specs of P-DIR-1 and P-SFP-VA-1 in the same grammar; the arms of L-X.24's table;
  `stage_r/dir/build_manifest.json` key `r5_overlap`; `VA_CHOP_ALIGNMENT` for §0.2; `exit_reason = "corridor_end"`
  on positions open at the scored window's end; the instances run at `TC12-R.dir` and `TC12-R.sfp`.
- **L-S (scalper):** the spec of P-SCALP-3 stating L-X.9's ten-case table, its definitions, booleans and fixed
  sentences, with ONE precondition item; `scored` = the TICK book, `ladder__touch`, `ladder__deep` and the Tier-E
  arms of L-X.24's table; the four per-order counts in the three ladder-class sidecars; the fee columns per leg
  and `taker_twin_haircut_net_r`; uncapped funding with `tc_series_net_r` and `funding_ceiling_bound`;
  `S_FILL_SENSITIVITY`, `S_MISS_GRID`, `S_REGIME` for §4; what CLOSED and CLOSED FOR GOOD forbid afterwards.
- **L-L (ledger, era, ferry):** `LEDGER-BOOKS` and `LEDGER-ROWS` for §0.4; `era/ERA.md` for the pointer row;
  `scripts/tierc12_ferry.py` with a forecast mode (off-bus staging) and an of-record mode pinned by sha for step 2,
  stubbed in the acts' sandbox proof and proven by F-ROWS `[ACT]`; the frozen priority order of the held set;
  F-LEDGER (the contract's, by exact FID).
- **The orchestrator's acts at the freeze, which this section reads and does not write:** D-5 … D-12 appended to
  `DISCLOSURES.md`; AM-1 in `LEANS_AMENDMENTS.md`; the TC12-LEANS record; the change of
  `scripts/tierc12_progress.py` at TC12-REG (`RESUME_ORDER`, `SUBSTAGES`, `certified`, the contract by prefix).

### OBJECTIONS

None against a ruling. O-1 … O-32 were checked against the files this section cites and no ruling was found wrong
on a fact. Section H (O-25..O-32) is conformed to: O-30 in L-X.13 (three templates, keyed by registration id),
O-31 in L-X.23 (the scorer's code under the dotted child `TC12-ENV.score-build`), O-32 in L-X.9, L-X.12 and
L-X.24 (the LOAO kill, the single-trade share, the per-order ladder). Three places where this section adds to a
ruling without contradicting it are stated in the readings: L-X.7's clause (c) and its REFUSAL SPREAD answer what
O-22's law does when a draw leaves an arm empty or cannot differ from zero; L-X.9 layers the contract's pre-named
kill (:104-106) over O-22's verdict law for P-SCALP-3 alone; and L-X.34 reads O-10's "scratch clone" as a scratch
proof tree outside both trees (a detached linked worktree), because a clone cannot run TC11's suites — listed for
the orchestrator and for the operator (OPEN TO OPERATOR 8).

A correction that is not against a ruling: this unit's brief cites CLOSE as "contract lines 121-129". On the filed
bytes (sha `861d6050…`) CLOSE is lines 126-131 (slice sha `5f964a17…9737`) and lines 114-124 are FIXTURES; every
cite in this section uses the verified map of L-X.17.
