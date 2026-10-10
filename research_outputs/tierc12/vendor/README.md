# TC12 vendor referee

`tierc11_env@1526093b.py` is a byte-for-byte copy of TC11's `scripts/tierc11_env.py`, taken from the main tree at the record `TC12-ENV.vendor` — after TC12-D, before any hunk is applied (LEANS L-D.25; ruling O-31).
- sha256 `1526093b25161927337ced6112a310075b1a57c825f08705814e48619398f798`, 68545 bytes, 1381 lines.
- This is the sha `research_outputs/tierc11/PROGRESS.json` certifies for `scripts/tierc11_env.py` under stage `TC11-ENV`, read by key from `artifact_shas`. The tag `1526093b` in the file name is a label that prefixes it.
- Three shas are held equal: this copy's, the certified one, and the live `scripts/tierc11_env.py`'s. `scripts/tierc12_vendor.py --verify` and F-VENDOR `[referee]` (`scripts/tierc12_env_fixtures.py --stage=TC12-ENV.vendor`) hold them. A difference in the live file is a moved TC11 byte, a finding against O-3.

It is filed here, tracked, so that the referee survives any later TC11 edit and exists in every tree, detached review worktrees included. The file is never imported and never run. `scripts/tierc12_env.py` is built from it by the declared hunks of `scripts/tierc12_vendor.py` (`ENV_HUNKS`) and nothing else; F-VENDOR reverts them and must meet this file byte for byte.
