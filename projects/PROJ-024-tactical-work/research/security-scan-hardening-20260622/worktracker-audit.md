# Audit Report: EPIC-004 Security-Scan Hardening Worktracker Entities

> **Type:** audit-report
> **Generated:** 2026-06-22
> **Agent:** wt-auditor
> **Audit Type:** full
> **Scope:** projects/PROJ-024-tactical-work/work/EPIC-004-security-scan-hardening/

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Coverage, issue counts, verdict |
| [Issues Found](#issues-found) | Errors, warnings, info items |
| [Remediation Plan](#remediation-plan) | Actionable fixes with effort estimates |
| [Files Audited](#files-audited) | Complete list of checked files |

---

## Summary

| Metric | Value |
|--------|-------|
| **Files Checked** | 10 (9 entities + WORKTRACKER.md) |
| **Coverage** | 100% |
| **Total Issues** | 8 |
| **Errors** | 3 |
| **Warnings** | 4 |
| **Info** | 1 |
| **Verdict** | FAILED |

---

## Issues Found

### Errors

| ID | File | Issue | Remediation |
|----|------|-------|-------------|
| E-001 | EN-007-security-scan-pipeline-hardening.md | **HIERARCHY VIOLATION (critical):** EN-007 is an Enabler parented directly to EPIC-004 (Epic). Per `worktracker-entity-hierarchy.md` containment rules: Epic → allowed children = `[Capability, Feature]` only. An Enabler's allowed parents are `[Feature, Epic]` — meaning an Enabler may sit directly under an Epic only when there is no intervening Feature. This structure is **permitted** by the hierarchy rule. However, EN-007's Children section lists STORY-026..030 as direct children. Per the same hierarchy, Enabler → allowed children = `[Task]` only. Stories are DeliveryItems with allowed parents `[Feature]`, not `[Enabler]`. The five Stories are placed inside the EN-007 folder with `Parent: EN-007` in their frontmatter — this is a **containment violation**. | See Remediation Plan items R-001 and R-002. The correct structure is: EPIC-004 → (new FEAT-xxx) → EN-007 + STORY-026..030. Alternatively, if a Feature container is not desired, the Stories must be re-parented to EPIC-004 directly (but Epic→Story is also not in the containment rules: Epic allows only Capability/Feature). The canonical fix is to insert a Feature between EPIC-004 and the delivery items. |
| E-002 | TASK-035-confirm-dependabot-settings.md | **Broken parent link path:** The Related Items section links to `EN-007-security-scan-pipeline-hardening/EN-007-security-scan-pipeline-hardening.md`. Because TASK-035 is already inside the `EN-007-security-scan-pipeline-hardening/` folder, this resolves to `.../EN-007-security-scan-pipeline-hardening/EN-007-security-scan-pipeline-hardening/EN-007-security-scan-pipeline-hardening.md` which does not exist. | Change the link to `EN-007-security-scan-pipeline-hardening.md` (no subfolder prefix — the `.md` is a sibling file). |
| E-003 | EPIC-004-security-scan-hardening.md | **Template section mismatch:** The EPIC template (`.context/templates/worktracker/EPIC.md`) requires a `Children (Features/Capabilities)` section [REQUIRED] that enumerates only Capability and Feature children. EPIC-004 instead uses a `Work Items` section that mixes EN-007, BUG-008, STORY-026..030, and TASK-035 — entities that are not direct children of an Epic per containment rules. This both uses a non-standard section heading and populates the section with non-conformant child types. | Rename the section to `Children (Features/Capabilities)`. If the hierarchy is restructured to insert a Feature, list only the Feature. Direct Bugs discovered at Epic level should follow the `{EpicId}--{BugId}-{slug}.md` naming pattern and live flat inside the Epic folder. |

### Warnings

| ID | File | Issue | Remediation |
|----|------|-------|-------------|
| W-001 | STORY-026..030 (all five Stories) | **Parent set to EN-007 (Enabler); Stories belong under a Feature.** All five Story files declare `Parent: EN-007` in their frontmatter blockquote. The worktracker hierarchy permits Feature → Story, but not Enabler → Story. This is a consequence of E-001 and affects all five stories consistently. | After the hierarchy is corrected (R-001), update the `Parent` field in each Story's frontmatter blockquote to the new Feature ID (e.g., `FEAT-NNN`). |
| W-002 | BUG-008-scheduled-scan-false-green.md | **Naming convention deviation:** The directory-structure rules specify that Bugs discovered at the Enabler level are placed flat inside the Enabler folder using pattern `{BugId}-{slug}.md` (correct). However, the Bug declares `Parent: EN-007` in its frontmatter. If the hierarchy is restructured to introduce a Feature (R-001), the Bug's parent must be updated to reflect the correct parent. Additionally, the directory-structure does not show BUG files with sub-folders — this file correctly has no sub-folder, which is conformant. | After hierarchy fix, verify Bug parent points to the correct parent entity. If Bug is discovered at Feature level, move to Feature folder using `{FeatureId}--{BugId}-{slug}.md` pattern. |
| W-003 | TASK-035-confirm-dependabot-settings.md | **Task placed flat in Enabler folder (no sub-folder) — correct per directory-structure rules. However:** The Task declares `Parent: EN-007` which is valid (Enabler → Task is permitted). The directory structure places task `.md` files flat inside the Enabler folder without a sub-folder, and TASK-035 follows this correctly. This warning is advisory: if the hierarchy is restructured (R-001), ensure TASK-035 remains under EN-007 (not the new Feature), as Task→Enabler parent is the valid relationship. | No action needed for the Task's parent relationship. Fix E-002 (broken parent link path). Monitor during hierarchy restructure to confirm TASK-035 remains under EN-007. |
| W-004 | EPIC-004-security-scan-hardening.md | **Missing template HTML comment header:** The EPIC template includes an HTML comment block (`<!-- TEMPLATE: Epic ... -->`) at the top. EPIC-004 does not include this comment. While not a hard requirement, template traceability is recommended for audit purposes. Other entities (Enabler, Stories, Task, Bug) also omit the template comment. | Optionally add `<!-- Template: .context/templates/worktracker/EPIC.md -->` as first line of the file. Apply consistently to all 9 entities. |

### Info

| ID | File | Issue | Remediation |
|----|------|-------|-------------|
| I-001 | All 9 entities | **H-32 placeholder:** All 9 entities carry `GitHub Issue: pending (to be linked by orchestrator)` — this satisfies the H-32 placeholder requirement. The WORKTRACKER.md does not record a GitHub Issue column for active items. When GH issues are created, update the `GitHub Issue` field to the actual URL/number in each entity file and add a GH Issue column to WORKTRACKER.md active items table. | Create GH issues for EPIC-004, EN-007, BUG-008, STORY-026..030, TASK-035 in `geekatron/jerry` and link them. |

---

## Detailed Findings by Check Type

### 1. Template Compliance

| Entity | Type | Required Sections Present | Status Field Valid | Notes |
|--------|------|--------------------------|-------------------|-------|
| EPIC-004 | Epic | Partial — `Work Items` instead of `Children (Features/Capabilities)` | pending ✓ | E-003 |
| EN-007 | Enabler | Yes — Summary, Problem Statement, Business Value, Technical Approach, Children, Progress Summary, Acceptance Criteria, Risks, History | pending ✓ | No Evidence section (optional per template) |
| BUG-008 | Bug | Yes — Summary, Reproduction Steps, Environment, Acceptance Criteria, Root Cause Analysis, Related Items, History | pending ✓ | Compliant |
| STORY-026 | Story | Yes — User Story, Summary, Acceptance Criteria, Children (Tasks), Progress Summary, Related Items, History | pending ✓ | Compliant |
| STORY-027 | Story | Yes | pending ✓ | Compliant |
| STORY-028 | Story | Yes | pending ✓ | Compliant |
| STORY-029 | Story | Yes | pending ✓ | Compliant |
| STORY-030 | Story | Yes | pending ✓ | Compliant |
| TASK-035 | Task | Yes — Summary, Acceptance Criteria, Evidence, Related Items, History | pending ✓ | E-002 (broken link in Related Items) |

All frontmatter status values extracted via `jerry ast frontmatter` — all are `pending` which is a valid status value.

### 2. Frontmatter / Metadata Validity (AST-verified)

| Entity | Type field | Status | Parent | GitHub Issue | Notes |
|--------|-----------|--------|--------|-------------|-------|
| EPIC-004 | epic | pending | PROJ-024 | pending (placeholder) | Missing `GitHub Issue` field in EPIC template; field added beyond template |
| EN-007 | enabler | pending | EPIC-004 | pending (placeholder) | Enabler Type: infrastructure ✓ |
| BUG-008 | bug | pending | EN-007 | pending (placeholder) | Severity: critical (extra field, acceptable) |
| STORY-026 | story | pending | EN-007 | pending (placeholder) | Parent should be Feature (W-001) |
| STORY-027 | story | pending | EN-007 | pending (placeholder) | Parent should be Feature (W-001) |
| STORY-028 | story | pending | EN-007 | pending (placeholder) | Parent should be Feature (W-001) |
| STORY-029 | story | pending | EN-007 | pending (placeholder) | Parent should be Feature (W-001) |
| STORY-030 | story | pending | EN-007 | pending (placeholder) | Parent should be Feature (W-001) |
| TASK-035 | task | pending | EN-007 | pending (placeholder) | Missing `Impact` field present in other tasks; optional |

### 3. Navigation Tables (H-23 / H-24)

All 9 entity files include a `## Document Sections` navigation table with anchor links. All files are well over 30 lines. Navigation tables are present and use anchor link format. **No violations.**

### 4. Relationship Integrity

**EPIC-004 ↔ EN-007:**
- EN-007 declares `Parent: EPIC-004` ✓
- EPIC-004 Work Items table lists EN-007 ✓
- Bidirectional link: present

**EN-007 ↔ BUG-008:**
- BUG-008 declares `Parent: EN-007` ✓
- EN-007 Children table lists BUG-008 ✓
- BUG-008 Related Items links to `EN-007-security-scan-pipeline-hardening.md` ✓

**EN-007 ↔ STORY-026..030:**
- All 5 Stories declare `Parent: EN-007` ✓
- EN-007 Children table lists all 5 Stories ✓
- Each Story's Related Items → Hierarchy links back to `../EN-007-security-scan-pipeline-hardening.md` ✓
- Bidirectional link: present; but the relationship itself violates containment (E-001 / W-001)

**EN-007 ↔ TASK-035:**
- TASK-035 declares `Parent: EN-007` ✓ (in blockquote frontmatter)
- EN-007 Children table lists TASK-035 ✓
- TASK-035 Related Items parent link path is broken (E-002)

**EPIC-004 ↔ direct children (BUG, STORIEs, TASK):**
- EPIC-004 Work Items table lists EN-007, BUG-008, STORY-026..030, TASK-035
- These non-Feature items should not appear as direct EPIC children per containment rules (E-001, E-003)

**No orphaned entities detected.** All 9 entities are reachable from WORKTRACKER.md.

### 5. Hierarchy Validity

**FINDING: The overall hierarchy structure is a containment violation.**

```
ACTUAL structure created:
EPIC-004 (Epic)
└── EN-007 (Enabler)          ← Epic→Enabler: PERMITTED (Enabler allowed_parents: [Feature, Epic])
    ├── BUG-008 (Bug)         ← Enabler folder bug: PERMITTED (Bugs discovered at Enabler level)
    ├── STORY-026 (Story)     ← Enabler→Story: VIOLATION (Enabler allowed_children: [Task] only)
    ├── STORY-027 (Story)     ← VIOLATION
    ├── STORY-028 (Story)     ← VIOLATION
    ├── STORY-029 (Story)     ← VIOLATION
    ├── STORY-030 (Story)     ← VIOLATION
    └── TASK-035 (Task)       ← Enabler→Task: PERMITTED

CORRECT structure per hierarchy rules:
EPIC-004 (Epic)
└── FEAT-NNN (Feature)        ← Epic→Feature: REQUIRED as intermediate container
    ├── EN-007 (Enabler)      ← Feature→Enabler: PERMITTED
    │   └── TASK-035 (Task)   ← Enabler→Task: PERMITTED
    ├── BUG-008 (Bug)         ← Feature-level bug (FEAT-NNN--BUG-008-*.md flat file)
    ├── STORY-026 (Story)     ← Feature→Story: PERMITTED
    ├── STORY-027 (Story)     ← PERMITTED
    ├── STORY-028 (Story)     ← PERMITTED
    ├── STORY-029 (Story)     ← PERMITTED
    └── STORY-030 (Story)     ← PERMITTED
```

**Root cause:** The creating agent omitted the Feature level between EPIC-004 and its delivery items (Stories, Enabler). The Epic containment rule (`allowed_children: [Capability, Feature]`) is satisfied by EN-007 only if the Enabler template is read in isolation (INV-EN03: "Enabler can have Feature or Epic as parent"), but the Story containment rule is not satisfied: Story's allowed parent is Feature, not Enabler.

**Note on Epic→Enabler:** The Enabler template (INV-EN03) and hierarchy rule both state `allowed_parents: [Feature, Epic]` — so EPIC-004 directly containing EN-007 is technically permitted by the Enabler's own rules. However, because EN-007 is then used as parent for Stories (which is forbidden), inserting a Feature is still the correct fix.

### 6. Directory Structure

| Check | Result |
|-------|--------|
| EPIC-004 folder: `EPIC-004-security-scan-hardening/` | Correct `{EpicId}-{slug}` pattern ✓ |
| EPIC-004 file: `EPIC-004-security-scan-hardening.md` | Correct ✓ |
| EN-007 folder: `EN-007-security-scan-pipeline-hardening/` | Correct `{EnablerId}-{slug}` pattern ✓ |
| EN-007 file: `EN-007-security-scan-pipeline-hardening.md` | Correct ✓ |
| BUG-008 file: `BUG-008-scheduled-scan-false-green.md` (flat in EN-007 folder) | Correct per Enabler-level bug pattern ✓ |
| TASK-035 file: `TASK-035-confirm-dependabot-settings.md` (flat in EN-007 folder) | Correct per Enabler-level task pattern ✓ |
| STORY-026 folder: `STORY-026-unify-ci-scheduled-scan/` | Correct naming pattern — but Stories belong in Feature folder, not Enabler folder (E-001) |
| STORY-027 folder: `STORY-027-cve-accept-list/` | Correct naming — wrong container (E-001) |
| STORY-028 folder: `STORY-028-owner-alerting-github-issue/` | Correct naming — wrong container (E-001) |
| STORY-029 folder: `STORY-029-fix-silent-failure-guard/` | Correct naming — wrong container (E-001) |
| STORY-030 folder: `STORY-030-remediate-transitive-cves/` | Correct naming — wrong container (E-001) |

Story sub-folders correctly contain only the Story `.md` file (no nested tasks yet — task decomposition is noted as pending). Sub-folder structure for Stories is correct.

### 7. WORKTRACKER.md Sync

All 9 new entities appear in the WORKTRACKER.md active work items table with correct ID, Type, Title, Status, and Parent values. Sync is complete and accurate.

| Entity | In WORKTRACKER.md | Type Correct | Status Correct | Parent Correct |
|--------|-------------------|-------------|---------------|---------------|
| EPIC-004 | ✓ | Epic ✓ | pending ✓ | PROJ-024 ✓ |
| EN-007 | ✓ | Enabler ✓ | pending ✓ | EPIC-004 ✓ |
| BUG-008 | ✓ | Bug ✓ | pending ✓ | EN-007 ✓ |
| STORY-026 | ✓ | Story ✓ | pending ✓ | EN-007 ✓ |
| STORY-027 | ✓ | Story ✓ | pending ✓ | EN-007 ✓ |
| STORY-028 | ✓ | Story ✓ | pending ✓ | EN-007 ✓ |
| STORY-029 | ✓ | Story ✓ | pending ✓ | EN-007 ✓ |
| STORY-030 | ✓ | Story ✓ | pending ✓ | EN-007 ✓ |
| TASK-035 | ✓ | Task ✓ | pending ✓ | EN-007 ✓ |

### 8. ID Uniqueness

Jerry worktracker IDs are **project-scoped** (each project maintains its own ID sequence). Evidence: BUG-008 exists in PROJ-001-oss-release, PROJ-030-bugs, and now PROJ-024-tactical-work — all different projects with independent ID sequences. EPIC-004, EN-007, BUG-008, STORY-026..030, and TASK-035 also appear in other projects but those are different projects. TASK-035 exists in PROJ-014 (`TASK-035-phase5b-conditional-adoption.md`) which is a different project and does not constitute a collision.

**Within PROJ-024-tactical-work:** All 9 new IDs are unique. No collision with existing PROJ-024 IDs (highest prior IDs were TASK-034, EN-006, STORY-025, BUG-007, EPIC-003).

**Verdict: No ID collisions within PROJ-024.**

### 9. H-32 GitHub Issue Parity

All 9 entities carry `GitHub Issue: pending (to be linked by orchestrator)` in their frontmatter blockquote. This satisfies the H-32 placeholder requirement for newly-created entities. GH issues must be created and linked before work begins.

---

## Remediation Plan

| # | Issue | Files Affected | Action | Effort |
|---|-------|---------------|--------|--------|
| R-001 | **E-001 (CRITICAL): Insert Feature between EPIC-004 and delivery items.** Create `FEAT-NNN-security-scan-hardening/` folder inside `EPIC-004-security-scan-hardening/`. Create `FEAT-NNN-security-scan-hardening.md` with `Parent: EPIC-004`. Move EN-007 folder and STORY-026..030 folders into the Feature folder. Move BUG-008 flat file into Feature folder, rename to `FEAT-NNN--BUG-008-scheduled-scan-false-green.md`. Update EPIC-004 Work Items section to list only FEAT-NNN. Update all Story parent fields from `EN-007` to `FEAT-NNN`. Update BUG-008 parent from `EN-007` to `FEAT-NNN`. Update WORKTRACKER.md parent columns for STORY-026..030 and BUG-008. Update EN-007 children to remove Stories (they move to Feature level). | EPIC-004-security-scan-hardening.md, EN-007-security-scan-pipeline-hardening.md, BUG-008-scheduled-scan-false-green.md, STORY-026..030 (all 5), WORKTRACKER.md | Create new Feature entity; restructure directory; update parent fields | High |
| R-002 | **E-001 (CRITICAL) — alternative if Feature insertion is not desired:** Re-parent all 5 Stories to EPIC-004 directly. This still violates the containment rule (Epic → Story is not in `allowed_children: [Capability, Feature]`). Therefore a Feature container is the only standards-conformant path. The alternative is not recommended. | N/A | Not recommended | — |
| R-003 | **E-002: Fix broken parent link in TASK-035.** In the Related Items section, change `EN-007-security-scan-pipeline-hardening/EN-007-security-scan-pipeline-hardening.md` to `EN-007-security-scan-pipeline-hardening.md`. | TASK-035-confirm-dependabot-settings.md | One-line edit | Low |
| R-004 | **E-003: Rename EPIC-004 children section.** Change `## Work Items` to `## Children (Features/Capabilities)`. After R-001, list only the new Feature. Remove Enabler, Bug, Stories, Task from EPIC direct children (they move under Feature). | EPIC-004-security-scan-hardening.md | Section rename + content update | Low |
| R-005 | **W-001: Update Story parent frontmatter** (addressed by R-001). | STORY-026..030 | Frontmatter update during restructure | Low (part of R-001) |
| R-006 | **I-001: Create GH Issues for all 9 entities.** Use `gh issue create` for each, link worktracker ID in body, update each entity's `GitHub Issue` field. | All 9 entities + WORKTRACKER.md | GH issue creation | Medium |

---

## Files Audited

| File | Entity | Lines | Checked |
|------|--------|-------|---------|
| projects/PROJ-024-tactical-work/WORKTRACKER.md | Project manifest | 84 | ✓ |
| projects/PROJ-024-tactical-work/work/EPIC-004-security-scan-hardening/EPIC-004-security-scan-hardening.md | EPIC-004 | 62 | ✓ |
| projects/PROJ-024-tactical-work/work/EPIC-004-security-scan-hardening/EN-007-security-scan-pipeline-hardening/EN-007-security-scan-pipeline-hardening.md | EN-007 | 117 | ✓ |
| projects/PROJ-024-tactical-work/work/EPIC-004-security-scan-hardening/EN-007-security-scan-pipeline-hardening/BUG-008-scheduled-scan-false-green.md | BUG-008 | 112 | ✓ |
| projects/PROJ-024-tactical-work/work/EPIC-004-security-scan-hardening/EN-007-security-scan-pipeline-hardening/STORY-026-unify-ci-scheduled-scan/STORY-026-unify-ci-scheduled-scan.md | STORY-026 | 82 | ✓ |
| projects/PROJ-024-tactical-work/work/EPIC-004-security-scan-hardening/EN-007-security-scan-pipeline-hardening/STORY-027-cve-accept-list/STORY-027-cve-accept-list.md | STORY-027 | 83 | ✓ |
| projects/PROJ-024-tactical-work/work/EPIC-004-security-scan-hardening/EN-007-security-scan-pipeline-hardening/STORY-028-owner-alerting-github-issue/STORY-028-owner-alerting-github-issue.md | STORY-028 | 82 | ✓ |
| projects/PROJ-024-tactical-work/work/EPIC-004-security-scan-hardening/EN-007-security-scan-pipeline-hardening/STORY-029-fix-silent-failure-guard/STORY-029-fix-silent-failure-guard.md | STORY-029 | 82 | ✓ |
| projects/PROJ-024-tactical-work/work/EPIC-004-security-scan-hardening/EN-007-security-scan-pipeline-hardening/STORY-030-remediate-transitive-cves/STORY-030-remediate-transitive-cves.md | STORY-030 | 95 | ✓ |
| projects/PROJ-024-tactical-work/work/EPIC-004-security-scan-hardening/EN-007-security-scan-pipeline-hardening/TASK-035-confirm-dependabot-settings.md | TASK-035 | 58 | ✓ |

**Total: 10 files, 100% coverage.**

---

*Audit Report Version: 1.0.0*
*Agent: wt-auditor v1.0.0*
*Constitutional Compliance: P-002 (persisted), P-003 (no subagents), P-020 (read-only, no auto-fixes)*
*Frontmatter extracted via: `jerry ast frontmatter` (H-33 compliant)*
*Generated: 2026-06-22*
