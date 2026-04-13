<!-- TEMPLATE: kano-survey-template.md | VERSION: 1.2.0 | DATE: 2026-03-04 -->
<!-- SKILL: /ux-kano-model | AGENT: ux-kano-analyst -->
<!-- SOURCE: SKILL.md [Execution Procedure § Phase 2], skills/ux-kano-model/agents/ux-kano-analyst.md <methodology> Phase 2, kano-methodology-rules.md -->
<!-- USAGE: Fill {{PLACEHOLDER}} fields. Copy REPEATABLE BLOCK markers for each feature being evaluated. Administer the completed survey to respondents. Return response data to ux-kano-analyst for classification. -->

# Kano Survey Questionnaire: {{TOPIC}}

> **Engagement:** {{ENGAGEMENT_ID}}
> **Product:** {{PRODUCT_NAME}}
> **Date:** {{SURVEY_DATE}}
> **Designed by:** ux-kano-analyst
> **Target Respondent Count:** {{TARGET_RESPONDENT_COUNT}}

## Document Sections

| Section | Purpose |
|---------|---------|
| [Survey Metadata](#survey-metadata) | Engagement context, product, respondent targeting |
| [Response Scale Reference](#response-scale-reference) | Standardized 5-point Kano response scale |
| [Feature Questions](#feature-questions) | Functional/dysfunctional question pairs per feature |
| [Response Collection Table](#response-collection-table) | Tabular format for recording respondent answers |
| [Administration Guidance](#administration-guidance) | Sample size, respondent selection, administration tips |

---

## Survey Metadata

| Field | Value |
|-------|-------|
| Engagement ID | {{ENGAGEMENT_ID}} |
| Product | {{PRODUCT_NAME}} |
| Product Domain | {{PRODUCT_DOMAIN}} |
| Target Users | {{TARGET_USER_DESCRIPTION}} |
| Survey Design Date | {{SURVEY_DATE}} |
| Feature Count | {{FEATURE_COUNT}} |
| Target Respondent Count | {{TARGET_RESPONDENT_COUNT}} |
| Minimum Respondents (Statistical) | 20 (Berger et al., 1993) |
| Minimum Respondents (Directional) | 5-8 (directional signal only) |

---

## Response Scale Reference
<!-- Rule: EVT-001, EVT-005 (kano-methodology-rules.md) -->

Each question uses the following standardized 5-point response scale. Present this scale to respondents before they begin.

| Response | Code | Meaning |
|----------|------|---------|
| **I like it** | 1 | Positive reaction to the described feature state |
| **I expect it** | 2 | Considers this a basic expectation |
| **I am neutral** | 3 | No strong feeling either way |
| **I can tolerate it** | 4 | Mild negative reaction, but acceptable |
| **I dislike it** | 5 | Strong negative reaction |

---

## Feature Questions
<!-- Rules: SQD-001 (pair completeness), SQD-002 (concrete language), SQD-003 (balanced tone), SQD-004 (response scale) per kano-methodology-rules.md -->

For each feature, respondents answer two questions: a **functional** question (how they feel if the feature IS present) and a **dysfunctional** question (how they feel if the feature is NOT present). The combination of these two answers determines the Kano classification.

<!-- REPEATABLE BLOCK: FEATURE QUESTION START -->
<!-- NOTE: {{FEATURE_NAME}} = canonical name for headings; {{FEATURE_NAME_LOWERCASE}} = same feature in lowercase for natural-language question flow. -->
### Feature {{N}}: {{FEATURE_NAME}}

**Feature description:** {{FEATURE_DESCRIPTION}}

**Functional question:**
> How would you feel if {{PRODUCT_NAME}} had {{FEATURE_NAME_LOWERCASE}}?

| | I like it | I expect it | I am neutral | I can tolerate it | I dislike it |
|---|---|---|---|---|---|
| Response | [ ] | [ ] | [ ] | [ ] | [ ] |

**Dysfunctional question:**
> How would you feel if {{PRODUCT_NAME}} did NOT have {{FEATURE_NAME_LOWERCASE}}?

| | I like it | I expect it | I am neutral | I can tolerate it | I dislike it |
|---|---|---|---|---|---|
| Response | [ ] | [ ] | [ ] | [ ] | [ ] |

<!-- REPEATABLE BLOCK: FEATURE QUESTION END -->

---

## Response Collection Table

Record each respondent's answers in the table below. Use the response codes (1-5) from the Response Scale Reference. One row per respondent per feature (total rows = respondent count x feature count).

| Respondent ID | Feature | Functional (1-5) | Dysfunctional (1-5) | Segment (optional) | Tenure (optional) | Usage Freq (optional) |
|---------------|---------|-------------------|----------------------|--------------------|--------------------|-----------------------|
| RESP-001 | Dashboard Export | 2 | 5 | Power User | 2 years | Daily |
| RESP-001 | Batch Upload | 1 | 4 | Power User | 2 years | Daily |
| {{RESP_ID}} | {{FEATURE_NAME}} | {{1-5}} | {{1-5}} | {{SEGMENT}} | {{TENURE}} | {{FREQUENCY}} |
<!-- REPEATABLE ROW: Copy row for each respondent-feature pair. The example rows above show how a single respondent (RESP-001) has one row per feature. Optional metadata columns support segment analysis with 50+ respondents (Tip 8). -->

### Response Code Reference

| Code | Response |
|------|----------|
| 1 | I like it |
| 2 | I expect it |
| 3 | I am neutral |
| 4 | I can tolerate it |
| 5 | I dislike it |

---

## Administration Guidance

### Sample Size
<!-- Rule: SSC-001 through SSC-004 (kano-methodology-rules.md) -->

| Tier | Respondent Count | Classification Quality | Recommendation |
|------|-----------------|----------------------|----------------|
| **Statistical** | 20+ respondents | Statistically reliable (Berger et al., 1993) | Preferred for production prioritization decisions |
| **Directional** | 5-8 respondents | Directional signal; majority may shift | Acceptable for early-stage exploration; plan to expand |
| **Segment analysis** | 50+ respondents | Enables per-segment breakdowns | Required if comparing user segments (practitioner recommendation) |

### Respondent Selection

- Select respondents from the **target user population** for the product or feature set
- Include a mix of experience levels (new users, regular users, power users) where possible
- Avoid selecting only internal team members or stakeholders -- they carry implementation bias
- If the product has distinct user segments, aim for proportional representation across segments

### Administration Tips

1. **Randomize feature order** across respondents to prevent order bias. Each respondent should see features in a different sequence.
2. **Avoid priming language** in introductions. Do not describe features as "exciting" or "basic" before respondents answer.
3. **Test question clarity** with 2-3 pilot respondents before full administration. High Questionable (Q) response rates indicate question wording issues.
4. **Present both questions together** for each feature (functional then dysfunctional) before moving to the next feature.
5. **Allow "I am neutral" responses** -- do not force respondents away from the neutral option. Neutral responses are valid data points (Indifferent classification).
6. **Use user-understandable language** in feature descriptions. Avoid developer jargon, internal code names, or technical architecture terms.
7. **Keep the survey focused** -- 5-15 features per survey is recommended (practitioner recommendation; not derived from Berger et al.). More than 20 features risks respondent fatigue and lower-quality responses.
8. **Record respondent metadata** (user segment, tenure, usage frequency) alongside responses for potential segment analysis with 50+ respondents.

### Post-Administration and Re-Invocation

After collecting responses:
1. Compile the Response Collection Table with all respondent data (one row per respondent per feature)
2. Re-invoke the `ux-kano-analyst` agent with the completed response data. Provide the following context fields:
   - **Engagement ID:** `{{ENGAGEMENT_ID}}` (must match this survey)
   - **Survey Data:** path to this completed file (e.g., `projects/${JERRY_PROJECT}/engagements/UX-0001/kano-survey-dashboard.md`)
   - **Respondent Count:** total number of respondents
3. The agent will apply the 5x5 evaluation table, compute CS coefficients, and produce the priority matrix

### Post-Administration Handoff

When re-invoking the `ux-kano-analyst` agent with completed data, provide the following fields in the UX CONTEXT block:

| Field | Value |
|-------|-------|
| `engagement_id` | `{{ENGAGEMENT_ID}}` |
| `survey_data_path` | Path to this completed file |
| `respondent_count` | Total number of respondents (integer) |
| `feature_count` | `{{FEATURE_COUNT}}` |
| `product` | `{{PRODUCT_NAME}}` |
| `target_users` | `{{TARGET_USER_DESCRIPTION}}` |

> Schema: `docs/schemas/handoff-v2.schema.json` + `ux_ext` fields per agent `<output>` On-Send Protocol.

---

*Template Version: 1.2.0 | /ux-kano-model Sub-Skill | PROJ-022 User Experience Skill*
*Source: SKILL.md [Execution Procedure § Phase 2], `skills/ux-kano-model/agents/ux-kano-analyst.md` [methodology] Phase 2*
*Methodology: Kano, N., Seraku, N., Takahashi, F., & Tsuji, S. (1984). "Attractive quality and must-be quality." Journal of the Japanese Society for Quality Control, 14(2), 39-48. Berger, C., Blauth, R., Boger, D., et al. (1993). "Kano's methods for understanding customer-defined quality." Center for Quality Management Journal, 2(4), 3-36. Matzler, K. & Hinterhuber, H.H. (1998). "How to make product development projects more successful by integrating Kano's model of customer satisfaction into quality function deployment." Technovation, 18(1), 25-38.*
*Rules: `skills/ux-kano-model/rules/kano-methodology-rules.md` (SQD, EVT, SSC rule families)*
