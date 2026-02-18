# EPIC-001:DEC-004: Post-Release Planning Decisions

> **Type:** decision
> **Status:** accepted
> **Priority:** high
> **Created:** 2026-02-17
> **Parent:** EPIC-001
> **Owner:** Adam Nowak
> **Related:** FEAT-016, FEAT-017, FEAT-018

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description of decisions captured |
| [Decision Context](#decision-context) | Background and constraints |
| [Decisions](#decisions) | Structured D-001 through D-003 entries |
| [Decision Summary](#decision-summary) | Quick reference table |
| [Related Artifacts](#related-artifacts) | Traceability |
| [Document History](#document-history) | Change log |

---

## Summary

Three strategic decisions captured from the OSS post-release planning session (transcript packet `transcript-oss-post-release-20260217-001`). These decisions establish platform support policy, skill optimization strategy, and installation distribution model for the Jerry framework.

**Decisions Captured:** 3

**Key Outcomes:**
- OSX-primary platform designation with Windows as portability effort
- Skill/agent definition optimization deferred to upcoming releases
- Installation model transitioning from private archive to repository-based access

---

## Decision Context

### Background

Following the initial OSS release of Jerry, a solo planning session was conducted to identify remaining work items and make explicit prioritization decisions. The session covered four primary areas: platform support transparency, skill/agent definition quality, installation instruction modernization, and user documentation planning.

### Constraints

- Project is already released as OSS — changes must be backward compatible
- Windows support requires user-reported issues to identify problems
- Skill/agent definitions are functional but not optimized — optimization is deferred, not urgent
- Installation model is transitioning — current collaborator model is interim until public release

---

## Decisions

### D-001: OSX-Primary Platform Designation

**Date:** 2026-02-17
**Participants:** Adam Nowak (project lead)

#### Question/Context

What is the official platform support posture for the Jerry framework, and how should this be communicated to users?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Claim full cross-platform support | Broader appeal | Dishonest — Windows has known issues |
| **B** | Designate OSX-primary, Windows as portability effort | Honest, sets expectations | May deter Windows users |
| **C** | Drop Windows support entirely | Simplifies maintenance | Alienates potential contributors |

#### Decision

**We decided:** The project is officially OSX-primary. Windows support is a portability initiative, not first-class support. The README will indicate this status and actively solicit Windows-specific issue reports.

#### Rationale

Honesty about platform support sets appropriate user expectations and encourages productive issue reporting rather than frustrated complaints. Actively soliciting Windows issues demonstrates commitment to improvement without overpromising.

#### Implications

- **Positive:** Clear user expectations, targeted issue collection
- **Negative:** Some Windows users may be deterred
- **Follow-up required:** FEAT-016 (README updates with platform notice)

**Transcript Citation:**
> "we need to update the README to indicate that this project was primarily built for OSX and we are working on platform portability support, namely Windows."
> — SPEAKER_00, seg-002

---

### D-002: Skill/Agent Definition Optimization Deferred

**Date:** 2026-02-17
**Participants:** Adam Nowak (project lead)

#### Question/Context

The skill and agent definitions are acknowledged as "chunky and not necessarily following best practices." Should this be addressed now or deferred?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Optimize now before further releases | Cleaner codebase | Delays other priority work |
| **B** | Defer with disclaimer, optimize in future releases | Focus on higher-priority items | Technical debt remains |

#### Decision

**We decided:** Optimization is deferred to upcoming releases. A disclaimer will be added to documentation noting that optimization is on the roadmap.

#### Rationale

The definitions are functional despite being suboptimal. Higher-priority items (installation instructions, platform notices) should be addressed first. Adding a disclaimer provides transparency without blocking progress.

#### Implications

- **Positive:** Focus on higher-priority post-release tasks
- **Negative:** Technical debt persists in skill/agent definitions
- **Follow-up required:** EN-938 (optimization disclaimer), future optimization epic

**Transcript Citation:**
> "This will definitely be tackled in the upcoming releases."
> — SPEAKER_00, seg-006

---

### D-003: Installation Model Transition to Repository-Based Access

**Date:** 2026-02-17
**Participants:** Adam Nowak (project lead)

#### Question/Context

The current installation instructions reference a private archive-based distribution model that is no longer the primary distribution method. What should the new installation model be?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Keep archive-based distribution | No documentation changes needed | Doesn't reflect reality |
| **B** | Collaborator + SSH (current) → public repo (future) | Accurate, forward-looking | Two-phase documentation needed |
| **C** | Jump directly to public repo model | Simplest instructions | Repo isn't public yet |

#### Decision

**We decided:** Transition to a two-phase repository-based installation model: (1) current interim model uses collaborator access with SSH keys via Claude Code marketplace, (2) future model uses public repository direct access.

#### Rationale

This reflects the actual distribution evolution and provides clear instructions for both current and future users. The two-phase approach avoids misleading users about the current state while documenting the intended end state.

#### Implications

- **Positive:** Instructions match reality, forward-looking
- **Negative:** Instructions will need updating when repo goes public
- **Follow-up required:** FEAT-017 (installation instructions modernization)

**Transcript Citation:**
> "And then going forward, when we make the repository public, then people can just quite literally add that to the Claude Code marketplace and have it show up."
> — SPEAKER_00, seg-010

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | OSX-primary platform; Windows = portability effort | 2026-02-17 | accepted |
| D-002 | Skill/agent optimization deferred to future releases | 2026-02-17 | accepted |
| D-003 | Installation model: archive → collaborator/SSH → public repo | 2026-02-17 | accepted |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EPIC-001](./EPIC-001-oss-release.md) | Parent epic |
| Feature | [FEAT-016](./FEAT-016-post-release-documentation/FEAT-016-post-release-documentation.md) | Implements D-001, D-002 |
| Feature | [FEAT-017](./FEAT-017-installation-instructions/FEAT-017-installation-instructions.md) | Implements D-003 |
| Feature | [FEAT-018](./FEAT-018-user-documentation/FEAT-018-user-documentation.md) | Related user documentation |
| Transcript | ~/Downloads/transcripts/transcript-oss-post-release-20260217-001/ | Source transcript packet |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-17 | Claude | Created decision document from transcript packet analysis |

---

## Metadata

```yaml
id: "EPIC-001:DEC-004"
parent_id: "EPIC-001"
work_type: DECISION
title: "Post-Release Planning Decisions"
status: accepted
priority: high
created_by: "Claude"
created_at: "2026-02-17"
updated_at: "2026-02-17"
decided_at: "2026-02-17"
participants: ["Adam Nowak"]
tags: ["post-release", "platform-support", "installation", "skill-optimization"]
decision_count: 3
superseded_by: null
supersedes: null
```
