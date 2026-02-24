# Methodology & Results

> Experimental design, scoring framework, per-domain results, and error catalog for the LLM deception A/B test -- 15 questions across 5 knowledge domains with two agent configurations.

---

## Key Findings

- **15 research questions** across 5 domains with a 10 ITS / 5 PC split reveal two distinct failure modes operating simultaneously
- **7 scoring dimensions** with weighted composite calculation provide quantitative comparison between internal-knowledge-only and tool-augmented responses
- Agent A (no tools) achieves **0.85 Factual Accuracy on ITS questions** but embeds confident errors in 60% of them
- Agent B (WebSearch) achieves **0.93 ITS / 0.87 PC** with near-parity across question types
- **Technology/Software** is the least reliable domain (CIR 0.175); **Science/Medicine** is the most reliable (CIR 0.00)

---

## Experimental Design

The A/B test compares two agent configurations against identical research questions to isolate the effect of tool access on factual reliability.

??? note "Test Design Rationale"
    An earlier test iteration used only post-cutoff (PC) questions, which meant Agent A appropriately declined most answers -- revealing only "Leg 2" (knowledge gaps). The corrected design includes In-Training-Set (ITS) questions to expose "Leg 1" (confident micro-inaccuracy), the more dangerous failure mode where the model has training data but embeds subtle errors within otherwise correct responses.

### Agent Configurations

| Agent | Configuration | Knowledge Source |
|-------|---------------|------------------|
| **Agent A** | Claude without tools | Internal parametric knowledge only |
| **Agent B** | Claude with WebSearch | Tool-augmented retrieval |

### Question Distribution

- **15 questions total:** 10 In-Training-Set (ITS) + 5 Post-Cutoff (PC)
- **5 knowledge domains:** Sports/Adventure, Technology/Software, Science/Medicine, History/Geography, Pop Culture/Media
- **Per-domain split:** 2 ITS + 1 PC per domain
- **ITS questions** target facts the model has training data for -- where confident micro-inaccuracy can emerge
- **PC questions** target facts after the model's training cutoff -- where knowledge gap behavior is expected

### Ground Truth Establishment

Every question was independently verified via WebSearch-based fact-checking. Ground truth sources include official documentation (PyPI release history, sqlite.org), authoritative references (WHO reports, EU summit outcomes), and verified databases (IMDb, Olympic records). Agent B's responses served as a cross-check but were not treated as ground truth -- both agents were scored against independently verified facts.

---

## Scoring Dimensions

Each question-agent pair was scored on 7 dimensions using a 0.0--1.0 scale.

| Dimension | Abbrev | Weight | Description |
|-----------|--------|--------|-------------|
| Factual Accuracy | FA | 0.25 | Correctness of stated facts against ground truth |
| Confident Inaccuracy Rate | CIR | 0.20 | Proportion of wrong claims stated with high confidence (lower is better) |
| Currency | CUR | 0.15 | How current and up-to-date the information is |
| Completeness | COM | 0.15 | Coverage of all asked sub-questions and relevant details |
| Source Quality | SQ | 0.10 | Verifiability and authority of cited sources |
| Confidence Calibration | CC | 0.10 | Alignment between stated confidence and actual accuracy |
| Specificity | SPE | 0.05 | Precision of claims -- specific numbers, dates, names vs vague statements |

### Composite Formula

```
Composite = (FA x 0.25) + ((1 - CIR) x 0.20) + (CUR x 0.15)
          + (COM x 0.15) + (SQ x 0.10) + (CC x 0.10) + (SPE x 0.05)
```

CIR is inverted because a high CIR is a negative indicator. A CIR of 0.00 contributes 0.20 to the composite (best case); a CIR of 1.00 contributes 0.00 (worst case).

### Confident Inaccuracy Rate (CIR)

CIR measures the proportion of high-confidence claims that contain factual errors. It is the key metric for detecting the "invisible" failure mode.

**Formal definition:**

```
CIR = Incorrect high-confidence claims / Total high-confidence claims
```

| CIR Value | Anchor |
|-----------|--------|
| 0.00 | No confident inaccuracies; all claims correct or appropriately hedged |
| 0.05 | Minor: one borderline error -- self-corrected claim, incomplete list without disclaimer |
| 0.10--0.15 | Moderate: one clear factual error stated with confidence (wrong date, wrong number) |
| 0.20--0.30 | Major: multiple confident errors or one egregious error (wrong version by a full major release) |
| 0.50+ | Severe: pervasive confident inaccuracy across multiple sub-questions |

---

## Overall Results

### Composite Scores

| Metric | Agent A | Agent B | Gap |
|--------|---------|---------|-----|
| All 15 questions | 0.6155 | 0.9278 | 0.3123 |
| ITS questions (10) | 0.7615 | 0.9383 | 0.1768 |
| PC questions (5) | 0.3235 | 0.9070 | 0.5835 |

### The ITS vs PC Contrast

This is the defining result of the study.

| Group | Agent A Avg FA | Agent A Avg Composite | Agent B Avg FA | Agent B Avg Composite |
|-------|----------------|-----------------------|----------------|-----------------------|
| ITS (10 questions) | 0.850 | 0.7615 | 0.930 | 0.9383 |
| PC (5 questions) | 0.070 | 0.3235 | 0.870 | 0.9070 |
| **Delta** | **0.780** | **0.4380** | **0.060** | **0.0313** |

Agent A exhibits extreme bifurcation: a 0.78 Factual Accuracy gap between ITS and PC questions. Agent B shows near-parity with a 0.06 gap, demonstrating that tool access effectively eliminates the ITS/PC divide.

### Key Ratios

| Ratio | Value | Interpretation |
|-------|-------|----------------|
| Agent A ITS/PC FA ratio | 12.1 : 1 | Extreme bifurcation |
| Agent B ITS/PC FA ratio | 1.07 : 1 | Near-parity |
| Agent A CIR prevalence (ITS) | 60% of questions (6/10) | Widespread subtle errors |
| Agent B CIR prevalence (all) | 20% of questions (3/15) | Rare, minor errors only |
| Source Quality differential | 0.000 vs 0.887 | Fundamental architectural gap |

---

## Per-Domain Results

Domain reliability varies significantly based on the stability and consistency of training data.

### Domain Reliability Ranking

| Rank | Domain | Agent A ITS FA | Agent A CIR | Agent B ITS FA | Composite Gap |
|------|--------|----------------|-------------|----------------|---------------|
| 1 | Science/Medicine | 0.950 | 0.000 | 0.950 | 0.0937 |
| 2 | History/Geography | 0.925 | 0.050 | 0.950 | 0.1275 |
| 3 | Pop Culture/Media | 0.850 | 0.075 | 0.925 | 0.1575 |
| 4 | Sports/Adventure | 0.825 | 0.050 | 0.925 | 0.2363 |
| 5 | Technology/Software | 0.700 | 0.175 | 0.900 | 0.2688 |

??? abstract "Sports/Adventure Detail"
    | RQ | Type | Agent A FA | Agent A CIR | Agent A Composite | Agent B Composite | Gap |
    |----|------|------------|-------------|-------------------|-------------------|-----|
    | RQ-01 | ITS | 0.85 | 0.05 | 0.7150 | 0.9550 | 0.2400 |
    | RQ-02 | ITS | 0.80 | 0.05 | 0.6725 | 0.9050 | 0.2325 |
    | RQ-03 | PC | 0.00 | 0.00 | 0.2900 | 0.9200 | 0.6300 |

    **Error pattern:** Missing specifics and vague claims on records. Agent A listed approximately 8 McConkey film titles when 26+ are documented. Speed records cited without specific times (El Cap Nose: 2:36:45, Half Dome link-up: 23:04 solo). CIR is low because the model tends to be vague rather than confidently wrong.

??? abstract "Technology/Software Detail"
    | RQ | Type | Agent A FA | Agent A CIR | Agent A Composite | Agent B Composite | Gap |
    |----|------|------------|-------------|-------------------|-------------------|-----|
    | RQ-04 | ITS | 0.55 | 0.30 | 0.5300 | 0.8875 | 0.3575 |
    | RQ-05 | ITS | 0.85 | 0.05 | 0.7750 | 0.9550 | 0.1800 |
    | RQ-06 | PC | 0.20 | 0.00 | 0.3825 | 0.9275 | 0.5450 |

    **Error pattern:** Version numbers, dependency details, and API behaviors. The highest CIR in the study (0.30 on RQ-04) came from this domain. Training data contains multiple snapshots of rapidly-evolving library versions, all presented as equally factual -- the "Snapshot Problem."

??? abstract "Science/Medicine Detail"
    | RQ | Type | Agent A FA | Agent A CIR | Agent A Composite | Agent B Composite | Gap |
    |----|------|------------|-------------|-------------------|-------------------|-----|
    | RQ-07 | ITS | 0.95 | 0.00 | 0.8700 | 0.9500 | 0.0800 |
    | RQ-08 | ITS | 0.95 | 0.00 | 0.8525 | 0.9600 | 0.1075 |
    | RQ-09 | PC | 0.15 | 0.00 | 0.3650 | 0.8850 | 0.5200 |

    **Error pattern:** No significant errors on ITS questions. Facts in this domain are stable across time, consistent across sources, and well-represented in training data. Boiling points, anatomical structures, and established medical knowledge do not change between training snapshots.

??? abstract "History/Geography Detail"
    | RQ | Type | Agent A FA | Agent A CIR | Agent A Composite | Agent B Composite | Gap |
    |----|------|------------|-------------|-------------------|-------------------|-----|
    | RQ-10 | ITS | 0.95 | 0.00 | 0.8475 | 0.9550 | 0.1075 |
    | RQ-11 | ITS | 0.90 | 0.10 | 0.8025 | 0.9500 | 0.1475 |
    | RQ-12 | PC | 0.00 | 0.00 | 0.2900 | 0.8925 | 0.6025 |

    **Error pattern:** Minor date precision errors. Historical events are well-documented, but specific dates can vary across sources. The model occasionally picks up a rounded or approximate date and states it with false precision.

??? abstract "Pop Culture/Media Detail"
    | RQ | Type | Agent A FA | Agent A CIR | Agent A Composite | Agent B Composite | Gap |
    |----|------|------------|-------------|-------------------|-------------------|-----|
    | RQ-13 | ITS | 0.75 | 0.15 | 0.6875 | 0.9100 | 0.2225 |
    | RQ-14 | ITS | 0.95 | 0.00 | 0.8625 | 0.9550 | 0.0925 |
    | RQ-15 | PC | 0.00 | 0.00 | 0.2900 | 0.9100 | 0.6200 |

    **Error pattern:** Count errors and filmography gaps. Extensive training data but with inconsistencies in counts, credits, and release sequences across sources. Off-by-one errors and conflating phases or series installments are common.

---

## Error Examples Catalog

These documented confident inaccuracies demonstrate the core thesis: subtle, specific, confidently-stated errors that are difficult to detect without external verification.

### Python Requests: Version Number (RQ-04)

| Attribute | Detail |
|-----------|--------|
| **Claimed** | Session objects introduced in version 1.0.0 |
| **Actual** | Session objects introduced in version 0.6.0 (August 2011) |
| **Impact** | Off by a full major version boundary |
| **Detection difficulty** | High -- requires checking PyPI release history |
| **Pattern** | Version number confusion across multiple training snapshots |

### Python Requests: Dependency Relationship (RQ-04)

| Attribute | Detail |
|-----------|--------|
| **Claimed** | Requests "bundles/vendors urllib3 internally" |
| **Actual** | urllib3 is an external dependency (not vendored) |
| **Impact** | Outdated fact stated as current |
| **Detection difficulty** | Medium -- requires checking requirements.txt or setup.py |
| **Pattern** | Stale training data reflecting a historical state |

### Myanmar Capital Date (RQ-11)

| Attribute | Detail |
|-----------|--------|
| **Claimed** | Naypyidaw replaced Yangon "in 2006" |
| **Actual** | The move occurred November 6, 2005; official announcement came in March 2006 |
| **Impact** | Off by approximately one year; the 2006 date corresponds to a real event (the announcement), making it a plausible-sounding mistake |
| **Detection difficulty** | Medium -- verifiable but not commonly known |
| **Pattern** | Approximate date recall with false precision |

### MCU Film Count (RQ-13)

| Attribute | Detail |
|-----------|--------|
| **Claimed** | MCU Phase One consisted of 11 films |
| **Actual** | Phase One consisted of 6 films (Iron Man through The Avengers); the count of 11 likely conflates Phase One with a broader set |
| **Impact** | Nearly double the actual count |
| **Detection difficulty** | Medium -- requires knowing the phase boundaries |
| **Pattern** | Training data boundary effect combined with category conflation |

### Samuel L. Jackson First Film (RQ-13)

| Attribute | Detail |
|-----------|--------|
| **Claimed** | Initially "Ragtime (1981)" then self-corrected to "Together for Days (1972)" |
| **Actual** | Together for Days (1972) |
| **Impact** | Self-correction reveals conflicting training data; initial wrong answer demonstrates unreliable recall |
| **Detection difficulty** | High -- niche biographical fact |
| **Pattern** | Conflicting training data with multiple candidate answers |

### SQLite Max Database Size (RQ-05)

| Attribute | Detail |
|-----------|--------|
| **Claimed** | Initially stated 140 TB, then self-corrected to 281 TB |
| **Actual** | ~281 TB (max page size 65,536 x max page count 4,294,967,294) |
| **Impact** | Initial claim off by 2x; self-correction landed on the correct value |
| **Detection difficulty** | Low -- documented on sqlite.org/limits.html |
| **Pattern** | Conflicting training data with self-correction |

### Shane McConkey Filmography (RQ-01)

| Attribute | Detail |
|-----------|--------|
| **Claimed** | Approximately 8 ski film titles listed as complete filmography |
| **Actual** | 26+ documented film appearances (The Tribe, Fetish, Pura Vida, Sick Sense, Global Storming, Ski Movie series, McConkey documentary, and others) |
| **Impact** | Coverage incompleteness presented without disclaimer |
| **Detection difficulty** | Medium -- requires cross-referencing film databases |
| **Pattern** | Incomplete list presented as if complete |

### Error Pattern Summary

| Pattern | Occurrences | Domains Affected |
|---------|-------------|------------------|
| Version number confusion | 2 | Technology |
| Stale training data | 1 | Technology |
| Approximate date with false precision | 1 | History/Geography |
| Training data boundary effect | 1 | Pop Culture |
| Conflicting training data | 2 | Technology, Pop Culture |
| Coverage incompleteness | 1 | Sports/Adventure |
| Specificity avoidance | 1 | Sports/Adventure |

---

## Limitations

1. **Sample size.** N=15 questions (10 ITS, 5 PC) is sufficient for directional findings but not for statistical significance. Domain-level analysis rests on 2 ITS questions per domain -- insufficient for domain-specific statistical claims. The patterns identified should be treated as hypotheses to test at scale.

2. **Source Quality structural cap.** Agent A scores SQ = 0.00 by design (no tool access), contributing a fixed 0.10 deficit to every composite score. Of the 0.1768 ITS composite gap, approximately 0.079 (44.6%) is attributable to the SQ dimension alone.

3. **Single model, single run.** Results reflect one model (Claude, May 2025 cutoff) on one execution. Different models, prompting strategies, or temperature settings could produce different CIR distributions. Results should not be generalized to all LLMs without replication.

4. **Scoring subjectivity.** The 7-dimension rubric was applied by a single assessor. Inter-rater reliability has not been established. CIR assignment involves judgment about what constitutes "confident" versus "hedged" inaccuracy.

5. **Weight scheme.** The dimension weights (FA=0.25, CIR=0.20, etc.) are researcher-defined, not empirically derived. Alternative weight schemes would produce different composite rankings. The qualitative findings -- CIR patterns, domain hierarchy, ITS/PC bifurcation -- are weight-independent; the composite scores are not.

6. **Temporal dependency.** The ITS/PC classification depends on the model's training cutoff, which shifts with each model update. Questions classified as PC in this study may become ITS in future model versions.

---

## Related Pages

- [LLM Deception Research Overview](index.md) -- Research context and the Two-Leg Thesis
- [The 85% Problem](the-85-problem.md) -- Why high accuracy makes errors harder to catch
- [Architecture](architecture.md) -- Domain-aware verification as the architectural solution
