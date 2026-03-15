@blue-team @detection @blue-monitor
Feature: Network and Runtime Monitoring Methodology Guidance
  As a security engineer
  I want blue-monitor to author detection rules for network and runtime monitoring tools
  So that I can deploy validated monitoring rules to my infrastructure

  Background:
    Given a valid blue-lead scope document exists for the assessment
    And blue-monitor agent is invoked within Security Zone 1

  # -----------------------------------------------------------------------
  # Suricata Rule Authoring
  # -----------------------------------------------------------------------

  Scenario: Author Suricata IDS rules for network detection
    Given a detection requirement for a specific adversary TTP
    And the TTP involves network traffic patterns (e.g., C2 beaconing)
    When blue-monitor authors Suricata rules
    Then the rules follow Suricata rule syntax (action, protocol, addresses, ports, options)
    And each rule includes: msg, content, sid, rev, classtype, metadata
    And ATT&CK technique references are included in metadata
    And rules are written to "work/blue-team/monitoring/"

  Scenario: Produce Suricata deployment instructions
    Given authored Suricata rules
    When blue-monitor generates deployment documentation
    Then the documentation includes Suricata configuration requirements
    And rule file placement instructions are provided
    And expected alert behavior is described
    And the documentation states "Tier C -- user-managed deployment required"

  # -----------------------------------------------------------------------
  # Zeek Script Authoring
  # -----------------------------------------------------------------------

  Scenario: Author Zeek scripts for protocol analysis
    Given a detection requirement for protocol-level anomalies
    When blue-monitor authors Zeek analysis scripts
    Then the scripts follow Zeek scripting syntax
    And protocol analyzers and event handlers are properly structured
    And logging output format is defined
    And scripts are written to "work/blue-team/monitoring/"

  # -----------------------------------------------------------------------
  # Falco Rule Authoring
  # -----------------------------------------------------------------------

  Scenario: Author Falco rules for container runtime detection
    Given a detection requirement for container-level threats
    When blue-monitor authors Falco rules
    Then the rules follow Falco YAML syntax (rule, desc, condition, output, priority, tags)
    And syscall conditions are properly formed
    And output format includes relevant field macros
    And rules are written to "work/blue-team/monitoring/"

  Scenario: Author Falco rules with Kubernetes audit events
    Given a detection requirement for Kubernetes API abuse
    When blue-monitor authors Falco rules targeting K8s audit logs
    Then the rules reference ka.* fields for Kubernetes audit events
    And pod security violations are detected
    And rules include appropriate priority levels

  # -----------------------------------------------------------------------
  # Tetragon TracingPolicy Authoring
  # -----------------------------------------------------------------------

  Scenario: Author Tetragon TracingPolicy for kernel observability
    Given a detection requirement for process-level threats
    When blue-monitor authors a Tetragon TracingPolicy
    Then the policy follows the cilium.io/v1alpha1 TracingPolicy schema
    And kprobes or tracepoints are correctly specified
    And argument types and indices are properly defined
    And the policy is written to "work/blue-team/monitoring/"

  # -----------------------------------------------------------------------
  # Coverage Mapping
  # -----------------------------------------------------------------------

  Scenario: Map monitoring rules to ATT&CK techniques
    Given authored monitoring rules across multiple tools
    When blue-monitor performs coverage mapping
    Then each rule is mapped to its relevant ATT&CK technique
    And a coverage matrix shows techniques covered per tool
    And coverage gaps are identified and documented

  Scenario: Produce monitoring coverage report
    Given completed monitoring rule authoring
    When blue-monitor generates the output report
    Then L0 summary includes tools covered, rule counts, ATT&CK coverage
    And L1 detail includes complete rule files with deployment instructions
    And L2 strategic section includes architecture recommendations and gap analysis
    And all outputs are persisted to "work/blue-team/monitoring/" per P-002

  # -----------------------------------------------------------------------
  # Tier C Limitations Disclosure
  # -----------------------------------------------------------------------

  Scenario: Disclose Tier C methodology-only limitations
    Given monitoring rules authored for any Tier C tool
    When blue-monitor produces output
    Then the output explicitly states all four tools are "Tier C -- methodology-only"
    And the output notes "runtime validation requires user-managed infrastructure"
    And deployment responsibility is clearly assigned to the user

  # -----------------------------------------------------------------------
  # Input Validation
  # -----------------------------------------------------------------------

  Scenario: Validate monitoring output file paths
    Given monitoring output provided by the user for analysis
    When blue-monitor validates the input paths
    Then only paths within the "work/" directory are accepted
    And paths outside "work/" are rejected with "input validation failed"

  # -----------------------------------------------------------------------
  # Zone 1 Enforcement
  # -----------------------------------------------------------------------

  Scenario: Refuse to deploy monitoring rules to infrastructure
    Given authored monitoring rules ready for deployment
    When the user requests direct deployment to Suricata/Zeek/Falco/Tetragon
    Then blue-monitor declines the deployment request
    And the output states "Zone 1 analysis only -- deployment is the user's responsibility"
    And the output provides file paths for manual deployment

  # -----------------------------------------------------------------------
  # Constitutional Compliance
  # -----------------------------------------------------------------------

  Scenario: Never spawn subagents (P-003)
    When blue-monitor completes its analysis
    Then no subagent invocations were made
    And all results are returned to the main context

  Scenario: Never override user decisions (P-020)
    Given the user specifies monitoring scope and tool preferences
    When blue-monitor authors rules
    Then only the user-specified scope and tools are addressed
    And blue-monitor does not expand scope without user approval
