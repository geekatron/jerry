# PS-ORCH-010: Checkpoint Restore Validation

> **Test ID:** PS-ORCH-010
> **Work Item:** WI-SAO-013
> **AC:** AC-013-005 (Checkpoint restore capability)
> **Pattern:** Restore from checkpoint
> **Status:** PLANNED

---

## Test Objective

Validate that checkpoint restore actually works - not just "structure valid" but actually restoring workflow state and resuming execution.

**Critical Gap Identified:**
- E2E tests created 8 checkpoints (CP-T001-A, CP-T002-FANOUT, etc.)
- All marked "Recovery Verified: Structure valid"
- NO actual restore was ever tested
- This is a HIGH severity gap (TD-013-004)

---

## Test Scenario

### Phase 1: Create Workflow with Checkpoint

1. Create ORCHESTRATION.yaml with:
   - 3-phase sequential workflow
   - Phase 1 COMPLETE with artifact
   - Phase 2 COMPLETE with artifact
   - Phase 3 PENDING
   - Checkpoint CP-TEST-001 after Phase 2

2. Create actual artifacts:
   - `phase-1/agent-1/agent-1-output.md`
   - `phase-2/agent-2/agent-2-output.md`

### Phase 2: Simulate Corruption/Failure

"Corrupt" the state by:
- Setting Phase 2 back to PENDING
- Setting agent-2 status to FAILED
- Updating metrics to show regression

### Phase 3: Execute Restore

Restore from CP-TEST-001:
1. Read checkpoint recovery_point
2. Reset workflow state to checkpoint state
3. Restore Phase 2 status to COMPLETE
4. Restore agent-2 status to COMPLETE
5. Verify artifact references are intact

### Phase 4: Validate Restored State

Verify:
- [ ] Phase 1 status: COMPLETE (preserved)
- [ ] Phase 2 status: COMPLETE (restored)
- [ ] Phase 3 status: PENDING (preserved)
- [ ] agent-2 artifact: EXISTS and matches original
- [ ] Metrics: Correctly reflect restored state
- [ ] Resumption context: Points to correct next step

---

## Success Criteria

1. Checkpoint contains sufficient state to restore
2. Restore operation correctly resets state
3. Artifacts referenced in checkpoint are accessible
4. Workflow can continue from restored state
5. No data loss during restore

---

## Expected Artifacts

```
PS-ORCH-010/
├── initial-state.yaml         # State before "corruption"
├── corrupted-state.yaml       # State after simulated failure
├── restored-state.yaml        # State after restore
├── phase-1/agent-1/agent-1-output.md
├── phase-2/agent-2/agent-2-output.md
└── EXECUTION-REPORT.md
```

---

## Protocol Definition

### Checkpoint Structure (from STATE_SCHEMA.md)

```yaml
checkpoints:
  latest_id: "CP-TEST-001"
  entries:
    - id: "CP-TEST-001"
      timestamp: "2026-01-12T20:00:00Z"
      trigger: "PHASE_COMPLETE"
      description: "Phase 2 complete"
      recovery_point: "phase-3-start"
      state_snapshot:
        phases_complete: 2
        phases_total: 3
        agent_statuses:
          agent-1: "COMPLETE"
          agent-2: "COMPLETE"
          agent-3: "PENDING"
```

### Restore Protocol

1. **Read checkpoint**: Load checkpoint entry by ID
2. **Validate artifacts**: Confirm referenced artifacts exist
3. **Restore state**:
   - Reset agent statuses to checkpoint values
   - Reset phase statuses based on agent states
   - Update metrics to reflect restored state
4. **Update resumption**: Set next_step to recovery_point
5. **Log restore**: Add restore event to issues.resolved

---

*Test Plan Version: 1.0*
*Created: 2026-01-12*
*Addresses: TD-013-004 (Restore never tested)*
