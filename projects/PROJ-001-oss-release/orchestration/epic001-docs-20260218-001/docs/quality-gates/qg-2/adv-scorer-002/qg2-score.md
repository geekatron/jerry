# Quality Score Report: FEAT-018 User Documentation -- Runbooks & Playbooks (QG-2)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Scoring Context](#scoring-context) | Deliverable metadata and scoring parameters |
| [L0 Executive Summary](#l0-executive-summary) | One-line assessment and verdict |
| [Score Summary](#score-summary) | Composite score and threshold comparison |
| [Per-Deliverable Scores](#per-deliverable-scores) | Individual file assessments |
| [Dimension Scores](#dimension-scores) | Weighted composite calculation with evidence |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Per-dimension evidence, gaps, and improvement paths |
| [Cross-Strategy Correlation Analysis](#cross-strategy-correlation-analysis) | Agreement and disagreement across S-003, S-002, S-007 |
| [Improvement Recommendations](#improvement-recommendations-priority-ordered) | Ranked revision targets |
| [Scoring Impact Analysis](#scoring-impact-analysis) | Gap-to-threshold calculation |
| [Leniency Bias Check](#leniency-bias-check-h-15-self-review) | H-15 self-review verification |

---

## Scoring Context

- **Deliverables:**
  1. `docs/runbooks/getting-started.md`
  2. `docs/playbooks/problem-solving.md`
  3. `docs/playbooks/orchestration.md`
  4. `docs/playbooks/transcript.md`
- **Deliverable Type:** User Documentation (Runbooks & Playbooks)
- **Criticality Level:** C2 (Standard)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored By:** adv-scorer-002
- **Scored:** 2026-02-18
- **Iteration:** QG-2 (quality gate review of final deliverables after 3-iteration creator-critic cycle)
- **Prior Score:** 0.937 (creator-critic cycle final score)
- **Strategy Reports Incorporated:** S-003 Steelman (13 findings), S-002 Devil's Advocate (10 findings), S-007 Constitutional (7 findings)

---

## L0 Executive Summary

**Score:** 0.89/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.84)

**One-line assessment:** The documentation suite demonstrates strong structural discipline and internal consistency but contains multiple evidence gaps (unsupported quantitative claims, keyword determinism assertions, missing version information) and a completeness hole (phantom INSTALLATION.md prerequisite) that prevent it from reaching the 0.92 quality gate. Targeted revision of 5-7 specific items would close the gap.

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.89 |
| **Threshold (H-13)** | 0.92 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | Yes (30 findings across 3 strategies) |
| **Prior Score (creator-critic cycle)** | 0.937 |
| **Delta from Prior** | -0.047 |

**Delta Explanation:** The prior 0.937 score was generated during the creator-critic cycle (internal quality loop). This QG-2 score applies the S-014 rubric with leniency bias counteraction, incorporating evidence from three independent adversarial strategies that surfaced gaps the creator-critic cycle did not detect. The downward delta reflects genuine gaps identified by the adversarial review process, not scoring error. Key gaps surfaced by adversarial review: phantom INSTALLATION.md (DA-001/CC-012), unsupported 1,250x cost claim (DA-004/SM-008), keyword determinism assertion (DA-003), and missing version information (DA-005).

---

## Per-Deliverable Scores

### 1. `docs/runbooks/getting-started.md`

| Dimension | Score | Key Evidence |
|-----------|-------|-------------|
| Completeness | 0.83 | Phantom INSTALLATION.md (DA-001), WORKTRACKER.md purpose undocumented (CC-010), no version info (DA-005) |
| Internal Consistency | 0.92 | Consistent structure, dual-platform commands. Minor: hedging language on persistence contradicts P-002 guarantee (CC-012) |
| Methodological Rigor | 0.93 | Strong procedural structure: prerequisites, 5 steps, verification, troubleshooting. Clean runbook methodology |
| Evidence Quality | 0.80 | Phantom prerequisite link (DA-001), no version info (DA-005), unverified `/plugin` UI reference (CC-013), hedging on output location |
| Actionability | 0.86 | Clear steps but: no mid-workflow error recovery (DA-002), hedging language on persistence (CC-012), no time estimate (SM-001) |
| Traceability | 0.88 | H-04 explained with context; bare H-rule citations elsewhere without links (CC-011) |

**Weighted Score:** (0.83 x 0.20) + (0.92 x 0.20) + (0.93 x 0.20) + (0.80 x 0.15) + (0.86 x 0.15) + (0.88 x 0.10) = 0.166 + 0.184 + 0.186 + 0.120 + 0.129 + 0.088 = **0.87** (REVISE)

---

### 2. `docs/playbooks/problem-solving.md`

| Dimension | Score | Key Evidence |
|-----------|-------|-------------|
| Completeness | 0.92 | All 9 agents documented, agent selection table, disambiguation rules, creator-critic cycle, troubleshooting. Minor gap: no sequential chaining example (SM-005) |
| Internal Consistency | 0.93 | Consistent voice and format. Agent roles, triggers, and outputs aligned. Minor: circuit breaker behavior vague (DA-009) |
| Methodological Rigor | 0.94 | Strong methodology: keyword-to-agent decision table, disambiguation rules, "When to Use / Do NOT use" boundaries, criticality auto-escalation |
| Evidence Quality | 0.84 | Keyword activation presented as deterministic (DA-003), no observable creator-critic cycle example (SM-004), naming convention lacks worked derivation (SM-003) |
| Actionability | 0.90 | 4 concrete examples, troubleshooting table, explicit agent invocation path. Gap: no mid-workflow error recovery entry (DA-002) |
| Traceability | 0.90 | SKILL.md link, quality-enforcement.md SSOT reference, cross-references to other playbooks. Minor: some bare H-rule citations (CC-011) |

**Weighted Score:** (0.92 x 0.20) + (0.93 x 0.20) + (0.94 x 0.20) + (0.84 x 0.15) + (0.90 x 0.15) + (0.90 x 0.10) = 0.184 + 0.186 + 0.188 + 0.126 + 0.135 + 0.090 = **0.91** (REVISE -- marginal)

---

### 3. `docs/playbooks/orchestration.md`

| Dimension | Score | Key Evidence |
|-----------|-------|-------------|
| Completeness | 0.91 | 3 workflow patterns with ASCII diagrams, 3 core artifacts, P-003 compliance section. Gap: barrier diagram lacks artifact labels (SM-006), no context budget warning (CC-016) |
| Internal Consistency | 0.94 | P-003 compliance section is exemplary. Core artifacts rationale well-aligned. No contradictions detected |
| Methodological Rigor | 0.93 | Strong: pattern taxonomy, explicit "Why all three are required" rationale, P-003 violation patterns documented, quality gate integration |
| Evidence Quality | 0.85 | Example 3 describes YAML state without showing it (SM-007). No version info for tools. Barrier diagram shows structure but not data flow |
| Actionability | 0.89 | 10-step procedure, 3 examples, troubleshooting table. Gap: no mid-workflow agent failure recovery (DA-002), no explicit invocation syntax for keyword disambiguation |
| Traceability | 0.91 | P-002 and P-003 cited with context. SKILL.md and quality-enforcement.md linked. Minor inconsistency in citation depth (CC-011) |

**Weighted Score:** (0.91 x 0.20) + (0.94 x 0.20) + (0.93 x 0.20) + (0.85 x 0.15) + (0.89 x 0.15) + (0.91 x 0.10) = 0.182 + 0.188 + 0.186 + 0.1275 + 0.1335 + 0.091 = **0.91** (REVISE -- marginal)

---

### 4. `docs/playbooks/transcript.md`

| Dimension | Score | Key Evidence |
|-----------|-------|-------------|
| Completeness | 0.90 | Two-phase architecture well-documented, 9 domain contexts, 4 examples, canonical-transcript.json warning. Gap: cost differential missing from Input Formats decision point (DA-004), overlapping domain guidance missing (SM-009) |
| Internal Consistency | 0.91 | Quality threshold deviation (0.90 vs 0.92 SSOT) acknowledged with SKILL.md pointer. Gap: SRT/TXT presented as equivalent to VTT in Input Formats table but described as 1,250x more expensive in Step-by-Step (DA-004) |
| Methodological Rigor | 0.92 | Strong two-phase rationale, explicit "NOT triggered by keyword" callout (prevents common misuse), ADR-006 reference for mindmap decision |
| Evidence Quality | 0.82 | The 1,250x cost claim is unsupported (DA-004/SM-008) -- no methodology, no calculation, no source. This is the most prominent quantitative claim in any of the 4 deliverables and it lacks any evidence chain. SRT cost differential understated at decision point |
| Actionability | 0.90 | CLI syntax examples, domain selection examples, 4 worked scenarios. Gap: no mid-workflow failure recovery for partial Phase 2 output (DA-002), SRT/TXT cost implication not actionable at format selection point |
| Traceability | 0.90 | SKILL.md link, ADR-006 reference, quality-enforcement.md SSOT reference. Minor gap: 0.90 threshold deviation cited but not linked to SKILL.md section anchor |

**Weighted Score:** (0.90 x 0.20) + (0.91 x 0.20) + (0.92 x 0.20) + (0.82 x 0.15) + (0.90 x 0.15) + (0.90 x 0.10) = 0.180 + 0.182 + 0.184 + 0.123 + 0.135 + 0.090 = **0.89** (REVISE)

---

### Per-Deliverable Summary

| Deliverable | Score | Verdict |
|-------------|-------|---------|
| getting-started.md | 0.87 | REVISE |
| problem-solving.md | 0.91 | REVISE (marginal) |
| orchestration.md | 0.91 | REVISE (marginal) |
| transcript.md | 0.89 | REVISE |
| **Corpus Mean** | **0.90** | **REVISE** |

**Observation:** No individual deliverable reaches the 0.92 threshold. The two playbooks (problem-solving, orchestration) are closest at 0.91. The getting-started runbook has the most gaps, primarily driven by the phantom INSTALLATION.md and WORKTRACKER.md purpose omission.

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Severity | Evidence Summary |
|-----------|--------|-------|----------|----------|------------------|
| Completeness | 0.20 | 0.89 | 0.178 | Minor | Phantom INSTALLATION.md (DA-001), WORKTRACKER.md undocumented (CC-010), cost differential missing at decision point (DA-004), barrier diagram unlabeled (SM-006), no version info (DA-005) |
| Internal Consistency | 0.20 | 0.92 | 0.184 | N/A (Threshold) | Strong cross-document structural consistency. Minor gaps: hedging language vs. P-002 guarantee (CC-012), SRT cost asymmetry between sections (DA-004), citation pattern inconsistency (CC-011) |
| Methodological Rigor | 0.20 | 0.93 | 0.186 | N/A (Above) | Excellent procedural structure across all 4 docs: prerequisites, step-by-step, verification, troubleshooting. Decision tables, disambiguation rules, pattern taxonomies |
| Evidence Quality | 0.15 | 0.84 | 0.126 | Major | 1,250x cost claim unsupported (DA-004/SM-008), keyword activation asserted as deterministic (DA-003), no version info (DA-005), creator-critic cycle lacks observable example (SM-004), naming convention un-derived (SM-003) |
| Actionability | 0.15 | 0.89 | 0.1335 | Minor | No mid-workflow error recovery in any playbook (DA-002), hedging on persistence (CC-012), no time estimate (SM-001), output directory creation ambiguous (DA-006) |
| Traceability | 0.10 | 0.90 | 0.090 | Minor | Cross-references present but citation pattern inconsistent (CC-011): some H-rule/P-principle references include context, others are bare IDs. Relative links assume standard directory structure (DA-010) |
| **TOTAL** | **1.00** | | **0.90** | | |

**Weighted Composite Calculation:**

```
composite = (0.89 x 0.20) + (0.92 x 0.20) + (0.93 x 0.20) + (0.84 x 0.15) + (0.89 x 0.15) + (0.90 x 0.10)
          = 0.178 + 0.184 + 0.186 + 0.126 + 0.1335 + 0.090
          = 0.8975
          ~ 0.90 (rounded)
```

**Verification:** 0.178 + 0.184 + 0.186 + 0.126 + 0.1335 + 0.090 = 0.8975. Rounded to two decimal places: **0.90**.

**Note on rounding:** The raw composite is 0.8975. I round down to 0.90 per the leniency bias counteraction protocol (uncertain between 0.90 and 0.89, choose conservative). The result is the same either way: REVISE.

---

## Detailed Dimension Analysis

### Completeness (0.89/1.00) -- Minor

**Evidence (Strengths):**
- All 4 deliverables follow a complete template: navigation table (H-23/H-24 compliant), "When to Use / Do NOT use", prerequisites, step-by-step, examples, troubleshooting, related resources
- Problem-solving playbook documents all 9 agents with roles, triggers, and output locations (lines 90-103)
- Orchestration playbook covers 3 structural patterns with ASCII diagrams (lines 57-131) and 3 core artifacts (lines 134-153)
- Transcript playbook covers 9 domain contexts, 3 input formats, and the two-phase architecture (lines 68-137)
- Getting-started runbook provides dual macOS/Linux and Windows PowerShell instructions (lines 37-55)

**Gaps:**
- **DA-001-qg2 (Major -- all 3 strategies agree):** Getting-started.md line 19 references `../INSTALLATION.md` which does not exist. The onboarding path breaks at step zero. S-003 identified this as an assumption (SM step 4 key assumption #1), S-002 flagged it as the first Major finding (DA-001), S-007 confirmed it relates to P-002 persistence of user-facing paths.
- **CC-010-qg2 (Major):** WORKTRACKER.md is created as a blank file (getting-started.md lines 48-54) with no explanation of what Jerry writes to it, how agents update it, or how users should interact with it. P-010 task tracking integrity requires agents to maintain it; users should understand this.
- **DA-004-qg2 (Major):** The 1,250x cost differential between VTT deterministic parsing and SRT/TXT LLM parsing is stated in the Step-by-Step section (transcript.md line 75) but is completely absent from the Input Formats table (lines 245-249) where users make their format selection decision. Information asymmetry at the decision point.
- **DA-005-qg2 (Major):** No version or compatibility information for uv, jerry CLI, or Claude Code in any of the 4 documents. Getting-started.md line 21 checks `uv --version` but never states what version is acceptable.
- **SM-006-qg2 (Major):** Cross-pollination barrier diagram (orchestration.md lines 67-87) shows control flow but not what artifacts cross the barrier.
- **CC-016-qg2 (Minor):** Orchestration playbook does not warn about context token consumption for large workflows.

**Improvement Path:**
1. Resolve the INSTALLATION.md reference (create it or inline installation steps)
2. Add WORKTRACKER.md purpose explanation in getting-started.md Step 1
3. Add cost/accuracy note to transcript.md Input Formats section
4. Add "Tested With" version block to getting-started.md prerequisites
5. Annotate the barrier diagram with artifact names

---

### Internal Consistency (0.92/1.00) -- Threshold

**Evidence (Strengths):**
- All 4 deliverables use identical structural patterns: navigation table, blockquote header, "When to Use / Do NOT use", prerequisites, step-by-step, examples, troubleshooting, related resources. This is the strongest dimension.
- Cross-references between documents are reciprocal (getting-started links to all 3 playbooks; each playbook links to the others and to quality-enforcement.md)
- Quality threshold (0.92) is consistently stated across problem-solving.md (line 148) and orchestration.md (line 33, step 6). The transcript.md deviation (0.90) is explicitly flagged with a SKILL.md pointer (line 126).
- P-003 compliance in orchestration.md (lines 170-188) accurately represents the agent hierarchy and warns against the specific violation pattern.

**Gaps:**
- **CC-012-qg2 (Major):** Getting-started.md uses hedging language on persistence ("you may see output under subdirectories") which contradicts P-002's guarantee that agents SHALL persist all significant outputs. The inconsistency is between the documented system guarantee and the user-facing description of that guarantee.
- **DA-004-qg2 (Major, cross-section):** Transcript.md Step-by-Step section describes VTT as "1,250x cheaper" (line 75) but the Input Formats table (lines 245-249) presents VTT, SRT, and TXT as effectively equivalent choices. The two sections of the same document give contradictory impressions about format equivalence.
- **CC-011-qg2 (Major, cross-document):** Constitutional citations are inconsistent: orchestration.md lines 152 and 172 cite P-002 and P-003 with full context explanations; problem-solving.md line 215 cites P-002 as a bare reference; getting-started.md line 33 uses bold formatting for H-04 but no link or context. The pattern inconsistency means users cannot reliably understand rule references.
- **DA-008-qg2 (Minor):** Windows PowerShell instructions appear in getting-started.md but not in any of the 3 playbooks, creating an inconsistent cross-platform posture.

**Improvement Path:**
1. Replace hedging language with P-002 guarantee assertion in getting-started.md
2. Add cost/accuracy note to transcript.md Input Formats table for consistency with Step-by-Step
3. Standardize citation pattern: first mention of any H-rule or P-principle includes a link to its source document

**High-score justification (3 evidence points for > 0.90):**
1. Identical structural template across all 4 documents (navigation table, sections, troubleshooting, examples, related resources)
2. Reciprocal cross-referencing: every playbook links to every other, and all link to SKILL.md and quality-enforcement.md
3. Quality threshold consistently stated with explicit deviation flagging in transcript.md

---

### Methodological Rigor (0.93/1.00) -- Above Threshold

**Evidence (Strengths):**
- Problem-solving playbook provides a keyword-to-agent decision table (lines 117-127) with disambiguation rules for overlapping agent roles (ps-analyst vs ps-investigator, ps-critic vs /adversary). This is exemplary methodological rigor for a playbook.
- Orchestration playbook establishes a 3-pattern taxonomy (cross-pollinated, sequential-checkpoint, fan-out/fan-in) with "Use when" selection guidance for each pattern.
- Getting-started runbook follows textbook runbook methodology: prerequisites with verifiable criteria, numbered steps with expected results, verification checklist, troubleshooting table.
- Transcript playbook explicitly warns against the most dangerous failure mode (reading canonical-transcript.json) with a CRITICAL WARNING callout (lines 131-136).
- All 4 troubleshooting tables use consistent symptom-cause-resolution triple format.

**Gaps:**
- **DA-009-qg2 (Minor):** Problem-solving.md circuit breaker (lines 167-168) uses "either accept the deliverable with caveats documented or escalate to the user" without specifying the condition that determines which path. This is a minor methodological vagueness.
- **DA-003-qg2 (Major, partial):** The keyword activation model is presented as a reliable mapping method without acknowledging its probabilistic nature. A rigorous methodology would note the limitation and provide a deterministic fallback in all playbooks.

**Improvement Path:**
1. Specify the circuit breaker condition (what triggers accept-with-caveats vs. escalate)
2. Add a brief disambiguation note acknowledging probabilistic keyword detection

**High-score justification (3 evidence points for > 0.90):**
1. Problem-solving agent selection table with 9-row keyword-to-agent mapping and 2 explicit disambiguation rules
2. Orchestration 3-pattern taxonomy with ASCII diagrams and "Use when" selection guidance per pattern
3. Consistent troubleshooting methodology across all 4 documents: 5-7 entries each, symptom-cause-resolution triples, covering the most common failure modes

---

### Evidence Quality (0.84/1.00) -- Major

**Evidence (Strengths):**
- Getting-started.md provides concrete, copy-paste-ready commands for every step (lines 37-43, 47-54, 67-72, 98-99, 154-159)
- Problem-solving.md provides 4 worked examples (lines 178-206) with "User request" and "System behavior" pairs
- Orchestration.md provides 3 examples (lines 220-236) demonstrating each workflow pattern
- Quality threshold explanation includes the 6-dimension weight table (problem-solving.md lines 149-157)

**Gaps:**
- **DA-004-qg2 / SM-008-qg2 (Major -- highest impact):** The "1,250x cheaper" claim (transcript.md line 75) is the most prominent quantitative assertion in the entire documentation suite and it has zero supporting evidence. No methodology, no calculation, no source citation. S-003 reconstructed a plausible calculation (SM-008: ~280K tokens, deterministic at ~0 tokens vs. ~330K for LLM). S-002 flagged this as a Major gap (DA-004). The claim may be correct but it reads as an unsupported assertion.
- **DA-003-qg2 (Major):** Keyword-based skill activation is presented as deterministic ("State your request in natural language, using one of the trigger keywords" -- problem-solving.md line 64; "use the keyword orchestration in your request to trigger automatic invocation" -- orchestration.md line 28). LLM keyword detection is probabilistic. No caveat, no conflict resolution rule, no evidence that this mapping is reliable.
- **DA-005-qg2 (Major):** No version information for any tool dependency across all 4 documents. Getting-started.md line 21 instructs `uv --version` but specifies no minimum. This means instructions become unreliable over time with no diagnostic path.
- **SM-004-qg2 (Major):** The creator-critic-revision cycle (problem-solving.md lines 139-173) is described mechanically but lacks an observable example of what the user sees during the cycle. S-003 provided a concrete reconstruction showing 3-iteration score progression.
- **SM-003-qg2 (Major):** Output file naming convention (problem-solving.md line 104) states the pattern `{ps-id}-{entry-id}-{topic-slug}.md` but does not derive each component. S-003 reconstructed a labeled breakdown.
- **CC-013-qg2 (Minor):** Getting-started.md line 23 references `/plugin` > Installed tab as a Claude Code UI element. This is not verified as current.

**Improvement Path:**
1. Add calculation methodology for the 1,250x claim (token cost comparison for a representative 1-hour VTT)
2. Add disambiguation notes acknowledging probabilistic keyword detection with explicit invocation fallback
3. Add "Tested With" version block listing uv, jerry CLI, and Claude Code versions
4. Add an observable creator-critic cycle example per SM-004
5. Break down the naming convention into labeled components per SM-003

---

### Actionability (0.89/1.00) -- Minor

**Evidence (Strengths):**
- Getting-started.md provides 5 numbered steps with expected results at each step and a final verification checklist (lines 176-182)
- All 4 troubleshooting tables provide concrete resolutions (not just "fix it" but specific commands and checks)
- Problem-solving.md provides an "Optional Path: Explicit agent request" section (lines 78-84) giving users a direct bypass for keyword detection
- Transcript.md CLI examples include all flags and absolute paths (lines 89-95, 98-101, 148-149, 163-166, 232-235)

**Gaps:**
- **DA-002-qg2 (Major -- most consequential):** No playbook documents how to recover from mid-workflow agent failure. All 3 playbooks' troubleshooting tables cover pre-start and post-completion failures but omit the most common real-world failure mode: an agent crashes partway through, leaving partial artifacts. S-002 provided specific acceptance criteria: each playbook must document (1) failure identification, (2) artifact salvage, (3) recovery procedure.
- **CC-012-qg2 (Major):** Hedging language on persistence in getting-started.md undermines the P-002 guarantee. Users reading "you may see output" cannot confidently determine whether persistence occurred.
- **DA-006-qg2 (Minor):** Output directories (`docs/research/`, `docs/analysis/`, etc.) are referenced but never specified as auto-created or manually required.
- **SM-001-qg2 (Minor):** No estimated time to complete the getting-started runbook.

**Improvement Path:**
1. Add "agent fails mid-execution" troubleshooting entry to each playbook with failure identification, salvage, and recovery steps
2. Replace hedging language with assertive P-002 guarantee
3. Clarify auto-creation behavior for output directories
4. Add time estimate to getting-started.md introduction

---

### Traceability (0.90/1.00) -- Minor

**Evidence (Strengths):**
- All 4 deliverables link to their respective SKILL.md (problem-solving.md line 226, orchestration.md line 256, transcript.md line 267)
- All 3 playbooks link to quality-enforcement.md SSOT (problem-solving.md line 229, orchestration.md line 257)
- Getting-started.md Next Steps section (lines 200-204) creates a navigation chain to all 3 playbooks
- Orchestration.md cites P-002 and P-003 with full context explanations (lines 152, 172)

**Gaps:**
- **CC-011-qg2 (Major, cross-document):** Citation pattern is inconsistent. Some rule references include context (orchestration.md:152 -- "Discarding any one of the three in favor of in-memory state violates P-002 (file persistence requirement)"). Others are bare IDs (problem-solving.md:51 -- "H-04 -- session will not proceed without this"). Users encountering these rule IDs for the first time have no way to look them up without knowing which document to consult.
- **DA-010-qg2 (Minor):** All cross-references use relative paths (e.g., `../../skills/problem-solving/SKILL.md`). These break if directory depth changes in forks.
- **SM-010-qg2 (Minor):** Quality threshold explanation pattern is not standardized across playbooks. Each states the threshold slightly differently.

**Improvement Path:**
1. Standardize citation pattern: first mention of any H-rule/P-principle includes a markdown link to its source document
2. Standardize quality threshold explanation template across all playbooks
3. Consider adding a note about relative link behavior on GitHub forks

---

## Cross-Strategy Correlation Analysis

### Finding Convergence Map

Where multiple strategies independently identified the same gap, the finding has higher confidence and scoring impact.

| Gap | S-003 (Steelman) | S-002 (Devil's Advocate) | S-007 (Constitutional) | Convergence | Scoring Impact |
|-----|-------------------|--------------------------|------------------------|-------------|----------------|
| **Phantom INSTALLATION.md** | SM step 4 key assumption #1 | DA-001-qg2 (Major) | CC-012-qg2 (Major, related -- P-002 hedging) | 3/3 AGREE | HIGH -- Completeness and Evidence Quality both impacted |
| **1,250x cost claim unsupported** | SM-008-qg2 (Major) | DA-004-qg2 (Major) | CC-014-qg2 (Minor -- P-005 graceful degradation context) | 3/3 AGREE | HIGH -- Evidence Quality primary, Completeness secondary |
| **Keyword activation determinism** | SM-004-qg2 (Major, partial -- focuses on creator-critic observability) | DA-003-qg2 (Major -- full treatment) | Not flagged | 2/3 AGREE | MEDIUM -- Evidence Quality, Methodological Rigor |
| **No mid-workflow error recovery** | Not flagged | DA-002-qg2 (Major) | Not flagged | 1/3 | MEDIUM -- Actionability primary (single strategy but high consequence) |
| **WORKTRACKER.md purpose undocumented** | Not flagged | Not flagged | CC-010-qg2 (Major) | 1/3 | MEDIUM -- Completeness (constitutional compliance concern) |
| **Inconsistent citations** | SM-010-qg2 (Minor -- quality threshold pattern) | DA-008-qg2 (Minor -- Windows inconsistency) | CC-011-qg2 (Major -- P-004 provenance) | 3/3 AGREE (different facets of consistency) | MEDIUM -- Internal Consistency, Traceability |
| **No version information** | Not flagged | DA-005-qg2 (Major) | Not flagged | 1/3 | MEDIUM -- Evidence Quality (single strategy but high OSS impact) |
| **Creator-critic cycle not observable** | SM-004-qg2 (Major) | DA-003-qg2 (partial overlap) | Not flagged | 1.5/3 | LOW-MEDIUM -- Evidence Quality |
| **Barrier diagram unlabeled** | SM-006-qg2 (Major) | Not flagged | Not flagged | 1/3 | LOW -- Completeness (single strategy, presentation improvement) |
| **SRT/TXT cost differential understated** | Not specifically flagged | DA-004-qg2 (Major, co-occurrence) | CC-014-qg2 (Minor) | 2/3 AGREE | MEDIUM -- Completeness (information at decision point) |

### Strategy Disagreements

| Area | S-003 View | S-002 View | S-007 View | Resolution |
|------|-----------|-----------|-----------|------------|
| **Overall quality** | HIGH -- "already above C2 quality gate threshold" | ACCEPT with targeted revisions -- structurally sound but optimistic-path-only | PARTIAL compliance -- 0.93 weighted mean but 0.88 for getting-started | S-002 and S-007 are more accurate; the phantom INSTALLATION.md and evidence gaps require revision |
| **Severity of keyword determinism** | Minor (SM-004 focuses on observability, not reliability) | Major (DA-003 -- fundamental design claim is unsubstantiated) | Not flagged | S-002 assessment is correct -- this is a Major evidence gap since it affects how users understand the core interaction model |
| **P-002 hedging language** | Not specifically flagged | Not specifically flagged | CC-012-qg2 (Major) | S-007 correctly identifies this as a constitutional compliance gap that other strategies missed |
| **Windows cross-platform** | SM-012-qg2 (Minor -- add note to playbooks) | DA-008-qg2 (Minor -- inconsistent posture) | Not flagged | Both strategies agree this is Minor; a note in each playbook is sufficient |

### Correlation Summary

- **HIGH convergence (3/3 or 2.5/3):** Phantom INSTALLATION.md, 1,250x cost claim, inconsistent citations. These have the highest confidence and the greatest scoring impact.
- **MEDIUM convergence (1.5-2/3):** Keyword determinism, SRT cost differential, mid-workflow recovery.
- **Strategy-unique findings with high impact:** WORKTRACKER.md purpose (S-007 only), version info (S-002 only), mid-workflow recovery (S-002 only). These were not independently corroborated but are substantively valid based on their evidence.
- **S-003 (Steelman) strength:** Identified 5 Major presentation/evidence improvements that are constructive (not just gaps). These translate directly into revision targets.
- **S-002 (Devil's Advocate) strength:** Identified the most consequential real-world gaps (mid-workflow failure, version decay). These are the most user-impactful findings.
- **S-007 (Constitutional) strength:** Identified governance compliance gaps (P-002 hedging, P-004 citations, P-010 WORKTRACKER) that other strategies missed because they focused on user experience rather than constitutional alignment.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension(s) | Current | Target | Recommendation | Finding Sources |
|----------|-------------|---------|--------|----------------|-----------------|
| 1 | Evidence Quality, Completeness | 0.84, 0.89 | 0.92+ | **Resolve phantom INSTALLATION.md:** Either create `docs/INSTALLATION.md` with uv installation, Jerry clone, and plugin registration steps, or inline the 3 prerequisites directly into getting-started.md. Every hyperlink in Prerequisites must resolve. | DA-001, SM step 4 #1, CC-012 |
| 2 | Evidence Quality | 0.84 | 0.92+ | **Support the 1,250x cost claim:** Add calculation methodology to transcript.md line 75-76 (example: "1-hour VTT produces ~280K tokens; deterministic parsing costs ~0 tokens vs. ~330K input+output tokens for LLM parsing"). Also add cost note to Input Formats table. | DA-004, SM-008, CC-014 |
| 3 | Evidence Quality | 0.84 | 0.90+ | **Add keyword disambiguation notes:** In problem-solving.md and orchestration.md, acknowledge that keyword detection is probabilistic, document what happens with conflicting keywords, and provide explicit `/skill` slash-command syntax as guaranteed-activation alternative in all playbooks. | DA-003, SM-004 |
| 4 | Actionability | 0.89 | 0.92+ | **Add mid-workflow error recovery:** Add one troubleshooting entry to each playbook covering agent failure mid-execution. For orchestration: use checkpoint recovery. For transcript: reuse Phase 1 chunks. For problem-solving: re-invoke with explicit file reference. | DA-002 |
| 5 | Completeness | 0.89 | 0.92+ | **Document WORKTRACKER.md purpose:** Add 2-3 sentences after the `touch` command in getting-started.md Step 1 explaining what Jerry writes to WORKTRACKER.md and how users can inspect it. | CC-010 |
| 6 | Actionability, Completeness | 0.89, 0.89 | 0.91+ | **Replace hedging language with P-002 guarantee:** In getting-started.md lines 161-162, change "you may see output under subdirectories" to "All skill agents persist their output to your project directory (P-002 guarantee). The specific subdirectory depends on the agent." | CC-012 |
| 7 | Traceability, Internal Consistency | 0.90, 0.92 | 0.92+ | **Standardize citation pattern:** For first mention of any H-rule or P-principle in each document, use pattern: `H-04 ([Quality Enforcement](../../.context/rules/quality-enforcement.md))`. Apply consistently across all 4 files. | CC-011, SM-010 |
| 8 | Evidence Quality | 0.84 | 0.88+ | **Add "Tested With" version block:** In getting-started.md Prerequisites, add minimum uv version, Jerry CLI version, and Claude Code compatibility note. | DA-005 |
| 9 | Evidence Quality | 0.84 | 0.88+ | **Add observable creator-critic cycle example:** In problem-solving.md after line 147, add a concrete 3-iteration example showing dimension scores, band classification, and termination per SM-004. | SM-004 |
| 10 | Evidence Quality | 0.84 | 0.87+ | **Break down naming convention:** In problem-solving.md line 104, expand the naming convention into labeled components per SM-003: `{ps-id}` = work item ID, `{entry-id}` = sequential entry number, `{topic-slug}` = kebab-case descriptor. | SM-003 |

**Implementation Guidance:** Priorities 1-6 are necessary to reach the 0.92 threshold. Addressing Priorities 1-3 alone would lift Evidence Quality from 0.84 to approximately 0.90-0.92; addressing Priorities 4-6 would lift Actionability and Completeness above 0.92. Priorities 7-10 are additional strengthening that would further raise the composite score but are not strictly necessary for threshold passage if Priorities 1-6 are implemented well.

---

## Scoring Impact Analysis

### Dimension Impact on Composite

| Dimension | Weight | Score | Weighted Contribution | Gap to 0.92 | Weighted Gap |
|-----------|--------|-------|----------------------|-------------|--------------|
| Completeness | 0.20 | 0.89 | 0.178 | 0.03 | 0.006 |
| Internal Consistency | 0.20 | 0.92 | 0.184 | 0.00 | 0.000 |
| Methodological Rigor | 0.20 | 0.93 | 0.186 | 0.00 (above) | 0.000 |
| Evidence Quality | 0.15 | 0.84 | 0.126 | 0.08 | 0.012 |
| Actionability | 0.15 | 0.89 | 0.1335 | 0.03 | 0.0045 |
| Traceability | 0.10 | 0.90 | 0.090 | 0.02 | 0.002 |
| **TOTAL** | **1.00** | | **0.8975** | | **0.0245** |

**Interpretation:**
- **Current composite:** 0.90/1.00 (rounded from 0.8975)
- **Target composite:** 0.92/1.00 (H-13 threshold)
- **Total weighted gap:** 0.0245 (need ~0.025 composite improvement)
- **Largest improvement opportunity:** Evidence Quality (weighted gap 0.012 -- nearly half the total gap)
- **Second largest:** Completeness (weighted gap 0.006)
- **Third largest:** Actionability (weighted gap 0.0045)

**Path to 0.92:** Raising Evidence Quality from 0.84 to 0.92 would add 0.012 to the composite (0.90 -> 0.91). Raising Completeness from 0.89 to 0.94 would add 0.010 (0.91 -> 0.92). This two-dimension strategy is the minimum path to threshold. Raising Actionability from 0.89 to 0.93 would add 0.006 as buffer.

### Verdict Rationale

**Verdict:** REVISE

**Rationale:**
1. The weighted composite score of 0.90 is below the H-13 threshold of 0.92.
2. No individual deliverable reaches 0.92 -- the closest are problem-solving.md and orchestration.md at 0.91.
3. Evidence Quality at 0.84 is the weakest dimension and the primary driver of the below-threshold composite. Three independent adversarial strategies converged on evidence gaps (1,250x claim, keyword determinism, version information).
4. The phantom INSTALLATION.md (DA-001) is a high-convergence finding (3/3 strategies) that affects both Completeness and Evidence Quality.
5. No Critical findings were identified (no dimension <= 0.50), so ESCALATE is not warranted.
6. The gap to threshold (0.025) is achievable through targeted revision of the 6 highest-priority recommendations.
7. The prior creator-critic cycle score of 0.937 did not detect several of the gaps that the adversarial strategies surfaced, validating the need for this QG-2 review.

---

## Leniency Bias Check (H-15 Self-Review)

- [x] **Each dimension scored independently** -- Completeness and Actionability were scored separately despite overlapping findings (e.g., DA-002 affects Actionability; WORKTRACKER.md omission affects Completeness). Cross-influence was avoided by using different evidence for each.
- [x] **Evidence documented for each score** -- All six dimensions include specific deliverable line references, finding IDs from all 3 strategy reports, and quotes or paraphrases of the relevant content.
- [x] **Uncertain scores resolved downward** -- Evidence Quality was considered at 0.85 but downgraded to 0.84 because the 1,250x claim is the most prominent quantitative assertion in the suite and has zero evidence chain. Internal Consistency was considered at 0.93 but held at 0.92 because the P-002 hedging language gap (CC-012) is a genuine inconsistency between system guarantee and user-facing description.
- [x] **First-draft calibration considered** -- These are NOT first drafts; they passed a 3-iteration creator-critic cycle. Scoring calibrates to "near-final" deliverable expectations, not first-draft ranges.
- [x] **No dimension scored above 0.95 without exceptional evidence** -- The highest dimension score is Methodological Rigor at 0.93. No dimension exceeds 0.95.
- [x] **High-scoring dimensions verified (> 0.90):**
  - Internal Consistency (0.92): (1) Identical structural template across 4 documents, (2) Reciprocal cross-referencing, (3) Quality threshold consistency with explicit deviation flagging
  - Methodological Rigor (0.93): (1) 9-row agent selection table with disambiguation, (2) 3-pattern orchestration taxonomy with "Use when" guidance, (3) Consistent troubleshooting methodology across all 4 documents
  - Traceability (0.90): (1) SKILL.md links from all playbooks, (2) quality-enforcement.md SSOT references, (3) Getting-started -> playbook navigation chain. Note: 0.90 is AT the > 0.90 boundary; the 3 evidence points above support this as the ceiling given the CC-011 citation inconsistency gap.
- [x] **Low-scoring dimensions verified:** (1) Evidence Quality at 0.84 -- justified by 3 Major evidence gaps (1,250x claim, keyword determinism, version info) corroborated across strategies; (2) Completeness at 0.89 -- justified by phantom INSTALLATION.md, WORKTRACKER.md omission, and cost differential missing from decision point; (3) Actionability at 0.89 -- justified by missing mid-workflow error recovery across all playbooks and hedging language on persistence.
- [x] **Weighted composite matches mathematical calculation** -- 0.178 + 0.184 + 0.186 + 0.126 + 0.1335 + 0.090 = 0.8975, rounded to 0.90. Verified.
- [x] **Verdict matches score range table** -- 0.90 is in the 0.85-0.91 REVISE band per H-13. Verdict = REVISE. Confirmed.
- [x] **Improvement recommendations are specific and actionable** -- All 10 recommendations specify the exact file, the exact gap, the finding sources, and concrete acceptance criteria (e.g., "create docs/INSTALLATION.md" not "improve completeness").

**Leniency Bias Counteraction Notes:**
- The prior creator-critic cycle scored 0.937. This QG-2 score of 0.90 represents a -0.037 delta. I verified this is justified by the adversarial findings and is not an artifact of scoring inconsistency. The creator-critic cycle did not have access to the S-002, S-003, and S-007 strategy reports that surfaced the evidence gaps.
- I considered whether Evidence Quality deserved 0.86 instead of 0.84. The 1,250x cost claim convergence across all 3 strategies (SM-008, DA-004, CC-014) convinced me that 0.84 is appropriate -- the most prominent quantitative claim in the suite has zero evidence backing, and this is compounded by the keyword determinism assertion and version information absence.
- Methodological Rigor at 0.93 could be argued as generous given the keyword determinism issue (DA-003). However, I scored DA-003 primarily under Evidence Quality (the claim is unsubstantiated evidence, not a methodological flaw -- the methodology of providing keyword tables is sound; the evidence that the mapping is reliable is absent). The minor circuit breaker vagueness (DA-009) is the only methodological gap.

---

*Strategy: S-014 (LLM-as-Judge) | Template: `.context/templates/adversarial/s-014-llm-as-judge.md` v1.0.0 | SSOT: `.context/rules/quality-enforcement.md` | Execution ID: qg2 | Scorer: adv-scorer-002*
