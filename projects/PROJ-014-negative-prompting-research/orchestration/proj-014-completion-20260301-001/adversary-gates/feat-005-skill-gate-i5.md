# Quality Score Report: Prompt Engineering SKILL.md (Iteration 5)

## L0 Executive Summary
**Score:** 0.9325/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.88)
**One-line assessment:** SKILL.md is structurally sound with all i4 fixes verified, but a residual P-002 inconsistency between the SKILL.md Constitutional Compliance table (claims universal P-002 adherence) and pe-scorer.governance.yaml (omits P-002, sets output.required: false) keeps the score below the 0.95 C4 threshold.

## Scoring Context
- **Deliverable:** `skills/prompt-engineering/SKILL.md`
- **Supporting Artifacts:** `skills/prompt-engineering/agents/pe-builder.governance.yaml`, `skills/prompt-engineering/agents/pe-constraint-gen.governance.yaml`, `skills/prompt-engineering/agents/pe-scorer.governance.yaml`
- **Deliverable Type:** Design (Skill definition)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Score:** i4 = 0.924 (REVISE)
- **Iteration:** 5 (FINAL per FA-03)
- **Scored:** 2026-03-01T00:00:00Z

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.9325 |
| **Threshold** | 0.95 (C4) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (standalone scoring) |

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.94 | 0.1880 | Nav table complete with 8 sections; Integration Points present; Build-Score-Iterate workflow documented; minor gap: pe-builder acceptance quality threshold undefined |
| Internal Consistency | 0.20 | 0.88 | 0.1760 | SKILL.md claims universal P-002 adherence; pe-scorer.governance.yaml omits P-002 from constitution.principles_applied and sets output.required: false — direct contradiction |
| Methodological Rigor | 0.20 | 0.95 | 0.1900 | Section ordering correct (Document Sections before Document Audience, NAV-002 compliant); all structural requirements met; rigorous constitutional compliance table with consequences |
| Evidence Quality | 0.15 | 0.93 | 0.1395 | PROJ-014 statistical finding cited with p-value and source files; 7-reference table; PROJ-006 added in i5; minor: P-002 universality claim unsupported given pe-scorer exception |
| Actionability | 0.15 | 0.96 | 0.1440 | Three invocation options with code examples; copy-paste Quick Reference; Build-Score-Iterate workflow diagram; Integration Points resolves tool-selection ambiguity; Routing Disambiguation with consequences |
| Traceability | 0.10 | 0.95 | 0.0950 | Full chain: SKILL.md → research files → SSOT rules; P-004 now in all 3 governance YAMLs; schema validation headers in governance YAMLs |
| **TOTAL** | **1.00** | | **0.9325** | |

## Detailed Dimension Analysis

### Completeness (0.94/1.00)

**Evidence:**
- Navigation table (lines 27-39) lists all 8 sections including "Invoking an Agent" — F-01 fix from i4 verified.
- Document Sections table appears at line 27, before Document Audience (Triple-Lens) at line 42 — F-03 fix from i4 verified.
- Integration Points section (lines 249-257) documents all 4 integration relationships: `/adversary`, `/problem-solving`, `prompt-templates.md`, `prompt-quality.md` — F-04 fix from i4 verified.
- Build-Score-Iterate workflow (lines 237-246) provides end-to-end numbered steps with P-003 coordination note.
- P-003 Compliance section (lines 109-132) includes explicit ASCII architecture diagram.
- All 3 core agent capabilities documented: pe-builder (5-element anatomy), pe-constraint-gen (NPT formatting), pe-scorer (7-criterion scoring).
- PROJ-006 reference added at line 310 (additional i5 improvement verified).
- When to Use / When NOT to use: Both explicitly documented with consequences.

**Gaps:**
- pe-builder's Quality Threshold for built prompts is not defined in SKILL.md. The Quick Reference mentions pe-scorer will score a prompt, but no threshold is stated for when a pe-builder-constructed prompt "passes" before the user proceeds. The Build-Score-Iterate workflow says "until score >= target" but leaves "target" undefined — the user must know to set their own target. This is a usability gap.
- The SKILL.md does not document the maximum iteration ceiling for the Build-Score-Iterate loop beyond "3 iterations" (line 243). This is implied from prompt-quality.md practice but not explicit in the workflow.

**Improvement Path:**
Add a table or note in the Build-Score-Iterate workflow specifying the default score target (e.g., "default target: 90 per prompt-quality.md C2 recommendation; adjust by task type per quality rubric threshold table"). This closes the undefined-target gap and makes the workflow fully self-contained.

---

### Internal Consistency (0.88/1.00)

**Evidence:**
The Constitutional Compliance section (lines 276-286) states: "All agents adhere to the **Jerry Constitution v1.0**" and lists P-002 with the requirement "NEVER produce transient-only output -- persist all artifacts to files."

pe-builder.governance.yaml `constitution.principles_applied` (line 44): includes P-002 — CONSISTENT.
pe-constraint-gen.governance.yaml `constitution.principles_applied` (line 46): includes P-002 — CONSISTENT.
pe-scorer.governance.yaml `constitution.principles_applied` (lines 41-46): lists P-003, P-020, P-022, P-004, P-011 — **P-002 is ABSENT** — INCONSISTENT with SKILL.md claim.

pe-scorer.governance.yaml `output.required: false` (line 48) explicitly signals that pe-scorer does not mandate file persistence. This is architecturally reasonable (pe-scorer can return inline scores), but it contradicts the SKILL.md statement that ALL agents adhere to P-002 (file persistence).

Additionally, pe-scorer's `capabilities.forbidden_actions` (lines 33-38) contains 5 entries. Unlike pe-builder and pe-constraint-gen, pe-scorer does NOT include a P-002 forbidden action entry. This is a third data point confirming pe-scorer intentionally opts out of P-002 compliance — in contradiction with SKILL.md's blanket claim.

All other consistency checks pass:
- Agent models (opus/sonnet/haiku) match cognitive mode taxonomy in agent-development-standards.md.
- NPT format table (lines 66-70) matches pe-constraint-gen's output filtering rules.
- P-003 hierarchy diagram (lines 113-131) is consistent with H-01/P-003 single-level nesting.
- Routing Disambiguation (lines 262-272) is consistent with mandatory-skill-usage.md trigger map.

**Gaps:**
- SKILL.md Constitutional Compliance table claims universal P-002 adherence, but pe-scorer.governance.yaml omits P-002 from constitution.principles_applied and sets output.required: false. These are directly contradictory.

**Improvement Path:**
Option A: Add a footnote to the Constitutional Compliance table: "P-002 applies to pe-builder and pe-constraint-gen. pe-scorer supports optional file persistence (output.required: false); inline scoring is permitted when no file output is requested."
Option B: Add P-002 to pe-scorer's constitution.principles_applied with a conditional note, and change output.required to conditionally true.
Option A is preferred as it accurately reflects the existing governance without requiring pe-scorer governance changes.

---

### Methodological Rigor (0.95/1.00)

**Evidence:**
- Section ordering: Document Sections (lines 27-39) precedes Document Audience (lines 42-51) — NAV-002 compliant. F-03 fix verified.
- H-23 nav table: Present with 8 entries, all with anchor links — compliant.
- H-26 description in YAML frontmatter (lines 3-4): Includes WHAT (structured prompt construction and quality validation), WHEN (invoke when building structured prompts, generating NPT-009/NPT-013 constraints, or scoring prompt quality), and trigger keywords (activation-keywords list).
- H-25 compliance: Skill folder `prompt-engineering` is kebab-case; SKILL.md has correct capitalization.
- Available Agents table (lines 95-99): Complete with agent filename, model, cognitive mode, purpose — meets AD-M-003 description quality standard.
- P-003 compliance section: Explicitly documented with ASCII diagram showing orchestrator-worker hierarchy — goes beyond minimum.
- Constitutional Compliance table (lines 278-286): Includes principle, requirement, and consequence columns — structured and complete.
- Architecture Notes (lines 291-310): Provides design rationale linking to 3 knowledge sources with numbered justification.

**Gaps:**
- Minor: SKILL.md YAML frontmatter uses `version: "1.0.0"` which is not an official Claude Code frontmatter field (per agent-development-standards.md, the 12 recognized fields do not include version). This is a non-standard field at the skill level (SKILL.md files are not agent definitions), but it signals a slight format inconsistency. Inconsequential for operation since unrecognized fields are silently ignored.

**Improvement Path:**
Score is already strong at 0.95. The YAML frontmatter version field, while non-standard for Claude Code, is an acceptable convention at the skill level. No urgent change required for this dimension.

---

### Evidence Quality (0.93/1.00)

**Evidence:**
- PROJ-014 statistical finding (line 56): "NPT-013 structured negation... achieves 100% compliance vs 92.2% for positive-only framing (p=0.016, CONDITIONAL GO via PG-003)" — cited to `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-6/final-synthesis.md` and `ab-testing-synthesis.md` at lines 306-307. Strong quantitative evidence with specific source file paths.
- 7-criterion rubric: Cited to `.context/rules/prompt-quality.md` — appropriate SSOT reference.
- 5-element prompt anatomy: Cited to `.context/rules/prompt-quality.md` — consistent.
- NPT-009/NPT-013 formats: Cited to `skills/prompt-engineering/rules/npt-pattern-reference.md` — specific.
- PROJ-006 research (line 310): "5-element anatomy derivation, quality rubric development, template validation" — adds depth to the evidence chain.
- Agent development standards: Referenced in Architecture Notes for schema compliance.
- Governance YAML headers: "Validated by: docs/schemas/agent-governance-v1.schema.json" — schema citation.

**Gaps:**
- The SKILL.md claims "All agents adhere to... P-002" but pe-scorer.governance.yaml omits P-002. This blanket claim lacks supporting evidence (because the evidence actually contradicts it).
- The Architecture Notes claim the scoring formula is `total = sum((raw_score_N / 3) * weight_N * 100)` — this is correct and consistent with prompt-quality.md, but the formula is presented inline without a citation marker to prompt-quality.md at that specific point (the reference table at lines 302-310 covers it globally, which is acceptable).

**Improvement Path:**
The P-002 inconsistency identified in Internal Consistency also reduces evidence quality slightly. Correcting the SKILL.md Constitutional Compliance table per the Option A recommendation above would resolve this dimension gap too.

---

### Actionability (0.96/1.00)

**Evidence:**
- Option 1/2/3 invocation (lines 137-184): Three complete invocation patterns including natural language, explicit agent request, and Task tool Python snippet — immediately implementable.
- Quick Reference section (lines 188-246): Four fully-worked examples with copy-paste commands and expected outcomes.
- Common Workflows table (lines 226-234): 6 rows mapping need → agent → example — decision tree for users.
- Build-Score-Iterate workflow (lines 237-246): Numbered steps with P-003 coordination note — procedural clarity.
- Routing Disambiguation table (lines 264-272): 6 rows specifying when NOT to use the skill, what to use instead, and the consequence of misrouting — prevents wrong-direction work.
- Integration Points table (lines 251-256): 4 rows clarifying relationship with `/adversary`, `/problem-solving`, `prompt-templates.md`, `prompt-quality.md` — resolves tool-selection ambiguity. F-04 fix verified.
- Agent Routing Guide (lines 103-107): Keyword-to-agent mapping with rationale — routes users to correct agent without guesswork.
- NPT format XML example (lines 207-214): Actual XML output rendered — users know exactly what to expect.

**Gaps:**
- "Build, score, iterate" workflow says "until score >= target or 3 iterations reached" but does not define what "target" defaults to. This creates a small actionability gap at the final step of the workflow.

**Improvement Path:**
Add a default target value (e.g., "target: >= 90 for most use cases; adjust per prompt-quality.md threshold table") to the Build-Score-Iterate workflow. One sentence resolves this gap and would push this dimension to 0.97+.

---

### Traceability (0.95/1.00)

**Evidence:**
- P-004 in all 3 governance YAMLs: pe-builder line 44, pe-constraint-gen line 46, pe-scorer line 44 — F-02 fix from i4 verified. All declare `P-004: Source Attribution`.
- References table (lines 302-310): 7 entries with full repo-relative paths — complete traceability chain.
- pe-constraint-gen forbidden_actions (lines 37): NPT constraint cites `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-6/final-synthesis.md` — traces enforcement to evidence.
- Governance YAML headers: "Validated by: docs/schemas/agent-governance-v1.schema.json" — schema citation.
- SKILL.md frontmatter: `SSOT Reference: .context/rules/prompt-quality.md, .context/rules/prompt-templates.md` — SSOT declared.
- Constitution compliance table: Each principle is named by ID (P-002 through P-022) enabling lookup in Jerry Constitution.
- PROJ-006 reference: Added at line 310, closing the 5-element anatomy research chain.

**Gaps:**
- Minor: The `version: "1.0.0"` field in SKILL.md frontmatter and the `Framework: Jerry Framework v0.9.0` metadata in the document header trace to no specific ADR or versioning document — these version claims are orphaned from a traceability perspective. Minor issue.

**Improvement Path:**
Score is already strong. If version traceability is desired, adding a note that `v0.9.0` references the Jerry Framework version at PROJ-014 creation time would close this gap.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.88 | 0.94+ | Add P-002 footnote to Constitutional Compliance table: "P-002 applies to pe-builder and pe-constraint-gen (output.required: true). pe-scorer supports optional file persistence (output.required: false); inline scoring output is permitted." This resolves the direct contradiction between SKILL.md's universal P-002 claim and pe-scorer.governance.yaml. One sentence addition. |
| 2 | Completeness | 0.94 | 0.96+ | Add a default score target to the Build-Score-Iterate workflow: "Default target: >= 90 for standard prompts; adjust per prompt-quality.md threshold table (C1/architecture: 90-92, security: 92-95)." One sentence resolves the undefined-target gap. |
| 3 | Evidence Quality | 0.93 | 0.95+ | Resolved automatically if Priority 1 is implemented (the P-002 universality claim will become accurate). |
| 4 | Actionability | 0.96 | 0.97+ | Resolved automatically if Priority 2 is implemented (the Build-Score-Iterate workflow will have a concrete target). |

## Leniency Bias Check
- [x] Each dimension scored independently before computing weighted composite
- [x] Evidence documented for each score with specific line references
- [x] Uncertain scores resolved downward: Internal Consistency was borderline 0.88/0.90; resolved to 0.88 because the P-002 inconsistency between SKILL.md and pe-scorer is specific, verifiable, and multi-evidenced (omitted from constitution.principles_applied AND output.required: false AND no P-002 forbidden action entry)
- [x] First-draft calibration not applicable (iteration 5)
- [x] No dimension scored above 0.95 without exceptional evidence (Actionability at 0.96: justified by three distinct invocation options with code, Integration Points section, copy-paste quick reference, workflow diagram, and routing disambiguation with consequences — concrete, multi-faceted actionability evidence)
- [x] Composite verified mathematically: 0.188 + 0.176 + 0.190 + 0.1395 + 0.144 + 0.095 = 0.9325

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.9325
threshold: 0.95
weakest_dimension: internal_consistency
weakest_score: 0.88
critical_findings_count: 0
iteration: 5
improvement_recommendations:
  - "Add P-002 footnote to Constitutional Compliance table clarifying pe-scorer exception (output.required: false). One sentence. Resolves direct contradiction between SKILL.md and pe-scorer.governance.yaml."
  - "Add default score target to Build-Score-Iterate workflow (e.g., >= 90 for standard prompts). Resolves undefined-target gap in actionability."
  - "Evidence Quality improvement is automatic after Priority 1 fix."
  - "Actionability improvement is automatic after Priority 2 fix."
```

---

*Score Report Version: 1.0.0*
*Strategy: S-014 (LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Scored by: adv-scorer*
*Created: 2026-03-01*
