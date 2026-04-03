---
source_use_case: UC-LIB-001
source_title: "Borrow a Book"
source_detail_level: ESSENTIAL_OUTLINE
source_goal_level: USER_GOAL
generated_by: tspec-generator
generated_at: "2026-03-09T10:00:00Z"
scenario_count: 4
coverage:
  basic_flow_mapped: true
  alternative_flows_mapped: 0
  extensions_mapped: 3
  total_flows: 4
  mapped_flows: 4
slice_id: null
version: "1.0.0"
---

# Feature: Borrow a Book

> As a Library Member, I want to borrow a book from the library so that I receive the book with a clear due date and no unnecessary delay.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Happy Path](#happy-path) | Main success scenario -- all preconditions met, book available |
| [Error Scenarios](#error-scenarios) | EXT-2A (card invalid), EXT-2B (overdue loans), EXT-3A (book unavailable) |
| [Traceability Matrix](#traceability-matrix) | Scenario-to-flow cross-reference for tspec-analyst |

---

## Happy Path

### Scenario: Borrow a Book - Main Success Scenario

**Source:** basic_flow (steps 1-5)

```gherkin
Given Library Member holds a valid, active library card
  And Library Member has no outstanding overdue books
When Library Member presents library card and requests a specific book copy at the circulation desk
  And the system verifies that member card status is valid and no overdue loans exist
  And the system verifies that the requested book copy is available for loan
  And Library Member confirms the loan and accepts the due date
Then the system creates a loan record, updates the book copy status to CHECKED_OUT, and prints a due-date slip
  And loan record is created linking the member to the book copy
  And book copy status is changed to CHECKED_OUT
  And due date is issued to the member
```

---

## Error Scenarios

### Scenario: Borrow a Book - Member Card Invalid at Step 2

**Source:** EXT-2A (anchor_step: 2, outcome: failure)

```gherkin
Given Library Member holds an expired or suspended library card
  And Library Member has no outstanding overdue books
  And the member card fails validation at step 2
When Library Member presents library card and requests a specific book copy at the circulation desk
Then the system rejects the request
  And book copy status remains unchanged
  And the system notifies Library Member of the reason the loan was refused
```

### Scenario: Borrow a Book - Member Has Overdue Loans at Step 2

**Source:** EXT-2B (anchor_step: 2, outcome: failure)

```gherkin
Given Library Member holds a valid, active library card
  And Library Member has at least one outstanding overdue book
  And the overdue loan check fails at step 2
When Library Member presents library card and requests a specific book copy at the circulation desk
Then the system rejects the request
  And book copy status remains unchanged
  And the system notifies Library Member of the reason the loan was refused
```

### Scenario: Borrow a Book - Requested Book Copy Unavailable at Step 3

**Source:** EXT-3A (anchor_step: 3, outcome: failure)

```gherkin
Given Library Member holds a valid, active library card
  And Library Member has no outstanding overdue books
  And the requested book copy is not available for loan (status CHECKED_OUT or RESERVED)
When Library Member presents library card and requests a specific book copy at the circulation desk
  And the system verifies that member card status is valid and no overdue loans exist
Then the system rejects the request
  And book copy status remains unchanged
  And the system notifies Library Member of the reason the loan was refused
```

---

## Traceability Matrix

| Scenario | Source Flow | Source Step | Type |
|----------|-------------|-------------|------|
| Borrow a Book - Main Success Scenario | basic_flow | 1-5 | happy_path |
| Borrow a Book - Member Card Invalid at Step 2 | EXT-2A | 2 | error (failure) |
| Borrow a Book - Member Has Overdue Loans at Step 2 | EXT-2B | 2 | error (failure) |
| Borrow a Book - Requested Book Copy Unavailable at Step 3 | EXT-3A | 3 | error (failure) |

---

## Sample Notes

> **Source UC:** This Feature file was generated from UC-LIB-001 at ESSENTIAL_OUTLINE level. The source UC (at `skills/use-case/samples/sample-use-case.md`) is at BRIEFLY_DESCRIBED level in the repository. This sample demonstrates what the output would look like if UC-LIB-001 were elaborated to ESSENTIAL_OUTLINE with three extensions added: EXT-2A (card invalid), EXT-2B (overdue loans), EXT-3A (book unavailable).

> **Clark Transformation Applied:**
> - RULE-C1-01: Feature name = `$.title` verbatim ("Borrow a Book")
> - RULE-C2-01: User story narrative from `$.primary_actor` + `$.stakeholders[0].interest`
> - RULE-C3-01: All 5 basic_flow steps combined into ONE happy path Scenario
> - RULE-ST-01: Steps 1, 4 (actor_action) → When clauses
> - RULE-ST-02: Step 5 (system_response) → Then clause
> - RULE-ST-03: Steps 2, 3 (validation) → Then assertion clauses
> - RULE-C5-01 + RULE-OT-01: Each extension (outcome=failure) → dedicated negative test Scenario
> - RULE-C7-01: Traceability Matrix appended
> - Coverage: 4/4 flows mapped = 100% (meets USER_GOAL target of 100%)

*Sample Version: 1.0.0 | Generated by: tspec-generator (demonstration) | Date: 2026-03-09*
*Source: Clark, T. D. (2018). Generating BDD Test Scenarios from Use Case Specifications.*
