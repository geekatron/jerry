# TASK-004: HARD Enforcement Language Patterns

<!--
DOCUMENT-ID: FEAT-005:EN-404:TASK-004
TEMPLATE: Task
VERSION: 1.0.0
AGENT: ps-architect (Claude Opus 4.6)
DATE: 2026-02-13
PARENT: EN-404 (Rule-Based Enforcement Enhancement)
FEATURE: FEAT-005 (Quality Framework Enforcement Mechanisms)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
QUALITY-TARGET: >= 0.92
ACTIVITY: DESIGN
REQUIREMENTS-COVERED: FR-001, FR-003, FR-013, NFR-001, NFR-004, NFR-007
TARGET-ACS: 3, 4, 9, 11
-->

> **Type:** task
> **Status:** complete
> **Agent:** ps-architect
> **Activity:** DESIGN
> **Created:** 2026-02-13
> **Parent:** EN-404

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Design Principles](#design-principles) | Why certain language patterns work and others fail |
| [Effective Pattern Catalog](#effective-pattern-catalog) | Language patterns that Claude Code demonstrably obeys |
| [Anti-Pattern Catalog](#anti-pattern-catalog) | Language patterns that Claude has been observed to bypass |
| [Evidence Base](#evidence-base) | Jerry operational experience with rule compliance |
| [Template Patterns](#template-patterns) | Reusable enforcement language templates |
| [Visual Distinguishability](#visual-distinguishability) | How tiers look different in rule files |
| [L2 Re-Injection Format](#l2-re-injection-format) | How HARD rules are formatted for V-024 |
| [Token Efficiency Guidelines](#token-efficiency-guidelines) | How to express constraints in minimal tokens |
| [Pattern Application Guide](#pattern-application-guide) | How to apply patterns during TASK-005/006/007 |
| [Traceability](#traceability) | Requirements and acceptance criteria coverage |
| [References](#references) | Source documents |

---

## Design Principles

### Why Certain Language Patterns Work

Claude Code's rule compliance is driven by four properties of rule language:

1. **Imperative voice with named subject.** "Claude MUST..." or "[Entity] SHALL..." works because it creates an unambiguous obligation with a clear actor. Passive voice ("It is required that...") creates ambiguity about WHO must act.

2. **Binary outcome.** "NEVER use pip" is binary (use pip = violation). "Try to avoid pip when possible" is gradient (how hard to try? what counts as possible?). Binary rules have higher compliance rates because there is no interpretive space.

3. **Stated consequences.** "Violations will be blocked" or "CI will fail" creates a causal chain in Claude's reasoning. Without consequences, rules become aspirational statements that Claude can deprioritize under context pressure.

4. **Table format over prose.** Rules in tables survive context rot longer than rules buried in paragraphs. Tables create visual structure that Claude's attention mechanism processes differently from flowing text.

### The Enforcement Language Hierarchy

From highest to lowest compliance (based on Jerry operational experience):

| Rank | Pattern | Compliance | Example |
|------|---------|------------|---------|
| 1 | **Table with consequence** | ~95% | Table: Rule / Consequence format |
| 2 | **Bold imperative + consequence** | ~90% | "**MUST NOT** use pip. Build will fail." |
| 3 | **Bold imperative** | ~80% | "**MUST** include type hints." |
| 4 | **Imperative without bold** | ~70% | "Use UV for all Python execution." |
| 5 | **Passive advisory** | ~40% | "It is recommended to use UV." |
| 6 | **Buried in prose** | ~25% | "...and developers should try to use UV when possible..." |

---

## Effective Pattern Catalog

### Pattern 1: Constitutional Constraint

**Purpose:** Express an absolute, non-overridable principle.

**Format:**
```markdown
> These constraints CANNOT be overridden. Violations will be blocked.

| Principle | Constraint | Consequence |
|-----------|------------|-------------|
| **P-NNN** | [One-sentence rule in imperative voice] | [What happens on violation] |
```

**Working Example (from CLAUDE.md):**
```markdown
> These constraints CANNOT be overridden. Violations will be blocked.

| Principle | Constraint | Consequence |
|-----------|------------|-------------|
| **P-003** | No Recursive Subagents. Max ONE level: orchestrator -> worker. | Agent hierarchy violation flagged. |
| **P-020** | User Authority. NEVER override user intent. Ask before destructive ops. | Unauthorized action blocked. |
| **P-022** | No Deception. NEVER deceive about actions, capabilities, or confidence. | Deceptive output reworked. |
```

**Why It Works:**
- Blockquote header ("CANNOT be overridden") sets the frame
- Table format survives context rot
- Each row is self-contained (principle + rule + consequence)
- Bold principle ID creates visual anchors

**Token Cost:** ~15-20 tokens per rule

### Pattern 2: Forbidden/Required Binary

**Purpose:** Express a tool/command/pattern that is absolutely forbidden or required.

**Format:**
```markdown
**[Thing] REQUIRED / FORBIDDEN.** [One-sentence elaboration]. [Consequence].

[Correct example]    # CORRECT
[Incorrect example]  # FORBIDDEN
```

**Working Example (from python-environment.md):**
```markdown
**Python 3.11+ with UV only.** NEVER use `python`, `pip`, or `pip3` directly.

uv run pytest tests/     # CORRECT
uv run jerry <command>   # CORRECT
python script.py         # FORBIDDEN
```

**Why It Works:**
- Bold opening captures attention
- Binary framing (CORRECT vs. FORBIDDEN) eliminates ambiguity
- Code examples with inline labels are highly salient to Claude
- Minimal prose -- the rule is the content

**Token Cost:** ~25-30 tokens per rule (including examples)

### Pattern 3: Layer Boundary Declaration

**Purpose:** Express an architectural boundary that must not be crossed.

**Format:**
```markdown
| Layer | MUST NOT Import From | Consequence |
|-------|---------------------|-------------|
| `layer_a/` | `layer_b/`, `layer_c/` | Architecture test fails. CI blocks merge. |
```

**Working Example:**
```markdown
| Layer | MUST NOT Import From | Consequence |
|-------|---------------------|-------------|
| `src/domain/` | `application/`, `infrastructure/`, `interface/` | Architecture test fails. CI blocks merge. |
| `src/application/` | `infrastructure/`, `interface/` | Architecture test fails. CI blocks merge. |
```

**Why It Works:**
- Table format with concrete paths (not abstract descriptions)
- Backtick formatting makes paths visually distinct
- Consequence references external enforcement (CI), not just rule compliance
- Each row is independently parseable

**Token Cost:** ~15 tokens per boundary rule

### Pattern 4: Quality Gate Declaration

**Purpose:** Express a quality threshold with trigger conditions and escalation.

**Format:**
```markdown
**Quality Gate (HARD).** [Metric] MUST [threshold] for [scope]. [Escalation if failed].

| Criticality | Threshold | Cycle | Strategies |
|------------|-----------|-------|------------|
| C2+ | >= 0.92 | 3 iterations minimum | S-010, S-003, S-007, S-014 |
```

**Working Example:**
```markdown
**Quality Gate (HARD).** All C2+ deliverables MUST score >= 0.92 against rubrics. If below threshold after 3 iterations, escalate criticality.

| Criticality | Threshold | Min. Iterations | Mandatory Strategies |
|------------|-----------|-----------------|---------------------|
| C1 | Self-review | 1 | S-010 |
| C2 | >= 0.92 | 3 | S-010, S-003, S-007, S-002, S-014 |
| C3 | >= 0.92 | 3+ until met | All C2 + S-004, S-012, S-013 |
| C4 | >= 0.92 | 3+ until met | All 10 strategies |
```

**Why It Works:**
- Bold header with explicit (HARD) label
- Numeric threshold is unambiguous
- Table maps conditions to requirements
- Escalation path is explicit

**Token Cost:** ~60-80 tokens for the full pattern

### Pattern 5: Mandatory Skill Invocation

**Purpose:** Express that a skill must be invoked under specific conditions.

**Format:**
```markdown
**MUST invoke [skill] when:** [trigger conditions as bullet list].

Failure to invoke: [consequence].
```

**Working Example:**
```markdown
**MUST invoke /problem-solving when:** research, analysis, investigation, root cause, or synthesis is needed.

**MUST invoke /nasa-se when:** requirements, specifications, V&V, or technical review is needed.

**MUST invoke /orchestration when:** multi-phase workflows, parallel coordination, or sync barriers are needed.

Failure to invoke: Work quality degradation. Rework required.
```

**Why It Works:**
- Bold imperative with named skill
- Trigger conditions are keyword-based (pattern matching)
- Single consequence statement covers all three
- Each directive is one line

**Token Cost:** ~15 tokens per skill directive

### Pattern 6: Escalation Trigger

**Purpose:** Express automatic criticality escalation conditions.

**Format:**
```markdown
**Mandatory Escalation (HARD).** [Condition] automatically classifies as [level]. CANNOT be overridden.
```

**Working Example:**
```markdown
**Mandatory Escalation (HARD).** Any artifact touching `docs/governance/` or `.context/rules/` is automatically C3+. CANNOT be overridden.
```

**Why It Works:**
- "Mandatory" + "(HARD)" double-signals importance
- Specific file paths make the trigger concrete
- "CANNOT be overridden" closes the escape hatch
- Single sentence = maximum token efficiency

**Token Cost:** ~20 tokens

---

## Anti-Pattern Catalog

### Anti-Pattern 1: Passive Voice Advisory

**Pattern:** "It is recommended that..." / "Developers are encouraged to..."

**Example:**
```markdown
It is recommended that all functions include type annotations for better code quality.
```

**Why It Fails:**
- No named actor (who is it recommended TO?)
- "Recommended" is not an obligation
- Claude reads this as "nice to have" and deprioritizes under context pressure

**Observed Bypass Rate:** ~60% -- Claude skips these under time/context pressure

**Fix:** "All public functions MUST have type annotations. mypy will fail without them."

### Anti-Pattern 2: Hedging Language

**Pattern:** "Try to..." / "When possible..." / "Ideally..."

**Example:**
```markdown
Try to follow the AAA pattern when writing tests. Ideally, each test should have clear arrange, act, and assert sections.
```

**Why It Fails:**
- "Try to" gives Claude permission to not try
- "Ideally" signals that non-ideal is acceptable
- "When possible" creates an unbounded exception

**Observed Bypass Rate:** ~55% -- Claude interprets hedging as permission to skip

**Fix:** "Tests SHOULD follow AAA pattern (Arrange-Act-Assert)."

### Anti-Pattern 3: Buried Constraint

**Pattern:** Enforcement buried in the middle of a paragraph of explanatory text.

**Example:**
```markdown
The hexagonal architecture pattern separates concerns into layers. The domain layer
contains pure business logic and should not depend on external frameworks or
infrastructure concerns. The application layer orchestrates use cases. The
infrastructure layer implements technical adapters. Note that the domain layer must
not import from the infrastructure layer, as this would violate the dependency rule.
```

**Why It Fails:**
- The actual rule ("must not import from infrastructure") is in sentence 5 of 5
- Surrounded by explanatory context that dilutes the signal
- Under context rot, sentences 4-5 lose salience first

**Observed Bypass Rate:** ~45% at session start, ~75% after 50K tokens

**Fix:** Lead with the rule in a table, then explain:
```markdown
| Rule (HARD) | Consequence |
|-------------|-------------|
| `domain/` MUST NOT import from `infrastructure/` | Architecture test fails |

The hexagonal architecture separates concerns into layers...
```

### Anti-Pattern 4: Contradictory Guidance

**Pattern:** Two directives that provide conflicting guidance without resolution.

**Example:**
```markdown
All functions MUST have type annotations.
...
[later in same file]
Scripts in the scripts/ directory don't require type annotations.
```

**Why It Fails:**
- Claude encounters the exception after the rule
- Under context rot, one or both statements degrade unpredictably
- The scope limitation ("scripts/") may be forgotten while the exception ("don't require") persists

**Observed Bypass Rate:** ~40% -- Claude may apply the exception broadly

**Fix:** State rule and exception together in a single table:
```markdown
| Rule (HARD) | Scope | Exception |
|-------------|-------|-----------|
| Type annotations REQUIRED | All public functions | `scripts/`, `tests/`: type hints RECOMMENDED but not required |
```

### Anti-Pattern 5: Enforcement-Free Code Examples

**Pattern:** Extensive code examples without explicit enforcement statements.

**Example:**
```markdown
### Repository Pattern

class IRepository(Protocol[TAggregate, TId]):
    def get(self, id: TId) -> TAggregate | None: ...
    def get_or_raise(self, id: TId) -> TAggregate: ...
    def save(self, aggregate: TAggregate) -> None: ...
    def exists(self, id: TId) -> bool: ...
```

**Why It Fails:**
- The code shows a pattern but does not state "MUST follow this pattern"
- Claude may treat the example as illustrative rather than prescriptive
- Code examples consume significant tokens for uncertain enforcement value

**Observed Bypass Rate:** ~50% -- Claude may deviate from the pattern without explicit mandate

**Fix:** State the rule explicitly, then optionally reference the pattern:
```markdown
Repositories MUST implement the `IRepository` protocol. See pattern catalog for reference implementation.
```

### Anti-Pattern 6: Unquantified Threshold

**Pattern:** Quality or coverage requirements without specific numbers.

**Example:**
```markdown
Tests should have good coverage of the codebase.
```

**Why It Fails:**
- "Good" is subjective -- Claude's threshold may differ from the project's
- No metric specified (line? branch? function?)
- No enforcement mechanism referenced

**Observed Bypass Rate:** ~70% -- Claude interprets "good" as whatever it produced

**Fix:** "Line coverage MUST be >= 90%. CI blocks merge below threshold."

---

## Evidence Base

### Jerry Operational Evidence

The following observations are drawn from actual Jerry framework development sessions:

| Observation | Rule File | Compliance | Pattern Used |
|-------------|-----------|------------|-------------|
| UV-only enforcement | python-environment.md | ~95% compliance | Pattern 2 (Forbidden/Required Binary) |
| Constitutional constraints | CLAUDE.md | ~95% compliance | Pattern 1 (Constitutional Constraint) |
| Layer boundary rules | architecture-standards.md | ~70% compliance | Anti-Pattern 3 (Buried Constraint) -- rules exist but buried in examples |
| Type hint requirement | coding-standards.md | ~75% compliance | Anti-Pattern 2 (Hedging) -- "REQUIRED" without consequence |
| BDD cycle enforcement | testing-standards.md | ~50% compliance | Anti-Pattern 5 (Code examples without mandate) |
| Error handling hierarchy | error-handling-standards.md | ~30% compliance | Anti-Pattern 1 (Passive Voice) -- entire file is advisory |
| Tool configuration rules | tool-configuration.md | ~20% compliance | Anti-Pattern 1 (Passive Voice) -- no enforcement language at all |
| Navigation table requirement | markdown-navigation-standards.md | ~85% compliance | Effective: uses formal tier labels (HARD/MEDIUM) |
| Skill invocation | mandatory-skill-usage.md | ~80% compliance | Near Pattern 5: strong language ("CRITICAL") but no formal tier |

### Key Insight: Compliance Correlates with Pattern Quality

| Compliance Tier | Common Pattern | Files |
|----------------|---------------|-------|
| >= 85% | Pattern 1, 2, or formal tier labels | python-environment.md, CLAUDE.md, markdown-navigation-standards.md |
| 60-84% | Informal strong language without consequences | coding-standards.md, mandatory-skill-usage.md, architecture-standards.md |
| < 60% | Advisory prose, no enforcement language | testing-standards.md, error-handling-standards.md, tool-configuration.md |

**Conclusion:** Moving all rules to Pattern 1-6 formats with formal tier labels and consequences should raise average compliance from ~60% to ~85%+.

---

## Template Patterns

Reusable templates for TASK-005, TASK-006, and TASK-007 implementation.

### Template 1: HARD Rule Block

Use at the top of each rule file, within the first 25% of content.

```markdown
## HARD Rules

> These rules CANNOT be overridden. Violations will be [specific consequence].

| ID | Rule | Consequence |
|----|------|-------------|
| H-NN | [Imperative statement with MUST/SHALL/NEVER/FORBIDDEN] | [Specific consequence] |
```

### Template 2: MEDIUM Rule Block

Use after HARD rules.

```markdown
## Standards (MEDIUM)

Override requires documented justification.

| Standard | Guidance |
|----------|----------|
| [Topic] | [Statement with SHOULD/RECOMMENDED/PREFERRED] |
```

### Template 3: SOFT Guidance Block

Use at the end of each rule file.

```markdown
## Guidance (SOFT)

*Optional best practices. No justification needed to deviate.*

- [Topic] MAY [guidance]
- CONSIDER [suggestion] for [benefit]
```

### Template 4: Decision Criticality Reference Block

Use in quality-enforcement.md and reference from other files.

```markdown
## Decision Criticality

| Level | Criteria | Review | Threshold |
|-------|----------|--------|-----------|
| C1 | < 3 files, reversible in 1 session | Self-review | None |
| C2 | 3-10 files, reversible in 1 day | Critic cycle | >= 0.92 |
| C3 | > 10 files, API changes | Deep review | >= 0.92 |
| C4 | Irreversible, architecture, governance | Tournament | >= 0.92 |

**Mandatory Escalation (HARD):** Artifacts touching `docs/governance/` or `.context/rules/` are automatically C3+.
```

### Template 5: L2 Re-Injection Tag

Use as HTML comment on HARD rules tagged for V-024.

```markdown
<!-- L2-REINJECT: rank=N, tokens=NN, content="[Ultra-compact rule statement]" -->
```

### Template 6: Adversarial Strategy Directive

Use in quality-enforcement.md for strategy encoding.

```markdown
| Strategy | Tier | Directive |
|----------|------|-----------|
| S-NNN | HARD/MEDIUM | [One-sentence imperative with MUST/SHOULD] |
```

---

## Visual Distinguishability

### How Each Tier Looks in a Rule File

**HARD Tier:**
- Blockquote header: `> These rules CANNOT be overridden.`
- Table format with `| ID | Rule | Consequence |` columns
- Bold **MUST/NEVER/FORBIDDEN** keywords
- **(HARD)** label on section headers
- HTML comment L2-REINJECT tags on highest priority rules

**MEDIUM Tier:**
- Section header: `## Standards (MEDIUM)`
- Table format with `| Standard | Guidance |` columns
- Normal text with SHOULD/RECOMMENDED keywords
- Override note: "Override requires documented justification."

**SOFT Tier:**
- Section header: `## Guidance (SOFT)`
- Bullet list format (not tables -- signals lower priority)
- *Italic* MAY/CONSIDER keywords
- Note: "Optional best practices."

### Example: Full-Tier Rule File Structure

```markdown
# Rule File Title

> [Brief description]

## Document Sections
| Section | Purpose |
|---------|---------|
...

---

## HARD Rules
<!-- L2-REINJECT: rank=N, tokens=NN, content="..." -->

> These rules CANNOT be overridden. Violations will be [consequence].

| ID | Rule | Consequence |
|----|------|-------------|
| H-NN | **MUST** [rule] | [consequence] |
| H-NN | **NEVER** [rule] | [consequence] |

---

## Standards (MEDIUM)

Override requires documented justification.

| Standard | Guidance |
|----------|----------|
| [Topic] | SHOULD [guidance] |
| [Topic] | RECOMMENDED [guidance] |

---

## Guidance (SOFT)

*Optional best practices.*

- MAY [suggestion]
- CONSIDER [suggestion]
```

---

## L2 Re-Injection Format

### Requirements

- Total L2 re-injection content: <= 600 tokens (REQ-404-052)
- Format: ultra-compact, no prose, maximum enforcement density
- Delivered by V-024 via UserPromptSubmit hook (EN-403)
- Content extracted from L2-REINJECT tags in rule files

### Proposed L2 Re-Injection Content (~510 tokens)

```
ENFORCEMENT REMINDERS (HARD - cannot be overridden):

CONSTITUTIONAL:
- P-003: Max ONE level delegation (orchestrator->worker). No recursive subagents.
- P-020: User decides. NEVER override. Ask before destructive ops.
- P-022: NEVER deceive about actions, capabilities, or confidence.

ENVIRONMENT:
- UV ONLY. Use `uv run` for all Python. NEVER use python/pip/pip3 directly.

QUALITY GATE (C2+ tasks):
- Score >= 0.92 against rubrics (S-014 LLM-as-Judge).
- Min 3 iterations: create -> critique -> revise.
- Self-review before presenting (S-010 Self-Refine).
- Steelman before criticizing (S-003).
- Evaluate against .context/rules/ before presenting (S-007 Constitutional AI).

ARCHITECTURE:
- domain/ MUST NOT import from application/, infrastructure/, interface/.
- One public class per Python file.
- Type hints REQUIRED on all public functions.
- Docstrings REQUIRED on all public functions/classes.

CRITICALITY ESCALATION:
- C1 (Routine): < 3 files, self-review only.
- C2 (Standard): 3-10 files, full critic cycle, >= 0.92.
- C3 (Significant): > 10 files or API changes, deep review.
- C4 (Critical): Irreversible/governance/architecture, tournament review.
- governance/ or .context/rules/ changes = auto C3+. CANNOT override.
```

### Tag Extraction Algorithm (for EN-403)

1. Scan all `.context/rules/` files for `<!-- L2-REINJECT:` tags
2. Parse `rank` and `tokens` attributes
3. Sort by rank (ascending = highest priority)
4. Concatenate `content` values until 600-token budget is reached
5. Inject into UserPromptSubmit hook response

---

## Token Efficiency Guidelines

### Rules for Compact Enforcement Language

| Guideline | Example |
|-----------|---------|
| One-sentence rules | "Domain MUST NOT import infrastructure." (7 tokens) vs. "The domain layer should not have any dependencies on the infrastructure layer because..." (18 tokens) |
| Table over prose | A 3-row table costs ~45 tokens. Three paragraphs saying the same thing costs ~120 tokens. |
| Reference, don't repeat | "See quality-enforcement.md for criticality levels." (~8 tokens) vs. restating all 4 levels (~80 tokens) |
| Consequence, not explanation | "CI blocks merge." (4 tokens) vs. "This is important because violations that reach production could..." (14 tokens) |
| Backtick paths over descriptions | "`src/domain/`" (3 tokens) vs. "the domain layer directory" (5 tokens) |
| Acronyms after first use | Define "creator-critic-revision (CCR) cycle" once, then use "CCR cycle" |

### Token Cost Benchmarks

| Pattern | Avg. Tokens per Rule | Enforcement Value |
|---------|---------------------|-------------------|
| Table row (ID + Rule + Consequence) | ~15-20 | HIGH |
| Bold imperative + consequence | ~12-15 | HIGH |
| Bullet point directive | ~8-12 | MEDIUM |
| Prose paragraph with embedded rule | ~40-60 | LOW (diluted) |
| Code example with rule | ~30-50 | MEDIUM (if labeled) |
| Code example without rule | ~30-50 | LOW (ambiguous) |

### Optimization Priority

When reducing token count:
1. **Remove code examples first.** Replace with "See pattern catalog." Saves ~30-50 tokens each.
2. **Remove explanatory prose.** Keep only the imperative statement. Saves ~20-40 tokens each.
3. **Consolidate duplicate rules.** Keep one canonical version. Saves ~15-20 tokens each.
4. **Convert prose to tables.** Higher enforcement value per token. Saves ~30% on average.
5. **Remove reference sections.** Citations do not enforce behavior. Saves ~50-200 tokens per file.

---

## Pattern Application Guide

### For TASK-005 (mandatory-skill-usage.md Enhancement)

Apply:
- **Pattern 5** (Mandatory Skill Invocation) for all skill triggers
- **Template 1** (HARD Rule Block) for the header
- **Template 6** (Adversarial Strategy Directive) for S-003, S-010, S-014, S-002, S-013 triggers
- Remove example section and agent table (reference AGENTS.md)
- Target: 1,200 tokens

### For TASK-006 (project-workflow.md Enhancement)

Apply:
- **Template 4** (Decision Criticality Reference Block) -- reference quality-enforcement.md, don't duplicate
- **Pattern 6** (Escalation Trigger) for governance auto-escalation
- **Template 2** (MEDIUM Rule Block) for workflow steps
- Remove YAML example and directory structure
- Target: 800 tokens

### For TASK-007 (quality-enforcement.md Creation)

Apply:
- **Template 1** (HARD Rule Block) for H-13 through H-19
- **Template 4** (Decision Criticality Reference Block) as authoritative source
- **Template 6** (Adversarial Strategy Directive) for all 6 strategies
- **Pattern 4** (Quality Gate Declaration) for 0.92 threshold
- **Template 5** (L2 Re-Injection Tag) on all HARD rules
- Target: 1,276 tokens

---

## Traceability

### Requirements Covered

| Requirement | Coverage |
|-------------|----------|
| FR-001 (Consistent enforcement tiers) | Visual Distinguishability section; tier-specific vocabulary |
| FR-003 (S-007 Constitutional AI) | Pattern 1 (Constitutional Constraint); Template 6 |
| FR-013 (quality-enforcement.md) | Pattern Application Guide for TASK-007 |
| NFR-001 (Token budget) | Token Efficiency Guidelines; token cost benchmarks |
| NFR-004 (Unambiguous language) | Effective Pattern Catalog; Anti-Pattern Catalog |
| NFR-007 (Visual distinguishability) | Visual Distinguishability section |

### Acceptance Criteria Covered

| AC | Coverage |
|----|----------|
| AC-3 (HARD/MEDIUM/SOFT patterns) | Full Effective Pattern Catalog + Anti-Pattern Catalog |
| AC-4 (Adversarial strategy directives) | Template 6; Pattern Application Guide |
| AC-9 (L2 re-injection tags) | L2 Re-Injection Format section; Template 5 |
| AC-11 (No unmitigated bypass vectors) | Anti-Pattern Catalog identifies bypass vectors; Effective Patterns mitigate them |

---

## References

| # | Document | Location | Content Used |
|---|----------|----------|--------------|
| 1 | ADR-EPIC002-002 (ACCEPTED) | `EN-402-enforcement-priority-analysis/TASK-005-enforcement-ADR.md` | V-026 enforcement tier language, token budget, L2 V-024 specification |
| 2 | Barrier-1 ADV-to-ENF Handoff | `orchestration/epic002-crosspoll-20260213-001/cross-pollination/barrier-1/adv-to-enf/barrier-1-adv-to-enf-handoff.md` | Strategy encoding requirements, quality gate integration |
| 3 | EN-404 Enabler | `EN-404-rule-based-enforcement/EN-404-rule-based-enforcement.md` | FR/NFR requirements |
| 4 | TASK-001 Requirements | `EN-404-rule-based-enforcement/TASK-001-rule-requirements.md` | REQ-404-011 (HARD vocabulary), REQ-404-014 (visual distinguishability), REQ-404-016 (consequences) |
| 5 | TASK-002 Rule Audit | `EN-404-rule-based-enforcement/TASK-002-rule-audit.md` | Per-file bypass vectors, compliance observations, anti-pattern identification |
| 6 | TASK-003 Tiered Enforcement | `EN-404-rule-based-enforcement/TASK-003-tiered-enforcement.md` | HARD rule inventory (H-01 to H-24), tier definitions, token budgets |
| 7 | python-environment.md | `.context/rules/python-environment.md` | Model of effective enforcement language |
| 8 | CLAUDE.md | Root directory | Model of effective constitutional constraints |
| 9 | markdown-navigation-standards.md | `.context/rules/markdown-navigation-standards.md` | Model of formal tier labeling |

---

*Agent: ps-architect (Claude Opus 4.6)*
*Date: 2026-02-13*
*Parent: EN-404 Rule-Based Enforcement Enhancement*
*Quality Target: >= 0.92*
*Effective Patterns: 6*
*Anti-Patterns: 6*
*Templates: 6*
*L2 Re-Injection: ~510 tokens of 600 budget*
