@blue-team @lead @AC-F-01 @H-20
Feature: Blue Team Lead Agent
  As a security operator using /blue-team
  I want the blue-lead agent to coordinate defensive operations
  So that I can scope assessments and manage the blue-team workflow

  Background:
    Given the blue-lead agent is invoked
    And the JERRY_PROJECT environment variable is set

  @scope
  Scenario: Create assessment scope document
    When the agent is asked to create an assessment scope
    Then the agent produces a scope document at the designated output path
    And the scope document contains assessment_type field
    And the scope document contains target_scope field

  @scope
  Scenario: Reject operations without assessment scope
    Given no assessment scope document exists
    When the agent is asked to coordinate a detection assessment
    Then the agent HALTS and requests scope creation first

  @routing
  Scenario: Route detection request to blue-detect
    Given a valid assessment scope exists
    When the agent receives a YARA rule validation request
    Then the agent routes to blue-detect agent
    And the handoff includes the assessment scope reference

  @routing
  Scenario: Route compliance request to blue-comply
    Given a valid assessment scope exists
    When the agent receives a compliance audit request
    Then the agent routes to blue-comply agent

  @routing
  Scenario: Route threat intel request to blue-intel
    Given a valid assessment scope exists
    When the agent receives a threat intelligence request
    Then the agent routes to blue-intel agent

  @purple-team
  Scenario: Recognize purple team mode from scope
    Given a valid assessment scope with purple_team_mode enabled
    When the agent reviews the scope
    Then the agent activates purple team coordination protocol
    And the agent references the exchange directory path

  @constitutional
  Scenario: Refuse to spawn subagents
    When the agent is asked to directly invoke another agent
    Then the agent refuses per P-003
    And the agent returns routing recommendation to the orchestrator

  @constitutional
  Scenario: Disclose limitations honestly
    When the agent cannot determine the appropriate routing
    Then the agent discloses the ambiguity per P-022
    And the agent requests user guidance per H-31
