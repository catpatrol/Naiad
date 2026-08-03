---
description: Re-render a stored BRIEF-2 capture to HTML
---
Regenerate the report from a STORED capture. The JSON is the record; the HTML is
disposable and is always rebuilt from it.

```
C:\venvs\naiad\Scripts\python.exe scripts/brief_render.py --date <YYYY-MM-DD> --slot <slot>
```

If `scripts/brief_render.py` does not exist yet, say so plainly — it is the
outstanding half of Stage 4 — and offer to read the capture JSON directly
instead. Do not fabricate a render.

Never recompute numbers here. A render that recomputes is a second source of
truth, and the two will drift.
