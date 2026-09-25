"""TIER-C11 · THE NINE REGISTRATIONS — texts of record cut from the contract, operative specs beside.

The TEXT of each registration is the contract's own lines, sliced by line number from
exchange/queue/2026-09-24_TC11_APOLLO.md and checked against the STEP Q sha, so that no text can be
re-typed. The OPERATIVE SPEC beside each text is the executor's reading (research_outputs/tierc11/LEANS.md).
It names the panel, era, ruler, base, scored arm, Tier-E arms, verdict rule and any precondition or
condition. Both are hashed and filed BEFORE any TC11 book is computed.

    ~/venvs/naiad/bin/python scripts/tierc11_registrations.py            # dry run: print, write nothing
    ~/venvs/naiad/bin/python scripts/tierc11_registrations.py --file     # write-once filing

HALTS IF: the contract's sha is not the STEP Q sha, the LEANS sha differs from the one passed with --leans-sha,
a slice does not begin with its registration id, or a filing already exists (write-once).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "exchange" / "queue" / "2026-09-24_TC11_APOLLO.md"
CONTRACT_SHA = "bb38e016a8f3e55ca3bcc09fec53ba6b8dc40accb60d054f8163d033a898f835"
LEANS = ROOT / "research_outputs" / "tierc11" / "LEANS.md"
OUT = ROOT / "research_outputs" / "tierc11" / "registrations"
FAMILY_M = 9
FAMILY_Q = 0.10
BAR = FAMILY_Q / FAMILY_M
SEED = 20260924

VERDICT_RULE = ("verdict_of_record = SUPPORTED iff (a) the cluster-90% CI lower bound > 0 AND (b) one-sided "
                "p <= 0.10/9 = 0.011111 (asset-cluster bootstrap by scripts/tierc11_score.py, T5 primitives, "
                "N_BOOT 4000, seed 20260924; sensitivity seed 20260816 beside); else NOT SUPPORTED. LOAO printed "
                "beside, deciding nothing. m = 9 in every case; a registration closed by its own precondition or "
                "condition prints its reason, spends no test and never loosens the bar. A registration carrying "
                "pre_seen or selection_hazard prints '<verdict> — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY "
                "(<hazard>)'. A paired row HALTs (no verdict) unless the key sets are identical. Tier-E arms carry "
                "no verdict word. [LEANS L-1.4, L-1.5]")

SCALE_IN_SAMPLE = ("SCALE-IN-SAMPLE: calibrated-scale range reads at instants <= the era cut are structurally "
                   "in-sample (tuning-era calibration); the holdout-slice statistic and the frozen-3.0 twin are "
                   "printed beside the verdict; pick stability printed [L-R.2]")
VETOES = (101, 103)

# (reg_id, prior_pct, text line range [lo, hi] 1-based inclusive, context line ranges, operative spec)
REGS = [
    ("P-WARN-1", 40, (40, 42), [(33, 39)], {
        "kind": "CONDITIONAL exit rule", "panel": "CLASSIC5", "era": "full corridor",
        "ruler": "paired (set kept; HALT unless key sets identical)",
        "base": "card-v6 (the same campaigns, v6 exits)",
        "condition": ("cohort = v6 campaigns with an IN-TRADE counter EMA12/EMA89 1h cross (1h close > entry "
                      "close, strictly before the 1h-resolved exit, not on the stop child) before the +1R latch "
                      "(L-W.3); delta = mean(cohort) - mean(whole v6 book) by T5.cluster_boot_diff seed 20260924; "
                      "MET iff the cluster-90% hi < 0 (L-W.4). NOT MET -> report-only, no slot spent, stated; the "
                      "rule book is then printed only as a collared Tier-E row."),
        "scored_arm": ("v6 campaigns walked on 1h children (L-W.0 walk law); on each child STOP -> +1R latch -> at "
                       "the close, if pre-+1R and a counter EMA12/EMA89 cross closed, exit at that 1h close; v6 "
                       "BELL/HARVEST/TRAIL at 4h closes unchanged; identity law on untouched campaigns [L-W.5]"),
        "tier_e_arms": ["tuning slice", "holdout slice", "complement comparison",
                        "forward leg E[final - marked at event]"],
        "leans": ["L-W.0", "L-W.1", "L-W.2", "L-W.3", "L-W.4", "L-W.5", "L-1.5"]}),
    ("P-AGE-1", 50, (45, 46), [(44, 44)], {
        "kind": "admission gate (post-filter)", "panel": "CLASSIC5", "era": "full corridor",
        "ruler": "two-sample", "base": "card-v6",
        "scored_arm": ("v6 book minus the campaigns whose ENTRY-bar tide streak (tierc7_lab_regime.tide_streak) "
                       "is >= the trailing 75th-percentile edge (B4 OLD; tierc9._trailing_edges over CLASSIC5 "
                       "4h bars with open <= the entry bar, >= 30 bars) [L-G.1]"),
        "tier_e_arms": ["SHADOW absolute: refuse streak > 206 bars (the whole-corridor median edge, not the OLD "
                        "edge; reads the corridor ahead)", "tuning slice", "holdout slice",
                        "disclosure: tierc9.tide_streak_age (arm bar, 3-state tide)",
                        "re-ride rival count (freed slots)", "refused cohort n / mean / sum R"],
        "pre_seen": ("the scored cohort IS TC10 P_AGE_1_TIDE_YOUTH B4 (same function, same trailing edges, same "
                     "200 campaigns, anchored by F-CTRL(b)); point known before filing: gated n 141, +0.4567 vs "
                     "+0.2087, delta ~ +0.2480 R; new information = the interval and campaigns entered after "
                     "2026-09-21T16:00Z (listed by count)"),
        "leans": ["L-G.1", "L-1.4", "L-1.5"]}),
    ("P-WIN-1", 50, (47, 48), [(44, 44)], {
        "kind": "admission gate (post-filter)", "panel": "CLASSIC5", "era": "full corridor",
        "ruler": "two-sample", "base": "card-v6",
        "scored_arm": "v6 book minus campaigns with entry_i - arm_i >= 16 (4h bars) [L-G.2]",
        "tier_e_arms": ["SHADOW cut: refuse lag 7..15", "tuning slice", "holdout slice",
                        "refused cohort n / mean / sum R",
                        "Tier-E r_over_atr > 2.2 admission + within-window priority book; 2x2x2 gates crossed "
                        "[L-G.3]"],
        "selection_hazard": ("direction informed by TC6V L-LAG deciles on the same corridor (lag-0 +0.4149, "
                             "56-bar decile -0.5796); P-LAG-1 on the same question NOT MET (delta +0.0616 "
                             "[-0.7819, +0.9566]); the 16 cut has no on-disk provenance; v6 lag 7-15 holds "
                             "4/200, so >=16 ~ >=7"),
        "leans": ["L-G.2", "L-G.3", "L-1.4", "L-1.5"]}),
    ("P-BRK-4H", 45, (52, 54), [(13, 15), (24, 25), (51, 51)], {
        "kind": "lane", "panel": "CLASSIC5", "era": "full corridor", "ruler": "vs zero", "base": None,
        "scored_arm": ("4h macro death (calibrated 4h scale, tuning-era pick) -> the FIRST retest that HOLDS on "
                       "tap-89 (EMA-89 of 4h close; census RETEST_PINS margin 1.0 ATR, hold 3 bars, ttl 400; "
                       "touches scanned in order within the candidacy window) -> entry at the touch+hold close; "
                       "stop BK.brk_stop beyond the retest extreme, offset 0.5 ATR(4h), railed R >= 1.0 ATR(4h); "
                       "tide aligned at the entry bar's close; v6 management (BK.ride_leg_l, ribbon=None, no "
                       "12/25 bell); one position per asset [L-T.1]"),
        "tier_e_arms": ["17-asset view (LOAO bar 9/17)", "memory-line first-that-holds lane (engine one-shot "
                        "flip as its twin)", "frozen-3.0 twin", "one-shot first-touch twin", "tuning slice",
                        "holdout slice"],
        "selection_hazard": ("the best of 7,920 TC10 census cells (4h retest-hold-tap89, CLASSIC5 NET H20 +0.681 "
                             "ALL n 236 / +0.706 holdout n 88; UNSEEN12 +0.064 / +0.272); every era and asset "
                             "was seen; the scored event (first-HOLD scan, tuning-calibrated scale) differs from "
                             "the one-shot frozen-3.0 row that was selected"),
        "scale_in_sample": SCALE_IN_SAMPLE,
        "leans": ["L-T.1", "L-R.2", "L-R.6", "L-1.4"]}),
    ("P-RELAY-1", 45, (55, 57), [(51, 51), VETOES], {
        "kind": "trigger lane", "panel": "CLASSIC5", "era": "full corridor", "ruler": "two-sample",
        "base": "card-v6 (the 12/26-triggered base)",
        "scored_arm": ("ARMED per the posture word: entry at the first 1h close strictly after the v6 arm close "
                       "and strictly before min(that window's v6 4h 12/26 trigger close, the window-close "
                       "instant, a 4h 89/316-against close) on which EMA9 crosses EMA12 in the trade direction; "
                       "windows whose 4h trigger closes first are MISSES; stop struct_stop_4h with pivots and "
                       "ATR(4h) as of the last CLOSED 4h bar, railed 1.0 ATR(4h); R on 4h; the entry 4h bar's "
                       "post-entry 1h children walked for STOP/+1R, then that bar's close runs v6's BELL/HARVEST/"
                       "TRAIL slot with latches carried, then the v6 ride; one relay per window, one position per "
                       "asset [L-T.2]"),
        "tier_e_arms": ["miss column (windows never relayed; what v6 did in them)",
                        "lead distribution vs the 4h trigger", "late-relay twin (relays allowed after the "
                        "trigger)", "tuning slice", "holdout slice"],
        "leans": ["L-T.2", "L-T.3", "L-W.0"]}),
    ("P-SCALP-2", 30, (71, 71), [(16, 18), (61, 70), VETOES], {
        "kind": "lane (range trade)", "panel": "CLASSIC5", "era": "holdout", "ruler": "vs zero", "base": None,
        "precondition": ("R2 lens verdict of record at 1h (CLASSIC5 pooled, holdout, calibrated, taker) == PASS; "
                         "otherwise CLOSED BY R2, not scored, no slot spent [L-S.1]"),
        "scored_arm": ("live CONFIRMED 1h range (calibrated 1h scale) whose last closed 1h bar closed inside the "
                       "as-of box; 5m close in its lower (upper) third; 5m EMA12/EMA89 cross up (down) -> entry "
                       "at the 5m close; target far boundary -/+ 0.25 ATR_1h (frozen at entry; entry refused if "
                       "the target is not beyond entry by > 10 bps); stop beyond the 5m (5,5) pivot, offset 0.5 "
                       "ATR_5m, railed 1.0 ATR_5m; invalidation exit at the first 1h close beyond the entry-side "
                       "boundary; within a 5m bar STOP -> TARGET -> invalidation; no trail; no tide; taker toll "
                       "[L-S.2]"),
        "tier_e_arms": ["maker twin, fill assumed (2.0 bps entry/target)", "maker twin, fill conditioned",
                        "17-asset view", "regime gate: 5m ATR tercile x 1h boundary-age tercile (trailing)",
                        "tuning slice", "frozen-3.0 twin"],
        "leans": ["L-S.1", "L-S.2", "L-1.2", "L-R.4"]}),
    ("P-ADD-BRK", 40, (75, 76), [(73, 74), (79, 79), VETOES], {
        "kind": "add rule", "panel": "CLASSIC5", "era": "full corridor",
        "ruler": "paired (set kept; HALT unless key sets identical)", "base": "card-v6",
        "scored_arm": ("v6 campaigns plus <= 2 adds of 0.5 unit at the 1h close of a 1h macro range death "
                       "(calibrated 1h scale) whose breakout side is the trade's direction; the event IN-TRADE and "
                       "after the +1R latch (1h path); booked by tierc7._account_chain (Add.i = the 4h bar "
                       "containing the 1h close; exit at the campaign's exit price; the funding ceiling once on "
                       "the total) [L-A.1, L-A.2]"),
        "tier_e_arms": ["head-to-head vs P-ADD-SFP", "frozen-3.0 twin", "below-entry adds refused twin",
                        "post-harvest adds refused twin", "tuning slice", "holdout slice"],
        "scale_in_sample": SCALE_IN_SAMPLE,
        "leans": ["L-A.1", "L-A.2", "L-W.0", "L-W.3", "L-1.5"]}),
    ("P-ADD-SFP", 40, (77, 78), [(73, 74), (79, 79), VETOES], {
        "kind": "add rule", "panel": "CLASSIC5", "era": "full corridor",
        "ruler": "paired (set kept; HALT unless key sets identical)", "base": "card-v6",
        "scored_arm": ("v6 campaigns plus <= 2 adds of 0.5 unit at the 1h close of a confirmed swing-failure in "
                       "the trade's favour on a CONFIRMED 1h range (calibrated 1h scale): spring (bottom harden) "
                       "for a long, upthrust (top harden) for a short; IN-TRADE and after the +1R latch; booked "
                       "by tierc7._account_chain as P-ADD-BRK [L-A.1, L-A.3]"),
        "tier_e_arms": ["head-to-head vs P-ADD-BRK", "frozen-3.0 twin", "below-entry adds refused twin",
                        "post-harvest adds refused twin", "tuning slice", "holdout slice"],
        "scale_in_sample": SCALE_IN_SAMPLE,
        "leans": ["L-A.1", "L-A.3", "L-W.0", "L-W.3", "L-1.5"]}),
    ("P-TP-RNG", 35, (83, 86), [(81, 82), VETOES], {
        "kind": "exit rule", "panel": "CLASSIC5", "era": "full corridor",
        "ruler": "paired (set kept; HALT unless key sets identical)", "base": "card-v6",
        "scored_arm": ("v6 campaigns; at each 4h bar, with the 12h as-of state at the bar's OPEN IN_RANGE, a "
                       "resting limit for the remainder (the position still open: 1.0, or 0.5 after the v6 "
                       "harvest) at the 12h far boundary -/+ 0.25 ATR_12h, live only when the prior 4h close is "
                       "on the near side AND the level is beyond entry in the trade's favour by > 10 bps; fill at "
                       "max(level, open) for a long, min(level, open) for a short; EXPANSION/NONE -> no TP; "
                       "order STOP -> TP -> BELL -> HARVEST -> TRAIL; v6 harvest kept [L-H.1]"),
        "tier_e_arms": ["D15 tail ratio on the row", "tp-post-harvest twin (TP only after the harvest, 0.5 "
                        "runner)", "unguarded twin (no entry-side guard) + withheld-order counts",
                        "frozen-3.0 twin", "tuning slice", "holdout slice"],
        "named_risk": "the wall-exit lesson: P-WALL-1 (TC6) delta -0.0331, tail ratio 0.9329 — loses by "
                      "cutting the tail",
        "scale_in_sample": SCALE_IN_SAMPLE,
        "leans": ["L-H.1", "L-R.2", "L-1.5"]}),
]


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def build(leans_sha: str | None) -> dict:
    raw = CONTRACT.read_bytes()
    got = sha256_bytes(raw)
    if got != CONTRACT_SHA:
        raise SystemExit(f"HALT: contract sha {got} is not the STEP Q sha {CONTRACT_SHA}")
    lines = raw.decode("utf-8").split("\n")
    lsha = sha256_bytes(LEANS.read_bytes())
    if leans_sha is not None and lsha != leans_sha:
        raise SystemExit(f"HALT: LEANS.md sha {lsha} != --leans-sha {leans_sha}")

    def cut(lo: int, hi: int) -> str:
        return "\n".join(lines[lo - 1:hi])

    regs = []
    for seq, (rid, prior, (lo, hi), ctx, spec) in enumerate(REGS, 1):
        text = cut(lo, hi)
        if not text.lstrip().startswith(rid):
            raise SystemExit(f"HALT: slice {lo}-{hi} does not begin with {rid}: {text[:40]!r}")
        if f"[{prior}%" not in text:
            raise SystemExit(f"HALT: {rid} prior {prior}% is not the contract's")
        body = {
            "registration": rid, "seq": seq, "prior_pct": prior, "family_m": FAMILY_M,
            "family_bar": round(BAR, 6), "seed": SEED,
            "text_of_record": text, "text_lines": [lo, hi],
            "context_of_record": [{"lines": [a, b], "text": cut(a, b)} for a, b in ctx],
            "operative_spec": spec, "verdict_rule": VERDICT_RULE,
        }
        payload = json.dumps(body, sort_keys=True, ensure_ascii=False).encode()
        body["text_sha256"] = sha256_bytes(text.encode())
        body["sha256"] = sha256_bytes(payload)
        regs.append(body)
    prev = "0" * 64
    chain = []
    for r in regs:
        line = {"seq": r["seq"], "registration": r["registration"], "sha256": r["sha256"], "prev": prev}
        line["line_sha256"] = sha256_bytes(json.dumps(line, sort_keys=True).encode())
        prev = line["line_sha256"]
        chain.append(line)
    return {"tier": "TIER-C11", "contract": {"path": str(CONTRACT.relative_to(ROOT)), "sha256": got},
            "leans": {"path": str(LEANS.relative_to(ROOT)), "sha256": lsha},
            "family_m": FAMILY_M, "family_q": FAMILY_Q, "family_bar": round(BAR, 6), "seed": SEED,
            "registrations": regs, "chain": chain, "head": prev,
            "law": ("texts are the contract's own lines (frozen at STEP Q); operative specs are the executor's "
                    "readings, filed before any TC11 book was computed; payload sha = sha256(json.dumps(body "
                    "without shas, sort_keys, ensure_ascii=False)); chain line_sha256 over {seq, registration, "
                    "sha256, prev}")}


def main(argv: list[str]) -> int:
    leans_sha = None
    if "--leans-sha" in argv:
        leans_sha = argv[argv.index("--leans-sha") + 1]
    doc = build(leans_sha)
    for r in doc["registrations"]:
        print(f"{r['seq']} {r['registration']:<10} [{r['prior_pct']}%] lines {r['text_lines']} "
              f"text {r['text_sha256'][:16]} payload {r['sha256'][:16]}")
    print(f"contract {doc['contract']['sha256'][:16]} · LEANS {doc['leans']['sha256'][:16]} · head {doc['head']}")
    if "--file" in argv:
        OUT.mkdir(parents=True, exist_ok=True)
        tgt = OUT / "REGISTRATIONS.json"
        if tgt.exists():
            raise SystemExit(f"HALT: {tgt} exists — the filing is write-once")
        tgt.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        print(f"FILED {tgt.relative_to(ROOT)} sha256 {sha256_bytes(tgt.read_bytes())}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
