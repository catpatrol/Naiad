# BUILDER'S REPORT — HEPHAESTUS — QUEUE 008 D-0 · THE CONFIRMATION GATE

**Lane** HEPHAESTUS · **Branch** `v12-v1-census` · **HEAD at start** `cdb56bf` · **Date** 2026-08-22
· **Commissioned by** the operator directly: *"proceed with QUEUE-008 D-0 and VIZ-4 twin"*.

**NOTHING FROM QUEUE 008 WAS BUILT. `~/naiad-sail` does not exist.** D-0 is a HALT-before-any-code
gate; its whole content is a decision put to you. This document is that decision, plus the evidence
that makes it a decision rather than a request for trust.

---

## 0 · WHAT HAPPENED, IN PLAIN LANGUAGE

Queue 008 is the contract for **SAIL** — a program that would watch the market live and write down
the trades your card v6 *would* have taken, with no money moving. It is the estate's only planned
out-of-sample instrument.

The contract has a problem it declares about itself. Most of it — seven of the nine deliverables and
nine of the ten tests — was **written by me, not approved by you**. The stamp says so:
*"D-1..D-8 and F-SAIL-1..7, 9, 10 are HEPHAESTUS's derivation … PENDING CONFIRMATION."* D-0 exists
to put that derivation back to you before a line of code is written, because the alternative is a
builder in a later session reading a ratified stamp over content no operator ever saw.

**So D-0 asked me to bring you my own homework to mark.** I did not mark it myself. I ran thirteen
independent agents over it — one per deliverable and fixture group, plus two critics — each required
to open every file the contract cites and check that the citation says what the contract claims.

**The result: every one of the eleven sections came back defective. 139 findings, 32 of them
blocking.** I then re-checked the eight most consequential myself, by hand, against the code. **All
eight held.** Three of them are the same class of error that nearly shipped a measured loss in the
2026-08-18 drafting session: *a citation that does not say what the contract claims it says.*

**And the two critics found something worse than any individual defect: the funnel itself was
wrong.** Fifty questions ordered by document number, of which about twenty were not decisions at all
but corrections I should simply make — while **the one question D-0 names first was never asked**.

**So this report does not hand you fifty questions. It hands you SIX**, in the order they must be
answered, with the corrections routed to where they belong.

---

## 1 · THE SIX QUESTIONS

Each is self-contained. You need nothing else open to answer any of them. Every option includes
dropping the thing entirely, and every recommendation says how strongly the evidence supports it.

---

### ❶ THE CARD-SPEC FORK — and it is not the fork the contract offered you

**WHAT IT IS.** SAIL is meant to be a *body* with no *brain*: it must not contain any trading logic
of its own. All the rules — where to enter, where the stop goes, when to exit — arrive in a single
data file called the **card-spec**, exported from Naiad. SAIL reads that file and obeys it. That is
the whole design: if a rule is not in the file, SAIL cannot do it.

**The problem: the card-spec does not exist.** I re-ran the enumeration — `card_spec`, `spec_sha`
and `export_card` return zero hits across every `.py`, `.json` and `.yaml` in Naiad. And the brief
orders APOLLO's export *after* this skeleton is built. So a builder reaching the acceptance tests
has nothing to import.

The contract offered you two branches: **(a)** wait for APOLLO's export, or **(b)** I write a
temporary "provisional" spec so work can start.

**WHY IT MATTERS — AND WHY THE FORK IS FALSE.** Branch (b) does not work as written, and I verified
this rather than inferring it:

- Branch (b) says the provisional spec is built *"mechanically from the union in D-2a"* and that
  *"criteria 1 and 4 are met against it"* (`008:19-22`).
- Criterion 4 is the **parity check** — proving SAIL reproduces card v6 on three known past trades.
  Those three trades live in a block called `reference_trades`, which is specified in **D-2a′**, a
  *different* item, not in the D-2a union (`008:294-300`).
- The test that consumes them says in its own text: ***"APOLLO's export paste generates the
  vectors"*** (`008:707-708`).
- And D-2a′ says a spec whose `reference_trades` block is missing **HALTS** the program on startup
  under D-9a — *"never a skipped check"*.

**A spec built the way branch (b) describes therefore stops SAIL dead at launch and cannot satisfy
criterion 4.** Branch (b) is not a slower path; it is not a path.

**It is worse than that.** The parity test names its source of truth as
*"`scripts/tierc6_rules.py:220 CARD_V6` executed through `scripts/tierc5.py`"*. I checked:
**`scripts/tierc5.py` contains zero occurrences of `trail_min_advance_atr`** — a field card v6
declares at `tierc6_rules.py:214` under ruling F-C4-d. The only code that passes it is
`tierc6.py:347` and `tierc7.py:252,262`. **Running v6 "through tierc5" would silently drop the
card's trail rule and generate parity vectors that are not card v6's behaviour** — and every future
SAIL build would then be certified against them.

| your options | for | against |
|---|---|---|
| **(a) Wait for APOLLO's export.** SAIL is not built until the card-spec exists. | The only branch that works as written. No rework. The parity vectors come from the one place authorised to make them. | SAIL waits on APOLLO. If that export is weeks away, the out-of-sample instrument does not exist for weeks. |
| **(b′) Provisional spec, AMENDED** — I also generate the three parity vectors, by running card v6 through `tierc6.py` (not `tierc5.py`), and label the whole file `provisional: true`. | Work starts now. The standing consequence is already stated: APOLLO's real export re-pins every slot and re-runs two tests. | I would be authoring both the thing under test and its expected answers — the exact collapse of commissioning and verification that D-0 exists to prevent. |
| **(c) Drop the parity requirement from the skeleton** — build SAIL without criterion 4, add it when the export lands. | Honest about what a skeleton is. Nothing is certified against vectors nobody trusts. | The parity check is the only thing that would catch SAIL quietly trading differently from your card. Dropping it makes the first real trade the first test. |
| **(d) Drop SAIL until APOLLO's export is scheduled.** | Costs nothing. Nothing downstream depends on SAIL today. | Leaves the estate with no out-of-sample instrument, which the brief calls the reason the whole build is structural. |

**MY RECOMMENDATION: (a), and I hold this firmly.** Branch (b) as offered is unbuildable, and the
amended (b′) asks me to write both the exam and the answer key on the one deliverable whose entire
purpose is to catch me being wrong. **If the export is genuinely far off, (c) is the honest second
choice** — build the body, and let the parity check arrive with the brain. What I would not do is
ratify (b) as written.

---

### ❷ THE VALIDATOR'S FIRST CLIENT IS A CLAIM THE ESTATE HAS ALREADY REJECTED

**WHAT IT IS.** Deliverable D-7 asks SAIL to carry a **validator**: a small piece of code that takes
a pre-registered claim — a prediction written down *before* the data is seen — and reports whether
live results bear it out. Its first assigned client is a claim called **L-LIMIT-2**: roughly, *"an
entry placed at a limit offset beats the same setup entered at the market trigger."*

**WHY IT MATTERS.** D-7 is not a minor item. Verdict criterion 13 exists solely because D-7 *"is a
founding justification for the whole build"* — one of the main reasons SAIL is being built at all is
to settle claims like this in live data instead of backtests.

**The finding, and I read this in the code myself.** `scripts/tierc6_lab_limit.py:91-98` opens with
a heading in its own words:

> **1. THE FORM IS FALSIFIED IN-SAMPLE BY ITS OWN CLAUSE (c).** `k* = 0.40` on both arms, and that
> cell's `max_single_trade_delta_share` is 41.4 — the paired improvement over the card is +0.0013
> R/campaign while a single campaign's delta is forty times the whole sum. F-C5-f's defect exactly:
> the number is real and the mechanism is one trade.

In plain terms: **the claim already failed its own pre-registered test.** The apparent improvement
is one third of one thousandth of an R per campaign, and a single trade accounts for forty times the
entire effect. The estate's own lab already ran the falsification clause and printed the verdict.

**The contract does not mention this anywhere.** D-7a instructs the builder to implement the claim
*"as written"* and treats it as an open question awaiting live data.

| your options | for | against |
|---|---|---|
| **(A) Keep D-7, repoint it at a different first client.** The validator is generic by design; L-LIMIT-2 was only the first customer. | Keeps the machinery, which is genuinely reusable, and stops it opening on a dead claim. | Nothing else is pre-registered and ready. You would be commissioning a validator with no client, which is how a deliverable becomes decoration. |
| **(B) Keep D-7 with L-LIMIT-2, and let the first printed row say "falsified in-sample".** | Honest. A validator whose first output is a refutation is a validator doing its job. | Spends build effort proving again what the lab already proved. |
| **(C) Drop D-7 from the skeleton.** Build SAIL as a journal-writer; add the validator when a live claim needs one. | Removes the largest single unbuilt component and its two blocking dependencies (see ❸). Nothing today needs it. | Criterion 13 exists because D-7 was a founding justification. Dropping it means the skeleton no longer answers the question it was partly commissioned to answer. |

**MY RECOMMENDATION: (C) for this phase, then (A) when a live claim exists.** Moderate-to-high
confidence. D-7 currently drags two blocking dependencies behind it (question ❸ and a statistics
problem: the functions it names — `cluster_boot`, the BH correction — live only in Naiad, which this
same contract twice forbids SAIL from reaching into). **You are being asked to fund a validator that
cannot import its own statistics, for a claim that has already failed.**

---

### ❸ WHAT L-LIMIT-2 NEEDS YOU TO NAME — and the trap inside it

**WHAT IT IS.** Independent of ❷: the L-LIMIT-2 results table carries a self-imposed lock. It may
not be published with a validation clause until you personally name three things. This is
REGISTER item 8, and it blocks D-7c.

**The three things, quoted from `scripts/tierc6_lab_limit.py:228-236`:** *the instrument · its
corridor edges · its card version.*

**THE TRAP, which the contract does not surface and which I read in the same block.** The interdict
continues:

> *the estate's only forward reserve today is the Prometheus paper route, and F-C5-k records that it
> is running **v1**, three card generations behind the book this form was measured on — so binding
> SAIL to it without a ruling would **validate v6's entry rule on v1's entries**.*

So the obvious answer — "bind it to the paper agent already running" — is the one answer that
silently invalidates the result.

| your options | for | against |
|---|---|---|
| **(A) Name SAIL as the instrument, once it exists, at card v6.** | The only binding that measures v6's rule on v6's entries. | Circular in time: SAIL does not exist, and D-7c is inside the contract that would build it. Answer ❶ and ❷ first. |
| **(B) Name the Prometheus paper route.** | Available today; it is already sailing. | It runs v1. You would be validating a v6 rule on v1 entries. **I would refuse to build this without you saying explicitly that you accept that.** |
| **(C) Leave it unbound.** The table stays unpublished with no validation clause. | Costs nothing and breaks nothing. The lab already prints its own falsification verdict. | REGISTER item 8 stays open and D-7c cannot be built — which is fine if you take (C) in question ❷. |

**MY RECOMMENDATION: (C), and it follows automatically if you drop D-7 for this phase.** High
confidence — this is a lock the estate placed on itself deliberately, and nothing forces it open now.

---

### ❹ "exited" or "belled" — the question as posed cannot be answered, because it is malformed

**WHAT IT IS.** The weekly report is meant to show a **funnel**: how many setups were seen, how many
passed each filter, how many were entered, and what happened to them. The contract asks you to rule
what the sixth and final stage is called — the brief says `exited`, the code says `belled`.

**WHY IT MATTERS — and why I am not asking you to pick a name.** I checked what `belled` actually
does. It appears **once** as a definition, in a list at `scripts/tierc2_rules.py:134-135`, and is
re-exported twice (`tierc3_rules.py:78`, `tierc4_rules.py:98`) as `= V1.FUNNEL_STAGES`. **No funnel
builder in the estate reads it.** It is a name in a tuple with no functional consumer.

And the two words are not synonyms describing one thing: **`belled` is one way a trade can end;
`exited` is all the ways.** A trade can end by stop, by bell, by time-stop, by corridor end, by
wall. Choosing `belled` as the terminal stage would report one exit type as though it were the total.

**A second, verified error rides with this.** D-8 claims the exit reasons are
*"corridor_end, stop, bell, time_stop, wall"*. There is **no exit reason `bell`**. At
`tierc6.py:291-298` the variable `bell` holds either `"bell_12_89"` or `"bell_89_316"`, and that
variable is what gets written. The literal string `"bell"` at `:300` is assigned to `blocked`, a
different field. A weekly report built to the contract's list would show an exit category that never
occurs and miss the two that do.

| your options | for | against |
|---|---|---|
| **(A) Rule `exited`, and have the weekly break it down by actual reason** — `corridor_end`, `stop`, `bell_12_89`, `bell_89_316`, `time_stop`, `wall`. | Matches what the code emits. The funnel's last stage becomes the union, with the breakdown underneath — which is what you would want to read. | Requires the contract's exit list corrected. I would do that as an amendment, not a question. |
| **(B) Rule `belled`, matching the constant.** | Consistent with a name already in the estate. | Reports one exit type as the terminal stage. Nothing consumes the constant anyway, so the consistency is with a dead name. |
| **(C) Drop the funnel from the weekly.** | The weekly still shows trades and R. | The funnel is the only view that shows *where the system leaks* — the thing you would use it for. |

**MY RECOMMENDATION: (A).** High confidence on the mechanics, which I verified in the code.

---

### ❺ IS D-4 RATIFIED, OR PENDING? Your own stamp and the gate disagree

**WHAT IT IS.** D-4 is the **setup registry** — the "nucleus" from your 2026-08-18 diagram, the part
that lets more than one setup plug into SAIL.

**THE CONTRADICTION, verified by reading both lines.** The stamp at `008:3` ratifies
*"DEC-1..DEC-5, **D-4 (strengthened)**, D-9, F-SAIL-8 and the REGISTER addition ONLY."* Four lines
later at `008:5`, and again at `008:160`, the file puts ***"D-1..D-8"*** to you as
**PENDING CONFIRMATION** — and `D-1..D-8` contains D-4.

**So D-4 is simultaneously in the ratified set and the pending set.** A builder in a later session
reading only the stamp treats it as yours; one reading only D-0 brings it back to you.

| your options | for | against |
|---|---|---|
| **(A) D-4 is RATIFIED** — the gate's list is corrected to "D-1, D-2, D-3, D-5, D-6, D-7, D-8". | Matches your stamp, which is the more specific instrument. D-4 is your diagram's own element. | The "strengthened" text was still written by me from your diagram. |
| **(B) D-4 is PENDING** — it joins the funnel and you confirm it like the rest. | Nothing derived escapes the gate. | Re-opens something you already stamped. |

**MY RECOMMENDATION: (A).** The stamp names D-4 explicitly and by exception; D-0's `D-1..D-8` reads
as a range written without checking what it swept in. **This is one word and it removes a real trap.**

---

### ❻ SCOPE: eighteen sub-deliverables have no test at all

**WHAT IT IS.** The contract ends with ten tests and thirteen conditions that define "done". The
completeness critic enumerated every sub-deliverable against every test and every condition.

**About eighteen sub-deliverables are pinned by no test leg and no condition.** They include
**the whole of D-3 (the feed — where SAIL's price data comes from)**, the execution economics in D-5,
and **restart survival in D-6** — whether SAIL still knows about your open position after the laptop
reboots. Nothing tests that today.

**Why this is a decision and not a correction:** closing it costs builder time, and you are the one
who decides whether the skeleton is allowed to be DONE with these untested.

| your options | for | against |
|---|---|---|
| **(A) Fund the three that matter** — a feed test, an execution-economics test, a restart test — and accept the rest untested for the skeleton. | These three are where a silent defect **poisons the out-of-sample record permanently**: bad bars, wrong fills, or a forgotten position all corrupt the journal you would later trust. | Three more tests to write before SAIL runs. |
| **(B) Fund all eighteen.** | Nothing ships untested. | Turns a skeleton into a full build; the contract calls itself a skeleton for a reason. |
| **(C) Ship as specified, untested.** | Fastest. | "Done" would then mean "the tests we wrote pass", not "it works". The feed is the input to everything; if it is wrong, every number SAIL ever writes is wrong and nothing would say so. |

**MY RECOMMENDATION: (A).** High confidence on which three — I applied one test to pick them: *does
a wrong answer here corrupt the record rather than the code?* Only those three pass it.

---

## 2 · THE EVIDENCE — what was checked, and how

**Thirteen agents, 0 errors, 635 tool calls, 1.78 M tokens, 30 minutes.** Eleven verified one
deliverable or fixture group each; two critiqued the pooled result. Every agent was read-only —
D-0 halts before any code, and nothing was written to the estate by any of them.

| section verified | verdict | blocking | material | minor | funnel items produced |
|---|:-:|--:|--:|--:|--:|
| D-1 · the ops spine | DEFECTIVE | 2 | 6 | 5 | 9 |
| D-2 · The card-spec handshake | DEFECTIVE | 2 | 4 | 3 | 6 |
| D-3 · The feed | DEFECTIVE | 2 | 12 | 4 | 11 |
| D-5 · The paper execution layer | DEFECTIVE | 2 | 6 | 4 | 8 |
| D-6 · State persistence and the wake-order note | DEFECTIVE | 2 | 6 | 4 | 7 |
| D-7 · THE VALIDATOR | DEFECTIVE | 3 | 4 | 2 | 6 |
| D-8 · The weekly report in "yardstick format" | DEFECTIVE | 4 | 6 | 3 | 7 |
| F-SAIL-1, F-SAIL-2, F-SAIL-3 | DEFECTIVE | 2 | 8 | 3 | 12 |
| F-SAIL-4, F-SAIL-5, F-SAIL-6 | DEFECTIVE | 1 | 5 | 4 | 10 |
| F-SAIL-7, F-SAIL-9, F-SAIL-10 | DEFECTIVE | 2 | 13 | 3 | 9 |
| PREREQUISITE | DEFECTIVE | 1 | 9 | 2 | 7 |
| **11 sections** | **all DEFECTIVE** | **23** | **79** | **37** | **92** |

| critic | verdict | blocking | material | minor |
|---|:-:|--:|--:|--:|
| COMPLETENESS | DEFECTIVE | 3 | 5 | 2 |
| DECIDABILITY | DEFECTIVE | 6 | 9 | 2 |

**92 funnel items and 139 defects came back. That is not a result I would hand you on trust** —
agent output is `[handoff]`, never `[verified]` (§6.1), and eleven agents primed to hunt a defect
class will find defects. **So I re-checked the eight most consequential myself, by hand, against the
code. All eight held.** They are below with the commands that prove them.

### 2.1 · The eight I verified personally — all `[verified]`

| # | the contract claims | the code says | class |
|---|---|---|---|
| **V1** | D-5: *"Fills at close per card law"*, unqualified | Card law says the opposite for the stop. `tierc4_rules.py:242-244`: *"THE STOP EXECUTES. A bar touching the stop exits AT the stop, ADVERSE-FIRST."* `tierc6.py:281`: `exit_i, exit_px, exit_reason = j, stop, "stop"` — **at the stop, not the close** | **wrong trading semantics** |
| **V2** | D-8: exit reasons are *"corridor_end, stop, bell, time_stop, wall"* | There is **no `bell` exit reason**. `tierc6.py:291-296` sets the variable `bell` to `"bell_12_89"` or `"bell_89_316"`; `:298` writes *that*. The literal `"bell"` at `:300` is `blocked`, a different field | **wrong enumeration** |
| **V3** | REGISTER 2: a live choice between `exited` and `belled` | `belled` is defined once (`tierc2_rules.py:134-135`) and re-exported twice (`tierc3_rules.py:78`, `tierc4_rules.py:98`, both `= V*.FUNNEL_STAGES`). **No funnel builder reads it** | **dead constant** |
| **V4** | F-SAIL-6: reference implementation is *"CARD_V6 executed through `scripts/tierc5.py`"* | `grep -c trail_min_advance_atr scripts/tierc5.py` → **0**. Card v6 declares it at `tierc6_rules.py:214` (ruling F-C4-d); only `tierc6.py:347` and `tierc7.py:252,262` pass it. **v6 through tierc5 silently drops the card's trail rule** | **wrong trading semantics** |
| **V5** | PREREQUISITE (b): a provisional spec from D-2a meets criteria 1 and 4 | `reference_trades` is in **D-2a′**, not D-2a (`008:294-300`); F-SAIL-6 assigns their generation to **APOLLO** (`008:707-708`); a spec missing them **HALTS under D-9a**. Branch (b) produces a spec that stops SAIL at launch | **unbuildable option** |
| **V6** | D-7a: implement L-LIMIT-2's claim *"as written"*, as an open question | `tierc6_lab_limit.py:91-98`: *"**THE FORM IS FALSIFIED IN-SAMPLE BY ITS OWN CLAUSE (c)** … the paired improvement is +0.0013 R/campaign while a single campaign's delta is forty times the whole sum"* | **already refuted** |
| **V7** | F-SAIL-7: grep for `sk-`, `token`, `secret` … *"fails on any hit"* | `sk-` occurs in **26 tracked files**, every sampled hit inside `risk-free` (13), `risk-normalized` (6), `risk-mode` (4), `disk-sleep` (4), `disk-only` (3). The test fails on the estate's own prose | **fixture cannot pass** |
| **V8** | The stamp ratifies *"D-4 (strengthened)"*; D-0 puts *"D-1..D-8"* pending | Both are true at `008:3` and `008:5`/`008:160`. **D-4 is in both sets** | **gate contradicts itself** |

**V1 and V4 are the same class as the 2026-08-18 near-miss** — a cited constant or module that does
not mean what the citation implies. That session caught `WALL_EXIT_ATR = 0.25` before it shipped a
measured loss. These two would have shipped **wrong fills** and **parity vectors that are not card
v6**, and the second is worse, because parity vectors are what every later build is certified
against.

### 2.2 · A finding that clears the contract, recorded because negatives matter

**D-2a's 22-field card union is CORRECT and complete.** The verifier checked it against the
authoritative fixture enumeration at `scripts/tierc6_fixtures.py:225-226` — six declared fields at
`tierc6_rules.py:212-217` plus sixteen inherited at `tierc5_rules.py:294-320`, with `harvest_frac`
and `wall_tf` both present. **This is the exact field list the 2026-08-18 session got wrong twice.**
It is right now, and the fixture-not-prose method is why.

---

## 3 · WHAT I WILL AMEND WITHOUT ASKING YOU

The decidability critic's central finding: **about twenty of the ninety-two items are not decisions
at all.** They are citation corrections, and putting them to you spends the one resource §1.4 calls
scarce — your attention — on questions with only one defensible answer.

**These are corrections I will make as amendments to the contract and report, not ask about:** the
`bell` exit-reason enumeration (V2) · the `tierc5.py` parity citation (V4) · the fills-at-close
wording (V1) · the `sk-` credential pattern list (V7) · the launchd plist key set (D-1b names one
load-bearing key; the proven shape at `M4-LAUNCHD.md:429-440` carries six) · the anti-vacuity clause
missing from F-SAIL-7 and F-SAIL-9 though F-SAIL-1 calls it *"MANDATORY"* · and roughly fourteen more
of the same kind.

**Nothing in that list changes what SAIL does. Every one of them changes what the contract says the
estate contains.** Each will be a dated correction that REPLACES the wrong text (§0), with the
citation that disproves it.

**I have not made them yet.** D-0 halts before any code, and I read that as covering the contract's
own body too: amending seventeen passages while the gate is open would hand you a different document
than the one you are being asked about. **They land in the same act as your answers.**

---

## 4 · THE GATE'S OWN DEFECTS

D-0 was written by me too, and it is the least complete thing in the contract.

1. **Its list is wrong in both directions** (V8). D-4 is ratified *and* pending.
2. **It carries two of the eight REGISTER items** — 2 and 7 — while **item 8 declares in its own row
   that it BLOCKS D-7c**. It is question ❸ above; the gate did not carry it. Item 5 also matters:
   verdict criterion 12 rests on it.
3. **It has no verdict criterion of its own.** Every other deliverable is pinned by one; the gate
   that authorises all of them is pinned by nothing.
4. **It has no ordering and no partial-closure rule.** It asks for thirty-three sub-decisions with no
   statement of which come first or what happens if you answer four of six.

**Recorded rather than quietly fixed**, and §5 proposes the repair.

---

## 5 · WHAT I RECOMMEND D-0 BECOMES

**A two-pass gate, and this report is pass one.**

- **Pass one (this document): the six questions.** They are the ones where a wrong answer corrupts
  the record rather than the code, and where you are genuinely the only person who can answer.
- **Pass two: the amendments.** I correct the ~20 citation defects, re-run the verification over the
  corrected text, and bring you a short list of anything that survives.
- **D-0 gains a verdict criterion:** *the gate is closed when every question in pass one has a dated
  answer recorded in this file, and no derived deliverable remains that no answer reaches.*

---

## 6 · VIZ-4 TWIN — CLOSED

`exchange/reports/DESIGN_CONTRACT_VIZ4_EMA_MANTLE_2026-08-15_1.md` was a byte-identical duplicate of
its twin. **Removed**, on the four-check gate of the 2026-08-12 TIDY precedent.

```
STEP 0 - ENUMERATE (invariant 6)              [NUL-safe: git ls-files -s -z, split on \0]
  stray blob                       : e65eff1eba776726537b5456628556f5df395c94
  tracked paths carrying that blob : 2
  TWIN SET (excluding the stray)   : 1

  1. sha256 equal to a twin       PASS   both 8e8b3264805c9dee92d4bd9ad79ba62e56f1f404175d9a60d82ae9d1b1cdec7c
  2. twin tracked                 PASS
  3. twin's blob on origin        PASS   origin/v12-v1-census -> e65eff1e…
  4. worktree == that blob        PASS   worktree = index = origin
```

**A fifth check of my own — not part of the ratified four — fired, and I adjudicated it rather than
letting it pass silently.** I asked whether the stray was cited anywhere by its distinct `_1` name.
Three hits: `LEDGER_ATHENA.md:777`, and the 08-18 and 08-22 build documents. **All three are
narrative** — two are historical records of the finding (which keep their citations under the
history rule) and the third is the PENDING item this session closes. **None is a functional
dependency**, so I proceeded. Stating it because it was a judgment, not a pass.

**Survivor re-verified after the removal** (08-12 precedent: re-verify the twin): 3,857 B, sha256
`8e8b3264…`, blob `e65eff1e…`, tracked, on origin. The removed content is recoverable verbatim from
commit `55ab89b`. **Box: `exchange/` 101 → 100 files.**

**Its rider, F-4, is untouched and now in its third session.** `RULES_OF_RECORD_VIZ_IRON_2026-08-15.md`
(mtime 22:40:26) records ruling F-1 declaring the VIZ-3 contract ABSENT; that contract sits on the
bus with mtime 22:47:32 — **7 minutes 6 seconds later**. Both publish. APOLLO's and yours to
reconcile; nothing operational turns on it.

---

## 7 · PROOF

| check | result |
|---|---|
| **`~/naiad-sail` exists?** | **No — `No such file or directory`.** D-0 halted before any code, as specified |
| files written by the thirteen agents | **zero** — every agent was read-only by instruction |
| queue 008 modified this session | **only the D-0 execution record** (§9); no deliverable text amended while the gate is open |
| **suite** | **334 passed, 1 skipped, 0 failed** |
| **F-CONV** | **4/4 PASS** |
| **F-ROT** | **7/7 PASS** |
| **F-MB-1** | **8/8 PASS** |
| `rotate_reports.py --dry-run` | **exit 0** |
| workflow | 13 agents · 0 errors · 0 empty results · 635 tool calls · 1,779,455 tokens · 30 min |

**Queue counters, and they moved for a reason that is not mine.** `queue_ratified_unbuilt` reads
**4**, up from the 3 I left this morning. `exchange/queue/2026-08-22_RF1_rangefinder_ARGUS.md` was
filed by **ARGUS at 04:52 today, while this session was running** — RF-1, SS12-RangeFinder,
operator-ratified by firing, `BUILT: PENDING`. It is a properly stamped work order and it belongs on
the bus, so it rides this publish. **Named because it is not this session's work** and because a
backlog counter that moves without explanation is the defect the 08-22 stamps existed to close.

---

## 8 · FILE DISPOSITION

Constants read from `publish_exchange`: `BOX_BYTES = 16,000,000`, `FLAG_BYTES = 64,000`.

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `exchange/queue/008_sail-skeleton.md` | yes | tracked | this publish | yes | GitHub + `--workflow` | 64,058 B + the D-0 record — **over the 64,000 B wire before this session touched it** |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-22_D0-CONFIRMATION-GATE.md` *(this document)* | yes | tracked (new) | this publish | yes | GitHub + `--workflow` | printed by the publish below |
| `exchange/status/LEDGER_ATHENA.md` | yes | tracked | this publish | yes | GitHub + `--workflow` | + this session's entry — **over the wire (append-only)** |
| ~~`exchange/reports/DESIGN_CONTRACT_VIZ4_EMA_MANTLE_2026-08-15_1.md`~~ | **removed** | **was tracked** | removal in this publish | yes | its byte-identical twin, tracked + pushed + recoverable from `55ab89b` | **−3,857 B off the box** |
| `exchange/queue/2026-08-22_RF1_rangefinder_ARGUS.md` | yes | untracked → tracked by this publish | this publish | yes | GitHub + `--workflow` | **ARGUS's file, not this session's** — 3,539 B |
| `~/naiad-sail` | **no** | — | — | — | — | n/a — **D-0 halted; nothing was founded** |

---

## 9 · THE D-0 EXECUTION RECORD

D-0 requires the outcome to be *"recorded in this file with its date"*. **The outcome is not yet
available** — it is your six answers. What is recorded in `008_sail-skeleton.md` today is that the
gate **RAN**, what it produced, and that it is **OPEN pending your word**. The answers get appended
beneath it, dated, when they arrive. I have not recorded a confirmation, because none has been given.

---

## 10 · WHAT REMAINS OPEN

| # | item | owner | state |
|--:|---|---|---|
| 1 | **The six questions of §1** | **operator** | **OPEN — D-0 does not close until each has a dated answer** |
| 2 | ~~VIZ-4 byte-identical twin~~ | — | **CLOSED** this session (§6) |
| 3 | The ~20 citation amendments | HEPHAESTUS | Held deliberately until the gate closes (§3) |
| 4 | D-0's own four defects | HEPHAESTUS / ATHENA | §4; repair proposed in §5, not made |
| 5 | Ruling F-1 vs the VIZ-3 contract on the bus | **APOLLO** | Untouched, **third session running** |
| 6 | `v3_scorer.py:393` still writes its packet to the root | operator | Carried from 2026-08-22 |
| 7 | Packet zips unprotected in `research_outputs/packets/` | operator / ATHENA | Carried |
| 8 | RF-1 (SS12-RangeFinder), ratified today, `BUILT: PENDING` | **HEPHAESTUS** | New backlog, ARGUS-drafted, not started |

## 11 · THE HONEST NEXT OPTIONS

1. **Answer ❶ alone and stop.** Everything else in the funnel is downstream of whether SAIL is built
   now or after APOLLO's export. *For:* one word unblocks or defers the whole contract. *Against:*
   ❺ is free and removes a real trap, so answering two costs no more than one.
2. **Answer all six, then let me make the ~20 amendments and re-verify.** *For:* closes D-0 in one
   more round-trip and the contract stops being a document nobody has checked. *Against:* the six
   are not trivial; ❷ in particular asks you to drop a deliverable.
3. **Build RF-1 instead.** It is ratified, unbuilt, and blocked on nothing. *For:* SAIL is blocked on
   your rulings either way; RF-1 is not. *Against:* it is display-only work while the out-of-sample
   instrument waits.

---

## 12 · SESSION CLOSE

```
=== STATUS_HEPHAESTUS — 2026-08-22 — QUEUE 008 D-0 ===
NOW: D-0 executed. NOTHING BUILT — ~/naiad-sail does not exist and no deliverable text was
amended while the gate is open. Thirteen read-only agents verified the derived content against
the estate: all eleven sections came back DEFECTIVE, 139 findings, 32 blocking. I re-checked the
eight most consequential by hand; all eight held. The funnel put to the operator is SIX questions,
not the ninety-two items the verification produced. VIZ-4 twin closed.
LAST EVENT: 2026-08-22 — one commit, one publish carrying the D-0 execution record, this report,
and the VIZ-4 removal.
FACTS:
- TWO DEFECTS ARE THE 2026-08-18 CLASS AGAIN — a citation that does not say what the contract
  claims. (1) D-5 says "Fills at close per card law"; card law says the stop exits AT the stop,
  ADVERSE-FIRST (tierc4_rules.py:242-244, tierc6.py:281). (2) F-SAIL-6 names the parity reference
  as "CARD_V6 executed through scripts/tierc5.py"; grep -c trail_min_advance_atr scripts/tierc5.py
  = 0, so v6 through tierc5 silently drops the card's F-C4-d trail rule and would generate parity
  vectors that are NOT card v6 — the vectors every later build is certified against [verified]
- THE PREREQUISITE FORK IS FALSE. Branch (b) builds a provisional spec "from the union in D-2a",
  but reference_trades is in D-2a-prime, F-SAIL-6 assigns their generation to APOLLO, and a spec
  missing them HALTS under D-9a. Branch (b) produces a spec that stops SAIL at launch and cannot
  meet criterion 4. It is not a slower path; it is not a path [verified]
- D-7's FIRST CLIENT IS ALREADY REFUTED. tierc6_lab_limit.py:91-98: "THE FORM IS FALSIFIED
  IN-SAMPLE BY ITS OWN CLAUSE (c) ... +0.0013 R/campaign while a single campaign's delta is forty
  times the whole sum." The contract treats it as an open question and says this nowhere [verified]
- REGISTER 2 IS MALFORMED. `belled` is defined once (tierc2_rules.py:134-135), re-exported twice,
  and read by NO funnel builder. And `belled` is one terminal disposition where `exited` is the
  union, so it is not a naming choice. A rider: D-8's exit list contains "bell", which is never
  written — tierc6.py:291-298 writes bell_12_89 or bell_89_316 [verified]
- THE GATE CONTRADICTS THE STAMP. 008:3 ratifies "D-4 (strengthened)"; 008:5 and 008:160 put
  "D-1..D-8" — which contains D-4 — as PENDING. D-4 is in both sets [verified]
- THE FUNNEL AS PRODUCED WAS NOT A FUNNEL. 92 items ordered by document number, ~20 of them
  citation corrections rather than decisions, and the one question D-0 names FIRST — the card-spec
  fork — was never asked by any of the eleven. Reduced to six ordered questions; the ~20
  corrections are mine to make and are named, not asked [verified]
- F-SAIL-7 CANNOT PASS: its `sk-` credential pattern matches risk-free / risk-normalized /
  risk-mode / disk-sleep in 26 tracked files [verified]
- CLEARED, and recorded because negatives matter: D-2a's 22-field card union IS correct and
  complete against the fixture enumeration at tierc6_fixtures.py:225-226 — the exact list the
  2026-08-18 session got wrong twice [verified]
- VIZ-4 twin removed on the four-check gate, all four PASS; a fifth check of my own fired on three
  citations, all adjudicated narrative-historical; survivor re-verified byte-identical [verified]
- suite 334/1 · F-CONV 4/4 · F-ROT 7/7 · F-MB-1 8/8 · rotate --dry-run exit 0 [verified]
- NOT MINE: ARGUS filed exchange/queue/2026-08-22_RF1_rangefinder_ARGUS.md at 04:52 mid-session,
  ratified by firing, BUILT: PENDING. queue_ratified_unbuilt 3 -> 4 for that reason [verified]
PENDING (operator):
1. THE SIX QUESTIONS in the report's section 1 — D-0 does not close until each has a dated answer
2. Question 1 alone unblocks or defers everything else; question 5 is one word and removes a trap
3. Ruling F-1 vs the VIZ-3 contract on the bus (APOLLO) — third session running
4. CARRIED: v3_scorer.py's root packet write; the unprotected packet zips
NEXT: your answers to the six, or build RF-1, which is ratified and blocked on nothing.
Owner: operator, then HEPHAESTUS.
METRICS: operator actions this session = 0 · files re-ingested = 0 · deliverables built = 0 ·
verification agents = 13 · findings raised = 139 (32 blocking) · findings re-verified by hand = 8
(8 held) · questions put to the operator = 6
=== END STATUS ===
```

**BRIGHT COLOURS — the six questions, and the two that matter most.**

**❶ The card-spec fork.** Wait for APOLLO's export **(a)**, or start now on a provisional spec —
except **branch (b) as written does not work**, and the amended version asks me to write both the
exam and the answer key. *Recommend **(a)**, or **(c)** drop the parity check from the skeleton if
the export is far off.*

**❺ Is D-4 ratified or pending?** Your stamp says ratified; the gate sweeps it back in. *One word.
Recommend **RATIFIED**.*

The other four — ❷ the validator's refuted first client · ❸ what L-LIMIT-2 needs you to name ·
❹ `exited` vs `belled` · ❻ eighteen untested sub-deliverables — are in §1 of
`exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-22_D0-CONFIRMATION-GATE.md`, each self-contained,
each with the option of dropping it.

**Nothing was built. `~/naiad-sail` does not exist. The gate held.**
