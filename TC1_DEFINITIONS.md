# TC-1 — §2 Architecture Definitions (pinned at G-7 pre-registration)

Canonical restatement, hashed into the pre-registration ledger entry.

1. **Structural stop (cells B, D) — birth rule.** At a tranche's fill, its stop is
   set to the nearest confirmed (5,5) pivot on the **1h** frame strictly beyond the
   entry (pivot low below fill for a long; pivot high above fill for a short),
   confirmed (pivot+5 on the 1h frame, visible by the exec fill bar) within a 200-bar
   1h lookback, offset ∓ 0.5·ATR_exec(signal bar) — long: pivot_low − 0.5·ATR;
   short: pivot_high + 0.5·ATR. If no confirmed pivot exists in the lookback, the
   tranche is **not taken** — a `no_struct_anchor` REJECT (a birth-time architecture
   constraint, not a void; S-2b measured ≈0 at 1h, but the rule exists). Sizing uses
   the structural distance as unit_risk, so qty scales with 1/structural_distance and
   realized_r is natively **struct-R** (a full stop is −size_r R regardless of stop
   width).

2. **Static-for-life (B).** The structural stop never moves after fill — no
   event-ratchet, no advance. Its exit price at exit == its stop at entry, every
   tranche (F-ARCH-B). Because it sits below entry (long), the BE add-gate — which
   admits an add only when every prior open tranche's live stop is at/beyond
   breakeven — can essentially never pass in B: (fill − struct)·dir > 0 always. So B
   is near-pyramid-free by construction (adds → `add_ineligible`).

3. **G-8c interaction.** The structural distance is ≥ the 1h pivot distance ≥ the
   0.5·ATR_exec floor by construction, so G-8c's min-stop never binds at 1h — asserted,
   not assumed.

4. **Trail (C, D) — engagement and one-way.** Engagement = the first exec close beyond
   the cell's **governor e200** in the trade's favor after fill. Pre-engagement the
   working stop is the cell's native phase-1 stop (native ratchet in C; the static
   structural stop in D). At engagement the trail seeds at the standing stop (native
   ratchet's value in C; the structural stop in D). Post-engagement the working stop
   is the **one-way tighten** (max for long, min for short — never loosens) of the
   trail line `gov_e200 ∓ 0.5·ATR_exec`. In C the native advances are ignored after
   engagement (fold-in frozen). In **D the post-engagement stop = max(trail line,
   structural floor)** — it can only tighten from the structural floor upward, never
   below it. Exit on touch, in the engine's wake order (queued open-flatten → gap →
   intra-bar; coverage from the fill bar).

5. **Everything else identical across A/B/C/D.** signal layer byte-untouched
   (architecture lives entirely in the trading layer); G-8 guards, sizing table, the
   BE add-gate (testing each cell's own live stop), max_tranches, cooldowns, fee/slip
   model, window, seeds — all unchanged. Absent config keys (`stop_mode`,
   `exit_trail`) reproduce baseline behavior exactly (cell A byte-identity is the
   proof).

6. **Expected path effects (measured, not written away).** In B/D the structural
   stop's long holds keep the book occupied, suppressing while-flat re-entries →
   tranche counts fall materially (predicted ≤70% of A's 6,304). B is near-pyramid-free
   (per (2)). Window-end open tranches grow under long holds (1.0.8 emission rule) →
   `fills_without_exit_row` reported per cell. These are real-run path effects the
   first-order S-2b tables could not see — the point of the phase.
