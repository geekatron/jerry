# Adversarial Review: Registration (Round 1)

## Execution Context

- **Strategies:** S-007 (Constitutional AI Critique), S-011 (Chain-of-Verification), S-002 (Devil's Advocate), S-010 (Self-Refine)
- **Sequence:** S-007 -> S-011 -> S-002 -> S-010
- **H-16 Note:** S-003 Steelman not run prior to S-002. This is a standalone adversarial audit of registration artifacts at user's explicit direction (P-020 authority). S-002 proceeds as direct critique per user instruction.
- **Templates:**
  - `.context/templates/adversarial/s-007-constitutional-ai.md`
  - `.context/templates/adversarial/s-011-cove.md`
  - `.context/templates/adversarial/s-002-devils-advocate.md`
  - `.context/templates/adversarial/s-010-self-refine.md`
- **Deliverables:**
  - `CLAUDE.md` — `/diataxis` row in Skills table
  - `AGENTS.md` — Diataxis Skill Agents section
  - `.context/rules/mandatory-skill-usage.md` — `/diataxis` trigger map row, H-22 update, L2-REINJECT update
- **Reference:** `.context/rules/agent-routing-standards.md` (trigger map format)
- **Executed:** 2026-02-27T00:00:00Z
- **Criticality:** C3 (AE-002 auto-escalation: touches `.context/rules/` = auto-C3 minimum)
- **Quality Threshold:** >= 0.95

---

## S-007 Constitutional Compliance

### Execution Protocol Applied

**Step 1: Load Constitutional Context**

Deliverable type: governance/routing rule documents + skill registration file. AE-002 applies (`.context/rules/` touched). Applicable rule files: `quality-enforcement.md` (H-22, H-25, H-26, H-34, H-36), `agent-routing-standards.md` (RT-M-001 through RT-M-009, H-36), `mandatory-skill-usage.md` (operational trigger map), `markdown-navigation-standards.md` (H-23).

**Step 2: Enumerate Applicable Principles**

| Principle | Tier | Applicability Rationale |
|-----------|------|------------------------|
| H-25: SKILL.md naming | HARD | Skill file structure compliance |
| H-26: Skill registration completeness | HARD | CLAUDE.md entry, AGENTS.md section, SKILL.md format |
| H-22: Proactive skill invocation | HARD | Trigger map must enable proactive routing |
| H-34: Official YAML frontmatter fields only | HARD | SKILL.md uses YAML frontmatter |
| H-36(b): Keyword-first routing standards | HARD | Trigger map quality and completeness |
| H-23: Navigation table required | HARD | SKILL.md is >30 lines Claude-consumed markdown |

**Step 3: Principle-by-Principle Evaluation**

| Principle | Status | Evidence |
|-----------|--------|----------|
| H-25: SKILL.md file named correctly, kebab-case folder | COMPLIANT | File: `SKILL.md`, folder: `skills/diataxis/` |
| H-26(a): Registered in CLAUDE.md | COMPLIANT | Line 87: `/diataxis \| Four-quadrant documentation methodology (6 agents: 4 writers, classifier, auditor)` |
| H-26(b): Registered in AGENTS.md | COMPLIANT | Lines 22, 242-273: Diataxis Skill Agents section with 6 agents |
| H-26(c): SKILL.md description has WHAT+WHEN+triggers | COMPLIANT | Description block covers what (four-quadrant), when (documentation creation, auditing, classification), triggers listed |
| H-26(d): Description <= 1024 chars, no XML | COMPLIANT | Frontmatter description within range |
| H-22: Trigger map entry present (5-column) | COMPLIANT | `mandatory-skill-usage.md` line 43 — 5-column format present |
| H-22: L2-REINJECT updated | COMPLIANT | `mandatory-skill-usage.md` line 5 includes `/diataxis for documentation creation, classification, and auditing` |
| H-22: H-22 rule text updated | COMPLIANT | HARD Rules table at line 23 includes "MUST invoke `/diataxis` for documentation creation, classification, and auditing using Diataxis four-quadrant methodology" |
| H-23: Navigation table in SKILL.md | COMPLIANT | Triple-Lens navigation table present (lines 43-47) |
| H-34: Official YAML frontmatter fields only | **VIOLATED** | `allowed-tools` used instead of `tools` — see CC-001 |
| H-36: Reference trigger map in `agent-routing-standards.md` includes `/diataxis` | **VIOLATED** | Reference Trigger Map in `agent-routing-standards.md` stops at `/saucer-boy-framework-voice`; no `/diataxis` row — see CC-002 |

---

### CC-001: SKILL.md Uses Invalid YAML Frontmatter Field `allowed-tools`

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **File** | `skills/diataxis/SKILL.md` line 11 |
| **Strategy Step** | S-007 Step 3 — H-34 violation |
| **Principle** | H-34: Agent definitions MUST use only the 12 official Claude Code frontmatter fields |

**Evidence:**

```yaml
# skills/diataxis/SKILL.md, line 11
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
```

The 12 official Claude Code frontmatter fields are: `name`, `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `isolation`. The field `allowed-tools` (hyphenated) is NOT in this list. The correct field name is `tools`.

**Analysis:**

Per H-34 and `agent-development-standards.md` (H-34 Architecture Note): "parsed by Claude Code runtime for tool enforcement and agent discovery" and non-official "fields are silently ignored by Claude Code." The `allowed-tools` field is therefore being silently discarded at runtime. Tool access constraints for all diataxis agents expressed at the SKILL.md level are not enforced. The skill inherits ALL tools from the invoking context, violating the Principle of Least Privilege (T1/T2 tier model defined in `agent-development-standards.md`).

**Recommendation:**

Replace `allowed-tools` with `tools` in the SKILL.md YAML frontmatter:

```yaml
# Before (incorrect — silently ignored by Claude Code)
allowed-tools: Read, Write, Edit, Glob, Grep, Bash

# After (correct — enforced by Claude Code runtime)
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
```

---

### CC-002: `agent-routing-standards.md` Reference Trigger Map Missing `/diataxis` Entry

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **File** | `.context/rules/agent-routing-standards.md` — Enhanced Trigger Map / Reference Trigger Map table |
| **Strategy Step** | S-007 Step 3 — H-36 routing standards compliance |
| **Principle** | H-36(b): Keyword-first routing; RT-M-004 SHOULD cross-reference new keywords against all existing skills |

**Evidence:**

`agent-routing-standards.md` Enhanced Trigger Map section lists only these skills:
`/problem-solving, /nasa-se, /orchestration, /transcript, /adversary, /saucer-boy, /saucer-boy-framework-voice`

The `/diataxis` row is absent from this reference table, despite being added to the operational `mandatory-skill-usage.md`. `agent-routing-standards.md` is the design-level SSOT for routing pattern guidance — its Reference Trigger Map is the canonical reference for collision analysis.

**Analysis:**

The divergence has two consequences: (1) future routing collision analyses referencing `agent-routing-standards.md` will not account for `/diataxis` keywords; (2) the RT-M-004 cross-referencing requirement ("When new keywords are added to the trigger map, they SHOULD be cross-referenced against all existing skills to identify collisions") cannot be verified as completed without a corresponding entry in the authoritative reference document.

**Recommendation:**

Add the `/diataxis` row to the Reference Trigger Map in `agent-routing-standards.md`, matching the `mandatory-skill-usage.md` entry. Add the priority ordering rationale comment explaining the choice of priority 11 for `/diataxis` (consistent with the rationale already documented for priorities 1-7 in that section).

---

### S-007 Compliance Summary

| Metric | Value |
|--------|-------|
| Principles evaluated | 11 |
| COMPLIANT | 9 |
| VIOLATED | 2 (1 Critical, 1 Major) |
| Constitutional Compliance Score | 1.00 - (1×0.10) - (1×0.05) = **0.85 (REVISE)** |

**Scoring Impact by S-014 Dimension:**

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | All 6 agents registered; counts accurate |
| Internal Consistency | 0.20 | Negative | CC-002: Reference map diverges from operational trigger map |
| Methodological Rigor | 0.20 | Negative | CC-001: Invalid YAML field bypasses tool access enforcement |
| Evidence Quality | 0.15 | Neutral | Agent listings match filesystem |
| Actionability | 0.15 | Neutral | Routing entry present and functional for basic keyword matching |
| Traceability | 0.10 | Negative | CC-002: Routing design not traceable from reference SSOT |

---

## S-011 Chain-of-Verification

### Claims Extracted and Verification Results

| Claim ID | Claim (from deliverables) | Source | Result |
|----------|---------------------------|--------|--------|
| CL-001 | AGENTS.md: "Diataxis Agents \| 6 \| `/diataxis` skill" | Filesystem `skills/diataxis/agents/*.md` | VERIFIED (6 files found) |
| CL-002 | AGENTS.md agent names: diataxis-tutorial, diataxis-howto, diataxis-reference, diataxis-explanation, diataxis-classifier, diataxis-auditor | Filesystem glob | VERIFIED (exact match) |
| CL-003 | CLAUDE.md: "6 agents: 4 writers, classifier, auditor" | AGENTS.md + filesystem | VERIFIED (4 writers = tutorial, howto, reference, explanation; + classifier + auditor = 6) |
| CL-004 | AGENTS.md total: "64 total" — per-skill sum 9+10+3+3+3+5+3+1+10+11+6=64 | Arithmetic + per-section counts | VERIFIED |
| CL-005 | L2-REINJECT in `mandatory-skill-usage.md` includes `/diataxis` | `mandatory-skill-usage.md` line 5 | VERIFIED |
| CL-006 | H-22 rule text in `mandatory-skill-usage.md` includes `/diataxis` | `mandatory-skill-usage.md` line 23 | VERIFIED |
| CL-007 | Trigger map uses 5-column format per `agent-routing-standards.md` | `mandatory-skill-usage.md` line 43 + `agent-routing-standards.md` format spec | VERIFIED (5 columns present) |
| CL-008 | SKILL.md activation-keywords match trigger map Detected Keywords | `mandatory-skill-usage.md` line 43 | MATERIAL DISCREPANCY — see CV-001 |
| CL-009 | Trigger map keywords cross-referenced against existing skills for collisions | `agent-routing-standards.md` Reference Trigger Map | UNVERIFIABLE — see CV-002 |
| CL-010 | Compound triggers follow "phrase match" format per `agent-routing-standards.md` | `agent-routing-standards.md` Compound Triggers column examples | VERIFIED (`"write docs" OR "document this" OR ...` matches established pattern) |

---

### CV-001: SKILL.md Activation Keywords Diverge from Trigger Map Detected Keywords

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Files** | `skills/diataxis/SKILL.md` activation-keywords (lines 12-30) vs `mandatory-skill-usage.md` line 43 |
| **Strategy Step** | S-011 Step 4: Consistency Check — MATERIAL DISCREPANCY |

**Claim (from SKILL.md activation-keywords):**

Keywords declared in SKILL.md that are NOT present in the trigger map's Detected Keywords column:
- `user guide`
- `getting started`
- `quickstart`
- `API docs`
- `developer guide`
- `write tutorial`
- `write documentation`
- `how-to guide`
- `document the`

**Independent Verification (from `mandatory-skill-usage.md` line 43):**

The `/diataxis` Detected Keywords column is:
```
documentation, tutorial, how-to, howto, reference docs, explanation, diataxis,
write docs, document this, create documentation, classify documentation,
audit documentation, quadrant, doc type
```

None of the 9 keywords listed above appear in this column.

Additionally, the SKILL.md `description` YAML frontmatter field explicitly states: "Triggers: documentation, tutorial, how-to, howto, reference docs, explanation, diataxis, write docs, user guide, getting started, quickstart, API docs." This is the field Claude Code uses for routing and skill discovery — it creates a false contract about activation conditions.

**Discrepancy:**

SKILL.md declares 9 activation keywords that have no corresponding entries in the operational trigger map. Users reading SKILL.md's `description` field to understand when the skill activates will receive incorrect information (P-022 concern). The request "write a user guide for getting started" will NOT route to `/diataxis` via keyword matching.

**Correction:**

Add the following to the trigger map's Detected Keywords for `/diataxis`:
`user guide, getting started, quickstart, API docs, developer guide, write tutorial, write documentation, how-to guide`

OR: Remove these keywords from SKILL.md `activation-keywords` and `description` triggers list, with documented rationale for exclusion.

---

### CV-002: Collision Analysis for `/diataxis` Keywords Unverifiable — Reference Map Incomplete

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **File** | `.context/rules/agent-routing-standards.md` — Reference Trigger Map table |
| **Strategy Step** | S-011 Step 3: Independent Verification — UNVERIFIABLE |

**Claim (implicit from routing governance):**

New trigger keywords for `/diataxis` were cross-referenced against existing skills for collisions per RT-M-004 ("When new keywords are added to the trigger map, they SHOULD be cross-referenced against all existing skills to identify collisions").

**Independent Verification:**

The Reference Trigger Map in `agent-routing-standards.md` — the canonical source for collision analysis — does not include a `/diataxis` row. Cross-referencing cannot be confirmed as completed from this authoritative source.

**Discrepancy:**

The collision analysis for keywords like `documentation`, `tutorial`, `explanation`, and `reference docs` against all existing skills has not been formally documented. For example: does `reference docs` collide with `/nasa-se` (which handles "reference" in a system architecture sense)? This is unverifiable without the `/diataxis` entry in the reference map.

**Correction:**

Add `/diataxis` row to the `agent-routing-standards.md` Reference Trigger Map. Document the collision analysis results (which keywords were checked, what conflicts were found, what negative keywords were added as a result).

---

## S-002 Devil's Advocate Findings

**H-16 Note:** S-003 Steelman was not applied prior to this S-002 execution. This is a constraint deviation from canonical ordering (H-16: Steelman MUST precede Devil's Advocate). The user explicitly directed this sequence (P-020 authority). S-002 proceeds as direct critique of the registration artifacts without the strengthening pass.

**Role Assumed:** Argue against the keyword selection, priority assignment, negative keyword coverage, and compound trigger design of the `/diataxis` trigger map entry.

**Assumptions Challenged:**

1. Priority 11 is the correct priority for documentation routing
2. The current keyword set provides adequate routing coverage without false positives
3. The negative keyword set adequately prevents `/diataxis` from firing on non-documentation requests
4. "howto" and "how-to" as separate entries serves a routing purpose

---

### DA-001: Priority 11 Creates Systematic Routing Failure for Mixed-Context Documentation Requests

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **File** | `mandatory-skill-usage.md` — `/diataxis` trigger map row, Priority column |
| **Strategy Step** | S-002 Step 3: Counter-argument — Unaddressed risks |

**Claim Challenged:**

Priority 11 (lowest of all 11 skills) is appropriate for documentation routing because documentation is a specialized domain.

**Counter-Argument:**

The routing algorithm in `agent-routing-standards.md` Step 3 (Numeric Priority Ordering) states: "If the highest-priority candidate is 2+ priority levels above the next: route to highest priority." This means `/problem-solving` (priority 6) beats `/diataxis` (priority 11) by 5 levels — a clear routing victory for research/analysis whenever documentation keywords co-occur with research keywords.

Consider these realistic user requests that fail to route to `/diataxis`:

- "Research the authentication patterns and **write the reference documentation**" — `research` triggers `/problem-solving` (priority 6); `reference docs` triggers `/diataxis` (priority 11). `/problem-solving` wins by 5 levels.
- "**Analyze** this codebase and **document** it" — `analyze` (priority 6) beats `document` (priority 11) by 5 levels.
- "**Investigate** the API design and create the **API docs**" — same failure mode; `API docs` isn't even in the trigger map.

The priority rationale in `agent-routing-standards.md` states: "7=`/adversary` (specialized; invoked primarily for quality assessment; highest priority number ensures it does not capture general analysis requests)." Documentation is NOT more specialized than adversarial review — it is a distinct domain users commonly invoke in analytical framing. Priority 11 makes `/diataxis` effectively unreachable via proactive routing when any analytical framing is present.

**Evidence:**

From `agent-routing-standards.md` priority ordering rationale:
- Priority 1: `/orchestration` (coordinates; must route first)
- Priority 6: `/problem-solving` (broadest scope)
- Priority 7: `/adversary` (specialized quality review)
- Priority 11: `/diataxis` (newly added — but documentation breadth exceeds adversarial review breadth)

The documented pattern is: highest priority number = "most specialized." But documentation creation is as broad a domain as research. Priority 11 breaks the H-22 proactive invocation intent for any documentation request that includes any analytical verb.

**Recommendation:**

Reassign `/diataxis` to priority 8 or 9. Add compound triggers that disambiguate pure documentation requests from mixed requests so that "write the reference documentation" (compound trigger phrase match) routes correctly even with a lower priority number. Alternatively, add `documentation` to the negative keywords of `/problem-solving` when compound triggers like "reference docs" or "write docs" are present.

**Acceptance Criteria:**

The request "analyze this module and write the reference documentation" routes to `/diataxis` (documentation outcome intended) rather than `/problem-solving` (research outcome intended). Demonstrate this routing resolution in `agent-routing-standards.md` collision analysis.

---

### DA-002: SKILL.md Activation-Keywords and Trigger Map Are Bidirectionally Inconsistent — Routing Contract Is Broken

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Files** | `skills/diataxis/SKILL.md` activation-keywords (lines 12-30) vs `mandatory-skill-usage.md` line 43 |
| **Strategy Step** | S-002 Step 3: Counter-argument — Logical flaws (inconsistency) |

**Claim Challenged:**

The SKILL.md `activation-keywords` field and the trigger map together define the routing contract for `/diataxis`.

**Counter-Argument:**

The bidirectional mismatch is more severe than it appears:

**Keywords in SKILL.md NOT in trigger map** (9 keywords — documented triggers that don't work):
`user guide`, `getting started`, `quickstart`, `API docs`, `developer guide`, `write tutorial`, `write documentation`, `how-to guide`, `document the`

**Keywords in trigger map NOT in SKILL.md** (5 keywords — trigger map functionality undiscoverable from SKILL.md):
`create documentation`, `classify documentation`, `audit documentation`, `quadrant`, `doc type`

The `activation-keywords` field in SKILL.md is the machine-readable routing contract used by the system. The `mandatory-skill-usage.md` trigger map is the actual routing mechanism. When these diverge, the routing contract is broken in both directions: users cannot rely on SKILL.md to know what triggers the skill, and the trigger map has undocumented coverage that nobody maintains.

**Evidence:**

SKILL.md `description` field: "Triggers: documentation, tutorial, how-to, howto, reference docs, explanation, diataxis, write docs, **user guide, getting started, quickstart, API docs**."

These last four keywords are in the description contract but absent from the trigger map. A user who reads "write a user guide" and expects `/diataxis` to activate proactively will be routed elsewhere.

**Recommendation:**

Establish a canonical single-source-of-truth for trigger keywords. The `activation-keywords` field in SKILL.md should be the SSOT; the trigger map's Detected Keywords column should be derived from it. Add all SKILL.md activation-keywords to the trigger map, or document explicit exclusions with rationale.

**Acceptance Criteria:**

All keywords listed in SKILL.md `activation-keywords` appear in the trigger map's Detected Keywords column (or are explicitly documented as excluded with routing rationale).

---

### DA-003: Missing Negative Keywords Create False-Positive Routing into `/diataxis`

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **File** | `mandatory-skill-usage.md` — `/diataxis` trigger map row, Negative Keywords column |
| **Strategy Step** | S-002 Step 3: Counter-argument — Unaddressed risks |

**Claim Challenged:**

Current negative keywords (`adversarial, tournament, transcript, penetration, exploit`) are sufficient to prevent `/diataxis` from firing on non-documentation requests.

**Counter-Argument:**

The five current negative keywords suppress only narrow security/adversarial contexts. They fail to prevent false-positive routing in these realistic scenarios:

1. **"Create the requirements documentation"** — Contains `documentation` (positive match). Not suppressed. Routes to `/diataxis`; should route to `/nasa-se`. Requirements documentation is NOT Diataxis documentation production.

2. **"Write the API security requirements documentation"** — Contains `documentation` (positive). `security` and `requirements` are not negative keywords. Routes to `/diataxis`; should route to `/nasa-se` or `/eng-team`.

3. **"Document the code review findings"** — Contains `document` (edge case via "document this"? unclear). `code review` is not a negative keyword. May route to `/diataxis`; should route to `/problem-solving` or `/adversary`.

4. **"Write documentation standards for the project"** — Contains `documentation` (positive). `standards` is not a negative keyword. This is a governance/framework task, not Diataxis documentation production.

Compare: `/nasa-se` has negative keywords `root cause, debug, adversarial, tournament, research (standalone), transcript` protecting it from research/debugging contexts. No reciprocal protection exists preventing `/diataxis` from invading `/nasa-se`'s domain when "documentation" appears alongside requirements work.

**Evidence:**

Current negative keywords: `adversarial, tournament, transcript, penetration, exploit`

Compare `/nasa-se` negative keywords: `root cause, debug, adversarial, tournament, research (standalone), transcript` — these protect `/nasa-se` from contamination but do not protect its domain from `/diataxis` invasion.

**Recommendation:**

Add these negative keywords to `/diataxis`:
- `requirements` — suppresses "requirements documentation" routing to `/nasa-se`
- `specification` — suppresses "specification documentation" routing to `/nasa-se`
- `code review` — suppresses "document the code review findings" routing to `/problem-solving`/`/adversary`

Also add `documentation` to `/nasa-se` negative keywords when compound triggers like "requirements specification" or "system design" are present, to prevent `/diataxis` from capturing technical writing that isn't Diataxis-typed documentation.

**Acceptance Criteria:**

- "Create the API requirements documentation" does NOT route to `/diataxis`
- "Write API reference documentation" DOES route to `/diataxis`
- "Document the system architecture" does NOT route to `/diataxis` (routes to `/nasa-se`)

---

### DA-004: Redundant `howto` and `how-to` Keyword Entries — Bag of Triggers Anti-Pattern Risk

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **File** | `mandatory-skill-usage.md` — `/diataxis` trigger map row, Detected Keywords column |
| **Strategy Step** | S-002 Step 3: Counter-argument — Logical flaws |

**Evidence:**

Trigger map Detected Keywords: `documentation, tutorial, **how-to**, **howto**, reference docs, explanation, ...`

Both `how-to` and `howto` appear. These represent the same concept.

**Counter-Argument:**

`agent-routing-standards.md` documents AP-02 (Bag of Triggers): "Keywords added without collision analysis. Multiple skills match with no conflict resolution." While having both hyphenated and unhyphenated forms provides defensive keyword coverage, it also adds noise to the trigger map and could mask future collision analysis work. If this is intentional, it should be documented (SKILL.md explicitly lists both in `activation-keywords`, suggesting it is intentional). If undocumented, it is an unacknowledged exception to AP-02 avoidance.

**Recommendation:**

Add a comment or footnote in the trigger map noting that `how-to` and `howto` are both retained intentionally to catch alternate user spellings of "how-to guide." This satisfies the documentation requirement without removing either keyword.

---

## S-010 Self-Refine Recommendations

**Objectivity Assessment:** This agent is the reviewer, not the creator. No attachment to the registration artifacts. Proceeding without bias.

**Self-Critique of Findings Quality:**

After reviewing all findings generated by S-007, S-011, and S-002, the following meta-observations are noted:

1. CC-001 and CV-001 are related: the `allowed-tools` invalid field name (CC-001) and the activation-keywords mismatch (CV-001) both stem from SKILL.md being out of sync with the authoritative standards. These should be addressed together in a single SKILL.md revision pass.

2. DA-001 (priority 11) and DA-003 (missing negative keywords) are compensating mechanisms for each other. If priority is raised (DA-001), fewer negative keywords are needed because the routing algorithm resolves conflicts earlier. If priority stays at 11, more aggressive negative keywords (DA-003) are essential to prevent routing loss. The remediation plan should treat these as linked.

3. DA-002 and CV-001 are the same root finding expressed from different strategies (logical inconsistency vs. factual discrepancy). This strengthens the Major severity classification — two independent methods converge on the same gap.

4. CC-002 and CV-002 are also the same root finding: `agent-routing-standards.md` reference map is incomplete. Single fix resolves both.

---

### SR-001: SKILL.md `description` Trigger List Creates False Routing Contract — P-022 Implication

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **File** | `skills/diataxis/SKILL.md` frontmatter `description` field (lines 3-10) |
| **Strategy Step** | S-010 Step 2: Systematic self-critique — P-022 (no deception) implication |

**Evidence:**

The `description` YAML frontmatter field states:
```
Triggers: documentation, tutorial, how-to, howto, reference docs,
explanation, diataxis, write docs, user guide, getting started, quickstart, API docs.
```

Keywords `user guide`, `getting started`, `quickstart`, and `API docs` do NOT appear in the operational trigger map in `mandatory-skill-usage.md`.

**Analysis:**

The `description` field is used by Claude Code for agent routing and is displayed during skill discovery. A user reading this description to understand when to use `/diataxis` will believe "user guide" and "getting started" activate it proactively. They do not. This represents a documented routing contract that does not match actual runtime behavior — a P-022 (no deception) concern, though passive rather than active deception.

**Recommendation:**

Update the `description` field Triggers list to include ONLY keywords that appear in the operational trigger map. This ensures the documented contract matches the implemented behavior. This finding is resolved by the same fix as DA-002/CV-001 (synchronizing keywords).

---

## Finding Summary Table

| # | Severity | Finding | Location | Recommendation |
|---|----------|---------|----------|----------------|
| CC-001 | **Critical** | `allowed-tools` is invalid YAML field — silently ignored by Claude Code; tool access constraints for 6 diataxis agents unenforced | `skills/diataxis/SKILL.md` line 11 | Replace `allowed-tools` with `tools` (list format) |
| CC-002 | **Major** | `agent-routing-standards.md` Reference Trigger Map missing `/diataxis` — collision analysis unverifiable, reference SSOT out of sync | `.context/rules/agent-routing-standards.md` Enhanced Trigger Map | Add `/diataxis` row with collision analysis documented |
| CV-001 | **Major** | SKILL.md activation-keywords (9 keywords) not in trigger map — routing contract broken; "user guide", "getting started", "quickstart", "API docs" advertised as triggers but non-functional | `SKILL.md` vs `mandatory-skill-usage.md` | Add missing keywords to trigger map OR remove from SKILL.md with rationale |
| DA-001 | **Major** | Priority 11 (lowest) causes systematic routing failure when documentation requests include any analytical verb (research, analyze, investigate) — `/problem-solving` always wins | `mandatory-skill-usage.md` priority column | Reassign to priority 8-9; add compound triggers for pure documentation requests |
| DA-002 | **Major** | Bidirectional keyword mismatch: SKILL.md and trigger map have different keyword sets; no single source of truth | `SKILL.md` + `mandatory-skill-usage.md` | Establish SKILL.md as SSOT; derive trigger map from it |
| DA-003 | **Major** | Missing negative keywords: `requirements`, `specification` allow `/diataxis` to capture requirements documentation, design documentation that should route to `/nasa-se` | `mandatory-skill-usage.md` negative keywords column | Add `requirements, specification` (and consider `code review`) as negative keywords |
| DA-004 | **Minor** | `howto` and `how-to` both present — intentional defensive coverage but undocumented; creates Bag of Triggers anti-pattern risk | `mandatory-skill-usage.md` detected keywords | Add comment documenting intentional dual-spelling coverage |
| CV-002 | **Minor** | Collision analysis for `/diataxis` keywords unverifiable from authoritative reference; RT-M-004 compliance cannot be confirmed | `.context/rules/agent-routing-standards.md` | Resolved by CC-002 fix (add `/diataxis` to reference map with collision notes) |
| SR-001 | **Minor** | `description` field advertises 4 trigger keywords not in operational trigger map — passive P-022 concern (false routing contract) | `skills/diataxis/SKILL.md` description frontmatter | Resolved by DA-002/CV-001 fix (synchronize keyword lists) |

---

## Remediation Plan

### P0 — Critical (MUST fix before acceptance)

**CC-001:** Fix `allowed-tools` -> `tools` in `skills/diataxis/SKILL.md`.
- File: `skills/diataxis/SKILL.md` line 11
- Change: `allowed-tools: Read, Write, Edit, Glob, Grep, Bash` -> `tools:` + YAML list
- Verification: Confirm field name against 12 official Claude Code frontmatter fields

### P1 — Major (SHOULD fix; justification required if not)

**CC-002 + CV-002:** Add `/diataxis` row to `agent-routing-standards.md` Reference Trigger Map with collision analysis.
- File: `.context/rules/agent-routing-standards.md` Enhanced Trigger Map section
- Add: Full 5-column row for `/diataxis` matching `mandatory-skill-usage.md` entry
- Add: Priority ordering rationale note explaining priority 11 choice (or revised priority)

**CV-001 + DA-002 + SR-001:** Synchronize SKILL.md activation-keywords with trigger map.
- Establish SKILL.md `activation-keywords` as SSOT
- Add to `mandatory-skill-usage.md` trigger map: `user guide, getting started, quickstart, API docs, developer guide, write tutorial, write documentation, how-to guide`
- Update SKILL.md `description` Triggers line to match operational trigger map exactly
- Verification: Every SKILL.md activation-keyword has a corresponding trigger map entry

**DA-001:** Reassign `/diataxis` priority from 11 to 8 or 9.
- File: `mandatory-skill-usage.md` — `/diataxis` trigger map row Priority column
- Add compound triggers for pure documentation requests to ensure correct routing at new priority
- Update `agent-routing-standards.md` priority ordering rationale comment
- Acceptance test: "analyze this module and write the reference documentation" routes to `/diataxis`

**DA-003:** Add negative keywords `requirements, specification` to `/diataxis` trigger map row.
- File: `mandatory-skill-usage.md` — `/diataxis` row, Negative Keywords column
- Change: `adversarial, tournament, transcript, penetration, exploit` -> `requirements, specification, adversarial, tournament, transcript, penetration, exploit`
- Acceptance test: "create the API requirements documentation" does NOT route to `/diataxis`

### P2 — Minor (MAY fix; acknowledgment sufficient)

**DA-004:** Document that `howto`/`how-to` dual entries are intentional defensive keyword coverage.

---

## Constitutional Compliance Score

| Severity | Count | Penalty |
|----------|-------|---------|
| Critical | 1 | 1 × (-0.10) = -0.10 |
| Major | 5 | 5 × (-0.05) = -0.25 |
| Minor | 3 | 3 × (-0.02) = -0.06 |

**Score:** 1.00 - 0.41 = **0.59 — REJECTED** (below 0.85 floor; well below 0.92 target and 0.95 specified threshold)

**Note:** Penalty model uses S-007 template operational values (Critical: -0.10, Major: -0.05, Minor: -0.02). Authoritative threshold of 0.92 for C2+ deliverables is from `quality-enforcement.md`. The 0.95 threshold specified by the user is stricter; this registration does not approach it in its current state.

**Threshold Determination:** REJECTED. The 1 Critical finding alone drives the score below any passing band. The 5 Major findings — forming a coherent cluster around routing quality gaps — constitute a systemic concern rather than isolated defects.

---

## Execution Statistics

- **Total Findings:** 9
- **Critical:** 1
- **Major:** 5
- **Minor:** 3
- **Protocol Steps Completed:**
  - S-007: 5 of 5 steps
  - S-011: 5 of 5 steps; 10 claims extracted; 8 verified, 1 material discrepancy (CV-001), 1 unverifiable (CV-002)
  - S-002: 5 of 5 steps (H-16 waiver per P-020 user authority; S-003 Steelman not run prior)
  - S-010: 6 of 6 steps
- **Compliance Status:** REJECTED (score 0.59 — requires P0 and P1 remediation before re-review)

---

*Report generated by adv-executor*
*Strategies executed: S-007, S-011, S-002, S-010*
*Finding prefixes: CC-NNN (S-007), CV-NNN (S-011), DA-NNN (S-002), SR-NNN (S-010)*
*Templates: `.context/templates/adversarial/s-007-constitutional-ai.md`, `s-011-cove.md`, `s-002-devils-advocate.md`, `s-010-self-refine.md`*
*SSOT: `.context/rules/quality-enforcement.md`*
*Date: 2026-02-27*
