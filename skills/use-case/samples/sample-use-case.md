---
id: UC-LIB-001
title: "Borrow a Book"
work_type: USE_CASE
version: "1.0.0"
status: APPROVED
goal_level: USER_GOAL
goal_symbol: "!"
domain: LIB
scope: "Library Management System"
primary_actor: "Library Member"
detail_level: BRIEFLY_DESCRIBED
trigger: "Member selects a book to borrow from the catalogue"
preconditions:
  - "Member holds a valid, active library card"
  - "Member has no outstanding overdue books"
postconditions:
  success:
    - "Loan record created linking the member to the book copy"
    - "Book copy status changed to CHECKED_OUT"
    - "Due date issued to the member"
  failure:
    - "Book copy status remains unchanged"
    - "Member is notified of the reason the loan was refused"
basic_flow:
  - step: 1
    actor: "Library Member"
    action: "presents library card and requests a specific book copy at the circulation desk"
    type: actor_action
  - step: 2
    actor: "System"
    action: "validates member card status and checks that no overdue loans exist"
    type: validation
  - step: 3
    actor: "System"
    action: "checks that the requested book copy is available for loan"
    type: validation
  - step: 4
    actor: "Library Member"
    action: "confirms the loan and accepts the due date"
    type: actor_action
  - step: 5
    actor: "System"
    action: "creates a loan record, updates the book copy status to CHECKED_OUT, and prints a due-date slip"
    type: system_response
supporting_actors:
  - name: "Librarian"
    type: human
stakeholders:
  - name: "Library Member"
    interest: "Receives the book with a clear due date and no unnecessary delay"
  - name: "Library Administration"
    interest: "Accurate loan records; overdue prevention through eligibility checks"
  - name: "Librarian"
    interest: "Simple, error-free checkout process"
priority: P1
realization_level: OUTLINED
created_at: "2026-03-09T00:00:00Z"
created_by: "eng-backend"
---

# Borrow a Book

**Primary Actor:** Library Member
**Goal:** A library member successfully borrows an available book and receives a due date.
**Brief:** The member presents their card at the circulation desk and requests a specific copy. The system verifies eligibility (valid card, no overdue loans) and book availability, then records the loan and issues a due-date slip. The use case ends when the member leaves the desk with the book and their due-date confirmation.

---

*Template: use-case-brief.template.md v1.0.0 | Detail level: BRIEFLY_DESCRIBED*
*Next step: Use uc-author to elaborate to BULLETED_OUTLINE (Steps 5-6) or ESSENTIAL_OUTLINE (Steps 7-10).*
