# Development Skill Test Strategy

**Document ID**: dev-skill-e-009-test-strategy
**Date**: 2026-01-09
**Author**: ps-analyst (Testing)

---

## Executive Summary

This test strategy defines a comprehensive testing approach for the Jerry Framework development skill, mapping the 37 patterns from the architecture analysis (e-008) to specific test types, frameworks, and quality gates. The strategy follows the test pyramid principle with adaptations for agent-based systems, emphasizing property-based testing for stateful operations and BDD for behavioral specifications.

The strategy targets:
- Unit test coverage >90% for domain layer
- Integration test coverage >80% for application layer
- Mutation score >80% for critical paths
- E2E scenario coverage for all user-facing workflows

---

## Test Pyramid Implementation

### Layer 1: Unit Tests (Bottom Layer)

**Target Coverage**: >90% line coverage, >85% branch coverage
**Framework**: pytest
**Pattern**: AAA (Arrange-Act-Assert)

#### Domain Layer Entities

| Component | Test Focus | Key Assertions |
|-----------|------------|----------------|
| `WorkItem` | Status transitions, invariant enforcement | Valid transitions only, ID immutability, timestamp ordering |
| `QualityGate` | Condition evaluation, threshold checking | Boolean evaluation, threshold bounds, gate ordering |
| `ReviewSession` | Review state machine, verdict aggregation | State transitions, reviewer limits, comment threading |
| `TestSuite` | Test result aggregation, coverage calculation | Result immutability, coverage percentage bounds |
| `ArchitectureDecision` | ADR immutability, supersession chains | Content immutability, valid supersession references |

```python
# tests/unit/domain/entities/test_work_item.py

import pytest
from datetime import datetime, timezone

from src.development.domain.entities.work_item import WorkItem
from src.development.domain.value_objects.task_status import TaskStatus
from src.development.domain.value_objects.priority import Priority
from src.development.domain.exceptions import InvalidStateTransitionError


class TestWorkItemCreation:
    """Tests for WorkItem entity creation."""

    def test_create_work_item_when_valid_inputs_then_entity_created(self):
        # Arrange
        title = "Implement feature X"
        description = "Add new capability to system"

        # Act
        item = WorkItem.create(title=title, description=description)

        # Assert
        assert item.title == title
        assert item.description == description
        assert item.status == TaskStatus.BACKLOG
        assert item.id is not None
        assert item.created_at is not None

    def test_create_work_item_when_empty_title_then_raises_validation_error(self):
        # Arrange
        title = ""

        # Act & Assert
        with pytest.raises(ValueError, match="Title cannot be empty"):
            WorkItem.create(title=title, description="desc")

    def test_create_work_item_when_title_exceeds_max_length_then_raises_error(self):
        # Arrange
        title = "x" * 256  # Exceeds 255 char limit

        # Act & Assert
        with pytest.raises(ValueError, match="Title exceeds maximum length"):
            WorkItem.create(title=title, description="desc")


class TestWorkItemStatusTransitions:
    """Tests for WorkItem status transition rules."""

    @pytest.fixture
    def work_item(self) -> WorkItem:
        return WorkItem.create(title="Test Item", description="Test")

    def test_transition_when_backlog_to_ready_then_succeeds(self, work_item: WorkItem):
        # Act
        work_item.mark_ready()

        # Assert
        assert work_item.status == TaskStatus.READY

    def test_transition_when_backlog_to_done_then_raises_invalid_state(
        self, work_item: WorkItem
    ):
        # Act & Assert
        with pytest.raises(InvalidStateTransitionError):
            work_item.mark_done()

    def test_transition_when_in_progress_to_review_then_succeeds(
        self, work_item: WorkItem
    ):
        # Arrange
        work_item.mark_ready()
        work_item.start()

        # Act
        work_item.submit_for_review()

        # Assert
        assert work_item.status == TaskStatus.REVIEW

    @pytest.mark.parametrize(
        "initial_status,target_status,should_succeed",
        [
            (TaskStatus.BACKLOG, TaskStatus.READY, True),
            (TaskStatus.READY, TaskStatus.IN_PROGRESS, True),
            (TaskStatus.IN_PROGRESS, TaskStatus.REVIEW, True),
            (TaskStatus.REVIEW, TaskStatus.DONE, True),
            (TaskStatus.BACKLOG, TaskStatus.DONE, False),
            (TaskStatus.DONE, TaskStatus.BACKLOG, False),
            (TaskStatus.CANCELLED, TaskStatus.READY, False),
        ],
    )
    def test_status_transition_matrix(
        self,
        work_item: WorkItem,
        initial_status: TaskStatus,
        target_status: TaskStatus,
        should_succeed: bool,
    ):
        # Arrange - Set up to initial status
        work_item._set_status_for_test(initial_status)

        # Act & Assert
        if should_succeed:
            work_item.transition_to(target_status)
            assert work_item.status == target_status
        else:
            with pytest.raises(InvalidStateTransitionError):
                work_item.transition_to(target_status)
```

#### Domain Layer Value Objects

| Component | Test Focus | Key Assertions |
|-----------|------------|----------------|
| `TaskStatus` | Enum values, transition validity | All statuses defined, transition rules encoded |
| `Priority` | Ordering, comparison operations | Correct ordering (critical > high > medium > low) |
| `RiskTier` | Classification boundaries, comparisons | T1 < T2 < T3 < T4, boundary values |
| `AcceptanceCriterion` | Gherkin parsing, validation | Given-When-Then structure, placeholder extraction |
| `SuccessCriterion` | Command validation, threshold parsing | Valid shell commands, numeric threshold parsing |
| `DependencyGraph` | DAG validation, cycle detection | Acyclic enforcement, topological ordering |
| `SnowflakeId` | Format validation, timestamp extraction | 64-bit bounds, monotonic timestamps |
| `FileVersion` | Hash consistency, comparison | Deterministic hashing, equality semantics |

```python
# tests/unit/domain/value_objects/test_acceptance_criterion.py

import pytest
from src.development.domain.value_objects.acceptance_criterion import (
    AcceptanceCriterion,
    InvalidGherkinError,
)


class TestAcceptanceCriterionParsing:
    """Tests for Gherkin acceptance criterion parsing."""

    def test_parse_when_valid_given_when_then_then_succeeds(self):
        # Arrange
        gherkin = """
        Given I have a user account
        When I submit valid credentials
        Then I should be logged in
        """

        # Act
        criterion = AcceptanceCriterion.parse(gherkin)

        # Assert
        assert criterion.given == "I have a user account"
        assert criterion.when == "I submit valid credentials"
        assert criterion.then == "I should be logged in"

    def test_parse_when_missing_given_then_raises_error(self):
        # Arrange
        gherkin = """
        When I submit valid credentials
        Then I should be logged in
        """

        # Act & Assert
        with pytest.raises(InvalidGherkinError, match="Missing 'Given' clause"):
            AcceptanceCriterion.parse(gherkin)

    def test_parse_when_contains_and_clauses_then_captures_all(self):
        # Arrange
        gherkin = """
        Given I have a user account
        And the account is active
        When I submit valid credentials
        Then I should be logged in
        And I should see my dashboard
        """

        # Act
        criterion = AcceptanceCriterion.parse(gherkin)

        # Assert
        assert "the account is active" in criterion.given_extensions
        assert "I should see my dashboard" in criterion.then_extensions

    def test_parse_when_contains_placeholders_then_extracts_them(self):
        # Arrange
        gherkin = """
        Given I have <quantity> items in my cart
        When I checkout with <payment_method>
        Then I should see order confirmation
        """

        # Act
        criterion = AcceptanceCriterion.parse(gherkin)

        # Assert
        assert criterion.placeholders == {"quantity", "payment_method"}


class TestAcceptanceCriterionImmutability:
    """Tests ensuring AcceptanceCriterion is immutable."""

    def test_criterion_when_attempting_modification_then_raises_error(self):
        # Arrange
        criterion = AcceptanceCriterion.parse(
            "Given X\nWhen Y\nThen Z"
        )

        # Act & Assert
        with pytest.raises(AttributeError):
            criterion.given = "Modified"
```

#### Domain Layer Services

| Service | Test Focus | Key Assertions |
|---------|------------|----------------|
| `TaskDecompositionService` | WBS decomposition, 100% rule | Sum of children equals parent, vertical slicing |
| `QualityGateEvaluator` | Gate condition evaluation | SLO threshold checking, gate ordering |
| `RiskAssessmentService` | Risk tier classification | File count thresholds, impact classification |
| `DependencyResolver` | Topological sorting | Correct ordering, cycle detection |

```python
# tests/unit/domain/services/test_dependency_resolver.py

import pytest
from src.development.domain.services.dependency_resolver import DependencyResolver
from src.development.domain.value_objects.dependency_graph import (
    DependencyGraph,
    CyclicDependencyError,
)


class TestDependencyResolverTopologicalSort:
    """Tests for topological sorting of task dependencies."""

    @pytest.fixture
    def resolver(self) -> DependencyResolver:
        return DependencyResolver()

    def test_resolve_when_linear_dependencies_then_returns_correct_order(
        self, resolver: DependencyResolver
    ):
        # Arrange
        graph = DependencyGraph()
        graph.add_dependency("task-c", "task-b")  # C depends on B
        graph.add_dependency("task-b", "task-a")  # B depends on A

        # Act
        order = resolver.resolve(graph)

        # Assert
        assert order == ["task-a", "task-b", "task-c"]

    def test_resolve_when_diamond_dependencies_then_handles_correctly(
        self, resolver: DependencyResolver
    ):
        # Arrange - Diamond: D depends on B,C; B,C depend on A
        graph = DependencyGraph()
        graph.add_dependency("task-d", "task-b")
        graph.add_dependency("task-d", "task-c")
        graph.add_dependency("task-b", "task-a")
        graph.add_dependency("task-c", "task-a")

        # Act
        order = resolver.resolve(graph)

        # Assert
        assert order.index("task-a") < order.index("task-b")
        assert order.index("task-a") < order.index("task-c")
        assert order.index("task-b") < order.index("task-d")
        assert order.index("task-c") < order.index("task-d")

    def test_resolve_when_cycle_detected_then_raises_error(
        self, resolver: DependencyResolver
    ):
        # Arrange - Cycle: A -> B -> C -> A
        graph = DependencyGraph()
        graph.add_dependency("task-a", "task-c")
        graph.add_dependency("task-b", "task-a")
        graph.add_dependency("task-c", "task-b")

        # Act & Assert
        with pytest.raises(CyclicDependencyError) as exc_info:
            resolver.resolve(graph)
        assert "task-a" in str(exc_info.value)

    def test_resolve_when_empty_graph_then_returns_empty_list(
        self, resolver: DependencyResolver
    ):
        # Arrange
        graph = DependencyGraph()

        # Act
        order = resolver.resolve(graph)

        # Assert
        assert order == []

    def test_resolve_when_independent_tasks_then_any_order_valid(
        self, resolver: DependencyResolver
    ):
        # Arrange
        graph = DependencyGraph()
        graph.add_node("task-a")
        graph.add_node("task-b")
        graph.add_node("task-c")

        # Act
        order = resolver.resolve(graph)

        # Assert
        assert set(order) == {"task-a", "task-b", "task-c"}
```

### Layer 2: Integration Tests (Middle Layer)

**Target Coverage**: >80% line coverage
**Framework**: pytest + fixtures
**Pattern**: Repository mocking, adapter testing

#### Application Layer Command Handlers

| Handler | Test Focus | Mocked Dependencies |
|---------|------------|---------------------|
| `CreateWorkItemHandler` | Successful creation, validation errors | `IWorkItemRepository`, `IIdGenerator` |
| `GenerateTestsHandler` | Test generation flow, failure handling | `ICodeGenerationPort`, `ITestRunnerPort` |
| `GenerateCodeHandler` | Code generation, test-first enforcement | `ICodeGenerationPort`, `IQualityGatePort` |
| `ExecuteQualityGateHandler` | Gate cascade execution | `IQualityGatePort`, `IEventPublisher` |
| `RequestReviewHandler` | Review request routing | `IReviewRepository`, `IRiskAssessmentPort` |

```python
# tests/integration/application/handlers/test_generate_tests_handler.py

import pytest
from unittest.mock import Mock, AsyncMock
from src.development.application.handlers.commands.generation_handlers import (
    GenerateTestsHandler,
)
from src.development.application.commands.generation_commands import (
    GenerateTestsCommand,
)
from src.development.application.ports.generation_ports import ICodeGenerationPort
from src.development.application.ports.execution_ports import ITestRunnerPort
from src.development.domain.entities.work_item import WorkItem
from src.development.domain.events.test_events import TestsGenerated


class TestGenerateTestsHandler:
    """Integration tests for test generation command handler."""

    @pytest.fixture
    def mock_code_generation_port(self) -> Mock:
        port = Mock(spec=ICodeGenerationPort)
        port.generate_tests = AsyncMock(
            return_value="""
def test_example():
    assert True
"""
        )
        return port

    @pytest.fixture
    def mock_test_runner_port(self) -> Mock:
        port = Mock(spec=ITestRunnerPort)
        port.run_tests = AsyncMock(
            return_value=Mock(
                passed=0, failed=1, errors=0, total=1, output="1 failed"
            )
        )
        return port

    @pytest.fixture
    def handler(
        self,
        mock_code_generation_port: Mock,
        mock_test_runner_port: Mock,
    ) -> GenerateTestsHandler:
        return GenerateTestsHandler(
            code_generation_port=mock_code_generation_port,
            test_runner_port=mock_test_runner_port,
        )

    @pytest.fixture
    def work_item(self) -> WorkItem:
        item = WorkItem.create(
            title="Implement user login",
            description="Add login functionality with OAuth",
        )
        item.add_acceptance_criterion(
            "Given a valid user\nWhen they submit credentials\nThen they are logged in"
        )
        return item

    async def test_handle_when_valid_work_item_then_generates_tests(
        self,
        handler: GenerateTestsHandler,
        work_item: WorkItem,
        mock_code_generation_port: Mock,
    ):
        # Arrange
        command = GenerateTestsCommand(work_item=work_item)

        # Act
        result = await handler.handle(command)

        # Assert
        mock_code_generation_port.generate_tests.assert_called_once()
        assert result.success is True
        assert result.test_code is not None

    async def test_handle_when_tests_generated_then_runs_tests(
        self,
        handler: GenerateTestsHandler,
        work_item: WorkItem,
        mock_test_runner_port: Mock,
    ):
        # Arrange
        command = GenerateTestsCommand(work_item=work_item)

        # Act
        result = await handler.handle(command)

        # Assert
        mock_test_runner_port.run_tests.assert_called_once()
        assert result.test_result.failed == 1  # Tests should fail (RED phase)

    async def test_handle_when_tests_pass_initially_then_raises_error(
        self,
        handler: GenerateTestsHandler,
        work_item: WorkItem,
        mock_test_runner_port: Mock,
    ):
        # Arrange - Tests pass (violates Red phase)
        mock_test_runner_port.run_tests = AsyncMock(
            return_value=Mock(passed=1, failed=0, errors=0, total=1)
        )
        command = GenerateTestsCommand(work_item=work_item)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.success is False
        assert "Tests must fail initially" in result.error_message

    async def test_handle_when_generation_fails_then_returns_error(
        self,
        handler: GenerateTestsHandler,
        work_item: WorkItem,
        mock_code_generation_port: Mock,
    ):
        # Arrange
        mock_code_generation_port.generate_tests = AsyncMock(
            side_effect=Exception("Generation failed")
        )
        command = GenerateTestsCommand(work_item=work_item)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.success is False
        assert "Generation failed" in result.error_message

    async def test_handle_when_complete_then_emits_tests_generated_event(
        self,
        handler: GenerateTestsHandler,
        work_item: WorkItem,
    ):
        # Arrange
        command = GenerateTestsCommand(work_item=work_item)

        # Act
        result = await handler.handle(command)

        # Assert
        assert len(result.events) == 1
        assert isinstance(result.events[0], TestsGenerated)
        assert result.events[0].work_item_id == work_item.id
```

#### Infrastructure Adapter Tests

| Adapter | Test Focus | External Dependencies |
|---------|------------|----------------------|
| `FileSystemWorkItemAdapter` | CRUD operations, atomic writes | Filesystem (tmpdir fixture) |
| `PyFileLockAdapter` | Lock acquisition, timeout handling | Filesystem (real locks) |
| `SnowflakeIdAdapter` | ID generation, uniqueness | Clock (mockable) |
| `PytestRunnerAdapter` | Test execution, output parsing | pytest subprocess |

```python
# tests/integration/infrastructure/adapters/test_filesystem_work_item_adapter.py

import pytest
import tempfile
from pathlib import Path
from src.development.infrastructure.adapters.persistence.filesystem_work_item_adapter import (
    FileSystemWorkItemAdapter,
)
from src.development.domain.entities.work_item import WorkItem
from src.development.domain.exceptions import WorkItemNotFoundError


class TestFileSystemWorkItemAdapterPersistence:
    """Integration tests for file system work item adapter."""

    @pytest.fixture
    def temp_dir(self) -> Path:
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def adapter(self, temp_dir: Path) -> FileSystemWorkItemAdapter:
        return FileSystemWorkItemAdapter(base_path=temp_dir)

    @pytest.fixture
    def sample_work_item(self) -> WorkItem:
        return WorkItem.create(
            title="Test Work Item",
            description="A test item for persistence testing",
        )

    async def test_save_when_new_item_then_creates_file(
        self,
        adapter: FileSystemWorkItemAdapter,
        sample_work_item: WorkItem,
        temp_dir: Path,
    ):
        # Act
        await adapter.save(sample_work_item)

        # Assert
        expected_path = temp_dir / f"{sample_work_item.id}.json"
        assert expected_path.exists()

    async def test_save_when_existing_item_then_updates_file(
        self,
        adapter: FileSystemWorkItemAdapter,
        sample_work_item: WorkItem,
    ):
        # Arrange
        await adapter.save(sample_work_item)
        sample_work_item.mark_ready()

        # Act
        await adapter.save(sample_work_item)

        # Assert
        retrieved = await adapter.get_by_id(sample_work_item.id)
        assert retrieved.status.name == "READY"

    async def test_get_by_id_when_exists_then_returns_item(
        self,
        adapter: FileSystemWorkItemAdapter,
        sample_work_item: WorkItem,
    ):
        # Arrange
        await adapter.save(sample_work_item)

        # Act
        retrieved = await adapter.get_by_id(sample_work_item.id)

        # Assert
        assert retrieved.id == sample_work_item.id
        assert retrieved.title == sample_work_item.title
        assert retrieved.description == sample_work_item.description

    async def test_get_by_id_when_not_exists_then_raises_error(
        self,
        adapter: FileSystemWorkItemAdapter,
    ):
        # Act & Assert
        with pytest.raises(WorkItemNotFoundError):
            await adapter.get_by_id("nonexistent-id")

    async def test_delete_when_exists_then_removes_file(
        self,
        adapter: FileSystemWorkItemAdapter,
        sample_work_item: WorkItem,
        temp_dir: Path,
    ):
        # Arrange
        await adapter.save(sample_work_item)
        file_path = temp_dir / f"{sample_work_item.id}.json"
        assert file_path.exists()

        # Act
        await adapter.delete(sample_work_item.id)

        # Assert
        assert not file_path.exists()

    async def test_list_all_when_multiple_items_then_returns_all(
        self,
        adapter: FileSystemWorkItemAdapter,
    ):
        # Arrange
        items = [
            WorkItem.create(title=f"Item {i}", description=f"Desc {i}")
            for i in range(5)
        ]
        for item in items:
            await adapter.save(item)

        # Act
        retrieved = await adapter.list_all()

        # Assert
        assert len(retrieved) == 5
        retrieved_ids = {item.id for item in retrieved}
        expected_ids = {item.id for item in items}
        assert retrieved_ids == expected_ids


class TestFileSystemWorkItemAdapterAtomicity:
    """Tests for atomic write operations."""

    @pytest.fixture
    def temp_dir(self) -> Path:
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def adapter(self, temp_dir: Path) -> FileSystemWorkItemAdapter:
        return FileSystemWorkItemAdapter(base_path=temp_dir)

    async def test_save_when_interrupted_then_no_partial_write(
        self,
        adapter: FileSystemWorkItemAdapter,
        temp_dir: Path,
    ):
        # Arrange
        item = WorkItem.create(title="Test", description="Test")
        await adapter.save(item)
        original_content = (temp_dir / f"{item.id}.json").read_text()

        # Act - Simulate failure during write by checking temp file cleanup
        temp_files = list(temp_dir.glob("*.tmp"))

        # Assert - No temp files should remain
        assert len(temp_files) == 0

    async def test_save_when_concurrent_writes_then_no_corruption(
        self,
        adapter: FileSystemWorkItemAdapter,
    ):
        # Arrange
        import asyncio

        item = WorkItem.create(title="Concurrent Test", description="Test")
        await adapter.save(item)

        async def update_item(version: int):
            retrieved = await adapter.get_by_id(item.id)
            retrieved._description = f"Updated by version {version}"
            await adapter.save(retrieved)

        # Act - Concurrent updates
        await asyncio.gather(*[update_item(i) for i in range(10)])

        # Assert - File should be valid JSON
        retrieved = await adapter.get_by_id(item.id)
        assert retrieved is not None
        assert "Updated by version" in retrieved.description
```

### Layer 3: System Tests (Upper Layer)

**Framework**: pytest-bdd
**Pattern**: BDD scenarios for multi-component workflows

#### BDD Feature Files

```gherkin
# tests/system/features/test_first_development.feature

@workflow @test-first
Feature: Test-First Development Workflow
    As a developer using Jerry
    I want to follow test-first discipline
    So that code quality is maintained

    Background:
        Given the development skill is initialized
        And I have a project workspace

    @happy-path
    Scenario: Complete TDD cycle for new feature
        Given I have a work item "Implement user authentication"
        And the work item has acceptance criteria:
            | criterion                                          |
            | Given valid credentials When login Then succeed    |
            | Given invalid credentials When login Then fail     |
        When I request test generation for the work item
        Then tests should be generated
        And the tests should initially fail
        When I request code generation for the work item
        Then code should be generated
        And all tests should pass
        And the work item status should be "REVIEW"

    @red-phase
    Scenario: Test generation produces failing tests
        Given I have a work item "Add validation logic"
        When I request test generation for the work item
        Then tests should be generated
        And the test runner should report failures
        And no implementation code should exist

    @green-phase
    Scenario: Code generation makes tests pass
        Given I have a work item with generated tests
        And the tests are currently failing
        When I request code generation for the work item
        Then code should be generated
        And all tests should pass

    @enforcement
    Scenario: Cannot generate code without tests
        Given I have a work item without tests
        When I attempt to generate code for the work item
        Then the operation should be rejected
        And the error should mention "tests must be generated first"

    @failure-handling
    Scenario: Code generation retry on test failure
        Given I have a work item with generated tests
        When I request code generation for the work item
        And the generated code does not pass all tests
        Then the system should retry code generation
        And the retry should include the failure information
```

```gherkin
# tests/system/features/quality_gate_cascade.feature

@workflow @quality-gates
Feature: Quality Gate Cascade
    As a code reviewer
    I want quality gates to catch issues early
    So that code quality is maintained

    Background:
        Given the quality orchestration service is initialized
        And all quality adapters are configured

    @cascade
    Scenario: Full quality gate cascade succeeds
        Given I have code changes ready for validation
        When I execute the quality gate cascade
        Then the pre-commit checks should pass
        And the linter checks should pass
        And the coverage checks should pass
        And the test suite should pass
        And the overall gate result should be "PASSED"

    @early-exit
    Scenario: Cascade stops on first failure
        Given I have code changes with formatting issues
        When I execute the quality gate cascade
        Then the pre-commit checks should fail
        And the linter checks should not be executed
        And the overall gate result should be "FAILED"
        And the failure reason should include "formatting"

    @coverage-threshold
    Scenario Outline: Coverage gate enforces threshold
        Given I have code changes with <coverage>% coverage
        When I execute the coverage quality gate
        Then the gate result should be "<result>"

        Examples:
            | coverage | result |
            | 95       | PASSED |
            | 80       | PASSED |
            | 79       | FAILED |
            | 50       | FAILED |

    @slo-based
    Scenario: SLO-based quality gate
        Given I have a quality gate with SLO conditions
        And the SLO requires 99.9% availability
        When I check the SLO condition
        And the actual availability is 99.95%
        Then the gate should pass
```

```gherkin
# tests/system/features/tiered_review.feature

@workflow @review
Feature: Tiered Code Review
    As a development team lead
    I want reviews scaled to change risk
    So that we balance thoroughness with velocity

    Background:
        Given the review coordination service is initialized
        And the risk assessment service is configured

    @tier-classification
    Scenario Outline: Risk tier classification based on change type
        Given I have code changes in "<change_type>" category
        And the changes affect <file_count> files
        When I request risk assessment
        Then the risk tier should be "<tier>"

        Examples:
            | change_type    | file_count | tier |
            | documentation  | 5          | T1   |
            | configuration  | 3          | T1   |
            | feature        | 10         | T2   |
            | api_change     | 5          | T3   |
            | security       | 2          | T3   |
            | core_logic     | 20         | T4   |
            | safety_critical| 1          | T4   |

    @human-gate
    Scenario: High-risk changes require human approval
        Given I have code changes classified as T3 risk
        When I submit the changes for review
        Then an agent review should be performed
        And a human approval request should be created
        And the review should not complete until human approval

    @automated-approval
    Scenario: Low-risk changes auto-approved
        Given I have code changes classified as T1 risk
        When I submit the changes for review
        Then an agent review should be performed
        And the review should complete automatically
        And no human approval should be required

    @adr-compliance
    Scenario: Review checks ADR compliance
        Given I have an ADR requiring all services to use async I/O
        And I have code changes adding a synchronous HTTP client
        When the agent reviews the changes
        Then the review should flag ADR violation
        And the comment should reference the relevant ADR
```

### Layer 4: E2E Tests (Top Layer)

**Framework**: subprocess + assertions
**Pattern**: Golden file testing, full skill invocation

```python
# tests/e2e/test_development_skill_invocation.py

import pytest
import subprocess
import json
import tempfile
from pathlib import Path


class TestDevelopmentSkillE2E:
    """End-to-end tests for development skill invocation."""

    @pytest.fixture
    def workspace(self) -> Path:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir) / "test_workspace"
            workspace.mkdir()
            (workspace / ".jerry").mkdir()
            (workspace / ".jerry" / "data").mkdir()
            yield workspace

    @pytest.fixture
    def skill_runner(self, workspace: Path):
        def run_skill(command: str, *args: str) -> subprocess.CompletedProcess:
            cmd = [
                "python", "-m", "jerry.skills.development",
                command, *args,
                "--workspace", str(workspace),
            ]
            return subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )
        return run_skill

    def test_create_task_e2e(self, skill_runner, workspace: Path):
        # Act
        result = skill_runner(
            "task", "create",
            "--title", "E2E Test Task",
            "--description", "A task created in E2E test",
        )

        # Assert
        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert output["success"] is True
        assert "id" in output
        assert output["title"] == "E2E Test Task"

        # Verify persistence
        items_dir = workspace / ".jerry" / "data" / "items"
        assert len(list(items_dir.glob("*.json"))) == 1

    def test_list_tasks_e2e(self, skill_runner, workspace: Path):
        # Arrange - Create some tasks
        for i in range(3):
            skill_runner("task", "create", "--title", f"Task {i}")

        # Act
        result = skill_runner("task", "list")

        # Assert
        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert output["success"] is True
        assert len(output["items"]) == 3

    def test_generate_tests_e2e(self, skill_runner, workspace: Path):
        # Arrange - Create a task with acceptance criteria
        create_result = skill_runner(
            "task", "create",
            "--title", "Calculator Add Function",
            "--description", "Implement addition function",
            "--acceptance", "Given two numbers When add Then return sum",
        )
        task_id = json.loads(create_result.stdout)["id"]

        # Act
        result = skill_runner("generate", "tests", "--task-id", task_id)

        # Assert
        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert output["success"] is True
        assert "test_code" in output
        assert "def test_" in output["test_code"]

    def test_full_tdd_cycle_e2e(self, skill_runner, workspace: Path):
        # Arrange - Create a task
        create_result = skill_runner(
            "task", "create",
            "--title", "String Reverser",
            "--description", "Implement string reverse function",
            "--acceptance", "Given a string When reverse Then return reversed string",
        )
        task_id = json.loads(create_result.stdout)["id"]

        # Act - Generate tests
        test_result = skill_runner("generate", "tests", "--task-id", task_id)
        assert test_result.returncode == 0
        test_output = json.loads(test_result.stdout)
        assert test_output["test_result"]["failed"] > 0  # Tests should fail

        # Act - Generate code
        code_result = skill_runner("generate", "code", "--task-id", task_id)
        assert code_result.returncode == 0
        code_output = json.loads(code_result.stdout)
        assert code_output["test_result"]["failed"] == 0  # Tests should pass

        # Act - Run quality gate
        gate_result = skill_runner("gate", "run", "--task-id", task_id)
        assert gate_result.returncode == 0
        gate_output = json.loads(gate_result.stdout)
        assert gate_output["result"] == "PASSED"

    def test_quality_gate_failure_e2e(self, skill_runner, workspace: Path):
        # Arrange - Create a task and generate non-compliant code
        create_result = skill_runner(
            "task", "create",
            "--title", "Non-compliant Code",
        )
        task_id = json.loads(create_result.stdout)["id"]

        # Manually create non-compliant code (missing type hints)
        code_file = workspace / "generated" / f"{task_id}.py"
        code_file.parent.mkdir(exist_ok=True)
        code_file.write_text("def func(x):\n    return x\n")

        # Act
        result = skill_runner("gate", "run", "--task-id", task_id)

        # Assert
        assert result.returncode == 1
        output = json.loads(result.stdout)
        assert output["result"] == "FAILED"
        assert "type hints" in output["failures"][0].lower()
```

---

## BDD Feature Files

### Feature Template Structure

```gherkin
# Template: tests/system/features/{domain}_{workflow}.feature

@{domain} @{workflow-tag}
Feature: {Feature Name}
    As a {role}
    I want {capability}
    So that {benefit}

    Background:
        Given {common setup step 1}
        And {common setup step 2}

    @happy-path
    Scenario: {Happy path scenario name}
        Given {precondition}
        When {action}
        Then {expected outcome}

    @edge-case
    Scenario: {Edge case scenario name}
        Given {edge case precondition}
        When {action}
        Then {expected edge case handling}

    @error-handling
    Scenario: {Error scenario name}
        Given {error condition}
        When {action triggering error}
        Then {error should be reported}
        And {system should remain stable}

    @parametric
    Scenario Outline: {Parameterized scenario name}
        Given {parameterized precondition with <param>}
        When {action with <input>}
        Then {outcome with <expected>}

        Examples:
            | param  | input  | expected |
            | value1 | input1 | result1  |
            | value2 | input2 | result2  |
```

### Step Definitions Structure

```
tests/
├── system/
│   ├── features/
│   │   ├── test_first_development.feature
│   │   ├── quality_gate_cascade.feature
│   │   ├── tiered_review.feature
│   │   └── agent_orchestration.feature
│   ├── step_defs/
│   │   ├── conftest.py              # Shared fixtures
│   │   ├── common_steps.py          # Shared step definitions
│   │   ├── work_item_steps.py       # WorkItem-related steps
│   │   ├── generation_steps.py      # Code/test generation steps
│   │   ├── quality_steps.py         # Quality gate steps
│   │   └── review_steps.py          # Review workflow steps
│   └── conftest.py                  # pytest-bdd scenario registration
```

```python
# tests/system/step_defs/conftest.py

import pytest
from pytest_bdd import given, when, then, parsers
from src.development.domain.entities.work_item import WorkItem
from src.development.application.services.development_workflow import (
    DevelopmentWorkflowService,
)


@pytest.fixture
def work_item_context():
    """Shared context for work item scenarios."""
    return {
        "work_item": None,
        "test_code": None,
        "impl_code": None,
        "test_result": None,
        "gate_result": None,
        "review_result": None,
        "error": None,
    }


@pytest.fixture
def workflow_service(mock_ports) -> DevelopmentWorkflowService:
    """Initialize workflow service with mocked ports."""
    return DevelopmentWorkflowService(
        code_generation_port=mock_ports.code_generation,
        test_runner_port=mock_ports.test_runner,
        quality_gate_port=mock_ports.quality_gate,
        work_item_repository=mock_ports.work_item_repo,
    )


@given("the development skill is initialized")
def skill_initialized(workflow_service):
    assert workflow_service is not None


@given("I have a project workspace")
def project_workspace(tmp_path):
    workspace = tmp_path / "test_workspace"
    workspace.mkdir()
    (workspace / ".jerry").mkdir()
    return workspace


@given(parsers.parse('I have a work item "{title}"'))
def have_work_item(work_item_context, title):
    work_item_context["work_item"] = WorkItem.create(
        title=title,
        description=f"Description for {title}",
    )
```

```python
# tests/system/step_defs/generation_steps.py

from pytest_bdd import given, when, then, parsers
from src.development.domain.value_objects.task_status import TaskStatus


@given("the work item has acceptance criteria:")
def work_item_has_criteria(work_item_context, datatable):
    work_item = work_item_context["work_item"]
    for row in datatable:
        work_item.add_acceptance_criterion(row["criterion"])


@when("I request test generation for the work item")
async def request_test_generation(work_item_context, workflow_service):
    try:
        result = await workflow_service.generate_tests(
            work_item_context["work_item"]
        )
        work_item_context["test_code"] = result.test_code
        work_item_context["test_result"] = result.test_result
    except Exception as e:
        work_item_context["error"] = e


@then("tests should be generated")
def tests_generated(work_item_context):
    assert work_item_context["test_code"] is not None
    assert "def test_" in work_item_context["test_code"]


@then("the tests should initially fail")
def tests_initially_fail(work_item_context):
    assert work_item_context["test_result"].failed > 0


@when("I request code generation for the work item")
async def request_code_generation(work_item_context, workflow_service):
    try:
        result = await workflow_service.generate_code(
            work_item_context["work_item"]
        )
        work_item_context["impl_code"] = result.code
        work_item_context["test_result"] = result.test_result
    except Exception as e:
        work_item_context["error"] = e


@then("code should be generated")
def code_generated(work_item_context):
    assert work_item_context["impl_code"] is not None


@then("all tests should pass")
def all_tests_pass(work_item_context):
    assert work_item_context["test_result"].failed == 0
    assert work_item_context["test_result"].passed > 0


@then(parsers.parse('the work item status should be "{status}"'))
def work_item_status(work_item_context, status):
    assert work_item_context["work_item"].status.name == status
```

---

## Property-Based Testing

### Hypothesis Strategies

```python
# tests/strategies/__init__.py

from hypothesis import strategies as st
from src.development.domain.entities.work_item import WorkItem
from src.development.domain.value_objects.task_status import TaskStatus
from src.development.domain.value_objects.priority import Priority
from src.development.domain.value_objects.risk_tier import RiskTier
from src.development.domain.value_objects.acceptance_criterion import (
    AcceptanceCriterion,
)


# Primitive strategies
valid_title = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "P", "S")),
    min_size=1,
    max_size=255,
).filter(lambda s: s.strip())

valid_description = st.text(min_size=0, max_size=4096)

valid_gherkin_clause = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "P", "S", "Z")),
    min_size=5,
    max_size=200,
).filter(lambda s: s.strip() and not s.startswith(" "))


# Enum strategies
task_status_strategy = st.sampled_from(list(TaskStatus))
priority_strategy = st.sampled_from(list(Priority))
risk_tier_strategy = st.sampled_from(list(RiskTier))


# Composite strategies
@st.composite
def acceptance_criterion_strategy(draw):
    """Generate valid AcceptanceCriterion instances."""
    given_clause = draw(valid_gherkin_clause)
    when_clause = draw(valid_gherkin_clause)
    then_clause = draw(valid_gherkin_clause)

    gherkin = f"Given {given_clause}\nWhen {when_clause}\nThen {then_clause}"
    return AcceptanceCriterion.parse(gherkin)


@st.composite
def work_item_strategy(draw, with_criteria: bool = False):
    """Generate valid WorkItem instances."""
    title = draw(valid_title)
    description = draw(valid_description)
    priority = draw(priority_strategy)

    item = WorkItem.create(
        title=title,
        description=description,
        priority=priority,
    )

    if with_criteria:
        num_criteria = draw(st.integers(min_value=1, max_value=5))
        for _ in range(num_criteria):
            criterion = draw(acceptance_criterion_strategy())
            item.add_acceptance_criterion(criterion.to_gherkin())

    return item


@st.composite
def dependency_graph_strategy(draw, max_nodes: int = 20):
    """Generate valid (acyclic) dependency graphs."""
    from src.development.domain.value_objects.dependency_graph import DependencyGraph

    num_nodes = draw(st.integers(min_value=0, max_value=max_nodes))
    node_ids = [f"task-{i}" for i in range(num_nodes)]

    graph = DependencyGraph()
    for node_id in node_ids:
        graph.add_node(node_id)

    # Add edges only forward (ensures acyclic)
    for i, source in enumerate(node_ids):
        if i + 1 < len(node_ids):
            # Can only depend on later nodes (reverse topological order)
            possible_targets = node_ids[i + 1:]
            if possible_targets:
                add_edge = draw(st.booleans())
                if add_edge:
                    target = draw(st.sampled_from(possible_targets))
                    graph.add_dependency(source, target)

    return graph


@st.composite
def snowflake_id_strategy(draw):
    """Generate valid SnowflakeId instances."""
    from src.development.domain.value_objects.snowflake_id import SnowflakeId

    timestamp_ms = draw(st.integers(min_value=0, max_value=2**41 - 1))
    worker_id = draw(st.integers(min_value=0, max_value=2**10 - 1))
    sequence = draw(st.integers(min_value=0, max_value=2**12 - 1))

    return SnowflakeId.from_components(timestamp_ms, worker_id, sequence)
```

### Stateful Testing

```python
# tests/property/test_work_item_state_machine.py

from hypothesis import settings, Phase
from hypothesis.stateful import (
    RuleBasedStateMachine,
    Bundle,
    rule,
    invariant,
    initialize,
    precondition,
)
import hypothesis.strategies as st
from src.development.domain.entities.work_item import WorkItem
from src.development.domain.value_objects.task_status import TaskStatus
from src.development.domain.exceptions import InvalidStateTransitionError


class WorkItemStateMachine(RuleBasedStateMachine):
    """Stateful property-based tests for WorkItem state transitions."""

    def __init__(self):
        super().__init__()
        self.work_item: WorkItem | None = None
        self.status_history: list[TaskStatus] = []

    @initialize()
    def init_work_item(self):
        self.work_item = WorkItem.create(
            title="Stateful Test Item",
            description="Item for state machine testing",
        )
        self.status_history = [TaskStatus.BACKLOG]

    @rule()
    def mark_ready(self):
        """Attempt to mark the work item as ready."""
        if self.work_item.status == TaskStatus.BACKLOG:
            self.work_item.mark_ready()
            self.status_history.append(TaskStatus.READY)

    @rule()
    def start_work(self):
        """Attempt to start work on the item."""
        if self.work_item.status == TaskStatus.READY:
            self.work_item.start()
            self.status_history.append(TaskStatus.IN_PROGRESS)

    @rule()
    def submit_for_review(self):
        """Attempt to submit for review."""
        if self.work_item.status == TaskStatus.IN_PROGRESS:
            self.work_item.submit_for_review()
            self.status_history.append(TaskStatus.REVIEW)

    @rule()
    def complete(self):
        """Attempt to complete the item."""
        if self.work_item.status == TaskStatus.REVIEW:
            self.work_item.mark_done()
            self.status_history.append(TaskStatus.DONE)

    @rule()
    def cancel(self):
        """Attempt to cancel the item."""
        if self.work_item.status not in [TaskStatus.DONE, TaskStatus.CANCELLED]:
            self.work_item.cancel()
            self.status_history.append(TaskStatus.CANCELLED)

    @rule()
    def reopen_from_review(self):
        """Attempt to reopen from review."""
        if self.work_item.status == TaskStatus.REVIEW:
            self.work_item.reopen()
            self.status_history.append(TaskStatus.IN_PROGRESS)

    @invariant()
    def status_matches_history(self):
        """Current status should match last status in history."""
        assert self.work_item.status == self.status_history[-1]

    @invariant()
    def no_invalid_transitions(self):
        """Status transitions should follow valid paths."""
        valid_transitions = {
            TaskStatus.BACKLOG: {TaskStatus.READY, TaskStatus.CANCELLED},
            TaskStatus.READY: {TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED},
            TaskStatus.IN_PROGRESS: {TaskStatus.REVIEW, TaskStatus.CANCELLED},
            TaskStatus.REVIEW: {TaskStatus.DONE, TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED},
            TaskStatus.DONE: set(),
            TaskStatus.CANCELLED: set(),
        }

        for i in range(1, len(self.status_history)):
            prev_status = self.status_history[i - 1]
            curr_status = self.status_history[i]
            assert curr_status in valid_transitions[prev_status], (
                f"Invalid transition: {prev_status} -> {curr_status}"
            )

    @invariant()
    def timestamps_monotonic(self):
        """Timestamps should be monotonically increasing."""
        if self.work_item.updated_at is not None:
            assert self.work_item.updated_at >= self.work_item.created_at


TestWorkItemStateMachine = WorkItemStateMachine.TestCase
TestWorkItemStateMachine.settings = settings(
    max_examples=100,
    stateful_step_count=20,
    phases=[Phase.generate, Phase.target, Phase.shrink],
)
```

```python
# tests/property/test_quality_gate_state_machine.py

from hypothesis.stateful import (
    RuleBasedStateMachine,
    rule,
    invariant,
    initialize,
)
from src.development.domain.entities.quality_gate import QualityGate, GateResult
from src.development.domain.services.quality_gate_evaluator import QualityGateEvaluator


class QualityGateCascadeStateMachine(RuleBasedStateMachine):
    """Stateful tests for quality gate cascade behavior."""

    def __init__(self):
        super().__init__()
        self.gates: list[QualityGate] = []
        self.evaluator: QualityGateEvaluator | None = None
        self.results: list[GateResult] = []

    @initialize()
    def init_cascade(self):
        self.evaluator = QualityGateEvaluator()
        # Initialize with standard gate cascade
        self.gates = [
            QualityGate(name="format", order=1, condition=lambda: True),
            QualityGate(name="lint", order=2, condition=lambda: True),
            QualityGate(name="coverage", order=3, condition=lambda: True),
            QualityGate(name="tests", order=4, condition=lambda: True),
        ]
        self.results = []

    @rule()
    def run_cascade(self):
        """Execute the full gate cascade."""
        self.results = self.evaluator.evaluate_cascade(self.gates)

    @rule()
    def fail_gate(self, gate_index: int = 0):
        """Make a specific gate fail."""
        if 0 <= gate_index < len(self.gates):
            self.gates[gate_index] = QualityGate(
                name=self.gates[gate_index].name,
                order=self.gates[gate_index].order,
                condition=lambda: False,
            )

    @rule()
    def restore_gate(self, gate_index: int = 0):
        """Restore a gate to passing."""
        if 0 <= gate_index < len(self.gates):
            self.gates[gate_index] = QualityGate(
                name=self.gates[gate_index].name,
                order=self.gates[gate_index].order,
                condition=lambda: True,
            )

    @invariant()
    def cascade_stops_on_failure(self):
        """Gates after a failure should not be evaluated."""
        if self.results:
            first_failure_idx = None
            for i, result in enumerate(self.results):
                if not result.passed:
                    first_failure_idx = i
                    break

            if first_failure_idx is not None:
                # No results after first failure should exist
                assert len(self.results) == first_failure_idx + 1

    @invariant()
    def gate_order_preserved(self):
        """Results should be in gate order."""
        if len(self.results) > 1:
            for i in range(1, len(self.results)):
                assert self.results[i].gate_order > self.results[i - 1].gate_order


TestQualityGateCascade = QualityGateCascadeStateMachine.TestCase
```

---

## Test Isolation Patterns

### Fixture Hierarchy

```python
# tests/conftest.py - Root level fixtures

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, AsyncMock


# === Session-scoped fixtures (one-time setup) ===

@pytest.fixture(scope="session")
def test_config():
    """Global test configuration."""
    return {
        "timeout_seconds": 30,
        "max_retries": 3,
        "coverage_threshold": 80,
    }


# === Module-scoped fixtures (per test module) ===

@pytest.fixture(scope="module")
def shared_workspace() -> Path:
    """Shared workspace for module-level tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = Path(tmpdir)
        (workspace / ".jerry").mkdir()
        (workspace / ".jerry" / "data").mkdir()
        (workspace / ".jerry" / "data" / "items").mkdir()
        yield workspace


# === Function-scoped fixtures (per test) ===

@pytest.fixture
def isolated_workspace() -> Path:
    """Isolated workspace for single test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = Path(tmpdir)
        (workspace / ".jerry").mkdir()
        (workspace / ".jerry" / "data").mkdir()
        (workspace / ".jerry" / "data" / "items").mkdir()
        yield workspace


@pytest.fixture
def mock_ports():
    """Bundle of mocked infrastructure ports."""
    class MockPorts:
        def __init__(self):
            self.code_generation = Mock()
            self.code_generation.generate_tests = AsyncMock(return_value="def test(): pass")
            self.code_generation.generate_code = AsyncMock(return_value="def impl(): pass")

            self.test_runner = Mock()
            self.test_runner.run_tests = AsyncMock(
                return_value=Mock(passed=0, failed=1, errors=0)
            )

            self.quality_gate = Mock()
            self.quality_gate.evaluate = AsyncMock(
                return_value=Mock(passed=True, details={})
            )

            self.work_item_repo = Mock()
            self.work_item_repo.save = AsyncMock()
            self.work_item_repo.get_by_id = AsyncMock()
            self.work_item_repo.list_all = AsyncMock(return_value=[])

    return MockPorts()


@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset any singletons between tests."""
    # Example: reset ID generator state
    from src.development.infrastructure.adapters.filesystem.snowflake_id_adapter import (
        SnowflakeIdAdapter,
    )
    SnowflakeIdAdapter._instance = None
    yield
```

```python
# tests/unit/conftest.py - Unit test specific fixtures

import pytest
from src.development.domain.entities.work_item import WorkItem
from src.development.domain.entities.quality_gate import QualityGate
from src.development.domain.value_objects.priority import Priority


@pytest.fixture
def sample_work_item() -> WorkItem:
    """Standard work item for unit tests."""
    return WorkItem.create(
        title="Unit Test Item",
        description="Created for unit testing",
        priority=Priority.MEDIUM,
    )


@pytest.fixture
def work_item_factory():
    """Factory for creating work items with custom attributes."""
    def create(
        title: str = "Test Item",
        description: str = "Test Description",
        priority: Priority = Priority.MEDIUM,
        **kwargs,
    ) -> WorkItem:
        return WorkItem.create(
            title=title,
            description=description,
            priority=priority,
            **kwargs,
        )
    return create


@pytest.fixture
def quality_gate_factory():
    """Factory for creating quality gates."""
    def create(
        name: str = "test_gate",
        order: int = 1,
        condition: callable = lambda: True,
        threshold: float | None = None,
    ) -> QualityGate:
        return QualityGate(
            name=name,
            order=order,
            condition=condition,
            threshold=threshold,
        )
    return create
```

```python
# tests/integration/conftest.py - Integration test specific fixtures

import pytest
from pathlib import Path
from src.development.infrastructure.adapters.persistence.filesystem_work_item_adapter import (
    FileSystemWorkItemAdapter,
)
from src.development.infrastructure.adapters.filesystem.filelock_adapter import (
    PyFileLockAdapter,
)


@pytest.fixture
def filesystem_adapter(isolated_workspace: Path) -> FileSystemWorkItemAdapter:
    """Real filesystem adapter for integration tests."""
    return FileSystemWorkItemAdapter(
        base_path=isolated_workspace / ".jerry" / "data" / "items"
    )


@pytest.fixture
def filelock_adapter(isolated_workspace: Path) -> PyFileLockAdapter:
    """Real file lock adapter for integration tests."""
    return PyFileLockAdapter(
        lock_dir=isolated_workspace / ".jerry" / "locks",
        timeout_seconds=5.0,
    )


@pytest.fixture
def real_pytest_runner():
    """Real pytest runner for integration tests."""
    from src.development.infrastructure.adapters.testing.pytest_runner_adapter import (
        PytestRunnerAdapter,
    )
    return PytestRunnerAdapter()
```

### Mock Strategy

| Component | Mock? | Rationale |
|-----------|-------|-----------|
| Domain entities | NO | Pure logic, no external dependencies |
| Domain services | NO | Pure logic, test directly |
| Application handlers | PARTIAL | Mock ports, test handler logic |
| Infrastructure adapters | YES (in unit tests) | Test adapter logic in isolation |
| External services (Claude) | YES | Expensive, non-deterministic |
| Filesystem | PARTIAL | Use tmpdir in integration, mock in unit |
| Time/Clock | YES | For deterministic tests |
| Random/ID generation | YES | For reproducibility |

---

## Mutation Testing Requirements

### Target Coverage

| Layer | Mutation Score Target | Rationale |
|-------|----------------------|-----------|
| Domain entities | >85% | Core business logic, high risk |
| Domain value objects | >90% | Immutable, critical invariants |
| Domain services | >80% | Complex logic, medium risk |
| Application handlers | >75% | Orchestration, lower risk |
| Infrastructure adapters | >60% | I/O logic, acceptable gaps |

### Configuration

```ini
# pyproject.toml

[tool.mutmut]
paths_to_mutate = "src/development/domain/"
tests_dir = "tests/unit/domain/"
runner = "python -m pytest"
use_coverage = true

[tool.mutmut.coverage]
fail_under = 80
```

### Exclusions

```python
# mutmut_config.py

def pre_mutation(context):
    """Configure mutation exclusions."""
    # Skip logging statements
    if context.current_source_token.strip().startswith("logger."):
        context.skip = True

    # Skip __repr__ and __str__ methods
    if context.current_function_name in ["__repr__", "__str__"]:
        context.skip = True

    # Skip type hints
    if ":" in context.current_source_token and "->" not in context.current_source_token:
        if context.current_source_token.strip().endswith(":"):
            pass  # Don't skip function signatures
        else:
            context.skip = True
```

### Mutation Testing Execution

```bash
# Run mutation testing on domain layer
mutmut run --paths-to-mutate=src/development/domain/ \
           --tests-dir=tests/unit/domain/

# Generate HTML report
mutmut html

# Check surviving mutants
mutmut results

# Run specific mutant
mutmut run --mutant=42
```

---

## Test Data Management

### Factories

```python
# tests/factories/__init__.py

from dataclasses import dataclass
from typing import Callable
from datetime import datetime, timezone
from src.development.domain.entities.work_item import WorkItem
from src.development.domain.value_objects.task_status import TaskStatus
from src.development.domain.value_objects.priority import Priority


@dataclass
class WorkItemFactory:
    """Factory for creating WorkItem test instances."""

    _counter: int = 0

    @classmethod
    def create(
        cls,
        title: str | None = None,
        description: str | None = None,
        status: TaskStatus = TaskStatus.BACKLOG,
        priority: Priority = Priority.MEDIUM,
        **overrides,
    ) -> WorkItem:
        cls._counter += 1
        item = WorkItem.create(
            title=title or f"Test Item {cls._counter}",
            description=description or f"Description for item {cls._counter}",
            priority=priority,
        )
        # Apply status if not default
        if status != TaskStatus.BACKLOG:
            item._set_status_for_test(status)
        # Apply any overrides
        for key, value in overrides.items():
            if hasattr(item, f"_{key}"):
                setattr(item, f"_{key}", value)
        return item

    @classmethod
    def create_ready(cls, **kwargs) -> WorkItem:
        return cls.create(status=TaskStatus.READY, **kwargs)

    @classmethod
    def create_in_progress(cls, **kwargs) -> WorkItem:
        return cls.create(status=TaskStatus.IN_PROGRESS, **kwargs)

    @classmethod
    def create_in_review(cls, **kwargs) -> WorkItem:
        return cls.create(status=TaskStatus.REVIEW, **kwargs)

    @classmethod
    def create_done(cls, **kwargs) -> WorkItem:
        return cls.create(status=TaskStatus.DONE, **kwargs)

    @classmethod
    def create_batch(cls, count: int, **kwargs) -> list[WorkItem]:
        return [cls.create(**kwargs) for _ in range(count)]


@dataclass
class QualityGateFactory:
    """Factory for creating QualityGate test instances."""

    @classmethod
    def create_passing(cls, name: str = "test_gate", order: int = 1):
        from src.development.domain.entities.quality_gate import QualityGate
        return QualityGate(name=name, order=order, condition=lambda: True)

    @classmethod
    def create_failing(cls, name: str = "test_gate", order: int = 1):
        from src.development.domain.entities.quality_gate import QualityGate
        return QualityGate(name=name, order=order, condition=lambda: False)

    @classmethod
    def create_cascade(cls, gate_configs: list[tuple[str, bool]]):
        """Create a cascade of gates with specified pass/fail status."""
        from src.development.domain.entities.quality_gate import QualityGate
        return [
            QualityGate(
                name=name,
                order=i + 1,
                condition=lambda passes=passes: passes,
            )
            for i, (name, passes) in enumerate(gate_configs)
        ]
```

### Golden Test Data

```yaml
# tests/fixtures/golden/work_items.yaml

valid_work_item_minimal:
  title: "Minimal valid item"
  description: ""

valid_work_item_full:
  title: "Full work item"
  description: "A complete work item with all fields"
  priority: HIGH
  acceptance_criteria:
    - "Given setup\nWhen action\nThen result"
  definition_of_done:
    - "Code complete"
    - "Tests passing"
    - "Documentation updated"

edge_case_max_title:
  title: "x" * 255  # Maximum length title
  description: "Edge case test"

edge_case_unicode_title:
  title: "Test with unicode: 日本語 and emojis"
  description: "Unicode handling test"
```

```python
# tests/fixtures/golden/__init__.py

import yaml
from pathlib import Path

GOLDEN_DIR = Path(__file__).parent


def load_golden(filename: str) -> dict:
    """Load golden test data from YAML file."""
    with open(GOLDEN_DIR / filename) as f:
        return yaml.safe_load(f)


def load_work_items() -> dict:
    return load_golden("work_items.yaml")


def load_acceptance_criteria() -> dict:
    return load_golden("acceptance_criteria.yaml")
```

---

## CI/CD Integration

### Test Stage Pipeline

```yaml
# .github/workflows/test.yaml

name: Test Suite

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e ".[test]"

      - name: Run unit tests
        run: |
          pytest tests/unit/ \
            --cov=src/development/domain \
            --cov-report=xml \
            --cov-fail-under=90 \
            -v --tb=short

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
          flags: unit

  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -e ".[test]"

      - name: Run integration tests
        run: |
          pytest tests/integration/ \
            --cov=src/development/application \
            --cov=src/development/infrastructure \
            --cov-report=xml \
            --cov-fail-under=80 \
            -v --tb=short

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
          flags: integration

  system-tests:
    runs-on: ubuntu-latest
    needs: integration-tests
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -e ".[test]"

      - name: Run BDD system tests
        run: |
          pytest tests/system/ \
            --bdd \
            -v --tb=short

  e2e-tests:
    runs-on: ubuntu-latest
    needs: system-tests
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -e ".[test]"

      - name: Run E2E tests
        run: |
          pytest tests/e2e/ \
            -v --tb=short \
            --timeout=120

  property-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -e ".[test]"

      - name: Run property-based tests
        run: |
          pytest tests/property/ \
            --hypothesis-show-statistics \
            --hypothesis-seed=12345 \
            -v

  mutation-tests:
    runs-on: ubuntu-latest
    needs: [unit-tests, property-tests]
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -e ".[test]"

      - name: Run mutation tests
        run: |
          mutmut run --paths-to-mutate=src/development/domain/ \
                     --tests-dir=tests/unit/domain/ \
                     --runner="pytest tests/unit/domain/" \
                     --CI

      - name: Check mutation score
        run: |
          mutmut results --score-only | grep -E "^[0-9]+" | \
            xargs -I {} sh -c '[ {} -ge 80 ] || exit 1'
```

### Parallelization Strategy

```yaml
# pytest.ini

[pytest]
addopts = -n auto --dist loadscope
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests requiring external resources
    e2e: marks end-to-end tests
    property: marks property-based tests

testpaths = tests
python_files = test_*.py
python_functions = test_*

# Parallelization configuration
# --dist loadscope: Group tests by module/class for fixture sharing
# -n auto: Use number of CPU cores for parallel execution
```

```python
# conftest.py - Parallelization support

import pytest


@pytest.fixture(scope="session")
def session_scoped_resource(tmp_path_factory):
    """Session-scoped resources are shared across parallel workers."""
    return tmp_path_factory.mktemp("shared")


@pytest.fixture(scope="function")
def worker_id(request):
    """Get pytest-xdist worker ID for parallel tests."""
    if hasattr(request.config, "workerinput"):
        return request.config.workerinput["workerid"]
    return "master"


def pytest_collection_modifyitems(config, items):
    """Group tests for optimal parallelization."""
    # Group slow tests together
    slow_tests = []
    fast_tests = []

    for item in items:
        if "slow" in item.keywords:
            slow_tests.append(item)
        else:
            fast_tests.append(item)

    # Reorder: fast tests first, then slow tests
    items[:] = fast_tests + slow_tests
```

---

## Quality Gates for Tests

### Code Review Checklist

```markdown
## Test Review Checklist

### Structure and Organization
- [ ] Tests follow naming convention: `test_{scenario}_when_{condition}_then_{expected}`
- [ ] Tests use AAA pattern (Arrange-Act-Assert) with comments
- [ ] Test file location matches source file location
- [ ] Related tests are grouped in classes

### Coverage and Completeness
- [ ] Happy path covered
- [ ] Edge cases covered (empty, null, max/min values)
- [ ] Error cases covered with appropriate assertions
- [ ] Boundary conditions tested

### Test Quality
- [ ] Tests are independent (no test order dependencies)
- [ ] Tests are deterministic (no random failures)
- [ ] Tests are fast (unit tests < 100ms each)
- [ ] Mocks are appropriate (not over-mocking)

### Assertions
- [ ] Assertions are specific (not just `assert True`)
- [ ] Error messages are descriptive
- [ ] Exception assertions include message checking
- [ ] State assertions check all relevant attributes

### Fixtures
- [ ] Fixtures are appropriately scoped
- [ ] Fixtures clean up resources
- [ ] Fixtures are reusable where appropriate
- [ ] Factory patterns used for complex objects

### Property-Based Testing
- [ ] Invariants identified and tested
- [ ] Strategies generate valid data
- [ ] Shrinking produces minimal examples
- [ ] State machines model real state transitions
```

### Metrics Thresholds

| Metric | Threshold | Enforcement |
|--------|-----------|-------------|
| Line coverage (domain) | >90% | CI gate (hard fail) |
| Line coverage (application) | >80% | CI gate (hard fail) |
| Line coverage (infrastructure) | >70% | CI gate (warning) |
| Branch coverage (domain) | >85% | CI gate (hard fail) |
| Mutation score (domain) | >80% | PR gate (soft fail) |
| Test execution time (unit) | <60s total | CI gate (warning) |
| Test execution time (integration) | <5m total | CI gate (warning) |
| Flaky test rate | <1% | PR gate (soft fail) |
| Property test examples | >100 | CI gate (warning) |

---

## Appendix: Test Directory Structure

```
tests/
├── conftest.py                     # Root fixtures
├── strategies/                     # Hypothesis strategies
│   ├── __init__.py
│   ├── domain_strategies.py
│   └── composite_strategies.py
├── factories/                      # Test data factories
│   ├── __init__.py
│   ├── work_item_factory.py
│   └── quality_gate_factory.py
├── fixtures/                       # Golden test data
│   ├── golden/
│   │   ├── work_items.yaml
│   │   └── acceptance_criteria.yaml
│   └── __init__.py
├── unit/                           # Unit tests
│   ├── conftest.py
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── test_work_item.py
│   │   │   ├── test_quality_gate.py
│   │   │   └── test_review_session.py
│   │   ├── value_objects/
│   │   │   ├── test_task_status.py
│   │   │   ├── test_acceptance_criterion.py
│   │   │   └── test_dependency_graph.py
│   │   └── services/
│   │       ├── test_task_decomposition.py
│   │       ├── test_quality_gate_evaluator.py
│   │       └── test_dependency_resolver.py
│   └── application/
│       └── handlers/
│           ├── test_work_item_handlers.py
│           └── test_generation_handlers.py
├── integration/                    # Integration tests
│   ├── conftest.py
│   ├── application/
│   │   └── handlers/
│   │       ├── test_generate_tests_handler.py
│   │       └── test_execute_quality_gate_handler.py
│   └── infrastructure/
│       └── adapters/
│           ├── test_filesystem_work_item_adapter.py
│           ├── test_filelock_adapter.py
│           └── test_pytest_runner_adapter.py
├── system/                         # BDD system tests
│   ├── conftest.py
│   ├── features/
│   │   ├── test_first_development.feature
│   │   ├── quality_gate_cascade.feature
│   │   └── tiered_review.feature
│   └── step_defs/
│       ├── conftest.py
│       ├── common_steps.py
│       ├── work_item_steps.py
│       ├── generation_steps.py
│       └── quality_steps.py
├── property/                       # Property-based tests
│   ├── conftest.py
│   ├── test_work_item_state_machine.py
│   ├── test_quality_gate_state_machine.py
│   └── test_dependency_graph_properties.py
└── e2e/                           # End-to-end tests
    ├── conftest.py
    ├── test_development_skill_invocation.py
    └── test_full_tdd_cycle.py
```

---

## Citations

1. Kent Beck, *Test-Driven Development: By Example*. Addison-Wesley, 2002.
2. Martin Fowler, "Test Pyramid." https://martinfowler.com/bliki/TestPyramid.html
3. Martin Fowler, "The Practical Test Pyramid." https://martinfowler.com/articles/practical-test-pyramid.html
4. pytest-bdd Documentation. https://github.com/pytest-dev/pytest-bdd
5. Hypothesis Documentation. https://hypothesis.readthedocs.io/en/latest/
6. pytest Fixtures. https://docs.pytest.org/en/latest/how-to/fixtures.html
7. Google Testing Blog. https://testing.googleblog.com/
8. mutmut Documentation. https://mutmut.readthedocs.io/
9. DZone, "Test-Driven Generation." https://dzone.com/articles/test-driven-generation

---

*Test strategy completed: 2026-01-09*
*Agent: ps-analyst (Testing)*
*Source documents: e-007 (synthesis), e-008 (architecture analysis), e-003 (BDD/TDD)*
*Test types covered: Unit, Integration, System (BDD), E2E, Property-based, Mutation*
