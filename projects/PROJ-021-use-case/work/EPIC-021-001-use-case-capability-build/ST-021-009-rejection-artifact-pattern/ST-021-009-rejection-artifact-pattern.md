# ST-021-009: Inter-Agent Rejection Artifact Pattern

> **Type:** story
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-11T00:00:00Z
> **Due:** 2026-03-12T00:00:00Z
> **Completed:** —
> **Parent:** EPIC-021-001
> **Owner:** claude
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a/I want/So that format |
| [Summary](#summary) | Context and scope |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable criteria |
| [Progress Summary](#progress-summary) | Tracking |
| [Related Items](#related-items) | Dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** Jerry Framework user invoking uc-slicer on a use case artifact

**I want** uc-slicer to produce a structured rejection artifact when it rejects an input artifact for insufficient detail level

**So that** uc-author can automatically detect the rejection and set the correct elaboration target without manual intervention

---

## Summary

Adversary finding PM-001 identified that no structured error propagation path exists between uc-author and uc-slicer. When uc-slicer rejects an artifact (e.g., BULLETED_OUTLINE when ESSENTIAL_OUTLINE is required), the user gets an error message but no machine-readable state routes back to uc-author.

**Source:** Adversary agent findings PM-001 (Critical, RPN not assigned)
**PS Analysis:** `pm001-fm001-fm002-analysis.md` recommends a lightweight YAML rejection artifact.

**Scope:**
- Design the rejection artifact YAML schema
- Implement rejection artifact production in uc-slicer agent definition
- Implement rejection artifact consumption in uc-author agent definition
- Security review of rejection artifact (red-team)
- Quality gate at >= 0.95

---

## Acceptance Criteria

- [ ] uc-slicer produces a `{artifact_path}-rejection.yaml` when rejecting an input artifact
- [ ] Rejection artifact contains: rejected_by, current_level, required_level, missing_elements, recommended_action
- [ ] uc-author detects rejection artifact on load and auto-sets elaboration target
- [ ] Red-team security review confirms no injection or manipulation vectors
- [ ] Adversary quality score >= 0.95 for the implemented pattern

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Phase** | Batch 1 — Design |
| **Design** | Pending (ps-architect) |
| **Implementation** | Blocked on design |
| **Security Review** | Blocked on implementation |
| **Quality Gate** | Blocked on security |

---

## Related Items

- **Parent:** [EPIC-021-001](../EPIC-021-001-use-case-capability-build.md)
- **Source Finding:** PM-001 in adversary-agent-findings.md
- **Analysis:** pm001-fm001-fm002-analysis.md
- **Depends On:** ps-architect design decision
- **Blocks:** Adversary R3 quality gate

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-11T00:00:00Z | claude | in_progress | Created from adversary finding PM-001 |
