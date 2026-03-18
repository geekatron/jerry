@tool-exec @auto-detect @UC-TOOLEXEC-001
Feature: Execute tool with auto-family detection (UC-TOOLEXEC-001)
  As a security engineer
  I want to run "jerry tool exec <tool> [args]" without specifying a family
  So that the system auto-detects the owning family and executes the tool transparently

  Background:
    Given the tool families registry "tool_families.yaml" is loaded
    And the "rainbow" family is registered at priority 10
    And the "rainbow" family is enabled
    And the credential filter service is active

  # ---------------------------------------------------------------------------
  # Basic Flow: Happy path -- Zone 1 local execution (BC-01)
  # ---------------------------------------------------------------------------

  @BC-01 @zone-1 @local-mode @exit-0
  Scenario: Auto-detect rainbow family and execute a Zone 1 tool locally
    Given the tool "syft" is registered in the "rainbow" family at Zone 1
    And no engagement is required for Zone 1 tools
    And the execution mode resolves to "local"
    When the user runs "jerry tool exec syft --version"
    Then the system queries "rainbow" family can_resolve("syft")
    And the "rainbow" family claims the tool
    And the tool executes via local subprocess
    And the credential filter is applied to the output
    And the exit code is 0

  @BC-01 @zone-1 @local-mode @exit-0
  Scenario: Auto-detect rainbow family and execute a Zone 1 cloud tool locally
    Given the tool "checkov" is registered in the "rainbow" family at Zone 1
    And no engagement is required for Zone 1 tools
    And the execution mode resolves to "local"
    When the user runs "jerry tool exec checkov --version"
    Then the system auto-detects the "rainbow" family
    And the tool executes via local subprocess
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # Basic Flow: Zone 2 container execution (BC-02)
  # ---------------------------------------------------------------------------

  @BC-02 @zone-2 @container-mode @exit-0
  Scenario: Auto-detect and execute a Zone 2 recon tool in container mode
    Given the tool "subfinder" is registered in the "rainbow" family at Zone 2
    And the engagement "pentest-2026-001" is initialized
    And the execution mode resolves to "container"
    And the container service "recon-pipeline" is running
    When the user runs "jerry tool exec subfinder -d example.com"
    Then the system auto-detects the "rainbow" family
    And the tool executes via "docker compose exec -T recon-pipeline subfinder -d example.com"
    And the credential filter is applied to the output
    And evidence is persisted to "work/engagements/pentest-2026-001/evidence/"
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # Basic Flow: Zone 3 exploit tool (BC-02, BC-08)
  # ---------------------------------------------------------------------------

  @BC-02 @zone-3 @container-mode @exit-0
  Scenario: Auto-detect and execute a Zone 3 exploit tool in container mode
    Given the tool "impacket-smbclient" is registered in the "rainbow" family at Zone 3
    And the engagement "pentest-2026-001" is initialized
    And the execution mode resolves to "container"
    And the container service "exploit-ops" is running
    When the user runs "jerry tool exec impacket-smbclient --help"
    Then the system auto-detects the "rainbow" family
    And the tool executes via "docker compose exec -T exploit-ops impacket-smbclient --help"
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # Priority-based auto-detection
  # ---------------------------------------------------------------------------

  @auto-detect @priority
  Scenario: Auto-detection queries families in priority order (lowest first)
    Given the "rainbow" family is registered at priority 10
    And the "ai-cli" family is registered at priority 50
    And both families are enabled
    And the tool "nuclei" is registered in the "rainbow" family
    And the "ai-cli" family does not recognize "nuclei"
    When the user runs "jerry tool exec nuclei --version"
    Then the system queries "rainbow" family first (priority 10)
    And the "rainbow" family claims the tool
    And the "ai-cli" family is never queried

  @auto-detect @priority @first-match
  Scenario: Auto-detection stops at first matching family
    Given the "rainbow" family is registered at priority 10
    And the "rainbow" family recognizes "syft"
    When the user runs "jerry tool exec syft --version"
    Then the system queries "rainbow" family can_resolve("syft")
    And the "rainbow" family returns True
    And no further families are queried

  # ---------------------------------------------------------------------------
  # Extension 3a: Unknown tool -- no family recognizes it (exit 1)
  # ---------------------------------------------------------------------------

  @BC-05 @exit-1 @error
  Scenario: No family recognizes the tool command
    Given no registered family recognizes the tool "unknowntool"
    When the user runs "jerry tool exec unknowntool --help"
    Then the system queries all registered families
    And no family claims the tool
    And the error message contains "Unknown tool: unknowntool"
    And the error message lists available families
    And the exit code is 1

  @BC-05 @exit-1 @error
  Scenario: Misspelled tool name is not recognized
    Given no registered family recognizes the tool "nulcei"
    When the user runs "jerry tool exec nulcei -u target.com"
    Then the exit code is 1
    And the error message contains "Unknown tool: nulcei"

  # ---------------------------------------------------------------------------
  # Extension 7a: Engagement not initialized (exit 5, BC-08)
  # ---------------------------------------------------------------------------

  @BC-08 @exit-5 @error
  Scenario: Zone 2 tool requires engagement but none is initialized
    Given the tool "subfinder" is registered in the "rainbow" family at Zone 2
    And the "rainbow" family requires engagement for Zone 2 tools
    And no engagement is initialized
    When the user runs "jerry tool exec subfinder -d example.com"
    Then the error message contains "Engagement not initialized"
    And the error message contains "jerry tool exec --init-engagement"
    And the exit code is 5

  @BC-08 @exit-5 @error
  Scenario: Zone 3 tool requires engagement but none is initialized
    Given the tool "impacket-smbclient" is registered in the "rainbow" family at Zone 3
    And no engagement is initialized
    When the user runs "jerry tool exec impacket-smbclient //target/share"
    Then the exit code is 5

  # ---------------------------------------------------------------------------
  # Extension 7b: Strict mode + Zone 2/3 + no explicit mode (exit 6, BC-03)
  # ---------------------------------------------------------------------------

  @BC-03 @exit-6 @strict-mode @error
  Scenario: Strict mode blocks Zone 2 tool without explicit mode
    Given the tool "nuclei" is registered in the "rainbow" family at Zone 2
    And strict mode is active
    And no execution mode is specified via CLI flag or environment variable
    And the engagement "pentest-2026-001" is initialized
    When the user runs "jerry tool exec nuclei -u target.com"
    Then the error message contains "Strict mode requires explicit mode selection"
    And the exit code is 6

  @BC-03 @exit-6 @strict-mode @error
  Scenario: Strict mode blocks Zone 3 tool without explicit mode
    Given the tool "msfconsole" is registered in the "rainbow" family at Zone 3
    And strict mode is active
    And no execution mode is specified via CLI flag or environment variable
    And the engagement "pentest-2026-001" is initialized
    When the user runs "jerry tool exec msfconsole"
    Then the exit code is 6

  @BC-03 @strict-mode @exit-0
  Scenario: Strict mode allows Zone 2 tool with explicit mode flag
    Given the tool "nuclei" is registered in the "rainbow" family at Zone 2
    And strict mode is active
    And the engagement "pentest-2026-001" is initialized
    And the container service "recon-pipeline" is running
    When the user runs "jerry tool exec --mode container nuclei -u target.com"
    Then the tool executes successfully
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # Extension 8a: Container not running, auto-start fails (exit 3, BC-06)
  # ---------------------------------------------------------------------------

  @BC-06 @exit-3 @container-mode @error
  Scenario: Container not running and auto-start fails
    Given the tool "subfinder" is registered in the "rainbow" family at Zone 2
    And the execution mode resolves to "container"
    And the container service "recon-pipeline" is not running
    And docker compose auto-start fails for "recon-pipeline"
    And the engagement "pentest-2026-001" is initialized
    When the user runs "jerry tool exec subfinder -d example.com"
    Then the system attempts to auto-start the container
    And the auto-start fails
    And the error message contains "Container" and "not running"
    And the exit code is 3

  @BC-06 @container-mode @exit-0
  Scenario: Container not running but auto-start succeeds
    Given the tool "subfinder" is registered in the "rainbow" family at Zone 2
    And the execution mode resolves to "container"
    And the container service "recon-pipeline" is not running
    And docker compose auto-start succeeds for "recon-pipeline"
    And the engagement "pentest-2026-001" is initialized
    When the user runs "jerry tool exec subfinder -d example.com"
    Then the system attempts to auto-start the container
    And the auto-start succeeds
    And the tool executes successfully
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # Extension 8b: Tool execution error (exit 2)
  # ---------------------------------------------------------------------------

  @exit-2 @error
  Scenario: Tool process returns non-zero exit code
    Given the tool "grype" is registered in the "rainbow" family at Zone 1
    And the execution mode resolves to "local"
    And the tool "grype" will fail with a non-zero exit code
    When the user runs "jerry tool exec grype db check"
    Then the tool's stderr is propagated to the user
    And the exit code is 2

  # ---------------------------------------------------------------------------
  # Extension 9a: Credential detected in output (exit 4, BC-07)
  # ---------------------------------------------------------------------------

  @BC-07 @exit-4 @credential-filter
  Scenario: AWS access key pattern detected in tool output
    Given the tool "nuclei" is registered in the "rainbow" family at Zone 2
    And the execution mode resolves to "local"
    And the engagement "pentest-2026-001" is initialized
    And the tool output will contain a string matching the AWS access key pattern
    When the user runs "jerry tool exec nuclei -u target.com"
    Then the output contains "[CREDENTIAL-REDACTED]" instead of the matched pattern
    And the raw output is quarantined to ".credential-quarantine/"
    And the quarantine filename contains a SHA-256 hash
    And the exit code is 4

  @BC-07 @exit-4 @credential-filter
  Scenario: Private key header detected in tool output
    Given the tool "subfinder" is registered in the "rainbow" family at Zone 2
    And the execution mode resolves to "local"
    And the engagement "pentest-2026-001" is initialized
    And the tool output will contain a PEM private key header
    When the user runs "jerry tool exec subfinder -d example.com"
    Then the output contains "[CREDENTIAL-REDACTED]"
    And the exit code is 4

  @BC-07 @exit-4 @credential-filter
  Scenario: Connection string with password detected in tool output
    Given the tool "checkov" is registered in the "rainbow" family at Zone 1
    And the execution mode resolves to "local"
    And the tool output will contain a database connection string with embedded password
    When the user runs "jerry tool exec checkov -d /app"
    Then the output contains "[CREDENTIAL-REDACTED]"
    And the exit code is 4

  # ---------------------------------------------------------------------------
  # Mode precedence (4-level)
  # ---------------------------------------------------------------------------

  @mode-precedence
  Scenario: CLI --mode flag takes highest precedence
    Given the tool "syft" is registered in the "rainbow" family at Zone 1
    And the environment variable "JERRY_TOOL_MODE" is set to "container"
    And the config file default_mode is "container"
    When the user runs "jerry tool exec --mode local syft --version"
    Then the execution mode is "local"
    And the tool executes via local subprocess

  @mode-precedence
  Scenario: Environment variable takes precedence over config file
    Given the tool "syft" is registered in the "rainbow" family at Zone 1
    And the environment variable "JERRY_TOOL_MODE" is set to "container"
    And the config file default_mode is "local"
    And no --mode flag is provided
    When the user runs "jerry tool exec syft --version"
    Then the execution mode is "container"

  @mode-precedence
  Scenario: Config file default_mode used when no flag or env var
    Given the tool "syft" is registered in the "rainbow" family at Zone 1
    And no --mode flag is provided
    And no execution mode environment variable is set
    And the config file default_mode is "container"
    When the user runs "jerry tool exec syft --version"
    Then the execution mode is "container"

  @mode-precedence
  Scenario: Hardcoded 'local' fallback when nothing else is set
    Given the tool "syft" is registered in the "rainbow" family at Zone 1
    And no --mode flag is provided
    And no execution mode environment variable is set
    And the config file does not specify default_mode
    When the user runs "jerry tool exec syft --version"
    Then the execution mode is "local"

  # ---------------------------------------------------------------------------
  # Alternative Flow: --verbose flag
  # ---------------------------------------------------------------------------

  @verbose
  Scenario: Verbose mode logs family resolution details
    Given the tool "nuclei" is registered in the "rainbow" family at Zone 2
    And the engagement "pentest-2026-001" is initialized
    And the execution mode resolves to "local"
    When the user runs "jerry tool exec --verbose nuclei --version"
    Then the output includes family resolution log entries
    And the log shows which families were queried
    And the log shows the claiming family is "rainbow"
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # Alternative Flow: --zone override
  # ---------------------------------------------------------------------------

  @zone-override
  Scenario: User overrides default zone with --zone flag
    Given the tool "nuclei" is registered in the "rainbow" family at Zone 2
    And the engagement "pentest-2026-001" is initialized
    And the execution mode resolves to "local"
    When the user runs "jerry tool exec --zone 3 nuclei -u target.com"
    Then the security policy validation uses Zone 3 constraints
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # BC-04: Zone 1 fallback
  # ---------------------------------------------------------------------------

  @BC-04 @zone-1 @fallback
  Scenario: Zone 1 tool executes without engagement (fallback safe zone)
    Given the tool "checkov" is registered in the "rainbow" family at Zone 1
    And no engagement is initialized
    And the execution mode resolves to "local"
    When the user runs "jerry tool exec checkov --version"
    Then no engagement check is performed for Zone 1
    And the tool executes successfully
    And the exit code is 0
