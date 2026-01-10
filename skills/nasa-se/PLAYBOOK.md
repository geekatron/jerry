# NASA Systems Engineering Skill Playbook

> User Guide for NASA SE Skill in Jerry Framework

---

## Quick Start

### Activation

The NASA SE skill activates on natural language prompts containing keywords like:
- "systems engineering", "NASA SE", "NPR 7123"
- "requirements", "verification", "risk management"
- "SRR", "PDR", "CDR", "FRR"
- "traceability", "VCRM", "trade study"

### First Steps

1. **Start a new SE effort:**
   ```
   "Help me set up systems engineering for my project"
   ```

2. **Get requirements help:**
   ```
   "Create a requirements specification for user authentication"
   ```

3. **Assess risks:**
   ```
   "Identify technical risks for the data processing module"
   ```

---

## Available Agents

| Agent | Purpose | Invoke With |
|-------|---------|-------------|
| `nse-requirements` | Requirements engineering | "requirements", "shall statement" |
| `nse-verification` | V&V, testing | "verification", "VCRM", "test" |
| `nse-risk` | Risk management | "risk", "mitigation", "5x5" |
| `nse-architecture` | System design | "architecture", "trade study" |
| `nse-reviewer` | Technical reviews | "SRR", "PDR", "CDR", "review" |
| `nse-integration` | System integration | "integration", "interface", "ICD" |
| `nse-configuration` | Config management | "baseline", "configuration", "change" |
| `nse-reporter` | Status reporting | "status report", "dashboard" |

---

## Common Workflows

### Workflow 1: New Project Setup

**Goal:** Initialize SE artifacts for a new project

**Steps:**
1. "Help me bootstrap SE for [project name]"
2. Agent creates:
   - Requirements specification template
   - Risk register
   - VCRM template
   - Interface list

**Example:**
```
User: Help me set up SE artifacts for my IoT sensor project

Agent: I'll initialize your SE baseline:
1. Creating requirements specification template
2. Setting up risk register with initial assessment
3. Creating VCRM template
4. Generating interface list template
```

---

### Workflow 2: Requirements Development

**Goal:** Develop and document requirements

**Steps:**
1. "I need requirements for [capability]"
2. Review generated requirements
3. Refine and add attributes
4. "Create traceability matrix"

**Example:**
```
User: Create requirements for secure user authentication

Agent: Here are the derived requirements:

REQ-AUTH-001: The system SHALL authenticate users via username/password.
- Priority: 1 (Critical)
- Verification: Test
- Rationale: Basic access control

REQ-AUTH-002: The system SHALL lock accounts after 5 failed attempts.
- Priority: 2 (High)
- Verification: Test
- Rationale: Brute force protection
...
```

**Best Practices:**
- Start with stakeholder needs ("users need to...")
- Let agent derive SHALL statements
- Review for measurability
- Add rationale for each requirement

---

### Workflow 3: Risk Assessment

**Goal:** Identify and score risks

**Steps:**
1. "Identify risks for [system/feature]"
2. Review identified risks
3. "Score these risks using 5x5 matrix"
4. "Create mitigation plans for RED risks"

**Example:**
```
User: What are the technical risks for the database migration?

Agent: Identified risks:

R-001: Data Corruption During Migration
- IF data validation fails during migration,
- THEN records may be corrupted,
- resulting in data integrity issues.
- Likelihood: 3 (Moderate)
- Consequence: 4 (High)
- Score: 12 (YELLOW)

R-002: Extended Downtime
...
```

**Best Practices:**
- Be specific about the system context
- Request If-Then format for statements
- Ensure all RED risks have mitigations
- Track risks over time

---

### Workflow 4: Technical Review Preparation

**Goal:** Prepare for SRR, PDR, CDR, or FRR

**Steps:**
1. "Help me prepare for [review type]"
2. Agent checks entrance criteria
3. Generates review package
4. Identifies gaps

**Example:**
```
User: Help me prepare for PDR

Agent: PDR Readiness Assessment:

Entrance Criteria Check:
✅ SRR action items closed
✅ Requirements baseline approved
⚠️ Preliminary design 80% complete (3 items pending)
✅ Interface requirements defined
❌ Preliminary ICDs not yet available

Recommendation: CONDITIONALLY READY
- Complete 3 pending design items
- Generate preliminary ICDs before review

Shall I help address these gaps?
```

**Best Practices:**
- Start preparation early
- Use entrance criteria checklist
- Address all RED criteria before review
- Document RFAs and track to closure

---

### Workflow 5: Trade Study

**Goal:** Make data-driven design decisions

**Steps:**
1. "Conduct trade study for [decision]"
2. Define criteria and weights
3. Score alternatives
4. Review recommendation

**Example:**
```
User: Trade study for database selection: PostgreSQL vs MongoDB vs DynamoDB

Agent: Trade Study: Database Selection

Criteria (weighted):
- Performance (25%)
- Cost (20%)
- Scalability (20%)
- Team expertise (15%)
- Vendor support (10%)
- Integration ease (10%)

[Scoring matrix provided]

Recommendation: PostgreSQL
- Score: 4.1/5.0
- Rationale: Best balance of performance, cost, and team expertise
```

**Best Practices:**
- Define criteria before evaluating
- Weight criteria by importance
- Score objectively with evidence
- Document assumptions

---

### Workflow 6: Status Reporting

**Goal:** Generate SE status reports

**Steps:**
1. "Generate SE status report"
2. Specify level (L0 summary, L1 full, L2 review package)
3. Review and distribute

**Example:**
```
User: Generate an executive dashboard for this sprint

Agent: SE Executive Dashboard

Overall Status: 🟡 YELLOW

| Domain | Status | Key Metric |
|--------|--------|------------|
| Requirements | 🟢 | 100% approved |
| Verification | 🟡 | 75% complete |
| Risk | 🟢 | 0 RED risks |

Top Issue: Verification behind schedule (5 tests pending)
Recommended Action: Prioritize critical path tests
```

---

## Tips and Best Practices

### 1. Be Specific
- ❌ "Help with requirements"
- ✅ "Create performance requirements for the API response time"

### 2. Provide Context
- ❌ "Assess risks"
- ✅ "Assess technical risks for migrating from MySQL to PostgreSQL"

### 3. Request Appropriate Level
- L0: Quick summary (1 paragraph)
- L1: Full artifact (complete document)
- L2: Review-ready package (comprehensive)

### 4. Iterate
- Start with initial output
- Refine with follow-up prompts
- Build up artifacts incrementally

### 5. Maintain Traceability
- Always link requirements to stakeholder needs
- Link design to requirements
- Link tests to requirements

---

## Output Locations

All artifacts are persisted to your project directory:

```
projects/{PROJECT}/
├── requirements/          # Requirements specs, traceability
├── verification/          # VCRM, test plans, results
├── risks/                 # Risk register, assessments
├── architecture/          # Design docs, trade studies
├── reviews/               # Review packages, checklists
├── interfaces/            # ICDs, N² diagrams
├── configuration/         # CI lists, baselines
└── reports/               # Status reports, dashboards
```

---

## Integration with Jerry

### Work Tracker
SE activities create Work Tracker items:
- Requirements → `task` items
- Risks → `issue` items for RED risks
- Review actions → `action-item` items

### Problem-Solving
NSE agents receive handoffs from Problem-Solving agents:
- ps-analyst → nse-risk (for risk assessment)
- ps-researcher → nse-requirements (for needs analysis)

### Constitutional Compliance
All outputs comply with:
- **P-040:** Bidirectional traceability
- **P-041:** Verification coverage
- **P-042:** Risk transparency
- **P-043:** AI guidance disclaimer

---

## Disclaimer

All NSE agent outputs include the following disclaimer:

> *DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
> standards. It is advisory only and does not constitute official NASA guidance.
> All SE decisions require human review and professional engineering judgment.
> Not for use in mission-critical decisions without SME validation.*

---

## Quick Reference Card

| Task | Prompt |
|------|--------|
| Create requirements | "Create requirements for [feature]" |
| Assess risks | "Identify risks for [system]" |
| Prepare for review | "Help me prepare for [PDR/CDR/etc]" |
| Trade study | "Compare options for [decision]" |
| Status report | "Generate SE status report" |
| Interface doc | "Create ICD for [interface]" |
| Traceability | "Show traceability for [requirement]" |
| Risk mitigation | "Create mitigation plan for [risk]" |

---

## References

- NPR 7123.1D: NASA SE Processes and Requirements
- NASA/SP-2016-6105 Rev2: NASA SE Handbook
- NPR 8000.4C: Risk Management
- INCOSE SE Handbook v5.0

---

*Playbook Version: 1.0.0*
*Last Updated: 2026-01-09*
