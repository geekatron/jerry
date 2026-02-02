---
schema_version: "1.0"
generator: "ts-formatter"
generated_at: "2026-01-28T00:00:00Z"
---

# Questions

> **Extracted from:** [transcript-meeting-001](./00-index.md)
> **Total:** 2
> **Open Questions:** 0 (all resolved in meeting)

## Questions

### {#que-001} How do we want to handle the feature flag for the new authentication?

- **Asked By:** [Alice](./03-speakers.md#spk-alice)
- **Status:** Resolved
- **Resolution:** Phased rollout approach ([#dec-002](./05-decisions.md#dec-002))
- **Confidence:** 0.90
- **Source:** [seg-021](./02-transcript.md#seg-021) - "How do we want to handle the feature flag..."

**Context:**
Question raised to discuss deployment strategy for new authentication. Led to decision on phased rollout.

<backlinks>
Referenced from:
- [02-transcript.md#seg-021](./02-transcript.md#seg-021) - Alice: "How do we want to handle..."
- [01-summary.md](./01-summary.md) - Open Questions
</backlinks>

---

### {#que-002} What about the legacy login endpoint? Are we deprecating it immediately?

- **Asked By:** [Charlie](./03-speakers.md#spk-charlie)
- **Status:** Resolved
- **Resolution:** Keep running for 2 weeks with deprecation warnings ([#dec-003](./05-decisions.md#dec-003))
- **Confidence:** 0.88
- **Source:** [seg-025](./02-transcript.md#seg-025) - "What about the legacy login endpoint?"

**Context:**
Important question about backward compatibility. Led to decision to maintain parallel operation.

<backlinks>
Referenced from:
- [02-transcript.md#seg-025](./02-transcript.md#seg-025) - Charlie: "What about the legacy login..."
- [01-summary.md](./01-summary.md) - Open Questions
</backlinks>
