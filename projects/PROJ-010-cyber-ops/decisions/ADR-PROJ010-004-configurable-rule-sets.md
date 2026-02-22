# ADR-PROJ010-004: Configurable Rule Set Architecture -- YAML-First with Profile Management

<!--
DOCUMENT-ID: FEAT-013:EN-116
AUTHOR: ps-architect agent
DATE: 2026-02-22
STATUS: PROPOSED
PARENT: EN-116 (ADR: Configurable Rule Sets)
FEATURE: FEAT-013 (Configurable Rule Set Architecture)
EPIC: EPIC-002 (Architecture & Design)
PROJECT: PROJ-010-cyber-ops
ADR-ID: ADR-PROJ010-004
TYPE: Architecture Decision Record
-->

> **ADR ID:** ADR-PROJ010-004
> **Version:** 1.0.0
> **Date:** 2026-02-22
> **Author:** ps-architect
> **Status:** PROPOSED
> **Deciders:** User (P-020 authority), ps-architect (recommendation)
> **Quality Target:** >= 0.95
> **Parent Feature:** FEAT-013 (Configurable Rule Set Architecture)
> **Parent Epic:** EPIC-002 (Architecture & Design)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Status](#status) | Current decision lifecycle stage and approval state |
| [Context](#context) | Why this decision is needed, background research, and governing constraints |
| [Decision](#decision) | The 8-component architecture: rule schema, directory structure, profiles, cascading overrides, defaults, scope enforcement, testing, and agent binding |
| [Options Considered](#options-considered) | Five rule definition format options evaluated with trade-off analysis |
| [Consequences](#consequences) | Positive, negative, and neutral outcomes with impact assessments |
| [Evidence Base](#evidence-base) | Summary of research findings from F-003, B-003, S-001, S-002 |
| [Compliance](#compliance) | R-011 satisfaction, PLAN.md requirements traceability, and governance alignment |
| [Related Decisions](#related-decisions) | Upstream architecture decisions and downstream feature dependencies |
| [References](#references) | Source citations organized by evidence category |

---

## Status

**PROPOSED** -- This ADR awaits adversarial review and user ratification.

**Required governance steps before acceptance:**

1. **C4 /adversary review** per R-013: Quality threshold >= 0.95, up to 5 creator-critic-revision iterations
2. **User ratification** per P-020 (User Authority)

**Downstream dependency:** This ADR, once accepted, unblocks EN-113 (Rule Set Schema & Directory Structure), EN-114 (Override Mechanism Design), and EN-115 (Default Rule Set Specification) for detailed implementation design.

---

## Context

### Why This Decision Is Needed

PLAN.md requirement R-011 mandates: "Both skills MUST support user-provided rule sets and content for practices, standards, and methodologies. Users MUST be able to override default rules (e.g., substitute OWASP with org-specific standards) without modifying core skill code." Without a formalized rule set architecture, /eng-team and /red-team would ship with hardcoded standards that cannot adapt to organizational diversity, making the skills unusable for organizations with proprietary or regulatory-specific requirements.

### Background

Phase 1 research produced four artifacts directly informing this decision:

**F-003 (Configurable Rule Set Research)** analyzed five production rule and policy configuration systems -- Semgrep (YAML-based SAST rules), OPA/Rego (general-purpose policy engine), SonarQube (quality profile system), Checkov (infrastructure-as-code policies), and ESLint (JavaScript/TypeScript linting) -- to identify convergent patterns for rule definition, profile management, and override mechanisms. All five tools converge on a common architecture: default rules provided by the platform, user overrides through a documented mechanism, per-project configuration, and the ability to disable specific rules (F-003, Finding 6).

**B-003 (OWASP, NIST, CIS, SANS Standards Analysis)** mapped the defensive standards landscape to /eng-team agent responsibilities and identified OWASP ASVS 5.0's 3-level assurance model (Level 1 baseline, Level 2 standard, Level 3 high-assurance) as the natural configuration axis for rule set selection. B-003 also mapped per-agent standard bindings: OWASP for eng-backend/eng-frontend, NIST for eng-architect/eng-lead, CIS for eng-infra, and CWE/SANS for eng-security.

**S-002 (Architecture Implications Synthesis)** formalized this as AD-007 (YAML-First Configurable Rule Sets with Profile Management), one of 12 architecture decisions Phase 2 must codify. S-002 identified four cross-cutting integration concerns: agent-to-rule-set binding, routing context affected by rule configuration, scope enforcement policy format consistency, and default rule set overridability.

**S-001 (Cross-Stream Findings)** documented Convergence 4 (Configurable Rule Sets as the Compliance Architecture): streams B, F, and A independently concluded that configurable rule sets are the correct compliance architecture, not a dedicated compliance agent. This convergence contributed to the deferral of eng-compliance in A-004, validated by the finding that "compliance requirements vary radically by regulatory environment; configurable rule sets (R-011) are a better fit than a static agent."

### Constraints

| Constraint | Source | Impact on Architecture |
|------------|--------|----------------------|
| **R-011: Configurable Rule Sets** | PLAN.md | Users MUST override defaults without modifying core skill code; this is the primary requirement this ADR satisfies |
| **R-013: C4 /adversary review** | PLAN.md | This ADR and all phase deliverables must pass >= 0.95 quality threshold |
| **AD-001: Methodology-First Design** | S-002 | Rules define methodology guidance parameters, not autonomous execution behavior; rules govern what agents advise, not what they execute |
| **AD-007: YAML-First Rule Sets** | S-002 | Phase 1 research converged on YAML-first with Python escape hatch; this ADR formalizes that decision with full specification |
| **Convergence 5: Structured Data Formats** | S-001 | JSON Schema for definitions, SARIF for findings, YAML for configuration -- rule sets use YAML as part of this unified data interchange layer |
| **P-003: No Recursive Subagents** | Jerry Constitution | Rule evaluation must operate within the orchestrator-worker pattern; no nested agent spawning for policy evaluation |
| **Git-based versioning** | F-003 R-RULES-007 | Rules stored in version-controlled directories; engagements pin to specific versions for reproducibility |

---

## Decision

The configurable rule set architecture consists of eight components that together satisfy R-011. Each component is specified below with its design rationale and evidence basis.

### Component 1: YAML-First Rule Definition Format

Rules are defined in YAML using a Semgrep-inspired structured schema. YAML is the primary format because it is: structured and schema-validatable, human-readable without programming language expertise, version-controllable in Git, and familiar to security practitioners who work with Semgrep, Checkov, and similar tools (F-003, Finding 1).

**Standard Rule Schema (shared by /eng-team and /red-team):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier using dot-separated namespace (e.g., `eng.owasp.a01.broken-access-control`, `red.attack.ta0001.phishing`) |
| `name` | string | Yes | Human-readable rule name |
| `version` | string | Yes | Semantic version of the rule definition (e.g., `1.0.0`) |
| `category` | enum | Yes | `security`, `architecture`, `coding`, `testing`, `engagement`, `methodology`, `compliance`, `infrastructure` |
| `severity` | enum | Yes | `critical`, `high`, `medium`, `low`, `info` |
| `description` | string | Yes | What the rule checks or enforces |
| `rationale` | string | Yes | Why the rule exists; connects to business or security value |
| `references` | array[object] | Yes | Standards references (CWE, OWASP, ATT&CK, NIST, CIS) with `type`, `id`, and `url` fields |
| `default` | enum | Yes | `enabled` or `disabled` -- initial activation state |
| `configurable_params` | object | No | Rule-specific tunable parameters with `name`, `type`, `default`, `description`, and optional `allowed_values` per parameter |
| `applicable_agents` | array[string] | No | Agent identifiers this rule applies to (e.g., `["eng-backend", "eng-frontend"]`); if omitted, applies to all agents in the skill |
| `tags` | array[string] | No | Custom tags for filtering and grouping (e.g., `["pci-dss", "hipaa", "authentication"]`) |
| `metadata` | object | No | Arbitrary key-value metadata for organizational extension |

**Example Rule Definition:**

```yaml
# rules/eng-team/security/eng-owasp-a01-access-control-verification.yaml
id: eng.owasp.a01.access-control-verification
name: Broken Access Control Verification
version: 1.0.0
category: security
severity: critical
description: >
  Verify that access control mechanisms enforce the principle of least privilege
  and that every endpoint, API route, and resource access point has explicit
  authorization checks. Covers OWASP Top 10 2025 A01 (Broken Access Control).
rationale: >
  Broken Access Control has been the #1 OWASP Top 10 category since 2021,
  maintaining that position in 2025. CWE-862 (Missing Authorization) jumped
  5 positions to #4 in the 2025 CWE Top 25, confirming that missing authorization
  checks are a persistent and growing weakness.
references:
  - type: owasp-top-10
    id: "A01:2025"
    url: "https://owasp.org/Top10/2025/"
  - type: cwe
    id: CWE-862
    url: "https://cwe.mitre.org/data/definitions/862.html"
  - type: cwe
    id: CWE-284
    url: "https://cwe.mitre.org/data/definitions/284.html"
  - type: asvs
    id: "V4"
    url: "https://owasp.org/www-project-application-security-verification-standard/"
default: enabled
configurable_params:
  asvs_level:
    type: integer
    default: 2
    description: "OWASP ASVS assurance level (1=baseline, 2=standard, 3=high-assurance)"
    allowed_values: [1, 2, 3]
  include_rbac_review:
    type: boolean
    default: true
    description: "Include role-based access control architecture review"
  max_unprotected_endpoints:
    type: integer
    default: 0
    description: "Maximum number of endpoints permitted without explicit authorization (0 = zero tolerance)"
applicable_agents:
  - eng-backend
  - eng-frontend
  - eng-security
  - eng-reviewer
tags:
  - owasp-top-10
  - access-control
  - authorization
  - asvs-v4
```

**Example /red-team Rule Definition:**

```yaml
# rules/red-team/methodology/red-attack-ta0001-initial-access.yaml
id: red.attack.ta0001.initial-access
name: Initial Access Technique Coverage
version: 1.0.0
category: methodology
severity: high
description: >
  Ensure initial access phase covers authorized techniques from MITRE ATT&CK
  tactic TA0001. Verify technique selection is justified by reconnaissance
  findings and constrained by engagement scope.
rationale: >
  Initial access is the entry point for all offensive engagements. Technique
  selection must be driven by reconnaissance intelligence and bounded by
  scope authorization to ensure engagement quality and legal compliance.
references:
  - type: mitre-attack
    id: TA0001
    url: "https://attack.mitre.org/tactics/TA0001/"
  - type: ptes
    id: "exploitation"
    url: "http://www.pentest-standard.org/index.php/Exploitation"
default: enabled
configurable_params:
  required_technique_justification:
    type: boolean
    default: true
    description: "Require written justification for each selected technique"
  min_techniques_attempted:
    type: integer
    default: 3
    description: "Minimum number of initial access techniques to attempt before concluding"
  scope_validation_mode:
    type: string
    default: "strict"
    description: "Scope validation strictness for technique authorization"
    allowed_values: ["strict", "standard", "permissive"]
applicable_agents:
  - red-exploit
  - red-lead
tags:
  - mitre-attack
  - initial-access
  - ptes
```

### Component 2: Python Escape Hatch for Complex Rules

Following Checkov's dual-format pattern (F-003, Finding 4), rules that cannot be expressed declaratively in YAML use Python for complex logic. YAML handles the majority of rules: attribute checks, threshold comparisons, standard validations, and methodology checklists. Python handles the minority requiring: multi-step validation across multiple rule outputs, dynamic computation based on engagement context, cross-rule dependency evaluation, and conditional logic chains exceeding declarative expressiveness.

**Python Rule Interface:**

```python
# rules/eng-team/architecture/eng_arch_dependency_cycle_detection.py
from cyberops.rules import Rule, RuleResult, RuleContext

class DependencyCycleDetection(Rule):
    """Detect circular dependency patterns in architecture designs.

    YAML cannot express graph traversal logic. This rule analyzes
    component dependency declarations to identify cycles that indicate
    architectural coupling violations.
    """

    id = "eng.architecture.dependency-cycle-detection"
    name = "Dependency Cycle Detection"
    version = "1.0.0"
    category = "architecture"
    severity = "high"
    default = "enabled"

    configurable_params = {
        "max_cycle_length": {
            "type": "integer",
            "default": 3,
            "description": "Maximum cycle length to report (longer cycles are less actionable)"
        },
        "ignore_weak_dependencies": {
            "type": "boolean",
            "default": False,
            "description": "Exclude optional/weak dependencies from cycle detection"
        }
    }

    def evaluate(self, context: RuleContext) -> RuleResult:
        """Evaluate the rule against the provided context."""
        # Complex graph traversal logic here
        ...
```

**Format Selection Criteria:**

| Criterion | Use YAML | Use Python |
|-----------|----------|------------|
| Single attribute or threshold check | Yes | No |
| Standard reference validation | Yes | No |
| Methodology checklist enforcement | Yes | No |
| Pattern matching against known patterns | Yes | No |
| Multi-step validation with state | No | Yes |
| Graph traversal or topological analysis | No | Yes |
| Dynamic computation based on engagement metadata | No | Yes |
| Cross-rule dependency evaluation | No | Yes |

Both formats produce the same `RuleResult` output structure, ensuring uniform downstream processing regardless of rule implementation format. Both formats share the same schema fields (id, category, severity, configurable_params, etc.) -- the Python class mirrors the YAML schema.

### Component 3: Rule Directory Structure

Rules are organized in a hierarchical directory structure within the skill or project repository, following Git-based versioning (F-003, R-RULES-007).

```
rules/
├── schema/
│   └── rule-schema.json              # JSON Schema for YAML rule validation
├── eng-team/
│   ├── security/
│   │   ├── eng-owasp-a01-access-control-verification.yaml
│   │   ├── eng-owasp-a02-security-misconfiguration.yaml
│   │   ├── eng-owasp-a03-supply-chain.yaml
│   │   ├── eng-owasp-a04-cryptographic-failures.yaml
│   │   ├── eng-owasp-a05-injection.yaml
│   │   ├── eng-owasp-a06-insecure-design.yaml
│   │   ├── eng-owasp-a07-authentication-failures.yaml
│   │   ├── eng-owasp-a08-integrity-failures.yaml
│   │   ├── eng-owasp-a09-logging-failures.yaml
│   │   ├── eng-owasp-a10-error-handling.yaml
│   │   ├── eng-cwe-top25-*.yaml          # CWE Top 25 2025 rules
│   │   └── eng-asvs-v*.yaml              # ASVS 5.0 chapter rules
│   ├── architecture/
│   │   ├── eng-nist-csf-*.yaml            # NIST CSF 2.0 function rules
│   │   ├── eng-ssdf-*.yaml                # NIST SSDF practice rules
│   │   └── eng_arch_dependency_cycle_detection.py  # Complex Python rule
│   ├── infrastructure/
│   │   ├── eng-cis-*.yaml                 # CIS Benchmark rules
│   │   └── eng-slsa-*.yaml                # SLSA build level rules
│   ├── coding/
│   │   └── eng-coding-*.yaml              # Secure coding practice rules
│   └── testing/
│       └── eng-testing-*.yaml             # Security testing rules
├── red-team/
│   ├── methodology/
│   │   ├── red-attack-*.yaml              # MITRE ATT&CK tactic/technique rules
│   │   ├── red-ptes-*.yaml                # PTES phase rules
│   │   ├── red-osstmm-*.yaml             # OSSTMM channel rules
│   │   └── red-owasp-testing-*.yaml       # OWASP Testing Guide rules
│   ├── engagement/
│   │   ├── red-scope-*.yaml               # Scope enforcement policy rules
│   │   └── red-roe-*.yaml                 # Rules of engagement enforcement
│   └── reporting/
│       └── red-reporting-*.yaml           # Report quality and completeness rules
├── profiles/
│   ├── eng-team/
│   │   ├── owasp-asvs-l1.yaml            # ASVS Level 1 (baseline)
│   │   ├── owasp-asvs-l2.yaml            # ASVS Level 2 (standard default)
│   │   ├── owasp-asvs-l3.yaml            # ASVS Level 3 (high-assurance)
│   │   ├── nist-ssdf-minimum.yaml         # NIST SSDF minimum compliance
│   │   ├── cis-level1.yaml                # CIS Level 1 (essential)
│   │   └── cis-level2.yaml                # CIS Level 2 (defense in depth)
│   └── red-team/
│       ├── ptes-standard.yaml             # PTES Standard engagement profile
│       ├── attack-full-scope.yaml         # Full ATT&CK tactic coverage
│       ├── attack-external-only.yaml      # External-only (no post-exploitation)
│       └── osstmm-standard.yaml           # OSSTMM standard methodology
├── tests/
│   ├── eng-team/
│   │   └── test_eng_owasp_a01.yaml        # Rule test definitions
│   └── red-team/
│       └── test_red_attack_ta0001.yaml
└── overrides/
    └── .gitkeep                            # User/org overrides placed here
```

**Naming Conventions:**

| Element | Convention | Example |
|---------|------------|---------|
| Rule file (YAML) | `{skill}-{standard}-{identifier}.yaml` | `eng-owasp-a01-access-control-verification.yaml` |
| Rule file (Python) | `{skill}_{category}_{identifier}.py` | `eng_arch_dependency_cycle_detection.py` |
| Rule ID | `{skill}.{category}.{standard}.{identifier}` | `eng.owasp.a01.access-control-verification` |
| Profile file | `{standard}-{level-or-variant}.yaml` | `owasp-asvs-l2.yaml` |
| Test file | `test_{rule_file_stem}.yaml` | `test_eng_owasp_a01.yaml` |

**Version Control:** Rule sets are tagged at release points (e.g., `rules-v1.0.0`). Engagements pin to a specific rule set version in their engagement configuration. This enables reproducible engagements: the same engagement re-run against the same rule set version produces the same rule evaluation, and difference analysis between versions identifies precisely which rules changed.

### Component 4: Profile Management System

The profile management system follows SonarQube's inheritance model (F-003, Finding 3), adapted for the /eng-team and /red-team context. Profiles are the mechanism for associating rule sets with engagements.

**Profile Schema:**

```yaml
# profiles/eng-team/owasp-asvs-l2.yaml
id: eng.profile.owasp-asvs-l2
name: "OWASP ASVS Level 2 (Standard)"
version: 1.0.0
description: >
  Standard application security profile for applications handling
  sensitive data. Enables ~250 ASVS verification requirements at
  Level 2 assurance. Recommended default for most engagements.
skill: eng-team
extends: null  # Base profile; does not inherit from another profile
rules:
  # Enable rules with specific parameter overrides
  eng.owasp.a01.access-control-verification:
    enabled: true
    severity: critical  # Override severity if needed
    params:
      asvs_level: 2
      include_rbac_review: true
      max_unprotected_endpoints: 0
  eng.owasp.a05.injection:
    enabled: true
    params:
      check_parameterized_queries: true
      check_orm_injection: true
  eng.cwe.cwe-079-xss:
    enabled: true
    params:
      output_encoding_required: true
      csp_header_required: true
  # Disable rules not applicable at Level 2
  eng.asvs.v17.webrtc:
    enabled: false  # WebRTC rules only required at ASVS Level 3
tags:
  - owasp
  - asvs
  - level-2
  - standard
```

**Profile Extension (Inheritance):**

```yaml
# overrides/acme-corp/profiles/acme-standard.yaml
id: org.acme.profile.standard
name: "Acme Corp Standard Security Profile"
version: 1.0.0
description: >
  Extends OWASP ASVS Level 2 with Acme Corp-specific requirements
  including PCI DSS controls and internal coding standards.
skill: eng-team
extends: eng.profile.owasp-asvs-l2  # Inherits all L2 rules; adds/overrides below
rules:
  # Add organization-specific rules
  org.acme.pci-dss.cardholder-data-encryption:
    enabled: true
    severity: critical
    params:
      encryption_algorithm: "AES-256-GCM"
      key_rotation_days: 90
  # Override a default rule parameter
  eng.owasp.a01.access-control-verification:
    params:
      max_unprotected_endpoints: 0  # Acme enforces zero tolerance (same as default, explicit)
      include_rbac_review: true
  # Disable a default rule (with justification)
  eng.owasp.a03.supply-chain:
    enabled: false
    justification: "Acme uses proprietary supply chain validation system; external check redundant"
```

**Profile Management Operations:**

| Operation | Description | SonarQube Equivalent |
|-----------|-------------|---------------------|
| **Extend** | Child profile inherits parent rules; adds and overrides; parent changes propagate to child | Profile Extension |
| **Copy** | Independent copy of a profile; no inheritance relationship; changes to source do not propagate | Profile Copy |
| **Assign** | Associate a profile with an engagement; each engagement uses exactly one profile per skill | Per-Project Assignment |
| **Compare** | Diff two profiles to see added, removed, and modified rules | Profile Comparison |
| **Export/Import** | Serialize profile to portable YAML; import into another installation | Profile Backup/Restore |

**Profile Inheritance Model:**

```
Skill Default (built-in)
├── OWASP ASVS L2 (standard profile)
│   ├── Acme Corp Standard (org extension -- adds PCI DSS, internal rules)
│   │   ├── Acme Team Alpha (team extension -- adds team-specific overrides)
│   │   └── Acme Team Beta (team extension -- different team overrides)
│   └── HealthCo Standard (org extension -- adds HIPAA rules)
├── OWASP ASVS L1 (baseline profile)
│   └── StartupCo Lean (org extension -- minimal overhead)
└── OWASP ASVS L3 (high-assurance profile)
    └── GovCo Critical (org extension -- adds NIST 800-53 HIGH baseline)
```

Changes to the OWASP ASVS L2 profile propagate to all child profiles (Acme Corp, HealthCo, and their children). Changes to Acme Corp Standard propagate to Team Alpha and Team Beta. This dynamic propagation is a key differentiator from static profile copying -- it ensures that security standard updates flow through the hierarchy without manual propagation.

### Component 5: Five-Layer Cascading Override Mechanism

Rule resolution follows a cascading override pattern inspired by ESLint flat config (F-003, Finding 5), where later layers override earlier layers with deterministic precedence.

**Override Layers:**

| Layer | Priority | Source | Description | Example |
|-------|----------|--------|-------------|---------|
| L1 | Lowest | Skill defaults | Rules built into /eng-team or /red-team skill code | OWASP ASVS L2 rules enabled by default |
| L2 | Low | Organization profile | Shared across the organization; set by security leadership | Acme Corp adds PCI DSS rules |
| L3 | Medium | Team/project profile | Per-team customization within organizational constraints | Team Alpha disables WebRTC rules (not applicable) |
| L4 | High | Engagement overrides | Per-engagement configuration in the engagement YAML | This engagement uses ASVS L3 instead of L2 |
| L5 | Highest | Runtime flags | Command-line or environment variable overrides | `--rule-override eng.owasp.a01.access-control-verification.params.asvs_level=3` |

**Precedence Rules:**

1. **Last writer wins:** When the same rule field is defined at multiple layers, the highest-priority layer's value takes effect.
2. **Merge for additive fields:** Array fields (`tags`, `applicable_agents`) merge across layers; scalar fields (`severity`, `enabled`, parameter values) replace.
3. **Explicit disable overrides enable:** Setting `enabled: false` at any layer disables the rule regardless of lower layers, unless a higher layer re-enables it.
4. **Justification required for disable:** Disabling a `critical`-severity rule at L2, L3, or L4 requires a `justification` field documenting why the rule is disabled. This is enforced by schema validation, not by the override mechanism itself.
5. **Runtime flags are ephemeral:** L5 overrides are not persisted; they apply only to the current execution. They exist for debugging, experimentation, and CI-specific configuration.
6. **Inheritance resolution precedes cascade:** Within a single layer (e.g., L2), profile inheritance (extends) is resolved first, producing a flat rule set. The cascade then applies across layers.

**Resolution Algorithm:**

```
1. Load skill default rules (L1) -> base rule set
2. Resolve organization profile inheritance chain -> org rule set
3. Merge org rule set onto base (L2 overrides L1) -> merged
4. Resolve team/project profile inheritance chain -> team rule set
5. Merge team rule set onto merged (L3 overrides L2) -> merged
6. Apply engagement overrides (L4 overrides L3) -> merged
7. Apply runtime flags (L5 overrides L4) -> final active rule set
```

**Conflict Resolution Example:**

| Rule Field | L1 (Skill Default) | L2 (Org Profile) | L3 (Team Profile) | L4 (Engagement) | Resolved Value |
|------------|--------------------|--------------------|---------------------|-------------------|----------------|
| `severity` | `high` | `critical` | -- | -- | `critical` (L2 wins) |
| `enabled` | `true` | `true` | `false` | -- | `false` (L3 wins) |
| `params.asvs_level` | `2` | -- | -- | `3` | `3` (L4 wins) |
| `tags` | `["owasp"]` | `["pci-dss"]` | `["team-alpha"]` | -- | `["owasp", "pci-dss", "team-alpha"]` (merged) |

### Component 6: Default Rule Sets

Both skills ship with comprehensive default rule sets mapped to established security standards. These defaults provide a production-ready starting point while the override mechanism enables full customization per R-011.

#### /eng-team Default Rule Sets

| Standard | Coverage | Primary Agents | Profile Mapping |
|----------|----------|----------------|-----------------|
| **OWASP ASVS 5.0** | ~350 verification requirements across 17 chapters at 3 assurance levels (L1 baseline, L2 standard, L3 high-assurance) | eng-backend (V2, V4, V5, V6, V7, V8, V10, V13, V15), eng-frontend (V3, V5, V11, V17), eng-infra (V11, V14, V16), eng-security (all chapters) | `owasp-asvs-l1.yaml`, `owasp-asvs-l2.yaml`, `owasp-asvs-l3.yaml` |
| **OWASP Top 10 2025** | 10 risk categories: A01 Broken Access Control through A10 Mishandling of Exceptional Conditions | eng-backend (A01, A05, A07, A10), eng-frontend (A01, A05, A07), eng-infra (A02, A03, A08), eng-architect (A06, A02), eng-security (all) | Included in all ASVS profiles as awareness baseline |
| **CWE Top 25 2025** | 25 most dangerous software weaknesses based on 39,000+ CVEs (December 2025) | eng-security (all 25), eng-backend (CWE-79, -89, -352, -862, -78, -22, -20, -798, -918, -287, -434, -502, -284, -863, -269, -94, -770), eng-frontend (CWE-79, -352, -20) | Included in all ASVS profiles as code review focus list |
| **CIS Benchmarks** | 100+ configuration guides across 8 technology categories; Level 1 (essential) and Level 2 (defense in depth) | eng-infra (primary), eng-backend (database and application server benchmarks), eng-architect (cloud platform benchmarks) | `cis-level1.yaml`, `cis-level2.yaml` |
| **NIST SP 800-218 SSDF** | 4 practice groups (Prepare, Protect, Produce, Respond) with outcome-based secure development practices | eng-lead (PO), eng-architect (PW.1, PW.2), eng-backend/eng-frontend (PW.4, PW.5, PW.6, PW.9), eng-infra (PS, PO.5), eng-security (PW.7, PW.8, RV) | `nist-ssdf-minimum.yaml` |
| **NIST CSF 2.0** | 6 core functions (Govern, Identify, Protect, Detect, Respond, Recover) | eng-architect (Govern, Identify), eng-lead (Govern), all implementation agents (Protect), eng-security (Detect, Respond), eng-infra (Recover) | Referenced within SSDF profile |

#### /red-team Default Rule Sets

| Standard | Coverage | Primary Agents | Profile Mapping |
|----------|----------|----------------|-----------------|
| **MITRE ATT&CK** | 14 tactics with technique selections; 21 agents achieve 14/14 tactic coverage at STRONG level | red-recon (TA0043), red-exploit (TA0001, TA0002, TA0040), red-privesc (TA0004, TA0006), red-lateral (TA0008, TA0007), red-persist (TA0003, TA0005), red-exfil (TA0009, TA0010), red-infra (TA0042, TA0011, TA0005), red-social (TA0043 social, TA0001 phishing) | `attack-full-scope.yaml`, `attack-external-only.yaml` |
| **PTES** | 7 phases: Pre-engagement, Intelligence Gathering, Threat Modeling, Vulnerability Analysis, Exploitation, Post-Exploitation, Reporting | All /red-team agents mapped to PTES phases | `ptes-standard.yaml` |
| **OSSTMM** | 5 channels: Human Security, Physical Security, Wireless Communications, Telecommunications, Data Networks | Applicable /red-team agents per channel | `osstmm-standard.yaml` |
| **OWASP Testing Guide** | Test categories covering web application security testing methodology | red-vuln, red-exploit (web application contexts) | Referenced within PTES and ATT&CK profiles |

### Component 7: Scope Enforcement Policies (/red-team)

/red-team scope enforcement policies follow OPA/Rego architectural patterns (F-003, Finding 2; S-002 AD-004) but use a YAML surface for consistency with the rest of the rule set architecture. The architectural principle from OPA is preserved: policy evaluation is decoupled from enforcement.

**Architecture:**

| Component | Function | OPA Equivalent |
|-----------|----------|----------------|
| **Policy Rules** (YAML) | Define what actions are permitted, denied, or require escalation | Rego policies |
| **Input Document** (JSON) | Structured representation of a proposed agent action | OPA input |
| **Policy Decision** (JSON) | Structured allow/deny with reasons and audit trail | OPA decision |
| **Scope Oracle** (infrastructure) | Evaluates proposed actions against policy rules; operates in separate trust domain | OPA server |

**Scope Enforcement Rule Example:**

```yaml
# rules/red-team/engagement/red-scope-target-validation.yaml
id: red.scope.target-validation
name: Target Authorization Validation
version: 1.0.0
category: engagement
severity: critical
description: >
  Validate that every proposed target is within the authorized scope
  defined in the engagement's signed scope document. Any action against
  an unauthorized target MUST be denied.
rationale: >
  Out-of-scope actions are the highest-risk category in red team engagements.
  OPA/Rego architectural patterns demonstrate that policy evaluation decoupled
  from enforcement prevents bypass. Every action must be validated before execution.
references:
  - type: owasp-agentic-ai
    id: ASI02
    url: "https://owasp.org/www-project-top-10-for-large-language-model-applications/"
  - type: internal
    id: AD-004
    url: "decisions/ADR-PROJ010-002-authorization-architecture.md"
default: enabled
configurable_params:
  validation_mode:
    type: string
    default: "strict"
    description: "Validation strictness: strict (exact match), subnet (CIDR match), domain (wildcard match)"
    allowed_values: ["strict", "subnet", "domain"]
  deny_action:
    type: string
    default: "block"
    description: "Action on denial: block (prevent execution), warn (log and continue), escalate (require red-lead approval)"
    allowed_values: ["block", "warn", "escalate"]
applicable_agents:
  - red-recon
  - red-vuln
  - red-exploit
  - red-privesc
  - red-lateral
  - red-persist
  - red-exfil
  - red-infra
  - red-social
tags:
  - scope-enforcement
  - authorization
  - safety-critical
```

**Policy Evaluation Flow:**

```
Agent proposes action
  -> Action serialized as structured input document (JSON)
    -> Scope Oracle loads active scope enforcement rules
      -> Rules evaluated against input: target in scope? technique authorized? time window valid?
        -> Decision returned: allow (proceed), deny (block + reason), escalate (require red-lead)
          -> Decision logged to tamper-evident audit trail
```

The YAML surface means scope enforcement rules participate in the same profile management and cascading override system as all other rules. An organization can customize scope enforcement behavior (e.g., changing `deny_action` from "block" to "escalate" for reconnaissance-only engagements) through the standard override mechanism. However, the `validation_mode` defaults to "strict" and the `deny_action` defaults to "block" for safety -- loosening these settings requires explicit justification at L2 or higher.

### Component 8: Rule Testing Framework

Custom rules must be testable before deployment, following patterns from all five analyzed tools: Semgrep (`--test`), OPA (built-in test), SonarQube (test framework), Checkov (pytest), ESLint (RuleTester) (F-003, R-RULES-008).

**Test Types:**

| Test Type | Description | Purpose |
|-----------|-------------|---------|
| **Positive tests** | Rule triggers on known-bad input; confirms detection works | Validates that the rule catches the condition it targets |
| **Negative tests** | Rule does not trigger on known-good input; confirms no false positives | Validates that the rule does not over-fire |
| **Parameter variation tests** | Rule behaves correctly across different `configurable_params` values | Validates that parameter overrides produce expected behavior |
| **Profile integration tests** | Rule activates/deactivates correctly within a profile context | Validates that profile enable/disable and parameter overrides resolve correctly |
| **Override precedence tests** | Rule resolution across cascade layers produces expected results | Validates the 5-layer cascade algorithm |

**Test Definition Format:**

```yaml
# tests/eng-team/test_eng_owasp_a01.yaml
rule_id: eng.owasp.a01.access-control-verification
tests:
  - name: "Triggers on endpoint without authorization check"
    type: positive
    input:
      endpoints:
        - path: "/api/admin/users"
          method: "GET"
          authorization: null
    expected:
      triggered: true
      severity: critical
      message_contains: "Missing authorization check"

  - name: "Does not trigger on endpoint with RBAC"
    type: negative
    input:
      endpoints:
        - path: "/api/admin/users"
          method: "GET"
          authorization:
            type: "rbac"
            roles: ["admin"]
    expected:
      triggered: false

  - name: "ASVS level 1 allows relaxed endpoint count"
    type: parameter_variation
    params:
      asvs_level: 1
      max_unprotected_endpoints: 2
    input:
      endpoints:
        - path: "/health"
          method: "GET"
          authorization: null
        - path: "/metrics"
          method: "GET"
          authorization: null
    expected:
      triggered: false  # 2 unprotected <= max of 2
```

**Test Execution:** Tests run during CI (pre-commit and PR validation) to prevent broken rules from reaching engagements. Rule changes without corresponding test updates are flagged. Test coverage metrics track the ratio of tested rules to total rules.

### Agent-to-Rule-Set Binding

Each of the 21 agents references its primary rule sets. The active profile determines which specific rules apply for a given engagement. This binding is declared in the agent definition and resolved at engagement start.

#### /eng-team Agent Bindings

| Agent | Primary Rule Sets | Default Profile | Standards Basis |
|-------|-------------------|-----------------|-----------------|
| eng-architect | NIST CSF 2.0, OWASP ASVS V1, NIST SSDF PW.1/PW.2 | `owasp-asvs-l2` | B-003 Agent Mapping |
| eng-lead | NIST SSDF PO, NIST CSF 2.0 Govern, OWASP SAMM Governance | `nist-ssdf-minimum` | B-003 Agent Mapping |
| eng-backend | OWASP Top 10, OWASP ASVS V2/V4/V5/V6/V7/V8/V10/V13/V15, CWE Top 25 | `owasp-asvs-l2` | B-003 Agent Mapping |
| eng-frontend | OWASP Top 10 (A01, A05, A07), OWASP ASVS V3/V5/V11, CWE Top 25 (XSS, CSRF) | `owasp-asvs-l2` | B-003 Agent Mapping |
| eng-infra | CIS Benchmarks, NIST 800-53 (AC/CM/CP/SC/SR), NIST SSDF PS/PO.5, SLSA | `cis-level1` | B-003 Agent Mapping |
| eng-qa | OWASP ASVS (test requirements), OWASP SAMM Verification, NIST SSDF PW.8 | `owasp-asvs-l2` | B-003 Agent Mapping |
| eng-security | All OWASP standards, NIST 800-53 (AU/CA/RA/SI), CWE Top 25, NIST SSDF PW.7/RV | `owasp-asvs-l2` | B-003 Agent Mapping |
| eng-reviewer | OWASP ASVS (review checklists), OWASP SAMM Verification, NIST SSDF PW.2/PW.7 | `owasp-asvs-l2` | B-003 Agent Mapping |
| eng-devsecops | DevSecOps pipeline rules, SLSA Build levels, NIST SSDF PS | `nist-ssdf-minimum` + `cis-level1` | B-003 Agent Mapping |
| eng-incident | NIST SSDF RV, NIST CSF 2.0 Respond/Recover | `nist-ssdf-minimum` | B-003 Agent Mapping |

#### /red-team Agent Bindings

| Agent | Primary Rule Sets | Default Profile | Standards Basis |
|-------|-------------------|-----------------|-----------------|
| red-lead | Scope enforcement, RoE enforcement, all methodology rules (oversight) | `ptes-standard` | A-004 Agent Boundaries |
| red-recon | ATT&CK TA0043 rules, PTES Intelligence Gathering, OSSTMM | `ptes-standard` | A-004 ATT&CK Mapping |
| red-vuln | Vulnerability analysis rules, CVE research rules | `ptes-standard` | A-004 Agent Boundaries |
| red-exploit | ATT&CK TA0001/TA0002/TA0040 rules, PTES Exploitation | `attack-full-scope` | A-004 ATT&CK Mapping |
| red-privesc | ATT&CK TA0004/TA0006 rules, PTES Post-Exploitation | `attack-full-scope` | A-004 ATT&CK Mapping |
| red-lateral | ATT&CK TA0008/TA0007 rules, PTES Post-Exploitation | `attack-full-scope` | A-004 ATT&CK Mapping |
| red-persist | ATT&CK TA0003/TA0005 rules, PTES Post-Exploitation | `attack-full-scope` | A-004 ATT&CK Mapping |
| red-exfil | ATT&CK TA0009/TA0010 rules, PTES Post-Exploitation | `attack-full-scope` | A-004 ATT&CK Mapping |
| red-reporter | Report quality rules, finding completeness rules, scope compliance rules | `ptes-standard` | A-004 Agent Boundaries |
| red-infra | ATT&CK TA0042/TA0011/TA0005 rules, C2 infrastructure rules | `attack-full-scope` | A-004 ATT&CK Mapping |
| red-social | ATT&CK TA0043 social/TA0001 phishing rules, social engineering methodology | `ptes-standard` | A-004 ATT&CK Mapping |

**Binding Resolution:** At engagement start, the system resolves each agent's active rule set by: (1) loading the agent's primary rule sets, (2) applying the engagement's assigned profile (which may override defaults), (3) running the 5-layer cascade to produce the final active rule set. The agent then operates under this resolved rule set for the duration of the engagement.

**Routing Context Integration:** Rule set configuration affects skill routing context (S-002, Cross-Cutting Concerns). If an organization substitutes OWASP with a proprietary standard through profile overrides, the routing system must still resolve agent selection correctly. This is achieved because routing operates on agent capability domains (which are static), not on active rule content (which is dynamic). The rule set determines what the agent checks against, not whether the agent is selected.

---

## Options Considered

### Option 1: YAML-Only Rules (Rejected)

**Description:** All rules defined exclusively in YAML. No programmatic rule authoring.

**Pros:**
- Maximum simplicity; all rules are data, not code
- Uniform validation through JSON Schema
- Lowest barrier to entry for rule authors

**Cons:**
- Cannot express complex rules requiring graph traversal, multi-step validation, or dynamic computation
- Would force either excluding complex rules or encoding complex logic in YAML in a way that reduces readability
- F-003 Finding 4 documents that Checkov's YAML-only surface was insufficient for real-world policy needs, leading to the Python escape hatch

**Why rejected:** YAML alone cannot express the full range of rules needed. Complex architectural pattern detection, cross-rule dependency analysis, and dynamic threshold computation require programmatic logic. Forcing these into YAML would produce unreadable rules that defeat the purpose of choosing YAML for simplicity.

### Option 2: Python-Only Rules (Rejected)

**Description:** All rules defined as Python classes implementing a standard interface.

**Pros:**
- Maximum expressiveness; any validation logic possible
- Full IDE support (type checking, autocompletion)
- Single implementation pattern

**Cons:**
- Requires Python expertise to author or modify rules
- Higher maintenance overhead for simple rules that YAML handles trivially
- Not accessible to security practitioners who lack Python skills but can write Semgrep-style YAML rules
- Violates the principle that rule authoring should not require programming (F-003, R-RULES-001)

**Why rejected:** Most rules are simple enough for YAML. Requiring Python for all rules raises the barrier to entry for exactly the users R-011 targets: security practitioners who want to customize rules for their organization's standards.

### Option 3: YAML Primary with Python Escape Hatch (Chosen)

**Description:** YAML as the primary rule format for the majority of rules, with Python available for complex rules that exceed YAML's expressiveness. Both formats share the same schema and produce the same output structure.

**Pros:**
- Low barrier to entry for simple rules (most rules)
- Full expressiveness for complex rules (minority)
- Follows the validated Checkov dual-format pattern (F-003, Finding 4)
- Both formats participate in the same profile management and cascade system
- Format selection criteria are documented and unambiguous

**Cons:**
- Two formats means two code paths for rule loading and validation
- Rule authors must decide which format to use (mitigated by documented selection criteria)
- Python rules require a runtime environment (mitigated by existing uv-based Python infrastructure)

**Why chosen:** This option provides the best balance of accessibility and expressiveness. The Checkov pattern validates that dual-format authoring works in production for security policy systems. The format selection criteria eliminate ambiguity about when to use which format.

### Option 4: OPA/Rego as Rule Language (Rejected)

**Description:** Use OPA's Rego language as the rule definition language for all rules.

**Pros:**
- Most powerful general-purpose policy language
- Built-in test framework
- CNCF graduated project with strong ecosystem
- Natural fit for /red-team scope enforcement policies

**Cons:**
- Rego introduces a domain-specific language learning curve that few security practitioners have
- Overkill for simple rules (checking whether a parameter exceeds a threshold should not require Rego comprehensions)
- Would add OPA runtime as an infrastructure dependency
- F-003 Finding 2 concludes: "Rego's learning curve makes it less suitable as a user-facing configuration format for R-011"

**Why rejected:** Rego's power is disproportionate to the needs of the majority of rules. The architectural patterns from OPA (policy evaluation decoupled from enforcement, structured input/output) are adopted for scope enforcement, but the Rego language itself is not exposed to users. Users interact with YAML; the scope oracle implements OPA patterns internally.

### Option 5: JSON Schema-Based Rules (Rejected)

**Description:** Define rules using JSON Schema validation patterns, leveraging the existing JSON Schema ecosystem.

**Pros:**
- Aligns with Convergence 5 (JSON Schema as universal format)
- Mature tooling for schema validation
- Machine-parseable with extensive library support

**Cons:**
- JSON Schema is optimized for data validation, not for expressing security policy logic
- Poor human readability compared to YAML for rule authoring
- Cannot express rationale, references, or configurable parameters without significant schema extension
- No precedent in the security tooling ecosystem (Semgrep, OPA, Checkov, ESLint all rejected JSON Schema for rule definition)

**Why rejected:** JSON Schema serves as the validation mechanism for YAML rules (the `schema/rule-schema.json` file validates rule YAML), but it is not suitable as the rule definition language itself. The security tooling ecosystem has converged on YAML or DSLs for rule definition, with JSON Schema in a supporting validation role.

---

## Consequences

### Positive

1. **R-011 fully satisfied.** Users can override default rules by creating organization profiles (L2), team profiles (L3), engagement overrides (L4), or runtime flags (L5) without modifying any skill code. The profile extension mechanism enables adding organization-specific rules (PCI DSS, HIPAA, proprietary standards) while inheriting and benefiting from default rule set updates.

2. **Compliance architecture without a compliance agent.** Convergence 4 validated that configurable rule sets are the correct compliance architecture. This decision eliminates the need for a dedicated eng-compliance agent (deferred in A-004), reducing agent count while providing superior compliance flexibility. Different regulatory environments (PCI DSS, HIPAA, SOC 2, GDPR) are served through profile customization, not through agent specialization.

3. **Standards-mapped defaults provide production readiness.** /eng-team ships with OWASP ASVS 5.0 (~350 requirements), OWASP Top 10 2025, CWE Top 25 2025, CIS Benchmarks, and NIST SSDF. /red-team ships with MITRE ATT&CK (14 tactics), PTES (7 phases), OSSTMM (5 channels), and OWASP Testing Guide. Organizations can start using the skills immediately with industry-standard defaults and customize incrementally.

4. **Unified rule format across both skills.** The shared rule schema means /eng-team and /red-team rules use the same structure (id, category, severity, description, rationale, references, configurable_params). This enables cross-skill rule management tooling, consistent user experience, and potential cross-skill rule correlation (e.g., /red-team exploitation findings linked to /eng-team verification rules through shared CWE references).

5. **Reproducible engagements through Git versioning.** Rules stored in version-controlled directories with tagged releases enable engagement pinning. The same engagement re-run against the same rule set version produces the same rule evaluation. Diff analysis between versions provides an audit trail of rule changes. This is validated by the Semgrep and Checkov pattern of Git-based rule versioning (F-003, R-RULES-007).

6. **Scope enforcement integrated into rule architecture.** /red-team scope enforcement policies use the same YAML rule format and participate in the same profile management system. This means scope enforcement behavior can be customized through the standard override mechanism while maintaining safety-critical defaults. The OPA/Rego architectural separation of policy decision from enforcement is preserved at the infrastructure level (Scope Oracle).

7. **Testable rules prevent engagement disruption.** The rule testing framework (positive, negative, parameter variation, profile integration, cascade precedence tests) ensures that custom rules are validated before deployment. This follows the testing patterns from all five analyzed tools and prevents broken rules from disrupting live engagements.

### Negative

1. **Dual-format maintenance burden.** Supporting both YAML and Python rule formats requires two code paths for rule loading, validation, and execution. The Python rule interface must remain backward-compatible as the YAML schema evolves. Estimated maintenance overhead: 15-20% additional effort for the rule engine implementation compared to a single-format approach.
   - **Mitigation:** Clear format selection criteria documented in Component 2. Expect 80-90% of rules to be YAML, limiting the Python code path usage. The Python interface is intentionally minimal (single `evaluate()` method) to reduce maintenance surface.

2. **Profile inheritance complexity for large organizations.** Deep inheritance chains (5+ levels) can make it difficult to trace which layer contributed a specific rule value. This is the same challenge SonarQube users face with nested profile hierarchies.
   - **Mitigation:** Profile comparison operation (diff two profiles) is a first-class feature. Maximum inheritance depth should be limited to 4 levels (skill default -> org -> team -> engagement) to prevent excessive nesting. The resolution algorithm is deterministic and traceable.

3. **Rule schema migration risk.** If the standard rule schema requires breaking changes in a future version, all existing YAML rules must be migrated. With potentially hundreds of rules across both skills and organization overrides, schema migration becomes a significant operation.
   - **Mitigation:** The schema is versioned (semantic versioning on rule files). Migration tooling should be built alongside the rule engine. Breaking schema changes should be treated as C3 decisions with appropriate governance.

4. **Initial rule authoring investment.** Populating comprehensive default rule sets for all mapped standards (OWASP ASVS ~350 requirements, CWE Top 25, CIS Benchmarks, ATT&CK 14 tactics with technique selections, PTES 7 phases) requires substantial initial authoring effort.
   - **Mitigation:** EN-115 (Default Rule Set Specification) scopes this work. Rule authoring can be prioritized by agent binding frequency: start with the rules for the most commonly used agents (eng-backend, eng-security, red-exploit, red-recon) and expand incrementally.

5. **Scope enforcement policy customization risk.** Allowing organizations to customize scope enforcement rules (Component 7) through the standard override mechanism means an organization could theoretically weaken scope enforcement (e.g., changing `deny_action` from "block" to "warn"). While this is by design (R-011 requires override capability), it creates a safety risk if done without understanding the consequences.
   - **Mitigation:** Critical-severity scope enforcement rules require a `justification` field when disabled or modified at any layer. The default values for scope enforcement are maximally restrictive ("strict" validation, "block" denial). Documentation must explicitly warn that weakening scope enforcement transfers safety responsibility to the organization. Audit trail records all scope enforcement rule modifications.

### Neutral (Requires Monitoring)

1. **Profile propagation lag.** When a default profile is updated (e.g., new OWASP ASVS 5.0 requirements added), changes propagate through the inheritance chain. Organizations using extended profiles receive these updates automatically. This is generally positive but could introduce unexpected rule changes in active engagements.
   - **Monitoring:** Engagement configuration should pin to a specific rule set version rather than tracking the latest. Profile updates should be communicated through release notes. Active engagements are not affected by post-start profile changes.

2. **Cross-skill rule correlation maturity.** The shared rule schema enables cross-skill correlation (e.g., linking /eng-team's CWE-89 SQL injection verification rule with /red-team's SQL injection exploitation technique rule). This capability requires additional tooling beyond the rule set architecture itself and is not required for R-011 satisfaction.
   - **Monitoring:** Track demand for cross-skill correlation during Phase 5 purple team exercises. Build correlation tooling if demand materializes.

3. **Community rule contribution pipeline.** The architecture supports community-contributed rules (following the Semgrep Registry model), but no contribution pipeline is specified in this ADR. As the rule library grows, a quality gate for community rules may become necessary.
   - **Monitoring:** Track rule library growth. When custom rule submissions exceed internal authoring capacity, design a contribution pipeline with quality validation.

---

## Evidence Base

### F-003: Configurable Rule Set Research (Primary)

F-003 analyzed five production rule configuration systems to identify convergent patterns:

| Tool | Key Pattern Adopted | Component |
|------|---------------------|-----------|
| **Semgrep** | YAML structured schema (id, severity, pattern, metadata); extensible without code changes; 2,000+ community rules as defaults | Component 1 (Rule Schema), Component 6 (Defaults) |
| **OPA/Rego** | Policy evaluation decoupled from enforcement; structured input documents; structured decision output | Component 7 (Scope Enforcement) |
| **SonarQube** | Profile extension with inheritance; per-project assignment; parameter override; organizational profile hierarchy | Component 4 (Profile Management) |
| **Checkov** | Dual-format authoring (YAML for simple, Python for complex); configuration precedence hierarchy | Component 2 (Python Escape Hatch) |
| **ESLint** | Cascading override (later configs override earlier); `extends` for inheritance; programmatic composition | Component 5 (Cascading Override) |

**Cross-tool convergence (F-003, Finding 6):** All five tools converge on: default rules, custom override mechanism, disable mechanism, and per-project configuration. This convergence validates the architecture's fundamental structure.

### B-003: OWASP, NIST, CIS, SANS Standards Analysis

B-003 provided the standards mapping that populates Component 6 (Default Rule Sets) and the agent-to-rule-set binding:

| Finding | Impact on Architecture |
|---------|----------------------|
| OWASP ASVS 5.0 expanded to ~350 requirements across 17 chapters with 3-level assurance model | ASVS levels become the primary configuration axis for /eng-team profiles |
| OWASP Top 10 2025 introduces A03 Supply Chain Failures and A10 Mishandling of Exceptional Conditions | New default rules for supply chain (eng-infra) and error handling (eng-backend) |
| CWE Top 25 2025 shows CWE-862 Missing Authorization jumped to #4 | Access control verification rule elevated to critical severity |
| NIST SSDF 4 practice groups map to /eng-team agent workflow | SSDF practice IDs embedded as rule references for governance traceability |
| CIS Benchmarks Level 1/Level 2 distinction maps to engagement criticality | CIS profiles serve as eng-infra configuration baseline |
| B-003 Recommendation R1: ASVS 5.0 as default, Level 2 recommended | `owasp-asvs-l2.yaml` as the default /eng-team profile |

### S-001: Cross-Stream Convergence 4

Three independent streams arrived at the same conclusion:

- **Stream B** (defensive standards): ASVS 3-level model provides a natural configuration axis
- **Stream F** (configurable rules): Five rule configuration systems analyzed; YAML-first with profiles recommended
- **Stream A** (roster design): eng-compliance deferred because configurable rule sets serve compliance needs better than a static agent

This triple convergence is classified as HIGH confidence. The architecture decision is supported by independent evidence from organizational analysis, standards analysis, and tool ecosystem analysis.

### S-002: AD-007 and Cross-Cutting Integration

S-002 formalized this as AD-007 with four cross-cutting integration concerns:

| Concern | Resolution in This ADR |
|---------|----------------------|
| Agent-to-rule-set binding | Component 8: each agent declares primary rule sets; active profile determines applied rules |
| Routing context affected by rule configuration | Routing operates on capability domains (static), not rule content (dynamic); addressed in Component 8 |
| Scope enforcement policy format consistency | Component 7: scope rules use same YAML format and participate in same profile/cascade system |
| Default rule set overridability | Components 5 and 6: 5-layer cascade enables override at every organizational level |

---

## Compliance

### R-011 Satisfaction

| R-011 Requirement | Architecture Component | How Satisfied |
|-------------------|------------------------|---------------|
| "Both skills MUST support user-provided rule sets" | Component 1 (Schema), Component 3 (Directory) | Users create YAML or Python rules in the `overrides/` directory; rules follow the standard schema and participate in the resolution system |
| "content for practices, standards, and methodologies" | Component 6 (Default Rule Sets) | Defaults mapped to OWASP, NIST, MITRE ATT&CK, CIS, SANS, PTES, OSSTMM |
| "Users MUST be able to override default rules" | Component 4 (Profiles), Component 5 (Cascade) | Profile extension enables override without modifying originals; 5-layer cascade provides override at organization, team, engagement, and runtime levels |
| "(e.g., substitute OWASP with org-specific standards)" | Component 4 (Profile Extension) | Organization creates a profile that extends or copies a default; disables OWASP rules; enables org-specific rules; original defaults unchanged |
| "without modifying core skill code" | Component 3 (Directory), Component 5 (Cascade) | All overrides are in external files (profiles, engagement config, runtime flags); no modifications to skill source code, agent definitions, or default rule files |

### PLAN.md Requirements Traceability

| Requirement | Relevance | Status |
|-------------|-----------|--------|
| R-011 | Primary -- this ADR directly satisfies R-011 | Fully addressed (see table above) |
| R-001 (Secure by Design) | Default rule sets embed security standards at every phase | Addressed via Component 6 |
| R-013 (C4 /adversary review) | This ADR subject to >= 0.95 quality threshold | Pending review |
| R-018 (Real Offensive Techniques) | /red-team default rules mapped to ATT&CK techniques | Addressed via Component 6 |
| R-019 (Secure SDLC Practices) | /eng-team defaults include OWASP ASVS, NIST SSDF, CIS | Addressed via Component 6 |
| R-020 (Authorization Verification) | Scope enforcement policies integrated into rule architecture | Addressed via Component 7 |

### Governance Alignment

| Governance Item | Compliance |
|-----------------|------------|
| AD-001 (Methodology-First Design) | Rules govern methodology guidance parameters; agents advise based on active rule sets, not execute based on them |
| AD-004 (Three-Layer Authorization) | Component 7 scope enforcement rules feed the Scope Oracle (Layer 2 dynamic authorization); scope rules participate in the same profile system |
| AD-007 (YAML-First Rule Sets) | This ADR is the formal specification of AD-007 |
| Convergence 4 (Rule Sets as Compliance Architecture) | Architecture explicitly replaces the deferred eng-compliance agent with configurable profile management |
| Convergence 5 (Structured Data Formats) | YAML for rule configuration, JSON Schema for rule validation, SARIF for finding output -- three formats aligned with the data interchange layer |

---

## Related Decisions

### Upstream (Inputs to This ADR)

| Decision | Relationship | Impact |
|----------|-------------|--------|
| AD-001 (Methodology-First Design) | Constrains | Rules govern methodology guidance, not autonomous execution behavior |
| AD-002 (21-Agent Roster) | Informs | Agent-to-rule-set binding maps 21 agents to their primary rule sets |
| AD-004 (Three-Layer Authorization) | Constrains | Scope enforcement policies (Component 7) must integrate with the Scope Oracle |
| AD-007 (YAML-First Rule Sets) | Formalizes | This ADR is the full specification of the AD-007 decision from S-002 |
| AD-008 (Layered SDLC Governance) | Informs | /eng-team default rule sets align with the 5-layer SDLC model |
| AD-009 (STRIDE+DREAD Default) | Informs | Threat modeling methodology rules are configurable per engagement criticality |

### Downstream (Unblocked by This ADR)

| Item | Relationship | Description |
|------|-------------|-------------|
| EN-113 (Rule Set Schema & Directory Structure) | Unblocked | Components 1, 2, 3 provide the specification for schema and directory implementation |
| EN-114 (Override Mechanism Design) | Unblocked | Components 4, 5 provide the specification for profile management and cascade implementation |
| EN-115 (Default Rule Set Specification) | Unblocked | Components 6, 8 provide the specification for default rule authoring and agent binding |
| FEAT-010 (Agent Team Architecture) | Informs | Agent definitions must declare primary rule sets; agent behavior governed by active rules |
| FEAT-011 (Skill Routing & Invocation) | Informs | Routing context considers rule configuration but resolves on capability domains |
| FEAT-015 (Authorization & Scope Control) | Informs | Scope enforcement policy format (Component 7) and integration with Scope Oracle |
| FEAT-052 (Rule Set Customization Guide) | Blocked until accepted | User documentation depends on finalized architecture |

---

## References

### Research Artifacts (Phase 1)

| Artifact | Location | Content |
|----------|----------|---------|
| F-003 | `work/research/stream-f-secure-sdlc/F-003-configurable-rule-sets.md` | Semgrep, OPA, SonarQube, Checkov, ESLint analysis; YAML schema; profile management; 10 recommendations |
| B-003 | `work/research/stream-b-methodology/B-003-owasp-nist-cis-sans.md` | OWASP, NIST, CIS, SANS standards analysis; ASVS 3-level model; agent mapping |
| S-002 | `work/research/synthesis/S-002-architecture-implications.md` | AD-007 decision; cross-cutting integration concerns; agent-to-rule-set binding |
| S-001 | `work/research/synthesis/S-001-cross-stream-findings.md` | Convergence 4 (configurable rule sets as compliance architecture); Convergence 5 (structured data formats) |

### Industry Sources (from F-003 Evidence)

| Source | Date | Relevance |
|--------|------|-----------|
| Semgrep -- Rule Structure Syntax (semgrep.dev/docs) | 2025 | Authoritative YAML rule schema: required fields, pattern operators, metavariables |
| OPA -- Open Policy Agent Documentation (openpolicyagent.org) | 2025 | Policy evaluation architecture; Rego language; decoupled decision/enforcement |
| SonarQube -- Managing Quality Profiles (docs.sonarsource.com) | 2025 | Profile creation, extension, copying, assignment, inheritance model |
| Checkov -- Custom Policies Overview (checkov.io) | 2025 | Dual-format architecture (YAML + Python); configuration hierarchy |
| ESLint -- Flat Config with extends (eslint.org) | March 2025 | Cascading override; defineConfig(); inheritance re-introduced |
| OWASP ASVS 5.0 (owasp.org) | May 2025 | ~350 requirements across 17 chapters at 3 assurance levels |
| OWASP Top 10 2025 (owasp.org) | 2025 | 10 risk categories; A03 Supply Chain and A10 Error Handling new entries |
| CWE Top 25 2025 (cwe.mitre.org) | December 2025 | 25 most dangerous software weaknesses; CWE-862 jumped to #4 |
| CIS Benchmarks (cisecurity.org) | 2025 | 100+ configuration guides; Level 1/Level 2 distinction |
| NIST SP 800-218 SSDF (csrc.nist.gov) | 2022 (v1.2 draft December 2025) | 4 practice groups for secure software development |
| NIST CSF 2.0 (csrc.nist.gov) | February 2024 | 6 core functions including Govern |
| MITRE ATT&CK (attack.mitre.org) | 2025 | 14 tactics with techniques; /red-team coverage mapping |
| PTES -- Penetration Testing Execution Standard (pentest-standard.org) | 2025 | 7-phase penetration testing methodology |
| OSSTMM -- Open Source Security Testing Methodology Manual | 2025 | 5-channel security testing methodology |

### PROJ-010 Internal References

| Reference | Location | Content |
|-----------|----------|---------|
| PLAN.md R-011 | `PLAN.md` | Configurable Rule Sets requirement text |
| FEAT-013 | `work/EPIC-002-architecture-design/FEAT-013-configurable-rule-sets/FEAT-013-configurable-rule-sets.md` | Feature entity with acceptance criteria |
| A-004 (Final Roster) | `work/research/stream-a-role-completeness/A-004-roster-decisions.md` | 21-agent roster; eng-compliance deferral; agent-to-ATT&CK mapping |
| F-001 (Secure SDLC Models) | `work/research/stream-f-secure-sdlc/F-001-sdlc-comparison.md` | 5-layer SDLC model; agent-to-phase mapping |
| F-002 (Authorization Architecture) | `work/research/stream-f-secure-sdlc/F-002-scope-enforcement.md` | Three-layer authorization; Scope Oracle design; OWASP Agentic AI Top 10 |
