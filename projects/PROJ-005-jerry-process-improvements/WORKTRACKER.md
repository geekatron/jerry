# PROJ-005: Work Item Quality Improvements -- Worktracker

> **Project:** PROJ-005-jerry-process-improvements
> **Status:** ACTIVE
> **Created:** 2026-02-16
> **Owner:** Tyler Zimmerman

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Project Summary](#project-summary) | What this project delivers |
| [Work Items](#work-items) | All tracked items with status |
| [Progress Summary](#progress-summary) | Current completion status |
| [Decisions](#decisions) | Key decisions made during project |
| [Discoveries](#discoveries) | Findings from research phase |

---

## Project Summary

Improve Jerry's worktracker work item creation quality for Bugs, PBIs (Stories), and Tasks by bringing content quality standards from the ADO skill into Jerry's rule system. This is a skill/rule-level change -- no domain model or code changes.

**Phase:** Implementation Complete

**Deliverables:**
- New content quality rule file (`worktracker-content-standards.md`)
- Two new integrity rules (WTI-007, WTI-008)
- Quick Creation Guides embedded in BUG/STORY/TASK templates
- wt-auditor content quality detection

---

## Work Items

### Epic

| ID | Type | Title | Status | Parent |
|----|------|-------|--------|--------|
| EPIC-001 | Epic | Work Item Content Quality | DONE | PROJ-005 |

### Enablers

| ID | Type | Title | Status | Parent | Phase |
|----|------|-------|--------|--------|-------|
| EN-001 | Enabler | Content Quality Rules & Standards | DONE | EPIC-001 | A (Critical Path) |
| EN-002 | Enabler | Template Quick Creation Guides | DONE | EPIC-001 | B |
| EN-003 | Enabler | Skill Integration & Auditor Enhancement | DONE | EPIC-001 | C |

### Tasks

| ID | Type | Title | Status | Parent | Complexity |
|----|------|-------|--------|--------|------------|
| TASK-001 | Task | Create worktracker-content-standards.md | DONE | EN-001 | Medium |
| TASK-002 | Task | Add WTI-007 (Content Quality Standards) to behavior-rules.md | DONE | EN-001 | Medium |
| TASK-003 | Task | Add WTI-008 (Collaboration Before Creation) to behavior-rules.md | DONE | EN-001 | Medium |
| TASK-004 | Task | Add Quick Creation Guide to BUG.md | DONE | EN-002 | Low |
| TASK-005 | Task | Add Quick Creation Guide to STORY.md + reframe DoD section | DONE | EN-002 | Low |
| TASK-006 | Task | Add Quick Creation Guide to TASK.md | DONE | EN-002 | Low |
| TASK-009 | Task | Create shared DOD.md (Definition of Done reference) | DONE | EN-002 | Low |
| TASK-007 | Task | Update SKILL.md to load content standards rule | DONE | EN-003 | Low |
| TASK-008 | Task | Add content quality audit phase to wt-auditor.md | DONE | EN-003 | High |

### Research Items (Completed)

| ID | Type | Title | Status | Output |
|----|------|-------|--------|--------|
| R-001 | Research | AC Quality Best Practices | DONE | `research/proj-005-r-001-ac-quality-best-practices.md` |
| A-001 | Analysis | Worktracker Content Quality Gap Analysis | DONE | `research/proj-005-a-001-worktracker-gap-analysis.md` |
| S-001 | Synthesis | Content Quality Research Synthesis | DONE | `research/proj-005-s-001-content-quality-synthesis.md` |

---

## Task Details

### TASK-001: Create worktracker-content-standards.md

**File:** `skills/worktracker/rules/worktracker-content-standards.md` (CREATE)
**Dependencies:** None (first in critical path)

**Acceptance Criteria:**
- [ ] File exists at `skills/worktracker/rules/worktracker-content-standards.md`
- [ ] Contains the #1 Rule: "If engineers/UX/QA need to ask clarifying questions, the AC has failed"
- [ ] Contains hard bullet limits table (Story: 5, Bug: 3, Task: 3, Enabler: 5, Feature: 5)
- [ ] Contains anti-pattern table with 5+ examples (DoD in AC, implementation details, hedge words, vague language, too broad)
- [ ] Contains concrete vs vague examples table with 6+ paired examples
- [ ] Contains AC vs DoD separation guidance with universal test
- [ ] Contains explicit guidance on where implementation details DO belong: "Implementation details belong in the Description section, Implementation Notes section, or child Task descriptions -- never in AC"
- [ ] Contains Hemingway writing style directive (short sentences, active voice, concrete nouns, no adverbs, no hedge words)
- [ ] Contains pre-finalization quality check with 4 questions: (1) Can an engineer build this without asking questions? (2) Can QA write test cases from this AC? (3) Are there any ambiguous terms remaining? (4) Is every AC bullet actionable and verifiable?
- [ ] Contains SPIDR splitting framework reference (Spike, Paths, Interfaces, Data, Rules) for scope overflow remediation
- [ ] Follows Jerry markdown-navigation-standards (Document Sections table with anchors)

### TASK-002: Add WTI-007 to behavior-rules.md

**File:** `skills/worktracker/rules/worktracker-behavior-rules.md` (MODIFY)
**Dependencies:** TASK-001

**Acceptance Criteria:**
- [ ] WTI-007 section added after WTI-006 with enforcement level HARD
- [ ] Sub-rules defined: WTI-007a (no DoD in AC), WTI-007b (no implementation details), WTI-007c (actor-first format), WTI-007d (no hedge words), WTI-007e (bullet count limits), WTI-007f (summary brevity), WTI-007g (scope overflow signal)
- [ ] WTI-007c includes explicit carve-out: "For Enablers, Features, and Tasks, the 'actor' may be a system component, infrastructure element, or process (e.g., 'Build pipeline...', 'Database migration...', 'Configuration file...')"
- [ ] Cross-references `worktracker-content-standards.md` for detailed examples and anti-patterns
- [ ] Follows the same heading pattern (`### WTI-NNN: Name (ENFORCEMENT)`), table format, anti-pattern section, and 'Why' rationale as existing WTI-001 through WTI-006

### TASK-003: Add WTI-008 to behavior-rules.md

**File:** `skills/worktracker/rules/worktracker-behavior-rules.md` (MODIFY)
**Dependencies:** TASK-001

**Acceptance Criteria:**
- [ ] WTI-008 section added after WTI-007 with enforcement level HARD
- [ ] Sub-rules defined: WTI-008a (pre-creation checkpoint), WTI-008b (AC review checkpoint), WTI-008c (missing information flag), WTI-008d (skip mechanism with quality risk acknowledgment)
- [ ] WTI-008c includes explicit sufficiency rubric with 2-3 examples: (1) INSUFFICIENT -- "create a bug for the login issue" (no symptom, steps, or location); (2) INSUFFICIENT -- "create a story for user profile editing" (no role, goal, or benefit); (3) SUFFICIENT -- user provides detailed symptom with repro steps (proceed to creation)
- [ ] Checkpoint question templates included for Stories, Bugs, and general AC review
- [ ] "(Recommended)" tag on preferred options per feedback item #7
- [ ] Skip mechanism preserves user autonomy (P-020 compliance)

### TASK-004: Add Quick Creation Guide to BUG.md

**File:** `.context/templates/worktracker/BUG.md` (MODIFY)
**Dependencies:** TASK-002 (references WTI-007 rules)

**Acceptance Criteria:**
- [ ] Quick Creation Guide section added near top of template (after frontmatter comment, before Document Sections)
- [ ] Guide specifies: 1-2 sentence summary (symptom-focused), max 3 AC bullets, 4-6 repro steps, actor/system-first AC format
- [ ] Guide includes BAD/GOOD AC examples specific to bugs
- [ ] Guide notes which sections to skip at creation time (Root Cause, Fix Description, Evidence)

### TASK-005: Add Quick Creation Guide to STORY.md + reframe DoD

**File:** `.context/templates/worktracker/STORY.md` (MODIFY)
**Dependencies:** TASK-002 (references WTI-007 rules), TASK-009 (DoD reframe cross-references DOD.md)

**Acceptance Criteria:**
- [ ] Quick Creation Guide section added near top of template
- [ ] Guide specifies: User Story format guidance (specific role, observable goal, business benefit), max 5 AC bullets, actor/system-first AC format
- [ ] Guide explicitly states: "AC must NOT contain DoD items (tests, code review, documentation, deployment)"
- [ ] Existing Definition of Done section (lines 289-313) reframed with note: "These items are team-level DoD standards. Do NOT include them in individual work item Acceptance Criteria."

### TASK-006: Add Quick Creation Guide to TASK.md

**File:** `.context/templates/worktracker/TASK.md` (MODIFY)
**Dependencies:** TASK-002 (references WTI-007 rules)

**Acceptance Criteria:**
- [ ] Quick Creation Guide section added near top of template
- [ ] Guide specifies: 1-2 sentence description, max 3 AC bullets, verification-oriented AC (not implementation-oriented)
- [ ] Guide includes BAD/GOOD AC examples specific to tasks
- [ ] Guide notes implementation details belong in Description or Implementation Notes, not AC

### TASK-009: Create shared DOD.md

**File:** `.context/templates/worktracker/DOD.md` (CREATE)
**Dependencies:** None

**Acceptance Criteria:**
- [ ] File exists at `.context/templates/worktracker/DOD.md`
- [ ] Contains team-level Definition of Done items extracted from STORY.md (lines 289-313)
- [ ] Includes items: code reviewed, tests passing, documentation updated, integration tests passing
- [ ] Explicit statement: "These items apply to ALL work items equally. They do NOT belong in individual Acceptance Criteria."
- [ ] STORY.md DoD section (TASK-005) cross-references this file

### TASK-007: Update SKILL.md to load content standards

**File:** `skills/worktracker/SKILL.md` (MODIFY)
**Dependencies:** TASK-001, TASK-002 (WTI-007 defined), TASK-003 (WTI-008 defined)

**Acceptance Criteria:**
- [ ] `@rules/worktracker-content-standards.md` added to Core Rules section
- [ ] WTI-007 and WTI-008 added to WTI Rules Enforced table
- [ ] Content quality mentioned in Core Capabilities section

### TASK-008: Add content quality audit phase to wt-auditor.md

**File:** `skills/worktracker/agents/wt-auditor.md` (MODIFY)
**Dependencies:** TASK-002 (references WTI-007 sub-rules)

**Acceptance Criteria:**
- [ ] Phase 2.5: Content Quality Check added between template compliance and relationship integrity phases
- [ ] Detection patterns specified for: DoD in AC (WTI-007a), implementation details (WTI-007b), hedge words (WTI-007d), AC bullet count (WTI-007e), summary length (WTI-007f)
- [ ] Content quality issues included in audit report format with file, sub-rule, matched text, and remediation columns
- [ ] Severity levels appropriate: bullet count and DoD detection as WARNING, hedge words and actor-format as INFO

---

## Progress Summary

```
Research Phase:    [####################] 100%
Planning Phase:    [####################] 100%
Implementation:    [####################] 100%
```

**Overall:** All 9 implementation tasks across 3 enablers complete. 7 files modified, 2 files created.

---

## Decisions

| ID | Decision | Rationale | Date |
|----|----------|-----------|------|
| DEC-001 | Target Jerry's worktracker, not ADO skill | ADO skill already has content standards; Jerry's worktracker has zero | 2026-02-16 |
| DEC-002 | Two consolidated rules (WTI-007, WTI-008) with sub-rules instead of six separate rules | Avoid rule proliferation; sub-rules provide granularity without overhead | 2026-02-16 |
| DEC-003 | Embed Quick Creation Guides in existing templates (not separate files) | Avoids file sprawl; Claude reads the guide first when opening template | 2026-02-16 |
| DEC-004 | Separate content-standards.md reference file | Keep behavior-rules.md focused on rule definitions; detailed examples/anti-patterns in reference file | 2026-02-16 |
| DEC-005 | Tiered collaboration checkpoints with skip mechanism | Rubber-stamp risk from research; user autonomy (P-020); skip preserves flow | 2026-02-16 |
| DEC-006 | WTI-007/008 apply to newly created items only; wt-auditor flags existing violations as INFO (advisory) | Avoids remediation avalanche on historical items; nse-reviewer Gap 3 | 2026-02-16 |
| DEC-007 | WTI-008 checkpoints apply to: Story (PBI), Bug, Task, Enabler, Feature. NOT: Discovery, Decision, Impediment, Sub-Task | Only AC-bearing work items need collaboration checkpoints; ADO types are PBI, Bug, Task; nse-reviewer Gap 5 | 2026-02-16 |

---

## Discoveries

| ID | Finding | Source | Impact |
|----|---------|--------|--------|
| DISC-001 | STORY.md DoD section (lines 289-313) actively teaches AC/DoD conflation | ps-analyst gap analysis | Must reframe; root cause of "DoD items in AC" complaints |
| DISC-002 | Only 38-47% of template content is creation-relevant | ps-analyst template effectiveness analysis | Validates Quick Creation Guide approach |
| DISC-003 | LLMs achieve kappa 0.84-0.87 when given explicit quality criteria | ps-researcher (Springer JIIS 2025) | Quality rules MUST be explicit and measurable |
| DISC-004 | Industry consensus on 3-5 AC bullets; 6+ signals scope issue | ps-researcher (Scrum.org, AltexSoft) | Validates ADO skill's hard limits approach |
| DISC-005 | Rubber-stamp risk: zero-override rate signals blind trust, not perfection | ps-researcher (CyberManiacs) | Checkpoints must be smart, not blanket approval |
| DISC-006 | Diataxis framework: reference vs how-to guide separation | ps-researcher (Diataxis.fr) | Templates are reference; need how-to creation guides |

---

## Bugs

*None yet.*
