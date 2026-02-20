# Single vs. Multi-Agent Orchestration

> Evidence-based analysis of when multi-agent orchestration outperforms single-agent approaches, drawing on 20 peer-reviewed sources from ACL, ICLR, ICML, EMNLP, and NeurIPS.

---

## Key Findings

- **Context length alone degrades LLM performance by 14-85%**, even with perfect retrieval — the architecturally decisive finding (Du & Tian, EMNLP 2025)
- **Multi-agent advantage narrows with stronger models**: gains dropped from ~10% to ~1-3% across one generation of model improvement (Xie et al., 2025 meta-study)
- **Self-refinement fails for logical reasoning** (+0.2% on math) but succeeds for stylistic tasks (+20-30%) — a separate critic overcomes this blind spot (Madaan et al., NeurIPS 2023)
- **Pipeline architectures (MetaGPT, ChatDev) show 2.8-3.9x quality improvement** over single-agent in software development tasks (ICLR/ACL 2024)
- **The real differentiator is verifiable process**: adversarial review, persistent artifacts, and structured quality scoring — not raw answer quality

---

## Single Agent vs. Multi-Agent Orchestration: Evidence-Based Analysis

This 320-line research artifact synthesizes findings from three independent research clusters: context window degradation mechanics, head-to-head single vs. multi-agent benchmarks, and quality assurance mechanism evaluation. The analysis provides a nuanced three-layer conclusion rather than a binary recommendation.

??? note "Methodology"
    The analysis draws on **20 sources** spanning three independent research clusters:

    - **Context window degradation** (7 sources): ACL, ICLR, EMNLP, Chroma Research, arXiv
    - **Single vs. multi-agent benchmarks** (6 studies): ICML, ICLR, ACL, PMC
    - **Quality assurance mechanisms** (6 studies): NeurIPS, Anthropic, domain-specific venues

    Of these, **15 are peer-reviewed** (ACL, ICLR, ICML, EMNLP, NeurIPS, PMC), 4 are arXiv preprints or technical reports, and 1 is a practitioner blog post. The clusters provide independent lines of evidence converging on the same conclusion.

??? abstract "Key Data: Context Rot Evidence"
    | Mechanism | Finding | Source |
    |-----------|---------|--------|
    | Lost in the Middle | U-shaped attention pattern — LLMs miss information in the middle of long contexts | Liu et al., ACL 2024 |
    | Context Rot | Performance unreliable as input length grows across all 18 models tested | Chroma Research, 2025 |
    | Length Alone Hurts | 13.9-85% degradation even when models forced to attend only to relevant tokens | Du & Tian, EMNLP 2025 |
    | Multi-Turn Drift | 39% average accuracy drop from single-turn to multi-turn conversations | Levy et al., 2025 |
    | Effective Window | Open-source LLMs use <50% of their claimed context length effectively | Ding et al., ICLR 2025 |

??? abstract "Key Data: Multi-Agent Performance Benchmarks"
    **Software Development (Pipeline Paradigm — directly applicable to Jerry):**

    | Study | Single Agent | Multi-Agent | Improvement |
    |-------|-------------|-------------|-------------|
    | MetaGPT vs AutoGPT (ICLR 2024) | 1.0 | 3.9 | **3.9x** quality |
    | ChatDev vs GPT-Engineer (ACL 2024) | 0.14 | 0.40 | **2.8x** quality |

    **Reasoning and Factuality (Debate Paradigm):**

    | Study | Single Agent | Multi-Agent | Improvement |
    |-------|-------------|-------------|-------------|
    | Du et al., ICML 2024 (Arithmetic) | 67.0% | 81.8% | **+14.8pp** |
    | Du et al., ICML 2024 (Biography facts) | 60.0% | 74.0% | **+14.0pp** |
    | A-HMAD, 2025 (Biography facts) | 60.0% | 80.6% | **+20.6pp** |

    **Diminishing Returns with Stronger Models:**

    | Benchmark | Early Models | Frontier Models | Trend |
    |-----------|-------------|-----------------|-------|
    | MetaGPT-HumanEval | +10.7% | +3.0% | Narrowing |
    | MathDebate-GSM8K | +9.0% | +0.8% | Narrowing |

[:octicons-link-external-16: Full artifact on GitHub](https://github.com/geekatron/jerry/blob/main/projects/PROJ-001-oss-release/research/single-vs-multi-agent-analysis.md)

---

## Related Research

- [Context Management](context-management.md)
- [Adversarial Strategy Catalog](adversarial-strategy-catalog.md)
- [Strategy Selection & Enforcement (ADRs)](strategy-selection-enforcement.md)
