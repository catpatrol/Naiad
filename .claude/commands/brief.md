---
description: Generate today's Naiad Daily Brief and report the paths and headline biases
---

Run the daily brief generator and report the result.

1. Run it from the repo root with the project venv (it needs numpy/pandas/pyarrow):

```
.venv/Scripts/python.exe scripts/daily_brief.py
```

It tops up klines and funding to the latest closed bar, computes Tier-1 layers
1–12 for all 10 basket assets, fetches Tier-2 (degrading to ⚠ chips on failure),
writes both snapshots, replaces today's line in the archive index, then runs
fixtures F-B1..F-B8.

2. Report back, concisely:
   - the two output paths (`research_outputs/brief/brief_<date>.json` / `.html`)
   - the HTML byte count
   - the fixture line (`n/8 fixtures pass`) — if any fixture FAILED, say so
     plainly and quote it; a failed run is not adoptable (A1.9)
   - the per-asset headline table the script prints (daily / weekly verdict and
     the three radar states)
   - anything in the **Actionable now** or **Stand aside** sections worth the
     operator's attention, and any ⚠ staleness or degraded-fetch chips

3. Then add the Tier-3 layer the script deliberately does not fetch: search the
   web for today's macro calendar and crypto headlines, and summarise them in
   chat as the "Calendar & events" panel the HTML reserves. Keep it short —
   scheduled events with times, plus anything that moved the basket.

Guardrails, all of which the artifact itself enforces:
- The brief is an **operations artifact, not study evidence**. Do not let any
  number here seed an engine rule, a pre-registration, or a study claim.
- It prints **no sizing** and never scores signal or trade outcomes. Do not add
  either in chat.
- If the operator asks "how did yesterday's flagged setups do?", that is the
  prohibited outcome join (firewall clause 4). Say so and offer the archive
  search instead: `/brief-history`.
