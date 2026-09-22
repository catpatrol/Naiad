#!/usr/bin/env python3
"""TIER-C10 STAGE B · FILE THE SIX REGISTRATIONS.

TEXT BEFORE RESULT.  A filed registration is NEVER amended: filing different text
under a filed id HALTs, and filing an id for which a .scored.json exists HALTs.
So this script defaults to --dry-run and files only on an explicit --file.

The six texts are NOT retyped here.  They are read VERBATIM from
research_outputs/tierc10/REGISTRATION_TEXTS.json, which is what the drafting and
three review rounds produced and what a reader reviews.  The arms are built with
tierc10_panel.arm_spec() so a hand-written dict can never reach the door.

WITNESS_LAW.  research_outputs/tierc10/registrations/ is gitignored, so git is NOT
the witness.  After filing, the registry length, head and every payload sha are
written to research_outputs/tierc10/REGISTRY_PIN.json, which the orchestrator
commits as a TRACKED file.  Without that pin the chain has no witness.
"""
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tierc10_panel as TP          # noqa: E402
import tierc8, tierc9               # noqa: E402

ROOT   = HERE.parent
TEXTS  = ROOT / "research_outputs/tierc10/REGISTRATION_TEXTS.json"
PIN    = ROOT / "research_outputs/tierc10/REGISTRY_PIN.json"

# THE ORDER OF FILING IS FIXED AND STATED: the contract's own order, descending
# prior.  The registry is hash-chained, so the order is part of the record.
ORDER = ("P-GEN-1", "P-SPR-2", "P-BE-1", "P-TRG-2", "P-BRK-I1", "P-BRK-S1")

V6 = tierc9.V6_ROLES
TRG912 = tierc9.Roles(name="trigger-9/12", trg_f=9, trg_s=12)
UNSEEN12 = ("ENAUSDT", "PUMPUSDT", "HYPEUSDT", "MNTUSDT_BYBIT", "SUIUSDT", "LTCUSDT",
            "XMRUSDT", "BNBUSDT", "UNIUSDT", "1000PEPEUSDT", "DOGEUSDT", "1000BONKUSDT")
NEVER_TOUCHED = ("PUMPUSDT", "MNTUSDT_BYBIT", "SUIUSDT")   # DATA_SPEND_AUDIT.json, F-D-5
GEN1_CARD = tierc8.Card(name="tc10-gen1-card-v6")

def arms_for(rid):
    A = TP.arm_spec
    if rid == "P-GEN-1":
        return [A("unseen12-card-v6", UNSEEN12, "vs_zero", True, ("card",),
                  card=GEN1_CARD, roles=V6, base="zero", loao_line="lineage", era="full"),
                A("panel17-card-v6", TP.panel17(), "vs_zero", False, ("card",),
                  card=GEN1_CARD, roles=V6, base="zero", loao_line="lineage", era="full"),
                A("never-touched-card-v6", NEVER_TOUCHED, "vs_zero", False, ("card",),
                  card=GEN1_CARD, roles=V6, base="zero", loao_line="lineage", era="full")]
    if rid == "P-SPR-2":
        return [A("standalone vs zero · full corridor", TP.CLASSIC5, "vs_zero", True,
                  ("spring",), base="zero", loao_line="lineage", era="full"),
                A("standalone vs zero · tuning era", TP.CLASSIC5, "vs_zero", False,
                  ("spring",), base="zero", loao_line="lineage", era="tuning"),
                A("standalone vs zero · holdout era", TP.CLASSIC5, "vs_zero", False,
                  ("spring",), base="zero", loao_line="lineage", era="holdout"),
                A("union with card v6 vs card v6", TP.CLASSIC5, "set_change", False,
                  ("card", "spring"), base="card-v6", loao_line="lineage", era="full")]
    if rid == "P-BE-1":
        return [A("be-floor-1R vs card-v6 (CLASSIC5, full)", TP.CLASSIC5, "two_sample", True,
                  ("card",), base="card-v6", loao_line="lineage", era="full"),
                A("be-floor-1R vs card-v6 (CLASSIC5, tuning) [Tier-E]", TP.CLASSIC5,
                  "set_change", False, ("card",), base="card-v6", loao_line="lineage", era="tuning"),
                A("be-floor-1R vs card-v6 (CLASSIC5, holdout) [Tier-E]", TP.CLASSIC5,
                  "set_change", False, ("card",), base="card-v6", loao_line="lineage", era="holdout"),
                A("be-floor-2R sensitivity vs card-v6 (CLASSIC5, full) [Tier-E]", TP.CLASSIC5,
                  "set_change", False, ("card",), base="card-v6", loao_line="lineage", era="full")]
    if rid == "P-TRG-2":
        return [A("trg-9/12 vs card v6 · CLASSIC5 · full", TP.CLASSIC5, "two_sample", True,
                  ("card",), card=TP.CONTROL_CARD, roles=TRG912, base="card-v6",
                  loao_line="lineage", era="full"),
                A("trg-9/12 vs zero · CLASSIC5 · full", TP.CLASSIC5, "vs_zero", False,
                  ("card",), card=TP.CONTROL_CARD, roles=TRG912, base="zero",
                  loao_line="lineage", era="full"),
                A("trg-9/12 vs card v6 · CLASSIC5 · tuning era", TP.CLASSIC5, "two_sample", False,
                  ("card",), card=TP.CONTROL_CARD, roles=TRG912, base="card-v6",
                  loao_line="lineage", era="tuning"),
                A("trg-9/12 vs card v6 · CLASSIC5 · holdout era", TP.CLASSIC5, "two_sample", False,
                  ("card",), card=TP.CONTROL_CARD, roles=TRG912, base="card-v6",
                  loao_line="lineage", era="holdout")]
    if rid == "P-BRK-I1":
        return [A("CLASSIC5-memory-line", TP.CLASSIC5, "vs_zero", True, ("brk-i1",),
                  base="zero", loao_line="lineage", era="full"),
                A("CLASSIC5-tierE-band", TP.CLASSIC5, "vs_zero", False, ("brk-i1",),
                  base="zero", loao_line="lineage", era="full"),
                A("PANEL17-tierE-memory-line", TP.panel17(), "vs_zero", False, ("brk-i1",),
                  base="zero", loao_line="lineage", era="full")]
    if rid == "P-BRK-S1":
        # excl_zero_campaign is the STRICTER count and is chosen for that reason;
        # the first draft claimed lineage was stricter and was refuted by loao_n.
        return [A("P-BRK-S1 vs zero", TP.CLASSIC5, "vs_zero", True, ("brk-s1",),
                  base="zero", loao_line="excl_zero_campaign", era="holdout"),
                A("P-BRK-S1 17-asset view", TP.panel17(), "vs_zero", False, ("brk-s1",),
                  base="zero", loao_line="excl_zero_campaign", era="holdout"),
                A("P-BRK-S1 memory-line anchor", TP.CLASSIC5, "vs_zero", False, ("brk-s1",),
                  base="zero", loao_line="excl_zero_campaign", era="holdout")]
    raise SystemExit(f"HALT: no arms defined for {rid!r}")


def main(argv):
    do_file = "--file" in argv
    regs = json.loads(TEXTS.read_text(encoding="utf-8"))
    missing = [r for r in ORDER if r not in regs]
    if missing:
        raise SystemExit(f"HALT: {TEXTS} carries no text for {missing}")

    # THE TEXT CANNOT FOLLOW THE RESULT.  Refuse outright if any result exists.
    scored = sorted(p.name for p in TP.REG_DIR.glob("*.scored.json")) if TP.REG_DIR.exists() else []
    if scored:
        raise SystemExit(f"HALT: a RESULT already exists ({scored}) — the text cannot follow "
                         f"the result. Nothing filed.")

    print("=" * 78)
    print("TIER-C10 STAGE B — REGISTRATIONS", "· FILING" if do_file else "· DRY RUN (nothing filed)")
    print(f"  registry dir : {TP.REG_DIR}  (exists: {TP.REG_DIR.exists()})")
    print(f"  family m     : {TP.FAMILY_M}   seed {TP.SEED}   n_boot {TP.N_BOOT}")
    print(f"  texts        : {TEXTS.name}  ({sum(len(regs[r]['text']) for r in ORDER):,} chars)")
    print("=" * 78)

    built = {}
    for rid in ORDER:
        rec = regs[rid]
        arms = arms_for(rid)
        built[rid] = (rec, arms)
        sc = [a for a in arms if a["scored_in_family"]]
        lines = {a.get("loao_line") for a in arms}
        eras = {a.get("era") for a in arms}
        panels = {a["panel_name"] for a in arms}
        clause = TP.loao_line_clause(sorted(lines)[0]) if len(lines) == 1 else None
        print(f"\n{rid}  prior {rec['prior_pct']}%   arms {len(arms)}   scored {len(sc)}")
        print(f"    scored arm : {sc[0]['arm'] if sc else '—'}")
        print(f"    panels     : {sorted(panels)}")
        print(f"    eras       : {sorted(eras)}   loao line: {sorted(lines)}")
        print(f"    bar        : above_half {rec['above_half_bar']}/{len(sc[0]['panel']) if sc else '?'}")
        print(f"    clause in text: {clause in rec['text'] if clause else 'MIXED LINES — register() will refuse'}")
        print(f"    text       : {len(rec['text']):,} chars · {rec['text'].splitlines()[0][:66]}")

    if not do_file:
        print("\n" + "=" * 78)
        print("DRY RUN ONLY. Nothing was filed. Re-run with --file to file.")
        print("=" * 78)
        return 0

    print("\n" + "=" * 78 + "\nFILING\n" + "=" * 78)
    pins = {}
    for rid in ORDER:
        rec, arms = built[rid]
        out = TP.register(rid, rec["text"], rec["prior_pct"], arms=arms, family_m=TP.FAMILY_M)
        pins[rid] = {"seq": out["seq"], "sha256": out["sha256"],
                     "text_sha256": out["text_sha256"], "prior_pct": rec["prior_pct"],
                     "already_filed": out.get("already_filed", False),
                     "registry_len": out["registry_len"], "registry_head": out["registry_head"]}
        print(f"  {rid:<10} seq {out['seq']}  sha {out['sha256'][:16]}…  "
              f"registry_len {out['registry_len']}  head {out['registry_head'][:16]}…"
              f"{'  (already filed — no-op)' if out.get('already_filed') else ''}")

    head = TP.registry_head()
    doc = {"tier": "TIER-C10", "stage": "B",
           "as_of_of_record": "2026-09-21T16:00:00Z", "seed": TP.SEED,
           "family_m": TP.FAMILY_M, "n_boot": TP.N_BOOT,
           "order_of_filing": list(ORDER),
           "registry_len": head["registry_len"], "registry_head": head["registry_head"],
           "registrations": pins,
           "witness_law": ("the registrations directory is gitignored and git is NOT the witness; "
                           "these pins are the witness and this file is committed TRACKED"),
           "texts_artifact": "research_outputs/tierc10/REGISTRATION_TEXTS.json"}
    PIN.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
    print(f"\n  WITNESS PINNED -> {PIN}")
    print(f"  registry_len {head['registry_len']}  registry_head {head['registry_head']}")
    print("  COMMIT THIS FILE (git add -f) or the chain has no witness.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
