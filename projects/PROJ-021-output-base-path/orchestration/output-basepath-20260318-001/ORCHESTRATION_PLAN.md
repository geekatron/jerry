# Configurable Output Base Path: Orchestration Plan

> **Document ID:** PROJ-021-ORCH-PLAN
> **Workflow ID:** output-basepath-20260318-001
> **Date:** 2026-03-18
> **Status:** PLANNED
> **Revision:** 2026-03-18 (v1.2) — Execution evidence requirements: 6 evidence gates, AC-3 known gap documented, criticality escalated to C3

## Document Sections

| Section | Purpose |
|---------|---------|
| [Scope Change Log](#scope-change-log) | Revision history and rationale for plan updates |
| [L0: Workflow Overview](#l0-workflow-overview) | Plain-language description for stakeholders |
| [L1: Technical Plan](#l1-technical-plan) | Workflow diagram, pipeline definitions, barrier definitions |
| [L2: Implementation Details](#l2-implementation-details) | State schema, path configuration, recovery strategies |
| [Evidence Artifact Registry](#evidence-artifact-registry) | Required execution evidence files with gate status and commands |
| [Disclaimer](#disclaimer) | Required output disclaimer |

---

## Scope Change Log

| Date | Revision | Author | Summary |
|------|----------|--------|---------|
| 2026-03-18 | v1.0 | orch-planner v2.2.0 | Initial plan created. Assumed 6 affected agents did not yet exist. |
| 2026-03-18 | v1.1 | orch-planner v2.2.0 | **Scope update:** All 6 agents confirmed present after fetching origin/main. Phase et-2 expanded to include governance YAML modifications. Phase nse-2 updated with concrete BDD targets. Phase et-3 updated with schema validation scope. File count revised from 5 to 11. Criticality reassessed. |
| 2026-03-18 | v1.2 | orch-planner v2.2.0 | **Execution evidence requirements:** 6 gaps identified in v1.1 (no baseline, no CLI test, no E2E resolver test, no `fallback_location` audit, no final full run, summaries instead of raw output). Added 6 evidence gates and Evidence Artifact Registry. AC-3 known gap documented. Criticality escalated to C3 (OSS trust concern + evidence gate overhead). |

### v1.2 Change Detail

**Trigger:** Review of v1.1 identified that all acceptance criteria were verified by documentation artifacts and summaries only — no raw terminal output, no CLI execution, no regression baseline. For an open-source repository, this is insufficient; contributors and reviewers cannot reproduce the verification independently.

**Gaps addressed in this revision:**

| Gap | Root Cause in v1.1 | Fix Applied |
|-----|--------------------|-------------|
| Gap 1: No baseline test run | No pre-implementation step | Added pre-et-2 baseline gate (`evidence/test-results-baseline.txt`) |
| Gap 2: No CLI integration test | AC-1/AC-2 verified only via unit tests | Added CLI round-trip execution in et-2 (`evidence/test-results-cli.txt`) |
| Gap 3: No E2E agent resolution test | AC-3 assumed governance YAML + resolver = runtime enforcement | Added integration test; AC-3 known gap explicitly documented |
| Gap 4: No `fallback_location` audit | Removal assumed safe without code search | Added grep audit gate before YAML edits (`evidence/fallback-location-audit.txt`) |
| Gap 5: No final full test run | et-3 ran pytest but saved summary in `.md`, not raw output | Final run saves to `evidence/test-results-final.txt`; compared to baseline |
| Gap 6: Summaries instead of raw output | `test-results.md` described results | All evidence files are `.txt` raw terminal output; `.md` summaries derive from them |

**What changed in this revision:**

| Area | v1.1 | v1.2 |
|------|------|------|
| Phase et-2 steps | Implementation, then quality gate | Pre-implementation baseline gate added; `fallback_location` audit gate before YAML edits; CLI and E2E evidence captured after implementation |
| Phase et-3 eng-reviewer | Ran pytest, saved summary | Saves full output to `evidence/test-results-final.txt`; compares to baseline |
| New section | (none) | Evidence Artifact Registry with 6 entries |
| AC-3 treatment | Assumed resolver + YAML = runtime enforcement | Explicitly documented as partially satisfied; runtime enforcement mechanism noted as out-of-scope for this issue |
| Criticality | C2 (retained from v1.1) | **Escalated to C3** (see updated [Criticality Assessment](#criticality-assessment)) |
| ORCHESTRATION.yaml | 5 evidence artifacts listed in outputs | 6 evidence artifacts; `evidence_gates` section added under `quality`; strategies updated for C3 |

**What did NOT change:**
- Pipeline structure, barrier definitions, and quality gate thresholds
- Execution queue phase order
- Agent assignments
- Governance YAML edit instructions

### v1.1 Change Detail

**Trigger:** Git fetch from origin/main revealed all 6 PROJ-021 skill agents are present in the codebase with existing `output.location` and `fallback_location` fields in their `.governance.yaml` files.

**What changed in this revision:**

| Area | v1.0 | v1.1 |
|------|------|------|
| Phase et-2 file scope | 5 files (3 new Python + 2 modified) | 11 files (original 5 + 6 governance YAMLs modified) |
| Phase et-2 eng-backend instructions | Create Python infrastructure only | Also: update 6 `.governance.yaml` output.location fields and remove redundant `fallback_location` fields |
| Phase nse-2 BDD targets | Abstract scenario stubs | Concrete scenarios exercising real governance YAML resolution |
| Phase et-3 eng-reviewer scope | H-07/H-10/H-11/H-20 Python standards | Added: JSON Schema validation of all 6 governance YAMLs after output.location format change |
| Criticality | C2 (5 files) | C2 retained with documented rationale (see [Criticality Assessment](#criticality-assessment)) |
| ORCHESTRATION.yaml metrics.files_affected_estimate | 5 | 11 |

**What did NOT change:**
- Pipeline structure (et + nse, 3 phases each)
- Barrier definitions (BARRIER-1, BARRIER-2, BARRIER-3)
- Quality gate thresholds (>= 0.93)
- Execution queue order
- Agent assignments

---

## L0: Workflow Overview

Jerry's skill agents currently assume all output goes to `projects/${JERRY_PROJECT}/`. Users who organize their repos with a `work/` directory (the repository-based placement pattern) or who don't set `JERRY_PROJECT` must manually correct every agent output path before running them. This is friction that blocks adoption of the repo-based pattern and makes the framework hostile to new users.

This workflow implements GitHub Issue #192: a `jerry config set output.base_path <path>` command and a `${JERRY_OUTPUT_BASE}` variable that agents can reference. When a user configures a base path it is resolved at invocation time; when nothing is configured the system falls back gracefully: first to `projects/${JERRY_PROJECT}/`, then to `work/`. The change affects the configuration domain, bootstrap layer, and a set of infrastructure files. No new CLI commands are needed — the existing `jerry config set/get` machinery already works.

Following a fetch from origin/main, all 6 affected skill agents (`uc-author`, `uc-slicer`, `tspec-generator`, `tspec-analyst`, `cd-generator`, `cd-validator`) are confirmed present in the codebase. Each currently hardcodes `projects/${JERRY_PROJECT}/` in its `output.location` governance field and carries a `fallback_location` field for the `work/` case. Both of these fields must be updated as part of this implementation: `output.location` is rewritten to use `${JERRY_OUTPUT_BASE}`, and `fallback_location` is removed because the fallback chain is now fully owned by `OutputResolver`. This raises the implementation file count from 5 to 11 but does not change the criticality classification (see [Criticality Assessment](#criticality-assessment)).

The workflow runs two parallel pipelines. The engineering pipeline (eng-team) handles architecture, implementation, BDD tests, security review, and final code review. The systems-engineering pipeline (nasa-se) handles requirements decomposition, verification planning, and a formal technical review gate. The pipelines cross-pollinate at three sync barriers: requirements feed the architecture decision before implementation begins, the completed implementation is handed to verification before security review, and all findings converge in a joint final review. Every phase boundary includes a mandatory `/adversary` quality gate scored against the 6-dimension S-014 rubric. Nothing proceeds to the next phase until the gate score reaches >= 0.93.

As of v1.2, the plan requires six concrete execution evidence gates — raw terminal output captured to `.txt` files — in addition to documentation artifacts. This is non-negotiable for an open-source repository where contributors must be able to reproduce verification independently. A baseline test run must pass before implementation begins; CLI round-trip must execute against the real binary; a `fallback_location` code audit must precede any YAML deletion; and a final full regression run must be compared to the baseline before merge. One known gap is explicitly documented: AC-3 ("agent output.location fields resolve `${JERRY_OUTPUT_BASE}` at invocation time") is partially satisfied — the resolver mechanism works, but runtime enforcement of the governance YAML `output.location` field at agent invocation time is out of scope for this issue and is logged as a follow-up item.

---

## L1: Technical Plan

### Workflow Diagram (ASCII)

```
DATE: 2026-03-18           WORKFLOW: output-basepath-20260318-001
REVISION: v1.2 (2026-03-18) -- 6 evidence gates; AC-3 known gap; C3 escalation
CRITICALITY: C3 (Significant) QUALITY GATE: >= 0.93 (S-014)

Pipeline A: eng-team (et)          Pipeline B: nasa-se (nse)
=================================  ================================

PHASE et-1: Architecture           PHASE nse-1: Requirements
  eng-architect                      nse-requirements
  - Output path resolution design    - Decompose AC 1-5 into reqs
  - Domain layer: OutputBasePath VO  - Define verification criteria
  - Application svc: OutputResolver  - Classify by MoSCoW
  - Config key: output.base_path     - Identify test oracles
       |                                  |
       v                                  v
  [QG-et-1: adv score >= 0.93]     [QG-nse-1: adv score >= 0.93]
       |                                  |
       +----------------+-----------------+
                        |
              ╔═════════════════╗
              ║   BARRIER-1     ║
              ║ Requirements    ║
              ║ Cross-Pollinate ║
              ║ QG >= 0.93      ║
              ╚═════════════════╝
                        |
         nse -> et: formal requirements doc
         et -> nse: architecture sketch for V&V testability review
                        |
       +-----------------+-----------------+
       |                                   |
       v                                   v
  [EVIDENCE GATE 1]                  PHASE nse-2: V&V Planning
  Baseline test run (pre-et-2)         nse-verification
  evidence/test-results-baseline.txt - Write V&V plan from reqs
  GATE: must pass before et-2 starts - BDD scenarios against real
       |                                governance YAML files (AC-3)
       v                              - Acceptance test matrix
PHASE et-2: Implementation           - Traceability matrix (AC->test)
  eng-backend
  [EVIDENCE GATE 2 -- before YAML edits]
  Audit: grep -r "fallback_location"
  evidence/fallback-location-audit.txt
  GATE: no Python reads the field
  - OutputBasePath value object
  - OutputResolver application svc
  - Bootstrap integration
  - LayeredConfigAdapter default
  - 6x .governance.yaml: replace
    output.location + rm fallback
  - BDD tests (RED phase first)
  [EVIDENCE GATE 3]
  CLI round-trip: jerry config set/get
  evidence/test-results-cli.txt
  GATE: AC-1 and AC-2 end-to-end
  [EVIDENCE GATE 4]
  Unit tests: uv run pytest tests/unit/
  evidence/test-results-unit.txt
  GATE: GREEN + AC-3 partial (known gap)
  [EVIDENCE GATE 5]
  E2E resolver + governance YAML
  evidence/test-results-e2e.txt
  GATE: resolver resolves; AC-3 gap doc
  - eng-qa: test strategy doc
       |                                  |
       v                                  v
  [QG-et-2: adv score >= 0.93]     [QG-nse-2: adv score >= 0.93]
       |                                  |
       +----------------+-----------------+
                        |
              ╔═════════════════╗
              ║   BARRIER-2     ║
              ║ Implementation  ║
              ║ + V&V Handoff   ║
              ║ QG >= 0.93      ║
              ╚═════════════════╝
                        |
         et -> nse: implemented code artifacts + test results
         nse -> et: V&V plan for security review scope
                        |
       +-----------------+-----------------+
       |                                   |
       v                                   v
PHASE et-3: Security + Final       PHASE nse-3: Technical Review
  eng-security                       nse-reviewer
  - Path traversal risk review       - SRR gate: reqs vs. impl
  - Env var injection review         - Verify V&V plan executed
  - Config scope abuse review        - Traceability sign-off
  - 6x governance YAML consistency   - Open action items
  eng-reviewer
  - Code standards gate (H-07, H-10, H-11)
  - JSON Schema validation: all 6
    governance YAMLs post-edit
  [EVIDENCE GATE 6]
  Final full run + regression check
  evidence/test-results-final.txt
  GATE: GREEN + cov >= 90% + no
  regressions vs. baseline
       |                                  |
       v                                  v
  [QG-et-3: adv score >= 0.93]     [QG-nse-3: adv score >= 0.93]
       |                                  |
       +----------------+-----------------+
                        |
              ╔═════════════════╗
              ║   BARRIER-3     ║
              ║  Joint Final    ║
              ║  Review Gate    ║
              ║  QG >= 0.93     ║
              ╚═════════════════╝
                        |
              WORKFLOW COMPLETE
              Status: READY_FOR_MERGE
```

---

### Pipeline Definitions

#### Pipeline A: eng-team (alias: et)

| Phase | ID | Agent | Inputs | Outputs | Quality Gate |
|-------|----|-------|--------|---------|--------------|
| Architecture | et-1 | eng-architect | Issue #192 context, codebase survey | ADR: output path resolution design | /adversary score >= 0.93 |
| Implementation | et-2 | eng-backend + eng-qa | BARRIER-1 requirements, ADR from et-1; baseline evidence gate must pass first | OutputBasePath VO, OutputResolver svc, bootstrap patch, 6x governance YAML edits, BDD tests (RED+GREEN), test strategy; evidence gates 1-5 captured | /adversary score >= 0.93 |
| Security + Review | et-3 | eng-security + eng-reviewer | BARRIER-2 V&V plan, all code artifacts + evidence files 1-5 | Security findings report, code review gate doc (incl. schema validation), evidence gate 6 (final full run vs. baseline) | /adversary score >= 0.93 |

**Phase et-1 Agent Detail (eng-architect):**
- Read: `src/configuration/domain/`, `src/bootstrap.py`, `src/infrastructure/adapters/configuration/layered_config_adapter.py`
- Decide: where `OutputBasePath` value object lives (configuration domain vs. shared kernel)
- Decide: where `OutputResolver` application service lives (configuration application layer)
- Decide: default key name (`output.base_path`), TOML section (`[output]`), env var (`JERRY_OUTPUT__BASE_PATH`)
- Decide: fallback chain implementation approach (strategy pattern vs. conditional in resolver)
- Output: `orchestration/{workflow_id}/et/phase-et-1/ADR-PROJ021-001-output-path-resolution.md`

**Phase et-2 Agent Detail (eng-backend):**

**Step 0 — Evidence Gate 1: Baseline test run (GATE — must pass before any code changes)**
```bash
uv run pytest tests/ --cov=src --cov-report=term-missing --tb=short 2>&1 | \
  tee orchestration/output-basepath-20260318-001/evidence/test-results-baseline.txt
```
- Capture full raw terminal output to `evidence/test-results-baseline.txt`
- GATE: all existing tests must pass. If any fail, stop — do not proceed with implementation until the pre-existing failures are understood and either fixed or documented as pre-existing known failures. Do not hide pre-existing failures in the implementation diff.

**Step 1 — Evidence Gate 2: `fallback_location` usage audit (GATE — must run before any governance YAML edits)**
```bash
grep -r "fallback_location" src/ skills/ tests/ \
  --include="*.py" --include="*.md" --include="*.yaml" \
  2>&1 | tee orchestration/output-basepath-20260318-001/evidence/fallback-location-audit.txt
```
- Capture full output. If the grep returns no Python (`.py`) matches, it is safe to remove `fallback_location`. If any `.py` file reads this field, stop — the removal plan must be revised. YAML/MD matches are expected (the governance files themselves) and are not blocking.

**Step 2 — Python implementation (BDD test-first per H-20)**
- Implement BDD tests FIRST (RED phase per H-20), then GREEN
- Files to create/modify (expected scope, subject to ADR from et-1):

  **Python infrastructure (original scope):**
  - `src/configuration/domain/value_objects/output_base_path.py` (new)
  - `src/configuration/application/services/output_resolver.py` (new)
  - `src/configuration/application/services/__init__.py` (new or update)
  - `src/infrastructure/adapters/configuration/layered_config_adapter.py` (add default key)
  - `src/bootstrap.py` (integrate OutputResolver, update `get_project_data_path`)
  - `tests/unit/configuration/domain/value_objects/test_output_base_path.py` (new BDD)
  - `tests/unit/configuration/application/services/test_output_resolver.py` (new BDD)
  - `tests/integration/test_bootstrap_output_resolver.py` (new integration)

  **Governance YAML edits (v1.1 scope addition — 6 files):**
  - `skills/use-case/agents/uc-author.governance.yaml`: change `output.location` from `projects/${JERRY_PROJECT}/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md` to `${JERRY_OUTPUT_BASE}use-cases/UC-{DOMAIN}-{NNN}-{slug}.md`; remove `fallback_location` field
  - `skills/use-case/agents/uc-slicer.governance.yaml`: same pattern — `output.location` -> `${JERRY_OUTPUT_BASE}use-cases/...`; remove `fallback_location`
  - `skills/test-spec/agents/tspec-generator.governance.yaml`: `output.location` -> `${JERRY_OUTPUT_BASE}test-specs/...`; remove `fallback_location`
  - `skills/test-spec/agents/tspec-analyst.governance.yaml`: `output.location` -> `${JERRY_OUTPUT_BASE}test-specs/...`; remove `fallback_location`
  - `skills/contract-design/agents/cd-generator.governance.yaml`: `output.location` -> `${JERRY_OUTPUT_BASE}contracts/...`; remove `fallback_location`
  - `skills/contract-design/agents/cd-validator.governance.yaml`: `output.location` -> `${JERRY_OUTPUT_BASE}contracts/...`; remove `fallback_location`

  **Governance YAML edit rules:**
  - The `${JERRY_OUTPUT_BASE}` token is written exactly as shown — no trailing slash in the token itself; the path separator between `${JERRY_OUTPUT_BASE}` and the subdirectory is the responsibility of `OutputResolver.resolve()` (must ensure trailing slash before concatenation)
  - `fallback_location` is removed entirely from all 6 files; its semantics are absorbed by the fallback chain in `OutputResolver`
  - All other fields in each `.governance.yaml` remain unchanged
  - After each edit, verify the file still parses as valid YAML (`uv run python -c "import yaml; yaml.safe_load(open('path'))"` or equivalent)

**Step 3 — Evidence Gate 3: CLI integration test (proves AC-1 and AC-2 end-to-end)**
```bash
{
  echo "=== AC-1: Persistent storage ==="
  uv run jerry config set output.base_path work/ --scope root
  echo "=== AC-2: Retrieval ==="
  uv run jerry config get output.base_path
  echo "=== Round-trip: project-based path ==="
  uv run jerry config set output.base_path projects/PROJ-021-output-base-path/ --scope root
  uv run jerry config get output.base_path
  echo "=== Cleanup: restore no configured path ==="
  uv run jerry config set output.base_path "" --scope root || true
} 2>&1 | tee orchestration/output-basepath-20260318-001/evidence/test-results-cli.txt
```
- GATE: all commands must exit 0 and `config get` must echo the value just set. Any error exits are blocking.
- Note: the cleanup step is best-effort (`|| true`) — its failure does not block the gate, but must be noted in the implementation summary.

**Step 4 — Evidence Gate 4: Unit tests**
```bash
uv run pytest tests/unit/ -v --tb=short 2>&1 | \
  tee orchestration/output-basepath-20260318-001/evidence/test-results-unit.txt
```
- GATE: all unit tests must be GREEN, including the new `test_output_base_path.py` and `test_output_resolver.py` tests.

**Step 5 — Evidence Gate 5: E2E resolver and governance YAML test**
```bash
uv run pytest tests/integration/test_bootstrap_output_resolver.py -v --tb=short 2>&1 | \
  tee orchestration/output-basepath-20260318-001/evidence/test-results-e2e.txt
```
- GATE: integration test must pass, demonstrating the full three-case fallback chain works with the real `LayeredConfigAdapter`.
- **AC-3 Known Gap (document in the test and in `evidence/test-results-e2e.txt`):** The governance YAML `output.location` field with `${JERRY_OUTPUT_BASE}` is a behavioral specification — agents read it as a hint for where to write output. The variable is present in the YAML after this change, and `OutputResolver.resolve()` produces the correct path. However, the mechanism by which a running agent substitutes `${JERRY_OUTPUT_BASE}` in `output.location` at invocation time is not built by this issue — it depends on the agent invocation framework reading and interpolating governance YAML fields. This is a known gap. The gap must be documented in `evidence/test-results-e2e.txt` and in the implementation summary as a follow-up item. Do not falsely claim AC-3 is fully satisfied.

**Phase et-2 Agent Detail (eng-qa):**
- Write test strategy document covering: unit scope, integration scope, coverage target (>= 90%), oracle sources (the 5 ACs from the issue), edge cases (missing env, both set, path traversal)
- Output: `orchestration/{workflow_id}/et/phase-et-2/test-strategy.md`

**Phase et-3 Agent Detail (eng-security):**
- Apply STRIDE to `OutputResolver`: spoofing (env var impersonation), tampering (config file injection), information disclosure (path traversal via `${JERRY_OUTPUT_BASE}`)
- Check: does the resolver sanitize user-supplied paths against directory traversal (e.g., `../../etc/passwd`)?
- Check: is the env var `JERRY_OUTPUT__BASE_PATH` documented and scoped correctly?
- Check (v1.1 addition): are all 6 governance YAML `output.location` values consistent with each other? Verify no agent retained a hardcoded `projects/${JERRY_PROJECT}/` prefix or a `fallback_location` field. Inconsistency across the 6 files at this point would indicate a partial edit — flag as HIGH severity.
- Output: `orchestration/{workflow_id}/et/phase-et-3/security-review.md`

**Phase et-3 Agent Detail (eng-reviewer):**
- Verify H-07 (hexagonal layer isolation: OutputResolver in application layer, OutputBasePath in domain, no domain→infra imports)
- Verify H-10 (one class per file)
- Verify H-11 (type hints + docstrings on all public methods)
- Verify H-20 (BDD test-first evidence; coverage to be confirmed by Evidence Gate 6 below)
- Verify (v1.1 addition — JSON Schema validation): run `uv run jerry agents validate` or equivalent schema check against all 6 modified `.governance.yaml` files. Each must pass `docs/schemas/agent-governance-v1.schema.json` validation. Confirm `fallback_location` is optional in the schema before accepting removal.
- Read `evidence/test-results-baseline.txt` and confirm it shows a clean baseline.
- Read `evidence/fallback-location-audit.txt` and confirm no Python code reads `fallback_location`.
- Read `evidence/test-results-cli.txt` and confirm AC-1 and AC-2 CLI round-trips pass.
- Read `evidence/test-results-unit.txt` and confirm unit tests GREEN.
- Read `evidence/test-results-e2e.txt` and confirm integration tests pass; verify AC-3 known gap is documented.

**Evidence Gate 6 — Final full test suite run (eng-reviewer final action before quality gate):**
```bash
uv run pytest tests/ --cov=src --cov-report=term-missing --tb=short 2>&1 | \
  tee orchestration/output-basepath-20260318-001/evidence/test-results-final.txt
```
- GATE: all tests GREEN. Coverage >= 90% line coverage across `src/`. No regressions versus `evidence/test-results-baseline.txt` (compare test counts and test IDs — any test present in baseline but absent or failing in final is a blocking regression).
- Regression comparison procedure: count passing tests in baseline; count passing tests in final; if final count is lower, identify missing tests by diffing the test IDs. A newly added test that fails is also a blocker.
- Output: `orchestration/{workflow_id}/et/phase-et-3/code-review-gate.md`

---

#### Pipeline B: nasa-se (alias: nse)

| Phase | ID | Agent | Inputs | Outputs | Quality Gate |
|-------|----|-------|--------|---------|--------------|
| Requirements | nse-1 | nse-requirements | GitHub Issue #192 AC 1-5, codebase context | Formal requirements doc (SRS-style), MoSCoW classification, verification criteria | /adversary score >= 0.93 |
| V&V Planning | nse-2 | nse-verification | BARRIER-1 ADR, formal requirements | V&V plan, BDD scenario stubs, AC-to-test traceability matrix | /adversary score >= 0.93 |
| Technical Review | nse-3 | nse-reviewer | BARRIER-2 code artifacts, V&V plan | SRR gate doc, traceability sign-off, open action items | /adversary score >= 0.93 |

**Phase nse-1 Agent Detail (nse-requirements):**
- Decompose the 5 acceptance criteria into testable requirements using SHALL statements
- Classify: AC-1 (config set persistence) = SHALL; AC-2 (config get retrieval) = SHALL; AC-3 (variable resolution at invocation) = SHALL; AC-4 (fallback to JERRY_PROJECT) = SHALL; AC-5 (fallback to work/) = SHALL
- Identify edge cases: what if output.base_path is a relative path? what if the configured path does not exist?
- Output: `orchestration/{workflow_id}/nse/phase-nse-1/requirements.md`

**Phase nse-2 Agent Detail (nse-verification):**
- Map each SHALL requirement to one or more BDD scenarios
- Write Gherkin-style scenario stubs for eng-backend to implement
- Define: acceptance test matrix with pass/fail oracles for each AC
- v1.1 addition — concrete BDD targets for AC-3 (agent output.location variable resolution):
  - Scenario: "Given `output.base_path` is set to `/custom/output/`, when `uc-author` resolves its output path, then the resolved path begins with `/custom/output/use-cases/`"
  - Scenario: "Given `output.base_path` is not set and `JERRY_PROJECT=PROJ-021`, when `uc-author` resolves its output path, then the resolved path begins with `projects/PROJ-021/use-cases/`"
  - Scenario: "Given `output.base_path` is not set and `JERRY_PROJECT` is unset, when `uc-author` resolves its output path, then the resolved path begins with `work/use-cases/`"
  - The above three scenarios apply symmetrically to all 6 agents (`uc-author`, `uc-slicer`, `tspec-generator`, `tspec-analyst`, `cd-generator`, `cd-validator`). nse-verification must list each agent as a test target, with the concrete file paths from their `.governance.yaml` as the oracle.
  - Scenario: "Given any of the 6 governance YAMLs is loaded, then its `output.location` field contains `${JERRY_OUTPUT_BASE}` and does NOT contain `${JERRY_PROJECT}`"
  - Scenario: "Given any of the 6 governance YAMLs is loaded, then no `fallback_location` field is present"
- Output: `orchestration/{workflow_id}/nse/phase-nse-2/vv-plan.md`

**Phase nse-3 Agent Detail (nse-reviewer):**
- Compare implemented code against requirements from nse-1
- Verify each AC has a passing test in the test suite
- Review traceability matrix: every requirement must have a test, every test must trace to a requirement
- Record open action items (if any) blocking READY_FOR_MERGE
- Output: `orchestration/{workflow_id}/nse/phase-nse-3/srr-gate.md`

---

### Sync Barriers

| Barrier | ID | Condition | Artifacts Crossing (et -> nse) | Artifacts Crossing (nse -> et) | Quality Gate |
|---------|----|-----------|-------------------------------|-------------------------------|--------------|
| Requirements Sync | BARRIER-1 | et-1 PASS AND nse-1 PASS | ADR-PROJ021-001 (architecture sketch for testability review) | requirements.md (formal SHALLs for architecture alignment) | Both pipelines >= 0.93 before barrier opens |
| Implementation Sync | BARRIER-2 | et-2 PASS AND nse-2 PASS | Code artifacts list + test results summary | vv-plan.md (for security review scope definition) | Both pipelines >= 0.93 before barrier opens |
| Final Review | BARRIER-3 | et-3 PASS AND nse-3 PASS | security-review.md + code-review-gate.md | srr-gate.md (traceability sign-off) | Both pipelines >= 0.93; combined composite >= 0.93 |

**Barrier behavior:**
- If either pipeline is below 0.93 at a barrier, the failing pipeline enters a revision cycle (max 3 iterations per H-14).
- If 3 iterations exhaust without reaching 0.93, the barrier escalates to human review per H-31.
- The passing pipeline waits at the barrier; it does not proceed to its next phase until the barrier opens.

---

## L2: Implementation Details

### Architectural Scope

The implementation touches the following hexagonal architecture layers:

```
DOMAIN LAYER (src/configuration/domain/)
  + output_base_path.py          NEW: OutputBasePath value object
    - Wraps a string path
    - Validates: non-empty, no null bytes
    - Does NOT validate path existence (existence is infra concern)

APPLICATION LAYER (src/configuration/application/services/)
  + output_resolver.py           NEW: OutputResolver application service
    - resolve() -> str method
    - Fallback chain:
        1. config.get("output.base_path")  [via LayeredConfigAdapter]
        2. os.environ.get("JERRY_OUTPUT__BASE_PATH")  [already via env layer]
        3. "projects/" + JERRY_PROJECT  [if JERRY_PROJECT set]
        4. "work/"  [terminal fallback]
    - No direct filesystem calls; delegates to config port
    - resolve() guarantees trailing slash on returned path

INFRASTRUCTURE LAYER (src/infrastructure/adapters/configuration/)
  ~ layered_config_adapter.py    MODIFY: add "output.base_path" to defaults
    - Default value: None (no default path; forces resolver to use fallback chain)

BOOTSTRAP (src/bootstrap.py)
  ~ get_project_data_path()      MODIFY: integrate OutputResolver
    - Call OutputResolver.resolve() instead of hardcoded "projects/" + project_id
    - Keep backward compatibility: existing callers get same string return type

TESTS
  + tests/unit/configuration/domain/value_objects/test_output_base_path.py
  + tests/unit/configuration/application/services/test_output_resolver.py
  + tests/integration/test_bootstrap_output_resolver.py

AGENT GOVERNANCE YAML (skills/ -- v1.1 scope addition)
  ~ skills/use-case/agents/uc-author.governance.yaml
      output.location:    projects/${JERRY_PROJECT}/use-cases/...
                       -> ${JERRY_OUTPUT_BASE}use-cases/...
      fallback_location:  REMOVED

  ~ skills/use-case/agents/uc-slicer.governance.yaml
      output.location:    projects/${JERRY_PROJECT}/use-cases/...
                       -> ${JERRY_OUTPUT_BASE}use-cases/...
      fallback_location:  REMOVED

  ~ skills/test-spec/agents/tspec-generator.governance.yaml
      output.location:    projects/${JERRY_PROJECT}/test-specs/...
                       -> ${JERRY_OUTPUT_BASE}test-specs/...
      fallback_location:  REMOVED

  ~ skills/test-spec/agents/tspec-analyst.governance.yaml
      output.location:    projects/${JERRY_PROJECT}/test-specs/...
                       -> ${JERRY_OUTPUT_BASE}test-specs/...
      fallback_location:  REMOVED

  ~ skills/contract-design/agents/cd-generator.governance.yaml
      output.location:    projects/${JERRY_PROJECT}/contracts/...
                       -> ${JERRY_OUTPUT_BASE}contracts/...
      fallback_location:  REMOVED

  ~ skills/contract-design/agents/cd-validator.governance.yaml
      output.location:    projects/${JERRY_PROJECT}/contracts/...
                       -> ${JERRY_OUTPUT_BASE}contracts/...
      fallback_location:  REMOVED
```

EVIDENCE DIRECTORY (v1.2 addition -- raw terminal output, not tracked in file count)
  orchestration/output-basepath-20260318-001/evidence/
    test-results-baseline.txt    Gate 1: pre-implementation baseline
    fallback-location-audit.txt  Gate 2: grep audit before YAML removal
    test-results-cli.txt         Gate 3: CLI round-trip (AC-1, AC-2)
    test-results-unit.txt        Gate 4: unit tests GREEN
    test-results-e2e.txt         Gate 5: integration + AC-3 gap documented
    test-results-final.txt       Gate 6: final run + regression vs. baseline
```

**Total file count: 11** (5 Python/infra + 6 governance YAML; 6 evidence `.txt` files are not counted as implementation files but are required artifacts for READY_FOR_MERGE)

**Layer isolation check (H-07):**
- OutputBasePath (domain) must not import from infra or interface layers.
- OutputResolver (application) may import OutputBasePath (domain) and IConfigurationProvider (port). Must NOT import LayeredConfigAdapter directly.
- Bootstrap (composition root) wires OutputResolver with the concrete adapter.

### State Schema (ORCHESTRATION.yaml)

See the companion `ORCHESTRATION.yaml` file at:
`projects/PROJ-021-output-base-path/orchestration/output-basepath-20260318-001/ORCHESTRATION.yaml`

### Dynamic Path Configuration

All artifact paths use the workflow ID as the base dynamic identifier. No hardcoded pipeline names.

```
Base:          orchestration/{workflow_id}/
Pipeline A:    orchestration/{workflow_id}/{pipeline_alias}/{phase_id}/
Pipeline B:    orchestration/{workflow_id}/{pipeline_alias}/{phase_id}/
Barrier:       orchestration/{workflow_id}/cross-pollination/{barrier_id}/{direction}/

Resolved examples (workflow_id = output-basepath-20260318-001, alias et):
  orchestration/output-basepath-20260318-001/et/phase-et-1/
  orchestration/output-basepath-20260318-001/nse/phase-nse-2/
  orchestration/output-basepath-20260318-001/cross-pollination/barrier-1/et-to-nse/
```

All paths are relative to `projects/PROJ-021-output-base-path/`.

### Recovery Strategies

| Failure Mode | Detection | Recovery |
|-------------|-----------|---------|
| Phase quality gate fails at iteration 1-2 | adv score < 0.93 | Agent revises output; critic re-scores. Max 3 iterations. |
| Phase quality gate fails at iteration 3 | adv score < 0.93 after 3 iterations | Escalate to human per H-31. Persist partial artifact with BLOCKED status. |
| Barrier cross-pollination artifact missing | File not found at expected barrier path | Halt downstream phase. Alert user. Do not synthesize from memory. |
| Architecture decision (et-1) conflicts with requirements (nse-1) at BARRIER-1 | ADR and requirements have contradictory constraints | nse-requirements and eng-architect run a joint clarification cycle (one additional iteration each); human decides if unresolved. |
| BDD tests fail to reach GREEN phase | Test suite exits non-zero after implementation | eng-backend diagnoses and fixes; eng-qa re-runs coverage check. No phase gate until GREEN. |
| eng-security finds path traversal risk | STRIDE analysis identifies unmitigated S or T risk | et-2 reopened for eng-backend to add sanitization; security re-reviews. Counts as one additional phase iteration. |
| Coverage below 90% | `uv run pytest --cov` report shows < 90% | eng-qa and eng-backend collaborate to fill gaps. eng-reviewer re-checks before passing et-3. |
| Partial governance YAML edit (some agents updated, some not) | eng-security finds inconsistent `output.location` values across the 6 files | et-2 reopened; eng-backend completes the remaining edits; eng-security re-reviews consistency check. |
| Governance YAML schema validation fails after edit | `jerry agents validate` or schema check exits non-zero on any of the 6 files | eng-backend corrects the offending field value; eng-reviewer re-runs schema check before passing et-3. |
| `fallback_location` removal breaks a downstream agent | Agent at invocation time raises KeyError or similar on missing field | Verify schema: if `fallback_location` was required (not optional), it must be added to the schema as deprecated or eng-backend must patch the agent's resolution logic rather than removing the field. Escalate to eng-architect if schema change is needed. |
| Evidence Gate 1 fails (baseline tests fail) | `test-results-baseline.txt` shows failures | Stop. Document pre-existing failures. Decide: fix them now (preferred) or document them as known failures in the implementation summary and carry them through as tracked items. Do not proceed with new implementation on a red baseline. |
| Evidence Gate 2 fails (`fallback_location` audit finds Python reader) | `fallback-location-audit.txt` contains `.py` matches | Stop YAML edits. eng-architect must revise the plan: either the Python code must be updated to not read `fallback_location`, or the field must remain and the resolver must emit it. |
| Evidence Gate 3 fails (CLI command errors) | `test-results-cli.txt` contains non-zero exits | eng-backend diagnoses: is the config key registered? Is the scope resolution correct? Fix and re-run. |
| Evidence Gate 6 finds regressions | Test count in `test-results-final.txt` lower than `test-results-baseline.txt`, or test IDs missing | eng-backend diagnoses regression; fixes before et-3 quality gate passes. |
| AC-3 known gap escalates to full blocker | Stakeholder review determines partial satisfaction of AC-3 is not acceptable | File a follow-up GitHub Issue for the agent invocation framework. The current issue proceeds as planned; AC-3 is marked partial. Do not delay this PR to implement the invocation framework. |

### Execution Queue (Dependency Order)

```
1. [PARALLEL]  et-1 (eng-architect)    nse-1 (nse-requirements)
2. [SYNC]      BARRIER-1 quality gate
3. [PARALLEL]  et-2 (eng-backend, eng-qa)  nse-2 (nse-verification)
4. [SYNC]      BARRIER-2 quality gate
5. [PARALLEL]  et-3 (eng-security, eng-reviewer)  nse-3 (nse-reviewer)
6. [SYNC]      BARRIER-3 quality gate
7. [COMPLETE]  Workflow status -> READY_FOR_MERGE
```

Within et-2, eng-backend executes first (RED test phase, then GREEN), then eng-qa reviews the test strategy and runs coverage. These are sequential within the phase.

Within et-3, eng-security executes first, then eng-reviewer incorporates security findings into the final gate. Sequential within the phase.

### Criticality Assessment

| Factor | v1.0 | v1.1 | v1.2 | Level |
|--------|------|------|------|-------|
| Reversibility | 1 day | 1 day | 1 day | C2 |
| File scope | 5 files | 11 files | 11 files + 6 evidence files | C3 (>10 substantive files; see v1.2 rationale) |
| Impact | Application layer + bootstrap | + agent behavioral hint in governance YAML | + OSS contributor trust; AC-3 known gap documented; 6 execution gates | C3 |
| Auto-escalation check | None | None | None | No forced escalation |
| **Final criticality** | **C2** | **C2 retained** | **C3 (escalated)** | **C3** |

**v1.2 Criticality Rationale (escalated from C2 to C3):**

The v1.1 rationale for retaining C2 was: "6 of 11 files are mechanical single-field YAML replacements." That argument weakened in v1.2 for three reasons:

1. **OSS trust concern.** For a public repository, changes to agent behavioral specifications (`output.location`) are visible to contributors who read governance YAML files directly. An incorrect value erodes confidence. The degree of scrutiny applied to behavioral specification changes should reflect their visibility, not just their logical complexity.

2. **AC-3 known gap.** The v1.2 analysis revealed that AC-3 ("agent output.location fields resolve `${JERRY_OUTPUT_BASE}` at invocation time") is only partially satisfied. The gap — that the agent invocation framework does not yet read and interpolate governance YAML fields at runtime — was not visible in v1.1. A partially-satisfied acceptance criterion in a public issue warrants higher scrutiny than a fully-satisfied one.

3. **Evidence gate overhead.** Adding 6 execution gates is itself a scope-significant change to the verification process. C3 level work requires "all tiers" of enforcement (H-13 quality gate, S-014 scoring, S-004 pre-mortem, S-012 FMEA, S-013 inversion). This aligns with the additional rigor the evidence gates represent.

Decision: escalated to C3. The file-count argument (v1.1) is superseded.

**Required adversarial strategies for C3:** S-007 (Constitutional AI Critique), S-002 (Devil's Advocate), S-014 (LLM-as-Judge scoring), S-004 (Pre-Mortem Analysis), S-012 (FMEA), S-013 (Inversion Technique).
**Optional:** S-001 (Red Team Analysis), S-003 (Steelman), S-010 (Self-Refine), S-011 (Chain-of-Verification).
**Quality threshold:** >= 0.93 (above both the C2 minimum of 0.92 and the C3 enforcement floor).

---

## Evidence Artifact Registry

All evidence files are raw terminal output captured to `.txt` via `tee`. They are stored under:
`projects/PROJ-021-output-base-path/orchestration/output-basepath-20260318-001/evidence/`

Summary `.md` files in phase directories may reference evidence files but must not replace them. A reviewer must be able to inspect the raw output without reading any summary.

| # | Artifact | Phase | Gate? | Command (abbreviated) | Proves |
|---|----------|-------|-------|----------------------|--------|
| 1 | `evidence/test-results-baseline.txt` | Pre-et-2 | YES — all existing tests must pass before implementation begins | `uv run pytest tests/ --cov=src --cov-report=term-missing --tb=short` | Existing tests pass; regression comparison baseline |
| 2 | `evidence/fallback-location-audit.txt` | et-2 (before any YAML edits) | YES — no `.py` file may read `fallback_location` | `grep -r "fallback_location" src/ skills/ tests/ --include="*.py" --include="*.yaml"` | Safe to remove `fallback_location` from governance YAML |
| 3 | `evidence/test-results-cli.txt` | et-2 (after implementation, before quality gate) | YES — all CLI commands must exit 0 and round-trip correctly | `uv run jerry config set output.base_path work/ --scope root && uv run jerry config get output.base_path` | AC-1 (persistent storage) and AC-2 (retrieval) satisfied end-to-end |
| 4 | `evidence/test-results-unit.txt` | et-2 (after implementation) | YES — all unit tests must be GREEN | `uv run pytest tests/unit/ -v --tb=short` | OutputBasePath and OutputResolver unit tests pass |
| 5 | `evidence/test-results-e2e.txt` | et-2 (after governance YAML edits) | YES — integration test must pass; AC-3 gap must be documented | `uv run pytest tests/integration/test_bootstrap_output_resolver.py -v --tb=short` | AC-3 partially satisfied: resolver resolves correctly; runtime enforcement gap documented as follow-up |
| 6 | `evidence/test-results-final.txt` | et-3 (eng-reviewer final gate action) | YES — GREEN, coverage >= 90%, no regressions vs. gate 1 | `uv run pytest tests/ --cov=src --cov-report=term-missing --tb=short` | No regressions introduced; coverage maintained; all ACs testable through test suite |

**Gate failure behavior:** Any GATE-marked evidence file that fails its pass criterion is a hard blocker. The phase quality gate (`/adversary` score >= 0.93) cannot pass until all evidence gates for that phase are green. Evidence gates are not advisory.

**AC-3 Known Gap (documented per Gate 5):**
The governance YAML `output.location` field now contains `${JERRY_OUTPUT_BASE}`. The `OutputResolver.resolve()` method correctly returns the configured or fallback path. However, the mechanism by which a running agent reads `output.location` from its governance YAML and interpolates the `${JERRY_OUTPUT_BASE}` token at invocation time is not implemented by this issue. This mechanism — part of the agent invocation framework — is a follow-up item. AC-3 is considered partially satisfied: the data layer (resolver + YAML) is correct; the invocation layer enforcement is pending. This gap must appear explicitly in `evidence/test-results-e2e.txt` and in the implementation summary.

---

## Disclaimer

This orchestration plan was generated by the orch-planner agent (v2.2.0) for PROJ-021. The plan represents a proposed workflow only and has not been validated against runtime behavior. Human review is required before execution begins. Quality gate scores specified herein (>= 0.93) are targets, not guarantees; actual scores depend on the quality of agent outputs during execution.

All file paths in this document are relative to the Jerry repository root at `projects/PROJ-021-output-base-path/` unless otherwise noted.

Generated: 2026-03-18 | Revised: 2026-03-18 (v1.2) | Workflow: output-basepath-20260318-001 | Planner: orch-planner v2.2.0
