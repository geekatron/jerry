# Worktracker Behavior Rules

> Rule file for /worktracker skill
> Source: CLAUDE.md lines 218-241 (EN-201 extraction)
> Extracted: 2026-02-01
> Updated: 2026-02-22 (Added WTI-008 Content Quality, WTI-009 Collaboration Before Creation - PROJ-005/PR-43)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Worktracker Integrity Rules](#worktracker-integrity-rules) | **CRITICAL** - Rules for keeping state accurate and honest (WTI-001 to WTI-006) |
| [Content Quality Rules](#content-quality-rules) | **CRITICAL** - Rules for work item content quality (WTI-008, WTI-009) |
| [Work tracker (worktracker) Behavior](#work-tracker-worktracker-behavior) | Canonical model and structure behavior |
| [Cross-References](#cross-references) | Links to other worktracker rule files |

---

## Worktracker Integrity Rules

> **Enforcement Level:** HARD
> **Source:** Process failure discovered during EN-201 execution (BUG: State drift)

These rules ensure the worktracker remains a **single source of truth** that is accurate, honest, and verifiable.

> **SSOT:** `.context/templates/worktracker/WTI_RULES.md` is the authoritative source for all WTI rule definitions. Consult the SSOT for full rationale, enforcement details, examples, and violation remediation procedures. The table below is a compact reference index.

| WTI Rule | Name | Tier | Summary |
|----------|------|------|---------|
| WTI-001 | Real-Time State Updates | HARD | Update worktracker status immediately after completing work. No batching. |
| WTI-002 | No Closure Without Verification | HARD | All acceptance criteria verified and evidence provided before DONE. |
| WTI-003 | Truthful and Accurate State | HARD | Status reflects reality -- truthful, accurate, honest, verifiable. |
| WTI-004 | Synchronize Before Reporting | HARD | Read fresh state before any status report. Never rely on cached state. |
| WTI-005 | Atomic Task State | HARD | Update child file AND parent reference atomically in the same operation. |
| WTI-006 | Evidence-Based Closure | HARD | Evidence section MUST contain verifiable links before closure. |
| WTI-007 | Mandatory Template Usage | HARD | Read canonical template from `.context/templates/worktracker/` before creating entity files. Never create from memory. |
| WTI-008 | Content Quality Standards | HARD | Work item content (Summary, AC, Description) MUST meet content quality standards. |
| WTI-009 | Collaboration Before Creation | HARD | Validate understanding with user before creating work items with AC. |

> **Full details:** For enforcement procedures, violation examples, correct examples, anti-patterns, remediation severity levels, and compliance verification, see [WTI_RULES.md](../../../.context/templates/worktracker/WTI_RULES.md).

---

## Content Quality Rules

> **Enforcement Level:** HARD
> **Source:** PROJ-005-jerry-process-improvements (ADO skill pattern extraction + industry research)
> **Added:** 2026-02-17
> **Reference:** `worktracker-content-standards.md` for detailed examples, anti-patterns, and writing guidance

These rules ensure work item **content** is clear, concise, and actionable. They complement WTI-001 through WTI-006 (which ensure structural integrity) by enforcing what is written inside work items.

**Applicability (DEC-006):** These rules apply to **newly created** work items only. The wt-auditor flags existing violations as INFO (advisory), not blocking.

### WTI-008: Content Quality Standards (HARD)

**Rule:** All work item content (Summary, Acceptance Criteria, Description) MUST meet content quality standards defined in `worktracker-content-standards.md`.

**The #1 Rule:** "If engineers, UX designers, or QA need to ask clarifying questions, the Acceptance Criteria has failed."

| Sub-Rule | Name | Enforcement | Detail |
|----------|------|-------------|--------|
| WTI-008a | No DoD in AC | HARD | AC must not contain Definition of Done items: test coverage, code review, documentation updates, deployment verification, QA sign-off. Universal test: "If it applies to every work item equally, it is DoD, not AC." |
| WTI-008b | No Implementation Details in AC | HARD | AC must not contain file paths, class names, method names, architecture patterns, or technology-specific decisions. Implementation details belong in the Description section, Implementation Notes section, or child Task descriptions -- never in AC. For Tasks and Enablers, focus on verifiable outcomes rather than implementation procedures (e.g., "API returns 204 on success" not "Call DELETE endpoint"). |
| WTI-008c | Actor-First Format | MEDIUM | AC bullets should begin with an actor or system subject: "User can...", "System validates...", "API returns...", "Admin sees...". For Enablers, Features, and Tasks, the "actor" may be a system component, infrastructure element, or process (e.g., "Build pipeline...", "Database migration...", "Configuration file..."). |
| WTI-008d | No Hedge Words | MEDIUM | AC must not use hedge words: "should be able to", "might need to", "could potentially", "if possible", "ideally", "as needed", "when appropriate". Replace with direct, testable statements. |
| WTI-008e | AC Bullet Count Limits | HARD | Maximum AC bullets by type: Story: 5, Bug: 5, Task: 5, Enabler: 5, Feature: 5. Exceeding the limit triggers WTI-008g. |
| WTI-008f | Summary Brevity | MEDIUM | Summary must be 1-3 sentences. Describe the what and why. No implementation details. Bug summaries describe symptoms, not root causes. |
| WTI-008g | Scope Overflow Signal | HARD | If AC exceeds the bullet limit (WTI-008e), the work item scope is likely too large. Claude MUST flag this and recommend splitting using the SPIDR framework (Spike, Paths, Interfaces, Data, Rules). See `worktracker-content-standards.md` for SPIDR details. |

**Anti-Pattern:**

```markdown
# BAD AC (violates WTI-008a, WTI-008b):
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

### WTI-009: Collaboration Before Creation (HARD)

**Rule:** Claude MUST validate understanding with the user before creating work items that contain Acceptance Criteria.

**Applicability (DEC-007):** This rule applies to: Story (PBI), Bug, Task, Enabler, Feature. It does NOT apply to: Discovery, Decision, Impediment, Sub-Task. For batch creation of related items (e.g., decomposing a Story into Tasks), a single upfront checkpoint for the batch satisfies WTI-009a; individual per-item checkpoints are not required.

| Sub-Rule | Name | Enforcement | Detail |
|----------|------|-------------|--------|
| WTI-009a | Pre-Creation Checkpoint | HARD | Before writing a work item file, present a summary of what will be created and ask for confirmation. Adapt summary fields by type: role/goal/benefit for stories; symptom/location/severity for bugs; what/why for enablers and tasks. |
| WTI-009b | AC Review Checkpoint | HARD | After drafting AC but before writing the file, present the AC to the user. Ask: (1) Can an engineer build this without asking questions? (2) Can QA write test cases from these criteria? (3) Are there any ambiguous terms? |
| WTI-009c | Missing Information Flag | HARD | If insufficient context exists to write specific AC, Claude MUST ask for clarification rather than generating vague AC. Sufficiency rubric: INSUFFICIENT -- "create a bug for the login issue" (no symptom, steps, or location). INSUFFICIENT -- "create a story for user profile editing" (no role, goal, or benefit). BORDERLINE -- "create a task to fix the API error handling" (has what but lacks specific scope; ask one clarifying question). SUFFICIENT -- user provides detailed symptom with repro steps, or specific role with observable goal (proceed to creation). |
| WTI-009d | Skip Mechanism | MEDIUM | User can say "skip", "just create it", or "cancel" to bypass or abort checkpoints. For skip: Claude acknowledges the quality trade-off: "Skipping quality review. AC may need refinement later." Add comment in file: `<!-- WTI-009: Checkpoint skipped by user -->`. For cancel: abort creation entirely. |

**Checkpoint Interaction Patterns:**

For **Stories (PBIs)** — present a summary and ask naturally:

> Before I create this story, let me confirm my understanding:
> - **Role:** [who benefits]
> - **Goal:** [what they can do]
> - **Benefit:** [why it matters]
>
> Does this capture the intent? Let me know if I should proceed to drafting AC, or if you'd like to correct any details first. You can also say "skip" to bypass this checkpoint or "cancel" to abort.

For **Bugs** — summarize the defect understanding:

> Before I create this bug, let me confirm my understanding:
> - **Symptom:** [what the user sees]
> - **Location:** [where it occurs]
> - **Severity:** [impact level]
> - **Repro steps:** [how to reproduce]
>
> Does this capture the issue? I'll proceed to drafting AC once confirmed, or you can correct any details. Say "skip" to bypass or "cancel" to abort.

For **AC Review** (all types) — present AC with quality questions:

> Here are the proposed Acceptance Criteria:
>
> [AC bullets]
>
> Quick quality check: (1) Can an engineer build this without questions? (2) Can QA write test cases from this? (3) Any ambiguous terms?
>
> Let me know if this looks good to create, or suggest revisions. Say "skip" to create as-is or "cancel" to abort.

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
- **Definition of Done**: `.context/templates/worktracker/DOD.md` (team-level DoD, referenced by WTI-008a)
- **Entity Hierarchy Rules**: `worktracker-entity-hierarchy.md`
- **System Mappings Rules**: `worktracker-system-mappings.md`
- **Directory Structure Rules**: `worktracker-directory-structure.md`
- **Template Usage Rules**: `worktracker-templates.md`
