# {Review Type} Review: {Subject}

> **PS:** {PS_ID}
> **Exploration:** {ENTRY_ID}
> **Created:** {DATE}
> **Status:** REVIEW
> **Agent:** ps-reviewer
> **Type:** {code|design|architecture|security|documentation}

---

## Review Summary

### Overview

| Aspect | Value |
|--------|-------|
| Subject | {what_is_being_reviewed} |
| Scope | {files_or_components_reviewed} |
| Reviewer | ps-reviewer |
| Duration | {time_spent} |
| Overall Assessment | PASS / PASS_WITH_CONCERNS / NEEDS_WORK / FAIL |

### Quick Stats

| Severity | Count |
|----------|-------|
| Critical | {n} |
| High | {n} |
| Medium | {n} |
| Low | {n} |
| Info | {n} |
| **Total** | **{n}** |

### Executive Summary

{2-3_paragraph_summary_of_review_findings}

---

## Scope

### Files/Components Reviewed

| Path | Lines | Focus Areas |
|------|-------|-------------|
| {path_1} | {lines} | {focus} |
| {path_2} | {lines} | {focus} |
| {path_3} | {lines} | {focus} |

### Out of Scope

- {excluded_1}
- {excluded_2}

---

## Findings

### Critical Findings

<!-- Issues that MUST be fixed before merge/release -->

#### [C-001] {Finding Title}

| Attribute | Value |
|-----------|-------|
| **Severity** | CRITICAL |
| **Location** | `{file_path}:{line_number}` |
| **Category** | Security / Correctness / Data Loss |

**Description:**

{detailed_description_of_the_issue}

**Evidence:**

```{language}
{code_snippet_showing_issue}
```

**Recommendation:**

{how_to_fix}

```{language}
{corrected_code_example}
```

**References:**
- {CVE_or_standard_reference}
- {documentation_link}

---

### High Findings

<!-- Significant issues that should be fixed soon -->

#### [H-001] {Finding Title}

| Attribute | Value |
|-----------|-------|
| **Severity** | HIGH |
| **Location** | `{file_path}:{line_number}` |
| **Category** | Performance / Maintainability / Reliability |

**Description:**

{detailed_description}

**Recommendation:**

{how_to_fix}

---

### Medium Findings

<!-- Issues that should be addressed but are not blocking -->

#### [M-001] {Finding Title}

| Attribute | Value |
|-----------|-------|
| **Severity** | MEDIUM |
| **Location** | `{file_path}:{line_number}` |
| **Category** | Code Quality / Best Practice |

**Description:**

{detailed_description}

**Recommendation:**

{how_to_fix}

---

### Low Findings

<!-- Minor improvements, style issues, suggestions -->

#### [L-001] {Finding Title}

| Attribute | Value |
|-----------|-------|
| **Severity** | LOW |
| **Location** | `{file_path}:{line_number}` |
| **Category** | Style / Documentation / Nitpick |

**Description:**

{description}

**Recommendation:**

{suggestion}

---

### Informational

<!-- Observations, positive feedback, notes for future -->

#### [I-001] {Observation Title}

{description_of_observation}

---

## Design Principles Evaluation

<!-- For design/architecture reviews -->

| Principle | Status | Notes |
|-----------|--------|-------|
| Single Responsibility | PASS/PARTIAL/FAIL | {notes} |
| Open/Closed | PASS/PARTIAL/FAIL | {notes} |
| Liskov Substitution | PASS/PARTIAL/FAIL | {notes} |
| Interface Segregation | PASS/PARTIAL/FAIL | {notes} |
| Dependency Inversion | PASS/PARTIAL/FAIL | {notes} |

---

## Security Evaluation

<!-- For security reviews - OWASP Top 10 -->

| Category | Status | Findings |
|----------|--------|----------|
| A01: Broken Access Control | PASS/FAIL | {notes} |
| A02: Cryptographic Failures | PASS/FAIL | {notes} |
| A03: Injection | PASS/FAIL | {notes} |
| A04: Insecure Design | PASS/FAIL | {notes} |
| A05: Security Misconfiguration | PASS/FAIL | {notes} |
| A06: Vulnerable Components | PASS/FAIL | {notes} |
| A07: Auth Failures | PASS/FAIL | {notes} |
| A08: Data Integrity Failures | PASS/FAIL | {notes} |
| A09: Logging Failures | PASS/FAIL | {notes} |
| A10: SSRF | PASS/FAIL | {notes} |

---

## Aggregate Metrics

### By Category

| Category | Critical | High | Medium | Low | Info |
|----------|----------|------|--------|-----|------|
| Security | {n} | {n} | {n} | {n} | {n} |
| Performance | {n} | {n} | {n} | {n} | {n} |
| Maintainability | {n} | {n} | {n} | {n} | {n} |
| Correctness | {n} | {n} | {n} | {n} | {n} |
| Style | {n} | {n} | {n} | {n} | {n} |

### By File

| File | Critical | High | Medium | Low | Info |
|------|----------|------|--------|-----|------|
| {file_1} | {n} | {n} | {n} | {n} | {n} |
| {file_2} | {n} | {n} | {n} | {n} | {n} |

---

## Recommendations

| Priority | Action | Effort | Finding IDs |
|----------|--------|--------|-------------|
| IMMEDIATE | {action} | S/M/L | C-001, H-001 |
| SOON | {action} | S/M/L | H-002, M-001 |
| LATER | {action} | S/M/L | M-002, L-001 |

---

## Positive Observations

<!-- Things done well that should be continued -->

1. {positive_1}
2. {positive_2}
3. {positive_3}

---

## PS Integration

| Action | Command | Status |
|--------|---------|--------|
| Exploration Entry | `add-entry {PS_ID} "Review: {subject}"` | Done ({ENTRY_ID}) |
| Entry Type | `--type REVIEW` | Done |
| Artifact Link | `link-artifact {PS_ID} {ENTRY_ID} FILE "docs/reviews/..."` | {PENDING/Done} |

---

**Generated by:** ps-reviewer agent
**Template Version:** 1.0 (Phase 38.17)
**Standards:** OWASP Top 10 (2021), SOLID Principles, Google Code Review Guidelines
