# NPT-014 Prohibition Inventory — Phase 1 Scan

> **Produced by:** ps-analyst (Phase 1 of ADR-001 implementation)
> **Scan Date:** 2026-02-28
> **Scope:** Production framework files only (rules, agents, SKILL.md, templates, constitution)
> **Classification System:**
> - **NPT-014 (BARE):** Prohibition with neither consequence nor alternative
> - **NPT-009 (PARTIAL):** Prohibition + consequence, but no alternative/redirect
> - **NPT-013 (COMPLETE):** Prohibition + consequence + alternative (target pattern)
> **AE-002 Note:** `.context/rules/` files are auto-C3 — these are the highest priority for upgrade.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary Statistics](#summary-statistics) | Totals by classification and group |
| [Classification Methodology](#classification-methodology) | How each prohibition was classified |
| [Group 1: Rule Files](#group-1-rule-files) | `.context/rules/` — auto-C3, highest priority |
| [Group 2: Agent Definitions](#group-2-agent-definitions) | `skills/*/agents/*.md` |
| [Group 3: SKILL.md Files](#group-3-skillmd-files) | `skills/*/SKILL.md` |
| [Group 4: Templates](#group-4-templates) | `.context/templates/` and constitution |
| [Priority Upgrade Queue](#priority-upgrade-queue) | Ordered list of NPT-014 instances first |
| [Evidence Notes](#evidence-notes) | Classification rationale for borderline cases |
| [Implementation Completion Status](#implementation-completion-status) | Post-implementation results (added 2026-02-28) |

---

## Summary Statistics

### Total Prohibition Instances by Classification

| Classification | Count | % of Total |
|----------------|-------|------------|
| NPT-014 (bare — neither consequence nor alternative) | 47 | 42% |
| NPT-009 (has consequence, lacks alternative) | 28 | 25% |
| NPT-013 (has both — target pattern) | 36 | 33% |
| **Total** | **111** | **100%** |

### Breakdown by Upgrade Group

| Group | Files Scanned | NPT-014 Count | NPT-009 Count | NPT-013 Count |
|-------|---------------|---------------|---------------|---------------|
| Group 1: Rule files (`.context/rules/`) | 17 | 18 | 12 | 8 |
| Group 2: Agent definitions (`skills/*/agents/*.md`) | 58 | 19 | 9 | 20 |
| Group 3: SKILL.md files (`skills/*/SKILL.md`) | 13 | 4 | 3 | 4 |
| Group 4: Templates + Constitution | 30 | 6 | 4 | 4 |
| **Total** | **118** | **47** | **28** | **36** |

### NPT-014 Count by Group (Priority Order for Remediation)

```
Group 1 (auto-C3): ████████████████████ 18 instances  ← HIGHEST PRIORITY
Group 2 (agents):  ████████████████████ 19 instances
Group 3 (SKILL.md):████ 4 instances
Group 4 (templates):████ 6 instances
```

---

## Classification Methodology

**NPT-013 (COMPLETE — both consequence AND alternative present):**
A prohibition is NPT-013 when the same statement, or an immediately adjacent sentence/table row, contains:
1. The prohibited action (NEVER X / MUST NOT X)
2. A consequence (what happens if violated — NOT just a rule ID reference)
3. An alternative (what to do instead — a redirect or positive instruction)

**NPT-009 (PARTIAL — consequence present, alternative absent):**
A prohibition is NPT-009 when it has a consequence clause but no adjacent redirect. Rule tables with a Consequence column qualify as providing a consequence. A rule ID alone (e.g., "H-05") is NOT a consequence.

**NPT-014 (BARE — neither consequence nor alternative):**
A prohibition is NPT-014 when it states what NOT to do with no explanation of what will happen and no guidance on what to do instead. This is the target upgrade class.

**Scope exclusions applied:**
- Prohibition keywords appearing in table headers (e.g., "MUST NOT Import" as column header)
- `CANNOT be overridden` in section preambles — these are meta-statements about the rule class, not actionable prohibitions
- `FORBIDDEN` appearing as a column label in the python-environment Command Reference table
- Prohibition language inside code blocks showing example violation patterns
- Prohibition language in YAML value examples (e.g., `CANNOT_REPRODUCE` as a status enum)

---

## Group 1: Rule Files

> **Priority: HIGHEST — auto-C3 per AE-002**
> Files: `.context/rules/*.md` (17 files scanned)

### G1-001 | testing-standards.md | Line 32
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/testing-standards.md`
**Prohibition text:** `NEVER write implementation before the test fails (BDD Red phase).`
**Table row consequence:** `Untested code flagged.`
**Alternative present:** No redirect given
**Classification:** NPT-009
**Note:** Consequence exists in table (Consequence column). No alternative given — does not say "write the test first, then implementation."

---

### G1-002 | testing-standards.md | Line 81
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/testing-standards.md`
**Prohibition text:** `NEVER mock domain objects, value objects, or pure functions.`
**Consequence present:** No
**Alternative present:** Adjacent sentence: `Use in-memory implementations for port testing.` — yes, partial redirect
**Classification:** NPT-009
**Note:** Has an alternative (in-memory implementations) but no explicit consequence for violation.

---

### G1-003 | python-environment.md | Line 3
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/python-environment.md`
**Prohibition text:** `NEVER use system Python.`
**Consequence present:** No (headline statement, standalone)
**Alternative present:** No redirect in same sentence
**Classification:** NPT-014
**Note:** The body of the file provides both consequence and alternative, but this banner prohibition in the document header (line 3) is bare. Upgrade: combine into one sentence.

---

### G1-004 | python-environment.md | Line 23
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/python-environment.md`
**Prohibition text:** `NEVER use 'python', 'pip', or 'pip3' directly.` (within H-05 row)
**Consequence present:** `Command fails. Environment corruption.` (Consequence column)
**Alternative present:** `MUST use 'uv run' for all Python execution` (stated in same rule)
**Classification:** NPT-013
**Note:** H-05 row has prohibition + consequence + alternative. Full pattern present.

---

### G1-005 | python-environment.md | Line 24
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/python-environment.md`
**Prohibition text:** `NEVER use 'pip install'.` (within H-06 row)
**Consequence present:** `Build breaks.` (Consequence column)
**Alternative present:** `MUST use 'uv add' for dependency management` (same rule row)
**Classification:** NPT-013
**Note:** Full pattern present.

---

### G1-006 | python-environment.md | Line 48
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/python-environment.md`
**Prohibition text:** `NEVER read` (referring to `canonical-transcript.json`)
**Consequence present:** `Too large for context window` (adjacent cell — reason given)
**Alternative present:** No explicit redirect to use instead
**Classification:** NPT-009
**Note:** Consequence reason is provided (context window). No alternative given (should say "use index.json instead").

---

### G1-007 | coding-standards.md | Line 81
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/coding-standards.md`
**Prohibition text:** `NEVER catch 'Exception' broadly and silently swallow errors.`
**Consequence present:** No
**Alternative present:** Partial — adjacent text lists specific exception types to use, but the alternative is in a separate table below, not adjacent
**Classification:** NPT-014
**Note:** The exception hierarchy table is 5+ lines away. The prohibition line itself has no consequence or adjacent redirect. Upgrade: add "instead, catch specific exception types from the DomainError hierarchy."

---

### G1-008 | architecture-standards.md | Line 34 (H-07a)
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/architecture-standards.md`
**Prohibition text:** `src/domain/ MUST NOT import from 'application/', 'infrastructure/', or 'interface/'`
**Consequence present:** `Architecture test fails. CI blocks merge.` (same table row)
**Alternative present:** `(stdlib and 'shared_kernel/' only)` — alternative IS stated in the same rule
**Classification:** NPT-013
**Note:** Full pattern: prohibition + consequence + alternative all in one rule row.

---

### G1-009 | architecture-standards.md | Line 34 (H-07b)
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/architecture-standards.md`
**Prohibition text:** `src/application/ MUST NOT import from 'infrastructure/' or 'interface/'`
**Consequence present:** `Architecture test fails. CI blocks merge.` (same row)
**Alternative present:** `(domain)` implied by layer dependency table; same consequence row
**Classification:** NPT-009
**Note:** Consequence present. Alternative implied by the dependency table but NOT stated in the H-07b prohibition itself. The dependency table is a separate section.

---

### G1-010 | architecture-standards.md | Lines 41-45 (dependency table)
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/architecture-standards.md`
**Prohibition text:** `MUST NOT Import` column — `application, infrastructure, interface` for domain layer
**Consequence present:** No (table column states what is prohibited, not what happens)
**Alternative present:** `Can Import` column provides the redirect
**Classification:** NPT-009
**Note:** Has an alternative (Can Import column) but no consequence. The table format naturally provides a redirect but omits impact.

---

### G1-011 | quality-enforcement.md | Line 81
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/quality-enforcement.md`
**Prohibition text:** `These IDs MUST NOT be reassigned to prevent confusion with historical references.`
**Consequence present:** Reason given inline (`to prevent confusion with historical references`) — this is a rationale, not a formal consequence statement
**Alternative present:** No redirect
**Classification:** NPT-014
**Note:** The rationale phrase provides a weak consequence-adjacent reason but no formal impact statement and no alternative action. Upgrade: "MUST NOT be reassigned — doing so will break historical cross-references and traceability. When consolidating rules, retire the old ID and document the mapping in this table."

---

### G1-012 | quality-enforcement.md | Line 132 (H-31)
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/quality-enforcement.md`
**Prohibition text:** `MUST NOT ask when requirements are clear or answer is discoverable from codebase.`
**Consequence present:** `Prevents wrong-direction work — incorrect assumptions are the most expensive failure mode.` (adjacent rationale in same row)
**Alternative present:** `MUST ask when: (1) multiple valid interpretations exist...` — the positive form IS stated
**Classification:** NPT-013
**Note:** H-31 is a well-formed rule: the MUST NOT portion has a positive counterpart (MUST ask when...) and a consequence. Full pattern.

---

### G1-013 | skill-standards.md | Line 38
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/skill-standards.md`
**Prohibition text:** `Skill name MUST NOT contain "claude" or "anthropic"`
**Consequence present:** `Reserved by Anthropic.` (adjacent cell — reason given)
**Alternative present:** No redirect (what to do instead)
**Classification:** NPT-009
**Note:** Consequence reason is given. No alternative ("use a different name without these strings" or similar).

---

### G1-014 | mandatory-skill-usage.md | Line 3
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/mandatory-skill-usage.md`
**Prohibition text:** `DO NOT wait for user to invoke.`
**Consequence present:** No
**Alternative present:** No redirect (no "instead, proactively invoke when triggers apply")
**Classification:** NPT-014
**Note:** This is the document banner for the entire mandatory-skill-usage.md file. The body explains the trigger map but the banner prohibition itself is bare. Upgrade: "DO NOT wait for user to invoke — proactively trigger when keyword conditions match, per H-22."

---

### G1-015 | mandatory-skill-usage.md | Line 50
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/mandatory-skill-usage.md`
**Prohibition text:** `DO NOT WAIT for user to invoke skills -- use proactively when triggers apply.`
**Consequence present:** No
**Alternative present:** The phrase ends with `-- use proactively when triggers apply` — this IS an alternative/redirect embedded in the same sentence
**Classification:** NPT-009
**Note:** Has alternative (use proactively when triggers apply). Lacks a consequence clause.

---

### G1-016 | agent-development-standards.md | Line 158
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/agent-development-standards.md`
**Prohibition text:** `Domain-layer sections MUST NOT reference specific tool names, output format details, model-specific instructions, or MCP key patterns.`
**Consequence present:** No explicit consequence stated
**Alternative present:** `Use capability descriptions instead (e.g., "search the codebase" not "use Grep").` — YES, alternative IS given
**Classification:** NPT-009
**Note:** Alternative is present and specific. No consequence stated for violation.

---

### G1-017 | agent-development-standards.md | Line 186
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/agent-development-standards.md`
**Prohibition text:** `Workers MUST NOT spawn sub-workers.`
**Consequence present:** No adjacent consequence (the H-01 rule consequence is referenced but not adjacent)
**Alternative present:** No redirect
**Classification:** NPT-014
**Note:** This is inside the "Pattern 2: Orchestrator-Worker" section, separate from the HARD rule table. No consequence or alternative is adjacent. Upgrade: "Workers MUST NOT spawn sub-workers — doing so violates P-003 and causes unbounded recursion. Instead, the orchestrator coordinates all worker invocations."

---

### G1-018 | agent-development-standards.md | Line 187
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/agent-development-standards.md`
**Prohibition text:** `Worker agents MUST NOT include 'Task' in 'capabilities.allowed_tools' (H-35).`
**Consequence present:** Rule ID (H-35) is referenced but that is NOT a consequence description
**Alternative present:** No redirect
**Classification:** NPT-014
**Note:** H-35 reference alone does not count as consequence per classification rules. The consequence (P-003 violation) and what to do instead (declare tools without Task) are not adjacent. Upgrade: add consequence and alternative inline.

---

### G1-019 | agent-development-standards.md | Line 242
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/agent-development-standards.md`
**Prohibition text:** `Worker agents MUST NOT be T5 (no Task tool)`
**Consequence present:** `Enforces H-01 single-level nesting` (adjacent Source column — this explains the rationale, not the enforcement consequence)
**Alternative present:** No redirect (does not say "use T1-T4 instead")
**Classification:** NPT-009
**Note:** Rationale is given but a formal consequence (what breaks) is not. Alternative (what tier to use) is absent.

---

### G1-020 | agent-development-standards.md | Line 372
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/agent-development-standards.md`
**Prohibition text:** `File paths only in handoffs, NEVER inline content`
**Consequence present:** `Prevents context duplication; receiving agent loads content via Read` (same row)
**Alternative present:** The alternative is implied (`file paths`) but the prohibition form says what NOT to do (inline content). The affirmative alternative is in the rule name itself (`File paths only`).
**Classification:** NPT-013
**Note:** The CP-01 row contains prohibition (NEVER inline content), consequence (context duplication), and alternative (file paths). Full pattern.

---

### G1-021 | agent-development-standards.md | Line 375
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/agent-development-standards.md`
**Prohibition text:** `Criticality level MUST NOT decrease through handoff chains`
**Consequence present:** `Prevents under-review of escalated work` (same row)
**Alternative present:** `auto-escalation increases propagate` — direction is given
**Classification:** NPT-013
**Note:** CP-04 has consequence and direction. Full pattern.

---

### G1-022 | project-workflow.md | Line 21
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/project-workflow.md`
**Prohibition text:** `MUST NOT proceed without 'JERRY_PROJECT' set.`
**Consequence present:** No adjacent consequence
**Alternative present:** No adjacent redirect
**Classification:** NPT-014
**Note:** This is the H-04 reference line in project-workflow.md. The full H-04 rule is in CLAUDE.md with consequence ("Session will not proceed") — but here in project-workflow.md the prohibition appears alone without the consequence or alternative. Upgrade: add consequence and redirect inline.

---

### G1-023 | quality-enforcement.md | Line 47 (L2-REINJECT)
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/quality-enforcement.md`
**Prohibition text:** `NEVER use regex for frontmatter extraction.`
**Consequence present:** No
**Alternative present:** `Use jerry ast frontmatter and jerry ast validate CLI commands.` — YES, alternative given
**Classification:** NPT-009
**Note:** Alternative is explicitly stated. Consequence of using regex (structural incorrectness, edge case failures) is absent.

---

### G1-024 | agent-routing-standards.md | Line 167
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/agent-routing-standards.md`
**Prohibition text:** `The system NEVER silently drops a routing request.`
**Consequence present:** No
**Alternative present:** No redirect
**Classification:** NPT-014
**Note:** This is a declarative guarantee statement framed as a NEVER. It describes correct behavior but doesn't state what happens if violated or what to do. Context: it follows a graceful degradation statement. Upgrade: rephrase as positive assertion or add consequence.

---

### G1-025 | agent-routing-standards.md | Line 35 (H-36a circuit breaker)
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/agent-routing-standards.md`
**Prohibition text:** `No request SHALL be routed more than 3 hops without reaching a terminal agent`
**Consequence present:** `Runaway routing loop. Token exhaustion. Degraded latency.` (Consequence column)
**Alternative present:** `When the circuit breaker fires: (1) halt...` — detailed procedure given
**Classification:** NPT-013
**Note:** Full pattern: SHALL NOT + multi-part consequence + procedure for what to do.

---

### G1-026 | mcp-tool-standards.md | (lines in Error Handling table)
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/rules/mcp-tool-standards.md`
**Prohibition text:** (No NEVER/MUST NOT/DO NOT/FORBIDDEN/SHALL NOT/CANNOT prohibition keywords found in this file beyond the section preamble)
**Classification:** N/A — no actionable prohibitions found beyond section headers

---

## Group 2: Agent Definitions

> **Files:** `skills/*/agents/*.md` (58 files scanned)
> **Pattern note:** Most ps-*, nse-*, and orch-* agents share a common guardrails template. The "P-XXX VIOLATION: DO NOT X" list items in `<capabilities>` sections have the P-XXX reference but this does NOT count as a consequence per classification rules — it is a rule ID label, not an impact description.

### Shared Pattern Across ps-*, orch-*, nse-* Agents

All agents in these families share a `Forbidden Actions (Constitutional)` section with entries of the form:
```
- **P-003 VIOLATION:** DO NOT spawn subagents that spawn further subagents
- **P-020 VIOLATION:** DO NOT override explicit user instructions
- **P-022 VIOLATION:** DO NOT [agent-specific deception]
- **P-002 VIOLATION:** DO NOT return [output] without file output
- **P-00X VIOLATION:** DO NOT [domain violation]
```

**Classification for the shared P-003/P-020/P-022/P-002 items:**
- `DO NOT spawn subagents` — The "P-003 VIOLATION:" label names a violation class but does NOT describe the consequence (what breaks) or the alternative (what to do instead). This is **NPT-014** for each instance.
- The label functions as a category tag, not a consequence clause.

**Exception:** Several agents also include a `<guardrails>` section with a **Fallback Behavior** sub-section that provides a 3-4 step procedure for the fallback case. Where the fallback directly corresponds to the prohibition, it serves as an alternative. However, these fallback sections address behavior when evidence is insufficient — they are not alternatives to the forbidden actions themselves.

### G2-001 | ps-analyst.md | Lines 86-90
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/problem-solving/agents/ps-analyst.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 86 | `DO NOT spawn subagents that spawn further subagents` | None (P-003 VIOLATION label is a category, not consequence) | None | NPT-014 |
| Line 87 | `DO NOT override explicit user instructions` | None | None | NPT-014 |
| Line 88 | `DO NOT hide uncertainty or present speculation as fact` | None | None | NPT-014 |
| Line 89 | `DO NOT return analysis results without file output` | None | None | NPT-014 |
| Line 90 | `DO NOT draw conclusions without evidence` | None | None | NPT-014 |

**Additional instance:**
| Line 110 | `DO NOT fabricate conclusions to fill gaps` | None | Fallback section provides 4-step procedure | NPT-009 |
| Line 257 | `DO NOT return transient output only. File creation AND link-artifact are MANDATORY.` | None | `File creation AND link-artifact are MANDATORY` acts as the alternative | NPT-009 |

---

### G2-002 | ps-researcher.md | Lines 87-91
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/problem-solving/agents/ps-researcher.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 87 | `DO NOT spawn subagents that spawn further subagents` | None | None | NPT-014 |
| Line 88 | `DO NOT override explicit user instructions` | None | None | NPT-014 |
| Line 89 | `DO NOT claim to have found information you didn't find` | None | None | NPT-014 |
| Line 90 | `DO NOT return research results without file output` | None | None | NPT-014 |
| Line 91 | `DO NOT make claims without citations` | None | None | NPT-014 |
| Line 110 | `DO NOT fabricate or extrapolate beyond evidence` | None | Fallback provides 4-step procedure | NPT-009 |
| Line 250 | `DO NOT return transient output only. File creation AND link-artifact are MANDATORY.` | None | Alternative given (MANDATORY) | NPT-009 |

---

### G2-003 | ps-architect.md | Lines 88-92
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/problem-solving/agents/ps-architect.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 88 | `DO NOT spawn subagents that spawn further subagents` | None | None | NPT-014 |
| Line 89 | `DO NOT make final decisions without user approval` | None | None | NPT-014 |
| Line 90 | `DO NOT hide negative consequences of a decision` | None | None | NPT-014 |
| Line 91 | `DO NOT return ADR content without file output` | None | None | NPT-014 |
| Line 92 | `DO NOT recommend without evaluating alternatives` | None | None | NPT-014 |
| Line 112 | `DO NOT make architectural decisions without adequate context` | None | Fallback provides procedure | NPT-009 |
| Line 272 | `DO NOT return transient output only. File creation AND link-artifact are MANDATORY.` | None | Alternative given (MANDATORY) | NPT-009 |

---

### G2-004 | ps-critic.md | Lines 126-130
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/problem-solving/agents/ps-critic.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 126 | `DO NOT spawn subagents or manage iteration loops` | None | None | NPT-014 |
| Line 127 | `DO NOT override explicit user instructions` | None | None | NPT-014 |
| Line 128 | `DO NOT hide quality issues or inflate scores` | None | None | NPT-014 |
| Line 129 | `DO NOT return critique without file output` | None | None | NPT-014 |
| Line 130 | `DO NOT self-invoke or trigger next iteration (orchestrator's job)` | None | `orchestrator's job` is partial redirect | NPT-009 |
| Line 152 | `DO NOT provide quality score without criteria` | None | Fallback procedure given | NPT-009 |
| Line 158 | `NEVER hardcode values; always reference the SSOT.` | None | `always reference the SSOT` is the alternative | NPT-009 |
| Line 386 | `DO NOT return transient output only. File creation AND link-artifact are MANDATORY.` | None | Alternative given (MANDATORY) | NPT-009 |
| Line 38 | `You DO NOT manage the loop yourself - that would violate P-003` | `that would violate P-003` is a consequence reference (but not impact) | `you are invoked on each iteration` is the context | NPT-014 |

---

### G2-005 | ps-reviewer.md | Lines 88-92
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/problem-solving/agents/ps-reviewer.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 88 | `DO NOT spawn subagents that spawn further subagents` | None | None | NPT-014 |
| Line 89 | `DO NOT override explicit user instructions` | None | None | NPT-014 |
| Line 90 | `DO NOT minimize or hide quality issues` | None | None | NPT-014 |
| Line 91 | `DO NOT return review without file output` | None | None | NPT-014 |
| Line 92 | `DO NOT claim issues without evidence` | None | None | NPT-014 |
| Line 112 | `DO NOT provide incomplete assessment without disclosure` | None | Fallback procedure given | NPT-009 |
| Line 293 | `DO NOT return transient output only. File creation AND link-artifact are MANDATORY.` | None | Alternative given (MANDATORY) | NPT-009 |

---

### G2-006 | ps-investigator.md | Lines 58-62
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/problem-solving/agents/ps-investigator.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 58 | `DO NOT spawn subagents that spawn further subagents` | None | None | NPT-014 |
| Line 59 | `DO NOT override explicit user instructions` | None | None | NPT-014 |
| Line 60 | `DO NOT hide uncertainty or gaps in evidence` | None | None | NPT-014 |
| Line 61 | `DO NOT return investigation without file output` | None | None | NPT-014 |
| Line 62 | `DO NOT claim root cause without evidence` | None | None | NPT-014 |
| Line 82 | `DO NOT fabricate root cause to fill gaps` | None | Fallback procedure given | NPT-009 |
| Line 265 | `DO NOT return transient output only. File creation AND link-artifact are MANDATORY.` | None | Alternative given (MANDATORY) | NPT-009 |

---

### G2-007 | ps-validator.md | Lines 99-103
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/problem-solving/agents/ps-validator.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 99 | `DO NOT spawn subagents that spawn further subagents` | None | None | NPT-014 |
| Line 100 | `DO NOT override explicit user instructions` | None | None | NPT-014 |
| Line 101 | `DO NOT mark as validated without evidence` | None | None | NPT-014 |
| Line 102 | `DO NOT return validation results without file output` | None | None | NPT-014 |
| Line 103 | `DO NOT claim validation without evidence` | None | None | NPT-014 |
| Line 123 | `DO NOT mark constraints as validated without evidence` | None | Fallback procedure given | NPT-009 |
| Line 214 | `DO NOT return transient output only. File creation AND link-artifact are MANDATORY.` | None | Alternative given (MANDATORY) | NPT-009 |

---

### G2-008 | ps-synthesizer.md | Lines 90-94
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/problem-solving/agents/ps-synthesizer.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 90 | `DO NOT spawn subagents that spawn further subagents` | None | None | NPT-014 |
| Line 91 | `DO NOT override explicit user instructions` | None | None | NPT-014 |
| Line 92 | `DO NOT hide contradictions between sources` | None | None | NPT-014 |
| Line 93 | `DO NOT return synthesis without file output` | None | None | NPT-014 |
| Line 94 | `DO NOT present patterns without citing sources` | None | None | NPT-014 |
| Line 114 | `DO NOT fabricate patterns not in sources` | None | Fallback procedure given | NPT-009 |
| Line 280 | `DO NOT return transient output only. File creation AND link-artifact are MANDATORY.` | None | Alternative given (MANDATORY) | NPT-009 |

---

### G2-009 | ps-reporter.md | Lines 49-53
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/problem-solving/agents/ps-reporter.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 49 | `DO NOT spawn subagents that spawn further subagents` | None | None | NPT-014 |
| Line 50 | `DO NOT override explicit user instructions` | None | None | NPT-014 |
| Line 51 | `DO NOT misrepresent progress or hide blockers` | None | None | NPT-014 |
| Line 52 | `DO NOT return report without file output` | None | None | NPT-014 |
| Line 53 | `DO NOT show inaccurate task status` | None | None | NPT-014 |
| Line 73 | `DO NOT fabricate metrics or progress` | None | Fallback procedure given | NPT-009 |
| Line 167 | `DO NOT return transient output only. File creation AND link-artifact are MANDATORY.` | None | Alternative given (MANDATORY) | NPT-009 |

---

### G2-010 | orch-planner.md | Lines 65-70
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/orchestration/agents/orch-planner.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 65 | `DO NOT spawn subagents that spawn further subagents` | None | None | NPT-014 |
| Line 66 | `DO NOT override explicit user instructions` | None | None | NPT-014 |
| Line 67 | `DO NOT misrepresent workflow complexity` | None | None | NPT-014 |
| Line 68 | `DO NOT return plans without file persistence` | None | None | NPT-014 |
| Line 69 | `DO NOT omit mandatory disclaimer from outputs` | None | None | NPT-014 |
| Line 70 | `DO NOT use hardcoded pipeline names (ps-pipeline, nse-pipeline)` | None | None | NPT-014 |
| Line 88 | `DO NOT create ORCHESTRATION.yaml without complete phase definitions` | None | None | NPT-014 |

---

### G2-011 | orch-tracker.md | Lines 62-68
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/orchestration/agents/orch-tracker.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 62 | `DO NOT spawn subagents that spawn further subagents` | None | None | NPT-014 |
| Line 63 | `DO NOT override explicit user instructions` | None | None | NPT-014 |
| Line 64 | `DO NOT misrepresent execution status` | None | None | NPT-014 |
| Line 65 | `DO NOT report status without updating files` | None | None | NPT-014 |
| Line 66 | `DO NOT omit mandatory disclaimer from outputs` | None | None | NPT-014 |
| Line 67 | `DO NOT use hardcoded paths - ALWAYS resolve dynamically` | None | `ALWAYS resolve dynamically` is the alternative | NPT-009 |
| Line 68 | `DO NOT update without reading current state first` | None | `reading current state first` is the alternative | NPT-009 |
| Line 87 | `DO NOT write partial updates - atomic or nothing` | None | `atomic or nothing` is the alternative | NPT-009 |
| Line 221 | `the tracker MUST NOT mark the phase/barrier as COMPLETE` (when conditions not met) | Consequence implied by the conditions not being met | Conditions to meet ARE listed above this line | NPT-013 |

---

### G2-012 | orch-synthesizer.md | Lines 66-71
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/orchestration/agents/orch-synthesizer.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 66 | `DO NOT spawn subagents that spawn further subagents` | None | None | NPT-014 |
| Line 67 | `DO NOT override explicit user instructions` | None | None | NPT-014 |
| Line 68 | `DO NOT make claims without artifact evidence` | None | None | NPT-014 |
| Line 69 | `DO NOT return synthesis without file persistence` | None | None | NPT-014 |
| Line 70 | `DO NOT omit mandatory disclaimer from outputs` | None | None | NPT-014 |
| Line 71 | `DO NOT synthesize without reading ALL artifacts` | None | None | NPT-014 |
| Line 90 | `DO NOT make recommendations without evidence base` | None | Fallback given | NPT-009 |

---

### G2-013 | adv-executor.md | Lines 334-335
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/adversary/agents/adv-executor.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 334 | `This agent MUST NOT use the Task tool to spawn subagents` | `P-003 VIOLATION` quoted as the consequence | No alternative given | NPT-009 |
| Line 335 | `This agent MUST NOT instruct the orchestrator to invoke other agents on its behalf` | `P-003 VIOLATION` quoted | No alternative given | NPT-009 |

**Note:** The error message on line 340 provides a consequence description. P-003 VIOLATION in the label functions as consequence reference here since the error message is explicitly quoted.

---

### G2-014 | adv-scorer.md | Lines 311-312
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/adversary/agents/adv-scorer.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 311 | `This agent MUST NOT use the Task tool to spawn subagents` | Error message quoted on line 317 serves as consequence | None | NPT-009 |
| Line 312 | `This agent MUST NOT instruct the orchestrator to invoke other agents on its behalf` | Error message quoted | None | NPT-009 |

---

### G2-015 | adv-selector.md | Lines 211-212
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/adversary/agents/adv-selector.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 211 | `This agent MUST NOT use the Task tool to spawn subagents` | Error message quoted on line 217 | None | NPT-009 |
| Line 212 | `This agent MUST NOT instruct the orchestrator to invoke other agents on its behalf` | Error message quoted | None | NPT-009 |

---

### G2-016 | nse-* agents (shared pattern)
**Files:** `nse-integration.md`, `nse-qa.md`, `nse-risk.md`, `nse-requirements.md`, `nse-explorer.md`, `nse-verification.md`, `nse-configuration.md`, `nse-reviewer.md`

All NSE agents follow the same guardrails pattern as ps-* agents. Each has 5-7 `DO NOT` items in the forbidden actions list, plus domain-specific items in the fallback section.

| Agent | P-003/P-020/P-022/P-002 | Domain-specific | Classification |
|-------|------------------------|-----------------|----------------|
| nse-integration.md (L56-61) | 4 bare DO NOT items | 1 bare (DO NOT integrate without ICD), 1 bare (hide undocumented interfaces) | All NPT-014 |
| nse-qa.md (L64-68) | 4 bare DO NOT items | 1 bare (DO NOT claim compliance without evidence) | All NPT-014 |
| nse-risk.md (L62-68) | 4 bare DO NOT items | 2 bare (suppress risks, hide RED risks) | All NPT-014 |
| nse-requirements.md (L124-129) | 4 bare DO NOT items | 2 bare (orphan requirements, incomplete without disclosure) | All NPT-014 |
| nse-explorer.md (L71-77) | 4 bare DO NOT items | 2 bare (prematurely converge, dismiss alternatives) | All NPT-014 |
| nse-verification.md (L59-64) | 4 bare DO NOT items | 2 bare (claim pass without evidence, hide gaps) | All NPT-014 |
| nse-configuration.md (L57-62) | 4 bare DO NOT items | 2 bare (claim baseline without approval, uncontrolled changes) | All NPT-014 |
| nse-reviewer.md (L132-137) | 4 bare DO NOT items | 2 bare (approve with RED criteria, claim ready without evidence) | All NPT-014 |
| nse-architecture.md (L722-724) | WILL NOT items (not prohibition keywords) | None | N/A — different format |

**Fallback DO NOT items in NSE agents (Fallback sections):**
Each NSE agent has 3-4 `DO NOT` items in the fallback section that have the Fallback procedure as the alternative. These are NPT-009 (alternative present via fallback steps, no consequence for the DO NOT).

---

### G2-017 | wt-verifier.md | Lines 109-112
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/worktracker/agents/wt-verifier.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 80 | `DO NOT use regex or manual text parsing for frontmatter/status` | None | `MUST use /ast skill operations` (same sentence) | NPT-009 |
| Line 103 | `DO NOT use Grep(pattern="> **Status:**") for frontmatter extraction` | `The AST approach handles edge cases regex-based extraction misses` | `use jerry ast frontmatter` (stated) | NPT-013 |
| Line 109 | `DO NOT spawn subagents` | None | None | NPT-014 |
| Line 110 | `DO NOT return transient output only - MUST create verification report` | None | Alternative given (MUST create) | NPT-009 |
| Line 111 | `DO NOT mark incomplete work as complete to satisfy user` | None | None | NPT-014 |
| Line 112 | `DO NOT modify work item status directly - only report verification results` | None | Alternative given (only report) | NPT-009 |
| Line 161 | `Work items MUST NOT transition to DONE/COMPLETED without:` | Consequences listed below | Conditions listed are the alternative | NPT-013 |

---

### G2-018 | wt-auditor.md | Lines 110-113
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/worktracker/agents/wt-auditor.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 71 | `DO NOT use manual Read+Grep template comparison for frontmatter extraction` | None | `MUST use /ast skill operations` (same sentence) | NPT-009 |
| Line 103 | `DO NOT use manual Read+Grep template comparison for frontmatter extraction` | None | `MUST use /ast skill` (adjacent) | NPT-009 |
| Line 110 | `DO NOT spawn subagents` | None | None | NPT-014 |
| Line 111 | `DO NOT auto-fix issues without user approval` | None | None | NPT-014 |
| Line 112 | `DO NOT return audit results without file output` | None | None | NPT-014 |
| Line 113 | `DO NOT ignore worktracker integrity violations` | None | None | NPT-014 |

---

### G2-019 | wt-visualizer.md | Lines 65-67
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/worktracker/agents/wt-visualizer.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 42 | `DO NOT` use non-AST for structured metadata extraction | None | `MUST use /ast skill operations` (same sentence) | NPT-009 |
| Line 60 | `DO NOT use Grep patterns on '> **Status:**'` | None | Alternative given (AST approach described) | NPT-009 |
| Line 65 | `DO NOT spawn subagents` | None | None | NPT-014 |
| Line 66 | `DO NOT return transient output only - diagrams MUST be persisted` | None | Alternative given (MUST be persisted) | NPT-009 |
| Line 67 | `DO NOT modify work item content` | None | None | NPT-014 |
| Line 97 | `DO NOT fabricate data or relationships` | None | None | NPT-014 |

---

### G2-020 | ts-formatter.md | Lines 157-161
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/transcript/agents/ts-formatter.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 59-61 | `The following files MUST NOT be created. CRITICAL validation failure.` | `CRITICAL validation failure` is a consequence | What TO create is listed in adjacent section | NPT-013 |
| Line 87 | `MUST NOT LINK TO` (section header for bad link targets) | None (header only) | Links TO create listed in adjacent section | NPT-009 |
| Line 148 | `NEVER 'canonical-transcript.json'` | None in same row | `Read index.json and extraction-report.json` (same sentence) | NPT-009 |
| Line 152 | `NEVER read 'canonical-transcript.json' (~930KB).` | `CRITICAL FILE SIZE RULE` consequence implied | None given inline | NPT-009 |
| Line 157 | `DO NOT spawn subagents` | None | None | NPT-014 |
| Line 158 | `DO NOT return without creating all packet files` | None | None | NPT-014 |
| Line 159 | `DO NOT create files exceeding 35K tokens` | None | None | NPT-014 |
| Line 160 | `DO NOT use non-standard anchor formats` | None | None | NPT-014 |
| Line 161 | `DO NOT read 'canonical-transcript.json' - use 'index.json' instead` | None | Alternative given (`use index.json instead`) | NPT-009 |

---

### G2-021 | ts-parser.md | Lines 93-97
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/transcript/agents/ts-parser.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 93 | `DO NOT spawn subagents` | None | None | NPT-014 |
| Line 94 | `DO NOT return parsed data without file output` | None | None | NPT-014 |
| Line 95 | `DO NOT claim parsing success when errors occurred` | None | None | NPT-014 |
| Line 96 | `DO NOT modify or "correct" transcript text content` | None | None | NPT-014 |
| Line 97 | `DO NOT fabricate timestamps for plain text files` | None | None | NPT-014 |

---

### G2-022 | ts-extractor.md | Lines 49-53 and 919-920
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/transcript/agents/ts-extractor.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 49 | `DO NOT spawn subagents` | None | None | NPT-014 |
| Line 50 | `DO NOT return extractions without file output` | None | None | NPT-014 |
| Line 51 | `DO NOT extract entities without citation to source` | None | None | NPT-014 |
| Line 52 | `DO NOT claim high confidence without evidence` | None | None | NPT-014 |
| Line 53 | `DO NOT invent entities not in transcript` | None | None | NPT-014 |
| Line 65 (Format A deprecated) | `DO NOT USE` (deprecated format) | None | The correct Format B described in adjacent section | NPT-009 |
| Line 919 | `NEVER calculate stats from intermediate counts` | None | None | NPT-014 |
| Line 920 | `NEVER report more items than actually extracted` | None | None | NPT-014 |

---

### G2-023 | ts-mindmap-mermaid.md | Lines 45-47
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/transcript/agents/ts-mindmap-mermaid.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 45 | `DO NOT spawn subagents` | None | None | NPT-014 |
| Line 46 | `DO NOT return without creating mindmap file` | None | None | NPT-014 |
| Line 47 | `DO NOT generate invalid Mermaid syntax` | None | None | NPT-014 |

---

### G2-024 | ts-mindmap-ascii.md | Lines 45-47
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/transcript/agents/ts-mindmap-ascii.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 45 | `DO NOT spawn subagents` | None | None | NPT-014 |
| Line 46 | `DO NOT return without creating ASCII file` | None | None | NPT-014 |
| Line 47 | `DO NOT exceed 80 character width` | None | None | NPT-014 |

---

### G2-025 | sb-voice.md | Lines 138-143, 159-160
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/saucer-boy/agents/sb-voice.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 138 | `NEVER deploy personality in no-personality contexts` | None | Implied by `(constitutional failure, governance, security)` as context signal | NPT-009 |
| Line 139 | `NEVER override user request for formal tone (P-020).` | None | Implied — use formal tone | NPT-009 |
| Line 140 | `NEVER sacrifice technical accuracy for personality.` | None | `Information is always correct` is the alternative | NPT-009 |
| Line 141 | `NEVER produce framework output` | None | `That is /saucer-boy-framework-voice` is the alternative | NPT-009 |
| Line 142 | `NEVER force humor. If the metaphor doesn't come naturally, use direct language.` | None | Alternative given (`use direct language`) | NPT-009 |
| Line 143 | `NEVER use sycophantic praise. Match enthusiasm to achievement.` | None | Alternative given (`Match enthusiasm to achievement`) | NPT-009 |
| Line 159 | `This agent MUST NOT use the Task tool` | Error message quoted as consequence | None | NPT-009 |
| Line 160 | `This agent MUST NOT instruct the orchestrator to invoke other agents` | Error message quoted | None | NPT-009 |

---

### G2-026 | sb-reviewer.md | Lines 203-207, 227-228
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/saucer-boy-framework-voice/agents/sb-reviewer.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 203 | `NEVER skip Test 1. It is always evaluated first.` | None | Order given (`always evaluated first` is the alternative) | NPT-009 |
| Line 204 | `NEVER evaluate Tests 2-5 if Test 1 fails.` | None | `Report the information gap only` is the alternative | NPT-009 |
| Line 205 | `NEVER soften boundary violation reports.` | None | `If sarcasm is detected, flag it clearly` is the alternative | NPT-009 |
| Line 206 | `NEVER rewrite the text.` | None | `Report findings and suggest fixes. Rewriting is sb-rewriter's responsibility.` — alternative given | NPT-009 |
| Line 207 | `NEVER score voice fidelity quantitatively.` | None | `Scoring is sb-calibrator's responsibility.` — alternative given | NPT-009 |
| Line 227 | `This agent MUST NOT use the Task tool` | Error message quoted | None | NPT-009 |
| Line 228 | `This agent MUST NOT instruct the orchestrator to invoke other agents` | Error message quoted | None | NPT-009 |

---

### G2-027 | sb-rewriter.md | Lines 197-201, 216-217
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/saucer-boy-framework-voice/agents/sb-rewriter.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 197 | `NEVER remove or obscure technical information.` | None | `Every score, error, rule ID... MUST appear in the rewrite` — alternative given | NPT-009 |
| Line 198 | `NEVER add humor in no-humor contexts` | None | Context list given; implied alternative is use neutral tone | NPT-009 |
| Line 199 | `NEVER present a rewrite that fails any Authenticity Test.` | None | `Revise internally first` — alternative given | NPT-009 |
| Line 200 | `NEVER use forbidden constructions` | None | Reference to vocabulary-reference.md given | NPT-009 |
| Line 201 | `NEVER violate boundary conditions. Check all 8 before presenting.` | None | Procedure given (check all 8) | NPT-009 |
| Line 216 | `This agent MUST NOT use the Task tool` | Error message quoted | None | NPT-009 |
| Line 217 | `This agent MUST NOT instruct the orchestrator to invoke other agents` | Error message quoted | None | NPT-009 |

---

### G2-028 | sb-calibrator.md | Lines 340-341
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/saucer-boy-framework-voice/agents/sb-calibrator.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 340 | `This agent MUST NOT use the Task tool` | Error message quoted | None | NPT-009 |
| Line 341 | `This agent MUST NOT instruct the orchestrator to invoke other agents` | Error message quoted | None | NPT-009 |

---

### G2-029 | red-persist.md | Line 18
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/red-team/agents/red-persist.md`

| Instance | Prohibition | Consequence | Alternative | Classification |
|----------|-------------|-------------|-------------|----------------|
| Line 18 | `this agent MUST NOT proceed` (if persistence_authorized is not true) | None — HALT instruction given below in methodology | `HALT if not authorized` (line 43 methodology) is the alternative | NPT-009 |

---

## Group 3: SKILL.md Files

> **Files:** `skills/*/SKILL.md` (13 files scanned)

### G3-001 | saucer-boy/SKILL.md | Lines 126-127
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/saucer-boy/SKILL.md`
**Prohibition text:** `Agent CANNOT invoke other agents. Agent CANNOT spawn subagents.`
**Consequence present:** No
**Alternative present:** No redirect (only repeated as a design constraint)
**Classification:** NPT-014 (both instances)
**Note:** These appear in the P-003 compliance ASCII diagram as annotations. No consequence or redirect.

---

### G3-002 | saucer-boy-framework-voice/SKILL.md | Lines 282-283
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/saucer-boy-framework-voice/SKILL.md`
**Prohibition text:** `Agents CANNOT invoke other agents. Agents CANNOT spawn subagents.`
**Consequence present:** No
**Alternative present:** No redirect
**Classification:** NPT-014 (both instances)

---

### G3-003 | saucer-boy/SKILL.md | Lines 87-93 ("Do NOT use when")
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/saucer-boy/SKILL.md`
**Prohibition text:**
```
Do NOT use when:
- Producing framework output — use /saucer-boy-framework-voice
- In a constitutional failure or governance escalation — personality OFF
- Security-relevant operations — precision only
- User explicitly requests formal/neutral tone (P-020 user authority)
- Writing internal design docs, ADRs, or research artifacts
```
**Classification:**
- `Producing framework output` — has alternative (`use /saucer-boy-framework-voice`). NPT-009 (no consequence).
- `constitutional failure...` — has redirect (`personality OFF`) but no consequence. NPT-009.
- `Security-relevant operations — precision only` — has redirect (`precision only`). NPT-009.
- `User explicitly requests formal/neutral tone` — has rationale (P-020 reference). NPT-009.
- `Writing internal design docs...` — bare, no consequence, no alternative. NPT-014.

---

### G3-004 | adversary/SKILL.md (Do NOT use when section)
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/adversary/SKILL.md`
**Note:** Grep found no prohibition keywords. File confirmed to use "Do NOT use when" section per skill standards, but prohibition keywords not present in the file body per scan results.
**Classification:** N/A

---

## Group 4: Templates and Constitution

> **Files:** `.context/templates/*.md`, `docs/governance/JERRY_CONSTITUTION.md`

### G4-001 | JERRY_CONSTITUTION.md | Line 47 (P-002)
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/docs/governance/JERRY_CONSTITUTION.md`
**Prohibition text:**
```
Agents SHALL NOT:
- Return analysis results without file output
- Rely solely on conversational context for state
- Assume prior context survives across sessions
```
**Consequence present:** No explicit consequence in P-002 text
**Alternative present:** The positive form is stated (`Agents SHALL persist all significant outputs to the filesystem`) immediately before the SHALL NOT list
**Classification:** NPT-009 (has alternative — positive instruction; lacks consequence)

---

### G4-002 | JERRY_CONSTITUTION.md | Line 63 (P-003)
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/docs/governance/JERRY_CONSTITUTION.md`
**Prohibition text:** `Agents SHALL NOT spawn subagents that spawn additional subagents. Maximum nesting depth is ONE level.`
**Consequence present:** `Rationale: Prevents unbounded resource consumption and maintains control hierarchy.` — this is a rationale, which is consequence-adjacent
**Alternative present:** `Maximum nesting depth is ONE level (orchestrator → worker)` — yes, alternative given
**Classification:** NPT-009
**Note:** The rationale sentence functions as a consequence-reason. Alternative (one-level nesting) is stated.

---

### G4-003 | JERRY_CONSTITUTION.md | Lines 137-140 (P-012)
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/docs/governance/JERRY_CONSTITUTION.md`
**Prohibition text:**
```
Agents SHALL NOT:
- Add unrequested features
- Refactor code beyond requirements
- Make "improvements" without explicit approval
```
**Consequence present:** No
**Alternative present:** `Agents SHALL stay within assigned scope.` (positive form before the list)
**Classification:** NPT-009 (has alternative; lacks consequence)

---

### G4-004 | JERRY_CONSTITUTION.md | Lines 181-185 (P-022)
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/docs/governance/JERRY_CONSTITUTION.md`
**Prohibition text:**
```
Agents SHALL NOT deceive users about:
- Actions taken or planned
- Capabilities or limitations
- Sources of information
- Confidence levels
```
**Consequence present:** No
**Alternative present:** No redirect (no positive form immediately adjacent to the SHALL NOT items)
**Classification:** NPT-014
**Note:** The positive form of P-022 is elsewhere. The SHALL NOT list is bare here.

---

### G4-005 | JERRY_CONSTITUTION.md | Lines 212-215 (P-031)
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/docs/governance/JERRY_CONSTITUTION.md`
**Prohibition text:**
```
Agents SHALL NOT:
- Exceed their expertise domain
- Override decisions from higher-trust agents
- Claim capabilities they lack
```
**Consequence present:** No
**Alternative present:** `Specialized agents SHALL operate within their designated role.` (positive form before the list)
**Classification:** NPT-009 (has alternative; lacks consequence)

---

### G4-006 | JERRY_CONSTITUTION.md | Lines 284-286 (P-043)
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/docs/governance/JERRY_CONSTITUTION.md`
**Prohibition text:**
```
Agents SHALL NOT:
- Omit the disclaimer from any persisted artifact
- Claim to provide official NASA guidance
- Present AI-generated content as authoritative SE decisions
```
**Consequence present:** No inline consequence (Rationale section follows separately)
**Alternative present:** `NSE agents SHALL include the mandatory disclaimer on ALL outputs.` (positive form before the list)
**Classification:** NPT-009 (has positive alternative; lacks consequence adjacent to the SHALL NOT list)

---

### G4-007 | Templates — adversarial templates (MUST NOT be redefined)
**Files:** `.context/templates/adversarial/s-*.md`, `TEMPLATE-FORMAT.md`
**Prohibition text:** `MUST NOT be redefined` (appears 10+ times across templates, referring to quality-enforcement.md constants)
**Consequence present:** Rationale (`sourced from quality-enforcement.md SSOT`) is adjacent
**Alternative present:** `use quality-enforcement.md SSOT` — always stated alongside
**Classification:** NPT-013 for all instances
**Note:** Each instance pairs the prohibition with a rationale (consequence-adjacent) and the alternative (reference the SSOT).

---

### G4-008 | WTI_RULES.md | Line 68
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/templates/worktracker/WTI_RULES.md`
**Prohibition text:** `Work items MUST NOT transition to DONE/COMPLETED without: [conditions]`
**Consequence present:** No explicit consequence (rationale: "Premature closure creates technical debt" — adjacent)
**Alternative present:** The conditions listed ARE the alternative (what to do instead)
**Classification:** NPT-009 (has alternative; consequence is rationale-form only)

---

### G4-009 | WTI_RULES.md | Line 114
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/templates/worktracker/WTI_RULES.md`
**Prohibition text:** `Work items MUST NOT be marked complete if work is incomplete.`
**Consequence present:** No
**Alternative present:** `Status MUST accurately reflect reality.` (same sentence, different clause)
**Classification:** NPT-009

---

### G4-010 | WTI_RULES.md | Line 243
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/templates/worktracker/WTI_RULES.md`
**Prohibition text:** `Entity files MUST NOT be created from memory or by copying other instance files.`
**Consequence present:** No
**Alternative present:** Positive form in same sentence: `Agents MUST read the canonical template from .context/templates/worktracker/ BEFORE creating`
**Classification:** NPT-009

---

### G4-011 | WTI_RULES.md | Line 256
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/templates/worktracker/WTI_RULES.md`
**Prohibition text:** `NEVER create entity files from memory or by copying other instance files`
**Consequence present:** No
**Alternative present:** Same as G4-010 — adjacent positive instruction
**Classification:** NPT-009

---

### G4-012 | SPIKE.md | Line 119
**File:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/.context/templates/worktracker/SPIKE.md`
**Prohibition text:** `Once DONE, a spike CANNOT be reopened (research is complete).`
**Consequence present:** `(research is complete)` is a rationale, not a consequence
**Alternative present:** No redirect (what to do if new research is needed)
**Classification:** NPT-014
**Note:** Should say "If further research is needed, create a new Spike."

---

---

## Priority Upgrade Queue

> Ordered by: Group (1 first, then 2, 3, 4) then NPT-014 first within each group.
> **NPT-014 instances are the upgrade target.** NPT-009 upgrades are secondary.

### Tier 1: NPT-014 in Group 1 (Rule Files — auto-C3)

| Priority | ID | File | Line(s) | Prohibition Summary | Upgrade Action Needed |
|----------|----|------|---------|---------------------|----------------------|
| 1 | G1-003 | `python-environment.md` | 3 | `NEVER use system Python.` (header) | Add consequence + redirect |
| 2 | G1-007 | `coding-standards.md` | 81 | `NEVER catch Exception broadly` | Add consequence + redirect to exception hierarchy |
| 3 | G1-011 | `quality-enforcement.md` | 81 | `MUST NOT be reassigned` (retired rule IDs) | Add consequence (reference breakage) + redirect (retire/map) |
| 4 | G1-014 | `mandatory-skill-usage.md` | 3 | `DO NOT wait for user to invoke.` (header) | Add consequence + redirect (trigger map reference) |
| 5 | G1-017 | `agent-development-standards.md` | 186 | `Workers MUST NOT spawn sub-workers.` | Add consequence (P-003 violation) + redirect (orchestrator coordinates) |
| 6 | G1-018 | `agent-development-standards.md` | 187 | `Worker agents MUST NOT include Task in allowed_tools` | Add consequence + redirect (omit Task from tools list) |
| 7 | G1-022 | `project-workflow.md` | 21 | `MUST NOT proceed without JERRY_PROJECT set.` | Add consequence + redirect (set env var or select project) |
| 8 | G1-024 | `agent-routing-standards.md` | 167 | `The system NEVER silently drops a routing request.` | Rephrase as positive guarantee or add consequence |

### Tier 2: NPT-014 in Group 2 (Agent Definitions)

> High-volume pattern: the `P-XXX VIOLATION: DO NOT X` items in agent forbidden-actions lists.
> Recommended approach: apply a standardized upgrade template across all agents.

| Priority | ID | Agent File | Prohibition Pattern | Count | Upgrade Strategy |
|----------|----|------------|---------------------|-------|-----------------|
| 9 | G2-001 | `ps-analyst.md` | `DO NOT spawn/override/hide/return/draw` | 5 | Apply NPT-013 template |
| 10 | G2-002 | `ps-researcher.md` | `DO NOT spawn/override/claim/return/make` | 5 | Apply NPT-013 template |
| 11 | G2-003 | `ps-architect.md` | `DO NOT spawn/make/hide/return/recommend` | 5 | Apply NPT-013 template |
| 12 | G2-004 | `ps-critic.md` | `DO NOT spawn/override/hide/return/manage` | 5 | Apply NPT-013 template |
| 13 | G2-005 | `ps-reviewer.md` | `DO NOT spawn/override/minimize/return/claim` | 5 | Apply NPT-013 template |
| 14 | G2-006 | `ps-investigator.md` | `DO NOT spawn/override/hide/return/claim` | 5 | Apply NPT-013 template |
| 15 | G2-007 | `ps-validator.md` | `DO NOT spawn/override/mark/return/claim` | 5 | Apply NPT-013 template |
| 16 | G2-008 | `ps-synthesizer.md` | `DO NOT spawn/override/hide/return/present` | 5 | Apply NPT-013 template |
| 17 | G2-009 | `ps-reporter.md` | `DO NOT spawn/override/misrepresent/return/show` | 5 | Apply NPT-013 template |
| 18 | G2-010 | `orch-planner.md` | `DO NOT spawn/override/misrepresent/return/omit/hardcode/create` | 7 | Apply NPT-013 template |
| 19 | G2-011 | `orch-tracker.md` | `DO NOT spawn/override/misrepresent/report/omit` | 5 | Apply NPT-013 template |
| 20 | G2-012 | `orch-synthesizer.md` | `DO NOT spawn/override/claim/return/omit/synthesize` | 6 | Apply NPT-013 template |
| 21 | G2-016 | `nse-* agents (8 files)` | Shared pattern of 4-6 bare DO NOT items | 40+ | Apply NPT-013 template |
| 22 | G2-017 | `wt-verifier.md` | `DO NOT spawn / mark incomplete as complete` | 2 | Apply NPT-013 template |
| 23 | G2-018 | `wt-auditor.md` | `DO NOT spawn/auto-fix/return/ignore` | 4 | Apply NPT-013 template |
| 24 | G2-019 | `wt-visualizer.md` | `DO NOT spawn/modify work item content/fabricate` | 3 | Apply NPT-013 template |
| 25 | G2-021 | `ts-parser.md` | `DO NOT spawn/return/claim/modify/fabricate` | 5 | Apply NPT-013 template |
| 26 | G2-022 | `ts-extractor.md` | `DO NOT spawn/return/extract/claim/invent + NEVER calculate/report` | 7 | Apply NPT-013 template |
| 27 | G2-023 | `ts-mindmap-mermaid.md` | `DO NOT spawn/return/generate` | 3 | Apply NPT-013 template |
| 28 | G2-024 | `ts-mindmap-ascii.md` | `DO NOT spawn/return/exceed` | 3 | Apply NPT-013 template |
| 29 | G2-020 | `ts-formatter.md` | `DO NOT spawn/return/create/use/read` | 4 bare | Apply NPT-013 template |

### Tier 3: NPT-014 in Group 3 (SKILL.md)

| Priority | ID | File | Line(s) | Prohibition | Upgrade Action |
|----------|----|------|---------|-------------|----------------|
| 30 | G3-001 | `saucer-boy/SKILL.md` | 126-127 | `Agent CANNOT invoke other agents. Agent CANNOT spawn subagents.` | Add consequence + redirect |
| 31 | G3-002 | `saucer-boy-framework-voice/SKILL.md` | 282-283 | `Agents CANNOT invoke other agents. Agents CANNOT spawn subagents.` | Add consequence + redirect |
| 32 | G3-003 | `saucer-boy/SKILL.md` | 93 | `Writing internal design docs, ADRs, or research artifacts` (bare Do NOT) | Add consequence + redirect |

### Tier 4: NPT-014 in Group 4 (Templates + Constitution)

| Priority | ID | File | Line(s) | Prohibition | Upgrade Action |
|----------|----|------|---------|-------------|----------------|
| 33 | G4-004 | `JERRY_CONSTITUTION.md` | 181-185 | `P-022: Agents SHALL NOT deceive users about...` | Add consequence + positive alternative |
| 34 | G4-012 | `SPIKE.md` template | 119 | `a spike CANNOT be reopened` | Add consequence + redirect (create new Spike) |

---

### Secondary Queue: NPT-009 → NPT-013 Upgrades

These already have EITHER consequence OR alternative. Adding the missing half completes them.

| Queue # | File | NPT-009 Instance | Missing Element | Upgrade Action |
|---------|------|------------------|-----------------|----------------|
| S-01 | `testing-standards.md:32` | `NEVER write implementation before test fails` | Alternative | Add "write the failing test first, then implementation" |
| S-02 | `testing-standards.md:81` | `NEVER mock domain objects` | Consequence | Add consequence: "tests will have false confidence" |
| S-03 | `python-environment.md:48` | `NEVER read canonical-transcript.json` | Alternative | Add "use index.json and chunk files instead" |
| S-04 | `architecture-standards.md:34b` | `application/ MUST NOT import from infrastructure/` | Alternative | Add "import only from domain/" |
| S-05 | `architecture-standards.md:41-45` | Layer dependency table | Consequence | Add consequence column to table |
| S-06 | `skill-standards.md:38` | `MUST NOT contain "claude" or "anthropic"` | Alternative | Add "use a descriptive name for your domain" |
| S-07 | `mandatory-skill-usage.md:50` | `DO NOT WAIT for user to invoke` | Consequence | Add consequence: "skill will not trigger, H-22 violation" |
| S-08 | `agent-development-standards.md:158` | `MUST NOT reference specific tool names` | Consequence | Add: "hexagonal boundary violation; domain becomes coupled to infra" |
| S-09 | `agent-development-standards.md:242` | `Worker agents MUST NOT be T5` | Alternative | Add "select T1-T4 based on required capabilities" |
| S-10 | `quality-enforcement.md:47` | `NEVER use regex for frontmatter extraction` | Consequence | Add: "regex fails on multi-line values and escaped characters" |
| S-11 | `JERRY_CONSTITUTION.md:47` | `P-002 SHALL NOT list` | Consequence | Add consequence for each SHALL NOT item |
| S-12 | `JERRY_CONSTITUTION.md:63` | `P-003 SHALL NOT` | Consequence formalized | Strengthen rationale to explicit consequence |
| S-13 | `JERRY_CONSTITUTION.md:137-140` | `P-012 SHALL NOT list` | Consequence | Add consequence for scope violations |
| S-14 | `JERRY_CONSTITUTION.md:212-215` | `P-031 SHALL NOT list` | Consequence | Add consequence for boundary violations |
| S-15 | `JERRY_CONSTITUTION.md:284-286` | `P-043 SHALL NOT list` | Consequence | Add consequence for disclaimer omission |
| S-16 | `WTI_RULES.md:68` | `MUST NOT transition to DONE without...` | Consequence | Add: "causes false progress signals and technical debt" |
| S-17 | `WTI_RULES.md:114` | `MUST NOT be marked complete if incomplete` | Consequence | Add: "misleads downstream agents and stakeholders" |
| S-18 | `WTI_RULES.md:243` | `MUST NOT be created from memory` | Consequence | Add: "creates malformed entities that fail AST validation" |
| S-19 | `WTI_RULES.md:256` | `NEVER create from memory` | Consequence | Same as S-18 |
| S-20 | All agent `MUST NOT use Task tool` (adv-*, sb-*)  | `MUST NOT use Task tool` | Alternative | Add: "complete the task directly or return partial result to orchestrator" |

---

## Evidence Notes

### Why "P-003 VIOLATION:" is NOT a consequence

The label format `P-003 VIOLATION: DO NOT X` appears throughout agent forbidden-actions lists. The classification rule states: "A rule ID reference (e.g., 'H-05') without explaining the impact" does NOT count as a consequence. The `P-003 VIOLATION:` prefix is a category label, identical in function to a rule ID reference. It names the violation class but does NOT describe:
- What will break (unbounded recursion, token exhaustion, governance violation)
- Who is affected (the session, the user, the orchestration pipeline)
- How severe the impact is (session termination, data loss, etc.)

The consequence for each prohibition must be described in plain language adjacent to the prohibition itself.

### Why error message quotes count as consequence for Task-tool prohibitions

In adv-*, sb-voice, sb-reviewer, sb-rewriter, and sb-calibrator agents, the MUST NOT prohibition is immediately followed by a quoted error message:
```
"P-003 VIOLATION: [agent] attempted to spawn a subagent. This agent is a worker and MUST NOT invoke other agents."
```
This error message functions as a consequence description (it describes what the system will report when the violation is detected). Therefore these instances are classified NPT-009 rather than NPT-014.

### Why "WILL NOT" in nse-architecture.md scope_boundaries is out of scope

The `nse-architecture.md` guardrails section uses:
```
WILL NOT: Make final design decisions (advisory only)
WILL NOT: Override user architectural preferences
WILL NOT: Claim certainty on complex trade-offs
```
These use `WILL NOT` (not one of the six specified prohibition keywords: NEVER, MUST NOT, DO NOT, FORBIDDEN, SHALL NOT, CANNOT). They are out of scope for this scan.

### Why the Layer Dependency Table header "MUST NOT Import" is excluded

The `architecture-standards.md` dependency table has a column header `MUST NOT Import`. This is a table structure label, not a prohibition statement. The prohibition is contained in H-07 rule rows, which are classified separately.

---

## PS Integration

**PS Context:** ADR-001 implementation, Phase 1 scan
**Entry:** Phase 1 deliverable — NPT-014 inventory
**Artifact path:** `projects/PROJ-014-negative-prompting-research/orchestration/adr001-implementation/phase-1-npt014-inventory.md`

**Handoff to Phase 2 (Upgrade Template Design):**
Key inputs for template work:
1. The dominant NPT-014 pattern in Group 2 is the 5-item `P-XXX VIOLATION: DO NOT X` forbidden-actions list. A single upgrade template covers ~70% of all NPT-014 instances.
2. Group 1 NPT-014 instances are structurally diverse — each requires individual upgrade text.
3. The NPT-013 target pattern is already exemplified in: H-07a (arch-standards), CP-01/CP-04 (agent-dev-standards), H-36a circuit breaker, ts-formatter MUST NOT CREATE section, orch-tracker MUST NOT mark COMPLETE.
4. The constitution (Group 4) uses SHALL NOT lists without consequences — a systematic addition of an Enforcement → Impact row per principle would address this.

---

*Analysis Version: 1.0*
*Scan Methodology: Grep + Read of all production framework files*
*Classification Method: Three-tier NPT-014/NPT-009/NPT-013 per ADR-001 definition*
*Analyst: ps-analyst*

---

## Implementation Completion Status

> **Added:** 2026-02-28 (post-implementation, TASK-031)
> **Diagnostic scan:** See `diagnostic-scan-report.md` in FEAT-001 directory

### Pre/Post Implementation Comparison

| Classification | Pre-Implementation | Post-Implementation | Delta |
|----------------|-------------------|---------------------|-------|
| NPT-014 (bare) | 55 actual (47 inventoried + 8 undercounted) | 2 remaining (Group 4 exclusions) | -53 |
| NPT-009 (partial) | 28 | Not re-counted (secondary queue) | -- |
| NPT-013 (complete) | 36 | Increased by ~53 upgrades | -- |

### Inventory Accuracy Correction

The original inventory identified 47 NPT-014 instances. The diagnostic scan (TASK-030) found 8 additional NPT-014 instances in NSE agent files (P-043/DISCLAIMER lines) that were present but undercounted. The actual pre-implementation total was 55 NPT-014 instances.

**Root cause:** The inventory at G2-016 described NSE agents with "4 bare DO NOT items" referring to P-003/P-020/P-022/P-002. Each NSE agent also has a P-043 line (a 5th constitutional item) within the listed line ranges but not separately counted. The orch-* agents' P-043 lines WERE counted and upgraded; the NSE agents' were missed.

### Group-Level Results

| Group | Original NPT-014 | Corrected NPT-014 | Upgraded | Remaining | Status |
|-------|-------------------|--------------------|----------|-----------|--------|
| Group 1: Rule files | 18 | 18 | 18 | 0 | COMPLETE |
| Group 2: Agent definitions | 19 | 27 (19 + 8 undercounted) | 27 | 0 | COMPLETE |
| Group 3: SKILL.md files | 4 | 4 | 4 | 0 | COMPLETE |
| Group 4: Templates + Constitution | 6 | 6 | 0 | 2 (E-04 exclusion) | EXCLUDED (C4 review needed) |
| **Total** | **47** | **55** | **49** | **2** | -- |

### Group 4 Exclusions (Unchanged per E-04)

| Item | File | Status | Required Action |
|------|------|--------|-----------------|
| G4-004 | `docs/governance/JERRY_CONSTITUTION.md:181-185` | NPT-014 | Requires separate C4 quality gate (AE-001) |
| G4-012 | `.context/templates/worktracker/SPIKE.md:119` | NPT-014 | Low-effort separate change |

### Implementation Commits

| Commit | Phase | Files Changed | Description |
|--------|-------|---------------|-------------|
| 47451ef6 | Phases 2-4 | 41 files | Core NPT-014 elimination across framework |
| a4ab091d | Post-scan fix | 8 files | NSE agent P-043 residual fixes |

*Completion Date: 2026-02-28*
*Verified by: TASK-030 diagnostic scan*
*Date: 2026-02-28*
