# BUILDERS REPORT — HEPHAESTUS · SAIL PROGRAMME, STEP 1
## The Prometheus inventory (BRIEF §2) — read-only census, verdict, and secrets disposition

**Lane:** HEPHAESTUS, executing under ATHENA custody · **Commissioning brief:**
`exchange/reports/BRIEF_ATHENA_SAIL_REPO_2026-08-17.md` (APOLLO, 2026-08-17)
**Operator go:** 2026-08-17 · **Executed:** 2026-08-18 00:40–02:00 local (the session ran past
midnight; the filename carries the commissioned date, the clock carries the truth — §6.1)
**Scope:** BRIEF §2 only — the read-only inventory that decides *retrofit Prometheus* vs
*found `naiad-sail`*. **NOTHING WAS BUILT.** No skeleton, no adapter, no scaffold.

> **PROMETHEUS WAS NOT TOUCHED.** No commit, no branch, no file created, modified or deleted in
> it, and no push — this session or ever, until a disposition is ratified. The census ran against
> a quarantine clone at `~/prometheus-inventory` whose push URL was deliberately broken
> (`git remote set-url --push origin DISABLED_READ_ONLY_INVENTORY`) before any agent read a byte.
> Every branch other than `main` was read with `git show <ref>:<path>` and `git ls-tree -r <ref>`;
> **no branch was ever checked out.**

---

## 0 · THE ANSWER, IN ONE BOX

| BRIEF §2 question | verdict | decisive citation |
|---|---|---|
| **(a)** Clean strategy entry-point, or a surface a thin adapter can wrap without touching internals? | **NO** | `src/prometheus/config.py:353-357` — the config loader *raises* on any key it does not already declare; `src/prometheus/replay.py:283` `_lifecycle` — private, no callable parameter, every manage/exit rule inlined at `:347-407` |
| **(b)** Feed covers {BTC,ETH,SOL,NEAR,ZEC}USDT.P at **4h+1h** with a **stated gap policy**? | **NO** | `src/prometheus/data/resample.py:119-121` + `src/prometheus/config.py:29` — 4h raises `ValueError` before a single bar is evaluated; no ingestion gap policy exists on any live path |
| **(c)** Weekly report generator that **accepts a template**? | **NO** (generator YES, template NO) | `src/prometheus/harness/report.py:443` `return _TEMPLATE.replace("__DATA_JSON__", …)` against a hardcoded 871-line raw string at `:452-1322` |
| **(d)** Secrets, working tree **and full history** | **CLEAN** | 420 commits · 4,307 blobs · 193 unique paths ever · **zero** credential-shaped filenames, **zero** env-read sites, ever |

**THE BRIEF'S RULE, APPLIED MECHANICALLY.** BRIEF §2: *"Three yes → retrofit. Any no → found
`naiad-sail`."* Three of three are NO — not marginally, and not one of them rescuable by
configuration. **→ FOUND `naiad-sail`.** The lift-by-copy list is §7.

**And the lean is not close.** BRIEF §2 closes *"do not fight a resistant engine for sentiment's
sake."* Prometheus is not merely resistant; it is a repo whose own pre-registered out-of-sample
batch returned **NO-GO twice** (§5.4) and whose live forward paper record is **negative** (§5.5).
Retrofitting it would inherit a rejected engine to host a card that has not been tested against it.

---

## 1 · LOCATING PROMETHEUS — enumerated, never assumed

The brief's reviewer is told to treat the repo as terra incognita. So is this report: nothing
below rests on prior knowledge of Prometheus.

**(a) Local candidates — NONE.** `ls -la ~` top level: 28 entries, no `prometheus` in any case.
`find ~ -maxdepth 4 -iname "*prometheus*"` returns **exactly three files, all documents inside
Naiad itself, none of them a repo**:

| path | lines | what it is |
|---|---|---|
| `~/Naiad/Prometheus_Paper_Analysis_Week1.md` | 570 | Fable-mode analysis of the first paper week |
| `~/Naiad/Prometheus_Stop_Loss_Logic_Learnings.md` | 261 | transferable exit-design conclusions |
| `~/Naiad/Prometheus_Data_Collection_Design.md` | 327 | Phase 6.0 instrumentation build spec |

`/Volumes` holds only `Macintosh HD → /`. **`/Volumes/LaCie` is NOT MOUNTED** — `ls: No such file
or directory`. Per §2.1 the LaCie is backup-only and reads never touch it in normal work, so its
absence blocks nothing here; it is stated because §6 invariant 6 requires enumeration, not a
single lookup.

**(b) Remote — FOUND, exact name, first try.** `ssh -T git@github.com` →
`Hi catpatrol! You've successfully authenticated`. Then:

    git ls-remote git@github.com:catpatrol/prometheus.git   → EXIT 0, 18 refs

No variant was guessed into existence and no HALT-SOFT was needed.

**(c) Quarantine clone.** `git clone --no-checkout … ~/prometheus-inventory`, then `checkout main`,
then push disabled. The name is deliberately **not** `~/naiad-sail` — that name stays reserved for
the ratified home. **The clone is outside `~/Naiad` and outside every sync tree; it is not backed
up and is not meant to be.** It is a disposable read surface: delete and re-clone at will.

---

## 2 · THE GENERAL CENSUS

| fact | value | how measured |
|---|---|---|
| Language | **Python only** | 42 `.py` files, 9,394 LOC on `main` |
| — split | src 24 files / 6,650 LOC · tests 17 files / ~2,744 LOC | `wc -l` |
| Dependency manifest | **`pyproject.toml` only** — `prometheus-agent` 0.1.0, `requires-python >=3.11` | deps: `httpx`, `pandas`, `numpy`, `pyyaml`, `pyarrow`; dev: `pytest>=8.0` |
| — absent | no `requirements.txt`, `setup.py`, `setup.cfg`, `poetry.lock`, `Pipfile` | `git ls-files`, no hit |
| Total size | **12 MB** working tree · **7.4 MB** `.git` | `du -sh` |
| File count | **111 tracked** on `main` (largest tree is `phase-5-birth-on` at 150) | `git ls-files \| wc -l` |
| Last commit | **`b4d11e6` · 2026-07-08 · "Update paper.yml"** | `git log -1` |
| Commits | **420** across all refs; `main` alone has **20** | `git rev-list --all --count` |
| Branches | **8** (1 local + 7 remote, `origin/HEAD → origin/main`) | `git branch -a` |
| Remotes | **`origin` only** — fetch = the SSH URL, push = `DISABLED_READ_ONLY_INVENTORY` (set by us) | `git remote -v` |
| Test suite | **16 modules + `conftest.py`, 131 test functions, 2,326 lines — fully OFFLINE** | see below |
| CI | **one workflow, and it is not a test pipeline** — `.github/workflows/paper.yml` | see §5.3 |

**File types on `main`:** 44 `.csv` · 42 `.py` · 9 `.md` · 3 `.html` · 2 `.yaml` · 2 `.txt` ·
2 `.gz` · 1 each `.yml .typed .toml .pine .htm .css .gitignore`.

**The test suite runs offline, and that is proven three ways rather than asserted** — (1)
`tests/conftest.py:1` *"The suite never touches the network (§3.4/§7.1)"*; (2) the only
HTTP-touching module injects a mock: `tests/test_data_layer.py:42-43`
`httpx.Client(transport=httpx.MockTransport(handler), base_url="https://mock")`; (3)
`grep -rn "parametrize\|pytest.mark\|skipif\|pytest.skip" tests/` returns **no hit** — no case
multiplication, no skips, no conditional exclusions. Every test is unconditional.
*(The suite was NOT executed — running `pytest` would write `.pytest_cache/` into a read-only
tree. Read, not run.)*

### 2.1 Largest ten files

| bytes | path | what it is |
|---:|---|---|
| 1,139,796 | `reports/binance_BTCUSDT_5m_20260526-20260609_developing/report.html` | committed Phase 1+2 study report |
| 514,176 | `docs/reference/SS___Breakout_Scanner___v2.htm` | browser-saved TradingView spec page |
| 501,193 | `reports/phase3b_exit_race_…/report.html` | Phase 3b exit horse-race report |
| 135,571 | `tests/fixtures/btcusdt_5m_study.csv.gz` | real Binance 5m candles, 7,320 rows |
| 128,545 | `tests/fixtures/btcusdt_5m_windowB.csv.gz` | real Binance 5m candles, 7,032 rows |
| 106,207 | `reports/phase3_replay_20260526-20260609/report.html` | Phase 3 four-arm replay report |
| 72,082 | `reports/…_developing/golden_sample.csv` | TradingView parity sheet, 484 rows |
| 61,464 | `reports/phase3b_…/journal_E-gated_X3_A.csv` | one of 36 exit-race journals |
| 61,351 | `reports/phase3b_…/journal_E-raw_X4_A.csv` | exit-race journal |
| 61,308 | `reports/phase3b_…/journal_E-raw_X3_A.csv` | exit-race journal |

**Reading:** the repo's weight is *committed study output*, not code. The top three files alone are
2.15 MB of 12 MB. Note for §4 residency if any of this is ever lifted: these are data, and
Invariant 3 says data does not enter `exchange/`.

### 2.2 README claims vs contents

| README claim | verdict | evidence |
|---|---|---|
| Title *"Phases 1 & 2"* (`README.md:1`) | **CONTRADICTED by its own body** | it documents Phase 3 (`:151-163`) and 3b (`:165-176`); the tree carries `replay.py`, `exit_race.py`, `docs/build_notes/phase3{,b}_notes.md`. It undersells by two phases. |
| Phase 1 = v10 Pine port + trend-health + harness (`:3-8`) | **CONFIRMED** | `skills/regime_ribbon.py`, `pyramid_signals.py`, `trend_health.py`, `harness/report.py`, each with a dedicated test module |
| Phase 2 = structure + SFP + Wyckoff + birth filter (`:8-13`) | **CONFIRMED** | `skills/structure.py`, `sfp_engine.py`, `wyckoff.py`, `birth_filter.py`, each tested |
| *"Nothing here trades. There are no API keys, no orders, no positions"* (`:15-16`) | **CONFIRMED as written · OVERSTATED as impression** | true of the `main` source tree. But `.github/workflows/paper.yml` — committed on `main` — runs an hourly agent out of this repo that has written **393 ticks through 2026-08-18** (§5.3). A reader taking `:15-16` at face value would not know a live agent is running. |
| *"writes two files into `runs/reports/`"* (`:56`) | **CONTRADICTED by the next four lines** | `:58,:65,:67,:69` then enumerate **four** files. The four-file version matches the tree. |
| Every documented CLI flag exists | **CONFIRMED** | `README.md:50-51,77,84,85,87,190` ↔ `harness/__main__.py:65-79` |
| 1,500 warm-up bars enforced (`:54`) | **CONFIRMED and enforced** | `harness/__main__.py:37` `MIN_WARMUP = 1500  # §3.3 — non-negotiable`, with a hard `SystemExit` |

---

## 3 · (a) THE ENGINE SEAM — **NO**

### 3.1 The verdict, and what carries it

There is **no strategy interface of any kind** in this repository. The negative was established by
enumeration, then independently reproduced by an adversarial verifier:

    grep -rnE 'Protocol|abstractmethod|ABC\b|register|registry|plugin|entry_point|entrypoint|
               importlib|getattr\(|dispatch|Callable|strategy_class|hook' src/ config/ pyproject.toml

returns **exactly four lines**: `skills/wyckoff.py:29` and `skills/sfp_engine.py:162` (the English
word *"registered"*), and `data/cache.py:11` and `:33`. A broader independent sweep for
`__call__|functools|partial(|setattr(|globals()|eval(|exec(|import_module|__subclasses__|singledispatch`
over `src/` returns **zero**. `pyproject.toml` is 26 lines with **no `[project.entry-points]`**.
All **43 classes** in `src/` are `@dataclass`. Docs grep for
`pluggable|plugin|seam|adapter|strategy card|registry|interface`: **zero hits**.

**The single `Callable` in the entire source tree is `data/cache.py:33`** —
`get_or_fetch(…, fetch_fn: Callable[[], pd.DataFrame], …)`. It is a genuine seam, and it injects
a **data source**, not a strategy (used that way at `harness/__main__.py:60`, `replay.py:644`,
`exit_race.py:45`).

**The config route is actively closed, by design.** `config.py:353-357` `_build` raises
`ValueError` on any YAML key not already declared as a dataclass field, and five mode-string fields
raise on unknown *values* — `htf_gate.mode` (`:52-56`), `structure.method` (`:100-102`),
`admission.mode` (`:213-215`), `sfp_linkage.mode` (`:226-228`), `base_cover_mode` (`:245-247`).
**You cannot introduce a new gate name, admission mode, exit stack or entry set from outside the
package.** Config is a closed vocabulary of tuned constants, not an extension point.

**The repo's own history proves it.** Phase 5 needed *one* new entry set and *one* new admission
gate. Neither could be added from outside; both required editing `src/`:

- `git diff main origin/phase-5-birth-on` — `replay.py:32-36` introduces a `RUN_SETS` dict and
  changes the lookup (`:604` on main → `:609` on phase-5).
- same diff — `birth_filter.py:318-327` inserts an `over_extended` reject block **inside** the FSM
  loop, plus a new `birth_sep_atr_max` field at `config.py:162`.

### 3.2 Where the brain lives — five sites, none behind an interface

| # | site | why it blocks a seam |
|---|---|---|
| 1 | `skills/pyramid_signals.py:64`, loop `:242-393` | declared verbatim port of a Pine script (`:1-16`). Computes indicators **and** trade primitives in one statement sequence — retest grades `:254-257`, filters `:260-268`, band retest `:276-291`, capitulation `:294-295`, ratchet stops `:303-312`, R1 `:315-318`, X-failure `:321-329`. **There is no line at which "indicator" ends and "signal" begins.** |
| 2 | `skills/birth_filter.py:157` `run_birth_filter` | ~300 lines, nine data arguments, **zero callables**; trigger enumeration, FSM, grading and both candidate stops inlined `:251-453`. Its output object *is also the journal schema* (`:21-22`) — brain and reporting share one structure by design. |
| 3 | `replay.py:190` `build_entries` | dispatched on four literal strings (`:213`, `:232`) |
| 4 | `replay.py:283` `_lifecycle` | private; every manage/exit rule inlined `:347-407`; **and it also contains the fill model** (next-bar-open `:319-322`, stop/gap `:349-352`) **and the measurement** (MFE/MAE `:354-364`, R `:409`). You cannot take the fill model without the exit rules. |
| 5 | `replay.py:416` `simulate_arm` | sizing `:440-442`, leverage ceiling `:485-498`, concurrency `:469-473` and the journal row `:444-462` all interleaved |

**The crux, stated plainly:** BRIEF §2's retrofit option is *"gut the strategy layer, keep the
plumbing."* That is **not achievable by subtraction here**, because the plumbing that would survive
— `_lifecycle` — is itself parameterised by the brain you deleted. Its exit behaviour is a function
of columns produced by site 1 (`fail_long`, `bull_cross`, `is_r1_long`, `stop_long`) and by
`trend_health` (`transition_event == "health_degraded"`, `:387`).

**What IS cleanly separated** — and this is the only real boundary in the repo — is the data layer
(`data/binance.py`, `data/hyperliquid.py`, `data/resample.py`, `data/cache.py`) and `indicators.py`.
They hold zero strategy and import nothing from `skills/` or `replay`.

### 3.3 The adversarial correction — recorded, because it sharpens the lift list

A verifier was tasked to **refute** the (a) finding. It **confirmed the headline** ("I could not
break it: there is no Protocol, ABC, registry, plugin, entry-point, importlib, dispatch table or
strategy callable anywhere") and confirmed ~90 citations at the exact line. It **refuted the
adapter assessment layered on top**, and the correction is material enough to carry:

> **WRONG AS FIRST STATED:** *"a thin adapter can implement at most ONE of the four hooks and
> would have to edit `src/prometheus/` for the other three."*
>
> **CORRECTED:** an adapter can implement **enter** fully, and can **re-aim all four existing
> manage/exit rules** by supplying its own `stop_long`/`stop_short`, `fail_long`/`fail_short`,
> `bull_cross`/`bear_cross`, `e200` and `health` arrays on a caller-built `PipelineResult`, plus a
> caller-built `ExitStack` — **with no edits.** `ExitStack` (`replay.py:34-51`) is a public frozen
> dataclass with **no `__post_init__` and no validation**; `exit_stacks()` (`:54-65`) is a
> convenience factory, not a gate, and only `stack.id` is ever checked (cosmetically, `:437`,
> `:463`). The repo's own test does the injection: `tests/test_phase3b_fixtures.py:180-182` builds
> a synthetic `EntrySignal` with a caller-chosen stop and passes it into `simulate_arm`.
>
> **What remains impossible without editing `src/prometheus/`:** a rule of a **new shape**
> (scale-out, time-stop, pyramiding, multi-leg — the loop breaks once and `ReplayTrade` `:86-142`
> is a single-exit row), the next-bar-open fill (`:319-322`), the gap-through model (`:349-352`),
> and any new admission predicate (`ModeRule`'s four fixed fields, `config.py:164-170`).

**Why the answer is still NO, with the correction fully accepted.** BRIEF §1 is the law: *SAIL is a
body, never a brain; it imports the ratified card and executes it; if a rule cannot be imported,
the trade does not exist.* Re-aiming Prometheus's four **fixed rule shapes** by forging its column
vocabulary means the card must be expressible in Prometheus's shapes — **the body would constrain
the brain**, which inverts §1. And per §7's acceptance grep, every one of those inlined
conditionals at `replay.py:347-407` is *"a strategy conditional outside the imported spec"* — i.e.
a retrofit ships pre-loaded with the exact defect the acceptance test exists to catch.

**But the correction changes §7's lift list**, and that is why it is here: `simulate_arm` +
`EntrySignal` + `ExitStack` are a **more valuable copy target** than the first pass credited.

---

## 4 · (b) THE DATA FEED — **NO**

### 4.1 Venue — correct market, and this was the detail most likely to be got wrong

**It is perpetuals, not spot.** `src/prometheus/data/binance.py:20-21`:

    BASE_URL   = "https://fapi.binance.com"
    KLINES_PATH = "/fapi/v1/klines"

`fapi` is the USD-M futures endpoint — the right market for a `.P` panel. Corroborated by
`README.md:25-27`: *"Use the chart `BINANCE:BTCUSDT.P` (Binance perpetual) — not Bybit, not spot."*
`api.binance.com` is **ABSENT** across all 7 branches. *(Honest correction from the verifier: a
Binance **spot** URL does exist in the repo — `docs/reference/SS___Breakout_Scanner___v2.htm:1029`
`https://data-api.binance.vision/api/v3` — but it is inside a saved-browser reference artifact that
**no `src/` module ever reads**. The panel verdict is unaffected; the first pass's blanket "appears
nowhere" was false and is corrected here rather than quietly dropped.)*

Three venue clients exist: **Binance USD-M REST** (live, three call sites — `harness/__main__.py:60`,
`exit_race.py:47`, `replay.py:646`), **Binance Vision archive CDN** (`binance_archive.py:36-37`,
branch-only, SHA-256-verifies every zip against its published `.CHECKSUM`), and **Hyperliquid**
(`hyperliquid.py:22-23`, used only as an optional volume overlay, swallowed on failure at
`harness/__main__.py:157`).

### 4.2 The panel — reachable, but nothing is as-is

| symbol | status | binding citation |
|---|---|---|
| BTCUSDT.P | **WITH-CONFIG** | the default: `harness/__main__.py:66`, `config/strategy_params.yaml:196` |
| ETHUSDT.P | **WITH-CONFIG** | `[phase-5-birth-on] oos_batch.py:40` `TIER1` |
| SOLUSDT.P | **WITH-CONFIG** | `[phase-5-birth-on] oos_batch.py:40` `TIER1` |
| NEARUSDT.P | **WITH-CONFIG** | `[phase-5-birth-on] oos_batch.py:40` `TIER1` |
| ZECUSDT.P | **WITH-CONFIG**, *and walled off* | `[phase-5-birth-on] oos_batch.py:41` `TIER2` = "EXPLORATORY only"; `docs/build_notes/phase4_notes.md:184-187` *"walled off — NOT in either verdict … Excluded from every go/no-go number by construction"* |

`--symbol` is free-form (`harness/__main__.py:66`, no `choices=`) and flows unchecked into the fapi
query at `binance.py:64`. **The universe constraint is not the fetcher; it is everything downstream**
— and the two files that enumerate a universe at all (`oos_batch.py`, `phase4_notes.md`) are
**branch-only and absent from `main`**.

### 4.3 The 4h blocker — the finding that decides (b)

Eleven intervals are whitelisted at the fetch layer (`resample.py:25-37`, `1m`…`1d`). **Only six
survive the pipeline with the shipped config.** `resample.py:119-121` (and identically `:56-58`):

    lms, hms = interval_ms(ltf_interval), interval_ms(htf_interval)
    if hms % lms != 0:
        raise ValueError(f"{htf_interval} is not a multiple of {ltf_interval}")

With `config.py:29 tf_govern = "1h"` and `config.py:128 wyckoff_tf = "1h"`, this admits exactly the
**divisors of 1h** — `1m, 3m, 5m, 15m, 30m, 1h` — and raises for **2h, 4h, 6h, 12h and 1d alike**.
For `--tf 4h`: `3,600,000 % 14,400,000 = 3,600,000 ≠ 0` → `ValueError` thrown at `pipeline.py:93`
**before a single bar is evaluated**, uncaught at `harness/__main__.py:138-140`.

**`--tf 1h` passes** — but the HTF gate then collapses onto the execution timeframe, which is not
what the gate was built to express. Making 4h work means raising `tf_govern`
(`config/strategy_params.yaml:24`) and `wyckoff_tf` (`:104`) to 4h/12h/1d — **a strategy-semantics
change, not a knob**, and therefore exactly the kind of change SAIL's card-spec is supposed to own.

> *Correction carried from the verifier:* the first pass headlined *"eleven intervals reachable"*
> and named only 4h as blocked. An operator reading that would believe eleven work. **Six work;
> five are blocked.** Corrected above rather than annotated, per §0.

### 4.4 Gap policy — **SPLIT, and absent where it counts**

**STATED — on the archive/OOS path only, and that path is branch-only.**
`[phase-5-birth-on] data/binance_archive.py:249-254`:

    def assert_gapless(df, tf, start_ms, end_ms) -> GapReport:
        """Check that ``df`` covers ``[start_ms, end_ms)`` with no interior gaps.
        A window that fails is dropped and recorded by the caller, never
        interpolated (Phase 4 §2.2)."""

Enforced at `oos_batch.py:206-213`; documented at `phase4_notes.md:57-58`; tested at
`tests/test_phase4_oos.py:114-121`; **and observed in the committed data** —
`reports/phase4_oos_batch_20260525_76mo/cells_summary.csv` carries 12 `gap(` drops across
NEAR/SOL/ZEC. The policy is: **DETECT → DROP THE WHOLE WINDOW → RECORD.** Never forward-fill,
never interpolate, never halt. *It is a good policy, and it is worth lifting (§7).*

**ABSENT — on `origin/main`, and on every LIVE fetch path on every branch.** `binance.py` (121
lines), `hyperliquid.py` (113) and `cache.py` (43) contain **no gap detection at all**; they do only
`drop_duplicates("open_time").sort_values("open_time")` (`binance.py:102-104`,
`hyperliquid.py:93-95`). **A missing candle passes through silently.** `harness/__main__.py:122-128`
checks only warm-up *count*, which a gapped series can satisfy. `main`'s only ingestion-integrity
rule is the closed-bar guard (`binance.py:88-89` `if close_time >= now: continue`).
Searched for a stated policy across `src/`, both configs, `docs/`, `docs/build_notes/`, `README.md`
and `tests/` on main — the one gap test that exists, `tests/test_gate_resample.py:94-103`
(*"drop all of hour 3 — exchange outage"*), covers **the resampler, not ingestion**.

**Net for (b):** the venue is right and the symbols are reachable, but **4h is unreachable without a
strategy-semantics edit, and the live path has no gap policy at all.** The brief asks one compound
question and the answer to it is NO.

---

## 5 · (c) REPORTING — generator **YES**, template **NO**

### 5.1 The mechanism

Every report in this repo is a **module-level Python raw string** with **one placeholder**,
substituted by a single `str.replace`. There is no template engine, no template file, and no
template parameter anywhere.

    src/prometheus/harness/report.py:441   def build_html(payload: dict[str, Any]) -> str:
    src/prometheus/harness/report.py:443   return _TEMPLATE.replace("__DATA_JSON__", json.dumps(payload, …))
    src/prometheus/harness/report.py:452   _TEMPLATE = r"""<!DOCTYPE html>          ← runs to :1322

That is **871 of the file's 1,322 lines — 66% of the module is literal HTML/CSS/JS.** The signature
takes **only the data payload**: no template argument, no path, no loader. The same pattern repeats
in `replay_report.py:109/:112` (206-line template) and `exit_race_report.py:56/:59` (229 lines),
and five more times on `phase-5-birth-on` (`oos_report.py`, `autopsy_report.py`, `paper_report.py`,
`birth_on_report.py` ×2 with a `_CSS` string joined by `+`). **Eight top-level markup strings across
the branch set.**

**No templating library — confirmed twice.** `pyproject.toml:10-16` lists five runtime deps and
none is a template engine; a grep for
`jinja|mako|chevron|mustache|FileSystemLoader|render_template|string\.Template|Environment\(|template_dir`
across `*.py/*.toml/*.cfg/*.txt/*.yaml/*.yml` returns **zero hits on `main` and zero across the
whole of `phase-5-birth-on`**.

**The strongest single check, and the verifier ran it rather than the census:** enumerate every
non-`.py` file under `src/` on **all eight remote branches** —

    for b in $(git branch -r | grep -v HEAD); do git ls-tree -r --name-only $b -- src | grep -viE '\.py$|py\.typed'; done

**empty on every branch.** There is no `.html`, `.css`, `.j2` or `.tpl` inside the package
anywhere. **Nothing template-shaped is packaged at all** — a loader would have nothing to load.

**No CLI seam:** `harness/__main__.py:65-80` enumerates all twelve flags. There is no `--template`,
`--html`, `--css` or `--layout`. The only path-taking flag is `--config`, an alternate
`strategy_params.yaml`.

**What IS injectable is the palette, and only the palette:** eleven colour knobs
(`config/strategy_params.yaml:138-152` → `config.py:307 HarnessColors` → `report.py:437`). Structure
is literal: `report.py:517` is a hardcoded `<details>` element, and the funnel is **19 hardcoded
stage labels** in the list at `report.py:156-176`.

**Input-vs-output was checked and not confused.** The three `reports/*/report.html` are **outputs**
(written at `exit_race.py:206`, `replay.py:660`, `harness/__main__.py:177`). The one `.htm` in the
tree is a saved TradingView spec page referenced only in prose (`skills/structure.py:4`,
`strategy_params.yaml:67`); **no code path opens it.**

### 5.2 Cadence — there is no weekly anything

BRIEF §5 wants a **weekly** yardstick report. Prometheus has no weekly cadence in code. It has:
**ad-hoc study windows** (`--start/--end/--last-days`, `harness/__main__.py:68-70`; every committed
report folder is a named window) and **one hourly tick loop** (`paper.yml:4-5`) whose design cadence
is actually 5-minutely (`paper_live.py:6-8`; `deploy/paper-agent.cron` = `*/5 * * * *`). **No
generator has a "since last report" concept, a period-over-period comparison, or date-rolling.**

**Verifier verdict on (c): NOT REFUTED — confirmed at high confidence.** It corrected six
supporting line numbers (e.g. `report.py:437` not `:438`; `:587` not `:617`; `replay.py:660` on main
not `:665`, which was a phase-5 line number mixed into a main-branch citation). **None touched a
decisive line**, and the corrected numbers are the ones printed above.

### 5.3 The fact that outranks the rest of §5 — **the agent is still running**

`.github/workflows/paper.yml` is committed on `main`, 61 lines:

- `schedule: - cron: "0 * * * *"` (`:3-5`) — **top of every hour**, plus `workflow_dispatch`.
- `permissions: contents: write` (`:8-9`) — *"lets the job save the journal back to the repo."*
- `actions/checkout@v4` **with `ref: phase-5-birth-on`** (`:20-22`) — **the workflow lives on `main`
  but deliberately runs code from an unmerged branch.** `main` does not contain the module it
  invokes: `src/prometheus/paper_live.py` exists **only** on `phase-5-birth-on`.
- runs `python -m prometheus.paper_live --coins BTC,ETH,SOL --start 2026-07-08T00:00:00Z` (`:49-52`),
  then commits the journal to the orphan `paper-data` branch (`:54-61`).

**It has not stopped. `origin/paper-data`'s tip is `f6609fd`, "paper tick 2026-08-18 03:36:04 UTC" —
today.** This is a live, unattended, self-committing process running out of a repo the estate is
about to rule on. It is named here as a **finding reported-not-fixed** (§8, item 1): stopping it is
a write to Prometheus, and Prometheus is read-only until the operator rules.

### 5.4 The branch map — and the verdict buried in it

| branch | ahead/behind `main` | files | what it holds |
|---|---|---|---|
| `claude/prometheus-phase1-build-8rxbnj` | 0 / 10 | 57 | **nothing unique** — merged via PR #1, #2 |
| `phase-3-replay` | 0 / 8 | 68 | **nothing unique** — merged via PR #3 |
| `phase-3b-exits` | 0 / 6 | 110 | **exactly `main` minus `paper.yml`** — merged via PR #4 |
| `phase-4-oos-batch` | 6 / 5 | 131 | **NOT merged.** OOS batch + `binance_archive.py` + `oos_report.py` |
| `phase-4b-birth-autopsy` | 6 / 4 | 131 | **identical tree to phase-4** (`git diff` → empty) |
| `phase-5-birth-on` | 6 / 6 | **150 — the largest tree, and the code CI actually runs** | `paper.py`, `paper_live.py`, `birth_on.py`, `deploy/`, runbooks |
| `paper-data` | **orphan — no common ancestor** | 12 | 393 commits of live journal (§5.5) |

**THE FINDING THAT MATTERS MOST, AND IT IS INVISIBLE FROM `main`:** the Phase-4 commit messages
record a pre-registered out-of-sample **rejection**:

- `9f973fe` — *"Phase 4: out-of-sample batch validation (frozen system, holdout) — **NO-GO**"*
- `1c1ac0d` — *"Phase 4: widest-depth re-run (163 OOS windows) + report fixes — **still NO-GO**"*

with the discipline stated at `phase4_notes.md:13-19`: *"The system is frozen… The report is
read-only for tuning. A negative verdict is a successful experiment (it saved real capital)."*
**That is good science and it is the estate's own standard.** It is also a fact about what a
retrofit would be inheriting.

**The estate is a chain of unmerged drafts, and `main` is the oldest link in it.**

### 5.5 `paper-data` — the live forward record, characterised

Orphan branch (created by the workflow's bootstrap `git init`, `paper.yml:41-44`), **393 commits**,
each titled `paper tick <ISO>`, spanning **2026-07-08 03:31 → 2026-08-18 03:36 UTC — 41 days, still
running.** No source code on it. Twelve files: `<COIN>/{paper_journal.csv, run_log.csv, state.json,
report.html}` for BTC/ETH/SOL. Journal schema is 22 columns (`paper_live.py:42-45`).

| coin | trades | hit | ΣR | final % | halted |
|---|---:|---:|---:|---:|---|
| BTC | 56 | 0.232 | **−6.67** | −0.038 | false |
| ETH | 73 | 0.178 | **−16.28** | −0.12 | false |
| SOL | 80 | 0.188 | **+6.43** | +0.048 | false |
| **total** | **209** | **0.196** | **−16.52** | **−0.11** | — |

Each figure in `state.json` was **independently reproduced** by summing the raw `r` column
(−6.669 / −16.284 / +6.428). **All 209 rows are closed trades**; no coin tripped the −5% circuit
breaker.

**Composition:** every trade on every coin carries the `trade_id` prefix **`p2_asbuilt-X4`** — the
entire forward record is **one frozen configuration, no arms, no controls, no A/B**. **~66% of
entries are ungraded "thin"** (BTC 36/56, ETH 48/73, SOL 53/80) — the exact failure mode the Phase 2
audit flagged (`phase2_audit_findings.md:9`). **Zero take-profit exits exist in the vocabulary**:
every trade ends on a stop, a trail, or a regime flip.

**Integrity — three things a reviewer must know.** (1) The window is **genuinely forward**:
`paper_start_ms` = 2026-07-08 00:00 UTC, the day the agent was stood up and **29 days after** the
last bar of the Phase 1–3b study window. (2) **GitHub is dropping most hourly runs** — 393 ticks in
41 days ≈ 9.6/day against a nominal 24 — **but no trades are lost by it**, and that was measured,
not assumed: the agent re-evaluates a rolling 1,600-bar ≈ 5.56-day window (`paper_live.py:38-40`)
and merges by `entry|dir` (`:58`, `:119`); the **maximum observed inter-tick gap is 12.75 h**, a
~10× margin. (3) **Corollary risk:** because the last ~5.5 days are recomputed and overwritten each
tick, **only rows older than ~5.5 days are frozen**. And the fill model is the backtest's own — so
this is a clean out-of-sample **signal** record, **not a P&L record**.

**For the SAIL decision:** this is a real, continuous, uncontaminated 41-day forward record — and it
is **negative in aggregate**. It is consistent with, not a rescue of, the Phase 4 NO-GO.

---

## 6 · (d) SECRETS — **CLEAN** · disposition **REUSE AS-IS, NO SCRUB**

Two independent scans ran (working tree + all 8 branch tips; full 420-commit history + every blob),
then a third agent adjudicated them, re-verifying the most serious hits itself. **No literal secret
value is printed anywhere below — redacted fingerprints only.**

**Scope, stated precisely:** 420 commits · **4,307 blobs — 100% coverage, nothing scoped down,
nothing truncated** · 10 refs · **193 unique paths ever present** in history.

### 6.1 The negatives, each established by enumeration

| test | result |
|---|---|
| Credential-shaped **filenames** ever, any branch, any commit — `.env`, `.env.*`, `credentials`, `.netrc`, `*.pem`, `*.p12`, `*.key`, `id_rsa`, `secrets.*`, `kubeconfig`, `.npmrc`, `.pypirc`, `.aws`, `.ssh`, `service_account`, … | **ZERO of 193 paths** |
| **Env-read sites** of any form — `os.environ`, `os.getenv`, `getenv(`, `environ[`, `dotenv`, `load_dotenv`, `ENV[`, `process.env`, systemd `Environment=` / `EnvironmentFile=` | **ZERO in all 4,307 blobs** |
| Pickaxe — was such a call ever added *and removed*? `git log --all -S` for `os.environ`, `getenv`, `dotenv` | **0 commits.** Never added, never removed — **this is not a scrub, it never existed** |
| Exchange SDK declared | **none** — `ccxt` 0, `eth_account` 0, `LocalAccount` 0, `sign_l1_action` 0 |
| Order-placement path | **none** — `place_order` 0, `submit_order` 0, `/fapi/v1/order` 0, `/api/v3/order` 0, `headers=` 0, `auth=` 0, `hmac` 0 |
| Deleted files across all history | **exactly one** (`paper.yml`, later recreated) — the only place a credential could have been committed-then-removed, and all three blob versions were opened |
| Outbound hosts, whole history | every one is a **public keyless endpoint** |

### 6.2 The ten hits, redacted — every one REFERENCE-ONLY

| citation | pattern | redacted fingerprint | live? |
|---|---|---|---|
| `.github/workflows/paper.yml:34` | URL-embedded token | `${{ secrets.GITHUB_TOKEN }}` **expression text** in `https://x-access-token:<EXPR>@github.com/…` — no value bound; 3 blob versions all opened | **REFERENCE-ONLY** |
| `reports/phase4_oos_batch_*/checksum_manifest.csv` | hex64 / "Binance-key shape" | 391 distinct 64-char lowercase hex under a column header literally named `sha256`, each paired with a **public** archive filename | REFERENCE-ONLY |
| `[branch] src/prometheus/birth_autopsy.py:32` | hex64 bound to a source constant | `PHASE4_PIN = "<64-hex, 59…82>"`, asserted at `:90` as `config_pin(stable=True) == PHASE4_PIN, "frozen config drifted"` — a **reproducibility pin** | REFERENCE-ONLY |
| `reports/phase4_oos_batch_*/cells_summary.csv` | hex64 | column `config_hash`: **2,286 occurrences collapsing to exactly 1 distinct value**, identical to `PHASE4_PIN`. *A secret is not stamped identically onto 2,286 result rows; a pin is.* | REFERENCE-ONLY |
| `[branch] docs/build_notes/phase4_notes.md:22-31` | hex64 in docs | the two config pins, self-described as *"SHA-256 over canonical JSON of the eight frozen-system blocks"* | REFERENCE-ONLY |
| **whole object DB — the difference-set test** | `[A-Za-z0-9]{64}` **minus** `[0-9a-f]{64}` | **DIFFERENCE SET IS EMPTY** (3,450 = 3,450, 0 remainder) | **clean negative** |
| adjudicator's own method artifact | `[0-9a-f]{40}` × 4,307 | `git cat-file --batch` header lines, count exactly = blob count — **caught and neutralised in the scanner's own output, reported for transparency** | not repo content |
| `docs/reference/…/css2.css` + the two `.htm` blobs | base64 run ≥40 | the **only** remaining high-entropy string repo-wide: a Google Fonts `fonts.gstatic.com/…woff2` cache-busting segment, 24 occurrences | REFERENCE-ONLY |
| `[branch] docs/Prometheus_v1_Spec.md:35,258,259` · `docs/runbooks/paper_trading.md:35,231,233` | prose | English sentences **asserting the absence of secrets** — *"It holds no secret, no wallet, no API key"* | REFERENCE-ONLY |
| `SS_Pyramid_v10.pine:1`, `README.md`, `binance.py:1`, `hyperliquid.py:1` | `secret` × **1,226** | **the strategy is literally named "Secret Sauce"** (21×) and the modules label themselves **"zero-secret"** (6×); the bulk is one HTML banner re-emitted by every hourly tick | REFERENCE-ONLY |

**That last row is why a naive scan of this repo looks catastrophic (~1,226 `secret` hits) while the
repo is in fact clean.** It is the single best argument for having run this scan properly rather
than trusting a grep count.

### 6.3 Disagreements between the two scans — resolved, not averaged

- **Real conflict:** Scan 1 reported `PHASE4_PIN` as `7e…60`; Scan 2 as `59…82`. **Scan 2 is
  correct** — the adjudicator read `birth_autopsy.py:32` directly; Scan 1 transposed the "stable
  pin" with the "as-is pin" (`phase4_notes.md:28-31`). **Impact on the verdict: none** — both are
  documented config pins. Recorded because a transcription error left unrecorded becomes a fact.
- **Not a conflict:** divergent keyword counts (`wallet` 17 vs 7) — Scan 1 counted **per-ref across
  8 tips**, Scan 2 **per unique blob**. Different denominators, same facts.
- **Not a conflict:** Scan 1 explicitly labelled its CLEAN **"tip-scoped only"** and refused to
  certify history. **It was right to refuse**, and the two verdicts compose rather than collide.

### 6.4 The BRIEF §6 question, answered plainly

> **Does the repo contain a code path that would require exchange credentials to run?** **NO — not
> one, and never has.** §6's *"No keys anywhere — paper needs none"* **requires nothing to be
> removed and nothing to be bypassed.** The condition is already structurally satisfied, and it was
> satisfied deliberately: `docs/Prometheus_Phase2_Build_Prompt.md:26` — *"Do NOT build: … anything
> requiring a key or secret."*

**One forward-looking caveat SAIL should own** — design intent, **not** a current code path:
`[branch] docs/runbooks/paper_trading.md:231-233` and `docs/Prometheus_v1_Spec.md:35,258,259`
describe an **optional, not-yet-built testnet order mode** that *would* need a wallet private key in
an environment variable. **There is no implementing code anywhere in history.** It matters only as a
constraint on future work: building that mode would create this repo's first credential path and
would breach §6. Note `paper_trading.md` is **absent from `main`** — a main-only review never sees it.

**DISPOSITION: REUSE AS-IS. No history scrub. No `filter-repo`, no BFG. Not a credential incident.**
This is the one question whose answer *helps* a retrofit — and it is outvoted 3–1.

---

## 7 · THE VERDICT, AND WHAT TO LIFT

### 7.1 The table the brief asked for

| # | question | verdict | the citation that decides it |
|---|---|---|---|
| **(a)** | clean strategy entry-point / thin-adapter surface | **NO** | `config.py:353-357` (config route closed by raise) · `replay.py:283` `_lifecycle` (private, rules inlined `:347-407`, fill model + metrics in the same body) · zero Protocol/ABC/registry/plugin/entry-point in `src/` |
| **(b)** | panel at 4h+1h with a stated gap policy | **NO** | `resample.py:119-121` + `config.py:29` (4h raises before evaluation; 5 of 11 intervals blocked) · `binance.py:102-104`, `hyperliquid.py:93-95`, `cache.py` (no ingestion gap policy on any live path) |
| **(c)** | report generator that accepts a template | **NO** (generator YES) | `report.py:443` `_TEMPLATE.replace(…)` against the hardcoded raw string at `:452-1322` · no non-`.py` file under `src/` on **any** of 8 branches · no templating dep |
| **(d)** | secrets, working tree + full history | **CLEAN** | 4,307/4,307 blobs · 0 credential filenames ever · 0 env-reads ever · alnum64−hex64 difference set **empty** |

**RULE APPLIED (BRIEF §2): any no → FOUND `naiad-sail`. Three of three are NO. → FOUND.**

### 7.2 What to lift by copy, with provenance

Every item below is **strategy-free** and would carry a provenance header naming the source repo,
branch, path and commit. *(Nothing has been copied. This is a shopping list, not an act.)*

| # | lift | source (`catpatrol/prometheus`) | why |
|---|---|---|---|
| 1 | **Binance USD-M klines client** — pagination at 1500, 4 retries/5 attempts with backoff, and the **closed-bar rule** `if close_time >= now: continue` | `main:src/prometheus/data/binance.py` (esp. `:20-21`, `:62-80`, `:88-89`, `:107-121`) @ `b4d11e6` | correct market, proven against the panel, zero strategy |
| 2 | **The gap policy itself** — `assert_gapless` + DETECT→DROP→RECORD, never interpolate | `phase-5-birth-on:src/prometheus/data/binance_archive.py:249-265` + `oos_batch.py:206-213` @ `f88e133` | **this is the (b) answer SAIL needs and Prometheus never wired to its live path.** Lift the policy, apply it where Prometheus did not |
| 3 | **Archive loader with checksum verification** — every zip SHA-256-checked against its published `.CHECKSUM` before a row is trusted | `phase-5-birth-on:src/prometheus/data/binance_archive.py:118-144` @ `f88e133` | fail-loud data integrity, the estate's way |
| 4 | **Cache with injected fetcher** — the one real seam in the repo | `main:src/prometheus/data/cache.py:27-43` @ `b4d11e6` | clean `Callable` data-source injection |
| 5 | **Resampler + HTF gate** — closed-bucket semantics, and the divisibility guard | `main:src/prometheus/data/resample.py:40,48,93,119-121` @ `b4d11e6` | **lift the guard, then choose `tf_govern` deliberately** — it is the thing that blocks 4h, and knowing why is worth more than the code |
| 6 | **Indicator primitives** — ema/rma/atr/sma/crossover/crossunder/bars_since/consecutive_count | `main:src/prometheus/indicators.py:19-91` @ `b4d11e6` | tested, strategy-free, Pine-faithful |
| 7 | **Journal schema + CSV writer** — the 22-column trade row | `main:src/prometheus/replay.py:86-142` + `harness/replay_report.py:44` @ `b4d11e6` | a working journal shape; **note the known defect: the engine computes 53 fields and the journal saves 22** (`Prometheus_Data_Collection_Design.md:17`) — lift the shape, widen it |
| 8 | **Operational invariants from the paper loop** — stop-guarantee, single-position, circuit breaker | `phase-5-birth-on:src/prometheus/paper.py:85-88, :90-93, :123-126` @ `f88e133` | earned in live weather; exactly BRIEF §4's paper-execution concerns |
| 9 | **Entry-injection pattern** — `EntrySignal` DTO + `simulate_arm(entries=…)` + the unvalidated `ExitStack` struct | `main:src/prometheus/replay.py:34-51, :69-82, :416-435` @ `b4d11e6` | **the adversarial pass upgraded this**: it is a real, test-proven injection pattern (`tests/test_phase3b_fixtures.py:180-182`). Copy the *shape* for SAIL's `enter` hook — do **not** import the module |
| 10 | **Scheduler templates** — cron / systemd service + timer, 5-minute cadence | `phase-5-birth-on:deploy/paper-agent.{cron,service,timer}` @ `f88e133` | BRIEF §6 wants launchd; these are the reference semantics. **And their history is the lesson: GitHub's scheduler dropped ~60% of the hourly runs (§5.5)** — launchd + the missed-while-asleep semantics is the right call |
| 11 | **The offline-fixture test pattern** — `httpx.MockTransport`, no network, no skips | `main:tests/conftest.py:1`, `tests/test_data_layer.py:42-43` @ `b4d11e6` | BRIEF §7 wants CI fixtures that state their failure condition |
| 12 | **The rolling-window merge-by-key idea** — re-evaluate a window wider than the worst tick gap, merge on `entry\|dir` | `phase-5-birth-on:src/prometheus/paper_live.py:38-40, :58, :119` @ `f88e133` | **this is the wake-order fidelity answer BRIEF §4 asks for**, and it is measured: 12.75 h max gap vs a 5.56-day window |

**What to lift NOTHING of:** `skills/*`, `birth_filter.py`, `pyramid_signals.py`, `replay.py`'s
`_lifecycle`/`build_entries` bodies, `config.py`'s strategy dataclasses. That is the brain, and
BRIEF §1 says SAIL does not have one.

**Two pieces of Prometheus's *record* are worth more than its code** — and they are already in
Naiad: `Prometheus_Stop_Loss_Logic_Learnings.md` (the SSv10 ratchet falsification) and
`Prometheus_Data_Collection_Design.md` (the 53-vs-22 field loss and the fix). Neither is a lift; both
are prior art the SAIL journal schema should read before it is frozen.

---

## 8 · FINDINGS REPORTED-NOT-FIXED, AND OPEN ITEMS

**Nothing in this list was acted on. Prometheus is read-only until the operator rules.**

1. **THE PROMETHEUS PAPER AGENT IS STILL RUNNING, UNATTENDED, TODAY.** Hourly GitHub Action
   (`paper.yml:3-5`) with `contents: write`, checking out an unmerged branch, committing to
   `origin/paper-data`. Latest tick **2026-08-18 03:36:04 UTC**. **Owner: operator.** Three
   options, with implications: **(i) leave it running** — it keeps accruing the estate's only live
   out-of-sample record at zero cost, and BRIEF §5's yardstick could eventually be measured against
   it; **(ii) stop it** (disable the workflow) — ends the accrual, and is a *write* to Prometheus,
   so it needs the disposition ruled first; **(iii) leave it and formally adopt `paper-data` as a
   comparison series** for SAIL. **Recommendation: (i) for now, decide at ratification** — it costs
   nothing and destroying a running out-of-sample record is not reversible.
2. **THE PHASE 4 OUT-OF-SAMPLE VERDICT WAS NO-GO, TWICE, AND IT IS INVISIBLE FROM `main`.** Commits
   `9f973fe` and `1c1ac0d` on `phase-4-oos-batch` (unmerged). Anyone assessing Prometheus from
   `main` — or from its README — would not know. **This is the single most important thing the
   inventory found that a casual look would miss.**
3. **`main` IS NOT THE LIVE CODE.** CI runs `phase-5-birth-on` (150 files vs 111). Five of the eight
   branches are unmerged drafts; the estate is a chain of them. Any future statement about "what
   Prometheus does" must name a branch.
4. **THE FORWARD RECORD IS NEGATIVE:** 209 closed trades, ΣR −16.52, 19.6% hit, two of three
   instruments losing, ~66% of entries ungraded "thin", zero take-profit exits in the vocabulary.
   Consistent with the Phase 4 NO-GO.
5. **A FUTURE §6 BREACH IS PRE-WRITTEN IN PROSE.** `paper_trading.md:231-233` describes an optional
   testnet order mode needing a wallet private key in an env var. No code exists. **If SAIL ever
   lifts that runbook, it lifts a §6 violation.**
6. **The (b) blocker is a *strategy* decision wearing a config costume.** Reaching 4h means moving
   `tf_govern`/`wyckoff_tf` — which changes what the HTF gate means. **In SAIL that constant belongs
   in the card-spec (BRIEF §3), not in a YAML knob.** Flagged now because it will otherwise be
   decided by accident during the skeleton build.

### 8.1 Deviations from the commissioning paste — named, per §3.1

- **Filename date.** The paste specifies `…_2026-08-17_SAIL-STEP1-INVENTORY.md` and that name is
  honoured exactly. Execution actually ran **2026-08-18 00:40–02:00 local**; the publish carries
  today's date. Both facts are stated rather than reconciled to one.
- **The brief was `git add`-ed before the publish, as the paste instructed.** §3.4 says to let
  `publish()` do the staging and not to `git add` exchange files separately. The brief is inside
  `exchange/`, so `publish()` stages it either way and the pre-staging changes nothing. Recorded
  because the rule was consciously crossed, not because it caused harm.
- **`/Volumes/LaCie` was not mounted**, so the local-candidate enumeration covered `~` and
  `/Volumes` only. Per §2.1 the LaCie is backup-only; this does not weaken the finding that no local
  Prometheus checkout exists on the working machine.
- **`pytest` was NOT run** in the Prometheus clone — it would write `.pytest_cache/` into a
  read-only tree. Test-suite facts are read from source, and that is stated wherever they appear.
- **One census claim was refuted and is corrected in place, not buried:** the (a) adapter assessment
  (§3.3) and two (b) exhaustiveness statements (§4.1, §4.3). The headline verdicts survived all
  three adversarial passes.

### 8.2 Method, so this can be re-derived or refuted

Ten agents: six parallel census readers ((a), (b), (c), secrets-tree, secrets-history, general), then
three adversarial refuters — one per lettered question, each instructed to **default to refuted if it
could not independently confirm** — and one secrets adjudicator that re-verified the most serious
hits itself rather than merging the two scans blindly. 939,182 subagent tokens, 399 tool calls,
0 errors. Full transcripts:
`~/.claude/projects/-Users-luis-Naiad/8f241ae7-8b32-4a9b-8e89-cb3656a5d59b/subagents/workflows/wf_c1912b28-f7f/`
(local, not in the box). **Verifier outcomes: (a) headline confirmed / adapter assessment refuted ·
(b) headline confirmed / three ABSENT claims refuted · (c) not refuted, high confidence ·
(d) CLEAN, adjudicated.**

---

## 9 · WHAT REMAINS OPEN — the operator's next word

**The disposition is NOT ratified by this report. It is proposed.**

| item | owner | implication |
|---|---|---|
| **RETROFIT vs FOUND — ratify** | **operator** | the inventory says **FOUND `naiad-sail`**, 3 NO / 0 YES. Ratifying unblocks BRIEF §8's sequence (skeleton → card-spec export → first heartbeat) |
| **Prometheus decommission-or-retrofit** (BRIEF §8 names this as inherited) | **operator** | includes the running agent (item 1). Until ruled, Prometheus stays read-only and nothing in it is touched |
| **`~/prometheus-inventory` — keep or delete** | operator | a disposable read surface outside `~/Naiad`, outside every sync tree, not backed up. Deleting it costs nothing; re-cloning takes seconds |
| **Where `tf_govern` lives in SAIL** (item 6) | operator, at skeleton time | card-spec constant vs config knob. Decide deliberately |

---

## 10 · FILE-DISPOSITION TABLE

Every file this session created, modified or moved. **Nothing was created, modified or moved inside
the Prometheus repo or its clone.**

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-17_SAIL-STEP1-INVENTORY.md` | yes | tracked (new) | see §11 | yes — `origin/v12-v1-census` | GitHub + estate zip | **51,927 B at creation = 0.32% of box — UNDER the 64,000 B trip-wire, not flagged.** Measured at creation, which is when the rule binds (§3.2). The publish re-reads the wire and names whatever is over it |
| `exchange/reports/BRIEF_ATHENA_SAIL_REPO_2026-08-17.md` | yes | tracked (new — dragged in by operator, staged this session) | see §11 | yes — `origin/v12-v1-census` | GitHub + estate zip | 5,171 B = 0.03% of box — under the wire |
| `exchange/status/LEDGER_ATHENA.md` | yes | tracked | see §11 | yes — `origin/v12-v1-census` | GitHub + estate zip | **104,471 B before this append = 0.65% of box — ALREADY OVER the 64,000 B trip-wire.** An append-only file that grew across the wire — the named cost in §3.2. Flagged, not refused |
| `~/prometheus-inventory/` | yes | **not in this repo** | n/a | n/a | **NOT PROTECTED — deliberately.** Disposable quarantine clone, outside `~/Naiad`, outside every sync tree | **n/a — unsynced**, outside the box entirely |

**Constants taken from `publish_exchange`, never a copy:** `BOX_BYTES = 16,000,000` ·
`FLAG_BYTES = 64,000` · warn 0.40 / refuse 0.70 · `TICK_EXTRA = ('LEDGER.md',)`.
Per §3.1, **this file does not contain its own sha256** — it is verified before and after the
publish and printed on screen.

---

## 11 · PUBLISH RECORD

One publish, carrying the brief and this report, per the commissioning paste. Invocation is §3.4's
exact form. The publish output — status, commit SHA, push result, offenders, box figures and the
live over-the-wire naming — is printed on screen and relayed in the closing block.

**LEDGER:** the STATUS block is appended to `exchange/status/LEDGER_ATHENA.md` in this same session,
per Invariant 4, ending with the line the paste specifies:

> *SAIL programme OPENED under ATHENA custody (brief 2026-08-17); step 1 inventory filed;
> disposition awaiting operator ratification.*

— HEPHAESTUS · the ground is surveyed. Three questions, three noes, and a clean history.
**Found her new; lift her plumbing; leave her brain where it was rejected.**
