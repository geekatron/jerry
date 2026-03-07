# Quality Score Report: Stream 3E — CI/CD Pipeline Setup

## L0 Executive Summary

**Score:** 0.848/1.00 | **Verdict:** REJECTED | **Weakest Dimension:** Completeness (0.82)

**One-line assessment:** The CI/CD pipeline is structurally sound and securely designed, but three concrete gaps block acceptance: (1) FR-023 HARD violation — raw `python3` used in composite actions instead of `uv run python`, (2) internal FR-027 contradiction — smoke workflow job 1 says warning-only but job 2 exits non-zero on missing test YAML, and (3) cost-monitor header documents "$20 Full" while the full workflow sets $50, an undocumented inconsistency. Fix all three before re-scoring.

---

## Scoring Context

- **Deliverable:** `.github/workflows/prompt-regression-smoke.yml`, `.github/workflows/prompt-regression-standard.yml`, `.github/workflows/prompt-regression-full.yml`, `.github/actions/cost-monitor/action.yml`, `.github/actions/artifact-publish/action.yml`, `.github/CODEOWNERS`
- **Deliverable Type:** Code (GitHub Actions CI/CD Pipeline)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Stream Threshold:** >= 0.94 PASS (stream-level, above H-13 baseline)
- **Scored:** 2026-03-07T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.848 |
| **Stream Threshold** | 0.94 (PASS) |
| **H-13 Threshold** | 0.92 (PASS) |
| **Verdict** | REJECTED |
| **Strategy Findings Incorporated** | No — standalone scoring |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.82 | 0.164 | 3 tiers + 2 actions present; FR-023 violated in both actions (raw `python3`); FR-027 smoke tier behavior contradicts spec |
| Internal Consistency | 0.20 | 0.83 | 0.166 | N values, permissions, action pins all consistent; cost-monitor header says "$20 Full" but full workflow sets $50 |
| Methodological Rigor | 0.20 | 0.86 | 0.172 | All key MC controls (MC-07, MC-08, MC-25, MC-28, MC-29, MC-31, MC-32, MC-33) implemented; H-05 violated in composite actions |
| Evidence Quality | 0.15 | 0.84 | 0.126 | FR + MC traceability in all 6 file headers; inline rationale throughout; Docker SHA appears to be a placeholder digest |
| Actionability | 0.15 | 0.87 | 0.131 | All three workflows are valid, executable GHA YAML; H-05 violation in actions is a compliance gap, not a runtime blocker |
| Traceability | 0.10 | 0.90 | 0.090 | Bidirectional FR + MC references in all files; Stream 3E declared; FR-019 module separation cited but not demonstrable from CI files |
| **TOTAL** | **1.00** | | **0.848** | |

---

## Detailed Dimension Analysis

### Completeness (0.82/1.00)

**Evidence:**

All three required workflow tiers are present and structurally complete:
- Smoke: `pull_request` trigger on `skills/*/agents/*.md`, N=0 LLM calls, structural Docker execution with `--network=none`, labeled "STRUCTURAL ONLY — not statistically valid" (FR-005 AC met)
- Standard: `pull_request` + `workflow_dispatch`, N=10 (`N_RUNS_PER_VERSION: "10"`), LLM API key injected, Wilcoxon statistical analysis via `jerry.testing.layer4_stats` (FR-003, FR-015, FR-016, FR-017, FR-018)
- Full: `workflow_dispatch` + `push: tags: v*.*.*` + `schedule: cron "0 2 * * 1"`, N=30, baseline store update logic, model migration mode (FR-028)

Both composite actions are present with complete input/output interfaces:
- cost-monitor: start/stop phases, MC-20 ceiling enforcement, MC-37 audit trail
- artifact-publish: tier-aware retention (7/30/90 days), auto-discovery, PR comment integration (FR-018, MC-30)

CODEOWNERS covers `.github/workflows/`, `.github/actions/`, `jerry/testing/`, `tests/prompt-regression/`, `baselines/`, `contracts/`, `skills/*/agents/*.md`, `docs/governance/`, `.context/rules/`, `CLAUDE.md` (MC-29 satisfied).

**Gaps:**

1. **FR-023 HARD violation (H-05):** Both composite actions use raw `python3` in bash steps, not `uv run python`. Specific locations:
   - `cost-monitor/action.yml` lines 128–148 (token count extraction), 160–167 (cost estimation), 202–209 (token ceiling check), 219–226 (cost ceiling check), 252–268 (structured record write)
   - `artifact-publish/action.yml` lines 266–306 (metadata generation), 435–443 (verdict extraction for step summary)

   FR-023 acceptance criteria: "All GitHub Actions workflow steps that invoke Python shall use `uv run pytest` or `uv run python`." The three main workflow files correctly use `uv run python`. The composite actions do not. FR-023 is a Must requirement.

2. **FR-027 internal contradiction:** The smoke workflow presents conflicting behavior for missing test YAML:
   - Job 1 (`detect-changed-agents`, step `check-test-authorship`) produces a `::warning::` annotation and sets `has_missing_tests=true` — correctly non-blocking
   - Job 2 (`smoke-structural-check`, step `validate-test-case-yaml-exists`) calls `exit 1` on missing YAML, making the per-agent smoke check a hard failure

   FR-027 specifies: "a warning annotation (not a blocking failure, to avoid over-enforcement for trivial changes)." The `exit 1` in job 2 is a blocking failure. The workflow header comment says "FR-027: Test case authorship enforcement (CI warning, not blocking)" which contradicts the actual behavior.

3. **FR-025 Docker SHA placeholder:** The promptfoo image SHA used across all three workflows (`sha256:4d8e9f6b2a1c3d5e7f8a0b2c4d6e8f0a2b4c6d8e0f2a4b6c8d0e2f4a6b8c0d2`) shows a strongly sequential hex pattern (4d8e, 9f6b, 2a1c, 3d5e, etc.) inconsistent with real cryptographic digests. If this is a placeholder rather than an actual pinned image digest, FR-025 AC ("Docker image version shall be pinned in the workflow YAML") is formally met but not substantively — the pin references a non-existent image.

**Improvement Path:**

- Replace all `python3` with `uv run python` in both composite actions. Add `uv run` setup steps to the composite action if not already available from the calling workflow context (composite actions inherit the calling job's environment, so `uv` should be available after the Install UV step in the caller).
- Decide the authoritative FR-027 behavior: warning-only or blocking. Update both jobs to match. The requirements say warning-only, so job 2 should downgrade the `exit 1` to a `::warning::` and exit 0.
- Replace the placeholder Docker SHA with the actual published digest for the target promptfoo version (e.g., from `docker manifest inspect ghcr.io/promptfoo/promptfoo:latest --format '{{json .}}'`).

---

### Internal Consistency (0.83/1.00)

**Evidence:**

Consistent across all six files:
- N values: smoke=0 LLM (structural), standard=10, full=30 — all env vars match the tier
- Permission blocks: identical `contents: read`, `pull-requests: write`, `checks: write` in all three workflows (MC-33)
- Action version pins: `actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683` (v4.2.2), `astral-sh/setup-uv@f0ec1fc3b38f5e7cd731bb1ce926ae18e12f4ccd` (v5.4.1), `actions/upload-artifact@ea165f8d65b6e75b540449bea1e5c8c7e45e428` (v4.6.2), `actions/github-script@60a0d83039c74a4aee543508d2ffcb1c3799cdea` (v7.0.1) — all consistent
- `QUALITY_PASS_THRESHOLD: "0.92"` in both standard and full — aligned with H-13
- `STATISTICAL_ALPHA: "0.05"` in both standard and full — consistent
- `HARNESS_MODEL_VERSION: "claude-sonnet-4-20250514"` in both standard and full — consistent
- ANTHROPIC_API_KEY: not present in smoke (MC-25 / MC-31), present in standard and full — consistent and intentional
- Docker SHA: same hash used in all three main workflows — consistent (even if potentially placeholder)
- Concurrency: smoke uses `${{ github.ref }}` suffix, standard uses `${{ github.ref }}` suffix, full uses no suffix with `cancel-in-progress: false` — appropriate semantic differences, not an inconsistency

**Gaps:**

1. **Cost ceiling inconsistency between action documentation and workflow configuration:**
   - `cost-monitor/action.yml` header comment (line 27): `MC-20: Per-workflow budget ceiling ($5 Standard, $20 Full)`
   - `prompt-regression-full.yml` env var (line 122): `COST_CEILING_USD: "50.00"` with comment "Full tier: N=30 x 5 agents x ~$5-8 per agent = up to $40 under normal conditions. $50 ceiling provides safety margin"
   - The discrepancy: $20 (action header) vs. $50 (full workflow). This is not an innocuous typo — the action header is authoritative documentation of what the control provides. A reviewer reading the action file would believe the ceiling is $20; the actual ceiling is $50.

2. **FR-027 behavior inconsistency within smoke.yml** (also noted under Completeness): Job 1 produces non-blocking warning, Job 2 produces blocking exit 1. Both claim to implement FR-027. The contradiction means the workflow's behavior depends on which job is inspected.

**Improvement Path:**

- Update `cost-monitor/action.yml` header comment to accurately document the tier ceilings as passed by callers: "$5 Standard, $50 Full" (or make the ceilings tier-aware within the action itself, not just passed as inputs).
- Resolve the FR-027 contradiction: pick one behavior and apply it consistently to both jobs in smoke.yml.

---

### Methodological Rigor (0.86/1.00)

**Evidence:**

MC security controls are implemented with strong coverage:

- **MC-07 (Docker read-only + cap-drop + path restriction):** All three workflows use `--read-only`, `--security-opt=no-new-privileges:true`, `--cap-drop=ALL`, read-only volume mounts (`:ro`), tmpfs for writable temp space. Resource limits scale appropriately by tier (smoke: 512m/1CPU, standard: 2g/2CPU, full: 4g/4CPU).
- **MC-08 (digest pinning):** `ghcr.io/promptfoo/promptfoo@sha256:...` format in all three workflows.
- **MC-09 (output validation):** Post-evaluation JSON validation steps in all three workflows using `uv run python -c`.
- **MC-25 (API key injection control):** Smoke explicitly excludes API key with comment "ANTHROPIC_API_KEY is intentionally NOT injected in Smoke tier." Standard and full inject via `env:` block with masked handling.
- **MC-28 (pull_request not pull_request_target):** Verified — smoke uses `pull_request`, standard uses `pull_request` and `workflow_dispatch`. Full does not use `pull_request` at all (manual + schedule + tag push). None use `pull_request_target`.
- **MC-29 (CODEOWNERS):** `.github/CODEOWNERS` covers all workflow and action paths. References OWASP CI/CD Top-10 C-09 and CIS GitHub Benchmark.
- **MC-31 (secret masking):** Standard and full workflows use `::add-mask::${{ secrets.ANTHROPIC_API_KEY }}` with defense-in-depth rationale documented.
- **MC-32 (concurrency):** All three workflows define concurrency groups. Full tier uses `cancel-in-progress: false` — correct because Full tier runs are expensive and should not be cancelled mid-run.
- **MC-33 (minimal permissions):** Consistent minimal permission blocks in all three workflows.
- **Pinned action versions:** All four external actions SHA-pinned with version comments.
- **Fork isolation (MC-28):** Standard workflow detects fork PRs via `github.event.pull_request.head.repo.fork` and falls back to smoke-only with an explanatory PR comment.
- **FR-004 (version key management):** Standard workflow captures base and head SHAs, passes to `layer4_stats.py` via env vars.
- **workflow_dispatch inputs:** Standard and full workflows have well-structured inputs with descriptions and defaults.

**Gaps:**

1. **H-05 (UV-only) violation in composite actions:** Both `cost-monitor/action.yml` and `artifact-publish/action.yml` use `python3` directly in bash steps. The main workflow steps correctly use `uv run python`. The composite actions do not. This is a methodological standards violation affecting two of the six deliverable files. FR-023 is classified Must. H-05 is HARD. This is the most significant methodological gap.

2. **MC-12 (single-process container, no shell):** Referenced in standard workflow header but not visibly enforced in the Docker invocation itself. The workflow uses the `eval` entrypoint command, which is promptfoo's evaluation subcommand. MC-12 implementation is supposed to be in a custom Dockerfile (`docker/promptfoo/Dockerfile`) per the system design, not in the workflow YAML. The workflow YAML alone cannot fully verify MC-12. This is acceptable if the Dockerfile exists, but that Dockerfile is not among the Stream 3E deliverables.

**Improvement Path:**

- Replace all `python3` invocations in both composite actions with `uv run python`. Verify that `uv` is available in the composite action execution context (it is, since composite actions inherit the calling job's PATH after the Install UV step runs).
- Document that MC-12 relies on the `docker/promptfoo/Dockerfile` (a Stream 3B deliverable) and add a cross-reference comment to the workflow YAML.

---

### Evidence Quality (0.84/1.00)

**Evidence:**

Every deliverable file has a structured header documenting:
- FR traceability (e.g., smoke.yml: FR-001, FR-002, FR-005, FR-023, FR-025, FR-027; full.yml: FR-002, FR-003, FR-004, FR-005, FR-010, FR-014 through FR-020, FR-023, FR-025, FR-028)
- MC control references (specific control IDs with one-line descriptions of what they implement)
- Stream assignment (Stream: 3E) in all six files

Inline documentation quality is high:
- Each Docker invocation parameter commented with its MC control (e.g., `# --read-only: Immutable container filesystem (prevents runtime tampering)`, `# --network=none: No outbound network access in Smoke mode`)
- Fork PR fallback logic explicitly comments "MC-28 fork secret isolation"
- Version A/B SHA capture comments explain FR-003 and FR-004 intent
- Cost monitor start/stop rationale documented inline
- Artifact retention policy justified in artifact-publish header (7/30/90 days by tier)
- CODEOWNERS references OWASP CI/CD Top-10 C-09 and CIS GitHub Benchmark by name

**Gaps:**

1. **Docker SHA credibility:** The promptfoo image SHA `sha256:4d8e9f6b2a1c3d5e7f8a0b2c4d6e8f0a2b4c6d8e0f2a4b6c8d0e2f4a6b8c0d2` shows a pattern of sequential hex bytes (4d8e, 9f6b, 2a1c, 3d5e, 7f8a, etc.). Real cryptographic SHA-256 digests do not exhibit this regularity. This strongly suggests a placeholder rather than an actual published image digest. If so, the evidence of "pinned to digest" (MC-08) is present in format only, not in substance. This reduces the credibility of the security evidence.

2. **FR-022 (license verification):** Not addressed in these deliverables, but FR-022 is a cross-cutting requirement. Its absence may be scope-appropriate for Stream 3E (which is CI/CD pipeline only), but there is no cross-reference to where FR-022 is delivered.

3. **MC-19 (API retry):** Referenced in standard and full workflow headers but not implemented in the workflow YAML — the header documents that the implementation is in `deepeval_adapter.py`. This is architecturally correct per the design, but the CI/CD stream cannot demonstrate MC-19 is actually implemented without access to that module.

**Improvement Path:**

- Replace placeholder Docker SHA with the actual published digest for the target promptfoo version. Document the version number alongside the digest in the comment (e.g., `# promptfoo v0.84.0, published 2026-02-15`).
- Add a comment in the workflow YAML cross-referencing FR-022 to the license verification stream (or note it as out of scope for Stream 3E).

---

### Actionability (0.87/1.00)

**Evidence:**

All six deliverable files are structurally valid and operationally actionable:

- Smoke workflow: matrix strategy correctly uses `fromJson(needs.detect-changed-agents.outputs.changed_agents)`, `fail-fast: false` ensures all agents are checked even when one fails, PR comment integration via `actions/github-script` with structured output including per-agent table.
- Standard workflow: `workflow_dispatch` inputs with descriptions and defaults enable manual trigger; `is_fork` output propagates correctly to downstream jobs; Version A capture logic handles the case where an agent is new (no base branch version) gracefully.
- Full workflow: agent list parsing handles comma-separated input correctly via `tr ',' '\n'`; model migration mode cleanly sets `is_model_migration=true` and propagates to evaluation env; baseline update gate (`REGRESSION_VERDICT == 'NO_REGRESSION' && update_baselines == 'true'`) is correctly conditional.
- cost-monitor: start/stop phase architecture cleanly separates concern; ceiling breach detection is additive (both token and cost ceilings checked independently); audit record written to step summary (MC-37) and structured JSON.
- artifact-publish: backward compatibility via `agent_id`/`agent_name` alias; auto-discovery from `results_path`; tier-aware retention via case statement; PR comment includes verdict, p-value, run link, and full markdown report.
- CODEOWNERS: 8 path rules covering the full pipeline, governance, and framework governance.

All verdict cases handled in regression gate steps: REGRESSION (exit 1), MARGINAL (warning, exit 0), NO_REGRESSION (exit 0), INSUFFICIENT_SAMPLES (warning or error depending on tier), ERROR/UNKNOWN (exit 1).

**Gaps:**

1. **H-05 violation in composite actions:** The `python3` invocations in cost-monitor and artifact-publish are a hard standards violation. They are functionally valid because `ubuntu-latest` GitHub Actions runners include Python 3. However, they violate the MUST requirement to use `uv run python`, which could break if the runner Python version differs from the project's pinned version. This is both a compliance and a potential operational risk.

2. **cost-monitor ceiling check pattern risk:** The budget ceiling check uses `python3 -c "..." 2>/dev/null | grep -q "BREACH" && { ... }`. If the Python command fails silently (the `2>/dev/null` suppresses all errors), the grep gets no input, returns non-zero, and the `&&` block is never executed — meaning ceiling breaches would be silently swallowed. The `|| echo 0` fallback in the cost calculation step mitigates this for cost computation, but not for the ceiling check itself.

3. **Version A capture edge case:** Standard workflow step "Checkout base branch agent definition (Version A)" runs `git show "origin/${{ github.base_ref }}:skills" 2>/dev/null || true` which pipes to `/dev/null` and always succeeds regardless of the result. If the origin base ref is not fetched (unlikely with `fetch-depth: 0` checkout but possible in edge cases), the step continues silently.

**Improvement Path:**

- Replace all `python3` with `uv run python` in composite actions.
- Add a fallback or error check to the cost-monitor ceiling check: if the Python command fails, emit a warning rather than silently skipping the ceiling check.

---

### Traceability (0.90/1.00)

**Evidence:**

Bidirectional traceability is present in all six deliverable files:

- All three workflow files have explicit FR traceability lists in headers, naming each FR by ID with a one-line description of how this file implements it.
- All three workflow files have explicit MC control lists in headers, referencing the system design threat model section (§3.x Attack Surface N).
- Both composite actions have FR and MC references in headers (cost-monitor: FR-005, MC-20, MC-37; artifact-publish: FR-018, MC-30, MC-37).
- CODEOWNERS references MC-29, T-29, and system-design.md §3.5 directly.
- All six files declare `Stream: 3E (CI/CD Pipeline Setup)` in their headers.
- Inline step comments reference specific MC controls throughout all workflows (not just in headers).
- The full workflow header references FR-019 (Shared Statistical Module) with the `jerry.testing.layer4_stats` invocation demonstrating the dependency.
- FR-004 (version key management) is traced to specific SHA capture steps in standard and full workflows.
- FR-027 (test case authorship) traced to specific warning steps in smoke workflow.

**Gaps:**

1. **FR-019 module architecture trace is indirect:** FR-019 specifies that `layer4_stats.py` must import from `stats.py` and not reimplement statistical logic. The CI/CD workflows invoke `jerry.testing.layer4_stats` as a module, which satisfies the invocation trace, but whether the module itself properly separates from `stats.py` (the core FR-019 AC) cannot be verified from the workflow YAML alone. The traceability claim is present but not demonstrable from these files.

2. **FR-001 (YAML test case definitions) trace is forward-referencing only:** Smoke workflow references FR-001 but the actual YAML test case files (`tests/prompt-regression/test-cases/*.yaml`) are not in this stream's deliverables. The trace is present but points to artifacts outside this stream's scope.

**Improvement Path:**

- Add inline cross-references to the stream or deliverable that implements FR-001 YAML test cases and FR-019 stats.py module (e.g., "FR-001 test case YAML: Stream 3B deliverable", "FR-019 stats.py: Stream 3C deliverable").

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness + Methodological Rigor | H-05 violation | 0.0 violations | Replace ALL `python3` with `uv run python` in `cost-monitor/action.yml` and `artifact-publish/action.yml`. Verify `uv` PATH availability in composite action context (it is — composite actions inherit caller's PATH after Install UV step). Affects ~8 bash steps across the two actions. |
| 2 | Completeness + Internal Consistency | FR-027 contradiction | Resolved | Resolve the smoke workflow FR-027 contradiction: job 2's `exit 1` on missing test YAML contradicts FR-027 ("warning, not blocking failure"). Per the requirements spec, change job 2's `exit 1` to a `::warning::` and `exit 0`. Update the workflow header comment accordingly. |
| 3 | Internal Consistency | $20/$50 discrepancy | $50 documented consistently | Update `cost-monitor/action.yml` line 27 header comment from "$20 Full" to "$50 Full". The full workflow's $50 ceiling has a justified rationale (N=30 × 5 agents × $5-8 + safety margin). The action header comment is wrong. |
| 4 | Evidence Quality | Placeholder Docker SHA | Real SHA | Replace the sequential-pattern SHA (`sha256:4d8e9f6b2a1c3d5e7f8a0b2c4d6e8f0a2b4c6d8e0f2a4b6c8d0e2f4a6b8c0d2`) with the actual published digest for the target promptfoo version. Document the version string alongside the digest in the comment. |
| 5 | Actionability | Silent ceiling check failure | Explicit failure | In `cost-monitor/action.yml`, add error handling to the Python ceiling check commands so that a Python execution failure does not silently swallow the ceiling breach detection (the `2>/dev/null` suppression is too broad). |
| 6 | Traceability | Forward-reference gaps | Explicit cross-references | Add stream cross-references to FR-001 (test case YAML: Stream 3B) and FR-019 (stats.py module: Stream 3C) in workflow headers, so traceability chains are complete without requiring readers to know the stream map. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific file locations and line references
- [x] Uncertain scores resolved downward (Completeness: chose 0.82 over 0.85 given two concrete Must-requirement gaps; Internal Consistency: chose 0.83 over 0.86 given the $20/$50 discrepancy)
- [x] First-draft calibration considered — this is a first-iteration score; the 0.848 composite is consistent with strong but gap-containing first-iteration CI/CD work
- [x] No dimension scored above 0.95 — highest is Traceability at 0.90, well-evidenced by explicit FR/MC headers in all six files
- [x] H-05 violation (HARD rule) weighted appropriately — reduces Completeness and Methodological Rigor rather than being dismissed

---

## Handoff Schema

```yaml
verdict: REJECTED
composite_score: 0.848
threshold: 0.94
weakest_dimension: Completeness
weakest_score: 0.82
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Replace python3 with uv run python in cost-monitor/action.yml and artifact-publish/action.yml (FR-023/H-05 HARD violation)"
  - "Resolve FR-027 contradiction in smoke.yml: change job 2 exit 1 to warning-only exit 0 to match requirements spec"
  - "Update cost-monitor header comment from $20 Full to $50 Full to match actual workflow ceiling"
  - "Replace placeholder Docker SHA with actual published promptfoo image digest"
  - "Add error handling to cost-monitor ceiling check to prevent silent failure swallowing ceiling breaches"
  - "Add stream cross-references in workflow headers for FR-001 (Stream 3B) and FR-019 (Stream 3C)"
```
