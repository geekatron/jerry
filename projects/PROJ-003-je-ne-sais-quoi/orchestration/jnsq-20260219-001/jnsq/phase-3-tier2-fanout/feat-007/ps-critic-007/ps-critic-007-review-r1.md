# ps-critic-007 Review R1: S-010 + S-003 (Steelman) + S-002 (Devil's Advocate)

<!--
AGENT: ps-critic-007
ROUND: 1
STRATEGIES: S-010 (Self-Refine), S-003 (Steelman), S-002 (Devil's Advocate)
DELIVERABLE: ps-creator-007-draft.md (v0.1.0 -> v0.2.0)
DATE: 2026-02-19
-->

## Document Sections

| Section | Purpose |
|---------|---------|
| [S-003 Steelman: Strongest Aspects](#s-003-steelman-strongest-aspects) | What works well and why (H-16: steelman before devil's advocate) |
| [S-010 Self-Refine: Internal Consistency](#s-010-self-refine-internal-consistency) | Template/rule inconsistencies found |
| [S-002 Devil's Advocate: Challenges](#s-002-devils-advocate-challenges) | Weaknesses identified and challenged |
| [Fixes Applied](#fixes-applied) | Changes made to draft in this round |
| [Open Items for R2](#open-items-for-r2) | Issues deferred or requiring deeper review |

---

## S-003 Steelman: Strongest Aspects

Per H-16, steelman analysis is presented before devil's advocate critique.

### 1. Proportionality Principle (Design Philosophy, lines 56-62)

The proportionality principle is the document's load-bearing design decision. By mapping delight energy to criticality and achievement significance, it prevents the two most common delight system failures: inflation (celebrating everything) and monotony (celebrating everything the same way). The C1-no-personality through C4-full-celebration gradient is well-calibrated against the quality-enforcement.md criticality levels.

### 2. Celebration Anti-Patterns (lines 287-296)

The six named anti-patterns (Inflation, Fatigue, Premature, Tone-deaf, Performative, Dismissive) with concrete fixes are a strong defensive specification. Naming the failure modes explicitly gives implementers a checklist that prevents the most common DX delight failures. The "Tone-deaf" anti-pattern (celebrating after repeated REJECTED failures) is particularly insightful -- it shows awareness that the developer's emotional state after a hard-won pass is relief, not joy.

### 3. Zero Personality Budget for Debugging/Error Recovery (lines 306-394)

The decision to set personality budget to zero in debugging and error recovery contexts is correct and well-reasoned. This directly inherits the persona doc's boundary condition "NOT a replacement for information" and the Audience Adaptation Matrix's "None" humor setting for REJECTED/Hard Stop contexts. The soundtrack energy anchors (Gang Starr "Moment of Truth" for debugging, Radiohead "Everything in Its Right Place" for error recovery) are implementer calibration tools, not user-facing references -- a smart distinction.

### 4. One-Sentence Rule with Clear Exceptions (line 66)

Making the one-sentence constraint HARD with exactly three named exceptions (F-003 Powder Day farewell, C4 tournament pass, epic complete) is disciplined design. The exceptions are justified by rarity and significance. This prevents scope creep where every delight moment gradually gets "just one more line."

### 5. Fallback Variant Weighting (line 420)

The 30% fallback weight is a well-calibrated fatigue prevention mechanism. Rather than trying to make every personality message perfect, it accepts that the best personality moments are the ones surrounded by clean, information-only messages. This is consistent with the persona doc's "when earned" criterion for absurdist elements.

### 6. Delight Budget Per Session (lines 692-698)

The graduated budget (2/4/6/8 personality moments by session duration) with fallback-to-information when exhausted is a practical implementation of the anti-fatigue principle. The budgets are conservative, which is correct -- understatement is explicitly called out as a design principle.

---

## S-010 Self-Refine: Internal Consistency

### Finding R1-001: Message Catalog C2 V-001 Inconsistency (FIXED)

**Location:** Message Catalog, C2 V-001 (line 545) vs. Delight Mechanics C2 variants (lines 413-418)

**Issue:** C2 V-001 in the Message Catalog had a `{secondary_observation}` placeholder not present in the Delight Mechanics section's C2 variants. The two sections describing the same messages were inconsistent.

**Fix:** Removed `{secondary_observation}` from C2 V-001 to match the Delight Mechanics variants.

### Finding R1-002: G-003 Context Description Mismatch (FIXED)

**Location:** Session Greetings table (line 98) vs. Greeting Selection Rules (line 107)

**Issue:** G-003's context column said "When the developer has not had a session in >24 hours" but selection rule 4 maps "first session with this project" to G-003. A developer's first-ever session has no prior session, so the ">24 hours" framing was misleading.

**Fix:** Updated G-003 context to "When the developer has not had a session in >24 hours, or when this is the developer's first session on this project."

### Finding R1-003: sb-calibrator Below-Threshold Handling Missing (FIXED)

**Location:** Integration with /saucer-boy, sb-calibrator Scoring (line 496)

**Issue:** The document specified a >= 0.80 scoring target but did not specify what happens when a template falls below. Is it revised? Removed? Replaced with fallback?

**Fix:** Added "Below-Threshold Handling" paragraph specifying: route to sb-rewriter, re-score, replace with fallback after two failed iterations.

### Finding R1-004: Streak Budget Interaction Unspecified (FIXED)

**Location:** Streak Rules (line 449)

**Issue:** Streak rule 1 says "Streak messages replace the standard delight observation" but did not clarify whether streaks consume a delight budget slot.

**Fix:** Added rule 2: "Streak messages consume one delight budget slot, the same as the standard observation they replace." Renumbered subsequent rules.

### Finding R1-005: FEAT-003 Alignment Caveat Missing (FIXED)

**Location:** Traceability table (line 776)

**Issue:** Self-review claimed FEAT-003 alignment as PASS, but FEAT-003 is at v0.1.0 (DRAFT). Alignment cannot be confirmed against an unreviewed document.

**Fix:** Added note to traceability entry: "FEAT-003 is at v0.1.0 (DRAFT); visual identity alignment is preliminary and should be re-confirmed when FEAT-003 reaches REVIEWED status."

---

## S-002 Devil's Advocate: Challenges

### Challenge R1-C1: Achievement Tracking Persistence Ambiguity

The document says achievements are tracked in "session state or WORKTRACKER.md metadata" (line 283). The "or" is load-bearing. If achievements are in session state only, they are lost on session boundaries. If they are in WORKTRACKER.md metadata, they survive but require WORKTRACKER schema changes. The State Management section (line 706) shows `achievement_flags` in a YAML structure but says it "can be persisted as a section in WORKTRACKER.md metadata or as a separate lightweight file." This ambiguity should be resolved in implementation but is acceptable for a spec-level document.

**Disposition:** Noted for R2 -- evaluate whether this ambiguity is acceptable at spec level or needs a RECOMMENDED approach.

### Challenge R1-C2: Soundtrack Anchors -- Implementer vs. User Confusion Risk

Each tone calibration context includes a "Soundtrack energy anchor" (e.g., line 321: "Gang Starr, 'Moment of Truth'"). These are described as implementer calibration tools. However, nothing in the document explicitly warns implementers that these must NOT appear in user-facing output. The debugging rules say "No jokes. No references. No soundtrack allusions. No ski metaphors." (line 319), which implicitly covers it for debugging, but the Creating context says "Allow moderate humor" and does not explicitly exclude soundtrack references.

**Disposition:** Flagged for R2 fix -- add explicit rule that soundtrack energy anchors are internal calibration and must never appear in user-facing messages.

### Challenge R1-C3: Time-of-Day Variant Coverage Gap

The time-of-day windows (lines 426-432) cover 06:00-09:00, 09:00-17:00, 17:00-22:00, 22:00-02:00, and 02:00-06:00. The 09:00-17:00 window says "No time-based adaptation." This is complete coverage, but the morning greeting variant (line 428) says "Morning session. Enforcement architecture is up." -- this is a session greeting variant, not a standalone time-of-day variant. The relationship between time-of-day variants and session greeting variants needs clarification: are they additive? Does the time variant replace the greeting? Or is time-of-day awareness only a modifier on existing greeting/farewell templates?

**Disposition:** Flagged for R2 fix -- clarify the interaction model between time-of-day variants and session message templates.

---

## Fixes Applied

| Finding | Fix | Lines Affected |
|---------|-----|----------------|
| R1-001 | Removed `{secondary_observation}` from C2 V-001 | Message Catalog |
| R1-002 | Updated G-003 context to include first-session case | Session Greetings table |
| R1-003 | Added Below-Threshold Handling paragraph | Integration with /saucer-boy |
| R1-004 | Added streak budget rule, renumbered | Streak Rules |
| R1-005 | Added FEAT-003 preliminary alignment note | Traceability table |

**Draft version:** 0.1.0 -> 0.2.0

---

## Open Items for R2

| ID | Issue | Source | Priority |
|----|-------|--------|----------|
| R2-001 | Achievement persistence ambiguity (session state vs. WORKTRACKER.md) | R1-C1 | MEDIUM |
| R2-002 | Soundtrack anchor user-facing leak risk | R1-C2 | HIGH |
| R2-003 | Time-of-day / session greeting interaction model | R1-C3 | HIGH |
| R2-004 | Delight budget enforcement mechanism unspecified (who/what enforces it at runtime?) | New | MEDIUM |
| R2-005 | Context detection confidence -- what happens when context is misdetected? | New | MEDIUM |
