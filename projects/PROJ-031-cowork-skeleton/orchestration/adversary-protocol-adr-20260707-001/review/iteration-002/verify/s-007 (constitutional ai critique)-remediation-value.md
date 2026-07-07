# Refutation Panel — Remediation-Value Lens (Iteration 2, S-007 Constitutional AI Critique)

## Navigation

| Section | Purpose |
|---------|---------|
| [Scope](#scope) | What was reviewed and why |
| [Verdicts](#verdicts) | Per-finding VERIFIED/REFUTED with evidence |
| [Summary](#summary) | Tally for the structured reply |

---

## Scope

**Target:** `projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-002/s-007-findings.md`
**Deliverable under review:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Lens:** Remediation-value ("would fixing it change observable behavior, and can it be fixed without adding machinery?" — per the ADR's own D-6/L1 lens definition, ADR lines 624-626).
**Panel scope per this ADR's own proposed protocol:** panels are gated at the Critical level only (ADR c-004, line 217: "panels are gated at the report level, i.e. only Critical-bearing reports are panelled"). The S-007 report under review declares exactly **1 Critical** (CC-001-iter2) and 2 Major / 1 Minor findings, which fall outside this lens's mandate per the ADR's own gating rule. This verdict therefore covers CC-001-iter2 only.

---

## Verdicts

### CC-001-iter2: `adv-verifier` Tool-Tier Self-Contradiction (T1 Read-Only vs. Mandatory File Persistence)

**Verdict: VERIFIED**

The finding's underlying factual claim checks out against the deliverable and the SSOT it cites: ADR lines 604 ("Tool tier T1 (read-only: Read, Glob, Grep)"), 614-616 ("persisted to `.../verify/{finding-id}-{lens}.md`"), 762 (WI-1 AC: "T1 tools only" + "per-lens verdict files persisted"), and 776-782 (Issue A body, same pairing) all restate the identical contradiction three times. `.context/rules/agent-development-standards.md` (Tool Security Tiers table) defines T1 as `Read, Glob, Grep` with no `Write`, and its own Selection Guidelines state "T2 when the agent produces artifacts. Writing files ... requires T2 minimum" — so the contradiction is real, not a misreading of an ambiguous SSOT.

Applying the remediation-value lens specifically (not the factual-accuracy lens, which is out of scope here): fixing this **does** change observable behavior, not just prose. WI-1 (ADR line 762, ADR line 766 dependency chain WI-3/WI-4/WI-5 all depend on WI-1) is the acceptance-criteria contract a builder would implement against; as written, a builder cannot satisfy both bullets simultaneously — either the agent literally has only `Read, Glob, Grep` and cannot execute its own documented Output Format contract (the per-lens verdict files that Fig. 1, Fig. 2, and Fig. 4 all depend on as the mechanism's core artifact), or the builder silently grants `Write` and the shipped agent's `tool_tier` no longer matches what the ADR — and the H-34 schema-valid governance file the ADR itself requires (line 617-618) — declares. This is not a hypothetical or cosmetic gap: the entire D-6 decision (the reason a *new* agent was chosen over reusing `adv-executor`, ADR lines 376-391) is justified specifically on the strength of the T1-blind-independence property; an implementer resolving the contradiction unilaterally at build time either breaks that property's stated tool grant or breaks the mechanism's required output, and either resolution happens invisibly, off the ADR's own record.

The proposed remediation is exactly what the remediation-value lens looks for as a "yes" signal: it is text-only (three restatements: L1 item 1, WI-1, Issue A), adds no new agent, no new template, no new process step, and is explicitly framed by the finding itself as consistent with the ADR's own subtraction-first doctrine (D-3) — i.e., it is a correction, not an addition. This is the opposite of churn: it closes a genuine implementability gap in the one place this ADR proposes new agent machinery, at negligible edit cost, before that machinery is built. Fixing it now is materially cheaper than discovering the contradiction during WI-1 implementation and resolving it ad hoc, unrecorded, with no ADR update to match.

**Evidence:** ADR lines 604, 614-616, 762, 776-782 (self-contradiction as restated three times); `.context/rules/agent-development-standards.md` Tool Security Tiers table (T1 row) and Selection Guidelines item 2 (SSOT tier definition); ADR lines 376-391 (D-6 rationale resting on the T1-blind property this contradiction undermines).

---

## Summary

| ID | Verdict |
|----|---------|
| CC-001-iter2 | VERIFIED |

**Tally:** 1 VERIFIED, 0 REFUTED (of 1 Critical in scope for this lens per the ADR's own Critical-only panel gating rule).
