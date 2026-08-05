#!/usr/bin/env python
"""brief_render.py -- Part I / Part II HTML from a STORED capture (§2, §3.5).

    C:\\venvs\\naiad\\Scripts\\python.exe scripts/brief_render.py --date 2026-08-03 --slot post_ny

THE RENDER RECOMPUTES NOTHING.  Every number here is read from the capture.  A
render that recomputed would be a second source of truth and the two would drift;
worse, the drift would be invisible, because the page would still look right.
That is why the capture is the record and the HTML is disposable.

TWO PARTS, BOTH PRINTED (ratified A-1).  Part I is the market monitor, generous
by design -- the operator cannot judge the decision instrument without seeing the
monitor it was distilled from.  Part II is derived from Part I under printed
rules, and §2.2's SEQUENCING RULE binds: a reader with Part I and the rules header
must be able to reconstruct Part II by hand.

PARITY BANNER.  Until the operator's readings are returned and matched, every
render says so at the top.  F-B33 asserts it in both directions.
"""

import argparse
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

BRIEFS = ROOT / "briefs"
OUT_DIR = ROOT / "research_outputs" / "brief"

# Atlas visual language.  Dark, low-chroma, one accent per semantic role; nothing
# here encodes a judgement the numbers do not already carry.
PAL = {"ink": "#0E1420", "panel": "#151D2C", "rule": "#26324C",
       "tx": "#C9D4E6", "mute": "#7A8AA5", "warn": "#E8853F",
       "ok": "#54C6A0", "bad": "#D9647A", "accent": "#6FA8DC"}


def esc(x):
    return html.escape("" if x is None else str(x))


def num(x, nd=2):
    if x is None:
        return "&mdash;"
    try:
        return f"{float(x):,.{nd}f}"
    except (TypeError, ValueError):
        return esc(x)


def sig(x, nd=2):
    """Signed, for quantities where the sign is the information."""
    if x is None:
        return "&mdash;"
    return f"{float(x):+,.{nd}f}"


def chip(text, kind="mute"):
    c = {"mute": PAL["mute"], "ok": PAL["ok"], "warn": PAL["warn"],
         "bad": PAL["bad"], "accent": PAL["accent"]}[kind]
    return (f'<span class="chip" style="border-color:{c};color:{c}">'
            f'{esc(text)}</span>')


# ══════════════════════════════════════════════════ D.7.1 target bucketing

# The mirror of R-1.  R-1 was: a knife-edge STOP inflates R:R.  With far targets
# admitted (correctly -- see the withdrawn D.4), the mirror appears: a distant
# TARGET inflates R:R just as arbitrarily.  A 47-ATR target on a 0.25-ATR stop
# reads 188:1 and means nothing.
#
# The fix is the same in spirit as R-1's: do not exclude, SEGREGATE.  Rank WITHIN
# distance buckets and never globally, so a near-target setup is compared with
# other near-target setups and the number stays interpretable.
TARGET_BUCKETS = (("NEAR", 0.0, 2.0), ("MID", 2.0, 6.0), ("FAR", 6.0, float("inf")))


def vwap_provenance_chip(a):
    """§5.9 -- every VWAP layer prints its SUBSTRATE and SOURCE.

    READ FROM THE CAPTURE, never imported. The render may not reach into
    `analytics` (F-B10: a render that recomputed would be a second source of
    truth), and reading the stored value is also the more honest chip -- it
    reports what the capture WAS BUILT WITH, not what the current code would do
    if it ran again.

    The point of printing it at all: a number differing from the operator's
    daily chart must explain itself where it is read, rather than becoming a
    parity incident three cycles later.
    """
    win = (a.get("rvwap") or {}).get("windows") or {}
    sub = src = None
    for w in win.values():
        sub = sub or w.get("substrate")
        src = src or w.get("source")
    if not sub and not src:
        return ""
    return ('<p class="mute small">substrate <b>{}</b> &middot; source '
            '<b>{}</b> &middot; instrument <b>BINANCE perpetual</b> &mdash; '
            'pinned by ruling (R1/R2), read from the capture. A VWAP read from '
            'a 1D chart, a spot pair or an index is a DIFFERENT number, not a '
            'rounding difference.</p>').format(esc(sub or "?"), esc(src or "?"))


def target_bucket(atr_distance):
    if atr_distance is None:
        return None
    for name, lo, hi in TARGET_BUCKETS:
        if lo <= abs(atr_distance) < hi:
            return name
    return "FAR"


def bucket_board(rows):
    """Group R:R rows by target distance and rank WITHIN each bucket."""
    out = {name: [] for name, _, _ in TARGET_BUCKETS}
    for r in rows or []:
        d = r.get("target_atr")
        if d is None and r.get("target") is not None and r.get("risk"):
            d = None
        b = target_bucket(d)
        if b:
            out[b].append(r)
    for b in out:
        out[b].sort(key=lambda r: -(r.get("rr") or 0))
    return out


# ══════════════════════════════════════════════════════════════ Part I

def part1_html(sym, a):
    L = []
    px, atr = a.get("price"), a.get("daily_atr")
    L.append(f'<h3>{esc(sym)} <span class="mute">'
             f'{num(px)} &middot; daily ATR {num(atr)}</span></h3>')

    # ---- stretch (D.5), the multi-scale picture first: it frames everything
    st = a.get("stretch") or {}
    if st.get("rows"):
        L.append('<div class="card"><h4>Stretch &mdash; distance from every '
                 'volume-weighted mean, in sigma</h4>')
        # §5.9 -- SUBSTRATE and SOURCE on the layer itself. A value that differs
        # from the operator's daily chart must explain itself on sight rather
        # than becoming a parity incident.
        L.append(vwap_provenance_chip(a))
        L.append('<table><tr><th>anchor / window</th><th>mean</th><th>sigma</th>'
                 '<th>age (bars)</th>'
                 '<th>&sigma; position</th><th>ATR</th><th>band</th><th></th></tr>')
        for r in st["rows"]:
            if r.get("sigma_position") is None:
                L.append(f'<tr class="mute"><td>{esc(r["name"])}</td>'
                         f'<td colspan="6">&mdash;</td><td>{chip("warming","warn")}</td></tr>')
                continue
            flags = []
            if r.get("thin_sample"):
                flags.append(chip("thin sample", "warn"))
            if r.get("band_reached"):
                k = abs(r["band_reached"])
                flags.append(chip(f"past {k}&sigma;",
                                  "bad" if k >= 2 else "accent"))
            L.append(f'<tr><td>{esc(r["name"])}</td><td>{num(r["mean"])}</td>'
                     f'<td>{num(r["sigma"])}</td>'
                     f'<td>{r.get("bars") if r.get("bars") is not None else "&mdash;"}</td>'
                     f'<td class="big">{sig(r["sigma_position"])}</td>'
                     f'<td>{sig(r["atr"])}</td><td>{r.get("band_reached") or 0}</td>'
                     f'<td>{"".join(flags)}</td></tr>')
        L.append('</table>')
        # C6 item 1.4 -- sigma WIDTHS are comparable only at comparable AGES.
        # A young anchor's band is narrow because it has accumulated less time,
        # not because the market is calm; its z-POSITION is unaffected.
        L.append('<p class="mute small"><b>Age is printed beside sigma because '
                 'widths are only comparable at comparable ages.</b> An anchored '
                 'sigma grows roughly as &radic;t &mdash; but so does the '
                 'displacement of price from the anchored mean, so the '
                 '&sigma; POSITION is approximately scale-free in time while '
                 'the WIDTH is not. '
                 'Measured on one Month anchor: &sigma; +86% from 29 to 114 bars '
                 'while the reading moved &minus;3.7%.</p>')
        d = st.get("disagreement")
        if d:
            L.append(f'<p class="prose">Widest disagreement: <b>{esc(d["max"]["name"])}</b> '
                     f'at {sig(d["max"]["sigma_position"])}&sigma; against '
                     f'<b>{esc(d["min"]["name"])}</b> at {sig(d["min"]["sigma_position"])}&sigma; '
                     f'&mdash; a spread of {num(d["spread_sigma"])}&sigma;.'
                     + (' Price is beyond +1&sigma; on one scale and below '
                        '&minus;1&sigma; on another at the same instant; both are true.'
                        if d.get("straddles_one_sigma") else '') + '</p>')
        L.append('</div>')

    # ---- C6 item 2: the DE-PEG layer. Redundancy is PRINTED, never
    # suppressed -- the operator wants to see what duplicates what and stay
    # open to what could be signal.
    dp = a.get("depeg") or {}
    if dp.get("adjacent"):
        L.append('<div class="card"><h4>Anchor de-peg &mdash; what is currently '
                 'redundant</h4><table>'
                 '<tr><th>pair</th><th>state</th><th>separation (ATR)</th>'
                 '<th>&sigma; ratio</th><th>ages (bars)</th>'
                 '<th>independent score</th></tr>')
        for key, r in dp["adjacent"].items():
            st = r.get("peg_state")
            k = {"identical": "bad", "pegged": "warn"}.get(st, "ok")
            ages = r.get("bars_since_anchor") or {}
            L.append(f'<tr><td>{esc(key)}</td><td>{chip(st, k)}</td>'
                     f'<td>{num(r.get("line_separation_atr"), 3)}</td>'
                     f'<td>{num(r.get("sigma_ratio"), 3)}</td>'
                     f'<td class="mute">'
                     f'{esc(r.get("shorter"))} {ages.get(r.get("shorter"))} / '
                     f'{esc(r.get("longer"))} {ages.get(r.get("longer"))}</td>'
                     f'<td>{"yes" if r.get("contributes_independent_score") else "<b>no</b>"}</td>'
                     f'</tr>')
        L.append('</table>')
        for r in dp["adjacent"].values():
            if r.get("peg_state") in ("identical", "pegged"):
                L.append(f'<p class="prose">{chip("redundant &mdash; still shown","warn")} '
                         f'{esc(r.get("prose"))}</p>')
        for e in (dp.get("events") or []):
            ages = e.get("ages_at_transition") or {}
            L.append(f'<p class="prose">{chip("DE-PEG","accent")} '
                     f'<b>{esc(e["pair"])}</b> moved {esc(e["from_state"])} '
                     f'&rarr; {esc(e["to_state"])} at '
                     f'{num(e.get("separation_atr"), 3)} ATR '
                     f'(ages {esc(str(ages))}).</p>')
        L.append('<p class="mute small"><b>An anchor carries independent '
                 'information only once it UNPEGS from the next-shorter one.</b> '
                 'Early in a period the longer anchor is measuring the same bars. '
                 'This is the CALENDAR, not the market: January 1 anchors Year, '
                 'Quarter and Month at once, so Y=Q until April 1; July 1 makes '
                 'M=Q for all of July. A redundant anchor is still drawn &mdash; '
                 'it contributes no independent score, and a de-peg is what makes '
                 'it informative.</p>')
        if dp.get("counterpart"):
            L.append('<p class="mute">anchored vs its rolling counterpart</p>'
                     '<table><tr><th>pair</th><th>state</th>'
                     '<th>separation (ATR)</th><th>&sigma; ratio</th>'
                     '<th>anchored age</th><th>rolling bars</th></tr>')
            for key, r in dp["counterpart"].items():
                if r.get("rolling_warming"):
                    L.append(f'<tr class="mute"><td>{esc(key)}</td>'
                             f'<td colspan="5">{chip("rolling warming","warn")}</td></tr>')
                    continue
                L.append(f'<tr><td>{esc(key)}</td>'
                         f'<td>{esc(r.get("peg_state"))}</td>'
                         f'<td>{num(r.get("line_separation_atr"), 3)}</td>'
                         f'<td>{num(r.get("sigma_ratio"), 3)}</td>'
                         f'<td>{r.get("anchored_bars")}</td>'
                         f'<td>{r.get("rolling_bars")}</td></tr>')
            L.append('</table><p class="mute small">While an anchored VWAP is '
                     'warming, its rolling counterpart is <b>already fully '
                     'formed</b> over the same span of market memory &mdash; so '
                     'that view is never missing. The separation between them is '
                     'itself information: calendar-anchoring versus '
                     'trailing-window on the same horizon.</p>')
        L.append('</div>')

    # ---- G7 anchor degeneracy (C5 3.1): a calendar accident must not read
    # as agreement between tools.
    deg = a.get("anchor_degeneracy") or []
    if deg:
        L.append('<div class="card"><h4>Anchor degeneracy &mdash; coinciding '
                 'anchors</h4>')
        for g in deg:
            L.append(f'<p class="prose">{chip("degenerate","warn")} '
                     f'<b>{esc(" = ".join(g["anchors"]))}</b> anchor on the same '
                     f'bar ({esc(g["anchor"])}), so their '
                     f'{g["duplicate_levels"]} levels are identical by '
                     f'construction and collapse to {g["collapses_to"]}. '
                     f'A degeneracy of the <b>calendar</b>, not agreement '
                     f'between tools &mdash; counted once, adding no score.</p>')
        L.append('</div>')

    # ---- windowed volume profiles
    vol = (a.get("volume_windows") or {}).get("windows") or {}
    if vol:
        L.append('<div class="card"><h4>Windowed volume profiles</h4>')
        L.append('<table><tr><th>window</th><th>POC</th><th>VAH</th><th>VAL</th>'
                 '<th>LVNs</th><th>substrate</th><th>lockbox</th></tr>')
        for w, b in vol.items():
            if b.get("warming"):
                L.append(f'<tr class="mute"><td>{esc(w)}</td>'
                         f'<td colspan="4">{chip("warming","warn")} no number</td>'
                         f'<td>{esc(b.get("substrate"))}</td><td></td></tr>')
                continue
            ov = (b.get("lockbox_overlap") or {}).get("overlap_days")
            L.append(f'<tr><td>{esc(w)}</td><td>{num(b["poc"])}</td>'
                     f'<td>{num(b["vah"])}</td><td>{num(b["val"])}</td>'
                     f'<td>{len(b.get("lvns") or [])}</td>'
                     f'<td>{esc(b.get("substrate"))}</td>'
                     f'<td>{num(ov,1) if ov else "&mdash;"}</td></tr>')
        L.append('</table><p class="mute small">Volume spread uniformly across '
                 'each bar&rsquo;s range &mdash; an approximation of tick data.</p></div>')

    # ---- §4.2 PROSE REQUIREMENT
    nest = a.get("va_nesting") or {}
    if nest.get("prose"):
        L.append('<div class="card"><h4>Value-area nesting</h4>')
        for s in nest["prose"]:
            L.append(f'<p class="prose">{esc(s)}</p>')
        L.append('</div>')

    # ---- oscillators
    osc = (a.get("oscillators") or {}).get("timeframes") or {}
    if osc:
        L.append('<div class="card"><h4>Oscillators</h4><table>'
                 '<tr><th>tf</th><th>RSI</th><th>StochRSI %K</th><th>%D</th>'
                 '<th>MACD</th><th>signal</th><th>hist</th><th>AO</th></tr>')
        for tf, b in osc.items():
            if b.get("warming"):
                L.append(f'<tr class="mute"><td>{esc(tf)}</td>'
                         f'<td colspan="7">{chip("warming","warn")}</td></tr>')
                continue
            L.append(f'<tr><td>{esc(tf)}</td><td>{num(b.get("rsi"))}</td>'
                     f'<td>{num(b.get("stoch_rsi_k"))}</td><td>{num(b.get("stoch_rsi_d"))}</td>'
                     f'<td>{num(b.get("macd"))}</td><td>{num(b.get("macd_signal"))}</td>'
                     f'<td>{num(b.get("macd_hist"))}</td><td>{num(b.get("ao"))}</td></tr>')
        L.append('</table>')
        dv = (a.get("oscillators") or {}).get("divergences") or []
        if dv:
            L.append(f'<p class="mute small">{len(dv)} generalised divergence(s) '
                     f'recorded, each carrying the price level of its pivot.</p>')
        L.append('<p class="mute small">The 1M plane carries price and volume '
                 'structure only &mdash; a closed-bar monthly oscillator has almost '
                 'no sample.</p></div>')

    # ---- the FULL bias scorecard, every vote (operator ruling A-4)
    bias = a.get("bias") or {}
    if bias:
        L.append('<div class="card"><h4>Bias scorecard &mdash; every vote</h4>')
        for horizon, b in bias.items():
            if not isinstance(b, dict):
                continue
            L.append(f'<p><b>{esc(horizon)}</b> &mdash; {esc(b.get("band"))}</p>')
            votes = b.get("votes") or b.get("components") or {}
            if isinstance(votes, dict) and votes:
                L.append('<table><tr><th>family</th><th>vote</th></tr>')
                for k, v in votes.items():
                    L.append(f'<tr><td>{esc(k)}</td><td>{esc(v)}</td></tr>')
                L.append('</table>')
        L.append('<p class="mute small">Kept generously and in full: it is too '
                 'early to know whether it works, and a vote deleted now cannot '
                 'be studied later.</p></div>')

    # ---- chart planes (§3.5) incl. the forming candle
    planes = (a.get("chart_planes") or {}).get("planes") or {}
    if planes:
        L.append('<div class="card"><h4>Chart planes</h4><table>'
                 '<tr><th>plane</th><th>default windows</th><th>forming candle</th></tr>')
        for p, b in planes.items():
            f = b.get("forming") or {}
            cell = "&mdash;"
            if f.get("available"):
                cell = (f'{chip("forming &mdash; drawn, greyed","warn")} '
                        f'O {num(f.get("open"))} H {num(f.get("high"))} '
                        f'L {num(f.get("low"))} C {num(f.get("close"))}')
            L.append(f'<tr><td>{esc(p)}</td>'
                     f'<td>{esc(", ".join(b.get("default_windows") or []))}</td>'
                     f'<td>{cell}</td></tr>')
        L.append('</table><p class="mute small">Value areas render as extended '
                 'horizontal bands. The forming candle is drawn and greyed so the '
                 'chart looks like the operator&rsquo;s &mdash; and appears in NO '
                 'computed value. Mid-week, the weekly RSI is last week&rsquo;s.'
                 '</p></div>')

    lat = a.get("lattice_12_25") or {}
    if lat.get("planes"):
        L.append('<div class="card"><h4>{12,25} lattice</h4><table>'
                 '<tr><th>plane</th><th>EMA12</th><th>EMA25</th><th>12&gt;25</th></tr>')
        for p, b in lat["planes"].items():
            if b.get("warming"):
                L.append(f'<tr class="mute"><td>{esc(p)}</td><td colspan="3">'
                         f'{chip("warming","warn")}</td></tr>')
                continue
            L.append(f'<tr><td>{esc(p)}</td><td>{num(b.get("ema12"))}</td>'
                     f'<td>{num(b.get("ema25"))}</td>'
                     f'<td>{"yes" if b.get("ema12_above_ema25") else "no"}</td></tr>')
        L.append('</table><p class="mute small">Display only. '
                 'No signal, no vote, no score contribution.</p></div>')
    return "\n".join(L)


# ══════════════════════════════════════════════════════════════ Part II

def part2_html(sym, a):
    L = []
    di = a.get("decision_instrument") or {}
    conf = a.get("confluence") or {}
    atr = a.get("daily_atr")

    # ---- confluence area map
    amap = di.get("confluence_area_map") or {}
    if amap:
        L.append('<div class="card"><h4>Confluence area map</h4>')
        for view, rows in amap.items():
            L.append(f'<p class="mute">{esc(view)}</p><table>'
                     '<tr><th>mean</th><th>score</th><th>families</th>'
                     '<th>members</th><th>scale confirmed</th></tr>')
            for r in rows[:8]:
                sc = ", ".join(r.get("scale_confirmed") or []) or "&mdash;"
                L.append(f'<tr><td>{num(r["mean"])}</td><td class="big">{r["score"]}</td>'
                         f'<td>{esc(", ".join(r.get("families") or []))}</td>'
                         f'<td>{r.get("member_count")}</td><td>{sc}</td></tr>')
            L.append('</table>')
        L.append('</div>')

    # ---- lines in the sand
    lines = di.get("lines_in_sand") or {}
    if lines:
        L.append('<div class="card"><h4>Lines in the sand</h4><table>'
                 '<tr><th>view</th><th>above</th><th>below</th></tr>')
        for view, ln in lines.items():
            ab = (ln or {}).get("above") or {}
            be = (ln or {}).get("below") or {}
            L.append(f'<tr><td>{esc(view)}</td>'
                     f'<td>{num(ab.get("mean"))} <span class="mute">score '
                     f'{ab.get("score","&mdash;")}</span></td>'
                     f'<td>{num(be.get("mean"))} <span class="mute">score '
                     f'{be.get("score","&mdash;")}</span></td></tr>')
        L.append('</table>')
        dif = di.get("lines_differ") or {}
        if dif.get("any_changed"):
            L.append('<p class="prose">Volume evidence <b>moves</b> a line here. '
                     'The two views are printed side by side so the move is '
                     'visible rather than argued.</p>')
        L.append('</div>')

    # ---- D.7.2 TARGET CLUSTERS, at any distance
    tc = target_clusters(conf, a.get("price"), atr)
    if tc["above"] or tc["below"]:
        L.append('<div class="card"><h4>Target clusters &mdash; highest scoring '
                 'beyond price, at any distance</h4><table>'
                 '<tr><th>side</th><th>mean</th><th>score</th><th>ATR away</th>'
                 '<th>families</th></tr>')
        for side in ("above", "below"):
            for c in tc[side][:4]:
                L.append(f'<tr><td>{side}</td><td>{num(c["mean"])}</td>'
                         f'<td class="big">{c["score"]}</td>'
                         f'<td>{num(c["atr_away"])}</td>'
                         f'<td>{esc(", ".join(c["families"]))}</td></tr>')
        L.append('</table><p class="mute small">A far cluster where a VWAP band, '
                 'a value-area edge and an SS level coincide is a higher-quality '
                 'target than a lone band. Distance is not quality &mdash; '
                 'composition is.</p></div>')

    # ---- R:R board, bucketed by target distance (D.7.1)
    for key, title in (("rr_ranking", "R:R board &mdash; with volume"),
                       ("rr_ranking_without_volume", "R:R board &mdash; without volume")):
        rr = di.get(key) or {}
        rows = list(rr.get("board") or [])
        for r in rows:
            if r.get("target") is not None and atr:
                r["target_atr"] = abs(r["target"] - r["entry"]) / atr
        buckets = bucket_board(rows)
        if not any(buckets.values()) and not rr.get("no_rr"):
            continue
        L.append(f'<div class="card"><h4>{title}</h4>')
        for bname, _, _ in TARGET_BUCKETS:
            brs = buckets[bname]
            if not brs:
                continue
            L.append(f'<p class="mute">{bname} targets</p><table>'
                     '<tr><th>side</th><th>entry</th><th>invalidation</th>'
                     '<th>target</th><th>R:R</th><th>inval ATR</th>'
                     '<th>target ATR</th><th></th></tr>')
            for r in brs:
                fl = chip("caution &mdash; tight stop", "warn") if r.get("caution") else ""
                L.append(f'<tr><td>{esc(r["side"])}</td><td>{num(r["entry"])}</td>'
                         f'<td>{num(r["invalidation"])}</td><td>{num(r["target"])}</td>'
                         f'<td class="big">{num(r["rr"])}</td>'
                         f'<td>{num(r.get("inval_atr"),3)}</td>'
                         f'<td>{num(r.get("target_atr"),2)}</td><td>{fl}</td></tr>')
            L.append('</table>')
        for n in (rr.get("no_rr") or []):
            L.append(f'<p class="prose">{esc(n["side"])} draft at '
                     f'{num(n["entry"])}: <b>no R:R printed</b> &mdash; {esc(n["reason"])}</p>')
        L.append('<p class="mute small">Ranked WITHIN distance buckets, never '
                 'globally: a distant target inflates R:R exactly as a knife-edge '
                 'stop does. This ranks structural quality, not probability.</p>'
                 '</div>')

    # ---- §5.2 REVERSION board, the second archetype
    rv = di.get("reversion_drafts") or {}
    rdrafts = rv.get("drafts") or []
    if rdrafts or rv.get("skipped_thin_sample"):
        L.append('<div class="card"><h4>Reversion drafts &mdash; entry at a band '
                 'price has REACHED, target the mean</h4>')
        if rdrafts:
            rbuckets = {b: [] for b, _, _ in TARGET_BUCKETS}
            for d in rdrafts:
                rbuckets[target_bucket(d.get("target_distance_atr")) or "FAR"].append(d)
            for bname, _, _ in TARGET_BUCKETS:
                brs = rbuckets[bname]
                if not brs:
                    continue
                L.append(f'<p class="mute">{bname} targets</p><table>'
                         '<tr><th>rank</th><th>side</th><th>anchor / window</th>'
                         '<th>band</th><th>entry</th><th>target (mean)</th>'
                         '<th>invalidation</th><th>R:R</th><th>&sigma; in ATR</th>'
                         '<th>age (bars)</th>'
                         '<th>target ATR</th><th>band score</th></tr>')
                for d in brs:
                    L.append(
                        f'<tr><td>{d.get("rank")}</td><td>{esc(d["side"])}</td>'
                        f'<td>{esc(d["name"])}</td><td>{esc(d["entry_band"])}</td>'
                        f'<td>{num(d["entry"])}</td><td>{num(d["target"])}</td>'
                        f'<td>{num(d["invalidation"])}</td>'
                        f'<td>{num(d["rr"])}</td>'
                        f'<td>{num(d.get("sigma_atr"))}</td>'
                        f'<td>{d.get("bars") if d.get("bars") is not None else "&mdash;"}</td>'
                        f'<td>{num(d.get("target_distance_atr"))}</td>'
                        f'<td class="big">{d.get("band_confluence_score")
                                           if d.get("band_confluence_score")
                                           is not None else "&mdash;"}</td></tr>')
                L.append('</table>')
        # ---- C6 item 3: THE HINGE. Both outcomes, no preference between them.
        if rdrafts:
            L.append('<p class="mute">the hinge &mdash; both outcomes at each '
                     'band, neither preferred</p><table>'
                     '<tr><th>draft</th><th>outcome</th><th>target</th>'
                     '<th>level</th><th>ATR away</th><th>R:R</th>'
                     '<th>rejection direction</th></tr>')
            for d in rdrafts:
                ta = d.get("target_a") or {}
                L.append(f'<tr><td>{esc(d["name"])} {esc(d["entry_band"])}</td>'
                         f'<td>{chip("A pullback","accent")}</td>'
                         f'<td>{esc(ta.get("label"))}</td>'
                         f'<td>{num(ta.get("target"))}</td>'
                         f'<td>{num(ta.get("distance_atr"))}</td>'
                         f'<td>{num(ta.get("rr"))}</td><td>&mdash;</td></tr>')
                for r in ((d.get("target_b") or {}).get("targets") or []):
                    L.append(f'<tr><td class="mute">&#8627;</td>'
                             f'<td>{chip("B rejection","warn")}</td>'
                             f'<td>{esc(r["label"])}</td>'
                             f'<td>{num(r["target"])}</td>'
                             f'<td>{num(r["distance_atr"])}</td>'
                             f'<td>{num(r["rr"])}</td>'
                             f'<td>{"yes" if r["in_rejection_direction"] else "no"}</td>'
                             f'</tr>')
            L.append('</table>'
                     '<p class="mute small"><b>A sigma band is a hinge with two '
                     'outcomes:</b> price pulls back to the mean (A), or the '
                     'level is genuinely rejected and price auctions toward the '
                     'dominant volume node and the far side of traded value (B). '
                     '<b>NO PREFERENCE IS EXPRESSED BETWEEN THEM.</b> Which one '
                     'occurs depends on how price is behaving at the level, and '
                     'these definitions carry into range detection &mdash; so '
                     'they are MEASURED before being set in stone. A '
                     'discrimination rule invented now would be a guess wearing '
                     'the clothes of a system.</p>')

        for s in (rv.get("skipped_thin_sample") or []):
            L.append(f'<p class="prose">{chip("skipped","warn")} '
                     f'{esc(s["name"])} &mdash; {esc(s["reason"])}</p>')
        L.append('<p class="mute small"><b>Ranked by the confluence score of the '
                 'BAND ITSELF, never by R:R.</b> Reversion R:R is a constant of '
                 'the geometry &mdash; a &sigma;2 entry is always 2:1 and a '
                 '&sigma;3 entry always 3:1 &mdash; so sorting by it would be '
                 'sorting by nothing. The band is already a registry member, so '
                 'its score is a lookup, not a new computation.</p>'
                 '<p class="mute small"><b>&sigma; in ATR is why identical '
                 'geometry is not an identical trade.</b> A 0.4-ATR &sigma; makes '
                 'a &sigma;2 reversion an 0.8-ATR day trade; an 11.4-ATR &sigma; '
                 'makes the same 2:1 setup a 22.8-ATR position held for months.</p>'
                 '<p class="mute small">Entry requires price to have ALREADY '
                 'REACHED the band and to be beyond it at the close. Nothing here '
                 'says price will return. Whether a band reversion pays anything '
                 'is H-VBR &mdash; census work under G-7, routed to APOLLO.</p>'
                 '</div>')

    # ---- drafts
    drafts = di.get("hypothesis_drafts") or []
    if drafts:
        L.append('<div class="card"><h4>Trade hypothesis drafts</h4>')
        for d in drafts:
            fl = chip("caution &mdash; tight stop", "warn") if not d.get("rankable") else ""
            L.append(f'<p class="prose">{chip("DRAFT","accent")} {fl} '
                     f'<b>If</b> {esc(d.get("if"))} <b>then</b> {esc(d.get("then"))}. '
                     f'<b>Invalidated if</b> {esc(d.get("invalidated_if"))}.</p>')
        L.append('<p class="mute small">Mechanically derived. No sizing, ever.</p></div>')

    # ---- composite bias
    cb = di.get("composite_bias") or {}
    if cb:
        L.append('<div class="card"><h4>Composite bias</h4>')
        L.append(f'<p class="big">{esc(cb.get("print"))} &mdash; '
                 f'<b>{esc(cb.get("band"))}</b></p><table>'
                 '<tr><th>family</th><th>vote</th><th>why</th></tr>')
        for k, v in (cb.get("votes") or {}).items():
            why = (cb.get("rationale") or {}).get(k, "")
            L.append(f'<tr><td>{esc(k)}</td><td class="big">{v:+d}</td>'
                     f'<td class="mute">{esc(why)}</td></tr>')
        L.append('</table>')
        if cb.get("compression_demoted"):
            L.append(f'<p>{chip("compression &mdash; band demoted one step","warn")}</p>')
        L.append('<p class="mute small">Equal weights, count-based, never fitted. '
                 'The bias print and the radar measure different things; when they '
                 'disagree nothing is reconciled.</p></div>')
    return "\n".join(L)


def target_clusters(conf, price, atr, top=6):
    """D.7.2 -- highest-scoring clusters beyond price, AT ANY DISTANCE.

    Deliberately unfiltered by distance.  The withdrawn +/-3 ATR admission filter
    judged levels by whether they could cluster NEAR price -- an entry-side test
    applied to targets, which are far from price by definition.  It would have
    capped every R:R by construction.  One sigma of BTC's 365d RVWAP is 11.4
    daily ATR: the far bands are structure, not ballast.
    """
    out = {"above": [], "below": []}
    v = (conf or {}).get("with_volume") or {}
    for c in (v.get("clusters") or []):
        m = c.get("mean")
        if m is None or price is None:
            continue
        row = {"mean": m, "score": c.get("score"),
               "families": c.get("families") or [],
               "atr_away": (abs(m - price) / atr) if atr else None,
               "member_count": c.get("member_count")}
        out["above" if m > price else "below"].append(row)
    for side in out:
        out[side].sort(key=lambda r: (-(r["score"] or 0), r["atr_away"] or 0))
        out[side] = out[side][:top]
    return out


# ══════════════════════════════════════════════════════════════ document

CSS = f"""
:root{{color-scheme:dark}}
body{{background:{PAL['ink']};color:{PAL['tx']};font:14px/1.55 -apple-system,
 Segoe UI,Roboto,sans-serif;margin:0;padding:24px}}
h1,h2,h3,h4{{margin:0 0 .5em;font-weight:600;letter-spacing:.01em}}
h1{{font-size:22px}} h2{{font-size:18px;color:{PAL['accent']};
 border-bottom:1px solid {PAL['rule']};padding-bottom:6px;margin-top:28px}}
h3{{font-size:16px;margin-top:20px}} h4{{font-size:13px;color:{PAL['mute']};
 text-transform:uppercase;letter-spacing:.06em}}
.card{{background:{PAL['panel']};border:1px solid {PAL['rule']};border-radius:8px;
 padding:14px 16px;margin:12px 0}}
table{{width:100%;border-collapse:collapse;margin:6px 0 2px}}
th{{text-align:left;font-weight:500;color:{PAL['mute']};font-size:11px;
 text-transform:uppercase;letter-spacing:.05em;padding:4px 8px 4px 0;
 border-bottom:1px solid {PAL['rule']}}}
td{{padding:4px 8px 4px 0;border-bottom:1px solid rgba(38,50,76,.5);
 font-variant-numeric:tabular-nums}}
tr.mute td{{color:{PAL['mute']}}}
.mute{{color:{PAL['mute']}}} .small{{font-size:12px}}
.big{{font-weight:600;font-size:15px}}
.prose{{margin:.5em 0;max-width:78ch}}
.chip{{display:inline-block;border:1px solid;border-radius:999px;
 padding:1px 8px;font-size:11px;margin-right:6px;white-space:nowrap}}
.banner{{background:{PAL['warn']};color:#1b1200;font-weight:700;padding:12px 16px;
 border-radius:8px;margin-bottom:18px;letter-spacing:.02em}}
.foot{{color:{PAL['mute']};font-size:12px;margin-top:28px;
 border-top:1px solid {PAL['rule']};padding-top:12px;max-width:90ch}}
"""


def render(doc, generated_utc=None):
    L = ['<!-- naiad brief-2 render -->', f'<style>{CSS}</style>']
    banner = doc.get("banner")
    if banner:
        L.append(f'<div class="banner">{esc(banner)}</div>')
    L.append(f'<h1>Naiad daily brief &mdash; {esc(doc.get("date"))} '
             f'<span class="mute">{esc(doc.get("slot"))}</span></h1>')
    L.append(f'<p class="mute small">rules {esc(doc.get("rules_version"))} '
             f'&middot; schema {esc(doc.get("schema_version"))} '
             f'&middot; analytics {esc(doc.get("analytics_version"))} '
             f'&middot; as of {esc(doc.get("as_of_utc"))} '
             f'&middot; rendered {esc(generated_utc or "&mdash;")}</p>')

    L.append('<h2>Part I &mdash; market monitor</h2>')
    L.append('<p class="mute small">What is the state of this market? Printed '
             'generously, for reading and judgement rather than for action.</p>')
    for sym, a in (doc.get("assets") or {}).items():
        L.append(part1_html(sym, a))

    L.append('<h2>Part II &mdash; decision instrument</h2>')
    L.append('<p class="mute small">Where would I act, and what would prove me '
             'wrong? Derived from Part I under the printed rules &mdash; every '
             'number below is reconstructable by hand from Part I.</p>')
    for sym, a in (doc.get("assets") or {}).items():
        L.append(f'<h3>{esc(sym)}</h3>')
        L.append(part2_html(sym, a))

    L.append(f'<div class="foot">{esc(doc.get("firewall",""))}<br><br>'
             'Confluence scores measure AGREEMENT BETWEEN TOOLS, not edge. '
             'R:R measures GEOMETRY, not probability. Whether any of it predicts '
             'anything is census work under G-7. No sizing, ever.</div>')
    return "\n".join(L)


def load_capture(date, slot, briefs_dir=BRIEFS):
    p = Path(briefs_dir) / f"brief_{date}_{slot}.json"
    if not p.exists():
        raise SystemExit(f"no capture at {p}")
    with p.open(encoding="utf-8") as fh:
        return json.load(fh)


def main():
    ap = argparse.ArgumentParser(description="Render a stored BRIEF-2 capture")
    ap.add_argument("--date", required=True)
    ap.add_argument("--slot", required=True)
    ap.add_argument("--out")
    args = ap.parse_args()

    from datetime import datetime, timezone
    doc = load_capture(args.date, args.slot)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    html_text = render(doc, generated_utc=stamp)

    out = Path(args.out) if args.out else (
        OUT_DIR / f"brief2_{args.date}_{args.slot}.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_text, encoding="utf-8", newline="\n")
    print(f"wrote {out}  ({out.stat().st_size:,} B)")
    if doc.get("banner"):
        print(f"\n  {doc['banner']}")


if __name__ == "__main__":
    main()
