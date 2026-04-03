# STORY-021: Add disallowedTools: [Agent] to Non-UX Worker Agents

> **Type:** story
> **Status:** wont_do
> **Priority:** medium
> **Impact:** low
> **Created:** 2026-03-29T18:00:00Z
> **Due:**
> **Completed:** 2026-03-29T19:00:00Z
> **Parent:** FEAT-001
> **Owner:**
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | What and why |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Related Items](#related-items) | Links and dependencies |

---

## User Story

**As a** Jerry framework maintainer

**I want** all non-UX worker agents to explicitly declare `disallowedTools: [Agent]`

**So that** P-003 single-level nesting is enforced via explicit deny (defense-in-depth) rather than implicit deny-by-omission

---

## Summary

Red-vuln finding F-003 (STORY-013-M007 engagement) identified that 79 non-UX worker agents rely solely on their `tools:` allowlist not including `Agent` for P-003 enforcement. While functionally equivalent, this implicit deny approach is structurally weaker: a single accidental `Agent` addition during a tier upgrade creates a P-003 violation with no automated detection.

Adding explicit `disallowedTools: [Agent]` to all non-T5 worker agents converts implicit-deny-by-omission to explicit-deny, making P-003 enforcement auditable and CI-checkable uniformly.

---

## Acceptance Criteria

- [ ] All non-T5 worker agents across all skills have `disallowedTools: [Agent]` in .md frontmatter
- [ ] Grep verification: zero non-T5 agents without disallowedTools declaration
- [ ] No T5 orchestrator agents accidentally receive disallowedTools
- [ ] CI validation passes (per STORY-022)

---

## Related Items

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Informed By | STORY-013 M-007 | UX agents fix revealed broader gap |
| Informed By | red-vuln F-003 | Finding that identified 79 agents without disallowedTools |
| Related | STORY-022 | CI check that would detect regressions |
