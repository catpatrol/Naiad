# NOTE — ATHENA → APOLLO · 2026-08-11 · DATA RESIDENCY + what changed under you

Read once; rule also in shared memory (#13). Full detail: STATUS_ATHENA_2026-08-11_LANE-CLOSE.md.

1. ALL bulk data now lives on D:/Naiad (external drive), mirroring repo paths. Your SEQ8 substrate
   research_outputs/seq8/ stays LOCAL (live, MC-1 reads it) and is MIRRORED on D:, 15/15
   hash-verified. seq8_run2 relocated to D: — and note the correction of record: run2's 8 data
   files are byte-identical twins, its 3 run manifests are NOT (a genuine determinism rerun);
   cite accordingly.
2. CONTRACT RULE, census-2 and everything you draft from now on: bulk outputs (klines, parquet,
   jsonl, captures) write DIRECTLY to D:/Naiad/<mirrored path> and are searched there. Every D:
   path carries a reachability gate that HALTS if D: is absent — never a silent laptop fallback.
   The drive is spinning USB: assume it can be unplugged. MC-1 as ratified keeps its written
   paths — do not amend it retroactively.
3. Determinism reruns (rule R3, CONVENTIONS §4): hash-and-compare, print both digests, discard the
   rerun DATA in the same session, KEEP its run manifests (KB-scale provenance).
4. Your session-start sources are unchanged: SS_SYSTEM_SYNTHESIS_2026-08-06.md + LEDGER_APOLLO.md
   + the MC1 queue item. Lane state never returns to shared memory. Memory itself is redrafted
   lean (13 entries) — if the auto-summary looks bulky, that is regeneration lag, not loss.
5. Archives: --phase now writes to D: by default with a Drive mirror; phase completion requires
   D: plugged in. Report rotation (queue 003, ratified) will move >30-day reports to
   docs/history/reports/ — your LEDGER, queue items and unacted notes are exempt.
