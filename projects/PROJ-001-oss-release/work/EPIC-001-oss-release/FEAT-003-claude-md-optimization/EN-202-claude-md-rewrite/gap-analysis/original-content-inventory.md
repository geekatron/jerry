# CLAUDE.md Original Content Inventory

> **Purpose:** Comprehensive catalog of all sections in CLAUDE.md.backup for gap analysis
> **Task:** TASK-001 - Extract and catalog ALL sections from the original CLAUDE.md backup
> **Created:** 2026-02-01
> **Source File:** `CLAUDE.md.backup`
> **Total Lines:** 915

---

## Executive Summary

The original CLAUDE.md file contains **915 lines** organized into **12 major sections** with extensive subsections. The content spans worktracker specifications, architecture documentation, project workflows, skill references, CLI documentation, and governance principles.

---

## Section Inventory

| # | Section Heading | Line Start | Line End | Approx Lines | Category | Key Content |
|---|-----------------|------------|----------|--------------|----------|-------------|
| 1 | **# CLAUDE.md - Jerry Framework Root Context** | 1 | 6 | 6 | PROJECT_WORKFLOW | Header, procedural memory note |
| 2 | **## Project Overview** | 8 | 25 | 18 | PROJECT_WORKFLOW | Jerry definition, Context Rot problem, core solutions |
| 2.1 | ### Core Problem: Context Rot | 13 | 24 | 12 | PROJECT_WORKFLOW | Chroma Research citation, 4 solutions |
| 3 | **## Worktracker** | 27 | 401 | 375 | WORKTRACKER | Complete worktracker specification (XML-wrapped) |
| 3.1 | ### 1: Entity Hierarchy | 32 | 92 | 61 | WORKTRACKER | Complete Hierarchy Tree (ASCII), Hierarchy Levels table |
| 3.1.1 | #### 1.1 Complete Hierarchy Tree | 34 | 78 | 45 | WORKTRACKER | WorkItem abstract tree with all entity types |
| 3.1.2 | #### 1.2 Hierarchy Levels | 80 | 92 | 13 | WORKTRACKER | L0-L5 level definitions table |
| 3.2 | ### 2: Entity Classification and Properties | 95 | 128 | 34 | WORKTRACKER | Classification Matrix, Containment Rules |
| 3.2.1 | #### 2.1 Classification Matrix | 97 | 112 | 16 | WORKTRACKER | Entity properties table |
| 3.2.2 | #### 2.2 Containment Rules Matrix | 113 | 128 | 16 | WORKTRACKER | Parent-child relationships |
| 3.3 | ### 3: System Mapping Summary | 131 | 159 | 29 | WORKTRACKER | Entity Mapping Table, Mapping Complexity |
| 3.3.1 | #### 3.1 Entity Mapping Table | 133 | 148 | 16 | WORKTRACKER | Canonical to ADO/SAFe/JIRA mapping |
| 3.3.2 | #### 3.2 Mapping Complexity | 149 | 159 | 11 | WORKTRACKER | Complexity by direction |
| 3.4 | ### 4. System Mappings | 160 | 215 | 56 | WORKTRACKER | Complete entity mapping with notes |
| 3.4.1 | #### 4.1 Complete Entity Mapping | 162 | 177 | 16 | WORKTRACKER | Full mapping table with Native column |
| 3.4.2 | #### 4.1. Entity Mapping by System | 178 | 215 | 38 | WORKTRACKER | ADO, SAFe, JIRA specific mappings |
| 3.4.2.1 | ##### 4.1.1 ADO Scrum Entity Types | 180 | 190 | 11 | WORKTRACKER | ADO to Canonical mapping |
| 3.4.2.2 | ##### 4.1.2 SAFe Entity Types | 191 | 204 | 14 | WORKTRACKER | SAFe to Canonical mapping |
| 3.4.2.3 | ##### 4.1.3 JIRA Entity Types | 205 | 215 | 11 | WORKTRACKER | JIRA to Canonical mapping |
| 3.5 | ### Work tracker (worktracker) Behavior | 218 | 241 | 24 | WORKTRACKER | Canonical model usage, WORKTRACKER.md structure, MCP Memory-Keeper |
| 3.6 | ### Work Tracker (worktracker) Templates | 244 | 267 | 24 | WORKTRACKER | Template location, directory structure |
| 4 | **## Work tracker (worktracker) Directory Structure** | 270 | 272 | 3 | WORKTRACKER | Empty section (duplicate header) |
| 5 | **## Templates (MANDATORY)** | 274 | 357 | 84 | WORKTRACKER | Critical template usage rules |
| 5.1 | ### Work Tracker (worktracker) Templates | 279 | 302 | 24 | WORKTRACKER | Template table with paths |
| 5.2 | ### Problem-Solving & Knowledge Templates | 303 | 320 | 18 | WORKTRACKER | Problem-solving template table |
| 5.3 | ### Template Usage Rules | 321 | 328 | 8 | WORKTRACKER | 5 mandatory rules |
| 5.4 | ### Directory Structure | 329 | 357 | 29 | WORKTRACKER | Combined template directory tree |
| 6 | **## Work tracker (worktracker) Directory Structure** | 360 | 401 | 42 | WORKTRACKER | Full worktracker directory structure with examples |
| 7 | **## `<todo>`** | 405 | 438 | 34 | PROJECT_WORKFLOW | META TODO requirements (XML-wrapped) |
| 8 | **## Architecture** | 442 | 472 | 31 | STANDARDS | Directory structure, Key Design Principles |
| 8.1 | ### Key Design Principles | 458 | 472 | 15 | STANDARDS | Hexagonal, Zero-Dependency, CQRS |
| 9 | **## Working with Jerry** | 475 | 520 | 46 | PROJECT_WORKFLOW | Project-based workflow guidance |
| 9.1 | ### Project-Based Workflow | 477 | 492 | 16 | PROJECT_WORKFLOW | Active project resolution, structure |
| 9.2 | ### Before Starting Work | 494 | 500 | 7 | PROJECT_WORKFLOW | 4-step checklist |
| 9.3 | ### During Work | 501 | 506 | 6 | PROJECT_WORKFLOW | 3-step workflow |
| 9.4 | ### After Completing Work | 507 | 512 | 6 | PROJECT_WORKFLOW | 3-step completion |
| 9.5 | ### Creating a New Project | 513 | 520 | 8 | PROJECT_WORKFLOW | 5-step creation flow |
| 10 | **## Project Enforcement (Hard Rule)** | 523 | 651 | 129 | PROJECT_WORKFLOW | Hook output format, AskUserQuestion flow |
| 10.1 | ### Hook Output Format | 533 | 603 | 71 | PROJECT_WORKFLOW | JSON format, project-context, project-required, project-error |
| 10.1.1 | #### `<project-context>` - Valid Project Active | 550 | 563 | 14 | PROJECT_WORKFLOW | Valid project example |
| 10.1.2 | #### `<project-required>` - No Project Selected | 564 | 584 | 21 | PROJECT_WORKFLOW | No project example |
| 10.1.3 | #### `<project-error>` - Invalid Project Specified | 585 | 603 | 19 | PROJECT_WORKFLOW | Invalid project example |
| 10.2 | ### Required AskUserQuestion Flow | 604 | 627 | 24 | PROJECT_WORKFLOW | 4-step flow, YAML example |
| 10.3 | ### Project Creation Flow | 629 | 651 | 23 | PROJECT_WORKFLOW | 5-step creation with structure |
| 11 | **## Skills Available** | 654 | 664 | 11 | SKILLS | Skills table (6 skills) |
| 12 | **## Mandatory Skill Usage (PROACTIVE)** | 667 | 774 | 108 | SKILLS | Critical skill usage requirements |
| 12.1 | ### /problem-solving (MANDATORY for Research/Analysis) | 672 | 692 | 21 | SKILLS | Use cases, provides, triggers |
| 12.2 | ### @nasa-se (MANDATORY for Requirements/Design) | 693 | 717 | 25 | SKILLS | Use cases, provides, triggers |
| 12.3 | ### @orchestration (MANDATORY for Multi-Step Workflows) | 718 | 739 | 22 | SKILLS | Use cases, provides, triggers |
| 12.4 | ### Skill Usage Behavior Rules | 740 | 747 | 8 | SKILLS | 5 behavior rules |
| 12.5 | ### Example: Starting a New Feature | 748 | 760 | 13 | SKILLS | Code example with checkmarks |
| 13 | **### Orchestration Skill Details** | 763 | 774 | 12 | SKILLS | Detailed orchestration artifacts |
| 14 | **## Agents Available** | 777 | 786 | 10 | SKILLS | Agent registry reference |
| 15 | **## Code Standards** | 789 | 798 | 10 | STANDARDS | Quick reference, link to rules file |
| 16 | **## CLI Commands (v0.1.0)** | 801 | 858 | 58 | CLI | Full CLI reference |
| 16.1 | ### Session Namespace | 809 | 818 | 10 | CLI | 4 session commands |
| 16.2 | ### Items Namespace | 819 | 832 | 14 | CLI | 5 items commands |
| 16.3 | ### Projects Namespace | 833 | 842 | 10 | CLI | 3 projects commands |
| 16.4 | ### Global Options | 843 | 850 | 8 | CLI | 3 global options |
| 16.5 | ### Exit Codes | 851 | 858 | 8 | CLI | Exit code table |
| 17 | **## Agent Governance (Jerry Constitution)** | 861 | 907 | 47 | GOVERNANCE | Constitution principles, validation |
| 17.1 | ### Core Principles (Quick Reference) | 867 | 877 | 11 | GOVERNANCE | Principle table |
| 17.2 | ### Hard Principles (Cannot Override) | 879 | 883 | 5 | GOVERNANCE | 3 hard principles |
| 17.3 | ### Self-Critique Protocol | 884 | 895 | 12 | GOVERNANCE | 5-point checklist |
| 17.4 | ### Behavioral Validation | 896 | 907 | 12 | GOVERNANCE | Test scenarios, prior art links |
| 18 | **## References** | 910 | 915 | 6 | STANDARDS | 3 external references |

---

## Category Summary

| Category | Section Count | Total Lines (approx) | Percentage |
|----------|--------------|---------------------|------------|
| **WORKTRACKER** | 24 subsections | ~560 | 61% |
| **PROJECT_WORKFLOW** | 12 subsections | ~240 | 26% |
| **SKILLS** | 7 subsections | ~140 | 15% |
| **STANDARDS** | 3 subsections | ~45 | 5% |
| **CLI** | 6 subsections | ~60 | 7% |
| **GOVERNANCE** | 5 subsections | ~50 | 5% |

> Note: Some sections overlap categories. The WORKTRACKER content dominates the file.

---

## Content Type Analysis

### Heavily Duplicated Content

| Content | Occurrences | Lines Duplicated |
|---------|-------------|------------------|
| Work Tracker Templates section | 2 | ~24 lines each |
| Work Tracker Directory Structure header | 2 | ~40 lines |
| Entity Mapping tables | 2 | ~60 lines (3.1 vs 4.1) |

### External Reference Files

| Referenced File | Section | Purpose |
|-----------------|---------|---------|
| `.claude/rules/coding-standards.md` | Code Standards | Detailed coding rules |
| `skills/worktracker/SKILL.md` | Skills Available | Worktracker skill |
| `skills/architecture/SKILL.md` | Skills Available | Architecture skill |
| `skills/problem-solving/SKILL.md` | Skills Available | Problem-solving skill |
| `skills/nasa-se/` | Skills Available | NASA SE skill |
| `skills/orchestration/SKILL.md` | Skills Available | Orchestration skill |
| `skills/transcript/SKILL.md` | Skills Available | Transcript skill |
| `skills/orchestration/PLAYBOOK.md` | Orchestration Details | Step-by-step guidance |
| `docs/governance/JERRY_CONSTITUTION.md` | Agent Governance | Full constitution |
| `docs/governance/BEHAVIOR_TESTS.md` | Behavioral Validation | Test scenarios |
| `docs/design/ADR-002-project-enforcement.md` | Project Enforcement | ADR reference |
| `AGENTS.md` | Agents Available | Agent registry |
| `projects/README.md` | Project workflow | Project registry |

---

## XML-Wrapped Sections

| Tag | Line Range | Purpose | Lines |
|-----|------------|---------|-------|
| `<worktracker>` | 30-401 | Complete worktracker specification | 372 |
| `<todo>` | 405-438 | META TODO requirements | 34 |

---

## Tables Inventory

| Table Name | Section | Rows | Columns |
|------------|---------|------|---------|
| Hierarchy Levels | 1.2 | 8 | 5 |
| Classification Matrix | 2.1 | 12 | 7 |
| Containment Rules Matrix | 2.2 | 12 | 2 |
| Entity Mapping Table | 3.1 | 12 | 4 |
| Mapping Complexity | 3.2 | 6 | 3 |
| Complete Entity Mapping | 4.1 | 12 | 6 |
| ADO Scrum Entity Types | 4.1.1 | 7 | 3 |
| SAFe Entity Types | 4.1.2 | 10 | 3 |
| JIRA Entity Types | 4.1.3 | 7 | 3 |
| Work Tracker Templates | Templates | 10 | 3 |
| Problem-Solving Templates | Templates | 9 | 3 |
| Skills Available | Skills | 6 | 3 |
| Agent Registry | Agents | 1 | 3 |
| Core Principles | Governance | 6 | 3 |
| Exit Codes | CLI | 3 | 2 |

---

## Code Blocks Inventory

| Type | Section | Lines | Description |
|------|---------|-------|-------------|
| ASCII Tree | 1.1 | 43 | WorkItem hierarchy |
| Directory Tree | Templates (3.6) | 14 | Template directory |
| Directory Tree | Templates (5.4) | 24 | Combined template directory |
| Directory Tree | Worktracker Dir (6) | 37 | Full worktracker structure |
| Directory Tree | Architecture | 13 | jerry/ root structure |
| Directory Tree | Project Structure | 5 | projects/PROJ-{nnn}-{slug}/ |
| JSON | Hook Output | 10 | Hook output format example |
| Markup | project-context | 8 | Valid project example |
| Markup | project-required | 15 | No project example |
| Markup | project-error | 13 | Invalid project example |
| YAML | AskUserQuestion | 8 | Example structure |
| Directory Tree | Project Creation | 5 | New project structure |
| Bash | Session Namespace | 4 | CLI commands |
| Bash | Items Namespace | 5 | CLI commands |
| Bash | Projects Namespace | 3 | CLI commands |
| Bash | Global Options | 3 | CLI commands |
| Markdown | Self-Critique | 5 | Checklist |
| Pseudo-code | Skill Example | 8 | Internal process |

---

## Key Findings

### 1. Massive Worktracker Section (61%)
The `<worktracker>` XML section consumes 372 lines (40% of the file) and contains highly detailed entity hierarchies, mappings, and directory structures that could be:
- Moved to `.claude/rules/worktracker-standards.md`
- Summarized in CLAUDE.md with reference links

### 2. Significant Duplication
- Work Tracker Templates section appears twice (lines 244-267 and 279-302)
- Entity Mapping appears twice with different levels of detail
- Work Tracker Directory Structure header appears twice

### 3. External References Already Exist
Many sections reference external files that contain the full details:
- Coding standards → `.claude/rules/coding-standards.md`
- Constitution → `docs/governance/JERRY_CONSTITUTION.md`
- Skills → individual SKILL.md files

### 4. Project Enforcement Over-Documentation
The Project Enforcement section (129 lines) contains detailed examples that could be moved to the referenced ADR.

### 5. META TODO Section
The `<todo>` section (34 lines) contains extensive behavioral requirements that could be:
- Kept as essential procedural memory
- Consolidated with related governance content

---

## Recommendations for Optimization

Based on this inventory:

1. **Extract Worktracker** → Create `.claude/rules/worktracker-standards.md`
2. **Remove Duplicates** → Eliminate repeated template/directory sections
3. **Consolidate Mappings** → Single comprehensive mapping section
4. **Summarize with Links** → Replace detailed sections with summaries + file references
5. **Keep Critical Sections** → Project Overview, Architecture, TODO, Governance summaries
6. **Inline-Reference Pattern** → Use `See: {file}` pattern for detailed content

---

## File Metadata

- **Total Lines:** 915
- **Character Count:** ~45,000 (estimated)
- **Token Estimate:** ~12,000-15,000 tokens
- **Major Sections:** 18
- **Subsections:** ~60
- **Tables:** 15
- **Code Blocks:** 18
- **External References:** 13 files
