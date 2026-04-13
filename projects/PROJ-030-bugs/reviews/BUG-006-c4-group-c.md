# Strategy Execution Report: Group C (S-002, S-004, S-001) — BUG-006 C4 Migration

## Execution Context

- **Strategies Executed:** S-002 (Devil's Advocate), S-004 (Pre-Mortem Analysis), S-001 (Red Team Analysis)
- **Deliverable:** ADR-EPIC002-001 Unified Output Path Resolution Protocol + migration implementation
- **Deliverable Path:** `docs/design/ADR-output-path-resolution-001.md`
- **Supporting Artifacts:** `projects/PROJ-030-bugs/work/BUG-006-skill-output-path-hardcoded.md`, `projects/PROJ-030-bugs/research/BUG-006-eng-audit-detail.md`, `projects/PROJ-030-bugs/research/BUG-006-red-audit-detail.md`, `projects/PROJ-030-bugs/research/BUG-006-ux-audit-detail.md`
- **Criticality:** C4 (Critical)
- **Executed:** 2026-04-01
- **Agent:** adv-executor (claude-sonnet-4-6)
- **H-16 Compliance:** S-003 (Steelman Technique) ran in Group B per strategy plan `projects/PROJ-030-bugs/work/BUG-006-c4-strategy-plan.md`

---

## Pre-Execution Evidence Base

Empirical grep verification performed prior to strategy execution:

| Check | Result |
|-------|--------|
| `skills/*/output/` pattern in skills/ | **0 matches** (AC-1 satisfied) |
| `filename_pattern` in governance YAML | **32 files** (10 eng + 11 red + 11 UX) |
| `Output Path Resolution` in agent .md | **32 files** (10 eng + 11 red + 11 UX) |
| `projects/${JERRY_PROJECT}/engagements` in eng composition YAML | **10 files** |
| `projects/${JERRY_PROJECT}/engagements` in red composition YAML | **11 files** |
| UX rules files (ci-checks, wave-progression, routing-rules) | Updated to new paths |
| `skills/*/output/` in .gitignore | Present |
| `filename_pattern` in schema JSON | Present |
| AD-M-011 in agent-development-standards.md | Present |

---

## S-002: Devil's Advocate

### Role Assumption

**Deliverable:** ADR-EPIC002-001 migration implementation (107 files, 32 agents, 13 skills)
**Criticality:** C4
**H-16 Compliance:** S-003 Steelman applied in Group B (confirmed per strategy plan)
**Role:** Argue against the migration's approach, sufficiency, and correctness.

### Findings Summary

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-20260401 | Composition YAML not included in the ADR's own verification specification | Major | ADR Verification table omits composition YAML coverage despite migration updating all 21 composition files | Completeness |
| DA-002-20260401 | P4 fallback described as "should never happen" yet no H-04 gate prevents it at runtime | Major | ADR Section "Priority 4: Work Directory Fallback" states "Should never happen in normal operation. Safety net only" but the SessionStart hook reference is passive | Methodological Rigor |
| DA-003-20260401 | The `{agent}` variable documentation contradicts standard variable syntax | Minor | ADR Agent Integration Specification states `{agent}` is "NOT a runtime variable — resolved when the agent definition is authored" but still uses brace-variable notation inconsistently with the other variables | Internal Consistency |
| DA-004-20260401 | Migration Guide omits Step 6 execution from recommended skill sequence | Major | ADR "Migration Order and Rollback" lists schema update as Step 0 but the recommended skill sequence (Step 0 then 1-4-5) skips renaming Step 6 to Step 0, creating ambiguous labeling | Actionability |
| DA-005-20260401 | Backward compatibility claim for /nasa-se is asserted without evidence | Minor | ADR Backward Compatibility states "/nasa-se agents already use `projects/${JERRY_PROJECT}/` prefix" with citation to a specific YAML line, but does not note that /nasa-se composition YAML was not audited in the same grep-verified manner as the three affected skill families | Evidence Quality |

### Detailed Findings

#### DA-001: Composition YAML Absent from Verification Table [MAJOR]

**Claim Challenged:** ADR Verification section lists 8 checks covering governance YAML, P1/P2/P3/P4 manual tests, ps-researcher unchanged, and AD-M-011 codification.

**Counter-Argument:** The verification table omits composition YAML (`skills/*/composition/*.agent.yaml`) entirely. The migration updated 21 composition YAML files (10 eng + 11 red — confirmed by grep: 10+11 matches for `projects/${JERRY_PROJECT}/engagements` in composition directories). This is a distinct file class from governance YAML. The ADR's own verification logic is incomplete because an implementer following the verification table would not check composition YAML files.

**Evidence:** ADR Verification section (lines 611-619): checks listed are `grep -r 'skills/.*/output/' skills/` (zero match), schema validation (32 agents), P1/P2/P3/P4 manual tests, ps-researcher unchanged, AD-M-011. No mention of composition YAML coverage.

**Impact:** Future migrations or rollbacks that reference the verification table as authoritative would miss confirming composition YAML updates, leaving 21 files potentially out-of-date.

**Dimension:** Completeness

**Response Required:** Add verification check: "All composition YAML files for eng-team (10) and red-team (11) have `output.location` updated to `projects/${JERRY_PROJECT}/engagements/` pattern — verify with `grep -r 'skills/.*/output' skills/*/composition/` returning zero matches."

**Acceptance Criteria:** Verification table extended to include composition YAML coverage check with specific grep command and expected result.

---

#### DA-002: P4 Fallback Has No Deterministic Gate [MAJOR]

**Claim Challenged:** ADR Priority 4 fallback states "Should never happen in normal operation" and references the SessionStart hook as prevention mechanism.

**Counter-Argument:** The SessionStart hook reference is entirely passive: "SessionStart hook should prevent this." The hook's prevention mechanism is not specified in the ADR, not referenced in the ADR's verification checks, and not enforced in any deterministic (L3/L5) layer described in the protocol. An agent operating in a context where `JERRY_PROJECT` is unset (e.g., a fresh terminal without project initialization) would silently fall back to `work/` without the user knowing the output was misrouted — the warning is in the agent's natural language output, not a deterministic gate.

**Evidence:** ADR Section "Priority 4: Work Directory Fallback" (line 234): "Agent MUST log a warning" — the enforcement mechanism is a text warning, not a tool-call failure or filesystem guard. ADR Failure Mode Analysis (line 363) confirms: P4 condition is detected only by "H-04 violation detected at session start."

**Impact:** In an H-04 violation scenario, agents may write outputs to `work/` silently. The ADR acknowledges this but doesn't specify a deterministic detection mechanism in the verification suite or L5 CI gate.

**Dimension:** Methodological Rigor

**Response Required:** Either (a) document the specific SessionStart hook logic that prevents P4 activation and add it as a verifiable check in the Verification table, or (b) acknowledge that P4 is an intentional graceful degradation with logged warning, and add "P4 fallback behavior tested" as a Verification check.

**Acceptance Criteria:** Verification table includes a P4 fallback test with specific test conditions (unset JERRY_PROJECT) and expected behaviors (output in work/ AND warning message logged).

---

#### DA-004: Migration Guide Step Numbering Creates Ambiguity [MAJOR]

**Claim Challenged:** ADR Migration Guide section "EXECUTE FIRST — Step 0" and the numbered steps 1-5 plus "Step 6."

**Counter-Argument:** The ADR labels the schema update as "Step 6" in the heading `### Step 6: Update Governance Schema` but simultaneously instructs it to execute first via `### EXECUTE FIRST — Step 0`. The "Migration Order and Rollback" subsection then says "Execution order (per skill, not cross-skill): 0. Update governance schema FIRST (Step 6)..." This creates a confusing reference where Step 0 = Step 6. An implementer following the ADR sequentially would first encounter "Step 1: Update Governance YAML" without seeing Step 6's content, since Step 6 appears later in the document.

**Evidence:** ADR Migration Guide (lines 375-543): "EXECUTE FIRST — Step 0: Update Governance Schema" appears before Step 1 in the Execution Order section, but the actual schema diff is in "Step 6: Update Governance Schema" (line 514). The ADR's own execution order clarification at line 537 says "0. Update governance schema FIRST (Step 6)."

**Impact:** Implementers reading the migration guide sequentially would encounter Step 1 instructions before Step 6 content, potentially executing YAML updates before the schema accepts the new `filename_pattern` field.

**Dimension:** Actionability

**Response Required:** Consolidate the step numbering: either renumber "Step 6" as "Step 0" throughout the document, or move the Step 6 content immediately after the "EXECUTE FIRST" directive so it appears before Step 1.

**Acceptance Criteria:** Migration guide uses unambiguous step ordering. The schema update step appears in document order before the YAML update step.

---

### S-002 Recommendations

**P1 (Major — SHOULD resolve):**

- **DA-001:** Add composition YAML verification check to ADR Verification table. Specific grep: `grep -r 'skills/.*/output' skills/*/composition/` must return zero matches.
- **DA-002:** Clarify P4 fallback enforcement by either documenting the SessionStart hook's H-04 detection logic or adding explicit P4 verification test to the Verification table.
- **DA-004:** Consolidate step numbering in Migration Guide — renumber Step 6 as Step 0 or relocate its content before Step 1.

**P2 (Minor — MAY resolve):**

- **DA-003:** Clarify `{agent}` variable documentation to distinguish "definition-time constant" from "runtime-interpolated variable" using different notation (e.g., `agent-architect` hardcoded vs. `{topic-slug}` runtime).
- **DA-005:** Add a note that /nasa-se was not subjected to the same `grep -rl` audit verification as the three affected skill families, but visual inspection confirms the correct pattern.

### S-002 Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Completeness | Negative | DA-001: Verification table incomplete — composition YAML coverage missing |
| Internal Consistency | Neutral | No contradictions in the migration logic itself |
| Methodological Rigor | Negative | DA-002: P4 fallback prevention mechanism unspecified; DA-004: step numbering confuses execution order |
| Evidence Quality | Neutral | Migration is grep-verified; the issues are documentation gaps, not factual errors |
| Actionability | Negative | DA-004: ambiguous step numbering reduces actionability of migration guide |
| Traceability | Neutral | ADR traces correctly to bug entity, audit details, and prior art |

**Overall S-002 Assessment:** REVISE — 3 Major findings identified. The migration implementation itself is correct (grep confirms zero old-pattern matches, 32 files verified with both `filename_pattern` and `Output Path Resolution` sections). The findings are documentation and verification gaps in the ADR itself, not implementation errors. The migration is functionally sound but the ADR's verification specification and migration guide need targeted revision.

---

## S-004: Pre-Mortem Analysis

### Header

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** ADR-EPIC002-001 migration implementation
**Criticality:** C4
**Date:** 2026-04-01
**H-16 Compliance:** S-003 Steelman applied in Group B (confirmed)
**Failure Scenario:** It is October 2026. The ADR-EPIC002-001 migration has failed. Six months after implementation, three newly-created agent definitions still use `skills/*/output/` paths, two engagements have outputs scattered across both old and new locations, and a pull request introduced a new UX sub-skill using the old anti-pattern — undoing part of the migration. The framework now has mixed output path conventions and BUG-006 is partially reopened.

### Perspective Shift

It is October 2026, six months after this migration was committed. We are now investigating why the migration's benefits have eroded, why the old anti-pattern reappeared, and why three new agents are non-compliant.

### Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-20260401 | No CI gate enforcing the new `projects/${JERRY_PROJECT}/engagements/` requirement — new agent definitions can introduce `skills/*/output/` without automated detection | Process | High | Critical | P0 | Methodological Rigor |
| PM-002-20260401 | AD-M-011 is MEDIUM priority (SHOULD) — a MEDIUM rule can be overridden "with documented justification," meaning a developer building a new skill can deviate from the output path standard without a formal governance violation | Process | High | Major | P1 | Internal Consistency |
| PM-003-20260401 | UX orchestrator now has hardcoded references to sub-skill output paths in wave-progression logic — if a new sub-skill is added without updating wave-progression.md, the signoff path tables become stale | Assumption | Medium | Major | P1 | Completeness |
| PM-004-20260401 | The migration removed committed output files from `skills/eng-team/output/` but the stale content may be referenced by external tools or documentation (e.g., the GH issue body #192 mentioned configurable output paths) — historical references to old paths persist in commit history and issues | External | Low | Minor | P2 | Traceability |
| PM-005-20260401 | The P3 default path `projects/${JERRY_PROJECT}/engagements/{engagement-id}/` relies on `{engagement-id}` being caller-provided — there is no default engagement-id generation specified in the ADR; standalone callers who omit engagement-id get a literal `{engagement-id}` in the path | Technical | Medium | Major | P1 | Actionability |
| PM-006-20260401 | Agent template caching: if an LLM agent's context was populated with the old governance YAML before the migration, cached instructions in long-running sessions could direct output to old paths until the session ends | Technical | Low | Minor | P2 | Evidence Quality |

### Detailed Findings

#### PM-001: No CI Gate for Output Path Pattern Enforcement [CRITICAL]

**Failure Cause:** The .gitignore blocks `skills/*/output/` from being committed, but no CI gate checks that NEW agent definition files comply with the output path convention. A developer creating `skills/new-skill/agents/new-agent.governance.yaml` with `output.location: "skills/new-skill/output/{engagement-id}/new-agent-{topic-slug}.md"` would receive no automated warning. The migration would be partially undone with each new non-compliant agent.

**Category:** Process

**Likelihood:** High — The root cause analysis in BUG-006 explicitly documents that the anti-pattern spread because "no MEDIUM standard in agent-development-standards.md requiring project-relative output paths" existed. Now that AD-M-011 exists but has no CI enforcement, the condition for propagation is only partially removed.

**Severity:** Critical — Over time, new non-compliant agents would require a BUG-006 re-investigation.

**Evidence:** ADR Verification table (lines 611-619) specifies a one-time `grep -r 'skills/.*/output/' skills/` check but does not mention a recurring CI gate. BUG-006 root cause analysis (line 77): "No CI gate checking for hardcoded skill-internal output paths" — this root cause is not addressed by any TASK in the implementation plan.

**Dimension:** Methodological Rigor

**Mitigation:** Add an L5 CI gate that runs on every PR: `grep -r 'skills/.*/output/' skills/` must return zero matches. This converts the one-time verification check into a recurring gate. The gate should fail the CI build if any new or modified agent file introduces the old pattern.

**Acceptance Criteria:** A CI check file (`.github/workflows/` or equivalent) contains a step that runs `grep -r 'skills/.*/output/' skills/` and fails if any match is found. The check is documented in the ADR Verification table.

---

#### PM-002: AD-M-011 MEDIUM Tier Permits Silent Deviation [MAJOR]

**Failure Cause:** AD-M-011 is classified as a MEDIUM standard (SHOULD, overridable with documented justification). This is lower enforcement than the bug's severity warrants. A developer building a new skill could write "Output location deviates from AD-M-011 for engagement isolation reasons" in the governance YAML or a PR description and bypass the standard without a HARD rule violation.

**Category:** Process

**Likelihood:** High — MEDIUM-tier standards are overridden frequently in the codebase (e.g., agent-development-standards.md AD-M-001 through AD-M-010 all use SHOULD). The override mechanism is legitimate but creates a gap.

**Severity:** Major — Not every new non-compliant agent would be caught; governance review would be the only detection mechanism.

**Evidence:** ADR Migration Guide Step 5 (line 509): "Agent output paths SHOULD follow the Unified Output Path Resolution Protocol... Override requires documented justification per MEDIUM tier vocabulary." The word SHOULD + override mechanism means the standard can be bypassed.

**Dimension:** Internal Consistency

**Mitigation:** Either (a) elevate AD-M-011 to HARD tier if the framework considers this invariant, or (b) add the CI gate from PM-001 as the compensating control for the MEDIUM classification — L5 gate replaces H-tier enforcement for the subset of the rule that is mechanically checkable (zero `skills/*/output/` references).

**Acceptance Criteria:** Either AD-M-011 is elevated to HARD tier with documented justification, OR a CI gate is confirmed as the compensating enforcement mechanism documented in the ADR.

---

#### PM-005: Engagement-ID Omission Produces Literal `{engagement-id}` in Path [MAJOR]

**Failure Cause:** The Priority 3 default template `projects/${JERRY_PROJECT}/engagements/{engagement-id}/{agent}-{topic-slug}.md` requires `{engagement-id}` to be provided by the caller. The ADR Failure Mode Analysis explicitly calls this out: "Agent MUST request engagement-id via H-31 clarification before writing." However, the ADR does not specify a default engagement-id generation scheme, leaving a gap between calling convention and agent behavior.

**Category:** Technical

**Likelihood:** Medium — Callers who use Pattern C ("no override, standalone") often omit engagement-id because they don't know they need one. The compatibility matrix shows "Engagement-id only" as caller input for the ad-hoc context, implying the user must know to provide this.

**Severity:** Major — An agent that writes to `projects/PROJ-024/engagements/{engagement-id}/eng-architect-auth-review.md` (literal brace text) creates an invalid path that subsequent agents cannot find.

**Evidence:** ADR Priority 3 section (line 215): "Agent resolves `${JERRY_PROJECT}` from environment and computes the full path." The Failure Mode Analysis (line 362): "`{engagement-id}` not provided and no default exists — Agent MUST request engagement-id via H-31 clarification before writing." The ADR requires H-31 clarification but does not specify a default engagement-id format agents can generate autonomously.

**Dimension:** Actionability

**Mitigation:** Specify a default engagement-id generation rule in the ADR: "If no engagement-id is provided and no H-31 response is received within one turn, agents SHOULD generate an engagement-id using the format `{YYYYMMDD}-{agent-name-prefix}` (e.g., `20260401-eng`), log the generated ID, and proceed." This allows standalone ad-hoc invocations to produce valid paths without user intervention.

**Acceptance Criteria:** ADR Priority 3 section or Failure Mode Analysis includes a fallback engagement-id generation rule that produces a deterministic, collision-resistant ID without user input.

---

### S-004 Recommendations

**P0 (Critical — MUST mitigate):**

- **PM-001:** Add L5 CI gate: `grep -r 'skills/.*/output/' skills/` on every PR, fail on any match. Document in ADR Verification table.

**P1 (Important — SHOULD mitigate):**

- **PM-002:** Clarify enforcement mechanism for AD-M-011. If MEDIUM tier remains, document the CI gate as the compensating HARD control. If the framework treats output path convention as invariant, consider HARD tier.
- **PM-003:** Document that wave-progression.md signoff file table must be updated whenever a new UX sub-skill is added. Add to UX skill development checklist.
- **PM-005:** Add default engagement-id generation rule to ADR Priority 3 fallback specification.

**P2 (Monitor):**

- **PM-004:** Historical references to old paths in GH issues and commit messages are cosmetic. No action required.
- **PM-006:** Agent session caching of old instructions is a transient issue. No action required.

### S-004 Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Completeness | Negative | PM-003: UX wave-progression sub-skill addition not covered; PM-001: CI gate absent |
| Internal Consistency | Negative | PM-002: MEDIUM tier + no CI gate leaves enforcement gap inconsistent with HARD bug severity |
| Methodological Rigor | Negative | PM-001: No recurring CI gate to enforce the migration's invariant means the fix is one-time, not systemic |
| Evidence Quality | Neutral | Migration evidence is solid (grep-verified, 32 agents confirmed) |
| Actionability | Negative | PM-005: Engagement-id generation gap leaves P3 default non-actionable for pure standalone callers |
| Traceability | Neutral | ADR traces correctly to BUG-006 entity and audit detail files |

**Overall S-004 Assessment:** REVISE — 1 Critical and 3 Major failure causes identified. The most significant finding is PM-001: the absence of a CI gate means the migration is a one-time fix that the framework cannot self-enforce. The BUG-006 root cause analysis itself identified "No CI gate checking for hardcoded skill-internal output paths" as a contributing factor — the implementation plan (TASK-006 through TASK-012) does not include a TASK for adding a CI gate.

---

## S-001: Red Team Analysis

### Threat Actor Profile

**Goal:** Exploit ambiguity, gaps, and rule-boundary conditions in the ADR and implementation to produce agent outputs in wrong locations, bypass the migration's intent, or cause new skill authors to reintroduce the anti-pattern without triggering any governance warning.

**Capability:** Full access to the codebase, CLAUDE.md, agent-development-standards.md, and the migration implementation. Understands the Jerry governance model, the MEDIUM/HARD tier enforcement vocabulary, and the LLM agent behavioral model.

**Motivation:** Reduce migration overhead — produce outputs wherever is easiest (skill directories), avoid engagement-id management complexity, or create new skills without being constrained by the new convention.

### Attack Vector Inventory

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-------------------|
| RT-001-20260401 | AD-M-011 MEDIUM tier override: new agent governance file claims "engagement isolation requires skill-internal output directory" and bypasses the standard | Rule Circumvention | High | Critical | P0 | Missing | Methodological Rigor |
| RT-002-20260401 | UX orchestrator composition YAML not in ADR's file count: 11 UX composition YAML files exist but the ADR's grep-verification command does not include them explicitly — a partial migration of UX composition YAML would not be caught by the specified verification | Boundary | Medium | Major | P1 | Partial | Completeness |
| RT-003-20260401 | P2 base_path ambiguity: if caller provides `base_path: projects/${JERRY_PROJECT}/engagements/RED-0001/` (with trailing slash) while another call omits the trailing slash, agents may produce `projects/${JERRY_PROJECT}/engagements/RED-0001//red-recon-topic.md` (double slash) | Ambiguity | Low | Minor | P2 | Missing | Internal Consistency |
| RT-004-20260401 | UX composition YAML count ambiguity: ADR states "11 UX files" for governance YAML but the UX orchestrator's composition YAML is not explicitly listed — UX has 11 sub-skills but the parent orchestrator also has governance+composition YAML. The grep results confirm 11 UX governance YAML matches for `filename_pattern` but the composition count for UX was not verified | Boundary | Medium | Major | P1 | Partial | Evidence Quality |
| RT-005-20260401 | Degradation via context rot: agents with long sessions may lose the Output Path Resolution section from working memory as context fills — the LLM may fall back to "writing to output/ wherever seems reasonable" after the governance YAML content is no longer attended to | Degradation | Medium | Major | P1 | Missing | Methodological Rigor |

### Defense Gap Assessment

#### RT-001: AD-M-011 Override Path [CRITICAL]

**Attack Vector:** An adversary building a new skill writes a governance YAML with `output.location: "skills/new-skill/output/{engagement-id}/new-agent-{topic-slug}.md"` and adds a comment `# AD-M-011 override: skill-internal output required for engagement isolation`. Since AD-M-011 is MEDIUM tier, this is a valid governance action.

**Category:** Rule Circumvention

**Exploitability:** High — the override mechanism is documented and legitimate; the adversary does not need to hide the deviation.

**Existing Defense:** Missing — .gitignore blocks output files from being committed, but new YAML pointing to those paths would still be committed. The YAML content is not blocked by .gitignore.

**Evidence:** ADR Migration Guide Step 5 (line 509): "Override requires documented justification per MEDIUM tier vocabulary." Agent-development-standards.md MEDIUM Standards preamble: "Override requires documented justification."

**Dimension:** Methodological Rigor

**Countermeasure:** L5 CI gate on `skills/*/output/` in any file in the `skills/` directory (not just output files) — this would catch governance YAML, composition YAML, and agent .md files referencing the old pattern, regardless of whether outputs actually land there.

**Acceptance Criteria:** CI gate scans all text files under `skills/` (not just governance YAML) for the pattern `skills/.*/output/` and fails the build on any match.

---

#### RT-002: UX Composition YAML Coverage Gap [MAJOR]

**Attack Vector:** The ADR's primary verification command is `grep -r 'skills/.*/output/' skills/`. This command would catch any remaining old-pattern references, including in UX composition YAML files. However, the file count claims in the ADR ("22 eng-team + 25 red-team + 60 UX = 107") do not explicitly enumerate UX composition YAML. The UX audit detail (`BUG-006-ux-audit-detail.md`) lists governance YAML but the per-skill tables show "Agent governance YAML: yes" without explicitly listing composition YAML separately.

**Category:** Boundary

**Exploitability:** Medium — the primary grep would catch any remaining violations, but the adversary exploiting this would be an auditor concluding the migration was incomplete based on ambiguous documentation rather than an actual gap.

**Existing Defense:** Partial — the grep command would catch UX composition YAML violations if they existed. The grep confirmation (0 matches) covers all files under `skills/`.

**Evidence:** BUG-006 UX audit detail (per-skill tables): lists "Agent .md" and "Agent governance YAML" for each sub-skill but the composition YAML is not explicitly inventoried in the UX audit. The eng audit explicitly lists "Agent Composition YAML — 10 files" as a separate section.

**Dimension:** Evidence Quality (audit documentation asymmetry)

**Countermeasure:** Update BUG-006-ux-audit-detail.md to explicitly enumerate UX composition YAML files (one per sub-skill = 11 files) in a format parallel to the eng audit detail's "Agent Composition YAML" section.

**Acceptance Criteria:** UX audit detail includes an explicit "Agent Composition YAML" section listing all 11 composition YAML files, parallel to the eng audit detail format.

---

#### RT-004: UX Agent Count Verification Gap [MAJOR]

**Attack Vector:** The ADR claims "11 UX files" for governance YAML migration. Grep confirms 11 UX governance YAML files have `filename_pattern`. However, the UX family includes the parent `ux-orchestrator` (in `skills/user-experience/`) plus 10 sub-skills (in `skills/ux-*/`) — totaling 11. The grep results list all 11, but the UX audit detail section headers enumerate only 11 sub-skills starting with "user-experience (parent orchestrator)" — consistent with the total. The potential attack is claiming the count is wrong to cast doubt on the migration's completeness.

**Category:** Boundary

**Exploitability:** Medium — the grep evidence (11 UX files for `filename_pattern`, 32 total) resolves the count definitively.

**Existing Defense:** Partial — grep evidence confirms 32 total governance YAML files have `filename_pattern`. The 32 count (10 eng + 11 red + 11 UX) matches the ADR's claim. The individual grep results list each file, providing traceability.

**Evidence:** Grep result: 32 total `filename_pattern` occurrences across 32 files. Files listed include `ux-orchestrator.governance.yaml` + 10 sub-skill files (ux-heart-metrics, ux-atomic-design, ux-jtbd, ux-heuristic-eval, ux-inclusive-design, ux-design-sprint, ux-ai-first-design, ux-lean-ux, ux-behavior-design, ux-kano-model) = 11 UX files. Total verified.

**Dimension:** Evidence Quality

**Countermeasure:** Add an explicit count verification table to the BUG-006-ux-audit-detail.md "Agent Governance YAML" section listing all 11 files by path, parallel to the eng/red audit detail format.

**Acceptance Criteria:** UX audit detail includes explicit governance YAML list with 11 files, enabling auditor verification without relying solely on grep count.

---

#### RT-005: Context Rot Degrades Output Path Resolution [MAJOR]

**Attack Vector:** An agent operating in a long session (context fill > 70%) may lose effective attention to the `Output Path Resolution` section added to agent .md files. The section is in the `<output>` block of each agent definition, which is loaded at session start. As context fills, early-session instructions degrade (L1 vulnerability per quality-enforcement.md enforcement architecture). The agent may default to writing to `output/` in a location it "knows" from prior training data or from earlier in the session when old-pattern YAML was visible.

**Category:** Degradation

**Exploitability:** Medium — context rot is a documented framework risk (AE-006c/AE-006d auto-escalation at 80%/88% fill). The Output Path Resolution section is not re-injected at L2 (per-prompt).

**Existing Defense:** Missing — the Output Path Resolution section is a Tier 2 content block (loaded at session start) with L1 vulnerability to context rot. No L2 re-injection marker exists for the output path protocol in any agent .md.

**Evidence:** Quality-enforcement.md Enforcement Architecture: "L1 — Session start — Behavioral foundation via rules — Vulnerable — ~12,500 tokens." Agent .md Output Path Resolution sections are L1 content. L2 re-injection covers only HARD rules (H-01 through H-36), not output path behavior.

**Dimension:** Methodological Rigor

**Countermeasure:** Add a brief L2-compatible reminder in each agent's output section or in SKILL.md frontmatter `description` field: "Output MUST follow ADR-EPIC002-001 path resolution: P1 explicit > P2 base_path > P3 default template > P4 fallback." This does not need to be full re-injection — a prominent reminder in the agent's active task instructions each turn is sufficient.

**Acceptance Criteria:** At least one mechanism exists to remind agents of the output path resolution protocol during mid-session turns, not only at session start.

---

### S-001 Recommendations

**P0 (Critical — MUST mitigate):**

- **RT-001:** Add L5 CI gate scanning all text files under `skills/` for `skills/.*/output/` pattern. Gate fails build on any match. This converts AD-M-011's MEDIUM-tier SHOULD into a mechanically-enforced invariant.

**P1 (Important — SHOULD mitigate):**

- **RT-002:** Update BUG-006-ux-audit-detail.md to add explicit UX composition YAML section (11 files) parallel to eng audit format.
- **RT-004:** Add explicit file list to UX audit detail governance YAML section for auditor traceability.
- **RT-005:** Add output path protocol reminder to agent SKILL.md `description` field or per-turn task instructions to mitigate context rot degradation.

**P2 (Monitor):**

- **RT-003:** Document that `base_path` values MUST NOT include trailing slashes, or that agents MUST normalize double-slash paths before writing. Add to Failure Mode Analysis.

### S-001 Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Completeness | Negative | RT-002, RT-004: UX audit documentation incomplete for composition YAML; RT-001: CI gate absent |
| Internal Consistency | Neutral | Migration logic is internally consistent; ambiguity (RT-003) is minor |
| Methodological Rigor | Negative | RT-001: No recurring enforcement mechanism; RT-005: Context rot degrades the Output Path Resolution section without L2 re-injection |
| Evidence Quality | Negative | RT-002, RT-004: UX composition YAML coverage documentation less rigorous than eng/red families |
| Actionability | Neutral | Countermeasures are specific and actionable |
| Traceability | Neutral | ADR traces correctly; the gap is prospective audit traceability, not existing traceability |

**Overall S-001 Assessment:** REVISE — 1 Critical and 3 Major attack vectors identified. The core implementation is correct (grep-verified, 0 old-pattern matches, 32 files with new pattern), but the attack surface includes: (1) the MEDIUM-tier standard with no CI enforcement for future agents, (2) context rot degrading the Output Path Resolution section without L2 re-injection, and (3) UX audit documentation asymmetry relative to eng/red families.

---

## Consolidated Findings Summary

| ID | Strategy | Severity | Finding | Priority |
|----|----------|----------|---------|---------|
| PM-001-20260401 | S-004 | Critical | No CI gate to enforce output path convention for new agents | P0 |
| RT-001-20260401 | S-001 | Critical | AD-M-011 MEDIUM override path allows new skill authors to bypass with documented justification | P0 |
| DA-001-20260401 | S-002 | Major | Composition YAML absent from ADR verification table | P1 |
| DA-002-20260401 | S-002 | Major | P4 fallback prevention mechanism (SessionStart hook) unspecified | P1 |
| DA-004-20260401 | S-002 | Major | Migration guide step numbering ambiguity (Step 0 = Step 6) | P1 |
| PM-002-20260401 | S-004 | Major | AD-M-011 MEDIUM tier permits silent deviation without governance violation | P1 |
| PM-003-20260401 | S-004 | Major | Wave-progression.md signoff table has no update trigger for new UX sub-skills | P1 |
| PM-005-20260401 | S-004 | Major | No default engagement-id generation leaves P3 default non-actionable for standalone callers | P1 |
| RT-002-20260401 | S-001 | Major | UX composition YAML not explicitly inventoried in audit detail (documentation gap) | P1 |
| RT-004-20260401 | S-001 | Major | UX governance YAML file list not enumerated per-file in audit detail (auditor traceability gap) | P1 |
| RT-005-20260401 | S-001 | Major | Context rot degrades Output Path Resolution section with no L2 re-injection countermeasure | P1 |
| DA-003-20260401 | S-002 | Minor | `{agent}` variable notation inconsistency in ADR Agent Integration Specification | P2 |
| DA-005-20260401 | S-002 | Minor | /nasa-se backward compat assertion lacks grep-verified evidence | P2 |
| PM-004-20260401 | S-004 | Minor | Historical references to old paths in GH issues (cosmetic) | P2 |
| PM-006-20260401 | S-004 | Minor | Session-cached old instructions may persist until session end | P2 |
| RT-003-20260401 | S-001 | Minor | Trailing slash normalization not specified for P2 base_path | P2 |

---

## Cross-Strategy Synthesis

Three strategies converge on two systemic findings:

**Finding 1 — No CI Gate (PM-001 + RT-001 + DA-001):** The migration fixes the existing 107 files but has no recurring enforcement mechanism. S-004 identifies this as a critical operational failure mode. S-001 identifies it as the highest-exploitability attack vector. S-002 identifies that even the verification table omits composition YAML. All three strategies point to the same root gap: the implementation is a one-time fix, not a self-enforcing standard. This is consistent with the BUG-006 root cause analysis which explicitly listed "No CI gate" as a contributing factor — but the task list (TASK-006 through TASK-012) contains no TASK for adding a CI gate.

**Finding 2 — Documentation Asymmetry in UX Audit (RT-002 + RT-004):** The eng-team and red-team audit details explicitly list composition YAML as a separate audited category. The UX audit detail does not. While the primary grep covers all files and confirms 0 violations, the documentation asymmetry creates an auditor confidence gap that could be exploited to question migration completeness.

**Finding 3 — Engagement-ID Gap in P3 (PM-005):** All three strategies touch the P3 default path: S-002 (DA-003, notation clarity), S-004 (PM-005, missing default generation), S-001 (RT-003, trailing slash normalization). The pattern suggests the P2/P3 caller convention is under-specified for standalone users who do not read the ADR before invoking agents.

---

## Execution Statistics

- **Total Findings:** 16
- **Critical:** 2 (PM-001, RT-001)
- **Major:** 9 (DA-001, DA-002, DA-004, PM-002, PM-003, PM-005, RT-002, RT-004, RT-005)
- **Minor:** 5 (DA-003, DA-005, PM-004, PM-006, RT-003)
- **Protocol Steps Completed:**
  - S-002: 5 of 5 steps
  - S-004: 6 of 6 steps
  - S-001: 5 of 5 steps

## H-15 Self-Review

Before persistence:

- [x] All findings have specific evidence from the deliverable (no vague findings)
- [x] Severity classifications are justified: Critical findings each identify a systemic enforcement gap with high reintroduction likelihood; Major findings identify significant documentation or specification gaps; Minor findings identify improvement opportunities
- [x] Finding identifiers follow template prefixes: DA-NNN-20260401, PM-NNN-20260401, RT-NNN-20260401
- [x] Summary table matches detailed findings (16 total, 2C/9M/5Mi)
- [x] No findings minimized: the two Critical findings (PM-001, RT-001) converge on the same root gap and are classified consistently across strategies
- [x] Cross-strategy synthesis notes convergence of all three strategies on the CI gate finding

**Self-Review Result:** PASS

---

*Strategy Execution Report: Group C*
*Strategies: S-002 (Devil's Advocate), S-004 (Pre-Mortem Analysis), S-001 (Red Team Analysis)*
*Agent: adv-executor (claude-sonnet-4-6)*
*Deliverable: ADR-EPIC002-001 + BUG-006 migration implementation*
*Criticality: C4*
*Date: 2026-04-01*
*SSOT: `.context/rules/quality-enforcement.md`*
