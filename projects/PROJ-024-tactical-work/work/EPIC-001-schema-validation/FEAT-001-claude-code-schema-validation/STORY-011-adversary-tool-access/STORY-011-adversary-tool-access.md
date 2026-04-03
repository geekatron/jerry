# STORY-011: Adversary Sub-Agents Need WebSearch, WebFetch, and Context7 Tool Access

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Add web research and MCP tool access to adversary agents to prevent factual hallucination
-->

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-27T09:00:00Z
> **Due:**
> **Completed:** 2026-03-29T00:30:00Z
> **Parent:** FEAT-001
> **Owner:** adam.nowak
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | What needs to happen |
| [Problem](#problem) | The hallucination incident |
| [Design Decision](#design-decision) | Direct access vs intermediary pattern |
| [Accepted Risk](#accepted-risk) | Documented risk acceptance |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** Jerry framework user running C4 adversarial tournaments

**I want** adversary agents to have web search and Context7 MCP access

**So that** factual claims in adversarial reviews are verified against live sources instead of relying on potentially stale LLM training data

---

## Summary

The `jerry:adv-executor` agent currently has T2 tools (Read, Write, Edit, Glob, Grep). It cannot verify factual claims via web search or library documentation. During a C4 tournament, the S-007 Constitutional AI strategy hallucinated a $3.4B acquisition figure when the verified amount is $25B.

Add WebSearch, WebFetch, and Context7 MCP **directly to adv-executor** (T2 -> T3). Document the accepted risk. The adv-scorer remains T2 -- its job is to evaluate evidence already assembled by adv-executor, not to source new evidence.

**GitHub Issue:** [geekatron/jerry#217](https://github.com/geekatron/jerry/issues/217)

---

## Problem

During a C4 adversary tournament, the S-007 Constitutional AI agent hallucinated that the PANW/CyberArk acquisition was "$3.4 billion" when the verified figure (via PANW press release) is $25 billion. The agent had no way to web search and verify because it lacked the tool.

Most critical strategies affected:
- **S-011 Chain-of-Verification** -- fact verification is its entire purpose
- **S-007 Constitutional AI** -- intellectual honesty requires verifiable claims
- **S-001 Red Team** -- competitive claims need current data

---

## Design Decision

### Rejected: adv-researcher Intermediary Pattern

The STORY-012 security reviews (eng-security SEC-001, red-vuln V-003) recommended creating a separate `adv-researcher` T3 agent to pre-fetch facts, keeping adv-executor at T2.

**This approach was rejected because:**

1. **It relocates the risk, doesn't eliminate it.** The researcher reads the same deliverable content to know what to look up, gets the same prompt injection exposure, AND has web tools.
2. **It breaks the adversary's ability to follow its own research threads.** A middleman can only fetch what it's told to -- it can't verify things the executor discovers mid-review.
3. **49 other agents already have this exposure.** ps-researcher, eng-security, all red-team agents -- they all read user-provided content AND have WebFetch. Singling out adv-executor is inconsistent.
4. **Prompt-level guardrails ("treat URLs as data") break legitimate use.** If a deliverable references an API doc URL, the adversary SHOULD fetch it to verify claims.

### Accepted: Direct Web Access + Risk Documentation

Grant WebSearch, WebFetch, Context7 directly to adv-executor. Accept the inherent risk that any agent reading untrusted content with web access has prompt injection exposure. This is the same risk profile as ps-researcher, eng-security, and 47 other T3 agents.

### Future Mitigation: Docker + Envoy (Infrastructure-Level)

The proper mitigation for web-enabled agent security is infrastructure-level network control: Docker containerization with Envoy proxy providing domain allowlists, outbound request logging, rate limiting, and internal network isolation. This is deterministic enforcement -- not prompt-level "please don't do bad things." Tracked as a future project initiative.

---

## Accepted Risk

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Prompt injection via deliverable content triggers WebFetch to attacker URL | Low (requires crafted deliverable) | Medium (data exfiltration channel) | Same risk as 49 other T3 agents. Operator awareness. Future: Docker + Envoy network control. |
| Search result poisoning influences quality findings | Low (requires SEO manipulation targeting niche terms) | Medium (false evidence in findings) | S-014 LLM-as-Judge multi-dimensional scoring; orchestrator can cross-verify. |
| Quality gate integrity | Low (requires both injection + score manipulation) | High (false PASS on C4 deliverable) | Three-pass scoring history provides drift detection; human review at C4. |
| Memory-Keeper + web persistence channel (red-vuln F-002, applies to orch agents not adv-executor) | Low (requires prior-session compromise) | Medium (cross-session poisoned data loses provenance) | Citation guardrails added to all orch agents. Future: Docker + Envoy. Formally accepted per STORY-013 wave2-vuln-assessment.md. |

---

## Acceptance Criteria

- [x] `adv-executor.md` frontmatter includes `WebSearch`, `WebFetch` in tools
- [x] `adv-executor.md` frontmatter includes `mcpServers: context7: true`
- [x] `adv-executor.governance.yaml` updated: `tool_tier: T4` (was T3 pre-renumbering; T4=External is correct under Persistent-First Linear model per ADR-STORY015-001)
- [x] `adv-executor.governance.yaml` updated: `capabilities.allowed_tools` reflects new tools
- [x] T4 citation guardrails present in `adv-executor.governance.yaml` `guardrails.output_filtering`
- [x] `skills/adversary/SKILL.md` `allowed-tools` includes `WebSearch`, `WebFetch`, and Context7 MCP tools
- [x] adv-scorer stays T2 (no web access) -- decision documented
- [x] Accepted risk documented in governance YAML
- [x] Schema validation passes — 611 schema tests (`uv run pytest tests/ -k schema`: 611 passed, 3 skipped), 320 architecture tests (`uv run pytest tests/contract/ tests/architecture/`: 320 passed, 2 skipped). Run 2026-03-29. See also STORY-013 TASK-009.
- [x] All existing tests pass — 62 pm-pmm (`uv run pytest tests/integration/test_pm_pmm_security_review.py`: 62 passed). Run 2026-03-29.
- [x] `mcp-tool-standards.md` Agent Integration Matrix updated for adv-executor

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner |
|----|-------|--------|-------|
| TASK-001 | Update adv-executor.md frontmatter (tools + mcpServers) | completed | eng-backend |
| TASK-002 | Update adv-executor.governance.yaml (T2->T3, citation guardrails, accepted risk) | completed | eng-backend |
| TASK-003 | Update adversary SKILL.md allowed-tools | completed | eng-backend |
| TASK-004 | Update mcp-tool-standards.md Agent Integration Matrix for adv-executor | completed | -- |
| TASK-005 | Run jerry agents validate-frontmatter to confirm | completed | -- |
| TASK-006 | Run full test suite to confirm no regressions | completed | claude |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: Claude Code Schema Validation](../FEAT-001-claude-code-schema-validation.md)
- **GitHub Issue:** [geekatron/jerry#217](https://github.com/geekatron/jerry/issues/217)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Informed By | STORY-012 | Audit identified the gap and security considerations |
| Informed By | red-vuln V-003 | Critical finding -- accepted with documented risk |
| Informed By | eng-security SEC-001 | High finding -- intermediary pattern rejected with rationale |
| Blocks | STORY-014 D-002 | mcp-tool-standards.md matrix update for adv-executor depends on this landing |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-27 | adam.nowak | pending | Story created from GitHub issue #217 |
| 2026-03-27 | adam.nowak | pending | Updated: rejected adv-researcher intermediary, direct web access with accepted risk |
| 2026-03-28 | adam.nowak | in_progress | Wave 1: eng-backend implemented (4 files). Wave 2: eng-security + red-vuln + ps-reviewer reviewed. DX-HIGH-1 fixed (body text). SEC-001 fixed (pm-pmm). F-002 formally accepted. mcp-tool-standards matrix updated. |
| 2026-03-28 | adam.nowak | in_progress | Iteration 2: SEC-002/003 citation guardrails, entity statuses, M-003 AC corrected. Score 0.895. |
| 2026-03-28 | adam.nowak | in_progress | Iteration 3: T3 rationale comment, task statuses updated, orch-planner T4+T3 documented. Score 0.942. |
| 2026-03-29 | claude | completed | All 11 ACs verified. AC-3 updated T3→T4 per tier renumbering (ADR-STORY015-001). 611 schema + 320 architecture tests pass. |
