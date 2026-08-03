---
description: Timestamp an operator observation into the current capture
---
Append a dated observation to today's capture and commit it.

```
C:\venvs\naiad\Scripts\python.exe scripts/brief_note.py --slot <slot> --text "<observation>"
```

If `scripts/brief_note.py` does not exist yet, say so — it is outstanding — and
do NOT hand-edit the capture JSON. A capture edited by hand no longer matches its
own `json_sha256` in the index, which silently breaks F-B9's round-trip.

Notes are observations, not predictions and not outcomes. Record what was seen,
never whether it paid.
