# Red Team Security Assessment: PROJ-021 Adversary Remediation Implementations

**Assessor:** red-vuln (Vulnerability Analyst, /red-team skill)
**Assessment date:** 2026-03-11
**Scope:** Defensive review of agent definition files within the Jerry Framework. No external targets.
**Authorization:** Defensive security review of PROJ-021 remediation artifacts.
**Files assessed:**
- `skills/use-case/agents/uc-author.md`
- `skills/use-case/agents/uc-author.governance.yaml`
- `skills/use-case/agents/uc-slicer.md`
- `skills/use-case/agents/uc-slicer.governance.yaml`
- `skills/contract-design/agents/cd-generator.md`
- `skills/contract-design/agents/cd-generator.governance.yaml`
- `docs/schemas/use-case-realization-v1.schema.json`
- Implementation summaries: pm001, fm001, fm002, in001

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overall Risk Rating](#overall-risk-rating) | Summary risk posture |
| [PM-001 Findings](#pm-001-findings-rejection-artifact-pattern) | Rejection artifact security (T1-T5) |
| [IN-001 Findings](#in-001-findings-description-validation-security) | Banned-term and semantic validation security |
| [FM-001 Findings](#fm-001-findings-governance-yaml-loading-prerequisites) | TOCTOU and cross-reference validation risks |
| [FM-002 Findings](#fm-002-findings-schema-allof-enforcement) | allOf constraint bypass and then-false pattern |
| [Cross-Cutting Findings](#cross-cutting-findings) | Issues spanning multiple implementations |
| [Finding Summary Table](#finding-summary-table) | All findings indexed by ID and severity |
| [Recommendations Summary](#recommendations-summary) | Prioritized remediation actions |

---

## Overall Risk Rating

**LOW**

The four implementations demonstrate sound security thinking within their design scope. The threat model is correctly calibrated to the same-trust-boundary case: these are LLM agent definitions operating within a single user session on a controlled filesystem. No Critical or High severity findings were identified. The Medium findings represent meaningful gaps that could degrade the reliability of security controls under realistic adversarial conditions. The Low and Info findings are design observations that are acceptable to carry as known residual risk.

The most significant residual risk is the absence of a formal rejection artifact schema file (Phase 2 deferred item from PM-001), which leaves schema drift across future agent pairs as a structural governance gap rather than a runtime vulnerability.

---

## PM-001 Findings: Rejection Artifact Pattern

### VULN-PM-001 (Medium): Missing Schema Version Upper Bound Allows Future Schema Injection

**Threat vector:** T5 (unknown schema version / future schema versions break consumers)

**Description:** The uc-author rejection artifact check validates `schema_version` is `"1.0.0"` and warns on unknown versions (step 2b). However, the validation logic is exact-match only against the current version string. A future schema version (`"2.0.0"` or `"1.1.0"`) would trigger the "unknown version -- warn and proceed without rejection context" path. This means a crafted rejection artifact at a higher schema version number causes uc-author to silently ignore the rejection context and proceed without the guidance it needs.

The more subtle risk: the "proceed without rejection context" fallback has no ceiling. If a rejection artifact is written by a future uc-slicer version that produces a v2.0.0 schema with a changed field layout, uc-author proceeds as if no rejection existed. This is not a prompt injection vector, but it is a silent degradation of the backward error channel -- the primary purpose of the PM-001 pattern.

**Evidence:**
- `uc-author.md` step 2b: "if unknown version, log a warning and proceed without rejection context"
- `uc-author.governance.yaml` session_context.on_receive: "validate schema_version is 1.0.0... On YAML parse failure (T4): warn and proceed"
- No upper-bound or version-range check is defined anywhere in the agent definitions

**Recommendation:** Add a version negotiation step: if `schema_version > "1.0.0"`, warn the user with the specific version found and ask whether to proceed. Do not silently consume unknown versions -- escalate to the user per H-31. This is a one-line addition to the protocol in step 2b.

---

### VULN-PM-002 (Low): Rejection Artifact Timestamp TOCTOU Window

**Threat vector:** T3 (stale rejection artifact)

**Description:** The staleness check in uc-author step 2d compares the artifact file's modification time against the rejection artifact's `timestamp` field. The timestamp in the rejection artifact is an ISO-8601 string that uc-slicer writes at the moment of rejection. The actual file system modification time is compared to this string.

This creates a narrow TOCTOU window: if the user modifies the UC artifact file after uc-slicer rejects it (correcting an unrelated field, for example), the modification time will be more recent than the rejection timestamp, and uc-author will trigger the staleness warning even though the rejection is still valid. This is a false positive, not a false negative -- the result is a user prompt rather than incorrect elaboration. The risk direction is benign (over-caution rather than under-caution).

However, there is a complementary false-negative path: if uc-slicer writes the rejection artifact and the system clock on the LLM side differs from the filesystem clock (e.g., in a remote execution context), the timestamp comparison could incorrectly conclude the rejection is not stale when it is.

**Evidence:**
- `uc-author.md` step 2d: "If the artifact file's modification time is more recent than the rejection artifact's `timestamp`..."
- The comparison relies on two different time sources: filesystem mtime and the LLM-written ISO-8601 string
- The LLM does not have access to the filesystem mtime directly; it must use Bash to retrieve it

**Recommendation:** Document the assumption that the LLM uses `stat` (or equivalent) to retrieve the artifact modification time via Bash, and that this is compared numerically against the ISO-8601 timestamp. This is already implied by the Bash tool access but is not explicitly stated, leaving the comparison mechanism ambiguous to future maintainers.

---

### VULN-PM-003 (Low): Rejection Artifact Cleanup Race on Elaboration Failure

**Threat vector:** Data integrity -- incomplete cleanup leaves conflicting state

**Description:** The post-elaboration cleanup protocol (uc-author.md "Post-elaboration cleanup") states: "If yes [artifact meets required level]: delete `{artifact_path}-rejection.yaml`." The `rm` command is executed via Bash. If the Bash tool fails (e.g., permission error, command timeout, concurrent access), the rejection artifact remains in place. This is the correct behavior per the implementation -- "leave in place on failure."

The problem is the converse: if elaboration partially succeeds (the agent writes an artifact but at a level below `required_state.detail_level`), the rejection artifact is left in place. On the next uc-author invocation, the rejection artifact is re-read. The T3 staleness check will likely conclude the artifact is stale (since the UC artifact was just modified). This triggers a user prompt -- the intended behavior.

However, the implementation does not handle the case where `$.detail_level` in the newly written artifact is *exactly equal to* `required_state.detail_level` but the content is semantically incomplete (e.g., a schema-valid artifact with empty extensions at ESSENTIAL_OUTLINE). The cleanup decision is based on the `detail_level` enum value, not on semantic content quality. This creates a path where a schema-valid but semantically hollow artifact causes the rejection artifact to be deleted, removing the backward error channel.

**Evidence:**
- `uc-author.md` post-elaboration cleanup step 1: "Verify the produced artifact's `$.detail_level >= required_state.detail_level`"
- Cleanup decision is purely level-comparison based
- No semantic content check precedes deletion

**Recommendation:** The current cleanup criterion (level comparison) is intentional and appropriate for the scope. Document this as a known limitation: the rejection artifact cleanup is level-based, not content-based. Semantic quality is the responsibility of the Cockburn quality indicators in Step 9 of the writing process.

---

### VULN-PM-004 (Info): Rejection Artifact `human_message` Leaks Rejection State

**Threat vector:** T1 variant -- information disclosure via displayed fields

**Description:** The `human_message` field is displayed to the user but not injected into agent reasoning context (step 2h). This is correct security behavior. However, the pm001-implementation-summary notes that `human_message` is "display-only." In practice, displaying a message authored by uc-slicer to the user in the context of uc-author's session constitutes presenting content from one agent in another agent's output without attribution clarity.

This is an information disclosure finding, not a prompt injection finding. The risk is that a user reading uc-author's output sees a message that appears to come from uc-author but was actually authored by uc-slicer. The display instruction says "display to user if present" without requiring attribution.

**Evidence:**
- `uc-author.md` step 2h: "`human_message`: display to user if present, but do NOT inject into agent reasoning context"
- No attribution requirement is stated (e.g., "display as: 'Message from uc-slicer: {human_message}'")

**Recommendation:** Add an attribution wrapper: display as "Message from uc-slicer: {human_message}" rather than raw display. This prevents confusion about which agent produced the message and makes the inter-agent communication chain transparent to the user.

---

### VULN-PM-005 (Info): No Maximum Length Constraint on Rejection Artifact String Fields

**Threat vector:** T1 (prompt injection via oversized fields)

**Description:** The rejection artifact YAML fields `human_message`, `recommended_action`, and `missing_elements[]` have no declared maximum length. While T1 mitigation correctly treats these as DATA not INSTRUCTIONS, an excessively large `missing_elements` array (e.g., 500 entries) would be consumed as a checklist, bloating the agent's working context window and potentially contributing to context rot (R-T01 in agent-routing-standards.md).

This is an amplification concern rather than a direct injection concern. The implementation correctly prevents instruction execution. The risk is context saturation from oversized legitimate-looking data.

**Evidence:**
- Rejection artifact YAML template in `uc-slicer.md` specifies `missing_elements` as an array with no `maxItems` constraint
- `uc-author.md` step 2f: "Extract `missing_elements[]` as the elaboration checklist -- use these as the specific content gaps to address"
- No length or item-count bounds are stated anywhere

**Recommendation:** Add a behavioral note to step 2f: "If `missing_elements[]` contains more than 10 items, truncate to the first 10 and warn the user." Ten is a practical ceiling for actionable checklist items; larger arrays indicate a malformed or adversarially constructed rejection artifact.

---

## IN-001 Findings: Description Validation Security

### VULN-IN-001 (Medium): SUBSTRING_TERMS Length Guard Bypassable via Unicode Padding

**Threat vector:** Banned-term bypass through encoding tricks

**Description:** The SUBSTRING_TERMS check in cd-generator Layer 2a applies only when `total description length < 60 characters`. The intent is to prevent false positives on legitimate descriptions that incidentally contain a banned substring. The bypass vector is: pad a placeholder description with Unicode characters that inflate the byte count above 60 without adding semantic content.

Examples:
- `"pending\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0"` -- "pending" followed by 14 non-breaking spaces exceeds 60 chars in UTF-8 byte length but passes no semantic quality check
- `"TBD " + "\u200B" * 80` -- "TBD" followed by 80 zero-width spaces; would still be caught by EXACT_MATCH_TERMS after `strip()`, but `\u200B` is not a standard whitespace that Python's `.strip()` removes by default

The EXACT_MATCH_TERMS check uses `description.strip()` before comparison, which handles ASCII whitespace. However, Unicode non-breaking spaces (U+00A0), zero-width spaces (U+200B), and other Unicode whitespace characters are not removed by Python's default `str.strip()` -- they require `str.strip()` with explicit argument or regex `\s` with `re.UNICODE`.

**Evidence:**
- `cd-generator.md` Layer 2a: "If description.strip() matches any EXACT_MATCH_TERMS (case-insensitive)"
- The `strip()` operation uses default Python behavior, which does not strip all Unicode whitespace
- `\u00A0` (non-breaking space), `\u2003` (em space), `\u200B` (zero-width space) all survive default `.strip()`
- A description of `"TBD\u00A0"` would survive the EXACT_MATCH_TERMS check and also survive the SUBSTRING_TERMS check if total length with those characters > 60

**Recommendation:** Specify Unicode-aware stripping in the Layer 2a algorithm: "normalize whitespace by collapsing all Unicode whitespace characters (including non-breaking space U+00A0 and zero-width characters U+200B, U+FEFF) before applying EXACT_MATCH_TERMS matching." For Layer 2b (LLM evaluation), the LLM will naturally see through Unicode padding because it processes semantics rather than byte counts, providing a compensating control for the deterministic layer's gap.

---

### VULN-IN-002 (Medium): Layer 2b Semantic Evaluation Anchored to English Verb Vocabulary

**Threat vector:** Layer 2b manipulation via language substitution

**Description:** The Layer 2b verb presence check evaluates whether `request_description` contains "at least one recognizable action verb from the HTTP method inference vocabulary." The vocabulary list is entirely English: `read, query, get, fetch, retrieve, search, list, create, add, submit`, etc.

An adversarially crafted description using a non-English strong verb that maps to the same HTTP method would pass Layer 2b undetected. For example:
- French: "récupère le profil du membre" (retrieves the member profile) -- passes as meaningful, but could also be used to pass a description like "obtient TBD" (gets TBD) -- the banned term survives Layer 2a if in a non-ASCII-strippable encoding
- More practically: a terse English description with a domain verb not in the list (e.g., "ingests the loan application") would be flagged as `x-description-quality: low` even though it is semantically correct

This is a dual-edged gap: the vocabulary-based heuristic produces false negatives (passes weak English descriptions using non-listed verbs) and false positives (warns on non-English or domain-specific strong verbs). Given that Layer 2b is WARN-not-REJECT, the false-negative direction is the security concern.

**Evidence:**
- `cd-generator.md` Layer 2b step 1: "Strong verbs: read, query, get, fetch, retrieve, search, list, find, create, add, submit, register..."
- The list covers common REST verbs but omits domain-specific verbs commonly used in UC artifacts (ingest, dispatch, forward, propagate, emit, consume)
- `in001-implementation-summary.md` "Remaining Risk Areas" acknowledges: "Non-English descriptions trigger excessive Layer 2b WARN due to English-centric verb vocabulary"

**Recommendation:** This risk is mitigated by the WARN-not-REJECT design and the `x-prototype: true` safety label. Document the English-centric limitation explicitly in the Layer 2b specification. For Phase v1.1, consider expanding the strong verb vocabulary to include 10-15 common domain-specific verbs identified from actual UC artifact usage patterns.

---

### VULN-IN-003 (Low): x-description-quality Annotation Trust Confusion

**Threat vector:** Trust boundary confusion -- annotation treated as authoritative rather than advisory

**Description:** The `x-description-quality: low` annotation is applied to generated OpenAPI operations by cd-generator. cd-validator (and human reviewers) reading the generated contract will see this annotation. The annotation's presence (or absence) may be treated as a definitive quality assessment.

The trust confusion arises from two directions:

1. **False confidence from absence:** An operation without `x-description-quality: low` is implicitly "quality: high," but this only means the LLM did not flag it in that session. A different session might flag the same operation. The annotation's absence is non-deterministic.

2. **Annotation spoofing:** A contract that was not generated by cd-generator (e.g., a hand-authored OpenAPI spec) could include or omit `x-description-quality: low` annotations arbitrarily. cd-validator would interpret this as cd-generator's quality assessment when it was not.

**Evidence:**
- `cd-generator.md` Layer 2b: "Add `x-description-quality: low` annotation to the generated OpenAPI operation"
- `cd-generator.governance.yaml` output_filtering: `"low_quality_descriptions_must_be_annotated_with_x_description_quality_low"`
- No documentation that the annotation is advisory and session-specific, not deterministic

**Recommendation:** Add to the L0 output specification: "Note: `x-description-quality: low` annotations reflect a single session's LLM evaluation and may vary across sessions. They are advisory. The authoritative quality check is Layer 2a (deterministic banned-term rejection). Do not treat absence of the annotation as a quality guarantee." Include this caveat in the mapping document's annotation description.

---

### VULN-IN-004 (Info): 20-Character minLength Floor Does Not Prevent Repetitive Padding

**Threat vector:** minLength bypass via character repetition

**Description:** The schema enforces `minLength: 20` on `request_description` and `response_description`. This catches single-word placeholders (TBD, N/A, etc.) but does not prevent character-repetition padding: `"xxxxxxxxxxxxxxxxxxxxxxxxxx"` (26 x's), `"aaaaaaaaaaaaaaaaaaaaa"` (21 a's), or concatenated single-char patterns.

The EXACT_MATCH_TERMS list catches `"xxx"` and `"yyy"` and `"zzz"` (exact matches after strip) but does not catch `"xxxxxxxxxx"` (10 x's) or `"zzzzzzzzz"` (9 z's) -- these would pass EXACT_MATCH_TERMS (no exact match) and pass SUBSTRING_TERMS (no banned substring), and would only be caught by Layer 2b's vagueness check (which flags descriptions using only generic terms).

This is primarily a defense-in-depth gap rather than a practical bypass, since Layer 2b would flag the description as `x-description-quality: low` and the `x-prototype: true` label remains mandatory.

**Evidence:**
- Schema `$defs.interaction.properties.request_description.minLength: 20` -- byte count only
- EXACT_MATCH_TERMS includes `xxx`, `yyy`, `zzz` but not `xxxx...` patterns
- Layer 2b would flag repeated-character descriptions via vagueness check

**Recommendation:** Accept as residual risk. The `x-prototype: true` mandatory label and cd-validator review step provide adequate compensating controls. Document that `minLength: 20` is a floor against trivially short placeholders, not a semantic quality guarantee.

---

## FM-001 Findings: Governance YAML Loading Prerequisites

### VULN-FM-001 (Low): Loading Prerequisites Are Declarative Strings, Not Enforced Contracts

**Threat vector:** TOCTOU -- files modified between prerequisite check and cross-reference validation

**Description:** The FM-001 fix adds loading prerequisite text to governance YAML `input_validation` entries. These are human-readable (and CI-readable) annotations, not runtime enforcement mechanisms. The format "(cross-reference prerequisite: full file must be loaded before field check can execute)" is a declaration of intent, not a technical guard.

The TOCTOU scenario: an LLM agent reads the governance YAML, sees the cross-reference entry for cd-generator entry 5 (source_step validation), loads the UC artifact, begins the validation, and the UC artifact is modified by a concurrent process (another agent or the user) between the load and the field validation. The cross-reference check operates on the loaded snapshot, not the live file. This is acceptable and expected behavior for LLM agents, but the governance YAML annotation does not make this assumption explicit.

More practically, the TOCTOU risk exists at the CI gate layer (L5): a CI tool that reads governance YAML entries and attempts to execute cross-reference validation against a live repository has a genuine TOCTOU window. The entry text says "full file must be loaded before field check can execute" but does not specify that the file must be locked or snapshotted during validation.

**Evidence:**
- `cd-generator.governance.yaml` entry 5: "(loading prerequisite: $.basic_flow, $.alternative_flows, and $.extensions must all be in scope to resolve source_flow references)"
- This is a string annotation; it does not create a runtime file locking mechanism
- `fm001-implementation-summary.md` L2: "The changes are backward-compatible with existing CI validation gates"

**Recommendation:** Add a clarifying annotation to cross-reference entries: "(atomic load required: snapshot the full artifact at load time; re-validation against a modified version requires a new load cycle)." This prevents CI tool authors from building gap-vulnerable validators that load fields incrementally.

---

### VULN-FM-002 (Info): Cross-Reference Prerequisite Format Is Unvalidated Free Text

**Threat vector:** Governance artifact drift -- future maintainers add incomplete prerequisites

**Description:** The "(cross-reference prerequisite: ...)" format established in FM-001 is a free-text annotation convention. It is not validated by `agent-governance-v1.schema.json` (which uses `additionalProperties: true` on the `guardrails.input_validation` array, accepting any string). A future maintainer writing a new cross-reference entry could use a different format, omit the prerequisite entirely, or use a partial form.

The `fm001-implementation-summary.md` L2 explicitly acknowledges this: "The boundary rule applied here is not yet formally documented in `agent-development-standards.md`."

**Evidence:**
- `agent-governance-v1.schema.json` `guardrails.input_validation` accepts any string array with no format constraint
- The comment block added to `cd-generator.governance.yaml` documents the convention, but comments are not machine-enforced
- No CI check validates the presence of prerequisite text on cross-reference entries

**Recommendation:** This is the Phase 2 documentation gap identified in FM-001. Accept as known residual risk pending formalization in `agent-development-standards.md`. The recommendation to adopt the boundary rule as a MEDIUM standard is correct and should be tracked.

---

## FM-002 Findings: Schema allOf Enforcement

### VULN-FM-002-A (Low): allOf then:false Constraint Applies Only When Both Fields Present

**Threat vector:** allOf bypass via field omission

**Description:** The seventh allOf constraint in `use-case-realization-v1.schema.json` (lines 537-547) uses `then: false` to reject INTERACTION_DEFINED + BRIEFLY_DESCRIBED/BULLETED_OUTLINE combinations. The constraint fires when both `realization_level` and `detail_level` are present and set to the prohibited combination.

The bypass vector: omit `detail_level` entirely. The allOf `if` condition requires both `realization_level` and `detail_level` to be present (`"required": ["realization_level", "detail_level"]`). If `detail_level` is absent, the constraint does not fire -- `then: false` is never evaluated.

An artifact with `realization_level: INTERACTION_DEFINED` and no `detail_level` field would:
1. Pass this allOf constraint (field absent, `if` condition not met, `then: false` not evaluated)
2. Fail the top-level `required` validation (schema line 20: `detail_level` is required)

This means the top-level required constraint catches the case before the allOf has a chance to be bypassed. The schema is correct in depth, and the bypass is blocked by the required constraint. The defense is not solely dependent on the allOf.

**Evidence:**
- Schema lines 537-547: `"required": ["realization_level", "detail_level"]` in the `if` condition
- Schema lines 7-23: `detail_level` in top-level `required` array
- Top-level `required` provides the catch for the omission bypass path

**Recommendation:** This is a non-exploitable bypass because of the defense-in-depth structure (top-level `required` + allOf). Document this explicitly in the schema description: "The then: false constraint is backed by the top-level required constraint on detail_level, ensuring the bypass-via-omission path is blocked." This makes the interdependence explicit for future schema maintainers.

---

### VULN-FM-002-B (Low): allOf Constraint 4 (extensions Required) Has No Minimum on Empty Arrays

**Threat vector:** Schema bypass via explicit empty array

**Description:** The sixth allOf constraint (lines 520-536) requires `extensions` to be present with `minItems: 1` when `detail_level` is ESSENTIAL_OUTLINE or FULLY_DESCRIBED. The schema correctly uses `minItems: 1` on the constraint's `then` clause.

However, the `extensions` property definition at lines 134-140 allows zero-length arrays by default (no `minItems` on the top-level property definition, only in the allOf constraint). This means: if `detail_level` is BULLETED_OUTLINE, an artifact with `extensions: []` (explicit empty array) is schema-valid. The allOf constraint does not apply because BULLETED_OUTLINE does not trigger it.

This is not a bypass of the allOf -- it is the intended behavior at lower detail levels. The concern is that an artifact at BULLETED_OUTLINE with `extensions: []` satisfies the schema, and when uc-author later promotes it to ESSENTIAL_OUTLINE, the allOf constraint will correctly reject it. But if uc-author writes ESSENTIAL_OUTLINE directly with `extensions: []`, the allOf fires and rejects it.

The gap: the CLI gate (`uv run jerry ast validate`) must correctly execute the allOf constraint, not just check field presence. This depends on the CLI tool's schema validation implementation.

**Evidence:**
- Schema lines 134-140: `extensions` property has no `minItems` constraint at the property level
- Schema lines 520-536: allOf constraint adds `minItems: 1` only when `detail_level` is ESSENTIAL_OUTLINE or FULLY_DESCRIBED
- `fm002-implementation-summary.md` "Residual Risk": "The CLI validation step must support the --schema use_case_realization flag and be capable of executing allOf constraints against YAML frontmatter"

**Recommendation:** Document the dependency: the CLI `jerry ast validate` tool must execute allOf constraints, not only top-level required/property constraints. If the CLI tool only validates required fields and property types (not allOf), the FM-002 CLI gate provides no additional protection over schema structural validation. This is the existing residual risk identified in the FM-002 summary -- confirm it is being tracked.

---

### VULN-FM-002-C (Info): `slice` Definition Uses additionalProperties: true

**Threat vector:** Unconstrained extension fields in slice objects

**Description:** The `$defs.slice` definition (schema lines 342-396) uses `"additionalProperties": true`, unlike `$defs.flow_step`, `$defs.extension`, `$defs.alternative_flow`, and `$defs.interaction` which all use `"additionalProperties": false`. This allows arbitrary additional fields in slice objects without schema rejection.

This is inconsistent with the other `$defs` definitions and the top-level schema (which uses `"additionalProperties": false`). The inconsistency suggests this was intentional -- the slice definition may be designed for extensibility. However, it also means:
- A slice object with a field named `system_role` or `actor_role` (borrowed from the interaction definition) would pass schema validation
- A crafted artifact could embed interaction-like data in slice objects that passes schema validation but confuses downstream slice consumers

**Evidence:**
- Schema line 395: `"additionalProperties": true` on `$defs.slice`
- All other `$defs` use `"additionalProperties": false`
- No documentation on why slice has an open schema while others are closed

**Recommendation:** Either document why `additionalProperties: true` is intentional for slices (extensibility reason), or change to `false` for consistency with the rest of the schema. If intentional, add a comment: "// additionalProperties: true intentional -- slice objects support worktracker extension fields not enumerated here."

---

## Cross-Cutting Findings

### VULN-CROSS-001 (Medium): No Defense Against Rejection Artifact Written Outside uc-slicer

**Threat vector:** Trust boundary confusion -- rejection artifact authorship not verified

**Description:** The PM-001 pattern assumes that any `{artifact_path}-rejection.yaml` file was written by uc-slicer. The `rejecting_agent` field is validated to have value "uc-slicer" in the written YAML template, but uc-author does not verify that `rejecting_agent == "uc-slicer"` when consuming the artifact. The governance YAML on_receive entry mentions extracting fields but does not specify validating the `rejecting_agent` field value.

The attack scenario within the same-trust-boundary model: a user or a different agent (e.g., a future tspec-analyst that also produces rejection artifacts per PM-003) writes a `{artifact_path}-rejection.yaml` targeting a use case artifact. uc-author would consume it as if it were from uc-slicer, directing elaboration according to the foreign rejection artifact's `required_state.detail_level`.

Within the current implementation scope (only one agent pair uses rejection artifacts), this is theoretical. It becomes concrete when PM-003 extends the pattern to tspec-generator/tspec-analyst.

**Evidence:**
- `uc-author.md` Rejection Artifact Check: no step validates `rejecting_agent` field value
- `uc-slicer.md` rejection artifact template includes `rejecting_agent: "uc-slicer"` but uc-author does not check this
- `pm001-implementation-summary.md` "Scalability": "The `rejecting_agent` field disambiguates the producer" -- but the consuming agent does not actually use it for disambiguation

**Recommendation:** Add a validation step (step 2c.1) to the uc-author rejection artifact check: "Validate that `rejecting_agent` is a recognized agent name for this artifact type (currently: 'uc-slicer'). If `rejecting_agent` is unrecognized, warn the user and proceed without rejection context." This ensures the disambiguation property claimed in the scalability section is actually enforced.

---

### VULN-CROSS-002 (Low): Governance YAML `on_send` for uc-slicer Specifies Overwrite but Not Concurrent Write Safety

**Threat vector:** Race condition -- concurrent uc-slicer instances overwriting rejection artifact

**Description:** The uc-slicer `on_send` session context specifies: "Overwrite any existing rejection artifact at that path." This is correct for the single-agent case. If two concurrent uc-slicer instances process the same artifact path simultaneously (theoretically possible in parallel orchestration setups), both would attempt to write to `{artifact_path}-rejection.yaml`. The last write wins, and the interim state could leave a partial YAML file if a write is interrupted.

In the Jerry Framework's current orchestration topology (single-threaded agent execution within a session), this is not a practical risk. It becomes relevant if the framework evolves toward parallel worker execution.

**Evidence:**
- `uc-slicer.governance.yaml` on_send: "Overwrite any existing rejection artifact at that path"
- No atomic write guarantee is specified (file locking, temp-then-rename, etc.)
- Current orchestration topology does not support concurrent agent instances

**Recommendation:** Accept as residual risk given current topology. Document the assumption: "This pattern assumes single-threaded sequential agent execution. Concurrent writes to the rejection artifact are not safe and require file locking if parallel execution is adopted."

---

### VULN-CROSS-003 (Info): Phase 2 Schema Formalization Absence Creates Governance Gap

**Threat vector:** Schema drift across future agent pairs (PM-001 identified residual risk)

**Description:** The PM-001 implementation defers formal schema for `rejection-artifact-v1.schema.json` to Phase 2 (when 5+ agent pairs use the pattern). Currently, the rejection artifact schema exists only as a YAML template in uc-slicer.md and behavioral protocol in uc-author.md. There is no machine-readable schema to validate rejection artifacts at the L5 CI gate.

This is a correctly identified and documented residual risk. As a standalone assessment finding, it is classified as Info because the Phase 2 trigger condition (5+ pairs) is not met and the risk is limited to the current single pair. However, if PM-003 (tspec-generator/tspec-analyst) is implemented before Phase 2 formalization, the schema drift risk increases proportionally.

**Evidence:**
- `pm001-implementation-summary.md` "Remaining Work": formal JSON Schema deferred to Phase 2
- No `docs/schemas/rejection-artifact-v1.schema.json` file exists
- `uc-author.md` schema_version validation is a string comparison, not a formal schema check

**Recommendation:** Confirm that the Phase 2 trigger (5+ pairs) is tracked as a worktracker entity with a concrete review milestone. Alternatively, lower the Phase 2 trigger to 2 pairs -- when tspec-generator/tspec-analyst implements PM-003, there will be 2 pairs using the pattern, which may justify immediate schema formalization rather than waiting for 5.

---

## Finding Summary Table

| ID | Severity | Area | Description | Exploitable Now |
|----|----------|------|-------------|-----------------|
| VULN-PM-001 | Medium | PM-001 | No upper-bound version check on schema_version; unknown future versions silently ignored | No (no v2.0.0 exists) |
| VULN-PM-002 | Low | PM-001 | Rejection artifact timestamp TOCTOU window (mtime vs. LLM-written timestamp) | Unlikely |
| VULN-PM-003 | Low | PM-001 | Cleanup based on level comparison, not semantic completeness | Low impact |
| VULN-PM-004 | Info | PM-001 | human_message displayed without attribution to rejecting_agent | Cosmetic |
| VULN-PM-005 | Info | PM-001 | No maximum length constraint on rejection artifact string fields | Not in practice |
| VULN-IN-001 | Medium | IN-001 | SUBSTRING_TERMS length guard bypassable via Unicode padding | Yes (deterministic) |
| VULN-IN-002 | Medium | IN-001 | Layer 2b English-centric verb vocabulary; domain/non-English verbs bypasses WARN | Yes (Layer 2b WARN only) |
| VULN-IN-003 | Low | IN-001 | x-description-quality annotation creates trust confusion when absent | Cosmetic |
| VULN-IN-004 | Info | IN-001 | 20-char minLength does not prevent repetition-padded descriptions | Layer 2b catches it |
| VULN-FM-001 | Low | FM-001 | Loading prerequisites are declarative strings, not enforced; TOCTOU at CI layer | CI only |
| VULN-FM-002 | Info | FM-001 | Cross-reference prerequisite format is unvalidated free text | No runtime impact |
| VULN-FM-002-A | Low | FM-002 | then:false constraint backed by required; omission bypass path exists but is blocked | No |
| VULN-FM-002-B | Low | FM-002 | CLI gate depends on allOf support in jerry ast validate (assumed, not confirmed) | CLI implementation dependent |
| VULN-FM-002-C | Info | FM-002 | slice definition uses additionalProperties: true inconsistently | Schema cleanliness only |
| VULN-CROSS-001 | Medium | Cross | rejecting_agent field not validated by consuming agent uc-author | Theoretical (1 pair) |
| VULN-CROSS-002 | Low | Cross | Rejection artifact overwrite not concurrent-write-safe | Not in current topology |
| VULN-CROSS-003 | Info | Cross | Phase 2 schema formalization absence; schema drift risk deferred | Not until PM-003 |

**Severity breakdown:** Critical: 0 | High: 0 | Medium: 4 | Low: 6 | Info: 7

---

## Recommendations Summary

Listed in priority order by exploitability and impact:

**Medium Priority (address before PM-003 extension):**

1. **VULN-IN-001 -- Unicode padding bypass of SUBSTRING_TERMS check:** Specify Unicode-aware normalization (strip U+00A0, U+200B, U+FEFF, and all Unicode whitespace categories) before EXACT_MATCH_TERMS and SUBSTRING_TERMS matching. One-line specification change in cd-generator.md Layer 2a.

2. **VULN-CROSS-001 -- rejecting_agent not validated by uc-author:** Add step 2c.1 to the rejection artifact check: validate `rejecting_agent` is a recognized value for this artifact type. Critical to implement before PM-003 adds a second rejecting agent.

3. **VULN-PM-001 -- Schema version upper bound:** Add version-range negotiation to step 2b: if `schema_version` is not `"1.0.0"`, warn and ask the user whether to proceed rather than silently ignoring the rejection context.

4. **VULN-IN-002 -- Layer 2b English-centric vocabulary:** Document the limitation explicitly; add common domain verbs to the strong-verb list in Phase v1.1. Low urgency given WARN-not-REJECT design.

**Low Priority (address in next maintenance cycle):**

5. **VULN-PM-002 -- Timestamp comparison mechanism:** Document that Bash `stat` is used to retrieve artifact modification time; clarify the comparison is numeric against the ISO-8601 string.

6. **VULN-FM-002-B -- CLI allOf support assumption:** Confirm or add a post-completion check that `jerry ast validate --schema use_case_realization` exercises allOf constraints, not only structural validation.

7. **VULN-FM-002-A and VULN-FM-002-C:** Document the design rationale for `then: false` defense-in-depth and `additionalProperties: true` on slice objects.

**Informational (document and track):**

8. **VULN-CROSS-003 -- Phase 2 trigger:** Confirm Phase 2 schema formalization is tracked; consider lowering trigger to 2 pairs (concurrent with PM-003 implementation).

9. **VULN-PM-004 -- human_message attribution:** Add attribution wrapper for user-facing display of rejection artifact message fields.

10. **VULN-PM-005, VULN-IN-004, VULN-FM-002, VULN-CROSS-002:** Accept as known residual risk with documented rationale.

---

## Assessment Methodology

This assessment applied PTES Vulnerability Analysis phase methodology, OWASP Testing Guide vulnerability identification, and adversarial design review per the Architectural Design Vulnerability Analysis section of this agent's specification. The assessment covered:

- Trust boundary stress-testing (each boundary's assumptions challenged)
- Business logic flaw analysis (PM-001 protocol completeness, IN-001 algorithm edge cases)
- Threat model gap analysis (what the implementation summaries' own threat models missed)
- Insecure default assessment (secure configuration vs. secure design evaluation)
- OWASP A04 (Insecure Design) cross-check across all four implementations

CVSS qualitative scoring was applied for severity classification. All findings are within the same-trust-boundary scope (single user session, controlled filesystem). No findings require external network access or cross-user exploitation.

**ATT&CK technique mappings (informational):**
- VULN-IN-001: T1027 (Obfuscated Files or Information -- Unicode encoding)
- VULN-CROSS-001: T1036 (Masquerading -- impersonation of expected agent identity)
- VULN-PM-001: T1195 (Supply Chain Compromise -- future schema version injection)

---

*Agent: red-vuln (Vulnerability Analyst, /red-team skill)*
*Constitutional compliance: P-001 (all findings evidence-based with citations), P-002 (output persisted), P-022 (limitations disclosed -- assessment is advisory; all findings are within same-trust-boundary threat model)*
*Scope: Defensive architectural review only. No active exploitation, no external targets, no system modification.*
*Date: 2026-03-11*
