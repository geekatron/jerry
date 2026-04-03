# IN-001 Implementation Summary: Interaction Description Quality Validation

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | What was implemented, security controls applied, OWASP categories |
| [L1: Technical Detail](#l1-technical-detail) | File-by-file changes with rationale |
| [L2: Strategic Implications](#l2-strategic-implications) | Posture assessment and evolution path |
| [OWASP Verification](#owasp-verification) | Self-verification checklist |
| [Remaining Risk Areas](#remaining-risk-areas) | Honest risk register post-implementation |

---

## L0: Executive Summary

**Finding addressed:** IN-001 (Critical, S-013 Inversion strategy) -- cd-generator accepted semantically empty interaction descriptions and produced structurally valid but meaningless OpenAPI contracts. The sole safety gate was the `x-prototype: true` label.

**Implementation:** Three-layer hybrid validation per ADR-IN001 Option C (score 8/10).

**Three files changed:**

| File | Change Type | Summary |
|------|-------------|---------|
| `docs/schemas/use-case-realization-v1.schema.json` | Schema strengthening | `minLength` raised from 1 to 20 on both `request_description` and `response_description` in the `$defs/interaction` definition; description text updated to explain the minimum and warn about placeholder rejection |
| `skills/contract-design/agents/cd-generator.md` | Agent methodology + guardrails | Added Layer 2a (banned-term check, REJECT) and Layer 2b (semantic quality heuristic, WARN) to Step 1; updated guardrails table from two-layer to three-layer; added description quality warning section to L0 output |
| `skills/contract-design/agents/cd-generator.governance.yaml` | Governance YAML | Added banned-term input_validation entry; added `low_quality_descriptions_must_be_annotated_with_x_description_quality_low` output_filtering entry (closes FM-001 pattern) |

**Key security controls applied:**

- **Input validation at trust boundary:** Schema-level floor (deterministic, context-rot immune) catches trivially short placeholders before any agent processing occurs
- **Defense in depth:** Three independent layers with different enforcement mechanisms and failure modes
- **Fail-closed default:** Layer 2a REJECTS on matched placeholder terms; only Layer 2b produces WARN to preserve flexibility for marginal descriptions
- **Actionable error messaging:** Every rejection names the specific interaction ID, field name, matched term, and the corrective agent to invoke (`/use-case uc-slicer Activity 5`)

**OWASP categories addressed:** A03:2021 Injection (placeholder text as semantic injection vector), A04:2021 Insecure Design (defense-in-depth pattern), A08:2021 Data Integrity Failures (input validation at every trust boundary crossing).

**Remaining risk areas:** Banned-term list requires periodic maintenance as new placeholder patterns emerge; Layer 2b LLM evaluation is non-deterministic (mitigated by WARN-not-REJECT design); 20-character threshold may reject terse but valid descriptions (one additional word of specificity resolves this).

---

## L1: Technical Detail

### Change 1: Schema -- `docs/schemas/use-case-realization-v1.schema.json`

**Location:** `$defs.interaction.properties.request_description` and `$defs.interaction.properties.response_description`

**Before:**
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

**After:**
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

**Enforcement layer:** L3 (schema validation, deterministic, context-rot immune). Enforced at the `$defs/interaction` definition level so the constraint applies to all agents consuming this schema: uc-author, uc-slicer, cd-generator, and tspec-generator.

**Backward compatibility:** All interaction descriptions in the UC-LIB-001 worked example exceed 40 characters. The 20-character floor does not break any existing valid artifact.

**Calibration rationale:** Descriptions under 20 characters cannot typically contain both an action verb and a resource noun -- the minimum elements needed for RULE-HM-01 through RULE-HM-04 HTTP method inference and RULE-RI-01 noun extraction. The borderline case ("retrieves the loan" at 19 chars) is intentionally at the boundary; one word of specificity resolves it to "retrieves the loan status" (26 chars).

---

### Change 2: Agent Methodology -- `skills/contract-design/agents/cd-generator.md`

**2a. Step 1 expansion -- Layer 2a (Banned-Term Check):**

Added immediately after the existing "Layer 2 (Semantic)" reference in Step 1. The banned-term algorithm operates in two tiers:

- **EXACT_MATCH_TERMS:** `TBD, TODO, N/A, n/a, ..., xxx, yyy, zzz, none` -- matched case-insensitively against the entire stripped description. No length constraint needed; these are always placeholders regardless of context.
- **SUBSTRING_TERMS:** `FIXME, placeholder, to be determined, to be defined, to be completed, not yet defined, fill in later, needs description, pending, insert description, description here, lorem ipsum, example text, sample description` -- matched as word-boundary substrings, but only when total description length is under 60 characters. This prevents false positives on longer descriptions that contain a banned substring incidentally (e.g., "returns pending approval status for the member's loan" passes because length > 60).

**Rejection message template** is fully specified, naming the interaction ID, field, matched term, and corrective action.

**2b. Step 1 expansion -- Layer 2b (Semantic Quality Heuristic):**

Added immediately after Layer 2a in Step 1. Three LLM-evaluated checks:

1. Verb presence -- strong verbs list aligned to RULE-HM-01 through RULE-HM-04 vocabulary
2. Noun presence -- at least one domain-specific resource noun
3. Vagueness check -- descriptions that use only generic terms without domain content

Failure produces `x-description-quality: low` annotation on the generated operation. Does NOT block generation.

**2c. L0 Summary expansion:**

Added a "Description quality warnings" bullet to the L0 output specification. When interactions carry `x-description-quality: low`, the L0 lists them with field name and criterion failure, and appends the recommendation to revise via `/use-case` before removing the PROTOTYPE label.

**2d. Guardrails table updated:**

The "Input Validation (Two-Layer Gate)" heading was updated to "Input Validation (Three-Layer Gate)". Two new table sections were added:
- Layer 2a table: banned-term REJECT row
- Layer 2b table: three WARN rows (verb absence, noun absence, vagueness)

---

### Change 3: Governance YAML -- `skills/contract-design/agents/cd-generator.governance.yaml`

**input_validation entry added (FM-001 closure):**

```yaml
- "Each $.interactions[*].request_description and response_description must not
   contain banned placeholder terms (TBD, TODO, FIXME, placeholder, N/A, lorem
   ipsum, etc.) -- REJECT with guidance directing to /use-case (uc-slicer
   Activity 5) for description revision; see cd-generator.md Step 1 Layer 2a
   for full banned-term list and matching algorithm"
```

This closes the FM-001 pattern: the validation rule now exists in both the `.md` guardrails section AND the `.governance.yaml` input_validation list, ensuring CI gates that inspect the governance YAML independently will capture this constraint.

**output_filtering entry added:**

```yaml
- "low_quality_descriptions_must_be_annotated_with_x_description_quality_low"
```

This declares the annotation obligation as a machine-readable output constraint. Consistent with the existing output_filtering format in the file (snake_case policy strings).

---

## L2: Strategic Implications

### Backend Security Posture Assessment

**Before IN-001 implementation:** The `/contract-design` skill had a single-layer input validation model: schema structural check (L3-enforced) plus agent guardrail field-presence checks. No semantic quality gate existed. A single malformed input -- an artifact where all seven required fields were present but contained placeholder text -- would pass all gates and produce a meaningless contract.

**After IN-001 implementation:** Three-layer validation with different enforcement characteristics:

| Layer | Enforcement Type | Context-Rot Immune | False Rejection Risk |
|-------|-----------------|-------------------|---------------------|
| Schema minLength | Deterministic, L3 | Yes | Low |
| Banned-term check | Deterministic, agent behavioral | Partially (L2-REINJECT protected via guardrails) | Near-zero (two-tier matching) |
| Semantic quality heuristic | LLM-evaluated, WARN | No (L1 only) | Low (WARN, not REJECT) |

The WARN-not-REJECT design for Layer 2b is a deliberate security trade-off: LLM-evaluated semantic quality is non-deterministic, and a hard REJECT on non-deterministic criteria would create unpredictable agent behavior (same description passes in one session, fails in another). WARN preserves the ability to generate a PROTOTYPE contract while making the quality gap visible.

### Dependency Risk Landscape

- **Schema consumer chain:** `use-case-realization-v1.schema.json` is consumed by uc-author, uc-slicer, cd-generator, and tspec-generator. The `minLength: 20` change on the `interaction` definition propagates to all consumers. For uc-author and uc-slicer, this means descriptions they produce must exceed 20 characters -- a quality-raising constraint, not a breaking change.
- **Banned-term list maintenance:** The 21-term list in Layer 2a requires periodic review. New placeholder conventions (e.g., "TBC", "WIP", "CHANGEME") will bypass it until added. Layer 2b provides a behavioral fallback as WARN, but the deterministic REJECT guarantee erodes over time without maintenance. Recommended: add banned-term review to the cd-generator update checklist.

### Scalability Considerations for Security Controls

The three-layer pattern established by this ADR is designed to scale to other natural-language fields across the Jerry framework:

- **Extension condition text** (uc-author validation): could apply the same pattern -- schema minLength + banned terms + LLM quality heuristic
- **Flow step action text** (uc-author validation): similar pattern applicable
- **tspec-generator scenario descriptions**: Layer 1 schema constraint already applies via schema inheritance; Layers 2a/2b would require tspec-generator-specific guardrail additions

### Evolution Path for Auth/Validation Architecture

Per ADR-IN001 L2 evolution roadmap:

| Phase | Change |
|-------|--------|
| v1.1 (recommended next) | uc-slicer Activity 5 adds WARN-level description quality check at interaction creation time, providing shift-left feedback before the artifact reaches cd-generator |
| v2.0 (future) | Replace boolean `x-description-quality: low/high` with numeric scoring (0.0-1.0); cd-validator incorporates description quality into overall contract quality score |
| v3.0 (future) | Automated description improvement suggestions via LLM when verb vocabulary and noun extraction heuristics are validated against a real UC artifact corpus |

---

## OWASP Verification

Self-verification against OWASP Top 10 for the implemented changes:

| OWASP Category | Assessment |
|----------------|-----------|
| A01:2021 Broken Access Control | Not applicable to this change (no access control logic modified) |
| A02:2021 Cryptographic Failures | Not applicable (no cryptographic operations) |
| A03:2021 Injection | **ADDRESSED.** Placeholder text in descriptions is a semantic injection vector: it passes structural validation but produces garbage output. Layer 2a explicitly rejects known placeholder patterns. Layer 1 schema minLength provides a deterministic floor. |
| A04:2021 Insecure Design | **ADDRESSED.** Three-layer defense in depth is the canonical secure design pattern for natural-language field validation. The WARN-not-REJECT design for Layer 2b follows the principle of least disruptive security control. |
| A05:2021 Security Misconfiguration | Not applicable (no configuration changes) |
| A06:2021 Vulnerable Components | Not applicable (no dependency changes) |
| A07:2021 Auth Failures | Not applicable |
| A08:2021 Data Integrity Failures | **ADDRESSED.** Input validation at the schema boundary (L3-enforced minLength) and at the agent boundary (banned-term check) ensures that transformation only proceeds on inputs with minimum semantic integrity. |
| A09:2021 Logging Failures | **ADDRESSED.** Layer 2b quality findings are logged in the L0 summary, creating a visible record of low-quality descriptions that persists in the output artifact. Rejection messages from Layers 1 and 2a name the specific field, term, and corrective action. |
| A10:2021 SSRF | Not applicable (cd-generator is T2, no external network access) |

---

## Remaining Risk Areas

| Risk | Probability | Impact | Residual Mitigation |
|------|-------------|--------|---------------------|
| Banned-term list becomes stale; novel placeholder patterns ("TBC", "WIP") bypass Layer 2a | Medium | Low | Layer 2b catches most novel placeholders as WARN; PROTOTYPE label is binding safety net |
| False rejection at Layer 1 for terse but valid descriptions under 20 characters | Low | Medium | User adds one word of specificity; threshold calibrated to allow minimal viable descriptions |
| Layer 2b LLM inconsistency: same description WARN/PASS varies across sessions | Medium | Low | WARN-not-REJECT design absorbs inconsistency; no blocking behavior |
| Non-English descriptions trigger excessive Layer 2b WARN due to English-centric verb vocabulary | Low | Low | Opus has multilingual verb recognition; WARN allows the user to proceed regardless |
| FM-001 pattern recurrence: future maintainers add Layer 2a/2b rules to .md but forget .governance.yaml | Medium | Low | The governance YAML entry references `cd-generator.md Step 1 Layer 2a` explicitly, creating a visible cross-reference that future maintainers will encounter |

---

*Implementation by: eng-backend*
*ADR reference: ADR-IN001 (PROPOSED, PROJ-021 verification pipeline)*
*Date: 2026-03-11*
*Files modified: 3 (schema, agent .md, agent .governance.yaml)*
*Constitutional compliance: P-001 (accuracy), P-002 (file persistence), P-022 (risks honestly documented)*
