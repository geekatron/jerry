# F-003: Configurable Rule Set Research

> Stream F: Secure SDLC | PROJ-010 Cyber Ops | Phase 1 Research

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | High-level synthesis of rule/policy configuration patterns |
| [L1: Key Findings](#l1-key-findings) | Numbered findings with evidence on each tool's approach |
| [L2: Detailed Analysis](#l2-detailed-analysis) | Deep analysis of Semgrep, OPA/Rego, SonarQube, Checkov, ESLint |
| [Comparison Matrix](#comparison-matrix) | Side-by-side comparison across configuration dimensions |
| [Evidence and Citations](#evidence-and-citations) | Categorized sources per R-006 |
| [Recommendations](#recommendations) | Numbered recommendations for R-011 configurable rule set architecture |

---

## L0: Executive Summary

Five rule and policy configuration systems were analyzed to inform R-011 (Configurable Rule Sets) architecture for /eng-team and /red-team: Semgrep (YAML-based SAST rules), OPA/Rego (general-purpose policy engine), SonarQube (quality profile system), Checkov (infrastructure-as-code policies), and ESLint (JavaScript/TypeScript linting). The analysis reveals two fundamentally different architectural approaches: declarative rule definition (Semgrep YAML, Checkov YAML, ESLint flat config) where rules are expressed as data structures, and programmatic policy definition (OPA/Rego, Checkov Python, SonarQube custom rules) where rules are expressed as executable logic. Semgrep's YAML rule format provides the most directly applicable model for /eng-team and /red-team configurable rules -- it uses a structured schema with required fields (id, languages, message, pattern, severity), supports metavariable matching for context-aware rules, and enables custom rule authoring without requiring code changes to the core engine. OPA/Rego provides the most powerful general-purpose policy engine but introduces a domain-specific language (Rego) learning curve. SonarQube's quality profile system (with inheritance, extension, and per-project assignment) provides the best model for rule set management and organizational override. ESLint's flat config (introduced in 2022, matured in 2025) demonstrates the modern pattern of configuration-as-code with programmatic composition, cascading overrides, and the recently re-introduced `extends` keyword for config inheritance. The recommended architecture for /eng-team and /red-team is a YAML-first rule definition format (inspired by Semgrep), with a profile management system (inspired by SonarQube), and a cascading override mechanism (inspired by ESLint flat config), using OPA/Rego patterns for complex policy evaluation where declarative rules are insufficient.

---

## L1: Key Findings

### Finding 1: Semgrep's YAML Rule Format Is the Most Applicable Model for Agent-Based Rule Definition

Semgrep rules are defined in YAML with a structured schema: required fields include `id` (unique rule identifier), `languages` (applicable programming languages), `message` (human-readable description), `pattern` or `patterns` (what to match), and `severity` (ERROR, WARNING, INFO) (Semgrep Docs, 2025). Rules support pattern operators (`pattern`, `pattern-not`, `pattern-either`, `pattern-inside`, `pattern-regex`), metavariable matching (`metavariable-pattern`, `metavariable-regex`, `metavariable-comparison`), and taint tracking for data flow analysis. Custom rules are created by writing YAML files and placing them in accessible directories -- no compilation or code changes to Semgrep itself are required. The Semgrep Registry provides over 2,000 community rules as defaults that can be extended or overridden with custom rules. This architecture -- structured schema, declarative definition, no-code-change extensibility, community defaults with custom overrides -- is the pattern /eng-team and /red-team should adopt for their configurable rule sets.

### Finding 2: OPA/Rego Provides the Most Powerful General-Purpose Policy Engine but Requires a Learning Curve

OPA (Open Policy Agent) decouples policy decision-making from policy enforcement, using the Rego language for policy expression (OPA Documentation, 2025). Rego is a declarative language inspired by Datalog, designed for expressing policies over hierarchical data structures like JSON. OPA is domain-agnostic: it can express policies for API authorization, Kubernetes admission control, CI/CD pipeline gates, infrastructure compliance, and arbitrary business logic. Policies are organized into modules with package declarations, imports, and rule definitions. OPA supports schema validation (both external JSON Schema and embedded Rego annotations), testing frameworks, and multiple deployment models (standalone, sidecar, embedded). For /red-team, OPA/Rego is particularly relevant for scope enforcement policies: "given this proposed action (JSON input), does it comply with the engagement scope (Rego policy)?" However, Rego's learning curve makes it less suitable as a user-facing configuration format for R-011. The recommended approach is to use OPA/Rego internally for complex policy evaluation while exposing a simpler YAML configuration surface to users.

### Finding 3: SonarQube's Quality Profile System Provides the Best Model for Rule Set Management

SonarQube defines quality profiles as the mechanism for associating rule sets with projects (SonarQube Docs, 2025). Each profile activates a subset of available rules for a specific language, with configurable severity and parameters per rule. The key management patterns are: (1) Extension -- a child profile inherits all rules from a parent profile and adds additional rules; changes to the parent propagate to the child; (2) Copying -- a new independent profile initialized from an existing one; no inheritance relationship; (3) Per-project assignment -- each project can be assigned a specific profile, overriding the default; (4) Parameter overriding -- a profile can customize rule parameters differently from the rule's defaults (the rule is then considered "overridden" in that profile); (5) Rule inheritance -- parent/child relationships between profiles where parent changes dynamically propagate to children. This profile management model -- especially the extension/inheritance pattern and per-project assignment -- directly addresses R-011's requirement that users override default rules without modifying core skill code.

### Finding 4: Checkov Demonstrates Dual-Format Rule Authoring (YAML for Simple, Python for Complex)

Checkov supports both YAML and Python formats for custom policy definition (Checkov Docs, 2025). YAML policies handle attribute checks (verifying resource configuration values), connection state checks (verifying relationships between resources), and allow/deny lists (permitted/forbidden resource types). Python policies handle more complex logic that YAML cannot express: multi-resource validation, dynamic threshold calculation, and conditional logic. The configuration hierarchy follows: built-in policies (default), custom YAML policies (overlay), custom Python policies (full flexibility), and `.checkov.yaml` or `.checkov.yml` configuration file for runtime settings. The dual-format pattern (YAML for simple rules, Python for complex rules) is directly applicable to /eng-team and /red-team: most configurable rules can be expressed in YAML, but complex rules (e.g., multi-step attack chain validation for /red-team, complex architectural pattern verification for /eng-team) need a programmatic escape hatch.

### Finding 5: ESLint's Flat Config Demonstrates Modern Configuration Composition Patterns

ESLint transitioned from the legacy `.eslintrc` format to "flat config" (`eslint.config.js`) starting in 2022, with the system maturing through 2025 (ESLint Blog, March 2025). The flat config system introduces: (1) `defineConfig()` for type-safe configuration; (2) re-introduced `extends` keyword for config inheritance (after initially removing it); (3) cascading override where later configuration objects override earlier ones when there is a conflict; (4) glob-based file targeting where rules apply to specific file patterns; (5) `globalIgnores()` for explicit ignore patterns; (6) programmatic composition since config files are JavaScript/TypeScript modules. The key innovation is that configuration files are code, enabling dynamic composition (import other configs, conditionally apply rules, merge configs from packages). For /eng-team and /red-team, the ESLint flat config pattern informs how rule sets should compose: default rules from the skill, user-provided overrides that cascade on top, glob-based targeting for different file types or contexts, and programmatic composition for advanced use cases.

### Finding 6: All Five Tools Share a Common Override and Merge Architecture

Despite different domains and implementation languages, all five tools converge on a common pattern for rule management:

| Pattern | Semgrep | OPA/Rego | SonarQube | Checkov | ESLint |
|---------|---------|----------|-----------|---------|--------|
| **Default rules** | Registry rules | Built-in library | Default profiles | Built-in policies | Recommended configs |
| **Custom rules** | YAML files in directories | Rego modules in bundles | Profile customization | YAML/Python policies | Config objects |
| **Override mechanism** | Rule ID collision (custom overrides registry) | Package imports with override | Profile extension/copy | Config file precedence | Cascade (last wins) |
| **Disable mechanism** | `--exclude-rule` or config | Policy removal | Deactivate in profile | `--skip-check` | `"off"` rule value |
| **Per-project config** | `.semgrep.yml` per repo | Bundle per deployment | Profile per project | `.checkov.yml` per repo | `eslint.config.js` per project |

This convergence validates the architecture: default rules provided by the skill, user overrides through a documented mechanism, per-engagement or per-project configuration, and the ability to disable specific rules.

---

## L2: Detailed Analysis

### Semgrep Rule Format

#### Rule Schema

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `id` | Yes | string | Unique rule identifier (e.g., `security.owasp.sql-injection`) |
| `languages` | Yes | array | Target languages (e.g., `[python, javascript]`) |
| `message` | Yes | string | Human-readable finding description |
| `pattern` | Yes (or `patterns`) | string | Code pattern to match |
| `severity` | Yes | enum | `ERROR`, `WARNING`, or `INFO` |
| `metadata` | No | object | Arbitrary metadata (category, CWE, OWASP, references) |
| `fix` | No | string | Suggested automatic fix |
| `options` | No | object | Rule behavior options (e.g., `symbolic_propagation`) |
| `paths` | No | object | Include/exclude file paths |

#### Pattern Operators

| Operator | Description | Example Use |
|----------|-------------|-------------|
| `pattern` | Match exact code pattern | `hashlib.md5(...)` |
| `pattern-not` | Exclude matches | Exclude safe patterns |
| `pattern-either` | Match any of several patterns (OR) | Multiple vulnerability variants |
| `pattern-inside` | Match only within a context | Only in specific functions |
| `pattern-not-inside` | Exclude matches within a context | Not in test files |
| `pattern-regex` | Regex-based matching | Complex string patterns |
| `metavariable-pattern` | Filter by metavariable value | Type-specific checks |
| `metavariable-regex` | Regex on metavariable | Pattern on variable names |
| `metavariable-comparison` | Numeric comparison on metavariable | Threshold checks |
| `patterns` | Combine operators (AND) | Multi-condition rules |

#### Configuration Hierarchy

```
1. Semgrep Registry (community rules)    -- Default rules; always available
2. Organization rules (shared config)     -- Org-wide custom rules
3. Repository .semgrep.yml               -- Per-project configuration
4. CLI flags (--include, --exclude)       -- Runtime overrides
```

#### Example Rule Structure

```yaml
rules:
  - id: security.injection.sql-injection-formatted-string
    languages: [python]
    message: >-
      Potential SQL injection via string formatting.
      Use parameterized queries instead.
    severity: ERROR
    metadata:
      category: security
      cwe: CWE-89
      owasp: A03:2021
      confidence: HIGH
    patterns:
      - pattern: |
          cursor.execute($QUERY % ...)
      - pattern-not: |
          cursor.execute("..." % ())
    fix: cursor.execute($QUERY, (...))
```

### OPA/Rego Policy Language

#### Language Structure

| Concept | Description | Example |
|---------|-------------|---------|
| **Package** | Namespace for policy rules | `package authz.redteam` |
| **Import** | Reference external data or other packages | `import data.engagement.scope` |
| **Rule** | Policy decision (default or conditional) | `allow { ... }` |
| **Default** | Fallback value when no rule matches | `default allow = false` |
| **Comprehension** | Set/object/array generation | `targets := {t \| t := scope.targets[_]}` |
| **Function** | Reusable policy logic | `in_scope(target) { ... }` |
| **Test** | Built-in test framework | `test_allow_in_scope { ... }` |

#### OPA Architecture for Policy Enforcement

| Component | Function | Integration Pattern |
|-----------|----------|-------------------|
| **OPA Server** | Evaluates policies against input data | REST API or gRPC sidecar |
| **Policy Bundle** | Collection of Rego policies and data | Loaded from filesystem, HTTP, or OCI registry |
| **Input Document** | JSON data to evaluate against policies | Provided by calling application per request |
| **Decision** | Policy evaluation result | JSON response (allow/deny, additional context) |
| **Data** | External reference data for policies | JSON documents loaded alongside policies |

#### Example Policy Structure (Red Team Scope Enforcement)

```rego
package redteam.scope

import data.engagement.authorized_targets
import data.engagement.authorized_techniques
import data.engagement.time_window

default allow_action = false

# Allow action if target is in scope and technique is authorized
allow_action {
    input.target == authorized_targets[_]
    input.technique == authorized_techniques[_]
    time.now_ns() >= time_window.start_ns
    time.now_ns() <= time_window.end_ns
}

# Deny action with reason
deny[msg] {
    not input.target == authorized_targets[_]
    msg := sprintf("Target %v is not in authorized scope", [input.target])
}

deny[msg] {
    not input.technique == authorized_techniques[_]
    msg := sprintf("Technique %v is not authorized for this engagement", [input.technique])
}
```

### SonarQube Quality Profiles

#### Profile Management Model

| Feature | Description | R-011 Relevance |
|---------|-------------|-----------------|
| **Default Profile** | Built-in profile per language with Sonar-recommended rules | Skill-provided default rule set |
| **Profile Extension** | Child profile inherits parent; adds/overrides rules; parent changes propagate | User extends default rule set with additions |
| **Profile Copy** | Independent copy of an existing profile; no inheritance | User creates fully custom rule set |
| **Rule Activation** | Per-rule enable/disable within a profile | User enables/disables specific rules |
| **Parameter Override** | Custom parameter values per rule per profile | User tunes rule sensitivity |
| **Severity Override** | Custom severity per rule per profile | User adjusts rule priority |
| **Per-Project Assignment** | Each project can have a different profile | Per-engagement rule set selection |
| **Profile Comparison** | Compare two profiles to see differences | Audit custom vs. default |
| **Profile Backup/Restore** | Export/import profile definitions | Portable rule set configuration |

#### Rule Configuration Dimensions

| Dimension | Options | Description |
|-----------|---------|-------------|
| **Severity** | Blocker, Critical, Major, Minor, Info | Impact classification |
| **Type** | Bug, Vulnerability, Security Hotspot, Code Smell | Rule category |
| **Tags** | Arbitrary tags | Custom categorization |
| **Parameters** | Rule-specific | Configurable thresholds and patterns |
| **Status** | Active, Inactive | Enabled/disabled per profile |
| **Prioritized** | Yes/No (Enterprise) | Whether rule is prioritized for new code |

#### Profile Inheritance Model

```
Sonar Way (Default)
├── Organization Standard (Extension -- adds org rules)
│   ├── Team A Profile (Extension -- adds team-specific rules)
│   └── Team B Profile (Extension -- different team-specific rules)
└── Security Focused (Copy -- independent security-heavy profile)
```

### Checkov Custom Policies

#### Dual-Format Architecture

| Format | Use Case | Capabilities | Limitations |
|--------|----------|-------------|-------------|
| **YAML** | Simple attribute checks, connection state, allow/deny lists | Declarative; no code required; AND/OR logic; attribute matching; connection state checking | Cannot express complex conditional logic; no dynamic computation |
| **Python** | Complex validation, multi-resource checks, dynamic thresholds | Full programming language; any validation logic possible; access to Checkov API | Requires Python knowledge; more maintenance overhead |

#### YAML Policy Structure

| Section | Description | Required |
|---------|-------------|----------|
| **Metadata** | Policy ID, name, category, severity, guideline | Yes |
| **Definition** | Attribute conditions, connection state, resource type filter | Yes |
| **Operator** | AND/OR logic combining conditions | For composite policies |

#### Policy Types

| Type | Description | Example |
|------|-------------|---------|
| **Attribute** | Check resource configuration values | Verify S3 bucket encryption is enabled |
| **Connection State** | Check relationships between resources | Verify security group is attached to instance |
| **Resource Type** | Allow/deny specific resource types | Block specific resource types in environment |
| **Composite** | Combine multiple checks with AND/OR logic | Encryption enabled AND logging configured |

#### Configuration Precedence

```
1. Built-in policies (Checkov defaults)         -- Always present
2. External policy directory (--external-checks) -- Organization custom policies
3. .checkov.yaml configuration file              -- Per-project settings
4. CLI flags (--check, --skip-check)             -- Runtime overrides
```

### ESLint Flat Config

#### Configuration Architecture

| Concept | Legacy (.eslintrc) | Flat Config (eslint.config.js) |
|---------|-------------------|-------------------------------|
| **Format** | JSON, YAML, or JavaScript | JavaScript/TypeScript module |
| **Composition** | `extends` and `overrides` | Array of config objects; `extends` re-introduced in 2025 |
| **File targeting** | `overrides[].files` | `files` property on config objects |
| **Plugin loading** | String references (`"plugin:name/config"`) | Direct imports (`import plugin from "..."`); explicit loading |
| **Inheritance** | `extends: ["config-name"]` | `extends: [importedConfig]` (2025); array spread (`...configs`) |
| **Merge behavior** | Deep merge with conflict resolution | Last object wins in cascade |
| **Ignores** | `.eslintignore` file | `globalIgnores()` helper or `ignores` property |
| **Type safety** | No native type checking | `defineConfig()` with TypeScript inference |

#### Override and Merge Behavior

| Scenario | Behavior |
|----------|----------|
| Same rule in multiple config objects | Last config object wins |
| `extends` with local override | Extended config applied first; local overrides cascade on top |
| Glob-specific config | Applies only to matching files; merges with global config |
| Rule set to `"off"` | Disables rule regardless of prior config |
| Plugin provides recommended config | Imported and spread into config array; user overrides cascade |

#### Configuration Composition Pattern

```javascript
// eslint.config.js -- Modern flat config pattern
import { defineConfig, globalIgnores } from "eslint/config";
import securityPlugin from "eslint-plugin-security";

export default defineConfig([
  // Global ignores
  globalIgnores(["dist/", "node_modules/"]),

  // Base config (applies to all files)
  {
    rules: {
      "no-eval": "error",
      "no-implied-eval": "error",
    },
  },

  // Security plugin with recommended rules
  {
    extends: [securityPlugin.configs.recommended],
    files: ["**/*.js"],
  },

  // Project-specific overrides
  {
    files: ["src/**/*.js"],
    rules: {
      "security/detect-non-literal-regexp": "warn", // Downgrade for specific project
    },
  },
]);
```

---

## Comparison Matrix

### Rule Configuration System Comparison

| Dimension | Semgrep | OPA/Rego | SonarQube | Checkov | ESLint |
|-----------|---------|----------|-----------|---------|--------|
| **Rule definition format** | YAML | Rego (DSL) | Java (custom rules) + XML/JSON (rule config) | YAML + Python | JavaScript/TypeScript |
| **User configuration format** | YAML (.semgrep.yml) | Rego + JSON (data) | Web UI + API | YAML (.checkov.yaml) | JavaScript (eslint.config.js) |
| **Schema validation** | Yes (YAML schema) | Yes (Rego annotations + JSON Schema) | Yes (rule parameter types) | Yes (YAML schema) | Yes (TypeScript types via defineConfig) |
| **Override mechanism** | Rule ID collision (custom overrides default) | Package override + data overlay | Profile extension/copy | Config precedence + CLI flags | Cascade (last config wins) |
| **Merge behavior** | Custom rules overlay registry rules | Bundle merge; last loaded wins | Inheritance from parent profile | External checks added to built-in | Array of configs merged sequentially |
| **Default rules** | 2,000+ community registry rules | OPA library (limited) | Language-specific default profiles | 750+ built-in policies | No built-in; ecosystem configs (recommended, etc.) |
| **Custom rule authoring** | Write YAML file; no code changes | Write Rego module; no core changes | Write Java class + register | Write YAML or Python; no core changes | Write JS rule plugin; no core changes |
| **Rule versioning** | Git-based (rules in repo) | Bundle versioning + OCI registry | Profile history in database | Git-based (policies in repo) | npm package versioning |
| **Per-project configuration** | .semgrep.yml per repo | Bundle per deployment/cluster | Profile assignment per project | .checkov.yaml per repo | eslint.config.js per project |
| **Severity levels** | ERROR, WARNING, INFO | Custom (policy-defined) | Blocker, Critical, Major, Minor, Info | CRITICAL, HIGH, MEDIUM, LOW | error, warn, off |
| **Rule disable** | --exclude-rule or config exclusion | Policy removal or data override | Deactivate in profile | --skip-check | Set rule to "off" |
| **Testing framework** | semgrep --test | OPA test (built-in) | SonarQube test framework | pytest (Python policies) | RuleTester |
| **Registry/repository** | Semgrep Registry (public) | OPA Playground + community | SonarQube Marketplace | GitHub (checkov repo) | npm (eslint-plugin-*) |
| **Domain** | Source code analysis (SAST) | General-purpose policy (any domain) | Code quality and security | Infrastructure as code (IaC) | JavaScript/TypeScript linting |
| **Agent team relevance** | eng-security, eng-devsecops (SAST rules) | red-lead, red-team (scope policies) | eng-reviewer (quality gates) | eng-infra (IaC policies) | eng-frontend (JS/TS rules) |

### Configuration Pattern Comparison for R-011

| Pattern | Semgrep | OPA/Rego | SonarQube | Checkov | ESLint | R-011 Applicability |
|---------|---------|----------|-----------|---------|--------|---------------------|
| **User creates custom rules** | Write YAML in directory | Write Rego module | Write Java rule class | Write YAML/Python | Write JS rule plugin | All patterns applicable; YAML preferred for simplicity |
| **User overrides default rules** | Custom rule with same ID | Data overlay changes policy inputs | Override severity/params in profile | Skip-check or override in config | Set rule to different severity | Profile extension model (SonarQube) is most user-friendly |
| **User disables default rules** | Exclude in config | Remove from bundle | Deactivate in profile | Skip-check | Set to "off" | All support this; need explicit mechanism |
| **User extends default set** | Add YAML files to directory | Add Rego modules to bundle | Extend profile | Add policies to directory | Add config objects to array | Additive extension is straightforward across all |
| **Organization shares custom rules** | Shared rule directory/registry | Shared bundle repository | Parent profile for organization | Shared policy repository | Published npm package | Profile hierarchy (SonarQube) is most mature for org management |
| **Rule versioning** | Git tags/branches | OCI registry tags | Profile export/import | Git tags/branches | Semver (npm) | Git-based versioning is simplest |

---

## Evidence and Citations

### Industry Leaders

| Source | Date | Content |
|--------|------|---------|
| [Semgrep -- Rule Structure Syntax](https://semgrep.dev/docs/writing-rules/rule-syntax) | 2025 | Authoritative YAML rule schema: required fields, pattern operators, metavariables |
| [Semgrep -- Writing Rules Overview](https://semgrep.dev/docs/writing-rules/overview) | 2025 | Custom rule authoring methodology and best practices |
| [Semgrep -- Running Rules](https://semgrep.dev/docs/running-rules) | 2025 | Rule execution, configuration, and registry integration |
| [OPA -- Open Policy Agent Documentation](https://www.openpolicyagent.org/docs/latest/) | 2025 | Authoritative OPA documentation including deployment and integration |
| [OPA -- Policy Language (Rego)](https://www.openpolicyagent.org/docs/policy-language) | 2025 | Rego language specification: modules, rules, comprehensions |
| [OPA -- Policy Reference](https://www.openpolicyagent.org/docs/policy-reference) | 2025 | Complete Rego language reference |
| [SonarQube -- Managing Quality Profiles (2025.2)](https://docs.sonarsource.com/sonarqube-server/2025.2/quality-standards-administration/managing-quality-profiles) | 2025 | Profile creation, extension, copying, assignment |
| [SonarQube -- Understanding Quality Profiles (2025.5)](https://docs.sonarsource.com/sonarqube-server/2025.5/quality-standards-administration/managing-quality-profiles/understanding-quality-profiles) | 2025 | Profile inheritance, rule activation, parameter override |
| [SonarQube -- Adding Coding Rules (2025.1 LTA)](https://docs.sonarsource.com/sonarqube-server/2025.1/extension-guide/adding-coding-rules) | 2025 | Custom rule development for SonarQube |

### Industry Experts

| Source | Date | Content |
|--------|------|---------|
| [Semgrep -- Custom Rules for Semgrep Secrets](https://semgrep.dev/docs/semgrep-secrets/rules) | 2025 | Custom rule authoring for secrets detection |
| [Semgrep -- Rule Structure Syntax Examples](https://semgrep.dev/docs/writing-rules/rule-ideas) | 2025 | Practical rule writing examples and patterns |
| [Semgrep -- Contributing Rules to Registry](https://semgrep.dev/docs/contributing/contributing-to-semgrep-rules-repository) | 2025 | Community rule contribution standards |
| [Spacelift -- OPA Rego Language Tutorial](https://spacelift.io/blog/open-policy-agent-rego) | 2025 | Comprehensive Rego tutorial with practical examples |
| [Komodor -- OPA Features, Use Cases, Getting Started](https://komodor.com/learn/open-policy-agent-opa-features-use-cases-and-how-to-get-started/) | 2025 | OPA architecture, deployment models, integration patterns |
| [SonarQube -- Editing a Quality Profile](https://docs.sonarsource.com/sonarqube-server/quality-standards-administration/managing-quality-profiles/editing-a-custom-quality-profile) | 2025 | Detailed profile editing and customization guide |
| [Checkov -- Custom Policies Overview](https://www.checkov.io/3.Custom%20Policies/Custom%20Policies%20Overview.html) | 2025 | Checkov custom policy architecture (YAML + Python dual format) |
| [Checkov -- YAML Custom Policies](https://www.checkov.io/3.Custom%20Policies/YAML%20Custom%20Policies.html) | 2025 | YAML policy structure, attribute checks, connection state, allow/deny lists |
| [Checkov -- Python Custom Policies](https://www.checkov.io/3.Custom%20Policies/Python%20Custom%20Policies.html) | 2025 | Python policy structure for complex validation logic |
| [ESLint -- Flat Config Evolving with extends](https://eslint.org/blog/2025/03/flat-config-extends-define-config-global-ignores/) | March 2025 | Re-introduced extends, defineConfig(), globalIgnores() |
| [ESLint -- Configuration Files](https://eslint.org/docs/latest/use/configure/configuration-files) | 2025 | Flat config format specification |
| [ESLint -- Combine Configs](https://eslint.org/docs/latest/use/configure/combine-configs) | 2025 | Config composition and merge behavior |
| [ESLint -- Configuration Migration Guide](https://eslint.org/docs/latest/use/configure/migration-guide) | 2025 | Legacy to flat config migration patterns |

### Industry Innovators

| Source | Date | Content |
|--------|------|---------|
| [Semgrep GitHub -- semgrep-rules Repository](https://github.com/semgrep/semgrep-rules) | 2025 | 2,000+ community rules; rule format examples |
| [OPA GitHub -- open-policy-agent/opa](https://github.com/open-policy-agent/opa) | 2025 | OPA source code and documentation |
| [Checkov GitHub -- bridgecrewio/checkov](https://github.com/bridgecrewio/checkov) | 2025 | Checkov source with 750+ built-in policies |
| [HashiCorp -- OPA Policies for Terraform Enterprise](https://developer.hashicorp.com/terraform/enterprise/policy-enforcement/define-policies/opa) | 2025 | OPA integration in infrastructure-as-code workflows |
| [GuardRails -- Custom Engine Rules](https://docs.guardrails.io/docs/custom-engine-rules) | 2025 | Custom rule integration for Semgrep-based engine |
| [Semgrep -- Write Custom Rules (Editor)](https://semgrep.dev/docs/semgrep-code/editor) | 2025 | UI-based and YAML-based rule authoring |
| [Spacelift -- What is Checkov](https://spacelift.io/blog/what-is-checkov) | 2025 | Checkov overview and custom policy patterns |

### Community Leaders

| Source | Date | Content |
|--------|------|---------|
| [OPA -- Homepage](https://www.openpolicyagent.org/) | 2025 | Official OPA project site (CNCF graduated project) |
| [ESLint -- Pluggable JavaScript Linter (New Config System)](https://eslint.org/blog/2022/08/new-config-system-part-2/) | 2022 | Original flat config introduction |
| [ESLint -- Plugin Migration to Flat Config](https://eslint.org/docs/latest/extend/plugin-migration-flat-config) | 2025 | Plugin author guidance for flat config compatibility |

### Community Experts

| Source | Date | Content |
|--------|------|---------|
| [Semgrep Blog -- Writing Semgrep Rules: A Methodology](https://semgrep.dev/blog/2020/writing-semgrep-rules-a-methodology/) | 2020 | Rule writing methodology and best practices |
| [AWS Prescriptive Guidance -- Centralized Custom Checkov Scanning](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/centralized-custom-checkov-scanning.html) | 2025 | Centralized Checkov policy management pattern for organizations |
| [Rightmove Tech Blog -- Guarding Infrastructure with Policy as Code](https://rightmove.blog/how-we-guard-our-infrastructure-with-policy-as-code/) | 2025 | Real-world Checkov policy-as-code implementation |
| [Raul Melo -- Navigating ESLint Flat Config](https://raulmelo.me/en/blog/migration-eslint-to-flat-config) | 2025 | Practitioner migration experience to flat config |

### Community Innovators

| Source | Date | Content |
|--------|------|---------|
| [Mohamed Lamine Allal (Medium) -- ESLint Flat Config Deep Dive](https://allalmohamedlamine.medium.com/eslint-flat-config-and-new-system-an-ultimate-deep-dive-2023-46aa151cbf2b) | 2023 | Comprehensive flat config analysis and migration patterns |
| [Checkov GitHub -- YAML Custom Policies (docs)](https://github.com/bridgecrewio/checkov/blob/main/docs/3.Custom%20Policies/YAML%20Custom%20Policies.md) | 2025 | YAML policy documentation source |

---

## Recommendations

### R-RULES-001: Adopt YAML-First Rule Definition Format

/eng-team and /red-team configurable rule sets SHOULD use YAML as the primary rule definition format, inspired by Semgrep's schema. YAML provides: structured, validatable schema; no programming language dependency; human-readable and machine-parseable; version-controllable in Git; familiar to security practitioners. The rule schema should include: `id` (unique identifier), `category` (security, architecture, coding-standards, engagement), `severity` (critical, high, medium, low, info), `description` (what the rule checks), `rationale` (why the rule exists), `references` (standards, CWEs, ATT&CK techniques), and `configuration` (rule-specific parameters). Priority: HIGH.

### R-RULES-002: Implement Profile Management System Inspired by SonarQube

/eng-team and /red-team SHOULD implement a profile management system with: (1) Default profiles provided by each skill (e.g., "OWASP ASVS Level 2" for /eng-team, "PTES Standard" for /red-team); (2) Profile extension where users inherit the default and add/override rules without modifying the original; (3) Per-engagement profile assignment where different engagements can use different profiles; (4) Profile inheritance where organizational profiles serve as parents for team-specific child profiles. This directly satisfies R-011's requirement that users "override default rules without modifying core skill code." Priority: HIGH.

### R-RULES-003: Support Cascading Override Mechanism

Rule resolution SHOULD follow a cascading override pattern inspired by ESLint flat config:

```
1. Skill defaults (lowest priority)     -- Built into skill code
2. Organization profile                 -- Shared across org
3. Team/project profile                 -- Per-team customization
4. Engagement overrides                 -- Per-engagement tweaks
5. Runtime flags (highest priority)     -- Command-line overrides
```

Later layers override earlier layers. Users can disable a default rule by setting its severity to "off" at any layer. This provides maximum flexibility while maintaining sensible defaults. Priority: HIGH.

### R-RULES-004: Provide Dual-Format Rule Authoring (YAML + Python)

Following Checkov's pattern, /eng-team and /red-team SHOULD support both YAML (for simple declarative rules) and Python (for complex programmatic rules). YAML handles: attribute checks, pattern matching, threshold comparisons, and standard validation. Python handles: multi-step validation, dynamic computation, cross-rule dependencies, and complex conditional logic. The Python escape hatch ensures R-011 is not limited by YAML's expressiveness while keeping the common case simple. Priority: MEDIUM.

### R-RULES-005: Use OPA/Rego Patterns for /red-team Scope Enforcement

/red-team scope enforcement policies SHOULD follow OPA/Rego architectural patterns: policy evaluation decoupled from enforcement, structured input documents (proposed actions as JSON), policy decisions as structured output (allow/deny with reasons), and data-driven policies where engagement scope is loaded as data, not hardcoded. This does not require embedding the OPA runtime -- the pattern can be implemented in Python -- but the architectural separation of policy decision from enforcement is the critical design principle. Priority: MEDIUM.

### R-RULES-006: Define Standard Rule Schema for Both Skills

A shared rule schema SHOULD be defined that both /eng-team and /red-team rule sets follow:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier (e.g., `eng.owasp.a01.broken-access-control`) |
| `name` | string | Yes | Human-readable name |
| `category` | enum | Yes | security, architecture, coding, testing, engagement, methodology |
| `severity` | enum | Yes | critical, high, medium, low, info |
| `description` | string | Yes | What the rule checks |
| `rationale` | string | Yes | Why the rule exists |
| `references` | array | No | Standards (CWE, OWASP, ATT&CK), URLs |
| `default` | enum | Yes | enabled, disabled |
| `configurable_params` | object | No | Rule-specific tunable parameters |
| `applicable_agents` | array | No | Which agents this rule applies to |
| `tags` | array | No | Custom tags for filtering |

This shared schema enables cross-skill rule management and consistent user experience. Priority: HIGH.

### R-RULES-007: Implement Rule Versioning Through Git

Rule sets SHOULD be versioned using Git, following the Semgrep and Checkov pattern of storing rules in version-controlled directories. Rule set versions should be tagged (e.g., `rules-v1.0.0`) and engagements should pin to a specific rule set version. This enables: reproducible engagements, rule set rollback, audit trail of rule changes, and difference analysis between versions. Priority: MEDIUM.

### R-RULES-008: Provide Rule Testing Framework

Custom rules SHOULD be testable before deployment, following patterns from all five analyzed tools: Semgrep (`--test`), OPA (built-in test), SonarQube (test framework), Checkov (pytest), ESLint (RuleTester). The testing framework should support: positive tests (rule triggers on known-bad input), negative tests (rule does not trigger on known-good input), and parameter variation tests (rule behaves correctly across configuration values). This prevents broken rules from disrupting engagements. Priority: MEDIUM.

### R-RULES-009: Ship Comprehensive Default Rule Sets Mapped to Standards

/eng-team SHOULD ship default rule sets mapped to:
- OWASP ASVS 5.0 (3 levels: L1 baseline, L2 standard, L3 high-assurance)
- OWASP Top 10 2025 (10 risk categories)
- CWE Top 25 2025 (25 weakness types)
- CIS Benchmarks (infrastructure hardening)
- NIST SSDF practices (governance compliance)

/red-team SHOULD ship default rule sets mapped to:
- MITRE ATT&CK (14 tactics with technique selections)
- PTES (7 phases with technique mappings)
- OSSTMM (5 channels with testing methodology)
- OWASP Testing Guide (test categories)

These defaults give users a production-ready starting point while R-011 enables full customization. Priority: HIGH.

### R-RULES-010: Document Override Mechanism in User-Facing Documentation

The rule set override mechanism MUST be documented with clear examples showing: how to view the active rule set, how to extend defaults with additional rules, how to override a default rule's severity, how to disable a default rule, how to create a custom profile, and how to assign a profile to an engagement. Documentation should include both /eng-team and /red-team examples. This ensures R-011 is usable, not just implemented. Priority: HIGH.
