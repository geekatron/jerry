# Rule Set Customization Guide

> Hands-on guide for customizing, extending, and validating rule sets in the Jerry Cyber Ops /eng-team and /red-team skills.

<!--
DOCUMENT-ID: FEAT-052:rule-set-customization-guide
AUTHOR: PROJ-010 Phase 6
DATE: 2026-02-22
STATUS: DRAFT
PARENT: FEAT-052 (Rule Set Customization Guide)
EPIC: EPIC-006 (Documentation & Guides)
PROJECT: PROJ-010-cyber-ops
TYPE: User Guide
SSOT: ADR-PROJ010-004 (Configurable Rule Set Architecture)
-->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Audience Guide](#audience-guide) | L0/L1/L2 reading paths |
| [Rule Set Format](#rule-set-format) | YAML rule schema, Python escape hatch, and field reference |
| [Default Rule Sets](#default-rule-sets) | Built-in standards: OWASP, NIST, MITRE ATT&CK, CIS, SANS |
| [Override Mechanism](#override-mechanism) | Five-layer cascade, profile inheritance, and override procedures |
| [Validation Guide](#validation-guide) | Testing custom rule sets before deployment |
| [Examples](#examples) | Organization-specific substitution scenarios |
| [Troubleshooting](#troubleshooting) | Common issues and resolution |
| [References](#references) | SSOT and source document traceability |

---

## Audience Guide

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (Stakeholder)** | Security managers, compliance officers | [Default Rule Sets](#default-rule-sets), [Override Mechanism](#override-mechanism) overview, [Examples](#examples) |
| **L1 (Practitioner)** | Security engineers customizing rules | [Rule Set Format](#rule-set-format), [Override Mechanism](#override-mechanism), [Validation Guide](#validation-guide), [Examples](#examples) |
| **L2 (Architect)** | Framework designers, rule authors | All sections, especially [Rule Set Format](#rule-set-format) (Python escape hatch), [Validation Guide](#validation-guide) (cascade testing) |

---

## Rule Set Format

The configurable rule set architecture uses YAML as the primary rule definition format with a Python escape hatch for complex rules. Both formats share a common schema and produce uniform output, ensuring that all rules participate in the same profile management and cascade override system regardless of implementation format.

**SSOT:** ADR-PROJ010-004, Component 1 (YAML-First Rule Definition Format) and Component 2 (Python Escape Hatch).

### YAML Rule Schema

Every YAML rule file follows this schema. Required fields are marked with (R); optional fields with (O).

| Field | Type | Req | Description |
|-------|------|-----|-------------|
| `id` | string | (R) | Unique identifier using dot-separated namespace. Pattern: `{skill}.{category}.{standard}.{identifier}` |
| `name` | string | (R) | Human-readable rule name |
| `version` | string | (R) | Semantic version of the rule definition (e.g., `1.0.0`) |
| `category` | enum | (R) | One of: `security`, `architecture`, `coding`, `testing`, `engagement`, `methodology`, `compliance`, `infrastructure` |
| `severity` | enum | (R) | One of: `critical`, `high`, `medium`, `low`, `info` |
| `description` | string | (R) | What the rule checks or enforces |
| `rationale` | string | (R) | Why the rule exists; business or security value |
| `references` | array[object] | (R) | Standards references with `type`, `id`, and `url` fields |
| `default` | enum | (R) | `enabled` or `disabled` -- initial activation state |
| `configurable_params` | object | (O) | Tunable parameters with `name`, `type`, `default`, `description`, and optional `allowed_values` |
| `applicable_agents` | array[string] | (O) | Agent IDs this rule applies to (omit to apply to all agents in the skill) |
| `tags` | array[string] | (O) | Custom tags for filtering and grouping |
| `metadata` | object | (O) | Arbitrary key-value pairs for organizational extension |

### Rule ID Naming Convention

Rule IDs use dot-separated namespaces to ensure uniqueness and enable filtering:

| Skill | Pattern | Example |
|-------|---------|---------|
| /eng-team | `eng.{category}.{standard}.{identifier}` | `eng.owasp.a01.access-control-verification` |
| /red-team | `red.{category}.{standard}.{identifier}` | `red.attack.ta0001.initial-access` |
| Organization | `org.{org-name}.{category}.{identifier}` | `org.acme.pci-dss.cardholder-encryption` |

### Complete YAML Rule Example (/eng-team)

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
    description: "Maximum endpoints permitted without explicit authorization (0 = zero tolerance)"
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

### Complete YAML Rule Example (/red-team)

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

### Python Escape Hatch for Complex Rules

When a rule requires logic that exceeds YAML's declarative expressiveness -- such as graph traversal, multi-step validation, or dynamic computation -- use a Python class that implements the same schema fields.

**When to use Python instead of YAML:**

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

**Python rule example:**

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
            "description": "Maximum cycle length to report"
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

Both YAML and Python rules produce the same `RuleResult` output structure, ensuring uniform downstream processing.

### Rule File Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| YAML rule file | `{skill}-{standard}-{identifier}.yaml` | `eng-owasp-a01-access-control-verification.yaml` |
| Python rule file | `{skill}_{category}_{identifier}.py` | `eng_arch_dependency_cycle_detection.py` |
| Rule ID | `{skill}.{category}.{standard}.{identifier}` | `eng.owasp.a01.access-control-verification` |
| Profile file | `{standard}-{level-or-variant}.yaml` | `owasp-asvs-l2.yaml` |
| Test file | `test_{rule_file_stem}.yaml` | `test_eng_owasp_a01.yaml` |

---

## Default Rule Sets

Both /eng-team and /red-team ship with comprehensive default rule sets mapped to established security standards. These defaults provide a production-ready starting point. The override mechanism (next section) enables full customization without modifying any default rule files.

**SSOT:** ADR-PROJ010-004, Component 6 (Default Rule Sets).

### /eng-team Default Standards

| Standard | Rule Count | Scope | Default Profile |
|----------|-----------|-------|-----------------|
| **OWASP ASVS 5.0** | ~350 verification requirements across 17 chapters | 3 assurance levels: L1 baseline, L2 standard, L3 high-assurance | `owasp-asvs-l1.yaml`, `owasp-asvs-l2.yaml`, `owasp-asvs-l3.yaml` |
| **OWASP Top 10 2025** | 10 risk categories | A01 Broken Access Control through A10 Mishandling of Exceptional Conditions | Included in all ASVS profiles |
| **CWE Top 25 2025** | 25 most dangerous weaknesses | Based on 39,000+ CVEs (December 2025) | Included in all ASVS profiles |
| **CIS Benchmarks** | 100+ configuration guides | 8 technology categories, Level 1 (essential) and Level 2 (defense in depth) | `cis-level1.yaml`, `cis-level2.yaml` |
| **NIST SP 800-218 SSDF** | 4 practice groups | Prepare, Protect, Produce, Respond | `nist-ssdf-minimum.yaml` |
| **NIST CSF 2.0** | 6 core functions | Govern, Identify, Protect, Detect, Respond, Recover | Referenced within SSDF profile |

**Agent-to-standard mapping:**

| Agent | Primary Standards | Default Profile |
|-------|-------------------|-----------------|
| eng-architect | NIST CSF 2.0, OWASP ASVS V1, NIST SSDF PW.1/PW.2 | `owasp-asvs-l2` |
| eng-lead | NIST SSDF PO, NIST CSF Govern, OWASP SAMM Governance | `nist-ssdf-minimum` |
| eng-backend | OWASP Top 10, OWASP ASVS (V2,V4-V8,V10,V13,V15), CWE Top 25 | `owasp-asvs-l2` |
| eng-frontend | OWASP Top 10 (A01,A05,A07), OWASP ASVS V3/V5/V11, CWE (XSS,CSRF) | `owasp-asvs-l2` |
| eng-infra | CIS Benchmarks, NIST 800-53, SLSA | `cis-level1` |
| eng-devsecops | DevSecOps pipeline rules, SLSA, NIST SSDF PS | `nist-ssdf-minimum` + `cis-level1` |
| eng-security | All OWASP standards, NIST 800-53, CWE Top 25, NIST SSDF PW.7/RV | `owasp-asvs-l2` |

### /red-team Default Standards

| Standard | Rule Count | Scope | Default Profile |
|----------|-----------|-------|-----------------|
| **MITRE ATT&CK** | 14 tactics | Full kill chain coverage at STRONG level | `attack-full-scope.yaml`, `attack-external-only.yaml` |
| **PTES** | 7 phases | Pre-engagement through Reporting | `ptes-standard.yaml` |
| **OSSTMM** | 5 channels | Human, Physical, Wireless, Telecom, Data Networks | `osstmm-standard.yaml` |
| **OWASP Testing Guide** | Test categories | Web application security testing methodology | Referenced within PTES and ATT&CK profiles |

**Agent-to-standard mapping:**

| Agent | Primary Standards | Default Profile |
|-------|-------------------|-----------------|
| red-lead | Scope enforcement, RoE enforcement, all methodology rules | `ptes-standard` |
| red-recon | ATT&CK TA0043, PTES Intelligence Gathering, OSSTMM | `ptes-standard` |
| red-exploit | ATT&CK TA0001/TA0002/TA0040, PTES Exploitation | `attack-full-scope` |
| red-privesc | ATT&CK TA0004/TA0006, PTES Post-Exploitation | `attack-full-scope` |
| red-lateral | ATT&CK TA0008/TA0007, PTES Post-Exploitation | `attack-full-scope` |
| red-persist | ATT&CK TA0003/TA0005, PTES Post-Exploitation | `attack-full-scope` |
| red-exfil | ATT&CK TA0009/TA0010, PTES Post-Exploitation | `attack-full-scope` |
| red-infra | ATT&CK TA0042/TA0011/TA0005, C2 infrastructure rules | `attack-full-scope` |
| red-social | ATT&CK TA0043/TA0001 social/phishing rules | `ptes-standard` |

### Default Profile Hierarchy

```
Skill Default (built-in)
+-- OWASP ASVS L2 (eng-team standard)
|   +-- [Your org extends here]
+-- OWASP ASVS L1 (eng-team baseline)
+-- OWASP ASVS L3 (eng-team high-assurance)
+-- CIS Level 1 (eng-team infrastructure)
+-- CIS Level 2 (eng-team defense-in-depth)
+-- NIST SSDF Minimum (eng-team governance)
+-- PTES Standard (red-team methodology)
+-- ATT&CK Full Scope (red-team full engagement)
+-- ATT&CK External Only (red-team external-only)
+-- OSSTMM Standard (red-team methodology)
```

---

## Override Mechanism

The override mechanism enables organizations to customize rule behavior at five layers without modifying any default rule files. Later layers override earlier layers with deterministic precedence.

**SSOT:** ADR-PROJ010-004, Component 4 (Profile Management) and Component 5 (Five-Layer Cascading Override).

### Five-Layer Cascade

| Layer | Priority | Source | Description |
|-------|----------|--------|-------------|
| L1 | Lowest | Skill defaults | Rules built into /eng-team or /red-team |
| L2 | Low | Organization profile | Shared across the organization; set by security leadership |
| L3 | Medium | Team/project profile | Per-team customization within organizational constraints |
| L4 | High | Engagement overrides | Per-engagement configuration |
| L5 | Highest | Runtime flags | CLI or environment variable overrides (ephemeral, not persisted) |

### Precedence Rules

1. **Last writer wins.** The highest-priority layer's value takes effect for scalar fields.
2. **Merge for additive fields.** Array fields (`tags`, `applicable_agents`) merge across layers. Scalar fields (`severity`, `enabled`, parameter values) replace.
3. **Explicit disable overrides enable.** Setting `enabled: false` at any layer disables the rule unless a higher layer re-enables it.
4. **Justification required for disable.** Disabling a `critical`-severity rule at L2, L3, or L4 requires a `justification` field.
5. **Runtime flags are ephemeral.** L5 overrides apply only to the current execution.
6. **Inheritance resolution precedes cascade.** Within a single layer, profile inheritance (`extends`) is resolved first, producing a flat rule set. The cascade then applies across layers.

### Resolution Algorithm

```
1. Load skill default rules (L1)              -> base rule set
2. Resolve organization profile inheritance   -> org rule set
3. Merge org rule set onto base (L2 > L1)    -> merged
4. Resolve team/project profile inheritance   -> team rule set
5. Merge team rule set onto merged (L3 > L2) -> merged
6. Apply engagement overrides (L4 > L3)      -> merged
7. Apply runtime flags (L5 > L4)             -> final active rule set
```

### How to Create an Organization Profile (L2)

Step 1: Create the profile file in the overrides directory.

```yaml
# overrides/acme-corp/profiles/acme-standard.yaml
id: org.acme.profile.standard
name: "Acme Corp Standard Security Profile"
version: 1.0.0
description: >
  Extends OWASP ASVS Level 2 with Acme Corp-specific requirements
  including PCI DSS controls and internal coding standards.
skill: eng-team
extends: eng.profile.owasp-asvs-l2  # Inherit all L2 rules
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
      asvs_level: 3         # Acme requires Level 3 for access control
      include_rbac_review: true

  # Disable a default rule (justification required for critical rules)
  eng.owasp.a03.supply-chain:
    enabled: false
    justification: "Acme uses proprietary supply chain validation system"
```

Step 2: Create any organization-specific rule files referenced by the profile.

```yaml
# overrides/acme-corp/rules/org-acme-pci-dss-cardholder-encryption.yaml
id: org.acme.pci-dss.cardholder-data-encryption
name: Cardholder Data Encryption (PCI DSS Req 3)
version: 1.0.0
category: compliance
severity: critical
description: >
  Verify that cardholder data is encrypted at rest and in transit using
  approved algorithms per PCI DSS Requirement 3.
rationale: >
  PCI DSS Requirement 3 mandates protection of stored cardholder data.
  Acme processes payment card transactions and must comply.
references:
  - type: pci-dss
    id: "Req-3"
    url: "https://www.pcisecuritystandards.org/"
  - type: nist
    id: "SP800-175B"
    url: "https://csrc.nist.gov/publications/detail/sp/800-175b/rev-1/final"
default: enabled
configurable_params:
  encryption_algorithm:
    type: string
    default: "AES-256-GCM"
    description: "Required encryption algorithm"
    allowed_values: ["AES-256-GCM", "AES-256-CBC", "ChaCha20-Poly1305"]
  key_rotation_days:
    type: integer
    default: 90
    description: "Maximum days before key rotation required"
applicable_agents:
  - eng-backend
  - eng-infra
  - eng-security
tags:
  - pci-dss
  - encryption
  - compliance
```

Step 3: Assign the profile to an engagement.

```yaml
# engagement configuration
engagement:
  id: "ENG-0042"
  profile: org.acme.profile.standard
  # All agents in this engagement now operate under the Acme profile
```

### How to Create a Team/Project Profile (L3)

Team profiles extend organizational profiles for team-specific needs.

```yaml
# overrides/acme-corp/teams/team-alpha-profile.yaml
id: org.acme.team.alpha
name: "Acme Team Alpha Profile"
version: 1.0.0
description: >
  Team Alpha works on API-only services. Disables frontend-specific
  rules and adds API security rules.
skill: eng-team
extends: org.acme.profile.standard  # Inherits Acme org profile
rules:
  # Disable frontend-specific rules (API-only team)
  eng.owasp.a01.access-control-verification:
    params:
      include_rbac_review: true
  eng.asvs.v17.webrtc:
    enabled: false
    justification: "Team Alpha builds API-only services, no WebRTC"

  # Add API-specific rules
  org.acme.api.rate-limiting:
    enabled: true
    severity: high
    params:
      min_rate_limit_rpm: 100
      require_api_key: true
```

### How to Apply Engagement-Level Overrides (L4)

Engagement overrides apply to a single engagement without creating a reusable profile.

```yaml
# engagement configuration with overrides
engagement:
  id: "ENG-0042"
  profile: org.acme.team.alpha
  overrides:
    # This specific engagement uses ASVS Level 3
    eng.owasp.a01.access-control-verification:
      params:
        asvs_level: 3
    # Enable a rule that's normally disabled
    eng.asvs.v17.webrtc:
      enabled: true
      justification: "This engagement includes WebRTC components"
```

### How to Apply Runtime Flags (L5)

Runtime flags are ephemeral and apply only to the current execution. They are not persisted.

```bash
# Override a single rule parameter at runtime
--rule-override eng.owasp.a01.access-control-verification.params.asvs_level=3

# Disable a rule for this run only
--rule-override eng.owasp.a03.supply-chain.enabled=false
```

### Cascade Conflict Resolution Example

This table shows how the same rule resolves across layers:

| Rule Field | L1 (Default) | L2 (Org) | L3 (Team) | L4 (Engagement) | Resolved |
|------------|-------------|----------|-----------|-----------------|----------|
| `severity` | `high` | `critical` | -- | -- | `critical` (L2 wins) |
| `enabled` | `true` | `true` | `false` | -- | `false` (L3 wins) |
| `params.asvs_level` | `2` | -- | -- | `3` | `3` (L4 wins) |
| `tags` | `["owasp"]` | `["pci-dss"]` | `["team-alpha"]` | -- | `["owasp", "pci-dss", "team-alpha"]` (merged) |

### Profile Operations Reference

| Operation | Description | Use Case |
|-----------|-------------|----------|
| **Extend** | Child inherits parent rules; parent changes propagate | Org profile extends ASVS L2 |
| **Copy** | Independent copy; no inheritance | Fork a profile for experimentation |
| **Assign** | Associate profile with engagement | Each engagement uses one profile per skill |
| **Compare** | Diff two profiles | Audit differences between team profiles |
| **Export/Import** | Portable YAML serialization | Share profiles between installations |

---

## Validation Guide

Custom rules and profiles must be validated before deployment to prevent broken rules from disrupting live engagements.

**SSOT:** ADR-PROJ010-004, Component 8 (Rule Testing Framework).

### Rule Schema Validation

Validate YAML rule files against the JSON Schema before testing behavior:

```bash
# Validate a single rule file against the schema
uv run python -m cyberops.rules.validate \
  --schema rules/schema/rule-schema.json \
  --rule overrides/acme-corp/rules/org-acme-pci-dss-cardholder-encryption.yaml
```

The validator checks:
- All required fields are present (`id`, `name`, `version`, `category`, `severity`, `description`, `rationale`, `references`, `default`)
- Field values conform to their enum types
- `configurable_params` entries have valid `type`, `default`, and `description` fields
- `allowed_values` constraints are consistent with parameter `type`
- Rule ID follows the dot-separated namespace convention

### Rule Test Definitions

Each custom rule should have corresponding test definitions:

```yaml
# tests/eng-team/test_org_acme_pci_dss.yaml
rule_id: org.acme.pci-dss.cardholder-data-encryption
tests:
  - name: "Triggers on unencrypted cardholder data storage"
    type: positive
    input:
      data_stores:
        - name: "payment_db"
          contains_cardholder_data: true
          encryption: null
    expected:
      triggered: true
      severity: critical
      message_contains: "cardholder data"

  - name: "Does not trigger on properly encrypted storage"
    type: negative
    input:
      data_stores:
        - name: "payment_db"
          contains_cardholder_data: true
          encryption:
            algorithm: "AES-256-GCM"
            key_rotation_days: 60
    expected:
      triggered: false

  - name: "Triggers when key rotation exceeds threshold"
    type: parameter_variation
    params:
      key_rotation_days: 90
    input:
      data_stores:
        - name: "payment_db"
          contains_cardholder_data: true
          encryption:
            algorithm: "AES-256-GCM"
            key_rotation_days: 120
    expected:
      triggered: true
      message_contains: "key rotation"
```

### Test Types

| Test Type | Purpose | When to Write |
|-----------|---------|---------------|
| **Positive** | Confirm rule triggers on known-bad input | Every rule must have at least one |
| **Negative** | Confirm rule does not trigger on known-good input | Every rule must have at least one |
| **Parameter variation** | Confirm configurable_params affect behavior correctly | Every rule with configurable_params |
| **Profile integration** | Confirm rule activates/deactivates correctly within a profile | When creating new profiles |
| **Override precedence** | Confirm cascade resolution produces expected results | When using multi-layer overrides |

### Running Tests

```bash
# Run all rule tests
uv run python -m cyberops.rules.test

# Run tests for a specific rule
uv run python -m cyberops.rules.test --rule-id org.acme.pci-dss.cardholder-data-encryption

# Run tests for all rules in a profile
uv run python -m cyberops.rules.test --profile org.acme.profile.standard

# Run override precedence tests for an engagement
uv run python -m cyberops.rules.test --engagement ENG-0042 --test-type precedence
```

### Profile Validation

Validate that a profile resolves correctly:

```bash
# Show the resolved rule set for a profile (after inheritance)
uv run python -m cyberops.rules.resolve --profile org.acme.profile.standard

# Compare two profiles
uv run python -m cyberops.rules.compare \
  --profile-a eng.profile.owasp-asvs-l2 \
  --profile-b org.acme.profile.standard

# Validate engagement rule resolution (full cascade)
uv run python -m cyberops.rules.resolve \
  --engagement ENG-0042 \
  --show-layers  # Shows which layer contributed each value
```

The `--show-layers` flag produces output showing the origin of each resolved value:

```
Rule: eng.owasp.a01.access-control-verification
  severity: critical          [L2: org.acme.profile.standard]
  enabled: true               [L1: skill default]
  params.asvs_level: 3        [L4: engagement override]
  params.include_rbac_review:  [L1: skill default]
  tags: [owasp, pci-dss]      [merged: L1 + L2]
```

### Pre-Deployment Checklist

Before deploying custom rules or profiles to a live engagement:

1. **Schema validation passes** -- All custom rule files pass JSON Schema validation
2. **Positive tests pass** -- Every custom rule triggers on known-bad input
3. **Negative tests pass** -- No false positives on known-good input
4. **Parameter variation tests pass** -- Configurable parameters produce expected behavior
5. **Profile resolution is correct** -- `--show-layers` output matches expectations
6. **No broken inheritance** -- Parent profile changes propagate correctly
7. **Critical rule disables are justified** -- Every disabled critical-severity rule has a `justification` field
8. **Version tagged** -- Custom rules are tagged (e.g., `rules-acme-v1.0.0`) for reproducibility

---

## Examples

### Example 1: Substituting OWASP with PCI DSS for a Financial Organization

**Scenario:** FinCo processes payment card transactions and needs PCI DSS rules instead of the generic OWASP ASVS rules. They want to keep OWASP ASVS as a baseline but add PCI DSS-specific controls and elevate certain severity levels.

**Before (default OWASP ASVS L2 profile):**
- Standard OWASP ASVS L2 rules across all agents
- No PCI DSS-specific rules
- Default severity levels

**Step 1: Create PCI DSS rules.**

```yaml
# overrides/finco/rules/org-finco-pci-dss-req3-data-protection.yaml
id: org.finco.pci-dss.req3.data-protection
name: PCI DSS Requirement 3 - Protect Stored Cardholder Data
version: 1.0.0
category: compliance
severity: critical
description: >
  Verify that primary account numbers (PAN) are rendered unreadable
  anywhere they are stored, using one-way hashing, truncation, index
  tokens, or strong cryptography per PCI DSS Requirement 3.
rationale: >
  PCI DSS Requirement 3 mandates protection of stored cardholder data.
  FinCo's PCI Level 1 merchant status requires full compliance.
references:
  - type: pci-dss
    id: "Req-3.4"
    url: "https://www.pcisecuritystandards.org/"
default: enabled
configurable_params:
  allowed_storage_methods:
    type: string
    default: "hash_or_truncate"
    description: "Allowed PAN storage methods"
    allowed_values: ["hash_or_truncate", "tokenize", "encrypt"]
  require_key_management_procedure:
    type: boolean
    default: true
    description: "Require documented key management procedures"
applicable_agents:
  - eng-backend
  - eng-infra
  - eng-security
tags:
  - pci-dss
  - requirement-3
  - data-protection
```

**Step 2: Create the FinCo organization profile.**

```yaml
# overrides/finco/profiles/finco-pci-standard.yaml
id: org.finco.profile.pci-standard
name: "FinCo PCI DSS Standard Profile"
version: 1.0.0
description: >
  Extends OWASP ASVS Level 2 with PCI DSS requirements for
  FinCo's payment processing applications.
skill: eng-team
extends: eng.profile.owasp-asvs-l2
rules:
  # Add PCI DSS rules
  org.finco.pci-dss.req3.data-protection:
    enabled: true
  org.finco.pci-dss.req6.secure-development:
    enabled: true
  org.finco.pci-dss.req8.access-management:
    enabled: true

  # Elevate severity for payment-relevant OWASP rules
  eng.owasp.a05.injection:
    severity: critical  # Elevated from high for PCI context
    params:
      check_parameterized_queries: true
      check_orm_injection: true

  # Elevate cryptographic failure severity
  eng.owasp.a04.cryptographic-failures:
    severity: critical
    params:
      require_tls_1_3: true
      require_aes_256: true
```

**After (FinCo PCI profile):**
- OWASP ASVS L2 rules as baseline (inherited)
- PCI DSS-specific rules added for Requirements 3, 6, and 8
- Injection and cryptographic failure rules elevated to critical severity
- All changes traceable through `--show-layers`

### Example 2: Adding HIPAA Compliance for a Healthcare Organization

**Scenario:** HealthCo builds patient management software and needs HIPAA-specific rules layered onto the default standards.

```yaml
# overrides/healthco/profiles/healthco-hipaa.yaml
id: org.healthco.profile.hipaa
name: "HealthCo HIPAA Compliance Profile"
version: 1.0.0
description: >
  Extends OWASP ASVS Level 3 with HIPAA Security Rule requirements.
  Level 3 chosen because patient health information requires high-assurance.
skill: eng-team
extends: eng.profile.owasp-asvs-l3  # High-assurance baseline for PHI
rules:
  # HIPAA-specific rules
  org.healthco.hipaa.phi-encryption:
    enabled: true
    severity: critical
    params:
      at_rest: true
      in_transit: true
      minimum_algorithm: "AES-256"
  org.healthco.hipaa.access-audit:
    enabled: true
    severity: critical
    params:
      log_all_phi_access: true
      retention_years: 6
  org.healthco.hipaa.minimum-necessary:
    enabled: true
    severity: high
    params:
      enforce_field_level_access: true

  # Strengthen default rules for HIPAA context
  eng.owasp.a01.access-control-verification:
    params:
      asvs_level: 3
      max_unprotected_endpoints: 0
  eng.owasp.a07.authentication-failures:
    params:
      require_mfa: true
      session_timeout_minutes: 15
```

### Example 3: Customizing Red Team Engagement Profiles

**Scenario:** An organization wants a red team engagement profile that restricts techniques to external-only testing (no post-exploitation) and adds an internal scope enforcement rule.

```yaml
# overrides/acme-corp/profiles/acme-external-pentest.yaml
id: org.acme.profile.external-pentest
name: "Acme External Penetration Test Profile"
version: 1.0.0
description: >
  External-only penetration test. No post-exploitation, no persistence,
  no exfiltration. Focus on external attack surface validation.
skill: red-team
extends: red.profile.attack-external-only
rules:
  # Add org-specific scope rules
  org.acme.scope.business-hours-only:
    enabled: true
    severity: critical
    params:
      start_hour: 8
      end_hour: 18
      timezone: "America/New_York"

  # Tighten technique justification requirements
  red.attack.ta0001.initial-access:
    params:
      required_technique_justification: true
      min_techniques_attempted: 5  # More thorough external testing
      scope_validation_mode: "strict"

  # Disable post-exploitation rules (external-only)
  red.attack.ta0004.privilege-escalation:
    enabled: false
    justification: "External-only engagement scope"
  red.attack.ta0003.persistence:
    enabled: false
    justification: "External-only engagement scope"
  red.attack.ta0009.exfiltration:
    enabled: false
    justification: "External-only engagement scope"
```

### Example 4: Internal Coding Standards Overlay

**Scenario:** A development team has internal coding standards that supplement the security standards. These go in a team-level profile (L3).

```yaml
# overrides/acme-corp/teams/backend-team-profile.yaml
id: org.acme.team.backend
name: "Acme Backend Team Profile"
version: 1.0.0
description: >
  Backend team-specific rules overlaying the Acme org profile.
  Adds internal API design standards and database access patterns.
skill: eng-team
extends: org.acme.profile.standard
rules:
  # Internal API design standards
  org.acme.internal.api-versioning:
    enabled: true
    severity: medium
    params:
      require_version_header: true
      deprecation_notice_days: 90

  # Database access pattern enforcement
  org.acme.internal.database-access:
    enabled: true
    severity: high
    params:
      require_orm: true
      allow_raw_sql: false
      require_query_timeout: true
      max_query_timeout_seconds: 30

  # Reduce ASVS level for internal-only APIs
  eng.owasp.a01.access-control-verification:
    params:
      asvs_level: 2  # Internal APIs use Level 2 (org default is 3)
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Resolution |
|-------|-------|------------|
| Rule not activating in engagement | Profile not assigned, or rule disabled at a higher layer | Run `uv run python -m cyberops.rules.resolve --engagement ENG-XXXX --show-layers` to trace resolution |
| Rule triggering unexpectedly | Parameter overridden at a different layer | Check `--show-layers` output for the contributing layer |
| Profile inheritance not propagating | `extends` field references wrong profile ID | Verify profile ID matches exactly (case-sensitive, dot-separated) |
| Schema validation failure | Missing required field or invalid enum value | Check error message for the specific field; compare against the schema reference |
| Python rule not loading | Class does not implement the `Rule` interface | Verify class has `id`, `name`, `version`, `category`, `severity`, `default`, and `evaluate()` |
| Critical rule disabled without justification | Schema enforcement requires `justification` field | Add `justification: "reason"` when disabling critical-severity rules |
| Unexpected tag merging | Array fields merge across layers | Tags are always additive; use specific layers to add, not replace |
| Engagement using wrong profile | Engagement config references wrong profile ID | Check engagement YAML `profile` field; verify profile file exists at expected path |

### Diagnostic Commands

```bash
# List all available profiles
uv run python -m cyberops.rules.profiles list

# Show inheritance chain for a profile
uv run python -m cyberops.rules.profiles show --profile org.acme.profile.standard --show-chain

# List all rules in a resolved profile
uv run python -m cyberops.rules.resolve --profile org.acme.profile.standard --list-rules

# Show which rules are overridden between two profiles
uv run python -m cyberops.rules.compare \
  --profile-a eng.profile.owasp-asvs-l2 \
  --profile-b org.acme.profile.standard \
  --show-diff

# Validate all rules in the overrides directory
uv run python -m cyberops.rules.validate --directory overrides/
```

---

## References

| Source | Content |
|--------|---------|
| [ADR-PROJ010-004](../../decisions/ADR-PROJ010-004-configurable-rule-sets.md) | SSOT: Configurable Rule Set Architecture -- YAML-first with profile management |
| [PLAN.md R-011](../../PLAN.md) | Configurable Rule Sets requirement |
| [F-003](../research/stream-f-secure-sdlc/F-003-configurable-rule-sets.md) | Semgrep, OPA, SonarQube, Checkov, ESLint rule configuration analysis |
| [B-003](../research/stream-b-methodology/B-003-owasp-nist-cis-sans.md) | OWASP, NIST, CIS, SANS standards analysis and agent mapping |
| [S-002](../research/synthesis/S-002-architecture-implications.md) | AD-007 decision: YAML-first rule sets with profile management |
| [S-001](../research/synthesis/S-001-cross-stream-findings.md) | Convergence 4: Configurable rule sets as compliance architecture |
| `/eng-team SKILL.md` | Engineering team skill definition and agent roster |
| `/red-team SKILL.md` | Red team skill definition and agent roster |

### Industry Standards Referenced

| Standard | URL |
|----------|-----|
| OWASP ASVS 5.0 | https://owasp.org/www-project-application-security-verification-standard/ |
| OWASP Top 10 2025 | https://owasp.org/Top10/2025/ |
| CWE Top 25 2025 | https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html |
| CIS Benchmarks | https://www.cisecurity.org/cis-benchmarks |
| NIST SP 800-218 SSDF | https://csrc.nist.gov/publications/detail/sp/800-218/final |
| NIST CSF 2.0 | https://www.nist.gov/cyberframework |
| MITRE ATT&CK | https://attack.mitre.org/ |
| PTES | http://www.pentest-standard.org/ |
| OSSTMM | https://www.isecom.org/OSSTMM.3.pdf |

---

*PROJ-010: Cyber Ops -- Rule Set Customization Guide*
*SSOT: ADR-PROJ010-004*
*Created: 2026-02-22*
