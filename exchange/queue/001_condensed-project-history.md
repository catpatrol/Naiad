# 001 — Condensed project history

**Drafted by:** ATHENA (drafting rights per ruling Q-5, 2026-08-02)
**Filed:** 2026-08-02 · **Executor:** HEPHAESTUS · **Validator/sequencer:** HERMES
**Status:** NOT EXECUTABLE until the stamp at the foot of this file reads a ratification word.

---

## 1 · Problem

The project's history is spread across nine dated handoff and status documents, several of them
overlapping, several superseded in part but not in whole, and none of them a single place a new lane
can read to learn what happened and why. Every new session pays a re-ingestion tax reading them —
which is precisely the cost the Q-8 metrics now measure.

## 2 · Deliverable

`docs/PROJECT_HISTORY.md` — one document, chronological, condensed.

**Basis:** `LEDGER.md` is the source of record. The history is **ledger-derived**: every claim must
trace to a ledger entry, a commit, or a ratified contract. The handoff documents may be used to
locate material and to recover narrative connective tissue, but they are not themselves authority —
where a handoff and the ledger disagree, the ledger wins and the disagreement is noted.

**Provenance tagging is mandatory.** Every claim carries exactly one tag:

| tag | meaning |
|---|---|
| `[ledger]` | traceable to a specific `LEDGER.md` entry |
| `[commit]` | traceable to a commit sha in this repo |
| `[ratified]` | an operator ruling on record |
| `[handoff]` | asserted by a handoff document, not independently confirmed in the ledger |
| `[unconfirmed]` | believed true, no source located — must be rare and must be visibly rare |

## 3 · Scope — the documents this supersedes

On acceptance, `docs/PROJECT_HISTORY.md` becomes the entry point for project history, and these nine
become archival. **Do not delete them.** Move them to `docs/history/` and add a one-line pointer at
the top of each naming the section of `PROJECT_HISTORY.md` that now carries their content.

Tracked:

- `HANDOFF_2026-07-22_Census_to_Census1b.md` (17,304 B)
- `REVIEWER_HANDOFF_2026-07-12.md` (9,390 B)
- `REVIEWER_HANDOFF_2026-07-13_V3_FORENSICS.md` (22,457 B)
- `REVIEWER_HANDOFF_2026-07-15_V3_RECOMPUTE.md` (13,625 B)
- `REVIEWER_HANDOFF_2026-07-25_ENGINE_INGESTION.md` (32,141 B)
- `docs/handoffs/HANDOFF_2026-07-27_BRIEF_to_CENSUS_1.md` (18,475 B)
- `docs/handoffs/HANDOFF_2026-07-27_BRIEF_to_ENGINE.md` (7,416 B)

Already filed into `docs/history/` by the 2026-08-02 filing pass (paths updated here so the order
stays executable):

- `docs/history/PROJECT_STATUS_AND_CONTEXT_2026-07-28.md` (26,588 B)
- `docs/history/STATUS_HANDOFF_BRIEF_2026-07-28.md` (30,588 B)
- `docs/history/STATUS — ENGINE (…).txt` (2,917 B) and `docs/history/STATUS — BRIEF (…).txt` (3,008 B)
  — the APOLLO and ARGUS ledger seeds; supersede their *narrative*, and leave the ledger seeds alone

Since the filing pass already moved the seven tracked documents' peers into `docs/history/`, the
"move them" instruction above now applies only to the five still at their original paths.

**Explicitly NOT superseded** — current coordination state, not history:
`docs/history/HANDOFF_DIONYSUS_to_ATHENA_2026-08-02_Workflow_Redesign_Inputs.md`,
`docs/history/FUNNEL_DIONYSUS_W1_Workflow_Architecture_2026-08-02.md`,
`docs/history/CHALLENGE_DIONYSUS_01_Architecture_2026-08-02.md`, `claude/STATUS_SYSTEM.md`, and the
per-lane ledgers under `exchange/status/`. These live in `docs/history/` for filing reasons only —
their content is current.

## 4 · Fixtures

| id | assertion |
|---|---|
| F-H1 | **Every claim carries a tag.** Zero untagged assertions. A mechanical check counts sentences ending a claim against tag occurrences and reports any shortfall by line number. |
| F-H2 | Every `[commit]` tag names a sha that `git cat-file -e` resolves in this repo. |
| F-H3 | Every `[ledger]` tag is locatable in `LEDGER.md` by a quoted anchor phrase, and the anchor is reproduced in the tag so a reader can find it without searching. |
| F-H4 | `[unconfirmed]` claims are ≤ 5% of all claims, and each is listed together in a closing "open questions" section rather than buried. |
| F-H5 | All nine superseded documents still exist on disk after the run (moved, never deleted), and each carries its pointer line. |
| F-H6 | The document is under the exchange content guard's reading of "one file, one topic": ≤ 1 MB, text only. |

## 5 · Verdict criteria

**The reviewer spot-checks 10 claims against the ledger**, chosen by the reviewer and not by the
builder, spread across at least four distinct phases of the project. A claim passes if its tag is
correct and its content is supported by the source the tag names.

- **10/10 correct → ACCEPT.**
- **9/10 → ACCEPT WITH CORRECTION:** the one defect is fixed and re-checked before the document is
  cited by anything.
- **≤ 8/10 → REJECT.** No partial adoption; the document is not the entry point until it re-passes.

A tag that is *present but wrong* (e.g. `[ledger]` on something the ledger does not say) counts as a
failure, not a formatting nit. Mis-tagging is the specific failure mode this fixture set exists to
catch — an untagged claim is visibly unsupported, while a wrongly-tagged one is invisibly so.

## 6 · Out of scope

Rewriting or correcting `LEDGER.md`; re-litigating past rulings; summarising study *results* (the
history records that a phase ran and what was ruled, not what the numbers were).

---

RATIFIED: operator, 2026-08-06 — "ratify 001". Drafted by ATHENA. Executor: HEPHAESTUS.
This contract was the ONLY one of four in the queue complete against the CONVENTIONS
standard (deliverables, numbered fixtures F-H1..H6, verdict criteria, and a scope
boundary) and had waited on this stamp since it was drafted — a fact surfaced by the
HERMES queue audit of 2026-08-05.
