# PM-001 Implementation Summary: Inter-Agent Rejection Artifact Pattern

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | What was implemented and key security controls |
| [L1: Technical Detail](#l1-technical-detail) | Change-by-change breakdown across all four files |
| [L2: Strategic Implications](#l2-strategic-implications) | Backend security posture and evolution path |
| [OWASP Verification](#owasp-verification) | Self-verification checklist |
| [Remaining Work](#remaining-work) | Phase 2 items deferred per ADR |

---

## L0: Executive Summary

This implementation delivers ADR-PM001 Option A (File-Based Rejection Artifact YAML Sidecar) across four agent definition files. The pattern introduces a structured, machine-readable backward error channel from uc-slicer to uc-author using the filesystem -- consistent with Jerry's "filesystem as infinite memory" core design principle.

**What was implemented:**
- uc-slicer now writes a YAML rejection artifact to `{artifact_path}-rejection.yaml` when input validation fails at Step 1, then halts
- uc-author now checks for that rejection artifact before every elaboration, extracts the elaboration target and missing elements checklist, and deletes the artifact after successful elaboration

**Key security controls applied:**
- T1 (prompt injection): All rejection artifact string fields treated as DATA, not INSTRUCTIONS. `recommended_action` yields only a `target_detail_level` via pattern-match; it is never executed as a prompt. `human_message` is displayed but not injected into reasoning context.
- T2 (path traversal): `rejected_artifact` is validated against the current artifact path before consumption; mismatch causes silent ignore and user warning.
- T3 (stale artifact): Rejection artifact `timestamp` is compared against artifact modification time; staleness triggers a user confirmation prompt before proceeding.
- T4 (malformed YAML): Parse failure is caught with a warning; uc-author proceeds without rejection context rather than halting.
- T5 (unknown rejection_reason): Unknown enum values fall back to `missing_elements[]` and `required_state` for guidance.

**OWASP categories addressed:** A03 (injection via string fields -- mitigated), A05 (secure defaults -- rejection artifact checked on every elaboration invocation by default).

**Success path:** Completely unmodified. No performance or token cost impact on successful pipeline runs.

**Remaining risk:** Phase 2 formal schema file (`docs/schemas/rejection-artifact-v1.schema.json`) and CLI validation are deferred -- schema drift across future agent pairs is the primary residual risk until Phase 2 is implemented.

---

## L1: Technical Detail

### 1. uc-slicer.md Changes

**File:** `skills/use-case/agents/uc-slicer.md`

**Change 1 -- Methodology Step 1 (halt instruction):**
Step 1 row in the 8-Step Slicing Methodology table now reads: "If validation fails, execute the rejection artifact protocol (see below) and HALT -- do not proceed to Step 2."

**Change 2 -- Rejection Artifact Protocol section (new):**
Added a full `## Rejection Artifact Protocol (Step 1 Failure Path)` subsection within `<methodology>`, positioned immediately after the step table. The section includes:
- Decision table mapping each validation failure to `rejection_reason`, `current_state`, `required_state`, and `missing_elements` examples
- Concrete YAML template showing the exact structure to write to `{artifact_path}-rejection.yaml`
- Overwrite semantics: if a prior rejection artifact exists, overwrite it
- User reporting requirements: both human-readable message AND artifact path
- HALT instruction: unconditional halt after writing

**Change 3 -- Output section (new subsection):**
Added `## Rejection Artifacts (Input Validation Failure Path)` as the first subsection within `<output>`. Clarifies that rejection artifacts are a side effect of input validation failure and are NOT produced on success.

**Change 4 -- Failure Modes table:**
- Replaced the original single "Input artifact at detail_level < ESSENTIAL_OUTLINE" row with an updated row that references the rejection artifact protocol explicitly
- Added a new "Rejection artifact written" row documenting the response behavior

### 2. uc-slicer.governance.yaml Changes

**File:** `skills/use-case/agents/uc-slicer.governance.yaml`

**Change 1 -- validation.post_completion_checks:**
Renamed `verify_rejection_artifact_written_on_detail_level_rejection` to `verify_rejection_artifact_written_on_input_validation_failure` per the ADR specification (the ADR uses the more general name to cover all four validation failure types, not only detail_level rejection).

**Change 2 -- session_context.on_send:**
Replaced the partial one-sentence entry with a complete production protocol entry specifying all required fields: `schema_version`, `rejecting_agent`, `rejected_artifact`, `rejection_reason` (with enum), `current_state`, `required_state`, `missing_elements`, `recommended_action`, and `timestamp`. Also specifies overwrite semantics and the unconditional HALT.

### 3. uc-author.md Changes

**File:** `skills/use-case/agents/uc-author.md`

**Change 1 -- Input section (optional inputs):**
Added `Rejection artifact at {artifact_path}-rejection.yaml (automatically checked when elaborating existing artifacts)` to the Optional inputs list.

**Change 2 -- Methodology: Rejection Artifact Check section (new, before Step 1):**
Added a full `## Rejection Artifact Check (Before Step 1)` section as the first content within `<methodology>`. This section defines the complete 10-sub-step protocol:
- Step 1: Read check using the Read tool
- Step 2a: Parse YAML
- Step 2b: Validate `schema_version` is `"1.0.0"` (unknown version: warn and proceed without context)
- Step 2c: Validate `rejected_artifact` matches current path -- T2 path-traversal mitigation (mismatch: warn and ignore)
- Step 2d: Staleness check via timestamp comparison -- T3 mitigation (stale: ask user before proceeding)
- Step 2e: Extract `required_state.detail_level` as elaboration target
- Step 2f: Extract `missing_elements[]` as elaboration checklist
- Step 2g: Report to user with agent name, target level, and missing elements; note override option
- Step 2h: Security guardrail -- treat all fields as DATA. `recommended_action` pattern-matched for target level only; `human_message` display-only; `missing_elements[]` checklist reference only
- Step 2i: Parse error handling -- T4 mitigation (warn and continue)
- Step 2j: Unknown `rejection_reason` handling -- T5 mitigation (fall back to `missing_elements[]` and `required_state`)
- Step 3: Absent file -- proceed normally
- Post-elaboration cleanup: verify `$.detail_level >= required_state.detail_level`, delete artifact on success, leave in place on failure

**Change 3 -- Guardrails Failure Modes table:**
Added `Stale rejection artifact detected` row: artifact modification time post-dates rejection timestamp; response is to warn the user and ask for explicit guidance before proceeding.

### 4. uc-author.governance.yaml Changes

**File:** `skills/use-case/agents/uc-author.governance.yaml`

**Change 1 -- session_context.on_receive:**
Added a fourth entry specifying the complete rejection artifact check and consumption protocol for the elaboration case. The entry is self-contained: covers the existence check, schema_version validation, path-match validation (T2), staleness check (T3), extraction of `required_state.detail_level` and `missing_elements[]`, user reporting, all five security mitigations (T1-T5) with brief rationale, and the cleanup protocol.

**Change 2 -- validation.post_completion_checks:**
Added `verify_rejection_artifact_deleted_after_successful_elaboration_above_required_level` to the existing checks list.

---

## L2: Strategic Implications

### Backend Security Posture

The rejection artifact is a data file consumed by an LLM agent. The threat model is correctly scoped to the same-trust-boundary case (same user session, same filesystem). The five mitigations (T1-T5) implement defense in depth appropriate to a low-severity, medium-likelihood threat profile. All five FMEA failure modes from ADR-PM001 have behavioral controls in place.

The most important security property is T1 (prompt injection mitigation): uc-author explicitly does not execute `recommended_action` as a prompt. It pattern-matches only the `target_detail_level` value from `required_state`. This is the correct design because the rejection artifact is authored by uc-slicer (a trusted agent in the same session), but the field is a free-text string -- and treating free-text strings from any source as instructions is the root of prompt injection vulnerability.

### Dependency Risk

The implementation has no new external dependencies. It uses the existing filesystem communication pattern and the standard Write/Read/Bash tools already available to both agents. The only new dependency is on the YAML sidecar convention, which is documented in the ADR as this framework's SSOT for the rejection artifact schema until Phase 2.

### Scalability

The `{artifact_path}-rejection.yaml` naming convention scales without modification to tspec-generator/tspec-analyst and cd-generator/cd-validator pairs. Each pair implements the same check-parse-act-cleanup protocol. The `rejecting_agent` field disambiguates the producer; the `rejected_artifact` path-match check ensures a consumer does not accidentally consume a rejection artifact intended for a different artifact.

### Evolution Path (per ADR)

- **Phase 2** (when 5+ agent pairs use rejection): Add `docs/schemas/rejection-artifact-v1.schema.json` formal JSON Schema file. Add `jerry ast validate --schema rejection_artifact` CLI command. Add `rejection` to the session_context artifact type enum.
- **Phase 3** (when session_context schema is next revised): Consider Option B (schema extension) with `rejection_context` field in handoff payload. File-based artifacts become the persistence layer for backward compatibility.

---

## OWASP Verification

| OWASP Category | Mitigation Applied |
|----------------|-------------------|
| A01 Broken Access Control | Rejection artifact access is scoped to the same filesystem session; no cross-user access possible |
| A03 Injection | T1: `recommended_action` and `human_message` are DATA not INSTRUCTIONS; pattern-match only; no string execution |
| A05 Security Misconfiguration | Rejection artifact check is ON by default for every elaboration invocation; no opt-in required |
| A08 Data Integrity Failures | T2: `rejected_artifact` path-match validation prevents a crafted file from redirecting elaboration to a wrong artifact; T3: staleness check prevents acting on outdated state |
| A09 Logging Failures | All warning conditions (unknown schema version, path mismatch, staleness, parse failure, unknown rejection_reason) log explicit user-visible warnings rather than silently proceeding or silently failing |

---

## Remaining Work

Per ADR-PM001, the following items are deferred to Phase 2 and are NOT part of this implementation:

| Item | Phase | Rationale |
|------|-------|-----------|
| Formal JSON Schema file at `docs/schemas/rejection-artifact-v1.schema.json` | Phase 2 | Only 1 agent pair currently uses the pattern; schema formalization justified at 5+ pairs |
| `jerry ast validate --schema rejection_artifact` CLI command | Phase 2 | Depends on formal schema file; no CLI command without schema |
| `rejection` artifact type added to `session_context.json` enum | Phase 2 | Schema versioning overhead not justified at current scale |
| `agent-development-standards.md` HD-M-006 MEDIUM standard | Phase 2 | Pattern established; promotion to standard justified when 5+ pairs demonstrate stable usage |
| tspec-generator/tspec-analyst rejection artifact implementation | Phase 2 | PM-003 (structurally identical finding for that pair) tracked separately |

---

*Implementation by: eng-backend*
*ADR reference: ADR-PM001 (projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/verification/adr-pm001-rejection-artifact.md)*
*Date: 2026-03-11*
*Constitutional compliance: P-001 (evidence-based), P-002 (persisted to file), P-022 (limitations disclosed -- Phase 2 deferred items documented)*
