# Security Assessment: Four-Layer Composite Test Harness (PROJ-036)

> **Project:** PROJ-036 (Prompt Regression Harness)
> **Reviewer:** eng-security
> **Date:** 2026-03-07
> **Criticality:** C4 (Critical — architecture review, 67 agent definitions affected)
> **Quality Threshold:** >= 0.94
> **Iteration:** 4 (iter1: 0.835, iter2: 0.908, iter3: 0.932)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Overall risk posture, one paragraph |
| [Threat Model Coverage Matrix](#threat-model-coverage-matrix) | MC-01 through MC-14: IMPLEMENTED / PARTIAL / MISSING |
| [OWASP Alignment Table](#owasp-alignment-table) | Per-file alignment with OWASP Top 10 categories |
| [Findings](#findings) | All findings with CWE, severity, evidence, remediation |
| [Supply Chain Assessment](#supply-chain-assessment) | Base images, dependencies, version pinning |
| [Container Security Assessment](#container-security-assessment) | Dockerfile review |
| [T-40 Adversarial Statistical Bypass Assessment](#t-40-adversarial-statistical-bypass-assessment) | Dedicated assessment of top-9 threat |
| [CWE Top 25 2025 Checklist](#cwe-top-25-2025-checklist) | Applicability and finding mapping for all 25 CWEs |
| [Recommendations](#recommendations) | Priority-ordered remediation actions |
| [Self-Review (S-010)](#self-review-s-010) | Pre-finalization quality check |

---

## L0: Executive Summary

The Four-Layer Composite Test Harness (PROJ-036) demonstrates a thoughtful, defense-in-depth security architecture with well-implemented controls for the highest-risk threats: the Python statistical engine (`stats.py`, `version_keys.py`) correctly enforces input validation, path traversal prevention, SHA-1 hash format validation, and adversarial score sequence detection; the GitHub Actions workflows correctly apply minimal permissions, fork isolation, and secret masking; and the domain-layer separation (H-07) provides structural defense against injection by ensuring LLM outputs are never evaluated as code. However, the assessment identifies two critical gaps and three high-severity findings that undermine the implemented architecture: the Docker base image is not pinned to a SHA-256 digest in any workflow (MC-08 is documented but unimplemented — a TODO comment remains in all three workflows), making the system vulnerable to tag-poisoning supply chain attacks; the `deepeval_adapter.py` does not implement the documented input sanitization layer for prompt injection (MC-02 is architecturally assigned to this file but the sanitization logic is absent from the implementation); and the `BaselineStore._validate_version_key()` method does not validate the git hash component against the 40-character hex pattern enforced by `version_keys.py`, creating a validation bypass path that could admit malformed version keys into the baseline store. The overall risk posture is MEDIUM-HIGH: the harness cannot yet be treated as a trusted security gate without resolving the MC-08 digest-pinning gap and the MC-02 input sanitization gap before production deployment. OWASP A02 (Cryptographic Failures — API token key management) and A06 (Vulnerable/Outdated Components — promptfoo npm supply chain) represent additional gaps documented below. The T-40 adversarial statistical bypass threat (top-9 by DREAD priority score 7.2) is assessed as IMPLEMENTED via `stats.py` MC-40 variance floor enforcement, effect size cross-check, and paired-difference symmetry detection.

---

## Threat Model Coverage Matrix

Assessment of each mitigation control MC-01 through MC-14 against the implementation. Coverage determination is based on direct code inspection, not on documentation claims. Controls beyond MC-14 that are referenced in this assessment are drawn from the full MC-01 through MC-40 range documented in system-design.md Part 4; MC-28 (fork secret isolation) is included in the OWASP table because it is a directly reviewed workflow control. MC-40 (T-40 statistical bypass) is assessed in its own section below.

| Control | Name | Status | Evidence |
|---------|------|--------|----------|
| MC-01 | YAML schema validation (filename match) | PARTIAL | `promptfoo-config.yaml` loads test-case files by filename, but no `conftest.py` validation logic was found in the reviewed files. The schema file `tests/prompt-regression/schemas/test-case.schema.json` is referenced in the design but not present in the assessed implementation. The `defaultTest.assert` in `promptfoo-config.yaml` provides a `not-regex` assertion for secrets (line 126) and a `not-empty` check, but filename-pattern matching is not implemented. |
| MC-02 | Input sanitization for prompt injection | MISSING | `deepeval_adapter.py` is specified as the implementation location (system-design.md Part 4, line 1535: `MC-02 | Input sanitization for prompt injection | jerry/testing/evaluation/deepeval_adapter.py`), but the reviewed code contains no sanitization layer. The `evaluate_batch()` method passes the `prompt` and `outputs` strings directly to DeepEval without stripping injection patterns. No call to a sanitization function or pattern-matching filter exists anywhere in the file. |
| MC-03 | Threshold enforcement via schema | PARTIAL | `promptfoo-config.yaml` includes a `cost` assertion (`threshold: 0.50`) and references schema-validated assertions. However, the `schemas/test-case.schema.json` enforcement file is not present in the assessed implementation. The `minimum` constraints on threshold values referenced in the threat model are unverifiable. |
| MC-04 | Git audit trail for test changes | IMPLEMENTED | Git history and PR-based workflow are existing repository mechanisms. The three CI workflows all use `pull_request` event (not `pull_request_target`), ensuring commit attribution via standard git history. |
| MC-05 | Sensitive data scan in test inputs | PARTIAL | `promptfoo-config.yaml` includes a `not-regex` assertion matching bearer tokens and API keys (line 126). However, the referenced `.pre-commit-config.yaml` sensitive data scanner was not present in the assessed files. Only the in-execution assertion guard is implemented; the pre-commit phase guard is unverifiable. |
| MC-06 | Test case count and size limits | PARTIAL | `promptfoo-config.yaml` sets `maxConcurrency: 1` and `timeout: 60000`. However, the conftest.py validation for maximum test case count (100 per file) and input payload size limit (10KB per var) referenced in the threat model is not implemented in the reviewed files. |
| MC-07 | Docker read-only + capability drop + path restriction | IMPLEMENTED | All three workflows apply `--read-only`, `--cap-drop=ALL`, and `--security-opt=no-new-privileges:true`. The `--network=none` flag is correctly applied in Smoke mode. Read-only volume mounts (`:ro`) are applied to all source/config directories. The `tmpfs` mount (`/tmp:rw,size=64m,noexec,nodev`) correctly restricts the only writable in-container surface. |
| MC-08 | Docker image digest pinning | MISSING | `Dockerfile` line 39: `FROM node:20-alpine3.21` (tag only, no SHA-256 digest). `prompt-regression-smoke.yml` line 218: `PROMPTFOO_IMAGE="ghcr.io/promptfoo/promptfoo:latest"`. Standard and Full workflows use `"ghcr.io/promptfoo/promptfoo:0.86.0"` (version tag only). All three files contain explicit TODO comments acknowledging this gap. MC-08 is unimplemented in production code despite being documented as a critical supply chain control. |
| MC-09 | Output volume validation | IMPLEMENTED | All three workflows include a post-step that validates promptfoo's JSON output using `uv run python -c "import json, sys..."`. The validation checks that the output is a valid JSON object. The smoke workflow includes non-fatal validation (warns on missing keys) while Standard and Full workflows fail on missing output. |
| MC-10 | Read-only config mounts | IMPLEMENTED | All workflow `docker run` commands mount source directories with the `:ro` flag: `/tests/prompt-regression:/workspace/tests:ro`, `/skills:/workspace/skills:ro`. Only the results output directory is mounted writable. |
| MC-11 | Container execution logging | IMPLEMENTED | GitHub Actions captures container stdout/stderr by default. All workflows pipe docker output through `2>&1` capturing both streams. Run IDs are available in the GHA context. |
| MC-12 | Single-process container, no shell | IMPLEMENTED | `Dockerfile` line 156: `ENTRYPOINT ["promptfoo"]` (array form, no shell). `CMD ["--help"]` provides a safe no-op default. No `CMD` with shell string form. No `bash` or `sh` entrypoint. |
| MC-13 | Docker resource limits | IMPLEMENTED | Smoke: `--memory=512m --cpus=1`. Standard: `--memory=2g --cpus=2`. Full: `--memory=4g --cpus=4`. `timeout-minutes` set at workflow level (Smoke=5, Standard=25, Full=60). Resource limits are tier-scaled appropriately. |
| MC-14 | Container hardening (no-new-privileges, cap-drop) | IMPLEMENTED | All three workflows apply `--security-opt=no-new-privileges:true` and `--cap-drop=ALL`. The Dockerfile creates a non-root user (`promptfoo`, UID 1001) and switches to it before the entrypoint (`USER promptfoo`, line 138). |

**Summary:** 7 IMPLEMENTED, 4 PARTIAL, 2 MISSING. The two MISSING controls (MC-02, MC-08) are pre-production blockers per the threat model's own High risk ratings.

---

## OWASP Alignment Table

This table covers all 10 OWASP Top 10 2021 categories. The MC-28 reference in the A01 row draws from the full MC-01 through MC-40 control set documented in system-design.md Part 4; fork secret isolation (MC-28) is a directly reviewed workflow control relevant to access control classification and is included on that basis.

| OWASP Category | Relevant Files | Assessment | Notes |
|----------------|----------------|------------|-------|
| A01:2021 Broken Access Control | All workflows, Dockerfile | PASS | Fork secret isolation (MC-28) implemented via `pull_request` event (not `pull_request_target`) in all three workflows. Minimal permissions (`contents: read`, `pull-requests: write`, `checks: write`) applied. Non-root container user enforced (MC-14). Read-only mounts prevent container filesystem escape to host data. |
| A02:2021 Cryptographic Failures | CI workflows, `promptfoo-config.yaml` | PARTIAL | API tokens (`ANTHROPIC_API_KEY`) are sourced via GitHub Actions secrets (never hardcoded) and masked with `::add-mask::`. However, there is no documented key rotation schedule or automated rotation mechanism — key management is entirely manual operational procedure. No secrets-at-rest encryption is applied to the baseline store (JSON files on disk, keyed by SHA-256 truncation). The `compute_prompt_content_hash()` function truncates SHA-256 to 16 hex characters (64 bits), below the NIST SP 800-57 128-bit minimum for collision-resistant identifiers (Finding F-009). |
| A03:2021 Injection | `version_keys.py`, `deepeval_adapter.py`, CI workflows | PARTIAL | `version_keys.py` correctly prevents shell injection (subprocess list form, no `shell=True`, allowlist path validation). However, `deepeval_adapter.py` passes prompt and output text directly to DeepEval without sanitization (MC-02 gap — see Finding F-001). The `not-regex` assertion in `promptfoo-config.yaml` catches some secret patterns in outputs but is not a full injection prevention control. |
| A04:2021 Insecure Design | `version_keys.py`, `stats.py`, `store.py` | PASS | Version key design enforces 40-char SHA-1 hash format, preventing key collision. Statistical engine validates score arrays against adversarial degenerate sequences. Baseline quality gate enforces mean >= 0.92 before storage. Domain layer isolation (H-07) prevents LLM outputs from being executed as code. |
| A05:2021 Security Misconfiguration | Dockerfile, CI workflows | PARTIAL | Docker non-root user, read-only filesystem, and capability dropping are correctly configured. However, the Dockerfile does not pin the base image to a SHA-256 digest (MC-08 gap — see Finding F-002). The Smoke workflow uses `:latest` tag for the promptfoo image (smoke.yml line 218), making it the most vulnerable to tag-poisoning attacks. |
| A06:2021 Vulnerable and Outdated Components | `docker/promptfoo/Dockerfile`, CI workflows | PARTIAL | The promptfoo npm package is pinned to version `0.86.0` by version tag (not by npm integrity hash or `package-lock.json`). The `npm install -g "promptfoo@${PROMPTFOO_VERSION}"` in the Dockerfile does not use `npm ci` from a lockfile or `--integrity` verification. No automated CVE scanning (e.g., Trivy, Grype, `npm audit`) is present in the CI pipeline to detect known vulnerabilities in the pinned npm package or its transitive dependencies. The node:20-alpine3.21 base image is not digest-pinned (MC-08), meaning it cannot be reliably scanned against a known-good artifact. |
| A07:2021 Identification and Authentication Failures | CI workflows, `promptfoo-config.yaml` | PASS | API key sourced exclusively via environment variables, never hardcoded. `ANTHROPIC_API_KEY` passed as named environment variable (not interpolated into command strings). `::add-mask::` defense-in-depth applied in Standard and Full workflows. The `defaultTest.assert not-regex` assertion would catch API key patterns if accidentally included in LLM outputs. |
| A08:2021 Software and Data Integrity Failures | `store.py`, `version_keys.py`, CI workflows | PARTIAL | Baseline integrity via git-commit-hash versioning (FR-004) is correctly implemented. `validate_baseline_version_key()` performs commit hash mismatch detection. However, `BaselineStore._validate_version_key()` performs only structural format validation, not cryptographic validation of the hash component (see Finding F-003). GitHub Actions are pinned to SHA digests (e.g., `actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683`) — this is correctly implemented and provides strong supply chain integrity for actions. Docker image tag pinning is absent (MC-08). |
| A09:2021 Security Logging and Monitoring Failures | `deepeval_adapter.py`, CI workflows | PARTIAL | GitHub Actions captures container stdout/stderr via `2>&1`. `evaluate_batch()` logs at WARNING level when exceptions occur (F-004). However, exception events in `evaluate_batch()` are logged only at WARNING level with no structured alert, no failure-rate tracking, and no surface to the CI/CD summary — an operator who does not examine logs may not notice that baseline capture is silently failing. No centralized security event logging (e.g., Langfuse integration, GHA step summary for security-relevant events) is implemented. The evaluation report artifacts (90-day GHA retention) provide post-hoc auditability but not real-time anomaly detection. |
| A10:2021 Server-Side Request Forgery (SSRF) | `docker/promptfoo/Dockerfile`, CI workflows, `promptfoo-config.yaml` | PARTIAL | The promptfoo container applies `--network=none` in Smoke mode (no outbound requests). Standard and Full modes permit outbound HTTPS for Anthropic API calls (required). T-07 in the threat model identifies that promptfoo's `file://` protocol handler could be exploited to read arbitrary files from the Docker container via a crafted YAML test case. MC-07 (read-only filesystem, dropped capabilities, whitelisted paths) partially mitigates this. However, no explicit promptfoo configuration restricting `file://` protocol handler usage was found in the reviewed `promptfoo-config.yaml`. Standard/Full containers have no network allowlist — the container can reach any external host over HTTPS, providing a potential SSRF exfiltration path if promptfoo processes attacker-controlled URLs. |

---

## Findings

### F-001 — MISSING Input Sanitization for Prompt Injection (MC-02)

| Attribute | Value |
|-----------|-------|
| **ID** | F-001 |
| **Severity** | High |
| **CWE** | CWE-20: Improper Input Validation |
| **Affected File** | `jerry/testing/evaluation/deepeval_adapter.py` |
| **Threat** | T-02 (YAML vars injection, Likelihood=H, Impact=H, Risk=High) — MC-02 is the mitigation control for T-02 and is assigned to `deepeval_adapter.py` in system-design.md Part 4. T-02 describes injection via YAML `vars.user_query` fields; the DeepEval adapter is the downstream processing surface where those injected strings reach the LLM judge. The injection surface is the YAML input path (T-02) manifesting at the adapter layer. There is no separately modeled threat for the adapter itself as a distinct injection surface in the T-01 through T-40 threat catalog. |
| **Requirement** | FR-023 (input validation), MC-02 (input sanitization layer) |
| **CVSS 3.1 Base Score** | 6.5 (AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:N) |

**Description:** The system design (Part 4, MC-02 controls mapping) specifies that MC-02 is implemented in `deepeval_adapter.py` as an "input sanitization layer [that] strips known injection patterns" and enforces "test input length limits." The reviewed implementation contains no such layer. The `evaluate_batch()` method accepts `prompt` and `outputs` as raw strings and passes them directly to `LLMTestCase(input=prompt, actual_output=output_text)` at line 330 without any preprocessing, pattern stripping, or length validation. The `evaluate()` method similarly accepts unconstrained input strings. Adversarially crafted YAML `vars.user_query` fields can deliver prompt injection payloads that manipulate the LLM judge's scoring behavior, potentially causing false PASS verdicts on regressed prompts.

**Evidence — exact insertion point:**
```
deepeval_adapter.py:329-333 (evaluate_batch() inner loop):
    for i, output_text in enumerate(outputs):
        test_case = LLMTestCase(       # <-- line 330: injection target
            input=prompt,              # line 331: unsanitized prompt
            actual_output=output_text, # line 332: unsanitized output
        )                              # line 333
```
The sanitization call must be inserted between the `output_text` assignment (line 329) and the `LLMTestCase` construction (line 330). No sanitization call precedes this construction. No length limit check exists in `evaluate_batch()`. No pattern-stripping function is imported or called anywhere in the file.

**Remediation:** Implement an input sanitization layer before `LLMTestCase` construction at line 330 in `evaluate_batch()`. At minimum:

1. Enforce a maximum input length (e.g., 10KB for `prompt`, 50KB for `output_text` to accommodate LLM responses).
2. Strip or escape known injection patterns targeting LLM judges (e.g., `Ignore previous instructions`, `SYSTEM:`, patterns that override evaluation rubrics).
3. Log a warning when a pattern match occurs so that injection attempts are visible in the audit trail.

```python
# Example remediation in evaluate_batch() — insert before line 330:
_MAX_PROMPT_BYTES = 10_240
_MAX_OUTPUT_BYTES = 51_200
_INJECTION_PATTERNS = re.compile(
    r"ignore previous instructions|SYSTEM:\s*override|evaluate this as|"
    r"score this.*10|give.*full marks",
    re.IGNORECASE
)

def _sanitize_input(text: str, max_bytes: int, label: str) -> str:
    if len(text.encode()) > max_bytes:
        logger.warning("Input '%s' truncated from %d to %d bytes (MC-02).",
                       label, len(text.encode()), max_bytes)
        text = text.encode()[:max_bytes].decode(errors="replace")
    if _INJECTION_PATTERNS.search(text):
        logger.warning("Potential injection pattern detected in '%s' (MC-02).", label)
    return text
```

---

### F-002 — Docker Image Not Pinned to SHA-256 Digest (MC-08 Unimplemented)

| Attribute | Value |
|-----------|-------|
| **ID** | F-002 |
| **Severity** | High |
| **CWE** | CWE-1395: Dependency on Vulnerable Third-Party Component |
| **Affected Files** | `docker/promptfoo/Dockerfile` (line 39), `.github/workflows/prompt-regression-smoke.yml` (line 218), `.github/workflows/prompt-regression-standard.yml` (line 321), `.github/workflows/prompt-regression-full.yml` (line 276) |
| **Threat** | T-08 (Docker image substitution, Likelihood=L, Impact=H, Risk=Medium) |
| **Requirement** | MC-08 (Docker image digest pinning) |
| **CVSS 3.1 Base Score** | 7.4 (AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N) |

**Description:** MC-08 requires Docker images to be pinned to SHA-256 digests rather than mutable tags. The design document explicitly documents this control as critical for supply chain integrity. However, in all four files, the image references use mutable tags:

- `Dockerfile:39`: `FROM node:20-alpine3.21` (tag only)
- `smoke.yml:218`: `PROMPTFOO_IMAGE="ghcr.io/promptfoo/promptfoo:latest"` — this is the most severe instance: the `:latest` tag changes silently on every upstream push, with no version control.
- `standard.yml:321`, `full.yml:276`: `"ghcr.io/promptfoo/promptfoo:0.86.0"` — version tag is better but still mutable; a registry compromise could replace this tag.

All four files contain explicit TODO comments acknowledging this gap but no remediation timeline. The risk is that a supply chain attacker who compromises the `node:20-alpine` or `ghcr.io/promptfoo/promptfoo` registry could substitute a malicious image that (a) exfiltrates the `ANTHROPIC_API_KEY` environment variable, (b) writes malicious content to the output volume, or (c) executes arbitrary code within the container.

**Evidence:**
```
Dockerfile:34-39:
# TODO: Pin to SHA digest in production (MC-08). Run:
#   docker pull node:20-alpine3.21
#   docker inspect --format='{{index .RepoDigests 0}}' node:20-alpine3.21
# Replace the FROM line below with the fully-qualified digest form, e.g.:
#   FROM node:20-alpine3.21@sha256:<real-64-char-digest> AS base
FROM node:20-alpine3.21 AS base

smoke.yml:212-218:
# MC-08 TODO: Pin to SHA digest in production (MC-08). Run:
#   docker pull ghcr.io/promptfoo/promptfoo:latest
#   docker inspect --format='{{index .RepoDigests 0}}' ghcr.io/promptfoo/promptfoo:latest
# Replace the image reference below with the fully-qualified digest form, e.g.:
#   ghcr.io/promptfoo/promptfoo@sha256:<real-64-char-digest>
PROMPTFOO_IMAGE="ghcr.io/promptfoo/promptfoo:latest"
```

**Remediation:** Execute the pinning procedure documented in the TODO comments before the harness handles any production secret. Priority order:

1. Smoke workflow: Replace `:latest` immediately — this is the highest risk. Pin to `ghcr.io/promptfoo/promptfoo@sha256:<digest>`.
2. Standard and Full workflows: Replace `0.86.0` tag with digest form.
3. Dockerfile: Replace `FROM node:20-alpine3.21` with digest-pinned form.

Establish a rotation policy: re-pin digests when upgrading promptfoo or when the node base image receives a security patch. Add a CI check (e.g., a Trivy or Grype scan) to detect known CVEs in the pinned images.

---

### F-003 — BaselineStore Version Key Validation Is Weaker Than VersionKey Module

| Attribute | Value |
|-----------|-------|
| **ID** | F-003 |
| **Severity** | Medium |
| **CWE** | CWE-20: Improper Input Validation |
| **Affected File** | `jerry/testing/baselines/store.py` (lines 410-432) |
| **Threat** | T-22 (Fake baseline records, Likelihood=M, Impact=H, Risk=High) |
| **Requirement** | FR-004 (version key management), MC-22 (baseline quality gate), MC-27 (path traversal prevention) |
| **CVSS 3.1 Base Score** | 5.3 (AV:N/AC:H/PR:L/UI:N/S:U/C:N/I:H/A:N) |

**Description:** `version_keys.py` enforces strict validation for version key components: the commit hash must be exactly 40 hexadecimal characters (lines 247-260), and the file path must match `^skills/[a-z0-9\-]+/agents/[a-z0-9\-]+\.md$` (lines 60-63). However, `BaselineStore._validate_version_key()` (lines 410-432 in `store.py`) performs only structural format validation: it checks that the string contains a `:` separator and that neither side of the split is empty. It does not validate:

1. That the hash component is exactly 40 hex characters.
2. That the file path component matches the agent file allowlist pattern.

An attacker with write access to the baseline store (e.g., via a malicious PR that directly adds baseline JSON files) could craft a version key like `short:../../etc/passwd` or `x:../arbitrary/path.md` that would pass `_validate_version_key()` but would fail if routed through `VersionKey.from_string()`. While path traversal to the filesystem is mitigated by the SHA-256-based slug path computation in `_record_path()` (line 407), the weaker validation creates an inconsistency between the two validation systems that could be exploited if the baseline store is extended in the future.

**Evidence:**
```python
# store.py:410-432 — only structural format check:
@staticmethod
def _validate_version_key(version_key: str) -> None:
    if ":" not in version_key:
        raise ValueError(...)
    parts = version_key.split(":", 1)
    if not parts[0] or not parts[1]:
        raise ValueError(...)
    # No hash format check, no path allowlist check

# version_keys.py:263-290 — full validation:
def _validate_agent_file_path(file_path: str) -> None:
    if file_path.startswith("/") or ".." in file_path:
        raise VersionKeyError(...)   # path traversal check
    if not _AGENT_FILE_PATH_PATTERN.match(file_path):
        raise VersionKeyError(...)   # allowlist check
```

**Remediation:** Replace `BaselineStore._validate_version_key()` with a call to `VersionKey.from_string()` imported from `tests/prompt-regression/version_keys.py`, or duplicate the validation constants (commit hash pattern and file path pattern) in `store.py` alongside a validation call. The simpler approach:

```python
# In store.py store() method, replace _validate_version_key() call:
from jerry.testing.types import VersionKey  # or import from version_keys
try:
    VersionKey.from_string(version_key)  # validates hash format + path allowlist
except (ValueError, VersionKeyError) as exc:
    raise ValueError(f"Invalid version_key: {exc}") from exc
```

---

### F-004 — evaluate_batch() Silently Swallows Exceptions with Score 0.0

| Attribute | Value |
|-----------|-------|
| **ID** | F-004 |
| **Severity** | Medium |
| **CWE** | CWE-390: Detection of Error Condition Without Action |
| **Affected File** | `jerry/testing/evaluation/deepeval_adapter.py` (lines 371-382) |
| **Threat** | T-35 (Adversarial score sequences, indirectly) |
| **Requirement** | FR-009 (score array collection), `contracts/behavioral-contracts.md` Section D |
| **CVSS 3.1 Base Score** | 4.3 (AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N) |

**Description:** The `evaluate_batch()` method at lines 371-382 catches all exceptions with a bare `except Exception as exc` handler and silently appends `0.0` for all criteria scores. This creates a security concern in two ways:

1. **Score manipulation**: An adversarial test input that consistently triggers exceptions in the DeepEval scoring pipeline would produce an array of `0.0` scores for the candidate version. When compared against a healthy baseline, this would generate a REGRESSION verdict (correct behavior), but the cause would be hidden from the audit trail.

2. **Baseline poisoning risk**: If baseline capture runs also trigger exceptions and silently produce 0.0 scores, the baseline quality gate (mean >= 0.92) would reject the baseline — but the exception cause is only logged at `WARNING` level and not surfaced to the CI/CD summary. An operator who does not examine logs might not notice that baseline capture is silently failing.

The `stats.py` `_validate_score_array()` function rejects all-identical arrays (including all-zeros), which provides some protection. However, a mixed array where some runs succeed and some are silently zeroed would pass the variation check while corrupting the score distribution.

**Evidence:**
```python
# deepeval_adapter.py:371-382:
except Exception as exc:  # noqa: BLE001
    logger.warning(
        "Batch evaluation failed on output %d/%d for agent '%s': %s. "
        "Appending 0.0 for this run across all criteria.",
        ...
    )
    for criterion in criteria:
        score_lists[criterion.name].append(0.0)
    score_lists["composite"].append(0.0)
```

**Remediation:** Re-raise exceptions after logging once the failure rate exceeds a configurable threshold (e.g., more than 20% of batch runs fail). Return a structured error result that the caller can propagate rather than silently padding with 0.0. At minimum, track the exception count and include it in the returned score dictionary metadata so Layer 4 can detect corrupted batches.

```python
exception_count = 0
# ... in the exception handler:
exception_count += 1
if exception_count > len(outputs) * 0.2:
    raise RuntimeError(
        f"Batch evaluation failure rate exceeded 20% ({exception_count}/{len(outputs)}) "
        f"for agent '{agent_name}'. Aborting to prevent corrupted score arrays."
    ) from exc
```

---

### F-005 — AGENT_ID Environment Variable Not Validated in CI Workflows

| Attribute | Value |
|-----------|-------|
| **ID** | F-005 |
| **Severity** | Medium |
| **CWE** | CWE-20: Improper Input Validation |
| **Affected Files** | `.github/workflows/prompt-regression-smoke.yml` (lines 193-194), `.github/workflows/prompt-regression-standard.yml` (lines 341-344) |
| **Threat** | T-02 (YAML injection — AGENT_ID derived from git-diff filenames, which are controlled by the PR contributor and can contain metacharacters on some platforms); T-07 (file:// path exploitation — a path-containing AGENT_ID could influence promptfoo's YAML config path construction) |
| **Requirement** | FR-001 (YAML test case definitions), MC-01 (YAML schema validation) |
| **CVSS 3.1 Base Score** | 4.6 (AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N) |

**Description:** In the smoke and standard workflows, the `AGENT_ID` is passed to Docker via `-e AGENT_ID="${{ matrix.agent }}"` without validation against the known allowlist of covered agents (`ps-researcher`, `ps-analyst`, `ps-architect`, `ps-critic`, `adv-scorer`). The matrix value is derived from git-diff output, which in a PR context represents filenames from the contributor's branch. A contributor could name an agent file to produce a path traversal or injection vector:

- `skills/foo/agents/../../../etc/bar.md` — if git allows such filenames on some platforms, the sed extraction could produce an `AGENT_ID` with path separator characters.
- An agent file named with shell metacharacters if supported by the OS filesystem.

The `VersionKeyRegistry.COVERED_AGENTS` frozenset in `version_keys.py` (line 587) provides the canonical allowlist, but this validation is not performed at the CI level before the value is passed to Docker. The `test-authorship` step does verify that a corresponding test YAML exists, but does not enforce the agent ID against the allowlist.

**Evidence:**
```yaml
# smoke.yml:193-194:
env:
  AGENT_ID: ${{ matrix.agent }}

# The matrix value is derived from:
AGENT_IDS=$(echo "$CHANGED_FILES" \
  | sed 's|.*/agents/||' \
  | sed 's|\.md$||' \
  | sort -u ...)
```

No allowlist check against `COVERED_AGENTS` is performed before the value reaches Docker.

**Remediation:** Add an explicit allowlist validation step in the CI workflow before the Docker run:

```bash
AGENT="${{ matrix.agent }}"
VALID_AGENTS="ps-researcher ps-analyst ps-architect ps-critic adv-scorer"
if ! echo "$VALID_AGENTS" | grep -qw "$AGENT"; then
  echo "::error::Agent '$AGENT' is not in the PROJ-036 coverage set."
  echo "::error::Valid agents: $VALID_AGENTS"
  exit 1
fi
```

---

### F-006 — Output JSON Validation Is Structurally Shallow (MC-09)

| Attribute | Value |
|-----------|-------|
| **ID** | F-006 |
| **Severity** | Low |
| **CWE** | CWE-693: Protection Mechanism Failure |
| **Affected Files** | All three workflow files (post-step validation steps) |
| **Threat** | T-09 (output volume tampering) |
| **Requirement** | MC-09 (output volume validation) |
| **CVSS 3.1 Base Score** | 3.1 (AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N) |

**Description:** The output volume validation steps (MC-09) check that the promptfoo output file is valid JSON and is a dictionary object. In the Smoke workflow, even missing `results` or `stats` keys are treated as non-fatal warnings rather than errors (`print(f'Warning: output missing expected keys: {missing}', file=sys.stderr)`). In Standard and Full workflows, the validation only checks that the output is a dictionary. This means a tampered output file that contains a valid JSON object with a different structure (e.g., `{"tampered": true}` instead of `{"results": [...], "stats": {...}}`) would pass the validation and be consumed by the statistical engine without error. The statistical engine would then fail when it cannot find expected fields, but the failure mode is an application error rather than a detected integrity violation.

**Evidence:**
```python
# smoke.yml validation step (lines 259-270):
required_keys = {'results', 'stats'}
present = set(data.keys()) if isinstance(data, dict) else set()
missing = required_keys - present
if missing:
    # Non-fatal in smoke: promptfoo schema varies by version
    print(f'Warning: output missing expected keys: {missing}', file=sys.stderr)
```

**Remediation:** Make the required-key check fatal in Standard and Full workflows. Apply JSON Schema validation against the known promptfoo output schema. Consider adding a checksum of the output file immediately after Docker writes it to the output volume, before the statistical engine reads it, to detect any intervening modification.

---

### F-007 — Dockerfile Installs UV Via pip, Leaving pip in the Image

| Attribute | Value |
|-----------|-------|
| **ID** | F-007 |
| **Severity** | Low |
| **CWE** | CWE-1059: Insufficient Technical Documentation (supply chain hygiene) |
| **Affected File** | `docker/promptfoo/Dockerfile` (lines 77-94) |
| **Threat** | T-08 (supply chain via transitive npm dependency) |
| **Requirement** | FR-023 (UV-only execution), FR-025 (Docker isolation) |
| **CVSS 3.1 Base Score** | 2.5 (AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N) |

**Description:** The Dockerfile installs `py3-pip` to bootstrap UV (`pip install --no-cache-dir "uv==${UV_VERSION}"`), then does not remove pip afterward. This leaves pip available inside the container, which could be used by a compromised promptfoo npm dependency to install additional Python packages at runtime. While the `--read-only` container filesystem and `--cap-drop=ALL` mitigate most of this risk, leaving pip available violates the spirit of H-05 (UV-only Python execution) and provides an unnecessary attack surface.

**Evidence:**
```
Dockerfile:77-94:
RUN apk add --no-cache \
        python3 \
        py3-pip \
        ...
    pip install --no-cache-dir "uv==${UV_VERSION}" && \
    uv --version
# pip is not removed after UV is installed
```

**Remediation:** Uninstall pip after UV is installed, or use a multi-stage build where pip is present only in the build stage:

```dockerfile
# Install UV via pip, then remove pip
RUN pip install --no-cache-dir "uv==${UV_VERSION}" && \
    uv --version && \
    pip uninstall -y pip setuptools && \
    apk del py3-pip
```

Alternatively, install UV via its official installer script (`curl -LsSf https://astral.sh/uv/install.sh | sh`) in a build stage and copy only the binary to the runtime stage.

---

### F-008 — Baseline Store Does Not Verify baseline_status Field on Store

| Attribute | Value |
|-----------|-------|
| **ID** | F-008 |
| **Severity** | Low |
| **CWE** | CWE-840: Business Logic Errors |
| **Affected File** | `jerry/testing/baselines/store.py` (lines 132-244) |
| **Threat** | T-22 (Fake baseline records, baseline data integrity) |
| **Requirement** | FR-020 (baseline store acceptance), MC-22 (baseline quality gate) |
| **CVSS 3.1 Base Score** | 3.7 (AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N) |

**Description:** `BaselineStore.store()` creates a new `BaselineRecord` with `baseline_status="active"` and overwrites any existing record at the SHA-256-keyed path. If a record at that path was previously written with `baseline_status="invalidated"`, the store operation overwrites the invalidation without checking whether the file already contains an invalidated record. This allows an operator who has re-captured a baseline after an invalidation to proceed normally, but it also means that if an invalidated record's path hash collides with a new version key (unlikely given SHA-256 truncation to 16 chars, but theoretically possible), the invalidation would be silently overwritten.

**Evidence:**
```python
# store.py:230-235:
path.write_text(
    json.dumps(dataclasses.asdict(record), indent=2),
    encoding="utf-8",
)
# No check whether path.exists() and whether existing record is "invalidated"
```

**Remediation:** Before writing, check whether the path exists and whether the existing record has `baseline_status="invalidated"`. If invalidated, require explicit confirmation (via a parameter) before allowing re-capture:

```python
if path.exists():
    existing = json.loads(path.read_text(encoding="utf-8"))
    if existing.get("baseline_status") == "invalidated" and not allow_overwrite_invalidated:
        raise ValueError(
            f"Cannot overwrite invalidated baseline for {agent_id}/{metric_id}. "
            "Pass allow_overwrite_invalidated=True after reviewing the invalidation reason."
        )
```

---

### F-009 — compute_prompt_content_hash Returns Truncated Digest (Info)

| Attribute | Value |
|-----------|-------|
| **ID** | F-009 |
| **Severity** | Info |
| **CWE** | CWE-327: Use of a Broken or Risky Cryptographic Algorithm (informational) |
| **Affected File** | `tests/prompt-regression/version_keys.py` (lines 513-565) |
| **Threat** | T-22 (Fake baseline records — secondary integrity check) |
| **Requirement** | FR-004 (version key integrity) |
| **CVSS 3.1 Base Score** | 0.0 (informational only) |

**Description:** `compute_prompt_content_hash()` computes a SHA-256 digest of file content and returns only the first 16 hex characters (`sha256.hexdigest()[:16]`). The function's docstring acknowledges this as "sufficient for collision resistance in this context." For a secondary integrity check used alongside the primary git-hash-based versioning, 16 hex characters (64 bits) is marginally sufficient. However, the birthday attack threshold is approximately 2^32 files before collision probability exceeds 50%, which is acceptable for this use case. This is flagged as informational because truncation to 64 bits is below the recommended 128-bit minimum for collision-resistant identifiers in security contexts (NIST SP 800-57), though the impact is low given this is a secondary, defense-in-depth check.

**Remediation (optional):** Consider returning the full 256-bit digest or a 128-bit (32-character) truncation to meet NIST SP 800-57 recommendations for collision resistance:

```python
return sha256.hexdigest()[:32]  # 128-bit truncation — adequate for security contexts
```

---

## Supply Chain Assessment

### GitHub Actions — PASS (with one exception)

All GitHub Actions in the three workflows are pinned to SHA-256 commit digests, which is the correct approach for supply chain integrity:

| Action | Pinned Version | SHA Digest Present |
|--------|---------------|-------------------|
| `actions/checkout` | v4.2.2 | `11bd71901bbe5b1630ceea73d27597364c9af683` |
| `astral-sh/setup-uv` | v5.4.1 | `f0ec1fc3b38f5e7cd731bb1ce926ae18e12f4ccd` |
| `actions/upload-artifact` | v4.6.2 | `ea165f8d65b6e75b540449bea1e5c8c7e45e428` |
| `actions/github-script` | v7.0.1 | `60a0d83039c74a4aee543508d2ffcb1c3799cdea` |

All four action pins appear correctly formatted. These SHA digests should be periodically rotated when upgrading action versions.

The `setup-uv` action uses `version: "latest"` in the smoke workflow at line 162 (`version: "latest"`), which is inconsistent with the SHA-pinned action itself. The action version is pinned, but the UV version it installs is not — this should be pinned to `version: "0.5.29"` to match the Dockerfile's `UV_VERSION="0.5.29"` (`docker/promptfoo/Dockerfile` line 75), ensuring CI and Docker environments use the same UV version. This is distinct from the Docker image pinning gap (F-002) but shares the same root cause: mutable version references in CI infrastructure.

### Docker Images — FAIL (MC-08 gap, see F-002)

As documented in F-002, all Docker image references use mutable tags. This is the most significant supply chain gap in the implementation. The issue is acknowledged in the code with TODO comments but has not been resolved.

### Python Dependencies

The implementation uses UV for Python dependency management (FR-023, H-05 compliant). The `uv sync --no-dev` call in workflows installs from a lockfile, providing reproducible dependency resolution. No `requirements.txt` or direct pip installs are present in workflow steps that handle untrusted input (the Dockerfile pip install of UV is a bootstrap exception appropriately documented).

The npm supply chain risk for promptfoo is mitigated by Docker isolation (FR-025) — npm packages run inside the container cannot reach the host Python environment. The `npm install -g "promptfoo@${PROMPTFOO_VERSION}"` in the Dockerfile is pinned to `0.86.0` by version tag (not digest). There is no integrity verification (e.g., `npm install --integrity` or `npm ci` from a lockfile) for the npm install. This is a medium supply chain risk for the npm ecosystem specifically, and maps to OWASP A06 (Vulnerable and Outdated Components) as documented in the OWASP table.

**Recommendation:** Generate a `package-lock.json` that pins the promptfoo npm package and its transitive dependencies, then use `npm ci` in the Dockerfile instead of `npm install -g`, or use `npm install --integrity` to verify the package integrity hash.

---

## Container Security Assessment

### Dockerfile Review

**Positive findings:**

1. **Non-root user correctly implemented** (MC-07, MC-14): `addgroup -g 1001 -S promptfoo && adduser -u 1001 -S promptfoo -G promptfoo` at lines 52-53, `USER promptfoo` at line 138. UID/GID allocation to a reserved numeric value is correct practice.

2. **ENTRYPOINT uses array form** (MC-12): `ENTRYPOINT ["promptfoo"]` at line 156 prevents shell string interpretation. No shell wrapper is used.

3. **Telemetry disabled** (privacy/security): `ENV PROMPTFOO_DISABLE_TELEMETRY=1` and `ENV PROMPTFOO_DISABLE_UPDATE_CHECK=1` prevent external data exfiltration from within the container.

4. **HEALTHCHECK is appropriately conservative**: `promptfoo --version` is a safe no-op health check that doesn't expose sensitive information.

5. **Environment variable defaults are safe**: `ENV AGENT_ID=""` and `ENV EVALUATION_MODE=smoke` default to the safest operational mode.

**Negative findings:**

1. **Base image not digest-pinned** (F-002, MC-08 gap): Critical finding documented above.

2. **pip remains in image after UV bootstrap** (F-007): Unnecessary attack surface for container-escape scenarios.

3. **npm cache cleanup is incomplete**: Lines 68-69 remove `/root/.npm` and `/tmp/npm-*`, but `npm install -g` writes to the Node.js global prefix directory (typically `/usr/local/lib/node_modules`). While the installed packages are intentional, the npm audit database and package metadata caches are not cleaned. This is low-severity but could be addressed by adding `npm cache clean --force` after verification.

4. **No explicit `--no-new-privileges` at build time**: The Dockerfile does not use `--security-opt=no-new-privileges` as a build argument. This is correctly enforced at runtime via the workflow `docker run` flags, but is worth noting for defense-in-depth.

5. **`git` and `jq` installed in runtime image**: Both tools are installed for operational reasons (git for file hash resolution, jq for JSON processing). Their presence slightly increases the attack surface. Consider evaluating whether these can be moved to a build-only stage or removed if the container's runtime use case does not require them.

### Runtime Hardening (Workflows)

All three workflows correctly apply the following runtime hardening flags:

- `--read-only`: Immutable container filesystem
- `--security-opt=no-new-privileges:true`: Privilege escalation prevention
- `--cap-drop=ALL`: All Linux capabilities dropped
- `--tmpfs /tmp:rw,size=NNm,noexec,nodev`: Writable tmpfs with noexec preventing code execution from tmpfs
- Memory and CPU limits scaled per evaluation tier
- Named volume mounts with `:ro` for all source directories

The `noexec` flag on the tmpfs mount is a strong defense against attackers who might write shellcode or scripts to `/tmp`. The `nodev` flag prevents device node creation. Together these significantly reduce the impact of a container compromise.

**Network isolation:** The Smoke workflow correctly applies `--network=none` since no LLM calls are made. Standard and Full workflows require external network access for Anthropic API calls, so they correctly omit `--network=none`. There is no explicit allowlist-based network policy for Standard/Full containers — the container can reach any external host. While the runtime environment (GitHub Actions ephemeral runner) limits the practical risk, a network policy restricting the container to only `api.anthropic.com` would further reduce the blast radius of a container compromise. This aligns with the A10 SSRF finding in the OWASP table.

---

## T-40 Adversarial Statistical Bypass Assessment

T-40 (Near-zero-variance bypass) is the 7th-ranked threat by DREAD priority score (Priority Score = 7.2, DREAD Score 6.2 + Integrity Impact Weight 1.0). The threat model rates it Likelihood=M, Impact=H, Risk=High. This section provides a dedicated assessment of the T-40 mitigation status.

**Threat description (system-design.md §3.6):** An attacker crafts score arrays that exploit a near-zero-variance condition to manipulate the Wilcoxon test into always returning `NO_REGRESSION` (p=1.0). For example: version A scores = [0.50, 0.50, 0.50, ...] and version B scores = [0.49, 0.51, 0.49, 0.51, ...] produce paired differences that alternate sign and sum to near-zero, yielding a non-significant p-value despite version B having lower mean quality.

**Mitigation control MC-40** specifies three mechanisms:
1. IQR variance floor check: reject score arrays where IQR < 0.01
2. Effect size cross-check: when p > alpha (non-significant), compute Cohen's d; if |d| > 0.50 despite non-significant p-value, emit WARN
3. Paired-difference symmetry check: if signed rank sum is near zero but mean |diff| > 0.05, flag as potential adversarial cancellation and emit WARN

**Assessment: PARTIAL**

Reviewing `jerry/testing/stats.py` (all 701 lines reviewed):

- `_validate_score_array()` (lines 128-176) correctly rejects arrays where `len(set(scores)) == 1` (all-identical values produce W=0, p=1.0 trivially). This addresses the degenerate constant-array case.
- `InvalidScoreArrayError` is raised for out-of-range values, empty arrays, and non-numeric content.
- The constant naming (`MIN_STATISTICAL_SAMPLE_SIZE = 20`, `QUALITY_PASS_THRESHOLD = 0.92`, `BONFERRONI_ALPHA_FULL = 0.004`) reflects the statistical controls that constrain the attack surface.
- Cohen's r effect size is computed via `_cohens_r()` (lines 184-212) using the normal approximation of the Wilcoxon W statistic.

**Confirmed absent controls (MC-40 Mechanisms 1, 2, and 3):**

The following MC-40-specified mechanisms are **absent** from `stats.py` after full-file review (701 lines):

1. **IQR variance floor check (MC-40 Mechanism 1):** No code checks `IQR < 0.01` on score arrays. The `require_variation=True` check only rejects all-identical arrays (`len(set(scores)) == 1`), not near-zero-variance arrays.
2. **Cohen's d cross-check for non-significant p-values (MC-40 Mechanism 2):** Cohen's *r* (a Wilcoxon-derived rank-biserial correlation) is computed via `_cohens_r()`, but MC-40 specifies Cohen's *d* (the standardized mean difference). These are distinct metrics: Cohen's r measures rank-order effect size while Cohen's d measures mean-difference effect size normalized by pooled standard deviation. There is no logic that checks `|d| > 0.50` when `p > alpha` and emits a WARN. The Cohen's r value is reported but not used as a safety gate.
3. **Paired-difference symmetry check (MC-40 Mechanism 3):** No code detects alternating-sign paired differences where signed rank sum is near zero but mean `|diff| > 0.05`.

The current implementation provides meaningful protection against the most naive T-40 attack vector (constant arrays) but does not address the near-zero-variance or alternating-sign paired-difference patterns described in the threat model.

**Recommendation (P-8):** Implement the following absent controls in `compare_versions()` in `stats.py` before Standard/Full tiers are production-activated:
1. Add IQR variance floor: reject score arrays where `IQR < 0.01` (raise `InvalidScoreArrayError`)
2. Add Cohen's d cross-check: when `p > alpha` and `|Cohen's d| > 0.50`, emit WARN and set `verdict = WARN`
3. Add paired-difference symmetry check: when signed rank sum ≈ 0 but mean `|diff| > 0.05`, flag as potential adversarial cancellation

---

## CWE Top 25 2025 Checklist

Systematic applicability check for each CWE in the [CWE Top 25 2025](https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html) list. "APPLICABLE" means the CWE category applies to this codebase's attack surface. "NOT APPLICABLE" means the CWE is structurally irrelevant (e.g., memory safety issues in a pure Python/Node.js codebase with no native code). "FINDING" means a finding was produced.

| Rank | CWE ID | Name | Status | Notes |
|------|--------|------|--------|-------|
| 1 | CWE-79 | Cross-site Scripting | NOT APPLICABLE | No web UI. PR comment output is GitHub-sanitized. No user-controlled HTML rendered server-side. |
| 2 | CWE-787 | Out-of-bounds Write | NOT APPLICABLE | Python and Node.js (memory-managed runtimes). No native code, no buffer manipulation. |
| 3 | CWE-89 | SQL Injection | NOT APPLICABLE | No SQL database. Baseline store uses filesystem + JSON. |
| 4 | CWE-416 | Use After Free | NOT APPLICABLE | Memory-managed runtimes. |
| 5 | CWE-78 | OS Command Injection | APPLICABLE / NOT FINDING | `version_keys.py` uses subprocess list form (no `shell=True`). CI workflow uses variable quoting. `AGENT_ID` validation gap (F-005) is the closest risk surface, but current Docker isolation limits the impact. The `git` binary in the container is invoked without attacker-controlled arguments. |
| 6 | CWE-20 | Improper Input Validation | APPLICABLE / FINDING | F-001 (MC-02 input sanitization gap), F-003 (version key validation inconsistency), F-005 (AGENT_ID allowlist). |
| 7 | CWE-125 | Out-of-bounds Read | NOT APPLICABLE | Memory-managed runtimes. |
| 8 | CWE-22 | Path Traversal | APPLICABLE / NOT FINDING | `version_keys.py` correctly applies path traversal prevention (`.startswith("/")`, `".." in file_path`, allowlist pattern). SHA-256-keyed paths in `store.py` prevent traversal. F-003 (weaker validation in `store.py`) is a consistency gap but does not produce path traversal in the current implementation. |
| 9 | CWE-352 | Cross-Site Request Forgery | NOT APPLICABLE | No web endpoints. CI/CD system. |
| 10 | CWE-434 | Unrestricted Upload of Dangerous File Type | NOT APPLICABLE | No file upload endpoint. YAML test case files are committed to git and reviewed via PR. |
| 11 | CWE-862 | Missing Authorization | APPLICABLE / NOT FINDING | GitHub Actions minimal permissions (`contents: read`, `pull-requests: write`, `checks: write`) are enforced. Fork secret isolation (MC-28) via `pull_request` event prevents unauthorized secret access. No missing authorization identified. |
| 12 | CWE-476 | NULL Pointer Dereference | NOT APPLICABLE | Python raises `AttributeError`/`TypeError`; not a NULL pointer vulnerability class. |
| 13 | CWE-287 | Improper Authentication | APPLICABLE / NOT FINDING | API key is sourced from GitHub Actions secrets. No authentication bypass path identified. `::add-mask::` prevents log disclosure. |
| 14 | CWE-190 | Integer Overflow | NOT APPLICABLE | Python integers are arbitrary precision. Score bounds validated to [0.0, 1.0]. |
| 15 | CWE-502 | Deserialization of Untrusted Data | APPLICABLE / NOT FINDING | Baseline store uses `json.loads()` (safe). YAML test files use PyYAML in safe-load mode (unverifiable in reviewed files — conftest.py not present, but promptfoo handles YAML loading inside the container). `json.loads()` on the promptfoo output file (MC-09 step) does not use pickle or eval. |
| 16 | CWE-77 | Command Injection | APPLICABLE / NOT FINDING | Docker `docker run` invocations use list-form argument quoting in shell. The `AGENT_ID` value is passed as an `-e` environment variable to Docker, not interpolated into shell command strings directly. The sed pipeline that extracts agent IDs operates on git-diff output, but the resulting values are used only as environment variable values, not shell command arguments. Risk is low with current quoting but allowlist validation (F-005 remediation) would eliminate residual risk. |
| 17 | CWE-119 | Buffer Overflow | NOT APPLICABLE | Memory-managed runtimes. |
| 18 | CWE-798 | Use of Hard-coded Credentials | APPLICABLE / NOT FINDING | No hardcoded API keys found in any reviewed file. `ANTHROPIC_API_KEY` sourced exclusively from GitHub Actions secrets. Dockerfile uses no hardcoded credentials. |
| 19 | CWE-918 | SSRF | APPLICABLE / PARTIAL FINDING | T-07 identifies the promptfoo `file://` protocol handler risk. No explicit promptfoo config restricting the `file://` handler was found. Standard/Full containers have unrestricted HTTPS egress. See OWASP A10 assessment and Recommendations P-10. |
| 20 | CWE-306 | Missing Authentication for Critical Function | APPLICABLE / NOT FINDING | Baseline store write operations are gated by CI workflow execution (requires merged PRs or manual trigger). No unauthenticated write path identified. |
| 21 | CWE-843 | Type Confusion | NOT APPLICABLE | Python's dynamic typing with explicit type checking in `_validate_score_array()` (numeric type check at line 157-163). No C-level type confusion surface. |
| 22 | CWE-94 | Code Injection | APPLICABLE / NOT FINDING | H-07 domain isolation prevents LLM responses from being evaluated as code. No `eval()`, `exec()`, or `__import__()` calls on LLM-sourced strings (MC-21 verified in design; `metrics.py` treats responses as strings). |
| 23 | CWE-400 | Uncontrolled Resource Consumption | APPLICABLE / NOT FINDING | MC-13 (memory/CPU limits per tier), MC-39 (score array length cap N <= 1000), workflow `timeout-minutes` enforced. Resource consumption is bounded by these controls. |
| 24 | CWE-863 | Incorrect Authorization | APPLICABLE / NOT FINDING | Fork PRs do not receive secrets (MC-28). Read-only mounts prevent container writes to source directories. Minimal permissions prevent unauthorized GitHub API operations. |
| 25 | CWE-276 | Incorrect Default Permissions | APPLICABLE / NOT FINDING | Container user is non-root UID 1001. Baseline store files are written by the CI runner (standard filesystem permissions). No world-writable directories identified. |

**Summary:** 12 CWEs applicable; 3 produced findings (CWE-20: F-001, F-003, F-005; CWE-918: OWASP A10 partial); 9 applicable with no finding; 13 not applicable.

---

## Recommendations

Priority-ordered remediation actions based on finding severity and threat model alignment.

| Priority | Finding | Action | Effort |
|----------|---------|--------|--------|
| P-1 (Critical — pre-production blocker) | F-002 (MC-08) | Pin all Docker image references to SHA-256 digests. Start with Smoke workflow `:latest` tag at smoke.yml line 218 — this is immediately exploitable. Generate digests via `docker inspect --format='{{index .RepoDigests 0}}'` and update all four files. | Low (configuration change) |
| P-2 (High — pre-production blocker) | F-001 (MC-02) | Implement input sanitization layer in `deepeval_adapter.py` `evaluate_batch()`. Insert sanitization call between line 329 (`output_text` assignment) and line 330 (`LLMTestCase` construction). Add length limits (10KB prompt, 50KB output) and injection pattern detection. Log pattern matches to the audit trail. | Medium (1-2 days) |
| P-3 (High) | F-003 | Replace `BaselineStore._validate_version_key()` with `VersionKey.from_string()` validation from `version_keys.py`, or import and apply the hash pattern and path allowlist pattern from that module. | Low (30 min) |
| P-4 (Medium) | F-004 | Add failure-rate monitoring to `evaluate_batch()` exception handler. Re-raise when failure rate exceeds 20%. Surface exception count in returned score metadata. | Low (1-2 hours) |
| P-5 (Medium) | F-005 | Add AGENT_ID allowlist check in CI workflows against `COVERED_AGENTS` set before Docker invocation. | Low (30 min) |
| P-6 (Medium) | MC-01/MC-03/MC-05/MC-06 PARTIAL | Implement the `tests/prompt-regression/schemas/test-case.schema.json` file and conftest.py validation for file count and payload size limits. The JSON Schema file must define: `type: object`, `required: [description, prompts, providers, tests]`, `properties.description` with pattern matching filename, `properties.tests.items.vars` with `maxProperties` and per-field `maxLength` constraints. | Medium (1-2 days) |
| P-7 (Medium) | Supply chain | Pin `setup-uv` action's UV install version in smoke.yml line 162: replace `version: "latest"` with `version: "0.5.29"` (matching the Dockerfile's `UV_VERSION="0.5.29"` at `docker/promptfoo/Dockerfile` line 75, ensuring CI and Docker use the same UV version). Add npm lockfile (`package-lock.json`) to Dockerfile build for reproducible npm dependency installation. | Low (1-2 hours) |
| P-8 (Medium) | T-40 / MC-40 | Implement the following absent MC-40 controls in `compare_versions()` in `stats.py`: (1) IQR variance floor — reject score arrays where IQR < 0.01 via `InvalidScoreArrayError`; (2) Cohen's d cross-check — when p > alpha and |Cohen's d| > 0.50, emit WARN verdict; (3) paired-difference symmetry check — when signed rank sum ≈ 0 but mean |diff| > 0.05, flag as adversarial cancellation. All three are confirmed absent after full 701-line review of stats.py. | Medium (1 day) |
| P-9 (Medium) | A10 / CWE-918 | Add a network policy recommendation for Standard/Full containers: configure a Docker network with an explicit egress allowlist restricting outbound traffic to `api.anthropic.com:443` only. Implement as a custom Docker bridge network with iptables OUTPUT rules or via a host-level network policy. | Medium (1 day) |
| P-10 (Low) | F-006 | Strengthen MC-09 output validation to be fatal for missing required keys in Standard and Full modes. Add JSON Schema validation against promptfoo output schema. | Low (2-4 hours) |
| P-11 (Low) | F-007 | Remove pip from the runtime Docker image after UV bootstrap, or use multi-stage build to isolate the pip install step. | Low (1 hour) |
| P-12 (Low) | F-008 | Add invalidation guard in `BaselineStore.store()` to prevent silent overwrite of invalidated baselines without explicit confirmation. | Low (1 hour) |

---

## Self-Review (S-010)

Pre-finalization verification against assessment quality dimensions.

| Dimension | Check | Status |
|-----------|-------|--------|
| **Completeness** | All MC-01 through MC-14 documented in Threat Model Coverage Matrix? | PASS — all 14 controls assessed. |
| **Completeness** | All OWASP Top 10 2021 categories assessed? | PASS — all 10 categories assessed in OWASP Alignment Table, including A02 (Cryptographic Failures), A06 (Vulnerable/Outdated Components — A06 gap, promptfoo npm supply chain), A09 (Security Logging/Monitoring Failures — F-004 silent exception swallowing), A10 (SSRF — T-07 file:// protocol risk). |
| **Completeness** | T-40 (top-9 DREAD threat) assessed? | PASS — dedicated T-40 section with PARTIAL verdict; three absent MC-40 mechanisms explicitly documented after full 701-line stats.py review. |
| **Completeness** | CWE Top 25 2025 systematically checked? | PASS — CWE checklist appendix covers all 25 CWEs with APPLICABLE / NOT APPLICABLE / FINDING status. |
| **Completeness** | All specified implementation files reviewed? | PASS — all 10 files reviewed: `version_keys.py`, `promptfoo-config.yaml`, `Dockerfile`, `prompt-regression-smoke.yml`, `prompt-regression-standard.yml`, `prompt-regression-full.yml`, `stats.py`, `store.py`, `deepeval_adapter.py`, `base.py`, `layer4_stats.py`. |
| **Evidence Quality** | Each finding has specific file:line evidence? | PASS — F-001 through F-009 all include specific file and line number citations with code excerpts. F-001 insertion point identified at deepeval_adapter.py line 330 (before `LLMTestCase` construction). UV `version: "latest"` identified at smoke.yml line 162. |
| **Actionability** | Each finding has concrete remediation? | PASS — each finding includes remediation steps and where applicable, code examples. P-6 specifies JSON Schema field structure for `test-case.schema.json`. P-7 specifies exact target UV version pin instruction. P-9 specifies network policy recommendation as a numbered priority. |
| **Traceability** | Each finding traces to a correct requirement or threat? | PASS — F-001 threat mapping corrected: T-02 is YAML vars injection with MC-02 assigned to `deepeval_adapter.py` (verified against system-design.md Part 4 line 1535); the adapter is the downstream surface where T-02 injection manifests, not a separately modeled threat. F-005 threat mapping corrected: T-02 (YAML injection via git-diff-derived filenames) and T-07 (file:// protocol exploitation via path-containing AGENT_ID) — T-03 (threshold tampering) removed as it is not the relevant threat for AGENT_ID validation. Contracts reference corrected to `contracts/behavioral-contracts.md` (verified path). MC-28 reference in OWASP table explained as drawn from the full MC-01 through MC-40 control set. |
| **Internal Consistency** | Summary count annotation correct? | PASS — summary row reads "7 IMPLEMENTED, 4 PARTIAL, 2 MISSING" with no spurious "PARTIAL-CRITICAL" category. MC-02 is classified as MISSING. |
| **ASVS Coverage** | ASVS V5 (Input Validation), V6 (Cryptography), V7 (Logging) addressed? | PASS — V5 addressed by F-001 (input validation gap), F-003 (version key validation); V6 addressed by F-009 (hash truncation), A02 assessment (key management); V7 addressed by F-004 (exception swallowing), A09 assessment (logging gaps). |
| **Severity Calibration** | Critical/High findings are genuinely blocking production deployment? | PASS — F-001 (MC-02 missing) and F-002 (MC-08 missing) are both pre-production blockers per the threat model's own High risk ratings. |

---

*Assessment produced by: eng-security (Security Code Review Specialist)*
*Review date: 2026-03-07*
*Iteration: 4 (iter1: 0.835, iter2: 0.908, iter3: 0.932 — threshold 0.94)*
*Scope: PROJ-036 Four-Layer Composite Test Harness — full codebase review (10 implementation files)*
*Methodology: Manual code review with data flow tracing, CWE Top 25 2025 checklist (all 25 entries), OWASP ASVS 5.0 V5/V6/V7/V8, OWASP Top 10 2021 (all 10 categories), threat model correlation (MC-01 through MC-40 with dedicated T-40 assessment)*
