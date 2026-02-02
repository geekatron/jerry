Feature: Domain Event Base Class
  As a domain modeler
  I want immutable events to capture state changes
  So that I can maintain an audit trail and enable event sourcing

  Background:
    Given the EventId generator is available

  @happy-path
  Scenario: Create domain event with auto-generated ID
    When I create a domain event for aggregate "WORK-001" of type "WorkItem"
    Then the event should have a unique event ID starting with "EVT-"
    And the event should have a timestamp in UTC
    And the event should have aggregate ID "WORK-001"
    And the event should have aggregate type "WorkItem"

  @happy-path
  Scenario: Domain event is immutable
    Given a domain event for aggregate "WORK-001"
    When I try to modify the event's entity_id
    Then a FrozenInstanceError should be raised

  @happy-path
  Scenario: Serialize event to dictionary
    Given a domain event for aggregate "WORK-001" of type "WorkItem" with version 3
    When I convert the event to a dictionary
    Then the dictionary should contain key "event_type" with value "DomainEvent"
    And the dictionary should contain key "event_id"
    And the dictionary should contain key "timestamp" as ISO string
    And the dictionary should contain key "aggregate_id" with value "WORK-001"
    And the dictionary should contain key "aggregate_type" with value "WorkItem"
    And the dictionary should contain key "version" with value 3

  @happy-path
  Scenario: Deserialize event from dictionary
    Given a dictionary representing a DomainEvent for "WORK-001"
    When I reconstruct the event from the dictionary
    Then the reconstructed event should have aggregate ID "WORK-001"
    And the reconstructed event should have the same event ID as the dictionary

  @happy-path
  Scenario: Event equality by event_id
    Given two domain events with the same event_id "EVT-test-123"
    Then the events should be equal
    And the events should have the same hash

  @happy-path
  Scenario: Event inequality by different event_id
    Given a domain event with event_id "EVT-aaa"
    And another domain event with event_id "EVT-bbb"
    Then the events should not be equal

  @negative
  Scenario: Empty aggregate ID rejected
    When I create a domain event with empty aggregate ID
    Then a ValueError should be raised with message containing "aggregate_id"

  @negative
  Scenario: Empty aggregate type rejected
    When I create a domain event with empty aggregate type
    Then a ValueError should be raised with message containing "aggregate_type"

  @negative
  Scenario: Negative version rejected
    When I create a domain event with version -1
    Then a ValueError should be raised with message containing "version"

  @edge-case
  Scenario: Event subclass includes payload
    Given a custom event "WorkItemCreated" with title "Test Task"
    When I convert the event to a dictionary
    Then the dictionary should contain key "event_type" with value "WorkItemCreated"
    And the dictionary should contain key "title" with value "Test Task"

  @edge-case
  Scenario: Event subclass deserialization via registry
    Given a WorkItemCreated event dictionary with title "Test Task"
    When I deserialize using the event registry
    Then the result should be a WorkItemCreated instance
    And the result should have title "Test Task"
