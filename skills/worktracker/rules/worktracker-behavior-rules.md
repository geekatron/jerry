# Worktracker Behavior Rules

> Rule file for /worktracker skill
> Source: CLAUDE.md lines 218-241 (EN-201 extraction)
> Extracted: 2026-02-01
> Updated: 2026-02-01 (Added Integrity Rules - BUG discovered in EN-201)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Worktracker Integrity Rules](#worktracker-integrity-rules) | **CRITICAL** - Rules for keeping state accurate and honest |
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

- **Entity Hierarchy Rules**: `worktracker-entity-hierarchy.md`
- **System Mappings Rules**: `worktracker-system-mappings.md`
- **Directory Structure Rules**: `worktracker-directory-structure.md`
- **Template Usage Rules**: `worktracker-templates.md`
