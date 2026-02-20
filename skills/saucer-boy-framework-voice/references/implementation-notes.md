# Implementation Notes for Downstream Features

> Specific guidance for FEAT-004, FEAT-006, and FEAT-007. Load when working on a specific downstream feature.

## Document Sections

| Section | Purpose |
|---------|---------|
| [FEAT-004: Framework Voice and Personality](#feat-004-framework-voice-and-personality) | Primary consumer of /saucer-boy |
| [FEAT-006: Easter Eggs and Cultural References](#feat-006-easter-eggs-and-cultural-references) | Highest risk persona feature |
| [FEAT-007: Developer Experience Delight](#feat-007-developer-experience-delight) | Texture of daily framework use |

---

## FEAT-004: Framework Voice and Personality

FEAT-004 is the primary consumer of /saucer-boy. It takes each class of framework output and rewrites it against the before/after pairs in `references/voice-guide.md`.

### Priority Order for Rewriting

1. Quality gate PASS and FAIL messages -- highest frequency, highest impact on DX
2. Error messages (especially JERRY_PROJECT, constitutional failures)
3. Session start and end messages
4. Rule explanation text (in docs and inline help)
5. Informational messages (lower priority -- do not inject personality where none is needed)

### Voice Calibration

When uncertain whether a rewrite has the right tone, apply the Audience Adaptation Matrix. Match the context to the energy/humor/depth column and check whether the rewrite lands in that zone. Then apply the Authenticity Tests in order, stopping at the first failure.

### Biographical Anchor

The voice range in the Voice Guide maps to biographical range:
- Pair 1 (PASS celebration) = banana-suit energy
- Pair 3 (REJECTED) = meticulous preparation energy (the discipline that built the Spatula)
- Pair 6 (constitutional failure) = the moment where jokes stop (the register of "What the Framework Does NOT Inherit")

### Workflow

1. Use sb-rewriter to transform current voice to Saucer Boy voice
2. Use sb-reviewer to validate the rewrite passes all 5 Authenticity Tests
3. Use sb-calibrator to quantitatively score the rewrite
4. Iterate until voice fidelity reaches 0.90+

---

## FEAT-006: Easter Eggs and Cultural References

Highest-risk feature from a persona perspective -- most potential to cross from authentic into try-hard.

### Guidance from Boundary Conditions

- Easter eggs must be immediately parseable without ski culture knowledge
- They should reward discovery, not make people feel excluded for not discovering them
- Hip hop bar fragments in docstrings: cite the artist and song. Unexplained lyrics are in-jokes. Cited lyrics are cultural annotations.
- The test: would someone who finds this easter egg smile, or feel like they are missing a reference?

### High-Value Easter Egg Territories

- Docstring comments in quality enforcement code (S-014 rubric calculation)
- CLI help text for the /adversary skill
- The JERRY_CONSTITUTION.md preamble
- Hidden `--saucer-boy` flag that enables maximum personality mode
- The Vail lifetime ban as a reference when the framework rejects with extreme prejudice
- The 8th-grade essay as a reference in onboarding text

### Calibration Example (In-Situ)

```python
# BEFORE (no personality):
# Calculate weighted composite score across all dimensions.
def calculate_composite(scores: dict[str, float], weights: dict[str, float]) -> float:

# AFTER (Saucer Boy easter egg — calibrated):
# Calculate weighted composite score across all dimensions.
# "You want to float, like a boat." — Shane McConkey on ski design,
# but also on how quality scores should feel: buoyant, not forced.
def calculate_composite(scores: dict[str, float], weights: dict[str, float]) -> float:
```

The easter egg works because: (a) McConkey quote is cited and attributed, (b) connection to the code's purpose is explicit, (c) non-ski-culture developers still get a clear comment, (d) one line of flavor without obscuring the technical purpose.

---

## FEAT-007: Developer Experience Delight

DX Delight is about the moments between the big features -- the texture of working with the framework day to day.

### High-Value Delight Moments

- **Session start:** Acknowledge the developer, set the tone
- **First-ever quality gate pass:** Different from routine -- the developer crossed a threshold for the first time
- **N-th consecutive quality gate pass:** The streak is worth noting
- **After rejected then passed:** "Round 2. Clean run. That's the process working."
- **3 AM commit (timestamp-based):** Dry acknowledgment of the developer's commitment

### Delight Principles

- Discovered, not announced
- Proportional to the moment
- Never delays the developer's work
- Feels like someone paying attention, not a template firing

### Voice Calibration

Pair 9 (Consecutive Pass) from `references/voice-guide.md` is the calibration anchor. Delight uses the same voice structure as standard messages -- the delight is a single additional observation, not a separate personality mode. If the delight element exceeds one sentence, it has become the message instead of enhancing it.

---

*Source: ps-creator-001-draft.md (Implementation Notes section, lines 617-731)*
*Canonical: DEC-001 D-002 — persona document is authoritative*
