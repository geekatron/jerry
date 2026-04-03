# STORY-020 Security Scope Assessment: Red-Vuln Analysis

> Agent: red-vuln (Vulnerability Analyst, /red-team skill)
> Scope: Governance-only review -- no exploitation, no active scanning
> Subject: STORY-020 security verification story for tier model renumbering
> Date: 2026-03-28

## Document Sections

| Section | Purpose |
|---------|---------|
| [Verdict](#verdict) | Is STORY-020 correctly scoped? |
| [Threat Model: What Actually Changes](#threat-model-what-actually-changes) | Ground-truth attack surface |
| [Actual Security Risks](#actual-security-risks) | Concrete risks with severity ratings |
| [Non-Risks (Over-Scope Candidates)](#non-risks-over-scope-candidates) | Theoretical risks that do not materialize |
| [Task-Level Recommendations](#task-level-recommendations) | Drop, keep, add, absorb |
| [Effort Estimate Assessment](#effort-estimate-assessment) | Is 5 points appropriate? |
| [STORY-018 Risk Absorption Question](#story-018-risk-absorption-question) | Should STORY-020 absorb migration script risks? |
| [Summary Table](#summary-table) | Disposition of all 6 STORY-020 tasks |

---

## Verdict

STORY-020 is **moderately over-scoped** and the effort estimate is **inflated by roughly a factor of 2**.

The core problem: TASK-001 ("Red team: permission model attack surface analysis") is framed as a full attack surface analysis for a change that has zero runtime effect. The governance-only nature of this migration eliminates the primary attack surface that red-team methodology is designed to evaluate. The real security work is a subset of what STORY-020 currently specifies, and most of it already overlaps with STORY-018's acceptance criteria.

The story is not meaningless -- there are genuine verification items. But they are verification and validation work (deterministic checks), not adversarial security analysis.

---

## Threat Model: What Actually Changes

To assess scope correctly, the attack surface must be grounded in what actually changes versus what merely changes on paper.

### Layer 1: Runtime Tool Access (the actual enforcement mechanism)

**What changes:** Nothing.

The `.md` frontmatter `tools` and `mcpServers` fields are the runtime enforcement boundary. Claude Code reads these fields to determine what tools an agent may invoke. STORY-018 explicitly specifies zero `.md` frontmatter changes. Pre/post-migration, every agent has identical runtime tool access.

**Security consequence:** No agent gains any new capability at runtime. There is no path from "governance YAML `tool_tier` field changed" to "agent can now call a tool it could not call before." The two layers are structurally decoupled.

### Layer 2: Governance Classification (what changes)

**What changes:** The `tool_tier` string in 51 `.governance.yaml` files.

This field is:
- Read by CI schema validation (L5 enforcement layer)
- Read by agent authors as guidance when designing new agents
- Read by reviewers to assess whether an agent's tool requests are tier-appropriate

It is NOT:
- Read by Claude Code at agent invocation time
- Used to grant or revoke tools dynamically
- Connected to any authentication or authorization mechanism

**Security consequence:** The governance YAML is a policy document, not an enforcement mechanism. Changes to it create policy drift risk (documented below) but not direct permission escalation.

### Layer 3: Documentation and Rule Files (indirect)

STORY-017 updates `agent-development-standards.md` to redefine tier meanings. This is the layer where a mistake has lasting downstream effects: future agents will be designed to the new tier definitions, and if the definitions are wrong, new agents will be systematically miscategorized.

This is the one layer where a genuine long-term security posture risk exists.

---

## Actual Security Risks

The following are concrete, non-theoretical risks ordered by severity.

### RISK-001: Policy Drift -- T4 Ceiling Grants MK Without Review
**Severity:** Medium
**Category:** Governance posture degradation (not immediate access escalation)

The 49 agents reclassified T3->T4 gain Memory-Keeper as a tier-level CEILING. Under the new model, an agent author can add `mcpServers: memory-keeper: true` to a T4 agent's `.md` frontmatter without triggering a tier-change review (because the agent is already T4, which permits MK). Under the old model, adding MK to a T3 agent would require a tier bump to T4, which creates a natural review checkpoint.

**Why this is Medium, not High:** The `.md` frontmatter change itself is still a PR-reviewable change. The governance checkpoint shifts from "tier change review" to "PR review of mcpServers addition." Whether this is a meaningful degradation depends on PR review quality. The ADR explicitly acknowledges this trade-off (Criterion 5, Least Privilege: scored 7/10 for Option A).

**What to verify:** The ADR's least-privilege justification is sound. STORY-020 should verify that the ADR's risk acknowledgment is documented and accepted, not attempt to re-litigate it as a blocking finding.

**Verification action:** Confirm that `agent-development-standards.md` MCP-M-002 language is updated to state T3+ (not T4+) for MK eligibility, and that the STORY-017 rule file changes include this update.

### RISK-002: eng-*/red-* MK Exclusion Becomes Implicit Rather Than Structural
**Severity:** Medium
**Category:** Documentation-dependent exclusion

Currently, eng-* and red-* agents are excluded from Memory-Keeper on the grounds that "file-based persistence per P-002 (engagement-scoped output)" is the right pattern for these skills. The ADR (mcp-tool-standards.md integration matrix note) documents this exclusion.

After migration, these agents are T4 -- a tier that PERMITS MK. The exclusion is now maintained only by the explicit "not included by design" note in `mcp-tool-standards.md`, not by their tier number. If that documentation is lost or misread, a future maintainer may reasonably add MK to an eng-* or red-* agent as a "normal T4 agent behavior" without realizing there is a design intent to the contrary.

**Why this is Medium, not High:** The exclusion is still documented. The risk is documentation rot over a multi-year horizon, not an immediate access change.

**Verification action:** STORY-017 should add an explicit exclusion note to the T4 tier definition in `agent-development-standards.md` that calls out eng-*/red-* as excluded by design. STORY-020 should verify this note is present.

### RISK-003: sed Corruption of YAML Structure
**Severity:** Low-to-Medium
**Category:** Migration execution integrity

The STORY-018 migration script uses `sed -i ''` with line-terminator-anchored patterns (`T3$` and `"T3"$`). The risks are:

1. **Partial-match corruption:** If any YAML comment or value contains the literal string `T3` followed by end-of-line, it will be incorrectly mutated. Example: a `description: "T3 is the external tier"` line ending in `T3` would not be caught by `T3$` but `T3 is the external tier` would also not match -- the `$` anchor protects this. The specific sed patterns appear safe for the described file structure.

2. **Quoted form missed:** The script handles both `tool_tier: T3` and `tool_tier: "T3"`. This coverage appears complete for standard YAML serialization.

3. **T3_HOLD cleanup failure:** If Step 3 fails midway, agents ts-parser and ts-extractor would have `tool_tier: T3_HOLD` -- an invalid enum value that schema validation would catch.

**Why this is Low-to-Medium:** The sed patterns are well-designed with anchors and intermediate values. The primary residual risk is an incomplete Step 3 execution, which is immediately detectable by schema validation (post-migration Step 4 verification).

**Verification action:** This is already covered by STORY-018 TASK-003 (post-migration verification) and TASK-005 (rollback test). STORY-020 need not duplicate this -- the finding is that STORY-018 already owns this risk.

### RISK-004: Schema Enum Mismatch if Rule Files and YAMLs Are Committed Non-Atomically
**Severity:** Low
**Category:** Transient inconsistency

If STORY-017 (rule files) and STORY-018 (YAML migration) land in separate commits, there is a window where YAML files reference a `tool_tier` enum value (`T3` as Persistent, `T4` as External) that does not yet match the enum definition in `agent-governance-v1.schema.json`. This would cause CI schema validation failures during that window.

**Why this is Low:** The STORY-018 acceptance criteria already require atomic commits: "Migration and rule file changes are in the same commit (atomic)." This risk is documented and mitigated by existing AC.

**Verification action:** STORY-020 TASK-002 (migration PR diff audit) should confirm the commit is atomic. This is already present in the story; no addition needed.

### RISK-005: H-35 Invariant -- Agent Tool Remains T5-Only
**Severity:** Low (verification item, not a real risk)
**Category:** Constitutional compliance

H-35 requires that only T5 agents may use the Agent tool. The migration does not add or remove any T5 agents and does not change any `.md` frontmatter. This invariant is maintained trivially.

**Verification action:** A single grep cross-reference (T5 agents vs Agent tool in .md files) is appropriate. This is already in STORY-020 AC. It is a 5-minute check, not a full security analysis.

---

## Non-Risks (Over-Scope Candidates)

The following items in STORY-020 address risks that do not materialize given the governance-only nature of the migration.

### NON-RISK-A: "Permission Escalation Paths" (TASK-001 framing)

The story asks red-vuln to "identify whether any tier ceiling expansion creates exploitable permission paths." This framing applies to systems where a classification change causes a runtime enforcement system to grant additional permissions. In this architecture, the `.md` frontmatter is the enforcement boundary and it does not change. There are no exploitable permission paths from a governance YAML change alone.

The appropriate framing is RISK-001 (policy drift): future agent authors have a broader ceiling to work with. This is a governance posture concern, not an exploitable attack path.

**Disposition:** Reframe TASK-001 from "attack surface analysis" to "permission ceiling verification" -- confirm that no agent's `.md` frontmatter changed and document the policy drift risk with accepted severity.

### NON-RISK-B: "Secrets or Sensitive Data Exposed in Migration"

STORY-020 TASK-002 includes "Verify no secrets or sensitive data exposed in migration." Governance YAML files containing `tool_tier` strings cannot expose secrets. The sed operation mutates a tier label. This check has zero probability of finding a real issue and should be removed as ceremony.

**Disposition:** Drop this check from TASK-002.

### NON-RISK-C: "Agents Can Gain Memory-Keeper Without Explicit .md Frontmatter Addition"

STORY-020 AC includes "Verify no agent can gain Memory-Keeper access without explicit .md frontmatter addition." This is definitionally true by the architecture -- Memory-Keeper requires explicit `mcpServers: memory-keeper: true` in `.md` frontmatter, which Claude Code enforces. No governance YAML change can bypass this. The AC is verifying an architectural invariant that cannot be violated by this migration.

**Disposition:** This check is redundant with the architectural guarantee and adds no verification value. Drop from AC, or replace with: "Confirm zero `.md` mcpServers fields changed in migration PR" (which is already in the Access Control Integrity table).

---

## Task-Level Recommendations

### TASK-001: Red team: permission model attack surface analysis
**Recommendation: RESCOPE (do not drop, but reduce significantly)**

Current scope is too broad. Replace "attack surface analysis" with a focused permission ceiling verification:
- Confirm zero `.md` frontmatter changes in migration PR (15 min)
- Document RISK-001 (policy drift) as an accepted governance trade-off (30 min)
- Confirm RISK-002 (eng-*/red-* exclusion) is explicitly documented in updated rule files (15 min)
- Document residual risk register with severity ratings (already done in this assessment -- reference it)

**Revised effort:** 1 hour, not a multi-hour attack surface analysis engagement.

### TASK-002: Security review: migration PR diff audit
**Recommendation: KEEP but narrow scope**

Remove the "secrets" check (NON-RISK-B). Focus on:
- Confirm only `.governance.yaml` files changed (no `.md` files)
- Confirm sed operations produced syntactically valid YAML
- Confirm atomic commit (rule files + YAML migration together)

This is already largely covered by STORY-018 acceptance criteria. STORY-020 TASK-002 provides independent verification -- which is valuable -- but should not duplicate STORY-018's own verification steps. Scope to: "independent confirmation that STORY-018's access control integrity ACs were met."

### TASK-003: Deterministic tier/tool consistency validation
**Recommendation: KEEP as-is**

This is the highest-value task in STORY-020. Verifying that every agent's governance YAML tier matches the ADR migration table and that every `.md` tools/mcpServers field is unchanged is concrete, deterministic work. The expected distribution (T1=4, T2=28, T3=2, T4=54, T5=1) provides a clear pass/fail criterion.

### TASK-004: Verify H-35 compliance (Agent tool at T5 only)
**Recommendation: KEEP but acknowledge it is a 5-minute grep**

H-35 verification is appropriate given the C4 criticality of the governance change. However, it should be scoped correctly: a grep cross-reference, not a full compliance analysis. The migration does not touch T5 at all, so this is expected to be a trivial pass. Document it as a confirmation check, not a discovery exercise.

### TASK-005: Verify eng-*/red-* MK exclusion maintained
**Recommendation: KEEP and STRENGTHEN**

This is a genuine residual risk (RISK-002). The verification should check:
1. Zero MK entries in eng-*/red-* `.md` frontmatter (unchanged from pre-migration)
2. `mcp-tool-standards.md` integration matrix "not included by design" note is still present AND the STORY-017 T4 tier definition in `agent-development-standards.md` contains an explicit eng-*/red-* exclusion note

The second check is new and addresses the documentation rot risk. Add this to the TASK-005 acceptance criteria.

### TASK-006: C4 adversarial review of complete implementation
**Recommendation: KEEP as-is**

The C4 quality gate (scoring >= 0.95 on S-014 rubric) is appropriate for a governance infrastructure change affecting 89 agents. This is the ADR-mandated review and should not be removed. However, note that the adversarial review assesses IMPLEMENTATION QUALITY and GOVERNANCE COMPLETENESS, not security vulnerability discovery. It is a quality gate, not a red-team exercise.

---

## Effort Estimate Assessment

**Current estimate:** 5 story points
**Recommended estimate:** 2-3 story points

Breakdown of actual work after rescoping:

| Task | Revised Effort |
|------|---------------|
| TASK-001 (rescoped permission ceiling verification) | 1 hour |
| TASK-002 (independent PR diff audit) | 30 minutes |
| TASK-003 (deterministic tier/tool consistency validation) | 1-2 hours (grep scripting + review) |
| TASK-004 (H-35 grep check) | 15 minutes |
| TASK-005 (MK exclusion + documentation verification) | 30 minutes |
| TASK-006 (C4 adversarial review) | 2-3 hours (this drives the effort) |

The 5-point estimate implies this is a significant security analysis engagement. It is not. The genuinely complex work is TASK-006 (the /adversary quality gate), which is a quality verification task, not a security analysis task. If TASK-006 is excluded from STORY-020's effort (it could arguably be its own story at 3 points), the remaining security verification work is 1-2 points.

**Recommendation:** If TASK-006 remains in STORY-020, a 3-point estimate is appropriate. If TASK-006 is split to a separate quality gate story, STORY-020 is a 2-point story.

---

## STORY-018 Risk Absorption Question

**Question:** Should STORY-020 absorb security concerns from STORY-018's migration script?

**Answer:** No. STORY-018 already owns the migration script security concerns with adequate specificity.

STORY-018 acceptance criteria include:
- eng-security AC: "No agent's `.md` frontmatter `tools` or `mcpServers` fields changed"
- eng-security AC: "No agent gains actual tool access it didn't have before"
- eng-lead AC: "Migration script handles both quoted and unquoted YAML forms"
- eng-lead AC: "T3_HOLD intermediate value fully resolved"
- ps-validator AC: "No YAML formatting corruption from sed operations"
- Rollback testing AC (3 checks)

STORY-020 should reference STORY-018's completion as a prerequisite (it already does, via Dependencies) and provide independent confirmation that those ACs were met. STORY-020 should NOT duplicate STORY-018's internal verification steps -- that creates double-accounting of effort and blurs ownership.

**The one exception:** STORY-020 TASK-002 (independent PR diff audit) is valuable precisely because it is independent of STORY-018's own author. Keep it as an independent verification layer, but scope it narrowly to: "confirm the STORY-018 ACs that have external-verifiability were met."

---

## Summary Table

| Task | Current Scope | Recommendation | Rationale |
|------|--------------|----------------|-----------|
| TASK-001 | Full attack surface analysis | RESCOPE to permission ceiling verification | No runtime change = no exploitable attack paths; real risk is policy drift (RISK-001) |
| TASK-002 | Security review + secrets check | KEEP, drop secrets sub-check | Secrets check is category error; independent PR audit has genuine value |
| TASK-003 | Deterministic tier/tool consistency | KEEP as-is | Highest-value concrete verification task |
| TASK-004 | H-35 compliance | KEEP, acknowledge it is a grep | Constitutional invariant confirmation appropriate for C4; trivial to execute |
| TASK-005 | MK exclusion check | KEEP and STRENGTHEN | RISK-002 is real; add documentation note verification |
| TASK-006 | C4 adversarial review | KEEP as-is | Quality gate, not security analysis; appropriate for C4 governance change |

**Not in STORY-020 but should be added:** A verification step that STORY-017's `agent-development-standards.md` T4 tier definition contains an explicit eng-*/red-* MK exclusion note. This addresses RISK-002's documentation rot vector and is currently unverified by any story.

---

## Final Scope Assessment

| Dimension | Assessment |
|-----------|-----------|
| Missing real risks? | One: documentation of eng-*/red-* exclusion in T4 tier definition (add to TASK-005) |
| Ceremony for non-risks? | Yes: "secrets" check in TASK-002; "exploitable permission paths" framing in TASK-001 |
| Correct effort estimate? | No: 5 points is inflated; 2-3 points after rescoping |
| STORY-018 risk overlap? | STORY-020 TASK-002 provides appropriate independent confirmation layer; no absorption needed |
| Red-team methodology appropriate? | Partially: TASK-001 does not warrant adversarial attack path analysis; the rest is V&V work |

The change being verified is a governance reclassification, not a permission grant. Security verification of governance reclassifications is primarily V&V work (did the reclassification happen correctly, did documentation stay consistent, are invariants maintained) rather than adversarial security analysis. STORY-020 should be scoped accordingly.
