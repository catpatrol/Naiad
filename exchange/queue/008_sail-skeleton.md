# 008 · The SAIL skeleton — MULTI-SETUP FORM (the nucleus and its sockets)

RATIFIED: **operator, 2026-08-18 — for DEC-1..DEC-5, D-4 (strengthened), D-9, F-SAIL-8 and the
REGISTER addition ONLY.** The filing paste is the ratifying act: *"Running this paste ratifies
D1-D4 … and D5."* **D-1..D-8 and F-SAIL-1..7, 9, 10 are HEPHAESTUS's derivation under BRIEF
§§1,3,4,5,6,7 and are PENDING CONFIRMATION — see D-0, which HALTS before any code.**
Drafted: **the operator**, via the 2026-08-18 diagram (nucleus + plug/unplug sockets) and the
filing paste; **transcribed and specified by HEPHAESTUS** under ATHENA custody.
Executor: **HEPHAESTUS**. Specification by reference to
`exchange/reports/BRIEF_ATHENA_SAIL_REPO_2026-08-17.md` §§1, 3, 4, 5, 6, 7.

BUILT: PENDING

> **PREREQUISITE, AND IT IS NOT OPTIONAL.** Verdict criteria 1 and 4 require a real
> `card_spec_v6.json`. **It does not exist** — `card_spec`, `spec_sha`, `export_card` return zero
> hits across every `.py`/`.json`/`.yaml` in Naiad — and BRIEF §8 places its export *after* this
> skeleton (*"Your inventory + skeleton → my card-spec export paste → first heartbeat"*). A builder
> reaching criterion 1 has nothing to import. **Ruling required before execution (REGISTER item 7):**
> either **(a)** APOLLO's export paste lands first and this contract runs after it, or **(b)**
> HEPHAESTUS authors a PROVISIONAL `card_spec_v6.json` mechanically from the union in D-2a, labelled
> `provisional: true`, and criteria 1 and 4 are met against it — **with the standing consequence,
> stated now, that APOLLO's authoritative export re-pins every slot and re-runs F-SAIL-2 and
> F-SAIL-6.** Whichever branch is ruled, it is named here before the builder starts. **The builder
> does not choose.**

---

## ⚠ READ THIS FIRST — THREE THINGS THIS FILING IS NOT

**1 · THERE WAS NO EARLIER FILING. This is fresh, and D-1..D-8 / F-SAIL-1..7 are AUTHORED HERE, not
recovered.** The paste says *"If `exchange/queue/008_sail-skeleton.md` ALREADY exists from the
earlier filing: AMEND it … else file fresh with them integrated"*, and instructs that *"All prior
deliverables D-1..D-8, fixtures F-SAIL-1..7, verdict criteria, and boundaries stand."* **They did
not exist.** Enumerated, not assumed: `exchange/queue/` holds `001`–`004` and six dated named
contracts and nothing else; `find . -iname "*008*"` returns nothing outside `.git`;
`grep -rln "F-SAIL\|sail-skeleton"` across every `.md` in the repo returns **only this file** —
the inventory report contains no `F-SAIL` hit at all. `git log --all -- exchange/queue/` shows no 008 at any commit.
**So D-1..D-8 and F-SAIL-1..7 below are HEPHAESTUS's derivation from BRIEF §§1,3,4,5,6,7 — not a
transcription of an operator-approved list.** They inherit the brief's authority, not a prior
stamp. **D-0 turns that from a hope into a gate.** D-4 (strengthened), D-9, F-SAIL-8 and the
register addition are the operator's own words and carry his stamp directly.

**THE RULE THIS FILING STANDS OUTSIDE, NAMED RATHER THAN PAPERED OVER.** `exchange/queue/README.md`
§4 gives queue drafting rights to **APOLLO, ATHENA and ARGUS**; §5 says *"HEPHAESTUS executes
ratified items only; an item without the operator's stamp is a request, not work."* **This contract
is transcribed by HEPHAESTUS, who will also execute it — commissioning and verifying collapse into
one hand, which is the separation the rule exists to keep.** The operator's live instruction
outranks the file (CONVENTIONS §0 precedence), so the filing is authorised; **the cost is real and
is paid by D-0**, which puts the derived content back to the operator before any code is written.

**2 · THREE SEPARATE "D" NUMBERINGS ARE IN PLAY. They are not the same series and must never be
cited bare.** This has already caused one near-collision in drafting:

| series | written as | meaning | authority |
|---|---|---|---|
| **RATIFIED DECISIONS** | **DEC-1 … DEC-5** | the five things this paste ratifies (the paste calls them "D1-D4" and "D5") | operator, 2026-08-18 |
| **DELIVERABLES** | **D-1 … D-9** | what the builder must produce | this contract |
| **the operator's diagram** | **"D3, the nucleus"** | the setup-registry element in the 2026-08-18 diagram, cited in `BRIEF_ATHENA_SAIL_REPO_2026-08-17.md:33` | operator's diagram |

**The diagram's D3 is this contract's D-4.** Renaming the decisions to `DEC-n` is a drafting choice
made to prevent a mis-cite; the operator's own labels are preserved in the table above.

**3 · QUEUE NUMBERING: 005-007 HAVE NO FILES, AND THAT IS PRE-EXISTING.** `exchange/queue/` jumps
`004` → `008`. Rulings 005, 006 and 007 were issued and executed without numbered queue files
(005 = the launchd/M4 migration, `CADENCE.md:17`; 007 = DIGEST retired / HERMES dormant,
`CONVENTIONS.md:4,112`). `008` is the number the operator allocated and it is consistent with the
**ruling** sequence. The queue README's "ascending, never reused" is satisfied. **Flagged, not
fixed** — back-filling 005-007 is not this contract's business.

---

## THE FIVE RATIFIED DECISIONS (DEC-1 … DEC-5)

Running the filing paste ratified these. They are law for this contract and are recorded here
because a decision that lives only in a chat message is a decision the next session cannot cite.

**DEC-1 · FOUND.** `naiad-sail` is founded as a new minimal repo. Prometheus is **not** retrofitted.
Basis: the step-1 inventory, `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-17_SAIL-STEP1-INVENTORY.md`
— three NO / zero YES against BRIEF §2's three questions, plus a CLEAN secrets history.

**DEC-2 · THE OLD AGENT SAILS UNTIL FIRST HEARTBEAT.** The Prometheus paper agent
(`.github/workflows/paper.yml`, hourly, committing to the orphan `paper-data` branch — running
continuously since 2026-07-08) **keeps running** until SAIL's first heartbeat lands. Then it is
disposed of by a separate operator word. **Rationale, recorded:** it is the estate's only accruing
live out-of-sample record, it costs nothing, and destroying it is irreversible. **Consequence the
builder must honour: Prometheus stays READ-ONLY. Nothing in this contract touches it** — not the
workflow, not the branch, not a file. Its disposition is item 3 in `LEDGER_ATHENA.md`'s pending list.

**DEC-3 · THE QUARANTINE CLONE IS DELETED AT CLOSE.** `~/prometheus-inventory` — the read-only
census clone with its push URL broken — is **removed at the end of the session that finishes the
lifting**, not before. It is outside `~/Naiad`, outside every sync tree, and unbacked-up by design;
re-cloning takes seconds. **The lift (D-3) reads from it; the close deletes it.** Deleting it before
the lift is complete is a defect, and so is leaving it behind.

**DEC-4 · `tf_govern` IS A SPEC CONSTANT, NOT A CONFIG KNOB.** The governing-timeframe constant
lives **in the card-spec** (BRIEF §3) and travels with the card's sha. It is **not** a YAML knob in
SAIL's config. **This closes an open item, and closing it is the decision — not a restatement of
one:** `LEDGER_ATHENA.md` pending item 5 and the inventory's §9 both carried it as undecided
("a strategy decision wearing a config costume"). It is decided now: **spec constant.**
*Why it matters concretely:* in Prometheus the equivalent key (`config.py:29 tf_govern="1h"`) is
what silently blocks 4h — `resample.py:119-121` requires `interval_ms(tf_govern) % interval_ms(tf) == 0`,
so five of eleven intervals raise before a bar is evaluated. A constant that can change the meaning
of a gate belongs to the brain. **Changing it is therefore a card version bump with a new sha, and
it runs `CONVENTIONS.md:661-678` §6.4, the named-constant change protocol — all three legs.**

**DEC-5 · MULTI-SETUP REGISTRY FROM BIRTH — and selection is a ruling, never a body decision.**
Three clauses, all binding:
 (i) SAIL is built as an **N-slot setup registry from the first commit**, not as a one-card harness
     later generalised. Setup #1 occupies slot 1; slots 2..N exist and are empty.
 (ii) **Which setups are live is an OPERATOR RULING**, expressed as the enable-list (D-9) and
     journaled when it changes. SAIL never decides for itself which setup to run.
 (iii) **Any future automatic selector — weather-based, regime-based, performance-based — is a
     RATIFIED META-CARD arriving through the same spec handshake (D-2). It is NEVER body logic.**
     A selector implemented in SAIL's own code is the same defect class as a strategy conditional
     in the body: it is a brain, and BRIEF §1 says the body has none. **This is out of scope by
     law, not by omission**, and D-9 and F-SAIL-1 make it mechanical.

---

## Why this exists

Two forces made SAIL structural, and they are independent — either alone would justify the build.

**The seal is open, so the estate has no out-of-sample left.** By explicit operator ruling all
history is in-sample. Card v6's headline — **n=195 campaigns, +39.84 R, +0.2043 R per campaign,
p 0.074 against its own bar — is NOT statistically certified** and cannot be certified by more of
the same data (`HANDOFF_APOLLO_NAIAD_SUCCESSION_2026-08-17.md:10-17`;
`BUILD_2026-08-16_TIERC6_REVB.md:15,57`). **Live forward paper is now the only remaining
out-of-sample instrument in the estate**, and SAIL is where it lives.

**And F-C6-c is blocking, with a live publication interdict attached.** Verbatim,
`exchange/reports/BUILD_2026-08-16_TIERC6_REVB.md:297` §10:

> **F-C6-c · SAIL IS UNBOUND.** The pre-registered limit form has no validator. Zero hits
> estate-wide. **Blocking for L-LIMIT-2's (c).**

This is not a tidiness item. The pre-registration writes its own interdict into the module
constant — `scripts/tierc6_lab_limit.py:228-236` — which says the table **may not be published with
a validation clause until the operator names the instrument**. The lab's header records what it
could not build (`:109-112`): *"WHAT COULD NOT BE BUILT: the SAIL validation. 'SAIL' appears NOWHERE
in this estate (zero grep hits)."* **D-7 is the cure. Until D-7 runs, a filed pre-registration
stays unpublishable.**

**The concentration problem is the third reason, and it is why the registry is multi-setup from
birth.** ZEC is 81.7% of the book and one May-2026 campaign is +25.06 R of it, with no structural
why found by forensics. A single-setup harness would compound that concentration; a registry that
can carry paired and rival setups from day one can measure it.

---

## Deliverables

**Every deliverable below is subject to BRIEF §1, THE ONE LAW: *SAIL is a body, never a brain.* It
imports the ratified card and executes it; it re-implements nothing. If a rule cannot be imported,
the trade does not exist in SAIL. Any strategy logic found outside the imported spec is a defect by
definition.** F-SAIL-1 makes that mechanical.

### D-0 · THE CONFIRMATION GATE — **HALT before any code**

**Nothing below D-0 is executed until D-0 closes.** HEPHAESTUS puts **D-1..D-8 and F-SAIL-1..7, 9,
10** — the derived content, per the stamp — to the operator as a §1.1 decision-funnel: what each is ·
why it matters · every actionable option **including dropping it** · implications for and against.
He obtains a one-word confirmation or an amendment, and **records the outcome in this file with its
date**. The same gate carries the PREREQUISITE ruling (card-spec (a) or (b)) and REGISTER items 2
and 7, which block verdict criteria 1, 4 and D-8(2).

**Why this exists rather than a trust-the-reader note:** the earlier draft carried an unqualified
RATIFIED stamp over content it internally declared underived-from-any-stamp. A builder in a later
session, with no access to the drafting conversation, would have read the stamp and built seven of
nine deliverables that no operator approved. *"Veto any line"* addressed to an absent reader is not
a control. **A HALT is.**

### D-1 · Found `naiad-sail`, with the ops spine (BRIEF §6)

A new minimal repo at `~/naiad-sail` — **the name reserved and deliberately not used for the
quarantine clone** (`BUILDERS_REPORT_HEPHAESTUS_2026-08-17_SAIL-STEP1-INVENTORY.md:68`). GitHub is
the anchor; the repo itself is code and documents only.

**D-1a · Identity gate v2, adapted.** The two-sided gate at `exchange/status/CONVENTIONS.md:116-125`,
with the path side re-anchored on the SAIL repo root instead of `$HOME/Naiad`. **Both sides are
required and the reason is unchanged:** checking only the path passes a copy left in a cloud tree;
checking only for marker-absence passes any directory on the machine (CL-2). HALT on any of
`*OneDrive*`, `*com~apple~CloudDocs*`, `*Mobile Documents*`.

**D-1b · launchd, per the house pattern — copy the proven shape, do not invent one.**
Two agents: **heartbeat, 4h-close-aligned — SIX fires per UTC day, at 00:00 / 04:00 / 08:00 /
12:00 / 16:00 / 20:00 UTC** — and **the weekly report, Sunday**.
**⚠ THE SCHEDULE IS NOT DIRECTLY EXPRESSIBLE AND THE CONTRACT SAYS SO RATHER THAN LEAVING IT TO BE
DISCOVERED.** `launchd`'s `StartCalendarInterval` fires on **machine local wall-clock and has no
timezone field** (`BUILDERS_REPORT_HEPHAESTUS_2026-08-15_M4-LAUNCHD.md:899-902`); this machine runs
at UTC−3. **RULED:** the plist carries six local `Hour` entries computed from the machine's current
UTC offset, an installer script regenerates them, **and the wrapper asserts at run time that
`datetime.now(timezone.utc)` is within N minutes of a 4h boundary and journals the offset it fired
at — so a DST drift is REPORTED, never silent.** `StartInterval` is **forbidden**: it drifts from
bootstrap time and is not close-aligned.
*(The first draft of this line said "four fires per UTC day". 24/4 = 6. A builder who wrote four
would have made SAIL blind at two of every six 4h closes on a card whose lens IS 4h — a
trading-behaviour defect wearing a scheduling costume. Recorded because the arithmetic was wrong in
a ratified-looking document.)* Model: `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-15_M4-LAUNCHD.md`
(M4 of ruling 005), which carries three plists verbatim with their bootstrap lines, `launchctl print`
read-backs, forced-run proofs and undo lines. **Non-negotiable, and it is measured rather than
stylistic:** `ProgramArguments` uses the ABSOLUTE interpreter path and the ABSOLUTE script path — a
bare `"python"` made `daily_routine.py` abort at startup, and it does *not* reach the per-job error
path (`scripts/routine_jobs.json:3`). Label form `com.naiad-sail.<name>`, bootstrapped into `gui/501`.

**D-1c · REGISTER THE CADENCE ROWS. This is a deliverable, not paperwork.** Add a row per SAIL agent
to `exchange/status/CADENCE.md` (rows `:11-13` are the model). **Named reason:** seven `com.naiad.*`
agents are armed on this machine today and `CADENCE.md` documents three — `grep -ni oracle` on it
returns nothing while four `com.naiad.oracle-*` agents run. `CONVENTIONS.md:823` is stale the same
way. **Adding a SAIL agent without its row repeats a defect the estate already has.** Flagged here
as a finding against the existing registry; fixing the four Oracle rows is **not** in this contract's
scope, and is named for the operator in the REGISTER below.

**D-1d · Missed-while-asleep semantics, per the Mac-era note.** Report-only. Enumerate the missed
fires by name at the top of the next run's output; **no backfill, no catch-up execution.** Pairs
with D-6's wake-order note. A silent skip is indistinguishable from success
(`CONVENTIONS.md` §3.3).

**D-1e · Logging under `logs/launchd/`** per house pattern, one file per agent.

**D-1f · No keys anywhere, enforced by CI.** F-SAIL-7. **BRIEF §6's condition is already
structurally satisfied on the Prometheus side and must stay that way here** — the inventory proved
zero env-read sites of any form across 4,307 blobs and zero commits ever adding or removing one.
**But there is no Naiad precedent for the credential-grep CI itself: ABSENT** — searched `scripts/`,
`tests/`, `fixtures/`, `.github/workflows/`; the only hit is prose at
`.github/workflows/collector.yml:14`. **F-SAIL-7 is invented, not copied, and the contract says so
rather than implying a model exists.**

**D-1g · Backups.** The SAIL **journal is data** and follows the residency rules — LaCie mirror plus
Drive. The **repo** is GitHub. **Named condition the builder will hit:** `/Volumes/LaCie` was **NOT
MOUNTED** when the inventory ran. Per `CONVENTIONS.md` §2.1, `drive_wait` gates backup *writes*, not
substrate reads — so an absent drive must produce an **unwritable backup copy that is reported**, never
a halted heartbeat and never a silent skip.

**D-1h · Provenance headers.** Every file lifted from Prometheus carries a header naming source repo,
branch, path and commit sha. See D-3.

### D-2 · The card-spec handshake (BRIEF §3)

**THE CONTRACT IS SPECIFYING SOMETHING NEW. Enumerated, not assumed:** `card_spec`, `spec_sha`,
`card_sha`, `export_card` return **zero hits** across every `.py`/`.json`/`.yaml` in Naiad;
`find -name "*card_spec*"` returns zero files. The thirteen prose hits are all forward-looking
(the brief, the handoff, the two ledgers, last session's report). **There is no exporter to conform
to — SAIL defines the consumer side and APOLLO's export paste meets it.**

**D-2a · The spec object.** `card_spec_v<N>.json` carries: **constants · gate definitions by name ·
lens · panel · version · sha**. Setup #1 is **card v6**, whose canonical binding is
`scripts/tierc6_rules.py:220 CARD_V6 = Card()`.

**⚠ THE REGISTER IS NOT THE CARD, AND CONFLATING THEM SHIPS A MEASURED LOSS.** The eight register
rows (`scripts/tierc6_rules.py:121-190`) are the *rulings*; the card is `CARD_V6 = Card()`. They
differ on one field and it matters:

| register row | register value | **card v6's value** | authority |
|---|---|---|---|
| `TRAIL_ARM_AFTER_R` | 1.0 | 1.0 | `:124`, `:213` |
| `TRAIL_MIN_ADVANCE_ATR` | 0.05 | 0.05 | `:131`, `:214` |
| `TRAIL_OFFSET_ATR` | `STOP_BUF_ATR` = 0.5 | same | `:138` |
| `TRAIL_RAIL_ATR` | `MIN_STOP_ATR` = 1.0 | same | `:144` |
| **`WALL_EXIT_ATR`** | **0.25** | **`null` — NOT CARDED** | `:151`, `:216`, `:220` |
| `BELL_DISPOSITION` | "backstop" | same | `:157` |
| `FUNDING_CEILING_R` | 1.0 | same | `:173` |
| `YARDSTICK` | "full_corridor_expectancy_of_the_current_card" | same | `:182` |

**`WALL_EXIT_ATR` IS REGISTERED, NOT CARDED.** The register row's own ruling field says so —
`"P-WALL-1 (registered, not carded)"` (`:151`) — the field default is `wall_exit_atr: float | None =
None  # P-WALL-1 sets 0.25` (`:216`), and the engine states it in code at `scripts/tierc6.py:317-319`:
*"Registered, NOT carded: the card v6 leaves `wall_exit_atr = None` and this branch is dead on every
scored card row."* The 0.25 cell is a **separate arm**, `RC.Card(name="v6+wall", grid="P-WALL-1",
wall_exit_atr=0.25)` (`scripts/tierc6.py:1171`), **and it FAILED: −0.0331 R, *"the wall exit costs
money, and it is the clearest negative result in the build"*** (`BUILD_2026-08-16_TIERC6_REVB.md:17`).
**The spec must be able to EXPRESS the field; setup #1's value is `null`. Writing 0.25 builds a
losing rule into the estate's only out-of-sample instrument.**

**THE AUTHORITATIVE ENUMERATION OF WHAT v6 DECLARES IS A FIXTURE, NOT A PROSE LIST** —
`scripts/tierc6_fixtures.py:225-226`: `{name, trail_arm_after_r, trail_min_advance_atr,
harvest_frac, wall_exit_atr, wall_tf}`. **Six fields, and two of them appear in no register row:**
`harvest_frac` (= `HARVEST_FRACTION`, **0.5** — the de-risk rule, `scripts/tierc4_rules.py:163-164`)
and `wall_tf` (**"12h"**). **A spec built from the register alone cannot express the harvest
fraction.**

**Everything else arrives from `V5.Card` unretyped (`scripts/tierc5_rules.py:287-320`) and is
equally part of the card**: `grid` · `entry_rail_atr` · `lane` · `limit_ae_mult` · `trail` ·
`trail_l`/`trail_r` (2/2) · `trail_extra_buf_atr` · `harvest`/`harvest_fixed_r`/`harvest_min_unit_r` ·
`time_stop_bars` · `funding_ceiling_r` · `adds_max`/`add_size` · `seal_open`.
**The spec's completeness test is mechanical: it must reproduce `dataclasses.fields(RC.Card)` in
full. A spec carrying only the eight register rows is an incomplete card and will trade differently
from v6.**

`lens` is `"4h"` (`scripts/tierc2_rules.py:62-65`); `panel` is the standing five,
`("BTCUSDT","ETHUSDT","SOLUSDT","NEARUSDT","ZECUSDT")` (`scripts/tierc2_rules.py:56-60`).
**`tf_govern` is carried here, per DEC-4.**

**D-2a′ · The spec also carries `reference_trades`: exactly THREE frozen parity vectors.** For each:
the input bars (symbol, interval, `open_time` range), the card fields consulted, and the expected
outputs (entry px, stop, every trail advance, exit px, net R) — all pinned under the spec's sha.
**SAIL never reaches into the Naiad repo; the vectors travel in the artifact** (BRIEF §3 forbids a
submodule, and SAIL is a separate repo — a fixture cannot import Naiad). A spec whose
`reference_trades` block is missing or has ≠3 entries is a **HALT** under D-9a, never a skipped
check. This is what makes F-SAIL-6 executable.

**D-2b · Artifact copy, pinned sha, no submodule.** SAIL pins the sha it runs and **prints it in
every journal row and every report header** (BRIEF §3). **SAIL refuses to start if spec sha ≠ pinned
sha** — fail-loud. F-SAIL-2.

**D-2b′ · THE SHA IS DEFINED HERE, because APOLLO's exporter must meet it.**
`spec_sha` = **SHA-256 over the spec file's bytes with the `sha` field itself excluded**, serialised
as UTF-8 JSON with `sort_keys=True`, `separators=(",",":")`, no trailing newline. **SAIL RECOMPUTES
it from the bytes on disk at every start and never trusts the file's self-declared `sha` field** —
a manifest checking itself is not a check, the same principle F-SAIL-5 applies to determinism. **The
slot's PINNED sha lives in the enable-list's `spec_sha` column and nowhere else**, so the start-up
check is **RECOMPUTED-vs-PINNED — a fact against a claim, never claim-vs-claim.**

**D-2c · Per-slot pinning.** Each registry slot pins **its own** spec sha independently (D-4). One
setup's re-pin must not silently re-pin another's.

**D-2d · Reuse the drift-proof config precedent.** `configs/tierc2_paper.yaml` already solves
"config that cannot drift from the code it configures", declaring `config_id` and `executor` and
explaining in its own header why the generic engine cannot consume it. **Copy that discipline.**

### D-3 · The feed (BRIEF §2's lift list; the panel at 4h + 1h)

Lift by copy with provenance headers, per the twelve-item list at
`BUILDERS_REPORT_HEPHAESTUS_2026-08-17_SAIL-STEP1-INVENTORY.md` §7.2. **Reads come from the
quarantine clone, which DEC-3 deletes at close.** The load-bearing items:

- **Binance USD-M klines client** — `main:src/prometheus/data/binance.py` @ `b4d11e6`, keeping the
  closed-bar rule (`:88-89`), pagination (`:62-80`) and 4 retries / 5 attempts (`:40`, `:107-121`).
  It is the correct market: `fapi.binance.com` (`:20-21`), corroborated by `README.md:25-27`.
- **THE GAP POLICY — lift the policy, and wire it where Prometheus did not.**
  `phase-5-birth-on:src/prometheus/data/binance_archive.py:249-265` @ `f88e133`:
  **DETECT → DROP THE WHOLE WINDOW → RECORD. Never forward-fill, never interpolate.** Prometheus
  enforced this only on its archive/OOS path; **its live path has no gap detection at all**, and a
  missing candle passes through silently. **SAIL's live path gets it. That is BRIEF §2(b)'s answer
  and it is the single most valuable thing in the lift list.**
- **Resampler and its divisibility guard** — `resample.py:40,48,93,119-121`. **Lift the guard
  knowingly:** it is what blocks 4h in Prometheus, and under DEC-4 the constant that drives it now
  lives in the spec.
- Checksum-verified archive loading (`binance_archive.py:118-144`) · injected-fetcher cache
  (`cache.py:27-43`) · indicator primitives (`indicators.py:19-91`) · the offline `MockTransport`
  test pattern (`tests/conftest.py:1`, `test_data_layer.py:42-43`).
- **FUNDING — the source is named here, because BRIEF §4 requires funding journaled and THE
  PROMETHEUS LIFT LIST HAS NONE.** Enumerated per Invariant 7: `grep -i funding` over
  `BUILDERS_REPORT_HEPHAESTUS_2026-08-17_SAIL-STEP1-INVENTORY.md` returns **zero hits**. Lift the
  shape from **Naiad's own** fetcher instead: `engine/data.py:349` `backfill_funding` — *"Funding
  rate history via REST (1000/page). Cached like klines."* — against `/fapi/v1/fundingRate`
  (`engine/data.py:359`), with the consumption shape at `scripts/tierc2_baseline.py:216`
  `load_funding` (`funding_time` → `funding_rate`). **The DETECT → DROP → RECORD gap policy applies
  to the funding series exactly as to klines: a campaign spanning a missing funding interval is
  journaled with its funding marked UNRESOLVED, never with an implicit zero.** Zero funding is not
  cosmetic — card v6 carries `FUNDING_CEILING_R` 1.0, a cap taken on the chain total, so an implicit
  zero silently disables a live rule.

**REF FORM IN THE QUARANTINE CLONE, stated because DEC-3 deletes it and an unresolvable address is
unrecoverable later:** the clone was made `--no-checkout` with only `main` checked out, so unmerged
branches resolve as `origin/<branch>`. Read them as `git show origin/phase-5-birth-on:<path>`; the
bare `phase-5-birth-on:<path>` form errors with `invalid object name`.

**Both 4h and 1h must be reachable for all five panel assets.** BRIEF §5's report and card v6's lens
are 4h; 1h is carried because the brief names it. **NOTHING from `skills/`, `birth_filter.py`,
`pyramid_signals.py`, or `replay.py`'s `_lifecycle`/`build_entries` bodies — that is the brain.**

### D-4 · THE SETUP REGISTRY — the nucleus **(STRENGTHENED, operator 2026-08-18)**

**THE SHELL IS A REGISTRY, NOT A CARD-HOLDER.** This supersedes any reading of BRIEF §4 in which the
shell holds one card. The brief already names it *"the setup-registry interface (the operator's
nucleus, D3)"* (`BRIEF_ATHENA_SAIL_REPO_2026-08-17.md:33`); DEC-5 makes N-slot structure a birth
requirement rather than a later generalisation.

**D-4a · N slots.** Each slot is one imported card-spec with:
  1. **its own pinned sha** (D-2c);
  2. **its own enable flag** in the operator-ratified enable-list (D-9);
  3. **its own journal attribution — `setup_id` on EVERY row**, without exception, including
     "no signal" rows;
  4. **its own funnel section in the weekly, beside the aggregate** (D-8).

**D-4b · The hooks are PER-SLOT and SPEC-FED: `admit / enter / manage / exit`.** Each hook reads its
behaviour from that slot's spec. **No hook may contain a strategy conditional** — F-SAIL-1.

**THE HOOK CONTRACT, stated so that a second setup cannot require a new signature** — F-SAIL-8's
whole premise is decided by this interface, so it is specified here rather than authored by the
builder who then writes the fixture that validates it. Each hook takes `(slot_state, spec, frame,
bar_i)` and returns a value object: `admit → bool` · `enter → EntrySignal | None` ·
`manage → StateDelta` · `exit → ExitDecision | None`. **A hook receives no global state and mutates
nothing outside its own `slot_state`.** Copy the SHAPE from the inventory's §7.2 item 9
(`main:src/prometheus/replay.py:34-51, :69-82, :416-435` @ `b4d11e6`, proven by
`tests/test_phase3b_fixtures.py:180-182`) — **do NOT import the module.**
**The test of the interface is that a rule of a NEW SHAPE can be expressed in the spec without a new
hook.** That is precisely what Prometheus could not do, and it is what F-SAIL-8 exists to catch.

**D-4c · Setup #1 = card v6.** The operator's slot label is **"Anchor / Neot"**. **Recorded honestly:
"Anchor / Neot" and "the 4H winner" are the operator's names and are NOT filed estate terms** —
`grep -rni "4h winner"` returns one unrelated hit (`BUILD_2026-08-14_CENSUS2B_PARTA_WTB1.md:822`,
"t+24h winners") and the case-sensitive form returns zero, and there is no lens bake-off anywhere in Tier-C
(the 4h lens is *ruled*, `scripts/tierc2_rules.py:62-65`, not won). The nearest filed basis for
"Anchor" is `BUILD_2026-08-15_TIERC3_RAILED.md:50` — *"moving the structural anchor from the 1H lens
to the system's own 4h lens is worth +16.41 R"* — and finding F-C3-b (`:316`), *"the object a
multiplier must beat is the 4h-anchor card."* **The slot label is the operator's; the binding
identity is `scripts/tierc6_rules.py:220`. The contract binds to the code, and carries the label as
a label.**

**D-4d · ORDER ROUTING IS ABSENT, NOT STUBBED.** The module that would talk to an exchange **does
not exist**. Not a stub, not a no-op, not a flag set to false. **A stub is a thing that can be
switched on; absence is not.** BRIEF §4.

**D-4e · State persistence is NAMESPACED PER SETUP.** Positions, trail levels and the window registry
are per-slot. Two enabled setups may hold simultaneous state on the same asset without either
seeing the other's. Cross-setup interaction (netting, shared risk budget, correlation limits) is
**explicitly out of scope** — see boundaries.

### D-5 · The paper execution layer (BRIEF §4)

**Journal-only.** Fills at close per card law. **10 bps plus funding journaled from venue data.**
No order routing (D-4d). Lift the three operational invariants earned in live weather —
stop-guarantee, single-position, circuit breaker (`phase-5-birth-on:src/prometheus/paper.py:85-88,
:90-93, :123-126` @ `f88e133`) — **adapted to per-slot state under D-4e.**

**Journal schema — specified, not gestured at.** The prior art is
`main:src/prometheus/replay.py:86-142` @ `b4d11e6`, the **51-field `ReplayTrade` dataclass** — that
is the *53-side* of the loss, not the 22-side. The 22 columns are a **projection applied at write
time** by `main:src/prometheus/harness/replay_report.py` @ `b4d11e6`. **That projection is the
defect** (`Prometheus_Data_Collection_Design.md:17`): about 33 already-computed fields are discarded
at the moment the trade is written. **SAIL persists the full computed record, not a projection.**

SAIL's row is every field of the slot's ride result — entry/stop/exit indices, prices and reasons,
`r_dist`, `net_r`, MFE/MAE in R and ATR, bars held, fees paid, harvest and add legs — **plus, on
EVERY row without exception including `no_signal` rows: `setup_id`, `spec_sha`, `card_version`,
`bar_open_time_ms`, `symbol`, `direction`** — **plus `funding_cum` and the boolean
`funding_resolved`** (D-3). **A row whose funding is unresolved may not be aggregated into the D-8
expectancy; it is counted and named instead.** One JSONL row per evaluation per slot. Adding a
column is additive-only; removing one is a schema version bump.

### D-6 · State persistence and the wake-order note (BRIEF §4)

Positions, trail levels and the window registry persist across restarts.

**D-6a · A WAKE-ORDER FIDELITY NOTE IS A DELIVERABLE, and the estate has been burned — cite the
precedent.** The incident is **RC-7 HALT 2, 2026-07-19**, recorded verbatim at
`RC7_Amendment_2.md:9-10` and in the evidence ledger at `LEDGER.md:303-306`. Root cause, verbatim:

> *"the candidate simulator's bar-event ordering is not the engine's wake order. Three faces, one
> defect: fill-bar coverage (halt 1), tie chronology (the 60), death-bar flatten precedence (this).
> **Ordering defects are fixed by ordering, not by conventions.**"*

The concrete failure: a trail sat inside a death bar's range and the pinned simulator priced an
intra-bar exit of −0.1961 R **the engine could never take**, because the wake flattens at the open
before the intra-bar check. **SAIL's note must state its wake order explicitly, step by step, and
F-SAIL-3 must exercise it** — because "fixed by ordering, not by conventions" means a prose
assurance is not a fix.

**AND THE ORDER IS NAMED HERE, because Naiad holds TWO non-identical ones and a builder would have
to pick.** SAIL's binding within-bar order is **card v6's**, verbatim from `scripts/tierc6.py:176-178`:

> **STOP → BELL → TIME STOP → HARVEST → WALL → ADDS → TRAIL** — *adverse-first throughout*,

with the trail **last** because its result governs bar *j+1*. `engine/trading.py:3-14` is the
RC-7-era engine's five-step wake — **it is the engine the HALT-2 incident was measured on, and it is
NOT SAIL's**; it is cited above as the incident, never as the specification.
**The executable precedent the brief means by "S-2" is `fixtures/test_s2_sim.py`** — synthetic legs
pinning each ordering fix *independently* (fill-bar coverage; death-bar flatten precedence), plus
`c141t213` as a permanent named regression that must price **+0.0739 R** forever. **F-SAIL-3's
wake-order leg is built in that shape: one synthetic leg per ordering decision, each able to go red
on its own.** Lift the inventory's §7.2 item 12 (`origin/phase-5-birth-on:src/prometheus/paper_live.py:38-40,
:58, :119` @ `f88e133`) for the rolling-window merge-by-key that keeps the live path
wake-order-faithful across missed fires.

### D-7 · THE VALIDATOR — F-C6-c's cure (BRIEF §4)

A **standing job** that scores every pre-registered form the Naiad lane exports, on SAIL's
accumulating live book — **out-of-sample by construction** — and prints its verdict row in the
weekly with **n-so-far**.

**D-7a · First client: L-LIMIT-2.** The form is already filed and frozen above every function that
could compute a result — `scripts/tierc6_lab_limit.py:203` `LIM2_PREREG`. The validator must
implement the claim at `:218-227` **as written**:

> *"H-LIM-2: on the out-of-sample instrument, arm A entered at offset k\*(A) x ATR(14) at the trigger
> bar posts a per-campaign expectancy in R strictly greater than the same instrument's
> market-trigger card, measured by the asset-cluster bootstrap of the PAIRED per-campaign delta
> (cluster_boot / cluster_boot_diff, 4000 draws, seed 20260816, stat='mean', unit of replication =
> ASSET), 90% two-sided interval excluding zero above, BH-corrected at m = the number of tests
> actually run in that family. PAIRED, because the arm cannot change which campaigns exist — it
> rides inside the card's own offered set."*

**And the SELECTION RULE is a second frozen text the validator must also honour** —
`LIM2_PREREG["the_form"]`, `scripts/tierc6_lab_limit.py:208-217`: `k*` is *"argmax over k … taken
SEPARATELY within each arm A"*, **ties broken by the SMALLER k**, and *"THE FRONTIER IS A FORM, NOT
A NUMBER: k\*(A) is whatever the table says it is, and this text is fixed before the table exists."*
**Expectancy is denominated in the OFFERED SET** — misses counted at their true value (0.0 for
FULL-LIMIT, half a card for SPLIT-ENTRY) — *"because a limit that never fills earns nothing and no
one can spend a per-fill expectancy."*

Parameterisation: `limit_px = entry_px − direction × k × atr_at_entry` (`:917-933`), **k an absolute
ATR(14) multiple**, `K_GRID = (0.10,0.20,0.30,0.40,0.50)` (`:145`),
`FRONTIER_ARMS = ("FULL-LIMIT","SPLIT-ENTRY")` (`:146`),
`LIM2_M = len(K_GRID) * len(FRONTIER_ARMS)` = 10 (`:147`).
**Reproduce all of it — the claim, the form, the tie-break and the denominator — or the validator is
scoring a different object.**

**D-7b · Generic by construction.** L-LIMIT-2 is the *first* client, not the only one. The validator
takes a registered form and returns a verdict row; adding a second form is data, not code.
**Downstream this is where `query_filter`'s registered predicates land** (*"mine → pre-register →
SAIL-validate; only registered predicates ever gate"*, `HANDOFF_APOLLO_NAIAD_SUCCESSION_2026-08-17.md:28-29`).

**D-7c · TWO LOCKS, NOT ONE — AND ONLY ONE IS IN THIS CONTRACT'S GIFT.**
`scripts/tierc6_lab_limit.py:228-236` lifts the interdict only when **the operator names the
instrument, its corridor edges and its card version.** **That act has not happened and is not among
DEC-1..DEC-5.** So: D-7 delivers the validator and its first printed row, and **the row does not
lift the interdict by itself.** The builder's deliverable is to produce the three facts the operator
needs — instrument = SAIL · corridor edges = SAIL's first heartbeat timestamp to the reporting
close · card version = v6 at its pinned spec sha — and put them to him as a §1.1 funnel.
**Rebinding `LIM2_PREREG["the_instrument"]` is a Naiad-side edit to a FROZEN pre-registration, runs
§6.4's three legs, and is NOT this contract's to make.** (The same passage warns why the shortcut is
barred: binding SAIL to the Prometheus paper route *"would validate v6's entry rule on v1's
entries"* — F-C5-k, named and not taken.) REGISTER item 8.

**D-7d · n-so-far is printed always, verdict only when n permits.** An underpowered verdict printed
as a verdict is the failure the pre-registration exists to prevent.

### D-8 · The weekly report, in yardstick format (BRIEF §5)

Every week, containing exactly:

1. **Expectancy-to-date vs the labeled bar.** The bar is **+0.2043 R per campaign, full-corridor,
   PROVISIONAL** — card v6's own full-corridor expectancy (`BUILD_2026-08-16_TIERC6_REVB.md:15,57`).
   **Units are R per CAMPAIGN. Not per bar, not per day, not percent.** It is PROVISIONAL because
   p = 0.074 against its own bar — not certified — and because the count moves: TC6-V restated
   2,534 → 2,535 days and 195 → 196 campaigns one day later
   (`BUILD_2026-08-17_TC6V_TIERC7.md:39`). **Print the bar with its provenance and its p-value, never
   bare.**
2. **The funnel.** BRIEF §5 names `armings seen → tide → d → triggered → entered → exited`.
   **⚠ THE LAST STAGE DOES NOT EXIST IN THE ESTATE AND THE BUILDER MUST NOT INVENT IT SILENTLY.**
   The authoritative constant is `scripts/tierc2_rules.py:132-135`:
   `FUNNEL_STAGES = ("armings_seen","passed_tide","passed_d","triggered","entered","belled")`.
   **The brief's sixth stage is `exited`; the code's sixth stage is `belled`.** They are not
   synonyms — `belled` is one terminal disposition, `exited` is the union of all of them.
   **Ruling required (REGISTER item 2).** Until ruled, SAIL emits the five agreed stages plus a
   terminal breakdown, and **labels the sixth column with whichever name the ruling gives it.**
   The funnel is a **cumulative partition**: each column is a subset of the one before, so `leak_*`
   columns are exact differences and the rows must reconcile — fixture-enforced upstream at
   `scripts/tierc4_fixtures.py:1401-1420`. **SAIL inherits that reconciliation requirement, and it
   is made executable rather than gestured at: SAIL's leak columns are one per gate the spec
   declares, named `leak_<gate>`, and the identity `stage[k] == stage[k-1] - leak[k]` holds for
   every k, asserted by fixture** (F-SAIL-4). **The terminal breakdown enumerates card v6's exit
   reasons from source** — `corridor_end`, `stop`, `bell`, `time_stop`, `wall`
   (`scripts/tierc6.py:223, :281, :298, :305, :323`) — **with `time_stop` and `wall` expected ZERO
   on setup #1, because `time_stop_bars` and `wall_exit_atr` are both `None` on card v6. A nonzero
   count in either is a SPEC DEFECT and must be reported as one, not absorbed.** Terminal counts sum
   to `entered` minus still-open.
   **One funnel per enabled slot, beside the aggregate** (D-4a(4)); the aggregate equals the sum of
   the per-slot funnels.
   Stage definitions are pinned: an **arming** is one 12/89 cross in one direction
   (`tierc2_rules.py:231-236`); **tide** is `e89>e316 AND close>e316` on 4h at the arming bar
   (`tierc2_rules.py:28,315-319`) — **both clauses load-bearing**, TC7-i found a gate missing the
   second and `F-C7C-TIDE` proves it bites on 1.6 M bars (`BUILD_2026-08-18_TC7C_TC8.md:59`).
3. **Per-asset and equal-risk aggregations, side by side.**
4. **D15 diagnostic columns.** Single implementation of record: `scripts/tierc5.py:579-622`.
   **D15 is the ONLY fully anchored D-item in the estate** (twelve of fifteen have no source at all,
   `DEFINITIONS_D_H_2026-08-16.md:53,36-52`) — so cite D15 and only D15, and cite the code.
   **The operator's ruling is verbatim and binding: `scripts/tierc5_rules.py:143-147` — "D15 caveats
   not hard gates". THE COLUMNS RIDE EVERY LINE AND GATE NOTHING.** A SAIL build in which a D15
   column gates anything is in breach. *(Graduation is a separate future ruling: "D15 returns from
   diagnostics to law at money.")*
5. **LOAO-3/5, once n permits.** `scripts/tierc7.py:623-718`. **5 = the five panel assets, one panel
   per asset dropped. The bar is 3 of 5 and it was named before the look.** It is **not** a
   significance threshold and must not be printed as one — *"an arm that clears its CI and fails 3/5
   has not been refuted; it has been shown to rest on one asset, which is a different fact and is
   reported as one."* This exists because **ZEC is 82% of the book and dropping it flips every arm.**
6. **The validator rows** (D-7), with n-so-far.
7. **The drift sentinel:** the card-spec sha **per slot**, plus a weekly recompute of **three fixture
   trades** against the Naiad reference implementation — parity check, **fail-loud on mismatch**
   (F-SAIL-6).

**Renders from an empty journal and from a synthetic one** (F-SAIL-4). **Box discipline: the report
is lean; the journal is referenced by pointer, never copied into `exchange/`** (Invariant 3 —
documents are cheap, data is not).

### D-9 · THE ENABLE-LIST **(NEW, operator 2026-08-18)**

**A tiny ratified file that SAIL refuses to start without.** Three columns and nothing else:

    setup_id  →  spec sha  →  enabled

**PATH AND FORMAT, NAMED — because the operator edits this file by hand as a ruling and an
unspecified interface is not a channel.** The file is **`<sail-root>/setups/enable_list.json`** — a
JSON array of objects with exactly the keys `setup_id` (string), `spec_sha` (64 hex chars) and
`enabled` (bool), **and no others; an unrecognised key makes the file unparseable under D-9a.**
Card-specs are mirrored to **`<sail-root>/setups/specs/card_spec_v<N>.json`**. **Both paths are part
of the contract, not the builder's discretion.**

**D-9a · Refusal is fail-loud and specific.** Missing file, unparseable file, a `setup_id` with no
registered slot, or a sha that does not match the slot's pinned sha → **HALT with the reason named**.
Never a default, never an empty-list fallback, never "assume all disabled and continue". A silent
skip is indistinguishable from success.

**D-9b · Changing it is an OPERATOR RULING, and the change is JOURNALED.** Enabling or disabling a
setup writes a journal row recording what changed, when, and to which shas. **The enable-list is the
only channel by which the live setup set changes.**

**D-9c · WEATHER-BASED AUTO-SELECTION IS OUT OF SCOPE BY LAW, NOT BY OMISSION — and this contract
says so.** Per DEC-5(iii), any future automatic selector must arrive as a **ratified meta-card
through the spec handshake (D-2)**. **A selector written into SAIL's body is a defect of the same
class as a strategy conditional, and F-SAIL-1 must catch it.** *Rationale, recorded so a later
session cannot mistake this for an oversight:* a body that chooses its own brain has become one.

---

## Fixtures — HALT loudly on any failure

**House form, and it is not decorative.** Each fixture prints its evidence lines, records
`[OK ]`/`[BAD]` per leg, and closes with a **`FAILS IF:`** line stating its own failure condition in
words. **Every leg runs — a fixture must not stop at the first failure**, so the transcript is
complete. **A fixture that raises is recorded as a FAILING fixture, never as an error that hides one**
(`scripts/seq8_fixtures.py:371-374`, `scripts/oracle_fixtures.py:729-734`). The harness returns 1 on
any red via `raise SystemExit(main())`, and prints the banner used unchanged across the estate:

    *** HALT: fixture mismatch. Nothing downstream is trustworthy. ***

**A missing prerequisite HALTS before any leg runs, loudly and by name** (`HALT: …`).

**PLACEMENT IS A CONTRACT DECISION AND IT IS MADE HERE: F-SAIL-1..8 live where SAIL's own CI runs
them, and the SAIL CI workflow must be written to reach them.** Named reason, measured in Naiad:
`.github/workflows/ci.yml:21` runs `python -m pytest fixtures/ -v` and **nothing else**, so
everything under `tests/` — including F-BOX-1 and F-BH-1 — **never executes on push**. That gap is a
standing open item in two ledgers. **SAIL must not be born with it.** F-SAIL-8 checks the CI reaches
every F-SAIL leg.

---

**F-SAIL-1 · THE LAW GREP — zero strategy conditionals outside the imported spec.** BRIEF §7(5).
**MUST BE AN AST / TOKEN SCAN OVER CODE, NEVER A RAW TEXT GREP** — the estate has diagnosed the raw
scan twice: a comment *explaining why* a field was renamed away from a tape-column name was itself
flagged (`scripts/tierc4_fixtures.py:78-106`, `code_only()`), and the known-weak survivor is recorded
reported-not-fixed at `BUILD_2026-08-16_TIERC4_MEANCARD.md:379`. **Use `code_only()`'s approach:
strip comments and docstrings, KEEP ordinary string literals** (a subscript like `tape["wall_family"]`
is a real consultation and a scan that dropped it would be weaker, not cleaner).
Models: **F-C7-CLOSURE** (`scripts/tierc7_fixtures.py:583-614`) for the idiom, **F-F3**
(`tests/test_forward0.py:150-207`) for the CI shape.
**THE ANTI-VACUITY CLAUSE IS MANDATORY**, and it is the part contracts forget: a law grep over an
empty or mis-globbed file set returns zero and goes green. F-F3's answer is the model — assert the
scan can still SEE real code, and that the prohibition is still STATED in the prose it was stripped
from. **Additional required leg per DEC-5(iii): the scan must also catch a SETUP SELECTOR in the
body, not only an entry/exit conditional.**
**THE TARGET SET AND THE PREDICATE ARE PINNED HERE, not left to the builder** — otherwise he authors
both and the expected-zero is self-fulfilling. Both cited models are fully pinned and that is why
they work: F-C7-CLOSURE scans a hard-coded module list for a hard-coded token set
(`scripts/tierc7_fixtures.py:586-591`); F-F3 scans one named file against a pre-declared
`BANNED_STATS` tuple (`tests/test_forward0.py:150-157`).
 · **TARGET:** every `.py` under `<sail>/src/` except `<sail>/src/spec/` (the loader) and
   `<sail>/fixtures/`, enumerated by glob **with the glob's non-empty result asserted**.
 · **PREDICATE**, over `code_only()` output: (i) any `if`/`elif`/ternary/`match` whose test carries
   a numeric literal other than 0, 1 or −1; (ii) any occurrence, in a conditional test, of the
   pinned identifier list `{e89, e316, e12, atr, tide, d, displacement, trigger, arm, harvest,
   trail, wall, bell, funding, seal, setup, select, regime, weather}` **not reached through a
   `spec[...]` / `slot.spec.` subscript.**
 · **THE BOUNDARY, RULED** (D-2a says the spec carries "gate definitions by name", which would
   otherwise leave gate BODIES in SAIL as an unruled grey zone): **a gate body may live in SAIL only
   if every threshold, direction and enable it consults is read from the slot's spec at call time.
   A gate body holding its own literal is a brain.**
 · **REQUIRED RED LEG:** a planted conditional (e.g. `if atr > 1.5:`) in a body file must be
   reported. **A fixture that has never been seen to fail is a fixture nobody has tested.**
**Expected zero, and the expected-zero is the fixture.**
FAILS IF: any decision lives in the body rather than in an imported spec — including a selector that
chooses among setups.

**F-SAIL-2 · SPEC-SHA REFUSAL.** SAIL refuses to start when a slot's spec sha ≠ its pinned sha, and
when the enable-list names a sha that matches no slot. **Per slot, independently.**
FAILS IF: SAIL starts on a drifted spec, or a mismatch is reported as a warning rather than a refusal.

**F-SAIL-3 · ONE HEARTBEAT, END TO END.** BRIEF §7(1). Importing the card-spec, producing a journal
row **or an honest "no signal" row**, with the spec sha printed and `setup_id` attributed. **Must
exercise the D-6a wake order explicitly** — ordering defects are fixed by ordering, not by
conventions.
FAILS IF: a tick produces no row at all (silence is not an answer), or a row omits its sha or its
`setup_id`.

**F-SAIL-4 · THE WEEKLY RENDERS TWICE.** BRIEF §7(2). From an **empty** journal and from a
**synthetic** one. The empty case is the load-bearing one: a report that only renders once there is
data cannot be trusted the first week.
FAILS IF: either render raises, or the empty render fabricates a figure instead of printing an
honest zero/n-a.

**F-SAIL-5 · DETERMINISM.** BRIEF §7(3): same inputs, two runs, one hash. **Inherits
`CONVENTIONS.md:518-526` §4.4 R3 and its D-3 refinement, which self-executes ("Every study contract
inherits this clause") — print BOTH digests in the build document, delete the rerun's DATA in the
same session, and RETAIN its run manifests and logs.** Two-level check per house standard: compare
the build's own claimed shas **and** independently re-hash the files on disk — a manifest-only
comparison is a claim checking itself (`scripts/tierc7_fixtures.py:649-684`). **Any normalisation
must be disclosed, not assumed** (`BUILDERS_REPORT_HEPHAESTUS_2026-08-04_SEQ8.md:93`).
**THE DETERMINISM SET IS NAMED HERE** — an unnamed set lets the builder pick one with no timestamps
in it, and F-SAIL-5 then passes trivially. Two runs **over a PINNED OFFLINE FIXTURE CACHE** (no
network — the `MockTransport` pattern; "same inputs" cannot mean live venue data, which moves) must
produce byte-identical `journal/*.jsonl`, per-slot `state/*.json`, and the rendered weekly.
**Exempt fields, disclosed not assumed: the run's wall-clock stamp and elapsed time**, compared as a
named exclusion in the manner of `BUILDERS_REPORT_HEPHAESTUS_2026-08-04_SEQ8.md:93`. Launchd logs
are outside the set.
FAILS IF: a second run writes a different byte, or a normalisation is applied without being named.

**F-SAIL-6 · PARITY ON THREE REFERENCE TRADES.** BRIEF §7(4) and §5's drift sentinel.
**⚠ THE BRIEF'S WORDING IS NOT EXECUTABLE AS WRITTEN AND THIS FIXTURE RESOLVES IT.** "The Naiad
reference implementation" appears nowhere in the estate outside the brief; three candidates differ
materially; **and SAIL is a separate repo that BRIEF §3 forbids from submoduling Naiad, so a SAIL
fixture cannot import it.** Hence D-2a′: **the three parity vectors travel INSIDE the spec.**
**The fixture:** recompute the three `reference_trades` vectors carried by **each enabled slot's**
spec and compare field by field to their pinned expected outputs — entry px, stop, every trail
advance, exit px, net R. **The reference implementation of record is `scripts/tierc6_rules.py:220
CARD_V6` executed through `scripts/tierc5.py`; APOLLO's export paste generates the vectors from it
and states which three campaigns they are.**
**This fixture must NOT be skippable.** Naiad's own parity fixture skips itself when its pack is
absent (`fixtures/test_f6_parity.py`) — a shape that certifies nothing on the likeliest build. **A
missing `reference_trades` block is a HALT (D-9a), never a skip.**
FAILS IF: SAIL and the pinned vectors disagree on any field of any of the three — which would mean
the body has re-implemented the brain, the exact hazard BRIEF §1 exists to cure.
FAILS IF: the block is absent and the fixture reports green.

**F-SAIL-7 · NO KEYS ANYWHERE.** BRIEF §6. CI greps for credential patterns and **fails on any hit**.
**No Naiad precedent exists — this one is invented.** Cover at minimum: `api_key`, `apikey`,
`secret`, `token`, `bearer`, `password`, `credential`, `private_key`, `BEGIN … PRIVATE KEY`, `AKIA`,
`ghp_`, `github_pat`, `sk-`, `xoxb-`, `X-MBX-APIKEY`, `hmac`, wallet/mnemonic/seed-phrase shapes,
`.env` and credential-shaped filenames, **and any env-read site at all** (`os.environ`, `os.getenv`,
`dotenv`, `process.env`) — since paper needs none and their presence alone signals a credential path.
**⚠ THE ALLOWLIST TRAP, learned the hard way:** F-CONV-1's first version asserted a token appeared
nowhere else in the repo and *"failed twice within an hour of being written"* because it punished
legitimate citation (`scripts/fixtures_conventions.py:145-157`). **SAIL's own prose about not having
keys must not trip its own grep.** Declare the exemption list in code with the rule for what may
enter it, as F-CONV-1 does.
**One forward-looking constraint recorded here because it is pre-written in prose SAIL might lift:**
`[phase-5-birth-on] docs/runbooks/paper_trading.md:231-233` describes an optional testnet order mode
that would need a wallet private key in an env var. **No implementing code exists. Lifting that
runbook lifts a §6 violation.**
FAILS IF: any credential pattern or env-read site appears in SAIL, on any branch.

**F-SAIL-8 · THE MODULARITY PROOF (NEW, operator 2026-08-18).** **Registering a synthetic second
setup requires ZERO body-code edits.** Proven by fixture, mechanically:
  1. a **toy spec** is dropped in. **IT MUST DIFFER FROM SETUP #1 IN A WAY THAT CHANGES BEHAVIOUR,
     not merely in name** — a different `lens` or a different gate threshold — **such that on the
     same fixture window it enters at least one campaign setup #1 does not, AND at least one
     campaign on an asset setup #1 is simultaneously holding.** *(Without this, the cheapest passing
     toy spec is one whose gates never admit: two streams of `no_signal` rows and two all-zero
     funnels go green and prove only that the enable-list parses.)* The second clause is what
     exercises **D-4e**: the fixture asserts the two slots' state files are **disjoint** and neither
     slot's position count is visible to the other;
  2. **one enable-list row** is added;
  3. the journal shows **correctly-attributed rows from BOTH setups** (`setup_id` distinct, per-slot
     shas distinct);
  4. the weekly **renders both funnels** beside the aggregate.
**IT FAILS IF ANY ENGINE FILE NEEDED TOUCHING.** Prove that mechanically, not by inspection: capture
the sha256 of every body file before and after the registration and assert the set is unchanged.
**"Body file" means every `.py` under `<sail>/src/`, enumerated by glob with the glob's non-empty
result asserted, excluding `<sail>/config/` and `<sail>/setups/`.** Also assert both setups' entered
counts are nonzero and unequal, and that the aggregate funnel equals the sum of the two per-slot
funnels.
**This fixture is the whole of DEC-5 made falsifiable, and it is the one that would have caught
Prometheus** — where adding one entry set and one admission gate each required editing `src/`
(`origin/phase-5-birth-on:src/prometheus/replay.py:32-36` and
`origin/phase-5-birth-on:src/prometheus/skills/birth_filter.py:318-327`, both @ `f88e133` — note
the second lives inside `skills/`, the directory D-3 forbids lifting from).
FAILS IF: a body file's sha changes, or either setup's rows are unattributed or missing.
**Additional leg:** SAIL's CI actually executes F-SAIL-1..8 — see the placement note above.

**F-SAIL-9 · NO ORDER PATH EXISTS (new — closing D-4d's enforcement gap).** D-4d is the phase's
defining safety boundary and had no fixture: **F-SAIL-7 covers credentials only, and a repo with
zero credential patterns can still contain a fully-written order-routing module.** Over every `.py`
on every branch, expect **zero**: any `POST`/`PUT`/`DELETE` against an `/order`, `/fapi/v1/order` or
`/api/v3/order` path string; the identifiers `place_order`, `create_order`, `submit_order`,
`cancel_order`, `new_order`, `client.futures_`, `ccxt`, `binance.client`; and any exchange-SDK
import. **Required red leg: a planted `def place_order(...)` must be reported.**
FAILS IF: any order-placement symbol exists on any branch — **including behind a flag, a stub, or a
`NotImplementedError`, because a stub is a thing that can be switched on.**

**F-SAIL-10 · THE OPS SPINE REPORTS RATHER THAN SKIPS (new — D-1 had no fixture at all).** Four legs:
 1. **with the backup target absent, the heartbeat COMPLETES and names the unwritable copy** — it
    does not halt and does not omit the line (§2.1: `drive_wait` gates writes, not reads).
    **This fires on day one: `/Volumes` today holds only `Macintosh HD`.**
 2. with a persisted last-run stamp set three fires in the past, the next run **enumerates exactly
    three missed fires by name and executes exactly one evaluation — a backfill is a failure** (D-1d);
 3. `exchange/status/CADENCE.md` holds one row per armed `com.naiad-sail.*` agent, cross-checked
    against `launchctl print gui/501` — **a count mismatch is red** (D-1c; this is the defect the
    existing registry already has: seven agents armed, three registered);
 4. every lifted file carries its provenance header — repo, branch, path, commit sha (D-1h).
FAILS IF: any leg skips silently. *"A silent skip is indistinguishable from success."*

---

## Verdict criteria — the skeleton is DONE when (BRIEF §7)

1. **One heartbeat runs end-to-end**, importing the card-spec, producing a journal row or an honest
   "no signal" row, **with spec sha printed** — F-SAIL-3.
2. **The weekly report renders** from an empty **and** a synthetic journal — F-SAIL-4.
3. **Determinism:** same inputs, two runs, one hash — F-SAIL-5, both digests in the build document.
4. **The parity check passes** on three reference trades — F-SAIL-6.
5. **The law grep passes: zero strategy conditionals outside the imported spec** — F-SAIL-1, an AST
   scan with its anti-vacuity clause, and its expected-zero stated as its failure condition.
6. **BUILDERS_REPORT filed** with the inventory verdict (BRIEF §2 — already filed, cite it) and
   **every deviation named**.
7. **(added by DEC-5)** **The modularity proof passes** — F-SAIL-8: a second setup registers with
   zero body-code edits.
8. **(added by DEC-5/D-9)** **SAIL refuses to start without a valid enable-list** — F-SAIL-2, D-9a.

9. **(closing an orphan)** **No keys anywhere** — F-SAIL-7 passes on every branch, with its
   exemption list declared in code and the rule for entry into it stated, and **SAIL's own prose
   about not having keys does not trip it.**
10. **(closing an orphan)** **No order path exists** — F-SAIL-9.
11. **(closing an orphan)** **The ops spine reports rather than skips** — F-SAIL-10.
12. **(closing an orphan)** **SAIL's CI actually executes F-SAIL-1..10 and fails the push on any
    red.** Naiad's `ci.yml:21` shape — `pytest fixtures/` only, so `tests/` never runs on push —
    **must not be reproduced.**
13. **(closing an orphan)** **The validator has printed at least one row** (D-7), with n-so-far —
    because D-7 is a founding justification for the whole build and appeared in no criterion, so the
    skeleton could have been DONE with the cure for F-C6-c absent.

**F-SAIL-1..10 ALL PASS and all thirteen criteria hold, or the skeleton is not done. Any single
fixture failure is a REJECT — halt without committing, and file the transcript.**
Box discipline: reports lean, journal by pointer.

*(The first draft stopped at eight and mapped no criterion to F-SAIL-7. A SAIL build carrying
credentials would have satisfied every stated DONE condition. Recorded rather than quietly fixed.)*

---

## Invariants

1. **BRIEF §1 outranks every line of this contract.** Body, never brain.
2. **PROMETHEUS IS READ-ONLY** — no commit, no branch, no file touched, in any session, until its
   disposition is ratified (DEC-2). The lift reads a quarantine clone and nothing else.
3. **CONVENTIONS Invariant 3** — documents are cheap, data is not. The SAIL journal never enters
   `exchange/`; it is referenced by path and sha.
4. **CONVENTIONS Invariant 4** — one build document per session, and it appends its ledger line.
5. **§4.4 R3 determinism** self-executes; this contract does not opt in, it merely must not
   contradict it.
6. **§6.4 named-constant protocol** governs every pinned constant here, `tf_govern` included
   (DEC-4): grep the NAME, the VALUE and the THRESHOLD TEXT; record a pin-vs-import decision per
   dependent; historical regenerators stay PINNED and labelled, live consumers IMPORT.
7. **To claim absence, enumerate** (Invariant 6). Every ABSENT in this contract names what was
   searched.

---

## What this phase is NOT

- **NOT live trading.** No order routing exists — absent, not stubbed (D-4d).
- **NOT a second implementation of the card.** Any rule SAIL cannot import does not exist in SAIL.
- **NOT an automatic setup selector.** Out of scope by law (DEC-5(iii), D-9c).
- **NOT cross-setup risk management.** Netting, shared risk budget and correlation limits between
  slots are deliberately excluded (D-4e). Two enabled setups run independently.
- **NOT the card-spec export.** APOLLO owes that paste on the Naiad side once this skeleton stands
  (BRIEF §8). This contract defines only the **consumer** side.
- **NOT a Prometheus decommission.** DEC-2 keeps the old agent sailing; its end is a separate word.
- **NOT a fix for the four missing Oracle rows in `CADENCE.md`**, nor for Naiad's `ci.yml` scope gap.
  Both are named in the REGISTER; neither is this contract's to fix.
- **NOT a graduation of D15 from diagnostics to law.** That is a future ruling at money.

---

## REGISTER — open items carried by this contract

Provenance tags per `CONVENTIONS.md:612`: `[open]` = undetermined.

| # | item | owner | note |
|---|---|---|---|
| 1 | **"SDK?"** — from the operator's 2026-08-18 diagram | **APOLLO** | **[open] · define or retire. NOTHING IS BUILT AGAINST IT.** It appears on the diagram without a referent; no `SDK` hit exists in the estate outside the diagram itself. Until defined, no deliverable here depends on it |
| 2 | **The funnel's sixth stage: `exited` or `belled`?** | operator / APOLLO | **[open]** · BRIEF §5 says `exited`; `scripts/tierc2_rules.py:132-135` says `belled`. Not synonyms — `belled` is one terminal disposition, `exited` the union. D-8(2) holds until ruled |
| 3 | **Prometheus disposition** (the running agent) | operator | **[open]** · DEC-2 defers it to first heartbeat. Also `LEDGER_ATHENA.md` pending item 3 |
| 4 | **`CADENCE.md` is stale by four Oracle rows** | ATHENA | **[open]** · seven `com.naiad.*` agents armed, three registered. Named by D-1c; fixing it is out of scope here |
| 5 | **Naiad `ci.yml` runs `pytest fixtures/` only** | operator | **[open]** · `tests/` never executes on push, so F-BOX-1 and F-BH-1 do not run in CI. One-line fix, an ops call. SAIL must not inherit the shape — see the placement note |
| 6 | **Slot-2 candidate** | APOLLO | **[open]** · the registry has N slots and one occupant. TC7's hybrid R&H program is the obvious future client; nothing is promised |
| 7 | **The card-spec does not exist yet — (a) export first, or (b) provisional spec?** | **operator / APOLLO** | **[open] · BLOCKS verdict criteria 1 and 4.** See the PREREQUISITE under the stamp. BRIEF §8 orders the export *after* the skeleton, so the acceptance test currently requires importing something that does not exist |
| 8 | **L-LIMIT-2's instrument binding** | **operator** | **[open] · BLOCKS D-7c.** The interdict at `scripts/tierc6_lab_limit.py:228-236` lifts only when the operator names **the instrument, its corridor edges and its card version**. That act is not among DEC-1..DEC-5. The validator's first row does not lift it by itself |

---

## Deliverable document

`exchange/reports/BUILDERS_REPORT_HEPHAESTUS_<date>_SAIL-SKELETON.md` — the single build document
per §3.1, ending with the file-disposition table (§3.2) and appending its STATUS block to
`exchange/status/LEDGER_ATHENA.md` (Invariant 4). **The full fixture transcript for F-SAIL-1..10 goes
in it verbatim, gate values as printed**, plus both determinism digests (§4.4), every deviation
named, and every finding reported-not-fixed.

---

## D-0 · EXECUTION RECORD — 2026-08-22

**D-0 RAN on 2026-08-22. IT IS OPEN.** No confirmation has been given and none is recorded here.
**Nothing below D-0 was executed: `~/naiad-sail` does not exist, and no deliverable or fixture text
in this file was amended while the gate is open.**

**What the gate produced.** The derived content — D-1..D-8 and F-SAIL-1..7, 9, 10 — was verified
against the estate by thirteen read-only agents (eleven verifiers, one per deliverable/fixture
group, plus a completeness critic and a decidability critic). **All eleven sections returned
DEFECTIVE: 139 findings, 32 of them blocking.** The eight most consequential were then re-checked by
hand against the code; **all eight held.** Full transcript, evidence and citations:
`exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-22_D0-CONFIRMATION-GATE.md`.

**What is put to the operator.** Not the ninety-two items the verification produced — the
decidability critic found that about twenty of them are citation corrections rather than decisions,
and that **the one question D-0 names first, the card-spec fork, was asked by none of the eleven**.
The funnel is therefore **SIX questions**, ordered, in §1 of that report:

| # | question | blocks |
|--:|---|---|
| ❶ | The card-spec fork — and branch (b) as written is unbuildable | verdict criteria 1 and 4; everything downstream |
| ❷ | D-7's first client (L-LIMIT-2) is already falsified in-sample by its own clause (c) | criterion 13 |
| ❸ | What L-LIMIT-2 needs the operator to name — instrument, corridor edges, card version | D-7c · REGISTER 8 |
| ❹ | `exited` vs `belled` — malformed as posed; `belled` has no functional consumer | D-8(2) · REGISTER 2 |
| ❺ | Is D-4 ratified or pending? The stamp and this gate disagree | the gate's own scope |
| ❻ | Eighteen sub-deliverables have no fixture and no verdict criterion | what "done" means |

**THE GATE'S OWN DEFECTS, recorded rather than quietly fixed.** (1) Its list is wrong in both
directions: the stamp at line 3 ratifies *"D-4 (strengthened)"* while lines 5 and 160 put
*"D-1..D-8"* — which contains D-4 — as PENDING. (2) It carries REGISTER items 2 and 7 but not item
8, whose own row declares it BLOCKS D-7c. (3) It has no verdict criterion of its own. (4) It states
no ordering and no partial-closure rule for the decisions it asks for.

**HOW THIS RECORD CLOSES.** The operator's answers are appended beneath this block, each dated, and
D-0 is closed when every one of the six carries one and no derived deliverable remains that no
answer reaches. The ~20 citation amendments land in the same act, not before — amending the
contract's body while the gate is open would hand the operator a different document than the one he
was asked about.
