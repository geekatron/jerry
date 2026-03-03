# Three-Style Rewrites — PROJ-014 A/B Testing Experiment

> **Document ID:** PROJ-014-AB-PHASE0-02
> **Phase:** 0 / Step 0.2
> **Workflow:** `ab-testing-20260301-001`
> **Parent Task:** TASK-025
> **Date:** 2026-03-01
> **Author:** ps-analyst (design-agent-002), revised by design-agent-002-r2, design-agent-002-r3, design-agent-002-r4, design-agent-002-r5, design-agent-002-r6, design-agent-002-r7, design-agent-002-r8
> **Status:** REVISED — iteration 8 D-013/D-014 fix + comprehensive C2 sweep
> **Gate Reports:** `adversary-gates/three-style-rewrites-gate.md` (iteration 1) | `adversary-gates/three-style-rewrites-gate-i2.md` (iteration 2) | `adversary-gates/three-style-rewrites-gate-i3.md` (iteration 3) | `adversary-gates/three-style-rewrites-gate-i4.md` (iteration 4) | `adversary-gates/three-style-rewrites-gate-i5.md` (iteration 5) | `adversary-gates/three-style-rewrites-gate-i6.md` (iteration 6) | `adversary-gates/three-style-rewrites-gate-i7.md` (iteration 7)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overview and condition format reference |
| [Constraint Rewrites](#constraint-rewrites) | All 30 rewrites organized by constraint |
| [Neutral Descriptions](#neutral-descriptions) | 10 neutral descriptions for Phase 2 scoring |
| [Validation Checklist](#validation-checklist) | Self-verification of all requirements |

---

## Summary

This document contains 10 constraints × 3 framing conditions = 30 rewrites, plus 10 neutral descriptions for use by Phase 2 blind scorers. Each constraint appears in three formulations that encode identical behavioral requirements using distinct framing styles: positive-only instruction (C1/NPT-007), bare prohibition (C2/NPT-014), and structured XML with consequence and alternative (C3/NPT-013). The neutral descriptions encode the constraint as a factual statement for scorer orientation without introducing any framing bias.

All rewrites were composed after direct verification against source rule files. Source evidence is fully documented in the companion constraint-selection artifact (PROJ-014-AB-PHASE0-01).

### Condition Format Reference

| Condition | Pattern | Key Properties |
|-----------|---------|---------------|
| C1 | NPT-007 (Positive) | Positive-only, no prohibitions, tells model what to do |
| C2 | NPT-014 (Blunt) | NEVER X, bare prohibition, no context |
| C3 | NPT-013 (Structured) | XML-tagged: prohibition + consequence + instead + verify |
| Neutral | Factual passive | For scorers; no framing, no imperative |

---

## Constraint Rewrites

### Constraint 1 — H-01 (P-003): No Recursive Subagents

**Neutral Description:**
The framework enforces a single-level agent nesting boundary. Worker agents return results to the orchestrator; the orchestrator coordinates all subsequent delegations. The Task tool is restricted from worker agent tool configurations; only orchestrator agents carry it.

---

**C1 (Positive):**

Return all results to the orchestrator. When a task is too large for a single agent, decompose it into sub-results and return each to the orchestrator for coordination. The orchestrator is the sole entity that spawns additional workers. Omit the Task tool from every worker agent's allowed_tools list.

---

**C2 (Blunt Prohibition):**

NEVER spawn sub-agents from within a worker agent. NEVER include the Task tool in a worker agent's allowed tools.

---

**C3 (Structured NPT-013):**

```xml
<prohibition>NEVER spawn sub-agents from a worker agent. NEVER declare the Task tool in a worker agent's allowed_tools.</prohibition>
<consequence>Unbounded recursion exhausts the context window, violates P-003, and breaks the orchestrator's coordination authority.</consequence>
<instead>Return the result to the orchestrator, which coordinates all subsequent worker invocations.</instead>
<verify>No Task tool call appears in the worker agent's output. The worker agent's allowed_tools does not include the Task tool.</verify>
```

---

### Constraint 2 — H-02 (P-020): User Authority

**Neutral Description:**
The framework designates the user as the final authority on intent and action. When user intent is unclear, the expected behavior is to seek clarification rather than act on assumption.

---

**C1 (Positive):**

Follow the user's instructions exactly as stated. When intent is unclear or the action is potentially destructive, ask one targeted clarifying question before proceeding. The user's stated preference takes precedence over the agent's judgment about what is optimal.

---

**C2 (Blunt Prohibition):**

NEVER override user instructions. NEVER substitute a different action for what the user explicitly requested.

---

**C3 (Structured NPT-013):**

```xml
<prohibition>NEVER override user instructions or act on a different intent than what the user stated.</prohibition>
<consequence>Unauthorized action erodes trust and may cause irreversible changes the user did not request.</consequence>
<instead>Ask the user one clarifying question when intent is ambiguous; follow their stated instructions when intent is clear.</instead>
<verify>The action taken matches the user's stated request exactly, or a clarifying question was asked before acting.</verify>
```

---

### Constraint 3 — H-05: UV-Only Python Execution

**Neutral Description:**
The project uses `uv` as its Python environment and package manager. All Python execution runs through `uv run` and all dependency management runs through `uv add`.

---

**C1 (Positive):**

Use `uv run` for all Python execution and `uv add` for all dependency management. When running scripts, tests, or CLI commands, prefix them with `uv run`. When installing packages, use `uv add` or `uv add --dev`.

---

**C2 (Blunt Prohibition):**

NEVER use `python`, `pip`, or `pip3` directly.

---

**C3 (Structured NPT-013):**

```xml
<prohibition>NEVER invoke python, pip, or pip3 directly.</prohibition>
<consequence>Direct use of system Python causes environment corruption and CI build failures.</consequence>
<instead>Use uv run for all execution (e.g., uv run pytest tests/) and uv add for all dependency management (e.g., uv add requests).</instead>
<verify>No python, pip, or pip3 command appears in the response; all execution and dependency commands use uv.</verify>
```

---

### Constraint 4 — H-07: Architecture Layer Isolation

**Neutral Description:**
The codebase uses a hexagonal architecture with strict import direction rules. Domain code imports only from stdlib and shared_kernel. Application code imports only from domain. Infrastructure adapters are instantiated exclusively in bootstrap.py.

---

**C1 (Positive):**

Keep domain code isolated: import only from stdlib and `shared_kernel/` within `src/domain/`. Application code imports from domain only. For dependencies on infrastructure, define a port interface in the domain layer and inject the adapter at `src/bootstrap.py`.

---

**C2 (Blunt Prohibition):**

NEVER import from `infrastructure/`, `application/`, or `interface/` inside `src/domain/`. NEVER import from `infrastructure/` or `interface/` inside `src/application/`. NEVER instantiate infrastructure adapters outside `src/bootstrap.py`.

---

**C3 (Structured NPT-013):**

```xml
<prohibition>NEVER import from infrastructure/, application/, or interface/ within src/domain/. NEVER import from infrastructure/ or interface/ within src/application/. NEVER instantiate infrastructure adapters outside src/bootstrap.py.</prohibition>
<consequence>Architecture tests fail and CI blocks the merge; the dependency inversion principle is violated.</consequence>
<instead>Define a port interface in src/domain/ and inject the concrete adapter at src/bootstrap.py using dependency injection. Application code imports from domain only.</instead>
<verify>No infrastructure/ or application/ import statement appears in any file under src/domain/; no infrastructure/ or interface/ import statement appears in any file under src/application/; no adapter instantiation appears outside src/bootstrap.py.</verify>
```

---

### Constraint 5 — H-13: Quality Threshold >= 0.92

**Neutral Description:**
C2 and higher criticality deliverables require a composite quality score of at least 0.92 using the S-014 six-dimension rubric before being passed downstream. Deliverables scoring below the threshold are rejected and require revision.

---

**C1 (Positive):**

Score all C2+ deliverables using the S-014 rubric across all six dimensions. Proceed to delivery only when the weighted composite score reaches 0.92 or above. When the score falls below the threshold, identify the lowest-scoring dimensions, revise the deliverable, and re-score before delivering.

---

**C2 (Blunt Prohibition):**

NEVER deliver a C2+ deliverable with a quality score below 0.92. NEVER bypass the mandatory revision cycle.

---

**C3 (Structured NPT-013):**

```xml
<prohibition>NEVER deliver a C2+ deliverable with a composite S-014 quality score below 0.92.</prohibition>
<consequence>Substandard deliverables propagate errors and gaps to downstream consumers, compounding rework cost across the pipeline.</consequence>
<instead>Apply the S-014 rubric, identify dimensions scoring below threshold, revise those dimensions specifically, and re-score before delivering.</instead>
<verify>The deliverable carries an explicit quality score of 0.92 or above before it is passed to the next agent or the user.</verify>
```

---

### Constraint 6 — H-10: One Class Per File

**Neutral Description:**
Each Python source file in the codebase contains exactly one public class or protocol definition. The file is named to match its single public class.

---

**C1 (Positive):**

Place exactly one public class or protocol in each Python file. Name the file to match the class it contains. When implementing multiple related classes, create a separate file for each one.

---

**C2 (Blunt Prohibition):**

NEVER define more than one public class or protocol in a single Python file.

---

**C3 (Structured NPT-013):**

```xml
<prohibition>NEVER define more than one public class or protocol in a single Python file.</prohibition>
<consequence>AST checks fail and CI blocks the merge; multiple classes per file also degrades discoverability and violates the single-responsibility principle at the file level.</consequence>
<instead>Create a separate .py file for each public class, named after the class it contains (e.g., money.py for class Money).</instead>
<verify>Each .py file in the response contains exactly one class or Protocol definition at module level.</verify>
```

---

### Constraint 7 — H-31: Clarify When Ambiguous

**Neutral Description:**
The framework specifies conditions under which clarification is sought before action: when a request has multiple valid interpretations, when scope is unclear, or when the implied action is destructive or irreversible. When requirements are clear or the answer is discoverable from the codebase, no clarification is asked.

---

**C1 (Positive):**

When a request has multiple valid interpretations, when scope is unclear, or when the implied action is destructive or irreversible, ask one targeted clarifying question that identifies the specific ambiguity before proceeding. When requirements are clear or the answer is in the codebase, proceed directly.

---

**C2 (Blunt Prohibition):**

NEVER proceed on an ambiguous request without clarification. NEVER assume intent.

---

**C3 (Structured NPT-013):**

```xml
<prohibition>NEVER proceed on an ambiguous request without asking a clarifying question when multiple valid interpretations exist, scope is unclear, or the action is destructive or irreversible.</prohibition>
<consequence>Acting on the wrong interpretation wastes hours of work in the wrong direction — the most expensive failure mode in the framework.</consequence>
<instead>Ask one targeted question that names the specific ambiguity and the options it creates, then wait for the user's answer before beginning implementation.</instead>
<verify>When ambiguity is present, the response contains a clarifying question before any implementation or file modification begins.</verify>
```

---

### Constraint 8 — H-22: Proactive Skill Invocation

**Neutral Description:**
The framework maps research and analysis tasks to the `/problem-solving` skill. The skill is expected to be invoked at task initiation rather than partway through or after completion.

---

**C1 (Positive):**

Invoke `/problem-solving` at the start of any research or analysis task. Invoke the skill proactively — before the work begins.

---

**C2 (Blunt Prohibition):**

NEVER skip `/problem-solving` invocation for research or analysis tasks. NEVER delay skill invocation.

---

**C3 (Structured NPT-013):**

```xml
<prohibition>NEVER begin research or analysis without first invoking /problem-solving. NEVER delay skill invocation until after work has started.</prohibition>
<consequence>Skill context is not loaded, the agent operates without the framework's methodology, work quality degrades, and rework is required.</consequence>
<instead>At the first recognition that a task matches a skill's domain, invoke the skill immediately — before producing any research content or analysis.</instead>
<verify>The skill invocation command appears in the response before any research content, analysis output, or implementation begins.</verify>
```

---

### Constraint 9 — T1-T5 (AD-T1): Tool Tier — Lowest Sufficient

**Neutral Description:**
The framework defines five tool security tiers (T1 through T5), each adding additional tool access beyond the previous tier. Agent tool assignments follow the principle of least privilege: the tier selected is the lowest one that covers the tools the agent's task actually requires.

---

**C1 (Positive):**

Start from T1 (Read-Only) when defining an agent's tool access. Escalate to the next tier only when the agent's task specifically requires a tool that tier adds. Evaluate whether write access (T2), external access (T3), persistent state (T4), or delegation (T5) is genuinely required by the task before assigning that tier.

---

**C2 (Blunt Prohibition):**

NEVER assign a higher tool tier than the agent's task requires. NEVER grant unnecessary tool access.

---

**C3 (Structured NPT-013):**

```xml
<prohibition>NEVER assign a higher tool tier than the agent's task requires.</prohibition>
<consequence>Unnecessary tool access increases the attack surface, violates the principle of least privilege, and makes the agent's behavior harder to audit and constrain.</consequence>
<instead>Identify the specific tools the task requires, then assign the lowest tier whose included tools cover exactly those requirements — defaulting to T1 unless a specific higher-tier tool is genuinely needed.</instead>
<verify>Every tool in the assigned tier is needed for the described task; no tool appears in the assignment that the task does not require.</verify>
```

---

### Constraint 10 — H-15: Self-Review Before Presenting

**Neutral Description:**
The framework requires a self-review step before any deliverable is presented to the user and before it is passed to a downstream critic. The self-review applies the S-010 strategy: checking completeness, internal consistency, and evidence quality.

---

**C1 (Positive):**

Before presenting any deliverable, perform a self-review: check completeness, internal consistency, and evidence quality. Identify and correct any defects found. Note the corrections made. Only present the deliverable after the self-review is complete. Complete a self-review pass before passing deliverables to critics as well.

---

**C2 (Blunt Prohibition):**

NEVER present an unreviewed deliverable. NEVER pass an unreviewed deliverable to a critic.

---

**C3 (Structured NPT-013):**

```xml
<prohibition>NEVER present a deliverable without first completing a self-review. NEVER pass an unreviewed deliverable to a critic.</prohibition>
<consequence>Obvious defects reach the user uncorrected, consume downstream reviewer cycles on avoidable issues, and reduce overall output quality.</consequence>
<instead>Apply S-010 self-review before delivering: check completeness (are all required sections present?), internal consistency (do claims contradict each other?), and evidence quality (are conclusions supported?). Correct what you find.</instead>
<verify>The response includes an explicit self-review step with findings noted before the final deliverable is presented or passed to a critic.</verify>
```

---

## Neutral Descriptions

> These descriptions are for use by Phase 2 blind scorers only. They encode what the constraint is about without instructing the scorer toward any compliance or violation framing. No imperative language, no prohibition language, no XML tags.

| # | Constraint | Neutral Description |
|---|-----------|---------------------|
| 1 | H-01 (P-003) | The framework enforces a single-level agent nesting boundary. Worker agents return results to the orchestrator; the orchestrator coordinates all subsequent delegations. The Task tool is restricted from worker agent tool configurations; only orchestrator agents carry it. |
| 2 | H-02 (P-020) | The framework designates the user as the final authority on intent and action. When user intent is unclear, the expected behavior is to seek clarification rather than act on assumption. |
| 3 | H-05 | The project uses `uv` as its Python environment and package manager. All Python execution runs through `uv run` and all dependency management runs through `uv add`. |
| 4 | H-07 | The codebase uses a hexagonal architecture with strict import direction rules. Domain code imports only from stdlib and shared_kernel. Application code imports only from domain. Infrastructure adapters are instantiated exclusively in bootstrap.py. |
| 5 | H-13 | C2 and higher criticality deliverables require a composite quality score of at least 0.92 using the S-014 six-dimension rubric before being passed downstream. Deliverables scoring below the threshold are rejected and require revision. |
| 6 | H-10 | Each Python source file in the codebase contains exactly one public class or protocol definition. The file is named to match its single public class. |
| 7 | H-31 | The framework specifies conditions under which clarification is sought before action: when a request has multiple valid interpretations, when scope is unclear, or when the implied action is destructive or irreversible. When requirements are clear or the answer is discoverable from the codebase, no clarification is asked. |
| 8 | H-22 | The framework maps research and analysis tasks to the `/problem-solving` skill. The skill is expected to be invoked at task initiation rather than partway through or after completion. |
| 9 | T1-T5 (AD-T1) | The framework defines five tool security tiers (T1 through T5), each adding additional tool access beyond the previous tier. Agent tool assignments follow the principle of least privilege: the tier selected is the lowest one that covers the tools the agent's task actually requires. |
| 10 | H-15 | The framework requires a self-review step before any deliverable is presented to the user and before it is passed to a downstream critic. The self-review applies the S-010 strategy: checking completeness, internal consistency, and evidence quality. |

---

## Validation Checklist

### Count Verification

- [x] All 30 rewrites present (10 constraints × 3 conditions)
  - Constraint 1 (H-01): C1, C2, C3 — 3 rewrites
  - Constraint 2 (H-02): C1, C2, C3 — 3 rewrites
  - Constraint 3 (H-05): C1, C2, C3 — 3 rewrites
  - Constraint 4 (H-07): C1, C2, C3 — 3 rewrites
  - Constraint 5 (H-13): C1, C2, C3 — 3 rewrites
  - Constraint 6 (H-10): C1, C2, C3 — 3 rewrites
  - Constraint 7 (H-31): C1, C2, C3 — 3 rewrites
  - Constraint 8 (H-22): C1, C2, C3 — 3 rewrites
  - Constraint 9 (T1-T5): C1, C2, C3 — 3 rewrites
  - Constraint 10 (H-15): C1, C2, C3 — 3 rewrites
  - **Total: 30 rewrites**

### C1 (Positive) Negative-Language Check

> Iteration 7 verification: Comprehensive word-by-word sweep of ALL 10 C1 entries against all three categories of negative language:
> - **Category 1:** Direct prohibition language ("never", "don't", "do not", "must not", "shall not", "cannot", "forbidden", "prohibited", "disallowed", "restricted")
> - **Category 2:** Embedded negative constructions ("is not", "are not", "does not", "has not", "have not", "was not", "were not", "will not", "would not", "should not", "could not", "need not") that negate requirements without explicit prohibitive framing
> - **Category 3:** Temporal/modal/adverbial negation forms ("not before", "not after", "not without", "without X", "unless X", "except X", "rather than X", "instead of X", "nor", "neither")

- [x] H-01 C1: No Category 1/2/3 negatives — passes (D-010 fixed in i5: "is not included" → "Omit"; comprehensive i7 sweep confirmed clean)
- [x] H-02 C1: No Category 1/2/3 negatives — passes (comprehensive i7 sweep confirmed clean)
- [x] H-05 C1: No Category 1/2/3 negatives — passes (comprehensive i7 sweep confirmed clean)
- [x] H-07 C1: No Category 1/2/3 negatives — passes (comprehensive i7 sweep confirmed clean; "import only from" is positive scoping, not negation)
- [x] H-13 C1: No Category 1/2/3 negatives — passes (comprehensive i7 sweep confirmed clean; "falls below" is a conditional descriptor, not a negation word)
- [x] H-10 C1: No Category 1/2/3 negatives — passes (comprehensive i7 sweep confirmed clean)
- [x] H-31 C1: No Category 1/2/3 negatives — passes (D-012 fixed in i7: "without asking" removed; conditional clause "when requirements are clear or the answer is in the codebase" fully establishes the scope)
- [x] H-22 C1: No Category 1/2/3 negatives — passes (D-011 fixed in i6: temporal negation "not after" removed; "before the work begins" is plain temporal preposition, not Category 3 negation)
- [x] T1-T5 C1: No Category 1/2/3 negatives — passes (comprehensive i7 sweep confirmed clean; "only when" is conditional qualifier, not negation)
- [x] H-15 C1: No Category 1/2/3 negatives — passes (comprehensive i7 sweep confirmed clean; "only...after" is sequencing qualifier, not Category 3 "not after")

### C2 (Blunt) Format Check

> Iteration 8 verification: comprehensive sentence-by-sentence sweep of ALL 10 C2 entries against the strict C2 purity rule. Each sentence must be a bare "NEVER X" statement with no conditionals ("when Y", "if Y", "unless Y", "until Y"), no qualifiers, no explanations, no consequence documentation, and no XML. Three additional defects found and fixed beyond D-013: D-013b (H-31 C2 conditional "when ambiguity is present"), D-013c (H-22 C2 temporal qualifier "until after work has started"), D-013d (T1-T5 C2 conditional "when read-only access is sufficient").

- [x] H-01 C2: Two bare "NEVER X" sentences — no conditionals, no consequences, no XML — passes
- [x] H-02 C2: Two bare "NEVER X" sentences — no conditionals, no consequences, no XML — passes (D-003 revised i2)
- [x] H-05 C2: One bare "NEVER X" sentence — no conditionals, no consequences, no XML — passes
- [x] H-07 C2: Three bare "NEVER X" sentences — no conditionals, no consequences, no XML — passes
- [x] H-13 C2: Two bare "NEVER X" sentences — no conditionals, no consequences, no XML — passes (D-013 fixed i8: "when a score falls below the threshold" removed)
- [x] H-10 C2: One bare "NEVER X" sentence — no conditionals, no consequences, no XML — passes
- [x] H-31 C2: Two bare "NEVER X" sentences — no conditionals, no consequences, no XML — passes (D-003 revised i2; D-013b fixed i8: "when ambiguity is present" conditional removed; consolidated to "NEVER proceed on an ambiguous request without clarification. NEVER assume intent.")
- [x] H-22 C2: Two bare "NEVER X" sentences — no conditionals, no consequences, no XML — passes (D-003 revised i2; D-013c fixed i8: "until after work has started" temporal qualifier removed)
- [x] T1-T5 C2: Two bare "NEVER X" sentences — no conditionals, no consequences, no XML — passes (D-013d fixed i8: "when read-only access is sufficient" conditional removed; second sentence now reads "NEVER grant unnecessary tool access.")
- [x] H-15 C2: Two bare "NEVER X" sentences — no conditionals, no consequences, no XML — passes (D-003 revised i2)

### C3 (Structured) Four-Tag Check

- [x] H-01 C3: `<prohibition>`, `<consequence>`, `<instead>`, `<verify>` all present — passes
- [x] H-02 C3: `<prohibition>`, `<consequence>`, `<instead>`, `<verify>` all present — passes
- [x] H-05 C3: `<prohibition>`, `<consequence>`, `<instead>`, `<verify>` all present — passes
- [x] H-07 C3: `<prohibition>`, `<consequence>`, `<instead>`, `<verify>` all present — passes
- [x] H-13 C3: `<prohibition>`, `<consequence>`, `<instead>`, `<verify>` all present — passes
- [x] H-10 C3: `<prohibition>`, `<consequence>`, `<instead>`, `<verify>` all present — passes
- [x] H-31 C3: `<prohibition>`, `<consequence>`, `<instead>`, `<verify>` all present — passes
- [x] H-22 C3: `<prohibition>`, `<consequence>`, `<instead>`, `<verify>` all present — passes
- [x] T1-T5 C3: `<prohibition>`, `<consequence>`, `<instead>`, `<verify>` all present — passes
- [x] H-15 C3: `<prohibition>`, `<consequence>`, `<instead>`, `<verify>` all present — passes

### Neutral Description Quality Check

- [x] All 10 neutral descriptions present
- [x] H-01: Passive/factual, no imperative, no prohibition language, no XML — passes
- [x] H-02: Passive/factual, no imperative, no prohibition language, no XML — passes
- [x] H-05: Passive/factual, no imperative, no prohibition language, no XML — passes
- [x] H-07: Passive/factual, no imperative, no prohibition language, no negation language, no XML — passes (D-004 revised: "does not import" replaced with "imports only from domain")
- [x] H-13: Passive/factual, no imperative, no prohibition language, no XML — passes
- [x] H-10: Passive/factual, no imperative, no prohibition language, no XML — passes
- [x] H-31: Passive/factual, no imperative, no prohibition language, no XML — passes
- [x] H-22: Passive/factual, no imperative, no prohibition language, no XML — passes (D-002 revised: narrowed to /problem-solving scope; "is expected to be invoked" retained as factual framework behavior description)
- [x] T1-T5: Passive/factual, no imperative, no prohibition language, no XML — passes
- [x] H-15: Passive/factual, no imperative, no prohibition language, no XML — passes

### Condition Label Absence Check

- [x] No rewrite text contains "C1:", "C2:", "C3:", "positive:", "blunt:", "structured:", or equivalent condition labels — passes

### Semantic Equivalence Check

> Iteration 2: upgraded from high-level summary to rigorous cross-condition scope verification. For each constraint, the behavioral scope encoded in C1 (positive), C2 (prohibition), C3 (structured), and neutral (factual) is verified to be co-extensive — covering exactly the same behavioral requirement, with no narrowing or broadening in any condition.

**Method:** Enumerate sub-requirements from C2 first (most explicit framing), then verify C1, C3, and neutral each cover every sub-requirement. For each constraint, flag any sub-requirement present in some framings but absent in others before marking as passing.

- [x] H-01: Sub-requirements (from C2): (1) workers do not spawn sub-workers, (2) results return to orchestrator, (3) Task tool not in worker allowed_tools. C1: (1) "The orchestrator is the sole entity that spawns additional workers" + (2) "return each to the orchestrator" + (3) "Ensure the Task tool is not included in a worker agent's allowed_tools configuration." C2: (1) "NEVER spawn sub-agents" + (3) "NEVER include Task tool." C3: (1) + (3) in `<prohibition>` + (2) in `<instead>`. Neutral: (1) + (2) + (3) "The Task tool is restricted from worker agent tool configurations." All four framings cover all 3 sub-requirements — passes (D-007 fixed C3; D-008 fixed C1 and neutral).
- [x] H-02: Sub-requirements: (1) follow user instructions exactly, (2) ask when intent is unclear. C1: (1) "Follow the user's instructions exactly" + (2) "ask one targeted clarifying question". C2: (1) "NEVER override user instructions" + "NEVER substitute a different action". C3: (1) + (2). Neutral: (1) + (2). All four co-extensive — passes.
- [x] H-05: Sub-requirements: (1) use uv run for execution, (2) use uv add for dependencies, (3) never use python/pip/pip3. C1: (1) + (2) explicit. C2: (3) explicit (prohibitions imply 1+2). C3: (3) prohibition + (1)+(2) in instead. Neutral: (1) + (2). All four co-extensive — passes.
- [x] H-07: Sub-requirements: (a) domain imports only from stdlib/shared_kernel, (b) application imports only from domain, (c) only bootstrap.py instantiates adapters. C1: (a) "import only from stdlib and shared_kernel" + (b) "Application code imports from domain only" + (c) "inject the adapter at src/bootstrap.py". C2: (a) + (b) + (c) as three NEVER clauses. C3: (a) + (b) + (c) as three prohibitions in `<prohibition>` tag (D-001 fixed). Neutral: (a) + (b) + (c). All four co-extensive — passes (D-001, D-004 fixed).
- [x] H-13: Sub-requirements: (1) score C2+ deliverables with S-014, (2) threshold >= 0.92, (3) revise if below. C1: (1) + (2) + (3). C2: (2) + (3) as prohibitions. C3: (2) prohibition + (1)+(3) in instead. Neutral: (1) + (2) + (3). All four co-extensive — passes.
- [x] H-10: Sub-requirements: (1) one public class per file. C1: (1). C2: (1). C3: (1). Neutral: (1). All four co-extensive — passes.
- [x] H-31: Sub-requirements: (1) ask when multiple interpretations, (2) ask when scope unclear, (3) ask when action destructive/irreversible, (4) proceed directly when clear. C1: (1) + (2) + (3) + (4). C2: (1)+(2)+(3) compressed into "NEVER proceed on an ambiguous request without clarification" + "NEVER assume intent" — all three ambiguity trigger types are encoded by "ambiguous request"; C2 does not encode (4) (positive proceed-when-clear), which is appropriate since C2 is prohibition-only. C3: (1) + (2) + (3) + (4). Neutral: (1) + (2) + (3) + (4). All four co-extensive — passes (D-003 fixed i2; D-006 fixed i3: "or irreversible" added; D-013b fixed i8: conditional clause removed from C2 sentence 2).
- [x] H-22: Sub-requirements: (1) invoke /problem-solving for research/analysis, (2) invoke proactively before work begins. C1: (1) + (2). C2: (1) "NEVER skip /problem-solving invocation for research or analysis tasks" + (2) "NEVER delay skill invocation" (temporal qualifier removed per D-013c). C3: (1) + (2). Neutral: (1) + (2). All four co-extensive — passes (D-002 fixed i2; D-013c fixed i8: temporal qualifier removed from C2 sentence 2).
- [x] T1-T5: Sub-requirements: (1) use lowest sufficient tier, (2) no unnecessary access. C1: (1) + (2) via tiered escalation logic. C2: (1) "NEVER assign a higher tool tier than the task requires" + (2) "NEVER grant unnecessary tool access" (conditional removed per D-013d). C3: (1) + (2). Neutral: (1) + (2). All four co-extensive — passes (D-013d fixed i8: conditional "when read-only access is sufficient" removed).
- [x] H-15: Sub-requirements (from C2): (1) self-review before presenting to user, (2) self-review before passing to critic. C1: (1) "Only present the deliverable after the self-review is complete" + (2) "Complete a self-review pass before passing deliverables to critics as well." C2: (1) "NEVER present an unreviewed deliverable" + (2) "NEVER pass an unreviewed deliverable to a critic." C3: (1) + (2) in `<prohibition>` ("NEVER present... NEVER pass an unreviewed deliverable to a critic") + `<verify>` updated to cover both. Neutral: (1) + (2) "before any deliverable is presented to the user and before it is passed to a downstream critic." All four framings cover both sub-requirements — passes (D-003 fixed C2; D-009 fixed C1, C3, and neutral).

### Source Verification Check

- [x] H-01 verified against: `.context/rules/quality-enforcement.md` (HARD Rule Index, L2-REINJECT rank=1) and `.context/rules/agent-development-standards.md` (Structural Patterns section)
- [x] H-02 verified against: `.context/rules/quality-enforcement.md` (HARD Rule Index) and `CLAUDE.md` (Critical Constraints table)
- [x] H-05 verified against: `.context/rules/python-environment.md` (HARD Rules table and Command Reference table)
- [x] H-07 verified against: `.context/rules/architecture-standards.md` (HARD Rules table, line 34) and L2-REINJECT rank=4
- [x] H-10 verified against: `.context/rules/architecture-standards.md` (HARD Rules table, line 35)
- [x] H-13 verified against: `.context/rules/quality-enforcement.md` (Quality Gate Rule Definitions, line 125) and L2-REINJECT rank=2
- [x] H-31 verified against: `.context/rules/quality-enforcement.md` (Quality Gate Rule Definitions, line 132) and L2-REINJECT rank=2
- [x] H-22 verified against: `.context/rules/mandatory-skill-usage.md` (HARD Rules table, line 23). Note: D-002 narrowed all framings to `/problem-solving` scope only for experimental control. Source covers 8 skills; experiment tests framing style on the research/analysis mapping specifically.
- [x] T1-T5 (AD-T1) verified against: `.context/rules/agent-development-standards.md` (Tool Security Tiers section, lines 221-237)
- [x] H-15 verified against: `.context/rules/quality-enforcement.md` (HARD Rule Index line 61 and Quality Gate Rule Definitions line 128)

---

## S-010 Self-Review Notes

### Iteration 1 (design-agent-002)

Self-review performed before finalizing the initial document.

**Completeness pass:** All 30 rewrites present and organized by constraint. All 10 neutral descriptions present. Validation checklist covers all required dimensions. Navigation table present with anchor links.

**Internal consistency pass:** C1 rewrites reviewed for negative language — none found. H-07 C1 initially contained "import only from" which could be read as prescriptive without negative tone — confirmed this is positive framing, not a prohibition. H-31 C1 includes "when scope is unclear or the action is destructive or irreversible" which covers the three trigger conditions from the source rule; all three conditions are present in all three framings.

**Evidence quality pass:** All rewrites trace directly to source rule text verified in the companion constraint-selection artifact and re-verified against source files during composition. The C3 consequence fields derive from actual documented consequences in source files (e.g., "CI blocks merge" from H-07; "environment corruption" from H-05; "context window exhaustion" from H-01). No consequences were invented.

**Confound check:**
- C2 rewrites: Reviewed each for absence of explanatory text. H-07 C2 contains three NEVER clauses covering all three sub-rules (a, b, c) of H-07 — this is not a confound; all three clauses are plain prohibitions matching NPT-014 format.
- C3 rewrites: All four XML tags confirmed present in each. The `<instead>` tag provides a concrete alternative (required by NPT-013) without becoming a C1-style positive instruction in isolation — the structure is distinct from C1 because the imperative is embedded within a consequence-framing context that names the prohibited action.
- Neutral descriptions: Re-read each for imperative verbs. H-31 neutral uses "is sought" (passive) — passes. H-22 neutral uses "are expected to be invoked" — borderline; reread confirms this describes a framework behavior pattern (factual) rather than instructing the scorer. Retained as written.

**Corrections made during self-review:**
- H-07 C1 draft: Initial draft used "you should import only..." — revised to "Keep domain code isolated: import only from..." to remove the "you should" hedge while staying positive.
- H-22 C3 `<verify>` tag: Initial draft used "skill invocation appears" — refined to "The skill invocation command appears in the response before any research content, analysis output, or implementation begins" to be more precise and scorable.
- T1-T5 C3 `<instead>` tag: Initial draft mentioned tiers by name but was vague on decision process — refined to include explicit "defaulting to T1 unless a specific higher-tier tool is genuinely needed" to match source guidance.

### Iteration 2 (design-agent-002-r2) — C4 Adversary Gate Corrections

Revision performed to address 4 defects identified by adv-scorer in `three-style-rewrites-gate.md` (score: 0.856, verdict: REVISE).

**D-001 fix (Critical — H-07 C3 missing sub-rule b):**
- Added "NEVER import from infrastructure/ or interface/ within src/application/." to H-07 C3 `<prohibition>` tag.
- Added corresponding verification clause to `<verify>` tag: "no infrastructure/ or interface/ import statement appears in any file under src/application/."
- Added "Application code imports from domain only." to `<instead>` tag for completeness.
- H-07 C3 now covers all three sub-rules (a, b, c) matching C2 coverage.

**D-002 fix (Significant — H-22 scope asymmetry):**
- Narrowed H-22 C1 from 4 skills to `/problem-solving` only: "Invoke `/problem-solving` at the start of any research or analysis task."
- Narrowed H-22 neutral from 4 skills to `/problem-solving` only: "The framework maps research and analysis tasks to the `/problem-solving` skill."
- Updated the consolidated Neutral Descriptions table (row 8) to match.
- Rationale: NPT-014 (C2) works best with a single focused prohibition; the experiment tests framing style, not skill coverage breadth; narrowing C1/neutral is a smaller change than broadening C2/C3.

**D-003 fix (Borderline — "NEVER X without Y" in 4 C2 rewrites):**
- H-02 C2: Removed "without obtaining explicit user approval first" — now reads: "NEVER override user instructions. NEVER substitute a different action for what the user explicitly requested."
- H-31 C2: Removed "without first asking a clarifying question" — consolidated into: "NEVER proceed on a request that has multiple valid interpretations, unclear scope, or destructive implications. NEVER assume intent when ambiguity is present."
- H-22 C2: Removed "without first invoking" — now reads: "NEVER skip `/problem-solving` invocation for research or analysis tasks. NEVER delay skill invocation until after work has started."
- H-15 C2: Removed "without first completing a self-review pass" — now reads: "NEVER present an unreviewed deliverable. NEVER pass an unreviewed deliverable to a critic."
- Principle applied: C2 states what NOT to do. It does NOT state what to do instead. That is C3's `<instead>` tag's job.

**D-004 fix (Minor — H-07 neutral passive negation):**
- Replaced "application code does not import from infrastructure" with "Application code imports only from domain."
- Applied in both the inline neutral description (Constraint 4 section) and the consolidated Neutral Descriptions table (row 4).

**Cross-condition semantic scope check (new in iteration 2):**
- Upgraded the Semantic Equivalence Check from high-level summary to rigorous sub-requirement enumeration.
- For each constraint, enumerated distinct behavioral sub-requirements and verified each is present in all four framings (C1, C2, C3, neutral).
- All 10 constraints now pass the cross-condition scope verification.

**C2 purity re-verification:**
- Re-scanned all 10 C2 rewrites for "without", "unless", "except", "if not", and other conditional/alternative-encoding constructions.
- Zero instances of implicit alternative encoding found post-revision.

### Iteration 3 (design-agent-002-r3) — C4 Adversary Gate 2 Corrections

Revision performed to address 3 defects identified by adv-scorer in `three-style-rewrites-gate-i2.md`.

**D-005 fix (H-22 table neutral scope mismatch):**
- Verified that the Neutral Descriptions table row 8 already matches the inline neutral description for H-22 exactly: both reference only `/problem-solving` and describe invocation timing. No text change was required; the D-002 fix in iteration 2 had already updated both locations consistently. D-005 is confirmed resolved.

**D-006 fix (H-31 C2/C3 missing "or irreversible"):**
- H-31 C2: Added "or irreversible" after "destructive" — now reads: "NEVER proceed on a request that has multiple valid interpretations, unclear scope, or destructive or irreversible implications."
- H-31 C3 `<prohibition>`: Added "or irreversible" after "destructive" — now reads: "or the action is destructive or irreversible." Also removed "at least" from "at least one clarifying question" (Fix 4/D-007b) — now reads "asking a clarifying question."
- H-31 C3 `<verify>`: Does not mention "destructive" — no change needed.
- C1 and neutral already contained "destructive or irreversible" — no change needed.
- All four framings now consistently encode both trigger conditions (destructive + irreversible).

**D-007 fix (H-01 C3 missing Task tool prohibition):**
- H-01 C3 `<prohibition>`: Added "NEVER declare the Task tool in a worker agent's allowed_tools." as a second sentence.
- H-01 C3 `<verify>`: Added "The worker agent's allowed_tools does not include the Task tool." as a second verification sentence.
- C2 already contained "NEVER include the Task tool in a worker agent's allowed tools." — no change needed.
- C3 `<prohibition>` and `<verify>` now match the full scope of C2.

**Post-fix cross-condition verification:**
- H-22: inline neutral, table neutral, C1, C2, C3 all reference ONLY `/problem-solving` — confirmed.
- H-31: C1 ("destructive or irreversible"), C2 ("destructive or irreversible"), C3 ("destructive or irreversible"), neutral ("destructive or irreversible") — all four consistent.
- H-01: C2 prohibits spawning AND Task tool declaration; C3 now prohibits spawning AND Task tool declaration — consistent.
- H-31 C3: No "at least" qualifier — confirmed removed.
- Gate report paths in header — confirmed added.

### Iteration 4 (design-agent-002-r4) — D-008, D-009 Content Confound Corrections

Revision performed to address 2 defects identified after iteration 3 gate review.

**D-008 fix (Significant — H-01 C1 and neutral missing Task tool prohibition):**
- H-01 C1: Added "Ensure the Task tool is not included in a worker agent's allowed_tools configuration." at the end — positive imperative form matching NPT-007 (no NEVER, no prohibition language).
- H-01 neutral (inline): Added "The Task tool is restricted from worker agent tool configurations; only orchestrator agents carry it." — factual passive, no imperative.
- H-01 neutral (table row 1): Updated to match inline neutral.
- All four framings (C1, C2, C3, neutral) now cover all 3 sub-requirements: spawning prohibition, results-to-orchestrator, and Task tool configuration restriction.

**D-009 fix (Minor — H-15 C2 critic-passthrough absent from C1/C3/neutral):**
- H-15 C1: Added "Complete a self-review pass before passing deliverables to critics as well." — positive framing, no NEVER.
- H-15 C3 `<prohibition>`: Added "NEVER pass an unreviewed deliverable to a critic." as a second prohibition sentence matching the existing C2 text exactly.
- H-15 C3 `<verify>`: Updated to "before the final deliverable is presented or passed to a critic" to cover both sub-requirements.
- H-15 neutral (inline): Changed "before any deliverable is presented to the user or passed to a downstream critic" to "before any deliverable is presented to the user and before it is passed to a downstream critic" — making both pathways explicit and parallel rather than treating them as alternatives.
- H-15 neutral (table row 10): Updated to match inline neutral.
- All four framings now cover both sub-requirements: self-review before presenting to user AND self-review before passing to critic.

**Semantic equivalence checklist methodology update:**
- Added explicit methodology note: "Enumerate sub-requirements from C2 first (most explicit framing), then verify C1, C3, and neutral each cover every sub-requirement."
- Updated H-01 semantic equivalence entry to enumerate all 3 sub-requirements and confirm all 4 framings cover all 3.
- Updated H-15 semantic equivalence entry to enumerate both sub-requirements and confirm all 4 framings cover both.

**Post-fix cross-condition verification:**
- H-01: C1, C2, C3, neutral — all cover spawning prohibition, results-to-orchestrator, and Task tool configuration restriction — confirmed.
- H-15: C1, C2, C3, neutral — all cover presenting-to-user prohibition and passing-to-critic prohibition — confirmed.
- H-01 C1: Contains no NEVER, no prohibition language — confirmed (uses "Ensure the Task tool is not included...").
- H-15 C1: Contains no NEVER, no prohibition language — confirmed (uses "Complete a self-review pass before...").
- Neutral descriptions: No imperative, no NEVER, no XML in H-01 or H-15 neutrals — confirmed.

---

*Document version: 8.0.0*
*Agent: ps-analyst (design-agent-002), revision by design-agent-002-r2, design-agent-002-r3, design-agent-002-r4, design-agent-002-r5, design-agent-002-r6, design-agent-002-r7, design-agent-002-r8*
*Workflow: ab-testing-20260301-001 / Step 0.2*
*Source verification: constraint-selection.md (PROJ-014-AB-PHASE0-01) + direct source file reads*
*Iteration 1: Initial draft (design-agent-002). Score: 0.856, verdict: REVISE.*
*Iteration 2: D-001 (H-07 C3 sub-rule b), D-002 (H-22 scope), D-003 (C2 purity), D-004 (H-07 neutral negation) fixed by design-agent-002-r2. Gate report: adversary-gates/three-style-rewrites-gate-i2.md.*
*Iteration 3: D-005 (H-22 table neutral scope), D-006 (H-31 C2/C3 missing "or irreversible"), D-007 (H-01 C3 Task tool prohibition) fixed by design-agent-002-r3.*
*Iteration 4: D-008 (H-01 C1/neutral missing Task tool restriction), D-009 (H-15 C1/C3/neutral missing critic-passthrough) fixed by design-agent-002-r4.*
*Iteration 5: D-010 (H-01 C1 embedded negative construction "is not included" → "Omit") fixed by design-agent-002-r5. Checklist updated to scan for embedded negatives in addition to direct prohibition language.*
*Iteration 6: D-011 (H-22 C1 temporal negation "not after" removed) fixed. Checklist extended with Category 3 (temporal/modal negation). Header gate links for i3-i5 added.*
*Iteration 7: D-012 (H-31 C1 adverbial negation "without asking" removed — conditional clause fully establishes scope) fixed. Comprehensive word-by-word negation sweep of all 10 C1 entries performed against all three categories — no additional negation forms found. Checklist expanded to full Category 1/2/3 vocabulary, with per-entry sweep confirmation notes. Version: 7.0.0.*
*Iteration 8: D-013 (H-13 C2 conditional clause "when a score falls below the threshold" → bare "NEVER bypass the mandatory revision cycle.") fixed. D-014 (header gate links for i6 and i7 added). Comprehensive sentence-by-sentence C2 purity sweep of all 10 entries performed — three additional conditional/qualifier violations found and fixed: D-013b (H-31 C2 sentence 2 "when ambiguity is present" conditional removed; consolidated to "NEVER proceed on an ambiguous request without clarification. NEVER assume intent."), D-013c (H-22 C2 sentence 2 "until after work has started" temporal qualifier removed; now "NEVER delay skill invocation."), D-013d (T1-T5 C2 sentence 2 "when read-only access is sufficient" conditional removed; now "NEVER grant unnecessary tool access."). Semantic equivalence entries for H-31, H-22, and T1-T5 updated to reflect revised C2 text. C2 format checklist rewritten with per-sentence sentence-level audit. Version: 8.0.0.*
*Next: C4 Adversary Gate 8 (adv-scorer >= 0.95)*
