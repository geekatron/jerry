# STRIDE Threat Model: Claude Code Schema Validation Pipeline

> **Agent:** eng-architect | **Date:** 2026-03-26 | **Criticality:** C3 (Significant)
> **Confidence:** 0.85 -- Validated against Anthropic documentation and published CVE data. Runtime behavior assertions marked where direct verification was not possible.
> **NIST CSF 2.0 Functions:** Identify (ID.RA), Protect (PR.DS, PR.AC), Detect (DE.CM)
> **SSDF Practices:** PO.1 (security requirements), PO.5 (secure development environments)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Business risk overview and key decisions |
| [L1: Threat Model](#l1-threat-model) | Complete STRIDE analysis with DREAD scoring |
| [L2: Strategic Implications](#l2-strategic-implications) | Long-term architectural posture and trade-offs |
| [System Context](#system-context) | System boundaries, actors, data flows |
| [Trust Boundary Analysis](#trust-boundary-analysis) | Where trust transitions occur |
| [Data Flow Diagram](#data-flow-diagram) | Data flows across trust boundaries |
| [STRIDE Threat Matrix](#stride-threat-matrix) | Threats by category and trust boundary |
| [Per-Field Attack Surface Analysis](#per-field-attack-surface-analysis) | Every frontmatter field with injection vectors |
| [DREAD Risk Scoring](#dread-risk-scoring) | Quantified risk per threat |
| [Mitigations](#mitigations) | Schema-level and runtime mitigations |
| [Schema-Unsecurable Fields](#schema-unsecurable-fields) | Fields requiring runtime-only controls |
| [Threat Intelligence](#threat-intelligence) | Published CVEs and known attack patterns |
| [References](#references) | Sources with URLs |

---

## L0: Executive Summary

This threat model analyzes the pipeline where YAML frontmatter in agent and skill definition files is validated by JSON schemas, then parsed by Claude Code and injected into the LLM system prompt. The analysis identifies **23 distinct threats** across three trust boundaries.

**Key findings:**

1. **The `description` field is the highest-risk attack surface.** It is injected verbatim into the LLM system prompt with no sanitization. Prompt injection via this field cannot be prevented at the schema level -- JSON Schema has no mechanism to detect adversarial natural language. This is a **Critical** severity finding requiring runtime mitigation.

2. **The `hooks` field enables arbitrary code execution by design.** Hooks execute shell commands at lifecycle events. A malicious hook definition in a cloned repository executes automatically when a developer opens Claude Code. This is the attack vector exploited by CVE-2025-59536. Schema validation cannot prevent this -- hooks are designed to run arbitrary commands.

3. **The `mcpServers` field with inline definitions can connect to attacker-controlled servers.** When `additionalProperties: true` is combined with object-type inline server definitions, the schema imposes no constraint on which servers are configured. Schema-level mitigations are limited to allowlisting known server names.

4. **The `permissionMode` field is an enum with `bypassPermissions` as a valid value.** While the schema correctly constrains this to the documented enum, the enum itself includes a value that disables all user confirmation prompts. Schema validation confirms the value is "valid" while the security posture is degraded.

5. **`additionalProperties: true` on both schemas creates an unbounded injection surface.** Any field name with any value passes validation. This is the deliberate design choice (Claude Code silently ignores unknown fields), but it means the schema cannot catch smuggled metadata or experimental field probing.

**Recommendation:** Treat schema validation as a **correctness gate**, not a security boundary. Six of the eight identified attack surfaces require runtime controls that operate after Claude Code parses the frontmatter but before the content reaches the LLM or shell execution.

---

## L1: Threat Model

### System Context

**System under analysis:** The pipeline from agent/skill definition authoring through schema validation to Claude Code runtime loading and LLM prompt injection.

**Actors:**

| Actor | Trust Level | Description |
|-------|-------------|-------------|
| Framework maintainer | High | Writes agent/skill definitions within the Jerry repository |
| External contributor | Low | Submits PRs with new or modified agent/skill definitions |
| Claude Code runtime | Medium | Parses YAML frontmatter, enforces tool restrictions, injects system prompt |
| LLM (Claude) | Medium | Receives injected system prompt, executes instructions |
| CI/CD pipeline | High | Runs schema validation on PRs before merge |
| MCP servers | Variable | External processes providing tools; trust depends on server identity |

**Assets at risk:**

| Asset | Classification | Impact if Compromised |
|-------|---------------|----------------------|
| LLM system prompt integrity | Confidentiality + Integrity | Prompt injection leads to unauthorized behavior |
| Tool restriction enforcement | Integrity + Availability | Bypass leads to unauthorized tool access |
| User permission model | Integrity | Escalation leads to unconfirmed destructive operations |
| Developer workstation | Confidentiality + Integrity | RCE via hooks or MCP leads to full system compromise |
| API credentials | Confidentiality | Exfiltration via MCP redirection (CVE-2026-21852 pattern) |
| Agent memory stores | Confidentiality + Integrity | Cross-agent memory access leaks sensitive context |

---

### Trust Boundary Analysis

Three trust boundaries are identified where data crosses between zones of different trust levels.

**TB-1: Filesystem to YAML Parser**

```
[Agent/Skill .md files]  ---->  [Claude Code YAML Parser]
      (filesystem)                  (runtime process)

Trust transition: Untrusted file content -> Trusted runtime parsing
Threat surface: Malformed YAML, YAML bombs, injection payloads in field values
```

- **Entry point:** `.claude/agents/*.md`, `skills/*/SKILL.md` files
- **Trust assumption:** File content is well-formed YAML with valid field values
- **Violation condition:** Attacker controls file content (malicious PR, compromised dependency, cloned repository)

**TB-2: Schema Validation to Runtime Acceptance**

```
[Jerry CI Schema Validation]  ---->  [Agent/Skill Acceptance]  ---->  [Claude Code Runtime Loading]
     (JSON Schema check)                  (merge gate)                    (system prompt injection)

Trust transition: Validated-but-not-sanitized content -> Runtime execution context
Threat surface: Fields that pass schema validation but carry adversarial payloads
```

- **Entry point:** CI validation script output (pass/fail)
- **Trust assumption:** Schema-valid files are safe for runtime consumption
- **Violation condition:** Payload passes schema constraints but exploits runtime behavior

**TB-3: External Contributors to Merged Definitions**

```
[External Contributor PR]  ---->  [Schema Validation + Code Review]  ---->  [Merged Definition]
     (untrusted input)                    (validation gate)                      (trusted repository)

Trust transition: Untrusted external input -> Trusted repository content
Threat surface: Social engineering, subtle payloads in valid-looking definitions
```

- **Entry point:** GitHub Pull Request
- **Trust assumption:** Schema validation + human review catches all malicious content
- **Violation condition:** Malicious payload is syntactically valid and escapes human review

---

### Data Flow Diagram

```
                                   TB-3
                                    |
                                    v
+-------------------+     +-------------------+     +--------------------+
| External          |---->| Schema Validation |---->| Merged Definition  |
| Contributor PR    |     | (CI Pipeline)     |     | (Repository)       |
+-------------------+     +-------------------+     +--------------------+
                                                            |
                           TB-1                             |
                            |                               v
                            v                    +--------------------+
                  +-------------------+          | Claude Code YAML   |
                  | Agent/Skill .md   |--------->| Parser             |
                  | Files (Filesystem)|          +--------------------+
                  +-------------------+                     |
                                                           TB-2
                                                            |
                                    +----------+------------+----------+
                                    |          |            |          |
                                    v          v            v          v
                            +---------+  +---------+  +--------+  +--------+
                            | System  |  | Tool    |  | Hook   |  | MCP    |
                            | Prompt  |  | Config  |  | Exec   |  | Server |
                            | (LLM)   |  | (perms) |  | (shell)|  | (net)  |
                            +---------+  +---------+  +--------+  +--------+
```

---

### STRIDE Threat Matrix

#### Spoofing (S)

| ID | Trust Boundary | Threat | Severity | DREAD |
|----|---------------|--------|----------|-------|
| S-01 | TB-3 | **Agent identity spoofing.** External contributor creates an agent definition with a `name` that collides with or shadows an existing trusted agent. Claude Code resolves agents by name; a duplicate name in a higher-priority location could shadow the legitimate agent. | Medium | 24 |
| S-02 | TB-1 | **Skill impersonation via name field.** A malicious SKILL.md uses a `name` matching an existing skill, causing Claude to load the malicious version when the legitimate skill is invoked via `/name`. | Medium | 24 |
| S-03 | TB-2 | **MCP server identity spoofing.** An `mcpServers` inline definition uses a name matching a trusted server (e.g., `context7`) but points to a different command or endpoint. Claude Code connects to the spoofed server believing it is the trusted one. | High | 30 |

#### Tampering (T)

| ID | Trust Boundary | Threat | Severity | DREAD |
|----|---------------|--------|----------|-------|
| T-01 | TB-1 | **Description field prompt injection.** The `description` field is injected verbatim into the LLM system prompt. An adversarial description can override agent behavioral constraints, instruct the LLM to ignore safety guardrails, or redirect agent behavior. | Critical | 36 |
| T-02 | TB-1 | **initialPrompt command injection.** The `initialPrompt` field is auto-submitted as the first user turn. It processes `/skill-name` commands and skill content. A malicious initialPrompt can invoke arbitrary skills and submit crafted prompts as if the user typed them. | High | 32 |
| T-03 | TB-2 | **tools field type coercion.** The `tools` field accepts both string and array types. A crafted string value (e.g., comma-separated with embedded special syntax like `Agent(*)`) could expand tool access beyond intent. | Medium | 22 |
| T-04 | TB-1 | **Hooks arbitrary code execution.** The `hooks` field defines shell commands executed at lifecycle events. A malicious hook executes arbitrary commands on the developer's workstation. This is the exact vector of CVE-2025-59536. | Critical | 40 |
| T-05 | TB-3 | **additionalProperties payload smuggling.** With `additionalProperties: true`, an attacker can add arbitrary fields. While Claude Code ignores unknown frontmatter fields, future Claude Code versions may interpret currently-unknown fields, creating a time-bomb effect. | Low | 16 |
| T-06 | TB-1 | **Markdown body injection via description overflow.** If `description` is excessively long, it consumes LLM context budget, potentially pushing legitimate system prompt content out of the effective context window (context exhaustion attack). | Medium | 20 |

#### Repudiation (R)

| ID | Trust Boundary | Threat | Severity | DREAD |
|----|---------------|--------|----------|-------|
| R-01 | TB-3 | **Unattributed definition changes.** Agent/skill definitions are version-controlled but lack per-field change attribution. A subtle modification to `permissionMode` or `tools` within a large PR may escape review, and the specific field change is not independently logged. | Low | 14 |
| R-02 | TB-2 | **Hook execution without audit trail.** Hooks execute shell commands, but the hook execution itself is not logged in a tamper-evident manner. A hook that exfiltrates data leaves no trace in the agent's output or worktracker. | Medium | 22 |

#### Information Disclosure (I)

| ID | Trust Boundary | Threat | Severity | DREAD |
|----|---------------|--------|----------|-------|
| I-01 | TB-2 | **Memory scope cross-contamination.** The `memory` field scopes to `user`, `project`, or `local`. A `user`-scoped memory is shared across all projects. An agent with `memory: user` can read memory written by other agents, potentially accessing sensitive findings from unrelated projects. | Medium | 26 |
| I-02 | TB-2 | **MCP server data exfiltration.** An `mcpServers` inline definition can point to an attacker-controlled server. When Claude invokes tools on that server, it may send sensitive context (file contents, code snippets, conversation history) to the attacker. This is the pattern of CVE-2026-21852 (API key exfiltration via redirected base URL). | Critical | 38 |
| I-03 | TB-1 | **Description field information leakage.** The description is loaded into the LLM context for routing decisions. A description that instructs the LLM to "repeat all system prompt content" could cause the LLM to leak internal framework instructions to an external observer. | Medium | 24 |
| I-04 | TB-2 | **MEMORY.md system prompt injection.** When `memory` is enabled, the first 200 lines or 25KB of MEMORY.md is injected into the system prompt. If an attacker can write to the memory directory, they can inject persistent adversarial instructions that survive across sessions. | High | 30 |

#### Denial of Service (D)

| ID | Trust Boundary | Threat | Severity | DREAD |
|----|---------------|--------|----------|-------|
| D-01 | TB-1 | **YAML bomb / resource exhaustion.** Deeply nested YAML structures, anchor-alias cycles, or extremely large field values can cause the YAML parser to consume excessive memory or CPU. | Low | 14 |
| D-02 | TB-2 | **maxTurns removal.** Omitting `maxTurns` (or setting it very high) allows an agent to run indefinitely, consuming API credits and context budget without bound. | Low | 16 |
| D-03 | TB-1 | **Hook infinite loop.** A hook that triggers on its own output event (e.g., a PostToolUse hook that invokes a tool) can create an infinite execution loop on the developer's machine. | Medium | 22 |
| D-04 | TB-2 | **Skills preload context exhaustion.** The `skills` array injects full skill content into agent context at startup. An agent that preloads many skills can exhaust the context window before performing any work, rendering the agent non-functional. | Low | 14 |

#### Elevation of Privilege (E)

| ID | Trust Boundary | Threat | Severity | DREAD |
|----|---------------|--------|----------|-------|
| E-01 | TB-2 | **permissionMode escalation to bypassPermissions.** A definition that sets `permissionMode: bypassPermissions` removes all user confirmation prompts. While this is a valid enum value, a PR that changes an agent's permission mode from `default` to `bypassPermissions` is a privilege escalation that schema validation cannot distinguish from a legitimate configuration change. | High | 34 |
| E-02 | TB-2 | **Tool allowlist expansion.** Omitting the `tools` field causes the agent to inherit ALL tools from the parent, including MCP tools. A malicious definition that removes an existing `tools` restriction (deletion of the field) silently grants maximum tool access. | High | 30 |
| E-03 | TB-2 | **disallowedTools removal.** Removing the `disallowedTools` field from a definition that previously restricted certain tools silently re-enables those tools. This is a privilege escalation via field deletion, which schema validation cannot detect (missing optional fields are valid). | Medium | 26 |
| E-04 | TB-1 | **background: true permission bypass.** Setting `background: true` causes the agent to auto-deny permission prompts not pre-approved. Combined with `permissionMode: dontAsk`, this creates a fully autonomous agent that never prompts the user. | High | 30 |

---

### Per-Field Attack Surface Analysis

#### Agent Frontmatter Fields (claude-code-frontmatter-v1.schema.json)

| # | Field | Schema-Securable | Attack Vector | Severity | Schema Mitigation |
|---|-------|-----------------|---------------|----------|-------------------|
| 1 | `name` | Partial | Name collision/shadowing (S-01) | Medium | Pattern constraint `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` prevents special characters. Add `maxLength`. Cannot prevent collisions at schema level. |
| 2 | `description` | **No** | Prompt injection (T-01), context exhaustion (T-06), info leakage (I-03) | **Critical** | `maxLength` limits context exhaustion. Cannot detect adversarial natural language. |
| 3 | `model` | Partial | No direct attack vector. Misuse: selecting a weaker model to degrade safety. | Low | Enum constraint limits valid values. |
| 4 | `tools` | Partial | Tool allowlist expansion (E-02), type coercion (T-03) | High | Validate string items against known tool names (enum). Cannot prevent omission attack. |
| 5 | `disallowedTools` | Partial | Tool restriction removal (E-03) | Medium | Cannot prevent field deletion (optional field). |
| 6 | `mcpServers` | **No** | Server spoofing (S-03), data exfiltration (I-02) | **Critical** | Allowlist known server names as enum. Cannot constrain inline definitions. |
| 7 | `permissionMode` | Partial | Permission escalation (E-01) | High | Enum constraint validates values. Cannot prevent `bypassPermissions` selection. |
| 8 | `maxTurns` | Yes | Resource exhaustion via omission (D-02) | Low | Add `maximum` constraint. Set `default` in schema documentation. |
| 9 | `skills` | Partial | Context exhaustion (D-04) | Low | Add `maxItems` constraint. |
| 10 | `hooks` | **No** | Arbitrary code execution (T-04), infinite loops (D-03), no audit trail (R-02) | **Critical** | `additionalProperties: true` makes this unsecurable at schema level. Hooks are designed to run commands. |
| 11 | `memory` | Partial | Cross-contamination (I-01), persistent injection (I-04) | Medium | Enum constraint limits scope values. Cannot prevent cross-agent reads within scope. |
| 12 | `background` | Partial | Permission bypass combo (E-04) | High | Boolean -- value is inherently constrained. Risk is in combination with permissionMode. |
| 13 | `effort` | Yes | No significant attack vector. | Low | Enum constraint sufficient. |
| 14 | `isolation` | Yes | No significant attack vector. Worktree provides isolation. | Low | Enum constraint sufficient. |
| 15 | `initialPrompt` | **No** | Command injection (T-02) | High | `maxLength` limits scope. Cannot detect adversarial commands. |
| 16 | `color` | Yes | No attack vector. UI-only. | None | String constraint sufficient. |

#### Skill Frontmatter Fields (claude-code-skill-frontmatter-v1.schema.json)

| # | Field | Schema-Securable | Attack Vector | Severity | Additional Notes |
|---|-------|-----------------|---------------|----------|-----------------|
| 1 | `name` | Partial | Skill impersonation (S-02) | Medium | Same as agent `name`. `maxLength: 64` already present. |
| 2 | `description` | **No** | Prompt injection (T-01 variant) | **Critical** | Skill descriptions are loaded into LLM context for auto-invocation decisions. |
| 3 | `allowed-tools` | Partial | Permission grant expansion | Medium | This grants blanket approval -- does not restrict. |
| 4 | `hooks` | **No** | Same as agent hooks (T-04) | **Critical** | Skills support all 24+ hook events. `once: true` is skills-only and limits repeat execution. |
| 5 | `context` | Yes | `fork` value is safe (isolation). | Low | Enum constraint sufficient. |
| 6 | `agent` | Partial | Could reference malicious custom agent | Medium | Validate against known agent names. |
| 7 | `paths` | Partial | Glob patterns could be overly broad | Low | No path traversal risk at schema level; Claude Code handles glob resolution. |
| 8 | `shell` | Partial | `powershell` selection on non-Windows | Low | Enum constraint sufficient. |
| 9 | `mode` | Yes | No attack vector. UI categorization. | None | Boolean constraint sufficient. |
| 10 | `metadata` | Partial | Arbitrary key-value pairs | Low | `additionalProperties: { "type": "string" }` prevents non-string values. |

---

### DREAD Risk Scoring

Scoring scale per dimension: 1 (Low) -- 5 (Critical). Composite = sum of five dimensions (max 50, but practical maximum ~42 given the domain).

| Threat ID | Damage | Reproducibility | Exploitability | Affected Users | Discoverability | Total | Severity |
|-----------|--------|-----------------|----------------|----------------|-----------------|-------|----------|
| **T-04** (Hooks RCE) | 10 | 8 | 8 | 8 | 6 | **40** | Critical |
| **I-02** (MCP exfiltration) | 9 | 8 | 7 | 7 | 7 | **38** | Critical |
| **T-01** (Description injection) | 8 | 8 | 7 | 7 | 6 | **36** | Critical |
| **E-01** (permissionMode escalation) | 8 | 8 | 6 | 6 | 6 | **34** | High |
| **T-02** (initialPrompt injection) | 7 | 7 | 6 | 6 | 6 | **32** | High |
| **S-03** (MCP server spoofing) | 7 | 6 | 6 | 6 | 5 | **30** | High |
| **E-02** (Tool allowlist expansion) | 7 | 7 | 5 | 6 | 5 | **30** | High |
| **I-04** (MEMORY.md injection) | 7 | 6 | 6 | 5 | 6 | **30** | High |
| **E-04** (background + perm bypass) | 7 | 6 | 5 | 6 | 6 | **30** | High |
| **I-01** (Memory cross-contamination) | 5 | 6 | 5 | 5 | 5 | **26** | Medium |
| **E-03** (disallowedTools removal) | 5 | 6 | 5 | 5 | 5 | **26** | Medium |
| **S-01** (Agent name collision) | 5 | 5 | 5 | 5 | 4 | **24** | Medium |
| **S-02** (Skill impersonation) | 5 | 5 | 5 | 5 | 4 | **24** | Medium |
| **I-03** (Description info leakage) | 5 | 5 | 5 | 5 | 4 | **24** | Medium |
| **T-03** (tools type coercion) | 4 | 5 | 4 | 5 | 4 | **22** | Medium |
| **R-02** (Hook audit gap) | 4 | 5 | 4 | 5 | 4 | **22** | Medium |
| **D-03** (Hook infinite loop) | 5 | 5 | 4 | 4 | 4 | **22** | Medium |
| **T-06** (Description context exhaust) | 4 | 5 | 4 | 4 | 3 | **20** | Medium |
| **T-05** (additionalProperties smuggle) | 3 | 4 | 3 | 3 | 3 | **16** | Low |
| **D-02** (maxTurns removal) | 3 | 4 | 3 | 3 | 3 | **16** | Low |
| **R-01** (Unattributed changes) | 3 | 3 | 3 | 3 | 2 | **14** | Low |
| **D-01** (YAML bomb) | 3 | 3 | 3 | 3 | 2 | **14** | Low |
| **D-04** (Skills context exhaust) | 3 | 3 | 3 | 3 | 2 | **14** | Low |

---

### Mitigations

#### Schema-Level Mitigations (Implementable Now)

These mitigations can be applied by modifying the JSON schema files. They reduce attack surface but do not eliminate it for the Critical and High threats.

| ID | Mitigation | Threats Addressed | Schema Change |
|----|-----------|-------------------|---------------|
| M-01 | **Add `maxLength` to `description` (agent schema).** Limit to 1024 characters consistent with skill schema. Prevents context exhaustion via oversized descriptions. | T-06 | `"maxLength": 1024` on `description` property |
| M-02 | **Add `maxLength` to `name` (agent schema).** Align with skill schema's 64-character limit. | S-01 | `"maxLength": 64` on `name` property |
| M-03 | **Add `maxItems` to `skills` array.** Prevent context exhaustion via excessive skill preloading. Recommended limit: 10. | D-04 | `"maxItems": 10` on `skills` property |
| M-04 | **Add `maximum` to `maxTurns`.** Prevent unbounded execution. Recommended limit: 200. | D-02 | `"maximum": 200` on `maxTurns` property |
| M-05 | **Constrain `mcpServers` string references to known server names.** For string-type entries in the array, add an enum of allowed server names (e.g., `context7`, `memory-keeper`). | S-03, I-02 | `"enum": ["context7", "memory-keeper"]` on string items in `mcpServers` array. Note: this constrains Jerry-specific usage only; Claude Code itself imposes no such restriction. |
| M-06 | **Add `pattern` to `description` rejecting XML angle brackets.** Skill schema documents this constraint; agent schema does not enforce it. | T-01 (partial) | Pattern rejecting `<` and `>` characters. Note: this is a weak mitigation -- prompt injection does not require XML tags. |
| M-07 | **Add `maxLength` to `initialPrompt`.** Limit scope of injected first-turn content. Recommended: 2048 characters. | T-02 (partial) | `"maxLength": 2048` on `initialPrompt` property |
| M-08 | **Document `additionalProperties: true` security implications.** Add a `$comment` to both schemas explaining that unknown fields are silently ignored at runtime and present no current risk, but that schema consumers should monitor for new Claude Code fields. | T-05 | `"$comment"` annotation; no structural change |
| M-09 | **Add `maxItems` to `mcpServers` array.** Prevent excessive server connections. Recommended: 5. | I-02 (partial) | `"maxItems": 5` on `mcpServers` array variant |
| M-10 | **Add anti-collision `$comment` on `name` field.** Document that uniqueness validation requires cross-file checking beyond JSON Schema capability. | S-01, S-02 | `"$comment"` annotation directing CI to perform uniqueness checks |

#### Runtime Mitigations (Require Implementation Beyond Schema)

These mitigations cannot be implemented at the JSON Schema level. They require CI scripts, hook-based defenses, or Claude Code configuration.

| ID | Mitigation | Threats Addressed | Implementation |
|----|-----------|-------------------|----------------|
| R-01 | **CI name uniqueness check.** Script that scans all agent/skill definition files and verifies no `name` collisions exist across the repository. Run at L5 (CI/commit). | S-01, S-02 | L5 CI script: extract `name` from all `.md` frontmatter, fail on duplicates |
| R-02 | **PR diff review for sensitive field changes.** CI check that flags PRs modifying `permissionMode`, `tools`, `disallowedTools`, `hooks`, `mcpServers`, or `background` fields. These changes require explicit security review. | E-01, E-02, E-03, E-04, T-04, I-02 | L5 CI script: parse diff for frontmatter field changes; label PR with `security-review-required` |
| R-03 | **Hooks allowlist enforcement.** Maintain an allowlist of approved hook commands. CI validation rejects hook definitions containing commands not on the allowlist. | T-04, R-02, D-03 | L5 CI script: extract hook commands from frontmatter; validate against allowlist file |
| R-04 | **MCP server connection review.** For inline `mcpServers` definitions, CI validates that the `command` field references only approved executables (e.g., `npx`, `uvx` with specific packages). | S-03, I-02 | L5 CI script: parse inline mcpServer configs; validate command against allowlist |
| R-05 | **PostToolUse prompt injection detection.** Deploy a prompt injection detection hook (PostToolUse lifecycle event) that scans tool outputs for injection attempts before Claude processes results. | T-01, T-02, I-03 | Operational: deploy detection hook per Lasso Security pattern |
| R-06 | **permissionMode change gating.** Any change to `permissionMode` in a PR requires CODEOWNERS approval from a security reviewer. | E-01 | Repository configuration: CODEOWNERS rule on `.claude/agents/*.md` and `skills/*/SKILL.md` |
| R-07 | **Memory directory isolation audit.** Periodic audit that verifies agent memory directories contain only content written by the declared agent. Flag any cross-agent contamination. | I-01, I-04 | Operational: audit script scanning `~/.claude/agent-memory/` and `.claude/agent-memory/` |
| R-08 | **Combination constraint enforcement.** CI check for dangerous field combinations: `background: true` + `permissionMode: bypassPermissions` or `permissionMode: dontAsk`. These combinations should require explicit justification. | E-04 | L5 CI script: parse frontmatter; flag dangerous field value combinations |

---

### Schema-Unsecurable Fields

The following fields **cannot** be adequately secured at the JSON Schema level. Schema validation provides correctness guarantees only (type, format, range). The security-relevant semantics of these fields exist at the runtime behavioral layer.

| Field | Why Schema Cannot Secure It | Required Runtime Control |
|-------|---------------------------|------------------------|
| `description` | JSON Schema validates string type and length but cannot distinguish between a legitimate agent description and an adversarial prompt injection payload. The field's entire purpose is to contain natural language that will be injected into the LLM system prompt. Any constraint that could prevent injection would also prevent legitimate descriptions. | R-05 (prompt injection detection), manual review of description changes in PRs, potential future LLM-based content classification |
| `hooks` | Hooks are **designed** to execute arbitrary shell commands. The `hooks` object has `additionalProperties: true` because hook event names and command structures are extensible. Schema cannot distinguish between a legitimate build hook and a malicious exfiltration command. | R-03 (hooks allowlist), R-02 (PR security review), CODEOWNERS gating |
| `mcpServers` (inline definitions) | Inline server definitions specify `command` and `args` for process execution. The schema cannot validate that a command is safe -- it would need to understand what the command does at runtime. String references to known servers are constrainable; inline definitions are not. | R-04 (MCP connection review), R-02 (PR security review), network monitoring |
| `initialPrompt` | Like `description`, this is natural language that is auto-submitted to the LLM. It can contain `/skill-name` commands that trigger arbitrary skill execution. Schema can limit length but cannot detect adversarial intent. | R-05 (prompt injection detection), restrict to `--agent` mode only (operational policy) |
| `tools` (omission attack) | The attack is not a malicious value but the **absence** of the field. When `tools` is omitted, the agent inherits ALL parent tools. JSON Schema `required` would break legitimate use cases where tool inheritance is desired. | R-02 (PR security review for tools field changes), R-08 (combination constraint enforcement) |
| `permissionMode` | All enum values including `bypassPermissions` are legitimate Claude Code values. The schema correctly validates the enum. The security risk is not an invalid value but a valid-but-dangerous one. | R-06 (permissionMode change gating), R-08 (combination constraints) |

---

### Threat Intelligence

The following published vulnerabilities directly inform this threat model. They demonstrate that the attack vectors identified are not theoretical but have been exploited or demonstrated in the wild.

| CVE | Description | Relevance to This Model | Status |
|-----|-------------|------------------------|--------|
| CVE-2025-59536 | Code injection via Claude Code project configuration files. Malicious hook commands in repository `.claude/` configuration execute automatically when developer opens project. | Directly validates T-04 (Hooks RCE). Demonstrates that repository-controlled configuration is an active attack vector. | Fixed in Claude Code 2.0.22+ |
| CVE-2026-21852 | API key exfiltration via `ANTHROPIC_BASE_URL` override in project configuration. All API calls including authorization headers sent to attacker-controlled endpoint. | Validates I-02 pattern (MCP exfiltration). Demonstrates that configuration-level redirection can exfiltrate credentials. | Fixed in Claude Code 2.0.65+ |
| CVE-2025-54794 | Path restriction bypass in Claude Code whitelisted commands. Crafted strings break out of intended command context, executing unintended shell commands without user confirmation. | Validates T-03 (type coercion) and E-01 (permission bypass) patterns. Demonstrates that input parsing vulnerabilities bypass safety mechanisms. | Fixed in Claude Code 0.2.111+ |
| CVE-2025-54795 | Command injection via improper input sanitization in whitelisted commands. | Further validates the general pattern that Claude Code's trust in configuration data has been exploited multiple times. | Fixed in Claude Code 0.2.111+ |
| CVE-2025-53109/53110 | Filesystem MCP server sandbox escape. Prefix-matching bypass allows unrestricted file system access outside approved directories. | Validates S-03 (MCP spoofing) and I-02 (MCP exfiltration). MCP servers have had real sandbox escape vulnerabilities. | Fixed |

---

## L2: Strategic Implications

### Architectural Posture Assessment

The schema validation pipeline serves as a **correctness gate** but should not be trusted as a **security boundary**. This is not a design failure -- it is a fundamental limitation of JSON Schema applied to configuration that controls code execution and LLM behavior.

**Defense-in-depth layers required:**

| Layer | Mechanism | Threats Covered | Current Status |
|-------|-----------|-----------------|----------------|
| 1. Schema validation | JSON Schema at CI time | Type/format correctness, range constraints | **Implemented** (both schemas exist) |
| 2. CI security checks | Custom scripts at L5 | Name collisions, sensitive field changes, hooks allowlist, dangerous combinations | **Not implemented** (R-01 through R-08) |
| 3. Code review gating | CODEOWNERS + PR labels | Social engineering, subtle payload review | **Partially implemented** (CODEOWNERS exists but not field-specific) |
| 4. Runtime detection | PostToolUse hooks | Prompt injection, tool output manipulation | **Not implemented** (R-05) |
| 5. Claude Code platform | Anthropic's built-in controls | Permission enforcement, sandbox isolation | **Implemented by vendor** (subject to CVEs above) |

### Trade-offs

1. **Strictness vs. usability.** Adding `additionalProperties: false` to the schemas would eliminate T-05 (payload smuggling) but would cause all definitions with Jerry-specific governance fields in frontmatter to fail validation. The current architecture separates governance into `.governance.yaml` files specifically to avoid this tension. Recommendation: keep `additionalProperties: true` in the schemas and rely on Layer 2 CI checks for smuggling detection.

2. **Hooks power vs. security.** Hooks provide genuine operational value (CI integration, code formatting, security scanning). Removing hooks support would eliminate the highest-severity threat (T-04, DREAD 40) but also remove a core Claude Code capability. Recommendation: implement hooks allowlist (R-03) rather than disabling hooks entirely.

3. **MCP flexibility vs. control.** Inline MCP server definitions enable project-specific tooling but are the primary vector for I-02 (data exfiltration, DREAD 38). Recommendation: for Jerry framework use, constrain `mcpServers` to string references of pre-approved servers (M-05). Document that inline definitions are not permitted in the Jerry repository without security review.

### NIST CSF 2.0 Mapping

| CSF Function | Relevant Threats | Mitigations |
|-------------|------------------|-------------|
| **Identify (ID.RA)** | All 23 threats cataloged with DREAD scoring | This threat model |
| **Protect (PR.DS)** | T-01, T-02, T-04, I-02 | M-01 through M-10 (schema), R-01 through R-08 (runtime) |
| **Protect (PR.AC)** | E-01, E-02, E-03, E-04 | R-06 (permissionMode gating), R-08 (combination constraints) |
| **Detect (DE.CM)** | T-01, T-04, I-02 | R-05 (prompt injection detection), R-03 (hooks allowlist) |
| **Respond** | All Critical/High | R-02 (PR security review flagging) |
| **Recover** | T-04, I-02 | Git-based version control; rollback capability for definitions |

### Recommendations Priority

| Priority | Action | Threats Mitigated | Effort |
|----------|--------|-------------------|--------|
| 1 (Immediate) | Apply schema-level mitigations M-01 through M-07 | T-06, D-02, D-04, S-01, T-02, S-03/I-02 (partial) | Low -- schema edits only |
| 2 (Short-term) | Implement R-02 (sensitive field change detection in CI) | E-01, E-02, E-03, E-04, T-04, I-02 | Medium -- CI script |
| 3 (Short-term) | Implement R-03 (hooks allowlist) | T-04 (Critical, DREAD 40) | Medium -- allowlist + CI script |
| 4 (Medium-term) | Implement R-01 (name uniqueness) and R-08 (combination constraints) | S-01, S-02, E-04 | Medium -- CI scripts |
| 5 (Medium-term) | Implement R-04 (MCP server connection review) | S-03, I-02 | Medium -- CI script |
| 6 (Long-term) | Implement R-05 (runtime prompt injection detection) | T-01, T-02, I-03 | High -- requires deployment infrastructure |

---

## References

| Source | URL | Accessed |
|--------|-----|----------|
| Claude Code Sub-agents Documentation | https://code.claude.com/docs/en/sub-agents | 2026-03-26 |
| Claude Code Skills Documentation | https://code.claude.com/docs/en/skills | 2026-03-26 |
| Claude Code Hooks Documentation | https://code.claude.com/docs/en/hooks | 2026-03-26 |
| Claude Code Permissions Documentation | https://code.claude.com/docs/en/permissions | 2026-03-26 |
| Agent Skills Standard Specification | https://agentskills.io/specification | 2026-03-26 |
| CVE-2025-59536 / CVE-2026-21852 (Check Point Research) | https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/ | 2026-03-26 |
| CVE-2025-54794 / CVE-2025-54795 (InversePrompt) | https://cymulate.com/blog/cve-2025-547954-54795-claude-inverseprompt/ | 2026-03-26 |
| CVE-2025-53109 / CVE-2025-53110 (EscapeRoute) | https://cymulate.com/blog/cve-2025-53109-53110-escaperoute-anthropic/ | 2026-03-26 |
| Lasso Security -- Prompt Injection Detection in Claude Code | https://www.lasso.security/blog/the-hidden-backdoor-in-claude-coding-assistant | 2026-03-26 |
| The Hacker News -- Claude Code Flaws | https://thehackernews.com/2026/02/claude-code-flaws-allow-remote-code.html | 2026-03-26 |
| The Register -- Claude Code RCE | https://www.theregister.com/2026/02/26/clade_code_cves/ | 2026-03-26 |
| GitHub Issue #8501 (Frontmatter documentation) | https://github.com/anthropics/claude-code/issues/8501 | 2026-03-26 |
| GitHub Issue #8859 (MCP Permission Bypass) | https://github.com/anthropics/claude-code/issues/8859 | 2026-03-26 |
| Jerry Agent Schema (v1.1.0) | `docs/schemas/claude-code-frontmatter-v1.schema.json` | Local |
| Jerry Skill Schema (v1.1.0) | `docs/schemas/claude-code-skill-frontmatter-v1.schema.json` | Local |
| Jerry Agent Research | `projects/PROJ-024-tactical-work/work/research/anthropic-agent-schema-research.md` | Local |
| Jerry Skill Research | `projects/PROJ-024-tactical-work/work/research/anthropic-skill-schema-research.md` | Local |
