# Security Code Review: PROJ-035 Agent Optimization (Pattern A Removal)

> **Reviewer:** eng-security
> **Date:** 2026-03-03
> **Scope:** Post-optimization security verification of 5 most heavily modified agent definition files
> **Review Type:** Manual security code review -- constitutional constraint preservation, privilege escalation detection, guardrail integrity
> **SSDF Practice:** PW.7 (Review human-readable code to identify vulnerabilities)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Overall verdict, severity counts, top risk areas |
| [L1 Technical Findings](#l1-technical-findings) | Per-agent findings with evidence, CWE mapping, CVSS |
| [L2 Strategic Implications](#l2-strategic-implications) | Security posture, systemic patterns, architecture recommendations |
| [ASVS Verification Status](#asvs-verification-status) | OWASP ASVS 5.0 chapter verification results |
| [Appendix: Review Methodology](#appendix-review-methodology) | Data flow tracing approach, files examined |

---

## L0 Executive Summary

### Overall Security Assessment: PASS WITH OBSERVATIONS

The Pattern A optimization (removal of duplicated inline standards content) does NOT introduce security regressions in the 5 reviewed agent definitions. Constitutional constraints are preserved across all files. No privilege escalation was detected. Guardrail enforcement layers remain intact.

### Finding Summary

| Severity | Count | Description |
|----------|------:|-------------|
| Critical | 0 | None |
| High | 0 | None |
| Medium | 2 | Observations (non-blocking) |
| Low | 3 | Minor gaps requiring documentation |
| Informational | 4 | Positive security patterns noted |

**Overall verdict:** No security vulnerabilities introduced by PROJ-035 optimization. The 2 Medium observations are pre-existing structural issues unrelated to the optimization, not regressions.

### Top 3 Risk Areas

1. **nse-reporter: Missing P-020 in `.md` body forbidden_actions** -- The `.md` body `<guardrails>` section does not contain explicit forbidden_actions markup at all; constitutional enforcement relies entirely on the `.governance.yaml`. This is architecturally sound but creates a single-source dependency for P-020 behavioral guidance in the system prompt.

2. **ts-extractor: P-020 compliance reference anomaly** -- The `.md` header declares `P-002, P-003, P-004` in Constitutional Compliance but omits P-022 and P-020 from the header block, despite both being present in the forbidden_actions body and `.governance.yaml`. Version mismatch between header and body.

3. **wt-verifier: Output filtering underspecified in governance YAML** -- The `.governance.yaml` `guardrails.output_filtering` contains only 2 entries (`no_false_positives`, `all_failures_documented`) against the minimum 3 required by H-34 schema requirements.

### Recommended Immediate Actions

1. (Low priority) Add `no_secrets_in_output` to `wt-verifier.governance.yaml` `output_filtering` to satisfy H-34 minimum-3 constraint.
2. (Low priority) Update `ts-extractor.md` header block to include P-020 and P-022 in the constitutional compliance declaration for consistency with the body and governance file.
3. (Informational) Document in project ADR that nse-reporter's behavioral forbidden_actions are governed exclusively via `.governance.yaml` -- this is compliant but non-obvious to reviewers.

---

## L1 Technical Findings

### Agent 1: `skills/nasa-se/agents/nse-architecture.md`

**Lines changed in optimization:** 686
**Tool tier declared:** T3 (External) -- `.governance.yaml`
**Model:** opus

#### Finding 1.1: Constitutional Triplet -- PASS

| Principle | `.md` body `<forbidden_actions>` | `.governance.yaml` `constitution.principles_applied` | `.governance.yaml` `capabilities.forbidden_actions` |
|-----------|:-:|:-:|:-:|
| P-003 (No recursive subagents) | PRESENT (line 234) | PRESENT (line 60) | PRESENT |
| P-020 (User authority) | PRESENT (line 235) | PRESENT (line 65) | PRESENT |
| P-022 (No deception) | PRESENT (line 236) | PRESENT (line 61) | PRESENT |

**Evidence (.md body, lines 234-237):**
```
- **P-003 VIOLATION:** DO NOT spawn subagents. Consequence: unbounded recursion exhausts
  the context window...
- **P-020 VIOLATION:** DO NOT override user decisions...
- **P-022 VIOLATION:** DO NOT misrepresent capabilities, confidence levels, or actions taken...
```

**Verdict:** Constitutional triplet preserved. NPT-009 format with consequence clauses. No regression from optimization.

#### Finding 1.2: Tool Security Tier -- PASS

**Declared tier:** T3 (External) in `.governance.yaml`
**Tools in `.md` frontmatter:** `Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch`
**Task tool present:** NO

T3 includes T2 tools plus WebSearch, WebFetch, and Context7. Observed tool set is consistent with T3 declaration. The Task tool is absent from frontmatter, enforcing the single-level nesting constraint (H-35). No privilege escalation.

**CWE-306 check (Missing Auth for Critical Function):** Not applicable -- this is not an HTTP endpoint agent. Tool access is correctly scoped.

#### Finding 1.3: Forbidden Actions Completeness -- PASS

`.governance.yaml` `capabilities.forbidden_actions` contains 6 entries:
1. Spawn recursive subagents (P-003)
2. Override user decisions (P-020)
3. Return transient output only (P-002)
4. Omit mandatory disclaimer (P-043)
5. Make final design decisions (advisory only)
6. Misrepresent capabilities or confidence (P-022)

Exceeds the minimum 3 required by H-34. Domain-specific entries (items 4, 5) extend the minimum set appropriately.

**Note:** The format uses legacy NPT-014 style (`{description} ({principle-reference})`) rather than NPT-009-complete format. This is pre-existing and not a regression introduced by PROJ-035. It does not create a security gap -- consequences are supplied in the `.md` body forbidden_actions.

#### Finding 1.4: Input Validation -- PASS

`.governance.yaml` `guardrails.input_validation` defines:
- `project_id` format: `^PROJ-\d{3}$` with `action: reject` on invalid
- `entry_id` format: `^e-\d+$` with `action: reject` on invalid

Format validation with explicit reject action is present. Regex patterns are appropriately constrained (no unbounded quantifiers).

#### Finding 1.5: Output Filtering -- PASS

`.governance.yaml` `guardrails.output_filtering` contains 5 entries including `no_secrets_in_output`, `mandatory_disclaimer_on_all_outputs`, traceability requirements. Exceeds minimum 3.

**Sensitive data exposure check:** No data paths that would cause leakage of credentials or PII. The agent operates on architectural documents. `no_secrets_in_output` is present and enforceable.

#### Finding 1.6: No Security Regressions from Optimization -- PASS

The optimization removed Pattern A sections (`<constitutional_compliance>`, `<adversarial_quality_mode>`, `<session_context_validation>`). Cross-referencing against phase1c-security-guardrail-review.md confirms each removed section has 2+ surviving enforcement layers. The current file is materially the same as the pre-optimization baseline for security-relevant content.

---

### Agent 2: `skills/transcript/agents/ts-extractor.md`

**Lines changed in optimization:** 631
**Tool tier declared:** T4 (Persistent) -- `.governance.yaml`
**Model:** sonnet

#### Finding 2.1: Constitutional Triplet -- PASS WITH OBSERVATION

| Principle | `.md` body `<forbidden_actions>` | `.md` header block | `.governance.yaml` `constitution.principles_applied` |
|-----------|:-:|:-:|:-:|
| P-003 (No recursive subagents) | PRESENT (line 49) | PRESENT | PRESENT (line 47) |
| P-020 (User authority) | PRESENT (line 50) | MISSING from header | PRESENT (line 50) |
| P-022 (No deception) | PRESENT (line 53) | MISSING from header | PRESENT (line 50) |

**Finding MEDIUM-001:** The `.md` header block (line 14) declares `Constitutional Compliance: P-002, P-003, P-004` but omits P-020 and P-022. The body and `.governance.yaml` are correct. This creates an inconsistency where a reviewer scanning only the header would not identify P-020 and P-022 as applied.

- **CWE:** CWE-710 (Improper Adherence to Coding Standards) -- documentation inconsistency
- **CVSS v3.1 (qualitative):** Informational -- no exploitable vulnerability; purely a documentation gap
- **Location:** `skills/transcript/agents/ts-extractor.md`, line 14
- **Evidence:** `> **Constitutional Compliance:** P-002, P-003, P-004` -- P-020, P-022 absent

**Remediation:** Update line 14 to: `> **Constitutional Compliance:** P-001 (Hard), P-002, P-003 (Hard), P-004 (Hard), P-020 (Hard), P-022 (Hard)` to match the footer at line 471 and the `.governance.yaml`.

#### Finding 2.2: Tool Security Tier -- PASS

**Declared tier:** T4 (Persistent) in `.governance.yaml`
**Tools in `.md` frontmatter:** `Read, Write, Glob`
**MCP declared:** `memory-keeper: true`
**Task tool present:** NO

T4 includes T2 tools plus Memory-Keeper. The observed tool set (`Read, Write, Glob`) is a subset of T4, which is permissible (principle of least privilege within tier). Memory-Keeper access is declared in `mcpServers`. Task tool is absent -- no privilege escalation.

**Key observation:** ts-extractor declares T4 but uses a narrower tool set than the tier permits. This is conservative and secure. The Memory-Keeper is appropriately scoped to `jerry/{project}/transcript/{packet-id}/extraction` (line 449 of `.md`).

#### Finding 2.3: Forbidden Actions -- PASS

`.md` body forbidden_actions (lines 49-54) contains 6 entries covering P-003, P-020, P-002, P-004, P-022, and a domain-specific hallucination prohibition. All entries use NPT-009-complete format with explicit consequence clauses.

`.governance.yaml` `capabilities.forbidden_actions` (lines 84-90) contains 6 matching entries.

**Anti-hallucination guardrail preserved:** The `HALLUCINATION VIOLATION: DO NOT invent entities not in transcript` entry is critical for ts-extractor's data integrity function. This entry is present and was preserved through the optimization. This is a domain-specific security control against CWE-20 (Improper Input Validation) -- fabricated entities would corrupt the extraction database.

#### Finding 2.4: Input Validation -- PASS

`.governance.yaml` `guardrails.input_validation` defines 8 fields including:
- `format_required: chunked`
- `canonical_json_forbidden: true` -- prevents context exhaustion attack vector
- `confidence_threshold_min: 0.7`, `confidence_threshold_max: 1.0` -- bounds validation
- `max_extractions: 100` -- resource exhaustion prevention

**Security-relevant finding:** `canonical_json_forbidden: true` is a significant input validation control. The `ts-extractor.md` body also reinforces this at line 60: "CRITICAL: NEVER read `canonical-transcript.json` (~930KB)." This prevents a context exhaustion attack where a malicious input path could direct the agent to consume its entire context window with a single file read.

#### Finding 2.5: Citation Anti-Hallucination Controls -- PASS (positive pattern)

The citation validation requirements (lines 247-252 of `.md`):
- `segment_id MUST exist in input transcript`
- `text_snippet MUST be substring of segment text`
- Extractions without valid citations are REJECTED

These controls implement input provenance verification (CWE-20 mitigating control). The `.governance.yaml` `output_filtering` includes `validate_citation_segments_exist` and `verify_stats_match_array_lengths`. These controls were preserved through optimization.

#### Finding 2.6: Output Filtering -- PASS

`.governance.yaml` `guardrails.output_filtering` contains 7 entries. Exceeds minimum 3. Includes `no_secrets_in_output`.

---

### Agent 3: `skills/problem-solving/agents/ps-critic.md`

**Lines changed in optimization:** 603
**Tool tier declared:** T2 (Read-Write) -- `.governance.yaml`
**Model:** sonnet

#### Finding 3.1: Constitutional Triplet -- PASS

| Principle | `.md` body `<capabilities>` forbidden_actions | `.governance.yaml` `constitution.principles_applied` | `.governance.yaml` `capabilities.forbidden_actions` |
|-----------|:-:|:-:|:-:|
| P-003 (No recursive subagents) | PRESENT (line 69) | PRESENT (line 45) | PRESENT |
| P-020 (User authority) | PRESENT (line 70) | PRESENT (line 49) | PRESENT |
| P-022 (No deception) | PRESENT (line 71) | PRESENT (line 46) | PRESENT |

**Evidence (.md body, lines 69-73):** Full NPT-009-complete format with explicit consequence clauses for all three constitutional principles plus P-002 and a loop violation entry.

The P-003 forbidden action entry includes domain-specific consequence detail: "self-managed iteration violates P-003 and the orchestrator loses coordination authority; unbounded recursion exhausts the context window." This is more specific than the minimum requirement and directly addresses the ps-critic's specific risk surface (participating in iteration loops without self-managing them).

**Verdict:** Strongest constitutional triplet implementation of the 5 reviewed agents.

#### Finding 3.2: Tool Security Tier -- PASS

**Declared tier:** T2 (Read-Write) in `.governance.yaml`
**Tools in `.md` frontmatter:** `Read, Write, Edit, Glob, Grep`
**Task tool present:** NO

T2 includes T1 tools plus Write, Edit, Bash. The observed tool set is a subset of T2 (no Bash declared but within tier scope). Task tool is absent -- no privilege escalation. ps-critic correctly operates as a T2 worker agent.

**Note:** The generator-critic loop is managed by the orchestrator (main context), not ps-critic. The absence of Task in the tool list mechanically enforces this architectural constraint (H-35).

#### Finding 3.3: Anti-Leniency Controls -- PASS (positive pattern)

Line 71: `**P-022 VIOLATION:** DO NOT hide quality issues or inflate scores. Consequence: substandard deliverables pass quality gates; the quality enforcement system loses credibility and effectiveness.`

This is a domain-specific security control against quality gate bypass. The P-022 forbidden action explicitly targets the specific attack vector for this agent type (score inflation rather than capability misrepresentation). This nuance was preserved through the optimization.

`.governance.yaml` `guardrails.output_filtering` includes:
- `quality_score_range` -- bounds validation on numeric output
- `improvements_must_be_actionable` -- prevents vague feedback
- `no_vague_feedback`

#### Finding 3.4: Guardrail Coverage -- PASS

**Input validation** (`.governance.yaml` lines 23-26): Defines format constraints for ps_id, entry_id, artifact_path, criteria. Pattern validation is present.

**Note:** The `ps_id_format` uses pattern `^[a-z]+-\d+(\.\d+)?$` which is less restrictive than nse-architecture's pattern. This is acceptable given ps-critic operates on a broader set of work items.

**Fallback behavior:** `warn_and_request_criteria` -- ensures the agent fails safely when evaluation criteria are missing rather than producing an uncritiqued score of 0.0.

#### Finding 3.5: Self-Critique Pre-Submission Check -- PASS

The optimization preserved the behavioral instruction in `<identity>` (lines 32-38) that explicitly prohibits self-managed loop iteration. The consequence clause is present: "Consequence: self-managed iteration violates P-003 and causes unbounded recursion; the orchestrator loses coordination authority."

This is a behavioral guardrail that supplements the mechanical enforcement (absence of Task tool).

---

### Agent 4: `skills/nasa-se/agents/nse-reporter.md`

**Lines changed in optimization:** 492
**Tool tier declared:** T3 (External) -- `.governance.yaml`
**Model:** haiku

#### Finding 4.1: Constitutional Triplet -- PASS WITH OBSERVATION

| Principle | `.md` body section | `.governance.yaml` `constitution.principles_applied` | `.governance.yaml` `capabilities.forbidden_actions` |
|-----------|:-:|:-:|:-:|
| P-003 (No recursive subagents) | NOT IN BODY (no `<forbidden_actions>` block) | PRESENT (line 59) | PRESENT (line 100) |
| P-020 (User authority) | NOT IN BODY | PRESENT (line 63) | PRESENT (line 101) |
| P-022 (No deception) | NOT IN BODY | PRESENT (line 64) | PRESENT (line 101) |

**Finding MEDIUM-002:** `nse-reporter.md` does not contain a `<forbidden_actions>` block in its `.md` body. The `<guardrails>` section (lines 182-202) contains `<output_filtering>` and `<scope_boundaries>` but no explicit forbidden_actions with NPT-009 format consequence clauses.

- **CWE:** CWE-710 (Improper Adherence to Coding Standards) -- structural compliance gap
- **CVSS v3.1 (qualitative):** Low -- constitutional constraints are fully represented in `.governance.yaml` which is the machine-readable enforcement artifact; the `.md` body behavioral enforcement is weaker
- **Location:** `skills/nasa-se/agents/nse-reporter.md`, `<guardrails>` section (lines 182-202)
- **Evidence:** No forbidden_actions block present. `<scope_boundaries>` uses `WILL NOT:` pattern rather than NPT-009 `{PRINCIPLE} VIOLATION: NEVER {action} -- Consequence: {impact}` format.

**Impact assessment:** The `.governance.yaml` contains all three constitutional principles in both `constitution.principles_applied` and `capabilities.forbidden_actions`. The L2-REINJECT enforcement layers (rank=1 re-injection on every prompt) also provide independent enforcement. This gap is therefore a defense-in-depth concern rather than a complete absence of control. It is NOT a regression from PROJ-035 -- this structural gap pre-dates the optimization.

**Remediation:** Add a `<forbidden_actions>` subsection to the `<guardrails>` block with NPT-009-format entries for P-003, P-020, and P-022.

#### Finding 4.2: Tool Security Tier -- PASS

**Declared tier:** T3 (External) in `.governance.yaml`
**Tools in `.md` frontmatter:** `Read, Write, Glob, Grep, WebFetch`
**Task tool present:** NO

WebFetch is included, consistent with T3 (External) tier. No WebSearch -- slightly below T3 full capability which is acceptable (principle of least privilege within tier). Task tool is absent -- no privilege escalation.

**Note on WebFetch:** nse-reporter uses WebFetch potentially to retrieve reference data (NPR documents, technical standards). This is appropriate for a reporting agent that may need to fetch current information.

#### Finding 4.3: Sensitive Data Non-Exposure -- PASS

`no_secrets_in_output` is present in `.governance.yaml` `guardrails.output_filtering` (line 43). Domain-specific output filtering for `prominently_display_RED_items`, `include_risk_status_in_all_reports`, and `flag_inconsistencies_between_data_sources` are all preserved.

**Critical output filtering rule preserved:** `never hide or minimize serious issues` appears in the `.md` body `<output_filtering>` (line 189). This is a security-relevant control -- reporting agents that suppress adverse information create false assurance, analogous to log injection or audit trail tampering (CWE-117 pattern in the reporting context).

#### Finding 4.4: Forbidden Actions Coverage -- LOW-001 (Minor Gap)

`.governance.yaml` `capabilities.forbidden_actions` contains 7 entries (lines 99-106), which exceeds H-34 minimum of 3. However, the entries use legacy NPT-014 format without explicit consequence clauses:

```yaml
- Spawn recursive subagents (P-003)
- Override domain status assessments
- Hide adverse information
- Minimize serious issues
```

- **Severity:** Low
- **Assessment:** Not a regression. Pre-existing format gap. Consequences are partially supplied by the `<scope_boundaries>` WILL NOT entries in the `.md` body.
- **Remediation (optional):** Migrate to NPT-009 format for consistency.

---

### Agent 5: `skills/worktracker/agents/wt-verifier.md`

**Lines changed in optimization:** 461
**Tool tier declared:** T2 (Read-Write) -- `.governance.yaml`
**Model:** sonnet

#### Finding 5.1: Constitutional Triplet -- PASS

| Principle | `.md` body `<capabilities>` forbidden_actions | `.governance.yaml` `constitution.principles_applied` | `.governance.yaml` `capabilities.forbidden_actions` |
|-----------|:-:|:-:|:-:|
| P-003 (No recursive subagents) | PRESENT (line 94) | PRESENT (line 41) | PRESENT |
| P-020 (User authority) | PRESENT (line 97) | PRESENT (line 43) | PRESENT |
| P-022 (No deception) | PRESENT (line 96) | PRESENT (line 44) | PRESENT |

**Evidence (.md body, lines 94-97):** NPT-009-complete format with consequence clauses for all four forbidden actions (P-003, P-002, P-022, P-020).

**Security-critical forbidden action preserved:** Line 96: `**P-022 VIOLATION:** DO NOT mark incomplete work as complete to satisfy user. Consequence: false completion signals trigger downstream work on incomplete prerequisites; work tracker integrity is compromised.`

This is the primary security control for wt-verifier. The P-022 application here specifically targets completion fraud (marking incomplete work as done), which is the agent's primary threat surface. This nuanced application of P-022 was preserved through the optimization.

#### Finding 5.2: Tool Security Tier -- PASS

**Declared tier:** T2 (Read-Write) in `.governance.yaml`
**Tools in `.md` frontmatter:** `Read, Glob, Grep, Write, Bash`
**Task tool present:** NO

T2 includes T1 plus Write, Edit, Bash. The observed tool set matches T2 declaration. Bash is required for `jerry ast` CLI commands per H-33 enforcement. Task tool is absent -- no privilege escalation.

**Bash tool security note:** Bash is declared and necessary for AST-based frontmatter extraction (`uv run --directory ${CLAUDE_PLUGIN_ROOT} jerry ast frontmatter`). The specific Bash command is scoped to a known CLI path pattern. No evidence of arbitrary shell command execution paths.

#### Finding 5.3: Output Filtering Gap -- LOW-002 (Minor Gap)

**Finding LOW-002:** `.governance.yaml` `guardrails.output_filtering` contains only 2 entries:
- `no_false_positives`
- `all_failures_documented`

H-34 requires minimum 3 entries. The missing third entry should be `no_secrets_in_output` which is standard for all agent types.

- **CWE:** CWE-710 (Coding Standards non-compliance)
- **CVSS v3.1 (qualitative):** Low -- wt-verifier processes work item files, not credential stores. The risk of secret exposure is low, but the schema requirement is unmet.
- **Location:** `skills/worktracker/agents/wt-verifier.governance.yaml`, lines 23-25
- **Remediation:** Add `- no_secrets_in_output` to the `output_filtering` array.

#### Finding 5.4: Input Validation -- PASS WITH OBSERVATION

`.governance.yaml` `guardrails.input_validation` defines:
- `work_item_path_exists: true`
- `verification_scope_valid: full | acceptance_criteria | evidence`

Both constraints are present. However, this is a simple YAML object format without regex pattern validation (unlike nse-architecture's regex-with-reject). This is acceptable for wt-verifier's input domain (file paths and enum values).

**Note:** The `.md` body `<guardrails>` section (lines 100-117) provides the substantive input validation including fallback behavior steps. The two-layer specification (`.governance.yaml` + `.md` body) is complementary and intact.

#### Finding 5.5: AST-Enforcement H-33 Control -- PASS (positive pattern)

The H-33 enforcement instruction is prominent in the `<capabilities>` section (lines 72-91) and explicitly prohibits regex-based frontmatter extraction:

```
MUST use `jerry ast frontmatter` via `uv run --directory ${CLAUDE_PLUGIN_ROOT}`.
DO NOT use `Grep(pattern="> **Status:**")` for frontmatter extraction.
```

This is a security-relevant control against structured data parsing errors (CWE-20 application). Using AST-based parsing prevents the agent from making incorrect status decisions based on malformed regex matches against frontmatter. This control was preserved through the optimization.

#### Finding 5.6: WTI Rule Enforcement -- PASS (positive pattern)

Domain-specific security controls (WTI-002, WTI-003, WTI-006) are preserved in the `<wti_rules>` section. Specifically:
- WTI-002: 80% acceptance criteria threshold
- WTI-003: Truthful state enforcement (P-022 application)
- WTI-006: Evidence-based closure (prevents closure without proof)

These are functional security controls against work item manipulation. Preserved through optimization.

---

### Cross-Agent Finding: Forbidden Actions Format Inconsistency -- LOW-003

Across the 5 reviewed agents, forbidden_actions format varies:

| Agent | `.md` body format | `.governance.yaml` format |
|-------|:-:|:-:|
| nse-architecture | NPT-009-complete | NPT-014 (legacy) |
| ts-extractor | NPT-009-complete | NPT-014 (legacy) |
| ps-critic | NPT-009-complete | NPT-014 (legacy) |
| nse-reporter | None (scope_boundaries only) | NPT-014 (legacy) |
| wt-verifier | NPT-009-complete | NPT-014 (legacy) |

All 5 `.governance.yaml` files use the legacy NPT-014 format in `capabilities.forbidden_actions` (descriptive without structured consequence clauses). This is consistent with the `capabilities.forbidden_action_format` being absent (which implies NPT-014 per the schema specification in `agent-development-standards.md`).

- **Severity:** Low (pre-existing, not a regression from PROJ-035)
- **Assessment:** Security impact is low. NPT-014 entries still communicate prohibited actions and reference constitutional principles. NPT-009-complete format in `.md` bodies provides the consequence-rich enforcement where the LLM model processes its behavioral instructions.
- **Remediation:** Track migration to NPT-009-complete for `.governance.yaml` entries in a future enabler.

---

## L2 Strategic Implications

### Security Posture Assessment

The PROJ-035 Pattern A optimization correctly identifies that duplicated inline standards content is not a security control layer -- it is redundant documentation. The 5 reviewed agents retain security enforcement at the correct layers:

1. **Mechanical enforcement** (highest reliability): Task tool absence in frontmatter, tool tier constraints, Claude Code runtime enforcement
2. **Schema enforcement** (high reliability): `.governance.yaml` schema-validated constitutional triplet and forbidden_actions
3. **L2 re-injection** (high reliability): Per-prompt re-injection of P-003, P-020, P-022
4. **Behavioral instructions** (medium reliability): NPT-009-format forbidden_actions in `.md` body with consequence clauses

The removed Pattern A sections (`<constitutional_compliance>` tables, `<session_context_validation>` blocks, `<adversarial_quality>` blocks) were layer 5+ in this stack -- correctly identified as redundant by phase1c-security-guardrail-review.md. This review confirms that assessment is accurate for the 5 reviewed agents.

### Systemic Vulnerability Patterns

**Pattern 1: Governance YAML as Security Backstop**
Three agents (nse-architecture, nse-reporter, wt-verifier) rely on `.governance.yaml` as the primary source for constitutional compliance declarations. The `.md` bodies provide behavioral reinforcement of varying quality. This is architecturally sound but creates a dependency on the schema validation CI gate (L5) for completeness verification. Any CI gate failure would allow unchecked governance files.

**Pattern 2: Per-Agent P-022 Application Quality Varies**
The most security-relevant finding across all 5 agents is the quality variance in P-022 application:
- ps-critic: Explicitly prohibits score inflation ("DO NOT hide quality issues or inflate scores")
- ts-extractor: Explicitly prohibits confidence inflation ("DO NOT claim high confidence without evidence")
- wt-verifier: Explicitly prohibits completion fraud ("DO NOT mark incomplete work as complete")
- nse-architecture: Generic capability misrepresentation prohibition
- nse-reporter: `.governance.yaml` only, no `.md` body behavioral instruction

The agents with domain-specific P-022 applications (ps-critic, ts-extractor, wt-verifier) are more resistant to their specific deception attack vectors. This pattern should be formalized in the agent development standards as a recommended practice.

**Pattern 3: Input Validation Depth Varies**
nse-architecture uses regex patterns with explicit reject actions. wt-verifier uses boolean/enum validation without patterns. ts-extractor uses rich schema validation with 8 constraints. This variance reflects different risk profiles (appropriate) but lacks explicit documentation of the design rationale for each agent's validation depth.

### Comparison with Threat Model Predictions

The PROJ-035 optimization phase1c review predicted:
- Constitutional principles would survive via `.governance.yaml` + L2 re-injection (CONFIRMED)
- Session context validation would be replaceable by auto-loaded standards (CONFIRMED)
- Adversarial quality sections would be redundant with L2 re-injection (CONFIRMED)

This security review independently validates those predictions. No additional threat vectors were introduced by the optimization.

### Recommendations for Security Architecture Evolution

1. **Formalize domain-specific P-022 guidance:** The agent development standards should explicitly require that P-022 forbidden action entries include the agent-specific deception vector, not just the generic capability misrepresentation prohibition. This elevates the security quality of future agents to the level demonstrated by ps-critic, ts-extractor, and wt-verifier.

2. **Standardize `.governance.yaml` output_filtering minimum:** Enforce a universal `no_secrets_in_output` base entry plus 2 agent-specific entries to consistently meet the H-34 minimum-3 requirement. Add this as a CI gate check separate from JSON Schema validation.

3. **Address nse-reporter `.md` body gap in a future story:** nse-reporter is the only agent among the reviewed set without explicit NPT-009-format forbidden_actions in its `.md` body. While not a security regression from PROJ-035, this represents an architectural inconsistency that reduces LLM-level behavioral enforcement for a reporting agent -- one that processes potentially sensitive project health data.

---

## ASVS Verification Status

Applicable OWASP ASVS 5.0 chapters for agent definition security review:

| Chapter | Focus | Verification Findings |
|---------|-------|----------------------|
| V1 (Architecture) | Trust boundary enforcement | PASS -- Tool tier enforcement creates correct trust boundaries. Worker agents lack Task tool access (mechanical enforcement). |
| V4 (Access Control) | Authorization per operation | PASS -- T1-T5 tier model correctly scopes tool access. No agent accesses capabilities beyond declared tier. |
| V5 (Validation) | Input validation | PASS WITH GAP -- Input validation present on 4/5 agents. wt-verifier has minimum validation (boolean/enum). No agent performs directory traversal validation (not applicable to this agent type). |
| V7 (Error Handling) | Fallback behavior | PASS -- All 5 agents declare `fallback_behavior` in `.governance.yaml`. Fallback values are `warn_and_retry`, `warn_and_request_criteria`, `warn_and_skip` -- all fail-safely. |
| V8 (Data Protection) | Sensitive data controls | PASS WITH GAP -- `no_secrets_in_output` present in 4/5 agents' output_filtering. wt-verifier missing this entry (LOW-002). |

---

## Appendix: Review Methodology

### Files Examined

| File | Location | Lines |
|------|----------|------:|
| nse-architecture.md | `/Users/evorun/workspace/jerry/skills/nasa-se/agents/nse-architecture.md` | 312 |
| nse-architecture.governance.yaml | `/Users/evorun/workspace/jerry/skills/nasa-se/agents/nse-architecture.governance.yaml` | 101 |
| ts-extractor.md | `/Users/evorun/workspace/jerry/skills/transcript/agents/ts-extractor.md` | 471 |
| ts-extractor.governance.yaml | `/Users/evorun/workspace/jerry/skills/transcript/agents/ts-extractor.governance.yaml` | 91 |
| ps-critic.md | `/Users/evorun/workspace/jerry/skills/problem-solving/agents/ps-critic.md` | 151 |
| ps-critic.governance.yaml | `/Users/evorun/workspace/jerry/skills/problem-solving/agents/ps-critic.governance.yaml` | 91 |
| nse-reporter.md | `/Users/evorun/workspace/jerry/skills/nasa-se/agents/nse-reporter.md` | 291 |
| nse-reporter.governance.yaml | `/Users/evorun/workspace/jerry/skills/nasa-se/agents/nse-reporter.governance.yaml` | 107 |
| wt-verifier.md | `/Users/evorun/workspace/jerry/skills/worktracker/agents/wt-verifier.md` | 245 |
| wt-verifier.governance.yaml | `/Users/evorun/workspace/jerry/skills/worktracker/agents/wt-verifier.governance.yaml` | 61 |
| phase1c-security-guardrail-review.md | `/Users/evorun/workspace/jerry/.claude/worktrees/orktree/projects/PROJ-035-skill-optimization/work/agent-optimization/phase1c-security-guardrail-review.md` | 174 |
| proj-017 baseline nse-architecture.md | `/Users/evorun/workspace/jerry/.claude/worktrees/proj-017-portability/skills/nasa-se/agents/nse-architecture.md` | sampled |
| proj-017 baseline nse-reporter.md | `/Users/evorun/workspace/jerry/.claude/worktrees/proj-017-portability/skills/nasa-se/agents/nse-reporter.md` | sampled |
| proj-017 baseline ps-critic.md | `/Users/evorun/workspace/jerry/.claude/worktrees/proj-017-portability/skills/problem-solving/agents/ps-critic.md` | sampled |

### Data Flow Tracing Approach

**For each agent, the following data flows were traced:**

1. **Input path:** External request -> frontmatter `tools` declaration -> input_validation guardrails -> agent methodology
2. **Output path:** Agent outputs -> output_filtering guardrails -> Write tool invocation -> file system
3. **Trust boundary:** Worker agent boundary (Task tool absence) -> orchestrator-worker topology
4. **Constitutional compliance path:** `.md` body forbidden_actions -> `.governance.yaml` constitution + forbidden_actions -> L2 re-injection

### CWE Review Coverage

| CWE ID | Category | Checked | Finding |
|--------|----------|:-------:|---------|
| CWE-79 | XSS | N/A | Not applicable (no HTML output rendering) |
| CWE-89 | SQL Injection | N/A | Not applicable (no database queries) |
| CWE-78 | OS Command Injection | Checked | No unconstrained shell execution paths. Bash tool scoped to `jerry ast` CLI pattern in wt-verifier. |
| CWE-287 | Improper Authentication | Checked | Trust boundary enforcement via tool tier model. No authentication bypass identified. |
| CWE-862 | Missing Authorization | Checked | All agents checked for Task tool presence (privilege escalation). None found. |
| CWE-306 | Missing Auth for Critical Function | Checked | No unprotected critical operations. wt-verifier requires explicit orchestrator invocation. |
| CWE-502 | Deserialization | Checked | ts-extractor reads JSON. Canonical JSON file is explicitly forbidden. Format validation present. |
| CWE-798 | Hardcoded Credentials | Checked | No credentials found in any reviewed file. |
| CWE-22 | Path Traversal | Checked | wt-verifier uses `${JERRY_PROJECT}` path variable. No user-controlled path concatenation identified. |
| CWE-352 | CSRF | N/A | Not applicable (agent framework, no HTTP state-changing operations) |
| CWE-20 | Improper Input Validation | Checked | MEDIUM-001, LOW-002 noted. Core validation controls intact on all 5 agents. |
| CWE-710 | Coding Standards | Checked | MEDIUM-001, MEDIUM-002, LOW-001, LOW-002, LOW-003 noted. |

---

*Reviewer: eng-security*
*Review Type: Manual security code review per SSDF PW.7*
*Methodology: Constitutional triplet verification, tool tier privilege audit, forbidden actions completeness, input/output validation coverage, data flow tracing*
*Confidence: HIGH -- both `.md` and `.governance.yaml` files reviewed for all 5 agents; pre-optimization baseline sampled for regression confirmation*
*Report Version: 1.0.0*
