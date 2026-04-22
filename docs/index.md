# Jerry Framework

> Jerry: a Claude Code plugin with 30 expert skills, quality guardrails, and filesystem-based memory.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Why Jerry?](#why-jerry) | What problems Jerry solves |
| [What is Jerry?](#what-is-jerry) | Framework overview and core capabilities |
| [Platform Support](#platform-support) | Supported platforms and status |
| [Quick Start](#quick-start) | Get up and running in minutes |
| [Known Limitations](#known-limitations) | Current constraints and caveats |
| [Guides](#guides) | Playbooks for each skill |
| [Reference](#reference) | Developer and contributor docs |
| [Available Skills](#available-skills) | Skill commands with purpose descriptions |
| [License](#license) | Open source license information |

---

## Why Jerry?

**Your context window is not infinite.** Once sessions exceed 50K-100K tokens, LLMs begin losing track of earlier instructions — rules get skipped, conventions drift, and output quality degrades silently. Jerry externalizes rules and state to the filesystem and re-injects critical constraints every prompt, so they are enforced reliably regardless of context depth.

**Quality should be measurable, not subjective.** Jerry scores every deliverable against a six-dimension rubric and enforces a minimum threshold. Below the threshold, work is revised — not shipped.

**Knowledge should accumulate, not evaporate.** Every research finding, architecture decision, and analysis result is written to a file. When you return to a project next week or next month, the knowledge is still there.

**Complex work needs structure.** Multi-phase workflows with parallel agents, quality gates, and cross-session state tracking are first-class citizens in Jerry, not afterthoughts bolted onto a chat interface.

---

## What is Jerry?

Jerry is a Claude Code plugin with a curated library of methodology-grade skills, behavioral guardrails, and persistent knowledge management — keeping Claude's work consistent and high-quality across sessions. It addresses the **Context Rot** problem (Claude's performance degrades as context fills) by treating the filesystem as infinite memory: rules, worktracker, knowledge, and decisions persist to disk and load selectively per task.

### Core Capabilities

- **Behavioral Guardrails** -- A 5-layer enforcement system with 24 HARD rules that cannot be overridden, plus MEDIUM and SOFT tiers. Rules auto-load at session start via hooks, get re-injected every prompt (~600 tokens/prompt), and persist through context compaction. Total enforcement budget: ~15,100 tokens (7.6% of 200K context).

- **Workflow Orchestration** -- Coordinate multi-phase, multi-agent workflows with persistent state tracking. Fan-out parallel work, synchronize at barriers, and resume across sessions with checkpoint recovery.

- **Knowledge Persistence** -- Every skill invocation produces a persisted artifact on disk (research, analysis, decisions, reviews). These survive session boundaries and context compaction, building a cumulative project knowledge base.

- **Quality Enforcement** -- A quantitative quality gate (>= 0.92 weighted composite score) with a creator-critic-revision cycle (minimum 3 iterations). Six scoring dimensions (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability) with calibrated weights ensure deliverables meet a consistent standard before acceptance.

- **Adversarial Review** -- Ten adversarial strategies across 4 families (Iterative Self-Correction, Dialectical Synthesis, Role-Based Adversarialism, Structured Decomposition) applied at 4 criticality levels (C1 Routine through C4 Critical tournament review with all 10 strategies).

### Jargon Quick Reference

A few terms used in the Core Capabilities section:

| Term | Meaning |
|------|---------|
| **Context Rot** | The observed degradation in LLM output quality as the context window fills — rules get skipped, earlier instructions forgotten, output drifts. Jerry's core design response is to externalize rules and state to files and re-inject critical constraints every prompt. |
| **HARD / MEDIUM / SOFT rules** | Jerry's three-tier rule system. HARD rules cannot be overridden and are blocked at the tooling level. MEDIUM rules are enforced but can be deviated from with documented justification. SOFT rules are conventions — suggested but not enforced. |
| **Creator-critic-revision cycle** | A required iteration pattern for non-trivial deliverables. The creator agent produces a draft, a critic agent reviews it against quality criteria, the creator revises based on feedback. Repeats until the quality score clears a threshold (default 0.92). |
| **Tournament review** | The highest-criticality review mode (C4). All ten adversarial strategies execute against the deliverable. Used for constitutional changes, security-relevant designs, and wave-exit gates. |

---

## Platform Support

Jerry is **primarily developed and tested on macOS**. Cross-platform portability is actively being improved.

| Platform | Status |
|----------|--------|
| **macOS** | Primary — fully supported |
| **Linux** | Expected to work — CI runs on Ubuntu, not primary dev platform |
| **Windows** | In progress — core functionality works, edge cases may exist |

Jerry's CI pipeline tests on macOS, Ubuntu, and Windows. Encountering a platform-specific issue? File a report using the template for your platform:

- [macOS issue](https://github.com/geekatron/jerry/issues/new?template=macos-compatibility.yml)
- [Linux issue](https://github.com/geekatron/jerry/issues/new?template=linux-compatibility.yml)
- [Windows issue](https://github.com/geekatron/jerry/issues/new?template=windows-compatibility.yml)

---

> **Early Access Notice:** Jerry is under active development. The framework is functional and used in production workflows, but APIs, skill interfaces, and configuration formats may change between releases. See [releases](https://github.com/geekatron/jerry/releases) for version history. For version pinning, see the [Local Clone Install](INSTALLATION.md#local-clone) section.

---

## Quick Start

### 1. Install Jerry

In Claude Code, run two commands:

```
/plugin marketplace add https://github.com/geekatron/jerry
/plugin install jerry@geekatron-jerry
```

Verify: `/plugin` > **Installed** tab > `jerry` appears. See the full [Installation Guide](INSTALLATION.md) for scope options, local clone fallback, and troubleshooting.

### 2. Enable Hooks (Recommended)

Install [uv](https://docs.astral.sh/uv/) to enable Jerry's hooks for session context auto-loading and per-prompt quality enforcement:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # macOS/Linux
```

Restart your terminal. See the [Installation Guide](INSTALLATION.md#enable-hooks-early-access) for Windows instructions and the full [Capability Matrix](INSTALLATION.md#capability-matrix).

### 3. Create a Project and Start Working

Set up your first project and invoke a skill:

```bash
export JERRY_PROJECT=PROJ-001-my-first-project
mkdir -p projects/PROJ-001-my-first-project/.jerry/data/items
```

Then follow the [Getting Started Runbook](runbooks/getting-started.md) for a guided walkthrough from project setup to your first persisted skill output.

---

## Known Limitations

- **Skill and agent definitions are not yet optimized.** Current definitions are comprehensive but verbose. Optimization for token efficiency and best-practice alignment is planned for upcoming releases.
- **Windows portability is in progress.** Some hooks and scripts may behave differently on Windows. See [Platform Support](#platform-support) above.

---

## Guides

| Guide | Description |
|-------|-------------|
| [Getting Started Runbook](runbooks/getting-started.md) | Step-by-step from installation to first skill invocation |
| [Problem-Solving Playbook](playbooks/problem-solving.md) | Research, analysis, architecture decisions, and 9 specialized agents |
| [Orchestration Playbook](playbooks/orchestration.md) | Multi-phase workflows with parallel pipelines and quality gates |
| [Transcript Playbook](playbooks/transcript.md) | Meeting transcript parsing with domain-specific entity extraction |
| [Plugin Development](playbooks/PLUGIN-DEVELOPMENT.md) | Developing and distributing Claude Code plugins |

---

## Reference

| Document | Description |
|----------|-------------|
| [CLAUDE.md Guide](CLAUDE-MD-GUIDE.md) | How Jerry's tiered context loading works and how to modify it |
| [Jerry Constitution](governance/JERRY_CONSTITUTION.md) | Behavioral principles governing all Jerry agents |
| [Installation Guide](INSTALLATION.md) | Full installation and setup instructions |
| [Bootstrap Guide](BOOTSTRAP.md) | Context distribution setup (developers only) |

---

## Available Skills

Jerry ships with 30 skills organized by functional area. Top-level skills are user-invocable via their `/command`; sub-skills under `/user-experience` are auto-routed by the parent skill based on the work requested.

### Core Workflow

| Skill | Command | Purpose |
|-------|---------|---------|
| Problem-Solving | `/problem-solving` | Research, analysis, root cause investigation |
| Orchestration | `/orchestration` | Multi-phase workflow coordination |
| Work Tracker | `/worktracker` | Task and work item management |
| Architecture | `/architecture` | Design decisions and ADRs |
| Adversary | `/adversary` | Adversarial quality reviews, tournament scoring, strategy templates |
| AST | `/ast` | Markdown AST parsing, query, validation, frontmatter modification |
| Bootstrap | `/bootstrap` | Context distribution and onboarding for new Jerry environments |

### Engineering

| Skill | Command | Purpose |
|-------|---------|---------|
| Engineering Team | `/eng-team` | Secure software engineering methodology (10 agents: architecture, implementation, quality, incident response) |
| Red Team | `/red-team` | Offensive security testing methodology (11 agents: recon, exploitation, post-exploitation, reporting) |
| NASA SE | `/nasa-se` | Systems engineering processes — requirements, V&V, technical reviews |

### Product & Marketing

| Skill | Command | Purpose |
|-------|---------|---------|
| PM/PMM | `/pm-pmm` | Product management and marketing (5 agents: strategy, customer insight, market, business, competitive) |

### Documentation & Specification

| Skill | Command | Purpose |
|-------|---------|---------|
| Diataxis | `/diataxis` | Four-quadrant documentation methodology (6 agents: 4 writers, classifier, auditor) |
| Use Case | `/use-case` | Guided use case authoring and decomposition (2 agents: Cockburn 12-step author, Jacobson UC 2.0 slicer) |
| Test Spec | `/test-spec` | BDD test specification from use cases (2 agents: Clark transformation generator, 7 Cs coverage analyst) |
| Contract Design | `/contract-design` | API contract generation from use cases (2 agents: UC-to-OpenAPI generator, 9-step validator) |

### Prompting & Content

| Skill | Command | Purpose |
|-------|---------|---------|
| Prompt Engineering | `/prompt-engineering` | Structured prompt construction, NPT constraint generation, prompt quality scoring (3 agents) |
| Transcript | `/transcript` | Meeting transcript parsing with domain-specific entity extraction |

### User Experience (parent + 10 sub-skills)

| Skill | Command | Purpose |
|-------|---------|---------|
| User Experience | `/user-experience` | AI-augmented UX methodology for tiny teams (11 agents: orchestrator + 10 framework specialists) |
| UX JTBD | *(via `/user-experience`)* | Jobs-to-Be-Done research and analysis |
| UX Kano Model | *(via `/user-experience`)* | Kano feature classification by satisfaction impact |
| UX HEART Metrics | *(via `/user-experience`)* | Google HEART framework for UX measurement |
| UX Heuristic Eval | *(via `/user-experience`)* | Nielsen 10-heuristic evaluation |
| UX Inclusive Design | *(via `/user-experience`)* | WCAG 2.2 accessibility evaluation + Microsoft Inclusive Design |
| UX Atomic Design | *(via `/user-experience`)* | Component taxonomy (Atoms/Molecules/Organisms/Templates/Pages) |
| UX Behavior Design | *(via `/user-experience`)* | Fogg B=MAP behavior bottleneck diagnosis |
| UX Lean UX | *(via `/user-experience`)* | Hypothesis-driven design and ICE-prioritized experiments |
| UX Design Sprint | *(via `/user-experience`)* | AJ&Smart 4-day design sprint facilitation |
| UX AI-First Design | *(via `/user-experience`)* | Trust-calibrated AI interaction patterns |

### Voice

| Skill | Command | Purpose |
|-------|---------|---------|
| Saucer Boy | `/saucer-boy` | Session conversational voice (McConkey personality) |
| Saucer Boy Framework Voice | `/saucer-boy-framework-voice` | Internal: framework output voice quality gate, persona compliance |

---

## License

Jerry Framework is open source under the [Apache License 2.0](https://github.com/geekatron/jerry/blob/main/LICENSE).
