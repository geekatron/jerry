# Claude Code Frontmatter Validation Report

> Generated: 2026-03-27 11:03:50
> Schema (agents): `docs/schemas/claude-code-frontmatter-v1.schema.json`
> Schema (skills): `docs/schemas/claude-code-skill-frontmatter-v1.schema.json`

## L0 Executive Summary

| Metric | Value |
|--------|-------|
| Total files scanned | 119 |
| Agent files | 89 |
| Skill files | 30 |
| **PASS** (clean) | **90** |
| **PASS** (with warnings) | **29** |
| **FAIL** (validation errors) | **0** |
| No frontmatter | 0 |
| Parse errors | 0 |

| Type | Pass | Fail |
|------|------|------|
| Agents | 89 | 0 |
| Skills | 30 | 0 |

**Overall assessment: PASS**

## L1 Technical Detail

### Per-File Failures

No failures detected.

### Files Passing With Warnings

#### `skills/adversary/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'version']

#### `skills/architecture/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'version']

#### `skills/ast/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'version']

#### `skills/bootstrap/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'version']

#### `skills/contract-design/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'version']

#### `skills/diataxis/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'version']

#### `skills/eng-team/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'agents', 'version']
- `allowed-tools`: mcp_tools_in_allowed_tools
  - MCP tools may not be grantable via allowed-tools: ['mcp__context7__resolve-library-id', 'mcp__context7__query-docs']

#### `skills/nasa-se/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'version']
- `allowed-tools`: mcp_tools_in_allowed_tools
  - MCP tools may not be grantable via allowed-tools: ['mcp__context7__resolve-library-id', 'mcp__context7__query-docs', 'mcp__memory-keeper__context_save', 'mcp__memory-keeper__context_get', 'mcp__memory-keeper__context_search']

#### `skills/orchestration/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'version']
- `allowed-tools`: mcp_tools_in_allowed_tools
  - MCP tools may not be grantable via allowed-tools: ['mcp__memory-keeper__context_save', 'mcp__memory-keeper__context_get', 'mcp__memory-keeper__context_search']

#### `skills/pm-pmm/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'version']

#### `skills/problem-solving/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'version']
- `allowed-tools`: mcp_tools_in_allowed_tools
  - MCP tools may not be grantable via allowed-tools: ['mcp__context7__resolve-library-id', 'mcp__context7__query-docs', 'mcp__memory-keeper__context_save', 'mcp__memory-keeper__context_get', 'mcp__memory-keeper__context_search']

#### `skills/prompt-engineering/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'version']

#### `skills/red-team/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'version']
- `allowed-tools`: mcp_tools_in_allowed_tools
  - MCP tools may not be grantable via allowed-tools: ['mcp__context7__resolve-library-id', 'mcp__context7__query-docs']

#### `skills/saucer-boy-framework-voice/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'version']

#### `skills/saucer-boy/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'version']

#### `skills/test-spec/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'version']

#### `skills/transcript/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'context_injection', 'version']
- `allowed-tools`: mcp_tools_in_allowed_tools
  - MCP tools may not be grantable via allowed-tools: ['mcp__memory-keeper__context_save', 'mcp__memory-keeper__context_get']

#### `skills/use-case/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'version']

#### `skills/user-experience/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'agents', 'version']
- `allowed-tools`: mcp_tools_in_allowed_tools
  - MCP tools may not be grantable via allowed-tools: ['mcp__context7__resolve-library-id', 'mcp__context7__query-docs', 'mcp__memory-keeper__context_save', 'mcp__memory-keeper__context_get', 'mcp__memory-keeper__context_search']

#### `skills/ux-ai-first-design/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'agents', 'version']
- `allowed-tools`: mcp_tools_in_allowed_tools
  - MCP tools may not be grantable via allowed-tools: ['mcp__context7__resolve-library-id', 'mcp__context7__query-docs']

#### `skills/ux-atomic-design/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'agents', 'version']
- `allowed-tools`: mcp_tools_in_allowed_tools
  - MCP tools may not be grantable via allowed-tools: ['mcp__context7__resolve-library-id', 'mcp__context7__query-docs']

#### `skills/ux-behavior-design/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'agents', 'version']

#### `skills/ux-design-sprint/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'agents', 'version']
- `allowed-tools`: mcp_tools_in_allowed_tools
  - MCP tools may not be grantable via allowed-tools: ['mcp__context7__resolve-library-id', 'mcp__context7__query-docs']

#### `skills/ux-heart-metrics/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'version']

#### `skills/ux-heuristic-eval/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'agents', 'version']
- `allowed-tools`: mcp_tools_in_allowed_tools
  - MCP tools may not be grantable via allowed-tools: ['mcp__context7__resolve-library-id', 'mcp__context7__query-docs']

#### `skills/ux-inclusive-design/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'agents', 'version']
- `allowed-tools`: mcp_tools_in_allowed_tools
  - MCP tools may not be grantable via allowed-tools: ['mcp__context7__resolve-library-id', 'mcp__context7__query-docs']

#### `skills/ux-kano-model/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'agents', 'version']

#### `skills/ux-lean-ux/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'agents', 'version']
- `allowed-tools`: mcp_tools_in_allowed_tools
  - MCP tools may not be grantable via allowed-tools: ['mcp__context7__resolve-library-id', 'mcp__context7__query-docs']

#### `skills/worktracker/SKILL.md`

- `(root)`: unrecognized_fields
  - Jerry-specific fields not recognized by Claude Code: ['activation-keywords', 'version']

### All Files (Full Inventory)

**Agents:**

| File | Status |
|------|--------|
| `skills/adversary/agents/adv-executor.md` | PASS |
| `skills/adversary/agents/adv-scorer.md` | PASS |
| `skills/adversary/agents/adv-selector.md` | PASS |
| `skills/contract-design/agents/cd-generator.md` | PASS |
| `skills/contract-design/agents/cd-validator.md` | PASS |
| `skills/diataxis/agents/diataxis-auditor.md` | PASS |
| `skills/diataxis/agents/diataxis-classifier.md` | PASS |
| `skills/diataxis/agents/diataxis-explanation.md` | PASS |
| `skills/diataxis/agents/diataxis-howto.md` | PASS |
| `skills/diataxis/agents/diataxis-reference.md` | PASS |
| `skills/diataxis/agents/diataxis-tutorial.md` | PASS |
| `skills/eng-team/agents/eng-architect.md` | PASS |
| `skills/eng-team/agents/eng-backend.md` | PASS |
| `skills/eng-team/agents/eng-devsecops.md` | PASS |
| `skills/eng-team/agents/eng-frontend.md` | PASS |
| `skills/eng-team/agents/eng-incident.md` | PASS |
| `skills/eng-team/agents/eng-infra.md` | PASS |
| `skills/eng-team/agents/eng-lead.md` | PASS |
| `skills/eng-team/agents/eng-qa.md` | PASS |
| `skills/eng-team/agents/eng-reviewer.md` | PASS |
| `skills/eng-team/agents/eng-security.md` | PASS |
| `skills/nasa-se/agents/nse-architecture.md` | PASS |
| `skills/nasa-se/agents/nse-configuration.md` | PASS |
| `skills/nasa-se/agents/nse-explorer.md` | PASS |
| `skills/nasa-se/agents/nse-integration.md` | PASS |
| `skills/nasa-se/agents/nse-qa.md` | PASS |
| `skills/nasa-se/agents/nse-reporter.md` | PASS |
| `skills/nasa-se/agents/nse-requirements.md` | PASS |
| `skills/nasa-se/agents/nse-reviewer.md` | PASS |
| `skills/nasa-se/agents/nse-risk.md` | PASS |
| `skills/nasa-se/agents/nse-verification.md` | PASS |
| `skills/orchestration/agents/orch-planner.md` | PASS |
| `skills/orchestration/agents/orch-synthesizer.md` | PASS |
| `skills/orchestration/agents/orch-tracker.md` | PASS |
| `skills/pm-pmm/agents/pm-business-analyst.md` | PASS |
| `skills/pm-pmm/agents/pm-competitive-analyst.md` | PASS |
| `skills/pm-pmm/agents/pm-customer-insight.md` | PASS |
| `skills/pm-pmm/agents/pm-market-strategist.md` | PASS |
| `skills/pm-pmm/agents/pm-product-strategist.md` | PASS |
| `skills/problem-solving/agents/ps-analyst.md` | PASS |
| `skills/problem-solving/agents/ps-architect.md` | PASS |
| `skills/problem-solving/agents/ps-critic.md` | PASS |
| `skills/problem-solving/agents/ps-investigator.md` | PASS |
| `skills/problem-solving/agents/ps-reporter.md` | PASS |
| `skills/problem-solving/agents/ps-researcher.md` | PASS |
| `skills/problem-solving/agents/ps-reviewer.md` | PASS |
| `skills/problem-solving/agents/ps-synthesizer.md` | PASS |
| `skills/problem-solving/agents/ps-validator.md` | PASS |
| `skills/prompt-engineering/agents/pe-builder.md` | PASS |
| `skills/prompt-engineering/agents/pe-constraint-gen.md` | PASS |
| `skills/prompt-engineering/agents/pe-scorer.md` | PASS |
| `skills/red-team/agents/red-exfil.md` | PASS |
| `skills/red-team/agents/red-exploit.md` | PASS |
| `skills/red-team/agents/red-infra.md` | PASS |
| `skills/red-team/agents/red-lateral.md` | PASS |
| `skills/red-team/agents/red-lead.md` | PASS |
| `skills/red-team/agents/red-persist.md` | PASS |
| `skills/red-team/agents/red-privesc.md` | PASS |
| `skills/red-team/agents/red-recon.md` | PASS |
| `skills/red-team/agents/red-reporter.md` | PASS |
| `skills/red-team/agents/red-social.md` | PASS |
| `skills/red-team/agents/red-vuln.md` | PASS |
| `skills/saucer-boy-framework-voice/agents/sb-calibrator.md` | PASS |
| `skills/saucer-boy-framework-voice/agents/sb-reviewer.md` | PASS |
| `skills/saucer-boy-framework-voice/agents/sb-rewriter.md` | PASS |
| `skills/saucer-boy/agents/sb-voice.md` | PASS |
| `skills/test-spec/agents/tspec-analyst.md` | PASS |
| `skills/test-spec/agents/tspec-generator.md` | PASS |
| `skills/transcript/agents/ts-extractor.md` | PASS |
| `skills/transcript/agents/ts-formatter.md` | PASS |
| `skills/transcript/agents/ts-mindmap-ascii.md` | PASS |
| `skills/transcript/agents/ts-mindmap-mermaid.md` | PASS |
| `skills/transcript/agents/ts-parser.md` | PASS |
| `skills/use-case/agents/uc-author.md` | PASS |
| `skills/use-case/agents/uc-slicer.md` | PASS |
| `skills/user-experience/agents/ux-orchestrator.md` | PASS |
| `skills/ux-ai-first-design/agents/ux-ai-design-guide.md` | PASS |
| `skills/ux-atomic-design/agents/ux-atomic-architect.md` | PASS |
| `skills/ux-behavior-design/agents/ux-behavior-diagnostician.md` | PASS |
| `skills/ux-design-sprint/agents/ux-sprint-facilitator.md` | PASS |
| `skills/ux-heart-metrics/agents/ux-heart-analyst.md` | PASS |
| `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.md` | PASS |
| `skills/ux-inclusive-design/agents/ux-inclusive-evaluator.md` | PASS |
| `skills/ux-jtbd/agents/ux-jtbd-analyst.md` | PASS |
| `skills/ux-kano-model/agents/ux-kano-analyst.md` | PASS |
| `skills/ux-lean-ux/agents/ux-lean-ux-facilitator.md` | PASS |
| `skills/worktracker/agents/wt-auditor.md` | PASS |
| `skills/worktracker/agents/wt-verifier.md` | PASS |
| `skills/worktracker/agents/wt-visualizer.md` | PASS |

**Skills:**

| File | Status |
|------|--------|
| `skills/adversary/SKILL.md` | PASS (warn) |
| `skills/architecture/SKILL.md` | PASS (warn) |
| `skills/ast/SKILL.md` | PASS (warn) |
| `skills/bootstrap/SKILL.md` | PASS (warn) |
| `skills/contract-design/SKILL.md` | PASS (warn) |
| `skills/diataxis/SKILL.md` | PASS (warn) |
| `skills/eng-team/SKILL.md` | PASS (warn) |
| `skills/nasa-se/SKILL.md` | PASS (warn) |
| `skills/orchestration/SKILL.md` | PASS (warn) |
| `skills/pm-pmm/SKILL.md` | PASS (warn) |
| `skills/problem-solving/SKILL.md` | PASS (warn) |
| `skills/prompt-engineering/SKILL.md` | PASS (warn) |
| `skills/red-team/SKILL.md` | PASS (warn) |
| `skills/saucer-boy-framework-voice/SKILL.md` | PASS (warn) |
| `skills/saucer-boy/SKILL.md` | PASS (warn) |
| `skills/test-spec/SKILL.md` | PASS (warn) |
| `skills/transcript/SKILL.md` | PASS (warn) |
| `skills/use-case/SKILL.md` | PASS (warn) |
| `skills/user-experience/SKILL.md` | PASS (warn) |
| `skills/ux-ai-first-design/SKILL.md` | PASS (warn) |
| `skills/ux-atomic-design/SKILL.md` | PASS (warn) |
| `skills/ux-behavior-design/SKILL.md` | PASS (warn) |
| `skills/ux-design-sprint/SKILL.md` | PASS (warn) |
| `skills/ux-heart-metrics/SKILL.md` | PASS (warn) |
| `skills/ux-heuristic-eval/SKILL.md` | PASS (warn) |
| `skills/ux-inclusive-design/SKILL.md` | PASS (warn) |
| `skills/ux-jtbd/SKILL.md` | PASS |
| `skills/ux-kano-model/SKILL.md` | PASS (warn) |
| `skills/ux-lean-ux/SKILL.md` | PASS (warn) |
| `skills/worktracker/SKILL.md` | PASS (warn) |

## L2 Strategic Implications

All files pass schema validation. The frontmatter corpus is schema-conformant.

**29 files pass with warnings.** The most common warning is `unrecognized_fields` -- Jerry-specific fields (`version`, `activation-keywords`, `agents`, etc.) are silently ignored by Claude Code but are valid Jerry governance metadata. No action required unless cleaning up frontmatter for portability.

**Warning policy:** The `unrecognized_fields` warning is expected and non-actionable. Jerry governance metadata (`version`, `activation-keywords`, `agents`, `allowed-tools` in SKILL.md) intentionally extends beyond Claude Code's official field set. These fields are silently ignored by Claude Code at runtime. No migration required.
