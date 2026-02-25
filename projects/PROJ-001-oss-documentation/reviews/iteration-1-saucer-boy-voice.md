# Voice Compliance Report

> **Report:** sb-reviewer iteration-1 — INSTALLATION.md voice compliance
> **Requested energy level:** "More Saucer Boy"
> **Agent:** sb-reviewer v1.0.0
> **Date:** 2026-02-25

## Summary

**Verdict:** PASS with significant voice gap findings
**Text Type:** documentation
**Audience Context:** onboarding
**Expected Tone:** Medium energy, warm humor, invitation — "the system is learnable"

The document passes all 5 Authenticity Tests. It will not mislead a developer, it does not strain the persona, and every section is legible without ski-culture context. However, "PASS" here means "no blockers to shipping." It does not mean "this document has the Saucer Boy voice the user requested." The document has a voice gap — a substantial one. The McConkey energy peaks in the header and first few sections, then drains almost entirely through the middle and lower thirds. The result is an uneven document that feels like two different writers. The boundary condition scan found one clear mechanical assembly flag (Boundary #8) and one minor formulaic transition cluster.

The user asked for "More Saucer Boy." The report identifies exactly where that energy lives, where it goes missing, and which sections have the highest return on voice investment.

---

## Authenticity Test Results

| Test | Name | Verdict | Evidence |
|------|------|---------|----------|
| 1 | Information Completeness | PASS | All sections contain complete technical information. Prerequisites, install steps, hook setup, configuration, verification, troubleshooting, and uninstallation are all actionable without voice elements. No information gaps. |
| 2 | McConkey Plausibility | PASS | The voice that is present is plausible. "Two commands and you're riding," "Let it rip," "you're shredding," and "Clean slate" are all in-spirit without strain. No section overreaches. The concern is not false notes — it is silence. |
| 3 | New Developer Legibility | PASS | Every skiing metaphor in the document is transparent. "Riding," "shredding," "take Jerry for a lap," "drop in" — all self-explanatory from context. No reference requires ski-culture knowledge to decode. |
| 4 | Context Match | PASS (with gap) | The opening and Using Jerry sections hit the right energy for onboarding: warm, inviting, light. However, the Troubleshooting section, Configuration section, and Uninstallation section drop to a tone that reads as generic technical documentation — well below the "medium energy, warm" target for onboarding context. The matrix calls for "invitation — the system is learnable" throughout, not just at the entry points. |
| 5 | Genuine Conviction | PASS (with gap) | Where the voice is present it reads as believed, not assembled. "That's your signal — you're in" and "Let it rip" land as genuine. The Troubleshooting section's "Check these in order" and the Configuration section's step-by-step lists feel procedural without a person behind them. The conviction is intermittent, not sustained. |

---

## Boundary Condition Check

| # | Boundary | Status | Evidence |
|---|----------|--------|----------|
| 1 | NOT Sarcastic | CLEAR | No mockery detected. All tone is inclusive. |
| 2 | NOT Dismissive of Rigor | CLEAR | Quality and security notes are handled with appropriate gravity. The early-access caveat for hooks is appropriately serious. |
| 3 | NOT Unprofessional in High Stakes | CLEAR | The security note in the hooks section ("The commands below download and execute a script...") is entirely humor-free and direct. Correct. |
| 4 | NOT Bro-Culture Adjacent | CLEAR | "The whole crew gets Jerry" is the closest thing to crew-culture language. It reads as welcoming rather than exclusionary — the reference is to the team, not to an in-group. |
| 5 | NOT Performative Quirkiness | CLEAR | The ski vocabulary is restrained. No emoji overload, no strained whimsy. The voice that is present does not try too hard. |
| 6 | NOT Character Override | CLEAR | The document governs framework output language only. No behavioral instructions to Claude. |
| 7 | NOT Information Replacement | CLEAR | Every personality marker is additive. "Two commands and you're riding" does not replace the two commands. |
| 8 | NOT Mechanical Assembly | FLAGGED | See detail below. |

### Boundary #8 Detail — Mechanical Assembly

Two specific patterns detected:

**Pattern 1 — Voice register drop (Structural Tell, High severity):**
The document opens at a conversational energy level that the voice reference confirms is on-persona. By the Troubleshooting section, the register shifts to a clinical diagnostic format: "Check these in order:", numbered fix lists with bolded symptom headers, and zero personality. This is a textbook voice register drop — conversational introduction, procedural middle, no recovery. The Troubleshooting section is the longest section in the document, which means the voice drains exactly when the developer most needs the warmth signal that the system is learnable. This does not fail Test 1 (information is present) but it does trip Boundary #8.

**Pattern 2 — Parallel structure formulae (Structural Tell, Medium severity):**
The Troubleshooting section contains multiple entries that follow an identical structural pattern: bolded symptom title, "Symptom:" in italics, "Cause:" in italics, "Fix (choose one):" or "Check these in order:". This is a documentation template, not a voice. Six consecutive entries using the same header pattern read as machine-generated even when the information is accurate.

The Capability Matrix and Document Sections table are appropriately functional — tables should be tables. The issue is the flowing text within Troubleshooting, not the structural tables throughout the document.

---

## Voice Gap Analysis — Where the Energy Lives and Where It Dies

This section maps the document's voice distribution for sb-rewriter prioritization.

### Sections with Saucer Boy voice present

| Section | Voice Evidence | Energy Level |
|---------|---------------|-------------|
| Document header | "Let's get you set up and shredding." | Medium-High |
| Which Install Method? | "Pick the line that fits." | Medium |
| Install from GitHub | "Two commands and you're riding." / "That's your signal — you're in." | Medium |
| Plugin Dir Flag | "Take Jerry for a lap before committing." | Medium |
| Verification (Skill test) | "Let it rip." / "You're shredding." | Medium-High |
| Using Jerry | "Let it rip." / "Each skill guides you through what it needs." | Medium |
| Uninstallation | "Clean slate." | Low-Medium |

### Sections where the voice goes dark

| Section | Current register | Gap vs. matrix target | Investment return |
|---------|-----------------|----------------------|------------------|
| Prerequisites | Functional tables plus informational blockquotes. No persona. | Medium — target is warm invitation | Medium |
| Enable Hooks | Opens well ("They need uv. It takes 30 seconds."), then the hook table and uv install section are procedural without warmth. | Low-Medium gap in hook table; higher in install block | Medium |
| Configuration | Step-by-step instructions with zero personality. The framing "This is where Jerry goes from installed to yours" is the only warm moment. | Significant — this is a key onboarding moment | High |
| Verification | Plugin and hooks verification sub-sections are procedural lists; the Skill test sub-section has the document's best voice moment. | Medium | Medium |
| Troubleshooting | Longest section. Entirely clinical. Symptom/Cause/Fix diagnostic format with no person behind it. | Highest gap in the document | High |
| Getting Help | One warm line ("The docs get better when you tell us where they fall short.") followed by a link list. | Low gap — brief section, link lists are fine | Low |
| Developer Setup | Appropriately minimal — this section serves contributors, not onboarding developers. Minimal voice is correct here. | None — context is right | None needed |

---

## Suggested Fixes

Each fix is scoped, specific, and ordered by return on investment. These are findings for sb-rewriter, not rewrites.

### Fix 1 — Configuration section opening (HIGH priority)

**Current:** "This is where Jerry goes from installed to yours. Jerry uses project-based workflows to organize your work — think of a project as a workspace where your research, decisions, and work items accumulate over time. Most skills require an active project — without one, you'll see `<project-required>` messages instead of skill output. Set this up now so verification goes smoothly."

**Issue:** The first sentence is the best voice moment in the section. Then the second sentence goes academic (em-dash parenthetical, passive accumulation phrasing). By the third sentence it has dropped to warning-label territory. The onboarding audience needs warmth and invitation here — this is the step where developers learn Jerry's operating model for the first time. The current text treats it as a prerequisite to check off.

**Direction for rewriter:** The conviction to work from is: projects are not bureaucracy — they are how Jerry builds institutional memory for the developer. The explanation of `<project-required>` needs to stay (Test 1), but it can be delivered with warmth. The em-dash parenthetical in sentence 2 can become its own sentence.

---

### Fix 2 — Troubleshooting section voice (HIGH priority)

**Current:** Six problem entries in identical Symptom/Cause/Fix template format, with bolded headers but no human voice connecting them.

**Issue:** This is the document's largest voice gap and the highest-stakes onboarding moment. A developer in troubleshooting mode is frustrated. The current format treats them like a tier-1 support ticket. The audience-adaptation note for onboarding specifically calls for: "The rigor of the system can be intimidating. The voice should lower that barrier."

**Direction for rewriter:** The Symptom/Cause/Fix structure is fine as an organizer — keep it. What is missing is a human at the top of the section acknowledging that installation has rough edges. One direct sentence before the list would change the register significantly. Within each entry, "Check these in order:" and "Fix (choose one):" can stay operational, but the cause descriptions can be warmed. "Claude Code uses SSH to clone the repository when you use the `owner/repo` shorthand" is accurate but cold — same information can be delivered with a collaborator's voice.

---

### Fix 3 — Enable Hooks section mid-section voice drop (MEDIUM priority)

**Current:** The section opens strong: "Skills work the moment you install. Hooks are the next level — they keep Jerry dialed across your entire session..." Then the hook table is functional-only, and the uv install instructions drop to pure procedure.

**Issue:** The opening sets a medium-energy tone, then the section goes quiet for ~40 lines. The "Install uv" sub-section's security note is correctly humor-free (Boundary #3). But the surrounding text can hold the warmth without touching the security note.

**Direction for rewriter:** The uv install steps themselves should stay clean — platform-specific commands need to be clear. The text around those commands (transitions, post-install confirmation) has room for the persona. "That's it. Once uv is installed, hooks activate automatically the next time you start Claude Code." — this is already good. The gap is the text leading into it.

---

### Fix 4 — Prerequisites section (LOW priority)

**Current:** Table of prerequisites, then three sequential blockquotes with SSH and version information. All informational, no voice.

**Issue:** This is the first content section after the document header. The header voice ("Let's get you set up and shredding") dies here. The blockquote for "Don't have Claude Code yet?" is a missed warmth moment — it is directed at someone who just found Jerry and does not yet have the base tool.

**Direction for rewriter:** The "Don't have Claude Code yet?" note is the right place to add warmth — it is speaking directly to someone at step zero. The table and SSH note need to stay precise (high technical stakes, Test 1). The Claude Code callout can be warmer without touching accuracy.

---

### Fix 5 — Boundary #8 structural tell in Troubleshooting (MEDIUM priority, see Boundary #8 above)

**Current:** Six consecutive entries in identical format: bolded problem header, italic Symptom/Cause/Fix labels, numbered fix list.

**Issue:** This structural pattern reads as assembled from a template rather than written. The information is complete (Test 1 clear), but the repetition across six entries creates a hollow mechanical feel.

**Direction for rewriter:** Vary the structural openers across entries. Not every entry needs "Symptom:" — some problems are self-evident from the header. Not every fix list needs "Fix (choose one):" — some have one obvious fix. Collapsing the template markers where they add nothing would reduce the mechanical tell without losing any information.

---

## H-15 Self-Review Check

- Each test was evaluated with specific textual evidence: confirmed.
- Test 1 was evaluated first and evaluation continued only because it passed: confirmed.
- Tests 2-5 evaluated in order with specific citations from the text: confirmed.
- Boundary conditions checked independently: confirmed.
- Boundary #8 was evaluated with LLM-tell patterns reference loaded: confirmed.
- Vocabulary reference loaded and scanned: no forbidden constructions detected in the document.
- Suggested fixes are specific and actionable: confirmed.
- Violations are not softened: the voice gap finding is reported directly. The "PASS" verdict is accurate but the gap analysis makes clear this is not the energy level the user requested.

---

## Session Context (sb-reviewer -> orchestrator)

```yaml
verdict: PASS
failed_test: null
boundary_violations: [8]
text_type: documentation
audience_context: onboarding
suggested_fixes_count: 5
voice_gap_sections: [Configuration, Troubleshooting, EnableHooks_mid, Prerequisites]
note: "PASS means no blockers. Does not mean energy target is met. User requested 'More Saucer Boy' — route to sb-rewriter with Fix 1 (Configuration) and Fix 2 (Troubleshooting) as highest-priority targets."
```
