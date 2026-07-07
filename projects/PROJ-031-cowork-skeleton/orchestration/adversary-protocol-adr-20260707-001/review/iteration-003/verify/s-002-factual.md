# S-002 Factual-Lens Refutation Panel — Iteration 3

## Navigation

| Section | Purpose |
|---------|---------|
| [Header](#header) | Scope and method |
| [Verdicts](#verdicts) | Per-finding factual verdict |

---

## Header

**Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-003/s-002-findings.md`
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Lens:** Factual accuracy (does the defect exist at the cited lines; misreads/stale refs/restatements of disclosed limits are REFUTED)
**Scope:** Critical-severity findings only, per protocol (DA-001-i3, DA-002-i3). DA-003-i3 (Major) and DA-004-i3 (Minor) are out of panel scope and not adjudicated here.

---

## Verdicts

### DA-001-i3: D-1/D-2 combination silently disables the existing Critical gate at C1–C2 — VERIFIED

Direct reads confirm every cited line. ADR lines 109-111 quote the current unconditional rule verbatim,
matching `skills/adversary/agents/adv-scorer.md:166-167`: "Any Critical finding from adv-executor
reports → automatic REVISE regardless of score" — no criticality branch exists at that site (confirmed
by direct read of `adv-scorer.md` lines 150-179). ADR line 439 (D-1) states panels run "C4 all
Criticals; C3 Criticals only; C1–C2 none"; ADR line 440 (D-2) states "Only panel-VERIFIED Criticals
trigger automatic-REVISE" with no C1–C2 carve-out; line 514's Mermaid source literally routes C1–C2
Criticals straight to the scorer, bypassing the panel. WI-3's acceptance criteria (line 847, confirmed)
describes a full, unqualified replacement: "Lines 166–167 rule replaced with verified-only gating."
Since no panel ever runs at C1–C2, no C1–C2 Critical can ever be panel-VERIFIED, so the automatic-REVISE
trigger is logically unreachable at exactly that tier. A full grep of `C1.C2` across the ADR (10 hits)
and a full read of the Negative Consequences (5 items, lines 794-809) and Risk register (7 items, lines
822-830) confirms this specific gap is nowhere named or accepted as a trade-off — the closest adjacent
disclosure (Positive Consequence #4, lines 785-788) discloses only that C1–C2 panels don't run for cost
reasons, not that the auto-REVISE trigger itself becomes unreachable. This is a genuine, undisclosed
internal-consistency gap, not a misread or a restatement of an already-disclosed limitation.

### DA-002-i3: WI-7's "generalization gate" only blocks a doc pointer, not the mechanism — VERIFIED

Direct reads confirm every cited line. Line 830 (RSK-7) and line 851 (WI-7) match the quoted text
exactly, including the "MUST NOT land until WI-8's non-ADR-genre validation has run" precondition. The
Work-Item Decomposition dependency column (lines 843-852) confirms WI-7 alone lists WI-8 as a dependency
("WI-2, WI-3, **WI-8**"); WI-1 depends only on WI-2, WI-3 on WI-1, WI-4 on WI-2 (line 848, confirmed —
no genre restriction in its AC), WI-5 on WI-1/WI-3/WI-4, and WI-6 on WI-3 — none of WI-1 through WI-6
depend on WI-8. `skills/adversary/agents/adv-selector.md:89-107` (directly read) confirms the
AE-001–AE-005 escalation logic keys only on path patterns and content keywords, never on deliverable
genre, so the Verify-stage insertion (WI-4) activates identically for any C3/C4 deliverable regardless
of genre. WI-7's own AC text narrowly defines "the concrete act of treating the protocol as
framework-general" as the `quality-enforcement.md` cross-reference edit — a documentation pointer —
which is the only item actually gated behind WI-8. This is a real, traceable gap between RSK-7's stated
mitigation (a pre-deployment validation gate) and the WI dependency graph's actual effect (the code
mechanism ships and activates for all genres independent of WI-8), not a misread of the dependency table
or a restatement of RSK-7's already-disclosed n=2 external-validity limitation (that limitation is a
different claim — evidence-base correlation — from the claim adjudicated here, which is about what WI-8
actually gates).

---

## Result

Both Critical findings (DA-001-i3, DA-002-i3) VERIFIED at the factual layer: cited line numbers and
external file references resolve exactly as quoted, and the described defects are real textual/logical
gaps in the ADR as written, not misreads, stale references, or restatements of limitations the ADR
already discloses elsewhere.
