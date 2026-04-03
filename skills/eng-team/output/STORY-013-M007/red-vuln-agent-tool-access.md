# Vulnerability Assessment: Agent Tool Access Control

> **Agent:** red-vuln (Vulnerability Analyst, /red-team)
> **Engagement:** STORY-013-M007 Agent Tool Access Assessment
> **Date:** 2026-03-29
> **Scope:** UX skill agent definitions in the Jerry Framework; sweep of all 89 agent files
> **Authorization:** Internal framework security assessment, authorized by project owner
> **Methodology:** PTES Vulnerability Analysis; OWASP A04 (Insecure Design); trust boundary and attack path analysis
> **Authorization level:** Analysis scope; read-only; no exploitation

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Severity counts, risk posture, key findings |
| [L1: Technical Detail](#l1-technical-detail) | Complete vulnerability inventory with evidence |
| [Finding F-001: Task Alias Enforcement](#f-001-task-alias-enforcement-was-the-original-disallowedtools-a-no-op) | Bypass risk: was disallowedTools: [Task] enforced? |
| [Finding F-002: Incomplete Remediation Scope](#f-002-incomplete-remediation-scope-governance-yaml-still-uses-task) | Governance layer still uses deprecated name |
| [Finding F-003: Widespread disallowedTools Absence](#f-003-widespread-disallowedtools-absence-in-non-ux-worker-agents) | 79 non-UX worker agents lack explicit disallowedTools |
| [Finding F-004: Escalation Paths via Tool Inheritance](#f-004-escalation-paths-tool-inheritance-and-mcp-servers) | Alternative channels for Agent tool access |
| [Finding F-005: Governance Schema Gap](#f-005-governance-schema-gap-no-disallowedtools-mirror-in-governance-yaml) | No machine-readable enforcement at governance layer |
| [Finding F-006: CI Enforcement Gap](#f-006-ci-enforcement-gap-no-check-for-task-in-disallowedtools) | No automated detection of Task vs Agent in disallowedTools |
| [Attack Path Analysis](#attack-path-analysis) | Multi-step exploitation chains |
| [Architectural Design Review (OWASP A04)](#architectural-design-review-owasp-a04) | Trust boundary stress test |
| [Blast Radius Assessment](#blast-radius-assessment) | Impact if original defect was actively exploited |
| [Risk Scoring Summary](#risk-scoring-summary) | CVSS-informed scoring table |
| [L2: Strategic Implications](#l2-strategic-implications) | Attack chains, risk methodology, engagement alignment |

---

## L0: Executive Summary

### Finding Counts by Severity

| Severity | Count |
|----------|-------|
| High     | 1     |
| Medium   | 3     |
| Low      | 2     |
| **Total** | **6** |

### Overall Risk Posture

**Medium** -- The original defect (`disallowedTools: [Task]` instead of `[Agent]` on 10 UX worker agents) has been remediated at the .md frontmatter layer where runtime enforcement occurs. The risk posture is partially mitigated. However, three residual concerns remain:

1. The ux-orchestrator's `governance.yaml` `allowed_tools` list still declares `Task` (not `Agent`), creating a governance-layer inconsistency that could confuse future audits and mislead CI checks that parse governance rather than frontmatter.
2. 79 non-UX worker agents across 13 skills use a `tools:` allowlist approach rather than `disallowedTools:`, meaning they rely on allowlist-not-including-Agent as the enforcement mechanism rather than an explicit deny. This is technically equivalent but structurally weaker -- a single miscategorized allowlist entry would open the door, and there is no CI check that verifies `Agent` is absent from non-orchestrator tools lists.
3. No CI check exists that detects `disallowedTools: [Task]` as a misconfiguration. The original defect persisted through the PROJ-022 Wave 1-5 build cycle and was only caught during STORY-013 manual audit.

The blast radius of the original `Task` defect, had it been exploitable, would have been low-to-medium: Claude Code's JSON schema confirms `Task` is a documented backward-compatible alias for `Agent` (see schema comment in `docs/schemas/claude-code-frontmatter-v1.schema.json`). This means `disallowedTools: [Task]` **was NOT a no-op** -- it was functionally equivalent to `disallowedTools: [Agent]` at runtime. The remediation was therefore correct as policy hygiene, but the original code was not actively vulnerable to recursive delegation.

### Top Exploitable Findings

1. **F-002 (Medium):** ux-orchestrator governance.yaml `allowed_tools` still declares `Task` -- creates governance audit confusion and misleads future schema checks.
2. **F-003 (Medium):** 79 non-UX worker agents have no `disallowedTools` field at all -- enforcement relies solely on tool allowlist not including `Agent`. No CI verification.
3. **F-006 (Medium):** No CI check exists to detect `Task` vs `Agent` naming in `disallowedTools` fields.

### Key Recommendations

1. Update `ux-orchestrator.governance.yaml` `allowed_tools` to use `Agent` instead of `Task` (F-002, Medium).
2. Add a CI check that (a) verifies all non-T5 agents lack `Agent` in their `tools` frontmatter field, and (b) warns if `Task` appears in `disallowedTools` (F-006, Medium).
3. Consider adding an explicit `disallowedTools: [Agent]` to all non-T5 worker agents across all skills for defense-in-depth, supplementing the allowlist-based approach (F-003, Medium).

---

## L1: Technical Detail

### Evidence Collection

| Evidence Source | Description |
|----------------|-------------|
| `git show 12b5148a -- skills/ux-ai-first-design/agents/ux-ai-design-guide.md` | Confirmed original UX worker agents created with `disallowedTools: [Task]` |
| `docs/schemas/claude-code-frontmatter-v1.schema.json` | Schema comment: "The subagent spawning tool was renamed from 'Task' to 'Agent' in v2.1.63. Both names work as aliases." |
| `agent-development-standards.md` H-35 | Explicitly states: "Worker agents (invoked via Agent tool) MUST NOT include `Agent` (or its backward-compatible alias `Task`) in the official `tools` frontmatter field." |
| All 10 UX worker `.md` frontmatter | Confirmed `disallowedTools: [Agent]` post-fix |
| `ux-orchestrator.governance.yaml` `allowed_tools` | Still contains `Task` (not `Agent`) |
| All non-UX worker `.md` frontmatter | None have `disallowedTools` field; use explicit `tools:` allowlist |
| `scripts/validate-agent-frontmatter.py` | No check for `Task` vs `Agent` in `disallowedTools`; no check for `Agent` absence in non-T5 tools lists |

---

## F-001: Task Alias Enforcement -- Was the Original disallowedTools a No-Op?

**Severity:** Low (mitigated -- finding is informational)
**Affected agents:** All 10 original UX worker agents (pre-fix)
**Current status:** REMEDIATED in .md frontmatter
**ATT&CK Technique:** Not applicable (framework-internal governance)
**CWE:** CWE-284 (Improper Access Control -- governance layer)

### Assessment

The original defect was `disallowedTools: [Task]` on all 10 UX worker agents created in PROJ-022. The question is whether `Task` was honored as a valid tool name by Claude Code, or whether it was silently ignored (making the field a no-op).

**Finding: The original disallowedTools was NOT a no-op.**

Evidence from the framework's own JSON schema (`docs/schemas/claude-code-frontmatter-v1.schema.json`, `tools` field description comment):

> "The subagent spawning tool was renamed from 'Task' to 'Agent' in v2.1.63. Both names work as aliases. Hook payloads use 'Agent' as tool_name (#29677)."

This confirms that Claude Code recognizes `Task` as a backward-compatible alias for `Agent`. Therefore:
- `disallowedTools: [Task]` was enforced identically to `disallowedTools: [Agent]` at runtime
- The 10 UX worker agents were correctly blocking recursive delegation during their entire operational lifetime
- The remediation to `disallowedTools: [Agent]` is correct policy hygiene (using the canonical current name) but did not change the security posture

### Residual Risk

The schema note that "Hook payloads use 'Agent' as tool_name" suggests `Task` may behave differently in hooks or log-based audit trails. Any audit tooling parsing hook stop events would see `Agent` in the payload regardless of which name was declared. This is an observability gap, not a security gap.

---

## F-002: Incomplete Remediation Scope -- governance.yaml Still Uses Task

**Severity:** Medium
**Affected agents:** ux-orchestrator
**File:** `skills/user-experience/agents/ux-orchestrator.governance.yaml`
**Current status:** OPEN
**Evidence:**

```yaml
capabilities:
  allowed_tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task          # <-- deprecated name, should be Agent
  - WebSearch
  - WebFetch
  ...
forbidden_actions:
  - "P-003 VIOLATION: NEVER delegate Task tool access to sub-skill agents..."
  - "P-003: No Recursive Subagents (Hard) - Only orchestrator has Task; sub-skills are workers"
```

The .md frontmatter for ux-orchestrator correctly declares `Agent` in `tools:`. The governance.yaml `allowed_tools` list is NOT the runtime enforcement layer -- it is a governance metadata mirror. However, using `Task` here creates three distinct problems:

1. **Audit confusion:** Future auditors reading governance.yaml would see `Task` and assume the orchestrator is using the deprecated tool name, potentially flagging a false-positive defect.
2. **CI risk:** If a future CI check validates that governance.yaml `allowed_tools` matches frontmatter `tools`, the mismatch would produce a false-positive error (`Task` in governance, `Agent` in frontmatter).
3. **Governance-security inconsistency:** The `forbidden_actions` also use `Task` ("NEVER delegate Task tool access to sub-skill agents"), meaning the prohibition text names a deprecated tool. If a worker agent were somehow granted `Agent` (current name), the forbidden action text would not syntactically match.

Additionally, the same `Task` name appears in `forbidden_actions` text strings across 13 agents in problem-solving, nasa-se, diataxis, transcript, use-case, test-spec, contract-design, and worktracker skills. These are in free-text prohibition statements, not machine-parsed fields, so they do not affect runtime enforcement -- but they create documentation debt and may confuse future maintainers.

**Remediation:** Update `ux-orchestrator.governance.yaml` `allowed_tools: [Task]` to `allowed_tools: [Agent]`. Update `forbidden_actions` text strings to reference `Agent` tool. This is a low-effort, high-clarity fix.

---

## F-003: Widespread disallowedTools Absence in Non-UX Worker Agents

**Severity:** Medium
**Affected agents:** 79 non-UX worker agents across 13 skills (adversary, contract-design, diataxis, eng-team, nasa-se, orchestration, pm-pmm, problem-solving, prompt-engineering, red-team, saucer-boy, test-spec, transcript, use-case, worktracker)
**Current status:** OPEN (by design -- but unverified by CI)

### Analysis

The 10 UX worker agents use `disallowedTools: [Agent]` as the enforcement mechanism (explicit deny). The 79 non-UX worker agents use an explicit `tools:` allowlist that does not include `Agent` (implicit deny by omission). Both approaches are valid per Claude Code's permission model -- `disallowedTools` applies a denylist on top of inherited tools; `tools:` applies an allowlist that supersedes inheritance.

The defense-in-depth difference is significant:

| Mechanism | Failure Mode | Detectability |
|-----------|-------------|---------------|
| Explicit `disallowedTools: [Agent]` | `Agent` must be explicitly added AND the deny must be removed | Two-step failure; denylist removal is auditable |
| Allowlist without `Agent` | Single step: `Agent` accidentally added to `tools:` | One-step failure; not separately auditable |

For the 79 non-UX workers, there is currently no CI check that verifies `Agent` is absent from their `tools:` list. If a maintainer accidentally added `Agent` to a worker agent's `tools:` list during a tools expansion (e.g., upgrading from T2 to T4), no automated gate would catch the P-003 violation before commit.

Evidence: The STORY-013 manual audit discovered that the UX workers used the wrong name. A similar audit of all 79 non-UX workers has not been performed in this engagement. The allowlist-only approach relies on human discipline for T5 designation to remain exclusive.

**Note on scope overlap:** This finding is partially mitigated by H-35 (`agent-development-standards.md`), which states that non-T5 worker agents MUST NOT include `Agent` in `tools` frontmatter. H-35 is in the L2-REINJECT enforcement tier (per `agent-development-standards.md` Two-Tier Enforcement Model table), meaning it is re-injected at every prompt. However, L2 enforcement is "immune to context rot" but depends on LLM instruction-following -- it is not a deterministic gate.

---

## F-004: Escalation Paths -- Tool Inheritance and MCP Servers

**Severity:** Low
**Affected agents:** All worker agents that have `mcpServers` declared
**Current status:** Informational

### Analysis

**Path 1: Tool inheritance from parent session.** Claude Code's permission model uses inheritance: "Subagents invoked via the Task tool inherit the parent conversation's permission context." (`docs/explanation/permission-security-model.md`). This means `disallowedTools: [Agent]` on a worker agent blocks the worker from spawning further sub-agents. However, if the parent session has broad permissions including `Agent`, a worker agent that somehow gains `Agent` access would be able to spawn subagents because the parent session's permission context is inherited. The `disallowedTools` deny is an additive restriction on the inherited set, so `disallowedTools: [Agent]` still blocks the tool even when the parent has it. The inheritance path does not represent an escalation path beyond what is currently declared.

**Path 2: MCP server tool-granting.** MCP servers listed in `mcpServers` can expose tools. None of the current MCP servers (context7, memory-keeper) expose an Agent-equivalent tool -- context7 exposes `resolve-library-id` and `query-docs`; memory-keeper exposes `context_save`, `context_get`, `context_search`. No current MCP server bypasses the P-003 constraint. However, if a future MCP server were added (e.g., a workflow automation MCP that exposes a `spawn_agent` tool), it would not be covered by `disallowedTools: [Agent]`. MCP tools are named `mcp__<server>__<tool>` and would need their own explicit denials.

**Path 3: Bash escalation.** The `disallowedTools` comment in the schema notes: "KNOWN LIMITATION: Restriction is name-based not capability-based -- agents with Bash access can bypass Write/Edit restrictions via shell commands (#31292)." Worker agents with Bash access could potentially invoke `claude` CLI or other tooling to spawn subagents outside the framework's tool model. This is a platform-level limitation documented by Anthropic and cannot be mitigated by `disallowedTools` alone.

---

## F-005: Governance Schema Gap -- No disallowedTools Mirror in governance.yaml

**Severity:** Low
**Affected agents:** All 10 UX worker agents (and all workers with disallowedTools)
**Current status:** Open (architectural gap)

### Analysis

The dual-file architecture (H-34) splits agent definitions into:
- `.md` frontmatter: Claude Code runtime fields (including `disallowedTools`)
- `.governance.yaml`: Machine-readable governance metadata validated by `agent-governance-v1.schema.json`

The `governance.yaml` schema (`docs/schemas/agent-governance-v1.schema.json`) does not have a `capabilities.disallowed_tools` field that mirrors the frontmatter `disallowedTools`. The only governance-layer tool tracking is `capabilities.allowed_tools` (which mirrors `tools:` from frontmatter).

This creates a gap: the `disallowedTools` declaration exists only in `.md` frontmatter. An auditor examining only governance.yaml cannot determine whether a worker agent has explicit deny constraints. The L5 CI gate (`validate-agent-frontmatter.py`) validates the frontmatter structure but does not cross-check it against governance.yaml.

As evidence, ux-orchestrator's governance.yaml uses `Task` in `allowed_tools` while its frontmatter correctly uses `Agent` -- and this inconsistency was not caught by any automated gate. The absence of a `disallowed_tools` field in the governance schema is one reason this cross-check is not performed.

---

## F-006: CI Enforcement Gap -- No Check for Task in disallowedTools

**Severity:** Medium
**Affected layers:** L5 CI (validate-agent-frontmatter.py, check_agent_conformance.py)
**Current status:** Open

### Analysis

The frontmatter validator (`scripts/validate-agent-frontmatter.py`) validates that `disallowedTools` is a valid field (present in `AGENT_FIELDS` set), that it is a string or array, and that the YAML parses correctly. It does NOT:

1. Check whether `Task` appears in `disallowedTools` (a deprecated alias that should be replaced with `Agent`)
2. Check whether `Agent` appears in `disallowedTools` for non-T5 workers (verifying the P-003 constraint is enforced)
3. Check whether `Agent` is absent from non-T5 worker `tools:` lists (verifying allowlist-based enforcement works)
4. Cross-validate `disallowedTools` in frontmatter against `allowed_tools` in governance.yaml

The STORY-013 defect (all 10 UX workers using `Task` in `disallowedTools`) persisted through the entire PROJ-022 Wave 1-5 build cycle. Six distinct commits added UX worker agents and none of the automated gates caught the deprecated name. The defect was only discovered during a manual audit in STORY-013.

The `agent-development-standards.md` H-35 verification column states: "L5 (CI): Grep for P-003/P-020/P-022 presence." This is implemented as a governance.yaml `constitution.principles_applied` check. It does NOT verify that `disallowedTools` contains `Agent` (the behavioral enforcement mechanism).

**Missing CI check (recommended):**

```python
# In validate-agent-frontmatter.py, validate_agent() function:
disallowed = fm.get("disallowedTools")
if isinstance(disallowed, str):
    disallowed = [t.strip() for t in disallowed.split(",")]
if isinstance(disallowed, list):
    if "Task" in disallowed:
        warnings.append(
            "  disallowedTools: contains deprecated 'Task' -- "
            "rename to 'Agent' (canonical name since v2.1.63)"
        )
```

---

## Attack Path Analysis

### AP-001: Worker Agent Recursive Delegation (Pre-Fix)

**Status:** MITIGATED by fix
**Precondition:** `disallowedTools: [Task]` was the enforcement mechanism AND `Task` was not recognized as a valid tool alias

**Attack chain:**
1. User or adversary invokes ux-orchestrator with a crafted request
2. ux-orchestrator delegates to a UX worker agent (expected behavior)
3. Worker agent, with `disallowedTools: [Task]` acting as a no-op, spawns a sub-agent
4. Sub-agent executes with worker agent's tool permissions (Read, Write, WebSearch, WebFetch, Context7)
5. Sub-agent writes artifacts to project filesystem, potentially exfiltrating context or modifying governance files

**Assessment:** This chain did NOT work in practice. The JSON schema documents that `Task` is recognized as a backward-compatible alias for `Agent`, meaning `disallowedTools: [Task]` was enforced. The attack path was blocked by the alias resolution even before the fix.

### AP-002: Future Governance Confusion Leading to Misconfiguration

**Status:** OPEN (residual risk from F-002, F-006)
**Precondition:** A future maintainer reads `ux-orchestrator.governance.yaml` and concludes the orchestrator uses the deprecated `Task` tool; separately, a different maintainer adds `Task` (or `Agent`) to a worker agent's `disallowedTools` in the wrong way

**Attack chain:**
1. ux-orchestrator.governance.yaml `allowed_tools: [Task]` creates the impression that `Task` is the current tool name
2. Future maintainer adding a new UX worker agent uses `disallowedTools: [Task]` (mimicking the governance.yaml pattern)
3. Depending on whether the alias remains active in future Claude Code versions, this may or may not enforce the block
4. No CI check catches this because the current validator does not flag `Task` in `disallowedTools`

**ATT&CK Technique:** T1562.001 (Impair Defenses: Disable or Modify Tools) -- analogy

### AP-003: Allowlist-Based Enforcement Single-Point Failure

**Status:** OPEN (F-003)
**Precondition:** 79 non-UX worker agents rely on `tools:` allowlist (without `Agent`) as the sole P-003 enforcement

**Attack chain:**
1. Maintainer expands a worker agent's tool tier (e.g., T2 to T4)
2. During tools list update, `Agent` is accidentally included (copy-paste from ux-orchestrator, template error)
3. Worker agent now has Agent tool access, violating P-003
4. No CI check catches the violation
5. Worker agent spawns subagents in production, violating the single-level nesting constraint

**Likelihood:** Low (requires human error). **Impact:** Medium (P-003 violation, recursive delegation, uncontrolled token consumption).

---

## Architectural Design Review (OWASP A04)

### Trust Boundary Stress Test

**Trust boundary:** Worker agent boundary (enforced by `disallowedTools: [Agent]` or allowlist omission)

**Violation scenarios:**

1. **Alias confusion attack:** If Anthropic renames `Agent` to a third name in a future version, both `Task` and `Agent` references in `disallowedTools` could become stale simultaneously. There is no version-pinned enforcement -- the denylist is name-based, not capability-based.

2. **MCP tool wrapping:** A future MCP server could expose a tool named `mcp__workflow__spawn_agent` that effectively spawns subagents. `disallowedTools: [Agent]` would not block it. The trust boundary relies on the narrow definition of "Agent tool" without addressing capability-equivalent alternatives.

3. **Trust inheritance inversion:** Claude Code's permission inheritance means a worker agent that gains Agent access can spawn sub-workers that further inherit the worker's tool set (not the parent orchestrator's tool set). This creates a potential privilege ceiling -- recursive delegates would have at most the worker's permissions, not the orchestrator's. This limits but does not eliminate the blast radius of a P-003 violation.

### Business Logic Flaw Analysis

**Flaw: Defense-in-depth asymmetry.** The UX skill uses `disallowedTools` (explicit deny). All other skills use `tools:` allowlist (implicit deny by omission). This creates two enforcement patterns that must both be maintained correctly. An auditor checking "does this agent satisfy P-003?" must apply different checks depending on the skill. A CI check that verifies P-003 compliance must handle both patterns. This dual-pattern design increases maintenance burden and audit complexity.

**Flaw: Governance.yaml as documentation, not enforcement.** The governance layer (`forbidden_actions` text) says "NEVER use the Task tool" but uses deprecated naming. If the behavioral enforcement fails (e.g., because `disallowedTools` is misconfigured), the governance-layer text does not provide a fallback enforcement mechanism -- it is documentation read by an LLM, not a deterministic gate.

---

## Blast Radius Assessment

**Scenario: What if `disallowedTools: [Task]` had been a genuine no-op (alias not recognized)?**

Had `Task` not been recognized as a valid tool name in `disallowedTools`, each of the 10 UX worker agents would have had unrestricted access to the Agent tool (inherited from the session context, not blocked by the no-op denylist). The blast radius would have been:

| Dimension | Assessment |
|-----------|------------|
| Agents affected | 10 UX workers: ux-ai-design-guide, ux-atomic-architect, ux-behavior-diagnostician, ux-sprint-facilitator, ux-heart-analyst, ux-heuristic-evaluator, ux-inclusive-evaluator, ux-jtbd-analyst, ux-kano-analyst, ux-lean-ux-facilitator |
| Max delegation depth | 2 hops (worker -> sub-worker); deeper requires T5 designation which sub-workers would not have |
| Tool access at sub-worker | Inherited from worker: Read, Write, Edit, Glob, Grep, Bash (T2); some T3 agents also WebSearch, WebFetch, Context7 |
| Data at risk | Project filesystem writes (arbitrary artifact creation); for T3 workers, WebSearch/WebFetch-sourced content; no Memory-Keeper (not granted to UX workers) |
| P-003 violation | Yes -- single-level nesting constraint violated |
| External impact | Low -- no external systems accessible; MCP servers limited to context7 and memory-keeper; no outbound connections beyond web search |
| Exploitability | Low -- requires a crafted prompt that causes the worker agent to decide to spawn a sub-agent AND the worker agent's system prompt does not include the "Tools NOT available: Task tool" behavioral instruction |

Note: All 10 UX worker agents include the text "Tools NOT available: Task tool -- this is a worker agent (P-003)." in their `<capabilities>` section. This behavioral L2 constraint would deter most exploitation scenarios even without the `disallowedTools` enforcement.

**Conclusion:** Even in the worst-case scenario where `Task` was a no-op, the blast radius was limited by (a) behavioral instructions in agent bodies, (b) sub-workers inheriting only worker-level permissions (not orchestrator-level), and (c) the absence of Memory-Keeper or filesystem-write escalation paths that would persist the compromise.

---

## Risk Scoring Summary

| Finding | Severity | CVSS v3.1 (est.) | Exploitability | Impact | Status |
|---------|----------|-----------------|----------------|--------|--------|
| F-001: Task alias enforcement | Low | 2.1 (AV:L/AC:H/PR:H/UI:N/S:U/C:N/I:L/A:N) | Very Low -- alias IS enforced | Informational | Mitigated |
| F-002: governance.yaml uses Task | Medium | 4.3 (AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N) | Low -- documentation/audit confusion | Governance inconsistency | Open |
| F-003: No disallowedTools on 79 workers | Medium | 4.2 (AV:L/AC:H/PR:H/UI:N/S:U/C:L/I:L/A:N) | Low -- requires human error in tools list | P-003 violation potential | Open (by design) |
| F-004: Tool inheritance escalation paths | Low | 3.1 (AV:L/AC:H/PR:H/UI:N/S:U/C:L/I:N/A:N) | Very Low -- no current MCP bypass | Informational | Open (platform limitation) |
| F-005: No disallowedTools in governance schema | Low | 2.0 (AV:L/AC:H/PR:H/UI:N/S:U/C:N/I:N/A:N) | Very Low -- schema gap only | Audit traceability gap | Open (architectural) |
| F-006: No CI check for Task in disallowedTools | Medium | 5.3 (AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N) | Medium -- CI gaps enable silent regression | Regression vulnerability | Open |

---

## L2: Strategic Implications

### Attack Chain Priority

The highest-value remediation targets are F-006 (CI enforcement gap) and F-002 (governance.yaml stale naming). Together they address the systemic failure that allowed the original defect to persist undetected:

1. **F-006 (CI gap):** The original `disallowedTools: [Task]` defect survived PROJ-022 Waves 1-5 because no automated check flagged it. Adding a CI check for deprecated `Task` naming and for `Agent` absence from non-T5 tools lists would prevent regression. Estimated effort: 1 developer-hour in `validate-agent-frontmatter.py`.

2. **F-002 (governance stale naming):** ux-orchestrator governance.yaml `allowed_tools: [Task]` is a single-line fix but has downstream ripple effects on future audits and CI cross-validation. Estimated effort: 30 minutes.

3. **F-003 (defense-in-depth):** Adding `disallowedTools: [Agent]` to all 79 non-UX worker agents is a defense-in-depth improvement. It converts implicit-deny-by-omission to explicit-deny, making P-003 enforcement auditable and CI-checkable uniformly. Estimated effort: medium -- 79 file edits, but mechanical. Could be scripted.

### Risk Scoring Methodology

Scores use CVSS v3.1 base metric approximation. Environmental modifier: internal framework with no external network exposure reduces impact scores. Temporal modifier: published Anthropic documentation on `Task` alias reduces exploitability (the defect was less severe than initially scoped).

### Engagement Objective Alignment

This assessment directly addressed the five scoped dimensions:

1. **Bypass risk (F-001):** `disallowedTools: [Task]` was NOT a no-op. Claude Code honors `Task` as a backward-compatible alias. Risk: Low/Mitigated.
2. **Completeness (F-002, F-003):** No other agent files have `Task` in `disallowedTools`. However, ux-orchestrator governance.yaml has `Task` in `allowed_tools`, and 79 non-UX workers have no `disallowedTools` at all.
3. **Escalation paths (F-004):** No current MCP server enables Agent-equivalent escalation. Bash-to-CLI is a platform-level limitation acknowledged by Anthropic.
4. **Governance gap (F-005):** `agent-governance-v1.schema.json` has no `disallowedTools` mirror field; the governance audit trail for deny-based enforcement is incomplete.
5. **Impact assessment (Blast Radius section):** 10 agents affected; limited blast radius even in the worst case due to behavioral constraints and permission ceiling at sub-worker level.

### Recommendations for eng-team Hardening

| Priority | Recommendation | Effort | Finding |
|----------|---------------|--------|---------|
| P1 | Add CI check: warn if `Task` in `disallowedTools`, error if `Agent` in non-T5 `tools:` list | 1h | F-006 | **STORY-022** |
| P1 | Update ux-orchestrator.governance.yaml: `Task` -> `Agent` in `allowed_tools` and `forbidden_actions` text | 30min | F-002 | **REMEDIATED** |
| P2 | Consider adding `disallowedTools: [Agent]` to all non-T5 worker agents for defense-in-depth | Medium | F-003 | **STORY-021** |
| P2 | Add `disallowed_tools` mirror field to `agent-governance-v1.schema.json` | 1h | F-005 |
| P3 | Document Bash escalation limitation in security model docs; note it is platform-level | 30min | F-004 |

---

*Agent: red-vuln (Vulnerability Analyst, /red-team)*
*Engagement: STORY-013-M007*
*Constitutional Compliance: P-001 (evidence-based), P-002 (persisted), P-003 (no subagents), P-020 (user authority), P-022 (no deception)*
*Output: Level L0/L1/L2 per agent output spec*
*Date: 2026-03-29*
