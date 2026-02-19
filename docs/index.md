# Jerry Framework

> Behavioral guardrails and workflow orchestration for Claude Code. Accrues knowledge, wisdom, experience.

## Document Sections

| Section | Purpose |
|---------|---------|
| [What is Jerry?](#what-is-jerry) | Framework overview and core capabilities |
| [Why Jerry?](#why-jerry) | Key reasons to adopt Jerry |
| [Platform Support](#platform-support) | Supported platforms and status |
| [Quick Start](#quick-start) | Get up and running in minutes |
| [Known Limitations](#known-limitations) | Current constraints and caveats |
| [Guides](#guides) | Playbooks for each skill |
| [Reference](#reference) | Developer and contributor docs |
| [Available Skills](#available-skills) | Skill commands with purpose descriptions |
| [License](#license) | Open source license information |

---

## What is Jerry?

Jerry is a Claude Code plugin that provides **behavioral guardrails**, **workflow orchestration**, and **persistent knowledge management** for AI-assisted development sessions. It solves the core problem of **Context Rot** -- the degradation of LLM performance as context windows fill -- by using the filesystem as infinite memory.

### Core Capabilities

- **Behavioral Guardrails** -- A layered rule system (HARD / MEDIUM / SOFT) that enforces coding standards, architecture constraints, and quality thresholds across every session. Rules auto-load at session start and persist through context compaction.

- **Workflow Orchestration** -- Coordinate multi-phase, multi-agent workflows with persistent state tracking. Fan-out parallel work, synchronize at barriers, and resume across sessions with checkpoint recovery.

- **Knowledge Persistence** -- Every skill invocation produces a persisted artifact on disk. Research, analysis, decisions, and reviews survive session boundaries and build a cumulative project knowledge base.

- **Quality Enforcement** -- A quantitative quality gate (>= 0.92 weighted composite score) with a creator-critic-revision cycle. Six scoring dimensions ensure deliverables meet a consistent standard before acceptance.

- **Adversarial Review** -- Ten adversarial strategies (Red Team, Devil's Advocate, Steelman, Pre-Mortem, FMEA, and more) applied at appropriate criticality levels to catch blind spots, strengthen ideas, and prevent premature conclusions.

---

## Why Jerry?

**Your context window is not infinite.** As sessions grow, LLMs lose track of earlier instructions, skip rules, and produce inconsistent output. Jerry externalizes rules and state to the filesystem so they are reloaded reliably every session, every time.

**Quality should be measurable, not subjective.** Jerry scores every deliverable against a six-dimension rubric and enforces a minimum threshold. Below the threshold, work is revised -- not shipped.

**Knowledge should accumulate, not evaporate.** Every research finding, architecture decision, and analysis result is written to a file. When you return to a project next week or next month, the knowledge is still there.

**Complex work needs structure.** Multi-phase workflows with parallel agents, quality gates, and cross-session state tracking are first-class citizens in Jerry, not afterthoughts bolted onto a chat interface.

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

> **Early Access Notice:** Jerry is under active development. The framework is functional and used in production workflows, but APIs, skill interfaces, and configuration formats may change between releases. Pin to a specific [release tag](https://github.com/geekatron/jerry/releases) if you need stability (e.g., `git clone --branch v1.0.0 https://github.com/geekatron/jerry.git`).

---

## Quick Start

### 1. Install Jerry

Follow the [Installation Guide](INSTALLATION.md) for platform-specific setup (macOS and Windows). You will need Git, uv, and Claude Code.

### 2. Bootstrap Context

From the cloned Jerry repository root, run the bootstrap to set up the context distribution (requires uv — installed in Step 1):

```bash
cd ~/plugins/jerry
uv run python scripts/bootstrap_context.py
```

See the [Bootstrap Guide](BOOTSTRAP.md) for details.

### 3. Create a Project and Start Working

Set up your first project inside the Jerry clone and invoke a skill:

```bash
export JERRY_PROJECT=PROJ-001-my-first-project
mkdir -p projects/PROJ-001-my-first-project/.jerry/data/items
```

> **Note:** This creates the project directory inside your Jerry clone (`~/plugins/jerry/projects/`). To use Jerry on a separate repository, run these commands from that repository's root instead.

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
| [Bootstrap Guide](BOOTSTRAP.md) | Context distribution setup after cloning |

---

## Available Skills

| Skill | Command | Purpose |
|-------|---------|---------|
| Problem-Solving | `/problem-solving` | Research, analysis, architecture decisions |
| Orchestration | `/orchestration` | Multi-phase workflow coordination |
| Work Tracker | `/worktracker` | Task and work item management |
| Transcript | `/transcript` | Meeting transcript parsing |
| NASA SE | `/nasa-se` | Systems engineering processes |
| Architecture | `/architecture` | Design decisions and ADRs |
| Adversary | `/adversary` | Adversarial quality reviews and tournament scoring |

---

## License

Jerry Framework is open source under the [Apache License 2.0](https://github.com/geekatron/jerry/blob/main/LICENSE).
