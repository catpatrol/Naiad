# CENSUS-1 — Definitions restatement (contract §5 + Amendment §1, in my own words)

Pinned **before** the G-7 pre-registration and any analysis. Engine 1.0.11
byte-untouched; the census only reads price. Estate: the 7-asset exploration
set {BTC, ETH, JTO, NEAR, SOL, TAO, ZEC}USDT. Window: exploration-classic —
every study candle's open_time < 2024-07-01T00:00:00Z, per-asset start = the
earliest S-1 mandate start (BTC 2019-10-01 … TAO 2024-05-01). Seven timeframes
{5m, 15m, 30m, 1H, 4H, 12H, 1D} (5-minute floor; 1m excluded by ruling; 30m and
1d are OHLCV-resampled from 15m/1h with the S-1 aggregation). EMAs 9/89/200 on
each TF's own closed bars; ATR-14 (Wilder). Dual coordinates throughout: bps
(relative to the anchor price) **and** ATR (the anchor's ATR basis).

## The three cross events (§3.1, role of 9/200 neutralized per Amendment §1.2)
On every TF, three EMA-pair crosses, up and down, are journalled with the bar's
close-time price and that TF's ATR:
- **9/89 — "regime"**: the current arming signal (fast crosses the slow line).
- **89/200 — "stage"**: the current structure gate (slow crosses the trend line).
- **9/200 — "momentum-vs-trend"**: **new**. The contract's original text called
  this "the continuation-gap probe" — that was a hypothesis wearing a
  definition's clothes. Amendment §1.2 **strips the pre-assigned role**: two
  candidate readings are on record — operator's *mid-sequence reversal marker*
  (canonically 9/89 → 9/200 → 89/200) and the reviewer's *pullback-free
  continuation confirmer* — and **D6 assigns the role from the data**, against
  the canonical ordering as its null (below).

A cross is **anchored** on the first exec (5m) bar whose open ≥ the cross bar's
close — you can only act once the bar that produced the cross has closed. No
lookahead.

## The state vector (§3.2)
At each 5m bar, the full stack state: for each of the seven TFs, the sign of
{price−e9, price−e89, price−e200, e9−e89, e89−e200, e9−e200}, plus bars-since
each of the three crosses. Higher-TF values are taken **as-of** the last CLOSED
HTF bar (close-time ≤ exec open) — the frozen live-governor convention; the exec
ribbon uses the current 5m bar. This vector is the raw material for the
combination scan and the D9 factor score.

## Continuation moment (§3.4) — and why it is S-3's frozen winning state
A 5m bar qualifies when, in the prevailing direction (sign of exec e9−e89):
price is beyond the exec e9, the exec ribbon is separated ≥ 1.0 ATR
(|e9−e89|/ATR ≥ 1.0), and **no pullback-reclaim in the prior 20 bars** —
operationalized trade-independently as: every one of the prior 20 closes held
beyond the exec e9 in-direction (a closing-basis pullback would have re-touched
e9). This is the *trend running cleanly with no pullback*. S-3 found **exactly
this state frozen 97.59%** of the time at +1R winning moments: the pullback-
dependent PRIME/CONFIRM gate had nothing available because the market was
running, not retracing. The census catalogs that state across the whole stack so
a decoupled add can key on it (D4).

## Governor lens (§4)
The single census is re-analyzed under four candidate governor lenses {1H, 4H
(current), 12H, 1D} as **analysis filters** (one run, four lenses; no
re-simulation). For a lens G, "long regime" = G's e9 > e89; events and moments
are partitioned by G's regime and outcomes conditioned within it. Amendment §1.3
reframes the deliverable: the product is a **governor-per-mandate map**, not a
single winner — fast horizons speak to intraday adoption, slow to position
adoption.

## Regime-scale horizon (§3.3)
Alongside the fixed horizons {20, 100, 500 exec bars}, the horizon that matches
how the winning book earns: from the anchor **until the next 9/89 cross on the
candidate governor** (the regime flip), bounded at 2,000 exec bars. Measured per
lens, because the flip that ends the regime is the lens's own.

## Cross-TF replication (§5, the anti-fishing test)
A pattern is worth pursuing only if its forward-outcome **sign holds across ≥ 2
timeframe pairs**. A pattern seen on one TF pair only is recorded as
"single-instance, likely noise." This gate is mandatory for every annex item.

## The cascade chain and per-rung remaining move (D8, Amendment §2)
Anchored on an **initiating** 9/89 cross (any TF), the empirical chain of
follow-on 9/89 crosses across the stack: for each other TF, the **first**
same-direction follow-on, its **lag** (exec bars), and the **remaining forward
MFE/MAE** (bps + ATR of the rung's TF) measured *from the follow-on event*. The
question, in the operator's words: does the time-based cascade itself constitute
an entry-and-add schedule — 5m cross = entry, 30m cross = add, 1h cross = add —
with meaningful move remaining at each rung? Reported per lens, dual coordinates,
CIs, **full lag distributions — never cherry-picked chains**.

## The factor list and the dose-response question (D9, Amendment §2, FIXED)
Registered factors, each computable trade-independently from the state vector at
an arming moment (an exec-5m 9/89 cross), direction-signed where structural:
- **F1** 1D structurally aligned (e89>e200) · **F2** 12H structurally aligned ·
  **F3** lens-governor regime aligned (e9>e89) · **F4** price beyond the lens
  e89 · **F5** price beyond the lens+1 e200 · **F6** a faster-TF 9/89 cross
  in-direction within the last 20 lens bars · **F7** 9/200 state aligned on the
  lens (e9 vs e200) · **F8** exec ribbon separated ≥ 1.0 ATR in-direction ·
  **F9** pullback-terminus-at-EMA flag — the D10 zone-landing condition (price
  within 0.35 lens-ATR of the lens e89/e200) applied at the arming moment.
For each anchored moment, the count **k** of true factors and the forward MFE/MAE
**by k** — the **dose-response curve**, per lens. This is the evidence base for
the operator's flexible-entry framework ("enough of them present → trade"), and
it is statistically kinder than conjunction-hunting: one monotonicity test, not a
combinatorial haystack. The factor list is **fixed here and never tuned** — no
factor added, removed, or reweighted. The fib pocket proper is *not* a factor
(it needs an arming leg, a trading construct); D10 tests its mechanism instead.

## The pullback terminus, the matched null, and WHY the null is mandatory (D10)
A **pullback terminus** = a confirmed strict (5,5) pivot low on the lens's own
frame while that lens governor is in long regime (mirror: pivot high in short
regime). For each terminus: distance to the lens e89 and e200, and to the lens+1
e200, in lens-ATR; and the subsequent 100-lens-bar forward MFE from the
confirmation bar. **The matched null is mandatory:** the same distances measured
at random in-regime lens bars (matched by lens and regime, n ≥ 10× the terminus
count, seed pinned at 20260721). **Why:** with **21 EMA lines on the field**
(three EMAs × seven TFs), *every* price point is near *some* line — proximity
alone proves nothing. Only **excess** clustering against the matched null is a
finding; the reference band is 0.35 lens-ATR (the Z2 width). Every D10 clustering
claim is reported with its matched-null row printed beside it.

---
*Definitions fixed pre-registration. The census observes first everywhere; every
role it assigns (the 9/200's included), it assigns from data against a stated
null.*
