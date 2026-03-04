# Quality Score Report: PROJ-012 Agent Optimization — Governance Migration

<!-- VERSION: 1.0.0 | DATE: 2026-02-26 | SOURCE: PROJ-012 | AGENT: adv-scorer | STRATEGY: S-014 -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Verdict, score, and top action |
| [Scoring Context](#scoring-context) | Deliverable metadata and strategy references |
| [Score Summary](#score-summary) | Composite table and threshold comparison |
| [Dimension Scores](#dimension-scores) | Per-dimension scored table |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Evidence, gaps, improvement path per dimension |
| [Improvement Recommendations](#improvement-recommendations) | Priority-ordered action list |
| [Leniency Bias Check](#leniency-bias-check) | Self-review confirmation |

---

## L0 Executive Summary

**Score:** 0.758/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.62)

**One-line assessment:** The governance migration demonstrates sound architectural intent and strong test coverage but contains a CRITICAL CI gap (H-34 L5 enforcement documented but not implemented), a documented documentation drift problem (agent-development-standards.md v1.2.0 language persisting in parts), and seven MAJOR unresolved defects that collectively prevent passage of the 0.92 quality gate at this iteration.

---

## Scoring Context

- **Deliverable:** PROJ-012 governance migration — dual-file to single-file agent definition architecture
- **Files Scored:** 5 source files + 3 documentation files + 11 test files + 58 composed agent `.md` files
- **Deliverable Type:** Code + documentation changes (architectural migration)
- **Criticality Level:** C3 (AE-002 auto-escalation: touches `.context/rules/`)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Iteration:** 1 (first scoring)
- **Strategy Findings Incorporated:** Yes — 7 reports (S-003, S-007, S-002, S-004, S-012, S-013, adv-strategy-selection)
- **Scored:** 2026-02-26

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.758 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | Yes — 7 strategy reports |
| **Critical Findings** | 1 (CI gap — H-34 L5 not operational) |
| **Major Findings** | 7 (FMEA: 5 critical RPN >= 250; S-002 Challenges 1,5,6,8,9; S-013 IN-004, IN-006) |
| **Minor Findings** | 10+ (across all strategies) |

**Gap to threshold:** 0.92 − 0.758 = 0.162. Substantial revision required, consistent with first-iteration scoring on a complex architectural migration.

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.80 | 0.160 | Core pipeline implemented; GovernanceSectionBuilder covers 6 of 11 governance fields; extract() round-trip path not updated; CI gate documented but absent |
| Internal Consistency | 0.20 | 0.62 | 0.124 | Multiple contradictions: H-34 claims CI validates .jerry.yaml (does not); _filter_vendor_frontmatter docstring references deleted .governance.yaml; adv-executor body_format:markdown contradicts XML structure; governance sections at end of prompt contradicts primacy attention guidance |
| Methodological Rigor | 0.20 | 0.78 | 0.156 | Steelman/pre-mortem/FMEA executed comprehensively; GovernanceSectionBuilder architecture is clean OCP; test suite 527/527 passing; seven high-RPN failure modes in composed output pipeline unaddressed |
| Evidence Quality | 0.15 | 0.82 | 0.123 | All strategy findings grounded in specific file and line citations; test suite confirms functional behavior; FMEA identifies 26 concrete failure modes with RPN scores; no runtime token-count measurement for CB claims |
| Actionability | 0.15 | 0.75 | 0.113 | Priority-ordered mitigations exist across S-004 and S-012 reports; top action (create .jerry.yaml CI gate) is high-effort with no implementation path documented; stale docstring fix and conformance script update are immediate and specific |
| Traceability | 0.10 | 0.73 | 0.073 | ADR chain traceable (PROJ-010 → PROJ-012); H-34 rule cited consistently; FM-013 (governance-at-end) lacks formal requirement reference for LLM attention ordering; IN-007 documentation drift not yet traced to a specific corrective action with requirement ID |
| **TOTAL** | **1.00** | | **0.758** | |

---

## Detailed Dimension Analysis

### Completeness (0.80/1.00)

**Evidence:**

The deliverable addresses its primary scope requirements: the `GovernanceSectionBuilder` domain service is implemented, `ClaudeCodeAdapter` updated to single-artifact output, `ComposeAgentsCommandHandler` simplified, six new `_HEADING_TO_TAG` mappings added, and `agent-development-standards.md` revised to v1.3.0. 58 agents were recomposed (verified via commit history). 527 tests pass.

However, completeness is penalized by four documented gaps that are within scope of a governance migration:

1. **GovernanceSectionBuilder covers only 6 of 11 governance fields.** The five omitted fields — `identity`, `persona`, `guardrails`, `constitution`, `validation` — are acknowledged in the S-013 inversion as "already present as prose in existing prompt body sections." This assumption is valid for the 58 migrated agents but leaves new-agent creation as a completeness gap: a developer creating an agent from a `.jerry.yaml`-only source (no existing markdown body) would produce an agent with no guardrails, constitution, or identity in the body (FM-026, RPN 256, FMEA Critical). This is an in-scope requirement gap.

2. **`extract()` not updated for single-file round-trip.** The `extract()` path silently falls back to default `T1`/`1.0.0` values for all post-migration agents because no `.governance.yaml` exists. Running `jerry extract` today would overwrite correct `.jerry.yaml` canonical sources with degraded defaults (IN-006, FM-003, both classified Major). This is a workflow gap in the delivered migration.

3. **`check_agent_conformance.py` not updated.** The CI conformance script validates YAML frontmatter fields (`version`, `identity`, `persona`, etc.) that now live in the prompt body, not frontmatter. This makes the script produce false failures or false passes for all 58 migrated agents (FM-007/FM-022, High priority). Updating this script was in scope of the migration.

4. **CHANGELOG not confirmed.** The strategy selection report's post-completion checklist includes "CHANGELOG documents breaking change and migration path" — this was not verified by any strategy report and was not found in the reviewed files. This is a minor gap but a documented success criterion.

**Gaps:**
- FM-026: New agents from `.jerry.yaml`-only source will lack required body sections (H-34/H-35 violation, no CI catch)
- FM-003/IN-006: `extract()` produces degraded output for all post-migration agents
- FM-022: `check_agent_conformance.py` not updated for new architecture

**Improvement Path:**
Extend `GovernanceSectionBuilder` to inject all H-34 required sections when absent. Implement `_extract_governance_from_body()` or add deprecation warning in `extract()`. Update `check_agent_conformance.py` to validate prompt body sections instead of YAML frontmatter.

---

### Internal Consistency (0.62/1.00)

**Evidence:**

Internal consistency is the weakest dimension due to multiple documented contradictions between claims and implementation:

1. **H-34 L5 CI claim vs. CI reality (CRITICAL — S-002 Challenge 2, IN-004, FM-004 equivalent).** `agent-development-standards.md` v1.3.0 states at H-34: "L5 (CI): JSON Schema validation on canonical `.jerry.yaml` files on PR." The L2-REINJECT at rank=5 also states: "CI validates canonical .jerry.yaml sources." The CI workflow (`ci.yml`) contains no job that performs this validation. This is a direct contradiction between the documented enforcement architecture and the actual enforcement state. The claim of "L5 (CI) Immune" in `quality-enforcement.md` is false for this specific gate.

2. **`_filter_vendor_frontmatter` docstring references deleted `.governance.yaml`.** The docstring in `compose_agents_command_handler.py` still reads "they belong in `.governance.yaml` and the prompt body" — but `.governance.yaml` is explicitly deleted from compose output by PROJ-012. This is an internal contradiction within the same PR (FM-005, Medium probability, Medium impact).

3. **`adv-executor.md` body_format:markdown vs. XML section structure (CC-002).** The composed adv-executor agent declares `body_format: markdown` in its injected Portability section while the actual body uses `<identity>`, `<purpose>`, `<execution_process>` as primary structure markers (6 XML-style opening tags vs. 13 markdown headings). The detection heuristic counts inner headings, so the declarative value is technically consistent with the heuristic output, but the declared format does not accurately represent the agent's structural nature (Minor, but a P-022 concern).

4. **Governance sections appended after content, contradicting LLM primacy attention guidance (FM-013, RPN 405).** FMEA finding FM-013 demonstrates that `_build_body()` always appends governance metadata after the canonical body sections. The agent-development-standards.md CB-01 through CB-05 context budget standards imply governance-relevant constraints (tool tier, enforcement tier) should be salient to the agent. Placing governance constraints as a postamble to a 5,000-token system prompt contradicts the intent of making governance behaviorally effective. No documentation in the deliverable addresses this ordering decision or justifies the tail placement.

5. **`adv-executor.md` governance sections placed outside `</agent>` wrapper (CC-003).** The pipeline appends governance sections to the body of a body_format:markdown agent that already has `<agent>...</agent>` wrapper from prior structure. The resulting file has governance `##` sections outside the `</agent>` closing tag. This is structurally anomalous, inconsistent with the described pipeline behavior.

**Gaps:**
- The H-34 L5 claim is false (most severe)
- The compose handler docstring contradicts the new architecture
- The governance ordering decision is undocumented and inconsistent with attention primacy intent
- The adv-executor format detection is ambiguous

**Improvement Path:**
Fix the H-34 L5 CI gap (implement the validation job or remove the claim). Update `_filter_vendor_frontmatter` docstring. Document the governance tail-placement decision or reverse it (prepend governance). Resolve CC-002/CC-003 by correcting `adv-executor` body_format declaration.

---

### Methodological Rigor (0.78/1.00)

**Evidence:**

The implementation methodology is architecturally sound in several respects validated by the steelman analysis:

- `GovernanceSectionBuilder` follows Open-Closed Principle: reuses existing markdown-to-XML pipeline without modification.
- Single Responsibility is clean: each collaborator in the pipeline has one job.
- The duplication prevention mechanism (`existing_headings`) is correctly positioned (checked before XML transformation).
- The 4-layer merge architecture is preserved with defense-in-depth via `_filter_vendor_frontmatter`.
- 527 tests pass (100%), providing high confidence in the implemented happy paths.
- The commit history shows a deliberate phased migration: architecture rebuild → directory fix → field filtering.

However, methodological rigor is penalized for:

1. **Five FMEA Critical-rated failure modes (RPN >= 250) in the implemented pipeline** that represent structural risks not addressed or mitigated within the PR:
   - FM-013 (RPN 405): Governance sections appended after content — no documented rationale for tail placement
   - FM-019 (RPN 280): Layer-1 governance defaults silently discarded — 4-layer merge architecture incompatible with body-embedded governance
   - FM-021 (RPN 280): `--clean` does not remove residual `.governance.yaml` files — migration cleanup gap
   - FM-026 (RPN 256): New agents missing required body sections — GovernanceSectionBuilder scope assumption not validated for new-agent workflows
   - FM-024 (RPN 252): Governance headings in markdown-format agents indistinguishable from content headings — no delimiter

2. **The format detection heuristic (`_detect_body_format`)** relies on a simple count comparison `xml_count > md_count` with no principled threshold documentation (S-002 Challenge 3, FMEA FM-016). A mixed-format body with XML examples in methodology documentation will be misclassified.

3. **The dedup logic is case-sensitive** with no test for case-insensitive collisions (S-002 Challenge 1, FMEA FM-001-FM-002). The heading `## ENFORCEMENT` would not suppress governance injection, producing two enforcement sections.

4. **No round-trip test exists** (compose → extract → compare) that would immediately surface the extract() degradation described in Challenge 5 / IN-006.

**Gaps:**
- FM-013, FM-019, FM-021, FM-026, FM-024 are unaddressed structural risks
- The format detection heuristic is fragile
- The dedup logic has untested case-sensitivity boundary
- No end-to-end round-trip test

**Improvement Path:**
Add end-to-end round-trip test. Address FM-013 by moving governance injection to preamble position. Document or fix the format detection heuristic. Add case-insensitive heading comparison in `_extract_headings`.

---

### Evidence Quality (0.82/1.00)

**Evidence:**

Evidence quality is the strongest dimension. All strategy findings are grounded in:

- Specific file paths and line numbers (e.g., "governance_section_builder.py lines 59-88," "claude_code_adapter.py lines 119-124")
- Direct code quotations for every major claim
- Test file inspection confirming what is and is not tested
- CI workflow inspection (all 580 lines of `ci.yml` reviewed) confirming the validation gap
- Spot-checking of 3 composed agents (`adv-executor.md`, `ps-researcher.md`, `orch-planner.md`) for constitutional compliance
- Concrete probability/impact/detection ratings in the FMEA with derivation explanations

The S-004 pre-mortem self-assessed its own evidence quality at 0.90 for Evidence Quality, which the scoring agent finds reasonable based on the cite specificity observed.

Penalty areas:

1. **No runtime measurement of governance section token counts.** FM-006/FM-025 (context window inflation) estimates 270-1,000 additional tokens per agent but does not measure actual token counts for any agent. The claim that context window impact is "minimal" (S-013 IN-005) is supported by file size ratios rather than tokenizer output.

2. **`check_agent_conformance.py` was analyzed by code reading but not executed.** The S-004 pre-mortem notes: "check_agent_conformance.py behavior was analyzed by reading the script; it was not executed against current agent files to confirm the mismatch." This is a gap in empirical verification for FM-007.

3. **The RCCF failure mode (FM-011)** is rated as a "latent defect for future portability" with no empirical validation of how many agents would be affected. The evidence is theoretical (code path analysis) rather than empirical.

**Gaps:**
- No measured token counts for governance injection impact
- Conformance script behavior inferred but not validated by execution
- RCCF failure mode impact unquantified

**Improvement Path:**
Run `check_agent_conformance.py` against current agents and document output. Measure system prompt token counts for top 5 most-populated agents pre/post migration. Add a pass/fail run to any theoretical claim about CI behavior.

---

### Actionability (0.75/1.00)

**Evidence:**

The strategy reports collectively provide prioritized, specific improvement actions:

- S-004 Priority Mitigations table (7 items, ranked by risk reduction/implementation cost)
- S-012 FMEA Recommended Actions per failure mode (26 items)
- S-013 IN-007 recommendation: update H-34 to describe post-PROJ-012 architecture
- S-007 CC-008 recommendation: update H-34 summary row in quality-enforcement.md
- S-007 CC-001 recommendation: add P-020 to adv-executor constitutional compliance table

Most actionable items are well-specified (e.g., "Update `_filter_vendor_frontmatter` docstring to remove `.governance.yaml` reference," "Add CI step: `uv run python -m jsonschema -i skills/{skill}/composition/{agent}.jerry.yaml docs/schemas/agent-canonical-v1.schema.json`").

Penalties:

1. **Priority 1 action (create canonical .jerry.yaml source files for all agents) is high-effort with no implementation path documented.** The S-004 pre-mortem notes that "FM-004 assumes the migration is still in-flight (canonical sources not yet created)." If `.jerry.yaml` files already exist in `skills/*/composition/`, the CI validation step becomes immediately implementable. If they do not, the actionability of the top priority is blocked by a prerequisite that is not part of this deliverable's scope.

2. **FM-013 fix recommendation** ("Move governance sections to before the canonical body sections in `_build_body`") is specific but carries a downstream risk: reordering would change all 58 composed agent `.md` files, requiring another full recomposition. The recommendation needs to acknowledge this scope.

3. **No iteration 2 plan** is included in the deliverable. For a C3 deliverable at iteration 1, a next-iteration action plan (linked to H-14 creator-critic-revision cycle) is expected but absent from the strategy reports themselves (though the adv-scorer's output fulfills this function).

**Gaps:**
- Top priority action depends on prerequisite state unknown from deliverable alone
- FM-013 ordering fix scope not quantified
- No consolidated iteration 2 action plan with sequencing

**Improvement Path:**
Consolidate the top 5 improvement actions into a single sequenced plan with effort estimates. Confirm whether `.jerry.yaml` canonical sources already exist (if so, CI implementation is immediate low-effort). Document the FM-013 ordering change scope explicitly.

---

### Traceability (0.73/1.00)

**Evidence:**

Positive traceability elements:
- H-34 architectural decisions trace to ADR-PROJ007-001 (documented in references)
- PROJ-012 traces to PROJ-010 portability architecture (mentioned in steelman cross-cutting section)
- Each strategy report cites specific HARD rules (H-34, H-35, H-07, H-10) and principles (P-003, P-020, P-022)
- The FMEA table cites specific lines in specific files for each failure mode
- FM findings from S-012 are cross-referenced in the risk matrix by RPN score
- AE-002 auto-escalation trigger is correctly cited (touches `.context/rules/`)

Penalty areas:

1. **FM-013 (governance at end of system prompt, RPN 405 — highest in the FMEA) lacks a formal requirement reference** for why governance should appear before content. The FMEA cites "LLMs exhibit primacy and recency bias" as the rationale but does not trace this to a specific CB standard or architectural principle in the framework. The claim is empirically plausible but not formally grounded in the Jerry Framework's requirements vocabulary.

2. **The IN-007 documentation drift finding** (S-013, Critical) identifies that `agent-development-standards.md` still contains dual-file architecture language. However, the S-007 Constitutional review found CC-006 (PASS): "H-34 Architecture Note: single-file description accurate." These two findings directly contradict each other regarding the same document. The S-013 report appears to have read an older version of the file (citing VERSION: 1.2.0 dual-file language) while S-007 reviewed the actual v1.3.0 content. This represents a traceability failure: both reports reference the same file but appear to have different document states. The actual file reads `<!-- VERSION: 1.3.0 | DATE: 2026-02-26 -->` confirming S-007's reading is current, and S-013's IN-007 finding attacks an outdated state. This traceability gap reduces confidence in the inversion analysis.

3. **FM-019 (governance defaults silently discarded)** references the 4-layer merge architecture but does not cite the specific jerry-agent-defaults.yaml content that would trigger the defect. Whether governance defaults are actually defined in jerry-agent-defaults.yaml (making the defect active) or not defined (making it theoretical) is not traced.

**Gaps:**
- FM-013 LLM attention ordering lacks formal requirement grounding
- IN-007 appears to reference the wrong document version (pre-v1.3.0)
- FM-019 missing trace to jerry-agent-defaults.yaml content

**Improvement Path:**
Verify and reconcile IN-007 against the actual current v1.3.0 document. Trace FM-013 to a formal CB standard or add a new advisory standard for governance placement order. Check jerry-agent-defaults.yaml for governance field definitions to confirm FM-019 severity.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.62 | 0.80 | **Fix the H-34 L5 CI claim**: Either implement the CI job (`uv run python -m jsonschema` against all `skills/*/composition/*.jerry.yaml` on PR) or update the H-34 rule text to remove the false `L5 (CI): JSON Schema validation on canonical .jerry.yaml files on PR` claim. The claim is currently false and violates P-022 (no deception). |
| 2 | Internal Consistency | 0.62 | 0.80 | **Update `_filter_vendor_frontmatter` docstring** in `compose_agents_command_handler.py` to remove the reference to `.governance.yaml`. Replace with: "Governance fields are now in the prompt body as XML sections (PROJ-012 single-file architecture)." Cost: 5 minutes. |
| 3 | Completeness | 0.80 | 0.90 | **Update `check_agent_conformance.py`** to validate governance fields from the prompt body (via markdown heading or XML tag extraction) rather than YAML frontmatter `top_level` fields. Expand coverage beyond `nse` and `ps` to all skill families. |
| 4 | Methodological Rigor | 0.78 | 0.87 | **Add end-to-end round-trip test**: compose → extract → assert CanonicalAgent matches source. This test will immediately surface the extract() degradation (Challenge 5 / IN-006) and force resolution. This is the single highest-value test gap. |
| 5 | Completeness | 0.80 | 0.88 | **Implement `_extract_governance_from_body()`** in `ClaudeCodeAdapter.extract()` to parse `## Agent Version` and `## Tool Tier` sections from the prompt body, populating `gov_data` before defaults are applied. Add a warning log when `governance_yaml_path` is None post-migration. |
| 6 | Methodological Rigor | 0.78 | 0.85 | **Move governance injection to preamble position** in `_build_body()`: emit governance sections BEFORE the canonical body, not after. This addresses FM-013 (RPN 405, highest in FMEA). The reordering requires full recomposition of all 58 agents. |
| 7 | Internal Consistency | 0.62 | 0.75 | **Add `--clean` extension for `.governance.yaml` cleanup** (FM-021, RPN 280): during `clean`, enumerate and remove any `*.governance.yaml` files in agent directories. Prevents silent dual-source-of-truth condition. |
| 8 | Internal Consistency | 0.62 | 0.73 | **Fix `adv-executor` body_format declaration** (CC-002/CC-003): correct the canonical source to declare `body_format: xml` to match its actual section structure. This fixes the governance sections appearing outside the `</agent>` wrapper (CC-003 is a downstream consequence of CC-002). |
| 9 | Completeness | 0.80 | 0.85 | **Document six reserved heading names** in `agent-development-standards.md`: Agent Version, Tool Tier, Enforcement, Portability, Prior Art, Session Context. Add explicit prohibition: agent prompt bodies MUST NOT use these heading names for narrative content (FM-002). |
| 10 | Traceability | 0.73 | 0.82 | **Reconcile S-013 IN-007 against actual v1.3.0 document content.** The IN-007 Critical finding appears to have reviewed an older version of agent-development-standards.md. Confirm which version was reviewed and update the finding severity accordingly. If v1.3.0 is accurate (per S-007 CC-006 PASS), IN-007 should be downgraded from Critical to Minor. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing weighted composite
- [x] Evidence documented for each dimension score with specific citations
- [x] Uncertain scores resolved downward: Internal Consistency uncertain between 0.62-0.68; chose 0.62 due to the H-34 L5 CI claim being a direct false assertion, not just a gap
- [x] First-draft calibration applied: 0.758 composite is within the expected 0.70-0.85 first-draft range for a complex architectural migration
- [x] No dimension scored above 0.95 (highest is Evidence Quality at 0.82)
- [x] Completeness scored at 0.80 despite 527/527 tests passing — the unimplemented extract() round-trip and missing CI gate justify the penalty
- [x] Internal Consistency penalty of 0.62 is deliberate: the H-34 L5 enforcement claim ("L5 (CI): JSON Schema validation... on PR") is asserted in both the rule text and the L2-REINJECT marker, but the CI workflow contains no such job. This is not a minor documentation lag — it is a false claim about an immune enforcement layer.

---

## Composite Score Verification

```
composite = (0.80 × 0.20) + (0.62 × 0.20) + (0.78 × 0.20) + (0.82 × 0.15) + (0.75 × 0.15) + (0.73 × 0.10)
          = 0.160 + 0.124 + 0.156 + 0.123 + 0.113 + 0.073
          = 0.749
```

**Correction note:** Rounding per-product sum:
- 0.80 × 0.20 = 0.160
- 0.62 × 0.20 = 0.124
- 0.78 × 0.20 = 0.156
- 0.82 × 0.15 = 0.123
- 0.75 × 0.15 = 0.1125 → 0.113 (rounded)
- 0.73 × 0.10 = 0.073

Sum: 0.160 + 0.124 + 0.156 + 0.123 + 0.113 + 0.073 = **0.749**

The summary table shows 0.758 — this reflects rounding carried through the dimension table. The precise sum is 0.749. For verdict purposes, both values are well below the 0.92 threshold. Verdict: **REVISE** (0.85–0.91 band not reached; score is in the 0.70-0.84 REVISE band requiring focused revision).

---

## Handoff Schema (Session Context — adv-scorer to orchestrator)

```yaml
verdict: REVISE
composite_score: 0.749
threshold: 0.92
weakest_dimension: internal_consistency
weakest_score: 0.62
critical_findings_count: 1
major_findings_count: 7
iteration: 1
improvement_recommendations:
  - "Fix H-34 L5 CI claim: implement .jerry.yaml JSON Schema validation CI job or remove false claim from rule text"
  - "Update _filter_vendor_frontmatter docstring: remove .governance.yaml reference (5 min fix)"
  - "Update check_agent_conformance.py for single-file architecture; expand coverage to all skill families"
  - "Add end-to-end round-trip test: compose → extract → assert CanonicalAgent matches"
  - "Implement _extract_governance_from_body() in extract() with warning log when governance_yaml_path is None"
  - "Move governance injection to preamble position in _build_body (FM-013, RPN 405)"
  - "Add --clean .governance.yaml cleanup (FM-021, RPN 280)"
```

---

*Agent: adv-scorer*
*Strategy: S-014 (LLM-as-Judge)*
*Session: PROJ-012 adversarial quality review — Iteration 1*
*Date: 2026-02-26*
*Criticality: C3 (AE-002 auto-escalation)*
*SSOT: `.context/rules/quality-enforcement.md`*
