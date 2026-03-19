# Current-State Inventory: Jerry Framework Documentation Surface

> **Phase:** A1 (Workstream A)
> **Agent:** ps-researcher
> **Project:** PROJ-0037-doc-module
> **Date:** 2026-03-08

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Key gaps at a glance |
| [L1: Per-Skill Delta Table](#l1-per-skill-delta-table) | Presence across all documentation surfaces |
| [L2: Full Inventory](#l2-full-inventory) | Complete inventory with line references |

---

## L0: Executive Summary

1. **README lists 6 of 13 skills.** Seven skills are completely absent: `/adversary`, `/ast`, `/bootstrap`, `/eng-team`, `/red-team`, `/saucer-boy`, `/saucer-boy-framework-voice`.
2. **README claims "8 specialized agents" — actual count is 58.** AGENTS.md verified count (2026-02-22): 9 + 10 + 3 + 3 + 3 + 5 + 3 + 1 + 10 + 11 = 58 invokable agents across 10 skill directories.
3. **README documentation table lists 4 documents — at least 8 more are user-relevant.** Missing: Bootstrap guide, Getting Started runbook, Constitution, playbooks (problem-solving, orchestration, transcript), CLAUDE-MD Guide, Plugin Development playbook.
4. **CLAUDE.md lists 12 skills; mandatory-skill-usage.md routes 10.** Bootstrap is absent from CLAUDE.md. Architecture and bootstrap are absent from the trigger map.
5. **Example session output path uses legacy convention.** Shows `docs/analysis/EN-001-e-001-test-failures.md` — current convention uses `projects/{PROJECT_ID}/` paths.

---

## L1: Per-Skill Delta Table

| # | Skill | SKILL.md | README | CLAUDE.md | Trigger Map | AGENTS.md | Agents |
|---|-------|----------|--------|-----------|-------------|-----------|--------|
| 1 | `/adversary` | Y | **N** | Y | Y | Y (3) | adv-executor, adv-scorer, adv-selector |
| 2 | `/architecture` | Y | **N** | Y | **N** | **N** (0 agents) | — |
| 3 | `/ast` | Y | **N** | Y | Y | **N** (0 agents) | — |
| 4 | `/bootstrap` | Y | **N** | **N** | **N** | **N** (0 agents) | — |
| 5 | `/eng-team` | Y | **N** | Y | Y | Y (10) | eng-architect, eng-backend, eng-devsecops, eng-frontend, eng-incident, eng-infra, eng-lead, eng-qa, eng-reviewer, eng-security |
| 6 | `/nasa-se` | Y | Y | Y | Y | Y (10) | nse-architecture, nse-configuration, nse-explorer, nse-integration, nse-qa, nse-reporter, nse-requirements, nse-reviewer, nse-risk, nse-verification |
| 7 | `/orchestration` | Y | Y | Y | Y | Y (3) | orch-planner, orch-synthesizer, orch-tracker |
| 8 | `/problem-solving` | Y | Y | Y | Y | Y (9) | ps-analyst, ps-architect, ps-critic, ps-investigator, ps-reporter, ps-researcher, ps-reviewer, ps-synthesizer, ps-validator |
| 9 | `/red-team` | Y | **N** | Y | Y | Y (11) | red-exfil, red-exploit, red-infra, red-lateral, red-lead, red-persist, red-privesc, red-recon, red-reporter, red-social, red-vuln |
| 10 | `/saucer-boy` | Y | **N** | Y | Y | Y (1) | sb-voice |
| 11 | `/saucer-boy-framework-voice` | Y | **N** | Y | Y | Y (3) | sb-calibrator, sb-reviewer, sb-rewriter |
| 12 | `/transcript` | Y | Y | Y | Y | Y (5) | ts-extractor, ts-formatter, ts-mindmap-ascii, ts-mindmap-mermaid, ts-parser |
| 13 | `/worktracker` | Y | Y | Y | **implicit** | Y (3) | wt-auditor, wt-verifier, wt-visualizer |

**Totals:** 13 SKILL.md files, 6 in README (46%), 12 in CLAUDE.md (92%), 10 in trigger map (77%), 58 agents in AGENTS.md.

### Skills with No Agent Directory

Three skills have SKILL.md but no `agents/` directory: `/architecture`, `/ast`, `/bootstrap`. These operate as single-agent skills where the main context handles the skill directly.

---

## L2: Full Inventory

### L2.1: README Gaps (by section)

**Skills Table (README lines 107-114):**

| Listed | Missing |
|--------|---------|
| `/problem-solving`, `/worktracker`, `/nasa-se`, `/orchestration`, `/architecture`, `/transcript` | `/adversary`, `/ast`, `/bootstrap`, `/eng-team`, `/red-team`, `/saucer-boy`, `/saucer-boy-framework-voice` |

**Features Section (README line 133-139):**

Current bullets:
- "8 specialized agents (researcher, analyst, architect, validator, synthesizer, reviewer, investigator, reporter)" — **INCORRECT**: 58 agents, only problem-solving agents listed
- "Work Tracking" — accurate
- "Knowledge Accrual" — accurate
- "NASA Systems Engineering" — accurate
- "Multi-Agent Orchestration" — accurate

Missing feature bullets:
- Adversarial quality review (10 strategies, quality scoring)
- Secure software engineering (OWASP, ASVS, SLSA, DevSecOps)
- Offensive security methodology (MITRE ATT&CK, PTES)
- AST-based markdown parsing
- Framework voice quality (Saucer Boy persona)
- Diataxis documentation methodology (exists in plugin but no SKILL.md in repo)

**Documentation Table (README lines 143-148):**

| Listed | Exists but unlisted |
|--------|---------------------|
| docs/INSTALLATION.md | docs/BOOTSTRAP.md |
| CLAUDE.md | docs/CLAUDE-MD-GUIDE.md |
| AGENTS.md | docs/governance/JERRY_CONSTITUTION.md |
| CONTRIBUTING.md | docs/runbooks/getting-started.md |
| | docs/playbooks/problem-solving.md |
| | docs/playbooks/orchestration.md |
| | docs/playbooks/transcript.md |
| | docs/playbooks/PLUGIN-DEVELOPMENT.md |

**Known Limitations (README lines 98-101):**

| # | Limitation | Status |
|---|-----------|--------|
| 1 | "Skill and agent definitions are not yet optimized" | Still valid — definitions are comprehensive but verbose |
| 2 | "Windows portability is in progress" | Still valid — CI tests on Windows but edge cases remain |

No new limitations to add beyond what's documented.

**Example Session (README lines 116-131):**

- Agent name `ps-analyst` is correct for analysis tasks
- Output path `docs/analysis/EN-001-e-001-test-failures.md` uses legacy path convention
- Current convention: `projects/{PROJECT_ID}/analysis/...` or `projects/{PROJECT_ID}/research/...`
- The example flow is otherwise accurate

### L2.2: Cross-Reference Discrepancies

| Source A | Source B | Discrepancy |
|----------|----------|-------------|
| README (6 skills) | CLAUDE.md (12 skills) | 6 skills missing from README |
| CLAUDE.md (12 skills) | SKILL.md files (13) | `/bootstrap` missing from CLAUDE.md |
| Trigger map (10 routes) | SKILL.md files (13) | `/architecture`, `/bootstrap`, `/diataxis` missing from trigger map |
| README ("8 agents") | AGENTS.md (58 agents) | README undercounts by 50 agents |
| AGENTS.md (10 skills with agents) | SKILL.md (13 total) | 3 skills have no agents directory (architecture, ast, bootstrap) |

### L2.3: Documentation File Inventory

**User-facing docs (relevant for README documentation table):**

| File | Purpose | In README? |
|------|---------|------------|
| docs/INSTALLATION.md | Platform-specific installation | Y |
| docs/BOOTSTRAP.md | First-time Jerry setup | N |
| docs/CLAUDE-MD-GUIDE.md | CLAUDE.md authoring guide | N |
| docs/runbooks/getting-started.md | Getting started runbook | N |
| docs/governance/JERRY_CONSTITUTION.md | Framework governance | N |
| docs/playbooks/problem-solving.md | Problem-solving agent guide | N |
| docs/playbooks/orchestration.md | Orchestration workflow guide | N |
| docs/playbooks/transcript.md | Transcript parsing guide | N |
| docs/playbooks/PLUGIN-DEVELOPMENT.md | Plugin development guide | N |
| CONTRIBUTING.md | Contributor guide | Y |
| CLAUDE.md | Claude Code context | Y |
| AGENTS.md | Agent registry | Y |

**Internal/reference docs (not for README table):**

- docs/design/ — ADRs (6 files)
- docs/research/ — Research papers (12+ files)
- docs/knowledge/ — Knowledge base (15+ files)
- docs/archive/ — Historical artifacts (60+ files)
- docs/schemas/ — Schema documentation (2 files)
- docs/scores/ — Quality scores (7 files)
- docs/security/ — Security test cases (1 file)

### L2.4: SKILL.md Frontmatter Structure

All 13 SKILL.md files use YAML frontmatter with these fields:

| Field | Present In | Notes |
|-------|-----------|-------|
| `name` | 13/13 | Skill identifier |
| `description` | 13/13 | 1-3 sentence purpose description |
| `version` | 13/13 | Semantic version string |
| `allowed-tools` | 13/13 | Tool access list |
| `activation-keywords` | 13/13 | Trigger keywords array |
| `agents` | Some | Agent name list (eng-team, red-team have it; not universal) |

This structured frontmatter is the primary input for the Phase B auto-documentation module.
