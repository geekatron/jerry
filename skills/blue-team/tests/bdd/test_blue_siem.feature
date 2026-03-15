@blue-team @detection @blue-siem
Feature: SIEM/Log Analysis and Detection Rule Translation
  As a detection engineer
  I want blue-siem to author Sigma rules, convert them to SIEM queries, and analyze EVTX logs
  So that I can build validated detection logic across multiple SIEM platforms

  Background:
    Given a valid blue-lead scope document exists for the assessment
    And blue-siem agent is invoked within Security Zone 1

  # -----------------------------------------------------------------------
  # Sigma Rule Authoring
  # -----------------------------------------------------------------------

  Scenario: Author Sigma detection rule from ATT&CK technique
    Given a detection requirement for ATT&CK technique T1059.001 (PowerShell)
    When blue-siem authors a Sigma rule
    Then the rule includes: title, status, description, references, author, date, tags
    And the logsource specifies category, product, and service
    And the detection section defines search criteria with proper Sigma syntax
    And falsepositives section lists known benign triggers
    And the rule is written to "work/blue-team/siem/"

  Scenario: Validate Sigma rule syntax
    Given an authored Sigma rule file
    When blue-siem executes "sigma check" against the rule
    Then the validation result is "PASS" for valid rules
    And validation errors are reported with specific field-level feedback for invalid rules

  Scenario: Author multiple related Sigma rules
    Given a detection requirement spanning multiple ATT&CK techniques
    When blue-siem authors a Sigma rule set
    Then each technique gets an individual rule
    And rules share consistent metadata conventions
    And cross-references between related rules are documented

  # -----------------------------------------------------------------------
  # Sigma Backend Conversion
  # -----------------------------------------------------------------------

  Scenario: Convert Sigma rule to Splunk SPL
    Given a validated Sigma rule
    When blue-siem converts using "sigma convert -t splunk"
    Then the output is valid Splunk SPL query syntax
    And the required pySigma backend plugin is documented
    And pipeline mapping requirements are noted

  Scenario: Convert Sigma rule to Elastic KQL
    Given a validated Sigma rule
    When blue-siem converts using "sigma convert -t elasticsearch"
    Then the output is valid Elasticsearch/Kibana query
    And field mapping differences are documented

  Scenario: Document SIEM-specific conversion requirements
    Given Sigma rules converted to multiple backends
    When blue-siem generates conversion documentation
    Then each backend's plugin installation requirements are listed
    And pipeline file requirements for field mapping are documented
    And known limitations per backend are disclosed

  # -----------------------------------------------------------------------
  # EVTX Analysis with Hayabusa
  # -----------------------------------------------------------------------

  Scenario: Generate EVTX timeline with Hayabusa CSV output
    Given EVTX files at "work/blue-team/siem/evtx/"
    When blue-siem executes "hayabusa csv-timeline"
    Then a CSV timeline is produced at "work/blue-team/siem/"
    And the timeline includes timestamps, event IDs, rule matches, and severity levels
    And results are sorted chronologically

  Scenario: Generate EVTX timeline with Hayabusa JSONL output
    Given EVTX files at "work/blue-team/siem/evtx/"
    When blue-siem executes "hayabusa json-timeline" with "-L" flag
    Then a JSONL file is produced with one event per line
    And each event includes structured fields for downstream processing

  Scenario: Filter Hayabusa results by severity
    Given EVTX files with mixed severity detections
    When blue-siem executes Hayabusa with "--min-level high"
    Then only HIGH and CRITICAL severity events appear in the timeline
    And lower severity events are excluded

  # -----------------------------------------------------------------------
  # EVTX Hunting with Chainsaw
  # -----------------------------------------------------------------------

  Scenario: Hunt EVTX logs with Sigma rules via Chainsaw
    Given EVTX files and Sigma rules at "work/blue-team/siem/"
    When blue-siem executes "chainsaw hunt" with Sigma rules and mapping file
    Then hunting results are produced in JSON format
    And per-rule match results are organized by rule name
    And timestamps and event details are included

  Scenario: Search EVTX logs for specific strings via Chainsaw
    Given EVTX files and a search string
    When blue-siem executes "chainsaw search" with "--json"
    Then matching events are returned in JSON format
    And event context (surrounding events) is available

  # -----------------------------------------------------------------------
  # Cross-Source Correlation (Integrative Mode)
  # -----------------------------------------------------------------------

  Scenario: Correlate Hayabusa and Chainsaw findings
    Given Hayabusa timeline results and Chainsaw hunting results
    When blue-siem performs cross-source correlation
    Then a unified forensic timeline is produced
    And overlapping detections are deduplicated
    And unique findings from each tool are preserved
    And the correlation confidence is documented

  Scenario: Correlate multiple log source findings
    Given detections from Sigma rules across different SIEM backends
    When blue-siem performs cross-source correlation
    Then common adversary behaviors are identified across log sources
    And detection coverage per log source is assessed
    And gaps in individual log source coverage are identified

  # -----------------------------------------------------------------------
  # Wazuh Methodology Guidance
  # -----------------------------------------------------------------------

  Scenario: Provide Wazuh rule authoring guidance
    Given a detection requirement for Wazuh SIEM
    When blue-siem provides Wazuh methodology guidance
    Then XML rule syntax examples are provided
    And decoder configuration guidance is included
    And the output explicitly states "Wazuh is Tier C -- methodology-only"
    And deployment responsibility is assigned to the user

  # -----------------------------------------------------------------------
  # Output and Persistence
  # -----------------------------------------------------------------------

  Scenario: Produce SIEM analysis report
    Given completed Sigma rule authoring and EVTX analysis
    When blue-siem generates the output report
    Then L0 summary includes rules authored, backends targeted, EVTX findings count
    And L1 detail includes Sigma rules, converted queries, timeline data, hunting results
    And L2 strategic section includes detection coverage analysis and architecture recommendations
    And all outputs are persisted to "work/blue-team/siem/" per P-002

  # -----------------------------------------------------------------------
  # Zone 1 Enforcement
  # -----------------------------------------------------------------------

  Scenario: Refuse to access live SIEM infrastructure
    When the user requests querying a production SIEM instance
    Then blue-siem declines the request
    And the output states "Zone 1 analysis only -- no production SIEM access"
    And alternative instructions for local analysis are provided

  # -----------------------------------------------------------------------
  # Constitutional Compliance
  # -----------------------------------------------------------------------

  Scenario: Never spawn subagents (P-003)
    When blue-siem completes its analysis
    Then no subagent invocations were made
    And all results are returned to the main context

  Scenario: Disclose Wazuh Tier C limitations (P-022)
    When blue-siem provides Wazuh guidance
    Then the output explicitly states Wazuh is "Tier C -- methodology guidance only"
    And no claim of direct Wazuh execution capability is made
