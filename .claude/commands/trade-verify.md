---
description: Verify FORWARD-0 chain integrity and capture linkage
---
```
C:\venvs\naiad\Scripts\python.exe scripts/forward_log.py --verify
```

Reports two things and nothing else:
- **chain** — every line's `entry_sha256` recomputes from its own content plus
  its predecessor's digest. A retroactive edit, a deleted line or a reordering
  breaks the chain from that point forward and is named by line number.
- **linkage** — every entry's `brief_json_sha256` matches a stored capture, so an
  intent can always be traced to the exact numbers it was formed from.

Exit code is non-zero when either check fails.

If the chain is broken, report the line number and the reason verbatim. Do NOT
repair it by editing the file — a chain that can be silently repaired proves
nothing. The correct response is to say what broke and let the operator decide.

This command computes NO statistic over the log, and neither should you when
reporting its output. Integrity is not performance.
