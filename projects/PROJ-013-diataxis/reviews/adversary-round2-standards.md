# Adversarial Review: diataxis-standards.md (Round 2)

**Strategy Sequence:** S-007 Constitutional Compliance -> S-004 Pre-Mortem Analysis -> S-012 FMEA -> S-010 Self-Refine
**Target Deliverable:** `skills/diataxis/rules/diataxis-standards.md`
**Round 1 Report:** `projects/PROJ-013-diataxis/reviews/adversary-round1-standards.md`
**Executed:** 2026-02-27
**Reviewer:** adv-executor
**Quality Threshold:** >= 0.95 weighted composite
**Criticality:** C3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Round 1 Remediation Verification](#round-1-remediation-verification) | Per-finding status of all Round 1 remediations |
| [S-007 Constitutional Compliance](#s-007-constitutional-compliance) | Principle-by-principle HARD rule review |
| [S-004 Pre-Mortem Analysis](#s-004-pre-mortem-analysis) | Prospective failure enumeration (post-remediation) |
| [S-012 FMEA Findings](#s-012-fmea-findings) | Updated component-level failure mode analysis |
| [S-010 Self-Refine Recommendations](#s-010-self-refine-recommendations) | Prioritized revision actions for Round 2 |
| [S-014 Quality Scoring](#s-014-quality-scoring) | 6-dimension weighted composite score |
| [Finding Summary Table](#finding-summary-table) | Consolidated Round 2 findings |

---

## Round 1 Remediation Verification

### Verification Matrix

| Round 1 ID | Finding | Status | Evidence |
|-----------|---------|--------|----------|
| SR-001 | H-03/HAP-04 internal contradiction | **OPEN** | No boundary definition between "real-world variations" and "edge cases" was added. H-03 (line 38-39) and HAP-04 (line 89) still exist in unresolved tension. |
| SR-002 | Detection heuristic false-positive handling missing | **OPEN** | No "False-Positive Handling Protocol" subsection added to Section 3. Writer Agent Self-Review Behavior (lines 130-133) still contains exactly 3 steps with no false-positive guidance. |
| SR-003 | Confidence thresholds uncalibrated | **FIXED** | Section 4 Confidence Derivation table (lines 147-152) now includes a "Rationale" column with explanations for each threshold level. 0.85 and 0.70 thresholds are now defined with operational reasoning. |
| SR-004 | E-01 "Zero numbered procedure lists" suppresses legitimate ordered concept enumeration | **OPEN** | Line 60: Pass Condition still reads "Zero numbered procedure lists" with no distinction between procedural and conceptual enumeration. |
| SR-005 | No escalation path when user acknowledges 3+ quadrant-mix flags | **OPEN** | Lines 130-133: Writer Agent Self-Review Behavior contains only 3 numbered steps. No repeated-acknowledgment escalation rule added. |
| SR-006 | Voice guidelines not scoped to Diataxis deliverables | **OPEN** | Section 5 preamble (lines 195-203) contains universal voice markers with no scoping note specifying guidelines apply to Diataxis deliverables only, not Jerry rule files or ADRs. |
| SR-007 | "2+ imperative verb sequences" heuristic is ambiguous | **PARTIALLY FIXED** | Line 120: "sequences" was not replaced with "imperative sentences," but examples "(e.g., 'Run X', 'Configure Y', 'Install Z')" were added. Core ambiguity in the term "sequences" persists; examples clarify intent but do not resolve the sentence-vs-phrase boundary question. |
| SR-008 | T-08 "Reliable reproduction" unverifiable by agent | **FIXED** | Line 30: Pass Condition now reads "Author has verified steps produce the documented result, or steps are flagged `[UNTESTED]`." The [UNTESTED] flag mechanism provides a verifiable pass condition for LLM agents. |
| SR-009 | R-01 "Mirrors code structure" not applicable to non-code reference docs | **OPEN** | Line 48: R-01 still reads "Documentation organization aligns with the machinery described" / "Section hierarchy matches code hierarchy" with no scope note for non-code reference documents. |
| SR-010 | Subsection navigation absent for 262-line file | **OPEN** | No `###`-level anchors or in-section navigation added. The file (now 262 lines) remains navigable only at `##` level. |
| SR-011 | H-01/H-07 overlapping pass conditions with no tiebreaker | **OPEN** | Lines 36 and 43: H-01 and H-07 still have no precedence statement or tiebreaker. |
| SR-012 | HAP-03 detection signal too vague | **OPEN** | Line 88: Detection signal still reads "Steps for things the reader already knows" without audience-level tie. |
| SR-013 | Decomposition sequence rationale absent | **OPEN** | Lines 188-189: Decomposition sequence still listed with no rationale note. |

### Remediation Summary

| Category | Count |
|----------|-------|
| FIXED | 2 (SR-003, SR-008) |
| PARTIALLY FIXED | 1 (SR-007) |
| OPEN | 10 (SR-001, SR-002, SR-004, SR-005, SR-006, SR-009, SR-010, SR-011, SR-012, SR-013) |

**Assessment:** 2 of 7 Priority 1 findings were addressed (SR-003, SR-008). Five Priority 1 findings remain open (SR-001, SR-002, SR-004, SR-005, SR-006). The two highest-RPN findings from Round 1 -- FM-011 (no false-positive handling, RPN 392) and FM-014 (uncalibrated confidence thresholds, RPN 392) -- saw one addressed (FM-014 via SR-003) and one unaddressed (FM-011 via SR-002).

---

## S-007 Constitutional Compliance

**Applicable principles (same as Round 1):**

| ID | Principle | Tier | Source |
|----|-----------|------|--------|
| H-23 | Navigation table REQUIRED for files >30 lines | HARD | markdown-navigation-standards.md |
| H-24 | Anchor links REQUIRED in navigation table | HARD | markdown-navigation-standards.md |
| NAV-002 | Navigation table placement | MEDIUM | markdown-navigation-standards.md |
| NAV-004 | All major `##` headings listed | MEDIUM | markdown-navigation-standards.md |

### Principle-by-Principle Evaluation

**H-23: Navigation table present (HARD)**
Status: COMPLIANT
Evidence: Lines 5-14 contain the "Document Sections" navigation table.

**H-24: Anchor links in navigation table (HARD)**
Status: COMPLIANT
Evidence: All five entries use `[Section N: ...]( #section-N-... )` anchor link syntax.

**NAV-002: Navigation table placement (MEDIUM)**
Status: COMPLIANT
Evidence: Navigation table at line 5, immediately after document heading and tagline.

**NAV-004: All major `##` headings listed (MEDIUM)**
Status: COMPLIANT
Evidence: All five primary content sections listed. No new `##` headings were added during remediation.

**NAV-004 advisory (`###` subsection coverage)**
Status: PARTIAL CONCERN (persists from Round 1)
Evidence: The 262-line file still has no `###`-level anchors. This advisory gap was acknowledged in Round 1 (SR-010) and remains unaddressed.

### S-007 Score

| Principle | Tier | Result |
|-----------|------|--------|
| H-23 | HARD | COMPLIANT |
| H-24 | HARD | COMPLIANT |
| NAV-002 | MEDIUM | COMPLIANT |
| NAV-004 (`##` headings) | MEDIUM | COMPLIANT |
| NAV-004 (`###` advisory) | MEDIUM | PARTIAL (persists from Round 1) |

**Constitutional Compliance Score: 0.97** (unchanged from Round 1 -- no new violations, no advisory gap resolved)

---

**CC-001 (Minor):** No HARD rule violations. One persistent MEDIUM advisory gap: subsection navigation coverage for a 262-line document. Unchanged from Round 1.

---

## S-004 Pre-Mortem Analysis

**Failure scenario:** It is 2026-08-27. `diataxis-standards.md` was partially remediated in Round 2 and deployed. Agents are experiencing the same failure modes as projected in Round 1 because the five highest-priority findings were not addressed.

### Failure Cause Inventory (Post-Remediation)

**PM-R01: H-03/HAP-04 boundary still absent (Persisting Assumption Failure)**
H-03 requires at minimum one variant; HAP-04 warns against edge-case completeness. Agents writing how-to guides will interpret H-03 as requiring edge-case coverage and simultaneously be penalized for it under HAP-04. The Round 1 recommendation to add a boundary definition ("a real-world variation is a conditional path during normal execution; an edge case is rare/exceptional") was not implemented.
- **Likelihood:** High (unchanged from Round 1)
- **Severity:** Major
- **Priority:** P1

**PM-R02: False-positive heuristics remain unguided (Persisting Process Failure)**
Section 3 still has no false-positive handling. A tutorial containing "Alternatively, if you are on macOS, run `brew install X`" will trigger the "Choice/alternative offerings in tutorials" heuristic (line 122) despite being a legitimate platform-conditional. This was the highest-RPN finding in Round 1 (FM-011, RPN 392) and was not addressed.
- **Likelihood:** High
- **Severity:** Major
- **Priority:** P1

**PM-R03: Voice scope conflict with existing Jerry style (Persisting External Failure)**
Section 5 still does not scope its guidelines to Diataxis deliverables. Agents writing Jerry rule files or ADRs following these voice guidelines may produce output inconsistent with established Jerry prose. The "discursive, contextual, knowledgeable colleague over coffee" explanation voice conflicts with the precise, terse style visible in `.context/rules/` files.
- **Likelihood:** Medium
- **Severity:** Major
- **Priority:** P1

**PM-R04: E-01 over-constraint in explanation writing (Persisting Assumption Failure)**
"Zero numbered procedure lists" in E-01 still blocks legitimate ordered concept enumeration ("Three reasons X matters: 1. A 2. B 3. C"). Agents writing explanation documents will either suppress valid enumeration patterns or fail E-01 unnecessarily. The amendment distinguishing procedural from conceptual numbered lists was not applied.
- **Likelihood:** Medium
- **Severity:** Major
- **Priority:** P1

**PM-R05: H-02 "3+ sentences" threshold introduces new blind spot (New Failure)**
The Round 2 remediation added "3+ sentences explaining rationale without action verbs" as the definition of "why digression" in H-02 (line 37). This is an improvement (quantitative threshold vs. none), but creates a new failure mode: a 2-sentence "why" digression is now implicitly permitted. In a tightly-stepped how-to guide, two sentences of rationale between steps constitute meaningful explanatory contamination. There is no guidance on whether 1-2 sentence digressions are acceptable or merely below the mandatory-flag threshold.
- **Likelihood:** Medium
- **Severity:** Minor
- **Priority:** P2

**PM-R06: Repeated acknowledgment escalation still absent (Persisting Process Failure)**
A user acknowledging 5 separate `[ACKNOWLEDGED]` quadrant-mix flags indicates fundamental misclassification, but Section 3 provides no recovery path. This was PM-006 in Round 1 and SR-005 in the revision plan, not addressed.
- **Likelihood:** Low (unchanged)
- **Severity:** Major
- **Priority:** P1

### Pre-Mortem Prioritization

| ID | Failure Cause | Likelihood | Severity | Priority | Round 1 Counterpart |
|----|---------------|------------|----------|----------|---------------------|
| PM-R01 | H-03/HAP-04 boundary absent | High | Major | P1 | SR-001 |
| PM-R02 | False-positive heuristics unguided | High | Major | P1 | SR-002 |
| PM-R03 | Voice scope conflict | Medium | Major | P1 | SR-006 |
| PM-R04 | E-01 ordered concept suppression | Medium | Major | P1 | SR-004 |
| PM-R05 | H-02 "3+ sentences" blind spot | Medium | Minor | P2 | NEW |
| PM-R06 | Repeated acknowledgment no recovery | Low | Major | P1 | SR-005 |

---

## S-012 FMEA Findings

### Element Decomposition (Same as Round 1)

| Element ID | Element | Remediation Delta |
|-----------|---------|-------------------|
| E-01 | Tutorial Quality Criteria (T-01 through T-08) | T-08 FIXED; T-03 unchanged |
| E-02 | How-To Guide Quality Criteria (H-01 through H-07) | H-02 partially FIXED; H-03/HAP-04, H-01/H-07 unchanged |
| E-03 | Reference Quality Criteria (R-01 through R-07) | R-02/R-03 FIXED; R-01 scope unchanged |
| E-04 | Explanation Quality Criteria (E-01 through E-07) | E-02 FIXED; E-01 ordered enumeration unchanged |
| E-05 | Tutorial Anti-Patterns (TAP-01 through TAP-05) | TAP-05 FIXED (downgraded, detection signals added) |
| E-06 | How-To Anti-Patterns (HAP-01 through HAP-05) | HAP-04/H-03 contradiction unchanged |
| E-07 | Reference Anti-Patterns (RAP-01 through RAP-05) | No change |
| E-08 | Explanation Anti-Patterns (EAP-01 through EAP-05) | No change |
| E-09 | Detection Heuristics (Section 3) | "Sequences" examples added; FM-011 false-positive handling unchanged |
| E-10 | Classification Decision Guide (Section 4) | FM-014 FIXED (rationale column added); FM-015, FM-016 unchanged |
| E-11 | Jerry Voice Guidelines (Section 5) | FM-017, FM-018 unchanged |

### Updated FMEA Failure Mode Analysis

**E-01: Tutorial Quality Criteria**

| FM-ID | Failure Mode | Effect | S | O | D | RPN | Status | Severity |
|-------|-------------|--------|---|---|---|-----|--------|----------|
| FM-001 | T-08 unverifiable by LLM agents | Criterion silently ignored | 6 | 8 | 7 | 336 | **CLOSED** -- [UNTESTED] flag now provides verifiable pass/fail path | Closed |
| FM-002 | T-03 "introduced earlier" ambiguous scope | Agents disagree on prerequisite scope | 5 | 5 | 6 | 150 | **OPEN** | Major |

**E-02: How-To Guide Quality Criteria**

| FM-ID | Failure Mode | Effect | S | O | D | RPN | Status | Severity |
|-------|-------------|--------|---|---|---|-----|--------|----------|
| FM-003 | H-02/H-03 conditional branch clarified | [H-02 clarification FIXED] | -- | -- | -- | -- | **CLOSED** | Closed |
| FM-004 | H-01/H-07 overlap -- no tiebreaker | Titles satisfying one but not both criteria are ambiguous | 5 | 4 | 5 | 100 | **OPEN** | Minor |
| FM-NEW01 | H-02 "3+ sentences" creates 2-sentence blind spot | 2-sentence why-digressions implicitly permitted; meaningful explanation contamination possible | 4 | 5 | 6 | 120 | **NEW** | Minor |

**E-03: Reference Quality Criteria**

| FM-ID | Failure Mode | Effect | S | O | D | RPN | Status | Severity |
|-------|-------------|--------|---|---|---|-----|--------|----------|
| FM-005 | R-01 not applicable to non-code reference | Inapplicable criterion applied to CLI/config docs | 4 | 6 | 5 | 120 | **OPEN** | Major |
| FM-006 | R-07 "public interface" undefined for document systems | Boundary unclear for entity vs. SKILL.md vs. CLI | 3 | 5 | 6 | 90 | **OPEN** | Minor |

**E-04: Explanation Quality Criteria**

| FM-ID | Failure Mode | Effect | S | O | D | RPN | Status | Severity |
|-------|-------------|--------|---|---|---|-----|--------|----------|
| FM-007 | E-01 "Zero numbered procedure lists" suppresses ordered concept lists | Legitimate enumeration prevented | 5 | 6 | 7 | 210 | **OPEN** | Major |
| FM-008 | E-02 minimum two cross-references may be excessive for short pieces | Fixed with "each with a sentence explaining" -- threshold remains but is now quality-gated | 3 | 5 | 5 | 75 | **PARTIALLY MITIGATED** (relationship explanation requirement raises quality floor) | Minor |

**E-05 through E-08: Anti-Pattern Tables**

| FM-ID | Failure Mode | Effect | S | O | D | RPN | Status | Severity |
|-------|-------------|--------|---|---|---|-----|--------|----------|
| FM-009 | Severity ratings undocumented | Mechanical severity without context causes false positives | 6 | 5 | 7 | 210 | **OPEN** | Major |
| FM-010 | HAP-04 vs. H-03 direct contradiction | H-03 requires variants; HAP-04 warns against edge cases; no boundary | 7 | 6 | 8 | 336 | **OPEN** | Major |

**E-09: Detection Heuristics**

| FM-ID | Failure Mode | Effect | S | O | D | RPN | Status | Severity |
|-------|-------------|--------|---|---|---|-----|--------|----------|
| FM-011 | No false-positive handling | Legitimate platform-conditionals flagged; user friction | 7 | 7 | 8 | 392 | **OPEN** | Major |
| FM-012 | "2+ imperative verb sequences" ambiguous | Examples added but "sequences" vs "sentences" boundary unresolved | 5 | 6 | 6 | 180 | **PARTIALLY MITIGATED** (RPN reduced 245 -> 180 via examples) | Major |
| FM-013 | "3+ consecutive sentences with no action verb" may flag legitimate context-setting | Opening context sentences in how-to trigger false positive | 4 | 6 | 6 | 144 | **OPEN** | Major |

**E-10: Classification Decision Guide**

| FM-ID | Failure Mode | Effect | S | O | D | RPN | Status | Severity |
|-------|-------------|--------|---|---|---|-----|--------|----------|
| FM-014 | Confidence thresholds uncalibrated | Agents treat values as authoritative; inconsistent classification | 7 | 7 | 8 | 392 | **CLOSED** -- Rationale column added with operational definitions | Closed |
| FM-015 | No feedback loop from repeated [ACKNOWLEDGED] | Misclassified documents not reclassified | 6 | 4 | 8 | 192 | **OPEN** | Major |
| FM-016 | Decomposition sequence prescriptive without rationale | Agents follow order without understanding why | 3 | 5 | 6 | 90 | **OPEN** | Minor |

**E-11: Jerry Voice Guidelines**

| FM-ID | Failure Mode | Effect | S | O | D | RPN | Status | Severity |
|-------|-------------|--------|---|---|---|-----|--------|----------|
| FM-017 | Voice not cross-referenced to Jerry rule file prose | Agents writing rule files diverge from established style | 7 | 5 | 8 | 280 | **OPEN** | Major |
| FM-018 | Voice Quality Gate references H-15 but specifies no HARD rule for voice compliance | No enforceable compliance path for voice violations | 5 | 6 | 7 | 210 | **OPEN** | Major |

### FMEA Summary (Round 2)

| Status | Count | Notes |
|--------|-------|-------|
| CLOSED | 3 (FM-001, FM-003, FM-014) | Fully remediated in Round 2 |
| PARTIALLY MITIGATED | 2 (FM-008, FM-012) | RPN reduced but not eliminated |
| OPEN | 13 | Unaddressed from Round 1 |
| NEW | 1 (FM-NEW01) | Introduced by Round 2 remediation |

**Highest-risk open elements (unchanged from Round 1):**
- E-09 FM-011: RPN 392 (no false-positive handling)
- E-05/E-06 FM-010: RPN 336 (HAP-04/H-03 contradiction)
- E-04 FM-007: RPN 210 (E-01 ordered concept suppression)
- E-11 FM-017: RPN 280 (voice not scoped)

---

## S-010 Self-Refine Recommendations

### Findings Table (Round 2 -- All Strategies Consolidated)

Round 2 produces findings in three categories: (A) persistent unaddressed Round 1 findings that remain as-is, (B) partially mitigated findings with residual risk, and (C) new findings introduced by Round 2 remediation.

#### Category A: Persistent Critical Findings (Unaddressed from Round 1)

| ID | Finding | Severity | Evidence | Dimension |
|----|---------|----------|----------|-----------|
| SR2-001 | H-03/HAP-04 internal contradiction (PERSISTS) | Major | H-03 line 38-39 requires "at minimum one 'If you need X, do Y' variant"; HAP-04 line 89 warns against "Documenting every edge case." No boundary definition added. FM-010, RPN 336. | Internal Consistency |
| SR2-002 | Detection heuristic false-positive handling missing (PERSISTS) | Major | Section 3 lines 114-133 has no false-positive protocol. "Alternatively" on line 122 fires on legitimate macOS/Windows conditionals in tutorials. FM-011, RPN 392 -- highest RPN in document. | Actionability |
| SR2-003 | Voice guidelines not scoped to Diataxis deliverables (PERSISTS) | Major | Section 5 lines 195-253 contains no statement that these guidelines apply only to confirmed Diataxis deliverables, not Jerry rule files or ADRs. FM-017, RPN 280. | Internal Consistency |
| SR2-004 | E-01 "Zero numbered procedure lists" suppresses ordered concept enumeration (PERSISTS) | Major | Line 60: Pass Condition still "Zero numbered procedure lists." Ordered concept lists ("Three reasons X matters: 1. A 2. B 3. C") are legitimate explanation content but fail this criterion. FM-007, RPN 210. | Completeness |
| SR2-005 | No escalation path for repeated [ACKNOWLEDGED] quadrant-mix flags (PERSISTS) | Major | Lines 130-133: Writer Agent Self-Review Behavior has 3 steps. Step (d) for reclassification escalation not added. FM-015, RPN 192. | Completeness |
| SR2-006 | "2+ imperative verb sequences" -- "sequences" still undefined (PERSISTS, partially mitigated) | Major | Line 120: "sequences" not replaced with "imperative sentences." Examples added mitigate RPN from 245 to 180, but sentence-vs-phrase boundary is unresolved. FM-012. | Methodological Rigor |
| SR2-007 | FM-013: "3+ consecutive sentences with no action verb" may flag legitimate context-setting (PERSISTS) | Major | Line 125: Opening context sentence "This guide assumes your service is running." has no action verb and would trigger this heuristic in isolation. Not addressed from Round 1. | Actionability |

#### Category B: Residual Minor Findings (Partially Fixed or Persistent Minor)

| ID | Finding | Severity | Evidence | Dimension |
|----|---------|----------|----------|-----------|
| SR2-008 | T-03 "introduced earlier" scope ambiguous | Minor | Line 25: "No step requires knowledge not introduced earlier in the tutorial." Scope of "earlier" undefined -- does broader Jerry documentation count? Does the prerequisites block count? FM-002, RPN 150. | Methodological Rigor |
| SR2-009 | R-01 "Mirrors code structure" inapplicable to non-code reference (PERSISTS) | Minor | Line 48: Pass Condition "Section hierarchy matches code hierarchy" does not apply to CLI or configuration reference without underlying code structure. FM-005, RPN 120. | Completeness |
| SR2-010 | H-01/H-07 overlapping pass conditions with no tiebreaker (PERSISTS) | Minor | Lines 36 and 43: H-01 "Title begins with 'How to'" and H-07 "Title describes user goal" can conflict. No precedence rule. FM-004, RPN 100. | Internal Consistency |
| SR2-011 | Subsection navigation absent for 262-line file (PERSISTS) | Minor | Navigation table covers `##` headings only. 262-line file with 4 per-quadrant subsections per section would benefit from `###`-level anchors. CC-001. | Actionability |
| SR2-012 | HAP-03 detection signal untied to audience competence (PERSISTS) | Minor | Line 88: "Steps for things the reader already knows" -- no audience reference makes this subjective. | Actionability |
| SR2-013 | Decomposition sequence rationale absent (PERSISTS) | Minor | Lines 188-189: "Tutorial first, then How-To, then Reference, then Explanation" stated without rationale. FM-016, RPN 90. | Traceability |
| SR2-014 | FM-018: Voice Quality Gate lacks HARD rule reference | Minor | Lines 257-262: Voice Quality Gate section references H-15 self-review but does not specify which H-rule governs voice compliance. Agents cannot enforce voice as a HARD constraint. | Traceability |

#### Category C: New Findings (Introduced by Round 2 Remediation)

| ID | Finding | Severity | Evidence | Dimension |
|----|---------|----------|----------|-----------|
| SR2-015 | H-02 "3+ sentences" threshold creates 2-sentence blind spot | Minor | Line 37: "Zero 'why' digressions (3+ sentences explaining rationale without action verbs)." This improvement introduces a new gap: 1-2 sentence rationale digressions between steps are now implicitly permitted. In tight how-to guides, 2-sentence explanations represent meaningful explanatory contamination. FM-NEW01, RPN 120. | Completeness |

### Prioritized Revision Plan (Round 2)

**Priority 1 -- Must fix before deployment (carry-forward from Round 1):**

**SR2-001 -- H-03/HAP-04 Boundary Definition (HIGHEST PRIORITY):**
Add a disambiguating note after H-03 and after HAP-04 that defines the boundary:
> "A real-world variation is a conditional path the reader may encounter during normal task execution (e.g., OS-specific commands, optional authentication steps). An edge case is a rare or exceptional condition that the main task path never requires. H-03 requires at minimum one real-world variation. HAP-04 prohibits exhaustive cataloguing of edge cases. These criteria are complementary: one conditional branch satisfies H-03 without triggering HAP-04."

**SR2-002 -- False-Positive Handling Protocol (HIGHEST PRIORITY by RPN):**
Add a new subsection after the heuristic table in Section 3:

> **False-Positive Handling Protocol**
> A detected heuristic signal is a false positive when the flagged construct is contextually required by the primary quadrant. Override conditions:
> - "Alternatively" in a tutorial step introducing a platform-specific path (macOS/Windows/Linux) is a legitimate OS conditional, NOT how-to contamination. Suppress flag.
> - An imperative verb in explanation is a false positive if it appears in a quoted command, code block, or example (not running prose). Suppress flag.
> - "3+ consecutive sentences without action verb" in how-to is a false positive if the sentences appear as the guide's opening context (first paragraph only). Apply the heuristic starting from the second paragraph.
> When a signal fires and context clearly belongs to the primary quadrant: suppress the flag, do not ask user. When signal context is ambiguous: flag with `[QUADRANT-MIX: ...]` per the existing protocol.

**SR2-003 -- Voice Guideline Scoping:**
Add to the Section 5 opening block (before "Universal Jerry Voice Markers"):
> "**Scope:** These guidelines govern Diataxis documentation output (tutorials, how-to guides, reference documents, explanation documents). For Jerry internal documents (rule files, ADRs, SKILL.md, CLAUDE.md), the existing Jerry rule file prose style takes precedence. Apply Section 5 guidelines only when the deliverable's quadrant classification has been confirmed."

**SR2-004 -- E-01 Ordered Concept Lists:**
Replace E-01 pass condition:

Current: "Zero numbered procedure lists"

Replace with: "Zero numbered procedure lists (numbered lists where each item is an action the reader performs in sequence). Numbered concept lists (numbered lists enumerating reasons, principles, or conceptual items) are permitted."

**SR2-005 -- Repeated Acknowledgment Escalation:**
Add step (d) to Writer Agent Self-Review Behavior (Section 3):
> "(d) If the document accumulates 3 or more `[ACKNOWLEDGED]` markers, halt and re-run the two-axis test with the full document content. If the new classification differs from the original, report the reclassification to the user before continuing."

**SR2-006 -- Imperative Verb Sequences Definition:**
Replace "2+ imperative verb sequences (e.g., 'Run X', 'Configure Y', 'Install Z') in a paragraph" with:
> "2+ imperative sentences (sentences beginning with an imperative verb form: 'Run', 'Configure', 'Set', 'Add', 'Create', 'Delete') within a single paragraph of explanation output"

**SR2-007 -- Context-Setting Sentence Exemption:**
Append to the "Explanation blocks in how-to" heuristic row:
> "Exception: first-paragraph context-setting sentences ('This guide assumes your service is running.') are exempt from this heuristic. Apply starting from the second paragraph."

**Priority 2 -- Address in next iteration:**

**SR2-008 -- T-03 "Introduced Earlier" Scope:**
Add a scope note to T-03: "'Earlier in the tutorial' means content appearing before the current step within this document. External knowledge documented in a referenced prerequisites block or linked document is excluded from this criterion."

**SR2-009 -- R-01 Non-Code Reference Scope:**
Add a note to R-01: "For non-code reference documents (CLI reference, configuration reference), interpret 'machinery described' as the command hierarchy, configuration schema, or entity model."

**SR2-013 -- Decomposition Sequence Rationale:**
Add: "(Sequence follows Diataxis learning progression: hands-on experience first, task application second, lookup reference third, conceptual deepening last.)"

**SR2-015 -- H-02 Threshold Clarification:**
Add a clarifying note to H-02 pass condition: "1-2 sentence digressions are noted but below mandatory-flag threshold; 3+ sentences require flagging. Use judgment for 1-2 sentence cases when they substantially interrupt action flow."

**Priority 3 -- Quality improvements:**

**SR2-010 -- H-01/H-07 Tiebreaker:** Add: "If H-01 and H-07 conflict, H-07 takes precedence. H-01 is a recommended pattern, not an absolute requirement."

**SR2-011 -- Subsection Navigation:** Consider adding `###`-level navigation within each section, or a quick-reference table mapping criteria IDs to sections.

**SR2-012 -- HAP-03 Audience Tie:** Replace "Steps for things the reader already knows" with "Steps that a competent practitioner at the guide's stated audience level already knows."

**SR2-014 -- FM-018 Voice Compliance Rule:** If voice compliance is intended to be enforceable, specify which H-rule governs it. If not HARD, state "MEDIUM standard." Currently the Voice Quality Gate creates ambiguous compliance expectations.

---

## S-014 Quality Scoring

### Dimension-Level Assessment

**1. Completeness (weight: 0.20)**
- Tutorial, How-To, Reference, Explanation criteria: comprehensive, 8+7+7+7 = 29 criteria covering all major quality dimensions per quadrant.
- Anti-patterns: 5 per quadrant, 20 total.
- Detection heuristics: 7 signals.
- Classification guide: 2-axis test + 5 borderline cases + multi-quadrant decomposition.
- Voice guidelines: universal + 4 per-quadrant.
- **Gaps:** E-01 over-restricts explanation enumeration (SR2-004), HAP-04/H-03 contradiction creates an unsatisfiable specification for a common case (SR2-001), no false-positive handling creates silent failure mode (SR2-002). These are three significant completeness gaps affecting core functionality.
- **Dimension Score: 0.77**

**2. Internal Consistency (weight: 0.20)**
- R-02/R-03 distinction: FIXED (clearly separate concerns now).
- H-02 clarification: FIXED (conditionals are action content).
- H-03/HAP-04 contradiction: OPEN -- direct conflict between a quality criterion and an anti-pattern with no resolution. This is the most significant internal consistency issue.
- H-01/H-07 tension: OPEN (minor).
- Voice guidelines unscoped: creates conflict with Jerry rule file prose standard (external consistency issue).
- **Dimension Score: 0.78**

**3. Methodological Rigor (weight: 0.20)**
- Confidence threshold rationale: FIXED -- derivation column added with operational definitions. Significant improvement.
- Detection heuristics: "sequences" partially clarified by examples; core definitional issue persists.
- "3+ sentences" threshold for H-02: new quantitative improvement.
- False-positive handling: absent for the highest-frequency detection scenario.
- T-03 scope: undefined boundary for "introduced earlier."
- **Dimension Score: 0.82**

**4. Evidence Quality (weight: 0.15)**
- Quality criteria: all have Test + Pass Condition columns providing evidence basis.
- Anti-pattern detection signals: specific enough for pattern matching.
- Borderline cases: 5 concrete examples with reasoning chains.
- Before/after voice examples: concrete and illustrative.
- T-08 [UNTESTED] fix: well-targeted.
- E-02 relationship explanation requirement: improved from "count only" to "count + explanation."
- **Dimension Score: 0.90**

**5. Actionability (weight: 0.15)**
- Per-criterion test and pass conditions: highly actionable.
- Per-anti-pattern detection signals: mostly specific; HAP-03 is vague.
- Detection heuristics: actionable flag + tag protocol. False-positive handling gap reduces actionability for edge cases.
- Self-review behavior: 3-step protocol is clear but missing repeated-acknowledgment escalation.
- Voice guidelines: transformation examples are highly actionable.
- **Dimension Score: 0.83**

**6. Traceability (weight: 0.10)**
- Criterion IDs (T-01 through E-07): stable, referenceable.
- Anti-pattern IDs (TAP-01 through EAP-05): stable, referenceable.
- FM IDs from Round 1: consistent with FMEA output.
- Confidence threshold rationale: FIXED -- derivation now present.
- Severity rating derivation: still absent for anti-pattern tables.
- Decomposition sequence: stated without rationale.
- Voice Quality Gate: references H-15 but does not identify governing HARD rule for voice compliance.
- **Dimension Score: 0.82**

### Weighted Composite Score

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|---------|
| Completeness | 0.20 | 0.77 | 0.154 |
| Internal Consistency | 0.20 | 0.78 | 0.156 |
| Methodological Rigor | 0.20 | 0.82 | 0.164 |
| Evidence Quality | 0.15 | 0.90 | 0.135 |
| Actionability | 0.15 | 0.83 | 0.125 |
| Traceability | 0.10 | 0.82 | 0.082 |
| **Total** | **1.00** | | **0.816** |

**Round 2 Composite Score: 0.816**

### Score Interpretation

| Band | Score Range | This Deliverable |
|------|------------|------------------|
| PASS | >= 0.95 | Not reached |
| REVISE | 0.85 - 0.94 | Not reached |
| REJECTED | < 0.85 | **0.816 -- REJECTED** |

**Score vs. Round 1 Estimate:**

Round 1 post-revision estimate was >= 0.95 if all 7 Priority 1 findings were addressed. Only 2 of 7 were addressed (SR-003, SR-008). The score reflects this: addressing 2/7 Priority 1 findings yielded a modest improvement over the pre-revision estimate (0.82 was estimated pre-revision in Round 1), but insufficient to clear the 0.95 threshold.

**Delta from Round 1:** Round 1 estimated pre-revision quality at 0.82. Round 2 measures 0.816. The small positive delta reflects SR-003 (confidence threshold rationale) and SR-008 (T-08 [UNTESTED] fix) along with the R-02/R-03, H-02, E-02, and TAP-05 fixes noted in the context description. However, five Priority 1 findings remain unaddressed, preventing threshold crossing.

---

## Finding Summary Table

### Round 2 New and Persisting Findings

| ID | Severity | Finding | Location | Persisting From |
|----|----------|---------|----------|-----------------|
| SR2-001 | **Major** | H-03/HAP-04 contradiction: no boundary between "real-world variation" and "edge case" | Section 1 (H-03), Section 2 (HAP-04) | SR-001 |
| SR2-002 | **Major** | False-positive handling absent from Section 3 heuristics (highest-RPN unaddressed finding) | Section 3, all heuristic rows | SR-002 |
| SR2-003 | **Major** | Voice guidelines not scoped to Diataxis deliverables; conflicts with Jerry rule file prose style | Section 5, preamble | SR-006 |
| SR2-004 | **Major** | E-01 "Zero numbered procedure lists" blocks legitimate ordered concept enumeration in explanations | Section 1, E-01 | SR-004 |
| SR2-005 | **Major** | No reclassification escalation when user acknowledges 3+ quadrant-mix flags | Section 3, Writer Agent Self-Review Behavior | SR-005 |
| SR2-006 | **Major** | "2+ imperative verb sequences" -- "sequences" undefined (sentence vs. phrase boundary unresolved) | Section 3, detection heuristics row 1 | SR-007 (partial) |
| SR2-007 | **Major** | "3+ consecutive sentences with no action verb" heuristic fires on legitimate how-to context-setting | Section 3, explanation blocks heuristic | FM-013 |
| SR2-008 | Minor | T-03 "introduced earlier" scope undefined (prerequisites block, external docs?) | Section 1, T-03 | FM-002 |
| SR2-009 | Minor | R-01 "Mirrors code structure" inapplicable to CLI or configuration reference without code | Section 1, R-01 | SR-009 |
| SR2-010 | Minor | H-01/H-07 overlapping pass conditions with no precedence rule | Section 1, H-01 and H-07 | SR-011 |
| SR2-011 | Minor | No `###`-level subsection navigation in 262-line document | Document-wide | SR-010 |
| SR2-012 | Minor | HAP-03 detection signal untied to stated audience competence level | Section 2, HAP-03 | SR-012 |
| SR2-013 | Minor | Decomposition sequence (Tutorial -> How-To -> Reference -> Explanation) stated without rationale | Section 4, Multi-Quadrant Decomposition | SR-013 |
| SR2-014 | Minor | Voice Quality Gate references H-15 but names no HARD rule for voice compliance enforcement | Section 5, Voice Quality Gate | FM-018 |
| SR2-015 | Minor | H-02 "3+ sentences" threshold creates implicit permission for 2-sentence why-digressions | Section 1, H-02 | NEW |

### Fixed in Round 2

| Former ID | Finding | Fix Applied |
|-----------|---------|-------------|
| SR-003 | Confidence thresholds uncalibrated | Rationale column added to Confidence Derivation table |
| SR-008 | T-08 "Reliable reproduction" unverifiable | [UNTESTED] flag mechanism added to pass condition |
| Round 1 context: R-02/R-03 | "Wholly authoritative" vs "complete specification" conflated | Now clearly distinct criteria |
| Round 1 context: H-02/H-03 | Conditional branches not classified as action content | H-02 clarification added |
| Round 1 context: E-02 | Requires relationship explanation | Pass condition now requires "a sentence explaining how topics relate" |
| Round 1 context: TAP-05 | Was Critical, vague detection | Downgraded to Major, concrete detection signals added |

---

## Execution Statistics

- **Total Round 2 Findings:** 15 (7 Major, 8 Minor)
- **Critical:** 0
- **Major:** 7 (SR2-001 through SR2-007)
- **Minor:** 8 (SR2-008 through SR2-015)
- **Round 1 Findings Closed:** 6 (SR-003, SR-008 from revision + R-02/R-03, H-02/H-03, E-02, TAP-05 from context)
- **Round 1 Findings Persisting:** 10
- **New Findings (Round 2):** 1 (SR2-015 -- introduced by H-02 remediation)
- **Protocol Steps Completed:** 4 of 4 (S-007, S-004, S-012, S-010)

**Constitutional Compliance Score (S-007):** 0.97 (unchanged -- no HARD violations)
**Round 2 Composite Score (S-014):** 0.816
**Quality Gate Result:** REJECTED (threshold 0.95 not met)

**Recommended Action:** REVISE -- Round 3 required. The 7 Priority 1 findings listed in the SR2 revision plan are all carry-forwards from Round 1. All 7 must be addressed to clear the 0.95 threshold. The two highest-impact findings are SR2-001 (H-03/HAP-04 contradiction, affects core how-to guide writing accuracy) and SR2-002 (false-positive handling absent, affects trust and usability of the detection heuristics, RPN 392). These two alone account for a substantial portion of the Completeness (0.77), Internal Consistency (0.78), and Actionability (0.83) score shortfalls. Addressing all 7 Priority 1 findings is projected to raise the composite score to >= 0.95.
