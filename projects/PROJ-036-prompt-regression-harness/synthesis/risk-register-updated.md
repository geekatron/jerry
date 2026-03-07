# Updated Risk Register: Four-Layer Composite Test Harness

> **Project:** PROJ-036 (Prompt Regression Harness)
> **Stream:** 7B (Cross-Synthesis)
> **Date:** 2026-03-07
> **Agent:** ps-synthesizer v2.3.0
> **Criticality:** C4
> **Quality Threshold:** >= 0.94
> **Sources:** 5A (Security Assessment), 5B (FMEA V&V), 5C (Test Suite gaps), 1B (Design risks), 3E (CI/CD operational risks)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Risk posture overview |
| [L1: Risk Register Table](#l1-risk-register-table) | All risks with ID, description, likelihood, impact, status, residual |
| [L1: Pre-Production Blockers](#l1-pre-production-blockers) | Risks that must be mitigated before any production deployment |
| [L1: Accepted Residual Risks](#l1-accepted-residual-risks) | Risks explicitly accepted per ADR-001 |
| [L1: Open Risk Items](#l1-open-risk-items) | Risks requiring future work |
| [L2: Risk Consolidation Analysis](#l2-risk-consolidation-analysis) | Cross-source patterns, RPN reduction summary, strategic risk posture |
| [Risk Source Traceability](#risk-source-traceability) | Mapping from risk IDs to source documents |

---

## L0: Executive Summary

The consolidated risk register synthesizes risks from five sources: the FMEA (10 original failure modes), the security assessment (9 findings, 40 STRIDE threats), the V&V gap analysis, the system design risk register, and the CI/CD operational risk analysis. Total risks consolidated: 28 distinct risk items after deduplication.

Overall risk posture: **MEDIUM-HIGH**, reducing to **MEDIUM** upon resolution of two pre-production blockers (RR-001 input sanitization, RR-002 Docker digest pinning). The core statistical regression detection mission has LOW residual risk: all must-have FM mitigations are FULLY MITIGATED (FM-001, FM-002, FM-004, FM-005, FM-006, FM-010) or have accepted residual (FM-003, FM-007, FM-009). The harness correctly identifies regressions when its test cases cover the changed behavioral dimensions.

The highest residual risk is RR-007 (incomplete MR coverage for agent-specific behavioral properties, FM-003 residual RPN=96), which is structurally irreducible until Phase D implementation of agent-specific MRs. The second highest is RR-008 (false confidence from incomplete test suite coverage, FM-007 residual RPN=216), which is mitigated by process control (authorship checklist FR-027) but cannot be eliminated technically.

Total FMEA RPN reduction: from 1,823 (original) to 400 (residual) = **78.1% reduction**.

---

## L1: Risk Register Table

### Risk ID Format: RR-{NNN}

| Risk ID | Category | Description | Likelihood | Impact | Mitigation Status | Residual Risk | Source |
|---------|----------|-------------|------------|--------|-------------------|---------------|--------|
| **RR-001** | Security | Input sanitization absent from `deepeval_adapter.py` (MC-02 MISSING). Adversarial YAML test cases can deliver prompt injection payloads that manipulate LLM judge scoring, producing false PASS verdicts on regressed prompts. | HIGH | HIGH | **OPEN — Pre-Production Blocker** | HIGH (CVSS 6.5, CWE-20) | 5A F-001, 1B T-02 |
| **RR-002** | Security | Docker image not pinned to SHA-256 digest (MC-08 MISSING). Smoke workflow uses `:latest` tag; Standard/Full use `0.86.0` version tag only. Registry compromise could substitute malicious image to exfiltrate API keys or corrupt outputs. | MEDIUM | HIGH | **OPEN — Pre-Production Blocker** | HIGH (CVSS 7.4, CWE-1395) | 5A F-002, 1B T-08 |
| **RR-003** | Security | `BaselineStore._validate_version_key()` performs only structural format validation, not 40-hex-char hash pattern or path allowlist validation. Weaker than `version_keys.py`. | LOW | MEDIUM | PARTIAL — path traversal mitigated by SHA-256 slug path; full bypass requires malicious write access | MEDIUM (CVSS 5.3) | 5A F-003 |
| **RR-004** | Security | `evaluate_batch()` silently swallows exceptions, appending 0.0 scores. Adversarial inputs triggering consistent exceptions produce all-0.0 score arrays. High failure rate (>20%) not surfaced to CI/CD summary. | MEDIUM | MEDIUM | PARTIAL — `stats.py` `_validate_score_array()` rejects all-identical arrays; mixed corruption not caught | MEDIUM (CVSS 4.3) | 5A F-004 |
| **RR-005** | Security | AGENT_ID environment variable derived from git-diff filenames without allowlist validation against `COVERED_AGENTS` frozenset before Docker invocation. | LOW | MEDIUM | PARTIAL — Docker isolation limits damage; no confirmed exploit path | LOW (CVSS 4.6) | 5A F-005 |
| **RR-006** | Security | SHA-256 truncation to 64 bits in `compute_prompt_content_hash()` — below NIST SP 800-57 128-bit minimum for collision-resistant identifiers. | LOW | LOW | PARTIAL — 64-bit space still collision-resistant for practical scenarios; not NIST-compliant | LOW (CVSS 3.4) | 5A F-009 |
| **RR-007** | Coverage | Incomplete metamorphic relation coverage (FM-003). 5 universal MRs cover cross-cutting behavioral properties. Agent-specific behavioral invariants (e.g., nse-requirements must produce a traceability matrix) not yet encoded. Each new agent type adds uncovered behavioral space. | MEDIUM | HIGH | ACCEPTED — 5 universal MRs cover major perturbation types; FR-012 deferred to Phase D; FR-013 (coverage tracking) NOT STARTED | RPN = 96 (S=8, O=2, D=6; reduced from 240) | 5B FM-003, 5C gap |
| **RR-008** | Coverage | False confidence from incomplete test suite coverage (FM-007). Harness passes but test cases don't cover the changed behavioral dimension. Structurally irreducible — no technical gate can guarantee complete behavioral coverage. | MEDIUM | HIGH | ACCEPTED — FR-027 (authorship checklist) implemented as PR warning; FR-013 MR coverage tracking deferred | RPN = 216 (S=9, O=3, D=8; reduced from 432) | 5B FM-007 |
| **RR-009** | Statistical | MR violation ambiguity before empirical calibration (FM-009). Tolerance values set from initial estimates; calibration against 100+ real output pairs not yet executed. Pre-calibration MR violations are warnings, not failures. | MEDIUM | MEDIUM | PARTIAL — tolerance values per contracts C.1-C.5; calibration process documented; empirical run pending | RPN = 50 (post-calibration; S=5, O=2, D=5; down from 125) | 5B FM-009 |
| **RR-010** | Statistical | STANDARD mode N accumulation protocol undocumented. STANDARD mode produces N=10 per evaluation run; Wilcoxon requires N >= 20. The mechanism for accumulating runs across sessions to reach N >= 20 before statistical comparison is not specified. | LOW | MEDIUM | OPEN — STANDARD mode Wilcoxon would raise InsufficientSamplesError if invoked with a single 10-run evaluation | MEDIUM | QG-2 gap, 5B |
| **RR-011** | Dependency | DeepEval version pinning incomplete (FM-008, FR-026 PARTIAL). `deepeval` absent from `pyproject.toml`. AC-1 (pinned version in `uv.lock`) not satisfiable. | LOW | LOW | OPEN — model pinning confirmed (primary control); package dependency pinning is secondary control | RPN = 20 (S=5, O=2, D=2; down from 60; model pin is primary) | 5B FM-008, FR-026 |
| **RR-012** | Dependency | npm dependency conflict with UV-only Python environment (FM-004). promptfoo is a Node.js tool incompatible with UV dependency management. | LOW | MEDIUM | MITIGATED — Docker isolation completely prevents npm/UV conflicts; fallback path (Python API) documented per ADR-001 | RPN = 0 (residual); accepted fallback noted | 5B FM-004 |
| **RR-013** | Cost/Ops | LLM cost overrun from multi-sample statistical engine (FM-006). Full mode (N=30 per version, 13 metrics) could reach $5-8 per agent evaluation. | MEDIUM | MEDIUM | MITIGATED — Tiered modes (Smoke=$0, Standard=~$2, Full=~$5-8); per-test case $0.50 cost assertion; cost monitoring composite action | RPN = 0 (residual per FMEA); operational monitoring required | 5B FM-006, 1B |
| **RR-014** | Statistical | Prompt version mismatch in baseline store (FM-005). Comparison against wrong baseline produces meaningless results; may silently pass a regression. | LOW | HIGH | MITIGATED — FR-004 git commit hash composite key; FR-020 baseline quality gate; BaselineMismatchError hard exception | RPN = 0 (fully mitigated) | 5B FM-005 |
| **RR-015** | Statistical | Stale baseline captures known-poor prompt version (FM-010). Comparing against known-bad baseline produces false pass results. | LOW | HIGH | MITIGATED — FR-020 baseline quality gate (mean >= 0.92 hard rejection); `audit()` staleness tracking; `invalidate()` for MAJOR contract releases | RPN = 0 (fully mitigated) | 5B FM-010 |
| **RR-016** | Statistical | Vanilla LLM-as-Judge bias invalidates comparison (FM-001). Position and order bias in LLM-as-Judge scoring makes comparisons unreliable. | HIGH | HIGH | MITIGATED — FR-021 position randomization + rubric shuffling mandatory (ValueError if bypassed) | RPN = 0 (fully mitigated) | 5B FM-001 |
| **RR-017** | Statistical | Statistical false alarm from small evaluation sets (FM-002). CLT-based methods perform poorly for N < 20. | MEDIUM | MEDIUM | MITIGATED — FR-014 N >= 20 hard enforcement (InsufficientSamplesError); Smoke mode labeled STRUCTURAL ONLY | RPN = 0 (fully mitigated) | 5B FM-002 |
| **RR-018** | CI/CD | GitHub Actions workflow hijacking (T-29). Malicious PRs could exploit misconfigured workflow permissions to access secrets or override test results. | LOW | HIGH | MITIGATED — `pull_request` event (not `pull_request_target`); minimal permissions (contents: read, pull-requests: write); fork secret isolation per MC-28 | LOW | 1B T-29, 5A A01 |
| **RR-019** | CI/CD | API key exposure in CI/CD logs (T-25). `ANTHROPIC_API_KEY` logged or interpolated into command strings. | LOW | HIGH | MITIGATED — GHA secrets only (never hardcoded); `::add-mask::` applied; passed as named env var (not interpolated) | LOW | 1B T-25, 5A A07 |
| **RR-020** | CI/CD | promptfoo `file://` protocol handler could read arbitrary files from Docker container via crafted YAML test case (T-07). | LOW | MEDIUM | PARTIAL — read-only mounts, cap-drop, no-new-privileges limit damage; no explicit file:// protocol restriction in promptfoo-config.yaml | LOW-MEDIUM | 1B T-07, 5A A10 |
| **RR-021** | Supply Chain | promptfoo npm package pinned to version tag `0.86.0` (not npm integrity hash or lockfile). `npm install -g` without `npm ci`. No automated CVE scanning (Trivy, Grype, npm audit) in CI pipeline. | MEDIUM | HIGH | PARTIAL — version tag provides partial protection; no digest pinning; no automated scanning | MEDIUM | 5A A06 |
| **RR-022** | Supply Chain | No automated key rotation schedule for `ANTHROPIC_API_KEY`. Key management is entirely manual operational procedure. | LOW | MEDIUM | OPEN — no rotation policy documented or enforced | LOW-MEDIUM | 5A A02 |
| **RR-023** | Architecture | Dual `InsufficientSamplesError` classes with incompatible constructors (stats.py vs. base.py). Callers in different layers receive different exception types with different message formats. | LOW | MEDIUM | OPEN — `jerry/testing/__init__.py` re-exports only `stats.py` version; `base.py` version is local to metamorphic package | LOW (localized impact) | QG-2 critical finding |
| **RR-024** | Architecture | Peer coupling in metamorphic package: `mr_003_context.py`, `mr_004_formatting.py`, `mr_005_roundtrip.py` import `_wilcoxon_p_and_effect` from `mr_001_paraphrase.py`. | LOW | LOW | OPEN — documented; within-package only; no H-07 violation | LOW (structural debt) | QG-2 gap |
| **RR-025** | Requirements | FR-013 contract path discrepancy: FR-013 specifies `tests/prompt-regression/contracts/{agent-id}.yaml`; 1D delivers at `contracts/per-agent/`. Runtime path for FR-013 MR coverage computation is ambiguous. | LOW | LOW | OPEN — FR-013 NOT STARTED; will need reconciliation during Phase D implementation | LOW | QG-1 finding |
| **RR-026** | Requirements | FR-013 and FR-012 NOT STARTED. MR coverage tracking and agent-specific MRs are SHOULD-priority requirements not implemented. Until Phase D, the harness has no visibility into coverage of agent-specific behavioral properties. | LOW | MEDIUM | ACCEPTED — SHOULD priority; does not block primary regression detection mission | MEDIUM (systemic coverage gap) | 5B VCRM |
| **RR-027** | Design | T-41 (uncatalogued): adversarial input crafting to trigger false MR violations by generating paraphrase inputs designed to trigger MR-001 violations and block legitimate merges. Not in T-01 through T-40 threat catalog. | LOW | MEDIUM | PARTIAL — paraphrase generation uses deterministic rule-based regex (not LLM); dual-condition violation required (statistical + practical); single MR failures are warnings until calibrated | LOW | QG-1 gap (Architectural Coherence) |
| **RR-028** | Monitoring | STANDARD mode N accumulation: no mechanism to accumulate N=10-run batches to N >= 20 across sessions for Wilcoxon comparison. STANDARD mode effectively cannot trigger statistical comparison in single evaluation run. | LOW | MEDIUM | OPEN — architectural protocol gap; Wilcoxon would raise InsufficientSamplesError if attempted | MEDIUM | QG-2 Quantitative Consistency gap |

---

## L1: Pre-Production Blockers

These two risks MUST be mitigated before the harness is used with production API keys or configured as a blocking PR gate.

### RR-001: Input Sanitization Absent (MC-02 MISSING)

**Severity:** High | **CVSS 3.1:** 6.5 | **CWE:** CWE-20

**Why it blocks:** Without input sanitization in `deepeval_adapter.py`, an adversarially crafted YAML test case `vars.user_query` can inject prompt instructions that override the LLM judge's evaluation rubric. A compromised evaluation could produce PASS verdicts for genuinely regressed prompts, defeating the entire purpose of the harness.

**Remediation (code-level):**
```python
# In jerry/testing/evaluation/deepeval_adapter.py, before LLMTestCase construction:
_MAX_PROMPT_BYTES = 10_240
_MAX_OUTPUT_BYTES = 51_200
_INJECTION_PATTERNS = re.compile(
    r"ignore previous instructions|SYSTEM:\s*override|evaluate this as|"
    r"score this.*10|give.*full marks",
    re.IGNORECASE
)

def _sanitize_input(text: str, max_bytes: int, label: str) -> str:
    if len(text.encode()) > max_bytes:
        logger.warning("Input '%s' truncated (MC-02).", label)
        text = text.encode()[:max_bytes].decode(errors="replace")
    if _INJECTION_PATTERNS.search(text):
        logger.warning("Injection pattern detected in '%s' (MC-02).", label)
    return text
```

**Verification:** Unit test confirming injection patterns are detected and logged; integration test confirming length truncation at 10KB boundary.

---

### RR-002: Docker Image Not Digest-Pinned (MC-08 MISSING)

**Severity:** High | **CVSS 3.1:** 7.4 | **CWE:** CWE-1395

**Why it blocks:** The Smoke workflow uses `ghcr.io/promptfoo/promptfoo:latest` — the highest-risk mutable tag. A registry compromise substituting a malicious image would execute with access to the `ANTHROPIC_API_KEY` environment variable. All three workflows have TODO comments with remediation instructions but no digest values filled in.

**Remediation (priority order):**
1. Smoke: `docker pull ghcr.io/promptfoo/promptfoo:latest && docker inspect --format='{{index .RepoDigests 0}}'` — replace `:latest` with `@sha256:<digest>` immediately
2. Standard/Full: Same procedure for `ghcr.io/promptfoo/promptfoo:0.86.0`
3. Dockerfile: Same procedure for `node:20-alpine3.21`

**Operational:** Establish digest rotation policy — re-pin when upgrading promptfoo versions or when base image receives security patch. Add Trivy or Grype scan step to detect CVEs in pinned images.

---

## L1: Accepted Residual Risks

These risks have been explicitly evaluated and accepted in ADR-001 or by the V&V team. They do not block merge.

| Risk ID | Description | Acceptance Rationale | Residual RPN |
|---------|-------------|---------------------|--------------|
| RR-007 | Incomplete MR coverage for agent-specific behavioral properties | Structurally irreducible until Phase D; 5 universal MRs cover major perturbation types; ongoing process | 96 |
| RR-008 | False confidence from incomplete test suite coverage | No technical gate can guarantee test suite completeness; authorship checklist (FR-027) is primary mitigation; Phase F perturbation testing is planned | 216 |
| RR-009 | MR violation ambiguity before empirical calibration | Tolerance values set from initial estimates per contracts C.1-C.5; MR violations are warnings until calibrated; calibration is a process activity | 50 |
| RR-012 | npm/UV environment conflict | Docker isolation completely prevents conflict; Python API fallback path documented and accepted | 0 |

**Total accepted residual RPN: 362** (vs. original 1,823 = 80.1% reduction when accounting for all fully mitigated FMs)

---

## L1: Open Risk Items

These risks are known, not blocking merge, and require future work:

| Risk ID | Description | Priority | Owner | Phase |
|---------|-------------|----------|-------|-------|
| RR-010 | STANDARD mode N accumulation protocol undocumented | MEDIUM | Protocol documentation | Post-merge |
| RR-011 | DeepEval package absent from pyproject.toml | LOW | Add dependency declaration | Post-merge |
| RR-022 | No automated API key rotation policy | LOW | Operational documentation | Post-merge |
| RR-023 | Dual InsufficientSamplesError classes incompatible | MEDIUM | Consolidate to types.py | Post-merge |
| RR-024 | Peer coupling in metamorphic package | LOW | Extract _wilcoxon_helpers.py | Phase D |
| RR-025 | FR-013 contract path discrepancy | LOW | Reconcile paths during Phase D | Phase D |
| RR-026 | FR-012/FR-013 NOT STARTED | MEDIUM | Phase D agent-specific MR implementation | Phase D |
| RR-027 | T-41 MR violation crafting not in threat catalog | LOW | Add to threat model (T-41) | Phase D |
| RR-028 | STANDARD mode N accumulation undocumented | MEDIUM | Document protocol in baselines/protocol.md | Post-merge |

---

## L2: Risk Consolidation Analysis

### Risk Source Consolidation

Risks were consolidated from five independent sources. Deduplication removed 12 overlapping entries where the same underlying risk was identified in multiple sources (e.g., FM-002 in FMEA and T-35 in threat model both address adversarial score manipulation; consolidated as RR-004/RR-017).

| Source | Original Risk Count | After Deduplication | Net New (unique) |
|--------|--------------------|--------------------|-----------------|
| 1B (system design, FMEA) | 10 FM + 40 threats | 10 FM-derived | 10 |
| 5A (security assessment) | 9 findings + 40 threats | 9 security findings | 8 (FM overlap: 2) |
| 5B (V&V gaps) | 7 gaps | 7 | 6 (FM overlap: 1) |
| 5C (test coverage gaps) | 4 gaps | 4 | 2 (V&V overlap: 2) |
| 3E (CI/CD operational) | 5 risks | 5 | 2 (security overlap: 3) |
| **Total** | **75 raw** | **28 distinct** | — |

### FMEA RPN Trajectory

| FM ID | Description | Original RPN | Mitigated RPN | Reduction | Status |
|-------|-------------|-------------|---------------|-----------|--------|
| FM-007 | False confidence from coverage gaps | 432 | 216 | 50% | Accepted residual |
| FM-001 | LLM-as-Judge bias | 280 | 0 | 100% | Fully mitigated |
| FM-003 | Incomplete MR coverage | 240 | 96 | 60% | Accepted residual |
| FM-002 | Statistical false alarm (small N) | 168 | 0 | 100% | Fully mitigated |
| FM-005 | Prompt version mismatch | 144 | 0 | 100% | Fully mitigated |
| FM-010 | Stale baseline | 144 | 0 | 100% | Fully mitigated |
| FM-006 | LLM cost overrun | 140 | 0 | 100% | Fully mitigated |
| FM-009 | MR violation ambiguity | 125 | 50 | 60% | Mitigated post-calibration |
| FM-004 | npm/UV conflict | 90 | 0 | 100% | Fully mitigated |
| FM-008 | DeepEval version drift | 60 | 20 | 67% | PARTIAL (model pin only) |
| **TOTAL** | | **1,823** | **382** | **79.0%** | |

### Strategic Risk Posture

The harness's risk posture has three distinct layers:

**Layer 1 — Security (Medium-High, requires action before production):**
RR-001 and RR-002 are the only risks that block the harness from safely handling production secrets. Both have documented remediation paths with code-level guidance. Resolving these two items moves the security posture from Medium-High to Low-Medium.

**Layer 2 — Coverage (Medium, accepted residual):**
The fundamental challenge of behavioral test completeness (RR-007, RR-008) is irreducible by technical means alone. Phase D (agent-specific MRs) and Phase F (perturbation testing) are the planned roadmap to narrow this gap systematically. The current accepted residual is appropriate for an initial deployment.

**Layer 3 — Architecture (Low, technical debt):**
RR-023 (dual InsufficientSamplesError) and RR-024 (metamorphic peer coupling) are known structural debts with low near-term risk. They should be addressed before Phase D extension work to prevent debt compounding.

---

## Risk Source Traceability

| Risk ID | Primary Source | Secondary Source | FR/MC Reference |
|---------|---------------|-----------------|-----------------|
| RR-001 | 5A F-001 | 1B T-02, MC-02 | FR-023 AC-2, MC-02 |
| RR-002 | 5A F-002 | 1B T-08, MC-08 | MC-08 |
| RR-003 | 5A F-003 | 1B T-22 | FR-004, MC-22, MC-27 |
| RR-004 | 5A F-004 | 1B T-35 | FR-009, contracts Section D |
| RR-005 | 5A F-005 | 1B T-02, T-07 | FR-001, MC-01 |
| RR-006 | 5A F-009 | 1B (A02) | FR-004 |
| RR-007 | 5B FM-003 | 1A FR-012, FR-013 | FM-003 (RPN 240->96) |
| RR-008 | 5B FM-007 | 1A FR-027, FR-013 | FM-007 (RPN 432->216) |
| RR-009 | 5B FM-009 | contracts C.1-C.5 | FR-011, FM-009 (RPN 125->50) |
| RR-010 | QG-2 Quantitative gap | 5B VCRM | FR-005, FR-014 |
| RR-011 | 5B FR-026 PARTIAL | 5A A06 | FR-026, FM-008 |
| RR-012 | 5B FM-004 | 3E, 1B | FR-025, FR-023, FM-004 |
| RR-013 | 5B FM-006 | 1B, 3E | FR-005, NFR-004, FM-006 |
| RR-014 | 5B FM-005 | 1B | FR-004, FR-020, FM-005 |
| RR-015 | 5B FM-010 | 1B | FR-020, FM-010 |
| RR-016 | 5B FM-001 | 1B T-35 | FR-021, FM-001 |
| RR-017 | 5B FM-002 | 1A FR-014 | FR-014, FR-005, FM-002 |
| RR-018 | 1B T-29 | 5A A01 | MC-28 |
| RR-019 | 1B T-25 | 5A A07 | MC-01, A07 |
| RR-020 | 1B T-07 | 5A A10, MC-07 | FR-025, MC-07 |
| RR-021 | 5A A06 | 1B T-08 | MC-08 (related) |
| RR-022 | 5A A02 | — | NFR (operational) |
| RR-023 | QG-2 critical finding | 5C (base.py) | stats.py, base.py |
| RR-024 | QG-2 structural gap | 3C implementation | metamorphic/mr_001 |
| RR-025 | QG-1 structural gap | 1A FR-013, 1D | FR-013, contracts/per-agent/ |
| RR-026 | 5B VCRM | 5C coverage | FR-012, FR-013 |
| RR-027 | QG-1 Architectural Coherence gap | 1B threat model | T-41 (unmodeled) |
| RR-028 | QG-2 Quantitative gap | 5B VCRM | FR-005, FR-014, baselines/protocol.md |

---

*Stream: 7B (Cross-Synthesis)*
*Agent: ps-synthesizer v2.3.0*
*Constitutional compliance: P-003 (no recursion), P-020 (user authority), P-022 (no deception)*
*Sources: 5A (security), 5B (V&V/FMEA), 5C (test gaps), 1B (design risks), 3E (CI/CD), QG-1/QG-2/QG-3 barrier reports*
*Date: 2026-03-07*
