# WT Verifier: Output Schema and Usage Examples

> Verification result schema and scenario examples. Reference for orchestrators and downstream agents.

## Verification Report Schema

```yaml
verification_result:
  passed: boolean                    # Overall pass/fail
  score: float                       # 0.0-1.0 (AC percentage)
  work_item_id: string               # e.g., "EN-001"
  verification_scope: string         # full | acceptance_criteria | evidence
  timestamp: string                  # ISO 8601

  acceptance_criteria:
    total_criteria: integer
    checked_criteria: integer
    percentage: float
    passed: boolean                  # >= 0.80
    unchecked_items: array[string]   # List of unchecked criteria text

  evidence:
    total_links: integer
    valid_links: integer
    passed: boolean                  # >= 1
    evidence_items:
      - type: string                 # PR, test, doc, etc.
        link: string
        status: string               # valid | placeholder | broken

  child_rollup:
    applicable: boolean              # true if parent_context provided
    total_children: integer
    completed_children: integer
    passed: boolean                  # all completed
    incomplete_children: array[string]  # List of incomplete child IDs

  blocking_issues: array[string]     # Issues preventing DONE transition
  recommendations: array[string]     # Suggested actions
```

## Usage Examples

### Example 1: Full Verification -- All Checks Passing

```
User: "Is EN-003 ready to be marked as done?"

Task Invocation:
- work_item_path: "projects/PROJ-009/.../EN-003-example.md"
- verification_scope: "full"
- parent_context: "projects/PROJ-009/.../FEAT-002-claude-md-optimization.md"
- strict_mode: false

Expected Output:
- verification-report.md with Status: PASSED
- Score: 1.0 (100%)
- Recommendations: "EN-003 can be transitioned to DONE status"
```

### Example 2: Verification Failure -- Insufficient Acceptance Criteria

```
User: "Verify EN-005 is complete"

Task Invocation:
- work_item_path: "projects/PROJ-009/.../EN-005-example.md"
- verification_scope: "full"

Expected Output:
- verification-report.md with Status: FAILED
- Score: 0.65 (65% - below 80% threshold)
- Blocking Issues:
  - "WTI-002 VIOLATION: Only 65% of acceptance criteria verified (13/20 checked)"
- Recommendations:
  - "Complete remaining 7 acceptance criteria before marking EN-005 as DONE"
  - "Update evidence section with proof of completion for each criterion"
```

### Example 3: Evidence Missing

```
User: "Can we close EN-007?"

Task Invocation:
- work_item_path: "projects/PROJ-009/.../EN-007-example.md"
- verification_scope: "evidence"

Expected Output:
- verification-report.md with Status: FAILED
- Blocking Issues:
  - "WTI-006 VIOLATION: Evidence section is empty (no verifiable links)"
- Recommendations:
  - "Add links to PRs, commits, test results, or documentation"
  - "Evidence must be permanent and verifiable (not placeholder text)"
```

### Example 4: Child Rollup Failure

```
User: "Is FEAT-002 complete?"

Task Invocation:
- work_item_path: "projects/PROJ-009/.../FEAT-002-claude-md-optimization.md"
- verification_scope: "full"

Expected Output:
- verification-report.md with Status: FAILED
- Blocking Issues:
  - "WTI-003 VIOLATION: 3 child enablers are not complete (EN-002, EN-004, EN-006)"
- Recommendations:
  - "Complete EN-002, EN-004, EN-006 before marking FEAT-002 as DONE"
  - "Verify each child enabler has 80%+ acceptance criteria and evidence"
```

### Example 5: Strict Mode (Warnings Block Completion)

```
User: "Verify EN-009 in strict mode"

Task Invocation:
- work_item_path: "projects/PROJ-009/.../EN-009-example.md"
- verification_scope: "full"
- strict_mode: true

Expected Output:
- verification-report.md with Status: FAILED
- Warnings (elevated to errors in strict mode):
  - "Evidence section contains placeholder link: 'TODO: Add PR link'"
- Blocking Issues:
  - "Strict mode enabled: Warnings treated as errors"
- Recommendations:
  - "Replace placeholder evidence links with actual URLs"
  - "Disable strict_mode if warnings should not block completion"
```
