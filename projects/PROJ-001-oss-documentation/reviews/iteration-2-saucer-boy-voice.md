# Voice Compliance Report

> **Report:** sb-reviewer iteration-2 — INSTALLATION.md voice compliance
> **Prior Review:** `docs/reviews/iteration-1-saucer-boy-voice.md` — PASS with significant voice gap findings
> **Agent:** sb-reviewer v1.0.0
> **Date:** 2026-02-25

## Summary

**Verdict:** PASS
**Text Type:** documentation
**Audience Context:** onboarding
**Expected Tone:** Medium energy, warm humor, low technical depth, tone anchor = Invitation — "the system is learnable"

This revision closes the three highest-priority voice gaps identified in iteration 1. The Configuration section now carries warmth throughout its opening. The Troubleshooting section has a human acknowledgment sentence that changes its register. The Enable Hooks mid-section has the "immune system" line that holds warmth through a long procedural stretch. All five Authenticity Tests pass.

Two specific concerns merit tracking for iteration 3:

**Regression at skill-test endpoint:** "You're shredding" (the document's prior high-energy payoff at skill verification) was replaced with "Jerry is now fully operational." This is a voice loss at the celebration moment the Audience Adaptation Matrix specifically calls for high energy and humor. The replacement reads as a status indicator, not a landing.

**Partial resolution of Boundary #8:** The Troubleshooting section's mechanical assembly pattern has improved — the section no longer has six entries in identical Symptom/Cause/Fix template format. However, the "plugin not found" entry still uses the Symptom label as a standalone header, and the register across the troubleshooting entries is still variable in ways that read as assembled rather than written. The flag is reduced from HIGH severity to LOW severity, but it is not cleared.

The document is shippable. The above two items are the remaining voice investment targets.

---

## Authenticity Test Results

| Test | Name | Verdict | Evidence |
|------|------|---------|----------|
| 1 | Information Completeness | PASS | All sections complete. Prerequisites, all four install paths, hook setup, configuration (four-step project setup with platform-specific commands), verification, skill table, developer setup, troubleshooting (six categories), updating, uninstallation, getting help, license. No information gaps detected. |
| 2 | McConkey Plausibility | PASS | Voice that is present is plausible throughout. "It's how Jerry remembers what you're working on across sessions" — warm and functional. "Four steps and you're set" — direct, confident. "Think of hooks as Jerry's immune system — the skills are the muscles, but hooks keep everything running clean underneath" — earned analogy, not strained. "Installation has a few rough edges" — grounded, acknowledges reality. No section overreaches. |
| 3 | New Developer Legibility | PASS | All skiing metaphors remain transparent. "Shredding" (header), "pick the line that fits" (nav table — four options in a table, unambiguous), "immune system" (biological, not skiing). One mild flag: "What you need before dropping in" in the nav table — "dropping in" is slightly opaque for absolute non-skiers but recoverable from context ("What you need before..."). Not a failure. |
| 4 | Context Match | PASS (with gap at endpoint) | Configuration and Troubleshooting sections now hit the onboarding matrix target ("invitation — the system is learnable"). Enable Hooks holds warmth through the mid-section. However, the Verification > Skill Test sub-section ends with "Jerry is now fully operational" — a status-indicator close for what should be the document's landing moment. The Audience Adaptation Matrix calls for medium energy and warm humor in onboarding context; "fully operational" is low energy with no warmth. This is a context match gap, not a context match failure — the section is not wrong-energy, it is under-energy at its peak moment. |
| 5 | Genuine Conviction | PASS | Where voice is present it reads as believed. "Installation has a few rough edges — most of them are SSH or project configuration. Here's how to get through the common ones." carries the tone of someone who has actually helped people through these problems. "Think of hooks as Jerry's immune system" reads as a conviction-first analogy, not a decoration applied afterward. The skill verification endpoint ("Jerry is now fully operational") breaks conviction at the finish — a status report, not a collaborator landing the session. |

*No tests failed. All five evaluated.*

---

## Boundary Condition Check

| # | Boundary | Status | Evidence |
|---|----------|--------|----------|
| 1 | NOT Sarcastic | CLEAR | No mockery detected. All tone is inclusive. Troubleshooting entries are direct without condescension. |
| 2 | NOT Dismissive of Rigor | CLEAR | Quality and security notes handled with appropriate gravity. Hook early access caveat is appropriately serious. Security note in uv install is humor-free. Correct. |
| 3 | NOT Unprofessional in High Stakes | CLEAR | Security note in hooks section ("The commands below download and execute a script from astral.sh") remains entirely humor-free and direct. No humor in early-access caveat or security-sensitive sections. |
| 4 | NOT Bro-Culture Adjacent | CLEAR | "The whole crew" is not present in this revision. No exclusionary language detected. "The system is learnable" framing is inclusive. |
| 5 | NOT Performative Quirkiness | CLEAR | The "immune system" analogy is earned — it does explanatory work that "the hooks enforce rules" would not. The ski vocabulary is restrained and transparent. No strained whimsy, no emoji overload. |
| 6 | NOT Character Override | CLEAR | The document governs framework installation language only. No behavioral instructions to Claude. |
| 7 | NOT Information Replacement | CLEAR | All voice elements are additive. "Four steps and you're set" does not replace the four steps — they follow immediately. "Installation has a few rough edges" does not replace the troubleshooting entries — they follow. |
| 8 | NOT Mechanical Assembly | FLAGGED (reduced severity) | See detail below. |

### Boundary #8 Detail — Mechanical Assembly

**Status vs. Iteration 1:** The HIGH severity pattern (six consecutive identical Symptom/Cause/Fix template entries) has been broken. The Troubleshooting section now has varied structural openers across its entries. This is a meaningful improvement. The flag is reduced from HIGH to LOW severity.

**Remaining patterns detected:**

**Pattern 1 — Isolated Symptom label (Low severity):**
In the "Plugin not found after adding source" entry, the `**Symptom:**` label appears as a standalone bold element before the explanation: `**Symptom:** \`/plugin install jerry@jerry-framework\` returns "plugin not found"`. This is the only remaining entry using the Symptom header label as a document template artifact. The other entries have dropped it. The inconsistency — one entry retaining the label when all others abandoned it — reads as an oversight rather than a deliberate structural choice. It is not a failure, but it is an assembly seam.

**Pattern 2 — Voice register drop at Verification endpoint (Low-Medium severity):**
The Skill Test sub-section ends: "Jerry is now fully operational." This closes the document's highest-energy instructional moment in a flat register. Per `llm-tell-patterns.md` Voice Register Drop pattern: when the introduction and most of the document operate at a conversational-warm register, a hard drop to functional status language at the resolution point is a structural tell. The prior version's "You're shredding" was not wrong to remove — it may have been too casual for some audiences — but the replacement is under-energy rather than right-energy. The fix is not to restore the original; it is to find the right energy at the endpoint.

**Pattern 3 — "installation succeeded" at Step 4 confirmation (Low severity):**
Line 114: "If `jerry` appears, installation succeeded." replaces the prior "That's your signal — you're in." The replacement is accurate and clear. However, it is a confirmation written in passive-construction style. The information is present (Test 1: PASS). The voice is absent at a moment that is the payoff for completing a four-step install. Low severity because it is not the final verification — the Skill Test endpoint is.

No em-dash stacking detected. No hedging phrases detected. No formulaic transitions ("Here's the thing:") detected. No parallel structure formulae (three consecutive same-opening sentences) detected. No ungrounded quantitative claims detected.

---

## Voice Gap Comparison — Iteration 1 vs. Iteration 2

| Section | Iteration 1 Gap Level | Iteration 2 Gap Level | Change |
|---------|----------------------|----------------------|--------|
| Configuration opening | Significant | Closed | Improved |
| Troubleshooting section opening | Highest in document | Reduced — human acknowledgment present | Improved |
| Enable Hooks mid-section | Low-Medium | Closed — "immune system" line holds warmth | Improved |
| Step-level confirmations (Verification endpoint) | "You're shredding" was working | "Jerry is now fully operational" is under-energy | Regressed |
| Step-level confirmation (Install Step 4) | "you're in" was working | "installation succeeded" is under-energy | Minor regression |
| Prerequisites | Low-Medium gap (blockquote warmth) | Unchanged — same level as iteration 1 | Unchanged |
| Troubleshooting structural format | Six identical template entries | Varied structure, one remaining Symptom label | Improved |

Net: Three major gaps closed, one minor regression introduced, one minor regression introduced, one section unchanged.

---

## Suggested Fixes

Each fix is scoped and specific. Ordered by voice return on investment.

### Fix 1 — Verification endpoint — skill test confirmation (HIGH priority)

**Current text (line 372-373):**
```
You should see the problem-solving skill activate — it'll describe itself and list its available agents (researcher, analyst, architect, and the rest of the crew). Jerry is now fully operational.
```

**Issue:** "Jerry is now fully operational" closes the document's highest-energy instructional moment in a flat register. This is the payoff for completing the entire installation sequence — it should land. The Audience Adaptation Matrix calls for medium energy with warm humor in onboarding context. The current close treats verification as a checkbox, not as a reward.

**Direction for rewriter:** The conviction to work from is: getting the first skill to respond is the moment the developer knows it worked — everything before this was setup, this is the proof. The voice at this endpoint should feel like the payoff. "You're shredding" was probably right to remove (some audiences find it too casual). But the replacement needs more energy than a status indicator. Do not invent false enthusiasm; find the honest landing for someone who has just confirmed their install works.

---

### Fix 2 — Install Step 4 confirmation (MEDIUM priority)

**Current text (line 114):**
```
If `jerry` appears, installation succeeded. Head to [Configuration](#configuration) to set up your first project, then [Verification](#verification) to confirm everything's firing.
```

**Issue:** "installation succeeded" replaces "That's your signal — you're in" with a passive-construction confirmation. The second sentence ("Head to Configuration...") recovers some energy, but the confirmation itself is flat. A developer who has just completed a four-step install process deserves a moment that says "yes, that's it."

**Direction for rewriter:** The momentum here matters — the developer just completed four steps and is heading toward Configuration. The confirmation should carry that forward. Keep "Head to Configuration..." — that sentence is good. Fix the confirmation sentence.

---

### Fix 3 — Troubleshooting "Plugin not found" Symptom label (LOW priority)

**Current text (line 514):**
```
**Symptom:** `/plugin install jerry@jerry-framework` returns "plugin not found"
```

**Issue:** This is the only remaining entry in the Troubleshooting section using the `**Symptom:**` label. All other entries have dropped it. The inconsistency is more noticeable than the label itself. It reads as an assembly artifact — one entry that wasn't revised when the others were.

**Direction for rewriter:** Either (a) drop the label and fold the symptom description into the section header or opening sentence, consistent with every other troubleshooting entry in the revised document, or (b) restore the Symptom labels across all entries if the structured format is intentional. Inconsistency is the tell; either choice, made consistently, is fine.

---

### Fix 4 — Prerequisites section (LOW priority — unchanged from iteration 1)

**Note:** This section was not addressed in the iteration 2 revision. The iteration 1 finding stands: the "Don't have Claude Code yet?" blockquote is a warmth opportunity that remains generic. The document header voice ("Let's get you set up and shredding") still dies in this section.

**Direction for rewriter:** The "Don't have Claude Code yet?" note is the right place to add warmth — it is speaking directly to someone at step zero. See iteration-1-saucer-boy-voice.md Fix 4 for full guidance.

---

## H-15 Self-Review Check

- Each test was evaluated with specific textual evidence: confirmed.
- Test 1 was evaluated first and evaluation continued only because it passed: confirmed.
- Tests 2-5 evaluated in order with specific citations from the text: confirmed.
- Boundary conditions checked independently of the 5 tests: confirmed.
- Boundary #8 evaluated with llm-tell-patterns.md loaded: confirmed. Em-dash stacking, hedging phrases, formulaic transitions, parallel structure formulae, and ungrounded quantitative claims were scanned — none detected. Voice register drop detected at Verification endpoint. One isolated template artifact detected.
- Vocabulary reference loaded: no forbidden constructions detected.
- Suggested fixes are specific and actionable: confirmed.
- Voice gap comparison table provided to show iteration-over-iteration progress: confirmed.
- Regressions are reported directly without softening (P-022): confirmed. Two minor regressions documented.

---

## Session Context (sb-reviewer -> orchestrator)

```yaml
verdict: PASS
failed_test: null
boundary_violations: [8]
text_type: documentation
audience_context: onboarding
suggested_fixes_count: 4
boundary_8_severity: LOW  # Reduced from HIGH in iteration 1
regressions_introduced: 2  # "Jerry is now fully operational" and "installation succeeded"
gaps_closed: 3  # Configuration opening, Troubleshooting opener, Enable Hooks mid-section
note: >
  PASS with reduced voice gap. Three major improvements confirmed.
  Two minor regressions at instructional confirmation moments.
  Highest-priority fix: Verification endpoint close (Fix 1).
  Route to sb-rewriter for Fix 1 and Fix 2 before shipping.
  Fix 3 and Fix 4 are low-priority and can be batched.
```
