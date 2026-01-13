# Gap Analysis: Worktracker vs Problem-Solving Skill Structure

> **PS ID:** init-wt-skills
> **Entry ID:** e-005
> **Topic:** Comparative Gap Analysis
> **Author:** ps-analyst (Claude Opus 4.5)
> **Created:** 2026-01-11
> **Status:** COMPLETE

---

## L0: Executive Summary (ELI5)

Imagine you have two toolboxes. The `problem-solving` toolbox is a professional-grade setup: 8 specialized tools, each with its own instruction manual, organized compartments, and a master guide explaining how all the tools work together. The `worktracker` skills are like having 2 good screwdrivers loose in a drawer - functional but missing all the supporting infrastructure.

**The Gap in Numbers:**

| Metric | problem-solving | worktracker + decomposition | Gap |
|--------|-----------------|----------------------------|-----|
| Total files | 11 | 2 | -9 files |
| Total lines | 5,129 | 776 | -4,353 lines |
| Specialized agents | 8 | 0 | -8 agents |
| User playbook | Yes | No | Missing |
| Orchestration docs | Yes | No | Missing |
| Agent template | Yes | No | Missing |
| L0/L1/L2 output | Yes | No | Missing |
| State management | Yes | No | Missing |

**Priority Gap Rankings (by Impact x Effort):**

| Rank | Gap | Impact | Effort | Priority Score |
|------|-----|--------|--------|----------------|
| 1 | Missing agents | Critical | High | P0 |
| 2 | Missing agent template | High | Low | P1 |
| 3 | Missing PLAYBOOK.md | High | Medium | P1 |
| 4 | Inline templates | Medium | Low | P2 |
| 5 | Missing ORCHESTRATION.md | Medium | Medium | P2 |
| 6 | Missing L0/L1/L2 output | Medium | High | P3 |
| 7 | Missing state management | Low | Medium | P3 |

**Recommendation:** Start with P1 items (agent template + playbooks) which provide high value at low-medium effort, enabling the higher-effort P0 agent work to follow a consistent pattern.

---

## L1: Technical Analysis (Software Engineer)

### 1. Structural Gap Inventory

#### Gap S-001: Missing Three-Document Structure

**Observed Pattern (problem-solving):**
```
skills/problem-solving/
├── SKILL.md          # Contract (265 lines)
├── PLAYBOOK.md       # User Guide (407 lines)
└── docs/
    └── ORCHESTRATION.md  # Technical Architecture (486 lines)
```

**Current State (worktracker skills):**
```
skills/worktracker/
└── SKILL.md          # Everything in one file (336 lines)

skills/worktracker-decomposition/
└── SKILL.md          # Everything in one file (440 lines)
```

**Impact:** Users lack clear guidance on how to use the skills (PLAYBOOK), and developers lack technical documentation on composition patterns (ORCHESTRATION).

**Evidence:**
- `skills/problem-solving/PLAYBOOK.md` (407 lines): Table of contents, quick start, examples, troubleshooting
- `skills/problem-solving/docs/ORCHESTRATION.md` (486 lines): Agent pipeline, state management, fan-out patterns
- `skills/worktracker/SKILL.md`: Contains command reference only, no "how to use effectively"
- `skills/worktracker-decomposition/SKILL.md`: Contains command reference + inline templates, no user guidance

#### Gap S-002: Missing Agent Directory Structure

**Observed Pattern (problem-solving):**
```
skills/problem-solving/agents/
├── PS_AGENT_TEMPLATE.md     # Canonical template (335 lines)
├── ps-researcher.md         # 459 lines
├── ps-analyst.md            # 442 lines
├── ps-architect.md          # 426 lines
├── ps-validator.md          # 429 lines
├── ps-synthesizer.md        # 477 lines
├── ps-reviewer.md           # 446 lines
├── ps-investigator.md       # 489 lines
└── ps-reporter.md           # 468 lines
```

**Current State (worktracker skills):**
- No `agents/` directory exists
- No agent definitions exist
- No agent template exists

**Impact:** Operations are not backed by specialized agents, meaning:
- No L0/L1/L2 multi-audience output
- No constitutional compliance enforcement at agent level
- No state management for composition
- No guardrails or fallback behavior

#### Gap S-003: Inline Templates vs Extracted Templates

**Observed Pattern (problem-solving):**
- Templates referenced but stored separately (implied by `output.template` fields in agents)

**Current State (worktracker-decomposition/SKILL.md):**
```markdown
### Phase File Template (Lines 297-348)
{template inline in SKILL.md}

### Hub Template (Lines 350-390)
{template inline in SKILL.md}
```

**Impact:**
- Templates duplicated in RUNBOOK-002 and PURPOSE-CATALOG
- Changes require editing multiple files
- Templates not reusable by agents
- Harder to validate template compliance

### 2. Agent Gap Inventory

#### Gap A-001: No wt-analyzer Agent

**Problem-Solving Equivalent:** `ps-analyst`
- Performs 5 Whys, FMEA, trade-off analysis, gap analysis
- Output: Structured analysis reports with root cause and recommendations

**Worktracker Need:** Analyze WORKTRACKER files for decomposition triggers
- Detect size thresholds (500/800 lines)
- Identify phase boundaries
- Detect pain indicators (difficult navigation, context loss)

**Recommended Capabilities:**
```yaml
agent: wt-analyzer
cognitive_mode: convergent
methodologies:
  - Decomposition trigger detection (soft/hard thresholds)
  - Phase boundary identification (pattern matching)
  - Pain indicator detection (structural analysis)
output: Analysis report with decomposition recommendation
```

#### Gap A-002: No wt-decomposer Agent

**Problem-Solving Equivalent:** `ps-architect` + `ps-synthesizer`
- Makes structural decisions
- Transforms information across documents

**Worktracker Need:** Execute decomposition transformation
- Create hub-and-spoke file structure
- Maintain navigation links
- Preserve session context

**Recommended Capabilities:**
```yaml
agent: wt-decomposer
cognitive_mode: convergent
methodologies:
  - Hub creation (navigation graph, status dashboard)
  - Spoke extraction (phase files with backlinks)
  - Progressive detail assignment
output: Multi-file hub-and-spoke structure
```

#### Gap A-003: No wt-validator Agent

**Problem-Solving Equivalent:** `ps-validator`
- Verifies constraints with evidence
- Binary pass/fail assessment

**Worktracker Need:** Validate decomposed structure
- Verify hub size limits (<150 lines)
- Check all navigation links
- Validate session context presence

**Recommended Capabilities:**
```yaml
agent: wt-validator
cognitive_mode: convergent
methodologies:
  - Requirements Traceability Matrix (links valid)
  - Constraint verification (hub size, structure)
  - Session context validation
output: Validation report with pass/fail status
```

#### Gap A-004: No wt-reporter Agent (worktracker skill)

**Problem-Solving Equivalent:** `ps-reporter`
- Generates status reports with metrics
- Health indicators and progress tracking

**Worktracker Need:** Generate work item summaries
- Session resume summaries
- Progress dashboards
- Blocker identification

**Recommended Capabilities:**
```yaml
agent: wt-reporter
cognitive_mode: convergent
methodologies:
  - Status aggregation
  - Progress calculation
  - Blocker identification
output: Status report for session resume
```

### 3. Template Gap Inventory

#### Gap T-001: Templates Not Extracted

| Template | Current Location | Should Be |
|----------|-----------------|-----------|
| Phase File | `worktracker-decomposition/SKILL.md:297-348` | `templates/phase.md` |
| Hub Template | `worktracker-decomposition/SKILL.md:350-390` | `templates/hub.md` |

#### Gap T-002: Missing Templates

| Template | Purpose | Problem-Solving Equivalent |
|----------|---------|---------------------------|
| Analysis Report | wt-analyzer output | `ps-analyst` output template |
| Validation Report | wt-validator output | `ps-validator` output template |
| Category File | Cross-cutting category structure | N/A (domain-specific) |
| Work Item | Individual work item format | N/A (domain-specific) |
| Session Summary | wt-reporter output | `ps-reporter` output template |

### 4. Feature Gap Inventory

#### Gap F-001: Missing L0/L1/L2 Output Levels

**What problem-solving has:**
```markdown
## L0: Executive Summary (ELI5)
{Plain language summary for non-technical stakeholders}

## L1: Technical Analysis (Software Engineer)
{Implementation details, code examples, technical specifications}

## L2: Architectural Implications (Principal Architect)
{Strategic implications, trade-offs, long-term consequences}
```

**What worktracker skills have:**
- Single-level output (command results)
- No audience adaptation
- No strategic context

**Impact:** Outputs don't serve multiple stakeholders. A manager can't get a quick summary; an architect can't see strategic implications.

#### Gap F-002: Missing State Management

**What problem-solving has:**
```yaml
state_management:
  output_key: "researcher_output"
  state_schema:
    ps_id: "{ps_id}"
    entry_id: "{entry_id}"
    artifact_path: "{path}.md"
    summary: "{key_finding}"
    confidence: "high|medium|low"
    next_agent_hint: "{suggested_next}"
```

**What worktracker skills have:**
- No output keys
- No state schema
- No next_agent_hint for composition

**Impact:** Cannot compose worktracker operations into pipelines. Cannot pass results between agents.

#### Gap F-003: Missing Constitutional Compliance Table

**What problem-solving agents have:**
```markdown
## Constitutional Compliance

| Principle | Enforcement | How Applied |
|-----------|-------------|-------------|
| P-001 (Truth/Accuracy) | Soft | All claims cite sources |
| P-002 (File Persistence) | Medium | Output persisted to files |
| P-003 (No Recursion) | Hard | Single-level delegation only |
...
```

**What worktracker skills have:**
- Implicit adherence (no explicit table)
- No self-critique checklist
- No enforcement level specification

#### Gap F-004: Missing Guardrails Section

**What problem-solving agents have:**
```yaml
guardrails:
  input_validation:
    - Verify PS context provided
    - Check mandatory parameters
  output_filtering:
    - No output without file persistence
    - Evidence required for claims
  fallback_behavior:
    - If tool fails, report and suggest alternatives
```

**What worktracker skills have:**
- No input validation rules
- No output filtering rules
- No fallback behavior defined

### 5. Priority Ranking Matrix

| ID | Gap | Impact | Effort | Dependencies | Priority |
|----|-----|--------|--------|--------------|----------|
| A-000 | Agent template | HIGH | LOW | None | **P1** |
| S-001 | PLAYBOOK.md (both skills) | HIGH | MEDIUM | None | **P1** |
| T-001 | Extract templates | MEDIUM | LOW | None | **P2** |
| A-001 | wt-analyzer agent | CRITICAL | HIGH | A-000 | **P0** |
| A-002 | wt-decomposer agent | CRITICAL | HIGH | A-000, A-001 | **P0** |
| A-003 | wt-validator agent | HIGH | HIGH | A-000 | **P0** |
| S-002 | ORCHESTRATION.md | MEDIUM | MEDIUM | A-001+ | **P2** |
| F-001 | L0/L1/L2 output | MEDIUM | HIGH | A-000 | **P3** |
| F-002 | State management | LOW | MEDIUM | A-000 | **P3** |
| A-004 | wt-reporter agent | MEDIUM | HIGH | A-000 | **P3** |

**Recommended Sequence:**
1. **P1 First** (A-000, S-001): Create agent template and playbooks - enables all future agent work
2. **P2 Second** (T-001, S-002): Extract templates, create orchestration docs - sets foundation
3. **P0 Third** (A-001, A-002, A-003): Create core agents following template - main value delivery
4. **P3 Last** (F-001, F-002, A-004): Polish with L0/L1/L2, state management, reporter

---

## L2: Architectural Implications (Principal Architect)

### 1. Strategic Analysis

#### Why This Gap Matters

The gap between problem-solving and worktracker skills represents a **capability asymmetry** in the Jerry framework:

1. **Problem-solving** is the "flagship" skill - well-documented, agent-backed, composable
2. **Worktracker** is a "core" skill - used by every project, but lacks the same infrastructure

This asymmetry means:
- Problem-solving operations produce rich, multi-audience artifacts
- Worktracker operations produce simple command output
- Problem-solving can be composed into pipelines
- Worktracker cannot be composed

**Risk:** As Jerry scales to more projects, the worktracker capability gap becomes a bottleneck. Work tracking is used in every session, but lacks the robustness of other skills.

### 2. Design Patterns to Apply

#### Pattern 1: PAT-001 Agent Definition Template

From the ps-agent portfolio analysis (e-001), all 8 problem-solving agents follow an identical structure:

```yaml
- YAML frontmatter (identity, version, capabilities)
- <agent> XML block (identity, persona, capabilities, guardrails)
- <constitutional_compliance> (principles, self-critique)
- <invocation_protocol> (PS context, persistence)
- <output_levels> (L0/L1/L2 definitions)
- <state_management> (output key, schema, upstream/downstream)
- Markdown documentation (purpose, templates, examples)
```

**Recommendation:** Create `skills/worktracker-decomposition/agents/WT_AGENT_TEMPLATE.md` following this exact structure.

#### Pattern 2: PAT-002 Layered Output (L0/L1/L2)

Every agent output serves three audiences:
- L0: Executive summary (ELI5)
- L1: Technical details (Engineer)
- L2: Strategic implications (Architect)

**Recommendation:** Require all wt-* agents to produce L0/L1/L2 output. For worktracker operations:
- L0: "Task status changed to in_progress"
- L1: Full task metadata, history, dependencies
- L2: Project-level impact, phase implications, resource allocation

#### Pattern 3: PAT-005 Single-Level Delegation

From the constitution (P-003): Maximum ONE level of agent nesting.

**Recommendation:** Only one wt-* agent (likely wt-analyzer) should have the Task tool for single-level delegation. Other agents cannot spawn sub-agents.

### 3. Composition Architecture

#### Proposed Agent Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                    WORKTRACKER-DECOMPOSITION PIPELINE                │
└─────────────────────────────────────────────────────────────────────┘

    ANALYSIS                   TRANSFORMATION               VERIFICATION

    ┌─────────────────┐
    │   wt-analyzer   │──────┐
    │   (convergent)  │      │
    │   Trigger detect│      │
    └─────────────────┘      │
                             │     ┌─────────────────┐
                             └────►│  wt-decomposer  │──────┐
                                   │   (convergent)  │      │
                                   │   Hub + Spokes  │      │
                                   └─────────────────┘      │
                                                            │
                                                            │
                                                            │     ┌─────────────────┐
                                                            └────►│  wt-validator   │
                                                                  │   (convergent)  │
                                                                  │   Link check    │
                                                                  └─────────────────┘
```

#### Proposed Composition Points

| wt-* Agent | Can Compose With | Composition Pattern |
|------------|------------------|---------------------|
| wt-analyzer | ps-analyst | Gap analysis, root cause of decomposition need |
| wt-analyzer | ps-researcher | Research decomposition patterns in codebase |
| wt-decomposer | ps-architect | ADR for decomposition decisions |
| wt-validator | ps-validator | Constraint verification patterns |
| wt-reporter | ps-reporter | Status aggregation patterns |

### 4. Effort Estimation

Based on problem-solving agent line counts (average 456 lines):

| Deliverable | Estimated Lines | Effort (hours) |
|-------------|-----------------|----------------|
| WT_AGENT_TEMPLATE.md | ~335 | 3h |
| wt-analyzer.md | ~450 | 6h |
| wt-decomposer.md | ~450 | 6h |
| wt-validator.md | ~450 | 4h |
| PLAYBOOK.md (worktracker) | ~300 | 3h |
| PLAYBOOK.md (decomposition) | ~350 | 4h |
| ORCHESTRATION.md | ~400 | 4h |
| Extract templates (2) | ~100 | 2h |
| **TOTAL** | **~2,835** | **~32h** |

### 5. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Template changes break all agents | Medium | High | Version template, use semantic versioning |
| wt-* agents diverge from ps-* patterns | Medium | Medium | Code review against template |
| Composition patterns cause circular dependencies | Low | High | Define clear upstream/downstream in state_management |
| L0/L1/L2 overhead slows operations | Medium | Low | Make L1/L2 optional in agent config |
| Agents drift from constitution | Low | High | Automated validation via BEHAVIOR_TESTS.md |

### 6. Strategic Recommendations

#### Recommendation 1: Create Agent Template First (P1)

**Rationale:** All agent work depends on having a consistent template. Creating WT_AGENT_TEMPLATE.md first ensures consistency across all future wt-* agents.

**Deliverable:** `skills/worktracker-decomposition/agents/WT_AGENT_TEMPLATE.md`
- Copy PS_AGENT_TEMPLATE.md structure
- Adapt for worktracker domain
- Include worktracker-specific state fields

#### Recommendation 2: Create Playbooks Second (P1)

**Rationale:** Even without agents, playbooks improve discoverability and usability. Users can understand how to use the skills effectively.

**Deliverables:**
- `skills/worktracker/PLAYBOOK.md` (~300 lines)
- `skills/worktracker-decomposition/PLAYBOOK.md` (~350 lines)

Include: Quick start, examples, best practices, troubleshooting

#### Recommendation 3: Extract Templates Early (P2)

**Rationale:** Inline templates create duplication risk. Extract before agents reference them.

**Deliverables:**
- `skills/worktracker-decomposition/templates/phase.md`
- `skills/worktracker-decomposition/templates/hub.md`

#### Recommendation 4: Build Agents in Dependency Order (P0)

**Sequence:**
1. `wt-analyzer` (no agent dependencies)
2. `wt-decomposer` (depends on analyzer output)
3. `wt-validator` (depends on decomposer output)

Each agent: ~450 lines, 4-6 hours

#### Recommendation 5: Document Orchestration After Agents (P2)

**Rationale:** ORCHESTRATION.md documents how agents compose. Write after agents exist so documentation matches implementation.

**Deliverable:** `skills/worktracker-decomposition/docs/ORCHESTRATION.md`

---

## Knowledge Items Generated

### PAT-007: Skill Parity Pattern

**Context:** Framework skills should have consistent infrastructure
**Problem:** Skills with different maturity levels create user confusion
**Solution:** Define a minimum "skill infrastructure" standard:
- SKILL.md (contract)
- PLAYBOOK.md (user guide)
- docs/ORCHESTRATION.md (technical architecture)
- agents/ directory with template
**Consequences:**
- (+) Consistent user experience across skills
- (+) Predictable learning curve
- (+) Enables skill composition
- (-) Higher initial development cost

### LES-003: Templates Should Be Extracted Early

**Context:** Creating skill documentation with templates
**What Happened:** worktracker-decomposition has inline templates that are duplicated in RUNBOOK-002 and PURPOSE-CATALOG
**What We Learned:** Inline templates create duplication debt; extract early before they spread
**Prevention:** Extract templates to dedicated files before referencing in multiple documents

### ASM-002: Agent Infrastructure Enables Composition

**Assumption:** Skills without agent backing cannot participate in orchestrated pipelines
**Context:** Worktracker operations produce simple output, not composable state
**Impact if Wrong:** May find alternative composition patterns that don't require agents
**Confidence:** HIGH (based on problem-solving implementation)
**Validation Path:** Attempt to compose worktracker operations without agents

---

## References

### Input Documents

| Document | Path | Key Insight |
|----------|------|-------------|
| PS Agent Portfolio (e-001) | `projects/PROJ-001-plugin-cleanup/research/init-wt-skills-e-001-ps-agent-portfolio.md` | 8 agents with identical structure, PAT-001 through PAT-005 patterns |
| Worktracker Skill Gaps (e-004) | `projects/PROJ-001-plugin-cleanup/research/init-wt-skills-e-004-worktracker-skill-gaps.md` | 5,129 vs 776 line disparity, missing components list |

### Skill Files Analyzed

| File | Path | Lines |
|------|------|-------|
| problem-solving SKILL.md | `skills/problem-solving/SKILL.md` | 265 |
| problem-solving PLAYBOOK.md | `skills/problem-solving/PLAYBOOK.md` | 407 |
| worktracker SKILL.md | `skills/worktracker/SKILL.md` | 336 |
| worktracker-decomposition SKILL.md | `skills/worktracker-decomposition/SKILL.md` | 440 |

### External References

| Reference | URL | Relevance |
|-----------|-----|-----------|
| Chroma Context Rot | https://research.trychroma.com/context-rot | Why agent-backed persistence matters |
| Anthropic Agent Skills | https://venturebeat.com/technology/anthropic-launches-enterprise-agent-skills-and-opens-the-standard | Skills as procedural knowledge interfaces |

---

## Summary

This gap analysis identified **7 primary gaps** between the problem-solving skill structure (mature reference implementation) and the worktracker skills (functional but infrastructure-poor):

1. **Structural gaps (2):** Missing three-document structure, missing agent directory
2. **Agent gaps (4):** Missing wt-analyzer, wt-decomposer, wt-validator, wt-reporter
3. **Template gaps (2):** Inline templates, missing new templates
4. **Feature gaps (4):** Missing L0/L1/L2, state management, constitutional compliance, guardrails

**Closing these gaps requires approximately 32 hours of effort and 2,835 lines of new content.**

The recommended approach is to build foundation first (template, playbooks), then infrastructure (agents), then polish (L0/L1/L2, state management). This sequence ensures each subsequent step has the patterns it needs.

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-11 | ps-analyst (Claude Opus 4.5) | Initial gap analysis from e-001 and e-004 inputs |
