# Refutation Panel — Materiality Lens — S-007 (Constitutional AI Critique) Findings, Iteration 2

## Navigation

| Section | Purpose |
|---------|---------|
| [Scope](#scope) | What was reviewed and against what standard |
| [Verdicts](#verdicts) | Per-finding VERIFIED/REFUTED with evidence |
| [Summary](#summary) | Final tallies |

---

## Scope

**Lens:** Materiality — does the finding genuinely undermine the ADR (wrong decision, unimplementable
spec, or false evidence)? Style and edge-case concerns are REFUTED even when technically true.
Default posture: REFUTED IF UNCERTAIN.

**Target:** `projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-002/s-007-findings.md`
(4 findings: CC-001-iter2 Critical, CC-002-iter2 Major, CC-003-iter2 Major, CC-004-iter2 Minor).

**Cross-checked against:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
(full text, lines 1-866), `.context/rules/agent-development-standards.md` (Tool Security Tiers),
`.context/rules/quality-enforcement.md` (Criticality Levels), `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`.

---

## Verdicts

### CC-001-iter2: `adv-verifier` Tool-Tier Self-Contradiction — **VERIFIED**

The ADR states, verbatim, at line 604: "Tool tier **T1 (read-only: Read, Glob, Grep)**" for the
proposed `adv-verifier` agent, then at lines 614-616 requires its output to be "**persisted** to
`.../adversary/iteration-NNN/verify/{finding-id}-{lens}.md`" — repeated as a joint acceptance
criterion ("T1 tools only" + "per-lens verdict files persisted") at WI-1 (line 762) and Draft Issue A
(lines 777-782). The framework's own SSOT (`.context/rules/agent-development-standards.md`, Tool
Security Tiers) defines T1 as exactly `Read, Glob, Grep` (no Write) and states explicitly: "T2 when
the agent produces artifacts. Writing files ... requires T2 minimum." Persisting a new per-lens
verdict file is producing a file artifact and therefore requires Write, which T1 structurally
excludes. This is not a stylistic nit: as literally written, a builder cannot satisfy both WI-1
acceptance-criteria bullets simultaneously without silently deviating from the stated tier (violating
H-34) — this is squarely "unimplementable spec" under the materiality test, and it hits the one
agent artifact (D-6) the entire verification architecture's independence claim depends on.

### CC-002-iter2: "Architectural" Blindness Claim vs. Cross-Lens Filesystem Reads — **REFUTED**

The finding hypothesizes that a later-invoked lens could use its Glob/Read grant to locate and read
an earlier lens's already-persisted verdict file if the three lens invocations are not run strictly
in parallel (ADR lines 612-613, 742). This is a plausible but speculative implementation-detail
concern, not a defect in the ADR's stated decision: the ADR does not specify sequential invocation,
and this very execution environment's own convention (independent tool/agent calls issued together
when there is no dependency between them) is the natural way an implementer would invoke three blind,
input-independent lenses, which forecloses the described race in ordinary practice. The finding
itself concedes this is a residual/completeness gap addressable by several non-decision-changing
options (parallelism guarantee, path scoping, or a wording downgrade) — it does not show the D-1/D-6
decision is wrong or unimplementable, only that one sentence ("enforced architecturally") could be
more precisely worded. Per the materiality lens, an edge-case implementation-ordering risk on a
claim that is already substantially true in the framework's normal parallel-invocation practice is
REFUTED.

### CC-003-iter2: New Verify Stage Not Reflected in SSOT Criticality Levels Table — **REFUTED**

The finding correctly observes the Verify stage is mandatory at C3 (Criticals only)/C4 (all Criticals)
per D-1 (ADR line 403) and WI-4 (line 765), while the ADR deliberately scopes its only SSOT edit to a
pointer in the Implementation section (lines 646-648), per its own constraint c-002 (line 215:
"SSOT constants ... are referenced, never redefined"). The finding itself concedes this "may be a
defensible, intentional design choice" with a real, named precedent — `adv-scorer.md`'s existing
unconditional Critical-gating rule already lives outside the `quality-enforcement.md` Criticality
Levels table today, which the ADR's proposed edit (D-2/L1 item 3) directly supersedes in place. The
gap identified is a documentation-traceability/consistency preference (should the SSOT table gain a
footnote), explicitly permitted by the ADR's own stated constraint rather than an oversight that
produces a wrong decision or a non-implementable spec. This is a SHOULD-tier completeness suggestion,
not a genuine undermining defect; REFUTED under the materiality lens.

### CC-004-iter2: `scope: framework` Declared Pre-Promotion — **REFUTED**

Confirmed accurate as far as text match: ADR frontmatter line 5 reads `scope: framework` while the
file resides in `projects/PROJ-031-cowork-skeleton/decisions/` (a project location) and Status is
`PROPOSED` (lines 93-96); `adr-standards-rule-draft.md:52` does read "Scope is expressed by
**location** (may change)." However, the finder itself classifies this Minor and explicitly states
"It does not undermine the ADR's technical content and the convention itself is still in draft."
ADR-M-013 (`adr-standards-rule-draft.md:58`) permits declaring scope at authoring time "when not
uncertain," which the author plausibly is not, given the ADR's explicit subject (governing the
`/adversary` skill framework-wide). This is a soft convention-interpretation ambiguity in a still-draft
standard, not a wrong decision, unimplementable spec, or false evidence. REFUTED under the materiality
lens (style/interpretation, not substance).

---

## Summary

| Finding | Severity (as filed) | Materiality Verdict |
|---------|---------------------|----------------------|
| CC-001-iter2 | Critical | **VERIFIED** |
| CC-002-iter2 | Major | REFUTED |
| CC-003-iter2 | Major | REFUTED |
| CC-004-iter2 | Minor | REFUTED |

**1 of 4 findings VERIFIED** (the sole Critical). The Critical genuinely blocks acceptance under the
materiality test: the `adv-verifier` tool-tier declaration (T1, Read/Glob/Grep only) is directly
incompatible with its own mandatory output contract (per-lens verdict files persisted), per the
framework's own Tool Security Tier SSOT — an unimplementable-spec defect in the ADR's central new
agent (D-6), not a style issue. The two Major findings and the one Minor finding are real
observations but do not meet the materiality bar: they identify residual completeness/precision gaps
that the ADR's own text substantially anticipates, defends, or renders moot via existing framework
convention, and none alters the correctness or implementability of the ADR's six decisions.
