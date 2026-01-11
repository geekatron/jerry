# DOC-001: WORKTRACKER Decomposition Synthesis

> **Document ID**: DOC-001-synthesis
> **Date**: 2026-01-11
> **Agent**: ps-synthesizer
> **Inputs**: DOC-001-R1 (Git History), DOC-001-R2 (Session Analysis), DOC-001-R3 (File Analysis)

---

## 1. Executive Summary

The WORKTRACKER decomposition represents a deliberate response to **Context Rot** - the phenomenon where LLM performance degrades as context windows fill, even when within technical limits. What began as a single monolithic 821-line file tracking project PROJ-001-plugin-cleanup was transformed into a **Hub and Spoke architecture**: a 109-line navigation index plus 9 specialized phase files totaling over 4,100 lines of structured work tracking.

The decomposition was not a one-time event but an **iterative evolution**. Early attempts to expand the WORKTRACKER with full task details caused the file to become "massive" and unwieldy, prompting a revert and rethink. The final solution, implemented in commit `4882948` on January 9, 2026, restructured the tracking system for three key capabilities: **multi-session continuity** (survive context compaction), **parallel execution** (multiple agents working simultaneously), and **progressive detail** (active work gets maximum detail while completed work stays minimal).

The resulting pattern is generalizable: any large work-tracking document can be decomposed using these principles. The methodology prioritizes **filesystem as infinite memory** - offloading state to files rather than holding everything in context. This synthesis extracts the reproducible methodology, identifies patterns for future use, and provides inputs for the planned deliverables (RUNBOOK-002, PURPOSE-CATALOG.md, and the worktracker-decomposition skill).

---

## 2. The Problem: Why Decomposition Was Needed

### 2.1 Context Rot Manifested

The WORKTRACKER grew organically as PROJ-001 progressed through seven implementation phases. Each phase added tasks, subtasks, acceptance criteria, evidence records, and session context. By January 9, 2026, the file had reached **821 lines** - a size that created several problems:

| Problem | Symptom | Impact |
|---------|---------|--------|
| **Context Window Consumption** | Loading the full file consumed significant context | Less room for actual work, code, and reasoning |
| **Navigation Difficulty** | Finding the active task required scrolling through completed phases | Time wasted, easy to lose place |
| **Compaction Vulnerability** | When context was compacted, key state was lost | Session continuity broken |
| **Update Overhead** | Every small change required parsing the entire file | Increased error rate, slower updates |
| **Parallel Work Blocked** | Single file meant only one writer at a time | Sequential bottleneck |

### 2.2 The Failed Expansion Attempt

The git history (R1) reveals that before the successful decomposition, there was a failed attempt:

```
05874e5 - Expand Phases 2-4 with full TASK/Sub-task details (file became massive)
ea4c5f3 - Revert "Expand Phases 2-4 with full TASK/Sub-task details"
24cbc7e - Restore WORKTRACKER_PROPOSAL.md to commit 78000bb
```

This pattern shows that simply adding more detail to a monolithic file is **not sustainable**. The file became too large, and the only option was to revert. This failure directly motivated the decomposition approach.

### 2.3 User Recognition of the Problem

The session analysis (R2) captures the user's retrospective recognition:

> "I would like to know if it would be possible for you to tell me the process by which we got to the beautiful `work/` folder and decomposed worktracker? I would like to be able to reproduce this process going forward."

This request explicitly frames the decomposition as a **reproducible process** worth documenting - validating that the pattern has value beyond this single project.

---

## 3. The Solution: What Was Created

### 3.1 Structural Transformation

The decomposition transformed a monolithic file into a **multi-file graph structure**:

**Before (Monolithic)**:
```
WORKTRACKER.md (821 lines)
├── Quick Status
├── Phase 1: Infrastructure Setup (COMPLETED) - ~100 lines
├── Phase 2: Core File Updates (COMPLETED) - ~100 lines
├── Phase 3: Agent Updates (COMPLETED) - ~100 lines
├── Phase 4: Governance (COMPLETED) - ~100 lines
├── Phase 5: Validation (COMPLETED) - ~100 lines
├── Phase 6: Enforcement (IN PROGRESS) - ~200 lines
├── Phase 7: Design Synthesis (COMPLETED) - ~100 lines
└── Bug Tracking, Tech Debt - ~100 lines
```

**After (Hub and Spoke)**:
```
WORKTRACKER.md (109 lines) - Navigation Hub
├── Navigation Graph (ASCII diagram)
├── Quick Status Dashboard (links to all phases)
├── Session Resume Protocol
└── Principles (non-negotiable rules)

work/
├── PHASE-01-INFRASTRUCTURE.md (222 lines)
├── PHASE-02-CORE-UPDATES.md (188 lines)
├── PHASE-03-AGENT-UPDATES.md (198 lines)
├── PHASE-04-GOVERNANCE.md (163 lines)
├── PHASE-05-VALIDATION.md (202 lines)
├── PHASE-06-ENFORCEMENT.md (960 lines) <-- Active phase, maximum detail
├── PHASE-07-DESIGN-SYNTHESIS.md (509 lines)
├── PHASE-BUGS.md (143 lines)
├── PHASE-DISCOVERY.md (99 lines)
├── PHASE-TECHDEBT.md (341 lines)
├── PHASE-IMPL-DOMAIN.md (633 lines)
└── INITIATIVE-DEV-SKILL.md (488 lines)
```

**Key Metrics**:
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Main file size | 821 lines | 109 lines | -87% |
| Total tracking content | 821 lines | 4,146+ lines | +405% |
| Files | 1 | 13 | +12 |
| Max context needed for navigation | 821 lines | 109 lines | -87% |
| Max context for active work | 821 lines | 960 lines | Isolated |

### 3.2 File Type Taxonomy

The file analysis (R3) identified **four distinct file types** in the decomposed structure:

| Type | Pattern | Purpose | Example |
|------|---------|---------|---------|
| **Sequential Phase** | `PHASE-{NN}-{NAME}.md` | Track work for numbered phases | `PHASE-06-ENFORCEMENT.md` |
| **Cross-Cutting Category** | `PHASE-{CATEGORY}.md` | Track items spanning phases | `PHASE-BUGS.md`, `PHASE-TECHDEBT.md` |
| **Initiative** | `INITIATIVE-{NAME}.md` | Complex multi-phase orchestration | `INITIATIVE-DEV-SKILL.md` |
| **Implementation Domain** | `PHASE-IMPL-{DOMAIN}.md` | Detailed implementation tasks | `PHASE-IMPL-DOMAIN.md` |

### 3.3 Navigation Architecture

Each phase file includes a **navigation section** enabling traversal:

```markdown
## Navigation

| Link | Description |
|------|-------------|
| [<- WORKTRACKER](../WORKTRACKER.md) | Back to index |
| [<- Phase 5](PHASE-05-VALIDATION.md) | Previous phase |
| [Phase 7 ->](PHASE-07-DESIGN-SYNTHESIS.md) | Next phase |
```

The main WORKTRACKER.md includes a **visual navigation graph**:

```
              +-------------------------------------+
              |           WORKTRACKER.md            |
              |              (INDEX)                |
              +-----------------+-------------------+
                                |
      +-----------------+-------+-------+
      |                 |               |
      v                 v               v
COMPLETED         IN PROGRESS      SUPPORT
Phases 1-5,7      Phase 6         BUGS, TECHDEBT
```

### 3.4 Progressive Detail Principle

A key observation: **active work gets maximum detail, completed work stays minimal**.

| Phase Status | Line Count Range | Detail Level |
|--------------|------------------|--------------|
| COMPLETED | 163-222 lines | Task summaries, outputs, dates |
| IN PROGRESS | 633-960 lines | Full subtask trees, BDD tests, acceptance criteria |
| SUPPORT | 99-341 lines | As needed for tracking |

This ensures context is not wasted on completed work while providing maximum support for active work.

---

## 4. The Methodology: Step-by-Step Reproducible Process

### 4.1 Pre-Conditions

Before decomposing a WORKTRACKER, verify:

1. **Size Threshold Exceeded**: File is >500 lines (soft) or >800 lines (hard trigger)
2. **Multiple Phases Exist**: At least 3 distinct phases or categories
3. **Some Phases Complete**: Completed work can be archived minimally
4. **Active Work Identified**: Clear understanding of what is "in progress"

### 4.2 Decomposition Steps

**Step 1: Analyze the Existing Structure**

```
INPUT: Monolithic WORKTRACKER.md
OUTPUT: List of phases, categories, and their boundaries
```

- Identify all phases (numbered sequences)
- Identify cross-cutting categories (bugs, tech debt, discoveries)
- Identify complex initiatives that span phases
- Note line counts and completion status for each section

**Step 2: Create the work/ Directory Structure**

```
mkdir -p {project_path}/work/
```

**Step 3: Create Phase Files (Sequential)**

For each numbered phase:

```markdown
# Phase N: {Title}

> **Status**: [STATUS_EMOJI] {STATUS} ({PERCENT}%)
> **Goal**: {One-line goal description}

---

## Navigation

| Link | Description |
|------|-------------|
| [<- WORKTRACKER](../WORKTRACKER.md) | Back to index |
| [<- Phase N-1](PHASE-{N-1}-*.md) | Previous phase |
| [Phase N+1 ->](PHASE-{N+1}-*.md) | Next phase |

---

## Task Summary

| Task ID | Title | Status | Subtasks | Output |
|---------|-------|--------|----------|--------|
{migrated task rows}

---

## {TASK-ID}: {Task Title} {STATUS_EMOJI}

{Full task details from monolithic file}

---

## Session Context

### For Resuming Work
{Instructions specific to this phase}

### Key Files to Know
| File | Purpose |
|------|---------|
{relevant files for this phase}

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| {today} | {agent} | Initial decomposition from WORKTRACKER.md |
```

**Step 4: Create Category Files (Cross-Cutting)**

For bugs, tech debt, and discoveries:

```markdown
# Phase {CATEGORY}: {Title}

> **Status**: {STATUS}
> **Purpose**: Track {category} discovered during project development

---

## {Category} Summary

| ID | Title | Severity/Priority | Status | Phase Found |
|----|-------|-------------------|--------|-------------|
{migrated items}

---

## Template

{Template for new items of this type}
```

**Step 5: Transform WORKTRACKER.md into Navigation Hub**

Replace detailed content with:

1. **Navigation Graph** (ASCII art showing structure)
2. **Quick Status Dashboard** (links to all phase files with status)
3. **Session Resume Protocol** (how to continue after compaction)
4. **Principles** (non-negotiable rules that apply everywhere)
5. **Document History** (preserves changelog)

Target: **<150 lines**

**Step 6: Update Cross-References**

- Ensure all links work bidirectionally
- Update any external references to point to new locations
- Add "Session Context" sections to active phase files

**Step 7: Commit Atomically**

Single commit with clear message:

```
docs({project}): restructure WORKTRACKER to multi-file graph format

Restructured work tracking for multi-session and parallel work:

- WORKTRACKER.md is now an index with navigation graph
- Created work/ directory with per-phase files
- {Active phase} has detailed breakdown for active tasks
- Added subtask IDs with dependencies
- Added file-level mappings and acceptance criteria
- Added session context for compaction survival

Structure:
  work/PHASE-01-{NAME}.md ({status})
  work/PHASE-02-{NAME}.md ({status})
  ...
  work/PHASE-{CAT}.md ({status})
```

### 4.3 Post-Decomposition Maintenance

**When to Update Phase Files**:
- Add new tasks to the relevant phase file
- Update task status in both phase file AND WORKTRACKER.md dashboard
- Expand active work with subtasks, tests, acceptance criteria

**When to Archive**:
- When a phase completes, reduce detail to summaries
- Move detailed implementation notes to `/reports/` or `/synthesis/`
- Keep enough context for future reference

**When to Re-Decompose**:
- If a phase file exceeds 1,000 lines
- If a new cross-cutting category emerges
- If parallel work creates merge conflicts

---

## 5. Patterns Identified: Generalizable Principles

### 5.1 Hub and Spoke Pattern

**Description**: Central index file with minimal content that links to detailed spoke files.

**When to Use**: Any time a single document exceeds context-friendly size (~500 lines) and contains distinct sections.

**Structure**:
```
{Document}.md (Hub)
├── Navigation Graph
├── Status Dashboard
├── Resume Protocol
└── Principles

{document_type}/
├── {Section-01}.md (Spoke)
├── {Section-02}.md (Spoke)
└── {Category}.md (Spoke)
```

**Benefits**:
- Load only what's needed
- Navigate to any section in O(1)
- Parallel updates without conflicts

### 5.2 Progressive Detail Pattern

**Description**: Allocate detail inversely to completion status.

**When to Use**: Any work tracking where completed items should not compete for context with active items.

**Implementation**:
| Status | Detail Level | Line Target |
|--------|--------------|-------------|
| Completed | Summary + output links | <50 lines per task |
| In Progress | Full breakdown | Unlimited |
| Pending | Basic description | <20 lines per task |

**Benefits**:
- Context spent where it matters
- History preserved but not intrusive
- Active work gets maximum support

### 5.3 Session Resume Protocol Pattern

**Description**: Every file includes explicit instructions for resuming work after context compaction.

**When to Use**: Any document that might be loaded into a fresh context.

**Template**:
```markdown
## Session Context

### For Resuming Work
1. Check Current Focus (above) for active task
2. Navigate to [specific section] for detailed breakdown
3. Read [specific context] before starting work
4. Check Dependencies before proceeding
5. Update timestamp after each work session

### Key Files to Know
| File | Purpose |
|------|---------|
| {path} | {why it matters} |
```

**Benefits**:
- Self-documenting recovery path
- No external dependency for context
- Enables multi-session continuity

### 5.4 Explicit Dependency Graph Pattern

**Description**: Tasks declare predecessors and successors explicitly.

**When to Use**: Any work with dependencies between items.

**Implementation**:
```
008d.0 (Research)
    |
    v
008d.1 (Value Objects)
    |
    +---> 008d.1.1 (Refactor ProjectId)
    +---> 008d.1.2 (Extract slug property)
    |
    v
008d.2 (Entities) <--- CAN PARALLEL ---> 008d.3 (New Objects)
```

**Benefits**:
- Parallel work opportunities visible
- Critical path analysis possible
- Prevents starting blocked work

### 5.5 Cross-Cutting Category Pattern

**Description**: Items that span phases get their own dedicated files.

**When to Use**: When bugs, tech debt, discoveries, or other cross-cutting concerns appear.

**Implementation**:
- Create `PHASE-{CATEGORY}.md` with standardized template
- Include "Phase Found" or "Source" field for traceability
- Support items being added from any phase

**Benefits**:
- No context pollution in phase files
- Dedicated triage and prioritization
- Clear ownership and lifecycle

---

## 6. Inputs for Deliverables

### 6.1 For RUNBOOK-002: WORKTRACKER Decomposition Runbook

**Key Sections to Include**:

1. **Trigger Criteria**
   - File size thresholds (>500 soft, >800 hard)
   - Session pain indicators (difficulty finding active work)
   - Compaction recovery failures

2. **Pre-Flight Checklist**
   - [ ] Backup current WORKTRACKER.md (git commit)
   - [ ] Identify phase boundaries
   - [ ] Identify cross-cutting categories
   - [ ] Confirm active work phase(s)

3. **Execution Steps** (from Section 4.2 above)

4. **Validation Criteria**
   - [ ] WORKTRACKER.md < 150 lines
   - [ ] All navigation links work
   - [ ] Session context sections present in active files
   - [ ] Quick status dashboard complete
   - [ ] Git commit with proper message format

5. **Rollback Procedure**
   - `git revert {commit}` to restore monolithic version
   - Decision criteria for rollback

### 6.2 For PURPOSE-CATALOG.md

**File Type Entries**:

| File Pattern | Purpose | When Created | Owner |
|--------------|---------|--------------|-------|
| `WORKTRACKER.md` | Navigation hub and session resume point | Project start | Project Lead |
| `work/PHASE-{NN}-*.md` | Sequential phase work tracking | Decomposition | Phase Owner |
| `work/PHASE-{CATEGORY}.md` | Cross-cutting issue tracking | As needed | All Agents |
| `work/INITIATIVE-*.md` | Complex multi-phase orchestration | For large initiatives | Initiative Lead |
| `work/PHASE-IMPL-*.md` | Detailed implementation tasks | Implementation phases | Implementor |

**Naming Convention Entries**:

| ID Pattern | Example | Usage |
|------------|---------|-------|
| `{PREFIX}-{NNN}` | `SETUP-001` | Phase-level tasks |
| `{PREFIX}-{NNN}.{N}` | `008d.1` | Subtasks |
| `{PREFIX}-{NNN}.{N}.{N}` | `008d.1.1` | Sub-subtasks |
| `R-{ID}` | `R-008d.0` | Research phase |
| `I-{ID}` | `I-008d.1` | Implementation phase |
| `T-{ID}` | `T-008d.1.3` | Test phase |
| `E-{ID}` | `E-008d` | Evidence phase |

### 6.3 For worktracker-decomposition Skill

**Skill Capabilities**:

1. **Analysis Mode**
   - Input: Path to WORKTRACKER.md
   - Output: Report with size, phases, categories, recommendation

2. **Decomposition Mode**
   - Input: Path to WORKTRACKER.md, confirmed=true
   - Output: Created work/ folder with all files

3. **Validation Mode**
   - Input: Path to decomposed structure
   - Output: Validation report (links, sizes, missing sections)

4. **Maintenance Mode**
   - Input: Path to WORKTRACKER.md, new_phase or new_category
   - Output: Created file with template, updated navigation

**Skill Invocation Examples**:

```
/worktracker-decompose analyze projects/PROJ-002/WORKTRACKER.md
/worktracker-decompose execute projects/PROJ-002/WORKTRACKER.md
/worktracker-decompose validate projects/PROJ-002/
/worktracker-decompose add-phase projects/PROJ-002/ --name "Phase 8: Deployment"
```

**Key Implementation Constraints**:

- Must preserve all task IDs during decomposition
- Must update all cross-references bidirectionally
- Must include session context in all created files
- Must commit atomically with proper message format
- Must support dry-run mode for preview

---

## 7. Cross-Reference Matrix

This synthesis draws from and supports the following artifacts:

### Input Artifacts

| ID | Artifact | Key Contribution |
|----|----------|------------------|
| DOC-001-R1 | Git History Analysis | Commit `4882948` details, before/after states, timeline |
| DOC-001-R2 | Session Analysis | User intent, iterative evolution, failure/recovery pattern |
| DOC-001-R3 | File Analysis | File type taxonomy, schemas, parallelization patterns |

### Output Artifacts (To Be Created)

| ID | Artifact | Dependencies |
|----|----------|--------------|
| RUNBOOK-002 | Decomposition Runbook | Sections 4, 5, 6.1 of this synthesis |
| PURPOSE-CATALOG.md | File Purpose Registry | Section 6.2 of this synthesis |
| worktracker-decomposition SKILL | Automation Skill | Section 6.3 of this synthesis |

### Related Artifacts

| Artifact | Relationship |
|----------|--------------|
| `WORKTRACKER.md` | Subject of decomposition |
| `work/*.md` | Products of decomposition |
| `CLAUDE.md` | References this pattern |
| Jerry Constitution | Principles applied (P-002: File Persistence) |

---

## 8. Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-11 | ps-synthesizer (Claude Opus 4.5) | Initial synthesis created from R1, R2, R3 research |
