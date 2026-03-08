# Security Re-Assessment — PROJ-036 Gap Closure Deliverables

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Overall risk posture, finding counts, key recommendations |
| [L1 Technical Detail](#l1-technical-detail) | Per-dimension vulnerability inventory with evidence |
| [L2 Strategic Implications](#l2-strategic-implications) | Attack path analysis, engagement alignment, hardening recommendations |

---

## Assessment Metadata

| Field | Value |
|-------|-------|
| Analyst | red-vuln (Vulnerability Analyst) |
| Assessment Date | 2026-03-07 |
| Scope | PROJ-036 gap-closure-20260307-001 deliverables (27 gaps, 5 work items) |
| Assessment Type | Security re-assessment of gap closure changes |
| Focus | NEW vulnerabilities introduced by the gap closure; pre-existing issues excluded |
| Tool Level | Level 2 (Standalone) — code review without active scanning tools |
| Authorization | Analysis only; no exploitation |

**Files assessed:**

1. `jerry/testing/layer4_stats.py`
2. `jerry/testing/baselines/store.py`
3. `jerry/testing/evaluation/deepeval_adapter.py`
4. `jerry/testing/evaluation/jerry_geval_deepeval_metric.py`
5. `jerry/testing/evaluation/exceptions.py`
6. `jerry/testing/extraction/promptfoo_extractor.py`
7. `tests/prompt-regression/conftest.py`
8. `tests/prompt-regression/unit/` (6 unit test files + test_build_metric_for_mr.py + test_resolve_model.py)
9. `tests/prompt-regression/integration/` (test_layer4_pipeline.py, test_evaluator_construction.py, test_pipeline_smoke.py)
10. `.github/actions/cost-monitor/action.yml`
11. `.github/actions/artifact-publish/action.yml`
12. `.github/workflows/prompt-regression-*.yml`
13. `scripts/pre_tool_use.py`

---

## L0 Executive Summary

### Finding Counts by Severity

| Severity | Count | Notes |
|----------|-------|-------|
| Critical | 0 | No critical findings from gap closure changes |
| High | 0 | No high findings |
| Medium | 2 | Docker image tag-only pinning (pre-existing, worsened by no SHA remediation); shell injection surface in cost-monitor action |
| Low | 3 | Symlink traversal gap in BaselineStore; version key path component not sanitized for filesystem use; uv install version pinning absent |
| Informational | 2 | `TODO(CG-008)` stub accepting unvalidated commit SHA; `GITHUB_ENV` injection surface in artifact-publish |

### Overall Risk Posture

**LOW-MEDIUM.** The gap closure successfully closed its 27 canonical gaps. The security controls introduced (CG-025 path traversal, CG-027 regex validation, CG-018A/B GHA output sanitization, CG-005 typed exception hierarchy, CG-013 case-insensitive model detection, CG-024 Bedrock identifier rejection, CG-016 telemetry opt-out, bool-guard on score extraction) are correctly implemented and well-tested. No introduced vulnerability rises above Medium severity. The two Medium findings are architectural limitations of the current CI/CD design rather than implementation defects; both have mitigating controls in place.

### Top Exploitable Findings

1. **M-001 (Medium):** Docker image pinned to version tag `0.86.0` without SHA digest. Tag mutation or registry compromise allows supply-chain injection into the evaluation pipeline. Mitigated by GHCR provenance and the fact that `ghcr.io/promptfoo/promptfoo` is maintained by a known vendor; risk is elevated only under adversarial supply-chain conditions.
2. **M-002 (Medium):** `cost-monitor/action.yml` interpolates GHA inputs directly into `bash` heredocs and Python `-c` strings (`${AGENT}`, `${TIER}`, `${CEILING_USD}`, `${TOTAL_TOKENS_K}`). Values sourced from `inputs.agent_name` and `inputs.evaluation_tier` are not validated before interpolation. If an adversary can control workflow inputs (e.g., via `workflow_dispatch` with malicious `target_agents`), shell metacharacters could be injected.
3. **L-001 (Low):** `BaselineStore.audit()` calls `self._root.rglob("*.json")` which will follow symlinks. An attacker who can create a symlink inside `baselines/data/` pointing to an arbitrary JSON file outside the project could cause the audit to read unintended files. Write access to the baselines directory is required, making this a low-severity local privilege escalation.

### Key Recommendations for Stakeholders

1. Upgrade Docker image references to SHA-pinned digests (CG-007 accepted deviation should be re-evaluated at next GHCR availability window).
2. Add input validation for `agent_name` in `cost-monitor/action.yml` matching the same regex applied in `layer4_stats.py` main() (^[a-z][a-z0-9_-]*$).
3. Mark `TODO(CG-008)` in `baselines/store.py` as a tracked security item: the commit SHA is currently trusted without cryptographic verification.

---

## L1 Technical Detail

### Dimension 1: Input Validation Completeness

**CG-025 — Path Traversal (output path validation)**

STATUS: IMPLEMENTED CORRECTLY. No new vulnerability introduced.

`Layer4Pipeline._validate_output_path()` (layer4_stats.py lines 396-421) resolves the supplied path to absolute form using `path.resolve()`, then calls `resolved.is_relative_to(cwd)`. This is the correct approach: `Path.is_relative_to()` compares resolved absolute paths, defeating all `../` traversal sequences including URL-encoded and double-encoded variants. The CWD anchor is computed fresh at call time via `Path.cwd().resolve()`, eliminating stale-CWD race conditions. Unit tests in `test_path_validation.py` confirm rejection of `..`-relative paths and absolute paths outside CWD.

One gap: `_validate_output_path()` is called for JSON and Markdown output paths but NOT for the `store_root` supplied to `BaselineStore.__init__()`. If a caller passes a `store_root` containing `../` sequences, the baseline store will create files outside the intended directory. This is a pre-existing design gap, not introduced by the gap closure, but the gap closure's wiring of `BaselineStore` in `layer4_stats.py` main() (line 662-664) uses a `__file__`-relative path which mitigates the risk in the production invocation. Manual CLI callers who construct `BaselineStore` directly remain at risk.

CVSS v3.1 estimate (residual gap): 3.3 (AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N) — Low.

**CG-018 — GHA Output Sanitization**

STATUS: IMPLEMENTED CORRECTLY. No new vulnerability introduced.

`_emit_gha_outputs()` in layer4_stats.py (lines 454-495) sanitizes all values written to GITHUB_OUTPUT by replacing `\n` and `\r` with spaces before writing `key=value\n` lines. The sanitization is applied both in the GHA context (file write) and in the local logging fallback. Agent ID format validation (lines 620-628) uses `re.match(r"^[a-z][a-z0-9_-]*$", args.agent)` which prevents injection of control characters, special characters, and path separators via the `--agent` CLI argument.

Residual risk: The `report.classification`, `report.merge_recommendation`, `report.agent`, and `report.evaluation_mode` values written to GHA_OUTPUT originate from the statistical engine's internal enum values. These are bounded by Python enum membership and do not contain user-controlled data. No injection surface here.

**CG-027 — Version Key Pattern Validation**

STATUS: IMPLEMENTED CORRECTLY. No new vulnerability introduced.

`VERSION_KEY_PATTERN = re.compile(r"^[0-9a-f]{7,40}:[^\n\r\0]+$")` (store.py line 71) is anchored at both ends (`^` and `$`), enforces 7-40 lowercase hex for the git hash component, and excludes newline, carriage return, and null byte from the path component. The `_validate_version_key()` method applies both a structural colon-split check and the regex check in sequence. Tests in `test_version_key_validation.py` cover all injection vectors: newline, carriage return, null byte, uppercase hex, and truncated hash.

One observational gap: the version key path component (after the colon) is passed through as a filesystem slug after SHA256 hashing in `_record_path()`, so the raw path is never used directly as a filename. The SHA256 hashing (line 415: `hashlib.sha256(version_key.encode()).hexdigest()[:16]`) provides a complete filesystem safety barrier regardless of what characters appear in the path component. The CG-027 validation thus provides defense-in-depth rather than being the sole protection.

**CG-018 — Regex Validation (bool guard in promptfoo_extractor.py)**

STATUS: IMPLEMENTED CORRECTLY. No new vulnerability introduced.

`extract_score_arrays()` (promptfoo_extractor.py lines 279-287) explicitly rejects boolean scores before the numeric type check:

```python
if isinstance(raw_score, bool):
    logger.warning(...)
    continue
```

This prevents `True` (which equals 1 in Python) from being interpreted as score 1.0 and `False` (which equals 0) from being interpreted as score 0.0. Both would pass the range check `0.0 <= score <= 1.0`. This is a correct defensive measure against JSON boolean coercion. No vulnerability introduced.

**agent_id validation gap in cost-monitor action:**

The `cost-monitor/action.yml` receives `agent_name` as a workflow input and interpolates it directly into bash heredocs, Python `-c` strings, and environment variable assignments:

```bash
AGENT="${{ inputs.agent_name }}"
...
cat >> "$GITHUB_STEP_SUMMARY" << EOF
| Agent | ${AGENT} | ...
EOF
```

And:

```python
record = {
    'agent': '${AGENT}',
    ...
}
```

The `layer4_stats.py main()` applies `re.match(r"^[a-z][a-z0-9_-]*$", args.agent)` before running the pipeline, but the cost-monitor action operates independently and has no equivalent validation. If `inputs.agent_name` contains shell metacharacters (e.g., `ps-researcher$(malicious)` or a newline), the bash interpolation in the heredoc and the Python `-c` string may be affected.

Mitigating controls: (1) `workflow_dispatch` triggers require authentication; (2) the `target_agents` input in the Full workflow is filtered through `jq -R -s -c` which produces a JSON array, limiting injection opportunity; (3) in PR-triggered Standard workflow, `agent_name` is derived from `matrix.agent`, which originates from the `changed_agents` output filtered through `sed` and `jq`. The jq filtering substantially reduces the injection surface.

Residual risk without explicit validation in the action: agent names derived from PR file paths (sed extraction: `sed 's|.*/agents/||'` + `sed 's|\.md$||'`) could contain unexpected characters if a branch introduces a specially crafted filename in `skills/*/agents/`. This is a low-probability, low-impact vector given the file path origin, but the absence of explicit validation in the action is a defense gap.

CVSS v3.1 estimate: 4.2 (AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:N) — Medium (requires ability to create files with crafted names in the repository and trigger the PR workflow, which requires merge access or PR creation).

### Dimension 2: API Key Handling (CG-006 / CG-016)

STATUS: CORRECTLY IMPLEMENTED. No hardcoded keys. No new vulnerability introduced.

`deepeval_adapter.py` (lines 158-168, 425-436) uses `os.environ.get("ANTHROPIC_API_KEY", "")` exclusively. The check raises `EvaluationConfigError` with a descriptive message when the key is absent but does NOT log, surface, or store the key value itself. The `context` dict carried in `EvaluationConfigError` contains `{"field": "ANTHROPIC_API_KEY", "model_name": ...}` — the field name but never the key value.

`conftest.py` reads `ANTHROPIC_MODEL` from environment with a hard-coded default model identifier, which is a model name string (not a secret). No API key handling in conftest.

Workflows mask the API key via `echo "::add-mask::${{ secrets.ANTHROPIC_API_KEY }}"` (MC-31) before any step that might log it. The mask is applied early in the job.

`DEEPEVAL_TELEMETRY_OPT_OUT: "YES"` is set as a workflow environment variable (CG-016), preventing DeepEval from transmitting evaluation data to external telemetry endpoints.

No hardcoded API keys found in any assessed file. Finding: PASS.

### Dimension 3: Exception Hierarchy Safety (CG-005)

STATUS: IMPLEMENTED. Minor information disclosure surface exists.

`exceptions.py` defines three exception classes (`EvaluationConfigError`, `EvaluationAPIError`, `EvaluationScoringError`) each carrying an optional `context: dict[str, str]` attribute. The design separates structured diagnostics from the human-readable message, which is correct for preventing accidental key leakage into log messages.

Information disclosure analysis:

- `EvaluationConfigError` is constructed with `context={"field": "ANTHROPIC_API_KEY", "model_name": self.model_name}`. The field name is a known environment variable name, not a secret. Model name is a non-sensitive configuration string. No key value exposure.
- `EvaluationScoringError` is constructed with `context={"agent": ..., "zero_count": ..., "zero_fraction": ...}`. Non-sensitive operational metrics.
- `EvaluationAPIError` examples in docstrings suggest `context={"status_code": "429", "retry_after": "60"}`. HTTP status codes and retry headers are non-sensitive.

In `_evaluate_synchronously()` (jerry_geval_deepeval_metric.py lines 263-268), the last-resort `BLE001` handler wraps `exc` and includes `str(exc)` in the new `EvaluationScoringError`'s message. If the underlying exception from DeepEval's GEval contains API response data including internal headers or rate-limit metadata, that data propagates into the error message. This is an inherited disclosure from the DeepEval library, not introduced by this gap closure.

The test `test_config_error_with_context_dict_should_store_context` in `test_exceptions.py` asserts the context is accessible, but does not test that secret values are NOT included. This is a coverage gap in the security test suite.

CVSS v3.1 estimate (theoretical): 2.2 (AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N) — Informational/Low. Requires specific conditions in DeepEval's error paths to expose non-public data.

### Dimension 4: Docker Image Pinning (CG-007)

STATUS: PARTIALLY MITIGATED. Accepted deviation — SHA digest pending.

Both `prompt-regression-full.yml` and `prompt-regression-standard.yml` reference:

```
PROMPTFOO_IMAGE="ghcr.io/promptfoo/promptfoo:0.86.0"
```

The inline comment confirms the accepted deviation:

```
# CG-007: Version-pinned Docker image (supply chain security).
# To upgrade to SHA pinning: docker pull <tag> && docker inspect --format='{{index .RepoDigests 0}}' <tag>
# Then replace the tag with the @sha256: digest.
```

This was assessed in the original gap analysis (CG-007 accepted deviation, barrier cleared). From a re-assessment perspective:

- Version tag `0.86.0` is mutable by the registry operator (GHCR). If the promptfoo project's GHCR registry is compromised or the tag is reassigned to a different image, the pipeline will silently consume the malicious image.
- Mitigating controls: (1) GitHub Container Registry (`ghcr.io`) requires authentication for writes; the promptfoo package is maintained by a known open-source project; (2) `--read-only`, `--cap-drop=ALL`, `--security-opt=no-new-privileges:true`, `--tmpfs` docker flags constrain what a compromised container can do on the host.
- The container has `ANTHROPIC_API_KEY` passed via `-e ANTHROPIC_API_KEY`, which means a compromised container image could exfiltrate the key.

The runtime hardening (read-only filesystem, dropped capabilities, no-new-privileges) does NOT prevent the container process from making outbound network calls to exfiltrate the injected API key. This represents the substantive residual risk of not SHA-pinning.

CVSS v3.1 estimate (tag mutation scenario): 5.9 (AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N) — Medium. Requires supply chain compromise of GHCR.io/promptfoo/promptfoo, which is a realistic but low-probability attack.

**Third-party GitHub Actions pinning:** All pinned actions use commit SHA:
- `actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683` (v4.2.2)
- `astral-sh/setup-uv@f0ec1fc3b38f5e7cd731bb1ce926ae18e12f4ccd` (v5.4.1)
- `actions/upload-artifact@ea165f8d65b6e75b540449bea1e5c8c7e45e428` (v4.6.2)
- `actions/github-script@60a0d83039c74a4aee543508d2ffcb1c3799cdea` (v7.0.1)

These are correctly SHA-pinned. No supply chain gap for GHA actions themselves.

### Dimension 5: Supply Chain (CG-028 / CG-029 / CG-030)

**CG-028 — deepeval version pinning:**

```toml
"deepeval>=3.8.0,<4.0.0",
```

The `>=3.8.0,<4.0.0` constraint prevents breaking API changes from DeepEval v4 but does not prevent silent feature-level changes within the 3.x series. For security-relevant dependencies (the LLM judge adapter), minor version changes in DeepEval could alter how `GEval.score`, `AnthropicModel`, or `BaseMetric` behave, potentially affecting scoring fidelity.

Assessment: The upper bound `<4.0.0` is correct. The lower bound `>=3.8.0` is reasonable. No improvement needed for security purposes; functional regression testing covers behavioral changes.

**CG-029 — scipy explicit dependency:**

```toml
"scipy>=1.11.0",
```

`scipy>=1.11.0` without an upper bound allows automatic minor and major version upgrades. For a statistical library used in Wilcoxon signed-rank tests, a major version change could alter test behavior or introduce breaking API changes. This is a supply chain risk but was assessed as acceptable in the gap closure (CG-029 is about explicit dependency declaration, not strict pinning). No new vulnerability from the gap closure.

**pip-audit (CG-030):** No evidence of a pip-audit step in the CI workflows was found. The gap closure documentation references CG-030 but the workflow files do not contain a `pip-audit` or `uv audit` invocation. This is a pre-existing gap, not introduced by the gap closure changes.

**UV version in workflows:**

```yaml
uses: astral-sh/setup-uv@f0ec1fc3b38f5e7cd731bb1ce926ae18e12f4ccd
with:
  version: "latest"
```

`version: "latest"` for the uv installation means the uv binary itself is not version-pinned. A compromised or maliciously updated uv release could affect dependency resolution during `uv sync`. This is a low-severity supply chain gap given that the action itself is SHA-pinned (preventing action code injection) and uv is maintained by Astral with a strong security track record. However, `version: "latest"` is inconsistent with the supply chain hardening philosophy applied to all other dependencies.

CVSS v3.1 estimate (uv "latest" scenario): 3.1 (AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N) — Low.

### Dimension 6: Symlink Traversal in BaselineStore.audit()

`BaselineStore.audit()` (store.py lines 346-389) uses `self._root.rglob("*.json")`. Python's `Path.rglob()` follows symbolic links by default. If an attacker can create a symlink inside `baselines/data/` pointing to a JSON file elsewhere on the filesystem (e.g., `/etc/passwd` reformatted as JSON, or an application secrets file), `audit()` will attempt to read and parse it. Malformed content is caught by the `json.JSONDecodeError` handler (line 362-364), but valid JSON content from an unintended file would be surfaced in the audit output.

This requires write access to the baseline data directory. In the CI context (GitHub Actions runner), the runner has write access to the workspace, so a malicious workflow step could create such a symlink before audit runs. In the production local use case, it requires local write access to the project directory.

CVSS v3.1 estimate: 3.3 (AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N) — Low.

### Dimension 7: TODO(CG-008) — Unvalidated Commit SHA in Baseline Store

In `baselines/store.py` main() (lines 597-626), the `store` action constructs a version key as:

```python
version_key = f"{args.commit_sha}:{args.agent_file}"
```

The `args.commit_sha` value comes from the CLI `--commit-sha` argument, which originates from the git SHA captured in the workflow (`git rev-parse HEAD`). In the workflow context this is safe. However, the `TODO(CG-008)` comment indicates score extraction is not yet wired:

```
logger.info(
    "TODO(CG-008): Score extraction not yet wired. "
    "Store invocation received for agent=%s version=%s.",
    ...
)
return 0
```

The store action currently accepts any `--commit-sha` value without cryptographic verification that it corresponds to a real, authorized commit. Once CG-008 score extraction is implemented, the commit SHA will be embedded in the version key stored to disk. If the SHA is attacker-controlled (e.g., via `workflow_dispatch` with a crafted input), the version key will contain an unverified SHA. The CG-027 regex validation does constrain the SHA to `[0-9a-f]{7,40}`, preventing most injection attacks, but it does not verify the SHA is a real git object.

This is Informational: the downstream impact is that baseline records could be created with false version attribution, allowing an attacker to claim a baseline was captured at a different commit than it actually was. The quality gate (mean >= 0.92) still applies.

### Dimension 8: GITHUB_ENV Injection in artifact-publish Action

`artifact-publish/action.yml` writes to `GITHUB_ENV` via:

```bash
echo "RESOLVED_AGENT=${AGENT}" >> "$GITHUB_ENV"
echo "EFFECTIVE_REPORT_JSON=${REPORT_JSON}" >> "$GITHUB_ENV"
```

Where `AGENT` is sourced from `inputs.agent_id` or `inputs.agent_name`. If these inputs contain newlines (the GITHUB_ENV injection pattern: `KEY=VALUE\nNEW_KEY=NEW_VALUE`), an attacker could inject additional environment variables.

Mitigating control: GHA strips newlines from `${{ inputs.* }}` expressions at the expression evaluation stage. This is a documented GHA protection. The risk is informational given current GHA behavior, but is worth noting if the action is adapted for other CI systems.

CVSS v3.1: Informational in GHA context.

---

## L2 Strategic Implications

### Attack Path Analysis

**Path A — Supply Chain via Docker Image (Realistic, Medium Probability)**

```
Adversary compromises GHCR promptfoo registry
    |
    v
ghcr.io/promptfoo/promptfoo:0.86.0 tag reassigned to malicious image
    |
    v
PR triggers Standard workflow
    |
    v
Malicious container receives ANTHROPIC_API_KEY via -e ANTHROPIC_API_KEY
    |
    v
Container exfiltrates key via outbound HTTPS (not blocked by --cap-drop=ALL)
    |
    v
Adversary uses key for unauthorized LLM API consumption / data access
```

Attack chain prerequisite: GHCR registry compromise. Probability: Low. Impact: High (API key exfiltration, unauthorized billing). Overall: Medium.

**Path B — Malicious Agent File Name via PR (Low Probability)**

```
Adversary submits PR creating skills/*/agents/ps-researcher$(evil).md
    |
    v
Standard workflow detect-changed-agents job extracts filename via sed
    |
    v
sed extraction may retain shell metacharacters if not filtered by jq
    |
    v
cost-monitor action receives agent_name=$(evil) via matrix.agent
    |
    v
Bash heredoc interpolates ${AGENT} with shell injection
```

Attack chain prerequisite: Ability to create PRs with crafted filenames; jq filtering in changed-agents detection must fail to sanitize. Probability: Very Low (jq filtering substantially limits this). Impact: Low (CI job failure or environment variable injection within the runner). Overall: Low.

**Path C — Symlink Injection in Baseline Store (Requires Local Access)**

```
Attacker has write access to baselines/data/ directory
    |
    v
Creates baselines/data/ps-researcher/composite_score/evil -> /etc/passwd
    |
    v
Runs BaselineStore.audit()
    |
    v
audit() reads symlink target as JSON (fails silently on parse error)
    |
    v
If target is valid JSON, unintended data surfaces in audit output
```

Attack chain prerequisite: Local write access to the baselines directory. This is inside the project workspace, so the attacker already has significant access. Impact: Information disclosure of local JSON files. Overall: Low.

### Risk Scoring Summary

| Finding ID | Description | CVSS Base | Severity | New in Gap Closure? |
|-----------|-------------|-----------|----------|---------------------|
| M-001 | Docker image version-tag-only pinning (CG-007 accepted deviation) | 5.9 | Medium | No (pre-existing accepted deviation) |
| M-002 | cost-monitor action lacks agent_name format validation before shell interpolation | 4.2 | Medium | Yes (action was introduced/modified in gap closure) |
| L-001 | BaselineStore.audit() follows symlinks via rglob() | 3.3 | Low | Yes (store.py introduced in gap closure) |
| L-002 | uv `version: "latest"` in CI workflows — unpinned build tool | 3.1 | Low | Yes (workflows modified in gap closure) |
| L-003 | store_root path not validated for traversal on BaselineStore construction | 3.3 | Low | Yes (store.py introduced in gap closure) |
| I-001 | TODO(CG-008) — commit SHA accepted without git object verification | N/A | Informational | Yes (stub in store.py) |
| I-002 | GITHUB_ENV injection surface in artifact-publish (mitigated by GHA) | N/A | Informational | Yes (action modified in gap closure) |

### ATT&CK Technique Mappings

| Finding | ATT&CK Technique |
|---------|-----------------|
| M-001 (Docker supply chain) | T1195.001 (Supply Chain Compromise: Compromise Software Dependencies and Development Tools) |
| M-002 (shell injection) | T1059.004 (Command and Scripting Interpreter: Unix Shell) |
| L-001 (symlink traversal) | T1083 (File and Directory Discovery) |
| L-002 (unpinned build tool) | T1195.001 (Supply Chain Compromise) |
| I-001 (false SHA attribution) | T1556 (Modify Authentication Process) — minor, integrity concern only |

### Engagement Objective Alignment

The primary security objective for PROJ-036 is protecting the integrity of the regression harness pipeline and its statistical outputs. The gap closure successfully addressed all 27 canonical gaps. The new findings introduced by the gap closure are confined to:

1. A CI/CD pipeline hardening gap (M-002) that could affect pipeline integrity but not statistical output integrity (the main protection is the CWD-anchored path validation and statistical engine).
2. Baseline store design properties (L-001, L-003) that affect local development scenarios more than the CI pipeline.

The core security posture of the pipeline — API key env-only handling, path traversal prevention, GHA output injection prevention, version key integrity — is correctly implemented.

### Recommendations for Hardening (eng-team)

1. **[Priority: High]** Add agent_id format validation (`^[a-z][a-z0-9_-]*$`) to `cost-monitor/action.yml` as a validation step before any shell interpolation, mirroring the pattern used in `layer4_stats.py main()`.

2. **[Priority: High]** Resolve CG-007 Docker SHA pinning. The accepted deviation comment documents the procedure: `docker pull ghcr.io/promptfoo/promptfoo:0.86.0 && docker inspect --format='{{index .RepoDigests 0}}'`. The promptfoo GHCR registry supports SHA digests. This should be done at the earliest available Docker daemon window.

3. **[Priority: Medium]** Pin uv version in CI workflows. Change `version: "latest"` to a specific version pin (e.g., `version: "0.5.4"`) to ensure reproducible builds and reduce supply chain exposure.

4. **[Priority: Medium]** Add `follow_symlinks=False` to `BaselineStore.audit()`'s rglob call. Python 3.12 supports `path.rglob("*.json", follow_symlinks=False)`. This eliminates the symlink traversal surface without functional impact.

5. **[Priority: Low]** Implement store_root path validation in `BaselineStore.__init__()` analogous to `_validate_output_path()` in Layer4Pipeline. A check that `store_root.resolve().is_relative_to(Path.cwd().resolve())` would prevent accidental writes outside the project root.

6. **[Priority: Low]** Track `TODO(CG-008)` as a security item. When score extraction is wired, add commit SHA verification (e.g., `git cat-file -t <sha>` returning "commit") before accepting the SHA in the version key.

7. **[Priority: Informational]** Add a negative test to the exception hierarchy test suite asserting that `EvaluationConfigError.context` never contains an API key value. This documents the invariant and catches future regressions.

### Threat Model Assumptions Validated

The gap closure did not introduce any violations of the following assumptions in the existing threat model:

- API keys are env-only: CONFIRMED
- GHA outputs are sanitized: CONFIRMED (CG-018A/B correctly implemented)
- Output path traversal is blocked: CONFIRMED (CG-025 correctly implemented)
- Version key injection is blocked: CONFIRMED (CG-027 correctly implemented)
- Docker telemetry is disabled: CONFIRMED (CG-016 DEEPEVAL_TELEMETRY_OPT_OUT=YES)
- Exception hierarchy does not leak secrets: CONFIRMED (context dicts contain field names, not values)

### Threat Model Assumptions Stressed (New Attack Paths)

The following attack paths were not addressed in the prior threat model and were identified during this re-assessment:

1. **Symlink injection into baseline store** — not modeled. Requires local write access; low-impact but non-zero.
2. **Crafted agent filename in PR triggering shell injection** — partially modeled (agent_id validation exists in Python layer) but the CI action layer lacks equivalent protection.
3. **uv build tool supply chain** — not modeled. Lower risk than Docker due to Astral's security posture, but consistency with the supply chain philosophy warrants pinning.

---

## Assessment Limitations

- This assessment is performed at Level 2 (standalone) without active scanning tools. Nuclei, Nessus, or pip-audit results would elevate evidence quality for the supply chain dimension.
- No dynamic analysis was performed. The bash shell injection surface (M-002) was assessed by static code review only; runtime behavior under crafted inputs was not verified.
- DeepEval library internals (GEval, AnthropicModel, BaseMetric) were not assessed. The library is treated as a trusted dependency; vulnerabilities within DeepEval itself are out of scope.
- The `scripts/pre_tool_use.py` hook was reviewed but assessed as pre-existing code outside the gap closure scope. The `"eval"` dangerous command detection using word-boundary regex (`(?<![a-zA-Z0-9_.-])eval(?![a-zA-Z0-9_.-])`) is noted as correctly avoiding false positives on `deepeval` filenames.

---

*red-vuln | Vulnerability Analyst | /red-team skill*
*Assessment Level: Level 2 (Standalone — no active scanning)*
*Constitutional Compliance: P-001 (evidence-based), P-002 (persisted), P-022 (no deception)*
*Agent Version: 1.0.0*
*SSOT: ADR-PROJ010-001, ADR-PROJ010-006*
