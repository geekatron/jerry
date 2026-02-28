# Quality Score Report: Diataxis Skill Agents (Round 4)

## L0 Executive Summary

**Score:** 0.896/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.88) / Traceability (0.87)
**One-line assessment:** All HARD requirements met and all Round 3 fixes confirmed; four MEDIUM-standard gaps prevent reaching the 0.95 user-specified threshold — the primary blockers are the missing `on_send` in writer agent session contexts, a residual field naming mismatch between classifier output and auditor input, and the undocumented schema reference.

---

## Scoring Context

- **Deliverable:** 12 files — `skills/diataxis/agents/diataxis-{tutorial,howto,reference,explanation,classifier,auditor}.md` + `.governance.yaml`
- **Deliverable Type:** Agent definitions (dual-file architecture per H-34)
- **Criticality Level:** C3 (new skill, >10 files, >1 day to reverse)
- **Scoring Strategy:** S-014 (LLM-as-Judge) + S-007 (Constitutional AI Critique) + S-013 (Inversion) + S-010 (Self-Refine)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`, `.context/rules/agent-development-standards.md`
- **Scored:** 2026-02-27
- **Prior Score (Round 3):** 0.9145 (REVISE)
- **Iteration:** 4

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.896 |
| **User Threshold** | 0.95 |
| **SSOT Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (standalone Round 4 scoring) |

**Note on threshold:** User specified 0.95. Standard H-13 threshold is 0.92. This score (0.896) falls below both. Verdict is REVISE regardless of which threshold is applied.

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.90 | 0.180 | All HARD requirements met; missing `on_send` in 4 writer agent session contexts (AD-M-007 SHOULD) |
| Internal Consistency | 0.20 | 0.88 | 0.176 | `classifier.quadrant` → `auditor.declared_quadrant` naming mismatch documented but unresolved; T2 label with no Bash in explanation minor/documented |
| Methodological Rigor | 0.20 | 0.93 | 0.186 | All 5 R3 fixes confirmed; methodologies rigorous, external criteria loading, deterministic confidence, fully expanded Mixing Resolution Gates |
| Evidence Quality | 0.15 | 0.88 | 0.132 | All claims traceable; model_justification present for opus (R3 fix); confidence derivation is deterministic table not LLM self-assessment |
| Actionability | 0.15 | 0.90 | 0.135 | Very actionable for standalone use; minor gap in pipeline contexts (writer agents lack on_send handoff contract) |
| Traceability | 0.10 | 0.87 | 0.087 | Constitutional principles cited explicitly; no `$schema` field in YAML files; classifier→auditor field mapping documented but asymmetric |
| **TOTAL** | **1.00** | | **0.896** | |

**Composite calculation:** 0.180 + 0.176 + 0.186 + 0.132 + 0.135 + 0.087 = **0.896**

---

## Round 3 Fix Verification

All 5 Round 3 fixes confirmed applied:

| Fix | Status | Evidence |
|-----|--------|----------|
| P1: Auditor verdict vocabulary aligned (PASS/NEEDS REVISION/MAJOR REWORK) | CONFIRMED | `diataxis-auditor.md` Step 6 and `on_send.verdict` in governance YAML both use `PASS|NEEDS REVISION|MAJOR REWORK` |
| P1: Classifier `routing_note` added to `on_send` | CONFIRMED | `diataxis-classifier.governance.yaml` `on_send.routing_note: "Maps quadrant to writer agent: tutorial->diataxis-tutorial, howto->diataxis-howto, reference->diataxis-reference, explanation->diataxis-explanation"` |
| P1: Auditor field name aligned (`declared_quadrant`) | CONFIRMED | `diataxis-auditor.governance.yaml` `on_receive.declared_quadrant` with comment `(maps from classifier.quadrant)` |
| P2: Explanation `model_justification` added | CONFIRMED | In `diataxis-explanation.md` identity section (AD-M-009 cite) and `diataxis-explanation.governance.yaml` `identity.model_justification` field |
| P3: All 4 Mixing Resolution Gates expanded with (a/b/c) steps | CONFIRMED | tutorial/howto/reference/explanation all have 3-step reclassification: (a) report quadrant and flag count, (b) suggest invoking diataxis-classifier, (c) wait for user decision |

---

## Detailed Dimension Analysis

### Completeness (0.90/1.00)

**Evidence:**

All HARD requirements (H-34, H-35) are fully met across all 12 files:
- Dual-file architecture: confirmed for all 6 agents
- Required YAML fields: `version`, `tool_tier`, `identity.role`, `identity.expertise` (min 2 entries each), `identity.cognitive_mode` — present in all 6 YAML files
- Required MD body sections: `<identity>`, `<purpose>`, `<input>`, `<capabilities>`, `<methodology>`, `<output>`, `<guardrails>` — all 7 present in all 6 MD files
- H-35 constitutional triplet (P-003/P-020/P-022): present in all 6 `constitution.principles_applied` arrays
- `capabilities.forbidden_actions` min 3 entries: all 6 have 6 entries each
- `guardrails.output_filtering` min 3 entries: all 6 have 4 entries
- `guardrails.fallback_behavior` valid pattern: all 6 use `warn_and_retry` or `escalate_to_user`
- `validation.post_completion_checks`: present in all 6 YAML files with 4-5 verifiable assertions each
- `output.levels` declared: all 6 present (explanation has L0/L1/L2; others L1)
- `session_context.on_receive`: present in all 5 non-classifier agents
- `session_context.on_send`: present in classifier and auditor

**Gaps:**

AD-M-007 MEDIUM SHOULD: Writer agents (tutorial, howto, reference, explanation) have `session_context.on_receive` only. No `on_send` is declared. This means an orchestrator consuming writer agent output has no structured handoff contract — it must infer the output path from the input context. Technically the file artifact IS the output, but a structured `on_send` would declare at minimum `{ output_path, quadrant, status }` for downstream pipeline consumption. All 4 writer agents are affected.

**Improvement Path:**

Add `session_context.on_send` to each writer agent governance YAML declaring the handoff contract:
```yaml
session_context:
  on_send:
    output_path: "Path to the produced document"
    quadrant: "The quadrant this document belongs to"
    status: "complete|failed"
```

---

### Internal Consistency (0.88/1.00)

**Evidence:**

Strong internal consistency across most pairs:
- Cognitive mode: MD body and YAML `identity.cognitive_mode` match for all 6 agents (systematic x4, convergent x1, divergent x1)
- Tool lists vs. tool tiers: tutorial/howto/reference use T2 tools and T2 tier (consistent); classifier/auditor use T1 tools and T1 tier (consistent)
- Verdict vocabulary: `PASS|NEEDS REVISION|MAJOR REWORK` consistent between auditor MD methodology Step 6 and auditor governance YAML `on_send.verdict`
- Constitutional references: all 6 YAML files reference `docs/governance/JERRY_CONSTITUTION.md` consistently

**Gaps:**

1. **Classifier `quadrant` → Auditor `declared_quadrant` field naming mismatch.** The classifier's `on_send` outputs a field named `quadrant`. The auditor's `on_receive` expects a field named `declared_quadrant`. R3 fixed the auditor's field name but the classifier's `on_send` field remains `quadrant`. The auditor documents this with the comment `(maps from classifier.quadrant)`, but a direct caller reading both schemas would encounter a rename they must handle. The fields contain the same value but have different names.

2. **Explanation `tool_tier: T2` label with no Bash tool.** The governance YAML comment says `# T2 minus Bash -- Bash not needed for explanation writing` but the tier enum is `T2`. Per standards, T2 = "T1 + Write, Edit, Bash." Using `T2` for an agent that does not have Bash creates a technically incorrect tier label. The comment is transparent but the tier label itself is imprecise. A T2-minus-Bash agent is functionally a custom tier that doesn't map cleanly to the T1-T5 vocabulary.

**Improvement Path:**

1. Rename classifier `on_send.quadrant` to `on_send.declared_quadrant` to match auditor's `on_receive.declared_quadrant` — or rename auditor's `on_receive.declared_quadrant` to `on_receive.quadrant` and update the auditor input section comment. One side needs to change to eliminate the asymmetry.

2. Either (a) add Bash back to explanation agent (the least disruptive option — explanation writing rarely needs Bash but it doesn't hurt), or (b) formally document the custom tier in the governance YAML as `tool_tier_override` instead of using the standard T2 label.

---

### Methodological Rigor (0.93/1.00)

**Evidence:**

This is the strongest dimension. Multiple rigorous methodological design decisions:

1. **External criteria loading:** All 6 agents explicitly load quality criteria from `skills/diataxis/rules/diataxis-standards.md` rather than memorizing criteria inline. This is explicitly enforced in both MD body ("do not use memorized criteria") and guardrails ("ALWAYS load quality criteria from diataxis-standards.md"). This prevents criteria drift as the standards evolve.

2. **Deterministic confidence derivation (classifier):** The classifier uses a 4-case lookup table (both unambiguous = 1.00, one mixed = 0.85, both mixed = 0.70, unresolvable = escalate) rather than LLM self-assessment. This is explicitly called out in guardrails: "ALWAYS use deterministic confidence derivation (not LLM self-assessment)."

3. **Fully expanded Mixing Resolution Gates (R3 fix):** All 4 writer agents have the complete 3-step reclassification process:
   - (a) Report current quadrant, acknowledged flag count, dominant foreign quadrant(s)
   - (b) Suggest invoking diataxis-classifier with full document content
   - (c) Wait for user decision before continuing

4. **Verdict thresholds with rationale (auditor):** `PASS: Zero Critical, at most 2 Minor` / `NEEDS REVISION: 1+ Major OR 3+ Minor, zero Critical` / `MAJOR REWORK: 1+ Critical` with explicit rationale: "2-Minor tolerance is intentional — minor style issues should not block publication."

5. **Consistent 6-step pattern across all writer agents:** Understand → Design → Write → Apply Criteria → Self-Review with Mixing Detection → Persist.

6. **Hint handling in classifier (Step 5):** Explicit decision tree for when hint matches vs. conflicts, including: use hint per P-020, calibrate confidence to 0.85 on override, never report 1.00 on conflicting override.

**Gaps:**

Auditor's fallback classification (when no quadrant is declared) explicitly acknowledges it "lacks the classifier's hint handling and full confidence derivation" — this is transparent, not a gap. The pipeline guidance ("invoke diataxis-classifier before the auditor") is appropriate.

The Verification Failure Handling (Step 5b in tutorial and implied in howto/reference) is only explicitly defined in tutorial, not in howto or reference. These agents also use Bash for verification, so a parallel step would strengthen consistency.

**Improvement Path:**

Add explicit `Step 5b: Verification Failure Handling` to howto and reference methodologies matching the tutorial pattern: "If Bash verification of any step fails, annotate the step with `[VERIFICATION-FAILED: {error}]` and warn the user before proceeding."

---

### Evidence Quality (0.88/1.00)

**Evidence:**

1. **Model selection (AD-M-009):** Explanation's `opus` selection is now evidenced in both locations:
   - MD identity section: "Uses opus because explanation writing requires synthesizing design rationale across multiple architectural documents, making non-obvious cross-topic connections, and producing nuanced discursive prose that balances multiple perspectives"
   - Governance YAML: `identity.model_justification: "Opus selected for divergent conceptual exploration requiring creative association, nuanced reasoning, and multi-perspective synthesis"`
   Both are specific and map to documented capabilities from the cognitive mode taxonomy.

2. **Tool tier assignments:** Traceable to the T1-T5 taxonomy in agent-development-standards.md. T1 (classifier/auditor) = read-only evaluation matches the taxonomy's "T1: Evaluation, auditing, scoring, validation" description.

3. **Cognitive mode assignments:** Each assignment is traceable to the taxonomy: systematic for procedural completeness (writer agents, auditor), convergent for focused decision/classification (classifier), divergent for broad conceptual exploration (explanation).

4. **Constitutional compliance claims:** Each YAML entry cites a specific principle with behavioral implication (e.g., "P-003: No Recursive Subagents (Hard) - Worker agent, no Task tool"). Not vague.

5. **Confidence table (classifier):** Deterministic derivation table is self-evidencing.

**Gaps:**

1. The quality criteria labels (T-01 through T-08, H-01 through H-07, etc.) are referenced in agent identity sections but their content is in `diataxis-standards.md`. The agent definitions don't include even a summary of these criteria — they're entirely deferred to runtime loading. While this is the correct design choice (external loading), a reviewer of just the agent files cannot verify whether the criteria enumeration is complete.

2. The `verification_failure_handling` pattern (Step 5b) in tutorial is undocumented for howto/reference though both use Bash for verification — slightly undermines evidence that verification behavior is consistently applied.

**Improvement Path:**

Add a cross-reference in the identity/expertise section noting the specific criteria count per quadrant (e.g., "Diataxis tutorial quadrant quality criteria (T-01 through T-08, 8 criteria)") with a note that these are loaded at runtime from diataxis-standards.md — this makes the criteria count verifiable without requiring runtime file access.

---

### Actionability (0.90/1.00)

**Evidence:**

Writer agents are highly actionable:
- Input sections specify exactly what is required (topic/goal/subject + output path) with clear optionals
- Methodology is numbered and sequential with explicit decision gates
- Output locations are templated and specific
- Fallback behavior is defined for each failure mode
- Post-completion checks are verifiable assertions (not vague)
- Mixing Resolution Gates provide clear 3-way decision trees with escalation criteria

Classifier is highly actionable for its primary use case:
- Two-axis test is a concrete decision procedure
- Confidence table is deterministic (no judgment required)
- Output format is fully specified with all 6 fields
- `routing_note` maps the output directly to the correct writer agent (R3 fix)

Auditor is highly actionable:
- Step 6 includes a full report template with column definitions
- Verdict thresholds are numeric and unambiguous
- All 7 mixing heuristics are enumerated

**Gaps:**

Writer agents lack `on_send` in session context. In an orchestrated pipeline (e.g., an orchestrator that invokes classifier → writer → auditor), the orchestrator has no structured way to know what the writer produced beyond knowing the output_path that was passed as input. The auditor then needs `declared_quadrant` as input, but the writer's `on_send` doesn't confirm the quadrant used. This creates a manual step in pipeline construction.

**Improvement Path:**

Add `session_context.on_send` to writer agents:
```yaml
on_send:
  output_path: "The file path where the document was written"
  quadrant: "The Diataxis quadrant of the produced document"
  status: "complete|failed"
  verification_failures: "Count of [VERIFICATION-FAILED] annotations, if any"
```

---

### Traceability (0.87/1.00)

**Evidence:**

1. All 6 governance YAML files have `constitution.reference: "docs/governance/JERRY_CONSTITUTION.md"` — explicit constitutional anchor
2. All 6 `principles_applied` arrays cite P-003, P-020, P-022 with behavioral descriptions
3. Tool tier choices trace to `agent-development-standards.md` T1-T5 taxonomy
4. Model choices trace to AD-M-009 (model selection standard)
5. Cognitive mode choices trace to the cognitive mode taxonomy in agent-development-standards.md
6. Quality criteria loading traces to `skills/diataxis/rules/diataxis-standards.md` (explicit path in all methodology sections)
7. Template paths are explicit and consistent: `skills/diataxis/templates/{quadrant}-template.md`
8. Classifier → Auditor pipeline is documented in auditor `on_receive.declared_quadrant` with the comment `(maps from classifier.quadrant)`

**Gaps:**

1. **No `$schema` field in governance YAML files.** Per H-34, governance YAMLs "MUST validate against `docs/schemas/agent-governance-v1.schema.json`." Adding `$schema: "../../docs/schemas/agent-governance-v1.schema.json"` to each file would make the schema reference explicit and machine-verifiable without L5 CI tooling. Currently the schema validation link is implicit (handled at L5 CI), but the YAML files themselves don't declare it.

2. **Classifier `quadrant` vs auditor `declared_quadrant` creates a traceability gap.** A reader tracing the data flow from classifier output to auditor input must mentally resolve the field rename. The comment documents this but breaks the direct trace.

3. **Version field is `0.1.0` in all 6 files with no version history.** For initial release this is appropriate, but there's no changelog or source tracking in the YAML files to explain what changed between versions. This will become a traceability concern as the agents evolve.

**Improvement Path:**

1. Add `$schema: "../../docs/schemas/agent-governance-v1.schema.json"` to all 6 governance YAML files (first line or in a comment block). This is a low-effort high-traceability improvement.

2. Align the classifier→auditor field naming (either rename classifier `on_send.quadrant` to `on_send.declared_quadrant` or document the rename in a dedicated `interface_contracts` section).

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.88 | 0.93 | Align field naming: rename `classifier.on_send.quadrant` to `classifier.on_send.declared_quadrant` to match `auditor.on_receive.declared_quadrant`. One-line change in `diataxis-classifier.governance.yaml`. |
| 2 | Completeness + Actionability | 0.90 | 0.95 | Add `session_context.on_send` to writer agents (tutorial, howto, reference, explanation). Declare at minimum: `output_path`, `quadrant`, `status`. Enables pipeline orchestration. |
| 3 | Traceability | 0.87 | 0.92 | Add `$schema: "../../docs/schemas/agent-governance-v1.schema.json"` to all 6 governance YAML files. Makes schema compliance explicit and machine-verifiable. |
| 4 | Internal Consistency | 0.88 | 0.91 | Resolve explanation `tool_tier` label: either (a) add Bash to explanation tools list (simplest — Bash is harmless for explanation writing), or (b) use `tool_tier: T2_no_bash` with a comment and document the custom tier in agent-development-standards.md. |
| 5 | Methodological Rigor | 0.93 | 0.96 | Add explicit `Step 5b: Verification Failure Handling` to `diataxis-howto.md` and `diataxis-reference.md` methodologies, matching the tutorial pattern: annotate with `[VERIFICATION-FAILED: {error}]` and warn user. |
| 6 | Evidence Quality | 0.88 | 0.91 | Add criteria count note to identity sections: "8 criteria (T-01 through T-08) loaded at runtime from diataxis-standards.md" — makes the criteria enumeration verifiable without runtime file access. |

---

## S-007 Constitutional AI Critique Findings

| Principle | Agent(s) | Assessment |
|-----------|----------|------------|
| P-003 (No Recursive Subagents) | All | PASS. No agent includes Task in its tools list. T1 agents (classifier, auditor) explicitly forbid "Invoke writer agents directly (T1 boundary)." Writer agents explicitly declare "Worker only." |
| P-020 (User Authority) | Classifier (hint handling) | PASS. Step 5 handles hint conflicts by using the user hint, setting confidence to 0.85 with rationale, never overriding to LLM preference. Explicit: "use the hint (per P-020 user authority)." |
| P-022 (No Deception) | Classifier, Auditor | PASS. Classifier forbidden actions: "Inflate confidence for ambiguous classifications (P-022)." Auditor: "Inflate or deflate finding severity (P-022)." Both have explicit transparency requirements. |

---

## S-013 Inversion Analysis

**Question:** What would cause this skill to fail systematically in production?

| Failure Mode | Risk | Mitigation Present? |
|---|---|---|
| Criteria drift: agents memorize stale criteria rather than loading from diataxis-standards.md | HIGH | YES — all agents have both methodology instruction and guardrail constraint to load from file |
| Confidence inflation: classifier self-assesses confidence as LLM | HIGH | YES — deterministic confidence table enforced, forbidden action in guardrails |
| Quadrant mixing undetected: writer produces mixed document | MEDIUM | YES — 7 heuristics in auditor, explicit flags in writer self-review steps |
| Pipeline breakage: orchestrator can't route writer output to auditor | MEDIUM | PARTIAL — missing on_send in writer agents creates pipeline gap |
| False classification: user provides wrong quadrant | LOW | YES — hint handling with conflict detection and confidence calibration |
| Field rename friction: classifier→auditor data flow | LOW | PARTIAL — documented in comment but not resolved as clean interface |

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computed
- [x] Evidence documented for each score — specific field names, sections, and gaps cited
- [x] Uncertain scores resolved downward (borderline 0.88 vs 0.90 cases resolved at 0.88)
- [x] First-draft calibration not applicable (Round 4 of iterative revision)
- [x] No dimension scored above 0.95 without exceptional evidence (highest is 0.93 for Methodological Rigor, well-evidenced)
- [x] Score progression reviewed: R3=0.9145, R4=0.896. R4 is lower than R3 despite fixes being confirmed — verified this is justified by independent dimension-level evidence, not scoring artifact

**Calibration note:** R4 score (0.896) is lower than R3 (0.9145). This is correct: the R3 score incorporated strategy execution findings from the adv-executor report which may have been more favorable. R4 is a standalone scorer assessment from first principles. The 4 gaps identified are real (field naming mismatch, missing on_send x4, tool tier label, no schema field) and justify dimension scores in the 0.87-0.93 range. The deliverable is strong work with genuine but targeted remaining gaps.

**Gap to threshold:** 0.95 - 0.896 = 0.054. Achieving 0.95 requires resolving all 6 priority items. The two highest-impact items are Priority 1 (field naming alignment, trivial fix) and Priority 2 (add on_send to writer agents, moderate effort). These alone would add approximately 0.03-0.04 to the composite.
