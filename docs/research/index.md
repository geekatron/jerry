# Research

> Jerry's development is driven by evidence-based research. Every architectural decision, quality framework component, and workflow pattern is backed by structured research artifacts with citations, formal methodologies, and multi-perspective analysis.

This section curates the key research produced during Jerry's development. Each page presents key findings inline with expandable methodology details and links to the full research artifacts on GitHub.

---

## Research Domains

| Domain | Pages | Description |
|--------|-------|-------------|
| [Adversarial Strategies & Quality](#adversarial-strategies--quality) | 3 | How we selected and implemented 10 adversarial review strategies from 36 candidates |
| [Agent Architecture](#agent-architecture) | 1 | Evidence-based analysis of single vs. multi-agent orchestration |
| [Context Management](#context-management) | 1 | Solving context rot in LLM sessions |
| [Skill Architecture](#skill-architecture) | 1 | Compliance framework for Claude Code skill patterns |
| [Governance](#governance) | 1 | Constitutional AI governance for LLM agents |
| [OSS Release Methodology](#oss-release-methodology) | 1 | FMEA, root cause analysis, and best practices for open-sourcing |
| [Software Architecture](#software-architecture) | 1 | Hexagonal, DDD, and CQRS patterns in Python |
| [Claude Code Ecosystem](#claude-code-ecosystem) | 1 | Plugin, skill, and CLI patterns |

**Total:** 47 research artifacts across 9 domains, ~28,000 lines of documented research.

---

## Adversarial Strategies & Quality

The adversarial quality framework was built through a rigorous research pipeline: 36 strategies cataloged from academic, industry, and emerging sources, narrowed to 15 through deduplication, then scored and selected to a final 10 using NASA SE trade study methodology.

<div class="grid cards" markdown>

-   **Adversarial Strategy Catalog**

    ---

    Unified catalog of 15 adversarial review strategies synthesized from academic literature (CIA, DoD, Hegelian dialectics), industry practices, and emerging AI patterns. 117+ citations.

    [:octicons-arrow-right-24: Strategy Catalog](adversarial-strategy-catalog.md)

-   **Strategy Selection & Enforcement (ADRs)**

    ---

    Two architecture decision records: selection of the final 10 strategies with composite scoring, and design of the 5-layer enforcement architecture with token budget feasibility analysis.

    [:octicons-arrow-right-24: ADRs](strategy-selection-enforcement.md)

-   **Adversarial Quality Deep Dives**

    ---

    Trade studies, risk registers (FMEA), scoring methodology, and the strategy selection decision tree. Supporting research behind the headline decisions.

    [:octicons-arrow-right-24: Deep Dives](adversarial-deep-dives.md)

</div>

---

## Agent Architecture

<div class="grid cards" markdown>

-   **Single vs. Multi-Agent Orchestration**

    ---

    Evidence-based analysis drawing on 20 peer-reviewed sources (ACL, ICLR, ICML, EMNLP, NeurIPS). Quantitative findings on when multi-agent helps vs. hurts, with context rot as the primary mechanism.

    [:octicons-arrow-right-24: Agent Analysis](single-vs-multi-agent.md)

</div>

---

## Context Management

<div class="grid cards" markdown>

-   **Context Management & LLM Performance**

    ---

    Research on context rot thresholds, CLAUDE.md optimization (50-70% token savings quantified), decomposition patterns, and cross-platform sync strategies.

    [:octicons-arrow-right-24: Context Management](context-management.md)

</div>

---

## Skill Architecture

<div class="grid cards" markdown>

-   **Skill Compliance Framework**

    ---

    2,646-line compliance framework with 117 checkpoints across 8 orchestration patterns. Reusable for any Claude Code skill. Includes 4-phase remediation roadmap.

    [:octicons-arrow-right-24: Skill Framework](skill-compliance-framework.md)

</div>

---

## Governance

<div class="grid cards" markdown>

-   **Governance & Constitutional AI**

    ---

    The Jerry Constitution implements Constitutional AI for LLM agent governance, drawing on Anthropic, OpenAI, and DeepMind prior art. Progressive enforcement from advisory to hard constraints.

    [:octicons-arrow-right-24: Governance](governance-constitutional-ai.md)

</div>

---

## OSS Release Methodology

<div class="grid cards" markdown>

-   **OSS Preparation & Methodology**

    ---

    FMEA risk analysis (21 risks scored), 5 Whys root cause analysis, gap analysis, and best practices research from Google, Microsoft, and Apache Foundation sources.

    [:octicons-arrow-right-24: OSS Methodology](oss-methodology.md)

</div>

---

## Software Architecture

<div class="grid cards" markdown>

-   **Software Architecture & Patterns**

    ---

    Python architecture standards (Hexagonal + DDD + CQRS), teaching-edition walkthroughs, and domain-specific playbooks.

    [:octicons-arrow-right-24: Architecture](architecture-patterns.md)

</div>

---

## Claude Code Ecosystem

<div class="grid cards" markdown>

-   **Claude Code Ecosystem**

    ---

    Research on Claude Code CLI patterns, plugin architecture and distribution, skill structure and agent design patterns.

    [:octicons-arrow-right-24: Ecosystem](claude-code-ecosystem.md)

</div>

---

## How Research is Conducted

Jerry uses a structured research pipeline with specialized agents:

1. **ps-researcher** gathers information with source citations (L0/L1/L2 structure)
2. **ps-analyst** applies formal methodologies (5 Whys, FMEA, gap analysis, trade studies)
3. **ps-architect** produces Architecture Decision Records (ADRs) in Nygard format
4. **ps-synthesizer** extracts cross-cutting patterns from multiple research documents
5. **ps-critic** reviews deliverables against a 6-dimension quality rubric (>= 0.92 threshold)

All research artifacts are persisted to the filesystem and survive context compaction, building a cumulative knowledge base across sessions.

[:octicons-link-external-16: Full research catalog on GitHub](https://github.com/geekatron/jerry/blob/main/projects/PROJ-001-oss-release/research/bug008-research-catalog.md){ .md-button }
