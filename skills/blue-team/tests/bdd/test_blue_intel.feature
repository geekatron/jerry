@blue-team @threat-intel @blue-intel
Feature: Threat Intelligence Collection and Dissemination
  As a security analyst performing threat intelligence operations
  I want blue-intel to collect, process, and disseminate threat intelligence
  So that I can produce actionable intelligence products for defensive operations

  Background:
    Given an active assessment scope document from blue-lead
    And the threat intelligence domain is enabled in the scope
    And the agent operates in Zone 1 (Analysis) mode

  # --- Intelligence Collection (MISP) ---

  Scenario: Search MISP events by tags
    Given a configured MISP instance with API access
    When I request threat intelligence for a specific threat group
    Then blue-intel queries MISP using PyMISP search API with relevant tags
    And retrieved events are parsed for indicator data
    And source evaluation (Admiralty/NATO) is applied to MISP data

  Scenario: Search MISP attributes by type
    Given a MISP instance with attribute data
    When I request IP-based indicators
    Then blue-intel queries MISP attributes by type (ip-dst, ip-src)
    And retrieved attributes include confidence and context metadata
    And each attribute source is evaluated for reliability

  Scenario: Handle MISP unavailability gracefully
    Given MISP instance is unreachable or credentials are missing
    When MISP collection is attempted
    Then blue-intel reports the collection limitation per P-022
    And continues with available sources (TAXII, OSINT)
    And documents the intelligence gap in the report

  # --- Intelligence Collection (TAXII) ---

  Scenario: Retrieve STIX objects from TAXII feed
    Given a configured TAXII server with accessible collections
    When I request intelligence from a TAXII feed
    Then blue-intel connects using taxii2-client
    And STIX objects are retrieved from specified collections
    And source evaluation is applied to TAXII-sourced data

  Scenario: Retrieve MITRE ATT&CK data from TAXII
    Given the MITRE ATT&CK TAXII server is accessible
    When I request ATT&CK technique data
    Then blue-intel retrieves attack-pattern objects from the ATT&CK collection
    And technique IDs and tactic mappings are extracted
    And the data source is rated Reliability A (official MITRE source)

  Scenario: Handle TAXII server unavailability
    Given a TAXII server is unreachable
    When TAXII collection is attempted
    Then blue-intel reports the connection failure per P-022
    And falls back to cached ATT&CK data or OSINT sources
    And documents the intelligence gap

  # --- Intelligence Collection (OSINT) ---

  Scenario: Collect OSINT via web search
    Given intelligence requirements that cannot be satisfied by MISP/TAXII
    When OSINT collection is initiated
    Then blue-intel uses WebSearch for current threat reports and advisories
    And uses WebFetch for detailed report retrieval
    And applies source evaluation to each OSINT source
    And all external sources are cited with URLs

  # --- STIX 2.1 Object Creation ---

  Scenario: Create STIX 2.1 threat actor profile
    Given collected intelligence about a threat group
    When a threat actor profile is produced
    Then blue-intel creates a STIX ThreatActor SDO with name, description, and aliases
    And the object includes MITRE ATT&CK group references
    And the STIX object is valid STIX 2.1 (spec_version 2.1)

  Scenario: Create STIX 2.1 indicator objects
    Given collected IOC data (IPs, domains, file hashes)
    When indicators are structured
    Then blue-intel creates STIX Indicator SDOs with STIX patterns
    And each indicator includes valid_from timestamp
    And pattern_type is set to "stix"

  Scenario: Create STIX 2.1 campaign with temporal bounds
    Given intelligence about a specific adversary campaign
    When a campaign report is produced
    Then blue-intel creates a STIX Campaign SDO with first_seen and last_seen
    And Relationship SROs link the campaign to threat actors and malware
    And temporal analysis is documented

  Scenario: Produce STIX 2.1 bundle
    Given multiple STIX objects created from intelligence collection
    When the intelligence product is finalized
    Then blue-intel creates a STIX Bundle containing all objects
    And the bundle is serialized to JSON
    And the bundle file is persisted alongside the intelligence report

  # --- Source Evaluation ---

  Scenario: Apply Admiralty/NATO source evaluation
    Given intelligence from multiple sources with varying reliability
    When source evaluation is applied
    Then each source receives a reliability rating (A-F)
    And each claim receives a credibility rating (1-6)
    And the evaluation is documented per intelligence claim in the report

  Scenario: Evaluate OSINT source reliability
    Given intelligence from a blog post and a government advisory
    When source evaluation is applied
    Then the government advisory receives higher reliability (B or above)
    And the blog post receives appropriate reliability (C or D)
    And both evaluations include justification

  # --- TLP Marking ---

  Scenario: Apply TLP markings to intelligence products
    Given an intelligence product ready for dissemination
    When TLP marking is applied
    Then each section receives appropriate TLP marking per FIRST TLP v2.0
    And TLP:CLEAR is used for unrestricted sharing
    And TLP:AMBER is used for organization-limited sharing
    And TLP markings are visible in report headers

  # --- Cross-Skill Integration (IP-7) ---

  Scenario: Prepare IP-7 handoff for eng-architect
    Given completed threat intelligence analysis with ATT&CK mappings
    When IP-7 cross-skill handoff is in scope
    Then blue-intel produces a DGE schema handoff document
    And includes "Recommended STRIDE Inputs" section
    And ATT&CK techniques are mapped to STRIDE threat categories
    And trust_boundary trust_level is "analysis-verified"
    And taint_propagation is "neutralized"

  Scenario: Feed blue-ioc with indicator data
    Given collected indicators from intelligence sources
    When indicator data is prepared for blue-ioc
    Then indicators are structured with type, value, and confidence
    And STIX indicator objects are included as artifacts
    And the handoff recommends rule types per indicator type

  Scenario: Feed blue-d3fend with TTP data
    Given adversary TTP analysis with ATT&CK technique mappings
    When TTP data is prepared for blue-d3fend
    Then ATT&CK technique IDs and tactic associations are included
    And adversary capability assessment is provided
    And the handoff supports D3FEND countermeasure mapping

  # --- Credential Filter ---

  Scenario: Apply credential filter on red-team tainted input
    Given artifacts received from a red-team cross-skill handoff (IP-5)
    When the adversary-tainted artifacts are processed
    Then the Rainbow credential filter pipeline is applied
    And all three layers (L1 regex, L2 entropy, L3 structural) are executed
    And any credential material triggers fail-closed quarantine
    And intelligence is extracted only from sanitized content

  # --- Output Structure ---

  Scenario: Produce L0/L1/L2 intelligence report
    Given completed intelligence collection and analysis
    When the intelligence report is generated
    Then L0 contains threat landscape overview with TLP markings
    And L1 contains STIX bundles, ATT&CK mappings, and source evaluations
    And L2 contains strategic threat assessment and intelligence gaps
    And the report is persisted to "work/blue-team/intel/{product-slug}.md"

  # --- Zone 1 Enforcement ---

  Scenario: Reject active reconnaissance request
    Given a request to interact with adversary infrastructure
    When the request is evaluated
    Then blue-intel refuses per Zone 1 constraints
    And documents the intelligence gap that active recon would fill
    And recommends escalating to /red-team if offensive collection is authorized

  # --- Scope Validation ---

  Scenario: Validate scope includes threat intelligence domain
    Given an assessment scope without threat intelligence coverage
    When threat intelligence collection is requested
    Then blue-intel reports the scope mismatch
    And recommends updating scope via blue-lead
