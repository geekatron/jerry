# EPIC-001:DEC-001: FEAT-002 Skill Architecture -- Progressive Disclosure Decomposition

> **Type:** decision
> **Status:** DOCUMENTED
> **Priority:** HIGH
> **Created:** 2026-02-19
> **Parent:** EPIC-001
> **Owner:** Claude (orchestrator)
> **Related:** DISC-001 Progressive Disclosure Architecture

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description of decisions captured |
| [Decision Context](#decision-context) | Background and constraints |
| [Decisions](#decisions) | D-001 through D-003 structured entries |
| [Decision Summary](#decision-summary) | Quick reference table |
| [Related Artifacts](#related-artifacts) | Traceability |
| [Document History](#document-history) | Change tracking |
| [Metadata](#metadata) | Machine-readable metadata |

---

## Summary

Three architectural decisions for how the /saucer-boy skill (FEAT-002) should consume the 879-line Phase 1 persona document without causing context rot.

**Decisions Captured:** 3

**Key Outcomes:**
- Progressive Disclosure pattern (SKILL.md + references/) selected over wholesale loading or summarization
- Persona doc remains canonical source; skill files are operationalized derivatives
- SKILL.md carries decision rules (authenticity tests); references/ carries examples (voice pairs, cultural palette)

---

## Decision Context

### Background

With the FEAT-001 persona document at 879 lines (~15k tokens), the question arose: how should FEAT-002 (/saucer-boy skill) consume this content without causing context rot? The answer required balancing context efficiency against completeness of persona information.

### Constraints

- Context rot threshold at ~256k tokens (DISC-001, docs/knowledge/DISCOVERIES_EXPANDED.md)
- L1 enforcement budget ~12,500 tokens (quality-enforcement.md)
- Persona doc must remain the canonical, quality-gated artifact
- Skill must support 3 agents with different information needs (reviewer, rewriter, calibrator)

---

## Decisions

### D-001: Use Anthropic Progressive Disclosure Pattern for /saucer-boy Skill

**Date:** 2026-02-19
**Participants:** Human (anowak), Claude

#### Question/Context

How should the 879-line persona document be decomposed for the /saucer-boy skill to consume without excessive context usage?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Load persona doc wholesale as SKILL.md body | Simple, no decomposition needed | ~15k tokens per invocation, context rot risk |
| **B** | Progressive Disclosure: SKILL.md (<5k words) + references/ (on-demand) | 4-5x context reduction, agent-specific loading, matches Anthropic pattern | Requires careful split-point design, cross-reference maintenance |
| **C** | Summarize persona to <500 lines, discard detail | Very lean context | Loses calibration examples, voice pairs, cultural palette |

#### Decision

**We decided:** Option B -- Progressive Disclosure with references/ directory.

#### Rationale

- Matches Anthropic's official skill architecture (Context7 /anthropics/skills)
- Aligns with Jerry's own DISC-001 (Context Rot, filesystem-as-memory)
- Enables agent-specific loading: sb-reviewer loads boundary-conditions; sb-rewriter loads voice-guide
- Preserves all detail (unlike Option C) without loading it all (unlike Option A)
- Jerry's existing skills (adversary, problem-solving) already use this pattern with modular agent/reference files

---

### D-002: Persona Doc Remains Canonical Source; Skill Files Are Operationalized Derivatives

**Date:** 2026-02-19
**Participants:** Human (anowak), Claude

#### Question/Context

Should FEAT-002 modify the persona document itself, or create a separate skill structure?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Modify persona doc to be skill-ready | Single source, no duplication | Re-triggers quality gate (0.95 threshold, 6 critic iterations), mixes "brand bible" with "field manual" |
| **B** | Separate skill structure derived from persona doc | Independent quality process, clean separation of concerns | Two artifacts to maintain |

#### Decision

**We decided:** Option B -- Separate skill structure. The persona doc (ps-creator-001-draft.md) is the "brand bible" -- the canonical, reviewed, quality-gated artifact. The skill files in `skills/saucer-boy/` are the "field manual" -- operationalized extractions organized for context-efficient consumption.

#### Rationale

Modification of the persona doc would require re-running the quality gate (0.95 threshold, 6 critic iterations). Extraction into a skill structure is a new deliverable with its own quality process (FEAT-002 C3 pipeline).

---

### D-003: SKILL.md Carries Decision Rules; references/ Carries Examples

**Date:** 2026-02-19
**Participants:** Human (anowak), Claude

#### Question/Context

What goes in SKILL.md vs references/?

#### Decision

**We decided:** SKILL.md contains the Authenticity Tests (hard gates), Core Thesis, Voice Traits table, and agent registry. References carry the before/after voice pairs, humor deployment rules, cultural palette, and implementation notes.

#### Rationale

Agents need decision rules on every invocation (Authenticity Tests determine pass/fail). They need examples only when generating or reviewing specific content types. The decision rules are ~200 lines; the examples are ~600 lines. Loading both every time wastes 75% of the context.

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | Progressive Disclosure for /saucer-boy skill (SKILL.md + references/) | 2026-02-19 | DOCUMENTED |
| D-002 | Persona doc = canonical source; skill = operationalized derivative | 2026-02-19 | DOCUMENTED |
| D-003 | SKILL.md = decision rules; references/ = examples | 2026-02-19 | DOCUMENTED |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | EPIC-001-je-ne-sais-quoi | Parent epic |
| Source | EPIC-001:DISC-001 | Progressive Disclosure Architecture discovery |
| Source | EPIC-001:DISC-002 | Training Data Research Errors (informs citation requirements in skill references) |
| Informs | FEAT-002 | Directly constrains skill architecture design |
| Informs | FEAT-004, FEAT-006, FEAT-007 | Consumers of the /saucer-boy skill |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-19 | Claude (orchestrator) | Created decision document |

---

## Metadata

```yaml
id: "EPIC-001:DEC-001"
parent_id: "EPIC-001"
work_type: DECISION
title: "FEAT-002 Skill Architecture -- Progressive Disclosure Decomposition"
status: DOCUMENTED
priority: HIGH
created_by: "Claude (orchestrator)"
created_at: "2026-02-19"
updated_at: "2026-02-19"
decided_at: "2026-02-19"
participants: [Human (anowak), Claude]
tags: [architecture, feat-002, skill-design]
decision_count: 3
superseded_by: null
supersedes: null
```
