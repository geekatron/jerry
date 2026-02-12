# New CLAUDE.md Inventory

> **TASK-004**: Extract and catalog ALL content from the NEW CLAUDE.md
> **Date**: 2026-02-01
> **Status**: Complete

---

## Document Overview

| Metric | Value |
|--------|-------|
| **Total Lines** | 81 (including blank lines) |
| **Content Lines** | ~65 |
| **Total Sections** | 6 |
| **Target Reduction** | From ~1,500+ lines to 81 lines (95% reduction) |

---

## Section-by-Section Inventory

### 1. Header & Identity (Lines 1-11)

| Attribute | Value |
|-----------|-------|
| **Line Range** | 1-11 |
| **Line Count** | 11 |
| **Purpose** | Document title, one-line description, core problem/solution |

**Content Summary:**
- Title: "CLAUDE.md - Jerry Framework Root Context"
- Descriptor: "Procedural memory for Claude Code. Loaded once at session start."
- **Identity Statement**: Jerry is a framework for behavior and workflow guardrails
- **Core Problem**: Context Rot - LLM performance degrades as context fills
- **Core Solution**: Filesystem as infinite memory (persist to files, load selectively)

**External References:**
| Reference | Type | Purpose |
|-----------|------|---------|
| [Chroma Research](https://research.trychroma.com/context-rot) | External URL | Context rot research citation |

---

### 2. Navigation (Lines 13-30)

| Attribute | Value |
|-----------|-------|
| **Line Range** | 13-30 |
| **Line Count** | 18 |
| **Purpose** | Pointer table to find information by need |

**Content Summary:**
- Philosophy: "Find information rather than reading it here"
- Auto-loaded content marked with (A)
- Navigation table with 9 entries

**Navigation Table Content:**

| Need | Location | Type |
|------|----------|------|
| Coding standards | `.claude/rules/` | Auto-loaded (A) |
| Work tracking | `/worktracker` skill | Skill invocation |
| Problem solving | `/problem-solving` skill | Skill invocation |
| Architecture | `/architecture` skill | Skill invocation |
| NASA SE | `/nasa-se` skill | Skill invocation |
| Orchestration | `/orchestration` skill | Skill invocation |
| Transcript | `/transcript` skill | Skill invocation |
| Templates | `.context/templates/` | Directory pointer |
| Knowledge | `docs/knowledge/` | Directory pointer |
| Governance | `docs/governance/JERRY_CONSTITUTION.md` | File pointer |

**Key Annotation:**
- `(A)` = Auto-loaded content
- Skills reference `skills/{skill-name}/SKILL.md`

---

### 3. Active Project (Lines 32-44)

| Attribute | Value |
|-----------|-------|
| **Line Range** | 32-44 |
| **Line Count** | 13 |
| **Purpose** | Project context enforcement and hook behavior |

**Content Summary:**
- Environment variable: `JERRY_PROJECT=PROJ-001-example`
- SessionStart hook provides context via XML tags
- Hard rule: Claude MUST NOT proceed without active project

**XML Tag Table:**

| Tag | Meaning | Claude Action |
|-----|---------|---------------|
| `<project-context>` | Valid project active | Proceed with work |
| `<project-required>` | No project set | Use AskUserQuestion to select/create |
| `<project-error>` | Invalid project ID | Help user fix or select valid project |

**External References:**
| Reference | Type | Purpose |
|-----------|------|---------|
| `scripts/session_start_hook.py` | Script | Hook implementation |
| `projects/README.md` | File | Project registry |

---

### 4. Critical Constraints (Lines 46-66)

| Attribute | Value |
|-----------|-------|
| **Line Range** | 46-66 |
| **Line Count** | 21 |
| **Purpose** | Non-overridable rules and Python environment |

**Content Summary:**
- Section marked as HARD constraints (cannot be overridden)
- 3 core principles with descriptions
- Python environment requirements with examples

**Principles Table:**

| Principle | Constraint | Rule |
|-----------|------------|------|
| **P-003** | No Recursive Subagents | Max ONE level: orchestrator -> worker |
| **P-020** | User Authority | User decides. Never override. Ask before destructive ops |
| **P-022** | No Deception | Never deceive about actions, capabilities, or confidence |

**Python Environment (Subsection):**
- Requirement: Python 3.11+ with UV only
- FORBIDDEN: `python`, `pip`, `pip3` commands directly
- CORRECT examples provided in code block

**External References:**
| Reference | Type | Purpose |
|-----------|------|---------|
| `docs/governance/JERRY_CONSTITUTION.md` | File | Full governance document |

---

### 5. Quick Reference (Lines 68-80)

| Attribute | Value |
|-----------|-------|
| **Line Range** | 68-80 |
| **Line Count** | 13 |
| **Purpose** | CLI commands and skill summary table |

**Content Summary:**
- CLI version: v0.1.0
- CLI command summary (single line)
- Skills table with 6 entries

**CLI Commands:**

| Namespace | Commands |
|-----------|----------|
| `jerry session` | start, end, status, abandon |
| `jerry items` | list, show |
| `jerry projects` | list, context, validate |

**Skills Table:**

| Skill | Purpose |
|-------|---------|
| `/worktracker` | Task/issue management |
| `/problem-solving` | Research, analysis, root cause |
| `/nasa-se` | Requirements, V&V, reviews |
| `/orchestration` | Multi-phase workflows |
| `/architecture` | Design decisions |
| `/transcript` | Transcription parsing |

**External References:**
| Reference | Type | Purpose |
|-----------|------|---------|
| `skills/` directory | Directory | Skill details |

---

## Complete Reference Index

### Files Referenced

| File/Directory | Section | Purpose |
|----------------|---------|---------|
| `.claude/rules/` | Navigation | Coding standards (auto-loaded) |
| `.context/templates/` | Navigation | Templates |
| `docs/knowledge/` | Navigation | Knowledge base |
| `docs/governance/JERRY_CONSTITUTION.md` | Navigation, Critical Constraints | Governance |
| `scripts/session_start_hook.py` | Active Project | Hook implementation |
| `projects/README.md` | Active Project | Project registry |
| `skills/` | Quick Reference | Skill implementations |
| `skills/{skill-name}/SKILL.md` | Navigation | Individual skill docs |

### Skills Referenced

| Skill Command | Referenced In | Purpose |
|---------------|---------------|---------|
| `/worktracker` | Navigation, Quick Reference | Task/issue management |
| `/problem-solving` | Navigation, Quick Reference | Research, analysis, root cause |
| `/architecture` | Navigation, Quick Reference | Design decisions |
| `/nasa-se` | Navigation, Quick Reference | Requirements, V&V, reviews |
| `/orchestration` | Navigation, Quick Reference | Multi-phase workflows |
| `/transcript` | Navigation, Quick Reference | Transcription parsing |

### External URLs

| URL | Section | Purpose |
|-----|---------|---------|
| https://research.trychroma.com/context-rot | Identity | Context rot research |

---

## Content Categorization

### What IS Included (New File)

| Category | Content | Line Count |
|----------|---------|------------|
| Identity | What Jerry is, core problem/solution | 7 |
| Navigation | Pointer table to resources | 14 |
| Project Rules | Environment variable, hook behavior | 11 |
| Hard Constraints | P-003, P-020, P-022, Python env | 19 |
| Quick Reference | CLI commands, skills summary | 11 |

### What is DELEGATED (Not Inline)

| Topic | Delegated To |
|-------|--------------|
| Work Tracker entity hierarchy | `/worktracker` skill |
| Work Tracker directory structure | `/worktracker` skill |
| Work Tracker templates | `.context/templates/` |
| TODO list requirements | `/worktracker` skill |
| Mandatory skill usage details | Individual skill files |
| Full CLI documentation | CLI help / skill |
| Agent registry | `AGENTS.md` |
| Full governance | `docs/governance/JERRY_CONSTITUTION.md` |
| Architecture details | `/architecture` skill, `.claude/rules/` |
| Coding standards | `.claude/rules/` (auto-loaded) |

---

## Design Observations

### Compression Strategies Used

1. **Pointer Pattern**: Replace inline content with navigation table
2. **Skill Delegation**: Detailed workflows moved to skill SKILL.md files
3. **Auto-load Annotation**: Mark what Claude loads automatically
4. **Table Format**: Dense information in scannable tables
5. **Single-line Examples**: CLI examples condensed to one line
6. **Reference Consolidation**: Multiple references to same file consolidated

### Information Density

| Section | Lines | Information Items | Items/Line Ratio |
|---------|-------|-------------------|------------------|
| Identity | 11 | 4 (title, descriptor, problem, solution) | 0.36 |
| Navigation | 18 | 11 (9 locations + 2 annotations) | 0.61 |
| Active Project | 13 | 6 (env var, 3 tags, hard rule, ref) | 0.46 |
| Critical Constraints | 21 | 9 (3 principles, Python rule, 3 examples, ref) | 0.43 |
| Quick Reference | 13 | 10 (CLI + 6 skills + 3 command groups) | 0.77 |

**Average Items/Line**: 0.53 (highly dense)

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total lines | 81 |
| Total sections | 6 |
| Tables used | 6 |
| Code blocks | 1 |
| Files referenced | 8+ |
| Skills referenced | 6 |
| External URLs | 1 |
| Hard constraints documented | 4 (P-003, P-020, P-022, Python) |

---

*Generated: 2026-02-01*
*Task: TASK-004 of EN-202 Gap Analysis*
