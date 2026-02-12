# EN-206: Context Distribution Strategy

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-02 (Claude)
PURPOSE: Enable cross-platform distribution of .claude/rules/ and .claude/patterns/ to end users
-->

> **Type:** enabler
> **Status:** in_progress
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** architecture
> **Created:** 2026-02-02T06:30:00Z
> **Due:** 2026-02-15T00:00:00Z
> **Completed:** -
> **Parent:** FEAT-002
> **Owner:** Claude
> **Effort:** 20

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers - cross-platform rules/patterns distribution |
| [Problem Statement](#problem-statement) | Why .claude/ doesn't distribute via plugins |
| [Business Value](#business-value) | Enabling OSS adoption with Jerry's behavioral guardrails |
| [Technical Approach](#technical-approach) | .context/ canonical source with sync strategies |
| [Children (Tasks)](#children-tasks) | 7 work items: research, restructure, sync, bootstrap skill, docs, testing, rollback |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done for distribution strategy |
| [Risks and Mitigations](#risks-and-mitigations) | Platform compatibility and adoption risks |
| [Dependencies](#dependencies) | EN-202 completion, platform research |
| [Related Items](#related-items) | Jerry persona alignment |

---

## Summary

Enable cross-platform distribution of Jerry's behavioral rules and patterns to end users. Since `.claude/rules/` and `.claude/patterns/` are project-level memory (NOT distributed via plugins), we need a portable strategy to:

1. **Relocate** canonical rules/patterns from `.claude/` → `.context/` (version-controlled)
2. **Research** 3-5 strategies for syncing `.context/` → `.claude/` with cross-platform portability
3. **Create** a `/bootstrap` skill with Jerry personality ("ski buddy" energy, not corporate setup wizard)
4. **Document** the approach for OSS adopters

**Technical Scope:**
- Move `.claude/rules/` and `.claude/patterns/` content to `.context/`
- Research symlinks, junction points, copy scripts, and other sync mechanisms
- Address Windows portability (symlinks require admin/developer mode)
- Create humorous, on-brand `/bootstrap` skill aligned with Jerry of the Day / Shane McConkey persona
- User-facing documentation

---

## Enabler Type Classification

**This Enabler Type:** ARCHITECTURE (restructuring context distribution architecture)

| Type | Description | This Enabler |
|------|-------------|--------------|
| **ARCHITECTURE** | Architectural runway and design work | ✅ Restructuring how Jerry distributes behavioral rules |
| INFRASTRUCTURE | Platform, tooling, DevOps enablers | Partial - sync mechanism |
| EXPLORATION | Research and proof-of-concept work | Partial - SPIKE-001 research |
| COMPLIANCE | Security, regulatory requirements | No |

---

## Problem Statement

**Research Finding (EN-202:research-plugin-claude-folder-loading.md):**

Claude Code plugins distribute via `.claude-plugin/` manifest, NOT `.claude/` folders. When a user installs a plugin:

```
DISTRIBUTED (via plugin):          NOT DISTRIBUTED:
├── .claude-plugin/plugin.json     ├── .claude/
├── skills/                        │   ├── settings.json
├── agents/                        │   ├── rules/      ❌
├── hooks/                         │   └── patterns/   ❌
└── commands/
```

**The Problem:**
1. Jerry's behavioral rules (mandatory skill usage, project workflow, coding standards) live in `.claude/rules/`
2. These rules are NOT automatically provided to plugin consumers
3. Users must manually set up their `.claude/` folder
4. Windows users face additional challenges with symlinks

**User Impact:**
- OSS adopters don't get Jerry's guardrails automatically
- "Jerry moments" can occur due to missing behavioral rules
- Friction in onboarding experience

---

## Business Value

A solved distribution strategy provides:

1. **Seamless OSS Adoption** - Users run `/bootstrap` and Jerry's guardrails are active
2. **Cross-Platform Support** - Works on macOS, Linux, AND Windows
3. **On-Brand Experience** - Bootstrap feels like Jerry (ski buddy, not corporate wizard)
4. **Maintainability** - Single source of truth in `.context/`, synced to user's `.claude/`

### Features Unlocked

- OSS users get full Jerry behavioral guardrails
- Windows users can participate without admin privileges
- Jerry personality extends to onboarding (not just runtime)
- Foundation for future context management improvements

---

## Technical Approach

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     JERRY FRAMEWORK REPO                             │
├─────────────────────────────────────────────────────────────────────┤
│  .context/                   (Canonical Source - Version Controlled) │
│  ├── rules/                                                          │
│  │   ├── mandatory-skill-usage.md                                   │
│  │   ├── project-workflow.md                                        │
│  │   └── coding-standards.md                                        │
│  └── patterns/                                                       │
│      └── PATTERN-CATALOG.md                                         │
│                                                                      │
│  .claude/                    (Synced from .context/ - User Config)   │
│  ├── rules/ ────────────────► Synced via chosen strategy            │
│  └── patterns/ ─────────────► Synced via chosen strategy            │
│                                                                      │
│  skills/bootstrap/           (New Skill - Jerry Personality)         │
│  └── SKILL.md               "Your AI's ski buddy for setup"         │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ User runs /bootstrap
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        USER'S PROJECT                                │
├─────────────────────────────────────────────────────────────────────┤
│  .claude/                                                            │
│  ├── rules/                  (Populated by /bootstrap)              │
│  │   ├── mandatory-skill-usage.md                                   │
│  │   ├── project-workflow.md                                        │
│  │   └── coding-standards.md                                        │
│  └── patterns/               (Populated by /bootstrap)              │
│      └── PATTERN-CATALOG.md                                         │
└─────────────────────────────────────────────────────────────────────┘
```

### Research Scope (SPIKE-001)

Research 3-5 strategies with analysis for each:

| Strategy | macOS/Linux | Windows | Pros | Cons |
|----------|-------------|---------|------|------|
| Symlinks | Native | Requires Dev Mode | Single source | Windows friction |
| Junction Points | N/A | Native | Windows native | macOS/Linux incompatible |
| File Copy | Works | Works | Universal | Sync issues, duplication |
| Git Submodule | Works | Works | Version-controlled | Complex for users |
| Bootstrap Script | Works | Works | Explicit, controllable | Requires execution |

### Jerry Persona Alignment

The `/bootstrap` skill MUST embody Jerry's personality:

- **Voice Mode:** `saucer_boy` (default) - playful, ski metaphors, buddy energy
- **NOT:** Corporate wizard, enterprise onboarding, or generic setup
- **Tone:** "Getting your bindings adjusted" not "Configuring your environment"
- **Error Messages:** "Yard sale on the setup - let's recover" not "Installation failed"
- **Success:** "Fresh tracks await!" not "Setup complete"

Reference: persona-voice-guide.md (Jerry persona guidelines)

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Effort | Type | Owner |
|----|-------|--------|--------|------|-------|
| [SPIKE-001](./SPIKE-001-research-sync-strategies.md) | Research 3-5 Cross-Platform Sync Strategies | **complete** | 3 | Spike | Claude |
| [TASK-001](./TASK-001-restructure-to-context.md) | Restructure: Move rules/patterns to .context/ | pending | 2 | Task | Claude |
| [TASK-002](./TASK-002-implement-sync-mechanism.md) | Implement Chosen Sync Mechanism | pending | 3 | Task | Claude |
| [TASK-003](./TASK-003-create-bootstrap-skill.md) | Create /bootstrap Skill with Jerry Personality | pending | 3 | Task | Claude |
| [TASK-004](./TASK-004-user-documentation.md) | Create User Documentation | pending | 2 | Task | Claude |
| [TASK-005](./TASK-005-integration-testing.md) | Integration Testing and Platform Verification | pending | 5 | Task | Claude |
| [TASK-006](./TASK-006-rollback-documentation.md) | Rollback and Recovery Documentation | pending | 2 | Task | Claude |

### Discoveries

| ID | Title | Status | Impact |
|----|-------|--------|--------|
| [DISC-001](./DISC-001-windows-junction-points-no-admin.md) | Windows Junction Points Work Without Admin | VALIDATED | CRITICAL |

### Decisions

| ID | Title | Status |
|----|-------|--------|
| [DEC-001](./DEC-001-sync-strategy-selection.md) | Sync Strategy Selection | ACCEPTED |

### Task Dependencies

```
SPIKE-001 (Research Strategies) ✓
    │
    ├──► TASK-001 (Restructure to .context/)
    │        │
    │        └──► TASK-002 (Implement Sync) ───┬──► TASK-004 (Documentation)
    │                  │                        │
    │                  └──► TASK-005 (Testing) ─┤
    │                  │                        │
    │                  └──► TASK-006 (Rollback)─┘
    │
    └──► TASK-003 (Bootstrap Skill) ───────────► TASK-004 (Documentation)
```

### Critical Path

SPIKE-001 → TASK-001 → TASK-002 → TASK-005 → TASK-004

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [###.................] 14%  (1/7 completed)           |
| Effort:    [###.................] 15%  (3/20 points)             |
+------------------------------------------------------------------+
| Overall:   [###.................] 15%                            |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 7 |
| **Completed Tasks** | 1 (SPIKE-001) |
| **Total Effort (points)** | 20 |
| **Completed Effort** | 3 |
| **Completion %** | 15% |

---

## Acceptance Criteria

### Definition of Done

- [ ] 3-5 sync strategies researched with cross-platform analysis
- [ ] Rules and patterns moved to `.context/` canonical location
- [ ] Sync mechanism implemented (chosen from research)
- [ ] `/bootstrap` skill created with Jerry personality
- [ ] Skill passes voice/tone validation against Jerry persona guidelines
- [ ] User documentation created
- [ ] Works on macOS, Linux, AND Windows
- [ ] Windows solution doesn't require admin privileges

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | `.context/rules/` contains all behavioral rules | [ ] |
| TC-2 | `.context/patterns/` contains pattern catalog | [ ] |
| TC-3 | `.claude/rules/` syncs from `.context/rules/` | [ ] |
| TC-4 | `/bootstrap` skill loads correctly | [ ] |
| TC-5 | Bootstrap works on Windows without admin | [ ] |
| TC-6 | Jerry persona validation passes | [ ] |

---

## Evidence

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| Sync Strategy Research | Research | 3-5 strategies with cross-platform analysis | SPIKE-001 |
| `.context/` Structure | Infrastructure | Canonical rules/patterns location | `.context/` |
| Bootstrap Skill | Skill | Jerry-personality setup wizard | `skills/bootstrap/SKILL.md` |
| User Documentation | Documentation | How to bootstrap Jerry | EN-205 or standalone |

### Technical Verification

| Criterion | Verification Method | Evidence | Verified By | Date |
|-----------|---------------------|----------|-------------|------|
| Cross-platform sync | Manual testing | Test on macOS, Linux, Windows | - | - |
| Jerry persona | Voice guide comparison | Validate against Jerry persona guidelines | - | - |
| Windows no-admin | Test without admin | Standard user account test | - | - |

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Windows symlink complexity | High | High | Research alternatives (junction points, copy script) |
| User confusion with multiple strategies | Medium | Medium | Recommend ONE primary strategy, document alternatives |
| Sync drift (copy strategy) | Medium | Medium | Bootstrap detects and warns about drift |
| Persona mismatch in bootstrap | Low | Medium | Validate against Jerry persona guidelines |
| Admin privilege requirement on Windows | High | High | Ensure at least one no-admin strategy works |

---

## Dependencies

### Depends On

- [EN-202: CLAUDE.md Rewrite](../EN-202-claude-md-rewrite/EN-202-claude-md-rewrite.md) - Must complete before restructuring
- [research-plugin-claude-folder-loading.md](../EN-202-claude-md-rewrite/research-plugin-claude-folder-loading.md) - Research foundation

### Enables

- [EN-204: Validation & Testing](../EN-204-validation-testing/EN-204-validation-testing.md) - Validate context distribution works
- [EN-205: Documentation Update](../EN-205-documentation-update/EN-205-documentation-update.md) - Bootstrap docs
- Full OSS adoption with guardrails
- Windows developer support

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-002: CLAUDE.md Optimization](../FEAT-003-claude-md-optimization.md)

### Related Items

- **Research Foundation:** [research-plugin-claude-folder-loading.md](../EN-202-claude-md-rewrite/research-plugin-claude-folder-loading.md)
- **Jerry Persona Guide:** persona-voice-guide.md (Jerry persona guidelines)
- **Jerry of the Day Research:** jerry-of-the-day-research.md (Jerry persona origin research)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-02T10:00:00Z | Claude | in_progress | **QG-1 PASSED:** ps-critic (0.91), nse-qa (0.93) - combined 0.92 meets threshold |
| 2026-02-02T09:45:00Z | Claude | in_progress | Added TASK-005 (Integration Testing) and TASK-006 (Rollback) from QG-1 gap analysis |
| 2026-02-02T09:00:00Z | Claude | in_progress | QG-1 remediation: Created addendum addressing all critical gaps |
| 2026-02-02T08:30:00Z | Claude | in_progress | QG-1 adversarial review: ps-critic (0.71), nse-qa (0.78) - 7 gaps, 6 NCs identified |
| 2026-02-02T08:00:00Z | Claude | in_progress | SPIKE-001 complete, DISC-001 and DEC-001 documented |
| 2026-02-02T06:30:00Z | Claude | pending | Enabler created based on plugin loading research findings |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | PBI with ValueArea=Architectural |
| **SAFe** | Enabler (ARCHITECTURE type) |
| **JIRA** | Story with 'enabler' label |
