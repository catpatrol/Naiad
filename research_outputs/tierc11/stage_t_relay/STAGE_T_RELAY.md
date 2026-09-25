as_of_last_closed_4h: 2026-09-25T00:00:00Z

# TIER-C11 · STAGE T-relay — P-RELAY-1 (the 1h relay inside the armed 4h window)

substrate tc11_20260925 · corridor 2019-09-08T16:00:00Z → 2026-09-25T00:00:00Z · CLASSIC5 · seed 20260924 · registration P-RELAY-1 seq 5 text sha b089017bcc8b5503… payload sha e8f6d4595b449a18…

**This stage builds books, not verdicts.** No CI, no p and no verdict word appear here; the scorer reads `research_outputs/tierc11/regbooks/P-RELAY-1/`. Every non-registered table carries the L-1.4 collar (tier = 'TIER-E', selection_not_a_result = 'a SELECTION, not a result', gates = 'nothing').

## Readings built

- [LEAN-HEPHAESTUS] L-T.2 windows = every v6 arming on CLASSIC5 (replay9's armings, TIDE and d >= 0.75 at the arm bar) whether or not v6 entered it; ARMED from the arm close to min(v6 4h 12/26 trigger close, counter 12/89 close, 89/316-against close); the relay enters at the FIRST 1h close strictly inside that interval on which EMA9 crosses EMA12 with the trend; one relay per window, one position per asset; stop struct_stop_4h as of the last CLOSED 4h bar railed 1.0 ATR (R on 4h); RD.relay_entry / relay_stop / relay11(walk_after=True).
- [LEAN-HEPHAESTUS] L-T.3 every relay's close < its window's v6 4h trigger close (when the window triggered); misses are windows whose trigger closed first (every lag-0 window) or that closed unrelayed — each with what v6 did in it.
- [LEAN-HEPHAESTUS] L-W.0 / AM-5 a relay entry inside a 4h bar whose four 1h children do not reproduce the parent is taken at the parent's close (moved) and the bar is counted; the book prints its mismatch-bar count and names the bars.
- [LEAN-HEPHAESTUS] AM-6 (s3) a relay stopped inside its entry bar J books mae/mfe at 1h resolution (the stop child is the stop unit); L-T.2 arms the harvest on close[J-1].
- [LEAN-HEPHAESTUS] AM-7 haircut_net_r = net_r - fee_r x slip_bps_side / taker_bps_side (charter tier per stem from E.fees()); printed beside net_r, never replacing it.
- [LEAN-HEPHAESTUS] SR-1 window set = replay9's armings (tide_ok and d_ok) over replay9's own bounds; v6's disposition of each is replay9's.
- [LEAN-HEPHAESTUS] SR-2 bounds known by the as-of only; a window with no bound by the pin is armed at the pin (1h closes <= the pin eligible); tie order trigger -> counter 12/89 -> 89/316-against.
- [LEAN-HEPHAESTUS] SR-3 first cross only: a window whose first qualifying cross cannot be entered is a MISS with the reason (v6's one-trigger-per-window law); refusal order position open, then the stop (replay9's order).
- [LEAN-HEPHAESTUS] SR-4 a moved entry is refused unless its RESOLVED instant is strictly before every bound (relay_entry refuses the trigger; the runner the other two).
- [LEAN-HEPHAESTUS] SR-5 one position per asset at 1h resolution: entry instant strictly after the previous relay's 1h-resolved exit; v6's 4h-bar law printed as a disclosure.
- [LEAN-HEPHAESTUS] SR-6 late-relay twin (Tier-E rival) = the record rule with the trigger bound removed (the trigger instant and later admissible).
- [LEAN-HEPHAESTUS] SR-7 relay entry_ms = open of the 4h bar J holding the entry close; relay exit_close_ms = the 1h-resolved exit instant; base v6 exit_close_ms = the exit bar's close (tierc11_books convention); both carry exit_bar_close_ms.

## Anchor

- base v6 = tierc11_books.v6_book over the full TC11 corridor: TP._book_sha f3c68f544bcda52c909374105dabbdc773c9bffa4b66b2ef7e0f35ac9b369132 n 200 == the books manifest of record (F-CTRL held there); replay9's per-asset trades reproduce it campaign for campaign.

## Regbooks written (book, not a verdict)

| arm | kind | ruler | era_scope | n | ΣR (net) | mean R | Σ haircut R | book_sha256 | label |
|---|---|---|---|---:|---:|---:|---:|---|---|
| scored | scored | two_sample | full | 173 | +78.4797 | +0.4536 | +74.4328 | 57d8bbef8190492d… | book, not a verdict |
| base | base | two_sample | full | 200 | +40.8076 | +0.2040 | +36.6975 | f41bfaf02b86dfb0… | book, not a verdict |
| tierE__late_relay | tierE | two_sample | full | 283 | +131.6439 | +0.4652 | +125.5708 | 9e295b903e0c6e37… | book, not a verdict · Tier-E, a SELECTION, not a result |
| tierE__tuning_slice | tierE | two_sample | tuning | 114 | +36.0856 | +0.3165 | +33.5315 | 10ac7ec867fab087… | book, not a verdict · Tier-E, a SELECTION, not a result |
| tierE__holdout_slice | tierE | two_sample | holdout | 59 | +42.3942 | +0.7185 | +40.9012 | 7e975ad781e3e31f… | book, not a verdict · Tier-E, a SELECTION, not a result |
| tierE__miss_v6 | tierE | vs_zero | full | 131 | +53.9413 | +0.4118 | +51.2278 | 306b9ceebecb9e51… | book, not a verdict · Tier-E, a SELECTION, not a result |

## The window dispositions — a partition of every armed window (Tier-E, whole)

| variant | disposition | n windows | of which lag 0 | relay n | relay ΣR | v6 entered n | v6 ΣR in them | v6 mean R | tier | selection_not_a_result | gates |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| record | RELAYED | 173 | 0 | 173 | +78.4797 | 69 | -13.1337 | -0.1903 | TIER-E | a SELECTION, not a result | nothing |
| record | MISS_TRIGGER_FIRST_LAG0 | 52 | 52 | 0 | +0.0000 | 52 | +22.3888 | +0.4306 | TIER-E | a SELECTION, not a result | nothing |
| record | MISS_TRIGGER_FIRST | 79 | 0 | 0 | +0.0000 | 79 | +31.5525 | +0.3994 | TIER-E | a SELECTION, not a result | nothing |
| record | MISS_CLOSED_COUNTER_12_89 | 46 | 0 | 0 | +0.0000 | 0 | +0.0000 | — | TIER-E | a SELECTION, not a result | nothing |
| record | MISS_CLOSED_TIDE_AGAINST | 0 | 0 | 0 | +0.0000 | 0 | +0.0000 | — | TIER-E | a SELECTION, not a result | nothing |
| record | MISS_OPEN_AT_ASOF | 0 | 0 | 0 | +0.0000 | 0 | +0.0000 | — | TIER-E | a SELECTION, not a result | nothing |
| record | MISS_REFUSED_MOVED_ONTO_BOUND | 0 | 0 | 0 | +0.0000 | 0 | +0.0000 | — | TIER-E | a SELECTION, not a result | nothing |
| record | MISS_REFUSED_POSITION_OPEN | 0 | 0 | 0 | +0.0000 | 0 | +0.0000 | — | TIER-E | a SELECTION, not a result | nothing |
| record | MISS_REFUSED_NO_STOP | 0 | 0 | 0 | +0.0000 | 0 | +0.0000 | — | TIER-E | a SELECTION, not a result | nothing |
| record | ALL | 350 | 52 | 173 | +78.4797 | 200 | +40.8076 | +0.2040 | TIER-E | a SELECTION, not a result | nothing |
| late | RELAYED | 283 | 42 | 283 | +131.6439 | 179 | +60.2723 | +0.3367 | TIER-E | a SELECTION, not a result | nothing |
| late | MISS_TRIGGER_FIRST_LAG0 | 0 | 0 | 0 | +0.0000 | 0 | +0.0000 | — | TIER-E | a SELECTION, not a result | nothing |
| late | MISS_TRIGGER_FIRST | 0 | 0 | 0 | +0.0000 | 0 | +0.0000 | — | TIER-E | a SELECTION, not a result | nothing |
| late | MISS_CLOSED_COUNTER_12_89 | 67 | 10 | 0 | +0.0000 | 21 | -19.4647 | -0.9269 | TIER-E | a SELECTION, not a result | nothing |
| late | MISS_CLOSED_TIDE_AGAINST | 0 | 0 | 0 | +0.0000 | 0 | +0.0000 | — | TIER-E | a SELECTION, not a result | nothing |
| late | MISS_OPEN_AT_ASOF | 0 | 0 | 0 | +0.0000 | 0 | +0.0000 | — | TIER-E | a SELECTION, not a result | nothing |
| late | MISS_REFUSED_MOVED_ONTO_BOUND | 0 | 0 | 0 | +0.0000 | 0 | +0.0000 | — | TIER-E | a SELECTION, not a result | nothing |
| late | MISS_REFUSED_POSITION_OPEN | 0 | 0 | 0 | +0.0000 | 0 | +0.0000 | — | TIER-E | a SELECTION, not a result | nothing |
| late | MISS_REFUSED_NO_STOP | 0 | 0 | 0 | +0.0000 | 0 | +0.0000 | — | TIER-E | a SELECTION, not a result | nothing |
| late | ALL | 350 | 52 | 283 | +131.6439 | 200 | +40.8076 | +0.2040 | TIER-E | a SELECTION, not a result | nothing |

Disposition codes: `RELAYED` relayed: the first with-trend 1h 9/12 close inside the armed interval, entered · `MISS_TRIGGER_FIRST_LAG0` miss: the v6 4h 12/26 trigger closed first, at the arm bar (lag 0 — no 1h close lies strictly between) · `MISS_TRIGGER_FIRST` miss: the v6 4h 12/26 trigger closed first (lag >= 1) · `MISS_CLOSED_COUNTER_12_89` miss: the window closed unrelayed (counter 4h 12/89) · `MISS_CLOSED_TIDE_AGAINST` miss: the window closed unrelayed (4h 89/316 against) · `MISS_OPEN_AT_ASOF` miss: still armed at the as-of, unrelayed (censored) · `MISS_REFUSED_MOVED_ONTO_BOUND` miss: the first cross sits in an L-W.0 mismatch bar and its parent-close entry is not strictly before the bound · `MISS_REFUSED_POSITION_OPEN` miss: the first cross came while a relay was open on the asset (one position per asset) · `MISS_REFUSED_NO_STOP` miss: no structural stop (struct_stop_4h None / ATR not finite).

## The lead of the relay over the v6 4h trigger (relayed windows, Tier-E, whole)

| lead kind | bin | n | tier | selection_not_a_result | gates |
|---|---|---:|---|---|---|
| lead_4h_bars | 0 | 0 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 1 | 3 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 2 | 0 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 3 | 3 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 4 | 0 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 5-9 | 3 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 10-19 | 5 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | >=20 | 55 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | no trigger (NA) | 104 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 1-3 | 0 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 4-7 | 3 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 8-15 | 3 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 16-31 | 2 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 32-63 | 2 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | >=64 | 59 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | no trigger (NA) | 104 | TIER-E | a SELECTION, not a result | nothing |

Every distinct value (whole):

| lead kind | lead value (bars) | n | tier | selection_not_a_result | gates |
|---|---:|---:|---|---|---|
| lead_4h_bars | 1 | 3 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 3 | 3 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 5 | 2 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 9 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 10 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 16 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 17 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 18 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 19 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 20 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 21 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 23 | 2 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 24 | 5 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 26 | 2 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 28 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 30 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 31 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 32 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 34 | 2 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 35 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 36 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 39 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 41 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 42 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 43 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 45 | 2 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 52 | 5 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 55 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 56 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 58 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 64 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 66 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 67 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 68 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 71 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 72 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 73 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 80 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 83 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 85 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 93 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 95 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 103 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 104 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 105 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 108 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 109 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 132 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 135 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 173 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 178 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_4h_bars | 188 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 4 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 5 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 6 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 12 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 13 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 14 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 20 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 21 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 38 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 41 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 67 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 71 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 75 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 77 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 81 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 85 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 94 | 2 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 97 | 2 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 98 | 2 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 99 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 105 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 107 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 113 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 120 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 127 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 129 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 137 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 139 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 142 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 147 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 158 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 166 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 168 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 173 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 182 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 183 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 208 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 209 | 2 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 211 | 2 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 220 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 227 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 232 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 258 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 266 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 269 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 275 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 284 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 289 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 294 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 320 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 332 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 343 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 374 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 382 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 413 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 419 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 421 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 433 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 437 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 528 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 542 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 693 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 714 | 1 | TIER-E | a SELECTION, not a result | nothing |
| lead_1h_bars | 753 | 1 | TIER-E | a SELECTION, not a result | nothing |

## Era slices (by the entry CLOSE, L-1.3; Tier-E, whole)

| arm | era | n | ΣR | mean R | Σ haircut R | win % | tier | selection_not_a_result | gates |
|---|---|---:|---:|---:|---:|---:|---|---|---|
| scored (relay) | tuning | 114 | +36.0856 | +0.3165 | +33.5315 | 34.21 | TIER-E | a SELECTION, not a result | nothing |
| scored (relay) | holdout | 59 | +42.3942 | +0.7185 | +40.9012 | 33.90 | TIER-E | a SELECTION, not a result | nothing |
| scored (relay) | full | 173 | +78.4797 | +0.4536 | +74.4328 | 34.10 | TIER-E | a SELECTION, not a result | nothing |
| base (v6) | tuning | 123 | -1.3238 | -0.0108 | -3.7532 | 33.33 | TIER-E | a SELECTION, not a result | nothing |
| base (v6) | holdout | 77 | +42.1314 | +0.5472 | +40.4507 | 36.36 | TIER-E | a SELECTION, not a result | nothing |
| base (v6) | full | 200 | +40.8076 | +0.2040 | +36.6975 | 34.50 | TIER-E | a SELECTION, not a result | nothing |
| tierE__late_relay | tuning | 181 | +39.7714 | +0.2197 | +36.0232 | 35.91 | TIER-E | a SELECTION, not a result | nothing |
| tierE__late_relay | holdout | 102 | +91.8725 | +0.9007 | +89.5476 | 37.25 | TIER-E | a SELECTION, not a result | nothing |
| tierE__late_relay | full | 283 | +131.6439 | +0.4652 | +125.5708 | 36.40 | TIER-E | a SELECTION, not a result | nothing |

## Mechanics disclosed (the relay book)

- entry kinds: {'1h': 141, '4h-close': 32} · moved to the parent's close (L-W.0): 0
- mismatch-bar count (AM-5, bars ridden by the parent, summed over the book): 0; bars named: none
- exit reasons: {'bell_12_89': 11, 'stop': 162} · exit resolved by: {'1h': 162, 'close': 11}
- stopped inside the entry bar J: 4 · belled at J's close: 0
- SR-5 disclosure: relays the v6 4h-bar position law (entry bar <= previous exit bar) would refuse: 0
- relays at/after the trigger: record 0 (must be 0, L-T.3) · late twin 110

## The relay book (scored arm), whole — book, not a verdict

| asset | dir | arm close | 1h cross close | entry (instant) | kind | trigger close | lead 1h | stop | R | exit (instant) | exit_reason | net R | haircut R | era | v6 in window |
|---|---:|---|---|---|---|---|---:|---:|---:|---|---|---:|---:|---|---|
| BTCUSDT | -1 | 2020-01-01T00:00:00Z | 2020-01-01T10:00:00Z | 2020-01-01T10:00:00Z | 1h | — | — | 7258.95 | 74.5047 | 2020-01-01T16:00:00Z | stop | -1.096929 | -1.135701 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | -1 | 2020-03-28T12:00:00Z | 2020-04-01T00:00:00Z | 2020-04-01T00:00:00Z | 4h-close | 2020-04-01T20:00:00Z | 20 | 6571.98 | 164.877 | 2020-04-01T23:00:00Z | stop | -1.074831 | -1.090575 | tuning | entered -1.0189 |
| BTCUSDT | -1 | 2020-04-21T16:00:00Z | 2020-04-22T01:00:00Z | 2020-04-22T01:00:00Z | 1h | — | — | 6953.45 | 125.483 | 2020-04-22T08:00:00Z | stop | -1.054913 | -1.076879 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | +1 | 2020-05-28T16:00:00Z | 2020-05-30T05:00:00Z | 2020-05-30T05:00:00Z | 1h | 2020-06-08T00:00:00Z | 211 | 9366.61 | 145.327 | 2020-06-02T15:00:00Z | stop | -0.999684 | -1.025701 | tuning | entered -0.6723 |
| BTCUSDT | +1 | 2020-06-23T00:00:00Z | 2020-06-24T03:00:00Z | 2020-06-24T03:00:00Z | 1h | — | — | 9502.62 | 164.434 | 2020-06-24T09:00:00Z | stop | -1.064079 | -1.087395 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | +1 | 2020-07-07T04:00:00Z | 2020-07-07T19:00:00Z | 2020-07-07T19:00:00Z | 1h | 2020-07-11T00:00:00Z | 77 | 9188.06 | 83.937 | 2020-07-09T16:00:00Z | stop | -0.718405 | -0.762474 | tuning | entered -1.1357 |
| BTCUSDT | +1 | 2020-07-21T12:00:00Z | 2020-07-22T18:00:00Z | 2020-07-22T18:00:00Z | 1h | 2020-08-14T08:00:00Z | 542 | 9242.74 | 119.812 | 2020-08-02T05:00:00Z | stop | +13.328149 | +13.294009 | tuning | entered -0.2358 |
| BTCUSDT | +1 | 2020-08-31T00:00:00Z | 2020-08-31T13:00:00Z | 2020-08-31T13:00:00Z | 1h | — | — | 11616.6 | 113.359 | 2020-09-01T01:00:00Z | stop | -1.129284 | -1.170475 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | -1 | 2020-09-21T20:00:00Z | 2020-09-23T06:00:00Z | 2020-09-23T06:00:00Z | 1h | — | — | 10597.5 | 130.381 | 2020-09-24T17:00:00Z | stop | -1.077780 | -1.110092 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | -1 | 2020-10-02T08:00:00Z | 2020-10-03T09:00:00Z | 2020-10-03T09:00:00Z | 1h | — | — | 10632.9 | 129.177 | 2020-10-04T07:00:00Z | stop | -1.075610 | -1.108335 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | +1 | 2020-12-13T08:00:00Z | 2020-12-14T03:00:00Z | 2020-12-14T03:00:00Z | 1h | 2021-01-14T12:00:00Z | 753 | 18698.6 | 605.02 | 2020-12-21T11:00:00Z | stop | +5.515890 | +5.501967 | tuning | entered -0.5390 |
| BTCUSDT | +1 | 2021-01-29T16:00:00Z | 2021-01-30T19:00:00Z | 2021-01-30T19:00:00Z | 1h | — | — | 32698.5 | 1682.84 | 2021-01-31T16:00:00Z | stop | -0.758387 | -0.766415 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | +1 | 2021-03-28T16:00:00Z | 2021-03-29T09:00:00Z | 2021-03-29T09:00:00Z | 1h | 2021-04-06T00:00:00Z | 183 | 55704.8 | 1465.05 | 2021-04-03T19:00:00Z | stop | +0.053103 | +0.037381 | tuning | entered -1.0870 |
| BTCUSDT | +1 | 2021-04-30T20:00:00Z | 2021-05-02T03:00:00Z | 2021-05-02T03:00:00Z | 1h | — | — | 56227.3 | 1469.8 | 2021-05-02T05:00:00Z | stop | -1.038755 | -1.054257 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | -1 | 2021-06-18T20:00:00Z | 2021-06-19T19:00:00Z | 2021-06-19T19:00:00Z | 1h | 2021-06-25T12:00:00Z | 137 | 37332.5 | 1837.22 | 2021-06-23T02:00:00Z | stop | +0.860737 | +0.853186 | tuning | entered -0.0628 |
| BTCUSDT | +1 | 2021-09-16T00:00:00Z | 2021-09-17T04:00:00Z | 2021-09-17T04:00:00Z | 4h-close | — | — | 47049.1 | 850.101 | 2021-09-17T19:00:00Z | stop | -0.780948 | -0.803342 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | +1 | 2021-10-28T20:00:00Z | 2021-10-29T14:00:00Z | 2021-10-29T14:00:00Z | 1h | 2021-10-29T20:00:00Z | 6 | 59487.6 | 1836.9 | 2021-11-01T05:00:00Z | stop | -0.818911 | -0.832121 | tuning | entered -1.0655 |
| BTCUSDT | -1 | 2021-12-29T00:00:00Z | 2021-12-31T01:00:00Z | 2021-12-31T01:00:00Z | 1h | 2022-01-17T12:00:00Z | 419 | 48914.8 | 1874.79 | 2022-01-11T17:00:00Z | stop | +2.309315 | +2.299729 | tuning | entered -0.3716 |
| BTCUSDT | -1 | 2022-02-18T08:00:00Z | 2022-02-19T09:00:00Z | 2022-02-19T09:00:00Z | 1h | 2022-02-28T04:00:00Z | 211 | 42310.8 | 2349.41 | 2022-02-23T12:00:00Z | stop | +0.362885 | +0.356158 | tuning | entered -1.0275 |
| BTCUSDT | -1 | 2022-03-05T08:00:00Z | 2022-03-06T09:00:00Z | 2022-03-06T09:00:00Z | 1h | — | — | 39985.8 | 848.464 | 2022-03-09T04:00:00Z | stop | -1.037361 | -1.056012 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | -1 | 2022-06-03T16:00:00Z | 2022-06-04T13:00:00Z | 2022-06-04T13:00:00Z | 1h | — | — | 30482.7 | 962.227 | 2022-06-06T02:00:00Z | stop | -0.792739 | -0.805165 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | -1 | 2022-07-12T00:00:00Z | 2022-07-13T13:00:00Z | 2022-07-13T13:00:00Z | 1h | — | — | 20633.8 | 1480.36 | 2022-07-14T18:00:00Z | stop | -1.011766 | -1.017141 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | -1 | 2022-09-14T20:00:00Z | 2022-09-18T10:00:00Z | 2022-09-18T10:00:00Z | 1h | — | — | 20204.3 | 379.835 | 2022-09-21T18:00:00Z | stop | -0.230554 | -0.251469 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | -1 | 2022-10-09T00:00:00Z | 2022-10-09T23:00:00Z | 2022-10-09T23:00:00Z | 1h | 2022-10-15T08:00:00Z | 129 | 19599.8 | 209.54 | 2022-10-13T19:00:00Z | stop | +0.317351 | +0.280399 | tuning | entered -0.7515 |
| BTCUSDT | -1 | 2022-12-17T04:00:00Z | 2022-12-18T11:00:00Z | 2022-12-18T11:00:00Z | 1h | 2022-12-25T16:00:00Z | 173 | 16874.1 | 175.649 | 2022-12-20T03:00:00Z | stop | -1.077185 | -1.115412 | tuning | entered -1.1690 |
| BTCUSDT | +1 | 2023-02-16T00:00:00Z | 2023-02-17T17:00:00Z | 2023-02-17T17:00:00Z | 1h | — | — | 22964.8 | 1125.92 | 2023-02-22T16:00:00Z | stop | -0.454072 | -0.462550 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | -1 | 2023-06-01T12:00:00Z | 2023-06-01T21:00:00Z | 2023-06-01T21:00:00Z | 1h | — | — | 27183.4 | 332.96 | 2023-06-02T06:00:00Z | stop | -1.077301 | -1.109758 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | +1 | 2023-08-08T20:00:00Z | 2023-08-10T14:00:00Z | 2023-08-10T14:00:00Z | 1h | 2023-08-14T16:00:00Z | 98 | 29437.3 | 232.504 | 2023-08-10T15:00:00Z | stop | -1.127110 | -1.177954 | tuning | entered -1.1627 |
| BTCUSDT | -1 | 2023-09-25T00:00:00Z | 2023-09-26T11:00:00Z | 2023-09-26T11:00:00Z | 1h | — | — | 26432.2 | 194.221 | 2023-09-27T11:00:00Z | stop | -1.110048 | -1.164285 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | +1 | 2023-10-16T12:00:00Z | 2023-10-18T03:00:00Z | 2023-10-18T03:00:00Z | 1h | 2023-11-16T00:00:00Z | 693 | 27045.9 | 1409.77 | 2023-10-27T18:00:00Z | stop | +3.455577 | +3.446801 | tuning | entered -1.0290 |
| BTCUSDT | +1 | 2024-01-02T00:00:00Z | 2024-01-03T02:00:00Z | 2024-01-03T02:00:00Z | 1h | 2024-01-04T16:00:00Z | 38 | 43234.5 | 2113.3 | 2024-01-03T13:00:00Z | stop | -1.024607 | -1.032990 | tuning | entered -1.0557 |
| BTCUSDT | +1 | 2024-03-25T16:00:00Z | 2024-03-27T02:00:00Z | 2024-03-27T02:00:00Z | 1h | — | — | 67911.5 | 2476.39 | 2024-04-02T03:00:00Z | stop | -1.109673 | -1.120857 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | +1 | 2024-04-07T00:00:00Z | 2024-04-08T02:00:00Z | 2024-04-08T02:00:00Z | 1h | — | — | 68462 | 996.105 | 2024-04-09T18:00:00Z | stop | -0.706086 | -0.733864 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | +1 | 2024-04-23T00:00:00Z | 2024-04-23T15:00:00Z | 2024-04-23T15:00:00Z | 1h | — | — | 65450.4 | 1430.11 | 2024-04-24T15:00:00Z | stop | -1.048888 | -1.067394 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | -1 | 2024-08-28T12:00:00Z | 2024-08-29T21:00:00Z | 2024-08-29T21:00:00Z | 1h | — | — | 60648.5 | 1151.57 | 2024-09-02T21:00:00Z | stop | +0.183484 | +0.162864 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | +1 | 2024-10-12T16:00:00Z | 2024-10-13T22:00:00Z | 2024-10-13T22:00:00Z | 1h | 2024-10-25T00:00:00Z | 266 | 62178.5 | 682.53 | 2024-10-21T14:00:00Z | stop | +6.526482 | +6.488274 | holdout | entered -1.0955 |
| BTCUSDT | +1 | 2025-01-03T16:00:00Z | 2025-01-04T15:00:00Z | 2025-01-04T15:00:00Z | 1h | — | — | 94120.3 | 3871.67 | 2025-01-08T18:00:00Z | stop | -0.559824 | -0.569846 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | +1 | 2025-01-15T08:00:00Z | 2025-01-16T18:00:00Z | 2025-01-16T18:00:00Z | 1h | 2025-01-23T16:00:00Z | 166 | 96469.9 | 3305.43 | 2025-01-19T23:00:00Z | stop | +0.824553 | +0.812304 | holdout | entered -0.8405 |
| BTCUSDT | -1 | 2025-03-29T00:00:00Z | 2025-03-30T15:00:00Z | 2025-03-30T15:00:00Z | 1h | — | — | 84950.2 | 2180.37 | 2025-04-01T16:00:00Z | stop | -1.030152 | -1.045536 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | +1 | 2025-06-08T20:00:00Z | 2025-06-09T10:00:00Z | 2025-06-09T10:00:00Z | 1h | — | — | 105755 | 807.334 | 2025-06-12T04:00:00Z | stop | +1.246845 | +1.193758 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | +1 | 2025-06-25T08:00:00Z | 2025-06-26T21:00:00Z | 2025-06-26T21:00:00Z | 1h | 2025-07-02T16:00:00Z | 139 | 106559 | 1168.78 | 2025-06-27T02:00:00Z | stop | -1.092690 | -1.129358 | holdout | entered +1.0934 |
| BTCUSDT | +1 | 2025-08-08T00:00:00Z | 2025-08-08T12:00:00Z | 2025-08-08T12:00:00Z | 4h-close | — | — | 115843 | 997.12 | 2025-08-14T13:00:00Z | stop | +1.069338 | +1.022190 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | -1 | 2026-03-08T00:00:00Z | 2026-03-08T16:00:00Z | 2026-03-08T16:00:00Z | 4h-close | — | — | 68723.4 | 1548.7 | 2026-03-09T14:00:00Z | stop | -0.726526 | -0.744011 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | -1 | 2026-03-20T16:00:00Z | 2026-03-21T17:00:00Z | 2026-03-21T17:00:00Z | 1h | 2026-03-24T20:00:00Z | 75 | 71406.5 | 1131.62 | 2026-03-23T12:00:00Z | stop | -1.071936 | -1.096977 | holdout | entered -1.0562 |
| BTCUSDT | -1 | 2026-07-28T04:00:00Z | 2026-07-29T17:00:00Z | 2026-07-29T17:00:00Z | 1h | — | — | 64429.2 | 642.583 | 2026-07-29T19:00:00Z | stop | -1.099766 | -1.139672 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | -1 | 2026-08-11T16:00:00Z | 2026-08-12T15:00:00Z | 2026-08-12T15:00:00Z | 1h | — | — | 64571.6 | 1227.16 | 2026-08-17T19:00:00Z | stop | -0.611994 | -0.632762 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| BTCUSDT | +1 | 2026-09-18T16:00:00Z | 2026-09-20T17:00:00Z | 2026-09-20T17:00:00Z | 1h | — | — | 78219.1 | 3078.71 | 2026-09-23T15:00:00Z | stop | +1.014883 | +1.004110 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| ETHUSDT | +1 | 2020-06-22T16:00:00Z | 2020-06-25T17:00:00Z | 2020-06-25T17:00:00Z | 1h | — | — | 227.456 | 6.59379 | 2020-06-26T04:00:00Z | bell_12_89 | -0.308838 | -0.322982 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ETHUSDT | +1 | 2020-07-06T16:00:00Z | 2020-07-07T17:00:00Z | 2020-07-07T17:00:00Z | 1h | 2020-07-13T00:00:00Z | 127 | 234.936 | 3.46384 | 2020-07-09T16:00:00Z | stop | +0.688228 | +0.660539 | tuning | entered -0.9374 |
| ETHUSDT | +1 | 2020-07-20T08:00:00Z | 2020-07-21T07:00:00Z | 2020-07-21T07:00:00Z | 1h | 2020-08-08T12:00:00Z | 437 | 235.639 | 2.43093 | 2020-08-02T05:00:00Z | stop | +28.546091 | +28.500985 | tuning | entered -0.1891 |
| ETHUSDT | +1 | 2020-09-17T20:00:00Z | 2020-09-19T12:00:00Z | 2020-09-19T12:00:00Z | 4h-close | — | — | 378.128 | 8.48224 | 2020-09-20T10:00:00Z | stop | -1.058640 | -1.076671 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ETHUSDT | +1 | 2021-03-07T08:00:00Z | 2021-03-07T22:00:00Z | 2021-03-07T22:00:00Z | 1h | 2021-03-18T16:00:00Z | 258 | 1611.53 | 53.5825 | 2021-03-10T03:00:00Z | stop | +1.881329 | +1.868491 | tuning | entered -1.0452 |
| ETHUSDT | +1 | 2021-03-29T16:00:00Z | 2021-03-31T07:00:00Z | 2021-03-31T07:00:00Z | 1h | 2021-04-09T00:00:00Z | 209 | 1741.38 | 115.214 | 2021-04-07T11:00:00Z | stop | +1.041618 | +1.034892 | tuning | entered +1.0215 |
| ETHUSDT | -1 | 2021-07-09T12:00:00Z | 2021-07-10T05:00:00Z | 2021-07-10T05:00:00Z | 1h | — | — | 2278.83 | 171.539 | 2021-07-18T01:00:00Z | stop | +0.312327 | +0.307475 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ETHUSDT | +1 | 2021-09-16T04:00:00Z | 2021-09-18T06:00:00Z | 2021-09-18T06:00:00Z | 1h | — | — | 3097.1 | 414.795 | 2021-09-19T08:00:00Z | bell_12_89 | -0.175093 | -0.178447 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ETHUSDT | +1 | 2021-11-30T00:00:00Z | 2021-12-03T06:00:00Z | 2021-12-03T06:00:00Z | 1h | — | — | 4449.86 | 120.225 | 2021-12-03T17:00:00Z | stop | -1.045031 | -1.060036 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ETHUSDT | -1 | 2022-02-18T12:00:00Z | 2022-02-21T12:00:00Z | 2022-02-21T12:00:00Z | 4h-close | 2022-02-28T12:00:00Z | 168 | 2704.99 | 80.2556 | 2022-02-21T15:00:00Z | stop | -1.033205 | -1.046486 | tuning | entered -1.0267 |
| ETHUSDT | -1 | 2022-03-04T16:00:00Z | 2022-03-06T05:00:00Z | 2022-03-06T05:00:00Z | 1h | 2022-03-10T16:00:00Z | 107 | 2785.19 | 139.364 | 2022-03-09T04:00:00Z | stop | -0.316725 | -0.324380 | tuning | entered -0.7577 |
| ETHUSDT | -1 | 2022-07-11T20:00:00Z | 2022-07-13T13:00:00Z | 2022-07-13T13:00:00Z | 1h | — | — | 1101.55 | 73.1093 | 2022-07-14T00:00:00Z | stop | -1.016406 | -1.022233 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ETHUSDT | -1 | 2022-12-16T16:00:00Z | 2022-12-18T11:00:00Z | 2022-12-18T11:00:00Z | 1h | 2022-12-22T20:00:00Z | 105 | 1226.69 | 47.1918 | 2022-12-20T16:00:00Z | stop | -1.022182 | -1.032380 | tuning | entered -1.0727 |
| ETHUSDT | +1 | 2023-02-16T00:00:00Z | 2023-02-17T17:00:00Z | 2023-02-17T17:00:00Z | 1h | — | — | 1604.19 | 68.7611 | 2023-02-22T16:00:00Z | stop | -0.655997 | -0.665609 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ETHUSDT | +1 | 2023-03-01T12:00:00Z | 2023-03-02T23:00:00Z | 2023-03-02T23:00:00Z | 1h | — | — | 1618.72 | 29.0885 | 2023-03-03T02:00:00Z | stop | -1.058395 | -1.080854 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ETHUSDT | +1 | 2023-05-05T16:00:00Z | 2023-05-07T11:00:00Z | 2023-05-07T11:00:00Z | 1h | — | — | 1865.11 | 39.4213 | 2023-05-08T01:00:00Z | stop | -0.591301 | -0.610518 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ETHUSDT | -1 | 2023-10-05T16:00:00Z | 2023-10-07T08:00:00Z | 2023-10-07T08:00:00Z | 4h-close | 2023-10-19T04:00:00Z | 284 | 1654.99 | 18.99 | 2023-10-13T21:00:00Z | stop | +1.841857 | +1.807772 | tuning | entered -1.0381 |
| ETHUSDT | +1 | 2024-01-09T08:00:00Z | 2024-01-09T23:00:00Z | 2024-01-09T23:00:00Z | 1h | — | — | 2237.06 | 104.134 | 2024-01-12T22:00:00Z | stop | +1.709838 | +1.700494 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ETHUSDT | +1 | 2024-02-06T20:00:00Z | 2024-02-07T13:00:00Z | 2024-02-07T13:00:00Z | 1h | — | — | 2247.95 | 124.027 | 2024-02-28T18:00:00Z | stop | +6.252587 | +6.243637 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ETHUSDT | +1 | 2024-03-26T08:00:00Z | 2024-03-27T03:00:00Z | 2024-03-27T03:00:00Z | 1h | — | — | 3526.93 | 94.9497 | 2024-03-27T15:00:00Z | stop | -0.719608 | -0.734732 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ETHUSDT | +1 | 2024-04-08T12:00:00Z | 2024-04-10T22:00:00Z | 2024-04-10T22:00:00Z | 1h | — | — | 3438.44 | 76.733 | 2024-04-12T17:00:00Z | stop | -0.538071 | -0.556302 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ETHUSDT | -1 | 2024-05-06T20:00:00Z | 2024-05-07T12:00:00Z | 2024-05-07T12:00:00Z | 4h-close | 2024-05-07T16:00:00Z | 4 | 3152.04 | 90.134 | 2024-05-13T09:00:00Z | stop | +1.159892 | +1.146533 | tuning | entered +1.3763 |
| ETHUSDT | -1 | 2024-08-27T16:00:00Z | 2024-08-28T14:00:00Z | 2024-08-28T14:00:00Z | 1h | — | — | 2587.77 | 105.116 | 2024-08-29T16:00:00Z | stop | -1.023442 | -1.033089 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| ETHUSDT | -1 | 2024-10-02T00:00:00Z | 2024-10-05T17:00:00Z | 2024-10-05T17:00:00Z | 1h | 2024-10-08T12:00:00Z | 67 | 2442.36 | 38.6131 | 2024-10-06T15:00:00Z | stop | -1.053817 | -1.078918 | holdout | entered -0.3628 |
| ETHUSDT | +1 | 2025-01-03T20:00:00Z | 2025-01-05T20:00:00Z | 2025-01-05T20:00:00Z | 4h-close | — | — | 3590.89 | 46.0324 | 2025-01-07T15:00:00Z | stop | -1.031627 | -1.063048 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| ETHUSDT | +1 | 2025-06-30T04:00:00Z | 2025-06-30T18:00:00Z | 2025-06-30T18:00:00Z | 1h | — | — | 2446.1 | 40.6491 | 2025-07-01T08:00:00Z | stop | -1.065682 | -1.089952 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| ETHUSDT | +1 | 2025-07-02T20:00:00Z | 2025-07-05T07:00:00Z | 2025-07-05T07:00:00Z | 1h | — | — | 2469.58 | 56.6163 | 2025-07-22T09:00:00Z | stop | +19.389923 | +19.368141 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| ETHUSDT | +1 | 2025-08-20T20:00:00Z | 2025-08-22T04:00:00Z | 2025-08-22T04:00:00Z | 4h-close | 2025-08-22T16:00:00Z | 12 | 4118.82 | 158.165 | 2025-08-25T07:00:00Z | stop | +2.252544 | +2.241268 | holdout | entered +0.1414 |
| ETHUSDT | +1 | 2025-09-11T12:00:00Z | 2025-09-15T05:00:00Z | 2025-09-15T05:00:00Z | 1h | 2025-09-18T04:00:00Z | 71 | 4333.66 | 307.322 | 2025-09-21T08:00:00Z | bell_12_89 | -0.520639 | -0.526579 | holdout | entered -0.7758 |
| ETHUSDT | +1 | 2025-10-02T00:00:00Z | 2025-10-04T07:00:00Z | 2025-10-04T07:00:00Z | 1h | 2025-10-09T00:00:00Z | 113 | 4425.93 | 79.063 | 2025-10-08T00:00:00Z | stop | -0.956375 | -0.978998 | holdout | entered -1.0463 |
| ETHUSDT | -1 | 2026-03-26T16:00:00Z | 2026-03-29T01:00:00Z | 2026-03-29T01:00:00Z | 1h | — | — | 2072.53 | 74.5163 | 2026-03-30T09:00:00Z | stop | -1.029671 | -1.040596 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| ETHUSDT | +1 | 2026-05-03T00:00:00Z | 2026-05-03T10:00:00Z | 2026-05-03T10:00:00Z | 1h | — | — | 2271.41 | 44.1479 | 2026-05-06T19:00:00Z | stop | +0.414543 | +0.393470 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| ETHUSDT | +1 | 2026-08-17T12:00:00Z | 2026-08-18T15:00:00Z | 2026-08-18T15:00:00Z | 1h | 2026-08-30T16:00:00Z | 289 | 1895.23 | 14.9467 | 2026-08-28T17:00:00Z | stop | +32.750682 | +32.692907 | holdout | entered -1.0311 |
| NEARUSDT | +1 | 2020-12-16T20:00:00Z | 2020-12-18T11:00:00Z | 2020-12-18T11:00:00Z | 1h | — | — | 0.98655 | 0.0279498 | 2020-12-23T11:00:00Z | stop | -0.008734 | -0.045106 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| NEARUSDT | +1 | 2021-03-29T12:00:00Z | 2021-04-01T15:00:00Z | 2021-04-01T15:00:00Z | 1h | 2021-04-05T00:00:00Z | 81 | 5.8136 | 0.310004 | 2021-04-03T18:00:00Z | stop | -1.246072 | -1.265325 | tuning | entered -1.2828 |
| NEARUSDT | -1 | 2021-05-09T08:00:00Z | 2021-05-10T11:00:00Z | 2021-05-10T11:00:00Z | 1h | — | — | 5.24687 | 0.20157 | 2021-05-12T10:00:00Z | stop | -0.790089 | -0.815515 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| NEARUSDT | -1 | 2021-06-16T12:00:00Z | 2021-06-17T14:00:00Z | 2021-06-17T14:00:00Z | 1h | 2021-06-18T04:00:00Z | 14 | 3.25696 | 0.183057 | 2021-06-18T12:00:00Z | stop | -0.646974 | -0.664083 | tuning | entered -0.6224 |
| NEARUSDT | +1 | 2021-10-02T16:00:00Z | 2021-10-03T03:00:00Z | 2021-10-03T03:00:00Z | 1h | 2021-10-06T16:00:00Z | 85 | 8.08708 | 0.342924 | 2021-10-03T08:00:00Z | stop | -1.024083 | -1.048165 | tuning | entered +0.0776 |
| NEARUSDT | -1 | 2022-02-11T00:00:00Z | 2022-02-11T17:00:00Z | 2022-02-11T17:00:00Z | 1h | 2022-02-17T20:00:00Z | 147 | 12.2554 | 0.478366 | 2022-02-15T09:00:00Z | stop | +1.632495 | +1.608708 | tuning | entered +2.1736 |
| NEARUSDT | -1 | 2022-03-07T20:00:00Z | 2022-03-08T16:00:00Z | 2022-03-08T16:00:00Z | 4h-close | — | — | 10.1677 | 0.424725 | 2022-03-09T04:00:00Z | stop | -1.022885 | -1.046325 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| NEARUSDT | -1 | 2022-07-11T12:00:00Z | 2022-07-12T19:00:00Z | 2022-07-12T19:00:00Z | 1h | — | — | 3.5115 | 0.253495 | 2022-07-14T20:00:00Z | stop | -1.036689 | -1.050041 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| NEARUSDT | -1 | 2022-11-08T04:00:00Z | 2022-11-10T12:00:00Z | 2022-11-10T12:00:00Z | 4h-close | — | — | 3.02092 | 0.875923 | 2022-12-07T00:00:00Z | bell_12_89 | +0.434875 | +0.432642 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| NEARUSDT | +1 | 2023-02-16T04:00:00Z | 2023-02-17T13:00:00Z | 2023-02-17T13:00:00Z | 1h | — | — | 2.35507 | 0.0809267 | 2023-02-22T03:00:00Z | stop | +0.350544 | +0.320230 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| NEARUSDT | -1 | 2023-03-16T00:00:00Z | 2023-03-16T13:00:00Z | 2023-03-16T13:00:00Z | 1h | — | — | 2.13259 | 0.210588 | 2023-03-17T20:00:00Z | bell_12_89 | -0.585094 | -0.594510 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| NEARUSDT | -1 | 2023-03-21T08:00:00Z | 2023-03-22T08:00:00Z | 2023-03-22T08:00:00Z | 4h-close | 2023-03-31T12:00:00Z | 220 | 2.12826 | 0.107262 | 2023-03-29T13:00:00Z | stop | +0.158975 | +0.140218 | tuning | entered -1.0222 |
| NEARUSDT | -1 | 2023-07-05T20:00:00Z | 2023-07-06T13:00:00Z | 2023-07-06T13:00:00Z | 1h | — | — | 1.39738 | 0.0613834 | 2023-07-08T10:00:00Z | stop | -1.035636 | -1.057901 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| NEARUSDT | -1 | 2023-07-24T12:00:00Z | 2023-07-27T17:00:00Z | 2023-07-27T17:00:00Z | 1h | 2023-07-31T20:00:00Z | 99 | 1.39164 | 0.0266442 | 2023-07-28T10:00:00Z | stop | -1.045379 | -1.097110 | tuning | entered -1.0482 |
| NEARUSDT | -1 | 2023-10-04T00:00:00Z | 2023-10-05T14:00:00Z | 2023-10-05T14:00:00Z | 1h | 2023-10-17T20:00:00Z | 294 | 1.11008 | 0.0170838 | 2023-10-15T19:00:00Z | stop | +1.750268 | +1.687223 | tuning | entered -0.9004 |
| NEARUSDT | +1 | 2024-01-11T20:00:00Z | 2024-01-12T15:00:00Z | 2024-01-12T15:00:00Z | 1h | — | — | 3.48508 | 0.180919 | 2024-01-12T17:00:00Z | stop | -1.021716 | -1.041479 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| NEARUSDT | +1 | 2024-04-05T20:00:00Z | 2024-04-07T02:00:00Z | 2024-04-07T02:00:00Z | 1h | — | — | 6.86494 | 0.253063 | 2024-04-07T22:00:00Z | stop | -0.914527 | -0.942214 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| NEARUSDT | +1 | 2024-05-04T08:00:00Z | 2024-05-05T07:00:00Z | 2024-05-05T07:00:00Z | 1h | 2024-05-14T00:00:00Z | 209 | 6.69829 | 0.217707 | 2024-05-08T16:00:00Z | stop | +0.415372 | +0.383364 | tuning | entered -1.0367 |
| NEARUSDT | -1 | 2024-07-25T12:00:00Z | 2024-07-27T18:00:00Z | 2024-07-27T18:00:00Z | 1h | 2024-08-12T08:00:00Z | 374 | 6.08611 | 0.416114 | 2024-08-08T22:00:00Z | stop | +2.017723 | +2.005112 | holdout | entered -1.0178 |
| NEARUSDT | -1 | 2024-08-29T20:00:00Z | 2024-08-31T08:00:00Z | 2024-08-31T08:00:00Z | 4h-close | — | — | 4.27086 | 0.159857 | 2024-09-09T08:00:00Z | stop | +1.816714 | +1.791907 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| NEARUSDT | +1 | 2024-10-14T20:00:00Z | 2024-10-15T09:00:00Z | 2024-10-15T09:00:00Z | 1h | — | — | 4.57132 | 0.507677 | 2024-10-18T00:00:00Z | bell_12_89 | -0.550375 | -0.560112 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| NEARUSDT | -1 | 2025-01-08T08:00:00Z | 2025-01-10T15:00:00Z | 2025-01-10T15:00:00Z | 1h | — | — | 5.39278 | 0.383784 | 2025-01-15T15:00:00Z | stop | -0.435966 | -0.449227 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| NEARUSDT | -1 | 2025-03-29T08:00:00Z | 2025-03-30T18:00:00Z | 2025-03-30T18:00:00Z | 1h | 2025-04-15T16:00:00Z | 382 | 2.72505 | 0.118054 | 2025-04-01T16:00:00Z | stop | -0.568663 | -0.591022 | holdout | entered -0.2898 |
| NEARUSDT | -1 | 2025-05-04T16:00:00Z | 2025-05-05T12:00:00Z | 2025-05-05T12:00:00Z | 4h-close | — | — | 2.57825 | 0.241247 | 2025-05-08T16:00:00Z | stop | -0.643568 | -0.653572 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| NEARUSDT | +1 | 2025-08-08T12:00:00Z | 2025-08-11T03:00:00Z | 2025-08-11T03:00:00Z | 1h | 2025-08-12T20:00:00Z | 41 | 2.68675 | 0.12525 | 2025-08-11T12:00:00Z | stop | -1.022617 | -1.044568 | holdout | entered -0.7008 |
| NEARUSDT | +1 | 2025-08-24T00:00:00Z | 2025-08-24T18:00:00Z | 2025-08-24T18:00:00Z | 1h | — | — | 2.59066 | 0.107335 | 2025-08-25T07:00:00Z | stop | -0.730985 | -0.755769 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| NEARUSDT | +1 | 2025-10-02T12:00:00Z | 2025-10-05T02:00:00Z | 2025-10-05T02:00:00Z | 1h | 2025-10-09T00:00:00Z | 94 | 2.82844 | 0.120557 | 2025-10-09T03:00:00Z | stop | -0.256296 | -0.280649 | holdout | entered -1.0418 |
| NEARUSDT | -1 | 2025-11-16T16:00:00Z | 2025-11-18T07:00:00Z | 2025-11-18T07:00:00Z | 1h | 2025-12-05T12:00:00Z | 413 | 2.35471 | 0.116713 | 2025-11-20T00:00:00Z | stop | -1.010020 | -1.029695 | holdout | entered +0.2645 |
| NEARUSDT | -1 | 2025-12-29T20:00:00Z | 2025-12-30T19:00:00Z | 2025-12-30T19:00:00Z | 1h | 2025-12-31T00:00:00Z | 5 | 1.5763 | 0.0482962 | 2026-01-01T14:00:00Z | stop | -0.376555 | -0.408372 | holdout | entered -1.0161 |
| NEARUSDT | -1 | 2026-01-19T00:00:00Z | 2026-01-20T06:00:00Z | 2026-01-20T06:00:00Z | 1h | 2026-02-19T00:00:00Z | 714 | 1.62713 | 0.0491342 | 2026-01-21T21:00:00Z | stop | +0.087117 | +0.055057 | holdout | entered -0.8950 |
| NEARUSDT | +1 | 2026-05-06T16:00:00Z | 2026-05-07T13:00:00Z | 2026-05-07T13:00:00Z | 1h | 2026-05-19T00:00:00Z | 275 | 1.34938 | 0.146624 | 2026-05-15T14:00:00Z | stop | +0.157695 | +0.147407 | holdout | entered +8.7450 |
| NEARUSDT | +1 | 2026-06-15T08:00:00Z | 2026-06-16T08:00:00Z | 2026-06-16T08:00:00Z | 4h-close | — | — | 2.22223 | 0.227765 | 2026-06-17T22:00:00Z | stop | -1.008176 | -1.018433 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| SOLUSDT | -1 | 2020-11-26T12:00:00Z | 2020-11-27T10:00:00Z | 2020-11-27T10:00:00Z | 1h | — | — | 1.95817 | 0.152573 | 2020-11-30T01:00:00Z | stop | -1.141849 | -1.154184 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| SOLUSDT | -1 | 2021-07-27T20:00:00Z | 2021-07-28T07:00:00Z | 2021-07-28T07:00:00Z | 1h | 2021-07-29T04:00:00Z | 21 | 28.6337 | 1.18473 | 2021-07-28T12:00:00Z | stop | -1.021302 | -1.044971 | tuning | entered -0.7809 |
| SOLUSDT | +1 | 2021-10-01T16:00:00Z | 2021-10-04T19:00:00Z | 2021-10-04T19:00:00Z | 1h | 2021-10-08T20:00:00Z | 97 | 164.391 | 6.68337 | 2021-10-05T03:00:00Z | stop | -1.027599 | -1.052696 | tuning | entered -1.0249 |
| SOLUSDT | +1 | 2021-10-15T12:00:00Z | 2021-10-16T10:00:00Z | 2021-10-16T10:00:00Z | 1h | 2021-10-20T12:00:00Z | 98 | 149.831 | 11.9847 | 2021-10-24T12:00:00Z | stop | +0.994056 | +0.980017 | tuning | entered +4.7230 |
| SOLUSDT | +1 | 2021-12-01T12:00:00Z | 2021-12-02T10:00:00Z | 2021-12-02T10:00:00Z | 1h | — | — | 216.975 | 10.4227 | 2021-12-03T19:00:00Z | stop | -1.030147 | -1.051465 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| SOLUSDT | -1 | 2021-12-29T08:00:00Z | 2021-12-30T23:00:00Z | 2021-12-30T23:00:00Z | 1h | 2022-01-17T12:00:00Z | 421 | 179.214 | 7.50443 | 2022-01-02T01:00:00Z | stop | -1.007168 | -1.030549 | tuning | entered +5.8468 |
| SOLUSDT | -1 | 2022-02-11T08:00:00Z | 2022-02-11T18:00:00Z | 2022-02-11T18:00:00Z | 1h | 2022-02-17T16:00:00Z | 142 | 115.461 | 9.98061 | 2022-02-15T02:00:00Z | stop | +0.538324 | +0.528034 | tuning | entered +0.8530 |
| SOLUSDT | -1 | 2022-03-04T20:00:00Z | 2022-03-06T03:00:00Z | 2022-03-06T03:00:00Z | 1h | — | — | 94.9082 | 6.26818 | 2022-03-09T04:00:00Z | stop | +0.050054 | +0.035943 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| SOLUSDT | -1 | 2022-06-29T12:00:00Z | 2022-07-01T11:00:00Z | 2022-07-01T11:00:00Z | 1h | — | — | 33.6112 | 1.64124 | 2022-07-01T21:00:00Z | stop | -1.020743 | -1.040723 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| SOLUSDT | -1 | 2022-07-12T00:00:00Z | 2022-07-12T19:00:00Z | 2022-07-12T19:00:00Z | 1h | — | — | 34.6756 | 1.14561 | 2022-07-14T00:00:00Z | stop | -1.038788 | -1.068556 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| SOLUSDT | -1 | 2022-08-03T08:00:00Z | 2022-08-03T23:00:00Z | 2022-08-03T23:00:00Z | 1h | — | — | 40.4846 | 1.72463 | 2022-08-05T07:00:00Z | stop | -1.024394 | -1.047368 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| SOLUSDT | -1 | 2022-09-15T16:00:00Z | 2022-09-18T12:00:00Z | 2022-09-18T12:00:00Z | 4h-close | 2022-09-23T12:00:00Z | 120 | 34.3176 | 1.00765 | 2022-09-23T22:00:00Z | stop | +0.739490 | +0.706817 | tuning | entered -1.0307 |
| SOLUSDT | -1 | 2022-10-02T00:00:00Z | 2022-10-02T11:00:00Z | 2022-10-02T11:00:00Z | 1h | — | — | 33.0758 | 0.745798 | 2022-10-03T16:00:00Z | stop | -1.037434 | -1.081283 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| SOLUSDT | -1 | 2022-10-08T04:00:00Z | 2022-10-10T08:00:00Z | 2022-10-10T08:00:00Z | 4h-close | 2022-10-19T00:00:00Z | 208 | 33.3199 | 0.429918 | 2022-10-14T02:00:00Z | stop | +2.512354 | +2.437134 | tuning | entered +0.9711 |
| SOLUSDT | -1 | 2022-11-08T04:00:00Z | 2022-11-10T11:00:00Z | 2022-11-10T11:00:00Z | 1h | 2022-11-28T12:00:00Z | 433 | 31.156 | 18.602 | 2022-12-14T16:00:00Z | bell_12_89 | -0.197648 | -0.198367 | tuning | entered -1.1144 |
| SOLUSDT | +1 | 2023-02-16T04:00:00Z | 2023-02-17T18:00:00Z | 2023-02-17T18:00:00Z | 1h | — | — | 22.3187 | 0.653288 | 2023-02-21T09:00:00Z | stop | +3.211122 | +3.174307 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| SOLUSDT | +1 | 2023-04-28T20:00:00Z | 2023-04-30T07:00:00Z | 2023-04-30T07:00:00Z | 1h | — | — | 21.3347 | 2.12434 | 2023-05-02T00:00:00Z | bell_12_89 | -0.673778 | -0.684492 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| SOLUSDT | -1 | 2023-06-06T08:00:00Z | 2023-06-07T07:00:00Z | 2023-06-07T07:00:00Z | 1h | — | — | 20.5427 | 0.512694 | 2023-06-09T12:00:00Z | stop | +1.312705 | +1.274311 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| SOLUSDT | +1 | 2023-08-09T04:00:00Z | 2023-08-10T12:00:00Z | 2023-08-10T12:00:00Z | 4h-close | — | — | 23.7379 | 0.658109 | 2023-08-15T20:00:00Z | stop | -0.297987 | -0.334948 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| SOLUSDT | +1 | 2024-01-28T04:00:00Z | 2024-01-29T03:00:00Z | 2024-01-29T03:00:00Z | 1h | 2024-02-02T04:00:00Z | 97 | 91.6977 | 5.35233 | 2024-02-01T02:00:00Z | stop | -0.280731 | -0.298739 | tuning | entered -0.5133 |
| SOLUSDT | +1 | 2024-02-27T04:00:00Z | 2024-02-28T08:00:00Z | 2024-02-28T08:00:00Z | 4h-close | 2024-03-21T08:00:00Z | 528 | 106.945 | 3.25532 | 2024-02-28T18:00:00Z | stop | -1.074457 | -1.107810 | tuning | entered -1.0187 |
| SOLUSDT | -1 | 2024-07-04T08:00:00Z | 2024-07-07T07:00:00Z | 2024-07-07T07:00:00Z | 1h | 2024-07-07T20:00:00Z | 13 | 144.097 | 4.34868 | 2024-07-09T09:00:00Z | stop | -0.534359 | -0.566750 | holdout | entered -0.8402 |
| SOLUSDT | -1 | 2024-08-28T20:00:00Z | 2024-08-29T19:00:00Z | 2024-08-29T19:00:00Z | 1h | — | — | 149.275 | 9.65041 | 2024-09-06T13:00:00Z | stop | +0.605835 | +0.591676 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| SOLUSDT | +1 | 2024-10-13T00:00:00Z | 2024-10-13T09:00:00Z | 2024-10-13T09:00:00Z | 1h | — | — | 144.484 | 2.10381 | 2024-10-13T16:00:00Z | stop | -1.069178 | -1.138355 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| SOLUSDT | -1 | 2025-01-08T16:00:00Z | 2025-01-09T04:00:00Z | 2025-01-09T04:00:00Z | 4h-close | — | — | 199.086 | 4.80605 | 2025-01-15T14:00:00Z | stop | +0.366034 | +0.325811 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| SOLUSDT | -1 | 2025-03-28T20:00:00Z | 2025-03-30T12:00:00Z | 2025-03-30T12:00:00Z | 4h-close | — | — | 130.23 | 5.22965 | 2025-04-01T16:00:00Z | stop | -1.036892 | -1.061294 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| SOLUSDT | +1 | 2025-08-08T12:00:00Z | 2025-08-10T18:00:00Z | 2025-08-10T18:00:00Z | 1h | 2025-08-17T08:00:00Z | 158 | 173.45 | 8.16022 | 2025-08-11T23:00:00Z | stop | -1.026195 | -1.047951 | holdout | entered -1.0304 |
| SOLUSDT | +1 | 2025-10-02T04:00:00Z | 2025-10-03T16:00:00Z | 2025-10-03T16:00:00Z | 4h-close | — | — | 229.083 | 5.58656 | 2025-10-03T18:00:00Z | stop | -1.044610 | -1.086116 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| SOLUSDT | -1 | 2025-10-30T16:00:00Z | 2025-10-31T19:00:00Z | 2025-10-31T19:00:00Z | 1h | 2025-11-12T00:00:00Z | 269 | 190.761 | 4.92099 | 2025-11-10T00:00:00Z | stop | +3.865161 | +3.829357 | holdout | entered +0.8381 |
| SOLUSDT | -1 | 2026-03-07T16:00:00Z | 2026-03-08T12:00:00Z | 2026-03-08T12:00:00Z | 4h-close | — | — | 86.9663 | 4.22626 | 2026-03-09T20:00:00Z | stop | -0.796149 | -0.816111 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| SOLUSDT | -1 | 2026-03-26T20:00:00Z | 2026-03-28T12:00:00Z | 2026-03-28T12:00:00Z | 4h-close | 2026-04-07T04:00:00Z | 232 | 88.8694 | 5.97939 | 2026-04-03T13:00:00Z | stop | +0.065034 | +0.051221 | holdout | entered -1.0550 |
| SOLUSDT | -1 | 2026-04-27T20:00:00Z | 2026-04-29T15:00:00Z | 2026-04-29T15:00:00Z | 1h | — | — | 84.8559 | 1.07589 | 2026-05-01T04:00:00Z | stop | -0.583166 | -0.661293 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| SOLUSDT | -1 | 2026-06-23T20:00:00Z | 2026-06-24T10:00:00Z | 2026-06-24T10:00:00Z | 1h | — | — | 70.7067 | 1.43669 | 2026-06-26T08:00:00Z | stop | -0.986337 | -1.035016 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| ZECUSDT | +1 | 2020-05-17T08:00:00Z | 2020-05-19T10:00:00Z | 2020-05-19T10:00:00Z | 1h | — | — | 43.4672 | 4.7428 | 2020-05-26T16:00:00Z | bell_12_89 | -0.760559 | -0.770359 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ZECUSDT | +1 | 2020-07-06T20:00:00Z | 2020-07-07T16:00:00Z | 2020-07-07T16:00:00Z | 4h-close | 2020-07-21T12:00:00Z | 332 | 53.8363 | 1.79365 | 2020-07-09T16:00:00Z | stop | -0.141084 | -0.172107 | tuning | entered +2.8952 |
| ZECUSDT | +1 | 2020-08-30T20:00:00Z | 2020-09-01T03:00:00Z | 2020-09-01T03:00:00Z | 1h | — | — | 78.1295 | 2.17047 | 2020-09-02T12:00:00Z | stop | -1.131278 | -1.167775 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ZECUSDT | +1 | 2020-12-17T00:00:00Z | 2020-12-18T03:00:00Z | 2020-12-18T03:00:00Z | 1h | — | — | 70.7867 | 4.74328 | 2020-12-21T11:00:00Z | stop | -1.058609 | -1.074032 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ZECUSDT | +1 | 2021-02-02T08:00:00Z | 2021-02-05T06:00:00Z | 2021-02-05T06:00:00Z | 1h | — | — | 82.2748 | 10.9852 | 2021-02-15T03:00:00Z | stop | +1.276354 | +1.267053 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ZECUSDT | +1 | 2021-03-09T04:00:00Z | 2021-03-10T14:00:00Z | 2021-03-10T14:00:00Z | 1h | 2021-03-18T04:00:00Z | 182 | 130.864 | 5.39621 | 2021-03-12T14:00:00Z | stop | +1.628414 | +1.602288 | tuning | entered -0.4239 |
| ZECUSDT | +1 | 2021-03-29T08:00:00Z | 2021-03-30T17:00:00Z | 2021-03-30T17:00:00Z | 1h | 2021-04-09T04:00:00Z | 227 | 137.914 | 13.6457 | 2021-04-07T10:00:00Z | stop | +1.718179 | +1.706050 | tuning | entered +0.9082 |
| ZECUSDT | +1 | 2021-04-27T16:00:00Z | 2021-04-28T20:00:00Z | 2021-04-28T20:00:00Z | 4h-close | 2021-05-12T04:00:00Z | 320 | 227.672 | 10.3084 | 2021-04-29T17:00:00Z | stop | -1.045844 | -1.068430 | tuning | entered -1.0147 |
| ZECUSDT | +1 | 2021-09-02T08:00:00Z | 2021-09-03T12:00:00Z | 2021-09-03T12:00:00Z | 4h-close | — | — | 146.027 | 7.593 | 2021-09-07T09:00:00Z | stop | +0.764894 | +0.744173 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ZECUSDT | -1 | 2021-10-12T08:00:00Z | 2021-10-13T07:00:00Z | 2021-10-13T07:00:00Z | 1h | — | — | 121.115 | 5.96503 | 2021-10-14T04:00:00Z | stop | -1.013944 | -1.033749 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ZECUSDT | +1 | 2021-11-21T08:00:00Z | 2021-11-23T04:00:00Z | 2021-11-23T04:00:00Z | 4h-close | — | — | 186.137 | 23.6431 | 2021-11-26T09:00:00Z | stop | +1.866344 | +1.856521 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ZECUSDT | -1 | 2022-02-18T12:00:00Z | 2022-02-19T12:00:00Z | 2022-02-19T12:00:00Z | 4h-close | — | — | 125.468 | 17.2681 | 2022-02-25T16:00:00Z | stop | +0.025875 | +0.019627 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ZECUSDT | -1 | 2022-03-07T00:00:00Z | 2022-03-07T21:00:00Z | 2022-03-07T21:00:00Z | 1h | — | — | 110.874 | 4.81384 | 2022-03-07T23:00:00Z | stop | -1.022532 | -1.045065 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ZECUSDT | -1 | 2022-07-23T20:00:00Z | 2022-07-24T21:00:00Z | 2022-07-24T21:00:00Z | 1h | — | — | 61.1504 | 1.90038 | 2022-07-27T15:00:00Z | stop | +0.263876 | +0.232850 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ZECUSDT | -1 | 2022-12-17T00:00:00Z | 2022-12-19T12:00:00Z | 2022-12-19T12:00:00Z | 4h-close | — | — | 44.3621 | 0.992066 | 2022-12-26T05:00:00Z | stop | +2.981626 | +2.939413 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ZECUSDT | -1 | 2023-06-01T00:00:00Z | 2023-06-02T15:00:00Z | 2023-06-02T15:00:00Z | 1h | — | — | 33.0031 | 1.16311 | 2023-06-11T18:00:00Z | stop | +6.205378 | +6.181087 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ZECUSDT | +1 | 2023-11-25T00:00:00Z | 2023-11-26T07:00:00Z | 2023-11-26T07:00:00Z | 1h | — | — | 28.024 | 2.05597 | 2023-11-27T20:00:00Z | bell_12_89 | -0.549538 | -0.563903 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ZECUSDT | +1 | 2024-03-26T00:00:00Z | 2024-03-27T23:00:00Z | 2024-03-27T23:00:00Z | 1h | — | — | 30.2293 | 0.910735 | 2024-03-29T08:00:00Z | stop | -1.073235 | -1.106927 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ZECUSDT | -1 | 2024-05-12T00:00:00Z | 2024-05-12T09:00:00Z | 2024-05-12T09:00:00Z | 1h | — | — | 23.0803 | 0.440329 | 2024-05-15T13:00:00Z | stop | -0.298851 | -0.350402 | tuning | NOT ENTERED: no trigger by the window close / as-of |
| ZECUSDT | -1 | 2024-09-22T20:00:00Z | 2024-09-23T09:00:00Z | 2024-09-23T09:00:00Z | 1h | — | — | 30.3512 | 0.971172 | 2024-09-26T15:00:00Z | stop | -1.016636 | -1.047388 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| ZECUSDT | +1 | 2024-11-17T00:00:00Z | 2024-11-17T18:00:00Z | 2024-11-17T18:00:00Z | 1h | 2024-11-21T16:00:00Z | 94 | 41.0307 | 2.92932 | 2024-11-19T21:00:00Z | stop | -0.348489 | -0.363339 | holdout | entered +1.0917 |
| ZECUSDT | -1 | 2025-03-21T16:00:00Z | 2025-03-23T20:00:00Z | 2025-03-23T20:00:00Z | 4h-close | — | — | 31.8825 | 1.02245 | 2025-03-24T06:00:00Z | stop | -1.027652 | -1.058335 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| ZECUSDT | +1 | 2025-12-10T08:00:00Z | 2025-12-11T11:00:00Z | 2025-12-11T11:00:00Z | 1h | — | — | 316.022 | 102.938 | 2025-12-15T04:00:00Z | bell_12_89 | +0.027245 | +0.023165 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| ZECUSDT | +1 | 2025-12-20T00:00:00Z | 2025-12-21T21:00:00Z | 2025-12-21T21:00:00Z | 1h | — | — | 434.205 | 14.0054 | 2025-12-22T20:00:00Z | stop | -1.040997 | -1.072500 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| ZECUSDT | -1 | 2026-02-19T12:00:00Z | 2026-02-20T09:00:00Z | 2026-02-20T09:00:00Z | 1h | 2026-03-06T16:00:00Z | 343 | 309.372 | 48.142 | 2026-03-04T09:00:00Z | stop | +0.518209 | +0.513047 | holdout | entered -0.7735 |
| ZECUSDT | -1 | 2026-03-22T00:00:00Z | 2026-03-23T09:00:00Z | 2026-03-23T09:00:00Z | 1h | — | — | 228.346 | 11.0663 | 2026-03-23T12:00:00Z | stop | -1.020134 | -1.040269 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| ZECUSDT | +1 | 2026-06-03T00:00:00Z | 2026-06-03T19:00:00Z | 2026-06-03T19:00:00Z | 1h | — | — | 556.213 | 58.7471 | 2026-06-04T03:00:00Z | stop | -1.005585 | -1.015553 | holdout | NOT ENTERED: no trigger by the window close / as-of |
| ZECUSDT | +1 | 2026-08-04T20:00:00Z | 2026-08-07T01:00:00Z | 2026-08-07T01:00:00Z | 1h | — | — | 495.362 | 10.3182 | 2026-08-10T17:00:00Z | stop | -0.792149 | -0.840804 | holdout | NOT ENTERED: no trigger by the window close / as-of |

## The miss column — every window the relay never activated, whole (Tier-E)

| asset | dir | arm close | lag | trigger close | window close | 89/316 against | first 1h 9/12 close | disposition | what v6 did | v6 net R | late twin | tier | selection_not_a_result | gates |
|---|---:|---|---:|---|---|---|---|---|---|---:|---|---|---|---|
| BTCUSDT | -1 | 2019-12-27T12:00:00Z | — | — | 2019-12-28T04:00:00Z | 2020-01-11T00:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | +1 | 2020-01-27T00:00:00Z | 1 | 2020-01-27T04:00:00Z | 2020-02-17T20:00:00Z | 2020-03-08T00:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +1.8131 | RELAYED +0.9901 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | +1 | 2020-02-18T20:00:00Z | 4 | 2020-02-19T12:00:00Z | 2020-02-20T12:00:00Z | 2020-03-08T00:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.0710 | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | +1 | 2020-02-24T00:00:00Z | — | — | 2020-02-24T04:00:00Z | 2020-03-08T00:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | +1 | 2020-08-24T12:00:00Z | — | — | 2020-08-25T12:00:00Z | 2020-09-08T20:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | +1 | 2020-11-29T04:00:00Z | 4 | 2020-11-29T20:00:00Z | 2020-12-09T16:00:00Z | 2021-05-14T16:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +1.2069 | RELAYED -0.6750 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | +1 | 2021-03-03T12:00:00Z | — | — | 2021-03-05T12:00:00Z | 2021-05-14T16:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | +1 | 2021-05-05T16:00:00Z | 2 | 2021-05-06T00:00:00Z | 2021-05-12T20:00:00Z | 2021-05-14T16:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.1300 | RELAYED -0.7177 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2021-07-01T08:00:00Z | 2 | 2021-07-01T16:00:00Z | 2021-07-04T08:00:00Z | 2021-07-31T04:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.7894 | RELAYED -0.8242 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2021-07-05T16:00:00Z | 1 | 2021-07-05T20:00:00Z | 2021-07-24T00:00:00Z | 2021-07-31T04:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.1772 | RELAYED +0.0218 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | +1 | 2021-11-07T04:00:00Z | 4 | 2021-11-07T20:00:00Z | 2021-11-16T08:00:00Z | 2021-11-28T12:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +3.1217 | RELAYED -0.7710 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2022-07-26T08:00:00Z | — | — | 2022-07-28T04:00:00Z | 2022-08-13T08:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2022-09-27T20:00:00Z | 4 | 2022-09-28T12:00:00Z | 2022-10-04T08:00:00Z | 2022-10-31T00:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.8874 | RELAYED -0.7471 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | +1 | 2023-05-04T08:00:00Z | 0 | 2023-05-04T08:00:00Z | 2023-05-08T04:00:00Z | 2023-05-17T04:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -0.8185 | RELAYED -1.0721 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2023-09-01T00:00:00Z | 2 | 2023-09-01T08:00:00Z | 2023-09-14T04:00:00Z | 2023-10-05T08:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +0.0149 | RELAYED -1.0972 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | +1 | 2023-12-19T00:00:00Z | 2 | 2023-12-19T08:00:00Z | 2023-12-27T08:00:00Z | 2024-01-26T00:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.0724 | RELAYED +0.3088 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | +1 | 2024-10-07T08:00:00Z | — | — | 2024-10-09T00:00:00Z | 2025-02-14T00:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | +1 | 2024-11-05T16:00:00Z | 3 | 2024-11-06T04:00:00Z | 2024-12-20T04:00:00Z | 2025-02-14T00:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +3.8512 | RELAYED +2.3168 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2025-02-22T00:00:00Z | 5 | 2025-02-22T20:00:00Z | 2025-03-20T12:00:00Z | 2025-04-24T00:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +9.1430 | RELAYED +9.4156 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2025-04-03T00:00:00Z | 3 | 2025-04-03T12:00:00Z | 2025-04-12T08:00:00Z | 2025-04-24T00:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.0488 | RELAYED -1.0446 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | +1 | 2025-06-16T20:00:00Z | — | — | 2025-06-17T16:00:00Z | 2025-08-28T00:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2025-12-06T04:00:00Z | 0 | 2025-12-06T04:00:00Z | 2025-12-09T16:00:00Z | 2026-01-16T08:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -0.8173 | RELAYED -0.8425 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2025-12-29T12:00:00Z | 3 | 2025-12-30T00:00:00Z | 2025-12-31T12:00:00Z | 2026-01-16T08:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.7982 | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2025-12-31T20:00:00Z | 3 | 2026-01-01T08:00:00Z | 2026-01-02T04:00:00Z | 2026-01-16T08:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.9886 | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2026-03-26T16:00:00Z | 0 | 2026-03-26T16:00:00Z | 2026-04-06T12:00:00Z | 2026-04-15T16:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +0.8804 | RELAYED -1.0321 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2026-06-17T20:00:00Z | 3 | 2026-06-18T08:00:00Z | 2026-07-04T00:00:00Z | 2026-08-20T12:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +0.0132 | RELAYED -1.0798 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | +1 | 2026-09-14T20:00:00Z | 0 | 2026-09-14T20:00:00Z | 2026-09-15T08:00:00Z | — | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -1.1055 | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2020-03-07T04:00:00Z | — | — | 2020-03-08T16:00:00Z | 2020-03-13T00:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2020-05-15T00:00:00Z | — | — | 2020-05-16T00:00:00Z | 2020-09-24T08:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2020-05-28T00:00:00Z | 0 | 2020-05-28T00:00:00Z | 2020-06-15T00:00:00Z | 2020-09-24T08:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +2.7901 | RELAYED +0.3623 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2020-08-29T20:00:00Z | — | — | 2020-09-04T08:00:00Z | 2020-09-24T08:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2020-09-13T08:00:00Z | — | — | 2020-09-13T12:00:00Z | 2020-09-24T08:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2020-10-02T00:00:00Z | 2 | 2020-10-02T08:00:00Z | 2020-10-09T20:00:00Z | 2020-10-13T04:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.0437 | RELAYED -1.0536 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2020-11-02T04:00:00Z | 0 | 2020-11-02T04:00:00Z | 2020-11-02T20:00:00Z | 2021-05-30T12:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -0.8944 | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2020-11-05T00:00:00Z | 0 | 2020-11-05T00:00:00Z | 2020-12-09T08:00:00Z | 2021-05-30T12:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +4.3350 | RELAYED +2.3093 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2020-12-13T12:00:00Z | 0 | 2020-12-13T12:00:00Z | 2020-12-24T04:00:00Z | 2021-05-30T12:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +3.6422 | RELAYED +3.8715 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2021-04-20T20:00:00Z | 5 | 2021-04-21T16:00:00Z | 2021-05-17T16:00:00Z | 2021-05-30T12:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.0238 | RELAYED -0.6910 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2021-06-08T04:00:00Z | 0 | 2021-06-08T04:00:00Z | 2021-06-30T00:00:00Z | 2021-08-01T08:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +0.7859 | RELAYED -1.0200 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2021-08-27T16:00:00Z | 4 | 2021-08-28T08:00:00Z | 2021-09-08T16:00:00Z | 2021-09-28T08:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +1.7103 | RELAYED +1.4497 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2021-11-25T20:00:00Z | — | — | 2021-11-26T12:00:00Z | 2021-12-14T04:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2021-12-28T08:00:00Z | 0 | 2021-12-28T08:00:00Z | 2022-02-02T04:00:00Z | 2022-03-25T12:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +0.6596 | RELAYED +0.4065 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2022-02-13T20:00:00Z | — | — | 2022-02-15T08:00:00Z | 2022-03-25T12:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2022-09-07T04:00:00Z | 1 | 2022-09-07T08:00:00Z | 2022-09-08T12:00:00Z | 2022-09-10T16:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.0180 | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2022-10-07T16:00:00Z | 4 | 2022-10-08T08:00:00Z | 2022-10-18T04:00:00Z | 2022-10-29T16:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +0.8031 | RELAYED +0.2075 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2022-12-07T20:00:00Z | — | — | 2022-12-08T20:00:00Z | 2023-01-11T04:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2023-05-24T16:00:00Z | 1 | 2023-05-24T20:00:00Z | 2023-05-27T20:00:00Z | 2023-05-29T20:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.0360 | RELAYED -0.0898 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2023-07-13T16:00:00Z | 0 | 2023-07-13T16:00:00Z | 2023-07-19T00:00:00Z | 2023-08-03T12:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -0.6132 | RELAYED -0.7792 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2023-07-20T12:00:00Z | — | — | 2023-07-20T16:00:00Z | 2023-08-03T12:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2023-08-31T20:00:00Z | 3 | 2023-09-01T08:00:00Z | 2023-09-16T16:00:00Z | 2023-10-25T12:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.3978 | RELAYED -1.0449 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2023-11-19T20:00:00Z | 4 | 2023-11-20T12:00:00Z | 2023-12-13T08:00:00Z | 2024-04-17T04:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.0669 | RELAYED +0.5914 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2023-12-13T20:00:00Z | 6 | 2023-12-14T20:00:00Z | 2023-12-18T00:00:00Z | 2024-04-17T04:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.8374 | RELAYED -0.7441 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2023-12-27T12:00:00Z | 1 | 2023-12-27T16:00:00Z | 2024-01-04T04:00:00Z | 2024-04-17T04:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.8097 | RELAYED -0.7887 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2024-03-31T08:00:00Z | 0 | 2024-03-31T08:00:00Z | 2024-04-02T00:00:00Z | 2024-04-17T04:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -1.1095 | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2024-04-24T20:00:00Z | 4 | 2024-04-25T12:00:00Z | 2024-04-28T04:00:00Z | 2024-05-22T08:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.0481 | RELAYED -1.0250 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2024-04-30T12:00:00Z | 0 | 2024-04-30T12:00:00Z | 2024-05-06T04:00:00Z | 2024-05-22T08:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -0.3444 | RELAYED -0.8806 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2024-09-15T20:00:00Z | 2 | 2024-09-16T04:00:00Z | 2024-09-19T20:00:00Z | 2024-10-20T20:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.0476 | RELAYED -0.8091 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2025-01-27T00:00:00Z | 0 | 2025-01-27T00:00:00Z | 2025-01-31T20:00:00Z | 2025-05-10T04:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +0.4907 | RELAYED -0.8804 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2025-02-01T20:00:00Z | 2 | 2025-02-02T04:00:00Z | 2025-02-23T08:00:00Z | 2025-05-10T04:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +1.5813 | RELAYED -0.1226 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2025-02-24T16:00:00Z | 0 | 2025-02-24T16:00:00Z | 2025-03-24T12:00:00Z | 2025-05-10T04:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +5.2363 | RELAYED +0.4757 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2025-06-03T04:00:00Z | 2 | 2025-06-03T12:00:00Z | 2025-06-06T04:00:00Z | 2025-10-14T12:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.5820 | RELAYED -1.0673 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2025-06-10T00:00:00Z | 0 | 2025-06-10T00:00:00Z | 2025-06-14T04:00:00Z | 2025-10-14T12:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +0.4020 | RELAYED -0.3682 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2025-06-16T20:00:00Z | 0 | 2025-06-16T20:00:00Z | 2025-06-17T00:00:00Z | 2025-10-14T12:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -1.0334 | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2025-08-05T04:00:00Z | 0 | 2025-08-05T04:00:00Z | 2025-08-20T08:00:00Z | 2025-10-14T12:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -1.0521 | RELAYED -1.0506 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2025-10-29T20:00:00Z | 0 | 2025-10-29T20:00:00Z | 2025-12-03T20:00:00Z | 2026-01-15T12:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +6.1794 | RELAYED +6.1843 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2026-02-27T16:00:00Z | 4 | 2026-02-28T08:00:00Z | 2026-03-03T00:00:00Z | 2026-04-14T08:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.0148 | RELAYED -0.6229 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2026-03-07T20:00:00Z | — | — | 2026-03-10T08:00:00Z | 2026-04-14T08:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2026-03-22T12:00:00Z | — | — | 2026-03-24T08:00:00Z | 2026-04-14T08:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2026-04-02T12:00:00Z | 6 | 2026-04-03T12:00:00Z | 2026-04-06T08:00:00Z | 2026-04-14T08:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.4175 | RELAYED -0.7422 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2026-04-29T12:00:00Z | — | — | 2026-04-29T16:00:00Z | 2026-05-18T12:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2026-06-18T16:00:00Z | 1 | 2026-06-18T20:00:00Z | 2026-07-03T00:00:00Z | 2026-07-21T00:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.0438 | RELAYED -1.0523 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2026-08-05T20:00:00Z | 0 | 2026-08-05T20:00:00Z | 2026-08-11T16:00:00Z | — | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -1.0795 | RELAYED -0.5432 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2026-08-12T12:00:00Z | — | — | 2026-08-12T20:00:00Z | — | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | +1 | 2026-09-18T12:00:00Z | 0 | 2026-09-18T12:00:00Z | — | — | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +2.7072 | RELAYED +0.2165 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | +1 | 2020-12-27T20:00:00Z | 0 | 2020-12-27T20:00:00Z | 2021-01-28T08:00:00Z | 2021-04-24T20:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +1.4896 | RELAYED +0.9810 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | +1 | 2021-01-31T04:00:00Z | — | — | 2021-01-31T20:00:00Z | 2021-04-24T20:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | +1 | 2021-02-25T20:00:00Z | 0 | 2021-02-25T20:00:00Z | 2021-02-28T20:00:00Z | 2021-04-24T20:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -1.0078 | RELAYED -1.0180 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2021-05-04T16:00:00Z | 0 | 2021-05-04T16:00:00Z | 2021-05-07T12:00:00Z | 2021-05-15T08:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -0.9638 | RELAYED -1.0028 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2021-05-13T00:00:00Z | — | — | 2021-05-14T00:00:00Z | 2021-05-15T08:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2021-07-08T12:00:00Z | 2 | 2021-07-08T20:00:00Z | 2021-07-24T12:00:00Z | 2021-08-11T04:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.4246 | RELAYED -1.0101 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | +1 | 2021-09-24T04:00:00Z | — | — | 2021-09-24T20:00:00Z | 2021-11-28T20:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | +1 | 2021-11-08T20:00:00Z | 1 | 2021-11-09T00:00:00Z | 2021-11-16T16:00:00Z | 2021-11-28T20:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +0.1092 | RELAYED -1.0181 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | +1 | 2022-01-11T04:00:00Z | 0 | 2022-01-11T04:00:00Z | 2022-01-20T08:00:00Z | 2022-01-28T20:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +0.8129 | RELAYED -0.2952 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | +1 | 2022-04-19T04:00:00Z | 1 | 2022-04-19T08:00:00Z | 2022-04-22T16:00:00Z | 2022-05-01T04:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.7536 | RELAYED -0.8487 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2022-06-28T08:00:00Z | 0 | 2022-06-28T08:00:00Z | 2022-07-08T00:00:00Z | 2022-08-08T00:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +1.3659 | RELAYED +0.5942 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2022-07-26T12:00:00Z | — | — | 2022-07-28T12:00:00Z | 2022-08-08T00:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2022-09-06T20:00:00Z | 2 | 2022-09-07T04:00:00Z | 2022-09-08T08:00:00Z | 2022-09-13T12:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.8635 | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2022-10-28T00:00:00Z | — | — | 2022-10-29T16:00:00Z | 2023-01-16T00:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2022-11-02T08:00:00Z | — | — | 2022-11-04T08:00:00Z | 2023-01-16T00:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2022-12-07T16:00:00Z | 2 | 2022-12-08T00:00:00Z | 2023-01-04T08:00:00Z | 2023-01-16T00:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.0448 | RELAYED +0.1170 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | +1 | 2023-02-02T04:00:00Z | 4 | 2023-02-02T20:00:00Z | 2023-02-07T04:00:00Z | 2023-03-06T16:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.0315 | RELAYED -1.0461 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | +1 | 2023-02-08T00:00:00Z | 2 | 2023-02-08T08:00:00Z | 2023-02-10T08:00:00Z | 2023-03-06T16:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.0198 | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2023-04-02T20:00:00Z | 2 | 2023-04-03T04:00:00Z | 2023-04-05T04:00:00Z | 2023-04-15T08:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.0167 | RELAYED -1.0177 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2023-06-05T16:00:00Z | 0 | 2023-06-05T16:00:00Z | 2023-06-22T04:00:00Z | 2023-10-29T12:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +1.6496 | RELAYED +1.6020 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | +1 | 2024-01-30T12:00:00Z | — | — | 2024-01-31T16:00:00Z | 2024-02-03T00:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | +1 | 2024-03-25T00:00:00Z | 1 | 2024-03-25T04:00:00Z | 2024-04-01T20:00:00Z | 2024-06-11T12:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +0.4096 | RELAYED -0.9918 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2024-07-03T12:00:00Z | 3 | 2024-07-04T00:00:00Z | 2024-07-13T00:00:00Z | 2024-09-24T20:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +0.7916 | RELAYED -0.4779 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2024-09-16T20:00:00Z | — | — | 2024-09-17T20:00:00Z | 2024-09-24T20:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2024-09-18T16:00:00Z | — | — | 2024-09-19T00:00:00Z | 2024-09-24T20:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | +1 | 2024-10-07T08:00:00Z | — | — | 2024-10-09T20:00:00Z | 2024-10-26T16:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | +1 | 2024-10-21T00:00:00Z | 0 | 2024-10-21T00:00:00Z | 2024-10-22T04:00:00Z | 2024-10-26T16:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -1.0349 | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2025-01-20T04:00:00Z | 0 | 2025-01-20T04:00:00Z | 2025-01-20T08:00:00Z | 2025-05-11T12:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -1.0176 | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2025-02-23T16:00:00Z | 6 | 2025-02-24T16:00:00Z | 2025-03-03T00:00:00Z | 2025-05-11T12:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +0.4262 | RELAYED -0.8107 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2025-03-03T20:00:00Z | 2 | 2025-03-04T04:00:00Z | 2025-03-21T08:00:00Z | 2025-05-11T12:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.1998 | RELAYED +2.1924 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | +1 | 2025-05-21T16:00:00Z | 2 | 2025-05-22T00:00:00Z | 2025-05-25T08:00:00Z | 2025-06-02T04:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.2939 | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | +1 | 2025-05-29T04:00:00Z | 0 | 2025-05-29T04:00:00Z | 2025-05-30T04:00:00Z | 2025-06-02T04:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -0.8324 | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2025-06-12T16:00:00Z | 2 | 2025-06-13T00:00:00Z | 2025-06-30T08:00:00Z | 2025-07-15T12:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +0.4747 | RELAYED +0.2145 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2026-07-22T04:00:00Z | 0 | 2026-07-22T04:00:00Z | 2026-08-20T00:00:00Z | 2026-08-26T04:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +2.0212 | RELAYED +0.4076 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2020-12-04T20:00:00Z | 0 | 2020-12-04T20:00:00Z | 2020-12-30T00:00:00Z | 2021-01-07T12:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +4.4971 | RELAYED +4.3341 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | +1 | 2021-03-07T12:00:00Z | 3 | 2021-03-08T00:00:00Z | 2021-03-17T00:00:00Z | 2021-05-30T08:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.0391 | RELAYED +0.0255 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | +1 | 2021-03-27T08:00:00Z | 0 | 2021-03-27T08:00:00Z | 2021-05-11T12:00:00Z | 2021-05-30T08:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +2.2569 | RELAYED +0.6453 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | +1 | 2021-05-12T00:00:00Z | 3 | 2021-05-12T12:00:00Z | 2021-05-13T20:00:00Z | 2021-05-30T08:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.6498 | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | +1 | 2021-05-16T04:00:00Z | 0 | 2021-05-16T04:00:00Z | 2021-05-20T04:00:00Z | 2021-05-30T08:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -0.8325 | RELAYED -0.3268 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | +1 | 2021-09-18T20:00:00Z | 2 | 2021-09-19T04:00:00Z | 2021-09-20T08:00:00Z | 2021-12-10T20:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.7784 | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2022-07-25T16:00:00Z | — | — | 2022-07-28T20:00:00Z | 2022-08-13T04:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2022-12-16T16:00:00Z | 1 | 2022-12-16T20:00:00Z | 2023-01-03T12:00:00Z | 2023-01-14T16:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +3.0396 | RELAYED +1.2011 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2023-03-16T00:00:00Z | — | — | 2023-03-18T00:00:00Z | 2023-03-23T00:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2023-04-02T20:00:00Z | 1 | 2023-04-03T00:00:00Z | 2023-04-05T08:00:00Z | 2023-04-12T12:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.7538 | RELAYED -0.8261 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | +1 | 2023-05-06T04:00:00Z | — | — | 2023-05-06T20:00:00Z | 2023-05-10T04:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | +1 | 2023-07-27T08:00:00Z | 0 | 2023-07-27T08:00:00Z | 2023-07-31T16:00:00Z | 2023-08-22T20:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -0.6097 | RELAYED -1.0681 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | +1 | 2023-10-16T08:00:00Z | 0 | 2023-10-16T08:00:00Z | 2024-01-06T04:00:00Z | 2024-04-18T16:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +0.6384 | RELAYED +9.0077 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | +1 | 2024-01-17T12:00:00Z | — | — | 2024-01-19T00:00:00Z | 2024-04-18T16:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | +1 | 2024-02-08T00:00:00Z | 1 | 2024-02-08T04:00:00Z | 2024-02-21T12:00:00Z | 2024-04-18T16:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +0.5237 | RELAYED -0.3044 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2024-04-25T00:00:00Z | 3 | 2024-04-25T12:00:00Z | 2024-05-04T20:00:00Z | 2024-05-18T00:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +1.2210 | RELAYED +1.4371 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | +1 | 2024-06-04T20:00:00Z | 0 | 2024-06-04T20:00:00Z | 2024-06-08T04:00:00Z | 2024-06-14T16:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +0.0976 | RELAYED -1.0292 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2024-07-12T00:00:00Z | 0 | 2024-07-12T00:00:00Z | 2024-07-14T04:00:00Z | 2024-07-19T00:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -1.0316 | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2024-09-16T04:00:00Z | 0 | 2024-09-16T04:00:00Z | 2024-09-19T12:00:00Z | 2024-09-27T00:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -1.0239 | RELAYED -0.8853 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | +1 | 2024-10-07T16:00:00Z | — | — | 2024-10-08T00:00:00Z | 2024-10-11T00:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | +1 | 2024-11-06T04:00:00Z | 0 | 2024-11-06T04:00:00Z | 2024-12-02T08:00:00Z | 2024-12-22T20:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +1.0160 | RELAYED +0.3312 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | +1 | 2025-06-11T00:00:00Z | — | — | 2025-06-13T00:00:00Z | 2025-06-13T16:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | +1 | 2025-08-21T04:00:00Z | — | — | 2025-08-21T20:00:00Z | 2025-10-14T12:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | +1 | 2025-08-22T16:00:00Z | 1 | 2025-08-22T20:00:00Z | 2025-09-22T20:00:00Z | 2025-10-14T12:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.2568 | RELAYED +0.0056 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2025-12-05T20:00:00Z | 1 | 2025-12-06T00:00:00Z | 2025-12-10T08:00:00Z | 2026-01-17T04:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.8296 | RELAYED -0.8652 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2025-12-11T04:00:00Z | 1 | 2025-12-11T08:00:00Z | 2026-01-02T04:00:00Z | 2026-01-17T04:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.1311 | RELAYED +0.5093 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2026-02-27T20:00:00Z | 3 | 2026-02-28T08:00:00Z | 2026-03-02T16:00:00Z | 2026-05-09T20:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.8438 | RELAYED -0.6424 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2026-03-22T12:00:00Z | — | — | 2026-03-24T00:00:00Z | 2026-05-09T20:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2026-04-12T20:00:00Z | 0 | 2026-04-12T20:00:00Z | 2026-04-14T00:00:00Z | 2026-05-09T20:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -1.0419 | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2026-06-19T04:00:00Z | — | — | 2026-06-21T00:00:00Z | 2026-07-07T00:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | +1 | 2026-09-18T04:00:00Z | 0 | 2026-09-18T04:00:00Z | — | — | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +1.4469 | RELAYED +0.5051 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | +1 | 2020-06-22T12:00:00Z | 1 | 2020-06-22T16:00:00Z | 2020-06-28T20:00:00Z | 2020-09-05T16:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +0.4268 | RELAYED -0.4109 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | +1 | 2020-12-07T04:00:00Z | 3 | 2020-12-07T16:00:00Z | 2020-12-09T00:00:00Z | 2020-12-25T16:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.9399 | RELAYED -0.9280 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2020-12-29T08:00:00Z | 3 | 2020-12-29T20:00:00Z | 2021-01-07T12:00:00Z | 2021-01-10T16:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +0.1316 | RELAYED +0.1495 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2021-07-02T12:00:00Z | 2 | 2021-07-02T20:00:00Z | 2021-07-26T04:00:00Z | 2021-08-11T16:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.8322 | RELAYED -0.8731 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2021-12-28T08:00:00Z | 1 | 2021-12-28T12:00:00Z | 2022-02-05T04:00:00Z | 2022-03-11T00:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +0.0118 | RELAYED -0.2160 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | +1 | 2022-04-26T04:00:00Z | 0 | 2022-04-26T04:00:00Z | 2022-04-27T00:00:00Z | 2022-04-28T16:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -1.0313 | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2022-07-11T04:00:00Z | 2 | 2022-07-11T12:00:00Z | 2022-07-16T12:00:00Z | 2022-08-11T00:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +1.1205 | RELAYED +0.9980 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2022-09-06T20:00:00Z | 1 | 2022-09-07T00:00:00Z | 2022-09-09T20:00:00Z | 2023-01-15T20:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.8154 | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2022-09-13T16:00:00Z | 0 | 2022-09-13T16:00:00Z | 2022-09-27T04:00:00Z | 2023-01-15T20:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +0.6957 | RELAYED +0.6884 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2022-09-28T08:00:00Z | 1 | 2022-09-28T12:00:00Z | 2022-10-05T12:00:00Z | 2023-01-15T20:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.0234 | RELAYED -1.0309 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2022-10-06T20:00:00Z | 2 | 2022-10-07T04:00:00Z | 2022-10-25T20:00:00Z | 2023-01-15T20:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +3.1047 | RELAYED +1.7266 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2022-11-07T04:00:00Z | 0 | 2022-11-07T04:00:00Z | 2022-11-23T20:00:00Z | 2023-01-15T20:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -1.0288 | RELAYED +3.0099 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2022-11-28T00:00:00Z | 0 | 2022-11-28T00:00:00Z | 2022-11-30T20:00:00Z | 2023-01-15T20:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -0.6165 | RELAYED -1.0468 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | +1 | 2023-02-02T04:00:00Z | 0 | 2023-02-02T04:00:00Z | 2023-02-05T20:00:00Z | 2023-03-03T08:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -1.0295 | RELAYED -0.8550 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | +1 | 2023-02-08T12:00:00Z | — | — | 2023-02-09T00:00:00Z | 2023-03-03T08:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | +1 | 2023-02-12T16:00:00Z | — | — | 2023-02-13T16:00:00Z | 2023-03-03T08:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | +1 | 2023-02-16T08:00:00Z | — | — | 2023-02-17T16:00:00Z | 2023-03-03T08:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2023-06-23T00:00:00Z | — | — | 2023-06-23T08:00:00Z | 2023-07-04T20:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2023-08-15T04:00:00Z | 2 | 2023-08-15T12:00:00Z | 2023-08-31T04:00:00Z | 2023-10-03T12:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +4.7299 | RELAYED -0.2817 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2023-09-10T08:00:00Z | 2 | 2023-09-10T16:00:00Z | 2023-09-13T20:00:00Z | 2023-10-03T12:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.7947 | RELAYED -1.0240 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2024-04-24T20:00:00Z | 4 | 2024-04-25T12:00:00Z | 2024-05-04T16:00:00Z | 2024-05-26T00:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.0306 | RELAYED +0.2191 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | +1 | 2024-06-04T20:00:00Z | 3 | 2024-06-05T08:00:00Z | 2024-06-08T04:00:00Z | 2024-06-12T04:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.9794 | RELAYED -1.0783 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2024-09-29T00:00:00Z | 1 | 2024-09-29T04:00:00Z | 2024-10-07T08:00:00Z | 2024-10-13T12:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +2.7924 | RELAYED +0.8580 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | +1 | 2024-10-28T04:00:00Z | 2 | 2024-10-28T12:00:00Z | 2024-11-13T20:00:00Z | 2025-01-11T12:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.0214 | RELAYED -0.8593 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2025-01-18T20:00:00Z | 3 | 2025-01-19T08:00:00Z | 2025-02-18T00:00:00Z | 2025-04-03T04:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.0265 | RELAYED -1.0189 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2025-02-18T16:00:00Z | — | — | 2025-02-19T16:00:00Z | 2025-04-03T04:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2025-02-24T16:00:00Z | — | — | 2025-02-27T04:00:00Z | 2025-04-03T04:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2025-04-14T00:00:00Z | 0 | 2025-04-14T00:00:00Z | 2025-04-24T00:00:00Z | 2025-05-06T16:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +0.8287 | RELAYED -0.9824 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2025-04-24T04:00:00Z | — | — | 2025-04-24T12:00:00Z | 2025-05-06T16:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2025-04-28T00:00:00Z | — | — | 2025-04-28T04:00:00Z | 2025-05-06T16:00:00Z | — | MISS_CLOSED_COUNTER_12_89 | NOT ENTERED: no trigger by the window close / as-of | — | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | +1 | 2025-06-10T00:00:00Z | 0 | 2025-06-10T00:00:00Z | 2025-06-12T12:00:00Z | 2025-06-22T08:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -0.9954 | RELAYED -0.8364 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2025-08-12T00:00:00Z | 1 | 2025-08-12T04:00:00Z | 2025-08-13T00:00:00Z | 2025-08-27T08:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -1.0354 | MISS_CLOSED_COUNTER_12_89 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2025-08-15T00:00:00Z | 0 | 2025-08-15T00:00:00Z | 2025-08-21T08:00:00Z | 2025-08-27T08:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -1.0252 | RELAYED +0.3030 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | +1 | 2025-09-02T12:00:00Z | 2 | 2025-09-02T20:00:00Z | 2025-11-22T16:00:00Z | 2025-12-19T04:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +0.8681 | RELAYED +0.5034 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | +1 | 2025-12-24T20:00:00Z | 1 | 2025-12-25T00:00:00Z | 2026-01-08T00:00:00Z | 2026-01-14T00:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +5.1566 | RELAYED +5.2323 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2026-03-26T08:00:00Z | 1 | 2026-03-26T12:00:00Z | 2026-03-31T12:00:00Z | 2026-04-09T04:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | -0.3253 | RELAYED -0.3546 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | +1 | 2026-04-23T20:00:00Z | 0 | 2026-04-23T20:00:00Z | 2026-04-29T20:00:00Z | 2026-06-12T08:00:00Z | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | +0.5087 | RELAYED -1.0308 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | +1 | 2026-04-30T20:00:00Z | 3 | 2026-05-01T08:00:00Z | 2026-05-28T00:00:00Z | 2026-06-12T08:00:00Z | — | MISS_TRIGGER_FIRST | ENTERED | +25.0605 | RELAYED +8.7847 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | +1 | 2026-08-17T08:00:00Z | 0 | 2026-08-17T08:00:00Z | — | — | — | MISS_TRIGGER_FIRST_LAG0 | ENTERED | -1.0542 | RELAYED +31.0438 | TIER-E | a SELECTION, not a result | nothing |

## The FORWARD LEDGER (L-T.6) — both books side by side

From `research_outputs/tierc11/forward/` (scripts/tierc11_forward_ledger.py --refresh): FORWARD_LEDGER.jsonl sha256 e53328add9e71f1c6198f724a131565a2a10ad2ad1600c36a74c6676f7ada288 · FORWARD_LEDGER.md sha256 52e839001f7ad6f1e13533a6d6745488dc587d11db25c3bfe6b0de66823413ec. The ledger's own report follows verbatim from its side-by-side table.

### Both books, side by side

| | base v6 (12/26 trigger) | frozen 9/12 |
|---|---|---|
| definition | tierc11_books.v6_book (TP.run_cell_n) · roles v6-roles | tierc11_books.trg912_book (T9.replay9) · roles trigger-9/12 |
| campaigns ridden to the pin (whole tape) | 200 | 199 |
| book sha (TP._book_sha) at the pin | f3c68f544bcda52c… | 2c32fd60924336ac… |
| appended (closed after the opening) — n | 0 | 0 |
| appended ΣR (net) · Σ haircut R | +0.0000 · +0.0000 | +0.0000 · +0.0000 |
| status | UNSCORED (n 0 < 30) | UNSCORED (n 0 < 30) |
| OPEN at the pin (listed, not appended, not counted) | none | SOLUSDT long entered 2026-09-24T16:00:00Z (bar open) · marked to the pin -0.031452 |
| continuations entered at/before the opening (listed, not counted) | ETHUSDT long entered 2026-09-18T08:00:00Z (bar open) · stop +2.707180 | none |

### Appended campaigns (whole)

| seq | book | asset | dir | entry (bar open) | exit (bar open) | exit_reason | net R | haircut R | era | P-AGE-1 band | refuses | P-WIN-1 lag | refuses | shadow 7-15 | appended at |
|---:|---|---|---:|---|---|---|---:|---:|---|---|---|---:|---|---|---|
| — | (none yet) | | | | | | | | | | | | | | |

### Refreshes

| seq | pin | snapshot | v6 appended now | 9/12 appended now | v6 n | 9/12 n | line sha |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | 2026-09-25T00:00:00Z | tc11_20260925 | 0 | 0 | 0 | 0 | 0db889425ef8e3d2… |

LIMIT (finding, not fixed): the foundation is pinned to the TC11 snapshot and pin; a refresh on bars after 2026-09-25T00:00Z needs the foundation re-rooted on a new snapshot + pin record (operator / foundation work).

## Files

- `stage_t_relay/relay_disposition_grid.parquet` content sha bbb652c3183ddcc0…
- `stage_t_relay/relay_era_slices.parquet` content sha f07c8fc30e2b5e40…
- `stage_t_relay/relay_lead_bins.parquet` content sha 68cedbbd02897576…
- `stage_t_relay/relay_lead_values.parquet` content sha 4c2e2e7bd0d4bf4c…
- `stage_t_relay/relay_windows.parquet` content sha d33b1e65cad84440…
- `regbooks/P-RELAY-1/scored.parquet` + `scored.json` book_sha256 57d8bbef8190492d…
- `regbooks/P-RELAY-1/base.parquet` + `base.json` book_sha256 f41bfaf02b86dfb0…
- `regbooks/P-RELAY-1/tierE__late_relay.parquet` + `tierE__late_relay.json` book_sha256 9e295b903e0c6e37…
- `regbooks/P-RELAY-1/tierE__tuning_slice.parquet` + `tierE__tuning_slice.json` book_sha256 10ac7ec867fab087…
- `regbooks/P-RELAY-1/tierE__holdout_slice.parquet` + `tierE__holdout_slice.json` book_sha256 7e975ad781e3e31f…
- `regbooks/P-RELAY-1/tierE__miss_v6.parquet` + `tierE__miss_v6.json` book_sha256 306b9ceebecb9e51…
- `regbooks/P-RELAY-1/STATUS.json`
- the FORWARD LEDGER of this stage (L-T.6) is `research_outputs/tierc11/forward/FORWARD_LEDGER.jsonl` + `FORWARD_LEDGER.md` (scripts/tierc11_forward_ledger.py); the fixtures are `scripts/tierc11_stage_t_relay_fixtures.py` → `stage_t_relay/FIXTURES_STAGE_T_RELAY.txt`
