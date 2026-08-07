# Pre-Mortem Report: GitHub Issue #354 (BUG-005 / REM-05, H-36 governance ruling)

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `issue-354.md` — live text of GitHub issue #354, geekatron/jerry
**Criticality:** C4 (tournament)
**H-16 Compliance:** N/A for this compact single-artifact review — no prior S-003 output provided in context; findings below are limited to failure-mode enumeration per S-004 protocol, adapted for a ~300-word text artifact.
**Failure Scenario:** It is six months from now. The owner read issue #354, ruled on the H-36 question using only the eng-team precedent cited in the issue, and closed it. Weeks later the contributor's BUG-001 redesign picks a delegation topology that changes what counts as a "hop" for nuclear-sop, invalidating the ruling. Separately, two of the three assignees each assumed the other was "the owner" and neither acted for a month. The issue had to be reopened and re-litigated.

## Summary

Fact-checking against the remediation register, BUG-005 entity, verdict, and the actual PR-branch rule file confirms every factual claim in the issue text (deadline date, contradictory fallback instructions, missing tracking work-item, eng-team precedent, 3-hop rule) is accurate and traceable. Failure risk is not misstatement but **omission**: two omissions could plausibly cause wasted owner effort or stalled action. Recommendation: ACCEPT with targeted mitigations (2 Major, 2 Minor) — no Critical findings; text does not misdirect, but it under-specifies enough to fail in the scenario above.

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| S-004-01 | Omits that the ruling is blocked on the BUG-001 (REM-01) hop-model redesign | Process | Medium | Major | P1 | Completeness |
| S-004-02 | No file/section pointer to where the contradiction actually lives | Technical | Medium | Major | P1 | Actionability |
| S-004-03 | Three assignees, no named "owner" despite text requiring owner-only authority | Process | Medium | Major | P1 | Actionability |
| S-004-04 | "Fail-closed default" urged without stating what today's default is | Assumption | Low | Minor | P2 | Evidence Quality |
| S-004-05 | Internal tracking codes (`REM-05`) unglossed in the Tracking line | Assumption | Low | Minor | P2 | Completeness |

## Finding Details

### S-004-01: Missing BUG-001 blocking dependency [MAJOR]

**Failure Cause:** The register states the H-36 ruling itself "depends on the hop-model redesign in REM-01" (BUG-001, issue #350) — the delegation-topology decision that defines what counts as a hop. The issue text presents the eng-team precedent as sufficient to "resolve this issue outright" with no caveat that the ruling may need to be revisited once BUG-001's topology is chosen.
**Category:** Process
**Likelihood:** Medium — an owner working issue-by-issue, without cross-referencing #350, would plausibly rule now.
**Severity:** Major — consequence is wasted decision-making and a reopened issue, not a wrong immediate action.
**Evidence:** `remediation-register.md` REM-05: "the ruling itself depends on the hop-model redesign in REM-01"; BUG-005 entity: "which itself depends on the REM-01 hop-model redesign."
**Dimension:** Completeness
**Mitigation:** Add one clause: "Note: this ruling may need to be revisited once issue #350 (delegation topology) is decided — resolve together where possible."
**Acceptance Criteria:** Issue text names the #350 dependency explicitly.

### S-004-02: No pointer to the contradicting text [MAJOR]

**Failure Cause:** The issue says "the skill's rule file contains" the deadline and "the file's two fallback instructions contradict each other" but never names the file. Verified in the PR worktree: both instructions are in `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` (rule NS-H-08, and the separate "3-Hop vs. 4-Hop Mode Selection > Governance Deadline" subsection) — a human or agent acting on the issue alone must search the repo to find them.
**Category:** Technical
**Likelihood:** Medium — most readers will need the exact location to verify or edit.
**Severity:** Major — forces a repo-wide search before any action is possible.
**Evidence:** Confirmed by direct read of `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` lines ~37 (NS-H-08) and ~284-286 (Governance Deadline) on the PR branch.
**Dimension:** Actionability
**Mitigation:** Add: "See `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`, rule NS-H-08 and the adjacent 'Governance Deadline' subsection."
**Acceptance Criteria:** Issue text contains a resolvable file path to the contradiction.

### S-004-03: No named owner among three assignees [MAJOR]

**Failure Cause:** The issue is assigned to three people and states the decision "requires owner authority, not maintainer or contributor alone" — but never states which assignee is the owner. An external contributor or agent reading the issue cannot determine who must act, risking each assignee assuming another will rule.
**Category:** Process
**Likelihood:** Medium — diffusion-of-responsibility is a common failure mode with multi-assignee issues carrying a single-person authority requirement.
**Severity:** Major — directly blocks the one action this issue exists to trigger.
**Evidence:** Issue assignee line lists three usernames with no role annotation; body text distinguishes "owner" from "maintainer or contributor" without mapping names to roles.
**Dimension:** Actionability
**Mitigation:** Add a role annotation, e.g., "@geekatron (repo owner) — your ruling is required here; others are tagged for context."
**Acceptance Criteria:** Issue text or assignee metadata unambiguously identifies the person with owner authority.

### S-004-04: Fail-closed recommendation lacks contrast [MINOR]

**Failure Cause:** "Whatever the ruling: encode it once, with one fallback behavior, one anchor date, and a fail-closed default" is sound advice but doesn't state that today's shipped default is fail-open (silently drops to 3-hop and eliminates sop-verifier), so a reader can't see why fail-closed matters here.
**Category:** Assumption
**Likelihood:** Low — the earlier sentence about contradicting fallbacks gives partial context.
**Severity:** Minor.
**Evidence:** `remediation-register.md` REM-05 G3: "the default is fail-open... inverting the skill's own conservative-decision principle."
**Dimension:** Evidence Quality
**Mitigation:** Append: "(today's shipped default silently reverts to 3-hop and removes the verifier — the opposite of fail-closed)."
**Acceptance Criteria:** One clause states the current default's actual behavior.

### S-004-05: Unglossed internal ID in Tracking line [MINOR]

**Failure Cause:** "Worktracker: ... (register section REM-05)" uses an internal cluster ID with no explanation of what it is or that the reader can safely ignore it.
**Category:** Assumption
**Likelihood:** Low — placed in a clearly metadata/footer line, low risk of misdirection.
**Severity:** Minor.
**Evidence:** Tracking line, issue-354.md.
**Dimension:** Completeness
**Mitigation:** Add "(internal cross-reference, no action needed)" after the REM-05 citation.
**Acceptance Criteria:** Reader can tell REM-05/PROJ-032/BUG-005 IDs are provenance, not required reading.

## Recommendations

**P1 (Major, should mitigate before/at posting):** S-004-01 (name the #350 dependency), S-004-02 (add file/rule pointer), S-004-03 (name the owner).
**P2 (Minor, polish):** S-004-04 (state today's default), S-004-05 (gloss REM-05).

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | S-004-01, S-004-05: missing dependency and unglossed ID |
| Internal Consistency | 0.20 | Neutral | No contradictions found in the text itself |
| Methodological Rigor | 0.20 | Neutral | N/A — text artifact, not a methodology |
| Evidence Quality | 0.15 | Negative | S-004-04: recommendation lacks contrastive evidence |
| Actionability | 0.15 | Negative | S-004-02, S-004-03: missing pointer and owner identity block action |
| Traceability | 0.10 | Positive | All factual claims independently verified against register, BUG-005 entity, verdict, and live rule file |

**Overall assessment:** No fabricated or misleading claims found (0 Critical). 3 Major omissions reduce actionability for a zero-context external reader/agent; targeted 1-2 sentence additions close all of them without materially increasing length.
