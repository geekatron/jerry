# Voice Compliance Report

> **Report:** sb-reviewer iteration-4 — INSTALLATION.md voice compliance
> **Prior Reviews:**
> - Iteration 1: `docs/reviews/iteration-1-saucer-boy-voice.md` — PASS with significant voice gap findings
> - Iteration 2: `docs/reviews/iteration-2-saucer-boy-voice.md` — PASS, 2 minor regressions flagged
> - Iteration 3: `docs/reviews/iteration-3-saucer-boy-voice.md` — PASS, 2 LOW severity Boundary #8 observations, shippable
> **Agent:** sb-reviewer v1.0.0
> **Date:** 2026-02-25

## Summary

**Verdict:** PASS
**Text Type:** documentation
**Audience Context:** onboarding
**Expected Tone:** Medium energy, warm, low technical depth, tone anchor = Invitation — "the system is learnable"

All seven content changes evaluated. All five Authenticity Tests pass. No regressions introduced from iteration 3. The new content is uniformly functional-accurate — it adds information without adding voice, which is the correct tradeoff for the changes made: these are precision corrections and navigational improvements, not voice moments. None of the new content attempts personality and fails; it simply does not attempt personality, which is acceptable given what each change is doing.

One Boundary #8 observation from iteration 3 has been partially resolved: the "Plugin not found" entry, previously flagged for its `**Symptom:**` label (cleared in iteration 3) and its inline-blockquote positioning, is now a `###` heading with a dedicated troubleshooting paragraph. The structural improvement is genuine. One new LOW severity Boundary #8 pattern is introduced in the source-name variability notes (three consecutive entries with identical phrasing). Severity matches iteration 3 (LOW). Document remains shippable.

---

## Regression Check: Iteration 3 Open Items

| Item | Iteration 3 Status | Current Text | Resolved? |
|------|-------------------|--------------|-----------|
| SSH context box warmth (Fix 1 — LOW, optional) | "Even though Jerry's repo is public" — mildly defensive register | Unchanged (line 44) | NO — carried forward, still LOW, still optional |
| Callout box density in Prerequisites (Fix 2 — LOW, optional — content org question, not voice) | 7 stacked callout boxes; density reduces signal value | Unchanged — structure not revised | NO — carried forward, content-org note not voice |

Both iteration 3 items were explicitly marked optional and not required for shipping. Neither has been addressed; neither constitutes a regression. Carrying forward as unchanged observations.

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

Evaluating each new element with voice elements removed:

**Interactive Installation caveat — anchor links added (lines 144, 146):**
Previously referenced "Step 1 above" without a link. Now: "complete [Step 1](#install-from-github) above." The callout explains why Jerry won't appear in the Discover tab (community plugin, not in official catalog) and gates the instruction on Step 1 completion. The anchor link makes the cross-reference navigable rather than implicit. Information was already complete; the anchor improves discoverability. PASS.

**"Plugin not found" in Step 3 — references Step 2 (line 120):**
Previously: "The source name must match exactly what `/plugin marketplace list` shows." (general instruction, no anchor). Now: "Re-run Step 2 and copy the name from the output." The specific step reference replaces the generic instruction. A developer who hits the error now has a named action (re-run Step 2) rather than a procedure they must infer. Complete and more actionable than prior iteration. PASS.

**"Plugin not found" in Local Clone Step 3 — troubleshooting link added (line 272):**
"See [Plugin not found](#plugin-not-found-after-adding-source) in Troubleshooting." The Local Clone path now routes to the full troubleshooting entry rather than containing a redundant fix inline. The link target (line 544) is a complete `###` section with full diagnostic steps. No information gap — the linked section contains all necessary steps. PASS.

**Updating section — source-name variability note (lines 615, 631, 643):**
Three `**Source name differs?**` notes added:
- GitHub users: "Use the name from `/plugin marketplace list`: `/plugin marketplace update <name-from-list>`." (line 615) — names the command, names the variable, provides resolved syntax. Complete.
- Local clone: "Use the name from `/plugin marketplace list`." (line 631) — shorter form; the full `/plugin marketplace update` command is on line 628. The adjacent command block provides the syntax; the note provides the variable substitution instruction. Complete.
- Uninstall: "Use the name from `/plugin marketplace list`: `/plugin uninstall jerry@<name-from-list>`." (line 643) — names the command, names the variable. Complete.

All three notes are actionable without voice elements. PASS.

**JERRY_PROJECT format consequence (line 348):**
"If you use a different format (e.g., `my-project` instead of `PROJ-001-my-project`), you'll see `<project-error>` messages." Previous text explained the format but did not document the consequence of a format violation. The new sentence closes that gap: developer knows what happens, not just what the format is. PASS.

**Windows Local Clone path corrected (lines 258-260):**
"`/plugin marketplace add C:/Users/YOUR_USERNAME/plugins/jerry`" with "Replace `YOUR_USERNAME` with your actual Windows username. To find the full path, run `echo $env:USERPROFILE` in PowerShell." The placeholder `YOUR_USERNAME` is now explained with a concrete lookup command. A Windows developer who does not know their username has an actionable path. PASS.

**.gitignore concrete command (line 378):**
"If you don't have a `.gitignore` yet: `echo '.jerry/' >> .gitignore`." Previously: "do not commit it" with no `.gitignore` guidance for new developers. The concrete command removes inference. PASS.

**"Plugin not found" promoted to `###` heading (line 544):**
`### Plugin not found after adding source` — now a navigable section with a full paragraph entry (lines 544-552). The Local Clone path's `[Plugin not found](#plugin-not-found-after-adding-source)` anchor link is now valid because the target heading exists. Previously this was an inline blockquote; now it is a first-class troubleshooting entry. PASS.

**Overall Test 1 verdict: PASS — No information gaps in any new content. Several gaps from prior iterations closed.**

### Test 2 — McConkey Plausibility

The new content introduces no voice elements — no skiing vocabulary, no personality markers, no humor. This is correct for the changes made: these are precision corrections (format consequence, path fix, `.gitignore` command) and navigational improvements (anchor links, heading promotion). Functional-accurate language is appropriate here.

No overreach detected because there is nothing to overreach with. The absence of voice in these additions does not fail Test 2 — the test asks whether voice present is plausible, not whether voice is present.

The one passage adjacent to new content that does carry voice — "Pick any slug that describes your work (e.g., `PROJ-001-my-api`)" (line 348) — is direct and warm without strain. The em-dash in "and it matters — Jerry's CLI and hooks validate this pattern" is a single em-dash functioning as a normal emphasis connector (not stacked). Plausible.

**PASS — No strained voice detected. Absence of voice in precision-correction content is correct.**

### Test 3 — New Developer Legibility

No skiing vocabulary introduced in the new content. All new content is plain technical English. The `PROJ-{NNN}-{slug}` format notation (line 348) is a standard placeholder convention that does not require domain knowledge. The `YOUR_USERNAME` placeholder (line 258) is similarly universal.

The troubleshooting section heading "Plugin not found after adding source" (line 544) is unambiguous without any framework or skiing context.

**PASS — All new content legible without domain knowledge.**

### Test 4 — Context Match

The Audience Adaptation Matrix for onboarding context: medium energy, warm, low technical depth, tone anchor = invitation — "the system is learnable."

The new content is functional-accurate in register throughout. For the specific change types:
- Anchor links, heading promotions, and cross-references: these are structural improvements, not text with a register. Not evaluated against energy level.
- Format consequence note (line 348): correctly low energy for a "by the way, this matters" note within a step. The "and it matters" construction gives it a slight warmth without overplaying. Correct for a cautionary aside.
- Windows path fix (lines 258-260): appropriately instructional. "To find the full path, run..." is direct and helpful. Correct register for a practical instruction.
- `.gitignore` command (line 378): inline and concise. "If you don't have a `.gitignore` yet:" is friendly phrasing for what could be a bare instruction. Correct register.
- Source-name variability notes (Updating and Uninstallation): routine informational. The Audience Adaptation Matrix assigns this context low energy, efficient tone. The `**Source name differs?**` construction is direct without warmth, which matches the low-energy efficient anchor for Updating and Uninstallation contexts.

**PASS — All new content registers correctly against the Audience Adaptation Matrix.**

### Test 5 — Genuine Conviction

Where voice is absent, conviction cannot be evaluated. Where it is present:

"The format is `PROJ-{NNN}-{slug}` and it matters" (line 348) — the "and it matters" is conviction-first phrasing. The sentence does not hedge. It states the format and immediately signals why it matters, without ceremony. Believed.

"Replace `YOUR_USERNAME` with your actual Windows username. To find the full path, run `echo $env:USERPROFILE` in PowerShell." (line 260) — practical, direct. Reads as someone who has fielded this question and knows exactly what to say. Believed.

"`echo '.jerry/' >> .gitignore`" with the surrounding "If you don't have a `.gitignore` yet:" (line 378) — the conditional framing is considerate without being defensive. Believed.

**PASS — No assembled or performed voice detected. Functional-accurate passages read as trustworthy, not hollow.**

---

## Boundary Condition Check

| # | Boundary | Status | Evidence |
|---|----------|--------|----------|
| 1 | NOT Sarcastic | CLEAR | No mockery in any new content. The format-consequence note ("you'll see `<project-error>` messages") is matter-of-fact, not scolding. |
| 2 | NOT Dismissive of Rigor | CLEAR | Format consequence is stated directly: use a different format and you get `<project-error>`. Rigor of the naming convention is treated seriously. |
| 3 | NOT Unprofessional in High Stakes | CLEAR | No humor present in any new content. Not applicable — these are navigational and precision improvements. |
| 4 | NOT Bro-Culture Adjacent | CLEAR | No exclusionary language. "YOUR_USERNAME" is a universal technical convention. |
| 5 | NOT Performative Quirkiness | CLEAR | No personality attempted in new content. Nothing strained. |
| 6 | NOT Character Override | CLEAR | Document governs framework installation language only. No behavioral instructions to Claude. |
| 7 | NOT Information Replacement | CLEAR | All changes add information. No personality substituting for content. |
| 8 | NOT Mechanical Assembly | FLAGGED (LOW) | See detail below. |

### Boundary #8 Detail — Mechanical Assembly

**Status vs. Iteration 3:** The two LOW severity patterns from iteration 3 are unchanged (callout box density — content org issue, not voice; SSH context box register seam — optional fix, not required). One new LOW severity pattern is introduced. Net severity: LOW, consistent across iterations 2, 3, and 4.

**New Pattern — Source-name variability note repetition (Low severity):**

The three `**Source name differs?**` notes (lines 615, 631, 643) use near-identical phrasing across Updating (GitHub users), Updating (local clone), and Uninstallation sections:

- Line 615: `**Source name differs?** Use the name from \`/plugin marketplace list\`: \`/plugin marketplace update <name-from-list>\`.`
- Line 631: `**Source name differs?** Use the name from \`/plugin marketplace list\`.`
- Line 643: `**Source name differs?** Use the name from \`/plugin marketplace list\`: \`/plugin uninstall jerry@<name-from-list>\`.`

Three consecutive sections, same bolded opener, same instructional frame. This is a parallel structure pattern (the structural tell from `llm-tell-patterns.md`). The severity is LOW because: (a) this is deliberate parallelism serving consistency — a developer who sees the pattern in one section recognizes it in others; (b) each note customizes the command suffix, showing intentional variation; (c) callout-box notes that repeat a convention are expected to repeat it. This is less of a "hollow" tell and more of a "template applied consistently" tell. Noting as LOW, not recommending a fix.

**Pattern from iteration 3 — Callout box format uniformity:** Unchanged. The density in Prerequisites (four stacked callout boxes, lines 42-48) is a content-org observation, not a voice failure. The iteration-3 note stands.

**Pattern from iteration 3 — SSH context box register seam:** Unchanged. The "Even though Jerry's repo is public" phrasing (line 44) is still mildly defensive in register. The optional Fix 1 from iteration 3 remains open.

**Cleared patterns:** No patterns cleared in this iteration — no new voice fixes were in scope.

**Scanning for new LLM tell patterns in all new content:**
- Em-dash stacking: "and it matters — Jerry's CLI and hooks validate this pattern" (line 348) — single em-dash, not stacked. CLEAR.
- Hedging phrases ("it's worth noting," "importantly"): none detected. CLEAR.
- Formulaic transitions ("here's the thing:"): none detected. CLEAR.
- Parallel structure beyond the source-name note pattern: none detected beyond the flagged pattern above.
- Corrective insertions ("it's not X, it's Y"): none detected. CLEAR.
- Voice register drops: no new drops introduced. The existing Troubleshooting register (noted in iteration 1, stable since) is unchanged. CLEAR for new content.
- Ungrounded quantitative claims: none detected. CLEAR.

---

## Voice Gap Comparison — Iteration 3 vs. Iteration 4

| Section | Iteration 3 State | Iteration 4 State | Change |
|---------|------------------|------------------|--------|
| "Plugin not found" (Install from GitHub) | Inline blockquote, Step 2 not explicitly named | References "Re-run Step 2"; anchor to troubleshooting | Improved (navigability + specificity) |
| "Plugin not found" (Local Clone) | Inline blockquote with full fix steps | Cross-reference link to `###` troubleshooting section | Improved (deduplication, cleaner structure) |
| "Plugin not found" (Troubleshooting) | Inline blockquote at same level as other entries | Promoted to `###` heading with full paragraph | Improved (structural — more discoverable) |
| Interactive Installation caveat | Cross-references "Step 1 above" (no link) | Anchor link `[Step 1](#install-from-github)` | Improved (navigability) |
| JERRY_PROJECT format | Format explained, consequence not documented | Consequence documented: `<project-error>` messages | Improved (information gap closed) |
| Windows Local Clone path | `YOUR_USERNAME` placeholder with no lookup help | Lookup command added: `echo $env:USERPROFILE` | Improved (actionability) |
| .gitignore | "is gitignored — do not commit it" with no command | Concrete command added: `echo '.jerry/' >> .gitignore` | Improved (actionability) |
| Updating section | Source-name variability not documented | Three `**Source name differs?**` notes added | Improved (information gap closed) |
| SSH context box (iter 3 Fix 1, optional) | Mildly defensive register | Unchanged | Unchanged |
| Callout box density (iter 3 Fix 2, optional — content org) | 7 stacked callouts in Prerequisites + Install header | Unchanged | Unchanged |

Net: Eight content improvements, zero regressions, one new LOW severity Boundary #8 observation. Both optional iteration-3 items remain open and unchanged.

---

## Suggested Fixes

The document is shippable without any of the following. These are ordered by return on investment.

### Fix 1 — SSH context box warmth (LOW priority — optional, carried from iteration 3)

**Current text (line 44):**
```
When you add a plugin source using the `owner/repo` shorthand (e.g., `geekatron/jerry`),
Claude Code clones the repository via SSH. Even though Jerry's repo is public, the
`owner/repo` format defaults to SSH. If you don't have SSH keys configured for GitHub,
you'll see "Permission denied (publickey)." The fix is simple: use the full HTTPS URL
instead. Both commands do the same thing. See [Install from GitHub](#install-from-github)
for both options side by side.
```

**Observation:** "Even though Jerry's repo is public" is defensive phrasing — it implies the developer might expect public repos to not require SSH, which is a reasonable assumption. The fix is to drop the defensive aside and go straight to the behavior. The close ("Both commands do the same thing") is good — confident and reassuring. The information is complete either way.

**Direction for rewriter (if pursued):** Open with the behavior, not the exception. The first sentence can be tightened: the SSH default behavior is the thing, not the public-repo expectation. The "fix is simple" construction could drop "simple" — the fix is just the fix.

---

### Fix 2 — Source-name variability note variation (LOW priority — Boundary #8, optional)

**Current text (lines 615, 631, 643):**
Three near-identical `**Source name differs?**` notes across Updating and Uninstallation. Parallel structure pattern detected (LOW severity).

**Observation:** The repetition serves consistency — a developer who sees the pattern in the GitHub update section will recognize it in the local clone and uninstall sections. The case for leaving it identical is strong: consistent callout conventions reduce cognitive load. The case for varying it is that three identical openers read as templated.

**Direction for rewriter (if pursued):** Consider whether the local clone update note (line 631 — the shorter form) can be collapsed into the preceding command block as a code comment or inline note, reducing the visible pattern count from three to two. Alternatively, accept the repetition as intentional convention-marking and leave as-is. This is a judgment call, not a voice failure.

---

## H-15 Self-Review Check

- Each test was evaluated with specific textual evidence from the new content: confirmed.
- Test 1 was evaluated first and the only test that could have halted evaluation: confirmed.
- Tests 2-5 evaluated in order with citations from specific new content: confirmed.
- Boundary conditions checked independently of the 5 tests: confirmed.
- Boundary #8 evaluated with `llm-tell-patterns.md` loaded: confirmed. Em-dash stacking, hedging phrases, formulaic transitions, parallel structure, corrective insertions, voice register drops, and ungrounded quantitative claims all scanned. One new parallel structure pattern found (source-name notes). All other patterns clear.
- Vocabulary reference loaded and scanned: no forbidden constructions detected in new content.
- Iteration 3 open items verified as unchanged (not regressed, not resolved — both explicitly optional): confirmed.
- Suggested fixes are specific, actionable, and explicitly marked optional: confirmed.
- Voice gap comparison table provided for iteration-over-iteration tracking: confirmed.
- Violations are not softened (P-022): the LOW severity Boundary #8 pattern is reported directly. The "shippable" verdict is accurate and does not hide the observations.

---

## Session Context (sb-reviewer -> orchestrator)

```yaml
verdict: PASS
failed_test: null
boundary_violations: [8]
text_type: documentation
audience_context: onboarding
suggested_fixes_count: 2
boundary_8_severity: LOW  # Consistent with iterations 2 and 3; one new pattern (source-name parallelism)
regressions_introduced: 0
gaps_closed: 8  # Plugin-not-found navigability x3, Interactive Installation anchor, JERRY_PROJECT consequence, Windows path lookup, .gitignore command, Updating source-name variability
iteration_3_open_items_resolved: 0/2  # Both were optional; neither addressed; neither constitutes a regression
note: >
  PASS with no blockers. All eight new content additions are complete and correctly
  registered. Zero regressions from iteration 3. One new LOW severity Boundary #8
  pattern (source-name variability note parallelism) — deliberate convention, not a failure.
  Both suggested fixes are optional. Document is shippable as-is.
  No sb-rewriter routing required unless a future iteration explicitly targets the two
  optional iteration-3 items (SSH box warmth, callout box density consolidation).
```
