# TIER-C10 · OPERATOR RULINGS — RECOVERED VERBATIM

**Provenance.** These rulings were given by the operator on 2026-09-21T22:46:10Z in the
builder session `730798c3-4e2c-4d67-8a9b-be6f9aae52f5`. That session was killed by an
API 529 at 2026-09-22T01:06:58Z and its scratchpad — which held the only copy
(`OPERATOR_RULINGS.md`) — was destroyed with it. The text below was recovered on
2026-09-22 from the surviving session transcript
(`~/.claude/projects/-Users-luis-Naiad/730798c3-4e2c-4d67-8a9b-be6f9aae52f5.jsonl`, user
message at line 268) and is reproduced **verbatim**. It is filed here, inside the build
tree, so that it survives the next interruption.

**Standing.** These are the operator's words. Where an executor lean operationalises one,
the lean is marked as such and is NOT the ruling.

---

## Verbatim

> See decisions on pending items,
>
> 1- The RB3 hold pins and the EMA-band definition
> Let's try the 89/127 ribbon, the 127/200 ribbon, and taps on each ema. Feel free to search data from past runs to tune the defaults
>
> 2- The panel for P-BRK-S1 and P-BRK-I1.
> All 17
>
> 3- P-SPR-2's population, scored arm and top-side upthrusts.
> Full corridor, standalone vs zero, top side in, we trade both ways
>
> 4- What "daily 12/25 direction" and lens-scaled bell and harvest mean.
> It means we observe the transition from expansion of the bands, into consolidation and closing of the bands. This is followed by new expansion, either as continuation or as reversal, a final cross after the interweaving of the ema turns to expanding the ribbon between the ema's
>
> 5- Which Binance publication is the record.
> The USDT pair, either on Binance or Bybit
>
> 6- The LaCie destination and consent to push, which I'll ask for again at close.
> Permission to push granted

---

## Operationalisation (EXECUTOR LEANS — not the operator's words)

- **R1 → bands.** Candidate set pinned as `{ribbon-89/127, ribbon-127/200, tap-89, tap-127,
  tap-200}`. "Feel free to search data from past runs to tune the defaults" is read as
  permission to fit the hold pins — so, to keep the scored arm honest, the executor tunes on
  the era `<= 2024-06-30` **only** and scores P-BRK-S1 on the holdout era
  (`>= 2024-07-01T00:00:00Z`). The era cut instant is `1719791999000` ms (the last instant of
  the tuning era); `cut+1 ms` is the first instant of the holdout.
- **R2 → panel.** BRK panel = all 17. **CONFLICT:** the RESUME contract of 2026-09-22 carries a
  PANEL PIN reading "both BRK forms score on the 5-asset book per G-7; the 17-asset view is
  Tier-E", which contradicts this ruling. Filed as a finding; the operator settles it.
- **R3 → P-SPR-2.** Full corridor (not exploration-classic era only); scored arm is
  standalone vs zero; top-side upthrusts included; both directions traded. **CONFLICT:** the
  contract text for P-SPR-2 reads "4h, 5-asset exploration-classic, vs card/standalone".
  Filed as a finding; the operator settles it.
- **R4 → ribbon lifecycle.** "Daily 12/25 direction" is a LIFECYCLE, not a bare cross:
  expansion → consolidation/interweaving → final cross → new expansion (continuation or
  reversal). Executor pins K=3 for the consolidation test and rings the bell also on the
  counter 12/25 cross.
- **R5 → publication of record.** The USDT pair on Binance or Bybit. This does **not**
  distinguish the venue's REST API from its BULK ARCHIVE publication, and those two disagree
  on a handful of incident bars. So **F-D-1 stays RED and is printed RED**; F-D-1b (which asks
  BOTH publications for every bar and checks label consistency) carries the load.
- **R6 → push.** Permission granted. Destination is still unnamed by the operator; the real
  vault is `/Volumes/LaCie/Repo Clone/naiad-backups` and the default destination would create
  an empty vault, so the mirror must be invoked with an explicit `--dest`. The operator said
  they will be asked again at CLOSE.

## Still blocked on the operator (no text exists on disk)

- The PANEL conflict (R2 "all 17" vs the resume contract's PANEL PIN "5-asset book").
- The P-SPR-2 population conflict (R3 "full corridor" vs the contract's "exploration-classic").
- Which NULL variant is the record (`gaps-only`, the contract-literal design, vs `gaps+order`,
  which reduces a measured own-window leak from 25.62% to 7.97%). Both are filed side by side.
- Whether the 5m HOLD RATE is part of P-BRK-S1's scoring ground (if so it needs the same
  era collar the outcome rows have).
- PUMPFUN → PUMPUSDT and MNT → Bybit are printed LEANS, not rulings; they need the nod at CLOSE.
- The LaCie destination.

---

# RULINGS OF 2026-09-22 (R7–R10)

Given by the operator during the RESUME-AND-FINISH session, in answer to the four conflicts R0's
completeness census surfaced. Filed the moment they were given.

## R7 · LAW 4 governs the CORRIDOR PIN, not stage completeness

**Ruled: "Corridor pin only."** LAW 4's clause — *"if Stage D is not complete, re-pin at resume and
redo everything downstream"* — protects the as-of pin. It does **not** order the destruction of
stages that verify clean merely because Stage D lacks four *report* artifacts.

Nothing is re-pinned. Nothing downstream is recomputed. The five COMPLETE-VERIFIED stages
(STEP 0 · NULL/gaps-only · NULL/gaps+order · A · PANEL) stand. The corridor remains
**AS_OF 2026-09-21T16:00:00Z**, substrate frozen at `tc10_20260921`, `live_cache_touched: false`.

*Basis:* all 119 Stage D manifest shas re-hash (twice), the write-once seal holds on all four
records, and the corridor never moved. What Stage D lacks — F-D-4, F-D-5, the haircut twin,
contract multipliers — are report artifacts that cannot move an as-of.

## R8 · The BRK panel is the 5-ASSET BOOK — the PANEL PIN governs

**Ruled: "5-asset book — the PANEL PIN governs."** This **supersedes ruling R2 of 2026-09-21
("All 17")**, on the operator's own word.

- P-BRK-S1 and P-BRK-I1 score on CLASSIC5 (BTC ETH SOL NEAR ZEC), per G-7.
- LOAO above-half bar = **3/5**.
- The 17-asset view prints as **Tier-E** beside each BRK row.
- The gap against R2 is filed as a finding in the build doc, as the contract's PANEL PIN requires.

`scripts/tierc10_brk.py` scores on whatever panel the *registration* names (`g["panel"]`), so this
is a registration-text decision, not a code change.

## R9 · P-SPR-2 rides R3 — FULL CORRIDOR, BOTH WAYS

**Ruled: "R3 governs — full corridor, both ways."** Ruling R3 of 2026-09-21 is later than the
contract's frozen text and **supersedes** it.

- Population: the **full corridor** — *not* the exploration-classic era (≤ 2024-06-30).
- Scored arm: **standalone vs zero**.
- **Top-side upthrusts are IN**; both directions are traded.
- The contract's frozen wording — *"4h, 5-asset exploration-classic, vs card/standalone"* — prints
  as the **superseded draft**, recorded so the change is visible and not silent.

## R10 · The NULL of record is `gaps+order`

**Ruled: "gaps+order — the leak-reduced one."**

- `gaps+order` is the null of record. It cuts the measured own-window overlap from **25.62% to
  7.97%** over 1,020 draws, so the foil is fairer.
- `gaps-only` — the contract-literal design — remains **filed and printed beside it**, never deleted.
- The two disagree on **3,455 of 19,926** comparable summary cells by sign and 2,469 by q75
  clearance, including the headline cell *5m DIE, era ALL, H20 net*. Every such disagreement is
  printed, not hidden.
- Under the null of record, 4h retest-hold-tap89 sits at **percentile 100** (real +0.3168 vs null
  median +0.0689, q25 −0.026, q75 +0.162) rather than 90.
- **K=20 resolves a percentile to 5 points at best. It is a DESCRIPTION, never a p-value.**

## Still blocked on the operator after R7–R10

- **F-D-1 / R5.** "The USDT pair, either on Binance or Bybit" names the pair and permits the venue,
  but the actual disagreement is the venue's **REST API vs its BULK ARCHIVE**, which publish
  different bars on incident stamps. F-D-1 stays RED and is **printed RED**; F-D-1b carries. No bar
  is rewritten either way without the narrower word: **REST or ARCHIVE?**
- **The 5m HOLD RATE.** If it is part of P-BRK-S1's scoring ground it needs the same holdout-era
  collar the outcome rows carry. Executor is proceeding on the **conservative** reading (collar it),
  and will say so on the row.
- **PUMPFUN → PUMPUSDT** and **MNT → Bybit** remain printed LEANS, not rulings; they need the nod at
  CLOSE.
- **The LaCie destination** (R6 granted permission to push; the destination is still unnamed, and the
  default would create an empty vault — the real one is `/Volumes/LaCie/Repo Clone/naiad-backups`).
