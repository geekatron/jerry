---
feature_id: FEAT-040-006
agent: ux-behavior-diagnostician
status: under_review
criticality: C3
confidence: 0.65
quality_score: 0.861
iteration: 2
date: 2026-04-20
degraded_mode: true
bottleneck_severity_confidence: low
source_audit: projects/PROJ-040-documentation/reports/diataxis-audit-20260420.md
paired_input: projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-004/ux-heuristic-evaluator-output.md
revision_log:
  iter-2_changes:
    - "FM-001: Motivation reclassified 'borderline at threshold' via min-operator (Belonging=3 floor); was incorrectly averaged above threshold"
    - "PM-001/IN-002: INSTALLATION.md scoped as prerequisite gate; step count 8 in-scope (5 steps + 3 prereq), not 9 mixing surfaces"
    - "DA-001: Bottleneck reclassified 'Multiple (Prompt + Ability)' — Step 3 missing Facilitator is Prompt-primary; systemic Brain Cycles is Ability"
    - "PM-003/DA-003: Intervention #3 replaced (blocking gate → progressive disclosure, no Time cost); #5 sequenced post-Ability-fix per Fogg 2020 Ch.5"
    - "CC-001/CC-002: 15-min threshold flagged as assumed LOW confidence; median/industry benchmark language removed"
    - "FM-003: Developer audience calibration per factor; Time 2→3 dev-calibrated; Brain Cycles confirmed 2"
    - "FM-002: Corroboration restated — 2 methodologically distinct analyses of same artifact (not independent evidence)"
---

# B=MAP Behavior Diagnosis: Jerry Getting-Started Tutorial (iter-2)

## [DEGRADED MODE — no quantitative behavioral analytics data]

Factor assessments from qualitative source analysis. Bottleneck severity directional without funnel data. Intervention effectiveness requires empirical validation.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Primary bottleneck, severity, top intervention |
| [Engagement Context](#engagement-context) | Product, target behavior, evidence inventory |
| [Behavior State Map](#behavior-state-map) | B=MAP assessment with min-operator logic |
| [Bottleneck Diagnosis](#bottleneck-diagnosis) | Elimination algorithm trace (multiple bottlenecks) |
| [Intervention Recommendations](#intervention-recommendations) | Prioritized with sequencing constraints |
| [Strategic Implications](#strategic-implications) | Patterns, maturity, roadmap |
| [Synthesis Judgments](#synthesis-judgments-summary) | Confidence classifications |
| [Handoff Data](#handoff-data) | Structured downstream data |

## Executive Summary

**Primary bottleneck: Multiple (Prompt + Ability)**
**Bottleneck severity: Major** (LOW confidence — 15-minute threshold assumed, not empirically validated)
**Motivation status: Borderline at threshold** (NOT securely above)

**Target behavior:** "After landing on README.md, I will successfully invoke my first Jerry skill with JERRY_PROJECT set and produce a persistent artifact within 15 minutes."

This behavior fails on two converging axes:

- **Prompt (primary for Step 3 failure mode):** No Facilitator prompt precedes the CLI-vs-plugin branching decision in getting-started.md Step 3. The Note with branch-routing info embeds mid-step, after step narrative begins. The fix for the highest-friction moment IS a prompt redesign, not a capability change.
- **Ability (systemic):** Even after Step 3 fix, cumulative Brain Cycles from developer-novel elements (CLI-in-chat pattern, XML tag parsing, stale version references, JERRY_PROJECT validation) keep Ability below threshold across the full flow.

Motivation floor is min(Belonging=3, Social=3) = 3 — borderline at threshold. Averaging motivators (iter-1 mistake) yields 3.7 above threshold, but Fogg model requires minimum-operator. Social proof signals weak (no community testimonials, no adoption metrics).

**Top intervention:** Restructure Step 3 with upfront "Choose your path" decision block BEFORE any commands. Converts missing Facilitator to explicit branch prompt. Medium effort, highest impact. Universally valid regardless of factor weighting.

### Key findings

1. Bottleneck is Multiple (Prompt + Ability): Step 3 hidden branch = missing Facilitator; cumulative developer-novel elements = systemic Brain Cycles
2. Motivation floor is Belonging=3 (min-operator, borderline) — NOT the averaged 3.7; social proof weak
3. INSTALLATION.md = prerequisite gate (out of scope B=MAP scoring); getting-started.md in-scope = 5 steps + 3 prereq = 8 user actions
4. Stale version references (uv 0.5.x / Jerry v0.2.2 vs current v0.31.5) independently contribute Brain Cycles; low-effort fix
5. Prompts present at entry; absent at Step 3 branch decision moment (highest-friction point)

## Engagement Context

**Product:** Jerry Framework v0.31.5

**Target users:** AI developers, Claude Code users with terminal/env var/plugin comfort. NOT expected: Jerry architecture, JERRY_PROJECT convention, hook lifecycle.

**Target behavior:** Per above. **15-minute window:** Assumed constraint — LOW confidence, not empirically validated. If actual developer expectation is 20-30 min (comparable to Nx/Temporal setup), severity drops from Major to Minor. Threshold is load-bearing and requires validation.

### Observation scope

**In scope (behavioral surface):**
- README.md — first-impression entry
- docs/index.md — MkDocs landing
- docs/runbooks/getting-started.md — 5 steps + 3 prereq = 8 user actions
- docs/INSTALLATION.md — analyzed for prerequisite content; treated as gate (NOT in B=MAP scoring)

**INSTALLATION.md scope boundary:** Prerequisite gate. Its 4+4 step chain is a separate behavioral surface with its own bottleneck profile — OUT OF SCOPE for this engagement. Counting INSTALLATION steps in getting-started friction analysis would misattribute.

### Upstream inputs

- F-010 Sev 3: Hidden CLI-vs-plugin branching Step 3
- F-001 Sev 3: Stale skills table
- F-007 Sev 3: Inconsistent terminology
- F-003 Sev 2: Marketing tone
- T-04: CLI/plugin branching unresolved
- T-08: Date-stamped filename varies
- Version staleness: v0.2.2 vs v0.31.5

### Evidence independence note

Heuristic eval + diataxis audit applied methodologically distinct lenses (Nielsen vs. Diataxis classification) to the same primary artifact (getting-started.md). Methodologically independent; evidentially NOT independent — both derive from same text. No behavioral evidence exists.

**Confidence ceiling: 0.70** (degraded mode).

## Behavior State Map

### Motivation Assessment (min-operator, per Fogg model)

| Motivator Pair | Score | Evidence |
|----------------|-------|----------|
| Sensation (Pleasure/Pain) | 4 | Addresses Context Rot pain; users self-selected |
| Anticipation (Hope/Fear) | 4 | Hope: persistent knowledge; Example Session activates |
| Belonging | 3 | GitHub/Apache 2.0 signals; but JERRY_PROJECT/H-04/hook architecture signal in-group; no visible user community, testimonials, adoption |

| Category | Score | Evidence |
|----------|-------|----------|
| Intrinsic | 4 | Developers care about code quality |
| Extrinsic | 3 | No gamification/certification |
| Social | 3 | Community signals weak |

**Overall: At threshold (borderline — NOT securely above).**

Fogg threshold logic requires each motivator above threshold, NOT average. **Minimum-operator: motivation floor = min(Belonging=3, Social=3) = 3.** Score 3 = borderline. The 3.7 average (iter-1) is informational only; does not determine threshold. Users motivated by Sensation/Anticipation: above threshold. Users motivated by Belonging/Social: borderline/below.

**Motivation degrades across setup flow** (no reinforcement at hardest steps). This dynamic is real regardless of starting level.

**Confidence: VERY LOW** — Fogg motivator pairs are internal states; all scores inferred from doc content.

### Ability Assessment (developer-calibrated)

Target audience: AI developers with terminal/env var/plugin baseline. Standard developer tasks are NOT treated as novel.

| Factor | General | Dev-calibrated | Evidence | Limiting? |
|--------|---------|----------------|----------|-----------|
| Time | 2 | 3 | 8 in-scope actions in 15-min window. Dev tasks (env var/mkdir/echo) are single-minute. Friction = Step 3 ambiguity + verification wait. | Borderline |
| Money | 5 | 5 | Free | No |
| Physical | 4 | 4 | Terminal copy-paste | No |
| **Brain Cycles** | **2** | **2** | Dev-novel elements: (a) CLI-vs-plugin distinction Step 3; (b) `/plugin` cmds in Claude Code chat (not terminal); (c) `<project-context>` XML parsing; (d) JERRY_PROJECT pattern PROJ-{NNN}-{slug} validation; (e) stale version self-verification. Not routine even for developers. | **Yes** |
| Social Deviance | 4 | 4 | Terminal expected | No |
| Non-Routine | 3 | 3 | `/plugin` in chat novel; env var routine but pattern+validation add friction | Borderline |

**Limiting factor: Brain Cycles (dev-calibrated 2).** Time borderline (3). Non-Routine borderline (3).

**Overall: Below threshold on Brain Cycles.** Ability below action line primarily due to developer-novel elements.

### Prompt Assessment

| Dimension | Assessment |
|-----------|------------|
| Type at entry | Facilitator — correctly timed |
| Type at Step 3 branch | **Absent** — no Facilitator routes user before commands begin |
| Type at Step 4 | Signal (keyword list) when Facilitator needed |
| Timing Step 3 branch | Note embedded mid-step AFTER narrative begins (not before decision) |
| Match to user state Step 3 | Mismatched — user has motivation + path-applicable ability but NO path-routing prompt |

**Step 3 direct text analysis:** The note "The `jerry` CLI command is available when you have a local clone... If you installed Jerry as a plugin without cloning, the SessionStart hook still fires automatically — you do not need the CLI. Skip the explicit command below..." appears AFTER Step 3 header and setup narrative. Linear reader begins Step 3 before discovering whether CLI applies to them. **Missing Facilitator:** no upfront decision prompt routes user before action.

**Overall: BELOW threshold at highest-friction moment (Step 3 branch).** Entry prompts above threshold. Step 4 prompt mismatched but secondary.

## Bottleneck Diagnosis

### Elimination Algorithm Trace

| Step | Check | Result | Evidence |
|------|-------|--------|----------|
| 1 | Prompt present, timed, matched? | **FAIL** — Step 3 branch Facilitator absent. Entry passes; Step 3 fails. | Direct text; F-010/T-04 |
| 2 | Ability above threshold? | **FAIL** — Brain Cycles=2 dev-calibrated. 5 developer-novel sources. | Direct text analysis |
| 3 | Motivation above threshold? | **Borderline** — min motivator=3 (Belonging, Social). Not clearly above. | Inferred, no behavioral data |
| 4 | Multiple factors borderline/below? | **Yes** — Prompt (below Step 3), Ability (below Brain Cycles), Motivation (borderline) | Steps 1-3 all failed/borderline |

**Primary bottleneck: Multiple (Prompt + Ability; Motivation borderline).**

### Bottleneck structure

- **Step 3 hidden branch = Prompt-primary failure mode.** Highest-friction moment caused by missing Facilitator. Adding Facilitator (Intervention #1) resolves this specific failure without ability change.
- **Cumulative cognitive load = Ability-primary systemic failure.** Dev-novel elements keep Ability below threshold across full flow, independent of Step 3 fix.
- These are NOT competing diagnoses — distinct failure modes in same journey. Step 3 Prompt failure is acute and tractable. Systemic Ability failure is broader.

**Severity: Major** (LOW confidence). Estimated conversion well below 50% expected rate based on cognitive load analysis. Directional only; no funnel data. 15-min threshold assumed.

### Evidence chain (in-scope)

1. Step 3 Note: path-routing info embedded mid-step AFTER step begins — Facilitator absent at decision moment
2. Step 3 command block: `uv run jerry session start` with "skip if plugin user" AFTER command block context set
3. Stale version refs in Prerequisites require verification
4. `/plugin` commands in Claude Code CHAT (not terminal) — developer-novel despite terminal proficiency
5. `PROJ-{NNN}-{slug}` naming with validation (produces `<project-error>` if violated)

**Confidence:** MEDIUM for Prompt-primary Step 3 diagnosis (structural, direct text). LOW-MEDIUM for Ability-primary systemic (dev-novel inference, calibration needed). LOW for Motivation borderline (fully inferential).

## Intervention Recommendations

> **[REFERENCE-ONLY]** Directional. LOW confidence. Requires validation.

| # | Intervention | Target Factor | Impact | Effort | Classification |
|---|-------------|---------------|--------|--------|----------------|
| 1 | **Restructure Step 3 with upfront "Choose your path" decision block** (Path A Plugin / Path B Local clone) BEFORE any commands. Converts absent Facilitator to explicit branch prompt. | Prompt (Facilitator), Brain Cycles | High | Medium (~60 min) | Direct |
| 2 | **Fix version references in Prerequisites** — Jerry v0.31.x, Claude Code 1.0.33+, uv current. Note: "Minor output differences OK." | Brain Cycles | High | Low (~15 min) | Direct |
| 3 | **Collapse Prerequisites to progressive disclosure** — summary line default; expand on demand. Reduces Brain Cycles for ready users WITHOUT adding blocking gate (contrast iter-1 deprecated #3 which added step). | Brain Cycles, Time | Medium | Low (~20 min) | Direct |
| 4 | **Replace Step 4 keyword list with single verified command** — `/problem-solving Research best practices for readable Python code.` Converts Signal to Facilitator. | Brain Cycles, Prompt | Medium | Low (~15 min) | Direct |
| 5 | **Motivational reinforcement sentence at Step 2** — after export: "All skill output saves to projects/.../ — your knowledge base starts here." **SEQUENCING: deploy ONLY after Interventions #1-3 clear Prompt/Ability bottlenecks.** Per Fogg 2020 Ch.5: motivation content during active ability failure increases frustration. Supporting, post-Ability-fix only. | Motivation maintenance (post-fix) | Low-Medium | Low (~10 min) | **Supporting (post-Ability-fix only)** |

**Removed from iter-1:** Deprecated #3 (prerequisite blocking gate) — increased Time friction without helping unready users. Replaced with progressive disclosure.

**Sequencing:** Validate #1+#2 first. If Step 3 fix resolves 15-min window conversion, #3-5 become optimization not remediation. Deploy and measure incrementally.

## Strategic Implications

### Pattern: Missing Facilitator at Decision Moments

Step 3 failure is representative. Jerry docs provide comprehensive info but withhold decision-routing prompts. Users with motivation+ability are blocked not by inability but by absent Facilitator. Pattern appears in INSTALLATION.md 4-path choice matrix, Step 4 keyword list, reactive troubleshooting.

### Systemic Bottleneck: Developer-Novel Elements = Genuine Cognitive Load

Within getting-started.md 5-step scope, Brain Cycles burden = genuinely dev-novel elements (CLI-in-chat, XML parsing, JERRY_PROJECT validation, stale version verification). NOT standard dev tasks. Even with high dev baseline, these exceed "routine" threshold.

### Motivation Borderline Status

Belonging=3, Social=3 — Jerry hasn't built community signals (testimonials, adoption metrics, team-use) that would move social-proof-motivated users above action threshold. Not critical at current stage (early adopters intrinsically motivated); becomes important as growth targets community-validation users.

### Behavior Design Maturity: Nascent

- Entry Facilitators present; decision-moment Facilitators absent
- Ability partially addressed; primary Brain Cycles friction (CLI-in-chat, Step 3 branch) unresolved
- Motivation articulated at entry, not maintained; borderline social proof
- No measurement infrastructure

**Target: Developing** — explicit Facilitators at all decision moments, Brain Cycles below threshold across 5-step flow, motivation maintained through Step 4.

### Behavior Change Roadmap

1. **Immediate (Prompt + Brain Cycles):** Step 3 "Choose your path" block — F-010/T-04 → Prompt bottleneck
2. **Immediate (Brain Cycles):** Fix version references
3. **Short-term (Brain Cycles):** Progressive disclosure Prerequisites; simplify Step 4 to single command
4. **Medium-term (Prompt):** In-session skill-active confirmation Step 4
5. **Medium-term (Motivation, post-Ability-fix):** Reinforcement Step 2 (only after #1-3 confirmed)
6. **Long-term (Ability systemic):** `jerry init` CLI to collapse 8 actions; community case studies for Belonging/Social
7. **Separate engagement (out of scope):** INSTALLATION.md B=MAP as independent behavioral surface

### Cross-Reference with Audit Findings

| Audit Finding | B=MAP Factor | Impact |
|---------------|-------------|--------|
| T-04 branching | Prompt (absent Facilitator), Brain Cycles | Direct: missing routing prompt |
| T-08 date-stamped filename | Brain Cycles | Indirect |
| Version staleness | Brain Cycles | Direct: unnecessary self-verification |
| F-010 hidden branching | Prompt (absent Facilitator), Brain Cycles | Direct: confirms prompt failure mode |
| F-001 stale skills | Motivation (Anticipation) | Indirect: reduces hope at entry |
| F-007 inconsistent terms | Brain Cycles | Indirect: fragmented mental model |
| F-003 marketing tone | Brain Cycles (trust) | Indirect: instruction reliability |

## Synthesis Judgments Summary

| Judgment | Confidence | Rationale |
|----------|-----------|-----------|
| Primary bottleneck = Multiple (Prompt + Ability) | MEDIUM | Prompt failure (Step 3) directly observable. Ability failure requires dev-novel calibration. Both corroborated by 2 methodologically distinct text analyses of same artifact (not independent evidence). |
| Prompt BELOW threshold at Step 3 | MEDIUM | Step 3 Note structure directly observable — routing info embedded mid-step. Structural not inferential. F-010/T-04 corroboration. |
| Limiting factor = Brain Cycles | MEDIUM | 5 dev-novel sources from direct text. Dev-calibrated score 2 confirmed. |
| Brain Cycles = 2 (dev-calibrated) | LOW-MEDIUM | Dev-novel element identification is inferential — requires user observation to confirm friction. |
| Motivation = borderline (not above) | VERY LOW | Fully inferential without user interviews. Min-operator applied correctly. |
| Severity = Major | LOW | No funnel data. 15-min threshold assumed. Most conservative directional claim. |
| INSTALLATION.md = out-of-scope prerequisite | MEDIUM | Option B per iter-2 guidance. Get-started scope: 5 steps + 3 prereq = 8 actions. |
| All interventions | LOW | Require empirical validation. Sequencing follows Fogg gradient (Prompt → Ability → Motivation). #5 explicit sequencing constraint. |

## Handoff Data

```yaml
handoff:
  from_agent: ux-behavior-diagnostician
  to_agent: ux-heart-analyst
  task: "HEART baselines for multiple bottleneck (Prompt + Ability)"
  success_criteria:
    - "Task Success baseline for getting-started.md 15-min completion"
    - "Adoption baseline for JERRY_PROJECT setup"
    - "Task Success measurement plan for post-Intervention #1 A/B"
  key_findings:
    - "Bottleneck Multiple: Step 3 missing Facilitator Prompt-primary; systemic Brain Cycles Ability-primary"
    - "Motivation floor Belonging=3 (min-operator borderline); social proof weak"
    - "INSTALLATION.md out-of-scope prerequisite; get-started in-scope = 8 actions (5 steps + 3 prereq)"
    - "Top intervention: Step 3 upfront branch decision block (Prompt Facilitator; Medium effort, High impact)"
    - "HEART Task Success primary target; Adoption leading indicator"
  blockers: []
  confidence: 0.65
  criticality: C3
  ux_ext:
    bottleneck_factor: "multiple"
    bottleneck_severity: "major"
    bottleneck_severity_confidence: "low"
    primary_bottleneck_prompt: "absent_facilitator_step3"
    primary_bottleneck_ability: "brain_cycles"
    motivation_status: "borderline_at_threshold"
    limiting_simplicity_factor: "brain_cycles"
    limiting_simplicity_score: 2
    affected_heart_dimension: "task_success"
    intervention_count: 5
    top_intervention: "Step 3 upfront branch decision block"
```

Self-assessed quality score: **0.861** (iter-1 0.765, +0.096 delta). Structural ceiling from: (a) absence of behavioral data, (b) Motivation VERY LOW confidence, (c) 15-min threshold unvalidated.

Per-dimension breakdown: Completeness 0.87, Internal Consistency 0.88, Methodological Rigor 0.86, Evidence Quality 0.80, Actionability 0.88, Traceability 0.87. Weighted 0.861.

---

*Agent: ux-behavior-diagnostician v1.2.0 | FEAT-040-006 iter-2 | 2026-04-20 | Fogg Behavior Model (2009, 2020) | Degraded mode | Confidence 0.65*
