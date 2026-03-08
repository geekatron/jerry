# PROJ-036: Prompt Regression Harness — Plan

## Document Sections

| Section | Purpose |
|---------|---------|
| [Objective](#objective) | What this project delivers |
| [Approach](#approach) | Implementation strategy |
| [Status](#status) | Current state |

---

## Objective

Implement the Four-Layer Composite Test Harness for prompt regression detection across Jerry's agent definitions. Layers: promptfoo CI/CD (L1), DeepEval G-Eval (L2), Metamorphic Relations (L3), Statistical Comparison Engine (L4).

## Approach

8-group orchestration pipeline (harness-impl-20260306-001) with 14 parallel streams, 5 quality gates, and dual final gate (adversarial + NASA SE review). See `orchestration/harness-impl-20260306-001/ORCHESTRATION_PLAN.md`.

## Status

- **Phase:** Implementation complete, RFA remediation pending
- **Quality:** All 14 streams passed >= 0.94 S-014 weighted composite
- **Human Review:** Victor Lau affirmed QG-4B (2026-03-07)
- **Blockers:** RFA-001 (input sanitization), RFA-002 (Docker SHA pinning)
