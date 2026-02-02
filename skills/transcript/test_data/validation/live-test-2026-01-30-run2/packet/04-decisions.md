# Decisions

> **Total Decisions:** 12
> **Average Confidence:** 0.91

---

## Summary by Decision Maker

| Decision Maker | Count | Decisions |
|----------------|-------|-----------|
| [speaker:robert-chen] | 3 | dec-001, dec-002, dec-007 |
| [speaker:james-wilson] | 4 | dec-005, dec-006, dec-008, dec-012 |
| [speaker:jennifer-adams] | 2 | dec-003, dec-011 |
| [speaker:diana-martinez] | 2 | dec-004, dec-010 |
| [speaker:sarah-mitchell] | 1 | dec-009 |

---

## Summary by Category

| Category | Count | Decision IDs |
|----------|-------|-------------|
| People & Culture | 4 | dec-001, dec-002, dec-007, dec-009 |
| Engineering Organization | 4 | dec-005, dec-006, dec-008, dec-012 |
| Product Strategy | 2 | dec-003, dec-011 |
| Security & Infrastructure | 2 | dec-004, dec-010 |

---

## People & Culture Decisions

### [decision:dec-001] Hybrid Work Operating Model
- **Decided By:** [speaker:robert-chen]
- **Confidence:** 0.95
- **Topic:** [topic:top-007] Employee Q&A: Work-Life Balance

**Decision:**
Adopted hybrid work as the operating model going forward with 2-3 days in office per week

**Rationale:**
The office is for connection and collaboration, not just sitting at a desk. Some roles are fully remote based on function and location.

**Citation:**
> "We've embraced hybrid work as our operating model going forward."
> - Segment: seg-1527 | Timestamp: 2:25:06 | [Chunk 4](#seg-1527)

**Related:**
- [question:que-002] Remote work approach
- [action:act-007] Gather hybrid work feedback

---

### [decision:dec-002] No-Meeting Fridays
- **Decided By:** [speaker:robert-chen]
- **Confidence:** 0.94
- **Topic:** [topic:top-007] Employee Q&A: Work-Life Balance

**Decision:**
Implemented no-meeting Fridays to provide focused time for employees

**Rationale:**
Address work-life balance concerns and prevent burnout

**Citation:**
> "We've implemented no-meeting Fridays to provide focused time."
> - Segment: seg-1519 | Timestamp: 2:24:18 | [Chunk 4](#seg-1519)

**Related:**
- [question:que-001] Burnout concerns
- [decision:dec-007] Unlimited PTO policy

---

### [decision:dec-007] Unlimited PTO Policy
- **Decided By:** [speaker:robert-chen]
- **Confidence:** 0.90
- **Topic:** [topic:top-007] Employee Q&A: Work-Life Balance

**Decision:**
Use unlimited PTO policy with active encouragement to take time off

**Rationale:**
Address burnout risk in fast-growing company; track and follow up with those not using it

**Citation:**
> "Our unlimited PTO policy is real - we actually encourage people to take time off."
> - Segment: seg-1521 | Timestamp: 2:24:30 | [Chunk 4](#seg-1521)

**Related:**
- [action:act-006] Track vacation usage
- [decision:dec-002] No-meeting Fridays

---

### [decision:dec-009] Internal Mobility Encouraged
- **Decided By:** [speaker:sarah-mitchell]
- **Confidence:** 0.89
- **Topic:** [topic:top-008] HR and People Operations Updates

**Decision:**
Internal mobility strongly encouraged with 30%+ of open roles filled internally

**Rationale:**
Career development is a priority; managers support career moves even outside their team

**Citation:**
> "Internal mobility is strongly encouraged here."
> - Segment: seg-2023 | Timestamp: 3:15:36 | [Chunk 5](#seg-2023)

**Related:**
- [question:que-006] Role rotation opportunities
- [action:act-011] Internal job posting visibility

---

## Engineering Organization Decisions

### [decision:dec-005] Squad-Based Engineering Model
- **Decided By:** [speaker:james-wilson]
- **Confidence:** 0.92
- **Topic:** [topic:top-002] Engineering Organization and Squad Model

**Decision:**
Reorganized engineering into a squad-based model with autonomous cross-functional teams

**Rationale:**
Autonomy enables faster decision-making and innovation; guilds prevent divergence

**Citation:**
> "However, autonomy requires coordination mechanisms to prevent divergence."
> - Segment: seg-501 | Timestamp: 0:45:50 | [Chunk 2](#seg-501)

**Related:**
- [decision:dec-006] Guild creation
- [decision:dec-012] Separation of product and people management

---

### [decision:dec-006] Engineering Guilds
- **Decided By:** [speaker:james-wilson]
- **Confidence:** 0.91
- **Topic:** [topic:top-002] Engineering Organization and Squad Model

**Decision:**
Created guilds (backend, frontend, data) for coordination across squads

**Rationale:**
Maintain coding standards and review architecture while allowing squad autonomy

**Citation:**
> "The backend guild, frontend guild, and data guild meet regularly to share practices."
> - Segment: seg-503 | Timestamp: 0:46:01 | [Chunk 2](#seg-503)

**Related:**
- [decision:dec-005] Squad-based model
- [decision:dec-012] Product and people separation

---

### [decision:dec-008] Elasticsearch Search Infrastructure
- **Decided By:** [speaker:james-wilson]
- **Confidence:** 0.93
- **Topic:** [topic:top-002] Engineering Organization and Squad Model

**Decision:**
Rebuilt search infrastructure using Elasticsearch improving latency from 800ms to under 100ms

**Rationale:**
Performance improvement needed; relevance scores also improved by 45%

**Citation:**
> "The Search squad completely rebuilt our search infrastructure using Elasticsearch."
> - Segment: seg-509 | Timestamp: 0:46:34 | [Chunk 2](#seg-509)

**Impact:**
- Latency: 800ms -> <100ms (8x improvement)
- Relevance: +45% improvement

---

### [decision:dec-012] Separation of Product and People Management
- **Decided By:** [speaker:james-wilson]
- **Confidence:** 0.88
- **Topic:** [topic:top-002] Engineering Organization and Squad Model

**Decision:**
Separation of product work and people management in engineering organization

**Rationale:**
This structure has worked well - chapters handle career development, squads handle product

**Citation:**
> "This separation of product work and people management has worked well for us."
> - Segment: seg-507 | Timestamp: 0:46:23 | [Chunk 2](#seg-507)

**Related:**
- [decision:dec-005] Squad-based model
- [decision:dec-006] Guilds for coordination

---

## Product Strategy Decisions

### [decision:dec-003] Better Defaults Over Customization
- **Decided By:** [speaker:jennifer-adams]
- **Confidence:** 0.93
- **Topic:** [topic:top-003] Product Research and Data-Driven Development

**Decision:**
Pivoted from building more customization to building better defaults based on user role

**Rationale:**
Research revealed users wanted fewer options with smarter defaults, not more customization

**Citation:**
> "We pivoted from building more customization to building better defaults."
> - Segment: seg-536 | Timestamp: 0:49:02 | [Chunk 2](#seg-536)

**Related:**
- [action:act-004] Mobile app redesign
- [decision:dec-011] Data-driven development

---

### [decision:dec-011] Data-Driven Development with A/B Testing
- **Decided By:** [speaker:jennifer-adams]
- **Confidence:** 0.91
- **Topic:** [topic:top-003] Product Research and Data-Driven Development

**Decision:**
Adopted data-driven product development with A/B testing before full rollout

**Rationale:**
Reduces risk and increases confidence in decisions; ran 23 experiments last quarter

**Citation:**
> "We use A/B testing extensively to validate hypotheses before full rollout."
> - Segment: seg-529 | Timestamp: 0:48:24 | [Chunk 2](#seg-529)

**Impact:**
- 23 A/B experiments last quarter
- Reduced risk in product decisions

**Related:**
- [decision:dec-003] Better defaults pivot

---

## Security & Infrastructure Decisions

### [decision:dec-004] Zero-Trust Networking
- **Decided By:** [speaker:diana-martinez]
- **Confidence:** 0.94
- **Topic:** [topic:top-004] Infrastructure and Cloud Migration

**Decision:**
Implemented zero-trust networking across all production environments

**Rationale:**
Security remains a top priority in all architectural decisions

**Citation:**
> "We've implemented zero-trust networking across all production environments."
> - Segment: seg-1015 | Timestamp: 1:33:46 | [Chunk 3](#seg-1015)

**Related:**
- [action:act-002] ISO 27001 certification
- [action:act-013] Post-quantum cryptography

---

### [decision:dec-010] Strategic Patent Filing
- **Decided By:** [speaker:diana-martinez]
- **Confidence:** 0.87
- **Topic:** [topic:top-009] Innovation and R&D Strategy

**Decision:**
File patents strategically rather than just counting them

**Rationale:**
Focus on protecting innovations that matter, not vanity metrics

**Citation:**
> "We file patents strategically, not just to count them."
> - Segment: seg-2512 | Timestamp: 4:06:12 | [Chunk 6](#seg-2512)

---

## Decisions by Topic

| Topic | Decisions |
|-------|-----------|
| [topic:top-002] Engineering | [decision:dec-005], [decision:dec-006], [decision:dec-008], [decision:dec-012] |
| [topic:top-003] Product Research | [decision:dec-003], [decision:dec-011] |
| [topic:top-004] Infrastructure | [decision:dec-004] |
| [topic:top-007] Work-Life Balance | [decision:dec-001], [decision:dec-002], [decision:dec-007] |
| [topic:top-008] HR Updates | [decision:dec-009] |
| [topic:top-009] R&D Strategy | [decision:dec-010] |

---

## Related Links

- [00-index.md](00-index.md) - Navigation hub
- [02-speakers.md](02-speakers.md) - Speaker details
- [03-action-items.md](03-action-items.md) - Related actions

---

*Generated by ts-formatter agent*
