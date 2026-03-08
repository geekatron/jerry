# PROJ-035 Research Extraction Summary

> Key findings extracted from the four Phase 1 research surveys.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Sources](#sources) | Research artifact index |
| [Key Extractions](#key-extractions) | Cross-cutting findings |

---

## Sources

| Phase | Artifact | Key Finding |
|-------|----------|-------------|
| 1A | `historical-testing-methodologies.md` | Metamorphic testing and property-based testing are the most applicable historical approaches for LLM output evaluation |
| 1B | `industry-frameworks-survey.md` | promptfoo (CI/CD gate), DeepEval (G-Eval), and custom statistical engines cover complementary evaluation layers |
| 1C | `agent-sdk-evaluation.md` | Anthropic Agent SDK provides tool-use patterns but no built-in evaluation; evaluation must be custom-built |
| 1D | `innovation-frameworks.md` | Debiasing strategies (position randomization, rubric shuffling) are critical for reliable LLM-as-Judge scoring |

## Key Extractions

1. **Four-layer architecture emerged** from combining the strongest approach from each survey
2. **Statistical rigor requires N >= 20** samples with Wilcoxon signed-rank for paired comparison
3. **Wilson score confidence intervals** provide bounded pass-rate estimates for quality floors
4. **Bonferroni correction** is necessary for multi-metric comparison to control family-wise error
5. **Metamorphic relations** provide oracle-safe behavioral consistency assertions

These extractions directly informed ADR-001 and the PROJ-036 implementation.
