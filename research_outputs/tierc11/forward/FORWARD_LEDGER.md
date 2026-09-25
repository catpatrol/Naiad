as_of_last_closed_4h: 2026-09-25T00:00:00Z

# TIER-C11 · THE FORWARD LEDGER — base v6 and frozen 9/12, side by side

opening 2026-09-21T16:00:00Z (entry close must be after it) · last refresh pin 2026-09-25T00:00:00Z · substrate tc11_20260925 · chain head `0db889425ef8e3d2075a2a3cf2d1b500c3b0bbc7f7b4d535ffa3dec3575261cb` · 2 line(s)

**Standing and UNSCORED until each book's own n >= 30.** No CI, no p, no verdict. A campaign is appended exactly once, when it closes; an OPEN campaign is listed, never appended or counted; a continuation (entered at or before the opening) is listed, never counted.

- L-T.6: opens 2026-09-21T16:00:00Z; admits only campaigns whose entry close is > the opening; appends a campaign exactly once, when closed (exit_reason != corridor_end); OPEN campaigns are listed, never appended or counted; a refresh re-rides both frozen books over the whole tape to its pin on the F-CTRL code path and HALTs if any appended row changes; n per book; UNSCORED until n >= 30 per book.
- Every v6 row stamps the P-AGE-1 trailing band (B4 OLD refused) and the P-WIN-1 lag (>= 16 refused; 7-15 shadow).
- Chain: line_sha256 = sha256(canonical JSON of the line without line_sha256); prev = the previous line's line_sha256 (genesis: 64 zeros); canonical = sort_keys, separators (',', ':'), ensure_ascii False, allow_nan False.

## Both books, side by side

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

## Appended campaigns (whole)

| seq | book | asset | dir | entry (bar open) | exit (bar open) | exit_reason | net R | haircut R | era | P-AGE-1 band | refuses | P-WIN-1 lag | refuses | shadow 7-15 | appended at |
|---:|---|---|---:|---|---|---|---:|---:|---|---|---|---:|---|---|---|
| — | (none yet) | | | | | | | | | | | | | | |

## Refreshes

| seq | pin | snapshot | v6 appended now | 9/12 appended now | v6 n | 9/12 n | line sha |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | 2026-09-25T00:00:00Z | tc11_20260925 | 0 | 0 | 0 | 0 | 0db889425ef8e3d2… |

LIMIT (finding, not fixed): the foundation is pinned to the TC11 snapshot and pin; a refresh on bars after 2026-09-25T00:00Z needs the foundation re-rooted on a new snapshot + pin record (operator / foundation work).
