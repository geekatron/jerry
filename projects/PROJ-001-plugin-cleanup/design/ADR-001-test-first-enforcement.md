# ADR-001: Test-First Protocol Enforcement

**Status**: Proposed
**Date**: 2026-01-09
**Deciders**: Development Team
**Technical Story**: INIT-DEV-SKILL

---

## Context

The Jerry Framework development skill requires a mechanism to enforce test-driven development (TDD) discipline for all agent-generated code. This decision is critical because:

1. **AI-generated code quality risk**: Research document e-003 emphasizes that "AI tends toward 'looks right' code that compiles but may not work correctly." Tests provide the specification that constrains generation.

2. **Pattern consistency**: PAT-001-e003 (Test-First Agent Protocol) from the research synthesis (e-007) identifies test-first as a non-negotiable pattern for multi-agent development systems.

3. **Risk mitigation**: Risk R-002 in the gap analysis (e-010) identifies "Developers/agents bypass test-first protocol" as a Medium probability, High impact risk (score 6).

4. **Industry alignment**: The research cites Kent Beck's TDD, Google's testing practices, and NVIDIA's AI testing approaches as establishing test-first as industry standard, especially critical for AI-generated code.

### References

- dev-skill-e-007-synthesis.md: "Test-First is Non-Negotiable for AI-Generated Code" (Theme 1)
- dev-skill-e-008-architecture-analysis.md: PAT-001-e003 mapped to DevelopmentWorkflowService
- dev-skill-e-009-test-strategy.md: Test pyramid with BDD scenarios for test-first workflow
- dev-skill-e-010-risk-gap-analysis.md: R-002, DQ-001, A-008

---

## Decision Drivers

- **Code quality**: Tests constrain AI generation, reducing hallucination-driven bugs
- **Verifiability**: Red-Green-Refactor cycle provides observable evidence of correctness
- **Adoption resistance**: Assumption A-008 notes potential user resistance to strict enforcement
- **Operational overhead**: Hard constraints may slow development for exploratory work
- **Audit requirements**: Need traceable evidence that tests preceded code
- **Jerry Constitution compliance**: P-001 (Truth and Accuracy), P-008 (Evidence Artifacts)

---

## Considered Options

### Option A: Hard Constraint with No Override

**Description**: The DevelopmentWorkflowService enforces that `GenerateTestsCommand` must be successfully executed (with failing tests) before `GenerateCodeCommand` can proceed. No bypass mechanism exists.

**Implementation**:
```python
# src/development/application/services/development_workflow.py

class DevelopmentWorkflowService:
    async def generate_code(self, work_item: WorkItem) -> CodeGenerationResult:
        # HARD CONSTRAINT: Check test-first compliance
        if not work_item.has_tests:
            raise TestFirstViolationError(
                f"Work item {work_item.id} has no tests. "
                "Tests must be generated before code. "
                "Use generate_tests() first."
            )

        if not work_item.tests_failed_initially:
            raise RedPhaseViolationError(
                f"Work item {work_item.id} tests did not fail initially (Red phase). "
                "Generated tests must fail before implementing code."
            )

        # Proceed with code generation
        return await self._code_generation_port.generate_code(work_item)
```

**Pros**:
- Maximum enforcement of TDD discipline
- Clear audit trail (tests always precede code)
- Eliminates bypass risk entirely
- Simplest to implement and reason about

**Cons**:
- Blocks exploratory/spike work where tests may not be appropriate
- May frustrate users working on documentation or configuration
- No accommodation for edge cases (prototype, proof-of-concept)
- Potential productivity impact on experienced developers

### Option B: Soft Constraint with Warning

**Description**: The workflow logs warnings but allows code generation without tests. Warnings are captured in audit logs and surfaced in quality reports.

**Implementation**:
```python
# src/development/application/services/development_workflow.py

class DevelopmentWorkflowService:
    async def generate_code(self, work_item: WorkItem) -> CodeGenerationResult:
        # SOFT CONSTRAINT: Warn but allow
        if not work_item.has_tests:
            await self._event_publisher.publish(
                TestFirstWarning(
                    work_item_id=work_item.id,
                    message="Code generated without tests. TDD discipline not followed.",
                    timestamp=datetime.now(timezone.utc),
                )
            )
            self._logger.warning(
                f"SOFT_CONSTRAINT_VIOLATION: Work item {work_item.id} "
                "code generated without tests."
            )

        # Proceed with code generation regardless
        return await self._code_generation_port.generate_code(work_item)
```

**Pros**:
- Maximum flexibility for developers
- Accommodates all work types
- Captures audit data for reporting
- No productivity impact

**Cons**:
- Likely to result in widespread bypass (defeats purpose)
- Warnings often ignored over time ("warning fatigue")
- Does not address core quality concern
- Misaligned with research recommendations

### Option C: Quality Gate with Mandatory Coverage Check (Post-Generation)

**Description**: Code generation proceeds freely, but a mandatory quality gate checks test coverage before the work item can be marked as done. The gate blocks completion if coverage is below threshold.

**Implementation**:
```python
# src/development/application/services/quality_orchestration.py

class QualityOrchestrationService:
    async def execute_completion_gate(
        self, work_item: WorkItem
    ) -> QualityGateResult:
        results = []

        # Gate 1: Test existence
        test_exists_result = await self._check_tests_exist(work_item)
        results.append(test_exists_result)
        if not test_exists_result.passed:
            return QualityGateResult(
                passed=False,
                results=results,
                blocking_gate="test_existence",
                message="Tests required before completion."
            )

        # Gate 2: Coverage threshold (80% default)
        coverage_result = await self._check_coverage(
            work_item, threshold=0.80
        )
        results.append(coverage_result)
        if not coverage_result.passed:
            return QualityGateResult(
                passed=False,
                results=results,
                blocking_gate="coverage_threshold",
                message=f"Coverage {coverage_result.actual}% below threshold 80%."
            )

        return QualityGateResult(passed=True, results=results)
```

**Pros**:
- Allows flexible development workflow
- Enforces quality at critical milestone (completion)
- Coverage check validates test effectiveness
- Accommodates iterative development

**Cons**:
- Does not enforce Red phase (tests may pass trivially)
- Tests written after code may not drive design
- "Test-later" often results in lower-quality tests
- Misses the design benefits of TDD

### Option D: Combination Approach - Tiered Enforcement (RECOMMENDED)

**Description**: Enforcement level depends on work item classification:

| Work Item Type | Enforcement Level | Rationale |
|----------------|-------------------|-----------|
| Production code | Hard constraint | Core quality requirement |
| Bug fix | Hard constraint | Regression prevention |
| Spike/Prototype | Soft constraint (warning) | Exploratory work |
| Documentation | None | No code to test |
| Configuration | Quality gate only | Coverage check sufficient |

**Implementation**:
```python
# src/development/domain/value_objects/enforcement_level.py

from enum import Enum, auto

class EnforcementLevel(Enum):
    """Test-first enforcement levels."""
    HARD = auto()      # Block code generation without tests
    SOFT = auto()      # Warn but allow
    GATE_ONLY = auto() # Check at completion only
    NONE = auto()      # No enforcement

# src/development/domain/entities/work_item.py

@dataclass
class WorkItem:
    # ... existing fields ...
    work_type: WorkItemType

    @property
    def enforcement_level(self) -> EnforcementLevel:
        """Derive enforcement level from work type."""
        enforcement_map = {
            WorkItemType.FEATURE: EnforcementLevel.HARD,
            WorkItemType.BUG_FIX: EnforcementLevel.HARD,
            WorkItemType.REFACTOR: EnforcementLevel.HARD,
            WorkItemType.SPIKE: EnforcementLevel.SOFT,
            WorkItemType.PROTOTYPE: EnforcementLevel.SOFT,
            WorkItemType.DOCUMENTATION: EnforcementLevel.NONE,
            WorkItemType.CONFIGURATION: EnforcementLevel.GATE_ONLY,
            WorkItemType.CHORE: EnforcementLevel.GATE_ONLY,
        }
        return enforcement_map.get(self.work_type, EnforcementLevel.HARD)

# src/development/application/services/development_workflow.py

class DevelopmentWorkflowService:
    async def generate_code(self, work_item: WorkItem) -> CodeGenerationResult:
        enforcement = work_item.enforcement_level

        if enforcement == EnforcementLevel.HARD:
            # HARD: Block without tests
            if not work_item.has_tests:
                raise TestFirstViolationError(
                    f"Work item {work_item.id} requires tests before code. "
                    f"Work type '{work_item.work_type.name}' has HARD enforcement."
                )
            if not work_item.tests_failed_initially:
                raise RedPhaseViolationError(
                    f"Work item {work_item.id} tests must fail initially (Red phase)."
                )

        elif enforcement == EnforcementLevel.SOFT:
            # SOFT: Warn and log
            if not work_item.has_tests:
                await self._log_soft_violation(work_item)

        elif enforcement == EnforcementLevel.GATE_ONLY:
            # GATE_ONLY: No pre-check, coverage gate at completion
            pass

        # NONE: No enforcement at all

        # Proceed with code generation
        result = await self._code_generation_port.generate_code(work_item)

        # Always record test-first compliance status
        await self._record_compliance_audit(work_item, enforcement)

        return result

    async def _log_soft_violation(self, work_item: WorkItem) -> None:
        """Log soft constraint violation with audit trail."""
        await self._event_publisher.publish(
            TestFirstSoftViolation(
                work_item_id=work_item.id,
                work_type=work_item.work_type,
                timestamp=datetime.now(timezone.utc),
            )
        )
        self._logger.info(
            f"SOFT_VIOLATION: Work item {work_item.id} ({work_item.work_type.name}) "
            "proceeding without tests per soft enforcement policy."
        )

    async def _record_compliance_audit(
        self, work_item: WorkItem, enforcement: EnforcementLevel
    ) -> None:
        """Record compliance status for audit and reporting."""
        await self._audit_port.record(
            TestFirstComplianceRecord(
                work_item_id=work_item.id,
                enforcement_level=enforcement,
                had_tests=work_item.has_tests,
                tests_failed_initially=work_item.tests_failed_initially,
                timestamp=datetime.now(timezone.utc),
            )
        )
```

**Pros**:
- Balances discipline with flexibility
- Addresses adoption resistance (A-008) by accommodating exploratory work
- Maintains audit trail for all work types
- Aligns with tiered review approach (PAT-003-e004)
- Configurable per project needs

**Cons**:
- More complex implementation
- Requires clear work type classification
- Potential for "spike" abuse to bypass constraints
- Additional domain modeling required

---

## Decision Outcome

**Chosen Option**: **Option D - Combination Approach (Tiered Enforcement)**

### Justification

1. **Research alignment**: The e-007 synthesis explicitly notes that test-first is "non-negotiable for AI-generated code" - Option D preserves this for production code while acknowledging that not all work is production code.

2. **Risk mitigation**: Risk R-002 (bypass) is addressed by hard constraints on production code types, while Risk R-010 (bottlenecks) is addressed by allowing flexibility for exploratory work.

3. **Adoption strategy**: Assumption A-008 identifies potential adoption resistance. Option D reduces resistance by being pragmatic about work type differences.

4. **Evidence support**: Architecture analysis (e-008) recommends "Hard constraint for production code; soft for spikes/exploration" in the ADR-001 section.

5. **Audit requirements**: Jerry Constitution P-008 (Evidence Artifacts) is satisfied by comprehensive compliance recording.

6. **Progressive enforcement**: Aligns with the progressive quality gate strategy recommended in e-008 (ADR-004 recommendation).

### Consequences

#### Positive

- Production code quality protected by hard constraint
- Exploratory work unimpeded (enables innovation)
- Complete audit trail for compliance reporting
- Configurable by project (enforcement_map can be overridden)
- Clear documentation of expectations per work type
- Gradual user education through tiered approach

#### Negative

- Implementation complexity higher than simple hard/soft choice
- Work type classification must be accurate (potential for misclassification)
- Requires user understanding of work types
- "Spike" category could be abused to bypass constraints
- Additional domain entities (WorkItemType, EnforcementLevel)

#### Neutral

- Audit data enables future analysis of TDD adoption patterns
- May reveal organizational patterns around work type distribution
- Creates precedent for tiered enforcement in other areas

---

## Implementation

### Components Affected

From e-008 architecture analysis:

| Component | Layer | Change Description |
|-----------|-------|-------------------|
| `WorkItem` | Domain Entity | Add `work_type` field, `enforcement_level` property |
| `WorkItemType` | Value Object | New enum for work type classification |
| `EnforcementLevel` | Value Object | New enum for enforcement levels |
| `DevelopmentWorkflowService` | Application Service | Add tiered enforcement logic |
| `TestFirstViolationError` | Domain Exception | New exception for hard violations |
| `RedPhaseViolationError` | Domain Exception | New exception for red phase violations |
| `TestFirstSoftViolation` | Domain Event | New event for soft violations |
| `TestFirstComplianceRecord` | Value Object | Audit record structure |
| `IAuditPort` | Application Port | New port for compliance recording |

### Code Examples

**Domain Value Objects**:
```python
# src/development/domain/value_objects/work_item_type.py

from enum import Enum, auto

class WorkItemType(Enum):
    """Classification of work items for enforcement decisions."""
    FEATURE = auto()        # New functionality
    BUG_FIX = auto()        # Defect correction
    REFACTOR = auto()       # Code improvement without behavior change
    SPIKE = auto()          # Time-boxed exploration
    PROTOTYPE = auto()      # Proof of concept
    DOCUMENTATION = auto()  # Docs only, no code
    CONFIGURATION = auto()  # Config changes
    CHORE = auto()          # Maintenance tasks
```

**Domain Exception**:
```python
# src/development/domain/exceptions.py

class TestFirstViolationError(DomainError):
    """Raised when test-first protocol is violated with hard enforcement."""

    def __init__(self, work_item_id: str, work_type: str, message: str):
        self.work_item_id = work_item_id
        self.work_type = work_type
        super().__init__(message)

class RedPhaseViolationError(DomainError):
    """Raised when tests do not fail initially (Red phase missing)."""

    def __init__(self, work_item_id: str, message: str):
        self.work_item_id = work_item_id
        super().__init__(message)
```

**BDD Test Scenario** (from e-009):
```gherkin
# tests/system/features/test_first_development.feature

@workflow @test-first @enforcement
Feature: Tiered Test-First Enforcement
    As a developer using Jerry
    I want appropriate test-first enforcement based on work type
    So that I can balance quality discipline with productivity

    @hard-enforcement
    Scenario: Feature work requires tests before code
        Given I have a work item of type "FEATURE"
        And the work item has no tests
        When I attempt to generate code for the work item
        Then the operation should be rejected
        And the error should be "TestFirstViolationError"
        And the error message should mention "HARD enforcement"

    @hard-enforcement @red-phase
    Scenario: Bug fix requires failing tests (Red phase)
        Given I have a work item of type "BUG_FIX"
        And the work item has tests that pass
        When I attempt to generate code for the work item
        Then the operation should be rejected
        And the error should be "RedPhaseViolationError"

    @soft-enforcement
    Scenario: Spike allows code without tests with warning
        Given I have a work item of type "SPIKE"
        And the work item has no tests
        When I attempt to generate code for the work item
        Then code should be generated
        And a soft violation warning should be logged
        And a compliance record should be created

    @no-enforcement
    Scenario: Documentation has no test-first requirement
        Given I have a work item of type "DOCUMENTATION"
        When I check the enforcement level
        Then the enforcement level should be "NONE"
```

### Migration Path

**Phase 1 (Week 1-2)**: Domain foundation
1. Add `WorkItemType` enum to domain layer
2. Add `EnforcementLevel` enum to domain layer
3. Update `WorkItem` entity with `work_type` field
4. Implement `enforcement_level` derived property
5. Add domain exceptions

**Phase 2 (Week 3)**: Application layer
1. Create `IAuditPort` interface
2. Update `DevelopmentWorkflowService` with tiered enforcement
3. Add compliance recording to workflow
4. Implement `TestFirstSoftViolation` event

**Phase 3 (Week 4)**: Infrastructure and testing
1. Implement `FileSystemAuditAdapter`
2. Add BDD scenarios for all enforcement levels
3. Add property-based tests for state transitions
4. Integration tests for audit recording

**Phase 4 (Week 5)**: CLI and documentation
1. Update CLI to require work type on task creation
2. Add `--work-type` flag with validation
3. Document enforcement policy in SKILL.md
4. Create user guide for work type selection

---

## Validation

### Test Scenarios

| Scenario | Input | Expected Behavior |
|----------|-------|-------------------|
| Feature without tests | WorkItemType.FEATURE, no tests | `TestFirstViolationError` raised |
| Feature with passing tests | WorkItemType.FEATURE, tests pass | `RedPhaseViolationError` raised |
| Feature with failing tests | WorkItemType.FEATURE, tests fail | Code generation proceeds |
| Bug fix without tests | WorkItemType.BUG_FIX, no tests | `TestFirstViolationError` raised |
| Spike without tests | WorkItemType.SPIKE, no tests | Code generated, warning logged |
| Documentation without tests | WorkItemType.DOCUMENTATION | Code generated, no warning |
| Configuration without tests | WorkItemType.CONFIGURATION | Code generated, gate check at completion |

### Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Hard enforcement compliance rate | 100% | Audit records for HARD types |
| Red phase compliance | >95% | Tests failing initially for HARD types |
| Soft violation rate | <20% | Soft violations / total SOFT type items |
| Work type accuracy | >90% | Manual sampling of classified items |
| Test coverage for gated items | >80% | Coverage reports at completion gate |
| User adoption satisfaction | >4/5 | User survey post-pilot |

### Acceptance Criteria

1. **AC-001**: When a work item of type FEATURE, BUG_FIX, or REFACTOR attempts code generation without tests, a `TestFirstViolationError` is raised with descriptive message.

2. **AC-002**: When a work item has tests that pass initially, a `RedPhaseViolationError` is raised indicating Red phase violation.

3. **AC-003**: When a work item of type SPIKE or PROTOTYPE generates code without tests, the operation succeeds and a `TestFirstSoftViolation` event is published.

4. **AC-004**: Every code generation attempt creates a `TestFirstComplianceRecord` in the audit store.

5. **AC-005**: The enforcement level is correctly derived from work item type according to the enforcement_map.

6. **AC-006**: CLI rejects task creation without specifying work type.

---

## Related Decisions

- **ADR-006**: File Locking Strategy - Impacts audit record persistence
- **ADR-008**: Quality Gate Layer Configuration - Completion gate check for GATE_ONLY enforcement
- **ADR-009**: Event Storage Mechanism - Required for TestFirstSoftViolation event persistence

---

## References

### Research Documents
- dev-skill-e-007-synthesis.md - Pattern catalog and cross-cutting themes
- dev-skill-e-008-architecture-analysis.md - Component mapping and ADR recommendations
- dev-skill-e-009-test-strategy.md - BDD scenarios and test pyramid
- dev-skill-e-010-risk-gap-analysis.md - Risk R-002, Assumption A-008, DQ-001

### External Sources
- Beck, Kent. *Test-Driven Development: By Example*. Addison-Wesley, 2002.
- Fowler, Martin. "Test Driven Development." https://martinfowler.com/bliki/TestDrivenDevelopment.html
- Martin, Robert C. "The Cycles of TDD." https://blog.cleancoder.com/uncle-bob/2014/12/17/TheCyclesOfTDD.html
- NVIDIA. "Building AI Agents to Automate Software Test Case Creation." https://developer.nvidia.com/blog/building-ai-agents-to-automate-software-test-case-creation/
- DZone. "Test-Driven Generation: Adopting TDD With GenAI." https://dzone.com/articles/test-driven-generation
- Google Engineering Practices. "The Standard of Code Review." https://google.github.io/eng-practices/review/reviewer/standard.html

### Jerry Framework
- Jerry Constitution v1.0 - P-001 (Truth and Accuracy), P-008 (Evidence Artifacts)
- Coding Standards (.claude/rules/coding-standards.md)

---

*ADR-001 created: 2026-01-09*
*Author: ps-architect*
*Status: Proposed*
