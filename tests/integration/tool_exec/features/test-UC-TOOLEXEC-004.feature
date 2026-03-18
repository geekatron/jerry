@tool-exec @discovery @UC-TOOLEXEC-004
Feature: List families and tools (UC-TOOLEXEC-004)
  As a security engineer or developer
  I want to list available tool families and their registered tools
  So that I can discover what tools are available and how they are configured

  Background:
    Given the tool families registry "tool_families.yaml" is loaded

  # ---------------------------------------------------------------------------
  # Basic Flow: --list-families
  # ---------------------------------------------------------------------------

  @list-families @exit-0
  Scenario: List all registered families
    Given the "rainbow" family is registered and enabled with 34 tools
    When the user runs "jerry tool --list-families"
    Then the output contains a table with columns: Name, Description, Status, Tool Count, Config Path
    And the table includes a row for "rainbow" with status "enabled"
    And the exit code is 0

  @list-families @exit-0
  Scenario: List families includes disabled families with status indicator
    Given the "rainbow" family is registered and enabled
    And the "blue-team" family is registered but disabled
    When the user runs "jerry tool --list-families"
    Then the output contains a row for "rainbow" with status "enabled"
    And the output contains a row for "blue-team" with status "disabled"
    And the exit code is 0

  @list-families @exit-0
  Scenario: List families shows priority ordering
    Given the "rainbow" family is registered at priority 10
    And the "ai-cli" family is registered at priority 50
    When the user runs "jerry tool --list-families"
    Then "rainbow" appears before "ai-cli" in the output
    And the exit code is 0

  @list-families @exit-0
  Scenario: List families with single registered family
    Given only the "rainbow" family is registered
    When the user runs "jerry tool --list-families"
    Then the output contains exactly one family row
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # Basic Flow: --list-tools (all families)
  # ---------------------------------------------------------------------------

  @list-tools @exit-0
  Scenario: List all tools across all enabled families
    Given the "rainbow" family is registered and enabled
    And the "rainbow" family has tools: "syft", "grype", "nuclei", "subfinder"
    When the user runs "jerry tool --list-tools"
    Then the output contains a table with columns: Tool, Family, Zone, Default Mode
    And the table includes rows for "syft", "grype", "nuclei", "subfinder"
    And each row shows the owning family "rainbow"
    And the exit code is 0

  @list-tools @exit-0
  Scenario: List tools shows zone information for rainbow family
    Given the "rainbow" family is registered and enabled
    And the tool "syft" is registered at Zone 1
    And the tool "subfinder" is registered at Zone 2
    And the tool "impacket-smbclient" is registered at Zone 3
    When the user runs "jerry tool --list-tools"
    Then the row for "syft" shows Zone "1"
    And the row for "subfinder" shows Zone "2"
    And the row for "impacket-smbclient" shows Zone "3"
    And the exit code is 0

  @list-tools @exit-0
  Scenario: List tools shows dash for families without zones
    Given the "ai-cli" family is registered and enabled
    And the "ai-cli" family has tool "gemini" with no zone
    When the user runs "jerry tool --list-tools"
    Then the row for "gemini" shows Zone "--"
    And the exit code is 0

  @list-tools @exit-0
  Scenario: List tools excludes disabled families
    Given the "rainbow" family is registered and enabled with tool "syft"
    And the "blue-team" family is registered but disabled with tool "yr"
    When the user runs "jerry tool --list-tools"
    Then the output contains a row for "syft"
    And the output does not contain a row for "yr"
    And the exit code is 0

  @list-tools @exit-0
  Scenario: List tools sorted by family priority then tool prefix
    Given the "rainbow" family is at priority 10 with tools "syft", "nuclei"
    And the "ai-cli" family is at priority 50 with tool "gemini"
    When the user runs "jerry tool --list-tools"
    Then "nuclei" appears before "gemini" in the output
    And "syft" appears before "gemini" in the output
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # Basic Flow: --list-tools --family <name>
  # ---------------------------------------------------------------------------

  @list-tools @exit-0 @filtered
  Scenario: List tools filtered by specific family
    Given the "rainbow" family is registered and enabled
    And the "rainbow" family has tools: "syft", "grype", "nuclei"
    When the user runs "jerry tool --list-tools --family rainbow"
    Then the output contains rows only for tools in the "rainbow" family
    And the exit code is 0

  @list-tools @exit-0 @filtered
  Scenario: List tools for a family with many tools
    Given the "rainbow" family is registered with 34 tool prefixes
    When the user runs "jerry tool --list-tools --family rainbow"
    Then the output contains 34 tool entries
    And each entry shows family "rainbow"
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # Extension 3a: --list-tools --family with invalid name (exit 7)
  # ---------------------------------------------------------------------------

  @list-tools @exit-7 @error
  Scenario: List tools with non-existent family name
    Given no family named "nonexistent" is registered
    When the user runs "jerry tool --list-tools --family nonexistent"
    Then the error message contains "Family 'nonexistent' not found"
    And the error message lists available families
    And the exit code is 7

  # ---------------------------------------------------------------------------
  # Extension 2a: Registry missing or unparseable (exit 8)
  # ---------------------------------------------------------------------------

  @exit-8 @error
  Scenario: Registry file is missing
    Given the tool families registry file does not exist
    When the user runs "jerry tool --list-families"
    Then the error message contains "registry not found"
    And the exit code is 8

  @exit-8 @error
  Scenario: Registry file contains invalid YAML
    Given the tool families registry file contains invalid YAML
    When the user runs "jerry tool --list-families"
    Then the error message contains "registry" and "invalid"
    And the exit code is 8
