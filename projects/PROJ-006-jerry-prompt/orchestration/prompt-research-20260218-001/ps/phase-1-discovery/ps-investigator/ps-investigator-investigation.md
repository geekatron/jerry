# PS-Investigator: Jerry Internals Investigation

> **Agent:** ps-investigator
> **PS ID:** prompt-research-20260218-001
> **Entry ID:** phase-1-discovery
> **Date:** 2026-02-18
> **Severity:** MEDIUM (investigation of architecture, not a failure)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Investigation Scope](#investigation-scope) | What was investigated and why |
| [Findings Summary](#findings-summary) | Key patterns discovered |
| [Evidence References](#evidence-references) | Full report location |
| [State Output](#state-output) | Agent handoff schema |

---

## Investigation Scope

This investigation analyzed Jerry's internal prompt architecture to identify structural patterns that make its prompts effective. The investigation covered:

- `c:/AI/jerry/CLAUDE.md` - Root context file
- `c:/AI/jerry/skills/problem-solving/SKILL.md` - Problem-solving skill definition
- `c:/AI/jerry/skills/orchestration/SKILL.md` - Orchestration skill definition
- `c:/AI/jerry/skills/nasa-se/SKILL.md` - NASA SE skill definition
- `c:/AI/jerry/skills/problem-solving/agents/ps-investigator.md` - Agent spec
- `c:/AI/jerry/skills/problem-solving/agents/ps-researcher.md` - Agent spec
- `c:/AI/jerry/skills/problem-solving/agents/ps-critic.md` - Agent spec
- `c:/AI/jerry/skills/orchestration/agents/orch-planner.md` - Agent spec
- `c:/AI/jerry/skills/shared/AGENT_TEMPLATE_CORE.md` - Federated template core
- `c:/AI/jerry/projects/PROJ-001-oss-release/orchestration/en001-bugfix-20260210-001/ORCHESTRATION_PLAN.md` - Real example
- `c:/AI/jerry/skills/orchestration/PLAYBOOK.md` - Orchestration playbook
- `.claude/rules/` - All rule files

---

## Findings Summary

8 distinct prompt patterns were identified in Jerry's internals:

| # | Pattern | Key Mechanism |
|---|---------|---------------|
| P-01 | YAML Frontmatter Intent Header | `activation-keywords` list, `model` selection, `allowed-tools` allowlist |
| P-02 | XML Section Identity Segmentation | `<identity>`, `<persona>`, `<capabilities>`, `<guardrails>` tags |
| P-03 | Triple-Lens Output Framework | L0 (ELI5), L1 (Engineer), L2 (Architect) mandatory output levels |
| P-04 | Constitutional Self-Verification | Checkbox pre-response checklist + principle-behavior table with enforcement tiers |
| P-05 | Mandatory Persistence Protocol | Named protocol + numbered steps + prohibition - stated three ways |
| P-06 | State Schema as API Contract | Typed YAML output schema for inter-agent communication |
| P-07 | Adversarial Critique Loop | Create-Critique-Revise-Validate with circuit breaker (max 3 iterations, 0.85 threshold) |
| P-08 | Navigation Table with Anchors | HARD requirement: anchor-linked section tables for targeted reading |

**Root architecture insight:** Jerry solves context rot (LLM performance degradation as context fills) by treating the filesystem as infinite memory. The CLAUDE.md root is intentionally sparse. Full context is loaded selectively on demand.

**Key design principle:** Every quality requirement is expressed as a number (quality_score 0.0-1.0), not a verbal description. This enables programmatic evaluation by ps-critic.

---

## Evidence References

Full investigation report persisted to:
`c:/AI/jerry/projects/PROJ-006-jerry-prompt/research/jerry-internals-investigation.md`

The report contains:
- L0: Executive summary (2 paragraphs, accessible)
- L1: 8 detailed findings with specific file/line evidence
- L2: Structural deep dive (5-layer architecture, federated template system)
- Pattern catalog (table)
- User prompt anatomy analysis
- Anti-pattern catalog
- Evidence chain (14 entries)

---

## State Output

```yaml
investigator_output:
  ps_id: "prompt-research-20260218-001"
  entry_id: "phase-1-discovery"
  artifact_path: "c:/AI/jerry/projects/PROJ-006-jerry-prompt/research/jerry-internals-investigation.md"
  severity: "MEDIUM"
  root_cause: "Jerry uses structured XML sections, YAML frontmatter, Triple-Lens output, constitutional checklists, and filesystem-as-memory to achieve context-rot-resistant multi-agent prompting"
  confidence: "high"
  patterns_identified: 8
  next_agent_hint: "ps-synthesizer for pattern synthesis across investigation findings"
```

---

*Agent Version: ps-investigator (Jerry framework)*
*Created: 2026-02-18*
*Constitutional Compliance: P-001, P-002, P-003, P-004, P-022*
