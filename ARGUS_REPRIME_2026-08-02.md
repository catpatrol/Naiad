# ARGUS — RE-PRIME ACKNOWLEDGMENT & CONSOLIDATED STATE · 2026-08-02
**From:** ARGUS (analytics toolkit · daily brief · volume filter) · **To:** the operator, HERMES (consolidation), ATHENA (workflow interview input), APOLLO (reviewer of record)
**One artifact, four audiences — per the two-port pipeline: one consolidated stream out.**

## 1 · Re-prime confirmed, gap stated honestly
`PRIMER_ARGUS_2026-08-01_v1_1.md` ingested (7,718 B, sha `6e446223…`). The primer's premise is accepted as accurate: **no ARGUS work progressed between 2026-07-29 and this re-prime.** The scoping interview (D-AR-1..15) was issued 2026-07-29 and never answered; the F-AN-8 amendment was drafted and held per standing orders and was never fired; `analytics/` v1.0.0 presumably still sits on disk uncommitted and unadopted. Nothing was lost — the halt discipline held — but nothing moved. The revised interview below is the unblocking artifact.

## 2 · Box verification (first-message checklist)
| item | state |
|---|---|
| `Rvwap_pine_code.txt` | PRESENT, 9,887 B, sha `702aa02a…` — matches the pinned reference |
| `CONTRACT_ARGUS_Analytics_Scoping_2026-07-29.md` | PRESENT, 9,700 B |
| `PRIMER_ARGUS_2026-08-01_v1_1.md` / `PRIMER_HERMES_…` | PRESENT |
| `Naiad_Knowledge_Canon_Synthesis_v1.md` | **MISSING from the box** |
| `Naiad_KB_Addendum_FourTraders_x_Canon_v1.md` | **MISSING from the box** |

The two KB syntheses the primer instructs me to verify are not in the project box. **Not blocking** — the primer's §"Early conclusions" summary is sufficient for the interview — but folding canon specifics deeper than that summary (Casella & Berger floors, Coulling casebook detail) requires the files. Requested drop when convenient.

## 3 · Erratum, on the record (ARGUS)
My 2026-07-29 interview (D-AR-9) recommended a kline-approximated CVD "from the taker-buy fields Binance klines carry." The primer corrects the machinery fact: **the estate persists a single volume column** (`data.py` KLINE_COLS) — taker-buy/delta fields are not stored, so CVD is not computable from the current estate. Same error class as the ten logged in `STATUS_HANDOFF_BRIEF_2026-07-28.md` §2.6: an inference about machinery stated above its evidence. D-AR-9 is revised accordingly (RVOL stays cheap and real; delta/VSA work parks behind an estate-column addition at a future refresh — an ATHENA-side decision).

## 4 · Decision register — revised state (full four-part context in-chat, ARGUS-SCOPE-1 v2)
| # | decision | default |
|---|---|---|
| **W-2** | analytics/brief/volume-filter proceed through the pause as infrastructure | **yes** (primer default; operator confirms) |
| D-AR-1 | one report: volume filter folds into BRIEF-2 | (a) fold |
| D-AR-2 | unify windows {prior-day, 7, 30, 90, 365} across VP+RVWAP; `profile_windowed` family | (a) yes |
| D-AR-3 | D-B12 reconciliation: trailing mechanical windows ≠ parked judgment-composites | (a) confirm |
| D-AR-4 | un-park LVN detection on windowed profiles; TPO SPs + composites stay parked | (a) yes |
| D-AR-5 | "anchored 7/30/90/365D" = trailing windows, recomputed each capture | (a) confirm |
| D-AR-6 | VP bundle: 120 rows · VA 70% · substrate 1m/5m/15m tiered · printed + chipped | bundle |
| D-AR-7 | chart planes 4H←{7,30} 1D←{30,90} 1W←{90,365} 1M←{365}; forming candle drawn greyed, all computed values closed-bar | (a) |
| D-AR-8 | oscillators + divergences extend to 1W; 1M plane = price/volume structure only | (a) |
| D-AR-9 **REVISED** | volume-side additions | **(b) RVOL only**; (c) additionally commission estate columns at next refresh to enable delta/VSA later |
| D-AR-10 | dual scoring per capture: areas + lines with and without volume families; toggle switches views; both recorded | yes |
| D-AR-11 | full report at three scheduled slots + on-command; Atlas style stands | (a) — say (b) for on-command-only |
| D-AR-12 | rules_version → 2.0.0 (closed-bar era + volume filter); 8c diff is the bridge | yes |
| D-AR-13 | adoption bundle: fire F-AN-8 amendment on ratification · parity readings parallel to Phase II · VP excluded from the hard parity gate | bundle |
| D-AR-14 | `INTERFACE.md`: census-facing contract (signatures, conventions, causality classes, level/VA schema); census consumes functions + its own data, never live captures | yes |
| D-AR-15 | build shape: paper-amend v4 (Amendment 2 = this interview) → ONE Phase II–III build | (a) |
| **D-AR-16 NEW** | draw XO's {12,25} weekly/daily EMA pair on the 1D/1W planes as a toggleable display-only lattice beside the volume layer (scanner Pine in box; census will measure {9,89,200}×{12,25} anyway) | yes |
| **D-AR-17 NEW** | record the volume-vs-spread (VPA/effort-vs-result) door as a NAMED PARKED item with its estate-column dependency, routed to ATHENA's refresh queue — noted, not built | yes |

Answer format: one line — "W-2 yes, all defaults" plus exceptions by number.

## 5 · Workflow requirements — ARGUS input to ATHENA's exchange/ interview (requirements, not design; ATHENA ratifies)
**ARGUS emits:** contracts/amendments (`ARGUS_CONTRACT_*.md`) · decision interviews (chat-native; register mirrored in artifacts like this one) · reviewer acceptance reports (`ARGUS_ACCEPT_*.md`) · re-prime/status artifacts (`STATUS_ARGUS_*.md`) · large HTML review renders (drops, not inline) · the parity worksheet (round-trips operator ↔ builder ↔ ARGUS).
**ARGUS consumes:** Builder's Reports (one per outcome, md + machine-readable json) · `MANIFEST.json` · primers/KB syntheses · operator TradingView readings.
**Requirements for exchange/:** (1) predictable lane-prefixed filenames, dated, append-only — never overwritten in place; (2) one Builder's Report per outcome into `exchange/reports/`, with the bright-colors filename rule intact; (3) `exchange/status/` as the input HERMES consolidates — ARGUS will mirror every STATUS block there once the directory exists; (4) large/binary artifacts (HTML renders, zips) stay in repo or box with a pointer file in exchange, so the stream stays readable; (5) captures/panel remain repo-side (`briefs/`) — exchange is a message bus, not a data store. Until exchange/ is ratified, ARGUS continues file-drop + box routing unchanged.

## 6 · Standing state (unchanged, for HERMES's dashboard)
`analytics/` v1.0.0 on disk, uncommitted, unadopted · F-AN-1..7, 9..14 PASS · F-AN-8 FAIL correct (unclosed 4h/12h/1d bar in v1.1) · ruling ratified: drop the bar; 8a/8b/8c amendment ready to fire as ARGUS's first paste after interview ratification · adoption = fixtures green + ~28-reading parity, no partial adoption · downstream waiting: CENSUS-2b, CENSUS-1d, H-RVX · firewall on every feature fact: [display-only] vs [evidence].

— ARGUS, 2026-08-02
