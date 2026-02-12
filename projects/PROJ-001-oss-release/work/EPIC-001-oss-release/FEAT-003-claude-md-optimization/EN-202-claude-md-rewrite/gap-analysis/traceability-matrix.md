# CLAUDE.md Content Traceability Matrix

> **Document ID:** GAP-ANALYSIS-TRACEABILITY
> **Purpose:** Comprehensive gap analysis identifying content LOST vs PRESERVED during CLAUDE.md optimization
> **Created:** 2026-02-01
> **Author:** ps-validator agent
> **Source:** CLAUDE.md.backup (915 lines)
> **Target:** CLAUDE.md (81 lines)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | High-level gap assessment |
| [Traceability Matrix](#traceability-matrix) | Section-by-section disposition |
| [GAPS Identified](#gaps-identified) | Content LOST during optimization |
| [PRESERVED Content](#preserved-content-verification) | Content successfully preserved |
| [Deferred to EN-203](#deferred-to-en-203) | Content pending migration |
| [Recommendations](#recommendations) | Gap closure actions |

---

## Executive Summary

### Overall Assessment: **MEDIUM CONCERN - Several GAPS Identified**

| Metric | Value |
|--------|-------|
| **Original Lines** | 915 |
| **New CLAUDE.md Lines** | 81 |
| **Reduction** | 91.1% |
| **Sections Analyzed** | 18 major + 60 subsections |
| **GAPS Identified** | 7 (3 CRITICAL, 2 HIGH, 2 MEDIUM) |
| **PRESERVED** | 14 sections (inline or extracted) |
| **REDUNDANT** | 4 sections (duplicates removed) |

### GAP Severity Distribution

| Severity | Count | Description |
|----------|-------|-------------|
| **CRITICAL** | 3 | Essential behavioral content missing - affects Claude operation |
| **HIGH** | 2 | Important guidance missing - degrades capability |
| **MEDIUM** | 2 | Nice-to-have content missing - minor impact |
| **LOW** | 0 | - |

---

## Traceability Matrix

### Legend

| Disposition | Meaning |
|-------------|---------|
| **PRESERVED_INLINE** | Content remains in new CLAUDE.md |
| **EXTRACTED_TO_SKILL** | Content moved to skill files |
| **EXTRACTED_TO_RULES** | Content moved to `.claude/rules/` |
| **REDUNDANT** | Duplicate content removed |
| **GAP** | Content LOST - not preserved elsewhere |
| **DEFERRED** | Planned for EN-203 (TODO migration) |

### Complete Traceability

| # | Original Section | Line Range | Disposition | Target Location | Gap Severity |
|---|------------------|------------|-------------|-----------------|--------------|
| 1 | **Header & Procedural Memory Note** | 1-6 | PRESERVED_INLINE | CLAUDE.md lines 1-3 | - |
| 2 | **Project Overview** | 8-24 | PRESERVED_INLINE | CLAUDE.md lines 5-11 (Identity) | - |
| 2.1 | Core Problem: Context Rot | 13-24 | PRESERVED_INLINE | CLAUDE.md lines 9-11 | - |
| 3 | **Worktracker (`<worktracker>`)** | 27-401 | EXTRACTED_TO_SKILL | `/worktracker` skill (6 files) | - |
| 3.1 | Entity Hierarchy | 32-92 | EXTRACTED_TO_SKILL | `worktracker-entity-hierarchy.md` | - |
| 3.2 | Entity Classification | 95-128 | EXTRACTED_TO_SKILL | `worktracker-entity-hierarchy.md` | - |
| 3.3 | System Mapping Summary | 131-159 | EXTRACTED_TO_SKILL | `worktracker-system-mappings.md` | - |
| 3.4 | System Mappings (Full) | 160-215 | EXTRACTED_TO_SKILL | `worktracker-system-mappings.md` | - |
| 3.5 | Work tracker Behavior | 218-241 | EXTRACTED_TO_SKILL | `worktracker-behavior-rules.md` | - |
| 3.6 | Work Tracker Templates (1st) | 244-267 | EXTRACTED_TO_SKILL | `worktracker-templates.md` | - |
| 4 | **Work tracker Directory Structure (empty)** | 270-272 | REDUNDANT | N/A | - |
| 5 | **Templates (MANDATORY)** | 274-357 | EXTRACTED_TO_SKILL | `worktracker-templates.md` | - |
| 5.1 | Worktracker Templates (2nd) | 279-302 | REDUNDANT | Duplicate of 3.6 | - |
| 5.2 | Problem-Solving Templates | 303-320 | **GAP** | **NOT EXTRACTED** | **HIGH** |
| 5.3 | Template Usage Rules | 321-328 | EXTRACTED_TO_SKILL | `worktracker-templates.md` | - |
| 6 | **Work tracker Directory Structure** | 360-399 | EXTRACTED_TO_SKILL | `worktracker-directory-structure.md` | - |
| 7 | **TODO (`<todo>`)** | 405-438 | **DEFERRED** | EN-203 (pending) | **CRITICAL** |
| 7.1 | META TODO Requirements | 409-432 | **DEFERRED** | EN-203 TASK-002 (pending) | **CRITICAL** |
| 7.2 | TODO Sync Requirements | 433-437 | **DEFERRED** | EN-203 (pending) | **CRITICAL** |
| 8 | **Architecture** | 442-472 | PRESERVED_INLINE (summary) | Navigation table row | - |
| 8.1 | Jerry Directory Structure | 444-456 | EXTRACTED_TO_RULES | `file-organization.md` | - |
| 8.2 | Key Design Principles | 458-472 | EXTRACTED_TO_RULES | `architecture-standards.md` | - |
| 9 | **Working with Jerry** | 475-520 | **GAP** | **NOT PRESERVED** | **CRITICAL** |
| 9.1 | Project-Based Workflow | 477-492 | **GAP** | Partial in Active Project section | **MEDIUM** |
| 9.2 | Before Starting Work | 494-500 | **GAP** | **NOT PRESERVED** | **HIGH** |
| 9.3 | During Work | 501-506 | **GAP** | **NOT PRESERVED** | **MEDIUM** |
| 9.4 | After Completing Work | 507-512 | **GAP** | **NOT PRESERVED** | **MEDIUM** |
| 9.5 | Creating a New Project | 513-520 | **GAP** | **NOT PRESERVED** | **MEDIUM** |
| 10 | **Project Enforcement (Hard Rule)** | 523-651 | PRESERVED_INLINE (condensed) | CLAUDE.md lines 32-44 | - |
| 10.1 | Hook Output Format | 533-603 | PRESERVED_INLINE (condensed) | CLAUDE.md lines 36-42 | - |
| 10.2 | Required AskUserQuestion Flow | 604-627 | **GAP** | **NOT PRESERVED** | **HIGH** |
| 10.3 | Project Creation Flow | 629-651 | **GAP** | **NOT PRESERVED** | **MEDIUM** |
| 11 | **Skills Available** | 654-664 | PRESERVED_INLINE | CLAUDE.md lines 17-27, 73-80 | - |
| 12 | **Mandatory Skill Usage (PROACTIVE)** | 667-774 | **GAP** | **NOT PRESERVED** | **CRITICAL** |
| 12.1 | /problem-solving (MANDATORY) | 672-692 | **GAP** | **NOT PRESERVED** | **CRITICAL** |
| 12.2 | @nasa-se (MANDATORY) | 693-717 | **GAP** | **NOT PRESERVED** | **CRITICAL** |
| 12.3 | @orchestration (MANDATORY) | 718-739 | **GAP** | **NOT PRESERVED** | **CRITICAL** |
| 12.4 | Skill Usage Behavior Rules | 740-747 | **GAP** | **NOT PRESERVED** | **CRITICAL** |
| 12.5 | Example: Starting a New Feature | 748-760 | **GAP** | **NOT PRESERVED** | **LOW** |
| 13 | **Orchestration Skill Details** | 763-774 | EXTRACTED_TO_SKILL | `skills/orchestration/SKILL.md` | - |
| 14 | **Agents Available** | 777-786 | **GAP** | Brief mention only | **MEDIUM** |
| 15 | **Code Standards** | 789-798 | PRESERVED_INLINE | Navigation table row | - |
| 16 | **CLI Commands (v0.1.0)** | 801-858 | PRESERVED_INLINE (condensed) | CLAUDE.md line 70 | - |
| 17 | **Agent Governance (Jerry Constitution)** | 861-907 | PRESERVED_INLINE (condensed) | CLAUDE.md lines 46-66 | - |
| 17.1 | Core Principles | 867-877 | PRESERVED_INLINE | Critical Constraints table | - |
| 17.2 | Hard Principles | 879-883 | PRESERVED_INLINE | Critical Constraints table | - |
| 17.3 | Self-Critique Protocol | 884-895 | **GAP** | **NOT PRESERVED** | **MEDIUM** |
| 17.4 | Behavioral Validation | 896-907 | **GAP** | **NOT PRESERVED** | **LOW** |
| 18 | **References** | 910-915 | REDUNDANT | Available in referenced files | - |

---

## GAPS Identified

### CRITICAL GAPS (Must Address Before Release)

#### GAP-001: TODO Section Not Migrated (DEFERRED - EN-203)
**Severity:** CRITICAL
**Original Lines:** 405-438 (34 lines)
**Status:** DEFERRED to EN-203 (EN-203 status: pending)

**Lost Content:**
- All 19+ META TODO requirements ("MUST ALWAYS BE ON LIST")
- Project ID reminder pattern
- Worktracker sync requirements
- Quality reminders (no shortcuts, be truthful)
- Research/analysis framework requirements
- Three-persona documentation requirement
- Mermaid/ASCII diagram requirement

**Impact:** Claude will NOT maintain META TODO items unless EN-203 is completed before release.

**Mitigation:** EN-203 must be completed before CLAUDE.md optimization is considered complete.

---

#### GAP-002: Mandatory Skill Usage Section Missing
**Severity:** CRITICAL
**Original Lines:** 667-774 (108 lines)
**Target:** Not extracted anywhere

**Lost Content:**
```markdown
## Mandatory Skill Usage (PROACTIVE)

> **CRITICAL:** You MUST use the following skills PROACTIVELY without waiting for the user to prompt you.
> These skills are designed to ensure quality, rigor, and traceability in all work.

### /problem-solving (MANDATORY for Research/Analysis)
- USE AUTOMATICALLY WHEN: Starting ANY research or analysis task, Investigating bugs...
- Trigger Phrases: "research", "analyze", "investigate"...

### @nasa-se (MANDATORY for Requirements/Design)
- USE AUTOMATICALLY WHEN: Defining or analyzing requirements...
- Trigger Phrases: "requirements", "specification"...

### @orchestration (MANDATORY for Multi-Step Workflows)
- USE AUTOMATICALLY WHEN: Work involves multiple phases...
- Trigger Phrases: "orchestration", "pipeline", "workflow"...

### Skill Usage Behavior Rules
1. DO NOT WAIT for user to invoke skills
2. COMBINE SKILLS when appropriate
3. INVOKE EARLY - Use skills at the start of work
4. PERSIST ARTIFACTS - All skill outputs must be persisted
5. REFERENCE IN TODO - Track skill invocations
```

**Impact:** Claude will NOT proactively invoke skills. This removes a key behavioral pattern that ensures quality analysis and research.

**Recommendation:** This content should either:
1. Be added to a new rule file: `.claude/rules/mandatory-skill-usage.md`
2. Be condensed and added to CLAUDE.md Quick Reference
3. Be added to each skill's SKILL.md with "Proactive Invocation" section

---

#### GAP-003: Working with Jerry Section Missing
**Severity:** CRITICAL (subset HIGH)
**Original Lines:** 475-520 (46 lines)
**Target:** Partially covered in Active Project section

**Lost Content:**
```markdown
### Before Starting Work
1. Set `JERRY_PROJECT` environment variable for your target project
2. Check `projects/${JERRY_PROJECT}/PLAN.md` for current plan
3. Review `projects/${JERRY_PROJECT}/WORKTRACKER.md` for task state
4. Read relevant `docs/knowledge/` for domain context

### During Work
1. Use Work Tracker to persist task state
2. Update PLAN.md as implementation progresses
3. Document decisions in `docs/design/`

### After Completing Work
1. Update Work Tracker with completion status
2. Capture learnings in `docs/experience/` or `docs/wisdom/`
3. Commit with clear, semantic messages

### Creating a New Project
1. Check `projects/README.md` for next project number
2. Create directory: `mkdir -p projects/PROJ-{nnn}-{slug}/.jerry/data/items`
3. Create `PLAN.md` and `WORKTRACKER.md`
4. Add entry to `projects/README.md`
5. Set `JERRY_PROJECT` environment variable
```

**Impact:** New users/sessions will NOT have step-by-step guidance on project workflow.

**Recommendation:** Create `.claude/rules/project-workflow.md` with this content or add to worktracker skill.

---

### HIGH GAPS

#### GAP-004: Problem-Solving Templates Reference Missing
**Severity:** HIGH
**Original Lines:** 303-320 (18 lines)

**Lost Content:**
```markdown
### Problem-Solving & Knowledge Templates
**Location:** `docs/knowledge/exemplars/templates/`

| Template | Use For | Path |
|----------|---------|------|
| `adr.md` | Architecture Decision Records | ... |
| `research.md` | Research artifacts | ... |
| `analysis.md` | Analysis artifacts | ... |
| `synthesis.md` | Synthesis documents | ... |
| `review.md` | Review artifacts | ... |
| `investigation.md` | Investigation reports | ... |
```

**Impact:** Users looking for problem-solving templates won't find them through worktracker skill.

**Recommendation:** Add to `/problem-solving` skill or create separate templates skill.

---

#### GAP-005: AskUserQuestion Flow Missing
**Severity:** HIGH
**Original Lines:** 604-627 (24 lines)

**Lost Content:**
```markdown
### Required AskUserQuestion Flow
When `<project-required>` or `<project-error>` is received, Claude **MUST**:
1. **Parse** the available projects from the hook output
2. **Present options** via `AskUserQuestion`:
   - List available projects (from `AvailableProjects`)
   - Offer "Create new project" option
3. **Handle response**:
   - If existing project selected → instruct user to set `JERRY_PROJECT`
   - If new project → guide through creation flow
4. **DO NOT** proceed with unrelated work until resolved

Example AskUserQuestion structure:
```yaml
question: "Which project would you like to work on?"
header: "Project"
options:
  - label: "PROJ-001-plugin-cleanup"
    description: "[ACTIVE] Plugin system cleanup and refactoring"
  - label: "Create new project"
    description: "Start a new project workspace"
```

**Impact:** Claude may not know exactly how to handle project selection when no project is set.

**Recommendation:** Add to project workflow rules or Active Project section.

---

### MEDIUM GAPS

#### GAP-006: Self-Critique Protocol Missing
**Severity:** MEDIUM
**Original Lines:** 884-895 (12 lines)

**Lost Content:**
```markdown
### Self-Critique Protocol
Before finalizing significant outputs, agents SHOULD self-critique:
1. P-001: Is my information accurate and sourced?
2. P-002: Have I persisted significant outputs?
3. P-004: Have I documented my reasoning?
4. P-010: Is WORKTRACKER updated?
5. P-022: Am I being transparent about limitations?
```

**Impact:** Available in full JERRY_CONSTITUTION.md but not summarized for quick reference.

**Recommendation:** Already exists in `docs/governance/JERRY_CONSTITUTION.md` - just need reference.

---

#### GAP-007: Agents Available Details Missing
**Severity:** MEDIUM
**Original Lines:** 777-786 (10 lines)

**Lost Content:**
```markdown
## Agents Available
See `AGENTS.md` for the full registry. Agents are scoped to skills:

| Skill | Agents | Location |
|-------|--------|----------|
| problem-solving | 8 specialists (researcher, analyst, synthesizer, etc.) | `skills/problem-solving/agents/` |

Invoke agents via the `/problem-solving` skill.
```

**Impact:** Reference to AGENTS.md is missing. Users won't know where to find agent registry.

**Recommendation:** Add to Navigation table or Quick Reference.

---

## PRESERVED Content Verification

### Successfully Preserved (No Action Needed)

| Content | Original Location | New Location | Verification |
|---------|-------------------|--------------|--------------|
| Identity/Context Rot | Lines 8-24 | CLAUDE.md lines 5-11 | VERIFIED |
| Skills table | Lines 654-664 | CLAUDE.md lines 73-80 | VERIFIED |
| Hard Principles (P-003, P-020, P-022) | Lines 879-883 | CLAUDE.md lines 50-54 | VERIFIED |
| Python Environment | Not in original | CLAUDE.md lines 56-64 | VERIFIED (NEW) |
| CLI Commands | Lines 801-858 | CLAUDE.md line 70 | CONDENSED |
| Project Enforcement | Lines 523-651 | CLAUDE.md lines 32-44 | CONDENSED |
| Worktracker content | Lines 27-401 | `/worktracker` skill | VERIFIED |

### Successfully Extracted to Skills

| Content | Original Lines | Target File | Lines | Verification |
|---------|----------------|-------------|-------|--------------|
| Entity Hierarchy | 32-92 | `worktracker-entity-hierarchy.md` | 114 | VERIFIED |
| Classification Matrix | 95-128 | `worktracker-entity-hierarchy.md` | included | VERIFIED |
| System Mappings | 131-215 | `worktracker-system-mappings.md` | 102 | VERIFIED |
| Worktracker Behavior | 218-241 | `worktracker-behavior-rules.md` | 149 | VERIFIED |
| Templates | 244-356 | `worktracker-templates.md` | 137 | VERIFIED |
| Directory Structure | 360-399 | `worktracker-directory-structure.md` | 91 | VERIFIED |

### Successfully Extracted to Rules

| Content | Original Lines | Target File | Verification |
|---------|----------------|-------------|--------------|
| Architecture | 442-472 | `architecture-standards.md` | VERIFIED |
| Directory Structure | 444-456 | `file-organization.md` | VERIFIED |
| Design Principles | 458-472 | `architecture-standards.md` | VERIFIED |

---

## Deferred to EN-203

### EN-203 Status: PENDING (NOT STARTED)

| Content | Original Lines | Target | Status |
|---------|----------------|--------|--------|
| TODO section | 405-438 | `skills/worktracker/rules/todo-integration.md` | PENDING |
| META TODO requirements | 409-432 | TASK-002 | PENDING |
| TODO sync requirements | 433-437 | TASK-002 | PENDING |

**WARNING:** EN-203 has NOT been executed. This means CRITICAL behavioral content is NOT preserved anywhere.

**Recommendation:** Execute EN-203 immediately before considering optimization complete.

---

## Recommendations

### Immediate Actions (Before Release)

| Priority | Action | Target | Addresses |
|----------|--------|--------|-----------|
| **P0** | Complete EN-203 | todo-integration.md | GAP-001 |
| **P0** | Create mandatory-skill-usage.md | `.claude/rules/` | GAP-002 |
| **P0** | Create project-workflow.md | `.claude/rules/` | GAP-003, GAP-005 |

### Short-Term Actions

| Priority | Action | Target | Addresses |
|----------|--------|--------|-----------|
| **P1** | Add problem-solving templates ref | `/problem-solving` skill | GAP-004 |
| **P1** | Add AGENTS.md to Navigation | CLAUDE.md Navigation table | GAP-007 |
| **P2** | Add Self-Critique Protocol ref | Quick Reference | GAP-006 |

### Content to Create

#### 1. mandatory-skill-usage.md (P0)

```markdown
# Mandatory Skill Usage Rules

> Auto-invoke skills proactively without waiting for user prompt.

## Trigger Rules

| Keyword Detected | Skill to Invoke |
|------------------|-----------------|
| research, analyze, investigate, explore | `/problem-solving` |
| requirements, specification, V&V | `/nasa-se` |
| orchestration, pipeline, multi-phase | `/orchestration` |

## Behavior Rules

1. DO NOT WAIT for user to invoke skills
2. COMBINE SKILLS when appropriate
3. INVOKE EARLY at start of work
4. PERSIST ARTIFACTS
5. REFERENCE IN TODO
```

#### 2. project-workflow.md (P0)

```markdown
# Project Workflow Rules

## Before Starting Work
1. Set JERRY_PROJECT environment variable
2. Check projects/${JERRY_PROJECT}/PLAN.md
3. Review projects/${JERRY_PROJECT}/WORKTRACKER.md
4. Read relevant docs/knowledge/

## During Work
1. Use Work Tracker to persist task state
2. Update PLAN.md as implementation progresses
3. Document decisions in docs/design/

## After Completing Work
1. Update Work Tracker with completion status
2. Capture learnings in docs/experience/
3. Commit with clear, semantic messages

## AskUserQuestion Flow (when project-required)
[Full flow from original]
```

---

## Gap Closure Status

| GAP ID | Severity | Status | Action Required |
|--------|----------|--------|-----------------|
| GAP-001 | CRITICAL | OPEN | Complete EN-203 |
| GAP-002 | CRITICAL | OPEN | Create mandatory-skill-usage.md |
| GAP-003 | CRITICAL | OPEN | Create project-workflow.md |
| GAP-004 | HIGH | OPEN | Add to /problem-solving skill |
| GAP-005 | HIGH | OPEN | Add to project-workflow.md |
| GAP-006 | MEDIUM | LOW_PRIORITY | Reference exists in CONSTITUTION |
| GAP-007 | MEDIUM | OPEN | Add to Navigation table |

---

## Summary

### CLAUDE.md Optimization Assessment

| Aspect | Rating | Notes |
|--------|--------|-------|
| Size Reduction | **EXCELLENT** | 91% reduction achieved |
| Worktracker Extraction | **COMPLETE** | All content in skill files |
| TODO Migration | **INCOMPLETE** | EN-203 not executed |
| Mandatory Skills | **GAP** | Critical behavioral content lost |
| Project Workflow | **GAP** | Operational guidance lost |
| Overall Completeness | **70%** | 3 CRITICAL gaps remain |

### Risk Assessment

**Release Risk: HIGH**

The CLAUDE.md optimization is NOT COMPLETE for release. Critical behavioral content that affects Claude's operation is missing:

1. **TODO management** - Claude won't maintain META TODO items
2. **Proactive skill invocation** - Claude won't automatically invoke skills
3. **Project workflow guidance** - New sessions won't have operational steps

### Recommended Next Steps

1. **STOP** considering EN-202 complete
2. **EXECUTE** EN-203 TODO migration
3. **CREATE** mandatory-skill-usage.md
4. **CREATE** project-workflow.md
5. **UPDATE** CLAUDE.md Navigation table with AGENTS.md reference
6. **RE-VALIDATE** after gap closure

---

*Generated: 2026-02-01*
*Validator: ps-validator agent*
*Confidence: HIGH (all source files analyzed)*
