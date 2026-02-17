# Worktracker Behavior Rules

> Rule file for /worktracker skill
> Source: CLAUDE.md lines 218-241 (EN-201 extraction)
> Extracted: 2026-02-01
> Updated: 2026-02-17 (Added WTI-007 Content Quality, WTI-008 Collaboration Before Creation - PROJ-005)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Worktracker Integrity Rules](#worktracker-integrity-rules) | **CRITICAL** - Rules for keeping state accurate and honest (WTI-001 to WTI-006) |
| [Content Quality Rules](#content-quality-rules) | **CRITICAL** - Rules for work item content quality (WTI-007, WTI-008) |
| [Work tracker (worktracker) Behavior](#work-tracker-worktracker-behavior) | Canonical model and structure behavior |
| [Cross-References](#cross-references) | Links to other worktracker rule files |

---

## Worktracker Integrity Rules

> **Enforcement Level:** HARD
> **Source:** Process failure discovered during EN-201 execution (BUG: State drift)

These rules ensure the worktracker remains a **single source of truth** that is accurate, honest, and verifiable.

### WTI-001: Real-Time State Updates (HARD)

**Rule:** You MUST update worktracker file status **immediately** after completing work.

| When | Action Required |
|------|-----------------|
| Task started | Set status to `in_progress`, add timestamp to History |
| Task completed | Set status to `DONE`, update Progress Summary |
| Bug discovered | Create BUG file immediately |
| Decision made | Create DEC file immediately |
| Discovery found | Create DISC file immediately |

**Anti-Pattern:** Completing work in background agents without updating worktracker state.

**Why:** Stale state causes confusion, duplicate work, and loss of institutional knowledge.

### WTI-002: No Closure Without Verification (HARD)

**Rule:** You MUST NOT mark any work item as `DONE` or `completed` without:

1. **Verifying ALL Acceptance Criteria** are met
2. **Providing Evidence** of completion (file paths, test results, citations)
3. **Updating the Evidence section** with verification proof

| Closure Requirement | Evidence Type |
|---------------------|---------------|
| Code/File creation | File path that exists |
| Test passing | Test command output or CI link |
| Documentation | Document path and section reference |
| Research | Citations, sources, references |

**Anti-Pattern:** Marking tasks complete based on agent completion signals without verifying deliverables exist.

### WTI-003: Truthful and Accurate State (HARD)

**Rule:** Worktracker state MUST be truthful, accurate, and honest at all times.

| Principle | Requirement |
|-----------|-------------|
| **Truthful** | Status reflects actual state, not desired state |
| **Accurate** | Progress percentages match actual completion |
| **Honest** | Blockers and issues are documented, not hidden |
| **Verifiable** | Claims can be verified by reading referenced files |

**Anti-Pattern:** Showing 100% progress when work items are incomplete or untested.

### WTI-004: Synchronize Before Reporting (HARD)

**Rule:** Before reporting status or progress, you MUST:

1. **Read the current worktracker file** to get latest state
2. **Verify file system** matches claimed deliverables
3. **Update any drift** discovered during verification
4. **Report the verified state**, not cached/remembered state

**Why:** Context compaction and session boundaries cause state drift. Always verify before report.

### WTI-005: Atomic Task State (MEDIUM)

**Rule:** Task state changes should be atomic - update the task file AND the parent enabler/story in the same operation.

```
When TASK-001 completes:
1. Update TASK-001-*.md status → DONE
2. Update parent EN-001 task table status → DONE
3. Update parent EN-001 progress summary
4. Commit all changes together
```

**Why:** Partial updates create inconsistent state between parent and child documents.

### WTI-006: Evidence-Based Closure (HARD)

**Rule:** The Evidence section MUST be populated before closure:

```markdown
## Evidence

### Technical Verification

| Criterion | Verification Method | Evidence | Verified By | Date |
|-----------|---------------------|----------|-------------|------|
| File created | `ls -la path/to/file` | File exists, 45 lines | Claude | 2026-02-01 |
| Content correct | Manual review | Contains required sections | Claude | 2026-02-01 |
```

**Anti-Pattern:** Empty evidence tables with status marked as complete.

---

## Content Quality Rules

> **Enforcement Level:** HARD
> **Source:** PROJ-005-jerry-process-improvements (ADO skill pattern extraction + industry research)
> **Added:** 2026-02-17
> **Reference:** `worktracker-content-standards.md` for detailed examples, anti-patterns, and writing guidance

These rules ensure work item **content** is clear, concise, and actionable. They complement WTI-001 through WTI-006 (which ensure structural integrity) by enforcing what is written inside work items.

**Applicability (DEC-006):** These rules apply to **newly created** work items only. The wt-auditor flags existing violations as INFO (advisory), not blocking.

### WTI-007: Content Quality Standards (HARD)

**Rule:** All work item content (Summary, Acceptance Criteria, Description) MUST meet content quality standards defined in `worktracker-content-standards.md`.

**The #1 Rule:** "If engineers, UX designers, or QA need to ask clarifying questions, the Acceptance Criteria has failed."

| Sub-Rule | Name | Enforcement | Detail |
|----------|------|-------------|--------|
| WTI-007a | No DoD in AC | HARD | AC must not contain Definition of Done items: test coverage, code review, documentation updates, deployment verification, QA sign-off. Universal test: "If it applies to every work item equally, it is DoD, not AC." |
| WTI-007b | No Implementation Details in AC | HARD | AC must not contain file paths, class names, method names, architecture patterns, or technology-specific decisions. Implementation details belong in the Description section, Implementation Notes section, or child Task descriptions -- never in AC. |
| WTI-007c | Actor-First Format | MEDIUM | AC bullets should begin with an actor or system subject: "User can...", "System validates...", "API returns...", "Admin sees...". For Enablers, Features, and Tasks, the "actor" may be a system component, infrastructure element, or process (e.g., "Build pipeline...", "Database migration...", "Configuration file..."). |
| WTI-007d | No Hedge Words | MEDIUM | AC must not use hedge words: "should be able to", "might need to", "could potentially", "if possible", "ideally", "as needed", "when appropriate". Replace with direct, testable statements. |
| WTI-007e | AC Bullet Count Limits | HARD | Maximum AC bullets by type: Story: 5, Bug: 3, Task: 3, Enabler: 5, Feature: 5. Exceeding the limit triggers WTI-007g. |
| WTI-007f | Summary Brevity | MEDIUM | Summary must be 1-3 sentences. Describe the what and why. No implementation details. Bug summaries describe symptoms, not root causes. |
| WTI-007g | Scope Overflow Signal | HARD | If AC exceeds the bullet limit (WTI-007e), the work item scope is likely too large. Claude MUST flag this and recommend splitting using the SPIDR framework (Spike, Paths, Interfaces, Data, Rules). See `worktracker-content-standards.md` for SPIDR details. |

**Anti-Pattern:**

```markdown
# BAD AC (violates WTI-007a, WTI-007b):
- [ ] Update AssetTypeRepository.cs to add new method
- [ ] All unit tests pass with 90%+ coverage
- [ ] Code reviewed and approved
- [ ] Documentation updated

# GOOD AC (compliant):
- [ ] Admin can create a new asset type from the Asset Management page
- [ ] System validates asset type name is unique within the tenant
- [ ] API returns 409 Conflict when duplicate name is submitted
```

**Why:** Work items with vague, implementation-focused, or DoD-contaminated AC require engineers to ask clarifying questions, waste sprint planning time, and produce inconsistent implementations. Explicit content quality rules make AC clear enough to build from without questions.

### WTI-008: Collaboration Before Creation (HARD)

**Rule:** Claude MUST validate understanding with the user before creating work items that contain Acceptance Criteria.

**Applicability (DEC-007):** This rule applies to: Story (PBI), Bug, Task, Enabler, Feature. It does NOT apply to: Discovery, Decision, Impediment, Sub-Task.

| Sub-Rule | Name | Enforcement | Detail |
|----------|------|-------------|--------|
| WTI-008a | Pre-Creation Checkpoint | HARD | Before writing a work item file, present a summary of what will be created and ask for confirmation. Adapt summary fields by type: role/goal/benefit for stories; symptom/location/severity for bugs; what/why for enablers and tasks. |
| WTI-008b | AC Review Checkpoint | HARD | After drafting AC but before writing the file, present the AC to the user. Ask: (1) Can an engineer build this without asking questions? (2) Can QA write test cases from these criteria? (3) Are there any ambiguous terms? |
| WTI-008c | Missing Information Flag | HARD | If insufficient context exists to write specific AC, Claude MUST ask for clarification rather than generating vague AC. Sufficiency rubric: INSUFFICIENT -- "create a bug for the login issue" (no symptom, steps, or location). INSUFFICIENT -- "create a story for user profile editing" (no role, goal, or benefit). SUFFICIENT -- user provides detailed symptom with repro steps, or specific role with observable goal (proceed to creation). |
| WTI-008d | Skip Mechanism | MEDIUM | User can say "skip" or "just create it" to bypass checkpoints. Claude must acknowledge the quality trade-off: "Skipping quality review. Note: AC may need refinement later." Add comment in file: `<!-- WTI-008: Checkpoint skipped by user -->`. |

**Checkpoint Interaction Templates:**

For **Stories (PBIs)**:
```
Before I create this story, let me confirm my understanding:

- **Role:** [who benefits]
- **Goal:** [what they can do]
- **Benefit:** [why it matters]

Does this capture the intent?

(Recommended) Yes, proceed to AC draft
(Recommended) Correct these details first
Skip -- create with what we have
```

For **Bugs**:
```
Before I create this bug, let me confirm my understanding:

- **Symptom:** [what the user sees]
- **Location:** [where it occurs]
- **Severity:** [impact level]
- **Repro steps:** [how to reproduce]

Does this capture the issue?

(Recommended) Yes, proceed to AC draft
(Recommended) Correct these details first
Skip -- create with what we have
```

For **AC Review** (all types):
```
Here are the proposed Acceptance Criteria:

[AC bullets]

Quality check:
1. Can an engineer build this without asking questions?
2. Can QA write test cases from these criteria?
3. Are there any ambiguous terms?

(Recommended) Approve and create
Revise -- [suggest changes]
Skip -- create as-is
```

**Anti-Pattern:** Creating a work item file with placeholder AC ("TBD", "To be determined") or vague AC generated from insufficient context.

**Why:** Work items created without user validation often miss critical context, contain assumptions, or address the wrong problem. Two brief checkpoints (pre-creation + AC review) catch these issues before they waste sprint planning time. The skip mechanism preserves user autonomy (P-020) when speed is needed.

---

## Work tracker (worktracker) Behavior

We use the Canonical model for all work items in our project documentation and tracking artifacts. The ADO Scrum, SAFe Terminology and Jira (Standard/Adv. Roadmaps) columns are provided for reference to map our canonical model to common frameworks and tools. If users use terminology from ADO Scrum, SAFe or JIRA, we should map it to our canonical model for consistency.

`WORKTRACKER.md` is the Global Manifest tracking all Initiatives and Epics, Bugs, Decisions, Discoveries and Impediments. It exists in the root of the project folder ({ProjectId} e.g. `PROJ-005-plugin-bugs`). It is a pointer with relationships to to the items it is tracking.

A folder is created for each Epic (`{EpicId}-{slug}`) in the `work/` folder.
Each Epic folder contains its own `{EpicId}-{slug}.md` tracking Features, Enablers, Stories and Tasks (Effort) for that Strategic Theme. This file also acts as a pointer with relationships to all respective artifacts of the Epic.

A folder (`{FeatureId}-{slug}`) is created for each Feature in the `work/{EpicId}-{slug}/` folder.
Each Feature folder contains its own `{FeatureId}-{slug}.md` tracking Unit of Work, Enablers and Tasks (Effort) for that Feature. Each `FEATURE-WORKTRACKER.md` must have and maintain relationships to related artifacts in-order to enable traceability and auditability as well as easier traversal for you - it is a pointer with relationships to all respective artifacts of the Feature.

A folder (`{EnablerId}-{slug}`) is created for each Enabler in the `work/{EpicId}-{slug}/{FeatureId}-{slug}/` folder.
Each Enabler folder contains its own `{EnablerId}-{slug}.md` tracking Tasks, Sub-Tasks, Spikes, Bugs, Impediments and Discoveries for that Enabler. Each `{EnablerId}-{slug}.md` must have and maintain relationships to related artifacts in-order to enable traceability and auditability as well as easier traversal for you - it is a pointer with relationships to all respective artifacts of the Enabler.

A folder (`{EnablerId}-{slug}`) is created for each Story in the `work/{EpicId}-{slug}/{FeatureId}-{slug}/` folder.
Each Story folder contains its own `{Story}-{slug}.md` tracking Tasks, Sub-Tasks, Spikes, Bugs, Impediments and Discoveries for that Story. Each `{Story}-{slug}.md` must have and maintain relationships to related artifacts in-order to enable traceability and auditability as well as easier traversal for you - it is a pointer with relationships to all respective artifacts of the Story.

A file is created for each Task, Sub-Task, Spike, Bug, Impediment and Discovery in the respective `{EnablerId}-{slug}` or `{StoryId}-{slug}` following the scheme outlined in the Directory Structure. Each Task, Sub-Task, Spike, Bug, Impediment and Discovery file must have and maintain relationships to related artifacts in-order to enable traceability and auditability as well as easier traversal for you.
Each Enabler and Story must contain verifiable acceptance criteria.
Each Enabler and Story must be broken down into detailed Tasks with verifiable evidence. Verifiable evidence (citations, references and sources) must be provided to support closing out a Task.

Use MCP Memory-Keeper to help you remember and maintain the structure and relationships of the Worktracker system. You don't have to remember everything, just remember to use MCP Memory-Keeper to help you keep track of everything. Try MCP Memory-Keeper first before searching the repository.

---

## Cross-References

- **Content Quality Standards**: `worktracker-content-standards.md` (detailed examples, anti-patterns, SPIDR framework)
- **Definition of Done**: `.context/templates/worktracker/DOD.md` (team-level DoD, referenced by WTI-007a)
- **Entity Hierarchy Rules**: `worktracker-entity-hierarchy.md`
- **System Mappings Rules**: `worktracker-system-mappings.md`
- **Directory Structure Rules**: `worktracker-directory-structure.md`
- **Template Usage Rules**: `worktracker-templates.md`
