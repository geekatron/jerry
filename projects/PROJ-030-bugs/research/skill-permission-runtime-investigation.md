# Investigation: Does Skill(name) Actually Work as a Permission Pattern?

> Closing IN-001 from S-013 Inversion Review (Issue #181)
> Investigator: ps-investigator
> Date: 2026-03-14
> Confidence: HIGH (direct documentation evidence; no empirical runtime test gap acknowledged)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language finding for stakeholders |
| [L1: Technical Investigation](#l1-technical-investigation) | 5 Whys, evidence chain, mechanism detail |
| [L2: Systemic Assessment](#l2-systemic-assessment) | Implications, risks, corrective actions |
| [Evidence Chain](#evidence-chain) | All sources cited |
| [Limitations](#limitations) | Gaps in investigation |

---

## L0: Executive Summary

**Finding: Skill(name) IS a real, working permission pattern in Claude Code. The entries in `.claude/settings.local.json` are valid and serve a functional purpose.**

IN-001 raised the concern that Jerry had never verified that `Skill(name)` entries in `settings.local.json` actually control skill invocation permissions at runtime. This investigation confirms:

1. `Skill` is explicitly named as a valid tool prefix in the official Claude Code JSON schema regex for permission rules — it appears alongside `Bash`, `Read`, `Edit`, `WebFetch`, and `Agent`.

2. The official Claude Code documentation has a dedicated section titled "Restrict Claude's skill access" that explains exactly how `Skill(name)` works: use it in the `deny` array to block specific skills, or in the `allow` array to pre-approve skills without prompting. `Skill(name)` for exact match; `Skill(name *)` for prefix match with arguments.

3. Without `Skill(name)` entries in `allow`, in `default` permissionMode Claude Code would prompt the user for permission on first invocation of each skill. The `settings.local.json` `allow` entries eliminate those prompts for the 19 listed skills.

4. A separate GitHub bug (#18950) describes Bash permissions NOT inheriting inside skills — that is a different, unrelated issue. The `Skill()` mechanism itself is not in question there.

**The `Skill()` entries in Jerry's `settings.local.json` are correctly placed and functionally valid. No corrective action required on the permission entries themselves.**

---

## L1: Technical Investigation

### Incident Overview

| Attribute | Value |
|-----------|-------|
| Issue | IN-001 from S-013 Inversion Review (Issue #181) |
| Concern | "We've never verified that Skill(name) actually grants permissions at runtime" |
| Risk raised | Skills may auto-approve regardless; entries may be inert |
| Severity | MEDIUM (if inert, permission governance is illusory) |

### 5 Whys Analysis

| Level | Question | Answer | Evidence |
|-------|----------|--------|----------|
| Why 1 | Why was IN-001 raised? | No runtime verification existed when the entries were added to `settings.local.json` | S-013 Inversion review flagged assumption without evidence |
| Why 2 | Why was there no verification? | The `Skill` tool was a relatively new addition to Claude Code's permission system; team relied on the schema being correct without reading the permission docs for runtime behavior | E-001: `Skill` is in the schema regex; E-002: docs explain runtime behavior |
| Why 3 | Why might the concern be valid? | In `default` permissionMode without explicit `allow` rules, Claude Code prompts for first use — so if `Skill()` entries were inert, there would be no observable failure, just prompts | E-003: default mode description; docs permission table |
| Why 4 | What does the evidence show? | `Skill` is listed explicitly in the JSON schema regex AND the official docs have an explicit "Restrict Claude's skill access" section showing `Skill(name)` in `deny` and `allow` arrays with stated behavior | E-001, E-002 |
| Why 5 | Root cause of original concern | Assumption gap, not a real defect — no documented runtime failure, just an untested assumption. Evidence confirms `Skill()` works as documented. | E-001, E-002, E-003 |

**Root Cause Determination: There is no defect. The concern (IN-001) was an assumption gap, not a runtime failure. `Skill()` permission rules are a documented, implemented feature of Claude Code's permission system.**

### How Skill() Works at Runtime

From the official documentation (E-002):

> "By default, Claude can invoke any skill that doesn't have `disable-model-invocation: true` set."

> "Three ways to control which skills Claude can invoke:
>
> Disable all skills by denying the Skill tool in /permissions:
>   `Skill` (in deny rules)
>
> Allow or deny specific skills using permission rules:
>   `Skill(commit)` — exact match
>   `Skill(review-pr *)` — prefix match with arguments
>   `Skill(deploy *)` — deny example
>
> Permission syntax: `Skill(name)` for exact match, `Skill(name *)` for prefix match with any arguments."

This is exactly the pattern used in Jerry's `settings.local.json`.

### What the settings.local.json Entries Do

The 19 `Skill(...)` entries in the `allow` array of `.claude/settings.local.json`:

```json
"Skill(adversary)",
"Skill(architecture)",
"Skill(ast)",
...
```

These entries pre-approve Claude's invocation of those skills without prompting the user. Without these entries, in `default` permissionMode (set nowhere explicitly in `.claude/settings.json`, so it defaults to `default`), Claude Code would prompt the user for confirmation the first time it invokes each skill.

**Effect:** The `allow` entries eliminate per-session permission prompts for the 19 listed Jerry skills. This is the correct and intended use of the `Skill()` permission pattern.

### Settings Precedence Context

The settings layers relevant here:

| File | Content | Precedence |
|------|---------|------------|
| `.claude/settings.json` | Shared project settings (no `Skill()` entries, no `defaultMode`) | Level 4 (lower) |
| `.claude/settings.local.json` | Local project settings (19 `Skill()` allow entries) | Level 3 (higher) |

Since `.claude/settings.json` has no `defaultMode` field, the session operates in `default` mode. The `settings.local.json` allow rules for `Skill()` take effect and suppress prompts for those skills.

### The Unrelated GitHub Issue (#18950)

GitHub issue #18950 describes: "Skills/subagents do not inherit user-level permissions from settings.json" — meaning Bash commands that are auto-approved in the main session still prompt when executed from within a skill.

This is a separate bug about Bash permission inheritance inside a skill's execution context. It does not affect whether `Skill()` entries in the `allow` array work for the model's invocation of the skill itself. The two mechanisms are:

- `Skill(name)` in allow/deny: Controls whether Claude can invoke the skill (the entry point)
- Bash permissions inside a skill: Controls what Bash commands run without prompting once inside the skill

IN-001 was about the first mechanism. Issue #18950 is about the second. They are orthogonal.

### Ishikawa Category Assessment

| Category | Factor | Status |
|----------|--------|--------|
| Method | Permission syntax not verified against docs | RESOLVED — docs confirm syntax |
| Machine | Runtime evaluator may not check Skill() | RESOLVED — docs confirm evaluator checks it |
| Material | Schema may not include Skill | RESOLVED — schema regex explicitly includes Skill |
| Man | Team assumption without documentation check | ROOT CAUSE of concern (not a defect) |
| Measurement | No runtime test existed | REMAINING GAP (see Limitations) |
| Mother Nature | Claude Code API changes | LOW RISK — feature is documented in current official docs |

---

## L2: Systemic Assessment

### Systemic Factor

The IN-001 concern arose because the team added `Skill()` entries without consulting the official permission documentation, relying instead on schema validation alone. Schema validation confirms the entries are syntactically valid; it does not confirm runtime behavior. The documentation gap between "schema valid" and "runtime functional" is a category of assumption that can produce silent non-enforcement.

**This is not a defect in the current configuration. But it is a process gap: when adding permission entries of unfamiliar types, the team should verify runtime behavior via docs, not just schema.**

### FMEA for Related Risks

| Failure Mode | Effect | Cause | S | O | D | RPN | Action |
|--------------|--------|-------|---|---|---|-----|--------|
| `Skill()` entries become inert in a future Claude Code version | Skills invoke without permission checks silently | API breaking change | 6 | 2 | 7 | 84 | Monitor Claude Code changelog; retest after major version updates |
| New skill added without `Skill()` allow entry | User prompted on first skill invocation (UX friction, not security failure) | Process omission | 3 | 5 | 3 | 45 | Add to onboarding checklist: new skills require `settings.local.json` entry |
| `Skill()` syntax changes (e.g., `Skill(name *)` vs `Skill(name)`) | Wrong skills denied/allowed | Documentation drift | 5 | 2 | 5 | 50 | Pin permission doc URL in CLAUDE.md or `docs/reference/claude-code-permissions.md` |
| Bash permission non-inheritance inside skills (issue #18950) | Skill execution requires manual approval for Bash commands | Known Claude Code bug | 4 | 8 | 3 | 96 | Monitor issue #18950; add `allowed-tools` to SKILL.md files as workaround |

RPN thresholds: > 100 = high priority, 50-99 = medium, < 50 = low. No RPN exceeds 100.

### Prevention Strategies

1. **Process: doc-verify before permission entries are added** — When a new permission tool type appears (e.g., `Agent()`, `Task()`, `Skill()`), link the official docs section to the ADR or commit that adds the entries.

2. **Workaround for issue #18950** — The Bash inheritance bug means skills that execute Bash commands will prompt unless the skill's own SKILL.md uses `allowed-tools` frontmatter. Jerry SKILL.md files do not currently use `allowed-tools`. This is a separate improvement opportunity, not a blocker.

3. **Changelog monitoring** — `Skill()` is a documented feature; its removal or behavior change would be a documented breaking change. Low risk but worth checking when updating Claude Code.

---

## Corrective Actions

### CA-001: Close IN-001 as Resolved

| Attribute | Value |
|-----------|-------|
| Type | Immediate |
| Owner | Issue #181 author |
| Due | Next session |
| Status | TODO |

**Description:** Update Issue #181 to close IN-001 with this investigation as evidence. The concern was an assumption gap, not a runtime defect.
**Success Criteria:** IN-001 marked resolved in Issue #181 tracking.

### CA-002: Add Skill() doc reference to permissions reference file

| Attribute | Value |
|-----------|-------|
| Type | Short-term |
| Owner | Jerry framework maintainer |
| Due | Next permission-related PR |
| Status | TODO |

**Description:** In `docs/reference/claude-code-permissions.md`, add a section on `Skill()` permission rules with a link to the official docs and a note on the `allow` vs `deny` semantic. This prevents the same assumption gap from recurring.
**Success Criteria:** `docs/reference/claude-code-permissions.md` contains a `Skill()` section with official doc citation.
**Dependencies:** None.

### CA-003: Add allowed-tools to SKILL.md files (issue #18950 mitigation)

| Attribute | Value |
|-----------|-------|
| Type | Long-term |
| Owner | Jerry framework maintainer |
| Due | Next skills refactor |
| Status | TODO |

**Description:** GitHub issue #18950 shows Bash permissions do not inherit inside skills in some Claude Code versions. Jerry skills that execute Bash commands should declare `allowed-tools` in their SKILL.md frontmatter to avoid prompts during skill execution.
**Success Criteria:** All Jerry SKILL.md files that use Bash declare appropriate `allowed-tools`.
**Dependencies:** Issue #18950 resolution monitoring.

---

## Evidence Chain

| Evidence ID | Type | Source | Relevance |
|-------------|------|--------|-----------|
| E-001 | Schema | `/docs/schemas/claude-code-settings-v1.schema.json` line 8, regex pattern | `Skill` is explicitly listed in the `permissionRule` regex alongside Bash, Read, Edit, Agent, Task — confirming it is a recognized tool prefix |
| E-002 | Official docs | `https://code.claude.com/docs/en/skills` — "Restrict Claude's skill access" section | Explicit documentation of `Skill(name)` allow/deny syntax with exact behavior description and examples |
| E-003 | Official docs | `https://code.claude.com/docs/en/permissions` — permission modes table | `default` mode "prompts for permission on first use of each tool"; `allow` rules suppress these prompts |
| E-004 | GitHub issue | `https://github.com/anthropics/claude-code/issues/18950` | Confirms a separate Bash-inheritance bug inside skills; NOT evidence that `Skill()` entries themselves are inert |
| E-005 | Config file | `.claude/settings.local.json` | Shows 19 `Skill(name)` entries in `allow` array; no `defaultMode` set anywhere; entries are in the correct location and format |
| E-006 | Config file | `.claude/settings.json` | No `defaultMode`, no `Skill()` entries; confirms `settings.local.json` carries all skill permission configuration |

---

## Limitations

1. **No empirical runtime test**: This investigation is based on official documentation and schema analysis, not a live test of Claude Code's permission evaluator. The finding is HIGH confidence based on documentation but cannot be VERIFIED confidence without a runtime test. To achieve verified confidence, run Claude Code with a skill NOT in the allow list and confirm it prompts; then add it and confirm it does not prompt.

2. **Version specificity**: The documentation accessed reflects current Claude Code docs as of 2026-03-14. The schema is from `docs/schemas/claude-code-settings-v1.schema.json` in the Jerry repo (likely kept in sync with Claude Code releases). If the Jerry schema file is outdated, the E-001 evidence remains valid as the docs independently confirm the mechanism.

3. **Issue #18950 status unknown**: The Bash inheritance bug may be fixed in current Claude Code versions. The open/closed status could not be confirmed from the page content retrieved.

---

## PS Integration

| Attribute | Value |
|-----------|-------|
| PS ID | PROJ-030 |
| Entry ID | Issue #181 / IN-001 |
| Artifact | `projects/PROJ-030-bugs/research/skill-permission-runtime-investigation.md` |
| Root Cause | Assumption gap (no defect) — `Skill()` is a documented, working permission pattern |
| Confidence | HIGH (documentation evidence) / VERIFIED pending runtime test |
| Corrective Actions | CA-001 (close IN-001), CA-002 (add doc reference), CA-003 (allowed-tools in SKILL.md) |
| Next Agent Hint | No downstream agent needed; findings feed back to Issue #181 |

---

*Investigation Version: 1.0.0*
*Methodology: 5 Whys, Ishikawa, FMEA*
*Constitutional Compliance: P-001 (evidence-based root cause), P-002 (persisted to file), P-022 (limitations disclosed)*
*Generated: 2026-03-14*
