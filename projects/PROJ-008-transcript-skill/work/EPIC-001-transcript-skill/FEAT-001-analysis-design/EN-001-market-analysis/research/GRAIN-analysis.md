# Grain Competitive Analysis

> **Research Date:** 2026-01-25
> **Task:** TASK-004
> **Enabler:** EN-001
> **Agent:** ps-researcher
> **Research Method:** Live web research (WebSearch, WebFetch)
> **Confidence:** High (based on official website, multiple third-party reviews, and API documentation)
> **Product URL:** https://grain.com/

---

## L0: ELI5 Summary

Grain is like a smart robot that joins your video meetings and takes notes for you. It records everything that's said, writes it down (transcription), and figures out the important parts like who said what, what needs to be done next, and the key points. You can then share little video clips of the best moments with your team, and it automatically updates your sales tools with the meeting information.

---

## L1: Engineer Summary

Grain is an AI-powered meeting intelligence platform that provides:

- **Automatic recording and transcription** across Zoom, Google Meet, Microsoft Teams, and Webex
- **AI-generated meeting notes** with customizable templates
- **Entity extraction**: action items with assignees, key points, summaries, and chapter segmentation
- **Video highlighting**: create and share timestamped clips from recordings
- **CRM integration**: automatic sync to HubSpot and Salesforce
- **Export formats**: PDF, SRT, VTT, DOCX
- **MCP (Model Context Protocol) server** for integration with Claude, Cursor, and other AI tools
- **API access** via `https://api.grain.com/_/public-api/` with OAuth authentication
- **Webhook support** for recordings, highlights, and stories

Key technical limitations:
- Requires a visible recording bot (no stealth mode)
- Cross-meeting analysis is limited (individual meeting focus)
- Real-time transcription is English-only (post-meeting supports 100+ languages)

---

## L2: Architect Summary

### Architecture Pattern
Grain follows a **SaaS video-centric meeting intelligence model** with:
- Bot-based recording (joins as meeting participant)
- Cloud-based transcription and AI processing
- REST API with OAuth 2.0 authentication
- Webhook-based event streaming (recordings, highlights, stories)
- MCP server for LLM integration (Claude, Cursor, ChatGPT)

### Integration Architecture
```
+-------------------+     +--------------+     +-------------------+
| Video Platforms   |---->|   Grain      |---->| Downstream        |
| Zoom/Meet/Teams   |     |   Cloud      |     | Systems           |
+-------------------+     |              |     | - CRM (HubSpot)   |
                          | +----------+ |     | - Slack           |
                          | |Recording | |     | - Zapier          |
                          | |Engine    | |     | - MCP Clients     |
                          | +----+-----+ |     +-------------------+
                          |      |       |
                          |      v       |
                          | +----------+ |     +-------------------+
                          | |AI/NLP    | |---->| Exports           |
                          | |Pipeline  | |     | VTT/SRT/PDF/DOCX  |
                          | +----------+ |     +-------------------+
                          +--------------+
```

### Trade-offs
| Decision | Trade-off |
|----------|-----------|
| Bot-based recording | Transparency vs. participant discomfort |
| Video-centric model | Rich context vs. larger storage/bandwidth |
| Cloud processing | Scalability vs. data privacy concerns |
| MCP integration | LLM flexibility vs. vendor coupling |

### Key Differentiators
1. **Video-first**: Unlike text-only competitors, emphasizes shareable video clips
2. **MCP support**: Native integration with modern AI assistants
3. **Sales-optimized**: Deep CRM sync, deal boards, coaching features

---

## Feature Analysis

### Core Features

| Feature | Description | Evidence |
|---------|-------------|----------|
| AI Meeting Notes | Automatic transcription with AI-generated summaries | [Grain Homepage](https://grain.com/) accessed 2026-01-25 |
| Video Recording | Captures full meeting video with playback | [Grain Transcription](https://grain.com/transcription) accessed 2026-01-25 |
| Highlight Clips | Create and share timestamped video segments | [Grain Homepage](https://grain.com/) accessed 2026-01-25 |
| CRM Sync | Auto-populate HubSpot/Salesforce with meeting data | [Grain Integrations](https://grain.com/integrations) accessed 2026-01-25 |
| Custom Templates | Tailor notes format for different meeting types | [Grain Homepage](https://grain.com/) accessed 2026-01-25 |
| Ask AI | Query across all meetings with citations | [Grain Homepage](https://grain.com/) accessed 2026-01-25 |
| Tracker | Monitor specific words/phrases across calls | [Claap Blog](https://www.claap.io/blog/grain-pricing) accessed 2026-01-25 |

### Entity Extraction Capabilities

| Entity Type | Supported | Evidence |
|-------------|-----------|----------|
| Speakers | Yes | Speaker diarization mentioned in [TrustRadius](https://www.trustradius.com/products/grain/reviews) accessed 2026-01-25 |
| Action Items | Yes | "Automatically identified action items and assignees" - [Grain Homepage](https://grain.com/) accessed 2026-01-25 |
| Topics/Keywords | Yes | "Tracker functionality for monitoring specific terms/phrases" - [Grain Homepage](https://grain.com/) accessed 2026-01-25 |
| Questions | Unknown | Not explicitly documented |
| Decisions | Yes | "Meeting outcomes and decisions" identified - [Grain Homepage](https://grain.com/) accessed 2026-01-25 |
| Chapters | Yes | "Smart chapters" mentioned in [ProductiveWithChris](https://productivewithchris.com/tools/grain/) accessed 2026-01-25 |

### Transcript Format Support

| Format | Import | Export | Evidence |
|--------|--------|--------|----------|
| VTT | Unknown | Yes | [Grain Transcription](https://grain.com/transcription) mentions VTT export accessed 2026-01-25 |
| SRT | Unknown | Yes | [Grain Transcription](https://grain.com/transcription) mentions SRT export accessed 2026-01-25 |
| PDF | N/A | Yes | [Grain Transcription](https://grain.com/transcription) accessed 2026-01-25 |
| DOCX | N/A | Yes | [Grain Transcription](https://grain.com/transcription) accessed 2026-01-25 |
| TXT | Unknown | Unknown | Not explicitly documented |

### Integrations

| Platform | Type | Evidence |
|----------|------|----------|
| Zoom | Video conferencing | [Grain Integrations](https://grain.com/integrations) accessed 2026-01-25 |
| Google Meet | Video conferencing | [Grain Integrations](https://grain.com/integrations) accessed 2026-01-25 |
| Microsoft Teams | Video conferencing | [Grain Integrations](https://grain.com/integrations) accessed 2026-01-25 |
| Webex | Video conferencing | [Grain Integrations](https://grain.com/integrations) accessed 2026-01-25 |
| HubSpot | CRM | [Grain Integrations](https://grain.com/integrations) accessed 2026-01-25 |
| Salesforce | CRM | [Grain Integrations](https://grain.com/integrations) accessed 2026-01-25 |
| Slack | Collaboration | [Grain Integrations](https://grain.com/integrations) accessed 2026-01-25 |
| Zapier | Automation | [Grain Integrations](https://grain.com/integrations) accessed 2026-01-25 |
| Aircall | Phone | [Grain Integrations](https://grain.com/integrations) accessed 2026-01-25 |
| Productboard | Product management | [Grain Integrations](https://grain.com/integrations) accessed 2026-01-25 |
| Gong | Revenue intelligence | [ProductiveWithChris](https://productivewithchris.com/tools/grain/) accessed 2026-01-25 |
| Notion | Documentation | [ProductiveWithChris](https://productivewithchris.com/tools/grain/) accessed 2026-01-25 |

---

## Pricing

| Plan | Monthly (Billed Annually) | Monthly (Billed Monthly) | Key Features | Evidence |
|------|---------------------------|--------------------------|--------------|----------|
| **Free** | $0 | $0 | 20 recordings, 45-min cap, 90-day storage | [Grain Pricing](https://grain.com/pricing) accessed 2026-01-25 |
| **Starter** | $15/user | $19/user | Unlimited recordings, transcript downloads, Collections | [Grain Pricing](https://grain.com/pricing) accessed 2026-01-25 |
| **Business** | $29/user | $39/user | Deal boards, conversation trackers, advanced analytics | [Claap Blog](https://www.claap.io/blog/grain-pricing) accessed 2026-01-25 |
| **Enterprise** | Custom | Custom | Minimum paid seats, unlimited basic seats, custom features | [Grain Pricing](https://grain.com/pricing) accessed 2026-01-25 |

### Notable Pricing Aspects
- Free plan allows only one workspace member to record
- Unlimited free/basic viewer seats after upgrading one member to Starter
- 25% savings on annual billing

---

## API Access

### API Endpoint
- **Base URL**: `https://api.grain.com/_/public-api/`
- **Authentication**: OAuth 2.0
- **Example**: `GET https://api.grain.com/_/public-api/me`

### Available API Operations

| Operation | Description | Evidence |
|-----------|-------------|----------|
| Get Recording | Fetch recording by ID with optional transcript | [Zapier MCP](https://zapier.com/mcp/grain) accessed 2026-01-25 |
| Get Transcript | Retrieve transcript in configurable format | [Zapier MCP](https://zapier.com/mcp/grain) accessed 2026-01-25 |
| Get Intelligence Notes | Retrieve AI notes (key points, summary) | [Zapier MCP](https://zapier.com/mcp/grain) accessed 2026-01-25 |
| API Request (Beta) | Raw HTTP requests with authentication | [Zapier MCP](https://zapier.com/mcp/grain) accessed 2026-01-25 |

### Webhook Events

| Event Type | Trigger | Evidence |
|------------|---------|----------|
| Recording Added | New recording created | [Pipedream](https://pipedream.com/apps/grain) accessed 2026-01-25 |
| Recording Updated | Recording modified | [Pipedream](https://pipedream.com/apps/grain) accessed 2026-01-25 |
| Recording Removed | Recording deleted | [Pipedream](https://pipedream.com/apps/grain) accessed 2026-01-25 |
| Highlight Added/Updated/Removed | Highlight changes | [Pipedream](https://pipedream.com/apps/grain) accessed 2026-01-25 |
| Story Added/Updated/Removed | Story changes | [Pipedream](https://pipedream.com/apps/grain) accessed 2026-01-25 |

### MCP (Model Context Protocol) Integration
- **Purpose**: Connect meeting data directly to AI tools (Claude, Cursor, ChatGPT)
- **Capabilities**: Meeting queries, analytics, reporting within AI chat interfaces
- **Setup**: One-click installation for Cursor IDE
- **Evidence**: [MCPCursor Grain MCP](https://mcpcursor.com/server/grain-mcp), [Zapier MCP](https://zapier.com/mcp/grain) accessed 2026-01-25

---

## Strengths

1. **Video-centric approach** - Creates shareable video highlights, not just text clips - [ProductiveWithChris](https://productivewithchris.com/tools/grain/) accessed 2026-01-25

2. **Generous free tier** - 20 recordings vs. competitors' 5-10 - [Claap Blog](https://www.claap.io/blog/grain-pricing) accessed 2026-01-25

3. **Unlimited recordings on paid plans** - No per-minute or storage limits - [Claap Blog](https://www.claap.io/blog/grain-pricing) accessed 2026-01-25

4. **Strong CRM integration** - Native HubSpot/Salesforce sync with field enrichment - [Grain Integrations](https://grain.com/integrations) accessed 2026-01-25

5. **MCP server support** - Native integration with Claude, Cursor, and modern AI tools - [MCPCursor](https://mcpcursor.com/server/grain-mcp) accessed 2026-01-25

6. **Robust search and filtering** - Filter by owner, participants, company, date ranges - [Votars Review](https://votars.ai/en/blog/grain-review-2025-updated/) accessed 2026-01-25

7. **Editable transcripts** - Users can correct and refine transcriptions - [Grain Transcription](https://grain.com/transcription) accessed 2026-01-25

8. **Multi-language support** - 100+ languages for transcription - [Grain Transcription](https://grain.com/transcription) accessed 2026-01-25

9. **Export flexibility** - VTT, SRT, PDF, DOCX formats - [Grain Transcription](https://grain.com/transcription) accessed 2026-01-25

---

## Weaknesses

1. **Visible recording bot** - Cannot record discreetly; bot joins as visible participant - [Claap Blog](https://www.claap.io/blog/grain-pricing), [Bluedot Alternatives](https://www.bluedothq.com/blog/grain-alternatives) accessed 2026-01-25

2. **No mobile app** - Cannot record in-person meetings - [Votars Review](https://votars.ai/en/blog/grain-review-2025-updated/) accessed 2026-01-25

3. **Limited cross-meeting analysis** - AI analyzes individual meetings in isolation - [Votars Review](https://votars.ai/en/blog/grain-review-2025-updated/) accessed 2026-01-25

4. **Real-time English only** - Live transcription limited to English; other languages post-meeting only - [Votars Review](https://votars.ai/en/blog/grain-review-2025-updated/) accessed 2026-01-25

5. **Limited advanced analytics** - Lacks sophisticated revenue forecasting compared to Gong/Avoma - [Claap Blog](https://www.claap.io/blog/grain-pricing) accessed 2026-01-25

6. **Video-heavy focus** - May be overkill for users who just need text transcripts - [ProductiveWithChris](https://productivewithchris.com/tools/grain/) accessed 2026-01-25

7. **Fewer integrations than competitors** - 10 native integrations vs. competitors with 20+ - [Grain Integrations](https://grain.com/integrations) accessed 2026-01-25

8. **Pricing scales per user** - Can become expensive for large teams - [Claap Blog](https://www.claap.io/blog/grain-pricing) accessed 2026-01-25

9. **No Webex real-time support** - Webex integration added recently but may have limitations - [Bluedot Alternatives](https://www.bluedothq.com/blog/grain-alternatives) accessed 2026-01-25

---

## Competitive Positioning

### Best For
- Sales teams needing CRM integration
- Teams that share video clips internally
- Organizations with high meeting volume (20-50/week)
- Teams using modern AI tools (Claude, Cursor)

### Not Ideal For
- Users needing discreet recording
- Teams with low meeting volume (<5/week)
- Organizations requiring advanced revenue intelligence
- Users who only need text transcripts without video

### Key Competitors
| Competitor | Differentiator |
|------------|----------------|
| Otter.ai | More languages, mobile app |
| Fireflies.ai | Better analytics, sentiment analysis |
| Fathom | Free tier, simpler interface |
| Gong | Enterprise revenue intelligence |
| Avoma | Advanced coaching and forecasting |

---

## Differentiation Opportunities for Our Skill

Based on this analysis, our transcript processing skill can differentiate by:

1. **Text-Native Processing:** Focus on VTT/SRT input without requiring video, serving users who already have transcripts from other sources.

2. **Structured Entity Extraction:** Extract action items, questions, decisions as first-class entities with consistent schema, not embedded in prose summaries.

3. **Export-First Design:** Prioritize machine-readable output (YAML, JSON) over visual presentation, enabling downstream automation.

4. **Format Flexibility:** Accept multiple input formats (VTT, SRT, plain text) without video dependency.

5. **Open Processing:** Provide entity extraction without requiring meeting recording integration, serving the "bring your own transcript" use case.

6. **Lightweight Architecture:** Avoid video processing overhead for users who only need text analysis.

---

## References

1. [Grain Homepage](https://grain.com/) - Accessed 2026-01-25
2. [Grain Pricing](https://grain.com/pricing) - Accessed 2026-01-25
3. [Grain Integrations](https://grain.com/integrations) - Accessed 2026-01-25
4. [Grain Transcription](https://grain.com/transcription) - Accessed 2026-01-25
5. [Grain MCP Server - MCPCursor](https://mcpcursor.com/server/grain-mcp) - Accessed 2026-01-25
6. [Grain MCP - Zapier](https://zapier.com/mcp/grain) - Accessed 2026-01-25
7. [Grain API - Pipedream](https://pipedream.com/apps/grain) - Accessed 2026-01-25
8. [Grain Pricing Analysis - Claap Blog](https://www.claap.io/blog/grain-pricing) - Accessed 2026-01-25
9. [Grain Review 2025 - Votars](https://votars.ai/en/blog/grain-review-2025-updated/) - Accessed 2026-01-25
10. [Grain Review - ProductiveWithChris](https://productivewithchris.com/tools/grain/) - Accessed 2026-01-25
11. [Grain Alternatives - Bluedot](https://www.bluedothq.com/blog/grain-alternatives) - Accessed 2026-01-25
12. [Grain Pros & Cons - TrustRadius](https://www.trustradius.com/products/grain/reviews) - Accessed 2026-01-25
13. [Grain Reviews - G2](https://www.g2.com/products/grain/reviews) - Accessed 2026-01-25 (403 error on direct fetch)
14. [Grain on Product Hunt](https://www.producthunt.com/products/grain) - Accessed 2026-01-25
15. [Model Context Protocol - Anthropic](https://www.anthropic.com/news/model-context-protocol) - Accessed 2026-01-25

---

## Research Methodology Notes

### Sources Used
- **Primary**: grain.com official website and subpages
- **Secondary**: Third-party review sites (G2, TrustRadius, ProductiveWithChris, Votars)
- **Technical**: API documentation via Pipedream, Zapier MCP, MCPCursor

### Limitations
- G2 reviews page returned 403 error during WebFetch
- Specific API documentation not publicly available on grain.com
- Some features (like transcript import capabilities) not explicitly documented
- Language support claims inconsistent (100+ vs. 9 languages in different sources)

### Research Tools
- WebSearch for discovery
- WebFetch for page content extraction
- All citations include access date per requirements

---

## Document Metadata

| Field | Value |
|-------|-------|
| Document ID | GRAIN-analysis |
| Version | 2.0.0 |
| Created | 2026-01-25 |
| Updated | 2026-01-25 |
| Author | ps-researcher agent |
| Status | COMPLETE (live web research) |
| Previous Version | 1.0.0 (knowledge-base only) |
