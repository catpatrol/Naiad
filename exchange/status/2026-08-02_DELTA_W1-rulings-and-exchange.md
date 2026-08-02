# DELTA — what changed on 2026-08-02, for APOLLO and ARGUS

**Read this once. Do not re-prime, do not re-verify anything below — it is all already verified.**
Written by HEPHAESTUS. One page. What changed, and what you do differently from now on.

---

## 1 · The eight W1 rulings, and what each means for you

| ruling | decision | what it changes for your lane |
|---|---|---|
| **Q-1 C** | Sync bus **and** digest | Pushed repo files reach you through the project box. The DIGEST is an index with pointers, never a rewrite of your work. |
| **Q-2 A** | Auto-push `exchange/**` and lane ledgers only | Coordination state publishes itself. **Evidence never publishes without the operator.** Your study artifacts keep the per-authorization rule. |
| **Q-3 A** | Per-lane append-only ledgers | You have your own ledger. Others read it; nobody rewrites it. §5 below. |
| **Q-4 A** | Hybrid Hermes, 2×/day, CRONOS folded in | Cadence and timestamps are Hermes' schedule. **No seventh agent** — gate W-3 is closed. |
| **Q-5** (modified) | Drafting rights **APOLLO, ATHENA, ARGUS** | You may draft work orders for the builder. Dionysus and Hermes may not. §4 below. |
| **Q-6 A** | Apollo stays a chat | No migration. Your ratified action lists execute through the queue. HELIOS tripwire on record only. |
| **Q-7 A** | Non-blocking answer debt | A CHALLENGE never stalls you. Answer in writing by the next phase boundary — one line is enough. |
| **Q-8 A** | Two integers per session-end STATUS | §6 below. |

## 2 · The exchange map — where things go now

```
exchange/
  status/   your ledger · MANIFEST.json · CADENCE.md · daily/ outputs · this note
  queue/    numbered work orders, each carrying an operator stamp
  reports/  builder outputs — YYYY-MM-DD_<LANE>_<type>_<name>.md
  drops/    raw operator inbox; Hermes names (G-11) and files
  DIGEST.md Hermes-owned index (placeholder until his first pass)
```

**Content guard, binding:** text only · **1 MB per file** · anything larger is referenced by
`path:` + `sha256:` pointer, never carried.

Repo filing also changed the same day: handoffs, challenges, funnels and old STATUS docs are now in
`docs/history/`; primers in `docs/primers/`; HTML reports in `docs/reports/`; contracts in `prompts/`;
pine/scanner code in `docs/knowledge/pine/`. Nothing was deleted.

## 3 · `_reviewer_box` still works — you do not have to change mid-flight

If a paste of yours already writes to `_reviewer_box\reports\` or `_reviewer_box\daily\`, **it keeps
working.** The daily routine sweeps those two folders at the start of every run and moves whatever it
finds into the matching `exchange/` folder, logging each move. Nothing is lost and nothing is
overwritten — a name collision is kept under a suffixed name, never resolved by clobbering.

Write to `exchange/` for new work. The drop points are for the transition, not a second home.

## 4 · How to draft a queue item

A work order is a **full contract**, not a request line. File it as
`exchange/queue/NNN_<short-slug>.md` with the next unused number, and include:

1. **Problem** — why this is worth a builder session
2. **Deliverable** — the exact path that will exist afterwards
3. **Basis** — what is authority, and what wins when sources disagree
4. **Fixtures** — the mechanical checks that must pass
5. **Verdict criteria** — what ACCEPT, ACCEPT-WITH-CORRECTION and REJECT each mean
6. **Out of scope** — what this order does not license

End the file with the stamp line, exactly:

```
RATIFIED: PENDING
```

The operator replaces `PENDING` with one word and a date. **Until that happens the item is a request,
not work, and Hephaestus will not execute it.** That stamp is what keeps the queue from becoming a
lane instructing another lane. `001_condensed-project-history.md` is on file as a worked example.

## 5 · How to append to your ledger

`exchange/status/LEDGER_APOLLO.md` · `exchange/status/LEDGER_ARGUS.md`. **Append-only.** Never edit a
past entry — a correction is a NEW entry naming what it supersedes. The central `LEDGER.md` remains
the *evidence* ledger and is untouched by any of this.

```
=== STATUS_<LANE> — <date> ===
NOW: <2-3 sentences>
LAST EVENT: <date> — <one line>
FACTS: <up to 6 lines, each ending [verified/ledger/ratified/handoff/unconfirmed-live/open]>
PENDING: <numbered items waiting on the operator>
NEXT: <single next action + owner>
METRICS: operator actions this session = <n> · files re-ingested = <n>
=== END STATUS ===
```

Your ledgers are seeded from your last STATUS doc (2026-07-27) and **marked stale**. First thing you
append replaces that as the live picture.

## 6 · The two integers

Every session-end STATUS carries them:

- **operator actions this session** — drops, pastes, clicks
- **files re-ingested to seed** — how much context had to be re-fed

Two numbers, near-zero cost. They are the ferry census: every future architecture argument becomes
evidence instead of taste. Hermes tallies them weekly.

## 7 · F4 has a result — and it changes an assumption

**A scheduled Cowork run CAN see the local repo folder. READ = yes · LIST = yes · WRITE = yes.**
(Unattended run, 2026-08-02T15:00:50Z; full record in `SCHED_TEST_RESULT_2026-08-02.md`.) The working
assumption that "scheduled means remote means GitHub-only" was **wrong**.

What genuinely constrains a scheduled lane instead:

- **No network egress.** No Binance, no external APIs, no pypi. Market data must run machine-side or
  be pre-staged into the repo before the run fires.
- **No OAuth connectors** — anything needing Slack or Daloopa stays on-demand.
- **Git was never tested.** Whether a scheduled run can commit or push is **unknown** and needs its
  own pre-registered test before any lane gets commit duties.

### ⚠ SCHEDULED-LANE NO-DELETE POLICY — standing

F4 found that file deletion, initially blocked, became available **in an unattended run** by calling
`allow_cowork_file_delete` — with no human present to approve it. The technical guardrail did not
require a person.

**So: no scheduled lane deletes anything.** Not files, not archives, not repo content. Deletion is an
attended builder action with an operator decision behind it. This is a policy guardrail standing in
for a technical one that proved not to hold, and it holds regardless of any re-test — the cost of
being wrong is asymmetric.

---

**Nothing here needs verifying by you. Ask if something contradicts what you already hold.**
