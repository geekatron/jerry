# STORY-001: Phase 1 — Standards Compliance Validation of /nuclear-sop

> **Type:** story
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-08-07T00:00:00Z
> **Parent:** FEAT-001
> **Owner:** geekatron
> **GitHub Issue:** [#345](https://github.com/geekatron/jerry/issues/345)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | Who benefits and why |
| [Summary](#summary) | Scope of the validation |
| [Acceptance Criteria](#acceptance-criteria) | Observable done criteria |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes |

---

## User Story

**As a** Jerry maintainer evaluating PR #269
**I want** every /nuclear-sop artifact validated against current HARD rules and standards
**So that** merge risk from structural non-compliance is known before any deeper review effort is spent.

---

## Summary

Validate, at PR head `bda64202`: the 4 agent `.md` files + `.governance.yaml` companions against `agent-development-standards.md` (H-34 dual-file architecture, H-35 constitutional triplet, tool tiers per ADR-STORY015-001, AD-M-011 output paths); `SKILL.md`/`PLAYBOOK.md` against `skill-standards.md` (H-25/H-26); registration surfaces (`.claude-plugin/plugin.json`, CLAUDE.md/AGENTS.md). Use `jerry` CLI / schema validators where available.

**Scope:**
- `skills/nuclear-sop/agents/sop-{brief,executor,verifier,capture}.md` + `.governance.yaml`
- `skills/nuclear-sop/SKILL.md`, `PLAYBOOK.md`, rules/, templates/, composition/, behavioral-baselines/
- Registration: plugin.json, CLAUDE.md, AGENTS.md

## Acceptance Criteria

- [ ] All 8 agent files (4 .md + 4 .governance.yaml) have recorded schema-validation results against `agent-governance-v1.schema.json` and the official-frontmatter field list
- [ ] Every H-34/H-35/H-25/H-26 check outcome (pass or violation) is recorded per artifact with rule ID
- [ ] Tool tier declarations are checked against the ADR-STORY015-001 tier model and output paths against AD-M-011, with deviations listed as findings
- [ ] Findings report exists at `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-001-independent-review/STORY-001-standards-compliance/phase-1-standards-report.md` with Critical/Major/Minor severity per finding

---

## Evidence

| Deliverable | Type | Link |
|-------------|------|------|
| Phase 1 standards report | Review artifact | ./phase-1-standards-report.md |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-08-07T00:00:00Z | geekatron | pending | Story created; GH parity #345 |
