# EPIC-001:DISC-001: Progressive Disclosure Architecture for Skill Decomposition

> **Type:** discovery
> **Status:** VALIDATED
> **Priority:** HIGH
> **Impact:** HIGH
> **Created:** 2026-02-19
> **Completed:** 2026-02-19
> **Parent:** EPIC-001
> **Owner:** Claude (orchestrator)
> **Source:** Phase 1 Barrier 1 review, Context7 /anthropics/skills research

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Core finding: progressive disclosure solves persona context rot |
| [Context](#context) | Background and research question |
| [Finding](#finding) | Three-tier architecture and proposed decomposition |
| [Evidence](#evidence) | Sources and citations |
| [Implications](#implications) | Impact on FEAT-002 and downstream features |
| [Relationships](#relationships) | Related work items and discoveries |
| [Metadata](#metadata) | Machine-readable metadata |

---

## Summary

The 879-line FEAT-001 persona document (ps-creator-001-draft.md v0.9.0) cannot be loaded wholesale into the /saucer-boy skill context without causing context rot. Anthropic's official skill architecture uses a 3-tier Progressive Disclosure pattern that solves this: (1) Metadata always in context (~100 words), (2) SKILL.md body loaded on trigger (<5k words), (3) references/ directory loaded on-demand (unlimited). The persona document should be decomposed into ~8 purpose-specific reference files, reducing per-invocation context from ~15k tokens to 2-4k tokens.

**Key Findings:**
- Anthropic's skill architecture mandates a 3-tier progressive disclosure pattern (metadata / SKILL.md / references/)
- Agent-specific loading enables each agent to load only what it needs (e.g., sb-reviewer loads boundary-conditions, not the full cultural palette)
- Jerry's existing skills (adversary, problem-solving) already follow this pattern with modular reference files

**Validation:** Validated against Context7 /anthropics/skills library and existing Jerry skill implementations.

---

## Context

### Background

During Phase 1 Barrier 1 review, the question arose: how will FEAT-002 (/saucer-boy skill) consume the persona document without consuming excessive context? The persona doc at 879 lines (~15k tokens) exceeds the practical budget for a single skill invocation.

### Research Question

How should the /saucer-boy skill consume the Phase 1 persona document without causing context rot?

### Investigation Approach

1. Queried Context7 /anthropics/skills library for official skill architecture patterns
2. Analyzed Jerry's existing skills (adversary: 427 lines, problem-solving: 441 lines, worktracker: 198 lines) for decomposition patterns
3. Cross-referenced with DISC-001 Context Rot Threshold (~256k tokens) from docs/knowledge/DISCOVERIES_EXPANDED.md
4. Reviewed quality-enforcement.md L1 enforcement budget (~12,500 tokens, 7.6% of 200K)

---

## Finding

### Three-Tier Progressive Disclosure Architecture

| Tier | Content | Loaded When | Budget |
|------|---------|-------------|--------|
| Metadata | name + description YAML frontmatter | Always | ~100 words |
| SKILL.md | Core thesis, voice traits, authenticity tests, agent registry | Skill triggers | <5k words |
| references/ | voice-guide, humor-deployment, audience-adaptation, vocabulary, boundary-conditions, cultural-palette, visual-vocabulary, implementation-notes | On-demand | Unlimited |

### Proposed Decomposition

```
skills/saucer-boy/
├── SKILL.md                          # ~200 lines
├── references/
│   ├── voice-guide.md                # ~120 lines (9 before/after pairs)
│   ├── humor-deployment.md           # ~60 lines
│   ├── audience-adaptation.md        # ~80 lines
│   ├── vocabulary-reference.md       # ~60 lines
│   ├── boundary-conditions.md        # ~50 lines
│   ├── cultural-palette.md           # ~80 lines
│   ├── visual-vocabulary.md          # ~40 lines
│   └── implementation-notes.md       # ~120 lines (FEAT-002-007 guidance)
├── agents/
│   ├── sb-reviewer.md                # Reviews text for persona compliance
│   ├── sb-rewriter.md                # Rewrites text to match voice
│   └── sb-calibrator.md              # Scores voice fidelity
└── assets/
    └── (future: ASCII logo from FEAT-003)
```

### Agent-Specific Loading Patterns

Context7 best practice: "Include grep search patterns in SKILL.md if reference files are very large (over 10k words)."

- **sb-reviewer** only needs boundary-conditions + authenticity tests
- **sb-rewriter** needs voice-guide + humor-deployment
- **sb-calibrator** needs the full voice traits table + before/after pairs
- Neither sb-reviewer nor sb-rewriter needs the full cultural palette on every invocation

This agent-specific loading reduces per-invocation context from ~15k tokens to 2-4k tokens.

---

## Evidence

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Reference | Context7 query of /anthropics/skills library -- Progressive Disclosure Design Principle | https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md | 2026-02-19 |
| E-002 | Internal | DISC-001 Context Rot Threshold (~256k token degradation) | docs/knowledge/DISCOVERIES_EXPANDED.md | 2026-02-19 |
| E-003 | Internal | Jerry enforcement architecture -- L1 budget ~12,500 tokens, total 7.6% of 200K | .context/rules/quality-enforcement.md | 2026-02-19 |
| E-004 | Internal | Existing skill analysis -- adversary (427 lines), problem-solving (441 lines), worktracker (198 lines) | skills/adversary/SKILL.md, skills/problem-solving/SKILL.md, skills/worktracker/SKILL.md | 2026-02-19 |

---

## Implications

### Impact on Project

FEAT-002 (ps-researcher-002) MUST audit existing skill architectures AND the persona doc to identify optimal split points. The persona doc (v0.9.0) remains the canonical source; skill files are the operationalized derivative. ORCHESTRATION_PLAN.md Phase 2 must be updated to include this as a design constraint for ps-researcher-002 and ps-creator-002.

### Design Decisions Affected

- **Decision:** /saucer-boy skill architecture (DEC-001)
  - **Impact:** Mandates progressive disclosure decomposition over wholesale loading
  - **Rationale:** Context efficiency + alignment with Anthropic patterns

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Split-point design errors lose semantic coherence | MEDIUM | FEAT-002 ps-researcher-002 audits both persona doc and existing skills to identify natural section boundaries |
| Cross-reference maintenance burden across ~8 reference files | LOW | SKILL.md agent registry documents which agents load which references |

---

## Relationships

### Creates

- FEAT-002 design constraint (progressive disclosure architecture)

### Informs

- FEAT-004 (consumes persona through the skill)
- FEAT-006 (consumes persona through the skill)
- FEAT-007 (consumes persona through the skill)

### Related Discoveries

- DISC-001 Context Rot Threshold (docs/knowledge/DISCOVERIES_EXPANDED.md)

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-19 | Claude (orchestrator) | Created discovery |

---

## Metadata

```yaml
id: "EPIC-001:DISC-001"
parent_id: "EPIC-001"
work_type: DISCOVERY
title: "Progressive Disclosure Architecture for Skill Decomposition"
status: VALIDATED
priority: HIGH
impact: HIGH
created_by: "Claude (orchestrator)"
created_at: "2026-02-19"
updated_at: "2026-02-19"
completed_at: "2026-02-19"
tags: [architecture, context-efficiency, skill-design]
source: "Phase 1 Barrier 1 review, Context7 /anthropics/skills research"
finding_type: PATTERN
confidence_level: HIGH
validated: true
```
