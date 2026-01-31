# FEAT-002:DISC-003: Quality Artifact Folder Structure Precedence

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9, worktracker.md (Discovery File)
PURPOSE: Root cause analysis of skill convention violation and establishment of folder structure precedence
-->

> **Type:** discovery
> **Status:** VALIDATED
> **Priority:** CRITICAL
> **Impact:** CRITICAL
> **Created:** 2026-01-28T12:00:00Z
> **Completed:** 2026-01-28T14:00:00Z
> **Parent:** FEAT-002
> **Owner:** Claude
> **Source:** EN-008 GATE-5 Quality Review Failure Analysis

---

## Frontmatter

```yaml
# =============================================================================
# DISCOVERY WORK ITEM
# Source: ONTOLOGY-v1.md Section 3.4.9 (Discovery Entity Schema)
# Purpose: Root cause analysis of agent context loss and skill convention violation
# =============================================================================

id: "FEAT-002:DISC-003"
work_type: DISCOVERY
title: "Quality Artifact Folder Structure Precedence"

classification: TECHNICAL
status: VALIDATED
resolution: CORRECTIVE_ACTION_IMPLEMENTED
priority: CRITICAL
impact: CRITICAL

assignee: "Claude"
created_by: "Claude"

created_at: "2026-01-28T12:00:00Z"
updated_at: "2026-01-28T14:00:00Z"
completed_at: "2026-01-28T14:00:00Z"

parent_id: "FEAT-002"

tags: ["process", "quality", "folder-structure", "precedence", "context-rot", "skill-compliance", "root-cause-analysis"]

finding_type: GAP
confidence_level: HIGH
source: "EN-008 GATE-5 Quality Review"
research_method: "Root cause analysis (5W2H, Ishikawa, FMEA, 8D)"
validated: true
validation_date: "2026-01-28T14:00:00Z"
validated_by: "User"
```

---

## Summary

During EN-008 GATE-5 quality review execution, Claude (the AI agent) violated established skill conventions for quality artifact placement despite having loaded the problem-solving and nasa-se skills. This discovery performs root cause analysis using 5W2H, Ishikawa, FMEA, and 8D frameworks to understand the systemic failure and establish corrective actions.

**Core Problem Statement:**
Claude loaded skills containing explicit output location patterns but failed to apply them, instead inventing ad-hoc naming conventions that violated established SOP.

**Key Findings:**
1. Skills were loaded but not internalized - instructions read but not applied
2. Context rot degraded procedural memory across long orchestration sessions
3. No validation checkpoint exists to verify artifact placement before file creation
4. ORCHESTRATION.yaml was not maintained as SSOT, allowing state drift

**Validation:** User identified SOP breach; corrective action verified through file remediation

---

## Context

### Background

During the FEAT-002 orchestration workflow, Claude executed quality reviews for EN-007 and EN-008 using ps-critic and nse-qa agents. The skills were loaded via `/problem-solving` and `/nasa-se` skill invocations. These skills contain explicit output location specifications:

- **ps-critic.md line 59:** `location: "projects/${JERRY_PROJECT}/critiques/{ps-id}-{entry-id}-{iteration}-critique.md"`
- **nse-qa.md line 85:** `location: "projects/${JERRY_PROJECT}/qa/{proj-id}-{entry-id}-{artifact-type}-qa.md"`

Despite this information being available in loaded context, Claude created files with incorrect names in incorrect locations:
- `EN-008-entity-extraction/EN-008-ps-critic-report.md` (WRONG)
- `EN-008-entity-extraction/EN-008-nse-qa-report.md` (WRONG)

### Research Question

**Primary:** Why did Claude fail to follow skill-defined conventions despite having explicit instructions in loaded context?

**Secondary:** What systemic failures enabled this violation, and how can similar failures be prevented?

### Investigation Approach

1. **5W2H Analysis** - Comprehensive situation analysis
2. **Ishikawa Diagram** - Root cause identification (fishbone)
3. **FMEA** - Failure mode severity and prevention analysis
4. **8D Problem Solving** - Structured corrective action framework

---

## 5W2H Analysis

### WHO

| Aspect | Detail |
|--------|--------|
| **Who failed?** | Claude (AI agent executing orchestration workflow) |
| **Who detected?** | User (during GATE-5 review preparation) |
| **Who is affected?** | All future quality review workflows; automation tooling |
| **Who is responsible?** | Claude (execution); User (oversight); Framework (design) |

### WHAT

| Aspect | Detail |
|--------|--------|
| **What happened?** | Quality review files created with wrong names in wrong locations |
| **What was expected?** | Files in `critiques/` and `qa/` subdirectories per skill definitions |
| **What was actual?** | Files in enabler root with enabler-prefixed naming |
| **What was the deviation?** | Invented ad-hoc convention instead of following loaded skill instructions |

**Specific Deviations:**

| Expected (per skill) | Actual (created) |
|---------------------|------------------|
| `critiques/en008-gate5-iter1-critique.md` | `EN-008-ps-critic-report.md` |
| `qa/proj008-en008-implementation-qa.md` | `EN-008-nse-qa-report.md` |

### WHEN

| Aspect | Detail |
|--------|--------|
| **When did failure occur?** | During EN-008 quality review execution (2026-01-28) |
| **When was it detected?** | During GATE-5 preparation when user reviewed artifacts |
| **When in workflow?** | Late in orchestration (after EN-007 and EN-008 implementation complete) |
| **Context window state?** | Significant context consumed by prior work; approaching compaction |

### WHERE

| Aspect | Detail |
|--------|--------|
| **Where in codebase?** | `projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-002-implementation/EN-008-entity-extraction/` |
| **Where in workflow?** | Quality review phase of GATE-5 preparation |
| **Where in skill?** | ps-critic (line 59), nse-qa (line 85) define correct locations |
| **Where in memory?** | Skill instructions loaded but not internalized in procedural memory |

### WHY (Initial)

| Aspect | Detail |
|--------|--------|
| **Why was convention violated?** | Agent did not reference skill output specifications before creating files |
| **Why wasn't skill referenced?** | Context rot degraded awareness of loaded skill details |
| **Why no validation?** | No checkpoint to verify artifact paths before creation |
| **Why wasn't ORCHESTRATION.yaml used?** | State management discipline degraded during long session |

### HOW

| Aspect | Detail |
|--------|--------|
| **How did failure manifest?** | Files created with plausible but incorrect naming |
| **How was it detected?** | User visual inspection during GATE preparation |
| **How could it have been prevented?** | Pre-creation validation against skill definitions |
| **How was it corrected?** | Manual file move/rename; DISC-003 documentation |

### HOW MUCH

| Aspect | Detail |
|--------|--------|
| **How many files affected?** | 4 files (2 per enabler: EN-007, EN-008) |
| **How much rework required?** | ~30 minutes to remediate files and update references |
| **How much risk introduced?** | HIGH - automation tooling would fail to find artifacts |
| **How much pattern propagation?** | Would have corrupted all future GATE reviews without correction |

---

## Ishikawa (Fishbone) Root Cause Analysis

```
                                    QUALITY ARTIFACT
                                    PLACEMENT FAILURE
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         │                                 │                                 │
    ┌────┴────┐                      ┌─────┴─────┐                     ┌─────┴─────┐
    │ PEOPLE  │                      │  PROCESS  │                     │ TECHNOLOGY│
    └────┬────┘                      └─────┬─────┘                     └─────┬─────┘
         │                                 │                                 │
    ┌────┴──────────────┐            ┌─────┴──────────────┐           ┌─────┴──────────────┐
    │ Claude did not    │            │ No validation      │           │ Context window     │
    │ reference skill   │            │ checkpoint before  │           │ limitations cause  │
    │ before creating   │            │ file creation      │           │ context rot        │
    │ files             │            └────────────────────┘           └────────────────────┘
    └───────────────────┘                    │                               │
         │                           ┌───────┴──────────────┐         ┌─────┴──────────────┐
    ┌────┴──────────────┐            │ ORCHESTRATION.yaml  │         │ Skill instructions │
    │ Context rot       │            │ not maintained as   │         │ loaded but not     │
    │ degraded memory   │            │ SSOT during session │         │ internalized       │
    │ of skill details  │            └────────────────────┘           └────────────────────┘
    └───────────────────┘                    │                               │
         │                           ┌───────┴──────────────┐         ┌─────┴──────────────┐
    ┌────┴──────────────┐            │ No explicit         │         │ No automated       │
    │ User assumed      │            │ "verify skill       │         │ path validation    │
    │ Claude would      │            │ conventions" step   │         │ in Write tool      │
    │ follow SOP        │            │ in workflow         │         │ invocation         │
    └───────────────────┘            └────────────────────┘           └────────────────────┘
         │                                 │                                 │
    ┌────┴────┐                      ┌─────┴─────┐                     ┌─────┴─────┐
    │KNOWLEDGE│                      │ MATERIALS │                     │MEASUREMENT│
    └────┬────┘                      └─────┬─────┘                     └─────┬─────┘
         │                                 │                                 │
    ┌────┴──────────────┐            ┌─────┴──────────────┐           ┌─────┴──────────────┐
    │ Skill definitions │            │ Templates exist    │           │ No metric tracking │
    │ exist but not     │            │ but not referenced │           │ skill compliance   │
    │ enforced          │            │ during execution   │           │ rate               │
    └───────────────────┘            └────────────────────┘           └────────────────────┘
         │                                 │                                 │
    ┌────┴──────────────┐            ┌─────┴──────────────┐           ┌─────┴──────────────┐
    │ ORCHESTRATION     │            │ critique.md and    │           │ No pre-creation    │
    │ skill doesn't     │            │ qa-report.md       │           │ validation hook    │
    │ mandate path      │            │ templates not      │           │ for artifact       │
    │ verification      │            │ enforced           │           │ placement          │
    └───────────────────┘            └────────────────────┘           └────────────────────┘
```

### Root Cause Categories

#### 1. PEOPLE (Agent Behavior)
- **RC-P-001:** Claude did not re-read skill definitions before creating quality artifacts
- **RC-P-002:** Context rot degraded Claude's awareness of skill-specific output patterns
- **RC-P-003:** User assumed Claude would autonomously follow loaded SOP

#### 2. PROCESS (Workflow Design)
- **RC-PR-001:** No explicit validation checkpoint before file creation
- **RC-PR-002:** ORCHESTRATION.yaml not maintained as SSOT during execution
- **RC-PR-003:** No "verify skill conventions" step in quality review workflow

#### 3. TECHNOLOGY (System Constraints)
- **RC-T-001:** Context window limitations cause context rot over long sessions
- **RC-T-002:** Skills loaded as text but not enforced as constraints
- **RC-T-003:** No automated path validation in Write tool invocation

#### 4. KNOWLEDGE (Documentation)
- **RC-K-001:** Skill definitions exist but are advisory, not mandatory
- **RC-K-002:** ORCHESTRATION skill doesn't mandate path verification
- **RC-K-003:** No cross-reference between orchestration and quality agent skills

#### 5. MATERIALS (Artifacts)
- **RC-M-001:** Templates (critique.md, qa-report.md) exist but weren't referenced
- **RC-M-002:** No example artifacts in skill folders to demonstrate correct paths

#### 6. MEASUREMENT (Monitoring)
- **RC-ME-001:** No metric tracking skill compliance rate
- **RC-ME-002:** No pre-creation validation hook for artifact placement
- **RC-ME-003:** GATE preparation doesn't include artifact path audit

---

## FMEA (Failure Mode and Effects Analysis)

### Failure Mode Table

| ID | Failure Mode | Effect | Severity (S) | Occurrence (O) | Detection (D) | RPN | Priority |
|----|--------------|--------|--------------|----------------|---------------|-----|----------|
| FM-001 | Agent creates files with wrong naming convention | Automation fails; inconsistent project structure | 8 | 7 | 4 | 224 | **CRITICAL** |
| FM-002 | Agent creates files in wrong directory | Tooling cannot find artifacts; broken references | 9 | 7 | 4 | 252 | **CRITICAL** |
| FM-003 | ORCHESTRATION.yaml not updated | State drift; cannot resume workflow | 7 | 6 | 5 | 210 | **HIGH** |
| FM-004 | Skill instructions loaded but not applied | SOP violations; rework required | 8 | 8 | 3 | 192 | **HIGH** |
| FM-005 | Context rot degrades procedural memory | Agent "forgets" loaded instructions | 7 | 9 | 2 | 126 | **MEDIUM** |
| FM-006 | No validation checkpoint before GATE | Errors discovered late in workflow | 6 | 5 | 6 | 180 | **HIGH** |

**RPN Scale:**
- Severity (S): 1-10 (10 = catastrophic)
- Occurrence (O): 1-10 (10 = certain)
- Detection (D): 1-10 (10 = undetectable before failure)
- RPN = S × O × D (Risk Priority Number)

### Critical Failure Modes (RPN > 200)

#### FM-001: Wrong Naming Convention (RPN: 224)

| Aspect | Detail |
|--------|--------|
| **Failure Mode** | Agent creates files with wrong naming convention |
| **Potential Effects** | Automation fails; grep/glob patterns don't match; inconsistent project |
| **Potential Causes** | Context rot; skill not re-read; ad-hoc convention invented |
| **Current Controls** | None - user visual inspection only |
| **Recommended Actions** | Pre-creation validation; naming pattern enforcement |

#### FM-002: Wrong Directory (RPN: 252)

| Aspect | Detail |
|--------|--------|
| **Failure Mode** | Agent creates files in wrong directory |
| **Potential Effects** | Broken links; automation cannot locate artifacts; manual remediation |
| **Potential Causes** | Skill output paths not referenced; no directory structure enforcement |
| **Current Controls** | None - user visual inspection only |
| **Recommended Actions** | Mandatory skill path lookup before Write tool; directory validation |

### Severity Assessment

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FMEA SEVERITY MATRIX                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  SEVERITY  │ FM-002 ●                                              │
│      9     │ (Wrong directory)                                     │
│            │                                                       │
│      8     │ FM-001 ●──────● FM-004                               │
│            │ (Wrong naming)  (Skill not applied)                   │
│            │                                                       │
│      7     │ FM-003 ●──────● FM-005                               │
│            │ (ORCH not updated) (Context rot)                      │
│            │                                                       │
│      6     │                 FM-006 ●                              │
│            │                 (No validation)                       │
│            │                                                       │
│      5     │                                                       │
│            ├─────────────────────────────────────────────────────  │
│            │    5     6     7     8     9    10                    │
│            │              OCCURRENCE                                │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 8D Problem Solving

### D1: Establish the Team

| Role | Responsibility |
|------|---------------|
| **Problem Owner** | User (process oversight) |
| **Investigator** | Claude (root cause analysis) |
| **Implementer** | Claude (corrective actions) |
| **Validator** | User (verification of fix) |

### D2: Describe the Problem

**Problem Statement (5W2H Summary):**

During FEAT-002 EN-008 GATE-5 quality review execution on 2026-01-28, Claude created quality review artifacts (ps-critic critique, nse-qa report) with incorrect file names and in incorrect directories. Files were placed in the enabler root folder with enabler-prefixed names instead of in `critiques/` and `qa/` subdirectories with skill-defined naming patterns.

**Is/Is-Not Analysis:**

| Dimension | IS | IS NOT |
|-----------|-----|--------|
| **What** | Wrong naming & placement of quality artifacts | Wrong content in artifacts |
| **Where** | EN-007 and EN-008 enabler folders | Other project folders |
| **When** | Quality review phase of GATE-5 preparation | Implementation phase |
| **Extent** | 4 files (2 per enabler) | Widespread across project |

### D3: Develop Interim Containment Action (ICA)

**ICA-001: Manual File Remediation** ✅ IMPLEMENTED

| Action | Status | Evidence |
|--------|--------|----------|
| Create `critiques/` subdirectory in EN-008 | ✅ Complete | Directory exists |
| Create `qa/` subdirectory in EN-008 | ✅ Complete | Directory exists |
| Move and rename ps-critic file | ✅ Complete | `critiques/en008-gate5-iter1-critique.md` |
| Move and rename nse-qa file | ✅ Complete | `qa/proj008-en008-implementation-qa.md` |
| Update references in EN-008-entity-extraction.md | ✅ Complete | Lines 158-159 updated |
| Apply same remediation to EN-007 | ✅ Complete | Files in correct locations |

### D4: Determine Root Cause(s)

**Primary Root Cause:**
> **RC-PRIMARY:** Claude did not reference skill output specifications before creating files, relying instead on ad-hoc convention invention.

**Contributing Root Causes:**

| ID | Root Cause | Category | Contribution |
|----|------------|----------|--------------|
| RC-P-001 | Skill definitions not re-read before file creation | People | 35% |
| RC-T-001 | Context rot degraded memory of skill details | Technology | 25% |
| RC-PR-001 | No validation checkpoint in workflow | Process | 20% |
| RC-PR-002 | ORCHESTRATION.yaml not maintained as SSOT | Process | 15% |
| RC-K-001 | Skill conventions advisory, not enforced | Knowledge | 5% |

**5-Why Analysis:**

```
WHY 1: Why were files created with wrong names/locations?
  → Claude invented ad-hoc naming instead of following skill conventions

WHY 2: Why did Claude invent ad-hoc naming?
  → Claude did not reference skill output specifications before creating files

WHY 3: Why didn't Claude reference skill specifications?
  → Context rot degraded Claude's awareness that skills define output patterns

WHY 4: Why did context rot cause this specific failure?
  → Skills are loaded as informational text, not as enforced constraints

WHY 5: Why aren't skill patterns enforced?
  → No validation mechanism exists to verify paths against skill definitions before Write
```

**Root Cause Statement:**
The fundamental root cause is that skill conventions are loaded as advisory information but not enforced as mandatory constraints. When context rot degrades the agent's procedural memory, there is no failsafe to prevent convention violations.

### D5: Choose Permanent Corrective Actions (PCA)

| PCA ID | Action | Target Root Cause | Owner | Priority |
|--------|--------|-------------------|-------|----------|
| PCA-001 | Before creating quality artifacts, Claude MUST re-read skill agent definition to verify output path | RC-P-001 | Claude | CRITICAL |
| PCA-002 | Add "Verify Artifact Paths" step to GATE preparation workflow in ORCHESTRATION skill | RC-PR-001 | Claude | HIGH |
| PCA-003 | Update ORCHESTRATION.yaml after each file creation with artifact path | RC-PR-002 | Claude | HIGH |
| PCA-004 | Document skill output locations in orchestration PLAYBOOK.md | RC-K-001 | Claude | MEDIUM |
| PCA-005 | Add artifact path audit to GATE checklist | RC-PR-001 | Claude | MEDIUM |

### D6: Implement and Validate PCAs

| PCA ID | Implementation Status | Validation Evidence |
|--------|----------------------|---------------------|
| PCA-001 | ✅ Documented in this DISC-003 | This discovery serves as procedural reminder |
| PCA-002 | 🔄 Pending | Requires ORCHESTRATION skill update |
| PCA-003 | ✅ Implemented | ORCHESTRATION.yaml updated with quality_reviews paths |
| PCA-004 | 🔄 Pending | Requires PLAYBOOK.md update |
| PCA-005 | 🔄 Pending | Requires GATE checklist update |

### D7: Prevent Recurrence

**Systemic Improvements:**

1. **Skill Enforcement Protocol**
   - Before invoking any quality agent, Claude MUST read the agent definition
   - Output location from skill definition MUST be used exactly
   - ORCHESTRATION.yaml MUST track all artifact paths

2. **Pre-Creation Checklist**
   ```
   Before Write tool for quality artifacts:
   [ ] Read skill agent definition for output path
   [ ] Verify directory structure exists (create if needed)
   [ ] Verify filename matches skill pattern
   [ ] Update ORCHESTRATION.yaml with planned path
   ```

3. **GATE Audit Protocol**
   ```
   Before presenting GATE for approval:
   [ ] Verify all quality artifacts in correct directories
   [ ] Verify all filenames match skill conventions
   [ ] Verify ORCHESTRATION.yaml paths match actual files
   ```

**Knowledge Capture:**
- This DISC-003 serves as permanent record
- Pattern documented for all future FEAT-002 enablers
- Extends to all future projects using orchestration + quality skills

### D8: Recognize the Team

**Lessons Learned:**

| Lesson | Impact |
|--------|--------|
| Skills load as information but require active application | HIGH - Fundamental understanding of agent behavior |
| Context rot is real and affects procedural memory | HIGH - Must design for memory degradation |
| ORCHESTRATION.yaml is critical for state management | HIGH - Neglecting SSOT causes drift |
| User oversight caught failure early | MEDIUM - Late detection would have propagated error |

**Process Improvements Validated:**
- Manual remediation successfully corrected EN-007 and EN-008 artifacts
- DISC-003 establishes precedence for future quality reviews
- ORCHESTRATION.yaml now tracks quality review artifact paths

---

## Finding

### Established Folder Structure

Within an enabler folder during orchestrated workflows, quality artifacts MUST be organized:

```
{EnablerID}-{slug}/
├── critiques/                           # ps-critic outputs
│   └── {id}-{gate/entry}-iter{N}-critique.md
└── qa/                                  # nse-qa outputs
    └── {proj}-{entry}-{type}-qa.md
```

### Naming Conventions

**ps-critic (from `skills/problem-solving/agents/ps-critic.md` line 59):**
```
Pattern: {ps-id}-{entry-id}-{iteration}-critique.md
Example: en008-gate5-iter1-critique.md
```

**nse-qa (from `skills/nasa-se/agents/nse-qa.md` line 85):**
```
Pattern: {proj-id}-{entry-id}-{artifact-type}-qa.md
Example: proj008-en008-implementation-qa.md
```

### Why This Matters

1. **Traceability:** Subdirectories clearly separate quality review artifacts from implementation artifacts
2. **Consistency:** Following skill-defined patterns ensures automation compatibility
3. **Scalability:** Multiple review iterations can be organized without cluttering enabler root
4. **Auditability:** Standardized paths enable grep/glob automation for compliance checking

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Skill Definition | ps-critic output location | `skills/problem-solving/agents/ps-critic.md:59` | 2026-01-28 |
| E-002 | Skill Definition | nse-qa output location | `skills/nasa-se/agents/nse-qa.md:85` | 2026-01-28 |
| E-003 | Template | Critique template ID format | `skills/problem-solving/templates/critique.md:3` | 2026-01-28 |
| E-004 | Template | QA report ID format | `skills/nasa-se/templates/qa-report.md:3` | 2026-01-28 |
| E-005 | User Feedback | SOP breach identification | Conversation with user | 2026-01-28 |
| E-006 | Industry Research | Context rot phenomenon | Chroma Research | 2025 |
| E-007 | ORCHESTRATION.yaml | State drift evidence | FEAT-002 execution | 2026-01-28 |

### Corrective Action Taken

Files remediated for EN-007 and EN-008 quality reviews:

| Enabler | Original | Corrected |
|---------|----------|-----------|
| EN-007 | `EN-007-ps-critic-report.md` | `critiques/en007-gate5-iter1-critique.md` |
| EN-007 | `EN-007-nse-qa-report.md` | `qa/proj008-en007-implementation-qa.md` |
| EN-008 | `EN-008-ps-critic-report.md` | `critiques/en008-gate5-iter1-critique.md` |
| EN-008 | `EN-008-nse-qa-report.md` | `qa/proj008-en008-implementation-qa.md` |

---

## Implications

### Impact on Project

This discovery has CRITICAL impact:

1. **Immediate:** All future GATE reviews in FEAT-002 MUST follow established structure
2. **Systemic:** Validates that context rot is a real operational concern
3. **Process:** Establishes mandatory pre-creation validation checkpoint
4. **Knowledge:** Documents root cause analysis methodology for future failures

### Design Decisions Affected

- **Decision:** Quality artifact placement
  - **Impact:** Enabler folders remain clean with clear artifact categorization
  - **Rationale:** Skill definitions are authoritative; orchestration MUST NOT deviate

- **Decision:** ORCHESTRATION.yaml as SSOT
  - **Impact:** State MUST be updated after every artifact creation
  - **Rationale:** State drift causes workflow failures and audit gaps

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Context rot causes future SOP violations | HIGH | Pre-creation checklist; periodic skill re-read |
| ORCHESTRATION.yaml becomes stale | MEDIUM | Update after each file operation |
| Pattern not applied to other enablers | MEDIUM | This DISC-003 establishes precedence |

### Opportunities Created

- **OPP-001:** Develop automated artifact path validation
- **OPP-002:** Add skill compliance tracking to ORCHESTRATION metrics
- **OPP-003:** Create "context refresh" protocol for long sessions

---

## Relationships

### Creates

- No new work items (corrective action completed inline)

### Informs

- All future GATE reviews (GATE-5, GATE-6)
- Future enablers: EN-009, EN-013, EN-014, EN-015, EN-016
- ORCHESTRATION skill enhancement backlog

### Related Discoveries

- [DISC-001](./FEAT-002--DISC-001-enabler-alignment-analysis.md) - Enabler alignment analysis
- [DISC-002](./FEAT-002--DISC-002-future-scope-analysis.md) - Future scope analysis

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-002-implementation.md](./FEAT-002-implementation.md) | Parent feature |
| Skill | [skills/problem-solving/agents/ps-critic.md](../../../../../skills/problem-solving/agents/ps-critic.md) | ps-critic definition |
| Skill | [skills/nasa-se/agents/nse-qa.md](../../../../../skills/nasa-se/agents/nse-qa.md) | nse-qa definition |
| SSOT | [ORCHESTRATION.yaml](./ORCHESTRATION.yaml) | Workflow state |

---

## Recommendations

### Immediate Actions

1. ✅ **COMPLETE:** Update ORCHESTRATION.yaml to track correct artifact paths
2. ✅ **COMPLETE:** Apply pattern to EN-007 quality review artifacts
3. ✅ **COMPLETE:** Document root cause analysis in DISC-003

### Long-term Considerations

- Consider adding artifact path validation to orchestration skill
- Document skill output location patterns in PLAYBOOK.md
- Develop automated compliance checking for artifact paths
- Add "context refresh" step to long orchestration sessions

### Process Improvements

1. **Before quality agent invocation:**
   - Read agent skill definition
   - Extract output path pattern
   - Create directory structure if needed

2. **After artifact creation:**
   - Update ORCHESTRATION.yaml with artifact path
   - Verify file exists at expected location
   - Update parent enabler document references

3. **Before GATE presentation:**
   - Audit all artifact paths against skill patterns
   - Verify ORCHESTRATION.yaml matches filesystem
   - Confirm all references resolve correctly

---

## Open Questions

### Questions for Follow-up

1. **Q:** Should the orchestration skill enforce artifact path validation automatically?
   - **Investigation Method:** Design review with ps-architect
   - **Priority:** MEDIUM

2. **Q:** How can context rot be detected and mitigated during long sessions?
   - **Investigation Method:** Research on context window management
   - **Priority:** HIGH

3. **Q:** Should skills declare output patterns in a machine-readable format for validation?
   - **Investigation Method:** Skill schema design review
   - **Priority:** LOW

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28T14:00:00Z | Claude | Complete rewrite with 5W2H, Ishikawa, FMEA, 8D analysis |
| 2026-01-28T12:30:00Z | Claude | Created discovery documenting folder structure precedence |

---

## Metadata

```yaml
id: "FEAT-002:DISC-003"
parent_id: "FEAT-002"
work_type: DISCOVERY
title: "Quality Artifact Folder Structure Precedence"
status: VALIDATED
priority: CRITICAL
impact: CRITICAL
created_by: "Claude"
created_at: "2026-01-28T12:00:00Z"
updated_at: "2026-01-28T14:00:00Z"
completed_at: "2026-01-28T14:00:00Z"
tags: ["process", "quality", "folder-structure", "precedence", "context-rot", "skill-compliance", "root-cause-analysis", "5W2H", "Ishikawa", "FMEA", "8D"]
source: "EN-008 GATE-5 Quality Review"
finding_type: GAP
confidence_level: HIGH
validated: true
analysis_frameworks: ["5W2H", "Ishikawa", "FMEA", "8D"]
root_cause_count: 5
failure_modes_identified: 6
corrective_actions: 5
corrective_actions_complete: 2
```
