as_of_last_closed_4h: 2026-09-25T00:00:00Z

# TIER-C11 · STAGE R · R3 THE NEST ON THE LANES — the nesting grid at entry per lane book [contract R3; L-R.5, AM-6, SR-15] — Tier-E

Collar on every table below unless marked RECORD: tier = 'TIER-E' · selection_not_a_result = 'a SELECTION, not a result' · gates = 'nothing'.

SR-15 THE LANES PASS [contract R3 'at every instant of every campaign of every card (base v6, 9/12, the lanes below)'; L-R.5, AM-6]: `lanes` runs the nest-book door (read_regbook -> instants_of -> nest_frame, both scales) over every REGISTERED scored arm that is a campaign book — P-WARN-1, P-AGE-1, P-WIN-1, P-BRK-4H, P-RELAY-1, P-ADD-BRK, P-ADD-SFP, P-TP-RNG (P-SCALP-2 is closed by R2 and files no book) — plus P-BRK-4H tierE__panel17 (the twelve: 12h / 1w NA, hence 4h / 12h / 1d coincidence NA). Each book must be the book the scorer scored (its sidecar book_sha256 == scores/SCORE_MANIFEST.json's input, HALT otherwise). Named events per L-R.5 / AM-6: arm, entry (the relay's 1h entry close: 'relay_entry'), harvest, add (add1 / add2), bell, a warn exit at its 1h close, a close exit at its close — close events at their close; +1R, a stop and a TP fill are intrabar: at the OPEN of their bar or at the close of the 1h child that resolves them (the regbook's own stamp of record). THE TWIN LAW (one law for every intrabar event — +1R, a stop, a TP fill — every book, the relay included): an intrabar event whose stamp precedes the close of the 4h bar holding it carries exactly one close-stamped twin, labelled post-event, AT that close (a bar-OPEN stamp: the same bar's close; a 1h child's close: its parent 4h bar's close — exit_bar_close_ms for the relay, whose exit_close_ms is its 1h exit instant); a stamp that IS that close (the resolving 1h child is the bar's last) has none — its own instant is the close, a bar_close row through the exit stamp; close events (arm, entry, harvest, add, bell, a warn exit, a close exit) have none — a warn exit before its 4h bar's close ends the campaign there, so that close is not one of its instants. Each row's `stamp_law` names its rule from the event's own class (intrabar vs close), never from its position against exit_close_ms. An intrabar exit resolved by 'close' HALTs. A campaign OPEN at the pin -> 'as_of_pin'. Each row carries `named_event` (the event's name, 'bar_close' for a plain lens close) and the campaign's `exit_reason`. The nesting grid at ENTRY per book x scale x lens (state x coincidence frequency, outcomes by state, outcomes by coincidence: n, E[net R], P(win), sum R, the book's own net_r) is printed whole with SR-12's honesty labels, collared; declared cells: STATES4 (+ 'NA' where a member lacks the lens) x COIN_CATS (+ 'NA' where a member lacks L or L+1; 1w 'NA' only). LANES_MANIFEST.json pins, per book, the regbook bytes it stamped (the parquet's content sha — its csv — and its file sha) beside book_sha256, which covers the 16 required columns only, not the instant columns the nest reads.

SR-6 R3 INSTANTS [L-R.5, AM-6]: every CLOSE of the campaign's own lens from its arm close (entry close for a book without arming) through its exit stamp of record; plus the named events — arm, entry, harvest, bell, add, a close exit at their CLOSE; +1R and an intrabar exit (stop / tp) at the OPEN of their bar for the 4h books (latch bar = latch_1r_open_ms, exit = exit_event_ms: the books' UNWALKED 4h ride) — their close-stamped twins are labelled 'post-event' (instant kinds plus_1r_post_event / exit_post_event); a campaign OPEN at the pin (corridor_end) is stamped 'as_of_pin', never 'exit'. Each row's stamp_law names its rule. The nest is N.nest_at(symbol, instants, scale) — per L read at the last CLOSED bar of L at or before the instant.

SR-7 COINCIDENCE AT ENTRY (NEST_GRID): per lens L the category from L's two side flags — 'both' (coin_top and coin_bot), 'top', 'bot', 'none'; 'NA' for 1w (no lens above). Record rule = the live L+1 boundaries (coin_*); twin = with L+1's live memory lines (coin_*_mem).

SR-9 nest-book [L-R.5]: kinds v6transform (4h bars from the arm), lane4h (4h from the entry), relay (4h bars from the v6 arm — its stop, R, window and ride are 4h; its 1h entry instant is the named event 'entry'), scalp5m (5m bars from the entry). Columns read beyond the REGBOOK INTERFACE: arm = arm_close_ms | window_arm_close_ms | arm_ms + one lens bar (the arm bar's OPEN) | (v6transform) v6's own arm joined on the pairing key (symbol, entry_ms) [L-1.5]; kinds v6transform / relay start their bar closes there (a close event); exit = exit_stamp_ms (ride11's stamp of record) | exit_event_ms (the books' L-R.5 stamp) | a 1h-walked ride's RESOLVED exit instant exit_instant_ms / exit_close_1h_ms, read by exit_resolved_by: '1h' -> the instant as filed (a stop at the close of the 1h child that resolves it, a warn exit at its 1h close), 'close' -> a CLOSE reason as filed at exit_close_ms (an intrabar reason resolved by 'close', or a 'close' exit off exit_close_ms, HALTs), 'parent' -> an intrabar reason at the parent bar's OPEN, a close reason at the parent's close (a missing exit_resolved_by HALTs) [the lanes pass: the warn exit and the add books' exits at their own instant, never the exit bar's 4h close] | derived: an intrabar reason (stop / tp / target) -> the OPEN of the lens bar holding exit_close_ms, a close reason (bell* / corridor_end / warn* / invalidation* / close*) -> exit_close_ms; any other reason HALTs; THE TWIN LAW: an INTRABAR exit stamped before the close of the lens bar holding it (exit_bar_close_ms when filed — the relay, whose exit_close_ms is its 1h exit instant — else exit_close_ms; HALT unless it is that bar's close) carries the close-stamped twin 'exit_post_event' there; a stamp that IS that close (the resolving 1h child is the bar's last) has none, and a close event (a 1h warn exit) has none; a corridor_end campaign (OPEN at the pin) is stamped 'as_of_pin', never 'exit'; +1R = latch_stamp_ms (+ latch_post_event_ms) | latch_1h_ms gated by latched_1h: the resolving 1h child's close, a PARENT-decided latch (latch_1h_by 'parent' | its parent bar listed in walk_mismatch_ms) -> the parent's OPEN, an undecidable latch at a parent close HALTs; its twin by THE TWIN LAW: the close of the lens bar holding latch_1h_ms when after the stamp (the parent's close; the bar's close for a latch resolved before the bar's last 1h child; none when the resolving child is the bar's last) | derived on the lens tape by the bar-OPEN law when reached_1r is True (v6transform / lane4h), its twin at that bar's close | none; harvest = harvest_close_ms | harvest_ms + one lens bar | harvest_i on the lens tape (checked) | (v6transform) v6's own harvest close joined on the pairing key, checked per row against `harvested` and the exit stamp — gated by `harvested`; a close event inside (entry close, exit]; adds / others = add1_close_ms, add2_close_ms (close events; gated by n_adds); ev_<name>_ms (kind <name>, as given); UNSTAMPED = a campaign whose own record says an event happened (latched_1h / reached_1r True, harvested True, n_adds > k) but no source above stamps it is counted, and the door REFUSES to file (HALT naming the counts) [L-R.5 'plus the named events'].

SCALE-IN-SAMPLE [L-R.2, AM-4]: a calibrated-scale range read at an instant <= the era cut (2024-06-30T23:59:59Z) is structurally IN-SAMPLE (the tuning pick saw those bars; a whole-tape fallback pick is in-sample at every instant; frozen 3.0 never is). Every row carries `lenses_read` (the lenses the cell consumes: L, and L+1 for a coincidence cell), their `pick_window` and `stability_changed_members` (first-half-of-tuning pick != tuning pick), `n_scale_in_sample` / `n_stability_changed` (the cell's entries whose read is in-sample / rides a stability-changed pick, on ANY consumed lens), and the HOLDOUT slice (entry close after the cut: n_holdout, mean_net_r_holdout, p_win_holdout, sum_net_r_holdout) — the causal slice of a tuning pick, printed beside every cell.

Stamp laws differ by book and each row's `stamp_law` names its rule: the 4h rides without a 1h walk (P-AGE-1, P-WIN-1, P-BRK-4H, P-TP-RNG; P-WARN-1's +1R) stamp +1R / a stop / a TP fill at the OPEN of their 4h bar; the 1h-walked books (P-RELAY-1, P-ADD-BRK, P-ADD-SFP; P-WARN-1's exits) at the close of the resolving 1h child (a parent-decided event on a walk-mismatch bar at the parent's OPEN) — both lawful under L-R.5. One twin law for all: an intrabar event (+1R, a stop, a TP fill) stamped before the close of its 4h bar carries one post-event twin at that close (the relay's exit bar close = exit_bar_close_ms); a stamp that is itself the 4h close (the bar's last 1h child) carries none; close events carry none.

## The lane books

- **P-WARN-1/scored** (v6transform, lens 4h; 5 assets): n 200 campaigns · 17682 nest rows (both scales) · book_sha256 956e15390419f8ab… (== the scorer's input) · regbook stamped: content 8e7410a68114204e… / file ad7c8ce8d5a8a04b… · instants per scale: arm 200 · bar_close 7909 · entry 200 · exit 200 · exit_post_event 114 · harvest 34 · plus_1r 92 · plus_1r_post_event 92 · named events per scale: +1R 92 · +1R (post-event twin) 92 · arm 200 · entry 200 · exit: stop 158 · exit: stop (post-event twin) 114 · harvest 34 · warn exit 42
  - event sources: arm = arm_ms + 4h (the arm bar's OPEN + one bar); exit = exit_instant_ms by exit_resolved_by ('1h' -> as filed; 'close' -> a close reason as filed at exit_close_ms; 'parent' -> an intrabar reason at the parent bar's OPEN, a close reason at the parent's close) [L-R.5, AM-6]; exit_post_event = THE TWIN LAW: an intrabar exit stamped before the close of the 4h bar holding it -> that close (exit_close_ms); plus_1r = derived: the OPEN of the first 4h bar after the entry whose favourable extreme reaches entry +/- R (reached_1r rows only); plus_1r_post_event = derived: that bar's CLOSE; harvest = v6's own harvest close, joined on (symbol, entry_ms) [L-1.5] — checked per row: harvested -> v6 harvested at or before the exit stamp; not harvested -> v6 did not harvest before it
- **P-AGE-1/scored** (v6transform, lens 4h; 5 assets): n 141 campaigns · 11698 nest rows (both scales) · book_sha256 d008fa5086ce14f5… (== the scorer's input) · regbook stamped: content d8a887403f8b20dc… / file 6440a6e0d14cfbf1… · instants per scale: arm 141 · bar_close 5089 · entry 141 · exit 141 · exit_post_event 141 · harvest 38 · plus_1r 79 · plus_1r_post_event 79 · named events per scale: +1R 79 · +1R (post-event twin) 79 · arm 141 · entry 141 · exit: stop 141 · exit: stop (post-event twin) 141 · harvest 38
  - event sources: arm = arm_ms + 4h (the arm bar's OPEN + one bar); exit = exit_event_ms; exit_post_event = THE TWIN LAW: an intrabar exit stamped before the close of the 4h bar holding it -> that close (exit_close_ms); plus_1r = derived: the OPEN of the first 4h bar after the entry whose favourable extreme reaches entry +/- R (reached_1r rows only); plus_1r_post_event = derived: that bar's CLOSE; harvest = harvest_close_ms
- **P-WIN-1/scored** (v6transform, lens 4h; 5 assets): n 137 campaigns · 7886 nest rows (both scales) · book_sha256 fd3f407ad6b18670… (== the scorer's input) · regbook stamped: content 74759e9744db0490… / file 824c5e08ca79511f… · instants per scale: arm 137 · bar_close 3202 · entry 137 · exit 137 · exit_post_event 137 · harvest 39 · plus_1r 77 · plus_1r_post_event 77 · named events per scale: +1R 77 · +1R (post-event twin) 77 · arm 137 · entry 137 · exit: stop 137 · exit: stop (post-event twin) 137 · harvest 39
  - event sources: arm = arm_ms + 4h (the arm bar's OPEN + one bar); exit = exit_event_ms; exit_post_event = THE TWIN LAW: an intrabar exit stamped before the close of the 4h bar holding it -> that close (exit_close_ms); plus_1r = derived: the OPEN of the first 4h bar after the entry whose favourable extreme reaches entry +/- R (reached_1r rows only); plus_1r_post_event = derived: that bar's CLOSE; harvest = harvest_close_ms
- **P-BRK-4H/scored** (lane4h, lens 4h; 5 assets): n 322 campaigns · 17798 nest rows (both scales) · book_sha256 c76358dfaeb034dd… (== the scorer's input) · regbook stamped: content 4b48e80e84bae8b0… / file b58e678a0a350750… · instants per scale: bar_close 7402 · bell 53 · entry 322 · exit 322 · exit_post_event 269 · harvest 215 · plus_1r 158 · plus_1r_post_event 158 · named events per scale: +1R 158 · +1R (post-event twin) 158 · bell 53 · entry 322 · exit: bell_12_89 53 · exit: stop 269 · exit: stop (post-event twin) 269 · harvest 215
  - event sources: exit = exit_event_ms; exit_post_event = THE TWIN LAW: an intrabar exit stamped before the close of the 4h bar holding it -> that close (exit_close_ms); plus_1r = derived: the OPEN of the first 4h bar after the entry whose favourable extreme reaches entry +/- R (reached_1r rows only); plus_1r_post_event = derived: that bar's CLOSE; harvest = harvest_i on the 4h tape (checked against entry_i)
- **P-BRK-4H/tierE__panel17** (lane4h, lens 4h; 17 assets): n 762 campaigns · 43560 nest rows (both scales) · book_sha256 761922c7fc32f0ef… (== the scorer's input) · regbook stamped: content be2b23e0b06fbb9c… / file 286d9636cba9e6be… · instants per scale: bar_close 18210 · bell 110 · entry 762 · exit 762 · exit_post_event 652 · harvest 520 · plus_1r 382 · plus_1r_post_event 382 · named events per scale: +1R 382 · +1R (post-event twin) 382 · bell 110 · entry 762 · exit: bell_12_89 110 · exit: stop 652 · exit: stop (post-event twin) 652 · harvest 520
  - event sources: exit = exit_event_ms; exit_post_event = THE TWIN LAW: an intrabar exit stamped before the close of the 4h bar holding it -> that close (exit_close_ms); plus_1r = derived: the OPEN of the first 4h bar after the entry whose favourable extreme reaches entry +/- R (reached_1r rows only); plus_1r_post_event = derived: that bar's CLOSE; harvest = harvest_i on the 4h tape (checked against entry_i)
- **P-RELAY-1/scored** (relay, lens 4h; 5 assets): n 173 campaigns · 12296 nest rows (both scales) · book_sha256 57d8bbef8190492d… (== the scorer's input) · regbook stamped: content 9eb15727e863edf7… / file bc6854ec92dd1635… · instants per scale: arm 173 · bar_close 5292 · bell 11 · entry 173 · exit 173 · exit_post_event 114 · harvest 48 · plus_1r 95 · plus_1r_post_event 69 · named events per scale: +1R 95 · +1R (post-event twin) 69 · arm 173 · bell 11 · exit: bell_12_89 11 · exit: stop 162 · exit: stop (post-event twin) 114 · harvest 48 · relay_entry 173
  - event sources: arm = window_arm_close_ms; exit = exit_stamp_ms; exit_post_event = THE TWIN LAW: an intrabar exit stamped before the close of the 4h bar holding it -> that close (exit_bar_close_ms); plus_1r = latch_1h_ms (the resolving 1h child's close; a PARENT-decided latch -> the parent's OPEN, source walk_mismatch_ms); plus_1r_post_event = THE TWIN LAW: the close of the 4h bar holding latch_1h_ms, when after the stamp (a parent-decided latch: the parent's close; a latch resolved before the bar's last 1h child: the bar's close; none when the resolving child is the bar's last); harvest = harvest_close_ms
- **P-ADD-BRK/scored** (v6transform, lens 4h; 5 assets): n 200 campaigns · 19464 nest rows (both scales) · book_sha256 15ba415b7a30f20f… (== the scorer's input) · regbook stamped: content 4c68370ad23000e8… / file 7d44337a45923892… · instants per scale: add1 52 · add2 14 · arm 200 · bar_close 8684 · bell 4 · entry 200 · exit 200 · exit_post_event 144 · harvest 55 · plus_1r 103 · plus_1r_post_event 76 · named events per scale: +1R 103 · +1R (post-event twin) 76 · add 66 · arm 200 · bell 4 · entry 200 · exit: bell_12_89 4 · exit: stop 196 · exit: stop (post-event twin) 144 · harvest 55
  - event sources: arm = v6's own arm, joined on (symbol, entry_ms) [L-1.5]; exit = exit_close_1h_ms by exit_resolved_by ('1h' -> as filed; 'close' -> a close reason as filed at exit_close_ms; 'parent' -> an intrabar reason at the parent bar's OPEN, a close reason at the parent's close) [L-R.5, AM-6]; exit_post_event = THE TWIN LAW: an intrabar exit stamped before the close of the 4h bar holding it -> that close (exit_close_ms); plus_1r = latch_1h_ms (the resolving 1h child's close; a PARENT-decided latch -> the parent's OPEN, source n_walk_mismatch); plus_1r_post_event = THE TWIN LAW: the close of the 4h bar holding latch_1h_ms, when after the stamp (a parent-decided latch: the parent's close; a latch resolved before the bar's last 1h child: the bar's close; none when the resolving child is the bar's last); harvest = v6's own harvest close, joined on (symbol, entry_ms) [L-1.5] — checked per row: harvested -> v6 harvested at or before the exit stamp; not harvested -> v6 did not harvest before it; add1 = add1_close_ms; add2 = add2_close_ms
- **P-ADD-SFP/scored** (v6transform, lens 4h; 5 assets): n 200 campaigns · 19356 nest rows (both scales) · book_sha256 ee2d19250f3e3d74… (== the scorer's input) · regbook stamped: content adc9ea36c04ebbed… / file 739d45d76a9cc240… · instants per scale: add1 9 · add2 3 · arm 200 · bar_close 8684 · bell 4 · entry 200 · exit 200 · exit_post_event 144 · harvest 55 · plus_1r 103 · plus_1r_post_event 76 · named events per scale: +1R 103 · +1R (post-event twin) 76 · add 12 · arm 200 · bell 4 · entry 200 · exit: bell_12_89 4 · exit: stop 196 · exit: stop (post-event twin) 144 · harvest 55
  - event sources: arm = v6's own arm, joined on (symbol, entry_ms) [L-1.5]; exit = exit_close_1h_ms by exit_resolved_by ('1h' -> as filed; 'close' -> a close reason as filed at exit_close_ms; 'parent' -> an intrabar reason at the parent bar's OPEN, a close reason at the parent's close) [L-R.5, AM-6]; exit_post_event = THE TWIN LAW: an intrabar exit stamped before the close of the 4h bar holding it -> that close (exit_close_ms); plus_1r = latch_1h_ms (the resolving 1h child's close; a PARENT-decided latch -> the parent's OPEN, source n_walk_mismatch); plus_1r_post_event = THE TWIN LAW: the close of the 4h bar holding latch_1h_ms, when after the stamp (a parent-decided latch: the parent's close; a latch resolved before the bar's last 1h child: the bar's close; none when the resolving child is the bar's last); harvest = v6's own harvest close, joined on (symbol, entry_ms) [L-1.5] — checked per row: harvested -> v6 harvested at or before the exit stamp; not harvested -> v6 did not harvest before it; add1 = add1_close_ms; add2 = add2_close_ms
- **P-TP-RNG/scored** (v6transform, lens 4h; 5 assets): n 200 campaigns · 17456 nest rows (both scales) · book_sha256 a10c667b26932948… (== the scorer's input) · regbook stamped: content 520b72e66db30b71… / file 4ba47f8b6d41a0e9… · instants per scale: arm 200 · bar_close 7685 · bell 4 · entry 200 · exit 200 · exit_post_event 196 · harvest 53 · plus_1r 95 · plus_1r_post_event 95 · named events per scale: +1R 95 · +1R (post-event twin) 95 · TP fill 36 · TP fill (post-event twin) 36 · arm 200 · bell 4 · entry 200 · exit: bell_12_89 4 · exit: stop 160 · exit: stop (post-event twin) 160 · harvest 53
  - event sources: arm = v6's own arm, joined on (symbol, entry_ms) [L-1.5]; exit = exit_stamp_ms; exit_post_event = THE TWIN LAW: an intrabar exit stamped before the close of the 4h bar holding it -> that close (exit_close_ms); plus_1r = derived: the OPEN of the first 4h bar after the entry whose favourable extreme reaches entry +/- R (reached_1r rows only); plus_1r_post_event = derived: that bar's CLOSE; harvest = harvest_ms + 4h

## The 4h / 12h state at ENTRY per lane (n; calibrated = the scale of record, IN-SAMPLE on tuning-era entries; frozen3.0 = the causal twin)

- P-WARN-1/scored: calibrated 4h NONE 0 / IN_RANGE 141 / BULL_EXP 32 / BEAR_EXP 27 · calibrated 12h NONE 0 / IN_RANGE 103 / BULL_EXP 58 / BEAR_EXP 39 · frozen3.0 4h NONE 0 / IN_RANGE 94 / BULL_EXP 66 / BEAR_EXP 40 · frozen3.0 12h NONE 0 / IN_RANGE 74 / BULL_EXP 76 / BEAR_EXP 50
- P-AGE-1/scored: calibrated 4h NONE 0 / IN_RANGE 102 / BULL_EXP 23 / BEAR_EXP 16 · calibrated 12h NONE 0 / IN_RANGE 77 / BULL_EXP 36 / BEAR_EXP 28 · frozen3.0 4h NONE 0 / IN_RANGE 72 / BULL_EXP 41 / BEAR_EXP 28 · frozen3.0 12h NONE 0 / IN_RANGE 57 / BULL_EXP 50 / BEAR_EXP 34
- P-WIN-1/scored: calibrated 4h NONE 0 / IN_RANGE 103 / BULL_EXP 21 / BEAR_EXP 13 · calibrated 12h NONE 0 / IN_RANGE 72 / BULL_EXP 39 / BEAR_EXP 26 · frozen3.0 4h NONE 0 / IN_RANGE 66 / BULL_EXP 47 / BEAR_EXP 24 · frozen3.0 12h NONE 0 / IN_RANGE 48 / BULL_EXP 53 / BEAR_EXP 36
- P-BRK-4H/scored: calibrated 4h NONE 0 / IN_RANGE 112 / BULL_EXP 103 / BEAR_EXP 107 · calibrated 12h NONE 0 / IN_RANGE 121 / BULL_EXP 119 / BEAR_EXP 82 · frozen3.0 4h NONE 0 / IN_RANGE 56 / BULL_EXP 149 / BEAR_EXP 117 · frozen3.0 12h NONE 0 / IN_RANGE 119 / BULL_EXP 127 / BEAR_EXP 76
- P-BRK-4H/tierE__panel17: calibrated 4h NONE 0 / IN_RANGE 257 / BULL_EXP 262 / BEAR_EXP 243 · calibrated 12h NONE 0 / IN_RANGE 121 / BULL_EXP 119 / BEAR_EXP 82 / NA 440 · frozen3.0 4h NONE 0 / IN_RANGE 148 / BULL_EXP 335 / BEAR_EXP 279 · frozen3.0 12h NONE 0 / IN_RANGE 119 / BULL_EXP 127 / BEAR_EXP 76 / NA 440
- P-RELAY-1/scored: calibrated 4h NONE 0 / IN_RANGE 110 / BULL_EXP 25 / BEAR_EXP 38 · calibrated 12h NONE 0 / IN_RANGE 95 / BULL_EXP 42 / BEAR_EXP 36 · frozen3.0 4h NONE 0 / IN_RANGE 84 / BULL_EXP 46 / BEAR_EXP 43 · frozen3.0 12h NONE 0 / IN_RANGE 64 / BULL_EXP 65 / BEAR_EXP 44
- P-ADD-BRK/scored: calibrated 4h NONE 0 / IN_RANGE 141 / BULL_EXP 32 / BEAR_EXP 27 · calibrated 12h NONE 0 / IN_RANGE 103 / BULL_EXP 58 / BEAR_EXP 39 · frozen3.0 4h NONE 0 / IN_RANGE 94 / BULL_EXP 66 / BEAR_EXP 40 · frozen3.0 12h NONE 0 / IN_RANGE 74 / BULL_EXP 76 / BEAR_EXP 50
- P-ADD-SFP/scored: calibrated 4h NONE 0 / IN_RANGE 141 / BULL_EXP 32 / BEAR_EXP 27 · calibrated 12h NONE 0 / IN_RANGE 103 / BULL_EXP 58 / BEAR_EXP 39 · frozen3.0 4h NONE 0 / IN_RANGE 94 / BULL_EXP 66 / BEAR_EXP 40 · frozen3.0 12h NONE 0 / IN_RANGE 74 / BULL_EXP 76 / BEAR_EXP 50
- P-TP-RNG/scored: calibrated 4h NONE 0 / IN_RANGE 141 / BULL_EXP 32 / BEAR_EXP 27 · calibrated 12h NONE 0 / IN_RANGE 103 / BULL_EXP 58 / BEAR_EXP 39 · frozen3.0 4h NONE 0 / IN_RANGE 94 / BULL_EXP 66 / BEAR_EXP 40 · frozen3.0 12h NONE 0 / IN_RANGE 74 / BULL_EXP 76 / BEAR_EXP 50

### Honesty at ENTRY per (book, scale, lens) [L-R.2, AM-4]

- P-WARN-1/scored · calibrated · 1h: 123 of 200 entries read IN-SAMPLE; 115 on a stability-changed pick (1h: BTCUSDT,SOLUSDT,NEARUSDT); pick window 1h: tuning; holdout slice n 77
- P-WARN-1/scored · calibrated · 4h: 123 of 200 entries read IN-SAMPLE; 40 on a stability-changed pick (4h: NEARUSDT); pick window 4h: tuning; holdout slice n 77
- P-WARN-1/scored · calibrated · 12h: 123 of 200 entries read IN-SAMPLE; 123 on a stability-changed pick (12h: BTCUSDT,ETHUSDT,SOLUSDT); pick window 12h: tuning; holdout slice n 77
- P-WARN-1/scored · calibrated · 1d: 123 of 200 entries read IN-SAMPLE; 75 on a stability-changed pick (1d: BTCUSDT,SOLUSDT); pick window 1d: tuning; holdout slice n 77
- P-WARN-1/scored · calibrated · 1w: 200 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (1w: none); pick window 1w: whole-tape (fallback); holdout slice n 77
- P-WARN-1/scored · frozen3.0 · 1h: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (1h: none); pick window 1h: frozen3.0; holdout slice n 77
- P-WARN-1/scored · frozen3.0 · 4h: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (4h: none); pick window 4h: frozen3.0; holdout slice n 77
- P-WARN-1/scored · frozen3.0 · 12h: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (12h: none); pick window 12h: frozen3.0; holdout slice n 77
- P-WARN-1/scored · frozen3.0 · 1d: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (1d: none); pick window 1d: frozen3.0; holdout slice n 77
- P-WARN-1/scored · frozen3.0 · 1w: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (1w: none); pick window 1w: frozen3.0; holdout slice n 77
- P-AGE-1/scored · calibrated · 1h: 81 of 141 entries read IN-SAMPLE; 81 on a stability-changed pick (1h: BTCUSDT,SOLUSDT,NEARUSDT); pick window 1h: tuning; holdout slice n 60
- P-AGE-1/scored · calibrated · 4h: 81 of 141 entries read IN-SAMPLE; 29 on a stability-changed pick (4h: NEARUSDT); pick window 4h: tuning; holdout slice n 60
- P-AGE-1/scored · calibrated · 12h: 81 of 141 entries read IN-SAMPLE; 83 on a stability-changed pick (12h: BTCUSDT,ETHUSDT,SOLUSDT); pick window 12h: tuning; holdout slice n 60
- P-AGE-1/scored · calibrated · 1d: 81 of 141 entries read IN-SAMPLE; 52 on a stability-changed pick (1d: BTCUSDT,SOLUSDT); pick window 1d: tuning; holdout slice n 60
- P-AGE-1/scored · calibrated · 1w: 141 of 141 entries read IN-SAMPLE; 0 on a stability-changed pick (1w: none); pick window 1w: whole-tape (fallback); holdout slice n 60
- P-AGE-1/scored · frozen3.0 · 1h: 0 of 141 entries read IN-SAMPLE; 0 on a stability-changed pick (1h: none); pick window 1h: frozen3.0; holdout slice n 60
- P-AGE-1/scored · frozen3.0 · 4h: 0 of 141 entries read IN-SAMPLE; 0 on a stability-changed pick (4h: none); pick window 4h: frozen3.0; holdout slice n 60
- P-AGE-1/scored · frozen3.0 · 12h: 0 of 141 entries read IN-SAMPLE; 0 on a stability-changed pick (12h: none); pick window 12h: frozen3.0; holdout slice n 60
- P-AGE-1/scored · frozen3.0 · 1d: 0 of 141 entries read IN-SAMPLE; 0 on a stability-changed pick (1d: none); pick window 1d: frozen3.0; holdout slice n 60
- P-AGE-1/scored · frozen3.0 · 1w: 0 of 141 entries read IN-SAMPLE; 0 on a stability-changed pick (1w: none); pick window 1w: frozen3.0; holdout slice n 60
- P-WIN-1/scored · calibrated · 1h: 81 of 137 entries read IN-SAMPLE; 70 on a stability-changed pick (1h: BTCUSDT,SOLUSDT,NEARUSDT); pick window 1h: tuning; holdout slice n 56
- P-WIN-1/scored · calibrated · 4h: 81 of 137 entries read IN-SAMPLE; 26 on a stability-changed pick (4h: NEARUSDT); pick window 4h: tuning; holdout slice n 56
- P-WIN-1/scored · calibrated · 12h: 81 of 137 entries read IN-SAMPLE; 80 on a stability-changed pick (12h: BTCUSDT,ETHUSDT,SOLUSDT); pick window 12h: tuning; holdout slice n 56
- P-WIN-1/scored · calibrated · 1d: 81 of 137 entries read IN-SAMPLE; 44 on a stability-changed pick (1d: BTCUSDT,SOLUSDT); pick window 1d: tuning; holdout slice n 56
- P-WIN-1/scored · calibrated · 1w: 137 of 137 entries read IN-SAMPLE; 0 on a stability-changed pick (1w: none); pick window 1w: whole-tape (fallback); holdout slice n 56
- P-WIN-1/scored · frozen3.0 · 1h: 0 of 137 entries read IN-SAMPLE; 0 on a stability-changed pick (1h: none); pick window 1h: frozen3.0; holdout slice n 56
- P-WIN-1/scored · frozen3.0 · 4h: 0 of 137 entries read IN-SAMPLE; 0 on a stability-changed pick (4h: none); pick window 4h: frozen3.0; holdout slice n 56
- P-WIN-1/scored · frozen3.0 · 12h: 0 of 137 entries read IN-SAMPLE; 0 on a stability-changed pick (12h: none); pick window 12h: frozen3.0; holdout slice n 56
- P-WIN-1/scored · frozen3.0 · 1d: 0 of 137 entries read IN-SAMPLE; 0 on a stability-changed pick (1d: none); pick window 1d: frozen3.0; holdout slice n 56
- P-WIN-1/scored · frozen3.0 · 1w: 0 of 137 entries read IN-SAMPLE; 0 on a stability-changed pick (1w: none); pick window 1w: frozen3.0; holdout slice n 56
- P-BRK-4H/scored · calibrated · 1h: 210 of 322 entries read IN-SAMPLE; 187 on a stability-changed pick (1h: BTCUSDT,SOLUSDT,NEARUSDT); pick window 1h: tuning; holdout slice n 112
- P-BRK-4H/scored · calibrated · 4h: 210 of 322 entries read IN-SAMPLE; 63 on a stability-changed pick (4h: NEARUSDT); pick window 4h: tuning; holdout slice n 112
- P-BRK-4H/scored · calibrated · 12h: 210 of 322 entries read IN-SAMPLE; 184 on a stability-changed pick (12h: BTCUSDT,ETHUSDT,SOLUSDT); pick window 12h: tuning; holdout slice n 112
- P-BRK-4H/scored · calibrated · 1d: 210 of 322 entries read IN-SAMPLE; 124 on a stability-changed pick (1d: BTCUSDT,SOLUSDT); pick window 1d: tuning; holdout slice n 112
- P-BRK-4H/scored · calibrated · 1w: 322 of 322 entries read IN-SAMPLE; 0 on a stability-changed pick (1w: none); pick window 1w: whole-tape (fallback); holdout slice n 112
- P-BRK-4H/scored · frozen3.0 · 1h: 0 of 322 entries read IN-SAMPLE; 0 on a stability-changed pick (1h: none); pick window 1h: frozen3.0; holdout slice n 112
- P-BRK-4H/scored · frozen3.0 · 4h: 0 of 322 entries read IN-SAMPLE; 0 on a stability-changed pick (4h: none); pick window 4h: frozen3.0; holdout slice n 112
- P-BRK-4H/scored · frozen3.0 · 12h: 0 of 322 entries read IN-SAMPLE; 0 on a stability-changed pick (12h: none); pick window 12h: frozen3.0; holdout slice n 112
- P-BRK-4H/scored · frozen3.0 · 1d: 0 of 322 entries read IN-SAMPLE; 0 on a stability-changed pick (1d: none); pick window 1d: frozen3.0; holdout slice n 112
- P-BRK-4H/scored · frozen3.0 · 1w: 0 of 322 entries read IN-SAMPLE; 0 on a stability-changed pick (1w: none); pick window 1w: frozen3.0; holdout slice n 112
- P-BRK-4H/tierE__panel17 · calibrated · 1h: 454 of 762 entries read IN-SAMPLE; 459 on a stability-changed pick (1h: BTCUSDT,SOLUSDT,NEARUSDT,ENAUSDT,MNTUSDT_BYBIT,SUIUSDT,LTCUSDT,XMRUSDT,BNBUSDT,1000BONKUSDT); pick window 1h: tuning / whole-tape (fallback); holdout slice n 334
- P-BRK-4H/tierE__panel17 · calibrated · 4h: 454 of 762 entries read IN-SAMPLE; 285 on a stability-changed pick (4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT); pick window 4h: tuning / whole-tape (fallback); holdout slice n 334
- P-BRK-4H/tierE__panel17 · calibrated · 12h: 210 of 762 entries read IN-SAMPLE; 184 on a stability-changed pick (12h: BTCUSDT,ETHUSDT,SOLUSDT); pick window 12h: tuning; holdout slice n 334
- P-BRK-4H/tierE__panel17 · calibrated · 1d: 508 of 762 entries read IN-SAMPLE; 313 on a stability-changed pick (1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT); pick window 1d: tuning / whole-tape (fallback); holdout slice n 334
- P-BRK-4H/tierE__panel17 · calibrated · 1w: 322 of 762 entries read IN-SAMPLE; 0 on a stability-changed pick (1w: none); pick window 1w: whole-tape (fallback); holdout slice n 334
- P-BRK-4H/tierE__panel17 · frozen3.0 · 1h: 0 of 762 entries read IN-SAMPLE; 0 on a stability-changed pick (1h: none); pick window 1h: frozen3.0; holdout slice n 334
- P-BRK-4H/tierE__panel17 · frozen3.0 · 4h: 0 of 762 entries read IN-SAMPLE; 0 on a stability-changed pick (4h: none); pick window 4h: frozen3.0; holdout slice n 334
- P-BRK-4H/tierE__panel17 · frozen3.0 · 12h: 0 of 762 entries read IN-SAMPLE; 0 on a stability-changed pick (12h: none); pick window 12h: frozen3.0; holdout slice n 334
- P-BRK-4H/tierE__panel17 · frozen3.0 · 1d: 0 of 762 entries read IN-SAMPLE; 0 on a stability-changed pick (1d: none); pick window 1d: frozen3.0; holdout slice n 334
- P-BRK-4H/tierE__panel17 · frozen3.0 · 1w: 0 of 762 entries read IN-SAMPLE; 0 on a stability-changed pick (1w: none); pick window 1w: frozen3.0; holdout slice n 334
- P-RELAY-1/scored · calibrated · 1h: 114 of 173 entries read IN-SAMPLE; 112 on a stability-changed pick (1h: BTCUSDT,SOLUSDT,NEARUSDT); pick window 1h: tuning; holdout slice n 59
- P-RELAY-1/scored · calibrated · 4h: 114 of 173 entries read IN-SAMPLE; 32 on a stability-changed pick (4h: NEARUSDT); pick window 4h: tuning; holdout slice n 59
- P-RELAY-1/scored · calibrated · 12h: 114 of 173 entries read IN-SAMPLE; 113 on a stability-changed pick (12h: BTCUSDT,ETHUSDT,SOLUSDT); pick window 12h: tuning; holdout slice n 59
- P-RELAY-1/scored · calibrated · 1d: 114 of 173 entries read IN-SAMPLE; 80 on a stability-changed pick (1d: BTCUSDT,SOLUSDT); pick window 1d: tuning; holdout slice n 59
- P-RELAY-1/scored · calibrated · 1w: 173 of 173 entries read IN-SAMPLE; 0 on a stability-changed pick (1w: none); pick window 1w: whole-tape (fallback); holdout slice n 59
- P-RELAY-1/scored · frozen3.0 · 1h: 0 of 173 entries read IN-SAMPLE; 0 on a stability-changed pick (1h: none); pick window 1h: frozen3.0; holdout slice n 59
- P-RELAY-1/scored · frozen3.0 · 4h: 0 of 173 entries read IN-SAMPLE; 0 on a stability-changed pick (4h: none); pick window 4h: frozen3.0; holdout slice n 59
- P-RELAY-1/scored · frozen3.0 · 12h: 0 of 173 entries read IN-SAMPLE; 0 on a stability-changed pick (12h: none); pick window 12h: frozen3.0; holdout slice n 59
- P-RELAY-1/scored · frozen3.0 · 1d: 0 of 173 entries read IN-SAMPLE; 0 on a stability-changed pick (1d: none); pick window 1d: frozen3.0; holdout slice n 59
- P-RELAY-1/scored · frozen3.0 · 1w: 0 of 173 entries read IN-SAMPLE; 0 on a stability-changed pick (1w: none); pick window 1w: frozen3.0; holdout slice n 59
- P-ADD-BRK/scored · calibrated · 1h: 123 of 200 entries read IN-SAMPLE; 115 on a stability-changed pick (1h: BTCUSDT,SOLUSDT,NEARUSDT); pick window 1h: tuning; holdout slice n 77
- P-ADD-BRK/scored · calibrated · 4h: 123 of 200 entries read IN-SAMPLE; 40 on a stability-changed pick (4h: NEARUSDT); pick window 4h: tuning; holdout slice n 77
- P-ADD-BRK/scored · calibrated · 12h: 123 of 200 entries read IN-SAMPLE; 123 on a stability-changed pick (12h: BTCUSDT,ETHUSDT,SOLUSDT); pick window 12h: tuning; holdout slice n 77
- P-ADD-BRK/scored · calibrated · 1d: 123 of 200 entries read IN-SAMPLE; 75 on a stability-changed pick (1d: BTCUSDT,SOLUSDT); pick window 1d: tuning; holdout slice n 77
- P-ADD-BRK/scored · calibrated · 1w: 200 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (1w: none); pick window 1w: whole-tape (fallback); holdout slice n 77
- P-ADD-BRK/scored · frozen3.0 · 1h: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (1h: none); pick window 1h: frozen3.0; holdout slice n 77
- P-ADD-BRK/scored · frozen3.0 · 4h: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (4h: none); pick window 4h: frozen3.0; holdout slice n 77
- P-ADD-BRK/scored · frozen3.0 · 12h: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (12h: none); pick window 12h: frozen3.0; holdout slice n 77
- P-ADD-BRK/scored · frozen3.0 · 1d: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (1d: none); pick window 1d: frozen3.0; holdout slice n 77
- P-ADD-BRK/scored · frozen3.0 · 1w: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (1w: none); pick window 1w: frozen3.0; holdout slice n 77
- P-ADD-SFP/scored · calibrated · 1h: 123 of 200 entries read IN-SAMPLE; 115 on a stability-changed pick (1h: BTCUSDT,SOLUSDT,NEARUSDT); pick window 1h: tuning; holdout slice n 77
- P-ADD-SFP/scored · calibrated · 4h: 123 of 200 entries read IN-SAMPLE; 40 on a stability-changed pick (4h: NEARUSDT); pick window 4h: tuning; holdout slice n 77
- P-ADD-SFP/scored · calibrated · 12h: 123 of 200 entries read IN-SAMPLE; 123 on a stability-changed pick (12h: BTCUSDT,ETHUSDT,SOLUSDT); pick window 12h: tuning; holdout slice n 77
- P-ADD-SFP/scored · calibrated · 1d: 123 of 200 entries read IN-SAMPLE; 75 on a stability-changed pick (1d: BTCUSDT,SOLUSDT); pick window 1d: tuning; holdout slice n 77
- P-ADD-SFP/scored · calibrated · 1w: 200 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (1w: none); pick window 1w: whole-tape (fallback); holdout slice n 77
- P-ADD-SFP/scored · frozen3.0 · 1h: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (1h: none); pick window 1h: frozen3.0; holdout slice n 77
- P-ADD-SFP/scored · frozen3.0 · 4h: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (4h: none); pick window 4h: frozen3.0; holdout slice n 77
- P-ADD-SFP/scored · frozen3.0 · 12h: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (12h: none); pick window 12h: frozen3.0; holdout slice n 77
- P-ADD-SFP/scored · frozen3.0 · 1d: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (1d: none); pick window 1d: frozen3.0; holdout slice n 77
- P-ADD-SFP/scored · frozen3.0 · 1w: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (1w: none); pick window 1w: frozen3.0; holdout slice n 77
- P-TP-RNG/scored · calibrated · 1h: 123 of 200 entries read IN-SAMPLE; 115 on a stability-changed pick (1h: BTCUSDT,SOLUSDT,NEARUSDT); pick window 1h: tuning; holdout slice n 77
- P-TP-RNG/scored · calibrated · 4h: 123 of 200 entries read IN-SAMPLE; 40 on a stability-changed pick (4h: NEARUSDT); pick window 4h: tuning; holdout slice n 77
- P-TP-RNG/scored · calibrated · 12h: 123 of 200 entries read IN-SAMPLE; 123 on a stability-changed pick (12h: BTCUSDT,ETHUSDT,SOLUSDT); pick window 12h: tuning; holdout slice n 77
- P-TP-RNG/scored · calibrated · 1d: 123 of 200 entries read IN-SAMPLE; 75 on a stability-changed pick (1d: BTCUSDT,SOLUSDT); pick window 1d: tuning; holdout slice n 77
- P-TP-RNG/scored · calibrated · 1w: 200 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (1w: none); pick window 1w: whole-tape (fallback); holdout slice n 77
- P-TP-RNG/scored · frozen3.0 · 1h: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (1h: none); pick window 1h: frozen3.0; holdout slice n 77
- P-TP-RNG/scored · frozen3.0 · 4h: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (4h: none); pick window 4h: frozen3.0; holdout slice n 77
- P-TP-RNG/scored · frozen3.0 · 12h: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (12h: none); pick window 12h: frozen3.0; holdout slice n 77
- P-TP-RNG/scored · frozen3.0 · 1d: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (1d: none); pick window 1d: frozen3.0; holdout slice n 77
- P-TP-RNG/scored · frozen3.0 · 1w: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (1w: none); pick window 1w: frozen3.0; holdout slice n 77

### Frequency at ENTRY: state x coincidence, per lens (every lane book, both scales, both coincidence rules) — WHOLE

| book | scale_kind | lens | coin_rule | state | coin_cat | n | n_entries | share | n_scale_in_sample | n_stability_changed | n_holdout | lenses_read | pick_window |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P-WARN-1/scored | calibrated | 1h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | record | IN_RANGE | both | 4 | 200 | 0.0200 | 2 | 2 | 2 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | record | IN_RANGE | top | 9 | 200 | 0.0450 | 4 | 3 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | record | IN_RANGE | bot | 17 | 200 | 0.0850 | 12 | 11 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | record | IN_RANGE | none | 96 | 200 | 0.4800 | 61 | 57 | 35 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | record | BULL_EXP | none | 38 | 200 | 0.1900 | 27 | 23 | 11 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | record | BEAR_EXP | none | 36 | 200 | 0.1800 | 17 | 19 | 19 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | mem_twin | IN_RANGE | both | 4 | 200 | 0.0200 | 2 | 2 | 2 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | mem_twin | IN_RANGE | top | 10 | 200 | 0.0500 | 5 | 4 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | mem_twin | IN_RANGE | bot | 19 | 200 | 0.0950 | 14 | 12 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | mem_twin | IN_RANGE | none | 93 | 200 | 0.4650 | 58 | 55 | 35 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | mem_twin | BULL_EXP | none | 38 | 200 | 0.1900 | 27 | 23 | 11 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 1h | mem_twin | BEAR_EXP | none | 36 | 200 | 0.1800 | 17 | 19 | 19 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WARN-1/scored | calibrated | 4h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | record | IN_RANGE | both | 9 | 200 | 0.0450 | 7 | 8 | 2 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | record | IN_RANGE | top | 8 | 200 | 0.0400 | 1 | 7 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | record | IN_RANGE | bot | 12 | 200 | 0.0600 | 5 | 11 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | record | IN_RANGE | none | 112 | 200 | 0.5600 | 75 | 90 | 37 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | record | BULL_EXP | none | 32 | 200 | 0.1600 | 20 | 25 | 12 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | record | BEAR_EXP | none | 27 | 200 | 0.1350 | 15 | 22 | 12 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | mem_twin | IN_RANGE | both | 9 | 200 | 0.0450 | 7 | 8 | 2 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | mem_twin | IN_RANGE | top | 8 | 200 | 0.0400 | 1 | 7 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | mem_twin | IN_RANGE | bot | 13 | 200 | 0.0650 | 6 | 11 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | mem_twin | IN_RANGE | none | 111 | 200 | 0.5550 | 74 | 90 | 37 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | mem_twin | BULL_EXP | none | 32 | 200 | 0.1600 | 20 | 25 | 12 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 4h | mem_twin | BEAR_EXP | none | 27 | 200 | 0.1350 | 15 | 22 | 12 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WARN-1/scored | calibrated | 12h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | record | IN_RANGE | both | 6 | 200 | 0.0300 | 4 | 3 | 2 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | record | IN_RANGE | top | 4 | 200 | 0.0200 | 1 | 2 | 3 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | record | IN_RANGE | bot | 13 | 200 | 0.0650 | 5 | 8 | 8 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | record | IN_RANGE | none | 80 | 200 | 0.4000 | 44 | 61 | 36 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | record | BULL_EXP | none | 58 | 200 | 0.2900 | 45 | 32 | 13 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | record | BEAR_EXP | none | 39 | 200 | 0.1950 | 24 | 17 | 15 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | mem_twin | IN_RANGE | both | 7 | 200 | 0.0350 | 4 | 4 | 3 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | mem_twin | IN_RANGE | top | 9 | 200 | 0.0450 | 3 | 6 | 6 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | mem_twin | IN_RANGE | bot | 15 | 200 | 0.0750 | 8 | 10 | 7 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | mem_twin | IN_RANGE | none | 72 | 200 | 0.3600 | 39 | 54 | 33 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | mem_twin | BULL_EXP | none | 58 | 200 | 0.2900 | 45 | 32 | 13 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 12h | mem_twin | BEAR_EXP | none | 39 | 200 | 0.1950 | 24 | 17 | 15 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WARN-1/scored | calibrated | 1d | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | record | IN_RANGE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | record | IN_RANGE | top | 1 | 200 | 0.0050 | 1 | 1 | 1 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | record | IN_RANGE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | record | IN_RANGE | none | 72 | 200 | 0.3600 | 72 | 26 | 34 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | record | BULL_EXP | none | 77 | 200 | 0.3850 | 77 | 29 | 18 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | record | BEAR_EXP | none | 50 | 200 | 0.2500 | 50 | 19 | 24 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | mem_twin | IN_RANGE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | mem_twin | IN_RANGE | top | 1 | 200 | 0.0050 | 1 | 1 | 1 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | mem_twin | IN_RANGE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | mem_twin | IN_RANGE | none | 72 | 200 | 0.3600 | 72 | 26 | 34 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | mem_twin | BULL_EXP | none | 77 | 200 | 0.3850 | 77 | 29 | 18 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1d | mem_twin | BEAR_EXP | none | 50 | 200 | 0.2500 | 50 | 19 | 24 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1w | record | NONE | NA | 30 | 200 | 0.1500 | 30 | 0 | 0 | 1w | 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1w | record | IN_RANGE | NA | 43 | 200 | 0.2150 | 43 | 0 | 31 | 1w | 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1w | record | BULL_EXP | NA | 29 | 200 | 0.1450 | 29 | 0 | 19 | 1w | 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1w | record | BEAR_EXP | NA | 98 | 200 | 0.4900 | 98 | 0 | 27 | 1w | 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1w | mem_twin | NONE | NA | 30 | 200 | 0.1500 | 30 | 0 | 0 | 1w | 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1w | mem_twin | IN_RANGE | NA | 43 | 200 | 0.2150 | 43 | 0 | 31 | 1w | 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1w | mem_twin | BULL_EXP | NA | 29 | 200 | 0.1450 | 29 | 0 | 19 | 1w | 1w: whole-tape (fallback) |
| P-WARN-1/scored | calibrated | 1w | mem_twin | BEAR_EXP | NA | 98 | 200 | 0.4900 | 98 | 0 | 27 | 1w | 1w: whole-tape (fallback) |
| P-WARN-1/scored | frozen3.0 | 1h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | record | IN_RANGE | both | 1 | 200 | 0.0050 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | record | IN_RANGE | top | 9 | 200 | 0.0450 | 0 | 0 | 6 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | record | IN_RANGE | bot | 2 | 200 | 0.0100 | 0 | 0 | 1 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | record | IN_RANGE | none | 115 | 200 | 0.5750 | 0 | 0 | 42 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | record | BULL_EXP | none | 41 | 200 | 0.2050 | 0 | 0 | 17 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | record | BEAR_EXP | none | 32 | 200 | 0.1600 | 0 | 0 | 11 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | both | 1 | 200 | 0.0050 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | top | 10 | 200 | 0.0500 | 0 | 0 | 7 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | bot | 2 | 200 | 0.0100 | 0 | 0 | 1 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | none | 114 | 200 | 0.5700 | 0 | 0 | 41 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | none | 41 | 200 | 0.2050 | 0 | 0 | 17 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | none | 32 | 200 | 0.1600 | 0 | 0 | 11 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | record | IN_RANGE | both | 5 | 200 | 0.0250 | 0 | 0 | 1 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | record | IN_RANGE | top | 3 | 200 | 0.0150 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | record | IN_RANGE | bot | 13 | 200 | 0.0650 | 0 | 0 | 10 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | record | IN_RANGE | none | 73 | 200 | 0.3650 | 0 | 0 | 34 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | record | BULL_EXP | none | 66 | 200 | 0.3300 | 0 | 0 | 19 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | record | BEAR_EXP | none | 40 | 200 | 0.2000 | 0 | 0 | 13 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | both | 5 | 200 | 0.0250 | 0 | 0 | 1 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | top | 3 | 200 | 0.0150 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | bot | 13 | 200 | 0.0650 | 0 | 0 | 10 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | none | 73 | 200 | 0.3650 | 0 | 0 | 34 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | none | 66 | 200 | 0.3300 | 0 | 0 | 19 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | none | 40 | 200 | 0.2000 | 0 | 0 | 13 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | record | IN_RANGE | both | 5 | 200 | 0.0250 | 0 | 0 | 3 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | record | IN_RANGE | top | 9 | 200 | 0.0450 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | record | IN_RANGE | bot | 9 | 200 | 0.0450 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | record | IN_RANGE | none | 51 | 200 | 0.2550 | 0 | 0 | 25 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | record | BULL_EXP | none | 76 | 200 | 0.3800 | 0 | 0 | 24 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | record | BEAR_EXP | none | 50 | 200 | 0.2500 | 0 | 0 | 17 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | both | 6 | 200 | 0.0300 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | top | 9 | 200 | 0.0450 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | bot | 8 | 200 | 0.0400 | 0 | 0 | 3 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | none | 51 | 200 | 0.2550 | 0 | 0 | 25 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | none | 76 | 200 | 0.3800 | 0 | 0 | 24 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | none | 50 | 200 | 0.2500 | 0 | 0 | 17 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | record | NONE | none | 4 | 200 | 0.0200 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | record | IN_RANGE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | record | IN_RANGE | top | 2 | 200 | 0.0100 | 0 | 0 | 2 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | record | IN_RANGE | bot | 1 | 200 | 0.0050 | 0 | 0 | 1 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | record | IN_RANGE | none | 55 | 200 | 0.2750 | 0 | 0 | 25 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | record | BULL_EXP | none | 74 | 200 | 0.3700 | 0 | 0 | 19 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | record | BEAR_EXP | none | 64 | 200 | 0.3200 | 0 | 0 | 30 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | mem_twin | NONE | none | 4 | 200 | 0.0200 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | top | 2 | 200 | 0.0100 | 0 | 0 | 2 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | bot | 1 | 200 | 0.0050 | 0 | 0 | 1 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | none | 55 | 200 | 0.2750 | 0 | 0 | 25 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | none | 74 | 200 | 0.3700 | 0 | 0 | 19 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | none | 64 | 200 | 0.3200 | 0 | 0 | 30 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1w | record | NONE | NA | 37 | 200 | 0.1850 | 0 | 0 | 0 | 1w | 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1w | record | IN_RANGE | NA | 29 | 200 | 0.1450 | 0 | 0 | 25 | 1w | 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1w | record | BULL_EXP | NA | 40 | 200 | 0.2000 | 0 | 0 | 20 | 1w | 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1w | record | BEAR_EXP | NA | 94 | 200 | 0.4700 | 0 | 0 | 32 | 1w | 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1w | mem_twin | NONE | NA | 37 | 200 | 0.1850 | 0 | 0 | 0 | 1w | 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1w | mem_twin | IN_RANGE | NA | 29 | 200 | 0.1450 | 0 | 0 | 25 | 1w | 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1w | mem_twin | BULL_EXP | NA | 40 | 200 | 0.2000 | 0 | 0 | 20 | 1w | 1w: frozen3.0 |
| P-WARN-1/scored | frozen3.0 | 1w | mem_twin | BEAR_EXP | NA | 94 | 200 | 0.4700 | 0 | 0 | 32 | 1w | 1w: frozen3.0 |
| P-AGE-1/scored | calibrated | 1h | record | NONE | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | record | NONE | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | record | NONE | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | record | NONE | none | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | record | IN_RANGE | both | 3 | 141 | 0.0213 | 1 | 2 | 2 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | record | IN_RANGE | top | 7 | 141 | 0.0496 | 3 | 2 | 4 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | record | IN_RANGE | bot | 13 | 141 | 0.0922 | 8 | 7 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | record | IN_RANGE | none | 67 | 141 | 0.4752 | 41 | 40 | 26 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | record | BULL_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | record | BULL_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | record | BULL_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | record | BULL_EXP | none | 25 | 141 | 0.1773 | 17 | 16 | 8 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | record | BEAR_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | record | BEAR_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | record | BEAR_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | record | BEAR_EXP | none | 26 | 141 | 0.1844 | 11 | 14 | 15 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | mem_twin | NONE | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | mem_twin | NONE | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | mem_twin | NONE | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | mem_twin | NONE | none | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | mem_twin | IN_RANGE | both | 3 | 141 | 0.0213 | 1 | 2 | 2 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | mem_twin | IN_RANGE | top | 7 | 141 | 0.0496 | 3 | 2 | 4 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | mem_twin | IN_RANGE | bot | 15 | 141 | 0.1064 | 10 | 8 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | mem_twin | IN_RANGE | none | 65 | 141 | 0.4610 | 39 | 39 | 26 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | mem_twin | BULL_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | mem_twin | BULL_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | mem_twin | BULL_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | mem_twin | BULL_EXP | none | 25 | 141 | 0.1773 | 17 | 16 | 8 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | mem_twin | BEAR_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | mem_twin | BEAR_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | mem_twin | BEAR_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 1h | mem_twin | BEAR_EXP | none | 26 | 141 | 0.1844 | 11 | 14 | 15 | 1h+4h | 1h: tuning; 4h: tuning |
| P-AGE-1/scored | calibrated | 4h | record | NONE | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | record | NONE | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | record | NONE | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | record | NONE | none | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | record | IN_RANGE | both | 6 | 141 | 0.0426 | 6 | 5 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | record | IN_RANGE | top | 6 | 141 | 0.0426 | 0 | 5 | 6 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | record | IN_RANGE | bot | 9 | 141 | 0.0638 | 4 | 8 | 5 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | record | IN_RANGE | none | 81 | 141 | 0.5745 | 51 | 64 | 30 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | record | BULL_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | record | BULL_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | record | BULL_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | record | BULL_EXP | none | 23 | 141 | 0.1631 | 13 | 17 | 10 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | record | BEAR_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | record | BEAR_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | record | BEAR_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | record | BEAR_EXP | none | 16 | 141 | 0.1135 | 7 | 13 | 9 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | mem_twin | NONE | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | mem_twin | NONE | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | mem_twin | NONE | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | mem_twin | NONE | none | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | mem_twin | IN_RANGE | both | 6 | 141 | 0.0426 | 6 | 5 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | mem_twin | IN_RANGE | top | 6 | 141 | 0.0426 | 0 | 5 | 6 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | mem_twin | IN_RANGE | bot | 9 | 141 | 0.0638 | 4 | 8 | 5 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | mem_twin | IN_RANGE | none | 81 | 141 | 0.5745 | 51 | 64 | 30 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | mem_twin | BULL_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | mem_twin | BULL_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | mem_twin | BULL_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | mem_twin | BULL_EXP | none | 23 | 141 | 0.1631 | 13 | 17 | 10 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | mem_twin | BEAR_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | mem_twin | BEAR_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | mem_twin | BEAR_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 4h | mem_twin | BEAR_EXP | none | 16 | 141 | 0.1135 | 7 | 13 | 9 | 4h+12h | 4h: tuning; 12h: tuning |
| P-AGE-1/scored | calibrated | 12h | record | NONE | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | record | NONE | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | record | NONE | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | record | NONE | none | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | record | IN_RANGE | both | 6 | 141 | 0.0426 | 4 | 3 | 2 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | record | IN_RANGE | top | 3 | 141 | 0.0213 | 1 | 1 | 2 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | record | IN_RANGE | bot | 10 | 141 | 0.0709 | 3 | 5 | 7 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | record | IN_RANGE | none | 58 | 141 | 0.4113 | 31 | 41 | 27 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | record | BULL_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | record | BULL_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | record | BULL_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | record | BULL_EXP | none | 36 | 141 | 0.2553 | 25 | 18 | 11 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | record | BEAR_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | record | BEAR_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | record | BEAR_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | record | BEAR_EXP | none | 28 | 141 | 0.1986 | 17 | 15 | 11 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | mem_twin | NONE | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | mem_twin | NONE | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | mem_twin | NONE | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | mem_twin | NONE | none | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | mem_twin | IN_RANGE | both | 7 | 141 | 0.0496 | 4 | 4 | 3 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | mem_twin | IN_RANGE | top | 8 | 141 | 0.0567 | 3 | 5 | 5 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | mem_twin | IN_RANGE | bot | 10 | 141 | 0.0709 | 4 | 5 | 6 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | mem_twin | IN_RANGE | none | 52 | 141 | 0.3688 | 28 | 36 | 24 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | mem_twin | BULL_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | mem_twin | BULL_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | mem_twin | BULL_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | mem_twin | BULL_EXP | none | 36 | 141 | 0.2553 | 25 | 18 | 11 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | mem_twin | BEAR_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | mem_twin | BEAR_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | mem_twin | BEAR_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 12h | mem_twin | BEAR_EXP | none | 28 | 141 | 0.1986 | 17 | 15 | 11 | 12h+1d | 12h: tuning; 1d: tuning |
| P-AGE-1/scored | calibrated | 1d | record | NONE | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | record | NONE | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | record | NONE | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | record | NONE | none | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | record | IN_RANGE | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | record | IN_RANGE | top | 1 | 141 | 0.0071 | 1 | 1 | 1 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | record | IN_RANGE | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | record | IN_RANGE | none | 54 | 141 | 0.3830 | 54 | 19 | 28 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | record | BULL_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | record | BULL_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | record | BULL_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | record | BULL_EXP | none | 53 | 141 | 0.3759 | 53 | 18 | 15 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | record | BEAR_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | record | BEAR_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | record | BEAR_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | record | BEAR_EXP | none | 33 | 141 | 0.2340 | 33 | 14 | 16 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | mem_twin | NONE | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | mem_twin | NONE | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | mem_twin | NONE | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | mem_twin | NONE | none | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | mem_twin | IN_RANGE | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | mem_twin | IN_RANGE | top | 1 | 141 | 0.0071 | 1 | 1 | 1 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | mem_twin | IN_RANGE | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | mem_twin | IN_RANGE | none | 54 | 141 | 0.3830 | 54 | 19 | 28 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | mem_twin | BULL_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | mem_twin | BULL_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | mem_twin | BULL_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | mem_twin | BULL_EXP | none | 53 | 141 | 0.3759 | 53 | 18 | 15 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | mem_twin | BEAR_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | mem_twin | BEAR_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | mem_twin | BEAR_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1d | mem_twin | BEAR_EXP | none | 33 | 141 | 0.2340 | 33 | 14 | 16 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1w | record | NONE | NA | 14 | 141 | 0.0993 | 14 | 0 | 0 | 1w | 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1w | record | IN_RANGE | NA | 31 | 141 | 0.2199 | 31 | 0 | 25 | 1w | 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1w | record | BULL_EXP | NA | 19 | 141 | 0.1348 | 19 | 0 | 12 | 1w | 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1w | record | BEAR_EXP | NA | 77 | 141 | 0.5461 | 77 | 0 | 23 | 1w | 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1w | mem_twin | NONE | NA | 14 | 141 | 0.0993 | 14 | 0 | 0 | 1w | 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1w | mem_twin | IN_RANGE | NA | 31 | 141 | 0.2199 | 31 | 0 | 25 | 1w | 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1w | mem_twin | BULL_EXP | NA | 19 | 141 | 0.1348 | 19 | 0 | 12 | 1w | 1w: whole-tape (fallback) |
| P-AGE-1/scored | calibrated | 1w | mem_twin | BEAR_EXP | NA | 77 | 141 | 0.5461 | 77 | 0 | 23 | 1w | 1w: whole-tape (fallback) |
| P-AGE-1/scored | frozen3.0 | 1h | record | NONE | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | record | NONE | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | record | NONE | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | record | NONE | none | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | record | IN_RANGE | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | record | IN_RANGE | top | 9 | 141 | 0.0638 | 0 | 0 | 6 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | record | IN_RANGE | bot | 2 | 141 | 0.0142 | 0 | 0 | 1 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | record | IN_RANGE | none | 82 | 141 | 0.5816 | 0 | 0 | 35 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | record | BULL_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | record | BULL_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | record | BULL_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | record | BULL_EXP | none | 23 | 141 | 0.1631 | 0 | 0 | 10 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | record | BEAR_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | record | BEAR_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | record | BEAR_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | record | BEAR_EXP | none | 25 | 141 | 0.1773 | 0 | 0 | 8 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | mem_twin | NONE | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | mem_twin | NONE | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | mem_twin | NONE | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | mem_twin | NONE | none | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | top | 10 | 141 | 0.0709 | 0 | 0 | 7 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | bot | 2 | 141 | 0.0142 | 0 | 0 | 1 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | none | 81 | 141 | 0.5745 | 0 | 0 | 34 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | none | 23 | 141 | 0.1631 | 0 | 0 | 10 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | none | 25 | 141 | 0.1773 | 0 | 0 | 8 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | record | NONE | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | record | NONE | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | record | NONE | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | record | NONE | none | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | record | IN_RANGE | both | 5 | 141 | 0.0355 | 0 | 0 | 1 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | record | IN_RANGE | top | 2 | 141 | 0.0142 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | record | IN_RANGE | bot | 11 | 141 | 0.0780 | 0 | 0 | 8 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | record | IN_RANGE | none | 54 | 141 | 0.3830 | 0 | 0 | 30 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | record | BULL_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | record | BULL_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | record | BULL_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | record | BULL_EXP | none | 41 | 141 | 0.2908 | 0 | 0 | 13 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | record | BEAR_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | record | BEAR_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | record | BEAR_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | record | BEAR_EXP | none | 28 | 141 | 0.1986 | 0 | 0 | 8 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | mem_twin | NONE | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | mem_twin | NONE | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | mem_twin | NONE | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | mem_twin | NONE | none | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | both | 5 | 141 | 0.0355 | 0 | 0 | 1 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | top | 2 | 141 | 0.0142 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | bot | 11 | 141 | 0.0780 | 0 | 0 | 8 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | none | 54 | 141 | 0.3830 | 0 | 0 | 30 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | none | 41 | 141 | 0.2908 | 0 | 0 | 13 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | none | 28 | 141 | 0.1986 | 0 | 0 | 8 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | record | NONE | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | record | NONE | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | record | NONE | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | record | NONE | none | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | record | IN_RANGE | both | 4 | 141 | 0.0284 | 0 | 0 | 3 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | record | IN_RANGE | top | 8 | 141 | 0.0567 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | record | IN_RANGE | bot | 6 | 141 | 0.0426 | 0 | 0 | 3 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | record | IN_RANGE | none | 39 | 141 | 0.2766 | 0 | 0 | 19 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | record | BULL_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | record | BULL_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | record | BULL_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | record | BULL_EXP | none | 50 | 141 | 0.3546 | 0 | 0 | 20 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | record | BEAR_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | record | BEAR_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | record | BEAR_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | record | BEAR_EXP | none | 34 | 141 | 0.2411 | 0 | 0 | 11 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | mem_twin | NONE | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | mem_twin | NONE | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | mem_twin | NONE | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | mem_twin | NONE | none | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | both | 5 | 141 | 0.0355 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | top | 8 | 141 | 0.0567 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | bot | 5 | 141 | 0.0355 | 0 | 0 | 2 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | none | 39 | 141 | 0.2766 | 0 | 0 | 19 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | none | 50 | 141 | 0.3546 | 0 | 0 | 20 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | none | 34 | 141 | 0.2411 | 0 | 0 | 11 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | record | NONE | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | record | NONE | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | record | NONE | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | record | NONE | none | 2 | 141 | 0.0142 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | record | IN_RANGE | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | record | IN_RANGE | top | 1 | 141 | 0.0071 | 0 | 0 | 1 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | record | IN_RANGE | bot | 1 | 141 | 0.0071 | 0 | 0 | 1 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | record | IN_RANGE | none | 45 | 141 | 0.3191 | 0 | 0 | 24 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | record | BULL_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | record | BULL_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | record | BULL_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | record | BULL_EXP | none | 48 | 141 | 0.3404 | 0 | 0 | 13 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | record | BEAR_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | record | BEAR_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | record | BEAR_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | record | BEAR_EXP | none | 44 | 141 | 0.3121 | 0 | 0 | 21 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | mem_twin | NONE | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | mem_twin | NONE | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | mem_twin | NONE | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | mem_twin | NONE | none | 2 | 141 | 0.0142 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | top | 1 | 141 | 0.0071 | 0 | 0 | 1 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | bot | 1 | 141 | 0.0071 | 0 | 0 | 1 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | none | 45 | 141 | 0.3191 | 0 | 0 | 24 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | none | 48 | 141 | 0.3404 | 0 | 0 | 13 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | both | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | top | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | bot | 0 | 141 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | none | 44 | 141 | 0.3121 | 0 | 0 | 21 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1w | record | NONE | NA | 21 | 141 | 0.1489 | 0 | 0 | 0 | 1w | 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1w | record | IN_RANGE | NA | 21 | 141 | 0.1489 | 0 | 0 | 19 | 1w | 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1w | record | BULL_EXP | NA | 27 | 141 | 0.1915 | 0 | 0 | 13 | 1w | 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1w | record | BEAR_EXP | NA | 72 | 141 | 0.5106 | 0 | 0 | 28 | 1w | 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1w | mem_twin | NONE | NA | 21 | 141 | 0.1489 | 0 | 0 | 0 | 1w | 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1w | mem_twin | IN_RANGE | NA | 21 | 141 | 0.1489 | 0 | 0 | 19 | 1w | 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1w | mem_twin | BULL_EXP | NA | 27 | 141 | 0.1915 | 0 | 0 | 13 | 1w | 1w: frozen3.0 |
| P-AGE-1/scored | frozen3.0 | 1w | mem_twin | BEAR_EXP | NA | 72 | 141 | 0.5106 | 0 | 0 | 28 | 1w | 1w: frozen3.0 |
| P-WIN-1/scored | calibrated | 1h | record | NONE | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | record | NONE | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | record | NONE | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | record | NONE | none | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | record | IN_RANGE | both | 3 | 137 | 0.0219 | 2 | 1 | 1 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | record | IN_RANGE | top | 6 | 137 | 0.0438 | 2 | 1 | 4 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | record | IN_RANGE | bot | 12 | 137 | 0.0876 | 7 | 6 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | record | IN_RANGE | none | 62 | 137 | 0.4526 | 40 | 33 | 22 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | record | BULL_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | record | BULL_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | record | BULL_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | record | BULL_EXP | none | 27 | 137 | 0.1971 | 19 | 15 | 8 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | record | BEAR_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | record | BEAR_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | record | BEAR_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | record | BEAR_EXP | none | 27 | 137 | 0.1971 | 11 | 14 | 16 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | mem_twin | NONE | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | mem_twin | NONE | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | mem_twin | NONE | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | mem_twin | NONE | none | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | mem_twin | IN_RANGE | both | 3 | 137 | 0.0219 | 2 | 1 | 1 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | mem_twin | IN_RANGE | top | 6 | 137 | 0.0438 | 2 | 1 | 4 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | mem_twin | IN_RANGE | bot | 13 | 137 | 0.0949 | 8 | 6 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | mem_twin | IN_RANGE | none | 61 | 137 | 0.4453 | 39 | 33 | 22 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | mem_twin | BULL_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | mem_twin | BULL_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | mem_twin | BULL_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | mem_twin | BULL_EXP | none | 27 | 137 | 0.1971 | 19 | 15 | 8 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | mem_twin | BEAR_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | mem_twin | BEAR_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | mem_twin | BEAR_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 1h | mem_twin | BEAR_EXP | none | 27 | 137 | 0.1971 | 11 | 14 | 16 | 1h+4h | 1h: tuning; 4h: tuning |
| P-WIN-1/scored | calibrated | 4h | record | NONE | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | record | NONE | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | record | NONE | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | record | NONE | none | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | record | IN_RANGE | both | 7 | 137 | 0.0511 | 6 | 6 | 1 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | record | IN_RANGE | top | 5 | 137 | 0.0365 | 0 | 5 | 5 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | record | IN_RANGE | bot | 9 | 137 | 0.0657 | 5 | 9 | 4 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | record | IN_RANGE | none | 82 | 137 | 0.5985 | 51 | 63 | 31 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | record | BULL_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | record | BULL_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | record | BULL_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | record | BULL_EXP | none | 21 | 137 | 0.1533 | 13 | 15 | 8 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | record | BEAR_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | record | BEAR_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | record | BEAR_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | record | BEAR_EXP | none | 13 | 137 | 0.0949 | 6 | 8 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | mem_twin | NONE | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | mem_twin | NONE | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | mem_twin | NONE | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | mem_twin | NONE | none | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | mem_twin | IN_RANGE | both | 7 | 137 | 0.0511 | 6 | 6 | 1 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | mem_twin | IN_RANGE | top | 5 | 137 | 0.0365 | 0 | 5 | 5 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | mem_twin | IN_RANGE | bot | 9 | 137 | 0.0657 | 5 | 9 | 4 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | mem_twin | IN_RANGE | none | 82 | 137 | 0.5985 | 51 | 63 | 31 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | mem_twin | BULL_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | mem_twin | BULL_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | mem_twin | BULL_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | mem_twin | BULL_EXP | none | 21 | 137 | 0.1533 | 13 | 15 | 8 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | mem_twin | BEAR_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | mem_twin | BEAR_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | mem_twin | BEAR_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 4h | mem_twin | BEAR_EXP | none | 13 | 137 | 0.0949 | 6 | 8 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| P-WIN-1/scored | calibrated | 12h | record | NONE | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | record | NONE | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | record | NONE | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | record | NONE | none | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | record | IN_RANGE | both | 4 | 137 | 0.0292 | 3 | 1 | 1 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | record | IN_RANGE | top | 2 | 137 | 0.0146 | 1 | 1 | 1 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | record | IN_RANGE | bot | 9 | 137 | 0.0657 | 3 | 4 | 6 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | record | IN_RANGE | none | 57 | 137 | 0.4161 | 29 | 41 | 28 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | record | BULL_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | record | BULL_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | record | BULL_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | record | BULL_EXP | none | 39 | 137 | 0.2847 | 29 | 22 | 10 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | record | BEAR_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | record | BEAR_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | record | BEAR_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | record | BEAR_EXP | none | 26 | 137 | 0.1898 | 16 | 11 | 10 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | mem_twin | NONE | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | mem_twin | NONE | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | mem_twin | NONE | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | mem_twin | NONE | none | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | mem_twin | IN_RANGE | both | 4 | 137 | 0.0292 | 3 | 1 | 1 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | mem_twin | IN_RANGE | top | 5 | 137 | 0.0365 | 2 | 3 | 3 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | mem_twin | IN_RANGE | bot | 10 | 137 | 0.0730 | 4 | 5 | 6 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | mem_twin | IN_RANGE | none | 53 | 137 | 0.3869 | 27 | 38 | 26 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | mem_twin | BULL_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | mem_twin | BULL_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | mem_twin | BULL_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | mem_twin | BULL_EXP | none | 39 | 137 | 0.2847 | 29 | 22 | 10 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | mem_twin | BEAR_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | mem_twin | BEAR_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | mem_twin | BEAR_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 12h | mem_twin | BEAR_EXP | none | 26 | 137 | 0.1898 | 16 | 11 | 10 | 12h+1d | 12h: tuning; 1d: tuning |
| P-WIN-1/scored | calibrated | 1d | record | NONE | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | record | NONE | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | record | NONE | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | record | NONE | none | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | record | IN_RANGE | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | record | IN_RANGE | top | 1 | 137 | 0.0073 | 1 | 1 | 1 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | record | IN_RANGE | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | record | IN_RANGE | none | 45 | 137 | 0.3285 | 45 | 12 | 23 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | record | BULL_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | record | BULL_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | record | BULL_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | record | BULL_EXP | none | 57 | 137 | 0.4161 | 57 | 19 | 14 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | record | BEAR_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | record | BEAR_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | record | BEAR_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | record | BEAR_EXP | none | 34 | 137 | 0.2482 | 34 | 12 | 18 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | mem_twin | NONE | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | mem_twin | NONE | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | mem_twin | NONE | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | mem_twin | NONE | none | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | mem_twin | IN_RANGE | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | mem_twin | IN_RANGE | top | 1 | 137 | 0.0073 | 1 | 1 | 1 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | mem_twin | IN_RANGE | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | mem_twin | IN_RANGE | none | 45 | 137 | 0.3285 | 45 | 12 | 23 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | mem_twin | BULL_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | mem_twin | BULL_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | mem_twin | BULL_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | mem_twin | BULL_EXP | none | 57 | 137 | 0.4161 | 57 | 19 | 14 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | mem_twin | BEAR_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | mem_twin | BEAR_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | mem_twin | BEAR_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1d | mem_twin | BEAR_EXP | none | 34 | 137 | 0.2482 | 34 | 12 | 18 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1w | record | NONE | NA | 21 | 137 | 0.1533 | 21 | 0 | 0 | 1w | 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1w | record | IN_RANGE | NA | 30 | 137 | 0.2190 | 30 | 0 | 24 | 1w | 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1w | record | BULL_EXP | NA | 19 | 137 | 0.1387 | 19 | 0 | 13 | 1w | 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1w | record | BEAR_EXP | NA | 67 | 137 | 0.4891 | 67 | 0 | 19 | 1w | 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1w | mem_twin | NONE | NA | 21 | 137 | 0.1533 | 21 | 0 | 0 | 1w | 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1w | mem_twin | IN_RANGE | NA | 30 | 137 | 0.2190 | 30 | 0 | 24 | 1w | 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1w | mem_twin | BULL_EXP | NA | 19 | 137 | 0.1387 | 19 | 0 | 13 | 1w | 1w: whole-tape (fallback) |
| P-WIN-1/scored | calibrated | 1w | mem_twin | BEAR_EXP | NA | 67 | 137 | 0.4891 | 67 | 0 | 19 | 1w | 1w: whole-tape (fallback) |
| P-WIN-1/scored | frozen3.0 | 1h | record | NONE | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | record | NONE | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | record | NONE | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | record | NONE | none | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | record | IN_RANGE | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | record | IN_RANGE | top | 6 | 137 | 0.0438 | 0 | 0 | 5 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | record | IN_RANGE | bot | 2 | 137 | 0.0146 | 0 | 0 | 1 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | record | IN_RANGE | none | 89 | 137 | 0.6496 | 0 | 0 | 34 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | record | BULL_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | record | BULL_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | record | BULL_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | record | BULL_EXP | none | 23 | 137 | 0.1679 | 0 | 0 | 10 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | record | BEAR_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | record | BEAR_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | record | BEAR_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | record | BEAR_EXP | none | 17 | 137 | 0.1241 | 0 | 0 | 6 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | mem_twin | NONE | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | mem_twin | NONE | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | mem_twin | NONE | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | mem_twin | NONE | none | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | top | 7 | 137 | 0.0511 | 0 | 0 | 6 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | bot | 2 | 137 | 0.0146 | 0 | 0 | 1 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | none | 88 | 137 | 0.6423 | 0 | 0 | 33 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | none | 23 | 137 | 0.1679 | 0 | 0 | 10 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | none | 17 | 137 | 0.1241 | 0 | 0 | 6 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | record | NONE | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | record | NONE | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | record | NONE | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | record | NONE | none | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | record | IN_RANGE | both | 4 | 137 | 0.0292 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | record | IN_RANGE | top | 2 | 137 | 0.0146 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | record | IN_RANGE | bot | 10 | 137 | 0.0730 | 0 | 0 | 7 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | record | IN_RANGE | none | 50 | 137 | 0.3650 | 0 | 0 | 28 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | record | BULL_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | record | BULL_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | record | BULL_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | record | BULL_EXP | none | 47 | 137 | 0.3431 | 0 | 0 | 14 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | record | BEAR_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | record | BEAR_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | record | BEAR_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | record | BEAR_EXP | none | 24 | 137 | 0.1752 | 0 | 0 | 7 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | mem_twin | NONE | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | mem_twin | NONE | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | mem_twin | NONE | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | mem_twin | NONE | none | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | both | 4 | 137 | 0.0292 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | top | 2 | 137 | 0.0146 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | bot | 10 | 137 | 0.0730 | 0 | 0 | 7 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | none | 50 | 137 | 0.3650 | 0 | 0 | 28 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | none | 47 | 137 | 0.3431 | 0 | 0 | 14 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | none | 24 | 137 | 0.1752 | 0 | 0 | 7 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | record | NONE | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | record | NONE | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | record | NONE | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | record | NONE | none | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | record | IN_RANGE | both | 3 | 137 | 0.0219 | 0 | 0 | 2 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | record | IN_RANGE | top | 4 | 137 | 0.0292 | 0 | 0 | 1 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | record | IN_RANGE | bot | 6 | 137 | 0.0438 | 0 | 0 | 3 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | record | IN_RANGE | none | 35 | 137 | 0.2555 | 0 | 0 | 18 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | record | BULL_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | record | BULL_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | record | BULL_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | record | BULL_EXP | none | 53 | 137 | 0.3869 | 0 | 0 | 19 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | record | BEAR_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | record | BEAR_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | record | BEAR_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | record | BEAR_EXP | none | 36 | 137 | 0.2628 | 0 | 0 | 13 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | mem_twin | NONE | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | mem_twin | NONE | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | mem_twin | NONE | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | mem_twin | NONE | none | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | both | 3 | 137 | 0.0219 | 0 | 0 | 2 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | top | 4 | 137 | 0.0292 | 0 | 0 | 1 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | bot | 6 | 137 | 0.0438 | 0 | 0 | 3 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | none | 35 | 137 | 0.2555 | 0 | 0 | 18 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | none | 53 | 137 | 0.3869 | 0 | 0 | 19 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | none | 36 | 137 | 0.2628 | 0 | 0 | 13 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | record | NONE | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | record | NONE | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | record | NONE | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | record | NONE | none | 3 | 137 | 0.0219 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | record | IN_RANGE | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | record | IN_RANGE | top | 2 | 137 | 0.0146 | 0 | 0 | 2 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | record | IN_RANGE | bot | 1 | 137 | 0.0073 | 0 | 0 | 1 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | record | IN_RANGE | none | 37 | 137 | 0.2701 | 0 | 0 | 19 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | record | BULL_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | record | BULL_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | record | BULL_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | record | BULL_EXP | none | 47 | 137 | 0.3431 | 0 | 0 | 12 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | record | BEAR_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | record | BEAR_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | record | BEAR_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | record | BEAR_EXP | none | 47 | 137 | 0.3431 | 0 | 0 | 22 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | mem_twin | NONE | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | mem_twin | NONE | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | mem_twin | NONE | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | mem_twin | NONE | none | 3 | 137 | 0.0219 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | top | 2 | 137 | 0.0146 | 0 | 0 | 2 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | bot | 1 | 137 | 0.0073 | 0 | 0 | 1 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | none | 37 | 137 | 0.2701 | 0 | 0 | 19 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | none | 47 | 137 | 0.3431 | 0 | 0 | 12 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | both | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | top | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | bot | 0 | 137 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | none | 47 | 137 | 0.3431 | 0 | 0 | 22 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1w | record | NONE | NA | 24 | 137 | 0.1752 | 0 | 0 | 0 | 1w | 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1w | record | IN_RANGE | NA | 21 | 137 | 0.1533 | 0 | 0 | 18 | 1w | 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1w | record | BULL_EXP | NA | 24 | 137 | 0.1752 | 0 | 0 | 14 | 1w | 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1w | record | BEAR_EXP | NA | 68 | 137 | 0.4964 | 0 | 0 | 24 | 1w | 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1w | mem_twin | NONE | NA | 24 | 137 | 0.1752 | 0 | 0 | 0 | 1w | 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1w | mem_twin | IN_RANGE | NA | 21 | 137 | 0.1533 | 0 | 0 | 18 | 1w | 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1w | mem_twin | BULL_EXP | NA | 24 | 137 | 0.1752 | 0 | 0 | 14 | 1w | 1w: frozen3.0 |
| P-WIN-1/scored | frozen3.0 | 1w | mem_twin | BEAR_EXP | NA | 68 | 137 | 0.4964 | 0 | 0 | 24 | 1w | 1w: frozen3.0 |
| P-BRK-4H/scored | calibrated | 1h | record | NONE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | record | NONE | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | record | NONE | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | record | NONE | none | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | record | IN_RANGE | both | 5 | 322 | 0.0155 | 3 | 3 | 2 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | record | IN_RANGE | top | 14 | 322 | 0.0435 | 9 | 8 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | record | IN_RANGE | bot | 10 | 322 | 0.0311 | 8 | 6 | 2 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | record | IN_RANGE | none | 116 | 322 | 0.3602 | 77 | 67 | 39 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | record | BULL_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | record | BULL_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | record | BULL_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | record | BULL_EXP | none | 95 | 322 | 0.2950 | 60 | 53 | 35 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | record | BEAR_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | record | BEAR_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | record | BEAR_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | record | BEAR_EXP | none | 82 | 322 | 0.2547 | 53 | 50 | 29 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | mem_twin | NONE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | mem_twin | NONE | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | mem_twin | NONE | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | mem_twin | NONE | none | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | mem_twin | IN_RANGE | both | 5 | 322 | 0.0155 | 3 | 3 | 2 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | mem_twin | IN_RANGE | top | 16 | 322 | 0.0497 | 11 | 9 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | mem_twin | IN_RANGE | bot | 11 | 322 | 0.0342 | 9 | 7 | 2 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | mem_twin | IN_RANGE | none | 113 | 322 | 0.3509 | 74 | 65 | 39 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | mem_twin | BULL_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | mem_twin | BULL_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | mem_twin | BULL_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | mem_twin | BULL_EXP | none | 95 | 322 | 0.2950 | 60 | 53 | 35 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | mem_twin | BEAR_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | mem_twin | BEAR_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | mem_twin | BEAR_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 1h | mem_twin | BEAR_EXP | none | 82 | 322 | 0.2547 | 53 | 50 | 29 | 1h+4h | 1h: tuning; 4h: tuning |
| P-BRK-4H/scored | calibrated | 4h | record | NONE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | record | NONE | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | record | NONE | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | record | NONE | none | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | record | IN_RANGE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | record | IN_RANGE | top | 6 | 322 | 0.0186 | 5 | 5 | 1 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | record | IN_RANGE | bot | 6 | 322 | 0.0186 | 3 | 2 | 3 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | record | IN_RANGE | none | 100 | 322 | 0.3106 | 69 | 83 | 31 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | record | BULL_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | record | BULL_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | record | BULL_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | record | BULL_EXP | none | 103 | 322 | 0.3199 | 64 | 78 | 39 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | record | BEAR_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | record | BEAR_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | record | BEAR_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | record | BEAR_EXP | none | 107 | 322 | 0.3323 | 69 | 79 | 38 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | mem_twin | NONE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | mem_twin | NONE | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | mem_twin | NONE | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | mem_twin | NONE | none | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | mem_twin | IN_RANGE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | mem_twin | IN_RANGE | top | 7 | 322 | 0.0217 | 5 | 6 | 2 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | mem_twin | IN_RANGE | bot | 6 | 322 | 0.0186 | 3 | 2 | 3 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | mem_twin | IN_RANGE | none | 99 | 322 | 0.3075 | 69 | 82 | 30 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | mem_twin | BULL_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | mem_twin | BULL_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | mem_twin | BULL_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | mem_twin | BULL_EXP | none | 103 | 322 | 0.3199 | 64 | 78 | 39 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | mem_twin | BEAR_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | mem_twin | BEAR_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | mem_twin | BEAR_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 4h | mem_twin | BEAR_EXP | none | 107 | 322 | 0.3323 | 69 | 79 | 38 | 4h+12h | 4h: tuning; 12h: tuning |
| P-BRK-4H/scored | calibrated | 12h | record | NONE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | record | NONE | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | record | NONE | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | record | NONE | none | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | record | IN_RANGE | both | 15 | 322 | 0.0466 | 11 | 8 | 4 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | record | IN_RANGE | top | 13 | 322 | 0.0404 | 7 | 8 | 6 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | record | IN_RANGE | bot | 16 | 322 | 0.0497 | 6 | 9 | 10 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | record | IN_RANGE | none | 77 | 322 | 0.2391 | 50 | 49 | 27 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | record | BULL_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | record | BULL_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | record | BULL_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | record | BULL_EXP | none | 119 | 322 | 0.3696 | 86 | 71 | 33 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | record | BEAR_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | record | BEAR_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | record | BEAR_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | record | BEAR_EXP | none | 82 | 322 | 0.2547 | 50 | 39 | 32 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | mem_twin | NONE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | mem_twin | NONE | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | mem_twin | NONE | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | mem_twin | NONE | none | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | mem_twin | IN_RANGE | both | 18 | 322 | 0.0559 | 11 | 11 | 7 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | mem_twin | IN_RANGE | top | 19 | 322 | 0.0590 | 10 | 13 | 9 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | mem_twin | IN_RANGE | bot | 21 | 322 | 0.0652 | 13 | 13 | 8 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | mem_twin | IN_RANGE | none | 63 | 322 | 0.1957 | 40 | 37 | 23 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | mem_twin | BULL_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | mem_twin | BULL_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | mem_twin | BULL_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | mem_twin | BULL_EXP | none | 119 | 322 | 0.3696 | 86 | 71 | 33 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | mem_twin | BEAR_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | mem_twin | BEAR_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | mem_twin | BEAR_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 12h | mem_twin | BEAR_EXP | none | 82 | 322 | 0.2547 | 50 | 39 | 32 | 12h+1d | 12h: tuning; 1d: tuning |
| P-BRK-4H/scored | calibrated | 1d | record | NONE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | record | NONE | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | record | NONE | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | record | NONE | none | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | record | IN_RANGE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | record | IN_RANGE | top | 1 | 322 | 0.0031 | 1 | 1 | 1 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | record | IN_RANGE | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | record | IN_RANGE | none | 101 | 322 | 0.3137 | 101 | 37 | 45 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | record | BULL_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | record | BULL_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | record | BULL_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | record | BULL_EXP | none | 141 | 322 | 0.4379 | 141 | 55 | 35 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | record | BEAR_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | record | BEAR_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | record | BEAR_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | record | BEAR_EXP | none | 79 | 322 | 0.2453 | 79 | 31 | 31 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | mem_twin | NONE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | mem_twin | NONE | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | mem_twin | NONE | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | mem_twin | NONE | none | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | mem_twin | IN_RANGE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | mem_twin | IN_RANGE | top | 1 | 322 | 0.0031 | 1 | 1 | 1 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | mem_twin | IN_RANGE | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | mem_twin | IN_RANGE | none | 101 | 322 | 0.3137 | 101 | 37 | 45 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | mem_twin | BULL_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | mem_twin | BULL_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | mem_twin | BULL_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | mem_twin | BULL_EXP | none | 141 | 322 | 0.4379 | 141 | 55 | 35 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | mem_twin | BEAR_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | mem_twin | BEAR_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | mem_twin | BEAR_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1d | mem_twin | BEAR_EXP | none | 79 | 322 | 0.2453 | 79 | 31 | 31 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1w | record | NONE | NA | 43 | 322 | 0.1335 | 43 | 0 | 0 | 1w | 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1w | record | IN_RANGE | NA | 74 | 322 | 0.2298 | 74 | 0 | 45 | 1w | 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1w | record | BULL_EXP | NA | 45 | 322 | 0.1398 | 45 | 0 | 30 | 1w | 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1w | record | BEAR_EXP | NA | 160 | 322 | 0.4969 | 160 | 0 | 37 | 1w | 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1w | mem_twin | NONE | NA | 43 | 322 | 0.1335 | 43 | 0 | 0 | 1w | 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1w | mem_twin | IN_RANGE | NA | 74 | 322 | 0.2298 | 74 | 0 | 45 | 1w | 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1w | mem_twin | BULL_EXP | NA | 45 | 322 | 0.1398 | 45 | 0 | 30 | 1w | 1w: whole-tape (fallback) |
| P-BRK-4H/scored | calibrated | 1w | mem_twin | BEAR_EXP | NA | 160 | 322 | 0.4969 | 160 | 0 | 37 | 1w | 1w: whole-tape (fallback) |
| P-BRK-4H/scored | frozen3.0 | 1h | record | NONE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | record | NONE | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | record | NONE | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | record | NONE | none | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | record | IN_RANGE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | record | IN_RANGE | top | 3 | 322 | 0.0093 | 0 | 0 | 1 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | record | IN_RANGE | bot | 3 | 322 | 0.0093 | 0 | 0 | 2 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | record | IN_RANGE | none | 131 | 322 | 0.4068 | 0 | 0 | 39 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | record | BULL_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | record | BULL_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | record | BULL_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | record | BULL_EXP | none | 105 | 322 | 0.3261 | 0 | 0 | 39 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | record | BEAR_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | record | BEAR_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | record | BEAR_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | record | BEAR_EXP | none | 80 | 322 | 0.2484 | 0 | 0 | 31 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | mem_twin | NONE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | mem_twin | NONE | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | mem_twin | NONE | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | mem_twin | NONE | none | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | top | 3 | 322 | 0.0093 | 0 | 0 | 1 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | bot | 3 | 322 | 0.0093 | 0 | 0 | 2 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | none | 131 | 322 | 0.4068 | 0 | 0 | 39 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | none | 105 | 322 | 0.3261 | 0 | 0 | 39 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | none | 80 | 322 | 0.2484 | 0 | 0 | 31 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | record | NONE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | record | NONE | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | record | NONE | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | record | NONE | none | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | record | IN_RANGE | both | 4 | 322 | 0.0124 | 0 | 0 | 2 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | record | IN_RANGE | top | 1 | 322 | 0.0031 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | record | IN_RANGE | bot | 9 | 322 | 0.0280 | 0 | 0 | 9 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | record | IN_RANGE | none | 42 | 322 | 0.1304 | 0 | 0 | 12 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | record | BULL_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | record | BULL_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | record | BULL_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | record | BULL_EXP | none | 149 | 322 | 0.4627 | 0 | 0 | 48 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | record | BEAR_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | record | BEAR_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | record | BEAR_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | record | BEAR_EXP | none | 117 | 322 | 0.3634 | 0 | 0 | 41 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | mem_twin | NONE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | mem_twin | NONE | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | mem_twin | NONE | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | mem_twin | NONE | none | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | both | 4 | 322 | 0.0124 | 0 | 0 | 2 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | top | 1 | 322 | 0.0031 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | bot | 9 | 322 | 0.0280 | 0 | 0 | 9 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | none | 42 | 322 | 0.1304 | 0 | 0 | 12 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | none | 149 | 322 | 0.4627 | 0 | 0 | 48 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | none | 117 | 322 | 0.3634 | 0 | 0 | 41 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | record | NONE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | record | NONE | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | record | NONE | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | record | NONE | none | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | record | IN_RANGE | both | 10 | 322 | 0.0311 | 0 | 0 | 5 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | record | IN_RANGE | top | 23 | 322 | 0.0714 | 0 | 0 | 8 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | record | IN_RANGE | bot | 25 | 322 | 0.0776 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | record | IN_RANGE | none | 61 | 322 | 0.1894 | 0 | 0 | 23 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | record | BULL_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | record | BULL_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | record | BULL_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | record | BULL_EXP | none | 127 | 322 | 0.3944 | 0 | 0 | 45 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | record | BEAR_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | record | BEAR_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | record | BEAR_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | record | BEAR_EXP | none | 76 | 322 | 0.2360 | 0 | 0 | 27 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | mem_twin | NONE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | mem_twin | NONE | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | mem_twin | NONE | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | mem_twin | NONE | none | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | both | 13 | 322 | 0.0404 | 0 | 0 | 8 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | top | 26 | 322 | 0.0807 | 0 | 0 | 10 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | bot | 24 | 322 | 0.0745 | 0 | 0 | 2 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | none | 56 | 322 | 0.1739 | 0 | 0 | 20 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | none | 127 | 322 | 0.3944 | 0 | 0 | 45 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | none | 76 | 322 | 0.2360 | 0 | 0 | 27 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | record | NONE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | record | NONE | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | record | NONE | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | record | NONE | none | 6 | 322 | 0.0186 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | record | IN_RANGE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | record | IN_RANGE | top | 2 | 322 | 0.0062 | 0 | 0 | 2 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | record | IN_RANGE | bot | 2 | 322 | 0.0062 | 0 | 0 | 2 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | record | IN_RANGE | none | 118 | 322 | 0.3665 | 0 | 0 | 44 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | record | BULL_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | record | BULL_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | record | BULL_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | record | BULL_EXP | none | 111 | 322 | 0.3447 | 0 | 0 | 30 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | record | BEAR_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | record | BEAR_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | record | BEAR_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | record | BEAR_EXP | none | 83 | 322 | 0.2578 | 0 | 0 | 34 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | mem_twin | NONE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | mem_twin | NONE | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | mem_twin | NONE | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | mem_twin | NONE | none | 6 | 322 | 0.0186 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | top | 2 | 322 | 0.0062 | 0 | 0 | 2 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | bot | 2 | 322 | 0.0062 | 0 | 0 | 2 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | none | 118 | 322 | 0.3665 | 0 | 0 | 44 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | none | 111 | 322 | 0.3447 | 0 | 0 | 30 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | both | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | top | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | bot | 0 | 322 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | none | 83 | 322 | 0.2578 | 0 | 0 | 34 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1w | record | NONE | NA | 52 | 322 | 0.1615 | 0 | 0 | 0 | 1w | 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1w | record | IN_RANGE | NA | 45 | 322 | 0.1398 | 0 | 0 | 35 | 1w | 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1w | record | BULL_EXP | NA | 64 | 322 | 0.1988 | 0 | 0 | 30 | 1w | 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1w | record | BEAR_EXP | NA | 161 | 322 | 0.5000 | 0 | 0 | 47 | 1w | 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1w | mem_twin | NONE | NA | 52 | 322 | 0.1615 | 0 | 0 | 0 | 1w | 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1w | mem_twin | IN_RANGE | NA | 45 | 322 | 0.1398 | 0 | 0 | 35 | 1w | 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1w | mem_twin | BULL_EXP | NA | 64 | 322 | 0.1988 | 0 | 0 | 30 | 1w | 1w: frozen3.0 |
| P-BRK-4H/scored | frozen3.0 | 1w | mem_twin | BEAR_EXP | NA | 161 | 322 | 0.5000 | 0 | 0 | 47 | 1w | 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | record | NONE | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | record | NONE | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | record | NONE | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | record | NONE | none | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | record | IN_RANGE | both | 11 | 762 | 0.0144 | 7 | 9 | 4 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | record | IN_RANGE | top | 26 | 762 | 0.0341 | 16 | 19 | 11 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | record | IN_RANGE | bot | 24 | 762 | 0.0315 | 18 | 20 | 6 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | record | IN_RANGE | none | 283 | 762 | 0.3714 | 168 | 226 | 123 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | record | BULL_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | record | BULL_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | record | BULL_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | record | BULL_EXP | none | 212 | 762 | 0.2782 | 120 | 159 | 103 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | record | BEAR_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | record | BEAR_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | record | BEAR_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | record | BEAR_EXP | none | 206 | 762 | 0.2703 | 125 | 168 | 87 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | mem_twin | NONE | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | mem_twin | NONE | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | mem_twin | NONE | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | mem_twin | NONE | none | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | mem_twin | IN_RANGE | both | 11 | 762 | 0.0144 | 7 | 9 | 4 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | mem_twin | IN_RANGE | top | 28 | 762 | 0.0367 | 18 | 20 | 11 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | mem_twin | IN_RANGE | bot | 27 | 762 | 0.0354 | 20 | 23 | 7 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | mem_twin | IN_RANGE | none | 278 | 762 | 0.3648 | 164 | 222 | 122 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | mem_twin | BULL_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | mem_twin | BULL_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | mem_twin | BULL_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | mem_twin | BULL_EXP | none | 212 | 762 | 0.2782 | 120 | 159 | 103 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | mem_twin | BEAR_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | mem_twin | BEAR_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | mem_twin | BEAR_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | mem_twin | BEAR_EXP | none | 206 | 762 | 0.2703 | 125 | 168 | 87 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | NONE | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | NONE | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | NONE | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | NONE | none | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | NONE | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | IN_RANGE | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | IN_RANGE | top | 6 | 762 | 0.0079 | 5 | 5 | 1 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | IN_RANGE | bot | 6 | 762 | 0.0079 | 3 | 2 | 3 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | IN_RANGE | none | 100 | 762 | 0.1312 | 69 | 83 | 31 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | IN_RANGE | NA | 145 | 762 | 0.1903 | 91 | 87 | 59 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | BULL_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | BULL_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | BULL_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | BULL_EXP | none | 103 | 762 | 0.1352 | 64 | 78 | 39 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | BULL_EXP | NA | 159 | 762 | 0.2087 | 89 | 73 | 78 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | BEAR_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | BEAR_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | BEAR_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | BEAR_EXP | none | 107 | 762 | 0.1404 | 69 | 79 | 38 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | BEAR_EXP | NA | 136 | 762 | 0.1785 | 64 | 62 | 85 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | NONE | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | NONE | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | NONE | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | NONE | none | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | NONE | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | IN_RANGE | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | IN_RANGE | top | 7 | 762 | 0.0092 | 5 | 6 | 2 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | IN_RANGE | bot | 6 | 762 | 0.0079 | 3 | 2 | 3 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | IN_RANGE | none | 99 | 762 | 0.1299 | 69 | 82 | 30 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | IN_RANGE | NA | 145 | 762 | 0.1903 | 91 | 87 | 59 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | BULL_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | BULL_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | BULL_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | BULL_EXP | none | 103 | 762 | 0.1352 | 64 | 78 | 39 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | BULL_EXP | NA | 159 | 762 | 0.2087 | 89 | 73 | 78 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | BEAR_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | BEAR_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | BEAR_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | BEAR_EXP | none | 107 | 762 | 0.1404 | 69 | 79 | 38 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | BEAR_EXP | NA | 136 | 762 | 0.1785 | 64 | 62 | 85 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | NONE | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | NONE | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | NONE | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | NONE | none | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | NONE | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | IN_RANGE | both | 15 | 762 | 0.0197 | 11 | 8 | 4 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | IN_RANGE | top | 13 | 762 | 0.0171 | 7 | 8 | 6 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | IN_RANGE | bot | 16 | 762 | 0.0210 | 6 | 9 | 10 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | IN_RANGE | none | 77 | 762 | 0.1010 | 50 | 49 | 27 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | IN_RANGE | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | BULL_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | BULL_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | BULL_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | BULL_EXP | none | 119 | 762 | 0.1562 | 86 | 71 | 33 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | BULL_EXP | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | BEAR_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | BEAR_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | BEAR_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | BEAR_EXP | none | 82 | 762 | 0.1076 | 50 | 39 | 32 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | BEAR_EXP | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | NA | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | NA | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | NA | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | NA | none | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | NA | NA | 440 | 762 | 0.5774 | 298 | 189 | 222 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | NONE | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | NONE | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | NONE | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | NONE | none | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | NONE | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | IN_RANGE | both | 18 | 762 | 0.0236 | 11 | 11 | 7 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | IN_RANGE | top | 19 | 762 | 0.0249 | 10 | 13 | 9 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | IN_RANGE | bot | 21 | 762 | 0.0276 | 13 | 13 | 8 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | IN_RANGE | none | 63 | 762 | 0.0827 | 40 | 37 | 23 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | IN_RANGE | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | BULL_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | BULL_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | BULL_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | BULL_EXP | none | 119 | 762 | 0.1562 | 86 | 71 | 33 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | BULL_EXP | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | BEAR_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | BEAR_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | BEAR_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | BEAR_EXP | none | 82 | 762 | 0.1076 | 50 | 39 | 32 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | BEAR_EXP | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | NA | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | NA | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | NA | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | NA | none | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | NA | NA | 440 | 762 | 0.5774 | 298 | 189 | 222 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | NONE | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | NONE | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | NONE | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | NONE | none | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | NONE | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | IN_RANGE | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | IN_RANGE | top | 1 | 762 | 0.0013 | 1 | 1 | 1 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | IN_RANGE | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | IN_RANGE | none | 101 | 762 | 0.1325 | 101 | 37 | 45 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | IN_RANGE | NA | 180 | 762 | 0.2362 | 126 | 77 | 84 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | BULL_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | BULL_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | BULL_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | BULL_EXP | none | 141 | 762 | 0.1850 | 141 | 55 | 35 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | BULL_EXP | NA | 135 | 762 | 0.1772 | 92 | 66 | 64 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | BEAR_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | BEAR_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | BEAR_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | BEAR_EXP | none | 79 | 762 | 0.1037 | 79 | 31 | 31 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | BEAR_EXP | NA | 125 | 762 | 0.1640 | 80 | 46 | 74 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | NONE | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | NONE | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | NONE | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | NONE | none | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | NONE | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | IN_RANGE | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | IN_RANGE | top | 1 | 762 | 0.0013 | 1 | 1 | 1 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | IN_RANGE | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | IN_RANGE | none | 101 | 762 | 0.1325 | 101 | 37 | 45 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | IN_RANGE | NA | 180 | 762 | 0.2362 | 126 | 77 | 84 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | BULL_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | BULL_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | BULL_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | BULL_EXP | none | 141 | 762 | 0.1850 | 141 | 55 | 35 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | BULL_EXP | NA | 135 | 762 | 0.1772 | 92 | 66 | 64 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | BEAR_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | BEAR_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | BEAR_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | BEAR_EXP | none | 79 | 762 | 0.1037 | 79 | 31 | 31 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | BEAR_EXP | NA | 125 | 762 | 0.1640 | 80 | 46 | 74 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1w | record | NONE | NA | 43 | 762 | 0.0564 | 43 | 0 | 0 | 1w | 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1w | record | IN_RANGE | NA | 74 | 762 | 0.0971 | 74 | 0 | 45 | 1w | 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1w | record | BULL_EXP | NA | 45 | 762 | 0.0591 | 45 | 0 | 30 | 1w | 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1w | record | BEAR_EXP | NA | 160 | 762 | 0.2100 | 160 | 0 | 37 | 1w | 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1w | record | NA | NA | 440 | 762 | 0.5774 | 0 | 0 | 222 | 1w | 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1w | mem_twin | NONE | NA | 43 | 762 | 0.0564 | 43 | 0 | 0 | 1w | 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1w | mem_twin | IN_RANGE | NA | 74 | 762 | 0.0971 | 74 | 0 | 45 | 1w | 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1w | mem_twin | BULL_EXP | NA | 45 | 762 | 0.0591 | 45 | 0 | 30 | 1w | 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1w | mem_twin | BEAR_EXP | NA | 160 | 762 | 0.2100 | 160 | 0 | 37 | 1w | 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | calibrated | 1w | mem_twin | NA | NA | 440 | 762 | 0.5774 | 0 | 0 | 222 | 1w | 1w: whole-tape (fallback) |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | record | NONE | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | record | NONE | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | record | NONE | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | record | NONE | none | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | record | IN_RANGE | both | 1 | 762 | 0.0013 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | record | IN_RANGE | top | 8 | 762 | 0.0105 | 0 | 0 | 5 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | record | IN_RANGE | bot | 9 | 762 | 0.0118 | 0 | 0 | 3 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | record | IN_RANGE | none | 287 | 762 | 0.3766 | 0 | 0 | 108 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | record | BULL_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | record | BULL_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | record | BULL_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | record | BULL_EXP | none | 259 | 762 | 0.3399 | 0 | 0 | 124 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | record | BEAR_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | record | BEAR_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | record | BEAR_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | record | BEAR_EXP | none | 198 | 762 | 0.2598 | 0 | 0 | 94 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | mem_twin | NONE | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | mem_twin | NONE | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | mem_twin | NONE | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | mem_twin | NONE | none | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | mem_twin | IN_RANGE | both | 1 | 762 | 0.0013 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | mem_twin | IN_RANGE | top | 8 | 762 | 0.0105 | 0 | 0 | 5 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | mem_twin | IN_RANGE | bot | 10 | 762 | 0.0131 | 0 | 0 | 3 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | mem_twin | IN_RANGE | none | 286 | 762 | 0.3753 | 0 | 0 | 108 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | mem_twin | BULL_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | mem_twin | BULL_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | mem_twin | BULL_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | mem_twin | BULL_EXP | none | 259 | 762 | 0.3399 | 0 | 0 | 124 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | mem_twin | BEAR_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | mem_twin | BEAR_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | mem_twin | BEAR_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | mem_twin | BEAR_EXP | none | 198 | 762 | 0.2598 | 0 | 0 | 94 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | NONE | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | NONE | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | NONE | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | NONE | none | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | NONE | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | IN_RANGE | both | 4 | 762 | 0.0052 | 0 | 0 | 2 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | IN_RANGE | top | 1 | 762 | 0.0013 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | IN_RANGE | bot | 9 | 762 | 0.0118 | 0 | 0 | 9 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | IN_RANGE | none | 42 | 762 | 0.0551 | 0 | 0 | 12 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | IN_RANGE | NA | 92 | 762 | 0.1207 | 0 | 0 | 36 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | BULL_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | BULL_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | BULL_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | BULL_EXP | none | 149 | 762 | 0.1955 | 0 | 0 | 48 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | BULL_EXP | NA | 186 | 762 | 0.2441 | 0 | 0 | 88 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | BEAR_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | BEAR_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | BEAR_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | BEAR_EXP | none | 117 | 762 | 0.1535 | 0 | 0 | 41 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | BEAR_EXP | NA | 162 | 762 | 0.2126 | 0 | 0 | 98 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | NONE | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | NONE | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | NONE | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | NONE | none | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | NONE | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | IN_RANGE | both | 4 | 762 | 0.0052 | 0 | 0 | 2 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | IN_RANGE | top | 1 | 762 | 0.0013 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | IN_RANGE | bot | 9 | 762 | 0.0118 | 0 | 0 | 9 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | IN_RANGE | none | 42 | 762 | 0.0551 | 0 | 0 | 12 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | IN_RANGE | NA | 92 | 762 | 0.1207 | 0 | 0 | 36 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | BULL_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | BULL_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | BULL_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | BULL_EXP | none | 149 | 762 | 0.1955 | 0 | 0 | 48 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | BULL_EXP | NA | 186 | 762 | 0.2441 | 0 | 0 | 88 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | BEAR_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | BEAR_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | BEAR_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | BEAR_EXP | none | 117 | 762 | 0.1535 | 0 | 0 | 41 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | BEAR_EXP | NA | 162 | 762 | 0.2126 | 0 | 0 | 98 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | NONE | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | NONE | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | NONE | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | NONE | none | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | NONE | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | IN_RANGE | both | 10 | 762 | 0.0131 | 0 | 0 | 5 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | IN_RANGE | top | 23 | 762 | 0.0302 | 0 | 0 | 8 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | IN_RANGE | bot | 25 | 762 | 0.0328 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | IN_RANGE | none | 61 | 762 | 0.0801 | 0 | 0 | 23 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | IN_RANGE | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | BULL_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | BULL_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | BULL_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | BULL_EXP | none | 127 | 762 | 0.1667 | 0 | 0 | 45 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | BULL_EXP | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | BEAR_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | BEAR_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | BEAR_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | BEAR_EXP | none | 76 | 762 | 0.0997 | 0 | 0 | 27 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | BEAR_EXP | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | NA | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | NA | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | NA | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | NA | none | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | NA | NA | 440 | 762 | 0.5774 | 0 | 0 | 222 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | NONE | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | NONE | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | NONE | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | NONE | none | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | NONE | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | IN_RANGE | both | 13 | 762 | 0.0171 | 0 | 0 | 8 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | IN_RANGE | top | 26 | 762 | 0.0341 | 0 | 0 | 10 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | IN_RANGE | bot | 24 | 762 | 0.0315 | 0 | 0 | 2 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | IN_RANGE | none | 56 | 762 | 0.0735 | 0 | 0 | 20 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | IN_RANGE | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | BULL_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | BULL_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | BULL_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | BULL_EXP | none | 127 | 762 | 0.1667 | 0 | 0 | 45 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | BULL_EXP | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | BEAR_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | BEAR_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | BEAR_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | BEAR_EXP | none | 76 | 762 | 0.0997 | 0 | 0 | 27 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | BEAR_EXP | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | NA | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | NA | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | NA | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | NA | none | 0 | 762 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | NA | NA | 440 | 762 | 0.5774 | 0 | 0 | 222 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | NONE | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | NONE | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | NONE | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | NONE | none | 6 | 762 | 0.0079 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | NONE | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | IN_RANGE | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | IN_RANGE | top | 2 | 762 | 0.0026 | 0 | 0 | 2 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | IN_RANGE | bot | 2 | 762 | 0.0026 | 0 | 0 | 2 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | IN_RANGE | none | 118 | 762 | 0.1549 | 0 | 0 | 44 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | IN_RANGE | NA | 154 | 762 | 0.2021 | 0 | 0 | 84 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | BULL_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | BULL_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | BULL_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | BULL_EXP | none | 111 | 762 | 0.1457 | 0 | 0 | 30 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | BULL_EXP | NA | 136 | 762 | 0.1785 | 0 | 0 | 68 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | BEAR_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | BEAR_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | BEAR_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | BEAR_EXP | none | 83 | 762 | 0.1089 | 0 | 0 | 34 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | BEAR_EXP | NA | 150 | 762 | 0.1969 | 0 | 0 | 70 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | NONE | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | NONE | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | NONE | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | NONE | none | 6 | 762 | 0.0079 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | NONE | NA | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | IN_RANGE | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | IN_RANGE | top | 2 | 762 | 0.0026 | 0 | 0 | 2 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | IN_RANGE | bot | 2 | 762 | 0.0026 | 0 | 0 | 2 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | IN_RANGE | none | 118 | 762 | 0.1549 | 0 | 0 | 44 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | IN_RANGE | NA | 154 | 762 | 0.2021 | 0 | 0 | 84 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | BULL_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | BULL_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | BULL_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | BULL_EXP | none | 111 | 762 | 0.1457 | 0 | 0 | 30 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | BULL_EXP | NA | 136 | 762 | 0.1785 | 0 | 0 | 68 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | BEAR_EXP | both | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | BEAR_EXP | top | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | BEAR_EXP | bot | 0 | 762 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | BEAR_EXP | none | 83 | 762 | 0.1089 | 0 | 0 | 34 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | BEAR_EXP | NA | 150 | 762 | 0.1969 | 0 | 0 | 70 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1w | record | NONE | NA | 52 | 762 | 0.0682 | 0 | 0 | 0 | 1w | 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1w | record | IN_RANGE | NA | 45 | 762 | 0.0591 | 0 | 0 | 35 | 1w | 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1w | record | BULL_EXP | NA | 64 | 762 | 0.0840 | 0 | 0 | 30 | 1w | 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1w | record | BEAR_EXP | NA | 161 | 762 | 0.2113 | 0 | 0 | 47 | 1w | 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1w | record | NA | NA | 440 | 762 | 0.5774 | 0 | 0 | 222 | 1w | 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1w | mem_twin | NONE | NA | 52 | 762 | 0.0682 | 0 | 0 | 0 | 1w | 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1w | mem_twin | IN_RANGE | NA | 45 | 762 | 0.0591 | 0 | 0 | 35 | 1w | 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1w | mem_twin | BULL_EXP | NA | 64 | 762 | 0.0840 | 0 | 0 | 30 | 1w | 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1w | mem_twin | BEAR_EXP | NA | 161 | 762 | 0.2113 | 0 | 0 | 47 | 1w | 1w: frozen3.0 |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1w | mem_twin | NA | NA | 440 | 762 | 0.5774 | 0 | 0 | 222 | 1w | 1w: frozen3.0 |
| P-RELAY-1/scored | calibrated | 1h | record | NONE | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | record | NONE | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | record | NONE | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | record | NONE | none | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | record | IN_RANGE | both | 1 | 173 | 0.0058 | 1 | 1 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | record | IN_RANGE | top | 3 | 173 | 0.0173 | 2 | 2 | 1 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | record | IN_RANGE | bot | 9 | 173 | 0.0520 | 7 | 8 | 2 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | record | IN_RANGE | none | 63 | 173 | 0.3642 | 45 | 38 | 18 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | record | BULL_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | record | BULL_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | record | BULL_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | record | BULL_EXP | none | 52 | 173 | 0.3006 | 34 | 31 | 18 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | record | BEAR_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | record | BEAR_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | record | BEAR_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | record | BEAR_EXP | none | 45 | 173 | 0.2601 | 25 | 32 | 20 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | mem_twin | NONE | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | mem_twin | NONE | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | mem_twin | NONE | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | mem_twin | NONE | none | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | mem_twin | IN_RANGE | both | 1 | 173 | 0.0058 | 1 | 1 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | mem_twin | IN_RANGE | top | 3 | 173 | 0.0173 | 2 | 2 | 1 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | mem_twin | IN_RANGE | bot | 10 | 173 | 0.0578 | 8 | 9 | 2 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | mem_twin | IN_RANGE | none | 62 | 173 | 0.3584 | 44 | 37 | 18 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | mem_twin | BULL_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | mem_twin | BULL_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | mem_twin | BULL_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | mem_twin | BULL_EXP | none | 52 | 173 | 0.3006 | 34 | 31 | 18 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | mem_twin | BEAR_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | mem_twin | BEAR_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | mem_twin | BEAR_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 1h | mem_twin | BEAR_EXP | none | 45 | 173 | 0.2601 | 25 | 32 | 20 | 1h+4h | 1h: tuning; 4h: tuning |
| P-RELAY-1/scored | calibrated | 4h | record | NONE | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | record | NONE | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | record | NONE | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | record | NONE | none | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | record | IN_RANGE | both | 10 | 173 | 0.0578 | 7 | 10 | 3 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | record | IN_RANGE | top | 13 | 173 | 0.0751 | 8 | 12 | 5 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | record | IN_RANGE | bot | 8 | 173 | 0.0462 | 4 | 6 | 4 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | record | IN_RANGE | none | 79 | 173 | 0.4566 | 60 | 63 | 19 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | record | BULL_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | record | BULL_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | record | BULL_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | record | BULL_EXP | none | 25 | 173 | 0.1445 | 14 | 23 | 11 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | record | BEAR_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | record | BEAR_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | record | BEAR_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | record | BEAR_EXP | none | 38 | 173 | 0.2197 | 21 | 31 | 17 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | mem_twin | NONE | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | mem_twin | NONE | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | mem_twin | NONE | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | mem_twin | NONE | none | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | mem_twin | IN_RANGE | both | 10 | 173 | 0.0578 | 7 | 10 | 3 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | mem_twin | IN_RANGE | top | 13 | 173 | 0.0751 | 8 | 12 | 5 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | mem_twin | IN_RANGE | bot | 9 | 173 | 0.0520 | 4 | 7 | 5 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | mem_twin | IN_RANGE | none | 78 | 173 | 0.4509 | 60 | 62 | 18 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | mem_twin | BULL_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | mem_twin | BULL_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | mem_twin | BULL_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | mem_twin | BULL_EXP | none | 25 | 173 | 0.1445 | 14 | 23 | 11 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | mem_twin | BEAR_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | mem_twin | BEAR_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | mem_twin | BEAR_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 4h | mem_twin | BEAR_EXP | none | 38 | 173 | 0.2197 | 21 | 31 | 17 | 4h+12h | 4h: tuning; 12h: tuning |
| P-RELAY-1/scored | calibrated | 12h | record | NONE | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | record | NONE | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | record | NONE | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | record | NONE | none | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | record | IN_RANGE | both | 4 | 173 | 0.0231 | 2 | 0 | 2 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | record | IN_RANGE | top | 10 | 173 | 0.0578 | 4 | 6 | 6 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | record | IN_RANGE | bot | 11 | 173 | 0.0636 | 8 | 10 | 3 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | record | IN_RANGE | none | 70 | 173 | 0.4046 | 45 | 53 | 25 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | record | BULL_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | record | BULL_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | record | BULL_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | record | BULL_EXP | none | 42 | 173 | 0.2428 | 31 | 25 | 11 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | record | BEAR_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | record | BEAR_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | record | BEAR_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | record | BEAR_EXP | none | 36 | 173 | 0.2081 | 24 | 19 | 12 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | mem_twin | NONE | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | mem_twin | NONE | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | mem_twin | NONE | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | mem_twin | NONE | none | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | mem_twin | IN_RANGE | both | 6 | 173 | 0.0347 | 2 | 2 | 4 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | mem_twin | IN_RANGE | top | 12 | 173 | 0.0694 | 5 | 8 | 7 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | mem_twin | IN_RANGE | bot | 12 | 173 | 0.0694 | 11 | 11 | 1 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | mem_twin | IN_RANGE | none | 65 | 173 | 0.3757 | 41 | 48 | 24 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | mem_twin | BULL_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | mem_twin | BULL_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | mem_twin | BULL_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | mem_twin | BULL_EXP | none | 42 | 173 | 0.2428 | 31 | 25 | 11 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | mem_twin | BEAR_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | mem_twin | BEAR_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | mem_twin | BEAR_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 12h | mem_twin | BEAR_EXP | none | 36 | 173 | 0.2081 | 24 | 19 | 12 | 12h+1d | 12h: tuning; 1d: tuning |
| P-RELAY-1/scored | calibrated | 1d | record | NONE | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | record | NONE | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | record | NONE | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | record | NONE | none | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | record | IN_RANGE | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | record | IN_RANGE | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | record | IN_RANGE | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | record | IN_RANGE | none | 59 | 173 | 0.3410 | 59 | 27 | 22 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | record | BULL_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | record | BULL_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | record | BULL_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | record | BULL_EXP | none | 63 | 173 | 0.3642 | 63 | 28 | 17 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | record | BEAR_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | record | BEAR_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | record | BEAR_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | record | BEAR_EXP | none | 51 | 173 | 0.2948 | 51 | 25 | 20 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | mem_twin | NONE | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | mem_twin | NONE | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | mem_twin | NONE | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | mem_twin | NONE | none | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | mem_twin | IN_RANGE | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | mem_twin | IN_RANGE | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | mem_twin | IN_RANGE | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | mem_twin | IN_RANGE | none | 59 | 173 | 0.3410 | 59 | 27 | 22 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | mem_twin | BULL_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | mem_twin | BULL_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | mem_twin | BULL_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | mem_twin | BULL_EXP | none | 63 | 173 | 0.3642 | 63 | 28 | 17 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | mem_twin | BEAR_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | mem_twin | BEAR_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | mem_twin | BEAR_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1d | mem_twin | BEAR_EXP | none | 51 | 173 | 0.2948 | 51 | 25 | 20 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1w | record | NONE | NA | 20 | 173 | 0.1156 | 20 | 0 | 0 | 1w | 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1w | record | IN_RANGE | NA | 39 | 173 | 0.2254 | 39 | 0 | 22 | 1w | 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1w | record | BULL_EXP | NA | 28 | 173 | 0.1618 | 28 | 0 | 17 | 1w | 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1w | record | BEAR_EXP | NA | 86 | 173 | 0.4971 | 86 | 0 | 20 | 1w | 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1w | mem_twin | NONE | NA | 20 | 173 | 0.1156 | 20 | 0 | 0 | 1w | 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1w | mem_twin | IN_RANGE | NA | 39 | 173 | 0.2254 | 39 | 0 | 22 | 1w | 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1w | mem_twin | BULL_EXP | NA | 28 | 173 | 0.1618 | 28 | 0 | 17 | 1w | 1w: whole-tape (fallback) |
| P-RELAY-1/scored | calibrated | 1w | mem_twin | BEAR_EXP | NA | 86 | 173 | 0.4971 | 86 | 0 | 20 | 1w | 1w: whole-tape (fallback) |
| P-RELAY-1/scored | frozen3.0 | 1h | record | NONE | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | record | NONE | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | record | NONE | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | record | NONE | none | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | record | IN_RANGE | both | 2 | 173 | 0.0116 | 0 | 0 | 1 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | record | IN_RANGE | top | 7 | 173 | 0.0405 | 0 | 0 | 2 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | record | IN_RANGE | bot | 2 | 173 | 0.0116 | 0 | 0 | 2 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | record | IN_RANGE | none | 76 | 173 | 0.4393 | 0 | 0 | 21 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | record | BULL_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | record | BULL_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | record | BULL_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | record | BULL_EXP | none | 49 | 173 | 0.2832 | 0 | 0 | 15 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | record | BEAR_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | record | BEAR_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | record | BEAR_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | record | BEAR_EXP | none | 37 | 173 | 0.2139 | 0 | 0 | 18 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | mem_twin | NONE | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | mem_twin | NONE | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | mem_twin | NONE | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | mem_twin | NONE | none | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | both | 2 | 173 | 0.0116 | 0 | 0 | 1 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | top | 7 | 173 | 0.0405 | 0 | 0 | 2 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | bot | 2 | 173 | 0.0116 | 0 | 0 | 2 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | none | 76 | 173 | 0.4393 | 0 | 0 | 21 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | none | 49 | 173 | 0.2832 | 0 | 0 | 15 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | none | 37 | 173 | 0.2139 | 0 | 0 | 18 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | record | NONE | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | record | NONE | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | record | NONE | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | record | NONE | none | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | record | IN_RANGE | both | 5 | 173 | 0.0289 | 0 | 0 | 1 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | record | IN_RANGE | top | 4 | 173 | 0.0231 | 0 | 0 | 1 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | record | IN_RANGE | bot | 11 | 173 | 0.0636 | 0 | 0 | 9 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | record | IN_RANGE | none | 64 | 173 | 0.3699 | 0 | 0 | 21 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | record | BULL_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | record | BULL_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | record | BULL_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | record | BULL_EXP | none | 46 | 173 | 0.2659 | 0 | 0 | 12 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | record | BEAR_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | record | BEAR_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | record | BEAR_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | record | BEAR_EXP | none | 43 | 173 | 0.2486 | 0 | 0 | 15 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | mem_twin | NONE | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | mem_twin | NONE | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | mem_twin | NONE | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | mem_twin | NONE | none | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | both | 5 | 173 | 0.0289 | 0 | 0 | 1 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | top | 4 | 173 | 0.0231 | 0 | 0 | 1 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | bot | 11 | 173 | 0.0636 | 0 | 0 | 9 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | none | 64 | 173 | 0.3699 | 0 | 0 | 21 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | none | 46 | 173 | 0.2659 | 0 | 0 | 12 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | none | 43 | 173 | 0.2486 | 0 | 0 | 15 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | record | NONE | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | record | NONE | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | record | NONE | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | record | NONE | none | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | record | IN_RANGE | both | 2 | 173 | 0.0116 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | record | IN_RANGE | top | 15 | 173 | 0.0867 | 0 | 0 | 6 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | record | IN_RANGE | bot | 9 | 173 | 0.0520 | 0 | 0 | 2 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | record | IN_RANGE | none | 38 | 173 | 0.2197 | 0 | 0 | 15 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | record | BULL_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | record | BULL_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | record | BULL_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | record | BULL_EXP | none | 65 | 173 | 0.3757 | 0 | 0 | 22 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | record | BEAR_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | record | BEAR_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | record | BEAR_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | record | BEAR_EXP | none | 44 | 173 | 0.2543 | 0 | 0 | 14 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | mem_twin | NONE | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | mem_twin | NONE | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | mem_twin | NONE | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | mem_twin | NONE | none | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | both | 4 | 173 | 0.0231 | 0 | 0 | 2 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | top | 16 | 173 | 0.0925 | 0 | 0 | 6 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | bot | 8 | 173 | 0.0462 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | none | 36 | 173 | 0.2081 | 0 | 0 | 15 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | none | 65 | 173 | 0.3757 | 0 | 0 | 22 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | none | 44 | 173 | 0.2543 | 0 | 0 | 14 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | record | NONE | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | record | NONE | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | record | NONE | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | record | NONE | none | 3 | 173 | 0.0173 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | record | IN_RANGE | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | record | IN_RANGE | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | record | IN_RANGE | bot | 1 | 173 | 0.0058 | 0 | 0 | 1 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | record | IN_RANGE | none | 56 | 173 | 0.3237 | 0 | 0 | 18 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | record | BULL_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | record | BULL_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | record | BULL_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | record | BULL_EXP | none | 66 | 173 | 0.3815 | 0 | 0 | 20 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | record | BEAR_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | record | BEAR_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | record | BEAR_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | record | BEAR_EXP | none | 47 | 173 | 0.2717 | 0 | 0 | 20 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | mem_twin | NONE | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | mem_twin | NONE | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | mem_twin | NONE | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | mem_twin | NONE | none | 3 | 173 | 0.0173 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | bot | 1 | 173 | 0.0058 | 0 | 0 | 1 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | none | 56 | 173 | 0.3237 | 0 | 0 | 18 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | none | 66 | 173 | 0.3815 | 0 | 0 | 20 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | both | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | top | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | bot | 0 | 173 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | none | 47 | 173 | 0.2717 | 0 | 0 | 20 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1w | record | NONE | NA | 26 | 173 | 0.1503 | 0 | 0 | 0 | 1w | 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1w | record | IN_RANGE | NA | 24 | 173 | 0.1387 | 0 | 0 | 19 | 1w | 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1w | record | BULL_EXP | NA | 43 | 173 | 0.2486 | 0 | 0 | 19 | 1w | 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1w | record | BEAR_EXP | NA | 80 | 173 | 0.4624 | 0 | 0 | 21 | 1w | 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1w | mem_twin | NONE | NA | 26 | 173 | 0.1503 | 0 | 0 | 0 | 1w | 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1w | mem_twin | IN_RANGE | NA | 24 | 173 | 0.1387 | 0 | 0 | 19 | 1w | 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1w | mem_twin | BULL_EXP | NA | 43 | 173 | 0.2486 | 0 | 0 | 19 | 1w | 1w: frozen3.0 |
| P-RELAY-1/scored | frozen3.0 | 1w | mem_twin | BEAR_EXP | NA | 80 | 173 | 0.4624 | 0 | 0 | 21 | 1w | 1w: frozen3.0 |
| P-ADD-BRK/scored | calibrated | 1h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | record | IN_RANGE | both | 4 | 200 | 0.0200 | 2 | 2 | 2 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | record | IN_RANGE | top | 9 | 200 | 0.0450 | 4 | 3 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | record | IN_RANGE | bot | 17 | 200 | 0.0850 | 12 | 11 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | record | IN_RANGE | none | 96 | 200 | 0.4800 | 61 | 57 | 35 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | record | BULL_EXP | none | 38 | 200 | 0.1900 | 27 | 23 | 11 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | record | BEAR_EXP | none | 36 | 200 | 0.1800 | 17 | 19 | 19 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | mem_twin | IN_RANGE | both | 4 | 200 | 0.0200 | 2 | 2 | 2 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | mem_twin | IN_RANGE | top | 10 | 200 | 0.0500 | 5 | 4 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | mem_twin | IN_RANGE | bot | 19 | 200 | 0.0950 | 14 | 12 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | mem_twin | IN_RANGE | none | 93 | 200 | 0.4650 | 58 | 55 | 35 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | mem_twin | BULL_EXP | none | 38 | 200 | 0.1900 | 27 | 23 | 11 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 1h | mem_twin | BEAR_EXP | none | 36 | 200 | 0.1800 | 17 | 19 | 19 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | record | IN_RANGE | both | 9 | 200 | 0.0450 | 7 | 8 | 2 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | record | IN_RANGE | top | 8 | 200 | 0.0400 | 1 | 7 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | record | IN_RANGE | bot | 12 | 200 | 0.0600 | 5 | 11 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | record | IN_RANGE | none | 112 | 200 | 0.5600 | 75 | 90 | 37 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | record | BULL_EXP | none | 32 | 200 | 0.1600 | 20 | 25 | 12 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | record | BEAR_EXP | none | 27 | 200 | 0.1350 | 15 | 22 | 12 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | mem_twin | IN_RANGE | both | 9 | 200 | 0.0450 | 7 | 8 | 2 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | mem_twin | IN_RANGE | top | 8 | 200 | 0.0400 | 1 | 7 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | mem_twin | IN_RANGE | bot | 13 | 200 | 0.0650 | 6 | 11 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | mem_twin | IN_RANGE | none | 111 | 200 | 0.5550 | 74 | 90 | 37 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | mem_twin | BULL_EXP | none | 32 | 200 | 0.1600 | 20 | 25 | 12 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 4h | mem_twin | BEAR_EXP | none | 27 | 200 | 0.1350 | 15 | 22 | 12 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-BRK/scored | calibrated | 12h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | record | IN_RANGE | both | 6 | 200 | 0.0300 | 4 | 3 | 2 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | record | IN_RANGE | top | 4 | 200 | 0.0200 | 1 | 2 | 3 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | record | IN_RANGE | bot | 13 | 200 | 0.0650 | 5 | 8 | 8 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | record | IN_RANGE | none | 80 | 200 | 0.4000 | 44 | 61 | 36 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | record | BULL_EXP | none | 58 | 200 | 0.2900 | 45 | 32 | 13 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | record | BEAR_EXP | none | 39 | 200 | 0.1950 | 24 | 17 | 15 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | mem_twin | IN_RANGE | both | 7 | 200 | 0.0350 | 4 | 4 | 3 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | mem_twin | IN_RANGE | top | 9 | 200 | 0.0450 | 3 | 6 | 6 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | mem_twin | IN_RANGE | bot | 15 | 200 | 0.0750 | 8 | 10 | 7 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | mem_twin | IN_RANGE | none | 72 | 200 | 0.3600 | 39 | 54 | 33 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | mem_twin | BULL_EXP | none | 58 | 200 | 0.2900 | 45 | 32 | 13 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 12h | mem_twin | BEAR_EXP | none | 39 | 200 | 0.1950 | 24 | 17 | 15 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-BRK/scored | calibrated | 1d | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | record | IN_RANGE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | record | IN_RANGE | top | 1 | 200 | 0.0050 | 1 | 1 | 1 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | record | IN_RANGE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | record | IN_RANGE | none | 72 | 200 | 0.3600 | 72 | 26 | 34 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | record | BULL_EXP | none | 77 | 200 | 0.3850 | 77 | 29 | 18 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | record | BEAR_EXP | none | 50 | 200 | 0.2500 | 50 | 19 | 24 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | mem_twin | IN_RANGE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | mem_twin | IN_RANGE | top | 1 | 200 | 0.0050 | 1 | 1 | 1 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | mem_twin | IN_RANGE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | mem_twin | IN_RANGE | none | 72 | 200 | 0.3600 | 72 | 26 | 34 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | mem_twin | BULL_EXP | none | 77 | 200 | 0.3850 | 77 | 29 | 18 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1d | mem_twin | BEAR_EXP | none | 50 | 200 | 0.2500 | 50 | 19 | 24 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1w | record | NONE | NA | 30 | 200 | 0.1500 | 30 | 0 | 0 | 1w | 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1w | record | IN_RANGE | NA | 43 | 200 | 0.2150 | 43 | 0 | 31 | 1w | 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1w | record | BULL_EXP | NA | 29 | 200 | 0.1450 | 29 | 0 | 19 | 1w | 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1w | record | BEAR_EXP | NA | 98 | 200 | 0.4900 | 98 | 0 | 27 | 1w | 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1w | mem_twin | NONE | NA | 30 | 200 | 0.1500 | 30 | 0 | 0 | 1w | 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1w | mem_twin | IN_RANGE | NA | 43 | 200 | 0.2150 | 43 | 0 | 31 | 1w | 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1w | mem_twin | BULL_EXP | NA | 29 | 200 | 0.1450 | 29 | 0 | 19 | 1w | 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | calibrated | 1w | mem_twin | BEAR_EXP | NA | 98 | 200 | 0.4900 | 98 | 0 | 27 | 1w | 1w: whole-tape (fallback) |
| P-ADD-BRK/scored | frozen3.0 | 1h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | record | IN_RANGE | both | 1 | 200 | 0.0050 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | record | IN_RANGE | top | 9 | 200 | 0.0450 | 0 | 0 | 6 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | record | IN_RANGE | bot | 2 | 200 | 0.0100 | 0 | 0 | 1 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | record | IN_RANGE | none | 115 | 200 | 0.5750 | 0 | 0 | 42 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | record | BULL_EXP | none | 41 | 200 | 0.2050 | 0 | 0 | 17 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | record | BEAR_EXP | none | 32 | 200 | 0.1600 | 0 | 0 | 11 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | both | 1 | 200 | 0.0050 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | top | 10 | 200 | 0.0500 | 0 | 0 | 7 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | bot | 2 | 200 | 0.0100 | 0 | 0 | 1 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | none | 114 | 200 | 0.5700 | 0 | 0 | 41 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | none | 41 | 200 | 0.2050 | 0 | 0 | 17 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | none | 32 | 200 | 0.1600 | 0 | 0 | 11 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | record | IN_RANGE | both | 5 | 200 | 0.0250 | 0 | 0 | 1 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | record | IN_RANGE | top | 3 | 200 | 0.0150 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | record | IN_RANGE | bot | 13 | 200 | 0.0650 | 0 | 0 | 10 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | record | IN_RANGE | none | 73 | 200 | 0.3650 | 0 | 0 | 34 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | record | BULL_EXP | none | 66 | 200 | 0.3300 | 0 | 0 | 19 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | record | BEAR_EXP | none | 40 | 200 | 0.2000 | 0 | 0 | 13 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | both | 5 | 200 | 0.0250 | 0 | 0 | 1 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | top | 3 | 200 | 0.0150 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | bot | 13 | 200 | 0.0650 | 0 | 0 | 10 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | none | 73 | 200 | 0.3650 | 0 | 0 | 34 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | none | 66 | 200 | 0.3300 | 0 | 0 | 19 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | none | 40 | 200 | 0.2000 | 0 | 0 | 13 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | record | IN_RANGE | both | 5 | 200 | 0.0250 | 0 | 0 | 3 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | record | IN_RANGE | top | 9 | 200 | 0.0450 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | record | IN_RANGE | bot | 9 | 200 | 0.0450 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | record | IN_RANGE | none | 51 | 200 | 0.2550 | 0 | 0 | 25 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | record | BULL_EXP | none | 76 | 200 | 0.3800 | 0 | 0 | 24 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | record | BEAR_EXP | none | 50 | 200 | 0.2500 | 0 | 0 | 17 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | both | 6 | 200 | 0.0300 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | top | 9 | 200 | 0.0450 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | bot | 8 | 200 | 0.0400 | 0 | 0 | 3 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | none | 51 | 200 | 0.2550 | 0 | 0 | 25 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | none | 76 | 200 | 0.3800 | 0 | 0 | 24 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | none | 50 | 200 | 0.2500 | 0 | 0 | 17 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | record | NONE | none | 4 | 200 | 0.0200 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | record | IN_RANGE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | record | IN_RANGE | top | 2 | 200 | 0.0100 | 0 | 0 | 2 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | record | IN_RANGE | bot | 1 | 200 | 0.0050 | 0 | 0 | 1 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | record | IN_RANGE | none | 55 | 200 | 0.2750 | 0 | 0 | 25 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | record | BULL_EXP | none | 74 | 200 | 0.3700 | 0 | 0 | 19 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | record | BEAR_EXP | none | 64 | 200 | 0.3200 | 0 | 0 | 30 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | mem_twin | NONE | none | 4 | 200 | 0.0200 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | top | 2 | 200 | 0.0100 | 0 | 0 | 2 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | bot | 1 | 200 | 0.0050 | 0 | 0 | 1 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | none | 55 | 200 | 0.2750 | 0 | 0 | 25 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | none | 74 | 200 | 0.3700 | 0 | 0 | 19 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | none | 64 | 200 | 0.3200 | 0 | 0 | 30 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1w | record | NONE | NA | 37 | 200 | 0.1850 | 0 | 0 | 0 | 1w | 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1w | record | IN_RANGE | NA | 29 | 200 | 0.1450 | 0 | 0 | 25 | 1w | 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1w | record | BULL_EXP | NA | 40 | 200 | 0.2000 | 0 | 0 | 20 | 1w | 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1w | record | BEAR_EXP | NA | 94 | 200 | 0.4700 | 0 | 0 | 32 | 1w | 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1w | mem_twin | NONE | NA | 37 | 200 | 0.1850 | 0 | 0 | 0 | 1w | 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1w | mem_twin | IN_RANGE | NA | 29 | 200 | 0.1450 | 0 | 0 | 25 | 1w | 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1w | mem_twin | BULL_EXP | NA | 40 | 200 | 0.2000 | 0 | 0 | 20 | 1w | 1w: frozen3.0 |
| P-ADD-BRK/scored | frozen3.0 | 1w | mem_twin | BEAR_EXP | NA | 94 | 200 | 0.4700 | 0 | 0 | 32 | 1w | 1w: frozen3.0 |
| P-ADD-SFP/scored | calibrated | 1h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | record | IN_RANGE | both | 4 | 200 | 0.0200 | 2 | 2 | 2 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | record | IN_RANGE | top | 9 | 200 | 0.0450 | 4 | 3 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | record | IN_RANGE | bot | 17 | 200 | 0.0850 | 12 | 11 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | record | IN_RANGE | none | 96 | 200 | 0.4800 | 61 | 57 | 35 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | record | BULL_EXP | none | 38 | 200 | 0.1900 | 27 | 23 | 11 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | record | BEAR_EXP | none | 36 | 200 | 0.1800 | 17 | 19 | 19 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | mem_twin | IN_RANGE | both | 4 | 200 | 0.0200 | 2 | 2 | 2 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | mem_twin | IN_RANGE | top | 10 | 200 | 0.0500 | 5 | 4 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | mem_twin | IN_RANGE | bot | 19 | 200 | 0.0950 | 14 | 12 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | mem_twin | IN_RANGE | none | 93 | 200 | 0.4650 | 58 | 55 | 35 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | mem_twin | BULL_EXP | none | 38 | 200 | 0.1900 | 27 | 23 | 11 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 1h | mem_twin | BEAR_EXP | none | 36 | 200 | 0.1800 | 17 | 19 | 19 | 1h+4h | 1h: tuning; 4h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | record | IN_RANGE | both | 9 | 200 | 0.0450 | 7 | 8 | 2 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | record | IN_RANGE | top | 8 | 200 | 0.0400 | 1 | 7 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | record | IN_RANGE | bot | 12 | 200 | 0.0600 | 5 | 11 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | record | IN_RANGE | none | 112 | 200 | 0.5600 | 75 | 90 | 37 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | record | BULL_EXP | none | 32 | 200 | 0.1600 | 20 | 25 | 12 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | record | BEAR_EXP | none | 27 | 200 | 0.1350 | 15 | 22 | 12 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | mem_twin | IN_RANGE | both | 9 | 200 | 0.0450 | 7 | 8 | 2 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | mem_twin | IN_RANGE | top | 8 | 200 | 0.0400 | 1 | 7 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | mem_twin | IN_RANGE | bot | 13 | 200 | 0.0650 | 6 | 11 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | mem_twin | IN_RANGE | none | 111 | 200 | 0.5550 | 74 | 90 | 37 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | mem_twin | BULL_EXP | none | 32 | 200 | 0.1600 | 20 | 25 | 12 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 4h | mem_twin | BEAR_EXP | none | 27 | 200 | 0.1350 | 15 | 22 | 12 | 4h+12h | 4h: tuning; 12h: tuning |
| P-ADD-SFP/scored | calibrated | 12h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | record | IN_RANGE | both | 6 | 200 | 0.0300 | 4 | 3 | 2 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | record | IN_RANGE | top | 4 | 200 | 0.0200 | 1 | 2 | 3 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | record | IN_RANGE | bot | 13 | 200 | 0.0650 | 5 | 8 | 8 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | record | IN_RANGE | none | 80 | 200 | 0.4000 | 44 | 61 | 36 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | record | BULL_EXP | none | 58 | 200 | 0.2900 | 45 | 32 | 13 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | record | BEAR_EXP | none | 39 | 200 | 0.1950 | 24 | 17 | 15 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | mem_twin | IN_RANGE | both | 7 | 200 | 0.0350 | 4 | 4 | 3 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | mem_twin | IN_RANGE | top | 9 | 200 | 0.0450 | 3 | 6 | 6 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | mem_twin | IN_RANGE | bot | 15 | 200 | 0.0750 | 8 | 10 | 7 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | mem_twin | IN_RANGE | none | 72 | 200 | 0.3600 | 39 | 54 | 33 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | mem_twin | BULL_EXP | none | 58 | 200 | 0.2900 | 45 | 32 | 13 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 12h | mem_twin | BEAR_EXP | none | 39 | 200 | 0.1950 | 24 | 17 | 15 | 12h+1d | 12h: tuning; 1d: tuning |
| P-ADD-SFP/scored | calibrated | 1d | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | record | IN_RANGE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | record | IN_RANGE | top | 1 | 200 | 0.0050 | 1 | 1 | 1 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | record | IN_RANGE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | record | IN_RANGE | none | 72 | 200 | 0.3600 | 72 | 26 | 34 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | record | BULL_EXP | none | 77 | 200 | 0.3850 | 77 | 29 | 18 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | record | BEAR_EXP | none | 50 | 200 | 0.2500 | 50 | 19 | 24 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | mem_twin | IN_RANGE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | mem_twin | IN_RANGE | top | 1 | 200 | 0.0050 | 1 | 1 | 1 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | mem_twin | IN_RANGE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | mem_twin | IN_RANGE | none | 72 | 200 | 0.3600 | 72 | 26 | 34 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | mem_twin | BULL_EXP | none | 77 | 200 | 0.3850 | 77 | 29 | 18 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1d | mem_twin | BEAR_EXP | none | 50 | 200 | 0.2500 | 50 | 19 | 24 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1w | record | NONE | NA | 30 | 200 | 0.1500 | 30 | 0 | 0 | 1w | 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1w | record | IN_RANGE | NA | 43 | 200 | 0.2150 | 43 | 0 | 31 | 1w | 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1w | record | BULL_EXP | NA | 29 | 200 | 0.1450 | 29 | 0 | 19 | 1w | 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1w | record | BEAR_EXP | NA | 98 | 200 | 0.4900 | 98 | 0 | 27 | 1w | 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1w | mem_twin | NONE | NA | 30 | 200 | 0.1500 | 30 | 0 | 0 | 1w | 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1w | mem_twin | IN_RANGE | NA | 43 | 200 | 0.2150 | 43 | 0 | 31 | 1w | 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1w | mem_twin | BULL_EXP | NA | 29 | 200 | 0.1450 | 29 | 0 | 19 | 1w | 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | calibrated | 1w | mem_twin | BEAR_EXP | NA | 98 | 200 | 0.4900 | 98 | 0 | 27 | 1w | 1w: whole-tape (fallback) |
| P-ADD-SFP/scored | frozen3.0 | 1h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | record | IN_RANGE | both | 1 | 200 | 0.0050 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | record | IN_RANGE | top | 9 | 200 | 0.0450 | 0 | 0 | 6 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | record | IN_RANGE | bot | 2 | 200 | 0.0100 | 0 | 0 | 1 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | record | IN_RANGE | none | 115 | 200 | 0.5750 | 0 | 0 | 42 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | record | BULL_EXP | none | 41 | 200 | 0.2050 | 0 | 0 | 17 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | record | BEAR_EXP | none | 32 | 200 | 0.1600 | 0 | 0 | 11 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | both | 1 | 200 | 0.0050 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | top | 10 | 200 | 0.0500 | 0 | 0 | 7 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | bot | 2 | 200 | 0.0100 | 0 | 0 | 1 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | none | 114 | 200 | 0.5700 | 0 | 0 | 41 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | none | 41 | 200 | 0.2050 | 0 | 0 | 17 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | none | 32 | 200 | 0.1600 | 0 | 0 | 11 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | record | IN_RANGE | both | 5 | 200 | 0.0250 | 0 | 0 | 1 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | record | IN_RANGE | top | 3 | 200 | 0.0150 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | record | IN_RANGE | bot | 13 | 200 | 0.0650 | 0 | 0 | 10 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | record | IN_RANGE | none | 73 | 200 | 0.3650 | 0 | 0 | 34 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | record | BULL_EXP | none | 66 | 200 | 0.3300 | 0 | 0 | 19 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | record | BEAR_EXP | none | 40 | 200 | 0.2000 | 0 | 0 | 13 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | both | 5 | 200 | 0.0250 | 0 | 0 | 1 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | top | 3 | 200 | 0.0150 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | bot | 13 | 200 | 0.0650 | 0 | 0 | 10 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | none | 73 | 200 | 0.3650 | 0 | 0 | 34 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | none | 66 | 200 | 0.3300 | 0 | 0 | 19 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | none | 40 | 200 | 0.2000 | 0 | 0 | 13 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | record | IN_RANGE | both | 5 | 200 | 0.0250 | 0 | 0 | 3 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | record | IN_RANGE | top | 9 | 200 | 0.0450 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | record | IN_RANGE | bot | 9 | 200 | 0.0450 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | record | IN_RANGE | none | 51 | 200 | 0.2550 | 0 | 0 | 25 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | record | BULL_EXP | none | 76 | 200 | 0.3800 | 0 | 0 | 24 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | record | BEAR_EXP | none | 50 | 200 | 0.2500 | 0 | 0 | 17 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | both | 6 | 200 | 0.0300 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | top | 9 | 200 | 0.0450 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | bot | 8 | 200 | 0.0400 | 0 | 0 | 3 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | none | 51 | 200 | 0.2550 | 0 | 0 | 25 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | none | 76 | 200 | 0.3800 | 0 | 0 | 24 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | none | 50 | 200 | 0.2500 | 0 | 0 | 17 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | record | NONE | none | 4 | 200 | 0.0200 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | record | IN_RANGE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | record | IN_RANGE | top | 2 | 200 | 0.0100 | 0 | 0 | 2 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | record | IN_RANGE | bot | 1 | 200 | 0.0050 | 0 | 0 | 1 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | record | IN_RANGE | none | 55 | 200 | 0.2750 | 0 | 0 | 25 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | record | BULL_EXP | none | 74 | 200 | 0.3700 | 0 | 0 | 19 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | record | BEAR_EXP | none | 64 | 200 | 0.3200 | 0 | 0 | 30 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | mem_twin | NONE | none | 4 | 200 | 0.0200 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | top | 2 | 200 | 0.0100 | 0 | 0 | 2 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | bot | 1 | 200 | 0.0050 | 0 | 0 | 1 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | none | 55 | 200 | 0.2750 | 0 | 0 | 25 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | none | 74 | 200 | 0.3700 | 0 | 0 | 19 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | none | 64 | 200 | 0.3200 | 0 | 0 | 30 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1w | record | NONE | NA | 37 | 200 | 0.1850 | 0 | 0 | 0 | 1w | 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1w | record | IN_RANGE | NA | 29 | 200 | 0.1450 | 0 | 0 | 25 | 1w | 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1w | record | BULL_EXP | NA | 40 | 200 | 0.2000 | 0 | 0 | 20 | 1w | 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1w | record | BEAR_EXP | NA | 94 | 200 | 0.4700 | 0 | 0 | 32 | 1w | 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1w | mem_twin | NONE | NA | 37 | 200 | 0.1850 | 0 | 0 | 0 | 1w | 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1w | mem_twin | IN_RANGE | NA | 29 | 200 | 0.1450 | 0 | 0 | 25 | 1w | 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1w | mem_twin | BULL_EXP | NA | 40 | 200 | 0.2000 | 0 | 0 | 20 | 1w | 1w: frozen3.0 |
| P-ADD-SFP/scored | frozen3.0 | 1w | mem_twin | BEAR_EXP | NA | 94 | 200 | 0.4700 | 0 | 0 | 32 | 1w | 1w: frozen3.0 |
| P-TP-RNG/scored | calibrated | 1h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | record | IN_RANGE | both | 4 | 200 | 0.0200 | 2 | 2 | 2 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | record | IN_RANGE | top | 9 | 200 | 0.0450 | 4 | 3 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | record | IN_RANGE | bot | 17 | 200 | 0.0850 | 12 | 11 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | record | IN_RANGE | none | 96 | 200 | 0.4800 | 61 | 57 | 35 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | record | BULL_EXP | none | 38 | 200 | 0.1900 | 27 | 23 | 11 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | record | BEAR_EXP | none | 36 | 200 | 0.1800 | 17 | 19 | 19 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | mem_twin | IN_RANGE | both | 4 | 200 | 0.0200 | 2 | 2 | 2 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | mem_twin | IN_RANGE | top | 10 | 200 | 0.0500 | 5 | 4 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | mem_twin | IN_RANGE | bot | 19 | 200 | 0.0950 | 14 | 12 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | mem_twin | IN_RANGE | none | 93 | 200 | 0.4650 | 58 | 55 | 35 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | mem_twin | BULL_EXP | none | 38 | 200 | 0.1900 | 27 | 23 | 11 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 1h | mem_twin | BEAR_EXP | none | 36 | 200 | 0.1800 | 17 | 19 | 19 | 1h+4h | 1h: tuning; 4h: tuning |
| P-TP-RNG/scored | calibrated | 4h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | record | IN_RANGE | both | 9 | 200 | 0.0450 | 7 | 8 | 2 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | record | IN_RANGE | top | 8 | 200 | 0.0400 | 1 | 7 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | record | IN_RANGE | bot | 12 | 200 | 0.0600 | 5 | 11 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | record | IN_RANGE | none | 112 | 200 | 0.5600 | 75 | 90 | 37 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | record | BULL_EXP | none | 32 | 200 | 0.1600 | 20 | 25 | 12 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | record | BEAR_EXP | none | 27 | 200 | 0.1350 | 15 | 22 | 12 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | mem_twin | IN_RANGE | both | 9 | 200 | 0.0450 | 7 | 8 | 2 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | mem_twin | IN_RANGE | top | 8 | 200 | 0.0400 | 1 | 7 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | mem_twin | IN_RANGE | bot | 13 | 200 | 0.0650 | 6 | 11 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | mem_twin | IN_RANGE | none | 111 | 200 | 0.5550 | 74 | 90 | 37 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | mem_twin | BULL_EXP | none | 32 | 200 | 0.1600 | 20 | 25 | 12 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 4h | mem_twin | BEAR_EXP | none | 27 | 200 | 0.1350 | 15 | 22 | 12 | 4h+12h | 4h: tuning; 12h: tuning |
| P-TP-RNG/scored | calibrated | 12h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | record | IN_RANGE | both | 6 | 200 | 0.0300 | 4 | 3 | 2 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | record | IN_RANGE | top | 4 | 200 | 0.0200 | 1 | 2 | 3 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | record | IN_RANGE | bot | 13 | 200 | 0.0650 | 5 | 8 | 8 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | record | IN_RANGE | none | 80 | 200 | 0.4000 | 44 | 61 | 36 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | record | BULL_EXP | none | 58 | 200 | 0.2900 | 45 | 32 | 13 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | record | BEAR_EXP | none | 39 | 200 | 0.1950 | 24 | 17 | 15 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | mem_twin | IN_RANGE | both | 7 | 200 | 0.0350 | 4 | 4 | 3 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | mem_twin | IN_RANGE | top | 9 | 200 | 0.0450 | 3 | 6 | 6 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | mem_twin | IN_RANGE | bot | 15 | 200 | 0.0750 | 8 | 10 | 7 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | mem_twin | IN_RANGE | none | 72 | 200 | 0.3600 | 39 | 54 | 33 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | mem_twin | BULL_EXP | none | 58 | 200 | 0.2900 | 45 | 32 | 13 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 12h | mem_twin | BEAR_EXP | none | 39 | 200 | 0.1950 | 24 | 17 | 15 | 12h+1d | 12h: tuning; 1d: tuning |
| P-TP-RNG/scored | calibrated | 1d | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | record | IN_RANGE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | record | IN_RANGE | top | 1 | 200 | 0.0050 | 1 | 1 | 1 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | record | IN_RANGE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | record | IN_RANGE | none | 72 | 200 | 0.3600 | 72 | 26 | 34 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | record | BULL_EXP | none | 77 | 200 | 0.3850 | 77 | 29 | 18 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | record | BEAR_EXP | none | 50 | 200 | 0.2500 | 50 | 19 | 24 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | mem_twin | IN_RANGE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | mem_twin | IN_RANGE | top | 1 | 200 | 0.0050 | 1 | 1 | 1 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | mem_twin | IN_RANGE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | mem_twin | IN_RANGE | none | 72 | 200 | 0.3600 | 72 | 26 | 34 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | mem_twin | BULL_EXP | none | 77 | 200 | 0.3850 | 77 | 29 | 18 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1d | mem_twin | BEAR_EXP | none | 50 | 200 | 0.2500 | 50 | 19 | 24 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1w | record | NONE | NA | 30 | 200 | 0.1500 | 30 | 0 | 0 | 1w | 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1w | record | IN_RANGE | NA | 43 | 200 | 0.2150 | 43 | 0 | 31 | 1w | 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1w | record | BULL_EXP | NA | 29 | 200 | 0.1450 | 29 | 0 | 19 | 1w | 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1w | record | BEAR_EXP | NA | 98 | 200 | 0.4900 | 98 | 0 | 27 | 1w | 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1w | mem_twin | NONE | NA | 30 | 200 | 0.1500 | 30 | 0 | 0 | 1w | 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1w | mem_twin | IN_RANGE | NA | 43 | 200 | 0.2150 | 43 | 0 | 31 | 1w | 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1w | mem_twin | BULL_EXP | NA | 29 | 200 | 0.1450 | 29 | 0 | 19 | 1w | 1w: whole-tape (fallback) |
| P-TP-RNG/scored | calibrated | 1w | mem_twin | BEAR_EXP | NA | 98 | 200 | 0.4900 | 98 | 0 | 27 | 1w | 1w: whole-tape (fallback) |
| P-TP-RNG/scored | frozen3.0 | 1h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | record | IN_RANGE | both | 1 | 200 | 0.0050 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | record | IN_RANGE | top | 9 | 200 | 0.0450 | 0 | 0 | 6 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | record | IN_RANGE | bot | 2 | 200 | 0.0100 | 0 | 0 | 1 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | record | IN_RANGE | none | 115 | 200 | 0.5750 | 0 | 0 | 42 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | record | BULL_EXP | none | 41 | 200 | 0.2050 | 0 | 0 | 17 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | record | BEAR_EXP | none | 32 | 200 | 0.1600 | 0 | 0 | 11 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | both | 1 | 200 | 0.0050 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | top | 10 | 200 | 0.0500 | 0 | 0 | 7 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | bot | 2 | 200 | 0.0100 | 0 | 0 | 1 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | mem_twin | IN_RANGE | none | 114 | 200 | 0.5700 | 0 | 0 | 41 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | mem_twin | BULL_EXP | none | 41 | 200 | 0.2050 | 0 | 0 | 17 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1h | mem_twin | BEAR_EXP | none | 32 | 200 | 0.1600 | 0 | 0 | 11 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | record | IN_RANGE | both | 5 | 200 | 0.0250 | 0 | 0 | 1 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | record | IN_RANGE | top | 3 | 200 | 0.0150 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | record | IN_RANGE | bot | 13 | 200 | 0.0650 | 0 | 0 | 10 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | record | IN_RANGE | none | 73 | 200 | 0.3650 | 0 | 0 | 34 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | record | BULL_EXP | none | 66 | 200 | 0.3300 | 0 | 0 | 19 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | record | BEAR_EXP | none | 40 | 200 | 0.2000 | 0 | 0 | 13 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | both | 5 | 200 | 0.0250 | 0 | 0 | 1 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | top | 3 | 200 | 0.0150 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | bot | 13 | 200 | 0.0650 | 0 | 0 | 10 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | mem_twin | IN_RANGE | none | 73 | 200 | 0.3650 | 0 | 0 | 34 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | mem_twin | BULL_EXP | none | 66 | 200 | 0.3300 | 0 | 0 | 19 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 4h | mem_twin | BEAR_EXP | none | 40 | 200 | 0.2000 | 0 | 0 | 13 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | record | IN_RANGE | both | 5 | 200 | 0.0250 | 0 | 0 | 3 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | record | IN_RANGE | top | 9 | 200 | 0.0450 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | record | IN_RANGE | bot | 9 | 200 | 0.0450 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | record | IN_RANGE | none | 51 | 200 | 0.2550 | 0 | 0 | 25 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | record | BULL_EXP | none | 76 | 200 | 0.3800 | 0 | 0 | 24 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | record | BEAR_EXP | none | 50 | 200 | 0.2500 | 0 | 0 | 17 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | both | 6 | 200 | 0.0300 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | top | 9 | 200 | 0.0450 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | bot | 8 | 200 | 0.0400 | 0 | 0 | 3 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | mem_twin | IN_RANGE | none | 51 | 200 | 0.2550 | 0 | 0 | 25 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | mem_twin | BULL_EXP | none | 76 | 200 | 0.3800 | 0 | 0 | 24 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 12h | mem_twin | BEAR_EXP | none | 50 | 200 | 0.2500 | 0 | 0 | 17 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | record | NONE | none | 4 | 200 | 0.0200 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | record | IN_RANGE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | record | IN_RANGE | top | 2 | 200 | 0.0100 | 0 | 0 | 2 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | record | IN_RANGE | bot | 1 | 200 | 0.0050 | 0 | 0 | 1 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | record | IN_RANGE | none | 55 | 200 | 0.2750 | 0 | 0 | 25 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | record | BULL_EXP | none | 74 | 200 | 0.3700 | 0 | 0 | 19 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | record | BEAR_EXP | none | 64 | 200 | 0.3200 | 0 | 0 | 30 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | mem_twin | NONE | none | 4 | 200 | 0.0200 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | top | 2 | 200 | 0.0100 | 0 | 0 | 2 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | bot | 1 | 200 | 0.0050 | 0 | 0 | 1 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | mem_twin | IN_RANGE | none | 55 | 200 | 0.2750 | 0 | 0 | 25 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | mem_twin | BULL_EXP | none | 74 | 200 | 0.3700 | 0 | 0 | 19 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1d | mem_twin | BEAR_EXP | none | 64 | 200 | 0.3200 | 0 | 0 | 30 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1w | record | NONE | NA | 37 | 200 | 0.1850 | 0 | 0 | 0 | 1w | 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1w | record | IN_RANGE | NA | 29 | 200 | 0.1450 | 0 | 0 | 25 | 1w | 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1w | record | BULL_EXP | NA | 40 | 200 | 0.2000 | 0 | 0 | 20 | 1w | 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1w | record | BEAR_EXP | NA | 94 | 200 | 0.4700 | 0 | 0 | 32 | 1w | 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1w | mem_twin | NONE | NA | 37 | 200 | 0.1850 | 0 | 0 | 0 | 1w | 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1w | mem_twin | IN_RANGE | NA | 29 | 200 | 0.1450 | 0 | 0 | 25 | 1w | 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1w | mem_twin | BULL_EXP | NA | 40 | 200 | 0.2000 | 0 | 0 | 20 | 1w | 1w: frozen3.0 |
| P-TP-RNG/scored | frozen3.0 | 1w | mem_twin | BEAR_EXP | NA | 94 | 200 | 0.4700 | 0 | 0 | 32 | 1w | 1w: frozen3.0 |

### Outcomes by L state at ENTRY (n, E[net R], P(win), ΣR — the book's own net_r; the HOLDOUT slice beside) — WHOLE

| book | scale_kind | lens | state | n | mean_net_r | p_win | sum_net_r | n_scale_in_sample | n_stability_changed | n_holdout | mean_net_r_holdout | p_win_holdout | sum_net_r_holdout | pick_window | stability_changed_members |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P-WARN-1/scored | calibrated | 1h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-WARN-1/scored | calibrated | 1h | IN_RANGE | 126 | 0.2176 | 0.3333 | 27.4159 | 79 | 73 | 47 | 0.5951 | 0.3830 | 27.9693 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-WARN-1/scored | calibrated | 1h | BULL_EXP | 38 | -0.1280 | 0.2632 | -4.8655 | 27 | 23 | 11 | -0.3312 | 0.2727 | -3.6437 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-WARN-1/scored | calibrated | 1h | BEAR_EXP | 36 | 0.5381 | 0.3056 | 19.3728 | 17 | 19 | 19 | 0.9082 | 0.2105 | 17.2566 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-WARN-1/scored | calibrated | 1h | __ALL__ | 200 | 0.2096 | 0.3150 | 41.9232 | 123 | 115 | 77 | 0.5400 | 0.3247 | 41.5822 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-WARN-1/scored | calibrated | 4h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h: tuning | 4h: NEARUSDT |
| P-WARN-1/scored | calibrated | 4h | IN_RANGE | 141 | 0.1643 | 0.3121 | 23.1695 | 88 | 31 | 53 | 0.3936 | 0.3208 | 20.8609 | 4h: tuning | 4h: NEARUSDT |
| P-WARN-1/scored | calibrated | 4h | BULL_EXP | 32 | 0.7521 | 0.4062 | 24.0657 | 20 | 1 | 12 | 2.2043 | 0.5000 | 26.4521 | 4h: tuning | 4h: NEARUSDT |
| P-WARN-1/scored | calibrated | 4h | BEAR_EXP | 27 | -0.1967 | 0.2222 | -5.3120 | 15 | 8 | 12 | -0.4776 | 0.1667 | -5.7308 | 4h: tuning | 4h: NEARUSDT |
| P-WARN-1/scored | calibrated | 4h | __ALL__ | 200 | 0.2096 | 0.3150 | 41.9232 | 123 | 40 | 77 | 0.5400 | 0.3247 | 41.5822 | 4h: tuning | 4h: NEARUSDT |
| P-WARN-1/scored | calibrated | 12h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 12h | IN_RANGE | 103 | 0.1208 | 0.2718 | 12.4469 | 54 | 74 | 49 | 0.1703 | 0.2857 | 8.3469 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 12h | BULL_EXP | 58 | 0.4610 | 0.3621 | 26.7395 | 45 | 32 | 13 | 2.2197 | 0.3846 | 28.8562 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 12h | BEAR_EXP | 39 | 0.0702 | 0.3590 | 2.7369 | 24 | 17 | 15 | 0.2919 | 0.4000 | 4.3792 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 12h | __ALL__ | 200 | 0.2096 | 0.3150 | 41.9232 | 123 | 123 | 77 | 0.5400 | 0.3247 | 41.5822 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 1d | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 1d | IN_RANGE | 73 | 0.1335 | 0.2877 | 9.7459 | 38 | 27 | 35 | 0.3053 | 0.3143 | 10.6865 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 1d | BULL_EXP | 77 | 0.1417 | 0.3506 | 10.9088 | 59 | 29 | 18 | 1.0208 | 0.5556 | 18.3737 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 1d | BEAR_EXP | 50 | 0.4254 | 0.3000 | 21.2685 | 26 | 19 | 24 | 0.5218 | 0.1667 | 12.5220 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 1d | __ALL__ | 200 | 0.2096 | 0.3150 | 41.9232 | 123 | 75 | 77 | 0.5400 | 0.3247 | 41.5822 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 1w | NONE | 30 | 0.3901 | 0.3667 | 11.7028 | 30 | 0 | 0 | — | — | — | 1w: whole-tape (fallback) | 1w: none |
| P-WARN-1/scored | calibrated | 1w | IN_RANGE | 43 | 0.1497 | 0.3256 | 6.4368 | 43 | 0 | 31 | 0.1008 | 0.2903 | 3.1240 | 1w: whole-tape (fallback) | 1w: none |
| P-WARN-1/scored | calibrated | 1w | BULL_EXP | 29 | 1.2781 | 0.3103 | 37.0640 | 29 | 0 | 19 | 2.0104 | 0.3684 | 38.1983 | 1w: whole-tape (fallback) | 1w: none |
| P-WARN-1/scored | calibrated | 1w | BEAR_EXP | 98 | -0.1355 | 0.2959 | -13.2804 | 98 | 0 | 27 | 0.0096 | 0.3333 | 0.2599 | 1w: whole-tape (fallback) | 1w: none |
| P-WARN-1/scored | calibrated | 1w | __ALL__ | 200 | 0.2096 | 0.3150 | 41.9232 | 200 | 0 | 77 | 0.5400 | 0.3247 | 41.5822 | 1w: whole-tape (fallback) | 1w: none |
| P-WARN-1/scored | frozen3.0 | 1h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h: frozen3.0 | 1h: none |
| P-WARN-1/scored | frozen3.0 | 1h | IN_RANGE | 127 | 0.2731 | 0.2992 | 34.6883 | 0 | 0 | 49 | 0.9730 | 0.3673 | 47.6782 | 1h: frozen3.0 | 1h: none |
| P-WARN-1/scored | frozen3.0 | 1h | BULL_EXP | 41 | -0.0131 | 0.3171 | -0.5367 | 0 | 0 | 17 | -0.3619 | 0.1765 | -6.1515 | 1h: frozen3.0 | 1h: none |
| P-WARN-1/scored | frozen3.0 | 1h | BEAR_EXP | 32 | 0.2429 | 0.3750 | 7.7717 | 0 | 0 | 11 | 0.0050 | 0.3636 | 0.0555 | 1h: frozen3.0 | 1h: none |
| P-WARN-1/scored | frozen3.0 | 1h | __ALL__ | 200 | 0.2096 | 0.3150 | 41.9232 | 0 | 0 | 77 | 0.5400 | 0.3247 | 41.5822 | 1h: frozen3.0 | 1h: none |
| P-WARN-1/scored | frozen3.0 | 4h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h: frozen3.0 | 4h: none |
| P-WARN-1/scored | frozen3.0 | 4h | IN_RANGE | 94 | 0.2444 | 0.3298 | 22.9776 | 0 | 0 | 45 | 0.3765 | 0.3556 | 16.9413 | 4h: frozen3.0 | 4h: none |
| P-WARN-1/scored | frozen3.0 | 4h | BULL_EXP | 66 | 0.2776 | 0.2879 | 18.3244 | 0 | 0 | 19 | 1.5402 | 0.3158 | 29.2629 | 4h: frozen3.0 | 4h: none |
| P-WARN-1/scored | frozen3.0 | 4h | BEAR_EXP | 40 | 0.0155 | 0.3250 | 0.6212 | 0 | 0 | 13 | -0.3555 | 0.2308 | -4.6219 | 4h: frozen3.0 | 4h: none |
| P-WARN-1/scored | frozen3.0 | 4h | __ALL__ | 200 | 0.2096 | 0.3150 | 41.9232 | 0 | 0 | 77 | 0.5400 | 0.3247 | 41.5822 | 4h: frozen3.0 | 4h: none |
| P-WARN-1/scored | frozen3.0 | 12h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 12h: frozen3.0 | 12h: none |
| P-WARN-1/scored | frozen3.0 | 12h | IN_RANGE | 74 | 0.1170 | 0.2838 | 8.6588 | 0 | 0 | 36 | 0.2863 | 0.3056 | 10.3085 | 12h: frozen3.0 | 12h: none |
| P-WARN-1/scored | frozen3.0 | 12h | BULL_EXP | 76 | 0.4763 | 0.3684 | 36.1991 | 0 | 0 | 24 | 1.6812 | 0.5000 | 40.3482 | 12h: frozen3.0 | 12h: none |
| P-WARN-1/scored | frozen3.0 | 12h | BEAR_EXP | 50 | -0.0587 | 0.2800 | -2.9346 | 0 | 0 | 17 | -0.5338 | 0.1176 | -9.0745 | 12h: frozen3.0 | 12h: none |
| P-WARN-1/scored | frozen3.0 | 12h | __ALL__ | 200 | 0.2096 | 0.3150 | 41.9232 | 0 | 0 | 77 | 0.5400 | 0.3247 | 41.5822 | 12h: frozen3.0 | 12h: none |
| P-WARN-1/scored | frozen3.0 | 1d | NONE | 4 | -0.3259 | 0.2500 | -1.3037 | 0 | 0 | 0 | — | — | — | 1d: frozen3.0 | 1d: none |
| P-WARN-1/scored | frozen3.0 | 1d | IN_RANGE | 58 | -0.1536 | 0.2759 | -8.9075 | 0 | 0 | 28 | 0.0492 | 0.3571 | 1.3779 | 1d: frozen3.0 | 1d: none |
| P-WARN-1/scored | frozen3.0 | 1d | BULL_EXP | 74 | 0.2577 | 0.3108 | 19.0701 | 0 | 0 | 19 | 0.7761 | 0.3158 | 14.7453 | 1d: frozen3.0 | 1d: none |
| P-WARN-1/scored | frozen3.0 | 1d | BEAR_EXP | 64 | 0.5166 | 0.3594 | 33.0643 | 0 | 0 | 30 | 0.8486 | 0.3000 | 25.4590 | 1d: frozen3.0 | 1d: none |
| P-WARN-1/scored | frozen3.0 | 1d | __ALL__ | 200 | 0.2096 | 0.3150 | 41.9232 | 0 | 0 | 77 | 0.5400 | 0.3247 | 41.5822 | 1d: frozen3.0 | 1d: none |
| P-WARN-1/scored | frozen3.0 | 1w | NONE | 37 | 0.5372 | 0.3784 | 19.8752 | 0 | 0 | 0 | — | — | — | 1w: frozen3.0 | 1w: none |
| P-WARN-1/scored | frozen3.0 | 1w | IN_RANGE | 29 | 0.2104 | 0.3103 | 6.1027 | 0 | 0 | 25 | 0.2752 | 0.3200 | 6.8809 | 1w: frozen3.0 | 1w: none |
| P-WARN-1/scored | frozen3.0 | 1w | BULL_EXP | 40 | 0.6876 | 0.2500 | 27.5056 | 0 | 0 | 20 | 1.8572 | 0.3500 | 37.1441 | 1w: frozen3.0 | 1w: none |
| P-WARN-1/scored | frozen3.0 | 1w | BEAR_EXP | 94 | -0.1230 | 0.3191 | -11.5602 | 0 | 0 | 32 | -0.0763 | 0.3125 | -2.4428 | 1w: frozen3.0 | 1w: none |
| P-WARN-1/scored | frozen3.0 | 1w | __ALL__ | 200 | 0.2096 | 0.3150 | 41.9232 | 0 | 0 | 77 | 0.5400 | 0.3247 | 41.5822 | 1w: frozen3.0 | 1w: none |
| P-AGE-1/scored | calibrated | 1h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-AGE-1/scored | calibrated | 1h | IN_RANGE | 90 | 0.4357 | 0.4222 | 39.2101 | 53 | 51 | 37 | 0.9741 | 0.5405 | 36.0428 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-AGE-1/scored | calibrated | 1h | BULL_EXP | 25 | 0.1157 | 0.3600 | 2.8913 | 17 | 16 | 8 | -0.3999 | 0.2500 | -3.1995 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-AGE-1/scored | calibrated | 1h | BEAR_EXP | 26 | 0.8216 | 0.3846 | 21.3627 | 11 | 14 | 15 | 1.2772 | 0.2667 | 19.1583 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-AGE-1/scored | calibrated | 1h | __ALL__ | 141 | 0.4501 | 0.4043 | 63.4641 | 81 | 81 | 60 | 0.8667 | 0.4333 | 52.0016 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-AGE-1/scored | calibrated | 4h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h: tuning | 4h: NEARUSDT |
| P-AGE-1/scored | calibrated | 4h | IN_RANGE | 102 | 0.3760 | 0.3922 | 38.3490 | 61 | 22 | 41 | 0.7179 | 0.4390 | 29.4336 | 4h: tuning | 4h: NEARUSDT |
| P-AGE-1/scored | calibrated | 4h | BULL_EXP | 23 | 1.0220 | 0.4348 | 23.5052 | 13 | 1 | 10 | 2.6571 | 0.5000 | 26.5711 | 4h: tuning | 4h: NEARUSDT |
| P-AGE-1/scored | calibrated | 4h | BEAR_EXP | 16 | 0.1006 | 0.4375 | 1.6099 | 7 | 6 | 9 | -0.4448 | 0.3333 | -4.0030 | 4h: tuning | 4h: NEARUSDT |
| P-AGE-1/scored | calibrated | 4h | __ALL__ | 141 | 0.4501 | 0.4043 | 63.4641 | 81 | 29 | 60 | 0.8667 | 0.4333 | 52.0016 | 4h: tuning | 4h: NEARUSDT |
| P-AGE-1/scored | calibrated | 12h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 12h | IN_RANGE | 77 | 0.3498 | 0.3896 | 26.9346 | 39 | 50 | 38 | 0.4144 | 0.3947 | 15.7457 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 12h | BULL_EXP | 36 | 0.8718 | 0.3889 | 31.3844 | 25 | 18 | 11 | 2.7061 | 0.3636 | 29.7669 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 12h | BEAR_EXP | 28 | 0.1838 | 0.4643 | 5.1451 | 17 | 15 | 11 | 0.5899 | 0.6364 | 6.4890 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 12h | __ALL__ | 141 | 0.4501 | 0.4043 | 63.4641 | 81 | 83 | 60 | 0.8667 | 0.4333 | 52.0016 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 1d | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 1d | IN_RANGE | 55 | 0.3942 | 0.4364 | 21.6834 | 26 | 20 | 29 | 0.5590 | 0.4483 | 16.2101 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 1d | BULL_EXP | 53 | 0.4052 | 0.4151 | 21.4770 | 38 | 18 | 15 | 1.3205 | 0.6000 | 19.8070 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 1d | BEAR_EXP | 33 | 0.6153 | 0.3333 | 20.3037 | 17 | 14 | 16 | 0.9990 | 0.2500 | 15.9845 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 1d | __ALL__ | 141 | 0.4501 | 0.4043 | 63.4641 | 81 | 52 | 60 | 0.8667 | 0.4333 | 52.0016 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 1w | NONE | 14 | 0.5837 | 0.4286 | 8.1714 | 14 | 0 | 0 | — | — | — | 1w: whole-tape (fallback) | 1w: none |
| P-AGE-1/scored | calibrated | 1w | IN_RANGE | 31 | 0.4455 | 0.4194 | 13.8091 | 31 | 0 | 25 | 0.3051 | 0.3600 | 7.6264 | 1w: whole-tape (fallback) | 1w: none |
| P-AGE-1/scored | calibrated | 1w | BULL_EXP | 19 | 2.3159 | 0.4737 | 44.0025 | 19 | 0 | 12 | 3.5117 | 0.5833 | 42.1404 | 1w: whole-tape (fallback) | 1w: none |
| P-AGE-1/scored | calibrated | 1w | BEAR_EXP | 77 | -0.0327 | 0.3766 | -2.5188 | 77 | 0 | 23 | 0.0972 | 0.4348 | 2.2348 | 1w: whole-tape (fallback) | 1w: none |
| P-AGE-1/scored | calibrated | 1w | __ALL__ | 141 | 0.4501 | 0.4043 | 63.4641 | 141 | 0 | 60 | 0.8667 | 0.4333 | 52.0016 | 1w: whole-tape (fallback) | 1w: none |
| P-AGE-1/scored | frozen3.0 | 1h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h: frozen3.0 | 1h: none |
| P-AGE-1/scored | frozen3.0 | 1h | IN_RANGE | 93 | 0.5569 | 0.3763 | 51.7933 | 0 | 0 | 42 | 1.2771 | 0.4524 | 53.6376 | 1h: frozen3.0 | 1h: none |
| P-AGE-1/scored | frozen3.0 | 1h | BULL_EXP | 23 | 0.0287 | 0.3913 | 0.6599 | 0 | 0 | 10 | -0.3419 | 0.2000 | -3.4193 | 1h: frozen3.0 | 1h: none |
| P-AGE-1/scored | frozen3.0 | 1h | BEAR_EXP | 25 | 0.4404 | 0.5200 | 11.0109 | 0 | 0 | 8 | 0.2229 | 0.6250 | 1.7833 | 1h: frozen3.0 | 1h: none |
| P-AGE-1/scored | frozen3.0 | 1h | __ALL__ | 141 | 0.4501 | 0.4043 | 63.4641 | 0 | 0 | 60 | 0.8667 | 0.4333 | 52.0016 | 1h: frozen3.0 | 1h: none |
| P-AGE-1/scored | frozen3.0 | 4h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h: frozen3.0 | 4h: none |
| P-AGE-1/scored | frozen3.0 | 4h | IN_RANGE | 72 | 0.4072 | 0.4028 | 29.3165 | 0 | 0 | 39 | 0.5714 | 0.4359 | 22.2861 | 4h: frozen3.0 | 4h: none |
| P-AGE-1/scored | frozen3.0 | 4h | BULL_EXP | 41 | 0.6729 | 0.3415 | 27.5904 | 0 | 0 | 13 | 2.4797 | 0.3846 | 32.2359 | 4h: frozen3.0 | 4h: none |
| P-AGE-1/scored | frozen3.0 | 4h | BEAR_EXP | 28 | 0.2342 | 0.5000 | 6.5573 | 0 | 0 | 8 | -0.3151 | 0.5000 | -2.5204 | 4h: frozen3.0 | 4h: none |
| P-AGE-1/scored | frozen3.0 | 4h | __ALL__ | 141 | 0.4501 | 0.4043 | 63.4641 | 0 | 0 | 60 | 0.8667 | 0.4333 | 52.0016 | 4h: frozen3.0 | 4h: none |
| P-AGE-1/scored | frozen3.0 | 12h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 12h: frozen3.0 | 12h: none |
| P-AGE-1/scored | frozen3.0 | 12h | IN_RANGE | 57 | 0.3667 | 0.4211 | 20.9031 | 0 | 0 | 29 | 0.5756 | 0.4483 | 16.6931 | 12h: frozen3.0 | 12h: none |
| P-AGE-1/scored | frozen3.0 | 12h | BULL_EXP | 50 | 0.9216 | 0.4600 | 46.0795 | 0 | 0 | 20 | 2.1109 | 0.5500 | 42.2182 | 12h: frozen3.0 | 12h: none |
| P-AGE-1/scored | frozen3.0 | 12h | BEAR_EXP | 34 | -0.1035 | 0.2941 | -3.5185 | 0 | 0 | 11 | -0.6281 | 0.1818 | -6.9096 | 12h: frozen3.0 | 12h: none |
| P-AGE-1/scored | frozen3.0 | 12h | __ALL__ | 141 | 0.4501 | 0.4043 | 63.4641 | 0 | 0 | 60 | 0.8667 | 0.4333 | 52.0016 | 12h: frozen3.0 | 12h: none |
| P-AGE-1/scored | frozen3.0 | 1d | NONE | 2 | 0.2629 | 0.5000 | 0.5258 | 0 | 0 | 0 | — | — | — | 1d: frozen3.0 | 1d: none |
| P-AGE-1/scored | frozen3.0 | 1d | IN_RANGE | 47 | 0.0330 | 0.4043 | 1.5495 | 0 | 0 | 26 | 0.1728 | 0.4615 | 4.4931 | 1d: frozen3.0 | 1d: none |
| P-AGE-1/scored | frozen3.0 | 1d | BULL_EXP | 48 | 0.6251 | 0.4167 | 30.0034 | 0 | 0 | 13 | 1.3148 | 0.3846 | 17.0927 | 1d: frozen3.0 | 1d: none |
| P-AGE-1/scored | frozen3.0 | 1d | BEAR_EXP | 44 | 0.7133 | 0.3864 | 31.3855 | 0 | 0 | 21 | 1.4484 | 0.4286 | 30.4159 | 1d: frozen3.0 | 1d: none |
| P-AGE-1/scored | frozen3.0 | 1d | __ALL__ | 141 | 0.4501 | 0.4043 | 63.4641 | 0 | 0 | 60 | 0.8667 | 0.4333 | 52.0016 | 1d: frozen3.0 | 1d: none |
| P-AGE-1/scored | frozen3.0 | 1w | NONE | 21 | 0.7704 | 0.4286 | 16.1778 | 0 | 0 | 0 | — | — | — | 1w: frozen3.0 | 1w: none |
| P-AGE-1/scored | frozen3.0 | 1w | IN_RANGE | 21 | 0.5020 | 0.3810 | 10.5422 | 0 | 0 | 19 | 0.5284 | 0.3684 | 10.0398 | 1w: frozen3.0 | 1w: none |
| P-AGE-1/scored | frozen3.0 | 1w | BULL_EXP | 27 | 1.3757 | 0.3704 | 37.1449 | 0 | 0 | 13 | 3.1605 | 0.5385 | 41.0862 | 1w: frozen3.0 | 1w: none |
| P-AGE-1/scored | frozen3.0 | 1w | BEAR_EXP | 72 | -0.0056 | 0.4167 | -0.4008 | 0 | 0 | 28 | 0.0313 | 0.4286 | 0.8756 | 1w: frozen3.0 | 1w: none |
| P-AGE-1/scored | frozen3.0 | 1w | __ALL__ | 141 | 0.4501 | 0.4043 | 63.4641 | 0 | 0 | 60 | 0.8667 | 0.4333 | 52.0016 | 1w: frozen3.0 | 1w: none |
| P-WIN-1/scored | calibrated | 1h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-WIN-1/scored | calibrated | 1h | IN_RANGE | 83 | 0.4312 | 0.4337 | 35.7877 | 51 | 41 | 32 | 0.8281 | 0.5000 | 26.5000 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-WIN-1/scored | calibrated | 1h | BULL_EXP | 27 | -0.1845 | 0.3333 | -4.9824 | 19 | 15 | 8 | -0.1891 | 0.3750 | -1.5128 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-WIN-1/scored | calibrated | 1h | BEAR_EXP | 27 | 0.7840 | 0.3704 | 21.1687 | 11 | 14 | 16 | 1.1853 | 0.2500 | 18.9643 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-WIN-1/scored | calibrated | 1h | __ALL__ | 137 | 0.3794 | 0.4015 | 51.9740 | 81 | 70 | 56 | 0.7848 | 0.4107 | 43.9515 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-WIN-1/scored | calibrated | 4h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h: tuning | 4h: NEARUSDT |
| P-WIN-1/scored | calibrated | 4h | IN_RANGE | 103 | 0.2584 | 0.3786 | 26.6147 | 62 | 22 | 41 | 0.4785 | 0.3902 | 19.6165 | 4h: tuning | 4h: NEARUSDT |
| P-WIN-1/scored | calibrated | 4h | BULL_EXP | 21 | 1.3863 | 0.5238 | 29.1120 | 13 | 1 | 8 | 3.4920 | 0.6250 | 27.9359 | 4h: tuning | 4h: NEARUSDT |
| P-WIN-1/scored | calibrated | 4h | BEAR_EXP | 13 | -0.2887 | 0.3846 | -3.7527 | 6 | 3 | 7 | -0.5144 | 0.2857 | -3.6010 | 4h: tuning | 4h: NEARUSDT |
| P-WIN-1/scored | calibrated | 4h | __ALL__ | 137 | 0.3794 | 0.4015 | 51.9740 | 81 | 26 | 56 | 0.7848 | 0.4107 | 43.9515 | 4h: tuning | 4h: NEARUSDT |
| P-WIN-1/scored | calibrated | 12h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 12h | IN_RANGE | 72 | 0.3654 | 0.3889 | 26.3086 | 36 | 47 | 36 | 0.4700 | 0.3889 | 16.9200 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 12h | BULL_EXP | 39 | 0.4052 | 0.3846 | 15.8023 | 29 | 22 | 10 | 2.1843 | 0.4000 | 21.8431 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 12h | BEAR_EXP | 26 | 0.3793 | 0.4615 | 9.8631 | 16 | 11 | 10 | 0.5188 | 0.5000 | 5.1884 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 12h | __ALL__ | 137 | 0.3794 | 0.4015 | 51.9740 | 81 | 80 | 56 | 0.7848 | 0.4107 | 43.9515 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 1d | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 1d | IN_RANGE | 46 | 0.4368 | 0.4348 | 20.0928 | 22 | 13 | 24 | 0.7813 | 0.4583 | 18.7521 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 1d | BULL_EXP | 57 | 0.0791 | 0.4035 | 4.5060 | 43 | 19 | 14 | 0.7208 | 0.5714 | 10.0907 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 1d | BEAR_EXP | 34 | 0.8052 | 0.3529 | 27.3752 | 16 | 12 | 18 | 0.8394 | 0.2222 | 15.1086 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 1d | __ALL__ | 137 | 0.3794 | 0.4015 | 51.9740 | 81 | 44 | 56 | 0.7848 | 0.4107 | 43.9515 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 1w | NONE | 21 | 0.5176 | 0.4286 | 10.8694 | 21 | 0 | 0 | — | — | — | 1w: whole-tape (fallback) | 1w: none |
| P-WIN-1/scored | calibrated | 1w | IN_RANGE | 30 | -0.0537 | 0.3667 | -1.6113 | 30 | 0 | 24 | -0.0487 | 0.3333 | -1.1700 | 1w: whole-tape (fallback) | 1w: none |
| P-WIN-1/scored | calibrated | 1w | BULL_EXP | 19 | 2.2644 | 0.4737 | 43.0245 | 19 | 0 | 13 | 3.2198 | 0.5385 | 41.8580 | 1w: whole-tape (fallback) | 1w: none |
| P-WIN-1/scored | calibrated | 1w | BEAR_EXP | 67 | -0.0046 | 0.3881 | -0.3086 | 67 | 0 | 19 | 0.1718 | 0.4211 | 3.2634 | 1w: whole-tape (fallback) | 1w: none |
| P-WIN-1/scored | calibrated | 1w | __ALL__ | 137 | 0.3794 | 0.4015 | 51.9740 | 137 | 0 | 56 | 0.7848 | 0.4107 | 43.9515 | 1w: whole-tape (fallback) | 1w: none |
| P-WIN-1/scored | frozen3.0 | 1h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h: frozen3.0 | 1h: none |
| P-WIN-1/scored | frozen3.0 | 1h | IN_RANGE | 97 | 0.4324 | 0.3711 | 41.9464 | 0 | 0 | 40 | 1.0705 | 0.4000 | 42.8208 | 1h: frozen3.0 | 1h: none |
| P-WIN-1/scored | frozen3.0 | 1h | BULL_EXP | 23 | 0.2216 | 0.4348 | 5.0975 | 0 | 0 | 10 | -0.1449 | 0.3000 | -1.4493 | 1h: frozen3.0 | 1h: none |
| P-WIN-1/scored | frozen3.0 | 1h | BEAR_EXP | 17 | 0.2900 | 0.5294 | 4.9301 | 0 | 0 | 6 | 0.4300 | 0.6667 | 2.5800 | 1h: frozen3.0 | 1h: none |
| P-WIN-1/scored | frozen3.0 | 1h | __ALL__ | 137 | 0.3794 | 0.4015 | 51.9740 | 0 | 0 | 56 | 0.7848 | 0.4107 | 43.9515 | 1h: frozen3.0 | 1h: none |
| P-WIN-1/scored | frozen3.0 | 4h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h: frozen3.0 | 4h: none |
| P-WIN-1/scored | frozen3.0 | 4h | IN_RANGE | 66 | 0.5961 | 0.4545 | 39.3420 | 0 | 0 | 35 | 0.7137 | 0.4571 | 24.9781 | 4h: frozen3.0 | 4h: none |
| P-WIN-1/scored | frozen3.0 | 4h | BULL_EXP | 47 | 0.2814 | 0.3191 | 13.2244 | 0 | 0 | 14 | 1.6371 | 0.3571 | 22.9199 | 4h: frozen3.0 | 4h: none |
| P-WIN-1/scored | frozen3.0 | 4h | BEAR_EXP | 24 | -0.0247 | 0.4167 | -0.5924 | 0 | 0 | 7 | -0.5638 | 0.2857 | -3.9466 | 4h: frozen3.0 | 4h: none |
| P-WIN-1/scored | frozen3.0 | 4h | __ALL__ | 137 | 0.3794 | 0.4015 | 51.9740 | 0 | 0 | 56 | 0.7848 | 0.4107 | 43.9515 | 4h: frozen3.0 | 4h: none |
| P-WIN-1/scored | frozen3.0 | 12h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 12h: frozen3.0 | 12h: none |
| P-WIN-1/scored | frozen3.0 | 12h | IN_RANGE | 48 | 0.4434 | 0.4375 | 21.2850 | 0 | 0 | 24 | 0.8127 | 0.4583 | 19.5056 | 12h: frozen3.0 | 12h: none |
| P-WIN-1/scored | frozen3.0 | 12h | BULL_EXP | 53 | 0.5522 | 0.4151 | 29.2640 | 0 | 0 | 19 | 1.7106 | 0.5263 | 32.5019 | 12h: frozen3.0 | 12h: none |
| P-WIN-1/scored | frozen3.0 | 12h | BEAR_EXP | 36 | 0.0396 | 0.3333 | 1.4249 | 0 | 0 | 13 | -0.6197 | 0.1538 | -8.0560 | 12h: frozen3.0 | 12h: none |
| P-WIN-1/scored | frozen3.0 | 12h | __ALL__ | 137 | 0.3794 | 0.4015 | 51.9740 | 0 | 0 | 56 | 0.7848 | 0.4107 | 43.9515 | 12h: frozen3.0 | 12h: none |
| P-WIN-1/scored | frozen3.0 | 1d | NONE | 3 | -0.1607 | 0.3333 | -0.4820 | 0 | 0 | 0 | — | — | — | 1d: frozen3.0 | 1d: none |
| P-WIN-1/scored | frozen3.0 | 1d | IN_RANGE | 40 | 0.0824 | 0.4000 | 3.2965 | 0 | 0 | 22 | 0.2725 | 0.4545 | 5.9945 | 1d: frozen3.0 | 1d: none |
| P-WIN-1/scored | frozen3.0 | 1d | BULL_EXP | 47 | 0.3787 | 0.3830 | 17.7983 | 0 | 0 | 12 | 1.4663 | 0.4167 | 17.5954 | 1d: frozen3.0 | 1d: none |
| P-WIN-1/scored | frozen3.0 | 1d | BEAR_EXP | 47 | 0.6673 | 0.4255 | 31.3612 | 0 | 0 | 22 | 0.9255 | 0.3636 | 20.3615 | 1d: frozen3.0 | 1d: none |
| P-WIN-1/scored | frozen3.0 | 1d | __ALL__ | 137 | 0.3794 | 0.4015 | 51.9740 | 0 | 0 | 56 | 0.7848 | 0.4107 | 43.9515 | 1d: frozen3.0 | 1d: none |
| P-WIN-1/scored | frozen3.0 | 1w | NONE | 24 | 0.3532 | 0.3750 | 8.4780 | 0 | 0 | 0 | — | — | — | 1w: frozen3.0 | 1w: none |
| P-WIN-1/scored | frozen3.0 | 1w | IN_RANGE | 21 | 0.0334 | 0.3333 | 0.7011 | 0 | 0 | 18 | 0.0691 | 0.3333 | 1.2435 | 1w: frozen3.0 | 1w: none |
| P-WIN-1/scored | frozen3.0 | 1w | BULL_EXP | 24 | 1.6336 | 0.4167 | 39.2069 | 0 | 0 | 14 | 2.9146 | 0.5000 | 40.8038 | 1w: frozen3.0 | 1w: none |
| P-WIN-1/scored | frozen3.0 | 1w | BEAR_EXP | 68 | 0.0528 | 0.4265 | 3.5881 | 0 | 0 | 24 | 0.0793 | 0.4167 | 1.9042 | 1w: frozen3.0 | 1w: none |
| P-WIN-1/scored | frozen3.0 | 1w | __ALL__ | 137 | 0.3794 | 0.4015 | 51.9740 | 0 | 0 | 56 | 0.7848 | 0.4107 | 43.9515 | 1w: frozen3.0 | 1w: none |
| P-BRK-4H/scored | calibrated | 1h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-BRK-4H/scored | calibrated | 1h | IN_RANGE | 145 | 0.0980 | 0.3655 | 14.2029 | 97 | 84 | 48 | 0.3639 | 0.3958 | 17.4648 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-BRK-4H/scored | calibrated | 1h | BULL_EXP | 95 | 0.0190 | 0.3684 | 1.8092 | 60 | 53 | 35 | 0.0310 | 0.4571 | 1.0837 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-BRK-4H/scored | calibrated | 1h | BEAR_EXP | 82 | 0.0021 | 0.3171 | 0.1733 | 53 | 50 | 29 | 0.2233 | 0.3103 | 6.4746 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-BRK-4H/scored | calibrated | 1h | __ALL__ | 322 | 0.0503 | 0.3540 | 16.1853 | 210 | 187 | 112 | 0.2234 | 0.3929 | 25.0231 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-BRK-4H/scored | calibrated | 4h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h: tuning | 4h: NEARUSDT |
| P-BRK-4H/scored | calibrated | 4h | IN_RANGE | 112 | 0.0594 | 0.3393 | 6.6497 | 77 | 32 | 35 | 0.3693 | 0.3429 | 12.9239 | 4h: tuning | 4h: NEARUSDT |
| P-BRK-4H/scored | calibrated | 4h | BULL_EXP | 103 | -0.0986 | 0.3786 | -10.1585 | 64 | 13 | 39 | -0.0494 | 0.4359 | -1.9266 | 4h: tuning | 4h: NEARUSDT |
| P-BRK-4H/scored | calibrated | 4h | BEAR_EXP | 107 | 0.1841 | 0.3458 | 19.6941 | 69 | 18 | 38 | 0.3691 | 0.3947 | 14.0258 | 4h: tuning | 4h: NEARUSDT |
| P-BRK-4H/scored | calibrated | 4h | __ALL__ | 322 | 0.0503 | 0.3540 | 16.1853 | 210 | 63 | 112 | 0.2234 | 0.3929 | 25.0231 | 4h: tuning | 4h: NEARUSDT |
| P-BRK-4H/scored | calibrated | 12h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 12h | IN_RANGE | 121 | 0.0873 | 0.3471 | 10.5647 | 74 | 74 | 47 | 0.4506 | 0.4468 | 21.1766 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 12h | BULL_EXP | 119 | 0.0452 | 0.3529 | 5.3754 | 86 | 71 | 33 | 0.1598 | 0.3030 | 5.2747 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 12h | BEAR_EXP | 82 | 0.0030 | 0.3659 | 0.2452 | 50 | 39 | 32 | -0.0446 | 0.4062 | -1.4282 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 12h | __ALL__ | 322 | 0.0503 | 0.3540 | 16.1853 | 210 | 184 | 112 | 0.2234 | 0.3929 | 25.0231 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 1d | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 1d | IN_RANGE | 102 | 0.2675 | 0.4020 | 27.2856 | 56 | 38 | 46 | 0.5113 | 0.5000 | 23.5201 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 1d | BULL_EXP | 141 | -0.0198 | 0.3404 | -2.7876 | 106 | 55 | 35 | 0.2663 | 0.3429 | 9.3210 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 1d | BEAR_EXP | 79 | -0.1052 | 0.3165 | -8.3127 | 48 | 31 | 31 | -0.2522 | 0.2903 | -7.8180 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 1d | __ALL__ | 322 | 0.0503 | 0.3540 | 16.1853 | 210 | 124 | 112 | 0.2234 | 0.3929 | 25.0231 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 1w | NONE | 43 | -0.2546 | 0.2558 | -10.9475 | 43 | 0 | 0 | — | — | — | 1w: whole-tape (fallback) | 1w: none |
| P-BRK-4H/scored | calibrated | 1w | IN_RANGE | 74 | 0.0947 | 0.3919 | 7.0081 | 74 | 0 | 45 | 0.1060 | 0.3778 | 4.7701 | 1w: whole-tape (fallback) | 1w: none |
| P-BRK-4H/scored | calibrated | 1w | BULL_EXP | 45 | 0.3564 | 0.3556 | 16.0365 | 45 | 0 | 30 | 0.6568 | 0.3667 | 19.7045 | 1w: whole-tape (fallback) | 1w: none |
| P-BRK-4H/scored | calibrated | 1w | BEAR_EXP | 160 | 0.0256 | 0.3625 | 4.0883 | 160 | 0 | 37 | 0.0148 | 0.4324 | 0.5485 | 1w: whole-tape (fallback) | 1w: none |
| P-BRK-4H/scored | calibrated | 1w | __ALL__ | 322 | 0.0503 | 0.3540 | 16.1853 | 322 | 0 | 112 | 0.2234 | 0.3929 | 25.0231 | 1w: whole-tape (fallback) | 1w: none |
| P-BRK-4H/scored | frozen3.0 | 1h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h: frozen3.0 | 1h: none |
| P-BRK-4H/scored | frozen3.0 | 1h | IN_RANGE | 137 | -0.0142 | 0.3431 | -1.9515 | 0 | 0 | 42 | 0.1314 | 0.4286 | 5.5195 | 1h: frozen3.0 | 1h: none |
| P-BRK-4H/scored | frozen3.0 | 1h | BULL_EXP | 105 | 0.0488 | 0.3238 | 5.1239 | 0 | 0 | 39 | 0.2847 | 0.3077 | 11.1020 | 1h: frozen3.0 | 1h: none |
| P-BRK-4H/scored | frozen3.0 | 1h | BEAR_EXP | 80 | 0.1627 | 0.4125 | 13.0129 | 0 | 0 | 31 | 0.2710 | 0.4516 | 8.4016 | 1h: frozen3.0 | 1h: none |
| P-BRK-4H/scored | frozen3.0 | 1h | __ALL__ | 322 | 0.0503 | 0.3540 | 16.1853 | 0 | 0 | 112 | 0.2234 | 0.3929 | 25.0231 | 1h: frozen3.0 | 1h: none |
| P-BRK-4H/scored | frozen3.0 | 4h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h: frozen3.0 | 4h: none |
| P-BRK-4H/scored | frozen3.0 | 4h | IN_RANGE | 56 | 0.2118 | 0.3571 | 11.8624 | 0 | 0 | 23 | 0.4485 | 0.3043 | 10.3145 | 4h: frozen3.0 | 4h: none |
| P-BRK-4H/scored | frozen3.0 | 4h | BULL_EXP | 149 | -0.0540 | 0.3356 | -8.0445 | 0 | 0 | 48 | 0.1594 | 0.4167 | 7.6515 | 4h: frozen3.0 | 4h: none |
| P-BRK-4H/scored | frozen3.0 | 4h | BEAR_EXP | 117 | 0.1057 | 0.3761 | 12.3674 | 0 | 0 | 41 | 0.1721 | 0.4146 | 7.0571 | 4h: frozen3.0 | 4h: none |
| P-BRK-4H/scored | frozen3.0 | 4h | __ALL__ | 322 | 0.0503 | 0.3540 | 16.1853 | 0 | 0 | 112 | 0.2234 | 0.3929 | 25.0231 | 4h: frozen3.0 | 4h: none |
| P-BRK-4H/scored | frozen3.0 | 12h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 12h: frozen3.0 | 12h: none |
| P-BRK-4H/scored | frozen3.0 | 12h | IN_RANGE | 119 | 0.1505 | 0.3866 | 17.9062 | 0 | 0 | 40 | 0.4190 | 0.4750 | 16.7589 | 12h: frozen3.0 | 12h: none |
| P-BRK-4H/scored | frozen3.0 | 12h | BULL_EXP | 127 | 0.0341 | 0.3465 | 4.3369 | 0 | 0 | 45 | 0.1768 | 0.3333 | 7.9562 | 12h: frozen3.0 | 12h: none |
| P-BRK-4H/scored | frozen3.0 | 12h | BEAR_EXP | 76 | -0.0797 | 0.3158 | -6.0577 | 0 | 0 | 27 | 0.0114 | 0.3704 | 0.3080 | 12h: frozen3.0 | 12h: none |
| P-BRK-4H/scored | frozen3.0 | 12h | __ALL__ | 322 | 0.0503 | 0.3540 | 16.1853 | 0 | 0 | 112 | 0.2234 | 0.3929 | 25.0231 | 12h: frozen3.0 | 12h: none |
| P-BRK-4H/scored | frozen3.0 | 1d | NONE | 6 | -0.3925 | 0.1667 | -2.3551 | 0 | 0 | 0 | — | — | — | 1d: frozen3.0 | 1d: none |
| P-BRK-4H/scored | frozen3.0 | 1d | IN_RANGE | 122 | -0.0473 | 0.3443 | -5.7707 | 0 | 0 | 48 | -0.1142 | 0.3750 | -5.4800 | 1d: frozen3.0 | 1d: none |
| P-BRK-4H/scored | frozen3.0 | 1d | BULL_EXP | 111 | 0.1006 | 0.3784 | 11.1685 | 0 | 0 | 30 | 0.5674 | 0.4000 | 17.0224 | 1d: frozen3.0 | 1d: none |
| P-BRK-4H/scored | frozen3.0 | 1d | BEAR_EXP | 83 | 0.1583 | 0.3494 | 13.1426 | 0 | 0 | 34 | 0.3965 | 0.4118 | 13.4808 | 1d: frozen3.0 | 1d: none |
| P-BRK-4H/scored | frozen3.0 | 1d | __ALL__ | 322 | 0.0503 | 0.3540 | 16.1853 | 0 | 0 | 112 | 0.2234 | 0.3929 | 25.0231 | 1d: frozen3.0 | 1d: none |
| P-BRK-4H/scored | frozen3.0 | 1w | NONE | 52 | -0.1939 | 0.2692 | -10.0804 | 0 | 0 | 0 | — | — | — | 1w: frozen3.0 | 1w: none |
| P-BRK-4H/scored | frozen3.0 | 1w | IN_RANGE | 45 | 0.1861 | 0.4222 | 8.3733 | 0 | 0 | 35 | 0.2626 | 0.4286 | 9.1910 | 1w: frozen3.0 | 1w: none |
| P-BRK-4H/scored | frozen3.0 | 1w | BULL_EXP | 64 | 0.1343 | 0.3125 | 8.5964 | 0 | 0 | 30 | 0.6542 | 0.3667 | 19.6271 | 1w: frozen3.0 | 1w: none |
| P-BRK-4H/scored | frozen3.0 | 1w | BEAR_EXP | 161 | 0.0577 | 0.3789 | 9.2961 | 0 | 0 | 47 | -0.0807 | 0.3830 | -3.7950 | 1w: frozen3.0 | 1w: none |
| P-BRK-4H/scored | frozen3.0 | 1w | __ALL__ | 322 | 0.0503 | 0.3540 | 16.1853 | 0 | 0 | 112 | 0.2234 | 0.3929 | 25.0231 | 1w: frozen3.0 | 1w: none |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h: tuning / whole-tape (fallback) | 1h: BTCUSDT,SOLUSDT,NEARUSDT,ENAUSDT,MNTUSDT_BYBIT,SUIUSDT,LTCUSDT,XMRUSDT,BNBUSDT,1000BONKUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | IN_RANGE | 344 | 0.0916 | 0.3488 | 31.5076 | 209 | 207 | 144 | 0.3972 | 0.3958 | 57.2012 | 1h: tuning / whole-tape (fallback) | 1h: BTCUSDT,SOLUSDT,NEARUSDT,ENAUSDT,MNTUSDT_BYBIT,SUIUSDT,LTCUSDT,XMRUSDT,BNBUSDT,1000BONKUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | BULL_EXP | 212 | 0.0737 | 0.3915 | 15.6214 | 120 | 124 | 103 | 0.1399 | 0.4369 | 14.4063 | 1h: tuning / whole-tape (fallback) | 1h: BTCUSDT,SOLUSDT,NEARUSDT,ENAUSDT,MNTUSDT_BYBIT,SUIUSDT,LTCUSDT,XMRUSDT,BNBUSDT,1000BONKUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | BEAR_EXP | 206 | 0.2045 | 0.3835 | 42.1196 | 125 | 128 | 87 | 0.3556 | 0.3563 | 30.9413 | 1h: tuning / whole-tape (fallback) | 1h: BTCUSDT,SOLUSDT,NEARUSDT,ENAUSDT,MNTUSDT_BYBIT,SUIUSDT,LTCUSDT,XMRUSDT,BNBUSDT,1000BONKUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | __ALL__ | 762 | 0.1171 | 0.3701 | 89.2486 | 454 | 459 | 334 | 0.3070 | 0.3982 | 102.5487 | 1h: tuning / whole-tape (fallback) | 1h: BTCUSDT,SOLUSDT,NEARUSDT,ENAUSDT,MNTUSDT_BYBIT,SUIUSDT,LTCUSDT,XMRUSDT,BNBUSDT,1000BONKUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h: tuning / whole-tape (fallback) | 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | IN_RANGE | 257 | 0.2064 | 0.4008 | 53.0486 | 168 | 119 | 94 | 0.7189 | 0.4681 | 67.5735 | 4h: tuning / whole-tape (fallback) | 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | BULL_EXP | 262 | 0.0391 | 0.3397 | 10.2528 | 153 | 86 | 117 | 0.0988 | 0.3333 | 11.5573 | 4h: tuning / whole-tape (fallback) | 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | BEAR_EXP | 243 | 0.1068 | 0.3704 | 25.9471 | 133 | 80 | 123 | 0.1904 | 0.4065 | 23.4180 | 4h: tuning / whole-tape (fallback) | 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | __ALL__ | 762 | 0.1171 | 0.3701 | 89.2486 | 454 | 285 | 334 | 0.3070 | 0.3982 | 102.5487 | 4h: tuning / whole-tape (fallback) | 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | IN_RANGE | 121 | 0.0873 | 0.3471 | 10.5647 | 74 | 74 | 47 | 0.4506 | 0.4468 | 21.1766 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | BULL_EXP | 119 | 0.0452 | 0.3529 | 5.3754 | 86 | 71 | 33 | 0.1598 | 0.3030 | 5.2747 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | BEAR_EXP | 82 | 0.0030 | 0.3659 | 0.2452 | 50 | 39 | 32 | -0.0446 | 0.4062 | -1.4282 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | NA | 440 | 0.1661 | 0.3818 | 73.0633 | 0 | 0 | 222 | 0.3492 | 0.4009 | 77.5256 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | __ALL__ | 762 | 0.1171 | 0.3701 | 89.2486 | 210 | 184 | 334 | 0.3070 | 0.3982 | 102.5487 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d: tuning / whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | IN_RANGE | 282 | 0.2222 | 0.4149 | 62.6535 | 182 | 115 | 130 | 0.4334 | 0.4846 | 56.3467 | 1d: tuning / whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | BULL_EXP | 276 | 0.0925 | 0.3514 | 25.5165 | 198 | 121 | 99 | 0.3482 | 0.3434 | 34.4718 | 1d: tuning / whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | BEAR_EXP | 204 | 0.0053 | 0.3333 | 1.0786 | 128 | 77 | 105 | 0.1117 | 0.3429 | 11.7303 | 1d: tuning / whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | __ALL__ | 762 | 0.1171 | 0.3701 | 89.2486 | 508 | 313 | 334 | 0.3070 | 0.3982 | 102.5487 | 1d: tuning / whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 1w | NONE | 43 | -0.2546 | 0.2558 | -10.9475 | 43 | 0 | 0 | — | — | — | 1w: whole-tape (fallback) | 1w: none |
| P-BRK-4H/tierE__panel17 | calibrated | 1w | IN_RANGE | 74 | 0.0947 | 0.3919 | 7.0081 | 74 | 0 | 45 | 0.1060 | 0.3778 | 4.7701 | 1w: whole-tape (fallback) | 1w: none |
| P-BRK-4H/tierE__panel17 | calibrated | 1w | BULL_EXP | 45 | 0.3564 | 0.3556 | 16.0365 | 45 | 0 | 30 | 0.6568 | 0.3667 | 19.7045 | 1w: whole-tape (fallback) | 1w: none |
| P-BRK-4H/tierE__panel17 | calibrated | 1w | BEAR_EXP | 160 | 0.0256 | 0.3625 | 4.0883 | 160 | 0 | 37 | 0.0148 | 0.4324 | 0.5485 | 1w: whole-tape (fallback) | 1w: none |
| P-BRK-4H/tierE__panel17 | calibrated | 1w | NA | 440 | 0.1661 | 0.3818 | 73.0633 | 0 | 0 | 222 | 0.3492 | 0.4009 | 77.5256 | 1w: whole-tape (fallback) | 1w: none |
| P-BRK-4H/tierE__panel17 | calibrated | 1w | __ALL__ | 762 | 0.1171 | 0.3701 | 89.2486 | 322 | 0 | 334 | 0.3070 | 0.3982 | 102.5487 | 1w: whole-tape (fallback) | 1w: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h: frozen3.0 | 1h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | IN_RANGE | 305 | 0.0340 | 0.3639 | 10.3847 | 0 | 0 | 116 | 0.3134 | 0.4310 | 36.3541 | 1h: frozen3.0 | 1h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | BULL_EXP | 259 | 0.1907 | 0.3591 | 49.3986 | 0 | 0 | 124 | 0.3344 | 0.3548 | 41.4677 | 1h: frozen3.0 | 1h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | BEAR_EXP | 198 | 0.1488 | 0.3939 | 29.4653 | 0 | 0 | 94 | 0.2631 | 0.4149 | 24.7269 | 1h: frozen3.0 | 1h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | __ALL__ | 762 | 0.1171 | 0.3701 | 89.2486 | 0 | 0 | 334 | 0.3070 | 0.3982 | 102.5487 | 1h: frozen3.0 | 1h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h: frozen3.0 | 4h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | IN_RANGE | 148 | 0.0192 | 0.3446 | 2.8401 | 0 | 0 | 59 | 0.2168 | 0.3559 | 12.7906 | 4h: frozen3.0 | 4h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | BULL_EXP | 335 | 0.0990 | 0.3612 | 33.1736 | 0 | 0 | 136 | 0.2613 | 0.3824 | 35.5318 | 4h: frozen3.0 | 4h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | BEAR_EXP | 279 | 0.1908 | 0.3943 | 53.2349 | 0 | 0 | 139 | 0.3901 | 0.4317 | 54.2263 | 4h: frozen3.0 | 4h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | __ALL__ | 762 | 0.1171 | 0.3701 | 89.2486 | 0 | 0 | 334 | 0.3070 | 0.3982 | 102.5487 | 4h: frozen3.0 | 4h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 12h: frozen3.0 | 12h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | IN_RANGE | 119 | 0.1505 | 0.3866 | 17.9062 | 0 | 0 | 40 | 0.4190 | 0.4750 | 16.7589 | 12h: frozen3.0 | 12h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | BULL_EXP | 127 | 0.0341 | 0.3465 | 4.3369 | 0 | 0 | 45 | 0.1768 | 0.3333 | 7.9562 | 12h: frozen3.0 | 12h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | BEAR_EXP | 76 | -0.0797 | 0.3158 | -6.0577 | 0 | 0 | 27 | 0.0114 | 0.3704 | 0.3080 | 12h: frozen3.0 | 12h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | NA | 440 | 0.1661 | 0.3818 | 73.0633 | 0 | 0 | 222 | 0.3492 | 0.4009 | 77.5256 | 12h: frozen3.0 | 12h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | __ALL__ | 762 | 0.1171 | 0.3701 | 89.2486 | 0 | 0 | 334 | 0.3070 | 0.3982 | 102.5487 | 12h: frozen3.0 | 12h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | NONE | 6 | -0.3925 | 0.1667 | -2.3551 | 0 | 0 | 0 | — | — | — | 1d: frozen3.0 | 1d: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | IN_RANGE | 276 | 0.1663 | 0.3877 | 45.8982 | 0 | 0 | 132 | 0.3556 | 0.4470 | 46.9451 | 1d: frozen3.0 | 1d: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | BULL_EXP | 247 | 0.0473 | 0.3522 | 11.6802 | 0 | 0 | 98 | 0.1925 | 0.3571 | 18.8656 | 1d: frozen3.0 | 1d: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | BEAR_EXP | 233 | 0.1460 | 0.3734 | 34.0253 | 0 | 0 | 104 | 0.3533 | 0.3750 | 36.7381 | 1d: frozen3.0 | 1d: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | __ALL__ | 762 | 0.1171 | 0.3701 | 89.2486 | 0 | 0 | 334 | 0.3070 | 0.3982 | 102.5487 | 1d: frozen3.0 | 1d: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1w | NONE | 52 | -0.1939 | 0.2692 | -10.0804 | 0 | 0 | 0 | — | — | — | 1w: frozen3.0 | 1w: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1w | IN_RANGE | 45 | 0.1861 | 0.4222 | 8.3733 | 0 | 0 | 35 | 0.2626 | 0.4286 | 9.1910 | 1w: frozen3.0 | 1w: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1w | BULL_EXP | 64 | 0.1343 | 0.3125 | 8.5964 | 0 | 0 | 30 | 0.6542 | 0.3667 | 19.6271 | 1w: frozen3.0 | 1w: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1w | BEAR_EXP | 161 | 0.0577 | 0.3789 | 9.2961 | 0 | 0 | 47 | -0.0807 | 0.3830 | -3.7950 | 1w: frozen3.0 | 1w: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1w | NA | 440 | 0.1661 | 0.3818 | 73.0633 | 0 | 0 | 222 | 0.3492 | 0.4009 | 77.5256 | 1w: frozen3.0 | 1w: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1w | __ALL__ | 762 | 0.1171 | 0.3701 | 89.2486 | 0 | 0 | 334 | 0.3070 | 0.3982 | 102.5487 | 1w: frozen3.0 | 1w: none |
| P-RELAY-1/scored | calibrated | 1h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-RELAY-1/scored | calibrated | 1h | IN_RANGE | 76 | 0.5428 | 0.3026 | 41.2550 | 55 | 49 | 21 | 1.1734 | 0.2857 | 24.6405 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-RELAY-1/scored | calibrated | 1h | BULL_EXP | 52 | 0.5953 | 0.3077 | 30.9574 | 34 | 31 | 18 | 0.8493 | 0.2778 | 15.2881 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-RELAY-1/scored | calibrated | 1h | BEAR_EXP | 45 | 0.1393 | 0.4444 | 6.2673 | 25 | 32 | 20 | 0.1233 | 0.4500 | 2.4655 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-RELAY-1/scored | calibrated | 1h | __ALL__ | 173 | 0.4536 | 0.3410 | 78.4797 | 114 | 112 | 59 | 0.7185 | 0.3390 | 42.3942 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-RELAY-1/scored | calibrated | 4h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h: tuning | 4h: NEARUSDT |
| P-RELAY-1/scored | calibrated | 4h | IN_RANGE | 110 | 0.7937 | 0.3455 | 87.3077 | 79 | 17 | 31 | 1.5627 | 0.3226 | 48.4450 | 4h: tuning | 4h: NEARUSDT |
| P-RELAY-1/scored | calibrated | 4h | BULL_EXP | 25 | 0.2762 | 0.4800 | 6.9061 | 14 | 5 | 11 | 0.3895 | 0.6364 | 4.2846 | 4h: tuning | 4h: NEARUSDT |
| P-RELAY-1/scored | calibrated | 4h | BEAR_EXP | 38 | -0.4141 | 0.2368 | -15.7341 | 21 | 10 | 17 | -0.6080 | 0.1765 | -10.3355 | 4h: tuning | 4h: NEARUSDT |
| P-RELAY-1/scored | calibrated | 4h | __ALL__ | 173 | 0.4536 | 0.3410 | 78.4797 | 114 | 32 | 59 | 0.7185 | 0.3390 | 42.3942 | 4h: tuning | 4h: NEARUSDT |
| P-RELAY-1/scored | calibrated | 12h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 12h | IN_RANGE | 95 | 0.8825 | 0.3158 | 83.8414 | 59 | 69 | 36 | 1.2731 | 0.3333 | 45.8319 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 12h | BULL_EXP | 42 | 0.1127 | 0.3810 | 4.7354 | 31 | 25 | 11 | 0.1695 | 0.4545 | 1.8645 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 12h | BEAR_EXP | 36 | -0.2805 | 0.3611 | -10.0971 | 24 | 19 | 12 | -0.4419 | 0.2500 | -5.3023 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 12h | __ALL__ | 173 | 0.4536 | 0.3410 | 78.4797 | 114 | 113 | 59 | 0.7185 | 0.3390 | 42.3942 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 1d | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 1d | IN_RANGE | 59 | 1.2669 | 0.4237 | 74.7481 | 37 | 27 | 22 | 1.2504 | 0.5000 | 27.5093 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 1d | BULL_EXP | 63 | 0.4231 | 0.3333 | 26.6559 | 46 | 28 | 17 | 1.6312 | 0.3529 | 27.7312 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 1d | BEAR_EXP | 51 | -0.4495 | 0.2549 | -22.9243 | 31 | 25 | 20 | -0.6423 | 0.1500 | -12.8464 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 1d | __ALL__ | 173 | 0.4536 | 0.3410 | 78.4797 | 114 | 80 | 59 | 0.7185 | 0.3390 | 42.3942 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 1w | NONE | 20 | 1.3172 | 0.3500 | 26.3447 | 20 | 0 | 0 | — | — | — | 1w: whole-tape (fallback) | 1w: none |
| P-RELAY-1/scored | calibrated | 1w | IN_RANGE | 39 | 1.5394 | 0.4359 | 60.0372 | 39 | 0 | 22 | 2.4804 | 0.4545 | 54.5693 | 1w: whole-tape (fallback) | 1w: none |
| P-RELAY-1/scored | calibrated | 1w | BULL_EXP | 28 | -0.1061 | 0.3571 | -2.9706 | 28 | 0 | 17 | -0.2959 | 0.3529 | -5.0300 | 1w: whole-tape (fallback) | 1w: none |
| P-RELAY-1/scored | calibrated | 1w | BEAR_EXP | 86 | -0.0573 | 0.2907 | -4.9316 | 86 | 0 | 20 | -0.3573 | 0.2000 | -7.1452 | 1w: whole-tape (fallback) | 1w: none |
| P-RELAY-1/scored | calibrated | 1w | __ALL__ | 173 | 0.4536 | 0.3410 | 78.4797 | 173 | 0 | 59 | 0.7185 | 0.3390 | 42.3942 | 1w: whole-tape (fallback) | 1w: none |
| P-RELAY-1/scored | frozen3.0 | 1h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h: frozen3.0 | 1h: none |
| P-RELAY-1/scored | frozen3.0 | 1h | IN_RANGE | 87 | 0.7939 | 0.3333 | 69.0689 | 0 | 0 | 26 | 1.0206 | 0.3077 | 26.5355 | 1h: frozen3.0 | 1h: none |
| P-RELAY-1/scored | frozen3.0 | 1h | BULL_EXP | 49 | 0.3378 | 0.3265 | 16.5532 | 0 | 0 | 15 | 0.9712 | 0.2667 | 14.5680 | 1h: frozen3.0 | 1h: none |
| P-RELAY-1/scored | frozen3.0 | 1h | BEAR_EXP | 37 | -0.1930 | 0.3784 | -7.1424 | 0 | 0 | 18 | 0.0717 | 0.4444 | 1.2906 | 1h: frozen3.0 | 1h: none |
| P-RELAY-1/scored | frozen3.0 | 1h | __ALL__ | 173 | 0.4536 | 0.3410 | 78.4797 | 0 | 0 | 59 | 0.7185 | 0.3390 | 42.3942 | 1h: frozen3.0 | 1h: none |
| P-RELAY-1/scored | frozen3.0 | 4h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h: frozen3.0 | 4h: none |
| P-RELAY-1/scored | frozen3.0 | 4h | IN_RANGE | 84 | 0.5530 | 0.3810 | 46.4508 | 0 | 0 | 32 | -0.0478 | 0.3438 | -1.5305 | 4h: frozen3.0 | 4h: none |
| P-RELAY-1/scored | frozen3.0 | 4h | BULL_EXP | 46 | 0.7786 | 0.3696 | 35.8154 | 0 | 0 | 12 | 2.8597 | 0.5000 | 34.3163 | 4h: frozen3.0 | 4h: none |
| P-RELAY-1/scored | frozen3.0 | 4h | BEAR_EXP | 43 | -0.0881 | 0.2326 | -3.7864 | 0 | 0 | 15 | 0.6406 | 0.2000 | 9.6084 | 4h: frozen3.0 | 4h: none |
| P-RELAY-1/scored | frozen3.0 | 4h | __ALL__ | 173 | 0.4536 | 0.3410 | 78.4797 | 0 | 0 | 59 | 0.7185 | 0.3390 | 42.3942 | 4h: frozen3.0 | 4h: none |
| P-RELAY-1/scored | frozen3.0 | 12h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 12h: frozen3.0 | 12h: none |
| P-RELAY-1/scored | frozen3.0 | 12h | IN_RANGE | 64 | 1.0161 | 0.3750 | 65.0327 | 0 | 0 | 23 | 0.9291 | 0.3913 | 21.3701 | 12h: frozen3.0 | 12h: none |
| P-RELAY-1/scored | frozen3.0 | 12h | BULL_EXP | 65 | 0.3959 | 0.3077 | 25.7336 | 0 | 0 | 22 | 1.2688 | 0.3636 | 27.9139 | 12h: frozen3.0 | 12h: none |
| P-RELAY-1/scored | frozen3.0 | 12h | BEAR_EXP | 44 | -0.2792 | 0.3409 | -12.2866 | 0 | 0 | 14 | -0.4921 | 0.2143 | -6.8899 | 12h: frozen3.0 | 12h: none |
| P-RELAY-1/scored | frozen3.0 | 12h | __ALL__ | 173 | 0.4536 | 0.3410 | 78.4797 | 0 | 0 | 59 | 0.7185 | 0.3390 | 42.3942 | 12h: frozen3.0 | 12h: none |
| P-RELAY-1/scored | frozen3.0 | 1d | NONE | 3 | -0.6816 | 0.0000 | -2.0449 | 0 | 0 | 0 | — | — | — | 1d: frozen3.0 | 1d: none |
| P-RELAY-1/scored | frozen3.0 | 1d | IN_RANGE | 57 | 0.3888 | 0.3684 | 22.1628 | 0 | 0 | 19 | 0.3376 | 0.3684 | 6.4151 | 1d: frozen3.0 | 1d: none |
| P-RELAY-1/scored | frozen3.0 | 1d | BULL_EXP | 66 | -0.0604 | 0.3636 | -3.9858 | 0 | 0 | 20 | -0.2503 | 0.3500 | -5.0051 | 1d: frozen3.0 | 1d: none |
| P-RELAY-1/scored | frozen3.0 | 1d | BEAR_EXP | 47 | 1.3265 | 0.2979 | 62.3477 | 0 | 0 | 20 | 2.0492 | 0.3000 | 40.9842 | 1d: frozen3.0 | 1d: none |
| P-RELAY-1/scored | frozen3.0 | 1d | __ALL__ | 173 | 0.4536 | 0.3410 | 78.4797 | 0 | 0 | 59 | 0.7185 | 0.3390 | 42.3942 | 1d: frozen3.0 | 1d: none |
| P-RELAY-1/scored | frozen3.0 | 1w | NONE | 26 | 0.9150 | 0.3462 | 23.7909 | 0 | 0 | 0 | — | — | — | 1w: frozen3.0 | 1w: none |
| P-RELAY-1/scored | frozen3.0 | 1w | IN_RANGE | 24 | 2.2470 | 0.4583 | 53.9282 | 0 | 0 | 19 | 3.0208 | 0.5263 | 57.3947 | 1w: frozen3.0 | 1w: none |
| P-RELAY-1/scored | frozen3.0 | 1w | BULL_EXP | 43 | -0.2227 | 0.3023 | -9.5753 | 0 | 0 | 19 | -0.3594 | 0.3158 | -6.8277 | 1w: frozen3.0 | 1w: none |
| P-RELAY-1/scored | frozen3.0 | 1w | BEAR_EXP | 80 | 0.1292 | 0.3250 | 10.3359 | 0 | 0 | 21 | -0.3892 | 0.1905 | -8.1729 | 1w: frozen3.0 | 1w: none |
| P-RELAY-1/scored | frozen3.0 | 1w | __ALL__ | 173 | 0.4536 | 0.3410 | 78.4797 | 0 | 0 | 59 | 0.7185 | 0.3390 | 42.3942 | 1w: frozen3.0 | 1w: none |
| P-ADD-BRK/scored | calibrated | 1h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-ADD-BRK/scored | calibrated | 1h | IN_RANGE | 126 | 0.2177 | 0.3254 | 27.4293 | 79 | 73 | 47 | 0.6322 | 0.3404 | 29.7120 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-ADD-BRK/scored | calibrated | 1h | BULL_EXP | 38 | -0.2268 | 0.2368 | -8.6181 | 27 | 23 | 11 | -0.5376 | 0.1818 | -5.9138 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-ADD-BRK/scored | calibrated | 1h | BEAR_EXP | 36 | 0.4989 | 0.3333 | 17.9596 | 17 | 19 | 19 | 0.7814 | 0.2632 | 14.8470 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-ADD-BRK/scored | calibrated | 1h | __ALL__ | 200 | 0.1839 | 0.3100 | 36.7709 | 123 | 115 | 77 | 0.5019 | 0.2987 | 38.6452 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-ADD-BRK/scored | calibrated | 4h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h: tuning | 4h: NEARUSDT |
| P-ADD-BRK/scored | calibrated | 4h | IN_RANGE | 141 | 0.2087 | 0.3191 | 29.4309 | 88 | 31 | 53 | 0.5171 | 0.3208 | 27.4070 | 4h: tuning | 4h: NEARUSDT |
| P-ADD-BRK/scored | calibrated | 4h | BULL_EXP | 32 | 0.4863 | 0.3438 | 15.5613 | 20 | 1 | 12 | 1.7676 | 0.3333 | 21.2117 | 4h: tuning | 4h: NEARUSDT |
| P-ADD-BRK/scored | calibrated | 4h | BEAR_EXP | 27 | -0.3045 | 0.2222 | -8.2213 | 15 | 8 | 12 | -0.8311 | 0.1667 | -9.9734 | 4h: tuning | 4h: NEARUSDT |
| P-ADD-BRK/scored | calibrated | 4h | __ALL__ | 200 | 0.1839 | 0.3100 | 36.7709 | 123 | 40 | 77 | 0.5019 | 0.2987 | 38.6452 | 4h: tuning | 4h: NEARUSDT |
| P-ADD-BRK/scored | calibrated | 12h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 12h | IN_RANGE | 103 | 0.1494 | 0.3010 | 15.3913 | 54 | 74 | 49 | 0.1894 | 0.3061 | 9.2805 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 12h | BULL_EXP | 58 | 0.2750 | 0.3276 | 15.9512 | 45 | 32 | 13 | 2.0147 | 0.3077 | 26.1905 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 12h | BEAR_EXP | 39 | 0.1392 | 0.3077 | 5.4283 | 24 | 17 | 15 | 0.2116 | 0.2667 | 3.1742 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 12h | __ALL__ | 200 | 0.1839 | 0.3100 | 36.7709 | 123 | 123 | 77 | 0.5019 | 0.2987 | 38.6452 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 1d | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 1d | IN_RANGE | 73 | 0.1415 | 0.3014 | 10.3328 | 38 | 27 | 35 | 0.3003 | 0.2857 | 10.5088 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 1d | BULL_EXP | 77 | 0.0671 | 0.3247 | 5.1667 | 59 | 29 | 18 | 1.0796 | 0.4444 | 19.4330 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 1d | BEAR_EXP | 50 | 0.4254 | 0.3000 | 21.2714 | 26 | 19 | 24 | 0.3626 | 0.2083 | 8.7034 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 1d | __ALL__ | 200 | 0.1839 | 0.3100 | 36.7709 | 123 | 75 | 77 | 0.5019 | 0.2987 | 38.6452 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 1w | NONE | 30 | 0.2856 | 0.3333 | 8.5691 | 30 | 0 | 0 | — | — | — | 1w: whole-tape (fallback) | 1w: none |
| P-ADD-BRK/scored | calibrated | 1w | IN_RANGE | 43 | 0.2433 | 0.3023 | 10.4603 | 43 | 0 | 31 | 0.2007 | 0.2581 | 6.2205 | 1w: whole-tape (fallback) | 1w: none |
| P-ADD-BRK/scored | calibrated | 1w | BULL_EXP | 29 | 1.2746 | 0.3448 | 36.9625 | 29 | 0 | 19 | 2.0525 | 0.4211 | 38.9975 | 1w: whole-tape (fallback) | 1w: none |
| P-ADD-BRK/scored | calibrated | 1w | BEAR_EXP | 98 | -0.1961 | 0.2959 | -19.2210 | 98 | 0 | 27 | -0.2434 | 0.2593 | -6.5727 | 1w: whole-tape (fallback) | 1w: none |
| P-ADD-BRK/scored | calibrated | 1w | __ALL__ | 200 | 0.1839 | 0.3100 | 36.7709 | 200 | 0 | 77 | 0.5019 | 0.2987 | 38.6452 | 1w: whole-tape (fallback) | 1w: none |
| P-ADD-BRK/scored | frozen3.0 | 1h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h: frozen3.0 | 1h: none |
| P-ADD-BRK/scored | frozen3.0 | 1h | IN_RANGE | 127 | 0.2510 | 0.2913 | 31.8792 | 0 | 0 | 49 | 0.9783 | 0.3265 | 47.9344 | 1h: frozen3.0 | 1h: none |
| P-ADD-BRK/scored | frozen3.0 | 1h | BULL_EXP | 41 | -0.0763 | 0.3171 | -3.1302 | 0 | 0 | 17 | -0.4560 | 0.1765 | -7.7515 | 1h: frozen3.0 | 1h: none |
| P-ADD-BRK/scored | frozen3.0 | 1h | BEAR_EXP | 32 | 0.2507 | 0.3750 | 8.0219 | 0 | 0 | 11 | -0.1398 | 0.3636 | -1.5376 | 1h: frozen3.0 | 1h: none |
| P-ADD-BRK/scored | frozen3.0 | 1h | __ALL__ | 200 | 0.1839 | 0.3100 | 36.7709 | 0 | 0 | 77 | 0.5019 | 0.2987 | 38.6452 | 1h: frozen3.0 | 1h: none |
| P-ADD-BRK/scored | frozen3.0 | 4h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h: frozen3.0 | 4h: none |
| P-ADD-BRK/scored | frozen3.0 | 4h | IN_RANGE | 94 | 0.3454 | 0.3617 | 32.4646 | 0 | 0 | 45 | 0.4938 | 0.3778 | 22.2227 | 4h: frozen3.0 | 4h: none |
| P-ADD-BRK/scored | frozen3.0 | 4h | BULL_EXP | 66 | 0.0749 | 0.2576 | 4.9457 | 0 | 0 | 19 | 1.3650 | 0.2632 | 25.9353 | 4h: frozen3.0 | 4h: none |
| P-ADD-BRK/scored | frozen3.0 | 4h | BEAR_EXP | 40 | -0.0160 | 0.2750 | -0.6394 | 0 | 0 | 13 | -0.7318 | 0.0769 | -9.5128 | 4h: frozen3.0 | 4h: none |
| P-ADD-BRK/scored | frozen3.0 | 4h | __ALL__ | 200 | 0.1839 | 0.3100 | 36.7709 | 0 | 0 | 77 | 0.5019 | 0.2987 | 38.6452 | 4h: frozen3.0 | 4h: none |
| P-ADD-BRK/scored | frozen3.0 | 12h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 12h: frozen3.0 | 12h: none |
| P-ADD-BRK/scored | frozen3.0 | 12h | IN_RANGE | 74 | 0.1558 | 0.2973 | 11.5326 | 0 | 0 | 36 | 0.2824 | 0.2778 | 10.1647 | 12h: frozen3.0 | 12h: none |
| P-ADD-BRK/scored | frozen3.0 | 12h | BULL_EXP | 76 | 0.3628 | 0.3553 | 27.5715 | 0 | 0 | 24 | 1.6794 | 0.4583 | 40.3068 | 12h: frozen3.0 | 12h: none |
| P-ADD-BRK/scored | frozen3.0 | 12h | BEAR_EXP | 50 | -0.0467 | 0.2600 | -2.3332 | 0 | 0 | 17 | -0.6957 | 0.1176 | -11.8262 | 12h: frozen3.0 | 12h: none |
| P-ADD-BRK/scored | frozen3.0 | 12h | __ALL__ | 200 | 0.1839 | 0.3100 | 36.7709 | 0 | 0 | 77 | 0.5019 | 0.2987 | 38.6452 | 12h: frozen3.0 | 12h: none |
| P-ADD-BRK/scored | frozen3.0 | 1d | NONE | 4 | -1.0416 | 0.2500 | -4.1664 | 0 | 0 | 0 | — | — | — | 1d: frozen3.0 | 1d: none |
| P-ADD-BRK/scored | frozen3.0 | 1d | IN_RANGE | 58 | -0.1749 | 0.2586 | -10.1453 | 0 | 0 | 28 | 0.0725 | 0.3214 | 2.0299 | 1d: frozen3.0 | 1d: none |
| P-ADD-BRK/scored | frozen3.0 | 1d | BULL_EXP | 74 | 0.2914 | 0.3378 | 21.5611 | 0 | 0 | 19 | 0.9011 | 0.3158 | 17.1207 | 1d: frozen3.0 | 1d: none |
| P-ADD-BRK/scored | frozen3.0 | 1d | BEAR_EXP | 64 | 0.4613 | 0.3281 | 29.5214 | 0 | 0 | 30 | 0.6498 | 0.2667 | 19.4947 | 1d: frozen3.0 | 1d: none |
| P-ADD-BRK/scored | frozen3.0 | 1d | __ALL__ | 200 | 0.1839 | 0.3100 | 36.7709 | 0 | 0 | 77 | 0.5019 | 0.2987 | 38.6452 | 1d: frozen3.0 | 1d: none |
| P-ADD-BRK/scored | frozen3.0 | 1w | NONE | 37 | 0.5075 | 0.3514 | 18.7771 | 0 | 0 | 0 | — | — | — | 1w: frozen3.0 | 1w: none |
| P-ADD-BRK/scored | frozen3.0 | 1w | IN_RANGE | 29 | 0.2261 | 0.2414 | 6.5562 | 0 | 0 | 25 | 0.3315 | 0.2400 | 8.2866 | 1w: frozen3.0 | 1w: none |
| P-ADD-BRK/scored | frozen3.0 | 1w | BULL_EXP | 40 | 0.6737 | 0.2750 | 26.9494 | 0 | 0 | 20 | 1.8972 | 0.4000 | 37.9433 | 1w: frozen3.0 | 1w: none |
| P-ADD-BRK/scored | frozen3.0 | 1w | BEAR_EXP | 94 | -0.1650 | 0.3298 | -15.5118 | 0 | 0 | 32 | -0.2370 | 0.2812 | -7.5846 | 1w: frozen3.0 | 1w: none |
| P-ADD-BRK/scored | frozen3.0 | 1w | __ALL__ | 200 | 0.1839 | 0.3100 | 36.7709 | 0 | 0 | 77 | 0.5019 | 0.2987 | 38.6452 | 1w: frozen3.0 | 1w: none |
| P-ADD-SFP/scored | calibrated | 1h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-ADD-SFP/scored | calibrated | 1h | IN_RANGE | 126 | 0.1942 | 0.3571 | 24.4696 | 79 | 73 | 47 | 0.5515 | 0.4043 | 25.9225 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-ADD-SFP/scored | calibrated | 1h | BULL_EXP | 38 | -0.1859 | 0.2632 | -7.0629 | 27 | 23 | 11 | -0.3883 | 0.2727 | -4.2718 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-ADD-SFP/scored | calibrated | 1h | BEAR_EXP | 36 | 0.5390 | 0.3611 | 19.4053 | 17 | 19 | 19 | 0.9465 | 0.2632 | 17.9836 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-ADD-SFP/scored | calibrated | 1h | __ALL__ | 200 | 0.1841 | 0.3400 | 36.8120 | 123 | 115 | 77 | 0.5147 | 0.3506 | 39.6344 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-ADD-SFP/scored | calibrated | 4h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h: tuning | 4h: NEARUSDT |
| P-ADD-SFP/scored | calibrated | 4h | IN_RANGE | 141 | 0.1480 | 0.3333 | 20.8610 | 88 | 31 | 53 | 0.3795 | 0.3396 | 20.1138 | 4h: tuning | 4h: NEARUSDT |
| P-ADD-SFP/scored | calibrated | 4h | BULL_EXP | 32 | 0.6863 | 0.4062 | 21.9607 | 20 | 1 | 12 | 2.1366 | 0.5000 | 25.6395 | 4h: tuning | 4h: NEARUSDT |
| P-ADD-SFP/scored | calibrated | 4h | BEAR_EXP | 27 | -0.2226 | 0.2963 | -6.0097 | 15 | 8 | 12 | -0.5099 | 0.2500 | -6.1189 | 4h: tuning | 4h: NEARUSDT |
| P-ADD-SFP/scored | calibrated | 4h | __ALL__ | 200 | 0.1841 | 0.3400 | 36.8120 | 123 | 40 | 77 | 0.5147 | 0.3506 | 39.6344 | 4h: tuning | 4h: NEARUSDT |
| P-ADD-SFP/scored | calibrated | 12h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 12h | IN_RANGE | 103 | 0.1185 | 0.3204 | 12.2073 | 54 | 74 | 49 | 0.1645 | 0.3265 | 8.0589 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 12h | BULL_EXP | 58 | 0.4018 | 0.3621 | 23.3021 | 45 | 32 | 13 | 2.1819 | 0.3846 | 28.3648 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 12h | BEAR_EXP | 39 | 0.0334 | 0.3590 | 1.3026 | 24 | 17 | 15 | 0.2140 | 0.4000 | 3.2107 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 12h | __ALL__ | 200 | 0.1841 | 0.3400 | 36.8120 | 123 | 123 | 77 | 0.5147 | 0.3506 | 39.6344 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 1d | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 1d | IN_RANGE | 73 | 0.1446 | 0.3425 | 10.5590 | 38 | 27 | 35 | 0.2936 | 0.3429 | 10.2757 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 1d | BULL_EXP | 77 | 0.0694 | 0.3506 | 5.3438 | 59 | 29 | 18 | 0.9553 | 0.5556 | 17.1960 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 1d | BEAR_EXP | 50 | 0.4182 | 0.3200 | 20.9091 | 26 | 19 | 24 | 0.5068 | 0.2083 | 12.1627 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 1d | __ALL__ | 200 | 0.1841 | 0.3400 | 36.8120 | 123 | 75 | 77 | 0.5147 | 0.3506 | 39.6344 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 1w | NONE | 30 | 0.3101 | 0.4000 | 9.3026 | 30 | 0 | 0 | — | — | — | 1w: whole-tape (fallback) | 1w: none |
| P-ADD-SFP/scored | calibrated | 1w | IN_RANGE | 43 | 0.1365 | 0.3488 | 5.8704 | 43 | 0 | 31 | 0.0866 | 0.3226 | 2.6832 | 1w: whole-tape (fallback) | 1w: none |
| P-ADD-SFP/scored | calibrated | 1w | BULL_EXP | 29 | 1.2890 | 0.3448 | 37.3804 | 29 | 0 | 19 | 2.0144 | 0.4211 | 38.2744 | 1w: whole-tape (fallback) | 1w: none |
| P-ADD-SFP/scored | calibrated | 1w | BEAR_EXP | 98 | -0.1606 | 0.3163 | -15.7414 | 98 | 0 | 27 | -0.0490 | 0.3333 | -1.3232 | 1w: whole-tape (fallback) | 1w: none |
| P-ADD-SFP/scored | calibrated | 1w | __ALL__ | 200 | 0.1841 | 0.3400 | 36.8120 | 200 | 0 | 77 | 0.5147 | 0.3506 | 39.6344 | 1w: whole-tape (fallback) | 1w: none |
| P-ADD-SFP/scored | frozen3.0 | 1h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h: frozen3.0 | 1h: none |
| P-ADD-SFP/scored | frozen3.0 | 1h | IN_RANGE | 127 | 0.2508 | 0.3150 | 31.8458 | 0 | 0 | 49 | 0.9318 | 0.3673 | 45.6599 | 1h: frozen3.0 | 1h: none |
| P-ADD-SFP/scored | frozen3.0 | 1h | BULL_EXP | 41 | -0.0393 | 0.3415 | -1.6103 | 0 | 0 | 17 | -0.3354 | 0.2353 | -5.7026 | 1h: frozen3.0 | 1h: none |
| P-ADD-SFP/scored | frozen3.0 | 1h | BEAR_EXP | 32 | 0.2055 | 0.4375 | 6.5765 | 0 | 0 | 11 | -0.0294 | 0.4545 | -0.3230 | 1h: frozen3.0 | 1h: none |
| P-ADD-SFP/scored | frozen3.0 | 1h | __ALL__ | 200 | 0.1841 | 0.3400 | 36.8120 | 0 | 0 | 77 | 0.5147 | 0.3506 | 39.6344 | 1h: frozen3.0 | 1h: none |
| P-ADD-SFP/scored | frozen3.0 | 4h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h: frozen3.0 | 4h: none |
| P-ADD-SFP/scored | frozen3.0 | 4h | IN_RANGE | 94 | 0.2571 | 0.3617 | 24.1686 | 0 | 0 | 45 | 0.3962 | 0.3778 | 17.8301 | 4h: frozen3.0 | 4h: none |
| P-ADD-SFP/scored | frozen3.0 | 4h | BULL_EXP | 66 | 0.2047 | 0.2879 | 13.5113 | 0 | 0 | 19 | 1.4437 | 0.3158 | 27.4307 | 4h: frozen3.0 | 4h: none |
| P-ADD-SFP/scored | frozen3.0 | 4h | BEAR_EXP | 40 | -0.0217 | 0.3750 | -0.8679 | 0 | 0 | 13 | -0.4328 | 0.3077 | -5.6264 | 4h: frozen3.0 | 4h: none |
| P-ADD-SFP/scored | frozen3.0 | 4h | __ALL__ | 200 | 0.1841 | 0.3400 | 36.8120 | 0 | 0 | 77 | 0.5147 | 0.3506 | 39.6344 | 4h: frozen3.0 | 4h: none |
| P-ADD-SFP/scored | frozen3.0 | 12h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 12h: frozen3.0 | 12h: none |
| P-ADD-SFP/scored | frozen3.0 | 12h | IN_RANGE | 74 | 0.1446 | 0.3378 | 10.7011 | 0 | 0 | 36 | 0.2898 | 0.3333 | 10.4334 | 12h: frozen3.0 | 12h: none |
| P-ADD-SFP/scored | frozen3.0 | 12h | BULL_EXP | 76 | 0.4251 | 0.3816 | 32.3057 | 0 | 0 | 24 | 1.6882 | 0.5417 | 40.5159 | 12h: frozen3.0 | 12h: none |
| P-ADD-SFP/scored | frozen3.0 | 12h | BEAR_EXP | 50 | -0.1239 | 0.2800 | -6.1949 | 0 | 0 | 17 | -0.6656 | 0.1176 | -11.3149 | 12h: frozen3.0 | 12h: none |
| P-ADD-SFP/scored | frozen3.0 | 12h | __ALL__ | 200 | 0.1841 | 0.3400 | 36.8120 | 0 | 0 | 77 | 0.5147 | 0.3506 | 39.6344 | 12h: frozen3.0 | 12h: none |
| P-ADD-SFP/scored | frozen3.0 | 1d | NONE | 4 | -0.4412 | 0.2500 | -1.7647 | 0 | 0 | 0 | — | — | — | 1d: frozen3.0 | 1d: none |
| P-ADD-SFP/scored | frozen3.0 | 1d | IN_RANGE | 58 | -0.1681 | 0.3103 | -9.7486 | 0 | 0 | 28 | 0.0662 | 0.3929 | 1.8531 | 1d: frozen3.0 | 1d: none |
| P-ADD-SFP/scored | frozen3.0 | 1d | BULL_EXP | 74 | 0.2496 | 0.3514 | 18.4714 | 0 | 0 | 19 | 0.7641 | 0.3684 | 14.5170 | 1d: frozen3.0 | 1d: none |
| P-ADD-SFP/scored | frozen3.0 | 1d | BEAR_EXP | 64 | 0.4665 | 0.3594 | 29.8539 | 0 | 0 | 30 | 0.7755 | 0.3000 | 23.2642 | 1d: frozen3.0 | 1d: none |
| P-ADD-SFP/scored | frozen3.0 | 1d | __ALL__ | 200 | 0.1841 | 0.3400 | 36.8120 | 0 | 0 | 77 | 0.5147 | 0.3506 | 39.6344 | 1d: frozen3.0 | 1d: none |
| P-ADD-SFP/scored | frozen3.0 | 1w | NONE | 37 | 0.4678 | 0.4054 | 17.3091 | 0 | 0 | 0 | — | — | — | 1w: frozen3.0 | 1w: none |
| P-ADD-SFP/scored | frozen3.0 | 1w | IN_RANGE | 29 | 0.1665 | 0.3103 | 4.8288 | 0 | 0 | 25 | 0.2243 | 0.3200 | 5.6070 | 1w: frozen3.0 | 1w: none |
| P-ADD-SFP/scored | frozen3.0 | 1w | BULL_EXP | 40 | 0.6842 | 0.2750 | 27.3673 | 0 | 0 | 20 | 1.8610 | 0.4000 | 37.2202 | 1w: frozen3.0 | 1w: none |
| P-ADD-SFP/scored | frozen3.0 | 1w | BEAR_EXP | 94 | -0.1350 | 0.3511 | -12.6933 | 0 | 0 | 32 | -0.0998 | 0.3438 | -3.1928 | 1w: frozen3.0 | 1w: none |
| P-ADD-SFP/scored | frozen3.0 | 1w | __ALL__ | 200 | 0.1841 | 0.3400 | 36.8120 | 0 | 0 | 77 | 0.5147 | 0.3506 | 39.6344 | 1w: frozen3.0 | 1w: none |
| P-TP-RNG/scored | calibrated | 1h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-TP-RNG/scored | calibrated | 1h | IN_RANGE | 126 | 0.1716 | 0.3730 | 21.6259 | 79 | 73 | 47 | 0.5270 | 0.4468 | 24.7668 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-TP-RNG/scored | calibrated | 1h | BULL_EXP | 38 | -0.1387 | 0.3421 | -5.2720 | 27 | 23 | 11 | -0.2775 | 0.4545 | -3.0527 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-TP-RNG/scored | calibrated | 1h | BEAR_EXP | 36 | 0.5684 | 0.4167 | 20.4625 | 17 | 19 | 19 | 0.9021 | 0.2632 | 17.1394 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-TP-RNG/scored | calibrated | 1h | __ALL__ | 200 | 0.1841 | 0.3750 | 36.8165 | 123 | 115 | 77 | 0.5046 | 0.4026 | 38.8535 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| P-TP-RNG/scored | calibrated | 4h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h: tuning | 4h: NEARUSDT |
| P-TP-RNG/scored | calibrated | 4h | IN_RANGE | 141 | 0.1284 | 0.3759 | 18.1042 | 88 | 31 | 53 | 0.3199 | 0.3962 | 16.9565 | 4h: tuning | 4h: NEARUSDT |
| P-TP-RNG/scored | calibrated | 4h | BULL_EXP | 32 | 0.8062 | 0.4375 | 25.7995 | 20 | 1 | 12 | 2.2375 | 0.5833 | 26.8503 | 4h: tuning | 4h: NEARUSDT |
| P-TP-RNG/scored | calibrated | 4h | BEAR_EXP | 27 | -0.2625 | 0.2963 | -7.0872 | 15 | 8 | 12 | -0.4128 | 0.2500 | -4.9534 | 4h: tuning | 4h: NEARUSDT |
| P-TP-RNG/scored | calibrated | 4h | __ALL__ | 200 | 0.1841 | 0.3750 | 36.8165 | 123 | 40 | 77 | 0.5046 | 0.4026 | 38.8535 | 4h: tuning | 4h: NEARUSDT |
| P-TP-RNG/scored | calibrated | 12h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 12h | IN_RANGE | 103 | 0.0585 | 0.3689 | 6.0287 | 54 | 74 | 49 | 0.1055 | 0.3878 | 5.1712 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 12h | BULL_EXP | 58 | 0.4842 | 0.3793 | 28.0831 | 45 | 32 | 13 | 2.2197 | 0.3846 | 28.8562 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 12h | BEAR_EXP | 39 | 0.0693 | 0.3846 | 2.7046 | 24 | 17 | 15 | 0.3217 | 0.4667 | 4.8261 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 12h | __ALL__ | 200 | 0.1841 | 0.3750 | 36.8165 | 123 | 123 | 77 | 0.5046 | 0.4026 | 38.8535 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 1d | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 1d | IN_RANGE | 73 | 0.0320 | 0.3836 | 2.3367 | 38 | 27 | 35 | 0.1755 | 0.4000 | 6.1427 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 1d | BULL_EXP | 77 | 0.1699 | 0.3766 | 13.0846 | 59 | 29 | 18 | 1.0646 | 0.5556 | 19.1634 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 1d | BEAR_EXP | 50 | 0.4279 | 0.3600 | 21.3952 | 26 | 19 | 24 | 0.5645 | 0.2917 | 13.5473 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 1d | __ALL__ | 200 | 0.1841 | 0.3750 | 36.8165 | 123 | 75 | 77 | 0.5046 | 0.4026 | 38.8535 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 1w | NONE | 30 | 0.1330 | 0.4333 | 3.9911 | 30 | 0 | 0 | — | — | — | 1w: whole-tape (fallback) | 1w: none |
| P-TP-RNG/scored | calibrated | 1w | IN_RANGE | 43 | 0.1981 | 0.3953 | 8.5183 | 43 | 0 | 31 | 0.2229 | 0.3871 | 6.9089 | 1w: whole-tape (fallback) | 1w: none |
| P-TP-RNG/scored | calibrated | 1w | BULL_EXP | 29 | 1.2242 | 0.3793 | 35.5007 | 29 | 0 | 19 | 1.9155 | 0.4737 | 36.3947 | 1w: whole-tape (fallback) | 1w: none |
| P-TP-RNG/scored | calibrated | 1w | BEAR_EXP | 98 | -0.1142 | 0.3469 | -11.1936 | 98 | 0 | 27 | -0.1648 | 0.3704 | -4.4502 | 1w: whole-tape (fallback) | 1w: none |
| P-TP-RNG/scored | calibrated | 1w | __ALL__ | 200 | 0.1841 | 0.3750 | 36.8165 | 200 | 0 | 77 | 0.5046 | 0.4026 | 38.8535 | 1w: whole-tape (fallback) | 1w: none |
| P-TP-RNG/scored | frozen3.0 | 1h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h: frozen3.0 | 1h: none |
| P-TP-RNG/scored | frozen3.0 | 1h | IN_RANGE | 127 | 0.2520 | 0.3543 | 32.0036 | 0 | 0 | 49 | 0.8922 | 0.4286 | 43.7183 | 1h: frozen3.0 | 1h: none |
| P-TP-RNG/scored | frozen3.0 | 1h | BULL_EXP | 41 | -0.1018 | 0.3659 | -4.1746 | 0 | 0 | 17 | -0.2908 | 0.2941 | -4.9434 | 1h: frozen3.0 | 1h: none |
| P-TP-RNG/scored | frozen3.0 | 1h | BEAR_EXP | 32 | 0.2809 | 0.4688 | 8.9875 | 0 | 0 | 11 | 0.0071 | 0.4545 | 0.0785 | 1h: frozen3.0 | 1h: none |
| P-TP-RNG/scored | frozen3.0 | 1h | __ALL__ | 200 | 0.1841 | 0.3750 | 36.8165 | 0 | 0 | 77 | 0.5046 | 0.4026 | 38.8535 | 1h: frozen3.0 | 1h: none |
| P-TP-RNG/scored | frozen3.0 | 4h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h: frozen3.0 | 4h: none |
| P-TP-RNG/scored | frozen3.0 | 4h | IN_RANGE | 94 | 0.1900 | 0.4255 | 17.8598 | 0 | 0 | 45 | 0.3464 | 0.4667 | 15.5865 | 4h: frozen3.0 | 4h: none |
| P-TP-RNG/scored | frozen3.0 | 4h | BULL_EXP | 66 | 0.3207 | 0.3030 | 21.1677 | 0 | 0 | 19 | 1.5093 | 0.3158 | 28.6764 | 4h: frozen3.0 | 4h: none |
| P-TP-RNG/scored | frozen3.0 | 4h | BEAR_EXP | 40 | -0.0553 | 0.3750 | -2.2111 | 0 | 0 | 13 | -0.4161 | 0.3077 | -5.4095 | 4h: frozen3.0 | 4h: none |
| P-TP-RNG/scored | frozen3.0 | 4h | __ALL__ | 200 | 0.1841 | 0.3750 | 36.8165 | 0 | 0 | 77 | 0.5046 | 0.4026 | 38.8535 | 4h: frozen3.0 | 4h: none |
| P-TP-RNG/scored | frozen3.0 | 12h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 12h: frozen3.0 | 12h: none |
| P-TP-RNG/scored | frozen3.0 | 12h | IN_RANGE | 74 | 0.0524 | 0.3919 | 3.8779 | 0 | 0 | 36 | 0.2006 | 0.4167 | 7.2226 | 12h: frozen3.0 | 12h: none |
| P-TP-RNG/scored | frozen3.0 | 12h | BULL_EXP | 76 | 0.5009 | 0.4079 | 38.0702 | 0 | 0 | 24 | 1.7427 | 0.5417 | 41.8237 | 12h: frozen3.0 | 12h: none |
| P-TP-RNG/scored | frozen3.0 | 12h | BEAR_EXP | 50 | -0.1026 | 0.3000 | -5.1316 | 0 | 0 | 17 | -0.5996 | 0.1765 | -10.1928 | 12h: frozen3.0 | 12h: none |
| P-TP-RNG/scored | frozen3.0 | 12h | __ALL__ | 200 | 0.1841 | 0.3750 | 36.8165 | 0 | 0 | 77 | 0.5046 | 0.4026 | 38.8535 | 12h: frozen3.0 | 12h: none |
| P-TP-RNG/scored | frozen3.0 | 1d | NONE | 4 | -0.6011 | 0.2500 | -2.4045 | 0 | 0 | 0 | — | — | — | 1d: frozen3.0 | 1d: none |
| P-TP-RNG/scored | frozen3.0 | 1d | IN_RANGE | 58 | -0.1864 | 0.3448 | -10.8109 | 0 | 0 | 28 | -0.0149 | 0.4286 | -0.4175 | 1d: frozen3.0 | 1d: none |
| P-TP-RNG/scored | frozen3.0 | 1d | BULL_EXP | 74 | 0.2109 | 0.4054 | 15.6054 | 0 | 0 | 19 | 0.7786 | 0.4737 | 14.7937 | 1d: frozen3.0 | 1d: none |
| P-TP-RNG/scored | frozen3.0 | 1d | BEAR_EXP | 64 | 0.5379 | 0.3750 | 34.4265 | 0 | 0 | 30 | 0.8159 | 0.3333 | 24.4773 | 1d: frozen3.0 | 1d: none |
| P-TP-RNG/scored | frozen3.0 | 1d | __ALL__ | 200 | 0.1841 | 0.3750 | 36.8165 | 0 | 0 | 77 | 0.5046 | 0.4026 | 38.8535 | 1d: frozen3.0 | 1d: none |
| P-TP-RNG/scored | frozen3.0 | 1w | NONE | 37 | 0.2960 | 0.4324 | 10.9510 | 0 | 0 | 0 | — | — | — | 1w: frozen3.0 | 1w: none |
| P-TP-RNG/scored | frozen3.0 | 1w | IN_RANGE | 29 | 0.3167 | 0.3793 | 9.1852 | 0 | 0 | 25 | 0.3439 | 0.4000 | 8.5974 | 1w: frozen3.0 | 1w: none |
| P-TP-RNG/scored | frozen3.0 | 1w | BULL_EXP | 40 | 0.6372 | 0.3000 | 25.4876 | 0 | 0 | 20 | 1.7670 | 0.4500 | 35.3405 | 1w: frozen3.0 | 1w: none |
| P-TP-RNG/scored | frozen3.0 | 1w | BEAR_EXP | 94 | -0.0937 | 0.3830 | -8.8074 | 0 | 0 | 32 | -0.1589 | 0.3750 | -5.0844 | 1w: frozen3.0 | 1w: none |
| P-TP-RNG/scored | frozen3.0 | 1w | __ALL__ | 200 | 0.1841 | 0.3750 | 36.8165 | 0 | 0 | 77 | 0.5046 | 0.4026 | 38.8535 | 1w: frozen3.0 | 1w: none |

### Outcomes by coincidence at ENTRY (the HOLDOUT slice beside) — WHOLE

| book | scale_kind | lens | coin_rule | coin_cat | n | mean_net_r | p_win | sum_net_r | n_scale_in_sample | n_stability_changed | n_holdout | mean_net_r_holdout | p_win_holdout | sum_net_r_holdout | lenses_read | pick_window | stability_changed_members |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P-WARN-1/scored | calibrated | 1h | record | both | 4 | 2.4491 | 0.7500 | 9.7962 | 2 | 2 | 2 | 3.8599 | 0.5000 | 7.7198 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-WARN-1/scored | calibrated | 1h | record | top | 9 | 0.2213 | 0.3333 | 1.9913 | 4 | 3 | 5 | 0.6434 | 0.4000 | 3.2168 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-WARN-1/scored | calibrated | 1h | record | bot | 17 | 0.4480 | 0.5294 | 7.6162 | 12 | 11 | 5 | 1.5732 | 0.8000 | 7.8660 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-WARN-1/scored | calibrated | 1h | record | none | 170 | 0.1325 | 0.2824 | 22.5196 | 105 | 99 | 65 | 0.3505 | 0.2769 | 22.7796 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-WARN-1/scored | calibrated | 1h | mem_twin | both | 4 | 2.4491 | 0.7500 | 9.7962 | 2 | 2 | 2 | 3.8599 | 0.5000 | 7.7198 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-WARN-1/scored | calibrated | 1h | mem_twin | top | 10 | 0.0943 | 0.3000 | 0.9430 | 5 | 4 | 5 | 0.6434 | 0.4000 | 3.2168 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-WARN-1/scored | calibrated | 1h | mem_twin | bot | 19 | 0.2832 | 0.4737 | 5.3803 | 14 | 12 | 5 | 1.5732 | 0.8000 | 7.8660 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-WARN-1/scored | calibrated | 1h | mem_twin | none | 167 | 0.1545 | 0.2874 | 25.8037 | 102 | 97 | 65 | 0.3505 | 0.2769 | 22.7796 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-WARN-1/scored | calibrated | 4h | record | both | 9 | -0.0610 | 0.2222 | -0.5491 | 7 | 8 | 2 | -1.0485 | 0.0000 | -2.0970 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 4h | record | top | 8 | 0.7352 | 0.5000 | 5.8812 | 1 | 7 | 7 | 0.9097 | 0.5714 | 6.3682 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 4h | record | bot | 12 | 0.5366 | 0.1667 | 6.4395 | 5 | 11 | 7 | 0.6849 | 0.1429 | 4.7940 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 4h | record | none | 171 | 0.1763 | 0.3216 | 30.1516 | 110 | 137 | 61 | 0.5331 | 0.3279 | 32.5170 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 4h | mem_twin | both | 9 | -0.0610 | 0.2222 | -0.5491 | 7 | 8 | 2 | -1.0485 | 0.0000 | -2.0970 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 4h | mem_twin | top | 8 | 0.7352 | 0.5000 | 5.8812 | 1 | 7 | 7 | 0.9097 | 0.5714 | 6.3682 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 4h | mem_twin | bot | 13 | 0.7181 | 0.2308 | 9.3347 | 6 | 11 | 7 | 0.6849 | 0.1429 | 4.7940 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 4h | mem_twin | none | 170 | 0.1603 | 0.3176 | 27.2564 | 109 | 137 | 61 | 0.5331 | 0.3279 | 32.5170 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 12h | record | both | 6 | 0.5356 | 0.3333 | 3.2137 | 4 | 3 | 2 | -0.6138 | 0.0000 | -1.2277 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 12h | record | top | 4 | -0.8505 | 0.0000 | -3.4018 | 1 | 2 | 3 | -0.8127 | 0.0000 | -2.4380 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 12h | record | bot | 13 | 0.2289 | 0.2308 | 2.9754 | 5 | 8 | 8 | 0.7727 | 0.3750 | 6.1815 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 12h | record | none | 177 | 0.2211 | 0.3277 | 39.1360 | 113 | 110 | 64 | 0.6104 | 0.3438 | 39.0664 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 12h | mem_twin | both | 7 | 0.3026 | 0.2857 | 2.1183 | 4 | 4 | 3 | -0.7744 | 0.0000 | -2.3231 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 12h | mem_twin | top | 9 | -0.8687 | 0.0000 | -7.8185 | 3 | 6 | 6 | -0.8929 | 0.0000 | -5.3574 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 12h | mem_twin | bot | 15 | 0.2306 | 0.2667 | 3.4586 | 8 | 10 | 7 | 1.0396 | 0.4286 | 7.2770 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 12h | mem_twin | none | 169 | 0.2613 | 0.3373 | 44.1648 | 108 | 103 | 61 | 0.6883 | 0.3607 | 41.9858 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-WARN-1/scored | calibrated | 1d | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-WARN-1/scored | calibrated | 1d | record | top | 1 | 3.8512 | 1.0000 | 3.8512 | 1 | 1 | 1 | 3.8512 | 1.0000 | 3.8512 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-WARN-1/scored | calibrated | 1d | record | bot | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-WARN-1/scored | calibrated | 1d | record | none | 199 | 0.1913 | 0.3116 | 38.0720 | 199 | 74 | 76 | 0.4965 | 0.3158 | 37.7310 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-WARN-1/scored | calibrated | 1d | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-WARN-1/scored | calibrated | 1d | mem_twin | top | 1 | 3.8512 | 1.0000 | 3.8512 | 1 | 1 | 1 | 3.8512 | 1.0000 | 3.8512 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-WARN-1/scored | calibrated | 1d | mem_twin | bot | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-WARN-1/scored | calibrated | 1d | mem_twin | none | 199 | 0.1913 | 0.3116 | 38.0720 | 199 | 74 | 76 | 0.4965 | 0.3158 | 37.7310 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-WARN-1/scored | calibrated | 1w | record | NA | 200 | 0.2096 | 0.3150 | 41.9232 | 200 | 0 | 77 | 0.5400 | 0.3247 | 41.5822 | 1w | 1w: whole-tape (fallback) | 1w: none |
| P-WARN-1/scored | calibrated | 1w | mem_twin | NA | 200 | 0.2096 | 0.3150 | 41.9232 | 200 | 0 | 77 | 0.5400 | 0.3247 | 41.5822 | 1w | 1w: whole-tape (fallback) | 1w: none |
| P-WARN-1/scored | frozen3.0 | 1h | record | both | 1 | -0.4870 | 0.0000 | -0.4870 | 0 | 0 | 0 | — | — | — | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-WARN-1/scored | frozen3.0 | 1h | record | top | 9 | 0.3485 | 0.4444 | 3.1369 | 0 | 0 | 6 | 0.9547 | 0.6667 | 5.7281 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-WARN-1/scored | frozen3.0 | 1h | record | bot | 2 | -0.5115 | 0.5000 | -1.0231 | 0 | 0 | 1 | -1.0349 | 0.0000 | -1.0349 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-WARN-1/scored | frozen3.0 | 1h | record | none | 188 | 0.2143 | 0.3085 | 40.2964 | 0 | 0 | 70 | 0.5270 | 0.3000 | 36.8891 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-WARN-1/scored | frozen3.0 | 1h | mem_twin | both | 1 | -0.4870 | 0.0000 | -0.4870 | 0 | 0 | 0 | — | — | — | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-WARN-1/scored | frozen3.0 | 1h | mem_twin | top | 10 | 0.9316 | 0.5000 | 9.3163 | 0 | 0 | 7 | 1.7011 | 0.7143 | 11.9074 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-WARN-1/scored | frozen3.0 | 1h | mem_twin | bot | 2 | -0.5115 | 0.5000 | -1.0231 | 0 | 0 | 1 | -1.0349 | 0.0000 | -1.0349 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-WARN-1/scored | frozen3.0 | 1h | mem_twin | none | 187 | 0.1824 | 0.3048 | 34.1170 | 0 | 0 | 69 | 0.4451 | 0.2899 | 30.7097 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-WARN-1/scored | frozen3.0 | 4h | record | both | 5 | -0.5545 | 0.2000 | -2.7724 | 0 | 0 | 1 | -0.7735 | 0.0000 | -0.7735 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-WARN-1/scored | frozen3.0 | 4h | record | top | 3 | 0.1380 | 0.3333 | 0.4139 | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-WARN-1/scored | frozen3.0 | 4h | record | bot | 13 | -0.7047 | 0.0769 | -9.1610 | 0 | 0 | 10 | -0.6569 | 0.1000 | -6.5694 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-WARN-1/scored | frozen3.0 | 4h | record | none | 179 | 0.2986 | 0.3352 | 53.4428 | 0 | 0 | 66 | 0.7413 | 0.3636 | 48.9251 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-WARN-1/scored | frozen3.0 | 4h | mem_twin | both | 5 | -0.5545 | 0.2000 | -2.7724 | 0 | 0 | 1 | -0.7735 | 0.0000 | -0.7735 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-WARN-1/scored | frozen3.0 | 4h | mem_twin | top | 3 | 0.1380 | 0.3333 | 0.4139 | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-WARN-1/scored | frozen3.0 | 4h | mem_twin | bot | 13 | -0.7047 | 0.0769 | -9.1610 | 0 | 0 | 10 | -0.6569 | 0.1000 | -6.5694 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-WARN-1/scored | frozen3.0 | 4h | mem_twin | none | 179 | 0.2986 | 0.3352 | 53.4428 | 0 | 0 | 66 | 0.7413 | 0.3636 | 48.9251 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-WARN-1/scored | frozen3.0 | 12h | record | both | 5 | 0.9906 | 0.4000 | 4.9530 | 0 | 0 | 3 | 2.1296 | 0.6667 | 6.3888 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-WARN-1/scored | frozen3.0 | 12h | record | top | 9 | -0.2031 | 0.2222 | -1.8283 | 0 | 0 | 4 | -0.4897 | 0.2500 | -1.9588 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-WARN-1/scored | frozen3.0 | 12h | record | bot | 9 | 0.0394 | 0.3333 | 0.3543 | 0 | 0 | 4 | 0.7219 | 0.5000 | 2.8878 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-WARN-1/scored | frozen3.0 | 12h | record | none | 177 | 0.2172 | 0.3164 | 38.4443 | 0 | 0 | 66 | 0.5192 | 0.3030 | 34.2644 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-WARN-1/scored | frozen3.0 | 12h | mem_twin | both | 6 | 0.6429 | 0.3333 | 3.8575 | 0 | 0 | 4 | 1.3233 | 0.5000 | 5.2934 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-WARN-1/scored | frozen3.0 | 12h | mem_twin | top | 9 | -0.2031 | 0.2222 | -1.8283 | 0 | 0 | 4 | -0.4897 | 0.2500 | -1.9588 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-WARN-1/scored | frozen3.0 | 12h | mem_twin | bot | 8 | 0.1812 | 0.3750 | 1.4497 | 0 | 0 | 3 | 1.3278 | 0.6667 | 3.9833 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-WARN-1/scored | frozen3.0 | 12h | mem_twin | none | 177 | 0.2172 | 0.3164 | 38.4443 | 0 | 0 | 66 | 0.5192 | 0.3030 | 34.2644 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-WARN-1/scored | frozen3.0 | 1d | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-WARN-1/scored | frozen3.0 | 1d | record | top | 2 | 1.3995 | 0.5000 | 2.7991 | 0 | 0 | 2 | 1.3995 | 0.5000 | 2.7991 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-WARN-1/scored | frozen3.0 | 1d | record | bot | 1 | 2.0212 | 1.0000 | 2.0212 | 0 | 0 | 1 | 2.0212 | 1.0000 | 2.0212 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-WARN-1/scored | frozen3.0 | 1d | record | none | 197 | 0.1883 | 0.3096 | 37.1030 | 0 | 0 | 74 | 0.4968 | 0.3108 | 36.7619 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-WARN-1/scored | frozen3.0 | 1d | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-WARN-1/scored | frozen3.0 | 1d | mem_twin | top | 2 | 1.3995 | 0.5000 | 2.7991 | 0 | 0 | 2 | 1.3995 | 0.5000 | 2.7991 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-WARN-1/scored | frozen3.0 | 1d | mem_twin | bot | 1 | 2.0212 | 1.0000 | 2.0212 | 0 | 0 | 1 | 2.0212 | 1.0000 | 2.0212 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-WARN-1/scored | frozen3.0 | 1d | mem_twin | none | 197 | 0.1883 | 0.3096 | 37.1030 | 0 | 0 | 74 | 0.4968 | 0.3108 | 36.7619 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-WARN-1/scored | frozen3.0 | 1w | record | NA | 200 | 0.2096 | 0.3150 | 41.9232 | 0 | 0 | 77 | 0.5400 | 0.3247 | 41.5822 | 1w | 1w: frozen3.0 | 1w: none |
| P-WARN-1/scored | frozen3.0 | 1w | mem_twin | NA | 200 | 0.2096 | 0.3150 | 41.9232 | 0 | 0 | 77 | 0.5400 | 0.3247 | 41.5822 | 1w | 1w: frozen3.0 | 1w: none |
| P-AGE-1/scored | calibrated | 1h | record | both | 3 | 3.1231 | 0.6667 | 9.3694 | 1 | 2 | 2 | 3.8599 | 0.5000 | 7.7198 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-AGE-1/scored | calibrated | 1h | record | top | 7 | 0.4219 | 0.4286 | 2.9535 | 3 | 2 | 4 | 0.9858 | 0.5000 | 3.9432 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-AGE-1/scored | calibrated | 1h | record | bot | 13 | 0.7852 | 0.6154 | 10.2078 | 8 | 7 | 5 | 1.5732 | 0.8000 | 7.8660 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-AGE-1/scored | calibrated | 1h | record | none | 118 | 0.3469 | 0.3729 | 40.9334 | 69 | 70 | 49 | 0.6627 | 0.3878 | 32.4726 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-AGE-1/scored | calibrated | 1h | mem_twin | both | 3 | 3.1231 | 0.6667 | 9.3694 | 1 | 2 | 2 | 3.8599 | 0.5000 | 7.7198 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-AGE-1/scored | calibrated | 1h | mem_twin | top | 7 | 0.4219 | 0.4286 | 2.9535 | 3 | 2 | 4 | 0.9858 | 0.5000 | 3.9432 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-AGE-1/scored | calibrated | 1h | mem_twin | bot | 15 | 0.5315 | 0.5333 | 7.9719 | 10 | 8 | 5 | 1.5732 | 0.8000 | 7.8660 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-AGE-1/scored | calibrated | 1h | mem_twin | none | 116 | 0.3721 | 0.3793 | 43.1693 | 67 | 69 | 49 | 0.6627 | 0.3878 | 32.4726 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-AGE-1/scored | calibrated | 4h | record | both | 6 | 0.8308 | 0.6667 | 4.9849 | 6 | 5 | 0 | — | — | — | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 4h | record | top | 6 | 0.9954 | 0.6667 | 5.9721 | 0 | 5 | 6 | 0.9954 | 0.6667 | 5.9721 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 4h | record | bot | 9 | 0.3313 | 0.1111 | 2.9814 | 4 | 8 | 5 | 1.0924 | 0.2000 | 5.4622 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 4h | record | none | 120 | 0.4127 | 0.4000 | 49.5257 | 71 | 94 | 49 | 0.8279 | 0.4286 | 40.5673 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 4h | mem_twin | both | 6 | 0.8308 | 0.6667 | 4.9849 | 6 | 5 | 0 | — | — | — | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 4h | mem_twin | top | 6 | 0.9954 | 0.6667 | 5.9721 | 0 | 5 | 6 | 0.9954 | 0.6667 | 5.9721 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 4h | mem_twin | bot | 9 | 0.3313 | 0.1111 | 2.9814 | 4 | 8 | 5 | 1.0924 | 0.2000 | 5.4622 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 4h | mem_twin | none | 120 | 0.4127 | 0.4000 | 49.5257 | 71 | 94 | 49 | 0.8279 | 0.4286 | 40.5673 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 12h | record | both | 6 | 0.5257 | 0.3333 | 3.1542 | 4 | 3 | 2 | -0.6436 | 0.0000 | -1.2872 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 12h | record | top | 3 | -1.0130 | 0.0000 | -3.0390 | 1 | 1 | 2 | -1.0376 | 0.0000 | -2.0752 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 12h | record | bot | 10 | 1.0038 | 0.6000 | 10.0381 | 3 | 5 | 7 | 1.2245 | 0.5714 | 8.5713 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 12h | record | none | 122 | 0.4370 | 0.4016 | 53.3108 | 73 | 74 | 49 | 0.9550 | 0.4490 | 46.7927 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 12h | mem_twin | both | 7 | 0.2941 | 0.2857 | 2.0588 | 4 | 4 | 3 | -0.7942 | 0.0000 | -2.3827 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 12h | mem_twin | top | 8 | -0.9320 | 0.0000 | -7.4557 | 3 | 5 | 5 | -0.9989 | 0.0000 | -4.9946 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 12h | mem_twin | bot | 10 | 1.1793 | 0.7000 | 11.7932 | 4 | 5 | 6 | 1.6111 | 0.6667 | 9.6668 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 12h | mem_twin | none | 116 | 0.4920 | 0.4138 | 57.0679 | 70 | 69 | 46 | 1.0807 | 0.4783 | 49.7121 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-AGE-1/scored | calibrated | 1d | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-AGE-1/scored | calibrated | 1d | record | top | 1 | 3.8512 | 1.0000 | 3.8512 | 1 | 1 | 1 | 3.8512 | 1.0000 | 3.8512 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-AGE-1/scored | calibrated | 1d | record | bot | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-AGE-1/scored | calibrated | 1d | record | none | 140 | 0.4258 | 0.4000 | 59.6129 | 140 | 51 | 59 | 0.8161 | 0.4237 | 48.1504 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-AGE-1/scored | calibrated | 1d | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-AGE-1/scored | calibrated | 1d | mem_twin | top | 1 | 3.8512 | 1.0000 | 3.8512 | 1 | 1 | 1 | 3.8512 | 1.0000 | 3.8512 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-AGE-1/scored | calibrated | 1d | mem_twin | bot | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-AGE-1/scored | calibrated | 1d | mem_twin | none | 140 | 0.4258 | 0.4000 | 59.6129 | 140 | 51 | 59 | 0.8161 | 0.4237 | 48.1504 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-AGE-1/scored | calibrated | 1w | record | NA | 141 | 0.4501 | 0.4043 | 63.4641 | 141 | 0 | 60 | 0.8667 | 0.4333 | 52.0016 | 1w | 1w: whole-tape (fallback) | 1w: none |
| P-AGE-1/scored | calibrated | 1w | mem_twin | NA | 141 | 0.4501 | 0.4043 | 63.4641 | 141 | 0 | 60 | 0.8667 | 0.4333 | 52.0016 | 1w | 1w: whole-tape (fallback) | 1w: none |
| P-AGE-1/scored | frozen3.0 | 1h | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-AGE-1/scored | frozen3.0 | 1h | record | top | 9 | 0.3331 | 0.4444 | 2.9977 | 0 | 0 | 6 | 0.9315 | 0.6667 | 5.5889 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-AGE-1/scored | frozen3.0 | 1h | record | bot | 2 | -0.5115 | 0.5000 | -1.0231 | 0 | 0 | 1 | -1.0349 | 0.0000 | -1.0349 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-AGE-1/scored | frozen3.0 | 1h | record | none | 130 | 0.4730 | 0.4000 | 61.4895 | 0 | 0 | 53 | 0.8952 | 0.4151 | 47.4477 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-AGE-1/scored | frozen3.0 | 1h | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-AGE-1/scored | frozen3.0 | 1h | mem_twin | top | 10 | 0.9177 | 0.5000 | 9.1771 | 0 | 0 | 7 | 1.6812 | 0.7143 | 11.7683 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-AGE-1/scored | frozen3.0 | 1h | mem_twin | bot | 2 | -0.5115 | 0.5000 | -1.0231 | 0 | 0 | 1 | -1.0349 | 0.0000 | -1.0349 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-AGE-1/scored | frozen3.0 | 1h | mem_twin | none | 129 | 0.4288 | 0.3953 | 55.3101 | 0 | 0 | 52 | 0.7936 | 0.4038 | 41.2683 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-AGE-1/scored | frozen3.0 | 4h | record | both | 5 | -0.5545 | 0.2000 | -2.7724 | 0 | 0 | 1 | -0.7735 | 0.0000 | -0.7735 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-AGE-1/scored | frozen3.0 | 4h | record | top | 2 | 1.2481 | 1.0000 | 2.4963 | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-AGE-1/scored | frozen3.0 | 4h | record | bot | 11 | -0.5436 | 0.1818 | -5.9794 | 0 | 0 | 8 | -0.3986 | 0.2500 | -3.1885 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-AGE-1/scored | frozen3.0 | 4h | record | none | 123 | 0.5668 | 0.4228 | 69.7197 | 0 | 0 | 51 | 1.0973 | 0.4706 | 55.9635 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-AGE-1/scored | frozen3.0 | 4h | mem_twin | both | 5 | -0.5545 | 0.2000 | -2.7724 | 0 | 0 | 1 | -0.7735 | 0.0000 | -0.7735 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-AGE-1/scored | frozen3.0 | 4h | mem_twin | top | 2 | 1.2481 | 1.0000 | 2.4963 | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-AGE-1/scored | frozen3.0 | 4h | mem_twin | bot | 11 | -0.5436 | 0.1818 | -5.9794 | 0 | 0 | 8 | -0.3986 | 0.2500 | -3.1885 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-AGE-1/scored | frozen3.0 | 4h | mem_twin | none | 123 | 0.5668 | 0.4228 | 69.7197 | 0 | 0 | 51 | 1.0973 | 0.4706 | 55.9635 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-AGE-1/scored | frozen3.0 | 12h | record | both | 4 | 1.6375 | 0.7500 | 6.5499 | 0 | 0 | 3 | 2.3159 | 1.0000 | 6.9476 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-AGE-1/scored | frozen3.0 | 12h | record | top | 8 | -0.1285 | 0.2500 | -1.0279 | 0 | 0 | 4 | -0.4897 | 0.2500 | -1.9588 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-AGE-1/scored | frozen3.0 | 12h | record | bot | 6 | 0.4832 | 0.6667 | 2.8991 | 0 | 0 | 3 | 1.1824 | 0.6667 | 3.5473 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-AGE-1/scored | frozen3.0 | 12h | record | none | 123 | 0.4475 | 0.3902 | 55.0431 | 0 | 0 | 50 | 0.8693 | 0.4000 | 43.4655 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-AGE-1/scored | frozen3.0 | 12h | mem_twin | both | 5 | 1.0909 | 0.6000 | 5.4544 | 0 | 0 | 4 | 1.4630 | 0.7500 | 5.8522 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-AGE-1/scored | frozen3.0 | 12h | mem_twin | top | 8 | -0.1285 | 0.2500 | -1.0279 | 0 | 0 | 4 | -0.4897 | 0.2500 | -1.9588 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-AGE-1/scored | frozen3.0 | 12h | mem_twin | bot | 5 | 0.7989 | 0.8000 | 3.9945 | 0 | 0 | 2 | 2.3214 | 1.0000 | 4.6428 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-AGE-1/scored | frozen3.0 | 12h | mem_twin | none | 123 | 0.4475 | 0.3902 | 55.0431 | 0 | 0 | 50 | 0.8693 | 0.4000 | 43.4655 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-AGE-1/scored | frozen3.0 | 1d | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-AGE-1/scored | frozen3.0 | 1d | record | top | 1 | 3.8512 | 1.0000 | 3.8512 | 0 | 0 | 1 | 3.8512 | 1.0000 | 3.8512 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-AGE-1/scored | frozen3.0 | 1d | record | bot | 1 | 2.0212 | 1.0000 | 2.0212 | 0 | 0 | 1 | 2.0212 | 1.0000 | 2.0212 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-AGE-1/scored | frozen3.0 | 1d | record | none | 139 | 0.4143 | 0.3957 | 57.5917 | 0 | 0 | 58 | 0.7953 | 0.4138 | 46.1292 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-AGE-1/scored | frozen3.0 | 1d | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-AGE-1/scored | frozen3.0 | 1d | mem_twin | top | 1 | 3.8512 | 1.0000 | 3.8512 | 0 | 0 | 1 | 3.8512 | 1.0000 | 3.8512 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-AGE-1/scored | frozen3.0 | 1d | mem_twin | bot | 1 | 2.0212 | 1.0000 | 2.0212 | 0 | 0 | 1 | 2.0212 | 1.0000 | 2.0212 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-AGE-1/scored | frozen3.0 | 1d | mem_twin | none | 139 | 0.4143 | 0.3957 | 57.5917 | 0 | 0 | 58 | 0.7953 | 0.4138 | 46.1292 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-AGE-1/scored | frozen3.0 | 1w | record | NA | 141 | 0.4501 | 0.4043 | 63.4641 | 0 | 0 | 60 | 0.8667 | 0.4333 | 52.0016 | 1w | 1w: frozen3.0 | 1w: none |
| P-AGE-1/scored | frozen3.0 | 1w | mem_twin | NA | 141 | 0.4501 | 0.4043 | 63.4641 | 0 | 0 | 60 | 0.8667 | 0.4333 | 52.0016 | 1w | 1w: frozen3.0 | 1w: none |
| P-WIN-1/scored | calibrated | 1h | record | both | 3 | 0.3504 | 0.6667 | 1.0512 | 2 | 1 | 1 | -1.0252 | 0.0000 | -1.0252 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-WIN-1/scored | calibrated | 1h | record | top | 6 | 0.6860 | 0.5000 | 4.1162 | 2 | 1 | 4 | 0.9858 | 0.5000 | 3.9432 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-WIN-1/scored | calibrated | 1h | record | bot | 12 | 0.3978 | 0.5833 | 4.7736 | 7 | 6 | 5 | 1.5732 | 0.8000 | 7.8660 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-WIN-1/scored | calibrated | 1h | record | none | 116 | 0.3624 | 0.3707 | 42.0330 | 70 | 62 | 46 | 0.7210 | 0.3696 | 33.1674 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-WIN-1/scored | calibrated | 1h | mem_twin | both | 3 | 0.3504 | 0.6667 | 1.0512 | 2 | 1 | 1 | -1.0252 | 0.0000 | -1.0252 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-WIN-1/scored | calibrated | 1h | mem_twin | top | 6 | 0.6860 | 0.5000 | 4.1162 | 2 | 1 | 4 | 0.9858 | 0.5000 | 3.9432 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-WIN-1/scored | calibrated | 1h | mem_twin | bot | 13 | 0.2851 | 0.5385 | 3.7068 | 8 | 6 | 5 | 1.5732 | 0.8000 | 7.8660 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-WIN-1/scored | calibrated | 1h | mem_twin | none | 115 | 0.3748 | 0.3739 | 43.0998 | 69 | 62 | 46 | 0.7210 | 0.3696 | 33.1674 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-WIN-1/scored | calibrated | 4h | record | both | 7 | 0.5633 | 0.5714 | 3.9429 | 6 | 6 | 1 | -1.0419 | 0.0000 | -1.0419 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 4h | record | top | 5 | 1.1038 | 0.6000 | 5.5192 | 0 | 5 | 5 | 1.1038 | 0.6000 | 5.5192 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 4h | record | bot | 9 | 0.8219 | 0.2222 | 7.3970 | 5 | 9 | 4 | 1.5589 | 0.2500 | 6.2356 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 4h | record | none | 116 | 0.3027 | 0.3966 | 35.1149 | 70 | 86 | 46 | 0.7226 | 0.4130 | 33.2386 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 4h | mem_twin | both | 7 | 0.5633 | 0.5714 | 3.9429 | 6 | 6 | 1 | -1.0419 | 0.0000 | -1.0419 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 4h | mem_twin | top | 5 | 1.1038 | 0.6000 | 5.5192 | 0 | 5 | 5 | 1.1038 | 0.6000 | 5.5192 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 4h | mem_twin | bot | 9 | 0.8219 | 0.2222 | 7.3970 | 5 | 9 | 4 | 1.5589 | 0.2500 | 6.2356 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 4h | mem_twin | none | 116 | 0.3027 | 0.3966 | 35.1149 | 70 | 86 | 46 | 0.7226 | 0.4130 | 33.2386 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 12h | record | both | 4 | -0.4155 | 0.2500 | -1.6621 | 3 | 1 | 1 | -0.2568 | 0.0000 | -0.2568 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 12h | record | top | 2 | -0.9986 | 0.0000 | -1.9972 | 1 | 1 | 1 | -1.0334 | 0.0000 | -1.0334 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 12h | record | bot | 9 | 1.2371 | 0.6667 | 11.1336 | 3 | 4 | 6 | 1.6111 | 0.6667 | 9.6668 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 12h | record | none | 122 | 0.3648 | 0.3934 | 44.4998 | 74 | 74 | 48 | 0.7411 | 0.3958 | 35.5749 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 12h | mem_twin | both | 4 | -0.4155 | 0.2500 | -1.6621 | 3 | 1 | 1 | -0.2568 | 0.0000 | -0.2568 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 12h | mem_twin | top | 5 | -0.9002 | 0.0000 | -4.5010 | 2 | 3 | 3 | -1.0375 | 0.0000 | -3.1126 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 12h | mem_twin | bot | 10 | 1.1793 | 0.7000 | 11.7932 | 4 | 5 | 6 | 1.6111 | 0.6667 | 9.6668 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 12h | mem_twin | none | 118 | 0.3927 | 0.3983 | 46.3439 | 72 | 71 | 46 | 0.8186 | 0.4130 | 37.6541 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-WIN-1/scored | calibrated | 1d | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-WIN-1/scored | calibrated | 1d | record | top | 1 | 3.8512 | 1.0000 | 3.8512 | 1 | 1 | 1 | 3.8512 | 1.0000 | 3.8512 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-WIN-1/scored | calibrated | 1d | record | bot | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-WIN-1/scored | calibrated | 1d | record | none | 136 | 0.3538 | 0.3971 | 48.1228 | 136 | 43 | 55 | 0.7291 | 0.4000 | 40.1003 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-WIN-1/scored | calibrated | 1d | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-WIN-1/scored | calibrated | 1d | mem_twin | top | 1 | 3.8512 | 1.0000 | 3.8512 | 1 | 1 | 1 | 3.8512 | 1.0000 | 3.8512 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-WIN-1/scored | calibrated | 1d | mem_twin | bot | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-WIN-1/scored | calibrated | 1d | mem_twin | none | 136 | 0.3538 | 0.3971 | 48.1228 | 136 | 43 | 55 | 0.7291 | 0.4000 | 40.1003 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-WIN-1/scored | calibrated | 1w | record | NA | 137 | 0.3794 | 0.4015 | 51.9740 | 137 | 0 | 56 | 0.7848 | 0.4107 | 43.9515 | 1w | 1w: whole-tape (fallback) | 1w: none |
| P-WIN-1/scored | calibrated | 1w | mem_twin | NA | 137 | 0.3794 | 0.4015 | 51.9740 | 137 | 0 | 56 | 0.7848 | 0.4107 | 43.9515 | 1w | 1w: whole-tape (fallback) | 1w: none |
| P-WIN-1/scored | frozen3.0 | 1h | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-WIN-1/scored | frozen3.0 | 1h | record | top | 6 | 0.6832 | 0.5000 | 4.0995 | 0 | 0 | 5 | 0.8994 | 0.6000 | 4.4972 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-WIN-1/scored | frozen3.0 | 1h | record | bot | 2 | -0.5115 | 0.5000 | -1.0231 | 0 | 0 | 1 | -1.0349 | 0.0000 | -1.0349 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-WIN-1/scored | frozen3.0 | 1h | record | none | 129 | 0.3791 | 0.3953 | 48.8976 | 0 | 0 | 50 | 0.8098 | 0.4000 | 40.4892 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-WIN-1/scored | frozen3.0 | 1h | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-WIN-1/scored | frozen3.0 | 1h | mem_twin | top | 7 | 1.4684 | 0.5714 | 10.2789 | 0 | 0 | 6 | 1.7794 | 0.6667 | 10.6766 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-WIN-1/scored | frozen3.0 | 1h | mem_twin | bot | 2 | -0.5115 | 0.5000 | -1.0231 | 0 | 0 | 1 | -1.0349 | 0.0000 | -1.0349 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-WIN-1/scored | frozen3.0 | 1h | mem_twin | none | 128 | 0.3337 | 0.3906 | 42.7182 | 0 | 0 | 49 | 0.7002 | 0.3878 | 34.3098 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-WIN-1/scored | frozen3.0 | 4h | record | both | 4 | -0.4997 | 0.2500 | -1.9990 | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-WIN-1/scored | frozen3.0 | 4h | record | top | 2 | 1.2481 | 1.0000 | 2.4963 | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-WIN-1/scored | frozen3.0 | 4h | record | bot | 10 | -0.5290 | 0.2000 | -5.2901 | 0 | 0 | 7 | -0.3570 | 0.2857 | -2.4992 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-WIN-1/scored | frozen3.0 | 4h | record | none | 121 | 0.4691 | 0.4132 | 56.7668 | 0 | 0 | 49 | 0.9480 | 0.4286 | 46.4506 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-WIN-1/scored | frozen3.0 | 4h | mem_twin | both | 4 | -0.4997 | 0.2500 | -1.9990 | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-WIN-1/scored | frozen3.0 | 4h | mem_twin | top | 2 | 1.2481 | 1.0000 | 2.4963 | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-WIN-1/scored | frozen3.0 | 4h | mem_twin | bot | 10 | -0.5290 | 0.2000 | -5.2901 | 0 | 0 | 7 | -0.3570 | 0.2857 | -2.4992 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-WIN-1/scored | frozen3.0 | 4h | mem_twin | none | 121 | 0.4691 | 0.4132 | 56.7668 | 0 | 0 | 49 | 0.9480 | 0.4286 | 46.4506 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-WIN-1/scored | frozen3.0 | 12h | record | both | 3 | 2.0951 | 0.6667 | 6.2854 | 0 | 0 | 2 | 3.3416 | 1.0000 | 6.6832 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-WIN-1/scored | frozen3.0 | 12h | record | top | 4 | 0.0621 | 0.2500 | 0.2483 | 0 | 0 | 1 | -1.0542 | 0.0000 | -1.0542 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-WIN-1/scored | frozen3.0 | 12h | record | bot | 6 | 0.6325 | 0.6667 | 3.7947 | 0 | 0 | 3 | 1.4810 | 0.6667 | 4.4430 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-WIN-1/scored | frozen3.0 | 12h | record | none | 124 | 0.3359 | 0.3871 | 41.6456 | 0 | 0 | 50 | 0.6776 | 0.3800 | 33.8795 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-WIN-1/scored | frozen3.0 | 12h | mem_twin | both | 3 | 2.0951 | 0.6667 | 6.2854 | 0 | 0 | 2 | 3.3416 | 1.0000 | 6.6832 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-WIN-1/scored | frozen3.0 | 12h | mem_twin | top | 4 | 0.0621 | 0.2500 | 0.2483 | 0 | 0 | 1 | -1.0542 | 0.0000 | -1.0542 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-WIN-1/scored | frozen3.0 | 12h | mem_twin | bot | 6 | 0.6325 | 0.6667 | 3.7947 | 0 | 0 | 3 | 1.4810 | 0.6667 | 4.4430 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-WIN-1/scored | frozen3.0 | 12h | mem_twin | none | 124 | 0.3359 | 0.3871 | 41.6456 | 0 | 0 | 50 | 0.6776 | 0.3800 | 33.8795 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-WIN-1/scored | frozen3.0 | 1d | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-WIN-1/scored | frozen3.0 | 1d | record | top | 2 | 1.3995 | 0.5000 | 2.7991 | 0 | 0 | 2 | 1.3995 | 0.5000 | 2.7991 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-WIN-1/scored | frozen3.0 | 1d | record | bot | 1 | 2.0212 | 1.0000 | 2.0212 | 0 | 0 | 1 | 2.0212 | 1.0000 | 2.0212 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-WIN-1/scored | frozen3.0 | 1d | record | none | 134 | 0.3519 | 0.3955 | 47.1537 | 0 | 0 | 53 | 0.7383 | 0.3962 | 39.1312 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-WIN-1/scored | frozen3.0 | 1d | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-WIN-1/scored | frozen3.0 | 1d | mem_twin | top | 2 | 1.3995 | 0.5000 | 2.7991 | 0 | 0 | 2 | 1.3995 | 0.5000 | 2.7991 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-WIN-1/scored | frozen3.0 | 1d | mem_twin | bot | 1 | 2.0212 | 1.0000 | 2.0212 | 0 | 0 | 1 | 2.0212 | 1.0000 | 2.0212 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-WIN-1/scored | frozen3.0 | 1d | mem_twin | none | 134 | 0.3519 | 0.3955 | 47.1537 | 0 | 0 | 53 | 0.7383 | 0.3962 | 39.1312 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-WIN-1/scored | frozen3.0 | 1w | record | NA | 137 | 0.3794 | 0.4015 | 51.9740 | 0 | 0 | 56 | 0.7848 | 0.4107 | 43.9515 | 1w | 1w: frozen3.0 | 1w: none |
| P-WIN-1/scored | frozen3.0 | 1w | mem_twin | NA | 137 | 0.3794 | 0.4015 | 51.9740 | 0 | 0 | 56 | 0.7848 | 0.4107 | 43.9515 | 1w | 1w: frozen3.0 | 1w: none |
| P-BRK-4H/scored | calibrated | 1h | record | both | 5 | 0.1853 | 0.6000 | 0.9265 | 3 | 3 | 2 | -0.4460 | 0.5000 | -0.8919 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-BRK-4H/scored | calibrated | 1h | record | top | 14 | -0.2912 | 0.2143 | -4.0770 | 9 | 8 | 5 | 0.0925 | 0.4000 | 0.4627 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-BRK-4H/scored | calibrated | 1h | record | bot | 10 | -0.4046 | 0.2000 | -4.0456 | 8 | 6 | 2 | -0.6802 | 0.0000 | -1.3604 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-BRK-4H/scored | calibrated | 1h | record | none | 293 | 0.0798 | 0.3618 | 23.3813 | 190 | 170 | 103 | 0.2603 | 0.3981 | 26.8128 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-BRK-4H/scored | calibrated | 1h | mem_twin | both | 5 | 0.1853 | 0.6000 | 0.9265 | 3 | 3 | 2 | -0.4460 | 0.5000 | -0.8919 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-BRK-4H/scored | calibrated | 1h | mem_twin | top | 16 | -0.3205 | 0.1875 | -5.1274 | 11 | 9 | 5 | 0.0925 | 0.4000 | 0.4627 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-BRK-4H/scored | calibrated | 1h | mem_twin | bot | 11 | -0.3448 | 0.2727 | -3.7924 | 9 | 7 | 2 | -0.6802 | 0.0000 | -1.3604 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-BRK-4H/scored | calibrated | 1h | mem_twin | none | 290 | 0.0834 | 0.3621 | 24.1785 | 187 | 168 | 103 | 0.2603 | 0.3981 | 26.8128 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-BRK-4H/scored | calibrated | 4h | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 4h | record | top | 6 | 0.1403 | 0.5000 | 0.8421 | 5 | 5 | 1 | -0.8563 | 0.0000 | -0.8563 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 4h | record | bot | 6 | -0.3538 | 0.3333 | -2.1227 | 3 | 2 | 3 | -0.2231 | 0.3333 | -0.6692 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 4h | record | none | 310 | 0.0563 | 0.3516 | 17.4659 | 202 | 240 | 108 | 0.2458 | 0.3981 | 26.5486 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 4h | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 4h | mem_twin | top | 7 | 0.1917 | 0.5714 | 1.3419 | 5 | 6 | 2 | -0.1782 | 0.5000 | -0.3564 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 4h | mem_twin | bot | 6 | -0.3538 | 0.3333 | -2.1227 | 3 | 2 | 3 | -0.2231 | 0.3333 | -0.6692 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 4h | mem_twin | none | 309 | 0.0549 | 0.3495 | 16.9661 | 202 | 239 | 107 | 0.2434 | 0.3925 | 26.0488 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 12h | record | both | 15 | 0.5748 | 0.4000 | 8.6216 | 11 | 8 | 4 | 0.9140 | 0.2500 | 3.6559 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 12h | record | top | 13 | 0.1424 | 0.4615 | 1.8509 | 7 | 8 | 6 | 0.6280 | 0.6667 | 3.7682 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 12h | record | bot | 16 | -0.2024 | 0.3750 | -3.2380 | 6 | 9 | 10 | -0.0573 | 0.5000 | -0.5725 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 12h | record | none | 278 | 0.0322 | 0.3453 | 8.9508 | 186 | 159 | 92 | 0.1975 | 0.3696 | 18.1716 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 12h | mem_twin | both | 18 | 0.5093 | 0.4444 | 9.1665 | 11 | 11 | 7 | 0.6001 | 0.4286 | 4.2008 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 12h | mem_twin | top | 19 | 0.0439 | 0.4737 | 0.8343 | 10 | 13 | 9 | 0.4301 | 0.6667 | 3.8710 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 12h | mem_twin | bot | 21 | -0.3223 | 0.2857 | -6.7688 | 13 | 13 | 8 | -0.2424 | 0.3750 | -1.9394 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 12h | mem_twin | none | 264 | 0.0491 | 0.3447 | 12.9533 | 176 | 147 | 88 | 0.2147 | 0.3636 | 18.8907 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-BRK-4H/scored | calibrated | 1d | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-BRK-4H/scored | calibrated | 1d | record | top | 1 | 0.2602 | 1.0000 | 0.2602 | 1 | 1 | 1 | 0.2602 | 1.0000 | 0.2602 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-BRK-4H/scored | calibrated | 1d | record | bot | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-BRK-4H/scored | calibrated | 1d | record | none | 321 | 0.0496 | 0.3520 | 15.9251 | 321 | 123 | 111 | 0.2231 | 0.3874 | 24.7629 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-BRK-4H/scored | calibrated | 1d | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-BRK-4H/scored | calibrated | 1d | mem_twin | top | 1 | 0.2602 | 1.0000 | 0.2602 | 1 | 1 | 1 | 0.2602 | 1.0000 | 0.2602 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-BRK-4H/scored | calibrated | 1d | mem_twin | bot | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-BRK-4H/scored | calibrated | 1d | mem_twin | none | 321 | 0.0496 | 0.3520 | 15.9251 | 321 | 123 | 111 | 0.2231 | 0.3874 | 24.7629 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-BRK-4H/scored | calibrated | 1w | record | NA | 322 | 0.0503 | 0.3540 | 16.1853 | 322 | 0 | 112 | 0.2234 | 0.3929 | 25.0231 | 1w | 1w: whole-tape (fallback) | 1w: none |
| P-BRK-4H/scored | calibrated | 1w | mem_twin | NA | 322 | 0.0503 | 0.3540 | 16.1853 | 322 | 0 | 112 | 0.2234 | 0.3929 | 25.0231 | 1w | 1w: whole-tape (fallback) | 1w: none |
| P-BRK-4H/scored | frozen3.0 | 1h | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-BRK-4H/scored | frozen3.0 | 1h | record | top | 3 | 0.1843 | 0.3333 | 0.5528 | 0 | 0 | 1 | -0.4523 | 0.0000 | -0.4523 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-BRK-4H/scored | frozen3.0 | 1h | record | bot | 3 | 0.3197 | 0.3333 | 0.9592 | 0 | 0 | 2 | 0.6336 | 0.5000 | 1.2671 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-BRK-4H/scored | frozen3.0 | 1h | record | none | 316 | 0.0464 | 0.3544 | 14.6733 | 0 | 0 | 109 | 0.2221 | 0.3945 | 24.2083 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-BRK-4H/scored | frozen3.0 | 1h | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-BRK-4H/scored | frozen3.0 | 1h | mem_twin | top | 3 | 0.1843 | 0.3333 | 0.5528 | 0 | 0 | 1 | -0.4523 | 0.0000 | -0.4523 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-BRK-4H/scored | frozen3.0 | 1h | mem_twin | bot | 3 | 0.3197 | 0.3333 | 0.9592 | 0 | 0 | 2 | 0.6336 | 0.5000 | 1.2671 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-BRK-4H/scored | frozen3.0 | 1h | mem_twin | none | 316 | 0.0464 | 0.3544 | 14.6733 | 0 | 0 | 109 | 0.2221 | 0.3945 | 24.2083 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-BRK-4H/scored | frozen3.0 | 4h | record | both | 4 | 4.0583 | 0.7500 | 16.2332 | 0 | 0 | 2 | 8.2188 | 1.0000 | 16.4376 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-BRK-4H/scored | frozen3.0 | 4h | record | top | 1 | -0.3551 | 0.0000 | -0.3551 | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-BRK-4H/scored | frozen3.0 | 4h | record | bot | 9 | -0.3820 | 0.2222 | -3.4376 | 0 | 0 | 9 | -0.3820 | 0.2222 | -3.4376 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-BRK-4H/scored | frozen3.0 | 4h | record | none | 308 | 0.0122 | 0.3539 | 3.7449 | 0 | 0 | 101 | 0.1190 | 0.3960 | 12.0231 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-BRK-4H/scored | frozen3.0 | 4h | mem_twin | both | 4 | 4.0583 | 0.7500 | 16.2332 | 0 | 0 | 2 | 8.2188 | 1.0000 | 16.4376 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-BRK-4H/scored | frozen3.0 | 4h | mem_twin | top | 1 | -0.3551 | 0.0000 | -0.3551 | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-BRK-4H/scored | frozen3.0 | 4h | mem_twin | bot | 9 | -0.3820 | 0.2222 | -3.4376 | 0 | 0 | 9 | -0.3820 | 0.2222 | -3.4376 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-BRK-4H/scored | frozen3.0 | 4h | mem_twin | none | 308 | 0.0122 | 0.3539 | 3.7449 | 0 | 0 | 101 | 0.1190 | 0.3960 | 12.0231 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-BRK-4H/scored | frozen3.0 | 12h | record | both | 10 | -0.1474 | 0.3000 | -1.4738 | 0 | 0 | 5 | -0.4291 | 0.2000 | -2.1457 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-BRK-4H/scored | frozen3.0 | 12h | record | top | 23 | 0.1326 | 0.4783 | 3.0488 | 0 | 0 | 8 | 0.6149 | 0.7500 | 4.9188 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-BRK-4H/scored | frozen3.0 | 12h | record | bot | 25 | 0.0673 | 0.4000 | 1.6820 | 0 | 0 | 4 | 0.2013 | 0.7500 | 0.8052 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-BRK-4H/scored | frozen3.0 | 12h | record | none | 264 | 0.0490 | 0.3409 | 12.9283 | 0 | 0 | 95 | 0.2257 | 0.3579 | 21.4448 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-BRK-4H/scored | frozen3.0 | 12h | mem_twin | both | 13 | -0.0715 | 0.3846 | -0.9289 | 0 | 0 | 8 | -0.2001 | 0.3750 | -1.6007 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-BRK-4H/scored | frozen3.0 | 12h | mem_twin | top | 26 | 0.2836 | 0.5000 | 7.3723 | 0 | 0 | 10 | 0.4830 | 0.7000 | 4.8297 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-BRK-4H/scored | frozen3.0 | 12h | mem_twin | bot | 24 | 0.0817 | 0.3750 | 1.9598 | 0 | 0 | 2 | 0.9165 | 1.0000 | 1.8330 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-BRK-4H/scored | frozen3.0 | 12h | mem_twin | none | 259 | 0.0300 | 0.3359 | 7.7821 | 0 | 0 | 92 | 0.2170 | 0.3478 | 19.9612 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-BRK-4H/scored | frozen3.0 | 1d | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-BRK-4H/scored | frozen3.0 | 1d | record | top | 2 | -0.3902 | 0.5000 | -0.7803 | 0 | 0 | 2 | -0.3902 | 0.5000 | -0.7803 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-BRK-4H/scored | frozen3.0 | 1d | record | bot | 2 | -1.0219 | 0.0000 | -2.0438 | 0 | 0 | 2 | -1.0219 | 0.0000 | -2.0438 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-BRK-4H/scored | frozen3.0 | 1d | record | none | 318 | 0.0598 | 0.3553 | 19.0095 | 0 | 0 | 108 | 0.2578 | 0.3981 | 27.8473 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-BRK-4H/scored | frozen3.0 | 1d | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-BRK-4H/scored | frozen3.0 | 1d | mem_twin | top | 2 | -0.3902 | 0.5000 | -0.7803 | 0 | 0 | 2 | -0.3902 | 0.5000 | -0.7803 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-BRK-4H/scored | frozen3.0 | 1d | mem_twin | bot | 2 | -1.0219 | 0.0000 | -2.0438 | 0 | 0 | 2 | -1.0219 | 0.0000 | -2.0438 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-BRK-4H/scored | frozen3.0 | 1d | mem_twin | none | 318 | 0.0598 | 0.3553 | 19.0095 | 0 | 0 | 108 | 0.2578 | 0.3981 | 27.8473 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-BRK-4H/scored | frozen3.0 | 1w | record | NA | 322 | 0.0503 | 0.3540 | 16.1853 | 0 | 0 | 112 | 0.2234 | 0.3929 | 25.0231 | 1w | 1w: frozen3.0 | 1w: none |
| P-BRK-4H/scored | frozen3.0 | 1w | mem_twin | NA | 322 | 0.0503 | 0.3540 | 16.1853 | 0 | 0 | 112 | 0.2234 | 0.3929 | 25.0231 | 1w | 1w: frozen3.0 | 1w: none |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | record | both | 11 | -0.1061 | 0.4545 | -1.1666 | 7 | 9 | 4 | -0.4190 | 0.5000 | -1.6760 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) | 1h: BTCUSDT,SOLUSDT,NEARUSDT,ENAUSDT,MNTUSDT_BYBIT,SUIUSDT,LTCUSDT,XMRUSDT,BNBUSDT,1000BONKUSDT; 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | record | top | 26 | -0.1497 | 0.3462 | -3.8919 | 16 | 19 | 11 | 0.0054 | 0.3636 | 0.0592 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) | 1h: BTCUSDT,SOLUSDT,NEARUSDT,ENAUSDT,MNTUSDT_BYBIT,SUIUSDT,LTCUSDT,XMRUSDT,BNBUSDT,1000BONKUSDT; 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | record | bot | 24 | -0.2938 | 0.2083 | -7.0520 | 18 | 20 | 6 | -0.1871 | 0.1667 | -1.1228 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) | 1h: BTCUSDT,SOLUSDT,NEARUSDT,ENAUSDT,MNTUSDT_BYBIT,SUIUSDT,LTCUSDT,XMRUSDT,BNBUSDT,1000BONKUSDT; 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | record | none | 701 | 0.1446 | 0.3752 | 101.3592 | 413 | 553 | 313 | 0.3364 | 0.4026 | 105.2882 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) | 1h: BTCUSDT,SOLUSDT,NEARUSDT,ENAUSDT,MNTUSDT_BYBIT,SUIUSDT,LTCUSDT,XMRUSDT,BNBUSDT,1000BONKUSDT; 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | mem_twin | both | 11 | -0.1061 | 0.4545 | -1.1666 | 7 | 9 | 4 | -0.4190 | 0.5000 | -1.6760 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) | 1h: BTCUSDT,SOLUSDT,NEARUSDT,ENAUSDT,MNTUSDT_BYBIT,SUIUSDT,LTCUSDT,XMRUSDT,BNBUSDT,1000BONKUSDT; 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | mem_twin | top | 28 | -0.1765 | 0.3214 | -4.9423 | 18 | 20 | 11 | 0.0054 | 0.3636 | 0.0592 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) | 1h: BTCUSDT,SOLUSDT,NEARUSDT,ENAUSDT,MNTUSDT_BYBIT,SUIUSDT,LTCUSDT,XMRUSDT,BNBUSDT,1000BONKUSDT; 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | mem_twin | bot | 27 | -0.3034 | 0.2222 | -8.1921 | 20 | 23 | 7 | -0.2578 | 0.1429 | -1.8043 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) | 1h: BTCUSDT,SOLUSDT,NEARUSDT,ENAUSDT,MNTUSDT_BYBIT,SUIUSDT,LTCUSDT,XMRUSDT,BNBUSDT,1000BONKUSDT; 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 1h | mem_twin | none | 696 | 0.1488 | 0.3764 | 103.5497 | 409 | 549 | 312 | 0.3396 | 0.4038 | 105.9698 | 1h+4h | 1h: tuning / whole-tape (fallback); 4h: tuning / whole-tape (fallback) | 1h: BTCUSDT,SOLUSDT,NEARUSDT,ENAUSDT,MNTUSDT_BYBIT,SUIUSDT,LTCUSDT,XMRUSDT,BNBUSDT,1000BONKUSDT; 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning | 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | top | 6 | 0.1403 | 0.5000 | 0.8421 | 5 | 5 | 1 | -0.8563 | 0.0000 | -0.8563 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning | 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | bot | 6 | -0.3538 | 0.3333 | -2.1227 | 3 | 2 | 3 | -0.2231 | 0.3333 | -0.6692 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning | 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | none | 310 | 0.0563 | 0.3516 | 17.4659 | 202 | 240 | 108 | 0.2458 | 0.3981 | 26.5486 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning | 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | record | NA | 440 | 0.1661 | 0.3818 | 73.0633 | 244 | 222 | 222 | 0.3492 | 0.4009 | 77.5256 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning | 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning | 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | top | 7 | 0.1917 | 0.5714 | 1.3419 | 5 | 6 | 2 | -0.1782 | 0.5000 | -0.3564 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning | 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | bot | 6 | -0.3538 | 0.3333 | -2.1227 | 3 | 2 | 3 | -0.2231 | 0.3333 | -0.6692 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning | 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | none | 309 | 0.0549 | 0.3495 | 16.9661 | 202 | 239 | 107 | 0.2434 | 0.3925 | 26.0488 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning | 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 4h | mem_twin | NA | 440 | 0.1661 | 0.3818 | 73.0633 | 244 | 222 | 222 | 0.3492 | 0.4009 | 77.5256 | 4h+12h | 4h: tuning / whole-tape (fallback); 12h: tuning | 4h: NEARUSDT,MNTUSDT_BYBIT,XMRUSDT,UNIUSDT,1000PEPEUSDT,DOGEUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | both | 15 | 0.5748 | 0.4000 | 8.6216 | 11 | 8 | 4 | 0.9140 | 0.2500 | 3.6559 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | top | 13 | 0.1424 | 0.4615 | 1.8509 | 7 | 8 | 6 | 0.6280 | 0.6667 | 3.7682 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | bot | 16 | -0.2024 | 0.3750 | -3.2380 | 6 | 9 | 10 | -0.0573 | 0.5000 | -0.5725 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | none | 278 | 0.0322 | 0.3453 | 8.9508 | 186 | 159 | 92 | 0.1975 | 0.3696 | 18.1716 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | record | NA | 440 | 0.1661 | 0.3818 | 73.0633 | 298 | 189 | 222 | 0.3492 | 0.4009 | 77.5256 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | both | 18 | 0.5093 | 0.4444 | 9.1665 | 11 | 11 | 7 | 0.6001 | 0.4286 | 4.2008 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | top | 19 | 0.0439 | 0.4737 | 0.8343 | 10 | 13 | 9 | 0.4301 | 0.6667 | 3.8710 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | bot | 21 | -0.3223 | 0.2857 | -6.7688 | 13 | 13 | 8 | -0.2424 | 0.3750 | -1.9394 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | none | 264 | 0.0491 | 0.3447 | 12.9533 | 176 | 147 | 88 | 0.2147 | 0.3636 | 18.8907 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 12h | mem_twin | NA | 440 | 0.1661 | 0.3818 | 73.0633 | 298 | 189 | 222 | 0.3492 | 0.4009 | 77.5256 | 12h+1d | 12h: tuning; 1d: tuning / whole-tape (fallback) | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT; 1w: none |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | top | 1 | 0.2602 | 1.0000 | 0.2602 | 1 | 1 | 1 | 0.2602 | 1.0000 | 0.2602 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT; 1w: none |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | bot | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT; 1w: none |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | none | 321 | 0.0496 | 0.3520 | 15.9251 | 321 | 123 | 111 | 0.2231 | 0.3874 | 24.7629 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT; 1w: none |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | record | NA | 440 | 0.1661 | 0.3818 | 73.0633 | 298 | 189 | 222 | 0.3492 | 0.4009 | 77.5256 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT; 1w: none |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT; 1w: none |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | top | 1 | 0.2602 | 1.0000 | 0.2602 | 1 | 1 | 1 | 0.2602 | 1.0000 | 0.2602 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT; 1w: none |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | bot | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT; 1w: none |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | none | 321 | 0.0496 | 0.3520 | 15.9251 | 321 | 123 | 111 | 0.2231 | 0.3874 | 24.7629 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT; 1w: none |
| P-BRK-4H/tierE__panel17 | calibrated | 1d | mem_twin | NA | 440 | 0.1661 | 0.3818 | 73.0633 | 298 | 189 | 222 | 0.3492 | 0.4009 | 77.5256 | 1d+1w | 1d: tuning / whole-tape (fallback); 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT,XMRUSDT,BNBUSDT,1000PEPEUSDT,DOGEUSDT; 1w: none |
| P-BRK-4H/tierE__panel17 | calibrated | 1w | record | NA | 762 | 0.1171 | 0.3701 | 89.2486 | 322 | 0 | 334 | 0.3070 | 0.3982 | 102.5487 | 1w | 1w: whole-tape (fallback) | 1w: none |
| P-BRK-4H/tierE__panel17 | calibrated | 1w | mem_twin | NA | 762 | 0.1171 | 0.3701 | 89.2486 | 322 | 0 | 334 | 0.3070 | 0.3982 | 102.5487 | 1w | 1w: whole-tape (fallback) | 1w: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | record | both | 1 | -0.5941 | 0.0000 | -0.5941 | 0 | 0 | 0 | — | — | — | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | record | top | 8 | -0.0495 | 0.3750 | -0.3962 | 0 | 0 | 5 | -0.2523 | 0.4000 | -1.2614 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | record | bot | 9 | -0.0227 | 0.4444 | -0.2043 | 0 | 0 | 3 | 0.1570 | 0.3333 | 0.4710 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | record | none | 744 | 0.1216 | 0.3696 | 90.4432 | 0 | 0 | 326 | 0.3170 | 0.3988 | 103.3391 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | mem_twin | both | 1 | -0.5941 | 0.0000 | -0.5941 | 0 | 0 | 0 | — | — | — | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | mem_twin | top | 8 | -0.0495 | 0.3750 | -0.3962 | 0 | 0 | 5 | -0.2523 | 0.4000 | -1.2614 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | mem_twin | bot | 10 | -0.0600 | 0.4000 | -0.5996 | 0 | 0 | 3 | 0.1570 | 0.3333 | 0.4710 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1h | mem_twin | none | 743 | 0.1223 | 0.3701 | 90.8384 | 0 | 0 | 326 | 0.3170 | 0.3988 | 103.3391 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | both | 4 | 4.0583 | 0.7500 | 16.2332 | 0 | 0 | 2 | 8.2188 | 1.0000 | 16.4376 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | top | 1 | -0.3551 | 0.0000 | -0.3551 | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | bot | 9 | -0.3820 | 0.2222 | -3.4376 | 0 | 0 | 9 | -0.3820 | 0.2222 | -3.4376 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | none | 308 | 0.0122 | 0.3539 | 3.7449 | 0 | 0 | 101 | 0.1190 | 0.3960 | 12.0231 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | record | NA | 440 | 0.1661 | 0.3818 | 73.0633 | 0 | 0 | 222 | 0.3492 | 0.4009 | 77.5256 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | both | 4 | 4.0583 | 0.7500 | 16.2332 | 0 | 0 | 2 | 8.2188 | 1.0000 | 16.4376 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | top | 1 | -0.3551 | 0.0000 | -0.3551 | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | bot | 9 | -0.3820 | 0.2222 | -3.4376 | 0 | 0 | 9 | -0.3820 | 0.2222 | -3.4376 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | none | 308 | 0.0122 | 0.3539 | 3.7449 | 0 | 0 | 101 | 0.1190 | 0.3960 | 12.0231 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 4h | mem_twin | NA | 440 | 0.1661 | 0.3818 | 73.0633 | 0 | 0 | 222 | 0.3492 | 0.4009 | 77.5256 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | both | 10 | -0.1474 | 0.3000 | -1.4738 | 0 | 0 | 5 | -0.4291 | 0.2000 | -2.1457 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | top | 23 | 0.1326 | 0.4783 | 3.0488 | 0 | 0 | 8 | 0.6149 | 0.7500 | 4.9188 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | bot | 25 | 0.0673 | 0.4000 | 1.6820 | 0 | 0 | 4 | 0.2013 | 0.7500 | 0.8052 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | none | 264 | 0.0490 | 0.3409 | 12.9283 | 0 | 0 | 95 | 0.2257 | 0.3579 | 21.4448 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | record | NA | 440 | 0.1661 | 0.3818 | 73.0633 | 0 | 0 | 222 | 0.3492 | 0.4009 | 77.5256 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | both | 13 | -0.0715 | 0.3846 | -0.9289 | 0 | 0 | 8 | -0.2001 | 0.3750 | -1.6007 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | top | 26 | 0.2836 | 0.5000 | 7.3723 | 0 | 0 | 10 | 0.4830 | 0.7000 | 4.8297 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | bot | 24 | 0.0817 | 0.3750 | 1.9598 | 0 | 0 | 2 | 0.9165 | 1.0000 | 1.8330 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | none | 259 | 0.0300 | 0.3359 | 7.7821 | 0 | 0 | 92 | 0.2170 | 0.3478 | 19.9612 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 12h | mem_twin | NA | 440 | 0.1661 | 0.3818 | 73.0633 | 0 | 0 | 222 | 0.3492 | 0.4009 | 77.5256 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | top | 2 | -0.3902 | 0.5000 | -0.7803 | 0 | 0 | 2 | -0.3902 | 0.5000 | -0.7803 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | bot | 2 | -1.0219 | 0.0000 | -2.0438 | 0 | 0 | 2 | -1.0219 | 0.0000 | -2.0438 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | none | 318 | 0.0598 | 0.3553 | 19.0095 | 0 | 0 | 108 | 0.2578 | 0.3981 | 27.8473 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | record | NA | 440 | 0.1661 | 0.3818 | 73.0633 | 0 | 0 | 222 | 0.3492 | 0.4009 | 77.5256 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | top | 2 | -0.3902 | 0.5000 | -0.7803 | 0 | 0 | 2 | -0.3902 | 0.5000 | -0.7803 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | bot | 2 | -1.0219 | 0.0000 | -2.0438 | 0 | 0 | 2 | -1.0219 | 0.0000 | -2.0438 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | none | 318 | 0.0598 | 0.3553 | 19.0095 | 0 | 0 | 108 | 0.2578 | 0.3981 | 27.8473 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1d | mem_twin | NA | 440 | 0.1661 | 0.3818 | 73.0633 | 0 | 0 | 222 | 0.3492 | 0.4009 | 77.5256 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1w | record | NA | 762 | 0.1171 | 0.3701 | 89.2486 | 0 | 0 | 334 | 0.3070 | 0.3982 | 102.5487 | 1w | 1w: frozen3.0 | 1w: none |
| P-BRK-4H/tierE__panel17 | frozen3.0 | 1w | mem_twin | NA | 762 | 0.1171 | 0.3701 | 89.2486 | 0 | 0 | 334 | 0.3070 | 0.3982 | 102.5487 | 1w | 1w: frozen3.0 | 1w: none |
| P-RELAY-1/scored | calibrated | 1h | record | both | 1 | -1.0356 | 0.0000 | -1.0356 | 1 | 1 | 0 | — | — | — | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-RELAY-1/scored | calibrated | 1h | record | top | 3 | -0.6697 | 0.3333 | -2.0091 | 2 | 2 | 1 | -1.0410 | 0.0000 | -1.0410 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-RELAY-1/scored | calibrated | 1h | record | bot | 9 | -0.3564 | 0.2222 | -3.2072 | 7 | 8 | 2 | -0.7731 | 0.0000 | -1.5462 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-RELAY-1/scored | calibrated | 1h | record | none | 160 | 0.5296 | 0.3500 | 84.7317 | 104 | 101 | 56 | 0.8032 | 0.3571 | 44.9813 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-RELAY-1/scored | calibrated | 1h | mem_twin | both | 1 | -1.0356 | 0.0000 | -1.0356 | 1 | 1 | 0 | — | — | — | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-RELAY-1/scored | calibrated | 1h | mem_twin | top | 3 | -0.6697 | 0.3333 | -2.0091 | 2 | 2 | 1 | -1.0410 | 0.0000 | -1.0410 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-RELAY-1/scored | calibrated | 1h | mem_twin | bot | 10 | -0.4284 | 0.2000 | -4.2844 | 8 | 9 | 2 | -0.7731 | 0.0000 | -1.5462 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-RELAY-1/scored | calibrated | 1h | mem_twin | none | 159 | 0.5397 | 0.3522 | 85.8089 | 103 | 100 | 56 | 0.8032 | 0.3571 | 44.9813 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-RELAY-1/scored | calibrated | 4h | record | both | 10 | -0.4621 | 0.2000 | -4.6213 | 7 | 10 | 3 | -0.4381 | 0.3333 | -1.3143 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 4h | record | top | 13 | 2.1676 | 0.3077 | 28.1783 | 8 | 12 | 5 | -0.5524 | 0.2000 | -2.7621 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 4h | record | bot | 8 | -0.2991 | 0.2500 | -2.3926 | 4 | 6 | 4 | -0.5815 | 0.2500 | -2.3259 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 4h | record | none | 142 | 0.4036 | 0.3592 | 57.3154 | 95 | 117 | 47 | 1.0382 | 0.3617 | 48.7965 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 4h | mem_twin | both | 10 | -0.4621 | 0.2000 | -4.6213 | 7 | 10 | 3 | -0.4381 | 0.3333 | -1.3143 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 4h | mem_twin | top | 13 | 2.1676 | 0.3077 | 28.1783 | 8 | 12 | 5 | -0.5524 | 0.2000 | -2.7621 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 4h | mem_twin | bot | 9 | -0.1470 | 0.3333 | -1.3233 | 4 | 7 | 5 | -0.2513 | 0.4000 | -1.2566 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 4h | mem_twin | none | 141 | 0.3989 | 0.3546 | 56.2460 | 95 | 116 | 46 | 1.0375 | 0.3478 | 47.7271 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 12h | record | both | 4 | -0.2379 | 0.5000 | -0.9517 | 2 | 0 | 2 | 0.1224 | 1.0000 | 0.2448 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 12h | record | top | 10 | 2.4612 | 0.4000 | 24.6121 | 4 | 6 | 6 | 3.5490 | 0.5000 | 21.2938 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 12h | record | bot | 11 | 1.7026 | 0.4545 | 18.7287 | 8 | 10 | 3 | 1.9000 | 0.6667 | 5.6999 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 12h | record | none | 148 | 0.2439 | 0.3243 | 36.0906 | 100 | 97 | 48 | 0.3157 | 0.2708 | 15.1556 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 12h | mem_twin | both | 6 | 0.9597 | 0.6667 | 5.7583 | 2 | 2 | 4 | 1.7387 | 1.0000 | 6.9548 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 12h | mem_twin | top | 12 | 1.9213 | 0.3333 | 23.0556 | 5 | 8 | 7 | 2.9656 | 0.4286 | 20.7595 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 12h | mem_twin | bot | 12 | 0.8020 | 0.2500 | 9.6238 | 11 | 11 | 1 | -1.0100 | 0.0000 | -1.0100 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 12h | mem_twin | none | 143 | 0.2800 | 0.3357 | 40.0421 | 96 | 92 | 47 | 0.3338 | 0.2766 | 15.6899 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-RELAY-1/scored | calibrated | 1d | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-RELAY-1/scored | calibrated | 1d | record | top | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-RELAY-1/scored | calibrated | 1d | record | bot | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-RELAY-1/scored | calibrated | 1d | record | none | 173 | 0.4536 | 0.3410 | 78.4797 | 173 | 80 | 59 | 0.7185 | 0.3390 | 42.3942 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-RELAY-1/scored | calibrated | 1d | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-RELAY-1/scored | calibrated | 1d | mem_twin | top | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-RELAY-1/scored | calibrated | 1d | mem_twin | bot | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-RELAY-1/scored | calibrated | 1d | mem_twin | none | 173 | 0.4536 | 0.3410 | 78.4797 | 173 | 80 | 59 | 0.7185 | 0.3390 | 42.3942 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-RELAY-1/scored | calibrated | 1w | record | NA | 173 | 0.4536 | 0.3410 | 78.4797 | 173 | 0 | 59 | 0.7185 | 0.3390 | 42.3942 | 1w | 1w: whole-tape (fallback) | 1w: none |
| P-RELAY-1/scored | calibrated | 1w | mem_twin | NA | 173 | 0.4536 | 0.3410 | 78.4797 | 173 | 0 | 59 | 0.7185 | 0.3390 | 42.3942 | 1w | 1w: whole-tape (fallback) | 1w: none |
| P-RELAY-1/scored | frozen3.0 | 1h | record | both | 2 | 14.6853 | 1.0000 | 29.3706 | 0 | 0 | 1 | 0.8246 | 1.0000 | 0.8246 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-RELAY-1/scored | frozen3.0 | 1h | record | top | 7 | -0.4349 | 0.1429 | -3.0444 | 0 | 0 | 2 | -0.6881 | 0.0000 | -1.3761 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-RELAY-1/scored | frozen3.0 | 1h | record | bot | 2 | -0.1834 | 0.5000 | -0.3669 | 0 | 0 | 2 | -0.1834 | 0.5000 | -0.3669 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-RELAY-1/scored | frozen3.0 | 1h | record | none | 162 | 0.3242 | 0.3395 | 52.5204 | 0 | 0 | 54 | 0.8021 | 0.3333 | 43.3126 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-RELAY-1/scored | frozen3.0 | 1h | mem_twin | both | 2 | 14.6853 | 1.0000 | 29.3706 | 0 | 0 | 1 | 0.8246 | 1.0000 | 0.8246 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-RELAY-1/scored | frozen3.0 | 1h | mem_twin | top | 7 | -0.4349 | 0.1429 | -3.0444 | 0 | 0 | 2 | -0.6881 | 0.0000 | -1.3761 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-RELAY-1/scored | frozen3.0 | 1h | mem_twin | bot | 2 | -0.1834 | 0.5000 | -0.3669 | 0 | 0 | 2 | -0.1834 | 0.5000 | -0.3669 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-RELAY-1/scored | frozen3.0 | 1h | mem_twin | none | 162 | 0.3242 | 0.3395 | 52.5204 | 0 | 0 | 54 | 0.8021 | 0.3333 | 43.3126 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-RELAY-1/scored | frozen3.0 | 4h | record | both | 5 | -0.4762 | 0.2000 | -2.3812 | 0 | 0 | 1 | 0.0871 | 1.0000 | 0.0871 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-RELAY-1/scored | frozen3.0 | 4h | record | top | 4 | 1.6893 | 0.7500 | 6.7572 | 0 | 0 | 1 | 0.4145 | 1.0000 | 0.4145 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-RELAY-1/scored | frozen3.0 | 4h | record | bot | 11 | -0.6093 | 0.1818 | -6.7020 | 0 | 0 | 9 | -0.5980 | 0.2222 | -5.3818 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-RELAY-1/scored | frozen3.0 | 4h | record | none | 153 | 0.5281 | 0.3464 | 80.8058 | 0 | 0 | 48 | 0.9849 | 0.3333 | 47.2743 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-RELAY-1/scored | frozen3.0 | 4h | mem_twin | both | 5 | -0.4762 | 0.2000 | -2.3812 | 0 | 0 | 1 | 0.0871 | 1.0000 | 0.0871 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-RELAY-1/scored | frozen3.0 | 4h | mem_twin | top | 4 | 1.6893 | 0.7500 | 6.7572 | 0 | 0 | 1 | 0.4145 | 1.0000 | 0.4145 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-RELAY-1/scored | frozen3.0 | 4h | mem_twin | bot | 11 | -0.6093 | 0.1818 | -6.7020 | 0 | 0 | 9 | -0.5980 | 0.2222 | -5.3818 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-RELAY-1/scored | frozen3.0 | 4h | mem_twin | none | 153 | 0.5281 | 0.3464 | 80.8058 | 0 | 0 | 48 | 0.9849 | 0.3333 | 47.2743 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-RELAY-1/scored | frozen3.0 | 12h | record | both | 2 | 0.6462 | 0.5000 | 1.2923 | 0 | 0 | 0 | — | — | — | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-RELAY-1/scored | frozen3.0 | 12h | record | top | 15 | 0.3744 | 0.3333 | 5.6160 | 0 | 0 | 6 | 0.0088 | 0.1667 | 0.0531 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-RELAY-1/scored | frozen3.0 | 12h | record | bot | 9 | 2.3950 | 0.5556 | 21.5553 | 0 | 0 | 2 | 3.3550 | 1.0000 | 6.7100 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-RELAY-1/scored | frozen3.0 | 12h | record | none | 147 | 0.3402 | 0.3265 | 50.0161 | 0 | 0 | 51 | 0.6986 | 0.3333 | 35.6311 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-RELAY-1/scored | frozen3.0 | 12h | mem_twin | both | 4 | 2.0006 | 0.7500 | 8.0023 | 0 | 0 | 2 | 3.3550 | 1.0000 | 6.7100 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-RELAY-1/scored | frozen3.0 | 12h | mem_twin | top | 16 | 0.3015 | 0.3125 | 4.8232 | 0 | 0 | 6 | 0.0088 | 0.1667 | 0.0531 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-RELAY-1/scored | frozen3.0 | 12h | mem_twin | bot | 8 | 2.0152 | 0.5000 | 16.1217 | 0 | 0 | 0 | — | — | — | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-RELAY-1/scored | frozen3.0 | 12h | mem_twin | none | 145 | 0.3416 | 0.3241 | 49.5325 | 0 | 0 | 51 | 0.6986 | 0.3333 | 35.6311 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-RELAY-1/scored | frozen3.0 | 1d | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-RELAY-1/scored | frozen3.0 | 1d | record | top | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-RELAY-1/scored | frozen3.0 | 1d | record | bot | 1 | -1.0082 | 0.0000 | -1.0082 | 0 | 0 | 1 | -1.0082 | 0.0000 | -1.0082 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-RELAY-1/scored | frozen3.0 | 1d | record | none | 172 | 0.4621 | 0.3430 | 79.4879 | 0 | 0 | 58 | 0.7483 | 0.3448 | 43.4023 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-RELAY-1/scored | frozen3.0 | 1d | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-RELAY-1/scored | frozen3.0 | 1d | mem_twin | top | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-RELAY-1/scored | frozen3.0 | 1d | mem_twin | bot | 1 | -1.0082 | 0.0000 | -1.0082 | 0 | 0 | 1 | -1.0082 | 0.0000 | -1.0082 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-RELAY-1/scored | frozen3.0 | 1d | mem_twin | none | 172 | 0.4621 | 0.3430 | 79.4879 | 0 | 0 | 58 | 0.7483 | 0.3448 | 43.4023 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-RELAY-1/scored | frozen3.0 | 1w | record | NA | 173 | 0.4536 | 0.3410 | 78.4797 | 0 | 0 | 59 | 0.7185 | 0.3390 | 42.3942 | 1w | 1w: frozen3.0 | 1w: none |
| P-RELAY-1/scored | frozen3.0 | 1w | mem_twin | NA | 173 | 0.4536 | 0.3410 | 78.4797 | 0 | 0 | 59 | 0.7185 | 0.3390 | 42.3942 | 1w | 1w: frozen3.0 | 1w: none |
| P-ADD-BRK/scored | calibrated | 1h | record | both | 4 | 2.7870 | 0.5000 | 11.1482 | 2 | 2 | 2 | 5.3739 | 0.5000 | 10.7478 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-ADD-BRK/scored | calibrated | 1h | record | top | 9 | 0.2108 | 0.3333 | 1.8970 | 4 | 3 | 5 | 0.8150 | 0.4000 | 4.0748 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-ADD-BRK/scored | calibrated | 1h | record | bot | 17 | 0.4143 | 0.4118 | 7.0428 | 12 | 11 | 5 | 1.4711 | 0.4000 | 7.3556 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-ADD-BRK/scored | calibrated | 1h | record | none | 170 | 0.0981 | 0.2941 | 16.6829 | 105 | 99 | 65 | 0.2533 | 0.2769 | 16.4671 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-ADD-BRK/scored | calibrated | 1h | mem_twin | both | 4 | 2.7870 | 0.5000 | 11.1482 | 2 | 2 | 2 | 5.3739 | 0.5000 | 10.7478 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-ADD-BRK/scored | calibrated | 1h | mem_twin | top | 10 | 0.0849 | 0.3000 | 0.8487 | 5 | 4 | 5 | 0.8150 | 0.4000 | 4.0748 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-ADD-BRK/scored | calibrated | 1h | mem_twin | bot | 19 | 0.2530 | 0.3684 | 4.8069 | 14 | 12 | 5 | 1.4711 | 0.4000 | 7.3556 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-ADD-BRK/scored | calibrated | 1h | mem_twin | none | 167 | 0.1196 | 0.2994 | 19.9670 | 102 | 97 | 65 | 0.2533 | 0.2769 | 16.4671 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-ADD-BRK/scored | calibrated | 4h | record | both | 9 | 0.3627 | 0.4444 | 3.2642 | 7 | 8 | 2 | -1.0485 | 0.0000 | -2.0970 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 4h | record | top | 8 | 0.7251 | 0.5000 | 5.8006 | 1 | 7 | 7 | 0.9626 | 0.5714 | 6.7380 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 4h | record | bot | 12 | 0.4902 | 0.2500 | 5.8826 | 5 | 11 | 7 | 0.8923 | 0.2857 | 6.2464 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 4h | record | none | 171 | 0.1276 | 0.2982 | 21.8234 | 110 | 137 | 61 | 0.4550 | 0.2787 | 27.7579 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 4h | mem_twin | both | 9 | 0.3627 | 0.4444 | 3.2642 | 7 | 8 | 2 | -1.0485 | 0.0000 | -2.0970 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 4h | mem_twin | top | 8 | 0.7251 | 0.5000 | 5.8006 | 1 | 7 | 7 | 0.9626 | 0.5714 | 6.7380 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 4h | mem_twin | bot | 13 | 0.7543 | 0.3077 | 9.8054 | 6 | 11 | 7 | 0.8923 | 0.2857 | 6.2464 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 4h | mem_twin | none | 170 | 0.1053 | 0.2941 | 17.9006 | 109 | 137 | 61 | 0.4550 | 0.2787 | 27.7579 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 12h | record | both | 6 | 0.8410 | 0.3333 | 5.0461 | 4 | 3 | 2 | -0.6436 | 0.0000 | -1.2872 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 12h | record | top | 4 | -1.1762 | 0.0000 | -4.7050 | 1 | 2 | 3 | -1.2471 | 0.0000 | -3.7412 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 12h | record | bot | 13 | 0.8408 | 0.4615 | 10.9303 | 5 | 8 | 8 | 1.3671 | 0.5000 | 10.9369 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 12h | record | none | 177 | 0.1441 | 0.3051 | 25.4994 | 113 | 110 | 64 | 0.5115 | 0.2969 | 32.7367 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 12h | mem_twin | both | 7 | 0.5644 | 0.2857 | 3.9506 | 4 | 4 | 3 | -0.7942 | 0.0000 | -2.3827 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 12h | mem_twin | top | 9 | -1.0135 | 0.0000 | -9.1216 | 3 | 6 | 6 | -1.1101 | 0.0000 | -6.6605 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 12h | mem_twin | bot | 15 | 0.7267 | 0.4667 | 10.9010 | 8 | 10 | 7 | 1.7189 | 0.5714 | 12.0324 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 12h | mem_twin | none | 169 | 0.1837 | 0.3136 | 31.0409 | 108 | 103 | 61 | 0.5845 | 0.3115 | 35.6561 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-ADD-BRK/scored | calibrated | 1d | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-ADD-BRK/scored | calibrated | 1d | record | top | 1 | 4.7099 | 1.0000 | 4.7099 | 1 | 1 | 1 | 4.7099 | 1.0000 | 4.7099 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-ADD-BRK/scored | calibrated | 1d | record | bot | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-ADD-BRK/scored | calibrated | 1d | record | none | 199 | 0.1611 | 0.3065 | 32.0610 | 199 | 74 | 76 | 0.4465 | 0.2895 | 33.9354 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-ADD-BRK/scored | calibrated | 1d | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-ADD-BRK/scored | calibrated | 1d | mem_twin | top | 1 | 4.7099 | 1.0000 | 4.7099 | 1 | 1 | 1 | 4.7099 | 1.0000 | 4.7099 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-ADD-BRK/scored | calibrated | 1d | mem_twin | bot | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-ADD-BRK/scored | calibrated | 1d | mem_twin | none | 199 | 0.1611 | 0.3065 | 32.0610 | 199 | 74 | 76 | 0.4465 | 0.2895 | 33.9354 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-ADD-BRK/scored | calibrated | 1w | record | NA | 200 | 0.1839 | 0.3100 | 36.7709 | 200 | 0 | 77 | 0.5019 | 0.2987 | 38.6452 | 1w | 1w: whole-tape (fallback) | 1w: none |
| P-ADD-BRK/scored | calibrated | 1w | mem_twin | NA | 200 | 0.1839 | 0.3100 | 36.7709 | 200 | 0 | 77 | 0.5019 | 0.2987 | 38.6452 | 1w | 1w: whole-tape (fallback) | 1w: none |
| P-ADD-BRK/scored | frozen3.0 | 1h | record | both | 1 | -0.9374 | 0.0000 | -0.9374 | 0 | 0 | 0 | — | — | — | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-ADD-BRK/scored | frozen3.0 | 1h | record | top | 9 | 0.3227 | 0.3333 | 2.9045 | 0 | 0 | 6 | 0.9159 | 0.5000 | 5.4957 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-ADD-BRK/scored | frozen3.0 | 1h | record | bot | 2 | -0.5115 | 0.5000 | -1.0231 | 0 | 0 | 1 | -1.0349 | 0.0000 | -1.0349 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-ADD-BRK/scored | frozen3.0 | 1h | record | none | 188 | 0.1906 | 0.3085 | 35.8269 | 0 | 0 | 70 | 0.4884 | 0.2857 | 34.1845 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-ADD-BRK/scored | frozen3.0 | 1h | mem_twin | both | 1 | -0.9374 | 0.0000 | -0.9374 | 0 | 0 | 0 | — | — | — | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-ADD-BRK/scored | frozen3.0 | 1h | mem_twin | top | 10 | 1.1290 | 0.4000 | 11.2898 | 0 | 0 | 7 | 1.9830 | 0.5714 | 13.8809 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-ADD-BRK/scored | frozen3.0 | 1h | mem_twin | bot | 2 | -0.5115 | 0.5000 | -1.0231 | 0 | 0 | 1 | -1.0349 | 0.0000 | -1.0349 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-ADD-BRK/scored | frozen3.0 | 1h | mem_twin | none | 187 | 0.1467 | 0.3048 | 27.4416 | 0 | 0 | 69 | 0.3739 | 0.2754 | 25.7993 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-ADD-BRK/scored | frozen3.0 | 4h | record | both | 5 | -0.5545 | 0.2000 | -2.7724 | 0 | 0 | 1 | -0.7735 | 0.0000 | -0.7735 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-ADD-BRK/scored | frozen3.0 | 4h | record | top | 3 | 1.2463 | 1.0000 | 3.7390 | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-ADD-BRK/scored | frozen3.0 | 4h | record | bot | 13 | -0.7192 | 0.1538 | -9.3499 | 0 | 0 | 10 | -0.6559 | 0.2000 | -6.5590 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-ADD-BRK/scored | frozen3.0 | 4h | record | none | 179 | 0.2523 | 0.3128 | 45.1542 | 0 | 0 | 66 | 0.6966 | 0.3182 | 45.9777 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-ADD-BRK/scored | frozen3.0 | 4h | mem_twin | both | 5 | -0.5545 | 0.2000 | -2.7724 | 0 | 0 | 1 | -0.7735 | 0.0000 | -0.7735 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-ADD-BRK/scored | frozen3.0 | 4h | mem_twin | top | 3 | 1.2463 | 1.0000 | 3.7390 | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-ADD-BRK/scored | frozen3.0 | 4h | mem_twin | bot | 13 | -0.7192 | 0.1538 | -9.3499 | 0 | 0 | 10 | -0.6559 | 0.2000 | -6.5590 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-ADD-BRK/scored | frozen3.0 | 4h | mem_twin | none | 179 | 0.2523 | 0.3128 | 45.1542 | 0 | 0 | 66 | 0.6966 | 0.3182 | 45.9777 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-ADD-BRK/scored | frozen3.0 | 12h | record | both | 5 | 1.3513 | 0.4000 | 6.7567 | 0 | 0 | 3 | 2.7309 | 0.6667 | 8.1926 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-ADD-BRK/scored | frozen3.0 | 12h | record | top | 9 | -0.4617 | 0.1111 | -4.1551 | 0 | 0 | 4 | -1.0157 | 0.0000 | -4.0630 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-ADD-BRK/scored | frozen3.0 | 12h | record | bot | 9 | 0.1542 | 0.3333 | 1.3881 | 0 | 0 | 4 | 1.0515 | 0.5000 | 4.2062 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-ADD-BRK/scored | frozen3.0 | 12h | record | none | 177 | 0.1852 | 0.3164 | 32.7812 | 0 | 0 | 66 | 0.4592 | 0.2879 | 30.3095 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-ADD-BRK/scored | frozen3.0 | 12h | mem_twin | both | 6 | 0.9435 | 0.3333 | 5.6612 | 0 | 0 | 4 | 1.7743 | 0.5000 | 7.0971 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-ADD-BRK/scored | frozen3.0 | 12h | mem_twin | top | 9 | -0.4617 | 0.1111 | -4.1551 | 0 | 0 | 4 | -1.0157 | 0.0000 | -4.0630 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-ADD-BRK/scored | frozen3.0 | 12h | mem_twin | bot | 8 | 0.3104 | 0.3750 | 2.4835 | 0 | 0 | 3 | 1.7672 | 0.6667 | 5.3016 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-ADD-BRK/scored | frozen3.0 | 12h | mem_twin | none | 177 | 0.1852 | 0.3164 | 32.7812 | 0 | 0 | 66 | 0.4592 | 0.2879 | 30.3095 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-ADD-BRK/scored | frozen3.0 | 1d | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-ADD-BRK/scored | frozen3.0 | 1d | record | top | 2 | 1.8289 | 0.5000 | 3.6577 | 0 | 0 | 2 | 1.8289 | 0.5000 | 3.6577 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-ADD-BRK/scored | frozen3.0 | 1d | record | bot | 1 | 2.6755 | 1.0000 | 2.6755 | 0 | 0 | 1 | 2.6755 | 1.0000 | 2.6755 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-ADD-BRK/scored | frozen3.0 | 1d | record | none | 197 | 0.1545 | 0.3046 | 30.4376 | 0 | 0 | 74 | 0.4366 | 0.2838 | 32.3120 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-ADD-BRK/scored | frozen3.0 | 1d | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-ADD-BRK/scored | frozen3.0 | 1d | mem_twin | top | 2 | 1.8289 | 0.5000 | 3.6577 | 0 | 0 | 2 | 1.8289 | 0.5000 | 3.6577 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-ADD-BRK/scored | frozen3.0 | 1d | mem_twin | bot | 1 | 2.6755 | 1.0000 | 2.6755 | 0 | 0 | 1 | 2.6755 | 1.0000 | 2.6755 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-ADD-BRK/scored | frozen3.0 | 1d | mem_twin | none | 197 | 0.1545 | 0.3046 | 30.4376 | 0 | 0 | 74 | 0.4366 | 0.2838 | 32.3120 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-ADD-BRK/scored | frozen3.0 | 1w | record | NA | 200 | 0.1839 | 0.3100 | 36.7709 | 0 | 0 | 77 | 0.5019 | 0.2987 | 38.6452 | 1w | 1w: frozen3.0 | 1w: none |
| P-ADD-BRK/scored | frozen3.0 | 1w | mem_twin | NA | 200 | 0.1839 | 0.3100 | 36.7709 | 0 | 0 | 77 | 0.5019 | 0.2987 | 38.6452 | 1w | 1w: frozen3.0 | 1w: none |
| P-ADD-SFP/scored | calibrated | 1h | record | both | 4 | 2.4491 | 0.7500 | 9.7962 | 2 | 2 | 2 | 3.8599 | 0.5000 | 7.7198 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-ADD-SFP/scored | calibrated | 1h | record | top | 9 | 0.1857 | 0.3333 | 1.6713 | 4 | 3 | 5 | 0.5794 | 0.4000 | 2.8969 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-ADD-SFP/scored | calibrated | 1h | record | bot | 17 | 0.3939 | 0.4706 | 6.6959 | 12 | 11 | 5 | 1.4411 | 0.6000 | 7.2054 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-ADD-SFP/scored | calibrated | 1h | record | none | 170 | 0.1097 | 0.3176 | 18.6485 | 105 | 99 | 65 | 0.3356 | 0.3231 | 21.8122 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-ADD-SFP/scored | calibrated | 1h | mem_twin | both | 4 | 2.4491 | 0.7500 | 9.7962 | 2 | 2 | 2 | 3.8599 | 0.5000 | 7.7198 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-ADD-SFP/scored | calibrated | 1h | mem_twin | top | 10 | 0.0623 | 0.3000 | 0.6231 | 5 | 4 | 5 | 0.5794 | 0.4000 | 2.8969 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-ADD-SFP/scored | calibrated | 1h | mem_twin | bot | 19 | 0.2347 | 0.4211 | 4.4600 | 14 | 12 | 5 | 1.4411 | 0.6000 | 7.2054 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-ADD-SFP/scored | calibrated | 1h | mem_twin | none | 167 | 0.1313 | 0.3234 | 21.9326 | 102 | 97 | 65 | 0.3356 | 0.3231 | 21.8122 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-ADD-SFP/scored | calibrated | 4h | record | both | 9 | 0.1508 | 0.4444 | 1.3573 | 7 | 8 | 2 | -1.0485 | 0.0000 | -2.0970 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 4h | record | top | 8 | 0.4999 | 0.5000 | 3.9994 | 1 | 7 | 7 | 0.7053 | 0.5714 | 4.9368 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 4h | record | bot | 12 | 0.5730 | 0.2500 | 6.8764 | 5 | 11 | 7 | 0.8164 | 0.2857 | 5.7150 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 4h | record | none | 171 | 0.1437 | 0.3333 | 24.5789 | 110 | 137 | 61 | 0.5095 | 0.3443 | 31.0795 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 4h | mem_twin | both | 9 | 0.1508 | 0.4444 | 1.3573 | 7 | 8 | 2 | -1.0485 | 0.0000 | -2.0970 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 4h | mem_twin | top | 8 | 0.4999 | 0.5000 | 3.9994 | 1 | 7 | 7 | 0.7053 | 0.5714 | 4.9368 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 4h | mem_twin | bot | 13 | 0.7517 | 0.3077 | 9.7716 | 6 | 11 | 7 | 0.8164 | 0.2857 | 5.7150 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 4h | mem_twin | none | 170 | 0.1276 | 0.3294 | 21.6836 | 109 | 137 | 61 | 0.5095 | 0.3443 | 31.0795 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 12h | record | both | 6 | 0.5257 | 0.3333 | 3.1542 | 4 | 3 | 2 | -0.6436 | 0.0000 | -1.2872 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 12h | record | top | 4 | -0.8505 | 0.0000 | -3.4018 | 1 | 2 | 3 | -0.8127 | 0.0000 | -2.4380 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 12h | record | bot | 13 | 0.5133 | 0.4615 | 6.6735 | 5 | 8 | 8 | 0.8768 | 0.5000 | 7.0146 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 12h | record | none | 177 | 0.1717 | 0.3390 | 30.3861 | 113 | 110 | 64 | 0.5679 | 0.3594 | 36.3450 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 12h | mem_twin | both | 7 | 0.2941 | 0.2857 | 2.0588 | 4 | 4 | 3 | -0.7942 | 0.0000 | -2.3827 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 12h | mem_twin | top | 9 | -0.8687 | 0.0000 | -7.8185 | 3 | 6 | 6 | -0.8929 | 0.0000 | -5.3574 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 12h | mem_twin | bot | 15 | 0.4429 | 0.4667 | 6.6441 | 8 | 10 | 7 | 1.1586 | 0.5714 | 8.1101 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 12h | mem_twin | none | 169 | 0.2126 | 0.3491 | 35.9276 | 108 | 103 | 61 | 0.6437 | 0.3770 | 39.2644 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-ADD-SFP/scored | calibrated | 1d | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-ADD-SFP/scored | calibrated | 1d | record | top | 1 | 3.8512 | 1.0000 | 3.8512 | 1 | 1 | 1 | 3.8512 | 1.0000 | 3.8512 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-ADD-SFP/scored | calibrated | 1d | record | bot | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-ADD-SFP/scored | calibrated | 1d | record | none | 199 | 0.1656 | 0.3367 | 32.9608 | 199 | 74 | 76 | 0.4708 | 0.3421 | 35.7832 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-ADD-SFP/scored | calibrated | 1d | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-ADD-SFP/scored | calibrated | 1d | mem_twin | top | 1 | 3.8512 | 1.0000 | 3.8512 | 1 | 1 | 1 | 3.8512 | 1.0000 | 3.8512 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-ADD-SFP/scored | calibrated | 1d | mem_twin | bot | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-ADD-SFP/scored | calibrated | 1d | mem_twin | none | 199 | 0.1656 | 0.3367 | 32.9608 | 199 | 74 | 76 | 0.4708 | 0.3421 | 35.7832 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-ADD-SFP/scored | calibrated | 1w | record | NA | 200 | 0.1841 | 0.3400 | 36.8120 | 200 | 0 | 77 | 0.5147 | 0.3506 | 39.6344 | 1w | 1w: whole-tape (fallback) | 1w: none |
| P-ADD-SFP/scored | calibrated | 1w | mem_twin | NA | 200 | 0.1841 | 0.3400 | 36.8120 | 200 | 0 | 77 | 0.5147 | 0.3506 | 39.6344 | 1w | 1w: whole-tape (fallback) | 1w: none |
| P-ADD-SFP/scored | frozen3.0 | 1h | record | both | 1 | -0.9374 | 0.0000 | -0.9374 | 0 | 0 | 0 | — | — | — | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-ADD-SFP/scored | frozen3.0 | 1h | record | top | 9 | 0.1910 | 0.3333 | 1.7194 | 0 | 0 | 6 | 0.7184 | 0.5000 | 4.3105 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-ADD-SFP/scored | frozen3.0 | 1h | record | bot | 2 | -0.5115 | 0.5000 | -1.0231 | 0 | 0 | 1 | -1.0349 | 0.0000 | -1.0349 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-ADD-SFP/scored | frozen3.0 | 1h | record | none | 188 | 0.1971 | 0.3404 | 37.0531 | 0 | 0 | 70 | 0.5194 | 0.3429 | 36.3588 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-ADD-SFP/scored | frozen3.0 | 1h | mem_twin | both | 1 | -0.9374 | 0.0000 | -0.9374 | 0 | 0 | 0 | — | — | — | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-ADD-SFP/scored | frozen3.0 | 1h | mem_twin | top | 10 | 0.7899 | 0.4000 | 7.8988 | 0 | 0 | 7 | 1.4986 | 0.5714 | 10.4899 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-ADD-SFP/scored | frozen3.0 | 1h | mem_twin | bot | 2 | -0.5115 | 0.5000 | -1.0231 | 0 | 0 | 1 | -1.0349 | 0.0000 | -1.0349 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-ADD-SFP/scored | frozen3.0 | 1h | mem_twin | none | 187 | 0.1651 | 0.3369 | 30.8737 | 0 | 0 | 69 | 0.4374 | 0.3333 | 30.1794 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-ADD-SFP/scored | frozen3.0 | 4h | record | both | 5 | -0.5545 | 0.2000 | -2.7724 | 0 | 0 | 1 | -0.7735 | 0.0000 | -0.7735 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-ADD-SFP/scored | frozen3.0 | 4h | record | top | 3 | 1.1348 | 1.0000 | 3.4045 | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-ADD-SFP/scored | frozen3.0 | 4h | record | bot | 13 | -0.6605 | 0.1538 | -8.5868 | 0 | 0 | 10 | -0.5796 | 0.2000 | -5.7959 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-ADD-SFP/scored | frozen3.0 | 4h | record | none | 179 | 0.2501 | 0.3464 | 44.7667 | 0 | 0 | 66 | 0.7001 | 0.3788 | 46.2037 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-ADD-SFP/scored | frozen3.0 | 4h | mem_twin | both | 5 | -0.5545 | 0.2000 | -2.7724 | 0 | 0 | 1 | -0.7735 | 0.0000 | -0.7735 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-ADD-SFP/scored | frozen3.0 | 4h | mem_twin | top | 3 | 1.1348 | 1.0000 | 3.4045 | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-ADD-SFP/scored | frozen3.0 | 4h | mem_twin | bot | 13 | -0.6605 | 0.1538 | -8.5868 | 0 | 0 | 10 | -0.5796 | 0.2000 | -5.7959 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-ADD-SFP/scored | frozen3.0 | 4h | mem_twin | none | 179 | 0.2501 | 0.3464 | 44.7667 | 0 | 0 | 66 | 0.7001 | 0.3788 | 46.2037 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-ADD-SFP/scored | frozen3.0 | 12h | record | both | 5 | 1.0590 | 0.6000 | 5.2949 | 0 | 0 | 3 | 2.2436 | 1.0000 | 6.7307 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-ADD-SFP/scored | frozen3.0 | 12h | record | top | 9 | -0.2284 | 0.2222 | -2.0553 | 0 | 0 | 4 | -0.4897 | 0.2500 | -1.9588 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-ADD-SFP/scored | frozen3.0 | 12h | record | bot | 9 | 0.0990 | 0.4444 | 0.8913 | 0 | 0 | 4 | 0.8369 | 0.5000 | 3.3475 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-ADD-SFP/scored | frozen3.0 | 12h | record | none | 177 | 0.1846 | 0.3333 | 32.6811 | 0 | 0 | 66 | 0.4775 | 0.3182 | 31.5150 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-ADD-SFP/scored | frozen3.0 | 12h | mem_twin | both | 6 | 0.6999 | 0.5000 | 4.1994 | 0 | 0 | 4 | 1.4088 | 0.7500 | 5.6353 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-ADD-SFP/scored | frozen3.0 | 12h | mem_twin | top | 9 | -0.2284 | 0.2222 | -2.0553 | 0 | 0 | 4 | -0.4897 | 0.2500 | -1.9588 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-ADD-SFP/scored | frozen3.0 | 12h | mem_twin | bot | 8 | 0.2483 | 0.5000 | 1.9868 | 0 | 0 | 3 | 1.4810 | 0.6667 | 4.4430 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-ADD-SFP/scored | frozen3.0 | 12h | mem_twin | none | 177 | 0.1846 | 0.3333 | 32.6811 | 0 | 0 | 66 | 0.4775 | 0.3182 | 31.5150 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-ADD-SFP/scored | frozen3.0 | 1d | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-ADD-SFP/scored | frozen3.0 | 1d | record | top | 2 | 1.3995 | 0.5000 | 2.7991 | 0 | 0 | 2 | 1.3995 | 0.5000 | 2.7991 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-ADD-SFP/scored | frozen3.0 | 1d | record | bot | 1 | 2.0212 | 1.0000 | 2.0212 | 0 | 0 | 1 | 2.0212 | 1.0000 | 2.0212 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-ADD-SFP/scored | frozen3.0 | 1d | record | none | 197 | 0.1624 | 0.3350 | 31.9917 | 0 | 0 | 74 | 0.4705 | 0.3378 | 34.8141 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-ADD-SFP/scored | frozen3.0 | 1d | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-ADD-SFP/scored | frozen3.0 | 1d | mem_twin | top | 2 | 1.3995 | 0.5000 | 2.7991 | 0 | 0 | 2 | 1.3995 | 0.5000 | 2.7991 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-ADD-SFP/scored | frozen3.0 | 1d | mem_twin | bot | 1 | 2.0212 | 1.0000 | 2.0212 | 0 | 0 | 1 | 2.0212 | 1.0000 | 2.0212 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-ADD-SFP/scored | frozen3.0 | 1d | mem_twin | none | 197 | 0.1624 | 0.3350 | 31.9917 | 0 | 0 | 74 | 0.4705 | 0.3378 | 34.8141 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-ADD-SFP/scored | frozen3.0 | 1w | record | NA | 200 | 0.1841 | 0.3400 | 36.8120 | 0 | 0 | 77 | 0.5147 | 0.3506 | 39.6344 | 1w | 1w: frozen3.0 | 1w: none |
| P-ADD-SFP/scored | frozen3.0 | 1w | mem_twin | NA | 200 | 0.1841 | 0.3400 | 36.8120 | 0 | 0 | 77 | 0.5147 | 0.3506 | 39.6344 | 1w | 1w: frozen3.0 | 1w: none |
| P-TP-RNG/scored | calibrated | 1h | record | both | 4 | 2.4491 | 0.7500 | 9.7962 | 2 | 2 | 2 | 3.8599 | 0.5000 | 7.7198 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-TP-RNG/scored | calibrated | 1h | record | top | 9 | 0.2383 | 0.3333 | 2.1444 | 4 | 3 | 5 | 0.6740 | 0.4000 | 3.3699 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-TP-RNG/scored | calibrated | 1h | record | bot | 17 | 0.4205 | 0.5294 | 7.1480 | 12 | 11 | 5 | 0.7494 | 0.8000 | 3.7469 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-TP-RNG/scored | calibrated | 1h | record | none | 170 | 0.1043 | 0.3529 | 17.7279 | 105 | 99 | 65 | 0.3695 | 0.3692 | 24.0168 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-TP-RNG/scored | calibrated | 1h | mem_twin | both | 4 | 2.4491 | 0.7500 | 9.7962 | 2 | 2 | 2 | 3.8599 | 0.5000 | 7.7198 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-TP-RNG/scored | calibrated | 1h | mem_twin | top | 10 | 0.1096 | 0.3000 | 1.0962 | 5 | 4 | 5 | 0.6740 | 0.4000 | 3.3699 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-TP-RNG/scored | calibrated | 1h | mem_twin | bot | 19 | 0.2585 | 0.4737 | 4.9122 | 14 | 12 | 5 | 0.7494 | 0.8000 | 3.7469 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-TP-RNG/scored | calibrated | 1h | mem_twin | none | 167 | 0.1258 | 0.3593 | 21.0120 | 102 | 97 | 65 | 0.3695 | 0.3692 | 24.0168 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| P-TP-RNG/scored | calibrated | 4h | record | both | 9 | -0.0122 | 0.4444 | -0.1097 | 7 | 8 | 2 | -1.0485 | 0.0000 | -2.0970 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 4h | record | top | 8 | 0.1191 | 0.5000 | 0.9530 | 1 | 7 | 7 | 0.2701 | 0.5714 | 1.8904 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 4h | record | bot | 12 | 0.5504 | 0.5000 | 6.6046 | 5 | 11 | 7 | 0.7128 | 0.5714 | 4.9895 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 4h | record | none | 171 | 0.1717 | 0.3567 | 29.3686 | 110 | 137 | 61 | 0.5585 | 0.3770 | 34.0706 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 4h | mem_twin | both | 9 | -0.0122 | 0.4444 | -0.1097 | 7 | 8 | 2 | -1.0485 | 0.0000 | -2.0970 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 4h | mem_twin | top | 8 | 0.1191 | 0.5000 | 0.9530 | 1 | 7 | 7 | 0.2701 | 0.5714 | 1.8904 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 4h | mem_twin | bot | 13 | 0.7308 | 0.5385 | 9.4998 | 6 | 11 | 7 | 0.7128 | 0.5714 | 4.9895 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 4h | mem_twin | none | 170 | 0.1557 | 0.3529 | 26.4734 | 109 | 137 | 61 | 0.5585 | 0.3770 | 34.0706 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 12h | record | both | 6 | 0.2517 | 0.5000 | 1.5100 | 4 | 3 | 2 | -0.3712 | 0.5000 | -0.7423 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 12h | record | top | 4 | -0.8505 | 0.0000 | -3.4018 | 1 | 2 | 3 | -0.8127 | 0.0000 | -2.4380 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 12h | record | bot | 13 | 0.6123 | 0.4615 | 7.9600 | 5 | 8 | 8 | 1.0042 | 0.5000 | 8.0333 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 12h | record | none | 177 | 0.1737 | 0.3729 | 30.7483 | 113 | 110 | 64 | 0.5313 | 0.4062 | 34.0005 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 12h | mem_twin | both | 7 | 0.0592 | 0.4286 | 0.4145 | 4 | 4 | 3 | -0.6126 | 0.3333 | -1.8378 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 12h | mem_twin | top | 9 | -0.8687 | 0.0000 | -7.8185 | 3 | 6 | 6 | -0.8929 | 0.0000 | -5.3574 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 12h | mem_twin | bot | 15 | 0.5287 | 0.4667 | 7.9307 | 8 | 10 | 7 | 1.3041 | 0.5714 | 9.1288 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 12h | mem_twin | none | 169 | 0.2147 | 0.3846 | 36.2898 | 108 | 103 | 61 | 0.6052 | 0.4262 | 36.9199 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| P-TP-RNG/scored | calibrated | 1d | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-TP-RNG/scored | calibrated | 1d | record | top | 1 | 3.8512 | 1.0000 | 3.8512 | 1 | 1 | 1 | 3.8512 | 1.0000 | 3.8512 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-TP-RNG/scored | calibrated | 1d | record | bot | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-TP-RNG/scored | calibrated | 1d | record | none | 199 | 0.1657 | 0.3719 | 32.9653 | 199 | 74 | 76 | 0.4606 | 0.3947 | 35.0023 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-TP-RNG/scored | calibrated | 1d | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-TP-RNG/scored | calibrated | 1d | mem_twin | top | 1 | 3.8512 | 1.0000 | 3.8512 | 1 | 1 | 1 | 3.8512 | 1.0000 | 3.8512 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-TP-RNG/scored | calibrated | 1d | mem_twin | bot | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-TP-RNG/scored | calibrated | 1d | mem_twin | none | 199 | 0.1657 | 0.3719 | 32.9653 | 199 | 74 | 76 | 0.4606 | 0.3947 | 35.0023 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| P-TP-RNG/scored | calibrated | 1w | record | NA | 200 | 0.1841 | 0.3750 | 36.8165 | 200 | 0 | 77 | 0.5046 | 0.4026 | 38.8535 | 1w | 1w: whole-tape (fallback) | 1w: none |
| P-TP-RNG/scored | calibrated | 1w | mem_twin | NA | 200 | 0.1841 | 0.3750 | 36.8165 | 200 | 0 | 77 | 0.5046 | 0.4026 | 38.8535 | 1w | 1w: whole-tape (fallback) | 1w: none |
| P-TP-RNG/scored | frozen3.0 | 1h | record | both | 1 | -0.9374 | 0.0000 | -0.9374 | 0 | 0 | 0 | — | — | — | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-TP-RNG/scored | frozen3.0 | 1h | record | top | 9 | 0.4249 | 0.5556 | 3.8245 | 0 | 0 | 6 | 1.0021 | 0.6667 | 6.0129 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-TP-RNG/scored | frozen3.0 | 1h | record | bot | 2 | -0.1790 | 0.5000 | -0.3579 | 0 | 0 | 1 | -1.0349 | 0.0000 | -1.0349 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-TP-RNG/scored | frozen3.0 | 1h | record | none | 188 | 0.1824 | 0.3670 | 34.2872 | 0 | 0 | 70 | 0.4839 | 0.3857 | 33.8756 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-TP-RNG/scored | frozen3.0 | 1h | mem_twin | both | 1 | -0.9374 | 0.0000 | -0.9374 | 0 | 0 | 0 | — | — | — | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-TP-RNG/scored | frozen3.0 | 1h | mem_twin | top | 10 | 0.9787 | 0.6000 | 9.7872 | 0 | 0 | 7 | 1.7108 | 0.7143 | 11.9755 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-TP-RNG/scored | frozen3.0 | 1h | mem_twin | bot | 2 | -0.1790 | 0.5000 | -0.3579 | 0 | 0 | 1 | -1.0349 | 0.0000 | -1.0349 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-TP-RNG/scored | frozen3.0 | 1h | mem_twin | none | 187 | 0.1515 | 0.3636 | 28.3246 | 0 | 0 | 69 | 0.4045 | 0.3768 | 27.9129 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| P-TP-RNG/scored | frozen3.0 | 4h | record | both | 5 | -0.2370 | 0.4000 | -1.1850 | 0 | 0 | 1 | 0.1487 | 1.0000 | 0.1487 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-TP-RNG/scored | frozen3.0 | 4h | record | top | 3 | 1.2241 | 1.0000 | 3.6723 | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-TP-RNG/scored | frozen3.0 | 4h | record | bot | 13 | -0.6247 | 0.2308 | -8.1213 | 0 | 0 | 10 | -0.5330 | 0.3000 | -5.3303 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-TP-RNG/scored | frozen3.0 | 4h | record | none | 179 | 0.2372 | 0.3743 | 42.4505 | 0 | 0 | 66 | 0.6672 | 0.4091 | 44.0351 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-TP-RNG/scored | frozen3.0 | 4h | mem_twin | both | 5 | -0.2370 | 0.4000 | -1.1850 | 0 | 0 | 1 | 0.1487 | 1.0000 | 0.1487 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-TP-RNG/scored | frozen3.0 | 4h | mem_twin | top | 3 | 1.2241 | 1.0000 | 3.6723 | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-TP-RNG/scored | frozen3.0 | 4h | mem_twin | bot | 13 | -0.6247 | 0.2308 | -8.1213 | 0 | 0 | 10 | -0.5330 | 0.3000 | -5.3303 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-TP-RNG/scored | frozen3.0 | 4h | mem_twin | none | 179 | 0.2372 | 0.3743 | 42.4505 | 0 | 0 | 66 | 0.6672 | 0.4091 | 44.0351 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| P-TP-RNG/scored | frozen3.0 | 12h | record | both | 5 | 0.2707 | 0.8000 | 1.3534 | 0 | 0 | 3 | 0.7955 | 1.0000 | 2.3864 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-TP-RNG/scored | frozen3.0 | 12h | record | top | 9 | -0.2284 | 0.2222 | -2.0553 | 0 | 0 | 4 | -0.4897 | 0.2500 | -1.9588 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-TP-RNG/scored | frozen3.0 | 12h | record | bot | 9 | 0.1829 | 0.4444 | 1.6461 | 0 | 0 | 4 | 0.8369 | 0.5000 | 3.3475 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-TP-RNG/scored | frozen3.0 | 12h | record | none | 177 | 0.2027 | 0.3672 | 35.8722 | 0 | 0 | 66 | 0.5315 | 0.3788 | 35.0783 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-TP-RNG/scored | frozen3.0 | 12h | mem_twin | both | 6 | 0.0430 | 0.6667 | 0.2580 | 0 | 0 | 4 | 0.3227 | 0.7500 | 1.2910 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-TP-RNG/scored | frozen3.0 | 12h | mem_twin | top | 9 | -0.2284 | 0.2222 | -2.0553 | 0 | 0 | 4 | -0.4897 | 0.2500 | -1.9588 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-TP-RNG/scored | frozen3.0 | 12h | mem_twin | bot | 8 | 0.3427 | 0.5000 | 2.7416 | 0 | 0 | 3 | 1.4810 | 0.6667 | 4.4430 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-TP-RNG/scored | frozen3.0 | 12h | mem_twin | none | 177 | 0.2027 | 0.3672 | 35.8722 | 0 | 0 | 66 | 0.5315 | 0.3788 | 35.0783 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| P-TP-RNG/scored | frozen3.0 | 1d | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-TP-RNG/scored | frozen3.0 | 1d | record | top | 2 | 1.3995 | 0.5000 | 2.7991 | 0 | 0 | 2 | 1.3995 | 0.5000 | 2.7991 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-TP-RNG/scored | frozen3.0 | 1d | record | bot | 1 | 2.7591 | 1.0000 | 2.7591 | 0 | 0 | 1 | 2.7591 | 1.0000 | 2.7591 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-TP-RNG/scored | frozen3.0 | 1d | record | none | 197 | 0.1587 | 0.3706 | 31.2583 | 0 | 0 | 74 | 0.4499 | 0.3919 | 33.2953 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-TP-RNG/scored | frozen3.0 | 1d | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-TP-RNG/scored | frozen3.0 | 1d | mem_twin | top | 2 | 1.3995 | 0.5000 | 2.7991 | 0 | 0 | 2 | 1.3995 | 0.5000 | 2.7991 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-TP-RNG/scored | frozen3.0 | 1d | mem_twin | bot | 1 | 2.7591 | 1.0000 | 2.7591 | 0 | 0 | 1 | 2.7591 | 1.0000 | 2.7591 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-TP-RNG/scored | frozen3.0 | 1d | mem_twin | none | 197 | 0.1587 | 0.3706 | 31.2583 | 0 | 0 | 74 | 0.4499 | 0.3919 | 33.2953 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| P-TP-RNG/scored | frozen3.0 | 1w | record | NA | 200 | 0.1841 | 0.3750 | 36.8165 | 0 | 0 | 77 | 0.5046 | 0.4026 | 38.8535 | 1w | 1w: frozen3.0 | 1w: none |
| P-TP-RNG/scored | frozen3.0 | 1w | mem_twin | NA | 200 | 0.1841 | 0.3750 | 36.8165 | 0 | 0 | 77 | 0.5046 | 0.4026 | 38.8535 | 1w | 1w: frozen3.0 | 1w: none |
