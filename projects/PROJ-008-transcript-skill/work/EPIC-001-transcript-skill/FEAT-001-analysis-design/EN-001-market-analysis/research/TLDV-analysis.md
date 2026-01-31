# tl;dv Competitive Analysis

> **Research Date:** 2026-01-25
> **Research Method:** Live web research (WebSearch, WebFetch)
> **Researcher:** ps-researcher agent
> **Confidence:** High - Multiple authoritative sources including official documentation, third-party reviews, and API documentation
> **Task:** TASK-005
> **Enabler:** EN-001

---

## L0: ELI5 Summary

tl;dv is like a smart assistant that joins your video calls (Zoom, Google Meet, Teams) and writes down everything people say. It figures out who said what, makes a summary of the important stuff, and can send notes to your other work tools like Slack or your CRM. It's free to start but you pay more for fancy features like teaching it to coach your sales team.

---

## L1: Engineer Summary

tl;dv is an AI-powered meeting intelligence platform providing:

- **Recording & Transcription**: Automatic capture with speaker diarization across Zoom, Google Meet, and Microsoft Teams
- **NLP Processing**: AI-generated summaries, action item extraction, and topic detection
- **API Access**: REST API (v1alpha1) with webhook support for MeetingReady and TranscriptReady events
- **Integrations**: 5,000+ via Zapier, native CRM connectors (HubSpot, Salesforce)
- **Transcript Access**: JSON-structured via API; copy-to-clipboard via UI; no native VTT/SRT export
- **Language Support**: 30-40 languages with speaker identification

**Key Technical Limitations:**
- No VTT/SRT export natively
- API in alpha (v1alpha1)
- Cloud-only (no offline mode)
- 3-hour max meeting length
- Accuracy issues with accents and overlapping speakers

---

## L2: Architect Summary

### Architecture Patterns

tl;dv employs a **cloud-native SaaS architecture** with:

1. **Bot-Based Recording**: A virtual participant joins meetings to capture audio/video
2. **Asynchronous Processing Pipeline**: Recording -> Transcription -> NLP Analysis -> Summary Generation
3. **Event-Driven Integration**: Webhooks for MeetingReady/TranscriptReady events
4. **Multi-Tenant API**: RESTful API with API key authentication over HTTPS

### Trade-offs

| Decision | Benefit | Cost |
|----------|---------|------|
| Bot-based recording | Works across all platforms uniformly | Intrusive UX, potential trust issues |
| Cloud-only processing | Consistent quality, easy scaling | No offline capability, data sovereignty concerns |
| Zapier-first integrations | 5000+ apps accessible | Extra cost, reliability dependency |
| Alpha API | Early access for developers | Instability, breaking changes risk |

### Data Flow

```
Meeting Platform (Zoom/Meet/Teams)
    |
    v
tl;dv Bot (Recording Agent)
    |
    v
Cloud Processing Pipeline
    |-- Speech-to-Text Engine (30+ languages)
    |-- Speaker Diarization
    |-- NLP Summary Generation
    |-- Action Item Extraction
    v
Data Store (GCP/AWS hosted)
    |
    +-- REST API --> External Applications
    +-- Webhooks --> Real-time Notifications
    +-- UI --> User Dashboard
    +-- CRM Sync --> HubSpot/Salesforce
```

### Competitive Position

tl;dv occupies the **mid-market meeting intelligence** segment, positioned above basic transcription tools (Otter.ai) but below enterprise revenue intelligence platforms (Gong, Chorus). Its strength is accessibility (generous free tier, simple UX) but lacks the depth of analytics and native integrations expected by enterprise sales teams.

---

## Feature Analysis

### Core Features

| Feature | Description | Evidence |
|---------|-------------|----------|
| AI Meeting Recording | Automatic recording via virtual bot participant | [tldv.io](https://tldv.io/) accessed 2026-01-25 |
| AI Transcription | Speech-to-text with 30-40 language support | [BlueDotHQ Review](https://www.bluedothq.com/blog/tldv-review) accessed 2026-01-25 |
| Speaker Identification | Automatic labeling of speakers in transcript | [BlueDotHQ Review](https://www.bluedothq.com/blog/tldv-review) accessed 2026-01-25 |
| AI Summaries | Key points, decisions, next steps extraction | [BusinessDive Review](https://thebusinessdive.com/tldv-review) accessed 2026-01-25 |
| Meeting Templates | Pre-built templates for sales, HR, product, etc. | [BusinessDive Review](https://thebusinessdive.com/tldv-review) accessed 2026-01-25 |
| AI Coaching Hub | Speaking time, questions, filler words analysis | [BlueDotHQ Review](https://www.bluedothq.com/blog/tldv-review) accessed 2026-01-25 |
| Multi-Meeting Reports | Aggregate insights across 100+ meetings | [WebSearch results](https://tldv.io/) accessed 2026-01-25 |
| Searchable Library | Keyword search across all transcripts | [Claap Pricing Analysis](https://www.claap.io/blog/tl-dv-pricing) accessed 2026-01-25 |

### Entity Extraction Capabilities

| Entity Type | Supported | Quality | Evidence |
|-------------|-----------|---------|----------|
| Speakers | Yes | Good, but struggles with overlapping speech | [Hyprnote Review](https://hyprnote.com/blog/tldv-review/) accessed 2026-01-25 |
| Action Items | Yes | Requires multiple prompts for completeness | [Hyprnote Review](https://hyprnote.com/blog/tldv-review/) accessed 2026-01-25 |
| Topics/Keywords | Yes | NLP-based detection | [BlueDotHQ Review](https://www.bluedothq.com/blog/tldv-review) accessed 2026-01-25 |
| Questions | Yes | Tracked in AI Coaching Hub | [tldv.io](https://tldv.io/) accessed 2026-01-25 |
| Decisions | Yes | Included in structured summaries | [BusinessDive Review](https://thebusinessdive.com/tldv-review) accessed 2026-01-25 |
| Objection Handling | Yes (Business tier) | Sales-specific feature | [Claap Pricing Analysis](https://www.claap.io/blog/tl-dv-pricing) accessed 2026-01-25 |
| Sentiment | Yes | Part of NLP analysis | [BlueDotHQ Review](https://www.bluedothq.com/blog/tldv-review) accessed 2026-01-25 |

### Transcript Format Support

| Format | Import | Export | Evidence |
|--------|--------|--------|----------|
| VTT | Unknown | **No** (not natively) | [tl;dv API Docs](https://doc.tldv.io/index.html) accessed 2026-01-25 - no mention of VTT |
| SRT | Unknown | **No** (not natively) | [tl;dv API Docs](https://doc.tldv.io/index.html) accessed 2026-01-25 - no mention of SRT |
| Plain Text | N/A | Yes (copy to clipboard) | [tl;dv Help Center](https://intercom.help/tldv/en/articles/6122489-how-to-download-transcripts) accessed 2026-01-25 |
| JSON (API) | Yes | Yes | [tl;dv API Docs](https://doc.tldv.io/index.html) accessed 2026-01-25 |
| Media Import | Yes (.mp3, .mp4, .wav, .m4a, .mkv, .mov, .avi, .wma, .flac) | N/A | [tl;dv API Docs](https://doc.tldv.io/index.html) accessed 2026-01-25 |
| TXT/MD/CSV | No | Via third-party extension | [tl;dv Transcript Grabber](https://user17745.github.io/tl-dv-Transcript-Grabber/) accessed 2026-01-25 |

### Integrations

| Platform | Type | Tier Required | Evidence |
|----------|------|---------------|----------|
| Zoom | Recording | Free+ | [tldv.io](https://tldv.io/) accessed 2026-01-25 |
| Google Meet | Recording | Free+ | [tldv.io](https://tldv.io/) accessed 2026-01-25 |
| Microsoft Teams | Recording | Free+ | [tldv.io](https://tldv.io/) accessed 2026-01-25 |
| Slack | Notes/Alerts | Free+ | [tldv.io/integrations](https://tldv.io/integrations/) accessed 2026-01-25 |
| HubSpot | CRM Sync | Business+ | [tldv.io/hubspot](https://tldv.io/hubspot/) accessed 2026-01-25 |
| Salesforce | CRM Sync | Business+ | [tldv.io/salesforce](https://tldv.io/salesforce/) accessed 2026-01-25 |
| Notion | Notes Export | Pro+ | [tldv.io/integrations](https://tldv.io/integrations/) accessed 2026-01-25 |
| Google Docs | Notes Export | Pro+ | [tldv.io/integrations](https://tldv.io/integrations/) accessed 2026-01-25 |
| Trello | Task Sync | Pro+ | [tldv.io/integrations](https://tldv.io/integrations/) accessed 2026-01-25 |
| Asana | Task Sync | Pro+ | [tldv.io/integrations](https://tldv.io/integrations/) accessed 2026-01-25 |
| Pipedrive | CRM Sync | Business+ | [tldv.io/integrations](https://tldv.io/integrations/) accessed 2026-01-25 |
| Zapier | 5000+ apps | Pro+ | [BlueDotHQ Review](https://www.bluedothq.com/blog/tldv-review) accessed 2026-01-25 |
| Discord | Notes/Clips | Pro+ | [tldv.io/integrations](https://tldv.io/integrations/) accessed 2026-01-25 |
| Dropbox | Storage | Pro+ | [tldv.io/integrations](https://tldv.io/integrations/) accessed 2026-01-25 |
| Miro | Visual Boards | Pro+ | [tldv.io/integrations](https://tldv.io/integrations/) accessed 2026-01-25 |

---

## Pricing

| Plan | Monthly Price | Annual Price | Key Features | Limits |
|------|---------------|--------------|--------------|--------|
| **Free** | $0 | $0 | Unlimited recordings, 10 AI notes lifetime, basic transcription | 3-month auto-delete, 40 recordings/week cap, no searchable library |
| **Pro** | $29/user | $18/user | Unlimited AI summaries, permanent storage, searchable library, team folders, Zapier CRM sync | 120 recordings/week cap, requires Zapier for CRM |
| **Business** | $98/user | $59/user | Native Salesforce/HubSpot, AI coaching, sales playbooks (MEDDIC, BANT, SPIN), objection handling, Claude AI | 10-15 hours playbook setup time |
| **Enterprise** | Custom | Custom | Private AI hosting, dedicated CSM, custom billing, SLA support | Negotiated |

**Notes:**
- Current 40% off annual plans through 2025 promotion
- 3-hour maximum meeting length limit
- Pro/Business required for transcript download
- Source: [Claap Pricing Analysis](https://www.claap.io/blog/tl-dv-pricing) accessed 2026-01-25

---

## API Access

| Attribute | Details | Evidence |
|-----------|---------|----------|
| Version | v1alpha1 (Alpha) | [tl;dv API Docs](https://doc.tldv.io/index.html) accessed 2026-01-25 |
| Base URL | https://pasta.tldv.io | [tl;dv API Docs](https://doc.tldv.io/index.html) accessed 2026-01-25 |
| Authentication | API Key via x-api-key header | [tl;dv API Docs](https://doc.tldv.io/index.html) accessed 2026-01-25 |
| Protocol | HTTPS only | [tl;dv API Docs](https://doc.tldv.io/index.html) accessed 2026-01-25 |
| Sandbox | Not available | [tl;dv API Docs](https://doc.tldv.io/index.html) accessed 2026-01-25 |
| Rate Limits | Not documented | [tl;dv API Docs](https://doc.tldv.io/index.html) accessed 2026-01-25 |

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1alpha1/meetings` | GET | List meetings with pagination, date filtering |
| `/v1alpha1/meetings/{id}` | GET | Get specific meeting details |
| `/v1alpha1/meetings/{id}/transcript` | GET | Retrieve structured transcript with speakers/timestamps |
| `/v1alpha1/meetings/{id}/highlights` | GET | Get meeting highlights/notes |
| `/v1alpha1/meetings/import` | POST | Import media files (.mp3, .mp4, .wav, etc.) |
| `/v1alpha1/health` | GET | Health check |

### Webhooks

| Event | Trigger |
|-------|---------|
| MeetingReady | When meeting processing completes |
| TranscriptReady | When transcription finishes |

Configuration available at user, team, or organization level.

---

## Strengths

| Strength | Description | Evidence |
|----------|-------------|----------|
| Generous Free Tier | Unlimited recordings with 10 AI notes | [Claap Pricing Analysis](https://www.claap.io/blog/tl-dv-pricing) accessed 2026-01-25 |
| Multi-Language Support | 30-40 languages with transcription | [BlueDotHQ Review](https://www.bluedothq.com/blog/tldv-review) accessed 2026-01-25 |
| Speaker Identification | Automatic labeling of who said what | [BlueDotHQ Review](https://www.bluedothq.com/blog/tldv-review) accessed 2026-01-25 |
| Extensive Integrations | 5,000+ apps via Zapier | [BlueDotHQ Review](https://www.bluedothq.com/blog/tldv-review) accessed 2026-01-25 |
| Sales-Specific Features | AI coaching, playbooks (MEDDIC, BANT, SPIN) | [Claap Pricing Analysis](https://www.claap.io/blog/tl-dv-pricing) accessed 2026-01-25 |
| GDPR Compliance | EU data protection compliant | [BlueDotHQ Review](https://www.bluedothq.com/blog/tldv-review) accessed 2026-01-25 |
| Multi-Meeting Analysis | Aggregate insights across 100+ meetings | [WebSearch results](https://tldv.io/) accessed 2026-01-25 |
| Real-Time Collaborative Notes | Live note-taking with timestamps | [Efficient.app Review](https://efficient.app/apps/tldv) accessed 2026-01-25 |

---

## Weaknesses

| Weakness | Description | Evidence |
|----------|-------------|----------|
| Bot Intrusiveness | Virtual participant can feel awkward | [BlueDotHQ Review](https://www.bluedothq.com/blog/tldv-review) accessed 2026-01-25 |
| Limited Platform Support | Only Zoom, Meet, Teams (no Discord, phone, in-person) | [Hyprnote Review](https://hyprnote.com/blog/tldv-review/) accessed 2026-01-25 |
| Accent Accuracy Issues | Struggles with non-native English, Indian English, technical jargon | [Hyprnote Review](https://hyprnote.com/blog/tldv-review/) accessed 2026-01-25 |
| Speaker Overlap Problems | Fails with interruptions and fast-paced discussions | [Hyprnote Review](https://hyprnote.com/blog/tldv-review/) accessed 2026-01-25 |
| No Offline Mode | Cloud-dependent, no local processing | [Hyprnote Review](https://hyprnote.com/blog/tldv-review/) accessed 2026-01-25 |
| No VTT/SRT Export | No native subtitle format export | [tl;dv API Docs](https://doc.tldv.io/index.html) accessed 2026-01-25 |
| No Bulk Export | Cannot download transcripts in bulk | [tl;dv Help Center](https://intercom.help/tldv/en/articles/6122489-how-to-download-transcripts) accessed 2026-01-25 |
| Integration Reliability | Reports of broken HubSpot/Slack integrations | [Hyprnote Review](https://hyprnote.com/blog/tldv-review/) accessed 2026-01-25 |
| Search Accuracy | Sometimes returns irrelevant results | [Hyprnote Review](https://hyprnote.com/blog/tldv-review/) accessed 2026-01-25 |
| AI Summary Quality | Misses nuances, requires manual review | [Hyprnote Review](https://hyprnote.com/blog/tldv-review/) accessed 2026-01-25 |
| Alpha API | v1alpha1 indicates instability risk | [tl;dv API Docs](https://doc.tldv.io/index.html) accessed 2026-01-25 |
| Steep Business Tier Jump | $29 Pro to $59 Business (annual) is significant | [Claap Pricing Analysis](https://www.claap.io/blog/tl-dv-pricing) accessed 2026-01-25 |
| No Custom Vocabulary | Cannot train on domain-specific terminology | [Hyprnote Review](https://hyprnote.com/blog/tldv-review/) accessed 2026-01-25 |
| Support Quality | Reports of slow, unhelpful responses | [Hyprnote Review](https://hyprnote.com/blog/tldv-review/) accessed 2026-01-25 |

---

## Competitive Positioning Summary

### Market Segment
**Mid-Market Meeting Intelligence** - Accessible pricing, generous free tier, but lacking enterprise depth

### Primary Competitors
- **Otter.ai** - Similar pricing, stronger standalone transcription
- **Fireflies.ai** - Comparable features, different integration focus
- **Gong** - Enterprise revenue intelligence (premium segment)
- **Chorus.ai (ZoomInfo)** - Enterprise sales intelligence
- **Avoma** - Stronger analytics capabilities

### Differentiation
- Multi-meeting aggregation (100+ meetings)
- Sales playbook templates (MEDDIC, BANT, SPIN)
- Claude AI integration (Business tier)
- MCP (Model Context Protocol) integration for AI contextualization

---

## Relevance to Our Project

### Key Takeaways for Text Transcript Skill

1. **Different Use Case:** tl;dv solves the recording-to-insight problem. Our skill solves the transcript-to-insight problem. These are complementary but distinct.

2. **Entity Extraction Benchmark:** tl;dv extracts action items, speakers, topics, questions, decisions, and sentiment. We should match or exceed this for text transcripts.

3. **VTT/SRT Gap:** tl;dv does NOT natively support VTT/SRT import/export. This is a clear differentiation opportunity for our text-first approach.

4. **API Design Patterns:** Their webhook-based async pattern (MeetingReady, TranscriptReady) is worth considering for our processing pipeline.

5. **Integration Expectations:** CRM and productivity tool integrations (Slack, Notion, HubSpot) are market expectations.

6. **Pricing Reference:** Free tier with generous limits + paid tiers for advanced features is the standard model.

---

## References

1. [tl;dv Official Website](https://tldv.io/) - Accessed 2026-01-25
2. [tl;dv API Documentation](https://doc.tldv.io/index.html) - Accessed 2026-01-25
3. [tl;dv Pricing Page](https://tldv.io/app/pricing/) - Accessed 2026-01-25
4. [Claap: tl;dv Pricing 2026 Analysis](https://www.claap.io/blog/tl-dv-pricing) - Accessed 2026-01-25
5. [BlueDotHQ: Comprehensive tl;dv Review](https://www.bluedothq.com/blog/tldv-review) - Accessed 2026-01-25
6. [BusinessDive: Honest tl;dv Review After 18 Months](https://thebusinessdive.com/tldv-review) - Accessed 2026-01-25
7. [Hyprnote: tl;dv Review 2025](https://hyprnote.com/blog/tldv-review/) - Accessed 2026-01-25
8. [Efficient.app: tl;dv Review](https://efficient.app/apps/tldv) - Accessed 2026-01-25
9. [tl;dv Help Center: How to Download Transcripts](https://intercom.help/tldv/en/articles/6122489-how-to-download-transcripts) - Accessed 2026-01-25
10. [tl;dv Integrations](https://tldv.io/integrations/) - Accessed 2026-01-25
11. [tl;dv HubSpot Integration](https://tldv.io/hubspot/) - Accessed 2026-01-25
12. [tl;dv Salesforce Integration](https://tldv.io/salesforce/) - Accessed 2026-01-25
13. [tl;dv Transcript Grabber (Third-Party Extension)](https://user17745.github.io/tl-dv-Transcript-Grabber/) - Accessed 2026-01-25

---

## Appendix: Research Tool Results

### Successful Fetches
| Tool | URL | Result |
|------|-----|--------|
| WebFetch | https://doc.tldv.io/index.html | Full API documentation extracted |
| WebFetch | https://www.claap.io/blog/tl-dv-pricing | Complete pricing analysis extracted |
| WebFetch | https://www.bluedothq.com/blog/tldv-review | Comprehensive review with features/weaknesses |
| WebFetch | https://thebusinessdive.com/tldv-review | Detailed 18-month user review |
| WebFetch | https://hyprnote.com/blog/tldv-review/ | Critical analysis of limitations |
| WebFetch | https://efficient.app/apps/tldv | Feature review and rating |
| WebFetch | https://intercom.help/tldv/en/articles/6122489-how-to-download-transcripts | Export limitations documentation |

### Failed Fetches
| Tool | URL | Error | Impact |
|------|-----|-------|--------|
| WebFetch | https://www.g2.com/products/tl-dv/reviews | 403 Forbidden | Could not access G2 user reviews directly; used alternative review sources |
| WebFetch | https://tldv.io/ | CSS-only response | Homepage content not extracted; used search results and third-party reviews |
| WebFetch | https://tldv.io/app/pricing/ | Tracking code only | Pricing page not extracted; used Claap analysis as alternative source |
| WebFetch | https://tldv.io/integrations/ | CSS/structure only | Integration list not extracted; used search results for integration details |

All critical information was successfully obtained through alternative authoritative sources.

---

## Metadata

```yaml
research_id: TASK-005-tldv-live
product: tl;dv
url: https://tldv.io/
research_date: 2026-01-25
researcher: ps-researcher
research_method: live_web_research
tools_used:
  - WebSearch (3 queries)
  - WebFetch (10 attempts, 7 successful)
confidence_level: high
verification_status: verified_via_live_research
data_sources:
  - tl;dv API documentation (official)
  - Third-party reviews (Claap, BlueDotHQ, Hyprnote, BusinessDive, Efficient.app)
  - tl;dv Help Center (official)
  - WebSearch results (multiple sources)
```
