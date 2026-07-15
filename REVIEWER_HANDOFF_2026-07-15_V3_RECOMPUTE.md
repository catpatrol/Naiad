# REVIEWER HANDOFF — 2026-07-15 (V3 Recompute R1–R10, Tier A → V4 design inputs)
### From: Claude Code (**builder**, this session). To: the project reviewer + operator Ludwig.
### Direction note: the two prior handoffs run reviewer → next reviewer. This one runs
### **builder → reviewer**. It is a front door to artifacts, not a substitute for them.
### Authority: repo `LEDGER.md` + the committed artifacts. This doc summarizes them;
### on any conflict, **the repo wins**. Verify before acting.

---

## 0. Verify-first actions (in order — do these before believing anything below)

1. `git log --oneline -1` → expect **`2bdda8d`** on `v12-v1-census`.
   **⚠ NOT PUSHED.** The branch is *ahead 1* of `origin/v12-v1-census`. Pushing and
   merging are operator-only; the builder did neither. Until the operator pushes, this
   commit exists on the local machine only, and `origin` does **not** carry this phase.
2. `python scripts/v3_recompute.py` (~2 min, reads raw journals only, no network).
   Expect **`OUTPUT_HASH 2640decda9bb23c4c98e9280907962902d06546065d9c89bacd2afbb293eac71`**
   — component hashes `recompute.json 9bdea8ef…`, `V3_RECOMPUTE_R1_R10.md ca73bac2…`.
   The journal root is recorded **repo-relative**, so your hashes should match exactly.
   If they do not, stop — the reader or the estate differs, and nothing below is safe.
3. Diff `recompute.json` against your own recompute. That file, not this doc, is the
   deliverable for independent verification.

**Bootstrap CIs will differ from the 2026-07-13 record.** Seed here is `20260715`,
10,000 resamples, campaign-level. The headline CI is [−2.0257, −1.3613] against your
recorded [−2.0407, −1.3597]. That is the seed, not the data — every point estimate
matches exactly (see §3).

---

## 1. What this phase was

Ten measurements (R1–R10) from the existing V3 anchor journals. **Tier A: journal
arithmetic only.** No engine change, no config change, no replay, no network, no
lockbox touch, no merge. Read-only throughout; `engine/` and `configs/` are untouched
in the commit (verified: the commit contains exactly four files).

Basis: engine 1.0.7 (`2f260e1`), config `v12_anchor` (`a3917ea5…`), scored partition
(exploration-classic), 20 cells, 8,387 resolved tranches, 3,456 campaigns.
Evidence spend: **NONE** (VR-1; first look already consumed).

**Contract note.** `V3_Recompute_R1_R10_Builder_Contract.md` was not in the repo. It was
found in `~/Downloads` and read in full before any code was written. It is **not**
committed — if it should be under version control, that is an operator call.

---

## 2. Artifacts (commit `2bdda8d`, four files, 4,368 insertions, 0 deletions)

| file | what it is |
|---|---|
| `V3_RECOMPUTE_R1_R10.md` | the report — every table with its stated caveat in the header |
| `recompute.json` | machine-readable, **for your independent verification** |
| `scripts/v3_recompute.py` | the script; re-runnable, deterministic |
| `LEDGER.md` | entry + G-7 register item appended (append-only respected: 21 insertions, 0 deletions) |

Per contract §0 Step 6, what to carry: **the fixture table, the prediction scorecard,
and `recompute.json`.**

---

## 3. Fixtures F1–F9 — ALL MATCH (verdict PASS, 10/10 checks)

F1 3456/8387 · F2 −5756.9093 · F3 +1345.3095 · F4 −12859.1281 ·
F5 PROTECTED 3381 / STILLBORN 2076 / NEVER_GREEN 1830 / FADED 1100 ·
F6 A+ 39 / A 1153 / B 1954 / C 0 · F7 8365 · F8 45 · **F9 0**.

**Your 2026-07-13 record reproduced independently from raw bytes** (these were *not*
read as inputs — §3.3 respected; `ROLLUPS_AND_HYPOTHESES.md` and
`V3_STOP_AND_EXIT_FORENSICS.md` were never opened by the script):

grid net 1× −5756.9093 · 0× +1345.3095 · expectancy −1.6658 · win 11.28% ·
campaigns 3456 · strip-best −5871.3612 · best campaign BTCUSDT_swing c197 +114.4519 ·
grade census 310 ungraded = 45 V-initiated + 265 no-filled-R1 ·
Report 1's 2,899 per-tranche resumption count.

**F9 = 0 — your reading is UPHELD.** `signal.max_r_count = 0` and `signals.py:368`
(`rcap_ok = max_rc == 0 or r_count < max_rc`) make the `r_cap` branch unreachable by
construction. The signal layer is **not** capping PRIMEs, so unlimited adds remains a
**trading-config-only** change (`trading.max_tranches`), not Pine-parity-bound.
Aggressive mode stays cheap on this axis.

Two fixtures did real work rather than rubber-stamping:
- **F3/F4 only reproduce with the signed `one_r`** (contract §4's literal formula).
  The `abs` variant misses both. That discrepancy surfaced finding (a) below.
- **F6 forced the cohort definition** to *campaigns initiated by a non-V ENTRY_FILL*
  (R1 PRIME), by that tranche's journaled capped grade. Your own ledger line —
  "310 ungraded = 45 V-initiated + 265 no-filled-R1" — independently confirms it.

---

## 4. Prediction scorecard — P-R1 falsified, four confirmed

| # | verdict | evidence |
|---|---|---|
| **P-R1** | **FALSIFIED** | X-A gross delta: swing **+528.92** (wins), **position −97.23 (loses)**, intraday −421.47 |
| P-R2 | CONFIRMED | V share of Σwins **0.60%** vs 1.30% of campaigns |
| P-R6 | CONFIRMED | Z2 stage-1 **100.0%** — but trivially; see (d) |
| P-R7 | CONFIRMED | `tranche_cap` **145,749** ≫ 500 |
| P-R9 | CONFIRMED | `def_full` 1× = **−592.38**, still net negative |

**P-R1 is the one to read closely.** The prediction required X-A to beat the book on
swing **and** position. It beats swing decisively and **loses on position**. Grid-wide
X-A is a wash: **+10.22** against the book's +1345.31 — the swing win is nearly
cancelled by the other two mandates. X-B is materially identical to X-A (+10.31);
X-C (−1145.19) and X-D (−567.44) both lose badly. Any "adopt X-A" argument is a
**swing-only** argument, and it is first-order: a really-adopted exit rule changes
which adds fire and when campaigns die.

**P-R2 confirmed in the strong direction.** V campaigns are not merely *not* tail-carrying
— they are *under*-represented, carrying 0.60% of Σwins on 1.30% of campaigns, less than
half their weight.

---

## 5. Builder findings not previously registered

Each recomputed from raw bytes. **None affects a fixture** — all nine still match.

**(a) ZECUSDT_intraday traded on negative equity.** Realized equity crossed zero on
2022-11-02, bottomed at −2,732.24, ended −2,719.97. **717 of its 1,414 tranches carry a
negative `one_r`** (= `r_pct × equity`, `trading.py:367`) with inverted `qty` sign. This
is journaled faithfully and the §4 signed formula reproduces F3/F4 exactly, so it is
**not** a reader artifact and **not** a fixture failure. But a bankrupt-cell-keeps-trading
path is a finding about the anchor run, and every R-denominated quantity on those rows
is measured against a negative unit — which flips the sign of their cost adjustment.
Treat this cell's contribution to any aggregate with suspicion, R9 especially.

**(b) `engagement_flags.ext_before_exit` is MISNAMED.** `shadows.py:190-194` loops
`range(tr.fill_i, last + 1)` with `last = camp_end` — the **campaign-death** bar, not the
tranche's exit bar (the engine's own comment says "within the campaign"). It is therefore
true whenever an extension occurred anywhere between fill and campaign death, **including
after this tranche was already stopped out**. It reads `ext_before_CAMPAIGN_DEATH`.
By contrast `tpw_before_exit` (via `Tranche.first_tpw_i`, `trading.py:412-415`) is set
only for tranches open at the TPW bar's close and **is** strict. **The two flags are
named as a pair but measure different windows and must not be compared.** Any prior
analysis that compared them is comparing a tranche-life count to a campaign-life count.

**(c) TPW is effectively dead as an arming trigger.** It fired before exit for **2 of
1,581** R4-population tranches (**0.13%**). An independent timestamp scan (not the flag)
finds only **16 of 2,999** TPW event rows falling inside *any* open same-direction
tranche window. A TPW-armed harvest rule would almost never trigger on this run. Of the
two candidate triggers, the **2-ATR extension is the only viable one** — and note X-B
(= X-A + 50% banked at first TPW) is consequently near-identical to X-A, which explains
its +10.31 vs X-A's +10.22.

**(d) R6 zone × stage is NEARLY DEGENERATE.** Z2 fills are **100% stage-1** (0 stage-2);
Z3 fills are **100% stage-2** (0 stage-1). Two of six Z1/Z2/Z3 × stage cells are
**structurally empty**, not sparse. Only Z1 and the no-zone bucket populate both stages.
P-R6 is therefore confirmed **trivially at 100%**, not marginally at ≥95% — it tested a
coupling that appears enforced upstream, not a tendency. **Consequence: any Z2-vs-Z3
expectancy difference is confounded with a stage effect and cannot be separated from
these journals.**

**(e) R3's `ratcheted-≥-BE` class is empty BY CONSTRUCTION** for the gross-loss
population: a stop resting at/beyond the entry fill cannot fill at a gross loss. Read the
absence as a tautology of the population filter, **not** as evidence the ratchet never
reaches breakeven.

---

## 6. PARTIAL items — named gaps, no estimates substituted (contract §8)

**R4 "median MFE at the first trigger" — NOT COMPUTABLE.** `mfe_r` on the EXIT row is
whole-life MFE (`shadows.py:167`), not its value at the trigger bar; the trigger bar
index (`tpw_i` / `ext_i`) is never journaled.
→ **Missing field:** `mfe_at_tpw_r` / `mfe_at_ext_r`. **Row type:** the EXIT row,
alongside `mfe_r` / `give_back_r` — or a per-tranche TPW event row carrying `tranche_id`
plus running `mfe_r`.

**R4 "extension before their exit" — NOT COMPUTABLE.** Per finding (b), the only
journaled flag is mis-windowed and cannot be narrowed post hoc.
→ **Missing field:** `ext_i_offset` (bars from fill), or a correctly-windowed boolean over
`[fill_i, exit_i]`. **Row type:** the EXIT row, inside `engagement_flags`.

What *was* recoverable is reported and clearly labelled as such: R-at-first-trigger,
inverted from the shadow blend (`tpw_r = 2·exit_XB − exit_XA`), which is **R at the
trigger, not MFE at the trigger**. Median R at first extension: **+1.49** (n=359, a
genuine lower bound). **Both are candidates for S-1's shadow columns.**

---

## 7. D3 / VS-Z3 — the hold is now decidable (R6 + R7 are in)

VS-Z3 was **HELD pending R6/R7**. Both are now computed. Three inputs, and they do not
point the way the hold assumed:

1. **R8 publishes Z3 for the first time — and it is not better.**
   | zone | n | net R/unit | 95% CI |
   |---|---|---|---|
   | Z1 | 5790 | −1.5847 | [−2.0069, −1.2553] |
   | Z2 | 812 | −1.3807 | [−1.8132, −0.9971] |
   | Z3 | **996** | **−1.4127** | **[−2.0712, −0.9499]** |

   All three are negative and **all three CIs overlap heavily**. Z3 — the operator's
   stated primary structural setup — is **not distinguishable** from Z1 or Z2 in-sample.

2. **Widening `z3_prox` recruits from the `no_zone` pool: 229,963 rejects.** That is the
   sizing answer R7 was asked for.

3. **⚠ Z3 signals bypass the ribbon-separation gate.** `signals.py:369`:
   `rib_sep_ok = (…) or active_zone == 3`. So widening `z3_prox` does **not** merely add
   more Z3 signals — it adds signals that **skip a gate** (`ribbon_sep`, itself 43,917
   rejects). That is a **qualitative change to the eligible set, not a first-order
   R-scaling**, and nothing in this Tier-A phase measures it.

**Builder's read (not a nomination — the five-slot decision is the operator's):** the
premise that Z3 deserves widening is not supported by in-sample expectancy, the Z3
cohort is confounded with stage-2 per finding (d), and the gate-bypass makes it the
*least* first-order-measurable of the candidate variants. If VS-Z3 proceeds, it wants
S-1 instrumentation, not a Tier-A argument. **VS-Z3 was not implemented this phase**
(`z3_prox` unchanged at 0.35), per the hold.

---

## 8. Registers & open items

- **G-7 [OPEN]** — logged this phase per contract §10. No counter, code- or ledger-level,
  on tuned exploration-classic re-runs. Mitigation: every Tier-C exploration-classic run
  gets a pre-registered ledger line (config sha + hypothesis + prediction) **before** it
  runs. *This phase spent no evidence, so G-7 does not bind it — it binds what comes next.*
- G-1, G-2 unchanged (no lockbox guard; LIT excluded). G-3…G-6 closed at engine 1.0.7.
- **Not scored here** (S-1 items, carried unchanged): P-S1a, P-S1b.

---

## 9. Next-step queue

1. **Operator:** push `2bdda8d` if this phase is accepted (builder does not push/merge).
2. **Reviewer:** independent recompute → diff `recompute.json`; confirm `OUTPUT_HASH`.
3. **Reviewer/operator:** rule on **D3/VS-Z3** — §7 supplies what the hold was waiting for.
4. **S-1 scoping:** findings (b) and (c) and both §6 gaps are S-1 shadow-column
   candidates. Fixing the `ext_before_exit` window is a **correctness** fix, not a feature.
5. **Open question for the operator:** should the contract file itself be committed?

---

## 10. What this phase does NOT say

Every number is **in-sample on data already mined**. It **ranks candidates; it validates
nothing.** Not tuning, not evidence about the future, not a variant nomination, not a
lockbox touch, not S-1. **Aggressive mode is out of scope** — it creates tranches that do
not exist in these journals and needs a Tier-C run; R9 covers defensive and neutral only.
R1 and R9 are **first-order**: R9 does not change the stop path, but it *does* change the
equity path, the 1R rail, and the halt calendar — all of which gate admission. Faithful
measurement is S-1's job.
