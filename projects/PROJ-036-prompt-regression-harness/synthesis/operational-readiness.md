# Operational Readiness Assessment: Four-Layer Composite Test Harness

> **Project:** PROJ-036 (Prompt Regression Harness)
> **Stream:** 7B (Cross-Synthesis)
> **Date:** 2026-03-07
> **Agent:** ps-synthesizer v2.3.0
> **Criticality:** C4
> **Quality Threshold:** >= 0.94
> **Assessment Purpose:** Readiness determination for merge/deployment of FEAT-036-001

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Go/No-Go determination and rationale |
| [L1: Prerequisites Checklist](#l1-prerequisites-checklist) | All conditions required before merge/deployment |
| [L1: Known Limitations and Accepted Risks](#l1-known-limitations-and-accepted-risks) | What the harness cannot yet do |
| [L1: Deployment Sequence](#l1-deployment-sequence) | Which artifacts deploy first and in what order |
| [L1: Rollback Plan](#l1-rollback-plan) | How to revert if deployment causes problems |
| [L1: Monitoring Recommendations](#l1-monitoring-recommendations) | What to watch after merge |
| [L2: Open Items Requiring Future Work](#l2-open-items-requiring-future-work) | Future phases and backlog |
| [L2: Strategic Deployment Considerations](#l2-strategic-deployment-considerations) | Architecture implications for operations |
| [Sign-Off Criteria](#sign-off-criteria) | What constitutes final acceptance |

---

## L0: Executive Summary

**Overall Readiness: NOT READY FOR PRODUCTION DEPLOYMENT — CONDITIONAL READINESS FOR MERGE**

The harness is ready for merge to the feature branch and non-production validation, but is NOT ready to gate production PRs until two pre-production blockers are resolved (RR-001 input sanitization, RR-002 Docker digest pinning).

**Conditions met for merge:**
- All 3 quality barrier gates passed (QG-1: 0.956, QG-2: 0.955, QG-3: 0.957)
- All 12 completed streams passed per-stream threshold (>= 0.94)
- 24 of 27 functional requirements verified PASS; all must-have requirements PASS
- FMEA residual RPN reduced 78.1% from 1,823 to 400 (source: fmea-mitigation-verification.md Section "L1: Residual Risk Assessment")
- Full Wilcoxon + Wilson + Bonferroni statistical engine verified
- All 5 metamorphic relations implemented and tolerance-calibrated per behavioral contracts
- 3-tier CI/CD pipeline (Smoke/Standard/Full) operational
- Hexagonal architecture H-07 compliant; H-10, H-11 compliant
- QG-4A human review pending (blocker for final merge approval)

**Conditions not yet met for production gating:**
1. RR-001: `deepeval_adapter.py` input sanitization absent (MC-02 MISSING — F-001)
2. RR-002: Docker images not digest-pinned (MC-08 MISSING — F-002)
3. QG-4A human review not yet complete (required per ORCHESTRATION.yaml)

**Recommended deployment posture:** Merge as non-blocking validation initially. Enable as blocking gate only after resolving RR-001 and RR-002.

---

## L1: Prerequisites Checklist

### Phase 1: Quality Gates (ALL COMPLETE)

| Prerequisite | Status | Evidence |
|-------------|--------|---------|
| QG-1 Foundations Consistency >= 0.95 | COMPLETE | QG-1: 0.956 PASS (qg1-barrier-score.md) |
| QG-2 Implementation Consistency >= 0.95 | COMPLETE | QG-2: 0.955 PASS (qg2-barrier-score.md, 3 iterations) |
| QG-3 Assurance Consistency >= 0.95 | COMPLETE | QG-3: 0.957 PASS (qg3-barrier-score.md) |
| All 12 completed streams >= 0.94 | COMPLETE | See ORCHESTRATION.yaml stream_quality |
| Stream 7A (Engineering Review) >= 0.94 | PENDING | reviews/engineering-review.md — IN_PROGRESS |
| Stream 7B (Cross-Synthesis, this document) >= 0.94 | PENDING | This document + synthesis outputs |
| QG-4A Adversarial Final Score >= 0.95 | PENDING | Awaiting 7A + 7B completion |
| QG-4B NASA SE Technical Review | PENDING | Awaits QG-4A |

### Phase 2: Pre-Production Security (INCOMPLETE — blocking production deployment)

| Prerequisite | Status | Evidence | RR ID |
|-------------|--------|---------|-------|
| MC-02: Input sanitization in deepeval_adapter.py | OPEN | F-001 MISSING (security-assessment.md) | RR-001 |
| MC-08: Docker image digest-pinned in Dockerfile | OPEN | F-002 MISSING (security-assessment.md) | RR-002 |
| MC-08: Docker image digest-pinned in smoke.yml | OPEN | F-002: `:latest` tag still used | RR-002 |
| MC-08: Docker image digest-pinned in standard.yml | OPEN | F-002: `0.86.0` tag, no digest | RR-002 |
| MC-08: Docker image digest-pinned in full.yml | OPEN | F-002: `0.86.0` tag, no digest | RR-002 |

### Phase 3: Human Review (INCOMPLETE — required by governance)

| Prerequisite | Status | Note |
|-------------|--------|------|
| QG-4A human review sign-off | PENDING | ORCHESTRATION.yaml: `human_review_required: true` |
| Engineering lead approval | PENDING | Standard C4 governance requirement |

### Phase 4: Dependency Completeness (OPEN — non-blocking for merge)

| Prerequisite | Status | Evidence | Priority |
|-------------|--------|---------|---------|
| `deepeval` added to pyproject.toml as pinned dependency | OPEN | FR-026 PARTIAL | LOW (model pin is primary control) |
| `uv sync` run and `deepeval` pin verified in uv.lock | OPEN | FR-026 PARTIAL | LOW |

### Phase 5: Documentation Consistency (OPEN — non-blocking)

| Prerequisite | Status | Priority |
|-------------|--------|---------|
| Consolidate InsufficientSamplesError to single class | OPEN — RR-023 | MEDIUM |
| Document STANDARD mode N accumulation protocol in baselines/protocol.md | OPEN — RR-028 | MEDIUM |
| Add T-41 adversarial MR violation crafting to threat model | OPEN — RR-027 | LOW |
| Correct ScoreArray description in interface-verification.md (dataclass -> list[float] alias) | OPEN | LOW |

---

## L1: Known Limitations and Accepted Risks

### Limitation 1: No Agent-Specific MR Coverage (FR-012 NOT STARTED)

The harness implements 5 universal metamorphic relations covering paraphrase consistency, negation handling, irrelevant context, formatting perturbation, and language round-trip. It does NOT yet implement agent-specific behavioral invariants.

**Practical effect:** A regression that only affects agent-specific behavior (e.g., ps-architect stops producing ADR recommendations, nse-requirements drops the traceability matrix) may not be detected if the universal MRs pass and the G-Eval quality scores are not sensitive enough to catch it.

**Accepted residual:** FM-003 residual RPN = 96 (S=8, O=2, D=6). Accepted per ADR-001 as Phase D roadmap item.

**Mitigation until Phase D:** The G-Eval criteria in `evaluation/criteria/` encode some agent-specific quality dimensions. MR violations are supplementary signals, not the sole regression detector.

---

### Limitation 2: STANDARD Mode Cannot Trigger Wilcoxon (Single-Run N=10)

`EvaluationMode.STANDARD` produces N=10 LLM runs per evaluation. The Wilcoxon engine requires N >= 20 (`MIN_STATISTICAL_SAMPLE_SIZE = 20`). A single STANDARD mode evaluation cannot trigger statistical comparison — it would raise `InsufficientSamplesError`.

**Practical effect:** The intended workflow for STANDARD mode (accumulate N=10-run batches across multiple evaluations to reach N >= 20) is architecturally sound but the accumulation protocol is not documented. STANDARD mode currently operates as structural + G-Eval scoring without Wilcoxon comparison.

**Recommendation:** Document the N accumulation protocol in `baselines/protocol.md`. Consider adding an explicit warning in the STANDARD mode report: "Statistical comparison requires N >= 20 (currently N={n}). Additional evaluations needed."

---

### Limitation 3: MR Tolerances Set from Initial Estimates, Not Empirical Data

The 5 MR tolerance values (MR-001: 0.05, MR-002: directional, MR-003: 0.04, MR-004: 0.06, MR-005: 0.07) are set from initial estimates derived from the calibration methodology described in system-design.md. Empirical calibration against 100+ real Jerry agent output pairs has not yet been executed.

**Practical effect:** Initial tolerance values may produce higher false-positive or false-negative rates than the 15% target until calibration is run. MR violations are reported as warnings (not failures) until calibrated, per FR-010 and FM-009 mitigation.

**Recommendation:** Execute the calibration procedure described in system-design.md section 1.5 against at least 5 known-stable agent definitions, 30 runs each, before enabling MR violations as blocking signals.

---

### Limitation 4: No Centralized Security Event Logging

The harness logs security-relevant events (MC-02 injection patterns when implemented, exception thresholds in evaluate_batch) at WARNING level in Python logs. There is no centralized security monitoring, no failure-rate alerting, and no structured export to Langfuse (optional port is defined but adapter is not implemented).

**Practical effect:** Operators must examine GHA logs directly to detect unusual patterns. There is no dashboard or alert for patterns such as systematic evaluate_batch exception rates or repeated injection pattern detection.

**Recommendation:** Implement basic CI step summary output for security-relevant events (injection patterns detected, exception rate thresholds crossed) as a minimum observability measure before production deployment.

---

### Limitation 5: Smoke Mode Uses `:latest` Tag (Highest Supply Chain Risk)

Even after digest-pinning the production workflows, the Smoke workflow uses `ghcr.io/promptfoo/promptfoo:latest`. This is the highest-risk configuration because `:latest` changes silently. The Smoke workflow runs on every PR, regardless of whether agent definitions are changed — this is the most frequently executed workflow.

**Recommendation:** Prioritize Smoke workflow digest-pinning over Standard/Full (the `:latest` vs. version-tag distinction makes Smoke the highest-priority fix).

---

## L1: Deployment Sequence

Deploy in this order to minimize risk and enable rollback at each stage.

### Stage 0: Pre-Deploy Validation (BEFORE any merge)

| Step | Action | Validation |
|------|--------|-----------|
| 0.1 | Resolve RR-001: Implement `_sanitize_input()` in `deepeval_adapter.py` | Unit test: injection patterns detected; length truncation at 10KB |
| 0.2 | Resolve RR-002: Pin Dockerfile base image to SHA-256 digest | `docker build` succeeds with pinned digest |
| 0.3 | Resolve RR-002: Pin Smoke workflow to SHA-256 digest (highest priority) | Workflow runs successfully with digest-pinned image |
| 0.4 | Resolve RR-002: Pin Standard/Full workflows to SHA-256 digest | Workflows run successfully |
| 0.5 | QG-4A human review | Engineering lead sign-off |

### Stage 1: Deploy python/testing Package Only

**Artifacts:** `jerry/testing/` (types.py, stats.py, evaluation/, metamorphic/, baselines/, reports/, layer4_stats.py)

**Why first:** The statistical engine and evaluation backend are pure Python with no external runtime dependencies (beyond scipy, statsmodels which are already in pyproject.toml). They can be deployed and tested without CI/CD changes.

**Validation:**
- `uv run pytest tests/prompt-regression/unit/` — all unit tests pass
- `uv run pytest tests/prompt-regression/property/` — property-based tests pass (Hypothesis)
- `uv run pytest tests/prompt-regression/integration/` — integration tests pass

**Rollback:** Revert `jerry/testing/` to prior state. No CI/CD changes deployed; no external impact.

---

### Stage 2: Deploy promptfoo Test Case YAMLs

**Artifacts:** `tests/prompt-regression/*.yaml`, `tests/prompt-regression/metrics/`, `docker/promptfoo/Dockerfile`

**Why second:** YAML test cases and the Docker container definition can be reviewed independently of the workflow triggers. This stage establishes the test case library without enabling automated triggering.

**Validation:**
- Local: `docker build -t promptfoo-test docker/promptfoo/`
- Local: `docker run promptfoo-test promptfoo eval --config tests/prompt-regression/promptfoo-config.yaml` (with test API key)
- Verify YAML test cases load without schema errors

**Rollback:** Remove new YAML test case files. Docker image is local; no registry impact.

---

### Stage 3: Deploy Smoke Workflow (Non-Blocking)

**Artifacts:** `.github/workflows/prompt-regression-smoke.yml`, `.github/actions/cost-monitor/`, `.github/actions/artifact-publish/`

**Configuration:** Deploy with `BLOCKING: false` environment variable to ensure smoke failures produce PR annotations but do not block merge. This enables operational observation before making the gate blocking.

**Why third:** Smoke mode runs on every PR, is the cheapest ($0 LLM cost), and produces only structural check results. Running non-blocking first provides real-world operational experience before enabling enforcement.

**Validation:**
- Create a test PR that does NOT modify agent files — verify smoke workflow does NOT run (path filter working)
- Create a test PR that modifies one agent file — verify smoke workflow runs, produces annotations, does not block merge
- Verify Docker image is pulled from digest-pinned reference

**Rollback:** Disable the workflow by adding `if: false` condition to the top-level workflow or deleting the file. No agent definition changes have been gated; no merge was blocked.

---

### Stage 4: Deploy Standard Workflow (Non-Blocking)

**Artifacts:** `.github/workflows/prompt-regression-standard.yml`

**Configuration:** Non-blocking initially (same rationale as Stage 3).

**Why fourth:** Standard mode incurs LLM API costs (~$2 per agent evaluation). Deploy and observe cost patterns before enabling as blocking gate. Provides validation that score arrays and baseline store operations work correctly in real CI conditions.

**Validation:**
- Trigger a full standard-mode evaluation for one agent (ps-researcher recommended as most well-tested)
- Verify score arrays written to expected paths
- Verify baseline store read/write works with real git commit hash
- Verify PR comment posted with regression report
- Verify LLM cost is within NFR-004 ceiling ($10 per Full mode)

**Rollback:** Disable Standard workflow. No agent definition changes were blocked during non-blocking phase.

---

### Stage 5: Enable Smoke Workflow as Blocking Gate

**Prerequisites:**
- At least 2 weeks of non-blocking Smoke operation with no false positives
- MC-02 and MC-08 remediated
- Team briefed on new PR workflow requirement

**Configuration:** Remove `BLOCKING: false` override; ensure GitHub branch protection rule requires the check to pass.

**Rollback:** Re-add `BLOCKING: false` override. No code changes required.

---

### Stage 6: Enable Standard Workflow as Blocking Gate

**Prerequisites:**
- Stage 5 stable for at least 2 weeks
- Baseline store populated with production baselines for all 5 covered agents
- MR tolerance calibration executed with real output pairs

**Configuration:** Remove non-blocking override from Standard workflow.

**Stage 6 is the milestone where the harness achieves its primary mission:** blocking PRs that cause statistically significant regressions in covered agent definitions.

---

### Stage 7 (Future): Deploy Full Workflow and Enable Full Mode

**Prerequisites:**
- Stage 6 stable
- Phase D (agent-specific MRs, FR-012, FR-013) complete
- MR coverage tracking reporting implemented
- Budget approval for Full mode cost (~$5-8 per agent per evaluation)

---

## L1: Rollback Plan

### If Any Stage Causes Problems

**Decision authority:** Engineering lead or on-call engineer can initiate rollback without escalation for Stages 1-4. Stages 5-6 require engineering lead approval.

**Rollback speed:** All stages can be rolled back within 15 minutes by disabling the relevant workflow (add `if: false` top-level condition) or reverting the `jerry/testing/` package commit.

### Rollback by Stage

| Stage | Rollback Action | Impact | Time |
|-------|----------------|--------|------|
| Stage 1 (Python package) | `git revert` the jerry/testing/ commit | Tests fail; no CI impact | 5 min |
| Stage 2 (YAML test cases) | Remove YAML files from PR | Docker container not invoked | 5 min |
| Stage 3 (Smoke, non-blocking) | Disable workflow (`if: false`) | No structural checks run | 2 min |
| Stage 4 (Standard, non-blocking) | Disable workflow (`if: false`) | No LLM evaluation runs; no cost | 2 min |
| Stage 5 (Smoke, blocking) | Remove branch protection rule + add `if: false` | PRs can merge without check | 5 min |
| Stage 6 (Standard, blocking) | Remove branch protection rule + add `if: false` | PRs can merge without standard check | 5 min |

### Rollback Decision Criteria

Initiate rollback immediately if any of the following are observed:

1. **False positive rate > 10%:** More than 1 in 10 legitimate (non-regressive) PRs blocked by the harness
2. **False negative confirmed:** A known regression merged past the harness
3. **Security incident:** Evidence of API key exposure, injection attack success, or anomalous score patterns
4. **Excessive cost:** LLM evaluation costs exceed $50 in a single billing period without proportional PR coverage
5. **Blocking CI for > 30 minutes:** Harness execution time exceeds 30 minutes and blocks team velocity

---

## L1: Monitoring Recommendations

### What to Watch Post-Merge

#### Critical Metrics (Monitor Daily)

| Metric | Target | Alert Threshold | Monitoring Method |
|--------|--------|-----------------|------------------|
| False positive rate | < 5% | > 10% | Track PRs blocked vs. PRs that merged after override |
| CI execution time | < Smoke: 5m, Standard: 25m, Full: 60m | Exceed workflow timeout-minutes | GHA workflow execution time |
| LLM API cost per PR | < $2 (Standard), < $8 (Full) | > $10 per evaluation | GHA cost-monitor composite action |
| Exception rate in evaluate_batch() | < 1% | > 20% | GHA log search for WARNING "Batch evaluation failed" |
| InsufficientSamplesError rate | 0% (Full mode) | Any occurrence in Full mode | GHA log search for InsufficientSamplesError |

#### Security Metrics (Monitor Weekly)

| Metric | Alert Condition | Action |
|--------|----------------|--------|
| MC-02 injection pattern detection count | Any occurrence | Investigate YAML test case that triggered pattern |
| Baseline store write rejections (quality gate failures) | Unexpected spikes | Investigate cause — may indicate API key compromise or model degradation |
| Docker image pull failures | Any failure after digest-pinning | Verify digest still valid; registry integrity check |
| API key age | > 90 days | Rotate per documented procedure |

#### Coverage Metrics (Monitor Monthly)

| Metric | Target | Action if Below |
|--------|--------|----------------|
| MR coverage per agent (when FR-013 implemented) | > 50% | Prioritize agent-specific MR authorship for below-threshold agents |
| Test case coverage per agent | All 5 agents have >= 3 test cases | Add test cases for agents with gaps |
| Baseline freshness (age_days) | All baselines < 90 days | Trigger re-baseline for stale entries |

### Observability Setup Checklist

- [ ] GHA step summary enabled for regression reports (verify `$GITHUB_STEP_SUMMARY` writes are working)
- [ ] Artifact retention set to 90 days in all three workflow files
- [ ] Cost monitoring composite action deployed (`.github/actions/cost-monitor/`)
- [ ] Artifact publish composite action deployed (`.github/actions/artifact-publish/`)
- [ ] Langfuse integration configured (optional — port defined; adapter deferred)
- [ ] Alert channel established for MC-02 injection pattern detections (when MC-02 implemented)

### Escalation Path

| Severity | Condition | Escalation | Response |
|----------|-----------|------------|----------|
| P1 (Security) | API key exposure, injection attack confirmed, malicious image executed | Engineering lead immediately | Rotate key, disable harness, post-mortem |
| P1 (Blocking) | False positive rate > 30% for > 1 hour | On-call engineer | Rollback Stage 5 or 6 immediately |
| P2 (Quality) | False positive rate 10-30% | Engineering lead within 4 hours | Investigate; consider temporary non-blocking mode |
| P3 (Operational) | Baseline staleness > 90 days | Engineering team | Scheduled re-baseline sprint |
| P4 (Monitoring) | FR-013 not implemented after 60 days | Backlog grooming | Prioritize Phase D |

---

## L2: Open Items Requiring Future Work

### Phase D: Agent-Specific MR Framework

**Priority:** HIGH — directly closes the highest accepted residual risk (FM-003)

| Item | Description | Effort | Dependency |
|------|-------------|--------|-----------|
| FR-012: Agent-specific MR framework | Implement minimum 2 MRs per agent class (structural + behavioral) for all 5 covered agents = 10 new MR files | Large | FR-013 implementation |
| FR-013: MR coverage tracking module | Implement `mr_coverage_tracker.py`; compute coverage % from `contracts/per-agent/*.yaml` files; integrate into CI report | Medium | FR-012, contracts/per-agent/ |
| FR-013 path reconciliation | Resolve `tests/prompt-regression/contracts/` vs. `contracts/per-agent/` path discrepancy (QG-1 finding) | Small | FR-013 |
| T-41 threat model addition | Add adversarial MR violation crafting threat to system-design.md (QG-1 architectural gap) | Small | — |

### Post-Merge Technical Debt

**Priority:** MEDIUM — resolve before Phase D to prevent debt compounding

| Item | Description | Effort | Risk ID |
|------|-------------|--------|---------|
| Consolidate InsufficientSamplesError | Single class in types.py or stats.py; update base.py import | Small | RR-023 |
| Extract _wilcoxon_p_and_effect | New file metamorphic/_wilcoxon_helpers.py; update 3 importers | Small | RR-024 |
| Document STANDARD mode N accumulation | Add protocol note to baselines/protocol.md | Small | RR-028 |
| Declare deepeval in pyproject.toml | `deepeval = "==X.Y.Z"` in test deps; run uv sync | Small | RR-011 |
| Correct ScoreArray description | interface-verification.md: "dataclass" -> "list[float] type alias" | Trivial | QG-3 note |
| Add IMPROVEMENT classification to 1A FR-015/FR-018 | Document fourth Wilcoxon classification | Small | QG-1 finding |
| Add FR-017 cross-reference to 1D D.3 for k=13 | One sentence in harness-requirements.md | Trivial | QG-1 finding |

### Deferred Security Hardening

**Priority:** MEDIUM — address before Phase D's wider deployment scope

| Item | Description | Effort | Risk ID |
|------|-------------|--------|---------|
| BaselineStore._validate_version_key() strengthening | Replace with VersionKey.from_string() validation | Small | RR-003 |
| evaluate_batch() exception threshold re-raise | Fail batch if >20% exception rate rather than silently padding 0.0 | Small | RR-004 |
| AGENT_ID allowlist validation in CI workflows | Add allowlist check against COVERED_AGENTS before Docker run | Small | RR-005 |
| SHA-256 hash truncation fix | Extend compute_prompt_content_hash() to 128-bit minimum | Small | RR-006 |
| Automated API key rotation documentation | Document rotation policy; consider automation | Medium | RR-022 |
| npm audit / Trivy scan in CI | Add CVE scan step after Docker build | Small | RR-021 |
| file:// protocol restriction in promptfoo config | Restrict promptfoo file handler to whitelist paths | Small | RR-020 |

### Phase E-F: Future Layers (Per ADR-001 Roadmap)

| Phase | Description | Dependency |
|-------|-------------|-----------|
| Phase E: PPI Calibration | Prompt Perturbation Index calibration — extends Layer 3 | Phase D complete |
| Phase F: Perturbation Testing | Automated behavioral perturbation generator — extends Layer 3 | Phase E complete |
| PROJ-017 integration verification | Verify stats.py shared usage in PROJ-017 skill evaluation | PROJ-017 directory present in repo |

---

## L2: Strategic Deployment Considerations

### The Harness Changes the Development Contract for Prompt Authors

Before this harness, prompt changes to agent definitions had no automated validation path. After deployment (Stage 6), every PR modifying `skills/*/agents/*.md` must:
1. Author a corresponding test case YAML (FR-027 authorship checklist)
2. Pass the Smoke structural check (non-blocking until Stage 5)
3. Pass the Standard G-Eval + MR evaluation with no statistically significant regression (blocking at Stage 6)

This is a significant change to the development workflow for 67 agent definitions across 12 skills. Engineering communication and team onboarding are required before enabling blocking gates.

**Recommendation:** Announce the deployment plan to all skill authors before Stage 5. Provide a "migration guide" that explains: (a) what triggers the harness, (b) how to interpret PASS/WARN/FAIL verdicts, (c) how to add test cases for their agents, (d) how to request a re-baseline when intentionally improving an agent.

### The Baseline Store Is the Critical Operational Asset

The baseline store at `baselines/data/{agent_id}/{metric_id}/{version_key_slug}.json` accumulates historical quality data. This is the reference against which all future evaluations are compared. Operational considerations:

1. **Initial baselines must be established before enabling blocking gates.** If no baseline exists for an agent, the harness cannot perform statistical comparison (only Smoke structural checks). All 5 covered agents need initial baselines captured with N >= 30 Full mode runs.

2. **Baselines must be re-captured after intentional quality improvements.** When an agent is improved (IMPROVEMENT verdict), the baseline should be updated to the new higher quality level. Failing to update means future evaluations will compare against a suboptimal reference.

3. **Model migration requires full re-baseline.** If `anthropic:messages:claude-sonnet-4-20250514` is replaced, all baselines are invalidated. The `invalidate()` method in `BaselineStore` handles this, but requires a coordinated re-baseline sprint across all 5 agents (FR-026, protocol.md re-baseline runbook).

### The Statistical Thresholds Are Deliberate Engineering Decisions

The key constants (N >= 20, QUALITY_PASS_THRESHOLD = 0.92, BONFERRONI_K_FULL_SUITE = 13, Wilcoxon alpha = 0.05) were established through the behavioral contracts process (1D) and verified against the FMEA. They should not be changed casually:

- Reducing N below 20 would re-introduce FM-002 (statistical false alarms from small N) which was identified as high-risk in the FMEA
- Raising QUALITY_PASS_THRESHOLD above 0.92 would increase false positive rates for agents that legitimately operate near the threshold
- Changing Bonferroni k without updating all affected constants would silently invalidate the family-wise error rate calculation

Any threshold change should be treated as a C3 decision requiring the modification of `behavioral-contracts.md` Section D, a new re-baseline operation, and documentation update in `stats.py`.

---

## Sign-Off Criteria

The harness is ready for final merge (QG-4A PASS) when ALL of the following are true:

### Technical Criteria

- [ ] RR-001 resolved: `_sanitize_input()` implemented and tested in `deepeval_adapter.py`
- [ ] RR-002 resolved: All 4 Docker image references pinned to SHA-256 digests (Dockerfile, smoke.yml, standard.yml, full.yml)
- [ ] Stream 7A (Engineering Review) >= 0.94
- [ ] Stream 7B (Cross-Synthesis, this document) >= 0.94
- [ ] QG-4A adversarial scoring >= 0.95

### Governance Criteria

- [ ] Engineering lead human review sign-off (required per ORCHESTRATION.yaml QG-4A)
- [ ] QG-4B NASA SE Technical Review (NPR 7123.1D Appendix G)

### Operational Criteria

- [ ] Deployment sequence documented (this document, Section L1 Deployment Sequence)
- [ ] Rollback plan documented (this document, Section L1 Rollback Plan)
- [ ] Monitoring recommendations documented (this document, Section L1 Monitoring)
- [ ] Team communication plan prepared for blocking gate enablement

### Deferred (Acceptable without blocking merge)

- FR-026: deepeval in pyproject.toml (LOW risk, model pinning is primary control)
- FR-012: Agent-specific MRs (Phase D)
- FR-013: MR coverage tracking (Phase D)
- RR-023: InsufficientSamplesError consolidation (post-merge debt)
- RR-028: STANDARD mode N accumulation documentation (post-merge)

---

*Stream: 7B (Cross-Synthesis)*
*Agent: ps-synthesizer v2.3.0*
*Constitutional compliance: P-003 (no recursion), P-020 (user authority), P-022 (no deception)*
*Sources: QG-1/QG-2/QG-3 barrier reports, 5A security assessment, 5B V&V, ORCHESTRATION.yaml, all 12 completed streams*
*Date: 2026-03-07*
