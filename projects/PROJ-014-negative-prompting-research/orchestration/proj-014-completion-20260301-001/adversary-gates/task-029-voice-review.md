# Voice Compliance Report

> **sb-reviewer** | v1.0.0 | 2026-03-01

## Summary

**Verdict:** PASS (all 5 tests) with one Boundary #8 advisory flag (NOT Mechanical Assembly — mild staccato pattern in closing, not disqualifying)
**Text Type:** celebration / project-completion announcement (Slack)
**Audience Context:** internal team, post-completion
**Expected Tone:** High energy, celebration, direct — Audience Adaptation Matrix row: "Session complete" (Energy: High, Humor: Yes, Technical Depth: None, Tone Anchor: Celebration). Justified deviation: medium technical depth retained because research findings are the substance of the celebration; stripping stats would remove the thing being celebrated.

---

## Authenticity Test Results

| Test | Name | Verdict | Evidence |
|------|------|---------|----------|
| 1 | Information Completeness | PASS | All key research outputs present: CONDITIONAL GO verdict, 270 tests, 100% NPT-013 compliance, 92.2% positive-only framing rate, 7.8% violation rate, McNemar exact p=0.016, three models (haiku/sonnet/opus), format string verbatim, performance comparison (beats bare NEVER and positive framing both), performance conditions (high-pressure + lower-capability models), 4 shipped items with specifics, links (TBD placeholder — appropriate for draft), call-to-action. No developer need goes unserved. |
| 2 | McConkey Plausibility | PASS | The spirit is direct, confident, and result-first. "PROJ-014 shipped. 270 tests. CONDITIONAL GO." leads with the fact, not the journey. "The format that wins" — no hedging on a finding the research earned. "never lost a single matchup" converts academic language into plain competitive claim. No strained ski references — the rewriter explicitly declined them and that judgment is correct. The voice reads as someone who believes the result, not someone performing enthusiasm about it. |
| 3 | New Developer Legibility | PASS | No McConkey references present. No ski culture decoding required. NPT-013, CONDITIONAL GO, McNemar p-value are technical/framework terms — they require framework knowledge, not persona knowledge. An internal team Slack reader can parse every sentence without knowing who Shane McConkey is. All format strings, model names, and feature references are explicit. |
| 4 | Context Match | PASS | High energy opening (italic three-part staccato: project, count, verdict). Confident body (stats stated without qualification). Active closing (imperative call-to-action). The rewriter's decision to retain medium technical depth in a research completion context is defensible: the data is the celebration content. Humor is correctly not deployed — per Humor Deployment Rules, "When in doubt, use direct language." The data lands harder than a ski metaphor would. Energy level matches celebration without becoming forced or caffeinated. |
| 5 | Genuine Conviction | PASS | "The format that wins" — declarative, no hedging. "never lost a single matchup" — competitive claim, earned by 270 tests. "The data says it matters" — closes from the evidence, not from performed confidence. The voice does not assemble enthusiasm; it reports a result with appropriate weight. The phrase "where it matters most" is slightly formulaic but is grounded immediately by the specific conditions it refers to (high-pressure scenarios, lower-capability models), preventing it from reading as hollow filler. |

*No tests were skipped. Test 1 passed, evaluation continued through all five tests.*

---

## Boundary Condition Check

| # | Boundary | Status | Evidence |
|---|----------|--------|----------|
| 1 | NOT Sarcastic | CLEAR | No mockery, no irony at anyone's expense. Humor is not deployed at all; the message is dry and direct. Nothing can be read as laughing at the developer or at the research process. |
| 2 | NOT Dismissive of Rigor | CLEAR | Rigor is the core content. 270 tests, McNemar exact p=0.016, 100% compliance across three models — the message leads with quality evidence. The quality system is presented as what produced the result, not as something the team had to endure. |
| 3 | NOT Unprofessional in High Stakes | CLEAR | Context is celebration, not governance failure or security event. Humor Deployment Rules table: "Celebrations (all items complete) — Full energy." No high-stakes context conflict. |
| 4 | NOT Bro-Culture Adjacent | CLEAR | Language is technically precise and inclusive. No exclusionary irony. No in-group markers that would alienate a new developer or any team member encountering this for the first time. |
| 5 | NOT Performative Quirkiness | CLEAR | The rewriter explicitly declined ski metaphors ("A forced ski metaphor would undercut the result"). The voice is dry and confident, not try-hard. No strained references, no emoji, no whimsy for its own sake. |
| 6 | NOT Character Override | CLEAR | This is a text artifact (Slack announcement). It modifies framework output voice, not Claude reasoning behavior. Boundary #6 does not apply to this text type. |
| 7 | NOT Information Replacement | CLEAR | Cross-checking: every number from the research is present. Voice elements (italic opener, "The format that wins," "never lost a single matchup," closing call-to-action) are additions layered over complete information, not substitutions for it. The plain text, stripped of all voice elements, fully serves the developer's informational need. |
| 8 | NOT Mechanical Assembly | ADVISORY | Two instances of staccato emphasis patterns detected via llm-tell-patterns.md scan. Neither is disqualifying on its own, but together they constitute a mild mechanical assembly signal in the closing. See Suggested Fixes. **Full scan:** Em-dash stacking — one pair in the body ("That gap — 7.8% violation rate, McNemar exact p=0.016 — held across..."), which is normal punctuation, not stacking. Corrective insertion — none. Hedging phrases — none. Formulaic transitions — none. Voice register drops — consistent direct/conversational register held throughout. Ungrounded quantitative claims — all numbers are grounded in PROJ-014 research output. Parallel structure formulae — "every constraint, every model, every scenario" is in a single clause (not three sentences); acceptable. **Flagged pattern:** The closing three sentences: "Try `/prompt-engineering` in your next session. Write better constraints in less time. The data says it matters." Three consecutive sentences under 10 words each, the third providing rhetorical amplification of the first two. This is a staccato emphasis pattern per the detection heuristic. The information is real, not repeated, but the three-part progressive structure reads slightly assembled. |

---

## Suggested Fixes

### Boundary #8 — Staccato Closing (Advisory)

**Current text:**
> Try `/prompt-engineering` in your next session. Write better constraints in less time. The data says it matters.

**Issue:** Three consecutive short sentences where the third provides rhetorical amplification rather than new information. The pattern matches the staccato emphasis tell from llm-tell-patterns.md: "back-to-back sentences under 8 words, where the second restates or amplifies the first."

**Fix options:**

Option A — Merge and add specificity (per llm-tell-patterns.md correction guidance):
> Try `/prompt-engineering` in your next session — it generates NPT-013 constraints on demand. The data already made the case.

Option B — Lead with the specific value, then close:
> Try `/prompt-engineering` in your next session. The format is already there; the skill writes it faster than you will.

Option C — Keep it short but make the third sentence do distinct work (not just amplify):
> Try `/prompt-engineering` in your next session. The constraint format is built in. You'll notice the difference on the first constrained prompt.

**Recommendation:** Option A. It retains the call-to-action energy, collapses two sentences into one with specificity added, and the closing "The data already made the case" is a genuine closer rather than a rhetorical amplification. It is shorter than the current three sentences and reads with more conviction.

**Priority:** Advisory only. The text passes all five Authenticity Tests and all eight boundary conditions at the threshold level. The staccato closing is a polish item, not a gate failure. Ship as-is or apply the fix — both are compliant.

---

## Session Context (for orchestrator)

```yaml
verdict: PASS
failed_test: null
boundary_violations: []
boundary_advisories: [8]
text_type: celebration-announcement
audience_context: internal-team-post-completion
suggested_fixes_count: 1
fix_priority: advisory
route_to: sb-calibrator
```

---

*Report generated by sb-reviewer v1.0.0*
*References loaded: SKILL.md (always), llm-tell-patterns.md (Boundary #8 evaluation), vocabulary-reference.md (vocabulary scan)*
*Constitutional Compliance: Jerry Constitution v1.0 (P-003, P-020, P-022)*
