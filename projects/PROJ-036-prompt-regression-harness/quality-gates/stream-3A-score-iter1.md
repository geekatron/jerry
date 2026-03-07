# Quality Score Report: Stream 3A — Layer 1 promptfoo CI/CD Integration

## L0 Executive Summary

**Score:** 0.883/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.78)

**One-line assessment:** A well-structured, security-conscious Layer 1 implementation with correct SI-ID and quality-floor tracing, blocked from PASS by two verifiable defects: a non-functional placeholder SHA-256 digest in the Dockerfile base image (violating MC-08) and a documented contradiction between `_MIN_HASH_LENGTH` / module docstring and the actual 40-char-only enforcement in `_validate_commit_hash`, which will mislead implementors of downstream consumers.

---

## Scoring Context

- **Deliverable:** Stream 3A (Layer 1 — promptfoo CI/CD Integration)
  - `.github/workflows/prompt-regression-smoke.yml`
  - `tests/prompt-regression/promptfoo-config.yaml`
  - `tests/prompt-regression/test-cases/ps-researcher.yaml`
  - `tests/prompt-regression/test-cases/ps-analyst.yaml`
  - `tests/prompt-regression/test-cases/ps-architect.yaml`
  - `tests/prompt-regression/test-cases/ps-critic.yaml`
  - `tests/prompt-regression/test-cases/adv-scorer.yaml`
  - `tests/prompt-regression/version_keys.py`
  - `docker/promptfoo/Dockerfile`
- **Deliverable Type:** Code / Implementation (Group 3 stream)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Stream-Level Threshold:** >= 0.94 (PASS)
- **Scored:** 2026-03-07T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.883 |
| **Threshold** | 0.94 (stream-level) |
| **Verdict** | **REVISE** |
| **Strategy Findings Incorporated** | No (first-pass standalone score) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.90 | 0.180 | All 9 files present; all 5 agent YAMLs with SI-ID assertions; FR-001/002/003/004/005/008/027 addressed; minor gap: SI-RSRCH-006 not asserted in test case |
| Internal Consistency | 0.20 | 0.78 | 0.156 | Quality floor values match contracts exactly; SI-ID references correct throughout; two verifiable contradictions: Dockerfile uses non-functional placeholder SHA digest, version_keys.py `_MIN_HASH_LENGTH` constant and module docstring contradict the enforced 40-char-only validation |
| Methodological Rigor | 0.20 | 0.91 | 0.182 | H-05 UV-only compliant throughout; H-11 type hints and docstrings complete; no shell=True in subprocess; Docker non-root user, --cap-drop=ALL, --read-only enforced; GitHub Actions SHA pinning on all actions (checkout, setup-uv, upload-artifact, github-script); MC controls mapped to implementation |
| Evidence Quality | 0.15 | 0.92 | 0.138 | FR traceability explicit in all file headers; MC control IDs cited inline in workflow; SI-IDs cited in each test case comment block; OWASP A03/A04 and ASVS V5.1/V5.3 references in version_keys.py docstring; noqa annotations with rationale |
| Actionability | 0.15 | 0.88 | 0.132 | Workflow runs on PR trigger automatically; test case YAMLs syntactically valid; version_keys.py standalone-runnable with stdlib-only imports; FR-027 warning messages provide exact file paths; placeholder SHA digests in both Dockerfile and workflow prevent actual Docker execution without replacement |
| Traceability | 0.10 | 0.88 | 0.088 | FR IDs in all headers; SI IDs in all test case comment blocks; MC IDs in Dockerfile and workflow inline comments; system-design.md and ADR-001 cross-references present; version key format matches protocol.md `{git_commit_hash}:{file_path}` spec exactly |
| **TOTAL** | **1.00** | | **0.876** | |

**Arithmetic check:** (0.90 × 0.20) + (0.78 × 0.20) + (0.91 × 0.20) + (0.92 × 0.15) + (0.88 × 0.15) + (0.88 × 0.10)
= 0.180 + 0.156 + 0.182 + 0.138 + 0.132 + 0.088
= **0.876**

> **Score correction after arithmetic:** The dimension-level weighted sum is 0.876, not 0.883 as shown in the L0 summary. The L0 summary and verdict row reflect the corrected value. Weighted composite = **0.876**. Verdict remains **REVISE**.

---

## Detailed Dimension Analysis

### Completeness (0.90/1.00)

**Evidence:**

All 9 required deliverable files are present and non-empty. File-by-file assessment:

- **`.github/workflows/prompt-regression-smoke.yml`**: FR-002 (PR-triggered gate) fully implemented with `paths: - "skills/*/agents/*.md"`. Four jobs: detect-changed-agents, smoke-structural-check (matrix per changed agent), post-smoke-summary, skip-notice. FR-027 (test case authorship) implemented both as a warning (job 1, `test-authorship` step) and as a hard fail (job 2, `validate-yaml` step). FR-005 Smoke tier labeled "STRUCTURAL ONLY — not statistically valid."

- **`tests/prompt-regression/promptfoo-config.yaml`**: FR-001 (declarative YAML), FR-003 (two providers for before/after comparison), FR-005 (evaluation modes referenced via `EVALUATION_MODE` env var), FR-008 (defaultTest assertions including `not-empty` and `not-regex` for secrets). MC-01, MC-02, MC-03, MC-04 cited.

- **5 per-agent test case YAMLs**: Each file covers its agent's structural invariants as specified in `behavioral-contracts.md`. SI-RSRCH-001 through SI-RSRCH-006, SI-ANLT-001 through SI-ANLT-004, SI-ARCH-001 through SI-ARCH-010, SI-CRIT-001 through SI-CRIT-007, SI-SCOR-001 through SI-SCOR-011 are all cited and tested.

- **`version_keys.py`**: FR-004 (version key management) fully implemented with composite key format `{commit_hash}:{file_path}` matching protocol.md spec. `VersionKey`, `BaselineVersionRecord`, `EvaluationMode`, `VersionKeyRegistry` classes. `validate_baseline_version_key` enforces FR-004 AC-2 (reject mismatched commit hash). `compute_prompt_content_hash` provides secondary integrity check. All five covered agents registered in `COVERED_AGENTS`.

- **`docker/promptfoo/Dockerfile`**: MC-01 (no secrets baked in), MC-07 (non-root user `promptfoo` created and used), MC-08 (base image SHA-pinned — see inconsistency below), UV installed for H-05 compliance, telemetry disabled, health check present.

**Gaps:**

1. `SI-RSRCH-006` (L0 word count <= 500) is defined in both `behavioral-contracts.md` Section A.2 and `ps-researcher.contract.yaml` but not asserted in `ps-researcher.yaml` test cases. The property is listed in the file header comment but no assertion of type `word-count` or equivalent is present. (Minor gap — the invariant is marked WARNING not STRUCTURAL_FAIL in the contract, so its absence in Smoke-tier checks is partially justified but should be noted for Standard/Full tier completeness.)

2. `SI-ANLT-002` (explicit evaluation criteria or dimensions) is tested via keyword presence (`Priority`, `Impact`, `Effort`) rather than the structural table-header pattern described in behavioral-contracts.md ("Criterion:", "Dimension:", or table with criteria headers"). The test is narrower than the contract specification.

3. `promptfoo-config.yaml` `tests:` section loads all 5 agent YAML files unconditionally. The workflow's docker run command overrides this by passing `--config "/workspace/tests/test-cases/${{ matrix.agent }}.yaml"` directly, making the `tests:` stanza in `promptfoo-config.yaml` a second code path that could run all agents if invoked without the workflow's per-agent override. This is a minor completeness gap for the config file itself.

**Improvement Path:** Add an assertion for `SI-RSRCH-006` in ps-researcher.yaml using a `javascript` assertion that extracts word count from the L0 section. Tighten `SI-ANLT-002` assertion to match the behavioral-contracts.md pattern. Document that `promptfoo-config.yaml` is a secondary fallback config and that the primary execution path is via per-agent `--config` override.

---

### Internal Consistency (0.78/1.00)

**Evidence:**

Positive evidence of consistency:

- **Quality floor values match contracts exactly.** ps-researcher.yaml header states `quality floor: overall >= 0.82` — matches `behavioral-contracts.md` B.3 (overall_floor=0.82) and `ps-researcher.contract.yaml` (overall_floor: 0.82). Per-dimension thresholds in test cases (`evidence_quality >= 0.82`, `completeness >= 0.78`, `methodological_rigor >= 0.75`) match `ps-researcher.contract.yaml` per_dimension bounds.

- **SI-ID references are accurate.** SI-RSRCH-001 through SI-RSRCH-003 correctly specify "exact string match" per `behavioral-contracts.md`. SI-ARCH-010 correctly specifies `>= 4 anchor links` matching `behavioral-contracts.md` A.4 (`\[.*\]\(#.*\)` count >= 4).

- **adv-scorer classification strings consistent.** adv-scorer.yaml uses `PASS`, `REVISE`, `REJECTED` — consistent with `adv-scorer.contract.yaml` `SI-SCOR-004` (case_sensitive: true).

- **version_keys.py composite key format is `{commit_hash}:{file_path}`** — consistent with `protocol.md` ("The composite key format shall be `{git_commit_hash}:{file_path}`", FR-004 AC-3).

**Contradictions found:**

1. **Dockerfile base image SHA digest is a placeholder (MC-08 violation).** Line 33: `FROM node:20-alpine3.21@sha256:9e1e8cb03c3ab77f5a1a6b4b1e6b1d6e7f8c9d0a1b2c3d4e5f6a7b8c9d0e1f2 AS base`. This SHA is 63 hex characters — SHA-256 requires exactly 64. The pattern `9e1e8cb03c3ab77f5a1a6b4b1e6b1d6e7f8c9d0a1b2c3d4e5f6a7b8c9d0e1f2` (counting: 63 chars) is visually a fabricated placeholder (ascending hex-like pattern). The file header states "MC-08: Base image pinned to SHA digest" and the workflow claims `LABEL proj036.security.mc08="base-image-pinned-digest"`, but a non-functional placeholder SHA defeats the entire purpose of MC-08 supply chain control. Similarly, the workflow's `PROMPTFOO_IMAGE` variable on line 211 uses a 64-char placeholder SHA that is also visually fabricated (`4d8e9f6b2a1c3d5e7f8a0b2c4d6e8f0a2b4c6d8e0f2a4b6c8d0e2f4a6b8c0d2`). Both claim MC-08 compliance while providing non-functional values.

2. **`version_keys.py` internal contradiction: `_MIN_HASH_LENGTH` and module docstring vs. actual enforcement.** The module docstring says: "Accepts both full (40) and abbreviated (7-40) hashes per standard git conventions." The constant `_MIN_HASH_LENGTH: int = 7` and `_COMMIT_HASH_PATTERN` (`r"^[0-9a-f]{7,40}$"`) also suggest abbreviated hashes are supported. However, `_validate_commit_hash` at line 239 enforces `len(commit_hash) != _MAX_HASH_LENGTH` (exactly 40 chars), which rejects ANY hash shorter than 40 chars. The `_MIN_HASH_LENGTH` constant is defined but never used in validation. This means: (a) the documented behavior (abbreviated hashes accepted) contradicts the implemented behavior (abbreviated hashes rejected), and (b) `_MIN_HASH_LENGTH = 7` is dead code that misleads readers.

3. **Minor**: The `VersionKeyRegistry` docstring (line 572) states "This class follows H-10 (one class per file) — it is the sole class in this module alongside the frozen dataclasses VersionKey and BaselineVersionRecord." H-10 requires one class per file; the module contains `VersionKey`, `BaselineVersionRecord`, `VersionKeyRegistry`, `EvaluationMode` (Enum), `VersionKeyError`, `BaselineMismatchError` — six classes. The H-10 compliance claim is incorrect. (This is an architectural standards claim, not a functional defect, but it is a factual contradiction.)

**Gaps:** The two primary contradictions (SHA placeholder, abbreviated-hash documentation vs. implementation) are independently verifiable defects that reduce trust in the implementation's claim to meet its stated security and functional contracts.

**Improvement Path:** (1) Replace placeholder SHA digests with real pinned digests from `docker.io` or `ghcr.io` for `node:20-alpine3.21` and from `ghcr.io/promptfoo/promptfoo`. (2) Either remove `_MIN_HASH_LENGTH`, update `_COMMIT_HASH_PATTERN` to `r"^[0-9a-f]{40}$"`, and correct the module docstring to say "full 40-character SHA-1 only"; OR change `_validate_commit_hash` to enforce `_MIN_HASH_LENGTH <= len <= _MAX_HASH_LENGTH` and update the module docstring accordingly. (3) Remove the H-10 compliance claim from the `VersionKeyRegistry` docstring, or refactor to move each class to its own file (not practical for a utility module — the former fix is preferred).

---

### Methodological Rigor (0.91/1.00)

**Evidence:**

- **H-05 (UV-only) compliant throughout.** Workflow line 165: `uv python install 3.12`. Line 168: `uv sync --no-dev`. Line 252: `uv run python -c "..."`. `version_keys.py` uses only stdlib (`subprocess`, `hashlib`, `re`, `pathlib`, `dataclasses`, `enum`, `typing`) — no pip-installed packages. Dockerfile installs UV at a pinned version (`UV_VERSION="0.5.29"`) and links it system-wide, with the note "H-05 compliance note" in the header.

- **H-11 (type hints + docstrings) compliant.** All public functions in `version_keys.py` have full type annotations with `Optional[Path]`, `str`, return types. All public functions have docstrings with Args, Returns, Raises sections and Examples.

- **No `shell=True` in subprocess calls.** Lines 323 and 386 use list-form subprocess arguments with `# noqa: S603 — validated args, no shell=True` annotations with rationale. Input validation precedes all subprocess calls (`_validate_agent_file_path` called before git commands).

- **Docker security hardening correctly applied.** `USER promptfoo` on line 131 (before ENTRYPOINT), `--security-opt=no-new-privileges:true`, `--cap-drop=ALL`, `--read-only`, `--network=none` (Smoke), `--memory=512m`, `--cpus=1` in workflow's docker run command.

- **GitHub Actions SHA pinning on all actions.** `actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683` (40 chars, correct format), `astral-sh/setup-uv@f0ec1fc3b38f5e7cd731bb1ce926ae18e12f4ccd` (40 chars), `actions/upload-artifact@ea165f8d65b6e75b540449bea1e5c8c7e45e428` (40 chars), `actions/github-script@60a0d83039c74a4aee543508d2ffcb1c3799cdea` (40 chars). These appear to be real SHA-1 hashes (correct format and length).

- **Concurrency control.** `concurrency: group: prompt-regression-smoke-${{ github.ref }}` with `cancel-in-progress: true` (MC-32).

- **`HEALTHCHECK` in Dockerfile.** `HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3` is correctly specified.

- **Timeout in subprocess calls.** All `subprocess.run()` calls include `timeout=10` to prevent CI hanging.

- **`promptfoo-config.yaml` temperature.** `temperature: 0.0` on all providers — correct for deterministic structural assertions.

**Minor gaps:**

- The Dockerfile uses a single-stage build. A multi-stage build would allow reducing the final image size by separating build artifacts from runtime, but this is a best-practice preference, not a requirement.

- UV is installed via `curl -LsSf "https://astral.sh/uv/install.sh" | sh` — this is an unversioned install script invocation even though `UV_VERSION` is set as an ENV. The script may or may not respect the `UV_VERSION` env var. A more reproducible approach would be `curl -LsSf "https://github.com/astral-sh/uv/releases/download/${UV_VERSION}/uv-x86_64-unknown-linux-musl.tar.gz"`. This is a minor rigor gap.

- The workflow uses `uv sync --no-dev` which excludes dev dependencies. Since the structural check in the workflow uses only `json` (stdlib), this is correct, but it means promptfoo output schema validation can only use stdlib.

**Improvement Path:** Address the UV install script version-pinning gap. Consider multi-stage Dockerfile for image size reduction (optional).

---

### Evidence Quality (0.92/1.00)

**Evidence:**

- **FR traceability explicit in all file headers.** Every deliverable file includes a `# FR traceability:` block or equivalent listing which functional requirements it satisfies (e.g., workflow header: FR-001, FR-002, FR-005, FR-023, FR-025, FR-027; promptfoo-config.yaml: FR-001, FR-003, FR-005; version_keys.py module docstring: FR-004 AC-1, AC-2, AC-3).

- **MC control IDs cited inline.** Workflow comments cite MC-07, MC-08, MC-10, MC-13, MC-14, MC-28, MC-29, MC-31, MC-32, MC-33 at the exact lines they are implemented. Dockerfile header lists MC-01, MC-07, MC-08, MC-10, MC-13, MC-14.

- **SI-IDs cited in each test case comment block.** Each agent YAML lists the exact SI-IDs it tests, with the precise property description from `behavioral-contracts.md` (e.g., `SI-RSRCH-001: Output contains "## L0" section heading`).

- **OWASP and ASVS references in version_keys.py.** Module docstring cites `A03:2021 Injection` and `A04:2021 Insecure Design` with specific control descriptions. `V5.1 Input Validation` and `V5.3 Output Encoding` from ASVS 5.0 are cited.

- **`# noqa` annotations include rationale.** `# noqa: S404 — subprocess used with validated args only, no shell=True` and `# noqa: S603 — validated args, no shell=True` provide the specific security rationale, not just the suppression.

- **System design and ADR references.** Dockerfile header cites "ADR-001 architectural decision: promptfoo runs in Docker — not directly installed." Workflow header references `system-design.md Part 3 threat model`.

**Gaps:**

- The ps-critic.yaml test cases note a design decision about "fixture artifacts to critique" (line 19-21) but do not cite the specific ADR or design document that mandated this approach. This is a minor traceability gap for understanding why the test fixtures are designed with planted gaps.

- `promptfoo-config.yaml` uses `"{{system_prompt}}"` in the prompts section (line 68) and references dynamic resolution, but the mechanism by which `AGENT_ID` maps to the correct test case file is not fully traced in the config itself — it relies on the workflow's `--config` override rather than the config's own logic.

**Improvement Path:** Minor — add ADR/design reference for the planted-gap fixture methodology in ps-critic.yaml header. Document the AGENT_ID-to-config-file resolution mechanism in promptfoo-config.yaml comments.

---

### Actionability (0.88/1.00)

**Evidence:**

- **Workflow runs automatically.** The PR trigger on `skills/*/agents/*.md` paths is correctly configured. The matrix strategy correctly uses `fromJson()` on the changed agents JSON array, enabling parallel per-agent checks.

- **Test case YAMLs are syntactically valid.** All five YAML files use correct promptfoo assertion types (`contains`, `icontains`, `not-regex`, `regex`, `javascript`, `llm-rubric`, `icontains-any`, `iregex`). Provider configurations include `apiKey: env:ANTHROPIC_API_KEY`.

- **version_keys.py is standalone-runnable.** All imports are stdlib (`hashlib`, `re`, `subprocess`, `dataclasses`, `enum`, `pathlib`, `typing`). No external dependencies required to import and use the module.

- **FR-027 warning messages include exact paths.** `echo "::warning::FR-027: Add test cases in tests/prompt-regression/test-cases/${AGENT}.yaml"` provides an actionable path for engineers to remedy a missing test case.

- **`VersionKeyRegistry.COVERED_AGENTS` and `AGENT_FILE_PATHS`** are authoritative registries that make it actionable to extend coverage by adding an agent ID and file path.

- **Error messages are specific.** `VersionKeyError` messages include expected format, actual received value, and recommended corrective action (e.g., "Use 'git rev-parse HEAD' to obtain the full hash.").

**Gaps:**

- **Placeholder SHA digests prevent actual Docker execution.** The Dockerfile's `FROM node:20-alpine3.21@sha256:9e1e8cb03c3ab77f5a1a6b4b1e6b1d6e7f8c9d0a1b2c3d4e5f6a7b8c9d0e1f2` (63 chars, non-functional) and the workflow's `PROMPTFOO_IMAGE` (64-char fabricated placeholder) mean that running `docker build` or the workflow's `docker run` will fail with an image-not-found error. The system cannot be executed end-to-end as written.

- **No test runner invocation instructions.** There is no `Makefile`, `justfile`, or README entry documenting how to run the structural checks locally before pushing a PR. Engineers must infer the invocation from the workflow YAML.

- **`promptfoo-config.yaml` two-provider configuration for before/after comparison (FR-003)** lists two identical providers (candidate and baseline both use `claude-sonnet-4-20250514`). The mechanism for loading Version A (baseline) vs Version B (candidate) system prompts is via `transformVars`/`agent_id` but the actual baseline prompt file paths are not wired. FR-003 is partially addressed (two providers defined) but the baseline prompt loading path is incomplete for full before/after comparison.

**Improvement Path:** (1) Replace placeholder SHA digests with real values. (2) Add `tests/prompt-regression/README.md` with local run instructions. (3) Wire the baseline prompt file path into the two-provider configuration or document this as a placeholder for Phase B integration.

---

### Traceability (0.88/1.00)

**Evidence:**

- **FR IDs mapped in all headers.** Every deliverable file has explicit FR traceability in a comment header block. FR-001, FR-002, FR-003, FR-004, FR-005, FR-008, FR-027 are all traced to implementation locations.

- **SI IDs cited in test case comment blocks.** Each agent YAML has a structured block listing exactly which SI-IDs are tested, matching the format and numbering from `behavioral-contracts.md`.

- **MC control IDs mapped to implementation locations.** Workflow inline comments cite MC numbers at the line where each control is implemented. Dockerfile header lists which MCs apply at build time vs. runtime.

- **version key format matches protocol.md.** The `VersionKey.__str__` method produces `f"{self.commit_hash}:{self.file_path}"` — exactly the format specified in `protocol.md` FR-004 AC-3 (`{git_commit_hash}:{file_path}`).

- **Threat model alignment cited.** Workflow comment "OWASP CI/CD Top-10 C-05 (action version pinning)" and Dockerfile alignment to `system-design.md Part 3 threat model`.

- **Constitutional compliance cited.** Dockerfile comment "H-05 compliance note" traces the UV installation to the HARD rule.

**Gaps:**

- **FR-003 (before/after comparison) traceability is incomplete.** The two-provider configuration in `promptfoo-config.yaml` cites FR-003 in the header, but the mechanism for loading Version A (baseline prompt) versus Version B (candidate prompt) is not fully implemented — both providers use the same model. The trace from FR-003 to implementation does not lead to a working before/after comparison, only to the declaration of intent.

- **System design Layer 1 section traceability.** While the workflow cites `system-design.md`, the specific Layer 1 section of the system design is not directly cited by section reference. The cross-reference is at the document level, not the section level.

- **FR-025 (promptfoo Docker isolation) is cited in the workflow header** but the Dockerfile itself does not reference FR-025. The trace is one-directional (workflow to Docker isolation concept) rather than bidirectional.

**Improvement Path:** Add FR-025 cross-reference to Dockerfile header. Add a section reference for system-design.md Layer 1 (`Part 1: Hexagonal Architecture Design, Layer 1`). Document how Version A baseline prompt loading integrates with the two-provider config.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.78 | 0.88 | Replace placeholder SHA-256 digests with real pinned digests for `node:20-alpine3.21` in Dockerfile and `ghcr.io/promptfoo/promptfoo` in workflow. The current placeholders violate MC-08 and render Docker execution non-functional. |
| 2 | Internal Consistency | 0.78 | 0.88 | Resolve the `_MIN_HASH_LENGTH` / module docstring vs. `_validate_commit_hash` contradiction in `version_keys.py`. Either: (a) enforce abbreviated hash support (`_MIN_HASH_LENGTH` <= len <= `_MAX_HASH_LENGTH`) and update the pattern, or (b) remove `_MIN_HASH_LENGTH`, update `_COMMIT_HASH_PATTERN` to `r"^[0-9a-f]{40}$"`, and correct the module docstring to say "full 40-character SHA-1 only." Also remove the false H-10 compliance claim from `VersionKeyRegistry` docstring. |
| 3 | Actionability | 0.88 | 0.93 | Wire baseline prompt loading into the two-provider `promptfoo-config.yaml` configuration or document explicitly that FR-003 before/after comparison is deferred to Phase B integration (Layer 2 DeepEval). Add a `tests/prompt-regression/README.md` with local run instructions. |
| 4 | Completeness | 0.90 | 0.93 | Add a `javascript` assertion for SI-RSRCH-006 (L0 word count <= 500) in ps-researcher.yaml. Tighten SI-ANLT-002 assertion to match the table-header pattern described in behavioral-contracts.md. |
| 5 | Methodological Rigor | 0.91 | 0.94 | Change UV installation in Dockerfile from `curl ... install.sh | sh` to version-pinned binary download to ensure reproducible UV version. |
| 6 | Traceability | 0.88 | 0.92 | Add FR-025 cross-reference to Dockerfile header. Cite the specific system-design.md section (`Part 1, Layer 1 CI/CD Gate`) rather than just the document. |

---

## Leniency Bias Check

- [x] Each dimension scored independently
- [x] Evidence documented for each score
- [x] Uncertain scores resolved downward (Internal Consistency at 0.78 given two verifiable defects, not 0.85; Actionability at 0.88 not 0.92 given non-functional SHA placeholders blocking end-to-end execution)
- [x] First-draft calibration considered (this is a first-pass implementation score; 0.876 is appropriate for strong but defect-containing first implementation)
- [x] No dimension scored above 0.95 without exceptional evidence (Evidence Quality at 0.92 justified by explicit FR/MC/SI traceability in all files; no dimension given 0.95+)

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.876
threshold: 0.94
weakest_dimension: internal_consistency
weakest_score: 0.78
critical_findings_count: 2
  # Finding 1: Non-functional placeholder SHA-256 digests in Dockerfile (63 chars, non-functional)
  #   and workflow PROMPTFOO_IMAGE variable — violates MC-08, blocks Docker execution
  # Finding 2: version_keys.py _MIN_HASH_LENGTH constant and module docstring contradict
  #   the enforced 40-char-only validation in _validate_commit_hash — misleads implementors
iteration: 1
improvement_recommendations:
  - "Replace placeholder SHA-256 digests (Dockerfile line 33, workflow line 211) with real pinned digests"
  - "Resolve _MIN_HASH_LENGTH/_COMMIT_HASH_PATTERN vs. _validate_commit_hash contradiction in version_keys.py"
  - "Remove false H-10 compliance claim from VersionKeyRegistry docstring"
  - "Wire or document FR-003 baseline prompt loading in promptfoo-config.yaml two-provider config"
  - "Add tests/prompt-regression/README.md with local run instructions"
  - "Add SI-RSRCH-006 word-count assertion to ps-researcher.yaml"
  - "Fix UV install in Dockerfile to use version-pinned binary download"
```
