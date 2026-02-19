# adv-scorer-007: Quality Score Report — FEAT-007 Developer Experience Delight

<!--
AGENT: adv-scorer-007
STRATEGY: S-014 (LLM-as-Judge)
DELIVERABLE: ps-creator-007-draft.md (v0.4.0)
WORKFLOW: jnsq-20260219-001
PHASE: 3 — Tier 2 Fan-Out
FEATURE: FEAT-007 Developer Experience Delight
DATE: 2026-02-19
CRITICALITY: C2 (Standard)
INDEPENDENCE: Scored fresh. No prior exposure to this deliverable before this session.
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Scoring Context](#scoring-context) | Deliverable identity, criticality, independence declaration |
| [Dimension Scores](#dimension-scores) | Six dimensions scored individually with justification |
| [Strengths](#strengths) | What the deliverable does well |
| [Weaknesses](#weaknesses) | Where the deliverable falls short |
| [Composite Score and Verdict](#composite-score-and-verdict) | Weighted composite, band classification, disposition |
| [Revision Guidance (REVISE Band)](#revision-guidance-revise-band) | Targeted fixes for weakest dimensions |
| [Metadata](#metadata) | Machine-readable YAML |

---

## Scoring Context

**Deliverable:** `ps-creator-007-draft.md` — Version 0.4.0, STATUS: REVIEWED

**Parent requirement:** FEAT-007 Developer Experience Delight (EPIC-001-je-ne-sais-quoi). Requirement text: "Small touches that make the difference between a tool you use and a tool you love. Session start personality. Progress celebrations. The feeling of working WITH a companion, not UNDER a supervisor."

**Review history:** 3 rounds completed (R1: S-010+S-003+S-002, R2: S-002, R3: S-007). 14 fixes applied across rounds. H-14 minimum iteration count met.

**Criticality:** C2 (Standard). Quality threshold per H-13: >= 0.92 weighted composite.

**Independence declaration:** This score is produced by adv-scorer-007 without prior exposure to the deliverable in this session. Scores are not anchored to the ps-critic-007 assessments. The critic reviews were read for context on what was fixed, not to calibrate scores.

**Leniency bias countermeasure:** Each dimension is scored on evidence in the artifact only. Good intentions, review effort, and process compliance are not scoring criteria. The bar is what the deliverable says, not what it tried to say.

---

## Dimension Scores

### 1. Completeness — Score: 0.91

**Weight:** 0.20

**Question:** Does the deliverable fully address all FEAT-007 requirements?

**Strengths:**
The deliverable is exceptional in breadth of coverage. The FEAT-007 requirement identifies three themes: session start personality, progress celebrations, and companion feel. The deliverable expands these into six comprehensive areas, each with specific mechanisms:

- Session personality: 5 greeting variants (G-001 through G-005) with context-sensitive selection rules; 5 farewell variants (F-001 through F-005) with ordered selection rules; progress messages with energy calibration; session continuity signals.
- Companion behaviors: 5-context contextual awareness (debugging, creating, reviewing, exploring, error recovery); 6 encouragement triggers with data-specificity constraints; 5 boundary redirect scenarios; 4 knowledge-sharing triggers.
- Celebration design: Criticality-graduated (C1 through C4) quality gate celebrations; 4 milestone types; 5 achievement moment types; 6 named anti-patterns with fixes.
- Tone calibration: Complete attribute tables for each of 5 contexts with energy, humor, primary traits, personality budget, and behavior rules.
- Delight mechanics: Variant pools (minimum 3 per moment), 30% fallback weighting, staleness tracking; 5 time windows with interaction model; 5 streak types with threshold spacing; persisted state structure (8 fields).
- /saucer-boy integration: sb-reviewer routing table for 9 message categories; sb-calibrator scoring targets with 5-trait weights; tone spectrum position mapping for 12 contexts.

**Gaps identified:**

1. **State decay and long-horizon behavior not addressed.** The state management section specifies `last_scores: [{score, timestamp}, ...]` (last 5) and streak counters, but there is no specification for how stale state is handled. A developer returning to a project after 6 months: are streak counters still active? Is the last-5-scores window still relevant? The document addresses "zero state" (fresh checkout) but not "aged state" (partial/stale data that is technically present but contextually meaningless). This is a completeness gap for a companion system that is designed to persist across sessions.

2. **State file corruption or partial missing not addressed.** The document says state "must be recoverable from zero state." It does not specify behavior when state is present but incomplete (e.g., `achievement_flags` present but `streak_counters` missing). A complete spec should enumerate partial-state recovery behavior.

3. **No specification for developer preference management.** Time-of-day awareness is described as a "SOFT enhancement" that can be disabled by developer preference. Gentle redirects are MEDIUM-tier and can be overridden. But the document does not specify where these preferences are stored, how they are expressed, or how the framework reads them. This is acknowledged as an implementation detail but represents a genuine interface gap.

**Verdict:** Near-complete. The three gaps are real but do not undermine the primary delight system specification. They are refinements rather than structural omissions.

**Score: 0.91**

---

### 2. Internal Consistency — Score: 0.88

**Weight:** 0.20

**Question:** Are all parts internally consistent (no contradictions, aligned terminology)?

**Strengths:**
The three review rounds caught and fixed genuine inconsistencies: the `{secondary_observation}` placeholder mismatch between Message Catalog and Delight Mechanics (R1), the G-003 context description mismatch (R1), the FEAT-004/FEAT-006 integration overlap (R3). The farewell selection rules are ordered correctly with Powder Day taking precedence. Terminology is consistent throughout (C1/C2/C3/C4, PASS/REVISE/REJECTED, the specific variant ID naming scheme).

**Inconsistencies that remain:**

**Inconsistency IC-001 (One-Sentence Rule vs. C3 Message Catalog — SIGNIFICANT):**
Line 66 states: "if the delight element exceeds one sentence, it has become the message instead of enhancing it. This is a HARD constraint for all delight moments except the three Powder Day celebrations defined in the Celebration Design section." The three named exceptions are: F-003 (Powder Day farewell), C4 tournament pass, and epic complete.

However, the C3 Quality Gate PASS variants in the Message Catalog each contain two distinct personality phrases on separate lines:

- C3 V-001: `{standout_dimension} held across all sections.` + `That's a clean run. No gates clipped.`
- C3 V-002: `{dimension_summary}. {standout_dimension} was the difference.` + `Clean run.`
- C3 V-003: `Every dimension above threshold. {standout_dimension} led at {dim_score}.` + `The preparation showed.`

These are each two personality elements, not one. The Celebration Design section (line 273) explicitly authorizes "the observation plus one earned line of voice" for C3 -- so C3 is functionally a fourth exception to the one-sentence rule. The spec contradicts itself: the Design Philosophy states three exceptions; the Celebration Design section and Message Catalog implement a fourth.

**Inconsistency IC-002 (Farewell Selection Rule Ambiguity — MINOR):**
Farewell selection rule ordering:
1. If all items are complete: F-003.
2. If items were completed and all passed quality gates: F-005.
3. If items were completed: F-002.

Rule 2 applies when "items were completed and all passed quality gates." This rule is intended for partial-completion sessions where completed items all passed. But the rule as written would also match a session where all items were completed and all passed -- before rule 1 (F-003) is applied. Rule 1 correctly takes precedence due to ordering, but the rules do not include an explicit qualifier: "If items were completed and all passed quality gates (and NOT all items are complete)." A reader implementing these rules from this document could reasonably ask: does "all items complete + all passed" trigger F-003 or F-005? The ordering implies F-003, but the rule language does not make this explicit.

**Score: 0.88**

---

### 3. Methodological Rigor — Score: 0.92

**Weight:** 0.20

**Question:** Is the approach systematic, well-structured, following best practices?

**Strengths:**
The methodological structure is strong throughout:

- **Governing principle before rules.** The Design Philosophy section establishes the proportionality principle, the one-sentence rule, and what delight is NOT before any specifics are given. Rules cascade from principles.
- **Review process compliance.** H-14's 3-iteration minimum was met with three distinct strategies (S-010+S-003+S-002, S-002, S-007). Each round addressed open items from the previous round. 14 fixes applied and tracked.
- **Defensive specification.** The six anti-patterns section names failure modes explicitly, a practice that produces more resilient implementations than positive-only specs.
- **Quantified thresholds.** The 0.80 sb-calibrator target, 30% fallback weight, 0.92 quality gate, and delight budget numbers (2/4/6/8) are specific rather than vague.
- **Integration mapping.** The /saucer-boy section provides routing logic for which message categories require sb-reviewer validation -- a concrete implementation checklist.
- **Constitutional compliance.** R3 applied S-007 systematically against P-003, P-020, P-022, and the relevant H-rules. No violations found.
- **Self-review breadth.** 31-item self-review checklist covers the full deliverable scope.

**Weakness:**
Context detection signals remain vague: "command patterns and task metadata" (line 181) is the detection mechanism, but no specific signal taxonomy is provided. What command pattern constitutes "test failure" vs. "error in previous command"? What metadata field triggers "feature branch work"? The document correctly notes this is inference-based (P-022 compliance), but a more rigorous spec would enumerate the signal set even if implementation is flexible.

**Score: 0.92**

---

### 4. Evidence Quality — Score: 0.88

**Weight:** 0.15

**Question:** Are claims supported by evidence, citations, concrete examples?

**Strengths:**
The document provides substantial evidence support:

- **Source traceability.** All 6 source documents cited with version numbers in the Traceability section. Specific line references given for FEAT-006 (line 731-733 of ps-creator-006-draft.md).
- **Rule references.** Constitutional rules cited throughout: P-003, P-020, P-022, H-13, H-14, H-15, H-16, H-20, H-21, H-23, H-24. Not asserted without grounding.
- **Concrete message templates.** The Message Catalog provides complete, ready-to-use templates. The State Management section provides a full YAML structure. Evidence is not just prose description but executable specification.
- **Authenticity Tests.** The persona doc's 5-test battery is referenced as a quality gate for all templates, providing an external validation framework.
- **Soundtrack energy anchors.** Each tone context cites a specific track (artist, title, year, energy description) from the canonical EPIC-001 playlist. This is traceable evidence for the energy calibration, not arbitrary assignment.

**Weaknesses:**

1. **Design decisions lack empirical grounding.** The proportionality principle is stated as "the governing constraint" but is not supported by evidence. Why does C2 get one observation and C3 get one earned line? Why is the delight budget 4 for a 15-60 minute session? Why is 30% the right fallback weight? These numbers are reasonable but asserted, not derived from user research, domain literature, or calibration studies. For a design spec this is normal practice, but the evidence quality dimension must penalize unsupported quantitative claims.

2. **FEAT-003 alignment is preliminary.** FEAT-003 is at v0.1.0 (DRAFT). The visual identity alignment claimed in the self-review carries the caveat "preliminary and should be re-confirmed when FEAT-003 reaches REVIEWED status." This is an honest acknowledgment, but it means ~5% of the design's evidence base is unconfirmed. The box-art patterns, celebration tiers, and skier emoji usage all reference FEAT-003, whose design may change.

3. **Boundary between companion behaviors and implementation assumption.** The knowledge sharing section says "first time using a skill" as a detection trigger. R2's Challenge R2-C3 notes that "first time" should be framework-wide, not project-scoped, but concludes the spec language "is ambiguous in the right direction." Ambiguous evidence is not strong evidence.

**Score: 0.88**

---

### 5. Actionability — Score: 0.88

**Weight:** 0.15

**Question:** Can someone implement this directly without ambiguity?

**Strengths:**
The deliverable is implementer-facing in multiple ways:

- **Complete message templates.** A developer can lift the Message Catalog templates and begin implementation immediately. Templates include placeholders ({score}, {standout_dimension}, {project}, etc.) that are implementation-ready.
- **State management YAML.** The `delight_state:` structure in the Implementation Guidance section provides the schema for state persistence.
- **Selection rule ordering.** Greeting and farewell selection rules are numbered priority lists that can be implemented as if-else chains.
- **sb-reviewer routing table.** The 9-row table specifying which message categories require sb-reviewer validation is a concrete implementation checklist.
- **Budget enforcement mechanism.** The Budget Enforcement paragraph specifies the `delight_budget_remaining` counter, pre-allocation of greetings/farewells, V-FALLBACK selection, and tier boundary adjustment. A developer can implement this directly.

**Weaknesses:**

1. **Context detection is underspecified.** The Contextual Awareness section specifies five contexts with detection signals, but the signals are high-level: "Error in previous command, test failure, traceback in output" for debugging; "New file creation, feature branch work, implementation tasks" for creating. These are functional descriptions, not implementable specifications. What API, log, or metadata source provides "error in previous command"? How does the framework detect "feature branch work"? An implementer faces genuine ambiguity here.

2. **Staleness tracking is unspecified.** The Randomized Message Variants section says "avoid repeats within the same session" and the Implementation Guidance says "Track how many times each variant has been shown within a session and across recent sessions." But "recent sessions" is not defined. Last 3? Last 5? The variant_history in the state YAML stores timestamps but no retention window is specified. An implementer must make an arbitrary choice where the spec should provide a RECOMMENDED value.

3. **Preference storage interface is absent.** Developer preferences (disable time-of-day, override redirects) are mentioned but not specified. Where are they stored? How are they expressed? This gap requires an implementer to design an interface not specified by the document.

4. **No error states for the delight system itself.** What happens if `delight_state` fails to load? What happens if WORKTRACKER.md cannot be written for achievement persistence? The document says "recoverable from zero state" but doesn't address failure modes in the delight system's own operation.

**Score: 0.88**

---

### 6. Traceability — Score: 0.88

**Weight:** 0.10

**Question:** Can we trace requirements to implementation and back?

**Strengths:**
The document provides solid forward and backward traceability mechanisms:

- **Source document traceability.** The Traceability section maps 6 source documents to their contributions. Version numbers are pinned.
- **Constitutional rule citations.** H-xx and P-xxx references throughout the document create traceable compliance claims.
- **Review round traceability.** Each review document records what was found, what was fixed, and what version the draft moved to. 14 fixes are tracked across 3 rounds.
- **Self-review as forward traceability.** The 31-item self-review checklist maps design areas to PASS/FAIL verification outcomes.
- **Feature integration traceability.** The R3 cross-feature consistency check table (5 checks) creates explicit traceability between FEAT-007 and FEAT-004/FEAT-005/FEAT-006/FEAT-003.

**Weaknesses:**

1. **No bi-directional requirements traceability matrix.** The FEAT-007 requirement in EPIC-001 is a single sentence. The deliverable expands this into 6 major functional areas and dozens of sub-requirements. However, there is no explicit mapping from deliverable sections back to the parent requirement, nor from EPIC-001's FEAT-007 description to specific deliverable sections. The Requirements Verification table in R3 (lines 195-202) provides round-level traceability, but it is in the review document, not the deliverable itself.

2. **Soundtrack energy anchor citations are not bi-directional.** The document cites soundtrack anchors (Gang Starr "Moment of Truth," Daft Punk "Harder, Better, Faster, Stronger," etc.) back to FEAT-005 and EPIC-001's soundtrack table. But the anchors are not enumerated in a traceability section -- they are embedded in the Tone Calibration section. A future reader checking FEAT-005 alignment cannot easily confirm that all anchors reference tracks on the canonical list without reading the full Tone Calibration section.

3. **Achievement moment traceability to FEAT-006 is asymmetric.** The Celebration Design section now includes the FEAT-006 disambiguation (added in R3). But the traceability section does not list FEAT-006 as a source, even though R3 explicitly found that FEAT-006's achievement disambiguation belongs in FEAT-007's design.

**Score: 0.88**

---

## Strengths

The following are the deliverable's most significant strengths, identified independently:

**1. Proportionality as a governing constraint.** The C1-C4 graduation of celebration energy is not just a design choice -- it is a load-bearing structural decision that prevents the two most common delight system failures simultaneously (inflation and monotony). By anchoring celebration energy to the existing quality-enforcement.md criticality levels, the design inherits an already-validated classification system rather than inventing its own.

**2. Anti-pattern specification.** Naming six failure modes (Inflation, Fatigue, Premature, Tone-deaf, Performative, Dismissive) with concrete descriptions and fixes is defensive specification at its best. This section will prevent implementation errors that no amount of positive specification would catch. The "Tone-deaf" anti-pattern (celebrating after hard-won passes) demonstrates unusual situational awareness.

**3. Zero personality in high-stakes contexts.** The decision to set personality budget to zero in debugging and error recovery is correctly reasoned and correctly implemented. The Soundtrack energy anchor for error recovery (Radiohead "Everything in Its Right Place") is an evocative calibration tool that accurately captures the emotional register without requiring explicit description.

**4. Budget enforcement with pre-allocation.** The delight budget system (2/4/6/8 per session duration) with the specific mechanism of pre-allocating greeting/farewell slots is an elegant solution to the Powder Day vs. budget-exhaustion conflict identified in R2-C5. Pre-allocation ensures high-value delight moments (session boundaries) are always reserved, while contextual budget limits mid-session personality.

**5. P-022 compliance by design.** The document builds honesty into the companion's architecture: context detection is acknowledged as inference-based and fallible; session continuity draws only from persisted state; encouragement requires specific data citations; fabricated familiarity is prohibited. These are not afterthoughts -- they are design constraints embedded throughout.

**6. Implementation Guidance quality.** The "How to Build This Without It Feeling Mechanical" section is rare in specifications. The "template detector" test ("If you can hear the curly braces, the template is showing") is an implementer-facing heuristic that cannot be derived from the rules themselves. It addresses the gap between specification and craft.

---

## Weaknesses

**1. One-sentence rule vs. C3 exception list (IC-001).**
The most significant surviving defect. Design Philosophy states three exceptions to the one-sentence rule; the Celebration Design section and Message Catalog implement a fourth (C3's "one earned line" = two personality elements). This inconsistency survived three review rounds and creates genuine implementer confusion: is C3 covered by the one-sentence rule or not?

**2. Context detection underspecified.**
Five contexts are defined but detection signals are high-level prose. An implementer faces real ambiguity: what system call, log entry, or metadata field constitutes "error in previous command"? What distinguishes "feature branch work" from other creating tasks? The document correctly calls out inference fallibility (P-022 compliance) but does not provide enough signal taxonomy for confident implementation.

**3. Staleness window undefined.**
"Recent sessions" for variant staleness tracking is undefined. "Across recent sessions" in the Implementation Guidance and "variant_history" in the state YAML share this gap. An implementer must choose an arbitrary window without guidance.

**4. Farewell rule IC-002 ambiguity.**
The farewell selection rules technically cover the all-complete+all-passed case by ordering, but the language does not make the mutual exclusion explicit. A defensive implementer would add the qualifier; a literal implementer might not.

**5. Unsupported quantitative claims.**
The delight budget numbers (2/4/6/8), the 30% fallback weight, and the sb-calibrator threshold (0.80) are stated without derivation or citation. These are reasonable but asserted. Evidence Quality is penalized for this.

**6. Developer preference interface absent.**
Two preference override capabilities are specified (disable time-of-day, override redirects) with no specification of where preferences are stored or how they are expressed. This creates a design gap that downstream implementation must fill without guidance.

---

## Composite Score and Verdict

### Score Calculation

| Dimension | Weight | Raw Score | Weighted Score |
|-----------|--------|-----------|----------------|
| Completeness | 0.20 | 0.91 | 0.182 |
| Internal Consistency | 0.20 | 0.88 | 0.176 |
| Methodological Rigor | 0.20 | 0.92 | 0.184 |
| Evidence Quality | 0.15 | 0.88 | 0.132 |
| Actionability | 0.15 | 0.88 | 0.132 |
| Traceability | 0.10 | 0.88 | 0.088 |
| **COMPOSITE** | **1.00** | | **0.894** |

### Verdict

**Band: REVISE (0.85 -- 0.91)**

**Composite score: 0.894**

**Disposition: REJECTED per H-13.** Score is below the 0.92 threshold for C2 deliverables. The deliverable is in the REVISE band -- near threshold -- meaning targeted revision on the weakest dimensions is likely sufficient to achieve PASS. Significant structural rework is not required.

---

## Revision Guidance (REVISE Band)

The deliverable is 0.026 below threshold. The following targeted fixes address the specific defects identified:

### Fix RV-001: Resolve IC-001 (One-Sentence Rule vs. C3) [REQUIRED — Internal Consistency]

**Target:** Design Philosophy section, "The One-Sentence Rule" (line 66), and Celebration Design, "Celebration Escalation Rules" (line 271).

**The gap:** The one-sentence rule states three exceptions (F-003, C4, epic complete). C3's "one earned line" in the Celebration Escalation Rules and the C3 Message Catalog variants implement a fourth exception without naming it.

**Fix options (choose one):**
- A. Add C3 to the exception list: "This is a HARD constraint for all delight moments except the four multi-element celebrations: F-003 Powder Day farewell, C4 tournament pass, epic complete, and C3 quality gate passes (which receive the base message plus one earned phrase)."
- B. Redefine the rule to accommodate C3 explicitly: "Delight elements in C1 and C2 contexts are limited to one sentence. C3 allows one additional earned phrase. C4 and Powder Day events allow full multi-element celebration."
- C. Restructure C3 Message Catalog variants to be single-sentence compliant: collapse the two personality elements into one.

Option B is recommended -- it makes the graduation explicit rather than listing exceptions.

### Fix RV-002: Add "Recent Sessions" Retention Window [REQUIRED — Actionability]

**Target:** Delight Mechanics, Randomized Message Variants, "Variant Pool Rules" (line 421), and Implementation Guidance "Measure staleness" (line 682).

**The gap:** "Recent sessions" is undefined. The variant_history state field has no specified retention window.

**Fix:** Add a RECOMMENDED retention window: "Staleness tracking covers the last 5 sessions or 30 days, whichever is shorter. Variants that have appeared in this window are deprioritized. The retention window is tunable but SHOULD not be set below 3 sessions."

### Fix RV-003: Clarify Farewell IC-002 (Mutual Exclusion) [RECOMMENDED — Internal Consistency]

**Target:** Session Personality, Session Farewells, "Farewell Selection Rules" (line 133).

**The gap:** Rule 2 ("all completed and all passed quality gates") does not explicitly exclude the all-items-complete case.

**Fix:** Add qualifier to rule 2: "2. If items were completed, all passed quality gates, AND not all items in the session are complete: F-005."

### Fix RV-004: Add FEAT-006 to Traceability Table [RECOMMENDED — Traceability]

**Target:** Traceability section.

**The gap:** R3 fixed a FEAT-006 integration inconsistency (achievement disambiguation), but FEAT-006 is not listed as a source in the Traceability section.

**Fix:** Add row: `ps-creator-006-draft.md (current version) | Easter Eggs: achievement moment disambiguation (visible vs. hidden delight boundary, lines 731-733).`

### Fix RV-005: Specify Preference Storage Interface Minimally [RECOMMENDED — Actionability]

**Target:** Time-of-Day Awareness section and Gentle Redirects section.

**The gap:** Two preference overrides are specified without a storage mechanism.

**Fix:** Add a RECOMMENDED mechanism: "Developer preferences SHOULD be stored in a `delight_preferences` section of WORKTRACKER.md metadata, using the same pattern as `delight_state`. Recognized keys: `disable_time_of_day: bool` (default false). Implementation MAY use environment variables as an alternative (e.g., `JERRY_DELIGHT_TIME_AWARE=false`)."

---

## Metadata

```yaml
scorer: adv-scorer-007
strategy: S-014 (LLM-as-Judge)
deliverable: ps-creator-007-draft.md
deliverable_version: "0.4.0"
workflow: jnsq-20260219-001
feature: FEAT-007
criticality: C2
date: "2026-02-19"
independence: true
prior_exposure: false

scores:
  completeness:
    weight: 0.20
    raw: 0.91
    weighted: 0.182
  internal_consistency:
    weight: 0.20
    raw: 0.88
    weighted: 0.176
  methodological_rigor:
    weight: 0.20
    raw: 0.92
    weighted: 0.184
  evidence_quality:
    weight: 0.15
    raw: 0.88
    weighted: 0.132
  actionability:
    weight: 0.15
    raw: 0.88
    weighted: 0.132
  traceability:
    weight: 0.10
    raw: 0.88
    weighted: 0.088

composite: 0.894
threshold: 0.92
delta_to_threshold: -0.026
band: REVISE
verdict: REJECTED
h13_compliant: false

revision_required: true
revision_priority:
  - RV-001  # IC-001: one-sentence rule vs. C3 (REQUIRED)
  - RV-002  # staleness window (REQUIRED)
  - RV-003  # farewell IC-002 clarification (RECOMMENDED)
  - RV-004  # FEAT-006 traceability (RECOMMENDED)
  - RV-005  # preference storage interface (RECOMMENDED)

weakest_dimensions:
  - internal_consistency: 0.88  # IC-001 surviving inconsistency
  - evidence_quality: 0.88      # unsupported quantitative claims
  - actionability: 0.88         # context detection, staleness window
  - traceability: 0.88          # no bi-directional RTM, FEAT-006 missing
```
