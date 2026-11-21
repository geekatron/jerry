# QG-E3 Adversarial Review: sop-brief Agent + PRE_JOB_BRIEF Template

## Execution Context

| Field | Value |
|-------|-------|
| **Quality Gate** | QG-E3 (C3, threshold >= 0.93) |
| **Reviewer** | adv-executor |
| **Executed** | 2026-03-26T00:00:00Z |
| **Strategies Applied** | S-010, S-001, S-003, S-002, S-004, S-007, S-011 (7 of 7) |

**Artifacts Reviewed:**

| Artifact | Path |
|----------|------|
| Agent definition | `skills/nuclear-sop/agents/sop-brief.md` |
| Governance | `skills/nuclear-sop/agents/sop-brief.governance.yaml` |
| Template | `skills/nuclear-sop/templates/PRE_JOB_BRIEF.template.md` |

---

## Verdict

| | |
|-|-|
| **Score** | **0.919** |
| **Threshold** | 0.930 |
| **Band** | REVISE (0.919 < 0.930) |
| **Status** | FAIL -- below C3 quality gate |

The deliverable is structurally sound and methodologically thorough. It does not fail on any of the five key validation criteria. The score falls short of threshold due to one Major finding (OE search path bypass vector) and three Minor findings. Targeted remediation of the Major finding and two Minor findings should bring the score above 0.930.

---

## Key Validation Results

| Check | Result | Evidence |
|-------|--------|---------|
| H-34 dual-file architecture (official frontmatter only in .md) | PASS | `.md` frontmatter: name, description, model, tools only. All governance fields in `.governance.yaml`. |
| H-35 constitutional triplet (P-003, P-020, P-022) | PASS | `constitution.principles_applied` lines 60-62; `forbidden_actions` has 4 entries (>= 3 minimum). |
| No Task tool in frontmatter | PASS | `tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]` -- Task absent. Governance `allowed_tools` matches. |
| OE enforcement thresholds (WARNING >10, STOP >20) | PASS | `oe_thresholds.warning: 10`, `oe_thresholds.stop: 20` in governance.yaml; methodology Step 4 prose; identity description -- triple-redundant. |
| Nuclear patterns F-2a, D-1, H-2, A-3 encoded | PASS | Identity (line 12), purpose (lines 36-39), methodology (Steps 1-6 map to patterns), `domain_extensions.nuclear_patterns_implemented` (governance lines 88-93). |
| Template has MANDATORY OE Findings section | PASS | Template navigation table lists "MANDATORY -- all prior OE entries for this workflow type"; section header uses "MANDATORY CONTEXT" language (line 104). |

---

## Findings Summary

| ID | Severity | Finding | Location |
|----|----------|---------|----------|
| RT-001 | Major | OE search path override bypasses accumulation STOP gate | governance.yaml `oe_search_path` input_validation rule |
| DA-001 | Minor | Stray `</output>` tag after `</agent>` close | sop-brief.md line 360 |
| PM-001 | Minor | Handlebars-style conditionals in template have no population specification in methodology | PRE_JOB_BRIEF.template.md; sop-brief.md Step 6 |
| CV-001 | Minor | A-3 "sections 1-6" description understates validation scope (validates section 9) | sop-brief.md identity line 12; methodology Step 1 line 181 |
| CC-001 | Minor | Mixed-case typo in `output_filtering` entry | governance.yaml line 48 |

---

## Detailed Findings

### RT-001: OE Search Path Override Bypasses Accumulation STOP Gate

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Location** | `sop-brief.governance.yaml` -- `guardrails.input_validation.oe_search_path` rule; sop-brief.md Step 4 |
| **Strategy Step** | S-001 Red Team -- attack surface analysis |

**Evidence:**

governance.yaml lines 43-45:
```yaml
- field: oe_search_path
  rule: "Defaults to docs/experience/. If overridden: validate path exists before searching.
         If path does not exist: warn user and proceed with empty OE results (not a STOP)."
```

Step 4 methodology lines 247-248 (thresholds that can be bypassed):
```
- If count > 10: generate WARNING...
- If count > 20: STOP...
```

**Analysis:**

A caller that provides `oe_search_path: /nonexistent/path` receives a warning that the path does not exist and sop-brief proceeds with zero OE entries. With zero entries, the WARNING (>10) and STOP (>20) thresholds are never evaluated. The nuclear H-2 operating experience review is effectively bypassed -- the brief will contain "No prior OE entries found" even if 50 relevant OE entries exist under the default path.

This is a meaningful integrity risk: the OE accumulation STOP gate is one of the most safety-critical mechanisms in sop-brief (it exists to prevent execution against an unprocessed failure pattern per the STOP condition text). The bypass is not intentional user override -- it is an accidental or adversarial path that circumvents the gate entirely without triggering the OE STOP path or requiring the explicit OVERRIDE that the STOP condition demands.

The severity is Major rather than Critical because: (1) the caller must actively provide a non-default path (not a zero-effort bypass), and (2) the agent does warn the user that the path does not exist before proceeding with empty results.

**Recommendation:**

Change the governance.yaml rule and corresponding methodology Step 4 behavior: when `oe_search_path` does not exist, this should be a STOP condition (not a warn-and-continue), presenting the user with three options: (A) provide a valid OE search path, (B) explicitly confirm that no OE history exists for this workflow_type (OVERRIDE with documented justification), (C) HALT. This aligns the path-not-found case with the >20 accumulation STOP behavior and eliminates the silent bypass.

---

### DA-001: Stray `</output>` Tag After `</agent>` Close

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Location** | sop-brief.md, line 360 |
| **Strategy Step** | S-002 Devil's Advocate -- structural critique |

**Evidence:**

```
358 → </guardrails>
359 →
360 → </agent>
361 →
362 → </output>         <-- stray closing tag
```

The `<output>` section was properly closed at line 327. The `</output>` at line 360 (after `</agent>`) is an orphaned closing tag with no matching open tag at that level.

**Analysis:**

Claude Code's XML section parser reads agent definition sections between paired XML tags. An orphaned `</output>` after `</agent>` is formally invalid XML and may cause unexpected behavior depending on the parser's error handling: it could be silently ignored, or it could cause the parser to misidentify the agent boundary. In either case, it signals that the file was not structurally validated before delivery.

**Recommendation:**

Remove the stray `</output>` tag at line 360. Run a structural review of the file to confirm no other orphaned tags exist.

---

### PM-001: Template Conditionals Lack Population Specification

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Location** | PRE_JOB_BRIEF.template.md (multiple `{{#if}}` blocks); sop-brief.md Step 6 |
| **Strategy Step** | S-004 Pre-Mortem -- failure mode identification |

**Evidence:**

Template contains 9 Handlebars-style conditional blocks, e.g.:
```
{{#if PREREQ_WAIVED}}
> **WAIVED Prerequisites:** The following prerequisites were waived...
{{/if}}

{{#if OE_STOP}}
> **STOP CONDITION TRIGGERED:** OE accumulation threshold exceeded...
{{/if}}
```

Step 6 methodology (lines 282-303) instructs sop-brief to "populate all sections using findings" and "Write populated brief to `brief/pre-job-brief.md`" but does not specify how to handle conditional blocks: evaluate them (delete block if false, render content if true), remove all `{{#if}}` markers and keep all content, or leave markers verbatim.

**Analysis:**

If sop-brief leaves the `{{#if}}` markers verbatim in the written brief, the output will contain raw template syntax that is confusing and unprofessional. If sop-brief evaluates them correctly without specification, the behavior is implicit. This creates a risk of inconsistent brief output across different executions.

**Recommendation:**

Add explicit conditional handling instructions to Step 6:
- "When a conditional block's condition evaluates to true: include the block content, remove the `{{#if}}` and `{{/if}}` markers."
- "When a conditional block's condition evaluates to false: remove the entire block including content and markers."
This removes ambiguity and ensures consistent brief output.

---

### CV-001: A-3 Scope Description Understates Validation Coverage

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Location** | sop-brief.md identity section line 12; Step 1 line 181 |
| **Strategy Step** | S-011 Chain-of-Verification -- cross-reference check |

**Evidence:**

Identity line 12: "You implement nuclear pattern ... A-3 (Standard Procedure Structure, **sections 1-6**)."

Step 1, item 6: "Validate that **sections 5** (prerequisites) **and 9** (acceptance criteria) are present and non-empty."

Section 9 is beyond the claimed "sections 1-6" scope of A-3.

**Analysis:**

This is a description inconsistency, not an execution defect -- validating section 9 is correct behavior. However, the identity description may lead readers to believe the validation is limited to sections 1-6, when in fact sop-brief validates through at least section 9. The inconsistency could also cause confusion when cross-referencing sop-brief behavior against A-3 documentation.

**Recommendation:**

Update the identity description to accurately reflect the validation scope: change "A-3 (Standard Procedure Structure, sections 1-6)" to "A-3 (Standard Procedure Structure, sections 1-9)" or "A-3 (Standard Procedure Structure, key sections including prerequisites and acceptance criteria)."

---

### CC-001: Mixed-Case Typo in `output_filtering` Entry

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Location** | sop-brief.governance.yaml line 48 |
| **Strategy Step** | S-007 Constitutional AI Critique -- precision check |

**Evidence:**

```yaml
output_filtering:
  - "no_secrets_in_output"
  - "no_executable_commands_in_brief_output"
  - "all_oE_entries_presented_with_verification_outcome_and_provenance_status"
```

The third entry uses `oE_entries` (lowercase 'o', uppercase 'E') rather than the consistent snake_case pattern used by the other two entries (`no_secrets_in_output`, `no_executable_commands_in_brief_output`).

**Analysis:**

While `output_filtering` values are strings not code identifiers, the governance.yaml is a machine-readable governance record validated by JSON Schema. Inconsistent casing reduces the precision and professionalism of the record and may cause issues if automated tooling performs string matching against these values.

**Recommendation:**

Change `"all_oE_entries_presented_with_verification_outcome_and_provenance_status"` to `"all_oe_entries_presented_with_verification_outcome_and_provenance_status"` (all lowercase snake_case).

---

## S-014 Dimensional Scoring

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|---------|
| Completeness | 0.20 | 0.93 | 0.186 |
| Internal Consistency | 0.20 | 0.89 | 0.178 |
| Methodological Rigor | 0.20 | 0.90 | 0.180 |
| Evidence Quality | 0.15 | 0.95 | 0.143 |
| Actionability | 0.15 | 0.91 | 0.137 |
| Traceability | 0.10 | 0.96 | 0.096 |
| **Composite** | **1.00** | | **0.919** |

**Dimension notes:**

- **Completeness (0.93):** All H-34/H-35 required elements present. All five key validation checks pass. Minor deductions: stray XML tag, Handlebars conditional ambiguity.
- **Internal Consistency (0.89):** Triple-redundant OE thresholds are a strength. Deductions: OE search path bypass creates a logical inconsistency in the safety model (the STOP gate can be circumvented without the explicit OVERRIDE the STOP condition requires); A-3 sections 1-6 vs. section 9 inconsistency.
- **Methodological Rigor (0.90):** Six-step mandatory sequence with explicit STOP/WARNING/PASS outcomes is rigorous. Deduction: the OE search path bypass is a gap in rigor -- the safety model claims no silent failure path exists, but the path-not-found case in OE search is a de facto silent bypass.
- **Evidence Quality (0.95):** Nuclear patterns cited with specific codes throughout. Thresholds quantified. Provenance mechanism specified. Near-perfect evidence anchoring.
- **Actionability (0.91):** Step-by-step instructions with tool usage patterns are highly actionable. Deduction: Handlebars ambiguity in Step 6 requires implicit knowledge to execute correctly.
- **Traceability (0.96):** Nuclear patterns traced from identity through purpose through methodology through domain_extensions. Constitutional principles appear in both forbidden_actions and constitution.principles_applied. Excellent traceability chain.

---

## Remediation Priority

| Priority | Finding | Action | Expected Score Impact |
|----------|---------|--------|-----------------------|
| P1 | RT-001 | Change OE path-not-found from warn-and-continue to STOP with explicit options | +0.008 (Internal Consistency, Methodological Rigor) |
| P2 | PM-001 | Add conditional handling instructions to Step 6 | +0.003 (Actionability) |
| P3 | DA-001 | Remove stray `</output>` tag at line 360 | +0.001 (Completeness) |
| P4 | CV-001 | Update A-3 description to reflect sections 1-9 | +0.001 (Internal Consistency) |
| P4 | CC-001 | Fix `oE_entries` typo to `oe_entries` | +0.001 (Completeness) |

**Projected post-remediation score: ~0.933** (above 0.930 threshold)

---

## Execution Statistics

| Metric | Value |
|--------|-------|
| **Total Findings** | 5 |
| **Critical** | 0 |
| **Major** | 1 |
| **Minor** | 4 |
| **Strategies Executed** | 7 of 7 |
| **Key Validations Passed** | 6 of 6 |
| **Protocol Steps Completed** | 7 of 7 |
