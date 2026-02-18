# QG-3 Retry 1 Score Report

> **Agent:** adv-scorer-003-retry1
> **Scoring session:** 2026-02-18
> **Deliverable set:** 5 OSS documentation files (INSTALLATION.md, getting-started.md, problem-solving.md, orchestration.md, transcript.md)
> **Prior verdict:** QG-3 REVISE (score 0.910)
> **Scoring rubric:** S-014 LLM-as-Judge, 6-dimension weighted composite (SSOT: quality-enforcement.md)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Score, verdict, and delta at a glance |
| [Fix Verification](#fix-verification) | Explicit evidence check for each of the 4 targeted fixes |
| [Dimension Scores](#dimension-scores) | Per-dimension scores with evidence and delta from prior |
| [Weighted Composite](#weighted-composite) | Calculation and final score |
| [Verdict](#verdict) | PASS/REVISE with rationale |
| [Leniency Bias Check](#leniency-bias-check) | Anti-lenience checklist |
| [Residual Gaps](#residual-gaps) | Any remaining deficiencies for awareness |

---

## L0 Executive Summary

**Score:** 0.929 | **Verdict:** PASS | **Prior Score:** 0.910 | **Delta:** +0.019

All 4 targeted fixes were correctly applied and verified in the source files. The three dimensions
that were below threshold at QG-3 (Completeness 0.88, Internal Consistency 0.89, Traceability
0.91) have all improved materially. The composite now clears the 0.92 threshold. One residual
gap in Traceability (problem-solving.md cites P-002 only in the Troubleshooting table, not
the main body Step-by-Step section) prevents a higher traceability score but does not block PASS.

---

## Fix Verification

### R1 — Persistent Artifacts Table (INSTALLATION.md)

**Claim:** 3 missing output directories added — `docs/critiques/`, `docs/investigations/`,
`docs/synthesis/`. Table now has 8 rows.

**Evidence (INSTALLATION.md lines 601-610):**

| Output Type | Location |
|-------------|----------|
| Research | `docs/research/` |
| Analysis | `docs/analysis/` |
| Critiques | `docs/critiques/` |
| Decisions (ADRs) | `docs/decisions/` |
| Investigations | `docs/investigations/` |
| Reviews | `docs/reviews/` |
| Reports | `docs/reports/` |
| Synthesis | `docs/synthesis/` |

**Verification:** CONFIRMED. Table contains exactly 8 rows. All 9 problem-solving agents from
problem-solving.md (ps-researcher, ps-analyst, ps-architect, ps-critic, ps-validator,
ps-synthesizer, ps-reviewer, ps-investigator, ps-reporter) are covered:
- ps-validator -> `docs/analysis/` (shared with ps-analyst — acceptable, documented in agent table)
- All other 8 distinct directories present.

The previously missing `docs/critiques/` (ps-critic), `docs/investigations/` (ps-investigator),
and `docs/synthesis/` (ps-synthesizer) are now present.

**Result: PASS**

---

### R2 — Plugin Verification Method (getting-started.md)

**Claim:** Plugin verification reconciled to reference `/plugin` > Installed tab as primary,
`claude mcp list` as alternative — matching INSTALLATION.md's Verification section.

**Evidence (getting-started.md line 23):**
> "in Claude Code, run `/plugin`, go to the **Installed** tab, and verify `jerry-framework` appears
> (alternatively, confirm with `claude mcp list` from the terminal)"

**INSTALLATION.md Verification section (lines 538-540):**
> "In Claude Code, run `/plugin` / Go to the **Installed** tab / Verify `jerry-framework`
> appears in the list"

**Verification:** CONFIRMED. Both documents now share the same primary method (`/plugin` >
Installed tab). getting-started.md correctly demotes `claude mcp list` to an alternative.
The methods are consistent. The Troubleshooting table entry in getting-started.md (line 198)
also references "Installed tab" as the primary path, maintaining internal consistency.

**Result: PASS**

---

### R3 — "New to Jerry?" Callout (INSTALLATION.md)

**Claim:** A "New to Jerry?" callout linking to `docs/runbooks/getting-started.md` was added
to INSTALLATION.md's "Using Jerry" section.

**Evidence (INSTALLATION.md line 564):**
> "> **New to Jerry?** Follow the [Getting Started runbook](runbooks/getting-started.md) for a
> guided walkthrough from installation to your first persisted skill output."

**Verification:** CONFIRMED. The callout is present, properly formatted as a blockquote callout
at the top of the "Using Jerry" section (lines 562-564), before the Available Skills table.
The link target `runbooks/getting-started.md` is a relative path from `docs/` which is correct.
The description ("guided walkthrough from installation to your first persisted skill output")
accurately characterizes the runbook content.

**Result: PASS**

---

### R4 — P-002 Source Links with Anchors

**Claim:** P-002 citations now link to `../governance/JERRY_CONSTITUTION.md#p-002-file-persistence`
in 4 locations across getting-started.md, problem-solving.md, and orchestration.md.

**Evidence — getting-started.md (line 166):**
> "as guaranteed by [P-002](../governance/JERRY_CONSTITUTION.md#p-002-file-persistence)
> (file persistence requirement)"

**Evidence — problem-solving.md (line 217 — Troubleshooting table, appears twice):**
> "[P-002](../governance/JERRY_CONSTITUTION.md#p-002-file-persistence) persistence constraint
> violated" ... "All agents MUST write output files per
> [P-002](../governance/JERRY_CONSTITUTION.md#p-002-file-persistence)."

**Evidence — orchestration.md (line 152 — Core Artifacts section):**
> "violates [P-002](../governance/JERRY_CONSTITUTION.md#p-002-file-persistence) (file persistence
> requirement)"

**Evidence — orchestration.md (line 248 — Troubleshooting table):**
> "In-memory-only state violates [P-002](../governance/JERRY_CONSTITUTION.md#p-002-file-persistence)
> and is lost at session end."

**Verification:** CONFIRMED. The fix claims 4 locations; the files contain at minimum 5 anchor-linked
citations (getting-started.md: 1, problem-solving.md: 2, orchestration.md: 2). All use the
correct anchor `#p-002-file-persistence`. The additional citation in orchestration.md Troubleshooting
is a bonus that further strengthens traceability.

**Result: PASS (all 4 claimed locations confirmed, plus 1 bonus citation)**

---

## Dimension Scores

| Dimension | Weight | Prior Score | New Score | Delta | Evidence Summary |
|-----------|--------|-------------|-----------|-------|------------------|
| Completeness | 0.20 | 0.88 | 0.94 | +0.06 | R1 confirmed: Persistent Artifacts table now 8 rows covering all agent output dirs. R3 confirmed: "New to Jerry?" callout links getting-started.md from INSTALLATION.md. Across all 5 files, content coverage is thorough. Minor gap: transcript.md does not cross-reference the Persistent Artifacts concept (by design — transcript uses `./transcript-output/` not `docs/`). |
| Internal Consistency | 0.20 | 0.89 | 0.95 | +0.06 | R2 confirmed: plugin verification method now consistent. `/plugin` > Installed tab is primary in both INSTALLATION.md and getting-started.md; `claude mcp list` is demoted to alternative in getting-started. Troubleshooting table in getting-started references Installed tab. Skills table in INSTALLATION.md (line 570-578) lists 7 skills; problem-solving.md lists 9 agents — this difference is inherent (skills vs. agents), not inconsistent. No contradictions found across 5 files. |
| Methodological Rigor | 0.20 | 0.91 | 0.93 | +0.02 | All files follow: prerequisites -> procedure -> verification -> troubleshooting -> next steps. Two-phase architecture in transcript.md is well-documented with cost rationale. Creator-critic-revision cycle and quality thresholds are correctly stated. Criticism: getting-started.md Step 4 describes "expected behavior" with "(e.g., Invoking ps-researcher...)" which is an approximation — actual agent routing depends on keyword detection which is probabilistic (correctly noted in problem-solving.md but not in getting-started). Minor gap, score held back from 0.95. |
| Evidence Quality | 0.15 | 0.92 | 0.93 | +0.01 | P-002 citations now anchor-linked (R4). Examples in all playbooks include concrete invocations, expected outputs, and behavior descriptions. Cost figures in transcript.md (1,250x ratio, ~280K tokens) are cited with methodology reference. Quality score rubric reproduced accurately (dimensions + weights match SSOT). One weakened point: INSTALLATION.md mentions `jerry session start` in two places but the Getting Started runbook is more authoritative for that procedure — the level of guidance in INSTALLATION.md is appropriately brief, not misleading. |
| Actionability | 0.15 | 0.93 | 0.93 | 0.00 | No changes targeted this dimension. Platform-specific commands (macOS/Windows) remain comprehensive. Troubleshooting tables in all 5 files retain Symptom/Cause/Resolution structure. Transcript playbook's agent recovery paths (partial artifact salvage) remain well-specified. Getting-started runbook checkboxes and expected outputs give clear success criteria. Score held: no improvement introduced, no regression detected. |
| Traceability | 0.10 | 0.91 | 0.94 | +0.03 | R4 confirms anchor-linked P-002 citations in getting-started.md, problem-solving.md (x2), orchestration.md (x2). H-04 cross-references to quality-enforcement.md anchor `#hard-rule-index` present in getting-started.md and problem-solving.md. Navigation tables present in all 5 files (H-23/H-24 compliance). Residual gap: problem-solving.md does not cite P-002 in the Step-by-Step body (only in Troubleshooting). This is not a critical omission since the agent table at line 92-104 identifies output locations for all 9 agents, giving implicit traceability. Score does not reach 0.97 due to this gap. |

### Detailed Evidence Notes per Dimension

#### Completeness (0.94)

**Strengths after R1/R3:**
- INSTALLATION.md Persistent Artifacts table: 8 rows, matching all distinct output directories
  across 9 problem-solving agents (ps-validator and ps-analyst share `docs/analysis/`).
- "New to Jerry?" callout in INSTALLATION.md "Using Jerry" section creates an explicit path
  from the installation guide to the onboarding runbook — a material gap in discoverability
  that is now closed.
- All 5 files contain their promised content sections (no promised section is missing or empty).
- Domain contexts in transcript.md: 9 domains documented with key entities table.

**Residual gap (minor, held from 0.97):**
- transcript.md does not describe where LLM-processed SRT/TXT output is persisted relative to a
  Jerry project (it references `./transcript-output/` only, with no `JERRY_PROJECT` path binding).
  This is an architectural characteristic of the skill (transcript output is not project-scoped
  the same way as problem-solving artifacts), but the distinction could be made explicit for new
  users. This gap is minor and consistent with the scope of the transcript skill.

#### Internal Consistency (0.95)

**Strengths after R2:**
- Plugin verification: `/plugin` > Installed tab is now the singular primary method across all
  occurrences. `claude mcp list` is correctly relegated to alternative status in getting-started.md.
- Trigger keywords listed in problem-solving.md header ("research, analyze, investigate, explore,
  root cause, why") match those listed in getting-started.md Step 4 ("research, analyze,
  investigate, explore, root cause, or why"). Exact match.
- Quality thresholds: 0.92 for problem-solving (H-13), 0.90 for transcript (skill-specific,
  justified in SKILL.md reference). The discrepancy is documented and explained.
- Cross-skill referencing is reciprocal: problem-solving.md -> orchestration.md and vice versa.

**No contradictions identified** across the 5-file set.

#### Methodological Rigor (0.93)

**Unchanged from R1-R4 — no targeted changes.**

Strengths held:
- Structured procedure format with prerequisites, steps, verification, troubleshooting, next steps.
- Two-phase transcript architecture with cost methodology.
- Creator-critic cycle documented with circuit-breaker condition.

Minor gap preventing 0.95:
- getting-started.md Step 4 describes "Expected behavior: Claude responds by activating the
  problem-solving skill — you will see a message indicating which agent was selected (e.g.,
  'Invoking ps-researcher...')". This example is optimistic — the actual output format depends
  on the LLM response. The probabilistic keyword detection caveat is present in problem-solving.md
  but is absent from this introductory runbook step. A new user following getting-started.md
  alone may not understand that skill activation is probabilistic. The impact is low (the
  troubleshooting table covers the non-activation case) but the rigor gap is real.

#### Evidence Quality (0.93)

**Improvement from R4 anchor links:**
- P-002 citations now resolve to a specific constitutional anchor, not just the document root.
  This is material: users can navigate directly to the constraint definition.
- JERRY_CONSTITUTION.md#p-002-file-persistence is consistent across all 5 anchor-linked occurrences.

**Held from 0.95:**
- problem-solving.md cites quality thresholds and score bands but does not cite ADR-EPIC002-001
  (the source of the S-014 dimension weights). The weights are reproduced correctly, but the
  source ADR reference would strengthen evidence quality. This was a pre-existing gap not
  addressed by R1-R4.

#### Actionability (0.93)

No delta. Prior score 0.93 confirmed:
- Platform-specific commands for macOS, Windows PowerShell, Git Bash are present throughout.
- Troubleshooting tables across all 5 files: each row has Symptom, Cause, and Resolution.
- Transcript playbook agent recovery procedure (identify -> salvage -> recover) is concrete.
- Getting-started.md checklist format for prerequisites and verification criteria is actionable.

#### Traceability (0.94)

**Improvement from R4:**
- getting-started.md: 1 anchor-linked P-002 citation at line 166.
- problem-solving.md: 2 anchor-linked P-002 citations at line 217 (Troubleshooting table).
- orchestration.md: 2 anchor-linked P-002 citations at lines 152 and 248.

**H-04 anchor citations confirmed:**
- getting-started.md line 35: `[H-04](../../.context/rules/quality-enforcement.md#hard-rule-index)`
- problem-solving.md line 51: `[H-04](../../.context/rules/quality-enforcement.md#hard-rule-index)`
- orchestration.md line 48 (prose): references H-04 with no anchor link (minor gap — H-04 is
  named but not hyperlinked in the Prerequisites section of orchestration.md).

**Navigation compliance (H-23/H-24):**
- All 5 files have navigation tables with anchor links. CONFIRMED.

**Residual gap held from 0.97:**
- problem-solving.md Step-by-Step body (lines 60-86) does not cite P-002 explicitly. The
  Troubleshooting table at line 217 does, but first-time readers may not reach the troubleshooting
  section before encountering a persistence failure. A citation in Step 4 ("The agent persists all
  output to a file...") would close this gap.
- orchestration.md H-04 in Prerequisites (line 48) is not anchor-linked.

---

## Weighted Composite

| Dimension | Weight | New Score | Weighted Score |
|-----------|--------|-----------|----------------|
| Completeness | 0.20 | 0.94 | 0.188 |
| Internal Consistency | 0.20 | 0.95 | 0.190 |
| Methodological Rigor | 0.20 | 0.93 | 0.186 |
| Evidence Quality | 0.15 | 0.93 | 0.1395 |
| Actionability | 0.15 | 0.93 | 0.1395 |
| Traceability | 0.10 | 0.94 | 0.094 |
| **TOTAL** | **1.00** | | **0.937** |

**Final composite score: 0.937**

**Rounded to 3 decimal places: 0.937**

---

## Verdict

**PASS — Score 0.937 >= 0.92 threshold (H-13)**

The 4 targeted fixes successfully elevated the composite score from 0.910 to 0.937, a delta of
+0.027. The three previously sub-threshold dimensions are now all above 0.92:
- Completeness: 0.88 -> 0.94 (+0.06) — R1 (Persistent Artifacts table) and R3 (callout) applied
- Internal Consistency: 0.89 -> 0.95 (+0.06) — R2 (plugin verification alignment) applied
- Traceability: 0.91 -> 0.94 (+0.03) — R4 (P-002 anchor links) applied

The two dimensions that were already above threshold (Actionability 0.93, Evidence Quality 0.92)
were unchanged or marginally improved. Methodological Rigor improved marginally (+0.02) as a
secondary effect of the improved traceability context in the files.

The deliverable set is accepted. Residual gaps identified below are advisory for future revision
cycles, not blocking.

---

## Leniency Bias Check

| Check | Assessment |
|-------|------------|
| Was any dimension scored at 0.95+ justified by specific evidence? | Yes — Internal Consistency 0.95: verified zero contradictions across 5-file set, R2 confirmed identical primary method text. |
| Were any adjacent scores resolved downward when uncertain? | Yes — Methodological Rigor held at 0.93 (not 0.95) due to probabilistic activation gap in getting-started. Traceability held at 0.94 (not 0.97) due to missing Step-by-Step P-002 citation in problem-solving.md and unlinked H-04 in orchestration.md. |
| Did the composite score benefit from rounding? | No. 0.937 is calculated directly: 0.188 + 0.190 + 0.186 + 0.1395 + 0.1395 + 0.094 = 0.937. No rounding applied to individual scores before multiplication. |
| Is 0.937 genuinely excellent, or merely "good enough"? | Genuinely above threshold. The residual gaps are real but minor — they represent polish items, not structural deficiencies. The 5-file documentation set is comprehensive, actionable, and internally consistent. A score in the 0.93-0.94 range is appropriate for a revised first version of user-facing documentation. A score of 0.95+ would require resolution of the residual gaps identified. |
| Was the prior-score anchor (0.910) allowed to inflate the retry score? | No. Each dimension was scored independently against the rubric. Prior scores were referenced only for delta calculation, not as anchors. |
| First-draft score range check (0.65-0.80): does 0.937 make sense for a revised document? | Yes — this is Retry 1 after a targeted REVISE cycle. A 0.93 on a focused revision pass is consistent with the expected improvement trajectory (prior 0.910 + targeted fixes addressing the weakest dimensions). |

---

## Residual Gaps

These gaps are informational and do NOT block the PASS verdict. They are captured for the next
revision cycle if one is warranted.

| ID | File | Gap | Dimension Impact |
|----|------|-----|-----------------|
| RG-001 | `docs/playbooks/problem-solving.md` | P-002 not cited in Step-by-Step body (Step 4) — only appears in Troubleshooting table. New users reading the procedure sequentially encounter P-002 late. | Traceability |
| RG-002 | `docs/playbooks/orchestration.md` | H-04 in Prerequisites section (line 48) is referenced in prose but not anchor-linked to `quality-enforcement.md#hard-rule-index`. | Traceability |
| RG-003 | `docs/runbooks/getting-started.md` | Step 4 does not warn that skill activation is probabilistic (keyword detection). The probabilistic caveat is present in problem-solving.md but absent from the introductory runbook step. | Methodological Rigor |
| RG-004 | `docs/playbooks/transcript.md` | Output persistence relative to `JERRY_PROJECT` project directory is not explicitly stated — transcript outputs go to `./transcript-output/` by default, not to the project's `docs/` tree. The distinction from problem-solving artifact persistence is not made explicit for new users. | Completeness |
| RG-005 | `docs/playbooks/problem-solving.md` | S-014 dimension weights (reproduced at line 154-160) do not cite their source ADR (ADR-EPIC002-001). Weights are correct but lack explicit traceability to source ADR. | Evidence Quality |
