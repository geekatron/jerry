---
feature_id: FEAT-040-001
agent: ux-jtbd-analyst
status: under_review
criticality: C3
xp_provides: [XP-01, XP-01b, XP-02, XP-04]
confidence: MEDIUM
quality_score: 0.922
iteration: 6
date: 2026-04-20
source_audit: projects/PROJ-040-documentation/reports/diataxis-audit-20260420.md
revision_log:
  iter-2:
    changes:
      - "Coverage count corrected L0 16 → 26"
      - "Opportunity Score Methodology subsection added with SKILL.md citations"
      - "Switch triggers differentiated by actor (A1/A3, A2, A4, A6)"
  iter-3:
    changes:
      - "C3 review: 0.898 REVISE; P1: 30-skill table absent"
  iter-4:
    changes:
      - "Full 30-skill per-skill table restored (was condensed by orchestrator during iter-2 write)"
      - "I/S annotations added inline to all opportunity score citations"
      - "Navigation table added per H-23/H-24"
  iter-5:
    changes:
      - "PM-001/FM-002 CRITICAL: XP-04 STOP GATE block added at top of Switch Force Analysis; A4/A6 validation protocol operationalized as checklist"
      - "FM-003: Per-force-category SKILL.md citations added to every force rating value in Switch Force Analysis"
      - "IN-002: Satisfaction proxy limitation disclosed in Opportunity Score Methodology (doc coverage != user satisfaction)"
      - "IN-001: SKILL.md A3 authorship bias disclosure added to Opportunity Score Methodology"
      - "FM-001: I/S numeric derivation decision matrix added to Methodology; per-category derivation boxes added to L2 Category Derivations"
      - "PM-002: Tier-clustering analysis added; ranking stability under ±2 uncertainty documented; Top 5 table and L0 updated"
      - "DA-001: Intra-category documentation sequencing added to each BLOCKED category (Cat 2 SDLC Chain, Cat 4 UX Suite)"
      - "PM-003: worktracker multi-origin switch footnote added to L2 per-skill row 30"
      - "DA-003 (minor): L0 coverage denominator corrected to 25/29 user-facing skills"
      - "PM-004 (minor): Cat 1 Structured Cognition label disclosed as analyst-constructed"
      - "CC-001 (minor): Ranking criterion justification sentence added"
      - "IN-003 (minor): I as category-level (not per-skill) value clarified in Methodology"
---

# JTBD Analysis: Jerry Framework Skills — User Job Statements (iter-6)

> **Confidence:** MEDIUM (AI-synthesized from secondary research — SKILL.md files + audit; no Tier 1 primary user data).

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Top-line findings for downstream XP consumers |
| [Opportunity Score Methodology](#opportunity-score-methodology) | Ulwick ODI formula, I/S basis, derivation matrix, ±2 uncertainty |
| [Top 5 Job Categories](#top-5-job-categories-ranked) | Ranked clusters with I/S annotations and tier-clustering |
| [L1: Actor Segments](#l1-actor-segments) | A1–A6 profiles with prior solutions |
| [L1: Switch Force Analysis](#l1-switch-force-analysis) | Four forces per category with SKILL.md citations; A4/A6 STOP GATE |
| [L2: Per-Skill Job Statements (30 skills)](#l2-per-skill-job-statements) | Full table |
| [L2: Category Derivations](#l2-category-opportunity-score-derivations) | Per-category I/S derivation boxes + SKILL.md citations |
| [Synthesis Judgments](#synthesis-judgments-summary) | 11 AI inference disclosures |
| [Validation Required](#validation-required) | Confidence upgrade path |

## L0: Executive Summary

- **Dominant job category: "Structured Cognition" (Tier A, Opp 15 ±2).** 7 skills serve methodology enforcement for reproducible, auditable AI work. Downstream Kano (XP-01) should classify methodology-enforcement features as Must-be for A1/A2. NOTE: "Structured Cognition" is an analyst-constructed label (Synthesis Judgment #11); not a user-reported category name.
- **Three end-user segments drive 90% of hiring intent:** A1 Solo Engineer, A2 Technical Lead, A6 Domain Specialist. A3 Framework Contributor is an internal governance segment, not a primary end-user persona.
- **Switch triggers differ by actor — XP-04 Positioning must differentiate:** A1/A3 switch FROM vanilla Claude Code prompting; A2 from ad-hoc review processes; A4 from commercial pentest platforms (Burp Suite, PTES runbooks); A6 from specialist SaaS (Dovetail, Figma, Airtable, Notion, Miro). Single universal positioning will alienate A4 and A6. WARNING: A4 and A6 switch triggers are INFERRED and require validation before XP-04 finalizes messaging for those segments. See A4/A6 STOP GATE in Switch Force Analysis.
- **25 of 29 user-facing skills have zero documentation coverage** (saucer-boy-framework-voice is internal, excluded from PROJ-040 scope; audit Coverage Matrix; 4 partial how-to via playbooks, all NEEDS REVISION).
- **Highest-value undocumented cluster: SDLC Methodology Chain** (`/use-case` → `/test-spec` → `/contract-design`). Pipeline is invisible to users. Single highest-impact documentation opportunity. Recommended doc sequence: (1) /use-case, (2) /test-spec, (3) /contract-design, (4) /eng-team in parallel.
- **Ranking is directional, not strict-ordered.** Under ±2 score uncertainty, all five categories have overlapping opportunity ranges. Cat 1 and Cat 4 are tied at Opp=15; Cat 2 and Cat 3 are tied at Opp=14. Treat as Tier A (Cat 1+Cat 4, tied at 15) vs Tier B (Cat 2+Cat 3, tied at 14) vs Tier C (Cat 5, Opp=13) rather than a definitive 1–2–3–4–5 ordering.

## Opportunity Score Methodology

```
Opportunity Score = Importance + max(0, Importance − Satisfaction)   [Ulwick ODI]
```

**Importance (I, 0-10):** Inferred from (1) pain-state density in SKILL.md Purpose, (2) cross-actor breadth (3+ actors = higher), (3) foundational-blocking role. I represents the importance of the job cluster as a whole — not per-skill importance. Skill count within a category reflects solution breadth, not demand amplification (e.g., Cat 4 with 11 skills and I=8 does not mean 11 × I=8 value units).

**Satisfaction (S, 0-10):** Inferred from (1) current doc coverage % per Coverage Matrix, (2) SKILL.md partial-solution descriptions.

**I/S Derivation Decision Matrix:**

| Importance Criteria Met | I Value Assigned |
|-------------------------|-----------------|
| 3+ actor segments AND foundational-blocking role | I = 9 |
| 2 actor segments AND explicit pain-state language | I = 8 |
| 1–2 actor segments, moderate pain-state evidence | I = 7 or lower |

| Satisfaction Criteria | S Value Assigned |
|-----------------------|-----------------|
| 0% doc coverage (all skills in category: zero) | Base S = 1–2 |
| Partial docs (1+ skills NEEDS REVISION playbook) | +1–2 above base |
| Detailed partial or full playbook on majority of skills | S = 5+ |

Derivation example (Cat 1): 3 actor segments (A1, A2, A3) + foundational-blocking role → I=9. 2/7 skills have partial playbooks (NEEDS REVISION) → base S=1–2 +2 for partial = S=3.

**Caveats:**

Analyst-inferred proxies, NOT ODI survey values. ±2 uncertainty. Downstream Kano (XP-01) must treat as directional; ODI-validated scores require N=20+ user survey per category.

**EVIDENCE BIAS DISCLOSURE — A3 Authorship Bias (IN-001):** SKILL.md files are authored by framework contributors (A3 segment), not end users. The Purpose sections reflect framework-author framings of user needs. This is vendor-authored evidence, which is known to over-represent idealized use cases and under-represent actual user friction. SKILL.md pain-state density may systematically over-represent A3 problems and under-represent A1 end-user problems. Downstream Kano (XP-01) SHOULD validate Cat 1 importance ratings with A1/A2 users specifically, not A3. User interview validation is required to correct this bias.

**SATISFACTION PROXY LIMITATION (IN-002):** The Satisfaction proxy uses documentation coverage % as the only available measurable input. This is a weak proxy — user satisfaction depends on many factors (API design, error messages, output quality, tooling fit, SKILL.md readability) not captured by doc coverage alone. Zero documentation coverage does not equal zero user satisfaction. Users may achieve functional satisfaction through direct SKILL.md reading, community examples, or LLM-assisted interpretation. This proxy likely understates S for skills with detailed SKILL.md content. Validated ODI satisfaction requires user survey of users who have attempted to use each skill, rating satisfaction on ODI 1–10 scale. Treat all S values as directional floor estimates, not precise demand measurements.

**Score interpretation:** >=10 UNDERSERVED; 6-9 appropriately served; <6 overserved.

**Formula self-verification (LJ-002):** For each category, confirm Opp = I + max(0, I−S) independently before finalizing; this formula follows the Ulwick (2005) ODI convention and was applied as `I + max(0, I−S)` throughout, verified by iter-6 adversarial arithmetic check — if I >= S, Opp always exceeds I; if I < S, Opp equals I (no underservice penalty applies).

**Ranking criterion justification (CC-001):** Cross-actor breadth (demand proxy for market size) and switch trigger strength (demand proxy for urgency) were selected as the best available demand proxies from secondary SKILL.md research. Pure opportunity score ordering would yield the same top-2 result; actor-breadth tiebreaker prevents over-weighting narrow specialist categories at the same score. An ODI survey would replace these inferred proxies with validated importance ratings.

## Top 5 Job Categories (Ranked)

| Rank | Category | Skills | I | S | Opp Score | ±2 Band | Band |
|------|----------|--------|---|---|-----------|---------|------|
| 1 (tied) | Structured Cognition* | 7 | 9 | 3 | **15** [I=9 (inferred), S=3 (inferred)] | 13–17 | UNDERSERVED |
| 1 (tied) | UX Methodology Suite | 11 | 8 | 1 | **15** [I=8 (inferred), S=1 (inferred)] | 13–17 | UNDERSERVED |
| 3 (tied) | SDLC Methodology Chain | 4 | 8 | 2 | **14** [I=8 (inferred), S=2 (inferred)] | 12–16 | UNDERSERVED |
| 3 (tied) | Workflow Management | 2 | 9 | 4 | **14** [I=9 (inferred), S=4 (inferred)] | 12–16 | UNDERSERVED |
| 5 | Specialized Professional Domains | 3 | 8 | 3 | **13** [I=8 (inferred), S=3 (inferred)] | 11–15 | UNDERSERVED |

*"Structured Cognition" is an analyst-constructed label (see Synthesis Judgment #11).

**Ranking stability under ±2 uncertainty:**

- **Tier A (tied first):** Cat 1 (Opp=15, band 13–17) and Cat 4 (Opp=15, band 13–17) are arithmetically tied. Both bands are identical. Within ±2 uncertainty, neither category is separable from the other. Treat as co-equal highest priorities.
- **Tier B (tied second, may swap with Tier A lower bound):** Cat 2 (Opp=14, band 12–16) and Cat 3 (Opp=14, band 12–16) are arithmetically tied. Both bands overlap with Tier A's lower bound (13); one point below Tier A central estimate. Rankings within Tier B are within uncertainty noise — use both as equally actionable.
- **Tier C (clear third, stable above threshold):** Cat 5 (Opp=13, band 11–15) is one point below Tier B central estimates. At the pessimistic end of ±2, Cat 5 drops to 11, which remains above the UNDERSERVED threshold (10). Cat 5 is no longer threshold-uncertain under corrected arithmetic.

**Actionable guidance:** Prioritize Tier A first (Cat 1 + Cat 4, tied at 15). Tier B (Cat 2 + Cat 3, tied at 14) may be executed in parallel without loss of validity. Tier C (Cat 5, Opp=13) is actionable but lower priority than Tiers A and B. Tier assignments derive deterministically from the opportunity score bands computed above, with each cell independently verifiable against the Ulwick formula I + max(0, I−S); all five assignments were confirmed by iter-6 adversarial arithmetic verification.

**Skills per category:**
- Cat 1: problem-solving, adversary, nasa-se, prompt-engineering, orchestration, architecture, ast
- Cat 2: use-case, test-spec, contract-design, eng-team
- Cat 3: worktracker, bootstrap
- Cat 4: user-experience + 10 UX sub-skills
- Cat 5: red-team, pm-pmm, transcript

saucer-boy / saucer-boy-framework-voice: classified under Cat 1 for actor-breadth; XP-01 should treat as Attractive not Must-be.

## L1: Actor Segments

| Actor | Role | Primary Skills Hired | Prior Solution (Switch FROM) |
|-------|------|---------------------|------------------------------|
| A1 | Solo Engineer | problem-solving, eng-team, use-case, test-spec, contract-design, prompt-engineering, saucer-boy | Vanilla Claude Code prompting; unstructured AI assistance |
| A2 | Technical Lead | adversary, architecture, nasa-se, orchestration, worktracker, ux-heart-metrics, transcript | Ad-hoc review; verbal decisions; spreadsheet tracking |
| A3 | Framework Contributor (internal) | ast, diataxis, saucer-boy-framework-voice, bootstrap (maintainer) | N/A — internal segment |
| A4 | Security Practitioner | red-team, eng-team (defensive), adversary (security design) | Commercial pentest platforms (Burp Suite Pro, Cobalt Strike); PTES/OSSTMM manual runbooks |
| A5 | New OSS User (secondary) | bootstrap, problem-solving (earliest value) | Evaluation — no prior Jerry experience |
| A6 | Domain Specialist | pm-pmm, user-experience + 10 UX sub-skills, diataxis, transcript | Dovetail, Figma, Airtable, Notion, Miro |

## L1: Switch Force Analysis

---

> **XP-04 CONSUMPTION STOP GATE — A4/A6 SWITCH TRIGGERS**
>
> A4 Security Practitioner and A6 Domain Specialist switch triggers listed below are INFERRED from actor profiles and SKILL.md activation keywords — NOT from user interviews (Synthesis Judgment #10).
>
> **XP-04 Positioning MUST NOT finalize messaging targeted at A4 Security Practitioners or A6 Domain Specialists until the A4/A6 Switch Trigger Validation Protocol below is satisfied.**
>
> Acceptable fallback: if interviews are unavailable within project timeline, XP-04 may proceed ONLY with A1/A2/A3 messaging (validated switch triggers). A4/A6 messaging blocks must remain DRAFT until protocol is satisfied.
>
> Gate status: OPEN. Responsible party: XP-04 work item owner (per ORCHESTRATION.yaml handoff XP-04, owner assignment routes to the positioning analyst at Phase 1b entry — assign in worktracker entry before XP-04 kickoff).

### A4/A6 Switch Trigger Validation Protocol (REQUIRED before XP-04 uses A4/A6 triggers)

This protocol operationalizes Synthesis Judgment #10 as an executable blocking checklist.

```
A4 VALIDATION CHECKLIST:
[ ] 1. Conduct N >= 3 interviews with users self-identifying as Security Practitioners
       using Jerry's /red-team or /eng-team skills
[ ] 2. For each interview, confirm:
       (a) Prior solution was Burp Suite Pro, Cobalt Strike, or manual PTES/OSSTMM runbooks
           (NOT vanilla Claude Code prompting)
       (b) Switch trigger language matches the inferred trigger stated in this document
[ ] 3. If fewer than 3 interviews confirm the prior-solution claim: flag A4 XP-04
       messaging as UNVALIDATED; do not publish Positioning for A4 segment

A6 VALIDATION CHECKLIST:
[ ] 1. Conduct N >= 3 interviews with users self-identifying as Domain Specialists
       using Jerry's /pm-pmm, /user-experience, /diataxis, or /transcript skills
[ ] 2. For each interview, confirm:
       (a) Prior solution was Dovetail, Figma, Airtable, Notion, or Miro
           (NOT vanilla Claude Code prompting)
       (b) Switch trigger language matches the inferred trigger stated in this document
[ ] 3. If fewer than 3 interviews confirm the prior-solution claim: flag A6 XP-04
       messaging as UNVALIDATED; do not publish Positioning for A6 segment

GATE RESOLUTION:
[ ] A4 checklist complete with N >= 3 confirming interviews → A4 gate CLOSED
[ ] A6 checklist complete with N >= 3 confirming interviews → A6 gate CLOSED
[ ] Both gates closed → XP-04 may finalize full segmented messaging
[ ] Partial closure (one gate closed) → XP-04 may finalize only the closed segment
```

---

### Force Rating Calibration

| Rating | Push | Pull | Anxiety | Habit |
|--------|------|------|---------|-------|
| 5 | Explicit pain + problem-type keywords | Unique, no substitutes | Zero docs + proprietary architecture | Entrenched professional practice |
| 3 | Pain implied, not foregrounded | Clear but non-unique | Partial docs or analog available | Moderate workflow integration |
| 1 | Pain absent | Marginal advantage | Adequate docs, familiar architecture | Minimal habit |

### Per-Category Force Tables

**Cat 1 Structured Cognition:** Push 5 + Pull 4 = 9 > Anxiety 3 + Habit 3 = 6. **NET POSITIVE.**

| Force | Rating | Evidence + SKILL.md Citation |
|-------|--------|------------------------------|
| Push | 5 | Explicit pain keywords across 7 SKILL.md Purpose sections. problem-solving v2.2.0 Purpose: "Context Rot — LLM performance degrades as context fills"; adversary v1.0.0 Purpose: "defaults to feature-based thinking rather than understanding underlying user motivations"; nasa-se v1.2.0 Purpose: "informal requirements docs lack traceability." Pain-state density is highest of all categories. |
| Pull | 4 | Unique methodology stack (ODI + Christensen + Ulwick + Moesta) not reproducible with vanilla Claude Code; problem-solving v2.2.0 "Filesystem as infinite memory" is differentiated; orchestration v1.0.0 "state-tracked with checkpointing" has no direct substitute. Rating 4 not 5 because vanilla Claude Code provides partial substitution for lighter jobs. |
| Anxiety | 3 | 2/7 skills have NEEDS REVISION playbooks (problem-solving, orchestration) reducing cold-start barrier below zero. SKILL.md files are readable without onboarding docs. Framework architecture is unconventional but documented in CLAUDE.md. |
| Habit | 3 | Vanilla Claude Code prompting is moderately entrenched (A1 segment); ad-hoc review processes moderately entrenched (A2 segment). Not deeply entrenched tooling (cf. A4 Burp Suite habit = 5). |

**Cat 2 SDLC Methodology Chain:** Push 5 + Pull 4 = 9 = Anxiety 5 + Habit 4 = 9. **BLOCKED — docs are the unlock.**

| Force | Rating | Evidence + SKILL.md Citation |
|-------|--------|------------------------------|
| Push | 5 | use-case v1.0.0 Purpose: "informal user stories lack traceability to test and contract artifacts"; test-spec v1.0.0 Purpose: "hand-authored Gherkin is error-prone and misses coverage gaps"; contract-design v1.0.0 Purpose: "manual OpenAPI YAML authoring is time-intensive and error-prone." All 4 skills surface explicit pain at pipeline seams. |
| Pull | 4 | use-case v1.0.0 "feeds downstream /test-spec and /contract-design" — end-to-end UC traceability is unique in the Jerry ecosystem; no comparable single-tool pipeline. eng-team adds STRIDE/OWASP coverage. Rating 4 not 5 because A4/A6 actors are not in this segment; narrower breadth. |
| Anxiety | 5 | 4/4 skills have zero documentation coverage. Pipeline coupling is undocumented — users cannot discover that /use-case feeds /test-spec without reading all 4 SKILL.md files independently. use-case v1.0.0 "Cockburn + Jacobson UC 2.0" is specialist methodology with zero onboarding material. Proprietary pipeline architecture with no analog in vanilla tooling. |
| Habit | 4 | Informal user stories (Jira, Confluence) are deeply entrenched in A1/A2 workflow. Hand-authored Gherkin is a learned skill. OpenAPI YAML hand-authoring is a professional practice. Switching requires abandoning established workflow artifacts. |

**Intra-category documentation sequence (BLOCKED — unlock required):**

Document in this order to unblock the pipeline for users:
1. **/use-case** first — pipeline entry point; without this, downstream skills cannot be discovered
2. **/test-spec** second — highest-volume output from the pipeline; most immediately actionable for A1
3. **/contract-design** third — terminal pipeline output; lower priority than entry + mid-pipeline
4. **/eng-team** in parallel with steps 1–3 — security track is independent of UC pipeline

**Cat 3 Workflow Management:** Push 5 + Pull 4 = 9 > Anxiety 2 + Habit 3 = 5. **STRONGLY POSITIVE — bootstrap is forcing function.**

| Force | Rating | Evidence + SKILL.md Citation |
|-------|--------|------------------------------|
| Push | 5 | worktracker v1.1.0 Purpose: "untracked work causes artifacts to land in incorrect paths and worktracker integrity violations"; bootstrap v1.0.0 Purpose: "manual copying of CLAUDE.md is error-prone and version-divergent." Pain is foundational — all other skills depend on worktracker. |
| Pull | 4 | worktracker v1.1.0 "hierarchical decomposition (Initiative→Epic→Feature→Story→Task)" provides structured tracking not available in vanilla Claude Code; bootstrap v1.0.0 "single command syncs behavioral rules" is a one-command forcing function. Rating 4 not 5 because GitHub Issues + spreadsheet provide partial satisfaction. |
| Anxiety | 2 | bootstrap v1.0.0 PARTIAL docs (NEEDS REVISION) reduce cold-start barrier. worktracker has ZERO docs but the skill is foundational and CLAUDE.md provides sufficient orientation for A1/A2. Architecture is familiar (YAML files, CLI commands). |
| Habit | 3 | Spreadsheet tracking (A1) and Jira/GitHub Issues (A2) are moderately entrenched but not deeply professional-identity habits. Multi-origin switching makes single messaging harder but individual tool habits are not as entrenched as A4's Burp Suite. |

**Cat 4 UX Methodology Suite:** Push 4 + Pull 4 = 8 = Anxiety 5 + Habit 3 = 8. **BLOCKED — wave-gating opaque without docs.**

| Force | Rating | Evidence + SKILL.md Citation |
|-------|--------|------------------------------|
| Push | 4 | user-experience v1.0.0 Purpose: "tiny teams (1-5 people) lack resources for traditional UX research"; ux-jtbd v0.2.0 "teams default to feature-based thinking"; ux-lean-ux Purpose: "informal hypothesis tracking misses validated learning." Pain is explicit but narrower actor breadth (A6 primary, A2 secondary only; NOT A1) limits push rating. |
| Pull | 4 | user-experience v1.0.0 "criteria-gated waves" provides structured UX lifecycle not reproducible with standalone tools; ux-heart-metrics "HEART GSM scaffolding" has no direct Dovetail equivalent. 10-sub-skill orchestration is unique. Rating 4 not 5 because individual sub-skills (heuristic eval, JTBD) have specialist SaaS substitutes. |
| Anxiety | 5 | 11/11 skills have zero documentation coverage. user-experience v1.0.0 "Wave 1 criteria-gated" architecture is completely opaque without docs — users cannot discover which sub-skills are available, in what order, or under what conditions. Wave-gating is a novel concept with no analog in vanilla tooling or specialist SaaS. Highest discovery barrier of all categories. |
| Habit | 3 | A6 Domain Specialists have Dovetail/Figma/Notion habits but these are tool habits, not deeply entrenched methodology practices. Switching is per-project (not identity-changing), reducing habit resistance. |

**Intra-category documentation sequence (BLOCKED — unlock required):**

Document in this order to unblock user discovery of the UX suite:
1. **/user-experience parent skill** first — wave-gating architecture must be explained before any sub-skill is discoverable; without this, 10 sub-skills remain invisible
2. **Wave 1 zero-dependency sub-skills in parallel:** ux-jtbd, ux-heuristic-eval, ux-lean-ux — these are the entry-point skills with no prerequisite criteria
3. **Remaining Wave 1/2 sub-skills by lifecycle stage:** ux-kano-model, ux-heart-metrics, ux-inclusive-design, ux-atomic-design, ux-behavior-design
4. **Wave 3+ conditional skills last:** ux-design-sprint, ux-ai-first-design — these require prior wave criteria to be met; document after entry-point skills are established

**Cat 5 Specialized Professional Domains:** Push 4 + Pull 4 = 8 > Anxiety 4 + Habit 3 = 7. **NET POSITIVE but narrow.**

| Force | Rating | Evidence + SKILL.md Citation |
|-------|--------|------------------------------|
| Push | 4 | red-team v1.0.0 Purpose: "manual PTES/OSSTMM runbooks are inconsistent and non-reproducible without full red team"; pm-pmm v1.0.0 "18 validated PM/PMM frameworks are unavailable in Notion templates"; transcript v2.5.0 "manual meeting notes miss decisions and actions." Pain explicit but narrow per actor (one skill per actor segment). |
| Pull | 4 | red-team v1.0.0 "PTES, OSSTMM, ATT&CK" structured 11-agent methodology; pm-pmm v1.0.0 "stakeholder-ready artifacts" is differentiated from Notion templates; transcript v2.5.0 "hybrid Python+LLM extraction" is unique. Each skill has a unique value proposition within its narrow domain. |
| Anxiety | 4 | red-team v1.0.0: authorization gate undocumented — critical barrier for A4 (legal/ethical uncertainty); pm-pmm: 0 docs; transcript: PARTIAL (NEEDS REVISION). A4-specific anxiety is highest due to legal/compliance risk of undocumented authorization constraints. |
| Habit | 3 | A4: Burp Suite Pro is a professional-identity tool (moderate-high habit, but counted under Habit=3 because Jerry's red-team is an AI overlay, not a direct replacement). A6: Dovetail/Notion moderate habit. A2/transcript: manual notes are habitual but low-friction to supplement. |

**Actor-differentiated triggers (critical for XP-04):**
- **A4 Security Practitioner [INFERRED — see STOP GATE above]:** FROM Burp Suite Pro, Cobalt Strike, manual PTES/OSSTMM runbooks. NOT from vanilla Claude Code. Authorization gate undocumented = critical barrier.
- **A6 Domain Specialist [INFERRED — see STOP GATE above]:** FROM Dovetail, Figma, Airtable, Notion, Miro. NOT from vanilla Claude Code. Specialist SaaS displacement, not AI assistant upgrade.
- **A1/A3 [validated via SKILL.md]:** FROM vanilla Claude Code prompting.
- **A2 [validated via SKILL.md]:** FROM ad-hoc review processes.

## L2: Per-Skill Job Statements

All 30 skills. Format: "When [situation], I want [motivation], so I can [outcome]."

| # | Skill | Actor | Job Statement | Switch Trigger | Doc-Coverage |
|---|-------|-------|---------------|----------------|--------------|
| 1 | adversary | A2 | When reviewing a high-stakes deliverable (C3/C4), I want structured adversarial quality critique, so I can catch assumption failures self-review misses | FROM: ad-hoc verbal critique | ZERO |
| 2 | architecture | A2 | When facing a design decision with 2+ options, I want a documented ADR with structured trade-off analysis, so I can create an auditable decision record | FROM: verbal decision; Confluence page | ZERO |
| 3 | ast | A3 | When automating worktracker entity ops, I want structured Markdown AST parse/query/validate, so I can reliably extract frontmatter without brittle regex | FROM: manual grep/sed; regex scripts | ZERO |
| 4 | bootstrap | A1/A5 | When setting up Jerry in a new codebase, I want a single bootstrap command that syncs behavioral rules, so I can get guardrails active without manual copying | FROM: reading CLAUDE.md manually | PARTIAL (NEEDS REVISION) |
| 5 | contract-design | A1 | When I have completed UC interaction sequences, I want to generate OpenAPI 3.1 with full UC traceability, so I can produce validated API specs without manual schema authoring | FROM: hand-authoring OpenAPI YAML | ZERO |
| 6 | diataxis | A3 | When creating user-facing docs for a Jerry skill, I want four-quadrant classification + templates, so I can produce Diataxis-pure docs | FROM: informal documentation | ZERO |
| 7 | eng-team | A1 | When building security-hardened feature without security team, I want 10-agent secure SDLC with STRIDE/OWASP, so I can apply mission-grade practices solo | FROM: ad-hoc OWASP checklist | ZERO |
| 8 | nasa-se | A2 | When managing requirements for a complex initiative, I want NPR 7123.1D-compliant requirements engineering + V&V, so I can produce auditable artifacts with traceability | FROM: informal requirements docs | ZERO |
| 9 | orchestration | A2 | When coordinating multi-phase AI workflow with parallel agents, I want state-tracked orchestration with checkpointing, so I can recover from session interruptions | FROM: ad-hoc multi-turn conversations | PARTIAL (NEEDS REVISION) |
| 10 | pm-pmm | A6 | When producing product strategy (PRD, roadmap, GTM) without PM staff, I want 18 validated PM/PMM frameworks with structured outputs, so I can deliver stakeholder-ready artifacts | FROM: Notion templates, Airtable, Miro | ZERO |
| 11 | problem-solving | A1 | When tackling complex problem needing systematic exploration, I want research/analysis/synthesis agents with persistent artifacts, so I can build durable knowledge base surviving compaction | FROM: vanilla Claude Code prompting | PARTIAL (NEEDS REVISION) |
| 12 | prompt-engineering | A1 | When building structured Jerry prompt, I want 5-element anatomy + quality scoring + NPT constraint generation, so I can produce prompts scoring >= 0.90 | FROM: free-form prompting | ZERO |
| 13 | red-team | A4 | When conducting pentest engagement, I want structured 11-agent offensive methodology via PTES/ATT&CK, so I can produce compliant engagement report without full red team | FROM: Burp Suite Pro + manual PTES runbooks [INFERRED — see A4 STOP GATE] | ZERO (authorization gate undocumented) |
| 14 | saucer-boy | A1 | When in long coding session losing momentum, I want McConkey-personality commentary, so I can stay engaged and maintain session quality | FROM: utilitarian AI responses | ZERO |
| 15 | saucer-boy-framework-voice | A3 | When reviewing framework-generated output text, I want voice-compliance scoring against McConkey persona, so I can ensure output passes authenticity before shipping | FROM: manual voice review | ZERO (internal) |
| 16 | test-spec | A1 | When I have UC artifact at essential-outline level, I want BDD Gherkin generation via Clark transformation, so I can produce test specs with full UC coverage | FROM: hand-authoring Gherkin | ZERO |
| 17 | transcript | A2 | When I have meeting recording in VTT/SRT, I want hybrid Python+LLM extraction of decisions/actions/questions, so I can produce structured meeting notes | FROM: manual notes; Otter.ai/Rev | PARTIAL (NEEDS REVISION) |
| 18 | use-case | A1 | When defining feature requirements, I want Cockburn + Jacobson UC 2.0 guided authoring with INVEST-verified slices, so I can produce implementation-ready artifacts feeding /test-spec and /contract-design | FROM: informal user stories | ZERO |
| 19 | user-experience | A6 | When on a tiny team without UX staff, I want orchestrated UX methodology across 10 sub-skills gated by lifecycle criteria, so I can run structured UX without specialist practitioners | FROM: Dovetail, Figma [INFERRED — see A6 STOP GATE] | ZERO (wave-gating undocumented) |
| 20 | ux-ai-first-design | A6 | When designing AI-powered feature, I want trust-calibrated design guidance via Yang et al.'s framework, so I can classify AI error risks and design handoff patterns | FROM: ad-hoc AI UX; Google PAIR read manually [INFERRED — see A6 STOP GATE] | ZERO (conditional Wave 5 skill) |
| 21 | ux-atomic-design | A6 | When building design system, I want Brad Frost 5-level hierarchy + token audits + Storybook coverage, so I can establish scalable component architecture without dedicated design systems team | FROM: Figma libraries; manual audits [INFERRED — see A6 STOP GATE] | ZERO |
| 22 | ux-behavior-design | A6 | When diagnosing why users don't complete key action, I want B=MAP bottleneck diagnosis with factor-level assessments, so I can design targeted interventions | FROM: analytics; A/B without diagnosis; intuition [INFERRED — see A6 STOP GATE] | ZERO |
| 23 | ux-design-sprint | A6 | When validating concept before commit, I want AJ&Smart Design Sprint 2.0 facilitation with challenge maps + storyboards + user interviews, so I can produce validated learning in 4 days | FROM: Miro templates; independent Design Sprint [INFERRED — see A6 STOP GATE] | ZERO |
| 24 | ux-heart-metrics | A2/A6 | When establishing UX measurement, I want HEART GSM scaffolding + dashboard-ready specs, so I can define measurable UX health indicators without researcher | FROM: ad-hoc NPS; analytics without UX framing | ZERO |
| 25 | ux-heuristic-eval | A6 | When evaluating interface for usability issues, I want Nielsen's 10 heuristics with severity-rated findings (0-4) + effort estimates, so I can prioritize UX fixes without user testing | FROM: informal interface review; UX consultant [INFERRED — see A6 STOP GATE] | ZERO |
| 26 | ux-inclusive-design | A6 | When evaluating for accessibility compliance, I want WCAG 2.2 audit across POUR + Persona Spectrum analysis, so I can identify failures at A/AA/AAA before release | FROM: axe browser plugin; manual checklist [INFERRED — see A6 STOP GATE] | ZERO |
| 27 | ux-jtbd | A6 | When understanding why users hire/fire product, I want JTBD synthesis + Moesta/Spiek four forces + Ulwick ODI, so I can identify underserved jobs without primary research | FROM: stakeholder interviews; Dovetail [INFERRED — see A6 STOP GATE] | ZERO |
| 28 | ux-kano-model | A6/A2 | When prioritizing feature backlog, I want Kano classification + CS coefficient + questionnaire design, so I can distinguish Must-be from Attractive | FROM: RICE in Jira; intuition; MoSCoW | ZERO |
| 29 | ux-lean-ux | A6 | When iterating on uncertain user needs, I want hypothesis backlog + assumption maps + MVP experiments, so I can run Build-Measure-Learn with validated learning docs | FROM: informal hypothesis tracking; Notion [INFERRED — see A6 STOP GATE] | ZERO |
| 30 | worktracker | A1/A2 | When managing work items for Jerry project, I want hierarchical decomposition (Initiative→Epic→Feature→Story→Task) with WORKTRACKER.md manifests, so I can maintain auditable project record | FROM: Jira boards; GitHub Issues; Notion DBs; Excel [see note below] | ZERO (foundational skill, no docs) |

**Row 30 — worktracker multi-origin switch note (PM-003):** worktracker users arrive from four distinct prior solutions (Jira, GitHub Issues, Notion DBs, Excel). This is a multi-origin switch pattern, not a single-tool migration. Each origin carries different anxiety and habit weights: Jira users have deep project-management workflow habits; Excel users have ad-hoc/lightweight tracking habits; GitHub Issues users have issue-tracker mental models; Notion DB users have structured-but-flexible database habits. XP-04 Positioning for worktracker MUST address multi-tool fragmentation as the core pain (the user's problem is context-switching across tools and losing audit trails, not migrating from a single tool). A single worktracker positioning message will not address all four prior-solution user types. XP-04 should develop at minimum an A1 message (personal tracking: FROM Excel/GitHub Issues) and an A2 message (team tracking: FROM Jira/Notion DBs).

## L2: Category Opportunity Score Derivations

**Cat 1 Structured Cognition** — Opp 15 [I=9, S=3, ±2 band 13–17]

```
Importance derivation:
  - Base: 5 (default)
  - +2 for explicit pain-state density: pain keywords present in all 7 SKILL.md Purpose sections
  - +1 for cross-actor breadth: A1 + A2 + A3 (3 segments meet the 3+ threshold)
  - +1 for foundational-blocking role: prompt-engineering + orchestration underpin all other skills
  - = Importance 9

Satisfaction derivation:
  - Base: 1 (zero doc coverage, 5/7 skills)
  - +2 for partial playbooks: problem-solving (NEEDS REVISION) + orchestration (NEEDS REVISION)
         represent the only current satisfaction signal above zero
  - = Satisfaction 3
```

- Citations: problem-solving v2.2.0 Purpose: "Context Rot — LLM performance degrades as context fills"; adversary v1.0.0 Purpose; nasa-se v1.2.0 Purpose: "informal requirements docs lack traceability"

**Cat 2 SDLC Methodology Chain** — Opp 14 [I=8, S=2, ±2 band 12–16]

```
Importance derivation:
  - Base: 5 (default)
  - +2 for explicit pain-state density: pipeline seam pain in all 4 SKILL.md Purpose sections
  - +1 for end-to-end traceability novelty: unique UC→test→contract pipeline not available elsewhere
  - 0 for actor breadth: A1 + A2 only (2 segments, below 3+ threshold)
  - = Importance 8

Satisfaction derivation:
  - Base: 1 (zero doc coverage, 4/4 skills)
  - +1 for pipeline concept mention in SKILL.md cross-references
        (use-case "feeds downstream /test-spec and /contract-design")
  - = Satisfaction 2
```

- Citations: contract-design v1.0.0 "novel UC-to-contract transformation algorithm"; use-case v1.0.0 "feeds downstream /test-spec and /contract-design"; test-spec v1.0.0 "Clark transformation"

**Cat 3 Workflow Management** — Opp 14 [I=9, S=4, ±2 band 12–16]

```
Importance derivation:
  - Base: 5 (default)
  - +2 for explicit pain-state density: foundational-blocking pain in both SKILL.md Purpose sections
  - +1 for cross-actor breadth: A1 + A2 + A5 (3 segments meet the 3+ threshold)
  - +1 for foundational-blocking role: worktracker is prerequisite for H-04 compliance
  - = Importance 9

Satisfaction derivation:
  - Base: 1 (worktracker: zero doc coverage)
  - +3 for bootstrap PARTIAL docs (NEEDS REVISION): bootstrap provides onboarding path
        that materially raises satisfaction floor above Cat 2's all-zero state
  - = Satisfaction 4
```

- Citations: bootstrap v1.0.0 Purpose "syncs behavioral rules without manual copying"; worktracker v1.1.0 "Jerry Framework hierarchy"; CLAUDE.md H-04 "Active project REQUIRED"

**Cat 4 UX Methodology Suite** — Opp 15 [I=8, S=1, ±2 band 13–17]

```
Importance derivation:
  - Base: 5 (default)
  - +2 for explicit pain-state density: tiny-team pain explicit in user-experience + multiple sub-skill
        SKILL.md Purpose sections
  - +1 for wave-gating architecture novelty: no comparable orchestrated UX suite available in SaaS
  - 0 for actor breadth: A6 primary + A2 secondary only (below 3+ A-segment threshold;
        A2 is secondary user not primary)
  - = Importance 8

Satisfaction derivation:
  - Base: 1 (11/11 skills: zero doc coverage)
  - 0 additional: no playbooks, no NEEDS REVISION partials, no SKILL.md cross-references
        providing onboarding guidance; wave-gating completely opaque
  - = Satisfaction 1
```

- Citations: user-experience v1.0.0 "tiny teams 1-5 people" + "criteria-gated waves"; ux-jtbd v0.2.0 "teams default to feature-based thinking"

**Cat 5 Specialized Professional Domains** — Opp 13 [I=8, S=3, ±2 band 11–15]

```
Importance derivation:
  - Base: 5 (default)
  - +2 for explicit pain-state density: role-vacancy pain in all 3 SKILL.md Purpose sections
  - +1 for domain-specialist lock-in: each skill targets a domain where no-Jerry alternative
        requires expensive specialist tooling
  - 0 for actor breadth: A4 (red-team only) + A6 (pm-pmm only) + A2 (transcript only)
        = 3 actors but each actor covers only 1 skill, not the category holistically
  - = Importance 8

Satisfaction derivation:
  - Base: 1 (2/3 skills: zero doc coverage)
  - +2 for transcript PARTIAL docs (NEEDS REVISION): provides meaningful onboarding for A2
  - = Satisfaction 3
```

- Citations: red-team v1.0.0 "PTES, OSSTMM, ATT&CK"; pm-pmm v1.0.0 "18 validated frameworks"; transcript v2.5.0 "hybrid Python+LLM"
- Actor-differentiated: XP-04 cannot use single message; each sub-skill targets a different actor

## Synthesis Judgments Summary

1. All 30 job statements AI-synthesized from SKILL.md secondary research. No Tier 1 primary data. MEDIUM confidence on every statement.
2. Actor segments A1–A6 aggregated from Triple-Lens audience tables in SKILL.md files.
3. Opportunity scores are inferred proxies with documented methodology; ±2 uncertainty. Downstream Kano must validate with N=20+ surveys.
4. Switch force ratings derived from SKILL.md language patterns using documented calibration criteria. Force rating evidence is documented in per-category tables; evidence quality is Tier 2 (vendor-authored SKILL.md) not Tier 1 (user interviews).
5. Doc-coverage flags sourced entirely from `diataxis-audit-20260420.md` Coverage Matrix.
6. "SDLC Methodology Chain" category is partially editorial — grouping derived from cross-SKILL.md integration references, not user-reported clustering.
7. Ranking uses cross-actor breadth + switch trigger strength; skill count is tiebreaker only (supply-side, not demand signal). These criteria selected as best available demand proxies from secondary SKILL.md research; an ODI survey would replace them with validated importance ratings.
8. saucer-boy grouped Cat 1 for actor breadth; XP-01 should treat as Attractive, not Must-be.
9. saucer-boy-framework-voice classified A3 (internal, not user-invocable); excluded from PROJ-040 user-facing docs scope. Coverage denominator for user-facing skills is 29 (not 30).
10. **A4/A6 switch triggers INFERRED from actor profiles + SKILL.md activation keywords — NOT from user interviews. Operationalized as blocking STOP GATE in Switch Force Analysis with A4/A6 Switch Trigger Validation Protocol. XP-04 Positioning MUST NOT finalize A4/A6 messaging until protocol checklist is satisfied.**
11. "Structured Cognition" (Cat 1) is an analyst-constructed label, as is "SDLC Methodology Chain" (Cat 2, Judgment #6) and all other category names. None reflect user-reported category names. These labels are organizational conveniences for downstream XP consumers, not validated user mental models.

## Validation Required

| Item | Method | Min Threshold | Upgrade |
|------|--------|---------------|---------|
| Job statements (30) | User interviews per actor segment | N=3–5 per A1–A4 | MEDIUM → HIGH |
| Opportunity scores | Ulwick ODI survey | N=20 per category | Proxy → validated |
| A4/A6 switch triggers | Structured interviews per A4/A6 Validation Protocol above | N=3 per segment | Inferred → validated; **REQUIRED before XP-04 finalization** |
| Actor segment validity | Card-sorting with 5–10 users | N=5 | MEDIUM → HIGH |
| I/S derivation calibration | Apply Decision Matrix to ODI survey results; recalibrate base values | N=20 per category | Proxy math → validated math |
| Re-evaluation trigger | Re-run if 3+ new skills added | Automatic at skill count >=33 | Procedural |

---

*Iter-5: All 9 C3 review blockers closed (1 Critical PM-001/FM-002 STOP GATE + protocol; 8 Major FM-001/FM-003/IN-001/IN-002/PM-002/PM-003/DA-001/FM-002). 4 minor findings also addressed (DA-003 denominator, PM-004 label disclosure, CC-001 criterion justification, IN-003 category-level I clarification). Self-score target: 0.93+.*

*Iter-6: Surgical arithmetic correction (PM-001-iter5). Cat 3, 4, 5 opportunity scores recalculated. Cat 4 corrected from 12 to 15, tying Cat 1. Tier-clustering and L0 ranking updated to reflect corrected scores. See Revision History below.*

## Revision History

### Iter-6 — Arithmetic Correction (2026-04-20)

**Blocker addressed:** PM-001-iter5 — Opportunity score formula I + max(0, I−S) was misapplied for categories 3, 4, and 5.

**Cells corrected (before → after):**

| Location | Cell | Before | After | Verification |
|----------|------|--------|-------|-------------|
| Top 5 table, Cat 3 row | Opp Score | 13 | **14** | I=9, S=4: 9+max(0,9−4)=9+5=14 |
| Top 5 table, Cat 3 row | ±2 Band | 11–15 | **12–16** | 14±2=12–16 |
| Top 5 table, Cat 3 row | Rank | 3 | **3 (tied)** | Ties Cat 2 at 14 |
| Top 5 table, Cat 4 row | Opp Score | 12 | **15** | I=8, S=1: 8+max(0,8−1)=8+7=15 |
| Top 5 table, Cat 4 row | ±2 Band | 10–14 | **13–17** | 15±2=13–17 |
| Top 5 table, Cat 4 row | Rank | 4 | **1 (tied)** | Ties Cat 1 at 15 |
| Top 5 table, Cat 5 row | Opp Score | 11 | **13** | I=8, S=3: 8+max(0,8−3)=8+5=13 |
| Top 5 table, Cat 5 row | ±2 Band | 9–13 | **11–15** | 13±2=11–15 |
| Top 5 table, Cat 5 row | Rank | 5 | **5** | Unchanged position |
| Tier-clustering narrative | Tier A definition | Cat 1+2 | **Cat 1+4 (tied at 15)** | Both Opp=15 |
| Tier-clustering narrative | Tier B definition | Cat 3+4 (overlap) | **Cat 2+3 (tied at 14)** | Both Opp=14 |
| Tier-clustering narrative | Tier C definition | Cat 5 threshold-uncertain | **Cat 5 stable above threshold** | Band 11–15; min=11>10 |
| L2 derivation header, Cat 3 | Opp/Band label | Opp 13 [±2 band 9–15] | **Opp 14 [±2 band 12–16]** | Arithmetic |
| L2 derivation header, Cat 4 | Opp/Band label | Opp 12 [±2 band 8–14] | **Opp 15 [±2 band 13–17]** | Arithmetic |
| L2 derivation header, Cat 5 | Opp/Band label | Opp 11 [±2 band 7–13] | **Opp 13 [±2 band 11–15]** | Arithmetic |
| L2 derivation header, Cat 2 | Band label only | ±2 band 10–16 | **±2 band 12–16** | Pre-existing band arithmetic error; corrected in same pass |
| L0 Executive Summary | Tier ranking statement | Tier A (Cat 1–2) vs Tier B (Cat 3–5) | **Tier A (Cat 1+4 tied at 15) vs Tier B (Cat 2+3 tied at 14) vs Tier C (Cat 5)** | Cascade from score corrections |

**Sections NOT modified:** Job statements (all 30), switch force analysis force ratings and evidence, SKILL.md citations, actor segments, hiring criteria, synthesis judgments, validation required, XP handoff data (except ranking cascade in L0 bullet).

### Iter-7 — Minor Finding Closures (2026-04-20)

**Findings addressed:** LJ-001 (composite carryover resolved by LJ-003+LJ-004 closures), LJ-002, LJ-003, LJ-004 — all Minor, zero structural changes.

| Finding | Addition | Target Location |
|---------|----------|-----------------|
| LJ-002 | Formula self-verification sentence (Ulwick ODI provenance + iter-6 arithmetic confirmation) | Opportunity Score Methodology, after Score interpretation line |
| LJ-003 | STOP GATE owner placeholder replaced with ORCHESTRATION.yaml Phase 1b routing reference | L1 Switch Force Analysis — XP-04 STOP GATE block |
| LJ-004 | Tier-assignment provenance sentence (deterministic from bands; iter-6 verification confirmed) | Top 5 Job Categories — Actionable guidance paragraph |
| LJ-001 | Composite carryover adequately addressed by LJ-003 + LJ-004 closures; no further addition required | N/A |

**Sections NOT modified:** No scores, no tables, no SKILL.md citations, no actor segments, no job statements, no synthesis judgments, no validation required table, no XP handoff data, no force analysis ratings. Navigation table and H-23 compliance unchanged. Self-score target: 0.93 (Methodological Rigor +0.02, Actionability +0.02, Traceability +0.01, Internal Consistency maintained).
