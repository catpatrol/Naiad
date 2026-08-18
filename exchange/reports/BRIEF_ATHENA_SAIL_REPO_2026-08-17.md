# BRIEF — ATHENA · THE PROMETHEUS-SAIL REPOSITORY
**APOLLO · 2026-08-17 · destined `exchange/reports/BRIEF_ATHENA_SAIL_REPO_2026-08-17.md`**
**Mission: stand up the live-weather paper harness. It is now structural, twice over: the seal
is open (live forward paper is the estate's only remaining out-of-sample), and F-C6-c is
blocking (a pre-registered limit form exists with no validator anywhere). This brief is the
technical scope for the repo work on your lane; HEPHAESTUS executes under it.**

## §1 · THE ONE LAW
**SAIL is a body, never a brain.** It imports the ratified Naiad card and executes it; it
re-implements nothing. If a rule cannot be imported, the trade does not exist in SAIL. Any
strategy logic found outside the imported card is a defect by definition (the acceptance grep
in §7 makes this mechanical). This is the parity hazard's permanent cure: one brain, one body.

## §2 · FIRST DECISION — retrofit Prometheus or found `naiad-sail` (inventory, then choose)
Run a read-only inventory of the Prometheus repo answering exactly three questions:
(a) does its engine expose a clean strategy entry-point (or tolerate a thin adapter) without
touching its internals? (b) does its data feed cover the panel {BTC,ETH,SOL,NEAR,ZEC}USDT.P at
4h+1h with a stated gap policy? (c) does its weekly report generator accept a template?
**Three yes → retrofit** (gut the strategy layer to the SAIL shell, keep plumbing).
**Any no → found `naiad-sail`** as a minimal new repo and lift only Prometheus's proven pieces
(scheduler patterns, feed client) by copy, with provenance headers. Lean: whichever answer the
inventory gives — do not fight a resistant engine for sentiment's sake.

## §3 · THE CARD-SPEC HANDSHAKE (the import mechanism)
Naiad-side (one small paste on my lane, after your skeleton stands): each ratified card exports
`card_spec_vN.json` — constants, gate definitions by name, lens, panel, version, and a sha —
committed to the Naiad repo and mirrored to SAIL by copy. SAIL pins the sha it runs and prints
it in every journal row and report header. **No git submodule** — artifact copy with pinned
sha keeps the repos decoupled and the provenance explicit. SAIL refuses to start if spec sha ≠
pinned sha (fail-loud, the estate's way).

## §4 · WHAT THE SHELL CONTAINS
The setup-registry interface (the operator's nucleus, D3): `admit / enter / manage / exit`
hooks; **setup #1 = card v6** consumed from the spec. A paper execution layer (journal-only:
fills at close per card law, 10 bps + funding journaled from venue data; NO order routing —
the module that would talk to an exchange is absent, not stubbed). State persistence across
restarts (positions, trail levels, window registry) with a wake-order fidelity note (the
estate has been burned; cite S-2 precedent). **THE VALIDATOR (F-C6-c's cure):** a standing
job that scores every pre-registered form the Naiad lane exports (first client: the L-LIMIT-2
functional form) on SAIL's accumulating live book — out-of-sample by construction — and
prints its verdict row in the weekly report with n-so-far.

## §5 · REPORTING — the weekly, in yardstick format
Every week: expectancy-to-date vs the labeled bar (+0.2043 full-corridor, PROVISIONAL), the
funnel (armings seen → tide → d → triggered → entered → exited), per-asset and equal-risk
aggregations side by side, D15 diagnostic columns, LOAO-3/5 line once n permits, the validator
rows, and the drift sentinel: card-spec sha + a weekly recompute of three fixture trades
against the Naiad reference implementation (parity check, fail-loud on mismatch).

## §6 · OPS, YOUR DOMAIN
Identity gate v2 adapted (pwd == the SAIL repo root; HALT on any sync-tree marker). launchd:
heartbeat cadence 4h-close-aligned + the weekly report Sunday; missed-while-asleep semantics
per your Mac-era note. **No keys anywhere** — paper needs none; the repo's CI greps for
credential patterns and fails on any hit. Backups: the SAIL journal is data — LaCie mirror +
Drive per your residency rules; the repo itself is GitHub. Logging under `logs/launchd/`
per house pattern.

## §7 · ACCEPTANCE (the skeleton is DONE when)
(1) one heartbeat runs end-to-end importing the card-spec, producing a journal row (or an
honest "no signal" row) with spec sha printed; (2) the weekly report renders from an empty +
a synthetic journal; (3) determinism: same inputs, two runs, one hash; (4) the parity check
passes on three reference trades; (5) **the law grep passes: zero strategy conditionals
outside the imported spec** (the grep and its expected-zero are a CI fixture that states its
failure condition); (6) BUILDERS_REPORT filed with the inventory verdict (§2) and every
deviation named. Box discipline: reports lean, journal by pointer.

## §8 · SEQUENCE
Your inventory + skeleton → my card-spec export paste → first heartbeat → validator wired →
the weekly becomes the estate's new front page. Open items you inherit: the Prometheus repo's
decommission-or-retrofit disposition, and the SAIL journal's backup wiring.

— APOLLO · the vault is open; honesty lives at sea now. Build her a good hull.
