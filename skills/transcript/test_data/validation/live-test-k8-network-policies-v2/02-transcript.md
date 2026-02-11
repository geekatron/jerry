---
schema_version: "1.0"
generator: "ts-formatter"
generated_at: "2026-01-29T21:00:00Z"
packet_id: "k8-network-policies-v2"
---

# Full Transcript

## Recording Setup Confirmation
*Duration: 00:00:03 - 00:00:06 (3 seconds)*

<a id="seg-001"></a>
**[00:00:03]** [Alex Johnson](03-speakers.md#spk-001): It's it has started, right? [🔗 question-001](06-questions.md#que-001)

---

## Kubernetes Network Policy Implementation Recommendations
*Duration: 00:00:05 - 00:00:41 (36 seconds)*

<a id="seg-002"></a>
**[00:00:05]** [Sam Chen](03-speakers.md#spk-002): All right. Yeah. So I guess I was a little interested in

<a id="seg-003"></a>
**[00:00:10]** [Sam Chen](03-speakers.md#spk-002): where it's kind of recommended solutions and products rather than generic like,

<a id="seg-004"></a>
**[00:00:16]** [Sam Chen](03-speakers.md#spk-002): well, sorry, whether recommended specific

<a id="seg-005"></a>
**[00:00:20]** [Sam Chen](03-speakers.md#spk-002): implementations rather than just like concepts. [🔗 question-002](06-questions.md#que-002)

<a id="seg-006"></a>
**[00:00:24]** [Sam Chen](03-speakers.md#spk-002): So for example I saw like Cuverno in there and Cillium and things like that.

<a id="seg-007"></a>
**[00:00:25]** [Alex Johnson](03-speakers.md#spk-001): OK.

<a id="seg-008"></a>
**[00:00:31]** [Sam Chen](03-speakers.md#spk-002): I was wondering like are they have we have we recommended those if we if we [🔗 question-003](06-questions.md#que-003)

<a id="seg-009"></a>
**[00:00:38]** [Sam Chen](03-speakers.md#spk-002): like or is that just like a yeah.

---

## Decision Tree and Analysis Artifacts
*Duration: 00:00:39 - 00:00:58 (19 seconds)*

<a id="seg-010"></a>
**[00:00:39]** [Alex Johnson](03-speakers.md#spk-001): No, we no, we didn't. So there's a decision tree in there that [🔗 decision-001](05-decisions.md#dec-001)

<a id="seg-011"></a>
**[00:00:42]** [Alex Johnson](03-speakers.md#spk-001): I can walk you guys through. That's part of the like million artifacts. [🔗 action-001](04-action-items.md#act-001)

<a id="seg-012"></a>
**[00:00:46]** [Alex Johnson](03-speakers.md#spk-001): So it actually did an analysis as part of it. It went out,

<a id="seg-013"></a>
**[00:00:50]** [Alex Johnson](03-speakers.md#spk-001): it looked at multiple Kubernetes network interface drivers. It did the evaluation.

<a id="seg-014"></a>
**[00:00:55]** [Alex Johnson](03-speakers.md#spk-001): There's a matrix in here somewhere where it's like oh.

<a id="seg-015"></a>
**[00:00:56]** [Sam Chen](03-speakers.md#spk-002): OK.

---

## Microsoft's Official Kubernetes Network Recommendation
*Duration: 00:00:58 - 00:01:12 (14 seconds)*

<a id="seg-016"></a>
**[00:00:58]** [Alex Johnson](03-speakers.md#spk-001): This is Microsoft's official one. This new one I recommend is because it's

<a id="seg-017"></a>
**[00:01:02]** [Alex Johnson](03-speakers.md#spk-001): the one that's deprecating the official recommended Microsoft.

<a id="seg-018"></a>
**[00:01:05]** [Alex Johnson](03-speakers.md#spk-001): There are other ones and that was its decision tree and as part of the

<a id="seg-019"></a>
**[00:01:08]** [Alex Johnson](03-speakers.md#spk-001): orchestration run. So if I you know what, let me share my screen so I'm not talking

<a id="seg-020"></a>
**[00:01:12]** [Alex Johnson](03-speakers.md#spk-001): to the ether.

---

## Backlinks

### Speakers
- [Alex Johnson (spk-001)](03-speakers.md#spk-001) - 12 segments
- [Sam Chen (spk-002)](03-speakers.md#spk-002) - 8 segments

### Action Items
- [action-001](04-action-items.md#act-001) - Walk through decision tree (seg-011)

### Decisions
- [decision-001](05-decisions.md#dec-001) - No specific recommendations (seg-010)

### Questions
- [question-001](06-questions.md#que-001) - Recording started? (seg-001)
- [question-002](06-questions.md#que-002) - Specific implementations vs concepts (seg-005)
- [question-003](06-questions.md#que-003) - Tools recommended? (seg-008)

### Topics
- [topic-001](07-topics.md#top-001) - Recording Setup
- [topic-002](07-topics.md#top-002) - K8s Network Policy Recommendations
- [topic-003](07-topics.md#top-003) - Decision Tree and Artifacts
- [topic-004](07-topics.md#top-004) - Microsoft's Recommendation
