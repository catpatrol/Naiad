---
description: Search the daily-brief archive by date, asset, radar state, flag or verdict
argument-hint: [e.g. --from 2026-07-01 --state ZONE_ACTIVE --asset SOLUSDT]
---

Search the archived daily briefs. Arguments: $ARGUMENTS

1. Pass the arguments straight through to the lookup tool from the repo root:

```
.venv/Scripts/python.exe scripts/brief_lookup.py $ARGUMENTS
```

Available filters: `--date` `--from` `--to` `--asset` `--state` `--flag`
`--verdict` `--text`, plus `--full` to dump whole index lines. With no
arguments it lists every archived day.

If the operator described what they want in prose rather than flags, translate
it — "SOL days where funding was crowded" becomes
`--asset SOLUSDT --flag funding_p90_plus`; "when was BTC last in a zone" becomes
`--asset BTCUSDT --state ZONE_ACTIVE`.

2. Report the matching dates with their verdicts, radar states and true flags,
   and give the snapshot paths so the operator can open the HTML. If a snapshot
   file is missing (the index line survives but the day's files were pruned),
   say so — the index is the durable record, the snapshots are the detail.

3. To read a specific day's numbers, open that day's JSON directly. Every JSON
   embeds the complete rule set that produced it under `rules`, with
   `rules_version` and `rules_sha256` — so a number from an older brief is
   always interpretable against the rules of its own day. If `rules_version`
   differs across the range being compared, **say so**: the confluence
   dictionary and thresholds may have changed, and archive comparability depends
   on that version.

FIREWALL (A1.1 clause 4). The archive is an operations journal. It **may** be
mined for hypotheses, and that is exactly what this command is for — spotting
recurring confluence layerings worth pre-registering. But:
- Any rule idea it produces enters the study **only** through G-7
  pre-registration, scored **only** on exploration-classic data.
- The archive is **never** a scoring window. Do not compute how radar-flagged
  setups subsequently performed, hit rates, or expectancy over these days — that
  is the prohibited outcome join, whatever form the question takes.
- A forward-validation protocol would be a separate governance act. None exists.
If asked for any of the above, decline plainly, say which clause forbids it, and
offer the descriptive alternative (how often a state or flag *occurred*, never
how it *paid*).
