# Adversarial Review: diataxis-standards.md (Round 3)

**Strategy Sequence:** S-007 Constitutional Compliance -> S-004 Pre-Mortem Analysis -> S-012 FMEA -> S-010 Self-Refine
**Target Deliverable:** `skills/diataxis/rules/diataxis-standards.md`
**Round 2 Report:** `projects/PROJ-013-diataxis/reviews/adversary-round2-standards.md`
**Executed:** 2026-02-27
**Reviewer:** adv-executor
**Quality Threshold:** >= 0.95 weighted composite
**Criticality:** C3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Round 2 Remediation Verification](#round-2-remediation-verification) | Per-finding status of all Round 2 Priority 1 and Priority 2/3 remediations |
| [S-007 Constitutional Compliance](#s-007-constitutional-compliance) | Principle-by-principle HARD rule review |
| [S-004 Pre-Mortem Analysis](#s-004-pre-mortem-analysis) | Prospective failure enumeration (post-remediation) |
| [S-012 FMEA Findings](#s-012-fmea-findings) | Updated component-level failure mode analysis with new RPNs |
| [S-010 Self-Refine Recommendations](#s-010-self-refine-recommendations) | Prioritized revision actions for Round 3 |
| [S-014 Quality Scoring](#s-014-quality-scoring) | 6-dimension weighted composite score |
| [Finding Summary Table](#finding-summary-table) | Consolidated Round 3 findings |

---

## Round 2 Remediation Verification

### Priority 1 Findings (7 items — all REQUIRED)

| R2 ID | Finding | Status | Evidence |
|-------|---------|--------|----------|
| SR2-001 | H-03/HAP-04 contradiction: no boundary between "real-world variation" and "edge case" | **FIXED** | Line 38 (H-03): "A real-world variation is a conditional path during normal task execution... Edge cases (rare/exceptional conditions) are out of scope -- see HAP-04. One conditional branch satisfies H-03 without triggering HAP-04." Line 89 (HAP-04): "Edge cases are rare/exceptional conditions the main task path never requires. This is complementary to H-03 -- one real-world variation satisfies H-03 without triggering HAP-04." Both sides of the boundary are now defined. |
| SR2-002 | False-positive handling absent from Section 3 heuristics | **FIXED** | Lines 128-135: New "False-Positive Handling Protocol" subsection with three named override conditions. Writer Agent Self-Review Behavior updated (step 3, line 142) to apply protocol before flagging. |
| SR2-003 | Voice guidelines not scoped to Diataxis deliverables | **FIXED** | Lines 206: "Scope: These guidelines govern Diataxis documentation output (tutorials, how-to guides, reference documents, explanation documents). For Jerry internal documents (rule files, ADRs, SKILL.md, CLAUDE.md), the existing Jerry rule file prose style takes precedence. Apply Section 5 guidelines only when the deliverable's quadrant classification has been confirmed." |
| SR2-004 | E-01 "Zero numbered procedure lists" blocks ordered concept enumeration | **FIXED** | Line 60: Pass Condition now reads "Zero numbered procedure lists (numbered lists where each item is an action the reader performs in sequence). Numbered concept lists enumerating reasons, principles, or conceptual items are permitted." |
| SR2-005 | No reclassification escalation when user acknowledges 3+ quadrant-mix flags | **FIXED** | Line 143: Step 4 added: "If the document accumulates 3 or more `[ACKNOWLEDGED]` markers, halt and re-run the two-axis test with the full document content. If the new classification differs from the original, report the reclassification to the user before continuing." |
| SR2-006 | "2+ imperative verb sequences" — "sequences" undefined | **FIXED** | Line 120: Replaced with "2+ imperative sentences (sentences beginning with an imperative verb form: 'Run', 'Configure', 'Set', 'Add', 'Create', 'Delete') within a single paragraph of explanation output." Sentence boundary is now explicit. |
| SR2-007 | "3+ consecutive sentences with no action verb" heuristic fires on how-to context-setting | **FIXED** | Line 125: "Exception: first-paragraph context-setting sentences ('This guide assumes your service is running.') are exempt. Apply this heuristic starting from the second paragraph." |

**Priority 1 Verdict: 7 of 7 FIXED.** All Round 2 Priority 1 findings have been addressed.

### Priority 2 Findings (4 items)

| R2 ID | Finding | Status | Evidence |
|-------|---------|--------|----------|
| SR2-008 | T-03 "introduced earlier" scope ambiguous | **FIXED** | Line 25: "'Earlier' means content appearing before the current step within this document. External knowledge in a referenced prerequisites block or linked document is excluded." |
| SR2-009 | R-01 "Mirrors code structure" inapplicable to non-code reference | **FIXED** | Line 48: "For non-code reference (CLI, configuration, entities), interpret as command hierarchy, config schema, or entity model." |
| SR2-013 | Decomposition sequence stated without rationale | **FIXED** | Line 199: "(Sequence follows Diataxis learning progression: hands-on experience first, task application second, lookup reference third, conceptual deepening last.)" |
| SR2-015 | H-02 "3+ sentences" creates 2-sentence blind spot | **PARTIALLY FIXED** | Line 37 note: "1-2 sentence digressions are below mandatory-flag threshold; use judgment when they substantially interrupt action flow." The blind spot is acknowledged but "use judgment" remains an unverifiable instruction for automated agents. Residual minor risk persists. |

### Priority 3 Findings (5 items)

| R2 ID | Finding | Status | Evidence |
|-------|---------|--------|----------|
| SR2-010 | H-01/H-07 overlapping pass conditions with no tiebreaker | **FIXED** | Line 36: "Note: If H-01 and H-07 conflict, H-07 (user goal framing) takes precedence. H-01 is a recommended pattern." |
| SR2-011 | No `###`-level subsection navigation | **OPEN** | File is now 275 lines. Navigation table still covers `##` headings only. No `###`-level anchors added. |
| SR2-012 | HAP-03 detection signal untied to audience competence | **FIXED** | Line 88: "Steps that a competent practitioner at the guide's stated audience level already knows." |
| SR2-014 | Voice Quality Gate references H-15 but names no HARD rule for voice compliance | **OPEN** | Lines 269-274: Voice Quality Gate section still references H-15 self-review but does not specify which HARD rule governs voice compliance. No MEDIUM/SOFT classification stated. |

### Remediation Summary

| Category | Count | IDs |
|----------|-------|-----|
| FIXED (Priority 1) | 7 | SR2-001 through SR2-007 |
| FIXED (Priority 2/3) | 7 | SR2-008, SR2-009, SR2-010, SR2-012, SR2-013 + R2 context fixes |
| PARTIALLY FIXED | 1 | SR2-015 |
| OPEN | 2 | SR2-011, SR2-014 |

**Assessment:** The Round 2 remediation was substantially complete. All 7 Priority 1 findings are resolved. However, the remediation effort introduced 4 new findings (2 Major, 2 Minor) through specification interactions that were not present in the pre-remediation document. These new issues prevent the deliverable from clearing the 0.95 threshold.

---

## S-007 Constitutional Compliance

**Applicable principles:**

| ID | Principle | Tier | Source |
|----|-----------|------|--------|
| H-23 | Navigation table REQUIRED for files >30 lines | HARD | markdown-navigation-standards.md |
| H-24 | Anchor links REQUIRED in navigation table | HARD | markdown-navigation-standards.md |
| NAV-002 | Navigation table placement | MEDIUM | markdown-navigation-standards.md |
| NAV-004 | All major `##` headings listed | MEDIUM | markdown-navigation-standards.md |

### Principle-by-Principle Evaluation

**H-23: Navigation table present (HARD)**
Status: COMPLIANT
Evidence: Lines 5-13 contain the "Document Sections" navigation table with five entries.

**H-24: Anchor links in navigation table (HARD)**
Status: COMPLIANT
Evidence: All five navigation table entries use `[Section N: ...]( #section-N-... )` anchor link syntax with valid target anchors.

**NAV-002: Navigation table placement (MEDIUM)**
Status: COMPLIANT
Evidence: Navigation table at lines 5-13, immediately after the document title and tagline.

**NAV-004: All major `##` headings listed (MEDIUM)**
Status: COMPLIANT
Evidence: All five `##` primary content sections are listed in the navigation table. No new `##` headings were added during Round 2 remediation.

**NAV-004 advisory (`###` subsection coverage)**
Status: PARTIAL CONCERN (persists from Rounds 1 and 2)
Evidence: The 275-line file contains 4 named subsections per section (Tutorial/How-To/Reference/Explanation criteria, anti-patterns, detection heuristics sub-components, etc.) with no `###`-level navigation anchors. Readers cannot jump directly to, e.g., "How-To Guide Quality Criteria" without scrolling.

### S-007 Score

| Principle | Tier | Result |
|-----------|------|--------|
| H-23 | HARD | COMPLIANT |
| H-24 | HARD | COMPLIANT |
| NAV-002 | MEDIUM | COMPLIANT |
| NAV-004 (`##` headings) | MEDIUM | COMPLIANT |
| NAV-004 (`###` advisory) | MEDIUM | PARTIAL (persists from Round 1) |

**Constitutional Compliance Score: 0.97** (unchanged — no HARD violations; one persistent MEDIUM advisory gap unaddressed across three rounds)

---

**CC-001 (Minor):** No HARD rule violations. Persistent MEDIUM advisory gap: subsection navigation coverage for a 275-line document that has grown through two rounds of remediation. Now entering its third round open.

---

## S-004 Pre-Mortem Analysis

**Failure scenario:** It is 2026-08-27. `diataxis-standards.md` was substantially remediated in Round 3 and deployed. Writer agents are producing tutorials with "Alternatively, on macOS..." constructions that simultaneously pass the False-Positive Handling Protocol and fail the T-04 quality criterion. Agents are confused and producing inconsistent tutorial quality reports.

### Failure Cause Inventory (Post-Remediation)

**PM3-001: T-04 and False-Positive Protocol create contradictory tutorial authorship instructions (NEW)**
T-04 (line 26) states the pass condition for tutorials is "Zero 'alternatively' or 'you could also' constructions." The False-Positive Handling Protocol (line 131) states that "Alternatively" introducing a platform-specific path is a legitimate OS conditional and the flag should be suppressed. A tutorial writer adding "Alternatively, on macOS, run `brew install X`" will:
- Fail T-04 (zero alternatives required — the construction is present)
- Be told by the False-Positive Protocol to suppress the flag

The document provides no resolution for this conflict. A quality reviewer applying T-04 would reject the document; the False-Positive Protocol says the detection signal is a false positive. This creates irreducibly inconsistent evaluation outcomes.
- **Likelihood:** High — OS-conditional tutorials are the most common tutorial pattern. Nearly every software tutorial has a macOS/Windows/Linux path split.
- **Severity:** Major — the most fundamental tutorial quality criterion (T-04) is now in direct conflict with the False-Positive Protocol added to fix the previous highest-RPN finding (FM-011).
- **Priority:** P1

**PM3-002: Case 5 enumeration order contradicts canonical decomposition sequence (NEW)**
The Multi-Quadrant Decomposition rule (line 199) specifies: "Tutorial first (if present), then How-To Guide, then Reference, then Explanation." Borderline Case 5 (lines 191-193) lists the recommended decomposition as: "1. Reference, 2. Explanation, 3. How-To Guide." This is a different sequence. A writer agent reading Case 5 as a template would produce decomposition recommendations in the Reference-Explanation-How-To order, contradicting the canonical Tutorial-How-To-Reference-Explanation sequence.
- **Likelihood:** Medium — Case 5 is likely to be used as a template for SKILL.md-type documents, which are common in the Jerry ecosystem.
- **Severity:** Minor — wrong document ordering is recoverable; it does not cause functional failure.
- **Priority:** P2

**PM3-003: EAP-01 fires on one imperative sentence; heuristic requires two (NEW)**
EAP-01 (line 106) lists "Imperative verbs ('Run this', 'Configure that')" as a detection signal with no threshold — any instance triggers the anti-pattern flag. The detection heuristic (line 120) requires 2+ imperative sentences within a single paragraph before firing. An explanation document containing exactly one sentence starting "Run `jerry session start`" will:
- Trigger EAP-01 (no threshold — any imperative verb)
- Not trigger the heuristic (below 2-sentence paragraph threshold)

Agents applying EAP-01 will flag; agents applying the heuristic table will not. No guidance specifies which to apply when they conflict.
- **Likelihood:** Medium — single-imperative-sentence contamination is a common explanation anti-pattern.
- **Severity:** Major — contradictory detection instructions produce inconsistent quality enforcement.
- **Priority:** P1

**PM3-004: Writer Agent Self-Review step ordering inverts false-positive check (NEW)**
Writer Agent Self-Review Behavior (lines 139-143) lists:
- Step 2: "When a mixing signal is detected: (a) flag with appropriate `[QUADRANT-MIX: ...]` tag..."
- Step 3: "Apply the False-Positive Handling Protocol above before flagging -- suppress signals that match an override condition"

A literal reading of this numbered list instructs agents to flag first (step 2) and then check for false positives (step 3). The intended order is the reverse: check false-positives before flagging. The "before flagging" parenthetical in step 3 conflicts with the numbered list sequence. An agent reading the list sequentially will flag first, then awkwardly retract the flag after step 3.
- **Likelihood:** Medium — numbered lists imply sequential execution. Agents following step-by-step protocols read them in order.
- **Severity:** Minor — the error is recoverable (the agent retracts the incorrect flag), but creates unnecessary user confusion and friction.
- **Priority:** P2

**PM3-005: SR2-015 "use judgment" instruction remains unverifiable for automated agents (PERSISTING, PARTIALLY FIXED)**
H-02 note (line 37): "1-2 sentence digressions are below mandatory-flag threshold; use judgment when they substantially interrupt action flow." "Use judgment" is not an actionable instruction for an automated writer agent. Agents cannot reason about "substantially interrupt" without a quantitative or structural heuristic. A 1-sentence digression before a critical step may substantially interrupt flow; a 2-sentence digression in a 50-step guide may not. The note clarifies the threshold boundary but does not provide a decision rule for borderline cases.
- **Likelihood:** Low (2-sentence digressions are less common than the 3+ case)
- **Severity:** Minor
- **Priority:** P3

### Pre-Mortem Prioritization

| ID | Failure Cause | Likelihood | Severity | Priority | Origin |
|----|---------------|------------|----------|----------|--------|
| PM3-001 | T-04/False-Positive Protocol conflict | High | Major | P1 | NEW (introduced by SR2-002 fix) |
| PM3-002 | Case 5 ordering vs. canonical decomposition sequence | Medium | Minor | P2 | NEW |
| PM3-003 | EAP-01 vs. heuristic threshold inconsistency | Medium | Major | P1 | NEW (latent from R1) |
| PM3-004 | Writer Agent Self-Review step ordering inversion | Medium | Minor | P2 | NEW (introduced by SR2-002 fix) |
| PM3-005 | H-02 "use judgment" unverifiable for agents | Low | Minor | P3 | PERSISTS from SR2-015 |

---

## S-012 FMEA Findings

### Element Decomposition (Round 3)

| Element ID | Element | Round 3 Delta |
|-----------|---------|---------------|
| E-01 | Tutorial Quality Criteria (T-01 through T-08) | T-03, T-08 CLOSED; T-04/FPP conflict NEW |
| E-02 | How-To Guide Quality Criteria (H-01 through H-07) | H-01/H-07, H-03/HAP-04, H-02 3+sentences all CLOSED; H-02 "use judgment" persists minor |
| E-03 | Reference Quality Criteria (R-01 through R-07) | R-01 non-code scope CLOSED; all open items resolved |
| E-04 | Explanation Quality Criteria (E-01 through E-07) | E-01 ordered concept suppression CLOSED; EAP-01 vs. heuristic threshold NEW |
| E-05 | Tutorial Anti-Patterns (TAP-01 through TAP-05) | All closed from R2 |
| E-06 | How-To Anti-Patterns (HAP-01 through HAP-05) | HAP-03 audience tie CLOSED; HAP-04/H-03 CLOSED |
| E-07 | Reference Anti-Patterns (RAP-01 through RAP-05) | No change; all remain closed |
| E-08 | Explanation Anti-Patterns (EAP-01 through EAP-05) | EAP-01 vs. heuristic inconsistency NEW |
| E-09 | Detection Heuristics (Section 3) | False-positive protocol CLOSED; T-04 conflict NEW; step ordering NEW |
| E-10 | Classification Decision Guide (Section 4) | Decomposition sequence rationale CLOSED; Case 5 ordering conflict NEW |
| E-11 | Jerry Voice Guidelines (Section 5) | Voice scope CLOSED; FM-018 (HARD rule reference) OPEN |

### Updated FMEA Failure Mode Analysis

**E-01 / E-09: Tutorial Quality Criteria and Detection Heuristics**

| FM-ID | Failure Mode | Effect | S | O | D | RPN | Status | Severity |
|-------|-------------|--------|---|---|---|-----|--------|----------|
| FM-001 | T-08 unverifiable by LLM agents | Criterion silently ignored | 6 | 8 | 7 | 336 | **CLOSED** (Round 2) | Closed |
| FM-002 | T-03 "introduced earlier" ambiguous scope | Agents disagree on prerequisite scope | 5 | 5 | 6 | 150 | **CLOSED** (Round 3) | Closed |
| FM-R3-01 | T-04 "zero alternatives" vs. False-Positive Protocol "suppress OS conditional Alternatively" | Tutorial with macOS/Windows alternatives simultaneously fails T-04 and passes FPP; contradictory evaluation outcomes | 6 | 7 | 6 | 252 | **NEW (OPEN)** | Major |

**E-02 / E-06: How-To Guide Quality Criteria and Anti-Patterns**

| FM-ID | Failure Mode | Effect | S | O | D | RPN | Status | Severity |
|-------|-------------|--------|---|---|---|-----|--------|----------|
| FM-003 | H-02/H-03 conditional branch clarified | [Fixed Round 2] | -- | -- | -- | -- | **CLOSED** | Closed |
| FM-004 | H-01/H-07 overlap — no tiebreaker | Ambiguous title assessment | 5 | 4 | 5 | 100 | **CLOSED** (Round 3) | Closed |
| FM-NEW01 | H-02 "3+ sentences" creates 2-sentence blind spot | 2-sentence digressions implicitly permitted | 4 | 5 | 6 | 120 | **PARTIALLY MITIGATED** — "use judgment" note added but unverifiable | Minor |

**E-04 / E-08: Explanation Quality Criteria and Anti-Patterns**

| FM-ID | Failure Mode | Effect | S | O | D | RPN | Status | Severity |
|-------|-------------|--------|---|---|---|-----|--------|----------|
| FM-007 | E-01 "Zero numbered procedure lists" suppresses ordered concept lists | Legitimate enumeration prevented | 5 | 6 | 7 | 210 | **CLOSED** (Round 3) | Closed |
| FM-008 | E-02 minimum two cross-references may be excessive | Fixed in R2 | 3 | 5 | 5 | 75 | **CLOSED** | Closed |
| FM-R3-02 | EAP-01 fires on any imperative verb; heuristic requires 2+ per paragraph | Contradictory detection for single-imperative explanation sentences | 5 | 6 | 6 | 180 | **NEW (OPEN)** | Major |

**E-05 through E-07: Anti-Pattern Tables**

| FM-ID | Failure Mode | Effect | S | O | D | RPN | Status | Severity |
|-------|-------------|--------|---|---|---|-----|--------|----------|
| FM-009 | Severity ratings undocumented | False positive severity escalation | 6 | 5 | 7 | 210 | **OPEN** (persists) | Major |
| FM-010 | HAP-04 vs. H-03 direct contradiction | Contradictory evaluation for conditional branches | 7 | 6 | 8 | 336 | **CLOSED** (Round 3) | Closed |

**E-09: Detection Heuristics**

| FM-ID | Failure Mode | Effect | S | O | D | RPN | Status | Severity |
|-------|-------------|--------|---|---|---|-----|--------|----------|
| FM-011 | No false-positive handling | Legitimate platform-conditionals flagged | 7 | 7 | 8 | 392 | **CLOSED** (Round 3) | Closed |
| FM-012 | "2+ imperative verb sequences" — "sequences" undefined | Inconsistent heuristic application | 5 | 6 | 6 | 180 | **CLOSED** (Round 3 — replaced with "imperative sentences") | Closed |
| FM-013 | "3+ consecutive sentences" fires on context-setting | False positive in how-to guide opening | 4 | 6 | 6 | 144 | **CLOSED** (Round 3 — exception added) | Closed |
| FM-R3-03 | Writer Agent Self-Review step 2 flags before step 3 checks false-positives | Agents flag then retract; causes user confusion | 4 | 6 | 7 | 168 | **NEW (OPEN)** | Minor |

**E-10: Classification Decision Guide**

| FM-ID | Failure Mode | Effect | S | O | D | RPN | Status | Severity |
|-------|-------------|--------|---|---|---|-----|--------|----------|
| FM-014 | Confidence thresholds uncalibrated | Inconsistent classification | 7 | 7 | 8 | 392 | **CLOSED** (Round 2) | Closed |
| FM-015 | No feedback loop from repeated [ACKNOWLEDGED] | Misclassified docs persist | 6 | 4 | 8 | 192 | **CLOSED** (Round 3 — step 4 added) | Closed |
| FM-016 | Decomposition sequence prescriptive without rationale | Agents follow order without understanding | 3 | 5 | 6 | 90 | **CLOSED** (Round 3 — rationale note added) | Closed |
| FM-R3-04 | Case 5 enumeration order (Reference, Explanation, How-To) contradicts canonical sequence (Tutorial, How-To, Reference, Explanation) | Writer agents produce wrong decomposition ordering for SKILL.md-type documents | 4 | 5 | 6 | 120 | **NEW (OPEN)** | Minor |

**E-11: Jerry Voice Guidelines**

| FM-ID | Failure Mode | Effect | S | O | D | RPN | Status | Severity |
|-------|-------------|--------|---|---|---|-----|--------|----------|
| FM-017 | Voice not scoped to Diataxis deliverables | Jerry rule file style conflicts | 7 | 5 | 8 | 280 | **CLOSED** (Round 3 — Scope note added) | Closed |
| FM-018 | Voice Quality Gate references H-15 but specifies no HARD rule for voice compliance | No enforceable compliance path | 5 | 6 | 7 | 210 | **OPEN** (persists) | Minor |

### FMEA Summary (Round 3)

| Status | Count | Notes |
|--------|-------|-------|
| CLOSED (this round) | 12 | FM-002, FM-004, FM-007, FM-010, FM-011, FM-012, FM-013, FM-015, FM-016, FM-017 + 2 from R2 context |
| CLOSED (prior rounds) | 6 | FM-001, FM-003, FM-008, FM-014 + 2 R2 context fixes |
| PARTIALLY MITIGATED | 1 | FM-NEW01 (H-02 "use judgment") |
| NEW OPEN | 4 | FM-R3-01 (RPN 252), FM-R3-02 (RPN 180), FM-R3-03 (RPN 168), FM-R3-04 (RPN 120) |
| PERSISTING OPEN | 2 | FM-009 (RPN 210), FM-018 (RPN 210) |

**Highest-risk open elements (Round 3):**
- FM-R3-01: RPN 252 — T-04 vs. False-Positive Protocol direct conflict (NEW, Critical path: tutorial authorship)
- FM-009: RPN 210 — severity ratings undocumented for anti-pattern tables (persisting from Round 1)
- FM-018: RPN 210 — Voice Quality Gate lacks HARD rule reference (persisting from Round 1)
- FM-R3-02: RPN 180 — EAP-01 vs. heuristic threshold inconsistency (NEW)
- FM-R3-03: RPN 168 — Writer Agent Self-Review step ordering inversion (NEW)
- FM-R3-04: RPN 120 — Case 5 ordering vs. canonical sequence (NEW)

---

## S-010 Self-Refine Recommendations

### Findings Table (Round 3 — New Findings Only)

All Round 2 findings that remain open are listed with their updated status. New Round 3 findings are marked NEW.

#### New Major Findings (Priority 1)

| ID | Finding | Severity | Evidence | Dimension |
|----|---------|----------|----------|-----------|
| SR3-001 | T-04 directly conflicts with False-Positive Handling Protocol for OS-conditional tutorials | **Major** | T-04 pass condition (line 26): "Zero 'alternatively' or 'you could also' constructions." False-Positive Protocol (line 131): "Alternatively in a tutorial step introducing a platform-specific path (macOS/Windows/Linux) is a legitimate OS conditional, NOT how-to contamination. Suppress flag." These are irreconcilable: T-04 requires zero instances; FPP says the instance is legitimate. An OS-conditional tutorial fails T-04 but passes FPP. FM-R3-01, RPN 252. | Internal Consistency |
| SR3-002 | EAP-01 fires on any single imperative verb in explanation; Section 3 heuristic requires 2+ per paragraph — no reconciliation guidance | **Major** | EAP-01 (line 106): "Imperative verbs ('Run this', 'Configure that')" — no count threshold. Detection heuristic (line 120): "2+ imperative sentences ... within a single paragraph." For one imperative sentence in an explanation document, EAP-01 says flag, heuristic says do not flag. No tiebreaker or scope note specifies which table to use. FM-R3-02, RPN 180. | Internal Consistency |

#### New Minor Findings (Priority 2)

| ID | Finding | Severity | Evidence | Dimension |
|----|---------|----------|----------|-----------|
| SR3-003 | Writer Agent Self-Review step 2 instructs flagging before step 3 instructs false-positive check — inverted order | **Minor** | Lines 141-142: Step 2 says "When a mixing signal is detected: (a) flag with appropriate `[QUADRANT-MIX: ...]` tag..." before step 3 instructs agents to "Apply the False-Positive Handling Protocol above before flagging." The sequential numbered list reads flag-then-check, but the protocol text says check-then-flag. FM-R3-03, RPN 168. | Methodological Rigor |
| SR3-004 | Case 5 decomposition enumeration order (Reference, Explanation, How-To) contradicts canonical Multi-Quadrant Decomposition sequence (Tutorial, How-To, Reference, Explanation) | **Minor** | Lines 191-193 (Case 5): "1. Reference: Agent registry table... 2. Explanation: Purpose... 3. How-To Guide: Step-by-step..." Line 199 (canonical): "Tutorial first (if present), then How-To Guide, then Reference, then Explanation." Case 5 does not follow the canonical sequence. Writer agents using Case 5 as a template will produce misordered decompositions. FM-R3-04, RPN 120. | Internal Consistency |

#### Persisting Open Findings

| ID | Finding | Severity | Evidence | Dimension |
|----|---------|----------|----------|-----------|
| SR3-005 | FM-009: Anti-pattern severity ratings have no documented derivation (persists from Round 1) | **Major** | Section 2 tables list "Severity: Major/Minor" per anti-pattern. No criteria, scale, or rationale for these assignments is provided. Agent applying them mechanically may over- or under-penalize violations. | Traceability |
| SR3-006 | FM-018: Voice Quality Gate references H-15 but no HARD rule governs voice compliance enforcement (persists from Round 1) | **Minor** | Lines 269-274: Voice Quality Gate is actionable (4 steps) but specifies no governing rule tier. Agents cannot treat voice violations as HARD constraint violations. The gate implies enforcement without specifying enforcement level. | Traceability |
| SR3-007 | SR2-011: No `###`-level subsection navigation (persists from Round 1) | **Minor** | File is now 275 lines. Navigation table covers only the 5 `##` headings. Readers and agents seeking "How-To Guide Quality Criteria" or "Explanation Anti-Patterns" have no navigation anchor. | Actionability |
| SR3-008 | FM-NEW01: H-02 "use judgment" instruction unverifiable for automated agents (partially mitigated) | **Minor** | Line 37: "1-2 sentence digressions are below mandatory-flag threshold; use judgment when they substantially interrupt action flow." No structural heuristic replaces "use judgment" for borderline cases. | Methodological Rigor |

### Prioritized Revision Plan (Round 3)

**Priority 1 — Must fix before deployment:**

**SR3-001 — T-04/False-Positive Protocol Conflict (HIGHEST PRIORITY):**
The conflict requires a resolution strategy. Two options:

Option A (preferred): Add a scope note to T-04 that explicitly creates an exception for platform-conditional alternatives:
> Pass Condition: "Zero 'alternatively' or 'you could also' constructions, **except** OS-conditional platform alternatives (e.g., 'Alternatively, on macOS, run `brew install X`'). OS-conditional alternatives are documented in the False-Positive Handling Protocol and do not violate T-04."

Option B: Add a precedence rule to the False-Positive Protocol:
> "When an override condition suppresses a detection flag, the corresponding quality criterion's pass condition is also satisfied. The False-Positive Protocol takes precedence over literal pass condition language when the override condition applies."

Option A is preferred because it makes the exception visible at the point of evaluation (T-04) rather than requiring the agent to locate and apply a cross-document precedence rule.

**SR3-002 — EAP-01 vs. Heuristic Threshold:**
Add a scope note to EAP-01 or the heuristic detection table clarifying the relationship:
> Option A: Add to EAP-01 Detection Signal column: "Single instance: Minor. Quantitative threshold for Major classification: see Section 3 detection heuristics."
> Option B: Add a note to the Section 3 heuristic row: "Section 2 EAP-01 also applies to single-instance imperative verbs (Minor severity). This heuristic escalates to Major at the 2+/paragraph threshold."

Either option creates a coherent two-level severity model: EAP-01 catches any instance (Minor); the heuristic escalates at the paragraph-level threshold (Major).

**Priority 2 — Address in next iteration:**

**SR3-003 — Writer Agent Self-Review Step Ordering:**
Reorder to place the false-positive check before the flag action. Replace:
> "2. When a mixing signal is detected: (a) flag with appropriate `[QUADRANT-MIX: ...]` tag, (b) describe the flagged content to the user, (c) ask whether to remove/revise or keep with `[ACKNOWLEDGED]` marker"
> "3. Apply the False-Positive Handling Protocol above before flagging -- suppress signals that match an override condition"

With:
> "2. When a mixing signal is detected: (a) first apply the False-Positive Handling Protocol — if the signal matches an override condition, suppress and do not flag; (b) if not suppressed, flag with appropriate `[QUADRANT-MIX: ...]` tag; (c) describe the flagged content to the user; (d) ask whether to remove/revise or keep with `[ACKNOWLEDGED]` marker"

**SR3-004 — Case 5 Ordering:**
Update Case 5 decomposition enumeration to match the canonical Tutorial-How-To-Reference-Explanation sequence. Since Case 5 does not include a tutorial, the corrected order is:
> "1. How-To Guide: Step-by-step invocation instructions
>  2. Reference: Agent registry table, parameter specifications
>  3. Explanation: Purpose, design rationale, architectural context"

**Priority 3 — Quality improvements:**

**SR3-005 — Anti-Pattern Severity Derivation:** Add a brief legend before Section 2 tables: "Severity ratings: Major = directly affects reader's ability to complete the task or correctly classify the document. Minor = degrades quality or increases friction but does not cause task failure."

**SR3-006 — Voice Quality Gate Rule Tier:** Add one sentence after the gate header: "Voice compliance is a MEDIUM standard (not HARD). Flag violations with `[VOICE: ...]` tags and apply per the self-review protocol."

**SR3-007 — Subsection Navigation:** Add `###`-level anchors and a per-section mini-navigation or consider a quick-reference ID table mapping criterion IDs (T-01, H-03, etc.) to their section lines.

**SR3-008 — H-02 "Use Judgment" Heuristic:** Replace "use judgment when they substantially interrupt action flow" with: "1-2 sentence digressions do not require flagging unless they appear between two numbered steps (not at the end of a step block); in that case, treat as Minor."

---

## S-014 Quality Scoring

### Dimension-Level Assessment

**1. Completeness (weight: 0.20)**
- Tutorial, How-To, Reference, Explanation criteria: 8+7+7+7=29 criteria with test and pass conditions.
- Anti-patterns: 20 total with detection signals.
- Detection heuristics: 7 signals with agent actions and severity.
- False-Positive Handling Protocol: now present with 3 override conditions (SR2-002 CLOSED).
- Writer Agent Self-Review: 4 steps including reclassification escalation (SR2-005 CLOSED).
- Classification guide: 2-axis test, confidence derivation, 5 borderline cases, multi-quadrant decomposition with rationale.
- Voice guidelines: scoped to Diataxis deliverables (SR2-003 CLOSED).
- **Remaining gap:** SR3-001 (T-04/FPP conflict) creates an incomplete specification — one common tutorial pattern (OS-conditional) has contradictory pass/fail guidance, representing an unsatisfied completeness requirement for tutorial authorship.
- **Dimension Score: 0.89** (up from 0.77; gap from T-04/FPP conflict)

**2. Internal Consistency (weight: 0.20)**
- H-03/HAP-04: CLOSED (boundary definition on both sides).
- H-01/H-07: CLOSED (tiebreaker added).
- E-01 ordered concept suppression: CLOSED.
- **New conflicts (Round 3):** SR3-001 (T-04 vs. FPP — directly irreconcilable instructions for OS-conditional tutorials, High likelihood), SR3-002 (EAP-01 vs. heuristic threshold — contradictory severity for single-imperative explanation sentences), SR3-004 (Case 5 vs. canonical sequence — different ordering in same section).
- Three new internal consistency issues prevent a high score despite the 10+ closures this round.
- **Dimension Score: 0.83** (up from 0.78; new conflicts partially offset closures)

**3. Methodological Rigor (weight: 0.20)**
- Confidence threshold rationale: CLOSED from R2.
- Imperative sentences definition: CLOSED (SR2-006).
- Context-setting exemption: CLOSED (SR2-007).
- Decomposition sequence rationale: CLOSED (SR2-013).
- T-03 scope boundary: CLOSED (SR2-008).
- **Remaining issues:** SR3-003 (step ordering inversion — protocol says check-then-flag, list reads flag-then-check), SR3-008 (H-02 "use judgment" still unverifiable for automated agents).
- **Dimension Score: 0.91** (up from 0.82; step ordering issue is minor)

**4. Evidence Quality (weight: 0.15)**
- All quality criteria: test + pass condition columns maintained throughout remediations.
- Anti-pattern detection signals: specific and pattern-matchable.
- Borderline cases: 5 concrete examples with resolution reasoning.
- Before/after voice examples: concrete and illustrative.
- T-08 [UNTESTED] flag: well-targeted.
- Confidence derivation rationale column: present.
- False-positive override conditions: specific enough to match programmatically.
- **No new evidence quality issues introduced.**
- **Dimension Score: 0.92** (stable from R2)

**5. Actionability (weight: 0.15)**
- Per-criterion test and pass conditions: highly actionable.
- False-Positive Handling Protocol: adds actionable override conditions (SR2-002 CLOSED).
- Writer Agent Self-Review escalation: step 4 adds reclassification path (SR2-005 CLOSED).
- Voice scope: agents now know when to apply Section 5 (SR2-003 CLOSED).
- **Remaining issues:** SR3-001 conflict creates unactionable situation for agents evaluating OS-conditional tutorials (both T-04 and FPP are actionable individually, but jointly they give contradictory action). SR3-003 (step ordering) creates procedural confusion in self-review. SR3-007 (subsection navigation) reduces navigability.
- **Dimension Score: 0.89** (up from 0.83; T-04/FPP conflict partially reduces gains)

**6. Traceability (weight: 0.10)**
- Criterion IDs (T-01 through E-07): stable.
- Anti-pattern IDs (TAP-01 through EAP-05): stable.
- Decomposition sequence rationale: CLOSED (SR2-013).
- T-03 scope: CLOSED (SR2-008).
- **Remaining issues:** SR3-005 (anti-pattern severity derivation undocumented — persists from Round 1, FM-009), SR3-006 (Voice Quality Gate lacks rule tier — persists, FM-018).
- **Dimension Score: 0.88** (up from 0.82; two traceability gaps persist)

### Weighted Composite Score

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|---------|
| Completeness | 0.20 | 0.89 | 0.178 |
| Internal Consistency | 0.20 | 0.83 | 0.166 |
| Methodological Rigor | 0.20 | 0.91 | 0.182 |
| Evidence Quality | 0.15 | 0.92 | 0.138 |
| Actionability | 0.15 | 0.89 | 0.134 |
| Traceability | 0.10 | 0.88 | 0.088 |
| **Total** | **1.00** | | **0.886** |

**Round 3 Composite Score: 0.886**

### Score Interpretation

| Band | Score Range | This Deliverable |
|------|------------|------------------|
| PASS | >= 0.95 | Not reached |
| REVISE | 0.85 - 0.94 | **0.886 — REVISE** |
| REJECTED | < 0.85 | Not reached |

**Delta from Round 2:** +0.070 (0.816 -> 0.886). The substantial improvement reflects all 7 Priority 1 remediations being applied. However, 2 new Major findings (SR3-001 T-04/FPP conflict, SR3-002 EAP-01/heuristic conflict) introduced by the remediation effort prevented crossing the 0.95 threshold.

**Score decomposition of shortfall:** The 0.064 gap to the 0.95 threshold is driven primarily by:
1. Internal Consistency (0.83): Three new conflicts (SR3-001, SR3-002, SR3-004) account for approximately 0.025 of the gap.
2. Completeness (0.89): SR3-001 creates contradictory authorship guidance for the most common tutorial pattern, accounting for approximately 0.020 of the gap.
3. Actionability (0.89): T-04/FPP conflict and step ordering inversion reduce actionability scores, accounting for approximately 0.015 of the gap.

---

## Finding Summary Table

### Round 3 New Findings

| ID | Severity | Finding | Location | Origin |
|----|----------|---------|----------|--------|
| SR3-001 | **Major** | T-04 "zero alternatives" directly conflicts with False-Positive Protocol "suppress OS-conditional Alternatively" — irreconcilable for platform-conditional tutorials | Section 1 (T-04 line 26), Section 3 (FPP line 131) | Introduced by SR2-002 fix |
| SR3-002 | **Major** | EAP-01 fires on any single imperative verb in explanation; Section 3 heuristic requires 2+ per paragraph — no reconciliation guidance, contradictory for single-instance cases | Section 2 (EAP-01 line 106), Section 3 (heuristic line 120) | Latent from Round 1 |
| SR3-003 | Minor | Writer Agent Self-Review step 2 instructs flagging before step 3 instructs false-positive check — numbering inverts intended logical order | Section 3, Writer Agent Self-Review (lines 141-142) | Introduced by SR2-002 fix |
| SR3-004 | Minor | Case 5 decomposition enumeration (Reference, Explanation, How-To) contradicts canonical Multi-Quadrant Decomposition sequence (Tutorial, How-To, Reference, Explanation) | Section 4, Case 5 (lines 191-193) vs. Multi-Quadrant (line 199) | Latent from Round 1 |

### Persisting Open Findings

| ID | Severity | Finding | Location | Persisting From |
|----|----------|---------|----------|-----------------|
| SR3-005 | **Major** | Anti-pattern severity ratings (Major/Minor) have no documented derivation criteria | Section 2, all anti-pattern tables | Round 1 (FM-009) |
| SR3-006 | Minor | Voice Quality Gate references H-15 but no rule tier (HARD/MEDIUM/SOFT) specified for voice compliance | Section 5, Voice Quality Gate (lines 269-274) | Round 1 (FM-018) |
| SR3-007 | Minor | No `###`-level subsection navigation in 275-line document | Document-wide | Round 1 (SR-010) |
| SR3-008 | Minor | H-02 "use judgment" instruction unverifiable for automated agents in 1-2 sentence digression borderline cases | Section 1, H-02 (line 37) | Round 2 (SR2-015) |

### Fixed in Round 3 (from Round 2 open list)

| Former ID | Finding | Fix Applied |
|-----------|---------|-------------|
| SR2-001 | H-03/HAP-04 contradiction | Boundary definition added to both H-03 and HAP-04 |
| SR2-002 | False-positive handling absent | False-Positive Handling Protocol subsection added |
| SR2-003 | Voice not scoped to Diataxis deliverables | Scope block added to Section 5 opening |
| SR2-004 | E-01 ordered concept suppression | Pass condition distinguishes procedure vs. concept lists |
| SR2-005 | No reclassification escalation | Step 4 added to Writer Agent Self-Review Behavior |
| SR2-006 | "sequences" undefined | Replaced with "imperative sentences" with definition |
| SR2-007 | Context-setting false positive | Exception added for first-paragraph context-setting |
| SR2-008 | T-03 "introduced earlier" scope | Scope clarification added in-criterion |
| SR2-009 | R-01 non-code reference | Note added for non-code reference interpretation |
| SR2-010 | H-01/H-07 no tiebreaker | Tiebreaker note added to H-01 |
| SR2-012 | HAP-03 audience competence untied | Detection signal updated to "stated audience level" |
| SR2-013 | Decomposition sequence rationale | Rationale note added in-line |

---

## Execution Statistics

- **Total Round 3 New Findings:** 8 (2 Major, 6 Minor)
- **New Critical:** 0
- **New Major:** 2 (SR3-001, SR3-002)
- **New Minor:** 6 (SR3-003, SR3-004, SR3-005 persisting, SR3-006 persisting, SR3-007 persisting, SR3-008 persisting)
- **Round 2 Findings Closed:** 12 (all 7 Priority 1 + 5 Priority 2/3)
- **Persisting Open:** 4 (SR3-005 through SR3-008)
- **New Open:** 4 (SR3-001 through SR3-004)
- **Protocol Steps Completed:** 4 of 4 (S-007, S-004, S-012, S-010)

**Constitutional Compliance Score (S-007):** 0.97 (no HARD violations; one persistent MEDIUM advisory)
**Round 3 Composite Score (S-014):** 0.886
**Quality Gate Result:** REVISE (threshold 0.95 not met; above 0.85 REVISE band)

**Recommended Action:** REVISE — Round 4 required. Two Priority 1 findings (SR3-001, SR3-002) must be addressed to cross the 0.95 threshold. These are the only Major findings remaining. SR3-001 (T-04/FPP conflict) is the highest-priority fix: it directly contradicts authorship guidance for the most common tutorial pattern. SR3-002 (EAP-01/heuristic inconsistency) creates contradictory detection for explanation anti-patterns. With these two fixed plus the four Minor findings addressed, the projected Round 4 score is >= 0.95 (each dimension would reach 0.92+ with these targeted fixes).

**Projected Round 4 score if all 4 new findings addressed:**
- Internal Consistency: ~0.94 (3 new conflicts resolved)
- Completeness: ~0.94 (T-04/FPP conflict resolved)
- Methodological Rigor: ~0.94 (step ordering inversion resolved)
- Actionability: ~0.93 (conflict resolution restores unambiguous agent behavior)
- Evidence Quality: ~0.92 (stable)
- Traceability: ~0.90 (FM-009 severity derivation + FM-018 rule tier)
- Projected composite: ~0.934

To reach 0.95, the persisting SR3-005 (anti-pattern severity derivation, FM-009) and SR3-006 (voice rule tier, FM-018) — both persisting from Round 1 — must also be addressed.
