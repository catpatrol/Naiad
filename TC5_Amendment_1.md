# TC-5 — Amendment 1 (pre-registration halt): the align-frame ruling

**Date:** 2026-07-20 · **Authority:** builder halted at pre-registration — `tf_align=15m` is infeasible config-only (`signals.py:152` indexes `mtf[cell.tf_align]`, built solely from MTF_SET {5m, 1h, 4h, 12h}; `replay.py:79` loads {exec, gov} ∪ MTF_SET; 15m is never loaded). Nothing was run, priced, or pre-registered; a G-7 entry whose cells cannot execute would be void. Halt + pinned v1 numbers committed at `1731793`. The align frame is experiment-defining (grade → R1 size → every traded number), so the builder correctly escalated instead of substituting. This document is the reviewer's ruling; operator veto stands on silence.

---

## 1. On the record

1. **Reviewer spec error:** Amendment author's own veto-V1 default (15m, "role-preserving") was unrealizable, not merely unloaded. Logged.
2. **The invariant, corrected:** v1's cross-mandate pattern is `tf_align` = **one MTF_SET rung below the governor** (5m↓1h · 1h↓4h · 4h↓12h) — not "one above exec." At 1H/5m, that rung *is* the exec chart: the invariant cannot survive this scale.
3. **The structural finding (keep it):** exec=5m and gov=1h are adjacent MTF_SET rungs — **the 1H/5m mandate has a compressed confluence ladder.** Feeds the registered SSv12 relative-steps note, now with a resolution-floor clause. Related: the evidence's informative TF for a 1H-governor book (30m, RC-7r FH-3) is also absent from MTF_SET — a future MTF_SET question, explicitly out of this phase.
4. **Pinned v1 same-asset subset (committed, reused — do not recompute):** net 1× **−1,362.56** · gross 0× **+113.04** · 1,550 campaigns · 3,664 tranches · median `mfe_bps` **13.04** vs toll **19.96** → **ratio 0.65** · **5/5 halted** (BTC 2022-04-11 · ETH 2022-07-15 · SOL 2023-04-28 · NEAR 2023-01-21 · ZEC 2022-06-01).

## 2. The ruling

**`tf_align = 1h` (the governor) for all five v2 cells** — the v2 triple is **(gov 1h, exec 5m, align 1h)**.
Rejected: **B** (align=exec — A-grade near-tautological at the reclaim; grade distinction collapses and grade drives size) · **C** (add 15m to MTF_SET — alters CLUSTER/TPW for every cell; breaks single-variable isolation and "MTF_SET unchanged") · **D** (engine edit — breaks F-ENG in a config-only phase).
Adopted rationale: config-only; the unrealizable one-below-gov invariant's nearest coherent substitute; "full size only when the governor ribbon agrees" is stricter grading in the conservative direction; FH-3 shows governor-ribbon alignment carries real (stage-adjacent) separation.

## 3. Contract deltas (exhaustive — nothing else changes)

- **§1:** `tf_align` **15m → 1h**; add the printed caveat line to every deliverable header: *"v2 align sits AT the governor — no strictly-between rung exists at this scale (compressed ladder)."*
- **§4 F-SPEC:** expected header becomes gov=1h, exec=5m, **tf_align=1h**.
- **§5:** P-TC5-a's bar concretized: v1 pinned ratio 0.65 → the ≥2× form means **≥ 1.30**. **New row P-TC5-f:** median `mfe_bps`/toll ratio (v2) ≥ **1.0** — the economic break-even — prior **65%**, falsified if < 1.0. (Registered now, legitimately: no v2 data exists.) All other rows carry verbatim.
- **§6:** grade-census deliverable gains one column: A-grade share of fills, v2 vs v1 subset (the align semantics changed; measure it, don't assume it).
- Ledger: the halt entry stands as committed; the amendment entry (§4 below) is appended; the G-7 pre-registration proceeds referencing the already-committed pinned numbers.

## 4. Ledger entry (builder-typed, append-only)

```
[2026-07-20] TC-5 AMENDMENT 1 — align-frame ruling after infeasibility halt.
tf_align=15m unrealizable config-only (not in MTF_SET; never loaded). Reviewer spec
error logged. Structural finding: 1H/5m has a compressed confluence ladder (exec and
gov are adjacent MTF_SET rungs; the one-below-gov align invariant cannot survive this
scale) → SSv12 relative-steps note gains a resolution-floor clause. RULING: tf_align=1h
(governor) — triple (1h, 5m, 1h); B degenerate, C breaks isolation, D breaks F-ENG.
P-TC5-a bar = ratio ≥ 1.30 (2 × pinned 0.65); P-TC5-f added: ratio ≥ 1.0, prior 65%.
Pinned v1 numbers at 1731793 reused verbatim. Pre-registration authorized to proceed.
```

## 5. The amended go-paste

```
CONTRACT: TC-5 — re-run from pre-registration under Amendment 1

Read TC5_Amendment_1.md, then the original TC5_Intraday_Respec_Builder_Contract.md.
The amendment overrides tf_align (1h), F-SPEC, adds P-TC5-f and the A-grade-share
column, and concretizes P-TC5-a's bar at 1.30. Everything else carries unchanged.

Order of work:

1. Append the §4 amendment ledger entry.
2. G-7 PRE-REGISTRATION — five config shas with tf_align=1h, all SIX prediction rows
   (a–f), referencing the pinned v1 numbers committed at 1731793 (do not recompute).
   Commit BEFORE creating any run.
3. RUN the five cells twice into research_outputs/tc5/. Engine tree untouched.
4. FIXTURES — F-ENG first (diff vs 6fdab03 lineage must be EMPTY apart from configs,
   contracts, and ledger). Any MISMATCH: HALT.
5. DELIVERABLES per the original §6 plus the A-grade-share column and the
   compressed-ladder caveat line on every table.
6. PREDICTIONS — all six, falsifications first. Artifacts + completion ledger. Commit.
   Do not push, do not merge.

Do NOT: touch the engine or MTF_SET · substitute any other align frame · recompute or
alter the pinned v1 numbers · apply any TC-1 architecture key · touch the lockbox.

Report back: pre-registration confirmation, fixture table, the thesis table (mfe_bps
vs toll, v2 beside pinned v1), per-cell headlines, the six-row scorecard, both hashes,
tc5_results.json.
```

---

*Amendment prepared by the reviewer under Fable-mode, 2026-07-20. The 15m spec died at the source-code wall it should have died at, before a single config existed — and left behind a real finding: the fractal port compresses the ladder, and the grading frame must live on the rungs that exist. The v2 mandate now trades stricter-graded than its parent, which is the right direction for a book being rescued from its own toll.*
