@tool-exec @engagement @UC-TOOLEXEC-003
Feature: Initialize engagement (UC-TOOLEXEC-003)
  As a security engineer
  I want to initialize an engagement workspace before running Zone 2/3 tools
  So that evidence, reports, and quarantined credentials are organized per engagement

  # ---------------------------------------------------------------------------
  # Basic Flow: Happy path -- create new engagement
  # ---------------------------------------------------------------------------

  @exit-0 @create
  Scenario: Initialize a new engagement with valid ID
    Given no engagement directory exists for "pentest-2026-001"
    When the user runs "jerry tool exec --init-engagement pentest-2026-001"
    Then the directory "work/engagements/pentest-2026-001/" is created
    And the subdirectory "work/engagements/pentest-2026-001/evidence/" exists
    And the subdirectory "work/engagements/pentest-2026-001/reports/" exists
    And the subdirectory "work/engagements/pentest-2026-001/.credential-quarantine/" exists
    And the file "work/engagements/pentest-2026-001/.engagement-meta.json" exists
    And the ".engagement-meta.json" contains the field "id" with value "pentest-2026-001"
    And the ".engagement-meta.json" contains the field "created_at" in ISO 8601 format
    And the confirmation message contains "Engagement 'pentest-2026-001' initialized"
    And the exit code is 0

  @exit-0 @create
  Scenario: Initialize engagement with hyphenated ID
    Given no engagement directory exists for "client-abc-q1-2026"
    When the user runs "jerry tool exec --init-engagement client-abc-q1-2026"
    Then the directory "work/engagements/client-abc-q1-2026/" is created
    And the exit code is 0

  @exit-0 @create
  Scenario: Initialize engagement with underscore ID
    Given no engagement directory exists for "internal_audit_003"
    When the user runs "jerry tool exec --init-engagement internal_audit_003"
    Then the directory "work/engagements/internal_audit_003/" is created
    And the exit code is 0

  @exit-0 @create
  Scenario: Initialize engagement with numeric-only ID
    Given no engagement directory exists for "20260317"
    When the user runs "jerry tool exec --init-engagement 20260317"
    Then the directory "work/engagements/20260317/" is created
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # Extension 2a: Invalid engagement ID format (exit 1)
  # ---------------------------------------------------------------------------

  @exit-1 @error @validation
  Scenario: Engagement ID with path separator is rejected
    When the user runs "jerry tool exec --init-engagement ../etc/passwd"
    Then the error message contains "Invalid engagement ID format"
    And no directory is created
    And the exit code is 1

  @exit-1 @error @validation
  Scenario: Engagement ID with forward slash is rejected
    When the user runs "jerry tool exec --init-engagement foo/bar"
    Then the error message contains "Invalid engagement ID format"
    And the exit code is 1

  @exit-1 @error @validation
  Scenario: Engagement ID with spaces is rejected
    When the user runs "jerry tool exec --init-engagement 'pentest 2026'"
    Then the error message contains "Invalid engagement ID format"
    And the exit code is 1

  @exit-1 @error @validation
  Scenario: Engagement ID with shell metacharacters is rejected
    When the user runs "jerry tool exec --init-engagement 'test;rm -rf /'"
    Then the error message contains "Invalid engagement ID format"
    And the exit code is 1

  @exit-1 @error @validation
  Scenario: Engagement ID with backslash is rejected
    When the user runs "jerry tool exec --init-engagement 'test\\..\\.etc'"
    Then the error message contains "Invalid engagement ID format"
    And the exit code is 1

  @exit-1 @error @validation
  Scenario: Empty engagement ID is rejected
    When the user runs "jerry tool exec --init-engagement ''"
    Then the error message contains "Invalid engagement ID format"
    And the exit code is 1

  @exit-1 @error @validation
  Scenario Outline: Engagement ID with special character <char> is rejected
    When the user runs "jerry tool exec --init-engagement 'test<char>value'"
    Then the error message contains "Invalid engagement ID format"
    And the exit code is 1

    Examples:
      | char |
      | $    |
      | `    |
      | \|   |
      | >    |
      | <    |
      | &    |

  # ---------------------------------------------------------------------------
  # Extension 4a: Idempotent -- directory already exists (exit 0)
  # ---------------------------------------------------------------------------

  @exit-0 @idempotent
  Scenario: Re-initializing an existing engagement is idempotent
    Given the engagement "pentest-2026-001" already exists with all subdirectories
    And the ".engagement-meta.json" has created_at "2026-03-15T10:00:00Z"
    When the user runs "jerry tool exec --init-engagement pentest-2026-001"
    Then no existing files are overwritten
    And the ".engagement-meta.json" still has created_at "2026-03-15T10:00:00Z"
    And the confirmation message contains "already exists"
    And the exit code is 0

  @exit-0 @idempotent
  Scenario: Re-initializing engagement with missing subdirectory repairs structure
    Given the engagement "pentest-2026-001" exists
    But the subdirectory "work/engagements/pentest-2026-001/reports/" is missing
    When the user runs "jerry tool exec --init-engagement pentest-2026-001"
    Then the subdirectory "work/engagements/pentest-2026-001/reports/" is created
    And the subdirectory "work/engagements/pentest-2026-001/evidence/" still exists
    And the ".engagement-meta.json" is preserved
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # Meta.json content verification
  # ---------------------------------------------------------------------------

  @meta-json
  Scenario: Engagement meta.json contains required fields
    Given no engagement directory exists for "audit-2026-q1"
    When the user runs "jerry tool exec --init-engagement audit-2026-q1"
    Then the ".engagement-meta.json" contains exactly these fields:
      | Field      | Type   |
      | id         | string |
      | created_at | string |
      | created_by | string |
    And the "id" field equals "audit-2026-q1"
    And the "created_at" field matches ISO 8601 pattern
    And the exit code is 0
