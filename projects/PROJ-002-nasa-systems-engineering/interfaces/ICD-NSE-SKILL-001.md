# Interface Control Document: NASA SE Skill

> **Document ID:** ICD-NSE-SKILL-001
> **Version:** 1.0
> **Date:** 2026-01-09
> **Status:** CONTROLLED
> **Author:** Claude Code

---

## L0: Executive Summary

The NASA SE Skill interfaces with the Jerry Framework through 7 primary interfaces: skill activation, 8 agent invocations, knowledge base access, project output persistence, orchestration coordination, state handoff between agents, and user interaction. All interfaces use markdown/YAML formats with well-defined contracts.

---

## L1: Interface Specification

### 1. N² Diagram: Skill Component Interfaces

**Components:**
| ID | Component | Description |
|----|-----------|-------------|
| A | SKILL.md Router | Skill activation and agent routing |
| B | Agent Suite (8) | Specialized SE domain agents |
| C | Knowledge Base | Standards, processes, exemplars |
| D | Project Outputs | Persisted SE artifacts |
| E | Orchestration | Agent coordination patterns |
| F | Jerry Framework | Parent framework integration |
| G | User | Human interaction point |

**N² Matrix:**

|     | A | B | C | D | E | F | G |
|-----|---|---|---|---|---|---|---|
| **A** | - | IF-001 | IF-002 | - | IF-003 | IF-004 | - |
| **B** | - | IF-005 | IF-006 | IF-007 | IF-008 | - | - |
| **C** | - | - | - | - | - | - | - |
| **D** | - | - | - | - | - | - | - |
| **E** | - | IF-009 | - | - | - | - | - |
| **F** | IF-010 | - | - | - | - | - | - |
| **G** | IF-011 | - | - | IF-012 | - | - | - |

*Rows = Provider, Columns = Consumer*

### 2. Interface Registry

| IF ID | Provider | Consumer | Type | Protocol | Status |
|-------|----------|----------|------|----------|--------|
| IF-001 | SKILL.md | Agents | Invocation | Task Tool | ✅ Defined |
| IF-002 | SKILL.md | Knowledge | Read | Glob/Read | ✅ Defined |
| IF-003 | SKILL.md | Orchestration | Pattern | YAML Config | ✅ Defined |
| IF-004 | SKILL.md | Jerry | Activation | Keywords | ✅ Defined |
| IF-005 | Agents | Agents | State Handoff | JSON Schema | ✅ Defined |
| IF-006 | Agents | Knowledge | Read | Glob/Read | ✅ Defined |
| IF-007 | Agents | Project | Write | Write Tool | ✅ Defined |
| IF-008 | Agents | Orchestration | Follow | YAML Workflow | ✅ Defined |
| IF-009 | Orchestration | Agents | Invoke | Sequence | ✅ Defined |
| IF-010 | Jerry | SKILL.md | Activate | Keyword Match | ✅ Defined |
| IF-011 | User | SKILL.md | Request | Natural Language | ✅ Defined |
| IF-012 | User | Project | Review | Read Files | ✅ Defined |

---

### 3. Interface Definitions

#### IF-001: Agent Invocation Interface

| Attribute | Value |
|-----------|-------|
| Interface ID | IF-001 |
| Interface Name | Agent Invocation |
| Provider | SKILL.md (Router) |
| Consumer | nse-* Agents (8) |
| Interface Type | Software |
| Classification | Internal |

**Protocol Specification:**

| Attribute | Value |
|-----------|-------|
| Protocol | Task Tool API |
| Format | Markdown Prompt |
| Transport | Claude Code Internal |
| Authentication | N/A (internal) |

**Data Elements:**

| Element | Type | Format | Required |
|---------|------|--------|----------|
| agent_name | string | nse-{domain} | Y |
| project_id | string | PROJ-\d{3} | Y |
| entry_id | string | e-\d+ | N |
| topic | string | free text | Y |
| output_level | enum | L0/L1/L2 | N (defaults L1) |

**Example Invocation:**
```markdown
## NSE CONTEXT (REQUIRED)
- **Project ID:** PROJ-002
- **Entry ID:** e-001
- **Topic:** Create requirements specification for authentication
```

---

#### IF-005: Agent State Handoff Interface

| Attribute | Value |
|-----------|-------|
| Interface ID | IF-005 |
| Interface Name | State Handoff |
| Provider | Any nse-* Agent |
| Consumer | Any nse-* Agent |
| Interface Type | Data |
| Classification | Internal |

**State Schema (JSON):**
```json
{
  "agent_id": "string (nse-{domain})",
  "project_id": "string (PROJ-XXX)",
  "entry_id": "string (e-XXX)",
  "artifact_path": "string (file path)",
  "summary": "string (brief output summary)",
  "domain_data": {
    "comment": "Domain-specific fields"
  },
  "next_agent_hint": "string (suggested next agent)",
  "nasa_processes_applied": ["array of process IDs"]
}
```

**Domain-Specific Extensions:**

| Agent | Additional Fields |
|-------|-------------------|
| nse-requirements | req_count, tbd_count, tbr_count |
| nse-risk | risk_count, red_risks, total_exposure |
| nse-verification | verified_count, pending_count, coverage_pct |
| nse-architecture | alternative_count, selected_alternative |
| nse-integration | interface_count, defined_count, tbd_count |
| nse-configuration | ci_count, baseline_id, pending_changes |
| nse-reviewer | entrance_criteria_met, exit_criteria_met |
| nse-reporter | overall_status, domain_statuses |

---

#### IF-004: Jerry Framework Activation Interface

| Attribute | Value |
|-----------|-------|
| Interface ID | IF-004 |
| Interface Name | Skill Activation |
| Provider | SKILL.md |
| Consumer | Jerry Framework |
| Interface Type | Software |
| Classification | External |

**Activation Keywords (20):**
```yaml
activation_keywords:
  - "systems engineering"
  - "NASA SE"
  - "NPR 7123"
  - "requirements"
  - "verification"
  - "risk management"
  - "technical review"
  - "SRR"
  - "PDR"
  - "CDR"
  - "FRR"
  - "interface control"
  - "configuration management"
  - "trade study"
  - "status report"
  - "VCRM"
  - "traceability"
  - "baseline"
  - "risk register"
  - "ICD"
```

---

#### IF-007: Project Output Persistence Interface

| Attribute | Value |
|-----------|-------|
| Interface ID | IF-007 |
| Interface Name | Output Persistence |
| Provider | nse-* Agents |
| Consumer | Project Directory |
| Interface Type | Data |
| Classification | Internal |

**Output Path Convention:**
```
projects/${JERRY_PROJECT}/{domain}/{doc-id}-{topic-slug}.md
```

**Domain Directories:**
| Domain | Directory | Agent |
|--------|-----------|-------|
| Requirements | requirements/ | nse-requirements |
| Risks | risks/ | nse-risk |
| Verification | verification/ | nse-verification |
| Architecture | architecture/ | nse-architecture |
| Interfaces | interfaces/ | nse-integration |
| Configuration | configuration/ | nse-configuration |
| Reviews | reviews/ | nse-reviewer |
| Reports | reports/ | nse-reporter |

**File Format Requirements:**
- Format: Markdown with YAML frontmatter
- Mandatory disclaimer at top
- L0/L1/L2 output levels
- References section with NASA citations

---

### 4. Interface Constraints

| Constraint | Description | Rationale |
|------------|-------------|-----------|
| P-002 Compliance | All outputs MUST be persisted | Constitutional requirement |
| P-003 Compliance | No recursive agent spawning | Hard constitutional limit |
| P-043 Compliance | All outputs include disclaimer | AI guidance transparency |
| File Format | Markdown only | Jerry standard |
| Encoding | UTF-8 | Consistency |
| Line Endings | LF or CRLF | Cross-platform |

---

### 5. Error Handling

| Error Code | Meaning | Consumer Action |
|------------|---------|-----------------|
| MISSING_CONTEXT | NSE Context not provided | Add required context block |
| INVALID_PROJECT | Project ID format invalid | Use PROJ-\d{3} format |
| AGENT_NOT_FOUND | Unknown agent specified | Use valid nse-* agent name |
| PERSISTENCE_FAILED | Write tool failed | Retry or check permissions |
| STATE_PARSE_ERROR | Malformed state JSON | Validate against schema |

---

### 6. Verification Approach

| Method | Description | Criteria |
|--------|-------------|----------|
| Inspection | Review interface documentation | All fields documented |
| Demonstration | Invoke agent via Task tool | Agent responds correctly |
| Test | BDD behavioral tests | Tests pass |

---

## L2: Integration Context

### Interface Complexity Assessment

| Metric | Value | Assessment |
|--------|-------|------------|
| Total Interfaces | 12 | Moderate |
| Defined | 12 | ✅ 100% |
| Draft | 0 | ✅ |
| TBD | 0 | ✅ |
| Complexity Score | Medium | Manageable |

### Critical Interfaces

| IF ID | Why Critical | Risk |
|-------|--------------|------|
| IF-004 | Skill activation entry point | Low - well-defined keywords |
| IF-005 | Multi-agent coordination | Medium - state schema validation |
| IF-007 | Output persistence (P-002) | Low - Write tool reliable |

### Integration Sequence

```
1. User → IF-011 → SKILL.md (natural language request)
2. Jerry → IF-010 → SKILL.md (keyword activation)
3. SKILL.md → IF-001 → Agent (Task tool invocation)
4. Agent → IF-006 → Knowledge (read standards)
5. Agent → IF-007 → Project (write output)
6. Agent → IF-005 → Agent (state handoff if chained)
7. User → IF-012 → Project (review artifacts)
```

### Risk Assessment

| Risk | L | C | Score | Mitigation |
|------|---|---|-------|------------|
| State handoff data loss | 2 | 3 | 6 | JSON schema validation |
| Activation keyword collision | 1 | 2 | 2 | Specific keyword set |
| Output path conflicts | 2 | 2 | 4 | Naming conventions |

---

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-09 | Claude Code | Initial release |

---

## References

- NPR 7123.1D Process 12 - Interface Management
- NASA-HDBK-1009A - Interface Control Document format
- Jerry Framework SKILL.md specification
- ORCHESTRATION.md - Agent coordination patterns

---

*DISCLAIMER: This Interface Control Document is AI-generated based on NASA Systems Engineering standards. It is advisory only and does not constitute official NASA guidance. All interface decisions require human review and professional engineering judgment.*
