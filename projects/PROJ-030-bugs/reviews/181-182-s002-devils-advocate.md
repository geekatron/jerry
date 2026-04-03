# Devil's Advocate Report: `.claude/settings.local.json` (#181/#182 Implementation)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `.claude/settings.local.json` (GitHub Issues #181/#182)
**Companion Design:** `projects/PROJ-030-bugs/work/devsecops/settings-local-json-design.md`
**Criticality:** C4 (Critical — governs all tool permissions for every session)
**Date:** 2026-03-14
**Reviewer:** adv-executor
**H-16 Compliance:** S-003 Steelman applied 2026-03-14 (confirmed — `181-182-s003-steelman.md` line 183: "H-16 Status: S-003 first; S-002/S-004 may now proceed")

---

## Step 1: Role Assumption

The Devil's Advocate role is formally assumed. The mandate is to construct the strongest possible case against the design decisions in the `settings.local.json` implementation. The steelmanned argument (S-003) must be engaged directly — not strawmanned. Where the S-003 reconstruction makes its strongest claims, this report must challenge those claims with the best available counter-arguments.

The deliverable is a 56-line JSON configuration file. The companion design document is the carrier of rationale. Both are subject to challenge. Critical finding criteria: a counter-argument that invalidates a core claim or reveals a HARD rule violation or a factual error in the implementation.

---

## Summary

7 counter-arguments identified (2 Critical, 3 Major, 2 Minor). The Critical findings are not about the security reasoning — the S-003 steelman defended that well — but about a **factual discrepancy between the design document and the actual file**, and about the **completeness of the skill enumeration claim** that underpins the entire Decision 2. The design document says `Bash(git push *)` is kept; the actual file omits it. The design document claims 25 allow entries; the actual file has 24. The design document says 19 skills are enumerated against CLAUDE.md; but CLAUDE.md registers more than 19 skills in its Quick Reference table. These are not framing issues — they are correctness failures.

**Recommendation: REVISE.** Address DA-001 (file/design discrepancy) and DA-002 (skill count completeness) before accepting. The layered architecture reasoning (SM-002, SM-003 from S-003) withstands scrutiny on its own terms but rests on a factual foundation that has not been verified.

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-20260314 | Design document and actual file are inconsistent on `git push` and entry count | Critical | Design doc L1 §4 line 136: "Keep it in local `allow`." Actual file: no `Bash(git push *)` entry. Design doc L0 claims 25 entries; actual file has 24. | Internal Consistency |
| DA-002-20260314 | The "19 skills" completeness claim is unverified and potentially wrong | Critical | Design doc Decision 2: "CLAUDE.md registers 19 skills." CLAUDE.md Quick Reference table lists 16 skills by name, but also registers `/saucer-boy-framework-voice`, `/ast`, `/eng-team`, `/red-team`, `/pm-pmm`, `/prompt-engineering`, `/diataxis`, `/user-experience` — the count depends on what "registered" means, and the design does not verify it deterministically | Completeness |
| DA-003-20260314 | Removing `Skill(jerry:name)` is irreversible risk without a verified fallback test | Major | Design doc Decision 1 fallback: "If removing the colon form causes approval prompts, it can be restored in a follow-up commit." No test protocol defined. At C4 criticality, a permission regression would break H-22 for all skills silently. | Methodological Rigor |
| DA-004-20260314 | The S-003 "git push is system operating as designed" reframe does not neutralize the actual runtime risk | Major | S-003 SM-003 reframes T-01 as "operating as designed." But the design doc's own analysis (Decision 4, final paragraph) reveals that `deny > ask > allow` with "first matching rule wins" and local (precedence 3) overrides shared (precedence 4) — this evaluation order is asserted, not empirically verified. If the precedence behavior changes or is misread, the result is either silent rejection (push always requires approval) or auto-approval escalation. | Evidence Quality |
| DA-005-20260314 | `mcp__plugin_context7_context7__*` wildcard has no documented rationale for its continued existence | Major | Design doc Decision 6: the entry exists "because of the Context7 plugin namespace convention (GitHub Issue #29360)." But the entry is a wildcard covering an entire unnamed plugin namespace. If the plugin namespace convention is a workaround for a known bug (#29360), the wildcard may grant permissions to future tools added under that namespace without review. | Completeness |
| DA-006-20260314 | The "Bash(grep *) is read-only" safety claim is factually incomplete | Minor | Design doc T-07 mitigation: "`grep` is read-only. The deny array blocks `curl` and `wget` for exfiltration prevention." But `grep` can write via shell redirection (`grep pattern file > /tmp/out`), and the `Bash(grep *)` permission pattern matches `grep ... > somefile` as a complete Bash command. The deny array blocks `curl`/`wget` as standalone tools but does not restrict output redirection within approved Bash commands. | Evidence Quality |
| DA-007-20260314 | No verification step is defined to confirm the corrected file actually eliminates the approval prompts it claims to fix | Minor | Design doc L0: "Claude Code may prompt for approval on every invocation." The corrected file is deployed without a defined acceptance test. For a C4 artifact, no smoke test or post-deploy verification step is specified. | Actionability |

---

## Detailed Findings

### DA-001-20260314: Design Document and Actual File Are Inconsistent [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Design doc Decision 4 vs. actual `.claude/settings.local.json` |
| **Strategy Step** | Step 2 (Challenge Assumptions) + Step 3 (Construct Counter-Arguments) |

**Claim Challenged:**
Design doc Decision 4, final paragraph: "**Keep it in local `allow`.**" (referring to `Bash(git push *)`). Design doc L0: "Total allow entries: 25 (down from 56)."

**Counter-Argument:**
The actual `settings.local.json` file does NOT contain `Bash(git push *)`. The file contains exactly 24 allow entries: 19 Skill entries, 3 MCP wildcard entries, and 2 Bash entries (`Bash(git stash *)` and `Bash(grep *)`). The design document's Decision 4 table explicitly marks `Bash(git push *)` with "Keep? No" in the local-only entries table — then the final paragraph reverses that decision and says "Keep it" — and the actual file follows the "No" column, not the reversal paragraph.

This is not a semantic ambiguity. Either:
- The design document contains an internal contradiction (the table says "No" and the conclusion paragraph says "Keep"), and the file implements one half of that contradiction; or
- The file was generated from the table's "No" decision and the reversal paragraph was added to the design doc after the file was written, creating a stale design doc.

Either way: the design document cannot be used as an accurate specification for the file it claims to describe. The S-003 SM-003 reframe ("git push is system operating as designed") depends on the `Bash(git push *)` entry existing in the file — but it does not exist. The steelmanned defense of that decision defends a configuration that was not implemented.

**Evidence:**
- Design doc line 134: Table row `Bash(git push *)` | No | "Already in `settings.json` `ask` array"
- Design doc line 136: "This means the local `allow` entry intentionally overrides the shared `ask` entry, auto-approving `git push` for this developer. This is a valid developer-specific override. **Keep it in local `allow`.**"
- Actual file: lines 1-56 contain no `Bash(git push *)` entry
- Design doc L0 line 29: "Total allow entries: 25 (down from 56)" — actual count is 24

**Impact:**
The design document is not an accurate description of the delivered artifact. Any downstream strategy (S-004, S-012) that uses the design document as the specification will be reviewing a different artifact than what is actually deployed. The S-014 scoring will be scoring a document that misrepresents the implementation.

**Dimension:** Internal Consistency

**Response Required:**
The creator must either (a) add `Bash(git push *)` to the actual file to match the design doc's stated decision, or (b) update the design doc to reflect that `Bash(git push *)` was deliberately excluded and remove the contradicting "Keep it" paragraph. The choice reveals whether the final decision was to keep or remove git push auto-approval — which is the most security-sensitive Bash permission in the file.

**Acceptance Criteria:**
Design document and actual file must agree on the presence or absence of `Bash(git push *)`. Entry count must be consistent across L0 summary and actual file. One authoritative statement of the final decision, not two contradicting statements.

---

### DA-002-20260314: The "19 Skills" Completeness Claim Is Unverified [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Design doc Decision 2 and CLAUDE.md |
| **Strategy Step** | Step 2 (Challenge Assumptions) + Step 3 |

**Claim Challenged:**
Design doc Decision 2: "CLAUDE.md registers 19 skills. Only 7 had permission entries." Design doc L0: "Add `Skill(name)` entries for all 19 CLAUDE.md-registered skills."

**Counter-Argument:**
The claim that CLAUDE.md registers exactly 19 skills is an unverified assertion. The design document provides a table of 19 skills and notes what was "Previously Present" vs. "Added," but does not demonstrate that this list is complete by citing specific CLAUDE.md line numbers or the current CLAUDE.md Quick Reference table state.

The actual CLAUDE.md Quick Reference table (as of this review) lists skills in the Skills table. The design document explicitly excludes `bootstrap` ("not registered in CLAUDE.md") and the 10 `ux-*` sub-skills ("invoked through the parent skill"). These exclusions are policy decisions, not factual assertions about what CLAUDE.md contains — but they are presented as if they are factual.

The completeness argument is the entire foundation of FINDING-003 (missing skill permissions break H-22). If the enumeration is incomplete — if CLAUDE.md has been updated to add skills that are not in the 19-item list — then the implementation has not actually resolved FINDING-003. It has merely reduced the gap.

Furthermore, the security framing from S-003 SM-001 (approval fatigue as a security control) strengthens the severity of any incompleteness: if any skill is missing from the permission list, the approval-fatigue vulnerability persists for that skill.

**Evidence:**
- Design doc Decision 2 table lists 19 skills with "Previously Present" and "Note" columns
- No citation to specific CLAUDE.md line numbers
- Design doc Decision 2, "Not included" section: exclusion rationale provided for `bootstrap` and `ux-*` sub-skills, but without verification that no other skills exist in CLAUDE.md that are similarly categorized
- The 19-skill count is treated as a closed claim throughout the document

**Impact:**
If one or more skills registered in CLAUDE.md are absent from `settings.local.json`, H-22 continues to be violated for those skills. The implementation claims to resolve FINDING-003 but may have only partially resolved it.

**Dimension:** Completeness

**Response Required:**
The creator must provide an explicit, line-cited comparison between the current CLAUDE.md Quick Reference Skills table and the 19-item permission list in `settings.local.json`. The comparison must show: (a) every skill in CLAUDE.md that has a `Skill(name)` entry in the file, and (b) every skill in CLAUDE.md that is intentionally excluded with documented rationale.

**Acceptance Criteria:**
A mapping table with CLAUDE.md source line numbers confirming that the 19-skill enumeration is complete (or updated to the correct count). The exclusion rationale for `bootstrap` and `ux-*` sub-skills must be explicitly stated as a policy decision, not implied.

---

### DA-003-20260314: Removing `Skill(jerry:name)` Is Irreversible Risk Without a Verified Fallback Test [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Design doc Decision 1 |
| **Strategy Step** | Step 3 (Counter-Arguments, lens: Unaddressed Risks) |

**Claim Challenged:**
Design doc Decision 1 rationale: "If removing the colon form causes approval prompts, it can be restored in a follow-up commit."

**Counter-Argument:**
The fallback path "restore in a follow-up commit" is only viable if the permission regression is detected. At C4 criticality, a permission regression that causes skills to trigger approval prompts is a silent failure mode — it does not raise an error, it merely prompts the developer. If the developer is in a flow state and approves reflexively (exactly the T-05 approval-fatigue behavior the implementation claims to prevent), the regression goes undetected.

The design asserts that `Skill(name)` is the documented form and `Skill(jerry:name)` is undocumented, citing research references 1 and 2 and GitHub Issue #29360. But the decision document does not show that `Skill(name)` form was empirically verified to match the skills in this specific Claude Code version, on this specific platform (darwin), with this specific skill directory structure. The research is about documentation form, not runtime behavior.

For a C4 artifact, "we believe it will work based on documentation" is a weaker justification than "we tested it and it worked." The fallback is described as trivial but the regression detection path relies on developer attention.

**Evidence:**
- Design doc Decision 1 last sentence: "If removing the colon form causes approval prompts, it can be restored in a follow-up commit."
- No test protocol defined in the design document
- No acceptance test in the implementation

**Impact:**
If `Skill(name)` does not correctly match skill invocations in the runtime environment, all 19 skill permissions silently revert to requiring manual approval, breaking H-22 for every skill. This would be a complete rollback of the FINDING-003 fix.

**Dimension:** Methodological Rigor

**Response Required:**
Define and execute a smoke test: invoke at least one previously-failing skill after deploying the corrected file and confirm no approval prompt is raised. Document the test result. The acceptance threshold for C4 is demonstrated behavior, not documented expectation.

**Acceptance Criteria:**
A smoke test result (pass/fail) documented alongside the implementation, showing that at least one of the newly-added `Skill(name)` entries correctly auto-approves a skill invocation without prompting.

---

### DA-004-20260314: The `git push` Override Relies on Asserted-Not-Verified Precedence Behavior [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major (conditional on DA-001 resolution) |
| **Section** | Design doc Decision 4, "Reconsideration on `git push`" |
| **Strategy Step** | Step 3 (Counter-Arguments, lens: Unstated Assumptions) |

**Claim Challenged:**
Design doc Decision 4: "Per Claude Code evaluation order documentation, `deny > ask > allow` with 'first matching rule wins' — but the precedence documentation also states that local (precedence 3) overrides shared (precedence 4). This means the local `allow` entry intentionally overrides the shared `ask` entry."

**Counter-Argument:**
The precedence claim has an internal tension that the design does not resolve. The evaluation model `deny > ask > allow` applies within a single settings file. The cross-file precedence rule "local (3) overrides shared (4)" applies to which file takes precedence when both contain an entry for the same permission.

The question is: does "local overrides shared" mean the local file's `allow` entry replaces the shared file's `ask` entry entirely (so the local `allow` wins), or does it mean the two files are merged and then `deny > ask > allow` is applied to the merged result (so `ask` from shared would still win over `allow` from local)?

The design cites the precedence documentation for the first interpretation but does not rule out the second. If Claude Code implements merged evaluation rather than file-level override, the `ask` entry in `settings.json` would continue to gate `git push` regardless of the local `allow` entry. The developer's belief that `git push` is auto-approved could be incorrect, and they would not know until they tried to push.

Note: This finding becomes moot if DA-001 is resolved by removing the `Bash(git push *)` entry (the "No" decision from the table). The finding remains relevant if DA-001 is resolved by adding the entry back.

**Evidence:**
- Design doc Decision 4: "Per Claude Code evaluation order documentation, `deny > ask > allow` with 'first matching rule wins'"
- Design doc Decision 4: "the precedence documentation also states that local (precedence 3) overrides shared (precedence 4)"
- No empirical test of the interaction between local `allow` and shared `ask` for the same command

**Impact:**
Developer believes `git push` is auto-approved but it requires manual approval on every invocation — or, conversely, developer believes there is a team safety gate on `git push` but the local override has silently removed it.

**Dimension:** Evidence Quality

**Response Required:**
Provide the specific Claude Code documentation citation or empirical test result that resolves the ambiguity between file-level override vs. merged evaluation for the `allow` vs. `ask` cross-file scenario. Alternatively, test empirically: create a minimal settings pair and observe which behavior Claude Code exhibits.

**Acceptance Criteria:**
Either (a) a documentation citation that unambiguously describes the cross-file `allow` vs. `ask` interaction, or (b) an empirical test result showing the observed runtime behavior.

---

### DA-005-20260314: `mcp__plugin_context7_context7__*` Wildcard Scope Is Insufficiently Justified [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Design doc Decision 6 |
| **Strategy Step** | Step 3 (Counter-Arguments, lens: Unaddressed Risks) |

**Claim Challenged:**
Design doc Decision 6: "The `mcp__plugin_context7_context7__*` entries exist because of the Context7 plugin namespace convention (GitHub Issue #29360)."

**Counter-Argument:**
The S-003 SM-005 argument ("MCP wildcards appropriate for developer-local config; agent-level governance provides second layer") defends `mcp__memory-keeper__*` and `mcp__context7__*` — both of which are named, documented MCP servers with known tool sets. The `mcp__plugin_context7_context7__*` wildcard is different in kind: it is a workaround for a known bug (#29360) in Claude Code's plugin namespace resolution.

A wildcard created to work around a bug in namespace resolution has an indefinite scope. If the bug is fixed, the workaround wildcard may no longer be needed — but it remains in the file, now granting permissions to whatever tools might be exposed under the `plugin_context7_context7` namespace in a future Claude Code version. The design doc does not document a review trigger for this entry ("if Issue #29360 is closed, remove this entry").

The `mcp-tool-standards.md` agent-level governance (the second layer SM-005 relies on) restricts which agents can use which tools. But an agent with `mcp__context7__*` in `allowed_tools` might also match `mcp__plugin_context7_context7__*` permissions if the plugin convention is active — the agent-level governance was designed for the named server, not the plugin namespace alias.

**Evidence:**
- Design doc Decision 6: "The `mcp__plugin_context7_context7__*` entries exist because of the Context7 plugin namespace convention (GitHub Issue #29360)."
- No documentation of what tools this namespace exposes
- No review trigger defined for when Issue #29360 is resolved
- Agent definitions in `skills/*/agents/*.md` declare `context7` tools, not `plugin_context7_context7` tools

**Impact:**
Permanent wildcard permission for a namespace created as a bug workaround. If the plugin namespace ever exposes tools beyond `resolve-library-id` and `query-docs`, those tools receive automatic permission without explicit review.

**Dimension:** Completeness

**Response Required:**
Document what tools are exposed under the `mcp__plugin_context7_context7__*` namespace (by inspecting the MCP server configuration). Add a review trigger comment noting that this entry should be re-evaluated when Issue #29360 is resolved. Alternatively, replace the wildcard with specific tool entries for only the known tools.

**Acceptance Criteria:**
Either (a) specific tool entries replacing the wildcard, or (b) a comment in the settings file or design doc listing the known tools under this namespace and a review trigger for Issue #29360 resolution.

---

## Recommendations

### P0 — Critical (MUST resolve before acceptance)

**DA-001:** Reconcile the design document and the actual file on `Bash(git push *)`.
- Action: Either add `Bash(git push *)` to `settings.local.json` (implementing the "Keep it" decision) or update the design doc to remove the "Keep it" paragraph (implementing the "No" decision from the table).
- Acceptance criteria: One authoritative, non-contradicting statement across design doc and actual file. Entry count in L0 summary must match actual file.

**DA-002:** Verify the 19-skill enumeration against current CLAUDE.md.
- Action: Perform a line-cited comparison between CLAUDE.md Quick Reference Skills table and the 19 `Skill(name)` entries in `settings.local.json`. Confirm count and document exclusion rationale for intentionally-omitted skills.
- Acceptance criteria: Mapping table with CLAUDE.md source references. Any discrepancy results in either adding missing skills or documenting the exclusion rationale.

### P1 — Major (SHOULD resolve; require justification if not)

**DA-003:** Define and execute a smoke test for `Skill(name)` form correctness.
- Action: Invoke at least one newly-added skill (e.g., `Skill(architecture)` or `Skill(diataxis)`) and confirm no approval prompt appears. Document result.
- Acceptance criteria: Observed behavior (no approval prompt) confirmed.

**DA-004:** Resolve the cross-file `allow` vs. `ask` precedence ambiguity.
- Action: Cite documentation or empirical test for whether local `allow` overrides shared `ask` in merged evaluation.
- Acceptance criteria: Unambiguous determination of runtime behavior. (Note: moot if DA-001 removes `git push` from local.)

**DA-005:** Document the scope and review trigger for `mcp__plugin_context7_context7__*`.
- Action: List known tools under this namespace; add review trigger tied to Issue #29360 resolution.
- Acceptance criteria: Documented tool scope and review trigger condition.

### P2 — Minor (MAY resolve; acknowledgment sufficient)

**DA-006:** Acknowledge that `Bash(grep *)` permits output redirection and confirm this is acceptable risk.
- Action: Add a note to the threat model that T-07 "read-only" characterization is a simplification; `grep` with redirection can write to files. The accepted-risk determination remains valid but should be stated accurately.

**DA-007:** Define a post-deploy verification step for the corrected file.
- Action: Add a "Verification" section to the design doc listing 1-2 observable behaviors that confirm the fix is working (e.g., skill invocations no longer prompt; deprecated syntax no longer in file).

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-002: The core completeness claim (all 19 skills enumerated) is unverified. DA-005: MCP wildcard scope undocumented. Both findings target the deliverable's claim to complete coverage. |
| Internal Consistency | 0.20 | Negative | DA-001: Design doc and actual file contradict each other on the most security-sensitive Bash entry. This is a direct Internal Consistency failure — the artifact cannot be both documents simultaneously. |
| Methodological Rigor | 0.20 | Negative | DA-003: No smoke test or post-deploy verification. For a C4 configuration artifact, empirical verification is part of rigorous methodology. The design stops at documentation of expected behavior. |
| Evidence Quality | 0.15 | Negative | DA-004: The cross-file precedence claim is asserted without empirical evidence. DA-006: The "grep is read-only" mitigation is technically incomplete. |
| Actionability | 0.15 | Neutral | The design document provides clear decisions and rationale. The S-003 improvements (SM-002 architectural principle) strengthen actionability for future decisions. DA-007 (minor) does not materially reduce the existing actionability. |
| Traceability | 0.10 | Neutral | Findings trace to FINDINGs, decisions trace to design rationale, threat model maps to STRIDE/DREAD/NIST CSF. Traceability is a strength of this deliverable. DA-001 does not break traceability — it reveals a decision reversal that is fully traceable but internally contradictory. |

**Net assessment:** 4 of 6 dimensions negatively impacted. The two Critical findings (DA-001, DA-002) each target a different dimension (Internal Consistency, Completeness) and represent factual correctness failures, not framing weaknesses. The steelmanned argument from S-003 is architecturally sound — the two-layer permission model, the security framing of approval fatigue, and the defense-in-depth for MCP wildcards are all valid — but the steelman defends a design that the actual file does not fully implement.

---

## Execution Statistics
- **Total Findings:** 7
- **Critical:** 2
- **Major:** 3
- **Minor:** 2
- **Protocol Steps Completed:** 5 of 5
- **H-16 Compliance:** S-003 confirmed before execution
- **H-15 Self-Review:** Applied before persistence

---

*Strategy: S-002 Devil's Advocate*
*Template: `.context/templates/adversarial/s-002-devils-advocate.md` v1.0.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Executed: 2026-03-14*
*Criticality: C4*
