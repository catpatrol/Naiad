# BRIEF — ARGUS · SS v12-T: THE PINE INDICATOR TUNED TO THE TRADE
**APOLLO · 2026-08-16 · destined `exchange/reports/BRIEF_ARGUS_PINE_SSV12T_2026-08-16.md`**
**Companion of record: `SSV12_LOGIC_2026-08-16.md` (the handbook — Part A steps, Part B
evidence). The PINE lane's constraints ledger binds whoever implements (plain-text tooltips ·
500-label cap + capless history dots · lookahead_on parity on closed HTF bars · evidence class
on every label · PARITY NOT CERTIFIED banner until operator spot-checks).**

## §1 · THE COMMISSION
One indicator, one trade. Strip SS v12.1's generality to the six-gate lifecycle of the
handbook, so a discretionary human sees exactly — and only — what the system sees, in order,
with the next decision always obvious. Name: **SS v12-T**. Base: SS_v12_1.pine (attach it).

## §2 · WHAT RENDERS, MAPPED TO HANDBOOK STEPS
**S0 TIDE (Step 0):** background tint = permitted side (bull/bear/none) from 4h e89 vs e316 +
close; a one-cell status chip "TIDE: LONG ONLY / SHORT ONLY / STAND DOWN".
**S1 WINDOW (Step 1):** 12/89 cross ticks open/close the window; open windows shade the
chart span faintly; displacement printed at the arming (hollow mark < 0.75 ATR — label
"below floor [provisional]").
**S2 TRIGGER (Step 2):** 12/26-in-window = THE arrow (largest mark on the chart); LPS
second-chance tag on the first fast-ribbon pullback-hold. Tooltip carries the handbook's
sentence: "+0.19 ATR provisional; the seal eulogizes ~28h late — never wait."
**S3 STOP (Step 3):** entry-stop line drawn at fill (anchor = 800h 4h pivot, rail 1.0 ATR);
label shows R in ATR.
**S4 SLEEP → S5 TRAIL (Steps 4–5):** a "+1R" horizontal from entry; before it: chip
"TRAIL ASLEEP — do nothing". After first touch: the ratchet as a STEP-LINE (pivot ± 0.5 ATR,
rail-checked, min advance 0.05 ATR), each advance a small tick with tooltip (pivot ts,
binding side).
**S6 DE-RISK (Step 6):** the opposing 89/316 band lightly filled while in a trade; first
touch = "½ OFF" glyph; tooltip: "de-risk, expects a small loss — +5.7R lifetime, 32/37
helped."
**S7 WALLS (Step 7):** champion-wall lines via security: 889 (12h + 1d), 3618 (4h), 4618
(1h) — drawn on any chart TF, labeled with clock + rejection rate (62.7/61.9/52.3/48.4%);
proximity glow within 0.5 ATR. Legend: "walls stop price; the tide line does not (316 =
weakest 12h wall, 23.9%)."
**S8 EXITS (Step 8):** bell glyph retained as BACKSTOP (labeled so); funding-ceiling not
computable in TV — one ⓘ states it lives engine-side.

## §3 · ALERTS — the R1 set, verbatim message templates
window-open(dir) · window-close · TRIGGER(dir) [the entry alert] · LPS-second-chance ·
**+1R reached — TRAIL ARMS** · trail-advance · de-risk band touch · champion-wall approach
(0.5 ATR, per clock) · bell(backstop) · counter-arming. Template:
"SSv12-T [{class}] {step} {dir} {ticker} {tf} @ {close}".

## §4 · DEFAULTS & EVIDENCE DISCIPLINE
All thresholds quote SSV12_LOGIC Part B as provenance (tooltips cite the number's own
evidence, one line each). Grid-set lens defaults inherited (5m/30m marks OFF — toll).
No new semantics, no new thresholds: anything not in the handbook needs an APOLLO word
first. Deliver as pine file + one-page quickstart; version SS_v12_T_0; ledger append on
filing.

— APOLLO · one trade, six gates, zero ambiguity on what happens next.
