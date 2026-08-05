# Naiad Knowledge Base — Canon Synthesis v1
**The operator's library (20 texts, delivered 2026-07-31) read as a lens on Secret Sauce v12**
**Author:** APOLLO (reviewer) · **Status:** original synthesis for the permanent Knowledge Base · **Filing:** project box now; `docs/knowledge/` on the next docs commit batch

*Provenance and copyright:* this document is an original analysis written for Project Naiad. It reproduces none of the source texts; the ideas are attributed, the words are ours, and the library itself remains the operator's own files. Depth disclosure: all 20 files were identity-verified (16 by extracted title text; 4 scanned editions — Elder's *Trading for a Living*, Natenberg, Murphy, Douglas's *The Disciplined Trader* — by filename and structure). The synthesis draws on the canonical content of these standard works, applied against Naiad's measured record.

---

## How to read this document

Part A maps each text (grouped in seven domains) to what Naiad has measured, is measuring, or should measure. Part B is the actionable register — every item that could change a contract carries a **[VETO]** flag for operator ruling. Part C lists what we deliberately do *not* import, because a lens is defined by its edges. Part D inventories the whole Knowledge Base as it now stands. Invocation conventions stand: "Depth: <topic>" for a one-theme pass, "Breadth: <domains>" for a sweep.

---

# PART A — The canon, mapped to Naiad

## A1 · System design & risk — Van Tharp, *Trade Your Way to Financial Freedom*

Tharp's central claims: a trading system is an expression of beliefs; the unit of account is the **R-multiple** (risk per trade), performance is the **expectancy** of the R-distribution, and **position sizing** is the lever that shapes equity outcomes around a given expectancy — it amplifies edge, it cannot create it.

**Naiad already lives inside this framework, deliberately.** R = 0.5% of cell equity; cell-R is the grid's expectancy accounting; every phase report is a Tharp-style R-distribution report card. Two confirmations and no changes: our ratified sizing-deferral ("all sizing levers negative first-order until exits have edge") is precisely Tharp's amplify-not-create doctrine, measured; and pre-registration is his "you trade your beliefs" made falsifiable — the belief is written down before the market grades it.

## A2 · The multi-timeframe method — Elder, *Trading for a Living* + *Come Into My Trading Room*

Elder's **Triple Screen** is the closest published ancestor of Secret Sauce's architecture: a slow screen sets the **tide** (trade only with the higher-TF trend), a middle screen finds the **wave** (a counter-trend pullback on the trading TF), a fast screen times the **ripple** (the entry trigger). His screens sit roughly 5× apart; our ladder runs 4–12×. Tide/wave/ripple ≍ governor / pullback-PRIME / exec trigger — a 30-year pedigree for the funnel, independently arrived at.

Three transfers. First, **validation**: the HTF→LTF principle the operator stated as an analytical law (trend tier 1D/1W/1M, build tier below) is Elder's tide, and Q4b's weekly lens extension is exactly "read the tide one screen higher." Second, a **challenge worth measuring, not adopting**: Elder times the wave with oscillator divergence; divergence lives in our brief but has never entered the engine, and D9's grave (timing-confluence) counsels suspicion — so divergence-at-the-wave goes to the census **annex** as an event-class candidate under Q3a, nothing more. Third, *Come Into My Trading Room*'s record-keeping discipline — the trading diary as the trader's real edge — is our journal/ledger ethos; his 2%-per-trade / 6%-per-month loss rules rhyme with our 0.5% R and G-8 equity floor.

## A3 · Psychology as process — Douglas ×2, Lefevre, *The New Market Wizards*

Douglas (*Trading in the Zone*, *The Disciplined Trader*): an edge is a **probability distribution over a series of trades**; the losing mind demands to be right on the next one. Naiad's answer is architectural: the census thinks in populations because it cannot do otherwise, and pre-registration removes the need for any single claim to be right — falsification is a deliverable, not a wound. Douglas's psychology is implemented here as *governance*: the machine cannot revenge-trade, and the operator's discipline concentrates where it belongs — at the gates.

Lefevre (*Reminiscences*): the book's most famous lesson — the big money was never in the thinking but in the **sitting** — is our S-3 finding wearing a straw hat: the winning structural-stop book wins by riding to regime break (opposite-cross exits, 67% winners), not by managing individual winners. His "pivotal points" are walls before walls had clustering algorithms; his sucker-play taxonomy is our stillbirth/toll-bleed population described from the inside.

*The New Market Wizards*: methods diverge wildly; risk control, loss-cutting, and process discipline converge — an independent triangulation of our macro-finding that measured edge concentrates in exit asymmetry and location rather than entry cleverness.

## A4 · Classical technical analysis — Murphy; Person; Williams; *Naked Forex*

Murphy (*Technical Analysis of the Financial Markets*) is the grammar book. Three entries matter now: **rectangles** are our ranges, and his treatment of them (edges, false breaks, volume behavior) is the folklore Q5–Q7 will test; the **measured move** — range height projected from the breakout — is a *second take-profit candidate* to measure beside the AMT opposing-wall harvest (see B4); **continuation flags** are the micro-range add family of Q9(ii), named in 1986. His volume-confirmation doctrine is asserted; §1.5 makes us test it.

Person (*Technical Trading Tactics*): pivot levels plus moving-average confirmation plus candle triggers — kin to our pivot(5,5) machinery and wall families; his confirmation-stacking is confluence counting, and D9 already taught us to count rather than believe.

Williams (*Long-Term Secrets to Short-Term Trading*): the useful core is **range expansion** — large-range days as trend births, volatility breakout as an entry logic — which is a published ancestor of our acceptance-by-expansion candidates and of the IMBALANCE-onset idea; his inside-day and smash-day patterns join the census annex as event-class candidates. His day-of-week/day-of-month seasonality does **not** transfer (Part C).

*Naked Forex*: trade only at zones, on price-action catalysts, with no indicators — philosophically identical to "areas where I want to do business." It is the strongest popular statement of location-first entry grammar, and its existence is a comfort, not a proof: the C7b stamp (location surviving ≠ outcome paying) still applies to every zone claim, theirs and ours.

## A5 · Market structure of a 24-hour decentralized market — Lien; *Currency Strategy*; *Currency Trading for Dummies*

FX is crypto's closest structural cousin: continuous, session-driven, carry-bearing. Lien's session anatomy — the **Asia range** compressing, London breaking it — is a daily-scale range→breakout cycle that our session anchors (already planned in 2a) can capture almost for free; the *Asia-session range as a measurable range object* joins the annex (B5). Her pair taxonomy (ranging pairs vs trending pairs) is the per-asset version of our regime classifier. The carry-trade logic across all three books feeds A7's funding frame. The fundamental-forecasting halves of these books stay on the shelf (Part C).

## A6 · Inference and the quant toolkit — Casella & Berger; *Quantitative Trading Strategies Using Python*; the ML-for-algo-trading compilation; McKinney

Casella & Berger is the formal backbone under practices we adopted by instinct: estimators and their variances under our bootstrap CIs, hypothesis testing under our confirm/falsify verdicts. Two upgrades it funds, both aimed at the sequence miner where they matter most: **(1) formal multiple-testing control** — mining dozens-to-hundreds of patterns makes per-comparison significance meaningless; a Benjamini–Hochberg **false-discovery-rate** layer on the confirmatory table (proposed q = 0.10) turns "top of a sorted list" into a controlled claim (B1); **(2) principled support floors** — a small power calculation converts the miner's minimum-n from an arbitrary number into "the n below which the effect we care about is undetectable."

The quant/ML texts converge independently on disciplines we already ratified: **walk-forward validation** is our held-in-time split; **leakage prevention** is our decision curtain; **probability-of-backtest-overfitting and deflated performance** metrics are the formal cousins of strip-best and the deflation gauges (available as future formalization, not required now). They also supply the implementation pattern for B2's benchmark suite: vectorized, frozen, boring. McKinney is builder tooling — the pandas idiom the whole estate already speaks.

## A7 · Derivatives — Hull; Natenberg

Hull's cost-of-carry is the frame that makes perpetuals legible: a perp replaces expiry with a continuously-paid carry leg — **funding is the carry**. That converts C-4 from "an unmeasured fee" into a priced financing leg: cost = position × time × rate path. And one concrete catch from this reading: **the journals already carry `funding_cum` on every fill row** (verified in the Block-E schema inventory) — so a first Tier-A read of realized funding per tranche may be computable from existing journals, before any new data collection (B3). Natenberg supplies the volatility vocabulary — realized-vol regimes (already in the brief), and the conceptual note that a breakout playbook is synthetically a long-gamma position, which is what an options expression would someday make explicit. Someday is doing real work in that sentence: see B9 and Part C.

---

# PART B — Applications register (actionable; [VETO] = operator ruling required)

**B1 [VETO] · Q3a Amendment A1 — FDR control for the pattern miner.** Add Benjamini–Hochberg false-discovery-rate control (q = 0.10) to the confirmatory pattern table, layered *on top of* the existing bars (five-asset replication, held-in-time split, net-of-toll floors), plus a power-based support floor. Source: A6. Cost: a few lines in the census analyzer; benefit: the miner's headline claims become formally controlled.

**B2 [VETO] · The yardstick suite.** A frozen, Tier-A, vectorized benchmark set printed beside every Tier-C result: per-asset buy-and-hold; 9/89 MA-cross long-flat; Donchian-20 breakout; a vol-targeted variant of each. These are rulers, not systems — pre-registered once, never tuned, answering "does SS clear naive momentum?" the way strip-best answers "does it clear one lucky trade?" Source: A6, A4-Williams. Direct answer to the operator's "quant strategy in parallel" question, in control-arm form.

**B3 · Funding read from existing journals (upgrades the parked funding micro-contract).** Before commissioning any new funding-data work: a Tier-A pass over `funding_cum` in the S-3/TC-1 journals — realized funding per tranche, per mandate, per holding-time bucket; reconciliation against the funding-rate files in the estate. Source: A7 + the Block-E schema. This likely settles D5's funding question years cheaper than planned.

**B4 [VETO] · Second TP candidate — the measured move.** In 2b's exit-counterfactual leg (Q10a), measure harvest at *range-height projection* beside harvest at the *opposing wall* — two published TP doctrines, head-to-head, counted, with the ⅔-fraction curve applied to both. Source: A4-Murphy vs A1-of-the-Level-doc (AMT).

**B5 · Annex — session-range object.** The Asia-session range (and its London/NY break behavior) measured as a candidate daily range family in the census annex; costs nothing beyond the session anchors already planned. Source: A5. Annex-only; no change to Q-R2's ruled families.

**B6 · Annex — event-class candidates.** Williams's range-expansion day and inside-day; Elder's wave-screen divergence. All annex-only under Q3a; none touches the rule surface without graduating.

**B7 · No action — pedigree notes.** Elder's Triple Screen validates the funnel architecture; Tharp's framework confirms our R accounting and sizing deferral; Douglas is implemented as governance; Lefevre independently states S-3's riding finding.

**B8 · Execution-fit statement (answering the operator's question directly).** The data we collect — bar-close signals on 1m/5m exec frames, klines plus funding — fits exactly one execution model: **signal at bar close, market-order emulation with modeled toll, on perpetuals**. That is what the engine does. Maker/limit-chase optimization and L2-microstructure execution require order-book data we do not collect and are deferred by the standing priority rule (edge before execution engineering). No change recommended; the fit is already correct.

**B9 · OPT-0 — options workstream, parked with prerequisites.** An options strategy is a different instrument, venue, and data estate (IV surfaces, chain liquidity — thin outside BTC/ETH), plus a pricing stack (Natenberg/Hull). Parked as a named future workstream whose prerequisites are: demonstrated perp edge; an IV data feed; a venue liquidity study. The one conceptual bridge kept warm: TRANSITION-mode conviction is synthetically long gamma, and if the breakout playbook graduates, a defined-risk options expression is the natural convex form — later.

---

# PART C — The anti-import list (what this library will not smuggle in)

Calendar seasonality (Williams's TDW/TDM) — overfit-prone, regime-fragile, and crypto's calendar is not the S&P's. Oscillator timing without location — D9 dug that grave; Elder's divergence enters only as an annex candidate. Indicator stacking — more confirmations is not more truth; counting stays, believing doesn't. FX fundamental forecasting (the core of *Currency Strategy* and half of Lien) — different market, different drivers; only the structural anatomy transfers. Options income/premium-selling strategies — wrong instrument for this phase and a risk shape (short convexity) opposite to the project's. And from the quant compilation: model-first ML (fitting learners to price and hoping) — Naiad measures named, pre-registered structures; learners may someday rank features, never author rules.

---

# PART D — The Knowledge Base, inventoried

1. **Trading Knowledge Foundation v0** (`docs/knowledge/`) — the established canon mapped against Naiad's measurements, 11 sections: AMT/Market Profile; Wyckoff; time-series momentum; volume-at-price/order-flow; classical levels; oscillators & divergence; derivatives posture (funding/basis/OI); regime & volatility structure; the anti-library; the reading list; evolution rules.
2. **Level Selection Deep Dive — Wyckoff · AMT · CCL** (`docs/knowledge/`) — springs/LPS (the §1.2/§1.4 tests now running as Block E), opposing-level harvest (the TP candidate), the CCL cross-cluster-level hypothesis with its VP-equivalence deflation gauge.
3. **Trader Philosophies Analysis** (project box) — the four X-lenses (tradermatt, Trader_XO, CrypNuevo, Stefan) mapped to measured objects; the practitioner referee for range/breakout design.
4. **This document — Canon Synthesis v1** — the operator's 20-text library as lens and register.

A closing note worth smiling at: Foundation v0's §10 is a reading list this project wrote for its own operator. Today the operator delivered the shelf — Murphy, Elder, Douglas, Tharp, the Wizards — plus the inference and derivatives backbone the list didn't dare ask for. The library and the study now cite each other.

— APOLLO, 2026-07-31
