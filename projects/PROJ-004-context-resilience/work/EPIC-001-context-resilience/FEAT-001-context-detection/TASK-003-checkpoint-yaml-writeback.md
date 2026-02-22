# TASK-003: Checkpoint Write-Back to ORCHESTRATION.yaml

> **Type:** task
> **Status:** completed
> **Priority:** medium
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** 2026-02-21
> **Parent:** EN-008
> **Owner:** --
> **Effort:** 2h

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description |
| [Description](#description) | What needs to be done |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical guidance |
| [Related Items](#related-items) | Links |
| [History](#history) | Status changes |

---

## Summary

Add checkpoint write-back step to ORCHESTRATION.yaml resumption section after checkpoint creation. Completed as part of parent enabler EN-008.

---

## Description

**Addresses:** AC-4 (PARTIAL)

AC-4 specifies: "Checkpoint writes to ORCHESTRATION.yaml resumption section." Currently, `CheckpointService` reads ORCHESTRATION.yaml content into the checkpoint's `resumption_state` dict but does not write back an updated resumption section. State flows via the checkpoint file (`.jerry/checkpoints/cx-NNN.json`) to new sessions through `FilesystemCheckpointRepository` + `ResumptionContextGenerator`, not via ORCHESTRATION.yaml mutation.

Add a write-back step in `CheckpointService.create_checkpoint()` that updates the ORCHESTRATION.yaml `resumption` section with the latest checkpoint ID, fill percentage, tier, and timestamp.

---

## Acceptance Criteria

- [ ] `CheckpointService.create_checkpoint()` writes back to ORCHESTRATION.yaml after creating checkpoint
- [ ] Write-back updates `resumption.latest_checkpoint_id`, `resumption.fill_percentage`, `resumption.tier`, `resumption.checkpoint_timestamp`
- [ ] Uses `yaml.safe_load()` + `yaml.safe_dump()` to parse and write YAML (preserves structure)
- [ ] Fail-open: if ORCHESTRATION.yaml not found or write fails, checkpoint still succeeds
- [ ] Write uses atomic file write pattern (consistent with AtomicFileAdapter)
- [ ] Unit tests for write-back (happy path + file not found + write failure fallback)
- [ ] Existing 229 hook tests still pass

---

## Implementation Notes

**Key file:** `src/context_monitoring/application/services/checkpoint_service.py`

The write-back should happen after the checkpoint file is successfully written to `.jerry/checkpoints/`. This ensures the ORCHESTRATION.yaml resumption section always points to a valid checkpoint file. The write should be fail-open since ORCHESTRATION.yaml is not always present (e.g., non-orchestrated workflows).

Consider using the existing `AtomicFileAdapter` for atomic writes to prevent corruption if the process is interrupted during write.

---

## Related Items

- Parent: [EN-008](./EN-008-context-resilience-hardening.md)
- Validation Report: AC-4 (PARTIAL)
- Related: TASK-001 (structured field extraction from same file)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-20 | pending | Created from ST-003 validation AC-4 (PARTIAL). |
