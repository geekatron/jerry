# Voice Compliance Report

> **Report:** sb-reviewer iteration-3 — INSTALLATION.md voice compliance
> **Prior Reviews:**
> - Iteration 1: `docs/reviews/iteration-1-saucer-boy-voice.md` — PASS with significant voice gap findings
> - Iteration 2: `docs/reviews/iteration-2-saucer-boy-voice.md` — PASS, 2 minor regressions flagged (endpoint close, Step 4 confirmation)
> **Agent:** sb-reviewer v1.0.0
> **Date:** 2026-02-25

## Summary

**Verdict:** PASS
**Text Type:** documentation
**Audience Context:** onboarding
**Expected Tone:** Medium energy, warm humor, low technical depth, tone anchor = Invitation — "the system is learnable"

Both regressions flagged in iteration 2 have been fixed. The Verification endpoint now closes with "That's the whole crew reporting for duty. You're live." — earned energy, right register. Step 4 now reads "If `jerry` appears, you're in." — direct, confident, the missing warmth restored. Boundary #8 LOW severity flag from iteration 2 is CLEARED: the isolated `**Symptom:**` label in the "Plugin not found" entry has been resolved. All five Authenticity Tests pass.

The new callout boxes added since iteration 2 are the primary focus of this review. The verdict on them is mostly positive: the boxes are informational and accurate, the voice is functional and mostly consistent, and none fail Test 1. However, there is one specific voice concern that warrants tracking: the **HTTPS context box** and the **SSH check extension** carry a noticeably more formal register than the surrounding prose — technically correct but warmer opportunities missed. Two new minor Boundary #8 patterns have been introduced in the new content, both LOW severity.

The document is shippable. The new content integrates cleanly into the information structure. Voice investment for the next iteration is optional, not required.

---

## Regression Check: Iteration 2 Open Items

| Item | Iteration 2 Status | Current Text | Resolved? |
|------|-------------------|--------------|-----------|
| Verification endpoint (Fix 1 — HIGH priority) | "Jerry is now fully operational" — under-energy close | "That's the whole crew reporting for duty. You're live." (line 404) | YES — CLOSED |
| Step 4 confirmation (Fix 2 — MEDIUM priority) | "installation succeeded" — passive construction | "If `jerry` appears, you're in." (line 128) | YES — CLOSED |
| "Plugin not found" Symptom label (Fix 3 — LOW) | Isolated `**Symptom:**` label remained | Label not present in current entry (line 544–550) | YES — CLEARED |
| Prerequisites section warmth (Fix 4 — LOW, unchanged from iter 1) | "Don't have Claude Code yet?" blockquote still generic | "No worries — install it first... We'll be here when you get back." (line 46) | YES — CLOSED (new warmth added) |

All four open items from iteration 2 are resolved. Net: zero regressions carried forward from prior iterations.

---

## Authenticity Test Results

| Test | Name | Verdict | Evidence |
|------|------|---------|----------|
| 1 | Information Completeness | PASS | See detail below. |
| 2 | McConkey Plausibility | PASS | See detail below. |
| 3 | New Developer Legibility | PASS | See detail below. |
| 4 | Context Match | PASS | See detail below. |
| 5 | Genuine Conviction | PASS | See detail below. |

*All five tests evaluated. Test 1 passed; evaluation continued to Tests 2-5.*

### Test 1 — Information Completeness (HARD Gate)

All new callout boxes are informational and complete. Scanning each new element:

- **Network access box** (line 42): Names both services (`github.com`, `astral.sh`), names the exception path (air-gapped), cross-links to the section. Actionable without voice elements.
- **SSH context box** (line 44): Explains the `owner/repo` → SSH default, names the error message, names the fix (HTTPS URL). A developer who hits "Permission denied (publickey)" before reading this box will find the explanation complete when they do reach it.
- **Don't have Claude Code yet?** (line 46): Names the resource, gives timing ("Takes a few minutes"), closes with presence. No information gap.
- **Version check box** (line 48): Names the version requirement, names the command to check, names the action if the command is unrecognized. Complete.
- **SSH username check extension** (line 63): The expanded `ssh -T git@github.com` callout now includes username verification — "If you see `Hi <username>!` and `<username>` is your GitHub account, you have SSH set up. If the username is unexpected..." This is new content since iteration 2. The unexpected-username case is explained with clear action (use HTTPS). Actionable.
- **Variable notation in Step 3** (lines 106–118): The restructured step uses `<name-from-step-2>` as the variable placeholder and provides the resolved example immediately after. A developer cannot get stuck between the variable and the resolved form. Complete.
- **Hooks verification inline callout** (line 394): "That's Jerry loading your project context and getting ready to ride." This is a confirmatory sentence, not a callout box, but it names the mechanism (SessionStart hook, `<project-context>` tag). Sufficient.
- **JERRY_PROJECT verification box** (line 362): Names the verification command per platform, names the success condition, names the failure conditions (saved the profile, using the correct shell). Complete.
- **Launch order matters box** (line 364): Explains why order matters (environment variable inheritance), names the action (set JERRY_PROJECT before launching Claude Code), names the recovery (restart from a terminal where variable is set). Complete.
- **Don't have a repository yet?** (line 376): Provides the commands, names what Jerry requires (any directory, not an existing codebase). Complete.
- **Air-gapped install section** (lines 286–293): Three-step procedure, names the network dependency for uv, provides the fallback (GitHub releases binary). Complete.
- **Uninstall source-name note** (lines 637, 645, 647): Both uninstall steps include "Not sure of the source name? Run `/plugin marketplace list`." Actionable.

**PASS — No information gaps detected in new content.**

### Test 2 — McConkey Plausibility

Voice elements present in the new content:

- "We'll be here when you get back." (line 46) — warm, patient, not condescending. Plausible.
- "Pick whichever command matches your setup — both do the same thing." (line 81) — direct, no unnecessary explanation of why. Plausible.
- "That's Jerry loading your project context and getting ready to ride." (line 394) — the "getting ready to ride" ending is light and earned; it is the hooks verification payoff. Plausible.
- "That's the whole crew reporting for duty. You're live." (line 404) — this is the iteration 2 regression fix. Direct energy, grounded, no strain. Plausible.
- "If `jerry` appears, you're in." (line 128) — the iteration 2 regression fix. Confident, terse, no ceremony. Plausible.

The SSH context box and network access box carry a neutral-functional register. No voice is present, but no voice is strained either. They are documentation-register, not Saucer Boy register — a finding for Test 4, not Test 2.

**PASS — No overreach detected. Voice present is in-spirit.**

### Test 3 — New Developer Legibility

New skiing vocabulary introduced since iteration 2:

- "getting ready to ride" (line 394) — self-explanatory from context (the hook is loading project context). A developer with no skiing background reads this as "getting ready to go." Transparent.

No new opaque skiing references introduced. All prior transparent references remain transparent.

The variable placeholder notation `<name-from-step-2>` and the resolved example immediately following it (lines 106–118) are clear without any domain knowledge.

**PASS — All new content legible without ski-culture context.**

### Test 4 — Context Match

New callout boxes are technical-informational in register, matching the expected tone for their content type:

- Security/network callouts (network access, SSH context): appropriately neutral. The Audience Adaptation Matrix assigns "Routine informational" context a low energy, efficient tone anchor — these fit.
- Warmth callouts (Don't have Claude Code yet?, We'll be here when you get back): medium energy, warm — correct for onboarding context.
- Verification endpoint (That's the whole crew reporting for duty. You're live.): medium energy, warm — the Audience Adaptation Matrix's onboarding row calls for medium energy with warm humor. This lands correctly.
- Hooks verification ending (getting ready to ride): light-medium — correct for a confirmation moment.

One mild observation: the **air-gapped install section** and **version pinning section** are appropriately dry. They serve developers in restricted environments where efficiency matters more than warmth. Correct register for that sub-audience.

**PASS — Energy calibration appropriate throughout new content.**

### Test 5 — Genuine Conviction

"We'll be here when you get back." — this reads as believed, not performed. The "we" is inclusive and grounded.

"That's the whole crew reporting for duty. You're live." — conviction is present. The collaborator voice is genuine at the endpoint.

"If `jerry` appears, you're in." — terse and direct. No ceremony, no performance. Believed.

"Pick whichever command matches your setup — both do the same thing." — the "both do the same thing" is reassurance from someone who has fielded this question before. Conviction-first.

The SSH context box ("When you add a plugin source using the `owner/repo` shorthand...") reads as accurate explanation rather than voice. It does not fail conviction — it simply has no conviction to evaluate. The information is precise and trustworthy.

**PASS — No assembled or performed voice detected in new content.**

---

## Boundary Condition Check

| # | Boundary | Status | Evidence |
|---|----------|--------|----------|
| 1 | NOT Sarcastic | CLEAR | No mockery detected. All tone is inclusive. New callout boxes are direct without condescension. |
| 2 | NOT Dismissive of Rigor | CLEAR | Network security callout ("The commands below download and execute a script from astral.sh") remains humor-free and direct. Air-gapped install section appropriately serious. |
| 3 | NOT Unprofessional in High Stakes | CLEAR | Security-relevant content (uv script inspection, network requirements) carries no humor. Correct. |
| 4 | NOT Bro-Culture Adjacent | CLEAR | "The whole crew reporting for duty" — crew reference is inclusive (the skill agents), not exclusionary. No language that would make a new or female developer feel excluded. |
| 5 | NOT Performative Quirkiness | CLEAR | "Getting ready to ride" and "You're live" are restrained. No emoji, no strained whimsy. |
| 6 | NOT Character Override | CLEAR | Document governs framework installation language only. No behavioral instructions to Claude. |
| 7 | NOT Information Replacement | CLEAR | All voice elements additive. "You're in" follows the conditional check, not replacing it. "We'll be here when you get back" follows the external link, not replacing it. |
| 8 | NOT Mechanical Assembly | FLAGGED (LOW) | See detail below. |

### Boundary #8 Detail — Mechanical Assembly

**Status vs. Iteration 2:** The HIGH and LOW severity patterns flagged in iteration 2 are cleared. The isolated `**Symptom:**` label is gone. The Verification endpoint has been fixed ("You're live" replaces "fully operational"). The Step 4 confirmation has been fixed ("you're in" replaces "installation succeeded"). Boundary #8 was reduced to LOW severity in iteration 2; two new LOW severity patterns have been introduced in new content. Net severity: LOW, same as iteration 2.

**New Pattern 1 — Callout box register uniformity (Low severity):**

Six of the new callout boxes follow a structural template: bold header in quotes, explanation, named action/fix. This is the correct format for callout boxes — and individually each box is fine. The concern is that six boxes in the Prerequisites and Install from GitHub sections all share an identical internal structure: "Bold title? When condition, consequence. Fix: action." The uniformity is visible when the boxes stack (lines 42–48, then 73–78, then 90, 102, 120). This is a Low severity observation — the format is appropriate for the content type, and the alternative (varying callout structure) could hurt usability. Noting it as an assembly signal, not as a failure.

**New Pattern 2 — SSH context box register drop (Low severity):**

The SSH context box (line 44) explains the `owner/repo` → SSH default behavior in a functional, accurate register. Within the box, the sentence "Even though Jerry's repo is public, the `owner/repo` format defaults to SSH" is a mild register shift toward a technical-explainer voice. The phrase "The fix is simple:" immediately follows as a softener, which partially compensates. This is not a failure — the information is high-stakes enough (permission denied errors) to justify prioritizing clarity over warmth. The gap between the "Don't have Claude Code yet? No worries — install it first... We'll be here when you get back" box (warm, human) and the SSH context box (neutral, technical) is noticeable when reading them in sequence. Not flagged as a fix — noted as a design seam.

**Cleared patterns from iteration 2:**
- Isolated `**Symptom:**` label in "Plugin not found" entry: CLEARED
- Voice register drop at Verification endpoint ("Jerry is now fully operational"): CLEARED
- Passive construction at Step 4 confirmation ("installation succeeded"): CLEARED

No em-dash stacking detected in new content. No hedging phrases ("it's worth noting," "importantly") detected. No formulaic transitions detected. No parallel structure formulae (three consecutive same-opening sentences) detected. No ungrounded quantitative claims detected.

---

## Voice Gap Comparison — Iteration 2 vs. Iteration 3

| Section | Iteration 2 Gap Level | Iteration 3 Gap Level | Change |
|---------|----------------------|----------------------|--------|
| Verification endpoint | Under-energy ("fully operational") | Closed — "You're live" | Improved (regression fixed) |
| Step 4 confirmation | Passive construction ("installation succeeded") | Closed — "you're in" | Improved (regression fixed) |
| "Plugin not found" Symptom label | Low — one isolated template artifact | Cleared | Improved |
| Prerequisites warmth ("Don't have Claude Code yet?") | Low-Medium gap (generic) | Closed — "We'll be here when you get back" | Improved |
| New callout boxes (6 new) | Not present | Functional-accurate; minor register seam in SSH box | Stable (no gap, mild observation) |
| Troubleshooting | Improved from iteration 1, stable | Unchanged — same level as iteration 2 | Unchanged |
| Air-gapped install, version pinning | New sections | Appropriately dry for restricted-environment sub-audience | Correct register |

Net: Four open items from iteration 2 closed, zero regressions introduced, two LOW severity assembly observations noted in new content.

---

## Suggested Fixes

The document is shippable without any of the following. These are ordered by return on investment for future iteration, if one occurs.

### Fix 1 — SSH context box warmth (LOW priority — optional)

**Current text (line 44):**
```
When you add a plugin source using the `owner/repo` shorthand (e.g., `geekatron/jerry`), Claude Code clones the repository via SSH. Even though Jerry's repo is public, the `owner/repo` format defaults to SSH. If you don't have SSH keys configured for GitHub, you'll see "Permission denied (publickey)." The fix is simple: use the full HTTPS URL instead. Both commands do the same thing. See [Install from GitHub](#install-from-github) for both options side by side.
```

**Observation:** This box prioritizes accuracy over warmth, correctly — the error message being explained ("Permission denied (publickey)") is a developer frustration point that warrants a precise answer. However, "Even though Jerry's repo is public" carries a mild explanatory register that contrasts with the surrounding document voice. The close ("Both commands do the same thing") is good — direct, reassuring.

**Direction for rewriter (if pursued):** The opening sentence can be tightened without losing precision. "Even though Jerry's repo is public" is defensive phrasing; drop it and go straight to the behavior. The information is complete either way.

---

### Fix 2 — Callout box density in Prerequisites (LOW priority — optional)

**Current state:** Four callout boxes stack in the Prerequisites section (lines 42–48), followed by three more in the Install from GitHub header (lines 73–78). Seven consecutive callout boxes before reaching the first step creates a reading pattern where the developer learns to skim them.

**Observation:** This is not a voice problem — it is a document structure observation. The information in each box is necessary. The density may reduce the signal value of individual boxes.

**Direction (if pursued):** Consider consolidating the SSH-related boxes (Prerequisites SSH row + "Why does SSH come up?" box) since they serve the same developer question. The SSH context could be folded into the Prerequisites table row directly, reducing the box count. This is a content organization question, not a voice question. Route to documentation review, not sb-rewriter.

---

## H-15 Self-Review Check

- Each test was evaluated with specific textual evidence: confirmed.
- Test 1 was evaluated first and was the only test that could have halted evaluation: confirmed.
- Tests 2-5 evaluated in order with citations from the specific new content: confirmed.
- Boundary conditions checked independently of the 5 tests: confirmed.
- Boundary #8 evaluated with `llm-tell-patterns.md` loaded: confirmed. Em-dash stacking, hedging phrases, formulaic transitions, parallel structure formulae, and ungrounded quantitative claims were scanned — none detected in new content. Two LOW severity structural observations noted (callout box format uniformity, SSH box register seam).
- Vocabulary reference loaded and scanned: no forbidden constructions detected in new content.
- Iteration 2 regressions verified as resolved with specific line citations: confirmed.
- Suggested fixes are specific and actionable (or explicitly marked optional): confirmed.
- Voice gap comparison table provided for iteration-over-iteration tracking: confirmed.
- Violations are not softened (P-022): the LOW severity Boundary #8 patterns are reported directly. The "shippable" verdict is accurate and does not hide the LOW severity observations.

---

## Session Context (sb-reviewer -> orchestrator)

```yaml
verdict: PASS
failed_test: null
boundary_violations: [8]
text_type: documentation
audience_context: onboarding
suggested_fixes_count: 2
boundary_8_severity: LOW  # Same as iteration 2; different specific patterns; both new and LOW
regressions_introduced: 0
gaps_closed: 4  # Verification endpoint, Step 4 confirmation, Symptom label, Prerequisites warmth
iteration_2_open_items_resolved: 4/4
note: >
  PASS with no blockers. All four iteration-2 open items resolved.
  Two new LOW severity Boundary #8 observations in new callout box content.
  Both suggested fixes are optional — document is shippable as-is.
  No further sb-rewriter routing required unless iteration 4 is explicitly scoped.
```
