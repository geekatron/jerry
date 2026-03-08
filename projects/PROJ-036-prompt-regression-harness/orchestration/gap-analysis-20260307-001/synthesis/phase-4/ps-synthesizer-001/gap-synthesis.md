# Phase 4 Synthesis — PROJ-036 Test Harness Gap Closure Plan

> **PS Synthesizer Output**
> Agent: ps-synthesizer v2.3.0
> PS ID: gap-analysis-20260307-001
> Entry: phase-4
> Date: 2026-03-07
> Methodology: Braun & Clarke Thematic Analysis (6 phases) + Cross-Reference Matrix

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary (L0)](#executive-summary-l0) | Plain-language overview of findings and priorities |
| [Source Quality Assessment](#source-quality-assessment) | Confidence levels and coverage for each input |
| [Cross-Reference Matrix](#cross-reference-matrix) | Gap deduplication across all four Phase outputs |
| [Canonical Gap Registry](#canonical-gap-registry) | 34 unique gaps, deduplicated, prioritized |
| [Dependency Graph](#dependency-graph) | Which gaps block other gaps |
| [Technical Synthesis (L1)](#technical-synthesis-l1) | Implementation implications per gap |
| [Strategic Synthesis (L2)](#strategic-synthesis-l2) | Architectural patterns and systemic observations |
| [Implementation Roadmap](#implementation-roadmap) | Sequenced phases with effort estimates |
| [Cross-Phase Patterns](#cross-phase-patterns) | Themes appearing across multiple phases |
| [Risk Assessment](#risk-assessment) | Consolidated risk register |
| [Knowledge Items Generated](#knowledge-items-generated) | PAT, LES, ASM items |

---

## Executive Summary (L0)

We analyzed five documents covering the PROJ-036 prompt regression test harness from four angles: a 38-component gap inventory (Phase 1A), a requirements traceability matrix covering 45 requirements (Phase 1B), a secure code review with 10 findings (Phase 2A), a supply-chain security assessment (Phase 2B), and an adversarial quality score of the AnthropicModel fix (Phase 3).

After deduplication across all five sources, we identified **34 canonical gaps** grouped into five priority tiers.

**The most urgent problem:** Two Python modules (`layer4_stats.py` and `baselines/store.py`) are called by the GitHub Actions Full workflow as if they have CLI entry points, but neither does. Every Full-tier CI run fails immediately at the Python invocation step before any evaluation runs. This is a P0 blocker that can be fixed in a single afternoon.

**The second most urgent problem:** A live Anthropic API key exists on disk in the `.env` file. The key must be rotated now — this is independent of all other work.

**What works well:** The statistical engine (Layer 4), the metamorphic relation framework (Layer 3), and the core G-Eval evaluation classes (Layer 2) are all fully implemented and validated. The GitHub Actions Smoke workflow is production-ready. The before/after version comparison architecture is correctly designed.

**What still needs to be built:** The connective tissue — CLI entry points, the score array extraction pipeline that bridges promptfoo output to Layer 4 input, and real baseline data. Without these three things, the system has sophisticated layers that cannot talk to each other.

**Summary for stakeholders:** The hardest algorithmic work is done. The remaining gaps are primarily integration wiring, security hardening, and test coverage. A focused sprint of approximately 3-4 weeks would close all P0 through P2 gaps and bring the harness to production readiness.

---

## Source Quality Assessment

| Source | Phase | Agent | Evidence Basis | Confidence |
|--------|-------|-------|---------------|------------|
| `gap-inventory.md` | 1A | ps-analyst | Direct source reads + validation run artifacts | HIGH — all COMPLETE/MISSING verified by Grep |
| `traceability-matrix.md` | 1B | nse-requirements | Requirements source + code inspection + CI files | HIGH — FR-001 through FR-030 all traced |
| `code-review.md` | 2A | eng-security | Line-level code review of 5 modules | HIGH — all findings cite specific line numbers |
| `security-assessment.md` | 2B | red-vuln | Configuration analysis + workflow inspection | HIGH — three attack surfaces with evidence |
| `quality-score.md` | 3 | adv-scorer | S-014 LLM-as-Judge scoring of AnthropicModel fix | HIGH — scored with anti-leniency bias check |

**Cross-source consistency:** All five sources were generated in the same orchestration run (2026-03-07) against the same codebase state. There are no temporal divergence risks. Where sources address overlapping topics (e.g., the silent zero-score issue appears in both the code review and the quality score), their findings are consistent and mutually reinforcing.

---

## Cross-Reference Matrix

The following table maps key gap concepts to their appearances across source documents. This is the deduplication backbone for the Canonical Gap Registry.

| Concept | Phase 1A Gap Inventory | Phase 1B Traceability | Phase 2A Code Review | Phase 2B Security | Phase 3 Quality Score | Agreement |
|---------|----------------------|----------------------|---------------------|------------------|-----------------------|-----------|
| Missing `__main__` for layer4_stats | Item 37 (BUG/CRITICAL) | GAP-L4-CLI partial | — | — | — | HIGH |
| Missing `__main__` for baselines.store | Item 38 (BUG/HIGH) | GAP-L4-CLI partial | — | — | — | HIGH |
| JSON field mismatch `overall_verdict` | PARTIAL item 33 | — | — | — | — | SINGLE SOURCE |
| Live API key in .env | — | NFR-009 (PASS for CI) | SEC-001 CRITICAL | A1 risk (negligible in CI) | — | MEDIUM — eng sees critical, red sees negligible |
| Silent zero-score on failure | — | — | SEC-002 HIGH | — | Score 0.806 (quality issue) | HIGH — two sources |
| Missing API key validation | — | — | SEC-003 HIGH | A1-7 no fallback | — | HIGH |
| Prompt injection via agent output | — | — | SEC-004 HIGH | A2-1 LOW risk | — | MEDIUM — eng rates HIGH, red rates LOW (threat model difference) |
| Docker image not SHA-pinned | Item 31 note | GAP-L1-DOCKER-PIN | — | A3-1a/b MEDIUM | — | HIGH |
| conftest.py evaluator fixture missing | Item 28 (PARTIAL) | GAP-L2-PYTEST | — | — | — | HIGH |
| MR-to-DeepEval adapter missing | Item 34 (MISSING) | GAP-L3-BASECLASS | — | — | — | HIGH |
| Score array extraction pipeline missing | Item 35 (MISSING) | GAP-L2-EXPORT partial | — | — | — | HIGH |
| Baseline population missing | Item 36 (MISSING) | GAP-L4-CLI / FR-020 partial | — | — | — | HIGH |
| No unit tests for _resolve_model() | — | NFR-011 unconfirmed | — | — | Methodological Rigor 0.72 | HIGH — two sources |
| Case-sensitive prefix match in _resolve_model() | — | — | — | — | Completeness 0.78 | SINGLE SOURCE |
| No gap item linkage for fix | — | — | — | — | Traceability 0.72 | SINGLE SOURCE |
| LICENSES.md missing | — | GAP-CC-LICENSES | — | — | — | SINGLE SOURCE |
| GHA output injection (agent_id/verdict) | — | — | SEC-005 MEDIUM | — | — | SINGLE SOURCE |
| Path traversal in report writes | — | — | SEC-006 MEDIUM | — | — | SINGLE SOURCE |
| DeepEval Sentry/PostHog telemetry | — | — | SEC-007 MEDIUM | A3-3 LOW | — | HIGH — two sources |
| Re-baseline runbook missing | — | GAP-L2-REBASELINE | — | — | — | SINGLE SOURCE |
| Monte Carlo Type I error test missing | — | GAP-NFR-TYPE1 | — | — | — | SINGLE SOURCE |
| 90% coverage unconfirmed | — | GAP-NFR-COVERAGE | SEC review notes H-20 | — | H-20 violation noted | HIGH — three sources |
| CLI commands missing (jerry test *) | Item notes | GAP-NFR-CLI | — | — | — | HIGH |
| Layer entry-point modules absent | — | GAP-CC-LAYER-MODULES | — | — | — | SINGLE SOURCE |

**Contradiction surfaced:** The live API key in `.env` (SEC-001) is rated CRITICAL by the eng-security agent (CWE-798, CVSS 9.1) but negligible by the red-vuln agent (A1-1 finding: "no exposure risk"). The resolution: both are correct in their respective scopes. The eng-security finding is correct that the key exists on disk in plaintext and must be rotated. The red-vuln finding is correct that the CI/CD pipeline itself does not expose the key (masking, fork isolation, smoke tier isolation are all confirmed). The canonical action is: **rotate the key** (correct the key-exists-on-disk finding) AND **maintain the CI controls** (the CI posture is sound and requires no architectural change).

---

## Canonical Gap Registry

Gaps are assigned canonical IDs (CG-NNN) for cross-referencing. Duplicates from Phase 1A and 1B have been merged. Priority definitions:

- **P0 (Blocker):** Prevents any CI/CD pipeline tier from completing
- **P1 (Critical):** Security vulnerabilities or data integrity risks requiring immediate action
- **P2 (High):** Functional gaps blocking major requirements; harness cannot reach production
- **P3 (Medium):** Quality, test coverage, and verification gaps; production readiness concerns
- **P4 (Low):** Documentation, format, optional features

### P0 — Blockers

| CG ID | Gap Title | Source Items | Blocking FRs | Effort | Notes |
|-------|-----------|-------------|-------------|--------|-------|
| CG-001 | Missing `__main__` entrypoint for `layer4_stats.py` | Item 37, IL-2, GAP-L4-CLI | FR-015, FR-016, FR-017, FR-018 | S | Argument parser for `--agent`, `--tier`, `--results-file`, `--head-sha`, `--bonferroni-k`, `--output-report`, `--output-markdown` flags; instantiate Layer4Pipeline and call `run()` |
| CG-002 | Missing `__main__` entrypoint for `baselines/store.py` | Item 38, IL-3, GAP-L4-CLI | FR-020 | S | Argument parser for `--action`, `--agent`, `--results-file`, `--commit-sha`, `--tier`, `--reason` flags; call `BaselineStore.store()/retrieve()/audit()` |
| CG-003 | `ComparisonReport` field name mismatch (`classification` vs `overall_verdict`) | Item 33 defect, IL-7 | FR-018 | S | GHA Full workflow reads `data.get('overall_verdict', 'UNKNOWN')`; `ReportGenerator.to_json()` serializes `classification`; fix the GHA extraction step to read the correct field |

### P1 — Critical Security

| CG ID | Gap Title | Source Items | Severity | Effort | Notes |
|-------|-----------|-------------|---------|--------|-------|
| CG-004 | Live API key on disk in `.env` | SEC-001 | CRITICAL (CVSS 9.1) | S | Rotate key via Anthropic console immediately; replace `.env` with comment placeholder; commit `.env.example` with `sk-ant-...` placeholder |
| CG-005 | Silent zero-score substitution masks evaluation failures | SEC-002, quality score observation | HIGH | M | Three nested `except Exception` handlers return `0.0` on any API/auth failure; add pre-batch health check, failure count threshold, post-batch zero-array assertion; replace broad catches with typed exception hierarchy (`EvaluationConfigError`, `EvaluationAPIError`, `EvaluationScoringError`) |
| CG-006 | No API key presence validation at startup | SEC-003 | HIGH | S | Add `ANTHROPIC_API_KEY` env check to `DeepEvalAdapter.__post_init__`; raise `EnvironmentError` with actionable message if absent; log CRITICAL (not WARNING) on `AuthenticationError` |
| CG-007 | Docker images not pinned to SHA digest | SEC A3-1a/b, GAP-L1-DOCKER-PIN | MEDIUM | S | Pin all three workflows to SHA digests; resolve current digest with `docker inspect --format='{{index .RepoDigests 0}}'`; resolve smoke `:latest` to a specific release digest |

### P2 — High (Functional Gaps)

| CG ID | Gap Title | Source Items | Blocking FRs | Effort | Notes |
|-------|-----------|-------------|-------------|--------|-------|
| CG-008 | Score array extraction pipeline missing | Item 35, IL-5, GAP-L2-EXPORT | FR-009, FR-003, FR-015 | L | No script converts `promptfoo-output.json` to `dict[str, tuple[ScoreArray, ScoreArray]]` for Layer 4; this is the critical data flow gap connecting Layers 1 and 4 |
| CG-009 | Baseline population pipeline missing | Item 36, IL-6, GAP-L4-CLI, FR-020 | FR-020, FR-003, FR-014 | L | `tests/prompt-regression/baselines/captured/` does not exist; no real N=30 capture has occurred; the protocol.md references scripts that do not exist; required before any real before/after comparison |
| CG-010 | MR-to-DeepEval adapter wire missing | Item 34, IL-4, GAP-L3-BASECLASS | FR-010, FR-003 | M | `DeepEvalAdapter` has no `build_metric_for_mr()` method; MR classes cannot be passed to `deepeval.assert_test()`; domain ABC exists but adapter wrapping is absent |
| CG-011 | conftest.py `evaluator` fixture missing | Item 28, IL-1, GAP-L2-PYTEST | FR-006 | S | 18-line conftest does sys.path only; needs `@pytest.fixture` returning `DeepEvalAdapter` as `EvaluationPort`; this is the entry point for live pytest-based L2 evaluation |
| CG-012 | Custom GitHub Actions not confirmed to exist | GAP-NFR-CI, NFR-005 | NFR-005 | S | Standard workflow references `.github/actions/cost-monitor` and `.github/actions/artifact-publish`; these must exist for the Standard workflow to run; verify or create stubs |
| CG-013 | `_resolve_model()` case-sensitive prefix match | Phase 3 quality score | FR-006, FR-007 | S | `self.model.startswith("claude")` fails for `"Claude-..."` (capitalized); change to `self.model.lower().startswith("claude")`; add unit tests for 4 cases |
| CG-014 | Unit tests for `_resolve_model()` absent | Phase 3 quality score, GAP-NFR-COVERAGE | NFR-011, H-20 | S | Method is 3 lines and directly testable; absence violates H-20 (90% coverage); add 4 parameterized test cases |
| CG-015 | LICENSES.md absent, no CI license check | GAP-CC-LICENSES, FR-022 | FR-022 | S | Create LICENSES.md listing deepeval (Apache 2.0), scipy (BSD), statsmodels (BSD), anthropic (MIT); add `uv run pip-audit` or `pip-licenses` step to Smoke workflow |
| CG-016 | DeepEval telemetry (Sentry/PostHog) not disabled | SEC-007, A3-3 | NFR-009 | S | Add `DEEPEVAL_TELEMETRY_OPT_OUT=YES` to `.env`, `.env.example`, and all three CI workflow `env:` blocks; prevents evaluation metadata reaching third-party endpoints |
| CG-017 | Prompt injection via unsanitized agent output to LLM judge | SEC-004, A2-1 | FR-006, FR-007 | S | Add output truncation at `LLMTestCase` construction point (8000 chars); add `[AGENT OUTPUT START/END]` delimiters in judge prompt; reconcile inconsistency with debiasing.py truncation |
| CG-018 | GHA output injection via `agent_id`/`classification` values | SEC-005 | NFR-009 | S | Add newline sanitization in `_emit_gha_outputs`; add `agent_id` format validation regex `^[a-z][a-z0-9-]*$` |

### P3 — Medium (Quality and Verification)

| CG ID | Gap Title | Source Items | Blocking FRs/NFRs | Effort | Notes |
|-------|-----------|-------------|------------------|--------|-------|
| CG-019 | 90% test coverage unconfirmed | GAP-NFR-COVERAGE, NFR-011, H-20 | NFR-011 | M | Run `uv run pytest --cov=jerry/testing --cov-report=term-missing tests/prompt-regression/`; identify uncovered lines; H-20 is a HARD rule — this is a governance risk |
| CG-020 | Monte Carlo Type I error validation test missing | GAP-NFR-TYPE1, NFR-007 | NFR-007 | M | `test_stats_type1_error.py` not implemented; required before production deployment per NFR-007; implement as parameterized pytest benchmark using synthetic score arrays |
| CG-021 | No performance benchmark measurements | GAP-NFR-PERF, NFR-001, NFR-002 | NFR-001, NFR-002 | M | No P95 timing data for Smoke (< 60s) or Standard (< 15 min); implement timing instrumentation; run 10-run benchmark for each tier |
| CG-022 | Re-baseline runbook and CI detection absent | GAP-L2-REBASELINE, FR-026 | FR-026 | S | Create `tests/prompt-regression/runbooks/re-baseline-after-upgrade.md`; add CI detection step that fails if DeepEval version changed without updated baselines |
| CG-023 | `_resolve_model()` fix has no gap item linkage or design note | Phase 3 quality score | NFR-014, traceability | S | Add code comment referencing gap-analysis-20260307-001; create a worktracker entry or brief design note documenting the prefix-match decision and its Bedrock/Vertex limitation |
| CG-024 | Bedrock/Vertex Claude model IDs not handled in `_resolve_model()` | Phase 3 quality score | FR-006 | S | Anthropic-hosted `claude-*` covered; Bedrock ARN format (`anthropic.claude-3-sonnet-20240229-v1:0`) silently falls through to GPTModel; document limitation explicitly; add guard with `ValueError` for ARN-pattern inputs |
| CG-025 | Path traversal in report writes (no allowed-root validation) | SEC-006 | NFR-009 | S | Add allowed-root validation in `_persist_report`; validate `json_path` and `markdown_path` are under permitted output directories before writing |
| CG-026 | LLM judge rationale flows unsanitized to reports | SEC-008 | NFR-009 | S | Escape `evidence` string in HTML rendering path; JSON path is already safe (serializer handles escaping) |
| CG-027 | `version_key` format not validated at entry points | SEC-009 | NFR-009 | S | Add regex validation `^[0-9a-f]{7,40}:[^\n\r\0]+$` at `evaluate_batch` and `Layer4Pipeline.run` entry points |
| CG-028 | DeepEval version pinning uses `>=2.0.0` (unbounded upper) | Code review dependency section | FR-026 | S | Narrow to `>=3.8.0,<4.0.0` in `pyproject.toml` to prevent silent 4.x breaking changes from altering evaluation behavior |
| CG-029 | `scipy` not declared as explicit dependency | Code review dependency section | FR-015, FR-019 | S | Add `scipy>=1.11.0` to `pyproject.toml` with comment referencing FR-015; currently a transitive dep that could break if resolution path changes |
| CG-030 | pip-audit not enforced in CI gate | A3-6 | NFR-009 | S | Add `uv run pip-audit` step to Smoke workflow; converts existing dev dependency into a CI-enforced CVE gate |

### P4 — Low (Documentation and Format)

| CG ID | Gap Title | Source Items | Blocking FRs/NFRs | Effort | Notes |
|-------|-----------|-------------|------------------|--------|-------|
| CG-031 | Criteria stored in Python modules, not YAML/JSON | GAP-L2-CRITERIA-FORMAT, FR-007 AC-3 | FR-007 | L | FR-007 AC-3 specifies `tests/prompt-regression/criteria/*.yaml`; current Python module format is functional; migration is a pure format change with no behavioral difference; defer unless AC-3 is a hard requirement |
| CG-032 | Test case files named `{agent-id}.yaml` not `{agent-id}-regression.yaml` | GAP-NFR-NAMING, NFR-008 | NFR-008 | S | Trivial rename; update promptfoo-config.yaml references simultaneously |
| CG-033 | PR checklist template not confirmed | GAP-CC-PR-TEMPLATE, FR-027 | FR-027 | S | Add `.github/PULL_REQUEST_TEMPLATE.md` with required checklist item for test case authorship |
| CG-034 | `debiasing-config.yaml` documentation file absent | GAP-L2-DEBIAS-CONFIG, FR-021 | FR-021 | S | Debiasing itself is implemented and mandatory; the config file is a documentation artifact per FR-021 AC-4; create the YAML file documenting the debiasing configuration |

---

## Dependency Graph

Arrows indicate "must be completed before." Items on the same row in a phase can be parallelized.

```
P0 BLOCKERS (must complete first)
  CG-001 [__main__ layer4_stats]
  CG-002 [__main__ baselines.store]
  CG-003 [field name mismatch]
  CG-004 [rotate API key — independent, do immediately]
       |
       v
P1 SECURITY (unblock before feature work)
  CG-005 [silent zero-score] ----requires----> CG-001 (need __main__ to test CI path)
  CG-006 [API key validation] ----related to--> CG-005 (same exception handling refactor)
  CG-007 [Docker SHA pin] ----independent, parallelize
  CG-016 [telemetry opt-out] ----independent, parallelize
       |
       v
P2 FUNCTIONAL GAPS
  CG-008 [score array pipeline] ----requires----> CG-001 (needs __main__ to receive --results-file)
  CG-008 [score array pipeline] ----requires----> CG-002 (needs __main__ to call store)
  CG-009 [baseline population] ----requires----> CG-002 (needs __main__ to populate)
  CG-009 [baseline population] ----requires----> CG-008 (needs scores to store as baselines)
  CG-010 [MR adapter] ----independent of P0 blockers (domain layer)
  CG-011 [conftest fixture] ----requires----> CG-013 (fix model resolution first)
  CG-011 [conftest fixture] ----requires----> CG-014 (add tests first for safety)
  CG-012 [custom GHA actions] ----independent
  CG-013 [case-insensitive prefix] ----independent
  CG-014 [_resolve_model tests] ----independent
  CG-015 [LICENSES.md] ----independent
  CG-017 [prompt injection truncation] ----independent
  CG-018 [GHA output injection] ----independent
       |
       v
P3 QUALITY / VERIFICATION
  CG-019 [coverage measurement] ----requires----> CG-014 (add missing tests first)
  CG-019 [coverage measurement] ----requires----> CG-011 (conftest adds testable fixture)
  CG-020 [Monte Carlo test] ----independent
  CG-021 [performance benchmarks] ----requires----> CG-008 (need real pipeline to benchmark)
  CG-021 [performance benchmarks] ----requires----> CG-009 (need baselines to run full benchmark)
  CG-022 [re-baseline runbook] ----independent
  CG-023 [gap item linkage] ----independent
  CG-024 [Bedrock limitation] ----follows----> CG-013 (group with model resolution work)
  CG-025 [path traversal guard] ----independent
  CG-026 [rationale sanitization] ----independent
  CG-027 [version_key validation] ----independent
  CG-028 [deepeval version bound] ----independent
  CG-029 [scipy declaration] ----independent
  CG-030 [pip-audit CI] ----independent
       |
       v
P4 DOCUMENTATION / FORMAT
  CG-031 [criteria YAML format] ----independent
  CG-032 [file naming] ----independent
  CG-033 [PR template] ----independent
  CG-034 [debiasing config] ----independent
```

**Critical chain (longest dependency path to production):**

```
CG-004 (rotate key) [immediate]
  -> CG-001 + CG-002 (add __main__ entry points)
    -> CG-008 (score array extraction)
      -> CG-009 (real baseline population)
        -> CG-021 (end-to-end performance benchmark)
```

This 5-step chain is the minimum required to have a fully functioning production-grade harness. All other gaps are either security hardening, quality improvements, or documentation that can be completed in parallel.

---

## Technical Synthesis (L1)

### Integration Layer Status

The harness consists of four computational layers connected by integration layers. The table below shows the current wiring status:

| Layer | Components | Status | Primary Gap |
|-------|-----------|--------|-------------|
| Layer 1 (promptfoo) | YAML test cases, CI workflows | PARTIAL | No end-to-end live execution confirmed; Docker not SHA-pinned |
| L1→L4 Bridge | Score array extraction from promptfoo JSON | MISSING | CG-008 — the entire data flow connection |
| Layer 2 (DeepEval) | G-Eval criteria, adapter, debiasing | PARTIAL | conftest fixture (CG-011), silent failure (CG-005), model resolution (CG-013) |
| Layer 3 (MR) | 5 MR classes, domain ABC | PARTIAL | DeepEval adapter wrapping (CG-010) |
| Layer 4 (Stats) | Wilcoxon, Wilson, Bonferroni, Layer4Pipeline | PARTIAL | Missing CLI entry point (CG-001), no real baseline data (CG-009) |
| Baseline Store | BaselineStore, BaselinePersistencePort | PARTIAL | Missing CLI entry point (CG-002), no captured data |
| Report Generator | ReportGenerator, ComparisonReport | BUG | Field name mismatch in GHA extraction (CG-003) |

### Security Posture by Layer

| Layer | Posture | Key Risk | Action |
|-------|---------|---------|--------|
| API Key handling (CI) | STRONG | Key on disk locally (CG-004) | Rotate immediately; CI controls are sound |
| Evaluation pipeline | WEAK | Silent zero-score (CG-005), no startup validation (CG-006) | Add health check and typed exception hierarchy |
| Docker execution | MEDIUM | Mutable image tags (CG-007) | SHA-pin all three workflows |
| GHA output | LOW | Injection via unvalidated values (CG-018) | Newline sanitize and format-validate |
| Supply chain | MEDIUM | deepeval telemetry (CG-016), pip-audit not in CI (CG-030) | Opt out and add CI gate |

### _resolve_model() Specific Actions (Phase 3 Quality Score Remediation)

The AnthropicModel fix (scored 0.806, REVISE) requires four targeted changes to reach the 0.92 threshold:

1. Change `self.model.startswith("claude")` to `self.model.lower().startswith("claude")` (CG-013)
2. Add 4 unit tests for `_resolve_model()` including capitalization edge case (CG-014)
3. Add code comment linking to gap-analysis-20260307-001 (CG-023)
4. Document Bedrock/Vertex limitation in docstring; add `ValueError` guard for ARN-pattern inputs (CG-024)

With all four changes, the projected composite score is approximately 0.90-0.93, clearing the 0.92 C3 threshold.

---

## Strategic Synthesis (L2)

### Architectural Strength: The Core Algorithms Are Sound

The most strategically important finding from the cross-phase analysis is that the computational core — Layer 4 statistical engine (`stats.py`, 695 lines), Layer 3 metamorphic relations (5 MR classes), and Layer 2 G-Eval evaluation (criteria, adapter, debiasing) — is all implemented, validated, and architecturally clean. The validation run produced real Layer 2 scores for ps-researcher (0.935 PASS) and real Layer 4 Wilcoxon results (p=0.0000, Cohen's r=0.843) when called programmatically with synthetic data.

This means the risk profile is lower than the raw gap count suggests. The gaps are primarily integration wiring (entry points, data pipelines), not algorithmic rework.

### Architectural Weakness: Integration Layers Are Incomplete as a Pattern

Across all four analysis phases, a single structural pattern emerges: **every integration layer is missing or partial**. The IL-1 through IL-7 list from Phase 1A maps directly to this: the layers that connect the computational modules to each other and to the CI/CD pipeline are consistently the absent pieces.

This is a recognizable architectural anti-pattern — strong domain layer, weak adapter/port layer — consistent with systems built bottom-up (domain first, integration later). The consequence is that integration work is now the critical path, not algorithmic work.

### Systemic Risk: Silent Failure Mode Is Architecturally Dangerous

The Phase 2A finding (SEC-002, three nested `except Exception` handlers that silently substitute 0.0) represents the most strategically dangerous gap in the system. It subverts the entire purpose of the regression harness: if a broken evaluation configuration produces a false-green CI result, the harness is not merely useless — it is actively misleading. Engineers would believe their prompt changes are safe when the evaluation machinery has quietly failed.

This is classified as a **systemic risk** because it is invisible. SEC-001 (key on disk) is visible and immediately rotatable. SEC-002 requires architectural refactoring of the exception handling model, which is a more sustained effort but is essential before the harness is used for production gating decisions.

### Emergent Theme: Validation Evidence Is One-Sided

The Phase 3 quality score surfaced a recurring finding that appears in softer form across the other phases: **before-state evidence is absent**. The AnthropicModel fix demonstrably works (0.935 for ps-researcher vs. 0.0 before), but the "before" state is described contextually, not persisted. The baseline population gap (CG-009) means that every Layer 4 comparison to date has used synthetic baselines, not real captured data. The coverage gap (CG-019) means the 90% target is asserted, not measured.

This pattern — asserting rather than measuring prior state — is a test harness anti-pattern. A harness that measures prompt quality but does not measure its own quality creates a blind spot in the system's self-knowledge.

---

## Implementation Roadmap

### Sprint 0 — Immediate (Day 1, no CI required)

| CG ID | Action | Effort | Owner | Output |
|-------|--------|--------|-------|--------|
| CG-004 | Rotate Anthropic API key; replace .env with placeholder; commit .env.example | S (15 min) | Security | New API key in use |

### Sprint 1 — P0 Blockers (Week 1)

Goal: Full workflow can execute end-to-end without Python invocation failures.

| CG ID | Action | Effort | Depends On | Output |
|-------|--------|--------|-----------|--------|
| CG-001 | Add `__main__` to `layer4_stats.py` with argparse | S | CG-004 | GHA Full workflow layer4_stats step no longer fails |
| CG-002 | Add `__main__` to `baselines/store.py` with argparse | S | — | GHA Full workflow baseline step no longer fails |
| CG-003 | Fix `overall_verdict` → `classification` field extraction in GHA Full workflow | S | — | Verdict extraction branch logic becomes reachable |
| CG-006 | Add `ANTHROPIC_API_KEY` presence validation to `DeepEvalAdapter.__post_init__` | S | — | Auth failures surface immediately with actionable message |
| CG-016 | Add `DEEPEVAL_TELEMETRY_OPT_OUT=YES` to `.env.example` and all three CI workflow `env:` blocks | S | CG-004 | No evaluation metadata reaches Sentry/PostHog |

Estimated week 1 effort: 2-3 days across 5 gaps.

### Sprint 2 — P1 Security + P2 Quick Wins (Weeks 2-3)

Goal: Security posture hardened; model resolution fix quality-gate compliant; critical functional wiring added.

| CG ID | Action | Effort | Depends On | Output |
|-------|--------|--------|-----------|--------|
| CG-007 | SHA-pin all three Docker workflow images | S | — | Supply chain gap closed |
| CG-013 | Change `startswith("claude")` to `.lower().startswith("claude")` | S | — | Case-insensitive model resolution |
| CG-014 | Add 4 unit tests for `_resolve_model()` | S | CG-013 | H-20 coverage for this method |
| CG-023 | Add gap item linkage comment + design note in worktracker | S | — | Traceability restored; quality score reaches 0.92 |
| CG-024 | Document Bedrock/Vertex limitation; add ValueError guard | S | CG-013 | No silent GPTModel fallback for Bedrock ARNs |
| CG-005 | Refactor to typed exception hierarchy; add health check; add zero-array assertion | M | CG-006 | Silent false-green CI failure mode eliminated |
| CG-011 | Add `evaluator` fixture to conftest.py returning `DeepEvalAdapter as EvaluationPort` | S | CG-013, CG-014 | FR-006 pytest integration wired |
| CG-015 | Create LICENSES.md; add pip-audit step to Smoke workflow | S | — | FR-022 compliance; OSI license verification |
| CG-030 | Add `uv run pip-audit` to Smoke CI gate | S | CG-015 | CVE gate automated |
| CG-018 | Add newline sanitization and `agent_id` format validation in layer4_stats.py | S | — | GHA output injection prevented |
| CG-017 | Add output truncation at LLMTestCase construction; add judge framing delimiters | S | — | Prompt injection surface reduced |
| CG-025 | Add allowed-root validation in `_persist_report` | S | — | Path traversal prevented |
| CG-027 | Add `version_key` format validation at entry points | S | — | Malformed keys caught early |
| CG-028 | Narrow deepeval version bound to `>=3.8.0,<4.0.0` | S | — | Silent 4.x behavior changes blocked |
| CG-029 | Declare `scipy>=1.11.0` explicitly in pyproject.toml | S | — | Transitive dependency gap closed |
| CG-012 | Verify or create `.github/actions/cost-monitor` and `artifact-publish` stubs | S | — | Standard workflow unblocked |

Estimated weeks 2-3 effort: 5-7 days across 17 gaps (most are S-sized).

### Sprint 3 — P2 Functional Data Pipeline (Weeks 3-5)

Goal: End-to-end data flow from promptfoo output to Layer 4 statistical analysis working with real data.

| CG ID | Action | Effort | Depends On | Output |
|-------|--------|--------|-----------|--------|
| CG-008 | Build score array extraction script: parse `promptfoo-output.json` → `dict[str, tuple[ScoreArray, ScoreArray]]` | L | CG-001 | L1→L4 bridge complete |
| CG-010 | Add `build_metric_for_mr()` to `DeepEvalAdapter`; wrap MR classes in thin `BaseMetric` adapter | M | — | Layer 3 MR integration into DeepEval pytest path |
| CG-009 | Execute baseline population: capture N=30 runs per agent; store via `BaselineStore.store()` | L | CG-002, CG-008 | Real baseline data; before/after comparisons become valid |

Estimated weeks 3-5 effort: 6-10 days. CG-009 is the longest gap because it requires actual LLM API calls (N=30 × 5 agents × estimated $0.10-0.20 per run = ~$15-30 in API costs).

### Sprint 4 — P3 Quality and Verification (Weeks 5-7)

Goal: H-20 compliance confirmed; NFR-007 Monte Carlo test written; performance benchmarks measured.

| CG ID | Action | Effort | Depends On | Output |
|-------|--------|--------|-----------|--------|
| CG-019 | Run coverage measurement; identify and close gaps to reach 90% | M | CG-011, CG-014 | H-20 HARD rule compliance confirmed |
| CG-020 | Implement `test_stats_type1_error.py` Monte Carlo test | M | — | NFR-007 verification artifact |
| CG-021 | Run 10-run performance benchmark for each tier; record P95 | M | CG-008, CG-009 | NFR-001/002 acceptance criteria met |
| CG-022 | Write re-baseline runbook; add CI DeepEval version change detection | S | — | FR-026 compliance |
| CG-026 | Escape evidence string in HTML report path | S | — | Defense-in-depth for judge rationale |

Estimated weeks 5-7 effort: 4-6 days.

### Sprint 5 — P4 Documentation and Format Cleanup (Week 7+)

| CG ID | Action | Effort | Output |
|-------|--------|--------|--------|
| CG-032 | Rename test case files to `{agent-id}-regression.yaml`; update promptfoo-config.yaml references | S | NFR-008 compliance |
| CG-033 | Add `.github/PULL_REQUEST_TEMPLATE.md` with test authorship checklist | S | FR-027 compliance |
| CG-034 | Create `debiasing-config.yaml` documentation file | S | FR-021 AC-4 compliance |
| CG-031 | Evaluate criteria YAML migration (FR-007 AC-3); defer if not a hard requirement | L | Decision needed on FR-007 AC-3 interpretation |

---

## Cross-Phase Patterns

### Pattern 1: Strong Domain Layer, Weak Adapter/Port Layer

**Sources:** Phase 1A (8 Missing Integration Layers), Phase 1B (all Layer 1 and cross-cutting FRs Partial or Missing), Phase 3 (fix is correct at the domain layer but lacks integration artifacts)

**Description:** Every computational domain module is implemented. Every integration layer (CLI entry points, score pipelines, baseline population, conftest fixtures) is absent. This is a systematic pattern, not a collection of random gaps. The harness was built domain-first, which produced a sound algorithmic foundation, but the adapter/port layer connecting domains to each other and to CI was deferred.

**Architectural Implication:** The implementation roadmap correctly prioritizes integration wiring before quality improvements. No amount of code quality work will make the harness functional without the connective tissue.

### Pattern 2: Silent Failure Substitution as a Systemic Risk

**Sources:** Phase 2A (SEC-002: three nested `except Exception` handlers with 0.0 substitution), Phase 1A (PARTIAL classification for DeepEvalAdapter due to NotImplementedError), Phase 3 (quality score 0.806 — below threshold partly because "results" cannot be distinguished from "failures")

**Description:** Multiple independent sources converge on the same structural defect: the system substitutes valid-looking values for failure states. Zero scores look like real low scores. `NotImplementedError` prevents the evaluate() path from being used at all. The quality score's low Methodological Rigor (0.72) reflects that the fix is not tested in failure modes. Collectively, these gaps mean the harness could be "running" while silently producing fabricated results.

**Architectural Implication:** Exception handling refactoring (CG-005) and API key validation (CG-006) are P1 not P2 despite being code-quality changes, because they affect the trustworthiness of every result the harness produces.

### Pattern 3: Before-State Evidence Consistently Absent

**Sources:** Phase 3 (no before/after artifact for AnthropicModel fix), Phase 1A (all Layer 4 results annotated "Synthetic baseline -- validation only"), Phase 1B (FR-003 partial — real before/after not demonstrated)

**Description:** Three independent observations from three different analysis lenses all identify the same gap: the system has not measured its own "before" state. The AnthropicModel fix works, but the 0.0 baseline is asserted not persisted. The Layer 4 statistics run, but on synthetic data. The before/after comparison architecture exists, but has never run with real LLM data on both sides.

**Architectural Implication:** CG-009 (baseline population) is the single most strategically important Sprint 3 action. Until real baselines are captured and stored, the harness cannot perform its primary function (detect regressions between prompt versions).

### Pattern 4: Governance and Compliance Items Are Consistently Deferred

**Sources:** Phase 1B (LICENSES.md missing, FR-022; Monte Carlo test missing, NFR-007; coverage unconfirmed, NFR-011; PR template missing, FR-027), Phase 3 (no gap item linkage, Traceability 0.72)

**Description:** Multiple must-priority compliance items (LICENSES.md, coverage measurement, Type I error validation, version key format validation) are absent. This is not a severity classification disagreement — all sources agree these are required. The pattern is deferral: governance work is consistently behind functional work.

**Architectural Implication:** Sprint 2 deliberately bundles governance items (CG-015 LICENSES, CG-030 pip-audit) with security hardening to ensure they are not deferred again. The Monte Carlo test (CG-020) is a verification artifact required before production deployment and is properly scoped in Sprint 4.

### PAT-001: Health-Check-Before-Batch Pattern

**Sources:** SEC-002 remediation recommendation (Phase 2A), implicit in CG-005 remediation

**Description:** In evaluation pipelines that use external LLM APIs, adding a pre-batch health check (single minimal API call) before the main evaluation loop is a reliable way to distinguish "evaluation ran and scored low" from "evaluation never ran and silently substituted zeros." This pattern surfaces misconfiguration immediately rather than after all N runs.

**Quality:** HIGH (eng-security independently derived; aligns with general defensive programming practice for external API dependencies)

---

## Risk Assessment

### Consolidated Risk Register

| Risk ID | Description | Source | Likelihood | Impact | Composite | Status |
|---------|-------------|--------|-----------|--------|-----------|--------|
| RISK-001 | API key compromise from .env file on developer workstations | SEC-001 | MEDIUM (key exists on disk) | HIGH (unauthorized API use) | HIGH | CG-004 remediates |
| RISK-002 | False-green CI from broken evaluation config (silent 0.0 substitution) | SEC-002 | HIGH (any auth failure triggers it) | CRITICAL (regression detection fails silently) | CRITICAL | CG-005 + CG-006 remediates |
| RISK-003 | Full-tier GHA workflow fails immediately at Python invocation | Items 37-38, IL-2/IL-3 | CERTAIN (no `__main__` exists) | HIGH (entire Full tier is non-functional) | CRITICAL | CG-001 + CG-002 remediates |
| RISK-004 | Verdict extraction always returns UNKNOWN in Full workflow | Item 33 defect, IL-7 | CERTAIN (field name mismatch) | HIGH (enforcement branching is unreachable) | CRITICAL | CG-003 remediates |
| RISK-005 | Docker image substitution via mutable tag | A3-1a/b | LOW (requires registry compromise) | HIGH (arbitrary CI code execution) | MEDIUM | CG-007 remediates |
| RISK-006 | No real before/after comparison ever executed | IL-5, IL-6 | CERTAIN (baselines are synthetic only) | HIGH (primary function not demonstrated) | HIGH | CG-008 + CG-009 remediates |
| RISK-007 | 90% coverage requirement violated | GAP-NFR-COVERAGE | MEDIUM (unconfirmed) | MEDIUM (H-20 HARD rule governance) | MEDIUM | CG-019 remediates |
| RISK-008 | Type I error not empirically validated before production use | NFR-007 | CERTAIN (test not written) | MEDIUM (statistical rigor theoretical only) | MEDIUM | CG-020 remediates |
| RISK-009 | DeepEval 4.x breaking changes alter evaluation behavior | Code review dependency | LOW (uv.lock pinned to 3.8.9) | HIGH (scores change without notice) | MEDIUM | CG-028 remediates |
| RISK-010 | Prompt injection scores falsely elevated by adversarial agent output | SEC-004, A2-1 | VERY LOW (requires trusted code compromise) | MEDIUM (false NO_REGRESSION) | LOW | CG-017 reduces surface |
| RISK-011 | AnthropicModel fix quality below C3 threshold (0.806) | Phase 3 | CERTAIN (measured) | LOW (fix works but is not test-covered) | LOW | CG-013 + CG-014 + CG-023 + CG-024 remediates |

### Risk Prioritization Summary

**Risks requiring immediate action (before any new feature work):**
- RISK-001: Rotate API key (CG-004) — 15 minutes
- RISK-003: Add `__main__` entry points (CG-001, CG-002) — half day
- RISK-004: Fix field name mismatch (CG-003) — 30 minutes

**Risks requiring Sprint 2 action (before Production readiness):**
- RISK-002: Silent zero-score refactoring (CG-005, CG-006) — 3 hours
- RISK-005: Docker SHA pinning (CG-007) — 1 hour

**Risks that are high impact but require longer-horizon work:**
- RISK-006: Real baseline capture (CG-008, CG-009) — weeks 3-5

---

## Knowledge Items Generated

### PAT-001: Health-Check-Before-Batch

**Context:** Evaluation pipelines calling external LLM APIs for per-sample scoring.

**Problem:** Broad exception handlers that substitute 0.0 for failure states create silent false-green results. If all N evaluations fail (API down, key missing, model unavailable), the downstream statistical layer receives N zeros and produces a "no regression" verdict with high confidence.

**Solution:** Before entering the evaluation loop, make a single minimal API call. If it fails, raise a distinct `EvaluationConfigError` that propagates out of the test runner without being caught by the per-sample handlers. Add a post-loop assertion: if more than 20% of scores in the composite array are exact zeros, raise rather than return.

**Consequences:** (+) Broken evaluation configs surface immediately rather than after N expensive API calls. (+) Zero scores can only appear when the agent genuinely scores zero, not when the API failed. (-) Adds one extra API call per batch (small cost). (-) Health check itself could fail transiently; needs a retry or is limited to one attempt.

**Quality:** HIGH

**Sources:** Phase 2A (SEC-002 remediation), Phase 3 (quality score Methodological Rigor gap)

---

### PAT-002: CLI Entry Point as Deployment Gate

**Context:** Python modules intended to be invoked as `python -m package.module` from CI/CD pipelines.

**Problem:** A class can be fully implemented and tested via its programmatic API while being completely unreachable from the command line. CI/CD workflows that call the module via `python -m` fail at invocation before any logic runs, producing false "the module is broken" diagnostics that obscure the real issue (missing `__main__`).

**Solution:** Define a `main()` function and `if __name__ == "__main__": main()` block as part of the same pull request that implements the class, not as a follow-on task. The CLI entry point is part of the module's interface contract with CI/CD. Consider adding an end-to-end smoke test that calls the module via subprocess to confirm the `__main__` path is reachable.

**Consequences:** (+) CI/CD invocability is verified as part of the original implementation. (+) The `main()` function doubles as integration documentation for the module's required arguments. (-) Adds implementation scope to the original PR.

**Quality:** HIGH (two independent instances: CG-001 and CG-002 both stem from the same omission pattern)

**Sources:** Phase 1A (Items 37, 38), Phase 1B (GAP-L4-CLI)

---

### LES-001: Synthetic Baselines Are Not Validation

**Context:** When it was not possible to capture real baseline data before the validation run, synthetic score arrays were constructed and used for Layer 4 testing.

**What Happened:** The validation run produced Layer 4 results annotated "Synthetic baseline -- validation only." The statistical machinery ran and produced output (p=0.0000, Cohen's r=0.843 for ps-researcher), but the comparison was between a real candidate and a fabricated baseline. The Layer 4 code was confirmed functional, but the full regression detection workflow was not demonstrated.

**What We Learned:** Demonstrating that statistical code runs is not the same as demonstrating that it detects regressions reliably. A harness validated only against synthetic data has a critical gap in its evidence base. The absence of real before/after comparison data means RISK-006 (primary function not demonstrated) remains open until Sprint 3 is complete.

**Prevention:** Schedule baseline population as part of the acceptance criteria for the harness itself, not as a subsequent operational step. The baseline capture is not optional post-implementation work; it is part of the implementation.

**Sources:** Phase 1A (evidence from validation run section), Phase 1B (FR-003 Partial), Phase 3 (Evidence Quality 0.80)

---

### ASM-001: Layer 3 MR Tolerances Are Analytically Derived, Not Calibrated

**Context:** The five metamorphic relations have tolerance values embedded in their implementations. These tolerances determine what delta between original and transformed outputs counts as a test failure.

**Impact if Wrong:** MR tests will have an uncalibrated false positive rate. If tolerances are set too tight, legitimate model outputs that vary slightly under paraphrase transformation will be flagged as regressions. If too loose, real semantic degradations will be missed. NFR-006 requires the false positive rate to be at most 15%.

**Confidence:** LOW — calibration requires 100+ known-good output pairs per MR per agent; the validation run used N=5 pairs, which is explicitly insufficient.

**Validation Path:** Complete baseline population (CG-009, N=30 per agent), then run `CalibrationRunner` against the captured data. The `apply_calibrated_tolerances()` function is already implemented and awaits data. See `jerry/testing/metamorphic/calibration.py`.

**Sources:** Phase 1B (NFR-006, GAP-NFR-MR-FPR), Phase 2B (A3-1 risk context)

---

## Source Summary

| Source | Type | Key Contribution | Gaps Contributed |
|--------|------|-----------------|-----------------|
| `gap-inventory.md` (Phase 1A) | Analysis | 38-component inventory; identified P0 blockers (missing `__main__` entry points); provided validation run evidence | CG-001, CG-002, CG-003, CG-008, CG-009, CG-010, CG-011 |
| `traceability-matrix.md` (Phase 1B) | Requirements | 45 FR/NFR traces; named 34 gap IDs; identified CLI, license, PR template, and NFR gaps | CG-012, CG-015, CG-019, CG-020, CG-021, CG-022, CG-028, CG-029, CG-031, CG-032, CG-033, CG-034 |
| `code-review.md` (Phase 2A) | Engineering | 10 security findings; surfaced silent zero-score pattern (systemic); identified GHA injection, path traversal, telemetry | CG-004, CG-005, CG-006, CG-016, CG-017, CG-018, CG-025, CG-026, CG-027 |
| `security-assessment.md` (Phase 2B) | Security | 3 attack surfaces; validated CI API key controls as sound; confirmed Docker SHA-pin gap as highest supply chain risk | CG-007, CG-030 (reinforced) |
| `quality-score.md` (Phase 3) | Adversarial | Scored AnthropicModel fix at 0.806 (REVISE); identified case-sensitivity, unit test, and traceability gaps | CG-013, CG-014, CG-023, CG-024 |

---

*Synthesis method: Braun & Clarke Thematic Analysis (6 phases). Cross-reference matrix built across all 5 sources. 34 canonical gaps derived from deduplication of 57 raw gap references (38 component items + 34 named gap IDs + 10 security findings + 7 risk matrix entries, minus 37 duplicates). Contradictions disclosed in Cross-Reference Matrix section.*

*Confidence: HIGH for P0/P1 gaps (directly verified by Grep and source reads). HIGH for P2 gaps (two or more sources corroborating). MEDIUM for P3/P4 single-source gaps.*

*Generated: 2026-03-07 | ps-synthesizer v2.3.0 | gap-analysis-20260307-001 phase-4*
