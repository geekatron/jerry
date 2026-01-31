# Fireflies.ai Competitive Analysis

> **Research Date:** 2026-01-25
> **Research Method:** Live web research (WebSearch, WebFetch)
> **Confidence:** High - based on official documentation and multiple third-party reviews
> **Researcher:** ps-researcher agent
> **Task:** TASK-003
> **Enabler:** EN-001

---

## L0: ELI5 Summary

Fireflies.ai is like a robot assistant that joins your video meetings (Zoom, Google Meet, Teams), listens to everything, and writes down what everyone says. After the meeting, it creates a summary with the important points and things people promised to do. It works in over 100 languages and can search through all your past meetings to find specific conversations. Think of it as a super-smart secretary that never forgets anything from any meeting.

---

## L1: Engineer Summary

Fireflies.ai is an AI-powered meeting transcription and intelligence platform with a multi-stage processing pipeline:

1. **Audio Capture**: Bot joins meetings (Zoom, Meet, Teams, Webex) or ingests uploaded files (MP3, MP4, M4A, WAV)
2. **Speech Recognition**: 95% accuracy transcription across 100+ languages
3. **Speaker Diarization**: Identifies and labels individual speakers (85-90% accuracy)
4. **NLP Analysis**: Extracts action items (~70% accuracy), topics, sentiment, key highlights
5. **Export**: Supports PDF, DOCX, SRT, VTT, JSON formats

The platform exposes a **GraphQL API** at `https://api.fireflies.ai/graphql` with Bearer token authentication. Key capabilities include fetching transcripts, speaker analytics, action items, and meeting summaries programmatically.

**Technical Constraints:**
- Single-language transcription per meeting (no multi-language mixing)
- Storage limits on Free/Pro tiers (800/8000 minutes)
- AI credits consumed by AskFred and advanced summaries

---

## L2: Architect Summary

### Architecture Patterns

Fireflies employs a **cloud-native, API-first architecture** with:

- **GraphQL API Layer**: Single endpoint design for efficient data fetching
- **Pre-built NLP Pipeline**: Sentiment analysis, entity extraction, topic categorization
- **Webhook-based Integration**: POST callbacks with `meetingId` for async processing
- **Multi-tenant SaaS**: Role-based access (admin, user, viewer) with team isolation

### Trade-offs & Design Decisions

| Decision | Benefit | Trade-off |
|----------|---------|-----------|
| GraphQL over REST | Precise data fetching, reduced bandwidth | Steeper learning curve |
| Bot-based capture | Universal platform support | Visible presence may concern participants |
| Pre-built NLP | Zero ML training required | Limited customization |
| Per-seat licensing | Predictable costs | Scales linearly with team size |
| AI credit system | Controls compute costs | User confusion, hidden caps |

### Security & Compliance

- SOC 2 Type II certified
- GDPR compliant with EU data handling
- HIPAA compliant with BAA (Enterprise)
- 256-bit AES encryption, SSL/TLS
- Private dedicated cloud storage option
- Zero data retention for AI training

---

## Feature Analysis

### Core Features

| Feature | Description | Evidence |
|---------|-------------|----------|
| Transcription | 95% accuracy across 100+ languages with auto-language detection | [Fireflies.ai Homepage](https://fireflies.ai) accessed 2026-01-25 |
| AI Summaries | Overviews, bullet points, action items, customized notes | [Fireflies.ai Homepage](https://fireflies.ai) accessed 2026-01-25 |
| AskFred | GPT-powered Q&A over meeting content | [Fireflies.ai Homepage](https://fireflies.ai) accessed 2026-01-25 |
| Smart Search | Filter by speakers, questions, tasks, topics, metrics | [Fireflies API](https://fireflies.ai/api) accessed 2026-01-25 |
| Conversation Intelligence | Talk-time tracking, sentiment analysis, topic tracking | [Outdoo Review](https://www.outdoo.ai/blog/fireflies-ai-review) accessed 2026-01-25 |
| Live Assist | Real-time suggestions and coaching during meetings | [Fireflies.ai Homepage](https://fireflies.ai) accessed 2026-01-25 |
| Talk to Fireflies | Perplexity AI integration for web search during meetings | [MeetGeek Pricing Analysis](https://meetgeek.ai/blog/fireflies-ai-pricing) accessed 2026-01-25 |

### Entity Extraction Capabilities

| Entity Type | Supported | Accuracy | Evidence |
|-------------|-----------|----------|----------|
| Speakers | Yes | 85-90% (Google Meet/Zoom), generic labels for others | [Fireflies API](https://fireflies.ai/api) accessed 2026-01-25 |
| Action Items | Yes | ~70% | [ItsConvo Review](https://www.itsconvo.com/blog/fireflies-ai-review) accessed 2026-01-25 |
| Topics/Keywords | Yes | Not specified | [Bardeen Guide](https://www.bardeen.ai/answers/what-is-fireflies-ai) accessed 2026-01-25 |
| Questions | Yes | Via Smart Search filters | [Max Productive Review](https://max-productive.ai/ai-tools/fireflies-ai/) accessed 2026-01-25 |
| Decisions | Partial | Part of summary/next steps | [Outdoo Review](https://www.outdoo.ai/blog/fireflies-ai-review) accessed 2026-01-25 |
| Sentiment | Yes | Per-speaker percentage | [Fireflies API Docs](https://docs.fireflies.ai/graphql-api/query/transcript) accessed 2026-01-25 |
| Dates/Deadlines | Yes | Via NLP extraction | [Fireflies API](https://fireflies.ai/api) accessed 2026-01-25 |
| Pricing Mentions | Yes | Via NLP extraction | [Fireflies API](https://fireflies.ai/api) accessed 2026-01-25 |

### Transcript Format Support

| Format | Import | Export | Notes | Evidence |
|--------|--------|--------|-------|----------|
| VTT | No | Yes | Download with/without timestamps | [Fireflies Blog](https://fireflies.ai/blog/transcribe-audio-to-text/) accessed 2026-01-25 |
| SRT | No | Yes | For YouTube uploads, paid plans only | [Fireflies SRT Guide](https://fireflies.ai/blog/what-is-an-srt-file/) accessed 2026-01-25 |
| PDF | No | Yes | Standard export option | [Fireflies Knowledge Base](https://guide.fireflies.ai/hc/en-us/articles/360020247558) accessed 2026-01-25 |
| DOCX | No | Yes | Standard export option | [Fireflies Knowledge Base](https://guide.fireflies.ai/hc/en-us/articles/360020247558) accessed 2026-01-25 |
| JSON | No | Yes | API and download | [Fireflies Knowledge Base](https://guide.fireflies.ai/hc/en-us/articles/360020247558) accessed 2026-01-25 |
| MP3 | Yes | No | Audio file upload | [Fireflies Blog](https://fireflies.ai/blog/transcribe-audio-to-text/) accessed 2026-01-25 |
| MP4 | Yes | No | Video file upload | [Fireflies Blog](https://fireflies.ai/blog/transcribe-audio-to-text/) accessed 2026-01-25 |
| WAV | Yes | No | Audio file upload | [Fireflies Blog](https://fireflies.ai/blog/transcribe-audio-to-text/) accessed 2026-01-25 |
| M4A | Yes | No | Audio file upload | [Fireflies Blog](https://fireflies.ai/blog/transcribe-audio-to-text/) accessed 2026-01-25 |

**Note:** VTT/SRT import not supported. Fireflies only imports raw audio/video files, not existing transcript files.

### Integrations

#### Video Conferencing

| Platform | Support Level | Evidence |
|----------|---------------|----------|
| Zoom | Full | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| Google Meet | Full | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| Microsoft Teams | Full | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| Webex | Full | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| GoToMeeting | Full | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| Dialpad | Full | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| Lifesize | Full | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| Slack Huddles | Limited/None | [tldv Review](https://tldv.io/blog/fireflies-review/) accessed 2026-01-25 |

#### CRM

| Platform | Type | Evidence |
|----------|------|----------|
| Salesforce | Bi-directional sync | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| HubSpot | Bi-directional sync | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| Affinity | Bi-directional sync | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| Redtail | Sync | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| Wealthbox | Sync | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |

#### Collaboration & Storage

| Platform | Type | Evidence |
|----------|------|----------|
| Slack | Summary push | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| Notion | Note sync | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| Confluence | Document sync | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| SharePoint | Document sync | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| Google Drive | Storage | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| Dropbox | Storage | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| OneDrive | Storage | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| Box | Storage | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |

#### Project Management

| Platform | Type | Evidence |
|----------|------|----------|
| Asana | Action item sync | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| Trello | Action item sync | [AFFiNE Integration Guide](https://affine.pro/blog/fireflies-ai-integrations-list-tips) accessed 2026-01-25 |
| Jira | Action item sync | [AFFiNE Integration Guide](https://affine.pro/blog/fireflies-ai-integrations-list-tips) accessed 2026-01-25 |
| Linear | Action item sync | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| Airtable | Data sync | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |

#### Dialers

| Platform | Evidence |
|----------|----------|
| Zoom Phone | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| RingCentral | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| Aircall | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| Open Phone | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |

#### ATS (Applicant Tracking)

| Platform | Evidence |
|----------|----------|
| Greenhouse | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| Lever | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |
| BambooHR | [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25 |

**Total Integrations:** 100+ apps claimed ([Fireflies Homepage](https://fireflies.ai))

---

## Pricing

| Tier | Monthly (Annual) | Monthly (Monthly) | Storage | AI Credits | Key Features |
|------|------------------|-------------------|---------|------------|--------------|
| **Free** | $0 | $0 | 800 min/seat | 20 | Limited summaries, 2hr video limit, no downloads |
| **Pro** | $10/seat | $18/seat | 8,000 min/seat | 30 | Unlimited transcription, unlimited summaries, action items, downloads |
| **Business** | $19/seat | $29/seat | Unlimited | 50 | Video recording (3hr), multi-language, conversation intelligence, team analytics |
| **Enterprise** | $39/seat | Custom | Unlimited | 30 | Rules engine, SSO, SCIM, HIPAA, private storage, dedicated AM |

**Source:** [Fireflies Pricing Page](https://fireflies.ai/pricing) accessed 2026-01-25

### Hidden Costs

- **AI Credit Packs:** $5 for 50 credits, up to $600 for bulk — [MeetGeek Analysis](https://meetgeek.ai/blog/fireflies-ai-pricing) accessed 2026-01-25
- **Storage Overages:** Pro tier has 8,000 min cap despite "unlimited transcription" — [Lindy Analysis](https://www.lindy.ai/blog/fireflies-ai-pricing) accessed 2026-01-25
- **CRM Integrations:** Advanced features gated behind Business/Enterprise — [CloudEagle Guide](https://www.cloudeagle.ai/blogs/blogs-fireflies-ai-pricing-guide) accessed 2026-01-25

---

## API Access

### Endpoint
```
https://api.fireflies.ai/graphql
```

### Authentication
- Bearer token via `Authorization: Bearer {api_key}` header
- API keys generated in Fireflies dashboard

### Key Queries

| Query | Purpose | Evidence |
|-------|---------|----------|
| `transcript(id: String!)` | Fetch single transcript with full details | [Fireflies API Docs](https://docs.fireflies.ai/graphql-api/query/transcript) accessed 2026-01-25 |
| `transcripts` | List all transcripts (id, title, created_at) | [Fireflies API Docs](https://docs.fireflies.ai/) accessed 2026-01-25 |
| `user` | Get user info, roles, usage | [Fireflies API](https://fireflies.ai/api) accessed 2026-01-25 |

### Transcript Query Response Fields

```graphql
{
  id, title, dateString, date, duration, privacy
  transcript_url, audio_url, video_url
  speakers { name, duration, word_count, sentiment }
  sentences { text, speaker_name, start_time, end_time, ai_filters }
  summary { keywords, action_items, outline, overview, topics_discussed }
  analytics { sentiments, categories }
  meeting_attendees, meeting_attendance
  calendar_info, channel
}
```

**Source:** [Fireflies Transcript Query Docs](https://docs.fireflies.ai/graphql-api/query/transcript) accessed 2026-01-25

### Webhooks

- POST callback with `meetingId` on transcription completion
- Use `meetingId` to fetch full transcript via API

**Source:** [Rollout Integration Guide](https://rollout.com/integration-guides/fireflies.ai/api-essentials) accessed 2026-01-25

### Limitations

- Rate limits not publicly documented
- API actively expanding per official docs — [Fireflies API Docs](https://docs.fireflies.ai/) accessed 2026-01-25

---

## Strengths

1. **High Transcription Accuracy (95%)** — Superior to Zoom's 70-80% native transcription — [Fireflies Blog](https://fireflies.ai/blog/transcribe-audio-to-text/) accessed 2026-01-25

2. **Extensive Language Support (100+ languages)** — Auto-language detection with 60+ supported for transcription — [Fireflies Homepage](https://fireflies.ai) accessed 2026-01-25

3. **Comprehensive Integration Ecosystem (100+ apps)** — Deep CRM, project management, and storage integrations — [Fireflies Integrations](https://fireflies.ai/integrations) accessed 2026-01-25

4. **Powerful GraphQL API** — Flexible data fetching, custom NLP layer access, webhook support — [Fireflies API Docs](https://docs.fireflies.ai/) accessed 2026-01-25

5. **Enterprise-Grade Security** — SOC 2 Type II, GDPR, HIPAA, zero AI training data retention — [Fireflies API](https://fireflies.ai/api) accessed 2026-01-25

6. **Real-time Features** — Live note generation during calls, Talk to Fireflies (Perplexity integration) — [MeetGeek Analysis](https://meetgeek.ai/blog/fireflies-ai-pricing) accessed 2026-01-25

7. **Multi-format Export** — VTT, SRT, PDF, DOCX, JSON options — [Fireflies Knowledge Base](https://guide.fireflies.ai/hc/en-us/articles/360020247558) accessed 2026-01-25

---

## Weaknesses

1. **No VTT/SRT Import** — Cannot process existing transcript files, only raw audio/video — [Fireflies Blog](https://fireflies.ai/blog/transcribe-audio-to-text/) accessed 2026-01-25

2. **Single-Language Limitation** — Cannot transcribe multiple languages in same meeting — [Cosmo Edge Review](https://cosmo-edge.com/fireflies-ai-user-reviews/) accessed 2026-01-25

3. **Confusing AI Credit System** — Hidden caps even on "unlimited" plans, credit pack upsells — [MeetGeek Analysis](https://meetgeek.ai/blog/fireflies-ai-pricing) accessed 2026-01-25

4. **Storage Caps on Lower Tiers** — Free (800 min), Pro (8000 min) despite "unlimited transcription" marketing — [Lindy Analysis](https://www.lindy.ai/blog/fireflies-ai-pricing) accessed 2026-01-25

5. **Action Item Accuracy (~70%)** — Requires manual review and correction — [ItsConvo Review](https://www.itsconvo.com/blog/fireflies-ai-review) accessed 2026-01-25

6. **English-Only Interface** — No localization for global teams — [tldv Review](https://tldv.io/blog/fireflies-review/) accessed 2026-01-25

7. **Limited Slack Huddles/Webex Support** — Platform gaps for some communication tools — [tldv Review](https://tldv.io/blog/fireflies-review/) accessed 2026-01-25

8. **Bot Visibility Concerns** — Joins meetings visibly, may concern participants — [Outdoo Review](https://www.outdoo.ai/blog/fireflies-ai-review) accessed 2026-01-25

9. **Unidirectional CRM Sync** — Can push to CRMs but limited customization of what gets synced — [MeetGeek Analysis](https://meetgeek.ai/blog/fireflies-ai-pricing) accessed 2026-01-25

10. **Slower Development Pace** — Some critics note platform feels dated compared to newer competitors — [Breakcold Review](https://www.breakcold.com/blog/fireflies-ai-review) accessed 2026-01-25

---

## Competitive Positioning for Transcript Skill

### Relevance to Jerry Transcript Skill

| Fireflies Capability | Relevance | Notes |
|---------------------|-----------|-------|
| VTT/SRT Export | Medium | We need import, they only export |
| Entity Extraction | High | Benchmark for action items, topics, speakers |
| GraphQL API | High | Architectural pattern to consider |
| NLP Layer | High | Pre-built extraction is a key differentiator |
| Multi-format support | Medium | Our focus is VTT/SRT specifically |

### Gaps Our Skill Could Fill

1. **VTT/SRT Import & Parse** — Fireflies cannot import existing transcripts
2. **Multi-language Meeting Support** — Fireflies limited to single language
3. **Offline Processing** — Fireflies is cloud-only
4. **Custom Entity Extraction** — Fireflies NLP is pre-built, limited customization
5. **Developer-First CLI** — Fireflies has no CLI, only API

---

## References

1. [Fireflies.ai Homepage](https://fireflies.ai) - Accessed 2026-01-25
2. [Fireflies.ai Pricing](https://fireflies.ai/pricing) - Accessed 2026-01-25
3. [Fireflies.ai API](https://fireflies.ai/api) - Accessed 2026-01-25
4. [Fireflies.ai Integrations](https://fireflies.ai/integrations) - Accessed 2026-01-25
5. [Fireflies API Documentation](https://docs.fireflies.ai/) - Accessed 2026-01-25
6. [Fireflies Transcript Query Docs](https://docs.fireflies.ai/graphql-api/query/transcript) - Accessed 2026-01-25
7. [MeetGeek - Fireflies AI Pricing 2026](https://meetgeek.ai/blog/fireflies-ai-pricing) - Accessed 2026-01-25
8. [Outdoo - Fireflies AI Review 2026](https://www.outdoo.ai/blog/fireflies-ai-review) - Accessed 2026-01-25
9. [Lindy - Fireflies.ai Pricing 2026](https://www.lindy.ai/blog/fireflies-ai-pricing) - Accessed 2026-01-25
10. [tldv - Fireflies.ai Review 2026](https://tldv.io/blog/fireflies-review/) - Accessed 2026-01-25
11. [ItsConvo - Fireflies AI Review 2025](https://www.itsconvo.com/blog/fireflies-ai-review) - Accessed 2026-01-25
12. [Breakcold - Fireflies.ai Review 2026](https://www.breakcold.com/blog/fireflies-ai-review) - Accessed 2026-01-25
13. [AFFiNE - Fireflies.ai Integrations](https://affine.pro/blog/fireflies-ai-integrations-list-tips) - Accessed 2026-01-25
14. [CloudEagle - Fireflies Pricing Guide](https://www.cloudeagle.ai/blogs/blogs-fireflies-ai-pricing-guide) - Accessed 2026-01-25
15. [Bardeen - Fireflies.ai Guide](https://www.bardeen.ai/answers/what-is-fireflies-ai) - Accessed 2026-01-25
16. [Max Productive - Fireflies.ai Review 2025](https://max-productive.ai/ai-tools/fireflies-ai/) - Accessed 2026-01-25
17. [Cosmo Edge - Fireflies.ai User Reviews](https://cosmo-edge.com/fireflies-ai-user-reviews/) - Accessed 2026-01-25
18. [Fireflies Blog - SRT Guide](https://fireflies.ai/blog/what-is-an-srt-file/) - Accessed 2026-01-25
19. [Rollout - Fireflies API Essentials](https://rollout.com/integration-guides/fireflies.ai/api-essentials) - Accessed 2026-01-25
20. [Fireflies Knowledge Base](https://guide.fireflies.ai/hc/en-us/articles/360020247558) - Accessed 2026-01-25
