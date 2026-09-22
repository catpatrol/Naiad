# QUARANTINE — 2026-09-22T09:55Z

LAW 2 of the RESUME contract: *"partials are QUARANTINED to
`research_outputs/tierc10/_partial_<ts>/` — never deleted."*

These are **kill-partials**: transcripts written by FILTERED fixture runs (a leg-substring
invocation) during the 2026-09-21 session that the API 529 then killed. Each records a
one-or-few-leg run, not a suite. They sat beside the whole-suite transcripts of record, where a
reader could mistake a partial's "1/1 PASS" for a suite's verdict. Moved, not deleted.

| file | bytes | what it actually is |
|---|---|---|
| `lanes/FIXTURES_LANES_partial.txt` | 4,692 | a filtered `be_latch lanes_gate spr_build` run |
| `panel/FIXTURES_PANEL_partial.txt` | 6,552 | `FIXTURE SUMMARY 1/1 PASS {"F-LAW4-GATE": true}` |

The suites of record are untouched and both re-passed on 2026-09-22:
`lanes/FIXTURES_LANES.txt` (exit 0, 10/10 PASS, 51/51 break legs RED) and
`panel/FIXTURES_PANEL.txt` (exit 0, 22/22 PASS, 150/150 break legs RED, F-CTRL 0.000e+00).

## DISCLOSED, NOT QUARANTINED

`census/smoke/` and `null/smoke/` are **legitimate** smoke roots with their own
`build_manifest.json` — but they carry full lookalike filenames (`smoke/outcome_grid.parquet`
39,316 B against the canonical 675,998 B) and were built before the R1 bands and the era split,
so their contents are now WRONG in substance (2 classes, no era column). Both fixture suites
default to a smoke root only when the full root has no manifest; both full roots have one, so the
default resolves correctly today. They are left in place and disclosed here because moving them
would change the fallback behaviour of two suites during a resume. **Rebuild or remove at CLOSE.**
