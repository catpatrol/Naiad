---
description: Build today's BRIEF-2 capture for a session slot
---
Run the BRIEF-2 capture for the requested slot (default `ny_am` if the operator
does not name one). Amendment 2 §2.3 slots: `london` · `ny_am` · `post_ny`.

```
C:\venvs\naiad\Scripts\python.exe scripts/brief_capture.py --slot <slot>
```

Then build the day's panel partitions:

```
C:\venvs\naiad\Scripts\python.exe scripts/brief_panel.py --date <YYYY-MM-DD>
```

Notes for the run:
- The capture is TRACKED (`briefs/brief_<date>_<slot>.json`) and auto-commits;
  it NEVER pushes. Repo work is commit-no-push.
- A same-slot re-run REFUSES unless `--force` is passed — replacing a stored
  capture breaks archive comparability for anything already published from it.
- Panel partitions are WRITE-ONCE. A second run reports `EXISTS` and rewrites
  nothing. That is correct behaviour, not an error.
- Every render carries `PARITY NOT CERTIFIED` until the operator's parity
  readings are returned and matched. Do not present numbers as adopted.

Report: capture path, sha256, runtime, level counts per asset, and whether the
volume-included and volume-excluded lines in the sand differ.
