---
description: Build or rebuild BRIEF-2 panel partitions
---
Write-once daily partitions (Amendment 2 §8.2).

```
C:\venvs\naiad\Scripts\python.exe scripts/brief_panel.py --date <YYYY-MM-DD>     # one day
C:\venvs\naiad\Scripts\python.exe scripts/brief_panel.py --rebuild-all           # every captured day
C:\venvs\naiad\Scripts\python.exe scripts/brief_panel.py --consolidated          # untracked convenience view
```

Behaviour to expect and to report accurately:
- Partitions are written ONCE. Re-running prints `EXISTS ... (write-once; not
  rewritten)` and changes nothing. This is the design, not a failure.
- `--force` exists only to repair a known-bad file. Do not pass it to "refresh"
  a partition; refreshing is exactly what write-once forbids.
- Every partition rebuilds from CAPTURES ALONE. The panel never reads a previous
  partition, so a corrupted one cannot propagate forward.

Grain: `(asset, slot, date)` for snapshots; levels and areas join back on it.
Columns are documented in `briefs/panel/SCHEMA.md`.
