# Diataxis Classification Validation: STORY-019 Documentation Deliverables

> Classification analysis of proposed Tier Model documentation against the Diataxis two-axis framework.

## Classification Results

| Deliverable | Proposed Quadrant | Correct Quadrant | Confidence | Status |
|-------------|------------------|-----------------|------------|--------|
| Tier Migration Guide | How-To | **How-To** | 1.00 | CORRECT |
| Tier Selection Reference | Reference | **Explanation** | 1.00 | INCORRECT |
| Options Explainer (existing) | -- | Explanation | 1.00 | CORRECT |

## Answers

1. **Migration Guide correctly a how-to?** Yes. Reader is applying existing knowledge (application mode), not learning tiers from scratch (tutorial/acquisition mode).

2. **Tier Selection Reference correctly a reference?** No. Two-axis test: Theoretical + Acquisition = Explanation, not Reference. Reader is *learning* which tier fits (acquisition), not looking up facts in a known system (application). Rename to "Tier Selection Guide" or replace with Quick-Reference Card.

3. **Explanation document needed?** Already exists — the Options Explainer covers it.

4. **Reclassify options explainer?** No — already correctly Explanation.

5. **Quadrant mixing risks?** HIGH risk in proposed "Reference" that contains Explanation content. Readers expecting a facts table would receive teaching material.

## Recommendation

Replace "Tier Selection Reference" with a genuine Reference artifact (Quick-Reference Card: 1-page facts-only table). The Options Explainer already covers the Explanation need. Final set: Explanation (existing) + How-To (migration guide) + Reference (quick-card).

---

*Classifier: diataxis-classifier*
*Date: 2026-03-28*
*Methodology: Two-axis test (Practical/Theoretical x Acquisition/Application)*
