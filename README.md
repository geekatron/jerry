# Jerry Framework

> A Claude Code plugin for behavior and workflow guardrails with knowledge accrual.

[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-blue.svg)](https://code.claude.com)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

## What is Jerry?

Jerry is a **Claude Code plugin** that adds structured problem-solving capabilities, work tracking, and knowledge management to your Claude Code sessions. It combats **Context Rot**—the phenomenon where LLM performance degrades as context fills—through persistent artifacts and filesystem-based memory.

> **Note:** You do NOT need Python installed to use Jerry. The plugin runs within Claude Code using its built-in capabilities. Python is only required if you want to contribute to Jerry's development.

> "The effective context window where models perform optimally is often <256k tokens, far below advertised limits."
> — [Chroma Research](https://research.trychroma.com/context-rot)

## Quick Start

### Prerequisites

- [Claude Code](https://code.claude.com) installed and configured
- [Git](https://git-scm.com/) for cloning the repository
- [uv](https://docs.astral.sh/uv/) for Python dependency management (required for hooks)

### Installation

Jerry is installed via a **local marketplace**. Choose your platform:

<details>
<summary><strong>macOS</strong></summary>

```bash
# 1. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone Jerry to a local directory
mkdir -p ~/plugins
git clone https://github.com/geekatron/jerry.git ~/plugins/jerry

# 3. In Claude Code, add the local marketplace
/plugin marketplace add ~/plugins/jerry

# 4. Install the Jerry plugin
/plugin install jerry@jerry-framework
```

</details>

<details>
<summary><strong>Windows (PowerShell)</strong></summary>

```powershell
# 1. Install uv (if not already installed)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Restart your terminal to update PATH, then verify
uv --version

# 3. Clone Jerry to a local directory
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\plugins"
git clone https://github.com/geekatron/jerry.git "$env:USERPROFILE\plugins\jerry"

# 4. In Claude Code, add the local marketplace (use forward slashes)
/plugin marketplace add C:/Users/$env:USERNAME/plugins/jerry

# 5. Install the Jerry plugin
/plugin install jerry@jerry-framework
```

</details>

### Verify Installation

After installation, run `/plugin` in Claude Code and check the **Installed** tab. You should see `jerry` listed.

See [docs/INSTALLATION.md](docs/INSTALLATION.md) for detailed instructions and troubleshooting.

## Platform Support

Jerry is **primarily developed and tested on macOS**. We are actively working on cross-platform portability, with Windows support as the immediate priority.

| Platform | Status |
|----------|--------|
| **macOS** | Primary — fully supported |
| **Linux** | Expected to work — not regularly tested |
| **Windows** | In progress — core functionality works, edge cases may exist |

**Encountering a platform-specific issue?** File a report using the template for your platform:

- [macOS issue](https://github.com/geekatron/jerry/issues/new?template=macos-compatibility.yml)
- [Linux issue](https://github.com/geekatron/jerry/issues/new?template=linux-compatibility.yml)
- [Windows issue](https://github.com/geekatron/jerry/issues/new?template=windows-compatibility.yml)

Your reports directly drive portability improvements.

> Jerry's CI pipeline tests on macOS, Ubuntu, and Windows. See [CONTRIBUTING.md](CONTRIBUTING.md) for platform-specific development notes.

## Known Limitations

- **Skill and agent definitions are not yet optimized.** Current definitions are comprehensive but verbose. Optimization for token efficiency and best-practice alignment is on the roadmap for upcoming releases.
- **Windows portability is in progress.** Some hooks and scripts may behave differently on Windows. See [Platform Support](#platform-support) above.

## Using Jerry

Jerry provides **skills**—natural language interfaces you invoke with slash commands:

<!-- BEGIN:GENERATED:SKILLS_TABLE -->
| Skill | Purpose | Example |
|-------|---------|---------|
| `/adversary` | On-demand adversarial quality reviews using strategy temp... | "Run adversarial review on this ADR" |
| `/architecture` | This skill should be used when the user asks to "design s... | "Create ADR for caching strategy" |
| `/ast` | Markdown AST operations for Jerry documents. Provides str... | "Validate entity frontmatter" |
| `/bootstrap` | This skill should be used when the user says "bootstrap",... | "Bootstrap Jerry" |
| `/contract-design` | API contract generation from use case realization artifac... | "Generate OpenAPI contract from use case" |
| `/diataxis` | Four-quadrant documentation framework. Produces tutorials... | "Write a tutorial for the CLI" |
| `/eng-team` | Secure engineering team skill providing methodology guida... | "Threat model the auth service" |
| `/nasa-se` | NASA Systems Engineering skill implementing NPR 7123.1D p... | "Define requirements for API" |
| `/orchestration` | Multi-agent workflow orchestration with state tracking, c... | "Orchestrate the release pipeline" |
| `/pm-pmm` | Product management and product marketing decision framewo... | "Create product strategy PRD" |
| `/problem-solving` | Structured problem-solving framework with specialized age... | "Research OAuth2 patterns" |
| `/prompt-engineering` | Structured prompt construction and quality validation for... | "Build structured prompt for analysis" |
| `/red-team` | Offensive security team skill providing methodology guida... | "Recon the target application" |
| `/saucer-boy` | Session conversational voice with McConkey personality. I... | "Give me a pep talk" |
| `/saucer-boy-framework-voice` | INTERNAL SKILL — auto-loaded for framework output voice q... | "Auto-loaded for output text" |
| `/test-spec` | BDD test specification generation from use case artifacts... | "Generate test specification" |
| `/transcript` | Parse, extract, and format transcripts (VTT, SRT, plain t... | "Parse the meeting notes" |
| `/use-case` | Guided use case authoring and decomposition using Cockbur... | "Create use case for login flow" |
| `/user-experience` | Parent orchestrator for AI-augmented UX methodology targe... | "Run UX audit on dashboard" |
| `/ux-ai-first-design` | AI-first interaction design sub-skill (CONDITIONAL) for t... | "Evaluate AI-first design patterns" |
| `/ux-atomic-design` | Atomic Design component taxonomy sub-skill for the /user-... | "Build component taxonomy" |
| `/ux-behavior-design` | Fogg Behavior Model B=MAP bottleneck diagnosis sub-skill ... | "Map user behavior triggers" |
| `/ux-design-sprint` | AJ&Smart Design Sprint 2.0 facilitation sub-skill for the... | "Plan 5-day design sprint" |
| `/ux-heart-metrics` | HEART Metrics framework sub-skill for the /user-experienc... | "Define HEART metrics for feature" |
| `/ux-heuristic-eval` | Nielsen heuristic evaluation sub-skill for the /user-expe... | "Run heuristic evaluation" |
| `/ux-inclusive-design` | Inclusive design and WCAG 2.2 accessibility evaluation su... | "Audit for accessibility compliance" |
| `/ux-jtbd` | Jobs-to-Be-Done research and analysis sub-skill for the /... | "Map jobs to be done" |
| `/ux-kano-model` | Kano model feature classification and prioritization sub-... | "Classify features with Kano model" |
| `/ux-lean-ux` | Lean UX hypothesis-driven design sub-skill for the /user-... | "Define lean UX hypothesis" |
| `/worktracker` | Work item tracking and task management using the Jerry Fr... | "Create a task for login feature" |

<!-- END:GENERATED:SKILLS_TABLE -->

### Example Session

```
You: /problem-solving analyze why the tests are failing

Claude: I'll invoke the ps-analyst agent to investigate...
        [Creates persistent analysis artifact]

        Root cause identified: Missing mock for external API call in
        test_auth_service.py:45. The test expects a response object
        but receives None.

        Analysis saved to: docs/analysis/EN-001-e-001-test-failures.md
```

All outputs are **persisted to files**, surviving context compaction and building your project's knowledge base.

## Features

<!-- BEGIN:GENERATED:FEATURES -->
- **89 Specialized Agents** across 30 skills — from research and analysis to security testing and infrastructure hardening. See [AGENTS.md](AGENTS.md) for the full registry.
- **Structured Problem-Solving**: 9 agents (researcher, analyst, architect, validator, synthesizer, reviewer, critic, investigator, reporter) with adversarial quality gates
- **Work Tracking**: Local task management with status, priorities, dependencies, and template-enforced consistency
- **Knowledge Accrual**: Persistent artifacts in `projects/` that survive session boundaries
- **NASA Systems Engineering**: 10 agents implementing NPR 7123.1D processes for mission-grade rigor
- **Multi-Agent Orchestration**: Coordinate complex workflows with parallel pipelines, sync barriers, and checkpointing
- **Adversarial Quality Reviews**: 10 adversarial strategies (Red Team, Devil's Advocate, Pre-Mortem, FMEA, and more) with LLM-as-Judge scoring
- **Secure Engineering**: 10 agents covering threat modeling (STRIDE), secure code review (OWASP ASVS), DevSecOps pipelines, and incident response
- **Offensive Security**: 11 agents covering the full MITRE ATT&CK kill chain — reconnaissance through reporting — with mandatory scope authorization
- **AST-Based Parsing**: Structured markdown frontmatter extraction for worktracker entities and validation

<!-- END:GENERATED:FEATURES -->

## Documentation

| Document | Purpose |
|----------|---------|
| [Installation Guide](docs/INSTALLATION.md) | Detailed setup instructions for all platforms |
| [CLAUDE.md](CLAUDE.md) | Context for Claude Code sessions |
| [AGENTS.md](AGENTS.md) | Registry of available agents |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute to Jerry development |

## For Contributors

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and contribution guidelines.

Quick development setup:

```bash
git clone https://github.com/geekatron/jerry.git
cd jerry
uv sync
uv run pytest
```

## References

- [Claude Code Plugin Documentation](https://code.claude.com/docs/en/discover-plugins)
- Cockburn, A. (2005). "[Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)"
- Chroma. "[Context Rot Research](https://research.trychroma.com/context-rot)"

## License

Apache-2.0 — See [LICENSE](LICENSE) and [NOTICE](NOTICE) for details.
