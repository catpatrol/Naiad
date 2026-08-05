# BUILDERS REPORT — HERMES — 2026-08-05 — FIRST_RUN (box steward)

**Lane:** HERMES (coordination and verification) · **Surface:** Claude Cowork, `naiad` folder attached
**Instruction:** `PRIMER_HERMES_2026-08-06_v3_BOX_STEWARD.md` §7, executed end to end
**Read with zero prior context.** Every term is defined at first use.

---

## 0 · What this document is, in plain language

The three web chats in this project (APOLLO, ARGUS, ATHENA) cannot read files off your computer. They see repo content **only** through the Claude project knowledge box — a search index built from files you tick in a picker. That box holds roughly **6.39 MB**. It has overflowed twice.

My job this run was to measure exactly what is in it, name anything that does not belong, and build an index so a lane can ask for a file instead of you ticking everything just in case.

**I found one thing that outranks everything else in this report, and it is not a file — it is a contradiction inside the rulebook.** Depending on which of two clauses in `CONVENTIONS.md` is live, the box is either at 21% or at 110%. I cannot resolve that. You can, in one word.

**A note on dates.** This primer is dated 2026-08-06 and my sandbox clock reads 2026-08-05T23:30Z. I have used the measured clock for filenames and timestamps and flagged the difference rather than silently picking one. `[verified]`

---

## 1 · Step 0 — CONVENTIONS.md read

Read in full: `exchange/status/CONVENTIONS.md`, **41,564 bytes**, last modified 2026-08-05 20:30. `[verified]`

One rule found there that I applied immediately, quoted because it shaped the whole measurement — §3.2, "Corollary for guards":

> *"A per-file size limit does not bound a folder. `exchange/` reached 51% of the context box while nine of its ten data files were individually under the 1 MB cap — one breach, nine compliant, half the box gone. **Budget the total, not the item.**"*

That is why §2 below reports folder totals first and individual offenders second.

---

## 2 · The box budget — the table you most need

**Box capacity: 6,390,000 bytes.** This number is *derived, not given.* The primer says two capture files totalling 4,024,198 B are "about 63%" of the box (implies 6.388 million) and that 770 KB of ARGUS prose is "about 12%" (implies 6.42 million). I used 6,390,000 and I am stating the derivation so you can correct it if the real figure differs. `[verified]`

**Definitions used:** *prose* = `.md` and `.txt`. *data* = everything else (`.json`, `.jsonl`, `.csv`, `.html`, `.parquet`). Only **git-tracked** files are counted, because an untracked file never reaches GitHub and therefore never reaches the box.

### Scenario A — the box holds `LEDGER.md` + `exchange/` only

This is what CONVENTIONS §3.2 says your standing tick set is, as of 2026-08-06.

| item | bytes | % of 6.39 MB | files |
|---|---:|---:|---:|
| `LEDGER.md` | 255,011 | 3.99% | 1 |
| `exchange/` — **prose** | 872,848 | 13.66% | 68 |
| `exchange/` — **data** | 225,314 | 3.53% | 6 |
| `exchange/` total | 1,098,162 | 17.19% | 74 |
| **TOTAL IN BOX** | **1,353,173** | **21.2%** | **75** |

**Verdict: healthy.** Roughly four-fifths of the box free.

### Scenario B — the sync also reaches `docs/` and `prompts/`

This is what CONVENTIONS §4.3 says, measured 2026-08-03 and never revised.

| item | bytes | % of 6.39 MB | files |
|---|---:|---:|---:|
| Scenario A subtotal | 1,353,173 | 21.2% | 75 |
| `docs/` (tracked) | 5,432,504 | 85.02% | 70 |
| `prompts/` (tracked) | 225,748 | 3.53% | 15 |
| **TOTAL IN BOX** | **7,011,425** | **109.7%** | **160** |

**Verdict: overflowed by 621,425 bytes.** The difference between the two scenarios is **5,658,252 bytes — 88.5 percentage points.**

### Every file in `exchange/` over 1% of box (63,900 B)

There is exactly **one**.

| file | bytes | % box | type | owning lane |
|---|---:|---:|---|---|
| `exchange/reports/WF1_discriminants.json` | 113,355 | 1.77% | **data** | APOLLO |

### `exchange/` by folder

| folder | bytes | % box | files |
|---|---:|---:|---:|
| `exchange/reports/` | 840,222 | 13.15% | 44 |
| `exchange/status/` | 113,532 | 1.78% | 14 |
| `exchange/status/daily/` | 107,048 | 1.68% | 8 |
| `exchange/queue/` | 23,724 | 0.37% | 5 |
| `exchange/` (root) | 13,075 | 0.20% | 2 |
| `exchange/drops/` | 561 | 0.01% | 1 |

**The law confirmed a fourth time.** 68 prose documents = 13.7% of the box. Two capture files = 63.0%. **Documents are cheap; data is not. Write more reports, never fewer.**

---

## 3 · The offenders — every data file, with a proposed home

**I moved nothing and deleted nothing.** These are proposals.

### 3.1 Inside `exchange/` — one genuine offender

| file | bytes | % box | proposed home | replace with |
|---|---:|---:|---|---|
| `exchange/reports/WF1_discriminants.json` | 113,355 | 1.77% | `research_outputs/wf1/WF1_discriminants.json` — it is a study artifact | pointer stub `WF1_discriminants.json.pointer.md`, ~1 KB (0.02% box), carrying path + sha256 + bytes + box cost, modelled on the exemplary stub at `docs/history/argus/CAPTURE_2026-08-03_post_ny.json.pointer.md` |

**Net saving: ~112 KB, 1.75 percentage points.** Modest — `exchange/` is in good shape.

### 3.2 The five remaining data files in `exchange/` — leave them

| file | bytes | % box | verdict |
|---|---:|---:|---|
| `exchange/status/daily/MANIFEST_2026-07-28.json` | 26,000 | 0.41% | **keep** — the manifest series *is* the integrity record; it is the status layer's reason to exist |
| `exchange/status/MANIFEST.json` | 22,600 | 0.35% | **keep** — ground truth, read by every lane |
| `exchange/status/daily/MANIFEST_2026-08-05.json` | 22,600 | 0.35% | **keep** |
| `exchange/status/daily/MANIFEST_2026-08-03.json` | 21,115 | 0.33% | **keep** |
| `exchange/status/daily/MANIFEST_2026-08-02.json` | 19,644 | 0.31% | **keep** |

Total 112 KB / 1.75%. Each is under 0.5%, the rolling window already caps the series at 7, and they are the one class of data file whose whole purpose is to be read from the bus. **Recommendation: the content guard's "text only" clause should carry a named exception for `status/**/MANIFEST*.json`** — otherwise the rule is permanently in technical breach and a rule in permanent breach stops being enforced. That is ATHENA's to draft.

### 3.3 Outside `exchange/` — decided entirely by Finding H-1

| file | bytes | % box | tracked? | on origin? |
|---|---:|---:|---|---|
| `docs/history/argus/CAPTURE_CERTIFIED_2026-08-05_post_ny.json` | 2,050,315 | **32.09%** | TRACKED | **on origin** |
| `docs/history/argus/CAPTURE_2026-08-05_post_ny.json` | 1,973,883 | **30.89%** | TRACKED | **on origin** |
| `docs/reports/Cascade Rewire.html` | 243,474 | 3.81% | TRACKED | on origin |
| `docs/history/argus/RENDER_2026-08-03_post_ny.html` | 144,574 | 2.26% | TRACKED | on origin |
| `docs/history/argus/PARITY_C3_2026-08-03.json` | 54,427 | 0.85% | TRACKED | on origin |

The top two total **4,024,198 bytes — 62.98%**, matching the primer's figure to the byte. `[verified]`

**Proposed homes, if H-1 resolves toward Scenario B:** captures and renders → `briefs/`; parity JSON → `research_outputs/`; each replaced by a ~1 KB pointer stub. **If H-1 resolves toward Scenario A, these cost nothing and nothing needs doing.** This is precisely why I am not proposing action before you rule.

---

## 4 · Findings — including things nobody has flagged

### H-1 · CONVENTIONS contradicts itself about what is in the box — **the headline**

Two clauses in the same authoritative file:

> **§3.2:** *"Standing tick set (operator, 2026-08-06): `LEDGER.md` and `exchange/` ONLY."*

> **§4.3:** *"Known limit, measured 2026-08-03: the sync reaches `exchange/`, `docs/`, `prompts/`."*

The second is a *measurement* of what the sync selection reached on 08-03. The first is a *ruling* narrowing it on 08-06. They can both be historically true — but §4.3 is written in the present tense with no note that it has been superseded, so **a lane reading §4.3 concludes `docs/` is in the box.**

This is the exact failure the file names in its own opening rule:

> *"A correction REPLACES the assertion it corrects. Appending a note beneath an uncorrected claim is not a correction; it is a second claim, and a reader believes the first one because the first one is what they read… When a fact changes, rewrite every place that asserts it."*

The primer instructed me that where it and CONVENTIONS conflict, CONVENTIONS wins and I flag rather than choose. Here **CONVENTIONS conflicts with itself**, so the same instruction applies with more force. **Flagged, not resolved.** `[verified]`

### H-2 · The pointer discipline was applied to the symptom, not the process

On 2026-08-04 a 1,879,133 B capture was removed from `exchange/` and replaced by `docs/history/argus/CAPTURE_2026-08-03_post_ny.json.pointer.md` — 1,060 bytes, naming the original path, the tracked-and-pushed twin, the sha256, the byte count and the box cost. **It is exemplary. It is the template.**

**Two days later the same lane wrote two larger capture files into a synced tree with no pointer at all.** The single instance was cured; the process that generates instances was not. The fix that would hold is a guard at write time — CONVENTIONS §3.2 already requires flagging any artifact over ~1% "at the moment it is created, which is the only moment the choice is cheap" — but nothing enforces it. `[verified]`

### H-3 · Three of four queue items are incomplete against the CONVENTIONS standard

| item | RATIFIED | deliverables | fixtures | verdict criteria | "what this is not" |
|---|---|---|---|---|---|
| `001_condensed-project-history.md` | **PENDING** | yes | F-H1..H6 | yes | yes |
| `002_backup-and-publish-guards.md` | yes (2026-08-04) | yes | yes | **MISSING** | yes |
| `2026-08-03_WF1_winner_forensics_APOLLO.md` | yes (2026-08-03) | **MISSING** | yes | **MISSING** | **MISSING** |
| `2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md` | **NO STAMP AT ALL** | yes | yes | **MISSING** | yes |

**Reported, not fixed** — validating completeness is my duty; drafting is not. The one complete item is the one still unratified. `[verified]`

### H-4 · One queue item has no ratification stamp, and work on it appears to have run anyway

`queue/2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md` has no `RATIFIED:` line — not "PENDING", absent entirely. `queue/README.md` rule 5: *"an item without the operator's stamp is a request, not work."* Yet `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_SEQ8.md` (33,748 B) exists and describes SEQ8 work performed.

Two innocent explanations: you ratified it verbally and the stamp was never written back, or the note-form ruling in `NOTE_DIONYSUS_to_APOLLO_2026-08-04_SEQ8_findings_and_agreements.md` was treated as authorisation. **I am not adjudicating — I am reporting that the gate and the work disagree on the record.** `[verified]`

### H-5 · CONVENTIONS §8 carries a mangled edit — nobody has flagged this

After the "Triggers armed" paragraph, an orphan fragment survives:

```
08:30. **Not armed:** the HERMES scheduled run. **Manual and staying manual:** Sync now.
```

It is the tail of a superseded sentence whose head was rewritten in place. Cosmetically minor — but it sits in the one file that binds all six actors, and it is the same class of half-applied correction as H-1. **ATHENA's file; hers to fix.** `[verified]`

### H-6 · The manifest's HEAD is behind the live HEAD, again

`exchange/status/MANIFEST.json` was generated 2026-08-05T16:50:42Z and records HEAD `c9e16e8`. Live HEAD is `aa65905`. I reported the identical condition on 2026-08-04. **Clock-fresh, content-stale** — a lane reading the manifest for repo state reads a superseded commit, and the staleness test as written cannot detect it because it measures the timestamp, not the sha. `[verified]`

### H-7 · Two lanes look silent and are not

| lane | ledger newest | artifacts filed since |
|---|---|---:|
| ARGUS | 2026-07-27 (9 days) | 20+ |
| HEPHAESTUS | 2026-08-02 (3 days) | 19 reports |
| APOLLO | 2026-07-27 (9 days) | 3 |

ARGUS and HEPHAESTUS are among the most productive lanes and their ledgers are among the stalest. **The staleness stamp measures the status layer, not the lane** — read it as "this lane's ledger is unreliable", never as "this lane is idle." APOLLO is the one where low ledger activity and low artifact count coincide. `[verified]`

### H-8 · The queue counter under-reports

`MANIFEST.json` reports `queue_open: 1`. Four non-README items exist. The counter appears to match only `NNN_`-prefixed filenames, so the two date-named items (`2026-08-03_WF1…`, `2026-08-04_SEQ8…`) are invisible to it. Anyone trusting the manifest's queue count sees a quarter of the queue. `[verified]`

### H-9 · All four inbox notes are addressed to lanes that have not moved since

Detail in `exchange/DIGEST.md` §4. Three of four are to APOLLO, whose ledger is 9 days stale. Two were acted on **by the builder**, which is not the addressee acting. **I moved none of them** — a note addressed to APOLLO is APOLLO's file. `[verified]`

### H-10 · `drops/` is empty

README only. No filing or G-11 naming owed this cycle. `[verified]`

---

## 5 · Things I did NOT do, stated so the boundary is legible

- **Deleted nothing.** No file, no archive, no repo content — the absolute policy of primer §2 and CONVENTIONS §4.1.
- **Moved nothing.** Every relocation in §3 is a proposal.
- **Re-authored no lane's content.** Findings name the owning lane.
- **Instructed no lane.** No ratification stamp exists authorising me to.
- **Did not push.** Explained in §7.
- **Did not verify my own executions** (duty D6). The two files I wrote are listed in §6 with hashes computed after writing; **nobody has independently checked them, and that check is not mine to perform.**

---

## 6 · File-disposition table

Six standing columns plus BOX COST, per CONVENTIONS §3.2.

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `exchange/DIGEST.md` | yes | tracked | **not committed** | **no** | none yet — worktree only | 11,847 B · **0.19%** |
| `exchange/reports/BUILDERS_REPORT_HERMES_2026-08-05_FIRST_RUN.md` | yes | **untracked (new)** | **not committed** | **no** | none yet — worktree only | ~17,900 B · **~0.28%** |

**Combined box cost of this run: ~0.47% of the 6.39 MB budget.** Both are prose; neither approaches the 1 MB per-file cap.

**Neither file is protected until HEPHAESTUS publishes.** They exist on one disk, inside a OneDrive tree, uncommitted. *(Per CONVENTIONS §3.1, a file must never contain its own sha256 — that row is stale the moment it is written. The DIGEST's hash is printed on screen in §7 instead.)*

---

## 7 · I cannot push, and would not

No network egress from this surface, and `exchange/**` publishing is HEPHAESTUS's guarded path via `publish_exchange.py` — **a library module with no `__main__`, so running it as a script publishes nothing and exits quietly.** Not mine to call regardless.

**Your one remaining action:** have these two files published, then click **Sync now**. Until you do, no web lane can see this DIGEST — and the DIGEST is the thing that lets them stop asking you to tick more folders.

---

## 8 · The decision I need from you — funnel format, CONVENTIONS §1.1

**WHAT IS IT.** Your rulebook states two different things about which folders feed the project knowledge box. One clause says `LEDGER.md` and `exchange/` only. Another says the sync also reaches `docs/` and `prompts/`. Only you know which is currently ticked in the picker.

**WHY IT MATTERS, AND WHY IT IS YOURS.** Under the first reading the box is 21% full and healthy. Under the second it is **110% full — overflowed**, and two capture files are eating 63% of it on their own. It needs your judgment because the answer lives in a settings panel only you can see, not in any file I can read.

**OPTIONS.**
- **(a)** Confirm the tick set is `LEDGER.md` + `exchange/` only. Then §4.3 is stale prose and ATHENA rewrites it. Nothing else to do; the box is healthy.
- **(b)** Confirm `docs/` and `prompts/` are still ticked. Then the box is overflowed now, and the five files in §3.3 need pointer stubs urgently — ~4.4 MB recovered, ~69 percentage points.
- **(c)** Untick `docs/` and `prompts/` while ruling, converting (b) into (a) immediately, then let ATHENA reconcile the wording at leisure.

**IMPLICATIONS.** (a) costs one line of drafting and risks nothing if you are right. (b) is the honest path if `docs/` is genuinely ticked, but leaves the box overflowed until the stubs ship. (c) is fastest to a safe state, at the cost of the three web lanes losing access to `docs/` content — which is survivable precisely because this DIGEST now lists what is there, so they can ask for it.

**MY RECOMMENDATION: (c), then (a).** It reaches a known-safe state in one click and does not depend on my reading of two clauses being right. I hold this **weakly** — I cannot see your picker, and that is the only place the true answer lives. If checking it is quick, check first and pick (a) or (b) on evidence rather than on my inference.

---

```
=== STATUS_HERMES — 2026-08-05 ===
NOW: First run as box steward, executed end to end per primer v3 §7. Box measured, DIGEST
rebuilt from placeholder-successor into a full index, one genuine offender named in exchange/
and five named outside it. Nothing moved, nothing deleted, nothing pushed.
LAST EVENT: 2026-08-05 — HERMES box-steward run; DIGEST.md and this report written.
FACTS:
- exchange/ = 1,098,162 B across 74 files = 17.2% of the 6.39 MB box; prose 872,848 B (68 files)
  vs data 225,314 B (6 files) [verified]
- CONVENTIONS contradicts itself: §3.2 ticks LEDGER+exchange only (21.2%), §4.3 says sync also
  reaches docs/+prompts/ (109.7%, OVERFLOWED). 88.5 points hang on it [verified]
- Two capture JSONs in docs/history/argus/ total 4,024,198 B = 62.98%, both TRACKED and on
  origin; matches the primer's figure to the byte [verified]
- One exchange/ file over 1%: reports/WF1_discriminants.json, 113,355 B, 1.77%, data, APOLLO [verified]
- Queue: 3 of 4 items lack verdict criteria; SEQ8 has NO ratification stamp yet builder work on
  it is already filed [verified]
- Manifest HEAD c9e16e8 is behind live aa65905 — clock-fresh, content-stale, same as 08-04 [verified]
PENDING:
1. Rule H-1: is the tick set LEDGER+exchange only, or does it still include docs/+prompts/?
2. Ratify or reject queue 001 (the only complete contract, still PENDING since 2026-08-02)
3. Rule on SEQ8: was it authorised? The stamp and the executed work disagree
4. Publish these two files, then click Sync now — nothing reaches the web lanes until then
NEXT: Operator rules H-1. Owner: operator.
METRICS: operator actions this session = 1 · files re-ingested = 1
=== END STATUS ===
```
