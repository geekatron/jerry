# FEAT-005:DEC-002: Orchestration v3.0 Design Decisions

<!--
TEMPLATE: Decision
VERSION: 1.0.0
SOURCE: worktracker.md (Decision File), ADR/MADR best practices
CREATED: 2026-01-31 (FEAT-005 Orchestration v3.0 Design)
-->

> **Type:** decision
> **Status:** DOCUMENTED
> **Priority:** CRITICAL
> **Created:** 2026-01-31T03:30:00Z
> **Parent:** FEAT-005
> **Owner:** Claude
> **Related:** FEAT-005:DISC-003

---

## Frontmatter

```yaml
id: "FEAT-005:DEC-002"
work_type: DECISION
title: "Orchestration v3.0 Design Decisions"
status: DOCUMENTED
priority: CRITICAL
created_by: "Claude"
participants:
  - "User"
  - "Claude"
created_at: "2026-01-31T03:30:00Z"
updated_at: "2026-01-31T03:30:00Z"
decided_at: "2026-01-31T03:30:00Z"
parent_id: "FEAT-005"
tags: ["orchestration", "v3.0", "design-decisions", "dependency-chain"]
superseded_by: null
supersedes: null
decision_count: 5
```

---

## State Machine

```
              +----------+
              |  PENDING |
              +----+-----+
                   |
                   v
            +------------+
            | DOCUMENTED |  <-- CURRENT STATE (awaiting user approval of v3.0 plan)
            +------+-----+
                   |
                   v
            +----------+
            | ACCEPTED |
            +----------+
```

---

## Summary

This document captures the 5 key design decisions for ORCHESTRATION_PLAN v3.0, addressing the dependency chain flaw identified in DISC-003.

**Decisions Captured:** 5

**Key Outcomes:**
- TASK-419 becomes Phase 0 sequential prerequisite
- Adversarial critic evaluates after each enabler completion
- TASK-419 failure is a hard blocker requiring user decision
- v3.0 created fresh (not updating v2.x)
- Cross-pollination details documented with no ambiguity

---

## Decision Context

### Background

During orchestration planning for FEAT-005, the user identified a critical flaw in ORCHESTRATION_PLAN v2.x: TASK-419 was shown as parallel to EN-027 when it should be a sequential prerequisite. The user requested a redesign with specific requirements.

### Constraints

- Must maintain quality through adversarial critic feedback loops
- Must respect true dependency chain (TASK-419 gates all work)
- Must provide unambiguous cross-pollination documentation
- Must be created as v3.0 fresh start, not incremental update

### Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| User | Project Owner | Quality, correct dependencies, approval authority |
| Claude | Implementer | Accurate orchestration, efficient execution |

---

## Decisions

### D-001: Create v3.0 Fresh (Not Update v2.x)

**Date:** 2026-01-31T03:30:00Z
**Participants:** User, Claude

#### Question/Context

**User asked:** Should the orchestration plan be updated incrementally (v2.x → v2.3.0) or created fresh as v3.0?

**Claude's clarification question:** "Should I attempt to update the existing orchestration plan or create a new v3.0?"

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Update v2.x incrementally | Preserves history, smaller diff | Complex merge, confusing version history |
| **B** | Create v3.0 fresh | Clean slate, clear break, easier to reason about | Loses some history, larger file creation |

#### Decision

**We decided:** Create ORCHESTRATION_PLAN v3.0 as a fresh document, not an incremental update to v2.x.

#### Rationale

The dependency chain change is fundamental enough that a fresh start is cleaner. The v2.x files remain as historical reference, and v3.0 clearly communicates "this is the correct plan."

#### Implications

- **Positive:** Clear separation between flawed v2.x and correct v3.0
- **Negative:** Some historical context may need explicit linking
- **Follow-up required:** Link v3.0 to v2.x for historical context

---

### D-002: Adversarial Critic After Each Enabler

**Date:** 2026-01-31T03:30:00Z
**Participants:** User, Claude

#### Question/Context

**User asked:** When should the adversarial critic (ps-critic) evaluate work?

**Claude's clarification question:** "Should adversarial critic evaluate after each task, after each enabler, or only at quality gates?"

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | After each task | Very granular feedback | Too frequent, overhead |
| **B** | After each enabler | Balanced feedback loops | Some delay in catching issues |
| **C** | Only at quality gates | Efficient, batched | Late feedback, larger rework |

#### Decision

**We decided:** Adversarial critic evaluates after each enabler completes (Option B).

#### Rationale

Enabler-level evaluation provides the right balance:
- Catches issues before downstream enablers start
- Implements the feedback loop documented in DISC-002 (6 adversarial patterns)
- Aligns with quality gate structure (G-027, G-028, G-029, G-030, G-031)

#### Implications

- **Positive:** Issues caught at natural boundaries, not too frequent
- **Negative:** Tasks within enabler don't get individual critique
- **Follow-up required:** Configure ps-critic invocation after each enabler

---

### D-003: TASK-419 Failure = Hard Blocker

**Date:** 2026-01-31T03:30:00Z
**Participants:** User, Claude

#### Question/Context

**User asked:** What happens if TASK-419 (model parameter validation) fails?

**Claude's clarification question:** "If TASK-419 fails, should we: (a) continue with workarounds, (b) pause for user decision, or (c) abandon EN-031 entirely?"

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Continue with workarounds | Progress continues | May build on broken foundation |
| **B** | Pause for user decision | User authority preserved | Blocks all work |
| **C** | Abandon EN-031 entirely | Clean cut | May be premature |

#### Decision

**We decided:** TASK-419 failure is a **hard blocker requiring user decision** (Option B).

#### Rationale

- User has ultimate authority (P-020) over fundamental feature viability
- Model selection is a significant feature; its viability should be user-decided
- Continuing on broken foundation violates quality principles
- Abandoning entirely may be premature without user input

#### Implications

- **Positive:** User maintains control over project direction
- **Negative:** Potential delay while awaiting user decision
- **Follow-up required:** Document escalation procedure in v3.0

---

### D-004: Create Plan for Approval Only

**Date:** 2026-01-31T03:30:00Z
**Participants:** User, Claude

#### Question/Context

**User stated:** "Create the plan for my approval"

**Implicit question:** Should Claude create and execute the plan, or create for review first?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Create and execute immediately | Faster progress | No user review opportunity |
| **B** | Create for approval first | User review, course correction | Additional approval step |

#### Decision

**We decided:** Create ORCHESTRATION_PLAN v3.0 for user approval only; do not execute until approved (Option B).

#### Rationale

- User explicitly requested approval step
- Major orchestration changes warrant review
- Avoids wasted work if user has corrections

#### Implications

- **Positive:** User can review and adjust before execution
- **Negative:** Adds approval latency
- **Follow-up required:** Present v3.0 to user for approval

---

### D-005: Detailed Cross-Pollination with No Ambiguity

**Date:** 2026-01-31T03:30:00Z
**Participants:** User, Claude

#### Question/Context

**User stated:** "There should be no ambiguity for yourself regarding the orchestration plan. Ensure you capture detailed decisions and discoveries in the repository first."

**Implicit question:** How detailed should cross-pollination documentation be?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Brief CP-1, CP-2, CP-3 references | Concise | May lose context in future sessions |
| **B** | Full detailed documentation | Complete context, no ambiguity | Longer documents |

#### Decision

**We decided:** Cross-pollination must be documented with full detail and no ambiguity (Option B).

#### Rationale

- Context rot is a real concern across sessions
- Detailed documentation survives compaction
- Unambiguous instructions reduce errors during execution

#### Implications

- **Positive:** Future sessions have complete context
- **Negative:** Longer documents
- **Follow-up required:** v3.0 must include detailed CP specifications

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | Create v3.0 fresh, not update v2.x | 2026-01-31 | DOCUMENTED |
| D-002 | Adversarial critic after each enabler | 2026-01-31 | DOCUMENTED |
| D-003 | TASK-419 failure = hard blocker requiring user decision | 2026-01-31 | DOCUMENTED |
| D-004 | Create plan for approval only, don't execute | 2026-01-31 | DOCUMENTED |
| D-005 | Detailed cross-pollination with no ambiguity | 2026-01-31 | DOCUMENTED |

---

## Cross-Pollination Specification (D-005 Detail)

Per D-005, here is the detailed cross-pollination specification for v3.0:

### CP-1: TASK-419 → Track A (EN-027)

| Attribute | Value |
|-----------|-------|
| **ID** | CP-1 |
| **Trigger** | TASK-419 completion (PASS or FAIL) |
| **Source** | Phase 0 (TASK-419) |
| **Target** | Track A (EN-027 specifically) |
| **Information Transferred** | Model parameter validation results |
| **Format** | Structured findings in TASK-419 completion artifact |
| **If PASS** | EN-027 proceeds with model override capability in agent definitions |
| **If FAIL** | HARD GATE - escalate to user for decision |
| **Artifact Path** | `EN-031-model-selection-capability/TASK-419-validate-task-model.md` |

### CP-2: EN-027 → TASK-422

| Attribute | Value |
|-----------|-------|
| **ID** | CP-2 |
| **Trigger** | EN-027 quality gate G-027 PASS |
| **Source** | Track A (EN-027) |
| **Target** | Track B (TASK-422) |
| **Information Transferred** | Agent YAML schema patterns for model override |
| **Format** | Schema examples from compliant agent definitions |
| **When Available** | After G-027 passes (EN-027 complete) |
| **Artifact Path** | Agent definition files in `skills/transcript/agents/` |

### CP-3: TASK-420 → SKILL.md Documentation

| Attribute | Value |
|-----------|-------|
| **ID** | CP-3 |
| **Trigger** | TASK-420 completion |
| **Source** | Track B (TASK-420) |
| **Target** | Track A (influences EN-028 TASK-421 documentation) |
| **Information Transferred** | CLI parameter design (--model-* flags) |
| **Format** | CLI usage documentation |
| **When Available** | After TASK-420 complete |
| **Artifact Path** | `EN-031-model-selection-capability/TASK-420-add-cli-model-params.md` |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-005](./FEAT-005-skill-compliance.md) | Parent feature |
| Discovery | [FEAT-005:DISC-003](./FEAT-005--DISC-003-orchestration-dependency-chain-flaw.md) | Discovery of v2.x flaw |
| Reference | [ORCHESTRATION.yaml](./orchestration/ORCHESTRATION.yaml) | Current v2.2.0 state |
| Reference | [FEAT-003:DISC-002](../FEAT-003-future-enhancements/FEAT-003--DISC-002-adversarial-prompting-protocol.md) | Adversarial prompting protocol |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-31T03:30:00Z | Claude | Created decision document with 5 decisions |

---

## Metadata

```yaml
id: "FEAT-005:DEC-002"
parent_id: "FEAT-005"
work_type: DECISION
title: "Orchestration v3.0 Design Decisions"
status: DOCUMENTED
priority: CRITICAL
created_by: "Claude"
created_at: "2026-01-31T03:30:00Z"
updated_at: "2026-01-31T03:30:00Z"
decided_at: "2026-01-31T03:30:00Z"
participants: [User, Claude]
tags: [orchestration, v3.0, design-decisions, dependency-chain]
decision_count: 5
superseded_by: null
supersedes: null
```
