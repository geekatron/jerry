# SPIKE-002: Jerry CLI Integration Architecture for Context Resilience

<!--
TEMPLATE: Spike
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.8
-->

> **Type:** spike
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-19
> **Completed:** 2026-02-19
> **Parent:** FEAT-001
> **Owner:** --
> **Effort:** 4

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Research question, hypothesis, scope |
| [Findings](#findings) | Summary and detailed findings (populated after research) |
| [Recommendation](#recommendation) | Decision and recommended actions (populated after research) |
| [Related Items](#related-items) | Hierarchy and related work |
| [History](#history) | Status changes |

---

## Content

### Research Question

**Question:** How should the context resilience system leverage the Jerry CLI's existing infrastructure — TokenCounter (tiktoken), session lifecycle (event-sourced start/end/abandon), layered config (TOML hierarchy), enforcement engines (L2 prompt reinforcement, session quality context), and local context persistence — instead of building parallel hook-only implementations? Which of SPIKE-001's 14 follow-up work items can REUSE existing CLI infrastructure, which need to EXTEND it, and which are genuinely NEW?

### Hypothesis

We hypothesize that:
1. The Jerry CLI's `TokenCounter` service (tiktoken-based) can replace the proposed transcript-based heuristic (SPIKE-001 Method A) with direct token counting, reducing estimation uncertainty
2. `jerry session abandon` already models the "context compaction" use case and can serve as the checkpoint trigger, extending the session aggregate with context metrics rather than building a standalone PreCompact hook
3. The layered config system (`jerry config`) can manage threshold configuration hierarchically (project/root/local scopes) instead of a standalone threshold config file
4. The SessionStart hook's existing `additionalContext` injection pathway and `session_quality_context_generator.py` can deliver resumption prompts without building a new Template 1 populator from scratch
5. The prompt reinforcement engine's L2-REINJECT mechanism (already parsing quality-enforcement.md) can deliver context alerts using the same marker-based priority system
6. At least 60% of SPIKE-001's 14 follow-up work items can be reclassified from NEW to REUSE or EXTEND

### Timebox

| Aspect | Value |
|--------|-------|
| Timebox Duration | 4 hours |
| Start Date | 2026-02-19 |
| Target End Date | 2026-02-19 |

**Warning:** Do not exceed the timebox. If more research is needed, create a follow-up spike.

### Scope

**In Scope:**
- Deep audit of Jerry CLI modules relevant to context resilience (TokenCounter, session aggregate, config adapter, enforcement engines, local context)
- Mapping each SPIKE-001 follow-up item against CLI capabilities (REUSE/EXTEND/NEW classification)
- Revised architecture design as ADR showing CLI-integrated approach
- Revised follow-up work items superseding SPIKE-001's 14 items
- Integration points between CLI domain layer and hook scripts

**Out of Scope:**
- Implementation of any context resilience features (FEAT-001 scope)
- Revisiting SPIKE-001 findings on thresholds, detection tiers, or resumption schema (those findings stand)
- Changes to the CLI's existing architecture or domain model design
- Performance benchmarking of CLI services

### Research Approach

1. **CLI Capability Audit** (ps-researcher): Deep inventory of CLI modules — TokenCounter, session aggregate/events, config adapter, enforcement engines, local context adapter. Map each to SPIKE-001 follow-up items.
2. **Gap Analysis** (ps-analyst): For each of SPIKE-001's 14 follow-up items, classify as REUSE (existing CLI capability), EXTEND (CLI capability needs enhancement), or NEW (no CLI analog). Identify integration architecture.
3. **Revised Architecture** (ps-architect): Create ADR for CLI-integrated context resilience. Design how detection, thresholds, checkpointing, and resumption integrate with the CLI's hexagonal architecture.
4. **Quality Gate** (adv-scorer): Adversarial quality review of the revised architecture ADR.
5. **Synthesis & Revised Work Items** (ps-synthesizer): Produce revised follow-up work items superseding SPIKE-001's 14, with CLI integration points specified.

---

## Findings

### Summary

The Jerry CLI has substantial reusable infrastructure for context resilience. SPIKE-002's 5-phase investigation (CLI Capability Audit, Gap Analysis, Architecture Design, Quality Gate, Synthesis) produced the following key findings:

1. **10 of 14 SPIKE-001 items reclassified from NEW to REUSE/EXTEND.** The Phase 1 CLI Capability Audit identified 7 directly applicable CLI capabilities across 8 categories (TokenCounter, session lifecycle, configuration management, enforcement engines, hook integration, local context persistence, domain event model, ECW status line). Only 3 items remain genuinely NEW (resumption schema, update protocol, calibration).

2. **14 SPIKE-001 items consolidated to 10 revised items (CWI-00 through CWI-09).** Four consolidations: Items #1+#3 (both extend UserPromptSubmit), Items #4+#5 (inseparable schema+protocol), Items #2+#10 (checkpoint directory is sub-task of PreCompact hook), Items #13+#14 (calibration docs accompany validation). One addition: CWI-00 (FileSystemSessionRepository) based on user feedback.

3. **The InMemorySessionRepository gap should be fixed, not worked around.** Phase 2 identified the `InMemorySessionRepository` as the single most significant architectural risk (R1, rated HIGH). The `FileSystemEventStore` + `EventSourcedWorkItemRepository` pattern (369 + 431 lines of production-tested code) already exists for work items. User feedback correctly identified that the same pattern should be applied to create a `FileSystemSessionRepository`, eliminating all file-based workarounds for cross-process session state.

4. **Estimated effort reduced by ~22-23% from SPIKE-001.** SPIKE-001: 14 items at 25-37 hours. SPIKE-002 Final: 10 items at 19.5-28.5 hours. Reduction sources: CLI infrastructure reuse, work item consolidation, and proven patterns reducing implementation risk.

5. **Two-phase architecture rejected; bounded context adopted (Phase 5 revision).** ADR-SPIKE002-001 originally proposed infrastructure placement (Alternative 2). User review identified fundamental flaws: (1) ADR chose wrong alternative using invalid reasoning, (2) enforcement folder is tech debt not a pattern, (3) hooks must call CLI not import modules. DISC-001 documented 3 architecture violations. DEC-001 captured 4 corrective decisions. ADR-SPIKE002-002 replaces ADR-SPIKE002-001 with Alternative 3: proper bounded context `src/context_monitoring/` with CLI-first hooks calling `jerry --json hooks <event>`. QG-2 passed at 0.92 after 2 iterations (C3 criticality, 7 strategies).

6. **12 revised work items replace original 10.** Phase 5c revised CWI-00 through CWI-09 for the bounded context architecture and added CWI-10 (`jerry hooks` CLI namespace) and CWI-11 (hook wrapper scripts). Estimated effort: 26-35.5 hours.

### Detailed Findings

**Finding 1: CLI Infrastructure is Directly Applicable (Phase 1 Audit)**

The Jerry CLI provides 7 capability categories directly relevant to context resilience:

| Category | Capability | Relevance |
|----------|-----------|-----------|
| C1: Token Counting | `TokenCounter` (tiktoken `p50k_base`) | Validation reference for Method A accuracy |
| C2: Session Lifecycle | Event-sourced `Session` aggregate with `abandon(reason)` | Domain model for compaction events |
| C3: Configuration | `LayeredConfigAdapter` (4-level precedence, TOML, CLI) | Direct replacement for threshold config file |
| C4: Enforcement Engines | `PromptReinforcementEngine`, `SessionQualityContextGenerator`, `PreToolEnforcementEngine` | Proven patterns for all 4 new engines |
| C5: Hook Integration | `hooks.json`, `UserPromptSubmit`, `SessionStart` hooks | Extension points for context monitoring |
| C6: File Persistence | `FileSystemEventStore`, `AtomicFileAdapter` | Checkpoint writing, session persistence |
| C7: Domain Events | `SessionAbandoned` with reason field | Designed for compaction scenario |

**Finding 2: Consolidation Eliminates Duplicate Work (Phase 2 Gap Analysis)**

| Original Items | Merged Into | Reason |
|----------------|-------------|--------|
| #1 + #3 | CWI-03 | Both modify `user-prompt-submit.py`, share injection pattern |
| #4 + #5 | CWI-04 | Schema without protocol is dead content; inseparable |
| #2 + #10 | CWI-02 | Checkpoint directory creation is one line in constructor |
| #13 + #14 | CWI-09 | Documentation is natural output of validation activity |

**Finding 3: FileSystemSessionRepository is the Key Enabler (User Feedback)**

The `InMemorySessionRepository` loses state on process termination (line 35: "Loses data on process termination"). Since each CLI invocation and each hook execution runs as a separate process, session state does not persist. The existing `EventSourcedWorkItemRepository` + `FileSystemEventStore` pattern proves that event-sourced persistence works:

- `FileSystemEventStore`: 369 lines, JSONL format, `FileLock` cross-process safety, `os.fsync` durability
- `EventSourcedWorkItemRepository`: 431 lines, event registry, stream ID convention, `load_from_history()` reconstitution
- `ISessionRepository` port: Already defines `get`, `get_active`, `save`, `exists` methods
- `Session.load_from_history()`: Already supports event replay (lines 284-324)

Creating `FileSystemSessionRepository` follows the exact pattern. Estimated effort: 3-4 hours.

**Finding 4: Architecture Revised to Bounded Context + CLI-First Hooks (Phase 5)**

- **Original (ADR-SPIKE002-001):** Infrastructure placement alongside enforcement engines. Rejected after user review — enforcement folder is tech debt, hooks importing Python modules violates process boundary.
- **Revised (ADR-SPIKE002-002):** Proper bounded context `src/context_monitoring/` with hexagonal architecture (domain value objects, application services + ports, infrastructure adapters). Hooks are thin wrappers (~10 lines) calling `jerry --json hooks <event>` via subprocess. All logic wired through `bootstrap.py` composition root.
- **Key domain concepts:** ThresholdTier, FillEstimate, CheckpointData, ContextState (value objects); ContextThresholdReached, CompactionDetected, CheckpointCreated (events); ContextFillEstimator, CheckpointService, ResumptionContextGenerator (application services).

**Finding 5: Both Quality Gates Passed**

- QG-1: ADR-SPIKE002-001 scored 0.94 (threshold: 0.92). 1 P2 defect (missing rollback strategy).
- QG-2: ADR-SPIKE002-002 scored 0.92 after 2 iterations (C3 criticality, 7 strategies). Iteration 1 scored 0.89 REVISE (3 required fixes: H-10 violation, undefined ResumptionContextGenerator, session-start wrapper inconsistency). All addressed in iteration 2.

### Evidence/References

| Artifact | Location |
|----------|----------|
| Phase 1: CLI Capability Audit | `orchestration/spike002-cli-integration-20260219-001/res/phase-1-audit/cli-auditor/cli-capability-audit.md` |
| Phase 2: Gap Analysis | `orchestration/spike002-cli-integration-20260219-001/res/phase-2-gap-analysis/gap-analyst/gap-analysis.md` |
| Phase 3: ADR-SPIKE002-001 | `orchestration/spike002-cli-integration-20260219-001/res/phase-3-architecture/architecture-designer/adr-cli-integration.md` |
| QG-1: Gate Result | `orchestration/spike002-cli-integration-20260219-001/res/quality-gates/qg-1/gate-result.md` |
| Phase 4: Revised Work Items (v1, superseded) | `orchestration/spike002-cli-integration-20260219-001/res/phase-4-synthesis/work-item-synthesizer/revised-work-items.md` |
| DISC-001: Architecture Violations | `work/EPIC-001-context-resilience/FEAT-001-context-detection/DISC-001-architecture-violations.md` |
| DEC-001: CLI-First Architecture Decisions | `work/EPIC-001-context-resilience/FEAT-001-context-detection/DEC-001-cli-first-architecture.md` |
| Phase 5a: ADR-SPIKE002-002 (revised ADR) | `orchestration/spike002-cli-integration-20260219-001/res/phase-5-revision/adr-reviser/adr-cli-integration-v2.md` |
| QG-2: Gate Result (iteration 1) | `orchestration/spike002-cli-integration-20260219-001/res/quality-gates/qg-2/gate-result.md` |
| QG-2: Gate Result (iteration 2, PASS) | `orchestration/spike002-cli-integration-20260219-001/res/quality-gates/qg-2/gate-result-iter2.md` |
| Phase 5c: Revised Work Items (v2, authoritative) | `orchestration/spike002-cli-integration-20260219-001/res/phase-5-revision/work-item-reviser/revised-work-items-v2.md` |
| FileSystemEventStore source | `src/work_tracking/infrastructure/persistence/filesystem_event_store.py` |
| EventSourcedWorkItemRepository source | `src/work_tracking/infrastructure/adapters/event_sourced_work_item_repository.py` |
| ISessionRepository port | `src/session_management/application/ports/session_repository.py` |
| InMemorySessionRepository source | `src/session_management/infrastructure/adapters/in_memory_session_repository.py` |
| Session aggregate source | `src/session_management/domain/aggregates/session.py` |
| Session events source | `src/session_management/domain/events/session_events.py` |

---

## Recommendation

### Decision

**Implement context resilience as a proper bounded context** (`src/context_monitoring/`) with CLI-first hooks, as defined in ADR-SPIKE002-002. Implement the revised 12-item work plan (CWI-00 through CWI-11) which supersedes the original 10 items. Prioritize CWI-00 (FileSystemSessionRepository) as the P0 foundation enabler.

### Recommended Actions

1. **Immediately: Accept DEC-001 decisions** (D-001 through D-004). Accept ADR-SPIKE002-002 (transition from PROPOSED to ACCEPTED).

2. **Phase A (Foundation):** Implement CWI-00 (FileSystemSessionRepository), CWI-01 (threshold config via ConfigThresholdAdapter), CWI-10 (`jerry hooks` CLI namespace), and CWI-11 (hook wrapper scripts) in parallel. These have no dependencies and unblock all subsequent work.

3. **Phase B (Bounded Context Core):** Implement CWI-02 (bounded context foundation: directory structure, value objects, events, CheckpointService, repository) then CWI-03 (ContextFillEstimator + ResumptionContextGenerator application services). This is the critical path.

4. **Phase C (Integration):** Implement CWI-04 (resumption schema), CWI-05 (AE-006 sub-rules), CWI-07 (PreToolUse staleness validation) -- partially parallelizable.

5. **Phase D (Validation):** Execute CWI-08 (OQ-9 + Method C investigation) and CWI-09 (threshold calibration) timeboxed activities.

### Follow-up Work Items

| ID | Title | Type | Priority | Effort |
|----|-------|------|----------|--------|
| CWI-00 | FileSystemSessionRepository | Enabler | P0 | 3-4 hrs |
| CWI-01 | ConfigThresholdAdapter + IThresholdConfiguration Port | Enabler | P1 | 1 hr |
| CWI-02 | Context Monitoring Bounded Context Foundation | Enabler | P1 | 4-6 hrs |
| CWI-03 | ContextFillEstimator + ResumptionContextGenerator Services | Enabler | P1 | 4-5 hrs |
| CWI-04 | Enhanced Resumption Schema + Update Protocol | Story | P1 | 2-3 hrs |
| CWI-05 | AE-006 Graduated Sub-Rules | Story | P2 | 1 hr |
| CWI-06 | (Superseded — merged into CWI-03) | -- | -- | -- |
| CWI-07 | PreToolUse Staleness Validation | Enabler | P3 | 2-3 hrs |
| CWI-08 | Validation Spikes (OQ-9 + Method C) | Spike | P2 | 3 hrs |
| CWI-09 | Threshold Validation + Calibration Documentation | Story | P3 | 4 hrs |
| CWI-10 | `jerry hooks` CLI Namespace Registration | Enabler | P1 | 1-1.5 hrs |
| CWI-11 | Hook Wrapper Scripts + hooks.json Registration | Enabler | P1 | 1-2 hrs |

**Total: 12 items (11 active + 1 superseded), 26-35.5 hours estimated effort.**

Full work item definitions with acceptance criteria and dependency graphs are in the Phase 5c synthesis: `orchestration/spike002-cli-integration-20260219-001/res/phase-5-revision/work-item-reviser/revised-work-items-v2.md`

### Risks/Considerations

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Hook import latency (R3):** Adding engine imports to `user-prompt-submit.py` increases execution time within 5000ms timeout | MEDIUM | Performance budget: 3000ms for all engines, 2000ms headroom. Measure empirically after CWI-03. Fail-open design ensures graceful degradation. |
| **FileSystemSessionRepository `get_active()` performance (OQ-10):** Must scan all session streams to find ACTIVE session | LOW | Sessions are infrequent (1 per CLI session). Index file or read model can be added if needed. |
| **Phase 2 extraction criteria may be vague (QG-1 D-003):** "domain concepts stable" and "boundaries validated" lack measurable definitions | LOW | Add measurable thresholds during FEAT-001 implementation (e.g., "no interface-breaking changes for 2 feature cycles"). |
| **AE-002 auto-escalation for CWI-05:** Touching `.context/rules/quality-enforcement.md` triggers auto-C3 minimum | EXPECTED | Correct governance behavior. Plan for C3 review process. |
| **ADR missing rollback strategy (QG-1 D-001):** No documented revert plan if implementation fails | LOW | Straightforward: remove engine imports from hooks, remove hook entries from hooks.json, delete engine files. Estimated rollback: <1 hour. Address before ADR acceptance. |

---

## Related Items

- Parent: [FEAT-001: Context Exhaustion Detection & Graceful Session Handoff](./FEAT-001-context-detection.md)
- Predecessor: [SPIKE-001: Research Context Measurement, Detection Thresholds & Resumption Protocols](./SPIKE-001-context-research.md) — SPIKE-002 addresses a gap in SPIKE-001: the Jerry CLI was not considered as an integration surface
- Related: Jerry CLI implementation at `src/interface/cli/`, `src/session_management/`, `src/infrastructure/internal/enforcement/`

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-19 | in_progress | Spike created to address SPIKE-001 gap: Jerry CLI infrastructure was not factored into context resilience design. SPIKE-001 focused entirely on hook scripts, missing existing CLI capabilities (TokenCounter, session lifecycle, config system, enforcement engines). |
| 2026-02-19 | completed | Phases 1-4 + QG-1 completed. CLI Capability Audit, Gap Analysis, ADR-SPIKE002-001 (QG-1 PASS at 0.94), initial work item synthesis (10 items CWI-00 through CWI-09). |
| 2026-02-19 | completed | User review identified ADR-SPIKE002-001 chose wrong alternative. DISC-001 documented 3 hook-CLI architecture violations. DEC-001 captured 4 corrective decisions (CLI-first hooks, proper bounded context, jerry hooks commands, enforcement debt tracking). |
| 2026-02-19 | completed | Phase 5 completed: (5a) ADR-SPIKE002-002 produced — chooses Alternative 3 (bounded context + CLI-first hooks), supersedes ADR-SPIKE002-001. (5b) QG-2 passed at 0.92 after 2 iterations (C3 criticality, 7 strategies). (5c) 12 revised work items (CWI-00 through CWI-11) aligned with bounded context architecture. Estimated effort: 26-35.5 hours. |
