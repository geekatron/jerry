# TASK-004: Automated E2E Integration Test

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** --
> **Parent:** EN-008
> **Owner:** --
> **Effort:** 3h

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Description](#description) | What needs to be done |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical guidance |
| [Related Items](#related-items) | Links |
| [History](#history) | Status changes |

---

## Description

**Addresses:** DoD-7 (PASS empirical, not automated), NFC-1

DoD-7 specifies an end-to-end test for the exhaust-clear-resume-complete sequence. The PROJ-004 workflow itself (6 compaction events across 7 sessions) validates this path empirically, but no single automated test exercises the full pipeline in CI.

Create `tests/integration/test_context_exhaustion_e2e.py` that exercises the complete detection-checkpoint-resumption pipeline with mock JSONL transcript data.

---

## Acceptance Criteria

- [ ] `tests/integration/test_context_exhaustion_e2e.py` exists
- [ ] Test creates a mock JSONL transcript fixture with token counts near EMERGENCY threshold
- [ ] Test triggers `HooksPromptSubmitHandler` and verifies checkpoint is created
- [ ] Test simulates new session: triggers `HooksSessionStartHandler` and verifies resumption XML in `additionalContext`
- [ ] Test verifies `checkpoint_id` and `fill_percentage` are correctly round-tripped
- [ ] Test covers the full exhaust -> checkpoint -> resume sequence (no mocked services except file I/O)
- [ ] Test runs in CI (`uv run pytest tests/integration/`) with `@pytest.mark.integration` marker
- [ ] All existing 3652 tests still pass

---

## Implementation Notes

**Key file:** `tests/integration/test_context_exhaustion_e2e.py` (new)

Per REC-2 from the validation report:
1. Create a mock JSONL transcript fixture with token counts near EMERGENCY threshold (0.88+).
2. Trigger `HooksPromptSubmitHandler` with the fixture -- verify checkpoint created via `FilesystemCheckpointRepository`.
3. Simulate new session: trigger `HooksSessionStartHandler` -- verify `ResumptionContextGenerator` XML appears in `additionalContext`.
4. Verify `checkpoint_id` and `fill_percentage` are correctly round-tripped through the checkpoint file.

Use `tmp_path` fixture for temporary `.jerry/checkpoints/` directory. Wire dependencies through `create_hooks_handlers()` from `bootstrap.py` or manually construct with test doubles for file paths.

---

## Related Items

- Parent: [EN-008](./EN-008-context-resilience-hardening.md)
- Validation Report: REC-2, DoD-7 (PASS empirical)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-20 | pending | Created from ST-003 validation REC-2. |
