# Worktracker Skill Inventory

> **Document ID:** GAP-ANALYSIS-TASK-003
> **Created:** 2026-02-01
> **Author:** ps-analyst agent
> **Purpose:** Comprehensive catalog of content extracted to worktracker skill

---

## Executive Summary

The worktracker skill successfully extracts and modularizes the worktracker-related content from CLAUDE.md into 6 files totaling 583 lines. The skill uses a hierarchical loading strategy where the main SKILL.md file references rule files via `@` imports.

---

## File Inventory

### 1. SKILL.md (Main Entry Point)

| Attribute | Value |
|-----------|-------|
| **Path** | `skills/worktracker/SKILL.md` |
| **Lines** | 117 |
| **Purpose** | Main skill definition and entry point |

#### Frontmatter Configuration

```yaml
name: worktracker
description: Work item tracking and task management using Jerry Framework hierarchy
version: "1.0.0"
allowed-tools: Read, Write, Glob, Task, Edit
activation-keywords:
  - "work tracker", "worktracker", "work-tracker"
  - "update the work tracker", "/worktracker", "/jerry:worktracker"
```

#### Sections Covered

| Section | Lines | Content |
|---------|-------|---------|
| Overview | 38-58 | Core capabilities and when to use |
| Core Rules | 61-66 | `@rules/worktracker-behavior-rules.md` import |
| Quick Reference | 69-104 | Entity containment, template locations, key files |
| Additional Resources | 107-117 | Links to detailed rule files |

#### CLAUDE.md Mapping

| SKILL.md Section | CLAUDE.md Source |
|------------------|------------------|
| Entity Containment table | Lines 99-113 (Containment Rules Matrix) |
| Template Locations | Lines 244-356 (Template section) |
| Key File Locations | Lines 218-241 (Behavior section) |

---

### 2. worktracker-behavior-rules.md

| Attribute | Value |
|-----------|-------|
| **Path** | `skills/worktracker/rules/worktracker-behavior-rules.md` |
| **Lines** | 149 |
| **Purpose** | Behavior rules and integrity enforcement |
| **Source Reference** | CLAUDE.md lines 218-241 |

#### Sections Covered

| Section | Lines | Content |
|---------|-------|---------|
| Worktracker Integrity Rules | 20-114 | WTI-001 through WTI-006 rules |
| Work tracker Behavior | 117-139 | Canonical model behavior description |
| Cross-References | 143-149 | Links to other rule files |

#### Key Content: Integrity Rules (NEW - Not in original CLAUDE.md)

| Rule ID | Enforcement | Purpose |
|---------|-------------|---------|
| WTI-001 | HARD | Real-Time State Updates |
| WTI-002 | HARD | No Closure Without Verification |
| WTI-003 | HARD | Truthful and Accurate State |
| WTI-004 | HARD | Synchronize Before Reporting |
| WTI-005 | MEDIUM | Atomic Task State |
| WTI-006 | HARD | Evidence-Based Closure |

**Note:** These integrity rules were **ADDED** during EN-201 based on discovered process failures. They represent new content not present in the original CLAUDE.md.

#### CLAUDE.md Mapping

| Behavior Rules Section | CLAUDE.md Source Lines |
|------------------------|------------------------|
| Worktracker Behavior (main) | 218-241 |
| File relationships | 223-237 |
| MCP Memory-Keeper reference | 239 |

---

### 3. worktracker-directory-structure.md

| Attribute | Value |
|-----------|-------|
| **Path** | `skills/worktracker/rules/worktracker-directory-structure.md` |
| **Lines** | 91 |
| **Purpose** | Complete folder hierarchy for work items |
| **Source Reference** | CLAUDE.md lines 360-399 |

#### Sections Covered

| Section | Lines | Content |
|---------|-------|---------|
| Folder Structure Patterns | 19-44 | Project-based vs repository-based |
| WORKTRACKER Directory Structure | 48-91 | Complete ASCII tree with annotations |

#### Key Content

1. **Two Placement Patterns** (NEW clarification):
   - Project-based: `{RepositoryRoot}/projects/{ProjectId}/work/`
   - Repository-based: `{RepositoryRoot}/work/`

2. **Complete File Hierarchy**:
   - Epic level: `.md` files, BUG, DISC, IMP, DEC, plans/
   - Feature level: `.md` files, BUG, DISC, IMP, DEC
   - Enabler/Story level: TASK, BUG, DISC, IMP, DEC, SPIKE

#### CLAUDE.md Mapping

| Directory Structure Section | CLAUDE.md Source Lines |
|----------------------------|------------------------|
| Full directory tree | 360-399 |
| File naming conventions | Embedded in tree |
| Example IDs | Embedded in tree |

---

### 4. worktracker-entity-hierarchy.md

| Attribute | Value |
|-----------|-------|
| **Path** | `skills/worktracker/rules/worktracker-entity-hierarchy.md` |
| **Lines** | 114 |
| **Purpose** | Entity types, classification, and containment rules |
| **Source Reference** | CLAUDE.md lines 32-128 |

#### Sections Covered

| Section | Lines | Content |
|---------|-------|---------|
| 1.1 Complete Hierarchy Tree | 21-64 | ASCII tree of all entity types |
| 1.2 Hierarchy Levels | 66-78 | Level/Category/Planning Horizon table |
| 2.1 Classification Matrix | 83-98 | Container/Atomic/Quality Gates matrix |
| 2.2 Containment Rules Matrix | 100-114 | Parent/Child allowed relationships |

#### Key Content

**Entity Categories:**
- StrategicItem: Initiative, Epic, Capability, Feature
- DeliveryItem: Story, Task, Subtask, Spike, Enabler
- QualityItem: Bug
- FlowControlItem: Impediment

**Classification Matrix Properties:**
- Container (can hold children)
- Atomic (indivisible)
- Quality Gates (required for completion)
- Optional (not always needed)

#### CLAUDE.md Mapping

| Entity Hierarchy Section | CLAUDE.md Source Lines |
|--------------------------|------------------------|
| 1: Entity Hierarchy | 32-79 |
| Complete Hierarchy Tree | 34-65 |
| Hierarchy Levels | 67-79 |
| 2: Classification and Properties | 81-128 |
| Classification Matrix | 84-98 |
| Containment Rules Matrix | 100-114 |

---

### 5. worktracker-system-mappings.md

| Attribute | Value |
|-----------|-------|
| **Path** | `skills/worktracker/rules/worktracker-system-mappings.md` |
| **Lines** | 102 |
| **Purpose** | ADO Scrum, SAFe, and JIRA mappings |
| **Source Reference** | CLAUDE.md lines 131-215 |

#### Sections Covered

| Section | Lines | Content |
|---------|-------|---------|
| 3.1 Entity Mapping Table | 20-35 | Quick reference canonical to systems |
| 3.2 Mapping Complexity | 37-46 | Complexity ratings by direction |
| 4.1 Complete Entity Mapping | 49-64 | Full mapping with Native column |
| 4.1.1 ADO Scrum Entity Types | 67-77 | ADO to Canonical mapping |
| 4.1.2 SAFe Entity Types | 79-91 | SAFe to Canonical mapping |
| 4.1.3 JIRA Entity Types | 93-102 | JIRA to Canonical mapping |

#### Key Content

**Mapping Complexity Ratings:**
| Direction | Complexity |
|-----------|------------|
| Canonical to ADO | Medium |
| Canonical to SAFe | High |
| Canonical to JIRA | Medium |
| ADO to Canonical | Low |
| SAFe to Canonical | Medium |
| JIRA to Canonical | Low |

#### CLAUDE.md Mapping

| System Mappings Section | CLAUDE.md Source Lines |
|-------------------------|------------------------|
| 3: System Mapping Summary | 131-146 |
| Entity Mapping Table | 133-146 |
| Mapping Complexity | 148-156 |
| 4: System Mappings | 158-215 |
| Complete Entity Mapping | 160-175 |
| ADO Scrum Entity Types | 179-190 |
| SAFe Entity Types | 192-203 |
| JIRA Entity Types | 205-215 |

---

### 6. worktracker-templates.md

| Attribute | Value |
|-----------|-------|
| **Path** | `skills/worktracker/rules/worktracker-templates.md` |
| **Lines** | 137 |
| **Purpose** | Template locations and usage rules |
| **Source Reference** | CLAUDE.md lines 244-356 |

#### Sections Covered

| Section | Lines | Content |
|---------|-------|---------|
| Work Tracker Templates (intro) | 19-41 | Description and initial directory structure |
| Templates (MANDATORY) | 45-99 | Template usage rules and tables |
| Problem-Solving Templates | 74-91 | Knowledge templates (outside worktracker) |
| Template Usage Rules | 93-99 | 5 mandatory rules |
| Directory Structure | 101-127 | Complete ASCII tree |
| Cross-References | 131-137 | Links to other rule files |

#### Key Content

**Worktracker Templates (10 total):**
| Template | File Prefix |
|----------|-------------|
| ENABLER.md | EN-* |
| TASK.md | TASK-* |
| BUG.md | BUG-* |
| DISCOVERY.md | DISC-* |
| DECISION.md | DEC-* |
| SPIKE.md | SPIKE-* |
| EPIC.md | EPIC-* |
| FEATURE.md | FEAT-* |
| STORY.md | STORY-* |
| IMPEDIMENT.md | IMP-* |

**Problem-Solving Templates (9 total):**
- adr.md, research.md, analysis.md, deep-analysis.md
- synthesis.md, review.md, investigation.md, jrn.md
- use-case-template.md

**Template Usage Rules (5 mandatory):**
1. ALWAYS read template before creating
2. NEVER make up own format
3. INCLUDE all required sections
4. REFERENCE template in file header
5. ASK user if unsure

#### CLAUDE.md Mapping

| Templates Section | CLAUDE.md Source Lines |
|-------------------|------------------------|
| Work Tracker Templates (description) | 244-263 |
| Directory Structure (templates) | 265-281 |
| Templates (MANDATORY) | 283-356 |
| Work Tracker Templates (table) | 305-316 |
| Problem-Solving Templates | 318-330 |
| Template Usage Rules | 332-338 |
| Directory Structure (complete) | 340-356 |

---

## Content Mapping to Original CLAUDE.md

### Complete Line Mapping

| CLAUDE.md Section | Lines | Extracted To |
|-------------------|-------|--------------|
| Worktracker tag start | 30 | - |
| 1: Entity Hierarchy | 32-79 | worktracker-entity-hierarchy.md |
| 2: Entity Classification | 81-128 | worktracker-entity-hierarchy.md |
| 3: System Mapping Summary | 131-156 | worktracker-system-mappings.md |
| 4: System Mappings | 158-215 | worktracker-system-mappings.md |
| Work tracker Behavior | 218-241 | worktracker-behavior-rules.md |
| Work tracker Templates | 244-281 | worktracker-templates.md |
| Templates (MANDATORY) | 283-356 | worktracker-templates.md |
| Work tracker Directory Structure | 360-399 | worktracker-directory-structure.md |
| Worktracker tag end | 401 | - |

### Total Line Count Summary

| File | Lines |
|------|-------|
| SKILL.md | 117 |
| worktracker-behavior-rules.md | 149 |
| worktracker-directory-structure.md | 91 |
| worktracker-entity-hierarchy.md | 114 |
| worktracker-system-mappings.md | 102 |
| worktracker-templates.md | 137 |
| **TOTAL** | **710** |

### Original CLAUDE.md Lines

| Section | Lines |
|---------|-------|
| Worktracker section | 30-401 (~371 lines) |

**Expansion Factor:** 710 / 371 = **1.91x** (due to added structure, headers, and integrity rules)

---

## New Content Added (Not in Original CLAUDE.md)

### 1. Worktracker Integrity Rules (WTI-001 through WTI-006)

| Rule | Purpose | Source |
|------|---------|--------|
| WTI-001 | Real-Time State Updates | Process failure discovered during EN-201 |
| WTI-002 | No Closure Without Verification | Process failure discovered during EN-201 |
| WTI-003 | Truthful and Accurate State | Process failure discovered during EN-201 |
| WTI-004 | Synchronize Before Reporting | Process failure discovered during EN-201 |
| WTI-005 | Atomic Task State | Process failure discovered during EN-201 |
| WTI-006 | Evidence-Based Closure | Process failure discovered during EN-201 |

These 6 rules represent **~50 lines of new content** capturing learned best practices.

### 2. Folder Structure Patterns (Project-based vs Repository-based)

The original CLAUDE.md assumed project-based structure only. The extraction adds explicit documentation of both patterns with a ONE-OF relationship.

### 3. Document Section Navigation Tables

Each rule file includes a "Document Sections" table at the top for quick navigation - a UX improvement not present in original CLAUDE.md.

### 4. Cross-Reference Sections

Each rule file includes explicit cross-references to related files, improving discoverability.

---

## Loading Strategy Analysis

### Automatic Loading (via @import)

When `/worktracker` skill is invoked:
1. SKILL.md is loaded (117 lines)
2. `@rules/worktracker-behavior-rules.md` is loaded (149 lines)
3. **Total automatic load: 266 lines**

### On-Demand Loading (via reference)

The following are referenced but not auto-loaded:
- worktracker-entity-hierarchy.md (114 lines)
- worktracker-system-mappings.md (102 lines)
- worktracker-directory-structure.md (91 lines)
- worktracker-templates.md (137 lines)

**On-demand total: 444 lines**

### Context Window Impact

| Scenario | Lines Loaded |
|----------|--------------|
| Skill invoked (default) | 266 |
| All rules loaded | 710 |
| Original CLAUDE.md inline | ~371 |

**Savings:** Default load is **28% smaller** than original inline content, with full content available on-demand.

---

## Quality Assessment

### Completeness: HIGH

All original CLAUDE.md worktracker content has been extracted and is present in the skill files.

### Accuracy: HIGH

- Source line references maintained
- Content matches original with structural improvements
- No content loss detected

### Enhancements: SIGNIFICANT

- 6 new integrity rules added
- Document section navigation added
- Cross-references added
- Two placement patterns clarified

### Concerns: MINOR

1. **Duplicate template paths** in worktracker-templates.md (docs/templates vs .context/templates) - needs verification
2. **Problem-solving templates** included in worktracker skill but belong to problem-solving skill

---

## Recommendations

1. **Verify template paths** - Reconcile `docs/templates/worktracker/` vs `.context/templates/worktracker/`
2. **Consider moving problem-solving templates** to problem-solving skill or shared location
3. **Add SKILL.md to @ imports in CLAUDE.md** for automatic loading on skill invocation
4. **Document the loading strategy** explicitly in skill documentation

---

## References

- **Source:** CLAUDE.md lines 30-401
- **Extraction Date:** 2026-02-01
- **Work Item:** EN-201 (extraction) and EN-202 (rewrite)
- **Analyst:** ps-analyst agent
