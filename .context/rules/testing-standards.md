---
paths:
  - "src/**/*.py"
  - "tests/**/*.py"
  - "scripts/**/*.py"
  - ".context/patterns/**/*.py"
  - "hooks/**/*.py"
---

# Testing Standards

> Test pyramid, BDD cycle, coverage, and tool configuration for Jerry.

<!-- L2-REINJECT: rank=5, content="Testing standards REQUIRED (H-20): (a) BDD Red phase — NEVER write implementation before test fails, (b) 90% line coverage REQUIRED." -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [HARD Rules](#hard-rules) | Testing constraints H-20, H-21 |
| [Standards (MEDIUM)](#standards-medium) | Test structure, naming, mocking, tools |
| [Compaction Testing (PG-004)](#compaction-testing-pg-004) | Compaction survival testing for constraint-bearing artifacts |
| [Guidance (SOFT)](#guidance-soft) | Optional practices |

---

## HARD Rules

> These rules CANNOT be overridden. Violations will be blocked.

| ID | Rule | Consequence |
|----|------|-------------|
| H-20 | NEVER write implementation before the test fails (BDD Red phase). | Untested code flagged. |
| H-21 | Test suite MUST maintain >= 90% line coverage. | CI blocks merge. |

---

## Standards (MEDIUM)

Override requires documented justification.

### Test Pyramid Distribution

| Category | Target % | Focus |
|----------|----------|-------|
| Unit | 60% | Domain logic, value objects, aggregates |
| Integration | 15% | Adapter implementations, port contracts |
| Contract + Architecture | 10% | Interface compliance, layer boundaries |
| System | 10% | Component interaction |
| E2E | 5% | Full workflow validation |

### BDD Red/Green/Refactor

1. **RED:** Write a failing test first.
2. **GREEN:** Write minimal code to make it pass.
3. **REFACTOR:** Improve without changing behavior. Tests SHOULD still pass.

### Test Naming and Structure

- Format RECOMMENDED: `test_{scenario}_when_{condition}_then_{expected}`.
- AAA pattern RECOMMENDED: Arrange, Act, Assert -- clearly separated.
- Scenario distribution: 60% happy path, 30% negative cases, 10% edge cases.

### Test File Location

| Type | Location |
|------|----------|
| Unit | `tests/unit/{layer}/test_{module}.py` |
| Integration | `tests/integration/test_{adapter}.py` |
| E2E | `tests/e2e/test_{workflow}.py` |
| Contract | `tests/contract/test_{contract}.py` |
| Architecture | `tests/architecture/test_{concern}.py` |

### Coverage Configuration

- Branch coverage SHOULD be >= 85%.
- Exclusions RECOMMENDED: `__init__.py`, abstract base classes, `TYPE_CHECKING` blocks.

### Mocking Guidelines

- Mock external services, time, random, and expensive operations.
- NEVER mock domain objects, value objects, or pure functions.
- Use in-memory implementations for port testing.

### Tool Configuration

**pytest:** `uv run pytest` with markers: `unit`, `integration`, `e2e`, `architecture`.
**mypy:** Strict mode. `disallow_untyped_defs = true`. Override for `tests/` and `scripts/`.
**ruff:** `target-version = "py311"`, `line-length = 100`. Select: E, W, F, I, B, C4, UP, ARG, SIM, TCH, PTH, ERA, PL, RUF.

---

## Compaction Testing (PG-004)

> MEDIUM standard. Override requires documented justification.

Constraint-bearing artifacts SHOULD be tested for context compaction survival. When a compaction event occurs (AE-006e), the LLM context is summarized and prior content is discarded. Constraints embedded only in L1 (session-start) content are vulnerable to loss.

### Artifact Types Requiring Compaction Testing

| Artifact Type | Compaction Risk | Test Priority |
|--------------|----------------|---------------|
| Rule files with L2-REINJECT markers | Low (L2 re-injection survives compaction) | Verify L2 markers cover critical constraints |
| Rule files without L2-REINJECT markers | High (L1-only, lost on compaction) | Verify Tier B compensating controls exist |
| SKILL.md files | Medium (Tier 1 metadata reloaded; methodology lost) | Verify trigger keywords survive in routing layer |
| Agent definitions (.md + .governance.yaml) | Medium (reloaded on Task invocation) | Verify schema validation gates are deterministic (L3/L5) |
| Templates (.context/templates/) | High (loaded on-demand, not re-injected) | Verify template constraints have external enforcement |

### Test Structure

Compaction tests follow a three-step structure:

1. **Load:** Identify the critical constraints in the artifact (HARD rules, invariants, containment rules, state machine constraints).
2. **Simulate:** Assume compaction has occurred -- only L2-REINJECT content, deterministic gates (L3/L5), and compensating controls remain.
3. **Verify:** Confirm that each critical constraint has at least one compaction-resilient enforcement mechanism (L2 marker, L3 pre-tool gate, L5 CI check, or skill/hook enforcement).

### C3+ Quality Gate Integration

For C3+ deliverables that modify constraint-bearing artifacts:

- [ ] Each HARD rule in the artifact has at least one compaction-resilient enforcement mechanism
- [ ] L2-REINJECT markers cover the artifact's highest-priority constraints
- [ ] Tier B rules (no L2 marker) have documented compensating controls
- [ ] Template constraints have failure mode documentation (T-004)

---

## Guidance (SOFT)

*Optional best practices.*

- *Property-based testing MAY be used for edge case coverage.*
- *Pre-commit hooks SUGGESTED for local development (ruff, mypy).*
- *`pytest-cov` MAY be used for HTML coverage reports.*

See `quality-enforcement.md` for quality gate threshold (H-13, >= 0.92) and criticality levels (C1-C4).
