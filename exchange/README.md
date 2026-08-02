# exchange/ — the coordination bus

Built 2026-08-02 by HEPHAESTUS under `FUNNEL_DIONYSUS_W1` (rulings Q-1 C · Q-2 A · Q-3 A · Q-4 A ·
Q-5 as ruled · Q-6 A · Q-7 A · Q-8 A) and `FUNNEL_ATHENA_W2` (answered: defaults).

This directory is the **visibility bus**. It is pushed to GitHub automatically so that one operator
click ("Sync now") makes current coordination state readable by every web lane. Evidence and study
artifacts are NOT published this way — they keep the per-authorization push rule (ruling Q-2 A).

| folder | what lives here |
|---|---|
| `status/` | lane ledgers, `MANIFEST.json`, daily outputs, the `CADENCE.md` trigger registry |
| `queue/` | numbered builder work orders, each carrying an operator ratification stamp |
| `reports/` | builder outputs |
| `drops/` | raw operator inbox — drag artifacts in unformatted; Hermes names and files them |
| `DIGEST.md` | Hermes-maintained one-page index at the head of the bus |

## CONTENT GUARD — binding on every file under `exchange/**`

1. **Text only.** Markdown, JSON, plain text. No binaries, no archives, no images.
2. **1 MB per-file cap.** No single file under `exchange/**` may exceed 1,048,576 bytes.
3. **Larger artifacts are referenced, never carried.** Record a pointer instead:
   `path: <repo-relative or absolute path>` plus `sha256: <64 hex chars>` and a one-line description.
   The pointer is the exchange-side record; the bytes stay where they are.

Rationale: this directory is auto-pushed and pulled into project knowledge. Weight here costs every
lane on every sync, and binaries carry nothing a lane can read.

## Standing rules that govern this directory

- **Push scope (G-rule, ruling Q-2 A).** Coordination state under `exchange/**` auto-publishes.
  Evidence never publishes without the operator.
- **HERMES never re-authors content** and never instructs a lane without an operator stamp.
- **No lane instructs another.** The queue is a request lane, not a command lane — the operator's
  `RATIFIED` stamp is what converts a request into work.
