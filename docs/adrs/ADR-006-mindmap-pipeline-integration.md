# ADR-006: Mindmap Pipeline Integration

> **PS:** EN-024-adr-20260130-001
> **Exploration:** draft-006
> **Created:** 2026-01-30
> **Status:** ACCEPTED
> **Agent:** ps-architect
> **Supersedes:** N/A
> **Superseded By:** N/A

---

## Context

The Transcript Skill includes mindmap generator agents (ts-mindmap-mermaid, ts-mindmap-ascii) implemented in EN-009, but these agents are NOT integrated into the default pipeline. Users must manually invoke mindmaps after transcript processing, breaking the seamless workflow experience.

### Background

#### L0 (ELI5) - The Assembly Line Metaphor

Imagine a factory that processes meeting recordings:
1. **Reception Desk** (ts-parser) - Takes your raw recording and organizes it
2. **Research Analyst** (ts-extractor) - Finds all the important stuff
3. **Publishing House** (ts-formatter) - Makes beautiful documents
4. **Quality Inspector** (ps-critic) - Checks everything meets standards

There's also a "Visualization Department" (mindmap agents) that can create visual mind maps, but it's sitting in a separate building. Users have to walk over there separately to get a mind map. We want to connect the Visualization Department to the main assembly line so mind maps are automatically created.

#### L1 (Software Engineer) - Technical Gap

**Current Pipeline (4-Stage):**
```
ts-parser → ts-extractor → ts-formatter → ps-critic
```

**Mindmap Agents (Disconnected):**
```
ts-mindmap-mermaid  ← NOT in pipeline
ts-mindmap-ascii    ← NOT in pipeline
```

EN-009 implemented the mindmap agents with:
- Mermaid format with deep linking (ADR-003)
- ASCII art fallback for terminal compatibility
- Topic hierarchy visualization
- Entity symbol markers

However, the SKILL.md orchestrator does not invoke these agents.

#### L2 (Architect) - Strategic Considerations

**Industry Context:**
- Mind maps are a differentiating feature not common in competing transcript tools (EN-001 Market Analysis)
- Visual representation aids comprehension and reduces cognitive load
- Deep linking provides source verification capability

**Constitutional Compliance:**
- P-002: File Persistence - Mindmaps persist to `08-mindmap/` directory
- P-003: No Recursive Subagents - Single-level nesting maintained
- P-020: User Authority - User controls mindmap generation via flags

**Research conducted** (see TASK-240 Research, TASK-241 Analysis):
- Current pipeline state analysis
- 5W2H + Ishikawa analysis for integration
- Pareto analysis for risk prioritization
- Directory numbering correction (DISC-001: 07→08)

### Constraints

| ID | Constraint | Source |
|----|------------|--------|
| C-001 | Maximum ONE level of agent nesting | P-003 Jerry Constitution |
| C-002 | All outputs must persist to filesystem | P-002 Jerry Constitution |
| C-003 | Processing time < 10 seconds for 1-hour transcript | NFR-001 |
| C-004 | Mindmaps require extraction report AND packet path | ts-mindmap-* agents |
| C-005 | Output directory is `08-mindmap/` | DISC-001 Resolution |
| C-006 | ps-critic must validate mindmaps when present | EN-006 |

### Forces

1. **User Experience vs. Flexibility:** Generating mindmaps by default provides a complete packet but increases processing time. Opt-out flag provides escape hatch.

2. **Format Diversity vs. Simplicity:** Supporting both Mermaid and ASCII adds value but doubles mindmap generation work. Default "both" satisfies most use cases.

3. **Pipeline Integrity vs. Failure Tolerance:** Mindmap failure could block the entire pipeline or degrade gracefully. Graceful degradation preserves core functionality.

4. **Quality Assurance vs. Scope Creep:** ps-critic should validate mindmaps but needs new criteria. Modular criteria (MM-*/AM-*) prevent scope creep.

---

## Options Considered

### Option A: Mindmaps After ts-formatter, Before ps-critic (RECOMMENDED)

Insert mindmap generation as a conditional step between ts-formatter and ps-critic.

```
ts-parser → ts-extractor → ts-formatter → [ts-mindmap-*] → ps-critic
                                               │
                                     (conditional on --no-mindmap)
```

**Behavior:**
- Mindmaps generated **by default** with `--no-mindmap` opt-out flag
- `--mindmap-format` parameter: mermaid, ascii, both (default: both)
- Output to `08-mindmap/` directory

**Pros:**
- Mindmaps have access to formatter output (packet_path required)
- ps-critic can validate mindmap files
- Clean sequential flow with conditional step
- Satisfies user requirement for default generation

**Cons:**
- Adds ~1 minute to pipeline execution
- Two format options to maintain

**Fit with Constraints:**
- C-001: PASS - Single-level nesting maintained
- C-002: PASS - Files persist to 08-mindmap/
- C-003: PASS - ~1 minute overhead acceptable
- C-004: PASS - Mindmaps run after formatter provides packet_path
- C-005: PASS - Uses corrected 08-mindmap/ directory
- C-006: PASS - ps-critic receives mindmaps in validation scope

### Option B: Mindmaps Parallel with ts-formatter

Run mindmap generation in parallel with ts-formatter to save time.

```
ts-parser → ts-extractor ┬→ ts-formatter → ps-critic
                         └→ ts-mindmap-*
```

**Pros:**
- Faster execution (parallel)

**Cons:**
- Mindmaps need `packet_path` from ts-formatter - **DEPENDENCY VIOLATION**
- Cannot determine anchor format before packet creation
- ps-critic receives incomplete context

**Fit with Constraints:**
- C-004: **FAIL** - Mindmaps require packet_path from formatter

**REJECTED:** Dependency constraint violation.

### Option C: Mindmaps After ps-critic

Run mindmap generation as the final pipeline step.

```
ts-parser → ts-extractor → ts-formatter → ps-critic → [ts-mindmap-*]
```

**Pros:**
- Minimal impact to existing pipeline
- Mindmaps not critical path for quality review

**Cons:**
- ps-critic cannot validate mindmap quality
- Two-pass quality review needed if mindmap validation required
- Violates requirement for mindmap quality assurance

**Fit with Constraints:**
- C-006: **FAIL** - ps-critic cannot validate mindmaps

**REJECTED:** Quality assurance constraint violation.

---

## Decision

**We will use Option A: Mindmaps After ts-formatter, Before ps-critic.**

### Rationale

1. **Dependency Satisfaction (C-004):** Mindmap agents require both `extraction_report_path` (from ts-extractor) and `packet_path` (from ts-formatter). Option A is the only position that provides both.

2. **Quality Assurance (C-006):** Placing mindmaps before ps-critic enables validation of mindmap syntax, structure, and deep links as part of the standard quality review.

3. **User Requirement:** The user explicitly requested mindmaps be generated **by default** with opt-out behavior. This matches the "batteries included" philosophy.

4. **DISC-001 Resolution:** The corrected `08-mindmap/` directory avoids the numbering conflict with `07-topics.md` identified during pipeline research.

5. **Graceful Degradation:** The design allows the pipeline to continue with a warning if mindmap generation fails, preserving core functionality.

### Default Behavior

| Invocation | Mindmap Generation | Format |
|------------|-------------------|--------|
| `/transcript file.vtt` | **YES (default)** | Both (Mermaid + ASCII) |
| `/transcript file.vtt --mindmap-format mermaid` | YES | Mermaid only |
| `/transcript file.vtt --mindmap-format ascii` | YES | ASCII only |
| `/transcript file.vtt --no-mindmap` | NO (opt-out) | N/A |

### Alignment

| Criterion | Score | Notes |
|-----------|-------|-------|
| Constraint Satisfaction | HIGH | All 6 constraints met |
| Risk Level | LOW | Graceful degradation mitigates failures |
| Implementation Effort | MEDIUM | Orchestration update + ps-critic criteria |
| Reversibility | HIGH | Flag-based opt-out, no breaking changes |

---

## Consequences

### Positive Consequences

1. **Complete Packet Output:** Users receive mindmaps automatically with a single `/transcript` command, eliminating manual post-processing.

2. **Quality-Assured Mindmaps:** ps-critic validates mindmap syntax (MM-*) and ASCII constraints (AM-*), ensuring consistent quality.

3. **Format Flexibility:** Users can select specific formats or opt-out entirely via command-line parameters.

4. **Competitive Differentiation:** Mindmaps are a differentiating feature that competitors typically lack (per EN-001 market analysis).

5. **Deep Linking Integration:** Mindmap nodes link directly to transcript anchors (ADR-003), providing source verification.

### Negative Consequences

1. **Increased Processing Time:** Pipeline execution increases by ~1 minute when mindmaps are enabled (acceptable trade-off).

2. **Additional Failure Mode:** Mindmap generation could fail, requiring graceful degradation handling.

### Neutral Consequences

1. **ps-critic Scope Expansion:** New validation criteria (MM-*/AM-*) needed, but these are modular additions.

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Mindmap failure blocks pipeline | LOW | HIGH | Graceful degradation: continue with warning |
| ps-critic scoring regression | MEDIUM | LOW | Conditional scoring only when mindmaps present |
| Directory numbering confusion | LOW | MEDIUM | DISC-001 documents and resolves 07→08 |
| Format selection confusion | LOW | LOW | Clear documentation, sensible defaults |
| Deep link format mismatch | LOW | HIGH | ADR-003 defines canonical anchor format |

---

## Implementation

### Pipeline Integration Design

```
INTEGRATED PIPELINE (Mindmaps by Default)
==========================================

USER INPUT
    │
    │ /transcript file.vtt [--mindmap-format both]
    │ /transcript file.vtt --no-mindmap  (to disable)
    │
    ▼
┌───────────────────────────────────────────────────────────────────┐
│                     SKILL.md ORCHESTRATOR                          │
│                   (P-003: Single-level nesting)                    │
└───────────────────────────────────────────────────────────────────┘
    │
    │ Sequential Execution
    ▼
┌─────────┐     ┌─────────────┐     ┌─────────────┐
│ts-parser│────▶│ts-extractor │────▶│ts-formatter │
│ (haiku) │     │  (sonnet)   │     │  (sonnet)   │
└─────────┘     └─────────────┘     └──────┬──────┘
                                           │
                                           │ ts_formatter_output.packet_path
                                           ▼
                              ┌────────────────────────────┐
                              │   --no-mindmap flag set?   │
                              └────────────┬───────────────┘
                                           │
                    ┌──────────────────────┴──────────────────────┐
                    │ NO (default)                                │ YES
                    ▼                                             ▼
        ┌─────────────────────┐                          (skip mindmaps)
        │    ts-mindmap-*     │                                   │
        │      (sonnet)       │                                   │
        │                     │                                   │
        │ ┌─────────────────┐ │                                   │
        │ │ts-mindmap-mermaid│ │                                  │
        │ └─────────────────┘ │                                   │
        │ ┌─────────────────┐ │                                   │
        │ │ts-mindmap-ascii │ │                                   │
        │ └─────────────────┘ │                                   │
        └──────────┬──────────┘                                   │
                   │                                              │
                   │ 08-mindmap/ files                            │
                   ▼                                              │
        ts_mindmap_output                                         │
                   │                                              │
                   └──────────────────────┬───────────────────────┘
                                          │
                                          ▼
                              ┌─────────────────────┐
                              │     ps-critic       │
                              │      (sonnet)       │
                              │                     │
                              │ • Core validation   │
                              │ • MM-* criteria     │
                              │   (if mindmaps)     │
                              │ • AM-* criteria     │
                              │   (if ASCII)        │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              quality-review.md
```

### Parameter Specification

| Parameter | Type | Required | Default | Values | Description |
|-----------|------|----------|---------|--------|-------------|
| `--no-mindmap` | flag | No | false | (presence) | Disable mindmap generation |
| `--mindmap-format` | string | No | "both" | mermaid, ascii, both | Format(s) to generate |

### State Passing

New state key for mindmap output:

```yaml
ts_mindmap_output:
  enabled: boolean              # Was --no-mindmap NOT set?
  format_requested: string      # "mermaid" | "ascii" | "both"
  mermaid:
    path: string | null         # Path to 08-mindmap/mindmap.mmd
    status: string              # "complete" | "failed" | "skipped"
    error_message: string | null
    topic_count: integer
    deep_link_count: integer
  ascii:
    path: string | null         # Path to 08-mindmap/mindmap.ascii.txt
    status: string              # "complete" | "failed" | "skipped"
    error_message: string | null
    topic_count: integer
    max_line_width: integer     # Should be <= 80
  overall_status: string        # "complete" | "partial" | "failed"
```

### Graceful Degradation Design

```
FAILURE SCENARIO: Mindmap generation fails
==========================================

1. CAPTURE error message and status
   ts_mindmap_output.{format}.status = "failed"
   ts_mindmap_output.{format}.error_message = "{error}"

2. SET overall status
   IF all formats failed THEN
       ts_mindmap_output.overall_status = "failed"
   ELSE IF any format failed THEN
       ts_mindmap_output.overall_status = "partial"
   END IF

3. CONTINUE pipeline execution
   DO NOT ABORT - proceed to ps-critic

4. LOG warning in ps-critic output:
   "⚠️ Mindmap generation {partial/failed}: {error_message}"

5. INCLUDE regeneration instructions:
   "To regenerate mindmaps: /transcript --regenerate-mindmap <packet-path>"
```

### ps-critic Validation Criteria

**Mermaid Mindmap Criteria (MM-*):**

| ID | Criterion | Severity |
|----|-----------|----------|
| MM-001 | Valid Mermaid mindmap syntax | ERROR |
| MM-002 | Root node present and labeled | ERROR |
| MM-003 | Deep links use correct anchor format (#anchor-id) | ERROR |
| MM-004 | Topic hierarchy matches extraction report | WARNING |
| MM-005 | Entity symbols present (→, ?, !, ✓) | WARNING |
| MM-006 | Maximum 50 topics (overflow handled) | WARNING |
| MM-007 | File size < 35K tokens | ERROR |

**ASCII Mindmap Criteria (AM-*):**

| ID | Criterion | Severity |
|----|-----------|----------|
| AM-001 | No line exceeds 80 characters | ERROR |
| AM-002 | Legend present at bottom | ERROR |
| AM-003 | Valid UTF-8 box-drawing characters | ERROR |
| AM-004 | Tree structure visually balanced | WARNING |
| AM-005 | Entity symbols match Mermaid version | WARNING |

**Conditional Scoring:**
- When mindmaps enabled: 80% core criteria + 20% mindmap criteria
- When mindmaps disabled: 100% core criteria (unchanged)

### Output Directory Structure

```
transcript-{id}/
├── 00-index.md
├── 01-summary.md
├── 02-transcript.md
├── 03-speakers.md
├── 04-action-items.md
├── 05-decisions.md
├── 06-questions.md
├── 07-topics.md
├── 08-mindmap/                 # NEW: Mindmap directory
│   ├── mindmap.mmd             # Mermaid format (if enabled)
│   └── mindmap.ascii.txt       # ASCII format (if enabled)
└── _anchors.json
```

### Action Items

| # | Action | Owner | Task | Status |
|---|--------|-------|------|--------|
| 1 | Update SKILL.md with --no-mindmap and --mindmap-format | Claude | TASK-243 | Pending |
| 2 | Update pipeline orchestration flow | Claude | TASK-244 | Pending |
| 3 | Add MM-*/AM-* validation criteria to ps-critic | Claude | TASK-245 | Pending |
| 4 | Create integration tests | Claude | TASK-246 | Pending |
| 5 | Update PLAYBOOK.md and RUNBOOK.md | Claude | TASK-247 | Pending |
| 6 | Quality review (ps-critic >= 0.90) | Claude | TASK-248 | Pending |

### Validation Criteria

1. **Default Behavior Test:** `/transcript file.vtt` generates both mindmap formats
2. **Opt-Out Test:** `/transcript file.vtt --no-mindmap` skips mindmap generation
3. **Format Selection Test:** `--mindmap-format mermaid` generates only Mermaid
4. **Failure Handling Test:** Pipeline continues with warning on mindmap failure
5. **Quality Validation Test:** ps-critic validates MM-*/AM-* criteria when mindmaps present
6. **Output Location Test:** Mindmaps written to `08-mindmap/` directory

---

## Related Decisions

| ADR | Relationship | Notes |
|-----|--------------|-------|
| ADR-001 | DEPENDS_ON | Defines hybrid architecture with custom agents + ps-critic |
| ADR-002 | EXTENDS | Artifact structure extended with 08-mindmap/ (DISC-001 resolution) |
| ADR-003 | DEPENDS_ON | Deep link format used in mindmap nodes |
| ADR-004 | RELATED_TO | Token limits apply to mindmap files |
| ADR-005 | DEPENDS_ON | Phased agent implementation (mindmaps are prompt-based) |

---

## References

| # | Reference | Type | Relevance |
|---|-----------|------|-----------|
| 1 | TASK-240-pipeline-state-research.md | Research | Current pipeline analysis |
| 2 | TASK-241-5w2h-ishikawa-analysis.md | Analysis | Integration risk analysis |
| 3 | EN-024--DISC-001-mindmap-directory-numbering-discrepancy.md | Discovery | 07→08 numbering resolution |
| 4 | EN-009-mindmap-generator.md | Enabler | Mindmap agent implementation |
| 5 | ts-mindmap-mermaid.md | Agent Spec | Mermaid agent definition |
| 6 | ts-mindmap-ascii.md | Agent Spec | ASCII agent definition |
| 7 | ADR-002-artifact-structure.md | ADR | Packet structure standard |
| 8 | ADR-003-bidirectional-linking.md | ADR | Anchor format specification |
| 9 | EN-001 Market Analysis | Research | Competitive differentiation |
| 10 | Jerry Constitution P-002, P-003 | Governance | Constitutional compliance |

---

## Appendix A: Invocation Examples

### Default Behavior (Mindmaps Generated)

```bash
# Standard invocation - both mindmap formats generated
/transcript meeting.vtt

# Specify output directory
/transcript meeting.vtt --output ./docs/meetings/

# Force format detection
/transcript meeting.vtt --format vtt
```

### Format Selection

```bash
# Only Mermaid format
/transcript meeting.vtt --mindmap-format mermaid

# Only ASCII format
/transcript meeting.vtt --mindmap-format ascii

# Both formats (explicit, same as default)
/transcript meeting.vtt --mindmap-format both
```

### Opt-Out (Skip Mindmaps)

```bash
# Disable mindmap generation
/transcript meeting.vtt --no-mindmap

# With other options
/transcript meeting.vtt --no-mindmap --output ./docs/
```

---

## Appendix B: State Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        STATE FLOW                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ts-parser                                                           │
│      │                                                               │
│      ▼                                                               │
│  ts_parser_output:                                                   │
│    canonical_json_path: "canonical-transcript.json"                  │
│    format_detected: "vtt"                                            │
│    segment_count: 245                                                │
│      │                                                               │
│      ▼                                                               │
│  ts-extractor                                                        │
│      │                                                               │
│      ▼                                                               │
│  ts_extractor_output:                                                │
│    extraction_report_path: "extraction-report.json" ◄──────────┐    │
│    action_count: 14                                            │    │
│    decision_count: 4                                           │    │
│      │                                                         │    │
│      ▼                                                         │    │
│  ts-formatter                                                  │    │
│      │                                                         │    │
│      ▼                                                         │    │
│  ts_formatter_output:                                          │    │
│    packet_path: "transcript-20260130-meeting/" ◄──────────┐    │    │
│    files_created: [...]                                   │    │    │
│      │                                                    │    │    │
│      ▼                                                    │    │    │
│  ts-mindmap-* (uses extraction_report_path + packet_path) │────┴────┘
│      │                                                                │
│      ▼                                                               │
│  ts_mindmap_output:                                                  │
│    enabled: true                                                     │
│    format_requested: "both"                                          │
│    mermaid:                                                          │
│      path: "transcript-*/08-mindmap/mindmap.mmd"                    │
│      status: "complete"                                              │
│    ascii:                                                            │
│      path: "transcript-*/08-mindmap/mindmap.ascii.txt"              │
│      status: "complete"                                              │
│    overall_status: "complete"                                        │
│      │                                                               │
│      ▼                                                               │
│  ps-critic (validates all files including mindmaps)                  │
│      │                                                               │
│      ▼                                                               │
│  quality_output:                                                     │
│    quality_score: 0.92                                               │
│    passed: true                                                      │
│    issues: []                                                        │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Appendix C: Risk Mitigation Matrix

| Risk ID | Risk | Mitigation | Implementation |
|---------|------|------------|----------------|
| R-001 | Mindmap failure blocks pipeline | Graceful degradation | Try-catch with warning, continue to ps-critic |
| R-002 | State passing breaks | Explicit schema | `ts_mindmap_output` state key documented |
| R-003 | ps-critic validation gaps | Modular criteria | MM-*/AM-* criteria for mindmap-specific validation |
| R-004 | Directory numbering conflict | DISC-001 resolution | Use `08-mindmap/` consistently |
| R-005 | Format selection confusion | Clear defaults | Default "both", clear documentation |

---

**Generated by:** ps-architect agent
**Template Version:** 1.0 (Nygard ADR Format)
**Quality Review:** PENDING - requires ps-critic review (TASK-248)
**Constitutional Compliance:** P-002 (file persistence), P-003 (single-level nesting), P-020 (user authority)
