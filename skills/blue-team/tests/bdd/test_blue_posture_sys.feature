@blue-team @compliance @blue-posture-sys
Feature: System-Level Security Posture and Artifact Verification
  As a security analyst performing system compliance auditing
  I want blue-posture-sys to scan systems against SCAP profiles and verify container artifacts
  So that I can assess system hardening and supply chain integrity

  Background:
    Given an active assessment scope document from blue-lead
    And system-level or container targets are specified in the scope
    And the agent operates in Zone 1 (Analysis) mode

  # --- OpenSCAP XCCDF Evaluation ---

  Scenario: Evaluate system against DISA STIG profile
    Given SCAP content with DISA STIG profiles is available
    When I request an OpenSCAP DISA STIG evaluation
    Then blue-posture-sys executes "oscap xccdf eval --results results.xml --report report.html --profile <stig-profile-id> <content.xml>"
    And XCCDF results XML is produced
    And HTML report is generated
    And per-rule pass/fail/error/notapplicable status is parsed

  Scenario: Evaluate system against CIS system benchmark
    Given SCAP content with CIS system benchmark profiles
    When I request an OpenSCAP CIS evaluation
    Then the appropriate CIS profile is selected based on target OS
    And oscap xccdf eval is executed with the CIS profile
    And findings are mapped to CIS system benchmark controls

  Scenario: Produce ARF output for compliance tracking
    Given an OpenSCAP evaluation is requested
    When ARF output is specified
    Then blue-posture-sys executes with "--results-arf <file>" flag
    And Asset Reporting Format output is produced
    And the ARF file is suitable for compliance tracking systems

  Scenario: Guide profile selection for target system
    Given multiple SCAP profiles are available for the target OS
    When the user requests help selecting a profile
    Then blue-posture-sys lists available profiles using "oscap info <content.xml>"
    And recommends profiles based on compliance requirements
    And explains the scope differences between profiles

  Scenario: Reject remediation request
    Given OpenSCAP findings with available remediations
    When a request includes --remediate flag usage
    Then blue-posture-sys refuses the --remediate flag per Zone 1 constraints
    And documents the remediation steps as guidance only
    And informs the user that system changes require manual execution

  # --- Cosign Verification (Zone 1 Only) ---

  Scenario: Verify container image signature
    Given a container image with a Cosign signature
    When I request Cosign signature verification
    Then blue-posture-sys executes "cosign verify <image> --certificate-identity <id> --certificate-oidc-issuer <issuer>"
    And the verification result (pass/fail) is documented
    And certificate chain details are included in findings

  Scenario: Verify SBOM attestation on container image
    Given a container image with SBOM attestation
    When I request SBOM attestation verification
    Then blue-posture-sys executes "cosign verify-attestation <image> --type <predicate-type>"
    And the attestation verification result is documented
    And SBOM content type and validity are reported

  Scenario: Display supply chain artifact tree
    Given a container image in an OCI registry
    When I request the artifact tree
    Then blue-posture-sys executes "cosign tree <image>"
    And the supply chain artifact tree is displayed
    And signatures, attestations, and SBOMs are enumerated

  Scenario: Reject Cosign sign request
    Given a request to sign a container image
    When the sign operation is evaluated
    Then blue-posture-sys refuses the operation per Zone 1 constraints
    And cites that Cosign sign is Zone 3 (creates cryptographic material)
    And recommends the user perform signing outside the assessment

  Scenario: Reject Cosign attest request
    Given a request to create an attestation
    When the attest operation is evaluated
    Then blue-posture-sys refuses the operation per Zone 1 constraints
    And cites that Cosign attest is Zone 3 (creates attestation artifacts)

  Scenario: Reject Cosign attach request
    Given a request to attach artifacts to an image
    When the attach operation is evaluated
    Then blue-posture-sys refuses the operation per Zone 1 constraints
    And cites that Cosign attach is Zone 3 (modifies OCI artifacts)

  # --- Finding Consolidation ---

  Scenario: Consolidate OpenSCAP and Cosign findings
    Given OpenSCAP evaluation results and Cosign verification results
    When findings are consolidated into a unified report
    Then system compliance findings and supply chain verification are combined
    And each finding category is clearly separated
    And a unified compliance posture summary is produced

  Scenario: Map OpenSCAP findings to compliance frameworks
    Given XCCDF evaluation results with per-rule status
    When framework mapping is applied
    Then findings include DISA STIG rule IDs
    And findings include CIS system benchmark control IDs where applicable
    And compliance percentage per framework is calculated

  # --- Output Structure ---

  Scenario: Produce L0/L1/L2 system posture report
    Given completed system posture scans and verifications
    When the posture report is generated
    Then L0 contains SCAP pass/fail totals and container verification summary
    And L1 contains per-rule findings with SCAP IDs and Cosign verification detail
    And L2 contains system hardening maturity assessment and supply chain posture
    And the report is persisted to "work/compliance/{assessment-id}/system/"

  # --- Credential Filter ---

  Scenario: Apply credential filter on cross-skill input
    Given artifacts received from a cross-skill handoff
    When the artifacts are processed
    Then the Rainbow credential filter pipeline is applied
    And any credential-bearing content triggers fail-closed quarantine

  # --- Scope Validation ---

  Scenario: Validate scope includes system-level targets
    Given an assessment scope without system-level targets
    When a system posture scan is requested
    Then blue-posture-sys reports the scope mismatch
    And recommends updating scope via blue-lead
