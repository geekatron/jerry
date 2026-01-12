# NASA Systems Engineering Playbook

> **Version:** 2.0.0
> **Skill:** nasa-se
> **Purpose:** Systems engineering guidance based on NASA NPR 7123.1D and SE Handbook
> **Updated:** 2026-01-12 - Triple-lens refactoring (SAO-INIT-007)

---

## Document Overview

```
+============================================================================+
|                       TRIPLE-LENS COGNITIVE FRAMEWORK                       |
+=============================================================================+
|                                                                             |
|    L0 (ELI5)          L1 (Engineer)         L2 (Architect)                 |
|    ----------         -------------         --------------                 |
|    WHAT & WHY    ->   HOW (commands)   ->   CONSTRAINTS                    |
|    Metaphors          Invocations           Anti-patterns                  |
|    Intent             File paths            Boundaries                     |
|    Analogies          Input/Output          Invariants                     |
|                                                                             |
|    "Explains to       "Executable           "Prevents                      |
|     newcomers"         instructions"          mistakes"                    |
|                                                                             |
+=============================================================================+
```

**Target Audience:**
- **L0**: Anyone (stakeholders, newcomers, non-technical)
- **L1**: Engineers applying NASA SE practices
- **L2**: Architects designing SE workflows, ensuring compliance

---

# L0: The Big Picture (ELI5)

> *This section explains WHAT NASA Systems Engineering does and WHY it matters.*

## What Is NASA Systems Engineering?

### The Mission Control Metaphor

```
+===================================================================+
|                       MISSION CONTROL                              |
+===================================================================+
|                                                                   |
|   Think of NASA SE like running Mission Control:                  |
|                                                                   |
|               T-10...9...8...7...6...5...4...3...2...1           |
|                              LAUNCH!                              |
|                                                                   |
|   Before launch, you go through rigorous checkpoints:             |
|                                                                   |
|   +------+    +------+    +------+    +------+    +------+        |
|   | SRR  |--->| PDR  |--->| CDR  |--->| TRR  |--->| FRR  |        |
|   +------+    +------+    +------+    +------+    +------+        |
|   System      Prelim      Critical   Test        Flight           |
|   Req Rev     Design      Design     Readiness   Readiness        |
|                                                                   |
|   At each checkpoint, specialized teams review:                   |
|                                                                   |
|   +---------------+  +---------------+  +---------------+         |
|   | REQUIREMENTS  |  | VERIFICATION  |  |     RISK      |         |
|   | "What must    |  | "Does it      |  | "What could   |         |
|   |  we build?"   |  |  work?"       |  |  go wrong?"   |         |
|   +---------------+  +---------------+  +---------------+         |
|                                                                   |
|   +---------------+  +---------------+  +---------------+         |
|   | ARCHITECTURE  |  | INTEGRATION   |  | CONFIGURATION |         |
|   | "How do parts |  | "Do parts     |  | "What changed |         |
|   |  fit?"        |  |  connect?"    |  |  & why?"      |         |
|   +---------------+  +---------------+  +---------------+         |
|                                                                   |
|   Each team has a STATION in Mission Control.                     |
|   Each agent is a FLIGHT CONTROLLER at that station.              |
|                                                                   |
+===================================================================+
```

**Plain English:**
NASA Systems Engineering is a structured approach to building complex systems that works. It ensures you:
- Know what you're building (requirements)
- Can prove it works (verification)
- Understand what could go wrong (risk)
- Have parts that fit together (architecture, integration)
- Track all changes (configuration)

### Why Does This Matter?

| Without NASA SE | With NASA SE |
|-----------------|--------------|
| Requirements unclear or forgotten | Every "shall" is traceable |
| "It works on my machine" | Verification proves it works |
| Risks discovered at launch | Risks identified and mitigated early |
| Reviews are rubber stamps | Reviews catch problems before they're expensive |
| Changes happen randomly | Configuration baseline controls change |

### When Do I Use This?

```
ACTIVATION DECISION:
--------------------

IS THIS A SYSTEMS ENGINEERING TASK?
           |
     +-----+-----+
     |           |
     v           v
    YES          NO
     |           |
     v           v
  Use nse-*    Use ps-*
  agents       agents
     |
     v
WHAT TYPE?
     |
+----+----+----+----+----+----+----+
|    |    |    |    |    |    |    |
v    v    v    v    v    v    v    v
Req? Ver? Risk? Arch? Rev? Int? Cfg? Status?
```

**Activation Keywords:**

| Keyword | Agent |
|---------|-------|
| "requirements", "shall", "need" | nse-requirements |
| "verification", "VCRM", "test", "V&V" | nse-verification |
| "risk", "mitigation", "5x5" | nse-risk |
| "architecture", "trade study" | nse-architecture |
| "SRR", "PDR", "CDR", "review" | nse-reviewer |
| "integration", "interface", "ICD" | nse-integration |
| "configuration", "baseline", "change" | nse-configuration |
| "status", "dashboard" | nse-reporter |

---

## The Cast of Characters (Agents)

> *Meet the flight controllers at each station*

```
+=========================================================================+
|                    MISSION CONTROL STATIONS                              |
+=========================================================================+
|                                                                         |
|    STATION 1              STATION 2              STATION 3              |
|    +----------------+     +----------------+     +----------------+     |
|    | nse-requirements|     | nse-verification|     | nse-risk       |     |
|    | -------------- |     | -------------- |     | -------------- |     |
|    | CAPCOM         |     | FIDO           |     | FLIGHT SURGEON |     |
|    | "What to build"|     | "Does it work?"|     | "What's risky?"|     |
|    +----------------+     +----------------+     +----------------+     |
|                                                                         |
|    STATION 4              STATION 5              STATION 6              |
|    +----------------+     +----------------+     +----------------+     |
|    | nse-architecture|     | nse-reviewer   |     | nse-integration|     |
|    | -------------- |     | -------------- |     | -------------- |     |
|    | GNC            |     | FLIGHT DIRECTOR|     | INCO           |     |
|    | "How it fits"  |     | "Go/No-Go"     |     | "Connections"  |     |
|    +----------------+     +----------------+     +----------------+     |
|                                                                         |
|    STATION 7              STATION 8                                     |
|    +----------------+     +----------------+                            |
|    | nse-configuration|     | nse-reporter   |                            |
|    | -------------- |     | -------------- |                            |
|    | EGIL           |     | PAO            |                            |
|    | "What changed" |     | "Status update"|                            |
|    +----------------+     +----------------+                            |
|                                                                         |
+=========================================================================+
```

| Agent | Station | Like a... | Does What |
|-------|---------|-----------|-----------|
| `nse-requirements` | CAPCOM | Requirements analyst | Creates SHALL statements, traceability |
| `nse-verification` | FIDO | Test engineer | V&V planning, VCRM, test results |
| `nse-risk` | Flight Surgeon | Risk manager | Risk identification, 5x5 scoring, mitigation |
| `nse-architecture` | GNC | Systems architect | Trade studies, design decisions |
| `nse-reviewer` | Flight Director | Review board | SRR/PDR/CDR/TRR/FRR gate reviews |
| `nse-integration` | INCO | Integration engineer | ICDs, interface management |
| `nse-configuration` | EGIL | Config manager | Baseline management, change control |
| `nse-reporter` | PAO | Status reporter | Dashboards, status reports |

---

## The Review Sequence

> *The path from concept to flight*

```
+===================================================================+
|                    TECHNICAL REVIEW SEQUENCE                       |
+===================================================================+
|                                                                   |
|   CONCEPT     DESIGN           BUILD         TEST      FLY        |
|      |          |                |            |         |         |
|      v          v                v            v         v         |
|   +------+   +------+   +------+   +------+   +------+           |
|   | SRR  |-->| PDR  |-->| CDR  |-->| TRR  |-->| FRR  |---> GO!   |
|   +------+   +------+   +------+   +------+   +------+           |
|                                                                   |
|   SRR: System Requirements Review                                 |
|        "Do we know WHAT to build?"                               |
|                                                                   |
|   PDR: Preliminary Design Review                                  |
|        "Is the design APPROACH sound?"                           |
|                                                                   |
|   CDR: Critical Design Review                                     |
|        "Is the design COMPLETE and correct?"                     |
|                                                                   |
|   TRR: Test Readiness Review                                      |
|        "Are we ready to TEST?"                                   |
|                                                                   |
|   FRR: Flight Readiness Review                                    |
|        "Are we ready to FLY?"                                    |
|                                                                   |
+===================================================================+
```

Each review has **entrance criteria** (must be ready before) and **exit criteria** (must be met to pass).

---

# L1: How To Use It (Engineer)

> *This section provides executable instructions: commands, invocations, file paths.*

## Quick Start

### The 30-Second Version

1. **State your SE need** - "I need requirements for X"
2. **The right agent activates** - Based on keywords
3. **Output follows NASA format** - With traceability
4. **Disclaimer included** - AI guidance, human review required

### Minimal Example

```
User: "Create requirements for secure user authentication"

Claude: [Activates nse-requirements agent]
        [Creates requirements with SHALL statements]
        [Adds traceability to stakeholder needs]
        [Creates requirements/auth-requirements.md]
        [Includes P-043 disclaimer]
```

---

## Invocation Methods

### Method 1: Natural Language (Recommended)

```
"I need requirements for user authentication"
-> Activates nse-requirements

"What are the risks for the database migration?"
-> Activates nse-risk

"Help me prepare for PDR"
-> Activates nse-reviewer

"Create a trade study for caching options"
-> Activates nse-architecture

"Show verification status for phase 2"
-> Activates nse-verification

"Create ICD for the API interface"
-> Activates nse-integration
```

### Method 2: Explicit Agent Request

```
"Use nse-requirements to create security requirements"
"Have nse-risk do a 5x5 assessment"
"I need nse-reviewer to check PDR entrance criteria"
```

### Method 3: Review Preparation

```
"Help me prepare for [SRR|PDR|CDR|TRR|FRR]"
```

This triggers nse-reviewer to:
1. Check entrance criteria
2. Generate review package
3. Identify gaps
4. Create RFAs (Request For Action) list

---

## Agent Reference

| Agent | When to Use | Keywords | Output Location | Output Format |
|-------|-------------|----------|-----------------|---------------|
| `nse-requirements` | Creating SHALL statements | requirements, shall, need | `requirements/` | Requirements spec |
| `nse-verification` | V&V planning | verification, VCRM, test | `verification/` | VCRM, test plan |
| `nse-risk` | Risk management | risk, mitigation, 5x5 | `risks/` | Risk register |
| `nse-architecture` | Design decisions | architecture, trade study | `architecture/` | Trade study |
| `nse-reviewer` | Technical reviews | SRR, PDR, CDR, review | `reviews/` | Review package |
| `nse-integration` | Interface management | integration, interface, ICD | `interfaces/` | ICD |
| `nse-configuration` | Change control | configuration, baseline | `configuration/` | CI list |
| `nse-reporter` | Status updates | status, dashboard | `reports/` | Dashboard |

---

## Common Workflows

### Workflow 1: New Project Setup

**Goal:** Initialize SE artifacts for a new project.

```
User: "Help me bootstrap SE for my IoT sensor project"

[nse-requirements + nse-risk + nse-verification activate in sequence]

Artifacts Created:
- requirements/requirements-specification.md
- risks/risk-register.md
- verification/vcrm-template.md
- interfaces/interface-list.md
```

### Workflow 2: Requirements Development

**Goal:** Develop and document requirements.

```
WORKFLOW:
---------

1. "I need requirements for [capability]"
   -> nse-requirements creates SHALL statements

2. "Review generated requirements"
   -> Human review and refinement

3. "Create traceability matrix"
   -> nse-requirements links to stakeholder needs

EXAMPLE OUTPUT:
---------------

REQ-AUTH-001: The system SHALL authenticate users via username/password.
- Priority: 1 (Critical)
- Verification: Test
- Rationale: Basic access control
- Traces to: STK-001 (Stakeholder need for security)
```

### Workflow 3: Risk Assessment

**Goal:** Identify and score risks.

```
WORKFLOW:
---------

1. "Identify risks for [system/feature]"
   -> nse-risk creates risk register entries

2. "Score these risks using 5x5 matrix"
   -> nse-risk assigns Likelihood x Consequence

3. "Create mitigation plans for RED risks"
   -> nse-risk develops mitigation strategies

EXAMPLE OUTPUT:
---------------

R-001: Data Corruption During Migration
- Statement: IF data validation fails during migration,
             THEN records may be corrupted,
             resulting in data integrity issues.
- Likelihood: 3 (Moderate)
- Consequence: 4 (High)
- Risk Score: 12 (YELLOW)
- Mitigation: Implement checksums and rollback capability
```

### Workflow 4: Technical Review Preparation

**Goal:** Prepare for SRR, PDR, CDR, TRR, or FRR.

```
WORKFLOW:
---------

User: "Help me prepare for PDR"

[nse-reviewer activates]

1. Checks entrance criteria
2. Generates review package
3. Identifies gaps
4. Outputs recommendation

EXAMPLE OUTPUT:
---------------

PDR Readiness Assessment:

Entrance Criteria Check:
[PASS] SRR action items closed
[PASS] Requirements baseline approved
[WARN] Preliminary design 80% complete (3 items pending)
[PASS] Interface requirements defined
[FAIL] Preliminary ICDs not yet available

Recommendation: CONDITIONALLY READY
- Complete 3 pending design items
- Generate preliminary ICDs before review

RFAs to Address:
- RFA-001: Complete preliminary design for Module X
- RFA-002: Generate ICD for API interface
```

### Workflow 5: Trade Study

**Goal:** Make data-driven design decisions.

```
WORKFLOW:
---------

User: "Conduct trade study for database selection:
       PostgreSQL vs MongoDB vs DynamoDB"

[nse-architecture activates]

1. Defines criteria and weights
2. Scores alternatives
3. Provides recommendation

EXAMPLE OUTPUT:
---------------

Trade Study: Database Selection

Criteria (weighted):
- Performance (25%)
- Cost (20%)
- Scalability (20%)
- Team expertise (15%)
- Vendor support (10%)
- Integration ease (10%)

Scoring Matrix:
             | Postgres | MongoDB | DynamoDB |
Performance  |    4     |    3    |    5     |
Cost         |    5     |    3    |    2     |
Scalability  |    3     |    4    |    5     |
...

Recommendation: PostgreSQL
- Weighted Score: 4.1/5.0
- Rationale: Best balance of performance, cost, and team expertise
```

---

## Output Locations

All NASA SE artifacts are persisted:

```
projects/{PROJECT}/
|-- requirements/           # nse-requirements output
|   |-- requirements-spec.md
|   |-- traceability-matrix.md
|-- verification/           # nse-verification output
|   |-- vcrm.md
|   |-- test-plan.md
|   |-- test-results/
|-- risks/                  # nse-risk output
|   |-- risk-register.md
|   |-- risk-assessments/
|-- architecture/           # nse-architecture output
|   |-- trade-studies/
|   |-- design-docs/
|-- reviews/                # nse-reviewer output
|   |-- srr/
|   |-- pdr/
|   |-- cdr/
|-- interfaces/             # nse-integration output
|   |-- icds/
|   |-- interface-list.md
|-- configuration/          # nse-configuration output
|   |-- baselines/
|   |-- change-log.md
|-- reports/                # nse-reporter output
|   |-- dashboards/
|   |-- status-reports/
```

---

## Tips and Best Practices

### 1. Be Specific About Scope

```
Bad:  "Help with requirements"
Good: "Create performance requirements for the API response time"
```

### 2. Provide Domain Context

```
Bad:  "Assess risks"
Good: "Assess technical risks for migrating from MySQL to PostgreSQL,
       considering our 99.9% uptime requirement"
```

### 3. Request Appropriate Level

```
L0: "Give me a quick summary" (1 paragraph)
L1: "Full artifact please" (complete document)
L2: "Review-ready package" (comprehensive)
```

### 4. Iterate and Refine

```
Step 1: "Create initial requirements for auth"
Step 2: "Add security requirements to the auth spec"
Step 3: "Create VCRM for all auth requirements"
```

### 5. Maintain Traceability

```
Always link:
- Requirements -> Stakeholder needs
- Design -> Requirements
- Tests -> Requirements
- Risks -> Requirements or Design
```

---

## Troubleshooting

### "Requirements are too vague"

Make them measurable:

```
Bad:  "The system shall be fast"
Good: "The system shall respond within 100ms for 95% of requests"
```

### "Risk scores don't make sense"

Use the 5x5 matrix consistently:

```
Likelihood (1-5): How likely is this to happen?
Consequence (1-5): How bad would it be?
Score = L x C
  1-4:  GREEN (Accept)
  5-12: YELLOW (Mitigate)
  15-25: RED (Must address)
```

### "Review preparation is incomplete"

Check entrance criteria explicitly:

```
"List the entrance criteria for PDR and check each one"
```

---

# L2: Architecture & Constraints

> *This section documents what NOT to do, boundaries, invariants, and design rationale.*

## Anti-Pattern Catalog

### AP-001: AI as Authority

```
+===================================================================+
| ANTI-PATTERN: AI as Authority                                     |
+===================================================================+
|                                                                   |
| SYMPTOM:    AI-generated SE artifacts accepted without human      |
|             review. AI recommendations treated as authoritative.  |
|                                                                   |
| CAUSE:      Over-reliance on AI. Skipping human SME review.       |
|             Forgetting P-043 disclaimer requirement.              |
|                                                                   |
| IMPACT:     - Requirements may be incomplete or wrong             |
|             - Risks may be missed                                 |
|             - Verification gaps not caught                        |
|             - MISSION FAILURE if uncaught                         |
|                                                                   |
| FIX:        ALWAYS include P-043 disclaimer.                      |
|             ALWAYS require human SME review.                      |
|             AI is ADVISORY, never AUTHORITATIVE.                  |
|                                                                   |
+===================================================================+
```

**P-043 Disclaimer (REQUIRED on all nse-* outputs):**

```
*DISCLAIMER: This guidance is AI-generated based on NASA Systems
Engineering standards. It is advisory only and does not constitute
official NASA guidance. All SE decisions require human review and
professional engineering judgment. Not for use in mission-critical
decisions without SME validation.*
```

---

### AP-002: Skipping Review Gates

```
+===================================================================+
| ANTI-PATTERN: Skipping Review Gates                               |
+===================================================================+
|                                                                   |
| SYMPTOM:    Moving from PDR to CDR without closing RFAs.          |
|             "We'll fix it later." Entrance criteria not met.      |
|                                                                   |
| CAUSE:      Schedule pressure. "We know it works."                |
|             Not enforcing gate discipline.                        |
|                                                                   |
| IMPACT:     - Problems compound and become expensive              |
|             - Technical debt accumulates                          |
|             - Late discovery of fundamental issues                |
|             - Potential mission failure                           |
|                                                                   |
| FIX:        Gates are BLOCKING - no exceptions without waiver.    |
|             All entrance criteria must be GREEN to proceed.       |
|             All RFAs tracked to closure.                          |
|                                                                   |
+===================================================================+
```

**Review Gate Enforcement:**

```
GATE DISCIPLINE:
----------------

      [GATE]
         |
   +-----+-----+
   |           |
   v           v
 PASS         FAIL
   |           |
   v           v
PROCEED      STOP
             |
             v
         CLOSE RFAs
             |
             v
         RE-REVIEW
```

---

### AP-003: Orphan Requirements

```
+===================================================================+
| ANTI-PATTERN: Orphan Requirements                                 |
+===================================================================+
|                                                                   |
| SYMPTOM:    Requirements without traceability. No link to         |
|             stakeholder needs. No verification method defined.    |
|                                                                   |
| CAUSE:      Requirements created without traceability matrix.     |
|             VCRM not maintained. "We'll add traceability later."  |
|                                                                   |
| IMPACT:     - Can't prove requirements are necessary (gold plating)|
|             - Can't verify requirements are met                   |
|             - Changes break unknown dependencies                  |
|                                                                   |
| FIX:        Every requirement MUST have:                          |
|             1. Parent (stakeholder need or higher requirement)    |
|             2. Verification method (Test/Analysis/Demo/Inspect)   |
|             3. Rationale                                          |
|                                                                   |
+===================================================================+
```

**Traceability Enforcement:**

```
BIDIRECTIONAL TRACEABILITY:
---------------------------

Stakeholder Need
      |
      v (derives)
System Requirement
      |
      v (satisfies)
Design Element
      |
      v (verifies)
Test Case
```

---

### AP-004: Risk Blindness

```
+===================================================================+
| ANTI-PATTERN: Risk Blindness                                      |
+===================================================================+
|                                                                   |
| SYMPTOM:    Risk register empty or stale. "We don't have any      |
|             risks." Risks identified but no mitigation.           |
|                                                                   |
| CAUSE:      Risk management seen as bureaucracy. "Just build it." |
|             No risk owner assigned. Risks not reviewed regularly. |
|                                                                   |
| IMPACT:     - Risks become reality and surprise everyone          |
|             - No mitigation in place when risk occurs             |
|             - Cost/schedule overruns                              |
|                                                                   |
| FIX:        Risk register reviewed at every phase gate.           |
|             Every RED risk has owner and mitigation plan.         |
|             Risks scored using 5x5 matrix consistently.           |
|                                                                   |
+===================================================================+
```

---

## Constraints & Boundaries

### Hard Constraints (Cannot Violate)

| ID | Constraint | Rationale |
|----|------------|-----------|
| HC-001 | P-043 disclaimer on all nse-* outputs | AI is advisory, not authoritative |
| HC-002 | Requirements have bidirectional traceability | P-040 Jerry Constitution |
| HC-003 | All RED risks have mitigation plans | P-042 Risk transparency |
| HC-004 | Review gates have documented entrance/exit criteria | Gate discipline |
| HC-005 | Human SME review required for all SE artifacts | AI cannot replace engineering judgment |

### Soft Constraints (Should Not Violate)

| ID | Constraint | When to Relax |
|----|------------|---------------|
| SC-001 | Full L0/L1/L2 output for all artifacts | When user requests specific level |
| SC-002 | All requirements have rationale | For derived requirements with obvious parent |
| SC-003 | Complete VCRM before CDR | For incremental development with rolling baseline |

---

## Invariants

> *Conditions that must ALWAYS be true*

```
INVARIANT CHECKLIST:
--------------------

[X] INV-001: P-043 disclaimer present on all nse-* outputs
           Violation: AI mistaken for authority

[X] INV-002: Every requirement has verification method
           Violation: Can't prove requirement is met

[X] INV-003: Every RED risk has owner and mitigation
           Violation: Risk unmanaged

[X] INV-004: Review entrance criteria documented
           Violation: Gate discipline breaks down

[X] INV-005: Traceability is bidirectional
           Violation: Changes break unknown dependencies
```

---

## P-043 Disclaimer Placement

> *Where to put the disclaimer in outputs*

```
DISCLAIMER PLACEMENT:
---------------------

+-------------------------------------------+
|          nse-* Agent Output               |
|-------------------------------------------|
| # Document Title                          |
|                                           |
| ## L0: Executive Summary                  |
| [content]                                 |
|                                           |
| ## L1: Technical Details                  |
| [content]                                 |
|                                           |
| ## L2: Implications                       |
| [content]                                 |
|                                           |
| ---                                       |
| *DISCLAIMER: This guidance is AI-generated|
|  based on NASA Systems Engineering        |
|  standards. It is advisory only...*       |
|-------------------------------------------|
|           BOTTOM OF DOCUMENT              |
+-------------------------------------------+
```

**Disclaimer Text (P-043):**

```markdown
---

*DISCLAIMER: This guidance is AI-generated based on NASA Systems
Engineering standards. It is advisory only and does not constitute
official NASA guidance. All SE decisions require human review and
professional engineering judgment. Not for use in mission-critical
decisions without SME validation.*
```

---

## Cross-Skill Integration

### Handoff Points from Problem-Solving

```
CROSS-SKILL HANDOFF:
--------------------

  +----------------+                 +------------------+
  | ps-researcher  |---------------->| nse-requirements |
  | (research)     |  needs analysis | (shall statements)|
  +----------------+                 +------------------+

  +----------------+                 +------------------+
  | ps-architect   |---------------->| nse-architecture |
  | (decisions)    |  trade study    | (NASA format)    |
  +----------------+                 +------------------+

  +----------------+                 +------------------+
  | ps-analyst     |---------------->| nse-risk         |
  | (root cause)   |  risk input     | (5x5 scoring)    |
  +----------------+                 +------------------+
```

| Source Agent | Target Agent | Handoff Context |
|--------------|--------------|-----------------|
| `ps-researcher` | `nse-requirements` | Research to SHALL statements |
| `ps-architect` | `nse-architecture` | Design decisions to trade study |
| `ps-analyst` | `nse-risk` | Root cause to risk register |

---

## Design Rationale

### Why NASA SE Standards?

**Context:** NASA has 60+ years of systems engineering experience.

**Decision:** Base nse-* agents on NPR 7123.1D and SE Handbook.

**Consequences:**
- (+) Proven practices from successful missions
- (+) Rigorous approach catches problems early
- (+) Consistent with industry standards
- (-) Can be heavyweight for small projects
- (-) Requires domain knowledge to apply correctly

### Why Mandatory Disclaimer (P-043)?

**Context:** AI can generate plausible but incorrect SE guidance.

**Decision:** Every nse-* output must include disclaimer.

**Consequences:**
- (+) Users reminded AI is advisory
- (+) Legal protection
- (+) Encourages human review
- (-) Adds text to every output

### Why Review Gate Discipline?

**Context:** Skipping gates causes late discovery of problems.

**Decision:** Gates are blocking with documented entrance/exit criteria.

**Consequences:**
- (+) Problems caught early when cheap to fix
- (+) Clear go/no-go decisions
- (+) Documented rationale for proceeding
- (-) Can slow down progress if gate discipline is excessive

---

## References

- **NPR 7123.1D** - NASA SE Processes and Requirements
- **NASA/SP-2016-6105 Rev2** - NASA Systems Engineering Handbook
- **NPR 8000.4C** - Risk Management
- **INCOSE SE Handbook v5.0** - Industry standard

Internal References:
- [ORCHESTRATION_PATTERNS.md](../shared/ORCHESTRATION_PATTERNS.md) - 8 canonical patterns
- [AGENT_TEMPLATE_CORE.md](../shared/AGENT_TEMPLATE_CORE.md) - Agent definition format
- [Jerry Constitution](../../docs/governance/JERRY_CONSTITUTION.md) - P-040, P-041, P-042, P-043

---

## Quick Reference Card

| Task | Prompt |
|------|--------|
| Create requirements | `"Create requirements for [capability]"` |
| Assess risks | `"Identify risks for [system]"` |
| Score risks | `"Score risks using 5x5 matrix"` |
| Prepare for review | `"Help me prepare for [SRR/PDR/CDR/TRR/FRR]"` |
| Trade study | `"Conduct trade study for [decision]"` |
| Create ICD | `"Create ICD for [interface]"` |
| Verification status | `"Show VCRM for [requirements]"` |
| SE status report | `"Generate SE dashboard"` |

---

*Playbook Version: 2.0.0*
*Skill: nasa-se*
*Last Updated: 2026-01-12 - Triple-lens refactoring (SAO-INIT-007)*
*Template: PLAYBOOK_TEMPLATE.md v1.0.0*
