# D7 — Dry-run autopsy: BTCUSDT_swing, 2026-05-01 -> 2026-07-07

**SPENT WINDOW — every number here is a plumbing check, never evidence** (build prompt §1). Purpose: prove the journal alone answers every question in `fixtures/autopsy_questions.md`. Sample: 10 fills / 10 resolved tranche exits — far below the ≥20-per-cell read floor (charter §4); no conclusions may be drawn, only column liveness.

Run: `97f51466113cdcf9` · engine 1.0.0 · config naiad_v0 · 1503 journal rows · journal sha256 `5be17e5d1f6608ec…` · final equity 9619.04 · 2 halt(s)

## Q1 — Loss by cohort

| cohort | n | Σ realized_r | mean |
|---|---|---|---|
| NEVER_GREEN | 3 | -3.202 | -1.067 |
| STILLBORN | 3 | -1.869 | -0.623 |
| FADED | 0 | 0 | - |
| PROTECTED | 4 | -2.678 | -0.670 |

## Q2 — MFE/MAE by grade / zone / tier

| slice | n | mean mfe_r | mean mae_r |
|---|---|---|---|
| grade=- | 1 | 2.944 | -1.896 |
| grade=A | 3 | 0.117 | -2.692 |
| grade=B | 6 | 2.493 | -1.402 |
| zone=Z1 | 9 | 1.838 | -1.836 |
| zone=Z2 | 1 | 1.711 | -1.858 |
| tier=full | 3 | 0.117 | -2.692 |
| tier=provisional | 7 | 2.557 | -1.473 |

## Q3 — Pre-engagement death share (X-A trail)

6/10 tranches died before the e200 trail engaged (60% — the X0 lesson metric).

## Q4/Q5 — Capture ratio and tail capture (incumbent vs X-A..X-D)

| exit | mean capture (realized/MFE, MFE>0) | tail trades (MFE>5R) | tail captured (>3R) |
|---|---|---|---|
| incumbent (survival stop) | -1.603 | 1 | 0 |
| X-A | -1.136 | 1 | 0 |
| X-B | -1.136 | 1 | 0 |
| X-C | -1.051 | 1 | 0 |
| X-D | -1.094 | 1 | 0 |

*Tail-capture outranks give-back in every exit report (charter §3.3).*

## Q6 — ATR entry vs exit; post-exit continuation

| tranche | atr entry | atr exit | cont+1 | cont+5 | cont+20 | cohort |
|---|---|---|---|---|---|---|
| c32t1 | 72.00 | 72.73 | 0.353 | 0.351 | 1.994 | STILLBORN |
| c32t2 | 65.59 | 65.32 | -2.007 | -0.259 | -1.910 | PROTECTED |
| c32t3 | 65.47 | 65.32 | -0.850 | -0.110 | -0.809 | PROTECTED |
| c33t4 | 109.94 | 102.48 | -0.214 | -0.448 | 2.079 | PROTECTED |
| c34t5 | 135.19 | 137.39 | -0.492 | -0.606 | 0.627 | STILLBORN |
| c34t6 | 125.61 | 127.00 | -0.023 | -0.329 | 0.134 | NEVER_GREEN |
| c34t7 | 114.60 | 127.80 | -1.066 | -1.537 | -0.335 | NEVER_GREEN |
| c35t8 | 55.52 | 51.54 | 0.679 | 0.500 | 3.700 | STILLBORN |
| c35t9 | 49.00 | 44.15 | 0.918 | 3.448 | 3.415 | NEVER_GREEN |
| c35t10 | 53.88 | 57.47 | -0.756 | -2.422 | -1.202 | PROTECTED |

*(ATR at each ratchet step = `atr_exec` on the campaign's PRIME/CONFIRM/V rows — present in the journal, joinable by time.)*

## Q7 — Adds vs sizing counterfactuals

R1/V tranches: n=4, Σ realized_r=-2.265, Σ shadow full-1R-at-R1=-7.462
ADD tranches: n=6, Σ realized_r=-5.485, Σ shadow big-adds=-10.970

## Q8 — Shadow lines on identical data (per resolved exit)

| tranche | XA | XB | XC | XD | alt-anchor R | vol-buf R | strict? | unthr. size |
|---|---|---|---|---|---|---|---|---|
| c32t1 | -1.000 | -1.000 | -1.000 | -1.000 | -1.688 | -1.000 | False | 0.50 |
| c32t2 | 1.701 | 1.701 | 1.701 | 1.701 | 0.796 | 0.873 | False | 0.50 |
| c32t3 | -0.089 | -0.089 | 0.506 | 0.209 | -1.059 | -1.027 | False | 0.50 |
| c33t4 | 1.022 | 1.022 | 1.022 | 1.022 | 0.394 | -1.000 | False | 0.50 |
| c34t5 | -1.000 | -1.000 | -1.000 | -1.000 | -1.515 | -1.000 | True | 0.50 |
| c34t6 | -1.000 | -1.000 | -1.000 | -1.000 | -3.116 | -2.468 | True | 0.50 |
| c34t7 | -3.704 | -3.704 | -3.704 | -3.704 | -3.704 | -3.704 | True | 0.50 |
| c35t8 | -1.000 | -1.000 | -1.000 | -1.000 | -1.509 | -1.000 | False | 0.50 |
| c35t9 | -1.000 | -1.000 | -1.000 | -1.000 | -1.539 | -1.356 | False | 0.50 |
| c35t10 | -0.608 | -0.608 | 0.296 | -0.156 | -2.011 | -1.009 | False | 0.50 |

## Q9 — Give-back

Mean give_back_r on MFE>0 exits: 3.495; per-variant give-back = mfe_r − exit_X* (columns live, Q8 table).

## Q10/Q11 — Funnel: signals -> fills, reject mix

PRIME events: 293; fills: 10; trade-path rejects: 373; signal-gate rejects: 453.

| reject_reason | n |
|---|---|
| no_zone | 296 |
| max_tranches | 275 |
| not_positioned | 90 |
| ribbon_sep | 55 |
| bar_range | 41 |
| c_gate_no_zone | 39 |
| cooldown | 22 |
| gap_through_stop | 8 |

## Q12 — Expectancy by zone at equal grade

| zone | grade | n | mean realized_r |
|---|---|---|---|
| Z1 | - | 1 | -0.886 |
| Z1 | A | 3 | -0.933 |
| Z1 | B | 5 | -0.733 |
| Z2 | B | 1 | -0.396 |

## Q13 — The sniper-pocket question (retr bands, ALL PRIMEs)

| retr band | PRIMEs | filled exits | mean realized_r |
|---|---|---|---|
| [-9, 0) | 200 | 0 | - |
| [0, 0.25) | 60 | 9 | -0.763 |
| [0.25, 0.5) | 25 | 0 | - |
| [0.5, 0.786) | 8 | 0 | - |
| [0.786, 1.0) | 0 | 0 | - |
| [1.0, 9) | 0 | 0 | - |
| retr=null (V-born / no leg) | 0 | 1 | - |

## Q14/Q15 — Tier throttle and the strict ladder

Provisional-campaign exits: 7 (uncapped shadow grade/size on each row). Fills the strict (v11.0.0) ladder would have SKIPPED: 7, Σ realized_r -4.950 — the May-26 vs Jun-14 trade-off, measured.

## Q16 — Entries by stage at signal

| stage | fills | Σ realized_r (resolved) |
|---|---|---|
| 1 | 7 | -4.950 |
| 2 | 3 | -2.800 |

STAGE confirm events in window: 1.

## Q17 — Gated C-entries (journal-only, probation)

C events: 11; C-gate rejects: 39. No C ever fills (F5-asserted). Outcome simulation = Phase 2, re-fetching candles against journaled px_signal/stop.

## Q18 — Halts

2 halt(s): day 2026-06-19 at 2026-06-19T16:10:00Z (running R -2.800); day 2026-07-05 at 2026-07-05T09:20:00Z (running R -2.734).
Post-halt blocked fills (halted_day/week rejects): 0.

## Q19 — Cost anatomy

Σ fees 182.08 · Σ slippage 72.83 · Σ funding 1.48 · Σ pnl -380.96 USD (qty and px_fill journaled per fill).

## Q20 — Post-exit continuation by exit reason

| exit_reason | n | mean cont+1 | mean cont+5 | mean cont+20 |
|---|---|---|---|---|
| stop | 10 | -0.346 | -0.141 | 0.769 |

## Q21 — Capitulation V

V events in window: 0; V fills: 0. (Two true positives in nine months is the doctrine base rate — zero in a two-month plumbing window is unremarkable.)

## Q22 — TPW as exit input

TPW events: 34; resolved exits with a TPW before exit: 0; on those, mean X-B − X-A = -.

## Q23 — Time-in-trade by cohort

| cohort | n | median minutes |
|---|---|---|
| NEVER_GREEN | 3 | 0 |
| STILLBORN | 3 | 15 |
| FADED | 0 | - |
| PROTECTED | 4 | 222 |

## Q24 — Whipsaw-suppressed arrows

REGIME events: 4, arrows hidden on 0 (campaign outcomes joinable via subsequent EXIT rows).

## Q25 — Equity trajectory (per resolved exit)

| ts | tranche | pnl_usd | equity_after |
|---|---|---|---|
| 2026-05-17T11:40:00Z | c32t1 | -24.45 | 9975.55 |
| 2026-05-17T19:40:00Z | c32t2 | -22.16 | 9953.39 |
| 2026-05-17T19:40:00Z | c32t3 | -44.21 | 9909.19 |
| 2026-06-16T04:30:00Z | c33t4 | -19.62 | 9889.57 |
| 2026-06-19T14:25:00Z | c34t5 | -39.48 | 9850.09 |
| 2026-06-19T15:05:00Z | c34t6 | -50.53 | 9799.56 |
| 2026-06-19T16:10:00Z | c34t7 | -47.81 | 9751.76 |
| 2026-07-05T06:40:00Z | c35t8 | -28.34 | 9723.41 |
| 2026-07-05T07:15:00Z | c35t9 | -58.38 | 9665.03 |
| 2026-07-05T09:20:00Z | c35t10 | -46.00 | 9619.04 |

## Q26 — Initial stop distances

| tranche | |fill−stop|/ATRexec | /ATRgov | realized_r | mae_r | alt-anchor | vol-buf |
|---|---|---|---|---|---|---|
| c32t1 | 1.37 | 0.14 | -0.489 | -1.209 | 78446.5 | 78378.8 |
| c32t2 | 0.78 | 0.07 | -0.444 | -1.179 | 78495.2 | 78412.3 |
| c32t3 | 1.86 | 0.18 | -0.886 | -1.896 | 78286.3 | 78282.4 |
| c33t4 | 1.23 | 0.17 | -0.396 | -1.858 | 65732.9 | 65884.9 |
| c34t5 | 0.94 | 0.15 | -0.798 | -1.968 | 63209.6 | 63144.2 |
| c34t6 | 0.57 | 0.08 | -1.026 | -2.190 | 63296.6 | 63249.9 |
| c34t7 | 0.69 | 0.09 | -0.976 | -3.919 | 63308.3 | 63258.4 |
| c35t8 | 1.02 | 0.08 | -0.581 | -1.078 | 62658.6 | 62722.4 |
| c35t9 | 1.10 | 0.08 | -1.201 | -1.306 | 62693.5 | 62703.3 |
| c35t10 | 1.66 | 0.13 | -0.952 | -1.782 | 62699.4 | 62789.1 |

---

*All 26 questions answered from journal rows alone. Columns proven live are enforced mechanically by fixture F8.*
