# Task: TASK-143 - Create meeting-006-all-hands.vtt

> **Task ID:** TASK-143
> **Status:** done
> **Priority:** high
> **Enabler:** [EN-017-large-transcript-dataset](./EN-017-large-transcript-dataset.md)
> **Created:** 2026-01-28
> **Last Updated:** 2026-01-28
> **Completed:** 2026-01-28

---

## Summary

Create a ~3-hour quarterly all-hands transcript with approximately 90K tokens. This transcript tests multiple-split behavior (triggers 2-3 splits).

---

## Acceptance Criteria

- [ ] **AC-1:** Duration approximately 180 minutes (3 hours)
- [ ] **AC-2:** Token count between 85K-95K tokens
- [ ] **AC-3:** Valid W3C WebVTT format
- [ ] **AC-4:** Contains 9+ speakers (C-suite, VPs, audience Q&A)
- [ ] **AC-5:** Contains 6-8 distinct topics
- [ ] **AC-6:** Contains 15-20 action items
- [ ] **AC-7:** Contains 5-8 decisions
- [ ] **AC-8:** Contains 12-18 questions
- [ ] **AC-9:** File saved to `skills/transcript/test_data/transcripts/golden/meeting-006-all-hands.vtt`
- [ ] **AC-10:** Expected to trigger 2-3 file splits
- [ ] **AC-11:** Timestamps strictly sequential from 00:00:00 to end (per TASK-145)
- [ ] **AC-12:** No timestamp seconds ≥ 60 (valid VTT format)
- [ ] **AC-13:** Generate content end-to-end, never insert mid-file

---

## Technical Specifications

### Token Target
- **Target:** ~90,000 tokens
- **Range:** 85,000 - 95,000 tokens
- **Words needed:** ~30,000 words
- **Expected splits:** 2-3 (at semantic ## boundaries)

### Speaker Roster

| Speaker | Role | Contribution % |
|---------|------|----------------|
| Jennifer | CEO (Host) | 20% |
| David | CTO | 15% |
| Marcus | VP Engineering | 15% |
| Rachel | VP Product | 12% |
| Lisa | VP Sales | 8% |
| Kevin | VP Marketing | 8% |
| Employee1-5 | Audience Q&A | 22% combined |

### Agenda Structure

1. **Welcome & Company Update (30 min)** - CEO overview
2. **Engineering Update (25 min)** - CTO presentation
3. **Product Roadmap (25 min)** - VP Product presentation
4. **Sales & Revenue (20 min)** - VP Sales update
5. **Marketing & Brand (20 min)** - VP Marketing update
6. **Team Recognition (15 min)** - Awards and shoutouts
7. **Q&A Session (30 min)** - Open floor questions
8. **Closing & Next Steps (15 min)** - CEO wrap-up

### Expected Entities

| Entity Type | Expected Count |
|-------------|----------------|
| Speakers | 9+ |
| Topics | 6-8 |
| Action Items | 15-20 |
| Decisions | 5-8 |
| Questions | 12-18 |

---

## Unit of Work

### Step 1: Create VTT Header
```
WEBVTT

NOTE Duration: ~180 minutes
NOTE Token Target: ~90,000
NOTE Topic: Quarterly All-Hands Meeting
NOTE Expected Splits: 2-3
```

### Step 2: Write Welcome Section (~5,000 words)
- Company vision and mission
- Q4 achievements
- Financial overview

### Step 3: Write Engineering Section (~5,000 words)
- Technical accomplishments
- Infrastructure updates
- Security and reliability

### Step 4: Write Product Section (~4,500 words)
- Feature releases
- Customer success stories
- Q1 roadmap preview

### Step 5: Write Sales Section (~3,500 words)
- Revenue performance
- Key wins
- Pipeline outlook

### Step 6: Write Marketing Section (~3,500 words)
- Brand initiatives
- Campaign results
- Market positioning

### Step 7: Write Recognition Section (~2,500 words)
- Team awards
- Individual recognition
- Milestone celebrations

### Step 8: Write Q&A Section (~4,500 words)
- Employee questions
- Leadership responses
- Follow-up commitments

### Step 9: Write Closing Section (~1,500 words)
- Summary of key points
- Action items
- Next all-hands date

### Step 10: Validate Format & Multi-Split Behavior
- Run through ts-parser
- Verify token count ~90K
- Verify 2-3 splits expected

---

## Dependencies

### Depends On
- TASK-140 (Dataset Design)
- TASK-145 (Timestamp Ordering Fix) - Establishes correct pattern

### Blocks
- TASK-144 (Dataset Validation)

---

## Verification Evidence

| Criterion | Evidence Required |
|-----------|-------------------|
| AC-1-2 | TokenCounter output showing ~90K tokens |
| AC-3 | ts-parser validation passes |
| AC-4-8 | ts-extractor entity counts |
| AC-9 | File exists at specified path |
| AC-10 | TokenCounter indicates 2-3 splits required |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Initial task created |
