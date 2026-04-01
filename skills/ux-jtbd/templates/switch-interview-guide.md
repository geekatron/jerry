<!-- TEMPLATE: switch-interview-guide.md | VERSION: 1.2.0 | DATE: 2026-03-04 | SKILL: /ux-jtbd | AGENT: ux-jtbd-analyst | REVISION: v1.1.0->v1.2.0 iter3 quality fixes -- added Participant Screening, inline Moesta citations, sample size guidance, forces/job discovery traceability citations, canonical name alignment, visible rapport-building citation, Decision Basis traceability -->
<!-- SOURCE: Moesta, B. (2020). Demand-Side Sales 101. Lioncrest Publishing. -->
<!-- PURPOSE: Structured switch interview guide template. The ux-jtbd-analyst adapts these questions to the product context for each engagement. -->

# Switch Interview Guide: {{PRODUCT_NAME}}

> **Engagement ID:** {{ENGAGEMENT_ID}}
> **Product:** {{PRODUCT_NAME}}
> **Target Segment:** {{TARGET_SEGMENT}}
> **Date Generated:** {{DATE}}
> **Interviewer:** {{INTERVIEWER_NAME}}
> **Template Version:** 1.2.0

## Document Sections

| Section | Purpose |
|---------|---------|
| [Participant Screening](#participant-screening) | Who qualifies, recruitment screener, sample size guidance |
| [Interview Protocol](#interview-protocol) | Duration, recording, consent, rapport |
| [Timeline Questions](#timeline-questions) | Map the switching timeline from first thought to satisfaction |
| [Four Forces Questions](#four-forces-questions) | Push, pull, anxiety, and habit force discovery |
| [Job Discovery Questions](#job-discovery-questions) | Functional, social, and emotional job elicitation |
| [Follow-Up Probes](#follow-up-probes) | Generic depth questions for any response |
| [Analysis Mapping Guide](#analysis-mapping-guide) | How to map responses to the JTBD framework |
| [AI-Augmented Analysis Note](#ai-augmented-analysis-note) | P-022 disclosure on AI synthesis limitations |

---

## Participant Screening

Before conducting switch interviews, screen participants to ensure they qualify as valid interview subjects. Subject selection is critical to interview quality -- recent switchers produce richer recall and more actionable force data.

### Who Qualifies

A valid switch interview subject is someone who has **recently switched** from one solution to another (or from non-consumption to a solution) within the relevant product domain. Key criteria:

- **Recency:** The switching event occurred within the last 18 months. Beyond 18 months, recall degrades significantly and post-hoc rationalization replaces genuine timeline memory. Source: Moesta (2020) [Tier 2]
- **Completeness:** The participant completed the switch (not still evaluating or in a trial period). They must have passed through at least the Decision stage and ideally the Consumption stage.
- **Relevance:** The participant belongs to the target user segment for this engagement. Switching between unrelated product categories does not qualify.

### Recruitment Screener Questions

Use these screening questions to qualify candidates before scheduling the full interview:

1. "Have you started using a new [product category / tool / approach] for [relevant task] in the past 18 months?"
2. "Were you previously using a different [product category / tool / approach] for the same purpose, or were you doing it manually / not doing it at all?"
3. "Have you fully committed to the new approach, or are you still evaluating it alongside the old one?"
4. "Approximately when did you make the switch -- can you estimate the month and year?"

**Qualification rule:** A participant qualifies if they answer YES to questions 1 and 2, indicate full commitment (question 3), and the switch date falls within 18 months (question 4). Participants still in active evaluation may be interviewed but should be flagged as "in-progress switchers" in the analysis.

### Minimum Sample Size

A minimum of **5-10 switch interviews** with distinct participants is required before reliable patterns can be identified. A single interview produces individual insight but not pattern recognition. Source: Moesta (2020) [Tier 2]. For initial JTBD pattern identification, aim for 10+ interviews; for hypothesis validation, 5 interviews may suffice if the target segment is well-defined.

---

## Interview Protocol

### Logistics

| Parameter | Recommendation |
|-----------|---------------|
| **Duration** | 45-60 minutes (do not exceed 75 minutes; fatigue degrades recall quality). Source: Moesta (2020) [Tier 2] |
| **Format** | One-on-one, conversational (not survey-style) |
| **Recording** | Audio recording strongly recommended; video optional. Obtain explicit consent before recording. |
| **Note-taking** | Designate a note-taker or use recording transcription. The interviewer should focus on listening and follow-up, not writing. |
| **Environment** | Quiet, private setting. Remote interviews via video call are acceptable. Avoid group settings -- social dynamics suppress honest switching narratives. Source: Moesta (2020) [Tier 2] |

### Ethical Considerations

1. **Informed consent.** Before beginning, explain the purpose of the interview, how the data will be used, and that participation is voluntary. Obtain written or verbal (recorded) consent.
2. **Anonymity.** Assure the participant that their responses will be anonymized in all reports. Use participant codes (P-001, P-002) rather than names in analysis artifacts.
3. **Right to withdraw.** The participant may stop the interview or decline any question at any time without consequence.
4. **Data handling.** Interview recordings and transcripts are stored in the engagement directory (`projects/${JERRY_PROJECT}/engagements/{{ENGAGEMENT_ID}}/`) and are not shared outside the research team without explicit permission.
5. **No deception.** Per P-022, do not misrepresent the purpose of the interview or how the data will be used.

### Rapport-Building Opening (5-7 minutes)

Begin with warm-up questions that establish trust and context before entering the switching timeline. These are not scored or analyzed -- they set the conversational tone. Source: Moesta (2020) [Tier 2].

> 1. "Thank you for taking the time to speak with me. Before we dive in, could you tell me a little about yourself and your role?"

> 2. "How long have you been working in [their domain/role]?"

> 3. "What does a typical day look like for you when it comes to [relevant activity area]?"

**Transition to timeline:** Once rapport is established (the participant is speaking freely and appears comfortable), transition with:

> "I would love to hear the story of how you came to use [{{PRODUCT_NAME}} / the current solution]. Let us start from the very beginning..."

---

## Timeline Questions

> **Minimum interview count for pattern recognition:** A minimum of 5-10 switch interviews with distinct participants is required before patterns can be reliably identified from timeline data. A single interview produces individual insight, not pattern recognition -- this is a fundamental Moesta methodology constraint. Do not generalize findings from fewer than 5 interviews. Source: Moesta (2020) [Tier 2].

The switching timeline maps the journey from first awareness of a problem through to current satisfaction. The 6-stage switching timeline is drawn from Moesta's demand-side sales model. Source: Moesta (2020) [Tier 2]. The timeline reveals the forces acting on the user at each stage. Ask these questions in chronological order, following the participant's narrative.

### Stage 1: First Thought

The moment the participant first realized their current situation was not working.

> 4. "Can you think back to the very first time you thought 'something needs to change' about how you were handling [relevant task]? What was happening at that moment?"

> 5. "What specifically triggered that first thought? Was it a particular event, a frustration that built up, or something someone said?"

> 6. "When was that, roughly? Can you place it in time -- a month, a season, a project?"

### Stage 2: Passive Looking

The period where the participant was aware of the problem but not actively seeking a solution.

> 7. "After that first realization, how long did you sit with it before doing anything about it? What kept you from acting immediately?"

> 8. "During that time, did you notice alternatives in passing -- maybe a colleague mentioned something, or you saw an ad? What caught your attention?"

> 9. "What was happening in your work or life that made the problem feel more or less urgent during that period?"

### Stage 3: Active Looking

The point where the participant began deliberately searching for alternatives.

> 10. "What was the tipping point that moved you from thinking about it to actually looking for something new?"

> 11. "How did you go about looking? What did you search for, who did you ask, what did you compare?"

> 12. "What were the most important things you were looking for in a new solution? What would it need to do?"

> 13. "How many alternatives did you seriously consider? What made each one a contender -- or not?"

### Stage 4: Decision

The moment the participant committed to switching.

> 14. "Walk me through the moment you decided to go with [the chosen solution]. What was the final thing that tipped you over?"

> 15. "Was there anything that almost stopped you from making the switch, even at that late stage?"

> 16. "Did anyone else influence the decision? A manager, a colleague, a team?"

> 17. "What did you have to give up or leave behind by making the switch?"

### Stage 5: Consumption (First Use)

The participant's early experience with the new solution.

> 18. "What was your first experience like when you started using the new approach? Did it match your expectations?"

> 19. "What surprised you -- positively or negatively -- in those first days or weeks?"

> 20. "Was there a moment where you thought 'I made the right choice' -- or 'I made a mistake'? What triggered that feeling?"

### Stage 6: Satisfaction (Ongoing)

The participant's current assessment and whether the switch delivered on its promise.

> 21. "Looking back now, how do you feel about the switch overall?"

> 22. "What does the new approach do better than the old one? What does it do worse?"

> 23. "If you had to do it all over again, would you make the same choice? Why or why not?"

> 24. "Is there anything that would make you start looking again -- for yet another alternative?"

---

## Four Forces Questions

Source: Moesta (2020) [Tier 2] -- four forces of progress model.

These questions target each of the four forces in the Moesta/Spiek four forces model directly. Use them to supplement the timeline narrative when a particular force has not been adequately explored. The interviewer does not need to ask all of these -- select the ones that fill gaps in the timeline story.

### Push Forces (Current Pain)

Forces that push the user away from their current solution.

> 25. "What was happening that made you start looking for something new?"

> 26. "What was the most frustrating part of your old approach?"

> 27. "Was there a specific incident or moment of failure that stands out?"

> 28. "If you had to explain to someone why the old approach was not working, what would you say?"

> 29. "How long had those frustrations been building before you acted on them?"

### Pull Forces (New Solution Attraction)

Forces that attract the user toward the new solution.

> 30. "What did you hope the new approach would give you that the old one could not?"

> 31. "What was the most appealing thing about [the new solution] when you first encountered it?"

> 32. "Was there a specific feature, promise, or outcome that made you think 'this is the one'?"

> 33. "Did someone recommend it, or did you discover it on your own? What convinced you it was worth trying?"

> 34. "What did 'success' look like in your mind when you imagined using the new approach?"

### Anxiety Forces (Fear of the New)

Forces that create hesitation about switching.

> 35. "What concerns did you have about making the switch?"

> 36. "What was the scariest part about trying something new?"

> 37. "Did you worry about losing data, breaking workflows, or having to relearn everything?"

> 38. "Was there a cost concern -- money, time, effort -- that gave you pause?"

> 39. "What would have made you feel more confident about switching?"

### Habit Forces (Comfort with Current)

Forces that keep the user attached to their current solution.

> 40. "What was keeping you with the old approach, even though you knew it was not ideal?"

> 41. "Were there things about the old way that actually worked well -- things you did not want to lose?"

> 42. "How much time and effort had you invested in learning and customizing the old approach?"

> 43. "Did other people on your team or in your workflow depend on the old approach? How did that factor in?"

> 44. "Was there a sense of 'better the devil you know' -- even if the old approach was flawed, at least it was familiar?"

---

## Job Discovery Questions

Source: Christensen (2016) [Tier 2]; Ulwick (2016) [Tier 2] -- functional, social, and emotional job dimensions.

These questions go beyond the switching narrative to uncover the underlying functional, social, and emotional jobs the user is trying to accomplish. Use them after the timeline and forces questions have established context.

### Functional Jobs (What the User Is Trying to Accomplish)

> 45. "When you think about [the relevant task], what are you ultimately trying to get done?"

> 46. "What does a successful outcome look like for that task? How do you know when it is done well?"

> 47. "What are the steps you go through to accomplish that? Walk me through the process."

> 48. "Where in that process do things tend to break down or take longer than they should?"

> 49. "If you could wave a magic wand, what would the ideal version of accomplishing that task look like?"

### Social Jobs (How the User Wants to Be Perceived)

> 50. "When you accomplish [the task] well, how do others perceive you? What do they think?"

> 51. "Is there anyone -- a manager, a client, a teammate -- whose opinion matters when it comes to how you handle this?"

> 52. "Have you ever felt embarrassed or frustrated about how [the task] went in front of others? What happened?"

> 53. "Does the tool or approach you use affect how professional or competent you appear to others?"

### Emotional Jobs (How the User Wants to Feel)

> 54. "How do you want to feel when you are working on [the task]? What emotional state are you going for?"

> 55. "When things go wrong with [the task], how does that make you feel?"

> 56. "Is there a sense of anxiety, stress, or dread associated with any part of the process? What triggers it?"

> 57. "When you finish [the task] successfully, how does that make you feel? What is the emotional payoff?"

---

## Follow-Up Probes

Use these generic probes to deepen any response throughout the interview. They work with any question in the guide. The best switch interviews follow the participant's narrative rather than rigidly following a script -- these probes help you do that.

### Depth Probes

> "Tell me more about that."

> "What happened next?"

> "Why was that important to you?"

> "Can you give me a specific example?"

> "How did that make you feel?"

### Clarification Probes

> "When you say [their term], what do you mean by that?"

> "Help me understand -- you mentioned [detail]. Can you walk me through that?"

> "Was that the first time that happened, or had it happened before?"

### Contrast Probes

> "How was that different from what you expected?"

> "How does that compare to how you did it before?"

> "If someone else in your role had the same problem, would they see it the same way?"

### Timeline Anchoring Probes

> "Can you place that in time? Was it before or after [earlier event they mentioned]?"

> "How long did that phase last -- days, weeks, months?"

> "What else was going on at work or in your life at that time?"

---

## Analysis Mapping Guide

After the interview, use this mapping guide to translate narrative responses into structured JTBD framework artifacts. Each response segment maps to one or more framework elements.

> **Post-Interview Documentation Timing:** Apply this mapping guide within 24 hours of the interview while recall is fresh (Source: Moesta (2020) [Tier 2]). Interviewer memory of tone, emphasis, hesitation, and non-verbal cues degrades rapidly. If transcription is not available, write up key quotes and force impressions immediately after the session. Tag each note with the timeline stage and force category it relates to. Do not wait until all interviews are complete to begin mapping -- map each interview individually, then look for cross-interview patterns after the full set is complete.

### Response-to-Force Mapping

| Response Pattern | Maps To | Framework Element |
|-----------------|---------|-------------------|
| Frustrations, complaints about the old approach, "it was broken," "I was tired of..." | **Push** | Switch Force Analysis -- Push column |
| Excitement about a new approach, "I heard about...", "it promised...", "I wanted..." | **Pull** | Switch Force Analysis -- Pull column |
| Fear, hesitation, risk language: "what if...", "I was worried about...", "the cost of switching..." | **Anxiety** | Switch Force Analysis -- Anxiety column |
| Comfort, familiarity, investment language: "I was used to...", "we had already...", "at least it worked..." | **Habit** | Switch Force Analysis -- Habit column |

### Response-to-Job Mapping

| Response Pattern | Maps To | Framework Element |
|-----------------|---------|-------------------|
| Task descriptions, process steps, measurable outcomes: "I needed to...", "the goal was..." | **Functional Job** | Job Statement -- Motivation clause |
| Perception of others, reputation, status: "my team would think...", "I wanted to look..." | **Social Job** | Job Statement -- Outcome clause (social) |
| Emotional state language, feelings: "I wanted to feel...", "it stressed me out...", "I felt relieved when..." | **Emotional Job** | Job Statement -- Outcome clause (emotional) |

### Extracting Job Statements from Narratives

Follow this procedure to convert interview responses into canonical job statements:

1. **Identify the triggering situation.** Look for context markers: "When I was...", "Every time I had to...", "Whenever [event] happened..." This becomes the `When [situation]` clause.

2. **Identify the motivation.** Look for desire or action language: "I needed to...", "I wanted to...", "I was trying to..." This becomes the `I want to [motivation]` clause. Remove any product references -- restate as the underlying goal.

3. **Identify the expected outcome.** Look for success criteria or end-state language: "so that I could...", "which would let me...", "the goal was..." This becomes the `so I can [expected outcome]` clause. Ensure the outcome is measurable or observable.

4. **Validate against job statement rules.** Check the resulting statement against the validation rules in `skills/ux-jtbd/rules/jtbd-methodology-rules.md` [Job Statement Rules]: all three clauses present, user perspective, solution-agnostic, single dimension, measurable outcome.

5. **Classify the job type.** Apply the decision procedure from `skills/ux-jtbd/rules/jtbd-methodology-rules.md` [Job Classification Rules]: check for emotional language first, social language second, default to functional.

### Timeline-to-Force Mapping

| Timeline Stage | Primary Force(s) Revealed | What to Listen For |
|---------------|--------------------------|-------------------|
| First Thought | Push | The catalyst event; what broke |
| Passive Looking | Push + Habit | Why the pain persisted without action; what kept them in place |
| Active Looking | Push + Pull | What finally triggered action; what attracted them |
| Decision | Pull + Anxiety | What sealed the deal; what almost stopped them |
| First Use | Pull + Anxiety | Did the promise match reality; what surprised them |
| Satisfaction | All four forces in retrospect | Net assessment; would they switch again |

### Force Rating from Interview Data

After the interview, rate each force on the 1-5 scale defined in `skills/ux-jtbd/rules/jtbd-methodology-rules.md` [Switch Force Analysis Rules]:

| Rating | Criteria | Interview Signal |
|--------|----------|-----------------|
| 1 (Minimal) | Participant barely mentions the force | Brief, unemotional reference; quickly moved past |
| 2 (Low) | Participant mentions it but without emphasis | Acknowledged when asked directly but did not volunteer |
| 3 (Moderate) | Participant brings it up without prompting | Volunteered the force unprompted; moderate emotional intensity |
| 4 (Strong) | Participant returns to it multiple times | Repeated references throughout the interview; strong emotional intensity |
| 5 (Dominant) | The force dominates the narrative | The participant's story revolves around this force; highest emotional intensity |

**Output artifact population:** After mapping interview responses using the tables above, populate the structured output artifact using the Output Format Template in `skills/ux-jtbd/SKILL.md` [Output Format Template]. The mapping tables in this guide produce the raw data; the SKILL.md output format specifies where each mapped element (job statements, force ratings, opportunity scores) is placed in the final deliverable.

---

## AI-Augmented Analysis Note

> **P-022 Transparency Disclosure**
>
> When the `ux-jtbd-analyst` agent is used to synthesize switch interview data using the Moesta/Spiek four forces model, the following limitations apply:
>
> 1. **AI analysis of interview transcripts is secondary analysis.** The AI did not conduct the interview, observe body language, hear vocal tone, or build rapport with the participant. Nuance, hesitation, and emotional subtext may be lost in transcript-based analysis.
>
> 2. **Synthesis confidence is MEDIUM by default.** AI-synthesized job statements derived from interview transcripts carry MEDIUM confidence per `skills/user-experience/rules/synthesis-validation.md`. This means the statements require human review and validation before informing design decisions.
>
> 3. **Pattern recognition across interviews has limitations.** When analyzing multiple interview transcripts, the AI identifies surface-level linguistic patterns. It may miss contextual differences between participants or over-weight commonly-used phrases.
>
> 4. **Interview guide adaptation is not interviewing.** This template provides a starting framework. The ux-jtbd-analyst adapts questions to the product context, but effective interviewing requires real-time human judgment -- reading the room, following unexpected threads, and knowing when to deviate from the script.
>
> 5. **No substitute for direct user contact.** AI-augmented JTBD analysis is designed for tiny teams (1-5 people) who lack resources for full primary research. It supplements, but does not replace, direct user interviews. Whenever possible, conduct real switch interviews using this guide and feed the transcripts back to the analyst for structured synthesis.
>
> All AI-synthesized findings include a Synthesis Judgments Summary enumerating every significant inference. Review this summary to understand where the AI made judgment calls that a human interviewer might have made differently.

---

*Template Version: 1.2.0 | /ux-jtbd Sub-Skill | PROJ-022 User Experience Skill*
*Source: Moesta, B. (2020). Demand-Side Sales 101. Lioncrest Publishing.*
*Supplementary: Moesta, B. and Spiek, C. (2014). The Jobs-to-Be-Done Handbook. Re-Wired Group.*
*Agent: ux-jtbd-analyst (`skills/ux-jtbd/agents/ux-jtbd-analyst.md`)*
*Constitutional Compliance: P-022 (transparency disclosure), P-001 (source citations), P-020 (user authority)*
*Decision Basis: ADR-PROJ022-001, ADR-PROJ022-002, ORCHESTRATION.yaml (projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml)*
