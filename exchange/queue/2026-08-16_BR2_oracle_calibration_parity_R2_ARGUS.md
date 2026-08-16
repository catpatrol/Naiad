# QUEUE BR-2 — ORACLE: RECALIBRATION · PARITY VERDICT · R2 SECOND EYE
Drafted ARGUS 2026-08-16. Executor HEPHAESTUS. Reviewer ARGUS.
RATIFIED: operator, 2026-08-16 — pre-authorized per BR-1 Amendment A1-3
BUILT: PENDING
GATES (all HARD, checked before any work):
G-BR2-1 NOT-BEFORE: >=7 dated oracle_*.html files exist in briefs/oracle/.
G-BR2-2 SELF-CHECKS: selfcheck_log.jsonl shows PASS on >=5 of the last 7 days;
        print the log verbatim.
G-BR2-3 HUMAN PARITY: a line "PARITY: OK <date>" or "PARITY: mismatches: ..." exists in
        exchange/status/LEDGER_ARGUS.md dated within the live week (the operator's one
        mid-week chart glance, relayed through the ARGUS lane). Mismatches => R2 HALTS,
        recalibration still runs, mismatch autopsy becomes the deliverable.
WORK: (1) RECALIBRATION REPORT from calibration/*.json — every v1 threshold (collapse
0.02 · cluster 0.15 · LIS 1.5 ATR · family cap 3 · maturity floors 16/60 · target
buckets) against a week of measured distributions; proposed constants as a [VETO] table;
NOTHING self-adopts. (2) PARITY VERDICT assembled from G-BR2-2 + G-BR2-3. (3) R2 BUILD,
only if parity green: self-hunting HTML — websocket kline feed, in-page station semantics
read from station_canon.json (never re-implemented), R1 blocks regenerated live, same
provenance footer, DISPLAY-ONLY, no journal, no outcome aggregation, runs in the
operator's browser only. (4) CHAIN-CLOSE STATUS REPORT to exchange/reports/
ORACLE_CHAIN_CLOSE_<date>.md + ledger append + BUILT stamps on BR-1 and BR-2.
FIXTURES: F-R2-1 canon identity (JS reads the same station_canon.json sha as Python) ·
F-R2-2 no-network-writes (page sends nothing, only receives) · F-R2-3 firewall scan ·
F-R2-4 R1 format. Each shown failing first.
NOT THIS CONTRACT: no R3 daemon · no census scoring · no threshold self-adoption ·
no Pine changes · no sizing.
