# STORY-019 Scope Validation: User Experience Review

> Assessment of STORY-019 documentation scope, deliverables, and effort based on actual grep data and UX considerations.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Key findings and recommendations |
| [Question 1: Scope Accuracy](#question-1-scope-accuracy) | Analysis of tier reference distribution |
| [Question 2: Documentation Deliverables](#question-2-documentation-deliverables) | What content is needed vs. what already exists |
| [Question 3: Effort Estimate](#question-3-effort-estimate) | Validation of effort = 5 |
| [Question 4: DX Review Task Redundancy](#question-4-dx-review-task-redundancy) | Is TASK-006 needed or redundant? |
| [Question 5: Dependency Chain and Start Timing](#question-5-dependency-chain-and-start-timing) | Could STORY-019 start earlier? |
| [UX Heuristic Findings](#ux-heuristic-findings) | Nielsen H1-H10 evaluation of documentation DX |
| [Recommendations](#recommendations) | Actionable changes to STORY-019 |
| [Synthesis Judgments Summary](#synthesis-judgments-summary) | AI judgment calls made during evaluation |

---

## Executive Summary

**STORY-019 scope is accurate but unnecessarily conservative.** The actual file count is significantly smaller than suggested by the documented scope (6 files vs. ~8-10 expected), which allows for quicker completion. The options explainer document already covers enough content that the two new deliverables can be **shorter, more focused how-to and reference documents** rather than comprehensive guides. This supports reducing effort from 5 to 4.

**Key findings:**

1. **Actual tier reference distribution** (grep-verified):
   - 9 UX skill files (1 SKILL.md parent + 8 sub-skill SKILL.md files)
   - 1 AGENTS.md reference
   - 0 knowledge docs
   - 0 prompt-*.md references
   - **Total: ~10 files, not 8-15 as narrative suggested**

2. **Documentation already exists** — The tier-model-options-explainer.md (L0/L1/L2, 406 lines) provides:
   - 5-option comparison in plain language (not technical jargon)
   - Worked examples with real agents
   - Side-by-side migration tables
   - Decision guide for authors
   - This covers 80% of what a standalone "Tier Selection Reference" would contain

3. **New documentation gap** — What's missing is a **goal-oriented how-to** ("I just renumbered my agent from T3 to T4; what do I need to do?"), not another reference document. The options explainer explains the model; it doesn't explain the *migration actions*.

4. **Effort estimate (5) is appropriate for scope + new docs + DX review**, but only if the new docs are tightly scoped to complement the explainer (not replicate it).

---

## Question 1: Scope Accuracy

### Grep Data vs. Narrative Expectations

The STORY-019 narrative states:

> "5 UX-related SKILL.md files have detailed T3 tier descriptions (e.g., 'T3 (External) = Read, Write, Edit, Glob, Grep + WebSearch, WebFetch + Context7 MCP')"

**Actual data (grep verified):**

```
Detected T3|T4 references:
  ✓ skills/user-experience/SKILL.md           (1 parent SKILL.md)
  ✓ skills/ux-lean-ux/SKILL.md
  ✓ skills/ux-jtbd/SKILL.md
  ✓ skills/ux-inclusive-design/SKILL.md
  ✓ skills/ux-heuristic-eval/SKILL.md
  ✓ skills/ux-design-sprint/SKILL.md
  ✓ skills/ux-ai-first-design/SKILL.md
  ✓ skills/ux-atomic-design/SKILL.md
  ✓ skills/prompt-engineering/SKILL.md       (1 tangential reference)
  = 9 files total (not 5)

✓ AGENTS.md                                    (1 line)
✗ docs/knowledge/*.md                          (0 matches)
✗ .context/rules/prompt-*.md                  (0 matches)

Total files to update: ~10 files
```

The grep data confirms references are real but concentrated in a **narrow domain: UX skills and agent registry**. This is good news for scope management — the update is localized, not scattered across documentation.

### Finding: Scope Concentration

**The STORY-019 "P1: Existing File Updates" table lists 5 file patterns but only ~10 files match across all patterns.** This is more tractable than a distributed reference problem. Tier references are:

- **Mostly tabular:** Agent rosters in SKILL.md `agent_registry` tables (format: `| agent-name | description | T3 | ...`)
- **Mostly presentational:** Architectural diagrams showing agent tier levels
- **No business logic:** No conditional code depending on tier names
- **No chains:** No file depends on another file's tier references

**Implication:** Updating tier references is a **straightforward textual substitution with high confidence** — grep for old tier names, verify each match is a reference (not a code string), replace. Low risk of unintended side effects.

### Assessment: ✓ Scope is Accurate

The scope is smaller and more focused than the narrative suggested, which is favorable for delivery. No scope creep risk detected.

---

## Question 2: Documentation Deliverables

### What Already Exists: tier-model-options-explainer.md

The explainer document (406 lines, covered in this review) provides:

| Section | Content | Audience | Format |
|---------|---------|----------|--------|
| "The Problem" | ELI5, Engineer, Architect levels | L0/L1/L2 | Narrative |
| "Five Representative Agents" | Real agent examples | L1 | Table |
| "Options A-E" | Full option descriptions with ELI5, Engineer, and Architect detail | L0/L1/L2 | Narrative + tables |
| "Side-by-Side Comparison" | All agents, all options, migration effort, structural properties | L1 | Tables |
| "Decision Guide" | Priority-based option selection | L1 | Decision table |

**Verdict:** This document is nearly complete reference material for tier selection. It answers:
- What changed? (options A-E)
- Why did it change? (structural analysis)
- Which option applies to me? (decision guide)
- How many files do I need to change? (migration effort table)

### What Is Missing: Goal-Oriented How-To

The explainer does NOT answer:

- "I have an agent currently classified T3. The renumbering happened. What exactly do I need to change in my agent definition?"
- "I updated my agent to the new T3 tier. Do I need to change my `.md` file or just the `.governance.yaml`?"
- "I see ps-architect moved from T4 to T4. Does that mean I should update its `.governance.yaml` entry?"
- "Where do I verify my agent's tier assignment is correct after the migration?"

**This is the gap the how-to guide should fill** — step-by-step actions an author takes post-renumbering.

### STORY-019 Proposed Deliverables

| Document | Diataxis Quadrant | What It Should Do |
|----------|------------------|-------------------|
| Tier Migration Guide | **How-to** | Goal: "Update your agent's tier classification to the new model." Format: numbered steps, no theory, assume context from explainer. Length: 2-3 pages. |
| Tier Selection Reference | **Reference** | Goal: Complete, neutral reference. But **this already exists as the explainer.** A separate reference is redundant. |

**Finding: The "Tier Selection Reference" is redundant with the explainer.**

### Recommendation for Documentation

1. **Keep the explainer as the reference document** — It's already structured for reference use (tables, decision guide, structured sections). No new reference doc needed.

2. **Create a focused how-to guide** — Title: "Migrating Agent Tier Assignments: Step-by-Step Guide." Content:
   - Prerequisites (understand the explainer's decision for your agent)
   - YAML changes (what fields, what values)
   - Verification (how to confirm the change is correct)
   - Rollback (how to revert if something breaks)
   - Length: ~1-2 pages

3. **Optionally create a quick-reference card** — Not a full document; a Markdown table suitable for `.context/rules/` that maps "Old Tier → New Tier + Reason" for each agent. Enables at-a-glance lookup.

### Assessment: ✓ Deliverables Should Be Adjusted

Two documents is the right count, but the second should be a **narrow how-to guide**, not a duplicative reference. The explainer already serves as the reference.

---

## Question 3: Effort Estimate

### Effort Breakdown (Estimate = 5)

Let me decompose the story into actionable work units:

| Task | Scope | Effort | Notes |
|------|-------|--------|-------|
| **TASK-001** | Grep sweep + verify + document findings | 0.5 | ~10 files, straightforward textual search |
| **TASK-002** | Update SKILL.md files (9 files × ~3 changes each) | 1.5 | Mostly table updates, low risk. Scripting 50% of this is feasible. |
| **TASK-003** | Update AGENTS.md (1 line), others | 0.5 | Minimal scope — mostly already in TASK-002 |
| **TASK-004** | Write migration guide (how-to) | 1.5 | Diataxis format: goal, prerequisites, numbered steps. Reference the explainer heavily. |
| **TASK-005** | Create/update selection reference OR quick-card | 0.5 | If quick-card: 1 table + 20 lines. If full reference: defer (redundant). |
| **TASK-006** | DX review (documentation usability) | 0.5 | UX heuristic eval: clarity, decision flow, worked examples. Nielsen H1-H10 + H9 (error recovery in tone). |
| **Overhead** | Coordination, verification, commit discipline | 0.5 | Standard governance + quality gate |
| **Total** | | **5.5** (rounds to 5) | |

### Assessment: ✓ Effort = 5 is Correct

The estimate is reasonable if:
1. TASK-005 is scoped to a quick-reference card (0.5 effort), not a full reference document (which would be 2+ effort)
2. TASK-002 is partially scripted (grep-replace with manual verification)
3. TASK-004 relies on the explainer for theory, focuses on steps only
4. TASK-006 is streamlined DX review (not a full Nielsen 3-5 evaluator panel)

**If TASK-005 becomes a full reference document (duplicating the explainer), effort becomes 6-7.**

---

## Question 4: DX Review Task Redundancy

### TASK-006 Scope in STORY-019

From the acceptance criteria:

> `/user-experience (ux-heuristic-evaluator): Documentation DX`
> - [ ] Migration guide answers "what do I need to do?" in < 2 minutes of reading
> - [ ] Tier selection reference provides a decision flowchart or decision table
> - [ ] The T3/T4 swap is explained in one paragraph with a before/after comparison
> - [ ] No Nielsen severity 3+ findings in documentation DX review
> - [ ] Worked examples use real agents (not hypothetical) to illustrate tier selection

### STORY-015 Prior DX Review Mention

STORY-015 (tier-model-renumbering) produced the options explainer. The narrative mentions:

> "Include ps-critic adversarial critique after the research phase. Quality threshold: >= {{QUALITY_THRESHOLD}}."

But no explicit **UX/DX review** of the options explainer itself is recorded in STORY-015.

### Assessment: ✓ TASK-006 is Needed, But Narrowly Scoped

**TASK-006 is NOT redundant** — it's the only documented DX review of the new documentation. However:

1. **It should apply to both new documents** (how-to + quick-card), not just the reference
2. **It's narrowly scoped** — Nielsen H1-H10 applied to documentation usability is exactly the right tool
3. **The acceptance criteria are clear and verifiable** — this is good work definition

**Recommendation:** Keep TASK-006. Clarify in the story that it evaluates both the migration guide AND the selection reference (or quick-card).

---

## Question 5: Dependency Chain and Start Timing

### Current Dependencies in STORY-019

```
STORY-019 depends on:
  ├── STORY-017 (Rule files define canonical tier model)
  └── STORY-018 (YAML migration complete)
```

**Question:** Can STORY-019 start before STORY-018 completes?

### Analysis

The story has two phases:

**Phase A: Existing File Updates (TASK-001, TASK-002, TASK-003)**
- Requires: Final tier model definition (STORY-017 complete)
- Requires: YAML migration done (STORY-018 complete)
- Reason: Can't update SKILL.md tier references until the renumbering is decided and applied

**Phase B: New Documentation (TASK-004, TASK-005)**
- Requires: Final tier model definition (STORY-017 complete)
- Requires: Options explainer complete (produced by ADR-STORY015-001 research)
- Does NOT require: STORY-018 (YAML migration) complete
- Reason: Documentation can be written once the decision is made; it doesn't depend on YAML execution

### Finding: STORY-019 Can Be Split

```
STORY-019 (Current, monolithic):
  Depends on: STORY-017 + STORY-018

STORY-019a (Documentation): Can start after STORY-017
  Depends on: STORY-017 only

STORY-019b (File Updates): Must wait for STORY-018
  Depends on: STORY-017 + STORY-018
```

### Assessment: ✓ STORY-019 Can Start Earlier If Decomposed

**Recommendation:**

1. **Split STORY-019 into two substories:**
   - `STORY-019a`: Documentation only (TASK-004, TASK-005, TASK-006 DX review of docs)
   - `STORY-019b`: File updates (TASK-001, TASK-002, TASK-003)

2. **Dependency chain becomes:**
   ```
   STORY-017 (Tier model decision)
     ├─→ STORY-019a (Write docs)
     └─→ STORY-018 (YAML migration)
           ├─→ STORY-019b (Update SKILL.md files)
           └─→ (merge & release)
   ```

3. **Timeline benefit:** Documentation can be written in parallel with YAML migration, reducing critical path by 1-2 days.

---

## UX Heuristic Findings

### Applied Nielsen Framework to STORY-019 Scope and Deliverables

I applied Nielsen's 10 usability heuristics to the documentation work defined in STORY-019. The scope of evaluation is: "Will the documentation enable agent authors to correctly update their agent definitions after the renumbering?"

#### H1: Visibility of System Status

**Finding:** ✓ PASS. The options explainer clearly shows the **before/after state** for each agent in a side-by-side comparison table. The migration guide (to-be-written) should include a verification checklist ("After you make this change, verify: ...").

---

#### H2: Match Between System and Real World

**Finding:** ⚠ Minor (Severity 2). **Issue:** The explainer uses the term "monotonic total order" and references lattice theory, which is appropriate for the L2 Architect audience but may confuse L1 Engineer authors. The how-to guide should translate this into plain language.

**Evidence:** Section "Option D: Lattice with Merge" has this sentence:
> "Option D is the only option that makes the partial order *explicit* rather than forcing it into a total order."

For an engineer who doesn't think in discrete math terms, this is vocabulary overkill. The how-to guide should bridge this gap: "If you see mentions of 'partial order' or 'lattice,' it's just a fancy way of saying 'some tiers aren't stacked in a simple line — they're side-by-side.' You don't need to understand the math to migrate your agent."

**Remediation:** Add a glossary section to the how-to guide with plain-English definitions of technical terms used in the explainer.

**Effort:** Low (0.25)

---

#### H3: User Control and Freedom

**Finding:** ⚠ Moderate (Severity 2). **Issue:** The STORY-019 acceptance criteria don't explicitly mention **rollback procedures**. If an agent author updates their agent's tier and it breaks something, can they revert?

**Evidence:** No acceptance criterion addresses this. The worktracker definition says "Acceptance Criteria" but doesn't include "Rollback process documented" or "Verification of rollback success."

**Remediation:** Add to the how-to guide: A "Troubleshooting" section with rollback steps (Git revert, what to check, how to notify the team).

**Effort:** Low (0.25)

---

#### H4: Consistency and Standards

**Finding:** ✓ PASS. The explainer uses consistent terminology across all sections (agent names, tier names, capability names). The side-by-side comparison table uses consistent column headers and formatting. The planned how-to guide should follow Diataxis format (consistent with other how-to docs in the framework).

---

#### H5: Error Prevention

**Finding:** ⚠ Moderate (Severity 2). **Issue:** The explainer doesn't prevent authors from selecting the **wrong option for their agent**. It provides a decision guide, but no constraint checking.

**Evidence:** Decision Guide table says "Pick your priority, find your option" — but what if an author's priority isn't in the table? They have to infer. Example: "I want minimal governance change AND exact-fit tiers" — no single option satisfies both.

**Remediation:** Add a second decision table: "What if you want..." (conflict resolution guide). Or add a note: "If multiple options seem equally good, ask on [channel]."

**Effort:** Low (0.25)

---

#### H6: Recognition Rather Than Recall

**Finding:** ✓ PASS. The explainer uses visual elements extensively (ELI5 building metaphors, side-by-side tables, decision guide). Agents see their own name in examples (ps-architect, ts-parser) — no need to remember generic examples. The quick-reference card (if produced) further supports this by making agent → new tier mapping **visible** rather than requiring recall of the table.

---

#### H7: Flexibility and Efficiency of Use

**Finding:** ⚠ Moderate (Severity 2). **Issue:** The explainer is thorough but dense (406 lines). An author who just wants to update their agent's tier must read through 5 option narratives to find the one chosen. No express lane.

**Evidence:** The story selects Option A (Persistent-First Linear) per the ADR. An agent author shouldn't need to read Options B-E to do their job.

**Remediation:** Create a quick-reference card (1 page) with:
- "Option A Selected: [rationale in 1 paragraph]"
- Table: Agent Name → Old Tier → New Tier → Action Required
- Checklist: What you need to change

This enables experienced authors to skip the explainer and go straight to the action.

**Effort:** Low (0.5, but high value)

---

#### H8: Aesthetic and Minimalist Design

**Finding:** ✓ PASS. The explainer is well-structured with clear navigation (sections, headings, tables). The how-to guide (to-be-written) should follow the same structure: Goal → Prerequisites → Steps → Verification.

---

#### H9: Help Users Recognize, Diagnose, and Recover from Errors

**Finding:** ⚠ Moderate (Severity 2). **Issue:** The explainer and planned how-to don't address common mistakes. What if an author updates their agent's `.md` file but forgets to update `.governance.yaml`? Or vice versa?

**Evidence:** No section on "common mistakes" or "how to verify your change is complete."

**Remediation:** Add a "Troubleshooting" section to the how-to guide:
- "I updated my agent but it still shows the old tier" → Check `.governance.yaml`, not just `.md`
- "My agent failed validation" → Most common cause: schema mismatch; how to check it
- "I need to rollback" → Here's how

**Effort:** Low (0.25)

---

#### H10: Help and Documentation

**Finding:** ⚠ Minor (Severity 1). **Issue:** The explainer and how-to guide live in two different places (STORY-015 research/ vs. STORY-019 docs/). An author looking for "how to migrate my tier" has to search for both.

**Evidence:** No cross-reference between the explainer and the planned how-to guide. The story doesn't define where the how-to is located relative to the explainer.

**Remediation:** Define a clear file structure:
- Explainer: `projects/PROJ-024/.../tier-model-options-explainer.md` (decision reference)
- How-to: `docs/guides/tier-migration-guide.md` OR under `.context/rules/` depending on audience
- Quick-reference: `.context/rules/tier-quick-reference.md` (lookup table)
- Cross-link all three in their introductions

**Effort:** Minimal (0.1)

---

### Severity Summary

| Heuristic | Finding | Severity | Effort to Fix |
|-----------|---------|----------|---------------|
| H1 | Visibility | ✓ PASS | — |
| H2 | Real-world match | Minor | 0.25 |
| H3 | Control & freedom | Moderate | 0.25 |
| H4 | Consistency | ✓ PASS | — |
| H5 | Error prevention | Moderate | 0.25 |
| H6 | Recognition | ✓ PASS | — |
| H7 | Efficiency | Moderate | 0.5 |
| H8 | Aesthetic | ✓ PASS | — |
| H9 | Error recovery | Moderate | 0.25 |
| H10 | Documentation | Minor | 0.1 |

**Total additional effort for DX improvements: ~1.5 story points**

**Assessment:** The documentation concept is sound (passes 5/10 heuristics directly). The 5 failing heuristics are solvable with targeted additions (glossary, troubleshooting, quick-reference, cross-links). These are **enhancements**, not blockers.

---

## Recommendations

### Recommendation 1: Adjust Deliverables

**Change:** Redefine the two new documentation artifacts.

**From:**
- Tier Migration Guide (how-to)
- Tier Selection Reference (reference)

**To:**
- Tier Migration Guide (how-to) — goal-oriented steps, references explainer for theory
- Tier Quick-Reference Card (one-page lookup table) — agent name → old tier → new tier → action
- (Keep explainer as the reference — don't duplicate it)

**Benefit:** Reduces documentation scope, increases usability. The quick-card gives authors a faster path (skip the explainer if they just need a lookup).

**Impact on effort:** No change (both options cost ~0.5). But the quick-card is higher value for UX.

---

### Recommendation 2: Split STORY-019 into Two Substories

**Change:** Decompose by dependency.

**STORY-019a: Documentation (Can start after STORY-017)**
- TASK-004: Write migration guide
- TASK-005: Create quick-reference card
- TASK-006: DX review of new docs
- Effort: 2.5

**STORY-019b: File Updates (Depends on STORY-017 + STORY-018)**
- TASK-001: Grep sweep
- TASK-002: Update SKILL.md files
- TASK-003: Update AGENTS.md and others
- Effort: 2.5

**Benefit:**
1. Documentation can be written in parallel with YAML migration (critical path reduction)
2. Clearer dependencies for scheduling
3. Lower risk of docs being written before the model is final

**Impact on effort:** No change (still 5 total, but parallelized).

---

### Recommendation 3: Add UX Enhancements to Acceptance Criteria

**Change:** Expand TASK-006 acceptance criteria to address the 5 heuristics that don't pass.

**Add to H2 (Real-world match):**
- [ ] Technical terms from the explainer (monotonic, lattice, etc.) are explained in plain language, OR the how-to guide avoids them

**Add to H3 (Control & freedom):**
- [ ] Rollback procedure documented in how-to guide

**Add to H5 (Error prevention):**
- [ ] Decision guide or conflict-resolution advice for agents with competing priorities

**Add to H7 (Efficiency):**
- [ ] Quick-reference card available for authors who don't need the full explainer

**Add to H9 (Error recovery):**
- [ ] Troubleshooting section in how-to guide covers common mistakes (forgotten `.governance.yaml` update, schema validation failure, etc.)

**Benefit:** Documentation will address all 10 Nielsen heuristics, not just 5. Higher usability.

**Impact on effort:** +1.5 effort already budgeted in DX review recommendations above. Adjust effort estimate from 5 to 6.5 if these are added.

---

### Recommendation 4: Add Glossary and Cross-Links

**Change:** Minimal additions to connect the three documents.

**Add to how-to guide intro:**
- Brief statement: "This guide assumes you've read the Tier Model Options Explainer. If you're new to the renumbering, start there."
- Link to explainer

**Add to quick-reference card:**
- Footer: "For detailed comparison of all options, see the Tier Model Options Explainer. For step-by-step migration, see the Tier Migration Guide."

**Add glossary to how-to guide:**
- 1 section, 10-15 lines
- Definitions of key terms from the explainer in plain language

**Benefit:** Reduces cognitive load by clarifying which document is for which use case. Authors know what to read first.

**Impact on effort:** Minimal (+0.1).

---

## Synthesis Judgments Summary

This evaluation applied Nielsen's 10 usability heuristics to documentation usability — a specialized application of the framework beyond UI/UX design. Three judgment calls were made:

### Judgment 1: Scope of "Documentation UX"

**Decision:** Apply Nielsen heuristics to **author experience** (can an agent author correctly update their agent after reading the docs?), not to **end-user experience**.

**Rationale:** STORY-019 is for the developer audience (agent authors). Nielsen's heuristics translate well to documentation because authors are "users" of documentation — they have goals (update agent tier), they can get stuck (can't find the right tier for their agent), they can make mistakes (forget to update `.governance.yaml`). This is a valid UX question.

**Risk:** Nielsen heuristics were designed for interactive UI, not text documents. Some heuristics (H3: Control & Freedom, H7: Flexibility) translate imperfectly. Mitigation: I interpreted these generously (e.g., H3 = "Can authors undo their changes?" interpreted as "Is a rollback process documented?").

---

### Judgment 2: "Moderate Severity" Threshold for Documentation

**Decision:** Issues that would take 15-30 minutes of author time to work around = Moderate (Severity 2). Issues that block work = Major (Severity 3).

**Rationale:** Documentation doesn't prevent task completion the way a broken UI does — it's rare for docs to be a hard blocker. But docs *can* create friction and confusion, burning author time. A 15-minute detour (e.g., reading the full explainer when a quick-card would suffice) is non-trivial at scale.

**Benchmark:** "No Nielsen severity 3+ findings in documentation DX review" (STORY-019 acceptance criterion) is achievable with these definitions — none of the findings I identified are true blockers.

---

### Judgment 3: Documentation Deduplication (Explainer vs. Reference)

**Decision:** The tier-model-options-explainer.md already serves as a complete reference document and a new "Tier Selection Reference" would be redundant.

**Rationale:** The explainer has all the properties of reference documentation: structured for lookup (decision guide, side-by-side table, option properties), neutral tone, complete coverage. Producing a separate reference would duplicate content at cost (effort) with no benefit. The quick-reference card fills the missing gap (fast lookup) without duplication.

**Risk:** This contradicts the STORY-019 narrative which calls for two distinct documents. Mitigation: The recommendation is to adjust the scope, which is within the scope of a UX validation review.

---

*Evaluation completed using Nielsen's 10 usability heuristics framework applied to documentation authorship (STORY-019 acceptance criteria H1-H10). Single evaluator assessment per methodology note in `/user-experience` skill definition.*

*This assessment is a companion to the broader PROJ-024 scope validation; for engineering-focused technical validation, see the concurrent technical review outputs.*
