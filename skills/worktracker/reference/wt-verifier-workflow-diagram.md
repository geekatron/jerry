# WT Verifier: L1 Technical Workflow Diagram

> ASCII workflow diagram showing the verification pipeline steps. Reference for understanding agent internal flow.

## L1: Technical Workflow (Software Engineer)

```
+---------------------------------------------------------+
| 1. INPUT VALIDATION                                      |
|---------------------------------------------------------|
| - Verify work item file exists                          |
| - Parse frontmatter via jerry ast frontmatter [/ast]    |
| - Extract status, type, id from frontmatter dict        |
| - Validate verification_scope parameter                 |
+---------------------------------------------------------+
                         |
+---------------------------------------------------------+
| 2. ACCEPTANCE CRITERIA EXTRACTION                        |
|---------------------------------------------------------|
| - Locate "## Acceptance Criteria" section               |
| - Extract all checkbox items (- [ ] and - [x])          |
| - Count total criteria and checked criteria             |
| - Calculate verification percentage                     |
+---------------------------------------------------------+
                         |
+---------------------------------------------------------+
| 3. EVIDENCE VALIDATION                                   |
|---------------------------------------------------------|
| - Locate "## Evidence" section                          |
| - Extract all markdown links [text](url)                |
| - Check for placeholder text (TODO, TBD, #)             |
| - Verify at least one real link exists                  |
+---------------------------------------------------------+
                         |
+---------------------------------------------------------+
| 4. CHILD ROLLUP (if parent_context provided)             |
|---------------------------------------------------------|
| - Glob for child work items (TASK-*.md in subdirectory) |
| - Extract each child's status via jerry ast frontmatter |
| - Verify all children fm["Status"] == "completed"       |
+---------------------------------------------------------+
                         |
+---------------------------------------------------------+
| 5. PASS/FAIL DETERMINATION                               |
|---------------------------------------------------------|
| WTI-002: criteria_percentage >= 0.80                     |
| WTI-006: evidence_links.length >= 1                      |
| WTI-003: all_children_done == true (if applicable)       |
|                                                          |
| passed = (criteria_pass AND evidence_pass AND            |
|           children_pass)                                 |
+---------------------------------------------------------+
                         |
+---------------------------------------------------------+
| 6. REPORT GENERATION (P-002 MANDATORY)                   |
|---------------------------------------------------------|
| - Create verification report file                       |
| - Include L0/L1/L2 sections                             |
| - Document all checks performed                         |
| - List blocking issues and recommendations              |
| - Return file path and pass/fail status                 |
+---------------------------------------------------------+
```
