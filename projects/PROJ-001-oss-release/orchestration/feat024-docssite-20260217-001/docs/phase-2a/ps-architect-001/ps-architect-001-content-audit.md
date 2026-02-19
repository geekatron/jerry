# Phase 2A Content Audit Report

> **Agent:** ps-architect-001
> **Phase:** 2A (EN-947: Content Curation & Landing Page)
> **Workflow:** feat024-docssite-20260217-001
> **Date:** 2026-02-17

## Document Sections

| Section | Purpose |
|---------|---------|
| [Task Summary](#task-summary) | Completion status of TASK-001 through TASK-005 |
| [Content Classification](#content-classification) | Full audit of docs/ directory |
| [Nav Structure](#nav-structure) | Final mkdocs.yml nav decisions |
| [Link and Content Issues](#link-and-content-issues) | Issues found during TASK-005 review |
| [Files Modified](#files-modified) | List of files changed in this phase |

---

## Task Summary

| Task | Description | Status | Notes |
|------|-------------|--------|-------|
| TASK-001 | Improve docs/index.md | COMPLETE | Landing page rewritten with branding, capabilities, Why Jerry?, Quick Start, Guides, Reference, Skills table. H-23/H-24 compliant (nav table with anchor links). |
| TASK-002 | Audit docs/ directory | COMPLETE | Full classification below. 57 files audited across 14 directories. |
| TASK-003 | Define nav structure in mkdocs.yml | COMPLETE | Nav updated with 4 top-level sections: Getting Started, Guides, Reference, Governance. Internal dirs excluded. |
| TASK-004 | Link getting-started paths | COMPLETE | runbooks/getting-started.md verified, linked from landing page Quick Start section and nav (under Getting Started). |
| TASK-005 | Review selected docs for issues | COMPLETE | 11 issues identified across 6 files. See details below. |

---

## Content Classification

### Directory-Level Classification

| Directory | Classification | Rationale |
|-----------|---------------|-----------|
| `docs/` (root files) | PUBLIC | index.md, INSTALLATION.md, BOOTSTRAP.md, CLAUDE-MD-GUIDE.md are all user-facing |
| `docs/adrs/` | PARTIAL | ADRs are architecture decisions -- relevant as reference, but contain internal work item references. Excluded from initial nav; can be added later as a curated subset. |
| `docs/analysis/` | INTERNAL | Internal analysis artifacts (work items). Contains work-025-e-001, work-026-e-002. Not user-facing. |
| `docs/design/` | INTERNAL | Internal architecture design docs (PYTHON-ARCHITECTURE-STANDARDS.md). Not user-facing. |
| `docs/governance/` | PARTIAL | JERRY_CONSTITUTION.md is public (defines agent behavioral principles). AGENT_CONFORMANCE_RULES.md and BEHAVIOR_TESTS.md are internal governance tooling. |
| `docs/knowledge/` | INTERNAL | Internal exemplars, research materials, framework reference docs. 20+ files. Not user-facing. |
| `docs/playbooks/` | PUBLIC | All 4 playbooks are user-facing skill guides: problem-solving.md, orchestration.md, transcript.md, PLUGIN-DEVELOPMENT.md. |
| `docs/research/` | INTERNAL | Internal research artifacts. Contains work-026-e-001. Not user-facing. |
| `docs/runbooks/` | PUBLIC | getting-started.md is the primary onboarding runbook. |
| `docs/schemas/` | PARTIAL | SCHEMA_VERSIONING.md and SESSION_CONTEXT_GUIDE.md are useful developer reference. session_context.json and types/ are raw schema files (included implicitly but not in nav). |
| `docs/specifications/` | INTERNAL | Internal specifications (JERRY_URI_SPECIFICATION.md). Not user-facing. |
| `docs/synthesis/` | INTERNAL | Internal synthesis artifacts. Not user-facing. |
| `docs/templates/` | INTERNAL | Internal migration guides (AGENT_MIGRATION_GUIDE.md). Not user-facing. |

### File-Level Classification (Public Files)

| File | Classification | In Nav? | Notes |
|------|---------------|---------|-------|
| `index.md` | PUBLIC | Yes (Home) | Rewritten in TASK-001 |
| `INSTALLATION.md` | PUBLIC | Yes (Getting Started) | Core installation guide, 831 lines |
| `BOOTSTRAP.md` | PUBLIC | Yes (Getting Started) | Context distribution setup, 170 lines |
| `CLAUDE-MD-GUIDE.md` | PUBLIC | Yes (Reference) | Developer context loading guide, 118 lines |
| `CNAME` | PUBLIC (infra) | No | Custom domain file for GitHub Pages. Not a doc. |
| `runbooks/getting-started.md` | PUBLIC | Yes (Getting Started) | Primary onboarding runbook, 209 lines |
| `playbooks/problem-solving.md` | PUBLIC | Yes (Guides) | Problem-solving skill playbook, 233 lines |
| `playbooks/orchestration.md` | PUBLIC | Yes (Guides) | Orchestration skill playbook, 262 lines |
| `playbooks/transcript.md` | PUBLIC | Yes (Guides) | Transcript skill playbook, 280 lines |
| `playbooks/PLUGIN-DEVELOPMENT.md` | PUBLIC | Yes (Guides) | Plugin development playbook, 432 lines |
| `governance/JERRY_CONSTITUTION.md` | PUBLIC | Yes (Governance) | Constitutional principles, public-appropriate |
| `schemas/SCHEMA_VERSIONING.md` | PUBLIC | Yes (Reference) | Schema versioning guide for contributors |
| `schemas/SESSION_CONTEXT_GUIDE.md` | PUBLIC | Yes (Reference) | Session context schema guide for contributors |

### File-Level Classification (Internal/Excluded Files)

| File | Classification | Reason for Exclusion |
|------|---------------|---------------------|
| `governance/AGENT_CONFORMANCE_RULES.md` | INTERNAL | Internal agent template conformance tooling |
| `governance/BEHAVIOR_TESTS.md` | INTERNAL | Internal behavioral test golden dataset |
| `analysis/work-025-e-001-model-selection-effort.md` | INTERNAL | Work item analysis artifact |
| `analysis/work-026-e-002-transcript-skill-gap-analysis.md` | INTERNAL | Work item analysis artifact |
| `design/PYTHON-ARCHITECTURE-STANDARDS.md` | INTERNAL | Internal architecture design doc |
| `research/work-026-e-001-jerry-skill-patterns.md` | INTERNAL | Work item research artifact |
| `specifications/JERRY_URI_SPECIFICATION.md` | INTERNAL | Internal URI specification |
| `synthesis/work-026-e-003-jerry-skill-compliance-framework.md` | INTERNAL | Work item synthesis artifact |
| `templates/AGENT_MIGRATION_GUIDE.md` | INTERNAL | Internal migration guide |
| `knowledge/` (entire directory, 25 files) | INTERNAL | Exemplars (patterns, architecture, rules, templates, frameworks), research materials. Subdirs: exemplars/patterns (1), exemplars/architecture (3), exemplars/rules (3), exemplars/templates (8), exemplars/frameworks/problemsolving (5), root (1 — DISCOVERIES_EXPANDED.md). |
| `adrs/` (all 7 ADR files) | DEFERRED | ADRs contain internal work item refs (WI-SAO-xxx, en004-adr-xxx). Candidate for future curated inclusion after content scrubbing. |
| `schemas/session_context.json` | INTERNAL | Raw JSON schema file (referenced by guide, not directly navigated) |
| `schemas/types/session_context.py` | INTERNAL | Python type definitions |
| `schemas/types/session_context.ts` | INTERNAL | TypeScript type definitions |

---

## Nav Structure

Final `mkdocs.yml` nav section:

```yaml
nav:
  - Home: index.md
  - Getting Started:
    - Installation: INSTALLATION.md
    - Bootstrap: BOOTSTRAP.md
    - Getting Started Runbook: runbooks/getting-started.md
  - Guides:
    - Problem Solving: playbooks/problem-solving.md
    - Orchestration: playbooks/orchestration.md
    - Transcript Processing: playbooks/transcript.md
    - Plugin Development: playbooks/PLUGIN-DEVELOPMENT.md
  - Reference:
    - CLAUDE.md Guide: CLAUDE-MD-GUIDE.md
    - Schema Versioning: schemas/SCHEMA_VERSIONING.md
    - Session Context Schema: schemas/SESSION_CONTEXT_GUIDE.md
  - Governance:
    - Jerry Constitution: governance/JERRY_CONSTITUTION.md
```

### Nav Decisions

| Decision | Rationale |
|----------|-----------|
| Moved Getting Started Runbook under Getting Started (not Guides) | It is part of the onboarding flow, logically follows Installation and Bootstrap |
| Added Transcript Processing to Guides | Public playbook, was missing from Phase 1 stub nav |
| Added Plugin Development to Guides | Public playbook, was missing from Phase 1 stub nav |
| Added Schema docs to Reference | Developer-facing reference material useful for contributors |
| Created Governance section | Jerry Constitution is a differentiating public doc that explains agent behavioral principles |
| Excluded ADRs from nav | ADRs reference internal work items (WI-SAO-xxx); need content scrubbing before public inclusion |
| Excluded all internal directories | analysis/, design/, knowledge/, research/, specifications/, synthesis/, templates/ are not user-facing |

---

## Link and Content Issues

Issues discovered during TASK-005 review of public-facing docs. These are reported for QG-1 and do not block Phase 2A completion.

### Go-Live Risk Prioritization

| Priority | Issue IDs | Description | Launch Impact |
|----------|-----------|-------------|---------------|
| **LAUNCH-BLOCKING** | 1, 2, 7 | Broken cross-references in 4 playbooks + getting-started.md + transcript.md — primary user-facing guides will have 404 links | Users clicking skill/rule references get 404s on core guides |
| **POST-LAUNCH** | 3, 6 | INSTALLATION.md external refs, PLUGIN-DEVELOPMENT.md internal analysis exposure | Lower-traffic pages; functional content still readable |
| **ACCEPTABLE-DEBT** | 4, 5, 8, 9, 10, 11 | Collaborator-specific content, informational path refs, ADR internal refs, schema internal paths | No user-visible impact; cosmetic or informational |

### Issue 1: Internal path references in playbooks

**Files:** `playbooks/problem-solving.md`, `playbooks/orchestration.md`
**Issue:** Multiple links point to `.context/rules/quality-enforcement.md` and `skills/*/SKILL.md` which are outside the `docs/` directory and will produce 404s on the docs site.
**Examples:**
- `[H-04](../../.context/rules/quality-enforcement.md#hard-rule-index)` (problem-solving.md:51)
- `[SKILL.md](../../skills/problem-solving/SKILL.md)` (problem-solving.md:4, 229)
- `[SKILL.md](../../skills/orchestration/SKILL.md)` (orchestration.md:4, 259)
- `[quality-enforcement.md](../../.context/rules/quality-enforcement.md)` (orchestration.md:208, 260)
- `[orch-planner.md](../../skills/orchestration/agents/orch-planner.md)` (orchestration.md:166)
**Severity:** MEDIUM -- Links will be broken on the public docs site. Content still readable.
**Recommendation:** Either copy referenced files into docs/ or convert these to non-linking references.

### Issue 2: Internal path references in getting-started.md

**File:** `runbooks/getting-started.md`
**Issue:** Links to `.context/rules/quality-enforcement.md` and `governance/JERRY_CONSTITUTION.md` using `../../` relative paths that may not resolve correctly on the docs site.
**Examples:**
- `[H-04](../../.context/rules/quality-enforcement.md#hard-rule-index)` (line 35)
- `[P-002](../governance/JERRY_CONSTITUTION.md#p-002-file-persistence)` (lines 166, 152 in orchestration.md)
**Severity:** MEDIUM -- Broken links on docs site.
**Recommendation:** Replace `.context/` references with docs-site-relative links or remove the link while keeping the rule ID text.

### Issue 3: Internal path references in INSTALLATION.md

**File:** `INSTALLATION.md`
**Issue:** References to `../CONTRIBUTING.md` and `../LICENSE` which are outside docs/ and will 404.
**Examples:**
- `[CONTRIBUTING.md](../CONTRIBUTING.md)` (lines 753, 788)
- `[Apache License 2.0](../LICENSE)` (line 830)
**Severity:** LOW -- These are in the "For Developers" section which is less critical.
**Recommendation:** Link to the GitHub repo URLs instead (e.g., `https://github.com/geekatron/jerry/blob/main/CONTRIBUTING.md`).

### Issue 4: Collaborator-specific content in INSTALLATION.md

**File:** `INSTALLATION.md`
**Issue:** The "Collaborator Installation (Private Repository)" section (lines 47-275) describes SSH key setup for private repo access. When the repo becomes public, this section becomes irrelevant and could confuse users.
**Severity:** LOW -- The doc already includes a "Future: Public Repository" section that anticipates this.
**Recommendation:** Consider restructuring post-public-release to lead with the simpler public installation flow.

### Issue 5: Internal project path references in playbooks

**Files:** `playbooks/problem-solving.md`, `playbooks/orchestration.md`
**Issue:** References to `projects/{JERRY_PROJECT}/` paths which expose internal project structure.
**Severity:** LOW -- These are instructional (showing users where output goes) and are appropriate for public docs.
**Recommendation:** No action needed. These are intentional documentation of the project workflow.

### Issue 6: PLUGIN-DEVELOPMENT.md contains Jerry-specific internal analysis

**File:** `playbooks/PLUGIN-DEVELOPMENT.md`
**Issue:** The "Jerry Project Structure Analysis" section (lines 189-230) and "Gotchas and Conflicts" section (lines 232-324) contain internal project structure analysis with ISSUE/CONFLICT annotations. This reads more like an internal audit than a public guide.
**Severity:** MEDIUM -- Exposes internal structural issues to public users.
**Recommendation:** Consider splitting into: (a) a generic "How to develop Claude Code plugins" public guide, and (b) an internal "Jerry plugin architecture issues" doc.

### Issue 7: Transcript playbook references to internal SKILL.md

**File:** `playbooks/transcript.md`
**Issue:** Multiple references to `../../skills/transcript/SKILL.md` which is outside docs/.
**Examples:**
- `[transcript/SKILL.md](../../skills/transcript/SKILL.md)` (line 3)
- `[SKILL.md Design Rationale](../../skills/transcript/SKILL.md#design-rationale-hybrid-pythonllm-architecture)` (line 80)
- `[ADR-006](../../skills/transcript/SKILL.md#design-rationale-mindmap-default-on-decision)` (line 128)
**Severity:** MEDIUM -- Broken links on docs site.
**Recommendation:** Same as Issue 1.

### Issue 8: Constitution references internal work items

**File:** `governance/JERRY_CONSTITUTION.md`
**Issue:** Contains references to internal session IDs (e.g., "Session claude/create-code-plugin-skill-MG1nh") and work item IDs (e.g., "WORK-028"). These are fine for governance but expose internal process.
**Severity:** LOW -- Minimal user impact, appears in attribution metadata.
**Recommendation:** Consider stripping session IDs from Author field for public release.

### Issue 9: BOOTSTRAP.md references internal scripts

**File:** `BOOTSTRAP.md`
**Issue:** References `scripts/bootstrap_context.py` and `.context/` paths which are internal to the repo structure. This is appropriate since BOOTSTRAP.md is specifically about setting up the repo after cloning.
**Severity:** INFORMATIONAL -- Appropriate for the document's purpose.
**Recommendation:** No action needed.

### Issue 10: Schema guides reference internal file paths

**Files:** `schemas/SCHEMA_VERSIONING.md`, `schemas/SESSION_CONTEXT_GUIDE.md`
**Issue:** Reference internal paths like `TOOL_REGISTRY.yaml`, `skills/orchestration/templates/ORCHESTRATION.template.yaml`, `.claude/agents/TEMPLATE.md`. These are developer-facing reference docs, so internal paths are expected.
**Severity:** INFORMATIONAL -- Appropriate for developer reference.
**Recommendation:** No action needed.

### Issue 11: ADR files reference internal work items

**Files:** All files in `docs/adrs/`
**Issue:** ADRs contain work item references (WI-SAO-xxx, en004-adr-xxx) and internal exploration IDs. This is why ADRs are deferred from the nav.
**Severity:** INFORMATIONAL -- ADRs are deferred from nav pending content scrubbing.
**Recommendation:** If ADRs are added to nav in a future phase, strip internal work item references first.

---

## Files Modified

| File | Action | Description |
|------|--------|-------------|
| `docs/index.md` | Rewritten | Landing page with branding, capabilities, Why Jerry?, Quick Start, Guides, Reference, Skills table |
| `mkdocs.yml` | Updated | Nav section expanded with Getting Started, Guides, Reference, Governance sections |
| This file | Created | Phase 2A content audit report |

---

## Summary for QG-1

### Classification Breakdown

| Classification | Count | Details |
|---------------|-------|---------|
| PUBLIC | 13 | In nav: index.md, INSTALLATION.md, BOOTSTRAP.md, CLAUDE-MD-GUIDE.md, CNAME (infra), runbooks/getting-started.md, 4 playbooks, JERRY_CONSTITUTION.md, 2 schema guides |
| DEFERRED | 7 | docs/adrs/ — 7 ADR files pending internal work-item reference scrubbing |
| INTERNAL | 37 | knowledge/ (25), governance/ (2), analysis/ (2), design/ (1), research/ (1), specifications/ (1), synthesis/ (1), templates/ (1), schemas/ (3 — JSON + type defs) |
| **Total** | **57** | Verified via `find docs/ -type f \| wc -l` |

### Task Results

**Landing page** (TASK-001): Complete. H-23 (nav table) and H-24 (anchor links) compliant. Content covers all required sections: branding/tagline, core capabilities (5 items), Why Jerry? (4 reasons), Quick Start (3 steps with links), Guides table, Reference table, Skills table, License.

**Content audit** (TASK-002): 57 files audited across 14 directories. 13 files classified PUBLIC and included in nav. 7 ADR files deferred pending content scrubbing. 37 files classified INTERNAL and excluded.

**Nav structure** (TASK-003): 4 top-level sections with 12 pages total. No internal files referenced. Logical flow: onboarding (Getting Started) -> skill usage (Guides) -> deep reference (Reference) -> governance.

**Getting-started links** (TASK-004): Verified `runbooks/getting-started.md` exists with 209 lines of well-structured onboarding content. Linked from landing page Quick Start section and nav.

**Doc review** (TASK-005): 11 issues identified. 3 launch-blocking (broken links in core guides), 2 post-launch (lower-traffic pages), 6 acceptable-debt (informational/cosmetic). Primary concern: broken cross-references to files outside `docs/` (`.context/rules/`, `skills/*/SKILL.md`, `../CONTRIBUTING.md`). These will produce 404s on the live docs site.

### Security Note (QG-1 Revision)

**pymdownx.snippets removed from mkdocs.yml** (DA-001-qg1 remediation). The snippets extension was enabled without path restriction, which would allow arbitrary file inclusion via `--8<--` syntax in any markdown file, bypassing the PUBLIC/INTERNAL content isolation boundary. Removed entirely as no current docs use snippet inclusion syntax. If needed in future, must be configured with `restrict_base_path: true` and `base_path: docs`.
