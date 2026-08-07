# Red Team Report: GitHub Issue #354 (BUG-005 / REM-05, H-36 governance ruling)

**Strategy:** S-001 Red Team Analysis (adapted, compact, ~300-word communication artifact)
**Deliverable:** `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-006-issue-quality/snapshots/final/issue-354.md`
**Criticality:** C4 (tournament)
**H-16 Note:** No S-003 output supplied to this executor; per adv-executor Step 0 this run is scoped to S-001 only (orchestrator-managed sequencing) and does not itself certify H-16 compliance for the tournament as a whole.
**Threat Actor:** An external contributor's autonomous coding agent that parses this issue text literally, with zero access to internal governance docs, and acts on it (files edits, decides who has authority, decides whether to self-implement the "resolution").

## Summary

The issue is largely accurate against ground truth (deadline date, contradiction, missing tracking item, eng-team precedent, worktracker path, and severity all check out). The attack surface is in what the text implies but does not pin down: it labels the counted units "agent-to-agent handoffs" when the underlying rule actually counts main-context-to-agent invocations (the real point of dispute), it presents a permissive-sounding resolution path next to a governance decision reserved for "owner" without saying who that is or blocking an agent from self-implementing it, and it says "the file's" contradiction when the fix actually spans three files. Recommendation: REVISE (targeted) — no fabrications found, but three Major/Critical gaps could misdirect an acting agent.

## Findings Table

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| S-001-01 | Critical | "agent-to-agent handoffs" mischaracterizes what H-36 counts (main-context re-invocations), obscuring the actual dispute | Para 1 |
| S-001-02 | Critical | No guard against an agent self-implementing the "resolves this issue outright" reading without owner sign-off | Para 2 |
| S-001-03 | Major | "the skill's rule file" (singular) undercounts — fix spans three files | Para 1 / Tracking |
| S-001-04 | Major | "owner" vs "maintainer or contributor" left undefined; no named authority | Para 2 / Tracking |
| S-001-05 | Major | "eng-team skill" precedent cited with no locator | Para 2 |
| S-001-06 | Minor | "candidate designs" overstates REM-05's content (binary choice, not multiple architectures) | Tracking |

## Finding Details

### S-001-01: "agent-to-agent handoffs" mischaracterizes the counted unit [CRITICAL]

**Attack Vector:** An agent reads "internal four-agent sequence violates ... three agent-to-agent handoffs" and infers the fix is about direct agent→agent messaging (e.g., have sop-verifier hand off to sop-capture directly). Ground truth (`nuclear-sop-behavior-rules.md` "4-Hop Sequence") shows all four invocations originate from *main context* (`Main context -> sop-brief`, `Main context -> sop-executor`, `Main context -> sop-verifier`, `Main context -> sop-capture`) — there is no agent-to-agent handoff at all; that absence is exactly why the hop-counting question is disputed.
**Evidence:** Issue para 1: "violates the framework's routing rule limiting a request to three agent-to-agent handoffs."
**Consequence:** An agent could "resolve" this by restructuring delegation topology (which would itself violate P-003/H-01 single-level nesting) instead of correctly recognizing this is a hop-counting/governance question.
**Countermeasure:** Replace with "three routing hops (re-invocations from the framework's coordinating context)" — matches how the rule actually counts, without naming H-36.

### S-001-02: No guard against self-implementing an owner-reserved decision [CRITICAL]

**Attack Vector:** Para 2 states "adopting that reading ... resolves this issue outright and removes the skill's self-scheduled sunset clause" immediately before "Whatever the ruling: encode it once..." A literal-reading agent optimizing for "resolve the issue" could treat the precedent as pre-approved and ship the edit itself, without the explicit owner ruling the same paragraph says is required ("The decision to make (owner)").
**Evidence:** Para 2, full text.
**Consequence:** A governance decision reserved for the repository owner gets made unilaterally by a contributor's agent — the exact failure mode PROJ-032's verdict was written to prevent (verdict: "this is the one blocker that is not purely contributor work").
**Countermeasure:** Add one sentence: "Do not implement this reading yourself — wait for an explicit owner comment on this issue approving it before editing the rule file(s)."

### S-001-03: File count understated [MAJOR]

**Attack Vector:** "the skill's rule file contains ... two fallback instructions [that] contradict each other" implies a single-file fix. Ground truth (`remediation-register.md` REM-05, "Affected files") lists three: `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`, `skills/nuclear-sop/SKILL.md`, `skills/nuclear-sop/PLAYBOOK.md` — SKILL.md and PLAYBOOK.md carry a duplicate, textually-different copy of the same deadline/fallback language.
**Consequence:** An agent that patches only `nuclear-sop-behavior-rules.md` leaves the contradiction live in the other two files, satisfying the letter of the issue while missing its substance.
**Countermeasure:** "the skill's rule file" -> "three files: `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`, `SKILL.md`, and `PLAYBOOK.md` (all three currently restate the deadline/fallback differently)."

### S-001-04: "Owner" undefined [MAJOR]

**Attack Vector:** "requires owner authority, not maintainer or contributor alone" never says who the owner is. Assignees list three usernames with no roles attached, so a reader cannot map "owner" to a person or account.
**Consequence:** An agent may address the ruling request to the wrong assignee, or (worse, combined with S-001-02) conclude no distinct owner exists and act itself.
**Countermeasure:** Name the owner explicitly, e.g., "requires a ruling from the repository owner (@geekatron) — a maintainer applying fixes or the contributor proposing designs cannot issue this ruling."

### S-001-05: Uncited precedent [MAJOR]

**Attack Vector:** "the existing eng-team skill runs a predetermined 8-step sequence across 10 worker agents with no hop-ceiling machinery" is offered as the deciding precedent but has no path, forcing a repo-wide search to verify or apply it.
**Countermeasure:** Add `(see skills/eng-team/SKILL.md)`.

### S-001-06: "Candidate designs" oversells REM-05 [MINOR]

**Attack Vector:** "Full analysis with candidate designs: remediation-register.md" — REM-05's redesign question is a binary choice (keep 4-hop vs. revert to 3-hop), not multiple named architectures like sibling clusters (e.g., REM-07's allowlist/category-gating/engine-delegation options). A reader expecting a menu of designs finds a yes/no framing instead.
**Countermeasure:** "Full analysis: remediation-register.md, section REM-05" (drop "with candidate designs" or replace with "with the binary framing").

## Recommendations

- **P0:** S-001-01, S-001-02 — both risk sending an acting agent down a wrong or unauthorized path; fix before posting.
- **P1:** S-001-03, S-001-04, S-001-05 — close actionability/lookup gaps.
- **P2:** S-001-06 — wording precision only.

## Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Evidence Quality | Negative | S-001-01 mischaracterizes the technical mechanism being disputed |
| Actionability | Negative | S-001-02/04/05 force lookups or leave authority/execution ambiguous |
| Completeness | Negative | S-001-03 undercounts affected files |
| Internal Consistency | Neutral | No contradictions found within the issue text itself |
| Traceability | Positive | All checkable facts (date, path, severity, precedent) verified against ground truth |
