# C4 Adversarial Tournament Execution Plan — BUG-010 Containment Widening

> **Deliverable:** `jerry ast` path-containment widening + 2 security hardening fixes (H-01 ownership gate, H-02/H-08 broad-root warning gap closure)
> **Criticality:** C4 (Critical) — Irreversible security-relevant change, public-facing CLI surface, shipping in PR #341
> **Auto-escalation applied:** AE-005 (security-relevant code) → C4
> **Tournament scope:** All 10 selected adversarial strategies (S-001 through S-014), ordered per H-16 (Steelman before Devil's Advocate) and the 6-group execution model
> **Executor model:** Each strategy runs as a blind background agent (fresh context, no prior strategy outputs), groups run sequentially, strategies within groups run in parallel
> **Quality gate:** >= 0.92 composite score per S-014 LLM-as-Judge with 6-dimension rubric (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Criticality Assessment](#criticality-assessment) | Requested vs. auto-escalated level, final C4 assignment, AE-005 rule trigger |
| [Tournament Overview](#tournament-overview) | 6-group structure, sequential/parallel batching, blind-agent model |
| [Execution Plan by Group](#execution-plan-by-group) | Groups A–F with ordered strategy list, per-strategy lens, executor agent, template path |
| [Strategy Execution Sequences](#strategy-execution-sequences) | Detailed per-group execution (which run together, which wait for prior group completion) |
| [Success Criteria](#success-criteria) | Quality gate threshold, artifact persistence, orchestrator handoff |

---

## Criticality Assessment

| Assessment | Finding |
|---|---|
| **Requested criticality level** | C4 (explicitly stated by owner: "C4 adversarial tournament... before it ships") |
| **Auto-escalation rules applied** | AE-005 (security-relevant code) — the `jerry ast` path-containment widening involves filesystem access control logic, symlink resolution, ownership verification, and privilege boundaries; multiple CWE references (CWE-22, CWE-59, CWE-552, CWE-668, CWE-281, CWE-367, CWE-377, CWE-1284); active red-team engagement RED-BUG010 produced 2 CONFIRMED security findings (H-01 multi-user temp exposure, H-02/H-08 broad-root warning gaps) warranting comprehensive adversarial review before merge. |
| **Auto-escalation verdict** | ✓ AE-005 triggered — escalates to C4 minimum |
| **Final criticality level** | **C4** (no change from requested; AE-005 confirms C4 assignment) |
| **Strategy set** | All 10 selected strategies required per SSOT quality-enforcement.md C4 row: {S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014} |
| **H-16 constraint** | S-003 (Steelman, Group B) must precede S-002 (Devil's Advocate, Group C) — satisfied by group ordering. ✓ |

---

## Tournament Overview

**Execution model (per user memory feedback):** Each adversarial strategy executes as a blind background agent with fresh context, receiving only the deliverable path and the strategy-specific lens. Agents receive no output from prior strategies, preventing confirmation bias and anchoring. Groups run sequentially (barrier-sync between groups); strategies within each group run in parallel (fan-out/fan-in within the group).

**Group structure:**

```
TIME ──→

[GROUP A: Self-Refine]  ──→  [GROUP B: Steelman]  ──→  [GROUP C: Challenge]  ──→  [GROUP D: Verify]  ──→  [GROUP E: Decompose]  ──→  [GROUP F: Score]
      S-010                      S-003                 (S-002, S-004, S-001)       (S-007, S-011)        (S-012, S-013)              S-014
      solo                       solo              (parallel within group)     (parallel within group) (parallel within group)      solo
```

**Per-strategy executor agents:** Each strategy is assigned a blind executor from the `/adversary` skill agent roster (adv-executor or equivalent). The executor receives:
1. Deliverable path: `/Users/adam.nowak/workspace/GitHub/geekatron/jerry-wt/feat/proj-024-tactical-work-6/`
2. Branch: `fix/BUG-010-ast-project-root`
3. Strategy-specific lens (one question/focus area per strategy, listed below)
4. No prior strategy outputs; no knowledge of red-team findings (except: adversary-scorer will receive red-team findings for quality comparison in S-014)

---

## Execution Plan by Group

### GROUP A: Self-Refine (Solo)

Runs first. Self-review cycle to catch obvious defects before external challenge.

| Order | Strategy ID | Strategy Name | Template Path | Executor Agent | Lens (Research Question) | Intended Outcome |
|-------|---|---|---|---|---|---|
| 1 | S-010 | Self-Refine | `.context/templates/adversarial/s-010-self-refine.md` | adv-executor (blind) | **How robust is the ownership-gate design under the two remediation patterns proposed (H-01 POSIX UID check + Windows `os.name` gate)?** Are there gaps in the scoping rules (e.g., does the H-01 gate *only* apply to temp-default matches, or could it accidentally reject an intentional project-root file)? Does the docstring policy text accurately reflect user-discretion boundaries? | Self-identified defects in structure, scope, or clarity before Group B strengthening. Confidence in the core design assumptions. |

**Rationale:** H-01 ownership gate is the highest-leverage remediation; S-010 must verify the basic architecture is sound before S-003 defends it and S-002 attacks it.

---

### GROUP B: Steelman (Solo)

Runs after Group A completion. Strengthens the design by finding the *strongest* technical case for why the widening is sound.

| Order | Strategy ID | Strategy Name | Template Path | Executor Agent | Lens (Research Question) | Intended Outcome |
|-------|---|---|---|---|---|---|
| 2 | S-003 | Steelman Technique | `.context/templates/adversarial/s-003-steelman.md` | adv-executor (blind) | **What is the most coherent, technically-sound argument for why the default-root widening (project + temps + /tmp) is actually the *right* design choice, not a risky compromise?** Can you construct a model where the three roots form a principled set, each with a distinct justification? What aspects of the ownership-gate remediation make the widening *safer* than it appears on first reading? | Articulated strengths of the design that the devil's advocate (S-002) and other challenge strategies can target. Clarity on what assumptions hold and why. |

**Rationale:** H-16 requires Steelman before Devil's Advocate. By finding the strongest case for the widening, we prevent premature rejection and identify the core assumptions that downstream strategies should probe.

---

### GROUP C: Challenge (Parallel within group)

Runs after Group B completion. Three attack strategies execute in parallel, each targeting different angles.

#### C.1 — S-002 Devil's Advocate

| Order | Strategy ID | Strategy Name | Template Path | Executor Agent | Lens (Research Question) | Intended Outcome |
|-------|---|---|---|---|---|---|
| 3a | S-002 | Devil's Advocate | `.context/templates/adversarial/s-002-devils-advocate.md` | adv-executor (blind) | **Does the "exclusive override" semantics of `--root` really provide user-discretion protection, or does it hide complexity that will bite users?** If a user runs `jerry ast parse /tmp/file.md --root /home/user`, they've explicitly approved `/home/user` — but the project root is now *excluded*. Is this counterintuitive enough to cause accidental misuse? Does the error message when a project-root file is rejected under `--root /elsewhere` clearly explain *why* it failed? | Identified cognitive gaps, UX confusion, or documented assumptions that don't hold up under scrutiny. |

**Rationale:** Red-team focused on code; S-002 focuses on user-intent and cognitive load. The exclusive override is a subtle design choice that could trap users.

#### C.2 — S-004 Pre-Mortem Analysis

| Order | Strategy ID | Strategy Name | Template Path | Executor Agent | Lens (Research Question) | Intended Outcome |
|-------|---|---|---|---|---|---|
| 3b | S-004 | Pre-Mortem Analysis | `.context/templates/adversarial/s-004-pre-mortem.md` | adv-executor (blind) | **Assume this ships and a security incident occurs 6 months later on a shared CI/build host where Jerry runs under a shared `/tmp`.** What is the most likely failure mode? Is it H-01 (ownership gate bypassed somehow), or H-02 (user runs `--root /home` thinking it's a reasonable choice and gets a false sense of security from the lack of warning)? Which remediation failure would cause the most damage? | Identified highest-RPN risks, remediation brittleness, or assumptions most likely to fail in production. |

**Rationale:** Pre-mortem surfaces second-order effects and deployment-model dependencies that static code review might miss. The H-01/H-02 findings from red-team are specific; S-004 should probe if there are *other* likely failure modes.

#### C.3 — S-001 Red Team Analysis

| Order | Strategy ID | Strategy Name | Template Path | Executor Agent | Lens (Research Question) | Intended Outcome |
|-------|---|---|---|---|---|---|
| 3c | S-001 | Red Team Analysis | `.context/templates/adversarial/s-001-red-team.md` | adv-executor (blind) | **The red-team engagement (RED-BUG010) found 2 CONFIRMED vulnerabilities (H-01 ownership gate gap, H-02 broad-root warning coverage gap) and 8 REFUTED safe findings.** From a red-team perspective: (1) Are the two remediations truly *complete*, or are they partial patches for deeper architectural issues? (2) Could an attacker chain H-01 + H-02 together (temp write + missing warning on broad `--root`) to construct a more severe scenario than either alone? (3) What's the interaction between the `--root /tmp` case and the scoped H-01 gate? | Adversarial perspective on remediation completeness, exploit-chaining potential, and residual gaps in the combined fix. |

**Rationale:** S-001 is a second pass on red-team findings. The first pass was thorough, but S-001 can probe whether the *remediations* themselves introduce new attack surfaces or incomplete closures.

**H-16 satisfaction:** S-003 (Steelman, Group B) completes before any of C.1/C.2/C.3 begin. ✓

---

### GROUP D: Verify (Parallel within group)

Runs after Group C completion. Two verification strategies trace assumptions end-to-end.

#### D.1 — S-007 Constitutional AI Critique

| Order | Strategy ID | Strategy Name | Template Path | Executor Agent | Lens (Research Question) | Intended Outcome |
|-------|---|---|---|---|---|---|
| 4a | S-007 | Constitutional AI Critique | `.context/templates/adversarial/s-007-constitutional-ai.md` | adv-executor (blind) | **Does this change respect the Jerry constitution and the owner's stated governance principles?** The owner said "reasonable best effort, not a hard boundary, user discretion" — the `--root` flag operationalizes that, but the H-01 ownership gate (checking `st_uid == os.geteuid()`) is a *restriction* even on temp-default roots. Is that consistent with the "user discretion" framing, or does it silently enforce an additional policy the owner didn't explicitly endorse? Does the narrow scoping of the H-01 gate (temp-default-root-only, never project-root-only, never explicit-`--root`) align with the documented user-discretion boundaries? | Governance alignment assessment, policy consistency, transparency of implicit restrictions, alignment with documented user-discretion model. |

**Rationale:** The two remediations (H-01 + H-02) are *constraints* that reduce surface area. S-007 verifies these constraints are legitimate under the constitutional model.

#### D.2 — S-011 Chain-of-Verification (COVE)

| Order | Strategy ID | Strategy Name | Template Path | Executor Agent | Lens (Research Question) | Intended Outcome |
|-------|---|---|---|---|---|---|
| 4b | S-011 | Chain-of-Verification | `.context/templates/adversarial/s-011-cove.md` | adv-executor (blind) | **Trace the security assumptions end-to-end: assume `CLAUDE_PROJECT_DIR` is set correctly, `tempfile.gettempdir()` resolves correctly, `/tmp` existence is checked correctly, the `--root` value is resolved correctly.** Now construct a counter-example: (1) What if `CLAUDE_PROJECT_DIR` contains a symlink to `/tmp`? Does the deduplication in `get_containment_roots` handle that? (2) What if `tempfile.gettempdir()` returns a path under `/tmp`, or vice versa? (3) What if a user hardlinks a file from outside the project into a temp directory? | End-to-end assumption tracing, counter-examples, deduplication edge cases, symlink-in-the-root-path scenarios. |

**Rationale:** S-011 is defensive verification. It assumes the design is sound and looks for subtle edge cases that could make it unsound — counter-examples to stated assumptions.

---

### GROUP E: Decompose (Parallel within group)

Runs after Group D completion. Two decomposition strategies break the design into failure modes.

#### E.1 — S-012 FMEA (Failure Mode and Effects Analysis)

| Order | Strategy ID | Strategy Name | Template Path | Executor Agent | Lens (Research Question) | Intended Outcome |
|-------|---|---|---|---|---|---|
| 5a | S-012 | FMEA | `.context/templates/adversarial/s-012-fmea.md` | adv-executor (blind) | **Systematically enumerate failure modes for both remediations (H-01 ownership gate + H-02 broad-root warning):**(1) **H-01 failures:** (a) `os.stat().st_uid` call raises `OSError` (file disappears mid-check, TOCTOU race) — is the `pass` exception handler the right behavior, or should it fail-closed? (b) `os.geteuid()` behavior on a container where all files are owned by UID 0 — does the gate reject all temp files? (c) Windows `os.name != "nt"` branch — is there a fallback on Windows if `tempfile.gettempdir()` returns a cross-tenant path? (2) **H-02 failures:** (a) `Path.home()` raises `RuntimeError` in some CI runners — does `_is_broad_containment_root` fail-closed? (b) The `.relative_to()` check for ancestor-of-home — does it handle symlinked home directories? (c) Does the Windows UNC-subpath case (`\\host\share\sub`) get covered by the `.relative_to()` logic, or is it a residual gap? | Ranked failure modes by severity + likelihood, especially TOCTOU races, exception handling, and cross-platform edge cases. |

**Rationale:** S-012 is systematic risk enumeration. Both remediations have exception handlers and edge cases; FMEA surfaces which ones are highest-risk.

#### E.2 — S-013 Inversion Technique

| Order | Strategy ID | Strategy Name | Template Path | Executor Agent | Lens (Research Question) | Intended Outcome |
|-------|---|---|---|---|---|---|
| 5b | S-013 | Inversion Technique | `.context/templates/adversarial/s-013-inversion.md` | adv-executor (blind) | **Invert the design: what if the three default roots were *rejected* and users had to use `--root` for *everything* (even the project root)?** What problems would that solve? (a) Eliminates H-01 multi-user exposure in one swoop — no implicit temp permission. (b) Forces explicit opt-in, making the user intent crystal-clear. (c) Simplifies testing and auditing — no implicit defaults. What problems would it *create*? (a) Breaking change to existing scripts that do `jerry ast parse file.md`. (b) Worse UX — Claude scratchpad files would require a `--root` flag. (c) Reduces "best effort" to "zero effort on defaults." Now, given that inversion is unacceptable (breaks usability), what aspects of the current design are *required* to make the default-root widening acceptable? | Inverted-design analysis revealing which design choices are *essential* vs. *contingent*, and whether the current remediations address the essential risks. |

**Rationale:** S-013 surfaces design *trade-offs* by considering the opposite approach. This clarifies which risks are inherent to the widening vs. mitigatable via remediations.

---

### GROUP F: Score (Solo)

Runs after Group E completion. Comprehensive quality assessment against the 6-dimension rubric.

| Order | Strategy ID | Strategy Name | Template Path | Executor Agent | Lens (Research Question) | Intended Outcome |
|-------|---|---|---|---|---|---|
| 6 | S-014 | LLM-as-Judge | `.context/templates/adversarial/s-014-llm-as-judge.md` | adv-scorer (blind) | **Comprehensive quality scoring against the 6-dimension rubric (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability).** Score the entire deliverable (bug report + eng-lead plan + red-team findings + proposed remediations) as a unified artifact. Specific lens: (1) **Completeness** — does it address all 10 acceptance criteria in BUG-010.md? Are the two remediations (H-01 + H-02) fully specified, not partial sketches? (2) **Internal Consistency** — do the eng-lead plan's scope and the red-team findings agree on the threat model? Are the remediation code sketches consistent with the test plan? (3) **Methodological Rigor** — is the red-team assessment (PTES + NIST 800-115 + white-box review) sufficiently rigorous for a C4 security change? (4) **Evidence Quality** — are the two CONFIRMED findings backed by executed reproductions (not just code reasoning)? Are the 8 REFUTED findings backed by active verification, not assumption? (5) **Actionability** — can eng-backend implement both remediations from the red-team evidence and the code sketches without ambiguity? Are open decisions (R-3: broad-root warning policy, R-4: temp-match transparency note) clearly flagged for user review? (6) **Traceability** — can a reviewer connect every AC back to evidence (red-team verdict, eng-lead plan section, remediation code)? | Composite quality score (0.0–1.0, normalized to 0–100), dimension-level scores, gap analysis, actionability assessment. |

**Rationale:** S-014 is the final quality gate. It synthesizes all prior adversarial strategies and assesses whether the deliverable meets the C4 standard (>= 0.92 composite).

---

## Strategy Execution Sequences

### Sequential Group Execution (Barrier-Sync Between Groups)

```
Start: Group A (S-010) ─────→ Complete
       ↓
Wait: All GROUP A strategies finish
       ↓
Start: Group B (S-003) ─────→ Complete
       ↓
Wait: All GROUP B strategies finish
       ↓
Start: Group C (S-002, S-004, S-001) ──[parallel within group]──→ Complete
       ↓
Wait: All GROUP C strategies finish (all 3 complete before next group starts)
       ↓
Start: Group D (S-007, S-011) ──[parallel within group]──→ Complete
       ↓
Wait: All GROUP D strategies finish
       ↓
Start: Group E (S-012, S-013) ──[parallel within group]──→ Complete
       ↓
Wait: All GROUP E strategies finish
       ↓
Start: Group F (S-014) ─────→ Complete (score all priors)
       ↓
End: Tournament complete, quality gate checked, results persisted
```

### Parallel Execution Within Groups

**Group C (Challenge):** S-002, S-004, S-001 run in parallel, each blind to the others' outputs.
- Orchestrator fans out 3 adv-executor agents, one per strategy, each receiving only the lens and deliverable path.
- Orchestrator waits for all 3 to complete (barrier-sync).
- No cross-feedback; no strategy sees another's findings during execution.

**Group D (Verify):** S-007, S-011 run in parallel.
- Same pattern: fan-out 2 agents, barrier-sync completion.

**Group E (Decompose):** S-012, S-013 run in parallel.
- Same pattern: fan-out 2 agents, barrier-sync completion.

---

## Success Criteria

| Criterion | Condition | Validation |
|---|---|---|
| **All 10 strategies executed** | Every strategy (S-001 through S-014) produces a report artifact (markdown or equivalent). | Orchestrator collects 10 reports. |
| **H-16 constraint satisfied** | S-003 (Steelman) completes before S-002 (Devil's Advocate) begins. | Group B finishes before Group C starts (barrier-sync enforces this). ✓ |
| **Blind-agent model honored** | Each strategy agent receives no output from prior strategies, only the deliverable path and lens. No confirmation bias via sequential exposure to prior findings. | Executor agents are invoked with `--no-prior-outputs` equivalent, no access to prior reports during execution. |
| **Quality gate passed** | S-014 LLM-as-Judge produces a composite score >= 0.92 (C4 standard, per quality-enforcement.md). | Scorer reports `composite_score >= 0.92` or `status: REJECTED` with dimension breakdowns. |
| **Artifacts persisted** | All 10 strategy reports and the tournament summary persisted to `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/BUG-010-ast-project-root/`. | Files exist and are commit-ready (P-002: File Persistence). |
| **Orchestrator handoff** | Tournament summary (this plan + executive summary of all 10 findings + quality gate result) handed off to orchestrator with a clear "APPROVED for merge" or "BLOCKED pending revision" verdict. | Orchestrator receives a structured handoff with criticality, verdict, and next-step guidance. |

---

## Orchestrator Handoff Template

After all 6 groups complete, the tournament produces a structured handoff:

```markdown
## TOURNAMENT RESULTS — BUG-010 Containment Widening (C4)

### Overall Quality Score
- **Composite (S-014):** [score] / 1.0 (target >= 0.92)
- **Status:** PASS or FAIL

### Dimension Scores (S-014 Rubric)
- Completeness: [score]
- Internal Consistency: [score]
- Methodological Rigor: [score]
- Evidence Quality: [score]
- Actionability: [score]
- Traceability: [score]

### Key Findings by Strategy
- **Group A (S-010 Self-Refine):** [top finding]
- **Group B (S-003 Steelman):** [top finding]
- **Group C Challenge:**
  - S-002 Devil's Advocate: [top finding]
  - S-004 Pre-Mortem: [top finding]
  - S-001 Red Team: [top finding]
- **Group D Verify:**
  - S-007 Constitutional AI: [top finding]
  - S-011 COVE: [top finding]
- **Group E Decompose:**
  - S-012 FMEA: [top finding]
  - S-013 Inversion: [top finding]

### Final Verdict
**APPROVED for merge** ✓ [if score >= 0.92] or **BLOCKED, revision required** ✗ [if score < 0.92, with remediation guidance]

### Orchestrator Next Steps
1. Route to eng-backend (if APPROVED) with tournament summary as quality gate evidence.
2. Route to user/PR owner (if BLOCKED) with specific remediation guidance from lowest-scoring dimension.
```

---

## References

| Document | Location |
|---|---|
| Criticality Levels SSOT | `.context/rules/quality-enforcement.md` [Criticality Levels] |
| Strategy Catalog | `.context/rules/quality-enforcement.md` [Strategy Catalog] |
| H-16 Ordering Constraint | `.context/rules/quality-enforcement.md` [Ordering Rules], [H-16 Constraint] |
| Template Paths | `.context/rules/quality-enforcement.md` [Template Paths] |
| BUG-010 Scope | `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/BUG-010-ast-project-root/BUG-010-ast-project-root.md` |
| Engineering Plan | `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/BUG-010-ast-project-root/eng-lead-implementation-plan.md` |
| Red-Team Scope | `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/BUG-010-ast-project-root/red-lead-scope-and-attack-plan.md` |
| Red-Team Findings | `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/BUG-010-ast-project-root/red-vuln-findings.md` |

---

*adv-selector v1.0.0 — C4 Strategy Selection. All 10 strategies mapped per SSOT. H-16 satisfied. 6-group execution model specified. Tournament ready for orchestrator dispatch.*
