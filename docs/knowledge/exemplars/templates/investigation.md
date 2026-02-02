# Investigation: {Symptom/Issue}

> **PS:** {PS_ID}
> **Exploration:** {ENTRY_ID}
> **Created:** {DATE}
> **Status:** INVESTIGATION
> **Agent:** ps-investigator
> **Severity:** CRITICAL | HIGH | MEDIUM | LOW

---

## Investigation Summary

### Overview

| Aspect | Value |
|--------|-------|
| Issue Reported | {brief_description} |
| First Detected | {date_time} |
| Environment | {production/staging/dev} |
| Impact | {users_affected_or_scope} |
| Duration | {how_long_issue_lasted} |
| Current Status | INVESTIGATING / ROOT_CAUSE_FOUND / RESOLVED |

### Executive Summary

{2-3_paragraph_summary_of_investigation_findings}

---

## Symptom Description

### What Happened

{detailed_description_of_the_observed_behavior}

### Expected Behavior

{what_should_have_happened}

### Timeline of Events

| Time | Event | Source |
|------|-------|--------|
| {time_1} | {event_1} | {log/user_report/monitoring} |
| {time_2} | {event_2} | {source} |
| {time_3} | {event_3} | {source} |

### Evidence Collected

| # | Evidence | Type | Location |
|---|----------|------|----------|
| 1 | {evidence_1} | Log / Screenshot / Metric | {path_or_link} |
| 2 | {evidence_2} | Log / Screenshot / Metric | {path_or_link} |

---

## 5 Whys Analysis

### Problem Statement

**Symptom:** {clear_statement_of_the_problem}

### Analysis

| Level | Question | Answer | Evidence |
|-------|----------|--------|----------|
| **Why 1** | Why did {symptom} occur? | {answer_1} | {supporting_evidence} |
| **Why 2** | Why did {answer_1}? | {answer_2} | {supporting_evidence} |
| **Why 3** | Why did {answer_2}? | {answer_3} | {supporting_evidence} |
| **Why 4** | Why did {answer_3}? | {answer_4} | {supporting_evidence} |
| **Why 5** | Why did {answer_4}? | **{root_cause}** | {supporting_evidence} |

---

## Ishikawa (Fishbone) Diagram

```
                                    ┌────────────────────────────────────────────┐
                                    │                                            │
    METHODS                         │                 MATERIALS                  │
    ───────                         │                 ─────────                  │
    │ {cause_1}                     │                     {cause_5} │            │
    │   └─ {sub_cause}              │                {cause_6} ─┘   │            │
    │ {cause_2}                     │                               │            │
    │   └─ {sub_cause}              │                               │            │
    ├───────────────────────────────┼───────────────────────────────┤            │
    │                               │                               │            │
    │                               │    ╔═══════════════════════╗  │            │
    │                               │    ║                       ║  │            │
    │                               │    ║    {PROBLEM}          ║──┼────────────┤
    │                               │    ║                       ║  │            │
    │                               │    ╚═══════════════════════╝  │            │
    │                               │                               │            │
    ├───────────────────────────────┼───────────────────────────────┤            │
    │ {cause_3}                     │                 {cause_7} │   │            │
    │   └─ {sub_cause}              │                     └─────┘   │            │
    │ {cause_4}                     │                 {cause_8}     │            │
    │   └─ {sub_cause}              │                               │            │
    │                               │                               │            │
    MACHINES                        │               MANPOWER        │            │
    ────────                        │               ────────        │            │
                                    │                               │            │
                                    └───────────────────────────────┘            │
                                                                                 │
    MEASUREMENTS                              MOTHER NATURE (Environment)        │
    ────────────                              ─────────────────────────          │
    │ {cause_9}                                   {cause_11} │                   │
    │   └─ {sub_cause}                       {cause_12} ─┘   │                   │
    │ {cause_10}                                             │                   │
    │                                                        ──────────────────┘
```

### Category Analysis

| Category | Contributing Factors | Likelihood |
|----------|---------------------|------------|
| **Methods** (Process) | {factors} | HIGH/MED/LOW |
| **Machines** (Equipment/Tools) | {factors} | HIGH/MED/LOW |
| **Materials** (Inputs) | {factors} | HIGH/MED/LOW |
| **Manpower** (People) | {factors} | HIGH/MED/LOW |
| **Measurements** (Data) | {factors} | HIGH/MED/LOW |
| **Mother Nature** (Environment) | {factors} | HIGH/MED/LOW |

---

## Failure Mode and Effects Analysis (FMEA)

| ID | Failure Mode | Effect | Cause | Severity (1-10) | Occurrence (1-10) | Detection (1-10) | RPN | Mitigation |
|----|--------------|--------|-------|-----------------|-------------------|------------------|-----|------------|
| FM1 | {mode_1} | {effect} | {cause} | {S} | {O} | {D} | {RPN} | {mitigation} |
| FM2 | {mode_2} | {effect} | {cause} | {S} | {O} | {D} | {RPN} | {mitigation} |
| FM3 | {mode_3} | {effect} | {cause} | {S} | {O} | {D} | {RPN} | {mitigation} |

**RPN Threshold:** Items with RPN > 100 require immediate action

---

## Root Cause Determination

### Primary Root Cause

**Root Cause:** {definitive_statement_of_root_cause}

**Category:** {which_6M_category}

**Evidence:**

{evidence_supporting_this_determination}

### Contributing Factors

| # | Factor | Category | Impact |
|---|--------|----------|--------|
| 1 | {factor_1} | {category} | HIGH/MED/LOW |
| 2 | {factor_2} | {category} | HIGH/MED/LOW |
| 3 | {factor_3} | {category} | HIGH/MED/LOW |

### Why This Is the Root Cause

{explanation_of_why_this_is_root_and_not_symptom}

---

## Corrective Actions

### Immediate Actions (Containment)

| # | Action | Owner | Status | Due |
|---|--------|-------|--------|-----|
| 1 | {immediate_fix} | {owner} | DONE/PENDING | {date} |
| 2 | {workaround} | {owner} | DONE/PENDING | {date} |

### Short-term Actions (Correction)

| # | Action | Owner | Status | Due |
|---|--------|-------|--------|-----|
| 1 | {fix_root_cause} | {owner} | PENDING | {date} |
| 2 | {related_fix} | {owner} | PENDING | {date} |

### Long-term Actions (Prevention)

| # | Action | Owner | Status | Due |
|---|--------|-------|--------|-----|
| 1 | {process_change} | {owner} | PENDING | {date} |
| 2 | {monitoring_add} | {owner} | PENDING | {date} |
| 3 | {documentation} | {owner} | PENDING | {date} |

---

## Verification

### How We Verified the Fix

{description_of_verification_steps}

### Test Results

| Test | Expected | Actual | Status |
|------|----------|--------|--------|
| {test_1} | {expected} | {actual} | PASS/FAIL |
| {test_2} | {expected} | {actual} | PASS/FAIL |

---

## Lessons Learned

### What Went Well

1. {positive_1}
2. {positive_2}

### What Could Be Improved

1. {improvement_1}
2. {improvement_2}

### Knowledge Items Generated

- **LES-XXX:** {lesson_description}
- **PAT-XXX:** {pattern_description}
- **ASM-XXX:** {assumption_description}

---

## PS Integration

| Action | Command | Status |
|--------|---------|--------|
| Exploration Entry | `add-entry {PS_ID} "Investigation: {symptom}"` | Done ({ENTRY_ID}) |
| Entry Type | `--type INVESTIGATION` | Done |
| Artifact Link | `link-artifact {PS_ID} {ENTRY_ID} FILE "docs/investigations/..."` | {PENDING/Done} |

---

**Generated by:** ps-investigator agent
**Template Version:** 1.0 (Phase 38.17)
**Methodology:** Toyota 5 Whys, Ishikawa Fishbone, NASA FMEA, Six Sigma DMAIC
