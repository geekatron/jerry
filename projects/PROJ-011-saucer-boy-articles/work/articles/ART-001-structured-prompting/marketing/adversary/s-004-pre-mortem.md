# S-004 Pre-Mortem Analysis — Marketing Deliverables

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverables:** `work/marketing/slack-message.md`, `work/marketing/medium-article.md`
**Date:** 2026-02-24
**Reviewer:** adv-executor (S-004)

**Failure Scenario:** "It is August 2026. The Slack message was posted in three company channels and two public Slack communities. It received minimal engagement — a few emoji reactions, zero thread replies, and no measurable click-through. The Medium article was published and received 47 views in the first week, 2 claps, and zero shares. The blog post it promoted saw no measurable traffic increase from either channel."

---

## Findings Summary

| Finding ID | Deliverable | Severity | Failure Mode | Probability |
|------------|-------------|----------|-------------|-------------|
| S-004-001 | Slack | CRITICAL | Opener insults reader's current work | HIGH |
| S-004-002 | Slack | MAJOR | "Polished garbage" alienates target audience | MEDIUM |
| S-004-003 | Slack | MAJOR | McConkey reference opaque to most readers | HIGH |
| S-004-004 | Slack | MAJOR | No information gap; gives away the key insights | HIGH |
| S-004-005 | Slack | MINOR | Model universality claim unsubstantiated | LOW |
| S-004-006 | Medium | CRITICAL | Title triggers clickbait skepticism | HIGH |
| S-004-007 | Medium | CRITICAL | Citations not hyperlinked — ironic credibility gap | HIGH |
| S-004-008 | Medium | MAJOR | Length in no-man's-land (too long for casual, too short for deep) | MEDIUM |
| S-004-009 | Medium | MAJOR | Competes in exhausted "prompting levels" frame | HIGH |
| S-004-010 | Medium | MAJOR | Limitations section undermines confidence before CTA | MEDIUM |
| S-004-011 | Medium | MAJOR | No author credibility signals | MEDIUM |
| S-004-012 | Medium | MINOR | Tonal inconsistency between Slack and Medium pieces | LOW |
| S-004-013 | Medium | MINOR | Tags too generic for Medium discovery | LOW |
| S-004-014 | Medium | OBSERVATION | No cross-link to blog post from Medium article | LOW |

---

## Priority Classification

### P0 — Must Mitigate Before Publication

**S-004-001 | Slack opener insults the reader**

The first sentence — "Your LLM output looks authoritative. Clean headings, professional language, confident tone. Except it's a mirage." — tells the reader their work is garbage. In a Slack channel, this is the only content visible before the fold. The natural psychological response is defensive dismissal, not curiosity.

**Recommendation:** Reframe the opener to position the reader as the smart person discovering a non-obvious insight. Example: "There's a gap between how polished LLM output looks and how well it holds up under scrutiny — and most teams don't notice until it costs them."

**S-004-006 | Medium title triggers skepticism**

"Your AI Output Looks Expert. It Isn't." uses a clickbait pattern Medium readers have been trained to distrust. The "X Looks Good. It's Actually Bad" formula has been overused in the AI content space. Additionally, telling readers their output "isn't" expert is insulting at the highest-stakes position: the title.

**Recommendation:** Reframe around the insight rather than the insult. Examples: "The Prompting Level Most Teams Skip (And Why It Changes Everything)" or "Three Levels of LLM Prompting: From Plausible to Rigorous."

**S-004-007 | Citations not hyperlinked**

The article references five papers using academic parenthetical style (Author et al., Year) without hyperlinks. An article whose core thesis is about the gap between appearing rigorous and being rigorous demonstrates that exact gap in its own citation practices. A knowledgeable reader will notice this irony.

**Recommendation:** Convert every citation to an inline hyperlink. The References section exists at the bottom but the inline citations in the body lack clickable links to the actual papers.

---

### P1 — Should Mitigate

**S-004-004 | Slack gives away the answer**

Both Slack versions deliver the three-level framework and the two-session pattern — the blog's core value propositions. The reader's rational response: "I got the gist. No need to click." Restructure to create an information gap rather than summarize.

**S-004-009 | Exhausted content frame**

"Levels of prompting" returns dozens of near-identical articles on Medium. The unique differentiators (two-session pattern, fluency-competence gap research, Panickssery self-critique limitation) are buried in the body. Lead with what makes this different.

**S-004-002 | "Polished garbage" alienates practitioners**

Replace with intriguing-but-respectful phrasing. The people most likely to click are the ones most likely to feel attacked by this phrase.

**S-004-003 | McConkey reference opaque in Slack**

Either remove from Slack entirely or add one sentence of setup: "Shane McConkey showed up to world-class ski competitions in a banana suit — and still won."

**S-004-008 | Length in no-man's-land**

~1,100 words: too long for casual Medium scrollers (500-700), too short for deep-dive audience (2,000-3,000). Commit to either punchy manifesto or comprehensive breakdown.

**S-004-010 | Limitations section placement**

"When This Breaks" appears right before the call to action, ending the reader's emotional arc on doubt. Move it before the principles summary so recovery strategies follow.

**S-004-011 | No author credibility**

No information about who wrote it or their experience. Add a brief first-person aside: "After a year of using these patterns across production codebases..."

---

### P2 — Monitor

- **S-004-005:** Qualify the model universality claim with specifics
- **S-004-012:** Align tonal voice between Slack and Medium
- **S-004-013:** Replace 1-2 generic Medium tags with niche ones ("AI Tools", "LLM Prompting")
- **S-004-014:** Add blog cross-link to Medium article closing

---

## Scoring Impact Assessment

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | Missing reference links, author signals, cross-links |
| Internal Consistency | 0.20 | Negative | Article about rigor lacks rigorous citations; tonal mismatch between channels |
| Methodological Rigor | 0.20 | Negative | No competitive differentiation analysis; length strategy not deliberate |
| Evidence Quality | 0.15 | Negative | Citations present but unverifiable without hyperlinks |
| Actionability | 0.15 | Mixed | "Start Here" section is strong; but Slack gives away the answer and limitations undermine motivation |
| Traceability | 0.10 | Negative | Citations cannot be traced to sources without hyperlinks |

**Overall:** The deliverables are well-written at the sentence level with genuine insight. Failure modes are primarily strategic (audience psychology, competitive positioning, citation mechanics) rather than content-quality issues. The three P0 findings are each individually sufficient to cause the promotional campaign to underperform.

---

*Pre-Mortem completed by adv-executor | S-004 Pre-Mortem Analysis | C4 adversarial tournament*
