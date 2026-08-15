# Phase archives — the aging rule (operator ruling, 2026-08-15)

**New zips are born HERE, at `~/Naiad/research_outputs/_archive/`; older zips live on the LaCie
at `/Volumes/LaCie/Naiad/research_outputs/_archive/`, and backups go to the LaCie only.**
**So this folder holding no `*.zip` is the NORMAL end state of a cycle — it is not a missing
archive, and the retention report says so in those words rather than "none found".**

---

The `*.sha256` sidecars in THIS folder stay TRACKED in git and are the canonical fingerprints.
They are the one part of the record that needs no volume mounted and no zip present: a clone that
has never seen an archive can still say what the set contains and what each member must hash to.

**ATTESTATION CHAIN:** git — a clean tree at the origin tip — proves the tracked sidecars; the
sidecars attest the zips. That is verification basis (1), repo-tracked sidecar — the strongest tier.

Archives are PERMANENT EVIDENCE — never prunable, wherever they live. Each one holds a different
phase's evidence, so an older archive is not a superseded copy of a newer one; it is the only copy
of work that will never be produced again. If a zip is lost, restore it from the LaCie and verify
against the sidecar here.

`backup_estate.py --phase` is unchanged by this ruling: the archive is still born local and
`--mirror` still carries it to the LaCie as a second, separately-verified step.

*(History. The 2026-08-06 ruling B put the zips on `D:/Naiad/research_outputs/_archive` with the
independent backup on `G:/My Drive/naiad-backups/phases`; neither path exists on this host. A
2026-08-15 v2 note then described all nine zips as living here permanently — true when written,
superseded the same day by the aging rule above, under which the nine 2026-07/2026-08 archives were
verified against their LaCie twins and aged out.)*
