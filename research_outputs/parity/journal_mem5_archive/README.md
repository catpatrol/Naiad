# journal_mem5_archive — zoneMemory-5 variant seed (pre-1.0.3 engine output)

Archived 2026-07-12 under Engine 1.0.3 (input-parity conformance). These journals
were produced with the engine's pre-1.0.3 hardcoded `zone_memory = 5` for 5m exec,
which did NOT match the deployed Pine input default `zoneMemory = 3` — the 3C
parity-break root cause (see `research_outputs/ssv11_3/Engine_1.0.3_precontract_zoneMemory_fork.md`
and CHANGELOG "engine 1.0.3").

NOT waste, NOT deleted (regenerate-never-merge, LEDGER 2026-07-10): pre-paid seed
data for a future v12 named-variant candidate, "zoneMemory-5". Relative to the live
mem=3 parity journal, the mem=5 variant carries ~18 extra entries, 2 regrades, and
4,360 stop-divergent bars over the 2025-10-06 -> 2026-07-07 dev window.

Contents:
- `BTCUSDT_swing/*.jsonl`  — mem=5 v11_faithful parity journal (run_id 20711045..., engine 1.0.1/1.0.2).
- `dryrun_naiad_v0/`       — mem=5 naiad_v0 dryrun journal (non-load-bearing; the
                             collector stamps fresh journals at its own epoch).

Do not load these into parity checks. The live parity journal is
`research_outputs/parity/journal/` (regenerated at mem=3, Engine 1.0.3).
