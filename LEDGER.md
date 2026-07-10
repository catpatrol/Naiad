# Data-Spend Ledger

*Maintained by the REVIEWER only (charter §2). The builder proposes entries in
its session summary; the reviewer decides what lands here. Governing rule:
reading a result spends the data, whether or not you act on it. Never read a
proxy of a measurement we can afford to make for real.*

## Opening entries (charter §6, at ratification 2026-07-09)

|Dataset|Status at ratification|
|-|-|
|BTC, all TFs, 2025-10-06 → 2026-07-07|**SPENT for validation** (fitted twice: the nine-month study and the v11.0.2 verification cycle). Parity fixtures and characterization only.|
|All assets, first valid candle → 2025-09-30, excluding the row above|**Characterization set.** All tuning lives here and only here.|
|All assets, everything before 2022-01-01 (BTC/ETH ≈ 2019–2021: Covid crash, 2021 blow-off)|**SEALED retro holdout.** Read **once**, against the pre-registered bar in charter §7. The read spends it regardless of outcome.|
|Forward paper journals|**Virgin, renewable.** Honest exactly once per frozen ruleset; each window is a one-shot exam.|

## Entries after ratification

*(none yet — reviewer appends here)*

*## 2026-07-10 — Phase 1 packet review (naiad\_packet\_20260710\_1303.zip, git c97fc31)*



*- \*\*Data touched:\*\* BTCUSDT\_swing journal 2026-05-01→07-07 and D5 parity artifacts 2025-10-06→2026-07-07 — entirely inside the \*\*hard-spent\*\* BTC window. \*\*Fresh evidence spent: none.\*\* All numbers handled as plumbing characterization under the charter's spent-window rule.*

*- \*\*Looks logged:\*\* reviewer recomputed equity, tranches, halts, signal-event decomposition, cost anatomy, ratchet paths, parity cross-consistency, schema completeness from raw journal bytes. D7 capture/tail table seen and explicitly \*\*not\*\* interpreted (n=10, spent).*

*- \*\*Verdict:\*\* CONDITIONAL PASS — see `Phase1\_Reviewer\_Verdict.md`. Conditions: D-1 fix (summary rows/sha must be computed from persisted files; disk shows 1502 rows vs claimed 1503, sha not reproducible from disk bytes), operator D5/F6 TradingView sign-off incl. the V-signature fork (Feb 6 / Jun 22, 5m vs 4H chart), operator charter eyeball (§3.4 sizing five-tuple; §3.5 live-exit = survival stop only, playbook exits shadow-only; v\_births\_provisional charter-wins; halt\_scope per\_cell).*

*- \*\*Standing reminders:\*\* holdout partitions for Phase 2 remain undefined/unlocked (Decisions P2-1..P2-3 pending ratification); collector remains OFF; nine-month BTC window remains spent and may never serve as out-of-sample validation.*

*### Addendum 2026-07-10 (afternoon): tickets D-1..D-3 closed; basket backfill complete*

*- Reviewer re-verified packet naiad\_packet\_20260710\_1448.zip (git c2ae143): formula-reproducible*

&#x20; *journal\_sha256 5b7e4b333e364af394f55da6840c2d4dd89cc43c70003bcd98dc365e67e5b5ee, rows 1502,*

&#x20; *29/29 file hashes match, journal diff = 2 HALT rows only (D-2). Fixtures 25 green incl. F1b.*

*- Known journal caveat (pending 1.0.1): same-bar reject key collisions drop duplicates; reject*

&#x20; *counts are lower bounds until subkey fix lands.*

*- --all backfill complete: 60/60 series, 0 duplicates, one 1-bar gap (BTC 1m, listing day).*

&#x20; *LIT floor verified on all 6 intervals: first candle 2025-12-23 (nothing pre-Lighter). §5c closed.*



