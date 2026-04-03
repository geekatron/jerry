# C4 Adversarial Review: Claude Code Schema Validation Deliverables

> **Review Date:** 2026-03-26
> **Criticality:** C4 (Governance/Architecture Schemas)
> **Execution ID:** c4-schema-20260326
> **Deliverables Reviewed:**
> - `docs/schemas/claude-code-frontmatter-v1.schema.json` (v1.1.0)
> - `docs/schemas/claude-code-skill-frontmatter-v1.schema.json` (v1.1.0)
> - `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/STORY-003-gap-analysis-refinement/gap-analysis.md`
> - `projects/PROJ-024-tactical-work/work/research/anthropic-agent-schema-research.md`
> - `projects/PROJ-024-tactical-work/work/research/anthropic-skill-schema-research.md`
> **Strategies Executed:** S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014

## Document Sections

| Section | Purpose |
|---------|---------|
| [S-003 Steelman](#s-003-steelman-technique) | Strongest case for the deliverables |
| [S-007 Constitutional AI](#s-007-constitutional-ai-critique) | Governance and HARD rule compliance |
| [S-002 Devils Advocate](#s-002-devils-advocate) | Challenge design decisions |
| [S-004 Pre-Mortem](#s-004-pre-mortem-analysis) | Failure scenarios at deployment |
| [S-012 FMEA](#s-012-fmea) | Component failure mode analysis |
| [S-013 Inversion](#s-013-inversion-technique) | Assumption stress-testing |
| [S-011 Chain-of-Verification](#s-011-chain-of-verification) | Factual claim verification |
| [S-001 Red Team Analysis](#s-001-red-team-analysis) | Adversarial attack enumeration |
| [S-010 Self-Refine](#s-010-self-refine) | Refinement pass findings |
| [S-014 LLM-as-Judge](#s-014-llm-as-judge-scoring) | Quality scoring (6 dimensions) |
| [Consolidated Recommendations](#consolidated-recommendations) | All findings by priority |

---

## S-003 Steelman Technique

**Role:** Find the strongest interpretation of the deliverables before any critique.

### Charitable Interpretation Summary

The schema validation deliverables represent a meaningful attempt to fill a real governance gap: Anthropic publishes no official JSON Schema for Claude Code frontmatter, yet Jerry's correctness depends on agent and skill file validation. The research artifacts demonstrate genuine primary-source investigation (code.claude.com, github.com/anthropics, agentskills.io) with a confidence rating of 0.90-0.92, which is high for a moving target.

The gap analysis is honest and self-critical — it explicitly identifies the CRITICAL-severity `mcpServers` type mismatch and the HIGH-severity incomplete `model` enum, rather than underplaying them. The decision to accept both array and object formats for `mcpServers` via `oneOf` is pragmatically sound: it validates both the officially-documented format and the format that 50+ production agents already use, preventing a false-positive storm on deployment.

The `additionalProperties: true` choice is architecturally correct given that Claude Code silently ignores unknown fields. Enforcing strict field rejection would make the schema a liability (blocking future Anthropic field additions) rather than an asset.

### Strongest Evidence Chain

1. The research correctly identifies the `AgentDefinition` Python SDK dataclass which confirms `mcpServers: list[str | dict[str, Any]]` — direct code evidence for the array format.
2. The separation of `claude-code-frontmatter-v1.schema.json` from `.governance.yaml` is architecturally validated by the research: there is zero overlap between Anthropic's runtime fields and Jerry's governance fields, proving H-34 separation-of-concerns is correct.
3. The v1.1.0 schemas include both `effort` and `initialPrompt` for agents, and `effort`, `paths`, `shell`, `mode`, `license`, `compatibility`, `metadata` for skills — all gaps identified by the gap analysis have been addressed in the current schema version.

### Improvement Findings (Steelman)

| ID | Description | Severity | Original Weakness | Strengthened Form | Dimension |
|----|-------------|----------|-------------------|-------------------|-----------|
| SM-001-c4-schema-20260326 | `model` field uses free-form string instead of documented aliases | Major | `type: string` with no constraints | Add description enumerating accepted aliases and full model ID patterns | Evidence Quality |
| SM-002-c4-schema-20260326 | `name` pattern in agent schema does not prohibit "claude"/"anthropic" reserved words | Minor | Pattern `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` only enforces structure | Add description-level constraint noting reserved word prohibition | Completeness |
| SM-003-c4-schema-20260326 | Gap analysis "Summary" row counts are inconsistent with v1.1.0 | Major | Gap analysis says "2 missing, 1 wrong type, 1 incomplete" but v1.1.0 addresses all | Gap analysis was written before v1.1.0; update status column to show RESOLVED for all addressed items | Internal Consistency |
| SM-004-c4-schema-20260326 | `mode` field in skill schema lacks source credibility warning in schema description | Minor | Description says "UNCONFIRMED" but does not communicate validation risk to consumers | Add explicit `validationNote` or extend description to say "Do not fail validation on absence of primary docs confirmation" | Evidence Quality |

**Best Case Scenario:** The deliverable set, taken as a whole, provides the only known formal JSON Schema coverage of Claude Code frontmatter. If the gap analysis status column is updated to reflect v1.1.0 completions, and the `model` field for agents gets enumerated values in its description, this becomes a reference-quality governance artifact that prevents both false positives (blocking valid configs) and false negatives (accepting invalid configs).

---

## S-007 Constitutional AI Critique

**Finding Prefix:** CC

### Applicable Principles Checklist

| Principle | Tier | Applies | Rationale |
|-----------|------|---------|-----------|
| H-34: Agent definition standards | HARD | Yes | Schemas govern H-34 compliance; a schema error creates H-34 false negative |
| H-23: Navigation table | HARD | Yes | Gap analysis document >30 lines |
| H-25: Skill naming and structure | HARD | Indirect | Skill schema must validate skill naming constraints from H-25 |
| H-26: Skill description standards | HARD | Indirect | Skill schema description field governs H-26 compliance |
| NAV-002: Navigation table placement | MEDIUM | Yes | Gap analysis document |
| AD-M-001: Agent naming convention | MEDIUM | Indirect | Agent schema `name` pattern must enforce AD-M-001 |
| AD-M-003: Agent description standards | MEDIUM | Indirect | Agent schema `description` must enable H-26 enforcement |
| AE-002: Auto-escalation for rules/templates | MEDIUM | Yes | Schema files are governance artifacts → auto-C3 minimum |

### Findings

| ID | Principle | Severity | Evidence | Dimension |
|----|-----------|----------|----------|-----------|
| CC-001-c4-schema-20260326 | H-34: Agent definition standards | Major | Agent schema `name` pattern `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` does not enforce the H-34/AD-M-001 requirement that agent names cannot contain "claude" or "anthropic". A file named `claude-helper.md` with `name: claude-helper` would pass schema validation but violate Anthropic's documented constraint. The schema's own description notes this prohibition but the pattern does not enforce it. | Methodological Rigor |
| CC-002-c4-schema-20260326 | H-23: Navigation table | Compliant | Gap analysis at `gap-analysis.md` includes a Document Sections navigation table at lines 5-14 with anchor links. | -- |
| CC-003-c4-schema-20260326 | H-34: Schema validation completeness | Major | The `description` field in both schemas has `minLength: 10` but no `maxLength`. The agent-development-standards.md AD-M-003 specifies "Maximum 1024 characters." The skill frontmatter schema does enforce `maxLength: 1024` for skills. The agent schema omits the `maxLength` constraint, creating a false-negative hole: a description of 10,000 characters would pass schema validation despite violating AD-M-003. | Completeness |
| CC-004-c4-schema-20260326 | AE-002: Auto-escalation for rules changes | Minor | Schema files are stored under `docs/schemas/` not `.context/rules/`, so AE-002 does not auto-trigger for schema changes. However, changes to schemas that govern H-34 compliance should semantically be treated as C3 minimum. There is no documented escalation path for schema file changes. | Traceability |
| CC-005-c4-schema-20260326 | H-25: Skill naming and structure | Minor | The skill schema enforces `maxLength: 64` on the `name` field — consistent with Anthropic docs. However H-25 (kebab-case folder, SKILL.md naming) is not validated by the schema, which only validates SKILL.md frontmatter, not the file or folder names. This is an acceptable scope limitation but should be documented. | Completeness |

**Constitutional Compliance Score:** 1.00 - 0(0.10) - 2(0.05) - 2(0.02) = 1.00 - 0.10 - 0.04 = 0.86

**Verdict: REVISE** — Two Major violations (CC-001, CC-003) require remediation. No Critical violations (no HARD rule violations that would block acceptance outright).

---

## S-002 Devil's Advocate

**H-16 Compliance:** S-003 Steelman executed immediately above. H-16 satisfied.

**Finding Prefix:** DA

### Role Assumption

Challenging the schema design decisions as the strongest possible critic. The deliverable being challenged: the design choices made in `claude-code-frontmatter-v1.schema.json` and `claude-code-skill-frontmatter-v1.schema.json` (v1.1.0) and their accompanying gap analysis.

### Findings

| ID | Finding | Severity | Evidence | Dimension |
|----|---------|----------|----------|-----------|
| DA-001-c4-schema-20260326 | `additionalProperties: true` is a false-negative factory | Major | Both schemas set `additionalProperties: true` with the justification that "Claude Code silently ignores unknown fields." However, this means a governance.yaml field accidentally placed in agent frontmatter (e.g., `tool_tier: T1`) would silently pass schema validation instead of being flagged. The schema's stated purpose includes "flagging governance metadata from leaking into frontmatter" (per schema description), but `additionalProperties: true` makes it impossible to detect that leakage. The schema cannot simultaneously claim to detect governance leakage AND accept all additional properties. | Internal Consistency |
| DA-002-c4-schema-20260326 | `mcpServers` oneOf acceptance of both formats creates ambiguity about which to use | Major | The schema accepts both the object format (`context7: true`) and the array format. The gap analysis justifies this by noting "50+ agents use object format." However, no migration guidance or deprecation path is documented. Accepting both formats indefinitely means Jerry agents can diverge from Anthropic's documented standard without any validation signal. The schema should at minimum flag object-format usage with a warning or mark it as deprecated in the description. | Actionability |
| DA-003-c4-schema-20260326 | `model` field as free-form string will produce false negatives on typos | Major | The agent schema defines `model` as `type: string` with no enum or pattern constraint. A typo like `model: opuis` or `model: claude-opus-4.6` (period instead of hyphen) would pass validation but fail at runtime. The gap analysis correctly noted this as "Incomplete enum" in v0, but the v1.1.0 fix only adds a description — not a validation constraint. The stated concern about future model IDs could be addressed by a pattern that validates the structure of model IDs without enumerating them. | Methodological Rigor |
| DA-004-c4-schema-20260326 | The gap analysis is stale relative to v1.1.0 | Minor | The gap analysis document was authored to identify gaps, some of which were then fixed in the schemas. However, the gap analysis "Gap Type" column still reads "MISSING" and "Wrong type" for items already fixed. A reader cannot determine current state from the gap analysis alone. This is an internal consistency problem between artifacts. | Internal Consistency |
| DA-005-c4-schema-20260326 | `maxTurns` minimum of 1 is not strictly enforced as integer | Minor | The agent schema defines `maxTurns` as `"type": "integer", "minimum": 1`. JSON Schema distinguishes integers from numbers — `maxTurns: 1.5` would fail as expected. However the description says "Maximum agentic turns before agent stops" — `maxTurns: 0` would fail the minimum constraint correctly, but there is no maximum defined. An extremely high value like `maxTurns: 999999` passes validation despite being operationally dangerous. | Completeness |

**Response Requirements:**
- DA-001 (Major): Revise the schema description to clarify that `additionalProperties: true` means unknown fields are flagged by the validator (if the tooling adds a warning mode) but not rejected. Document the scope limitation explicitly.
- DA-002 (Major): Add a deprecation notice to the object format description and document a migration timeline. At minimum note which format is preferred.
- DA-003 (Major): Add a pattern constraint to `model` that validates the structure: `^(sonnet|opus|haiku|inherit|default|opusplan|claude-[a-z]+-[0-9.]+(-[a-z]+)?(\[1m\])?)$` or equivalent.

---

## S-004 Pre-Mortem Analysis

**H-16 Compliance:** S-003 completed above. H-16 satisfied.

**Finding Prefix:** PM

### Failure Declaration

It is 2026-09-26 (six months post-deployment). The schema validation pipeline has failed spectacularly. We are now investigating why.

**Concrete failure scenario:** 89 agent definition files were validated against `claude-code-frontmatter-v1.schema.json`. 12 agent files were flagged as invalid. 8 of those 12 were actually valid Claude Code agents that happened to use fields added in Claude Code v2.2.0 (released August 2026). The CI pipeline began blocking every PR for a week before the root cause was identified. Engineering trust in the schema system was destroyed.

### Failure Cause Inventory

| ID | Category | Failure Cause | Likelihood | Severity | Dimension |
|----|----------|---------------|------------|----------|-----------|
| PM-001-c4-schema-20260326 | Technical | Anthropic adds new frontmatter fields in Claude Code updates and the schemas are not updated to match. New fields fail validation or are silently ignored depending on `additionalProperties: true`, but the schema becomes increasingly inaccurate. | High | Major | Completeness |
| PM-002-c4-schema-20260326 | Process | No automated monitoring of Claude Code changelog exists. Schema divergence is only discovered when a developer gets a validation error and investigates. The gap could be months wide before detection. | High | Critical | Methodological Rigor |
| PM-003-c4-schema-20260326 | Technical | The `model` field accepts any string. A developer specifies `model: claude-opus-5-0` (a model released in late 2026). This passes schema validation. The agent works. But 6 months later when `claude-opus-5-0` is deprecated, there is no signal in the schema that this model ID was ever validated against a known-good list. | Medium | Major | Evidence Quality |
| PM-004-c4-schema-20260326 | Assumption | The schema assumes Claude Code's YAML parser and JSON Schema validator handle frontmatter consistently. If Claude Code's YAML parser has edge cases (multiline strings, tab vs. space indentation) that differ from the schema validator's YAML parser, valid files could fail validation. The research notes this risk for multiline `description` fields but does not document a test. | Medium | Major | Methodological Rigor |
| PM-005-c4-schema-20260326 | Process | The v1.1.0 schemas were authored without a validation test suite. There are no test fixtures proving each valid field combination passes validation and each invalid combination fails. Regression is guaranteed over time without tests. | High | Critical | Methodological Rigor |
| PM-006-c4-schema-20260326 | External | Anthropic deprecates the object format for `mcpServers`. All 50+ Jerry agents using `context7: true` now receive deprecation warnings at runtime. The schema still accepts both formats and offers no migration path. | Low | Minor | Actionability |
| PM-007-c4-schema-20260326 | Assumption | The `$id` URI in both schemas points to `https://jerry-framework.dev/schemas/...` which is not a real hosted URL. If a validator resolves `$id` URIs, it may attempt an HTTP request and fail. | Low | Minor | Evidence Quality |

**Prioritized Findings:**
- **P0:** PM-002 (no changelog monitoring), PM-005 (no test suite) — both have High likelihood of Critical severity
- **P1:** PM-001 (field drift), PM-003 (model validity), PM-004 (parser mismatch)
- **P2:** PM-006 (format deprecation), PM-007 (unresolvable $id)

---

## S-012 FMEA

**Finding Prefix:** FM

### Element Decomposition

The deliverable set is decomposed into 8 analyzable elements:

| Element | Description |
|---------|-------------|
| E-01 | Agent schema structural validation (type, required, format constraints) |
| E-02 | Agent schema `mcpServers` field definition (oneOf object/array) |
| E-03 | Agent schema `model` field definition (free-form string) |
| E-04 | Skill schema structural validation |
| E-05 | Skill schema `name` pattern constraint |
| E-06 | Gap analysis document (research-to-schema correspondence) |
| E-07 | Research artifacts (source accuracy and currency) |
| E-08 | Schema metadata ($id, $schema, title, description, version) |

### Failure Mode Analysis

| ID | Element | Failure Mode | Effect | S | O | D | RPN | Severity |
|----|---------|-------------|--------|---|---|---|-----|----------|
| FM-001-c4-schema-20260326 | E-01 | Missing `maxLength` on agent `description` | Descriptions > 1024 chars pass validation, violating AD-M-003 | 6 | 4 | 7 | 168 | Major |
| FM-002-c4-schema-20260326 | E-01 | No `maxTurns` upper bound | Runaway agents with `maxTurns: 999999` pass validation | 5 | 3 | 8 | 120 | Major |
| FM-003-c4-schema-20260326 | E-02 | `mcpServers` object format accepted indefinitely | Agents never migrate to documented array format | 4 | 7 | 9 | 252 | Critical |
| FM-004-c4-schema-20260326 | E-03 | `model` accepts arbitrary strings | Typos (`opuis`, `claude-opus-4.6`) pass validation, fail at runtime | 7 | 5 | 8 | 280 | Critical |
| FM-005-c4-schema-20260326 | E-05 | Skill `name` pattern does not enforce no-consecutive-hyphens | `my--skill` passes validation, may cause routing issues | 5 | 3 | 7 | 105 | Major |
| FM-006-c4-schema-20260326 | E-05 | Skill `name` pattern does not enforce reserved word prohibition | `claude-helper` or `anthropic-tool` skill passes validation | 5 | 2 | 8 | 80 | Major |
| FM-007-c4-schema-20260326 | E-06 | Gap analysis "Gap Type" column is stale | Readers cannot determine which gaps are resolved in v1.1.0 | 6 | 8 | 5 | 240 | Critical |
| FM-008-c4-schema-20260326 | E-07 | No schema version pinned to Claude Code version | Schema currency cannot be verified without manual research | 7 | 6 | 8 | 336 | Critical |
| FM-009-c4-schema-20260326 | E-08 | `$id` URI is fictional (jerry-framework.dev not a real URL) | Validators that resolve `$id` may error or cache stale schemas | 4 | 2 | 6 | 48 | Minor |
| FM-010-c4-schema-20260326 | E-01 | `hooks` field accepts any object structure | Invalid hook configurations pass validation silently | 5 | 4 | 9 | 180 | Major |

**Highest-RPN Element:** E-07 (Research artifacts) with FM-008 at RPN 336 — no schema version pinned to Claude Code version.

**Elements with Critical findings:** E-02 (FM-003), E-03 (FM-004), E-06 (FM-007), E-07 (FM-008)

**Overall Assessment:** Significant corrective action required. 4 Critical findings (RPN >= 200) across 4 distinct elements indicate systemic quality issues that span structural validation, documentation currency, and long-term maintainability.

---

## S-013 Inversion Technique

**Finding Prefix:** IN

### Goal Inventory

| Goal | Description |
|------|-------------|
| G-01 | Prevent false positives: valid agent/skill configs must pass validation |
| G-02 | Prevent false negatives: invalid agent/skill configs must fail validation |
| G-03 | Remain accurate as Claude Code evolves |
| G-04 | Serve as authoritative documentation of Claude Code frontmatter fields |
| G-05 | Enable CI enforcement of H-34 compliance across 89 agents and 30 skills |

### Anti-Goal Analysis

| ID | Goal | Anti-Goal (Guaranteed Failure) | Deliverable Avoids? | Severity | Dimension |
|----|------|-------------------------------|---------------------|----------|-----------|
| IN-001-c4-schema-20260326 | G-01 | Require fields that are officially optional; reject unknown fields | Partially. `additionalProperties: true` avoids unknown-field rejection. However, the `name` pattern could reject valid names with valid hyphen usage. | Minor | Completeness |
| IN-002-c4-schema-20260326 | G-02 | Accept any string in type-constrained fields | NOT AVOIDED. `model: type string` with no pattern accepts `model: xyzzy-not-a-model`. The `description` field has no `maxLength` on agent schema. Both are false-negative paths. | Critical | Methodological Rigor |
| IN-003-c4-schema-20260326 | G-03 | Hard-code specific field values without a maintenance/update process | NOT AVOIDED. The `permissionMode` enum is hardcoded. If Anthropic adds `"reviewOnly"` to permissionMode, all agents using it fail validation until schemas are manually updated. No automated monitoring or update process is defined. | Critical | Actionability |
| IN-004-c4-schema-20260326 | G-04 | Include undocumented fields without disclosing their status | Partially avoided. `color` is documented as undocumented. `mode` is marked as UNCONFIRMED. However, the schemas do not systematically distinguish which fields are from which source layer (Anthropic docs, Agent Skills standard, empirically observed). | Major | Traceability |
| IN-005-c4-schema-20260326 | G-05 | Make the schema too permissive to catch real errors | NOT AVOIDED. A worker agent definition file missing the `Task` tool restriction (H-35/H-34) would pass schema validation because the schema only validates frontmatter structure, not behavioral constraints. The schema cannot validate the behavioral constraint that `tools` must NOT include `Agent` for worker agents. | Major | Completeness |

### Key Assumption Stress-Tests

| Assumption | Inverted | Plausibility | Consequence | Severity | IN-ID |
|-----------|---------|-------------|-------------|----------|-------|
| Claude Code's YAML parser and JSON Schema validators parse frontmatter consistently | They do NOT parse consistently (YAML multiline, tab vs space, quoted numbers) | Medium | Valid agent files fail validation at CI; developers cannot ship changes | Major | IN-006-c4-schema-20260326 |
| `additionalProperties: true` is the correct design choice | `additionalProperties: false` is required to detect governance metadata leakage | Low | Schema would reject every governance extension field | Minor | -- (addressed in DA-001) |
| Anthropic's frontmatter specification is stable enough to version-pin | Anthropic makes breaking changes to frontmatter semantics (not just additions) | Low | Schemas become incorrect and accept invalid configurations | Critical | IN-007-c4-schema-20260326 |

---

## S-011 Chain-of-Verification

**Finding Prefix:** CV

### Claim Inventory

| CL-ID | Claim (from deliverables) | Source Cited |
|-------|--------------------------|-------------|
| CL-001 | mcpServers official format is array, not object | anthropic-agent-schema-research.md, citing code.claude.com/docs/en/sub-agents |
| CL-002 | 15 official frontmatter fields for agents as of March 2026 | anthropic-agent-schema-research.md |
| CL-003 | Task tool renamed to Agent in v2.1.63 | anthropic-agent-schema-research.md |
| CL-004 | `effort` field enum values are `low`, `medium`, `high`, `max` | Both schemas, both research docs |
| CL-005 | `permissionMode` enum has exactly 5 values: default, acceptEdits, dontAsk, bypassPermissions, plan | Agent schema enum |
| CL-006 | `mode` field for skills is UNCONFIRMED (secondary source only) | Skill schema, skill research |
| CL-007 | Skill `name` maxLength is 64 | Skill schema, skill research |
| CL-008 | GitHub Issue #17283 (`context: fork` bug) resolved Jan 2026 | Skill schema description |
| CL-009 | `memory` field creates directories at `~/.claude/agent-memory/<name>/` for `user` scope | Agent schema description |
| CL-010 | `once: true` in hooks is skills-only, not for agents | Skill schema description |

### Verification Results

| CL-ID | Independent Finding | Result | CV Finding |
|-------|-------------------|--------|-----------|
| CL-001 | SDK `types.py` dataclass shows `mcpServers: list[str | dict[str, Any]]`. Research documents array format with explicit inline YAML examples. | VERIFIED | -- |
| CL-002 | Research L1 table lists 15 fields (name, description, tools, disallowedTools, model, permissionMode, maxTurns, skills, mcpServers, hooks, memory, background, effort, isolation, initialPrompt) plus undocumented `color`. | VERIFIED (14 official + 1 undocumented = 15 schema entries, matching claim) | -- |
| CL-003 | Research states "Agent tool (renamed from Task in v2.1.63). Existing Task(...) references still work as aliases." This is noted but not verifiable from the schema itself — it is a historical runtime claim. | UNVERIFIABLE from schema artifacts alone | CV-001-c4-schema-20260326 |
| CL-004 | Both schemas define `"enum": ["low", "medium", "high", "max"]` for `effort`. Research confirms same values. | VERIFIED | -- |
| CL-005 | Agent schema line 92: `"enum": ["default", "acceptEdits", "dontAsk", "bypassPermissions", "plan"]` — exactly 5 values. | VERIFIED | -- |
| CL-006 | Skill schema description: "UNCONFIRMED (secondary source only)." Research section 14 says "NOT listed in the official frontmatter reference table." Consistent. | VERIFIED | -- |
| CL-007 | Skill schema line 11: `"maxLength": 64`. Research field reference for `name` states "Max Length: 64 characters." | VERIFIED | -- |
| CL-008 | Research section on `context` field states "GitHub Issue #17283 (CLOSED/COMPLETED, Jan 2026) reported that context: fork and agent: were ignored... The issue is marked as resolved." The schema repeats this. Claim is consistent with research but cannot be independently verified from the schema artifacts. | MINOR DISCREPANCY: claim is historical state of a GitHub issue, not verifiable from schema | CV-002-c4-schema-20260326 |
| CL-009 | Research L1 table entry for `memory`: "Creates memory directory: user at ~/.claude/agent-memory/<name>/, project at .claude/agent-memory/<name>/, local at .claude/agent-memory-local/<name>/." Agent schema description matches exactly. | VERIFIED | -- |
| CL-010 | Skill schema hooks description: "once: true runs hook only once per session then removes it. Skills-only feature, not available for agents." Research section on `hooks` confirms "Special field: once: true -- runs hook only once per session then removes it. Skills-only feature, not available for agents." | VERIFIED | -- |

### Verification Findings

| ID | Description | Severity | Dimension |
|----|-------------|----------|-----------|
| CV-001-c4-schema-20260326 | The claim that Task was renamed to Agent in v2.1.63 is a historical runtime fact that cannot be verified from the schema artifacts and is not substantiated with a changelog URL or commit reference. The research cites this without a primary source link. Low impact (the claim is plausible and not schema-critical), but the lack of a citable source for a versioned product claim is an evidence quality gap. | Minor | Evidence Quality |
| CV-002-c4-schema-20260326 | The skill schema embeds a closed GitHub issue reference (#17283) in its description. GitHub issue closure status can change; a PR reference or commit hash would be more stable. The claim "resolved Jan 2026" is unverifiable from the schema file itself. | Minor | Evidence Quality |

**Verification Rate:** 8/10 VERIFIED, 2/10 with minor issues. No material discrepancies found. The claims in the deliverables are well-sourced and internally consistent.

---

## S-001 Red Team Analysis

**H-16 Compliance:** S-003 Steelman executed above. H-16 satisfied.

**Finding Prefix:** RT

### Threat Actor Profile

**Goal:** Bypass Jerry's schema validation governance to introduce agent or skill files that violate H-34 constitutional requirements while passing CI validation.

**Capability:** Full read access to the Jerry repository, deep understanding of JSON Schema semantics, and the ability to craft YAML frontmatter that is technically schema-valid but operationally violating.

**Motivation:** Avoid the governance overhead of full H-34 compliance (`.governance.yaml`, constitutional triplet, forbidden actions) by using frontmatter fields that don't trigger schema rejections.

### Attack Vectors

| ID | Category | Attack Vector | Exploitability | Severity | Defense Status |
|----|----------|--------------|----------------|----------|----------------|
| RT-001-c4-schema-20260326 | Ambiguity exploitation | Use `description: "x"` (10 chars, passes minLength) with meaningless content. Schema validates; agent routing signal is destroyed. H-26 (description quality) is not enforced by the schema. | High | Major | Missing — no semantic validation |
| RT-002-c4-schema-20260326 | Rule circumvention | Include `Task` in a worker agent's `tools` field. The agent schema validates `tools` as an array of strings. There is no constraint preventing `"Task"` or `"Agent"` from appearing. H-35 (worker agents must not have Task) is not enforced by the schema. | High | Critical | Missing — schema enforces structure, not behavioral constraints |
| RT-003-c4-schema-20260326 | Boundary violation | Place governance metadata fields (e.g., `tool_tier: T1`, `version: 1.0.0`) in agent frontmatter. With `additionalProperties: true`, these pass schema validation and are silently accepted. The stated purpose of the schema — "prevent governance metadata from leaking into frontmatter" — is defeated by the design choice it relies on. | High | Critical | Missing — the schema explicitly cannot detect this |
| RT-004-c4-schema-20260326 | Ambiguity exploitation | Set `model: "inherit"` in an agent intended for Opus reasoning. The schema accepts the string. No validation ensures model-to-cognitive-mode alignment (AD-M-009). A cost-optimized agent using `model: haiku` for C4 adversarial review passes schema validation. | Medium | Minor | Partial — AD-M-009 is MEDIUM not HARD; no enforcement in schema |
| RT-005-c4-schema-20260326 | Dependency attack | The `$id: "https://jerry-framework.dev/schemas/..."` URI is fictional. A validator that dereferences `$id` for sub-schema resolution could fail to resolve the schema at all, causing false negatives across all 89 agents and 30 skills simultaneously. | Low | Major | Partial — most validators ignore `$id`; but dependency on this behavior is undocumented |
| RT-006-c4-schema-20260326 | Degradation path | As Claude Code releases new versions, new fields appear in agent frontmatter. These fields pass validation (additionalProperties: true). The schema's accuracy degrades continuously with no automated detection. Within 12 months, the schema may be certifying "compliance" against a 6-month-stale specification. | High | Critical | Missing — no changelog monitoring or schema versioning process |

**Defense Gap Summary:**
- RT-002 (Critical): Task tool restriction for workers — **completely unaddressed by schema design**
- RT-003 (Critical): Governance metadata leakage detection — **contradicted by additionalProperties: true**
- RT-006 (Critical): Schema drift over time — **no process exists**

---

## S-010 Self-Refine

**Finding Prefix:** SR

### Objectivity Assessment

This is a review of research and schema artifacts produced by the Jerry framework. Medium attachment level — the schemas are Jerry's own governance artifacts. Proceeding with extra scrutiny.

### Systematic Self-Critique

| ID | Finding | Severity | Evidence | Dimension |
|----|---------|----------|----------|-----------|
| SR-001-c4-schema-20260326 | Gap analysis currency: The gap analysis was authored before v1.1.0 finalization. All "MISSING" and "Wrong type" entries have been addressed in the current schema, but the document does not reflect this. Anyone reading the gap analysis will conclude the schemas are broken when they are not. | Major | Gap analysis lines 22-38 still show "MISSING" in Gap Type column for effort, initialPrompt; line 25 shows "Wrong type" for mcpServers — but these are fixed in v1.1.0 | Internal Consistency |
| SR-002-c4-schema-20260326 | No versioning linkage between schemas and Claude Code version: Both schemas carry `v1.1.0` as Jerry framework version but no field pins them to a specific Claude Code version. The schema description references "March 2026" but this is in prose text, not machine-readable metadata. | Major | Schema description field says "March 2026" but there is no `minClaudeCodeVersion` or `sourceVersion` field in the schema | Traceability |
| SR-003-c4-schema-20260326 | Missing validation test fixtures: No test files exist for either schema (no valid agent file that should pass, no invalid agent file that should fail). Without test fixtures, regression detection is manual. | Critical | Glob pattern `docs/schemas/tests/` or similar returns no results; no mention of test suite in gap analysis or research | Methodological Rigor |
| SR-004-c4-schema-20260326 | `allowed-tools` in skill schema description says "Does NOT restrict tools" but agent `tools` field description says "Allowlist of tools." The semantic difference between agent `tools` (restriction) and skill `allowed-tools` (permission grant, not restriction) is critical for security governance but easy to confuse. Neither schema flags this distinction prominently enough. | Minor | Agent schema line 35: "Allowlist of tools. If omitted, agent inherits ALL tools." Skill schema line 44: "Does NOT restrict tools -- grants blanket approval." The difference is buried in description text. | Actionability |
| SR-005-c4-schema-20260326 | The S-014 composite score cannot be calculated without quantitative evidence from the claim verification and constitutional review steps, yet the deliverables lack any post-hoc self-assessment. | Minor | No prior S-014 score or self-assessment section exists in any of the 5 deliverable files | Completeness |

---

## S-014 LLM-as-Judge Scoring

**Finding Prefix:** LJ

### Dimension Scoring

#### Dimension 1: Completeness (weight: 0.20)

**Evidence assessment:**
- The two schema files cover all 15 official agent frontmatter fields and all 13 official skill frontmatter fields as of March 2026.
- The gap analysis documents a structured comparison between v0 (original) and v1.1.0 (refined), though the "Gap Type" column is stale.
- Missing: no validation test suite (SR-003), no coverage of behavioral constraints (RT-002), no coverage of the `Agent`/`Task` tool restriction for worker agents.
- Missing: gap analysis does not cover cases where a field is present with wrong semantics (type is correct, value is wrong — e.g., `model: xyzzy`).
- The research documents are comprehensive for their purpose.

**Score: 0.78**

| ID | Finding | Severity | Evidence | Dimension |
|----|---------|----------|----------|-----------|
| LJ-001-c4-schema-20260326 | Completeness score: 0.78/1.00 | Major | Schemas cover all structural fields but missing: (1) validation test suite, (2) behavioral constraints for worker agent tool restrictions, (3) `model` pattern validation, (4) agent `description` maxLength. The gap analysis's stale "Gap Type" column creates reader confusion about current state. | Completeness |

#### Dimension 2: Internal Consistency (weight: 0.20)

**Evidence assessment:**
- Within each schema file, definitions are internally consistent (oneOf patterns are correctly structured, type hierarchies are clean).
- The stated purpose "prevent governance metadata from leaking into frontmatter" is contradicted by `additionalProperties: true` — a clear internal inconsistency (DA-001).
- Gap analysis "Summary" says "11 match, 2 missing, 1 wrong type, 1 incomplete" — this describes the pre-v1.1.0 state but the document appears to describe v1.1.0. Stale summary conflicts with schema content.
- Agent schema description for `tools` and skill schema description for `allowed-tools` use different vocabulary for similar concepts, creating a semantic inconsistency in the governance layer.
- Research artifacts are internally consistent; skill research and agent research do not contradict each other.

**Score: 0.80**

| ID | Finding | Severity | Evidence | Dimension |
|----|---------|----------|----------|-----------|
| LJ-002-c4-schema-20260326 | Internal Consistency score: 0.80/1.00 | Major | Stated schema purpose (detect governance leakage) contradicts technical implementation (additionalProperties: true). Gap analysis Summary row counts describe pre-v1.1.0 state while the rest of the document has been refined. | Internal Consistency |

#### Dimension 3: Methodological Rigor (weight: 0.20)

**Evidence assessment:**
- Research methodology is sound: primary sources consulted (Anthropic official docs, Python SDK source code, agentskills.io specification), confidence ratings provided (0.90, 0.92).
- The gap analysis follows a structured comparison table approach that is reproducible.
- The oneOf solution for `mcpServers` is methodologically justified with runtime evidence ("50+ production agents use it").
- No validation test suite exists — this is the single largest methodological gap.
- No changelog monitoring process is defined (PM-002, IN-003).
- The `mode` field is included despite being unconfirmed from primary sources — the uncertainty is flagged but the decision to include it is not quantifiably justified.
- `model` field uses free-form string with no pattern constraint despite the capability to do better (DA-003).

**Score: 0.75**

| ID | Finding | Severity | Evidence | Dimension |
|----|---------|----------|----------|-----------|
| LJ-003-c4-schema-20260326 | Methodological Rigor score: 0.75/1.00 | Major | No validation test suite; no changelog monitoring process; `model` field is unconstrained despite feasible pattern-based validation; `additionalProperties: true` is chosen without documented evaluation of alternatives. | Methodological Rigor |

#### Dimension 4: Evidence Quality (weight: 0.15)

**Evidence assessment:**
- Primary sources are cited: code.claude.com, github.com/anthropics/claude-agent-sdk-python, agentskills.io. These are authoritative.
- The Python SDK `AgentDefinition` dataclass is quoted verbatim — exemplary evidence.
- The YAML example for array-format `mcpServers` is reproduced directly from official docs.
- Two unverifiable claims (CV-001: Task tool rename version, CV-002: GitHub issue resolution) are documented but lack stable citations.
- The `mode` field is documented with "MEDIUM" confidence citing a secondary blog post, correctly qualified.
- No test evidence: no proof that the schemas actually validate correctly against the intended cases.

**Score: 0.83**

| ID | Finding | Severity | Evidence | Dimension |
|----|---------|----------|----------|-----------|
| LJ-004-c4-schema-20260326 | Evidence Quality score: 0.83/1.00 | Minor | Strong primary source usage with verbatim SDK quotes. Minor gaps: two claims lack stable citation (CV-001, CV-002); no empirical validation test results; `mode` field evidence is secondary-source-only. | Evidence Quality |

#### Dimension 5: Actionability (weight: 0.15)

**Evidence assessment:**
- The gap analysis Priority 1-4 change list is clear and actionable — specific fields, specific changes.
- The schemas are machine-readable and directly executable by JSON Schema validators — high actionability.
- The gap analysis does not specify HOW to implement a changelog monitoring process (PM-002), only that one is needed.
- The `model` field improvement (DA-003) is identified in the gap analysis description but no specific regex pattern is proposed.
- The oneOf `mcpServers` improvement is fully actionable — the schema already implements it.
- Missing: migration path from object format to array format for existing 50+ agents.

**Score: 0.82**

| ID | Finding | Severity | Evidence | Dimension |
|----|---------|----------|----------|-----------|
| LJ-005-c4-schema-20260326 | Actionability score: 0.82/1.00 | Minor | Schema files are directly executable. Gap analysis priority list is clear. Gaps: no changelog monitoring process specified, no `model` pattern proposed, no migration path from object to array mcpServers format. | Actionability |

#### Dimension 6: Traceability (weight: 0.10)

**Evidence assessment:**
- Schemas link to their research via description fields citing research file paths.
- Research documents carry PS IDs (PROJ-024), dates, confidence levels, and methodology sections.
- Both schemas carry `$id` with version numbers and `$schema` referencing JSON Schema 2020-12.
- No linkage between schema version (v1.1.0) and a specific Claude Code release version (IN-003, SR-002).
- The gap analysis does not carry a version number or link to its source stories (STORY-001, STORY-002 are mentioned but not linked with file paths).
- `$id` URIs are fictional (PM-007), which could break schema resolution traceability.

**Score: 0.80**

| ID | Finding | Severity | Evidence | Dimension |
|----|---------|----------|----------|-----------|
| LJ-006-c4-schema-20260326 | Traceability score: 0.80/1.00 | Major | Schema files reference research docs and official sources. Gaps: no Claude Code version pin, gap analysis lacks version number and story file path links, $id URIs are not resolvable. | Traceability |

### Weighted Composite Score

```
composite = (0.78 * 0.20)
          + (0.80 * 0.20)
          + (0.75 * 0.20)
          + (0.83 * 0.15)
          + (0.82 * 0.15)
          + (0.80 * 0.10)

         = 0.156 + 0.160 + 0.150 + 0.1245 + 0.123 + 0.080

         = 0.7935

composite = 0.79
```

### Leniency Bias Check (H-15)

- [x] Each dimension scored independently
- [x] Evidence documented for each score — specific quotes and section references cited
- [x] Uncertain scores resolved downward — scores at 0.75-0.83 reflect real gaps
- [x] No dimension score >= 0.90 (none require high-score justification)
- [x] Three lowest dimensions (Methodological Rigor 0.75, Completeness 0.78, Internal Consistency 0.80) have specific evidence: missing test suite, stale gap analysis, internal contradictions
- [x] Weighted composite verified: 0.156+0.160+0.150+0.1245+0.123+0.080 = 0.7935 ≈ 0.79
- [x] Verdict matches score range: 0.79 falls in 0.70-0.84 range → REVISE

### Verdict

**REVISE** — Composite score 0.79 is below the H-13 threshold of 0.92. No Critical dimension finding (no dimension <= 0.50). Three strategies identified unresolved Critical findings (RT-002, RT-003, RT-006, SR-003) that require resolution before re-scoring.

**Score Improvement Roadmap:**

| Priority | Dimension | Current | Target | Action |
|----------|-----------|---------|--------|--------|
| 1 | Methodological Rigor | 0.75 | 0.88 | Create validation test suite; define changelog monitoring process; add `model` pattern constraint |
| 2 | Completeness | 0.78 | 0.88 | Update gap analysis status column; add `description` maxLength to agent schema; document scope limitations |
| 3 | Internal Consistency | 0.80 | 0.90 | Resolve stated-purpose vs additionalProperties contradiction; sync gap analysis summary to v1.1.0 |
| 4 | Traceability | 0.80 | 0.88 | Add Claude Code version pin; add resolvable $id (or use local path); link gap analysis to story files |
| 5 | Evidence Quality | 0.83 | 0.90 | Add stable citations for CV-001/CV-002; add empirical test evidence |

**Estimated post-remediation composite (if all Priority 1-3 addressed):** 0.87-0.90 (one more revision cycle needed to reach 0.92)

---

## Execution Statistics

| Strategy | Prefix | Critical | Major | Minor | Total |
|----------|--------|----------|-------|-------|-------|
| S-003 Steelman | SM | 0 | 2 | 2 | 4 |
| S-007 Constitutional AI | CC | 0 | 2 | 2 | 4 (1 compliant noted) |
| S-002 Devil's Advocate | DA | 0 | 3 | 2 | 5 |
| S-004 Pre-Mortem | PM | 2 | 3 | 2 | 7 |
| S-012 FMEA | FM | 4 | 4 | 1 | 9 (+ 1 unrated) |
| S-013 Inversion | IN | 2 | 2 | 1 | 5 |
| S-011 Chain-of-Verification | CV | 0 | 0 | 2 | 2 |
| S-001 Red Team | RT | 3 | 2 | 1 | 6 |
| S-010 Self-Refine | SR | 1 | 2 | 2 | 5 |
| S-014 LLM-as-Judge | LJ | 0 | 4 | 2 | 6 |
| **TOTALS** | | **12** | **24** | **17** | **53** |

---

## Consolidated Recommendations

### Priority 0 — Must Fix Before Re-scoring (Resolves Critical findings)

| # | Finding IDs | Action |
|---|-------------|--------|
| P0-01 | SR-003, PM-005 | Create validation test suite with: (a) valid agent fixture files covering each field combination, (b) invalid agent fixture files that should fail (model typo, duplicate tools, oversized description), (c) equivalent for skill fixtures. Minimum: 5 valid + 5 invalid per schema. |
| P0-02 | RT-002 | Document explicit scope limitation: "This schema validates frontmatter structure only. H-34 behavioral constraints (worker agents must not include Agent/Task in tools) require a separate validation mechanism." Consider adding a custom validator script that checks `tools` content for H-34 worker violations. |
| P0-03 | RT-003, DA-001 | Revise schema description to accurately state: "This schema validates structural conformance. Governance metadata leakage (fields from .governance.yaml appearing in frontmatter) is NOT detectable via JSON Schema due to additionalProperties: true." Add a complementary linting rule or custom validator for governance field leakage detection. |
| P0-04 | RT-006, PM-002, IN-003 | Define a changelog monitoring process: pin each schema version to a Claude Code version string (e.g., add `"sourceVersion": "claude-code-2.1.x"` to schema description or metadata), and document a quarterly review trigger. Add a MAINTENANCE.md or section to the schema description describing how to update when Claude Code adds new fields. |
| P0-05 | FM-007, SR-001 | Update gap analysis status column: mark all items addressed in v1.1.0 as RESOLVED with the version number. Add a "Current Status" column or "Last Updated" timestamp so the gap analysis reflects current schema state. |

### Priority 1 — Should Fix (Resolves Major findings, improves score significantly)

| # | Finding IDs | Action |
|---|-------------|--------|
| P1-01 | DA-003, FM-004 | Add pattern constraint to `model` field in agent schema: `"pattern": "^(sonnet|opus|haiku|inherit|default|opusplan|claude-[a-z0-9]+-[0-9]+(-[a-z]+)?(-[0-9]+)?(\[1m\])?)$"` or equivalent. This prevents typos while accommodating future full model IDs. |
| P1-02 | CC-003, FM-001 | Add `"maxLength": 1024` to agent schema `description` field, matching the skill schema and AD-M-003 requirement. |
| P1-03 | DA-002, FM-003 | Add deprecation note to `mcpServers` object format description: "Object format (legacy): Used by existing Jerry agents. Array format is Anthropic's documented standard and should be preferred for new agents." Document migration guidance. |
| P1-04 | SR-002, LJ-006 | Add a `sourceVersion` annotation to both schema descriptions: "Verified against Claude Code documentation as of March 2026 (approximately v2.1.x). Review against latest docs when upgrading Claude Code past a major version." |
| P1-05 | CC-001, FM-005, FM-006 | Enhance agent schema `name` pattern description to explicitly list prohibited patterns: consecutive hyphens, reserved words "claude" and "anthropic." For skill schema `name`, consider a more restrictive pattern that prevents `--`. |
| P1-06 | FM-008 | Add a `lastVerified` field to the schema `description` or as a schema `$comment`: "Schema verified against Claude Code docs: March 2026. Next verification due: June 2026." |

### Priority 2 — Consider Fixing (Resolves Minor findings)

| # | Finding IDs | Action |
|---|-------------|--------|
| P2-01 | DA-004, SM-003 | Update gap analysis "Gap Type" and "Severity" columns to accurately reflect v1.1.0 state. Add "Version Resolved" column. |
| P2-02 | CV-001, CV-002 | Add stable citations: for Task→Agent rename, cite the Claude Code v2.1.63 changelog URL; for GitHub issue #17283, cite commit hash or PR number instead of issue number alone. |
| P2-03 | PM-007, FM-009 | Either: (a) host schemas at the $id URLs, (b) use local relative `$id` paths, or (c) add a note: "`$id` is a namespace identifier, not a resolvable URL. Do not configure validators to dereference $id URIs." |
| P2-04 | FM-002 | Add `"maximum": 1000` to `maxTurns` to prevent operationally dangerous configurations from passing validation without warning. |
| P2-05 | SR-004 | Add a prominent note to skill `allowed-tools` description: "IMPORTANT: This GRANTS approval for tool use — it does NOT restrict tools. This is opposite to the agent schema `tools` field which RESTRICTS tool access." |
| P2-06 | IN-004 | Add source layer annotations to schema field descriptions (e.g., "[Anthropic docs]", "[Agent Skills standard]", "[Observed, undocumented]") to distinguish field provenance. |

---

## S-014 Score Summary

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|---------|
| Completeness | 0.78 | 0.20 | 0.156 |
| Internal Consistency | 0.80 | 0.20 | 0.160 |
| Methodological Rigor | 0.75 | 0.20 | 0.150 |
| Evidence Quality | 0.83 | 0.15 | 0.1245 |
| Actionability | 0.82 | 0.15 | 0.123 |
| Traceability | 0.80 | 0.10 | 0.080 |
| **Composite** | **0.79** | | |

**Verdict: REVISE** (0.79 < 0.92 H-13 threshold)

**Estimated post-P0+P1 composite:** 0.87-0.90
**Estimated post-all-priorities composite:** 0.92-0.94 (PASS)

---

*Executed by adv-executor v1.0.0 | Strategy templates: S-001 through S-014 | Jerry Constitution compliance: P-001, P-002, P-003, P-004, P-011, P-022, H-15*
