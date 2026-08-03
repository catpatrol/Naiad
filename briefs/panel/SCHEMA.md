# `briefs/panel/` — SCHEMA

Amendment 2 §8.2. Every column, its units, its source layer, and the
`schema_version` in which it appeared.

**Layout — write-once daily partitions.**

```
briefs/panel/snapshots/YYYY-MM-DD.parquet
briefs/panel/levels/YYYY-MM-DD.parquet
briefs/panel/areas/YYYY-MM-DD.parquet
```

Each partition is **written once and never rewritten**. `brief_panel.py` refuses
to overwrite an existing partition unless `--force` is passed, and nothing in the
normal path passes it. Rationale: a rewritten monolithic parquet stores a
complete new blob in git every day, so growth *compounds*; write-once partitions
make it linear and additive. A silently-rewritable partition would also make an
archived file untrustworthy — a reader could not know whether the bytes on disk
are the bytes computed that day.

**Rebuild guarantee.** Every partition rebuilds from **captures alone**
(`briefs/brief_<date>_<slot>.json`). `brief_panel.py` never reads a previous
partition; if it did, one corrupted file would propagate forward and the
guarantee would be false.

**Consolidated view.** `briefs/panel/consolidated_*.parquet` is generated on
demand by `--consolidated`. It is **untracked and regenerable** — a convenience
for analysis, never a record.

**Grain.**

| table | grain |
|---|---|
| `snapshots` | `(asset, slot, date)` — exactly one row per asset per capture |
| `levels` | `(asset, slot, date, view, cluster_id, label)` |
| `areas` | `(asset, slot, date, kind, key)` |

`levels` and `areas` join back to `snapshots` on `(date, slot, asset)`.

---

## `snapshots` — one row per (asset, slot, date)

| column | type | units | source layer | since |
|---|---|---|---|---|
| `date` | str | `YYYY-MM-DD` | capture envelope | 2.0.0 |
| `slot` | str | `london` / `ny_am` / `post_ny` | capture envelope | 2.0.0 |
| `asset` | str | symbol | capture | 2.0.0 |
| `schema_version` | str | semver | envelope §8.1 | 2.0.0 |
| `rules_version` | str | semver | envelope §8.1 | 2.0.0 |
| `rules_sha256` | str | hex64 | envelope, canonical rule-set hash | 2.0.0 |
| `analytics_version` | str | semver | `analytics.ANALYTICS_VERSION` | 2.0.0 |
| `analytics_sha` | str | hex64 | `analytics.analytics_sha()` | 2.0.0 |
| `engine_version` | str | semver | `engine.version` | 2.0.0 |
| `as_of_utc` | str | ISO-8601 Z | capture; the decision bar | 2.0.0 |
| `parity_certified` | bool | — | envelope; **false until the operator's readings match** | 2.0.0 |
| `price` | float | quote ccy | last CLOSED 1h close | 2.0.0 |
| `daily_atr` | float | quote ccy | `volatility.atr(14)` on closed 1d | 2.0.0 |
| `level_count` | int | count | confluence registry, all families | 2.0.0 |
| `cluster_count_wv` | int | count | §5.4 with-volume view | 2.0.0 |
| `cluster_count_nv` | int | count | §5.4 without-volume view | 2.0.0 |
| `lis_above_wv` | float | quote ccy | line in the sand above, with volume | 2.0.0 |
| `lis_below_wv` | float | quote ccy | line in the sand below, with volume | 2.0.0 |
| `lis_above_nv` | float | quote ccy | line above, volume families excluded | 2.0.0 |
| `lis_below_nv` | float | quote ccy | line below, volume families excluded | 2.0.0 |
| `lines_differ` | bool | — | §9.2 item 6 — did volume evidence move the lines | 2.0.0 |
| `bias_band` | str | 5-band ordinal | §7.3 composite bias print | 2.0.0 |
| `bias_agree` | int | 0..5 | §7.3 "N of 5 agree" | 2.0.0 |
| `bias_total` | int | −5..+5 | §7.3 signed vote sum | 2.0.0 |
| `bias_dissenting` | str | comma-separated | §7.3 dissent, named | 2.0.0 |
| `compression_demoted` | bool | — | §7.3 band demoted one step toward neutral | 2.0.0 |
| `divergence_count` | int | count | §6.1 generalised divergences | 2.0.0 |
| `instability_chip` | bool | — | §5.2 sensitivity annex, top-3 changed | 2.0.0 |

> `lis_*_nv` may be null when the without-volume registry produces no cluster on
> that side. That is a real state, not a defect: it means the volume families
> were the *only* evidence on that side, which is precisely what §5.4 exists to
> make visible.

---

## `levels` — one row per scored cluster member

| column | type | units | source layer | since |
|---|---|---|---|---|
| `date`, `slot`, `asset` | str | — | grain | 2.0.0 |
| `view` | str | `with_volume` / `without_volume` | §5.4 dual scoring | 2.0.0 |
| `cluster_id` | int | index within view | `levels.cluster` | 2.0.0 |
| `cluster_mean` | float | quote ccy | cluster centre | 2.0.0 |
| `cluster_score` | int | count | §5.2 — capped members + distinct families | 2.0.0 |
| `family` | str | one of five | §5.1 | 2.0.0 |
| `label` | str | — | human-readable level name | 2.0.0 |
| `level` | float | quote ccy | the price | 2.0.0 |
| `source_layer` | str | — | which layer emitted it | 2.0.0 |
| `timeframe` | str | window / lens | §4.3 keys scale confirmation on this | 2.0.0 |
| `collapsed_count` | int | count | same-family levels merged at 0.02 ATR | 2.0.0 |
| `scale_confirmed` | str | comma-separated windows | §4.3 badge; **adds no score** | 2.0.0 |

`cluster_score` is **counted, never fitted**: `Σ over families of min(count, 3)`
plus the number of distinct families. F-B28 asserts no weight vector exists
anywhere in the scoring path.

---

## `areas` — value areas and nesting pairs

Two `kind`s share one table because both describe *where value is*, and keeping
them joinable on the same grain is what lets a query ask "where was price
relative to value" without a second join.

| column | type | units | source layer | since |
|---|---|---|---|---|
| `date`, `slot`, `asset` | str | — | grain | 2.0.0 |
| `kind` | str | `window` / `nesting_pair` | — | 2.0.0 |
| `key` | str | window name, or `7d<->30d` | — | 2.0.0 |
| `warming` | bool | — | §3.2 warm-up honesty | 2.0.0 |
| `poc` | float | quote ccy | §3.3 windowed profile | 2.0.0 |
| `vah` | float | quote ccy | §3.3, 70% value area | 2.0.0 |
| `val` | float | quote ccy | §3.3, 70% value area | 2.0.0 |
| `lvn_count` | int | count | §3.4 low-volume nodes | 2.0.0 |
| `substrate` | str | `1m`/`5m`/`15m` | §3.3 — **the substrate ACTUALLY used** | 2.0.0 |
| `bars` | int | count | bars in the window | 2.0.0 |
| `lockbox_overlap_days` | float | days | disclosure; see below | 2.0.0 |
| `state` | str | five states | §4.1 nesting | 2.0.0 |
| `overlap_frac` | float | 0..1 of the **SHORTER** VA | §4.1 | 2.0.0 |
| `consensus_low` / `consensus_high` | float | quote ccy | §4.1 consensus band | 2.0.0 |
| `gap_low` / `gap_high` | float | quote ccy | §4.1 gap band when disjoint | 2.0.0 |
| `price_location` | str | 5 values | §4.1 | 2.0.0 |

`window` rows populate the profile columns and leave the nesting columns null;
`nesting_pair` rows do the reverse.

**`warming` means NO NUMBER, not a substituted one.** A 365d profile computed on
200 days is a 200-day profile wearing the wrong label, so `poc/vah/val` are null
whenever `warming` is true. As of 2026-08-03 this affects `LITUSDT` at 365d only
(222.4 days of history).

**`lockbox_overlap_days`** is a disclosure, never a refusal. Operator ruling
2026-08-03: the sealed lockbox `[2024-07-01, 2025-10-06)` governs **scored
outcome evidence**, not raw price inside a display-only trailing window. Measured
on 2026-08-03: the 365d window overlaps by **64.115 days**, self-clearing
2026-10-06; 7/30/90d are **0.0**.

---

## Measured storage — fact replacing the §8.2 estimate

Measured 2026-08-03, ten assets, one slot:

| | bytes |
|---|---|
| capture JSON, one slot | 794,451 |
| `snapshots` partition | 17,104 |
| `levels` partition | 19,164 |
| `areas` partition | 13,597 |
| **partitions, per day** | **49,865** |

Projected annual, three slots/day: **captures ~870 MB + partitions ~18 MB ≈
888 MB/yr**.

§8.2 estimated ~150–250 MB/year and asked that measurement replace the estimate.
It does: **the partition design worked (18 MB/yr, linear and additive) but the
tracked captures are ~3.5× the whole estimate on their own.** The cause is
identified and is not the panel: `levels.dual_score` stores the collapsed
registry **twice** per view — once flat as `members`, once nested inside each
`clusters[].members` — which is ~10 KB of every ~56 KB asset block. Removing the
redundancy is a schema change to `dual_score`'s output contract (F-B27 asserts
`members` is present), so it is **reported, not applied unilaterally**.
