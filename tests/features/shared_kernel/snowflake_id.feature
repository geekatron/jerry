Feature: Snowflake ID Generation
  As a developer using Jerry Framework
  I want to generate unique IDs without coordination
  So that multiple Claude instances can create work items safely

  Background:
    Given the Snowflake epoch is configured

  @happy-path
  Scenario: Generate unique ID
    Given a Snowflake ID generator with worker ID 1
    When I generate an ID
    Then the ID should be a positive 64-bit integer
    And the ID should contain the worker ID 1

  @happy-path
  Scenario: Multiple IDs are unique
    Given a Snowflake ID generator with worker ID 1
    When I generate 1000 IDs
    Then all IDs should be unique

  @happy-path
  Scenario: IDs are time-sortable
    Given a Snowflake ID generator with worker ID 1
    When I generate an ID
    And I wait 10 milliseconds
    And I generate another ID
    Then the second ID should be greater than the first

  @happy-path
  Scenario: Different workers generate different IDs
    Given a Snowflake ID generator with worker ID 1
    And another Snowflake ID generator with worker ID 2
    When each generator produces 100 IDs simultaneously
    Then all 200 IDs should be unique

  @happy-path
  Scenario: Parse ID extracts components
    Given a Snowflake ID generator with worker ID 742
    When I generate an ID
    And I parse the generated ID
    Then the parsed worker ID should be 742
    And the parsed sequence should be between 0 and 4095
    And the parsed timestamp should be recent

  @happy-path
  Scenario: Convert ID to base62
    Given a Snowflake ID generator with worker ID 1
    When I generate an ID
    And I convert the ID to base62
    Then the base62 string should be alphanumeric
    And the base62 string should be at most 11 characters

  @negative
  Scenario: Invalid worker ID rejected - negative
    When I create a generator with worker ID -1
    Then a ValueError should be raised with message containing "Worker ID"

  @negative
  Scenario: Invalid worker ID rejected - too large
    When I create a generator with worker ID 1024
    Then a ValueError should be raised with message containing "Worker ID"

  @edge-case
  Scenario: Derive worker ID is deterministic per process
    When I derive a worker ID
    And I derive another worker ID in the same process
    Then both derived worker IDs should be identical

  @edge-case
  Scenario: Worker ID is within valid range
    When I derive a worker ID
    Then the derived worker ID should be between 0 and 1023

  @boundary
  Scenario: Maximum worker ID accepted
    Given a Snowflake ID generator with worker ID 1023
    When I generate an ID
    Then the ID should be a positive 64-bit integer

  @boundary
  Scenario: Minimum worker ID accepted
    Given a Snowflake ID generator with worker ID 0
    When I generate an ID
    Then the ID should be a positive 64-bit integer
