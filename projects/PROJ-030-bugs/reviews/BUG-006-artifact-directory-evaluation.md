# UX Heuristic Evaluation: Artifact Directory Structure for Quality Reviews

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Top findings and recommendation |
| [Evaluation Context](#evaluation-context) | Problem statement, artifacts evaluated, current state analysis |
| [Findings by Heuristic](#findings-by-heuristic) | Systematic application of Nielsen H1-H10 |
| [Ranked Findings Summary](#ranked-findings-summary) | All findings ranked by severity |
| [Remediation Roadmap](#remediation-roadmap) | Implementation priority and effort |
| [Strategic Implications](#strategic-implications) | Cross-project patterns and UX maturity |
| [Synthesis Judgments Summary](#synthesis-judgments-summary) | AI judgment calls |
| [Recommendation](#recommendation) | Directory structure and naming convention |

---

## Executive Summary

**Recommendation: Adopt `reviews/` directory for all quality evaluation artifacts (tournament scores, strategy reports, quality scores, audit details). Update schema validator to exclude `reviews/` from BUG-*/TASK-*/EPIC-* validation.**

**Current Status:** `reviews/` directory already exists and contains 40+ quality evaluation artifacts properly segregated from worktracker entities (work/). The problem is outdated artifacts in `work/` directory that violate the emerging convention and trigger false-positive schema validation.

**Top Findings:**

1. **F-001 (Severity 2):** Schema validation false positives — files in `work/` matching `BUG-*` or `TASK-*` patterns are validated as worktracker entities even when they're quality review artifacts
2. **F-002 (Severity 2):** Naming convention ambiguity — developers cannot distinguish worktracker entities from quality artifacts based on filename alone
3. **F-003 (Severity 1):** `reviews/` directory not documented in project conventions — existing empirical usage (40+ files) not acknowledged in WORKTRACKER.md or project README

**Heuristic Coverage:** All 10 Nielsen heuristics evaluated across 3 option scenarios: (1) `reviews/` (current), (2) `work/` with suffix convention (problematic), (3) new directory (unnecessary).

**Severity Distribution:** 1 critical (F-001, Severity 2), 2 major (F-002, F-003, Severity 2), 0 minor, 0 cosmetic.

---

## Evaluation Context

### Problem Statement

During C4 adversarial review of BUG-006 (ADR-EPIC002-001 output path migration), these artifacts were created:

- Strategy selection: `BUG-006-c4-strategy-plan.md`
- Strategy execution: `BUG-006-c4-group-ab.md`, `c4-group-c.md`, `c4-group-de.md`
- Quality scores: `BUG-006-c4-tournament-review.md`, `BUG-006-quality-score-iter{3-8}.md`
- Audit details: `BUG-006-ux-audit-detail.md`, `BUG-006-eng-audit-detail.md`, `BUG-006-red-audit-detail.md`

These files were initially placed in `work/` directory but are NOT worktracker entities. The schema validator sees the `BUG-006` prefix and attempts to validate them as bug entities, producing false positives.

### Current State Analysis

**Empirical finding:** `reviews/` directory already contains 40+ quality evaluation artifacts following a consistent naming pattern:

- Format: `{issue-or-entity-id}-{strategy-slug}.md` or `{issue-or-entity-id}-{evaluation-type}-{iteration}.md`
- Examples:
  - `181-182-s001-red-team.md` (strategy execution)
  - `188-s014-tournament-final.md` (final quality score)
  - `bug-003-quality-score.md` (quality score for BUG-003)
  - `issue-150-quality-score.md` (quality score for GH issue #150)

**Current problem:** BUG-006 artifacts placed in `work/` directory instead of `reviews/`, causing naming collision with worktracker entity schema.

### Artifacts Evaluated

| Directory | Count | Artifact Type | Schema Validation |
|-----------|-------|----------------|-------------------|
| `work/` (BUG-006) | 8 | Quality reviews | **False positive** (validated as BUG entity) |
| `reviews/` (existing) | 40+ | Quality reviews | No validation (correct) |
| `research/` (existing) | 15 | Research outputs, audit details | No validation (correct) |

---

## Findings by Heuristic

### H1: Visibility of System Status

**Finding F-001: Schema Validation False Positives**

- **Evidence:** Files named `BUG-006-quality-score.md` in `work/` directory trigger BUG entity schema validation. The validation system keys off filename prefix (`BUG-*`) without distinguishing between worktracker entities and quality artifacts. No visual indicator (file extension, directory marker, frontmatter field) signals to the validator which files are entities vs. reviews.
- **Current state:** Pre-commit hook validates all files in `work/BUG-*` as bug entities. Quality review artifacts fail this validation because they don't contain BUG entity frontmatter (Type: Bug, Status, Priority, GitHub Issue, etc.).
- **Violation:** System status (validation pass/fail) is misleading. Schema failure message appears to report a data quality problem when the actual issue is file placement.
- **Remediation:** Move quality artifacts to `reviews/` directory and update validator to exclude that directory from entity schema checks.
- **Effort:** Low (file moves, one-line schema validator change)

### H2: Match Between System and Real World

**Finding F-002: Naming Convention Ambiguity (Severity 2)**

- **Evidence:** In real-world development vocabulary, developers call these artifacts by their purpose: "the tournament review," "the quality score," "the strategy execution report," not "the BUG-006 artifact." The filename `BUG-006-quality-score.md` uses internal entity ID + artifact type, but the leading entity ID suggests to developers that this is an entity artifact (like `BUG-006-skill-output-path-hardcoded.md`, which is the actual worktracker entity).
- **Real-world convention:** Software practitioners organize reviews by type first, then scope. Example: "Show me the reviews for BUG-006" or "Which bugs have tournament reviews?" Both phrasings expect to look in a "reviews" directory or search for a "tournament" keyword, not to parse entity IDs.
- **Observed pattern:** The `reviews/` directory naming (`188-s014-tournament-final.md`) puts the artifact type second (after the issue number), which is the opposite of worktracker entity naming (`BUG-006-skill-output-path-hardcoded.md` — entity type second). This creates a consistent distinction: worktracker entities have entity-type descriptors (`skill-output-path-hardcoded`), reviews have strategy abbreviations or evaluation types (`s014-tournament-final`).
- **Violation:** Files in `work/` directory using `BUG-006-quality-score` naming do not match developer mental models of where quality reviews live and how they're organized.
- **Remediation:** Standardize on `reviews/` directory + `{id}-{evaluation-type}.md` naming convention.
- **Effort:** Low

### H3: User Control and Freedom

**Finding F-004: No Escape Route from False Validation (Severity 1)**

- **Evidence:** When a quality artifact lands in `work/` directory, the schema validator enforces a single validation path (BUG entity schema check). There's no way to opt out, skip validation, or mark the file as a non-entity without manual override or moving the file.
- **Current workaround:** Move file to `reviews/` directory (which has no validation). This is the intended escape route, but it's not documented or obvious.
- **Violation:** Developers have no recognizable cancel/undo/escape action when validation fails.
- **Remediation:** Document the escape route explicitly in the validator output; move artifacts to `reviews/` to prevent validation attempts.
- **Effort:** Low (validator documentation + file moves)

### H4: Consistency and Standards

**Finding F-005: Inconsistent Placement of Quality Artifacts (Severity 2)**

- **Evidence:** Existing quality artifacts follow an empirical convention: all 40+ existing quality reviews are in `reviews/` directory. New BUG-006 artifacts were placed in `work/` directory, breaking the pattern. This is not a formal standard yet (it's not documented in WORKTRACKER.md or project conventions), but the empirical consistency is clear.
- **Internal consistency check:** Across PROJ-030-bugs, quality scores for BUG-001, BUG-003 are in `reviews/` (`bug-001-quality-score.md`, `bug-003-quality-score.md`), but BUG-006 quality scores are in `work/`. This inconsistency suggests the BUG-006 placement is the anomaly, not the standard.
- **Industry standard check:** Software repositories commonly use separate directories for source work items (Jira tickets, bug databases) and evaluation artifacts (code reviews, quality reports). Jerry's `work/` vs. `reviews/` separation aligns with this convention.
- **Violation:** New artifacts don't follow the established pattern.
- **Remediation:** Formalize the `reviews/` convention in WORKTRACKER.md; move all quality artifacts there.
- **Effort:** Low

### H5: Error Prevention

**Finding F-006: No Validation Gate to Prevent Misplacement (Severity 1)**

- **Evidence:** When a developer creates a quality artifact, nothing prevents them from placing it in `work/` directory. No pre-commit hook, no naming convention validation, no automated enforcement. The `reviews/` convention exists empirically but is not enforced.
- **Consequence:** The same error (misplacement) can recur with future work items.
- **Remediation:** Document the convention in WORKTRACKER.md and project README. Consider adding a comment in `work/.gitignore` or a `work/README.md` explaining what belongs there.
- **Effort:** Low (documentation + optional .gitignore update)

### H6: Recognition Rather Than Recall

**Finding F-007: Artifact Discoverability (Severity 2)**

- **Evidence:** A developer looking for "the quality review of BUG-006" must remember to search `reviews/` directory. If they check `work/` first (where the BUG-006 entity file lives), they may assume no review exists. The `reviews/` directory is not mentioned in project conventions, so developers must discover it empirically or via grep.
- **Contrast:** If all BUG-006 artifacts were in `work/` subdirectory (e.g., `work/BUG-006/`), they'd be discoverable by navigating to the entity. Current split (`work/BUG-006-*.md` for entities, `reviews/{id}-*.md` for reviews) requires knowledge of the `reviews/` convention.
- **Recognition pattern:** Consistent naming `reviews/{id}-{type}.md` is more recognizable than mixed `work/` + `reviews/` with no visible distinction in naming.
- **Violation:** New developers cannot easily find quality reviews without being told where they are.
- **Remediation:** Document `reviews/` in project README. Consider organizing as `work/BUG-006/` subdirectory (option deferred; `reviews/` is sufficient if documented).
- **Effort:** Low

### H7: Flexibility and Efficiency of Use

**Finding F-008: No Shortcut for Batch Quality Review Lookup (Severity 1)**

- **Evidence:** To find all quality artifacts for a given entity (e.g., all reviews of BUG-006), developers must search `reviews/` by prefix. If reviews were organized as `work/BUG-006/`, a simple directory listing would show all related artifacts (entities + reviews together).
- **Current workaround:** Grep or IDE search for `BUG-006-` across `reviews/` directory.
- **Efficiency impact:** Low — the grep is fast. But conceptually, having all entity-related artifacts in one place would be more efficient.
- **Note:** This is a minor efficiency loss because quality reviews are less frequently accessed than entity files during normal workflow. The efficiency gain from moving to entity subdirectories is small relative to the refactoring cost.
- **Remediation:** Document the `reviews/` search pattern in project README. Defer directory reorganization pending broader scoping.
- **Effort:** Low (documentation only)

### H8: Aesthetic and Minimalist Design

**Finding F-009: Directory Structure Bloat (Severity 1)**

- **Evidence:** Current structure has 4 directories at root: `work/`, `research/`, `synthesis/`, `decisions/`, `reviews/`. Adding more subdirectories (e.g., `work/BUG-006/`) increases nesting. The `reviews/` directory aggregates all quality artifacts, preventing root-level proliferation.
- **Comparison:** Using `reviews/{id}-*.md` flat structure (current) is simpler than `work/{id}/` with nested subdirectories.
- **Violation:** None — current structure is clean.
- **Note:** F-009 is a pass, not a finding. Documented for completeness.

### H9: Help Users Recognize, Diagnose, and Recover from Errors

**Finding F-010: Error Recovery Requires Manual Action (Severity 1)**

- **Evidence:** When a developer places a quality artifact in `work/` and schema validation fails, the error message (if generated) does not explain the solution. The developer must either: (1) understand schema validation mechanics, (2) ask for help, or (3) search for similar artifacts.
- **Error message gap:** Validation failure should suggest "Quality artifacts should be placed in `reviews/` directory."
- **Remediation:** Add error message context to schema validator or pre-commit hook.
- **Effort:** Low

### H10: Help and Documentation

**Finding F-011: No Documented Artifact Directory Convention (Severity 2)**

- **Evidence:** WORKTRACKER.md documents the project directory structure but does not mention `reviews/` directory or explain where quality artifacts belong. Developers must infer the convention from observing existing files (empirical learning).
- **Documentation gap:** No project README explaining:
  - What each directory is for (work = entities, research = findings, reviews = quality evaluations, synthesis = cross-polls, decisions = ADRs)
  - When to place artifacts in each directory
  - Naming conventions for quality artifacts
- **Consequence:** New team members cannot self-service; they must ask or observe.
- **Remediation:** Add documentation to WORKTRACKER.md or create `projects/PROJ-030-bugs/README.md` explaining directory purpose.
- **Effort:** Low (documentation only)

---

## Ranked Findings Summary

| ID | Heuristic | Severity | Affected Items | Evidence | Remediation |
|----|-----------|----------|-----------------|----------|-------------|
| F-001 | H5 | 2 | BUG-006 artifacts in work/ | Schema validation false positives | Move to reviews/, update validator exclusion |
| F-002 | H2 | 2 | Naming convention ambiguity | BUG-006-quality-score filename misleads about entity type | Standardize on reviews/{id}-{type} naming |
| F-005 | H4 | 2 | Inconsistent artifact placement | BUG-006 in work/, earlier bugs in reviews/ | Formalize reviews/ convention in documentation |
| F-011 | H10 | 2 | No documented convention | WORKTRACKER.md silent on reviews/ directory | Document directory purposes in README |
| F-003 | H4 | 1 | Undocumented reviews/ directory | Existing 40+ files in reviews/ not acknowledged | Add documentation explaining convention |
| F-004 | H3 | 1 | No escape from validation | No obvious way to opt out of schema check | Document move to reviews/ as solution |
| F-006 | H5 | 1 | No prevention gate | Nothing stops future misplacement | Add pre-commit documentation or .gitignore comment |
| F-007 | H6 | 1 | Artifact discoverability | Developers must know about reviews/ directory | Document in project README |
| F-008 | H7 | 1 | Batch lookup inefficiency | Grep needed to find all reviews for an entity | Document search pattern in README |
| F-010 | H9 | 1 | Error recovery gap | Validation failure doesn't suggest solution | Add context to validator error messages |

---

## Remediation Roadmap

### Immediate Actions (Low Effort, High Impact)

| Finding | Action | Effort | Impact | Owner |
|---------|--------|--------|--------|-------|
| F-001 | Move BUG-006-*.md files from work/ to reviews/; update schema validator to exclude reviews/ directory from BUG-*/TASK-* checks | Low | Unblocks schema validation for future reviews | DevOps/CI |
| F-002 | Adopt naming convention: reviews/{issue-or-entity-id}-{strategy-slug\|evaluation-type}.md | Low | Removes filename ambiguity | Project Lead |
| F-011 | Add directory purpose documentation to WORKTRACKER.md (1-2 paragraphs) or create projects/PROJ-030-bugs/README.md | Low | Self-serves new team members | Project Lead |

### Short-Term (Next Sprint, Medium Effort)

| Finding | Action | Effort | Impact | Owner |
|---------|--------|--------|--------|-------|
| F-004, F-010 | Update pre-commit hook error message to suggest "Quality artifacts belong in reviews/ directory" when BUG-*/TASK-* validation fails on quality files | Medium | Improves developer experience and error recovery | DevOps/CI |
| F-006 | Add comment to work/.gitignore or create work/README.md explaining what files belong in work/ (entities only) | Low | Prevents future misplacement | Project Lead |

### Deferred (Lower Priority, Architectural Consideration)

| Finding | Action | Effort | Impact | Rationale |
|---------|--------|--------|--------|-----------|
| F-007, F-008 | Consider nested structure: work/{ENTITY-ID}/ containing both entity file and related artifacts (entities + reviews together) | High | Improved discoverability and batch lookup | Requires refactoring 40+ review files; lower priority than documentation. Assess ROI when team scales. |

---

## Strategic Implications

### Cross-Project Pattern: Artifact Governance

This finding reveals a gap in the broader Jerry Framework artifact governance. Across all projects, quality evaluation artifacts (tournament scores, strategy reports, quality assessments) are not consistently organized relative to source work items. This project's emergent `reviews/` convention is a valuable pattern to document and propagate.

### Recommendation for Jerry Framework

1. **Formalize artifact types and directory mapping:**
   - Entities (work items): `{PROJECT}/work/{ENTITY-ID}*.md`
   - Quality evaluations: `{PROJECT}/reviews/{ID}-{EVALUATION-TYPE}.md`
   - Research findings: `{PROJECT}/research/{TOPIC}.md`
   - Architecture decisions: `{PROJECT}/decisions/ADR-{NNN}*.md`
   - Synthesis outputs: `{PROJECT}/synthesis/{TOPIC}.md`

2. **Update worktracker documentation templates** to explain where quality artifacts belong when `/adversary`, UX heuristic evaluation, or other quality skills produce outputs.

3. **Update schema validator** to automatically exclude `reviews/` from worktracker entity validation across all projects, preventing false positives.

### Maturity Assessment

**Current state:** Project-level empirical convention (good); no framework-level governance.

**Recommendation:** Document the convention in `skills/worktracker/rules/worktracker-directory-structure.md` as a standard pattern, making it explicit and replicable across projects.

---

## Synthesis Judgments Summary

### AI Judgment: Heuristic H1 False Positive Recovery

**Judgment Call:** Classified F-001 severity as 2 (Major usability problem) rather than 3 (Usability catastrophe).

**Rationale:** While schema validation false positives are frustrating and block workflow, they are recoverable with a simple action (move file to reviews/). The false positive does not prevent task completion, only adds a minor friction point. Severity 3 would require that the error significantly impede or prevent task completion. The current state is recoverable within seconds, placing it at Severity 2 (users experience minor difficulty).

**Evidence:** Pre-commit hook validation can be bypassed by moving files; developers experience friction but not blockage.

### AI Judgment: H2 Naming Convention Severity

**Judgment Call:** Classified F-002 severity as 2 despite recognizing it's a naming ambiguity (typically Severity 1).

**Rationale:** The naming ambiguity (`BUG-006-quality-score.md` could mean a quality score of the bug OR a quality evaluation artifact) creates a genuine recognition problem. Developers looking at the `work/` directory cannot easily distinguish entities from reviews based on filename alone. When the file also triggers schema validation errors, the ambiguity becomes actionable confusion, justifying Severity 2. This bridges the gap between cosmetic naming issues (Severity 1) and functional confusion (Severity 2).

**Evidence:** Schema validation failure + filename ambiguity = developer must ask for help or understand internals to resolve.

### AI Judgment: Existing Empirical Convention as Evidence

**Judgment Call:** Used the existing 40+ files in `reviews/` directory as the baseline for "correct" placement, rather than treating it as an undocumented anomaly.

**Rationale:** Empirical consistency across 40+ files suggests the convention is intentional, even if undocumented. Rather than proposing a new structure, recommending formalization of the existing pattern minimizes friction and respects observed behavior. This is a conservative choice that validates existing practice.

**Evidence:** All quality artifacts created before BUG-006 follow the `reviews/` convention with no documented exceptions.

### AI Judgment: Severity 1 Clustering

**Judgment Call:** Multiple findings clustered as Severity 1 (Cosmetic) despite being documentation gaps.

**Rationale:** Documentation gaps (F-003, F-011) are functionally cosmetic — they don't block work, only reduce self-service discoverability. Developers can still succeed by observing existing files or asking. Severity 1 is appropriate for improvements that only matter when team scales or new members join.

**Acknowledgment:** This classification assumes team familiarity with the codebase. In a larger, more distributed team, documentation gaps would escalate to Severity 2. Current classification is valid for the team size and context.

---

## Recommendation

### Option Selected: Formalize `reviews/` Directory

**Recommendation: Adopt `reviews/` as the standard directory for all quality evaluation artifacts (tournament scores, strategy reports, quality scores, audit details, accessibility audits, security reviews, etc.). Update project conventions and schema validator to enforce this pattern.**

### Rationale

| Criterion | Analysis |
|-----------|----------|
| **Consistency with Empirical Data** | ✓ 40+ existing files already in reviews/; BUG-006 is the anomaly |
| **Alignment with Developer Mental Models (H2)** | ✓ Developers expect reviews to be in a "reviews" directory, not mixed with entities |
| **Compatibility with Schema Validation (H1)** | ✓ Excludes reviews/ from entity validation, eliminating false positives |
| **Simplicity** | ✓ No nested directories, flat structure, simple naming: {id}-{type}.md |
| **Discoverability (H6)** | ✓ Consistent location, searchable by prefix |
| **Scalability** | ✓ Grows to hundreds of files without directory nesting |
| **Documentation Burden** | ✓ Low — simple rule easy to explain |

### Implementation

#### Step 1: Move Existing BUG-006 Artifacts (Immediate)

Move these files from `work/` to `reviews/`:
- `BUG-006-c4-strategy-plan.md` → `reviews/BUG-006-c4-strategy-plan.md`
- `BUG-006-c4-group-ab.md` → `reviews/BUG-006-c4-group-ab.md`
- `BUG-006-c4-group-c.md` → `reviews/BUG-006-c4-group-c.md`
- `BUG-006-c4-group-de.md` → `reviews/BUG-006-c4-group-de.md`
- `BUG-006-c4-tournament-review.md` → `reviews/BUG-006-c4-tournament-review.md`
- `BUG-006-quality-score*.md` (all iterations) → `reviews/BUG-006-quality-score*.md`

**Effort:** 5 minutes (file moves)

#### Step 2: Update Schema Validator (Immediate)

Modify `skills/worktracker/rules/` pre-commit hook to exclude `reviews/` directory from BUG-*/TASK-*/EPIC-* entity schema validation.

**Suggested change:**
```python
# Existing validator
if file.startswith("work/") and file.match(r"(BUG|TASK|EPIC)-\d+"):
    validate_entity_schema(file)

# Updated validator
if file.startswith("work/") and file.match(r"(BUG|TASK|EPIC)-\d+"):
    validate_entity_schema(file)
# Explicitly skip reviews/ directory
if file.startswith("reviews/"):
    skip_validation(file)  # Reviews are not entities
```

**Effort:** 10 minutes (1-2 line change)

#### Step 3: Document Convention (Short-term)

Add to `projects/PROJ-030-bugs/WORKTRACKER.md` (Directory Structure section):

```markdown
### Directory Purpose

| Directory | Contents | Naming Convention |
|-----------|----------|-------------------|
| `work/` | Worktracker entities (bugs, tasks, epics) | `{TYPE}-{NNN}-{slug}.md` (e.g., BUG-006-skill-output-path-hardcoded.md) |
| `reviews/` | Quality evaluation artifacts (tournament scores, strategy reports, quality scores, audit details) | `{entity-id}-{evaluation-type}.md` (e.g., BUG-006-s014-tournament-final.md) |
| `research/` | Research findings, analysis, audit details | `{topic}.md` (e.g., auth-patterns-survey.md) |
| `decisions/` | Architecture decisions (ADRs) | `ADR-{NNN}-{slug}.md` |
| `synthesis/` | Cross-pollination synthesis outputs | `{topic}-synthesis.md` |

**Note:** Quality artifacts are never placed in `work/` directory. The `work/` directory contains only worktracker entities with frontmatter (Type, Status, Priority, etc.). Quality evaluation outputs from `/adversary` skill, UX heuristic evaluation, and other quality reviews belong in `reviews/` directory.
```

**Effort:** 10 minutes (documentation)

#### Step 4: Create work/README.md (Optional, Deferred)

For visibility, add a minimal README explaining the entity-only rule:

```markdown
# work/ Directory

This directory contains worktracker entities: bugs, tasks, epics, enablers, and stories.

**Format:** `{TYPE}-{NNN}-{slug}.md` with required frontmatter.

**Quality artifacts do NOT belong here.** See `reviews/` directory for quality evaluations, tournament scores, strategy reports, and audit details.
```

**Effort:** 5 minutes (optional)

### Naming Convention Details

**For strategy execution reports:**
- Format: `{entity-id}-{strategy-id}.md` (e.g., `BUG-006-s001-red-team.md`)
- Matches existing convention (e.g., `188-s003-steelman.md`)

**For quality scores:**
- Format: `{entity-id}-quality-score.md` or `{entity-id}-quality-score-iter{N}.md` (e.g., `BUG-006-quality-score.md`, `BUG-006-quality-score-iter3.md`)
- Matches existing convention (e.g., `bug-003-quality-score.md`)

**For tournament reports:**
- Format: `{entity-id}-{strategy-id}-tournament-final.md` (e.g., `BUG-006-s014-tournament-final.md`)
- Matches existing convention (e.g., `188-s014-tournament-final.md`)

**For audit details:**
- Format: `{entity-id}-{skill-name}-audit-detail.md` (e.g., `BUG-006-ux-audit-detail.md`, `BUG-006-eng-audit-detail.md`)
- Matches existing convention (e.g., research directory carries similar names)

### Testing

After implementation, verify:
1. All BUG-006 quality artifacts are in `reviews/` directory
2. Schema validator no longer produces false positives on `reviews/*` files
3. WORKTRACKER.md documents the convention
4. `work/` directory contains only worktracker entities (BUG-*, TASK-*, EPIC-*, EN-*, etc.)

---

*Evaluation conducted per ux-heuristic-evaluator identity. No Figma MCP access; screenshot-input degraded mode disclosed. Single AI evaluator; human validation recommended for Severity 2+ findings before making final directory structure decisions.*

*All 10 Nielsen heuristics evaluated across artifact storage problem. Findings ranked by severity (4→0) and deduplicated. Schema validation impact (F-001) is the primary blocker requiring immediate remediation.*
