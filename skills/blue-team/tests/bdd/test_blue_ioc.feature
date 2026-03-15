@blue-team @threat-intel @blue-ioc
Feature: IOC Lifecycle Management and YARA Rule Authoring
  As a threat intelligence analyst
  I want blue-ioc to manage indicators of compromise and author YARA rules
  So that intelligence is operationalized into validated detection signatures

  Background:
    Given a valid blue-lead scope document exists for the assessment
    And blue-ioc agent is invoked within Security Zone 1

  # -----------------------------------------------------------------------
  # IOC Ingestion and Validation
  # -----------------------------------------------------------------------

  Scenario: Ingest IOCs from blue-intel STIX bundle
    Given a STIX 2.1 bundle from blue-intel at "work/blue-team/intel/campaign-report.json"
    And the bundle contains indicators with hashes, IP addresses, and domains
    When blue-ioc processes the STIX bundle
    Then each indicator is extracted with its type, value, and metadata
    And indicators are classified by type (file-hash, ipv4-addr, domain-name)
    And all indicators are persisted to "work/blue-team/ioc/"

  Scenario: Ingest IOCs from blue-malware-analyst findings
    Given an IOC list from blue-malware-analyst at "work/blue-team/analysis/sample-001/iocs.md"
    When blue-ioc processes the IOC list
    Then indicators are parsed with their confidence levels
    And provenance is recorded linking to the malware analysis source

  Scenario: Validate STIX bundle trust-boundary prefix on free-text fields
    Given a STIX 2.1 bundle with free-text fields (description, name, labels)
    When blue-ioc validates the bundle
    Then free-text fields are checked for trust-boundary compliance
    And structured IOC value fields (pattern, hashes, ipv4-addr, domain-name) are NOT prefixed
    And validation results are documented

  # -----------------------------------------------------------------------
  # Cross-Skill Trust Boundary (IP-5: Red-to-Blue)
  # -----------------------------------------------------------------------

  Scenario: Apply credential filter to red-team artifacts
    Given an artifact received from /red-team via IP-5 RBEE schema
    When blue-ioc processes the cross-skill handoff
    Then the credential filter pipeline is applied (L1 regex, L2 entropy, L3 structural)
    And the input is classified as "adversary-tainted" until filter completes
    And any detected credentials are quarantined to "work/.credential-quarantine/"
    And the sanitized artifact is processed for IOC extraction

  Scenario: Reject cross-skill artifact on credential filter failure
    Given an artifact from /red-team where the credential filter crashes
    When blue-ioc attempts to process the artifact
    Then the artifact is rejected per fail-closed behavior
    And a quarantine placeholder is logged
    And the user is notified of the filter failure

  Scenario: Document trust boundary transition
    Given successfully filtered red-team artifacts
    When blue-ioc extracts IOCs from the filtered data
    Then the provenance chain documents: source agent, handoff timestamp, filter results
    And indicator classification transitions from "adversary-tainted" to "analysis-verified"
    And the transition is recorded in the output artifact

  # -----------------------------------------------------------------------
  # YARA Rule Authoring
  # -----------------------------------------------------------------------

  Scenario: Author YARA rules from file hash indicators
    Given enriched IOCs containing SHA-256 file hashes
    When blue-ioc generates YARA rules for the hash indicators
    Then each rule includes metadata block (author, date, description, reference, ATT&CK)
    And string definitions use hex byte patterns for hash matching
    And condition logic is complete and balanced
    And rules are syntax-validated with "yr check"

  Scenario: Author YARA rules from string-based indicators
    Given enriched IOCs containing malware string patterns
    When blue-ioc generates YARA rules
    Then string definitions include both ASCII and wide variants where appropriate
    And condition logic uses appropriate thresholds (e.g., "3 of ($s*)")
    And rules are syntax-validated with "yr check"

  Scenario: Validate all authored YARA rules before delivery
    Given newly authored YARA rules
    When blue-ioc runs syntax validation
    Then "yr check" is executed against every rule file
    And rules with syntax errors are flagged and excluded from deliverable
    And the validation report includes per-rule pass/fail status

  Scenario: Reject delivery of unvalidated YARA rules
    Given YARA rules that have not passed "yr check"
    When blue-ioc prepares the handoff to blue-detect
    Then unvalidated rules are excluded from the artifact list
    And the handoff notes which rules failed validation and why

  # -----------------------------------------------------------------------
  # STIX Indicator Creation
  # -----------------------------------------------------------------------

  Scenario: Create STIX 2.1 indicator objects
    Given enriched IOCs ready for STIX representation
    When blue-ioc creates STIX indicators using python-stix2
    Then each indicator has a valid STIX pattern (file hash, IP, domain)
    And valid-from and valid-until dates are set
    And indicator types are properly classified
    And a STIX bundle wrapping all indicators is produced

  # -----------------------------------------------------------------------
  # IOC Lifecycle Management
  # -----------------------------------------------------------------------

  Scenario: Track IOC aging based on last-seen date
    Given an IOC inventory with last-seen dates
    When blue-ioc evaluates IOC freshness
    Then indicators not seen in 90+ days are flagged as "stale"
    And indicators not seen in 180+ days are recommended for retirement
    And the aging assessment is documented

  Scenario: Require user confirmation for IOC retirement
    Given IOCs flagged for retirement
    When blue-ioc recommends retirement
    Then the recommendation is presented to the user per P-020
    And retirement does NOT proceed without explicit user approval
    And the retirement rationale is documented

  # -----------------------------------------------------------------------
  # Output and Persistence
  # -----------------------------------------------------------------------

  Scenario: Produce complete IOC lifecycle report
    Given a completed IOC processing cycle
    When blue-ioc generates the output report
    Then L0 summary includes total indicators, new ingested, rules authored, retired count
    And L1 detail includes per-indicator metadata table and YARA rule files
    And L2 strategic section includes coverage analysis and intelligence gap identification
    And all outputs are persisted to "work/blue-team/ioc/" per P-002

  # -----------------------------------------------------------------------
  # Constitutional Compliance
  # -----------------------------------------------------------------------

  Scenario: Never spawn subagents (P-003)
    When blue-ioc completes its processing
    Then no subagent invocations were made
    And all results are returned to the main context

  Scenario: Never misrepresent indicator confidence (P-022)
    Given indicators with varying source reliability
    When blue-ioc reports indicator confidence
    Then each indicator's confidence reflects its actual source quality
    And source reliability ratings use the Admiralty code
    And no indicator confidence is inflated
