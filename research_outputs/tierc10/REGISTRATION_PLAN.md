# TIER-C10 · STAGE B — THE REGISTRATION PLAN

**Status: STRUCTURE ONLY. No text is filed. No lane has ridden a real book.**

This file pins the *structural* parameters of all six registrations — panel, era, ruler, base,
runner, lanes, LOAO line, which arm owns the family slot — before any text is written and long
before any result is read. The texts themselves are drafted, reviewed and filed separately.

Why it exists: `draft:registrations` died on an API 529 on 2026-09-22T01:06:58Z and took the only
copy of its work with it. The structure is recorded here so that cannot happen twice.

## The machinery these must satisfy

`scripts/tierc10_panel.py` — read it before drafting, it refuses more than it accepts.

- `FAMILY_M = 6` · `N_BOOT = 4000` · `SEED = 20260921` (drives **every** ruler: one-sample,
  two-sample and equal-asset-risk). Sensitivity seed 20260816 is the estate's lineage seed.
- `RULERS = ("vs_zero", "two_sample", "set_change")` · `BASES = ("zero", "card-v6")`.
  `vs_zero` ↔ `zero`; any twin ruler ↔ `card-v6`. A mismatch HALTs.
- `RUNNERS = ("run_cell_n", "external")`. Give **both** `card` and `roles` (ridden through
  `run_cell_n`) or **neither** (external runner, which must enter through `require_arm`).
- `ERAS = ("full", "tuning", "holdout")`, cut at `2024-06-30T23:59:59Z` = `1719791999000` ms.
  The era is **mandatory** on every arm — "an era chosen after the look is a choice of the
  friendlier sample."
- `LOAO_LINES = ("lineage", "excl_zero_campaign")`. Every arm must name one, the **same** on all
  arms, and the registration TEXT must contain `loao_line_clause(choice)` **literally** or
  `register()` refuses the filing before a registry line exists.
- `above_half_bar(N) = ceil((N+1)/2)` → **3/5 · 7/12 · 9/17**. The contract's "LOAO above-half 3/5"
  is the N=5 case of this law, not a different rule [LEAN L6]. Print the generalisation in each text.
- **At most ONE arm per registration may carry `scored_in_family=True`.** Every other arm is
  report-only (Tier-E).
- A filed registration is **never amended**. Re-filing identical bytes is a no-op; different text
  under a filed id HALTs; filing an id that already has a `.scored.json` HALTs.
- **WITNESS_LAW:** the registrations directory is gitignored, so `registry_len` and `registry_head`
  returned by `register()` must be pinned in a **tracked** file or the chain has no witness.

## Rulings in force

R8 → the BRK panel is **CLASSIC5**, above-half **3/5**, the 17-asset view Tier-E. *Supersedes R2.*
R9 → P-SPR-2 rides the **full corridor**, **standalone vs zero**, **top side in, both ways.**
R10 → the null of record is **gaps+order**.

## The six

| id | prior | panel | N | bar | era | ruler / base | runner | lanes |
|---|---|---|---|---|---|---|---|---|
| P-GEN-1 | 45% | UNSEEN12 admitted | 12 | 7/12 | full | vs_zero / zero | `run_cell_n` | card |
| P-SPR-2 | 45% | CLASSIC5 | 5 | 3/5 | full | vs_zero / zero | external | spring |
| P-BE-1 | 40% | CLASSIC5 | 5 | 3/5 | full | twin / card-v6 | external | card |
| P-TRG-2 | 40% | CLASSIC5 | 5 | 3/5 | full | twin / card-v6 | `run_cell_n` | card |
| P-BRK-I1 | 35% | CLASSIC5 | 5 | 3/5 | full | vs_zero / zero | external | brk-i1 |
| P-BRK-S1 | 30% | CLASSIC5 | 5 | 3/5 | **holdout** | vs_zero / zero | external | brk-s1 |

`CLASSIC5 = (BTCUSDT, ETHUSDT, SOLUSDT, NEARUSDT, ZECUSDT)`.
`UNSEEN12 admitted = (ENAUSDT, PUMPUSDT, HYPEUSDT, MNTUSDT_BYBIT, SUIUSDT, LTCUSDT, XMRUSDT,
BNBUSDT, UNIUSDT, 1000PEPEUSDT, DOGEUSDT, 1000BONKUSDT)` — `panels.UNSEEN_admitted_stems`, the only
reading under which the contract's "the ADMITTED twelve" (line 92) and "the ADMITTED LIST ... IS
P-GEN-1's panel" (line 50) agree, since the admitted list on disk is all **seventeen**.

### Per-registration notes

**P-GEN-1** — card v6, **all pins frozen**, `card=CARD_V6, roles=V6_ROLES`. Tier-E arms beside the
scored one: the 17-asset view, and the **never-touched** view. The contract demands "LOAO printed
twice (all admitted · never-touched only)"; F-D-5 measured the never-touched set as exactly
**PUMPFUN, MNT, SUI** (3 assets, bar 2/3) — the other nine unseen assets are *display-only*, having
appeared in the Oracle's 18-symbol roster or the frozen study basket. **This weakens the "twelve
unseen" premise and the text must say so**: only 3 of the 12 are virgin. Haircut twin on every row.

**P-SPR-2** — `CARD_SPR2 = Card(name="tc10-spring-standalone", lane="spring")`. Per R9 the scored
arm is **standalone vs zero over the full corridor with top-side upthrusts in**. The contract's
frozen wording ("4h, 5-asset exploration-classic, vs card/standalone") is the **superseded draft**
and prints as such — "exploration-classic" was an *era* (≤ 2024-06-30), not a panel. A vs-card twin
may print as Tier-E.

**P-BE-1** — external runner; the lane is the v6 card with the breakeven floor at first tape +1R,
**SEQUENCED** (dip before/after +1R read from tape order). Registered pin `be_floor_after_r = 1.0`.
The `set_change` law picks two-sample vs paired from whether the campaign-key set moved — read
`_set_change_law` and `_rule` before choosing the ruler string. **F-C10-BE cannot run until this is
filed** (`BE_CAMPAIGNS` is an empty tuple until then).

**P-TRG-2** — `run_cell_n` with `roles = tierc9.Roles(name="trigger-9/12", trg_f=9, trg_s=12)`
(already in `tierc9.py:129`). **CLASSIC5 only** — trigger 9/12 is deliberately *not* run on the
unseen twelve, so that panel stays virgin for P-GEN-1. This is the one grid pre-naming.

**P-BRK-I1** — 1d macro DIE → first flip-hold on the **memory-line** → enter; stop beyond retest
extreme, rail 1.0 ATR(1d); permission = weekly 12>25 posture AND the daily 12/25 **ribbon lifecycle**
per R4 (expansion → consolidation/interweaving → final cross → new expansion; K=3, bell also on the
counter cross). Net 10 bps + funding. `LANE_ERA` = `full`. Tier-E: the EMA-band anchor, and the
17-asset view. **Carries the 1d height-vs-toll verdict on its row.**

**P-BRK-S1** — 5m macro DIE → first HOLD retest of the tuned band → enter at hold close; stop beyond
retest extreme, rail 1.0 ATR(5m); 4h tide aligned. **Era `holdout` is mandatory and now enforced in
code**: R1's protocol tunes on ≤ 2024-06-30 and scores on the holdout, so a filing at `era="full"`
would score the scalper in-sample on the very grid that chose its pins.
**The resume paste's "(FLIP_HOLD pins)" is a drafting error** — FLIP_HOLD (1.0 ATR / 6 bars) is
P-BRK-I1's *memory-line* pin set. The band set actually built and tuned per R1 is
`{ribbon89_127, ribbon127_200, tap89, tap127, tap200}`, tuned to **ribbon127_200 / margin 1.0 ATR /
hold 3 bars / ttl 400**. No text may quote FLIP_HOLD for S1.
**Carries the 5m height-vs-toll verdict on its row — and that gate FAILS** (0/17 single assets pass
at 5m, on either scale kind). The text must not promise what the gate denies.

## What no text may do

- Quote a pin it did not read from the filed artifact.
- Name an era after the look, or omit one.
- Omit the LOAO clause, or name a different count on different arms.
- Claim more than one scored arm.
- Promise a result. The text is a claim about *what will be measured and how*, filed before the look.
