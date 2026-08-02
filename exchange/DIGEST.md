# DIGEST — one page, how every lane's work fits the whole

**Owner: HERMES.** This file is Hermes' to build and maintain. No other lane writes it. It sits at the
head of the sync bus so that one read tells the operator where everything stands.

**Status: PLACEHOLDER.** Created 2026-08-02 by HEPHAESTUS as part of the exchange v1 skeleton. Hermes
has not yet run against it. Nothing below is authoritative until Hermes' first pass replaces this
header.

**What it will carry** (per ruling Q-1 C — the digest is an *index with pointers*, never a re-authored
substitute for the raw artifacts):

- per-lane state with a staleness stamp, pointing at `status/LEDGER_<LANE>.md`
- open queue items and their ratification state, pointing at `queue/`
- unfiled drops awaiting naming, pointing at `drops/`
- the weekly tally of the Q-8 metrics (operator actions · files re-ingested)

**Until Hermes' first run, read the raw files directly:** `status/LEDGER_*.md`, `status/CADENCE.md`,
`status/MANIFEST.json`, `queue/`, `reports/`.
