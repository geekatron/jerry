# EN-001: DDD scaffolding for transcript/validation operation

> **Type:** enabler
> **Enabler Type:** architecture
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** FEAT-003
> **Owner:** adam.nowak
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this Enabler delivers |
| [Technical Approach](#technical-approach) | DDD module layout under /transcript BC |
| [Design Decisions to Capture](#design-decisions-to-capture) | ADRs to author during this enabler |
| [Agent Assignment](#agent-assignment) | Specific skill+agent mappings |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Change log |

---

## Summary

Author the empty module skeleton for `transcript/validation/` operation following hexagonal architecture (H-07): domain, application, infrastructure, interface layers. Define ports (RuleEngine, ReportRenderer, SubprocessSandbox), entity skeletons (Packet, ValidationRule, ValidationResult), and a single composition root entrypoint. No business logic in this Enabler — only the scaffolding so STORY-003 through STORY-006 can land rule implementations against stable interfaces.

This Enabler also captures architectural decisions as ADRs in this project's decisions folder, traceable from STORY-003..006 acceptance.

---

## Technical Approach

```
src/jerry/transcript/validation/
├── __init__.py                    # Public API surface
├── domain/                        # Pure domain — no infra/interface imports
│   ├── __init__.py
│   ├── packet.py                  # Packet aggregate (entity)
│   ├── rule.py                    # ValidationRule (entity), RuleId (VO)
│   ├── result.py                  # ValidationResult (entity), Severity (VO)
│   └── exceptions.py              # DomainError hierarchy
├── application/                   # Use cases / services — depends only on domain + ports
│   ├── __init__.py
│   ├── ports.py                   # RuleEngine, ReportRenderer, SubprocessSandbox protocols
│   ├── packet_validator.py        # PacketValidator service (orchestrates rule execution)
│   └── update_anchors.py          # UpdateAnchorsService (writes back declared = walked truth)
├── infrastructure/                # Adapters — depends on application ports + external libs
│   ├── __init__.py
│   ├── filesystem_packet_loader.py    # FileReader adapter
│   ├── subprocess_sandbox.py          # SubprocessSandbox adapter (security boundary)
│   ├── jsonschema_engine.py           # JSON Schema rule engine adapter
│   └── markdown_report_renderer.py    # ReportRenderer adapter
└── interface/                     # Composition root — depends on infra + application
    ├── __init__.py
    └── cli.py                     # CLI commands: verify, update-anchors

skills/transcript/scripts/
└── validate_packet.py             # Thin CLI shim (entrypoint) importing from src/jerry/transcript/validation/

tests/transcript/validation/
├── unit/                          # Pure domain + application tests (no infra)
├── integration/                   # Adapter tests with real filesystem and subprocess
└── golden/                        # Parameterized over test_data/ packets
```

H-07 isolation: domain layer has zero imports from application, infrastructure, or interface. Application layer depends only on domain + own ports. Interface is the only composition root.

---

## Design Decisions to Capture

| Decision | Captured As |
|----------|------------|
| Why validation is an operation within `/transcript` BC, not a separate BC | DEC-001 (this project) |
| Why hexagonal with 4 layers (vs 3-layer Clean) | DEC-002 |
| Why SubprocessSandbox is a separate port from RuleEngine | DEC-003 |
| How the gist's procedural shape maps to the DDD layout (gist as reference, not literal port) | DEC-004 |
| Where validators live: src/jerry/ vs skills/transcript/scripts/ | DEC-005 |

---

## Agent Assignment

| Step | Skill | Agent | Purpose |
|------|-------|-------|---------|
| 1 | `/problem-solving` | `ps-architect` | Author DEC-001..DEC-005 ADRs (validation as operation within /transcript BC; hexagonal 4-layer; SubprocessSandbox port; gist as reference; src/jerry vs skills/scripts placement) |
| 2 | `/eng-team` | `eng-architect` | Threat-informed architecture review on the DDD layout + DEC-001..005; produces architecture compliance memo |
| 3 | `/eng-team` | `eng-lead` | Implementation plan + dependency governance (which deps go in pyproject.toml; which are dev-only) |
| 4 | `/eng-team` | `eng-backend` | Create empty module skeleton (4 layers + `__init__.py` files); declare entity stubs and Protocol classes |
| 5 | `/eng-team` | `eng-qa` | Author scaffolding unit test (verifies import paths and H-07 isolation) |
| 6 | `/adversary` | `adv-executor` + `adv-scorer` | C4 ≥0.95 review on architecture (DEC-001..005 + module skeleton) |
| 7 | `/worktracker` | `wt-verifier` | Validate AC; close |

---

## Acceptance Criteria

- [ ] Empty module skeleton exists at `src/jerry/transcript/validation/` with the layout above.
- [ ] All `__init__.py` files declare the public API surface for their layer.
- [ ] Domain entities have type stubs (no business logic) — `Packet`, `ValidationRule`, `ValidationResult`, `RuleId`, `Severity`.
- [ ] Application ports (Protocol classes) declared: `RuleEngine`, `ReportRenderer`, `SubprocessSandbox`.
- [ ] H-07 verification: `grep -E '^from (jerry\.transcript\.validation\.(application|infrastructure|interface))' src/jerry/transcript/validation/domain/` returns zero matches.
- [ ] DEC-001 through DEC-005 ADRs authored under `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/plans/decisions/`.
- [ ] Unit test scaffolding exists at `tests/transcript/validation/unit/` with at least one passing trivial test (verifies import paths).
- [ ] `/eng-team` `eng-architect` ADR review on DEC-001 through DEC-005.
- [ ] `/adversary` C4 ≥0.95 on the architectural design (DEC-001..005 + module skeleton).

---

## Children Tasks

| ID | Title | Owner | Status |
|----|-------|-------|--------|
| [TASK-050](./TASK-050-author-decisions-001-through-005.md) | Author DEC-001..DEC-005 ADRs | `ps-architect` | pending |
| [TASK-051](./TASK-051-threat-informed-architecture-review.md) | Threat-informed architecture review on DDD layout + DEC-001..005 | `eng-architect` | pending |
| [TASK-052](./TASK-052-implementation-plan-and-dependency-governance.md) | Implementation plan + dependency governance | `eng-lead` | pending |
| [TASK-053](./TASK-053-create-empty-module-skeleton.md) | Create empty module skeleton (4 layers + __init__.py files) | `eng-backend` | pending |
| [TASK-054](./TASK-054-declare-domain-entities-and-ports.md) | Declare domain entity stubs and application port Protocol classes | `eng-backend` | pending |
| [TASK-055](./TASK-055-scaffolding-unit-test.md) | Author scaffolding unit test (verifies import paths) | `eng-qa` | pending |
| [TASK-056](./TASK-056-run-adversary-c4-on-architecture.md) | Run /adversary C4 review on architecture (DEC-001..005 + skeleton) | `adv-executor` | pending |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-003](../FEAT-003-deterministic-validation.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocks | STORY-003..STORY-006 | Rule implementations need stable interfaces |
| Blocks | EN-002, EN-003 | Test harness and subprocess sandbox plug into this scaffolding |
| Blocked By | EN-004 | Threat model on subprocess surface informs SubprocessSandbox port shape |

### Source

- [#273 §C5](https://github.com/geekatron/jerry/issues/273)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Enabler created. DDD layout captured. |
