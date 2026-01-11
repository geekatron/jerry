# NASA SE Skill Orchestration

> Agent Coordination Patterns for NASA Systems Engineering

---

## Document Information

| Field | Value |
|-------|-------|
| Document ID | NSE-ORCH-001 |
| Version | 1.0.0 |
| Date | 2026-01-09 |
| Status | Active |
| References | NPR 7123.1D, NASA/SP-2016-6105 Rev2 |

---

## Overview

This document defines orchestration patterns for coordinating the 9 NASA Systems
Engineering (NSE) agents within the Jerry Framework. Orchestration ensures proper
sequencing, data flow, and state management across multi-agent workflows.

**Key Principles:**
1. **Single Level Nesting** - Per P-003, only orchestrator → worker (no worker → worker spawning)
2. **State Persistence** - All agent outputs persist to filesystem for context recovery
3. **Explicit Handoffs** - State schema defines clear inputs/outputs between agents
4. **User Authority** - Major decisions require user approval (P-020)

---

## Agent Registry

### 9 NSE Agents

| Agent | ID | Type | Cognitive Mode | NPR 7123.1D Processes |
|-------|-------|------|---------------|----------------------|
| Requirements Engineer | `nse-requirements` | Foundation | Convergent | 1, 2, 11 |
| V&V Specialist | `nse-verification` | Core | Convergent | 7, 8 |
| Risk Manager | `nse-risk` | Core | Convergent | 13 |
| Technical Architect | `nse-architecture` | Core | Convergent | 3, 4, 17 |
| **Exploration Engineer** | `nse-explorer` | **Divergent** | **Divergent** | 5, 17 |
| Technical Review Gate | `nse-reviewer` | Review | Convergent | All (assessment) |
| System Integration | `nse-integration` | Core | Convergent | 6, 12 |
| Configuration Mgmt | `nse-configuration` | Support | Convergent | 14, 15 |
| Status Reporter | `nse-reporter` | Aggregator | Convergent | 16 |

### Cognitive Modes

| Mode | Purpose | Agents |
|------|---------|--------|
| **Convergent** | Analyze, narrow, decide, verify | 8 of 9 agents |
| **Divergent** | Generate, explore, expand options | `nse-explorer` only |

---

## Dependency Graph

```
                        ┌─────────────────────┐
                        │    nse-reporter     │ (Terminal - L2 aggregation)
                        │  Process 16: Assess │
                        └──────────┬──────────┘
                                   │
           ┌───────────────────────┼───────────────────────┐
           │                       │                       │
    ┌──────▼──────┐         ┌──────▼──────┐         ┌──────▼──────┐
    │ nse-reviewer│         │  nse-risk   │         │ nse-config  │
    │ Reviews/RFAs│         │ Process 13  │         │ Process 14  │
    └──────┬──────┘         └──────┬──────┘         └──────┬──────┘
           │                       │                       │
    ┌──────▼──────┐         ┌──────▼──────┐         ┌──────▼──────┐
    │ nse-verific │         │nse-integr.  │         │nse-archit.  │
    │ Process 7,8 │         │ Process 6,12│         │ Process 3,4 │
    └──────┬──────┘         └──────┬──────┘         └──────┬──────┘
           │                       │                       │
           └───────────────────────┼───────────────────────┘
                                   │
                        ┌──────────▼──────────┐
                        │  nse-requirements   │ (Foundation - must run first)
                        │  Process 1, 2, 11   │
                        └─────────────────────┘
```

### Dependency Rules

1. **nse-requirements** is the foundation - provides requirements baseline
2. **Core agents** (verification, risk, architecture, integration) depend on requirements
3. **nse-configuration** tracks baselines from all domains
4. **nse-reviewer** assesses readiness across all domains
5. **nse-reporter** aggregates status from all agents (terminal)

---

## Orchestration Patterns

### Pattern 1: Sequential Chain

Use when outputs from one agent are required inputs for the next.

```
┌─────────────┐    state    ┌─────────────┐    state    ┌─────────────┐
│   Agent A   │ ─────────▶  │   Agent B   │ ─────────▶  │   Agent C   │
└─────────────┘             └─────────────┘             └─────────────┘
```

**Example:** Requirements → Verification → Risk Assessment

```yaml
orchestration:
  pattern: sequential
  sequence:
    - agent: nse-requirements
      output: requirements/REQ-SPEC-001.md
    - agent: nse-verification
      input: requirements/REQ-SPEC-001.md
      output: verification/VCRM-001.md
    - agent: nse-risk
      input:
        - requirements/REQ-SPEC-001.md
        - verification/VCRM-001.md
      output: risks/RISK-REG-001.md
```

### Pattern 2: Parallel Fan-Out

Use when multiple agents can work independently on separate aspects.

```
                    ┌─────────────┐
                    │   Agent A   │
              ┌────▶│             │
              │     └─────────────┘
              │
┌─────────┐   │     ┌─────────────┐
│ Trigger │───┼────▶│   Agent B   │
└─────────┘   │     └─────────────┘
              │
              │     ┌─────────────┐
              └────▶│   Agent C   │
                    └─────────────┘
```

**Example:** Post-Requirements Parallel Analysis

```yaml
orchestration:
  pattern: fan-out
  trigger: requirements_baseline_approved
  parallel_agents:
    - agent: nse-verification
      task: Create VCRM
    - agent: nse-architecture
      task: Functional decomposition
    - agent: nse-risk
      task: Initial risk assessment
```

### Pattern 3: Fan-In Aggregation

Use when a terminal agent needs to synthesize from multiple sources.

```
┌─────────────┐
│   Agent A   │────┐
└─────────────┘    │
                   │     ┌─────────────┐
┌─────────────┐    ├────▶│ Aggregator  │
│   Agent B   │────┤     └─────────────┘
└─────────────┘    │
                   │
┌─────────────┐    │
│   Agent C   │────┘
└─────────────┘
```

**Example:** SE Status Report Generation

```yaml
orchestration:
  pattern: fan-in
  aggregator: nse-reporter
  sources:
    - agent: nse-requirements
      provides: requirements_status
    - agent: nse-verification
      provides: verification_status
    - agent: nse-risk
      provides: risk_status
    - agent: nse-integration
      provides: interface_status
    - agent: nse-configuration
      provides: baseline_status
  output: reports/SE-STATUS-001.md
```

### Pattern 4: Review Gate

Use for technical review preparation and assessment.

```
┌──────────────────────────────────────────────────────────┐
│                    Review Gate Flow                       │
│                                                          │
│  ┌──────────────┐                                        │
│  │  Parallel    │  Readiness                             │
│  │  Artifact    │  Check          ┌────────────────┐     │
│  │  Generation  │ ───────────────▶│  nse-reviewer  │     │
│  └──────────────┘                 │  Gate Decision │     │
│                                   └───────┬────────┘     │
│                                           │              │
│                               ┌───────────┴───────────┐  │
│                               ▼                       ▼  │
│                          READY ✅              NOT READY │
│                               │                       │  │
│                               ▼                       ▼  │
│                     Proceed to Review        Remediation │
│                                               Actions    │
└──────────────────────────────────────────────────────────┘
```

### Pattern 5: Divergent-Convergent Flow (Diamond Pattern)

Use when exploration is needed before analysis/decision.

```
                    ┌─────────────────────┐
                    │   nse-explorer      │ ◄── DIVERGENT
                    │   (Generate 3+      │     (Expand options)
                    │    alternatives)    │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   User Decision     │ ◄── CHECKPOINT
                    │   (Select path)     │     (Human in loop)
                    └──────────┬──────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
  ┌──────▼──────┐       ┌──────▼──────┐       ┌──────▼──────┐
  │nse-architect│       │  nse-risk   │       │nse-integr.  │
  │ (Implement) │       │  (Analyze)  │       │  (Plan)     │
  └─────────────┘       └─────────────┘       └─────────────┘
                    ▲── CONVERGENT
                        (Narrow to solution)
```

**Key Characteristics:**
1. Exploration FIRST - Generate options before committing
2. User decision point - Human selects which alternative(s) to pursue
3. Convergent agents receive exploration output as context
4. Trade study artifacts inform downstream decisions

**Example:** Architecture Decision Flow

```yaml
orchestration:
  pattern: divergent-convergent
  phases:
    - name: Exploration
      agent: nse-explorer
      mode: divergent
      task: Generate storage architecture alternatives
      output:
        min_alternatives: 3
        artifact: exploration/TRADE-STORAGE-001.md

    - name: User Selection
      type: checkpoint
      prompt: "Review alternatives and select approach(es) to pursue"
      input: exploration/TRADE-STORAGE-001.md

    - name: Implementation Analysis
      pattern: fan-out
      input: user_selected_alternatives
      parallel:
        - agent: nse-architecture
          task: Detailed design for selected approach
          mode: convergent
        - agent: nse-risk
          task: Risk assessment for selected approach
          mode: convergent
        - agent: nse-integration
          task: Interface planning for selected approach
          mode: convergent
```

**When to Use Divergent-Convergent:**
- Early phase decisions (Phase A/B)
- Technology selection
- Architecture alternatives
- "What are our options?" questions
- Trade studies required by NASA SE

**Anti-Patterns to Avoid:**
- Skipping exploration and jumping to convergent analysis
- Using convergent agents (nse-architecture) for exploration
- Premature convergence without user checkpoint

---

## Common Workflows

### Workflow 1: CDR Preparation

**Purpose:** Prepare all artifacts for Critical Design Review

**Duration:** Multi-session workflow

**Sequence:**

```yaml
workflow: cdr_preparation
phases:
  - name: Phase 1 - Baseline Check
    agents:
      - nse-requirements:
          task: Verify requirements baseline completeness
          check: TBD count = 0, TBR count = 0
      - nse-configuration:
          task: Verify design baseline status
          check: All CIs identified

  - name: Phase 2 - Parallel Artifact Generation
    pattern: fan-out
    agents:
      - nse-architecture:
          task: Complete detailed design documentation
          output: architecture/DESIGN-DOC-001.md
      - nse-verification:
          task: Complete VCRM, verification procedures
          output: verification/VCRM-001.md
      - nse-integration:
          task: Finalize ICDs
          output: interfaces/ICD-*.md
      - nse-risk:
          task: Update risk register, assess CDR risks
          output: risks/RISK-REG-001.md

  - name: Phase 3 - Readiness Assessment
    agent: nse-reviewer
    task: Assess CDR entrance criteria
    input: All Phase 2 outputs
    output: reviews/CDR-READINESS-001.md

  - name: Phase 4 - Status Package
    agent: nse-reporter
    task: Generate CDR status report
    level: L2
    output: reports/CDR-STATUS-001.md

gate:
  type: user_approval
  prompt: "CDR artifacts complete. Review and approve to proceed."
```

### Workflow 2: Requirements Change Impact

**Purpose:** Assess impact of a requirements change

**Trigger:** New or modified requirement

```yaml
workflow: requirements_change_impact
trigger: requirement_change_request
sequence:
  - agent: nse-requirements
    task: Update requirement, trace impact
    output: Changed requirements list

  - pattern: fan-out
    parallel:
      - agent: nse-verification
        task: Assess verification impact
        output: Affected test cases
      - agent: nse-architecture
        task: Assess design impact
        output: Affected design elements
      - agent: nse-integration
        task: Assess interface impact
        output: Affected ICDs
      - agent: nse-risk
        task: Assess new/changed risks
        output: Risk delta

  - agent: nse-configuration
    task: Prepare change request package
    input: All impact assessments
    output: Change Request (ECR)

  - gate: user_review
    prompt: "Review impact assessment and approve/reject change"
```

### Workflow 3: Risk Escalation

**Purpose:** Handle escalation of RED risk

**Trigger:** Risk score ≥ 16

```yaml
workflow: red_risk_escalation
trigger: risk_score >= 16
immediate_actions:
  - agent: nse-risk
    task: Generate risk brief
    level: L1
    output: risks/RISK-BRIEF-{ID}.md

  - agent: nse-reporter
    task: Generate executive alert
    level: L0
    output: reports/RISK-ALERT-{ID}.md

user_notification:
  type: immediate
  content: |
    🔴 RED RISK IDENTIFIED
    Risk ID: {risk_id}
    Title: {risk_title}
    Score: {likelihood} × {consequence} = {score}
    Recommended Action: Review risk brief and mitigation plan

follow_up:
  - pattern: fan-out
    agents:
      - nse-architecture:
          task: Assess design alternatives
      - nse-verification:
          task: Assess verification workarounds
```

### Workflow 4: New Project Bootstrap

**Purpose:** Initialize SE artifacts for a new project

```yaml
workflow: project_bootstrap
sequence:
  - agent: nse-requirements
    task: Create requirements specification template
    output: requirements/REQ-SPEC-001.md

  - agent: nse-risk
    task: Create risk register, initial risk assessment
    output: risks/RISK-REG-001.md

  - pattern: fan-out
    parallel:
      - agent: nse-architecture
        task: Create functional architecture template
        output: architecture/FUNC-ARCH-001.md
      - agent: nse-verification
        task: Create VCRM template
        output: verification/VCRM-001.md
      - agent: nse-integration
        task: Create interface list template
        output: interfaces/IF-LIST-001.md
      - agent: nse-configuration
        task: Create CI list, baseline definition
        output: configuration/CI-LIST-001.md

  - agent: nse-reporter
    task: Generate initial SE status
    level: L0
    output: reports/SE-STATUS-001.md

checkpoint:
  type: user_review
  prompt: "Initial SE artifacts created. Review and baseline."
```

### Workflow 5: Trade Study Exploration

**Purpose:** Explore alternatives before major technical decisions

**Trigger:** "What are our options for X?" or explicit trade study request

```yaml
workflow: trade_study_exploration
trigger: decision_needed
phases:
  - name: Phase 1 - Divergent Exploration
    agent: nse-explorer
    mode: divergent
    task: Generate alternatives for decision
    output:
      type: trade_study
      min_alternatives: 3
      artifact: exploration/TRADE-{topic}.md
    constraints:
      - no_premature_convergence
      - challenge_assumptions
      - include_unconventional_options

  - name: Phase 2 - User Review Checkpoint
    type: user_decision
    prompt: |
      Review the trade study: exploration/TRADE-{topic}.md

      Select which alternative(s) to pursue:
      [ ] Alternative 1: {name}
      [ ] Alternative 2: {name}
      [ ] Alternative 3: {name}
      [ ] Request additional alternatives

  - name: Phase 3 - Convergent Analysis
    pattern: fan-out
    parallel:
      - agent: nse-architecture
        task: Detailed design for selected alternative
        mode: convergent
        input: User-selected alternative from exploration
      - agent: nse-risk
        task: Risk assessment for selected approach
        mode: convergent
        input: User-selected alternative from exploration
      - agent: nse-requirements
        task: Requirements allocation for selected approach
        mode: convergent
        input: User-selected alternative from exploration

  - name: Phase 4 - Decision Documentation
    agent: nse-architecture
    task: Document final decision with rationale
    input: All Phase 3 outputs
    output: architecture/ADR-{topic}.md
    includes:
      - alternatives_considered
      - selection_rationale
      - trade_study_reference
```

**Divergent-Convergent Transition Rules:**

| Phase | Mode | Agent | Output |
|-------|------|-------|--------|
| Exploration | Divergent | nse-explorer | 3+ alternatives |
| Selection | Checkpoint | User | Chosen path(s) |
| Analysis | Convergent | nse-architecture, nse-risk, nse-requirements | Detailed analysis |
| Documentation | Convergent | nse-architecture | ADR with decision |

---

## Session Context Validation (WI-SAO-002)

All agent handoffs MUST use the session context schema for reliable chaining.

### Schema Reference

- **Schema:** `docs/schemas/session_context.json`
- **Version:** 1.0.0
- **Scope:** All nse-* agents and cross-skill handoffs

### Required Fields

Every session context MUST include:

```yaml
session_context:
  schema_version: "1.0.0"       # REQUIRED: For evolution support
  session_id: "{uuid}"          # REQUIRED: Detect session mismatch
  source_agent:                 # REQUIRED: Sender identification
    id: "nse-{domain}"
    family: "nse"
  target_agent:                 # REQUIRED: Receiver identification
    id: "{target-agent-id}"
    family: "ps|nse|orch"
  payload:                      # REQUIRED: Handoff data
    key_findings: [...]         # REQUIRED: Primary outputs
    confidence:                 # REQUIRED: Confidence score
      overall: 0.0-1.0
  timestamp: "ISO-8601"         # REQUIRED: Creation time
```

### Input Validation (On Receive)

Before processing, target agents MUST validate:

```
1. Schema Version Check
   ├── IF schema_version != "1.0.0"
   │   └── WARN "Potential schema mismatch" + attempt processing
   └── IF schema_version missing
       └── REJECT "Invalid handoff: missing schema_version"

2. Session Identity Check
   ├── IF session_id matches current session
   │   └── CONTINUE normally
   └── IF session_id differs
       └── WARN "State from different session" + prompt user (see FIX-NEG-008)

3. Source Agent Validation
   ├── IF source_agent.id matches pattern ^(ps|nse|orch)-[a-z]+$
   │   └── CONTINUE
   └── ELSE
       └── REJECT "Invalid source agent ID format"

4. Payload Validation
   ├── IF payload.key_findings is array
   │   └── CONTINUE
   ├── IF payload.confidence.overall is number 0.0-1.0
   │   └── CONTINUE
   └── ELSE
       └── REJECT "Malformed payload"
```

### Output Validation (On Send)

Before returning, source agents MUST:

```
1. Populate Key Findings
   └── key_findings array with findings from SE domain artifacts

2. Calculate Confidence
   └── confidence.overall between 0.0 and 1.0 with NASA SE context

3. Include Traceability (P-040)
   └── Each finding.traceability links to REQ-*, RISK-*, TSR-*, ICD-*

4. List Artifacts
   └── artifacts array with paths to all created SE work products

5. Set Timestamp
   └── ISO-8601 timestamp at completion time

6. Verify Target
   └── target_agent.id matches expected downstream agent per dependency graph
```

### Validation Error Handling

| Error Type | Severity | Action |
|------------|----------|--------|
| Missing required field | CRITICAL | Reject handoff, alert orchestrator |
| Invalid schema_version | WARNING | Log warning, attempt processing |
| Session mismatch | WARNING | Prompt user for decision (FIX-NEG-008) |
| Malformed payload | CRITICAL | Reject handoff, request retry |
| Invalid agent ID | CRITICAL | Reject handoff, halt workflow |
| Missing traceability | WARNING | Log gap, continue with documentation |

### Cross-Skill Handoff (nse ↔ ps)

When handing off between skill families:

```yaml
# nse-requirements → ps-analyst example (for trade study support)
session_context:
  source_agent:
    id: "nse-requirements"
    family: "nse"
    cognitive_mode: "convergent"
  target_agent:
    id: "ps-analyst"
    family: "ps"               # Different family - cross-skill handoff
    cognitive_mode: "divergent"
  payload:
    key_findings:
      - id: "F-001"
        summary: "Requirements trade study needed for mass allocation"
        category: "requirement"
        traceability: ["REQ-SYS-042", "TSR-001"]  # SE domain IDs
    context:
      se_lifecycle_phase: "Phase B"
      review_milestone: "CDR"
```

**Cross-Skill Considerations:**
1. Map SE lifecycle context for ps-* agents unfamiliar with NASA phases
2. Include traceability in NASA SE format (REQ-*, RISK-*, TSR-*, ICD-*)
3. Specify review milestone context for appropriate rigor level

### NSE Agent Chain Validation

For the 8-agent dependency chain, validate handoff compliance:

```
nse-requirements (foundation)
    └── VALIDATES: schema_version, session_id, payload structure
    └── OUTPUTS: REQ-* traceability, TBD/TBR counts
           │
    ┌──────┴──────────────────────────────────┐
    ▼                                         ▼
nse-verification                        nse-architecture
    └── VALIDATES: input requirements IDs     └── VALIDATES: input requirements IDs
    └── OUTPUTS: VCRM reference, test IDs     └── OUTPUTS: TSR reference, element IDs
           │                                         │
    ┌──────┴───────────────────┐                     │
    ▼                          ▼                     ▼
nse-risk                  nse-integration      nse-configuration
    └── VALIDATES: req + design input              └── VALIDATES: all domain inputs
    └── OUTPUTS: RISK-* IDs, L/C scores            └── OUTPUTS: CI-* references
           │                          │                   │
           └──────────────────────────┴───────────────────┘
                                      │
                                      ▼
                               nse-reviewer
                                  └── VALIDATES: all upstream artifacts
                                  └── OUTPUTS: readiness decision, RFAs
                                             │
                                             ▼
                                       nse-reporter
                                          └── VALIDATES: all sources for aggregation
                                          └── OUTPUTS: L0/L1/L2 status reports
```

---

## State Management

### Agent State Schema

All agents share a common state schema structure for handoffs:

```json
{
  "agent_id": "nse-{domain}",
  "session_id": "{uuid}",
  "timestamp": "{iso8601}",
  "project": "{project_name}",
  "phase": "{lifecycle_phase}",
  "inputs": {
    "from_agent": "{source_agent_id}",
    "artifacts": ["{artifact_paths}"]
  },
  "outputs": {
    "artifacts": ["{artifact_paths}"],
    "status": "{success/partial/failed}"
  },
  "handoff_ready": {
    "{target_agent}": true|false
  },
  "alerts": ["{critical_items}"]
}
```

### State Persistence

Agent states are persisted to:

```
projects/{PROJECT}/
└── .jerry/
    └── nse-state/
        ├── nse-requirements-state.json
        ├── nse-verification-state.json
        ├── nse-risk-state.json
        ├── nse-architecture-state.json
        ├── nse-explorer-state.json      # Divergent agent state
        ├── nse-integration-state.json
        ├── nse-configuration-state.json
        ├── nse-reviewer-state.json
        └── nse-reporter-state.json
```

### Session Validation (FIX-NEG-008)

Before loading any persisted state, the orchestrator MUST validate session identity:

**Session Validation Algorithm:**
```
function validateSession(state_file, current_session_id):
  state = load(state_file)

  if state.session_id == current_session_id:
    return CONTINUE_NORMALLY(state)

  if state.session_id != current_session_id:
    # Session mismatch detected
    warning = "State from different session detected"
    options = [
      "Continue with old state (resume previous work)",
      "Start fresh (preserve old state as backup)"
    ]

    user_choice = prompt_user(warning, options, timeout=30s)

    if user_choice == null:  # Timeout
      backup_state(state_file, timestamp)
      return START_FRESH(default_safe=true)

    if user_choice == "continue":
      return CONTINUE_WITH_STATE(state, warn_once=true)

    if user_choice == "start_fresh":
      backup_state(state_file, timestamp)
      return START_FRESH()

  return START_FRESH()  # Fallback safe default
```

**Session Mismatch Handling:**

| Scenario | Detection | Action | User Prompt |
|----------|-----------|--------|-------------|
| Same session | `session_id` matches | Continue normally | None |
| Different session | `session_id` differs | Warn + prompt | "State from different session detected. Continue or start fresh?" |
| Timeout (no response) | 30s without response | Safe default | None (auto-start fresh, preserve backup) |
| Corrupted state | Parse/schema error | Start fresh | "State file corrupted. Starting fresh." |

**Safe Defaults:**
- Default to starting fresh (never silently use old state)
- Always preserve old state as backup before overwriting
- Backup naming: `{state-file}.backup.{timestamp}`

**State Backup Location:**
```
projects/{PROJECT}/
└── .jerry/
    └── nse-state/
        ├── nse-requirements-state.json
        └── backups/
            └── nse-requirements-state.json.backup.2026-01-09T10-30-00Z
```

### Handoff Protocol

1. **Source Agent** completes task and sets `handoff_ready[target] = true`
2. **Orchestrator** reads source state, validates outputs exist
3. **Target Agent** receives inputs from source artifacts
4. **Target Agent** acknowledges receipt in its state
5. **Source Agent** state can be archived/cleared

---

## Error Handling

### Retry Policy

```yaml
retry_policy:
  max_attempts: 3
  backoff: exponential
  base_delay: 2s
  recoverable_errors:
    - api_timeout
    - rate_limit
    - transient_error
  non_recoverable_errors:
    - invalid_input
    - permission_denied
    - validation_failed
```

### Failure Modes

| Failure Mode | Detection | Recovery |
|--------------|-----------|----------|
| Agent timeout | No response in timeout window | Retry with exponential backoff |
| Invalid output | Schema validation fails | Alert user, request correction |
| Missing dependency | Required input not found | Block and notify, request missing artifact |
| Cascade failure | Multiple agents fail | Halt workflow, preserve state, alert user |

### Graceful Degradation

When an agent fails, the orchestration should:

1. **Preserve completed work** - Don't discard successful outputs
2. **Isolate failure** - Prevent cascade to other agents
3. **Notify user** - Clear explanation of what failed and why
4. **Offer recovery options** - Retry, skip, or abort

---

## Invocation Examples

### Example 1: CDR Preparation (User Request)

**User:** "Help me prepare for CDR"

**Orchestration Response:**

```
I'll coordinate the NSE agents to prepare your CDR package.

Phase 1: Checking baselines...
├── nse-requirements: Verifying requirements completeness
├── nse-configuration: Checking design baseline

Phase 2: Generating artifacts (parallel)...
├── nse-architecture: Updating design documentation
├── nse-verification: Completing VCRM
├── nse-integration: Finalizing ICDs
├── nse-risk: Updating risk assessment

Phase 3: Readiness check...
├── nse-reviewer: Assessing CDR entrance criteria

Phase 4: Status report...
├── nse-reporter: Generating CDR status package

[Checkpoint: Review CDR artifacts before proceeding]
```

### Example 2: Impact Assessment (User Request)

**User:** "What's the impact if we change REQ-042?"

**Orchestration Response:**

```
I'll coordinate impact analysis across domains.

Running parallel impact assessment...
├── nse-requirements: Tracing REQ-042 dependencies → 3 derived requirements affected
├── nse-verification: Finding affected tests → 2 test procedures need update
├── nse-architecture: Checking design impact → Component C design may change
├── nse-integration: Checking interface impact → ICD-007 potentially affected
├── nse-risk: Assessing new risks → 1 new YELLOW risk identified

Summary: REQ-042 change impacts:
- 3 requirements (trace update needed)
- 2 test procedures (modification required)
- 1 design element (analysis needed)
- 1 ICD (review recommended)
- 1 new risk (mitigation needed)

[Shall I generate a formal change request package?]
```

---

## Integration with Jerry Framework

### Work Tracker Integration

NSE workflows create Work Tracker items:

| Workflow Event | Work Item Type | Example |
|----------------|----------------|---------|
| Review preparation started | `task` | "Prepare CDR package" |
| Risk escalation | `issue` | "RED Risk: R-042 requires mitigation" |
| Review action assigned | `action-item` | "RFA-001: Update mass budget" |
| Change request created | `change-request` | "ECR-015: Modify REQ-042" |

### Problem-Solving Integration

NSE agents can receive handoffs from Problem-Solving agents:

```yaml
handoff:
  from: ps-analyst
  to: nse-risk
  context: "Analysis identified technical risk requiring formal assessment"
```

### Constitutional Compliance

All orchestrated workflows MUST comply with:

- **P-003:** Single level of agent nesting
- **P-020:** User authority for major decisions
- **P-040:** Traceability maintained across handoffs
- **P-041:** Verification status tracked
- **P-042:** Risks escalated appropriately
- **P-043:** Disclaimers on all outputs

---

## References

1. NPR 7123.1D - NASA Systems Engineering Processes and Requirements
2. NASA/SP-2016-6105 Rev2 - SE Handbook
3. Jerry Framework Constitution v1.0
4. NSE Skill Definition (SKILL.md)

---

*Document Version: 1.0.0*
*Last Updated: 2026-01-09*
