# S-012 FMEA — Marketing Deliverables

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverables:** `work/marketing/slack-message.md`, `work/marketing/medium-article.md`
**Date:** 2026-02-24
**Reviewer:** adv-executor (S-012)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [FMEA Table — Medium Article](#fmea-table--medium-article) | Component-level failure analysis for the full blog post |
| [FMEA Table — Slack Message](#fmea-table--slack-message) | Component-level failure analysis for both Slack versions |
| [FMEA Table — Cross-Channel](#fmea-table--cross-channel) | Failure modes spanning both deliverables |
| [Top 5 Risk Priority Items](#top-5-risk-priority-items) | Detailed analysis of highest-RPN failure modes |
| [Overall Risk Assessment](#overall-risk-assessment) | Summary verdict and disposition |

---

## FMEA Table — Medium Article

> Severity (Sev): 1=negligible, 10=catastrophic. Occurrence (Occ): 1=rare, 10=near-certain. Detection (Det): 1=easy to catch, 10=impossible to catch before publication. RPN = Sev × Occ × Det.

| Component | Failure Mode | Effect | Sev | Occ | Det | RPN | Recommended Action |
|-----------|-------------|--------|-----|-----|-----|-----|--------------------|
| **Title** ("Your AI Output Looks Expert. It Isn't.") | Reader perceives as condescending / gatekeeping — implies anyone currently getting good AI output is deceived | High-skill readers disengage immediately; defensive comments from AI practitioners | 7 | 5 | 3 | 105 | Test title against a secondary framing that leads with the solution, not the flaw; consider "Here's What Separates Good AI Output from Expert AI Output" as lower-aggression variant |
| **Opening hook** ("the expert part is a mirage") | Overstatement: skilled practitioners do get expert-quality output; absolute framing invites immediate falsification | Technical readers counter with examples that disprove the universal claim; credibility damage in comments | 7 | 6 | 4 | 168 | Qualify scope: "for most use cases" or "without structured prompting"; the nuance exists later in the piece but not in the hook |
| **"Fluency-competence gap" term** | Author-coined term presented as established term without flagging it as personal coinage | Readers Google it, find nothing, perceive a citation fabrication attempt; trust collapses | 8 | 4 | 5 | 160 | Add explicit hedge: "a shorthand I started using" is already present in the text — ensure it remains prominent; do not let editing remove it |
| **Bender & Koller (2020) citation use** | Paper argues about meaning/form in NLP; article uses it to support "models can sound like they understand without understanding" — an over-extension of a specific philosophical argument | ML researchers recognize the misapplication; signals careless scholarship; undermines the article's credibility with technical audience | 8 | 5 | 6 | 240 | Add a qualifying sentence: note that B&K's argument is philosophical/linguistic, not a direct benchmark result; the claim the article makes is consonant with the paper's spirit but should not be presented as a direct empirical finding from it |
| **Sharma et al. (2024) citation — RLHF/sycophancy** | RLHF amplification of sycophancy is real; however "models learn to agree with users rather than push back, even when the user is wrong" is a simplification; sycophancy is context-dependent and partially addressed in more recent model versions | Researchers push back in comments; claim ages badly as models improve | 6 | 5 | 5 | 150 | Add a temporal hedge: "at the time of writing" or "in models up to [year]"; acknowledge that mitigation is an active area of research |
| **Level 1 / Level 2 / Level 3 framework** | Framework feels arbitrary — no principled boundary between levels; "Level 3" prompt example is long but Level 2 example could also include self-critique | Readers question the taxonomy; reduces authority of the structured argument | 5 | 5 | 5 | 125 | Explicitly state what distinguishes levels (task complexity, downstream dependency, not just prompt length); add a decision rule: "Use Level 3 when phases build on each other" |
| **Level 2 prompt example** ("Research the top 10 industry frameworks for X") | Generic "X" placeholders make the example feel abstract/non-actionable; readers cannot immediately verify the claim that 2-3 more sentences yields measurably better output | Readers don't try it; conversion to action (the article's CTA goal) fails | 5 | 5 | 3 | 75 | Replace X with a concrete example (e.g., "software architecture review") to make the output difference viscerally clear |
| **Wei et al. (2022) CoT citation** | CoT paper studied arithmetic/commonsense tasks; article generalizes to "every prompting scenario I've tested" — the data don't support that breadth | Experienced ML readers flag over-generalization; weakens evidence quality | 6 | 4 | 5 | 120 | Limit the generalization: "the principle tracks in my experience" is already present — make sure the citation supports only the narrower claim (structured prompting improves arithmetic/reasoning benchmarks) and the author's experience supports the broader claim separately |
| **"Garbage in, increasingly polished garbage out"** | Memorable phrase but risk of misattribution or viral extraction without context; could be quoted as the author dismissing AI entirely | Misrepresentation of the article's actual position (AI is useful with structure) | 4 | 4 | 6 | 96 | Low risk; no change required. Phrase is accurate to the claim; over-engineering the messaging here would reduce impact |
| **Panickssery et al. (NeurIPS 2024) citation — self-critique** | Paper studies LLM evaluators rating their own generations; article uses it to qualify the self-critique prompt step — this is a valid and well-scoped use | Low failure risk; citation is well-matched to the claim | 2 | 2 | 2 | 8 | No action needed |
| **Liu et al. (2024) "Lost in the Middle" citation** | Study is on document retrieval tasks; article extends to "conversational case" with appropriate hedge ("hasn't been studied as rigorously") | Hedge is present; low risk of backlash if hedge is preserved through editing | 3 | 3 | 3 | 27 | Ensure copy-editing does not strip the hedge sentence; flag it as load-bearing |
| **"The Move Most People Miss" section** | Two-conversation pattern is counterintuitive and has real tradeoffs (acknowledged in the text); some practitioners may find this workflow impractical in tool environments that persist context | Readers in specific tool environments (Cursor, Claude Projects, custom memory layers) call the advice outdated or inapplicable | 5 | 5 | 4 | 100 | Add a brief parenthetical acknowledging that persistent-memory or project-scoped tools change the equation; the principle still holds but the implementation differs |
| **"When This Breaks" section** | Section exists and is well-done; single failure mode: the hallucination caveat could be read as undercutting the entire preceding advice | Readers focus on "it doesn't eliminate failures" as the article's true conclusion; discount the positive guidance | 4 | 3 | 4 | 48 | Reorder to ensure the section ends with a constructive pivot ("that's when you decompose the work") — this is already present; verify it is the final sentence of the section |
| **"Start Here" call to action** | Three questions are clear; risk: the second CTA at the end ("Next time you open an LLM...") is a different action from the first list | Two competing CTAs reduce conversion on both; readers unsure what the "one thing" to do is | 5 | 4 | 4 | 80 | Merge or subordinate: make the final paragraph the emotional close, and position the five-question checklist as the primary CTA; do not split the action request |
| **References section formatting** | Author name format mixes "Bender, E. M. & Koller, A." (APA-ish) with "Panickssery, A. et al." — inconsistent citation style | Readers perceive sloppiness; diminishes perceived scholarly rigor | 3 | 5 | 3 | 45 | Standardize to one citation format (APA preferred for technical-adjacent audience); minor cleanup |
| **Overall framing ("every model I've tested")** | First-person authority claim without n= or methodology; unfalsifiable | Skeptical readers dismiss as anecdote; reduces transferability of advice | 6 | 5 | 6 | 180 | Either add minimum context ("across 5+ model families over 18 months of production use") or reframe as "in my experience" throughout — currently inconsistent mix of both |
| **Tags** (AI, Prompt Engineering, LLMs, Productivity, Software Engineering) | "Software Engineering" tag may attract audience expecting code-specific content; article is general-purpose | Bounce rate increase from mismatched audience expectation | 3 | 4 | 3 | 36 | Replace "Software Engineering" with "Machine Learning" or "AI Tools" for better audience fit |

---

## FMEA Table — Slack Message

| Component | Failure Mode | Effect | Sev | Occ | Det | RPN | Recommended Action |
|-----------|-------------|--------|-----|-----|-----|-----|--------------------|
| **Short Version — opening** ("Your LLM output looks authoritative. Clean headings...") | Mirrors article hook; same condescension failure mode; more acute in Slack because no surrounding context to soften it | Immediate scroll-past from practitioners; hostile reply in channel | 7 | 6 | 3 | 126 | Same mitigation as article title: lead with benefit, not indictment |
| **Short Version — "polished garbage"** | In isolation (Slack), the phrase reads as a blanket dismissal of AI output with no nuance | Recipients who rely on AI tools feel targeted; defensive reactions | 6 | 5 | 4 | 120 | Add "without structure" qualifier: "Level 1 gets you polished garbage without constraints" makes it a technique critique, not a tool critique |
| **Short Version — "RLHF amplifies sycophantic tendencies"** | Technical jargon in a Slack post assumes ML-literate audience; non-technical channels will not parse "RLHF" | Message loses half its audience in the first paragraph | 5 | 6 | 3 | 90 | Either define inline ("RLHF — the technique used to make models helpful") or cut to the layman version: "models are trained to agree with you" |
| **Short Version — "[BLOG_URL]" placeholder** | Placeholder not replaced before send | Message goes out with literal "[BLOG_URL]" text; looks unprofessional, broken link | 9 | 4 | 2 | 72 | Pre-send checklist: verify URL replacement; critical but easy to detect |
| **Longer Version — McConkey opening** | Shane McConkey reference is insider knowledge (extreme skiing subculture); in a general professional Slack the analogy lands as non sequitur | Recipients confused; read as off-brand or self-indulgent | 6 | 6 | 4 | 144 | Reserve the Longer Version for communities where McConkey is a known cultural reference (skiing/outdoor sports channels, team channels where personality is established); add audience routing guidance to the document |
| **Longer Version — "looked completely unhinged"** | Word "unhinged" has negative connotations in professional contexts even when used positively | HR-sensitive readers flag; in formal Slack workspaces it reads as inappropriate | 5 | 4 | 4 | 80 | Replace with "unconventional" or "chaotic-looking" |
| **Longer Version — citation hedge ("at least one study on document retrieval")** | Vague attribution weakens credibility; reads as "I half-remember a study" | Technically literate readers note the imprecision; reduces credibility of the technique | 5 | 5 | 4 | 100 | Replace with specific attribution: "Liu et al. (2024) found in document retrieval tasks that..." even in the Slack post; precision signals rigor |
| **Longer Version — length** | "Longer version" is 190 words; this is long for a Slack post in most channels | Message gets truncated behind "see more" fold; key points in the bottom half go unread | 5 | 6 | 3 | 90 | Trim to 120 words maximum for Slack; move the citation detail to a reply thread rather than the main post |
| **Overall Slack framing — two versions without selection guidance** | Document contains both "Short" and "Long" versions but no guidance on when to use which | Sender posts wrong version to wrong channel; e.g., long version in a #general channel, short version in a technical channel where depth would be welcomed | 5 | 5 | 3 | 75 | Add explicit channel-routing guidance: "#general / #random → Short Version; #eng / #data / #ml → Longer Version" |

---

## FMEA Table — Cross-Channel

| Component | Failure Mode | Effect | Sev | Occ | Det | RPN | Recommended Action |
|-----------|-------------|--------|-----|-----|-----|-----|--------------------|
| **Terminology consistency** ("fluency-competence gap") | Term used in article but absent from Slack post; readers who see Slack first and then read article may not connect the two | Reduced brand/concept coherence across channels | 3 | 5 | 4 | 60 | Add the term (briefly) to the Slack post to create a breadcrumb for readers who follow through to the article |
| **Tone delta** | Article tone is measured and scholarly (hedges, caveats, "in my experience"); Slack tone is bolder and more declarative ("polished garbage," "it's a mirage") | Cross-channel readers experience tonal whiplash; undermines the scholarly authority built in the article | 6 | 5 | 5 | 150 | Reduce declarative severity in Slack to create a coherent voice; the Slack post should feel like a teaser for the article's depth, not a more extreme version of it |
| **CTA alignment** | Article ends with "Next time you open an LLM, before you type anything, write down three things..."; Slack ends with "Full post with the research behind it: [BLOG_URL]" — different actions requested | Neither CTA is reinforced by the other; conversion diluted | 4 | 5 | 4 | 80 | Align the Slack CTA to the article's three questions: "The article has a three-question checklist that changes what you get back — link below" |
| **Citation presence delta** | Article is heavily cited; Slack long version vaguely references "at least one study"; Slack short version mentions no sources at all | Readers who encounter Slack first may not recognize the research grounding; those who encounter article first may find Slack oversimplified | 5 | 4 | 4 | 80 | Short Version: add a single inline citation anchor ("backed by peer-reviewed research on sycophancy and context attention") to signal rigor without cluttering; Long Version: use proper citation as noted above |

---

## Top 5 Risk Priority Items

### 1. Bender & Koller (2020) Over-Extension — RPN 240

**Component:** Article citations — B&K use
**Failure Mode:** The paper makes a philosophical argument about the relationship between linguistic form and meaning. It does not empirically demonstrate that LLMs "sound like they understand without understanding" in the sense readers will interpret from the article. The article's use is directionally defensible but citation-precise it is not.
**Why it's the highest risk:** Technical readers (the most likely sharers and amplifiers of this content) will evaluate citation accuracy first. A single "this paper doesn't say that" comment from a credible ML researcher can anchor the entire comment section and define the article's public reception. The failure is partially detectable (6/10 detection difficulty) because it requires domain expertise to catch — meaning most editors will miss it but the most influential readers will not.
**Recommended Action:** Add a one-sentence framing: "Bender and Koller's 2020 argument centers on the distinction between linguistic form and meaning — a theoretical foundation for why fluency and competence diverge." This accurately represents the paper's scope and naturally leads to the broader claim rather than treating the paper as empirical evidence for it.

---

### 2. Overall Framing — First-Person Authority Without Methodology — RPN 180

**Component:** "Every model I've tested" / "in my experience" claims
**Failure Mode:** The article alternates between "in my experience" (appropriately hedged) and "this holds across every major model family I've tested" (unfalsifiable empirical claim). The asymmetry is inconsistent and makes the article's epistemic standards feel slippery.
**Why it matters:** Skeptical readers will note the inconsistency and apply the weakest framing to all claims. The article's value is in its practical advice, but that advice gains credibility from the evidence it marshals. If readers dismiss the evidence framing as anecdotal, the three-level framework itself becomes vulnerable to "just your opinion."
**Recommended Action:** Audit all first-person empirical claims and apply one of two framings consistently: (a) "in my experience with [specific types of tasks/models/timeframe]" for experience-based claims, or (b) cite the supporting paper for claims with direct empirical grounding. Eliminate the inconsistent mix of hedged and absolute language.

---

### 3. Opening Hook Absolute Framing — RPN 168

**Component:** Opening paragraph — "the expert part is a mirage"
**Failure Mode:** The hook universalizes a problem that is real but not universal. Practitioners who consistently get high-quality output without Level 3 prompting (they exist) will read the opening as an attack on their competence and disengage before the value is delivered.
**Why it matters:** The hook is the highest-leverage sentence in the piece. It determines whether a reader continues. If the ideal target audience (experienced practitioners who could benefit from Level 3 but already use Level 2) perceives the hook as irrelevant to them, the article fails its highest-value conversion goal.
**Recommended Action:** Qualify the hook to the specific case where it applies: "For anything beyond one-off tasks, your LLM output looks expert. The expert part is often a mirage." This preserves the impact while narrowing the claim to where it is actually defensible.

---

### 4. McConkey Opening in Slack Longer Version — RPN 144

**Component:** Slack Longer Version — McConkey analogy
**Failure Mode:** The McConkey reference is culturally specific (extreme skiing, a niche subculture). In most professional Slack workspaces, it lands as a non sequitur. Unlike the article where surrounding context establishes the author's voice, the Slack post is a cold read — the reference has no scaffolding.
**Why it matters:** The first sentence of the longer Slack version will determine whether channel members read further. A confusing opening in Slack produces an immediate scroll-past, and there is no recovery — unlike in a Medium article where a reader who is confused at sentence 1 may try sentence 2. In Slack, confusing = done.
**Recommended Action:** The McConkey analogy belongs in the Longer Version only for specific community contexts (e.g., outdoor sports-adjacent channels, teams where the author's personality is known). Default the Longer Version's opening to the direct framing: "Three levels of prompting — three levels of output quality. Most people stop at Level 2 and miss the move that changes everything." Reserve the McConkey version as an opt-in variant with explicit audience guidance.

---

### 5. Tonal Whiplash Cross-Channel — RPN 150 (cross-channel) / 126 (Slack standalone)

**Component:** Cross-channel tone delta; Slack Short Version opening
**Failure Mode:** The article's measured, scholarly tone (multiple hedges, explicit acknowledgment of limitations, citations with appropriate scope) is undermined by the Slack post's more aggressive declarations ("polished garbage," "it's a mirage," "Level 1 gets you polished garbage"). Readers who encounter both will experience a tonal split that registers as inauthenticity — either the article is over-hedged or the Slack is over-claiming.
**Why it matters:** Cross-channel consistency is not a nicety; it is the mechanism by which readers trust the author across contexts. If the author presents as a careful empiricist in one channel and a declarative provocateur in another, the more credible presentation (the article) is discounted.
**Recommended Action:** The Slack post should function as a teaser that earns the article's depth, not a more extreme version of the article's claims. Reduce the declarative severity in both Slack versions: replace "polished garbage" with "polished-looking but unreliable output" in formal channels; keep the bolder phrasing only in technically savvy or informal community channels. Add explicit channel routing guidance to the document.

---

## Overall Risk Assessment

### Risk Profile Summary

| Severity Band | Count | Highest RPN | Total RPN | Notes |
|--------------|-------|-------------|-----------|-------|
| Critical (RPN > 200) | 1 | 240 | 240 | B&K citation over-extension |
| High (RPN 126–200) | 5 | 180 | 786 | Framing, tone, McConkey, hook |
| Medium (RPN 75–125) | 8 | 125 | 866 | Framework taxonomy, CoT over-gen, RLHF hedge, CTA split, etc. |
| Low (RPN < 75) | 8 | 72 | 308 | URL placeholder, tags, formatting |

**Total RPN across all failure modes: 2,200**

### Publication Readiness

**Medium Article:** Conditionally ready. The article is substantively strong — the three-level framework is practical, the citations are real and mostly well-matched, the "When This Breaks" section demonstrates intellectual honesty, and the two-conversation pattern is genuinely useful advice. However, the B&K citation over-extension (RPN 240) and first-person authority inconsistency (RPN 180) are credibility risks with the technical audience this article is trying to reach and persuade. Both are fixable with minor edits that do not require restructuring.

**Slack Short Version:** Conditionally ready pending URL replacement (RPN 72, easy fix) and qualifier addition to "polished garbage" for formal channels. Low effort to clear.

**Slack Longer Version:** Not ready for general-channel deployment. The McConkey opening (RPN 144) and length (90+ words over recommended Slack limit) require revision before the piece functions in its intended distribution channel. The channel-routing guidance gap is a structural issue with the document itself — the Longer Version is a good piece of writing for the wrong default audience.

### Recommended Pre-Publication Actions (Priority Order)

1. **[Blocker — Article]** Fix B&K citation framing to accurately represent its scope as a philosophical/linguistic argument rather than an empirical finding.
2. **[High — Article]** Audit and standardize first-person authority framing throughout the article.
3. **[High — Slack LV]** Replace McConkey opening with direct framing as the default; make McConkey an opt-in variant with channel guidance.
4. **[High — Both]** Add tone calibration: reduce declarative severity in Slack to create coherent cross-channel voice.
5. **[Medium — Article]** Qualify the hook to avoid alienating practitioners who already get good output.
6. **[Medium — Slack LV]** Replace vague "at least one study" with specific Liu et al. attribution.
7. **[Low — Both]** Standardize citation format in article; replace "[BLOG_URL]" before send; add channel-routing guidance to Slack document.

### Risk Acceptance Threshold

For C2 marketing deliverables, items with RPN > 150 require mitigation before publication. Items 240 and 180 exceed this threshold. Items 168 and 150 are at the threshold boundary and SHOULD be addressed. All other items are within acceptable risk tolerance for C2 criticality.

**Disposition: REVISE — targeted revision required on items 1 and 2 above before the article publishes; Slack LV requires structural rework before general distribution.**
