# DRAFT CONTRACT — DIGEST REFRESH — for ATHENA, to instruct HERMES

**From:** HEPHAESTUS (builder) · **To:** ATHENA · **Date:** 2026-08-15 · **Branch:** `v12-v1-census`

> **AUTHORITY — read this first.** This is a **DRAFT**, not a contract. It carries **no RATIFIED
> stamp** and nobody should execute it. Queue drafting rights are APOLLO / ATHENA / ARGUS (ruling
> Q-5); I am the builder and I hold none. I am handing ATHENA a worked draft because I hold the
> measurements and raised the finding — **ATHENA amends it, ATHENA puts it to the operator, and it
> becomes `queue/006` only when it carries his stamp.**
>
> It also instructs **HERMES**, and `DIGEST.md` is HERMES-only by CONVENTIONS `NAIAD-S4-BOX` — *"an
> index of pointers, never a re-authored substitute."* **I have deliberately not written a line of
> the replacement DIGEST.** What follows is a defect inventory, a shape, and acceptance criteria.
> The index itself is HERMES's to author.

---

## 0 · Why this is urgent, in one paragraph

`exchange/DIGEST.md` was generated **2026-08-12T11:40Z by HERMES from `C:\Naiad`** — a machine this
project no longer runs on. It has been wrong since the migration. **What changed today is that it
became load-bearing:** THE GREAT COLLAPSE restructured CONVENTIONS so that `NAIAD-S0-CORE` — the
section *every lane reads every session* — now sends every lane to `exchange/DIGEST.md` as the
**first** of three sources for current state. A stale index that nobody consulted was a nuisance.
An authoritative index that everybody is now instructed to open, still telling them to halt unless
their path ends `C:\Naiad`, is a defect with teeth.

**I did not fix it myself, and that was deliberate.** A builder re-authoring the coordination lane's
output is the HELIOS tripwire in `NAIAD-S5-LANES`. The fix belongs to HERMES. This draft exists so
the fix is a ratified contract rather than an improvisation.

---

## 1 · Basis — files actually read this session

Per `NAIAD-S6-ERRORS` §6.3, every claim below cites a file read this session, not recalled.

| file | what was read | what it established |
|---|---|---|
| `exchange/DIGEST.md` | all 205 lines | the defect inventory in §2 |
| `exchange/status/CONVENTIONS.md` | all, post-collapse | that §0 THE MAP now points at DIGEST first |
| `scripts/publish_exchange.py` | constants + `budget()` | `BOX_BYTES` 16,000,000 · warn 0.40 · refuse 0.70 · tick set = `exchange/` + `LEDGER.md` |
| `scripts/backup_estate.py` | line 328 + the v2 amendment note | `BACKUP_DEST_DEFAULT = "/Volumes/LaCie/naiad-backups"` |
| `exchange/status/MANIFEST.json` | `head`, `queue_open` | manifest head `d830ecb`, live HEAD `0ea398e` — **F-4 still live** |
| `exchange/status/LEDGER_*.md` | entry headers, all six | true ledger recency (§2, Class 3) |
| `docs/memory/NAIAD_MEMORY_VERBATIM_2026-08-15.md` | all | the M5 open items, incl. the Cowork remount |

---

## 2 · The defect inventory

Line numbers are the 2026-08-12 edition as it stands at `0ea398e`.

### Class 1 — ACTIVELY MISLEADING. A lane obeying these does the wrong thing.

| # | line | what it says | what is true |
|---|---:|---|---|
| C1-1 | 20 | **"HALT if the path contains `OneDrive`; HALT unless it ends `C:\Naiad`"** | On this host there is no `C:`. **This gate halts unconditionally.** The live gate is in `NAIAD-S0-CORE`. |
| C1-2 | 16–20 | "TWO CLONES EXIST AND THE DEAD ONE LIES" | The OneDrive tree is a Windows-era hazard. The live tree is `~/Naiad`; the macOS markers are `com~apple~CloudDocs` and `Mobile Documents`. |
| C1-3 | 70 | Working clone = `C:\Naiad` | `~/Naiad` (= `/Users/luis/Naiad`). |
| C1-4 | 72 | Interpreter `C:\venvs\naiad\Scripts\python.exe` — *"did not move"* | `~/venvs/naiad/bin/python`, Python **3.12.14**. |
| C1-5 | 73 | Estate `C:\Users\luisf\AppData\Local\naiad\data_cache` | `~/.cache/naiad/data_cache`. |
| C1-6 | 14, 74–77 | Bulk data / archives / backups on `D:\Naiad`, `D:\naiad-backups` | Local under `~/Naiad`; backups `/Volumes/LaCie/naiad-backups`. Data residency v2. |
| C1-7 | 83 | Scheduled tasks "repointed to `Start In: C:\Naiad`", next runs **13-Aug** | Three **launchd** agents: `com.naiad.daily` 07:00, `com.naiad.estate` Sun 08:00, `com.naiad.workflow` Sun 08:30. |

### Class 2 — STALE NUMBERS. Not dangerous, but every one is quotable and wrong.

| # | line | says | true |
|---|---:|---|---|
| C2-1 | 28, 46, 49–50 | warn **50** / refuse **80** | **0.40 / 0.70** — ATHENA recalibrated 2026-08-15. |
| C2-2 | 3 | Live HEAD `cc10d8f` | `0ea398e` at drafting. |
| C2-3 | 24–41 | 141 files, tick set 2,831,045 B / 17.69% | See §5 acceptance figures. |
| C2-4 | 106 | `CONVENTIONS.md` 53,679 B, 08-12, *"THE FIRST RULE + FIND IT FAST index"* | **64,008 B, 2026-08-15**, and the shape is new: §0 CORE, S1–S8, two TOCs, nine tokens. |
| C2-5 | 186–189 | staleness table, all `2026-08-12` | Everything in `status/` moved on 08-15. |

### Class 3 — SUPERSEDED FINDINGS. Carry the number forward, change the verdict.

- **F-7** *(CONVENTIONS §8 mangled edit, "third cycle, unfixed")* — **CLOSE.** I checked `HEAD` before
  the rewrite with `grep -F`: the orphan fragment was **already gone**, so it had been fixed before
  today. It is not this session's repair and it is not still open. §8 has since been rewritten
  wholesale.
- **F-2** *(the abandoned clone reports itself healthy)* — **RESTATE, do not delete.** True and
  Windows-era. The old PC is alive and Phase B is a later phase; the finding belongs in a superseded
  block, not in a live warning banner.
- **F-4** *(manifest trails live HEAD)* — **STILL LIVE, fifth cycle.** Measured this session:
  manifest `head = d830ecb`, live HEAD `0ea398e`.
- **F-6** *(ledger gaps)* — **RE-MEASURE, the ranking has inverted.** Real newest-entry dates,
  by entry header rather than by any date in the file: APOLLO 08-15 · ATHENA 08-15 · HEPHAESTUS
  08-15 · DIONYSUS 08-13 · ARGUS 08-11 · **HERMES 08-04**. **HERMES is now the stalest ledger in the
  project, by seven days, and it is HERMES's own.**

### Class 4 — MISSING. This is the failure that matters most.

DIGEST's stated purpose is *"You cannot request what you do not know exists."* Six artifacts created
since 08-12 are absent from it, and **three of them are deliberately off the bus**, which means a web
lane cannot discover them any other way:

| artifact | on the bus? | why a lane needs to know |
|---|---|---|
| `docs/CASELAW.md` | **no** | the reasoning behind all 27 cited rules |
| `docs/CONVENTIONS_RULE_CENSUS_2026-08-15.md` | **no** | the evidence that the collapse lost nothing |
| `docs/memory/NAIAD_MEMORY_VERBATIM_2026-08-15.md` | **no** | the pre-collapse memory record |
| `scripts/fixtures_conventions.py` | no | F-CONV-1..4 |
| `LEDGER.md` → **STANDING VERDICTS** | yes | study state now lives there; §0 THE MAP points at it |
| the `NAIAD-S*` token scheme | — | how to address a rules section from memory or a contract |

Plus the 08-13/14/15 build reports (M2 restore, M3 sweep, M4 launchd, zip-residency, box-governance,
Tier-C2 baseline, VIZ-2, census2b ORACLE, and the collapse).

---

## 3 · Preconditions — HALT gates, checked before any writing

**HERMES has never run.** Do not assume the environment.

- **P-1 · The mount.** Cowork must be remounted at `~/Naiad`. This is an **open M5 item** and may not
  be done. If the mounted root is not the live working clone, **HALT and report** — do not write an
  index describing a tree you are not looking at. That is the C1 defect class repeating itself.
- **P-2 · The discriminator test.** Print the mounted root and the live HEAD. **HALT unless HEAD
  matches `origin/v12-v1-census`** as seen from the repo. A scheduled Cowork run has no network
  egress, so a stale checkout cannot be detected by fetching — it must be detected by refusing.
- **P-3 · Git.** Git availability in Cowork is **UNTESTED**; `NAIAD-S4-BOX` says assume a scheduled
  run cannot commit or push. **Test it and report the result** — do not silently proceed either way.
  See Q-1 in §7: who commits is an open question this contract does not settle.
- **P-4 · No deletion.** The scheduled-lane NO-DELETE policy is standing and unconditional. This
  contract authorises **writing `exchange/DIGEST.md`** and nothing else. It does not authorise
  tidying `reports/`, resolving R-4's twins, or removing anything.

---

## 4 · The work

### D-1 · Rebuild, do not patch
**Rebuild `exchange/DIGEST.md` from a fresh measurement of the live tree.** Patching leaves
Windows-era scaffolding in place — the C1 defects are not typos, they are a description of a
different machine.

**Preserve the supersession discipline the current edition gets right.** It records closed findings
as superseded rather than deleting them (§2 "is now VOID and is recorded here as superseded",
F-1/F-3). Keep that: carry closed findings forward **by number** with their new verdict, in a short
block, so the record of what was once believed survives the rebuild.

### D-2 · Stop copying facts that live in CONVENTIONS
**This is the root cause and the most important deliverable.** C1-1 happened because DIGEST kept its
own copy of the identity gate. When the gate changed, the copy did not. One fact, two homes.

**DIGEST must not restate the identity gate, the box thresholds, the tick-set definition, the
content guard, or any rule.** It **cites the token**: "identity gate: `NAIAD-S0-CORE`", "thresholds
and the tick set: `NAIAD-S4-BOX`". The nine tokens exist so a pointer can be exact and survive
renumbering. **A DIGEST that quotes a rule can go stale against it; a DIGEST that cites one cannot.**

Numbers HERMES **measures** (bytes, counts, dates, HEAD) are its own and belong in the file.
Numbers HERMES would be **restating** (16,000,000 B, 0.40, 0.70) get cited, not copied.

### D-3 · Geography, replaced wholesale
Table of §3 rewritten for the Mac era. **Do not derive it from the current DIGEST.** Source it from
`NAIAD-S2-PASTE` §2.1 GEOGRAPHY, which is now the authoritative map, and cite it.

### D-4 · The discoverability table
A section listing artifacts that exist but are **off the bus**, with a one-line reason a lane might
want each — Class 4 above. This is DIGEST's core purpose and it is currently unserved.

### D-5 · Findings, re-verdicted
F-1..F-8 carried forward by number: close F-7 with the reason, restate F-2 as historical, keep F-4
live with today's measurement, re-measure F-6, and add any new finding the rebuild surfaces.

### D-6 · The ledger-recency reader, and a known-answer test
**F-5 was a parsing defect** — a reader that matched only `=== STATUS_X — date ===` missed
`## date — …` and published a false staleness reading that read as another lane's neglect. HERMES
diagnosed this itself and the lesson must not be lost with the rewrite.

**Before publishing any recency figure, validate the reader against a known-answer set.** Both entry
header forms appear in the live ledgers; a reader that finds only one is wrong in the same direction
as last time. My own first attempt at this measurement — a naive `grep` for any date — returned
`2026-08-28` and `2026-09-05` for two lanes by matching *forward-looking* dates in prose. **Too loose
fails as badly as too strict.** The test set below is the acceptance answer, and it is deliberately
withheld from the reader's design: build the reader, then check it.

---

## 5 · Acceptance — F-DIG-1..6

**HERMES never self-verifies** (`NAIAD-S5-LANES`, the HELIOS tripwire). Acceptance is run by
**ATHENA**, or delegated to HEPHAESTUS. These are stated so either can execute them.

| fixture | assertion | how |
|---|---|---|
| **F-DIG-1** | **Zero Windows-era literals.** `C:\`, `C:/`, `D:\`, `D:/`, `G:\`, `G:/`, `AppData`, `Scripts\python`, `Task Scheduler`, `PowerShell` return **no hits** in the new DIGEST **except** inside a block explicitly labelled as superseded/historical. | `grep -F` each |
| **F-DIG-2** | **No rule is restated.** The strings `HALT`, `warn 0.4`/`warn 40`, `refuse 0.7`/`refuse 70`, `16,000,000` do not appear as assertions; each such topic instead cites a `NAIAD-S*` token. | read + `grep -F` |
| **F-DIG-3** | **Tokens resolve.** Every `NAIAD-S*` cited in DIGEST exists as a section header in CONVENTIONS. **Citing is free — no allowlist entry needed.** F-CONV-1 fails only on a second *definition* (a heading naming the token); mentions are unrestricted, which is the whole point of minting tokens. See the note below. | run `fixtures_conventions.py` |
| **F-DIG-4** | **Class 4 discoverable.** All six missing artifacts appear, each with a path. | `grep -F` each path |
| **F-DIG-5** | **Measurements agree with the disk**, ±1 file / ±1 KB drift for same-session writes. Cross-check set below. | recompute |
| **F-DIG-6** | **Ledger recency correct** against the known-answer set below — all six, exactly. | compare |

**F-DIG-5 cross-check, measured by me at `0ea398e`.** Provided to ATHENA **as the acceptance answer,
not as an input to HERMES** — a figure HERMES copies from this note is a figure nobody measured
twice, which is CL-18 (*a claim repeated across documents is not a claim verified*).

```
exchange/            2,693,282 B   144 files
LEDGER.md              259,298 B
TICK SET             2,952,580 B = 18.45% of 16,000,000
  reports/           2,003,267 B   12.52%   102 files
  status/              592,503 B    3.70%    30 files
  status/daily/        198,774 B    1.24%    14 files
  queue/                78,804 B    0.49%     9 files
  drops/                   561 B    0.00%     1 file
MANIFEST head d830ecb  ·  live HEAD 0ea398e   (F-4 live)
```

**F-DIG-6 known-answer set** — newest **entry header**, not newest date in the file:

```
APOLLO 2026-08-15 · ATHENA 2026-08-15 · HEPHAESTUS 2026-08-15
DIONYSUS 2026-08-13 · ARGUS 2026-08-11 · HERMES 2026-08-04
```

> **A fixture defect this draft found, and it is relevant to D-2.** F-CONV-1 originally asserted each
> token appeared **nowhere else in the repo**. That is the wrong invariant: tokens exist so that
> memory entries, contracts and notes *can cite a section exactly*. A check that fails on citation
> punishes the behaviour the tokens were minted for — and it did, twice within the hour: first on the
> collapse's own build document, then on **this note**, the first inter-lane document to use a token
> as intended. **Fixed at `scripts/fixtures_conventions.py`:** a *definition* is a heading naming the
> token, a *mention* is anything else, and only a second definition is a second home. Both controls
> run — a fake `## §9 · FAKE «NAIAD-S4-BOX»` heading still fails; a prose citation passes. **So
> DIGEST may cite freely, which is what D-2 asks of it.**

---

## 6 · Handback

Per `NAIAD-S3-REPORT`: **one build document**, `exchange/reports/BUILDERS_REPORT_HERMES_<date>_DIGEST-REFRESH.md`
— gate values as printed, the full F-DIG transcript, findings reported-not-fixed, the disposition
table with BOX COST — and it **ends by appending its STATUS entry to `LEDGER_HERMES.md` in the same
session.** That ledger is seven days stale and it is this lane's own; this contract closes that gap
as a byproduct, which is exactly what ruling 'append' is for.

**Rollback:** `git checkout -- exchange/DIGEST.md`. The rebuild touches one file. Nothing is deleted,
so nothing is unrecoverable.

---

## 7 · Open questions — ATHENA's calls, or the operator's

Presented as a decision funnel (`NAIAD-S1-OPERATOR`) because each changes what gets built.

### Q-1 · Who commits the rebuilt DIGEST?
**What it is.** Cowork's git availability is untested; a scheduled run is assumed unable to push.
**Why it matters.** DIGEST is worthless until it reaches the box, and it reaches the box only via a
push plus Sync now.
**Options.** (a) HERMES writes and commits, if P-3 shows git works — fewest hands, but unproven.
(b) **HERMES writes; HEPHAESTUS publishes in a following session** — proven path, one extra hop, and
it keeps authorship with HERMES while the commit is done by the lane that owns pushing. (c) HERMES
drafts to `drops/` and ATHENA reviews before anything lands.
**My lean: (b).** It works whatever P-3 returns, and it does not make the first-ever HERMES run
depend on an untested capability.

### Q-2 · Does DIGEST keep a budget section at all?
**What it is.** `publish()` prints tick-set %, exchange-only % and absolute MB on **every** publish,
and that print is authoritative at the moment it runs. DIGEST's table is a snapshot that is stale by
the next publish — and its current one is quoting retired thresholds.
**Options.** (a) Keep the full table. (b) **Keep only measurements that publish does not print** —
per-folder breakdown, file counts, prose-vs-data split — and cite `NAIAD-S4-BOX` for thresholds.
(c) Drop it; point at the last publish line.
**My lean: (b).** The folder breakdown is genuinely HERMES's contribution and nothing else produces
it. The thresholds are the part that went stale, and they are the part that should have been a
citation all along.

### Q-3 · Is the HERMES scheduled run armed as part of this?
**What it is.** `NAIAD-S8-BACKUP` records **NOT ARMED: no HERMES task exists, pending the operator.**
Three launchd agents are live; a fourth would be mechanical.
**Why it matters.** DIGEST staleness is a recurring finding *because* it is regenerated by hand. But
a scheduled run has no network egress, cannot push, and must not delete — so an armed HERMES writes a
file that then waits for a human anyway.
**Options.** (a) Arm it now. (b) **Run this refresh attended first, then decide** — one observed run
tells you what the schedule would actually produce. (c) Leave unarmed indefinitely.
**My lean: (b).** Arming a lane that has never run once is scheduling an unknown.

### Q-4 · Scope discipline
DIGEST lists R-1..R-5 residuals and an inbox with five open notes, several nine-plus days old. **I
recommend this contract does not touch them.** They are real, they are owned, and folding them in
turns a one-file index rebuild into a cross-lane cleanup that no single lane can accept. Re-state
them; do not chase them.

---

## 8 · What I am NOT asking for, stated so it is not inferred

- **No edit to CONVENTIONS.** It was rewritten today and its fixtures pass; DIGEST cites it.
- **No re-authoring of another lane's content.** DIGEST indexes and points. If a lane's ledger is
  wrong, that is a finding addressed to that lane, not a correction HERMES makes.
- **No deletion, of anything, for any reason.**
- **No new pointer stubs, no rotation, no tidying of R-4's twins.**

---

## 9 · Disposition of this draft

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `exchange/reports/NOTE_HEPHAESTUS_2026-08-15_TO_ATHENA_digest-refresh-contract-draft.md` | yes | tracked | at publish | yes, `origin/v12-v1-census` | GitHub | this file, ~15 KB · ~0.09% of box |

**Status: UNRATIFIED DRAFT.** It becomes `queue/006` when ATHENA has amended it and the operator has
stamped it. Until then nobody executes it.

---

*Ends. HEPHAESTUS → ATHENA, 2026-08-15.*
