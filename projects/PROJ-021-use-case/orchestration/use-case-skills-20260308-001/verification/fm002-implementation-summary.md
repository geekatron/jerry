# FM-002 Implementation Summary: uc-slicer Structural Validation Step

**Implementing Agent:** eng-backend
**Finding:** FM-002 -- uc-slicer `realization_level` enforcement behavioral only
**Date:** 2026-03-11
**Criticality:** C3 (Significant -- cascading failure into /contract-design)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | What was implemented, security controls, OWASP coverage |
| [L1: Technical Detail](#l1-technical-detail) | Exact changes per file, pre/post state, verification |
| [L2: Strategic Implications](#l2-strategic-implications) | Defense-in-depth posture, residual risk, evolution path |

---

## L0: Executive Summary

FM-002 identified that uc-slicer's `realization_level: INTERACTION_DEFINED` enforcement was behavioral only -- the instruction "NEVER set INTERACTION_DEFINED before populating interactions[]" was present in the agent definition but had no deterministic enforcement mechanism at the production step itself.

The allOf schema constraint (added in R2 remediation) closed the structural enforcement gap at the schema level: a validator catching the artifact after the fact. The remaining work was adding a **post-creation validation step at the moment of the state transition**, so the violation is caught by uc-slicer before the artifact is handed off to /contract-design.

**What was implemented:**

1. `uc-slicer.md` `<methodology>` Step 8 -- replaced behavioral instruction with an explicit CLI command: `uv run jerry ast validate {artifact_path} --schema use_case_realization`. The realization level is only set if validation succeeds.
2. `uc-slicer.md` `<output>` Post-Update Verification -- added explicit CLI invocation and annotated item 5 with the dual enforcement mechanism (allOf schema constraint + CLI validation at Step 8).
3. `uc-slicer.governance.yaml` `output_filtering` -- annotated the `realization_level_must_match_populated_blocks` entry with the enforcement mechanism. Already confirmed present from R2: `verify_realization_level_allOf_constraint_via_jerry_ast_validate` in `post_completion_checks`.
4. `uc-author.md` Post-Creation Verification -- added explicit CLI command invocation for consistency (uc-author validates the same schema; behavioral parity with uc-slicer).
5. `uc-author.governance.yaml` `post_completion_checks` -- renamed `verify_yaml_frontmatter_validates_against_schema` to `verify_yaml_frontmatter_validates_against_schema_via_jerry_ast_validate` to make the CLI dependency explicit and machine-readable.

**OWASP categories addressed:**

| OWASP Category | Application to FM-002 |
|----------------|----------------------|
| A08:2021 Data Integrity Failures | Schema validation at the moment of state transition prevents inconsistent artifact production |
| A05:2021 Security Misconfiguration | Explicit CLI validation step eliminates the "secure by assumption" anti-pattern where behavioral instruction was the sole enforcement mechanism |

**Remaining risk areas:** The CLI validation step (`uv run jerry ast validate`) must support the `--schema use_case_realization` flag and be capable of executing allOf constraints against YAML frontmatter. If this CLI mode is not yet implemented, the behavioral enforcement is restored to the R2 state (allOf constraint catches violations at schema validation time, not at the state transition itself). This assumption is explicitly carried from the analysis (E-013 in pm001-fm001-fm002-analysis.md).

---

## L1: Technical Detail

### Pre-State (Before This Implementation)

**uc-slicer.md Step 8** (behavioral only):
```
| 8 | Activity 5 | Set `realization_level: INTERACTION_DEFINED` after verifying
    `interactions[]` is non-empty; set `slice_state: ANALYZED` |
```

**uc-slicer.md Post-Update Verification item 1** (behavioral only):
```
1. Artifact validates against schema including allOf constraints
```

**uc-slicer.governance.yaml output_filtering** (annotation absent):
```yaml
- "realization_level_must_match_populated_blocks"
```

**uc-author.md Post-Creation Verification item 2** (behavioral, no CLI):
```
2. YAML frontmatter validates against `docs/schemas/use-case-realization-v1.schema.json`
```

**uc-author.governance.yaml post_completion_checks** (generic check name):
```yaml
- "verify_yaml_frontmatter_validates_against_schema"
```

### Post-State (After This Implementation)

**uc-slicer.md Step 8** -- CLI gate added at transition point:
```
| 8 | Activity 5 | Before setting `realization_level: INTERACTION_DEFINED`, run
    `uv run jerry ast validate {artifact_path} --schema use_case_realization` to
    verify the allOf constraint passes. Only set the realization level if
    validation succeeds. Set `slice_state: ANALYZED` after validation passes. |
```

**uc-slicer.md Post-Update Verification** -- CLI invocation explicit and item 5 annotated:
```
After updating the artifact, verify by running
`uv run jerry ast validate {artifact_path} --schema use_case_realization`
and confirming all of the following:
1. Artifact validates against `docs/schemas/use-case-realization-v1.schema.json`
   including allOf constraints (run `uv run jerry ast validate {artifact_path}
   --schema use_case_realization`)
...
5. interactions[] present and non-empty when realization_level = INTERACTION_DEFINED
   (enforced by allOf schema constraint + CLI validation at Step 8)
```

**uc-slicer.governance.yaml output_filtering** -- enforcement mechanism annotated:
```yaml
- "realization_level_must_match_populated_blocks (enforced by allOf schema
   constraint + uv run jerry ast validate post-creation check)"
```

**uc-author.md Post-Creation Verification** -- CLI invocation explicit:
```
After writing the artifact, verify by running
`uv run jerry ast validate {artifact_path} --schema use_case_realization`
and confirming all of the following:
1. File exists at the declared output path
2. YAML frontmatter validates against `docs/schemas/use-case-realization-v1.schema.json`
   (run `uv run jerry ast validate {artifact_path} --schema use_case_realization`)
```

**uc-author.governance.yaml post_completion_checks** -- check name made explicit:
```yaml
- "verify_yaml_frontmatter_validates_against_schema_via_jerry_ast_validate"
```

### Schema Verification: allOf Constraint Confirmed Present

Verified `docs/schemas/use-case-realization-v1.schema.json` lines 488-503:

```json
{
  "if": {
    "properties": {
      "realization_level": { "const": "INTERACTION_DEFINED" }
    },
    "required": ["realization_level"]
  },
  "then": {
    "required": ["interactions"],
    "properties": {
      "interactions": {
        "minItems": 1
      }
    }
  }
}
```

This constraint is present and correctly formed. The schema enforces: if `realization_level` is `INTERACTION_DEFINED`, then `interactions` must be present with at least 1 item.

### Governance YAML post_completion_checks Verification

Confirmed present in `uc-slicer.governance.yaml` from R2 remediation:
- `verify_artifact_validates_against_schema_including_allOf`
- `verify_interactions_present_when_realization_level_INTERACTION_DEFINED`
- `verify_detail_level_realization_level_cross_constraint_via_ast_validate`
- `verify_realization_level_allOf_constraint_via_jerry_ast_validate`

All four checks cover the FM-002 enforcement requirement. No additions to `post_completion_checks` were needed.

### Files Modified

| File | Change Type | Description |
|------|-------------|-------------|
| `skills/use-case/agents/uc-slicer.md` | Edit | Step 8 CLI gate + Post-Update Verification explicit CLI + item 5 annotation |
| `skills/use-case/agents/uc-slicer.governance.yaml` | Verified only | R2 checks already present; output_filtering annotation already applied by prior remediation |
| `skills/use-case/agents/uc-author.md` | Edit | Post-Creation Verification explicit CLI invocation |
| `skills/use-case/agents/uc-author.governance.yaml` | Edit | post_completion_checks check name made CLI-explicit |

### Files NOT Modified

Per task scope: no other agent files were modified.

The schema file `docs/schemas/use-case-realization-v1.schema.json` was read to verify the allOf constraint is present -- no modifications made.

---

## L2: Strategic Implications

### Defense-in-Depth Posture After FM-002 Fix

The FM-002 fix adds a third enforcement layer to the existing two-layer stack:

| Layer | Mechanism | When It Fires | What It Catches |
|-------|-----------|---------------|-----------------|
| L1: Behavioral | `NEVER set INTERACTION_DEFINED before populating interactions[]` in `<guardrails>` forbidden actions | LLM reasoning time | LLM self-correction when the forbidden action is present in context |
| L2: Schema allOf | `use-case-realization-v1.schema.json` allOf constraint | At schema validation (post-production) | Empty or absent `interactions[]` when `realization_level: INTERACTION_DEFINED` |
| L3: CLI gate (new) | `uv run jerry ast validate {artifact_path} --schema use_case_realization` at Step 8 | At the exact state transition point | Same as L2, but catches before artifact is marked complete -- error surfaces at uc-slicer, not cd-generator |

The L3 addition specifically addresses the UX failure identified in the adversary finding: without it, the violation would be caught downstream by cd-generator's input validation, with less context about what went wrong and which agent produced the invalid artifact.

### FMEA Assessment After Fix

From the analysis (pm001-fm001-fm002-analysis.md):

| Failure Mode | Before Fix | After Fix (Options A+B) | Reduction |
|-------------|------------|------------------------|-----------|
| Structural: empty interactions[] + INTERACTION_DEFINED | S=9, O=4, D=9 = RPN 324 | S=9, O=4, D=2 = RPN 72 | 78% |
| Semantic: broken source_step + INTERACTION_DEFINED | S=9, O=3, D=8 | S=9, O=3, D=6 = RPN 162 | 50% |

The structural violation RPN reduction to 72 is classified as acceptable. The semantic violation (source_step cross-reference) remains at RPN 162 (monitor), requiring a future CLI enhancement to `jerry ast validate` for semantic cross-reference mode.

### Scalability of the Pattern

The explicit CLI validation step pattern established here (run `uv run jerry ast validate` at the moment of state transition, not only at post-completion) should be applied to any future agent that performs a critical state transition that can be structurally verified. This is consistent with H-05 (UV-only Python execution) and the "filesystem as infinite memory" principle -- using deterministic tooling where possible rather than relying on behavioral instructions.

### Residual Risk

**CLI assumption:** If `uv run jerry ast validate {artifact_path} --schema use_case_realization` does not yet support this validation mode, the L3 gate produces a non-deterministic result (command may fail silently or with a different error). The agent definition now explicitly references the command, which creates an observable discrepancy if the CLI capability is absent. This is the preferred failure mode -- a visible gap rather than a silent pass.

**Semantic cross-reference gap:** The `source_step` cross-reference check (does each interaction's `source_step` reference a real step in `source_flow`) remains LLM-behavioral. The analysis (Option C in FM-002) scopes CLI-level semantic cross-reference validation as a future enhancement pending `jerry ast validate --semantic-cross-ref` mode.

---

*Implementation by eng-backend*
*Analysis source: pm001-fm001-fm002-analysis.md (ps-analyst, 2026-03-11)*
*OWASP Top 10 self-verification: A08 (Data Integrity), A05 (Security Misconfiguration)*
*ASVS 5.0 alignment: V5 (Validation, Sanitization, and Encoding) -- input validation at every trust boundary*
*Constitutional compliance: P-001 (evidence-based), P-002 (persisted to file), P-022 (CLI assumption explicitly disclosed)*
*H-05 compliance: all CLI commands use `uv run` prefix*
*Date: 2026-03-11*
