# Quality Score Report: PROJ-012 Agent Optimization -- Iteration 2

<!-- VERSION: 1.0.0 | DATE: 2026-02-26 | SOURCE: PROJ-012 | AGENT: adv-scorer | STRATEGY: S-014 -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Verdict, score, and top action |
| [Scoring Context](#scoring-context) | Deliverable metadata and strategy references |
| [Score Summary](#score-summary) | Composite table and threshold comparison |
| [Dimension Scores](#dimension-scores) | Per-dimension scored table |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Evidence, gaps, improvement path per dimension |
| [Fix Verification](#fix-verification) | Verification of the 7 iteration 2 fixes |
| [Remaining Gaps](#remaining-gaps) | Unaddressed findings carried from iteration 1 |
| [Improvement Recommendations](#improvement-recommendations) | Priority-ordered action list |
| [Leniency Bias Check](#leniency-bias-check) | Self-review confirmation |

---

## L0 Executive Summary

**Score:** 0.893/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Completeness (0.86)

**One-line assessment:** Iteration 2 resolves the CRITICAL H-34 L5 CI false claim and six other targeted fixes, lifting Internal Consistency from 0.62 to 0.91 and the composite from 0.749 to 0.893. The deliverable is now in the REVISE band (0.85-0.91) -- close to the 0.92 threshold but not yet passing due to persisting Completeness gaps (extract() degradation, GovernanceSectionBuilder covering only 6 of 11 fields, check_agent_conformance.py not updated) and the unaddressed FM-013 governance tail-placement concern.

---

## Scoring Context

- **Deliverable:** PROJ-012 governance migration -- single-file agent definition architecture
- **Files Scored:** 6 primary source files + 2 rule files + 3 test files + iteration 1 score report
- **Deliverable Type:** Code + documentation changes (architectural migration)
- **Criticality Level:** C3 (AE-002 auto-escalation: touches `.context/rules/`)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Iteration:** 2
- **Prior Score:** 0.749 (iteration 1)
- **Fixes Applied:** 7 (targeting Internal Consistency, Methodological Rigor, Completeness)
- **Scored:** 2026-02-26

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.893 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Prior Score** | 0.749 (iteration 1) |
| **Delta** | +0.144 |
| **Fixes Applied** | 7 of 10 iteration 1 recommendations addressed |
| **Critical Findings Remaining** | 0 (the H-34 L5 CI false claim is resolved) |
| **Major Findings Remaining** | 4 (FM-013, FM-019, extract() degradation, conformance script) |
| **Minor Findings Remaining** | 3+ (GovernanceSectionBuilder 6/11 coverage, new-agent path, auto-injection masking) |

**Gap to threshold:** 0.92 - 0.893 = 0.027. Targeted revision on 2-3 items should close the gap.

---

## Dimension Scores

| Dimension | Weight | Iter 1 Score | Iter 2 Score | Weighted | Change | Evidence Summary |
|-----------|--------|-------------|-------------|----------|--------|-----------------|
| Completeness | 0.20 | 0.80 | 0.86 | 0.172 | +0.06 | Round-trip compose integration test added; reserved governance headings documented; extract() and conformance script still unaddressed |
| Internal Consistency | 0.20 | 0.62 | 0.91 | 0.182 | +0.29 | H-34 L5 CI claim honestly hedged; docstring fixed; adv-executor body_format corrected; case-insensitive heading dedup implemented |
| Methodological Rigor | 0.20 | 0.78 | 0.90 | 0.180 | +0.12 | Case-insensitive dedup with test; round-trip integration test; 529 tests pass; FM-013 tail placement still unaddressed |
| Evidence Quality | 0.15 | 0.82 | 0.90 | 0.135 | +0.08 | New integration test provides empirical round-trip evidence; 529 passing tests; case-insensitive boundary tested |
| Actionability | 0.15 | 0.75 | 0.88 | 0.132 | +0.13 | 7 of 10 recommendations executed; remaining gaps are well-specified with clear implementation paths |
| Traceability | 0.10 | 0.73 | 0.92 | 0.092 | +0.19 | H-34 rule text, L2-REINJECT, Verification table, and quality-enforcement.md all updated consistently; reserved headings documented with GovernanceSectionBuilder traceability |
| **TOTAL** | **1.00** | **0.749** | | **0.893** | **+0.144** | |

---

## Detailed Dimension Analysis

### Completeness (0.86/1.00)

**Evidence of improvement (iteration 1 -> 2):**

1. **Round-trip compose integration test added** (`test_compose_pipeline.py::test_composed_agent_body_contains_governance_sections`, lines 362-486). This test creates a canonical source with governance fields (`version: 2.3.1`, `tool_tier: T3`, `enforcement`, `portability`), runs the full compose pipeline, and verifies: (a) governance fields do NOT appear in frontmatter, (b) governance data DOES appear in the prompt body (version, tool tier, enforcement, portability values confirmed). This directly addresses iteration 1 recommendation #4 (round-trip test) and provides empirical evidence for governance injection correctness.

2. **Reserved governance headings documented** in `agent-development-standards.md` lines 161-174. Six headings (Agent Version, Tool Tier, Enforcement, Portability, Prior Art, Session Context) are listed with their governance field mappings and injecting service. An explicit prohibition is stated: "Agent prompt bodies (`.jerry.prompt.md` files) MUST NOT use these heading names for narrative content." Case-insensitive matching is noted. This addresses iteration 1 recommendation #9.

3. **529 tests pass** (527 + 2 new). All pre-existing tests remain green.

**Persisting gaps:**

1. **`extract()` not updated for single-file round-trip.** The `extract()` method (claude_code_adapter.py lines 98-204) still reads `governance_yaml_path` and falls back to defaults when no `.governance.yaml` exists. Post-migration agents without `.governance.yaml` will produce degraded CanonicalAgent entities (version defaults to "1.0.0", tool_tier to T1). No `_extract_governance_from_body()` method was added. This was iteration 1 recommendation #5 and remains unaddressed. Impact: any future use of `jerry extract` on composed output will produce degraded canonical data.

2. **`check_agent_conformance.py` not updated.** This was iteration 1 recommendation #3 and remains unaddressed (explicitly listed in "REMAINING UNADDRESSED FINDINGS"). The conformance script still validates YAML frontmatter for governance fields that now live in the prompt body.

3. **GovernanceSectionBuilder covers 6 of 11 governance fields.** The five omitted fields (identity, persona, guardrails, constitution, validation) are assumed to exist as prose in the prompt body. For new agents created from `.jerry.yaml`-only sources without an existing markdown body, this creates an incomplete agent definition. The scoring context notes this was "lower priority or out of scope."

**Score justification:** +0.06 from iteration 1. The round-trip integration test and reserved headings documentation close two specific gaps. However, three substantive completeness gaps remain (extract degradation, conformance script, 6/11 field coverage). The extract degradation is the most impactful because it creates a silently broken workflow. Scored 0.86 rather than 0.88 because the persisting gaps are functional (not just documentary).

---

### Internal Consistency (0.91/1.00)

**Evidence of improvement (iteration 1 -> 2):**

1. **H-34 L5 CI false claim resolved (CRITICAL fix).** This was the most severe finding in iteration 1, directly violating P-022 (no deception). Three locations were updated:
   - `agent-development-standards.md` H-34 Verification column (line 33): Now reads "L5 (CI): JSON Schema validation on canonical `.jerry.yaml` files on PR (planned -- CI job not yet implemented; currently enforced at compose-time via Python validation)."
   - `agent-development-standards.md` L2-REINJECT (line 7): Now reads "Compose pipeline validates canonical .jerry.yaml sources (CI gate planned)."
   - `agent-development-standards.md` Verification table (line 431): Now reads "Compose-time validation (CI pipeline check planned)."
   - `quality-enforcement.md` H-34 row (line 74): Updated to "Agent definition standards (single-file architecture, governance in prompt body, canonical .jerry.yaml schema validation)."

   All four locations are now internally consistent: they describe compose-time validation as the current enforcement mechanism with CI as a planned future addition. The P-022 violation is resolved.

2. **Stale docstring fixed.** `compose_agents_command_handler.py` `_filter_vendor_frontmatter` docstring (lines 240-241): Now reads "they are injected into the prompt body as XML sections (PROJ-012 single-file architecture)". Correctly describes the current architecture without referencing the deleted `.governance.yaml`.

3. **adv-executor body_format corrected.** `adv-executor.jerry.yaml` line 65: `body_format: xml`. Verified in the composed output (`skills/adversary/agents/adv-executor.md`): `body_format: xml`. The canonical source and composed output are now consistent with the actual XML-tagged body structure of adv-executor.

4. **Case-insensitive heading dedup implemented.** `governance_section_builder.py` `_extract_headings` (lines 107-119): headings stored via `.lower()`. The `build()` method (lines 56-88) checks against lowercase keys (`"agent version"`, `"tool tier"`, etc.). A dedicated test (`test_build_skips_section_when_heading_exists_case_insensitive`, test file lines 274-291) validates that `## AGENT VERSION` and `## TOOL TIER` in an existing body suppress governance injection for those fields. This closes FMEA FM-001/FM-002 (heading collision risk).

**Persisting gaps:**

1. **FM-013 governance tail placement.** Governance sections are still appended AFTER the canonical body content in `_build_body()` (claude_code_adapter.py line 288). This ordering question was explicitly listed as "NOT fixed in iteration 2" (RPN 405). While the ordering is now at least internally consistent (build always appends; documented reserved headings describe this pattern), the question of whether governance constraints should appear earlier in the prompt for attention primacy remains an open design question, not an internal contradiction.

2. **FM-019 governance defaults silently discarded.** Layer-1 governance defaults (e.g., `version: 1.0.0` in `jerry-agent-defaults.yaml`) pass through the 4-layer merge but are then stripped by `_filter_vendor_frontmatter`. This means governance defaults defined at Layer 1 or Layer 2 have no effect on the composed output. This is architecturally consistent (governance goes in body, not frontmatter) but could surprise a developer who adds governance fields to defaults files expecting them to appear somewhere.

**Score justification:** +0.29 from iteration 1. This is the largest improvement across all dimensions, driven primarily by resolving the CRITICAL H-34 L5 CI false claim (the single biggest defect in iteration 1). Three additional consistency fixes (docstring, body_format, case-insensitive dedup) further strengthen the score. The remaining gaps (FM-013, FM-019) are design questions rather than direct contradictions. Scored 0.91 rather than 0.93 because FM-019 (governance defaults silently discarded) represents a subtle consistency gap where the 4-layer merge architecture nominally supports governance defaults but `_filter_vendor_frontmatter` ensures they have no effect -- this is architecturally intentional but not documented as such.

---

### Methodological Rigor (0.90/1.00)

**Evidence of improvement (iteration 1 -> 2):**

1. **Case-insensitive heading dedup with dedicated test.** The implementation in `governance_section_builder.py` is clean: `_extract_headings` normalizes to lowercase at extraction time (line 118: `headings.add(match.group(1).strip().lower())`), and all `build()` comparisons use lowercase literal strings. This is a correct-by-construction approach -- the normalization happens once at the boundary, not scattered across comparison sites. The test (`test_build_skips_section_when_heading_exists_case_insensitive`) uses `## AGENT VERSION` and `## TOOL TIER` (all-caps) to exercise the boundary, confirming the fix works.

2. **Round-trip compose integration test.** `test_composed_agent_body_contains_governance_sections` (test_compose_pipeline.py lines 362-486) is a 124-line integration test that exercises the full pipeline: create canonical source with specific governance values -> compose -> verify governance data in body and NOT in frontmatter. This test catches regression of the core PROJ-012 invariant (governance in body, not frontmatter). The test is thorough: it checks specific values (`2.3.1`, `T3`, `C2`, `128000`) rather than just structural presence.

3. **529 tests pass.** The two new tests integrate cleanly. No regressions.

4. **GovernanceSectionBuilder architecture remains clean.** The builder follows OCP: it produces markdown headings that feed into the existing `PromptTransformer` pipeline without modifying it. The `_HEADING_TO_TAG` mapping in `prompt_transformer.py` (lines 33-39) includes all six governance headings. The separation of concerns is maintained: builder produces markdown, transformer converts to XML, adapter assembles the full output.

**Persisting gaps:**

1. **FM-013 governance tail placement (RPN 405).** `_build_body()` appends governance after canonical content (line 288). No documented rationale for this ordering exists in the codebase. This is the highest-RPN finding from the FMEA and remains unaddressed. The methodological concern is not that tail placement is necessarily wrong, but that the ordering decision lacks documented justification and no test verifies the relative position of governance sections within the body.

2. **Five FMEA Critical-rated failure modes (RPN >= 250) partially addressed.** FM-001/FM-002 (heading collision) resolved via case-insensitive dedup. FM-013 (tail placement, RPN 405), FM-019 (defaults discarded, RPN 280), and FM-026 (new agents missing sections, RPN 256) remain. FM-021 (--clean not removing .governance.yaml, RPN 280) and FM-024 (governance headings indistinguishable in markdown format, RPN 252) remain.

3. **No round-trip extract test.** The new integration test verifies compose output. No test verifies compose -> extract -> compare, meaning the extract() degradation described in iteration 1 remains untested.

**Score justification:** +0.12 from iteration 1. The case-insensitive dedup and round-trip compose test close two significant methodology gaps. The test suite now provides empirical evidence for the core architecture invariant. Remaining gaps are primarily unaddressed FMEA findings that were explicitly deferred. Scored 0.90 rather than 0.92 because FM-013 (RPN 405, the single highest FMEA finding) remains without documented rationale, and no extract round-trip test exists.

---

### Evidence Quality (0.90/1.00)

**Evidence of improvement (iteration 1 -> 2):**

1. **New integration test provides empirical evidence.** The `test_composed_agent_body_contains_governance_sections` test (lines 362-486) verifies specific governance values round-trip through the compose pipeline. This replaces the iteration 1 gap where governance injection was only tested at the unit level (GovernanceSectionBuilder tests) but not through the full pipeline.

2. **Case-insensitive boundary condition tested.** The `test_build_skips_section_when_heading_exists_case_insensitive` test (lines 274-291) provides direct empirical evidence for the heading dedup fix, using boundary values (all-caps headings). This test would catch a regression if someone changed `_extract_headings` to use case-sensitive matching.

3. **529 passing tests provide strong functional evidence.** All claims about pipeline behavior are now backed by passing tests. The test coverage for GovernanceSectionBuilder alone is 17+ tests covering individual fields, all-fields, empty-fields, existing-body dedup, and case-insensitive dedup.

**Persisting gaps:**

1. **No runtime token count measurement.** The iteration 1 gap (no measured token counts for governance injection impact) remains. The CB-01 through CB-05 claims are still theoretical.

2. **`check_agent_conformance.py` not executed.** Iteration 1 noted this script was analyzed by reading but not executed. This gap persists.

3. **Extract() degradation not empirically validated.** The claim that extract() produces degraded output for post-migration agents is supported by code reading (no `.governance.yaml` -> defaults used) but no test exercises this exact failure mode.

**Score justification:** +0.08 from iteration 1. The new integration test and case-insensitive boundary test strengthen the evidence base substantially. Evidence quality is now strong for the compose pipeline direction (canonical -> composed) but weak for the reverse direction (composed -> canonical). Scored 0.90 rather than 0.92 because the extract() degradation claim lacks empirical validation.

---

### Actionability (0.88/1.00)

**Evidence of improvement (iteration 1 -> 2):**

1. **7 of 10 iteration 1 recommendations executed.** The scoring context confirms seven specific fixes were applied:
   - Fix 1 (Priority 1): H-34 L5 CI false claim resolved
   - Fix 2 (Priority 2): Stale docstring updated
   - Fix 3 (Priority 8): adv-executor body_format corrected
   - Fix 4 (iteration 1 rec #6 variant): Case-insensitive heading dedup
   - Fix 5 (Priority 9): Reserved governance headings documented
   - Fix 6 (Priority 4 variant): Round-trip compose integration test
   - Fix 7: Test suite expanded (529 tests passing)

2. **Remaining gaps have clear implementation paths.** The unaddressed items are well-specified:
   - extract() degradation: implement `_extract_governance_from_body()` (specific method, specific behavior)
   - conformance script: update to validate prompt body sections (specific script, specific validation change)
   - FM-013 tail placement: prepend governance before canonical body in `_build_body()` (specific code change, line 288)

**Persisting gaps:**

1. **The remaining 3 iteration 1 recommendations are unaddressed.** Priority 3 (conformance script), Priority 5 (extract governance from body), and Priority 6 (governance preamble position) were explicitly deferred. These represent the gap between 0.88 and a passing score.

2. **No iteration 3 plan.** While the remaining items are individually well-specified, no consolidated action plan for iteration 3 prioritizes among them. For a C3 deliverable at the REVISE band, a brief prioritized next-steps list would improve actionability.

**Score justification:** +0.13 from iteration 1. Executing 7 of 10 recommendations demonstrates strong iteration discipline. The remaining gaps are clearly articulated and achievable. Scored 0.88 rather than 0.90 because no consolidated iteration 3 plan sequences the remaining work.

---

### Traceability (0.92/1.00)

**Evidence of improvement (iteration 1 -> 2):**

1. **H-34 rule text updated consistently across four locations.** The H-34 description, L2-REINJECT, Verification table, and quality-enforcement.md H-34 row all use consistent language describing the single-file architecture with compose-time validation and planned CI gate. There are no internal contradictions in how the enforcement state is described.

2. **Reserved governance headings traced to GovernanceSectionBuilder.** The new "Reserved Governance Headings" subsection in `agent-development-standards.md` (lines 161-174) creates a bidirectional trace: from the documentation to the code service that implements injection, and from the heading names to the governance fields they represent. This closes the traceability gap where developers had no way to know which headings were reserved.

3. **IN-007 finding resolution.** The iteration 1 traceability penalty for IN-007 (S-013 apparently reviewing an older version of agent-development-standards.md) is resolved: the file is now unambiguously at v1.3.0 (line 3: `VERSION: 1.3.0 | DATE: 2026-02-26 | SOURCE: ... PROJ-012`) and all content is consistent with single-file architecture. The S-013 finding that attacked dual-file language is no longer applicable to the current document state.

4. **Quality-enforcement.md H-34 row traces to current architecture.** Line 74 reads "Agent definition standards (single-file architecture, governance in prompt body, canonical .jerry.yaml schema validation)." This accurately summarizes the PROJ-012 deliverable and provides a trace from the HARD rule index to the specific architectural approach.

**Persisting gaps:**

1. **FM-013 governance tail placement still lacks formal requirement reference.** The FMEA's highest-RPN finding (RPN 405) cites "LLMs exhibit primacy and recency bias" but does not trace this to a specific framework requirement (no CB standard, no ADR, no architectural principle). This is a minor traceability gap for a design question that was explicitly deferred.

**Score justification:** +0.19 from iteration 1. The consistent multi-location H-34 update and reserved headings documentation close the major traceability gaps. Scored 0.92 because the only remaining gap (FM-013 requirement grounding) is minor and pertains to a deferred design question.

---

## Fix Verification

| # | Fix Description | Verified | Evidence |
|---|----------------|----------|----------|
| 1 | H-34 L5 CI false claim resolved | YES | `agent-development-standards.md` lines 7, 33, 431 all say "planned" / "CI job not yet implemented" / "CI pipeline check planned". `quality-enforcement.md` line 74 updated. No false CI claims remain. |
| 2 | Stale docstring fixed | YES | `compose_agents_command_handler.py` lines 240-241: "they are injected into the prompt body as XML sections (PROJ-012 single-file architecture)". No reference to `.governance.yaml`. |
| 3 | adv-executor body_format corrected | YES | `adv-executor.jerry.yaml` line 65: `body_format: xml`. Composed output `skills/adversary/agents/adv-executor.md` also contains `body_format: xml`. |
| 4 | Case-insensitive heading dedup | YES | `governance_section_builder.py` line 118: `.lower()`. All `build()` checks use lowercase keys. Test at lines 274-291 validates with all-caps headings. |
| 5 | Reserved governance headings documented | YES | `agent-development-standards.md` lines 161-174: 6-row table with heading name, governance field, and injecting service. Prohibition stated. Case-insensitive matching noted. |
| 6 | Round-trip compose integration test | YES | `test_compose_pipeline.py` lines 362-486: 124-line test creates canonical source with governance fields, composes, verifies governance in body and NOT in frontmatter. Checks specific values. |
| 7 | 529 tests pass | CLAIMED | Not independently verified (scoring task does not run tests). Consistent with 527 original + 2 new tests described. |

**Verification result:** 6 of 7 fixes independently verified from file content. Fix 7 (test count) is consistent with evidence but not independently executed.

---

## Remaining Gaps

### Carried from iteration 1 (explicitly deferred):

| Finding | RPN | Impact | Status |
|---------|-----|--------|--------|
| FM-013: Governance sections at end of prompt body | 405 | Governance constraints may receive less LLM attention due to tail placement | Deferred -- design question, no documented rationale |
| FM-019: Layer-1 governance defaults silently discarded | 280 | Developers adding governance to defaults files will see no effect | Deferred -- architecturally intentional but undocumented |
| FM-003/IN-006: extract() produces degraded output | - | Running `jerry extract` on post-migration agents produces T1/1.0.0 defaults | Deferred -- workflow gap |
| FM-026: New agents from .jerry.yaml-only source lack body sections | 256 | GovernanceSectionBuilder covers 6/11 fields; identity, guardrails, constitution not injected | Deferred -- scope limitation |
| FM-022: check_agent_conformance.py validates old architecture | - | Script produces false failures/passes for migrated agents | Deferred -- CI tooling gap |
| Challenge 6: GovernanceSectionBuilder covers 6/11 fields | - | See FM-026 | Deferred |
| Challenge 8: Constitutional triplet auto-injection masks gaps without logging | - | extract() silently adds P-003/P-020/P-022 without logging, masking source-level gaps | Deferred -- minor |

### New observations from iteration 2 review:

| Finding | Severity | Description |
|---------|----------|-------------|
| No extract round-trip test | Medium | Compose -> extract -> compare test would surface extract() degradation. Iteration 2 added compose round-trip but not the full cycle. |
| FM-019 undocumented intentionality | Minor | `_filter_vendor_frontmatter` stripping governance defaults is architecturally correct but should be documented as intentional (e.g., a code comment explaining that governance defaults feed into the canonical agent, not into composed frontmatter). |

---

## Improvement Recommendations (Priority Ordered for Iteration 3)

| Priority | Dimension Impact | Current | Target | Recommendation | Effort |
|----------|-----------------|---------|--------|----------------|--------|
| 1 | Completeness +0.04, Methodological Rigor +0.02 | 0.86, 0.90 | 0.90, 0.92 | **Implement `_extract_governance_from_body()`** in `ClaudeCodeAdapter.extract()`. Parse `<agent_version>`, `<tool_tier>`, `<enforcement>`, `<portability>`, `<prior_art>`, `<session_context>` XML tags (or `## Agent Version` etc. markdown headings) from the prompt body. Populate `gov_data` before defaults are applied. Add deprecation warning log when `governance_yaml_path` is None. | Medium (2-3 hours) |
| 2 | Completeness +0.02, Evidence Quality +0.02 | 0.86, 0.90 | 0.88, 0.92 | **Add compose -> extract round-trip test**: Create canonical source, compose to `.md`, extract from composed `.md`, assert CanonicalAgent fields match the original source. This test will validate the extract() fix from Priority 1 and provide empirical evidence for the full migration cycle. | Low (1 hour) |
| 3 | Actionability +0.02 | 0.88 | 0.90 | **Add code comment to `_filter_vendor_frontmatter`** documenting that governance defaults from Layers 1-2 are intentionally stripped because governance data flows through the prompt body path (GovernanceSectionBuilder), not the frontmatter merge path. This closes FM-019 as "by design" with documented rationale. | Low (15 min) |
| 4 | Methodological Rigor +0.01 | 0.90 | 0.91 | **Document governance tail-placement rationale** in `_build_body()` as a code comment or in the "Reserved Governance Headings" section. Either justify the tail placement (e.g., "governance metadata is reference data, not behavioral instructions; tail placement keeps the primary identity/methodology flow uninterrupted") or note it as a deferred design decision with a worktracker reference. | Low (15 min) |

**Projected iteration 3 score with priorities 1-4:** Completeness 0.90, Internal Consistency 0.91, Methodological Rigor 0.92, Evidence Quality 0.92, Actionability 0.90, Traceability 0.92. Projected composite: ~0.913. This would bring the deliverable within 0.007 of the 0.92 threshold. Reaching 0.92 would additionally require addressing the conformance script gap (Completeness) or extending GovernanceSectionBuilder coverage.

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing weighted composite
- [x] Evidence documented for each dimension score with specific file paths and line numbers
- [x] Uncertain scores resolved downward: Internal Consistency uncertain between 0.91-0.93; chose 0.91 due to FM-019 (governance defaults silently discarded) being architecturally intentional but undocumented
- [x] No dimension scored above 0.92 except Traceability (0.92), which is justified by the consistent multi-location H-34 update
- [x] Completeness scored at 0.86 despite 529 tests passing -- the unimplemented extract() degradation and conformance script gap justify the penalty
- [x] The +0.29 improvement in Internal Consistency is large but justified: resolving a CRITICAL P-022 violation (false CI claim) in a single iteration is expected to produce a large score jump; the fix was verified in 4 file locations
- [x] The composite 0.893 is in the REVISE band (0.85-0.91), consistent with a deliverable that fixed its most severe defects but still has substantive completeness gaps
- [x] Iteration 2 composite (0.893) vs iteration 1 composite (0.749): the +0.144 delta is driven by Internal Consistency (+0.29) and Traceability (+0.19), both of which had their most severe findings directly addressed. This magnitude of improvement is proportionate to resolving a CRITICAL finding plus six MAJOR findings in one iteration.

---

## Composite Score Verification

```
composite = (0.86 x 0.20) + (0.91 x 0.20) + (0.90 x 0.20) + (0.90 x 0.15) + (0.88 x 0.15) + (0.92 x 0.10)
          = 0.172 + 0.182 + 0.180 + 0.135 + 0.132 + 0.092
          = 0.893
```

**Arithmetic verification:**
- 0.86 x 0.20 = 0.172
- 0.91 x 0.20 = 0.182
- 0.90 x 0.20 = 0.180
- 0.90 x 0.15 = 0.135
- 0.88 x 0.15 = 0.132
- 0.92 x 0.10 = 0.092

Sum: 0.172 + 0.182 + 0.180 + 0.135 + 0.132 + 0.092 = **0.893**

Verdict: **REVISE** (in the 0.85-0.91 band per quality-enforcement.md operational score bands)

---

## Handoff Schema (Session Context -- adv-scorer to orchestrator)

```yaml
verdict: REVISE
composite_score: 0.893
threshold: 0.92
prior_score: 0.749
delta: +0.144
weakest_dimension: completeness
weakest_score: 0.86
critical_findings_count: 0
major_findings_count: 4
iteration: 2
improvement_recommendations:
  - "Implement _extract_governance_from_body() in extract() to parse governance XML/heading tags from body (Priority 1, Medium effort)"
  - "Add compose -> extract round-trip test (Priority 2, Low effort)"
  - "Document governance defaults stripping as intentional in _filter_vendor_frontmatter (Priority 3, Low effort)"
  - "Document governance tail-placement rationale in _build_body() (Priority 4, Low effort)"
projected_iter3_score: 0.913
```

---

*Agent: adv-scorer*
*Strategy: S-014 (LLM-as-Judge)*
*Session: PROJ-012 adversarial quality review -- Iteration 2*
*Date: 2026-02-26*
*Criticality: C3 (AE-002 auto-escalation)*
*SSOT: `.context/rules/quality-enforcement.md`*
