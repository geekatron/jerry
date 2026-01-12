# WI-018: Integration & E2E Tests

| Field | Value |
|-------|-------|
| **ID** | WI-018 |
| **Title** | Integration & E2E Tests |
| **Type** | Task |
| **Status** | PENDING |
| **Priority** | HIGH |
| **Phase** | PHASE-06 |
| **Assignee** | WT-Test |
| **Created** | 2026-01-12 |
| **Completed** | - |

---

## Description

Implement integration and end-to-end tests for the configuration system: file locking under concurrent access, atomic writes with crash simulation, CLI command workflows, and hook output format contracts.

---

## Acceptance Criteria

- [ ] AC-018.1: Integration tests for concurrent file access
- [ ] AC-018.2: Integration tests for atomic write reliability
- [ ] AC-018.3: E2E tests for CLI commands (`jerry config show/get/set/path`)
- [ ] AC-018.4: Contract tests for hook output format
- [ ] AC-018.5: 90%+ coverage for configuration module
- [ ] AC-018.6: All tests pass in CI

---

## Sub-tasks

- [ ] ST-018.1: Create `tests/integration/test_atomic_file_adapter.py`
- [ ] ST-018.2: Create `tests/integration/test_layered_config.py`
- [ ] ST-018.3: Create `tests/e2e/test_config_cli.py`
- [ ] ST-018.4: Create `tests/contract/test_session_hook.py`
- [ ] ST-018.5: Verify coverage threshold met
- [ ] ST-018.6: Add to CI pipeline

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-018.1 | - | - |
| AC-018.2 | - | - |
| AC-018.3 | - | - |
| AC-018.4 | - | - |
| AC-018.5 | - | - |
| AC-018.6 | - | - |

---

## Implementation Notes

### Integration Tests: Concurrent Access

```python
# tests/integration/test_atomic_file_adapter.py
import multiprocessing
from pathlib import Path
import tempfile

from src.infrastructure.adapters.persistence.atomic_file_adapter import AtomicFileAdapter


class TestConcurrentAccess:
    """Test file locking under concurrent access."""

    def test_concurrent_writes_dont_corrupt(self, tmp_path: Path):
        """Multiple processes writing should not corrupt file."""
        target_file = tmp_path / "test.txt"
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")

        def write_task(process_id: int, iterations: int):
            for i in range(iterations):
                content = f"Process {process_id}, iteration {i}\n"
                adapter.write_atomic(target_file, content)

        # Spawn multiple processes
        processes = [
            multiprocessing.Process(target=write_task, args=(p, 100))
            for p in range(4)
        ]

        for p in processes:
            p.start()
        for p in processes:
            p.join()

        # File should be valid (one complete line, no corruption)
        content = target_file.read_text()
        assert content.startswith("Process ")
        assert content.strip().endswith(", iteration")  # Format check
```

### E2E Tests: CLI Commands

```python
# tests/e2e/test_config_cli.py
import subprocess


class TestConfigCLI:
    """End-to-end tests for jerry config commands."""

    def test_config_show_outputs_table(self):
        """jerry config show displays configuration table."""
        result = subprocess.run(
            ["jerry", "config", "show"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Key" in result.stdout
        assert "Value" in result.stdout

    def test_config_show_json_is_valid(self):
        """jerry config show --json outputs valid JSON."""
        result = subprocess.run(
            ["jerry", "config", "show", "--json"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        import json
        data = json.loads(result.stdout)
        assert isinstance(data, dict)

    def test_config_get_returns_value(self, monkeypatch):
        """jerry config get <key> returns value."""
        monkeypatch.setenv("JERRY_LOGGING__LEVEL", "DEBUG")

        result = subprocess.run(
            ["jerry", "config", "get", "logging.level"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "DEBUG" in result.stdout
```

### Contract Tests: Hook Output

```python
# tests/contract/test_session_hook.py
import subprocess


class TestSessionHookContract:
    """Verify session hook output format matches contract."""

    def test_hook_outputs_project_context_tag(self, monkeypatch):
        """Hook with valid project outputs <project-context>."""
        monkeypatch.setenv("JERRY_PROJECT", "PROJ-004-jerry-config")

        result = subprocess.run(
            ["python", "scripts/session_start.py"],
            capture_output=True,
            text=True,
        )
        assert "<project-context>" in result.stdout

    def test_hook_outputs_project_required_tag(self, monkeypatch):
        """Hook without project outputs <project-required>."""
        monkeypatch.delenv("JERRY_PROJECT", raising=False)

        result = subprocess.run(
            ["python", "scripts/session_start.py"],
            capture_output=True,
            text=True,
        )
        assert "<project-required>" in result.stdout
```

---

## Progress Log

| Timestamp | Update | Actor |
|-----------|--------|-------|
| 2026-01-12T11:00:00Z | Work item created | Claude |

---

## Dependencies

| Type | Work Item | Relationship |
|------|-----------|--------------|
| Depends On | WI-016 | CLI commands must be implemented |
| Depends On | WI-017 | Architecture tests should pass first |
| Blocks | - | Final validation |

---

## Related Artifacts

- **Testing Standards**: `.claude/rules/testing-standards.md`
- **Contract Tests Spec**: `tests/contract/README.md`
