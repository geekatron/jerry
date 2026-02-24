# C-002: Defensive Tool Ecosystem Survey

> Stream C: Tool Integration | PROJ-010 Cyber Ops | Phase 1 Research

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | High-level findings and strategic implications |
| [L1: Key Findings](#l1-key-findings) | Structured findings by tool category |
| [L2: Detailed Analysis](#l2-detailed-analysis) | Per-tool deep dive with API details |
| [Evidence and Citations](#evidence-and-citations) | Dated sources, categorized |
| [Recommendations](#recommendations) | Priority tools and adapter architecture |

---

## L0: Executive Summary

Defensive and security engineering tools present a more uniform integration landscape than offensive tools. The majority expose well-documented REST APIs (SonarQube, Snyk, Checkov/Bridgecrew, Checkmarx), structured CLI output (Semgrep, Trivy, Checkov), or both. The SARIF (Static Analysis Results Interchange Format) standard has emerged as the primary interchange format across SAST/DAST tools, providing a natural normalization layer for agentic consumption. OWASP ZAP stands out as the strongest open-source DAST integration target with its comprehensive REST API and automation framework. For SAST, Semgrep offers the best combination of CLI automation, YAML rule authoring (which is LLM-friendly), and structured output. Trivy provides broad coverage across containers, IaC, and Kubernetes with native JSON output. Configuration-driven dependency tools (Dependabot, Renovate) integrate via repository configuration files rather than runtime APIs, making them better suited to agent-generated configuration than real-time interaction.

---

## L1: Key Findings

### Finding 1: SARIF as Universal Output Standard

SARIF v2.1.0 (OASIS standard) has achieved broad adoption across security tooling:
- **Native SARIF output**: CodeQL, Semgrep, Nuclei, Trivy, Checkmarx, Burp Suite DAST
- **SARIF conversion available**: SonarQube, Snyk, ZAP (via plugins)
- **SARIF consumption**: GitHub Code Scanning, Azure DevOps, Visual Studio, VS Code

This means an agent that can parse SARIF can consume findings from most security tools through a single parser. SARIF includes severity, location (file/line), rule metadata, and fix suggestions -- all structured and machine-readable.

### Finding 2: Two Distinct Integration Patterns for Defensive Tools

**Pattern A -- Pipeline Integration (CI/CD):** Tools like Semgrep, Trivy, Checkov, and CodeQL are designed to run in CI/CD pipelines. They accept code/configuration as input and produce findings as output. Integration is CLI-based with structured output.

**Pattern B -- Platform API:** Tools like SonarQube, Snyk, Checkmarx, and Burp Suite DAST are platforms with persistent state. Integration is via REST/GraphQL APIs with authentication, project management, and historical data access.

For Jerry skills, Pattern A tools are simpler to integrate (stateless CLI wrapping) while Pattern B tools offer richer data but require session management.

### Finding 3: YAML Rule Authoring Is LLM-Friendly

Both Semgrep and Checkov use YAML-based rule/policy definitions that are well-suited to LLM generation:
- **Semgrep rules**: Pattern-matching DSL with metavariables, boolean operators, and fix suggestions
- **Checkov policies**: Attribute checks and connection-state validation for IaC resources
- **Nuclei templates**: Vulnerability detection with matchers and extractors

An agent can not only consume findings from these tools but also GENERATE custom rules/templates, creating a bidirectional integration surface.

### Finding 4: Webhook Patterns Enable Event-Driven Integration

Several platforms support webhooks for event-driven integration:
- **SonarQube**: Webhooks on analysis completion (up to 10 per project + 10 global, HMAC-SHA256 verification)
- **Snyk**: Webhook notifications for new vulnerabilities
- **Dependabot/Renovate**: PR-based notifications via repository events
- **ZAP**: Automation framework with event-driven scan pipelines

This suggests a future architecture where agents respond to security events rather than only initiating scans.

---

## L2: Detailed Analysis

### Tool Inventory

| Tool | API Type | Automation Level | Input Format | Output Format | Auth | Agentic Feasibility |
|------|----------|-----------------|--------------|---------------|------|---------------------|
| SonarQube | REST API + Webhooks | High | HTTP API calls | JSON, webhooks | Token / HMAC | HIGH -- comprehensive API, webhook-driven |
| Semgrep | CLI + Cloud API | High | YAML rules, CLI flags | JSON, SARIF, text | None (CLI), API key (Cloud) | HIGH -- structured output, LLM-writable rules |
| Snyk | REST API + CLI | High | CLI flags, API calls | JSON, SARIF, SBOM | API key / OAuth | HIGH -- comprehensive API, SBOM generation |
| Trivy | CLI + Operator | High | CLI flags | JSON, table, SARIF, CycloneDX | None (CLI) | HIGH -- multi-target scanning, JSON output |
| OWASP ZAP | REST API + Automation Framework | High | HTTP API, YAML automation plans | JSON, HTML, XML, Markdown | API key | HIGH -- full REST API with OpenAPI spec |
| Checkov | CLI + Bridgecrew API | High | CLI flags, YAML/Python policies | JSON, SARIF, JUnit | None (CLI), API key (Bridgecrew) | HIGH -- custom policy authoring, structured output |
| Dependabot | Configuration-driven | Medium | YAML config file | PR-based | GitHub token | MEDIUM -- config generation, not runtime API |
| Renovate | Configuration-driven | High | JSON config file | PR-based | Platform tokens | MEDIUM-HIGH -- rich config, but PR-based output |
| CodeQL | CLI + GitHub API | High | QL queries, CLI flags | SARIF | GitHub token | HIGH -- powerful analysis, SARIF output |
| Checkmarx One | REST API | High | API calls | JSON, SARIF | OAuth / API key | HIGH -- comprehensive API, SARIF support |
| Fortify | REST API | Medium | API calls | FPR (proprietary), PDF | SSC token | MEDIUM -- proprietary format, complex setup |
| Nikto | CLI | Low-Medium | CLI flags | JSON, XML, HTML, CSV, text | None | MEDIUM -- simple scanner, JSON output available |

### Per-Tool Deep Dive

#### SonarQube

**API Surface:**
- **REST API (Web API)**: Comprehensive endpoints for project management, issue querying, quality gate status, metrics, rules management, and webhook configuration
- **Webhooks**: Up to 10 per project + 10 global; HMAC-SHA256 authentication; triggered on analysis completion
- **Quality Profiles**: Configurable rule sets per language with API management
- **Quality Gates**: Pass/fail conditions with API-queryable status

**Key Automation Capabilities:**
- Project creation and configuration via API
- Trigger analysis and retrieve results
- Query issues by severity, type, component, date range
- Quality gate status polling
- Webhook-based event notification
- Quality profile and rule management
- Historical metrics and trend data

**Integration Pattern:**
```
CI/CD -> sonar-scanner -> SonarQube Server -> Analysis Complete
Agent -> REST API -> Query Issues, Quality Gate Status
Agent <- Webhook <- Analysis Completion Event
```

**Agentic Feasibility: HIGH**
- Mature REST API with extensive endpoint coverage
- Webhook support enables event-driven agent patterns
- Quality gate status provides clear pass/fail signals
- Issue data is structured with severity, effort, component paths
- Version 2025.2/2025.5 documentation confirms active API maintenance

**Key Limitation:** Requires running SonarQube server instance. Community edition has limited features versus commercial editions.

#### Semgrep

**API Surface:**
- **CLI**: `semgrep scan` with `--config` for rule specification, `--json` and `--sarif` output
- **Rule Syntax**: YAML-based DSL with pattern matching, metavariables, boolean operators (`pattern-either`, `pattern-not`, `metavariable-pattern`)
- **Semgrep Registry**: Community rule repository with `--config auto` for automatic rule selection
- **Semgrep Cloud API**: Platform API for organization-level rule management and deployment
- **MCP Server**: Semgrep provides an MCP server for AI agent integration (confirmed 2025)

**Key Automation Capabilities:**
- Static analysis with custom YAML rules
- Pattern-based code search (semantic, not text-based)
- Autofix suggestions in rules
- Multi-language support (30+ languages)
- CI/CD integration with exit codes
- Rule deployment automation via API
- Windows and multicore support (2025+)

**YAML Rule Structure:**
```yaml
rules:
  - id: example-rule
    pattern: $X == $X
    message: "Comparison of $X with itself is always true"
    languages: [python]
    severity: WARNING
    fix: "True"
```

**Integration Pattern:**
```
Agent -> Generate YAML Rules -> semgrep scan --config rules.yaml --json
      -> Parse JSON/SARIF Output -> Structured Findings
      -> OR: Semgrep MCP Server -> Direct Tool Integration
```

**Agentic Feasibility: HIGH**
- YAML rule syntax is LLM-friendly (agents can generate custom rules)
- JSON/SARIF output is structured and comprehensive
- `--config auto` provides sensible defaults without configuration
- Semgrep MCP server enables direct agent integration
- Semantic pattern matching provides higher quality results than regex-based tools
- Autofix capability means agents can suggest and apply fixes

**Key Limitation:** Advanced features (organization-wide policies, custom rule deployment at scale) require Semgrep Cloud subscription.

#### Snyk

**API Surface:**
- **REST API**: Comprehensive endpoints for project management, issue querying, SBOM generation, and vulnerability testing
- **CLI**: `snyk test`, `snyk monitor`, `snyk sbom`, `snyk container`, `snyk iac`
- **SBOM APIs**: Generate and test SBOMs via REST endpoints
- **Webhooks**: Vulnerability notification events

**Key Automation Capabilities:**
- Open source dependency vulnerability scanning
- Container image scanning
- Infrastructure as Code (IaC) scanning
- SBOM generation (CycloneDX v1.4-1.6, SPDX v2.3)
- SBOM testing for vulnerabilities via API
- License compliance checking
- Fix PR generation
- CI/CD pipeline integration

**Integration Pattern:**
```
Agent -> snyk CLI -> test/monitor/sbom commands -> JSON output
      -> REST API -> Project queries, SBOM generation
      -> SBOM API -> Vulnerability testing against SBOMs
```

**Agentic Feasibility: HIGH**
- Comprehensive REST API with well-documented endpoints
- CLI produces structured JSON output
- SBOM generation provides standardized dependency information
- Multiple scanning domains (SCA, containers, IaC) in single tool
- Fix suggestions are actionable

**Key Limitation:** Enterprise plan required for some features (SBOM generation). Free tier has limited scanning capacity.

#### Trivy (Aqua Security)

**API Surface:**
- **CLI**: Multi-target scanner with `--format json` output
- **Trivy Operator**: Kubernetes-native CRD-based continuous scanning
- **Output formats**: JSON, table, SARIF, CycloneDX, SPDX, template-based custom formats
- **Format conversion**: Can convert between output formats without re-scanning

**Key Automation Capabilities:**
- Container image vulnerability scanning
- Filesystem and repository scanning
- Kubernetes cluster scanning (misconfigurations + vulnerabilities)
- IaC scanning (Terraform, CloudFormation, Kubernetes manifests)
- SBOM generation and scanning
- License scanning
- Secret detection
- OCI registry scanning
- VEX (Vulnerability Exploitability eXchange) support

**Integration Pattern:**
```
Agent -> trivy image/fs/k8s/config -> --format json -> Structured Findings
      -> trivy convert -> Format Transformation
      -> Trivy Operator -> Kubernetes CRDs -> K8s API Queries
```

**Agentic Feasibility: HIGH**
- Broad scanning coverage (images, filesystems, K8s, IaC, SBOMs)
- Native JSON output is well-structured
- SARIF output for integration with code scanning platforms
- No authentication needed for CLI usage
- Trivy Operator provides continuous monitoring with Kubernetes API access
- Format conversion eliminates need for re-scanning

**Key Limitation:** Vulnerability database requires periodic updates. Kubernetes scanning requires kubectl access.

#### OWASP ZAP

**API Surface:**
- **REST API**: Comprehensive API with OpenAPI specification available
- **Automation Framework**: YAML-based scan plan configuration
- **Docker API Scanning**: `zap-api-scan.py` for OpenAPI/SOAP/GraphQL
- **Python API Client**: `python-owasp-zap-v2.4` package
- **Add-on system**: Extensible via marketplace add-ons

**Key Automation Capabilities:**
- Spider (crawling) with AJAX spider support
- Active and passive scanning
- API scanning (OpenAPI, SOAP, GraphQL)
- Authentication handling (form-based, script-based, SSO)
- Context-based scan scoping
- Scan policy configuration
- Report generation (JSON, HTML, XML, Markdown)
- CI/CD integration via Docker images and CLI

**Integration Pattern:**
```
Agent -> ZAP REST API -> Spider/Scan/Results endpoints
      -> Automation Framework YAML -> Declarative scan plans
      -> zap-api-scan.py -> API definition scanning
      -> Python Client -> Programmatic control
```

**Agentic Feasibility: HIGH**
- Full REST API with OpenAPI spec enables automated client generation
- Automation Framework YAML plans are agent-writable
- Python client library available for direct integration
- Docker images enable ephemeral scanning instances
- Free and open source (Checkmarx-funded since 2024)
- Version 2.17.0 (December 2025) confirms active development

**Key Limitation:** Active scanning can be slow for large applications. Authentication setup can be complex for modern SSO applications.

#### Checkov (Bridgecrew / Palo Alto Networks)

**API Surface:**
- **CLI**: `checkov -d . --output json` with comprehensive flag options
- **Custom Policies (YAML)**: Attribute checks, connection-state validation, AND/OR logic
- **Custom Policies (Python)**: Full Python programmability via BaseCheck class
- **Bridgecrew Platform API**: Centralized policy management and scan results

**Key Automation Capabilities:**
- Infrastructure as Code scanning (Terraform, CloudFormation, Kubernetes, Helm, ARM, Serverless)
- Custom policy authoring in YAML or Python
- Shared policy libraries across teams
- JSON, SARIF, JUnit, and other output formats
- CI/CD pipeline integration
- Bridgecrew platform synchronization

**YAML Policy Structure:**
```yaml
metadata:
  id: "CKV2_CUSTOM_1"
  name: "Ensure S3 bucket has encryption"
  category: "ENCRYPTION"
definition:
  cond_type: "attribute"
  resource_types:
    - "aws_s3_bucket"
  attribute: "server_side_encryption_configuration"
  operator: "exists"
```

**Integration Pattern:**
```
Agent -> Generate YAML/Python Policies -> checkov scan --output json
      -> Parse JSON/SARIF Output -> Structured Findings
      -> Bridgecrew API -> Centralized Policy Management
```

**Agentic Feasibility: HIGH**
- YAML policy syntax is LLM-friendly for custom rule generation
- JSON/SARIF output is structured
- Broad IaC framework coverage
- Shared policy libraries reduce duplication
- Bridgecrew API enables centralized management

**Key Limitation:** Some advanced features require Bridgecrew/Prisma Cloud subscription.

#### Dependabot / Renovate

**API Surface:**
- **Dependabot**: YAML configuration (`.github/dependabot.yml`), GitHub API for PR management
- **Renovate**: JSON configuration (`renovate.json`), supports 90+ package managers, GitHub/GitLab/Bitbucket/Azure DevOps

**Key Automation Capabilities:**
- Automated dependency update PR generation
- Version pinning and range management
- Auto-merge configuration for trusted updates
- Grouping related updates
- Scheduling (daily/weekly/monthly)
- Security update prioritization

**Integration Pattern:**
```
Agent -> Generate/Modify Config Files -> Repository Push
      -> Tool Creates PRs -> GitHub/GitLab API -> PR Review
```

**Agentic Feasibility: MEDIUM**
- Configuration-driven rather than API-driven at runtime
- Agent generates config files, tool handles execution
- PR-based output requires repository API interaction for monitoring
- Renovate's richer configuration offers more agent-tunable parameters
- No real-time interaction model -- async, event-driven

**Key Limitation:** Not suitable for real-time agent interaction. Best used for configuration generation and PR monitoring.

#### CodeQL (GitHub)

**API Surface:**
- **CLI**: `codeql database create`, `codeql database analyze` with SARIF output
- **GitHub Actions**: Automated CI/CD integration
- **Code Scanning API**: REST API for uploading SARIF and querying alerts
- **QL Language**: Purpose-built query language for code analysis

**Key Automation Capabilities:**
- Deep semantic code analysis
- Custom QL query authoring
- SARIF output with precise source locations
- GitHub Code Scanning integration
- Database creation and analysis pipeline
- Multi-language support (C/C++, C#, Go, Java, JavaScript, Python, Ruby, Swift)

**Integration Pattern:**
```
Agent -> codeql database create -> Code Database
      -> codeql database analyze --format=sarifv2.1.0 -> SARIF Results
      -> GitHub API -> Upload Results / Query Alerts
```

**Agentic Feasibility: HIGH**
- SARIF output is the gold standard for structured findings
- GitHub Code Scanning API provides cloud-based result management
- QL queries are powerful but have a learning curve
- CI/CD integration is well-established
- Free for public repositories, included with GitHub Advanced Security for private

**Key Limitation:** QL language has a steep learning curve. Database creation can be slow for large codebases.

#### Checkmarx One / Fortify

**Checkmarx One API Surface:**
- REST API with OAuth authentication
- Project management, scan initiation, result querying
- SARIF output support
- Webhook integration
- SAST, SCA, DAST, API security in single platform

**Fortify API Surface:**
- REST API via Software Security Center (SSC)
- Proprietary FPR format (with some SARIF conversion support)
- 1,700+ vulnerability categories
- Deep SAST analysis

**Agentic Feasibility:**
- **Checkmarx One: HIGH** -- Modern REST API, SARIF output, comprehensive scanning
- **Fortify: MEDIUM** -- Proprietary format, complex SSC infrastructure, but deep analysis

**Key Limitation:** Both are commercial products with significant licensing costs. Fortify's proprietary FPR format creates integration friction.

#### Nikto

**API Surface:**
- **CLI only**: `nikto -h <target> -o results.json -Format json`
- **Output formats**: JSON, XML, HTML, CSV, text, SQL
- **Docker image**: `sullo/nikto` for containerized scanning

**Agentic Feasibility: MEDIUM**
- Simple web server scanner (surface-level, not deep DAST)
- JSON output is available and structured
- Quick execution for basic checks
- Limited scope compared to ZAP or Burp Suite
- Good for complementary fast-check scanning

---

## Evidence and Citations

### Primary Sources (accessed 2026-02-22)

**SonarQube:**
- [SonarQube Webhooks Documentation (v2025.2)](https://docs.sonarsource.com/sonarqube-server/2025.2/project-administration/webhooks/) -- Webhook configuration and HMAC
- [SonarQube Webhooks Documentation (v2025.5)](https://docs.sonarsource.com/sonarqube-server/2025.5/project-administration/webhooks/) -- Latest version webhooks
- [SonarQube API Documentation](https://www.sonarsource.com/resources/library/application-programming-interface/) -- REST API overview

**Semgrep:**
- [Semgrep Rule Syntax](https://semgrep.dev/docs/writing-rules/rule-syntax) -- YAML rule structure
- [Semgrep CLI Reference](https://semgrep.dev/docs/cli-reference) -- CLI flags and options
- [Semgrep Rules Repository (GitHub)](https://github.com/semgrep/semgrep-rules) -- Community rules
- [Semgrep Rule Deployment Automation](https://semgrep.dev/docs/kb/semgrep-appsec-platform/automate-rules-deployment) -- API-based deployment
- [Semgrep Review 2026 (AppSec Santa)](https://appsecsanta.com/semgrep) -- Current capabilities

**Snyk:**
- [Snyk CLI SBOM Command](https://docs.snyk.io/developer-tools/snyk-cli/commands/sbom) -- SBOM generation
- [Snyk SBOM REST API](https://docs.snyk.io/snyk-api/using-specific-snyk-apis/sbom-apis/rest-api-get-a-projects-sbom-document) -- API endpoint
- [Snyk CLI Commands Summary](https://docs.snyk.io/developer-tools/snyk-cli/cli-commands-and-options-summary) -- Full CLI reference
- [Creating SBOMs with Snyk CLI (Blog)](https://snyk.io/blog/creating-sboms-snyk-cli/) -- SBOM workflow

**Trivy:**
- [Trivy Kubernetes CLI Reference](https://trivy.dev/docs/latest/references/configuration/cli/trivy_kubernetes/) -- K8s scanning
- [Trivy Cluster Scanning Tutorial](https://trivy.dev/docs/latest/tutorials/kubernetes/cluster-scanning/) -- Automation guide
- [Trivy Operator (GitHub)](https://github.com/aquasecurity/trivy-operator) -- Kubernetes-native scanning
- [Trivy Kubernetes Scanning Guide (OneUpTime, 2026)](https://oneuptime.com/blog/post/2026-02-02-trivy-kubernetes-scanning/view) -- Current usage

**OWASP ZAP:**
- [ZAP API Reference](https://www.zaproxy.org/docs/api/) -- REST API documentation
- [ZAP OpenAPI Automation Support](https://www.zaproxy.org/docs/desktop/addons/openapi-support/automation/) -- Automation framework
- [ZAP 2026 Review (AppSec Santa)](https://appsecsanta.com/zap) -- Version 2.17.0 details
- [ZAP API Security Implementation (Medium)](https://medium.com/@jaishreepatidar/api-penetration-testing-using-zap-automation-framework-practical-implementation-bca6c28e0236) -- Practical implementation

**Checkov:**
- [Checkov YAML Custom Policies](https://www.checkov.io/3.Custom%20Policies/YAML%20Custom%20Policies.html) -- YAML policy authoring
- [Checkov Python Custom Policies](https://github.com/bridgecrewio/checkov/blob/main/docs/3.Custom%20Policies/Python%20Custom%20Policies.md) -- Python policy authoring
- [Checkov GitHub Repository](https://github.com/bridgecrewio/checkov) -- Official repository
- [Bridgecrew Policy Synchronization](https://bridgecrew.io/blog/synchronizing-bridgecrew-custom-policies-with-checkov-using-our-public-apis/) -- API integration

**Dependabot / Renovate:**
- [Renovate GitHub Repository](https://github.com/renovatebot/renovate) -- Official repository
- [Renovate Configuration Options](https://docs.renovatebot.com/configuration-options/) -- Full config reference
- [Renovate Bot Comparison](https://docs.renovatebot.com/bot-comparison/) -- Dependabot vs Renovate
- [Renovate 2026 Review (AppSec Santa)](https://appsecsanta.com/renovate) -- Current capabilities

**CodeQL:**
- [CodeQL CLI SARIF Output](https://docs.github.com/en/code-security/codeql-cli/using-the-advanced-functionality-of-the-codeql-cli/sarif-output) -- SARIF generation
- [CodeQL CLI Overview](https://docs.github.com/en/code-security/codeql-cli/getting-started-with-the-codeql-cli/about-the-codeql-cli) -- CLI capabilities
- [Uploading SARIF to GitHub](https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/uploading-a-sarif-file-to-github) -- Integration workflow

**Checkmarx / Fortify:**
- [Checkmarx One API Documentation](https://docs.checkmarx.com/en/34965-68772-checkmarx-one-api-documentation.html) -- REST API reference
- [Checkmarx SCA REST API](https://docs.checkmarx.com/en/34965-19221-checkmarx-sca--rest--api-documentation.html) -- SCA API
- [Checkmarx CxSAST REST API](https://docs.checkmarx.com/en/34965-278101-using-the-cxsast--rest--api--v8-6-0-and-up-.html) -- SAST API
- [Checkmarx vs Fortify (AppSec Santa)](https://appsecsanta.com/checkmarx-vs-fortify) -- Feature comparison

**Nikto:**
- [Nikto GitHub Repository](https://github.com/sullo/nikto) -- Official repository
- [Nikto 2025 Commands Guide](https://squidhacker.com/2025/04/master-nikto-in-2025-50-essential-commands-every-hacker-needs-with-bonus-web-security-cheat-sheet/) -- Current usage

**SARIF Standard:**
- [SARIF Home (OASIS)](https://sarifweb.azurewebsites.net/) -- Standard homepage
- [SARIF v2.1.0 Specification](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html) -- Full specification
- [SARIF Guide (Sonar)](https://www.sonarsource.com/resources/library/sarif/) -- Comprehensive guide

---

## Recommendations

### Priority Integration Targets (Tier 1 -- Implement First)

1. **Semgrep** -- Highest ROI for secure SDLC integration. YAML rules are LLM-writable, JSON/SARIF output is structured, and an MCP server already exists. Enables bidirectional integration: consume findings AND generate custom rules. CLI adapter + MCP server pattern.

2. **OWASP ZAP** -- Best open-source DAST tool with comprehensive REST API and OpenAPI spec. Automation Framework YAML plans are agent-writable. Python client library available. CLI adapter + REST API adapter pattern.

3. **Trivy** -- Broadest coverage in a single tool (containers, filesystems, IaC, K8s, SBOMs, secrets). Native JSON/SARIF output. No authentication required for CLI. CLI adapter with JSON parsing.

### Secondary Integration Targets (Tier 2 -- Implement When Needed)

4. **SonarQube** -- Platform-level code quality analysis with webhook-driven event notification. REST API for issue querying and quality gate status. REST API adapter + webhook listener pattern.

5. **Checkov** -- IaC-specific scanning with LLM-writable YAML policies. Complements Trivy for deeper IaC analysis. CLI adapter with policy generation.

6. **Snyk** -- Comprehensive SCA with SBOM generation. REST API for platform features. CLI adapter + REST API pattern. Note: commercial features may limit scope.

7. **CodeQL** -- Deep semantic analysis with SARIF output. QL query language is powerful but complex for LLM generation. CLI adapter with SARIF parsing.

### Deferred (Tier 3 -- Configuration-Only or Commercial)

8. **Renovate/Dependabot** -- Configuration generation rather than runtime integration
9. **Checkmarx One** -- Commercial platform; integrate when customer environments require it
10. **Fortify** -- Proprietary format, complex infrastructure; integrate only on demand
11. **Nikto** -- Superseded by ZAP for most DAST use cases

### Recommended Normalization Architecture

```
+------------------+     +-------------------+     +------------------+
|                  |     |  SARIF             |     |                  |
|   Jerry Agent    |---->|  Normalization     |<----|  Semgrep         |
|   (Standalone    |     |  Layer             |<----|  ZAP             |
|    Capable)      |<----|                    |<----|  Trivy           |
|                  |     |  Common Finding    |<----|  CodeQL          |
+------------------+     |  Schema:           |<----|  SonarQube*      |
                         |  - severity        |<----|  Checkov         |
                         |  - location        |<----|  Snyk            |
                         |  - rule_id         |     +------------------+
                         |  - message         |
                         |  - fix_suggestion  |     * = via API, not SARIF
                         |  - evidence        |
                         +-------------------+
```

**Design Principles:**
- SARIF as the primary interchange format wherever supported
- Custom JSON-to-finding normalization for non-SARIF tools
- Common finding schema enables cross-tool correlation and deduplication
- Agent can reason about findings regardless of source tool
- Agent generates YAML rules/policies for tools that support them (Semgrep, Checkov, Nuclei)
- Webhook listeners enable event-driven agent activation (SonarQube, Snyk)
- Agent MUST be fully functional without any tools (R-012 standalone capable)
- Tools provide concrete evidence to support agent analysis and recommendations
