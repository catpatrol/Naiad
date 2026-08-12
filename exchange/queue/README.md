# queue/ — convention

1. Numbered work orders: `NNN_<short-slug>.md`, allocated in ascending order, never reused.
2. Format is a full contract — deliverable, basis, fixtures, verdict criteria — not a request line.
3. Every item ends with a stamp line: `RATIFIED: <word> <date>` (unratified items read `RATIFIED: PENDING`).
4. Drafting rights: APOLLO, ATHENA, ARGUS. HERMES validates completeness and sequences; he never drafts.
5. HEPHAESTUS executes ratified items only; an item without the operator's stamp is a request, not work.
6. Execution stamp: `BUILT: <artifact or commit>` on a line of its own once the item is
   delivered (unbuilt items read `BUILT: PENDING` or carry no stamp). `RATIFIED` says the
   work may start; `BUILT` says it finished. `MANIFEST.json` counts the gap between them
   as `queue_ratified_unbuilt` -- added 2026-08-12 after the counter reported 0 open
   against six items, because it had no way to tell started from finished.
