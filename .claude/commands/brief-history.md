---
description: Search the BRIEF-2 capture archive
---
Query the stored captures and panel partitions.

```
C:\venvs\naiad\Scripts\python.exe scripts/brief_lookup.py <args>
```

Supported filters (Amendment 2 §8):
- `--slot <london|ny_am|post_ny>` — one session slot
- `--area-score <N>` — captures where a confluence area scored at least N
- `--divergence` — captures carrying a generalised divergence (§6.1)
- `--rvwap-cross` — captures where an RVWAP pair changed side (§6.2)

Prefer the panel partitions for aggregate questions — they are columnar and
already have the grain `(asset, slot, date)`:

```
C:\venvs\naiad\Scripts\python.exe scripts/brief_panel.py --consolidated
```

The consolidated view is UNTRACKED and regenerable; never treat it as a record.

This searches STATE, never outcomes. If asked whether a level "worked", say that
outcome statistics are census work under G-7 and are not available here.
