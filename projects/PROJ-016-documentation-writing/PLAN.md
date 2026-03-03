# PLAN — PROJ-016 Documentation Writing

> Write user-facing Jerry documentation based on PROJ-015 audit findings, using /diataxis skill agents for quadrant-pure output.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Problem Statement](#problem-statement) | Why this project exists |
| [Scope](#scope) | What's in and out |
| [Approach](#approach) | How we'll execute |
| [Epics](#epics) | Work decomposition |
| [Dependencies](#dependencies) | What must happen first |

---

## Problem Statement

PROJ-015 audit found:
- **0% tutorial coverage** across all 15 skills — blocks new user adoption
- **0 of 6 docs pass** Diataxis purity — all mix quadrants
- **87% explanation gap** — users know *what* but not *why*
- **7 missing documents** needed for extraction from mixed-quadrant docs
- **9 Major findings** requiring document decomposition or revision

Jerry has strong reference documentation (100% coverage) but fails at onboarding and conceptual understanding.

## Scope

**In scope:**
- Write new tutorials, explanations, how-to guides per remediation plan
- Decompose mixed-quadrant documents into pure Diataxis docs
- Revise existing docs for quadrant purity
- Add Diataxis quadrant metadata to all docs
- Use /diataxis skill agents (diataxis-tutorial, diataxis-howto, diataxis-reference, diataxis-explanation)

**Out of scope:**
- Internal rule files (.context/rules/) — reference docs by nature, not user-facing
- Agent definition files — governed by agent-development-standards.md
- Re-auditing (PROJ-015 is complete)

## Approach

1. **P1 first**: Extract and decompose existing mixed docs (quick wins, resolves Major findings)
2. **Tutorials next**: Write top-5 skill tutorials using diataxis-tutorial agent
3. **Explanations**: Fill the 87% explanation gap for top skills
4. **Polish last**: Metadata, minor fixes, remaining tutorials

Each document written via /diataxis agents with ps-critic adversarial critique >= 0.90.

## Epics

| ID | Title | Priority | Effort | Key Deliverables |
|----|-------|----------|--------|------------------|
| EPIC-016-001 | Document Extraction & Revision | P1 | High | Decompose prompt-quality.md, create 2 explanation docs, revise INSTALLATION.md |
| EPIC-016-002 | Skill Tutorials | P1-P2 | Very High | Tutorials for /problem-solving, /orchestration, /worktracker |
| EPIC-016-003 | Reference Consolidation | P2 | Medium | Skills Reference, CLI Reference, decompose prompt-templates.md |
| EPIC-016-004 | Skill Explanations | P2 | High | Explanation docs for top 5 skills |
| EPIC-016-005 | Polish & Metadata | P3 | Low-Medium | Fix getting-started.md, add quadrant metadata, remaining tutorials |

## Dependencies

| Dependency | Status | Impact |
|------------|--------|--------|
| PROJ-015 audit merged (PR #134) | Open | Remediation report provides work item source |
| BUG-002 fix merged (PR #133) | Open | Unblocks version pipeline for this branch |
