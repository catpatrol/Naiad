## L-X · STATISTICS, REGISTRATIONS, SCORING AND CLOSE

This section governs everything that turns a book into a word and a word into a published record: (A) the three
families and the statistic of record (ruler, draws, interval, p, verdict law, the verdict vocabulary, LOAO, the
single-trade share, the in-sample labels, the beside-prints); (B) the registration architecture (how the contract is
pinned, how the five texts are sliced, what `REGISTRATIONS.json` holds, how it is written once, and how
text-before-result is proven); (C) the scorer (`scripts/tierc12_score.py`: its pinned inputs, the regbook interface
Stages G / R / S build to, its outputs and its write law); (D) CLOSE (the report's order, the number-tracing law,
findings-not-fixed, BOX-COST, the ledger append, and `close_acts.sh` — every step an operator keystroke, O-12). It
owns no registered row; the five rows are owned by L-G (P-ADM-1, P-BRD-1), L-R (P-DIR-1, P-SFP-VA-1) and L-S
(P-SCALP-3), and each owner's REGISTRATION SPEC imports the common clauses at the end of this section by reference.

Conventions used below. Paths are relative to `/Users/luis/Naiad` unless absolute; `x_rec/` abbreviates
`research_outputs/tierc12/x_rec/`. "The contract" is `exchange/queue/2026-10-08_TC12_APOLLO.md` (prefix sha256
`861d6050e80e66995e4f9db2855aaf274d63285249c2549e5a0813582095a7bd`), cited `:<line>`. A value written "(on file: v)"
is information for the reader; the constant the build uses is the named object, read at run time. Every sha, line
number and line-slice sha printed here was re-hashed or re-read while drafting [measured here]; no outcome of any
TC12 book was computed, and no `tc11x_*`, `tierc10_*` or `tierc11_*` module was imported or run.

---------------------------------------------------------------------------------------------------------------
### A · Families, the statistic of record, the verdict vocabulary

**L-X.1 THE THREE FAMILIES, PARSED** — "families declared by MECHANISM before the look, each independently failable,
bar = 0.10 ÷ m per family" (contract :8-9); "STAGE G · ADMISSION FAMILY (m=2, bar 0.05; …" (:52); "STAGE R ·
RANGE-STATE FAMILY (m=2, bar 0.05):" (:64); "STAGE S · SCALPER FAMILY (m=1, bar 0.10)" (:82)
READING:
- Nothing about a family is typed. The parse is rows of L-0.17's pin map, run by the pin door
  (`scripts/tierc12_pins.py`) over the PREFIX lines of the contract (L-X.16) and called by the registry filer
  (`scripts/tierc12_registrations.py`); L-0.18 states the law, this reading the exact rule. Two regular expressions:
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
FAILS-IF: F-FAM (PARSE leg) is RED when a header's bar ≠ q ÷ m or the parsed families are not the line map's;
planted mutation: the STAGE G header of a scratch copy rewritten with the SCALPER header's bar text must HALT
`FAMILY-BAR`.

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
- The tier declares three families, so the tier-wide chance of at least one false SUPPORTED is not q; the report's
  §1 says so in one sentence beside the three bars (a disclosure, deciding nothing).
SOURCE: `research_outputs/tierc11/LEANS.md:122-124` (L-1.4, "spends no test, and never loosens the bar");
`x_rec/tierc11x/LEANS_X.md:721-724`; `scripts/tierc11_score.py:2075-2092` (`family`, `tests_spent`);
`research_outputs/tierc11/scores/FAMILY.json` key `law` (sha `3fa36bd4…2d73`); O-22.
RIVALS: bar = q ÷ (tests actually run) — loosens the bar after a closure; refused by both precedents. A HALTed row
counted as a spent NOT SUPPORTED — prints a verdict the ruler never produced.
FAILS-IF: F-FAM (REAL and PLANTED legs, L-X.15).

**L-X.3 THE BOOTSTRAP OF RECORD: UNIT, DRAWS, SEEDS** — "bar = 0.10 ÷ m per family" (:9); "Seed 20261008." (:4)
READING:
- **Unit.** The whole asset: every trade of an asset (`symbol`) moves together. Each draw picks |U| assets from the
  |U| distinct labels with replacement (`rng.choice(uniq, size=len(uniq), replace=True)`), `uniq = np.unique(labels)`
  (sorted). No time blocks, no per-trade resampling.
- **Primitives, called and never re-implemented:** `tierc5.cluster_boot`, `tierc5.cluster_boot_diff`,
  `tierc5._ci_from`, reached as `E.T5` through L-D's env shim (file sha `ad912b38…5a6f` asserted before the first
  call).
- **Draws B.** The registry is filed before the env exists (L-0.10's order), so the FILING reads `N_BOOT` from
  filed records: `research_outputs/tierc11/scores/SCORES.json["n_boot"]` (on file: 4000), asserted equal to
  `x_rec/tierc11x/registrations/REGISTRY_PIN_X.json["n_boot"]`. The SCORER reads the lineage object `E.TP.N_BOOT`
  (L-0.17's door) and HALTs unless it equals the filing's `statistics.n_boot` and
  `inspect.signature(E.T5.cluster_boot).parameters["n_boot"].default`.
- **Seed of record.** The pin door's row for contract :4 (`Seed (\d{8})\.`, exactly one hit), asserted equal to
  `research_outputs/tierc12/PROGRESS.json["seed"]`. **Sensitivity seed:** filed from `SCORES.json["seed_sens"]` (on
  file 20260816); the scorer HALTs unless `E.T5.SEED` (`scripts/tierc5.py:86`) equals it. Printed beside, deciding
  nothing.
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
FAILS-IF: F-BOOT is RED when a row's persisted draws differ from the fixture's own `default_rng(seed).choice` loop;
planted mutations: `cluster_boot` called without `seed=`; the draw unit bent to rows; the seed bent by one.

**L-X.4 THE VS-ZERO FORM (P-SFP-VA-1, P-SCALP-3)** — "(vs zero; full corridor; …" (:69); "(vs zero; HOLDOUT era …"
(:83)
READING: values `v` = `net_r` of the scored arm (L-X.24), labels `c` = its `symbol`; point = `mean(v)`; draws =
`T5.cluster_boot(v, c, seed=SEED, n_boot=N_BOOT)`; `n_clusters = len(np.unique(c))`. P-SFP-VA-1's scored arm is the
4h book of record on the full corridor inside the scored window (O-9); P-SCALP-3's is the through-tick (TICK) book
on the holdout era inside the scored window. The filing asserts the text slice contains `vs zero` (detector
RULER-TEXT).
SOURCE: `scripts/tierc5.py:1178-1197`; `scripts/tierc11_score.py:977-985`; contract :69, :83; O-9.
RIVALS: none on the ruler (the contract names it). Per-direction or per-asset rulers — Tier-E slices of the owning
stage.
FAILS-IF: F-SCORE-ANCHOR (vs-zero leg): the mirrored ruler on TC11's filed `regbooks/P-BRK-4H/scored.parquet` at
TC11's seed must reproduce `SCORES.json rows[registration=P-BRK-4H].stats.main`; planted mutation: `seed=` omitted.

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
gate removes trades; the re-ride is a Tier-E disclosure (O-21).
FAILS-IF: F-SCORE-ANCHOR (two-sample leg): the mirrored ruler on TC11's filed `regbooks/P-AGE-1/{scored,base}.parquet`
at TC11's seed must reproduce `SCORES.json rows[registration=P-AGE-1].stats.main` (point, lo, hi, p_num, p_den,
n_draws_finite, n, n_base, n_clusters); planted mutation: the base arm replaced by the refused cohort.

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
UNVERIFIED: that `np.percentile`'s default method in `~/venvs/naiad` is "linear" in the installed numpy; F-BOOT's
hand leg re-derives `lo` and `hi` from the persisted draws by its own order-statistic interpolation and compares
`float.hex` values, which settles it at build.
FAILS-IF: F-BOOT is RED when `lo`, `hi` or `p` re-derived from the persisted draws (never from printed values)
differ; planted mutations: `p` bent to `#<0 / B`; the interval bent to the 2.5th / 97.5th; `<` used on a draw set
holding exact zeros.

**L-X.7 WHEN THE RULER IS NOT DEFINED: THE PANEL-COMPLETE CLAUSE, EMPTY ARMS, 4000 FINITE DRAWS** — O-22; contract
"five home assets" (:69-70, :84)
READING:
- A two-sample draw is NaN when an arm has no row in any picked asset (`tierc5.py:1220-1222`); a vs-zero book
  holding fewer assets than the declared panel is ruled on fewer clusters than registered. Both are decided before
  any outcome is read, on counts alone:
  - **Clause (c), PANEL COMPLETE:** every asset of the declared panel holds ≥ 1 row in every arm the ruler reads —
    the scored arm, and the base arm for a two-sample row. The declared panel of all five rows is the home panel:
    L-D's object for the five stems of contract :18, which the `panel` of every `scored`, `base` and `ladder`
    sidecar must equal (L-X.24).
  - **If (c) fails the row cannot read SUPPORTED.** It reads NOT SUPPORTED with the qualifier `PANEL INCOMPLETE
    (<asset> holds no <arm> row)`, its test is spent, and whatever the ruler returns on the finite draws is printed
    as `not_of_record` with `n_draws_finite`. An empty scored arm (`n = 0`) is the limiting case, qualifier `EMPTY
    BOOK`.
  - **If (c) holds, `n_draws_finite == N_BOOT` is ASSERTED at the seed of record and at the sensitivity seed;** a
    failure is HALT `DRAWS-NONFINITE` (with every asset present in every arm no take can be empty, so a non-finite
    draw is a code defect, not a result). A HALTed row prints no number, no word, spends no test, and blocks CLOSE
    (F-S0-FIVE).
- A gate that refuses nothing (`kept == base` by key): flagged `TWO-SAMPLE-PREMISE: key sets identical — the
  difference is 0 by construction`, ruled as it stands (every draw 0, `p = 1`), NOT SUPPORTED, test spent.
- Beside-prints (L-X.14) carry no clause (c): a leaf with non-finite draws prints `n_draws_finite` and
  `nonfinite_draws = k`, is ruled on the finite draws by `_ci_from`, and decides nothing.
- Clause (c) applies to each fill-ladder book of P-SCALP-3 (L-X.9).
SOURCE: `scripts/tierc5.py:1218-1222`, `:1227-1229`; `scripts/tierc10_panel.py:1241-1242` ("a declared asset whose
leave-out panel cannot be bootstrapped counts AGAINST the line" — the lineage's undefined-counts-against law);
`scripts/tierc11_score.py:856-866` (SC-6, the identical-key flag), `:955-970` (`n_draws_finite`);
`scout/U7_registrations_scoring.md` H6, R14.
RIVALS: drop the NaN draws and rule on the rest (`_ci_from`'s own behaviour) — the denominator falls below B + 1 and
the deciding rank moves silently. HALT the row with no verdict when an arm is empty on an asset — a free closure. A
count-against completion with NaN ranked below every draw — needs an interval law on infinities that no file
supplies. Of the faithful readings this is the one that cannot flatter: an undefined ruler never supports.
FAILS-IF: F-BOOT (EMPTY-ARM leg) is RED when a planted kept arm emptied on one asset reads anything but NOT
SUPPORTED · PANEL INCOMPLETE, or when a row with (c) true carries `p_den ≠ N_BOOT + 1`; planted mutation: clause (c)
removed from the rule (the planted arm must then be caught reading on a denominator below B + 1).

**L-X.8 THE VERDICT LAW** — "bar = 0.10 ÷ m per family" (:9); "NOT SUPPORTED if the through-tick book fails the bar"
(:104)
READING:
- **`SUPPORTED` iff (a) `lo > 0` (the 5th percentile of the B draws, strictly) AND (b) `p ≤ bar_f` (exact, L-X.6)
  AND (c) PANEL COMPLETE (L-X.7); else `NOT SUPPORTED`.** Evaluated at the seed of record on the scored arm.
  P-SCALP-3 adds the contract's pre-named kill on top (L-X.9); no other row adds anything.
- This is a named reading: the contract names a bar and not a verdict law. (a) is the lineage's law, (b) the
  family's multiplicity bar, joined as TC11 L-1.4 and X LX-1.2 join them and as O-22 rules.
- **Stated before the look.** Which clause binds follows from B, `_ci_from`'s lower level and the bar, and is
  computed by the scorer and printed per family (F-VERDICT's IMPLIED leg enumerates `k = 0..B`, it types nothing):
  at the two m = 2 families the clauses differ by one draw, (b) being the stricter; at the m = 1 SCALPER family
  clause (a) implies clause (b), so the bar is on record and does not decide, and P-SCALP-3's bar cell reads
  "`<q>` (not binding at m = 1; decided at the 5th percentile, clause (a))" — X's filed wording with q read from
  the contract.
- **The rival is printed, deciding nothing:** the literal bar alone, `p ≤ bar_f` (leaf `literal_bar`, L-X.14).
- The row also carries `stable_across_seeds` (does the frozen rule give the same word at the sensitivity seed) — a
  boolean; the sensitivity seed's word is never filed.
SOURCE: `research_outputs/tierc11/LEANS.md:114-121`; `x_rec/tierc11x/LEANS_X.md:657-685` (the reading, its
consequences at m = 2 and m = 1, `:668-672`), `:675-678` (why (a) is kept at m = 1);
`x_rec/scripts/tc11x_score.py:141` (`SFP_BAR_CELL`), `:209-218` (`literal_bar`); O-22;
`scout/U7_registrations_scoring.md` §2.1, R2.
RIVALS: `p ≤ bar` alone — looser at m = 1 (it would decide at the 10th percentile); printed as a column. CI-only
(TC10's form) — drops the family bar the contract names.
FAILS-IF: F-VERDICT is RED on any typed case; planted mutations: (i) an ADMISSION row scored at the SCALPER's bar
(detector BAR-OF-FAMILY); (ii) the m = 1 rule with clause (a) removed, fed a draw set with `lo < 0` and `p` between
the two clauses' limits, must stay NOT SUPPORTED.

**L-X.9 THE VERDICT VOCABULARY, AND THE SCALPER'S PRE-NAMED KILL** — "PRE-NAMED KILL: NOT SUPPORTED if the
through-tick book fails the bar; CLOSED FOR GOOD if it fails under DEEP too; CLOSED if it clears only under TOUCH
(the fill-sensitivity row is part of the verdict text); one-asset dependence read by LOAO 3/5 and the single-trade
share." (:104-106)
READING:
- **Five words, exhaustive.** `verdict_of_record` ∈ { `SUPPORTED` · `NOT SUPPORTED` · `NOT SUPPORTED — CLOSED` ·
  `NOT SUPPORTED — CLOSED FOR GOOD` · `CLOSED BY PRECONDITION` }. The scalper's two closure words (`CLOSED`,
  `CLOSED FOR GOOD`) exist on P-SCALP-3 only. They are always printed behind `NOT SUPPORTED — `, so a closure can
  never be read without the failure it rests on, and the bare word `CLOSED` never stands as a verdict.
- **Qualifiers are not words.** `FILL-SENSITIVE`, `ONE-ASSET DEPENDENT`, `PANEL INCOMPLETE`, `EMPTY BOOK`,
  `TWO-SAMPLE-PREMISE`, "CI wholly below zero", `SEED-FRAGILE`, `TIME-CLUSTER FRAGILE`, `VERDICT RESTS ON OPEN MARKS`
  qualify a cell and are filed in `qualifiers[]`. `HALT` and `ABSENT` are scorer statuses, never verdicts.
- **P-SCALP-3's table.** Let `C(X)` = clauses (a) ∧ (b) ∧ (c) on book X ∈ {TOUCH, TICK, DEEP} at the seed of record
  and the SCALPER bar — the same ruler, seed, B and bar on all three; "fails the bar" = `not C(X)`. Let `D` =
  ONE-ASSET DEPENDENT on the TICK book (L-X.11). The six cases partition every outcome:

  | C(TICK) | D | C(DEEP) | C(TOUCH) | verdict_of_record | qualifier |
  |---|---|---|---|---|---|
  | true | false | true | any | `SUPPORTED` | — |
  | true | false | false | any | `SUPPORTED` | `FILL-SENSITIVE (does not clear under DEEP)` |
  | true | true | any | any | `NOT SUPPORTED` | `ONE-ASSET DEPENDENT (LOAO k/N)` |
  | false | any | true | any | `NOT SUPPORTED` | — |
  | false | any | false | true | `NOT SUPPORTED — CLOSED` | `(clears only under TOUCH)` |
  | false | any | false | false | `NOT SUPPORTED — CLOSED FOR GOOD` | — |

- Why rows five and six split that way: "fails under DEEP too" and "clears only under TOUCH" both hold when TICK
  and DEEP fail and TOUCH clears; the clause that names that event exactly ("only under TOUCH") governs it, and
  "FOR GOOD" is left for the book that fails under every fill model. Every clause of the kill then has a live,
  disjoint event.
- **One test.** TOUCH and DEEP are ruled at the family bar and can never produce `SUPPORTED`; only the TICK book
  can. m stays 1 and one test is spent. The two twins are the contract's "fill-sensitivity row", a named exception
  to the Tier-E collar: they are arms of class `ladder` (L-X.24), and their `C(X)` booleans are filed inside the row.
- **The verdict text of P-SCALP-3** = its cell (word, qualifiers, label per L-X.13) followed by the fill-sensitivity
  row: per fill rule `n_filled`, point, interval, `p_num/p_den`, `C(X)`; then the LOAO line `k/N` with its bar, and
  the single-trade share of record (L-X.12).
- What a closure forbids afterwards is L-S's text and the ledger append's; this section fixes only the word and
  its condition.
SOURCE: contract :93-96 (the three fill rules), :104-106; `scripts/tierc11_score.py:1160-1167`;
`scripts/tierc11_registrations.py:38-39` and `scripts/tierc11_score.py:262-263` (the collar this departs from);
`scout/U7_registrations_scoring.md` §2.20, R11, R12.
RIVALS: (i) `CLOSED FOR GOOD` whenever TICK and DEEP both fail, whatever TOUCH reads — leaves the contract's CLOSED
clause with no event. (ii) One-asset dependence as a printed qualifier on a `SUPPORTED` cell (LOAO deciding nothing,
as on every earlier tier) — the clause sits inside "PRE-NAMED KILL", so the two readings are equally faithful, and
the one taken is the one that cannot flatter: a one-asset result does not read SUPPORTED. (iii) Twins as ordinary
Tier-E arms — the contract makes them part of the verdict text.
FAILS-IF: F-VERDICT (LADDER leg) is RED when any of the sixteen (C(TICK), D, C(DEEP), C(TOUCH)) combinations maps
to another word or qualifier than the table's; planted mutations: TOUCH and DEEP swapped in the rule; the D column
dropped; a `SUPPORTED` produced with C(TICK) false.

**L-X.10 CLOSED BY PRECONDITION** — "a registration closed by precondition spends no test" (:9)
READING:
- A registration's `preconditions` field is `none` or a list of items `{record: <path>, certified_by: <progress
  record and key>, selector, required}`, plus `sha256` where the record already exists at filing (an `x_rec` file).
  A record built after the filing (L-V's `va/VA_MIRROR.json`, L-D's fee schedule) is named by path and by the
  progress record that certifies its sha; the reader asserts the file's sha equals the certified one. None is a
  statistic of the row's own book.
- The owning stage evaluates the items BEFORE building any arm. If any item is not met it writes
  `regbooks/<ID>/STATUS.json` with `status = "CLOSED_BY_PRECONDITION"`, the item, the value found, `arms = []` — and
  nothing else: no parquet, no sidecar, no number of the book (O-22).
- The scorer re-evaluates every item itself from the same record. Builder and scorer disagreeing is HALT
  `PRECONDITION-MISMATCH`. Not met: `verdict_of_record = "CLOSED BY PRECONDITION"`, cell `CLOSED BY PRECONDITION
  (<record>#<selector> reads <found>; required <required>) — no number · no test spent`, every numeric leaf null,
  `spent_test = false`, no ruler called, the label filed in its own field and absent from the cell (a label
  qualifies a verdict; none is computed).
- A CLOSED regbook directory holding any arm file is HALT `CLOSED-HAS-ARM`.
- Which rows carry which items is the owners' text (L-R, L-S). On the records as filed no item fails (V3 HALTs the
  tier on a mirror disagreement), so F-FAM proves the law on a planted family.
SOURCE: `scripts/tierc11_score.py:1813-1827` (the closed row), `:290` (`PRECONDITION_LENS`);
`research_outputs/tierc11/regbooks/P-SCALP-2/STATUS.json` (the filed form); `x_rec/tierc11x/registrations/SCORED_X.json
rows[2]` (`number_free true`, `test_spent false`, `cell_text "CLOSED BY R2 (1h: FAIL)"`); O-17, O-22.
RIVALS: build the book of a closed row and print it collared (X's departure) — O-22 rules STATUS only.
FAILS-IF: F-FAM (PLANTED leg, L-X.15).

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
  above_half_bar(N) = ceil((N + 1) / 2)`. The contract's "3/5" is parsed from :106 with `LOAO (\d+)/(\d+)` and
  asserted equal to `(above_half_bar(N), N)` for the five home assets. BELOW panels never count toward the line.
- **Seed.** The seed of record, passed explicitly (`TP.loao_n`'s default is TC10's seed); the sensitivity seed's
  table is printed beside.
- **A declared asset with no trade** reproduces the headline when dropped. The lineage's line counts it; the count
  excluding such panels (`above_excl_zero_campaign`) is printed beside.
- **What it decides.** On P-ADM-1, P-BRD-1, P-DIR-1 and P-SFP-VA-1: nothing — printed beside under the collar. On
  P-SCALP-3, and only there, the contract's kill names it: `D` (L-X.9) is true iff `above_excl_zero_campaign <
  above_half_bar(N)` on the TICK book at the seed of record. The excluding count is the one used because a panel
  that merely reproduces the headline is no evidence of breadth. (Where `D` can change the word, `C(TICK)` holds,
  clause (c) leaves no zero-trade asset, and the two counts coincide; the excluding count is named so the rule
  reads the same on any book.)
SOURCE: `scripts/tierc10_panel.py:1193-1199` (`above_half_bar`), `:1234-1339` (`loao_n`; `:1241-1242`, `:1316-1338`);
`scripts/tierc11_score.py:1009-1048` (`loao` over frames); `research_outputs/tierc11/LEANS.md:118`;
`x_rec/tierc11x/LEANS_X.md:695-696`, `:719-720`; contract :106.
RIVALS: LOAO deciding nothing on P-SCALP-3 too (L-X.9 rival ii). The declared-panel count `k` for the kill — it can
credit a panel that is the headline itself.
FAILS-IF: F-SCORE-ANCHOR (LOAO leg): the mirror on TC11's filed P-AGE-1 arms must reproduce `SCORES.json
rows[registration=P-AGE-1].stats.loao` (line, bar, per panel); planted mutations: a BELOW panel counted toward the
line; `N` taken as the panels that bootstrapped; the panels ruled vs zero under a two-sample headline.

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
  rows; on P-SCALP-3 the share of record is part of the verdict text; neither decides a word (see OPEN TO OPERATOR).
SOURCE: `scripts/tierc11_score.py:1076-1118` [read here]; `research_outputs/tierc11/scores/SCORES.json
rows[registration=P-AGE-1].concentration` (keys on file); `x_rec/tierc11x/LEANS_X.md:1019-1025`;
`x_rec/scripts/tc11x_score.py:437` (`harvest_rival`); `scout/U7_registrations_scoring.md` §1.4.
RIVALS: X's form of record — defined on paired Δ, which no TC12 row has. A typed cut (a share above one half kills)
— a number no file supplies.
FAILS-IF: F-SCORE-ANCHOR (CONCENTRATION leg): the mirror must reproduce `SCORES.json
rows[registration=P-AGE-1].concentration`; planted mutation: the top trade taken by `net_r` instead of `|net_r|`.

**L-X.13 THE IN-SAMPLE LABELS IN THE VERDICT TEXT** — "Label pre_seen …" (:54-55); "Label: direction informed by …"
(:58-59, :67); "§0 VERDICTS FIRST: the five rows with their labels" (:126-127); "in-sample labels carried" (:130)
READING:
- Label keys are `pre_seen` and `selection_hazard`, each filed as `{tag, label, text, items}` in the spec. Per O-23:

  | row | keys | tag | cell template (the `<verdict>` slot takes the word and its qualifiers) |
  |---|---|---|---|
  | P-ADM-1 | `pre_seen` | — | `<verdict> — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (pre_seen: <clause>)` |
  | P-BRD-1 | `selection_hazard` | DIRECTION-INFORMED | `<verdict> — NOT CONFIRMATORY (selection_hazard: DIRECTION-INFORMED)` |
  | P-DIR-1 | `selection_hazard` | DIRECTION-INFORMED | `<verdict> — NOT CONFIRMATORY (selection_hazard: DIRECTION-INFORMED)` |
  | P-SFP-VA-1 | `pre_seen` | — | `<verdict> — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (pre_seen: <clause>)` |
  | P-SCALP-3 | `pre_seen` | — | `<verdict> — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (pre_seen: <clause>)` |

- Two templates, keyed on the label keys exactly as X's LX-1.3 keys them: a row carrying `pre_seen` prints the
  RE-SCORE form; a row carrying `selection_hazard` only prints the shorter form with its tag. `<clause>` is the
  owner's `pre_seen.text` up to its first top-level `;` (TC11 SC-8) and says in plain words what was seen: for
  P-ADM-1 the file and cell under `research_outputs/tierc11/stage_g/`; for the two lanes X's standing line and the
  fact that X3 printed value-area swing-failure outcomes on these bars while this trade form was never scored. That
  clause is what keeps "RE-SCORE" from overstating on the lanes; the harsher template is taken because the label
  cannot flatter.
- P-BRD-1's cell is followed by disclosure D-1 (`research_outputs/tierc12/DISCLOSURES.md`), carried in the row's
  `disclosures[]` and printed directly under the cell.
- **Mechanics (X's `label_cell` law):** each registration's filed `verdict_rule` carries exactly one substring
  `prints '<verdict> …'`; the scorer builds the cell by substituting the word, and HALTs unless there is exactly
  one. The filing HALTs (detector TEMPLATE) unless the template's opening matches the row's label keys per the table.
- The family bar applies unchanged to a labelled row; a labelled row is never cited as confirmation, in §0, in
  FAMILY.json or in the ledger append. A CLOSED BY PRECONDITION row prints no label in its cell (L-X.10).
SOURCE: O-23; D-1, D-3, D-4; `x_rec/tierc11x/LEANS_X.md:728-737` (the two templates), `:2468-2470` (the standing
pre_seen line); `x_rec/tierc11x/LEANS_X_AMENDMENTS.md:429-441` (AM-X18, tags on `selection_hazard`-only rows);
`x_rec/scripts/tc11x_score.py:316-321` (`label_cell`), `x_rec/scripts/tc11x_registrations.py:512-520`
(`honesty_prints`); `scripts/tierc11_score.py:560-578` (SC-8), `:1894-1900`; contract :54-55, :58-59, :67.
RIVALS: TC11's single template on all five (prints "RE-SCORE" on two rows whose form and cohort were never scored).
A third, softer template for the lanes ("IN-SAMPLE, NOT CONFIRMATORY") — a wording no precedent files, and softer.
FAILS-IF: F-REG (TEMPLATE leg) is RED when a filed rule carries zero or two templates or a template that does not
match its keys; planted mutation: P-ADM-1's template rewritten to the `selection_hazard` form.

**L-X.14 THE BESIDE-PRINTS EVERY ROW CARRIES (Tier-E)** — ""a SELECTION, not a result" on every non-registered
table" (:7); "no promotion from any Tier-E table" (:133)
READING:
- Every leaf below carries L-0.16's collar (`tier`, `selection_not_a_result`, `gates`, `would_read_ci_only` — one
  of TC11's four readings — `m_looks_this_table`, `m_note`, `promotable = False`), no verdict word, no key matching
  `verdict|clears_bar|spent_test`. The scorer DERIVES them from the arms of record; a stage ships an arm only where
  a re-ride or another book is needed (its own `tierE__<slug>` arms, listed in its spec's `disclosed_beside`).
- **What L-X contributes to L-0.16's `REGISTERED_TABLES_T`** (collar-exempt): `scores/SCORES.json rows`,
  `scores/FAMILY.json`, `scores/S0_VERDICTS.md`'s table; each regbook's `scored` and `base` arm; P-SCALP-3's
  `ladder__touch` and `ladder__deep` arms (L-X.9's named exception). Everything else this section writes is
  collared: every `tierE__*` and `strip` arm, `SCORES.json beside`, `DRAWS.parquet`.

  | slug | what the scorer computes |
  |---|---|
  | `seed_sens` | the row's ruler at the sensitivity seed |
  | `haircut`, `haircut_sens` | the row's ruler on `haircut_net_r` (the charter-slippage twin) at both seeds |
  | `taker_twin` | the row's ruler on `taker_twin_net_r`; on an all-taker arm the leaf reads `IDENTICAL TO THE RECORD (every leg taker)` and repeats no number |
  | `tuning_slice`, `holdout_slice` | the row's ruler on the rows of each era (era by the entry bar's close), in every arm. P-SCALP-3's era of record is the holdout: Stage S ships `tierE__full_corridor`, and the scorer prints `full_corridor` and its `tuning_slice` |
  | `loao`, `loao_sens` | L-X.11's table at both seeds |
  | `concentration`, `share_x` | L-X.12, both definitions |
  | `literal_bar` | the rival of L-X.8: `p`, the (100 · bar)-th percentile of the record's draws, `clears_literal_bar` |
  | `exact` | the enumerated cluster bootstrap, with `u` = the number of clusters: every composition `k` of `u` picks over the sorted clusters, weight `u! / Π k_a!` of `u^u`; vs zero the atom is `Σ k_a S_a / Σ k_a n_a` (X's `exact_cluster`); two-sample it is that ratio on the kept arm minus the same ratio on the base arm, over the union's clusters; `p_exact`, `lo_exact`, `hi_exact` decided in integers at the levels X fixes (`CI_LO_Q`, `CI_HI_Q`) |
  | `month_block` | the row's ruler with the cluster = the UTC calendar month of the entry close, same seed and B |
  | `drop_open` | the row's ruler with every `exit_reason == "corridor_end"` row removed from every arm; `n_open_at_pin` per asset |
  | `strip` | the forward strip arm: `n` and a pointer (path, file sha, book sha). NO statistic — no mean, no sum, no interval (O-9) |

- **Flags on the row, deciding nothing:** `SEED-FRAGILE` iff the frozen rule at either seed gives another word than
  the same rule on the exact enumeration (`lo_exact > 0 AND p_exact ≤ bar`); `TIME-CLUSTER FRAGILE` iff the
  `month_block` `lo ≤ 0` while the record's `lo > 0`; `VERDICT RESTS ON OPEN MARKS` iff the frozen rule on the
  `drop_open` twin gives another word (a boolean; the twin's word is never filed); and the size footnote (X's text,
  regenerated on synthetic exchangeable clusters by F-VERDICT's SIZE leg, no outcome read).
- `m_looks_this_table` = the number of interval-bearing leaves in `SCORES.json beside[]`.
SOURCE: `scripts/tierc11_score.py:1185-1203` (`stats_block`), `:258-263` (collar and forbidden keys);
`x_rec/scripts/tc11x_score.py:136`, `:139-140`, `:221-255`, `:281-286`, `:289`; `x_rec/tierc11x/LEANS_X.md:686-718`,
`:814-830`, `:1529-1531`, `:1566-1569`; `x_rec/tierc11x/LEANS_X_AMENDMENTS.md:211-219` (AM-X10 items 2-5); O-9, O-13.
RIVALS: slices shipped by the stages — a second builder for the same rows. A two-arm enumeration left out — X's
`exact_cluster` is one-sample, and the Monte Carlo error of p is material at the two m = 2 bars
(`x_rec/tierc11x/LEANS_X.md:697`).
FAILS-IF: F-COLLAR is RED when a beside leaf lacks a collar key or carries a verdict word; F-GRID is RED when the
written leaves are not the declared set per row; planted mutations: a leaf dropped; a `strip` leaf given a mean; a
`verdict` key planted in a leaf.

**L-X.15 F-FAM** — "F-FAM (m and bars printed per family; a precondition-closed row spends no test)" (:122-123)
READING: three legs, each with its named detector.
- **PARSE (L-X.1):** the three families re-parsed by the fixture's own regex from the contract prefix and compared
  with the filing and with `scores/FAMILY.json`; prints family · stage · header line · m · bar · bar_exact · deciding
  rank.
- **REAL:** on the scored tier, each row's `family`, `m`, `bar_exact` are its family's; `tests_spent_f` = the rows
  of f with status BUILT and no HALT; `tests_spent_f ≤ m_f`; a row with `spent_test = false` has every numeric leaf
  null.
- **PLANTED:** a scratch filing built from a scratch contract carrying one header in the same grammar (a family of
  m = 2), with one BUILT row on a synthetic book (no Naiad data) and one row whose precondition item reads a
  planted record that fails. Expected: `tests_spent = 1`; the bar stays q ÷ 2; the closed row is number-free with
  cell `CLOSED BY PRECONDITION (…) — no number · no test spent`; a call counter proves no ruler ran for it.
SOURCE: nearest code `scripts/tierc11_score_fixtures.py:1521-1535`, `:1630` (TC11's family leg on a planted family);
`x_rec/scripts/tc11x_score_fixtures.py:852`, `:1152-1154`, `:1281-1282`; no fixture named F-FAM exists in either tree
(`scout/U7_registrations_scoring.md` §1.10).
RIVALS: prove "spends no test" on a real row — none of the five can close on the records as filed.
FAILS-IF: any leg's condition above fails. Planted mutations, each caught by its named detector: the planted bar
recomputed as q ÷ (tests spent) → `M-LOOSENED`; the closed row counted as spent → `TESTS-SPENT`; a `point` planted
on the closed row → `CLOSED-NUMBER`; a `scored.parquet` planted in the closed regbook → `CLOSED-HAS-ARM`; a row
scored at another family's bar → `BAR-OF-FAMILY`.

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
SOURCE: `research_outputs/tierc12/progress/STEP_Q.json` (sha `8da374a7…1c27c`); the contract re-hashed [measured
here: 12,209 B, 137 `\n`, ends on `\n`]; `exchange/queue/README.md:8-12` (rule 6: "`BUILT: <artifact or commit>` on a
line of its own"); `scout/U1_rulings_close_state.md` §1.4, R-18 (a whole-file pin is what made TC11's stamp a
cascade); O-10.
RIVALS: pin the whole file (TC11, X) — the queue's own stamp then breaks every pin, which is the question the
contract's `"tc11-stamp"` ruling had to answer for TC11. Accept any tail — leaves the text open below the pin.
FAILS-IF: F-CONTRACT-PIN (the registry's leg beside L-0.1's F-CONTRACT) is RED when a scratch copy with
`BUILT: x\n` appended changes any slice, payload sha, chain head or verifier finding; planted mutations: one byte
flipped inside the prefix (must HALT `CONTRACT-PREFIX`); the `BUILT:` line inserted under `RATIFIED` (must HALT
`CONTRACT-PREFIX`); a tail line `NOTE: x` (must HALT `CONTRACT-TAIL`).

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
  `stage_g/STAGE_G.md`, `x_rec/tierc11x/LEANS_X.md`), its file sha asserted first.
SOURCE: `x_rec/tierc11x/REGISTRATION_PLAN.md:20-27` (the law, verified against TC11's own filing);
`scripts/tierc11_registrations.py:194-202`; `scout/U7_registrations_scoring.md` §1.11 (the same map, independently).
RIVALS: cite by quoted text instead of lines — no hash to verify. Cut from the live whole file — moved by a stamp.
FAILS-IF: F-REG is RED when any text, context or external slice does not re-cut from pinned bytes or its sha
differs from the map; planted mutation: one character edited in a filed `text_of_record`.

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
- The filing script types no text, no spec and no number: it slices, parses, carries and hashes.
SOURCE: `x_rec/tierc11x/REGISTRATION_PLAN.md` (sha `a887ea64…3d15`; §0 `:18-48`, §1 `:53-301`, §2 `:304-331`);
`x_rec/scripts/tc11x_registrations.py:111-116`, `:329-360`, `:523-670`; `scout/U7_registrations_scoring.md` R1.
RIVALS: specs typed in the script (TC11) — nothing to diff the filing against, and a single family assumed.
FAILS-IF: F-REG (SPEC-VERBATIM leg) is RED when an `operative_spec` leaf differs from the plan's block or the plan's
block from the LEANS's; planted mutation: one word changed in the plan's `arms` field of one registration.

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
  labels, disclosed_beside, failure_conditions}`, `verdict_rule`, `text_sha256`, `sha256`;
- **payload sha** = `sha256(json.dumps(body without text_sha256 and sha256, sort_keys=True,
  ensure_ascii=False).encode("utf-8"))`;
- **chain**: for each registration in `seq` order `line = {seq, registration, sha256, prev}`, `line_sha256 =
  sha256(json.dumps(line, sort_keys=True).encode())`, `prev` of the first = `"0" * 64`, `head` = the last
  `line_sha256`;
- `law` is read by object from `research_outputs/tierc11/registrations/REGISTRATIONS.json["law"]` (file sha
  `648834bf…f1ee` asserted) and `law_source` names that path, sha and key;
- `scored_window.end_ms` is read from `research_outputs/tierc11/data/AS_OF_PIN.json
  ["as_of_last_closed_4h_close_ms"]` and `era_cut.ms` from `x_rec/tierc11x/pins/PINS_X.json["era_cut_ms"]`; the
  scorer HALTs unless they equal L-D's objects `E.TC11_PIN_MS` and the env's era cut (O-9);
- `amendments` names `LEANS_AMENDMENTS.md` as it stands at filing (it holds the dated V2-versus-X amendment of
  O-16); a later amendment never edits the filing — the scorer pins the then-current file separately (L-X.23);
- rendering: `json.dumps(doc, indent=2, ensure_ascii=False) + "\n"`, insertion order, UTF-8; no clock, no host, no
  path outside the repo in any leaf.
SOURCE: `x_rec/scripts/tc11x_registrations.py:496-509` (`payload_sha`, `chain_of`), `:658-670`, `:673-675`;
`scripts/tierc11_registrations.py:204-221`; `x_rec/tierc11x/registrations/REGISTRATIONS_X.json` (keys read here);
`research_outputs/tierc11/data/AS_OF_PIN.json`, `x_rec/tierc11x/pins/PINS_X.json` (keys read here).
RIVALS: bars as floats; a timestamp in the filing (breaks F-DET; neither precedent carries one).
FAILS-IF: F-REG is RED when a payload sha or the chain does not re-derive from the filed bodies from `"0" * 64`;
planted mutations: one `prev` bent; `family_m` of one body changed; a registration's order swapped.

**L-X.20 WRITE-ONCE, AND `REGISTRY_PIN.json`** — "frozen texts" (:5)
READING:
- `--file` HALTs if `REGISTRATIONS.json` or `REGISTRY_PIN.json` exists, then creates both with `open(path, "xb")`;
  nothing is ever overwritten; there is no refile flag and no `_rerun` twin for the registry. A second `--file`
  leaves both files' bytes unchanged.
- `REGISTRY_PIN.json` (generated; `json.dumps(pin, indent=2, sort_keys=True, ensure_ascii=False) + "\n"`):
  `registrations_file {path, bytes, sha256}`, `order_of_filing`, `registry_len`, `genesis`, `head`, `chain` (the
  line shas), `registrations {<id>: {seq, sha256, text_sha256, text_lines, prior_pct, family, family_m,
  family_bar}}`, `families`, `contract`, `leans`, `amendments`, `plan`, `review`, `rulings`, `seed`, `seed_sens`,
  `n_boot`, `law`, `law_source`, `spec_carry_law`, `witness_law`, `text_before_result_law`.
- Both files are tracked (the nested `.gitignore` excludes only parquet, `_det_*/` and `x_rec/**`) and are committed
  alone with the frozen LEANS, the plan, the review record and `ATTEST_REG.json`, subject `tierc12(TC12-REG): …`.
SOURCE: `x_rec/scripts/tc11x_registrations.py:682-711` (`pin_of`), `:714-727` (`file_filing`);
`scripts/tierc11_registrations.py:241-247`; `research_outputs/tierc12/.gitignore`; O-2.
RIVALS: `write_text` behind an exists-check (TC11) — a race between check and write; exclusive create has none.
FAILS-IF: F-REG (WRITE-ONCE leg) is RED when a second `--file` changes a byte or exits 0, in the filed directory
and in a scratch twin; planted mutation: `"xb"` replaced by `"wb"` in a scratch copy of the filer.

**L-X.21 TEXT BEFORE RESULT** — "families declared by MECHANISM before the look" (:8)
READING: three clauses, each checked.
1. **Write-once** (L-X.20).
2. **The head is stamped into every book.** Every `regbooks/<ID>/STATUS.json`, every arm sidecar and every stage
   `build_manifest.json` that holds a book carries `registry_head` and `registrations_sha256`; the scorer HALTs a
   row (`HEAD-STAMP`) whose STATUS or sidecar lacks them or carries other values than `REGISTRY_PIN.json`'s.
3. **A git-order attestation, run out of process** (git facts gathered by a subprocess of the fixture module;
   `--no-optional-locks`; read-only verbs), keyed on TC12's own paths (`research_outputs/tierc12/`,
   `scripts/tierc12_*`, `analytics/value_area.py`, `exchange/rows/tierc12/`) because the branch takes an
   `exchange: auto-publish` commit every day:
   - **ATTEST-REG, at filing.** The working tree under `research_outputs/tierc12/` — walked on disk, ignored and
     untracked files included — holds no file outside PRE_REG = the `artifact_shas` paths of the progress records
     of the stages L-0 orders before TC12-REG, those records, `PROGRESS.json`, `.gitignore`, `scout/**`, `x_rec/**`,
     `leans_draft/**`, `review/**`, `registrations/**`, and the top-level documents (`LEANS.md`,
     `LEANS_AMENDMENTS.md`, `AMENDMENTS_PROPOSED.md`, `REGISTRATION_PLAN.md`, `ORCHESTRATOR_RULINGS.md`,
     `DISCLOSURES.md`); no `.parquet` exists anywhere under it outside `x_rec/`; `scripts/tierc12_*.py` ⊆ the
     scripts those records name. The sorted listing with each file's sha is filed as
     `registrations/ATTEST_REG.json` in the registration commit.
   - **ATTEST-ORDER, at TC12-SCORE, at CLOSE and in `close_acts.sh` step 0.** `REG` = the unique commit adding
     `registrations/REGISTRATIONS.json` (`git log --diff-filter=A --format=%H -- <path>`), whose blob equals the
     working file and the pin's sha. For every tracked TC12 path P outside PRE_REG, `first_add(P) ≠ REG` and `git
     merge-base --is-ancestor REG first_add(P)` holds. Ignored parquet is bound through clause 2 and through its
     stage's progress record, itself a tracked path under this test.
SOURCE: `x_rec/scripts/tc11x_registrations.py:916-958` (`attest_findings`, HEAD-LAW; the one order fixture on
disk); `x_rec/tierc11x/REGISTRATION_PLAN.md:362` ("no book of any kind before X-REG");
`scout/U7_registrations_scoring.md` §1.3 (no builder stamps the head in either tier), R15, H9.
RIVALS: a timestamp in the filing — a clock is not evidence and breaks F-DET. An attestation on `HEAD` adding only
tier files — fails on the first auto-publish commit.
FAILS-IF: F-ATTEST-ORDER is RED when any clause fails. Planted mutations, in scratch repositories: a STATUS.json
committed before the filing commit (ORDER); a STATUS carrying another head (HEAD-STAMP); an ignored
`books/x.parquet` present at filing (ATTEST-REG).

**L-X.22 THE VERIFIER** — "frozen texts" (:5)
READING: `verify_filing(doc, pin, contract_bytes, reg_bytes, ext_bytes, plan_bytes, leans_bytes) -> list[str]` is the
scorer's first act and F-REG's production side; `[]` iff every detector is silent: `CONTRACT-PREFIX` ·
`CONTRACT-TAIL` · `TEXT-SLICE` · `CONTEXT-SLICE` · `EXTERNAL-SLICE` · `PAYLOAD-SHA` · `SEED` · `FAMILY-PARSE` ·
`FAMILY-BAR` · `FAMILY-MEMBER` · `FAMILY-M-COUNT` · `RULER-TEXT` · `TEMPLATE` · `CHAIN` · `HEAD-PIN` ·
`SPEC-VERBATIM` · `PLAN==LEANS`. F-REG runs it and, beside it, an independent re-derivation written in the fixture
file (slices, shas, chain), so the production verifier is never compared with itself.
SOURCE: `x_rec/scripts/tc11x_registrations.py:731-805`; `scripts/tierc11_score.py:391-492`;
`x_rec/scripts/tc11x_registrations_fixtures.py:19-56`.
RIVALS: none.
FAILS-IF: F-REG is RED unless each plant is caught by its intended detector, one at a time: a contract byte; a text
character; a context range; a payload leaf; the seed; a header's bar; a chain `prev`; the pin's head; a spec word.

---------------------------------------------------------------------------------------------------------------
### C · The scorer

**L-X.23 SCORER INPUTS, EACH PINNED BY SHA** — "no number typed that a file can supply" (:8)
READING: `scripts/tierc12_score.py [--regbooks-root=DIR] [--out-dir=DIR] [--dry-run] [--refile=<AM-n|FIX-n>]`
reads, in this order, and HALTs the run on the first failure:
1. the contract through L-X.16;
2. `registrations/REGISTRATIONS.json` and `REGISTRY_PIN.json`: file shas equal to
   `progress/TC12-REG.json artifact_shas`; `verify_filing` returns `[]`;
3. `LEANS.md`: sha equal to the filing's `leans.sha256`;
4. `LEANS_AMENDMENTS.md`: sha equal to `PROGRESS.json["amendments_of_record"].sha256`; the sha is filed in the
   manifest, so a reader sees which amendments were in force when the row was scored;
5. L-D's fee schedule and pins (paths and shas from `progress/TC12-D.json`);
6. per registration, `regbooks/<ID>/STATUS.json` and each arm it lists: the file sha of every parquet and sidecar
   equal to the owning stage's progress record (`progress/TC12-G.json`, `TC12-R.json`, `TC12-S.json`); the canonical
   `book_sha256` recomputed from the parquet equal to the sidecar's; `registry_head` per L-X.21;
7. each precondition record named by a spec, by path and by the sha its certifying progress record files (L-X.10;
   L-V's `va/VA_MIRROR.json` through `progress/TC12-V.json`).
The scorer reads no TC11 or X file except the pinned constants this section names (`SCORES.json["n_boot"]`,
`["seed_sens"]`, `BASE_IDENT.json`, TC11's `AS_OF_PIN.json`, `PINS_X.json["era_cut_ms"]`) and, in F-SCORE-ANCHOR
only, TC11's filed regbooks.
SOURCE: `x_rec/scripts/tc11x_score.py:339-373` (`verify`, `load_inputs`: each input bound to its stage's progress
record); `scripts/tierc11_score.py:495-505`, `:2577-2608`; O-3, O-4, O-6.
RIVALS: shas typed in the scorer (TC11) — a re-pin then edits code. Books pinned only by their own sidecars (TC11) —
a sidecar can be rewritten with its book.
FAILS-IF: F-SCORE-INPUTS is RED when the scorer scores with a pinned input changed; planted mutations: one LEANS
byte; one byte of a regbook parquet (sidecar left alone); an arm on disk that STATUS does not list scored anyway.

**L-X.24 THE REGBOOK INTERFACE (what Stages G, R and S write)** — "F-KEY" (:124)
READING: the directory-level F-KEY (declared keys, as-of stamps, collar totality) is L-0.21's and runs on every
regbook directory; the ROW-level laws below are the scorer's, proven by F-REGBOOK.
- **Layout.** `research_outputs/tierc12/regbooks/<ID>/` holds `STATUS.json` and, per arm, `<arm>.parquet` +
  `<arm>.json`. Arm names match `^(scored|base|ladder__(touch|deep)|strip|tierE__[a-z0-9_]+)$`. The arm of record is
  `scored` (TC11's name; "treated" is not a name on disk). `base` exists on the three two-sample rows and only
  there. `ladder__touch` and `ladder__deep` exist on P-SCALP-3 only, where `scored` is the TICK book.
- **`STATUS.json`:** `registration`, `status` ∈ {`BUILT`, `CLOSED_BY_PRECONDITION`}, `reason`, `arms` (every arm on
  disk, no other), `registry_head`, `registrations_sha256`, `source_script`, `source_script_sha256`,
  `preconditions` (each item with the value found). A parquet on disk that `arms` does not list is a note and is
  not read.
- **Columns, exact dtypes.** TC11's sixteen, unchanged and in this order (read by `ast` from
  `scripts/tierc11_score.py:248-255`, sha asserted): `symbol` str · `entry_ms` int64 · `entry_close_ms` int64 ·
  `direction` int8 · `entry_px`, `stop_px`, `r_dist` float64 · `exit_close_ms` int64 · `exit_reason` str · `net_r`,
  `gross_r`, `fee_r`, `funding_r`, `haircut_net_r` float64 · `era` str · `lane` str. Then TC12's four, all
  float64: `fee_taker_r` (the fee of the taker legs ÷ `r_dist`) · `fee_maker_r` (the fee of the maker legs ÷
  `r_dist`) · `fee_all_taker_r` (the fee of every leg priced at the taker rate ÷ `r_dist`) · `taker_twin_net_r`
  (the all-taker twin's net R). Extra columns are allowed and ignored.
- **Meaning.** `symbol` is the asset (a fee-schedule stem). `entry_close_ms` is the close of the lens bar in which
  the position was entered (P-SCALP-3: the 5m bar of the fill); `entry_ms` is that bar's open. `net_r` is the toll
  of record in R; `funding_r` is the journaled funding, positive = paid; `haircut_net_r` is the charter-slippage
  twin; `taker_twin_net_r` is the TC-series all-taker twin.
- **Laws, each a HALT on `scored`, `base` and `ladder__*` arms** (a NOTE on `tierE__*` arms where TC11 notes):
  no null; unique `(symbol, entry_close_ms)`; `base` also unique on `(symbol, entry_ms)`; `direction` ∈ {+1, −1};
  `era == era_of(entry_close_ms)` (tuning iff the close ≤ the era cut); `0 < entry_close_ms − entry_ms ≤` one bar
  of the sidecar's `lens` (required, no default; the step read from L-D's lens table, of which TC11's
  `LENS_STEP_MS` at `scripts/tierc11_score.py:294-295` is the filed form); `exit_close_ms ≥ entry_close_ms`;
  `r_dist > 0`; every symbol in
  the sidecar's `panel`, and that `panel` equal to L-D's home panel on every `scored`, `base` and `ladder` arm; no
  `,`, `"`, CR or LF in a string;
  - **the scored window (O-9):** `entry_close_ms ≤ W` and `exit_close_ms ≤ W`, `W` = `E.TC11_PIN_MS` (equal to the
    filing's `scored_window.end_ms`); a position still open at `W` is marked there with `exit_reason =
    "corridor_end"`; `strip` arms hold exactly the rows with `W < entry_close_ms ≤ E.PIN_MS`;
  - **the fee identities:** `|fee_r − (fee_taker_r + fee_maker_r)| ≤ HAIRCUT_TOL`; `|taker_twin_net_r − (net_r +
    fee_r − fee_all_taker_r)| ≤ HAIRCUT_TOL`; on an arm whose sidecar `toll` is `taker`: `fee_maker_r == 0`,
    `fee_taker_r == fee_r`, `fee_all_taker_r == fee_r` and `taker_twin_net_r == net_r` exactly;
  - **the haircut law (TC11's AM-7 with its maker clause):** `|haircut_net_r − (net_r − fee_taker_r ×
    slip_bps_side / taker_bps_side)| ≤ HAIRCUT_TOL`, the two rates read per symbol from `E.fees()` (L-D); a maker
    leg carries no slippage;
  - **the net law, a disclosure only:** rows with `|net_r − (gross_r − fee_r − funding_r)| > NET_LAW_TOL` are
    counted and printed.
  `HAIRCUT_TOL`, `SUM_TOL`, `NET_LAW_TOL` are read by `ast` from `scripts/tierc11_score.py:264-266`.
- **Sidecar `<arm>.json`:** `registration`, `arm`, `kind` ∈ {`base`, `scored`, `ladder`, `strip`, `tierE`}, `ruler`
  ∈ {`two_sample`, `vs_zero`}, `era_scope` ∈ {`full`, `holdout`, `tuning`}, `panel` [stems], `lens`, `toll` ∈
  {`taker`, `maker_entry_targets__taker_stop`}, `fill_rule` (P-SCALP-3: `tick` / `touch` / `deep`), `n`,
  `sum_net_r` (within `SUM_TOL` of the parquet's), `book_sha256`, `book_ext_sha256`, `registry_head`,
  `registrations_sha256`, `fee_schedule {path, sha256}`, `description`, `source_script`, `source_script_sha256`;
  `tierE` sidecars carry the collar keys.
- **Two hashes.** `book_sha256` = TC11's SC-13 law over the sixteen columns (canonical CSV: rows sorted `(symbol,
  entry_close_ms)`, header, `,`-joined, ints `str(int)`, floats `repr(float)`, `\n` after every line), so a TC12 arm
  is comparable with a TC11 arm; `book_ext_sha256` = the same law over the twenty.
- **Cross-arm law on P-SCALP-3:** `n(ladder__touch) ≥ n(scored) ≥ n(ladder__deep)`, else HALT `LADDER-ORDER`.
SOURCE: `scripts/tierc11_score.py:245-266`, `:294-299`, `:618-635` (`canonical_csv`), `:646-770` (`validate_book`),
`:773-830`; `research_outputs/tierc11/regbooks/P-AGE-1/base.json` (the sidecar's filed form, `book_sha256_law`);
`research_outputs/tierc11/LEANS_AMENDMENTS.md:86-97` (AM-7); contract :101-102, :120; O-9, O-19;
`scout/U7_registrations_scoring.md` §1.8, §2.14, R13.
RIVALS: TC11's sixteen alone with AM-7 as written — a maker-toll scored arm cannot pass it (it assumes every fee leg
taker). A `fee_taker_r`-only extension (U7 R13) — leaves the all-taker twin unverifiable by identity.
FAILS-IF: F-REGBOOK is RED unless each plant on a copy of a real arm is caught by its named detector: era by the
open; a duplicate key; a null `net_r`; a dropped column; `direction` 0; float32; the haircut law broken on a maker arm;
`taker_twin_net_r` bent on a taker arm; an entry bar longer than the lens; an exit before entry; a row past `W` in
`scored`; a strip row at or before `W`; a stray asset; a comma in a string; a sidecar `n`, `sum_net_r` or
`era_scope` bent; a missing `registry_head`.

**L-X.25 GATES AT THE SCORER: ONE BASE, POST-FILTERS ONLY** — "both two-sample vs v6 — they remove trades" (:52)
READING:
- **F-BASE-IDENT.** The three `base` arms carry ONE `book_sha256`, and it equals
  `research_outputs/tierc11/scores/BASE_IDENT.json["book_sha256"]["P-AGE-1"]` (on file `f41bfaf0…68a8`; that file's
  sha `29f795dc…5581` asserted): the base is TC11's filed v6 book, bit for bit on the sixteen columns (O-21). A
  difference HALTs all three rows.
- **GATE-POSTFILTER (TC11's SC-16).** HALT a gate's row if its scored arm holds a key `(symbol, entry_ms)` absent
  from the base, or if a kept row differs from the base's on any of the sixteen columns (floats and ints compared
  exactly).
- The refused set equalling the contract's text is the owners' F-GATE, F-BRD and F-DIR, not the scorer's.
SOURCE: `scripts/tierc11_score.py:914-942` (`gate_findings`), `:1302` (`base_ident`);
`research_outputs/tierc11/scores/BASE_IDENT.json`; `research_outputs/tierc11/regbooks/P-AGE-1/base.json`; O-21.
RIVALS: one shared base file outside the regbooks — breaks the per-registration interface the contract's F-KEY
checks. Equality at 6 dp (TC11's SC-7 against `books/v6_campaigns.parquet`) — printed beside; the canonical sha is
the stricter and is of record.
FAILS-IF: F-BASE-IDENT is RED when any base arm's `book_sha256` differs from the filed value; planted mutations:
one base `net_r` moved by one ulp; one base row dropped; a gate's kept row altered; a campaign added to a gate.

**L-X.26 WHAT THE SCORER WRITES** — "§0 VERDICTS FIRST: the five rows with their labels" (:126-127)
READING: under `research_outputs/tierc12/scores/`:
- `SCORES.json`: `tier`, `stage`, `inputs` (every sha of L-X.23), `seed`, `seed_sens`, `n_boot`, `scored_window`,
  `era_cut`, `verdict_law`, `families`, then
  - `rows` — exactly one leaf per registration, in `seq` order: `registration`, `seq`, `family`, `m`, `bar`,
    `bar_exact`, `bar_cell`, `prior_pct`, `status`, `status_reason`, `ruler`, `era_scope`, `panel`, `lens`,
    `preconditions`, `n`, `n_base`, `n_clusters`, `point`, `lo`, `hi`, `p_num`, `p_den`, `p_one_sided`,
    `n_draws_finite`, `n_draws_le_0`, `deciding_rank`, `deciding_bound`, `clause_a`, `clause_b`, `clause_c`,
    `verdict_of_record`, `qualifiers`, `labels`, `disclosures`, `verdict_cell`, `verdict_text`,
    `stable_across_seeds`, `spent_test`, `premise`, `gate` (gates), `fill_ladder` and `one_asset` (P-SCALP-3),
    `draw_sets`, `provenance`, `halts`, `notes`;
  - `beside` — exactly one leaf per beside-print, keyed `(registration, slug)` (L-X.14), collared.
- `FAMILY.json`: `q`, `n_boot`, `families [{family, stage, header_line, m, bar, bar_exact, deciding_rank,
  registrations, tests_spent, supported, rows [{registration, seq, status, verdict_of_record, spent_test, p_num,
  p_den, clause_a, clause_b, clause_c, label}]}]`, `tests_spent_total`, `law`.
- `BASE_IDENT.json` (L-X.25) · `REGISTRY_CHECK.json` (L-X.22's findings and every sha it read) · `S0_VERDICTS.md`
  (the five rows as a table, the bytes the report's §0.1 quotes) · `SCORE_MANIFEST.json` (inputs, outputs, the
  scorer's own sha) · `DRAWS.parquet` · `REFILE_LOG.jsonl` · `build_manifest.json` · `FIXTURES_SCORE.txt`.
- **Draws persisted.** `DRAWS.parquet`, key `(registration, draw_set, draw_idx)`, holds every draw of the sets that
  bear on a word: `record` and `sens` for each row; `ladder_touch`, `ladder_deep` and the five `loao_<asset>` sets
  for P-SCALP-3. Columns: `draw` (6 dp), `draw_hex` (`float.hex`, exact), `seed`, `n_boot`, `cluster_kind`,
  `n_values`, `n_clusters`, `values_sha256`, `draws_sha256`, the collar and the as-of columns. Every other
  beside-print files its `seed` and `draws_sha256` only. F-BOOT re-derives `lo` and `p` from `draw_hex`.
SOURCE: `research_outputs/tierc11/scores/` (file set and keys read here: `SCORES.json`, `FAMILY.json`,
`SCORE_MANIFEST.json`); `x_rec/tierc11x/registrations/SCORED_X.json`, `SCORED_X_DRAWS.parquet` (columns read here),
`build_manifest.json` (`float_precision`); `x_rec/scripts/tc11x_score.py:729-750` (`draws_frame`);
`scripts/tierc2_baseline.py:162-188` (the estate's table writer: floats rounded by `_round_floats`, hence
`draw_hex` beside `draw`).
RIVALS: draws not persisted (TC11) — `lo` and `p` can then only be compared with their own printed values.
FAILS-IF: F-GRID is RED when `rows` is not the filing's registrations in `seq` order, `families` not the filing's
families, or `beside` not the declared set; planted mutations: a row dropped; a row duplicated; an undeclared
beside leaf.

**L-X.27 THE WRITE LAW: NO CLOBBER, A LOGGED REFILE, AN EXIT WORD** — "Q1/Q2 keep SCORES.json leaves" (:13)
READING:
- Each output: identical bytes → left alone; absent → written atomically (`.tmp` then `os.replace`); different
  bytes and no `--refile` → written beside as `<stem>_rerun<suffix>`, the record untouched. `DRAWS.parquet` is
  compared by content sha.
- `--refile=<id>` replaces the records only if `<id>` is a heading of `LEANS_AMENDMENTS.md` or a key of
  `progress/TC12-FIX.json`, and appends one line to `REFILE_LOG.jsonl`: the id, each replaced file's sha before
  and after, and for `SCORES.json` the counts of leaves added, removed and changed, the changed leaves split into
  numeric and non-numeric with their JSON paths. The question TC11 left open as Q1 is thereby answered by a file.
- The exit code is the bitwise OR of TC11's flags, read by `ast` from `scripts/tierc11_score.py:301-302`: a
  registered row HALTed · a Tier-E leaf halted · a registration ABSENT · a no-clobber refusal; nothing masks
  another. `--dry-run` validates every input and interface, calls no ruler and writes nothing.
- Two subprocess runs into `_det_score/`, under the two `PYTHONHASHSEED` values of the estate's F-DET law (TC11
  L-F.1's first literal and the tier's seed of record), are byte-equal to each other and to the records; no clock,
  worker count or load average appears in any output.
SOURCE: `scripts/tierc11_score.py:2611-2634`, `:2648-2665`, `:2450`; `research_outputs/tierc11/LEANS.md:520-521`
(L-F.1); `research_outputs/tierc11/BUILD_DRAFT.md:5943`, `:5988` (MINOR-9 and Q1);
`x_rec/scripts/tc11x_score.py:995-999` (X overwrites — not taken).
RIVALS: X's overwrite; TC11's unlogged `--refile` — the cause of Q1.
FAILS-IF: F-EXIT is RED when a differing output is overwritten without `--refile`, a `--refile` with an unknown id
is accepted, or a flag is masked; F-DET is RED on any byte; planted mutations: one byte bent in a record before a
re-run; a pid salt; a set-iteration line.

---------------------------------------------------------------------------------------------------------------
### D · CLOSE

**L-X.28 THE REPORT AND ITS ORDER** — "CLOSE: exchange/reports/BUILD_2026-10-08_TIERC12_VALUE_AREA.md — §0 VERDICTS
FIRST: the five rows with their labels, the VA chop table (with-vs-against), the feasibility mirror, the ledger's
appended rows · the families · Stage V pins and the traverse table · the VA stack whole · the scalper's
fill-sensitivity and twins · findings-not-fixed · BOX-COST · LEDGER_APOLLO append" (:126-129)
READING:
- Drafted OFF-BUS at `research_outputs/tierc12/BUILD_DRAFT.md` by `scripts/tierc12_close.py`, a deterministic
  generator that writes only its named outputs (the draft, the staged append, `close/S5_FINDINGS_NOT_FIXED.{json,md}`,
  `close/BOX_COST.{json,md}`, `close/TRACES.json`, `close/COMPUTE_LEDGER.json`, `close/close_acts.sh`), never under
  `exchange/`, and never commits, pushes or calls `publish()`. It reaches its destination only through
  `close_acts.sh` (LAW 5).
- The contract's named parts keep the contract's order; sections the standing conventions require are placed
  where they break none of it:

  | § | content |
  |---|---|
  | header | title = contract :1; the contract path and prefix sha; executor, seed, branch; the scored window and both pins; the reading rule; the size line (FLAGGED when over the wire); a status stamp filled at close |
  | **0 · VERDICTS FIRST** | 0.1 the five rows with their labels — `scores/S0_VERDICTS.md`'s table rows byte for byte, in filing order; under P-SCALP-3 its fill-sensitivity row · 0.2 the VA chop table, the with-vs-against cut, from Stage R's record, collared · 0.3 the feasibility mirror: the five words against X's record, the rows of the other eras beside (O-17), and the sentence that the licence was earned on X's record machine, not on V2 (O-16, D-2) · 0.4 the ledger's appended rows: the four books side by side, unscored |
  | 1 · THE FAMILIES | `FAMILY.json` rendered: q; per family m, bar, deciding rank, registrations, tests spent; the verdict law and its rival; the three-families sentence of L-X.2 |
  | 2 · STAGE V — PINS AND THE TRAVERSE TABLE | L-V's records |
  | 3 · THE VA STACK WHOLE | L-V's and L-R's grids, every cell |
  | 4 · THE SCALPER — FILL-SENSITIVITY AND TWINS | the P-SCALP-3 verdict text re-quoted under the registered marker (L-X.29), the three fill books, the miss column, the all-taker and charter twins, the regime columns |
  | 5 · THE OTHER STAGES, EACH GRID WHOLE | D (substrate, fees, pins) · C (the control and the strip) · G · R (Tier-E) · L (the era tables, the ferry forecast) |
  | 6 · FIXTURES | the roll: suite, tally, transcript sha |
  | 7 · FINDINGS — REPORTED, NOT FIXED | L-X.30 |
  | 8 · BOX-COST AND COMPUTE COST | L-X.31, with the seven-column file-disposition table |
  | 9 · DISCLOSURES, AMENDMENTS, OPEN QUESTIONS, WHAT THIS BUILD IS NOT | every line of `DISCLOSURES.md`; one line per amendment; contract :132-134 quoted |
  | 10 · THE LEDGER APPEND | the staged append, verbatim, inside one fence |
  | 11 · STATE PUSH AND THE CLOSE ACTS | the push stamp; the acts' step list; the last line `Operator: click Sync now.` |

- **"Whole", frozen by KIND, not by size:** a grid (a table whose cells F-GRID declares) prints every cell in the
  document; a per-trade, per-instant, per-bar or per-draw table is pointed to by path, file sha, row count and key,
  never inlined. The kind of every table is typed in the generator before any book exists.
- **Cap.** The generator HALTs if the draft exceeds the per-file cap parsed from `publish_exchange.POINTER_RULE`
  (`(\d+) MB per file`, decimal MB — TC11's reading, the stricter of the two caps on disk).
- **Precedence where conventions collide.** CONVENTIONS §3.2 ends a document on the file-disposition table and
  §3.1 on the ledger entry; the contract names a final line. The operator's ratified contract outranks both: the
  table sits in §8, the append in §10, and the last line of the report is the contract's.
SOURCE: contract :126-131; `scripts/tierc11_close.py:24-45` (the generator's output law), `:2507-2514` (the cap);
`x_rec/tierc11x/LEANS_X.md:2361-2405` (LX-C.1), `x_rec/tierc11x/LEANS_X_AMENDMENTS.md:593-606` (AM-X28);
`exchange/status/CONVENTIONS.md:13`, `:324`, `:342`; `exchange/README.md:21`; `exchange/reports/README.md:6`;
`exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:21-22` (LAW 5); `scout/U9_process_close_fixtures.md` §1.8, U9-19.
RIVALS: the contract's eight parts only — drops sections two standing rules require. Per-instant tables inlined
(TC11's report grew past the wire many times over). A whole-or-pointed choice made per table at render — a choice
made after the verdicts are known.
FAILS-IF: F-S0-FIVE is RED when §0.1's rows are not `S0_VERDICTS.md`'s byte for byte, not the filing's
registrations in filing order, a word disagrees with `FAMILY.json`, a label is absent, or P-SCALP-3's
fill-sensitivity row is absent; F-FORM is RED
when a named part is missing or out of order or the last line is not the contract's; planted mutations: a label
stripped from one §0 cell; §1 and §2 swapped; a line added after the final line.

**L-X.29 THE NUMBER-TRACING LAW AND THE VERDICT-WORD LAW** — "no number typed that a file can supply" (:8); "§0
VERDICTS FIRST" (:126)
READING:
- A number enters the report or the append in exactly one of four ways: (1) `T(key, spec, fmt)` — resolved from
  its record (`spec.kind` ∈ json · parquet · text · git · ast · filesha, with path and selector), formatted by a
  named format, and filed in `close/TRACES.json` with its uses per region; (2) a VERBATIM block behind `<!--
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
  P-SCALP-3 is the one such block outside §0), (iii) §10's fence, whose bytes equal the staged append, (iv) a
  verified verbatim block or cite quote of a pinned source.
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
progress record's `blockers` and `notes`; `LEANS_AMENDMENTS.md` and `AMENDMENTS_PROPOSED.md`; the review and judge
records' items carried to close; every fixture transcript's findings; the ferry's HELD FOR ATHENA list; every
OBJECTION and OPEN TO OPERATOR item of the frozen LEANS; the frozen-estate shas re-asserted against
`progress/TC12-R0.json` (a moved sha is a finding against TC12). The md is rendered from the json.
SOURCE: `research_outputs/tierc11/close/S5_FINDINGS_NOT_FIXED.json` (schema `tierc11.close.S5_FINDINGS_NOT_FIXED.v1`,
per `scout/U9` §1.8); `x_rec/scripts/tc11x_close_findings.py:2-46`; `x_rec/tierc11x/LEANS_X.md:2407-2410`.
RIVALS: a free-text section — no owner, no locator, no dedup.
FAILS-IF: F-FNF is RED when the md is not the json, a finding lacks a field, an id repeats, a harvested text does
not re-extract from its locator, or an executor-owned finding outranks an operator-owned one; planted mutations: a
harvested text edited; a blocker left unharvested.

**L-X.31 BOX-COST: WHAT IS MEASURED** — "BOX-COST" (:129)
READING: `close/BOX_COST.{json,md}` measures, with git read-only verbs and `os.lstat`, never a fetch:
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
FAILS-IF: F-BOXCOST is RED when the table differs from a re-derivation, a file over the wire is not FLAGGED, the
projection does not re-derive, or the md is not the json; planted mutations: a constant typed in the generator; a
row dropped; a FLAG removed.

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
     #rows[registration=<id>].verdict_cell»` — the cell carries the label; P-SCALP-3 also its fill-sensitivity row;
     a CLOSED BY PRECONDITION cell stays number-free;
  5. X's standing pre_seen line, and the licence sentence of O-16 (d);
  6. the rulings enacted (`:12-16`) and what was done under each; the forward ledger's fourth book and the appended
     rows, unscored; the ferry;
  7. INTEGRITY (the fixture roll, F-CTRL, text-before-result, the review attestations); OPEN FOR THE OPERATOR; and
     THE TIER LINE, citing X's landed block.
- Every digit of the prose is traced, cited or masked (L-X.29). Exactly three single-line `⟦STAMP AT CLOSE — …⟧`
  brackets, filled by step 5 of the acts: the commit count and remote state; the ferry of record's WRITTEN / HELD
  FOR ATHENA / FLAGGED counts; the tc11-stamp's result.
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
FAILS-IF: F-LEDGER-FMT is RED when the format law fails, a cite does not verify, a required item is absent, the
stamp count is not three, or §10 of the draft is not the append byte for byte; planted mutations: the final line
written inside the block; the LANE line removed; one quoted character changed; the "maker" cite dropped.

**L-X.33 CLOSE ACTS: THE STEP LIST** — "Q6 the close acts remain the operator's keystrokes" (:14-15);
"publish_exchange; STATE push; bright paths; final line" (:130)
READING: the generator writes `research_outputs/tierc12/close/close_acts.sh` (tracked; `set -euo pipefail`; no
force, no reset, no stash, no clean). The executor never runs it, never pushes, never calls `publish()`, never
merges, never moves a report onto the bus and never appends to the ledger (O-12). `--check` runs step 0 only.
- **Step 0 · refusals — nothing changes, each prints its reason:**
  a. the main tree, on `v12-v1-census`; the index clean;
  b. **the three prior blocks landed BY BYTES, in order:** for TC10, TC11 and X, the append committed at `HEAD`
     carries no pending stamp and its committed bytes occur exactly once in the committed
     `exchange/status/LEDGER_APOLLO.md`, at offsets TC10 < TC11 < X; the ledger's working copy equals `HEAD`; no
     `TIER-C12 · ` header is in it yet. A header grep is never used (X's header reads `TIER-C11 · TC11-X`);
  c. the three predecessors' reports are tracked under `exchange/reports/`;
  d. **SOURCES == HEAD:** every TC12 close source is present, tracked and identical to `HEAD`; the list is
     generated (the draft, the append, the `close/` files, `scores/*`, `registrations/*`, the ferry's staged
     manifest, `LEANS.md`, `LEANS_AMENDMENTS.md`, `PROGRESS.json`, the close, ferry and stamp scripts);
  e. the destination report and `exchange/rows/tierc12/` are absent; the draft has no open placeholder; the three
     stamps and the report's push stamp are pending;
  f. both contracts are as pinned: TC12's prefix with an empty tail (L-X.16); TC11's first `bytes` hashing to the
     sha `progress/TC12-R0.json` filed, with no `BUILT` line; `research_outputs/tierc11/scores/SCORES.json` at its
     R0 sha (Q1);
  g. ATTEST-ORDER (L-X.21) and `F-LEDGER-FMT --check` on the pre-stamp append as the sources stand now.
- **Step 1 ·** `git push origin v12-v1-census`, then `origin` verified equal to `HEAD`. On failure STOP: nothing
  has changed.
- **Step 2 · the ferry of record** (O-24; L-L's law): pinned at the then-`HEAD` by sha, the box measured with the
  three closes inside it, only TC12's own close adds reserved; the WRITTEN set copied sha-equal from the off-bus
  staging into `exchange/rows/tierc12/`, the rest listed HELD FOR ATHENA; then its FRESH leg and F-ROWS. On failure
  the files it wrote are moved aside (nothing deleted) and the script STOPS.
- **Step 3 · LAW 5:** the draft copied to `exchange/reports/BUILD_2026-10-08_TIERC12_VALUE_AREA.md`, sha equal
  across the copy; `git rm` of the draft committed alone as `tierc12(CLOSE): LAW 5 — …`.
- **Step 4 · the two BUILT stamps:** the tc11-stamp (L-X.34), then TC12's own (L-X.35).
- **Step 5 ·** every `⟦STAMP AT CLOSE⟧` filled from git and the ferry manifest, then `F-LEDGER-FMT --stamped`.
- **Step 6 ·** `cat` the append onto the ledger; the ledger's tail checked equal to the append byte for byte.
- **Step 7 ·** the non-exchange residue staged by explicit path with `git add -f` and committed in the same
  command sequence, `tierc12(CLOSE): …`. No exchange path is ever staged by the script (CONVENTIONS :415).
- **Step 8 ·** `publish()` by the invocation of record (CONVENTIONS §3.4), and the push result STATED.
- **Step 9 ·** bright paths, then the final line.
Every commit subject starts `tierc12(`; none starts `tierc10`, `tierc11(` or `tc11x(`, which feed the other
tiers' stamp counts.
**The scratch proof of the script (F-CLOSE-SCRIPT):** `bash -n`; a static law (the push only at step 1, `publish()`
only at step 8 and only by the invocation of record, the final line last and nowhere else); step 0 of a scratch
copy run with `--check` against scratch repositories; steps 1-7 run in a sandbox clone against a local bare
origin, cut before `publish()`; and the real repository's `HEAD`, index and porcelain equal before and after. The
sandbox leg runs a SCRATCH COPY (never the generated file) with every path outside both trees; it is TC11's
F-CLOSE-ORDER form and performs no operator act. L-0.26 words the acts' executions more narrowly (`bash -n` and
step 0 only); the difference is listed under INTERFACE ASSUMPTIONS for the reviser.
SOURCE: `research_outputs/tierc11/close/close_acts.sh` (sha `7f601f81…e2ba`; step 0 `:47-67`, LAW 5 `:75-89`, the
stamp `:91-109`, the residue `:117-122`); `x_rec/tierc11x/close/close_acts.sh` (sha `02191457…1940`; by-bytes tier
check `:142-180`, the ferry `:198-253`, the tail check `:295-303`, `git add -f` `:307`);
`exchange/status/CONVENTIONS.md:399`, `:413`, `:415`, `:419`; `scripts/tierc11_close_fixtures.py:34-41`
(F-CLOSE-ORDER); `x_rec/scripts/tc11x_close_fixtures.py:40-48` (F-CLOSE-SCRIPT); O-10, O-12, O-24;
`scout/U1_rulings_close_state.md` §1.7, R-17, H-8; `scout/U9_process_close_fixtures.md` U9-21.
RIVALS: a CERTIFIED_TIP pin (X) — meaningful only on a branch of its own; the main branch moves every day. Header
greps for tier order (TC11) — cannot tell TC11 from TC11-X.
FAILS-IF: F-CLOSE-SCRIPT is RED when a planted gate does not STOP at step 0 before any push — today's ledger (the
three blocks absent); TC11's block before TC10's; a block with a pending stamp; a dirty index; a source differing
from `HEAD`; the destination present; TC11's contract already stamped; `SCORES.json` moved — or when the sandbox
run does not push, ferry, move sha-equal, stamp, append and commit in that order, or the real repository changes.
Planted mutations of the script itself: the by-bytes check replaced by a header grep; `publish()` moved ahead of
the append; the final line printed twice.

**L-X.34 THE TC11-STAMP, AND ITS SCRATCH-CLONE PROOF** — "stamp TC11 BUILT and re-pin its registry files
["tc11-stamp"]" (:13)
READING: under O-10 — a close act, the line appended last, the cascade proven GREEN in a scratch clone. The LAW of
the stamp (where the line goes, which bytes move, what stays historical, what GREEN means) is L-0.24's; this
reading fixes how CLOSE and the acts HOST it, and restates the law only as far as the host needs it.
- **The line.** `BUILT: exchange/reports/BUILD_2026-09-24_TIERC11_EVENTS.md · <the commits whose subject starts
  tierc11(, read from git at the act>`, appended as the last line of `exchange/queue/2026-09-24_TC11_APOLLO.md`, the
  file required to end in `\n` first. Lines 1-103 stay byte-identical, so TC11's nine text slices, nine payload
  shas and its chain head (`research_outputs/tierc11/registrations/REGISTRY_PIN.json["head"]`) do not move; only
  the whole-file sha does. **Because the commit range is read at the act** (TC11's own close adds `tierc11(`
  commits), the stamped file's sha is known only then: a build-time proof proves the mechanism, and the act must
  re-prove on the very bytes it will write.
- **The re-pin** is a replacement of pinned shas, old → new, to a fixed point, inside an ALLOWED set and nowhere
  else — L-0.24's sets (a)-(f): the contract; `research_outputs/tierc11/registrations/{REGISTRATIONS.json,
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
- **Two phases, both in `scripts/tierc12_tc11_stamp.py`:**
  - `--prove`: a fresh `git clone --local` of the main tree at `HEAD` into a scratch directory outside both trees;
    TC11's ignored parquet staged into it by copy (the globs of TC11's attest tool); the line appended; the
    replacement run to its fixed point; TC11's scorer and the suites of TC11's last sweep run THERE, under TC11's
    snapshot read-only. GREEN iff every suite is GREEN with byte-identical transcripts on a second run, the changed
    set ⊆ ALLOWED, the three NEVER-moved score files are byte-identical, and TC11's chain head is unchanged. It
    writes a transcript and a map {old → new sha per moved file; each moved file's sha before and after; the
    historical list}.
  - `--apply`: only after a GREEN `--prove` at the same `HEAD`; asserts each pre-image in the main tree equals the
    clone's pre-image, then copies the proven post-images byte for byte. No TC11 code runs in the main tree.
- **When.** At TC12-CLOSE the executor runs `--prove` once and files `close/TC11_STAMP_PROOF.txt` and
  `close/TC11_STAMP_MAP.json`. **If that build-time proof is not GREEN, the generated `close_acts.sh` carries no
  stamp step at all**, the map is filed `applied: false`, and the ruling returns to the operator (L-0.24). If it is
  GREEN, step 4 of the acts (after the three blocks have landed) runs `--prove` again at the then-`HEAD`, then
  `--apply`; the non-exchange paths are committed as `tierc12(CLOSE): tc11-stamp — …`, and the contract itself is
  left for `publish()`.
  The proof costs one roll of TC11's suites each time (their per-suite walls are on file in
  `research_outputs/tierc11/PROGRESS.json stages[].fixtures[].wall_seconds`); the acts print that before starting it.
- **If the act-time `--prove` is RED** nothing is applied — no partial re-pin is ever written — the acts continue,
  and the append's third stamp reads `tc11-stamp NOT APPLIED — proof RED` with the transcript's path (see OPEN TO
  OPERATOR).
- TC11's close generator and its fixtures stand outside the cascade: that generator refuses a contract that
  carries a `BUILT` line, and its HALT in the clone is printed as EXPECTED (L-0.24).
SOURCE: L-0.24; O-10; contract :13; `research_outputs/tierc11/BUILD_DRAFT.md:5943-5945`, `:5989` (Q1, Q2,
FN-M-QUEUE-STAMP); `scripts/tierc11_registrations.py:24`, `:186-188`, `:244-245`; `scripts/tierc11_score.py:220-226`,
`:418-446`; `scripts/tierc11_worktree_attest.py:65`, `:113` (the staging globs); `exchange/queue/README.md:8-12`;
`scout/U1_rulings_close_state.md` §1.4-§1.6, R-1 … R-5, H-7; `scout/U9_process_close_fixtures.md` C5, U9-8, H10.
RIVALS: stamp under RATIFIED, where every earlier queue stamp sits — shifts every line TC11's registry cites. Q2's
three files alone — TC11's verifier then HALTs on its typed constants. Run TC11's scorer `--refile` in the main
tree — executes frozen code in place.
UNVERIFIED: (i) that TC11's scorer, re-run after the replacement, leaves `SCORES.json`, `FAMILY.json` and
`BASE_IDENT.json` byte-identical — asserted inside `--prove`, a HALT otherwise; (ii) that the suites of TC11's last
sweep re-pass in a clone with the staged parquet — the proof's own subject; (iii) the full ALLOWED closure
(which transcripts and manifests print a moved sha) — enumerated by `--prove`, and anything outside ALLOWED is RED.
None of the three was run while drafting (no TC11 module may be executed here).
FAILS-IF: F-TC11-STAMP is RED when, in the scratch clone, TC11's chain head moves, a NEVER-moved file changes, the
changed set leaves ALLOWED, a suite is RED, or `--apply` runs without a GREEN proof at the same `HEAD`; planted
mutations: the line inserted at line 5; a replacement applied to `SCORES.json`; `--apply` against a tree whose
pre-image differs by one byte.

**L-X.35 TC12's OWN BUILT STAMP** — "STEP Q: file this paste verbatim" (:10)
READING: at step 4 the acts append `BUILT: exchange/reports/BUILD_2026-10-08_TIERC12_VALUE_AREA.md · <the first and
last tierc12( commits and their count, read from git> · <the fixture roll's tally>` as the last line of TC12's
contract. L-X.16's prefix pin makes this free: no slice, sha or head moves, and the question TC11's contract left
open is not asked of TC12. The line reaches the record through `publish()`.
SOURCE: `exchange/queue/README.md:8-12`; `research_outputs/tierc11/BUILD_DRAFT.md:5945` (FN-M-QUEUE-STAMP);
`scout/U1_rulings_close_state.md` §1.6, R-18.
RIVALS: leave it unstamped — the queue counts it as ratified-unbuilt and the finding recurs.
FAILS-IF: F-CONTRACT-PIN (L-X.16), positive leg.

**L-X.36 "publish_exchange", "STATE push", "bright paths", THE FINAL LINE** — "publish_exchange; STATE push; bright
paths; final line: "Operator: click Sync now."" (:130-131)
READING:
- **publish_exchange** = `publish(repo, date)` of `scripts/publish_exchange.py`, called only by the acts at step 8,
  only through the invocation written out in CONVENTIONS §3.4; it stages `exchange/**`, guard-checks the whole
  index, commits `exchange: auto-publish <date>` and pushes the branch.
- **STATE push** = the push result stated plainly, never a push by the executor: the acts print `PUSH RESULT:
  SUCCEEDED — …` or `PUSH RESULT: FAILED — …` after step 1 and after step 8, and the report's §11 carries a
  `⟦STAMP AT CLOSE⟧` filled with step 1's result. The report also states that the daily routine pushes the whole
  branch whenever the route works, so "no push without the operator's word" cannot be enforced in the main tree —
  a finding, not hidden.
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
FAILS-IF: F-CLOSE-SCRIPT (static leg) and F-FORM (L-X.28); planted mutation: the final line moved inside the append
(F-LEDGER-FMT must turn RED as well).

---------------------------------------------------------------------------------------------------------------
### FIXTURES DEFINED BY THIS SECTION

Harness: L-0's `scripts/tierc12_fx.py` (`prove`: the BREAK leg first, and a break that does not go RED voids the
fixture; `plants`: one at a time, CAUGHT only when a finding names the intended detector; a crash is a fixture
defect). F-DET, F-KEY, F-GRID and F-COLLAR are L-0's laws (L-0.20, L-0.21, L-0.15, L-0.16); the rows below naming
them are this section's INSTANCES on the scorer's and the close's directories. F-TC11-STAMP's legs are L-0.24's and
are hosted by the close suite. Suites and transcripts:
`scripts/tierc12_registrations_fixtures.py` → `registrations/FIXTURES_REG.txt`; `scripts/tierc12_score_fixtures.py`
→ `scores/FIXTURES_SCORE.txt`; `scripts/tierc12_close_fixtures.py` → `close/FIXTURES_CLOSE.txt`.

| fixture | FAILS IF | planted mutation that must turn it RED |
|---|---|---|
| F-FAM (PARSE · REAL · PLANTED) | a header's bar ≠ q ÷ m; a family's count ≠ m; a row's bar is not its family's; tests spent ≠ BUILT un-halted rows; a closed row carries a number, an arm or a spent test | L-X.15's five |
| F-CONTRACT-PIN | an appended `BUILT:` line moves a slice, payload sha, head or finding; a prefix byte or a foreign tail line passes | L-X.16's three |
| F-REG (SLICE · HASH · WRITE-ONCE · TEMPLATE · SPEC-VERBATIM) | any detector of L-X.22 is silent on its plant, or the independent re-derivation disagrees with the filing | L-X.17 … L-X.22's plants |
| F-ATTEST-ORDER | a TC12 book path was first added at or before the registration commit, or outside its descendants; a STATUS lacks the head; a non-PRE_REG file existed at filing | L-X.21's three |
| F-BOOT | persisted draws ≠ the fixture's own loop; `lo`, `hi`, `p` re-derived from `draw_hex` differ; `p_den ≠ N_BOOT + 1` on a row of record | L-X.3, L-X.6, L-X.7's plants |
| F-VERDICT (CASES · IMPLIED · LADDER · SIZE) | a typed case maps to another word; the binding clause per family is not the enumerated one; a ladder combination maps off L-X.9's table | L-X.8, L-X.9's plants |
| F-SCORE-ANCHOR | the mirrored rulers, LOAO and concentration do not reproduce TC11's filed leaves on TC11's filed arms at TC11's seed (integers equal, floats equal as `float.hex`) | L-X.4, L-X.5, L-X.11, L-X.12's plants |
| F-SCORE-INPUTS | a row is scored with a pinned input changed | L-X.23's three |
| F-REGBOOK | a plant on the regbook interface's row-level laws is not caught by its named detector | L-X.24's list |
| F-BASE-IDENT | a base arm's canonical sha ≠ TC11's filed value; a gate holds a foreign key or an altered kept row | L-X.25's four |
| F-COLLAR · F-GRID | a beside leaf lacks the collar or carries a verdict word; rows, families or beside leaves are not the declared sets | L-X.14, L-X.26's plants |
| F-EXIT · F-DET | a record is clobbered without a logged `--refile`; a flag is masked; two runs differ in a byte | L-X.27's plants |
| F-S0-FIVE · F-FORM | §0.1 is not `S0_VERDICTS.md`'s five rows; a named part is missing or out of order; the last line is not the contract's | L-X.28's three |
| F-NUM · F-WORDS | an untraced digit; a trace that does not re-derive; a verdict word outside its four regions | L-X.29's three |
| F-FNF · F-BOXCOST | L-X.30's and L-X.31's conditions | their plants |
| F-LEDGER-FMT | the format law, a cite, a required item or the stamp count fails; §10 ≠ the append | L-X.32's four |
| F-CLOSE-SCRIPT | a planted gate does not STOP at step 0; the sandbox order is wrong; the real repository changes | L-X.33's lists |
| F-TC11-STAMP | TC11's head moves; a NEVER-moved file changes; the changed set leaves ALLOWED; `--apply` without a GREEN proof | L-X.34's three |

---------------------------------------------------------------------------------------------------------------
### REGISTRATION SPEC · (none owned by L-X)

L-X owns no registered row. The five blocks are L-G's (P-ADM-1, P-BRD-1), L-R's (P-DIR-1, P-SFP-VA-1) and L-S's
(P-SCALP-3). Each block's `family`, `family_m`, `family_bar`, `statistic`, `comparison`, `verdict_rule` and `labels`
fields carry the common clauses below, and the filing HALTs where a block's text and these clauses disagree
(detectors FAMILY-BAR, RULER-TEXT, TEMPLATE).

| seq | id | family (header) | m · bar | text | comparison | era of record (inside the scored window, O-9) | arms the scorer rules | label keys |
|---:|---|---|---|---|---|---|---|---|
| 1 | P-ADM-1 | ADMISSION (:52) | 2 · 0.05 | :53-56 | two-sample vs v6 | full corridor (no era named; TC11 L-1.3) | `scored`, `base` | `pre_seen` |
| 2 | P-BRD-1 | ADMISSION (:52) | 2 · 0.05 | :57-59 | two-sample vs v6 | full corridor | `scored`, `base` | `selection_hazard` (DIRECTION-INFORMED) + D-1 |
| 3 | P-DIR-1 | RANGE-STATE (:64) | 2 · 0.05 | :65-68 | two-sample vs v6 | full corridor | `scored`, `base` | `selection_hazard` (DIRECTION-INFORMED) |
| 4 | P-SFP-VA-1 | RANGE-STATE (:64) | 2 · 0.05 | :69-75 | vs zero | full corridor (:69) | `scored` | `pre_seen` |
| 5 | P-SCALP-3 | SCALPER (:82) | 1 · 0.10 | :83-106 | vs zero | holdout (:83) | `scored` (TICK), `ladder__touch`, `ladder__deep` | `pre_seen` |

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
  strip unscored. Tier-E arms carry no verdict word." — followed by exactly one `prints '<verdict> …'` template
  per L-X.13. The filing asserts the rule states the parsed q, m and bar, `N_BOOT`, both seeds and the template.
- **verdict_rule, P-SCALP-3 only, added:** L-X.9's six-case table verbatim, the definition of `C(X)` and `D`, "one
  test is spent; TOUCH and DEEP can never produce SUPPORTED", and the bar cell of L-X.8.
- **disclosed_beside, common set:** L-X.14's slugs, each Tier-E, no verdict word; owners append their own arms.
- **failure_conditions, common:** F-REGBOOK, F-KEY (L-0.21, on the regbook directory), F-BOOT, F-VERDICT,
  F-SCORE-ANCHOR, F-GRID, F-DET, and for gates F-BASE-IDENT; owners append theirs (F-GATE, F-BRD, F-DIR, F-SFP,
  F-SCALP, F-TOLL).

### OPEN TO OPERATOR

1. **The single-trade share has no threshold** in the contract (:106) or on any file, and the executor may not type
   one. Default if silent: none; both shares are printed in every row and in P-SCALP-3's verdict text and decide
   no word. LOAO alone carries the one-asset reading on P-SCALP-3, as a kill (L-X.9, L-X.11); naming rival (ii) of
   L-X.9 overrules that.
2. **The push route.** Step 1 of the acts is a push, and the SSH route has failed on every daily run since
   2026-09-27 (`exchange/status/daily/DAILY_2026-10-08.md:123`). Default: the acts STOP at step 1 with nothing
   changed until the route works.
3. **A tc11-stamp proof that is not GREEN.** Default, at build time: the acts carry no stamp step and the ruling
   returns to the operator (L-0.24). Default, at the act: nothing is applied, TC12's close continues, the append
   says so with the transcript's path, and the item is an operator-owned finding. Vetoing `"tc11-stamp"` by name
   removes step 4's first half altogether.
4. **X's frozen records name TC11's old shas for good** once the stamp lands (thirty tracked X records,
   `scout/U1_rulings_close_state.md` §1.4). Default: listed as HISTORICAL in the stamp map, none edited.
5. **The box.** After the three pending closes the forecast leaves the box within a few KB of WARN, so TC12's
   report alone crosses it; `publish()` prints the warning and still publishes. Default: published under WARN,
   REFUSE never overridden, every held file listed for ATHENA.
6. **A report over the per-file cap.** Default: the generator HALTs and the operator names what is pointed
   instead of printed; the executor does not choose after the verdicts are known.

### INTERFACE ASSUMPTIONS

- **L-0 (laws, process):** the stage order of L-0.10 (TC12-REG directly after TC12-LEANS and before TC12-D;
  L-X.21's PRE_REG is read from the progress records of the stages before it; L-0.10's T1 and L-X.21's clause 3
  are one test and are reconciled to one fixture by the reviser); the stage ids and their `progress/<STAGE>.json`
  records; `PROGRESS.json["amendments_of_record"]`; the amendment law (never from an outcome); the harness
  `scripts/tierc12_fx.py`; the pin door `scripts/tierc12_pins.py` and its map (L-0.17), which holds L-X.1's two
  regexes, the seed row and the `LOAO (\d+)/(\d+)` row; the prefix pin (L-0.1); F-DET, F-KEY, F-GRID, F-COLLAR and
  the collar helper; the freeze of `LEANS.md` by sha and the review record's path; the canonical markup of a
  REGISTRATION SPEC block (fifteen `- **<field>:**` bullets, L-X.18).
  **Three differences for the reviser to rule:** (i) L-0.26's F-NOT (ACTS leg) forbids any TC12 source holding a
  shell string whose git subcommand is `push`, an `import publish_exchange` or a call named `publish` — the close
  generator's TEMPLATE of `close_acts.sh` necessarily holds all three as text and needs a named exemption; (ii)
  L-0.26 limits executions of the acts to `bash -n` and step 0, while L-X.33's F-CLOSE-SCRIPT also runs steps 1-7
  of a scratch copy against a local bare origin (if L-0.26 stands, that leg is dropped and the order is held by the
  static law alone); (iii) L-0.16 limits the registered marker to score documents and §0, while L-X.28's §4
  re-quotes P-SCALP-3's verdict text under it.
- **L-D (substrate, env):** the env shim `E` (`scripts/tierc12_env.py`) exposing `E.T5`, `E.TP`, `E.era_of`, the
  home panel, `E.PIN_MS`, `E.TC11_PIN_MS`, the era cut, and `E.fees()` with `taker_bps_side`, `slippage_bps_side`,
  `maker_bps_side` per stem; `data/AS_OF_PIN.json`, `data/fee_schedule.json`, `STAGE_D_MANIFEST.json` certified by
  `progress/TC12-D.json`; write-protection of the frozen estate. The registry is filed before `E` exists, so the
  filer imports no env and reads only the files L-X.3 and L-X.19 name.
- **L-V (value area):** `va/VA_MIRROR.json` (the record each range row's precondition item reads, certified by
  `progress/TC12-V.json`); the files §0.3, §2 and §3 of the report quote; the dated V2-versus-X amendment.
- **L-C (control):** the v6 book the three `base` arms copy, bit-equal to TC11's on the sixteen columns; the strip.
- **L-G (admission):** the REGISTRATION SPECs of P-ADM-1 and P-BRD-1 incl. their label texts and `external_context`;
  the refused sets and F-GATE / F-BRD; the shadow arms.
- **L-R (range-state):** the specs of P-DIR-1 and P-SFP-VA-1; the with-vs-against table §0.2 quotes;
  `exit_reason = "corridor_end"` on positions open at the scored window's end.
- **L-S (scalper):** the spec of P-SCALP-3 carrying L-X.9's table verbatim (if L-S drafted LOAO as a qualifier
  only, the two differ and the reviser rules before freeze; L-X's is the stricter); `scored` = the TICK book,
  `ladder__touch`, `ladder__deep`, `tierE__full_corridor`; the four fee columns per leg; what CLOSED and CLOSED FOR
  GOOD forbid afterwards.
- **L-L (ledger, era, ferry):** the four-book record §0.4 quotes; `scripts/tierc12_ferry.py` with a forecast mode
  (off-bus staging) and an of-record mode pinned by sha for step 2; the frozen priority order of the held set;
  F-LEDGER and F-ROWS.

### OBJECTIONS

None against a ruling. O-1 … O-24 were checked against the files this section cites and no ruling was found wrong
on a fact. Two places where this section adds to a ruling without contradicting it are stated in the readings:
L-X.7's clause (c) answers what O-22's law does when a draw leaves an arm empty, and L-X.9 layers the contract's
pre-named kill (:104-106) over O-22's verdict law for P-SCALP-3 alone.

A correction that is not against a ruling: this unit's brief cites CLOSE as "contract lines 121-129". On the filed
bytes (sha `861d6050…`) CLOSE is lines 126-131 (slice sha `5f964a17…9737`) and lines 114-124 are FIXTURES; every
cite in this section uses the verified map of L-X.17.
