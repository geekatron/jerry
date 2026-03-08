# FEAT-036-001 Completion Prompt

> Multi-skill orchestration prompt for completing the remaining FEAT-036-001 acceptance criteria.
> Built via `/prompt-engineering` pe-builder 5-element anatomy.
> Criticality: C3 (>10 files, API changes, multi-phase pipeline)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Artifact Inventory](#artifact-inventory) | What exists vs what is missing |
| [Prompt](#prompt) | The orchestration prompt to execute |

---

## Artifact Inventory

| AC | Phase | Status | Existing Artifact |
|----|-------|--------|-------------------|
| Requirements with FMEA | 1A | EXISTS, unchecked | `design/harness-requirements.md` |
| System design with STRIDE | 1B | EXISTS, unchecked | `design/system-design.md` |
| Baseline protocol + test prompts | 1C | MISSING | — |
| Behavioral contracts | 1D | MISSING | — |
| Layer 1: promptfoo GitHub Action | 3A | EXISTS, unchecked | `.github/workflows/prompt-regression-*.yml` |
| Layer 2: DeepEval backend | 3B | EXISTS, unchecked | `jerry/testing/evaluation/deepeval_adapter.py`, `jerry/testing/evaluation/criteria/*.py` |
| Layer 3: Metamorphic relations | 3C | EXISTS, unchecked | `jerry/testing/metamorphic/mr_001-005_*.py` |
| Layer 4: Statistical engine | 3D | COMPLETE | `jerry/testing/stats.py`, `jerry/testing/layer4_stats.py` |
| CI/CD Smoke/Standard/Full | 3E | EXISTS, unchecked | `.github/workflows/prompt-regression-{smoke,standard,full}.yml` |
| Security assessment | 5A | EXISTS, unchecked | `design/security-assessment.md` |
| V&V execution | 5B | NEEDS WORK | — |
| Test suite 90% coverage | 5C | PARTIAL | 29 test files across `tests/prompt-regression/` |
| C4 quality gates | — | NEEDS VERIFICATION | — |
| Final dual gate | 8 | NEEDS WORK | — |

> All paths relative to `projects/PROJ-036-prompt-regression-harness/` unless prefixed with `jerry/` or `.github/`.

---

## Prompt

```
Use /worktracker to update FEAT-036-001 status to in_progress.

Use /orchestration with orch-planner to sequence the following 6-phase pipeline
for completing FEAT-036-001: Four-Layer Composite Test Harness Implementation.

Output orchestration plan:
projects/PROJ-036-prompt-regression-harness/orchestration/feat036-completion-001/ORCHESTRATION_PLAN.md

---

Phase 1 — Design Verification and Gap Closure (eng-architect + eng-lead)

Use /eng-team with eng-architect to verify and complete Phases 1A-1D:

1A — Requirements verification:
  Input: projects/PROJ-036-prompt-regression-harness/design/harness-requirements.md
  Task: Verify FMEA traceability is present and complete. Cross-reference against
  ADR-001 (the test harness architecture decision from prior research).
  If gaps found, remediate in-place.

1B — System design verification:
  Input: projects/PROJ-036-prompt-regression-harness/design/system-design.md
  Task: Verify hexagonal architecture compliance (H-07) and STRIDE threat model
  completeness. Confirm all 4 layers are specified with module decomposition.

1C — Baseline protocol creation (MISSING):
  Task: Create the baseline generation protocol and test prompts for 5+ agents
  (ps-researcher, ps-analyst, ps-architect, ps-critic, adv-scorer) across 3+
  cognitive modes (divergent, convergent, integrative).
  Data source: existing agent definitions in skills/*/agents/*.md and evaluation
  criteria in jerry/testing/evaluation/criteria/*.py.
  Output: projects/PROJ-036-prompt-regression-harness/design/baseline-protocol.md

1D — Behavioral contracts creation (MISSING):
  Task: Define behavioral contracts with metamorphic relation tolerances for all
  5 universal metamorphic relations (MR-001 through MR-005).
  Data source: jerry/testing/metamorphic/mr_00{1-5}_*.py for relation definitions,
  jerry/testing/types.py for classification enums and thresholds.
  Output: projects/PROJ-036-prompt-regression-harness/design/behavioral-contracts.md

Use /eng-team with eng-lead to produce standards mapping for Phase 1 deliverables.

Use /adversary with adv-scorer after Phase 1.
Quality threshold: >= 0.92 weighted composite (S-014 LLM-as-Judge, 6 dimensions).
Each Phase 1 deliverable scored independently. Below threshold = revision required.

---

Phase 2 — Implementation Verification (eng-backend + eng-qa)

Use /eng-team with eng-backend to verify Layers 1-3 and CI/CD implementation:

3A — Layer 1 verification:
  Input: .github/workflows/prompt-regression-smoke.yml,
         .github/workflows/prompt-regression-standard.yml,
         .github/workflows/prompt-regression-full.yml
  Task: Verify three-tier workflow modes (Smoke/Standard/Full) are correctly
  configured with appropriate trigger conditions, model pinning, and artifact
  collection.

3B — Layer 2 verification:
  Input: jerry/testing/evaluation/deepeval_adapter.py,
         jerry/testing/evaluation/jerry_geval_deepeval_metric.py,
         jerry/testing/evaluation/criteria/*.py
  Task: Verify DeepEval evaluation backend implements debiased LLM-as-Judge scoring.
  Confirm JERRY_JUDGE_MODEL env var override works per EN-036-001.
  Confirm 5 agent criteria files exist and match baseline protocol agents.

3C — Layer 3 verification:
  Input: jerry/testing/metamorphic/mr_001_*.py through mr_005_*.py
  Task: Verify 5 universal metamorphic relations are implemented as custom DeepEval
  metrics. Cross-reference against behavioral contracts from Phase 1D.

3E — CI/CD verification:
  Input: .github/workflows/prompt-regression-{smoke,standard,full}.yml,
         Dockerfile (if exists), docker-compose.yml (if exists)
  Task: Verify pipeline supports Smoke ($0 cost), Standard (~$2), and Full (~$5-8)
  evaluation modes with correct environment variable propagation.

Use /eng-team with eng-qa to verify test coverage for Layers 1-3:
  Input: tests/prompt-regression/ (all subdirectories)
  Task: Assess current test coverage. Identify gaps against 90% line coverage target (H-20).
  Produce coverage gap report.

Use /adversary with adv-scorer after Phase 2.
Quality threshold: >= 0.92 weighted composite per deliverable.

---

Phase 3 — Security Assessment (eng-security + red-team)

Use /eng-team with eng-security to verify Phase 5A security assessment:
  Input: projects/PROJ-036-prompt-regression-harness/design/security-assessment.md
  Task: Verify security assessment covers the harness itself — not just what the
  harness tests. Check for: input sanitization of score arrays (RR-001),
  Docker digest pinning (RR-002), API key handling, CI/CD secret exposure,
  supply chain integrity of DeepEval dependency.

Use /red-team with red-lead to scope a security review of the test harness:
  Scope: jerry/testing/ module, .github/workflows/prompt-regression-*.yml,
         Dockerfile and CI/CD configuration.
  Rules of engagement: Read-only analysis, no active exploitation.
  Task: red-vuln performs vulnerability identification on the test harness
  attack surface. Focus on: dependency chain (DeepEval, scipy, numpy),
  environment variable injection vectors, score manipulation risks,
  CI/CD pipeline privilege escalation.

Use /adversary with adv-scorer after Phase 3.
Quality threshold: >= 0.92 weighted composite per deliverable.

---

Phase 4 — V&V Execution and Test Coverage (eng-qa)

Use /eng-team with eng-qa to execute Phase 5B-5C:

5B — V&V execution:
  Task: Execute verification and validation against harness-requirements.md.
  Trace each requirement to its implementing module and test.
  Produce a requirements traceability matrix (RTM).
  Output: projects/PROJ-036-prompt-regression-harness/work/EPIC-036-001-test-harness/FEAT-036-001-implementation/vv-report.md

5C — Test suite completion:
  Input: tests/prompt-regression/ (29 existing test files)
  Task: Identify coverage gaps against 90% line coverage target.
  Write missing tests for uncovered modules. Run full suite via uv run pytest.
  Ensure property-based tests exist for statistical functions (Layer 4).
  Output: Updated test files + coverage report.

Use /adversary with adv-scorer after Phase 4.
Quality threshold: >= 0.92 weighted composite per deliverable.

---

Phase 5 — Quality Gate Verification (eng-reviewer + /adversary)

Use /eng-team with eng-reviewer as final quality gate:
  Task: Verify all FEAT-036-001 deliverables pass C4 quality gates
  (>= 0.95 S-014 weighted composite per quality-enforcement.md).
  Input: All artifacts produced in Phases 1-4 plus existing Phase 3D artifacts.
  Verification scope:
  - Architecture compliance (hexagonal layers, H-07)
  - Security standards compliance (OWASP, input validation)
  - Test coverage (>= 90%, H-20)
  - Requirements traceability (RTM from Phase 4)

Use /adversary with adv-selector at C4 criticality to select all 10 strategies.
Use /adversary with adv-executor to execute each strategy against the consolidated
deliverable set.
Use /adversary with adv-scorer for final quality scoring.
Quality threshold: >= 0.95 weighted composite (C4 requirement).

---

Phase 6 — Final Dual Gate (eng-reviewer + nse-reviewer)

Use /eng-team with eng-reviewer for engineering final review:
  Task: Confirm all 14 FEAT-036-001 acceptance criteria are satisfied.
  Produce a checklist with evidence links for each AC.

Use /nasa-se with nse-reviewer for NASA SE technical review:
  Task: Execute a CDR-equivalent technical review gate per NPR 7123.1D Appendix G.
  Verify entrance criteria: requirements baselined, design complete, V&V executed,
  risks mitigated.

Use /adversary with adv-scorer for final gate scoring.
Quality threshold: >= 0.95 weighted composite.

Output final report:
projects/PROJ-036-prompt-regression-harness/work/EPIC-036-001-test-harness/FEAT-036-001-implementation/final-review-report.md

Upon pass: Use /worktracker to mark FEAT-036-001 as completed.
```
