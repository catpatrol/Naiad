---
description: Record an intent in the FORWARD-0 hash-chained diary
---
Append one entry to `ops/forward_log.jsonl`.

```
C:\venvs\naiad\Scripts\python.exe scripts/forward_log.py --log   --kind <mechanical|hypothetical|actual>   --symbol BTCUSDT --lens 4h --direction long   --trigger "<what would have to happen>"   --entry <level> --stop <level> --targets <l1,l2>   --brief-date <YYYY-MM-DD> --brief-slot <slot>   --note "<why, in one line>"
```

To record an exit — a status transition on the same entry:

```
C:\venvs\naiad\Scripts\python.exe scripts/forward_log.py --transition <id> --status closed   --exit-level <level> --exit-reason "<target 1 | stop | invalidated>"
```

Rules that matter when running this:
- **`kind` is strictly separated.** `mechanical` = derived by the engine's rules;
  `hypothetical` = the operator's read, not taken; `actual` = a real position.
  Never mix them, and never infer one from another.
- **Append-only.** An exit is a NEW line carrying the same `id`, never an edit.
  If a stored line looks wrong, append a correction; do not rewrite history.
- **No sizing.** The record schema has no size field, deliberately.
- **This is a diary, not a scoreboard.** Do not compute anything over it — no
  win rate, no expectancy, no "how did the flagged setups do". That waits on
  **G-10** being separately ratified.

Always run `/trade-verify` after logging, and report the chain head.
