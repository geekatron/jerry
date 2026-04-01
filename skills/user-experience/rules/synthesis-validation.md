<!-- VERSION: 1.1.0 | DATE: 2026-03-04 | SOURCE: SKILL.md (skills/user-experience/SKILL.md) Sections "Synthesis Hypothesis Validation", "Cross-Framework Synthesis Protocol" | PARENT: /user-experience skill | REVISION: iter3 — address iter1+iter2 adversarial findings: add /ux-heuristic-eval rows, external citations, convergence elaboration annotations, CRISIS cross-reference, expanded failure modes, mixed-confidence rule, signal extraction completeness -->

# Synthesis Validation Rules

> Validation rules for cross-framework synthesis hypotheses produced by the ux-orchestrator agent. Enforces confidence classification gates (HIGH/MEDIUM/LOW) per P-022. See also: `skills/user-experience/rules/ux-routing-rules.md` (routing to sub-skills that produce synthesis inputs), `skills/user-experience/rules/wave-progression.md` (wave gates that determine which sub-skills are available for synthesis), `skills/user-experience/rules/mcp-coordination.md` (MCP availability affecting synthesis quality).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Confidence Classification](#confidence-classification) | HIGH/MEDIUM/LOW gate definitions and enforcement |
| [Sub-Skill Synthesis Output Map](#sub-skill-synthesis-output-map) | Per-sub-skill confidence assignments |
| [Cross-Framework Synthesis Protocol](#cross-framework-synthesis-protocol) | 4-step synthesis mechanism |
| [Convergence Thresholds](#convergence-thresholds) | When findings from multiple frameworks agree |
| [Contradiction Handling](#contradiction-handling) | When frameworks produce conflicting findings |
| [Synthesis Output Structure](#synthesis-output-structure) | Required sections, format, and CRISIS variant |
| [Failure Mode Handling](#failure-mode-handling) | Low-confidence synthesis escalation and degraded-mode behavior |
| [Constitutional References](#constitutional-references) | Governance document cross-references for standalone traceability |

---

## Confidence Classification

<!-- Source: SKILL.md Section "Synthesis Hypothesis Validation" — 3-tier confidence gate. -->

All synthesis hypotheses MUST include confidence classification per P-022 (no deception about confidence). The orchestrator assigns confidence at synthesis time based on evidence convergence.

### Gate Definitions

| Confidence | Definition | Gate Behavior | Advancement Rule |
|------------|-----------|--------------|-----------------|
| **HIGH** | 3+ frameworks converge on the same finding, OR 2 frameworks converge with strong quantitative evidence | User reviews output + acknowledges specific AI judgment calls via Synthesis Judgments Summary | Advances to design decisions after enumerated acknowledgment |
| **MEDIUM** | 2 frameworks converge OR 1 framework with strong evidence (quantitative data, established methodology, large sample) | Requires expert review OR validation against 2-3 real user data points | Cannot advance to design decisions without named validation source |
| **LOW** | Single framework finding with weak evidence, contradiction present, or AI inference without empirical grounding | Output permanently labeled reference-only; design recommendation section structurally omitted | Cannot be overridden by any user action |

### Gate Enforcement Mechanisms

- **HIGH gate:** Output includes a "Synthesis Judgments Summary" section listing each AI judgment call (e.g., "Interpreted slow task completion as navigation confusion rather than content scanning behavior"). Acknowledgment prompt presented before design recommendations are generated. User must confirm they have reviewed each judgment call.
- **MEDIUM gate:** Output includes a "Validation Required" section with placeholder fields for: (a) expert name and credentials, (b) user data reference (study, interview count, analytics source), or (c) literature citation. Design recommendations are withheld until at least one validation source is provided.
- **LOW gate:** Output template structurally omits the design recommendation section. Title tagged with `[REFERENCE-ONLY]`. Banner: "This output reflects AI synthesis from training data. It does not contain design recommendations."

### Classification Immutability

- HIGH may be downgraded to MEDIUM or LOW by the receiving sub-skill based on its own assessment (confidence propagation per `skills/user-experience/rules/ux-routing-rules.md#cross-sub-skill-handoff`).
- MEDIUM may be downgraded to LOW but NEVER upgraded to HIGH without additional evidence.
- LOW is permanent. No user action, expert review, or additional data can override a LOW classification within the same engagement. A new engagement with fresh evidence can produce a different classification.

---

## Sub-Skill Synthesis Output Map

<!-- Source: SKILL.md Section "Synthesis Hypothesis Validation" — per-sub-skill confidence table ("Typical Confidence" column in SKILL.md). This rule file uses "Typical Confidence" to match the SKILL.md source terminology. The SKILL.md table contains 12 rows across 9 sub-skills; this rule file adds 4 rows (2 for /ux-heuristic-eval, 2 for /ux-atomic-design) to cover all 10 sub-skills comprehensively. Added rows are marked with provenance annotations. -->

Each sub-skill synthesis step has a typical confidence based on methodology characteristics. The orchestrator uses these as starting points; actual confidence may differ based on evidence quality in each engagement.

| Sub-Skill | Synthesis Step | Typical Confidence | Rationale |
|-----------|---------------|-------------------|-----------|
| `/ux-heuristic-eval` | Severity rating calibration across heuristics | MEDIUM | Severity ratings involve subjective judgment; calibration across Nielsen's 10 heuristics (Nielsen, 1994a) requires consistent application context. <!-- Provenance: added at rule-file level; SKILL.md synthesis map omits /ux-heuristic-eval rows. Added because /ux-heuristic-eval is a Wave 1 core sub-skill and produces severity-rated findings consumed by the Signal Extraction Criteria table. --> |
| `/ux-heuristic-eval` | Comparative evaluation synthesis (cross-product or cross-version) | HIGH | Based on systematic checklist methodology with observable UI artifacts; HIGH when screenshots/screen recordings available as concrete evidence beyond subjective assessment. <!-- Provenance: added at rule-file level; same rationale as severity rating row above. Comparative synthesis across products/versions produces convergent evidence from repeated checklist application. --> |
| `/ux-jtbd` | Job statement synthesis from secondary research | MEDIUM | Secondary research lacks direct user observation (Ulwick, 2016; Christensen et al., 2016) |
| `/ux-lean-ux` | Assumption mapping; hypothesis generation | MEDIUM | Hypotheses are deliberately unvalidated per Lean UX methodology (Gothelf & Seiden, 2021) |
| `/ux-design-sprint` | Day 4 interview thematic analysis | HIGH | Based on direct user interviews (5 users per Sprint methodology; Knapp, Zeratsky & Kowitz, 2016) |
| `/ux-design-sprint` | Day 2 sketch selection rationale | MEDIUM | Selection rationale involves subjective judgment among sprint participants |
| `/ux-inclusive-design` | Persona Spectrum customization | MEDIUM | Persona Spectrums are heuristic models (Microsoft Inclusive Design Toolkit, 2016), not empirical profiles |
| `/ux-kano-model` | Directional classification (5-8 respondents) | MEDIUM | Small sample provides directional signal only; Kano survey requires >= 20 respondents for statistical classification (Berger et al., 1993), so 5-8 yields MEDIUM |
| `/ux-kano-model` | Feature priority conflict interpretation | LOW | Resolving conflicting priorities requires domain context AI lacks |
| `/ux-behavior-design` | B=MAP bottleneck diagnosis | MEDIUM | Fogg Behavior Model (Fogg, 2020) application to specific context is interpretive; B=MAP framework provides structured diagnosis but bottleneck attribution requires user-specific data |
| `/ux-behavior-design` | Design intervention recommendation | LOW | Intervention effectiveness depends on context-specific factors that training data cannot capture |
| `/ux-heart-metrics` | Goal-metric mapping interpretation | MEDIUM | HEART framework (Rodden, Hutchinson & Fu, 2010) mapping is methodologically grounded but context-dependent |
| `/ux-heart-metrics` | Metric threshold recommendation | LOW | Threshold values require domain-specific benchmarking data unavailable in training data |
| `/ux-ai-first-design` | AI interaction pattern recommendations | LOW | AI design patterns are rapidly evolving; training data may be stale relative to current best practices |
| `/ux-atomic-design` | Component taxonomy completeness assessment | MEDIUM | Taxonomy assessment depends on Storybook coverage (Frost, 2016); partial coverage yields partial assessment |
| `/ux-atomic-design` | Design token consistency analysis | LOW | Token consistency across a full system requires inspection of all component variants; AI sampling may miss edge cases. <!-- Provenance: added at rule-file level; SKILL.md synthesis map omits /ux-atomic-design design token analysis. Added because design token consistency is a common atomic design synthesis task and the /ux-atomic-design sub-skill produces component inventories where token analysis is a natural synthesis step. --> |

### Mixed-Confidence Resolution Rule

When a single sub-skill produces multiple synthesis steps with different confidence levels (e.g., `/ux-kano-model` produces both "Directional classification" at MEDIUM and "Feature priority conflict interpretation" at LOW), and both steps contribute signals to the same synthesis finding, the orchestrator applies the **minimum-confidence rule**: the final synthesis confidence for that finding is the lowest confidence among all contributing synthesis steps. This prevents confidence inflation when a high-confidence signal is combined with a low-confidence interpretation from the same sub-skill.

---

## Cross-Framework Synthesis Protocol

<!-- Source: SKILL.md Section "Cross-Framework Synthesis Protocol" — 4-step sequential mechanism. -->

When the orchestrator invokes multiple sub-skills for the same engagement, it produces a cross-framework synthesis after all sub-skill outputs are available.

### Trigger

Two or more sub-skill outputs exist for the same engagement ID.

### Synthesis Scope Rule

When multiple outputs exist per sub-skill for the same engagement ID (e.g., iterative heuristic evaluations), the orchestrator uses the **most recent output** per sub-skill per engagement ID. If a sub-skill has produced outputs at different dates, only the latest output file (determined by file modification timestamp or explicit version marker in the output) is included in synthesis. Prior outputs are not discarded but are excluded from synthesis to prevent double-counting.

### Mechanism (4-Step Sequential)

| Step | Name | Input | Output | Validation Check |
|------|------|-------|--------|-----------------|
| 1 | **Signal Extraction** | Each sub-skill output's findings/recommendations sections | Actionable signals with source reference | Each signal traces to a specific finding number in a specific sub-skill output |
| 2 | **Convergence Detection** | Extracted signals from all sub-skills | Grouped signals per [Convergence Thresholds](#convergence-thresholds): Strong/Moderate convergence (HIGH), Weak convergence (MEDIUM), No convergence (MEDIUM) | Convergent groups cite all contributing sub-skills; no signal appears in multiple groups; confidence assigned per convergence level |
| 3 | **Contradiction Identification** | Signals that recommend opposing actions | Flagged contradictions with both positions preserved | Every contradiction has exactly 2 opposing positions; no resolution is attempted |
| 4 | **Unified Output** | Convergent findings, singletons, contradictions | Synthesis report with 3 sections per confidence level | All signals from Step 1 appear in exactly one output section |

### Signal Extraction Criteria

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Section "Cross-Framework Synthesis Protocol" — signal extraction per sub-skill type. Extraction criteria thresholds align with each sub-skill's methodology-specific severity or priority scales. External citations for threshold derivations are provided inline. SKILL.md names 8 sub-skill types in the narrative description; this table adds Design Sprint and AI-First Design rows (provenance: rule-file elaboration) to cover all 10 sub-skills. -->

Signals are extracted based on sub-skill type:

| Sub-Skill Type | Signal Extraction Criteria | Threshold Source |
|---------------|--------------------------|-----------------|
| Heuristic Eval | Findings rated severity >= 2 (out of 0-4 scale) | Nielsen severity rating scale: 0=not a problem, 1=cosmetic, 2=minor, 3=major, 4=catastrophic (Nielsen, 1994b, "Severity Ratings for Usability Problems") |
| HEART Metrics | Metrics below target threshold | HEART framework GSM process (Rodden, Hutchinson & Fu, 2010, CHI '10); threshold is engagement-specific |
| Lean UX | Unvalidated assumptions; invalidated hypotheses | Lean UX Build-Measure-Learn cycle (Gothelf & Seiden, 2021); unvalidated = no experiment data |
| Behavior Design | B=MAP bottleneck diagnoses | Fogg Behavior Model B=MAP (Fogg, 2020, "Tiny Habits"); bottleneck = any factor (Motivation, Ability, Prompt) below action threshold |
| JTBD | Switch forces (push/pull) with strength >= 3 (out of 1-5 scale) | Jobs-to-be-Done switch interview methodology (Moesta & Spiek, 2014; Ulwick, 2016, "Jobs to Be Done"); strength >= 3 = "moderate or higher" on 5-point force scale |
| Kano | Features classified as Must-be or Attractive | Kano Model (Kano et al., 1984); Must-be and Attractive categories per functional/dysfunctional questionnaire methodology; sample size note: 5-8 respondents yields directional classification only (Berger et al., 1993, recommend >= 20 for statistical confidence) |
| Atomic Design | Components with no Storybook coverage | Atomic Design methodology (Frost, 2016, "Atomic Design"); Storybook coverage = component has at least one documented story |
| Inclusive Design | WCAG violations at AA or higher | WCAG 2.2 AA conformance level (W3C, 2023); AA is the standard compliance target for most products |
| Design Sprint | Interview themes identified by >= 3 of 5 users in Day 4 testing | Google Ventures Design Sprint (Knapp, Zeratsky & Kowitz, 2016, "Sprint"); 5-user threshold per Sprint methodology; >= 3/5 = majority pattern. <!-- Provenance: rule-file elaboration; SKILL.md narrative mentions Design Sprint signal extraction without specifying the threshold. --> |
| AI-First Design | Patterns flagged as HIGH trust-risk or HIGH error-risk in AI interaction audit | AI-First Design risk classification; trust-risk and error-risk are the two primary failure modes in AI interaction design (Yang et al., 2020, CHI '20, "Re-examining Whether, Why, and How Human-AI Interaction Is Uniquely Difficult to Design"). <!-- Provenance: rule-file elaboration; SKILL.md narrative does not specify AI-First Design extraction criteria. --> |

---

## Convergence Thresholds

<!-- Source: SKILL.md Section "Cross-Framework Synthesis Protocol" — convergence detection. SKILL.md states: "Convergent signals (2+ frameworks identify the same issue) receive HIGH synthesis confidence. Single-framework signals receive MEDIUM." This rule file elaborates the SKILL.md rule into a 4-level classification (Strong/Moderate/Weak/No convergence) to distinguish evidence quality within the 2+ framework HIGH band. The elaboration is consistent with SKILL.md: all 2+ convergent signals remain HIGH or above, and all single-framework signals remain MEDIUM. The Strong/Moderate distinction operationalizes P-022 (no deception about confidence) by differentiating strength of convergence evidence. Source: quality-enforcement.md H-13 (quality threshold) motivates the finer-grained classification for C2+ deliverable support. -->

| Convergence Level | Definition | Synthesis Confidence | Example | Source |
|-------------------|-----------|---------------------|---------|--------|
| **Strong convergence** | 3+ frameworks identify the same UX problem | HIGH | Heuristic Eval finds navigation confusion (severity 3) + HEART shows low Task Success for navigation + Behavior Design diagnoses ability bottleneck in navigation | SKILL.md "2+ frameworks = HIGH" (3+ is strictly stronger) |
| **Moderate convergence** | 2 frameworks identify the same UX problem with supporting quantitative or observational evidence | HIGH | Heuristic Eval finds form error visibility issue (severity 3) + Inclusive Design finds form WCAG violation (AA level) — both provide concrete evidence beyond subjective assessment | Elaboration of SKILL.md "2+ frameworks = HIGH"; qualified by evidence quality per P-022 |
| **Weak convergence** | 2 frameworks identify related but not identical problems | MEDIUM | JTBD identifies "quick checkout" job + HEART shows low Happiness for checkout (related but different lens) | Elaboration: "related but not identical" fails the Convergence Matching Rule 2 "same user problem" test, downgrading from SKILL.md's default HIGH for 2+ frameworks |
| **No convergence** | Single framework finding with no corroboration | MEDIUM | Only Kano model identifies a feature as Must-be; no other framework addresses that feature | Direct from SKILL.md: "Single-framework signals receive MEDIUM" |

### Convergence Matching Rules

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Section "Cross-Framework Synthesis Protocol" — convergence detection rules. Rule 2 operationalizes P-022 (no deception about confidence): when the orchestrator is uncertain whether signals describe the same user problem, it defaults to "related but NOT convergent" to prevent confidence inflation. -->

1. **Same screen/flow:** Signals that reference the same screen, flow, or component are candidates for convergence.
2. **Same user problem:** Signals that describe the same user-facing problem (even using different vocabulary) are convergent. Operationally, "same user problem" means: (a) both signals describe the same user action or goal being impeded, AND (b) both signals affect the same user population segment (or one applies to a superset of the other). When the orchestrator is uncertain whether signals describe the same problem, it defaults to "related but NOT convergent" to avoid inflating confidence (P-022; see [Constitutional References](#constitutional-references)).
3. **Same metric impact:** Signals that predict impact on the same HEART metric (Rodden, Hutchinson & Fu, 2010) are candidates for convergence.
4. **Partial overlap:** When signals overlap on one dimension (e.g., same screen but different problems), they are noted as related but NOT convergent.
5. **Population overlap tiebreak:** When user populations partially overlap (e.g., one signal applies to "mobile users" and another to "all users"), treat as convergent if the overlapping population segment constitutes >= 50% of the smaller population segment. When the overlap proportion is uncertain, apply the P-022 conservative default ("related but NOT convergent").

---

## Contradiction Handling

<!-- Source: SKILL.md Section "Cross-Framework Synthesis Protocol" — contradiction identification. -->

Contradictions occur when two or more frameworks recommend opposing actions for the same UX problem.

### Contradiction Detection

| Contradiction Type | Example | Handling |
|-------------------|---------|---------|
| **Direct opposition** | Heuristic Eval recommends simplifying a form; Kano Model identifies the removed fields as Must-be features | Present both positions with evidence; assign LOW confidence; user decides (P-020) |
| **Priority conflict** | HEART Metrics prioritizes Task Success improvements; Behavior Design prioritizes Motivation interventions (different bottleneck focus) | Present both priority frameworks; assign MEDIUM confidence; user decides sequencing |
| **Methodology conflict** | Lean UX invalidated a hypothesis that JTBD analysis supports as a core job need | Present the conflict; note methodological difference; assign LOW confidence; recommend additional user research |

### Contradiction Presentation Format

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Section "Cross-Framework Synthesis Protocol" — contradiction output format. The 6-field structure (ID, Position A, Position B, Additional Positions, Resolution, Confidence) enforces P-020 (user decides: "Resolution: User decision required") and P-022 (no AI-generated resolution presented as recommendation). N-way contradiction handling (field 4) extends the base 2-position format for 3+ framework conflicts. -->

Each contradiction in the synthesis output MUST include:

1. **Contradiction ID:** `CONTRA-{NNN}` sequential identifier
2. **Position A:** Framework name, finding reference, recommendation, evidence
3. **Position B:** Framework name, finding reference, recommendation, evidence
4. **Additional Positions (if applicable):** For n-way contradictions (3+ frameworks), list each additional framework as Position C, D, etc. with the same fields. When n > 2, the contradiction confidence is always LOW regardless of type.
5. **Resolution:** "User decision required" — no AI-generated resolution (P-020 compliance; see [Constitutional References](#constitutional-references))
6. **Confidence:** Always LOW for direct opposition or n-way (3+) contradictions; MEDIUM for 2-way priority/methodology conflicts

---

## Synthesis Output Structure

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Section "Cross-Framework Synthesis Protocol" — output structure requirements. Output filename convention: {topic-slug} per SKILL.md, e.g., ux-orchestrator-synthesis.md for standard synthesis, ux-orchestrator-crisis.md for CRISIS mode. See also: skills/user-experience/rules/ci-checks.md#output-quality-checks for CI gates UX-CI-011 through UX-CI-013 that validate synthesis output structure. -->

The orchestrator produces synthesis reports at `projects/${JERRY_PROJECT}/engagements/{engagement-id}/ux-orchestrator-synthesis.md` (engagement ID format defined in `skills/user-experience/rules/ux-routing-rules.md#cross-sub-skill-handoff`) with the following required sections:

| Section | Content | Confidence Level |
|---------|---------|-----------------|
| **Convergent Findings** | Findings where 2+ frameworks agree | HIGH |
| **Single-Framework Findings** | Findings from one framework only | MEDIUM |
| **Contradictions** | Findings where frameworks disagree | LOW (direct) or MEDIUM (priority/methodology) |
| **Synthesis Judgments Summary** | Enumerated list of AI judgment calls | N/A (meta-section) |
| **Validation Required** | Placeholder fields for MEDIUM findings | N/A (meta-section) |

### CRISIS Synthesis Variant

When the orchestrator operates in CRISIS mode (see `skills/user-experience/rules/ux-routing-rules.md#crisis-routing`), it produces a synthesis report at `projects/${JERRY_PROJECT}/engagements/{engagement-id}/ux-orchestrator-crisis.md`. The CRISIS synthesis follows the same 4-step protocol and confidence classification gates defined in this file, with the following CRISIS-specific additions managed by `ux-routing-rules.md`:

- **Priority ranking** of findings by user impact severity (CRISIS urgency ordering)
- **Quick-win identification** for findings addressable within one sprint
- **Metric coverage** mapping findings to HEART metrics for post-fix measurement

The CRISIS synthesis report structure, confidence gates, contradiction handling, and traceability requirements are identical to the standard synthesis defined in this file. Only the output filename and the three CRISIS-specific additions above differ. CI gates UX-CI-011 through UX-CI-013 (defined in `skills/user-experience/rules/ci-checks.md#output-quality-checks`) validate both synthesis filenames.

### MEDIUM Gate Validation Interaction Model

When the MEDIUM gate fires (see [Gate Enforcement Mechanisms](#gate-enforcement-mechanisms) above), the orchestrator collects the required validation source via the following interaction model: the orchestrator presents a validation prompt to the user requesting one of the three validation sources (expert name and credentials, user data reference, or literature citation). Upon receipt, the orchestrator includes the validation reference in the output's "Validation Required" section and generates the design recommendations section. If the user declines to provide a validation source, the findings remain at MEDIUM confidence with the design recommendations withheld, and the output is delivered without them (user decision per P-020).

### Required Traceability

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Section "Cross-Framework Synthesis Protocol" — output traceability requirements. These 4 required fields (source sub-skill, finding ID, engagement ID, confidence classification) enable CI gate UX-CI-012 (Traceability Check) defined in `skills/user-experience/rules/ci-checks.md#output-quality-checks`. -->

Every finding in the synthesis output MUST include:

- Source sub-skill name (e.g., `/ux-heuristic-eval`)
- Source finding ID (e.g., `HE-003`)
- Engagement ID
- Confidence classification with rationale

---

## Failure Mode Handling

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Section "Cross-Framework Synthesis Protocol" — failure modes. See also: skills/user-experience/rules/mcp-coordination.md#degraded-mode-behavior for MCP-related failure modes that affect synthesis input quality. -->

### Failure Mode Table

| Failure Mode | Detection | Orchestrator Action | Confidence Impact |
|-------------|-----------|-------------------|-------------------|
| **Low-Confidence Majority** | > 50% of findings classified as LOW | Add banner (see below); continue synthesis; deliver output with banner for user decision (P-020) | No override; LOW findings remain LOW |
| **Malformed Sub-Skill Output** | Sub-skill output missing required traceability fields (source finding ID, engagement ID) per [Required Traceability](#required-traceability) | Exclude the malformed output from synthesis; log the exclusion in the synthesis report's "Synthesis Judgments Summary" section; include a note: "Output from {sub-skill} excluded due to missing traceability fields" | Remaining sub-skill outputs synthesized normally; if exclusion reduces convergent signals below threshold, confidence may downgrade |
| **Empty Synthesis Result** | Convergence detection (Step 2) produces zero convergent findings AND zero contradictions (all signals are singletons) | Produce synthesis report with only "Single-Framework Findings" section populated; add note: "No cross-framework convergence detected. All findings are from individual frameworks." | All findings MEDIUM (no convergence) |
| **MCP Degraded Synthesis Inputs** | Sub-skill operated in text-only mode due to MCP unavailability (see `skills/user-experience/rules/mcp-coordination.md#degraded-mode-behavior`) | Accept sub-skill output but note MCP degradation in synthesis report; add note per affected finding: "Source sub-skill operated without MCP design artifact access" | No automatic downgrade; MCP degradation affects input quality, which is reflected in the sub-skill's own confidence assessment |

### Low-Confidence Majority

If synthesis confidence is LOW across > 50% of findings, the orchestrator adds a banner:

> "Cross-framework synthesis produced mostly low-confidence results. Consider validating individual sub-skill outputs independently before acting on synthesis recommendations."

This is a P-022 compliance mechanism (see [Constitutional References](#constitutional-references)) — the orchestrator does not overstate the value of synthesis when evidence is weak. After displaying the banner, the orchestrator continues synthesis and delivers the complete output to the user. The user decides whether to act on the synthesis or review individual sub-skill outputs instead (P-020).

### Synthesis Scope Limitation (v1.0.0)

Cross-framework synthesis operates on textual output from sub-skills. It does not access MCP design artifacts directly — synthesis inputs are the sub-skill reports, not raw Figma/Miro data. Future versions may add MCP-aware synthesis if usage patterns warrant it.

---

## Constitutional References

> Standalone traceability for governance principles cited in this file. This section ensures readers outside the SKILL.md context can locate the authoritative sources.

| Principle | Description | Authoritative Source |
|-----------|-------------|---------------------|
| P-003 | No recursive subagents; max 1 level | `docs/governance/JERRY_CONSTITUTION.md` |
| P-020 | User authority; never override user decisions | `docs/governance/JERRY_CONSTITUTION.md` |
| P-022 | No deception about actions, capabilities, or confidence | `docs/governance/JERRY_CONSTITUTION.md` |
| H-13 | Quality threshold >= 0.92 for C2+ deliverables | `.context/rules/quality-enforcement.md#quality-gate` |
| H-14 | Creator-critic-revision cycle, minimum 3 iterations | `.context/rules/quality-enforcement.md#quality-gate` |

### External Methodology Citations

| Citation Key | Full Reference |
|-------------|---------------|
| Nielsen, 1994a | Nielsen, J. (1994). "10 Usability Heuristics for User Interface Design." Nielsen Norman Group. |
| Nielsen, 1994b | Nielsen, J. (1994). "Severity Ratings for Usability Problems." Nielsen Norman Group. Severity scale: 0 (not a problem) to 4 (usability catastrophe). |
| Rodden, Hutchinson & Fu, 2010 | Rodden, K., Hutchinson, H., & Fu, X. (2010). "Measuring the User Experience on a Large Scale: User-Centered Metrics for Web Applications." Proceedings of CHI '10. |
| Gothelf & Seiden, 2021 | Gothelf, J. & Seiden, J. (2021). "Lean UX: Applying Lean Principles to Improve User Experience." 3rd ed. O'Reilly. |
| Fogg, 2020 | Fogg, B.J. (2020). "Tiny Habits: The Small Changes That Change Everything." Houghton Mifflin Harcourt. B=MAP model. |
| Ulwick, 2016 | Ulwick, A. (2016). "Jobs to Be Done: Theory to Practice." IDEA BITE PRESS. |
| Christensen et al., 2016 | Christensen, C.M., Hall, T., Dillon, K., & Duncan, D.S. (2016). "Competing Against Luck." Harper Business. |
| Moesta & Spiek, 2014 | Moesta, B. & Spiek, C. (2014). Jobs-to-be-Done switch interview methodology. The Re-Wired Group. |
| Berger et al., 1993 | Berger, C., Blauth, R., Boger, D., et al. (1993). "Kano's Methods for Understanding Customer-defined Quality." Center for Quality Management Journal, 2(4). Recommends >= 20 respondents for statistical Kano classification. |
| Kano et al., 1984 | Kano, N., Seraku, N., Takahashi, F., & Tsuji, S. (1984). "Attractive Quality and Must-be Quality." Journal of the Japanese Society for Quality Control, 14(2). |
| Frost, 2016 | Frost, B. (2016). "Atomic Design." Self-published. atomicdesign.bradfrost.com. |
| Knapp, Zeratsky & Kowitz, 2016 | Knapp, J., Zeratsky, J., & Kowitz, B. (2016). "Sprint: How to Solve Big Problems and Test New Ideas in Just Five Days." Simon & Schuster. |
| Microsoft, 2016 | Microsoft Inclusive Design Toolkit (2016). Persona Spectrum methodology. microsoft.com/design/inclusive. |
| W3C, 2023 | Web Content Accessibility Guidelines (WCAG) 2.2. W3C Recommendation. 2023-10-05. |
| Yang et al., 2020 | Yang, Q., Steinfeld, A., Rosé, C., & Zimmerman, J. (2020). "Re-examining Whether, Why, and How Human-AI Interaction Is Uniquely Difficult to Design." Proceedings of CHI '20. |

---

*Rule file: synthesis-validation.md*
*Parent skill: /user-experience*
*Parent SKILL.md: `skills/user-experience/SKILL.md`*
*Sibling rules: `skills/user-experience/rules/ux-routing-rules.md`, `skills/user-experience/rules/wave-progression.md`, `skills/user-experience/rules/mcp-coordination.md`, `skills/user-experience/rules/ci-checks.md`*
*Created: 2026-03-03*
*Updated: 2026-03-04*
*Revision: iter3 — adversarial findings from iter1 (0.879) and iter2 (0.889)*
*Status: COMPLETE*
