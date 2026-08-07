# Steelman Report: /nuclear-sop Skill (PR #269)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Steelman Context](#steelman-context) | Strategy metadata and scope |
| [Path Notation](#path-notation) | CI path-hygiene substitution rule applied to quoted paths |
| [Summary](#summary) | Assessment, improvement count, recommendation |
| [Step 1: Deep Understanding](#step-1-deep-understanding) | Charitable interpretation of the deliverable's core thesis |
| [Step 2: Weakness Classification](#step-2-weakness-classification) | Presentation/structural/evidence weaknesses found |
| [Step 3: Steelman Reconstruction](#step-3-steelman-reconstruction) | Key excerpts rewritten in strongest form, inline-annotated |
| [Step 4: Best Case Scenario](#step-4-best-case-scenario) | Ideal conditions, assumptions, confidence assessment |
| [Step 5: Improvement Findings](#step-5-improvement-findings) | Findings table and expanded details |
| [Step 6: Present the Steelman](#step-6-present-the-steelman) | Self-review and readiness for downstream critique |
| [Scoring Impact](#scoring-impact) | Effect of improvements on the 6 quality dimensions |
| [Execution Statistics](#execution-statistics) | Protocol completion and finding counts |
| [Strategy Verdict](#strategy-verdict) | One-paragraph summary judgment |

---

## Steelman Context

- **Deliverable:** `/nuclear-sop` skill (31 files, ~8.5k lines) + 5 registration surfaces (`.claude-plugin/plugin.json`, `CLAUDE.md`, `AGENTS.md`, `.context/rules/mandatory-skill-usage.md`, `CHANGELOG.md`), PR #269, branch `proj-0039-nuclear-engineer`, head commit `bda64202`
- **Deliverable Type:** Other — Agent Skill (4 agent `.md` + `.governance.yaml` pairs, 4 `composition/` canonical-format pairs, templates, Diataxis docs, behavioral-baseline QA artifacts, worked example with embedded test traps)
- **Criticality Level:** C4 (Critical — full tournament, all 10 strategies)
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Template:** `.context/templates/adversarial/s-003-steelman.md` v1.0.0
- **Steelman By:** adv-executor (worker agent) | **Date:** 2026-08-07T00:00:00Z (execution_id: `20260807T1200`) | **Original Author:** PR #269 contributor (identity not disclosed in reviewed files)
- **Blindness:** This execution ran without reading any prior review output (S-001/S-002/S-004/S-007/S-010/S-011/S-012/S-013/S-014 or PROJ-032 work products). All findings below are independently derived from the 36 reviewed files plus the current `.context/rules/` and `docs/governance/JERRY_CONSTITUTION.md` trees.

---

## Path Notation

Per the reviewing orchestrator's path-hygiene instruction, the literal string `projects/PROJ-` followed by a 3–4 digit ID other than `032` is forbidden in this report (CI rejects it). The deliverable's own files repeatedly cite evidence paths under the PR's own project tree using that exact pattern (`«PR projects tree»/PROJ-0039-nuclear-engineer/...`). Wherever this report quotes such a path, `«PR projects tree»/PROJ-0039-nuclear-engineer` has been mechanically replaced with the placeholder **`«PR projects tree»/PROJ-0039-nuclear-engineer`**. This is a structural substitution only — no other characters in the quoted path or surrounding text have been altered. This note exists so the substitution is transparent (P-022) rather than silently changing quoted evidence.

---

## Summary

**Steelman Assessment:** A well-researched, unusually candid transplant of nuclear-industry procedural discipline (pre-job briefing, STAR self-checking, place-keeping, hold points, independent verification, post-job OE capture) into Jerry's C2+ agent workflows, correctly built on top of existing Jerry mechanisms (P-003 single-level nesting, `/adversary` S-014 for QG-HOLD, Task-tool fresh-context isolation for IV-HOLD) rather than duplicating them — undermined in its current form by a cluster of mechanical (not architectural) consistency and freshness defects concentrated in exactly the mechanism the skill advertises as its headline differentiator.

**Improvement Count:** 2 Critical, 4 Major, 2 Minor (8 total)

**Original Strength:** Strong. The core methodology mapping is well-cited (5 named INPO/NRC source documents with revision numbers), the constitutional-compliance mapping is concrete rather than assertive (per-agent P-003/P-020/P-022/P-002 mechanisms, not just labels), and the skill ships an actual empirical validation fixture (3 ATT&CK-mapped STAR traps in the C3 worked example, claimed 3/3 catch rate) rather than a hypothetical illustration. All numeric thresholds that must match the current SSOT do match it exactly (H-13 0.92 threshold; RT-M-010 iteration ceilings C1=3/C2=5/C3=7/C4=10; step limits C1-C2=20/C3=15/C4=10) across every file that restates them.

**Recommendation:** Incorporate improvements. All 8 findings are same-file-family, low-risk, mechanically fixable edits — none require redesigning STAR, the hold-point model, the agent topology, or the OE schema. Two of the eight (S-003-01, S-003-02) sit directly on the mandatory OE-review loop and the H-36 governance self-monitoring mechanism and should be resolved before S-001/S-002/S-004/S-007 evaluate this artifact, so that downstream critique attacks the design rather than avoidable editorial defects.

---

## Step 1: Deep Understanding

**Core thesis:** Jerry's C2+ agent workflows lack formalized pre-execution context-loading and post-execution lessons-capture as first-class procedural steps — "the highest-value gap this skill addresses," per the skill's own framing (`skills/nuclear-sop/SKILL.md` § What the Skill Closes). Fifty years of nuclear power plant operating discipline (INPO AP-907 Rev.3, INPO 09-003 Rev.1, INPO 06-003, 10 CFR 50 Appendix B, NUREG-1792) already solved an analogous problem — ensuring a capable operator executes a high-stakes procedure reliably, catches its own errors, and converts every execution into institutional knowledge — and `/nuclear-sop` imports that framework as four cooperating worker agents (`sop-brief`, `sop-executor`, `sop-verifier`, `sop-capture`) that never violate the existing P-003 single-level-nesting constraint.

**Key claims, each independently well-supported in the reviewed files:**
1. Pre-job briefing (F-2a), prerequisite verification (D-1), and OE history review (H-2) can be made mandatory, sequential, and non-bypassable (`sop-brief` Step 1 is "MANDATORY for every `/nuclear-sop` invocation," NS-H-07).
2. STAR self-checking (B-1) is explicitly disclosed as a *behavioral* prompt-level constraint, not a physical interruption — `sop-executor.md` states plainly: "Both STAR reasoning and the tool call are generated in the same inference pass. The temporal separation is a structural constraint in the prompt, not a physical interruption as in nuclear plant operations." This is a stronger P-022 disclosure than most Jerry skill documentation offers, and it is backed by an actual A/B validation event (QG-E4, 3 deliberate traps, claimed 3/3 catch rate) rather than an unfalsifiable assertion.
3. Independent verification (C-2) is honestly labeled as *approximated*, not equivalent to personnel independence — `sop-verifier.md`'s own "Anchoring Bias Disclaimer" and the 3-hop mode's "ANCHORING BIAS DISCLAIMER" in `sop-capture.md` both state the limitation in the artifact itself, not only in a separate risk register.
4. The skill correctly declines to reinvent existing Jerry infrastructure: QG-HOLD calls `/adversary` S-014 rather than embedding its own scorer; IV-HOLD reuses the Task-tool fresh-context pattern that FC-M-001 already formalizes in `agent-development-standards.md`; `/orchestration` is explicitly deferred to for multi-procedure coordination.
5. All step-limit and iteration-ceiling numbers that must trace to the current SSOT (H-13's 0.92, RT-M-010's C1=3/C2=5/C3=7/C4=10) are reproduced identically everywhere they appear across 8+ files, with no drift.

**Strengthening opportunities identified (all in expression/structure, not in the underlying idea — see Step 2):** intra-file and cross-file consistency of the OE-entry file extension, the H-36 governance-deadline anchor event, the registration-content freshness narrative, navigation-table section coverage, and two registry-file completeness gaps.

**Decision Point:** The deliverable has a clear, discernible, well-evidenced thesis. Proceeding to Step 2.

---

## Step 2: Weakness Classification

| # | Weakness | Type | Magnitude |
|---|----------|------|-----------|
| 1 | OE entry file extension (`.yaml` vs. `.md`) disagrees across 3 of 8 files that specify it, against a Glob pattern that only matches one extension | Structural | Critical |
| 2 | H-36 governance-deadline anchor event differs across files (Phase 1 delivery vs. skill registration); no machine-checkable staleness signal; deadline date appears to have elapsed as of this review | Structural | Critical |
| 3 | `SKILL.md` "Registration Content" section still narrates DEFERRED status and stale copy-paste text after registration was actually (and better) applied | Presentation / Structural | Major |
| 4 | Navigation tables in `SKILL.md`, `PLAYBOOK.md`, `AGENTS.md`, and `docs/reference.md` each omit at least one existing `##`/`#` section (NAV-004 coverage) | Presentation | Major |
| 5 | `AGENTS.md` Agent Summary table/count not updated for the 4 new `sop-*` agents this PR adds | Structural | Major |
| 6 | `AGENTS.md` MCP "Not included (by design)" note omits `sop-*` despite fitting the same file-based-persistence exclusion pattern already documented for `wt-*`/`eng-*`/`red-*` | Evidence / Presentation | Major |
| 7 | `SKILL.md` "STAR Validation Pre-Ship Gate" heading retains pre-ship framing after the gate PASSED | Presentation | Minor |
| 8 | Nuclear Industry Source References table is not cross-linked to the internal Phase 1 Research Survey artifact that performed the actual pattern extraction | Evidence | Minor |

All eight are weaknesses in **expression, structure, or freshness** — none require changing the core thesis (nuclear SOP discipline transplanted into Jerry agent execution) or the agent topology. Per Step 2's decision rule, execution proceeds to reconstruction.

---

## Step 3: Steelman Reconstruction

Given the deliverable's size (36 files, ~8.5k lines), reconstruction is shown as **key excerpts** rewritten in strongest form with inline `[S-003-0N]` annotations, consistent with the template's own worked-example precedent ("Reconstruction (key sections shown)").

### 3.1 `skills/nuclear-sop/templates/POST_JOB_BRIEF.template.md` — OE entry paths

**Original:**
```markdown
**Local capture path:** `capture/oe-entry-{entry_id}.md`

**Persistent path (future sop-brief retrieval):** `docs/experience/{entry_id}.md`
```

**Strengthened [S-003-01]:**
```markdown
**Local capture path:** `capture/oe-entry-{entry_id}.yaml`

**Persistent path (future sop-brief retrieval):** `docs/experience/{entry_id}.yaml`

<!-- [S-003-01] Extension aligned to .yaml to match sop-capture.md Step 3, nuclear-sop-behavior-rules.md
     OE Entry Schema, docs/reference.md, docs/tutorial-getting-started.md, and the sop-brief.md /
     nuclear-sop-behavior-rules.md OE Search Mechanism, which Globs "docs/experience/*.yaml" only. -->
```

### 3.2 `skills/nuclear-sop/behavioral-baselines/bb-003-oe-feedback-loop-integrity.md` — B-21

**Original:**
```markdown
**B-21: OE entry written to BOTH locations**

After field validation, Write must be called twice:
1. `capture/oe-entry-{entry_id}.md` -- local capture directory
2. `docs/experience/{entry_id}.md` -- persistent OE registry
```

**Strengthened [S-003-01]:**
```markdown
**B-21: OE entry written to BOTH locations, with the schema's mandated extension**

After field validation, Write must be called twice:
1. `capture/oe-entry-{entry_id}.yaml` -- local capture directory
2. `docs/experience/{entry_id}.yaml` -- persistent OE registry

**B-21a (new): Extension conformance check.** A conforming OE write MUST use `.yaml` at both
locations. A `.md`-suffixed write at either location is itself a drift signal for this baseline
(add to Drift Detection Signals: "OE entry written with `.md` extension instead of schema-mandated
`.yaml` — sop-brief's Glob(`docs/experience/*.yaml`) will silently return zero matches for this
entry, defeating H-2 OE review for all future executions of this workflow_id").
```

### 3.3 `skills/nuclear-sop/examples/c3-adr-workflow-definition.md` — AC-7 and Section 11

**Original:**
```markdown
| AC-7 | OE entry written to docs/experience/ | `Glob: docs/experience/adr-authoring-c3-001-*.md` | At least one matching OE entry exists |
...
| OE Entry Reference | `adr-authoring-c3-001-{YYYYMMDD}-001` | Reference to `docs/experience/adr-authoring-c3-001-{YYYYMMDD}-001.md` |
```

**Strengthened [S-003-01]:**
```markdown
| AC-7 | OE entry written to docs/experience/ | `Glob: docs/experience/adr-authoring-c3-001-*.yaml` | At least one matching OE entry exists |
...
| OE Entry Reference | `adr-authoring-c3-001-{YYYYMMDD}-001` | Reference to `docs/experience/adr-authoring-c3-001-{YYYYMMDD}-001.yaml` |
```

### 3.4 `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` — NS-H-08 governance deadline

**Original:**
```markdown
| NS-H-08 | C3+ workflows MUST use 4-hop mode ... **GOVERNANCE DEADLINE:** H-36 governance ruling
tracked as worktracker entity `TASK-0039-H36-RULING` with deadline 60 days from skill registration
(2026-06-15). If the ruling eliminates sop-verifier, NS-H-08 is superseded and MUST be revised.
Until that revision is completed, NS-H-08 remains as written. |
```

**Strengthened [S-003-02]:**
```markdown
| NS-H-08 | C3+ workflows MUST use 4-hop mode ... **GOVERNANCE DEADLINE:** H-36 governance ruling
tracked as worktracker entity `TASK-0039-H36-RULING`
(`«PR projects tree»/PROJ-0039-nuclear-engineer/work/TASK-0039-H36-RULING.md`) with deadline
60 days from skill registration (2026-06-15) — the same anchor event and date used in
`SKILL.md` § H-36 Circuit Breaker Compliance and `PLAYBOOK.md` § L2: Architecture and Standards.
**Status field (REQUIRED, machine-checkable):** `governance_ruling_status: PENDING | RESOLVED-4HOP | RESOLVED-3HOP`,
last checked `{ISO-8601}`. If `governance_ruling_status: PENDING` AND current date > deadline date,
this rule is STALE and the reviewing agent/user MUST re-confirm the mode before trusting "MUST use
4-hop" as current guidance, rather than computing elapsed time manually from prose. |
```

### 3.5 `skills/nuclear-sop/SKILL.md` — Governance Ruling Pending anchor event

**Original:**
```markdown
**Governance ruling deadline:** If no H-36 ruling is received within 60 days of Phase 1 delivery,
the default behavior is 3-hop mode for all criticality levels.
```

**Strengthened [S-003-02]:**
```markdown
**Governance ruling deadline:** If no H-36 ruling is received by 2026-06-15 (60 days from skill
registration — the identical anchor event and date used in `nuclear-sop-behavior-rules.md` NS-H-08;
"Phase 1 delivery" is retired as a second, non-synchronized anchor), the default behavior is
3-hop mode for all criticality levels. See NS-H-08 `governance_ruling_status` for the current,
machine-checkable resolution state before relying on this section.
```

### 3.6 `skills/nuclear-sop/SKILL.md` — Registration Content

**Original:**
```markdown
> **DEFERRED REGISTRATION NOTE:** These entries are applied to the live files (`CLAUDE.md`,
`AGENTS.md`, `.context/rules/mandatory-skill-usage.md`) AFTER QG-E6 final review gate PASS.
... The skill is NOT registered and NOT live-routable until QG-E6 passes and the user applies
these entries.
```
followed by a `mandatory-skill-usage.md` row with Priority `12` and a shorter negative-keyword/compound-trigger list than what was actually applied.

**Strengthened [S-003-03]:**
```markdown
> **REGISTRATION STATUS: APPLIED.** QG-E6 passed and the user applied the entries below to
`CLAUDE.md`, `AGENTS.md`, and `.context/rules/mandatory-skill-usage.md` on {date}. The
`mandatory-skill-usage.md` row shown here is the row AS ACTUALLY APPLIED (Priority 16, expanded
negative-keyword and compound-trigger disambiguation against `/problem-solving`, `/nasa-se`, and
`/eng-team` collisions) — kept in sync so this section remains a correct reference copy rather than
a stale draft.
```
with the copy-paste block updated to Priority `16` and the applied negative-keyword/compound-trigger list, matching what is now live in `.context/rules/mandatory-skill-usage.md`.

### 3.7 `AGENTS.md` — Document Sections nav table and Agent Summary

**Original (Document Sections, excerpt):**
```markdown
| [NASA SE Skill Agents](#nasa-se-skill-agents) | nse-* agents (10 total) |
| [Orchestration Skill Agents](#orchestration-skill-agents) | orch-* agents (3 total) |
```

**Strengthened [S-003-04]:**
```markdown
| [NASA SE Skill Agents](#nasa-se-skill-agents) | nse-* agents (10 total) |
| [Nuclear SOP Skill Agents](#nuclear-sop-skill-agents) | sop-* agents (4 total) |
| [Orchestration Skill Agents](#orchestration-skill-agents) | orch-* agents (3 total) |
```

**Original (Agent Summary, excerpt):**
```markdown
| NASA SE Agents | 10 | `/nasa-se` skill |
| Orchestration Agents | 3 | `/orchestration` skill |
...
| **Total** | **89** | |
```

**Strengthened [S-003-05]:**
```markdown
| NASA SE Agents | 10 | `/nasa-se` skill |
| Nuclear SOP Agents | 4 | `/nuclear-sop` skill |
| Orchestration Agents | 3 | `/orchestration` skill |
...
| **Total** | **93** | |
```
(Per-skill sum re-verified: 9+10+**4**+3+3+3+5+3+1+10+11+5+6+3+11+2+2+2 = 93.)

### 3.8 `AGENTS.md` — MCP "Not included (by design)" note

**Original:**
```markdown
> **Not included (by design):** adv-* (self-contained strategy execution), sb-* (voice quality gate),
wt-* (read-only auditing), ps-critic/ps-validator (quality evaluation), ps-reporter (report
generation). eng-*/red-* agents do not use Memory-Keeper; their persistence model uses file-based
output per P-002 (engagement-scoped output directories), not cross-session MCP storage.
```

**Strengthened [S-003-08]:**
```markdown
> **Not included (by design):** adv-* (self-contained strategy execution), sb-* (voice quality
gate), wt-* (read-only auditing), ps-critic/ps-validator (quality evaluation), ps-reporter (report
generation), sop-* (nuclear-sop's persistence model is file-based — `PROCEDURE_STATE.yaml`,
`HOLD_POINT_LOG.md`, and dual-write OE entries under `docs/experience/` — matching the T1/T2 tier
scope of the other file-based-output agents in this list; no MCP tool is required). eng-*/red-*
agents do not use Memory-Keeper; their persistence model uses file-based output per P-002
(engagement-scoped output directories), not cross-session MCP storage.
```

### 3.9 `SKILL.md` — Pre-Ship Gate heading

**Original:** `### STAR Validation Pre-Ship Gate`

**Strengthened [S-003-06]:** `### STAR Validation Gate (QG-E4) — Result: PASSED`

### 3.10 `SKILL.md` — Nuclear Industry Source References

**Original (table footer, no cross-link to the internal survey artifact).**

**Strengthened [S-003-07]:** add one row beneath the citation table:
```markdown
**Internal synthesis:** These five sources were surveyed and mapped to Jerry nuclear-pattern IDs
(F-2a, D-1, H-2, B-1, A-5, A-2, A-4, D-2, C-3, C-2, F-2b, H-1) in the Phase 1 Research Survey —
`«PR projects tree»/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-build-20260325-001/eng/phase-1/`
— which is the traceable source for `WORKFLOW_DEFINITION.template.md`'s A-3 structure citation.
```

**Decision Point:** All eight improvements are Minor-to-Critical *filling of gaps*, not substance changes; none alter the core thesis. Proceeding to Step 4.

---

## Step 4: Best Case Scenario

**Ideal conditions under which this deliverable is strongest:** (1) Teams already running C2+ Jerry workflows with genuinely irreversible or hard-to-reverse steps (ADR placement, security-architecture decisions, agent-definition changes) where mandatory pre-briefing + STAR + hold points + OE capture measurably reduces repeat errors; (2) sufficient context-window budget across the 4-agent chain (`opus` for `sop-executor`, `sonnet` for the other three) that AE-006c context exhaustion does not truncate STAR compliance mid-execution; (3) sustained reuse over many executions, since the OE accumulation thresholds (WARNING >10, STOP >20) and the synthesis recommendation only pay off once a real corpus exists; (4) the H-36 hop-count governance question resolved in either direction, so C3+'s 4-hop requirement has an unambiguous, current status rather than a deadline that must be manually checked against wall-clock time.

**Key supporting assumptions that must hold:** STAR's behavioral (not deterministic) nature is an acceptable trade-off given explicit disclosure plus an empirical baseline (3/3 traps caught) rather than an unfalsifiable claim; the skill's own C1-exclusion ("NEVER invoke this skill when task is C1 routine work... overhead is disproportionate") correctly scopes the procedural overhead to work that warrants it; QG-HOLD and IV-HOLD correctly delegate to `/adversary` and the existing Task-tool isolation pattern rather than inventing parallel infrastructure.

**Confidence assessment:** **HIGH** that the core methodology transplant is sound, given five specifically-cited INPO/NRC sources (with revision numbers), a concrete per-agent constitutional-compliance mapping, and a genuine test fixture (not just a hypothetical) validating the highest-risk behavioral claim. **MODERATE-TO-HIGH** on the operational mechanics as currently written, pending resolution of the two Critical findings (S-003-01, S-003-02): the OE-loop extension defect could silently zero out the exact mechanism (`H-2` mandatory OE review) the skill calls out as its own key capability, and the governance-deadline defect means a reader cannot currently tell, from the shipped files alone, whether the "C3+ MUST use 4-hop mode" clause is still current policy or has already lapsed per its own stated fallback.

---

## Step 5: Improvement Findings

### Findings Summary / Improvement Findings Table

| ID | Template ID | Severity | Description | Dimension | File(s) |
|----|-------------|----------|--------------|-----------|---------|
| S-003-01 | SM-001-20260807T1200 | Critical | OE entry file extension (`.yaml` vs `.md`) disagrees across 3 files against a `.yaml`-only Glob retrieval pattern | Internal Consistency | `templates/POST_JOB_BRIEF.template.md`, `behavioral-baselines/bb-003-oe-feedback-loop-integrity.md`, `examples/c3-adr-workflow-definition.md` |
| S-003-02 | SM-002-20260807T1200 | Critical | H-36 governance-deadline anchor event differs across files; no machine-checkable staleness signal; deadline date appears elapsed as of this review | Internal Consistency / Traceability | `SKILL.md`, `PLAYBOOK.md`, `rules/nuclear-sop-behavior-rules.md` (NS-H-08) |
| S-003-03 | SM-003-20260807T1200 | Major | "Registration Content" narrates DEFERRED status and stale copy-paste text after registration was actually (and better) applied | Internal Consistency / Traceability | `SKILL.md` § Registration Content vs. `CLAUDE.md`, `AGENTS.md`, `.context/rules/mandatory-skill-usage.md`, `.claude-plugin/plugin.json` |
| S-003-04 | SM-004-20260807T1200 | Major | Navigation tables omit existing sections (NAV-004) in 4 files | Completeness | `SKILL.md`, `PLAYBOOK.md`, `AGENTS.md`, `docs/reference.md` |
| S-003-05 | SM-005-20260807T1200 | Major | Agent Summary table/count not updated for the 4 new `sop-*` agents | Internal Consistency | `AGENTS.md` |
| S-003-06 | SM-008-20260807T1200 | Major | MCP "Not included (by design)" note omits `sop-*` | Completeness | `AGENTS.md` |
| S-003-07 | SM-006-20260807T1200 | Minor | "Pre-Ship Gate" heading retains pre-ship framing after the gate PASSED | Actionability | `SKILL.md` |
| S-003-08 | SM-007-20260807T1200 | Minor | Source citations not cross-linked to the internal Phase 1 Research Survey artifact | Traceability | `SKILL.md` § Nuclear Industry Source References |

> Numbering note: `S-003-0N` IDs are the tournament cross-strategy identifiers requested for this execution; `SM-00N-{execution_id}` IDs are the template-canonical identifiers per `s-003-steelman.md` § Section 1 Identity ("Finding Prefix: SM-NNN-{execution_id}"). Both are stable 1:1 aliases for the same finding throughout this report.

---

### S-003-01 (Critical) — OE entry file extension inconsistency

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Affected Dimension** | Internal Consistency (primary), Completeness (secondary) |
| **Strategy Step** | Step 2 (Weakness Classification — Structural) |

**Evidence (Original):**
- `agents/sop-capture.md` § Step 3: *"Write OE entry to TWO locations (both writes are mandatory): 1. `capture/oe-entry-{entry_id}.yaml` ... 2. `docs/experience/{entry_id}.yaml`"*
- `rules/nuclear-sop-behavior-rules.md`: *"Glob `docs/experience/*.yaml` then filter entries where `workflow_id` matches the current workflow's `workflow_id` field."*
- `templates/POST_JOB_BRIEF.template.md`: *"**Local capture path:** `capture/oe-entry-{entry_id}.md`"* and *"**Persistent path (future sop-brief retrieval):** `docs/experience/{entry_id}.md`"*
- `behavioral-baselines/bb-003-oe-feedback-loop-integrity.md` B-21: *"1. `capture/oe-entry-{entry_id}.md` ... 2. `docs/experience/{entry_id}.md`"*
- `examples/c3-adr-workflow-definition.md` AC-7: *"`Glob: docs/experience/adr-authoring-c3-001-*.md`"* and Section 11: *"Reference to `docs/experience/adr-authoring-c3-001-{YYYYMMDD}-001.md`"*

**Strengthened:** All OE-entry path references standardized on `.yaml` (the majority spec: `SKILL.md`, `sop-capture.md`/`.governance.yaml`, `nuclear-sop-behavior-rules.md`, `docs/reference.md`, `docs/tutorial-getting-started.md`, and the generic `WORKFLOW_DEFINITION.template.md` all already agree on `.yaml`). See reconstructed excerpts in Step 3.1–3.3.

**Rationale:** `sop-brief`'s OE History Review (Step 4, MANDATORY, implements H-2) locates prior entries via `Glob(pattern="<oe_search_path>/**/*.yaml")`. If an implementer follows the `.md`-suffixed templates/baseline/example instead of the `.yaml`-suffixed agent methodology, `sop-capture` would write entries that `sop-brief`'s own Glob can never retrieve — silently returning zero OE entries every time, for a mechanism `SKILL.md` itself describes as producing "MANDATORY CONTEXT, not optional reading." This is exactly the kind of gap that, left unfixed, a Devil's Advocate or Red Team pass would weaponize as evidence that the skill's headline OE-feedback-loop claim is unreliable — which is why S-003 fixes it now rather than leaving it for S-002/S-001 to discover.

**Best Case Conditions:** The fix is a three-file, extension-only edit (`.md` → `.yaml` in 5 specific locations across `POST_JOB_BRIEF.template.md`, `bb-003`, and the C3 example) with zero architectural risk — the underlying dual-write-plus-Glob-retrieval design is sound and does not need to change.

**Recommendation:** Change the 5 `.md` OE-path references identified above to `.yaml`, and add a BB-003 drift-detection signal for "OE entry written with wrong extension" so future regressions are caught by the same QA mechanism the skill already uses for STAR/hold-point drift.

---

### S-003-02 (Critical) — H-36 governance-deadline inconsistency and apparent staleness

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Affected Dimension** | Internal Consistency, Traceability |
| **Strategy Step** | Step 2 (Weakness Classification — Structural) |

**Evidence (Original):**
- `SKILL.md` § H-36 Circuit Breaker Compliance: *"If no H-36 ruling is received within 60 days of Phase 1 delivery, the default behavior is 3-hop mode for all criticality levels."*
- `PLAYBOOK.md` § Workflow Sequences: *"If no H-36 ruling within 60 days of Phase 1 delivery, 3-hop mode becomes permanent for all criticality levels."*
- `rules/nuclear-sop-behavior-rules.md` NS-H-08: *"H-36 governance ruling tracked as worktracker entity `TASK-0039-H36-RULING` with deadline 60 days from skill registration (2026-06-15)."*

**Strengthened:** See reconstructed excerpts in Step 3.4–3.5: a single anchor event ("skill registration," matching NS-H-08's own concrete date), a full path to the tracked worktracker entity instead of a bare ID, and a machine-checkable `governance_ruling_status` field so staleness does not require a reader to manually diff a date against wall-clock time.

**Rationale:** Two different anchor events ("Phase 1 delivery" vs. "skill registration") for what is presented as the same 60-day countdown means two readers of two different files could compute two different deadlines. More importantly: this review is being conducted as of the session's current date, which is well after the concrete 2026-06-15 deadline stated in NS-H-08. If the governance ruling has not occurred, NS-H-08's *own stated fallback* ("the default behavior is 3-hop mode for all criticality levels... sop-verifier is eliminated as a separate agent") may already be due, yet NS-H-08 as written still asserts "C3+ workflows MUST use 4-hop mode... **APPROVED for all criticality levels**" in unqualified present tense, with no visible resolution recorded anywhere in the 36 reviewed files. This is not asserted as a certainty (the ruling may have occurred in an artifact outside the reviewed file set, per this execution's blindness constraint) — it is flagged precisely because the document provides no way for a reader to tell which state currently holds without leaving the skill's own files.

**Best Case Conditions:** Unifying the anchor event and adding a status field is a documentation-only change (no behavior change to `sop-executor`/`sop-verifier` regardless of which mode ultimately wins the governance ruling), and it converts an unverifiable, must-compute-manually claim into a self-auditing one.

**Recommendation:** (1) Standardize all three files on "60 days from skill registration (2026-06-15)"; (2) add the full worktracker path for `TASK-0039-H36-RULING`; (3) add a `governance_ruling_status` field to NS-H-08 (and mirror it in `SKILL.md`/`PLAYBOOK.md` via reference, not restatement) so the current resolution state is a single, checkable fact rather than three prose paragraphs that must independently agree.

---

### S-003-03 (Major) — Registration Content narrative is stale relative to what was actually applied

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Affected Dimension** | Internal Consistency, Traceability |
| **Strategy Step** | Step 2 (Weakness Classification — Presentation/Structural) |

**Evidence (Original):**
- `SKILL.md` § Registration Content: *"The skill is NOT registered and NOT live-routable until QG-E6 passes and the user applies these entries."* followed by a `mandatory-skill-usage.md` copy-paste row with `Priority 12` and negative-keywords `adversarial, tournament, quality gate, transcript, VTT, SRT, penetration, exploit, code review`.
- Actually-applied row in `.context/rules/mandatory-skill-usage.md`: `Priority 16`, negative-keywords `adversarial, tournament, quality gate, transcript, VTT, SRT, penetration, exploit, code review, multi-phase, pipeline coordination, research, investigate, root cause, threat model, STRIDE, secure design`, and an expanded compound-trigger list (`"step sign-off" OR "place-keeping" OR "procedure compliance"` added).
- `CLAUDE.md` Quick Reference table already lists `/nuclear-sop`; `AGENTS.md` already contains the full "## Nuclear SOP Skill Agents" section; `.claude-plugin/plugin.json` already lists all 4 `sop-*.md` agent paths.

**Strengthened:** See Step 3.6. The CLAUDE.md row match is exact (a positive finding worth preserving: the simple copy-paste instruction *was* followed faithfully) — only the `mandatory-skill-usage.md` block and the "DEFERRED"/"NOT registered" framing are out of sync with what shipped.

**Rationale:** A reviewer or future maintainer who trusts `SKILL.md`'s own words and re-applies its copy-paste block would *regress* the routing table's priority and negative-keyword disambiguation quality (the applied version is measurably better-disambiguated against `/problem-solving`, `/eng-team`, and `/nasa-se` collisions than the block still shown in `SKILL.md`). The self-contradiction is also exactly the situation a C4 tournament reviewer encounters: reading `SKILL.md` in isolation says "not yet registered," while reading the four named registration surfaces in the same PR shows it already is.

**Best Case Conditions:** This is a one-section text update with no behavioral consequence — the entries have already been correctly, and better, applied; only the narrative describing them needs to catch up.

**Recommendation:** Replace the "DEFERRED REGISTRATION NOTE" with a "REGISTRATION STATUS: APPLIED" note, and refresh the `mandatory-skill-usage.md` copy-paste block to match the live Priority-16 row so the section functions as an accurate reference rather than a stale draft.

---

### S-003-04 (Major) — Navigation-table coverage gaps (NAV-004) recur across the deliverable

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Affected Dimension** | Completeness |
| **Strategy Step** | Step 2 (Weakness Classification — Presentation) |

**Evidence (Original):**
- `SKILL.md` § Document Audience (Triple-Lens): none of the L0/L1/L2 rows link `#p-003-compliance`, even though `## P-003 Compliance` exists as a top-level section between "File Structure" and "Invoking an Agent."
- `PLAYBOOK.md` § Document Sections: omits `# PROCEDURE_STATE.yaml State Machine`, `# Step Limits by Criticality`, and `# OE Accumulation Thresholds` — three top-level sections that exist in the body between "Hold Point Reference" and "Integration with Other Skills."
- `AGENTS.md` § Document Sections: omits `## Nuclear SOP Skill Agents`, which exists in the body between "NASA SE Skill Agents" and "Orchestration Skill Agents."
- `docs/reference.md` § Document Sections: omits `## Related`, which exists at the end of the file.

**Strengthened:** Add the four missing entries to their respective nav tables (see Step 3.7 for the `AGENTS.md` example; the same pattern applies to the other three files).

**Rationale:** This is a recurring pattern across four independent files (not a single typo), which raises it above an isolated nit: it suggests sections were added late in each file's authoring pass without a final nav-table reconciliation step. By contrast, `docs/tutorial-getting-started.md` and `docs/howto-guides.md` have *complete* nav-table coverage, showing the authors do this correctly most of the time — which makes the gap easy to close by applying the same discipline uniformly.

**Best Case Conditions:** Four one-line table-row additions; zero content risk.

**Recommendation:** Add the four missing nav-table rows identified above. Consider a lightweight CI check (already implied by H-23/NAV-004) that diffs `##`/`#` headings against nav-table anchors for any new or modified Claude-consumed markdown file over 30 lines.

---

### S-003-05 (Major) — AGENTS.md Agent Summary not updated for the 4 new agents

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Affected Dimension** | Internal Consistency |
| **Strategy Step** | Step 2 (Weakness Classification — Structural) |

**Evidence (Original):** The Agent Summary table lists 17 skill categories summing to **89** (verified: 9+10+3+3+3+5+3+1+10+11+5+6+3+11+2+2+2 = 89), with no "Nuclear SOP Agents" row, immediately below a "## Nuclear SOP Skill Agents" section (added by this PR, per `CHANGELOG.md`'s own entry: *"4 agents (sop-brief, sop-executor, sop-verifier, sop-capture)... agents registered in plugin.json (#269)"*) that documents exactly 4 new invokable agents.

**Strengthened:** See Step 3.7 — add "Nuclear SOP Agents | 4 | `/nuclear-sop` skill" and correct the Total to 93 (re-verified: 9+10+4+3+3+3+5+3+1+10+11+5+6+3+11+2+2+2 = 93).

**Rationale:** This is a self-falsifying claim the moment the new section exists in the same document: a reader can add the visible per-category numbers and get 89, then count the "## Nuclear SOP Skill Agents" table's 4 rows and immediately notice the total undercounts by 4. (Note, scoped for fairness: the file's separate "Verification" footnote — "82 total files found; 4 template/extension files excluded... = 89 invokable agents" — already contains an arithmetic gap of its own, 82−4=78≠89, that predates this PR's changes and is not attributable to the nuclear-sop addition; it is called out here only so the recommendation below does not conflate the two issues.)

**Best Case Conditions:** One row addition and one total correction; no dependency on resolving the pre-existing 82-vs-89 footnote discrepancy, which is out of scope for this PR's own changes.

**Recommendation:** Add the Nuclear SOP Agents row, correct the Total to 93, and refresh the "Last verified" date. Separately (out of scope for this finding but noted for completeness), the pre-existing "82 total files... = 89" footnote arithmetic should be reconciled by whoever owns `AGENTS.md`'s verification process, independent of this PR.

---

### S-003-06 (Major) — MCP "Not included (by design)" note omits sop-*

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Affected Dimension** | Completeness |
| **Strategy Step** | Step 2 (Weakness Classification — Evidence/Presentation) |

**Evidence (Original):** *"**Not included (by design):** adv-* ..., sb-* ..., wt-* ..., ps-critic/ps-validator ..., ps-reporter .... eng-*/red-* agents do not use Memory-Keeper..."* — no mention of `sop-*` anywhere in the MCP Tool Access section (neither the Context7 table, the Memory-Keeper table, nor this explanatory note), despite `sop-*` agents' own governance files explicitly declaring file-based persistence only (`PROCEDURE_STATE.yaml`, `HOLD_POINT_LOG.md`, dual-write `docs/experience/*.yaml`) with T1/T2 tool tiers matching the same profile as the already-listed exclusions.

**Strengthened:** See Step 3.8 — add `sop-*` to the note with the same file-based-persistence rationale already used for the other exclusions.

**Rationale:** The note's own purpose is to make every agent's MCP status self-explanatory (present or explicitly excluded-with-reason). Leaving `sop-*` off silently could read as an oversight rather than a considered exclusion, especially since the PR's own edits already touched this file to add the "## Nuclear SOP Skill Agents" section — the natural place to also close this loop.

**Best Case Conditions:** A one-clause addition to an already-existing sentence; no schema or governance-file changes needed.

**Recommendation:** Add `sop-*` to the "Not included (by design)" note as shown in Step 3.8.

---

### S-003-07 (Minor) — "Pre-Ship Gate" heading retains pre-ship framing after the gate passed

**Evidence:** `SKILL.md`: *"### STAR Validation Pre-Ship Gate"* followed immediately by *"**C3+ workflow status: APPROVED.** QG-E4 STAR A/B validation PASSED on 2026-04-20 with 3/3 catch rate (100%)."*

**Recommendation:** Rename the heading to `### STAR Validation Gate (QG-E4) — Result: PASSED` (Step 3.9) so a reader scanning headings alone does not read "pre-ship" as "still pending."

---

### S-003-08 (Minor) — Source citations not cross-linked to the internal research artifact

**Evidence:** `SKILL.md` § Nuclear Industry Source References cites 5 external documents (INPO AP-907 Rev.3, INPO 09-003 Rev.1, INPO 06-003, 10 CFR 50 App B, NUREG-1792) with no pointer to the internal artifact that performed the extraction, while `WORKFLOW_DEFINITION.template.md`'s footer separately cites: *"source: Phase 1 Research Survey Section 3.3 — see `«PR projects tree»/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-build-20260325-001/eng/phase-1/`"* (path substituted per this report's path-hygiene rule).

**Recommendation:** Add the one-line cross-reference shown in Step 3.10 so a reader auditing the citation table has a single-hop path to the internal synthesis work, rather than needing to discover the connection by separately reading `WORKFLOW_DEFINITION.template.md`'s footer.

---

## Step 6: Present the Steelman

Self-review applied (H-15): all 8 findings cite specific, verbatim, file-and-line-traceable evidence; severity classifications follow the template's Step 5 definitions (Critical = "original could not withstand critique without this improvement," applied to S-003-01/02 because both sit on mechanisms the skill itself calls mandatory/load-bearing; Major = "original would score notably lower without it," applied to S-003-03/04/05/06 because each is a concrete, quotable, but non-load-bearing consistency gap; Minor = polish, applied to S-003-07/08). The reconstruction preserves the original thesis in full — no finding proposes changing the nuclear-pattern mapping, the 4-agent topology, the hold-point model, the STAR protocol, or the constitutional-compliance mechanisms. All 8 improvements are traceable to specific SM-NNN identifiers and cross-referenced to their S-003-0N tournament IDs.

**Decision:** Two Critical findings exist (S-003-01, S-003-02), both concentrated on the OE-review loop and the governance self-monitoring mechanism specifically — both are recommended for resolution before downstream critique strategies (S-002 Devil's Advocate, S-004 Pre-Mortem, S-001 Red Team, S-007 Constitutional AI) evaluate this artifact, per the template's own Step 6 decision rule ("If substantially different from original (many Critical/Major): recommend author review before critique"). This Steelman Reconstruction is ready for downstream use; reviewers should treat S-003-01 and S-003-02 as pre-existing conditions that other strategies are entitled to independently rediscover and weight in their own scoring.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | S-003-04 (nav-table gaps), S-003-05 (agent count), S-003-06 (MCP note) each close a concrete completeness gap in the deliverable's own self-description. |
| Internal Consistency | 0.20 | Positive | Largest-impact dimension: S-003-01 (OE extension), S-003-02 (governance-deadline anchor), S-003-03 (registration narrative), S-003-05 (agent count arithmetic) are all direct internal-consistency repairs. |
| Methodological Rigor | 0.20 | Positive | S-003-02's proposed machine-checkable status field and S-003-01's dual-write/Glob-retrieval alignment both harden the methodology's self-verifiability without altering the underlying nuclear-pattern mapping, which was already rigorous. |
| Evidence Quality | 0.15 | Positive | S-003-07 (citation cross-link) and S-003-02 (full worktracker path instead of a bare ID) strengthen the evidence chain supporting load-bearing claims. |
| Actionability | 0.15 | Positive | Every finding is single-file-or-few-file-scoped, concretely worded, and directly incorporable without redesign; S-003-07's heading rename directly improves a reader's ability to act on the gate's current status. |
| Traceability | 0.10 | Positive | S-003-02, S-003-06, S-003-07, S-003-08 each add a missing link, path, or cross-reference that was previously absent. |

Impact key: **Positive** = directly strengthened by incorporating the finding; no **Negative** impacts identified (no improvement introduces a new weakness).

---

## Execution Statistics

- **Total Findings:** 8
- **Critical:** 2 (S-003-01, S-003-02)
- **Major:** 4 (S-003-03, S-003-04, S-003-05, S-003-06)
- **Minor:** 2 (S-003-07, S-003-08)
- **Protocol Steps Completed:** 6 of 6 (Deep Understanding, Weakness Classification, Reconstruction, Best Case Scenario, Improvement Findings, Present the Steelman)
- **Files reviewed:** 31 skill files + 5 registration surfaces = 36 files, ~8.5k lines
- **H-16 status:** N/A for this execution (S-003 has no prerequisite strategy; this report is itself the H-16 prerequisite for any S-002/S-004/S-001 execution against this deliverable)

---

## Strategy Verdict

The `/nuclear-sop` skill is a well-conceived, unusually well-documented, and directionally sound transplant of nuclear-industry procedural discipline into Jerry's C2+ agent workflows: its architecture correctly reuses existing Jerry mechanisms (P-003 single-level nesting, `/adversary` S-014 for QG-HOLD, Task-tool fresh-context isolation for IV-HOLD) rather than duplicating them, and its self-disclosed limitations — STAR is behavioral rather than physical, `sop-verifier`'s independence is approximated rather than equivalent to personnel independence, 3-hop mode carries an explicit anchoring-bias disclaimer — exceed typical P-022 compliance and are backed by an actual empirical validation fixture (three ATT&CK-mapped STAR traps, a claimed 3/3 catch rate) rather than an unfalsifiable assertion; the idea does not need defending on substance, and downstream critique strategies should attack mechanism design, not premise. What this Steelman pass found instead is a concentrated cluster of mechanical, same-file-family consistency and freshness defects sitting precisely on the skill's two most safety-relevant self-monitoring surfaces: a three-file OE-entry extension mismatch (`.yaml` vs. `.md`) that could silently zero out `sop-brief`'s mandatory OE-retrieval Glob, and an H-36 governance-deadline mechanism with two different anchor events across files and no machine-checkable staleness signal, whose stated concrete deadline appears (as of this review) to have already elapsed without a visible resolution recorded anywhere in the reviewed files. Both are Critical, both are editorial rather than architectural, and both are resolvable in well under an hour without touching STAR, the hold-point model, or the agent topology — which is exactly why S-003 surfaces them now, before S-001/S-002/S-004/S-007 can use them as evidence that the OE feedback loop or the governance-tracking apparatus is unreliable by design rather than merely under-polished.

---

*Report Version: 1.0.0*
*Strategy: S-003 (Steelman Technique) v1.0.0*
*Template: `.context/templates/adversarial/s-003-steelman.md`*
*Constitutional Compliance: P-001 (evidence-based, every finding quotes source text), P-002 (persisted to file before return), P-003 (worker agent; no subagent invocation), P-004 (provenance cited for every claim), P-022 (path substitutions and blindness scope disclosed explicitly)*
*Agent: adv-executor (worker)*
*Execution ID: 20260807T1200*
