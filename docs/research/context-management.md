# Context Management

> Research on context rot thresholds, CLAUDE.md optimization (50-70% token savings quantified), decomposition patterns, and cross-platform sync strategies for LLM-based development tools.

---

## Key Findings

- **50-70% token savings** achievable through CLAUDE.md optimization without losing critical behavioral context
- **Context rot activates at 3,000+ tokens** of instruction density (Xu et al., 2025) — far below technical context window limits
- **Tiered loading patterns** (index/manifest → selective import) dramatically extend effective context lifetime
- **Cross-platform sync** (symlinks vs. copy vs. junction) requires different strategies for macOS, Linux, and Windows enterprise environments

---

## CLAUDE.md Optimization Best Practices

Research into optimizing the primary context file for Claude Code, with quantified token savings and Chroma Research evidence on context rot thresholds.

??? note "Methodology"
    Combined Claude Code documentation analysis with Chroma Research context rot findings to establish practical optimization guidelines. Quantified token consumption before and after optimization strategies.

??? abstract "Key Data"
    - L0/L1/L2 structured findings
    - **Token quantification**: before/after measurements for each optimization
    - **Size limits**: recommended targets based on context rot evidence
    - **50-70% savings**: demonstrated through rule consolidation, import-based loading, and L2-REINJECT patterns
    - Chroma Research cited: performance unreliable as input length grows across all 18 models tested

[:octicons-link-external-16: CLAUDE.md Optimization (540 lines)](https://github.com/geekatron/jerry/blob/main/projects/PROJ-001-oss-release/work/EPIC-001-oss-release/FEAT-002-research-and-preparation/orchestration/oss-release-20260131-001/ps/phase-0/ps-researcher-claude-md/claude-md-best-practices.md)

---

## Decomposition with Imports: Best Practices

Research on decomposing monolithic context files into modular, selectively-loaded components — the pattern Jerry uses to combat context rot.

??? note "Methodology"
    Analyzed monolithic vs. modular context loading patterns. Drew on Anthropic AWS re:Invent 2025 insights on context-as-bottleneck. Tested index/manifest loading strategies against Jerry's rule files.

??? abstract "Key Data"
    - Anthropic AWS re:Invent 2025 quote on context-as-bottleneck
    - Index/manifest patterns for selective loading
    - Tiered loading architecture: auto-load critical rules, demand-load reference material
    - Context rot mitigation through shorter, focused inputs per agent

[:octicons-link-external-16: Decomposition Research (602 lines)](https://github.com/geekatron/jerry/blob/main/projects/PROJ-001-oss-release/work/EPIC-001-oss-release/FEAT-002-research-and-preparation/orchestration/oss-release-20260131-001/ps/phase-0/ps-researcher-decomposition/decomposition-best-practices.md)

---

## Cross-Platform Sync Strategies

Research on syncing `.context/` rules to `.claude/rules/` across different operating systems and enterprise environments.

??? note "Methodology"
    Tested symlink, copy, and junction strategies across macOS, Linux, and Windows. Documented enterprise IT constraints (Group Policy, antivirus interference) through real-world Windows enterprise environment testing. L0/L1/L2 structured output.

??? abstract "Key Data"
    - L0/L1/L2 structure with platform compatibility matrix
    - **Symlink** (macOS/Linux): zero-copy, real-time sync, recommended default
    - **Copy** (Windows fallback): works everywhere, requires manual re-sync
    - **Junction** (Windows): NTFS-only, near-symlink behavior, enterprise IT restrictions
    - Windows enterprise constraints documented (Group Policy, antivirus interference)

[:octicons-link-external-16: Sync Strategies (614 lines)](https://github.com/geekatron/jerry/blob/main/projects/PROJ-001-oss-release/work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-206-context-distribution-strategy/research-sync-strategies.md)

---

## Related Research

- [Single vs. Multi-Agent Analysis](single-vs-multi-agent.md)
- [Claude Code Ecosystem](claude-code-ecosystem.md)
- [Architecture Patterns](architecture-patterns.md)
