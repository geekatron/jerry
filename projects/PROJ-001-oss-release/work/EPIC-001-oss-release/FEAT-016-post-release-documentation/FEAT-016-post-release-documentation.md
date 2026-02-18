# FEAT-016: Post-Release README & Documentation Updates

> **Type:** feature
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-17
> **Due:** ---
> **Completed:** 2026-02-18
> **Parent:** EPIC-001
> **Owner:** Adam Nowak
> **Target Sprint:** ---

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and value proposition |
| [Benefit Hypothesis](#benefit-hypothesis) | Expected benefits from this feature |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done and criteria |
| [Children (Stories/Enablers)](#children-storiesenablers) | Enabler inventory and tracking |
| [Progress Summary](#progress-summary) | Overall feature progress |
| [Related Items](#related-items) | Hierarchy and dependencies |
| [History](#history) | Status changes and key events |

---

## Summary

Update the project README and supporting documentation to accurately reflect the project's current platform support status, Windows portability efforts, and skill/agent optimization roadmap. These updates address post-release transparency needs identified during the OSS post-release planning session.

**Value Proposition:**
- Accurate platform support expectations for users (OSX-primary, Windows portability)
- Transparency about skill/agent definition optimization roadmap
- Active solicitation of Windows-specific issue reports from users

**Source:** Transcript packet `transcript-oss-post-release-20260217-001` (ACT-001, ACT-002, ACT-003)

---

## Benefit Hypothesis

**We believe that** updating the README with accurate platform notices, Windows issue solicitation, and optimization disclaimers

**Will result in** reduced confusion for new users, increased Windows issue reporting, and clear expectations about skill quality

**We will know we have succeeded when** README contains platform notice, Windows issues section exists, and optimization disclaimer is visible in documentation

---

## Acceptance Criteria

### Definition of Done

- [x] All enablers completed
- [x] README updated with OSX-primary platform notice
- [x] Windows issue solicitation guidance added
- [x] Skill/agent optimization disclaimer added to documentation
- [x] All acceptance criteria verified
- [x] Feature request issue template aligned with worktracker Feature entity

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | README clearly states the project was primarily built for OSX | [x] |
| AC-2 | README mentions Windows portability support is in progress | [x] |
| AC-3 | Users can find guidance on filing Windows-specific issues | [x] |
| AC-4 | Documentation includes disclaimer that skill/agent definitions will be optimized in upcoming releases | [x] |
| AC-5 | Feature request issue template exists with fields mapped to worktracker Feature entity | [x] |

---

## Children (Stories/Enablers)

### Enabler Inventory

| ID | Type | Title | Status | Priority | Effort |
|----|------|-------|--------|----------|--------|
| EN-936 | Enabler | Update README with OSX-primary platform notice | done | high | 2 |
| EN-937 | Enabler | Add Windows issue solicitation guidance | done | medium | 2 |
| EN-938 | Enabler | Add skill/agent optimization disclaimer | done | medium | 1 |
| EN-945 | Enabler | Create cross-platform issue templates (macOS & Linux) | done | high | 2 |
| EN-946 | Enabler | Feature request issue template (worktracker-aligned) | done | high | 2 |

### Work Item Links

- [EN-936: Update README with OSX-primary platform notice](./EN-936-readme-platform-notice/EN-936-readme-platform-notice.md)
- [EN-937: Add Windows issue solicitation guidance](./EN-937-windows-issue-solicitation/EN-937-windows-issue-solicitation.md)
- [EN-938: Add skill/agent optimization disclaimer](./EN-938-optimization-disclaimer/EN-938-optimization-disclaimer.md)
- [EN-945: Create cross-platform issue templates (macOS & Linux)](./EN-945-cross-platform-issue-templates/EN-945-cross-platform-issue-templates.md)
- [EN-946: Feature request issue template (worktracker-aligned)](./EN-946-feature-request-template/EN-946-feature-request-template.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Enablers:  [####################] 100% (5/5 completed)            |
| Effort:    [####################] 100% (9/9 points completed)     |
+------------------------------------------------------------------+
| Overall:   [####################] 100%                            |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Enablers** | 5 |
| **Completed Enablers** | 5 |
| **Total Effort (points)** | 9 |
| **Completed Effort** | 9 |
| **Completion %** | 100% |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001: OSS Release Preparation](../EPIC-001-oss-release.md)

### Related Features

- [FEAT-017: Installation Instructions Modernization](../FEAT-017-installation-instructions/FEAT-017-installation-instructions.md) - Co-identified in post-release planning session

### Transcript Source

- **Packet:** `transcript-oss-post-release-20260217-001`
- **Action Items:** ACT-001 (README update), ACT-002 (Windows issues), ACT-003 (optimization disclaimer)
- **Decisions:** DEC-001 (OSX-primary status), DEC-002 (optimization deferred)
- **Topics:** TOP-001 (Platform Support), TOP-002 (Skill/Agent Quality)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-17 | Claude | pending | Feature created from transcript packet analysis (ACT-001, ACT-002, ACT-003) |
| 2026-02-18 | Claude | done | All 3 enablers completed. README updated with Platform Support + Known Limitations sections. Windows issue template created at .github/ISSUE_TEMPLATE/windows-compatibility.yml. CONTRIBUTING.md updated with Windows issue reporting section. |
| 2026-02-18 | Claude | in_progress | Scope expanded: EN-945 created for macOS and Linux issue templates. Reverted to in_progress (3/4 enablers). |
| 2026-02-18 | Claude | done | EN-945 complete: macos-compatibility.yml and linux-compatibility.yml created. README Platform Support links all 3 templates. 4/4 enablers, 7/7 points. |
| 2026-02-18 | Claude | in_progress | Scope expanded: EN-946 created for worktracker-aligned feature request issue template. config.yml added for issue template chooser. Reverted to in_progress (4/5 enablers, 7/9 points). |
| 2026-02-18 | Claude | done | EN-946 complete: feature-request.yml with 10 worktracker-aligned fields, config.yml with Discussions link, CONTRIBUTING.md with feature request guidance. 5/5 enablers, 9/9 points. |
