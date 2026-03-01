# PROJ-012 Regression Analysis: Governance Migration

**Date:** 2026-02-26
**Branch:** `feat/proj-012-agent-optimization` vs `main`
**Analyst:** Claude Code (3 parallel analysis agents)
**Scope:** All 58 composed agent `.md` files in `skills/*/agents/`
**Criticality:** C3 (touches `.context/rules/`, modifies >10 files)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Overall verdict |
| [Analysis 1: Frontmatter Integrity](#analysis-1-frontmatter-integrity) | YAML frontmatter field preservation |
| [Analysis 2: Prompt Body Content](#analysis-2-prompt-body-content) | Body content preservation and changes |
| [Analysis 3: Governance Data Migration](#analysis-3-governance-data-migration) | Data completeness from .governance.yaml to .md body |
| [Findings Requiring Attention](#findings-requiring-attention) | Regressions and warnings |
| [Consolidated Verdict](#consolidated-verdict) | Final pass/fail matrix |

---

## Executive Summary

**Overall Verdict: CONDITIONAL PASS**

PROJ-012 successfully migrated from a dual-file architecture (`.md` + `.governance.yaml`) to a single-file architecture (`.md` with governance in prompt body). The migration is data-complete with zero governance data loss across all 58 agents.

Two pre-existing changes from earlier commits on this branch were flagged:
- **F-002 (Regression):** `wt-auditor` Phase 2.5 content quality methodology (WTI-008) was removed in a prior commit (`5d8ef86f`)
- **F-003 (Warning):** `llm-tell-patterns.md` reference load triggers removed from 4 saucer-boy agents in a prior commit

Neither F-002 nor F-003 was introduced by the governance migration work. Both originate from the branch's first commit (`5d8ef86f feat(PROJ-012): Rebuild agent optimization on PROJ-010 architecture`).

| Dimension | Verdict |
|-----------|---------|
| Frontmatter integrity | PASS |
| Governance data migration | PASS |
| Prompt body preservation (44/58 agents) | PASS |
| CLI example updates (10 agents) | PASS (intentional) |
| wt-auditor Phase 2.5 deletion | FAIL (pre-existing, not from governance migration) |
| saucer-boy reference pruning | WARN (pre-existing, not from governance migration) |

---

## Analysis 1: Frontmatter Integrity

**Verdict: PASS**

All 58 agents checked. Zero regressions.

### Field Preservation

| Field | Main | HEAD | Status |
|-------|------|------|--------|
| `name` | 58 | 58 | PASS |
| `description` | 58 | 58 | PASS |
| `model` | 58 | 58 | PASS |
| `tools` | 58 | 58 | PASS |
| `mcpServers` | 34 | 34 | PASS |
| `permissionMode` | 0 | 58 | NEW (official field, explicit default) |
| `background` | 0 | 58 | NEW (official field, explicit default) |

### Key Findings

- All field values are byte-for-byte identical between branches
- Two official Claude Code fields (`permissionMode: default`, `background: false`) were made explicit — previously implicit defaults
- Zero governance fields leaked into frontmatter
- All 34 `mcpServers` declarations preserved (including `ps-architect` with dual `context7` + `memory-keeper`)

---

## Analysis 2: Prompt Body Content

**Verdict: CONDITIONAL PASS**

### Change Categories

| Category | Count | Nature | Status |
|----------|-------|--------|--------|
| A: Frontmatter-only (body identical) | 44 | No body changes | PASS |
| B: CLI examples updated | 10 | `jerry ast` CLI → Python API (`ast_ops`); `CLAUDE_PLUGIN_ROOT` → `JERRY_PLUGIN_ROOT` | PASS (intentional) |
| C: llm-tell-patterns.md refs removed | 4 | Conditional load triggers removed from sb-* agents | WARN |
| D: Phase 2.5 deleted | 1 | wt-auditor WTI-008 content quality methodology removed | FAIL |

### Integrity Checks

| Check | Result |
|-------|--------|
| XML tag integrity (all 14 body-changed agents) | PASS — zero structural tags removed |
| Section ordering | PASS — no sections reordered |
| Duplicate sections introduced | PASS — none introduced; 8 pre-existing confirmed |
| Governance injection into composed output | PASS — all 58 agents have governance data |

---

## Analysis 3: Governance Data Migration

**Verdict: PASS**

22 agents deep-analyzed, all 58 exhaustively scanned.

### Field-by-Field Migration Results (58 agents)

| Field | Pass | Fail | Coverage |
|-------|------|------|----------|
| version present | 58 | 0 | 100% |
| version matches governance.yaml | 58 | 0 | 100% |
| tool_tier present | 58 | 0 | 100% |
| tool_tier matches governance.yaml | 58 | 0 | 100% |
| enforcement (when gov had it) | 25/25 | 0 | 100% |
| session_context (when gov had it) | 27/27 | 0 | 100% |
| portability (net-new, all agents) | 58 | 0 | 100% |

### Format Encoding

| Format | Count | Governance Encoding |
|--------|-------|---------------------|
| markdown (`body_format: markdown`) | 43 | `## Agent Version` headings |
| xml (`body_format: xml`) | 15 | `<agent_version>` XML tags |

Both formats carry identical data values. The `PromptTransformer` correctly maps headings to XML tags for xml-format agents.

### Fields NOT Migrated (by design)

`identity`, `persona`, `guardrails`, `capabilities.forbidden_actions`, `constitution`, `output`, `validation` — all already present as prose in existing prompt body sections. The pipeline only injects fields that add NEW information not already in the body.

---

## Findings Requiring Attention

### F-002: wt-auditor Phase 2.5 Content Quality Methodology Deleted

| Attribute | Detail |
|-----------|--------|
| **Severity** | Regression |
| **Agent** | `skills/worktracker/agents/wt-auditor.md` |
| **Origin** | Commit `5d8ef86f` (first branch commit, pre-governance migration) |
| **Impact** | WTI-008 AC quality checks (DoD detection, hedge words, AC bullet count, summary length, scope overflow) removed |
| **Gap** | `skills/worktracker/rules/worktracker-behavior-rules.md` still defines WTI-008 but wt-auditor no longer enforces it |
| **Action** | Determine if intentional. If yes, update WTI rules. If not, restore Phase 2.5 from main. |

### F-003: llm-tell-patterns.md Reference Removal

| Attribute | Detail |
|-----------|--------|
| **Severity** | Warning |
| **Agents** | sb-calibrator, sb-reviewer, sb-rewriter, sb-voice |
| **Origin** | Commit `5d8ef86f` (first branch commit, pre-governance migration) |
| **Impact** | Explicit conditional load triggers removed; file still exists |
| **Action** | Low priority. Agents can still reference the file but lose specific trigger guidance. |

### F-004/F-005: CLI API Updates (Informational)

10 agents updated from `uv run jerry ast` CLI to Python API imports (`skills.ast.scripts.ast_ops`). 3 worktracker agents updated `CLAUDE_PLUGIN_ROOT` → `JERRY_PLUGIN_ROOT`. Both intentional per PROJ-012 scope.

---

## Consolidated Verdict

| Check | Result | Evidence |
|-------|--------|----------|
| Frontmatter field preservation | PASS | 58/58 agents, all 5 field types identical |
| Frontmatter governance leakage | PASS | Zero non-official fields in frontmatter |
| Governance version migration | PASS | 58/58 exact match |
| Governance tool_tier migration | PASS | 58/58 exact match |
| Governance enforcement migration | PASS | 25/25 where applicable |
| Governance session_context migration | PASS | 27/27 where applicable |
| Portability injection (net-new) | PASS | 58/58 present |
| Body content preservation | PASS | 44/58 byte-identical; 14 with intentional changes |
| XML tag integrity | PASS | Zero structural tags removed |
| No duplicate sections introduced | PASS | 8 pre-existing, 0 new |
| wt-auditor Phase 2.5 | **FAIL** | Pre-existing from commit `5d8ef86f` |
| sb-* llm-tell-patterns.md | **WARN** | Pre-existing from commit `5d8ef86f` |

**The governance migration itself (`.governance.yaml` deletion + prompt body injection) introduced ZERO regressions.** The two flagged items (F-002, F-003) originate from the branch's initial architecture rebuild commit, not from the governance migration work.

---

## Methodology

Three parallel analysis agents executed:
1. **Frontmatter Agent** — Extracted and compared YAML frontmatter from all 58 agents using `git show main:path` vs HEAD
2. **Body Content Agent** — Compared prompt body content, checked XML tags, section ordering, duplicates across all 58 agents
3. **Governance Migration Agent** — Verified field-by-field data completeness from `.governance.yaml` to `.md` body across 22 deep-analyzed + 58 exhaustively scanned agents

All three agents wrote individual reports to `/tmp/regression-analysis-{dimension}.md`. This consolidated report synthesizes their findings.

---

*Generated: 2026-02-26*
*Analysis Agents: 3 parallel (sonnet model)*
*Total agents analyzed: 58 (exhaustive)*
