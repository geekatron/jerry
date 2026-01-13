# ADR-008: Quality Gate Layer Configuration

**Status**: Proposed
**Date**: 2026-01-09
**Deciders**: Development Team
**Author**: ps-architect agent (v2.0.0)
**Technical Story**: INIT-DEV-SKILL

---

## Context

### Problem Statement

The Jerry Framework development skill requires a quality gate architecture that enforces code quality standards across multiple stages of the development lifecycle. The challenge is determining:

1. **Which quality gates are mandatory vs. optional** - Not all changes require the same rigor
2. **Ordering and cascade behavior** - How gates should sequence and when to stop
3. **Fail-fast vs. collect-all-failures** - Whether to abort on first failure or gather all issues
4. **Risk-adaptive configuration** - How gate rigor should scale with change risk

### Background Research

Research from `dev-skill-e-002-quality-gates.md` identifies six key patterns for quality gate architecture:

| Pattern | ID | Key Insight |
|---------|-----|-------------|
| Layered Gate Architecture | PAT-001-e002 | Multiple gates at different stages catch different problems |
| Shift-Left Quality Gates | PAT-002-e002 | Earlier detection = lower cost of fix |
| SLO-Based Quality Gates | PAT-003-e002 | Production metrics as deployment criteria |
| Definition of Done as Gate | PAT-004-e002 | Team standards codified as automated checks |
| Agent Guardrail Architecture | PAT-005-e002 | Separate planning from execution for safety |
| Auto-Deploy with Rollback | PAT-006-e002 | Automation more reliable than human monitoring |

Additionally, `dev-skill-e-004` (tiered review) and `dev-skill-e-007-synthesis.md` establish risk-based rigor tiers that inform gate configuration.

---

## Decision Drivers

### From Industry Research (e-002)

1. **Google SRE Release Engineering**: Continuous testing, release branch, SLO-based, and canary gates
2. **Azure DevOps**: Four validation categories (Quality, Security, Change Management, Infrastructure)
3. **GitHub Actions**: Required checks pattern with branch protection
4. **SonarQube 2025**: 80% coverage on new code, maintainability ratings A+
5. **Stripe's Auto-Deploy**: 16.4 deploys/day with automatic rollback on failures
6. **AEGIS Framework (Forrester 2025)**: Six-domain agentic AI guardrails

### From Cross-Cutting Synthesis (e-007)

1. **Theme 2**: Layered Quality Gates with Appropriate Rigor - Risk-matched enforcement
2. **Theme 6**: Human Oversight at Strategic Points - Gate destructive actions
3. **Constraint c-008**: Evidence Artifacts - Automated validation must produce verifiable evidence

### From Architecture Analysis (e-008)

1. **ADR-004 Recommendation**: Progressive approach starting with local + PR gates
2. **QualityOrchestrationService**: Application layer component for gate cascade
3. **QualityGateEvaluator**: Domain service for condition evaluation

### From Test Strategy (e-009)

1. **Coverage Thresholds**: Domain >90%, Application >80%, Infrastructure >70%
2. **Mutation Testing**: Domain >80% mutation score for test quality verification
3. **BDD Scenarios**: `quality_gate_cascade.feature` defines expected behavior

---

## Considered Options

### Option 1: Linear Gate Cascade (L0 -> L1 -> L2)

**Description**: Gates execute sequentially in strict order. Each gate must pass before the next begins. Failure at any point halts the cascade.

```
L0 (Syntax) --> L1 (Semantic) --> L2 (Review)
    |               |               |
  FAIL?           FAIL?           FAIL?
    |               |               |
    v               v               v
  STOP            STOP            STOP
```

**Pros**:
- Simple mental model
- Fast fail (stops at first issue)
- Resource efficient (no wasted work after failure)

**Cons**:
- Multiple run cycles to find all issues
- Frustrating DX when many issues exist
- Cannot parallelize independent checks

### Option 2: Parallel Gate Execution

**Description**: All gates execute simultaneously. Results aggregated at the end.

```
     +-- L0 (Syntax) ----+
     |                   |
  -->+-- L1 (Semantic) --+--> Aggregate Results
     |                   |
     +-- L2 (Review) ----+
```

**Pros**:
- All issues surfaced in single run
- Maximum parallelization
- Better for CI environments

**Cons**:
- Wastes resources on deeper checks when shallow fails
- No logical dependency handling
- May produce confusing output (L2 comments on syntax errors)

### Option 3: Risk-Based Gate Selection

**Description**: Risk assessment determines which gates apply. Low-risk changes get minimal gates; high-risk changes get full cascade.

```
Risk Assessment --> T1: [L0]
                --> T2: [L0, L1]
                --> T3: [L0, L1, L2-agent]
                --> T4: [L0, L1, L2-agent, L2-human]
```

**Pros**:
- Right-sized effort for change type
- Fast path for low-risk changes
- Appropriate human oversight for high-risk

**Cons**:
- Risk classification can be wrong
- Complex configuration
- May miss issues in "low-risk" changes

### Option 4: Configurable Gate Profiles (Recommended)

**Description**: Hybrid approach combining linear cascade within tiers with risk-based tier selection. Gates within each level are parallelizable; levels cascade sequentially.

```
Risk Tier --> Select Profile --> Execute Cascade

Profile L0 (Syntax & Basic):
  +-- format-check ----+
  |                    |
  +-- lint-basic ------+--> L0 Result
  |                    |
  +-- secret-scan -----+

Profile L1 (Semantic & Quality):
  +-- coverage-check --+
  |                    |
  +-- type-check ------+--> L1 Result
  |                    |
  +-- test-run --------+

Profile L2 (Distinguished Review):
  +-- adr-compliance --+
  |                    |
  +-- agent-review ----+--> L2 Result
  |                    |
  +-- security-review -+
```

**Pros**:
- Parallelization within levels
- Fail-fast between levels
- Risk-adaptive profile selection
- Configurable per project/context
- Clear evidence artifacts per level

**Cons**:
- More complex configuration
- Requires profile management

---

## Decision Outcome

**Chosen Option**: Option 4 - Configurable Gate Profiles

### Rationale

1. **Balances thoroughness with speed**: Parallel within levels, sequential between levels
2. **Supports progressive adoption**: Start with L0+L1, add L2 for critical paths
3. **Aligns with research patterns**:
   - PAT-001-e002 (Layered Gate Architecture)
   - PAT-003-e004 (Tiered Review Rigor)
4. **Satisfies Jerry constraints**:
   - c-008 (Evidence Artifacts) - Each level produces evidence
   - c-007 (Finite Operations) - Bounded by timeout per level
5. **Enables risk-adaptive behavior**: Different profiles for different risk tiers

---

## Implementation

### Gate Definition Schema

```yaml
# .jerry/gates/quality-gates.yaml

version: "1.0"
schema: "jerry:jer::dev-skill:schema/QualityGateConfig+1.0.0"

profiles:
  default:
    description: "Standard development workflow"
    risk_tiers: [T1, T2]
    levels: [L0, L1]

  strict:
    description: "Critical path changes (API, security, core)"
    risk_tiers: [T3, T4]
    levels: [L0, L1, L2]

  quick:
    description: "Documentation and config changes only"
    risk_tiers: []
    levels: [L0]
    file_patterns:
      - "*.md"
      - "*.yaml"
      - "*.json"

gates:
  L0:
    name: "Syntax & Basic Validation"
    mandatory: true
    fail_fast: true
    timeout_seconds: 60
    parallel: true
    checks:
      - id: format-check
        name: "Code Formatting"
        command: "ruff format --check ."
        fix_command: "ruff format ."
        auto_fix: true

      - id: lint-basic
        name: "Basic Linting"
        command: "ruff check . --select=E,F"
        threshold: 0  # Zero errors allowed

      - id: secret-scan
        name: "Secrets Detection"
        command: "detect-secrets scan --baseline .secrets.baseline"
        critical: true  # Always blocks on failure

      - id: merge-conflict
        name: "Merge Conflict Markers"
        command: "git diff --check HEAD"
        critical: true

  L1:
    name: "Semantic & Quality Validation"
    mandatory: true
    fail_fast: false  # Collect all issues
    timeout_seconds: 300
    parallel: true
    depends_on: [L0]
    checks:
      - id: type-check
        name: "Type Checking"
        command: "mypy src/ --strict"
        threshold: 0

      - id: test-run
        name: "Test Suite Execution"
        command: "pytest tests/ -v --tb=short"
        coverage:
          enabled: true
          command: "pytest tests/ --cov=src --cov-report=xml"
          thresholds:
            domain: 90
            application: 80
            infrastructure: 70
            overall: 80

      - id: lint-full
        name: "Full Linting"
        command: "ruff check . --select=ALL"
        threshold: 10  # Allow up to 10 warnings

      - id: complexity-check
        name: "Cyclomatic Complexity"
        command: "radon cc src/ -a -nc"
        threshold:
          max_complexity: 10
          average_complexity: 5

      - id: docstring-check
        name: "Docstring Coverage"
        command: "interrogate src/ -v"
        threshold: 80  # 80% docstring coverage

  L2:
    name: "Distinguished Review"
    mandatory: false  # Triggered by risk tier
    fail_fast: false
    timeout_seconds: 600
    parallel: false  # Sequential for context
    depends_on: [L0, L1]
    trigger:
      risk_tiers: [T3, T4]
      file_patterns:
        - "src/**/domain/**"
        - "src/**/ports/**"
        - "**/security/**"
        - "**/*_api*"
    checks:
      - id: adr-compliance
        name: "ADR Compliance Check"
        type: agent_review
        prompt: |
          Review the following changes against existing Architecture Decision Records.
          Flag any violations of documented architectural decisions.
          Reference relevant ADR IDs in comments.
        evidence_required: true

      - id: agent-review
        name: "Agent Code Review"
        type: agent_review
        prompt: |
          Review the code changes for:
          1. Security vulnerabilities
          2. Performance implications
          3. Maintainability concerns
          4. Test coverage gaps
          Follow the Health-Over-Perfection principle (PAT-001-e004).
        evidence_required: true

      - id: human-approval
        name: "Human Approval Gate"
        type: human_gate
        trigger:
          risk_tier: T4
          change_categories: [security, api_breaking, data_migration]
        timeout_seconds: 86400  # 24 hours
        escalation:
          after_seconds: 3600
          notify: ["team-lead"]

risk_classification:
  T1:  # Low Risk
    description: "Documentation, config, non-functional changes"
    file_patterns:
      - "*.md"
      - "docs/**"
      - "*.yaml"
      - "*.json"
      - "tests/**"
    max_files: 20

  T2:  # Medium Risk
    description: "Feature changes, bug fixes, refactoring"
    file_patterns:
      - "src/**"
    excludes:
      - "src/**/domain/**"
      - "src/**/ports/**"
    max_files: 50

  T3:  # High Risk
    description: "Domain logic, ports, API changes"
    file_patterns:
      - "src/**/domain/**"
      - "src/**/ports/**"
      - "**/*_api*"
    any_match: true

  T4:  # Critical Risk
    description: "Security, data migration, breaking changes"
    file_patterns:
      - "**/security/**"
      - "**/migration/**"
      - "**/auth/**"
    keywords:
      - "BREAKING"
      - "SECURITY"
      - "MIGRATION"
    any_match: true
    requires_human_approval: true

thresholds:
  coverage:
    new_code: 80          # SonarQube default
    domain_layer: 90      # From e-009
    application_layer: 80
    infrastructure_layer: 70
    critical_paths: 95

  mutation:
    domain_layer: 85
    value_objects: 90
    critical_paths: 80

  complexity:
    cyclomatic_max: 10
    cognitive_max: 15
    method_length_max: 50

  duplication:
    max_duplicated_lines: 3%  # SonarQube default
```

### Gate Execution Flow

```
                              ┌─────────────────────────────────────────────────────────┐
                              │                  QUALITY GATE CASCADE                     │
                              └─────────────────────────────────────────────────────────┘

                                             ┌──────────────┐
                                             │ Change Input │
                                             └──────┬───────┘
                                                    │
                                                    v
                              ┌─────────────────────────────────────────────────────────┐
                              │              RISK ASSESSMENT SERVICE                      │
                              │  ┌──────────────────────────────────────────────────┐   │
                              │  │ Analyze: file patterns, keywords, change scope   │   │
                              │  │ Output: Risk Tier (T1/T2/T3/T4)                  │   │
                              │  └──────────────────────────────────────────────────┘   │
                              └───────────────────────┬─────────────────────────────────┘
                                                      │
                                                      v
                              ┌─────────────────────────────────────────────────────────┐
                              │              PROFILE SELECTOR                            │
                              │  ┌──────────────────────────────────────────────────┐   │
                              │  │ T1/T2 → default profile → [L0, L1]               │   │
                              │  │ T3/T4 → strict profile  → [L0, L1, L2]           │   │
                              │  └──────────────────────────────────────────────────┘   │
                              └───────────────────────┬─────────────────────────────────┘
                                                      │
                        ┌─────────────────────────────┼─────────────────────────────┐
                        │                             │                             │
                        v                             v                             v
          ┌─────────────────────────┐   ┌─────────────────────────┐   ┌─────────────────────────┐
          │         L0 GATE          │   │         L1 GATE          │   │         L2 GATE          │
          │   (Syntax & Basic)       │   │   (Semantic & Quality)   │   │  (Distinguished Review)  │
          ├─────────────────────────┤   ├─────────────────────────┤   ├─────────────────────────┤
          │  PARALLEL EXECUTION:    │   │  PARALLEL EXECUTION:    │   │  SEQUENTIAL EXECUTION:  │
          │                         │   │                         │   │                         │
          │  ┌─────────────────┐    │   │  ┌─────────────────┐    │   │  ┌─────────────────┐    │
          │  │ format-check    │    │   │  │ type-check      │    │   │  │ adr-compliance  │    │
          │  └─────────────────┘    │   │  └─────────────────┘    │   │  └────────┬────────┘    │
          │  ┌─────────────────┐    │   │  ┌─────────────────┐    │   │           │             │
          │  │ lint-basic      │    │   │  │ test-run        │    │   │  ┌────────v────────┐    │
          │  └─────────────────┘    │   │  └─────────────────┘    │   │  │ agent-review    │    │
          │  ┌─────────────────┐    │   │  ┌─────────────────┐    │   │  └────────┬────────┘    │
          │  │ secret-scan     │    │   │  │ coverage-check  │    │   │           │             │
          │  └─────────────────┘    │   │  └─────────────────┘    │   │  ┌────────v────────┐    │
          │  ┌─────────────────┐    │   │  ┌─────────────────┐    │   │  │ human-approval  │    │
          │  │ merge-conflict  │    │   │  │ complexity-check│    │   │  │ (T4 only)       │    │
          │  └─────────────────┘    │   │  └─────────────────┘    │   │  └─────────────────┘    │
          ├─────────────────────────┤   ├─────────────────────────┤   ├─────────────────────────┤
          │ fail_fast: true         │   │ fail_fast: false        │   │ fail_fast: false        │
          │ timeout: 60s            │   │ timeout: 300s           │   │ timeout: 600s           │
          │ mandatory: true         │   │ mandatory: true         │   │ mandatory: false        │
          └───────────┬─────────────┘   └───────────┬─────────────┘   └───────────┬─────────────┘
                      │                             │                             │
                      v                             v                             v
          ┌─────────────────────────┐   ┌─────────────────────────┐   ┌─────────────────────────┐
          │     L0 RESULT           │   │     L1 RESULT           │   │     L2 RESULT           │
          │ ─────────────────────── │   │ ─────────────────────── │   │ ─────────────────────── │
          │ PASS → continue to L1   │   │ PASS → continue to L2   │   │ PASS → GATE PASSED      │
          │ FAIL → STOP CASCADE     │   │ FAIL → STOP CASCADE     │   │ FAIL → STOP CASCADE     │
          │ (collect all L0 issues) │   │ (all issues collected)  │   │ (review comments)       │
          └───────────┬─────────────┘   └───────────┬─────────────┘   └───────────┬─────────────┘
                      │                             │                             │
                      │              DEPENDS ON     │              DEPENDS ON     │
                      └─────────────────────────────┴─────────────────────────────┘
                                                    │
                                                    v
                              ┌─────────────────────────────────────────────────────────┐
                              │                  GATE CASCADE RESULT                     │
                              │  ┌──────────────────────────────────────────────────┐   │
                              │  │ overall: PASSED | FAILED                         │   │
                              │  │ failed_at: L0 | L1 | L2 | null                   │   │
                              │  │ evidence: [artifact paths...]                    │   │
                              │  │ duration_ms: total execution time                │   │
                              │  └──────────────────────────────────────────────────┘   │
                              └─────────────────────────────────────────────────────────┘
```

### Threshold Configuration

| Metric | Layer | Threshold | Source | Enforcement |
|--------|-------|-----------|--------|-------------|
| Coverage (new code) | All | >= 80% | SonarQube default, e-002 | L1 gate |
| Coverage (domain) | Domain | >= 90% | e-009 | L1 gate |
| Coverage (application) | Application | >= 80% | e-009 | L1 gate |
| Coverage (infrastructure) | Infrastructure | >= 70% | e-009 | L1 gate |
| Mutation Score (domain) | Domain | >= 85% | e-009 | PR gate (soft) |
| Cyclomatic Complexity | All | <= 10 | Industry standard | L1 gate |
| Duplicated Lines | All | <= 3% | SonarQube default | L1 gate |
| Security Vulnerabilities | All | 0 critical | AEGIS framework | L0/L1 gate |
| Type Errors | All | 0 | Clean code | L1 gate |

### Evidence Artifact Format

Each gate execution produces an evidence artifact (constraint c-008):

```json
{
  "schema": "jerry:jer::dev-skill:schema/GateEvidence+1.0.0",
  "gate_id": "L1",
  "gate_name": "Semantic & Quality Validation",
  "execution_id": "exec-20260109-143052-abc123",
  "timestamp": "2026-01-09T14:30:52Z",
  "duration_ms": 45230,
  "result": "PASSED",
  "checks": [
    {
      "id": "type-check",
      "name": "Type Checking",
      "result": "PASSED",
      "duration_ms": 12340,
      "output_summary": "Success: no issues found in 142 source files",
      "artifact_path": ".jerry/evidence/type-check-20260109-143052.log"
    },
    {
      "id": "test-run",
      "name": "Test Suite Execution",
      "result": "PASSED",
      "duration_ms": 28450,
      "metrics": {
        "tests_passed": 247,
        "tests_failed": 0,
        "tests_skipped": 3,
        "coverage_overall": 84.2,
        "coverage_domain": 92.1,
        "coverage_application": 81.5,
        "coverage_infrastructure": 74.3
      },
      "artifact_path": ".jerry/evidence/test-run-20260109-143052.xml"
    }
  ],
  "risk_tier": "T2",
  "profile": "default"
}
```

### Integration Points

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT SKILL ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────┐     ┌──────────────────────┐             │
│  │   CLI / Skill        │     │   Pre-Commit Hook    │             │
│  │   `dev gate run`     │     │   `.pre-commit`      │             │
│  └──────────┬───────────┘     └──────────┬───────────┘             │
│             │                            │                          │
│             └────────────┬───────────────┘                          │
│                          │                                          │
│                          v                                          │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │            QualityOrchestrationService                       │   │
│  │  (Application Layer - src/development/application/services/) │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │  - load_profile(risk_tier)                                   │   │
│  │  - execute_cascade(profile, context)                         │   │
│  │  - aggregate_results(level_results)                          │   │
│  │  - emit_events(GatePassed | GateFailed)                      │   │
│  └──────────────────────────┬──────────────────────────────────┘   │
│                             │                                       │
│          ┌──────────────────┼──────────────────┐                   │
│          │                  │                  │                    │
│          v                  v                  v                    │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐          │
│  │ RiskAssessment│  │ QualityGate   │  │ Evidence      │          │
│  │ Service       │  │ Evaluator     │  │ Publisher     │          │
│  │ (Domain)      │  │ (Domain)      │  │ (Infra)       │          │
│  └───────────────┘  └───────────────┘  └───────────────┘          │
│                             │                                       │
│          ┌──────────────────┼──────────────────┐                   │
│          │                  │                  │                    │
│          v                  v                  v                    │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐          │
│  │ PreCommit     │  │ Ruff          │  │ Pytest        │          │
│  │ Adapter       │  │ Adapter       │  │ Adapter       │          │
│  │ (IQualityGate)│  │ (IQualityGate)│  │ (ITestRunner) │          │
│  └───────────────┘  └───────────────┘  └───────────────┘          │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Validation

### BDD Acceptance Criteria

The following scenarios from `dev-skill-e-009-test-strategy.md` validate this decision:

```gherkin
@workflow @quality-gates
Feature: Quality Gate Cascade

  Scenario: Full quality gate cascade succeeds
    Given I have code changes ready for validation
    And the changes are classified as T2 risk
    When I execute the quality gate cascade
    Then the L0 pre-commit checks should pass
    And the L1 semantic checks should pass
    And the overall gate result should be "PASSED"
    And evidence artifacts should be generated for each level

  Scenario: Cascade stops on L0 failure
    Given I have code changes with formatting issues
    When I execute the quality gate cascade
    Then the L0 format-check should fail
    And the L1 checks should not be executed
    And the overall gate result should be "FAILED"
    And the failure details should include fix suggestions

  Scenario: L2 triggered for high-risk changes
    Given I have code changes to "src/domain/entities/"
    When I perform risk assessment
    Then the risk tier should be "T3"
    And the L2 distinguished review should be triggered

  Scenario: Human approval required for T4 risk
    Given I have code changes classified as T4 risk
    When I execute the quality gate cascade
    And L0 and L1 pass
    Then a human approval request should be created
    And the gate should remain pending until approval
```

### Pattern Compliance Matrix

| Pattern ID | Pattern Name | Compliance | Implementation |
|------------|--------------|------------|----------------|
| PAT-001-e002 | Layered Gate Architecture | COMPLIANT | L0/L1/L2 cascade with dependencies |
| PAT-002-e002 | Shift-Left Quality Gates | COMPLIANT | L0 catches issues at commit time |
| PAT-003-e002 | SLO-Based Quality Gates | PARTIAL | Coverage thresholds; SLO integration future |
| PAT-004-e002 | Definition of Done as Gate | COMPLIANT | Checklist items in gate configuration |
| PAT-005-e002 | Agent Guardrail Architecture | COMPLIANT | L2 separates planning from execution |
| PAT-006-e002 | Auto-Deploy with Rollback | FUTURE | Not yet implemented |
| PAT-003-e004 | Tiered Review Rigor | COMPLIANT | T1-T4 risk classification |
| PAT-001-e004 | Health-Over-Perfection | COMPLIANT | Agent review prompt guidance |

### Constraint Compliance

| Constraint | ID | Compliance | Evidence |
|------------|-----|------------|----------|
| Evidence Artifacts | c-008 | COMPLIANT | Evidence JSON per gate execution |
| Finite Operations | c-007 | COMPLIANT | Timeout per level (60s, 300s, 600s) |
| Task Tracking | c-010 | COMPLIANT | Gates produce domain events |
| User Authority | c-020 | COMPLIANT | Human gate for T4 risk |

---

## Consequences

### Positive

1. **Layered enforcement** catches different issue types at appropriate stages
2. **Parallel execution** within levels maximizes CI efficiency
3. **Risk-adaptive profiles** balance rigor with velocity
4. **Evidence artifacts** provide audit trail and debugging information
5. **Progressive adoption** path from minimal to full enforcement
6. **Agent-ready** architecture supports AI-assisted review at L2

### Negative

1. **Configuration complexity** requires upfront setup
2. **Profile management** adds maintenance burden
3. **Risk classification** can produce false positives/negatives
4. **Tool dependencies** (ruff, mypy, pytest) must be installed

### Mitigations

1. Provide sensible defaults in `.jerry/gates/quality-gates.yaml`
2. CLI command `dev gate init` generates starter configuration
3. Risk classification can be manually overridden via `--risk-tier` flag
4. Document tool installation in project setup guide

---

## References

### Primary Research Documents

1. `dev-skill-e-002-quality-gates.md` - Quality gate patterns (PAT-001 through PAT-006)
2. `dev-skill-e-007-synthesis.md` - Cross-cutting themes and constraint mapping
3. `dev-skill-e-008-architecture-analysis.md` - Component architecture and ADR-004
4. `dev-skill-e-009-test-strategy.md` - Coverage thresholds and BDD scenarios

### Industry Sources (from e-002)

- [Google SRE Book - Release Engineering](https://sre.google/sre-book/release-engineering/)
- [Azure Pipelines Deployment Gates](https://learn.microsoft.com/en-us/azure/devops/pipelines/release/approvals/gates)
- [GitHub Actions Required Checks](https://graphite.com/guides/enforce-code-quality-gates-github-actions)
- [SonarQube Quality Gates](https://docs.sonarsource.com/sonarqube-server/2025.1/instance-administration/analysis-functions/quality-gates)
- [Stripe's Engineering Culture](https://newsletter.pragmaticengineer.com/p/stripe-part-2)
- [AEGIS Framework](https://bigid.com/blog/what-is-aegis/)

### Related ADRs

- ADR-003: Code Directory Structure - Bounded context organization
- ADR-004: Session Management Alignment - EntityBase patterns

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-09 | ps-architect | Initial proposal |

---

*Document generated by ps-architect agent (v2.0.0) on 2026-01-09*
*Source documents: e-002, e-007, e-008, e-009*
*Patterns referenced: PAT-001-e002 through PAT-006-e002, PAT-003-e004, PAT-001-e004*
