# Naiad project memory — CLOSING snapshot, 2026-08-03

Companion to `claude_project_memory_2026-08-03.md` (the OPENING snapshot, 30 entries verbatim).
Read the opening snapshot first; this file records only what changed, plus the layer the opening
snapshot missed. Append-only convention per `docs/memory/README.md`.

## Why there are two layers, and why this file exists
Legacy project memory has TWO layers. **Layer 2** = the numbered operator-ratified edits, which
the reviewer can read and edit directly — captured verbatim in the opening snapshot. **Layer 1** =
the auto-generated project summary Claude synthesises from conversation history, which cannot be
edited directly and regenerates on its own. **The opening snapshot captured only layer 2.** That
was a reviewer omission, found on 2026-08-03 when the operator asked what exactly was preserved.
Layer 1 is captured below.

## Layer 2 — what changed on 2026-08-03
Panel: **30 entries → 23**. Executed by ATHENA via the memory editing interface under ruling
G-5(a), after `exchange/status/CONVENTIONS.md` was published and verified readable. Nothing was
deleted before its replacement text was live: **write, publish, verify readable, only then delete.**

REMOVED (full text now in CONVENTIONS.md at the section named; verbatim originals in the opening
snapshot):
| was | title | now at |
|---|---|---|
| #7 | Exact paste-ready text | CONVENTIONS §2.2 |
| #8 | Context-gap audit | CONVENTIONS §6.3 |
| #9 | Claude-optimization track | CONVENTIONS §9 |
| #14 | Workflow-design rule | CONVENTIONS §2.4 |
| #16 | Builder-idle-time preference | CONVENTIONS §2.4 |
| #25 | Infrastructure inventory | CONVENTIONS §8 |
| #28 | Builder handback, both artifacts | CONVENTIONS §3 |
| #29 | Manual-task instruction rule | CONVENTIONS §1.2 |

HELD BACK, deliberately: #1 (SS Pine backlog), #15 (ARGUS charter), #19 (SS interview rulings) —
lane-specific, not covered by the acceptance probe, and the operator was opening APOLLO. They move
at the phase-boundary audit once the probe passes, with the four pending merges. Target: 16.

CORRECTED IN PLACE: #24 backup architecture — the export claim downgraded to disputed pending
T-6; the phase-archive retention correction folded in; the unarmed `--workflow` trigger recorded.

ADDED: the session-start pointer entry (now #23), naming CONVENTIONS.md as authoritative and
recording that project memory does not reach Cowork.

## Layer 1 — the auto-generated project summary, captured 2026-08-03
Not verbatim-editable and regenerates from conversation history, so this is a point-in-time record
of its substance rather than a restorable artifact.

- **Operator:** Ludwig, no programming background. Runs Project Naiad — a systematic research
  programme to develop consistently profitable trading systems (the prime directive). Secret Sauce
  is one of its systems, not the project.
- **Method:** observe → hypothesise (pre-register) → test → let results inform the next
  hypothesis. No live capital until confidence is established. Falsification is a deliverable.
- **Data estate:** ~653 MB of kline/funding files at `%LOCALAPPDATA%\naiad\data_cache`, never in
  the repo, never under OneDrive; backed up as dated hashed generations to Google Drive.
- **Guiding attitude, his words:** "the alpha is buried under a pile of debris. We explore,
  examine and implement a continuous improvement mindset to achieve our goal."
- **Pantheon:** APOLLO (SSv12, census, Tier-C, Engine V2, Pine) · ARGUS (analytics, daily brief,
  volume filter) · ATHENA (resilience, backups, integrity, workflow) · DIONYSUS (critique) ·
  HERMES (coordination, Cowork) · HEPHAESTUS (builder, local Claude Code). Chats cannot read each
  other; the exchange bus plus the project box plus relayed STATUS blocks are the only channel.
- **Basket:** BTC ETH SOL NEAR ZEC JTO TAO HYPE FARTCOIN LIT, Binance USDT-M perps, 30-cell grid
  (swing 4H/5m, intraday 1H/5m, position 12H/15m).
- **Study state at capture:** structural stop is the architecture of record; two-line exit
  falsified; the harvest problem unsolved; research inversion adopted (condition on outcome,
  discriminate at birth); W-F1 winner forensics commissioned; SS work resumed in APOLLO.
- **Working style:** decision-funnel interviews, one-word rulings, zero-context plain-language
  reports, exact paste-ready text, provenance tags on every claim, parallel workstreams.

## Restoring from these snapshots
Layer 2 restores entry-by-entry: paste an entry's verbatim text back through the memory panel, or
via Anthropic's Settings > Capabilities > Memory > Start import (extraction-based and lossy, which
is why the opening capture is verbatim). Layer 1 cannot be restored directly — it regenerates.
