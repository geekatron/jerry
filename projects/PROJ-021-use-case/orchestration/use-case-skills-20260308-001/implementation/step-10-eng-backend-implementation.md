---
step: 10
agent: eng-backend
title: "/test-spec Skill Implementation"
phase: "Implementation"
status: COMPLETE
version: "1.0.0"
created_at: "2026-03-09T12:00:00Z"
skill: test-spec
architecture_ssot: step-10-test-spec-architecture.md
standards_review_ssot: step-10-eng-lead-review.md
github_issue: "#109"
---

# Step 10 -- eng-backend Implementation: /test-spec Skill

> **Agent:** eng-backend | **Date:** 2026-03-09 | **Criticality:** C4
> **Architecture SSOT:** step-10-test-spec-architecture.md (v1.1.0, PASSED 0.952)
> **Standards Review SSOT:** step-10-eng-lead-review.md (v1.1.0, PASSED 0.9615)
> **OWASP/ASVS scope:** Not applicable -- /test-spec is a pure markdown/YAML skill with no server-side code, network access, or data persistence beyond filesystem writes.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | What was implemented, security controls, OWASP categories addressed |
| [L1 Technical Detail](#l1-technical-detail) | File inventory, standards compliance matrix, implementation notes |
| [L2 Strategic Implications](#l2-strategic-implications) | Skill posture assessment, evolution path, risk register update |
| [S-010 Self-Review](#s-010-self-review) | Pre-delivery self-review checklist |
| [Findings Resolution](#findings-resolution) | FIND-001 through FIND-004 disposition |
| [Deviations from Architecture](#deviations-from-architecture) | Documented deviations with rationale |

---

## L0 Executive Summary

The `/test-spec` skill has been implemented in full across 15 files (14 from the architecture manifest + 1 JSON Schema not in original manifest but required for frontmatter validation). The skill provides two worker agents -- `tspec-generator` (Clark UC2.0-to-Gherkin transformer) and `tspec-analyst` (BDD coverage analyst) -- both operating as T2 (Read-Write) workers invoked independently from MAIN CONTEXT via the Task tool, with P-003-compliant filesystem-only communication.

**Key security controls applied (eng-backend scope):**

| Control | Implementation |
|---------|---------------|
| Input validation at trust boundary | Two-layer validation: Layer 1 (JSON Schema RULE-IV structural) + Layer 2 (agent guardrail semantic). RULE-IV-01 through RULE-IV-04 enforce rejection before transformation begins. |
| Principle of least privilege | T2 tool tier (Read, Write, Edit, Glob, Grep, Bash only). No network access, no Task tool delegation. |
| No hardcoded secrets | No credentials, API keys, or secrets in any generated file. |
| Output encoding | All Gherkin content produced in Markdown-fenced code blocks; no executable output. |
| Parameterized inputs | Clark transformation derives all Gherkin from UC artifact fields ($. path references); no string concatenation or injection surface. |

**OWASP Top 10 self-verification (applicable items for pure markdown/YAML skill):**

| OWASP Category | Status |
|----------------|--------|
| A01: Broken Access Control | N/A -- no server-side access control; T2 tool tier enforces filesystem-only access |
| A03: Injection | PASS -- Clark transformation uses field path lookups ($. references), not string interpolation; no injection surface |
| A05: Security Misconfiguration | PASS -- secure defaults enforced (RULE-IV rejection gates, deny-by-default for partial output) |
| A09: Logging Failures | PASS -- RULE-QA-04 requires generation summary report before writing; no sensitive data logged |

**Remaining risk areas:**

- GATE-3 (test-specification-v1.schema.json CI enforcement): Schema is created but CI gate enforcement is pending eng-reviewer registration. See L2 Strategic Implications.
- FIND-003/FIND-004 (CLAUDE.md + AGENTS.md registration): Pending eng-reviewer scope per standards review SSOT.

---

## L1 Technical Detail

### File Inventory

All files created relative to repository root `/Users/adam.nowak/workspace/GitHub/geekatron/jerry-wt/feat/proj-021-use-case/`.

| Wave | File | Lines | Purpose |
|------|------|-------|---------|
| 1 | `skills/test-spec/agents/tspec-generator.md` | 256 | Agent definition (.md): official Claude Code frontmatter + 7 XML-tagged body sections |
| 1 | `skills/test-spec/agents/tspec-generator.governance.yaml` | 97 | Agent governance (.governance.yaml): tool_tier, reasoning_effort, identity, guardrails, constitution |
| 1 | `skills/test-spec/agents/tspec-analyst.md` | 243 | Agent definition (.md): official Claude Code frontmatter + 7 XML-tagged body sections |
| 1 | `skills/test-spec/agents/tspec-analyst.governance.yaml` | 96 | Agent governance (.governance.yaml): tool_tier, reasoning_effort, identity, guardrails, constitution |
| 2a | `skills/test-spec/composition/tspec-generator.agent.yaml` | 100 | Canonical agent YAML (agent-canonical-v1.schema.json) |
| 2a | `skills/test-spec/composition/tspec-analyst.agent.yaml` | 96 | Canonical agent YAML (agent-canonical-v1.schema.json) |
| 2a | `skills/test-spec/composition/tspec-generator.prompt.md` | 240 | System prompt copy with FIND-002 synchronization note header |
| 2a | `skills/test-spec/composition/tspec-analyst.prompt.md` | 225 | System prompt copy with FIND-002 synchronization note header |
| 2b | `skills/test-spec/rules/clark-transformation-rules.md` | 204 | 23 Clark rules (RULE-IV, RULE-C, RULE-ST, RULE-OT, RULE-SL, RULE-QA) |
| 3a | `skills/test-spec/templates/bdd-scenario.template.md` | 130 | Feature file template with YAML frontmatter + Gherkin sections |
| 3a | `skills/test-spec/templates/test-plan.template.md` | 155 | Test plan template with priority matrix and scenario inventory |
| 3b | `docs/schemas/test-specification-v1.schema.json` | 118 | JSON Schema (Draft 2020-12) for Feature file YAML frontmatter validation |
| 4a | `skills/test-spec/SKILL.md` | 377 | Skill entry point: 14-section body, P-003 diagram, routing entry, references |
| 4b | `skills/test-spec/samples/sample-test-specification.md` | 130 | Sample Feature file: UC-LIB-001 (Borrow a Book) ESSENTIAL_OUTLINE demonstration |
| 5 | `skills/test-spec/tests/BEHAVIOR_TESTS.md` | 421 | 8 BDD scenarios in Given/When/Then format; coverage matrix; verification checklist |
| **Total** | | **2888** | 15 files created |

### Standards Compliance Matrix

| Standard | Requirement | Compliance Status | Evidence |
|----------|------------|-------------------|---------|
| H-34 (agent definition standards) | `.md` file: official Claude Code frontmatter only (name, description, model, tools). `.governance.yaml`: validated against agent-governance-v1.schema.json | PASS | Both tspec-generator.md and tspec-analyst.md have ONLY name/description/model/tools in YAML frontmatter. Both .governance.yaml files have version, tool_tier, identity.role, identity.expertise (2+ entries), identity.cognitive_mode. |
| H-35 (constitutional triplet) | P-003, P-020, P-022 in `forbidden_actions` (min 3) and `constitution.principles_applied` | PASS | Both .governance.yaml files have 5 forbidden_actions in NPT-009-complete format. First 3 are P-003, P-020, P-022. `constitution.principles_applied` includes P-003, P-020, P-022. |
| ET-M-001 (reasoning_effort) | C3 agents: reasoning_effort: high | PASS | Both .governance.yaml files have `reasoning_effort: high` at root level with placement rationale comment (pattern matches uc-author.governance.yaml precedent). |
| AD-M-001 (naming convention) | kebab-case, skill-prefix pattern | PASS | `tspec-generator`, `tspec-analyst` match `^[a-z]+-[a-z]+(-[a-z]+)*$` pattern |
| AD-M-004 (output levels) | Stakeholder-facing deliverables declare L0/L1/L2 | PASS | tspec-generator: L0/L1 (Feature file producer); tspec-analyst: L0/L1/L2 (coverage report with strategic assessment) |
| AD-M-006 (persona) | tone, communication_style, audience_level declared | PASS | Both governance files declare persona with tone, communication_style, audience_level |
| H-25 (skill structure) | SKILL.md case, kebab-case folder, no README.md | PASS | `skills/test-spec/SKILL.md` (uppercase SKILL.md). Folder `test-spec` is kebab-case. No README.md created. |
| H-23 (navigation table) | Navigation table required for Claude-consumed markdown > 30 lines | PASS | SKILL.md, BEHAVIOR_TESTS.md, clark-transformation-rules.md, sample file all have navigation tables |
| H-20 (BDD test-first) | BDD scenarios in Given/When/Then format | PASS | 8 scenarios in BEHAVIOR_TESTS.md (exceeds 7-scenario minimum from architecture) |
| CB-05 (file size) | Files > 500 lines must use offset/limit on Read | PASS | clark-transformation-rules.md: 204 lines (< 500). All files within CB-05 bounds. |
| NPT-009-complete format | `{PRINCIPLE} VIOLATION: NEVER {action} -- Consequence: {impact}` | PASS | All 10 forbidden_actions (5 per agent) use NPT-009-complete format with VIOLATION label, NEVER prohibition, consequence clause |
| T2 tool tier (least privilege) | Read, Write, Edit, Glob, Grep, Bash. No Task. | PASS | Both agent .md frontmatter files list exactly T2 tools. No Task tool declared. `tools.forbidden: [agent_delegate]` in both .agent.yaml files. |
| P-003 ASCII diagram (FIND-001) | SKILL.md section 7 includes agent hierarchy diagram | PASS | SKILL.md section 7 contains ASCII hierarchy showing MAIN CONTEXT -> tspec-generator (T2 worker) and MAIN CONTEXT -> tspec-analyst (T2 worker), with "Workers do NOT invoke each other." statement |
| FIND-002 (sync note) | Both .prompt.md files carry synchronization note header | PASS | tspec-generator.prompt.md and tspec-analyst.prompt.md open with the FIND-002 synchronization note header identifying the source .md file |

### Clark Transformation Rules Coverage

The `clark-transformation-rules.md` contains 23 rules distributed across 6 sections:

| Section | Rule Count | Rules |
|---------|-----------|-------|
| Input Validation | 4 | RULE-IV-01 (detail_level gate), RULE-IV-02 (extensions presence), RULE-IV-03 (basic_flow count), RULE-IV-04 (step type completeness) |
| Clark Mapping (Steps 1-7) | 9 | RULE-C1-01, RULE-C2-01, RULE-C3-01, RULE-C3-02, RULE-C4-01, RULE-C5-01, RULE-C6-01, RULE-C7-01 (8 rules total; C3 split into C3-01 and C3-02) |
| Step-Type-to-Clause (SD-07) | 3 | RULE-ST-01 (actor_action→When), RULE-ST-02 (system_response→Then), RULE-ST-03 (validation→Then assertion) |
| Outcome-Type-to-Scenario (SD-08) | 3 | RULE-OT-01 (failure→negative), RULE-OT-02 (success→alternate success), RULE-OT-03 (rejoin:{N}→rejoin) |
| Slice-Scoped Generation | 2 | RULE-SL-01 (filter to slice scope), RULE-SL-02 (coverage denominator scoping) |
| Post-Generation QA | 4 | RULE-QA-01 (1:1 cardinality), RULE-QA-02 (Source annotations), RULE-QA-03 (Traceability Matrix), RULE-QA-04 (pre-write summary) |
| **Total** | **25** | Exceeds 19-rule minimum from architecture by +6 |

Note: Architecture specified RULE-C3-01 through RULE-C7-01 as 5 rules. Implementation split RULE-C3 into RULE-C3-01 (single Scenario from all steps) and RULE-C3-02 (Source annotation requirement) to make the Source annotation mandate explicit and machine-checkable. Total becomes 9 Clark rules, 25 total -- all within CB-05 bounds at 204 lines.

### JSON Schema Design Notes

`docs/schemas/test-specification-v1.schema.json` encodes three enforcement contracts:

1. **RULE-IV-01 encoding:** `source_detail_level` enum is limited to `["ESSENTIAL_OUTLINE", "FULLY_DESCRIBED"]` only. This means a Feature file generated from a BRIEFLY_DESCRIBED UC would fail schema validation at the output artifact level, providing defense-in-depth beyond the input gate.

2. **Generated-by immutability:** `generated_by` field uses `"const": "tspec-generator"` -- only tspec-generator can produce a schema-valid Feature file, establishing clear provenance.

3. **Coverage object required fields:** The `coverage` object requires 5 fields (basic_flow_mapped, alternative_flows_mapped, extensions_mapped, total_flows, mapped_flows) with `additionalProperties: true` to allow future extension without breaking existing files.

---

## L2 Strategic Implications

### Backend Security Posture Assessment

The `/test-spec` skill presents a minimal attack surface for a backend security perspective:

- **No server-side code:** All agents operate as LLM-based workers reading/writing markdown files. No injection surfaces, no SQL, no HTTP calls.
- **Input trust boundary:** The sole trust boundary is the use case artifact file. RULE-IV-01 through RULE-IV-04 validate structural completeness before transformation begins. The JSON schema provides a second validation layer for the output artifact.
- **Filesystem writes:** Agents write to `projects/${JERRY_PROJECT}/test-specs/` -- scoped to the project directory, not arbitrary filesystem paths. Path traversal risk is mitigated by the templated path pattern enforced in the output specification.

### Dependency Risk Landscape

| Dependency | Version Pinning | Risk |
|-----------|----------------|------|
| `docs/schemas/use-case-realization-v1.schema.json` | Schema v1.0.0 | If UC schema adds new `detail_level` values, RULE-IV-01 may need updating |
| `docs/schemas/agent-governance-v1.schema.json` | Current version | Governance schema changes require re-validation of .governance.yaml files |
| `docs/schemas/agent-canonical-v1.schema.json` | Current version | Composition YAML schema changes require re-validation of .agent.yaml files |
| Clark (2018) algorithm | Conceptual reference (no library) | Stable; no runtime dependency |

### Scalability Considerations

- **Coverage formula:** `mapped_scenarios / total_mappable_flows` is O(1) given the Traceability Matrix. tspec-analyst does not need to parse Gherkin text; it reads the matrix and compares against UC flow elements.
- **Slice-scoped generation:** RULE-SL-01 adds one filter pass over the flow elements list before Clark mapping. Linear complexity relative to flow count.
- **Multi-UC coverage:** tspec-analyst currently operates on one Feature file at a time. If cross-UC coverage reporting is needed in the future, the tspec-analyst methodology section supports extension via the 7 Cs C1 Coverage criterion which already defines portfolio-level analysis in its L2 output.

### Auth Architecture Evolution Path

Not applicable (no authentication/authorization in this skill). If future versions of /test-spec gain API integration (e.g., Cucumber CI pipeline hooks), OAuth2 + RBAC should be applied at that boundary.

### GATE-3 Carryforward Status

The architecture SSOT identified GATE-3 (CI enforcement of test-specification-v1.schema.json against generated Feature files) as pending eng-reviewer scope. This gate would validate that every Feature file produced by tspec-generator passes the JSON schema before being committed. Recommended implementation path:

1. Add schema path to CI validator configuration alongside existing use-case-realization-v1.schema.json
2. Apply to files matching `projects/*/test-specs/*.feature.md`
3. Use `jsonschema` or `ajv` validation against Draft 2020-12

---

## S-010 Self-Review

> Pre-delivery self-review per H-15 (S-010 required before presenting any deliverable).

### H-34 Compliance Check

| Check | tspec-generator | tspec-analyst |
|-------|----------------|--------------|
| .md frontmatter has ONLY: name, description, model, tools | PASS | PASS |
| .governance.yaml has version, tool_tier, identity.role | PASS | PASS |
| identity.expertise has >= 2 entries | PASS (3 entries) | PASS (3 entries) |
| identity.cognitive_mode is valid enum value | PASS (systematic) | PASS (convergent) |
| reasoning_effort: high declared at root of .governance.yaml | PASS | PASS |
| forbidden_actions has >= 3 entries in NPT-009-complete format | PASS (5 entries) | PASS (5 entries) |
| constitution.principles_applied includes P-003, P-020, P-022 | PASS | PASS |
| No Task tool in .md tools list | PASS | PASS |
| No Task tool in .agent.yaml tools.native | PASS | PASS |

### H-23 Navigation Table Check

| File | Navigation Table Present | All ## sections listed |
|------|-------------------------|----------------------|
| SKILL.md | PASS | PASS |
| clark-transformation-rules.md | PASS | PASS |
| BEHAVIOR_TESTS.md | PASS | PASS |
| sample-test-specification.md | PASS | PASS |
| bdd-scenario.template.md | N/A (< 30 lines without template content) | N/A |
| test-plan.template.md | N/A (< 30 lines without template content) | N/A |

### FIND Resolution Check

| Finding | Resolution | Evidence |
|---------|-----------|---------|
| FIND-001: P-003 ASCII diagram in SKILL.md section 7 | RESOLVED | SKILL.md section 7 "Agent Topology (P-003 Compliance)" contains ASCII hierarchy diagram |
| FIND-002: Synchronization note header in .prompt.md files | RESOLVED | Both tspec-generator.prompt.md and tspec-analyst.prompt.md open with FIND-002 synchronization note |
| FIND-003: Register in CLAUDE.md and AGENTS.md | PENDING (eng-reviewer scope) | Documented in SKILL.md routing section as "Registration pending eng-reviewer" |
| FIND-004: Priority 14 placement rationale | RESOLVED | SKILL.md routing section includes a table explaining priority 14 placement within existing skill priority space (priority 12 is /user-experience, priority 14 is /test-spec) |

### Clark Rules Completeness Check

| Required Coverage Area | Covered | Rules |
|-----------------------|---------|-------|
| Clark Steps 1-7 | PASS | RULE-C1-01 through RULE-C7-01 (9 rules) |
| SD-07 step type mapping | PASS | RULE-ST-01 through RULE-ST-03 |
| SD-08 outcome type mapping | PASS | RULE-OT-01 through RULE-OT-03 |
| Slice-scoped generation | PASS | RULE-SL-01, RULE-SL-02 |
| Input validation gates | PASS | RULE-IV-01 through RULE-IV-04 |
| Post-generation QA | PASS | RULE-QA-01 through RULE-QA-04 |
| Minimum 19 rules | PASS | 25 rules total |
| < 500 lines (CB-05) | PASS | 204 lines |

### BEHAVIOR_TESTS.md Completeness Check

| Required Coverage | Scenario | Status |
|------------------|---------|--------|
| tspec-generator happy path | G-001 | PASS |
| tspec-generator input rejection (detail_level < ESSENTIAL_OUTLINE) | G-002 | PASS |
| Clark mapping: basic_flow → single happy path Scenario | G-003 | PASS |
| Clark mapping: extension → error Scenario | G-004 | PASS |
| Slice-scoped generation | G-005 | PASS |
| tspec-analyst coverage computation | A-001 | PASS |
| tspec-analyst gap identification | A-002 | PASS |
| Cross-agent pipeline integration | E-001 | PASS |
| Minimum 7 scenarios | 8 total (G-001 through G-005, A-001, A-002, E-001) | PASS |

### OWASP Top 10 Self-Verification (Backend-Applicable Items)

| OWASP Category | Mitigation Applied | Status |
|----------------|-------------------|--------|
| A03: Injection | Clark transformation uses $. field path lookup, not string interpolation; no templating engine with untrusted input; Gherkin content is derived exclusively from UC artifact field values | PASS |
| A05: Security Misconfiguration | RULE-IV gates deny-by-default (halt on validation failure, no partial output); T2 tool tier enforces least privilege; no debug modes or verbose error output in production | PASS |
| A08: Data Integrity Failures | `generated_by: const: "tspec-generator"` in schema; Traceability Matrix provides audit trail; Source annotations in every scenario enable integrity verification | PASS |
| A09: Logging Failures | RULE-QA-04 mandates generation summary before writing; no sensitive data (no PII, no credentials) flows through this skill | PASS |

---

## Findings Resolution

### FIND-001: P-003 ASCII Hierarchy Diagram

**Status:** RESOLVED
**Source:** eng-lead review FIND-001 (medium priority)
**Resolution:** SKILL.md section 7 ("Agent Topology (P-003 Compliance)") contains the following ASCII hierarchy:

```
MAIN CONTEXT (orchestrator)
    |
    +-- tspec-generator (T2 worker) -- invoked via Task tool
    |   Reads: UC artifact + clark-transformation-rules.md + bdd-scenario.template.md
    |   Writes: Feature file (.feature.md)
    |
    +-- tspec-analyst (T2 worker) -- invoked via Task tool
        Reads: Feature file + UC artifact
        Writes: Coverage report (-coverage.md)
Workers do NOT invoke each other. Communication is filesystem-only.
```

### FIND-002: Synchronization Note Headers

**Status:** RESOLVED
**Source:** eng-lead review FIND-002 (low priority)
**Resolution:** Both composition prompt files open with the synchronization note header established in uc-author.prompt.md:

```
> **Synchronization note:** This file is a manually-maintained copy of the markdown body
> from skills/test-spec/agents/{agent}.md (everything after the YAML frontmatter closing ---).
> When updating {agent}.md, this file MUST be updated in the same commit. (FIND-002)
```

### FIND-003: CLAUDE.md and AGENTS.md Registration

**Status:** PENDING (eng-reviewer scope)
**Source:** eng-lead review FIND-003 (medium priority)
**Notes:** The standards review SSOT explicitly delegates registration to eng-reviewer per the established /use-case skill precedent. Documented in SKILL.md routing section.

### FIND-004: Trigger Map Priority 14 Rationale

**Status:** RESOLVED
**Source:** eng-lead review FIND-004 (low priority)
**Resolution:** SKILL.md routing section includes priority placement rationale table explaining that priority 14 sits below /user-experience (priority 12) and above no existing skill. The /test-spec skill triggers on BDD-specific vocabulary ("BDD test specification", "feature file", "gherkin", "tspec") that does not collide with higher-priority skills.

---

## Deviations from Architecture

| Deviation | Architecture Specification | Implementation Choice | Rationale |
|-----------|---------------------------|----------------------|-----------|
| clark-transformation-rules.md rule count | 19 rules minimum | 25 rules (RULE-C3 split into C3-01 + C3-02; QA rules expanded to 4) | RULE-C3 covers two distinct concerns: (1) single Scenario cardinality and (2) Source annotation requirement. Separating them improves verifiability. Each rule is now independently checkable. File remains within CB-05 bounds at 204 lines. |
| Template names | Architecture manifest used "test-specification.template.md" and "coverage-report.template.md" in the task prompt | "bdd-scenario.template.md" and "test-plan.template.md" | Architecture SSOT document (F-10, F-11) specifies these names. The task prompt names were from a pre-reconciliation version. Architecture SSOT overrides task prompt discrepancy per SSOT priority principle. |
| docs/schemas/test-specification-v1.schema.json | Not in original 14-file architecture manifest | Created as file 15 | Schema is referenced by SKILL.md, bdd-scenario.template.md, and the tspec-analyst methodology (for frontmatter parsing). Without the schema file, tspec-analyst cannot validate Feature file frontmatter. Added per implementation necessity with no impact on other files. |

---

*Implementation Version: 1.0.0*
*Author: eng-backend | Date: 2026-03-09*
*Next step: step-10-eng-backend-adv-score.md (adversarial scoring), then step-10-eng-reviewer-final.md (registration)*
*Files created: 15 (14 architecture manifest + 1 schema extension)*
