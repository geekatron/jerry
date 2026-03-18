@tool-exec @explicit-family @UC-TOOLEXEC-002
Feature: Execute tool with explicit family (UC-TOOLEXEC-002)
  As a security engineer
  I want to run "jerry tool exec --family <name> <tool> [args]" to target a specific family
  So that I bypass auto-detection and use the exact family I intend

  Background:
    Given the tool families registry "tool_families.yaml" is loaded
    And the "rainbow" family is registered and enabled
    And the credential filter service is active

  # ---------------------------------------------------------------------------
  # Basic Flow: Explicit family, happy path
  # ---------------------------------------------------------------------------

  @exit-0
  Scenario: Execute a tool with explicit rainbow family selection
    Given the tool "syft" is registered in the "rainbow" family at Zone 1
    And the execution mode resolves to "local"
    When the user runs "jerry tool exec --family rainbow syft --version"
    Then the system looks up "rainbow" family directly
    And no other families are queried
    And the tool "syft" is resolved within the "rainbow" family
    And the tool executes via local subprocess
    And the credential filter is applied to the output
    And the exit code is 0

  @exit-0 @container-mode
  Scenario: Execute an explicit family tool in container mode
    Given the tool "subfinder" is registered in the "rainbow" family at Zone 2
    And the engagement "pentest-2026-001" is initialized
    And the execution mode resolves to "container"
    And the container service "recon-pipeline" is running
    When the user runs "jerry tool exec --family rainbow --mode container subfinder -d example.com"
    Then the system looks up "rainbow" family directly
    And the tool executes via "docker compose exec -T recon-pipeline subfinder -d example.com"
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # Extension 3a: Family not found (exit 7)
  # ---------------------------------------------------------------------------

  @exit-7 @error
  Scenario: Explicit family name not in registry
    Given no family named "nonexistent" is registered
    When the user runs "jerry tool exec --family nonexistent nuclei --version"
    Then the error message contains "Family 'nonexistent' not found"
    And the error message lists available families
    And the exit code is 7

  @exit-7 @error
  Scenario: Explicit family name is registered but disabled
    Given the family "blue-team" is registered but disabled
    When the user runs "jerry tool exec --family blue-team yr --version"
    Then the error message contains "Family 'blue-team' not found"
    And the exit code is 7

  # ---------------------------------------------------------------------------
  # Extension 3b: Family config error (exit 8)
  # ---------------------------------------------------------------------------

  @exit-8 @error
  Scenario: Family exists but config file is missing
    Given the "rainbow" family is registered
    And the "rainbow" family config file path is invalid or missing
    When the user runs "jerry tool exec --family rainbow syft --version"
    Then the error message contains "configuration error"
    And the exit code is 8

  @exit-8 @error
  Scenario: Family exists but config file is malformed YAML
    Given the "rainbow" family is registered
    And the "rainbow" family config file contains invalid YAML
    When the user runs "jerry tool exec --family rainbow syft --version"
    Then the error message contains "configuration error"
    And the exit code is 8

  # ---------------------------------------------------------------------------
  # Extension 4a: Tool not recognized by named family (exit 1)
  # ---------------------------------------------------------------------------

  @exit-1 @error
  Scenario: Tool not recognized by the explicitly named family
    Given the "rainbow" family does not recognize the tool "unknowntool"
    When the user runs "jerry tool exec --family rainbow unknowntool --help"
    Then the error message contains "Tool 'unknowntool' not recognized by family 'rainbow'"
    And the exit code is 1

  @exit-1 @error
  Scenario: Tool belongs to a different family than the one specified
    Given the tool "gemini" would be recognized by the "ai-cli" family
    And the "rainbow" family does not recognize "gemini"
    When the user runs "jerry tool exec --family rainbow gemini --help"
    Then the error message contains "not recognized by family 'rainbow'"
    And the exit code is 1

  # ---------------------------------------------------------------------------
  # Extension 6a: Engagement not initialized (exit 5)
  # ---------------------------------------------------------------------------

  @BC-08 @exit-5 @error
  Scenario: Explicit family, Zone 2 tool, no engagement
    Given the tool "nuclei" is registered in the "rainbow" family at Zone 2
    And no engagement is initialized
    When the user runs "jerry tool exec --family rainbow nuclei -u target.com"
    Then the error message contains "Engagement not initialized"
    And the exit code is 5

  # ---------------------------------------------------------------------------
  # Extension 6b: Strict mode violation (exit 6)
  # ---------------------------------------------------------------------------

  @BC-03 @exit-6 @strict-mode @error
  Scenario: Explicit family, strict mode, no explicit mode for Zone 2
    Given the tool "nuclei" is registered in the "rainbow" family at Zone 2
    And strict mode is active
    And no execution mode is specified via CLI flag or environment variable
    And the engagement "pentest-2026-001" is initialized
    When the user runs "jerry tool exec --family rainbow nuclei -u target.com"
    Then the error message contains "Strict mode requires explicit mode selection"
    And the exit code is 6

  # ---------------------------------------------------------------------------
  # Extension 7a: Container not running (exit 3)
  # ---------------------------------------------------------------------------

  @BC-06 @exit-3 @error
  Scenario: Explicit family, container not running, auto-start fails
    Given the tool "subfinder" is registered in the "rainbow" family at Zone 2
    And the execution mode resolves to "container"
    And the container service "recon-pipeline" is not running
    And docker compose auto-start fails for "recon-pipeline"
    And the engagement "pentest-2026-001" is initialized
    When the user runs "jerry tool exec --family rainbow subfinder -d example.com"
    Then the exit code is 3

  # ---------------------------------------------------------------------------
  # Extension 7b: Tool error (exit 2)
  # ---------------------------------------------------------------------------

  @exit-2 @error
  Scenario: Explicit family, tool returns non-zero
    Given the tool "grype" is registered in the "rainbow" family at Zone 1
    And the execution mode resolves to "local"
    And the tool "grype" will fail with a non-zero exit code
    When the user runs "jerry tool exec --family rainbow grype db check"
    Then the exit code is 2

  # ---------------------------------------------------------------------------
  # Extension 8a: Credential detected (exit 4)
  # ---------------------------------------------------------------------------

  @BC-07 @exit-4 @credential-filter
  Scenario: Explicit family, credential pattern detected in output
    Given the tool "nuclei" is registered in the "rainbow" family at Zone 2
    And the execution mode resolves to "local"
    And the engagement "pentest-2026-001" is initialized
    And the tool output will contain a string matching the AWS access key pattern
    When the user runs "jerry tool exec --family rainbow nuclei -u target.com"
    Then the output contains "[CREDENTIAL-REDACTED]"
    And the exit code is 4

  # ---------------------------------------------------------------------------
  # Alternative Flow: --verbose with explicit family
  # ---------------------------------------------------------------------------

  @verbose
  Scenario: Verbose mode confirms explicit family bypass
    Given the tool "syft" is registered in the "rainbow" family at Zone 1
    And the execution mode resolves to "local"
    When the user runs "jerry tool exec --family rainbow --verbose syft --version"
    Then the output includes "Explicit family: rainbow. Skipping auto-detection."
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # Bypass auto-detection confirmation
  # ---------------------------------------------------------------------------

  @auto-detect-bypass
  Scenario: Explicit family flag prevents querying other families
    Given the "rainbow" family is registered at priority 10
    And the "ai-cli" family is registered at priority 50
    And both families are enabled
    When the user runs "jerry tool exec --family rainbow syft --version"
    Then the "ai-cli" family's can_resolve() is never called
    And the exit code is 0
