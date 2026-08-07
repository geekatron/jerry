# PROJ-032-nuclear-sop-review -- Work Tracker

> Review + remediation of the `/nuclear-sop` skill (PR #269). See `PLAN.md` for phases and `research/session-prompt.md` for the session entry point.

## Work Items

| ID | Type | Title | Status | Parent | GitHub |
|----|------|-------|--------|--------|--------|
| [EPIC-001](./work/EPIC-001-pr269-review/EPIC-001-pr269-review.md) | epic | PR #269 /nuclear-sop review & remediation | in_progress | — | — |
| [FEAT-002](./work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/FEAT-002-remediation-verdict.md) | feature | Remediation & verdict (Phases 4-5) | in_progress | EPIC-001 | — |
| [STORY-004](./work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/STORY-004-remediation.md) | story | Phase 4 — Remediation of Critical/Major findings | in_progress | FEAT-002 | [#348](https://github.com/geekatron/jerry/issues/348) |
| [STORY-005](./work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-005-verdict/STORY-005-verdict.md) | story | Phase 5 — Merge/rework/reject verdict | pending | FEAT-002 | [#349](https://github.com/geekatron/jerry/issues/349) |
| [BUG-001](./work/BUG-001-qg-hold-delegation-topology/BUG-001-qg-hold-delegation-topology.md) | bug | [REM-01] QG-HOLD and mid-procedure delegation topology (critical, DEFER-REWORK) | pending | STORY-004 | [#350](https://github.com/geekatron/jerry/issues/350) |
| [BUG-002](./work/BUG-002-user-hold-runtime-model/BUG-002-user-hold-runtime-model.md) | bug | [REM-02] USER-HOLD mechanism and runtime execution model (critical, DEFER-REWORK) | pending | STORY-004 | [#351](https://github.com/geekatron/jerry/issues/351) |
| [BUG-003](./work/BUG-003-trust-boundary-state-tamper/BUG-003-trust-boundary-state-tamper.md) | bug | [REM-03] Trust-boundary integrity and state tamper protection (critical, DEFER-REWORK) | pending | STORY-004 | [#352](https://github.com/geekatron/jerry/issues/352) |
| [BUG-004](./work/BUG-004-qg-e4-validation-evidence/BUG-004-qg-e4-validation-evidence.md) | bug | [REM-04] QG-E4 validation evidence (critical, DEFER-REWORK) | pending | STORY-004 | [#353](https://github.com/geekatron/jerry/issues/353) |
| [BUG-005](./work/BUG-005-h36-governance-ruling/BUG-005-h36-governance-ruling.md) | bug | [REM-05] H-36 governance ruling (critical, DEFER-REWORK) | pending | STORY-004 | [#354](https://github.com/geekatron/jerry/issues/354) |
| [BUG-006](./work/BUG-006-oe-feedback-loop-design/BUG-006-oe-feedback-loop-design.md) | bug | [REM-06] OE feedback-loop design (major, DEFER-REWORK) | pending | STORY-004 | [#355](https://github.com/geekatron/jerry/issues/355) |
| [BUG-007](./work/BUG-007-executor-command-gating/BUG-007-executor-command-gating.md) | bug | [REM-07] Executor command gating and injection screening (major, DEFER-REWORK) | pending | STORY-004 | [#356](https://github.com/geekatron/jerry/issues/356) |
| [BUG-008](./work/BUG-008-registration-status-truth/BUG-008-registration-status-truth.md) | bug | [REM-08] Registration and status truth reconciliation (critical, FIX-NOW) | in_progress | STORY-004 | [#357](https://github.com/geekatron/jerry/issues/357) |
| [BUG-009](./work/BUG-009-registration-enforcement-surfaces/BUG-009-registration-enforcement-surfaces.md) | bug | [REM-09] Registration enforcement surfaces (critical, FIX-NOW) | in_progress | STORY-004 | [#358](https://github.com/geekatron/jerry/issues/358) |
| [BUG-010](./work/BUG-010-agent-schema-conformance/BUG-010-agent-schema-conformance.md) | bug | [REM-10] Agent definition schema and standards conformance (critical, FIX-NOW) | in_progress | STORY-004 | [#359](https://github.com/geekatron/jerry/issues/359) |
| [BUG-011](./work/BUG-011-oe-artifact-contract/BUG-011-oe-artifact-contract.md) | bug | [REM-11] OE artifact contract alignment (critical, FIX-NOW) | in_progress | STORY-004 | [#360](https://github.com/geekatron/jerry/issues/360) |
| [BUG-012](./work/BUG-012-state-machine-contract/BUG-012-state-machine-contract.md) | bug | [REM-12] State machine and completion contract reconciliation (critical, FIX-NOW) | in_progress | STORY-004 | [#361](https://github.com/geekatron/jerry/issues/361) |
| [BUG-013](./work/BUG-013-composition-drift/BUG-013-composition-drift.md) | bug | [REM-13] Composition drift resynchronization (critical, FIX-NOW) | in_progress | STORY-004 | [#362](https://github.com/geekatron/jerry/issues/362) |
| [BUG-014](./work/BUG-014-navigation-tables/BUG-014-navigation-tables.md) | bug | [REM-14] Navigation tables (critical, FIX-NOW) | in_progress | STORY-004 | [#363](https://github.com/geekatron/jerry/issues/363) |

## Completed

| ID | Type | Title | Parent | Completed |
|----|------|-------|--------|-----------|
| [STORY-001](./work/EPIC-001-pr269-review/FEAT-001-independent-review/STORY-001-standards-compliance/STORY-001-standards-compliance.md) | story | Phase 1 — Standards compliance validation (32 findings: 6C/15M/11m) | FEAT-001 | 2026-08-07 |
| [STORY-002](./work/EPIC-001-pr269-review/FEAT-001-independent-review/STORY-002-engineering-review/STORY-002-engineering-review.md) | story | Phase 2 — Engineering review (30 findings: 4C/16M/10m, NO-GO) | FEAT-001 | 2026-08-07 |
| [STORY-003](./work/EPIC-001-pr269-review/FEAT-001-independent-review/STORY-003-c4-tournament/STORY-003-c4-tournament.md) | story | Phase 3 — C4 tournament (89 findings, 33C; S-014 0.52 REJECTED vs claimed 0.943) | FEAT-001 | 2026-08-07 |
| [FEAT-001](./work/EPIC-001-pr269-review/FEAT-001-independent-review/FEAT-001-independent-review.md) | feature | Independent review (Phases 1-3) | EPIC-001 | 2026-08-07 |
