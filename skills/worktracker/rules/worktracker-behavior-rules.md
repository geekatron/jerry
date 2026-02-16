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

> **Full details:** For enforcement procedures, violation examples, correct examples, anti-patterns, remediation severity levels, and compliance verification, see [WTI_RULES.md](../../../.context/templates/worktracker/WTI_RULES.md).

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
