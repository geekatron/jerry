@blue-team @threat-intel @blue-d3fend
Feature: D3FEND Countermeasure Mapping and Coverage Analysis
  As a security analyst performing defensive coverage assessment
  I want blue-d3fend to map ATT&CK techniques to D3FEND countermeasures
  So that I can identify coverage gaps and produce defensive architecture recommendations

  Background:
    Given an active assessment scope document from blue-lead
    And the agent operates in Zone 1 (Analysis) mode

  # --- ATT&CK-to-D3FEND Mapping ---

  Scenario: Map ATT&CK techniques to D3FEND countermeasures
    Given a list of in-scope ATT&CK technique IDs
    When D3FEND mapping is requested
    Then blue-d3fend queries the D3FEND knowledge base for each technique
    And applicable D3FEND countermeasures are identified per technique
    And each mapping includes D3FEND tactic category (Harden, Detect, Isolate, Deceive, Evict)
    And results are persisted to "work/blue-team/d3fend/{mapping-slug}.md"

  Scenario: Map ATT&CK sub-techniques to D3FEND
    Given ATT&CK techniques with sub-techniques (e.g., T1059.001)
    When D3FEND mapping is applied
    Then sub-techniques are mapped independently
    And parent technique coverage is assessed considering sub-technique coverage

  Scenario: Handle ATT&CK techniques without D3FEND mappings
    Given ATT&CK techniques that have no D3FEND countermeasure mappings
    When the mapping is assessed
    Then the techniques are classified as coverage gaps
    And the gap reason documents the D3FEND ontology limitation
    And recommendations are provided for methodology-only mitigation

  # --- Coverage Confidence Tiers ---

  Scenario: Classify coverage as Verified (Tier A/B)
    Given a D3FEND countermeasure mapped to a blue-team agent with Tier A/B tools
    When coverage confidence is assessed
    Then the countermeasure is classified as "Verified" confidence
    And the verifying tool and agent are documented
    And the countermeasure counts toward operational coverage metrics

  Scenario: Classify coverage as Partial (Tier C)
    Given a D3FEND countermeasure mapped to a blue-team agent with Tier C tools only
    When coverage confidence is assessed
    Then the countermeasure is classified as "Partial" confidence
    And the methodology-only limitation is documented
    And the countermeasure counts toward detection_rate but not verified_detection_rate

  Scenario: Classify coverage as Unverified
    Given a D3FEND countermeasure with no tool support in blue-team
    When coverage confidence is assessed
    Then the countermeasure is classified as "Unverified" confidence
    And it is NOT counted toward any operational coverage metric
    And the gap is documented with a recommendation

  Scenario: Exclude Unverified rows from operational metrics
    Given a coverage matrix with Verified, Partial, and Unverified entries
    When coverage metrics are calculated
    Then verified_detection_rate counts only Verified entries
    And full_detection_rate counts Verified and entries with full coverage
    And detection_rate counts Verified and Partial entries
    And Unverified entries are explicitly excluded from all rate calculations

  # --- Coverage Gap Analysis ---

  Scenario: Identify NO_DETECTION gaps
    Given ATT&CK techniques with no implemented countermeasures
    When gap analysis is performed
    Then each technique is classified as NO_DETECTION
    And gap impact is scored based on number of affected techniques
    And gaps are priority-ranked for closure

  Scenario: Identify PARTIAL_DETECTION gaps
    Given ATT&CK techniques with some but incomplete countermeasure coverage
    When gap analysis is performed
    Then each technique is classified as PARTIAL_DETECTION
    And missing countermeasure types are identified
    And recommended rule types for gap closure are specified

  Scenario: Produce priority-ranked gap list
    Given identified coverage gaps with impact scores
    When the gap list is prioritized
    Then gaps are ranked by descending impact score
    And each gap includes feasibility assessment (high/medium/low)
    And blocking technique counts are documented
    And prerequisite gaps are identified

  # --- CFE/DGE Envelope Production ---

  Scenario: Produce Coverage Feedback Envelope (CFE)
    Given completed coverage analysis as part of a purple team exercise
    When CFE production is requested
    Then blue-d3fend produces a CFE with technique_coverage_matrix
    And each technique includes detection_status enum and confidence score
    And aggregate rates (detection_rate, full_detection_rate, verified_detection_rate) are calculated
    And uncovered_technique_list is populated with gaps
    And trust_boundary is analysis-verified with blue-lead as verified_by

  Scenario: Produce D3FEND Gap Envelope (DGE)
    Given completed D3FEND coverage analysis
    When DGE production is requested
    Then blue-d3fend produces a DGE with d3fend_coverage_gaps array
    And priority_ranked_gap_list includes rank, impact_score, and feasibility
    And recommendation_per_gap includes recommendation_type and estimated_effort
    And scoping_relevance field is populated for red-lead consumption
    And D3FEND KB version is documented

  # --- Cross-Skill Integration (IP-7) ---

  Scenario: Prepare IP-7 handoff for eng-architect
    Given completed D3FEND analysis with architectural recommendations
    When IP-7 cross-skill handoff is in scope
    Then blue-d3fend produces a handoff document for eng-architect
    And includes "Architectural Recommendations" section mapping D3FEND tactics to layers
    And includes "STRIDE Integration" section mapping ATT&CK to STRIDE categories
    And trust_boundary trust_level is "analysis-verified"
    And taint_propagation is "neutralized"
    And data_classification tlp is "TLP:GREEN"

  # --- Detection Integration ---

  Scenario: Integrate detection results from blue-detect
    Given YARA scan results from blue-detect
    When detection results are incorporated into coverage analysis
    Then techniques covered by validated YARA rules are marked Verified
    And detection coverage metrics are updated
    And the detection evidence path is recorded

  Scenario: Integrate Sigma results from blue-siem
    Given Sigma rule validation results from blue-siem
    When detection results are incorporated
    Then techniques covered by validated Sigma rules are marked appropriately
    And behavioral detection coverage is assessed

  Scenario: Integrate monitoring results from blue-monitor
    Given detection artifacts from blue-monitor (Suricata/Falco rules)
    When monitoring results are incorporated
    Then network and runtime detection coverage is assessed
    And Tier C tools are classified as Partial confidence

  # --- D3FEND Tactic Distribution ---

  Scenario: Analyze D3FEND tactic distribution
    Given a complete ATT&CK-to-D3FEND coverage matrix
    When tactic distribution is analyzed
    Then the count of countermeasures per D3FEND tactic is calculated
    And Harden, Detect, Isolate, Deceive, and Evict distribution is reported
    And tactic imbalances are identified (e.g., heavy Detect, weak Isolate)

  # --- Output Structure ---

  Scenario: Produce L0/L1/L2 D3FEND analysis report
    Given completed D3FEND mapping and coverage analysis
    When the analysis report is generated
    Then L0 contains coverage rates and top gaps in plain language
    And L1 contains full coverage matrix, gap list, CFE/DGE, and STRIDE mappings
    And L2 contains defensive posture maturity and gap closure roadmap
    And the report is persisted to "work/blue-team/d3fend/{mapping-slug}.md"

  # --- Zone 1 Enforcement ---

  Scenario: Reject defensive deployment request
    Given a request to deploy D3FEND countermeasures
    When the deployment request is evaluated
    Then blue-d3fend refuses per Zone 1 constraints
    And documents the recommended countermeasures as guidance only
    And recommends human-led deployment of defensive controls

  # --- Credential Filter ---

  Scenario: Apply credential filter on cross-skill input
    Given artifacts received from a cross-skill handoff
    When the artifacts are processed
    Then the Rainbow credential filter pipeline is applied
    And any credential-bearing content triggers fail-closed quarantine

  # --- D3FEND KB Version Tracking ---

  Scenario: Document D3FEND KB version in all outputs
    Given a D3FEND analysis is produced
    When the report is finalized
    Then the D3FEND KB version used is documented (e.g., v0.15.0-BETA-2)
    And a note indicates that mappings may change with KB updates
    And the version is included in any CFE/DGE envelopes
