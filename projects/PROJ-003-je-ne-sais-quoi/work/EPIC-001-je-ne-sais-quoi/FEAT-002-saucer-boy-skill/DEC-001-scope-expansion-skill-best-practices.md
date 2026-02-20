# FEAT-002:DEC-001: Scope Expansion — Skill Best Practices Framework

<!--
TEMPLATE: Decision
VERSION: 1.0.0
SOURCE: worktracker.md (Decision File), ADR/MADR best practices
CREATED: 2026-02-19 (Claude)
PURPOSE: Document decision to expand FEAT-002 scope to include Anthropic skill best practices
-->

> **Type:** decision
> **Status:** ACCEPTED
> **Priority:** HIGH
> **Created:** 2026-02-19
> **Parent:** FEAT-002-saucer-boy-skill
> **Owner:** Claude
> **Related:** FEAT-002:EN-002-skill-implementation

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description of decisions captured |
| [Decision Context](#decision-context) | Background and constraints |
| [Decisions](#decisions) | Structured D-NNN decision entries |
| [Decision Summary](#decision-summary) | Quick reference table |
| [Related Artifacts](#related-artifacts) | Traceability |
| [Document History](#document-history) | Change log |

---

## Summary

Scope expansion for FEAT-002 EN-002 (skill implementation). The initial implementation mechanically extracted files from the design spec without verifying against established skill best practices. User review identified the deliverable as substandard — missing navigation tables, improper file references, and no evidence that existing skill patterns were consulted.

**Decisions Captured:** 3

**Key Outcomes:**
- Anthropic's skill development guide acquired and synthesized into a reusable reference
- `/saucer-boy` skill rework required against synthesized best practices before marking EN-002 complete
- Strategy updated: synthesize best practices first, then rework the skill, then proceed with remaining features

---

## Decision Context

### Background

FEAT-002 EN-002 (skill implementation) produced a `/saucer-boy` skill by extracting 14 files from the orchestration design spec (`ps-creator-002-draft.md`, 2,636 lines). The extraction was technically correct — all files were created with proper content — but the deliverable failed the user's quality bar.

The user's feedback (verbatim): *"I don't feel like you created a high quality skill as I don't see the content table, I don't see proper file references in the skill etc... It's like you didn't even bother looking up what are the Skills best practices, what-so-ever. And you consider this a high quality deliverable?"*

The previous adversarial review (S-014 LLM-as-Judge) scored 0.936, but focused on structural registration (AGENTS.md, CLAUDE.md) rather than content quality of the actual skill files. This represents a leniency bias violation — the score did not reflect the deliverable's real quality against established patterns.

### Constraints

- FEAT-002 EN-002 status must remain `pending` until the skill meets quality standards
- Anthropic published "The Complete Guide to Building Skills for Claude" (33 pages, Jan 2026) — authoritative source
- Jerry has 8 existing production skills with established conventions
- AE-002: changes to `.context/rules/mandatory-skill-usage.md` require auto-C3 minimum (deferred)

### Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| User | Product owner | Quality of deliverables, skill usability |
| Claude | Implementer | Correct patterns, honest quality assessment |

---

## Decisions

### D-001: Acquire and Internalize Anthropic Skill Guide

**Date:** 2026-02-19
**Participants:** User, Claude

#### Question/Context

User directed: "You need to download the following PDF and use it for skill development best practices." The guide is Anthropic's official 33-page document covering skill structure, frontmatter, progressive disclosure, testing, and distribution.

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Download PDF, read externally, apply ad hoc | Quick | Knowledge not persisted, not reusable |
| **B** | Download PDF into repo, synthesize into reusable reference | Durable, benefits future skills | Takes time, scope expansion |

#### Decision

**We decided:** Option B — Download the PDF into `docs/knowledge/anthropic-skill-development-guide.pdf` and synthesize a reusable reference document at `docs/knowledge/skill-development-best-practices.md` that merges Anthropic's universal requirements with Jerry's established conventions.

#### Rationale

The Jerry framework has 8 skills and will add more. A synthesized best practices document prevents this problem from recurring and provides a quality benchmark for all future skill development.

---

### D-002: Rework /saucer-boy Skill Before Proceeding

**Date:** 2026-02-19
**Participants:** User, Claude

#### Question/Context

User stated the initial skill extraction was low quality. The question: should we proceed with remaining features (FEAT-004, 006, 007) or fix the skill first?

User directed: "We should capture this as a detailed decision in the /worktracker and then use it to update our strategy before finishing the rest of the feature."

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Proceed with FEAT-004/006/007, fix skill later | Maintains momentum | Builds on a bad foundation |
| **B** | Fix skill first, then proceed | Clean foundation, skill quality informs remaining work | Delays remaining features |

#### Decision

**We decided:** Option B — Rework the `/saucer-boy` skill using the synthesized best practices framework before proceeding with FEAT-004, FEAT-006, and FEAT-007.

#### Rationale

1. FEAT-004 (Framework Voice), FEAT-006 (Easter Eggs), and FEAT-007 (DX Delight) all depend on the `/saucer-boy` skill for voice quality gating
2. Shipping remaining features on a substandard skill foundation compounds the quality debt
3. The synthesized best practices framework will inform the quality standard for all three remaining features
4. User explicitly requested this sequencing

---

### D-003: Invalidate Previous Quality Score

**Date:** 2026-02-19
**Participants:** Claude

#### Question/Context

The S-014 LLM-as-Judge score of 0.936 awarded during the initial skill implementation did not reflect the deliverable's actual quality. The review focused on registration concerns (AGENTS.md, CLAUDE.md entries) rather than skill content quality (navigation patterns, file references, conformance to established conventions).

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Keep the 0.936 score as-is | Avoids rework | Dishonest (P-022 violation) |
| **B** | Invalidate score, re-score after rework | Honest, maintains quality gate integrity | Requires full adversarial cycle |

#### Decision

**We decided:** Option B — The 0.936 score is invalidated. The reworked skill will undergo a fresh C2 adversarial review (S-003 Steelman → S-002 Devil's Advocate → S-007 Constitutional → S-014 LLM-as-Judge) with the scoring focused on skill content quality, not just structural registration.

#### Rationale

P-022 (No Deception) requires honest quality assessment. The previous score represented a leniency bias failure — it scored what was easy to verify (registration) rather than what matters (content quality). H-13 threshold of 0.92 is meaningless if the dimensions being scored don't reflect the actual quality criteria.

#### Implications

- **Positive:** Honest quality assessment, stronger deliverable
- **Negative:** Additional time for re-scoring
- **Follow-up required:** FEAT-002 score in EPIC doc must be updated after re-scoring

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | Acquire Anthropic guide, synthesize into reusable best practices reference | 2026-02-19 | ACCEPTED |
| D-002 | Rework /saucer-boy skill before proceeding with remaining features | 2026-02-19 | ACCEPTED |
| D-003 | Invalidate previous 0.936 quality score, re-score after rework | 2026-02-19 | ACCEPTED |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-002](../FEAT-002-saucer-boy-skill.md) | Parent feature |
| Reference | [docs/knowledge/anthropic-skill-development-guide.pdf](../../../../docs/knowledge/anthropic-skill-development-guide.pdf) | Anthropic's official skill guide (33 pages) |
| Reference | [docs/knowledge/skill-development-best-practices.md](../../../../docs/knowledge/skill-development-best-practices.md) | Synthesized best practices (Anthropic + Jerry) |
| Reference | [skills/saucer-boy/SKILL.md](../../../../skills/saucer-boy/SKILL.md) | Current skill (pre-rework) |
| Related | [FEAT-002:EN-002](../EN-002-skill-implementation/EN-002-skill-implementation.md) | Implementation enabler (blocked until rework) |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-19 | Claude | Created decision document with 3 decisions (D-001, D-002, D-003) |

---

## Metadata

```yaml
id: "FEAT-002:DEC-001"
parent_id: "FEAT-002-saucer-boy-skill"
work_type: DECISION
title: "Scope Expansion — Skill Best Practices Framework"
status: ACCEPTED
priority: HIGH
created_by: "Claude"
created_at: "2026-02-19"
updated_at: "2026-02-19"
decided_at: "2026-02-19"
participants: [User, Claude]
tags: [skill-quality, scope-expansion, best-practices]
decision_count: 3
superseded_by: null
supersedes: null
```
