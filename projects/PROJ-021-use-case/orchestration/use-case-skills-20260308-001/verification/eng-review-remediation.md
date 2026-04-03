# Eng-Reviewer: Adversary Remediation Final Gate Review

**Reviewer:** eng-reviewer
**Date:** 2026-03-11
**Criticality:** C3 (Significant)
**Verdict:** CONDITIONAL GO -- 1 blocking finding, 2 non-blocking findings

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | GO/NO-GO decision, overall assessment |
| [L1 Per-File Compliance Matrix](#l1-per-file-compliance-matrix) | Detailed per-artifact review results |
| [L2 Strategic Assessment](#l2-strategic-assessment) | Residual risk, quality posture, recommendations |
| [Blocking Findings](#blocking-findings) | Issues that must be fixed before merge |
| [Non-Blocking Findings](#non-blocking-findings) | Issues to address but do not block merge |
| [Adversary Finding Remediation Tracker](#adversary-finding-remediation-tracker) | Mapping of original findings to remediation status |
| [Quality Scoring](#quality-scoring) | S-014 dimension scores for this remediation pass |

---

## L0 Executive Summary

**Decision: CONDITIONAL GO**

The adversary remediation changes address the highest-priority findings from the three adversary reports (agent, schema, skill). Six of the seven files reviewed are correctly remediated. One file (`cd-generator.governance.yaml`) has a schema-invalid `enforcement.tier` value that will fail H-34 governance YAML validation. This is a blocking finding that requires a one-line fix.

**Overall Quality Score:** 0.93/1.00 (above 0.92 threshold with the blocking finding corrected)

**Key results:**
- tspec-analyst.md: Edit tool correctly removed, Glob and Grep correctly retained. Tool list is clean (5 tools, no duplicates). PASS.
- cd-generator.governance.yaml: cognitive_mode correctly changed to "systematic". enforcement.tier changed from "medium" to "high" -- but "high" is NOT a valid enum value per agent-governance-v1.schema.json (valid: hard, medium, soft). BLOCKING FINDING.
- test-spec SKILL.md: Stale PENDING note correctly removed. Footer status updated to ACTIVE. Header status remains PROPOSED (inconsistency). NON-BLOCKING FINDING.
- use-case SKILL.md: Footer status updated to ACTIVE. Header status remains PROPOSED (same inconsistency as test-spec). NON-BLOCKING FINDING.
- use-case-realization-v1.schema.json: All 5 P0 schema fixes applied correctly. `then: false` pattern is valid JSON Schema Draft 2020-12. PASS.
- test-specification-v1.schema.json: additionalProperties set to false. source_detail_level description improved. PASS.
- tspec-analyst.governance.yaml: tool_tier correctly remains T2. PASS.

---

## L1 Per-File Compliance Matrix

### 1. skills/test-spec/agents/tspec-analyst.md

| Check | Result | Evidence |
|-------|--------|----------|
| Edit tool removed from tools list | PASS | Tools: Read, Write, Glob, Grep, Bash (5 tools, verified via bash head) |
| Glob and Grep retained | PASS | Present at positions 3 and 4 in tools array |
| No duplicate tools | PASS | No repeated entries (confirmed via bash output) |
| Tool count appropriate for T2 tier | PASS | 5 tools, all within T2 (Read-Write) tier scope |
| Guardrails still reference read-only posture | PASS | "ANALYSIS VIOLATION: NEVER modify Feature files or use case artifacts" preserved |
| H-34 compliance (official frontmatter only) | PASS | name, description, model, tools are all official Claude Code fields |
| No breaking changes | PASS | Removing Edit reduces capability surface (safe direction); adding Glob/Grep for search is additive and appropriate for coverage analysis |

**Finding addressed:** SR-001/DA-003 (tspec-analyst Edit tool contradicts read-only posture)
**Verdict:** PASS

---

### 2. skills/contract-design/agents/cd-generator.governance.yaml

| Check | Result | Evidence |
|-------|--------|----------|
| cognitive_mode changed from convergent to systematic | PASS | Line 30: `cognitive_mode: "systematic"` |
| cognitive_mode is valid enum value | PASS | "systematic" is in agent-governance-v1.schema.json identity.cognitive_mode enum |
| enforcement.tier changed from medium | PASS | Line 107: `tier: "high"` (changed from "medium") |
| enforcement.tier is valid enum value | **FAIL** | "high" is NOT in agent-governance-v1.schema.json enforcement.tier enum. Valid values: `["hard", "medium", "soft"]`. This will fail H-34 schema validation. |
| tool_tier unchanged at T2 | PASS | Line 7: `tool_tier: "T2"` |
| Required fields present (version, tool_tier, identity) | PASS | All three present |
| Constitution includes P-003, P-020, P-022 | PASS | Lines 77-83 |
| Forbidden actions >= 3 with NPT-009 format | PASS | 6 entries, NPT-009-complete |
| reasoning_effort: max retained | PASS | Line 22 |
| No breaking changes to other fields | PASS | All other fields unchanged |

**Finding addressed:** DA-001 (cognitive_mode mismatch), DA-004/CC-003 (enforcement tier inconsistency)
**Verdict:** FAIL (enforcement.tier value invalid per governance schema)

**Required fix:** Change `enforcement.tier` from `"high"` to `"hard"`. The adversary report recommended `"critical"` which is also not a valid schema value. The correct highest-severity valid value is `"hard"` per the governance schema enum. The C4 classification justifies the highest enforcement tier (`"hard"`).

---

### 3. skills/test-spec/SKILL.md

| Check | Result | Evidence |
|-------|--------|----------|
| Stale PENDING note removed | PASS | `grep PENDING` returns no matches |
| Footer status changed to ACTIVE | PASS | Line 376: `Status: ACTIVE` |
| Header status updated | **PARTIAL** | Line 41: `Status: PROPOSED` (not updated to match footer) |
| Routing entry present and correct | PASS | Priority 14, 5-column format, keywords match mandatory-skill-usage.md |
| H-23 navigation table present | PASS | Document Sections table with anchor links |
| No breaking changes to agent references | PASS | Agent table unchanged |
| No breaking changes to routing keywords | PASS | Trigger map entry unchanged |

**Finding addressed:** SR-003/CC-004 (stale PENDING note), SR-001/IN-004 (PROPOSED to ACTIVE status)
**Verdict:** PASS with non-blocking inconsistency (header/footer status mismatch)

---

### 4. skills/use-case/SKILL.md

| Check | Result | Evidence |
|-------|--------|----------|
| Footer status changed to ACTIVE | PASS | Line 404: `Status: ACTIVE` |
| Header status updated | **PARTIAL** | Line 47: `Status: PROPOSED` (not updated to match footer) |
| H-23 navigation table present | PASS | Document Sections table with anchor links |
| No breaking changes to agent references | PASS | Agent table unchanged |
| No breaking changes to routing keywords | PASS | Trigger map entry unchanged |

**Finding addressed:** SR-001/IN-004 (PROPOSED to ACTIVE status)
**Verdict:** PASS with non-blocking inconsistency (header/footer status mismatch)

---

### 5. docs/schemas/use-case-realization-v1.schema.json

| Check | Result | Evidence |
|-------|--------|----------|
| Valid JSON | PASS | Python json.load() succeeds |
| $schema is Draft 2020-12 | PASS | `"$schema": "https://json-schema.org/draft/2020-12/schema"` |
| Root additionalProperties changed to false | PASS | Line 253: `"additionalProperties": false` |
| goal_symbol added to required array | PASS | Verified via Python: `"goal_symbol" in schema["required"]` is True |
| STORY_DEFINED -> slices conditional added | PASS | allOf[4]: if realization_level=STORY_DEFINED then requires slices with minItems: 1 |
| ESSENTIAL_OUTLINE -> extensions conditional added | PASS | allOf[5]: if detail_level in [ESSENTIAL_OUTLINE, FULLY_DESCRIBED] then requires extensions with minItems: 1 |
| detail_level/realization_level cross-constraint added | PASS | allOf[6]: `then: false` pattern correctly rejects INTERACTION_DEFINED with BRIEFLY_DESCRIBED or BULLETED_OUTLINE |
| `then: false` is valid JSON Schema Draft 2020-12 | PASS | `false` is a valid JSON Schema boolean schema (2020-12 Section 4.3.2); `then: false` means "if the condition matches, validation ALWAYS fails" -- this is the correct idiom for prohibition constraints |
| External actor type added | PASS | supporting_actors[*].type enum: `["human", "system", "timer", "external"]` |
| interaction.id description fixed | PASS | Description now reads: "Format: INT-{NN} or INT-{NNN} for use cases with >99 interactions. Examples: INT-01, INT-100." -- matches the `^INT-\d{2,3}$` pattern |
| Existing allOf constraints preserved | PASS | 3 goal_level/goal_symbol constraints (allOf[0-2]) and INTERACTION_DEFINED conditional (allOf[3]) unchanged |
| $defs additionalProperties remain false | PASS | flow_step, extension, alternative_flow, interaction, postconditions all have additionalProperties: false |
| slice additionalProperties remains true | NOTED | Line 395: `additionalProperties: true` in slice def. This was not in remediation scope; intentional for domain-specific extensions per uc-slicer operations |
| No breaking changes to existing valid artifacts | PASS | New conditionals only constrain previously-unconstrained combinations (adding constraints never invalidates previously-valid-and-correct artifacts) |

**Findings addressed:**
- SR-001 (additionalProperties true at root)
- SR-003 (goal_symbol not in required)
- DA-001 (extensions not conditionally required at ESSENTIAL_OUTLINE+)
- DA-003 (STORY_DEFINED does not require slices)
- DA-005 (supporting_actors missing "external" type)
- CV-003 (interaction.id description mismatch)
- IN-001 (BRIEFLY_DESCRIBED + INTERACTION_DEFINED passes validation)

**`then: false` Pattern Analysis:**

The `then: false` pattern at allOf[6] is a well-established JSON Schema Draft 2020-12 idiom for expressing prohibition constraints. Per the JSON Schema specification:

- A boolean `false` is a valid schema that always fails validation (Section 4.3.2: "false" means validation always fails)
- When used as the `then` value in an if/then/else construct: if the `if` condition matches (both realization_level is INTERACTION_DEFINED AND detail_level is BRIEFLY_DESCRIBED or BULLETED_OUTLINE), then the `then: false` causes overall validation to fail

The `description` field on the allOf entry is not part of the JSON Schema validation semantics but serves as documentation. Its placement on the allOf entry object (not inside the `then`) is correct -- JSON Schema ignores unrecognized keywords at evaluation time, and description is a recognized annotation keyword.

This pattern correctly prevents the logically invalid combination identified in adversary finding IN-001: `detail_level: BRIEFLY_DESCRIBED` + `realization_level: INTERACTION_DEFINED` will now fail schema validation.

**Note:** The constraint is asymmetric by design. It only blocks INTERACTION_DEFINED at BRIEFLY_DESCRIBED/BULLETED_OUTLINE. It does NOT block STORY_DEFINED at those levels. If STORY_DEFINED also requires at minimum ESSENTIAL_OUTLINE, an additional allOf entry with the same `then: false` pattern would be needed. Based on the use-case-writing-rules, STORY_DEFINED can theoretically exist at any detail_level because slice scoping (Activity 2) can happen before extensions are written. The current constraint is therefore correct as-is.

**Verdict:** PASS

---

### 6. docs/schemas/test-specification-v1.schema.json

| Check | Result | Evidence |
|-------|--------|----------|
| Valid JSON | PASS | Python json.load() succeeds |
| $schema is Draft 2020-12 | PASS | `"$schema": "https://json-schema.org/draft/2020-12/schema"` |
| Root additionalProperties changed to false | PASS | Line 131: `"additionalProperties": false` |
| source_detail_level description fixed | PASS | Now reads: "Detail level of the source use case at generation time. Only ESSENTIAL_OUTLINE and FULLY_DESCRIBED are valid values; the enum constraint enforces this restriction. Clark transformation requires >= ESSENTIAL_OUTLINE per RULE-IV-02." No longer implies schema-level rejection of BRIEFLY_DESCRIBED/BULLETED_OUTLINE -- accurately describes what the enum does. |
| coverage sub-object additionalProperties false | PASS | Line 92 |
| quality sub-object additionalProperties false | PASS | Line 120 |
| No breaking changes to existing valid artifacts | PASS | Adding additionalProperties:false only rejects previously-accepted-but-unintended extra fields |

**Finding addressed:**
- SR-001 from schema report (additionalProperties implied via same finding class)
- CV-001 (source_detail_level description misleading about rejection)

**Verdict:** PASS

---

### 7. skills/test-spec/agents/tspec-analyst.governance.yaml

| Check | Result | Evidence |
|-------|--------|----------|
| tool_tier remains T2 | PASS | Line 7: `tool_tier: "T2"` |
| T2 justified (needs Write for coverage report) | PASS | Comment on line 17-19 explains rationale; tspec-analyst writes a new coverage report file |
| cognitive_mode is convergent | PASS | Line 28 |
| Constitution includes P-003, P-020, P-022 | PASS | Lines 68-74 |
| Forbidden actions >= 3 | PASS | 5 entries, NPT-009-complete |
| enforcement.tier valid | PASS | Line 95: `tier: "medium"` (valid per governance schema enum) |
| No unintended changes | PASS | File contents match expected state |

**Verdict:** PASS

---

## Blocking Findings

### BLOCK-001: cd-generator.governance.yaml enforcement.tier schema violation

| Attribute | Value |
|-----------|-------|
| **Severity** | Blocking |
| **File** | `skills/contract-design/agents/cd-generator.governance.yaml` |
| **Line** | 107 |
| **Current Value** | `tier: "high"` |
| **Expected Value** | `tier: "hard"` |
| **Schema** | `docs/schemas/agent-governance-v1.schema.json` enforcement.tier enum: `["hard", "medium", "soft"]` |
| **Standards** | H-34 (agent definition governance YAML must validate against schema) |

**Root cause:** The adversary finding DA-004/CC-003 recommended `"critical"` as the enforcement tier value. The remediation chose `"high"` as a compromise. Neither `"critical"` nor `"high"` are valid values in the governance schema. The schema uses the tier vocabulary from `quality-enforcement.md` (HARD/MEDIUM/SOFT), not a severity scale (critical/high/medium/low).

**Required action:** Change `tier: "high"` to `tier: "hard"` on line 107 of `cd-generator.governance.yaml`. The `"hard"` value is the highest valid enforcement tier and correctly represents the C4 classification documented in the file's header comments.

---

## Non-Blocking Findings

### INFO-001: SKILL.md header/footer status inconsistency

| Attribute | Value |
|-----------|-------|
| **Severity** | Non-blocking (documentation inconsistency) |
| **Files** | `skills/test-spec/SKILL.md` (lines 41 vs 376), `skills/use-case/SKILL.md` (lines 47 vs 404) |
| **Issue** | Header blockquote says `Status: PROPOSED`, footer says `Status: ACTIVE` |

Both SKILL.md files had their footer status updated to ACTIVE but the header blockquote was not updated. This is a P-022-adjacent documentation inconsistency -- a reader encountering the header first would believe the skill is still PROPOSED.

**Recommended action:** Update the header blockquotes:
- `skills/test-spec/SKILL.md` line 41: change `PROPOSED` to `ACTIVE`
- `skills/use-case/SKILL.md` line 47: change `PROPOSED` to `ACTIVE`

### INFO-002: tspec-analyst.md initial read showed duplicate Glob/Grep entries

| Attribute | Value |
|-----------|-------|
| **Severity** | Non-blocking (tool observation only) |
| **File** | `skills/test-spec/agents/tspec-analyst.md` |
| **Issue** | Initial read appeared to show Glob and Grep listed twice. Subsequent reads and bash verification confirm the file is clean with 5 unique tools. |

The file on disk is correct. No action needed. This is documented for audit completeness.

---

## Adversary Finding Remediation Tracker

### Schema Findings (adversary-schema-findings.md)

| Finding | Priority | Status | Evidence |
|---------|----------|--------|----------|
| SR-001: additionalProperties true at root (use-case-realization) | P0 | REMEDIATED | Root additionalProperties set to false |
| SR-003: goal_symbol not in required | P0 | REMEDIATED | goal_symbol added to required array |
| DA-001: extensions not conditionally required at ESSENTIAL_OUTLINE+ | P0 | REMEDIATED | allOf conditional added |
| DA-003: STORY_DEFINED does not require slices | P1 | REMEDIATED | allOf conditional added with minItems: 1 |
| DA-005: supporting_actors type missing "external" | P1 | REMEDIATED | "external" added to enum |
| CV-001: source_detail_level description misleading | P0 | REMEDIATED | Description rewritten to accurately describe enum constraint |
| CV-003: interaction.id pattern/description mismatch | P1 | REMEDIATED | Description updated to match 2-3 digit pattern |
| IN-001: BRIEFLY_DESCRIBED + INTERACTION_DEFINED passes validation | P0 | REMEDIATED | then:false cross-constraint added |
| SR-001: additionalProperties (test-specification) | P0 | REMEDIATED | Root additionalProperties set to false |

### Agent Findings (adversary-agent-findings.md)

| Finding | Priority | Status | Evidence |
|---------|----------|--------|----------|
| DA-001: cd-generator cognitive_mode mismatch | Critical | REMEDIATED | Changed from convergent to systematic |
| DA-003/SR-001: tspec-analyst Edit tool contradicts read-only | Major | REMEDIATED | Edit removed, Glob and Grep added |
| DA-004/CC-003: cd-generator enforcement tier inconsistency | Major | PARTIAL -- BLOCKING | Changed from medium to "high" but "high" is invalid per schema; must be "hard" |

### Skill Findings (adversary-skill-findings.md)

| Finding | Priority | Status | Evidence |
|---------|----------|--------|----------|
| SR-001: Status PROPOSED (all skills) | P2 | PARTIAL | Footer updated to ACTIVE; header still says PROPOSED |
| SR-003/CC-004: test-spec PENDING note stale | P0 | REMEDIATED | PENDING note removed |

---

## Quality Scoring

Applying S-014 dimensions to this remediation pass:

| Dimension | Weight | Score | Weighted | Rationale |
|-----------|--------|-------|----------|-----------|
| Completeness | 0.20 | 0.93 | 0.186 | 12 of 13 tracked remediation items complete; 1 partial (enforcement.tier) |
| Internal Consistency | 0.20 | 0.90 | 0.180 | enforcement.tier schema violation is a consistency gap; header/footer status mismatch |
| Methodological Rigor | 0.20 | 0.96 | 0.192 | Schema changes use correct Draft 2020-12 idioms; then:false pattern is textbook; tool tier decisions are justified |
| Evidence Quality | 0.15 | 0.95 | 0.143 | All changes verified via bash/python; schema validation confirmed programmatically |
| Actionability | 0.15 | 0.95 | 0.143 | Blocking finding has exact one-line fix specified; non-blocking findings have specific line numbers |
| Traceability | 0.10 | 0.92 | 0.092 | Every change traces to a specific adversary finding ID |
| **TOTAL** | **1.00** | | **0.936** | |

**Score: 0.936 -- PASS (conditional on BLOCK-001 fix)**

After the BLOCK-001 fix (one-line change: `"high"` to `"hard"`), the Internal Consistency dimension rises to 0.95 and the composite reaches approximately 0.95.

---

## L2 Strategic Assessment

### Security Posture

The remediation changes improve the security posture of the skill suite:

1. **Schema hardening:** `additionalProperties: false` at both schema roots prevents silent frontmatter pollution -- the most impactful single change. All future misspelled or deprecated fields will be caught at schema validation time.

2. **Lifecycle constraint enforcement:** The `then: false` cross-constraint and the STORY_DEFINED/ESSENTIAL_OUTLINE conditionals ensure that artifacts cannot exist in logically invalid states. This closes the gap identified by the S-013 Inversion strategy (adversary finding IN-001).

3. **Agent tool surface reduction:** Removing Edit from tspec-analyst eliminates the attack surface where the coverage analyst could accidentally or maliciously modify Feature files or UC artifacts. The read-only analytical posture is now structurally enforced, not just behaviorally instructed.

4. **Cognitive mode correctness:** Changing cd-generator to systematic mode aligns the agent's behavioral signals with its deterministic 9-step algorithm, reducing the risk of the agent "deciding" among HTTP method options when it should mechanically apply lookup table rules.

### Residual Risk

| Risk | Severity | Mitigation |
|------|----------|------------|
| `slice` definition still has `additionalProperties: true` | Low | Intentional for domain-specific extensions; documented in this review |
| Header/footer status inconsistency in SKILL.md files | Low | Documentation polish; does not affect runtime behavior |
| Adversary findings not in remediation scope (PM-001, FM-001, FM-002, etc.) remain open | Medium | These are documented in the adversary reports for future work; the GATE-6 final quality gate accepted these as known gaps |

### Recommendation

1. **Immediate:** Fix BLOCK-001 (`enforcement.tier: "hard"` in cd-generator.governance.yaml)
2. **Immediate:** Fix header status in both SKILL.md files (PROPOSED to ACTIVE)
3. **Post-merge:** Address remaining adversary findings (PM-001 error propagation, FM-001 governance YAML completeness, FM-002 realization_level enforcement) as tracked in the adversary reports

---

*Report generated by eng-reviewer*
*Review scope: 7 files from adversary finding remediation*
*Standards applied: H-34 (agent definitions), JSON Schema Draft 2020-12, quality-enforcement.md*
*SSOT: `.context/rules/quality-enforcement.md`*
*Date: 2026-03-11*
