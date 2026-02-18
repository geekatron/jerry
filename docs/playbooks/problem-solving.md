# Problem-Solving Playbook

> **Skill:** problem-solving
> **SKILL.md:** [problem-solving/SKILL.md](../../skills/problem-solving/SKILL.md)
> **Trigger keywords:** research, analyze, investigate, explore, root cause, why

## Document Sections

| Section | Purpose |
|---------|---------|
| [When to Use](#when-to-use) | Activation criteria and exclusions |
| [Prerequisites](#prerequisites) | What must be in place before invoking |
| [Step-by-Step](#step-by-step) | Primary invocation path |
| [Agent Reference](#agent-reference) | All 9 agents with roles, triggers, and output locations |
| [Agent Selection Table](#agent-selection-table) | Keyword-to-agent decision table |
| [Creator-Critic-Revision Cycle](#creator-critic-revision-cycle) | Quality workflow for C2+ deliverables |
| [Examples](#examples) | Concrete invocation examples |
| [Troubleshooting](#troubleshooting) | Common failure modes |
| [Related Resources](#related-resources) | Cross-references to other playbooks and SKILL.md |

---

## When to Use

### Use this skill when:

- You need to **research** a new technology, approach, or unfamiliar topic
- You need to **analyze** data, code behavior, or a system to understand patterns or gaps
- You need to **investigate** a failure, incident, or unexpected behavior
- You need to **explore** options or approaches before making a decision
- You need to determine the **root cause** of a problem (bugs, performance issues, test failures, outages)
- You are asking **why** something is happening and need structured evidence before concluding
- You are making an architecture decision that needs documented rationale (ADR)
- You need to validate that constraints or requirements are satisfied with evidence
- You need to synthesize findings across multiple prior documents into themes or recommendations
- You need a code, design, or security quality review
- You need a status or progress report with metrics

### Do NOT use this skill when:

- You need iterative improvement of a deliverable with formal adversarial strategies — use `/adversary` for standalone adversarial reviews, tournament scoring, or formal strategy application (S-001 through S-014)
- You need to manage tasks and issues — use `/worktracker`
- You need to run a multi-phase orchestrated workflow with gates — use `/orchestration`
- The task is a simple one-step lookup or clarification that does not require a persisted artifact
- You need to parse a transcript file — use `/transcript` with the CLI command

---

## Prerequisites

- `JERRY_PROJECT` environment variable is set to an active project ([H-04](../../.context/rules/quality-enforcement.md#hard-rule-index) — session will not proceed without this)
- A Jerry session is active (`jerry session start` has been run)
- You have a clear problem statement, question, or topic to investigate
- For research or analysis tasks: relevant prior documents are accessible in the repository (optional but recommended — agents will scan for existing context)
- For code review tasks: the code to be reviewed is committed or staged in the repository
- For investigation tasks: symptoms, error logs, or failure evidence are available

---

## Step-by-Step

### Primary Path: Natural language request

1. State your request in natural language, using one of the trigger keywords: `research`, `analyze`, `investigate`, `explore`, `root cause`, or `why`. Example: "Research the trade-offs between SQLite and PostgreSQL for this use case."

2. The orchestrator reads your request and selects the appropriate agent based on the detected keywords and context. You do not need to name the agent explicitly unless you want a specific one.

> **Note on keyword detection:** Keyword detection is probabilistic — the LLM interprets your intent from context, not via exact string matching. If your message contains keywords for multiple skills (e.g., "analyze this orchestration workflow"), the orchestrator uses context to disambiguate. If the wrong skill or agent activates, use explicit invocation as a guaranteed alternative: name the agent directly (e.g., "Use ps-analyst to...") or use the `/problem-solving` slash command.

3. The selected agent begins work. For C2+ deliverables (reversible in 1 day, 3–10 files), expect a **creator-critic-revision cycle** — the agent will produce an initial deliverable, critique it, and revise. See [Creator-Critic-Revision Cycle](#creator-critic-revision-cycle) for details.

4. The agent persists all output to a file in the project's `docs/` subdirectory (e.g., `docs/research/`, `docs/analysis/`, `docs/decisions/`). You will see the file path in the response.

5. Review the persisted artifact. If it does not fully address your need, make a follow-up request — referencing the output file explicitly if you want the same agent to continue from it.

6. For complex problems requiring multiple perspectives, chain agents sequentially: researcher -> analyst -> architect -> validator. Each agent references the previous agent's output file.

### Optional Path: Explicit agent request

If you know which agent you need, name it directly:

```
"Use ps-researcher to explore graph database options."
"Have ps-analyst do a 5 Whys on the login failures."
"I need ps-architect to create an ADR for the new persistence layer."
```

---

## Agent Reference

All 9 problem-solving agents, their roles, invocation triggers, and output locations:

| Agent | Role | Invoke When You Need | Output Location |
|-------|------|----------------------|-----------------|
| `ps-researcher` | Research Specialist — Gathers information with citations from codebase, web, and prior documents | To **research**, **explore**, **find**, or **gather** information on a topic | `docs/research/` |
| `ps-analyst` | Analysis Specialist — Deep analysis using 5 Whys, FMEA, trade-off analysis, gap analysis, risk assessment | To **analyze**, find the **root cause**, assess **trade-offs**, perform a gap or risk analysis | `docs/analysis/` |
| `ps-architect` | Architecture Specialist — Creates Architecture Decision Records (ADRs) in Nygard format with L0/L1/L2 explanations | To document an **ADR**, make an **architecture decision**, **choose** between options | `docs/decisions/` |
| `ps-critic` | Quality Evaluator — Iterative refinement using S-014 (LLM-as-Judge) with quality scores | To **critique**, score, or iteratively **improve** a deliverable; part of H-14 creator-critic cycles | `docs/critiques/` |
| `ps-validator` | Validation Specialist — Verifies constraints and requirements with evidence and traceability matrices | To **validate**, **verify**, check **constraints**, or confirm a requirement is met | `docs/analysis/` |
| `ps-synthesizer` | Synthesis Specialist — Pattern extraction and knowledge generation across multiple documents | To **synthesize**, find **patterns** or **themes**, combine findings, perform meta-analysis | `docs/synthesis/` |
| `ps-reviewer` | Review Specialist — Code, design, architecture, and security quality assessment | To **review** code quality, design quality, or security posture (OWASP) | `docs/reviews/` |
| `ps-investigator` | Investigation Specialist — Root cause of failures and incidents using 5 Whys, Ishikawa diagrams, FMEA | To **investigate** a failure, incident, outage, or debug **what happened** | `docs/investigations/` |
| `ps-reporter` | Reporting Specialist — Status reports with health metrics and progress tracking | To generate a **report**, **status** update, **progress** summary, or health metrics | `docs/reports/` |

**Output file naming convention:** `{ps-id}-{entry-id}-{topic-slug}.md` — for example, `work-024-e-001-test-performance.md`.

All agents produce output at three levels:
- **L0 (ELI5):** Executive summary for non-technical stakeholders
- **L1 (Software Engineer):** Technical implementation details
- **L2 (Principal Architect):** Strategic implications and trade-offs

---

## Agent Selection Table

Use the detected keywords or context clues to select the right agent:

| Detected Keywords / Context | Recommended Agent | Rationale |
|-----------------------------|-------------------|-----------|
| research, explore, find, gather, learn about | `ps-researcher` | Topic is new; need information gathering with citations |
| analyze, root cause, trade-off, gap, risk, 5 whys, FMEA, why is X happening | `ps-analyst` | Need structured analysis with causal reasoning |
| ADR, architecture decision, design choice, choose between, decide on | `ps-architect` | Need a documented, reasoned decision record |
| critique, quality score, evaluate quality, improvement feedback, iterative refinement | `ps-critic` | Need structured quality scoring and revision feedback |
| validate, verify, constraint, requirement met, evidence, traceability | `ps-validator` | Need compliance verification with evidence |
| synthesize, patterns, themes, combine, meta-analysis, across documents | `ps-synthesizer` | Need cross-document pattern extraction |
| review, code review, quality, security, OWASP | `ps-reviewer` | Need quality assessment of an existing artifact |
| investigate, failure, incident, debug, what happened, outage | `ps-investigator` | Need failure root cause with corrective actions |
| report, status, progress, metrics, health | `ps-reporter` | Need structured reporting with metrics |

**Disambiguation — ps-analyst vs ps-investigator:**
- Use `ps-analyst` when analyzing a problem prospectively (trade-offs, gaps, risks, design decisions).
- Use `ps-investigator` when analyzing a failure retrospectively (incident, outage, bug that already occurred).

**Disambiguation — ps-critic vs /adversary:**
- Use `ps-critic` when inside a creator-critic-revision loop — iterative improvement of a deliverable in progress.
- Use `/adversary` when you want a standalone adversarial assessment, tournament scoring, or formal strategy application outside the improvement loop.

---

## Creator-Critic-Revision Cycle

For C2+ deliverables (reversible in up to 1 day, touching 3–10 files), the problem-solving skill enforces a **minimum 3-iteration creator-critic-revision cycle** per H-14 (HARD rule).

**You will observe this cycle when:**
- An agent produces a deliverable, then another pass critiques it and provides a quality score
- The agent revises and re-scores, repeating until the quality threshold is met
- This may happen 3 or more times before the deliverable is presented as final

**Quality threshold (H-13):** The weighted composite score must reach **>= 0.92** for C2+ deliverables. Deliverables below this threshold are rejected and require revision. The six scoring dimensions and their weights are:

| Dimension | Weight |
|-----------|--------|
| Completeness | 0.20 |
| Internal Consistency | 0.20 |
| Methodological Rigor | 0.20 |
| Evidence Quality | 0.15 |
| Actionability | 0.15 |
| Traceability | 0.10 |

**Score bands:**

| Band | Score | Outcome |
|------|-------|---------|
| PASS | >= 0.92 | Deliverable accepted |
| REVISE | 0.85 – 0.91 | Near-threshold — targeted revision required |
| REJECTED | < 0.85 | Significant rework required |

**Circuit breaker:** After the minimum 3 iterations, if no improvement occurs over 2 consecutive cycles, the agent will either accept the deliverable with caveats documented or escalate to the user.

**Criticality auto-escalation rules** apply to problem-solving artifacts:
- Artifacts touching `docs/governance/JERRY_CONSTITUTION.md` = auto-C4 (all 10 adversarial strategies required)
- Artifacts touching `.context/rules/` or `.claude/rules/` = auto-C3 minimum
- New or modified ADRs = auto-C3 minimum

---

## Examples

### Example 1: Researching a new technology

**User request:** "Research best practices for event sourcing in Python"

**System behavior:** The orchestrator detects the keyword `research` and invokes `ps-researcher`. The agent gathers information from the codebase, web sources, and any prior research documents in `docs/research/`. It produces a persisted artifact at a path such as `docs/research/work-024-e-001-event-sourcing.md`. The artifact includes an L0 executive summary, L1 technical details, and L2 strategic implications. Sources are cited. The agent performs a self-review (H-15, S-010 Self-Refine) before presenting the output.

---

### Example 2: Finding the root cause of a failure

**User request:** "Analyze why our test suite is running so slowly — root cause"

**System behavior:** The orchestrator detects `analyze` and `root cause` and invokes `ps-analyst`. The agent applies structured analysis techniques (5 Whys, gap analysis) to the test execution patterns. For a C2 deliverable, a creator-critic-revision cycle runs: the analyst produces an initial root cause analysis, `ps-critic` scores it against the 6-dimension rubric, and revisions are made until the score reaches >= 0.92. The final output is persisted at `docs/analysis/work-024-e-002-root-cause.md`, with corrective action recommendations at all three audience levels (L0/L1/L2).

---

### Example 3: Creating an architecture decision record

**User request:** "Create an ADR for choosing PostgreSQL over SQLite for the persistence layer"

**System behavior:** The orchestrator detects `ADR` and `architecture decision` and invokes `ps-architect`. The agent checks `docs/decisions/` for prior ADRs to ensure numbering and formatting consistency. It creates a new ADR in Nygard format at `docs/decisions/work-024-e-003-adr-persistence.md` with Status: PROPOSED. Because ADRs are auto-C3 (AE-003), a full C3 strategy set applies — the critic applies Devil's Advocate (S-002) and Pre-Mortem Analysis (S-004) in addition to the baseline quality score. The ADR includes L0 (why we chose this), L1 (technical rationale), and L2 (strategic trade-offs).

---

### Example 4: Explicit agent invocation for an investigation

**User request:** "Use ps-investigator to investigate the production API timeout that occurred last night"

**System behavior:** `ps-investigator` is invoked directly (no keyword detection needed — explicit agent name was provided). The agent applies 5 Whys and Ishikawa analysis to available logs, error messages, and system state evidence. It produces a root cause report with corrective actions at `docs/investigations/work-024-e-004-api-timeout.md`. The report distinguishes immediate corrective actions (L1) from systemic preventive measures (L2).

---

## Troubleshooting

| Symptom | Cause | Resolution |
|---------|-------|------------|
| "JERRY_PROJECT not set" or session fails to start | H-04 constraint: no active project is configured | Run `jerry session start` and ensure `JERRY_PROJECT` is set in the environment. See `docs/runbooks/getting-started.md` for setup procedure. |
| Agent produces output but no file appears in `docs/` | [P-002](../governance/JERRY_CONSTITUTION.md#p-002-file-persistence) persistence constraint violated — the agent did not write its output to disk | Re-invoke the agent with an explicit instruction: "Persist your findings to a file in `docs/research/`." All agents MUST write output files per [P-002](../governance/JERRY_CONSTITUTION.md#p-002-file-persistence). |
| Creator-critic cycle runs more than 5 times without reaching 0.92 | Deliverable has a fundamental structural problem; the critic is finding the same gap each iteration | Review the latest critique artifact in `docs/critiques/`. Identify the dimension with the lowest sub-score. Re-state the request with explicit guidance addressing that dimension. |
| Wrong agent was selected for my request | Keyword detection selected a different agent than intended | Use explicit agent naming: "Use ps-investigator to..." — this bypasses keyword selection and directly invokes the named agent. |
| Agent references a prior document that does not contain the expected content | File naming mismatch or document was moved | Ask Claude to search for all markdown files under `docs/` (e.g., "find all .md files in docs/") to verify the actual paths of prior artifacts, then re-invoke the agent with the correct file path. |
| ADR is created but not linked to existing decisions | New ADR lacks cross-references to prior related ADRs in `docs/decisions/` | Ask `ps-architect` to review existing ADRs and add cross-reference links: "Update the ADR to reference related prior decisions in `docs/decisions/`." |
| Quality score stuck at REVISE band (0.85–0.91) | Near-threshold deliverable — one or two dimensions consistently underscoring | Read the critique artifact. Identify the specific dimension gap (e.g., Traceability). Ask the creator agent to address it: "Improve traceability — add explicit links from each recommendation to its evidence source." |
| Agent fails mid-execution (partial output or no output) | Agent encountered an error, token budget exhaustion, or session interruption during processing | **1. Identify:** Check for a partial artifact in the expected output directory (e.g., `docs/research/`). **2. Salvage:** If a partial file exists, it can be used as input for a follow-up invocation. **3. Recover:** Re-invoke the same agent with an explicit file reference: "Use ps-researcher to continue the research from `docs/research/partial-file.md`." The agent will read the existing file and continue from where it left off. |

---

## Related Resources

- [SKILL.md](../../skills/problem-solving/SKILL.md) — Authoritative technical reference for this skill, including agent details, orchestration flow examples, adversarial quality mode, and template locations
- [Orchestration Playbook](./orchestration.md) — When to use the orchestration skill for multi-phase workflows that chain problem-solving agents across gates
- [Transcript Playbook](./transcript.md) — When to use the transcript skill for structured CLI-based transcript parsing before applying problem-solving agents to extracted content
- [Quality Enforcement Standards](../../.context/rules/quality-enforcement.md) — Authoritative SSOT for quality gate thresholds, criticality levels (C1–C4), strategy catalog (S-001–S-014), and auto-escalation rules (AE-001–AE-006)
