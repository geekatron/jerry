# S-010 Self-Refine -- Adversarial Strategy Execution Template

<!--
TEMPLATE: S-010 Self-Refine Strategy Execution
VERSION: 1.0.0 | DATE: 2026-02-15
SOURCE: quality-enforcement.md SSOT, ADR-EPIC002-001, Madaan et al. 2023
ENABLER: EN-804
STATUS: ACTIVE
FORMAT: Conforms to TEMPLATE-FORMAT.md v1.1.0
-->

> **Type:** adversarial-strategy-template
> **Status:** ACTIVE
> **Version:** 1.0.0
> **Date:** 2026-02-15
> **Source:** quality-enforcement.md, ADR-EPIC002-001, Madaan et al. 2023 "Self-Refine"
> **Enabler:** EN-804
> **Academic Foundation:** Madaan et al. 2023 demonstrated that LLMs can improve outputs through structured self-feedback loops without external critique

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Identity](#identity) | Strategy classification and metadata |
| [Purpose](#purpose) | When and why to apply Self-Refine |
| [Prerequisites](#prerequisites) | Required inputs and context before execution |
| [Execution Protocol](#execution-protocol) | Step-by-step self-review procedure |
| [Output Format](#output-format) | Required structure for self-review output |
| [Scoring Rubric](#scoring-rubric) | Quality evaluation of self-review execution |
| [Examples](#examples) | Concrete before/after demonstrations |
| [Integration](#integration) | Cross-strategy pairing and criticality mapping |

---

## Identity

| Field | Value |
|-------|-------|
| Strategy ID | S-010 |
| Strategy Name | Self-Refine |
| Family | Iterative Self-Correction |
| Composite Score | 4.00 |
| Finding Prefix | SR-NNN |
| Version | 1.0.0 |
| Date | 2026-02-15 |

### Criticality Tier Table

| Level | Name | Status | Rationale |
|-------|------|--------|-----------|
| C1 | Routine | **REQUIRED** | Only required strategy at C1; baseline quality mechanism (H-15) |
| C2 | Standard | Optional | S-007, S-002, S-014 are required instead |
| C3 | Significant | Optional | Part of comprehensive strategy set |
| C4 | Critical | **REQUIRED** | All 10 strategies required; tournament mode |

**Key insight:** S-010 has the LOWEST barrier to entry. It is the ONLY strategy required for C1 Routine work, making it the foundational quality mechanism for Jerry. H-15 mandates self-review before presenting any deliverable.

---

## Purpose

### When to Use

1. **Before presenting any deliverable (H-15 compliance):** Self-review is REQUIRED before showing work to users or external critics. Apply S-010 as the final quality check before submission.

2. **C1 Routine tasks:** For reversible work affecting <3 files in 1 session, S-010 is the only required quality strategy. Use it to catch simple errors before they propagate.

3. **First iteration of creator-critic-revision cycle:** S-010 is often the FIRST adversarial strategy applied. Run self-review before engaging external adversarial critique (S-002, S-004, S-007).

4. **Rapid iteration environments:** When external critique is expensive or slow, S-010 provides fast feedback loops. Use it between major review milestones to maintain quality momentum.

5. **Solo work without external reviewers:** When working independently, S-010 substitutes for peer review. Apply it to catch blind spots and validate assumptions.

### When NOT to Use

1. **As a substitute for external critique at C2+:** Self-review has inherent leniency bias. At C2 Standard and above, S-010 is OPTIONAL because S-007, S-002, and S-014 provide external adversarial perspectives. Do NOT rely solely on S-010 for high-criticality work.

2. **When self-validation echo chamber risk is high:** If you have strong emotional attachment to a solution or have invested significant time, self-review may fail to identify fundamental flaws. Escalate to S-002 (Devil's Advocate) or S-004 (Pre-Mortem) for objectivity.

3. **For governance or constitutional changes (C4):** S-010 alone is insufficient for irreversible decisions. C4 requires all 10 strategies including tournament-mode adversarial critique.

### Expected Outcome

A self-review report containing:
- At least 3 identified weaknesses, gaps, or improvement opportunities
- Evidence-backed findings with specific references to the deliverable
- Concrete revision recommendations prioritized by impact
- Verification that revisions actually improved quality (not just changed it)
- Decision point: ready for external review or needs another iteration

**Quality threshold:** Self-review execution scoring >= 0.92 per S-014 rubric (meta-evaluation of the self-review process itself).

### Pairing Recommendations

1. **S-010 before S-014:** Run self-review BEFORE formal LLM-as-Judge scoring. Self-refine to address obvious gaps, then score to validate improvement.

2. **S-010 before S-002/S-004:** H-16 does not apply to S-010 (it's not an adversarial critique requiring Steelman first), but S-010 SHOULD precede Devil's Advocate or Pre-Mortem to maximize their effectiveness. Present a self-refined deliverable rather than a rough draft.

3. **S-010 + S-007 for C2 Standard:** Combine self-review (S-010) with Constitutional AI Critique (S-007) at C2. Self-review catches surface issues; S-007 catches HARD rule violations.

4. **S-010 iteratively during C3/C4:** For Significant or Critical work, apply S-010 after each revision cycle to verify incremental improvement before the next adversarial strategy.

---

## Prerequisites

### Required Inputs

- [ ] Deliverable artifact to review (document, code, design, plan, etc.)
- [ ] Context about the deliverable's purpose and acceptance criteria
- [ ] Criticality level (C1-C4) to determine required strategies and quality threshold
- [ ] List of relevant HARD rules (from quality-enforcement.md) that apply to this deliverable
- [ ] Scoring dimensions and weights (from quality-enforcement.md SSOT)

### Context Requirements

**Background knowledge assumed:**
- Familiarity with the problem the deliverable addresses
- Understanding of the intended audience and their needs
- Awareness of quality-enforcement.md constants (threshold, dimensions, criticality)

**State required:**
- Deliverable is in a reviewable state (not incomplete or placeholder content)
- Creator has the cognitive capacity to critique objectively (not rushed or fatigued)
- Time allocated for at least 1 revision iteration post-review

### Ordering Constraints

**H-15 compliance:** Self-review MUST occur before presenting deliverables to users or external reviewers.

**Recommended sequence:**
1. Create initial deliverable (creator mode)
2. Apply S-010 Self-Refine (this strategy)
3. Revise based on S-010 findings
4. (Optional) Apply external adversarial strategies (S-002, S-004, S-007, S-014) based on criticality
5. Final revision and acceptance

**No H-16 dependency:** S-010 does NOT require S-003 Steelman first (H-16 applies to adversarial critique, not self-review).

---

## Execution Protocol

### Step 1: Shift Perspective

**Action:** Mentally distance yourself from the creator role and adopt a critical reviewer mindset.

**Procedure:**
1. Take a 5-minute break away from the deliverable (or simulate mental reset by reading unrelated content)
2. Review the deliverable's stated objectives and acceptance criteria
3. Imagine you are reviewing someone else's work — ask "Would I accept this if I didn't create it?"
4. Explicitly acknowledge any emotional attachment or time investment that might bias your review

**Decision Point:**
- If you cannot achieve objectivity (high emotional attachment, time pressure, fatigue), STOP and defer to external adversarial critique (S-002 or S-004)
- If objectivity achieved, proceed to Step 2

**Output:** Mental state shift documented (e.g., "Objectivity check: medium attachment to solution; proceeding with caution")

### Step 2: Systematic Self-Critique

**Action:** Examine the deliverable against scoring dimensions, HARD rules, and acceptance criteria to identify weaknesses.

**Procedure:**
1. **Completeness check (weight: 0.20):** Are all required sections present? Are there unexplored edge cases or unanswered questions?
2. **Internal Consistency check (weight: 0.20):** Are there contradictions between sections? Do examples match the specification?
3. **Methodological Rigor check (weight: 0.20):** Did you follow the prescribed procedure? Are shortcuts or assumptions unjustified?
4. **Evidence Quality check (weight: 0.15):** Are claims backed by specific evidence? Are references accurate and sufficient?
5. **Actionability check (weight: 0.15):** Are recommendations concrete? Can someone else implement them without guessing?
6. **Traceability check (weight: 0.10):** Are source documents linked? Are decisions traceable to requirements?
7. **HARD rule compliance:** Cross-reference quality-enforcement.md HARD rules (H-01 through H-24) relevant to this deliverable type

**Decision Point:**
- If zero findings identified, apply **leniency bias counteraction:** force yourself to find at least 3 improvement opportunities (even minor ones)
- If findings identified, proceed to Step 3

**Output:** Raw list of findings with dimension tags and severity estimates

### Step 3: Document Findings

**Action:** Formalize findings using the standard finding format with evidence and severity classification.

**Procedure:**
1. For each identified weakness, create a finding entry:
   - Assign unique identifier using SR-NNN prefix
   - Classify severity: Critical (blocks acceptance), Major (requires revision), Minor (improvement opportunity)
   - Tag affected dimension(s) from the scoring rubric
   - Provide specific evidence (quote, line number, section reference)
   - Explain why this is a finding (impact on quality or acceptance criteria)
2. Sort findings by severity (Critical first, then Major, then Minor)
3. Map findings to Scoring Impact table (Positive/Negative/Neutral per dimension)

**Finding Documentation Format:**

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| SR-001 | Missing edge case handling for empty input | Major | Section 3 "Input Validation" has no null/empty checks | Completeness |
| SR-002 | Contradictory threshold values | Critical | Page 2 states >=0.92, Page 5 states >=0.90 | Internal Consistency |
| SR-003 | Recommendation lacks implementation steps | Minor | "Improve performance" without specifying how | Actionability |

**Decision Point:**
- If Critical findings exist, revision is MANDATORY before external review
- If only Major/Minor findings, proceed to Step 4 to prioritize revisions

**Output:** Findings table with severity, evidence, and dimension tags

### Step 4: Generate Revision Recommendations

**Action:** Translate findings into concrete, prioritized revision actions.

**Procedure:**
1. For each Critical and Major finding, draft a specific revision recommendation:
   - What to change (precise location and content)
   - Why it matters (impact on acceptance criteria or quality dimensions)
   - How to verify the fix (success criteria)
2. Group recommendations by section or theme for efficient revision
3. Estimate revision effort (time, complexity) to prioritize
4. Identify any recommendations requiring external input or research

**Decision Point:**
- If recommendations require significant rework (>50% of deliverable), consider whether the approach is fundamentally flawed and escalate to S-004 Pre-Mortem or S-013 Inversion
- If recommendations are actionable with current approach, proceed to Step 5

**Output:** Prioritized revision checklist with effort estimates

### Step 5: Revise and Verify

**Action:** Implement revisions and verify that changes actually improved quality.

**Procedure:**
1. Apply revisions in priority order (Critical findings first)
2. After each revision, re-check the affected dimension score:
   - Did the change address the root cause or just the symptom?
   - Did the change introduce new inconsistencies or gaps?
   - Is the revised content measurably better than the original?
3. Update the findings table to mark resolved items
4. Document any findings that could NOT be resolved and why

**Decision Point:**
- If all Critical and Major findings resolved AND dimension scores improved: deliverable ready for external review
- If findings persist or new issues emerged: return to Step 2 for another iteration (H-14 requires minimum 3 iterations for C2+)
- If diminishing returns (iterations not improving quality): escalate to external adversarial critique

**Output:** Revised deliverable with verification notes and unresolved findings list

### Step 6: Decide Next Action

**Action:** Determine whether the deliverable is ready for external review or needs further self-refinement.

**Procedure:**
1. Calculate estimated composite score based on dimension assessments (use S-014 rubric if available)
2. Compare to quality threshold (>= 0.92 for C2+, per H-13)
3. Review unresolved findings and assess risk
4. Check iteration count against H-14 minimum (3 iterations for C2+)

**Decision Point:**
- **Ready for external review:** Score >= 0.92, Critical/Major findings resolved, H-14 iteration count met
- **Another S-010 iteration needed:** Score 0.85-0.91, actionable improvements identified, iteration budget remaining
- **Escalate to external critique:** Score < 0.85, fundamental flaws suspected, or self-review reaching diminishing returns

**Output:** Decision statement with rationale and next recommended strategy (if applicable)

---

## Output Format

Every S-010 Self-Refine execution MUST produce a self-review report with these sections:

### 1. Header

| Field | Value |
|-------|-------|
| Strategy | S-010 Self-Refine |
| Deliverable | {{Title and identifier of reviewed artifact}} |
| Criticality | {{C1/C2/C3/C4}} |
| Date | {{ISO 8601 date}} |
| Reviewer | {{Creator name/ID}} |
| Iteration | {{N of M total iterations}} |

### 2. Summary

2-3 sentence overall assessment answering:
- What is the current quality state of the deliverable?
- What are the most significant findings?
- Is it ready for external review or does it need revision?

### 3. Findings Table

All findings in standard format with severity, evidence, and dimension tags:

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| SR-NNN | {{Description}} | Critical/Major/Minor | {{Specific reference}} | {{Dimension}} |

### 4. Finding Details

Expanded description for each **Critical and Major** finding:
- **SR-NNN: {{Finding title}}**
  - **Severity:** {{Critical/Major}}
  - **Affected Dimension:** {{Dimension name}}
  - **Evidence:** {{Quote or specific reference with location}}
  - **Impact:** {{Why this matters for quality or acceptance}}
  - **Recommendation:** {{How to fix it}}

### 5. Recommendations

Prioritized action list for revision:
1. **{{Critical recommendation}}** (resolves SR-NNN)
2. **{{Major recommendation}}** (resolves SR-NNN, SR-NNN)
3. **{{Minor recommendation}}** (resolves SR-NNN)

### 6. Scoring Impact

Findings mapped to scoring dimensions with impact assessment:

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | SR-001 identifies missing edge case handling |
| Internal Consistency | 0.20 | Negative | SR-002 identifies contradictory thresholds (Critical) |
| Methodological Rigor | 0.20 | Neutral | No methodological shortcuts detected |
| Evidence Quality | 0.15 | Positive | All claims backed by specific references |
| Actionability | 0.15 | Negative | SR-003 identifies vague recommendations |
| Traceability | 0.10 | Neutral | Source document links present |

**Impact values:**
- **Positive:** Dimension meets or exceeds quality threshold based on self-assessment
- **Negative:** Dimension has identified gaps or weaknesses (findings present)
- **Neutral:** Dimension has no significant findings but does not exceptionally excel

### 7. Decision

**Outcome:** {{Ready for external review / Needs revision / Escalate to external critique}}

**Rationale:** {{Why this decision was made, referencing score estimate, findings severity, and iteration count}}

**Next Action:** {{Recommended next step, e.g., "Apply S-007 Constitutional AI Critique" or "Revise per recommendations and re-run S-010"}}

---

## Scoring Rubric

This rubric evaluates the **quality of the S-010 self-review execution itself** (meta-evaluation), not the deliverable being reviewed.

### Threshold Bands

| Band | Score Range | Outcome |
|------|------------|---------|
| PASS | >= 0.92 | Self-review execution accepted; findings are valid and actionable |
| REVISE | 0.85 - 0.91 | Self-review execution requires targeted improvement; close to threshold |
| REJECTED | < 0.85 | Self-review execution inadequate; significant rework required (H-13) |

**Note:** The SSOT threshold is >= 0.92 (H-13). REVISE band is a template-specific operational category for near-threshold deliverables.

### Dimension Weights

Values sourced from quality-enforcement.md SSOT (MUST NOT be redefined):

| Dimension | Weight | Measures (for S-010 execution) |
|-----------|--------|-------------------------------|
| Completeness | 0.20 | All 6 dimensions examined; all deliverable sections reviewed |
| Internal Consistency | 0.20 | No contradictory findings; severity classifications consistent |
| Methodological Rigor | 0.20 | All 6 steps followed; no shortcuts; leniency bias counteracted |
| Evidence Quality | 0.15 | Each finding has specific evidence with location references |
| Actionability | 0.15 | Recommendations concrete, prioritized, implementable |
| Traceability | 0.10 | Findings linked to deliverable sections and scoring dimensions |

### Strategy-Specific Rubric

**Completeness** (weight: 0.20)

| Band | Score | Criteria |
|------|-------|----------|
| Exceptional | 0.95+ | All 6 dimensions examined; all deliverable sections reviewed; leniency bias explicitly counteracted; minimum 3 findings identified even if deliverable is strong |
| Strong | 0.90-0.94 | All 6 dimensions examined; most sections reviewed; at least 2 findings identified |
| Acceptable | 0.85-0.89 | 4-5 dimensions examined; major sections reviewed; at least 1 finding identified |
| Inadequate | <0.85 | <4 dimensions examined; sections skipped; zero findings (leniency bias not counteracted) |

**Internal Consistency** (weight: 0.20)

| Band | Score | Criteria |
|------|-------|----------|
| Exceptional | 0.95+ | No contradictory findings; severity classifications rigorously justified; impact assessments align with evidence |
| Strong | 0.90-0.94 | No contradictions; severity mostly justified; minor alignment gaps |
| Acceptable | 0.85-0.89 | One minor contradiction resolved in notes; severity reasonable |
| Inadequate | <0.85 | Multiple contradictions; severity arbitrary; impact/evidence misaligned |

**Methodological Rigor** (weight: 0.20)

| Band | Score | Criteria |
|------|-------|----------|
| Exceptional | 0.95+ | All 6 steps executed in order; objectivity check documented; leniency bias counteraction explicit; verification of revisions performed |
| Strong | 0.90-0.94 | All 6 steps executed; objectivity check present; revisions verified |
| Acceptable | 0.85-0.89 | 5 steps executed; minor deviations documented; basic verification |
| Inadequate | <0.85 | <5 steps executed; objectivity not established; no verification; self-validation echo chamber evident |

**Evidence Quality** (weight: 0.15)

| Band | Score | Criteria |
|------|-------|----------|
| Exceptional | 0.95+ | Every finding has specific quote/reference with location; evidence is sufficient to justify severity; no vague claims |
| Strong | 0.90-0.94 | Most findings have specific evidence; locations provided; minor vagueness in Minor findings |
| Acceptable | 0.85-0.89 | Major/Critical findings have evidence; some Minor findings lack specifics |
| Inadequate | <0.85 | Findings lack evidence; vague references; cannot locate issues in deliverable |

**Actionability** (weight: 0.15)

| Band | Score | Criteria |
|------|-------|----------|
| Exceptional | 0.95+ | All recommendations specify what/where/how to fix; prioritized by impact; effort estimated; verification criteria provided |
| Strong | 0.90-0.94 | Recommendations concrete and prioritized; most include verification criteria |
| Acceptable | 0.85-0.89 | Recommendations actionable; priority implied; some lack verification criteria |
| Inadequate | <0.85 | Recommendations vague ("improve quality"); no prioritization; no verification criteria |

**Traceability** (weight: 0.10)

| Band | Score | Criteria |
|------|-------|----------|
| Exceptional | 0.95+ | Every finding linked to deliverable section AND scoring dimension; recommendations traceable to findings; decision traceable to scoring estimate |
| Strong | 0.90-0.94 | All findings linked to sections and dimensions; most recommendations traceable |
| Acceptable | 0.85-0.89 | Most findings linked; some dimension tags missing; traceable with effort |
| Inadequate | <0.85 | Findings not linked to deliverable; dimension tags missing; cannot trace recommendations to findings |

---

## Examples

### Example 1: C2 Standard Self-Review of an Architectural Decision Record (ADR)

**Context:** A developer created an ADR for adopting a new caching strategy. The ADR is classified as C2 Standard (reversible in 1 day, affects 5 files). Before presenting to the team, they apply S-010 Self-Refine per H-15.

#### Before (Initial ADR Excerpt)

```markdown
# ADR-023: Implement Redis Caching

## Decision
We will use Redis for caching.

## Rationale
Redis is fast and widely used. It will improve performance.

## Consequences
- Performance will improve
- We'll need to set up Redis
- Cache invalidation strategy needed

## Implementation
1. Install Redis
2. Add caching layer
3. Deploy
```

#### Strategy Execution

**Step 1: Shift Perspective**
- Objectivity check: Medium attachment (invested 30 minutes). Proceeding with caution.

**Step 2: Systematic Self-Critique**
- **Completeness:** Missing alternatives considered, no performance metrics, no failure mode analysis
- **Internal Consistency:** "Cache invalidation strategy needed" listed as consequence but not addressed in implementation
- **Methodological Rigor:** ADR template sections (Context, Options, Risks) skipped
- **Evidence Quality:** "Fast" and "widely used" are unsupported claims
- **Actionability:** "Add caching layer" is too vague
- **Traceability:** No links to requirements or benchmarks

**Step 3: Document Findings**

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| SR-001 | Missing alternatives analysis | Major | ADR template requires "Options Considered" section; none present | Completeness |
| SR-002 | Unsupported performance claims | Major | "Fast" and "improve performance" lack benchmarks or data | Evidence Quality |
| SR-003 | Cache invalidation mentioned but not addressed | Critical | Consequences list "cache invalidation strategy needed" but Implementation has no invalidation steps | Internal Consistency |
| SR-004 | Vague implementation step | Major | "Add caching layer" does not specify where in architecture or which components affected | Actionability |
| SR-005 | No failure mode analysis | Minor | What happens if Redis is unavailable? No fallback mentioned | Completeness |

**Step 4: Generate Revision Recommendations**

1. **Add "Alternatives Considered" section** (resolves SR-001) — Effort: 15 min — Compare Redis vs Memcached vs in-process cache with trade-off analysis
2. **Provide performance benchmarks** (resolves SR-002) — Effort: 10 min — Link to existing benchmarks or create simple test showing latency improvement
3. **Define cache invalidation strategy** (resolves SR-003) — Effort: 20 min — Add subsection under Implementation specifying TTL values, invalidation triggers, and consistency approach
4. **Expand implementation steps** (resolves SR-004) — Effort: 10 min — Specify which API endpoints get caching, cache key structure, configuration parameters
5. **Add failure mode handling** (resolves SR-005) — Effort: 5 min — Document graceful degradation if Redis unavailable

**Step 5: Revise and Verify**
- Applied all 5 recommendations
- Re-checked Internal Consistency: SR-003 resolved (cache invalidation now in Implementation section)
- Re-checked Evidence Quality: SR-002 resolved (linked to Redis benchmark study)
- Unresolved findings: None

**Step 6: Decide Next Action**
- Estimated score: 0.93 (all Critical/Major findings resolved)
- Iteration count: 1 of 3 minimum (C2 requires H-14 compliance)
- Decision: Ready for S-007 Constitutional AI Critique to check HARD rule compliance before team presentation

#### After (Revised ADR Excerpt)

```markdown
# ADR-023: Implement Redis Caching for Read-Heavy API Endpoints

## Context
Our API serves 10K req/sec with 80% read traffic. Database query latency averages 50ms, causing P95 response times of 200ms. We need sub-100ms P95 to meet SLA.

## Decision
We will use Redis for caching read responses on high-traffic endpoints (/products, /users).

## Alternatives Considered
| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Redis | Fast (sub-1ms), mature, persistence | Additional infrastructure | SELECTED |
| Memcached | Slightly faster, simple | No persistence, limited data structures | Not chosen |
| In-process cache | No external deps | Memory limits, no sharing across instances | Not chosen |

## Rationale
Redis benchmarks show 0.8ms P95 latency (source: redis.io/topics/benchmarks). With 80% cache hit rate, projected P95 drops to 60ms (0.8ms * 0.8 + 50ms * 0.2 = 10.64ms cached + 10ms uncached = 20.64ms blended).

## Consequences
- **Positive:** 70% latency reduction, SLA compliance
- **Negative:** Operational complexity (Redis cluster management), cache invalidation strategy required
- **Risks:** Cache stampede on invalidation, stale data if TTL misconfigured

## Implementation
1. Install Redis cluster (3 nodes for HA)
2. Add caching layer in API middleware:
   - Cache keys: `{endpoint}:{resourceID}:{version}`
   - TTL: 5 minutes (products), 10 minutes (users)
3. Implement cache invalidation:
   - On UPDATE/DELETE: invalidate specific key
   - On schema change: bump version in key
4. Fallback: On Redis unavailable, bypass cache and query database (graceful degradation)
5. Deploy with feature flag, monitor cache hit rate and P95 latency

## Failure Modes
- Redis down: API continues with database queries (slower but functional)
- Cache stampede: Use probabilistic early expiration (PER) to stagger refreshes
```

#### Findings Summary

**Scoring Impact:**

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative → Positive | SR-001 resolved (alternatives added); SR-005 resolved (failure modes added) |
| Internal Consistency | 0.20 | Negative → Positive | SR-003 resolved (cache invalidation now addressed in Implementation) |
| Methodological Rigor | 0.20 | Neutral | ADR template followed after revision |
| Evidence Quality | 0.15 | Negative → Positive | SR-002 resolved (benchmarks and SLA calculations provided) |
| Actionability | 0.15 | Negative → Positive | SR-004 resolved (implementation steps now concrete with cache key format, TTL values) |
| Traceability | 0.10 | Neutral → Positive | Added source link to Redis benchmarks, linked to SLA requirement |

**Outcome:** Deliverable improved from estimated 0.65 to 0.93. Ready for S-007 Constitutional AI Critique.

---

## Integration

### Canonical Pairings

1. **S-010 → S-014 (Self-Refine then Score):** Apply self-review to address obvious gaps before formal LLM-as-Judge scoring. This reduces scoring iterations and improves efficiency.

2. **S-010 → S-007 (Self-Refine then Constitutional Check):** At C2, run self-review first to catch surface issues, then S-007 to validate HARD rule compliance. This layered approach catches both quality gaps and governance violations.

3. **S-010 → S-002 (Self-Refine then Devil's Advocate):** Self-review before adversarial critique ensures you present a refined deliverable rather than a rough draft. S-002 can then focus on deeper logical flaws rather than obvious errors.

4. **S-010 iteratively with S-004/S-012/S-013 at C3:** For Significant work, apply S-010 after each revision cycle (e.g., after Pre-Mortem findings are addressed) to verify incremental improvement before the next strategy.

### H-16 Compliance

**H-16 does NOT apply to S-010.** H-16 (Steelman before critique) requires S-003 Steelman Technique before adversarial critiques like S-002, S-004, S-001. S-010 is NOT an adversarial critique — it is self-review by the creator. Therefore, S-003 is NOT required before S-010.

However, **S-010 SHOULD precede adversarial critiques** to maximize their effectiveness (present refined work rather than rough drafts).

### Criticality-Based Selection Table

Values sourced from quality-enforcement.md SSOT:

| Level | Required Strategies | Optional Strategies | S-010 Status |
|-------|---------------------|---------------------|--------------|
| C1 | S-010 | S-003, S-014 | **REQUIRED** (only required strategy) |
| C2 | S-007, S-002, S-014 | S-003, S-010 | Optional (external critique preferred) |
| C3 | C2 + S-004, S-012, S-013 | S-001, S-003, S-010, S-011 | Optional (comprehensive set) |
| C4 | All 10 selected | None | **REQUIRED** (all strategies required) |

**Key insight:** S-010 is the ONLY required strategy at C1, making it the baseline quality mechanism. At C2+, external adversarial strategies take precedence, but S-010 remains useful for rapid iteration.

### Cross-References

- **SSOT:** `.context/rules/quality-enforcement.md` (thresholds, weights, criticality levels, strategy catalog)
- **Related Templates:**
  - S-014 LLM-as-Judge (scoring mechanism for S-010 execution and deliverable quality)
  - S-007 Constitutional AI Critique (HARD rule compliance check, often paired with S-010 at C2)
  - S-003 Steelman Technique (NOT required before S-010, but improves adversarial critique effectiveness)
- **Academic Source:** Madaan et al. 2023 "Self-Refine: Iterative Refinement with Self-Feedback"
- **HARD Rules:** H-15 (self-review before presenting), H-13 (quality threshold >= 0.92), H-14 (minimum 3 iterations for C2+)
- **Format Standard:** TEMPLATE-FORMAT.md v1.1.0

---

<!-- TEMPLATE NOTES: This template instantiates TEMPLATE-FORMAT.md v1.1.0 for S-010 Self-Refine strategy. Academic foundation: Madaan et al. 2023 demonstrates LLM self-improvement through structured feedback loops. Jerry implementation: H-15 mandates self-review before presenting deliverables. VERSION: 1.0.0 | CREATED: 2026-02-15 | ENABLER: EN-804 -->
