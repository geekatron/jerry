# Heuristic Evaluation: Jerry CI Pipeline (29-Job Status Checks)

## Document Sections
| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Top findings, severity distribution, DX assessment |
| [Evaluation Context](#evaluation-context) | Product, target users, interface scope |
| [Findings by Heuristic](#findings-by-heuristic) | All 10 heuristics evaluated against the PR status checks |
| [Ranked Findings Summary](#ranked-findings-summary) | All findings ranked by severity |
| [Remediation Roadmap](#remediation-roadmap) | Implementation priority by effort |
| [Strategic Implications](#strategic-implications) | DX maturity, signal-to-noise ratio, organizational patterns |
| [Synthesis Judgments Summary](#synthesis-judgments-summary) | AI evaluation decision points |

---

## Executive Summary

**Top Findings:**
1. **F-001 (Severity 3):** Visual information overload from 29 status checks creates significant cognitive burden; developers must scan entire list to understand failure scope instead of seeing grouped summary
2. **F-002 (Severity 3):** Inconsistent naming conventions ("Test pip" vs "Test uv", "Frontmatter Validation" vs "Frontmatter-Validation") degrades pattern recognition and requires label-by-label cognitive load
3. **F-003 (Severity 2):** Matrix job expansion unintuitive; developer cannot predict job count without reading CI source — 10 semantic "tests" expand to 16 actual jobs (8 pip + 8 uv variants)
4. **F-004 (Severity 2):** Governance jobs ("HARD Rule Ceiling", "Changelog Entry") lack contextual help; developer sees the name but not the rationale or recovery guidance

**Severity Distribution:**
- Severity 4: 0 (no usability catastrophes blocking task completion)
- Severity 3: 2 findings (major issues impairing efficiency)
- Severity 2: 3 findings (minor usability problems)
- Severity 1: 1 finding (cosmetic)
- Severity 0: 0 findings

**Overall Usability Assessment:**
The CI pipeline is functionally complete (developers can see all check results) but operationally inefficient. The primary usability problem is **information architecture**: 29 discrete status items are presented as an undifferentiated list, requiring developers to manually parse and group information that should be pre-grouped by the interface. The pipeline prioritizes comprehensiveness (every variant and governance check visible) over usability (signal-to-noise ratio, progressive disclosure, mental model alignment).

**Heuristic Coverage:** All 10 Nielsen heuristics evaluated across the GitHub PR status checks interface for the 29-job CI pipeline.

---

## Evaluation Context

**Product:** Jerry Framework CI/CD Pipeline (GitHub Actions)
**Target Users:** Developers pushing code to the Jerry repository; users reading PR status checks within GitHub PR interface
**Screens Evaluated:** GitHub PR Checks interface showing 29 status checks (as displayed on any PR to `main` branch)
**Input Modality:** Screenshot-input mode (no GitHub API; visual inspection of PR interface)
**Evaluation Scope:** Screen-level evaluation of the status checks display
**Evaluation Type:** Developer experience (DX) heuristic evaluation using Nielsen's 10 usability heuristics

**Degraded Mode Disclosure:** This evaluation was produced without access to the GitHub API or interactive GitHub UI. The evaluation is based on the `.github/workflows/ci.yml` file which enumerates the 29 jobs that produce status checks. The actual visual layout and interaction patterns are inferred from standard GitHub PR status display behavior. Some contextual UI patterns (collapse groups, custom status checks) may not be fully captured.

---

## Findings by Heuristic

### H1: Visibility of System Status

**Finding F-001: Information Overload from Undifferentiated 29-Item Status List (Severity 3)**

- **Heuristic:** H1 -- Visibility of System Status
- **Severity:** 3 (Major usability problem)
- **Screen/Flow:** GitHub PR Checks interface, Status Checks section
- **Evidence:** The CI workflow enumerates 29 distinct jobs that each produce a GitHub status check:
  1. Lint & Format
  2. Type Check
  3. Security Scan
  4. Lockfile Freshness
  5. Plugin Validation
  6. Template Validation
  7. Frontmatter Validation
  8. License Header Check
  9. CLI Integration Tests
  10-17. Test pip (8 variants: 3 Python versions × 3 OSes - 6 excluded)
  18-25. Test uv (8 variants: 3 Python versions × 3 OSes - 6 excluded)
  26. Coverage Report
  27. Version Sync Check
  28. HARD Rule Ceiling
  29. Changelog Entry
  30. CI Success

  When a developer clicks "Details" on a single failed job (e.g., "Test uv (Python 3.13, macos-latest)"), they see only that job's failure. To understand whether the failure is an OS-specific issue, Python-version-specific issue, or a general problem affecting all test runs, developers must: (a) close that job detail, (b) scroll the full PR status list, (c) individually click 15 other test jobs to see their results. The interface provides no grouped summary ("5/16 test jobs failed") visible at a glance.

- **Remediation:** Group related jobs under collapsible status check categories. GitHub Actions supports custom status checks and workflow artifact naming that can signal grouping to external tools. Alternatively, implement a custom workflow summary step that post-processes the workflow completion and writes a summary comment listing: "Quality gates: 6 passed. Test suite: 16 variants (9 passed, 7 failed). Coverage: OK. Governance: All passed." This summary should be visible BEFORE the developer sees the 29-item list.

- **Effort:** Medium (requires custom summary step or GitHub workflow enhancement; no change to individual job logic)

---

### H2: Match Between System and Real World

**Finding F-002: Inconsistent Naming Conventions Create Non-Obvious Distinctions (Severity 3)**

- **Heuristic:** H2 -- Match Between System and Real World
- **Severity:** 3 (Major usability problem)
- **Screen/Flow:** GitHub PR Checks interface, job names column
- **Evidence:**
  - "Lint & Format" (inconsistent: uses ampersand and title case)
  - "Type Check" (title case, no verb)
  - "Security Scan" (title case)
  - "CLI Integration Tests" (title case, includes domain term "CLI")
  - "Test pip" (lowercase verb form)
  - "Test uv" (lowercase verb form)
  - "Frontmatter Validation" (title case, hyphenated domain term but displayed without hyphen)
  - "License Header Check" (title case, descriptive but verbose)
  - "HARD Rule Ceiling" (ALL CAPS acronym, non-obvious meaning)
  - "Changelog Entry" (imperative-looking but actually a validation check)

  A developer new to the project cannot predict which jobs fall into which category without reading the CI source. The naming convention appears arbitrary: some jobs include the action (Lint, Check, Scan, Validate, Test) and some do not. Some include context (pip/uv, Python version) and some do not. The distinction between "Validation" jobs (Plugin, Template, Frontmatter, License) is not semantically obvious — they do not share a common verb or structural pattern.

  Critical semantic issue: "HARD Rule Ceiling" and "Changelog Entry" are governance/process jobs, but their names do not signal this. A developer seeing these names has no idea what they validate or why they are required without clicking the job detail or reading the CI source.

- **Remediation:**
  1. **Naming convention:** Establish and enforce: `{Domain Prefix} — {Action} {Target}` (e.g., `code-quality — lint`, `test — unit`, `governance — changelog`).
  2. **Semantic grouping:** Use consistent prefixes for related jobs:
     - `code-quality — {task}` (lint, type-check, security-scan)
     - `validation — {target}` (plugin, template, frontmatter, headers)
     - `test — {installer}-py{version}-{os}` (test-pip-py3.14-ubuntu, test-uv-py3.14-macos)
     - `governance — {check}` (hard-rule-ceiling, changelog)
     - `reports — {type}` (coverage, version-sync)
  3. **Tooltips/descriptions:** Add a `.jobs.<job_id>.environment.DESCRIPTION` field in the CI to display brief explanations in the GitHub API and logs (though GitHub UI does not natively show these in the status checks display).

- **Effort:** Medium (rename 29 jobs, establish naming standard in CLAUDE.md, update CI source; no logic changes)

---

### H3: User Control and Freedom

**Finding F-005: Limited Ability to Filter or Dismiss Non-Critical Failures (Severity 2)**

- **Heuristic:** H3 -- User Control and Freedom
- **Severity:** 2 (Minor usability problem)
- **Screen/Flow:** GitHub PR Checks interface during CI troubleshooting
- **Evidence:** When a developer has a legitimate reason to skip certain checks (e.g., a known intermittent network failure in a non-critical job, or a skip-coverage exemption already applied to the code), they must re-run ALL 29 jobs from scratch. GitHub Actions does not natively support per-job skip markers in workflow files that affect the PR status display. The CI workflow includes some skip logic (`[skip-coverage]`, bot PR exemptions for changelog) but the developer cannot interact with these controls from the PR interface — they must modify commit messages or re-trigger from GitHub Actions web UI.

  Additionally, if a developer wants to re-run only the 8 test jobs (not the full 29), GitHub UI requires navigating to Actions → Workflow Run → Re-run Failed Jobs or Re-run All, not a per-check granular control.

- **Remediation:**
  1. **Short-term:** Document skip markers clearly in CONTRIBUTING.md. Add a workflow summary step that explains available skip options: `[skip-coverage]`, `[skip-changelog]`, and describe how to use them.
  2. **Medium-term:** Implement selective job re-running via GitHub workflow_dispatch inputs (manual trigger UI allows selecting which job categories to run).
  3. **Long-term:** Consider GitHub Actions reusable workflows or custom status checks API to group jobs and allow group-level control.

- **Effort:** Low (documentation only for short-term)

---

### H4: Consistency and Standards

**Finding F-003: Matrix Job Expansion Violates Consistency of Visible Checks (Severity 2)**

- **Heuristic:** H4 -- Consistency and Standards
- **Severity:** 2 (Minor usability problem)
- **Screen/Flow:** GitHub PR Checks interface, test jobs section
- **Evidence:** The developer's mental model predicts N status checks based on reading the workflow summary. However, the matrix strategy (`python-version: ["3.11", "3.12", "3.13", "3.14"]` and `os: [ubuntu-latest, windows-latest, macos-latest]`) expands 2 semantic jobs (`test-pip`, `test-uv`) into 16 concrete GitHub status checks (8 pip variants + 8 uv variants, after matrix exclusions).

  When a developer reads the CI workflow name ("Test pip", "Test uv"), they expect 2-3 status checks. When they open the PR, they see 16. This gap between expectation and reality is not explained in the status check interface — developers must infer the matrix expansion logic independently.

  **Consistency violation:** Other jobs do NOT use matrices (Lint, Type Check, Security, etc.), so the pattern is inconsistent. The principle of least surprise is violated: developers expect all jobs to behave the same way (single status check per job name), but test jobs violate this expectation.

- **Remediation:**
  1. **Short-term:** Update workflow job names to include the matrix variables in the job output name field: `name: Test pip (Python ${{ matrix.python-version }}, ${{ matrix.os }})` (already implemented in the CI, so status check names are correct). However, ensure this pattern is applied consistently across all matrix jobs.
  2. **Medium-term:** Add a custom job summary step in the test jobs that outputs a matrix completion table to the PR comment:
     ```
     | Python Version | Ubuntu | macOS | Windows |
     |---|---|---|---|
     | 3.11 | ✓ | — | — |
     | 3.12 | ✓ | — | — |
     | 3.13 | ✓ | ✓ | ✓ |
     | 3.14 | ✓ | ✓ | ✓ |
     ```
     This provides a visual summary at a glance instead of requiring the developer to scan 16 individual status checks.

- **Effort:** Low (the naming is already correct; add a summary table via custom step)

---

### H5: Error Prevention

**Finding F-004: Governance Job Failures Provide No Context for Recovery (Severity 2)**

- **Heuristic:** H5 -- Error Prevention
- **Severity:** 2 (Minor usability problem)
- **Screen/Flow:** GitHub PR Checks interface, when "HARD Rule Ceiling" or "Changelog Entry" fails
- **Evidence:** The workflow includes two governance checks that are not obvious to developers unfamiliar with the Jerry framework:
  - **HARD Rule Ceiling:** This job counts HARD rules in `quality-enforcement.md` and fails if the count exceeds 25. A developer who has not read the framework documentation will see this job fail with no clear explanation of why it failed or how to fix it.
  - **Changelog Entry:** This job validates that a CHANGELOG.md entry exists in the PR. It includes skip logic for bot PRs and `[skip-changelog]` markers, but a developer encountering the failure will not see this context in the status check itself.

  Both jobs have recovery paths documented in the CI script itself (comments in the YAML), but developers interact with the GitHub PR interface, not the source file. The status check display shows only: "HARD Rule Ceiling — Failed" with no guidance on next steps.

- **Remediation:**
  1. **Error message clarity:** Modify both jobs to output explicit, actionable error messages that include: (a) what was checked, (b) why it failed, (c) how to fix it, (d) where to find full documentation.
     - Example HARD Rule Ceiling failure: "HARD Rule Ceiling check failed: Found 26 rules, maximum is 25. See `.context/rules/quality-enforcement.md` for the HARD Rule Index. To add a new rule, file an ADR with C4 criticality and follow the exception mechanism: [link to ADR-EPIC002-001]."
     - Example Changelog failure: "CHANGELOG.md was not updated. Every PR must include a changelog entry in the [Unreleased] section (Keep a Changelog format). To skip this check, add [skip-changelog] to your PR title. See CONTRIBUTING.md for details."
  2. **Workflow summary step:** Add a final job that posts a summary comment to the PR with links to relevant documentation if governance jobs fail.

- **Effort:** Low (update error messages in CI script; add documentation links)

---

### H6: Recognition Rather Than Recall

**Finding F-006: Governance Job Names Require External Knowledge (Severity 2)**

- **Heuristic:** H6 -- Recognition Rather Than Recall
- **Severity:** 2 (Minor usability problem)
- **Screen/Flow:** GitHub PR Checks interface
- **Evidence:** Job names like "HARD Rule Ceiling", "Changelog Entry", "Plugin Validation" assume the developer knows what these terms mean in the Jerry context. A developer unfamiliar with the framework will see these names and have no recognition of their purpose without reading documentation or the CI source.

  Contrast with self-explanatory names: "Lint & Format" (obvious intent), "Type Check" (obvious intent), "Security Scan" (obvious intent). These names rely on common developer vocabulary and do not require external knowledge to understand their purpose.

  The governance jobs require recall of framework-specific terminology and context, placing cognitive burden on developers who are new to the project or returning after time away.

- **Remediation:**
  1. **Self-documenting names:** Change "HARD Rule Ceiling" to "HARD Rule Count Limit" or "Framework Rule Count Validation" to make the purpose more obvious.
  2. **Inline documentation:** Add a custom workflow step that posts a PR comment on first run (visible to all developers) explaining the governance checks:
     ```markdown
     ## CI Checks Explained
     **Governance Checks:**
     - **Framework Rule Count Validation:** Ensures the Jerry governance rule count does not exceed the maximum (currently 25/25). See: [docs/governance/JERRY_CONSTITUTION.md](link)
     - **Changelog Requirement:** Every PR must include a changelog entry. Exemptions: Dependabot PRs, bot commits, PRs with [skip-changelog] marker.
     - **Version Sync:** Validates that version numbers are consistent across configuration files.

     **Test Jobs:** Run on 3 OSes (Ubuntu, macOS, Windows) and 4 Python versions (3.11-3.14) for both pip and uv installers.
     ```

- **Effort:** Low (update job names slightly, add one-time PR comment with documentation)

---

### H7: Flexibility and Efficiency of Use

**Finding F-007: No Shortcuts for Advanced Users to See Only Failed Jobs (Severity 1)**

- **Heuristic:** H7 -- Flexibility and Efficiency of Use
- **Severity:** 1 (Cosmetic problem only)
- **Screen/Flow:** GitHub PR Checks interface, when scanning for failures
- **Evidence:** GitHub's native PR status display shows all 29 checks, even if 28 pass and 1 fails. Advanced users (experienced developers who want to quickly identify failures) cannot filter to show "failed checks only" — they must scroll the entire 29-item list. GitHub does not provide native filtering in the PR status checks display (though the GitHub API supports querying by conclusion status).

  Note: This is a GitHub platform limitation, not a Jerry CI pipeline limitation. However, it affects the developer experience of the CI pipeline.

- **Remediation:**
  1. **Workaround:** Use GitHub's native "Show more details" UI to collapse sections (if GitHub Groups jobs, which it does not by default for matrix jobs).
  2. **Long-term:** Consider using GitHub's Status Check Grouping feature (GitHub Enterprise feature, not available on public repos) or external PR automation tools that aggregate status checks.

- **Effort:** High (requires GitHub platform feature; outside scope of CI pipeline control)

---

### H8: Aesthetic and Minimalist Design

**Finding F-001 (restate): 29 Status Checks Produce Excessive Visual Noise (Severity 3)**

- **Heuristic:** H8 -- Aesthetic and Minimalist Design
- **Severity:** 3 (Major usability problem; combined signal-to-noise and cognitive load impact)
- **Screen/Flow:** GitHub PR Checks interface, initial view
- **Evidence:** The PR status display shows 29 discrete status checks without grouping or hierarchy. A developer opening a PR sees a vertically scrollable list of 29 items, each requiring individual attention. The signal-to-noise ratio is poor: developers care about "Did the test suite pass?" (1 signal), but the interface presents "Did each of the 16 matrix variants pass?" (16 items for 1 conceptual signal).

  The list is visually monotonous: all items have similar visual weight (green checkmark or red X), making it hard to distinguish critical checks from informational checks. A developer does not know which checks are blockers (must pass before merge) and which are informational (nice-to-know but not blockers).

  Visual clutter is compounded by:
  - Inconsistent capitalization (Lint & Format vs Test pip vs HARD Rule Ceiling)
  - Inconsistent naming styles (action + target vs target + action vs acronym)
  - No visual grouping or hierarchy
  - No progressive disclosure (all details visible on initial view; developer must click each to understand context)

- **Remediation:**
  1. **Group jobs by category:** Implement a GitHub workflow summary job that groups checks into categories and posts a summary comment:
     ```markdown
     ## CI Status Summary
     ✓ **Code Quality** (4/4)
       - Lint & Format ✓
       - Type Check ✓
       - Security Scan ✓
       - HARD Rule Ceiling ✓

     ✓ **Validation** (4/4)
       - Plugin Validation ✓
       - Template Validation ✓
       - Frontmatter Validation ✓
       - License Header Check ✓

     ✓ **Tests: pip** (4/4 variants)
       - Python 3.11 (ubuntu) ✓
       - Python 3.12 (ubuntu) ✓
       - Python 3.13 (ubuntu, macos, windows) ✓
       - Python 3.14 (ubuntu, macos, windows) ✓

     ✓ **Tests: uv** (4/4 variants)
       [same structure]

     ✓ **Governance & Reports** (3/3)
       - Coverage Report ✓
       - Version Sync Check ✓
       - Changelog Entry ✓
     ```
     This groups the 29 items into 5 semantic categories that match the developer's mental model.

  2. **Minimize repetition:** Use collapsible sections in the summary comment so developers can expand only sections they care about. The default view shows only the category summary (✓ Code Quality, ✓ Tests, etc.), and developers can expand to see details.

  3. **Use visual indicators:** Employ emoji or color-coding in the summary to distinguish check categories and status at a glance.

- **Effort:** Medium (add a custom workflow summary job that generates the grouped summary and posts it as a PR comment)

---

### H9: Help Users Recognize, Diagnose, and Recover from Errors

**Finding F-004 (restate): Governance Checks Lack Recovery Guidance**

- **Heuristic:** H9 -- Help Users Recognize, Diagnose, and Recover from Errors
- **Severity:** 2 (Minor usability problem; already identified in H5, restate here for H9)
- **Screen/Flow:** GitHub PR status checks when governance job fails
- **Evidence:** When a governance job fails, the status check display shows only the job name and failure indication. A developer encountering a "HARD Rule Ceiling" failure has:
  1. No error message explaining what the rule ceiling is
  2. No link to documentation
  3. No recovery steps
  4. Must navigate to GitHub Actions web UI or CI source to understand the failure

- **Remediation:** See F-004 remediation (error message clarity, documentation links in workflow summary)

- **Effort:** Low

---

### H10: Help and Documentation

**Finding F-008: CI Pipeline Design and Job Rationale Not Documented in Developer-Accessible Location (Severity 2)**

- **Heuristic:** H10 -- Help and Documentation
- **Severity:** 2 (Minor usability problem)
- **Screen/Flow:** Developer trying to understand why certain checks exist or what they validate
- **Evidence:** The CI pipeline includes 29 jobs with specific purposes (documented in inline YAML comments), but this documentation is not accessible to developers reading PR status checks. For example:
  - "CLI Integration Tests" has an EN-006 ADR reference in the YAML comments, but developers cannot see this from the PR interface.
  - "Frontmatter Validation" includes a reference to STORY-025 in comments, but developers do not see this context.
  - The entire plugin validation section (EN-005, EN-007) has detailed documentation in YAML but zero documentation visible in the PR status interface.

  The `.github/workflows/ci.yml` file is the SSOT for CI documentation, but it is not easily discoverable from the PR interface. Developers must navigate to the CI source file to understand the pipeline design.

- **Remediation:**
  1. **Create CONTRIBUTING.md documentation:** Add a section "Understanding CI Checks" that explains each job category, what it validates, and why.
  2. **Link from PR summary:** Include a one-time PR comment (first run) with a link to CONTRIBUTING.md → CI Checks section.
  3. **Update CLAUDE.md:** Add a brief section under "Navigation" or "Quick Reference" explaining the CI pipeline structure and where developers can find detailed CI documentation.
  4. **Add per-job descriptions in workflow:** While GitHub does not display job descriptions in the PR status UI, adding descriptions to each job in the YAML enables CI documentation generators to create reference docs automatically.

- **Effort:** Low (documentation only; no code changes)

---

## Ranked Findings Summary

| Finding | Heuristic | Severity | Affected Area | Issue |
|---------|-----------|----------|---------------|-------|
| F-001 | H1, H8 | 3 | GitHub PR Checks display | 29 undifferentiated status checks create cognitive overload; information not grouped by category |
| F-002 | H2 | 3 | Job naming conventions | Inconsistent naming (Lint & Format vs Test pip vs HARD Rule Ceiling) obscures semantic categories |
| F-003 | H4 | 2 | Matrix job expansion | Matrix expansion from 2 semantic jobs to 16 concrete checks violates consistency expectation; no visual summary |
| F-004 | H5, H9 | 2 | Governance job failures | HARD Rule Ceiling and Changelog failures provide no contextual help or recovery guidance |
| F-005 | H3 | 2 | Job re-running control | Limited granular control over which jobs to re-run; developers must re-trigger all 29 or none |
| F-006 | H6 | 2 | Governance job clarity | Job names like "HARD Rule Ceiling" require external knowledge; not self-documenting |
| F-007 | H7 | 1 | Filter shortcuts | GitHub platform limitation: no native way to filter to failed checks only |
| F-008 | H10 | 2 | CI documentation | Pipeline design and job rationale documented in YAML but not accessible from PR interface |

**Total Findings:** 8
**Severity 3:** 2 findings (major usability problems)
**Severity 2:** 5 findings (minor usability problems)
**Severity 1:** 1 finding (cosmetic)

---

## Remediation Roadmap

### High Priority (Severity 3) — Should fix before next release

| Finding | Title | Remediation | Effort | Est. Time |
|---------|-------|-----------|--------|-----------|
| F-001, F-008 | Information overload + documentation gap | Add custom GitHub Actions job that post-processes CI completion and posts a grouped summary comment to PRs. Summary should categorize 29 jobs into 5-6 semantic groups with collapsible details. | Medium | 4-6 hours |
| F-002 | Inconsistent naming conventions | Establish and enforce naming standard: `{domain-prefix} — {action} {target}`. Rename 29 jobs to follow pattern. Document in `.context/rules/` or CLAUDE.md. | Medium | 3-4 hours |

### Medium Priority (Severity 2) — Should fix in next release

| Finding | Title | Remediation | Effort | Est. Time |
|---------|-------|-----------|--------|-----------|
| F-004, F-006 | Governance job error clarity | Update "HARD Rule Ceiling" → "Framework Rule Count Validation". Update error messages in CI script to include actionable recovery steps and links to docs. | Low | 1-2 hours |
| F-003 | Matrix expansion visibility | Add custom job summary step that outputs a matrix completion table to PR comment (Python version × OS grid showing which tests passed). | Low | 2-3 hours |
| F-005 | Job re-running control | Document skip markers in CONTRIBUTING.md. Add workflow_dispatch inputs for selective job re-running (future enhancement). | Low | 1 hour (documentation) |
| F-008 | CI documentation | Create CONTRIBUTING.md section "Understanding CI Checks" with job-by-job explanations. Link from first-run PR comment. | Low | 2-3 hours |

### Low Priority (Severity 1) — Fix if time allows

| Finding | Title | Remediation | Effort | Est. Time |
|---------|-------|-----------|--------|-----------|
| F-007 | Filter shortcuts | Investigate GitHub Status Check Grouping (GHE only) or external PR automation tools. Document current limitations in CONTRIBUTING.md. | High | Future |

### Implementation Sequence

1. **Phase 1 (Week 1):** F-001, F-002 — Create grouped summary comment job + rename jobs for consistency
2. **Phase 2 (Week 2):** F-004, F-006, F-008 — Improve error messages, documentation, and CI clarity
3. **Phase 3 (Week 3):** F-003, F-005 — Matrix summary table, skip marker documentation

---

## Strategic Implications

### DX Maturity Assessment

The Jerry CI pipeline reflects a **mature but under-communicated governance framework**. The pipeline logic is sound:
- Comprehensive coverage (29 checks across multiple dimensions)
- Governance enforcement (HARD rules, changelog, version sync)
- Multi-platform testing (pip/uv, 3 OSes, 4 Python versions)

However, the **presentation** (29 undifferentiated status checks on GitHub PR interface) does not match the **developer's mental model** (group checks by category). This creates friction: developers must manually interpret and group information that the CI system has implicitly categorized.

### Signal-to-Noise Ratio

**Current:** 29 discrete checks for ~10-12 semantic concerns
- Code quality: 4 checks (Lint, Type, Security, HARD Rule)
- Validation: 4 checks (Plugin, Template, Frontmatter, License)
- Tests: 16 checks (representing 2 semantic dimensions: installer choice and platform coverage)
- Governance: 2 checks (Changelog, Version Sync)
- Reports: 1 check (Coverage)

**Ideal:** 5-6 grouped categories visible at first glance, expandable to granular details

**Root Cause:** GitHub's native status checks interface does not support grouping or hierarchical display. The CI system must work around this platform limitation by generating its own summary comment.

### Organizational Pattern

The pipeline structure reflects the Jerry framework's governance emphasis:
- The highest number of checks (16) are for test coverage (ensures compatibility across Python versions and installers)
- Governance checks (4) are weighted equally with code quality checks (4), signaling that framework governance is as important as code quality
- Validation checks (4) suggest framework structure and patterns are enforced at CI time

This is appropriate for a framework project where consistency and governance are critical. However, developers need help understanding this emphasis from the PR interface alone.

### Recommended Approach

**Short-term (immediate):** Post a summary comment on every PR that groups the 29 checks into 5-6 categories. This is a low-code workaround that leverages GitHub's native PR comment feature.

**Medium-term (1-2 releases):** Rename jobs for consistency and improve error messages. Provide clear documentation of the CI structure and each check's purpose.

**Long-term (future versions):** Investigate GitHub Actions features for check grouping or consider custom status check APIs if GitHub introduces them.

---

## Synthesis Judgments Summary

### AI Evaluation Decision Points

1. **Severity 3 rating for F-001 (information overload):** The 29-check display creates measurable friction in developer workflow (requires manual scanning and grouping). This rises to "major" severity because it directly impacts efficiency on every PR, though it does not prevent task completion. A developer can still see all results; they just must work harder to interpret them. Rating: justified.

2. **H4 Consistency finding (F-003):** Matrix job expansion violates the principle of least surprise. However, GitHub UI already displays matrix-expanded job names correctly (e.g., "Test pip (Python 3.14, ubuntu-latest)"). The consistency violation is subtle — it's about expectation-setting in the mental model, not a functional usability defect. Severity 2 is appropriate (minor problem, not major).

3. **H2 Naming convention finding (F-002):** The inconsistency in job naming ("Lint & Format" vs "Test pip" vs "HARD Rule Ceiling") is a genuine usability problem for developers new to the project, but experienced developers quickly internalize the naming. Severity 3 is justified because it impacts cognitive load on every PR review and onboarding experience. The naming patterns are not self-documenting.

4. **Governance job findings (F-004, F-006):** These are intentionally designed to be invisible to most developers (checks pass silently unless you violate governance). When they fail, the lack of context is a usability problem, but the failure rate is expected to be low in normal operation. Severity 2 is appropriate — the problem only surfaces when governance is violated, which is a design choice (fail loud when rules are broken).

5. **H10 documentation finding (F-008):** The CI documentation exists (in YAML comments and ADR references) but is not discoverable from the developer's primary interaction point (PR status interface). This is a documentation architecture problem, not a pipeline logic problem. Severity 2 is appropriate — developers can find documentation if they search, but it's not readily accessible.

### Single-Evaluator Limitation Note

This evaluation was conducted by a single AI evaluator (ux-heuristic-evaluator, Haiku model). Nielsen's research suggests individual evaluators typically find ~35% of usability problems. To increase coverage, recommend:

1. **Supplement with user interviews:** Ask 3-5 developers (Jerry contributors or users) to review a PR and describe their CI experience. Record which checks they notice, which they ignore, and where they get stuck.
2. **A/B test the grouped summary:** Implement the grouped summary comment and measure whether developers spend less time scanning the status checks (via informal feedback or analytics on PR interaction patterns).
3. **Heuristic review by domain expert:** Invite a GitHub Power User or DevOps engineer to review the CI pipeline from an operational perspective (not just developer UX).

---

## Handoff Data

For downstream sub-skills (Behavior Design, HEART Metrics):

| Finding | Heuristic | Severity | Task Success Impact | Candidate HEART Category |
|---------|-----------|----------|---------------------|--------------------------|
| F-001 | H1, H8 | 3 | Task completion time increases (developer must manually parse 29 checks to identify failures) | Engagement (effort to find information) |
| F-002 | H2 | 3 | Task completion accuracy decreases (developer may miss or misinterpret checks due to unclear naming) | Task success (correctness of interpretation) |
| F-003 | H4 | 2 | Task completion time increases slightly (developer surprised by 16 checks instead of expected 2) | Engagement (friction in expectations) |
| F-004 | H5, H9 | 2 | Task completion fails for first-time users (governance failure with no recovery guidance) | Task success (blockers without recovery paths) |
| F-005 | H3 | 2 | Task completion time increases (developer cannot selectively re-run jobs; must re-trigger all or navigate to Actions UI) | Adoption (workflow friction) |
| F-006 | H6 | 2 | Onboarding time increases (new developers cannot recognize governance check purposes without external knowledge) | Adoption (learning curve) |
| F-008 | H10 | 2 | Onboarding time increases (CI structure and rationale not documented in easily discoverable location) | Adoption (documentation accessibility) |

**HEART Focus:** Engagement (information discovery friction) and Adoption (onboarding and learning curve) are the primary opportunity areas. The grouped summary comment and improved documentation should reduce both metrics measurably.

---

## Related Documents

- **CI Pipeline Source:** `.github/workflows/ci.yml` (this evaluation's input artifact)
- **Framework Documentation:** `.context/rules/quality-enforcement.md` (EN-001, H-13 references in CI)
- **Contributing Guide:** CONTRIBUTING.md (should document CI expectations and skip markers)
- **ADR Reference:** PROJ-001-plugin-cleanup `decisions/ADR-CI-001-cicd-pipeline.md` (CI design rationale)

---

*Evaluation Version: 1.0.0*
*Evaluator: ux-heuristic-evaluator (Haiku model, screenshot-input mode)*
*Evaluation Date: 2026-04-13*
*Engagement: CI/DX Heuristic Review (informal)*
*Scope: GitHub PR Checks interface displaying 29 status checks from `.github/workflows/ci.yml`*
*Nielsen Heuristics Evaluated: All 10 (H1-H10)*
*Single-Evaluator Limitation: Individual evaluators find ~35% of usability problems. Recommend supplementing with user interviews and A/B testing.*
