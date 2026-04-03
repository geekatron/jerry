# eng-lead Feasibility Assessment: STORY-016 through STORY-020 + EN-004

> **Produced by:** eng-lead (Engineering Lead, /eng-team)
> **Date:** 2026-03-28
> **Scope:** Implementation feasibility, dependency accuracy, effort estimates, task granularity, and defect identification for the Option A (Persistent-First Linear) tier model renumbering implementation plan.
> **Standard alignment:** MS SDL Requirements phase, NIST SSDF PO.1/PO.3/PS.1/PS.2, OWASP SAMM Implementation practice.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Decision-ready summary of findings |
| [L1 Technical Detail](#l1-technical-detail) | Per-story analysis, defects, and recommendations |
| [L2 Strategic Implications](#l2-strategic-implications) | Technical debt, SAMM maturity, long-term considerations |

---

## L0 Executive Summary

**Overall feasibility:** FEASIBLE with three mandatory corrections before implementation begins.

**Implementation readiness:** The 6 stories are structurally sound. The dependency chain is coherent, the task decomposition is appropriate, and the migration approach (3-step T3_HOLD pattern) is technically correct. Three defects require correction before work starts; none are blockers to the overall approach.

**Key decisions required:**

| # | Decision | Owner | Urgency |
|---|----------|-------|---------|
| D-001 | Should STORY-017 and STORY-018 merge into one story? | adam.nowak | Before STORY-016 completes |
| D-002 | Can STORY-019 (docs) start from the ADR alone, parallel to STORY-017? | adam.nowak | Before STORY-016 completes |
| D-003 | Accept T2 count discrepancy (29 actual vs 28 in story) as a pre-existing data error? | adam.nowak | Before STORY-018 begins |

**Defects requiring correction:**

| ID | Severity | Story | Defect |
|----|----------|-------|--------|
| DEF-001 | HIGH | STORY-018 | sed migration script will silently skip diataxis-explanation.governance.yaml (inline comment on tool_tier line breaks end-of-line anchor) |
| DEF-002 | MEDIUM | STORY-018 | T2 count stated as 28 but actual count is 29; post-migration verification check will fail spuriously |
| DEF-003 | MEDIUM | STORY-020 | H-35 reference is stale (H-35 was retired into H-34 sub-item b per EN-002); should reference H-34 |

**Effort estimate verdict:** All estimates are reasonable. STORY-017 at effort=5 is the most uncertain (C4 quality gate + UX review are unpredictable in iteration count).

---

## L1 Technical Detail

### STORY-016: Add Option E to Tier Model ADR

**Feasibility:** FEASIBLE. Straightforward ADR extension work.

**Dependency accuracy:** Correctly depends on STORY-015 (ADR exists), correctly blocks STORY-017 and STORY-018. No issues.

**Effort estimate (3):** Appropriate. Option E evaluation section is described in the tier-model-options-explainer.md already; the work is adding it to the ADR matrix and re-running the C4 adversarial score. Three tasks map cleanly to the three acceptance criterion groups.

**Task granularity (3 tasks):** Correctly sized. TASK-001 and TASK-002 can be done in a single agent pass; keeping them separate is defensible because the matrix update is verifiable independently from the prose addition.

**Gap identified:** The acceptance criteria for the C4 re-score (TASK-003) do not specify whether the existing iteration artifacts (adversarial-review-iteration-1.md through -5.md) should be preserved or a new iteration sequence started. Recommend clarifying: start a new iteration sequence (adversarial-review-iteration-6.md) rather than modifying the existing chain, to preserve the decision audit trail.

**Missing task:** No task explicitly updates the options-explainer cross-reference. The explainer already has Option E; the ADR will now too. A 5-line cross-reference update in the explainer confirming "see ADR for full evaluation" costs under 10 minutes and avoids future confusion. SOFT recommendation to add.

**Standards mapping:**
- MS SDL Requirements: Option E evaluation closes an open options gap before baseline is set. Required for a complete decision record.
- NIST SSDF PO.1.1: Security requirements for the tier model must consider all identified options. Option E has distinct failure modes (schema complexity) not present in Options A-D.

---

### STORY-017: Implement P0 Rule File Changes for Tier Renumbering

**Feasibility:** FEASIBLE. The scope is well-defined with exact section-level change tables.

**Dependency accuracy:** Correctly depends on STORY-016 (finalized ADR). The claim that STORY-018 must wait for STORY-017 is valid: YAML files should not reference tier values that the rule files have not yet defined.

**Question D-001 addressed (merge with STORY-018?):** The ADR states "Changes are atomic: both files updated in the same commit." This is a commit-level atomicity requirement, not a story-level scope requirement. Stories decompose work by *type of change* (governance rules vs. mechanical data migration), not by commit boundary. The rule file changes (STORY-017) require C4 adversarial review of prose and UX review of selection guidelines -- skills and scrutiny that are different from the bulk YAML migration (STORY-018). Keeping them separate is correct. The atomic commit requirement is satisfied by merging the two stories' work into a single commit at the end of STORY-018, which the STORY-018 acceptance criteria already mandate. Recommendation: DO NOT MERGE. The stories should stay separate; the commit should merge them.

**Effort estimate (5):** Slightly high but defensible. The rule file changes themselves are under 2 hours of actual editing. The effort=5 cost is driven by the C4 adversarial review (AE-002 auto-escalation), which involves 3+ iteration cycles. If the reviewer is efficient, this might complete at effort=3. Keeping it at 5 provides reasonable buffer.

**Ambiguity in scope: L2-REINJECT comment.** TASK-003 says "Update L2-REINJECT HTML comment for new tier ordering." The L2-REINJECT comment in agent-development-standards.md (line 7) currently reads "Tool tiers T1-T5: always select lowest tier satisfying requirements." This text does not enumerate the specific tier names, so it may not require a content change -- only verification that the tier summary remains accurate under the new model. The task should clarify: verify first, update only if the content changes meaning. Mark this as a SOFT observation.

**Standards mapping:**
- NIST SSDF PO.3.1: Implement supporting toolchains -- the L2-REINJECT mechanism is part of the enforcement toolchain for tier governance. Changes here affect runtime enforcement fidelity.
- OWASP SAMM Implementation (I-SB): Security standards are being explicitly updated with principle-of-least-privilege rationale per tier. This is a maturity improvement.

---

### STORY-018: Execute Governance YAML Migration (51 Files)

**Feasibility:** FEASIBLE WITH CORRECTIONS. The 3-step T3_HOLD pattern is sound. Two defects must be corrected before execution.

**DEF-001 (HIGH): sed script will silently skip one file.**

The migration script uses end-of-line anchors:
```bash
sed -i '' 's/tool_tier: T3$/tool_tier: T4/' "$file"
sed -i '' 's/tool_tier: "T3"$/tool_tier: "T4"/' "$file"
```

`diataxis-explanation.governance.yaml` has an inline comment on the `tool_tier` line:
```yaml
tool_tier: T3  # T3: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Context7. Upgraded from T2 ...
```

The `$` end-of-line anchor will not match this line. The file will silently pass through Step 2 with `tool_tier: T3` unchanged. The post-migration verification check (T3 count = 2) would then fail because the actual T3 count would be 3.

Correction: Add a third sed pattern that handles the inline comment case:
```bash
sed -i '' 's/tool_tier: T3 /tool_tier: T4 /' "$file"
```
Or preferably, use a regex pattern that handles both forms:
```bash
sed -i '' 's/tool_tier: T3\([[:space:]].*\)\{0,1\}$/tool_tier: T4\1/' "$file"
```
Simpler and more robust: strip any existing comment and set the new tier value, accepting that the inline comment describing the old tier meaning becomes stale anyway post-migration.

**DEF-002 (MEDIUM): T2 count stated as 28, actual count is 29.**

The STORY-018 summary table states:
```
| Unchanged | 38 | T1 (4), T2 (28), T4-with-web (5), T5 (1) |
```

Actual current T2 count: 29. Actual total: 4 + 29 + 49 + 7 + 1 = 90. But the governance YAML file count is 89.

Investigation: The grep count of T2=29 may include one file where `tool_tier: T2` appears in a comment or narrative rather than as the actual field value. This requires manual verification before migration. The post-migration verification table states:
```
| T2 count | ... | Expected: 28 |
```
This will produce a false failure if the actual count is 29. Correction: Verify the discrepancy by running `grep -rl 'tool_tier:.*T2' skills/*/agents/*.governance.yaml` and reconciling against the 89-file total before migration begins. Update the expected counts in the verification table to match reality.

**Dependency accuracy:** Correctly depends on STORY-017. The claim that STORY-019 and STORY-020 must wait for STORY-018 is correct: documentation should describe the final state, and security verification should review the implemented state.

**Question D-002 addressed (can STORY-019 start from ADR alone?):** Partially yes. STORY-019 has two components: (a) the reference sweep and SKILL.md updates, and (b) the new migration guide and tier selection reference. Component (b) -- the new documents -- can be drafted from the ADR alone because the tier definitions are stable once STORY-016 is complete. Component (a) -- the reference sweep -- should wait for STORY-018 completion so the before/after state is fully known. Recommendation: Split STORY-019 into two sub-tasks. TASK-004 (Write Tier Migration Guide) and TASK-005 (Write Tier Selection Reference) can begin as soon as STORY-017 completes. TASK-001 through TASK-003 (reference sweep and existing file updates) should wait for STORY-018.

**Rollback coverage:** TASK-005 (test rollback) correctly covers round-trip testing. The rollback script for the inline-comment case (DEF-001) must also handle restoring the comment, not just reverting the tier value. Mark as a follow-on acceptance criterion addition.

**Effort estimate (3):** Correctly estimated. The mechanical sed work is under 30 minutes. The effort is consumed by the pre/post verification steps and the schema validation (TASK-004).

**Standards mapping:**
- NIST SSDF PS.1: Protect all forms of code from unauthorized access and tampering. The 3-step T3_HOLD pattern prevents a partial migration from creating an inconsistent governance state that could be exploited.
- NIST SSDF PS.2: Provide a mechanism for verifying software release integrity. The pre/post verification checks and rollback testing directly satisfy this practice.

---

### STORY-019: Tier Model Documentation and Migration Guide

**Feasibility:** FEASIBLE. Documentation work is well-scoped.

**Dependency accuracy:** The dependency on STORY-018 is partially over-constrained per the analysis above (D-002). Two of the six tasks (TASK-004, TASK-005: new documents) can start after STORY-017 completes.

**Effort estimate (5):** Justified. The actual documentation writing (TASK-004: how-to guide, TASK-005: reference doc) is 2-3 hours. The UX review cycle (TASK-006) adds unpredictable iteration. The reference sweep across SKILL.md files is non-trivial: the user-experience/SKILL.md alone has 16 T3/T4 references, and the inline tier definitions embedded in UX sub-skill SKILL.md files (ux-ai-first-design, ux-atomic-design, ux-design-sprint, ux-jtbd, etc.) are particularly dense with descriptive text that must be rewritten, not just string-replaced. The effort=5 estimate is appropriate.

**Documentation scope completeness:**

The P1 sweep scope covers `skills/*/SKILL.md`, `AGENTS.md`, `docs/knowledge/*.md`, `prompt-quality.md`, and `prompt-templates.md`. Codebase analysis identified two categories of tier references:

1. **UX skill SKILL.md files** (high density): user-experience/SKILL.md (16 refs), ux-ai-first-design/SKILL.md (4 refs including narrative tier descriptions like "T3 (External) = Read, Write, Edit..."), ux-atomic-design/SKILL.md (3 refs), ux-design-sprint/SKILL.md (5 refs), ux-jtbd/SKILL.md (4 refs), ux-lean-ux/SKILL.md (3 refs), ux-inclusive-design/SKILL.md (3 refs), ux-heuristic-eval/SKILL.md (3 refs). These require rewriting tier descriptions, not just changing "T3" to "T4".

2. **ADR-PROJ007-001-agent-design.md** (11 refs): This is a design document in `docs/design/`, not `docs/knowledge/`. The scope in STORY-019 references `docs/knowledge/` but not `docs/design/`. The ADR-PROJ007-001 contains the original tier table definition that served as the foundation for agent-development-standards.md. It should be updated or archived with a deprecation notice. Add to TASK-003 scope.

3. **prompt-engineering/SKILL.md** (2 refs): References "T3 research agent" in examples. These are illustrative examples, not definitions. Simple string update: change to "T4 research agent". Low effort.

**Gap in acceptance criteria:** The prompt-templates.md tier reference check is listed but no actual tier references appear in that file. TASK-001 (grep audit) will surface this; no correction needed before work starts.

**Standards mapping:**
- NIST SSDF PO.1.3: Ensure personnel are trained and educated. The migration guide and tier selection reference are training artifacts that directly support this practice.
- OWASP SAMM Education & Guidance (EG): Security documentation for agent authors reduces misclassification risk (agents incorrectly elevated to T4 when T2 suffices).

---

### STORY-020: Security and Access Control Verification

**Feasibility:** FEASIBLE. The security assessment scope is comprehensive.

**DEF-003 (MEDIUM): H-35 reference is stale.**

STORY-020 Security Assessment Scope states:
```
| Only T5 agents have Agent tool | Cross-reference `tool_tier: T5` against `tools:.*Agent` in .md | Only ux-orchestrator |
```

The story body references "H-35 compliance" throughout, but H-35 was retired into H-34 sub-item b per the EN-002 consolidation recorded in quality-enforcement.md:
```
| H-35 | H-34 (sub-item b) | Constitutional compliance in agent definitions | 2026-02-21 |
```

The verification check is substantively correct (verifying Agent tool at T5 only is the right check), but the rule reference should be "H-34" not "H-35". Correction: Update all "H-35 compliance" references in STORY-020 to "H-34 (sub-item b)". This is a documentation accuracy issue, not a functional defect, but it matters because the security reviewers will look up H-35 and find it tombstoned, creating unnecessary confusion.

**Dependency accuracy:** The dependency on STORY-019 (documentation) is labeled "should be updated (for completeness review)" in the related items. This is a SHOULD dependency, correctly not listed as a hard dependency in the table. The dependency on STORY-017 and STORY-018 is hard and correct.

**Effort estimate (5):** Justified. The red-vuln permission model analysis (TASK-001) involves genuine security reasoning about whether the 49-agent MK ceiling expansion creates exploitable paths. This is not mechanical work. The deterministic validation (TASK-003) is straightforward. The C4 adversarial review (TASK-006) will require 3+ iterations per H-14.

**Coverage gap identified:** The security assessment scope checks that no `.md` frontmatter `tools` or `mcpServers` fields changed. However, there is no check verifying that `disallowedTools` fields were also unchanged. If a governance YAML migration introduced any systematic diff in `.md` files (e.g., if the migration script ran on wrong file patterns), a `disallowedTools` change could quietly remove a constraint. Add to TASK-002 acceptance criteria: `grep -r 'disallowedTools' skills/*/agents/*.md before/after comparison` as an explicit check.

**Permission creep risk (red-vuln scope):** The story correctly identifies the primary risk: 49 agents moving from T3 to T4 means 49 agents now have their governance *ceiling* set to permit Memory-Keeper. None of them have actual MK access today (their `.md` frontmatter is unchanged). The risk is that future agents created by copying these files as templates will see `tool_tier: T4` and conclude MK access is appropriate without understanding that eng-* and red-* agents are explicitly excluded. This is a documentation risk, not a migration risk. The STORY-019 migration guide directly mitigates this. Flag for red-vuln analysis: the template-copy pattern is the highest-probability exploit path for this change.

**Standards mapping:**
- NIST SSDF PO.1.2: Implement Roles and Responsibilities for Security. The access control integrity checks directly verify that tier reclassification does not change runtime roles.
- MS SDL Security Review: The red-vuln attack surface analysis and eng-security code review constitute the threat modeling verification step for the implemented tier model.

---

### EN-004: Memory-Keeper Collision Detection Enhancement

**Feasibility:** FEASIBLE but scope is under-specified.

**Non-blocking status:** Correctly non-blocking. The ADR FMEA correctly rates FM-5 (MK collision risk) at RPN=105, below the 120 threshold for mandatory mitigation.

**Effort estimate (5):** Likely underestimated. The acceptance criteria describe optimistic concurrency detection -- a well-understood pattern, but one whose implementation depends entirely on what the Memory-Keeper MCP server exposes. If the MCP server does not support ETags or last-modified timestamps on keys, implementing optimistic concurrency requires either (a) a wrapper layer that stores version metadata alongside the actual value, or (b) a naming convention that embeds version information in the key. Neither is trivial. TASK-001 (design) should explicitly include a feasibility spike against the MCP server's actual API before committing to the implementation approach.

**Task gap:** TASK-004 says "Update MCP-002 governance standard with collision handling guidance." MCP-002 is defined in `.context/rules/mcp-tool-standards.md`, which is a C3 auto-escalation target (AE-002). Modifying this file requires C3 quality gate review, which is not reflected in the EN-004 acceptance criteria. Add a task: "C3 adversarial review of MCP-002 standard update."

**Dependency accuracy:** "Informed By STORY-018" is correct. "Non-blocking STORY-018" is correct. No issues.

**Standards mapping:**
- NIST SSDF PO.3.2: Implement supporting toolchains -- collision detection is a toolchain safety mechanism for MK writes.

---

## Question Answers (Direct)

### Q1: Should STORY-017 and STORY-018 merge?

No. Keep them separate. The atomicity requirement is at the commit level, not the story level. The two stories have different acceptance criteria, different skills required (UX review and C4 adversarial for STORY-017; bash execution, schema validation, rollback testing for STORY-018), and different risk profiles. Merging them would create a 11-task story that is harder to review, harder to track, and harder to roll back independently. The atomic commit is enforced by making the STORY-018 implementation commit include the STORY-017 file changes -- this is a workflow note, not a scope merger.

### Q2: Is the dependency chain too strict?

Yes, in one place. STORY-019 TASK-004 (migration guide) and TASK-005 (tier selection reference) can begin as soon as STORY-017 completes. They do not need STORY-018 to be complete because they describe the tier model semantics, not the per-agent assignments. The reference sweep tasks (TASK-001 through TASK-003) correctly depend on STORY-018. Recommend adding an internal dependency annotation: "TASK-004 and TASK-005 may begin after STORY-017 completes; TASK-001 through TASK-003 require STORY-018 completion."

STORY-020 correctly depends on all three predecessors and cannot be parallelized further given its role as the final verification gate.

### Q3: Are effort estimates realistic?

| Story | Estimate | Assessment |
|-------|----------|------------|
| STORY-016 | 3 | Accurate |
| STORY-017 | 5 | Slightly conservative but defensible due to C4 review iteration uncertainty |
| STORY-018 | 3 | Accurate (mechanical work + verification) |
| STORY-019 | 5 | Accurate (UX review iteration + dense SKILL.md rewrites) |
| STORY-020 | 5 | Accurate (security reasoning + C4 review) |
| EN-004 | 5 | Underestimated -- recommend 8 pending TASK-001 feasibility spike result |

### Q4: Are any tasks missing or redundant?

**Missing tasks identified:**

| Location | Missing Task | Priority |
|----------|-------------|----------|
| STORY-016 | Update options-explainer cross-reference to ADR | SOFT |
| STORY-018 | Verify T2 count discrepancy (29 vs 28) before migration | HIGH (must be TASK-000 pre-condition) |
| STORY-018 | Fix sed script for inline-comment case (DEF-001) before TASK-002 | HIGH |
| STORY-019 | Add ADR-PROJ007-001-agent-design.md to documentation sweep scope | MEDIUM |
| STORY-020 | Add disallowedTools diff check to TASK-002 | MEDIUM |
| EN-004 | Add C3 adversarial review for MCP-002 standard update | MEDIUM |

**Redundant tasks identified:**

STORY-018 TASK-006 (independent agent-by-agent tier verification by /adversary) and STORY-020 TASK-003 (deterministic tier/tool consistency validation by ps-validator) overlap substantially. Both verify that every agent has the correct tier after migration. The distinction is skill-level: TASK-006 is an independent audit by /adversary, TASK-003 is deterministic schema validation by ps-validator. These are complementary, not redundant -- defense-in-depth is appropriate here. Keep both.

### Q5: Is task granularity appropriate?

Yes. The 30 tasks across 6 stories average 5 tasks per story, which is appropriate for the complexity level. The tasks are generally 1-skill, 1-deliverable in scope. No task is so large it should be split further, and no two tasks are so small they should merge. One exception: STORY-017 TASK-001 (rewrite agent-development-standards.md) and TASK-002 (update mcp-tool-standards.md) could merge since both are short documents, but keeping them separate enables independent review artifacts. The current granularity is correct.

---

## L2 Strategic Implications

### SAMM Maturity Assessment

This implementation is a maturity advancement in the OWASP SAMM Implementation stream:

| Practice | Current Maturity | Post-Implementation | Evidence |
|----------|-----------------|--------------------|---------|
| Security Requirements (SR) | L1 (ad hoc) | L2 (defined) | Tier model with explicit principle-of-least-privilege ordering and documented rationale per tier |
| Secure Build (SB) | L1 | L1 (no change) | CI schema validation already exists; EN-004 would advance this |
| Secure Deployment (SD) | L1 | L1 (no change) | Out of scope for this change |
| Defect Management (DM) | L2 | L2 (maintained) | ADR FMEA and post-migration verification maintain existing level |

**Trajectory:** The Option A implementation moves the tier model from an informal taxonomy to a governance-enforced classification with runtime implications (T3 = MK access ceiling, T4 = web access ceiling). This is a genuine maturity improvement, not cosmetic renaming.

### Technical Debt Created

**Short-term debt (acceptable):**

1. **49 governance YAMLs with stale inline comments.** Several `tool_tier: T3` lines have inline comments describing old tier semantics (e.g., diataxis-explanation has "T3: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Context7"). After migration, these files will have `tool_tier: T4` but the comment will say "T3: ...". The migration script does not update comments. STORY-019 does not include a comment sweep. This is an accepted inconsistency: YAML inline comments are not load-bearing for governance (the tier value is authoritative, not the comment). Add a SOFT recommendation to EN-004 or a future story: sweep inline `tool_tier` comments and update them.

2. **ADR-PROJ007-001 not updated.** This foundational ADR contains the original tier table with old semantics. It will remain as historical documentation with outdated tier definitions until STORY-019 addresses it (assuming it is added to scope per the recommendation above). Risk: agent authors consulting the ADR rather than agent-development-standards.md will get wrong tier guidance. Low probability given the ADR is not in the auto-loaded rules path.

**Long-term debt (monitor):**

The separation between `tool_tier` (governance ceiling, in .governance.yaml) and actual tool access (runtime enforcement, in .md frontmatter) creates a permanently two-file truth. As the agent count grows beyond 89, maintaining this consistency manually becomes increasingly error-prone. EN-004's MCP-002 collision detection work, when it matures, should be accompanied by a CI gate that cross-checks `tool_tier` against `.md` tool declarations. This would close the most significant long-term maintenance risk from this change.

### Dependency Strategy

The sequential chain (016 → 017 → 018 → 019+020 parallel) is the correct architecture. The only relaxation I recommend is the partial parallelization of STORY-019 TASK-004 and TASK-005 with STORY-018, which reduces the critical path by approximately one sprint cycle without introducing risk.

EN-004 is correctly non-blocking and should remain so. Scheduling it immediately after STORY-018 completes is the recommended timing: the team has context, the motivation (49 new T3 agents eligible for MK) is fresh, and the MCP server API investigation (TASK-001) can run in parallel with STORY-019 and STORY-020.

---

*Assessment produced by: eng-lead*
*Tool tier: T3 (Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, Context7)*
*Evidence basis: codebase analysis (Glob, Grep, Bash), all 6 entity files read in full*
*Confidence: 0.88 (HIGH -- codebase counts verified against story claims; T2 discrepancy requires manual reconciliation before confidence reaches 0.92)*
