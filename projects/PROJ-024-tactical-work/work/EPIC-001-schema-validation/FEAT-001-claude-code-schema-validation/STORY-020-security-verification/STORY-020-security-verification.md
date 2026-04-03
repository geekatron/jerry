# STORY-020: Security and Access Control Verification

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Verify the new tier model maintains proper access control and H-34(b) compliance
-->

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-28T18:00:00Z
> **Due:**
> **Completed:** 2026-03-28T23:30:00Z
> **Parent:** FEAT-001
> **Owner:**
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | What needs to happen |
| [Security Assessment Scope](#security-assessment-scope) | What to verify |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist by skill |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** framework security reviewer

**I want** independent verification that the tier renumbering does not create permission escalation paths, H-34(b) violations, or MK namespace governance gaps

**So that** the governance infrastructure remains sound after a 51-file migration

---

## Summary

The tier renumbering changes what tiers mean (T3 = Persistent, T4 = External). While no agent's actual tool access changes (`.md` frontmatter is unchanged), the governance classification creates the permission *ceiling* that determines what tools an agent is *allowed* to add. This story verifies:

1. No agent gains actual tool access it didn't have (access control integrity)
2. H-34(b) remains enforced (Agent tool at T5 only)
3. MK namespace governance covers T3+ agents (not just old T4)
4. The migration didn't create temporary inconsistent state
5. eng-*/red-* MK exclusion is maintained despite T4 tier permitting MK

**Skills informing this story:**
- `/red-team` (red-vuln): Vulnerability assessment of the new permission model
- `/eng-team` (eng-security): Security code review of the rule file and YAML changes
- `/adversary` (adv-executor): C4 adversarial review of the complete implementation
- `/problem-solving` (ps-validator): Deterministic validation of tier/tool consistency

---

## Security Assessment Scope

### Access Control Integrity

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| No `.md` frontmatter tools changed | `git diff --name-only` on `.md` files in migration PR | Zero `.md` files in diff |
| No `.md` mcpServers changed | `grep -r 'memory-keeper' skills/*/agents/*.md` before/after | Identical output |
| Agent tool restriction unchanged | `grep -r 'disallowedTools' skills/*/agents/*.md` before/after | Identical output |

### H-34(b) Compliance

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| Only T5 agents have Agent tool | Cross-reference `tool_tier: T5` against `tools:.*Agent` in .md | Only ux-orchestrator |
| No worker has Agent tool | `grep -l 'Agent' skills/*/agents/*.md` cross-ref against T5 list | All matches are T5 |

### MK Namespace Governance

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| T3+ MK agents follow key namespace | All agents with `memory-keeper: true` are T3+ | No T1/T2 agent has MK |
| eng-*/red-* exclusion enforced | `grep -l 'memory-keeper' skills/eng-team/agents/*.md skills/red-team/agents/*.md` | Zero matches |
| Key pattern documented | mcp-tool-standards.md says "T3+" not "T4+" | Updated per STORY-017 |

### Migration State Consistency

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| No intermediate values | `grep -r 'T3_HOLD\|T4_HOLD' skills/*/agents/*.governance.yaml` | Zero matches |
| Tier total = 89 | Sum of T1+T2+T3+T4+T5 counts | Exactly 89 |
| Schema validation | All YAMLs pass JSON Schema | Zero validation errors |

---

## Acceptance Criteria

### /red-team (red-vuln): Permission Ceiling Verification

> **Scope note (validation 2026-03-28):** Red-team assessment rescoped from "attack surface analysis" to "permission ceiling verification" per red-team validation. Rationale: `.md` frontmatter is the enforcement boundary, not governance YAML. No runtime tool access changes, therefore no exploitable attack surface. See `research/validation-red-team.md`.

- [ ] Verify no agent can gain Memory-Keeper access without explicit `.md` frontmatter addition (permission ceiling ≠ actual grant)
- [ ] Verify no agent can gain web tool access without explicit `.md` frontmatter addition
- [ ] Confirm policy drift risk (RISK-001) is documented as accepted in ADR: 49 agents gain MK ceiling, future MK additions no longer trigger tier-change review
- [ ] Document any residual risks with severity classification

### /eng-team (eng-security): Code Review

- [ ] Review migration PR diff for unintended changes
- [ ] Verify sed operations didn't corrupt YAML structure (including inline comment handling)
- [ ] Confirm atomic commit (rule files + YAMLs in same commit)

### /adversary (C4 quality gate): Final Implementation Review

- [ ] Full implementation (rule files + YAMLs + docs) scores >= 0.95 on S-014 rubric
- [ ] No critical findings
- [ ] All 10 acceptance criteria from STORY-015 are still met post-implementation
- [ ] ADR recommendation matches implemented state

### /problem-solving (ps-validator): Deterministic Checks

- [ ] Every agent's governance YAML `tool_tier` matches the ADR migration table
- [ ] Every agent's `.md` `tools` field is unchanged from pre-migration state
- [ ] Every agent's `.md` `mcpServers` field is unchanged from pre-migration state
- [ ] Total tier distribution matches expected: T1=4, T2=28, T3=2, T4=54, T5=1

---

## Children (Tasks)

| ID | Title | Status | Owner | Skill |
|----|-------|--------|-------|-------|
| TASK-001 | Red team: permission ceiling verification (no runtime change = no attack surface) | pending | -- | /red-team |
| TASK-002 | Security review: migration PR diff audit | pending | -- | /eng-team |
| TASK-003 | Deterministic tier/tool consistency validation | pending | -- | /problem-solving |
| TASK-004 | Verify H-34(b) compliance (Agent tool at T5 only) | pending | -- | /eng-team |
| TASK-005 | Verify eng-*/red-* MK exclusion maintained AND T4 tier definition in agent-development-standards.md contains explicit exclusion note | pending | -- | /red-team |
| TASK-006 | C4 adversarial review of complete implementation | pending | -- | /adversary |

---

## Related Items

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Depends On | STORY-017 | Rule files must be in final state |
| Depends On | STORY-018 | YAML migration must be complete |
| Depends On | STORY-019 | Documentation should be updated (for completeness review) |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-28 | adam.nowak | pending | Created -- security and quality verification of tier renumbering |
| 2026-03-28 | claude | completed | 8/8 deterministic checks pass. Permission ceiling verified. eng-*/red-* MK exclusion at 5 locations. Full implementation scored 0.953 (C4 PASS). |
