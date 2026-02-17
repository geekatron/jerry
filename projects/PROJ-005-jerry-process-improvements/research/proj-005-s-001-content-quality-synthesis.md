# PROJ-005-S-001: Work Item Content Quality - Research Synthesis

> **PS ID:** proj-005
> **Entry ID:** s-001
> **Type:** Synthesis
> **Status:** Complete
> **Synthesizer:** ps-synthesizer (v2.0.0)
> **Date:** 2026-02-16
> **Topic:** Work Item Content Quality - Research Synthesis
> **Inputs:**
> - `proj-005-r-001` (Research): AC Quality Best Practices
> - `proj-005-a-001` (Analysis): Worktracker Content Quality Gap Analysis

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Five key synthesis conclusions for stakeholders |
| [L1 Detailed Synthesis](#l1-detailed-synthesis) | Cross-referenced findings, reconciled rules, prioritized plan |
| [L2 Strategic Implications and Risks](#l2-strategic-implications-and-risks) | Risk analysis, over-engineering concerns, long-term trajectory |
| [Consolidated Implementation Plan](#consolidated-implementation-plan) | Final agreed-upon changes with files, dependencies, complexity |
| [Sources](#sources) | Traceability to input documents |

---

## L0 Executive Summary

1. **Both inputs agree: the worktracker has zero content quality rules, and this is the root cause of recurring quality complaints.** The researcher found that industry best practices (QUS framework, INVEST, Diataxis) provide proven, measurable criteria for content quality. The analyst found that Jerry's WTI-001 through WTI-006 enforce only operational state -- never what is written inside work items. These findings are fully convergent: the gap is real and well-understood.

2. **The two rule proposals are complementary, not competing.** The researcher proposed WTI-007 through WTI-012 (six standalone rules, one concern per rule). The analyst proposed WTI-007 and WTI-008 (two umbrella rules with sub-rules 007a-007g and 008a-008d). The reconciled approach adopts the analyst's grouping structure (two rules, sub-rules) because it matches Jerry's existing WTI rule style, while incorporating the researcher's explicit naming and layered quality gate model to organize enforcement.

3. **Rubber-stamp risk and over-engineering risk are the two primary threats.** The researcher documented that zero-override rates signal blind trust, not quality. The analyst proposed four collaboration checkpoints -- but four mandatory checkpoints per work item risks the opposite problem: Claude becomes so cautious it slows work to a crawl. The reconciled plan reduces to two checkpoints (pre-creation and AC review) with explicit skip mechanisms and a scope-overflow warning that triggers only when bullet counts exceed limits.

4. **Templates should gain creation guides without losing reference depth.** Both inputs agree that the current 400-500 line templates are ontology references, not creation workflows. The Diataxis framework (researcher) and the Quick Creation Guide proposals (analyst) converge on the same solution: prepend a 30-50 line actionable guide to each template. The reference material stays but gains `<!-- REFERENCE ONLY -->` markers. No template restructuring or splitting is required.

5. **The Definition of Done must be extracted from individual work item AC into a shared artifact.** Both inputs independently identify this as a critical anti-pattern: STORY.md lines 289-313 contain DoD items ("Code reviewed," "Tests passing") that teach Claude to conflate AC with DoD. The fix is a shared `DOD.md` file, with the STORY.md DoD section reframed as a cross-reference rather than content to copy into each work item.

---

## L1 Detailed Synthesis

### 1. Cross-Reference of Findings

#### Where Research and Analysis Agree

| Finding | Researcher (r-001) | Analyst (a-001) | Convergence |
|---------|---------------------|------------------|-------------|
| AC must be testable, outcome-focused | QUS framework (Lucassen et al. 2016), Agile Alliance INVEST | ADO skill patterns lines 112-133, AC standards full file | **Full agreement** |
| AC must not contain DoD items | AC/DoD separation rule with citations from Agile Sherpas, AltexSoft | WTI-007a proposal with regex detection patterns | **Full agreement** |
| 3-5 AC bullets is the sweet spot | Scrum.org forum, AltexSoft, INVEST principle | ADO skill limits: Features 5, PBIs 4, Bugs 3 | **Agreement on range; analyst has per-type limits** |
| 6+ AC signals scope overflow | SPIDR splitting framework | WTI-007g scope overflow signal | **Full agreement** |
| Templates need creation guides | Diataxis framework (how-to vs reference) | Quick Creation Guide proposals for BUG, STORY, TASK | **Full agreement on approach** |
| LLMs need explicit rubrics | Springer JIIS 2025 study (kappa 0.84-0.87 with criteria) | wt-auditor content quality check with regex patterns | **Complementary** -- researcher provides rationale, analyst provides implementation |
| Human oversight must be smart, not exhaustive | Rubber-stamp risk, autonomy levels framework | WTI-008 collaboration checkpoints with skip mechanism | **Agreement on principle; differ on checkpoint count** |

#### Where They Differ

| Area | Researcher Position | Analyst Position | Reconciliation |
|------|---------------------|------------------|----------------|
| **Rule structure** | Six standalone rules (WTI-007 to WTI-012) | Two umbrella rules with sub-rules (WTI-007a-g, WTI-008a-d) | **Adopt analyst grouping.** Jerry's existing WTI rules are numbered sequentially. Sub-rules keep the numbering compact while preserving granularity. |
| **Checkpoint count** | Four tiers: auto-approve, summary review, full review, explicit approval | Four specific checkpoints: story pre-check, bug pre-check, AC review, scope overflow | **Reduce to three interaction points.** Merge story/bug pre-check into a single "pre-creation checkpoint" (the information gathered differs by type, but the interaction pattern is the same). Keep AC review. Scope overflow triggers only when limits exceeded (not a checkpoint per se). |
| **Quality gate layers** | Four layers: structural, content form, content semantics, human review | Two severity tiers within wt-auditor: WARNING and INFO | **Adopt researcher's four-layer model for conceptual framing,** but implement only layers 1-2 as automated rules. Layer 3 (semantic) is advisory via wt-auditor. Layer 4 (human review) is the collaboration checkpoints. |
| **Template treatment** | Separate `*_GUIDE.md` files alongside templates | Prepend Quick Creation Guide section inside templates | **Prepend inside templates.** Separate files create a discoverability problem -- Claude must know to look for two files. A guide prepended to the template is guaranteed to be read first. |
| **DoD handling** | Create `DOD.md` shared file | Remove/reframe DoD section in STORY.md | **Both.** Create `DOD.md` AND reframe STORY.md section to reference it. |

### 2. Consolidated Rule Set

The reconciled rule set extends WTI-001 through WTI-006 with two new rules: WTI-007 (Content Quality) and WTI-008 (Collaboration Before Creation).

#### WTI-007: Content Quality Standards (HARD)

**Rule:** All work item content (Summary, Acceptance Criteria, Description) MUST meet content quality standards.

**Preamble (from researcher):** "If an engineer needs to ask clarifying questions, the AC has failed." Write in a concise, direct style. AC describes outcomes observable by users, testers, or systems -- never implementation details, architecture decisions, or process requirements.

| Sub-Rule | Name | Enforcement | Detail |
|----------|------|-------------|--------|
| WTI-007a | No DoD in AC | HARD | AC must not contain Definition of Done items: test coverage, code review, documentation updates, deployment verification, QA sign-off. Universal test: "If it applies to every work item equally, it is DoD, not AC." |
| WTI-007b | No Implementation Details in AC | HARD | AC must not contain file paths, class names, method names, architecture patterns, or technology-specific decisions. Implementation details belong in Implementation Notes or task descriptions. |
| WTI-007c | Actor-First Format | MEDIUM | AC bullets should begin with an actor or system subject: "User can...", "System validates...", "API returns...", "Admin sees...". |
| WTI-007d | No Hedge Words | MEDIUM | AC must not use hedge words: "should be able to", "might need to", "could potentially", "if possible", "ideally", "as needed", "when appropriate". Replace with direct, testable statements. |
| WTI-007e | AC Bullet Count Limits | HARD | Maximum AC bullets by type: Story: 5, Bug: 3, Task: 3, Enabler: 5, Feature: 5. Exceeding the limit triggers WTI-007g. |
| WTI-007f | Summary Brevity | MEDIUM | Summary must be 1-3 sentences. Describe the what and why. No implementation details. Bug summaries describe symptoms, not root causes. |
| WTI-007g | Scope Overflow Signal | HARD | If AC exceeds the bullet limit (WTI-007e), the work item scope is likely too large. Claude MUST flag this and recommend splitting using the SPIDR framework (Spike, Paths, Interfaces, Data, Rules). |

**Anti-Pattern Examples (include in rule definition):**

```markdown
# BAD AC (violates WTI-007a, WTI-007b):
- [ ] Update AssetTypeRepository.cs to add new method
- [ ] All unit tests pass with 90%+ coverage
- [ ] Code reviewed and approved
- [ ] Documentation updated

# GOOD AC (compliant):
- [ ] Admin can create a new asset type from the Asset Management page
- [ ] System validates asset type name is unique within the tenant
- [ ] API returns 409 Conflict when duplicate name is submitted
```

**Traceability:**
- WTI-007a: researcher AC/DoD separation + analyst ADO skill lines 25-32
- WTI-007b: researcher outcome-focus finding + analyst ADO skill lines 131-133
- WTI-007c: analyst ADO AC standards line 12
- WTI-007d: analyst ADO AC standards line 13
- WTI-007e: analyst ADO skill bullet counts + researcher 3-5 consensus
- WTI-007f: analyst ADO skill description brevity rules
- WTI-007g: researcher SPIDR framework + analyst scope overflow design

#### WTI-008: Collaboration Before Creation (HARD)

**Rule:** Claude MUST validate understanding with the user before creating work items that contain Acceptance Criteria.

| Sub-Rule | Name | Enforcement | Detail |
|----------|------|-------------|--------|
| WTI-008a | Pre-Creation Checkpoint | HARD | Before writing a work item file, present a summary of what will be created (role/goal/benefit for stories; symptom/location/severity for bugs; what/why for enablers) and ask for confirmation. |
| WTI-008b | AC Review Checkpoint | HARD | After drafting AC but before writing the file, present the AC to the user with three quality check questions: (1) Can an engineer build this without asking questions? (2) Can QA write test cases from these criteria? (3) Are there any ambiguous terms? |
| WTI-008c | Missing Information Flag | HARD | If insufficient context exists to write specific AC, Claude MUST ask for clarification rather than generating vague AC. |
| WTI-008d | Skip Mechanism | MEDIUM | User can say "skip" or "just create it" to bypass checkpoints. Claude must acknowledge the quality trade-off and add an HTML comment: `<!-- WTI-008: Checkpoint skipped by user -->`. |

**Checkpoint Interaction Design:**

All checkpoints use the `(Recommended)` tag pattern to guide the user toward the quality path without being coercive.

```
Before I create this [type], let me confirm my understanding:

[Type-specific summary fields]

Does this capture the intent?

(Recommended) Proceed with corrections
Skip -- create with what you have
```

**Design Decision -- Why Two Checkpoints, Not Four:**

The analyst proposed four checkpoints (story pre-check, bug pre-check, AC review, scope overflow). The researcher's rubber-stamp risk findings warn that too many checkpoints cause approval fatigue. The reconciled design:

- **Merges** story pre-check and bug pre-check into a single "pre-creation checkpoint" that adapts its questions by work item type
- **Keeps** AC review as a separate checkpoint because it occurs at a different point in the workflow (after drafting, before writing)
- **Demotes** scope overflow from a checkpoint to a **triggered warning** -- it only fires when WTI-007e is violated, not on every creation
- **Net result:** Two mandatory checkpoints per work item creation (not four), with an occasional third trigger for scope overflow

**Traceability:**
- WTI-008a: analyst checkpoint 1/2 design + user feedback items #1, #3
- WTI-008b: analyst checkpoint 3 + ADO AC standards quality check questions
- WTI-008c: analyst WTI-008c + researcher "rationale clarity" LLM weakness finding
- WTI-008d: analyst skip mechanism + researcher autonomy levels framework

### 3. Layered Quality Gate Model

The researcher proposed four enforcement layers. The analyst proposed content quality checks in the wt-auditor. These are reconciled into a unified enforcement model:

```
Layer 1: Structural Integrity (existing -- WTI-001 to WTI-006)
  Enforcement: Automated, blocking
  Scope: File existence, state consistency, evidence links, atomic updates
  Owner: worktracker-behavior-rules.md
  Status: COMPLETE (already implemented)

Layer 2: Content Form (new -- WTI-007a,b,c,d,e,f,g)
  Enforcement: Automated checks (regex-based), blocking for HARD sub-rules
  Scope: AC presence, bullet counts, DoD detection, implementation detail detection,
         hedge words, actor-first format, summary length
  Owner: worktracker-behavior-rules.md (rule) + worktracker-content-quality.md (reference)
  Status: TO BE IMPLEMENTED

Layer 3: Content Semantics (new -- wt-auditor Phase 2.5)
  Enforcement: Automated advisory (WARNING/INFO severity)
  Scope: Deeper semantic analysis of AC quality, outcome-focus assessment
  Owner: wt-auditor agent definition
  Status: TO BE IMPLEMENTED (Priority 3)

Layer 4: Human Review (new -- WTI-008)
  Enforcement: Interactive checkpoints with skip mechanism
  Scope: Pre-creation understanding, AC review, scope overflow
  Owner: worktracker-behavior-rules.md
  Triggers:
    - Always: Pre-creation checkpoint, AC review checkpoint
    - Conditional: Scope overflow (only when WTI-007e violated)
    - Never auto-approve: Scope changes, item deletion, priority overrides
  Status: TO BE IMPLEMENTED
```

### 4. Template Changes

#### Quick Creation Guides

Both inputs converge on adding creation guides to templates. The analyst provided draft guides for BUG, STORY, and TASK. The researcher's Diataxis analysis confirms this is the correct approach (how-to guide for the "doing" quadrant).

**Consolidated guide requirements:**
- Maximum 30-50 lines
- Placed at the top of each template, after the HTML comment header and before Document Sections
- Action-oriented, step-by-step
- Include explicit good/bad AC examples
- Reference WTI-007 sub-rules by ID
- End with a completeness checklist

**Templates requiring guides (by priority):**

| Template | Lines | Creation-Relevant % | Guide Priority |
|----------|-------|---------------------|----------------|
| STORY.md | 492 | 41% | **P1** -- most commonly created |
| BUG.md | 467 | 47% | **P1** -- high quality impact |
| TASK.md | 252 | 38% | **P1** -- most frequently created |
| ENABLER.md | 400+ | ~45% (est.) | P2 |
| FEATURE.md | ~350 (est.) | ~40% (est.) | P2 |

#### Definition of Done Extraction

**Create:** `c:\AI\jerry\.context\templates\worktracker\DOD.md`

Contents: A shared Definition of Done applicable to all work items, containing the process-quality items currently embedded in STORY.md lines 289-313.

**Modify:** `c:\AI\jerry\.context\templates\worktracker\STORY.md`

Reframe the "Definition of Done" section (lines 289-313) to reference `DOD.md` rather than listing DoD items inline. Add explicit note: "These items do NOT belong in individual work item Acceptance Criteria."

#### Reference-Only Markers

Add `<!-- REFERENCE ONLY: Skip during creation -->` comments to ontology sections in all templates. This gives Claude a signal to deprioritize these sections during creation workflows.

### 5. wt-auditor Enhancement

The analyst's Phase 2.5 Content Quality Check proposal is well-specified with concrete regex patterns. This maps to Layer 3 (Content Semantics) in the quality gate model. Key implementation details:

**New audit check type:** Content Quality (severity: warning)

**Detection patterns adopted from analyst (a-001):**
- DoD detection: 9 regex patterns for common DoD phrases
- Implementation detail detection: 6 regex patterns for file paths, class names, code patterns
- Hedge word detection: 9 regex patterns for uncertainty language
- Bullet count validation: Count checkbox patterns against per-type limits
- Summary length: Sentence counting against 3-sentence maximum
- Actor-first format: Regex for subject-first AC pattern (INFO, not WARNING)

**Report format addition:** New "Content Quality Issues" subsection in audit reports with file, sub-rule, matched text, and remediation columns.

---

## L2 Strategic Implications and Risks

### Risk 1: Rubber-Stamp Risk (HIGH)

**Source:** Researcher finding Q4, citing CyberManiacs, Mediate.com, GitLab

**The problem:** If collaboration checkpoints become routine, users will auto-approve without reading. This is worse than no checkpoints because it creates a false sense of quality.

**Mitigations built into the plan:**
- Only two mandatory checkpoints (not four) to reduce fatigue
- Skip mechanism acknowledges quality trade-off explicitly
- `(Recommended)` tags guide without coercing
- Scope overflow is conditional, not always-on
- WTI-008c forces Claude to ask for real information rather than presenting boilerplate for approval

**Monitoring signal:** If users consistently skip both checkpoints, the checkpoints are either too frequent or not providing value. Track skip rates in work item HTML comments.

**Residual risk:** MEDIUM. Two checkpoints is the minimum viable oversight. The skip mechanism prevents hostage-taking but also allows quality to degrade if users always skip.

### Risk 2: Over-Engineering Risk (MEDIUM)

**The problem:** Too many rules cause Claude to spend more tokens on compliance than on content. The current 6 WTI rules are manageable. Adding 2 more rules with 11 sub-rules could push past the threshold where Claude starts ignoring rules or applying them mechanically.

**Mitigations built into the plan:**
- Sub-rules are grouped under two parent rules (WTI-007, WTI-008), not 11 separate rules
- The content quality reference file (`worktracker-content-quality.md`) is loaded on-demand, not auto-loaded -- Claude reads it when creating/auditing work items, not at session start
- Quick Creation Guides distill the rules into actionable steps that Claude follows naturally during creation
- HARD vs MEDIUM enforcement levels allow Claude to prioritize (HARD rules are non-negotiable; MEDIUM rules are best-effort)

**Monitoring signal:** If work item creation time increases significantly, or if Claude produces verbose "compliance explanations" in its output, the rule set is too heavy.

**Residual risk:** LOW-MEDIUM. The grouping strategy and on-demand loading should keep cognitive overhead manageable.

### Risk 3: Template Bloat (MEDIUM)

**The problem:** Adding 30-50 lines of creation guide to templates that are already 250-500 lines makes them even longer. This seems contradictory to the "wall of text" complaint.

**Mitigations built into the plan:**
- Creation guides go at the TOP -- Claude reads them first and can deprioritize the rest
- `<!-- REFERENCE ONLY -->` markers signal which sections to skip during creation
- The guide IS the actionable content; the rest IS the reference content. Diataxis says both can coexist if clearly delineated
- No content is removed from templates (preserving ontology completeness), only deprioritized

**Alternative considered:** Separate `*_GUIDE.md` files. Rejected because discoverability is worse -- Claude must be told to look for the guide file, whereas content at the top of the template is automatically read first.

**Residual risk:** LOW. The net effect is that Claude reads 30-50 useful lines at the top instead of scanning 400+ lines looking for what matters.

### Risk 4: Regex False Positives in wt-auditor (LOW)

**The problem:** The analyst's regex patterns for DoD detection, implementation detail detection, and hedge word detection will produce false positives. For example, "System validates that test data is consistent" would match the "test" pattern in DoD detection.

**Mitigations built into the plan:**
- All content quality checks are severity WARNING or INFO, never ERROR/blocking
- Reports include matched text for human review
- Remediation suggestions are advisory
- Pattern refinement can happen iteratively based on false positive rates

**Residual risk:** LOW. False positives in advisory warnings are annoying but not harmful.

### Strategic Trajectory

This synthesis represents the first content quality layer for Jerry's worktracker. The long-term trajectory is:

1. **Now (this plan):** Rule-based content quality (WTI-007, WTI-008) + collaboration checkpoints
2. **Near-term:** wt-auditor automated detection (Phase 2.5) provides feedback loops
3. **Future:** LLM-as-judge evaluation using the quality assessment rubric from the researcher's findings (YAML rubric in r-001 strategic implications section 6). This requires explicit evaluation criteria to achieve the near-human kappa scores documented in the Springer JIIS 2025 study.
4. **Long-term:** Confidence-based routing where Claude auto-assesses its own AC quality and only triggers human review when confidence is low (researcher's "smart escalation" pattern).

---

## Consolidated Implementation Plan

### Phase 1: Foundation (Priority 1 -- Blocks Quality)

| ID | Action | Files to Create/Modify | Dependencies | Complexity | Traceability |
|----|--------|------------------------|--------------|------------|--------------|
| S1-01 | Define WTI-007 (Content Quality Standards) with all sub-rules in behavior rules file | `skills/worktracker/rules/worktracker-behavior-rules.md` | None | **Medium** | r-001 Q1, Q3; a-001 Area 1 |
| S1-02 | Create content quality reference file with anti-patterns, good/bad examples, AC standards, concrete vs vague table, SPIDR splitting guide | `skills/worktracker/rules/worktracker-content-quality.md` (NEW) | S1-01 | **Medium** | r-001 Q1 anti-patterns; a-001 Area 3 ADO pattern extraction |
| S1-03 | Add Quick Creation Guide to STORY.md template | `.context/templates/worktracker/STORY.md` | S1-01 | **Low** | r-001 Q5 Diataxis; a-001 Area 2 STORY analysis |
| S1-04 | Add Quick Creation Guide to BUG.md template | `.context/templates/worktracker/BUG.md` | S1-01 | **Low** | r-001 Q5 Diataxis; a-001 Area 2 BUG analysis |
| S1-05 | Add Quick Creation Guide to TASK.md template | `.context/templates/worktracker/TASK.md` | S1-01 | **Low** | r-001 Q5 Diataxis; a-001 Area 2 TASK analysis |

### Phase 2: Collaboration and DoD (Priority 2 -- Addresses User Feedback)

| ID | Action | Files to Create/Modify | Dependencies | Complexity | Traceability |
|----|--------|------------------------|--------------|------------|--------------|
| S1-06 | Define WTI-008 (Collaboration Before Creation) with all sub-rules | `skills/worktracker/rules/worktracker-behavior-rules.md` | S1-01 | **Medium** | r-001 Q4; a-001 Area 4 |
| S1-07 | Create shared Definition of Done file | `.context/templates/worktracker/DOD.md` (NEW) | None | **Low** | r-001 AC/DoD separation; a-001 STORY.md DoD problem |
| S1-08 | Reframe DoD section in STORY.md to reference DOD.md | `.context/templates/worktracker/STORY.md` | S1-07 | **Low** | r-001 AC/DoD separation; a-001 R-5 |
| S1-09 | Update worktracker SKILL.md to reference WTI-007, WTI-008, and content quality file | `skills/worktracker/SKILL.md` | S1-01, S1-06 | **Low** | a-001 R-6 |

### Phase 3: Automation (Priority 3 -- Audit Infrastructure)

| ID | Action | Files to Create/Modify | Dependencies | Complexity | Traceability |
|----|--------|------------------------|--------------|------------|--------------|
| S1-10 | Add Content Quality audit phase (Phase 2.5) to wt-auditor agent definition | `skills/worktracker/agents/wt-auditor.md` | S1-01, S1-02 | **High** | a-001 Area 5 full specification |
| S1-11 | Add Quick Creation Guide to ENABLER.md template | `.context/templates/worktracker/ENABLER.md` | S1-01 | **Low** | a-001 R-9 |
| S1-12 | Add Quick Creation Guide to FEATURE.md template | `.context/templates/worktracker/FEATURE.md` | S1-01 | **Low** | a-001 R-9 |

### Phase 4: Polish (Priority 4 -- Reference Improvements)

| ID | Action | Files to Create/Modify | Dependencies | Complexity | Traceability |
|----|--------|------------------------|--------------|------------|--------------|
| S1-13 | Add `<!-- REFERENCE ONLY -->` markers to ontology sections in all templates | All `.context/templates/worktracker/*.md` | None | **Low** | a-001 R-10 |
| S1-14 | Update wt-auditor report format with Content Quality Issues section | `skills/worktracker/agents/wt-auditor.md` | S1-10 | **Low** | a-001 R-11 |

### Dependency Graph

```
Phase 1 (Foundation):
  S1-01 (WTI-007 rule) ──┬──> S1-02 (content-quality.md reference)
                          ├──> S1-03 (STORY guide)
                          ├──> S1-04 (BUG guide)
                          └──> S1-05 (TASK guide)

Phase 2 (Collaboration + DoD):
  S1-01 ──────────────────> S1-06 (WTI-008 rule)
  S1-07 (DOD.md) ─────────> S1-08 (STORY.md DoD reframe)
  S1-01 + S1-06 ──────────> S1-09 (SKILL.md update)

Phase 3 (Automation):
  S1-01 + S1-02 ──────────> S1-10 (wt-auditor Phase 2.5)
  S1-01 ──────────────────> S1-11 (ENABLER guide)
  S1-01 ──────────────────> S1-12 (FEATURE guide)

Phase 4 (Polish):
  S1-10 ──────────────────> S1-14 (audit report format)
  (no dependency) ────────> S1-13 (REFERENCE ONLY markers)
```

### Critical Path

```
S1-01 (WTI-007) -> S1-02 (content-quality.md) -> S1-03/04/05 (creation guides)
```

This critical path enables content quality enforcement from rules through templates. Everything else can proceed in parallel once S1-01 is complete.

### Effort Summary

| Phase | Items | Total Complexity | Estimated Effort |
|-------|-------|------------------|------------------|
| Phase 1 | 5 | 2 Medium + 3 Low | Primary effort |
| Phase 2 | 4 | 1 Medium + 3 Low | Secondary effort |
| Phase 3 | 3 | 1 High + 2 Low | Tertiary effort |
| Phase 4 | 2 | 2 Low | Minimal effort |
| **Total** | **14 items** | **3M + 1H + 10L** | |

---

## Sources

### Input Documents

| Document | Path | Role |
|----------|------|------|
| Research: AC Quality Best Practices | `c:\AI\jerry\projects\PROJ-005-jerry-process-improvements\research\proj-005-r-001-ac-quality-best-practices.md` | Industry best practices, academic frameworks, LLM quality findings |
| Analysis: Worktracker Gap Analysis | `c:\AI\jerry\projects\PROJ-005-jerry-process-improvements\research\proj-005-a-001-worktracker-gap-analysis.md` | Gap identification, rule proposals, detection patterns, template analysis |

### Key References Inherited from Inputs

| Reference | Source Document | Relevance to Synthesis |
|-----------|-----------------|------------------------|
| Quality User Story framework (Lucassen 2016) | r-001 | Foundation for AC quality criteria |
| Springer JIIS 2025 (LLM quality assessment) | r-001 | Evidence that explicit rubrics improve LLM evaluation |
| Diataxis framework | r-001 | Justification for creation guide architecture |
| Rubber-stamp risk (CyberManiacs) | r-001 | Risk mitigation for collaboration checkpoints |
| Autonomy levels (Tessl.io, Knight Columbia) | r-001 | Framework for checkpoint design |
| SPIDR splitting framework | r-001 | Scope overflow remediation approach |
| ADO Skill AC standards | a-001 | Source patterns for WTI-007 sub-rules |
| wt-auditor current specification | a-001 | Baseline for Phase 2.5 enhancement |
| User feedback document (2026-02-11) | a-001 | Requirements traceability for WTI-008 |

### Jerry Internal Files Referenced

| File | Purpose in Synthesis |
|------|---------------------|
| `skills/worktracker/rules/worktracker-behavior-rules.md` | Existing WTI-001 to WTI-006 (verified, lines 27-113) |
| `.context/templates/worktracker/STORY.md` | DoD section analysis (lines 289-313) |
| `.context/templates/worktracker/BUG.md` | Template effectiveness analysis |
| `.context/templates/worktracker/TASK.md` | Template effectiveness analysis |
| `skills/worktracker/agents/wt-auditor.md` | Current audit check types (lines 79-121) |
| `skills/worktracker/SKILL.md` | Skill definition requiring update |

---

*Synthesis completed: 2026-02-16*
*Agent: ps-synthesizer v2.0.0*
*PS ID: proj-005, Entry: s-001*
*Input documents: proj-005-r-001, proj-005-a-001*
