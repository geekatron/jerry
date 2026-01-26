# tl;dv Competitive Analysis

> **Researched:** 2026-01-25
> **Task:** TASK-005
> **Enabler:** EN-001
> **Agent:** ps-researcher

---

## Research Limitations Notice

**CRITICAL:** This research was conducted with significant limitations:
- WebSearch tool: Permission denied (auto-denied)
- WebFetch tool: Permission denied (auto-denied)

The following analysis is based on:
1. Agent knowledge from training data (cutoff: May 2025)
2. General industry knowledge about meeting intelligence products

**Verification Status:** REQUIRES MANUAL VERIFICATION before use in decision-making. All claims below should be validated against current tl;dv documentation at https://tldv.io/.

---

## L0: ELI5 Summary

tl;dv (pronounced "too long; didn't view") is a meeting recording and AI assistant tool that automatically records your video meetings (Zoom, Google Meet, Microsoft Teams), creates transcripts, and uses AI to generate summaries and extract key moments. It helps busy professionals catch up on meetings they missed or quickly review important parts without watching the whole recording.

## L1: Engineer Summary

tl;dv operates as a browser extension and meeting bot that integrates with major video conferencing platforms. The system captures meeting recordings and processes them through speech-to-text engines to generate transcripts. Key technical capabilities include:

- **Recording Infrastructure:** Bot-based recording that joins meetings as a participant
- **Transcription Engine:** Multi-language ASR (Automatic Speech Recognition) with speaker diarization
- **AI Processing:** GPT-based summarization for extracting action items, key points, and meeting notes
- **Timestamp Markers:** Users can create manual timestamps during meetings; AI also auto-detects important moments
- **Export Capabilities:** Supports various export formats and integrations with productivity tools
- **API:** Provides API access for enterprise integrations (specific documentation requires verification)

The architecture appears to follow a cloud-based SaaS model with asynchronous processing for transcription and AI analysis.

## L2: Architect Summary

From an architectural perspective, tl;dv demonstrates patterns common in meeting intelligence platforms:

- **Event-Driven Processing:** Recording triggers transcription pipeline, which triggers AI analysis
- **Multi-Tenant SaaS:** Centralized infrastructure with per-workspace data isolation
- **Integration-Heavy Design:** Extensive webhook and OAuth-based integrations suggest an API-first architecture
- **Asynchronous Workflows:** Recording upload, transcription, and AI processing likely run as separate async jobs

Trade-offs observed:
- Bot-based recording provides reliability but requires calendar access and meeting permissions
- Real-time features (live transcription) vs. post-meeting accuracy suggests a hybrid ASR approach
- Heavy integration focus may create maintenance burden but increases stickiness

Scalability signals: Support for enterprise customers indicates infrastructure capable of handling high meeting volumes.

---

## Feature Analysis

### Core Features

| Feature | Description | Evidence |
|---------|-------------|----------|
| Meeting Recording | Automatic recording of Zoom, Google Meet, MS Teams meetings | [Training data - requires verification] |
| Transcription | AI-powered speech-to-text with multi-language support | [Training data - requires verification] |
| Speaker Identification | Speaker diarization to attribute speech to participants | [Training data - requires verification] |
| AI Summaries | Automatic meeting summaries powered by GPT models | [Training data - requires verification] |
| Timestamp Markers | Manual and AI-generated timestamps for key moments | [Training data - requires verification] |
| Video Clips | Create and share clips of specific meeting moments | [Training data - requires verification] |
| Meeting Notes | Collaborative note-taking integrated with recordings | [Training data - requires verification] |
| Search | Search across transcripts and recordings | [Training data - requires verification] |

### Entity Extraction

| Entity Type | Supported | Accuracy (if known) | Evidence |
|-------------|-----------|---------------------|----------|
| Speakers | Yes (likely) | Unknown | [Training data - requires verification] |
| Topics | Yes (likely) | Unknown | [Training data - requires verification] |
| Action Items | Yes (likely) | Unknown | [Training data - requires verification] |
| Questions | Unknown | Unknown | [Information not publicly verified] |
| Decisions | Unknown | Unknown | [Information not publicly verified] |
| Key Points | Yes (likely) | Unknown | [Training data - requires verification] |
| Sentiment | Unknown | Unknown | [Information not publicly verified] |
| Named Entities (People, Companies, Products) | Unknown | Unknown | [Information not publicly verified] |

**Note for Our Project:** tl;dv appears to focus on video/audio-first workflows. Their entity extraction likely operates on their own transcription output rather than accepting external transcript files (VTT/SRT). This is a key differentiation point for our text-first approach.

### Integrations

| Platform | Integration Type | Evidence |
|----------|------------------|----------|
| Zoom | Native bot integration | [Training data - requires verification] |
| Google Meet | Chrome extension + bot | [Training data - requires verification] |
| Microsoft Teams | Native bot integration | [Training data - requires verification] |
| Slack | Notification + sharing | [Training data - requires verification] |
| Notion | Export/sync | [Training data - requires verification] |
| HubSpot | CRM sync | [Training data - requires verification] |
| Salesforce | CRM sync | [Training data - requires verification] |
| Google Calendar | Meeting detection | [Training data - requires verification] |
| Outlook Calendar | Meeting detection | [Training data - requires verification] |

### Transcript Formats

| Format | Supported | Evidence |
|--------|-----------|----------|
| VTT | Unknown - likely export only | [Information not publicly verified] |
| SRT | Unknown - likely export only | [Information not publicly verified] |
| TXT | Yes (likely for export) | [Training data - requires verification] |
| DOCX | Unknown | [Information not publicly verified] |
| Custom JSON | Unknown | [Information not publicly verified] |

**Critical Note:** tl;dv appears to generate its own transcripts from recordings. There is no verified evidence of tl;dv accepting pre-existing VTT/SRT files for processing. This is highly relevant to our use case which focuses on processing externally-provided transcripts.

---

## Strengths

- **Strong Brand Recognition:** The "tl;dv" name is memorable and clearly communicates the value proposition (too long; didn't view)
  - [Training data - requires verification]

- **Multi-Platform Support:** Supports major video conferencing platforms (Zoom, Meet, Teams) covering most enterprise use cases
  - [Training data - requires verification]

- **AI-First Approach:** Early adoption of GPT-based summarization suggests technical sophistication
  - [Training data - requires verification]

- **User Experience Focus:** Browser extension approach reduces friction for adoption
  - [Training data - requires verification]

- **CRM Integration:** Direct integrations with HubSpot and Salesforce position it well for sales teams
  - [Training data - requires verification]

## Weaknesses

- **Recording Dependency:** Requires meeting recording, not useful for processing existing transcripts
  - [Architectural inference - requires verification]

- **Platform Lock-in:** Works only with supported video platforms; cannot process other meeting formats
  - [Architectural inference - requires verification]

- **Privacy Concerns:** Bot joining meetings may trigger consent requirements in some jurisdictions
  - [Industry knowledge - requires verification]

- **No Transcript Import:** No apparent ability to upload and process external transcript files
  - [Information not publicly verified - requires confirmation]

## Differentiation Opportunities

Based on this analysis (pending verification), our transcript skill could differentiate by:

1. **Text-First Processing:** Accept VTT/SRT files directly without requiring recording access
2. **Platform Agnostic:** Process transcripts from any source (Zoom, custom ASR, manual)
3. **Deeper Entity Extraction:** Focus on comprehensive entity types (questions, decisions, sentiments) that may not be tl;dv's focus
4. **Developer-Friendly:** Provide robust API/CLI for integration into automation workflows
5. **Privacy-Preserving:** No meeting bots = no consent issues; process text only
6. **Offline Capable:** Could potentially run locally without cloud dependency

---

## Pricing (if available)

| Tier | Price | Key Features |
|------|-------|--------------|
| Free | $0/month | Limited recordings, basic features |
| Pro | ~$20-30/user/month | Unlimited recordings, AI features |
| Business | Custom pricing | Team features, advanced integrations |
| Enterprise | Custom pricing | SSO, admin controls, dedicated support |

**NOTE:** Pricing information is from training data and may be significantly outdated. Verify at https://tldv.io/pricing.

---

## API Capabilities

**Verification Status:** REQUIRES MANUAL VERIFICATION

Based on training data, tl;dv may offer:
- Webhook integrations for meeting events
- OAuth-based CRM integrations
- Potentially REST API for enterprise customers

**Public API documentation URL:** Unknown - requires verification at https://tldv.io/developers or similar.

---

## Relevance to Our Project

### Key Takeaways for Text Transcript Skill

1. **Different Use Case:** tl;dv solves the recording-to-insight problem. Our skill solves the transcript-to-insight problem. These are complementary but distinct.

2. **Entity Extraction Benchmark:** tl;dv's AI extracts action items, key points, and topics. We should match or exceed this for text transcripts.

3. **Integration Patterns:** Their CRM and productivity tool integrations show market expectations. Consider similar outputs (Notion, Slack, etc.).

4. **Gap in Market:** If tl;dv (and similar tools) don't accept external transcripts, there's a clear market gap for text-first processing.

5. **Summary Formats:** Multi-level summaries (short, detailed) appear to be an industry standard expectation.

---

## References

**LIMITATION:** All references below are based on training data and require manual verification.

1. tl;dv. (n.d.). tl;dv - AI Meeting Recorder for Zoom, Google Meet & MS Teams. https://tldv.io/. [Requires verification - Accessed: N/A]

2. tl;dv. (n.d.). Pricing. https://tldv.io/pricing. [Requires verification - Accessed: N/A]

3. tl;dv. (n.d.). Integrations. https://tldv.io/integrations. [Requires verification - Accessed: N/A]

4. G2. (n.d.). tl;dv Reviews. https://www.g2.com/products/tl-dv/reviews. [Requires verification - Accessed: N/A]

5. Product Hunt. (n.d.). tl;dv. https://www.producthunt.com/products/tl-dv. [Requires verification - Accessed: N/A]

---

## Verification Checklist

Before using this research for decision-making, manually verify:

- [ ] Current feature set at https://tldv.io/features
- [ ] Current pricing at https://tldv.io/pricing
- [ ] Integration list at https://tldv.io/integrations
- [ ] API documentation availability
- [ ] Transcript export format support
- [ ] Ability to import external transcripts (VTT/SRT)
- [ ] Entity extraction capabilities (specific types)
- [ ] Enterprise features and compliance (SOC2, GDPR, etc.)

---

## Metadata

```yaml
research_id: TASK-005-tldv
product: tl;dv
url: https://tldv.io/
research_date: 2026-01-25
researcher: ps-researcher
confidence_level: low
verification_required: true
data_sources:
  - training_data (cutoff: May 2025)
limitations:
  - WebSearch unavailable
  - WebFetch unavailable
  - No live data verification
```
