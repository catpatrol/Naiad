# BUILDERS REPORT — HEPHAESTUS · QUEUE 008 FILED
## The SAIL skeleton, multi-setup form — contract drafted, adversarially reviewed, twenty blocking defects fixed before filing

**Lane:** HEPHAESTUS under ATHENA custody · **Commissioning paste:** operator, 2026-08-18
(diagram: nucleus + plug/unplug sockets) · **Executed:** 2026-08-18
**Artifact:** `exchange/queue/008_sail-skeleton.md` · **FILED, not built.** No code was written.

**It is FILED, not AMENDED** — the paste allowed for either. Enumerated, not assumed: no `008` file
existed in the tree, `find . -iname "*008*"` returned nothing outside `.git`,
`git log --all -- exchange/queue/` showed no 008 at any commit, and `grep -rn "F-SAIL"` across every
`.md` returned nothing. **So the "prior D-1..D-8 and F-SAIL-1..7" the paste says "stand" had never
been written, and I authored them from BRIEF §§1,3,4,5,6,7.** That is the single most important
thing in this report, and the contract says it in its own first paragraph.

---

## 1 · THE HEADLINE — the review caught a defect that would have traded a measured loss

I drafted the contract, then ran four independent adversarial reviewers against it: citation
accuracy, coverage against the commissioning paste, house-law compliance, and
executability/fixture-falsifiability. **Verdicts: SHIP-WITH-FIXES · SHIP-WITH-FIXES · DO-NOT-SHIP ·
DO-NOT-SHIP. 81 defects, 20 of them blocking.** Every blocking finding was verified by hand against
the source before I acted on it. All are fixed.

**THE WORST ONE, AND IT IS WORTH THE WHOLE REVIEW:** my D-2a instructed the builder to write
`WALL_EXIT_ATR = 0.25` into `card_spec_v6.json` as one of card v6's eight register rows.

> **0.25 IS THE REGISTER'S VALUE. IT IS NOT THE CARD'S.** `CARD_V6 = Card()`
> (`scripts/tierc6_rules.py:220`) leaves `wall_exit_atr = None`. The field's own default says so —
> `wall_exit_atr: float | None = None  # P-WALL-1 sets 0.25` (`:216`) — the register row's ruling
> field says `"P-WALL-1 (registered, not carded)"` (`:151`), and the engine states it in code at
> `scripts/tierc6.py:317-319`: *"Registered, NOT carded: the card v6 leaves `wall_exit_atr = None`
> and this branch is dead on every scored card row."*
>
> The 0.25 cell is a **separate arm** — `RC.Card(name="v6+wall", grid="P-WALL-1",
> wall_exit_atr=0.25)` (`scripts/tierc6.py:1171`) — **and it FAILED: −0.0331 R, *"the wall exit
> costs money, and it is the clearest negative result in the build"***
> (`BUILD_2026-08-16_TIERC6_REVB.md:17`).

**A builder following my first draft would have shipped setup #1 with a wall exit card v6 does not
have, carrying a measured loss, into the estate's only remaining out-of-sample instrument** — and
the same paragraph of my own draft warned that an incomplete spec "will trade differently from v6".
I verified all of it by hand (`sed -n '205,222p'`, `'148,158p'`) before fixing it.

**The second blocking citation defect, same paragraph:** my two-list enumeration of the card's
fields **omitted `harvest_frac` (0.5 — the de-risk rule) and `wall_tf` ("12h")**. Both are
v6-*declared*, so they appear in no register row and are excluded by "inherits unretyped from V5".
The authoritative enumeration is a fixture, not prose — `scripts/tierc6_fixtures.py:225-226` gives
exactly six declared fields. **A spec built to my first list could not express the harvest fraction.**

---

## 2 · THE TWENTY BLOCKING DEFECTS, AND WHAT EACH BECAME

| # | defect in my draft | fix now in the contract |
|---|---|---|
| 1 | `WALL_EXIT_ATR 0.25` written as card v6's value | register-vs-card table; **card value is `null`**; the −0.0331 R result named |
| 2 | `harvest_frac` and `wall_tf` missing from the field enumeration | the fixture's six-field declared set cited as authority; completeness test is `dataclasses.fields(RC.Card)` |
| 3 | **"four fires per UTC day"** for a 4h-close heartbeat | **SIX** (00/04/08/12/16/20 UTC). 24 ÷ 4 = 6. My arithmetic was simply wrong |
| 4 | launchd schedule stated as if directly expressible | `StartCalendarInterval` has **no timezone field** (`M4-LAUNCHD.md:899-902`); machine is UTC−3. Installer regenerates local hours; wrapper asserts UTC proximity at run time; `StartInterval` forbidden |
| 5 | "spec sha ≠ pinned sha" with **no definition of the sha** | D-2b′: SHA-256 over bytes with the `sha` field excluded, canonical JSON; **recomputed from disk, never the self-declared field**; pinned value lives only in the enable-list — fact vs claim, never claim vs claim |
| 6 | Enable-list had **no path and no format** — yet "unparseable → HALT" was a criterion | `<sail-root>/setups/enable_list.json`, three keys exactly, unrecognised key = unparseable; specs at `setups/specs/` |
| 7 | **Funding required by BRIEF §4, no source anywhere.** The lift list has none (`grep -i funding` on the inventory = zero hits) | `engine/data.py:349 backfill_funding` / `/fapi/v1/fundingRate`, consumed per `tierc2_baseline.py:216`. Gap policy applies; **`funding_resolved` boolean; no implicit zero**, because `FUNDING_CEILING_R` 1.0 is a live rule |
| 8 | Wake order demanded "step by step" and **never named** | card v6's, verbatim: **STOP → BELL → TIME STOP → HARVEST → WALL → ADDS → TRAIL** (`tierc6.py:176-178`). `engine/trading.py` named as the *incident's* engine, not the spec. `fixtures/test_s2_sim.py` named as the executable precedent |
| 9 | F-SAIL-1 had **no target set and no predicate** → expected-zero self-fulfilling | target glob (with non-empty assertion) + a pinned predicate + **the ruled gate-body boundary** + a required red leg |
| 10 | F-SAIL-6 **could not be executed** — "the Naiad reference implementation" is undefined, three trades unnamed, and SAIL cannot import Naiad | D-2a′: **three `reference_trades` vectors travel inside the spec**; reference of record named; **missing block is a HALT, not a skip** |
| 11 | D-4d (order routing absent) had **no fixture and no criterion** | **F-SAIL-9 · NO ORDER PATH EXISTS**, with a required red leg; stubs explicitly caught |
| 12 | D-1's whole ops spine had **no fixture** | **F-SAIL-10**, four legs — and leg 1 fires on day one, since `/Volumes` holds only `Macintosh HD` |
| 13 | Verdict list closed at eight; **F-SAIL-7 mapped to no criterion** | criteria 9–13 added; **"any single fixture failure is a REJECT"** |
| 14 | **D-7 (the validator) appeared in no criterion** — the skeleton could be DONE with F-C6-c's cure absent | criterion 13: the validator has printed at least one row |
| 15 | D-7c claimed the interdict lifts when the row prints | **two locks.** `tierc6_lab_limit.py:228-236` lifts only when the operator names **instrument, corridor edges and card version** — not among DEC-1..5. REGISTER item 8 |
| 16 | **Unqualified `RATIFIED` stamp over content the document itself called underived** | stamp scoped to what the operator actually stamped; **D-0 CONFIRMATION GATE halts before any code** |
| 17 | Drafting-rights rule crossed without naming it | `queue/README.md` §4/§5 quoted; the collapse of commissioning and verifying into one hand named; cost paid by D-0 |
| 18 | **Criteria 1 and 4 require a card-spec that does not exist**, and BRIEF §8 exports it *after* this skeleton | PREREQUISITE block under the stamp: ruling (a) or (b), REGISTER item 7. **The builder does not choose** |
| 19 | F-SAIL-8's behavioural half was **vacuous** — two `no_signal` streams would go green | toy spec must differ *behaviourally*; must hold state on an asset setup #1 holds (exercises D-4e); "body file" defined by glob |
| 20 | F-SAIL-5's determinism set **unnamed** → trivially passable | pinned offline fixture cache; artifact set named; wall-clock exemptions disclosed per `SEQ8.md:93` |

**Majors and minors also applied:** funnel leak-column identity and the v6 terminal-reason set
(`time_stop`/`wall` expected **zero** — nonzero is a spec defect); per-slot funnels beside the
aggregate; the hook contract signatures; the journal schema written out (the 51-field `ReplayTrade`
is the *53-side*; the 22 is the projection, and the projection is the defect); D15 count corrected
**eleven → twelve** of fifteen; `K_GRID`/`FRONTIER_ARMS`/`LIM2_M` line numbers **:143/:144/:145 →
:145/:146/:147**; the elided *"PAIRED, because…"* sentence restored to the H-LIM-2 quote and the
ASCII `x` restored; `the_form`'s **tie-break-to-smaller-k** added; the `query_filter` citation
**:24 → :28-29**; Prometheus citations branch-qualified to `origin/phase-5-birth-on … @ f88e133`;
the `origin/` ref form documented because DEC-3 deletes the clone; and two of my own enumerations
in §1 corrected — both, as it happens, in the safe direction.

---

## 3 · WHAT THE CONTRACT CONTAINS

**DEC-1..DEC-5** — the five ratified decisions, recorded because a decision living only in a chat
message is one the next session cannot cite. **DEC-4 closes an open item rather than restating one:**
`tf_govern` is a **spec constant**, which `LEDGER_ATHENA.md` pending item 5 carried as undecided.

**D-0..D-9** — D-0 the confirmation gate; D-1 repo + ops spine; D-2 the card-spec handshake;
D-3 the feed; **D-4 the setup registry (strengthened: N slots, per-slot sha / enable flag /
`setup_id` on every row / own funnel section, per-slot spec-fed hooks, routing absent-not-stubbed,
state namespaced)**; D-5 paper execution; D-6 state + wake order; D-7 the validator;
D-8 the weekly; **D-9 the enable-list (new)**.

**F-SAIL-1..10** — the law grep, sha refusal, heartbeat, weekly renders, determinism, parity,
no-keys, **the modularity proof (new)**, **no order path (new)**, **the ops spine (new)**.

**Thirteen verdict criteria**, any single fixture failure a REJECT. **Eight REGISTER items**,
including the operator's `"SDK?"` — `[open]`, owner APOLLO, define-or-retire, **nothing built
against it** — and the two new blockers (items 7 and 8).

**Three separate "D" numberings were in play and would have collided:** the paste's decisions
(D1–D5), this contract's deliverables (D-1..D-9), and the brief's *"the operator's nucleus, D3"*
(`BRIEF_ATHENA_SAIL_REPO_2026-08-17.md:33`). Disambiguated with a table; the diagram's **D3 is this
contract's D-4**. Decisions renamed **DEC-n** so a bare cite cannot go wrong.

---

## 4 · FINDINGS REPORTED-NOT-FIXED

1. **The card-spec does not exist, and BRIEF §8 orders it after this skeleton.** Verdict criteria 1
   and 4 cannot be met until the operator rules (a) export-first or (b) provisional-spec.
   **This blocks execution, not filing.** REGISTER item 7.
2. **L-LIMIT-2's interdict needs an operator naming act** — instrument, corridor edges, card version
   — that is not among the five ratified decisions. The validator's first row does not lift it.
   REGISTER item 8.
3. **The funnel's sixth stage is unresolved:** BRIEF §5 says `exited`, `scripts/tierc2_rules.py:132-135`
   says `belled`. Not synonyms — `belled` is one terminal disposition, `exited` the union.
   REGISTER item 2; D-8(2) holds until ruled.
4. **`CADENCE.md` is stale by four rows** — seven `com.naiad.*` agents armed, three registered;
   `grep -ni oracle` on it returns nothing. Named by D-1c and REGISTER item 4. **Not fixed here** —
   it is ATHENA's file and outside this contract.
5. **Naiad's `ci.yml:21` runs `pytest fixtures/` only**, so `tests/` never executes on push and
   F-BOX-1/F-BH-1 do not run in CI. Named so SAIL is not born with the same shape. Not fixed.
6. **Queue numbering jumps 004 → 008.** Rulings 005–007 were issued and executed without numbered
   queue files. 008 is the operator's allocation and is consistent with the *ruling* sequence.
   Flagged, not back-filled.

## 4.1 · Deviations

- **HEPHAESTUS drafted a queue contract.** `queue/README.md` §4 reserves drafting to APOLLO, ATHENA
  and ARGUS; §5 makes HEPHAESTUS the executor. The operator's live instruction outranks the file
  (§0 precedence), so the filing is authorised — **but commissioning and verifying collapsed into
  one hand, and D-0 exists to pay that cost.** Named in the contract, not papered over.
- **The contract is 64,058 B — 58 B OVER the 64,000 B naming trip-wire.** Flagged by name here per
  §3.2, with its intended home: `exchange/queue/008_sail-skeleton.md`, on the bus, permanently.
  **I did not trim content to get under the wire.** The wire *names*, it does not refuse; and the
  house rule on re-pinning is explicit that deleting law to satisfy a number is the failure mode the
  mechanism exists to prevent. Twenty blocking fixes are what put it over.
- **The paste said "file … with them integrated" as though D-1..D-8 existed.** They did not. I
  authored them and marked them PENDING CONFIRMATION rather than presenting derivation as ratified.

---

## 5 · METHOD

Two workflows, nine agents, zero errors. **Research (5 agents):** card v6 · F-C6-c and L-LIMIT-2 ·
the yardstick vocabulary · ops patterns · fixture conventions — 814,126 tokens, 364 tool calls.
**Adversarial review (4 agents):** citations · paste coverage · house law · executability —
570,082 tokens, 221 tool calls. Transcripts (local, not on the bus):
`~/.claude/projects/-Users-luis-Naiad/8f241ae7-8b32-4a9b-8e89-cb3656a5d59b/subagents/workflows/wf_350c3d3f-074/`
and `…/wf_1d05d657-651/`.

**Every blocking finding was verified by hand against the source before I acted on it** — the wall
value, the declared-field set, the funding fetcher, the wake order, and `fixtures/test_s2_sim.py`.
The reviewers were right on all of them. **Defects found in my own work: 20 blocking + 61 lesser.
Fixed: all blocking, and every major and minor with a concrete correction.**

---

## 6 · FILE-DISPOSITION TABLE

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `exchange/queue/008_sail-skeleton.md` | yes | tracked (new) | see §7 | yes — `origin/v12-v1-census` | GitHub + estate zip | **64,058 B = 0.40% of box — ⚠ OVER the 64,000 B trip-wire by 58 B. FLAGGED by name; intended home is the bus, permanently.** The wire names, it never refuses |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-18_QUEUE-008-FILED.md` | yes | tracked (new) | see §7 | yes — `origin/v12-v1-census` | GitHub + estate zip | **15,610 B at creation = 0.10% of box — UNDER the 64,000 B wire, not flagged** |
| `exchange/status/LEDGER_ATHENA.md` | yes | tracked | see §7 | yes — `origin/v12-v1-census` | GitHub + estate zip | **110,389 B before this append — already over the wire.** Append-only file that grew across it; the named cost in §3.2 |

**Constants from `publish_exchange`, never a copy:** `BOX_BYTES = 16,000,000` · `FLAG_BYTES = 64,000`
· warn 0.40 / refuse 0.70 · `TICK_EXTRA = ('LEDGER.md',)`. Per §3.1 this file does not contain its
own sha256; it is verified before and after the publish and printed on screen.
**Nothing was created, modified or moved in Prometheus or its quarantine clone this session.**

## 7 · PUBLISH RECORD

**ONE commit + publish**, per the paste, carrying the contract, this report and the ledger append.
Invocation is §3.4's exact form; status, SHA, push result, offenders and box figures are printed on
screen and relayed in the closing block. The STATUS block is appended to
`exchange/status/LEDGER_ATHENA.md` in this same session per Invariant 4.

— HEPHAESTUS · **the contract is filed and it is honest about what it is.** The registry has N
sockets and one card; the enable-list is the operator's channel and the only one; and the wall that
would have cost money is `null`, where card v6 left it.
