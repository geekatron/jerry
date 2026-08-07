# /nuclear-sop Skill Structure Compliance Audit (PR #269)

> **Auditor:** skill-structure standards auditor (independent review)
> **Subject:** `/nuclear-sop` skill, PR #269 head commit `bda64202` ("chore(nuclear-sop): register 4 agents in plugin.json + changelog entry")
> **Subject worktree:** PR-branch checkout (31 files under `skills/nuclear-sop/` + registration surfaces)
> **Standards baseline:** current `feat/proj-032-nuclear-sop-review` worktree — `skill-standards.md` v1.2.0 (H-25, H-26), `markdown-navigation-standards.md` (H-23), `mandatory-skill-usage.md` (H-22, trigger map), `agent-routing-standards.md` (H-36, RT-M-001..015)
> **Scope:** non-agent surface (SKILL.md, PLAYBOOK.md, rules/, templates/, behavioral-baselines/, docs/, examples/, registration surfaces). Agent-definition internals (H-34/H-35 compliance of `agents/*.md` + `.governance.yaml`) are covered by a separate agent audit; agent files appear here only for the H-23 file sweep.
> **Date:** 2026-08-07

## Document Sections

| Section | Purpose |
|---------|---------|
| [Verdict Summary](#verdict-summary) | One-paragraph bottom line |
| [Per-Check Compliance Matrix](#per-check-compliance-matrix) | Every mandated check with PASS/FAIL/PARTIAL |
| [H-23 Navigation Table Sweep (31 files)](#h-23-navigation-table-sweep-31-files) | File-by-file nav-table status |
| [Findings](#findings) | Numbered findings with rule IDs, evidence, recommendations |
| [Trigger Map and Collision Analysis](#trigger-map-and-collision-analysis) | Routing-layer detail behind findings F-6/F-7 |
| [Verification Notes and Method](#verification-notes-and-method) | What was verified vs. inferred; calibration evidence |

---

## Verdict Summary

The `/nuclear-sop` skill is structurally strong on the basics: H-25 naming/structure is fully compliant, the frontmatter description is well-formed (684 chars, WHAT+WHEN+triggers, no XML), every repo-relative path referenced from SKILL.md/PLAYBOOK.md resolves on the PR branch, registration rows exist in CLAUDE.md, AGENTS.md, the trigger map, plugin.json, and CHANGELOG.md, and most long markdown files carry compliant navigation tables. The significant problems are (1) one Critical H-23 gap — three runtime-consumed long files (the workflow-definition template, hold-point log template, and the C3 example/QG-E4 fixture) ship without navigation tables while the framework's own template corpus and 3 of the skill's own 5 templates comply; and (2) a cluster of Major internal-consistency/governance defects: an OE-entry file-extension contradiction (`.yaml` vs `.md`) that would break the skill's own operating-experience feedback loop as written, a SKILL.md "DEFERRED REGISTRATION" note that falsely claims the skill is not registered on a branch that registers it, a PLAYBOOK security section still asserting a C3+ restriction that SKILL.md declares lifted, an H-36 governance deadline (2026-06-15) that has lapsed with contradictory fallback instructions and a claimed worktracker entity that does not exist, the H-22 rule text and L2-REINJECT never updated to cover `/nuclear-sop`, and an unresolved "nuclear workflow" keyword collision whose claimed compound-trigger resolution is absent from the actual row.

**Totals: 1 Critical, 6 Major, 6 Minor. 21 checks passed.**

---

## Per-Check Compliance Matrix

| # | Check | Rule | Result | Evidence Pointer |
|---|-------|------|--------|-----------------|
| 1 | Skill file exactly `SKILL.md` (case-sensitive) | H-25(a) | PASS | `skills/nuclear-sop/SKILL.md` exists; no case variants in file listing |
| 2 | Folder kebab-case, matches frontmatter `name` | H-25(b) | PASS | folder `nuclear-sop` = `name: nuclear-sop` (SKILL.md:2) |
| 3 | No `README.md` inside skill folder | H-25(c) | PASS | full recursive file listing contains no README.md |
| 4 | Description: WHAT+WHEN+triggers, <1024 chars, no XML | H-26(a) | PASS | 684 chars measured; contains "WHEN: use for any workflow requiring…" and "Triggers: nuclear sop, pre-job brief, …"; no `<`/`>` |
| 5 | Repo-relative paths in SKILL.md/PLAYBOOK.md resolve on PR branch | H-26(b) | PASS | all 19 distinct referenced paths verified to exist (agents ×4, templates ×5, baselines ×3, example, rules, spec synthesis, ADR-001, QG-E4 results, test-strategy, eng/phase-1 dir) |
| 6 | Registered in CLAUDE.md | H-26(c) | PASS | PR CLAUDE.md:78 `| \`/nuclear-sop\` | Nuclear-inspired SOP execution: pre-job brief, STAR self-check, hold points, OE capture |` |
| 7 | Registered in AGENTS.md | H-26(c) | PASS | PR AGENTS.md:152-162 "## Nuclear SOP Skill Agents" with 4-agent table, matches house style of sibling sections |
| 8 | Trigger-map row in mandatory-skill-usage.md | H-26(c)/H-22 | PASS (row) | PR `.context/rules/mandatory-skill-usage.md:50`, 5-column format, priority 16 |
| 9 | H-22 rule sentence + L2-REINJECT cover /nuclear-sop | H-22 | **FAIL** | grep of PR mandatory-skill-usage.md: only hit is trigger-map row; H-22 sentence and L2-REINJECT enumerate 15 other skills, not /nuclear-sop (Finding F-6) |
| 10 | Trigger-map priority uniqueness | RT-M-003 | PASS | priority 16 unused by any other row on both PR branch and current standards worktree (max elsewhere: 15) |
| 11 | Keyword collision analysis | RT-M-004 | **FAIL** | "nuclear workflow" collides with /orchestration "workflow" (priority 1 vs 16); claimed compound-trigger resolution absent from row (Finding F-7) |
| 12 | H-23 nav tables across all 31 skill files >30 lines | H-23 | **FAIL** (3 Critical violators; 8 letter-of-rule gaps consistent with corpus practice) | see [H-23 sweep](#h-23-navigation-table-sweep-31-files); Findings F-1, F-8 |
| 13 | SKILL.md frontmatter: Jerry-required fields | skill-standards MEDIUM | PASS | `name`, `description`, `version: "1.1.0"`, `allowed-tools`, `activation-keywords` all present, correct formats |
| 14 | `allowed-tools` grant-list plausibility | skill-standards MEDIUM | PARTIAL | `Read, Write, Edit, Glob, Grep, Bash` — omits `Agent`/`Task` although NS-H-08 4-hop mode mandates Task-tool invocation of sop-verifier; corpus convention mixed (Finding F-9) |
| 15 | plugin.json agent registration coherence | registration | PASS | `.claude-plugin/plugin.json:53-56` lists all 4 `skills/nuclear-sop/agents/sop-*.md`; all 4 files exist; alphabetical placement consistent; `"skills": "./skills/"` auto-covers the skill |
| 16 | CHANGELOG entry present | registration | PASS | CHANGELOG.md `[Unreleased] > Added`: "**feat(nuclear-sop):** `/nuclear-sop` skill — … agents registered in plugin.json (#269)" |
| 17 | templates/ internal consistency | consistency | **FAIL** | POST_JOB_BRIEF.template.md uses `.md` OE paths vs rules/docs/PLAYBOOK `.yaml` (Finding F-2); PRE_JOB_BRIEF and HOLD_POINT_LOG otherwise consistent with rules (hold vocab, SR-04/SR-05 cross-refs match) |
| 18 | behavioral-baselines/ internal consistency | consistency | **FAIL** (bb-003) / PASS (bb-001, bb-002) | bb-001 STAR phases match rules STAR Protocol; bb-002 APPROVE/REJECT/WAIVE paths match NS-H-02; bb-003 globs `docs/experience/*.md` contradicting rules' `*.yaml` (Finding F-2) |
| 19 | examples/ coherence | consistency | PARTIAL | 15 steps (= C3 max), 3 hold points, TRAP-01/02/03 at steps 6/9/11 exactly as SKILL.md QG-E4 fixture claims; defects: AC-7/§11 `.md` OE paths (F-2), TRAP-01 WARNING path mismatch (F-10), unpathed `skill-integration-analysis.md` citations (F-13) |
| 20 | Skill directory structure vs framework conventions | skill-standards MEDIUM | PASS | PLAYBOOK.md (4 precedents), docs/ (4), composition/ (13), rules/ + templates/ (worktracker) all established; `examples/` and `behavioral-baselines/` are novel but purposeful — noted, no finding |
| 21 | SKILL.md body structure vs reference implementations | skill-standards MEDIUM | PASS (with NAV-004 note) | Triple-Lens-only navigation matches both named reference implementations (adversary, problem-solving SKILL.md); P-003 Compliance section missing from Triple-Lens rows (Finding F-12) |
| 22 | Cross-document governance consistency | H-03/P-022, H-36, H-32 | **FAIL** | Findings F-3 (false deferred-registration note), F-4 (stale PLAYBOOK C3+ restriction), F-5 (H-36 deadline lapsed, contradictory fallbacks, phantom worktracker entity) |

---

## H-23 Navigation Table Sweep (31 files)

Rule: H-23 — all Claude-consumed markdown files over 30 lines MUST include a navigation table (NAV-001) with anchor links (NAV-006). YAML files are exempt ("pure data files"). Every markdown file in the skill exceeds 30 lines.

| File | Lines | Nav Table | Status |
|------|-------|-----------|--------|
| `SKILL.md` | 477 | Triple-Lens (Format 2) w/ anchor links | PASS — matches reference implementations (adversary, problem-solving); all 13 anchors verified against headings |
| `PLAYBOOK.md` | 704 | Document Sections | PASS (anchors verified; 3 top-level sections unlisted — NAV-004, MEDIUM, note only) |
| `rules/nuclear-sop-behavior-rules.md` | 322 | Document Sections | PASS (anchors incl. `#procedure_stateyaml-state-machine` verified) |
| `templates/PRE_JOB_BRIEF.template.md` | 245 | Document Sections | PASS |
| `templates/POST_JOB_BRIEF.template.md` | 191 | Document Sections | PASS |
| `templates/WORKFLOW_DEFINITION.template.md` | 250 | **NONE** (0 anchor links) | **FAIL — Finding F-1** |
| `templates/HOLD_POINT_LOG.template.md` | 76 | **NONE** (0 anchor links) | **FAIL — Finding F-1** |
| `templates/PROCEDURE_STATE.template.yaml` | 135 | n/a | EXEMPT (YAML data) |
| `examples/c3-adr-workflow-definition.md` | 559 | **NONE** (0 anchor links) | **FAIL — Finding F-1** |
| `behavioral-baselines/bb-001-star-clean-execution.md` | 233 | Document Sections | PASS |
| `behavioral-baselines/bb-002-user-hold-activation.md` | 265 | Document Sections | PASS |
| `behavioral-baselines/bb-003-oe-feedback-loop-integrity.md` | 297 | Document Sections | PASS |
| `docs/tutorial-getting-started.md` | 383 | Document Sections | PASS |
| `docs/howto-guides.md` | 553 | Document Sections | PASS |
| `docs/reference.md` | 628 | Document Sections | PASS |
| `agents/sop-brief.md` | 371 | none | Letter-of-rule gap — Finding F-8 (existing agent corpus uniformly has none: ps-researcher, eng-qa, wt-auditor all 0 anchors) |
| `agents/sop-executor.md` | 351 | none | Letter-of-rule gap — F-8 |
| `agents/sop-verifier.md` | 324 | none | Letter-of-rule gap — F-8 |
| `agents/sop-capture.md` | 293 | none | Letter-of-rule gap — F-8 |
| `agents/sop-*.governance.yaml` ×4 | 100-113 | n/a | EXEMPT (YAML data) |
| `composition/sop-brief.prompt.md` | 234 | none | Letter-of-rule gap — F-8 (composition prompt sources; corpus practice identical) |
| `composition/sop-executor.prompt.md` | 241 | none | Letter-of-rule gap — F-8 |
| `composition/sop-verifier.prompt.md` | 214 | none | Letter-of-rule gap — F-8 |
| `composition/sop-capture.prompt.md` | 199 | none | Letter-of-rule gap — F-8 |
| `composition/sop-*.agent.yaml` ×4 | 116-144 | n/a | EXEMPT (YAML data) |

**Calibration evidence for the template verdict:** Jerry's canonical template corpus carries nav tables — 23 of 25 files sampled in `.context/templates/adversarial/` and `.context/templates/worktracker/` (all 10 strategy templates, TEMPLATE-FORMAT.md, and 12 of 14 worktracker templates) have `Document Sections` + anchor links. The skill's own PRE_JOB_BRIEF and POST_JOB_BRIEF templates comply. The two non-compliant templates and the example are omissions, not a divergent convention.

---

## Findings

### F-1 (Critical, H-23) — Three runtime-consumed long files ship without navigation tables

- **Files:** `skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md` (250 lines), `skills/nuclear-sop/templates/HOLD_POINT_LOG.template.md` (76 lines), `skills/nuclear-sop/examples/c3-adr-workflow-definition.md` (559 lines)
- **Rule:** H-23 (HARD): "All Claude-consumed markdown files over 30 lines MUST include a navigation table (NAV-001)" with anchor links (NAV-006). Consequence per rule: "Document rejected."
- **Evidence:** grep for `](#` and `Document Sections`/`| Section | Purpose |` returns zero hits in all three files. These files are runtime inputs: sop-brief consumes the workflow-definition template in Step 0 generation, sop-executor executes the example as a procedure (it is also the QG-E4 STAR validation fixture named in SKILL.md:239), and sop-executor appends to the hold-point log. All three exceed 30 lines. Jerry's canonical template corpus (23/25 sampled `.context/templates/` files) and 3 of this skill's own 5 templates comply.
- **Recommendation:** Add `## Document Sections` tables with anchor links to all three files (the example has 11 numbered sections plus an appendix — precisely the kind of long document H-23 exists for).

### F-2 (Major, consistency / NS-H-06 enforcement integrity) — OE-entry file extension contradiction (`.yaml` vs `.md`) across the operating-experience feedback loop

- **Files:** `skills/nuclear-sop/templates/POST_JOB_BRIEF.template.md` (lines 127, 129), `skills/nuclear-sop/behavioral-baselines/bb-003-oe-feedback-loop-integrity.md` (lines 75-76, 96, 112), `skills/nuclear-sop/examples/c3-adr-workflow-definition.md` (lines 480, 518)
- **Rule violated:** internal consistency of skill enforcement artifacts (Major per calibration: internal contradiction in shipped enforcement fixtures / misleading metadata). The authoritative chain — `rules/nuclear-sop-behavior-rules.md` ("OE entries are written to BOTH … Global OE registry: `docs/experience/{entry_id}.yaml`"; OE Search: "Glob `docs/experience/*.yaml`"), PLAYBOOK.md artifact table, `docs/reference.md:201,484,537`, `docs/howto-guides.md:357`, `docs/tutorial-getting-started.md` — consistently uses `.yaml` (repo-wide tally: 29 `.yaml` OE references vs 8 `.md`).
- **Evidence:** POST_JOB_BRIEF.template.md:127-129: "**Local capture path:** `capture/oe-entry-{entry_id}.md` … **Persistent path (future sop-brief retrieval):** `docs/experience/{entry_id}.md`". bb-003:112: "Primary: `Glob: docs/experience/*.md` then filter by `workflow_id` match". Example AC-7 (line 480): "`Glob: docs/experience/adr-authoring-c3-001-*.md`".
- **Runtime consequence (as written):** if sop-capture follows the post-job template, sop-brief's rules-mandated `*.yaml` OE search returns nothing — the feedback loop the skill calls its "highest-value gap" closure silently empties. If sop-capture follows the rules (`.yaml`), the example's AC-7 false-fails under sop-verifier and bb-003's drift baseline raises false drift signals. Either branch corrupts the skill's own NS-H-06/OE enforcement loop.
- **Recommendation:** Normalize all OE paths to `.yaml` in POST_JOB_BRIEF.template.md, bb-003, and the example's AC-7/§11; add a consistency check to the skill's validation checklist.

### F-3 (Major, H-26(c)/H-03/P-022 — misleading governance metadata) — SKILL.md claims the skill is NOT registered on a branch that registers it, and its copy-ready trigger row contradicts the applied row

- **File:** `skills/nuclear-sop/SKILL.md` (Registration Content section, lines 444-477)
- **Evidence:** SKILL.md:446: "**DEFERRED REGISTRATION NOTE:** … The skill is NOT registered and NOT live-routable until QG-E6 passes and the user applies these entries." On the same PR branch: CLAUDE.md:78, AGENTS.md:152-162, `.context/rules/mandatory-skill-usage.md:50`, and plugin.json:53-56 all register the skill, and QG-E6 passed on 2026-04-14 (`«PR projects tree»/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-build-20260325-001/eng/phase-6/eng-reviewer-001/qg-e6-score.md`: "**Score:** 0.934/1.00 | **Verdict:** PASS"). Additionally, SKILL.md's copy-ready trigger row (line 476) specifies priority `12` — which collides with `/user-experience` (priority 12) in both the PR-branch and current trigger maps — whereas the actually spliced row uses priority `16` and an expanded negative-keyword list. Anyone "applying" the SKILL.md copy per its instructions would introduce a priority collision and regress the negatives.
- **Recommendation:** Replace the Registration Content section with a statement of applied registration (or drop it), and if copy-ready content is retained, synchronize it with the applied row (priority 16, full negative list).

### F-4 (Major, H-03/P-022 — stale governance state) — PLAYBOOK still asserts the C3+ restriction that SKILL.md declares lifted

- **File:** `skills/nuclear-sop/PLAYBOOK.md` (L2 Security Considerations, line 677)
- **Evidence:** PLAYBOOK.md:677: "**STAR Validation Pre-Ship Gate.** The skill is NOT available for C3+ workflows until the STAR A/B validation gate (QG-E4) passes. … Until QG-E4 passes … restrict to C1-C2 only." SKILL.md:229 states the opposite: "**C3+ workflow status: APPROVED.** QG-E4 STAR A/B validation PASSED on 2026-04-20 with 3/3 catch rate (100%)" and SKILL.md:244 "approved for all criticality levels (C1 through C4)"; NS-H-08 carries the same PASS annotation. The PLAYBOOK footer claims currency with "Skill: /nuclear-sop v1.1.0". A reader routed to the PLAYBOOK (its stated purpose is routing guidance) gets a criticality gate opposite to the skill's declared state.
- **Recommendation:** Update PLAYBOOK L2 to the post-QG-E4 state (approved C1-C4, with the QG-E4 evidence pointer), or restore the restriction everywhere if the PASS claim is not accepted at review.

### F-5 (Major, H-36 / H-32 — contradictory mandatory instructions past a lapsed governance deadline; phantom worktracker entity) — post-deadline C3+ behavior is undefined

- **Files:** `skills/nuclear-sop/SKILL.md` (lines 275-277), `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` (NS-H-08, line 37; §Governance Deadline, line 286), `skills/nuclear-sop/PLAYBOOK.md` (lines 264, 640)
- **Evidence:** NS-H-08: "C3+ workflows MUST use 4-hop mode … **GOVERNANCE DEADLINE:** H-36 governance ruling tracked as worktracker entity `TASK-0039-H36-RULING` with deadline 60 days from skill registration (2026-06-15). … Until that revision is completed, NS-H-08 remains as written." versus SKILL.md:277: "If no H-36 ruling is received within 60 days of Phase 1 delivery, the default behavior is 3-hop mode for all criticality levels. sop-verifier is eliminated as a separate agent…" (PLAYBOOK:264/640 repeat the 3-hop-fallback version). Today (2026-08-07) is past 2026-06-15; no ruling artifact exists on the PR branch; and the string `TASK-0039-H36-RULING` appears nowhere in the repository except its own mention in the rules file — no worktracker entity file exists (also unmet H-32 GitHub-issue parity for a claimed jerry-repo work item). A C3 execution today receives two contradictory mandatory instructions: "4-hop REQUIRED, NS-H-08 remains as written" and "3-hop is now the default for all criticality levels; sop-verifier is eliminated."
- **Note on the underlying H-36 question:** under the current H-36 definition ("a hop is one transition … where routing logic re-evaluates the destination"), the skill's predetermined main-context fan-out arguably accrues fewer hops than its own conservative analysis assumes; the framework already ships 10-11-agent skills under the same pattern. The defect is not the 4-agent design — it is shipping contradictory post-deadline mandates keyed to a tracker entity that does not exist.
- **Recommendation:** Resolve the ruling before merge (or reset the deadline relative to actual registration), create the `TASK-0039-H36-RULING` worktracker entity + GitHub issue per H-32, and make SKILL.md, PLAYBOOK.md, and NS-H-08 state one identical post-deadline behavior.

### F-6 (Major, H-26(c)/H-22 — registration gap) — H-22 rule sentence and L2-REINJECT omit /nuclear-sop

- **File:** PR `.context/rules/mandatory-skill-usage.md` (H-22 row, line 23; L2-REINJECT comment, line 5)
- **Evidence:** The H-22 HARD-rule sentence enumerates MUST-invoke clauses for all 15 other trigger-mapped skills ("MUST invoke `/problem-solving` … MUST invoke `/contract-design` …") but contains no `/nuclear-sop` clause; the L2-REINJECT comment likewise ends at `/contract-design`. The PR's own build artifact prescribed the update: `«PR projects tree»/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-build-20260325-001/eng/phase-6/eng-reviewer-001/registration-trigger-map-row.md` — "## Corresponding H-22 Rule Update — Add to the H-22 rule text…: MUST invoke `/nuclear-sop` for nuclear-inspired procedural execution requiring pre-job briefing, STAR self-checking, hold points, place-keeping, and OE capture." It was not applied.
- **Consequence:** the proactive-invocation mandate (H-22) and the context-rot-immune L2 re-injection layer never cover `/nuclear-sop`; the skill routes only via the trigger map (L1, context-rot-vulnerable at session scale).
- **Recommendation:** Apply the phase-6-prescribed H-22 sentence and extend the L2-REINJECT content string.

### F-7 (Major, RT-M-004/RT-M-003 — unresolved keyword collision with false resolution claim) — "nuclear workflow" routes to /orchestration

- **Files:** PR `.context/rules/mandatory-skill-usage.md:50` (applied row), `skills/nuclear-sop/SKILL.md:26,476` (activation keyword + copy row), `«PR projects tree»/PROJ-0039-nuclear-engineer/.../eng/phase-6/eng-reviewer-001/registration-trigger-map-row.md` (collision analysis)
- **Evidence:** "nuclear workflow" is an activation keyword (SKILL.md:26) and a trigger-map positive keyword. "workflow" is an `/orchestration` positive keyword (priority 1); "nuclear" is not in `/orchestration`'s negative list. The applied row's compound triggers are: `"nuclear procedure" OR "pre-job brief" OR "post-job brief" OR "STAR self-check" OR "hold point" OR "step sign-off" OR "place-keeping" OR "procedure compliance"` — "nuclear workflow" is absent. The phase-6 collision analysis claims the opposite: "'workflow' (standalone) -> `/orchestration` via priority (1 vs. 12); **'nuclear workflow' -> `/nuclear-sop` via compound trigger**" — a compound that does not exist in either the phase-6 row or the applied row. Under the routing algorithm (agent-routing-standards.md Steps 1-3), a request like "run this with nuclear workflow discipline" matches both skills, no compound fires, and Step 3 priority ordering (1 vs 16, gap >= 2) routes to `/orchestration` — a deterministic misroute of a documented activation keyword. (By contrast, the "procedure compliance" vs `/nasa-se` "compliance" collision IS correctly resolved by a compound trigger.)
- **Recommendation:** Add `"nuclear workflow" OR "nuclear sop"` to the compound-trigger list (or add "nuclear" to `/orchestration`'s negative keywords), and correct the collision-analysis artifact.

### F-8 (Minor, H-23 letter-of-rule) — agent and composition prompt files lack navigation tables, consistent with existing corpus practice

- **Files:** `skills/nuclear-sop/agents/sop-{brief,executor,verifier,capture}.md` (293-371 lines), `skills/nuclear-sop/composition/sop-{brief,executor,verifier,capture}.prompt.md` (199-241 lines)
- **Evidence:** zero anchor links / nav tables in all eight. Calibration: existing Jerry agent definitions uniformly ship without nav tables (ps-researcher.md 509 lines, wt-auditor.md 647 lines, eng-qa.md 132 lines — all 0 anchor links); agent bodies are governed by H-34's XML-tagged section structure instead. Reported for completeness of the 31-file sweep; treating these as Critical would indict the entire existing agent corpus.
- **Recommendation:** Resolve at framework level (either exempt agent definitions from H-23 explicitly in markdown-navigation-standards.md, or add nav tables corpus-wide); no nuclear-sop-specific action required.

### F-9 (Minor, skill-standards MEDIUM — grant-list plausibility) — `allowed-tools` omits Agent/Task while the skill's own HARD rule mandates Task-tool invocation

- **File:** `skills/nuclear-sop/SKILL.md:5`
- **Evidence:** `allowed-tools: Read, Write, Edit, Glob, Grep, Bash`. NS-H-04/NS-H-08 make sop-verifier invocation "via Task tool (fresh context)" MANDATORY for C3+; SKILL.md:331 "sop-verifier invoked via Task tool". Corpus convention is mixed: orchestration, problem-solving, nasa-se, transcript include `Agent` in allowed-tools; eng-team, red-team, adversary omit it (and function). If `allowed-tools` were enforced as a runtime gate while the skill is active, the mandatory 4-hop mode could not execute; because half the corpus omits it without observed breakage, this is recorded as a plausibility inconsistency, not a defect with confirmed runtime impact.
- **Recommendation:** Add `Agent` to `allowed-tools` for explicit consistency with the skill's mandatory delegation flow (matching orchestration/problem-solving precedent).

### F-10 (Minor, examples coherence) — TRAP-01's WARNING cites a different "final path" than the trap's Target

- **File:** `skills/nuclear-sop/examples/c3-adr-workflow-definition.md` (Step 6, lines 235-249)
- **Evidence:** WARNING (line 235): "This step writes to `projects/{JERRY_PROJECT}/decisions/ADR-NNN.md`." Target (line 249) and all trap annotations: "`docs/design/ADR-NNN.md`   <!-- TRAP-01: Wrong path…". The workflow's actual final placement path (Step 13) is `docs/design/`. The WARNING's `projects/…/decisions/` path appears nowhere else in the workflow; within a fixture whose purpose is precise path-mismatch detection, the trap's own description disagrees with its Target.
- **Recommendation:** Align the WARNING text to `docs/design/ADR-NNN.md`.

### F-11 (Minor, SKILL.md self-description accuracy) — File Structure section omits shipped components

- **File:** `skills/nuclear-sop/SKILL.md` (File Structure, lines 283-305)
- **Evidence:** The tree lists `SKILL.md`, `agents/`, `templates/`, `examples/`, `rules/` only. Actually shipped and undocumented there: `PLAYBOOK.md` (704 lines), `behavioral-baselines/` (3 files, referenced in the References table but absent from the tree), `composition/` (8 files, described in PLAYBOOK as agent sources), `docs/` (3 files).
- **Recommendation:** Complete the tree; the References table and PLAYBOOK already acknowledge most of these components.

### F-12 (Minor, NAV-004 MEDIUM) — SKILL.md Triple-Lens navigation omits the P-003 Compliance section

- **File:** `skills/nuclear-sop/SKILL.md` (Document Audience table, lines 36-42)
- **Evidence:** The Triple-Lens rows link 13 sections; the `## P-003 Compliance` section (line 309) appears in none of the three lens rows. NAV-004 (MEDIUM): all major sections SHOULD be listed. (PLAYBOOK.md similarly omits `# PROCEDURE_STATE.yaml State Machine`, `# Step Limits by Criticality`, and `# OE Accumulation Thresholds` from its nav table.) Structure otherwise matches the reference implementations (adversary and problem-solving SKILL.md are also Triple-Lens-only).
- **Recommendation:** Add the missing section links to the L2 lens row (SKILL.md) and the PLAYBOOK nav table.

### F-13 (Minor, conventions) — Project-ID format, tool naming, and unpathed citation

- **Files:** `skills/nuclear-sop/SKILL.md:34` et al.; `skills/nuclear-sop/examples/c3-adr-workflow-definition.md:28,30,536`
- **Evidence:** (a) `«PR projects tree»/PROJ-0039-nuclear-engineer/` uses a 4-digit ID; every other project on the branch uses `PROJ-{NNN}` 3-digit (project-workflow.md: "Projects follow `projects/PROJ-{NNN}-{slug}/`"), and PROJ-0039 sorts between PROJ-003 and PROJ-004. (b) Skill docs say "Task tool" throughout; current standards phrase it "Agent tool (or its backward-compatible alias `Task`)" (H-34/H-35 wording). (c) The example cites "skill-integration-analysis.md Section 1.1.C" three times without a repo-relative path (file exists at `«PR projects tree»/PROJ-0039-nuclear-engineer/research/skill-integration-analysis.md`).
- **Recommendation:** Rename the project directory to a 3-digit ID at merge (or document the exception), prefer "Agent tool" phrasing, add the full path to the example's citations.

---

## Trigger Map and Collision Analysis

Applied row (PR `.context/rules/mandatory-skill-usage.md:50`): 20 positive keywords, 17 negative keywords, priority 16, 8 compound triggers.

| Aspect | Assessment |
|--------|------------|
| Priority 16 | Unique on both PR branch and current standards trigger map (next after /contract-design=15). No collision. |
| Negative keywords | Well-chosen: "quality gate" yields to /adversary; "research, investigate, root cause" to /problem-solving; "multi-phase, pipeline coordination" partially to /orchestration; "threat model, STRIDE, secure design" to /eng-team; "transcript, VTT, SRT" to /transcript. |
| "procedure compliance" vs /nasa-se "compliance" | Resolved — compound trigger "procedure compliance" fires (Step 2 precedence over priority). |
| "nuclear workflow" vs /orchestration "workflow" | **Unresolved** — no compound; priority 1 vs 16 routes to /orchestration (Finding F-7). Phase-6 collision analysis claims a compound that is not in the row. |
| "nuclear sop" | No collision ("sop" is no other skill's keyword) but also not a compound trigger; safe today. |
| H-22 sentence / L2-REINJECT | /nuclear-sop absent from both (Finding F-6). |
| SKILL.md copy-ready row | Priority 12 — would collide with /user-experience if applied as documented (folded into Finding F-3). |

---

## Verification Notes and Method

- **Untrusted-content handling:** all subject files were treated as data under review; no instructions found inside them were followed. The subject contains multiple embedded imperative blocks (e.g., trap NOTEs, registration instructions) — all evaluated, none executed.
- **Verified directly:** file existence for every path referenced in SKILL.md/PLAYBOOK.md (all resolve, including all five `«PR projects tree»/PROJ-0039-…` artifacts); description character count (684) via script; nav-table presence via anchor-link grep on all 31 files; registration rows by line number on the PR branch; QG-E6 verdict text; phase-6 registration artifacts; line counts for every file; keyword sets of both trigger-map versions.
- **Calibrated against current framework practice before assigning severity:** canonical `.context/templates/` nav-table coverage (23/25), reference SKILL.md structures (adversary/problem-solving Triple-Lens-only), existing agent .md files (no nav tables), existing skill directories (PLAYBOOK.md ×4, docs/ ×4, composition/ ×13 — all precedented, so no structure finding), and allowed-tools conventions (mixed: 4 skills include Agent, 3 omit it).
- **Not verified (out of scope or unverifiable from the repo):** whether the QG-E4 "3/3 catch rate" run occurred as described (the results file exists; its content was not audited here — the fixture-vs-rules `.md`/`.yaml` contradiction in F-2 is noted as bearing on it); agent-definition internals (H-34/H-35) — separate agent audit; runtime enforcement semantics of `allowed-tools` in the Claude Code loader (F-9 is framed conditionally for this reason).
- **Claims I could not confirm:** existence of any H-36 governance ruling or the `TASK-0039-H36-RULING` worktracker entity anywhere on the branch (searched; only self-reference found) — reported as absence of evidence in F-5.

---

*Audit artifact for PROJ-032 / EPIC-001 / FEAT-001 / STORY-001. Subject commit: bda64202. Standards: current worktree at time of audit (2026-08-07).*
