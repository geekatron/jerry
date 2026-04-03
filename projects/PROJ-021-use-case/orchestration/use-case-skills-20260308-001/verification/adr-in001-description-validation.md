# ADR-IN001: Interaction Description Quality Validation for cd-generator

## Document Sections

| Section | Purpose |
|---------|---------|
| [Status](#status) | Decision lifecycle status |
| [L0: Executive Summary](#l0-executive-summary) | Plain-language decision summary |
| [Context](#context) | Problem and motivation |
| [Forces](#forces) | Tensions in play |
| [Options Considered](#options-considered) | Alternatives evaluated (P-011) |
| [Decision](#decision) | Chosen approach and rationale |
| [L1: Technical Implementation](#l1-technical-implementation) | Implementation specification |
| [L2: Architectural Implications](#l2-architectural-implications) | Long-term strategic consequences |
| [Consequences](#consequences) | Positive, negative, neutral outcomes (P-022) |
| [Risks](#risks) | Risk register with mitigation |
| [Related Decisions](#related-decisions) | Links to related ADRs and findings |
| [Adversarial Self-Review](#adversarial-self-review) | S-002, S-003, S-004, S-013 application |

---

## Status

**PROPOSED**

---

## L0: Executive Summary

We discovered that cd-generator -- the agent that transforms use case interaction descriptions into OpenAPI API contracts -- accepts placeholder or semantically empty descriptions (like "TBD", "perform the action", "return the result") and produces structurally valid but meaningless API specifications from them. The current safeguard (the `x-prototype: true` label) warns consumers that the contract is unreviewed, but it does not prevent the generation of garbage output in the first place.

We are proposing a three-layer validation approach. First, the JSON Schema adds a minimum character length (20 characters) to `request_description` and `response_description` fields, which catches trivially short placeholders like "TBD" at the structural level. Second, cd-generator's agent methodology gains a new semantic validation step that checks descriptions against a banned-term list (e.g., "placeholder", "TBD", "TODO") and a quality heuristic requiring at least one verb pattern recognizable by the HTTP method inference algorithm. Third, rejection messages are designed to tell the user exactly what to fix and direct them back to `/use-case` (uc-slicer) to improve the source descriptions.

This matters because semantically empty descriptions produce API contracts with meaningless operation names, wrong HTTP methods (all defaulting to POST with low-confidence warnings), and empty request/response schemas. These contracts waste reviewer time, erode trust in the `/contract-design` skill, and -- if the PROTOTYPE label is ever inadvertently removed -- could become the basis for incorrect API implementations.

---

## Context

### Problem Statement

Adversary finding IN-001 (S-013 Inversion strategy, severity Critical) identified that cd-generator's input validation gate has a semantic gap. The two-layer validation currently enforces:

- **Layer 1 (Structural):** JSON Schema validates that `request_description` and `response_description` exist and have `minLength: 1` (non-empty string).
- **Layer 2 (Agent Guardrails):** cd-generator checks that all 7 required interaction fields are present and that `source_step` references resolve to existing flow steps.

Neither layer validates that description text is *semantically meaningful*. The schema constraint `minLength: 1` permits descriptions like "x", "TBD", "placeholder", "perform the user action", or "return the result". All pass structural validation. When these descriptions reach cd-generator's transformation algorithm:

1. **HTTP method inference** (RULE-HM-01 through RULE-HM-05) finds no verb pattern match and defaults to POST with `x-method-inference: low` (RULE-HM-05).
2. **Resource identification** (RULE-RI-01) cannot extract a meaningful noun from "return the result" and produces a generic or incorrect path segment.
3. **Schema derivation** (RULE-SD-01, RULE-SD-02) produces empty `properties: {}` blocks because no named entities exist in the descriptions.

The generated contract is structurally valid OpenAPI YAML, carries `x-prototype: true`, and has extensive `x-method-inference: low` annotations -- but is semantically incorrect. The PROTOTYPE label is the sole safety net.

### Motivating Evidence

| Evidence Source | Finding |
|-----------------|---------|
| `adversary-skill-findings.md` IN-001 (S-013) | "cd-generator will accept it and produce a structurally valid but semantically incorrect OpenAPI contract labeled x-prototype: true. The PROTOTYPE label is the only safety gate." Severity: Critical. |
| `adversary-skill-findings.md` IN-001 Priority | P0 (must fix): "Add description quality requirements to cd-generator Input Requirements; strengthen PROTOTYPE label guidance" |
| `uc-to-contract-rules.md` RULE-HM-05 | POST default with low confidence when request_description matches no verb pattern |
| `use-case-realization-v1.schema.json` interaction definition | `request_description` and `response_description` have only `minLength: 1` -- no semantic constraints |

### Scope

This ADR addresses the interaction `request_description` and `response_description` fields only. It does not address:

- Precondition/postcondition quality (these produce warnings but not rejections when absent)
- Flow step `action` text quality (a separate concern for uc-author validation)
- Extension condition text quality (addressed by error response inference rules, not by this ADR)

---

## Forces

| Force | Direction | Weight |
|-------|-----------|--------|
| **Garbage-in-garbage-out prevention:** Semantically empty descriptions produce meaningless contracts that waste reviewer time and erode skill trust | Toward stricter validation | High |
| **False rejection risk:** Overly strict validation may reject legitimate domain-specific descriptions that use unfamiliar vocabulary, abbreviations, or non-English terms | Toward permissive validation | High |
| **Layered defense philosophy:** The existing two-layer validation (structural + semantic) should be extended, not replaced; enforcement should match the capability of each layer | Toward multi-layer solution | Medium |
| **Schema backward compatibility:** The JSON Schema is consumed by multiple agents (uc-author, uc-slicer, cd-generator); changes must not break existing valid artifacts | Toward minimal schema change | Medium |
| **Actionability of error messages:** Rejected artifacts must tell the user *exactly* what to fix and *which agent* to re-invoke, per PM-001 analysis findings | Toward prescriptive error messages | Medium |
| **Domain vocabulary diversity:** Different domains (finance, healthcare, logistics) use different vocabularies; validation must not be domain-biased | Toward vocabulary-neutral heuristics | Medium |
| **LLM judgment vs. deterministic rules:** Semantic quality assessment is inherently subjective; hard rules risk false positives while LLM evaluation risks inconsistency | Toward hybrid approach | Medium |

---

## Options Considered

### Option A: Schema-Only Enforcement (Minimum Length + Pattern)

Increase `minLength` on `request_description` and `response_description` to 20 characters and add a `pattern` constraint rejecting known placeholder text.

| Aspect | Assessment |
|--------|------------|
| **Pros** | Deterministic (L3 enforcement, context-rot immune). Zero token cost. Catches trivially short placeholders ("TBD", "N/A", "test"). Enforced consistently across all agents consuming the schema. |
| **Cons** | Cannot distinguish semantically meaningful 20-character text from padding ("perform the action!!"). Pattern matching is brittle -- banned terms require ongoing maintenance. Cannot assess whether a description contains an action verb. JSON Schema `pattern` on long text is unwieldy and cannot express "must contain at least one verb from a set." |
| **False rejection risk** | Low for `minLength: 20`. Examples: "Query member loans" (18 chars) would be rejected despite being meaningful. This can be mitigated by choosing a calibrated threshold. |
| **Steelman (S-003):** | The strongest argument for schema-only enforcement is *consistency and reliability*. Schema validation is deterministic, runs before the LLM processes anything, costs zero tokens, and cannot be degraded by context rot. A well-chosen minLength eliminates the bottom 10% of garbage descriptions with zero ambiguity. This layer should exist regardless of what other layers are added. |
| **Score** | 5/10 -- necessary but insufficient alone |

### Option B: Agent Guardrail Enforcement Only (LLM-Evaluated Semantic Checks)

Add semantic quality checks to cd-generator's Layer 2 agent guardrails. The LLM evaluates description quality using heuristic rules (banned terms, verb presence, noun extractability) and rejects descriptions that fail.

| Aspect | Assessment |
|--------|------------|
| **Pros** | Can assess semantic quality with nuance (understands domain jargon, abbreviations, multilingual text). Can detect "passes minLength but is semantically empty" cases. Can provide rich, context-specific error messages. Already fits the existing two-layer validation architecture. |
| **Cons** | LLM evaluation is non-deterministic -- the same description may pass in one session and fail in another. Vulnerable to context rot (L1 enforcement layer, not L2-protected). Adds token cost for each validation. Cannot guarantee consistency across model versions. No enforcement if the governance YAML is consumed independently (FM-001 pattern). |
| **False rejection risk** | Medium. LLM may over-reject domain jargon it has not seen, or under-reject plausible-sounding but meaningless text. |
| **Steelman (S-003):** | The strongest argument for LLM-only enforcement is *semantic flexibility*. Only the LLM can understand that "Patron presents library card for checkout processing" is meaningful while "System does the thing for the stuff" is not, despite both having similar length and containing verbs. For domain-specific vocabularies and multilingual descriptions, LLM judgment is more accurate than any rule set. |
| **Score** | 6/10 -- powerful but unreliable as sole enforcement |

### Option C: Hybrid Three-Layer Validation (Recommended)

Combine schema-level structural floor (Layer 1), agent-level semantic heuristics (Layer 2), and quality scoring with actionable feedback (Layer 2 enhanced).

**Layer 1 (Schema):** Increase `minLength` to 20 characters. This catches trivially short placeholders deterministically.

**Layer 2a (Deterministic Heuristics in Agent Guardrails):** Banned-term list check. If `request_description` or `response_description` contains banned placeholder terms (case-insensitive match), REJECT with specific guidance. This is applied as a string-match operation by the agent before LLM semantic evaluation.

**Layer 2b (LLM Semantic Quality Check in Agent Guardrails):** The agent evaluates whether the description contains at least one recognizable action verb (for request) or state-change description (for response). Descriptions that pass 2a but fail 2b receive a WARN with `x-description-quality: low` annotation rather than a hard REJECT, preserving the ability to generate a PROTOTYPE contract while flagging the quality gap.

| Aspect | Assessment |
|--------|------------|
| **Pros** | Three defense layers: deterministic floor (schema), deterministic reject (banned terms), nuanced warn (LLM quality). False rejection minimized: only trivially short or obviously placeholder text is hard-rejected; marginal descriptions generate warnings instead. Actionable error messages at each layer. Schema changes are backward-compatible (existing valid descriptions exceed 20 chars). |
| **Cons** | More complex to implement (three layers vs. one). Banned-term list requires maintenance. WARN-not-REJECT for Layer 2b means some low-quality descriptions still produce PROTOTYPE contracts (intentional trade-off). |
| **False rejection risk** | Low. Hard rejection occurs only for: (a) descriptions under 20 characters, (b) descriptions containing known placeholder terms. All other quality concerns produce warnings, not rejections. |
| **Steelman (S-003):** | The strongest argument against the hybrid approach is *complexity*: three validation layers create three potential failure points and three sets of error messages to maintain. A single well-tuned LLM evaluation (Option B) could theoretically achieve the same coverage with less architectural overhead. However, this argument does not account for the deterministic reliability advantage of the schema layer and the FM-001 finding that governance YAML constraints must be independently enforceable. |
| **Score** | 8/10 -- balanced trade-off of strictness, flexibility, and reliability |

### Option D: Upstream Prevention (uc-slicer Quality Gate)

Instead of validating at cd-generator input, enforce description quality at uc-slicer Activity 5 output. uc-slicer would not set `realization_level: INTERACTION_DEFINED` until interaction descriptions meet quality criteria.

| Aspect | Assessment |
|--------|------------|
| **Pros** | Catches the problem at the source. Prevents low-quality descriptions from ever reaching cd-generator. Aligns with the principle that data quality should be enforced at creation, not consumption. |
| **Cons** | uc-slicer already has the FM-002 realization_level enforcement gap -- adding more enforcement to an agent with known behavioral enforcement limitations compounds the problem. Does not protect cd-generator against manually constructed or externally imported artifacts that bypass uc-slicer. Creates a coupling: if uc-slicer's quality criteria change, cd-generator has no independent protection. Violates the defensive validation principle (each consumer validates its own inputs). |
| **False rejection risk** | Medium at uc-slicer (blocks the entire realization step, not just the contract generation). |
| **Steelman (S-003):** | The strongest argument for upstream prevention is *shift-left*. Catching description quality problems at uc-slicer means the user is corrected immediately when writing descriptions, not 30 minutes later when they invoke cd-generator. The feedback loop is tighter and the rework cost is lower. This argument is genuine and suggests that even if Option C is chosen, uc-slicer SHOULD also add description quality guidance (as a WARN, not a gate). |
| **Score** | 5/10 -- good principle but insufficient as sole defense |

### Options Comparison Summary

| Criterion | A: Schema-Only | B: Agent-Only | C: Hybrid (Rec.) | D: Upstream |
|-----------|---------------|---------------|-------------------|-------------|
| Catches "TBD" / short placeholders | Yes | Yes | Yes | Yes |
| Catches "perform the action" (verbose placeholder) | No | Yes | Yes (WARN) | Depends |
| Deterministic enforcement | Full | None | Partial (L1+2a) | None |
| Context-rot immune | Yes | No | Partially | No |
| False rejection risk | Low-Med | Medium | Low | Medium |
| Backward compatible | Yes (calibrated) | Yes | Yes | Yes |
| Independent of LLM | Yes | No | Partially | No |
| Actionable error messages | Limited | Rich | Rich | Rich |
| **Overall Score** | 5/10 | 6/10 | **8/10** | 5/10 |

---

## Decision

**Adopt Option C: Hybrid Three-Layer Validation.**

Implement description quality validation across three layers:

1. **Schema (deterministic, L3-immune):** Increase `minLength` from 1 to 20 on `request_description` and `response_description` in `use-case-realization-v1.schema.json`.
2. **Agent guardrails -- banned terms (deterministic):** Add a banned-term check to cd-generator's Layer 2 validation that hard-REJECTs descriptions containing known placeholder terms.
3. **Agent guardrails -- semantic quality (LLM-evaluated):** Add a quality heuristic check that WARNs (but does not reject) when descriptions lack recognizable action verbs or state-change language, annotating the generated contract with `x-description-quality: low`.

Additionally, recommend (but do not require) that uc-slicer Activity 5 add a WARN-level quality check on description content at generation time, providing earlier feedback in the pipeline.

### Rationale

The three-layer approach provides defense in depth calibrated to the reliability of each enforcement mechanism:

- **Layer 1 (Schema)** is deterministic and context-rot immune, so it handles the highest-confidence rejection (trivially short text). It works even when the governance YAML is consumed independently of the agent (FM-001 pattern).
- **Layer 2a (Banned Terms)** is deterministic at the agent level and handles the second tier of obvious placeholders that exceed the character limit but are clearly not real descriptions.
- **Layer 2b (Semantic Quality)** uses LLM judgment for nuanced assessment but produces warnings rather than rejections, reflecting the uncertainty inherent in LLM evaluation.

The WARN-not-REJECT design for Layer 2b is a deliberate trade-off: it allows users to generate a PROTOTYPE contract from marginal descriptions (perhaps as a quick exploration) while making the quality gap visible through annotations. The PROTOTYPE label already serves as the final safety net.

---

## L1: Technical Implementation

### Layer 1: Schema Changes

**File:** `docs/schemas/use-case-realization-v1.schema.json`

**Change:** Update the `interaction` definition's `request_description` and `response_description` properties.

Current:
```json
"request_description": {
  "type": "string",
  "minLength": 1,
  "description": "What the actor requests from the system."
},
"response_description": {
  "type": "string",
  "minLength": 1,
  "description": "What the system responds to the actor."
}
```

Proposed:
```json
"request_description": {
  "type": "string",
  "minLength": 20,
  "description": "What the actor requests from the system. Must be a semantically meaningful description of the request action (minimum 20 characters). Descriptions should contain action verbs recognizable by HTTP method inference (e.g., 'submits', 'retrieves', 'updates', 'removes'). Placeholder text (e.g., 'TBD', 'placeholder') will be rejected by cd-generator."
},
"response_description": {
  "type": "string",
  "minLength": 20,
  "description": "What the system responds to the actor. Must be a semantically meaningful description of the system response (minimum 20 characters). Descriptions should describe observable state changes or returned data. Placeholder text (e.g., 'TBD', 'placeholder') will be rejected by cd-generator."
}
```

**Calibration of 20-character threshold:**

| Example Description | Length | Status |
|---------------------|--------|--------|
| "TBD" | 3 | Rejected (below 20) |
| "placeholder text" | 16 | Rejected (below 20) |
| "do the thing here" | 18 | Rejected (below 20) |
| "retrieves the loan" | 19 | Rejected (below 20) |
| "retrieves the loan status" | 26 | Accepted |
| "submits a loan request for the selected book" | 46 | Accepted |
| "creates a loan record and returns a due-date slip" | 51 | Accepted |

The 20-character threshold was chosen by analyzing the shortest meaningful description that could support HTTP method inference. Descriptions under 20 characters cannot typically contain both an action verb and a resource noun -- the minimum elements needed for RULE-HM-01 through RULE-HM-04 verb pattern matching and RULE-RI-01 noun extraction. The borderline case ("retrieves the loan" at 19 chars) is intentionally at the boundary -- it barely qualifies semantically and would pass with one additional word of specificity.

**Backward compatibility:** All interaction descriptions in the worked example UC-LIB-001 exceed 40 characters. Any existing valid artifact should exceed 20 characters comfortably. If an existing artifact has descriptions under 20 characters, it was likely a placeholder that should have been caught.

### Layer 2a: Banned-Term List (cd-generator Agent Guardrails)

**File:** `skills/contract-design/agents/cd-generator.md` -- add to `<guardrails>` Layer 2 checks.

**Banned terms (case-insensitive match):**

```
BANNED_TERMS = [
  "TBD",
  "TODO",
  "FIXME",
  "placeholder",
  "to be determined",
  "to be defined",
  "to be completed",
  "not yet defined",
  "fill in later",
  "needs description",
  "pending",
  "insert description",
  "description here",
  "lorem ipsum",
  "example text",
  "sample description",
  "N/A",
  "none",
  "...",
  "xxx",
  "yyy",
  "zzz"
]
```

**Matching rule:** If any banned term appears as a substring of `request_description` or `response_description` (case-insensitive), REJECT with actionable error message.

**Guardrails table entry:**

```
| Any `$.interactions[*].request_description` or `$.interactions[*].response_description` contains banned placeholder terms | REJECT: "UC {id} interaction {INT-nn} contains placeholder text '{matched_term}' in {field_name}. Replace with a semantically meaningful description containing an action verb (for requests) or state-change description (for responses). Use /use-case (uc-slicer) to update the interaction descriptions." |
```

**Edge case handling for banned terms:**

| Edge Case | Handling |
|-----------|----------|
| "pending approval status is returned" (contains "pending") | False positive. Mitigation: match "pending" only when it appears as the entire description or as the first word. Alternatively, use whole-word matching with word boundaries. |
| "System returns N/A for optional fields" | False positive for "N/A". Mitigation: match "N/A" only when it is the complete description, not when embedded in a larger description. |
| Domain term collision (e.g., medical "TBD" meaning "to be disclosed") | Unlikely but possible. Mitigation: banned-term matching requires the term to be a substantial portion of the description (>50% of total length) OR the complete description. This prevents rejection of long descriptions that happen to contain a banned substring. |

**Refined matching algorithm:**

```
For each interaction description:
  1. If description.strip().upper() in EXACT_MATCH_TERMS (TBD, TODO, N/A, ..., xxx, yyy, zzz, none):
     REJECT (entire description is a placeholder)
  2. If any term in SUBSTRING_TERMS appears as a word-boundary match in description:
     AND the description total length < 60 characters:
     REJECT (short description dominated by placeholder language)
  3. Otherwise: PASS to Layer 2b
```

This two-tier matching prevents false positives on longer descriptions that incidentally contain a banned substring while still catching "TBD - needs work later" (31 chars, contains "TBD" and is short).

### Layer 2b: Semantic Quality Heuristic (cd-generator Agent Methodology)

**File:** `skills/contract-design/agents/cd-generator.md` -- add to methodology Step 1 (Input Validation Gate), after Layer 2 structural checks.

**Quality heuristic (LLM-evaluated, WARN not REJECT):**

For each interaction with `actor_role = consumer`:

1. **Verb presence check (request_description):** Does the description contain at least one recognizable action verb from the HTTP method inference vocabulary?
   - Strong verbs: read, query, get, fetch, retrieve, search, list, find, create, add, submit, register, initiate, start, send, post, update, modify, change, edit, set, replace, delete, remove, cancel, revoke, deactivate, terminate
   - If no strong verb found: flag as `x-description-quality: low` on the generated operation

2. **Noun presence check (request_description and response_description):** Does the description contain at least one identifiable domain noun (the resource or entity being acted upon)?
   - If no noun extractable: flag as `x-description-quality: low`

3. **Repetition/vagueness check:** Is the description semantically identical to the generic pattern "actor does action / system returns result" without domain-specific content?
   - Pattern match: descriptions that use only generic terms (action, result, request, response, process, handle, perform, execute, do, thing, stuff, data, information) without domain-specific nouns
   - If matched: flag as `x-description-quality: low`

**WARN behavior (not REJECT):**

When Layer 2b flags a description as low quality:

1. The interaction is still processed by the transformation algorithm
2. The generated operation carries `x-description-quality: low` annotation
3. The L0 summary includes a quality warning section listing all low-quality interactions
4. The L0 summary recommends: "Interactions with x-description-quality: low should be revised in the source UC artifact via /use-case before removing the PROTOTYPE label."

**Rationale for WARN not REJECT at Layer 2b:** LLM semantic judgment is non-deterministic and context-dependent. A hard REJECT on LLM-evaluated quality criteria would create unpredictable agent behavior -- the same description might pass in one session and fail in another. WARN provides visibility into quality concerns without blocking the generation workflow. The PROTOTYPE label already prevents premature consumption of low-quality contracts.

### Layer 2a: Governance YAML Update

**File:** `skills/contract-design/agents/cd-generator.governance.yaml` -- add to `guardrails.input_validation`.

```yaml
- "Each $.interactions[*].request_description and response_description must not contain banned placeholder terms (TBD, TODO, placeholder, N/A, etc.) -- REJECT with guidance directing to /use-case for description revision"
```

**File:** `skills/contract-design/agents/cd-generator.governance.yaml` -- add to `guardrails.output_filtering`.

```yaml
- "low_quality_descriptions_must_be_annotated_with_x_description_quality_low"
```

### Error Message Specification

**Layer 1 rejection (schema validation failure):**

```
UC {id} interaction {INT-nn} has a {field_name} that is too short
({actual_length} characters, minimum 20 required). Interaction descriptions
must be semantically meaningful sentences describing the request action or
system response. Use /use-case (uc-slicer Activity 5) to revise the
interaction descriptions.
```

**Layer 2a rejection (banned term detected):**

```
UC {id} interaction {INT-nn} contains placeholder text '{matched_term}' in
{field_name}. This cannot be transformed into a meaningful API operation.
Replace with a description that includes:
  - For request_description: an action verb (e.g., 'submits', 'retrieves',
    'updates', 'removes') and the resource being acted upon
  - For response_description: the system's observable response (e.g.,
    'creates a loan record', 'returns the member profile',
    'confirms deletion')
Use /use-case (uc-slicer Activity 5) to update the interaction descriptions.
```

**Layer 2b warning (semantic quality flag):**

```
WARNING: UC {id} interaction {INT-nn} has {field_name} with low semantic
quality -- no recognizable action verb or domain noun detected. The
interaction will be processed but the generated operation will carry
x-description-quality: low. HTTP method inference defaulted to POST
(RULE-HM-05). Review and revise in the source UC artifact before removing
the PROTOTYPE label.
```

### Edge Cases

| Edge Case | Layer | Handling |
|-----------|-------|----------|
| **Multilingual descriptions** (e.g., German: "Benutzer reicht Kreditantrag ein") | Layer 1: passes (>20 chars). Layer 2a: passes (no banned terms). Layer 2b: LLM evaluates verb presence in the source language. German action verbs are recognized by Opus. | No special handling needed; LLM multilingual capability covers this. |
| **Domain jargon and abbreviations** (e.g., "POSTs FHIR Bundle to /Patient endpoint") | Layer 1: passes. Layer 2a: passes ("POST" is not in banned list; "FHIR" is domain jargon). Layer 2b: "POST" is recognized as an action verb. | No false rejection. Domain jargon in the noun position is acceptable -- the LLM can extract it. |
| **Highly abbreviated descriptions** (e.g., "Req: auth token via OAuth2 PKCE") | Layer 1: 33 chars, passes. Layer 2a: passes. Layer 2b: "Req" is not a standard action verb; may flag as low quality. | Acceptable false positive at WARN level. User can proceed; contract carries quality annotation. Recommends expanding description for better inference. |
| **Multiple sentences** (e.g., "Member presents card. System scans barcode. Loan request is submitted.") | Layer 1: passes. Layer 2a: passes. Layer 2b: "presents", "scans", "submitted" are all recognizable verbs. | Passes all layers. Multiple sentences are acceptable; HTTP method inference uses the primary action verb. |
| **Descriptions with HTML/Markdown** (e.g., "Submits **loan request** for `book_id`") | Layer 1: passes. Layer 2a: passes. Layer 2b: verb "submits" recognized despite markup. | No special handling needed. Markup does not affect semantic evaluation. |
| **Unicode descriptions** (e.g., CJK characters) | Layer 1: character count, not byte count; JSON Schema string length is code points. Layer 2a: banned terms are Latin-only; no false positives on CJK. Layer 2b: LLM evaluates semantic content in source language. | Handled correctly by all layers. |

---

## L2: Architectural Implications

### Systemic Consequences

1. **Validation architecture precedent:** This ADR establishes the pattern of "schema floor + deterministic agent check + LLM semantic check" as the canonical three-layer validation approach for natural-language fields in Jerry artifacts. Future agents consuming text fields (e.g., tspec-generator consuming `$.extensions[*].condition` text) should follow this pattern.

2. **Schema-agent contract tightening:** Increasing `minLength` from 1 to 20 strengthens the schema-agent contract. All agents consuming the schema (uc-author, uc-slicer, cd-generator, tspec-generator) inherit this constraint automatically. uc-author will need to produce descriptions exceeding 20 characters when populating interactions -- this is not a breaking change but is a quality-raising constraint on upstream agents.

3. **Annotation namespace expansion:** The `x-description-quality` annotation extends the existing annotation namespace (`x-prototype`, `x-method-inference`, `x-source-interaction`, etc.) in generated OpenAPI contracts. cd-validator should be updated to report `x-description-quality: low` counts in its quality assessment.

4. **Shift-left opportunity for uc-slicer:** The recommendation that uc-slicer add WARN-level description quality checks during Activity 5 creates an architectural pattern where quality feedback is provided at creation time as well as consumption time. This is consistent with the PM-001 analysis finding that error propagation should flow both forward (to consumers) and backward (to producers).

### Evolution Path

| Phase | Change | Trigger |
|-------|--------|---------|
| **v1.0 (this ADR)** | Schema minLength + banned terms + LLM quality WARN | IN-001 remediation |
| **v1.1 (future)** | uc-slicer Activity 5 adds WARN-level description quality check at interaction creation time | After v1.0 is validated in practice |
| **v2.0 (future)** | Description quality scoring with numeric threshold (0.0-1.0) replacing boolean low/high; cd-validator incorporates description quality into overall contract quality score | After sufficient data on description quality distribution is collected from PROTOTYPE contract reviews |
| **v3.0 (future)** | Automated description improvement suggestions via LLM (e.g., "Your description 'gets the thing' could be improved to 'retrieves the member's current loan status'") | When the verb vocabulary and noun extraction heuristics are validated against a corpus of real UC artifacts |

### Integration with Existing Findings

| Finding | Relationship to This ADR |
|---------|--------------------------|
| FM-001 (governance YAML completeness) | The banned-term check is added to both the .md guardrails AND the .governance.yaml input_validation, closing the FM-001 pattern of "rule in .md but not in YAML." |
| FM-002 (realization_level enforcement) | This ADR follows the same layered-validation pattern recommended for FM-002: schema constraint (deterministic) + agent behavioral constraint (LLM-enforced). |
| PM-001 (error propagation) | Error messages in this ADR follow the PM-001 recommendation pattern: structured, actionable, directing the user to the correct upstream agent (/use-case uc-slicer). |
| DA-001 (cognitive mode) | cd-generator's cognitive mode is now "systematic" (per DA-001 remediation). The description validation is a systematic, step-by-step check -- consistent with the corrected cognitive mode. |

---

## Consequences

### Positive

1. **Eliminates trivially malformed descriptions** at the schema level with zero token cost and full determinism.
2. **Catches placeholder text** ("TBD", "TODO") before transformation begins, saving the token cost of generating a meaningless contract.
3. **Preserves flexibility** for marginal descriptions through WARN-not-REJECT at Layer 2b, preventing frustration from false rejections.
4. **Creates visible quality signal** via `x-description-quality: low` annotation, giving PROTOTYPE reviewers immediate visibility into which operations need attention.
5. **Provides actionable error messages** directing users to the specific field and agent needed for correction.
6. **Closes the FM-001 pattern** by adding validation rules to both .md and .governance.yaml.

### Negative (P-022 Compliance: Negative Consequences Honestly Documented)

1. **Banned-term list requires maintenance.** As new placeholder patterns emerge (e.g., "insert here", "change me"), the list must be updated. Without periodic review, new placeholder patterns will bypass Layer 2a. Mitigation: review banned-term list whenever cd-generator is updated; Layer 2b (LLM) catches most novel placeholders as WARNs.
2. **False positives on legitimate short descriptions.** The 20-character schema threshold will reject some legitimate but terse descriptions (e.g., "retrieves the loan" at 19 chars). Mitigation: the threshold is calibrated to allow minimal viable descriptions; affected users add one word of specificity.
3. **False positives from banned-term substring matching.** Descriptions containing "pending" as a legitimate domain term (e.g., "returns pending approval status") could be flagged if the matching algorithm is not carefully implemented. Mitigation: the refined matching algorithm uses whole-word + length checks to minimize false positives.
4. **Layer 2b WARN annotations add noise to generated contracts.** Operations with `x-description-quality: low` annotations increase the annotation density of the OpenAPI YAML. Mitigation: annotations are in the `x-` extension namespace and are invisible to OpenAPI consumers that do not inspect extensions.
5. **No enforcement on non-cd-generator consumers.** Other agents consuming interaction descriptions (e.g., tspec-generator reading `request_description` for scenario context) do not benefit from Layer 2a/2b checks. Mitigation: the schema minLength (Layer 1) protects all consumers; agent-specific checks can be added to other consumers as needed.

### Neutral

1. **Existing valid artifacts are unaffected.** All descriptions in the UC-LIB-001 worked example exceed 40 characters. The 20-character minimum does not break existing content.
2. **cd-validator does not need immediate changes.** The `x-description-quality: low` annotation is in the same `x-` namespace already consumed by cd-validator for `x-method-inference` and `x-prototype`. cd-validator SHOULD report low-quality description counts but this is a separate enhancement.

---

## Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Banned-term list becomes stale; new placeholder patterns bypass Layer 2a | Medium | Low (Layer 2b catches most) | Review banned-term list at each cd-generator version update; Layer 2b provides fallback |
| False rejection of legitimate terse descriptions at Layer 1 (schema) | Low | Medium (blocks uc-slicer from setting INTERACTION_DEFINED) | 20-char threshold is conservative; user adds one word of specificity |
| LLM inconsistency at Layer 2b produces different WARN/PASS results across sessions | Medium | Low (WARN only, no blocking) | WARN-not-REJECT design absorbs inconsistency; PROTOTYPE label is the binding safety net |
| Multilingual descriptions trigger false WARNs because Layer 2b verb vocabulary is English-centric | Low | Low (WARN, not REJECT) | Opus has multilingual capability; verb recognition works across major languages. WARN allows the user to proceed regardless. |
| Schema minLength change breaks an existing artifact with short but valid descriptions | Very Low | Medium (blocks artifact validation) | Audit all existing artifacts before deploying schema change; provide migration guidance |

---

## Related Decisions

| Reference | Relationship |
|-----------|--------------|
| Adversary finding IN-001 (`adversary-skill-findings.md`) | **Motivating finding.** This ADR directly addresses the Critical IN-001 finding from the S-013 Inversion strategy. |
| Adversary finding FM-001 (`adversary-agent-findings.md`) | **Pattern alignment.** FM-001 identified that governance YAML input_validation was incomplete. This ADR adds validation rules to both .md and .governance.yaml. |
| Adversary finding PM-001 (`adversary-agent-findings.md`) | **Error message design.** Error messages follow PM-001's structured rejection pattern directing users to the correct upstream agent. |
| PM-001/FM-001/FM-002 analysis (`pm001-fm001-fm002-analysis.md`) | **Design consistency.** This ADR follows the layered-validation and structured-rejection patterns recommended in the cross-cutting analysis. |
| DA-001 remediation (cognitive mode) | **Consistency.** The validation steps are systematic and procedural, consistent with cd-generator's corrected "systematic" cognitive mode. |

---

## Adversarial Self-Review

### S-010 Self-Refine (H-15 Mandatory)

Before presenting this ADR, verified:

- [x] **Completeness:** All 5 design deliverables requested are addressed (criteria, enforcement location, error messaging, edge cases, strictness trade-off)
- [x] **Alternatives evaluated:** 4 options analyzed per P-011 (minimum 3 required)
- [x] **Negative consequences documented:** 5 negative consequences per P-022
- [x] **Status is PROPOSED:** Per P-020, not ACCEPTED
- [x] **Evidence-based:** All claims reference specific findings, schema definitions, or rule specifications
- [x] **Error messages are actionable:** Each error message names the field, the problem, and the corrective action including the agent to invoke

### S-003 Steelman (H-16 Mandatory)

Each rejected alternative received a steelman analysis documenting its genuine merits before explaining why the hybrid approach is preferred. Key steelman findings:

- **Option A (schema-only):** Deterministic reliability is genuinely superior. This is why the schema layer is included in the hybrid approach, not rejected entirely.
- **Option B (agent-only):** Semantic flexibility is genuinely superior for nuanced quality assessment. This is why the LLM layer is included as Layer 2b.
- **Option D (upstream prevention):** Shift-left feedback is genuinely valuable. This is why the ADR recommends uc-slicer WARN-level checks as a future enhancement.

### S-002 Devil's Advocate

**Challenge: "What if the 20-character minimum is wrong?"**

If too low (e.g., 15): permits "does the action!!" (17 chars) -- a padded placeholder. If too high (e.g., 30): rejects "retrieves the loan status" (26 chars) -- a legitimate description. The 20-character threshold sits in the gap between trivially short placeholders (under 18 chars in common examples) and the shortest meaningful descriptions (20-25 chars in the HTTP inference vocabulary). Sensitivity analysis shows the window is narrow -- a 5-character change in either direction has meaningful impact. The threshold SHOULD be recalibrated after collecting data from the first 10-20 real artifacts processed by cd-generator.

**Challenge: "What if banned-term matching causes more problems than it solves?"**

The refined matching algorithm (exact match for short terms, word-boundary + length check for substring terms) reduces false positives to near zero for descriptions over 60 characters. For descriptions under 60 characters, false positives are intentionally more likely because short descriptions with placeholder substrings are genuinely suspicious. The cost of a false rejection at Layer 2a is low: the user adds a word of specificity and retries.

### S-004 Pre-Mortem

**"It is 6 months later and this decision failed. Why?"**

Most likely failure mode: the banned-term list becomes stale while placeholder patterns evolve. Users discover that "TBC" (to be confirmed) or "WIP" bypass the list. Layer 2b catches some of these as WARNs, but the deterministic rejection guarantee erodes. Mitigation: add a banned-term review step to the cd-generator version update checklist.

Second failure mode: teams in non-English-speaking environments find that the Layer 2b verb check produces excessive false WARNs because their descriptions use domain-specific abbreviations unfamiliar to the LLM. Mitigation: the WARN-not-REJECT design means this is annoying but not blocking; teams can ignore the annotation and proceed to PROTOTYPE review.

### S-013 Inversion

**"What if we deliberately chose the opposite -- no validation at all?"**

The PROTOTYPE label already warns that contracts are unreviewed. If we rely entirely on the PROTOTYPE label with no description validation, the worst case is: all interactions have "TBD" descriptions, cd-generator produces a contract with 100% POST operations and empty schemas, a reviewer opens the PROTOTYPE contract, sees that it is meaningless, and sends it back to the user. Cost: one wasted generation cycle (2-5 minutes of LLM time) plus reviewer time to determine the contract is useless. This cost is bearable for occasional occurrences but becomes a significant workflow tax if placeholder descriptions are common. The validation layers prevent the wasted generation cycle at near-zero cost.

---

*ADR Version: 1.0.0*
*PS ID: PROJ-021 / Orchestration use-case-skills-20260308-001*
*Finding: IN-001 (Critical, S-013 Inversion)*
*Author: ps-architect*
*Date: 2026-03-11*
*Constitutional Compliance: P-001 (accuracy), P-002 (file persistence), P-011 (alternatives evaluated), P-020 (PROPOSED status), P-022 (negative consequences documented)*
