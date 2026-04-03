# FM-001 Implementation Summary: Governance YAML Behavioral Sync

**Implementing Agent:** eng-backend
**Finding:** FM-001 -- governance YAML `input_validation` entries missing loading prerequisites for cross-reference constraints
**Source Analysis:** `pm001-fm001-fm002-analysis.md` (Option A recommendation: update existing entries with prerequisite wording)
**Date:** 2026-03-11
**Scope:** All 6 PROJ-021 agent governance YAMLs

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Summary](#l0-summary) | What changed, security posture |
| [L1 Technical Detail](#l1-technical-detail) | Per-agent changes with boundary rule classification |
| [L2 Strategic Implications](#l2-strategic-implications) | Systemic implications, boundary rule adoption |
| [Boundary Rule Applied](#boundary-rule-applied) | Decision framework used |
| [OWASP Verification](#owasp-verification) | OWASP Top 10 checklist for this change set |

---

## L0 Summary

**What was implemented:** Governance YAML `input_validation` entries across all 6 PROJ-021 agent definitions have been updated to include explicit loading prerequisites for cross-reference constraints. The primary FM-001 target (cd-generator entry 5) has been corrected from an ambiguous "cross-reference validation" string to a self-contained entry specifying what must be loaded before the check can execute.

**Additional coverage:** The analysis identified related gaps across the other 5 agents that follow the same pattern -- cross-reference or semantic constraints without loading prerequisites. All have been addressed in the same pass.

**Security controls applied:**
- A01 (Broken Access Control): n/a -- documentation change only
- A03 (Injection): No user input introduced into governance YAML
- A08 (Data Integrity): Governance YAML entries now carry sufficient context for CI gate operators to implement checks correctly, reducing the risk of false-pass conditions at L3/L5 enforcement layers

**Key security finding:** The FM-001 pattern (a constraint documented without its prerequisite) creates a false-pass risk at automated enforcement layers. A CI gate that reads the governance YAML and attempts to execute cross-reference validation without knowing it must load the full artifact will silently pass on partial input. The wording changes make the prerequisite machine-readable.

**Files modified:**
- `skills/use-case/agents/uc-author.governance.yaml`
- `skills/use-case/agents/uc-slicer.governance.yaml`
- `skills/test-spec/agents/tspec-generator.governance.yaml`
- `skills/test-spec/agents/tspec-analyst.governance.yaml`
- `skills/contract-design/agents/cd-generator.governance.yaml`
- `skills/contract-design/agents/cd-validator.governance.yaml`

**OWASP categories addressed:** A08 (Data Integrity -- governance artifacts now carry accurate prerequisite information)

**Remaining risk areas:** The boundary rule applied here (structural vs. cross-reference vs. behavioral) is not yet formally documented in `agent-development-standards.md`. This leaves future agent authors without an authoritative reference for how to classify constraints. This is a documentation gap, not a runtime gap -- existing behavioral constraints in the .md files remain authoritative.

---

## L1 Technical Detail

### Boundary Rule Applied

Per the FM-001 analysis recommendation (Option A), all changes apply the following boundary classification:

| Constraint Type | Location | Rationale |
|----------------|----------|-----------|
| Structural (field existence, format, type) | governance YAML `input_validation` | Deterministic; CI-executable without LLM |
| Cross-reference (field A references field B) | governance YAML WITH explicit loading prerequisite | Requires LLM execution but must be declared with prerequisites for CI gate awareness |
| Behavioral (HOW to execute a check) | .md only | Not machine-readable; LLM-driven execution |

The loading prerequisite format used throughout: `(cross-reference prerequisite: {what must be loaded} before {what check can execute})`

---

### Agent 1: uc-author.governance.yaml

**Gap identified:** Two gaps in addition to the general loading prerequisite pattern:
1. The "If elaborating existing artifact" entry did not specify that the full file must be loaded first
2. No entry existed for the rejection artifact check-on-receive (PM-001 behavioral sync)

**Changes made:**

| # | Change Type | Before | After |
|---|------------|--------|-------|
| 1 | Precision: loading prerequisite added | `"If elaborating existing artifact: file must exist and contain valid YAML frontmatter with $.work_type = USE_CASE"` | Same check with explicit `(cross-reference prerequisite: full file must be loaded before field check can execute)` |
| 2 | Added: detail_level field check | Missing | New entry: `"If elaborating existing artifact: $.detail_level must be present and set to a recognized Jacobson UC 2.0 level"` |
| 3 | Added: rejection artifact check | Missing | New entry: `"If session context includes artifact_path with a corresponding {artifact_path}-rejection.yaml: load the rejection artifact to determine required_level and missing_elements before selecting target_detail_level"` |

**Boundary classification:** All 3 additions are cross-reference or structural checks. The rejection artifact check is cross-reference (file A's path determines file B's expected path; both must be considered). The behavioral instructions for how uc-author responds to rejection artifacts remain in the .md `session_context.on_receive`.

---

### Agent 2: uc-slicer.governance.yaml

**Gap identified:** Three gaps:
1. Loading prerequisite missing from work_type check
2. `$.extensions[]` non-empty requirement missing from `input_validation` (present in .md `<input>` section and `<guardrails>` but absent from governance YAML)
3. `realization_level_must_match_populated_blocks` output_filtering entry did not reference the enforcement mechanism (FM-002 partial fix)
4. Post-completion checks missing FM-002 CLI validation entry and PM-001 rejection artifact verification

**Changes made:**

| # | Change Type | Before | After |
|---|------------|--------|-------|
| 1 | Precision: loading prerequisite | `"Input artifact must exist and contain valid YAML frontmatter with $.work_type = USE_CASE"` | Explicit full-file load prerequisite added |
| 2 | Precision: detail_level prerequisite | `"Input artifact $.detail_level must be >= ESSENTIAL_OUTLINE..."` | Added `"requires full artifact load to read $.detail_level"` |
| 3 | Added: missing extensions check | Not present | `"Input artifact must have $.extensions[] non-empty (at least 1 extension required); reject if $.extensions is absent or empty with actionable error directing to uc-author"` |
| 4 | Precision: output_filtering enforcement | `"realization_level_must_match_populated_blocks"` | Appended `"(enforced by allOf schema constraint + jerry ast validate post-creation check)"` |
| 5 | Added: post_completion_checks (FM-002) | Missing | `"verify_realization_level_allOf_constraint_via_jerry_ast_validate"` |
| 6 | Added: post_completion_checks (PM-001) | Missing | `"verify_rejection_artifact_written_on_detail_level_rejection"` |
| 7 | Added: session_context.on_send (PM-001) | Missing | Rejection artifact write step with required fields (current_level, required_level, missing_elements, recommended_action) |

**Boundary classification:** Item 3 (extensions check) is a structural constraint -- it validates field existence. Items 4-7 add enforcement metadata and behavioral sync to the success/rejection path. The rejection artifact _content_ is behavioral (what to put in the file); the _existence_ check is structural.

---

### Agent 3: tspec-generator.governance.yaml

**Gap identified:** Two gaps:
1. Loading prerequisite missing from work_type check
2. Slice-scoped generation cross-reference check missing: `.md` Layer 2 rejects if `slice_id` is specified and `$.realization_level < STORY_DEFINED`, but this cross-reference constraint had no governance YAML entry
3. `$.type` field enumeration was generic ("with $.type field") -- tightened to list valid values

**Changes made:**

| # | Change Type | Before | After |
|---|------------|--------|-------|
| 1 | Precision: loading prerequisite | `"Input artifact must exist and contain valid YAML frontmatter with $.work_type = USE_CASE"` | Full file load prerequisite added |
| 2 | Precision: type field enumeration | `"each with $.type field"` | `"each with $.type field populated (actor_action, system_response, or validation)"` |
| 3 | Added: slice_id cross-reference check | Not present | `"If slice_id is specified: load $.slices from the full artifact and verify $.realization_level >= STORY_DEFINED before accepting input (cross-reference prerequisite: full UC artifact must be loaded to resolve slice steps_included from $.slices[slice_id])"` |

**Boundary classification:** Item 3 is a cross-reference check with explicit loading prerequisite. Item 2 is a structural precision improvement (adds the valid enumeration values to the type field check).

---

### Agent 4: tspec-analyst.governance.yaml

**Gap identified:** Three gaps:
1. Loading prerequisite missing -- the coverage analysis requires both files, but the governance YAML did not state this mutual prerequisite
2. Feature file `source_use_case` frontmatter field check missing (needed for locating source artifact when path not explicit)
3. `$.extensions` warning condition was a single merged entry -- split to separate structural from warning behavior

**Changes made:**

| # | Change Type | Before | After |
|---|------------|--------|-------|
| 1 | Added: Feature file frontmatter check | Not present | `"Feature file YAML frontmatter must contain source_use_case field (cross-reference prerequisite: used to locate and validate source artifact when artifact_path is not explicitly provided)"` |
| 2 | Precision: UC artifact loading prerequisite | `"Source use case artifact must exist and contain valid YAML frontmatter with $.work_type = USE_CASE"` | Full file load prerequisite added |
| 3 | Precision: basic_flow reject vs. warn | `"Source use case must have $.basic_flow and $.extensions (minimum for coverage baseline)"` | Split into two entries: basic_flow as REJECT, extensions as WARN, each with their own action |
| 4 | Added: mutual prerequisite entry | Not present | `"Both Feature file and source use case artifact must be loaded before any coverage computation begins (mutual prerequisite: coverage cross-reference requires both inputs to be in scope simultaneously)"` |

**Boundary classification:** Items 1 and 4 are cross-reference constraints (one file's field determines how the other file is located/used). Items 2 and 3 are structural/precision improvements.

---

### Agent 5: cd-generator.governance.yaml (Primary FM-001 Target)

**Gap identified:** This is the primary FM-001 subject. Entry 5 ("Each $.interactions[*].source_step must reference an existing step...") had D=8 detection difficulty because it omitted the loading prerequisite: the full UC artifact must be loaded (not just the interactions block) to execute this check.

**Changes made:**

| # | Change Type | Before | After |
|---|------------|--------|-------|
| 1 | Precision: loading prerequisite (work_type) | `"Input artifact must exist and contain valid YAML frontmatter with $.work_type = USE_CASE"` | Full file load prerequisite added |
| 2 | FM-001 fix: cross-reference entry 5 | `"Each $.interactions[*].source_step must reference an existing step in the flow identified by $.interactions[*].source_flow (cross-reference validation)"` | `"Full UC artifact must be loaded (not just the interactions block) before executing cross-reference validation: each $.interactions[*].source_step must reference an existing step in the flow identified by $.interactions[*].source_flow (loading prerequisite: $.basic_flow, $.alternative_flows, and $.extensions must all be in scope to resolve source_flow references)"` |
| 3 | Added: extensions warn entry | Not present | `"$.extensions must be readable for error response mapping (warn if absent; absence means no 4xx/5xx responses will be generated)"` |
| 4 | Added: boundary rule comment | Not present | 3-line comment block documenting the structural vs. cross-reference vs. behavioral classification rule |

**FMEA impact (per analysis recommendation):** D decreases from 8 to approximately 5. The loading prerequisite is now visible to CI gate operators reading the governance YAML. RPN projection: 9 x 5 x 5 = 225 (down from 360), a 37.5% reduction. This matches the analysis prediction exactly.

**Boundary classification:** Item 2 is the direct FM-001 fix -- a cross-reference constraint made self-contained by explicit loading prerequisite. Item 3 is a new structural advisory entry (warn-level check that mirrors the .md's WARN behavior for absent extensions). Item 4 is a comment documenting the boundary rule for future maintainers.

---

### Agent 6: cd-validator.governance.yaml

**Gap identified:** Three gaps:
1. The governance YAML had a merged "Source use case artifact must exist and contain valid YAML frontmatter with $.interactions" -- this combined a structural check with a field-existence check without specifying what to load
2. No entry for the mutual prerequisite (both files must be loaded before traceability steps execute)
3. No entry for the `x-source-use-case` cross-reference check (the contract should reference the same UC as was provided)

**Changes made:**

| # | Change Type | Before | After |
|---|------------|--------|-------|
| 1 | Precision: contract structural check | `"Contract file must exist at specified path and contain valid YAML"` | Split into: (a) YAML parse check with `(structural check; no loading prerequisite)` annotation, (b) openapi field version check |
| 2 | Precision: UC artifact loading prerequisite | `"Source use case artifact must exist and contain valid YAML frontmatter with $.interactions"` | Full file load prerequisite added; specifies which validation steps depend on it (2, 5, 8, 9) |
| 3 | Added: mutual prerequisite | Not present | `"Both contract file and source use case artifact must be loaded before traceability validation begins (mutual prerequisite: Step 2 path completeness check cross-references contract operations against UC $.interactions[*].actor_role = consumer)"` |
| 4 | Added: x-source-use-case cross-reference | Not present | `"Contract info.x-source-use-case must reference a UC artifact that matches the source use case artifact provided (cross-reference check: load info section, then verify x-source-use-case value matches the loaded artifact's $.id field)"` |
| 5 | Added: boundary rule comment | Not present | 2-line comment documenting structural vs. cross-reference classification |

**Boundary classification:** Items 3 and 4 are cross-reference constraints with explicit loading prerequisites. Items 1 and 2 are structural precision improvements that annotate which checks require full-file loading vs. YAML-parse-only checks.

---

## L2 Strategic Implications

### Backend Security Posture Assessment

The changes made in this implementation address a specific class of governance artifact integrity gap: constraints documented without their execution prerequisites. From a backend security perspective, this matters because:

1. **False-pass risk at L3/L5 enforcement layers:** A CI gate reading governance YAML entries is an automated validator. Without explicit loading prerequisites, a correctly-implemented CI tool could silently pass validation for inputs that are semantically invalid. The wording changes introduce machine-readable prerequisite declarations that CI tool authors can act on.

2. **Defense-in-depth integrity:** The 3-layer validation architecture (schema structural check -> agent semantic check -> downstream rejection) depends on each layer having complete information about what to check. Layer 2 (agent semantic checks in .md) was already complete. This implementation closes the gap at Layer 1.5 (governance YAML, which sits between the fully automated Layer 1 and the LLM-interpreted Layer 2).

### Boundary Rule as a MEDIUM Standard

The boundary rule applied throughout this implementation (structural vs. cross-reference vs. behavioral, with loading prerequisites for cross-reference entries) is a documented principle from the FM-001 analysis. It is not yet formalized in `agent-development-standards.md`.

**Recommendation for future work:** Adopt the boundary rule as a MEDIUM standard under the "Agent Definition Schema" section of `agent-development-standards.md`. This would:
- Prevent future authors from creating cross-reference constraints without loading prerequisites
- Provide a testable criterion for CI gate implementation (entries with "cross-reference" in the text require a loading prerequisite)
- Create a consistent vocabulary across all governance YAMLs (the comment block added to cd-generator and cd-validator is a preview of what this standard would mandate)

This is explicitly flagged as an L2 recommendation; it is not in scope for this FM-001 implementation pass.

### Dependency Risk Landscape

The governance YAML changes are documentation-only modifications. They introduce no runtime code dependencies and carry zero dependency risk. The changes are backward-compatible with:
- `docs/schemas/agent-governance-v1.schema.json` -- no schema changes required; `additionalProperties: true` on `guardrails.input_validation` accepts extended string entries
- Existing CI validation gates -- the changes add content to existing string array entries, not new fields
- Agent runtime behavior -- LLM behavioral instructions remain in .md files; governance YAML changes are declarations, not instructions

### Scalability Considerations

The loading prerequisite pattern introduced here scales linearly with the number of cross-reference constraints added in future agent definitions. The pattern is self-contained within each governance YAML entry; no centralized registry or schema extension is required to support it. At the current scale of 6 agents, the per-entry approach is appropriate. If the agent count grows to 20+, a dedicated `semantic_validation` block (Option C from the FM-001 analysis) would provide better structural separation and CI tooling clarity.

### Evolution Path

Current state (post-implementation): Cross-reference constraints have explicit loading prerequisites declared inline in governance YAML string entries.

Near-term (recommended): Adopt the boundary rule as a MEDIUM standard in `agent-development-standards.md` with a standardized inline format for prerequisite declarations.

Medium-term (conditional on scale): If agent count reaches 20+ or CI tooling for governance YAML validation is implemented, evaluate Option C from FM-001 analysis -- a dedicated `semantic_validation` block in the governance YAML schema that separates structural from semantic checks and carries prerequisites as structured fields rather than free-text annotations.

---

## Boundary Rule Applied

The following classification was applied consistently across all 6 agents:

```
Structural constraint:
  → governance YAML input_validation
  → No loading prerequisite needed
  → Annotation: "(structural check; no loading prerequisite)" when clarity helps

Cross-reference constraint (field A references field B in same or different file):
  → governance YAML input_validation WITH explicit loading prerequisite
  → Format: "(cross-reference prerequisite: {what must be loaded} before {what check executes})"
  → Both files stated when mutual prerequisite applies

Behavioral constraint (HOW to execute, WHAT interpretation to apply, contextual quality):
  → .md guardrails / methodology only
  → NOT added to governance YAML
```

---

## OWASP Verification

Self-verification against OWASP Top 10 for this change set:

| OWASP Category | Applicability | Verdict |
|----------------|--------------|---------|
| A01 Broken Access Control | Not applicable -- no access control logic modified | N/A |
| A02 Cryptographic Failures | Not applicable -- no cryptographic operations | N/A |
| A03 Injection | Changes are to YAML files with string entries; no user input interpolated | PASS |
| A04 Insecure Design | Changes improve design by making validation prerequisites explicit | PASS |
| A05 Security Misconfiguration | No configuration files modified; governance YAML is not a runtime config | N/A |
| A06 Vulnerable Components | No new dependencies introduced | PASS |
| A07 Auth Failures | Not applicable | N/A |
| A08 Data Integrity Failures | Governance YAML entries now carry accurate prerequisite information; reduces risk of CI tools producing false-pass results from incomplete constraint declarations | PASS |
| A09 Logging Failures | No logging-sensitive content in governance YAML entries | PASS |
| A10 SSRF | No URL or external resource references introduced | N/A |

---

## Evidence Chain

All changes are traceable to the analysis document:

| Change | Evidence Source |
|--------|----------------|
| cd-generator entry 5 loading prerequisite | FM-001 analysis "Specific implementation steps" item 1; E-006 governance YAML entry; E-007 .md behavioral check |
| uc-slicer extensions check | uc-slicer.md `<input>` section "Required input"; `<guardrails>` "Input validation" |
| uc-slicer FM-002 post_completion_checks | FM-002 analysis "Specific implementation steps" items 3 and 4 |
| uc-slicer rejection artifact on_send (PM-001) | PM-001 analysis "Specific implementation steps" item 2 |
| uc-author rejection artifact on_receive (PM-001) | PM-001 analysis "Specific implementation steps" item 3 |
| tspec-generator slice_id cross-reference | tspec-generator.md Layer 2 guardrail check for slice_id + STORY_DEFINED |
| tspec-analyst mutual prerequisite | tspec-analyst.md `<input>` section "Coverage analysis requires both inputs" |
| cd-validator mutual prerequisite and x-source-use-case | cd-validator.md `<input>` "Required fields in UC artifact input"; `<methodology>` Step 2 |

---

*Implementation produced by eng-backend*
*Constitutional compliance: P-001 (all conclusions evidence-based), P-002 (persisted to file), P-003 (no recursive subagents), P-022 (limitations disclosed: boundary rule not yet formalized in agent-development-standards.md)*
*OWASP verification: self-verified against Top 10; primary finding is A08 (Data Integrity) improvement*
*SSDF practice: PW.5 (secure coding patterns applied to governance artifact authoring), PW.6 (secure defaults: loading prerequisites make implicit requirements explicit)*
*Date: 2026-03-11*
