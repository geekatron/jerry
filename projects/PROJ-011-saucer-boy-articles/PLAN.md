# PROJ-011: Saucer Boy Articles — Publication Pipeline

> High-quality articles written in the Saucer Boy (McConkey) voice, covering LLM engineering, prompting, and framework topics. Each article goes through C4 adversarial quality gates before publication.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Project scope and goals |
| [Article Pipeline](#article-pipeline) | How articles are produced |
| [Articles](#articles) | Article registry |
| [Quality Standards](#quality-standards) | Publication bar |

---

## Overview

PROJ-011 is the home for Saucer Boy articles — practitioner-facing content written in the McConkey voice that explains technical LLM concepts with personality, precision, and evidence. Every article passes through the full Jerry quality pipeline: creator-critic-revision cycles with C4 adversarial review, LLM-tell detection, and voice authenticity scoring.

## Article Pipeline

1. **Creator:** Saucer Boy voice (sb-voice agent) produces the draft
2. **Adversarial Review:** C4 all-strategy review with individual background agents
3. **Quality Gate:** >= 0.95 weighted composite (S-014 LLM-as-Judge)
4. **LLM-Tell Detection:** Dedicated pass to strip AI-generated indicators
5. **Voice Authenticity:** McConkey persona compliance check
6. **Human Review:** Semi-supervised — human gates at each iteration
7. **Publication:** Final artifact + citations companion

## Articles

| ID | Title | Status | Score |
|----|-------|--------|-------|
| ART-001 | Why Structured Prompting Works | IN PROGRESS | 0.938 (pre-humanization) |

## Quality Standards

- Content quality: >= 0.95 (S-014 6-dimension rubric)
- LLM-tell score: >= 0.95 (dedicated detection pass)
- Voice authenticity: >= 0.95 (Saucer Boy persona compliance)
- All three must pass independently before publication
