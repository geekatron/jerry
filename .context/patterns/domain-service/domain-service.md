# PAT-SVC-001: Domain Service Pattern

> **Status**: RECOMMENDED
> **Category**: Domain Service Pattern
> **Location**: `src/*/domain/services/`

---

## Overview

Domain Services encapsulate domain logic that doesn't naturally fit within a single entity or value object. They coordinate operations across multiple aggregates or implement complex business rules that span entity boundaries.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Eric Evans** | "A Service is an operation offered as an interface that stands alone in the model" |
| **Vaughn Vernon** | "Domain Services are stateless and express domain concepts" |
| **Martin Fowler** | "Service Layer defines application's boundary with a layer of services" |

---

## When to Use Domain Services

Use a Domain Service when:
1. Operation doesn't belong to any single entity
2. Logic spans multiple aggregates
3. Behavior needs external information to complete
4. Complex calculations or validations are needed

---

## Jerry Implementation

### Quality Validator Service

```python
# File: src/work_tracking/domain/services/quality_validator.py
from __future__ import annotations

from typing import TYPE_CHECKING

from src.shared_kernel.exceptions import QualityGateError
from src.work_tracking.domain.value_objects.quality_metrics import QualityMetrics

if TYPE_CHECKING:
    from src.work_tracking.domain.aggregates.work_item import WorkItem


class QualityValidator:
    """Domain service for validating quality gates.

    Encapsulates quality gate logic that:
    - Spans work item and its metrics
    - Has configurable thresholds
    - Provides detailed failure reasons

    Design Notes:
    - Stateless: No instance state, all data passed to methods
    - Domain-focused: Uses domain concepts, not infrastructure
    - Pure: No side effects, only validates and returns results
    """

    DEFAULT_COVERAGE_THRESHOLD = 0.8
    DEFAULT_REVIEW_REQUIRED = True
    DEFAULT_DOCS_REQUIRED = True

    def __init__(
        self,
        coverage_threshold: float = DEFAULT_COVERAGE_THRESHOLD,
        review_required: bool = DEFAULT_REVIEW_REQUIRED,
        docs_required: bool = DEFAULT_DOCS_REQUIRED,
    ) -> None:
        """Initialize with quality gate configuration.

        Args:
            coverage_threshold: Minimum test coverage (0.0 to 1.0)
            review_required: Whether code review is required
            docs_required: Whether documentation is required
        """
        self._coverage_threshold = coverage_threshold
        self._review_required = review_required
        self._docs_required = docs_required

    def validate_for_completion(
        self,
        work_item: WorkItem,
        metrics: QualityMetrics,
    ) -> None:
        """Validate work item can be completed.

        Args:
            work_item: Work item to validate
            metrics: Quality metrics for the work item

        Raises:
            QualityGateError: If quality gate fails
        """
        failures = self._get_failures(work_item, metrics)

        if failures:
            raise QualityGateError(
                work_item_id=work_item.id,
                gate_level="completion",
                failures=failures,
            )

    def can_complete(
        self,
        work_item: WorkItem,
        metrics: QualityMetrics,
    ) -> bool:
        """Check if work item can be completed.

        Args:
            work_item: Work item to check
            metrics: Quality metrics

        Returns:
            True if quality gate passes
        """
        failures = self._get_failures(work_item, metrics)
        return len(failures) == 0

    def get_quality_report(
        self,
        work_item: WorkItem,
        metrics: QualityMetrics,
    ) -> dict[str, any]:
        """Generate quality report for work item.

        Args:
            work_item: Work item to report on
            metrics: Quality metrics

        Returns:
            Quality report dictionary
        """
        failures = self._get_failures(work_item, metrics)

        return {
            "work_item_id": work_item.id,
            "passes": len(failures) == 0,
            "test_coverage": f"{metrics.test_coverage_percentage:.1f}%",
            "coverage_threshold": f"{self._coverage_threshold * 100:.1f}%",
            "coverage_met": metrics.test_coverage >= self._coverage_threshold,
            "documentation_complete": metrics.documentation_complete,
            "code_reviewed": metrics.code_reviewed,
            "acceptance_criteria_met": metrics.acceptance_criteria_met,
            "failures": failures,
        }

    def _get_failures(
        self,
        work_item: WorkItem,
        metrics: QualityMetrics,
    ) -> list[str]:
        """Get list of quality gate failures.

        Args:
            work_item: Work item being validated
            metrics: Quality metrics

        Returns:
            List of failure descriptions
        """
        failures = []

        # Test coverage check
        if metrics.test_coverage < self._coverage_threshold:
            failures.append(
                f"Test coverage {metrics.test_coverage_percentage:.1f}% "
                f"below threshold {self._coverage_threshold * 100:.1f}%"
            )

        # Documentation check (if required)
        if self._docs_required and not metrics.documentation_complete:
            failures.append("Documentation not complete")

        # Code review check (if required)
        if self._review_required and not metrics.code_reviewed:
            failures.append("Code review not completed")

        # Acceptance criteria always required
        if not metrics.acceptance_criteria_met:
            failures.append("Acceptance criteria not met")

        return failures
```

---

### Dependency Validator Service

```python
# File: src/work_tracking/domain/services/dependency_validator.py
from __future__ import annotations

from typing import TYPE_CHECKING

from src.shared_kernel.exceptions import InvariantViolationError

if TYPE_CHECKING:
    from src.work_tracking.domain.aggregates.work_item import WorkItem
    from src.work_tracking.domain.ports.work_item_repository import IWorkItemRepository


class DependencyValidator:
    """Domain service for validating work item dependencies.

    Validates dependency relationships:
    - No circular dependencies
    - All dependencies exist
    - Dependency state allows operations

    Design Notes:
    - Requires repository access (injected)
    - Spans multiple aggregates
    - Enforces cross-aggregate invariants
    """

    def __init__(self, repository: IWorkItemRepository) -> None:
        """Initialize with repository for dependency lookup.

        Args:
            repository: Work item repository
        """
        self._repository = repository

    def validate_can_add_dependency(
        self,
        work_item: WorkItem,
        dependency_id: str,
    ) -> None:
        """Validate that dependency can be added.

        Checks:
        - Dependency exists
        - No self-dependency
        - No circular dependency

        Args:
            work_item: Work item to add dependency to
            dependency_id: ID of potential dependency

        Raises:
            InvariantViolationError: If dependency invalid
        """
        # Self-dependency check
        if work_item.id == dependency_id:
            raise InvariantViolationError(
                invariant="no_self_dependency",
                message="Work item cannot depend on itself",
                context={"work_item_id": work_item.id},
            )

        # Existence check
        from src.work_tracking.domain.value_objects.work_item_id import WorkItemId
        dependency = self._repository.get(WorkItemId(dependency_id))
        if dependency is None:
            raise InvariantViolationError(
                invariant="dependency_exists",
                message=f"Dependency {dependency_id} does not exist",
                context={
                    "work_item_id": work_item.id,
                    "dependency_id": dependency_id,
                },
            )

        # Circular dependency check
        if self._would_create_cycle(work_item.id, dependency_id):
            raise InvariantViolationError(
                invariant="no_circular_dependency",
                message=f"Adding dependency {dependency_id} would create circular dependency",
                context={
                    "work_item_id": work_item.id,
                    "dependency_id": dependency_id,
                },
            )

    def validate_can_complete(self, work_item: WorkItem) -> None:
        """Validate all dependencies are complete.

        Args:
            work_item: Work item to check

        Raises:
            InvariantViolationError: If incomplete dependencies exist
        """
        from src.work_tracking.domain.value_objects.work_item_id import WorkItemId
        from src.work_tracking.domain.value_objects.work_item_status import WorkItemStatus

        incomplete = []

        for dep_id in work_item.dependency_ids:
            dep = self._repository.get(WorkItemId(dep_id))
            if dep and dep.status != WorkItemStatus.DONE:
                incomplete.append(dep_id)

        if incomplete:
            raise InvariantViolationError(
                invariant="dependencies_complete",
                message="Cannot complete: incomplete dependencies exist",
                context={
                    "work_item_id": work_item.id,
                    "incomplete_dependencies": incomplete,
                },
            )

    def _would_create_cycle(
        self,
        source_id: str,
        target_id: str,
        visited: set[str] | None = None,
    ) -> bool:
        """Check if adding dependency would create cycle.

        Uses DFS to detect cycles in dependency graph.

        Args:
            source_id: Work item adding dependency
            target_id: Potential dependency
            visited: Already visited nodes (for recursion)

        Returns:
            True if cycle would be created
        """
        from src.work_tracking.domain.value_objects.work_item_id import WorkItemId

        if visited is None:
            visited = set()

        if target_id in visited:
            return False

        visited.add(target_id)

        target = self._repository.get(WorkItemId(target_id))
        if target is None:
            return False

        for dep_id in target.dependency_ids:
            if dep_id == source_id:
                return True  # Cycle detected!
            if self._would_create_cycle(source_id, dep_id, visited):
                return True

        return False

    def get_dependency_chain(self, work_item: WorkItem) -> list[str]:
        """Get ordered list of dependencies (topological sort).

        Args:
            work_item: Work item to analyze

        Returns:
            List of dependency IDs in completion order
        """
        from src.work_tracking.domain.value_objects.work_item_id import WorkItemId

        result = []
        visited = set()

        def visit(item_id: str) -> None:
            if item_id in visited:
                return
            visited.add(item_id)

            item = self._repository.get(WorkItemId(item_id))
            if item:
                for dep_id in item.dependency_ids:
                    visit(dep_id)
                result.append(item_id)

        visit(work_item.id)
        return result[:-1]  # Exclude the work item itself
```

---

## Domain Service vs Application Service

| Aspect | Domain Service | Application Service |
|--------|----------------|---------------------|
| Location | `domain/services/` | `application/handlers/` |
| Dependencies | Domain objects only | May use infrastructure |
| Concern | Domain logic | Use case orchestration |
| Example | QualityValidator | CreateWorkItemCommandHandler |

---

## Testing Pattern

```python
def test_quality_validator_fails_below_threshold():
    """Quality gate fails when coverage below threshold."""
    validator = QualityValidator(coverage_threshold=0.8)
    work_item = create_work_item()
    metrics = QualityMetrics(
        test_coverage=0.5,  # Below 0.8 threshold
        documentation_complete=True,
        code_reviewed=True,
        acceptance_criteria_met=True,
    )

    with pytest.raises(QualityGateError) as exc_info:
        validator.validate_for_completion(work_item, metrics)

    assert "coverage" in str(exc_info.value).lower()


def test_quality_validator_passes_with_good_metrics():
    """Quality gate passes with sufficient metrics."""
    validator = QualityValidator(coverage_threshold=0.8)
    work_item = create_work_item()
    metrics = QualityMetrics.fully_passing(test_coverage=0.9)

    # Should not raise
    validator.validate_for_completion(work_item, metrics)


def test_dependency_validator_detects_cycle():
    """Circular dependencies are detected."""
    repo = InMemoryRepository()
    validator = DependencyValidator(repo)

    # A -> B -> C -> A would be a cycle
    item_a = create_work_item(id="A")
    item_b = create_work_item(id="B", dependencies=["A"])
    item_c = create_work_item(id="C", dependencies=["B"])

    repo.save(item_a)
    repo.save(item_b)
    repo.save(item_c)

    with pytest.raises(InvariantViolationError) as exc_info:
        validator.validate_can_add_dependency(item_a, "C")

    assert "circular" in str(exc_info.value).lower()
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: Domain services are stateless. Configuration is passed via constructor, data via method parameters.

> **Jerry Decision**: Domain services may accept repository interfaces for cross-aggregate queries, but must not perform writes.

> **Jerry Decision**: Domain services raise domain exceptions (InvariantViolationError, QualityGateError), not generic exceptions.

---

## Anti-Patterns

### 1. Stateful Domain Service

```python
# WRONG: Service with mutable state
class QualityValidator:
    def __init__(self):
        self.last_result = None  # Mutable state!

    def validate(self, item):
        self.last_result = ...  # Side effect!

# CORRECT: Stateless service
class QualityValidator:
    def validate(self, item, metrics) -> ValidationResult:
        return ValidationResult(...)  # Pure function
```

### 2. Infrastructure in Domain Service

```python
# WRONG: Domain service uses infrastructure
class QualityValidator:
    def validate(self, item):
        coverage = requests.get(f"http://ci/coverage/{item.id}")  # HTTP call!

# CORRECT: Infrastructure injected as port
class QualityValidator:
    def __init__(self, coverage_provider: ICoverageProvider):
        self._coverage = coverage_provider
```

---

## References

- **Eric Evans**: Domain-Driven Design (2003), Chapter 5 - Services
- **Vaughn Vernon**: Implementing DDD (2013), Chapter 7
- **Design Canon**: Section 4.5 - Domain Services
- **Related Patterns**: PAT-ARCH-001 (Composition Root), PAT-AGG-004 (Invariant Enforcement)
