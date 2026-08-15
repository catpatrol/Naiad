# ROTATION LOG

Append-only record of build documents moved off the exchange bus by
`scripts/rotate_reports.py` (queue 003, D-1). Every entry is a MOVE:
the file is still tracked, still on GitHub, and `git log --follow`
still returns its full history at the new path.

PROVENANCE OF THE 2026-08-15 BLOCK (queue 005 M4, gate 0). Those eight lines were
NOT written by the scheduled sweep. They are a **named-set early rotation**,
operator-ratified 2026-08-15: the CENSUS-2A contract is SPENT, so its eight run
documents were moved three days after they were written rather than after the
pinned 30-day window. `rotate_reports.py --dry-run` on the same day selected
**0 candidates / 93 too young**, which is the correct behaviour and was left
intact -- `AGE_DAYS = 30` was not widened, not flagged, not touched. The named
set was driven through the same D-1 semantics by importing this module's own
primitives (`sha256_file`, `git`, `append_log`), so the hash discipline and the
move-never-destroy invariant are the same code, not a re-implementation.
`CENSUS2A_CLOSEOUT_2026-08-12.md` was deliberately excluded and stays on the bus:
it is the pickup document.

| rotated | file | new path | sha256 |
|---|---|---|---|
| 2026-08-15 | `BUILD_2026-08-12_CENSUS2A_RUN_1.md` | `docs/history/reports/2026-08/BUILD_2026-08-12_CENSUS2A_RUN_1.md` | `4eb5beb21c1771fcbc71805af0ba7aedc1478d23098f99b00e4e73dcd9f90485` |
| 2026-08-15 | `BUILD_2026-08-12_CENSUS2A_RUN_2.md` | `docs/history/reports/2026-08/BUILD_2026-08-12_CENSUS2A_RUN_2.md` | `fef8adc86fa6b9ed0ef0909075c3482a4cf884286bcade5d5b31f5c24c526b99` |
| 2026-08-15 | `BUILD_2026-08-12_CENSUS2A_RUN_3.md` | `docs/history/reports/2026-08/BUILD_2026-08-12_CENSUS2A_RUN_3.md` | `2de36f28d23713e7d93ee72adb97544431cb64e62c636de486dcacddacfa782e` |
| 2026-08-15 | `BUILD_2026-08-12_CENSUS2A_RUN_4.md` | `docs/history/reports/2026-08/BUILD_2026-08-12_CENSUS2A_RUN_4.md` | `a29bcb890f308a8703c60202dc93d8f59da686b5ca092d816dea2ebacf245025` |
| 2026-08-15 | `BUILD_2026-08-12_CENSUS2A_RUN_5.md` | `docs/history/reports/2026-08/BUILD_2026-08-12_CENSUS2A_RUN_5.md` | `0af4b2ba4321157628eeeb86e741327a02c9f94dedf1c447a271f1c29f47be6f` |
| 2026-08-15 | `BUILD_2026-08-12_CENSUS2A_RUN_6.md` | `docs/history/reports/2026-08/BUILD_2026-08-12_CENSUS2A_RUN_6.md` | `4abb0076f020f9e790c0db542aa28009fb96d4ba250b74bcc12d0e5b357f311c` |
| 2026-08-15 | `BUILD_2026-08-12_CENSUS2A_RUN_7.md` | `docs/history/reports/2026-08/BUILD_2026-08-12_CENSUS2A_RUN_7.md` | `473ed3cd411c813cc17c1829a2a7549d95d189250541f936f5d66256ec7ebed7` |
| 2026-08-15 | `BUILD_2026-08-12_CENSUS2A_RUN_8.md` | `docs/history/reports/2026-08/BUILD_2026-08-12_CENSUS2A_RUN_8.md` | `bd53072ff61ee322554a1c235c2bb6ddb5c64b4761339f923dfeacb90c2f7e46` |
