# Quality Score Report: Stream 1B - System Design with Threat Model

## L0 Executive Summary

**Score:** 0.890/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Completeness (0.82)

**One-line assessment:** A structurally excellent system design with a well-executed STRIDE threat model, but with a measurable gap in Attack Surface 6 STRIDE coverage (3 of 6 categories missing), fixture bodies left as stub ellipses, and a DREAD priority ordering that is internally inconsistent with stated DREAD scores -- together these gaps prevent PASS at the C4 threshold.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-036-prompt-regression-harness/design/system-design.md`
- **Deliverable Type:** Design
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z
- **Iteration:** 1 (first scoring cycle)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.890 |
| **Threshold** | 0.94 (C4 criticality, per task specification) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (no adv-executor reports available) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.82 | 0.164 | All 4 layers present, but Attack Surface 6 covers only S and T (3/6 STRIDE categories); fixture bodies are stubs; MRObservability port absent |
| Internal Consistency | 0.20 | 0.92 | 0.184 | Module boundaries match dependency graph; port-adapter relationships consistent; threat IDs cross-reference to controls 1:1; one DREAD priority ordering inconsistency |
| Methodological Rigor | 0.20 | 0.91 | 0.182 | Hexagonal architecture correctly applied with explicit forbidden-dependency list; STRIDE systematic for 5 of 6 surfaces; H-07, H-10, H-11 compliance explicitly designed in |
| Evidence Quality | 0.15 | 0.90 | 0.135 | 12 evidence traceability entries with specific ADR-001 section citations; DREAD likelihood/impact ratings lack explicit justification text per threat |
| Actionability | 0.15 | 0.87 | 0.131 | Module decomposition implementable from this design; interface contracts are concrete Python; controls mapped to implementation phase and file location; pytest fixture bodies are stubs reducing immediate implementability |
| Traceability | 0.10 | 0.93 | 0.093 | Threat-to-control mapping 1:1 complete (36:36); architecture traced to 12 ADR-001 evidence IDs; NIST CSF 2.0 function assigned to every control |
| **TOTAL** | **1.00** | | **0.889** | |

*Composite rounded to 0.890.*

---

## Detailed Dimension Analysis

### Completeness (0.82/1.00)

**Evidence:**

All four architectural layers are present with dedicated section coverage: Layer 1 (CI/CD Gate) through Layer 4 (Statistical Engine) each appear in the system context diagram (lines 53-104), hexagonal diagram (lines 108-201), module decomposition (lines 203-283), dependency graph (lines 304-388), and integration patterns (lines 397-529). This is comprehensive.

Interface contracts are thorough: 10 domain types in `types.py` (ScoreArray, VersionKey, WilcoxonResult, MRResult, RegressionResult, ConfidenceInterval, EvaluationReport, BaselineRecord, EvaluationTier, TestVerdict), 3 port protocols (EvaluationPort, BaselinePersistencePort, ReportOutputPort), the full `stats.py` shared module, and 3 external interface contracts (GHA workflow, Docker mounts, pytest fixtures). The shared stats.py interface explicitly addresses the PROJ-017 compatibility requirement with both Wilcoxon (PROJ-035) and BCa bootstrap (PROJ-017) entry points.

**Gaps:**

1. **Attack Surface 6 STRIDE coverage is incomplete.** Attack Surface 6 (Statistical Comparison Engine) contains only 3 threats: T-34 (S: Spoofing), T-35 (T: Tampering), T-36 (T: Tampering). The categories R (Repudiation), I (Information Disclosure), D (Denial of Service), and E (Elevation of Privilege) have zero representation. This is a structural gap -- the self-review checklist at line 1515 states "STRIDE analysis covers all 6 attack surfaces" and claims 36 threats, but does not verify that all 6 STRIDE categories are represented per surface. For comparison, all other 5 attack surfaces have all 6 STRIDE categories covered (or nearly so). The statistical engine has meaningful R, I, D, E threat scenarios: evaluation results could be repudiated (no audit trail from stats module), score distributions could be disclosed in verbose logs, the engine could be DoS'd with extremely large score arrays (N = 100,000), and a zero-variance attack on the engine could bypass the CI gate (partial elevation).

2. **pytest fixture bodies are stubs.** The conftest.py code in section 2.3 (lines 978-1030) defines 5 fixtures (`version_a_key`, `version_b_key`, `evaluator`, `baseline_store`, `report_generator`) all with body `...`. While this is a "design" document (not implementation), the concrete fixture for `evaluation_tier` (which is fully implemented, lines 978-993) shows the document does provide full implementations when warranted. The stub bodies reduce the actionable completeness of the interface contract section.

3. **No MR port protocol defined.** The metamorphic relations layer has a well-defined ABC (`MetamorphicRelation`) in `metamorphic/base.py`, but there is no port protocol analogous to `EvaluationPort` for the MR layer. The integration pattern (section 1.5 Pattern 2, lines 433-467) describes how MRs plug into the pipeline, but the formal port contract for MR invocation from the evaluation layer is absent.

4. **Observability port is marked optional but not fully specified.** The Langfuse observability adapter is mentioned in the context diagram (line 94) and hexagonal diagram (lines 184-188), and a port is listed (line 195-198), but no protocol definition is provided for the Observability port.

**Improvement Path:**

Add R, I, D, and E threats for Attack Surface 6 (minimum 4 additional threat rows). Implement the `version_a_key`, `version_b_key`, `evaluator`, `baseline_store`, and `report_generator` fixture bodies to the same completeness level as `evaluation_tier`. Define a `MetamorphicRelationPort` protocol analogous to `EvaluationPort`.

---

### Internal Consistency (0.92/1.00)

**Evidence:**

Module boundaries in section 1.3 are fully consistent with the dependency graph in section 1.4. Every module identified as [DOMAIN] in the module decomposition appears in the domain core box of the dependency graph. Every module identified as [ADAPTER] appears in the adapter sections. Every module identified as [PORT] appears as a protocol interface separating domain from adapter.

The threat-to-control mapping is 1:1 complete. The STRIDE table for each attack surface references exactly one mitigation control (MC-NN) per threat, and the Controls Index in section 4.1 lists all 36 controls MC-01 through MC-36 with implementation locations. No threats are unmapped and no controls are orphaned.

The `types.py` definitions are internally consistent with their usage across interface contracts. `ScoreArray` (lines 600-623) uses `tuple[float, ...]` for immutability, consistent with the `WilcoxonResult` parameters (lines 642-652) and `stats.py` function signatures (lines 1128-1150).

**Gaps:**

1. **DREAD priority ordering is inconsistent with DREAD scores.** Section 4.2 DREAD matrix (lines 1437-1446) shows T-19 (LLM API rate limiting) with the highest DREAD score of 8.0, yet it is ranked Priority 7 out of 8. T-02 (YAML prompt injection) has DREAD score 7.2 but is Priority 1. T-20 (cost explosion) has DREAD score 7.4 but is Priority 4. The document explains: "Threats are ordered by a combination of DREAD score and impact severity" (line 1450) -- but the resulting ordering does not follow a consistent rule. If ordered by DREAD score: T-19 (8.0), T-02 (7.2), T-20 (7.4), ... If ordered by impact: the explanation inverts T-19 vs T-02 without explicit impact scoring. This is a weak internal inconsistency: the DREAD scores are computed but the priority ordering does not mechanically derive from them, and no explicit secondary ordering criterion is defined that would produce the observed sequence.

2. **`EvaluationTier` enum has `SMOKE = N=1` but test scoring says `SMOKE: structural only`.** The type definition (line 572) states `SMOKE = "smoke"` with comment `N=1, structural checks only, $0`. Section 1.5 Pattern 1 (lines 407-412) describes Smoke as "Smoke: non-agent-def changes (structural only)" -- consistent. However, the statistical engine's `InsufficientSamplesError` (lines 1239-1253) references `N >= 20` for Wilcoxon and `N >= 30` for BCa bootstrap, with the error message "Use Smoke mode for single-run structural checks only." This is consistent, but the `SMOKE = N=1` label in the enum comment implicitly suggests Smoke runs the statistical engine with N=1, which would always raise `InsufficientSamplesError`. The document does not clarify that the statistical engine is bypassed entirely in Smoke mode, not just reduced to N=1. Minor ambiguity.

**Improvement Path:**

Add a column to the DREAD table (e.g., "Priority Score" = DREAD + Impact Weight) that mechanically produces the priority ordering shown. Clarify that Smoke tier bypasses the statistical engine entirely (not just uses N=1).

---

### Methodological Rigor (0.91/1.00)

**Evidence:**

The hexagonal architecture is correctly applied. The document correctly distinguishes Domain Core, Inbound Adapters, Outbound Adapters, Inbound Ports, and Outbound Ports (sections 1.2 and 1.4). The "Adapters --> Domain Core <-- Ports" dependency direction (line 312) is architecturally correct. The forbidden dependencies list (lines 375-381) explicitly prevents 6 specific domain-to-adapter violations. The H-07 enforcement rules in section 1.4 (lines 391-395) correctly state the directional constraint.

STRIDE is applied systematically across 5 of 6 attack surfaces. The 5 complete surfaces each have all 6 STRIDE categories (S, T, R, I, D, E) represented, with meaningful threat descriptions that are specific to the attack surface rather than generic.

H-07, H-10, and H-11 compliance is explicitly designed in: H-10 (one class per file) has a dedicated compliance table (lines 285-301) mapping 14 files to their single responsibility; H-11 (type hints + docstrings) is demonstrated by all interface contracts having full type annotations and docstrings; H-07 (domain layer isolation) has the forbidden dependencies list.

DREAD scoring is applied to all 8 High-risk threats across 5 dimensions with computed scores (lines 1437-1447). NIST CSF 2.0 functions are assigned to all 36 controls.

Trust boundaries are explicitly mapped (5 boundaries, section 3.0, lines 1270-1307) before the threat analysis begins, which is correct STRIDE methodology.

**Gaps:**

1. **Attack Surface 6 STRIDE coverage is incomplete methodologically.** Only Spoofing and Tampering are represented for the Statistical Engine. This is not merely a completeness issue -- it is a methodological gap. STRIDE requires systematic analysis of all 6 categories per surface. The statistical engine has legitimate R, I, D, E threat vectors that were not analyzed.

2. **No explicit metamorphic relation tolerance calibration justification.** The MR definitions reference "tolerance" (line 667) but no methodology section addresses how tolerance thresholds (e.g., 0.05 for paraphrase consistency) are derived. ADR-001 likely discusses this, but the system design does not carry forward the justification.

3. **No sequence diagram or interaction model.** For a C4 criticality design, a sequence diagram showing the full evaluation flow (GHA event -> promptfoo -> assertion provider -> DeepEval -> MR check -> stats engine -> verdict -> PR comment) would provide methodological rigor that the ASCII flow diagrams in sections 1.5 begin but do not complete. The integration patterns in section 1.5 are approximations of sequence diagrams but lack actor lifelines and synchronization points.

**Improvement Path:**

Complete STRIDE for Attack Surface 6 (4 additional categories). Add a tolerance derivation section to section 1.3 or the MR domain module descriptions. Add a formal sequence diagram for the end-to-end evaluation flow.

---

### Evidence Quality (0.90/1.00)

**Evidence:**

The Evidence Traceability section (lines 1529-1543) provides 12 entries (ET-01 through ET-12) each with Source, Specific Location within ADR-001, and the Design Element Supported. This creates a verifiable chain from design decisions to their ADR-001 source. For example, ET-09 traces `stats.py` shared interface to "ADR-001 L1: PROJ-017 Relationship -- Shared Infrastructure section"; ET-06 traces the threat model to "ADR-001 L1: Risks -- FM-001 through FM-010 FMEA table."

NIST CSF 2.0 function assignment to all 36 controls (section 4.1) provides external framework grounding for the security controls.

DREAD scoring produces quantified risk values rather than purely subjective ratings for the 8 high-risk threats.

**Gaps:**

1. **STRIDE threat likelihood and impact ratings lack per-threat justification.** Each threat row has Likelihood (L/M/H), Impact (M/H), and Risk (Low/Medium/High) ratings, but no justification text appears in the table or in a footnote. For example, T-02 (YAML prompt injection) is rated Likelihood=H, Impact=H but the rationale for H likelihood (vs. M, given that test YAML files are PR-reviewed) is not stated. At C4 criticality, threat likelihood ratings should be explicitly justified.

2. **DREAD scoring rationale is absent at the dimension level.** The DREAD matrix provides 5 dimension scores per threat but no explanation of why T-02 scores Damage=8 vs. T-35 scoring Damage=9. The final scores appear without sub-dimension reasoning.

3. **ET-12 evidence trace is too coarse.** ET-12 traces H-07, H-10, H-11, H-05, H-20 to "Jerry CLAUDE.md" and "Architecture constraints applied to module decomposition." These rules actually come from `quality-enforcement.md`, `architecture-standards.md`, and `coding-standards.md` respectively -- not from CLAUDE.md directly. CLAUDE.md merely references those files. This is a minor traceability inaccuracy.

**Improvement Path:**

Add a one-sentence likelihood justification for each High-rated threat (at minimum). Add a footnote table explaining DREAD dimension scores for the top 3 threats. Correct ET-12 to reference the specific rule files rather than CLAUDE.md.

---

### Actionability (0.87/1.00)

**Evidence:**

The module decomposition (section 1.3) provides a complete directory tree with every file named, its hexagonal classification ([DOMAIN], [ADAPTER], [PORT]), and its responsible class from the H-10 compliance table. An implementation engineer can directly create this directory structure and file set from the design.

Interface contracts are concrete Python code with full type annotations, docstrings, and validation logic in `__post_init__` methods (e.g., `VersionKey.__post_init__` at lines 588-597 validates commit hash length and `.md` extension). The `stats.py` interface provides all 6 function signatures with complete parameter documentation, return type documentation, and exception documentation.

Security controls in section 4.1 are mapped to specific implementation files (e.g., MC-02: `jerry/testing/evaluation/deepeval_adapter.py`), and section 4.3 maps controls to implementation phases (A through E) aligned to the ADR-001 roadmap.

The Docker invocation (lines 950-959) is a concrete, runnable command with all security flags specified.

**Gaps:**

1. **pytest fixture stubs are not implementable.** Five of 6 fixtures in conftest.py (lines 996-1030) have body `...`. The `version_a_key` and `version_b_key` fixtures are critical integration points -- they need to read git environment variables (`github.event.pull_request.base.sha`, `github.event.pull_request.head.sha`) and construct `VersionKey` objects. Without these implementations, an engineer cannot directly implement the test infrastructure from this design document.

2. **No concrete YAML test case example.** The module decomposition lists `ps_researcher.yaml`, `ps_analyst.yaml`, etc. but the document does not provide a sample YAML test case showing the exact promptfoo format, the assertion types (`type: python`), and the custom assertion provider invocation. The external interface section (2.3) shows the GHA workflow contract but not the promptfoo YAML format. This is a gap for the engineer implementing Layer 1.

3. **MR tolerance thresholds are not specified.** The `MRResult` type includes `tolerance: float` (line 670) and the integration patterns reference "tolerance" (line 449: "|S_original - S_para| <= tolerance"), but no concrete tolerance values are provided in the design. An engineer implementing the MR classes does not know what tolerance to use.

**Improvement Path:**

Implement the 5 stub pytest fixtures with their core logic. Add a sample `ps_researcher.yaml` promptfoo test case (minimum: 10 lines showing provider, vars, and python assertion). Specify default tolerance values for each MR (MR-001 through MR-005) with derivation rationale.

---

### Traceability (0.93/1.00)

**Evidence:**

The threat-to-control mapping is complete and bidirectional. Each of the 36 threats (T-01 through T-36) has exactly one mitigation control reference in its table row. The Controls Index (section 4.1) lists all 36 controls (MC-01 through MC-36) each with implementation location. Cross-referencing any threat ID to its control and then to its implementation file is possible in one pass.

Architecture-to-ADR-001 traceability is provided via 12 evidence entries (ET-01 through ET-12) with specific section citations. The connection from design decisions to source ADR is documented explicitly rather than implied.

The self-review checklist (section S-010, lines 1513-1524) provides a verification record of 12 compliance checks, each marked complete.

**Gaps:**

1. **Missing traceability from MR definitions to requirements.** The 5 metamorphic relations (MR-001 through MR-005) appear in the module decomposition and integration patterns, but no evidence entry traces these specific MRs to their requirement source in ADR-001 or the harness requirements document. The document references "PROJ-036 Orchestration Plan, Stream 1B specification" (ET-11) as the scope source but does not trace individual MR selection to ADR-001's oracle problem analysis.

2. **ET-12 traceability inaccuracy noted above.** The rule references in ET-12 point to CLAUDE.md rather than the specific `.context/rules/` files where H-07, H-10, H-11 are actually defined.

3. **No traceability entry for security control design patterns.** The NIST CSF 2.0 alignment in section 4.2 references external framework mappings, but there is no evidence entry tracing security control selection (e.g., MC-14: cap-drop, no-new-privileges) to the specific source that justified these controls (ADR-001's Docker mitigation discussion or an external security reference).

**Improvement Path:**

Add ET-13 tracing MR-001 through MR-005 to ADR-001's oracle problem analysis (Phase 1A L2 Identified Gap #1; Phase 3 PAT-001). Correct ET-12. Add ET-14 tracing Docker security controls to ADR-001 Consequences Negative #2 and FM-001 FMEA entry.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness | 0.82 | 0.89 | Add R, I, D, E threats for Attack Surface 6 (Statistical Engine). Minimum: 4 threat rows covering repudiation of statistical outputs, disclosure of score distributions in logs, DoS via large score arrays, and near-zero-variance array bypass. |
| 2 | Actionability | 0.87 | 0.93 | Implement the 5 stub pytest fixtures (`version_a_key`, `version_b_key`, `evaluator`, `baseline_store`, `report_generator`) with their core logic using git environment variables. |
| 3 | Completeness | 0.82 | 0.89 | Add a sample promptfoo YAML test case for `ps_researcher.yaml` showing the exact provider block, vars, and `type: python` assertion with the custom assertion provider invocation. |
| 4 | Actionability | 0.87 | 0.93 | Specify default tolerance values for MR-001 through MR-005 (e.g., MR-001: 0.05, MR-002: directional-only, MR-003: 0.05, MR-004: 0.03, MR-005: 0.08) with derivation rationale from ADR-001 debiasing research. |
| 5 | Internal Consistency | 0.92 | 0.95 | Add a "Priority Score" column to the DREAD table that mechanically produces the priority ordering (e.g., Priority Score = DREAD_score * integrity_weight) so priority ordering is derivable rather than stated. |
| 6 | Evidence Quality | 0.90 | 0.93 | Add one-sentence likelihood justification for each H-rated threat. Correct ET-12 to reference `.context/rules/architecture-standards.md` and `.context/rules/coding-standards.md`. |
| 7 | Traceability | 0.93 | 0.95 | Add ET-13 (MR selection -> ADR-001 Phase 1A oracle problem) and ET-14 (Docker security controls -> ADR-001 Consequences + FM-001). |
| 8 | Methodological Rigor | 0.91 | 0.94 | Add MR tolerance calibration methodology section explaining how the tolerance thresholds are derived (statistical power analysis or empirical calibration from prior evaluation data). |

---

## Strengths

1. **Hexagonal architecture implementation is exemplary.** The forbidden-dependency list (6 explicit violations), the H-07 enforcement rules, and the explicit [DOMAIN]/[ADAPTER]/[PORT] annotations throughout the module decomposition demonstrate genuine architectural rigor -- not just labeling.

2. **STRIDE coverage for 5 attack surfaces is thorough.** Each of the 5 complete surfaces has all 6 STRIDE categories represented with specific, non-generic threat descriptions. The attacker motivation and technical mechanism are clear for each threat.

3. **Interface contracts are concrete and implementable.** The `types.py` definitions provide production-quality frozen dataclasses with `__post_init__` validation, appropriate type annotations (`tuple[float, ...]` for immutability), and docstrings meeting H-11 standards.

4. **Security controls are fully mapped with implementation locations.** All 36 controls name a specific file or configuration location. This is uncommon in design documents and significantly increases the actionability of the security design.

5. **PROJ-017 compatibility is explicitly designed.** The `stats.py` module correctly provides both Wilcoxon (PROJ-035) and BCa bootstrap (PROJ-017) entry points on the same `ScoreArray` type, with explicit import isolation (H-07) documented at the module docstring level.

6. **Evidence traceability section is structured and specific.** The 12 evidence entries with Source + Specific Location + Design Element create a verifiable traceability chain rather than the generic "as per ADR-001" references common in design documents.

---

## Weaknesses

1. **Attack Surface 6 has systematic STRIDE gaps.** Only S and T are covered for the Statistical Comparison Engine. R, I, D, E are missing entirely. This is not a matter of judgment -- it is an incomplete application of the stated methodology for one of the 6 attack surfaces.

2. **pytest fixture stubs reduce immediate implementability.** Five critical test infrastructure fixtures have body `...`. For a C4 criticality deliverable, the interface contract section should provide complete implementations for all fixtures that are not trivially delegated.

3. **DREAD priority ordering lacks a mechanical derivation.** The priority column does not follow DREAD score ordering (T-19 highest DREAD = 8.0 but Priority 7) and the stated secondary criterion ("integrity vs. operational disruption") is not scored, making the priority column appear post-hoc rather than derived.

4. **MR tolerance values are unspecified.** Engineers implementing MR-001 through MR-005 cannot determine the tolerance threshold from this design document. This is a gap between design and implementation readiness.

5. **ET-12 cites CLAUDE.md for rules that live in `.context/rules/` files.** Minor but meaningful for traceability accuracy at C4 criticality.

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing weighted composite
- [x] Evidence documented for each score (specific line numbers cited)
- [x] Uncertain scores resolved downward (Completeness 0.82 not 0.85; Actionability 0.87 not 0.90)
- [x] First-draft calibration considered (this is iteration 1; scores reflect actual gaps not aspirational quality)
- [x] No dimension scored above 0.95 without exceptional evidence
- [x] Attack Surface 6 incomplete STRIDE coverage scored as a real gap reducing Completeness, Methodological Rigor, and Evidence Quality, not smoothed over by overall document quality

---

## Session Context (Orchestrator Handoff)

```yaml
verdict: REVISE
composite_score: 0.890
threshold: 0.94
weakest_dimension: Completeness
weakest_score: 0.82
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Add R, I, D, E threats for Attack Surface 6 (Statistical Engine) -- 4 missing STRIDE categories"
  - "Implement 5 stub pytest fixtures in conftest.py section with actual git/env logic"
  - "Add sample ps_researcher.yaml promptfoo test case with python assertion type"
  - "Specify MR-001 through MR-005 default tolerance values with derivation rationale"
  - "Add mechanical derivation for DREAD priority column (priority scoring formula)"
  - "Add per-threat likelihood justification for H-rated threats"
  - "Add ET-13 (MR selection) and ET-14 (Docker controls) evidence traceability entries"
  - "Correct ET-12 to reference .context/rules/ files, not CLAUDE.md"
```
