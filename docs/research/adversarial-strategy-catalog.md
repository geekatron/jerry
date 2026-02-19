# Adversarial Strategy Catalog

> Unified catalog of 15 adversarial review strategies synthesized from academic literature, industry practices, and emerging AI patterns — with 117+ citations across three independent research streams.

---

## Key Findings

- **36 candidate strategies** from three research streams (academic, industry, emerging) were deduplicated and synthesized into **15 distinct strategies**
- Strategies cluster into **4 mechanistic families**: Role-Based Adversarialism, Structured Decomposition, Dialectical Synthesis, and Iterative Self-Correction
- **Academic strategies** (CIA, DoD, Hegelian dialectics) provide the strongest evidence base with 70+ years of formalized practice
- **LLM-specific strategies** (Constitutional AI, Self-Refine, LLM-as-Judge) are natively compatible with single-model architectures
- The catalog enables **criticality-based activation** — from lightweight self-review (C1) to full 10-strategy tournaments (C4)

---

## Unified Catalog of 15 Adversarial Review Strategies

The crown jewel of the adversarial research pipeline: 36 candidates from three parallel research efforts were deduplicated, analyzed for overlap, and synthesized into 15 distinct strategies with full profiles.

??? note "Methodology"
    The synthesis followed a rigorous pipeline:

    1. **TASK-001** (Academic): 12 strategies from peer-reviewed sources — CIA structured analytic techniques, DoD red teaming, Hegelian dialectics, decision science (36 citations)
    2. **TASK-002** (Industry): 14 strategies from industry practices and LLM-specific patterns (35 citations)
    3. **TASK-003** (Emerging): 10 strategies from cross-domain emerging approaches (46 references)
    4. **TASK-004** (Synthesis): Overlap analysis → deduplication → 15 unified strategies with standardized profiles

    Each strategy profile includes: origin, mechanism, strengths, weaknesses, Jerry-specific applicability, P-003 compliance assessment, and token budget estimate.

??? abstract "Key Data: The 15 Strategies"
    | ID | Strategy | Family | One-Line Description |
    |----|----------|--------|----------------------|
    | S-001 | Red Team Analysis | Role-Based | Independent team adopts adversary perspective to find vulnerabilities |
    | S-002 | Devil's Advocate | Role-Based | Formally assigned critic builds strongest case against prevailing judgment |
    | S-003 | Steelman Technique | Dialectical | Reconstruct argument in strongest form before critiquing |
    | S-004 | Pre-Mortem Analysis | Role-Based | Imagine the plan has failed; work backward to identify causes |
    | S-005 | Dialectical Inquiry | Dialectical | Two opposing plans from same data, debated to synthesis |
    | S-006 | Analysis of Competing Hypotheses | Decomposition | Multiple hypotheses evaluated against all evidence in a matrix |
    | S-007 | Constitutional AI Critique | Self-Correction | Critique outputs against explicit written principles iteratively |
    | S-008 | Socratic Method | Dialectical | Probing questions to expose contradictions and assumptions |
    | S-009 | Multi-Agent Debate | Dialectical | Multiple LLM agents argue across structured rounds |
    | S-010 | Self-Refine | Self-Correction | Iterative generate-feedback-refine loop |
    | S-011 | Chain-of-Verification | Decomposition | Generate verification questions for claims, answer independently |
    | S-012 | FMEA | Decomposition | Systematic failure mode enumeration with severity/occurrence/detection scoring |
    | S-013 | Inversion Technique | Decomposition | Ask "how would we guarantee failure?" to generate anti-pattern checklists |
    | S-014 | LLM-as-Judge | Self-Correction | Rubric-based structured evaluation with numerical scores |
    | S-015 | Prompt Adversarial Examples | Self-Correction | Adversarial prompt testing with graduated intensity |

??? abstract "Key Data: Mechanistic Families"
    | Family | Mechanism | Strategies | Best For |
    |--------|-----------|------------|----------|
    | **Role-Based Adversarialism** | Designated agent adopts oppositional persona | S-001, S-002, S-004 | Breaking groupthink, challenging assumptions |
    | **Structured Decomposition** | Systematic framework forces exhaustive enumeration | S-006, S-011, S-012, S-013 | Completeness, failure mode coverage |
    | **Dialectical Synthesis** | Opposing positions constructed and reconciled | S-003, S-005, S-008, S-009 | Novel insights, balanced analysis |
    | **Iterative Self-Correction** | Agent critiques and revises own output | S-007, S-010, S-014, S-015 | Quality scoring, constitutional compliance |

[:octicons-link-external-16: Unified Catalog (1,171 lines)](https://github.com/geekatron/jerry/blob/main/projects/PROJ-001-oss-release/work/EPIC-002-quality-enforcement/FEAT-004-adversarial-strategy-research/EN-301-deep-research-adversarial-strategies/deliverable-004-unified-catalog.md)

---

## Academic Literature on Adversarial Review Strategies

The foundational research artifact documenting 12 strategies from peer-reviewed academic sources with formal citations and methodology descriptions.

??? note "Methodology"
    Research drew from five major academic domains:

    - **Intelligence analysis**: CIA/DoD structured analytic techniques (Heuer & Pherson, 2014)
    - **Argumentation theory**: Dialectical methods, formal argumentation (Toulmin, 1958)
    - **Decision science**: Pre-mortem analysis, prospective hindsight (Klein, 1998)
    - **Cybersecurity**: Threat modeling, STRIDE (Shostack, 2014; MIL-STD-1629A)
    - **AI safety**: Constitutional AI, debate-based alignment (Bai et al., 2022; Irving et al., 2018)

    Selection criteria required: formal publication, explicit adversarial mechanism, reproducible methodology, mechanistic distinctness, and LLM workflow applicability.

??? abstract "Key Data: Source Tiers"
    | Tier | Source Type | Count |
    |------|-----------|-------|
    | Primary | Peer-reviewed papers, books with ISBN, government publications | 18 |
    | Secondary | Major institution research (Anthropic, RAND, MITRE) | 6 |
    | Tertiary | Conference proceedings, well-cited preprints | 3 |

    Key finding: strategies cluster into three fundamental mechanistic families — **role-based adversarialism** (breaking groupthink), **structured decomposition** (ensuring completeness), and **dialectical synthesis** (producing novel insights).

[:octicons-link-external-16: Academic Research (861 lines, 36 citations)](https://github.com/geekatron/jerry/blob/main/projects/PROJ-001-oss-release/work/EPIC-002-quality-enforcement/FEAT-004-adversarial-strategy-research/EN-301-deep-research-adversarial-strategies/deliverable-001-academic-adversarial-research.md)

---

## Industry Practices & LLM-Specific Patterns

Research into 14 adversarial review strategies from software engineering practice (Fagan inspections, Google code review, ATAM), design review methodology, and LLM-specific self-correction patterns (Constitutional AI, Self-Refine, multi-agent debate).

??? note "Methodology"
    Surveyed industry software engineering practices (Fagan, 1976 through modern Google code review culture), design critique methodologies, LLM/AI adversarial systems (Constitutional AI, Self-Refine, multi-agent debate), and QA adversarial patterns. Identified the creator-critic-revision cycle as a universal convergent pattern across all four domains.

??? abstract "Key Data"
    | Domain | Strategies | Key Insight |
    |--------|-----------|-------------|
    | Software Engineering | Fagan Inspection, Google Code Review, ATAM, Pair Programming | Deep adversarial traditions with measured defect-detection effectiveness |
    | LLM-Specific | Constitutional AI, Self-Refine, Multi-Agent Debate | Directly implementable patterns for creator-critic-revision cycles |
    | Design/Product | Design critique, stakeholder challenge | Present-critique-iterate mirrors the universal pattern |
    | QA | Adversarial testing, boundary analysis | Testing-oriented adversarial methods |

    **35 citations** across software engineering, AI/ML, and design methodology literature.

[:octicons-link-external-16: Industry Research (1,097 lines, 35 citations)](https://github.com/geekatron/jerry/blob/main/projects/PROJ-001-oss-release/work/EPIC-002-quality-enforcement/FEAT-004-adversarial-strategy-research/EN-301-deep-research-adversarial-strategies/deliverable-002-industry-adversarial-research.md)

---

## Emerging & Cross-Domain Adversarial Approaches

10 emerging adversarial review strategies discovered through cross-domain transfer analysis (legal, medical, military), cognitive science debiasing techniques, and frontier AI adversarial collaboration patterns.

??? note "Methodology"
    Applied cross-domain transfer analysis across legal (moot court), medical (M&M conferences), and military (wargaming) traditions. Identified cognitive debiasing techniques (Reference Class Forecasting, Inversion Technique) and AI-native patterns (Constitutional AI critique chains, progressive adversarial escalation) as underexplored adversarial review strategies. Explicit differentiation against TASK-001 and TASK-002 findings.

??? abstract "Key Data"
    | Category | Example Strategies | Novelty |
    |----------|--------------------|---------|
    | Cross-Domain Transfer | Moot Court, M&M Conference, Wargaming | Centuries of refined adversarial practice, never formally applied to software review |
    | Cognitive Debiasing | Reference Class Forecasting, Inversion Technique | Powerful adversarial tools rarely framed as review strategies |
    | AI-Native | Constitutional AI Critique Chains, Progressive Adversarial Escalation | No direct pre-AI precedent; most applicable to Jerry's architecture |
    | Meta-Strategy | Cynefin-Gated Selection | Matches adversarial intensity to problem complexity |

    **46 references** spanning legal theory, medical practice, military doctrine, and AI safety research.

[:octicons-link-external-16: Emerging Research (706 lines, 46 references)](https://github.com/geekatron/jerry/blob/main/projects/PROJ-001-oss-release/work/EPIC-002-quality-enforcement/FEAT-004-adversarial-strategy-research/EN-301-deep-research-adversarial-strategies/deliverable-003-emerging-adversarial-research.md)

---

## Related Research

- [Strategy Selection & Enforcement (ADRs)](strategy-selection-enforcement.md)
- [Adversarial Quality Deep Dives](adversarial-deep-dives.md)
- [Single vs. Multi-Agent Analysis](single-vs-multi-agent.md)
