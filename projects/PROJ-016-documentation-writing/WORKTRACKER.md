# WORKTRACKER — PROJ-016 Documentation Writing

> **Project:** PROJ-016-documentation-writing
> **Created:** 2026-03-02
> **Status:** Active
> **Source:** PROJ-015 remediation report

## Document Sections

| Section | Purpose |
|---------|---------|
| [Epics](#epics) | Top-level work items |
| [Features](#features) | Feature breakdown by epic |
| [Remediation Mapping](#remediation-mapping) | Traceability to PROJ-015 findings |

---

## Epics

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| EPIC-016-001 | Document Extraction & Revision | pending | high |
| EPIC-016-002 | Skill Tutorials | pending | high |
| EPIC-016-003 | Reference Consolidation | pending | medium |
| EPIC-016-004 | Skill Explanations | pending | medium |
| EPIC-016-005 | Polish & Metadata | pending | low |

### Epic Links

- [EPIC-016-001: Document Extraction & Revision](./work/EPIC-016-001-document-extraction/EPIC-016-001-document-extraction.md)
- [EPIC-016-002: Skill Tutorials](./work/EPIC-016-002-skill-tutorials/EPIC-016-002-skill-tutorials.md)
- [EPIC-016-003: Reference Consolidation](./work/EPIC-016-003-reference-consolidation/EPIC-016-003-reference-consolidation.md)
- [EPIC-016-004: Skill Explanations](./work/EPIC-016-004-skill-explanations/EPIC-016-004-skill-explanations.md)
- [EPIC-016-005: Polish & Metadata](./work/EPIC-016-005-polish-metadata/EPIC-016-005-polish-metadata.md)

---

## Features

### EPIC-016-001: Document Extraction & Revision

| ID | Title | Parent | Status | Priority | Diataxis Agent | P-ref |
|----|-------|--------|--------|----------|----------------|-------|
| FEAT-016-001 | Decompose prompt-quality.md into explanation + 2 how-to guides + reference | EPIC-016-001 | pending | high | diataxis-explanation, diataxis-howto, diataxis-reference | P1.1 |
| FEAT-016-002 | Create docs/explanation/context-architecture.md | EPIC-016-001 | pending | high | diataxis-explanation | P1.2 |
| FEAT-016-003 | Create docs/explanation/hooks-architecture.md | EPIC-016-001 | pending | high | diataxis-explanation | P1.3 |
| FEAT-016-004 | Revise INSTALLATION.md — remove marketing voice, extract explanation content | EPIC-016-001 | pending | high | diataxis-howto | P1.4 |

### EPIC-016-002: Skill Tutorials

| ID | Title | Parent | Status | Priority | Diataxis Agent | P-ref |
|----|-------|--------|--------|----------|----------------|-------|
| FEAT-016-005 | Write /problem-solving tutorial | EPIC-016-002 | pending | high | diataxis-tutorial | P1.5 |
| FEAT-016-006 | Write /orchestration tutorial | EPIC-016-002 | pending | high | diataxis-tutorial | P1.6 |
| FEAT-016-007 | Write /worktracker tutorial | EPIC-016-002 | pending | medium | diataxis-tutorial | P2.3 |

### EPIC-016-003: Reference Consolidation

| ID | Title | Parent | Status | Priority | Diataxis Agent | P-ref |
|----|-------|--------|--------|----------|----------------|-------|
| FEAT-016-008 | Decompose prompt-templates.md into reference catalog + how-to guide | EPIC-016-003 | pending | medium | diataxis-reference, diataxis-howto | P2.1 |
| FEAT-016-009 | Create Jerry Skills Reference (consolidate fragmented tables) | EPIC-016-003 | pending | medium | diataxis-reference | P2.5 |
| FEAT-016-010 | Create Jerry CLI Reference | EPIC-016-003 | pending | low | diataxis-reference | P3.3 |

### EPIC-016-004: Skill Explanations

| ID | Title | Parent | Status | Priority | Diataxis Agent | P-ref |
|----|-------|--------|--------|----------|----------------|-------|
| FEAT-016-011 | Write /problem-solving explanation (why structured problem-solving matters) | EPIC-016-004 | pending | medium | diataxis-explanation | P2.4 |
| FEAT-016-012 | Write /orchestration explanation (why multi-agent coordination) | EPIC-016-004 | pending | medium | diataxis-explanation | P2.4 |
| FEAT-016-013 | Write /worktracker explanation (why persistent work tracking) | EPIC-016-004 | pending | medium | diataxis-explanation | P2.4 |
| FEAT-016-014 | Write /eng-team explanation (why security-first engineering) | EPIC-016-004 | pending | medium | diataxis-explanation | P2.4 |
| FEAT-016-015 | Write /prompt-engineering explanation (why structured prompts) | EPIC-016-004 | pending | medium | diataxis-explanation | P2.4 |

### EPIC-016-005: Polish & Metadata

| ID | Title | Parent | Status | Priority | Diataxis Agent | P-ref |
|----|-------|--------|--------|----------|----------------|-------|
| FEAT-016-016 | Fix getting-started.md — remove tutorial branching, compress digressions | EPIC-016-005 | pending | low | diataxis-tutorial | P3.1, P3.2 |
| FEAT-016-017 | Fix title framing on BOOTSTRAP.md, CLAUDE-MD-GUIDE.md, prompt-templates.md | EPIC-016-005 | pending | low | -- | P2.2 |
| FEAT-016-018 | Add Diataxis quadrant metadata to all user-facing docs | EPIC-016-005 | pending | low | -- | P3.4 |
| FEAT-016-019 | Write tutorials for remaining 10 skills | EPIC-016-005 | pending | low | diataxis-tutorial | P3.5 |

---

## Remediation Mapping

> Traceability from PROJ-015 remediation plan items to PROJ-016 features.

| PROJ-015 Ref | Action | PROJ-016 Feature | Major Findings Resolved |
|-------------|--------|------------------|------------------------|
| P1.1 | Decompose prompt-quality.md | FEAT-016-001 | 2 |
| P1.2 | Create context-architecture.md | FEAT-016-002 | 3 |
| P1.3 | Create hooks-architecture.md | FEAT-016-003 | 2 |
| P1.4 | Revise INSTALLATION.md | FEAT-016-004 | 1 Major + 4 Minor |
| P1.5 | /problem-solving tutorial | FEAT-016-005 | Coverage gap |
| P1.6 | /orchestration tutorial | FEAT-016-006 | Coverage gap |
| P2.1 | Decompose prompt-templates.md | FEAT-016-008 | 1 |
| P2.2 | Fix title framing | FEAT-016-017 | 3 Minor |
| P2.3 | /worktracker tutorial | FEAT-016-007 | Coverage gap |
| P2.4 | Skill explanation docs | FEAT-016-011 to 015 | 5 explanation gaps |
| P2.5 | Jerry Skills Reference | FEAT-016-009 | 2 Minor |
| P3.1 | Fix tutorial branching | FEAT-016-016 | 1 Minor |
| P3.2 | Compress digressions | FEAT-016-016 | 2 Minor |
| P3.3 | Jerry CLI Reference | FEAT-016-010 | 1 Minor |
| P3.4 | Add quadrant metadata | FEAT-016-018 | Structural |
| P3.5 | Remaining tutorials | FEAT-016-019 | 10 coverage gaps |
