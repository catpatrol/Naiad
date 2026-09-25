#!/usr/bin/env python
"""TIER-C11 · TC11-SCORE — THE SCORER OF THE NINE [LEANS L-1.4, L-1.5, L-1.3, L-S.1,
L-W.4, AM-3, AM-7; research_outputs/tierc11/registrations/REGISTRATIONS.json operative specs].

Contract of record: exchange/queue/2026-09-24_TC11_APOLLO.md (sha256 bb38e016…, STEP Q
b9ed953).  Executor HEPHAESTUS; seed 20260924 (sensitivity 20260816); N_BOOT 4000.
Readings of record: research_outputs/tierc11/LEANS.md (frozen, sha 655e1605…) and
LEANS_AMENDMENTS.md (AM-1..AM-7).  A DECISION-SET module [L-F.2]: it imports only
tierc11_env (the RANGE-FREE shim) — never tierc11_nest, a census, stamps, null or
rangefinder module — and reads no Range object.  TC11 does NOT route through TP's
registry doors (register / require_registered / require_arm / score / external_book /
finish_family) [L-1.4]; the T5 bootstrap primitives are called directly, every seed and
n_boot passed explicitly.

WHAT IT DOES, IN ORDER
  1. VERIFIES REGISTRATIONS.json before anything is read or scored, and HALTS (nothing
     written) on ANY mismatch: the contract's bytes hash to the typed STEP Q sha; every
     text slice is RE-CUT from the contract by its line numbers and compared byte for
     byte (and its text_sha256); every context slice likewise; every payload sha is
     recomputed by the file's own law (sha256 of json.dumps(body without the two shas,
     sort_keys, ensure_ascii=False)); the hash chain is re-walked from the zero genesis
     (line_sha256 over {seq, registration, sha256, prev}); the head equals the chain's
     last line, the tracked REGISTRY_PIN.json head AND the typed head; the family is
     m 9 / q 0.10 / bar 0.011111 / seed 20260924; LEANS.md hashes to its frozen sha.
  2. READS THE REGBOOK INTERFACE and nothing else: research_outputs/tierc11/regbooks/
     <REG>/{STATUS.json, <arm>.parquet, <arm>.json}.  Every arm is validated (the
     required columns, dtypes, no nulls, unique keys, direction +-1, era == E.era_of(
     entry_close_ms), the AM-7 haircut law, the sidecar's n / sum / book_sha256 /
     ruler / panel / era_scope / collar).  A failure HALTS THAT ROW (no number, no
     verdict, no slot spent), never a neighbour.
  2b. CROSS-CHECKS each status word against the spec (STATUS-ILLEGAL) and its gating
     record (P-WARN-1 vs its condition.json, P-SCALP-2 vs R2_LENS_VERDICTS.json 1h) and,
     before any ruler, asserts the premises of pairing and gating: the L-1.5 identity law
     on every paired arm vs its own base (SC-15) and the post-filter law on a gate (SC-16).
     A failure HALTS that row [SC-17].
  3. RULES each BUILT registration by the ruler its SPEC names (never the sidecar):
       vs_zero     T5.cluster_boot(net_r, symbol)
       two_sample  T5.cluster_boot_diff(scored, base)            (same asset draw)
       paired      T5.cluster_boot of per-campaign deltas keyed (symbol, entry_ms);
                   HALT 'paired premise failed' unless the key sets are identical and
                   n == len(base)
     asset clusters; seed 20260924 and 20260816 beside; n_boot 4000; T5._ci_from:
     CI = the 5th..95th percentile, p = (#draws <= 0 + 1)/(B + 1).
     verdict_of_record = SUPPORTED iff ci_lo > 0 AND p <= 0.10/9, else NOT SUPPORTED
     ('— CI wholly below zero' appended when ci_hi < 0).  Beside it, deciding
     nothing: the deciding bound, the sensitivity-seed verdict, LOAO, the haircut twin
     (the same ruler on haircut_net_r), D15 (T5.d15), the gate's refused cohort, the
     honesty labels, the SCALE-IN-SAMPLE statistics (holdout slice, its in-sample count,
     the frozen-3.0 twin, the pick stability of the lens it consumes, the whole-tape
     fallback label) [SC-4, SC-14], the tuning / holdout slices, and for P-SCALP-2 the
     tuning-era R2 1h word, collared [§10].
  4. CLOSED_BY_PRECONDITION / CONDITION_NOT_MET rows print their reason in the verdict
     cell, no number, 'no slot spent'; m stays 9 and the bar never loosens.
  5. Tier-E arms (tierE__<slug>) and every derived slice are ruled the same way and
     printed with NO verdict word — `would_read_ci_only` — and the collar (tier
     'TIER-E', selection_not_a_result 'a SELECTION, not a result', gates 'nothing').
  6. F-BASE-IDENT (build-time): every 'base' arm of P-AGE-1, P-WIN-1, P-WARN-1,
     P-ADD-BRK, P-ADD-SFP, P-TP-RNG, P-RELAY-1 carries ONE book_sha256 and equals
     research_outputs/tierc11/books/v6_campaigns.parquet at that file's 6 dp.  A row
     whose base fails (or when the v6-equal bases split) HALTS [SC-7].
  7. WRITES (no-clobber; --refile to replace a record whose bytes differ):
       REGISTRY_CHECK.json  the verification record of step 1
       SCORES.json          every row, registered and Tier-E, every statistic
       FAMILY.json          m 9, q 0.10, bar, each row's verdict_of_record + spent_test
       BASE_IDENT.json      the F-BASE-IDENT record
       S0_VERDICTS.md       the §0 table (one row per registration) + detail blocks +
                            the Tier-E table (collared) + family + findings
       SCORE_MANIFEST.json  input book / sidecar shas and output shas

EXECUTOR SUB-READINGS (the frozen text is silent; each printed in READINGS):
  SC-1 clause (b) is evaluated EXACTLY: p = (k+1)/(B+1) <= 1/90 <=> 90(k+1) <= B+1.
       The deciding bound is the (floor((B+1)/90))-th smallest finite draw (the 44th of
       4000; p <= bar iff it is > 0); numpy's 1.111th percentile is printed beside.
  SC-2 LOAO = TP.loao_n's law, keyed (symbol, entry_ms) for paired [L-1.4]: N = the
       declared panel (the sidecar's panel), a panel that cannot be bootstrapped counts
       against, only panels excluding zero ABOVE count, bar ceil((N+1)/2); the count
       without zero-campaign panels beside.  At seed 20260924, sensitivity beside.
  SC-3 a Tier-E arm with a paired / two-sample ruler is ruled against the
       registration's base restricted to its era_scope, or against the sidecar's
       optional `base_arm` ('<arm>' or '<REG>/<arm>'; an extra field the interface
       allows) — e.g. the adds head-to-head.
  SC-4 SCALE-IN-SAMPLE: the holdout-slice statistic is derived here from the scored
       arm's era=='holdout' rows (base likewise), and a tierE arm slugged 'holdout*'
       is printed beside it; the frozen-3.0 twin is the tierE arm whose slug holds
       'frozen' (exact 'frozen_3_0_twin' first) — ABSENT is printed, never invented.
       Beside them, the count of holdout-slice campaigns whose own range read fell at
       an instant <= the era cut (in-sample), read from the regbook's extra columns
       (`scale_in_sample*` True, `n_adds_scale_in_sample` > 0, `die_close_ms` <= cut)
       [repair m-11]; 'not determinable' when the regbook carries none of them.
  SC-14 PICK STABILITY [L-R.2, repair MAJOR-1]: the lens each SCALE-IN-SAMPLE
       registration consumes is typed from its text of record — P-BRK-4H 4h ("4h macro
       death"), P-ADD-BRK / P-ADD-SFP 1h ("ONE LENS BELOW … 1h", "the 1h range"),
       P-TP-RNG 12h ("12h boundary").  The flag is read from
       research_outputs/tierc11/ranges/SCALE_PICKS.json (cells[].stable_first_half_vs_
       tuning, first_half_pick, tuning_pick) per CLASSIC5 asset at that lens; every
       change is printed in the §0 SCALE cell ("pick stability … CHANGED on …") and on
       every Tier-E row of that registration that consumes the calibrated pick (all but
       a frozen-3.0 arm: slug '*frozen*' or a `scale_kind` column with no 'calibrated').
       A regbook `stability_changed[_<lens>]` column that disagrees with the record on
       a CLASSIC5 row is a disclosure note.  Assets whose pick at that lens fell back to
       the whole tape (SCALE_PICKS.json fallback_cells) are labelled 'IN-SAMPLE
       everywhere' on every row holding them [L-R.2, repair m-13].
  SC-15 THE IDENTITY LAW [L-1.5, repair m-5]: on every paired arm ruled against the
       registration's own base (the scored arm and the paired Tier-E arms; never a
       base_arm head-to-head), the rows whose `acted_by` is null or blank must equal the
       base exactly on net_r, exit_close_ms and exit_reason; a regbook without
       `acted_by` cannot be asserted and HALTs likewise.  A failure HALTs the row.
  SC-16 A GATE IS A POST-FILTER [L-1.5, repair m-6]: the scored arm of an admission
       gate holds no key absent from the base and every kept row equals the base's
       row exactly on the 16 required columns; otherwise the row HALTs.
  SC-17 GATING STATUS WORDS ARE CROSS-CHECKED [L-W.4, L-S.1, §10; repair m-7]:
       P-WARN-1's STATUS must agree with its regbook's condition.json (BUILT iff met
       True, CONDITION_NOT_MET iff met False; met must equal ci_hi < 0); P-SCALP-2's
       with research_outputs/tierc11/stage_r/R2_LENS_VERDICTS.json lenses['1h']
       ['verdict'] (BUILT iff 'PASS', CLOSED_BY_PRECONDITION iff not).  A disagreement
       or an absent record HALTs the row.  P-SCALP-2's §0 cell prints the tuning-era
       R2 1h word beside it, collared (tier / selection_not_a_result / gates) [§10].
  SC-18 THE ADDS HEAD-TO-HEAD [spec tier_e_arms, repair m-14]: when neither add
       registration files a Tier-E arm whose base_arm is the other's scored arm, the
       scorer derives one ('derived__head_to_head_vs_<other>'), paired on (symbol,
       entry_ms), collared, deciding nothing.
  SC-19 REGBOOK STRICTNESS [repair m-2..m-4]: entry_ms / entry_close_ms / exit_close_ms
       are int64 and direction int8 exactly; a string field holding ',', '"', CR or LF
       HALTs (REGBOOK-STR: the canonical CSV of SC-13 does no quoting); 0 <
       entry_close_ms - entry_ms <= one lens step (the sidecar's optional `lens`, else
       4h — the lens bar of every TC11 registered book).
  SC-5 a gate's refused cohort = base keys absent from the scored arm (post-filter,
       L-1.5); the appendix names X = the refused cohort's sum of net_r.
  SC-6 a two-sample ruler on identical key sets is FLAGGED (not halted): the
       difference is 0 by construction; the flag rides the verdict cell.
  SC-7 F-BASE-IDENT compares the 13 regbook columns books/v6_campaigns carries
       (entry_close_ms, direction, entry_px, stop_px, r_dist, exit_close_ms,
       exit_reason, net_r, gross_r, fee_r, funding_r, era<-era_of_entry, lane) on the
       key (symbol, entry_ms), floats rounded to that file's 6 dp (pandas round, the
       tierc2_baseline._round_floats law).  A row is ruled against its base only if
       that base equals books/v6 AND carries the one sha the v6-equal bases share; a
       split among v6-equal bases halts every row ruled against a base.
  SC-8 the honesty label's <hazard> = '<key>: <its text up to the first top-level ;>'
       (the full text is printed in the detail block).
  SC-9 would_read_ci_only is one of 'CI above zero (lo > 0)', 'CI includes zero',
       'CI wholly below zero (hi < 0)', 'no interval' — a CI reading, no verdict word.
  SC-10 HALT scope: a registry mismatch halts the scorer before any write (exit 1); a
       book / premise / identity failure halts that ROW.  The exit code is a BIT FLAG
       word, every condition printed on an 'EXIT' line [repair m-9]: +2 a registered
       row HALTed, +4 a Tier-E row halted, +8 a registration has no STATUS.json (the
       family is incomplete), +16 a no-clobber refusal; 0 = none.
  SC-11 era-full registrations print the tuning and holdout slices of the scored arm
       beside, Tier-E [L-1.3].
  SC-12 checks of builder metadata of unknown summation / operation order: the
       sidecar's sum_net_r at 1e-6 (the estate's 6 dp); the AM-7 haircut law at 1e-12
       (float operation order only) — a HALT on scored / base arms, a disclosure on
       Tier-E arms (a maker twin applies the law to its taker legs only, AM-7).
  SC-13 book_sha256 = sha256 of the canonical CSV: the 16 required columns in the
       interface's order, rows sorted (symbol, entry_close_ms) (mergesort), a header
       line, fields joined by ',', ints as str(int), floats as repr(float), '\\n' line
       ends — byte-equal to pandas' to_csv(index=False) of the same frame (F-BASE-IDENT
       proves it on every planted arm).
  SC-20 A STATUS.json reason is the BUILDER's word, never the scorer's: it is printed
       under the label "builder's stage status:" (the detail block's status line, the
       closed rows' §0 cell) [final review statistics MINOR-1, fidelity MINOR-4].
  SC-21 PRE_SEEN FACTS IN THE §0 CELL [L-G.1 pre_seen, statistics MINOR-2]: a pre_seen
       honesty label carries "point known before filing; new campaigns since
       2026-09-21T16:00Z: scored <n> / base <n>", counted from the books by the entry
       bar's CLOSE > the TC10 pin (a bar closing AT the pin was seen by TC10).
  SC-22 D15 ON AN UNPAIRED RULER [statistics MINOR-3]: T5.d15 pairs on (symbol,
       entry_ms), so on a two-sample row (a gate: paired Δ 0 by construction; a lane:
       n_paired 0) and a vs-zero row (no base) the §0 D15 cell reads "D15 n/a
       (two-sample)" / "D15 n/a (vs zero)" and then the scored book's concentration:
       the top trade (largest |net_r|; ties -> the first in (symbol, entry_ms) order) and
       its share of the scored ΣR, the point with it removed from EVERY book holding its
       (symbol, entry_ms) key, the point without its asset (the LOAO point of that
       panel) and that asset's share of ΣR, and per asset Δ = scored mean − base mean
       (two-sample) or the scored mean (vs zero).  Deciding nothing; T5.d15 stays in
       SCORES.json and the detail block, labelled.

REPAIR G2 (final review 2026-09-25: statistics MINOR-1..4, reproducibility MINOR-2,
fidelity MINOR-4; labels and text only — no ruler, draw, statistic or verdict moved):
SC-20..SC-22 above; F-EXIT runs main() itself against an out-dir holding a bent record.

WHAT WOULD MAKE THIS WRONG: taking the ruler from the sidecar instead of the spec; a
CI-only verdict (clause (b) dropped); pairing on a key with lane (the paired key of
record is (symbol, entry_ms)); loosening the bar when a registration closes; a Tier-E
row carrying a verdict word; scoring against a base that is not v6.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_score.py --dry-run [--regbooks-root=DIR]
          # verify + validate + book facts only (n / sum R / mean R): no ruler, no CI, no p,
          # no verdict word, nothing written [TC10's dry-run law]
      ~/venvs/naiad/bin/python -B scripts/tierc11_score.py [--regbooks-root=DIR]
          [--out-dir=DIR] [--refile] [--regbooks-label=TOKEN]
      --out-dir defaults to research_outputs/tierc11/scores; otherwise it must be under
      scores/_det_score/ or outside the repo tree (a scratch).  --regbooks-label replaces
      the printed regbooks-root label (a display token only; the fixtures pass a fixed
      one so a transcript is reproducible under any --root [repair f-6]).
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sys
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_env as E                     # noqa: E402  (substrate guard + shim + hook)

import numpy as np                          # noqa: E402
import pandas as pd                         # noqa: E402

T5, TP, TB = E.T5, E.TP, E.TB

# ══════════════════════════════════════════════════════ 0 · CONSTANTS OF RECORD
CONTRACT_REL = "exchange/queue/2026-09-24_TC11_APOLLO.md"
CONTRACT_SHA = "bb38e016a8f3e55ca3bcc09fec53ba6b8dc40accb60d054f8163d033a898f835"
LEANS_REL = "research_outputs/tierc11/LEANS.md"
LEANS_SHA = "655e1605165e7a66c67f544e5cda421b46aa0b6fcd4cb97a6ad19654479f294f"
REGISTRATIONS_REL = "research_outputs/tierc11/registrations/REGISTRATIONS.json"
REGISTRATIONS_SHA = "648834bf30e20e92713bddef2374ddef1aae843f4d8ba152fc50166c8cc6f1ee"
PIN_REL = "research_outputs/tierc11/registrations/REGISTRY_PIN.json"
REGISTRY_HEAD = "6772568b31fcfb2d56eb8c80b66dedee4fb5082673369e872972df8f475ec8f9"
GENESIS = "0" * 64
REG_ORDER = ("P-WARN-1", "P-AGE-1", "P-WIN-1", "P-BRK-4H", "P-RELAY-1", "P-SCALP-2",
             "P-ADD-BRK", "P-ADD-SFP", "P-TP-RNG")
FAMILY_M = 9
FAMILY_Q = 0.10
BAR = FAMILY_Q / FAMILY_M                   # 0.0111… = 1/90
BAR_FRAC = Fraction(1, 10) / FAMILY_M       # exactly 1/90 [SC-1]
BAR_FILED = 0.011111                        # round(0.10/9, 6), as REGISTRATIONS.json files it
SEED = 20260924
SEED_SENS = 20260816
N_BOOT = 4000
AS_OF_LINE = "as_of_last_closed_4h: 2026-09-25T00:00:00Z"

RULER_OF_SPEC = {"paired (set kept; HALT unless key sets identical)": "paired",
                 "two-sample": "two_sample", "vs zero": "vs_zero"}
ERA_OF_SPEC = {"full corridor": "full", "holdout": "holdout"}
RULERS = ("vs_zero", "two_sample", "paired")
ERA_SCOPES = ("full", "holdout", "tuning")
STATUS_WORDS = ("BUILT", "CLOSED_BY_PRECONDITION", "CONDITION_NOT_MET")
LABEL_KEYS = ("pre_seen", "selection_hazard")

REQUIRED = ("symbol", "entry_ms", "entry_close_ms", "direction", "entry_px", "stop_px",
            "r_dist", "exit_close_ms", "exit_reason", "net_r", "gross_r", "fee_r",
            "funding_r", "haircut_net_r", "era", "lane")
INT_COLS = ("entry_ms", "entry_close_ms", "direction", "exit_close_ms")
FLOAT_COLS = ("entry_px", "stop_px", "r_dist", "net_r", "gross_r", "fee_r", "funding_r",
              "haircut_net_r")
STR_COLS = ("symbol", "exit_reason", "era", "lane")
SORT_KEY = ["symbol", "entry_close_ms"]
PAIR_KEY = ["symbol", "entry_ms"]
ARM_RX = re.compile(r"^(scored|base|tierE__[a-z0-9_]+)$")
COLLAR = {"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
          "gates": "nothing"}
CI_READINGS = ("CI above zero (lo > 0)", "CI includes zero",
               "CI wholly below zero (hi < 0)", "no interval")
VERDICT_WORD_RX = re.compile(r"\bSUPPORTED\b|\bverdict\b", re.IGNORECASE)
FORBIDDEN_TIER_E_KEY_RX = re.compile(r"verdict|clears_bar|spent_test", re.IGNORECASE)
HAIRCUT_TOL = 1e-12                         # SC-12: float operation order only
SUM_TOL = 1e-6                              # SC-12: the estate's 6 dp
NET_LAW_TOL = 1e-9                          # disclosure only

BASE_IDENT_REGS = ("P-AGE-1", "P-WIN-1", "P-WARN-1", "P-ADD-BRK", "P-ADD-SFP", "P-TP-RNG",
                   "P-RELAY-1")
V6_CAMPAIGNS = E.OUT / "books" / "v6_campaigns.parquet"
V6_MANIFEST = E.OUT / "books" / "build_manifest.json"
V6_CMP = (("entry_close_ms", "entry_close_ms"), ("direction", "direction"),
          ("entry_px", "entry_px"), ("stop_px", "stop_px"), ("r_dist", "r_dist"),
          ("exit_close_ms", "exit_close_ms"), ("exit_reason", "exit_reason"),
          ("net_r", "net_r"), ("gross_r", "gross_r"), ("fee_r", "fee_r"),
          ("funding_r", "funding_r"), ("era", "era_of_entry"), ("lane", "lane"))
V6_DP = 6

TC10_PIN_MS = 1_790_006_400_000            # 2026-09-21T16:00:00Z [L-G.1 pre_seen, L-T.6]
TC10_PIN_LABEL = "2026-09-21T16:00Z"
PRESEEN_TIME_COL = "entry_close_ms"         # SC-21: 'entered after the pin' by the entry CLOSE
BUILDER_STATUS_LABEL = "builder's stage status:"   # SC-20: a STATUS.json reason is the builder's
CONC_TOP_FROM_EVERY_BOOK = True             # SC-22: the top trade leaves every book holding its key
LEANS_AMEND_REL = "research_outputs/tierc11/LEANS_AMENDMENTS.md"   # hashed [repair m-12]
# SC-14 / SC-17: the plain-JSON records read beside the regbooks (never a Range object)
SCALE_PICKS_PATH = E.OUT / "ranges" / "SCALE_PICKS.json"
R2_VERDICTS_PATH = E.OUT / "stage_r" / "R2_LENS_VERDICTS.json"
SCALE_LENS_OF = {"P-BRK-4H": "4h", "P-ADD-BRK": "1h", "P-ADD-SFP": "1h", "P-TP-RNG": "12h"}
SCALE_CAUSAL_ERA = "holdout"                # L-R.2: the only slice with a causal scale
PRECONDITION_LENS = {"P-SCALP-2": "1h"}      # L-S.1: the R2 lens verdict of record gating it
CONDITION_FILE = {"P-WARN-1": "condition.json"}  # L-W.4: the condition record in its regbook
HEAD_TO_HEAD = {"P-ADD-BRK": "P-ADD-SFP", "P-ADD-SFP": "P-ADD-BRK"}   # SC-18
ERA_TIME_COL = "entry_close_ms"             # L-1.3: era by the entry bar's CLOSE
LENS_STEP_MS = {"5m": 300_000, "15m": 900_000, "1h": 3_600_000, "4h": 14_400_000,
                "12h": 43_200_000, "1d": 86_400_000}
DEFAULT_ENTRY_LENS = "4h"                   # SC-19: the lens bar of every TC11 registered book
INT_DTYPES = {"entry_ms": np.int64, "entry_close_ms": np.int64, "exit_close_ms": np.int64,
              "direction": np.int8}         # SC-19: the interface's exact dtypes
STR_BAD_RX = r'[,"\r\n]'                   # SC-19: the canonical CSV does no quoting
IDENTITY_COLS = ("net_r", "exit_close_ms", "exit_reason")   # L-1.5 (exit_ms -> exit_close_ms)
EXIT_FLAGS = (("a registered row HALTed", 2), ("a Tier-E row halted", 4),
              ("a registration is ABSENT (no STATUS.json)", 8), ("a no-clobber refusal", 16))
REGBOOKS = E.OUT / "regbooks"
SCORES = E.OUT / "scores"
DET_ROOT = SCORES / "_det_score"
OUTPUT_FILES = ("REGISTRY_CHECK.json", "SCORES.json", "FAMILY.json", "BASE_IDENT.json",
                "S0_VERDICTS.md", "SCORE_MANIFEST.json")

READINGS = (
    "[LEAN-HEPHAESTUS] L-1.4 rulers from the SPEC (paired: P-WARN-1, P-ADD-BRK, P-ADD-SFP, "
    "P-TP-RNG · two-sample: P-AGE-1, P-WIN-1, P-RELAY-1 · vs zero: P-BRK-4H, P-SCALP-2); "
    "T5.cluster_boot / cluster_boot_diff / _ci_from, asset clusters, seed 20260924 "
    "(20260816 beside), n_boot 4000 passed explicitly",
    "[LEAN-HEPHAESTUS] L-1.4 verdict_of_record = SUPPORTED iff ci_lo > 0 AND p <= 0.10/9, "
    "else NOT SUPPORTED ('— CI wholly below zero' when ci_hi < 0); m = 9 in every case",
    "[LEAN-HEPHAESTUS] SC-1 clause (b) exact: p = (k+1)/(B+1) <= 1/90 <=> 90(k+1) <= B+1; "
    "deciding bound = the floor((B+1)/90)-th smallest finite draw (44th of 4000); numpy's "
    "1.111th percentile beside",
    "[LEAN-HEPHAESTUS] SC-2 LOAO = TP.loao_n's law keyed (symbol, entry_ms): N = declared "
    "panel, unbootstrappable panel counts against, above-only, bar ceil((N+1)/2); decides "
    "nothing",
    "[LEAN-HEPHAESTUS] SC-3 Tier-E paired / two-sample arm: vs the registration's base "
    "restricted to its era_scope, or the sidecar's optional base_arm",
    "[LEAN-HEPHAESTUS] SC-4 SCALE-IN-SAMPLE: holdout slice derived from the scored arm "
    "(a tierE 'holdout*' arm beside); frozen-3.0 twin = tierE arm slugged '*frozen*'; the "
    "holdout campaigns whose range read fell <= the era cut counted beside",
    "[LEAN-HEPHAESTUS] SC-5 refused cohort = base keys absent from the scored arm; "
    "'on per-campaign expectancy only; the gate forfeits +X R total' iff mean(refused) > 0",
    "[LEAN-HEPHAESTUS] SC-6 two-sample on identical key sets: FLAGGED, not halted",
    "[LEAN-HEPHAESTUS] SC-7 F-BASE-IDENT: one book_sha256 across the base arms AND equal to "
    "books/v6_campaigns.parquet on 13 columns at its 6 dp; a row halts if its base fails v6 or "
    "the v6-equal bases split",
    "[LEAN-HEPHAESTUS] SC-8 honesty <hazard> = '<key>: <text up to its first top-level ;>'",
    "[LEAN-HEPHAESTUS] SC-9 Tier-E: would_read_ci_only in {CI above zero (lo > 0) | CI "
    "includes zero | CI wholly below zero (hi < 0) | no interval}; collar tier/"
    "selection_not_a_result/gates",
    "[LEAN-HEPHAESTUS] SC-10 registry mismatch halts the scorer before any write; a book / "
    "premise / identity failure halts its row only; exit = bit flags: +2 registered HALT, "
    "+4 Tier-E halted, +8 ABSENT, +16 no-clobber; every condition printed",
    "[LEAN-HEPHAESTUS] SC-11 era-full registrations: tuning + holdout slices beside, Tier-E "
    "[L-1.3]",
    "[LEAN-HEPHAESTUS] SC-12 sidecar sum_net_r at 1e-6; AM-7 haircut law at 1e-12 (HALT "
    "on scored/base, disclosure on Tier-E)",
    "[LEAN-HEPHAESTUS] SC-13 book_sha256 = sha256(canonical CSV of the 16 required "
    "columns sorted (symbol, entry_close_ms), floats repr)",
    "[LEAN-HEPHAESTUS] SC-14 pick stability [L-R.2]: lens consumed P-BRK-4H 4h, P-ADD-BRK / "
    "P-ADD-SFP 1h, P-TP-RNG 12h (texts of record); the per-CLASSIC5-asset change "
    "(SCALE_PICKS.json first half of tuning vs tuning) flagged on the §0 SCALE cell and every "
    "Tier-E row consuming the calibrated pick; whole-tape fallback cells labelled IN-SAMPLE",
    "[LEAN-HEPHAESTUS] SC-15 identity law [L-1.5]: paired arms vs their own base — rows with "
    "acted_by blank equal the base exactly on net_r, exit_close_ms, exit_reason, else HALT",
    "[LEAN-HEPHAESTUS] SC-16 gate = post-filter [L-1.5]: no key outside the base, every kept "
    "row equal to the base on the 16 columns, else HALT",
    "[LEAN-HEPHAESTUS] SC-17 gating status cross-checked: P-WARN-1 vs condition.json (met, "
    "ci_hi < 0), P-SCALP-2 vs R2_LENS_VERDICTS.json 1h; the tuning-era R2 1h word printed "
    "beside P-SCALP-2, collared [§10]",
    "[LEAN-HEPHAESTUS] SC-18 adds head-to-head: derived (paired, collared) when not filed "
    "with a base_arm",
    "[LEAN-HEPHAESTUS] SC-19 regbook strictness: int64 times, int8 direction, no ',', '\"', "
    "CR, LF in a string field, 0 < entry_close_ms - entry_ms <= one lens step (4h unless the "
    "sidecar names a lens)",
    "[LEAN-HEPHAESTUS] SC-20 a STATUS.json reason is the builder's word: printed under "
    "\"builder's stage status:\" (detail status line, closed §0 cells), never as the scorer's",
    "[LEAN-HEPHAESTUS] SC-21 pre_seen: the §0 honesty label carries 'point known before "
    "filing; new campaigns since 2026-09-21T16:00Z: scored <n> / base <n>', counted from the "
    "books by the entry bar's CLOSE > the TC10 pin",
    "[LEAN-HEPHAESTUS] SC-22 D15 on an unpaired ruler: 'D15 n/a (two-sample)' / 'D15 n/a (vs "
    "zero)', then the scored book's top trade (largest |net_r|) and its share of ΣR, the point "
    "without it (removed from every book holding its key), the point without its asset and "
    "that asset's share of ΣR, per asset Δ = scored mean - base mean (two-sample) or the "
    "scored mean (vs zero); deciding nothing",
)


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ══════════════════════════════════════════ 1 · THE REGISTRY, VERIFIED BEFORE ANY LOOK
def _payload_sha(reg: dict) -> str:
    body = {k: v for k, v in reg.items() if k not in ("text_sha256", "sha256")}
    return sha256_bytes(json.dumps(body, sort_keys=True, ensure_ascii=False).encode())


def _line_sha(line: dict) -> str:
    body = {"seq": line.get("seq"), "registration": line.get("registration"),
            "sha256": line.get("sha256"), "prev": line.get("prev")}
    return sha256_bytes(json.dumps(body, sort_keys=True).encode())


def verify_registrations(doc: dict, contract: bytes, pin: dict,
                         leans_bytes: bytes | None = None,
                         file_bytes: bytes | None = None) -> list[str]:
    """Every mismatch between REGISTRATIONS.json and (the contract, its own laws, the
    tracked pin, the typed referees) as a finding naming its detector.  Never stops at
    the first: each detector is judged on its own [F-SCORE-REG]."""
    out: list[str] = []
    try:
        csha = sha256_bytes(contract)
        if csha != CONTRACT_SHA:
            out.append(f"CONTRACT-SHA: the contract hashes to {csha} != STEP Q {CONTRACT_SHA}")
        if (doc.get("contract") or {}).get("sha256") != CONTRACT_SHA:
            out.append(f"CONTRACT-SHA: REGISTRATIONS.json names contract sha "
                       f"{(doc.get('contract') or {}).get('sha256')} != {CONTRACT_SHA}")
        if file_bytes is not None and sha256_bytes(file_bytes) != REGISTRATIONS_SHA:
            out.append(f"FILE-SHA: REGISTRATIONS.json hashes to {sha256_bytes(file_bytes)} "
                       f"!= the filing of record {REGISTRATIONS_SHA}")
        if leans_bytes is not None and sha256_bytes(leans_bytes) != LEANS_SHA:
            out.append(f"LEANS-SHA: LEANS.md hashes to {sha256_bytes(leans_bytes)} != frozen "
                       f"{LEANS_SHA}")
        if (doc.get("leans") or {}).get("sha256") != LEANS_SHA:
            out.append(f"LEANS-SHA: REGISTRATIONS.json names LEANS sha "
                       f"{(doc.get('leans') or {}).get('sha256')} != {LEANS_SHA}")
        fam = (doc.get("family_m"), doc.get("family_q"), doc.get("family_bar"), doc.get("seed"))
        if fam != (FAMILY_M, FAMILY_Q, BAR_FILED, SEED) or round(BAR, 6) != BAR_FILED:
            out.append(f"FAMILY: (m, q, bar, seed) = {fam} != ({FAMILY_M}, {FAMILY_Q}, "
                       f"{BAR_FILED}, {SEED})")
        lines = contract.decode("utf-8").split("\n")

        def cut(lo: int, hi: int) -> str:
            return "\n".join(lines[lo - 1:hi])

        regs = list(doc.get("registrations") or [])
        ids = [r.get("registration") for r in regs]
        if ids != list(REG_ORDER):
            out.append(f"ORDER: registrations {ids} != the typed nine {list(REG_ORDER)}")
        for i, r in enumerate(regs, 1):
            rid = r.get("registration")
            if r.get("seq") != i:
                out.append(f"ORDER: {rid} seq {r.get('seq')} != position {i}")
            lo, hi = (r.get("text_lines") or [0, 0])[:2]
            text = cut(int(lo), int(hi)) if lo and hi else ""
            if text != r.get("text_of_record"):
                out.append(f"TEXT-SLICE: {rid} lines {lo}-{hi} re-cut from the contract != "
                           f"text_of_record")
            if not text.lstrip().startswith(str(rid)):
                out.append(f"TEXT-SLICE: {rid} slice {lo}-{hi} does not begin with its id")
            if f"[{r.get('prior_pct')}%" not in text:
                out.append(f"TEXT-SLICE: {rid} prior {r.get('prior_pct')}% is not the "
                           f"contract's")
            if sha256_bytes(str(r.get("text_of_record")).encode()) != r.get("text_sha256"):
                out.append(f"TEXT-SHA: {rid} text_sha256 != sha256(text_of_record)")
            for ctx in r.get("context_of_record") or []:
                a, b = ctx.get("lines")
                if cut(int(a), int(b)) != ctx.get("text"):
                    out.append(f"CONTEXT-SLICE: {rid} context lines {a}-{b} != the contract")
            psha = _payload_sha(r)
            if psha != r.get("sha256"):
                out.append(f"PAYLOAD-SHA: {rid} payload hashes to {psha[:16]}… != filed "
                           f"{str(r.get('sha256'))[:16]}…")
            if (r.get("family_m"), r.get("family_bar"), r.get("seed")) != (FAMILY_M, BAR_FILED,
                                                                         SEED):
                out.append(f"FAMILY: {rid} (m, bar, seed) = ({r.get('family_m')}, "
                           f"{r.get('family_bar')}, {r.get('seed')})")
        chain = list(doc.get("chain") or [])
        if len(chain) != len(REG_ORDER) or len(chain) != len(regs):
            out.append(f"CHAIN: {len(chain)} chain lines for {len(regs)} registrations "
                       f"(typed {len(REG_ORDER)})")
        prev = GENESIS
        for i, (ln, r) in enumerate(zip(chain, regs), 1):
            rid = r.get("registration")
            if (ln.get("seq"), ln.get("registration"), ln.get("sha256")) != (
                    i, rid, r.get("sha256")):
                out.append(f"CHAIN: line {i} names ({ln.get('seq')}, {ln.get('registration')}, "
                           f"{str(ln.get('sha256'))[:16]}…) != ({i}, {rid}, "
                           f"{str(r.get('sha256'))[:16]}…)")
            if ln.get("prev") != prev:
                out.append(f"CHAIN: line {i} prev {str(ln.get('prev'))[:16]}… != the previous "
                           f"line's sha {prev[:16]}…")
            lsha = _line_sha(ln)
            if lsha != ln.get("line_sha256"):
                out.append(f"CHAIN: line {i} line_sha256 {str(ln.get('line_sha256'))[:16]}… "
                           f"!= recomputed {lsha[:16]}…")
            prev = lsha
        if doc.get("head") != prev:
            out.append(f"HEAD: REGISTRATIONS.json head {str(doc.get('head'))[:16]}… != the "
                       f"chain's last line {prev[:16]}…")
        if pin.get("head") != doc.get("head"):
            out.append(f"HEAD: REGISTRY_PIN.json head {str(pin.get('head'))[:16]}… != "
                       f"REGISTRATIONS.json head {str(doc.get('head'))[:16]}…")
        if pin.get("head") != REGISTRY_HEAD or prev != REGISTRY_HEAD:
            out.append(f"HEAD: pin head {str(pin.get('head'))[:16]}… / chain {prev[:16]}… != "
                       f"the head of record {REGISTRY_HEAD[:16]}…")
        pfam = (pin.get("contract_sha256"), pin.get("leans_sha256"), pin.get("n"),
                pin.get("family_m"), pin.get("family_bar"))
        if pfam != (CONTRACT_SHA, LEANS_SHA, len(REG_ORDER), FAMILY_M, BAR_FILED):
            out.append(f"PIN: REGISTRY_PIN.json (contract, leans, n, m, bar) = "
                       f"({str(pfam[0])[:12]}…, {str(pfam[1])[:12]}…, {pfam[2]}, {pfam[3]}, "
                       f"{pfam[4]}) is not the record")
    except Exception as e:                  # a mangled structure is a finding, not a crash
        out.append(f"REGISTRY-SHAPE: {type(e).__name__}: {e}")
    return out


def load_registry(root: Path = ROOT) -> tuple[dict, dict]:
    """Read and VERIFY the registry; HALT (SystemExit, nothing written) on any finding."""
    contract = (root / CONTRACT_REL).read_bytes()
    fbytes = (root / REGISTRATIONS_REL).read_bytes()
    doc = json.loads(fbytes.decode("utf-8"))
    pin = json.loads((root / PIN_REL).read_text(encoding="utf-8"))
    leans = (root / LEANS_REL).read_bytes()
    bad = verify_registrations(doc, contract, pin, leans_bytes=leans, file_bytes=fbytes)
    if bad:
        raise SystemExit("HALT (REGISTRY): REGISTRATIONS.json does not verify — nothing is "
                         "scored:\n  " + "\n  ".join(bad))
    lines = contract.decode("utf-8").split("\n")
    per = []
    for r, ln in zip(doc["registrations"], doc["chain"]):
        lo, hi = r["text_lines"]
        per.append({"seq": r["seq"], "registration": r["registration"],
                    "text_lines": [lo, hi],
                    "text_slice_recut_equal": "\n".join(lines[lo - 1:hi]) == r["text_of_record"],
                    "text_sha256": r["text_sha256"], "payload_sha256": _payload_sha(r),
                    "payload_sha256_filed": r["sha256"], "line_sha256": ln["line_sha256"],
                    "prev": ln["prev"]})
    amend = root / LEANS_AMEND_REL
    rec = {"contract": {"path": CONTRACT_REL, "sha256": sha256_bytes(contract)},
           "leans": {"path": LEANS_REL, "sha256": sha256_bytes(leans)},
           # binding amendments AM-1..AM-7 (AM-3, AM-7 implemented here): hashed, not pinned
           "leans_amendments": {"path": LEANS_AMEND_REL,
                                "sha256": (sha256_bytes(amend.read_bytes())
                                           if amend.exists() else None)},
           "registrations": {"path": REGISTRATIONS_REL, "sha256": sha256_bytes(fbytes)},
           "pin": {"path": PIN_REL, "head": pin["head"]},
           "head": doc["head"], "head_of_record_typed": REGISTRY_HEAD,
           "family": {"m": FAMILY_M, "q": FAMILY_Q, "bar": BAR, "bar_filed": BAR_FILED},
           "per_registration": per, "findings": [],
           "law": doc.get("law")}
    return doc, rec


def spec_of(reg: dict) -> dict:
    """The operative spec, normalised; HALT on a value no reading names."""
    s = reg["operative_spec"]
    rid = reg["registration"]
    ruler = RULER_OF_SPEC.get(s.get("ruler"))
    era = ERA_OF_SPEC.get(s.get("era"))
    if ruler is None or era is None:
        raise SystemExit(f"HALT (SPEC): {rid} ruler {s.get('ruler')!r} / era {s.get('era')!r} "
                         f"is not a known reading")
    panels = {"CLASSIC5": tuple(E.CLASSIC5), "PANEL17": tuple(E.PANEL17)}
    if s.get("panel") not in panels:
        raise SystemExit(f"HALT (SPEC): {rid} panel {s.get('panel')!r}")
    labels = {k: s[k] for k in LABEL_KEYS if s.get(k)}
    tea = list(s.get("tier_e_arms") or [])
    return {"registration": rid, "seq": reg["seq"], "prior_pct": reg["prior_pct"],
            "kind": s.get("kind"), "ruler": ruler, "era": era, "panel_name": s["panel"],
            "panel": panels[s["panel"]], "base_named": s.get("base"),
            "gate": str(s.get("kind", "")).startswith("admission gate"),
            "precondition": s.get("precondition"), "condition": s.get("condition"),
            "labels": labels, "scale_in_sample": s.get("scale_in_sample"),
            "tier_e_arms": tea, "named_risk": s.get("named_risk"),
            "d15_asked": any("D15" in x for x in tea) or "D15" in reg["text_of_record"],
            "text_of_record": reg["text_of_record"], "text_lines": reg["text_lines"],
            "payload_sha256": reg["sha256"]}


def first_clause(t: str) -> str:
    """The text up to its first ';' at parenthesis depth 0 (the whole text if none)."""
    depth = 0
    for i, ch in enumerate(t):
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth = max(0, depth - 1)
        elif ch == ";" and depth == 0:
            return t[:i].strip()
    return t.strip()


def hazard_of(spec: dict) -> str | None:
    """SC-8: '<key>: <text up to its first top-level ;>' per honesty label, joined."""
    parts = []
    for k in LABEL_KEYS:
        t = spec["labels"].get(k)
        if t:
            parts.append(f"{k}: {first_clause(t)}")
    return " · ".join(parts) if parts else None


def builder_status(reason) -> str:
    """SC-20: a STATUS.json reason, printed as the BUILDER's word (it sits beside the
    scorer's verdict and must never read as the scorer's)."""
    return f"{BUILDER_STATUS_LABEL} {reason}"


def new_since_pin(df: pd.DataFrame) -> int:
    """SC-21: campaigns entered after the TC10 pin (2026-09-21T16:00Z), by the entry bar's
    CLOSE — a bar closing AT the pin was seen by TC10."""
    return int((df[PRESEEN_TIME_COL].to_numpy(np.int64) > TC10_PIN_MS).sum())


def preseen_facts(a: pd.DataFrame, b: pd.DataFrame | None) -> dict:
    """SC-21 [L-G.1 pre_seen]: what a pre_seen re-score can add beside its known point —
    the campaigns entered after the TC10 pin, counted in the scored book and its base."""
    ns = new_since_pin(a)
    nb = None if b is None else new_since_pin(b)
    return {"since": TC10_PIN_LABEL, "time_col": PRESEEN_TIME_COL, "scored": ns, "base": nb,
            "text": (f"point known before filing; new campaigns since {TC10_PIN_LABEL}: "
                     f"scored {ns} / base {'—' if nb is None else nb}")}


def label_of(spec: dict, facts: dict | None) -> str | None:
    """The §0 honesty label: SC-8's '<key>: <first clause>' per label, the pre_seen clause
    carrying SC-21's facts."""
    parts = []
    for k in LABEL_KEYS:
        t = spec["labels"].get(k)
        if t:
            p = f"{k}: {first_clause(t)}"
            if k == "pre_seen" and facts:
                p += f"; {facts['text']}"
            parts.append(p)
    return " · ".join(parts) if parts else None


# ══════════════════════════════════════════════ 2 · THE REGBOOK INTERFACE
def canonical_csv(df: pd.DataFrame) -> bytes:
    """SC-13: the required columns in the interface's order, rows sorted (symbol,
    entry_close_ms), a header, ',' joined, ints str(int), floats repr(float), '\\n'."""
    d = df.loc[:, list(REQUIRED)].sort_values(SORT_KEY, kind="mergesort")
    cols = {c: d[c].tolist() for c in REQUIRED}
    rows = [",".join(REQUIRED)]
    for i in range(len(d)):
        f = []
        for c in REQUIRED:
            v = cols[c][i]
            if c in FLOAT_COLS:
                f.append(repr(float(v)))
            elif c in INT_COLS:
                f.append(str(int(v)))
            else:
                f.append(str(v))
        rows.append(",".join(f))
    return ("\n".join(rows) + "\n").encode("utf-8")


def book_sha256(df: pd.DataFrame) -> str:
    return sha256_bytes(canonical_csv(df))


def _fees() -> dict:
    return E.fees()


def validate_book(df: pd.DataFrame, side: dict, rid: str, arm: str,
                  fees: dict) -> tuple[list[str], list[str]]:
    """(halts, notes) for one arm against the REGBOOK INTERFACE [F-KEY]."""
    halts: list[str] = []
    notes: list[str] = []
    tag = f"{rid}/{arm}"
    miss = [c for c in REQUIRED if c not in df.columns]
    if miss:
        return [f"REGBOOK-COLS: {tag} lacks required column(s) {miss}"], notes
    for c in INT_COLS:
        if df[c].dtype != INT_DTYPES[c]:
            halts.append(f"REGBOOK-DTYPE: {tag} {c} is {df[c].dtype}, not "
                         f"{np.dtype(INT_DTYPES[c]).name} [SC-19]")
    for c in FLOAT_COLS:
        if df[c].dtype != np.float64:
            halts.append(f"REGBOOK-DTYPE: {tag} {c} is {df[c].dtype}, not float64")
    for c in STR_COLS:
        if not (pd.api.types.is_object_dtype(df[c]) or pd.api.types.is_string_dtype(df[c])):
            halts.append(f"REGBOOK-DTYPE: {tag} {c} is {df[c].dtype}, not str")
    nul = {c: int(df[c].isna().sum()) for c in REQUIRED if int(df[c].isna().sum())}
    if nul:
        halts.append(f"REGBOOK-NULL: {tag} nulls in required columns {nul}")
    if halts:
        return halts, notes
    bad_str = {c: int(df[c].astype(str).str.contains(STR_BAD_RX, regex=True).sum())
               for c in STR_COLS}
    bad_str = {c: k for c, k in bad_str.items() if k}
    if bad_str:
        halts.append(f"REGBOOK-STR: {tag} string field(s) holding ',', '\"', CR or LF {bad_str} "
                     f"— the canonical CSV (SC-13) does no quoting [SC-19]")
    dup = int(df.duplicated(subset=SORT_KEY).sum())
    if dup:
        halts.append(f"REGBOOK-KEY: {tag} {dup} duplicated (symbol, entry_close_ms) key(s)")
    if arm == "base" or side.get("ruler") == "paired" or side.get("kind") == "base":
        dup2 = int(df.duplicated(subset=PAIR_KEY).sum())
        if dup2:
            halts.append(f"REGBOOK-KEY: {tag} {dup2} duplicated (symbol, entry_ms) pairing "
                         f"key(s)")
    bad_dir = sorted(set(int(x) for x in df["direction"]) - {1, -1})
    if bad_dir:
        halts.append(f"REGBOOK-DIR: {tag} direction values {bad_dir} outside {{+1, -1}}")
    want_era = E.era_of(df[ERA_TIME_COL].to_numpy(np.int64))
    bad_era = int((df["era"].to_numpy(object) != np.asarray(want_era, object)).sum())
    if bad_era:
        halts.append(f"REGBOOK-ERA: {tag} {bad_era} row(s) whose era != E.era_of("
                     f"entry_close_ms) [L-1.3: era by the entry bar's CLOSE]")
    lens = side.get("lens") if isinstance(side.get("lens"), str) else DEFAULT_ENTRY_LENS
    step = LENS_STEP_MS.get(lens)
    if step is None:
        halts.append(f"REGBOOK-TIME: {tag} sidecar lens {lens!r} is not one of "
                     f"{sorted(LENS_STEP_MS)}")
    else:
        gap = df["entry_close_ms"].to_numpy(np.int64) - df["entry_ms"].to_numpy(np.int64)
        n_gap = int(((gap <= 0) | (gap > step)).sum())
        if n_gap:
            halts.append(f"REGBOOK-TIME: {tag} {n_gap} row(s) with entry_close_ms - entry_ms "
                         f"outside (0, {lens}] — entry_ms is the open of the lens bar holding "
                         f"the entry close [SC-19]")
    n_back = int((df["exit_close_ms"] < df["entry_close_ms"]).sum())
    if n_back:
        halts.append(f"REGBOOK-TIME: {tag} {n_back} row(s) with exit_close_ms < entry_close_ms")
    if bool((df["r_dist"] <= 0).any()):
        halts.append(f"REGBOOK-RDIST: {tag} r_dist <= 0 on some row")
    stray = sorted(set(df["symbol"]) - set(fees))
    if stray:
        halts.append(f"REGBOOK-SYMBOL: {tag} symbols {stray} are not fee-schedule stems")
    else:
        slip = df["symbol"].map(lambda s: fees[s]["slippage_bps_side"]).to_numpy(float)
        tak = df["symbol"].map(lambda s: fees[s]["taker_bps_side"]).to_numpy(float)
        want = df["net_r"].to_numpy(float) - df["fee_r"].to_numpy(float) * (slip / tak)
        err = np.abs(df["haircut_net_r"].to_numpy(float) - want)
        nbad = int((err > HAIRCUT_TOL).sum())
        if nbad:
            msg = (f"REGBOOK-HAIRCUT: {tag} {nbad} row(s) break the AM-7 law haircut_net_r = "
                   f"net_r - fee_r*slip/taker (worst {float(err.max()):.3e})")
            (notes if arm.startswith("tierE__") else halts).append(msg)
    net_err = np.abs(df["net_r"].to_numpy(float) - (df["gross_r"].to_numpy(float)
                                                     - df["fee_r"].to_numpy(float)
                                                     - df["funding_r"].to_numpy(float)))
    nn = int((net_err > NET_LAW_TOL).sum())
    if nn:
        notes.append(f"NET-LAW (disclosure): {tag} {nn}/{len(df)} row(s) with net_r != gross_r "
                     f"- fee_r - funding_r at 1e-9 (worst {float(net_err.max()):.3e})")
    # the sidecar
    kind_want = "tierE" if arm.startswith("tierE__") else arm
    for k, want_v in (("registration", rid), ("arm", arm), ("kind", kind_want)):
        if side.get(k) != want_v:
            halts.append(f"SIDECAR: {tag} {k} {side.get(k)!r} != {want_v!r}")
    if side.get("ruler") not in RULERS:
        halts.append(f"SIDECAR: {tag} ruler {side.get('ruler')!r} not in {RULERS}")
    if side.get("era_scope") not in ERA_SCOPES:
        halts.append(f"SIDECAR: {tag} era_scope {side.get('era_scope')!r} not in {ERA_SCOPES}")
    elif side.get("era_scope") != "full":
        off = int((df["era"] != side["era_scope"]).sum())
        if off:
            halts.append(f"SIDECAR: {tag} era_scope {side['era_scope']} but {off} row(s) "
                         f"carry another era")
    pan = side.get("panel")
    if not isinstance(pan, list) or not pan:
        halts.append(f"SIDECAR: {tag} panel {pan!r} is not a list of stems")
    else:
        stray_p = sorted(set(df["symbol"]) - set(pan))
        if stray_p:
            halts.append(f"STRAY-ASSET: {tag} holds {stray_p} outside its declared panel")
    if side.get("n") != len(df):
        halts.append(f"SIDECAR: {tag} n {side.get('n')} != {len(df)} rows")
    try:
        s_ok = abs(float(side.get("sum_net_r")) - float(df["net_r"].sum())) <= SUM_TOL
    except (TypeError, ValueError):
        s_ok = False
    if not s_ok:
        halts.append(f"SIDECAR: {tag} sum_net_r {side.get('sum_net_r')} != {df['net_r'].sum()!r}"
                     f" at 1e-6")
    got = book_sha256(df)
    if side.get("book_sha256") != got:
        halts.append(f"BOOK-SHA: {tag} sidecar claims {str(side.get('book_sha256'))[:16]}… but "
                     f"the parquet hashes to {got[:16]}…")
    for k in ("description", "source_script"):
        if not isinstance(side.get(k), str) or not side.get(k):
            halts.append(f"SIDECAR: {tag} {k} missing")
    if kind_want == "tierE":
        for k, v in COLLAR.items():
            if side.get(k) != v:
                halts.append(f"SIDECAR-COLLAR: {tag} {k} {side.get(k)!r} != {v!r}")
    return halts, notes


def load_arm(regdir: Path, rid: str, arm: str, fees: dict) -> dict:
    pq, js = regdir / f"{arm}.parquet", regdir / f"{arm}.json"
    if not ARM_RX.match(arm):
        return {"arm": arm, "df": None, "side": {}, "halts": [f"ARM-NAME: {rid}/{arm} is not "
                                                              f"scored|base|tierE__<slug>"],
                "notes": [], "sha": None, "side_sha": None}
    if not pq.exists() or not js.exists():
        return {"arm": arm, "df": None, "side": {}, "halts": [
            f"ARM-ABSENT: {rid}/{arm} lacks {'parquet' if not pq.exists() else 'json'}"],
                "notes": [], "sha": None, "side_sha": None}
    sb = js.read_bytes()
    try:
        side = json.loads(sb.decode("utf-8"))
        df = pd.read_parquet(str(pq))
        if not isinstance(side, dict):
            raise ValueError("the sidecar is not a JSON object")
    except Exception as e:                  # an unreadable arm halts its row, never the run
        return {"arm": arm, "df": None, "side": {}, "halts": [
            f"ARM-UNREADABLE: {rid}/{arm}: {type(e).__name__}: {e}"], "notes": [], "sha": None,
                "side_sha": sha256_bytes(sb)}
    halts, notes = validate_book(df, side, rid, arm, fees)
    if not any(h.startswith(("REGBOOK-COLS", "REGBOOK-NULL", "REGBOOK-DTYPE")) for h in halts):
        df = df.sort_values(SORT_KEY, kind="mergesort").reset_index(drop=True)
        sha = book_sha256(df)
    else:
        sha = None
    return {"arm": arm, "df": df, "side": side, "halts": halts, "notes": notes, "sha": sha,
            "side_sha": sha256_bytes(sb)}


def load_status(regdir: Path, rid: str) -> tuple[dict | None, list[str], list[str]]:
    p = regdir / "STATUS.json"
    if not p.exists():
        return None, [], []
    try:
        st = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(st, dict):
            raise ValueError("STATUS.json is not a JSON object")
    except Exception as e:
        return {"registration": rid}, [f"STATUS: {rid} STATUS.json unreadable: "
                                       f"{type(e).__name__}: {e}"], []
    halts, notes = [], []
    if st.get("registration") != rid:
        halts.append(f"STATUS: {rid} STATUS.json names {st.get('registration')!r}")
    if st.get("status") not in STATUS_WORDS:
        halts.append(f"STATUS: {rid} status {st.get('status')!r} not in {STATUS_WORDS}")
    if not isinstance(st.get("reason"), str) or not st.get("reason"):
        halts.append(f"STATUS: {rid} reason missing")
    arms = st.get("arms")
    if not isinstance(arms, list):
        halts.append(f"STATUS: {rid} arms {arms!r} is not a list")
        arms = []
    on_disk = sorted(q.stem for q in regdir.glob("*.parquet"))
    for a in on_disk:
        if a not in arms:
            notes.append(f"STATUS: {rid}/{a}.parquet on disk but not listed in STATUS.arms "
                         f"(not read)")
    return st, halts, notes


# ══════════════════════════════════════════════ 3 · THE RULERS
def paired_premise(a: pd.DataFrame, b: pd.DataFrame) -> list[str]:
    """L-1.4: identical key sets on (symbol, entry_ms) and n == len(base)."""
    ka = list(zip(a["symbol"], a["entry_ms"].astype(np.int64)))
    kb = list(zip(b["symbol"], b["entry_ms"].astype(np.int64)))
    sa, sb = set(ka), set(kb)
    out = []
    if len(ka) != len(sa) or len(kb) != len(sb):
        out.append(f"PAIRED-PREMISE: duplicated pairing keys (scored {len(ka) - len(sa)}, base "
                   f"{len(kb) - len(sb)})")
    if sa != sb or len(a) != len(b):
        only_a, only_b = sorted(sa - sb), sorted(sb - sa)
        out.append(f"PAIRED-PREMISE: paired premise failed — n scored {len(a)} vs n base "
                   f"{len(b)}; {len(only_a)} key(s) only in scored {only_a[:2]}, {len(only_b)} "
                   f"only in base {only_b[:2]}")
    return out


def _uses_base(ruler: str) -> bool:
    """L-1.4: only the paired and two-sample rulers read a base; vs zero never does."""
    return ruler != "vs_zero"


def two_sample_premise(a: pd.DataFrame, b: pd.DataFrame) -> dict:
    """SC-6: the key facts of a two-sample row; identical key sets are FLAGGED."""
    ka = set(zip(a["symbol"], a["entry_ms"].astype(np.int64)))
    kb = set(zip(b["symbol"], b["entry_ms"].astype(np.int64)))
    prem = {"key_sets_identical": bool(ka == kb), "n": len(a), "n_base": len(b),
            "n_shared_keys": len(ka & kb), "n_only_scored": len(ka - kb),
            "n_only_base": len(kb - ka)}
    if ka == kb:
        prem["flag"] = ("TWO-SAMPLE-PREMISE: key sets identical — the arm removed nothing; "
                        "the difference is 0 by construction")
    return prem


def _unacted(df: pd.DataFrame) -> np.ndarray:
    v = df["acted_by"]
    return (v.isna() | (v.astype(str).str.strip() == "")).to_numpy(bool)


def identity_findings(a: pd.DataFrame, b: pd.DataFrame, tag: str) -> list[str]:
    """SC-15 / L-1.5: every campaign the paired rule never acts on (acted_by blank)
    carries the base's net_r, exit_close_ms and exit_reason EXACTLY."""
    if "acted_by" not in a.columns:
        return [f"IDENTITY-LAW: {tag} carries no acted_by column — the L-1.5 identity law "
                f"cannot be asserted over the book"]
    un = a.loc[_unacted(a), PAIR_KEY + list(IDENTITY_COLS)]
    m = un.merge(b.loc[:, PAIR_KEY + list(IDENTITY_COLS)], on=PAIR_KEY, how="left",
                 suffixes=("_a", "_b"), indicator=True)
    out = []
    lost = int((m["_merge"] != "both").sum())
    if lost:
        out.append(f"IDENTITY-LAW: {tag} {lost} unacted row(s) have no base campaign")
    m = m[m["_merge"] == "both"]
    bad = {}
    for c in IDENTITY_COLS:
        x, y = m[f"{c}_a"], m[f"{c}_b"]
        if c == "net_r":
            ne = x.to_numpy(float) != y.to_numpy(float)
        elif c == "exit_close_ms":
            ne = x.to_numpy(np.int64) != y.to_numpy(np.int64)
        else:
            ne = x.astype(str).to_numpy() != y.astype(str).to_numpy()
        if int(ne.sum()):
            i = int(np.flatnonzero(ne)[0])
            bad[c] = (int(ne.sum()), f"{m['symbol'].iloc[i]} {int(m['entry_ms'].iloc[i])}")
    if bad:
        out.append(f"IDENTITY-LAW: {tag} unacted rows differ from the base "
                   + "; ".join(f"{c} on {k} row(s) (e.g. {e})" for c, (k, e) in bad.items())
                   + " [L-1.5: exact, 0.000e+00]")
    return out


def identity_summary(a: pd.DataFrame, b: pd.DataFrame) -> dict:
    un = _unacted(a) if "acted_by" in a.columns else np.zeros(len(a), bool)
    return {"acted_by_carried": "acted_by" in a.columns, "unacted": int(un.sum()),
            "acted": int(len(a) - un.sum()), "law": "L-1.5 identity law held (exact) on "
            "every unacted campaign" if "acted_by" in a.columns else "not assertable"}


def gate_findings(a: pd.DataFrame, b: pd.DataFrame, tag: str) -> list[str]:
    """SC-16 / L-1.5: gated = base minus the refused — no new key, every kept row equal to
    the base's on the 16 required columns (exact)."""
    ka = list(zip(a["symbol"], a["entry_ms"].astype(np.int64)))
    kb = set(zip(b["symbol"], b["entry_ms"].astype(np.int64)))
    out = []
    extra = [k for k in ka if k not in kb]
    if extra:
        out.append(f"GATE-POSTFILTER: {tag} holds {len(extra)} campaign(s) absent from the base "
                   f"(e.g. {extra[0]}) — a post-filter removes only")
    m = a.loc[:, list(REQUIRED)].merge(b.loc[:, list(REQUIRED)], on=PAIR_KEY, how="inner",
                                       suffixes=("_a", "_b"))
    bad = {}
    for c in REQUIRED:
        if c in PAIR_KEY:
            continue
        x, y = m[f"{c}_a"], m[f"{c}_b"]
        if c in FLOAT_COLS:
            ne = x.to_numpy(float) != y.to_numpy(float)
        elif c in INT_COLS:
            ne = x.to_numpy(np.int64) != y.to_numpy(np.int64)
        else:
            ne = x.astype(str).to_numpy() != y.astype(str).to_numpy()
        if int(ne.sum()):
            bad[c] = int(ne.sum())
    if bad:
        out.append(f"GATE-POSTFILTER: {tag} kept rows differ from the base on {bad} — a gate "
                   f"keeps each admitted campaign unchanged")
    return out


def paired_deltas(a: pd.DataFrame, b: pd.DataFrame, col: str) -> pd.DataFrame:
    m = a.loc[:, PAIR_KEY + [col]].merge(b.loc[:, PAIR_KEY + [col]], on=PAIR_KEY,
                                         how="inner", suffixes=("_a", "_b"),
                                         validate="one_to_one")
    m = m.sort_values(PAIR_KEY, kind="mergesort").reset_index(drop=True)
    return pd.DataFrame({"symbol": m["symbol"].to_numpy(object),
                         "entry_ms": m["entry_ms"].to_numpy(np.int64),
                         "delta": m[f"{col}_a"].to_numpy(float) - m[f"{col}_b"].to_numpy(float)})


def ci_of(draws: np.ndarray, point) -> dict:
    """T5._ci_from (5th/95th percentile, p = (#<=0 + 1)/(n+1)) plus the exact p and the
    deciding bound [SC-1]."""
    ci = T5._ci_from(draws, point)
    fin = draws[np.isfinite(draws)]
    nf = int(len(fin))
    k = int(np.sum(fin <= 0))
    srt = np.sort(fin)
    kmax = math.floor((nf + 1) * BAR_FRAC) - 1
    return {"point": None if point is None else float(point),
            "lo": ci["lo"], "hi": ci["hi"], "p_one_sided": ci["p_one_sided"],
            "p_num": k + 1 if nf else None, "p_den": nf + 1 if nf else None,
            "n_draws_finite": nf, "n_draws_le_0": k,
            "deciding_rank": kmax + 1 if 0 <= kmax < nf else None,
            "deciding_bound": float(srt[kmax]) if 0 <= kmax < nf else None,
            "pctl_1p111": float(np.percentile(fin, 100.0 * BAR)) if nf else None}


def ruled(ruler: str, a: pd.DataFrame, b: pd.DataFrame | None, col: str, seed: int,
          n_boot: int) -> dict:
    """One ruler, one seed, one column.  The draws are T5's; nothing re-implemented."""
    if ruler == "vs_zero":
        v = a[col].to_numpy(float)
        c = a["symbol"].to_numpy(object)
        n, nb = len(v), None
        if not n:
            return {"n": 0, "n_base": None, "n_clusters": 0, **ci_of(np.array([np.nan]), None)}
        pt = float(np.mean(v))
        draws = T5.cluster_boot(v, c, seed=seed, n_boot=n_boot)
        ncl = len(np.unique(c))
    elif ruler == "two_sample":
        va, ca = a[col].to_numpy(float), a["symbol"].to_numpy(object)
        vb, cb = b[col].to_numpy(float), b["symbol"].to_numpy(object)
        n, nb = len(va), len(vb)
        if not n or not nb:
            return {"n": n, "n_base": nb, "n_clusters": 0, **ci_of(np.array([np.nan]), None)}
        pt = float(np.mean(va)) - float(np.mean(vb))
        draws = T5.cluster_boot_diff(va, ca, vb, cb, seed=seed, n_boot=n_boot)
        ncl = len(np.unique(np.concatenate([ca, cb])))
    elif ruler == "paired":
        d = paired_deltas(a, b, col)
        v, c = d["delta"].to_numpy(float), d["symbol"].to_numpy(object)
        n, nb = len(v), len(b)
        if not n:
            return {"n": 0, "n_base": nb, "n_clusters": 0, **ci_of(np.array([np.nan]), None)}
        pt = float(np.mean(v))
        draws = T5.cluster_boot(v, c, seed=seed, n_boot=n_boot)
        ncl = len(np.unique(c))
    else:
        raise SystemExit(f"HALT: unknown ruler {ruler!r}")
    return {"n": int(n), "n_base": None if nb is None else int(nb), "n_clusters": int(ncl),
            **ci_of(draws, pt)}


def above_half_bar(n: int) -> int:
    return math.ceil((n + 1) / 2)


def loao(ruler: str, a: pd.DataFrame, b: pd.DataFrame | None, col: str, panel,
         seed: int, n_boot: int) -> dict:
    """SC-2: TP.loao_n's law over the DECLARED panel, keyed (symbol, entry_ms)."""
    panel = tuple(panel)
    per = []
    for drop in sorted(panel):
        a2 = a[a["symbol"] != drop]
        b2 = None if b is None else b[b["symbol"] != drop]
        if ruler == "vs_zero":
            few, nn = (len(a2) < 2 or a2["symbol"].nunique() < 2), len(a2)
        elif ruler == "two_sample":
            few, nn = (len(a2) < 2 or len(b2) < 2 or a2["symbol"].nunique() < 2), len(a2)
        else:
            d = paired_deltas(a2, b2, col)
            few, nn = (len(d) < 2 or d["symbol"].nunique() < 2), len(d)
        if few:
            per.append({"dropped": drop, "n": int(nn), "point": None, "ci_lo": None,
                        "ci_hi": None, "excludes_above": False, "excludes_below": False,
                        "note": "too few clusters", **COLLAR})
            continue
        r = ruled(ruler, a2, b2, col, seed, n_boot)
        per.append({"dropped": drop, "n": int(r["n"]), "point": r["point"], "ci_lo": r["lo"],
                    "ci_hi": r["hi"],
                    "excludes_above": bool(r["lo"] is not None and r["lo"] > 0),
                    "excludes_below": bool(r["hi"] is not None and r["hi"] < 0), "note": "",
                    **COLLAR})
    n_ab = sum(1 for p in per if p["excludes_above"])
    n_be = sum(1 for p in per if p["excludes_below"])
    bar = above_half_bar(len(panel))
    zero = sorted(set(panel) - set(a["symbol"]))
    n_ab_x = sum(1 for p in per if p["excludes_above"] and p["dropped"] not in zero)
    return {"panels": len(panel), "above": n_ab, "below": n_be, "bar": bar,
            "line": f"{n_ab}/{len(panel)} above" + (f", {n_be}/{len(panel)} BELOW" if n_be else ""),
            "clears_line": bool(n_ab >= bar), "seed": int(seed),
            "zero_campaign_assets": zero, "above_excl_zero_campaign": int(n_ab_x),
            "per_panel": per}


def d15_of(a: pd.DataFrame, b: pd.DataFrame) -> dict:
    """T5.d15 (pairs on (symbol, entry_ms); tail = top-decile MEAN ratio)."""
    def objs(d):
        return [SimpleNamespace(symbol=s, entry_ms=int(e), net_r=float(r))
                for s, e, r in zip(d["symbol"], d["entry_ms"], d["net_r"])]
    return T5.d15(objs(a), objs(b))


def conc_point(ruler: str, a: pd.DataFrame, b: pd.DataFrame | None):
    """SC-22: the unpaired ruler's point on (a, b) — mean(a) − mean(b) (two-sample) or
    mean(a) (vs zero); None when a book it reads is empty."""
    if not len(a) or (ruler == "two_sample" and (b is None or not len(b))):
        return None
    pt = float(np.mean(a["net_r"].to_numpy(float)))
    if ruler == "two_sample":
        pt -= float(np.mean(b["net_r"].to_numpy(float)))
    return pt


def _drop_key(df: pd.DataFrame, key: tuple) -> pd.DataFrame:
    hit = ((df["symbol"].to_numpy(object) == key[0])
           & (df["entry_ms"].to_numpy(np.int64) == key[1]))
    return df[~hit]


def concentration(ruler: str, a: pd.DataFrame, b: pd.DataFrame | None) -> dict | None:
    """SC-22 [statistics MINOR-3]: beside an UNPAIRED ruler's row (two-sample, vs zero),
    where T5.d15's paired columns say nothing, the scored book's concentration — the top
    trade (largest |net_r|; ties -> the first in (symbol, entry_ms) order) and its share of
    the scored ΣR; the point with it removed from EVERY book holding its (symbol,
    entry_ms) key; the point without its asset and that asset's share of ΣR; per asset
    Δ = scored mean − base mean (two-sample) or the scored mean (vs zero).  Decides
    nothing."""
    if ruler == "paired":
        return None
    kind = ("delta: scored mean - base mean" if ruler == "two_sample" else "scored mean")
    if not len(a):
        return {"ruler": ruler, "top": None, "per_asset_kind": kind, "per_asset": []}
    d = a.sort_values(PAIR_KEY, kind="mergesort").reset_index(drop=True)
    v = d["net_r"].to_numpy(float)
    k = int(np.argmax(np.abs(v)))            # the first maximum in (symbol, entry_ms) order
    key = (str(d["symbol"].iloc[k]), int(d["entry_ms"].iloc[k]))
    tot = float(a["net_r"].sum())
    in_base = bool(b is not None and len(_drop_key(b, key)) != len(b))
    from_base = in_base and CONC_TOP_FROM_EVERY_BOOK
    asset = key[0]
    per = []
    for s in sorted(set(a["symbol"]) | (set(b["symbol"]) if b is not None else set())):
        a_s = a[a["symbol"] == s]
        b_s = None if b is None else b[b["symbol"] == s]
        per.append({"asset": s, "n": int(len(a_s)),
                    "n_base": None if b_s is None else int(len(b_s)),
                    "value": conc_point(ruler, a_s, b_s)})
    return {"ruler": ruler,
            "top": {"symbol": key[0], "entry_ms": key[1],
                    "entry_close_ms": int(d["entry_close_ms"].iloc[k]), "net_r": float(v[k])},
            "sum_net_r": tot,
            "top_share": float(v[k]) / tot if abs(tot) > 1e-12 else None,
            "top_in_base": in_base,
            "top_removed_from": "scored and base" if from_base else "scored",
            "point_without_top": conc_point(ruler, _drop_key(a, key),
                                            _drop_key(b, key) if from_base else b),
            "asset": asset,
            "asset_share": (float(a.loc[a["symbol"] == asset, "net_r"].sum()) / tot
                            if abs(tot) > 1e-12 else None),
            "point_without_asset": conc_point(ruler, a[a["symbol"] != asset],
                                              None if b is None else b[b["symbol"] != asset]),
            "per_asset_kind": kind, "per_asset": per}


def _pct(x) -> str:
    return "n/a" if x is None else f"{100.0 * x:.1f}%"


def conc_text(ruler: str, c: dict | None, detail: bool = False) -> str:
    """SC-22: the §0 D15 cell of an unpaired row (detail=True adds the per-asset n)."""
    head = "D15 n/a (two-sample)" if ruler == "two_sample" else "D15 n/a (vs zero)"
    if not c or c.get("top") is None:
        return head + " · the scored book holds no campaign"
    t = c["top"]

    def per(p):
        x = f"{p['asset']} {_f(p['value'])}"
        if detail:
            x += (f" (n {p['n']} vs {p['n_base']})" if p.get("n_base") is not None
                  else f" (n {p['n']})")
        return x

    return " · ".join([
        head,
        f"top trade {t['symbol']} {TB.iso(t['entry_close_ms'])[:16]}Z {_f(t['net_r'])} R = "
        f"{_pct(c['top_share'])} of the scored ΣR {_f(c['sum_net_r'])}",
        f"point without it {_f(c['point_without_top'])}"
        + (" (removed from both books)" if c["top_removed_from"] == "scored and base" else ""),
        f"point without {c['asset']} {_f(c['point_without_asset'])} ({c['asset']} = "
        f"{_pct(c['asset_share'])} of ΣR)",
        ("per-asset Δ (scored mean − base mean): " if ruler == "two_sample"
         else "per-asset mean: ") + ", ".join(per(p) for p in c["per_asset"])])


def clears_bar(p) -> bool:
    """Clause (b): p <= 0.10/9 — exact on a Fraction [SC-1], float otherwise."""
    if p is None:
        return False
    if isinstance(p, Fraction):
        return p <= BAR_FRAC
    return float(p) <= BAR


def verdict_of_record(lo, hi, p) -> str:
    """L-1.4: SUPPORTED iff (a) lo > 0 AND (b) p <= 0.10/9; else NOT SUPPORTED, with
    '— CI wholly below zero' appended when hi < 0."""
    if lo is not None and lo > 0 and clears_bar(p):
        return "SUPPORTED"
    if hi is not None and hi < 0:
        return "NOT SUPPORTED — CI wholly below zero"
    return "NOT SUPPORTED"


def ci_reading(lo, hi) -> str:
    """SC-9: the Tier-E CI-only reading, no verdict word."""
    if lo is None or hi is None:
        return CI_READINGS[3]
    if lo > 0:
        return CI_READINGS[0]
    if hi < 0:
        return CI_READINGS[2]
    return CI_READINGS[1]


def p_exact(r: dict):
    return Fraction(r["p_num"], r["p_den"]) if r.get("p_num") else None


def stats_block(ruler: str, a: pd.DataFrame, b: pd.DataFrame | None, panel,
                n_boot: int = N_BOOT, with_loao: bool = True) -> dict:
    """The statistics of one arm: seed of record + sensitivity seed, LOAO (both seeds),
    the haircut twin (both seeds), D15.  The same for registered and Tier-E rows."""
    main = ruled(ruler, a, b, "net_r", SEED, n_boot)
    sens = ruled(ruler, a, b, "net_r", SEED_SENS, n_boot)
    hc = ruled(ruler, a, b, "haircut_net_r", SEED, n_boot)
    hcs = ruled(ruler, a, b, "haircut_net_r", SEED_SENS, n_boot)
    out = {"ruler": ruler, "main": main, "sens": sens, "haircut": hc, "haircut_sens": hcs,
           "sum_net_r": float(a["net_r"].sum()), "mean_net_r": (float(a["net_r"].mean())
                                                                if len(a) else None),
           "sum_net_r_base": None if b is None else float(b["net_r"].sum()),
           "mean_net_r_base": (None if b is None or not len(b) else float(b["net_r"].mean())),
           "n_assets": int(a["symbol"].nunique())}
    if with_loao:
        out["loao"] = loao(ruler, a, b, "net_r", panel, SEED, n_boot)
        out["loao_sens"] = loao(ruler, a, b, "net_r", panel, SEED_SENS, n_boot)
    out["d15"] = d15_of(a, b) if (ruler != "vs_zero" and b is not None) else None
    return out


def gate_block(a: pd.DataFrame, b: pd.DataFrame) -> dict:
    """L-1.5 / SC-5: the refused cohort of a post-filter gate."""
    ka = set(zip(a["symbol"], a["entry_ms"].astype(np.int64)))
    kb = set(zip(b["symbol"], b["entry_ms"].astype(np.int64)))
    refm = [(s, int(e)) not in ka for s, e in zip(b["symbol"], b["entry_ms"])]
    ref = b[np.asarray(refm, bool)]
    added = len(ka - kb)
    mean = float(ref["net_r"].mean()) if len(ref) else None
    ssum = float(ref["net_r"].sum()) if len(ref) else 0.0
    return {"refused_n": int(len(ref)), "refused_mean_r": mean, "refused_sum_r": ssum,
            "scored_sum_r": float(a["net_r"].sum()), "base_sum_r": float(b["net_r"].sum()),
            "scored_n": int(len(a)), "base_n": int(len(b)), "added_n": int(added),
            "forfeits": bool(mean is not None and mean > 0),
            "appendix": (f"on per-campaign expectancy only; the gate forfeits +{ssum:.4f} R "
                         f"total" if (mean is not None and mean > 0) else None)}


def adds_block(a: pd.DataFrame, b: pd.DataFrame) -> dict:
    """AM-3: beside the paired Δ (scored on net_r, never asserted == add_r) print Σ add_r
    and the funding the D12 ceiling absorbed (funding_r_uncapped - funding_r; the base's
    own absorption subtracted when it carries the column), and the residual.  Read from
    the regbook's EXTRA columns `add_r` / `funding_r_uncapped` when carried."""
    if "add_r" not in a.columns or "funding_r_uncapped" not in a.columns:
        return {"carried": False, "note": "the scored regbook carries no add_r / "
                                          "funding_r_uncapped column: AM-3's beside-print "
                                          "is not possible from the interface"}
    d = paired_deltas(a, b, "net_r")                      # (symbol, entry_ms) order
    ab = float(np.sum(a["funding_r_uncapped"].to_numpy(float) - a["funding_r"].to_numpy(float)))
    # the v6 leg's own absorption [repair m-8]: the add book's v6_funding_absorbed_r when it
    # carries it (its record of the v6 leg), else the base's uncapped - capped, else none
    if "v6_funding_absorbed_r" in a.columns:
        base_ab, src = float(np.sum(a["v6_funding_absorbed_r"].to_numpy(float))), \
            "scored.v6_funding_absorbed_r"
    elif "funding_r_uncapped" in b.columns:
        base_ab, src = float(np.sum(b["funding_r_uncapped"].to_numpy(float)
                                    - b["funding_r"].to_numpy(float))), \
            "base.funding_r_uncapped - base.funding_r"
    else:
        base_ab, src = None, "none (the base carries no absorption column)"
    absorbed = ab - (base_ab or 0.0)
    sd, sa = float(np.sum(d["delta"].to_numpy(float))), float(np.sum(a["add_r"].to_numpy(float)))
    return {"carried": True, "sum_delta_r": sd, "sum_add_r": sa,
            "sum_absorbed_funding_r": absorbed, "base_absorption_subtracted": base_ab is not None,
            "base_absorption_source": src, "sum_base_absorption_r": base_ab,
            "residual_delta_minus_add_minus_absorbed": sd - sa - absorbed,
            "n_campaigns_with_adds": int((a["add_r"].astype(float) != 0).sum()),
            "note": "AM-3: the paired delta is scored on net_r (tierc7._account_chain); "
                    "delta == add_r is never asserted"}


# ══════════════════════════════════════════════ 4 · F-BASE-IDENT
def v6_frame() -> tuple[pd.DataFrame, dict]:
    v6 = pd.read_parquet(str(V6_CAMPAIGNS))
    man = json.loads(V6_MANIFEST.read_text(encoding="utf-8"))
    csha = TB._content_sha(v6)
    rec = {"path": "research_outputs/tierc11/books/v6_campaigns.parquet", "n": int(len(v6)),
           "content_sha": csha, "manifest_content_sha": man["sha"]["v6_campaigns"],
           "sum_net_r_6dp": float(v6["net_r"].sum())}
    if csha != man["sha"]["v6_campaigns"]:
        raise SystemExit(f"HALT (BASE-V6): books/v6_campaigns.parquet content sha {csha[:16]}… "
                         f"!= its manifest {man['sha']['v6_campaigns'][:16]}…")
    return v6, rec


def v6_findings(rid: str, base: pd.DataFrame, v6: pd.DataFrame) -> list[str]:
    """SC-7: the base arm vs books/v6_campaigns on (symbol, entry_ms), 13 columns, 6 dp."""
    out = []
    kb = list(zip(base["symbol"], base["entry_ms"].astype(np.int64)))
    kv = list(zip(v6["symbol"], v6["entry_ms"].astype(np.int64)))
    if set(kb) != set(kv) or len(kb) != len(kv):
        out.append(f"BASE-V6: {rid}/base keys != books/v6 (n {len(kb)} vs {len(kv)}; only in "
                   f"base {sorted(set(kb) - set(kv))[:2]}, only in v6 "
                   f"{sorted(set(kv) - set(kb))[:2]})")
        return out
    m = base.merge(v6, on=PAIR_KEY, how="inner", suffixes=("_b", "_v"), validate="one_to_one")
    for bc, vc in V6_CMP:
        x = m[f"{bc}_b"] if f"{bc}_b" in m.columns else m[bc]
        y = m[f"{vc}_v"] if f"{vc}_v" in m.columns else m[vc]
        if bc in FLOAT_COLS:
            bad = (x.astype(float).round(V6_DP).to_numpy() != y.astype(float).to_numpy())
        elif bc in INT_COLS:
            bad = (x.astype(np.int64).to_numpy() != y.astype(np.int64).to_numpy())
        else:
            bad = (x.astype(str).to_numpy() != y.astype(str).to_numpy())
        nb = int(np.sum(bad))
        if nb:
            i = int(np.flatnonzero(bad)[0])
            xv, yv = x.iloc[i], y.iloc[i]
            xv = xv.item() if hasattr(xv, "item") else xv
            yv = yv.item() if hasattr(yv, "item") else yv
            out.append(f"BASE-V6: {rid}/base {bc} differs from books/v6 {vc} on {nb} row(s), "
                       f"e.g. {m['symbol'].iloc[i]} {int(m['entry_ms'].iloc[i])}: "
                       f"{xv!r} vs {yv!r}")
    return out


def base_ident(bases: dict, v6: pd.DataFrame) -> dict:
    """F-BASE-IDENT over the base arms present among BASE_IDENT_REGS."""
    findings = []
    shas = {rid: bases[rid]["sha"] for rid in sorted(bases)}
    if len(set(shas.values())) > 1:
        groups: dict = {}
        for rid, s in shas.items():
            groups.setdefault(s, []).append(rid)
        findings.append("BASE-IDENT: the base arms carry "
                        f"{len(groups)} different book_sha256: "
                        + "; ".join(f"{str(s)[:16]}… {g}" for s, g in sorted(
                            groups.items(), key=lambda kv: (-len(kv[1]), str(kv[0])))))
    v6ok = {}
    for rid in sorted(bases):
        f = v6_findings(rid, bases[rid]["df"], v6)
        v6ok[rid] = not f
        findings += f
    good = {bases[rid]["sha"] for rid in bases if v6ok[rid]}
    # SC-7: a row is ruled against its base only if that base equals books/v6 AND carries
    # the one sha the v6-equal bases share; a split among v6-equal bases halts them all
    per_ok = {rid: bool(v6ok[rid] and len(good) == 1 and bases[rid]["sha"] in good)
              for rid in sorted(bases)}
    return {"ok": not findings, "per_registration_ok": per_ok,
            "registrations_checked": sorted(bases),
            "registrations_expected": list(BASE_IDENT_REGS),
            "absent": [r for r in BASE_IDENT_REGS if r not in bases],
            "book_sha256": shas, "findings": findings,
            "law": "every 'base' arm of the seven carries ONE book_sha256 and equals "
                   "books/v6_campaigns.parquet on (symbol, entry_ms) x 13 columns at 6 dp "
                   "[SC-7]"}


# ══════════════════════════════════════ 4b · THE PLAIN-JSON RECORDS BESIDE THE REGBOOKS
def _rel(p) -> str:
    try:
        return str(Path(p).resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return f"<external>/{Path(p).name}"


def _truthy(s: pd.Series) -> np.ndarray:
    if s.dtype == bool:
        return s.to_numpy(bool)
    return s.map(lambda v: (v is True) or (isinstance(v, (int, float, np.integer, np.floating))
                                           and not pd.isna(v) and bool(v))
                 or (isinstance(v, str) and v.strip().lower() in ("true", "1"))).to_numpy(bool)


def load_scale_picks(path=None) -> dict:
    """SC-14: research_outputs/tierc11/ranges/SCALE_PICKS.json — the L-R.2 pick record
    (a plain JSON; no Range object is read)."""
    p = Path(path or SCALE_PICKS_PATH)
    try:
        raw = p.read_bytes()
        d = json.loads(raw.decode("utf-8"))
        cells = {(c["asset"], c["lens"]): {"first_half_pick": c.get("first_half_pick"),
                                           "tuning_pick": c.get("tuning_pick"),
                                           "stable": c.get("stable_first_half_vs_tuning"),
                                           "pick_window": c.get("pick_window")}
                 for c in d["cells"]}
        fb = set()
        for x in d.get("fallback_cells") or []:
            a, lens = str(x).rsplit(" ", 1)
            fb.add((a, lens))
        return {"ok": True, "path": _rel(p), "sha256": sha256_bytes(raw), "cells": cells,
                "fallback": fb}
    except Exception as e:                  # an unreadable record is printed, never invented
        return {"ok": False, "path": _rel(p), "sha256": None, "cells": {}, "fallback": set(),
                "error": f"{type(e).__name__}: {e}"}


def pick_stability(picks: dict, lens: str, df: pd.DataFrame | None) -> dict:
    """SC-14 / L-R.2: per CLASSIC5 asset at `lens`, the pick fit on the first half of the
    tuning era vs the whole tuning era; every change named."""
    if not picks.get("ok"):
        return {"lens": lens, "ok": False, "changed_assets": None, "stable_assets": None,
                "text": f"pick stability ({lens}): NOT PRINTABLE — {picks.get('path')} "
                        f"unreadable ({picks.get('error')})",
                "short": f"pick stability {lens}: NOT PRINTABLE"}
    changed, stable, undetermined = [], [], []
    for s in E.CLASSIC5:
        c = picks["cells"].get((s, lens))
        if c is None or c["stable"] is None:
            undetermined.append(s)
        elif c["stable"] is True:
            stable.append(s)
        else:
            changed.append((s, c["first_half_pick"], c["tuning_pick"]))
    names = [s for s, _, _ in changed]
    n = 0 if df is None else int(len(df))
    k = 0 if df is None else int(df["symbol"].isin(names).sum())
    head = f"pick stability ({lens}, first half of tuning vs tuning, CLASSIC5 [L-R.2]): "
    if changed:
        body = ("CHANGED on " + ", ".join(f"{s} {fh}->{tp}" for s, fh, tp in changed)
                + (f" ({k} of {n} campaigns on a changed asset)" if df is not None else ""))
        short = f"pick stability {lens}: CHANGED on {', '.join(names)} ({k} of {n} campaigns)"
    else:
        body = f"stable on all {len(stable)} CLASSIC5 assets"
        short = f"pick stability {lens}: stable"
    if undetermined:
        body += f"; no first-half pick for {', '.join(undetermined)}"
    return {"lens": lens, "ok": True, "changed_assets": names, "stable_assets": stable,
            "undetermined_assets": undetermined,
            "changed": [{"asset": s, "first_half_pick": fh, "tuning_pick": tp}
                        for s, fh, tp in changed],
            "n_campaigns_on_changed": k, "n_campaigns": n, "text": head + body, "short": short,
            "source": picks["path"], "source_sha256": picks["sha256"]}


def fallback_label(picks: dict, lens: str, df: pd.DataFrame | None) -> str | None:
    """SC-14 / L-R.2 [repair m-13]: an asset whose pick at `lens` fell back to the whole
    tape is labelled IN-SAMPLE everywhere."""
    if df is None or not picks.get("ok"):
        return None
    hit = sorted(s for s in set(df["symbol"]) if (s, lens) in picks["fallback"])
    if not hit:
        return None
    k = int(df["symbol"].isin(hit).sum())
    return (f"IN-SAMPLE everywhere (whole-tape pick fallback [L-R.2]): "
            + ", ".join(f"{s} {lens}" for s in hit) + f" ({k} of {len(df)} campaigns)")


def stability_column_notes(picks: dict, lens: str, df: pd.DataFrame, tag: str) -> list[str]:
    """A regbook's own stability column vs the record, on its CLASSIC5 rows (disclosure)."""
    col = next((c for c in (f"stability_changed_{lens}", "stability_changed")
                if c in df.columns), None)
    if col is None or not picks.get("ok"):
        return []
    c5 = df[df["symbol"].isin(E.CLASSIC5)]
    want = c5["symbol"].map(lambda s: (picks["cells"].get((s, lens)) or {}).get("stable")
                            is False).to_numpy(bool)
    bad = int((_truthy(c5[col]) != want).sum())
    return ([f"SCALE-STABILITY-COLUMN (disclosure): {tag} {col} disagrees with "
             f"{picks['path']} on {bad} CLASSIC5 row(s)"] if bad else [])


def consumes_pick(arm: str, df: pd.DataFrame | None) -> bool:
    """SC-14: a frozen-3.0 arm consumes no calibrated pick."""
    if "frozen" in arm:
        return False
    if df is not None and "scale_kind" in df.columns:
        return bool((df["scale_kind"].astype(str) == "calibrated").any())
    return True


def scale_flags_of(picks: dict, lens: str, arm: str, df: pd.DataFrame | None) -> str:
    """SC-14: the flags a Tier-E row of a SCALE-IN-SAMPLE registration carries."""
    if not consumes_pick(arm, df):
        return "frozen 3.0: no calibrated pick consumed"
    parts = [pick_stability(picks, lens, df)["short"]]
    fl = fallback_label(picks, lens, df)
    if fl:
        parts.append(fl)
    return " · ".join(parts)


def range_read_in_sample(h: pd.DataFrame) -> dict:
    """SC-4 [repair m-11]: holdout-slice campaigns whose own range read fell at an instant
    <= the era cut (in-sample), from the regbook's extra columns."""
    cols, mask = [], np.zeros(len(h), bool)
    for c in h.columns:
        if c == "scale_in_sample" or c.startswith("scale_in_sample_"):
            mask |= _truthy(h[c])
            cols.append(c)
    if "n_adds_scale_in_sample" in h.columns:
        mask |= (h["n_adds_scale_in_sample"].fillna(0).astype(float) > 0).to_numpy(bool)
        cols.append("n_adds_scale_in_sample")
    if "die_close_ms" in h.columns:
        v = h["die_close_ms"]
        mask |= (v.notna() & (v.fillna(0).astype(np.int64) <= E.ERA_CUT_MS)).to_numpy(bool)
        cols.append("die_close_ms<=cut")
    return {"n": int(len(h)), "in_sample": int(mask.sum()) if cols else None, "columns": cols}


def status_word_findings(rid: str, status: str, spec: dict) -> list[str]:
    """SC-17: a closing word only where the spec names its precondition / condition."""
    out = []
    if status == "CLOSED_BY_PRECONDITION" and not spec["precondition"]:
        out.append(f"STATUS-ILLEGAL: {rid} has no precondition in its spec; "
                   f"CLOSED_BY_PRECONDITION is not its word")
    if status == "CONDITION_NOT_MET" and not spec["condition"]:
        out.append(f"STATUS-ILLEGAL: {rid} has no condition in its spec; "
                   f"CONDITION_NOT_MET is not its word")
    return out


def condition_record(regdir: Path, rid: str, status: str) -> tuple[list[str], dict | None]:
    """SC-17 / L-W.4: the condition record agrees with the status word."""
    if rid not in CONDITION_FILE:
        return [], None
    p = Path(regdir) / CONDITION_FILE[rid]
    if not p.exists():
        return [f"CONDITION-RECORD: {rid} STATUS {status} but {CONDITION_FILE[rid]} is absent — "
                f"the L-W.4 condition cannot be checked"], None
    try:
        raw = p.read_bytes()
        c = json.loads(raw.decode("utf-8"))
        if not isinstance(c, dict):
            raise ValueError("not a JSON object")
    except Exception as e:
        return [f"CONDITION-RECORD: {rid} {CONDITION_FILE[rid]} unreadable: "
                f"{type(e).__name__}: {e}"], None
    met, hi = c.get("met"), c.get("ci_hi")
    rec = {"path": f"{rid}/{CONDITION_FILE[rid]}", "sha256": sha256_bytes(raw), "met": met,
           "ci_hi": hi, "delta": c.get("delta")}
    out = []
    if not isinstance(met, bool) or not isinstance(hi, (int, float)) or isinstance(hi, bool):
        out.append(f"CONDITION-RECORD: {rid} met {met!r} / ci_hi {hi!r} is not a (bool, number)")
        return out, rec
    if (hi < 0) != met:
        out.append(f"CONDITION-RECORD: {rid} met {met} but ci_hi {hi} — L-W.4: MET iff the "
                   f"cluster-90% hi < 0")
    if status == "BUILT" and not met:
        out.append(f"CONDITION-RECORD: {rid} STATUS BUILT but the condition record says NOT MET "
                   f"— L-W.4: then report-only, no slot")
    if status == "CONDITION_NOT_MET" and met:
        out.append(f"CONDITION-RECORD: {rid} STATUS CONDITION_NOT_MET but the condition record "
                   f"says MET")
    return out, rec


def load_r2(path=None) -> dict:
    """SC-17: research_outputs/tierc11/stage_r/R2_LENS_VERDICTS.json (plain JSON)."""
    p = Path(path or R2_VERDICTS_PATH)
    try:
        raw = p.read_bytes()
        d = json.loads(raw.decode("utf-8"))
        return {"ok": True, "path": _rel(p), "sha256": sha256_bytes(raw),
                "lenses": dict(d["lenses"])}
    except Exception as e:
        return {"ok": False, "path": _rel(p), "sha256": None, "lenses": {},
                "error": f"{type(e).__name__}: {e}"}


def precondition_record(r2: dict, rid: str, status: str) -> tuple[list[str], dict | None]:
    """SC-17 / L-S.1: P-SCALP-2 is BUILT iff the R2 1h lens verdict of record is PASS."""
    if rid not in PRECONDITION_LENS:
        return [], None
    lens = PRECONDITION_LENS[rid]
    if not r2.get("ok"):
        return [f"PRECONDITION-RECORD: {rid} the R2 record {r2.get('path')} is unreadable "
                f"({r2.get('error')})"], None
    v = (r2["lenses"].get(lens) or {}).get("verdict")
    rec = {"path": r2["path"], "sha256": r2["sha256"], "lens": lens, "word_of_record": v}
    out = []
    if v is None:
        out.append(f"PRECONDITION-RECORD: {rid} the R2 record holds no {lens} lens word")
    elif status == "BUILT" and v != "PASS":
        out.append(f"PRECONDITION-RECORD: {rid} STATUS BUILT but the R2 {lens} lens word of "
                   f"record is {v!r} — L-S.1: Stage S runs only on PASS")
    elif status == "CLOSED_BY_PRECONDITION" and v == "PASS":
        out.append(f"PRECONDITION-RECORD: {rid} STATUS CLOSED_BY_PRECONDITION but the R2 {lens} "
                   f"lens word of record is PASS")
    return out, rec


def r2_beside(r2: dict, rid: str) -> dict | None:
    """§10: P-SCALP-2's §0 row prints the tuning-era R2 word beside it, as Tier-E."""
    if rid not in PRECONDITION_LENS or not r2.get("ok"):
        return None
    lens = PRECONDITION_LENS[rid]
    L = r2["lenses"].get(lens) or {}
    tw, hw = L.get("tier_e_tuning_word"), L.get("verdict")
    return {"lens": lens, "tuning_word": tw, "holdout_word_of_record": hw,
            "source": r2["path"], "source_sha256": r2["sha256"], **COLLAR,
            "text": (f"beside, Tier-E [§10] (tier {COLLAR['tier']} · "
                     f"{COLLAR['selection_not_a_result']} · gates {COLLAR['gates']}): the "
                     f"tuning-era R2 {lens} word {tw} (holdout word of record {hw})")}


# ══════════════════════════════════════════════ 5 · ROWS
def _brief(r: dict | None) -> dict | None:
    if r is None:
        return None
    return {"n": r["n"], "n_base": r.get("n_base"), "point": r["point"], "ci_lo": r["lo"],
            "ci_hi": r["hi"], "p_one_sided": r["p_one_sided"]}


def tier_e_row(rid: str, arm: str, ruler: str, era_scope: str, panel_name: str,
               st: dict | None, note: str, book_sha: str | None, halt: str | None = None,
               scale_flags: str | None = None) -> dict:
    """A collared Tier-E row: the statistics, would_read_ci_only, NO verdict word."""
    row = {"registration": rid, "arm": arm, "ruler": ruler, "era_scope": era_scope,
           "panel": panel_name, "note": note, "book_sha256": book_sha,
           "scale_flags": scale_flags, **COLLAR}
    if halt is not None or st is None:
        row.update({"halted": halt or "no statistics", "n": None, "point": None, "ci_lo": None,
                    "ci_hi": None, "p_one_sided": None, "would_read_ci_only": CI_READINGS[3]})
        return row
    m = st["main"]
    row.update({
        "halted": None, "n": m["n"], "n_base": m.get("n_base"), "point": m["point"],
        "ci_lo": m["lo"], "ci_hi": m["hi"], "p_one_sided": m["p_one_sided"],
        "would_read_ci_only": ci_reading(m["lo"], m["hi"]),
        "sens": _brief(st["sens"]), "haircut": _brief(st["haircut"]),
        "haircut_sens": _brief(st["haircut_sens"]),
        "sum_net_r": st["sum_net_r"], "mean_net_r": st["mean_net_r"],
        "loao_line": st["loao"]["line"] if st.get("loao") else None,
        "loao_bar": st["loao"]["bar"] if st.get("loao") else None,
        "loao_line_sens": st["loao_sens"]["line"] if st.get("loao_sens") else None,
        "d15": st["d15"]})
    return row


def collar_findings(rows: list[dict]) -> list[str]:
    """Every Tier-E row carries the collar exactly and NO verdict word [F-COLLAR]."""
    out = []

    def walk(x, path):
        if isinstance(x, dict):
            for k, v in x.items():
                if FORBIDDEN_TIER_E_KEY_RX.search(str(k)):
                    out.append(f"COLLAR-VERDICT-WORD: {path}.{k} is a verdict field")
                walk(v, f"{path}.{k}")
        elif isinstance(x, (list, tuple)):
            for i, v in enumerate(x):
                walk(v, f"{path}[{i}]")
        elif isinstance(x, str) and VERDICT_WORD_RX.search(x):
            out.append(f"COLLAR-VERDICT-WORD: {path} = {x[:80]!r}")

    for r in rows:
        tag = f"{r.get('registration')}/{r.get('arm')}"
        for k, v in COLLAR.items():
            if k not in r:
                out.append(f"COLLAR-MISSING: {tag} lacks {k}")
            elif r[k] != v:
                out.append(f"COLLAR-VALUE: {tag} {k} {r[k]!r} != {v!r}")
        if r.get("would_read_ci_only") not in CI_READINGS:
            out.append(f"COLLAR-VALUE: {tag} would_read_ci_only {r.get('would_read_ci_only')!r}")
        walk(r, tag)
    return out


def _slug_pick(tier_e: dict, exact: str, sub: str) -> str | None:
    """A FILED Tier-E arm (tierE__ only — never a scorer-derived slice): the exact slug
    first, else the first sorted slug containing `sub` [SC-4]."""
    if exact in tier_e:
        return exact
    c = sorted(a for a in tier_e if a.startswith("tierE__") and sub in a[len("tierE__"):])
    return c[0] if c else None


def _stat_line(r: dict | None) -> str:
    if r is None or r.get("point") is None:
        return "no statistic"
    return (f"n {r['n']}, {_f(r['point'])} [{_f(r['lo'])}, {_f(r['hi'])}] "
            f"p {_p(r['p_one_sided'])}")


def _f(x, nd: int = 4) -> str:
    if x is None:
        return "—"
    return f"{x:+.{nd}f}"


def _p(x) -> str:
    return "—" if x is None else f"{x:.6f}"


def _restrict(df: pd.DataFrame | None, scope: str) -> pd.DataFrame | None:
    if df is None or scope == "full":
        return df
    return df[df["era"] == scope].reset_index(drop=True)


class Loader:
    """Loads each (registration, arm) once; resolves a Tier-E base_arm across
    registrations [SC-3]."""

    def __init__(self, root: Path, fees: dict):
        self.root, self.fees, self.cache, self.status = root, fees, {}, {}
        self._picks, self._r2 = None, None

    def picks(self) -> dict:
        """SCALE_PICKS.json, read once at the path bound NOW (SC-14)."""
        if self._picks is None:
            self._picks = load_scale_picks(SCALE_PICKS_PATH)
        return self._picks

    def r2(self) -> dict:
        """R2_LENS_VERDICTS.json, read once at the path bound NOW (SC-17)."""
        if self._r2 is None:
            self._r2 = load_r2(R2_VERDICTS_PATH)
        return self._r2

    def status_of(self, rid: str):
        if rid not in self.status:
            d = self.root / rid
            self.status[rid] = load_status(d, rid) if d.is_dir() else (None, [], [])
        return self.status[rid]

    def arm(self, rid: str, arm: str) -> dict:
        if (rid, arm) not in self.cache:
            self.cache[(rid, arm)] = load_arm(self.root / rid, rid, arm, self.fees)
        return self.cache[(rid, arm)]


def _arms_of(st: dict | None) -> list[str]:
    arms = list((st or {}).get("arms") or [])
    return sorted(set(arms), key=lambda a: (0 if a == "scored" else 1 if a == "base" else 2, a))


def score_tier_e(L: Loader, rid: str, arm: str, spec: dict, base_df, note: str,
                 halt_base: str | None, n_boot: int) -> dict:
    A = L.arm(rid, arm)
    side = A["side"]
    lens = SCALE_LENS_OF.get(rid) if spec.get("scale_in_sample") else None
    flags = (scale_flags_of(L.picks(), lens, arm, A["df"])
             if lens and A["df"] is not None and not any(
                 h.startswith(("REGBOOK-COLS", "REGBOOK-NULL", "REGBOOK-DTYPE"))
                 for h in A["halts"]) else None)
    disc = (stability_column_notes(L.picks(), lens, A["df"], f"{rid}/{arm}")
            if flags and consumes_pick(arm, A["df"]) else [])

    def row(st, n=note, halt=None, ruler=None, scope=None):
        r = tier_e_row(rid, arm, ruler or side.get("ruler", "?"),
                       scope or side.get("era_scope", "?"), _panel_name(side.get("panel")), st,
                       n, A["sha"], halt=halt, scale_flags=flags)
        r["disclosures"] = disc
        return r

    if A["halts"]:
        return row(None, halt=" | ".join(A["halts"]))
    ruler = side["ruler"]
    scope = side["era_scope"]
    b = None
    if _uses_base(ruler):
        ba = side.get("base_arm")
        if ba:
            brid, barm = (ba.split("/", 1) if "/" in ba else (rid, ba))
            B = L.arm(brid, barm)
            if B["halts"] or B["df"] is None:
                return row(None, halt=f"BASE-ARM: {ba} unusable: " + " | ".join(B["halts"]))
            b = _restrict(B["df"], scope)
            note = (note + f"; ruled against base_arm {ba}").lstrip("; ")
        else:
            if halt_base is not None or base_df is None:
                return row(None, halt=halt_base or "BASE-ABSENT: no base arm")
            b = _restrict(base_df, scope)
        if ruler == "paired":
            pp = paired_premise(A["df"], b)
            if not pp and not ba:           # SC-15: the identity law vs its own base
                pp = identity_findings(A["df"], b, f"{rid}/{arm}")
            if pp:
                return row(None, n=note, halt=" | ".join(pp))
    st = stats_block(ruler, A["df"], b, side["panel"], n_boot=n_boot)
    return row(st, n=note)


def _panel_name(panel) -> str:
    if not isinstance(panel, list):
        return str(panel)
    if tuple(sorted(panel)) == tuple(sorted(E.CLASSIC5)):
        return "CLASSIC5"
    if tuple(sorted(panel)) == tuple(sorted(E.PANEL17)):
        return "PANEL17"
    return ",".join(panel)


def score_registration(L: Loader, reg: dict, ident: dict, n_boot: int = N_BOOT) -> dict:
    spec = spec_of(reg)
    rid = spec["registration"]
    row = {"seq": spec["seq"], "registration": rid, "prior_pct": spec["prior_pct"],
           "kind": spec["kind"], "panel_name": spec["panel_name"], "panel": list(spec["panel"]),
           "era": spec["era"], "ruler": spec["ruler"], "scored_arm": "scored",
           "payload_sha256": spec["payload_sha256"], "text_of_record": spec["text_of_record"],
           "labels": spec["labels"], "hazard": hazard_of(spec),
           "scale_in_sample_flag": spec["scale_in_sample"], "named_risk": spec["named_risk"],
           "status": None, "status_reason": None, "verdict_of_record": None,
           "verdict_cell": None, "spent_test": False, "clears_bar": None, "stats": None,
           "gate": None, "adds": None, "scale_beside": None, "premise": None, "tier_e": [],
           "r2_beside": None, "condition_record": None, "precondition_record": None,
           "pre_seen_new_campaigns": None, "concentration": None,
           "provenance": {}, "halts": [], "notes": []}
    st, sh, sn = L.status_of(rid)
    row["notes"] += sn
    r2b = r2_beside(L.r2(), rid)            # §10: P-SCALP-2's tuning-era R2 word, collared
    row["r2_beside"] = r2b
    if st is None:
        row.update(status="ABSENT", verdict_of_record="ABSENT",
                   verdict_cell="ABSENT — no STATUS.json under the regbooks root (stage not "
                                "built) — no number, no slot spent"
                                + (f" · {r2b['text']}" if r2b else ""))
        return row
    row["status"], row["status_reason"] = st.get("status"), st.get("reason")
    arms = _arms_of(st)
    row["arms_listed"] = arms
    if sh:
        return _halt(row, sh)
    status = st["status"]
    # SC-17: the status word against the spec and against its gating record
    rh = status_word_findings(rid, status, spec)
    ch, row["condition_record"] = condition_record(L.root / rid, rid, status)
    ph, row["precondition_record"] = precondition_record(L.r2(), rid, status)
    if rh or ch or ph:
        return _halt(row, rh + ch + ph)
    uses_base = _uses_base(spec["ruler"])
    base_df, halt_base = None, None
    if "base" in arms:
        B = L.arm(rid, "base")
        row["provenance"]["base"] = _prov(B)
        row["notes"] += B["notes"]
        if B["halts"]:
            halt_base = " | ".join(B["halts"])
        elif rid in BASE_IDENT_REGS and not ident["per_registration_ok"].get(rid, False):
            halt_base = "F-BASE-IDENT: " + " | ".join(ident["findings"])
        else:
            base_df = B["df"]
    tier_arms = [a for a in arms if a.startswith("tierE__")]
    lens = SCALE_LENS_OF.get(rid) if spec["scale_in_sample"] else None
    # ── closed rows: the reason, no number, no slot spent; arms print as Tier-E
    if status in ("CLOSED_BY_PRECONDITION", "CONDITION_NOT_MET"):
        word = ("CLOSED BY PRECONDITION" if status == "CLOSED_BY_PRECONDITION"
                else "CONDITION NOT MET")
        row.update(verdict_of_record=status,
                   verdict_cell=(f"{word} ({builder_status(st['reason'])}) — report-only · no "
                                 f"number · no slot spent" + (f" · {r2b['text']}" if r2b else "")))
        if "scored" in arms:
            note = (f"the {'rule book' if status == 'CONDITION_NOT_MET' else 'scored arm'} of a "
                    f"{word} registration, printed only as a collared Tier-E row")
            row["tier_e"].append(score_tier_e(L, rid, "scored", spec, base_df, note, halt_base,
                                              n_boot))
        for x in tier_arms:
            row["tier_e"].append(score_tier_e(L, rid, x, spec, base_df, "", halt_base, n_boot))
        _collect_disclosures(row)
        return row
    # ── BUILT
    if "scored" not in arms:
        return _halt(row, [f"ARM-ABSENT: {rid} is BUILT but STATUS lists no scored arm"])
    A = L.arm(rid, "scored")
    row["provenance"]["scored"] = _prov(A)
    row["notes"] += A["notes"]
    halts = list(A["halts"])
    if not halts:
        side = A["side"]
        if side.get("ruler") != spec["ruler"]:
            halts.append(f"SPEC-MISMATCH: {rid}/scored sidecar ruler {side.get('ruler')!r} != the "
                         f"spec's {spec['ruler']!r}")
        if side.get("era_scope") != spec["era"]:
            halts.append(f"SPEC-MISMATCH: {rid}/scored era_scope {side.get('era_scope')!r} != the "
                         f"spec's {spec['era']!r}")
        if sorted(side.get("panel") or []) != sorted(spec["panel"]):
            halts.append(f"SPEC-MISMATCH: {rid}/scored panel {side.get('panel')} != the spec's "
                         f"{spec['panel_name']}")
    if uses_base:
        if "base" not in arms:
            halts.append(f"BASE-ABSENT: {rid} is ruled {spec['ruler']} but STATUS lists no base")
        elif halt_base:
            halts.append(halt_base)
    else:
        if "base" in arms:
            row["notes"].append(f"VS-ZERO: {rid} carries a base arm; the vs-zero ruler IGNORES it")
    if halts:
        return _halt(row, halts)
    a = A["df"]
    b = base_df if uses_base else None
    if uses_base:
        stray = sorted(set(b["symbol"]) - set(spec["panel"]))
        if stray:
            return _halt(row, [f"STRAY-ASSET: {rid}/base holds {stray} outside "
                               f"{spec['panel_name']}"])
    prem = {"ruler": spec["ruler"]}
    if spec["ruler"] == "paired":
        pp = paired_premise(a, b)
        if not pp:                          # SC-15: asserted over the whole book first
            pp = identity_findings(a, b, f"{rid}/scored")
        if pp:
            return _halt(row, pp)
        prem.update(key_sets_identical=True, n=len(a), n_base=len(b),
                    identity=identity_summary(a, b))
    elif spec["ruler"] == "two_sample":
        prem.update(two_sample_premise(a, b))
    if spec["gate"]:                        # SC-16: a gate is a post-filter
        gh = gate_findings(a, b, f"{rid}/scored")
        if gh:
            return _halt(row, gh)
    if lens:
        row["notes"] += stability_column_notes(L.picks(), lens, a, f"{rid}/scored")
    row["premise"] = prem
    stt = stats_block(spec["ruler"], a, b, spec["panel"], n_boot=n_boot)
    row["stats"] = stt
    m = stt["main"]
    pe = p_exact(m)
    verdict = verdict_of_record(m["lo"], m["hi"], pe)
    row["verdict_of_record"] = verdict
    row["clears_bar"] = clears_bar(pe)
    row["clears_bar_float"] = bool(m["p_one_sided"] is not None and m["p_one_sided"] <= BAR)
    row["spent_test"] = True
    row["verdict_at_sens_seed"] = verdict_of_record(stt["sens"]["lo"], stt["sens"]["hi"],
                                                    p_exact(stt["sens"]))
    row["verdict_stable_across_seeds"] = row["verdict_at_sens_seed"] == verdict
    cell = verdict
    if row["hazard"]:
        facts = None
        if "pre_seen" in spec["labels"]:     # SC-21: what the re-score adds, from the books
            facts = preseen_facts(a, b)
            row["pre_seen_new_campaigns"] = {k: facts[k] for k in ("since", "time_col",
                                                                   "scored", "base")}
        cell += f" — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY ({label_of(spec, facts)})"
    row["concentration"] = concentration(spec["ruler"], a, b)   # SC-22 (None when paired)
    if spec["gate"]:
        g = gate_block(a, b)
        row["gate"] = g
        if g["appendix"]:
            cell += f"; {g['appendix']}"
    if prem.get("flag"):
        cell += f" · FLAG: {prem['flag']}"
    if str(spec["kind"]).startswith("add rule"):
        row["adds"] = adds_block(a, b)
    row["verdict_cell"] = cell
    # slices (L-1.3), Tier-E
    if spec["era"] == "full":
        for sc in ("tuning", "holdout"):
            a2, b2 = _restrict(a, sc), _restrict(b, sc)
            fl = scale_flags_of(L.picks(), lens, "scored", a2) if lens else None
            if not len(a2):
                row["tier_e"].append(tier_e_row(rid, f"derived__slice_{sc}", spec["ruler"], sc,
                                                spec["panel_name"], None,
                                                f"the scored arm's {sc} slice [L-1.3]", None,
                                                halt="no campaigns in the slice",
                                                scale_flags=fl))
                continue
            if spec["ruler"] == "paired" and paired_premise(a2, b2):
                row["tier_e"].append(tier_e_row(rid, f"derived__slice_{sc}", spec["ruler"], sc,
                                                spec["panel_name"], None, "", None,
                                                halt=" | ".join(paired_premise(a2, b2)),
                                                scale_flags=fl))
                continue
            sts = stats_block(spec["ruler"], a2, b2, spec["panel"], n_boot=n_boot)
            row["tier_e"].append(tier_e_row(rid, f"derived__slice_{sc}", spec["ruler"], sc,
                                            spec["panel_name"], sts,
                                            f"the scored arm's {sc} slice (era by the entry "
                                            f"bar's close) [L-1.3]", book_sha256(a2),
                                            scale_flags=fl))
    for x in tier_arms:
        row["tier_e"].append(score_tier_e(L, rid, x, spec, base_df, "", halt_base, n_boot))
    if rid in HEAD_TO_HEAD:                 # SC-18: derived only when none is filed
        other = HEAD_TO_HEAD[rid]
        filed = [x for x in tier_arms
                 if str(L.arm(rid, x)["side"].get("base_arm") or "") == f"{other}/scored"]
        if not filed:
            row["tier_e"].append(derived_head_to_head(L, rid, other, spec, a, lens, n_boot))
    if spec["scale_in_sample"]:
        row["scale_beside"] = scale_beside(row, spec, a, b, n_boot, L.picks(), lens)
        row["verdict_cell"] += " · " + row["scale_beside"]["cell"]
        if row["scale_beside"]["frozen_arm"] is None:
            row["notes"].append(f"SCALE-TWIN-ABSENT: {rid} carries SCALE-IN-SAMPLE but no "
                                f"tierE__*frozen* arm was filed")
    _collect_disclosures(row)
    return row


def _collect_disclosures(row: dict) -> None:
    for t in row["tier_e"]:
        row["notes"] += list(t.get("disclosures") or [])


def derived_head_to_head(L: Loader, rid: str, other: str, spec: dict, a: pd.DataFrame,
                         lens: str | None, n_boot: int) -> dict:
    """SC-18: this registration's scored book vs the other add rule's scored book, paired
    on (symbol, entry_ms) — a collared Tier-E row, deciding nothing."""
    arm = f"derived__head_to_head_vs_{other.lower().replace('-', '_')}"
    note = (f"SC-18 derived head-to-head (a spec Tier-E arm no stage filed): {rid}/scored "
            f"ruled paired on (symbol, entry_ms) against {other}/scored; neither is promoted "
            f"by the other's failure")
    fl = scale_flags_of(L.picks(), lens, "scored", a) if lens else None
    so, sh, _ = L.status_of(other)
    if so is None or sh or so.get("status") != "BUILT" or "scored" not in (so.get("arms") or []):
        return tier_e_row(rid, arm, "paired", "full", spec["panel_name"], None, note, None,
                          halt=f"HEAD-TO-HEAD: {other} has no BUILT scored arm", scale_flags=fl)
    B = L.arm(other, "scored")
    if B["halts"] or B["df"] is None:
        return tier_e_row(rid, arm, "paired", "full", spec["panel_name"], None, note, None,
                          halt=f"HEAD-TO-HEAD: {other}/scored unusable: " + " | ".join(B["halts"]),
                          scale_flags=fl)
    pp = paired_premise(a, B["df"])
    if pp:
        return tier_e_row(rid, arm, "paired", "full", spec["panel_name"], None, note, None,
                          halt=" | ".join(pp), scale_flags=fl)
    st = stats_block("paired", a, B["df"], spec["panel"], n_boot=n_boot)
    return tier_e_row(rid, arm, "paired", "full", spec["panel_name"], st, note, book_sha256(a),
                      scale_flags=fl)


def scale_beside(row: dict, spec: dict, a: pd.DataFrame, b: pd.DataFrame | None,
                 n_boot: int, picks: dict, lens: str) -> dict:
    """SC-4 / SC-14 / L-R.2: beside a SCALE-IN-SAMPLE verdict — the holdout-slice
    statistic (derived from the scored arm; a filed tierE 'holdout*' arm beside it), the
    count of its campaigns with an in-sample range read, the frozen-3.0 twin (the filed
    tierE '*frozen*' arm, or ABSENT), the pick stability at the lens the row consumes,
    and the whole-tape fallback label."""
    era = SCALE_CAUSAL_ERA
    ah = a[a["era"] == era].reset_index(drop=True)
    bh = None if b is None else b[b["era"] == era].reset_index(drop=True)
    hs = ruled(spec["ruler"], ah, bh, "net_r", SEED, n_boot) if len(ah) else None
    ins = range_read_in_sample(ah)
    te = {r["arm"]: r for r in row["tier_e"]}
    h_arm = _slug_pick(te, "tierE__holdout_slice", "holdout")
    f_arm = _slug_pick(te, "tierE__frozen_3_0_twin", "frozen")
    h_stat = _brief_te(te.get(h_arm)) if h_arm else None
    f_stat = _brief_te(te.get(f_arm)) if f_arm else None
    ps = pick_stability(picks, lens, a)
    fl = fallback_label(picks, lens, a)
    parts = [f"holdout slice, derived: {_stat_line(hs)}",
             (f"{ins['in_sample']} of {ins['n']} of its campaigns carry a range read <= the era "
              f"cut (in-sample; {', '.join(ins['columns'])})" if ins["in_sample"] is not None
              else "in-sample range reads in the holdout slice: not determinable from the "
                   "regbook")]
    if h_arm:
        parts.append(f"filed {h_arm}: {_stat_line_te(h_stat)}")
    parts.append(f"frozen-3.0 twin {f_arm}: {_stat_line_te(f_stat)}" if f_arm else
                 "frozen-3.0 twin: ABSENT — no tierE__*frozen* arm filed")
    parts.append(ps["text"])
    if fl:
        parts.append(fl)
    cell = "SCALE-IN-SAMPLE (" + "; ".join(parts) + ")"
    return {"causal_era": era, "holdout_slice_derived": hs, "holdout_in_sample": ins,
            "holdout_arm": h_arm, "holdout_arm_stat": h_stat, "frozen_arm": f_arm,
            "frozen_arm_stat": f_stat, "lens": lens, "pick_stability": ps,
            "fallback_label": fl, "cell": cell}


def _brief_te(r: dict | None) -> dict | None:
    if r is None:
        return None
    return {"n": r.get("n"), "point": r.get("point"), "ci_lo": r.get("ci_lo"),
            "ci_hi": r.get("ci_hi"), "p_one_sided": r.get("p_one_sided"),
            "halted": r.get("halted")}


def _stat_line_te(r: dict | None) -> str:
    if r is None or r.get("point") is None:
        return "no statistic" + (f" ({r['halted']})" if r and r.get("halted") else "")
    return (f"n {r['n']}, {_f(r['point'])} [{_f(r['ci_lo'])}, {_f(r['ci_hi'])}] "
            f"p {_p(r['p_one_sided'])}")


def _prov(A: dict) -> dict:
    s = A["side"]
    df = A["df"]
    ok = df is not None and not A["halts"]
    return {"book_sha256": A["sha"], "sidecar_sha256": A["side_sha"], "n": s.get("n"),
            "sum_net_r": s.get("sum_net_r"), "era_scope": s.get("era_scope"),
            "ruler": s.get("ruler"), "panel": s.get("panel"),
            "source_script": s.get("source_script"), "description": s.get("description"),
            # L-1.3: an entry bar straddling the era cut is printed as a count
            "entry_bars_straddling_era_cut": (int(((df["entry_ms"] <= E.ERA_CUT_MS)
                                                   & (df["entry_close_ms"] > E.ERA_CUT_MS)).sum())
                                              if ok else None),
            # P-AGE-1 pre_seen: "campaigns entered after 2026-09-21T16:00Z (listed by count)"
            "entered_after_tc10_pin": new_since_pin(df) if ok else None,
            "halts": A["halts"]}


def _halt(row: dict, halts: list[str]) -> dict:
    row["halts"] = list(halts)
    te = [a for a in row.get("arms_listed") or [] if a.startswith("tierE__")]
    if te:
        row["notes"].append(f"TIER-E-NOT-SCORED: {row['registration']} HALTed; its Tier-E arms "
                            f"{te} were not ruled")
    row["status"] = "HALT" if row.get("status") in (None, "BUILT") else row["status"]
    row.update(verdict_of_record="HALT", spent_test=False, clears_bar=None,
               verdict_cell=("HALT — " + " | ".join(halts) + " — no number, no verdict, no "
                             "slot spent"))
    if any(h.startswith("PAIRED-PREMISE") for h in halts):
        row["verdict_cell"] = ("HALT — paired premise failed — " + " | ".join(halts)
                               + " — no number, no verdict, no slot spent")
    if row.get("r2_beside"):
        row["verdict_cell"] += f" · {row['r2_beside']['text']}"
    return row


# ══════════════════════════════════════════════ 6 · THE FAMILY
def family(rows: list[dict]) -> dict:
    fr = []
    for r in rows:
        fr.append({"seq": r["seq"], "registration": r["registration"], "status": r["status"],
                   "verdict_of_record": r["verdict_of_record"], "spent_test": r["spent_test"],
                   "p_one_sided": (r["stats"]["main"]["p_one_sided"] if r["stats"] else None),
                   "clears_bar": r["clears_bar"],
                   "honesty_label": (("IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (" + r["hazard"] + ")")
                                     if r["hazard"] and r["spent_test"] else None)})
    return {"family_m": FAMILY_M, "family_q": FAMILY_Q, "bar": BAR, "bar_filed": BAR_FILED,
            "bar_exact": "1/90", "tests_spent": sum(1 for r in fr if r["spent_test"]),
            "supported": [r["registration"] for r in fr
                          if r["verdict_of_record"] == "SUPPORTED"],
            "rows": fr,
            "law": ("m = 9 in every case; bar = 0.10/9 fixed, no ranks, no step-up; a "
                    "registration closed by its own precondition or condition spends no test "
                    "and never loosens the bar; a HALTed or ABSENT row spends no test "
                    "[L-1.4]")}


# ══════════════════════════════════════════════ 7 · RENDERING
def _js(x):
    if isinstance(x, dict):
        return {str(k): _js(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_js(v) for v in x]
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating,)):
        return None if not np.isfinite(x) else float(x)
    if isinstance(x, float):
        return None if not math.isfinite(x) else x
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, Fraction):
        return f"{x.numerator}/{x.denominator}"
    return x


def jbytes(obj) -> bytes:
    return (json.dumps(_js(obj), indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def _root_label(root: Path) -> str:
    try:
        return str(Path(root).resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return f"<external>/{Path(root).name}"


def s0_line(r: dict) -> list[str]:
    head = (f"{r['seq']} · {r['registration']} · {r['prior_pct']}% · scored ({r['kind']}) · "
            f"{r['panel_name']} · {r['era']} · {r['ruler']}")
    s = r.get("stats")
    if not s:
        return [head, "—", "—", "—", r["verdict_cell"], "—", "—", "—", "—"]
    m, lo = s["main"], s.get("loao")
    ncell = f"{m['n']}" + (f" (base {m['n_base']})" if m.get("n_base") is not None else "")
    g = r.get("gate")
    if g:
        ncell += (f"; refused n {g['refused_n']}, mean {_f(g['refused_mean_r'])}, ΣR "
                  f"{_f(g['refused_sum_r'])}; ΣR scored {_f(g['scored_sum_r'])} vs base "
                  f"{_f(g['base_sum_r'])}")
    ad = r.get("adds")
    if ad:
        ncell += (f"; ΣΔ {_f(ad['sum_delta_r'])}, Σ add_r {_f(ad['sum_add_r'])}, absorbed "
                  f"funding {_f(ad['sum_absorbed_funding_r'])} (AM-3)" if ad["carried"]
                  else "; add_r not carried (AM-3)")
    ci = f"[{_f(m['lo'])}, {_f(m['hi'])}]"
    pc = f"{_p(m['p_one_sided'])} · clears bar: {'yes' if r['clears_bar'] else 'no'}"
    lc = (f"{lo['line']} (bar {lo['bar']}/{lo['panels']}; "
          f"{'clears' if lo['clears_line'] else 'short'}) · sens {s['loao_sens']['line']}")
    h = s["haircut"]
    hc = f"{_f(h['point'])} [{_f(h['lo'])}, {_f(h['hi'])}] p {_p(h['p_one_sided'])}"
    return [head, ncell, _f(m["point"]), ci, r["verdict_cell"], pc, lc, hc, d15_cell(r)]


def d15_cell(r: dict) -> str:
    """The §0 D15 column: T5.d15 on a PAIRED row; on an unpaired row 'D15 n/a (…)' and the
    scored book's concentration [SC-22]; the named risk beside either."""
    if r["ruler"] == "paired":
        d = (r.get("stats") or {}).get("d15")
        dc = ("—" if d is None else
              f"tail {d.get('tail_exit_ratio')} · paired n {d.get('n_paired')} · max Δ share "
              f"{d.get('max_single_trade_delta_share')}")
    else:
        dc = conc_text(r["ruler"], r.get("concentration"))
    if r.get("named_risk"):
        dc += f" · named risk: {r['named_risk']}"
    return dc


def _md_table(header: list[str], rows: list[list[str]]) -> list[str]:
    def esc(x):
        return str(x).replace("|", "\\|").replace("\n", " ")
    out = ["| " + " | ".join(esc(h) for h in header) + " |",
           "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(esc(c) for c in r) + " |" for r in rows]
    return out


S0_HEADER = ["# · registration · prior · scored arm · panel · era · ruler", "n", "point",
             "90% CI", "verdict under its own text (with labels)", "p · clears bar", "LOAO",
             "haircut twin", "D15"]
TE_HEADER = ["registration", "arm", "ruler", "era_scope", "panel", "n", "point", "90% CI",
             "p", "would_read_ci_only", "LOAO", "haircut twin", "scale (L-R.2)", "tier",
             "selection_not_a_result", "gates"]


def te_line(t: dict) -> list[str]:
    if t.get("halted"):
        return [t["registration"], t["arm"], t["ruler"], t["era_scope"], t["panel"], "—", "—",
                "—", "—", f"{t['would_read_ci_only']} — halted: {t['halted']}", "—", "—",
                t.get("scale_flags") or "—", t["tier"], t["selection_not_a_result"], t["gates"]]
    h = t.get("haircut") or {}
    return [t["registration"], t["arm"], t["ruler"], t["era_scope"], t["panel"],
            str(t["n"]) + (f" (base {t['n_base']})" if t.get("n_base") is not None else ""),
            _f(t["point"]), f"[{_f(t['ci_lo'])}, {_f(t['ci_hi'])}]", _p(t["p_one_sided"]),
            t["would_read_ci_only"], f"{t.get('loao_line')} (bar {t.get('loao_bar')})",
            f"{_f(h.get('point'))} [{_f(h.get('ci_lo'))}, {_f(h.get('ci_hi'))}]",
            t.get("scale_flags") or "—", t["tier"], t["selection_not_a_result"], t["gates"]]


def render_md(res: dict) -> bytes:
    L = [AS_OF_LINE, "",
         "# TIER-C11 · §0 VERDICTS — the nine registrations, ONE family (m = 9, bar 0.10/9 = "
         "0.011111)", "",
         f"regbooks root: `{res['regbooks_root']}` · registry head `{REGISTRY_HEAD[:16]}…` "
         f"(verified) · seed {SEED} (sensitivity {SEED_SENS}) · n_boot {res['n_boot']} · "
         f"asset-cluster bootstrap (T5) · CI = 5th..95th percentile · p = (#draws <= 0 + 1)/"
         f"(B + 1)", ""]
    if res.get("banner"):
        L += [f"**{res['banner']}**", ""]
    L += ["## §0 table", ""]
    L += _md_table(S0_HEADER, [s0_line(r) for r in res["rows"]])
    fam = res["family"]
    L += ["", "## Family", "",
          f"m = {fam['family_m']} · q = {fam['family_q']} · bar = 0.10/9 = {fam['bar_filed']} "
          f"(exact 1/90) · tests spent {fam['tests_spent']} · SUPPORTED: "
          f"{', '.join(fam['supported']) or 'none'}", ""]
    L += _md_table(["#", "registration", "status", "verdict_of_record", "spent a test",
                    "p", "clears bar"],
                   [[str(x["seq"]), x["registration"], str(x["status"]),
                     str(x["verdict_of_record"]), "yes" if x["spent_test"] else "no",
                     _p(x["p_one_sided"]),
                     "—" if x["clears_bar"] is None else ("yes" if x["clears_bar"] else "no")]
                    for x in fam["rows"]])
    L += ["", f"Law: {fam['law']}", "", "## Detail blocks", ""]
    for r in res["rows"]:
        L += _detail(r)
    te = [t for r in res["rows"] for t in r["tier_e"]]
    L += ["## Tier-E rows — a SELECTION, not a result · gates nothing · no verdict word", "",
          f"{len(te)} rows, every one collared (tier / selection_not_a_result / gates); "
          f"would_read_ci_only is the CI-only reading.", ""]
    L += _md_table(TE_HEADER, [te_line(t) for t in te])
    bi = res["base_ident"]
    L += ["", "## F-BASE-IDENT", "",
          f"{'OK' if bi['ok'] else 'FAILED'} — checked {bi['registrations_checked']}; absent "
          f"{bi['absent']}; books/v6: n {res['v6']['n']}, content sha "
          f"{res['v6']['content_sha'][:16]}… == manifest", ""]
    L += _md_table(["registration", "base book_sha256"],
                   [[k, str(v)] for k, v in bi["book_sha256"].items()])
    for f in bi["findings"]:
        L.append(f"- {f}")
    L += ["", "## Registry verification", "",
          f"contract `{CONTRACT_SHA[:16]}…` · LEANS `{LEANS_SHA[:16]}…` · REGISTRATIONS.json "
          f"`{REGISTRATIONS_SHA[:16]}…` · head `{REGISTRY_HEAD[:16]}…` == REGISTRY_PIN.json · "
          f"0 findings · LEANS_AMENDMENTS.md (binding, hashed) "
          f"`{str(res['registry']['leans_amendments']['sha256'])[:16]}…`", ""]
    L += [f"Records read beside the regbooks (plain JSON): "
          + " · ".join(f"{k} {v['path']} `{str(v['sha256'])[:16]}…`"
                       for k, v in sorted(res["records"].items())), ""]
    L += _md_table(["seq", "registration", "text lines", "re-cut == text", "payload sha",
                    "chain line sha"],
                   [[str(p["seq"]), p["registration"], f"{p['text_lines'][0]}-"
                     f"{p['text_lines'][1]}", str(p["text_slice_recut_equal"]),
                     p["payload_sha256"][:16] + "…", p["line_sha256"][:16] + "…"]
                    for p in res["registry"]["per_registration"]])
    L += ["", "## Readings (sub-readings of the scorer)", ""]
    L += [f"- {x}" for x in READINGS]
    L += ["", "## Findings", ""]
    fl = res["findings"]
    L += ([f"- {f}" for f in fl] if fl else ["- none"])
    return ("\n".join(L) + "\n").encode("utf-8")


def _detail(r: dict) -> list[str]:
    L = [f"### {r['seq']} · {r['registration']} [{r['prior_pct']}%]", "",
         "Text of record (the contract's own lines):", "", "```", r["text_of_record"], "```", "",
         f"- kind: {r['kind']} · panel {r['panel_name']} · era {r['era']} · ruler "
         f"{r['ruler']} · payload sha `{r['payload_sha256'][:16]}…`",
         f"- status: {r['status']}" + (f" — {builder_status(r['status_reason'])}"
                                       if r.get("status_reason") else ""),
         f"- verdict cell: {r['verdict_cell']}"]
    for k, v in (r.get("labels") or {}).items():
        L.append(f"- {k} (full text): {v}")
    if "pre_seen" in (r.get("labels") or {}) and r["provenance"].get("scored"):
        L.append(f"- pre_seen: new information = the interval and the campaigns entered after "
                 f"2026-09-21T16:00Z: scored "
                 f"{r['provenance']['scored']['entered_after_tc10_pin']}, base "
                 f"{(r['provenance'].get('base') or {}).get('entered_after_tc10_pin')}")
    if r.get("scale_in_sample_flag"):
        L.append(f"- scale_in_sample: {r['scale_in_sample_flag']}")
    if r.get("condition_record"):
        c = r["condition_record"]
        L.append(f"- condition record (SC-17, L-W.4): {c['path']} `{str(c['sha256'])[:16]}…` · met "
                 f"{c['met']} · delta {c['delta']} · cluster-90% hi {c['ci_hi']} · agrees with "
                 f"STATUS {r['status']}")
    if r.get("precondition_record"):
        c = r["precondition_record"]
        L.append(f"- precondition record (SC-17, L-S.1): {c['path']} `{str(c['sha256'])[:16]}…` · "
                 f"R2 {c['lens']} lens word of record {c['word_of_record']} · agrees with STATUS "
                 f"{r['status']}")
    if r.get("r2_beside"):
        L.append(f"- {r['r2_beside']['text']} · {r['r2_beside']['source']} "
                 f"`{str(r['r2_beside']['source_sha256'])[:16]}…`")
    if r.get("named_risk"):
        L.append(f"- named risk: {r['named_risk']}")
    for k in ("scored", "base"):
        p = r["provenance"].get(k)
        if p:
            L.append(f"- {k} arm: book_sha256 `{str(p['book_sha256'])[:16]}…` · n {p['n']} · "
                     f"sum_net_r {p['sum_net_r']} · era_scope {p['era_scope']} · ruler "
                     f"{p['ruler']} · entry bars straddling the era cut "
                     f"{p['entry_bars_straddling_era_cut']} · entered after the TC10 pin "
                     f"{p['entered_after_tc10_pin']} · source {p['source_script']} · "
                     f"description (builder's): {p['description']}")
    s = r.get("stats")
    if s:
        m, sn = s["main"], s["sens"]
        L += [f"- seed {SEED}: point {_f(m['point'], 6)} · CI [{_f(m['lo'], 6)}, "
              f"{_f(m['hi'], 6)}] · p {_p(m['p_one_sided'])} = {m['p_num']}/{m['p_den']} "
              f"(draws <= 0: {m['n_draws_le_0']} of {m['n_draws_finite']}) · clears bar "
              f"{r['clears_bar']} · clusters {m['n_clusters']}",
              f"- deciding bound: the draw of rank {m['deciding_rank']} (ascending) of "
              f"{m['n_draws_finite']} = {_f(m['deciding_bound'], 6)} (p <= bar iff > 0) · "
              f"numpy's 1.111th percentile {_f(m['pctl_1p111'], 6)}",
              f"- seed {SEED_SENS} (sensitivity): point {_f(sn['point'], 6)} · CI "
              f"[{_f(sn['lo'], 6)}, {_f(sn['hi'], 6)}] · p {_p(sn['p_one_sided'])} · reads "
              f"{r['verdict_at_sens_seed']} · stable across seeds: "
              f"{r['verdict_stable_across_seeds']}",
              f"- books: scored n {m['n']} · sum R {_f(s['sum_net_r'], 6)} · mean R "
              f"{_f(s['mean_net_r'], 6)}"
              + (f" · base n {m['n_base']} · sum R {_f(s['sum_net_r_base'], 6)} · mean R "
                 f"{_f(s['mean_net_r_base'], 6)}" if s["sum_net_r_base"] is not None else "")]
        h, hs = s["haircut"], s["haircut_sens"]
        L.append(f"- haircut twin (same ruler on haircut_net_r, AM-7): {_f(h['point'], 6)} "
                 f"[{_f(h['lo'], 6)}, {_f(h['hi'], 6)}] p {_p(h['p_one_sided'])} · sens "
                 f"{_f(hs['point'], 6)} [{_f(hs['lo'], 6)}, {_f(hs['hi'], 6)}] p "
                 f"{_p(hs['p_one_sided'])}")
        d = s.get("d15")
        if r["ruler"] == "paired":
            L.append("- D15: " + ("—" if d is None else
                                   ", ".join(f"{k} {v}" for k, v in d.items())))
        else:                               # SC-22: T5.d15 pairs; this ruler does not
            L.append(f"- D15: n/a under the {r['ruler']} ruler (T5.d15 pairs on (symbol, "
                     f"entry_ms)) — " + ("no base" if d is None else
                                         "printed for the record only: "
                                         + ", ".join(f"{k} {v}" for k, v in d.items())))
            L.append("- concentration beside it (SC-22, deciding nothing): "
                     + conc_text(r["ruler"], r.get("concentration"), detail=True))
        if r.get("premise"):
            L.append("- premise: " + ", ".join(f"{k} {v}" for k, v in r["premise"].items()))
        if r.get("adds"):
            ad = r["adds"]
            L.append("- adds (AM-3): " + (
                f"ΣΔ {_f(ad['sum_delta_r'], 6)} · Σ add_r {_f(ad['sum_add_r'], 6)} · absorbed "
                f"funding {_f(ad['sum_absorbed_funding_r'], 6)} (v6-leg absorption subtracted: "
                f"{ad['base_absorption_subtracted']}, from {ad['base_absorption_source']}) · "
                f"residual "
                f"{_f(ad['residual_delta_minus_add_minus_absorbed'], 6)} · campaigns with adds "
                f"{ad['n_campaigns_with_adds']} · {ad['note']}" if ad["carried"] else ad["note"]))
        if r.get("gate"):
            g = r["gate"]
            L.append(f"- gate (post-filter): refused n {g['refused_n']} · mean "
                     f"{_f(g['refused_mean_r'], 6)} · sum {_f(g['refused_sum_r'], 6)} R · "
                     f"scored sum {_f(g['scored_sum_r'], 6)} R (n {g['scored_n']}) · base sum "
                     f"{_f(g['base_sum_r'], 6)} R (n {g['base_n']}) · added {g['added_n']}"
                     + (f" · {g['appendix']}" if g["appendix"] else ""))
        if r.get("scale_beside"):
            sb = r["scale_beside"]
            ins = sb["holdout_in_sample"]
            L.append(f"- SCALE-IN-SAMPLE beside: holdout slice (derived) "
                     f"{_stat_line(sb['holdout_slice_derived'])} · in-sample range reads in it "
                     f"{ins['in_sample'] if ins['in_sample'] is not None else 'not determinable'}"
                     f" of {ins['n']} ({', '.join(ins['columns']) or 'no column'}) · holdout arm "
                     f"{sb['holdout_arm'] or 'none filed'} "
                     f"{_stat_line_te(sb.get('holdout_arm_stat')) if sb['holdout_arm'] else ''}"
                     f" · frozen-3.0 twin {sb['frozen_arm'] or 'ABSENT'} "
                     f"{_stat_line_te(sb.get('frozen_arm_stat')) if sb['frozen_arm'] else ''}")
            ps = sb["pick_stability"]
            L.append(f"- {ps['text']} · record {ps.get('source')} "
                     f"`{str(ps.get('source_sha256'))[:16]}…`"
                     + (f" · {sb['fallback_label']}" if sb.get("fallback_label") else ""))
        for lab, lo in (("LOAO", s["loao"]), ("LOAO sens", s["loao_sens"])):
            L += ["", f"{lab} (seed {lo['seed']}): {lo['line']} · bar {lo['bar']}/{lo['panels']}"
                      f" · clears {lo['clears_line']} · zero-campaign panels "
                      f"{lo['zero_campaign_assets'] or 'none'} · above excl. zero-campaign "
                      f"{lo['above_excl_zero_campaign']}", ""]
            L += _md_table(["dropped", "n", "point", "90% CI", "above", "below", "note", "tier",
                            "selection_not_a_result", "gates"],
                           [[p["dropped"], str(p["n"]), _f(p["point"]),
                             f"[{_f(p['ci_lo'])}, {_f(p['ci_hi'])}]", str(p["excludes_above"]),
                             str(p["excludes_below"]), p["note"], COLLAR["tier"],
                             COLLAR["selection_not_a_result"], COLLAR["gates"]]
                            for p in lo["per_panel"]])
    if r["tier_e"]:
        L += ["", f"Tier-E rows of {r['registration']} (collared; no verdict word):", ""]
        L += _md_table(TE_HEADER, [te_line(t) for t in r["tier_e"]])
    for h in r["halts"]:
        L.append(f"- HALT: {h}")
    for n in r["notes"]:
        L.append(f"- note: {n}")
    L.append("")
    return L


# ══════════════════════════════════════════════ 8 · THE RUN
def score_all(regbooks_root: Path = REGBOOKS, n_boot: int = N_BOOT,
              banner: str | None = None, root_label: str | None = None) -> dict:
    doc, reg_rec = load_registry(ROOT)
    fees = _fees()
    L = Loader(Path(regbooks_root), fees)
    v6, v6_rec = v6_frame()
    bases = {}
    base_halts = []
    for rid in BASE_IDENT_REGS:
        st, sh, _ = L.status_of(rid)
        if st is None or sh or "base" not in (st.get("arms") or []):
            continue
        B = L.arm(rid, "base")
        if B["halts"] or B["df"] is None:
            base_halts.append(f"{rid}/base unusable: " + " | ".join(B["halts"]))
            continue
        bases[rid] = {"df": B["df"], "sha": B["sha"]}
    ident = base_ident(bases, v6)
    ident["unusable"] = base_halts
    rows = [score_registration(L, reg, ident, n_boot=n_boot) for reg in doc["registrations"]]
    te = [t for r in rows for t in r["tier_e"]]
    col = collar_findings(te)
    if col:
        raise SystemExit("HALT (COLLAR): a Tier-E row lacks its collar or carries a verdict "
                         "word — nothing written:\n  " + "\n  ".join(col))
    findings = []
    for r in rows:
        findings += [f"{r['registration']}: HALT {h}" for h in r["halts"]]
        findings += [f"{r['registration']}: {n}" for n in r["notes"]]
        findings += [f"{t['registration']}/{t['arm']}: Tier-E halted: {t['halted']}"
                     for t in r["tier_e"] if t.get("halted")]
    findings += ident["findings"]
    records = {"scale_picks": {k: L.picks()[k] for k in ("path", "sha256")},
               "r2_lens_verdicts": {k: L.r2()[k] for k in ("path", "sha256")}}
    if not L.picks()["ok"]:
        findings.append(f"SCALE-PICKS: {L.picks()['path']} unreadable ({L.picks()['error']}) — "
                        f"pick stability NOT PRINTABLE")
    if not L.r2()["ok"]:
        findings.append(f"R2-RECORD: {L.r2()['path']} unreadable ({L.r2()['error']})")
    res = {"regbooks_root": root_label or _root_label(regbooks_root), "n_boot": n_boot,
           "banner": banner, "registry": reg_rec, "v6": v6_rec, "base_ident": ident,
           "rows": rows, "family": family(rows), "findings": findings, "records": records}
    return res


DRY_LABEL = "book, not a verdict"


def _dry_facts(df: pd.DataFrame) -> str:
    """One arm's book facts — n, sum R, mean R, eras — and NOTHING ruled."""
    n = len(df)
    eras = df["era"].value_counts().to_dict()
    return (f"n {n:>4} · ΣR {float(df['net_r'].sum()):+.6f} · mean R "
            f"{(float(df['net_r'].mean()) if n else float('nan')):+.6f} · tuning "
            f"{eras.get('tuning', 0)} / holdout {eras.get('holdout', 0)}")


def dry_run(regbooks_root: Path = REGBOOKS,
            root_label: str | None = None) -> tuple[list[str], int]:
    """THE DRY RUN [TC10's --dry-run law]: verify the registry, read and validate every
    arm, F-BASE-IDENT, the status records (SC-17), the paired premise and the identity
    law (SC-15), the gate post-filter (SC-16), the spec-vs-sidecar checks — and print book
    facts only (n / sum R / mean R, labelled 'book, not a verdict').  It never calls a
    ruler, prints no interval, no p and no verdict word, and writes nothing.  Exit = the
    SC-10 bit flags (+2 a registered row would HALT, +4 a Tier-E arm is unusable, +8 a
    registration is ABSENT)."""
    doc, _ = load_registry(ROOT)
    fees = _fees()
    L = Loader(Path(regbooks_root), fees)
    v6, v6rec = v6_frame()
    bases = {}
    for rid in BASE_IDENT_REGS:
        st, sh, _ = L.status_of(rid)
        if st is None or sh or "base" not in (st.get("arms") or []):
            continue
        B = L.arm(rid, "base")
        if not B["halts"] and B["df"] is not None:
            bases[rid] = {"df": B["df"], "sha": B["sha"]}
    ident = base_ident(bases, v6)
    out = [f"DRY RUN · regbooks root {root_label or _root_label(regbooks_root)} · registry head "
           f"{REGISTRY_HEAD[:16]}… verified · books/v6 n {v6rec['n']} · every number below is a "
           f"{DRY_LABEL}"]
    flags = {"halt": False, "tier_e": False, "absent": False}   # EXIT_FLAGS[0..2]
    for reg in doc["registrations"]:
        spec = spec_of(reg)
        rid = spec["registration"]
        st, sh, sn = L.status_of(rid)
        if st is None:
            out.append(f"{spec['seq']} {rid}: ABSENT (no STATUS.json)")
            flags["absent"] = True
            continue
        arms = _arms_of(st)
        status = st.get("status")
        out.append(f"{spec['seq']} {rid}: {status} · spec ruler {spec['ruler']} · era "
                   f"{spec['era']} · arms {arms}")
        halts = list(sh)
        if not sh:
            halts += status_word_findings(rid, status, spec)
            halts += condition_record(L.root / rid, rid, status)[0]
            halts += precondition_record(L.r2(), rid, status)[0]
        for arm in arms:
            A = L.arm(rid, arm)
            if A["halts"] or A["df"] is None:
                if arm.startswith("tierE__"):
                    flags["tier_e"] = True
                else:
                    halts += A["halts"]
                out.append(f"    {arm:<34} HALT {' | '.join(A['halts'])[:220]}")
                continue
            side = A["side"]
            out.append(f"    {arm:<34} {_dry_facts(A['df'])} · ruler {side.get('ruler')} · "
                       f"era_scope {side.get('era_scope')} · {_panel_name(side.get('panel'))} · "
                       f"sha {A['sha'][:16]}… ({DRY_LABEL})")
            for nt in A["notes"]:
                out.append(f"      note: {nt}")
        B = L.arm(rid, "base") if "base" in arms else None
        bdf = B["df"] if (B is not None and not B["halts"]) else None
        if status == "BUILT" and "scored" in arms:
            A = L.arm(rid, "scored")
            if not A["halts"] and A["df"] is not None:
                side = A["side"]
                for k, want in (("ruler", spec["ruler"]), ("era_scope", spec["era"])):
                    if side.get(k) != want:
                        halts.append(f"SPEC-MISMATCH: scored {k} {side.get(k)!r} != {want!r}")
                if sorted(side.get("panel") or []) != sorted(spec["panel"]):
                    halts.append(f"SPEC-MISMATCH: scored panel != {spec['panel_name']}")
                if _uses_base(spec["ruler"]):
                    if B is None:
                        halts.append("BASE-ABSENT")
                    elif bdf is not None:
                        if spec["ruler"] == "paired":
                            pp = paired_premise(A["df"], bdf)
                            if not pp:
                                pp = identity_findings(A["df"], bdf, f"{rid}/scored")
                            halts += pp
                            if not pp:
                                idn = identity_summary(A["df"], bdf)
                                out.append(f"    paired premise: key sets identical, n == n_base; "
                                           f"identity law held on {idn['unacted']} unacted "
                                           f"campaign(s) ({idn['acted']} acted)")
                        else:
                            tp = two_sample_premise(A["df"], bdf)
                            out.append(f"    two-sample keys: shared {tp['n_shared_keys']}, only "
                                       f"scored {tp['n_only_scored']}, only base "
                                       f"{tp['n_only_base']}"
                                       + (" · FLAG: identical key sets" if tp.get("flag")
                                          else ""))
                        if spec["gate"]:
                            gh = gate_findings(A["df"], bdf, f"{rid}/scored")
                            halts += gh
                            if not gh:
                                out.append("    gate: a post-filter of the base (no new key, "
                                           "every kept row unchanged)")
                        if rid in BASE_IDENT_REGS and not ident["per_registration_ok"].get(rid):
                            halts.append("F-BASE-IDENT: this row's base is not the one v6 book")
        # SC-15 on the paired Tier-E arms ruled against this registration's own base
        for arm in arms:
            if not arm.startswith("tierE__") and not (arm == "scored" and status != "BUILT"):
                continue
            A = L.arm(rid, arm)
            side = A["side"]
            if (A["halts"] or A["df"] is None or side.get("ruler") != "paired"
                    or side.get("base_arm") or bdf is None):
                continue
            bb = _restrict(bdf, side.get("era_scope", "full"))
            th = paired_premise(A["df"], bb) or identity_findings(A["df"], bb, f"{rid}/{arm}")
            if th:
                flags["tier_e"] = True
                out.append(f"    HALT (Tier-E {arm}): {' | '.join(th)[:300]}")
        for h in halts:
            out.append(f"    HALT: {h[:300]}")
        if halts:
            flags["halt"] = True
    out.append(f"F-BASE-IDENT {'OK' if ident['ok'] else 'FAILED'} · checked "
               f"{ident['registrations_checked']} · absent {ident['absent']}"
               + "".join(f"\n    {f[:300]}" for f in ident["findings"]))
    conds = [EXIT_FLAGS[i] for i, k in enumerate(("halt", "tier_e", "absent")) if flags[k]]
    out.append(exit_line(conds))
    code = 0
    for _, b in conds:
        code |= b
    return out, code


def render(res: dict) -> dict:
    """{file name: bytes} — deterministic (no clock, no absolute path, sorted keys)."""
    scores = {"as_of_last_closed_4h": "2026-09-25T00:00:00Z", "seed": SEED,
              "seed_sens": SEED_SENS, "n_boot": res["n_boot"],
              "regbooks_root": res["regbooks_root"], "banner": res.get("banner"),
              "readings": list(READINGS), "rows": res["rows"], "findings": res["findings"]}
    files = {"REGISTRY_CHECK.json": jbytes(res["registry"]),
             "SCORES.json": jbytes(scores),
             "FAMILY.json": jbytes({**res["family"], "as_of_last_closed_4h":
                                    "2026-09-25T00:00:00Z", "banner": res.get("banner")}),
             "BASE_IDENT.json": jbytes({**res["base_ident"], "v6": res["v6"]}),
             "S0_VERDICTS.md": render_md(res)}
    inputs = {}
    for r in res["rows"]:
        for k, p in sorted(r["provenance"].items()):
            inputs[f"{r['registration']}/{k}"] = {"book_sha256": p["book_sha256"],
                                                   "sidecar_sha256": p["sidecar_sha256"]}
        for t in r["tier_e"]:
            if t["arm"].startswith(("tierE__", "scored")):
                inputs[f"{t['registration']}/{t['arm']}"] = {"book_sha256": t["book_sha256"]}
    for r in res["rows"]:
        for k in ("condition_record", "precondition_record"):
            if r.get(k):
                inputs[f"{r['registration']}/{k}"] = {"path": r[k]["path"],
                                                      "sha256": r[k]["sha256"]}
    files["SCORE_MANIFEST.json"] = jbytes({
        "stage": "TC11-SCORE", "as_of_last_closed_4h": "2026-09-25T00:00:00Z",
        "regbooks_root": res["regbooks_root"], "inputs": inputs,
        "records": res["records"], "leans_amendments": res["registry"]["leans_amendments"],
        "outputs": {k: sha256_bytes(v) for k, v in sorted(files.items())},
        "registry_head": REGISTRY_HEAD, "v6": res["v6"]})
    return files


def exit_conditions(res: dict, noclobber: bool = False) -> list[tuple[str, int]]:
    """SC-10: every condition that holds, each with its bit [repair m-9]."""
    rows = res["rows"]
    held = {EXIT_FLAGS[0][0]: any(r["verdict_of_record"] == "HALT" for r in rows),
            EXIT_FLAGS[1][0]: any(t.get("halted") for r in rows for t in r["tier_e"]),
            EXIT_FLAGS[2][0]: any(r["status"] == "ABSENT" for r in rows),
            EXIT_FLAGS[3][0]: bool(noclobber)}
    return [(name, bit) for name, bit in EXIT_FLAGS if held[name]]


def exit_code(res: dict, noclobber: bool = False) -> int:
    """SC-10: the bitwise OR of the flags that hold (0 = none); nothing masks another."""
    code = 0
    for _, bit in exit_conditions(res, noclobber):
        code |= bit
    return code


def exit_line(conds: list[tuple[str, int]]) -> str:
    code = 0
    for _, b in conds:
        code |= b
    return (f"EXIT {code} = " + (" + ".join(f"{b} ({n})" for n, b in conds) if conds
                                 else "0 (no condition)"))


def _guard_out(out: Path) -> Path:
    out = Path(out).resolve()
    sc = SCORES.resolve()
    det = DET_ROOT.resolve()
    inside = (out == sc) or (det == out or det in out.parents)
    outside_repo = ROOT.resolve() not in out.parents and out != ROOT.resolve()
    if not (inside or outside_repo):
        raise SystemExit(f"HALT: --out-dir {out} must be {sc}, under {det}, or outside the repo")
    return out


def write_outputs(files: dict, out: Path, refile: bool) -> list[str]:
    """No-clobber: identical bytes are left alone; different bytes go to <stem>_rerun
    and the record is untouched unless --refile."""
    out.mkdir(parents=True, exist_ok=True)
    notes = []
    for name, b in sorted(files.items()):
        p = out / name
        if p.exists() and p.read_bytes() == b:
            continue
        if p.exists() and not refile:
            rr = p.with_name(p.stem + "_rerun" + p.suffix)
            rr.write_bytes(b)
            notes.append(f"NO-CLOBBER: {name} differs from the record; this run -> {rr.name}")
            continue
        tmp = p.with_name(p.name + ".tmp")
        tmp.write_bytes(b)
        os.replace(tmp, p)
    return notes


def main(argv: list[str]) -> int:
    root = next((a.split("=", 1)[1] for a in argv if a.startswith("--regbooks-root=")), None)
    label = next((a.split("=", 1)[1] for a in argv if a.startswith("--regbooks-label=")), None)
    out = next((a.split("=", 1)[1] for a in argv if a.startswith("--out-dir=")), None)
    banner = next((a.split("=", 1)[1] for a in argv if a.startswith("--banner=")), None)
    root = Path(root).resolve() if root else REGBOOKS
    if "--dry-run" in argv:
        lines, code = dry_run(root, root_label=label)
        print("\n".join(lines))
        return code
    out = _guard_out(Path(out)) if out else SCORES
    res = score_all(root, banner=banner, root_label=label)
    files = render(res)
    notes = write_outputs(files, out, "--refile" in argv)
    for r in res["rows"]:
        m = (r["stats"] or {}).get("main") if r.get("stats") else None
        print(f"{r['seq']} {r['registration']:<10} {str(r['status']):<24} "
              + (f"n {m['n']:>4} point {_f(m['point'])} [{_f(m['lo'])}, {_f(m['hi'])}] p "
                 f"{_p(m['p_one_sided'])}  " if m else "")
              + f"{r['verdict_cell'][:140]}")
    print(f"F-BASE-IDENT {'OK' if res['base_ident']['ok'] else 'FAILED'}; "
          f"{len(res['findings'])} finding(s); wrote {sorted(files)} -> {_root_label(out)}")
    for n in notes:
        print(n)
    conds = exit_conditions(res, noclobber=bool(notes))
    print(exit_line(conds))
    return exit_code(res, noclobber=bool(notes))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
