# C4 Adversarial Tournament Report: Diataxis Audit 2026-04-20 — Iteration 2

## Tournament Context

| Field | Value |
|-------|-------|
| Deliverable | `projects/PROJ-040-documentation/reports/diataxis-audit-20260420.md` |
| Criticality | C4 — OSS-release blocking, irreversible downstream impact |
| Quality Threshold | >= 0.95 (user-specified, above H-13 default of 0.92) |
| Strategies Executed | S-003, S-010, S-007, S-002, S-004, S-012, S-013, S-011, S-001 (9 of 10; S-014 by adv-scorer) |
| Tournament Date | 2026-04-17 |
| Iteration | 2 |
| Executor | adv-executor |
| H-16 Compliance | S-003 executed first; all critique strategies follow |

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Iteration 1 Blocker Resolution](#iteration-1-blocker-resolution) | Status of each iter-1 P0 blocker |
| [S-003 Steelman](#s-003-steelman-technique) | Strongest version of the revised audit |
| [S-010 Self-Refine](#s-010-self-refine) | Self-review of iteration 2 changes |
| [S-007 Constitutional AI Critique](#s-007-constitutional-ai-critique) | HARD rule and governance compliance |
| [S-002 Devil's Advocate](#s-002-devils-advocate) | Counter-arguments to iteration 2 fixes |
| [S-004 Pre-Mortem Analysis](#s-004-pre-mortem-analysis) | Failure scenarios for iter-2 audit |
| [S-012 FMEA](#s-012-fmea) | Component-level failure mode analysis |
| [S-013 Inversion Technique](#s-013-inversion-technique) | Assumption stress-testing of iter-2 changes |
| [S-011 Chain-of-Verification](#s-011-chain-of-verification) | Verification of new claims |
| [S-001 Red Team Analysis](#s-001-red-team-analysis) | Adversarial attack on iter-2 credibility |
| [Consolidated Weakness List](#consolidated-weakness-list) | All findings by severity |
| [Recommended Revisions](#recommended-revisions) | Prioritized, actionable guidance |
| [Tournament Verdict](#tournament-verdict) | Overall assessment |

---

## Iteration 1 Blocker Resolution

| Iter-1 Blocker | Resolution Status | Evidence |
|----------------|-------------------|---------|
| **Blocker 1: 26 vs. 15 skills discrepancy** | Partially Resolved — New Error Introduced | Scope reconciliation subsection added. "26" corrected to "15" throughout. BUT: Coverage Matrix has 16 N-rows (not 15); scope reconciliation text enumerates 16 skills by name while claiming "15." A new off-by-one error replaces the old discrepancy. |
| **Blocker 2: EV-012 arithmetic** | Resolved | EV-012 fully rewritten with exact glob command, 88-file count, AGENTS.md 82-baseline explained (6 new files added since March 9), net discrepancy of 1 correctly calculated. Clean and defensible. |
| **Blocker 3: Git evidence for UNCHANGED claims** | Partially Resolved — Internal Contradiction | Git evidence table provided for 8 files with commit hashes (lines 103-116). BUT: The Delta section footer (line 601) explicitly disclaims: "All status assertions above are based on content re-verification only. This audit cannot run git log." This directly contradicts line 103 which claims commit hashes came from parent Bash workflow. The audit cannot simultaneously claim git evidence and disclaim it. |
| **Blocker 4: ~unknown line counts** | Resolved | Actual line counts populated: problem-solving.md 233, orchestration.md ~263, transcript.md ~278, PLUGIN-DEVELOPMENT.md ~429. Independently verifiable. |
| **Blocker 5/6: EV-019 through EV-025 with verbatim quotes; full 7/7 criterion evaluation for playbooks and AGENTS.md** | Resolved (with minor location error) | EV-019 through EV-025 added with direct quotes. Full H-01 through H-07 evaluation for all four playbooks; R-01 through R-07 for AGENTS.md. EV-024 cites wrong line numbers (25-31 vs actual 74-84) but the finding conclusion is correct. |

**Summary:** 2 of 6 blockers fully resolved (Blockers 2 and 4). 3 partially resolved with new issues (Blockers 1, 3, 5/6). 1 secondary (Blocker 6 subsumed into 5).

---

## S-003 Steelman Technique

**Finding Prefix:** SM | **H-16 Status:** This is the first strategy (H-16 satisfied)

### Steelman Assessment

Iteration 2 represents genuine, substantive revision. The document is materially better than iteration 1. The EV-012 rewrite is exemplary: it explains the 82 vs 87 vs 88 vs 89 agent count puzzle cleanly, identifies the 39-day gap as the likely source of the 82-to-88 change, and correctly calculates the remaining discrepancy as 1. The full 7/7 playbook criterion evaluations are real evaluations — EV-019 through EV-025 quote actual file content that I independently verified. The denominator justification note for UX sub-skills is the right answer to DA-001. The effort estimate footnote addresses DA-003 substantively.

### Strongest Version of the Audit's Arguments

**SM-001 (Preserved strength): The worsening trajectory finding is now more defensible.** The Delta section now shows the coverage percentage decline from 27% to 17% with the corrected denominator (15 P skills at PROJ-015, 30 total now). The framing — "15 new skills added with zero documentation while remediation backlog grew" — is the audit's strongest argument and survived revision intact.

**SM-002 (New strength): EV-012 is now the strongest evidence entry in the document.** The iteration 2 rewrite of EV-012 resolves what was the single most embarrassing factual error. It now explains: audit glob = 88 files; AGENTS.md baseline count = 82 (from March 9); 6 new files added since; AGENTS.md per-skill sum = 89; net discrepancy = 1. This is precisely the level of rigor the document needed.

**SM-003 (New strength): Full playbook criterion tables are genuinely useful.** The H-04 finding for transcript.md (EV-024) and orchestration.md (EV-022), the H-07 reference table findings (EV-020, EV-025), and the AGENTS.md R-02 finding all provide direct quotes that a writer can act on. The playbook section is now substantively better.

**SM-004 (Preserved strength): The [GIT-CONFIRMED] tags with commit hashes are the right approach.** Even if the implementation has gaps, providing specific hashes and dates in the Git Verification Evidence table is the correct mechanism. The UNCHANGED claims for the 8 listed files are backed by specific, independently verifiable commit hashes and dates. A downstream user can run `git show 7bfbcb16` to confirm.

**SM-005 (Minor): The denominator justification note is correct.** The rationale for treating 10 UX sub-skills as 10 separate documentation gaps — "each sub-skill has its own SKILL.md, its own agent, and is invoked independently" — is a sound methodological choice. The note citing the two coverage percentages (19% vs 13%) makes the choice transparent.

---

## S-010 Self-Refine

**Finding Prefix:** SR

### Objectivity Assessment

The revision log is accurate about what changed. The audit does not overclaim resolution of issues that are only partially resolved. The new issues introduced (16 vs 15 N-skill count, git evidence contradiction) appear to be genuine oversights rather than deliberate misrepresentation.

### Self-Review Findings

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| SR-001 | New off-by-one error: Coverage Matrix has 16 N-rows; scope reconciliation claims "15" and enumerates 16 skills | Critical | Scope reconciliation line 89: enumerated list = contract-design, diataxis, prompt-engineering, test-spec, use-case, user-experience, ux-ai-first-design, ux-atomic-design, ux-behavior-design, ux-design-sprint, ux-heart-metrics, ux-heuristic-eval, ux-inclusive-design, ux-jtbd, ux-kano-model, ux-lean-ux = 16 skills. Coverage Matrix shows 16 N-rows. Yet text says "exactly 15 skills as (N)." The word "exactly" makes this error worse. | Internal Consistency |
| SR-002 | Direct internal contradiction on git evidence: line 103 states hashes obtained via Bash; line 601 states "cannot run git log" and all assertions are content-re-verification only | Critical | Methodology § Git Verification Evidence line 103: "Git evidence was obtained by the parent workflow via Bash and is reproduced below." Delta § footer line 601: "All status assertions above are based on content re-verification only. This audit cannot run `git log` to confirm..." These two statements are mutually exclusive. | Internal Consistency |
| SR-003 | [GIT-CONFIRMED] applied to 2 non-file items in Delta table | Major | Delta table rows: "Create docs/explanation/context-architecture.md" and "Create Jerry CLI Reference document" both tagged [GIT-CONFIRMED]. These are non-existent files. A git log command on a non-existent path returns empty output; empty output confirms only that the file was never committed, not that it was "unchanged." The [GIT-CONFIRMED] tag implies the same evidence quality as confirmed file staleness, which is misleading. | Evidence Quality |
| SR-004 | Cascading error: Delta table states "15 skills marked P" in PROJ-015 column, but Coverage Matrix shows 14 P-rows and 16 N-rows (not 15P/15N) | Major | Delta section line 567: "Skills with SKILL.md | 15 (per Coverage Matrix: 15 skills marked P) | 30 | +15." Count of P rows in Coverage Matrix: adversary, architecture, ast, bootstrap, eng-team, nasa-se, orchestration, pm-pmm, problem-solving, red-team, saucer-boy-framework-voice, saucer-boy, transcript, worktracker = 14 P skills. Delta says 15. | Internal Consistency |
| SR-005 | EV-024 location error: cites "Lines 25-31 introductory blockquote" for transcript.md H-04 finding; actual H-04 content is at lines 74-84 | Major | EV-024: "docs/playbooks/transcript.md:25-31 — H-04 teaching content (introductory blockquote): 'The transcript skill uses a hybrid Python+LLM architecture...'" — but lines 25-31 of transcript.md are the "When to Use > Invocation" section, not before any steps. The H-04 teaching content with cost rationale appears at lines 74-84 in the Step-by-Step section. The conclusion (H-04 violation exists) is correct; the evidence location is wrong. | Evidence Quality |
| SR-006 | How-to coverage percentage changed from prior iteration without explanation: iter-1 stated 27% (4/15); iter-2 states 27% (4/15 skills at PROJ-015) and 17% (5/30 current) — but Coverage Summary states "17% (partial only)" for how-to. The Prior Coverage figure changed mid-document | Minor | Coverage Summary table: How-To = 5/30 = 17%. Delta table: PROJ-015 How-To = 4/15 = 27%, current = 5/30 = 17%. Executive Summary trajectory note (line 615): "~27% to ~17%." Consistent. Minor: this is actually correct in iter-2. Flag resolved. | Evidence Quality |
| SR-007 | Document 15 (AGENTS.md) line count given as "~200+" without specific count; all other documents have specific counts | Minor | Current-State Inventory row 15: "~200+" — auditor read to line 80+ but document continues. A specific line count should be obtainable via direct read. | Completeness |

### Decision: NOT ready for downstream use without SR-001 and SR-002 resolution

---

## S-007 Constitutional AI Critique

**Finding Prefix:** CC

### Applicable Principles

P-001 (Truth/Accuracy), P-022 (No Deception), P-011 (Evidence-Based assertions), H-23 (navigation table).

### Findings

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001 | P-001 (Truth/Accuracy) / P-022 (No Deception) | HARD | Critical | The scope reconciliation text states "The Coverage Matrix marks exactly 15 skills as (N)" — the word "exactly" asserts precision. The Coverage Matrix contains 16 N-rows (verified by count). The scope reconciliation enumeration itself lists 16 skills. The iteration-2 fix introduced a new factual error that is arguably worse than the original 26 vs 15 discrepancy: it is now a self-contradicting authoritative claim within 3 sentences of the named evidence. | Internal Consistency |
| CC-002 | P-022 (No Deception) | HARD | Critical | The Methodology section (line 103) states "Git evidence was obtained by the parent workflow via Bash and is reproduced below." The Delta section footer (line 601) states "All status assertions above are based on content re-verification only. This audit cannot run `git log` to confirm whether any of these files were touched and reverted." These statements cannot both be true. One section tells readers the hashes are Bash-confirmed; another tells readers git confirmation was not performed. Readers cannot determine which statement to trust. This is a P-022 violation. | Internal Consistency |
| CC-003 | P-011 (Evidence-Based) | HARD | Major | [GIT-CONFIRMED] is applied to the Delta table entries "Create docs/explanation/context-architecture.md" and "Create Jerry CLI Reference document." These are non-existent files. The git evidence table (8 files) does not include these items. The [GIT-CONFIRMED] tag implies git-verified evidence exists; none does for non-existent files. Evidence-based standard requires the tag to match the actual evidence available. | Evidence Quality |
| CC-004 | P-001 (Truth/Accuracy) | HARD | Major | The Delta table states "Skills with SKILL.md | 15 (per Coverage Matrix: 15 skills marked P)" but the Coverage Matrix shows 14 P rows (adversary, architecture, ast, bootstrap, eng-team, nasa-se, orchestration, pm-pmm, problem-solving, red-team, saucer-boy-framework-voice, saucer-boy, transcript, worktracker). Counting P-rows: 14. This means the PROJ-015 baseline figure is overstated by 1, causing the "+15" delta to be wrong as well (actual delta is +16 skills, not +15). | Internal Consistency |
| CC-005 | H-23 (Navigation table) | HARD | Minor | Navigation table present and functional. PASS — no violation. | N/A |

**Constitutional Compliance Score:** 1.00 - (0.10×2 + 0.05×2 + 0.02×0) = 1.00 - 0.30 = 0.70 → REJECTED

*Note: iteration 1 constitutional score was 0.58 (two critical violations at -0.10 each, two major at -0.05 each). Iteration 2 improves to 0.70 (two critical remain at -0.10 each, two new major replacing old ones at -0.05 each). Still REJECTED.*

---

## S-002 Devil's Advocate

**Finding Prefix:** DA | **H-16:** S-003 completed (satisfied)

### Role Assumption

Arguing against the iteration 2 fixes: the scope reconciliation made things worse, the git evidence is fabricated or contradicted, the playbook evaluations have the wrong line numbers.

### Findings

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001 | The scope reconciliation replaced a provably-wrong "26" with a provably-wrong "15" — and anchored it with the word "exactly" | Critical | Scope reconciliation (line 89): "The Coverage Matrix marks exactly 15 skills as (N)." Anyone who counts the N-rows in the same Coverage Matrix finds 16. Anyone who counts the names in the enumeration in the same paragraph finds 16. The iteration-2 fix created a self-refuting authoritative claim more embarrassing than the original vague "26 vs 15" discrepancy. | Internal Consistency |
| DA-002 | The git evidence table appears to contain fabricated data | Major | The git hashes (7bfbcb16, baec6816, 016fa573, etc.) appear only in the audit document itself — the grep across the entire repository returns only the audit file. A real "parent workflow via Bash" would have left these hashes in a workflow log or separate output file. The Delta footer's disclaimer (line 601) further undermines the table: after claiming Bash-provided evidence, the audit disclaims git confirmation entirely. This creates doubt about whether the hashes were actually run or were constructed. | Evidence Quality |
| DA-003 | EV-024 cites the wrong section of transcript.md for H-04 | Major | EV-024 locates H-04 teaching content at "lines 25-31 introductory blockquote" but those lines are in the "When to Use > Invocation" section — a legitimate "When to Use" explanation, not teaching content embedded in steps. The actual H-04 violation (teaching content inside how-to steps) is at lines 74-84 in the "Step-by-Step" section. The playbook H-04 finding for Document 13 is located at the wrong place; a writer acting on EV-024 would remove "When to Use" context that is arguably appropriate for a playbook. | Evidence Quality |
| DA-004 | EV-022 truncates the line range: "lines 57-65" for orchestration.md Workflow Patterns, but the section runs from line 57 to line 131 | Minor | EV-022: "docs/playbooks/orchestration.md:57-65." The Workflow Patterns section starts at line 57 and continues through line 131 (three patterns with ASCII diagrams). Citing only lines 57-65 understates the extent of the H-04 violation and would cause an editor to truncate insufficiently. | Evidence Quality |
| DA-005 | The document continues to use "~" approximations for line counts on some documents (Documents 4, 5, 6, 12, 13, 14, 15) despite the revision log claiming these were verified | Minor | Current-State Inventory: INSTALLATION.md "~450", BOOTSTRAP.md "~175", CLAUDE-MD-GUIDE.md "~90", getting-started.md "~200", orchestration.md "~263", transcript.md "~278", PLUGIN-DEVELOPMENT.md "~429", AGENTS.md "~200+". Only problem-solving.md (233) has an exact count. The revision log claims "~unknown" was replaced with verified counts for Documents 11-14, which is accurate — but the inherited approximations for Documents 3-6 and 15 were not addressed. | Completeness |

---

## S-004 Pre-Mortem Analysis

**Finding Prefix:** PM | **H-16:** S-003 completed (satisfied)

### Failure Declaration

It is November 2026. The documentation sprint based on this audit has completed. A post-release review discovers the scope reconciliation was wrong: the Coverage Matrix lists 16 new skills, but all downstream planning used "15." One skill (ux-lean-ux or another) received no documentation because the planning assumed 15 needed docs and 15 were created. Additionally, a senior reviewer ran `git show 7bfbcb16` and could not find the commit in the repository's git history, casting doubt on all git evidence in the audit.

### Failure Causes

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001 | Writers plan for 15 new-skill documentation items; Coverage Matrix actually shows 16 N-skills; one skill receives no documentation | Scope | High | Critical | P0 | Internal Consistency |
| PM-002 | A reviewer verifies git hashes cited in the audit against the actual git log; some hashes are not found; all git-based "UNCHANGED" claims become suspect; auditor credibility collapses | Evidence | Medium | Critical | P0 | Evidence Quality |
| PM-003 | The Delta table's "+15 skills" figure is wrong (actual +16); any downstream metrics tracking based on this figure produces incorrect baseline comparisons | Data Integrity | High | Major | P1 | Internal Consistency |
| PM-004 | An EV-024-based edit to transcript.md removes the "When to Use" invocation blockquote that is actually useful documentation; the document becomes less helpful while the actual H-04 violation (lines 74-84) remains | Misfire | Medium | Major | P1 | Actionability |
| PM-005 | The git disclaimer at line 601 contradicts the git evidence table; legal/compliance reviewers who read the full document flag the contradiction as evidence of poor audit quality; the audit's authority as the OSS-release gate document is challenged | Credibility | Low | Major | P1 | Internal Consistency |
| PM-006 | The 14 P vs 15 P discrepancy causes a documentation planning team to over-allocate resources to "existing skill" documentation and under-allocate to "new skill" documentation by one skill | Resource | Medium | Minor | P2 | Actionability |

### Mitigations

**P0:** PM-001 — Count N-rows in Coverage Matrix, count names in scope reconciliation enumeration, reconcile to single number. If 16 is correct, update all "15 new skills" references throughout. PM-002 — Either verify the cited git hashes against actual git history and correct any that do not exist, or remove the hash table and restate as "content-based UNCHANGED assertion (git verification not performed)." Do not claim both simultaneously.

**P1:** PM-003 — Correct the Delta table PROJ-015 baseline to 14 P skills (not 15); correct the delta to +16 (not +15). PM-004 — Correct EV-024 to cite lines 74-84 of transcript.md, not 25-31. PM-005 — Remove the line-601 disclaimer or reconcile it with the git evidence table header.

---

## S-012 FMEA

**Finding Prefix:** FM

### Element Decomposition (Iteration 2 Focus)

Analysis focuses on elements changed in iteration 2 and regression risk to elements that passed in iteration 1.

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|---------------------|
| FM-001 | Scope Reconciliation (new section) | "Exactly 15 (N)" stated; Coverage Matrix has 16 N-rows; enumerated list has 16 names; document is internally self-refuting within one paragraph | 9 | 10 | 3 | 270 | Critical | Internal Consistency |
| FM-002 | Git Verification Evidence table vs. Delta footer disclaimer | Two sections directly contradict each other on whether git evidence was obtained; readers cannot determine which is authoritative | 8 | 10 | 4 | 320 | Critical | Internal Consistency |
| FM-003 | [GIT-CONFIRMED] tag on non-existent files in Delta table | Two "NOT DONE" items tagged [GIT-CONFIRMED] but refer to files that do not exist; the tag misleads about evidence quality | 7 | 10 | 5 | 350 | Critical | Evidence Quality |
| FM-004 | EV-024 wrong line citation for transcript.md H-04 | H-04 finding cites "lines 25-31 introductory blockquote" — wrong section; actual violation is lines 74-84 | 6 | 10 | 4 | 240 | Critical | Evidence Quality |
| FM-005 | Delta baseline count (15 P, +15 delta) | 14 P skills in Coverage Matrix; Delta claims 15; delta should be +16 | 6 | 10 | 5 | 300 | Critical | Internal Consistency |
| FM-006 | EV-022 truncated line range (57-65 vs. 57-131) | Orchestration Workflow Patterns section spans 75 lines; citing only 9 understates the violation | 4 | 10 | 6 | 240 | Major | Evidence Quality |
| FM-007 | AGENTS.md line count "~200+" | Document 15 has no specific line count despite revision targeting line counts | 3 | 10 | 8 | 240 | Minor | Completeness |
| FM-008 | Inherited ~-approximations for Documents 3-6 line counts | INSTALLATION.md ~450, BOOTSTRAP.md ~175, CLAUDE-MD-GUIDE.md ~90, getting-started.md ~200 — these were in scope but not fixed | 3 | 8 | 7 | 168 | Minor | Completeness |

**Resolved failure modes (iteration 1 → iteration 2):**
- FM-002 (iter-1): EV-012 arithmetic error — RESOLVED. New EV-012 is correct and well-reasoned.
- FM-003 (iter-1): "~unknown" line counts — RESOLVED for Documents 11-14.
- FM-004 (iter-1): "UNCHANGED" without git evidence — PARTIALLY RESOLVED (8 files have evidence; contradiction with disclaimer; non-file items tagged incorrectly).
- FM-005 (iter-1): Playbook abbreviated evaluation — RESOLVED. Full H-01 through H-07 and R-01 through R-07 complete.

**Highest-risk element (iter-2):** Scope Reconciliation section — it is the single new section added to fix the audit's most visible prior error; it now contains a new self-refuting claim that is the first thing a reviewer checking the fix will encounter.

**Total identified RPN (iter-2 new/modified findings):** 1,928 across 8 items

---

## S-013 Inversion Technique

**Finding Prefix:** IN | **H-16:** S-003 completed (satisfied)

### Goals Statement (Iteration 2)

The iteration 2 revision's goals: (1) Resolve the 26 vs. 15 skills discrepancy with an authoritative reconciliation. (2) Provide verifiable git evidence for UNCHANGED claims. (3) Populate actual line counts. (4) Complete full criterion evaluations for all documents. (5) Add verbatim quotes for all playbook findings.

### Anti-Goals (Inversion)

**To guarantee iteration 2 fails its goals:**
- Add a reconciliation section that states "exactly 15 (N)" while the Coverage Matrix and the section's own enumerated list show 16
- Add git evidence in one section while disclaiming git capability in another section of the same document
- Apply a [GIT-CONFIRMED] tag to items that could not have git evidence because they don't exist as files
- Fix the H-04 finding for transcript.md but cite the wrong section with the wrong line numbers
- Correct the PROJ-015 baseline skill count to "15 P skills" when the Coverage Matrix shows 14 P rows

Four of the five anti-goals are present in iteration 2.

### Assumption Stress-Test (Iteration 2 Changes)

| ID | Assumption | Inversion | Severity | Affected Dimension |
|----|------------|-----------|----------|--------------------|
| IN-001 | "The Coverage Matrix marks exactly 15 skills as (N)" | Wrong: both the N-row count (16) and the enumerated list (16 names) contradict this | Critical | Internal Consistency |
| IN-002 | The git hashes in the Git Verification Evidence table are real commits that exist in the repository | Unverifiable with read-only tools; no hashes found anywhere except inside the audit document itself; Delta footer disclaimer suggests they may be content-based assertions only | Major | Evidence Quality |
| IN-003 | [GIT-CONFIRMED] in the Delta table means git evidence was obtained | Wrong for at least 2 items (non-existent files); possibly wrong for items not in the 8-file git evidence table | Major | Evidence Quality |
| IN-004 | EV-024's "lines 25-31" is the correct location for transcript.md's H-04 violation | Wrong: lines 25-31 are the "When to Use > Invocation" blockquote; H-04 violation (teaching inside steps) is at lines 74-84 | Major | Evidence Quality |
| IN-005 | The "+15" skills delta in the Delta table is correct | Wrong: 16 N skills in Coverage Matrix; PROJ-015 had 14 P skills; delta = +16 not +15 | Major | Internal Consistency |
| IN-006 | The scope reconciliation fix improved the document's accuracy | Paradoxically wrong: the fix introduced a new, more precise factual error ("exactly 15") that is immediately falsifiable from the same section of the same document | Critical | Internal Consistency |

---

## S-011 Chain-of-Verification

**Finding Prefix:** CV

### New Claims Introduced in Iteration 2

| Claim ID | Claim | Source |
|----------|-------|--------|
| CL-101 | "Coverage Matrix marks exactly 15 skills as (N)" | Scope Reconciliation, line 89 |
| CL-102 | Git evidence for 8 files: "7bfbcb16 / 2026-02-25" for INSTALLATION.md | Git Verification Evidence table, line 107 |
| CL-103 | "88 files found" via filesystem glob (EV-012 revision) | EV-012 |
| CL-104 | "AGENTS.md per-skill sum = 89; current filesystem count = 88; Net discrepancy: 1" | EV-012 |
| CL-105 | "Skills with SKILL.md | 15 (per Coverage Matrix: 15 skills marked P)" | Delta table, line 567 |
| CL-106 | EV-024 transcript.md H-04 evidence at "lines 25-31" | EV-024 |
| CL-107 | EV-019 problem-solving.md H-04 evidence at "lines 141-148" | EV-019 |
| CL-108 | EV-020 problem-solving.md H-07 evidence at "lines 90-113" | EV-020 |

### Independent Verification Results

| ID | Claim | Verification Method | Result | Discrepancy |
|----|-------|---------------------|--------|-------------|
| CV-101 | CL-101: "exactly 15 skills as (N)" | Count N-rows in Coverage Matrix; count names in scope reconciliation enumeration | MATERIAL DISCREPANCY | Coverage Matrix N-rows: contract-design, diataxis, prompt-engineering, test-spec, use-case, user-experience, ux-ai-first-design, ux-atomic-design, ux-behavior-design, ux-design-sprint, ux-heart-metrics, ux-heuristic-eval, ux-inclusive-design, ux-jtbd, ux-kano-model, ux-lean-ux = 16. Scope reconciliation enumeration in the same paragraph also lists 16 names. The claim of "exactly 15" is falsified by two sources within the same page. |
| CV-102 | CL-102: Git hash 7bfbcb16 / 2026-02-25 for INSTALLATION.md | Grep for hash string across full repository | UNVERIFIABLE | Hash string found only in the audit document (diataxis-audit-20260420.md). No other file in the repository references this hash. Cannot confirm it is a real commit. Delta footer disclaimer further undermines reliability. |
| CV-103 | CL-103: 88 files via filesystem glob | Count results of `skills/*/agents/*.md` glob | VERIFIED | Glob returns 88 .md files in skills/*/agents/ directories. EV-012's "88 files" is correct. |
| CV-104 | CL-104: Per-skill sum = 89; filesystem = 88; discrepancy = 1 | AGENTS.md line 68: total = 89. Filesystem = 88. | VERIFIED | AGENTS.md Agent Summary table per-skill sum: 9+10+3+3+3+5+3+1+10+11+5+6+3+11+2+2+2 = 89. Filesystem = 88. Discrepancy = 1. EV-012 analysis is accurate. |
| CV-105 | CL-105: "15 skills marked P" in Coverage Matrix | Count P-rows in Coverage Matrix | MATERIAL DISCREPANCY | P-rows: adversary, architecture, ast, bootstrap, eng-team, nasa-se, orchestration, pm-pmm, problem-solving, red-team, saucer-boy-framework-voice, saucer-boy, transcript, worktracker = 14 P-rows. Delta claims 15 P. Off-by-one in the same direction as the N-count error. Total skills = 14 P + 16 N = 30. Check: 14+16=30. Confirmed. |
| CV-106 | CL-106: transcript.md H-04 content at "lines 25-31" | Read transcript.md lines 23-35 | MATERIAL DISCREPANCY | Lines 24-31 are the "When to Use > Invocation" blockquote (explaining how the skill is triggered). The actual H-04 teaching content (two-phase architecture with cost rationale) is at lines 74-84 in the Step-by-Step section. Audit cites wrong location. |
| CV-107 | CL-107: problem-solving.md H-04 content at "lines 141-148" | Read problem-solving.md lines 141-150 | VERIFIED | Lines 141-148 begin "For C2+ deliverables...minimum 3-iteration creator-critic-revision cycle per H-14" and "An agent produces a deliverable, then another pass critiques it and provides a quality score." This is teaching content. Citation is correct. |
| CV-108 | CL-108: problem-solving.md H-07 Agent Reference table at "lines 90-113" | Read problem-solving.md lines 90-114 | VERIFIED | Lines 90-113 contain the "Agent Reference" section with 9-agent table (Agent/Role/Invoke When You Need/Output Location columns). Citation is correct. |

### Summary

4 VERIFIED, 3 MATERIAL DISCREPANCY, 1 UNVERIFIABLE out of 8 new claims.

**New material discrepancies:**

| ID | Claim | Severity | Correction Needed |
|----|-------|----------|-------------------|
| CV-101 | "exactly 15 skills as (N)" | Critical | Count N-rows and names: both show 16. Correct to "16 new skills" throughout. This affects Executive Summary, Scope Reconciliation, Coverage Matrix description, Delta table, Net Trajectory paragraph, and New Gaps table. |
| CV-105 | "15 skills marked P" in Delta table | Major | Count P-rows: 14. Correct PROJ-015 baseline to 14 and delta to +16. |
| CV-106 | EV-024 lines 25-31 | Major | Correct to lines 74-84; update evidence description to "Step-by-Step Primary Path section opening paragraph explains two-phase architecture with cost rationale." |

---

## S-001 Red Team Analysis

**Finding Prefix:** RT | **H-16:** S-003 completed (satisfied)

### Threat Actor Profile

**Goal:** Identify weaknesses that would cause a technical reviewer checking iteration 2's claimed fixes to reject it as insufficiently improved.

**Capability:** Full access to codebase, git history (or absence thereof), ability to count rows in tables, ability to verify quotes against source files.

### Attack Vectors (Iteration 2)

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-------------------|
| RT-101 | The scope reconciliation fix is self-refuting: adversary counts N-rows (16) and names (16) in the exact section that claims "exactly 15" | Inconsistency | High | Critical | P0 | Missing | Internal Consistency |
| RT-102 | Git evidence table and Delta footer disclaimer contradict: adversary quotes both passages side-by-side and asks "which one is true?" — there is no answer that doesn't impugn one section | Contradiction | High | Critical | P0 | Missing | Internal Consistency |
| RT-103 | Git hashes are not findable anywhere in the git repository except inside the audit; adversary attempts `git show 7bfbcb16` — if hash doesn't exist in repository, the entire git evidence table is invalidated | Dependency attack | High | Critical | P0 | Missing | Evidence Quality |
| RT-104 | EV-024 wrong location: adversary navigates to lines 25-31 of transcript.md and finds "When to Use > Invocation" blockquote — not the H-04 violation the audit describes; adversary questions auditor's competence | Location error | High | Major | P1 | Missing | Evidence Quality |
| RT-105 | Delta table baseline error (15 P vs 14 P): adversary counts P-rows (14), finds Delta claims 15; combined with N-count error (16 not 15) this creates a numerically incoherent skills accounting | Arithmetic | High | Major | P1 | Missing | Internal Consistency |
| RT-106 | [GIT-CONFIRMED] on non-existent files: adversary notes that "Create docs/explanation/context-architecture.md" is tagged [GIT-CONFIRMED] — a file that doesn't exist cannot have git confirmation it was unchanged; adversary challenges the evidentiary value of [GIT-CONFIRMED] across all 10 Delta items | Semantic abuse | Medium | Major | P1 | Missing | Evidence Quality |

### Defense Gap Assessment

**P0 Attacks (RT-101, RT-102, RT-103):** All three have MISSING defenses. These are immediately exploitable by any reviewer who checks the specific claims.

**P1 Attacks (RT-104, RT-105, RT-106):** All three have MISSING defenses.

---

## Consolidated Weakness List

### Critical Findings (Iteration 2)

| ID | Strategy | Finding | Section |
|----|----------|---------|---------|
| SR-001 | S-010 | Coverage Matrix has 16 N-rows; scope reconciliation enumerates 16 names; text claims "exactly 15" — self-refuting within same section | Scope Reconciliation |
| SR-002 | S-010 | Line 103 claims git evidence via Bash; line 601 disclaims git capability — direct internal contradiction | Methodology vs. Delta |
| CC-001 | S-007 | P-001/P-022: "exactly 15 (N)" is verifiably false from same-page evidence; word "exactly" intensifies the error | Scope Reconciliation |
| CC-002 | S-007 | P-022: Two sections contradict on whether git evidence was obtained; readers cannot determine which to trust | Methodology + Delta |
| FM-001 | S-012 | "Exactly 15 (N)" self-refutes in its own paragraph, RPN 270 | Scope Reconciliation |
| FM-002 | S-012 | Git evidence / disclaimer contradiction, RPN 320 | Methodology + Delta |
| FM-003 | S-012 | [GIT-CONFIRMED] on non-existent files, RPN 350 | Delta Table |
| FM-005 | S-012 | Delta baseline 15 P vs. actual 14 P; delta +15 vs. actual +16, RPN 300 | Delta Section |
| CV-101 | S-011 | "Exactly 15 (N)" falsified: Coverage Matrix + scope reconciliation enumeration both show 16 | Scope Reconciliation |
| IN-001 | S-013 | Scope reconciliation assumption instantly falsified by same-document evidence | Scope Reconciliation |
| IN-006 | S-013 | The fix itself introduced a more precise, more immediately falsifiable error | Scope Reconciliation |
| RT-101 | S-001 | Self-refuting scope reconciliation is exploitable by any reviewer who counts rows | Scope Reconciliation |
| RT-102 | S-001 | Git evidence / disclaimer contradiction immediately exploitable | Methodology + Delta |
| RT-103 | S-001 | Git hashes may not exist in repository history; [GIT-CONFIRMED] is unverifiable | Git Evidence Table |
| PM-001 | S-004 | Writers plan for 15 new-skill docs; 16 needed; one skill will be undocumented | Scope Reconciliation |
| PM-002 | S-004 | Git hash verification failure would collapse all UNCHANGED claims | Git Evidence Table |

### Major Findings (Iteration 2)

| ID | Strategy | Finding | Section |
|----|----------|---------|---------|
| SR-003 | S-010 | [GIT-CONFIRMED] applied to 2 non-existent files in Delta table | Delta Table |
| SR-004 | S-010 | Delta table "15 P" vs. actual 14 P; +15 vs. +16 | Delta Section |
| SR-005 | S-010 | EV-024 cites wrong lines (25-31 vs. 74-84) for transcript.md H-04 | Evidence Log |
| CC-003 | S-007 | P-011: [GIT-CONFIRMED] on non-existent files without matching git evidence | Delta Table |
| CC-004 | S-007 | P-001: Delta baseline 15 P overstated by 1; cascades through delta calculations | Delta Section |
| FM-004 | S-012 | EV-024 wrong line citation (25-31 vs. 74-84), RPN 240 | Evidence Log |
| FM-006 | S-012 | EV-022 truncated line range (57-65 vs. 57-131), RPN 240 | Evidence Log |
| CV-105 | S-011 | "15 P skills" in Delta falsified: Coverage Matrix shows 14 P | Delta Section |
| CV-106 | S-011 | EV-024 lines 25-31 is wrong section of transcript.md | Evidence Log |
| DA-001 | S-002 | Scope reconciliation replaced "26" with "exactly 15" — still wrong and now more precisely wrong | Scope Reconciliation |
| DA-002 | S-002 | Git hashes found only in audit document — not independently verifiable | Git Evidence Table |
| DA-003 | S-002 | EV-024 wrong location will cause misfire edit to transcript.md "When to Use" section | Evidence Log |
| IN-002 | S-013 | Git hashes unverifiable outside the audit document | Git Evidence Table |
| IN-003 | S-013 | [GIT-CONFIRMED] tag does not represent consistent evidence quality for all tagged items | Delta Table |
| IN-004 | S-013 | EV-024 wrong lines leads writer to wrong section | Evidence Log |
| IN-005 | S-013 | "+15 delta" wrong; +16 is correct | Delta Section |
| PM-003 | S-004 | "+15" delta figure will produce incorrect baseline comparisons | Delta Section |
| PM-004 | S-004 | EV-024 misfire will damage transcript.md by removing useful content | Evidence Log |
| RT-104 | S-001 | EV-024 wrong location exploitable by reviewer who reads transcript.md | Evidence Log |
| RT-105 | S-001 | 15 P vs. 14 P error immediately verifiable from same document | Delta Section |
| RT-106 | S-001 | [GIT-CONFIRMED] on non-existent files challenges all [GIT-CONFIRMED] tags | Delta Table |

### Minor Findings (Iteration 2)

| ID | Strategy | Finding | Section |
|----|----------|---------|---------|
| SR-006 | S-010 | AGENTS.md line count "~200+" still approximate | Current-State Inventory |
| SR-007 | S-010 | Coverage percentage note: iter-2 trajectory phrasing switched from "~20% to ~13%" to "~27% to ~17%" — both may be cited; pick one and use it consistently | Exec Summary vs Delta |
| DA-004 | S-002 | EV-022 line range truncated at 65 vs. 131 | Evidence Log |
| DA-005 | S-002 | ~-approximation line counts inherited for Documents 3-6, 15 | Current-State Inventory |
| FM-007 | S-012 | AGENTS.md line count "~200+" unresolved, RPN 240 | Current-State Inventory |
| FM-008 | S-012 | Documents 3-6 inherited ~-approximations not addressed, RPN 168 | Current-State Inventory |
| SM-003 | S-003 | Trajectory note: iter-2 uses "~27% to ~17%" while exec summary history note says "~20% to ~13%"; reconcile to single framing | Delta |

---

## Recommended Revisions

### P0 — Must fix before the audit can serve as a foundation document (blocking)

**R2-001 (Resolves: SR-001, CC-001, CV-101, FM-001, RT-101, IN-001, IN-006, PM-001, DA-001)**

The "exactly 15 (N)" error in the Scope Reconciliation section is the highest-priority fix. In the same paragraph, the enumeration lists 16 skills by name. Count the names, count the N-rows: both are 16. Update the Scope Reconciliation text to say "exactly 16 skills as (N)." Update all downstream references: Executive Summary ("The 15 new skills" → "The 16 new skills"), Delta table PROJ-015 baseline (14 P, not 15; delta = +16 not +15), Net trajectory paragraph, New Gaps table. The Coverage Summary statement "4/30 skills (13%)" uses 30 as denominator throughout and is unaffected.

*Specific corrections:*
- Line 89: "exactly 15 skills as (N)" → "exactly 16 skills as (N)"
- Line 91: "The 15 (P) skills in the Coverage Matrix" → "The 14 (P) skills in the Coverage Matrix"
- Line 93: "15 new skills" → "16 new skills"
- Line 33 (Executive Summary): "The 15 skills added since PROJ-015 baseline" → "The 16 skills added since PROJ-015 baseline"
- Line 567 (Delta): "15 (per Coverage Matrix: 15 skills marked P)" → "14 (per Coverage Matrix: 14 skills marked P)"
- Line 570: "4/15 skills (27%)" → "4/14 skills (29%)" for PROJ-015 how-to rate
- Line 609: "15 new skills (N in coverage matrix)" → "16 new skills (N in coverage matrix)"
- Line 615: "15 new skills were added" → "16 new skills were added"
- Also update Revision Log entry (line 47): "corrected '26 skills' to '15 new skills'" → "corrected '26 skills' to '16 new skills'"

**R2-002 (Resolves: SR-002, CC-002, FM-002, RT-102, RT-103, PM-002, DA-002, IN-002)**

The git evidence contradiction must be resolved. Two options:

*Option A (Preferred):* Keep the git evidence table and remove the line-601 disclaimer. State the hashes are from the parent workflow. Add a note: "To verify: `git show <hash> --oneline`" so readers can confirm independently.

*Option B:* Remove the git evidence table and the Methodology section header claim "Git evidence obtained by parent workflow via Bash." Replace with: "The following files were content-verified as UNCHANGED (the audit confirmed the failing content is present unchanged). Independent git verification can be performed with: `git log --since='2026-03-02' --oneline -- <path>`. This audit did not execute git commands directly."

Either option is acceptable. Do NOT keep both the table-with-hashes and the disclaimer that git cannot be run — these are mutually exclusive claims.

**R2-003 (Resolves: SR-003, CC-003, FM-003, RT-106, IN-003)**

Remove [GIT-CONFIRMED] from the two "create" items in the Delta table ("Create docs/explanation/context-architecture.md" and "Create Jerry CLI Reference document"). Replace with [CONFIRMED-MISSING] or leave as plain text status "NOT DONE — file does not exist." Git confirmation applies only to existing files where commit history can be queried; it has no meaning for non-existent files. Also clarify which of the 10 Delta items are covered by the git evidence table (8 of 10) and which rely on content re-verification only.

### P1 — Should fix before the audit can ground downstream writing work

**R2-004 (Resolves: SR-004, CC-004, CV-105, FM-005, IN-005, RT-105, PM-003)**

Correct all Delta table counts:
- PROJ-015 baseline row: "15 (per Coverage Matrix: 15 skills marked P)" → "14 (per Coverage Matrix: 14 skills marked P)"
- Delta value: "+15" → "+16"
- How-To coverage PROJ-015 rate: "4/15 skills (27%)" → "4/14 skills (29%)"

**R2-005 (Resolves: SR-005, CV-106, FM-004, RT-104, PM-004, DA-003, IN-004)**

Correct EV-024 to cite the actual H-04 location in transcript.md:

Replace current EV-024 with:
```
| EV-024 | `docs/playbooks/transcript.md:74-84` | H-04 teaching content in Step-by-Step > Primary Path section: "The transcript skill uses a mandatory two-phase architecture: Phase 1 (CLI — deterministic): Python parser converts the raw file into structured JSON chunks. This is ~1,250x cheaper than LLM parsing and produces 100% accurate timestamps... (Cost basis: A 1-hour VTT transcript produces ~280K tokens of structured data. The Python parser processes this at zero API token cost in <1 second. LLM parsing of the same data requires ~280K input tokens + ~50K output tokens at API rates, yielding a ~1,250:1 cost ratio.)" — this architecture explanation and cost rationale appears inside the Step-by-Step section before the numbered steps, constituting teaching content embedded in a how-to guide (H-04 violation). |
```

Also update the Document 13 H-04 criterion row to reference lines 74-84 and the Step-by-Step section, not lines 25-31.

**R2-006 (Resolves: DA-004, FM-006)**

Correct EV-022 to cite the full orchestration.md Workflow Patterns line range:

Replace "lines 57-65" with "lines 57-131" in EV-022. Update the Document 12 H-04 evidence to note the section spans all three workflow patterns with ASCII diagrams.

### P2 — Should fix for completeness

**R2-007 (Resolves: SR-006, FM-007, DA-005, FM-008)**

Read AGENTS.md to the end and supply a specific line count (replace "~200+"). Similarly, read Documents 3-6 precisely and replace "~450", "~175", "~90", "~200" with exact counts. This is a low-effort, high-credibility improvement.

**R2-008 (Resolves: SR-007, SM-003)**

Pick one trajectory framing and use it consistently throughout. The Executive Summary uses "~20% to ~13%" (based on a 15-skill denominator at PROJ-015). The Delta section uses "~27% to ~17%" (based on a corrected 14-skill PROJ-015 denominator). With the corrected count of 14 P skills, 4/14 = 29% (not 27%). Update all trajectory percentage statements to use the same calculation basis. Recommended: "29% to 17%" using actual counted values rather than approximations.

---

## Tournament Verdict

### Summary by Strategy

| Strategy | New Findings | Critical | Major | Minor |
|----------|-------------|----------|-------|-------|
| S-003 Steelman | 5 improvement notes | 0 | 0 | 0 |
| S-010 Self-Refine | 7 | 2 | 3 | 2 |
| S-007 Constitutional | 4 | 2 | 2 | 0 |
| S-002 Devil's Advocate | 5 | 1 | 2 | 2 |
| S-004 Pre-Mortem | 6 | 2 | 2 | 2 |
| S-012 FMEA | 8 | 5 | 2 | 1 (resolved: 4 iter-1 FM entries) |
| S-013 Inversion | 6 | 2 | 3 | 1 |
| S-011 CoVe | 8 (new claims) | 2 | 3 | 0 |
| S-001 Red Team | 6 | 3 | 3 | 0 |
| **Totals** | **37** | **16 Critical** | **21 Major** | **8 Minor** |

*Note: Iteration 1 had 61 findings (20 Critical). Iteration 2 has 37 findings (16 Critical) — net improvement. However, 3 P0 Critical findings are new introductions (not carried from iter-1), meaning the revision introduced new blocking issues.*

### Iteration 1 vs. Iteration 2 Critical Finding Comparison

| Iter-1 Root Cause | Iter-2 Status |
|-------------------|---------------|
| 26 vs. 15 skills discrepancy (most damaging) | REPLACED BY: 16 vs. "exactly 15" discrepancy — same type of error, now self-refuting within a single paragraph |
| EV-012 arithmetic error | FULLY RESOLVED |
| "UNCHANGED" without git evidence | PARTIALLY RESOLVED — git evidence table provided but contradicted by footer disclaimer; hash verifiability unknown |

### Does the Audit's Core Thesis Hold?

**YES, still.** The worsening trajectory finding (zero tutorials, zero skill-specific how-to, zero explanation for any skill; coverage declined from ~29% to ~17% with corrected numbers) remains the most defensible and most important finding in the audit. It is unaffected by the scope count errors.

**The iteration 2 revision fixed the right things (EV-012, playbook evaluations, line counts) but introduced a new critical error in the highest-visibility fix (scope reconciliation).** The pattern is: precise numbers were added that are wrong, when approximate language or cross-document consistency checks would have caught them.

### Verdict: REVISE — New P0 Items Block Use as Foundation Document

The audit has improved materially from iteration 1 (0.844 composite) but has not reached the 0.95 threshold. The single most important change introduced a new self-refuting factual claim ("exactly 15 (N)" while the document's own table and enumeration show 16). Additionally, the git evidence mechanism is internally contradicted, leaving the UNCHANGED claims in the same uncertain state as before — just with more elaborate scaffolding around the uncertainty.

**Three P0 actions required before use as a foundation document:**

1. **R2-001:** Correct "exactly 15 (N)" to "exactly 16 (N)" and cascade through all downstream references. This is a search-and-replace with careful arithmetic verification, not a research task.

2. **R2-002:** Resolve the git evidence contradiction (keep the table or keep the disclaimer, not both). If the hashes are real, keep them and remove the disclaimer. If the hashes are uncertain, remove the table and replace with content-verification language.

3. **R2-003:** Remove [GIT-CONFIRMED] from the two non-existent files in the Delta table.

**Assessment:** With R2-001 through R2-003 resolved, the audit should be substantially closer to the 0.95 threshold. The remaining P1 fixes (EV-024 location, Delta baseline counts) are important for precision but do not block the core use case. The core findings — zero tutorials, 16 undocumented new skills, 10 PROJ-015 items unresolved in 49 days — are correct, actionable, and well-evidenced.

---

## Execution Statistics

| Metric | Value |
|--------|-------|
| Total New Findings | 37 |
| Critical | 16 |
| Major | 21 |
| Minor | 8 (excludes Steelman improvements) |
| Strategies Executed | 9 of 10 (S-014 by adv-scorer) |
| Iter-1 Blockers Fully Resolved | 2 of 6 (Blockers 2 and 4) |
| Iter-1 Blockers Partially Resolved | 3 of 6 (Blockers 1, 3, 5/6) |
| New Critical Issues Introduced | 3 (scope count, git contradiction, non-file GIT-CONFIRMED) |
| New Claims Verified (S-011) | 4 VERIFIED, 3 MATERIAL DISCREPANCY, 1 UNVERIFIABLE |
| Root Cause Clusters (iter-2) | 3 (scope off-by-one, git evidence contradiction, EV location errors) |
| Verdict | REVISE — 3 P0 items block use as foundation document |
| Quality Threshold Met | NO — does not meet 0.95 (user-specified); gap likely 0.05-0.08 based on dimension improvements |
| Comparison to Iter-1 | Improved: fewer findings (37 vs 61), critical count reduced (16 vs 20), 2 major blockers fully resolved. Regressed: scope reconciliation introduced new self-refuting critical error. |
