# SPIKE-002: Jerry CLI Integration Architecture for Context Resilience

<!--
TEMPLATE: Spike
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.8
-->

> **Type:** spike
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-19
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

5. **Two-phase architecture validated at QG-1 (score 0.94).** ADR-SPIKE002-001 proposes Phase 1 (infrastructure placement alongside existing enforcement engines) and Phase 2 (bounded context extraction when domain stabilizes). The ADR passed quality gate review with scores ranging from 0.91 (Internal Consistency) to 0.96 (Evidence Quality) across 6 dimensions.

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

**Finding 4: Architecture Follows Two-Phase Approach (Phase 3 ADR)**

- **Phase 1 (FEAT-001):** Place new engines in `src/infrastructure/internal/enforcement/` alongside existing engines. Stateless, fail-open, token-budgeted pattern.
- **Phase 2 (post-FEAT-001):** Extract to `src/context_monitoring/` bounded context when: (1) domain concepts stable, (2) persistent session repository available (CWI-00 satisfies this), (3) bounded context boundaries validated.

**Finding 5: Quality Gate Passed (QG-1)**

ADR-SPIKE002-001 scored 0.94 weighted composite (threshold: 0.92). Five defects found (1 P2, 4 P3), none blocking. P2 defect: missing rollback strategy (recommended to address before ADR status transitions to ACCEPTED).

### Evidence/References

| Artifact | Location |
|----------|----------|
| Phase 1: CLI Capability Audit | `orchestration/spike002-cli-integration-20260219-001/res/phase-1-audit/cli-auditor/cli-capability-audit.md` |
| Phase 2: Gap Analysis | `orchestration/spike002-cli-integration-20260219-001/res/phase-2-gap-analysis/gap-analyst/gap-analysis.md` |
| Phase 3: ADR-SPIKE002-001 | `orchestration/spike002-cli-integration-20260219-001/res/phase-3-architecture/architecture-designer/adr-cli-integration.md` |
| QG-1: Gate Result | `orchestration/spike002-cli-integration-20260219-001/res/quality-gates/qg-1/gate-result.md` |
| Phase 4: Revised Work Items | `orchestration/spike002-cli-integration-20260219-001/res/phase-4-synthesis/work-item-synthesizer/revised-work-items.md` |
| FileSystemEventStore source | `src/work_tracking/infrastructure/persistence/filesystem_event_store.py` |
| EventSourcedWorkItemRepository source | `src/work_tracking/infrastructure/adapters/event_sourced_work_item_repository.py` |
| ISessionRepository port | `src/session_management/application/ports/session_repository.py` |
| InMemorySessionRepository source | `src/session_management/infrastructure/adapters/in_memory_session_repository.py` |
| Session aggregate source | `src/session_management/domain/aggregates/session.py` |
| Session events source | `src/session_management/domain/events/session_events.py` |

---

## Recommendation

### Decision

**Integrate context resilience with existing CLI infrastructure** using the two-phase approach defined in ADR-SPIKE002-001. Implement the revised 10-item work plan (CWI-00 through CWI-09) which supersedes SPIKE-001's 14 items. Prioritize CWI-00 (FileSystemSessionRepository) as the P0 foundation enabler.

### Recommended Actions

1. **Immediately: Accept ADR-SPIKE002-001** (transition from PROPOSED to ACCEPTED status). Address P2 defect D-001 (rollback strategy) before acceptance.

2. **Phase A (Foundation):** Implement CWI-00 (FileSystemSessionRepository), CWI-01 (threshold config), and CWI-04 (resumption schema) in parallel. These have no dependencies and unblock all subsequent work.

3. **Phase B (Core Detection):** Implement CWI-02 (PreCompact hook with session abandon) then CWI-03 (context-aware UserPromptSubmit). This is the critical path.

4. **Phase C (Integration):** Implement CWI-05 (AE-006 sub-rules), CWI-06 (resumption automation), CWI-07 (staleness validation) -- partially parallelizable.

5. **Phase D (Validation):** Execute CWI-08 (OQ-9 + Method C investigation) and CWI-09 (threshold calibration) timeboxed activities.

### Follow-up Work Items

| ID | Title | Type | Priority | Effort |
|----|-------|------|----------|--------|
| CWI-00 | FileSystemSessionRepository | Enabler | P0 | 3-4 hrs |
| CWI-01 | Threshold Configuration via LayeredConfigAdapter | Enabler | P1 | 0.5 hrs |
| CWI-02 | PreCompact Hook + Checkpoint Infrastructure | Enabler | P1 | 3-5 hrs |
| CWI-03 | Context-Aware UserPromptSubmit Hook | Enabler | P1 | 3-4 hrs |
| CWI-04 | Enhanced Resumption Schema + Update Protocol | Story | P1 | 2-3 hrs |
| CWI-05 | AE-006 Graduated Sub-Rules | Story | P2 | 1 hr |
| CWI-06 | Resumption Prompt Automation (SessionStart) | Story | P2 | 2-3 hrs |
| CWI-07 | PostToolUse Staleness Validation | Enabler | P3 | 2-3 hrs |
| CWI-08 | Validation Spikes (OQ-9 + Method C) | Spike | P2 | 3 hrs |
| CWI-09 | Threshold Validation + Calibration Documentation | Story | P3 | 4 hrs |

**Total: 10 items, 19.5-28.5 hours estimated effort.**

Full work item definitions with acceptance criteria, CLI integration points, and dependency graphs are in the Phase 4 synthesis: `orchestration/spike002-cli-integration-20260219-001/res/phase-4-synthesis/work-item-synthesizer/revised-work-items.md`

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
| 2026-02-19 | done | Spike completed. 5-phase orchestration executed: (1) CLI Capability Audit identified 7 reusable capability categories, (2) Gap Analysis reclassified 10/14 items from NEW to REUSE/EXTEND and consolidated to 9 items, (3) ADR-SPIKE002-001 designed two-phase CLI-integrated architecture, (4) QG-1 passed at 0.94/0.92 threshold, (5) Final synthesis produced 10 revised work items (CWI-00 through CWI-09) incorporating user feedback to add FileSystemSessionRepository as P0 enabler. All 6 hypotheses validated (4 CONFIRMED, 2 PARTIALLY CONFIRMED). Estimated effort: 19.5-28.5 hours (22-23% reduction from SPIKE-001). |
