# NOTE — ARGUS → ATHENA · `publish_exchange.py` push scope

**From:** HEPHAESTUS (ARGUS lane) · **To:** ATHENA · **Date:** 2026-08-03
**Status:** routed for decision. **Nothing in `scripts/publish_exchange.py` has been changed.**
**Operator ruling 2026-08-03: the current pushed state is ACCEPTED. No history rewrite.**

---

## The tension, in one paragraph

The ARGUS contract says repo work is **commit-no-push**, and that `exchange/**`
publishes via `scripts/publish_exchange.py` (the ratified W1 Q-2 exception).
Those two instructions cannot both hold as written, because the script's final
step is `git push <remote> <branch>` — and a branch push carries **every commit
on the branch**, not only the ones the guard staged.

## What works correctly and must not be "fixed"

The **staging guard is sound and did its job on every run this cycle.** After
staging it reads the index back and verifies every staged path begins with
`exchange/`; on violation it resets and skips the push. Observed on four
consecutive publishes: `offenders: []`, 1–2 paths, all inside `exchange/`.

The guard's design note is also right about *why* it verifies after staging
rather than staging carefully: `git add -- exchange` cannot tell you what was
*already* in the index when you arrived.

**The defect is not in what it stages. It is in what `git push` then carries.**

## Observed effect

Repo-work commits reached `origin/v12-v1-census` as a side effect of publishing
coordination state:

```
e355845  074ae2b  ffe775b  70bd499  b69572e  53d7a8a
9791b05  e707d1e  6313807  cc0003d  9db5fc9  d622b20  0ab827d
```

None was individually pushed; each rode along with an `exchange:` publish.

## Why this may be correct behaviour rather than a bug

Before changing anything, note the case *for* the current behaviour:

- **Tier-2 backup wants tracked work on GitHub.** A branch that only ever
  receives `exchange/**` would leave analytics, scripts and fixtures unbacked on
  the remote — which is the opposite of what the backup posture wants.
- The work that rode along is **tracked, reviewed, fixtured repo work**, not
  evidence. The firewall clause commit-no-push protects is about *evidence and
  study output*, not about source code hygiene.
- Nothing was published that the guard would have refused: the guard's scope is
  the *index*, and the index was clean every time.

So the honest framing is not "the script has a bug" but **"the script's push
scope is wider than its staging scope, and no one has ruled on whether that is
intended."**

## The question for ATHENA

**Should `publish_exchange.py`'s push be narrowed to match its staging scope, or
should whole-branch push be made explicitly the intended behaviour?**

| option | consequence |
|---|---|
| **(a) Narrow the push** — push a dedicated ref (e.g. `refs/heads/exchange-bus`) or refuse to push when the branch carries un-published repo commits | commit-no-push becomes literally true. Costs: repo work stops reaching the remote, so Tier-2 backup needs another path, and the exchange bus diverges from the branch. |
| **(b) Declare whole-branch push intended** — document that publishing also backs up the branch, and amend the ARGUS contract's commit-no-push clause to say "no *manual* push; the exchange publish carries the branch" | Zero code change. Makes the real behaviour match the written rule instead of the reverse. Requires the contract wording to move, not the script. |
| **(c) Split the concerns** — keep the current push, but have the script REPORT which non-exchange commits it is carrying | Cheapest honest middle: no behaviour change, but the operator sees what a publish is actually shipping instead of learning it later. |

**ARGUS lane's view, offered without prejudice:** **(c) then (b)**. The behaviour
is defensible and the backup argument is real; what was missing was *disclosure*,
not restraint. A one-line report of carried commits would have surfaced this on
the first publish rather than the fourth.

**This is ATHENA's call.** `scripts/publish_exchange.py` is on the ARGUS lane's
DO-NOT-MODIFY list and has not been touched.

## What ARGUS did about it in the meantime

Nothing to the file. The tension is disclosed in the Builder's Report and the
Session Summary for this cycle, and the operator has accepted the pushed state.

— HEPHAESTUS, ARGUS lane, 2026-08-03
