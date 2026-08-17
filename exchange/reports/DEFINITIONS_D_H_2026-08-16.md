# DEFINITIONS — THE D-BLOCK AND THE INTERVIEW HOOKS · 2026-08-16

**Lane** APOLLO · **Branch** `v12-v1-census` · **Drafted** APOLLO · **Executor** HEPHAESTUS
**RATIFIED** operator 2026-08-16, as STEP 0 of the TIER-C6 rev B commission.

**CLASS — definitional.** This document scores nothing and measures nothing. It maps every label
`D1`–`D15` and `H1`–`H7` to its source in the estate, or records that it has none.

---

## 0 · WHY THIS DOCUMENT EXISTS, AND WHAT IT IS ALLOWED TO DO

**F-C5-h, verbatim** (`BUILD_2026-08-16_TIERC5_FULLWATER.md:319`):

> **F-C5-h · THE INTERVIEW'S D-BLOCK AND HOOKS H3, H6 HAVE NO SOURCE.** §7. **Ruling needed: define D1–D15 and H1–H7 in the estate, or strike the labels and cite the pastes directly.** Precedent V-6, same sentence, same shape.

The commission's STEP 0 asks for *"every D1-D15 and H1-H7 mapped to its source (interview doc §, operator reply, deciding table)"*.

**THE MAPPING IS MOSTLY A MAP OF ABSENCES, AND THAT IS THE FINDING.** A repo-wide search returns **no source of any kind for 11 of the 15 D-items and 2 of the 7 H-items.** This document does not manufacture one. Where a label has no anchor it says **NONE**, because the alternative — quietly attaching a plausible definition to an unanchored label — is precisely the failure F-C5-h was raised to prevent.

**AND THE NEAR-MISSES ARE THE DANGEROUS PART.** `D1` through `D10` *do* return hits — in **four other contracts' deliverable namespaces**. `S3_Enrichment_Builder_Contract.md:49` has a D1 ("the per-trade anatomy table"). `Census_1_MTF_Signal_Stack_Builder_Contract.md:83` has a different D1 ("the cascade map"). `TC1_RESULTS.md:5` cites "s2b D1". `V3_Recompute_R1_R10_Builder_Contract.md:6` has a fourth. **A definitions document that mapped "D1" without saying whose D1 would manufacture exactly the false anchor this document exists to remove.** Every such collision is listed and dismissed by name below.

> ⚠ **TWO ATTACHED DOCUMENTS WERE NAMED IN THE COMMISSION AND DID NOT ARRIVE.** STEP 0 reads *"file the two attached documents (shas printed)"*. No documents accompanied the commission text, and a search of the estate confirms neither is already filed. **That sub-step is the one deliverable of this build that is not complete**, and it is recorded here rather than quietly dropped. Everything below is built from what the estate actually holds plus the rulings stated in the commission itself.

---

## 1 · THE D-BLOCK — D1 … D15

**The only place `D1–D15` appears as a block** is `exchange/reports/APOLLO_LANE_STATUS_2026-08-15.md:37-41`:

> *"plus the fuzz set and **D1–D15 of the scoped interview (identity/admission/lifecycle/measurement blocks).**"*

and `:66`: *"The work: (1) run the SSv12 precision interview **(D1–D15)**; …"*

**It names four block titles and a count. It defines not one item.**

| item | source in the estate | status |
|---|---|---|
| **D1** | — | **NONE.** Collides with four unrelated namespaces: `S3_Enrichment_Builder_Contract.md:49`, `Census_1_MTF_Signal_Stack_Builder_Contract.md:83`, `TC1_RESULTS.md:5`, `V3_Recompute_R1_R10_Builder_Contract.md:6` |
| **D2** | — | **NONE.** Collides: `S3_Enrichment…:50`, `Census_1…:84` |
| **D3** | — | **NONE.** Collides: `S3…:51`, `Census_1…:85`, `REVIEWER_HANDOFF_2026-07-15_V3_RECOMPUTE.md:183` |
| **D4** | — | **NONE.** Collides: `S3…:52`, `Census_1…:86`, `CENSUS_DEFINITIONS.md:48` |
| **D5** | — | **NONE.** Collides: `S3…:53`, `Census_1…:87` |
| **D6** | — | **NONE.** Collides: `S3…:54`, `Census_1…:88`, `CENSUS_DEFINITIONS.md:23` |
| **D7** | — | **NONE.** Collides: `Census_1…:89` |
| **D8** | — | **NONE.** Collides: `Census_1_Amendment_1.md:16`, `CENSUS_DEFINITIONS.md:70` |
| **D9** | — | **NONE.** Collides: `Census_1_Amendment_1.md:18-20`, `CENSUS_DEFINITIONS.md:80` |
| **D10** | — | **NONE.** Collides: `Census_1_Amendment_1.md:22`, `CENSUS_DEFINITIONS.md:98` |
| **D11** | — | **NONE. Zero hits repo-wide, in any namespace.** |
| **D12** | `scripts/tierc5_rules.py:160-169`, `REGISTER_DIFF["FUNDING_CEILING_R"]` = 1.0 | **ENACTMENT, NOT DEFINITION.** The row's own source line reads *"D12, enacted by the 2026-08-16 paste"* — and that paste is **not filed anywhere in the estate.** The *rule* is fully specified in code; the *label* is not anchored |
| **D13** | `scripts/tierc5_rules.py:261` — *"LEAD-IN [D13(c)]: lead-in armings are COUNTED, never SCORED. Both books printed."* | **ONLY sub-item (c) has content.** D13(a) and D13(b): **NONE** |
| **D14** | — | **NONE. Zero hits repo-wide, in any namespace.** |
| **D15** | *ruling:* `scripts/tierc5_rules.py:143-147`, `THE_RULING`, operator verbatim — *"D15 caveats not hard gates"*. *content:* `scripts/tierc5.py:579-593`, the `d15()` docstring | **THE ONLY FULLY ANCHORED D-ITEM.** Both a filed operator ruling and filed content |

### D15, quoted in full — because it is the one that survives

The four columns, defined at `scripts/tierc5.py:579-593` and nowhere else in the estate:

- **`paired_delta_expectancy_r`** — mean over PAIRED campaigns (same asset + entry bar) of cell − base
- **`tail_exit_ratio`** — cell top-decile winning mass ÷ base's
- **`max_single_trade_delta_share`** — the largest |per-campaign Δ| as a share of |Σ Δ|
- **`provisional`** — n < `PROVISIONAL_MIN_N` on this line (30, pinned before the look at `tierc5_rules.py:212-220`, and named there as *"a convention, not a test"*)

**The ruling demoted them from gates to diagnostics.** They ride every scored and shadow line in TIER-C5 and TIER-C6 and they gate nothing.

---

## 2 · THE INTERVIEW HOOKS — H1 … H7

**The only place in the estate that maps an H-label to content** is `BUILD_2026-08-16_TIERC5_FULLWATER.md:288-295`, a relay table headed *"| hook | what the paste names it | table |"*. Every H-item below is therefore **defined by relay, not by a filed source** — except the two that are not defined at all.

| item | source | status as of this document |
|---|---|---|
| **H1** harvest-vs-ride | `BUILD…TIERC5…:290`; enacted `scripts/tierc5.py:767` (`harvest_lab`) | **DEFINED BY RELAY · ANSWERED.** The harvest is a de-risk, never a profit-take: +5.7383 R, positive in every slice, 32 of 37 fills helped, and *both* the taken half and the would-have half are negative |
| **H2** resistance / walls | `BUILD…TIERC5…:291`; enacted `resistance_league` | **DEFINED BY RELAY · ANSWERED, AND EXTENDED THIS BUILD.** TIER-C6 Stage W adds the **support** side, so the league is now two-sided and a short is scored against the wall in front of it rather than the one behind it |
| **H3** | — | **WAS: NONE.** `BUILD…TIERC5…:292` reads literally *"H3 \| NOT DEFINED ANYWHERE \| —"* |
| **H4** the trail lab | `BUILD…TIERC5…:293` (shares a row with H5) | **DEFINED BY RELAY · MEASURED, NOT ANSWERED.** The S-TRAIL cells are on the table; the +0.25-buffer cell fails its own D15 column |
| **H5** the trail lab | as H4, same row | **DEFINED BY RELAY · ANSWERED AND CARDED THIS BUILD.** "The trail arms after +1R" is card v6's headline diff |
| **H6** | — | **WAS: NONE.** `BUILD…TIERC5…:294` |
| **H7** resistance / walls | `BUILD…TIERC5…:295` — *"as H2"* | **DEFINED ONLY AS AN ALIAS OF H2.** No independent content anywhere in the estate |

### H3 and H6 — DEFINED THIS TURN, BY OPERATOR RULING

The commission of 2026-08-16 supplies the content that did not exist, and this document files it so the labels stop being unanchored:

**H3 — THE HARVEST FRACTION.** *Ruled: **50%**.* The de-risk takes half the unit at the band touch and the remainder rides. The alternatives are pre-named as the shadow grid **S-HFRAC {33, 67}** so the ruled value is a comparison rather than an assumption, and TIER-C6 parameterises `_account` to make that grid possible — v5 read the fraction from a module constant, which is why S-HFRAC could not previously exist.

**H6 — THE PINS AND THEIR COMPARISON GRIDS.** *Ruled: the trail's two pinned numbers, each carried with the grid that surrounds it.* The offset is pinned at **0.5 ATR** (F-C4-b, ratified) with comparison grid **S-OFFSET {0.25, 0.5, 0.75}**; the minimum advance is pinned at **0.05 ATR** (F-C4-d) with comparison grid **S-MINADV {0, 0.05, 0.10}**. The two are reported as a **3 × 3 cross, whole**, so a reader can see the pinned cell's neighbourhood rather than the pinned cell alone.

**Both definitions are RELAYED, not filed-at-source** — they come from the commission text of 2026-08-16, which is itself an operator paste. That is the same provenance H1, H2, H4, H5 and H7 have, and it is stated rather than upgraded.

---

## 3 · THE NAMESPACE COLLISION TO NAME ONCE AND DISMISS

`exchange/queue/001_condensed-project-history.md:73-78` defines **`F-H1` … `F-H6`** — *fixture* identifiers for the condensed-history document (*"F-H1 | Every claim carries a tag."*), also cited at `2026-08-02_HEPHAESTUS_report_exchange-v1-build.md:361` and `BUILDERS_REPORT_HERMES_2026-08-05_FIRST_RUN.md:157`.

**Different prefix, different lane, unrelated.** It is named here because a reader searching for `H3` will find `F-H3` and conclude the hook has a source. It does not.

---

## 4 · THE DISPOSITION OF F-C5-h

F-C5-h offered two remedies: *define the labels in the estate, or strike them and cite the pastes directly.* **This document does both, item by item, because the honest answer differs by item.**

| | items | disposition |
|---|---|---|
| **DEFINED, fully anchored** | D15 | filed ruling + filed content. Keep the label |
| **DEFINED THIS TURN by operator ruling** | H3, H6 | content now exists; provenance is a relayed paste and is labelled so |
| **ENACTED but not defined** | D12, D13(c) | the RULE is fully specified in code; the LABEL's source paste was never filed. Keep the label, cite the code, and stop citing "the paste" |
| **DEFINED BY RELAY ONLY** | H1, H2, H4, H5, H7 | one table in one build document is the whole anchor. Keep, and cite that table rather than an interview section that is not in the estate |
| **STRIKE THE LABELS** | **D1–D11, D13(a), D13(b), D14** | **no source of any kind.** Eleven of fifteen. Per F-C5-h's own second remedy and the V-6 precedent, these labels should be struck from future documents and the underlying requirement cited directly, or defined before next use |

**RECOMMENDED RULING, ONE LINE:** *strike D1–D11, D13(a–b) and D14; keep D12, D13(c) and D15 citing code; keep H1–H7 citing the TIER-C5 relay table, with H3 and H6 now carrying the content ruled 2026-08-16.*

**PRECEDENT, ON THE RECORD.** `BUILD_2026-08-15_VIZ2_CATHEDRAL.md:52`, finding V-6, ruled the same way about the word `fuzz` — *"zero hits repo-wide… Ruling needed, or drop the word."* `fuzz` and `D1–D15` were named in the same sentence of the same status document. They should get the same answer.

---

*End of definitions document. APOLLO · 2026-08-16 · 22 labels mapped · 13 with no source · 2 defined this turn · F-C5-h answered rather than deferred.*
