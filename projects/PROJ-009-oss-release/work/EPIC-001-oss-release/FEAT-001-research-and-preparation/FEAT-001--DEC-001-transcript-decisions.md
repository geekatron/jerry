# FEAT-001:DEC-001: Transcript Decisions (Jerry OSS Release Planning Session)

<!--
TEMPLATE: Decision
VERSION: 1.0.0
SOURCE: .context/templates/worktracker/DECISION.md
CREATED: 2026-01-31
PURPOSE: Capture decisions made during the Jerry OSS Release planning transcript session
-->

> **Type:** decision
> **Status:** ACCEPTED
> **Priority:** HIGH
> **Created:** 2026-01-31T00:00:00Z
> **Parent:** FEAT-001
> **Owner:** User + Claude
> **Related:** transcripts/001-oss-release/packet/05-decisions.md

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overview of 4 decisions captured |
| [Decision Context](#decision-context) | Background, constraints, stakeholders |
| [Decisions](#decisions) | D-001 through D-004 detailed decisions |
| [Decision Summary](#decision-summary) | Quick reference table |
| [Related Artifacts](#related-artifacts) | Parent, source, conventions |
| [Document History](#document-history) | Change log |

---

## Frontmatter

```yaml
id: "FEAT-001:DEC-001"
work_type: DECISION
title: "Transcript Decisions (Jerry OSS Release Planning Session)"
status: ACCEPTED
priority: HIGH
created_by: "User"
participants:
  - "User"
  - "Claude"
created_at: "2026-01-31T00:00:00Z"
updated_at: "2026-01-31T18:00:00Z"
decided_at: "2026-01-31T00:00:00Z"
parent_id: "FEAT-001"
tags: ["oss-release", "license", "architecture", "repository-strategy"]
decision_count: 4
superseded_by: null
supersedes: null
```

---

## Summary

This document captures the four key decisions made during the Jerry OSS Release planning transcript session. These decisions establish the foundational strategic direction for the open-source release.

**Decisions Captured:** 4

**Key Outcomes:**
- MIT License selected for maximum adoption
- Orchestration approach chosen for complex multi-phase workflow
- Dual repository strategy established for internal vs public separation
- Decomposition with imports pattern selected for CLAUDE.md optimization

---

## Decision Context

### Background

During a planning session for the Jerry Framework open-source release, several strategic decisions were made regarding licensing, release methodology, repository structure, and architecture optimization. These decisions came from the transcript at `transcripts/001-oss-release/packet/05-decisions.md`.

### Constraints

- Must support maximum open-source adoption
- Must protect sensitive internal information
- Must enable Claude Code plugin/skill discovery
- Must manage complexity of multi-phase release workflow

### Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| User | Project Owner | Strategic direction, quality |
| Claude | Implementation | Technical feasibility, best practices |
| OSS Community | Future Users | Ease of adoption, clear licensing |

---

## Decisions

### D-001: MIT License

**Date:** 2026-01-31
**Participants:** User, Claude

#### Question/Context

What license should be used for the Jerry Framework open-source release?

> **Citation:** "MIT is fine" — [seg-0094](../../../transcripts/001-oss-release/packet/02-transcript.md#seg-0094)

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | MIT License | Maximum permissive, wide adoption, simple | No copyleft protection |
| **B** | Apache 2.0 | Patent protection, attribution | More complex, longer |
| **C** | GPL v3 | Strong copyleft, ensures derivatives remain open | Limits commercial adoption |

#### Decision

**We decided:** Use MIT License for the Jerry Framework open-source release.

#### Rationale

MIT License is the most permissive and widely adopted open-source license. It maximizes potential adoption by allowing both personal and commercial use without complex requirements. The simplicity of MIT aligns with the goal of broad community adoption.

#### Implications

- **Positive:** Maximum adoption potential, simple compliance
- **Negative:** No copyleft protection for derivatives
- **Follow-up required:** Create LICENSE file in repository

---

### D-002: Orchestration Approach for Release

**Date:** 2026-01-31
**Participants:** User, Claude

#### Question/Context

How should the complex multi-phase OSS release workflow be coordinated?

> **Citation:** "Orchestration" — [seg-0064](../../../transcripts/001-oss-release/packet/02-transcript.md#seg-0064)

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Orchestration Skill | Structured workflow, state tracking, quality gates | More complex setup |
| **B** | Manual Sequential | Simple, direct | No state tracking, no parallelism |
| **C** | Ad-hoc Task List | Flexible | No coordination, easy to miss steps |

#### Decision

**We decided:** Use the /orchestration skill to coordinate the multi-phase OSS release workflow with state tracking, checkpointing, and quality gates.

#### Rationale

The OSS release involves 19 agents across 5 phases with complex dependencies. Orchestration provides structured state management, parallel execution where possible, sync barriers for cross-pollination, and mandatory quality gates at each phase.

#### Implications

- **Positive:** Reproducible workflow, checkpoint recovery, visibility
- **Negative:** Initial setup overhead
- **Follow-up required:** Create ORCHESTRATION_PLAN.md, ORCHESTRATION.yaml, ORCHESTRATION_WORKTRACKER.md

---

### D-003: Dual Repository Strategy

**Date:** 2026-01-31
**Participants:** User, Claude

#### Question/Context

How should the internal development repository relate to the public open-source repository?

> **Citation:** "So, Jerry-Core will be the new name of the internal repo or the existing repo that we're working in." — [seg-0104](../../../transcripts/001-oss-release/packet/02-transcript.md#seg-0104)

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Dual Repository | source-repository (internal), jerry (public) | Clear separation, safe migration |
| **B** | Single Repository | One repo with access controls | Simpler, but risky |
| **C** | Fork Model | Public fork of private | Complex sync requirements |

#### Decision

**We decided:** Use a dual repository strategy:
- **source-repository** (internal): Current development repository with sensitive configurations
- **jerry** (public): Clean open-source release repository

#### Rationale

The dual repository approach provides clear separation between internal development (which may contain sensitive project-specific configurations) and the public release. This allows for careful curation of what goes public while maintaining development velocity internally.

#### Implications

- **Positive:** Safe migration, clear boundaries, controlled release
- **Negative:** Need to maintain sync strategy
- **Follow-up required:** Define sync process between repos

---

### D-004: Decomposition with Imports Pattern

**Date:** 2026-01-31
**Participants:** User, Claude

#### Question/Context

How should the CLAUDE.md file be optimized for manageable size while maintaining full context?

> **Citation:** "always loaded instructions via imports vs. optionally loaded instructions via file references" — [seg-0093](../../../transcripts/001-oss-release/packet/02-transcript.md#seg-0093)

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Decomposition with Imports | Always-loaded via imports, contextual via file refs | Balanced loading, clear hierarchy |
| **B** | Monolithic | Single large file | Simple, but too large |
| **C** | Full Decomposition | Everything in separate files | Too many file reads needed |

#### Decision

**We decided:** Use a decomposition pattern with:
- **Always-loaded instructions:** Core rules and governance via imports (loaded at session start)
- **Contextually-loaded instructions:** Domain-specific details via file references (loaded on demand)

#### Rationale

The current CLAUDE.md file is large and causes context rot. By decomposing into always-loaded (essential) and contextually-loaded (on-demand) sections, we optimize context window usage while maintaining full capability access.

#### Implications

- **Positive:** Reduced context rot, faster session start, better organization
- **Negative:** Need to carefully categorize what's "always" vs "contextual"
- **Follow-up required:** Research best practices for CLAUDE.md decomposition patterns

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | MIT License for OSS release | 2026-01-31 | ACCEPTED |
| D-002 | Orchestration approach for workflow coordination | 2026-01-31 | ACCEPTED |
| D-003 | Dual repository strategy (source-repository / jerry) | 2026-01-31 | ACCEPTED |
| D-004 | Decomposition with imports for CLAUDE.md optimization | 2026-01-31 | ACCEPTED |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-001](./FEAT-001-research-and-preparation.md) | Parent feature |
| Source | [transcripts/001-oss-release/packet/05-decisions.md](../../../transcripts/001-oss-release/packet/05-decisions.md) | Source transcript decisions |
| Related | [DEC-002](./FEAT-001--DEC-002-orchestration-decisions.md) | Orchestration execution decisions |
| Convention | [.context/templates/worktracker/DECISION.md](../../../../.context/templates/worktracker/DECISION.md) | Decision template |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-31T18:00:00Z | Claude | Created decision document from transcript extraction |

---

## Metadata

```yaml
id: "FEAT-001:DEC-001"
parent_id: "FEAT-001"
work_type: DECISION
title: "Transcript Decisions (Jerry OSS Release Planning Session)"
status: ACCEPTED
priority: HIGH
created_by: "User"
created_at: "2026-01-31T00:00:00Z"
updated_at: "2026-01-31T18:00:00Z"
decided_at: "2026-01-31T00:00:00Z"
participants: ["User", "Claude"]
tags: ["oss-release", "license", "architecture", "repository-strategy"]
decision_count: 4
superseded_by: null
supersedes: null
```

---
