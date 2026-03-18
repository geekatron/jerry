@tool-exec @health-check @UC-TOOLEXEC-006
Feature: Health check (UC-TOOLEXEC-006)
  As a security engineer or developer
  I want to verify tool availability across families before starting an engagement
  So that I can diagnose configuration issues and confirm my environment is ready

  Background:
    Given the tool families registry "tool_families.yaml" is loaded

  # ---------------------------------------------------------------------------
  # Basic Flow: All families health check
  # ---------------------------------------------------------------------------

  @exit-0 @all-families
  Scenario: Health check across all enabled families
    Given the "rainbow" family is registered and enabled
    And Docker is running
    And the rainbow container services are running
    When the user runs "jerry tool --health-check"
    Then the output contains a status table with columns: Family, Tool, Mode, Status, Detail
    And the output includes entries for each tool in the "rainbow" family
    And the output includes a summary line with total, available, and unavailable counts
    And the exit code is 0

  @exit-0 @all-families
  Scenario: Health check with multiple families
    Given the "rainbow" family is registered and enabled
    And the "ai-cli" family is registered and enabled
    When the user runs "jerry tool --health-check"
    Then the output contains entries for both "rainbow" and "ai-cli" families
    And the exit code is 0

  @exit-0 @all-families
  Scenario: Health check skips disabled families in all-families mode
    Given the "rainbow" family is registered and enabled
    And the "blue-team" family is registered but disabled
    When the user runs "jerry tool --health-check"
    Then the output contains entries for "rainbow" family
    And the output does not contain entries for "blue-team" family
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # Basic Flow: Single family health check
  # ---------------------------------------------------------------------------

  @exit-0 @single-family
  Scenario: Health check for specific family
    Given the "rainbow" family is registered and enabled
    When the user runs "jerry tool --health-check --family rainbow"
    Then the output contains entries only for the "rainbow" family
    And the exit code is 0

  @exit-0 @single-family
  Scenario: Health check for disabled family via explicit --family flag
    Given the "blue-team" family is registered but disabled
    When the user runs "jerry tool --health-check --family blue-team"
    Then the output contains entries for the "blue-team" family
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # Rainbow family: Docker container checks
  # ---------------------------------------------------------------------------

  @rainbow @container @exit-0
  Scenario: Rainbow health check reports running containers as available
    Given the "rainbow" family is registered and enabled
    And the container service "recon-pipeline" is running
    And the container service "exploit-ops" is running
    When the user runs "jerry tool --health-check --family rainbow"
    Then the row for tools in sub-skill "rainbow-recon" shows status "available"
    And the row for tools in sub-skill "rainbow-exploit" shows status "available"
    And the exit code is 0

  @rainbow @container @exit-0
  Scenario: Rainbow health check reports stopped containers as unavailable
    Given the "rainbow" family is registered and enabled
    And the container service "recon-pipeline" is not running
    When the user runs "jerry tool --health-check --family rainbow"
    Then the row for "subfinder" shows status "unavailable" in container mode
    And the detail column contains "not running"
    And the exit code is 0

  @rainbow @local @exit-0
  Scenario: Rainbow health check reports local tool availability via PATH
    Given the "rainbow" family is registered and enabled
    And the tool "syft" is available in PATH
    And the tool "nuclei" is not available in PATH
    When the user runs "jerry tool --health-check --family rainbow"
    Then the row for "syft" shows status "available" in local mode
    And the row for "nuclei" shows status "unavailable" in local mode
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # AI CLI family: Executable and API key checks
  # ---------------------------------------------------------------------------

  @ai-cli @exit-0
  Scenario: AI CLI health check reports executable and API key status
    Given the "ai-cli" family is registered and enabled
    And the executable "gemini" is available in PATH
    And the environment variable "GEMINI_API_KEY" is set
    When the user runs "jerry tool --health-check --family ai-cli"
    Then the row for "gemini" shows status "available"
    And the exit code is 0

  @ai-cli @exit-0
  Scenario: AI CLI health check reports missing executable as unavailable
    Given the "ai-cli" family is registered and enabled
    And the executable "codex" is not available in PATH
    When the user runs "jerry tool --health-check --family ai-cli"
    Then the row for "codex" shows status "unavailable"
    And the detail column contains "Executable not found"
    And the exit code is 0

  @ai-cli @exit-0
  Scenario: AI CLI health check reports missing API key as degraded
    Given the "ai-cli" family is registered and enabled
    And the executable "gemini" is available in PATH
    And the environment variable "GEMINI_API_KEY" is not set
    When the user runs "jerry tool --health-check --family ai-cli"
    Then the row for "gemini" shows status "degraded"
    And the detail column contains "API key GEMINI_API_KEY not set"
    And the exit code is 0

  @ai-cli @exit-0 @security
  Scenario: API key values are never displayed in health check output
    Given the "ai-cli" family is registered and enabled
    And the environment variable "GEMINI_API_KEY" is set to "AIzaSyAbCdEfGh123456"
    When the user runs "jerry tool --health-check --family ai-cli"
    Then the output does not contain "AIzaSyAbCdEfGh123456"
    And the output does not contain the value of any API key environment variable
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # Extension 3a: --family with invalid name (exit 7)
  # ---------------------------------------------------------------------------

  @exit-7 @error
  Scenario: Health check with non-existent family name
    Given no family named "nonexistent" is registered
    When the user runs "jerry tool --health-check --family nonexistent"
    Then the error message contains "Family 'nonexistent' not found"
    And the error message lists available families
    And the exit code is 7

  # ---------------------------------------------------------------------------
  # Extension 5a: Docker daemon not running
  # ---------------------------------------------------------------------------

  @rainbow @docker-down @exit-0
  Scenario: Docker daemon not running degrades container checks gracefully
    Given the "rainbow" family is registered and enabled
    And Docker daemon is not running
    When the user runs "jerry tool --health-check --family rainbow"
    Then all container-mode tools show status "unavailable"
    And the detail column contains "Docker daemon not running"
    And local-mode tool checks still execute
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # Extension 5b: Compose file not found
  # ---------------------------------------------------------------------------

  @rainbow @compose-missing @exit-0
  Scenario: Missing compose file degrades that sub-skill gracefully
    Given the "rainbow" family is registered and enabled
    And the compose file for "rainbow-exploit" does not exist
    And the compose file for "rainbow-recon" exists
    When the user runs "jerry tool --health-check --family rainbow"
    Then tools in sub-skill "rainbow-exploit" show status "unavailable"
    And the detail column contains "Compose file not found"
    And tools in sub-skill "rainbow-recon" are checked normally
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # Extension 6a: AI CLI executable not in PATH
  # ---------------------------------------------------------------------------

  @ai-cli @exit-0
  Scenario: AI CLI tool not in PATH reports unavailable without stopping others
    Given the "ai-cli" family is registered and enabled
    And the executable "gemini" is available in PATH
    And the executable "codex" is not available in PATH
    And the executable "claude-code" is not available in PATH
    When the user runs "jerry tool --health-check --family ai-cli"
    Then the row for "gemini" shows status "available" or "degraded"
    And the row for "codex" shows status "unavailable"
    And the row for "claude-code" shows status "unavailable"
    And all three tools are reported (no short-circuit)
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # Summary line verification
  # ---------------------------------------------------------------------------

  @summary @exit-0
  Scenario: Health check summary shows correct counts
    Given the "rainbow" family is registered and enabled
    And 30 out of 34 rainbow tools are available
    And 4 rainbow tools are unavailable
    When the user runs "jerry tool --health-check --family rainbow"
    Then the summary line shows "34 total, 30 available, 4 unavailable"
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # Non-failure guarantee (DR-023)
  # ---------------------------------------------------------------------------

  @exit-0 @graceful
  Scenario: Health check itself never fails due to tool unavailability
    Given the "rainbow" family is registered and enabled
    And Docker daemon is not running
    And no rainbow tools are available in PATH
    When the user runs "jerry tool --health-check --family rainbow"
    Then all tools show status "unavailable"
    And the exit code is 0
