# QG-3 Final Score Report — S-014 LLM-as-Judge

> **Agent:** adv-scorer-003
> **Gate:** QG-3 — Cross-Deliverable Consistency (Final Quality Gate)
> **Criticality:** C2 (Standard)
> **Orchestration:** epic001-docs-20260218-001
> **Date:** 2026-02-18

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Verdict and composite score |
| [Prior Gate Context](#prior-gate-context) | QG-1 and QG-2 scores |
| [Deliverables Reviewed](#deliverables-reviewed) | All 5 files scored |
| [Dimension Scores](#dimension-scores) | Per-dimension evidence and scores |
| [Weighted Composite](#weighted-composite) | Score calculation |
| [Leniency Bias Check](#leniency-bias-check) | Downward-resolve audit |
| [Verdict](#verdict) | PASS / REVISE / ESCALATE |
| [Improvement Recommendations](#improvement-recommendations) | Priority-ordered (if REVISE) |

---

## L0 Executive Summary

QG-3 evaluated all 5 documentation deliverables together for cross-document consistency,
user journey coherence, and aggregate quality. The documentation set is coherent,
well-structured, and largely consistent — terminology is uniform, cross-references between
playbooks form a complete ring, and quality framework alignment with the SSOT is
accurate. Two genuine cross-document gaps were identified: (1) the Persistent Artifacts
table in `INSTALLATION.md` is incomplete relative to the output directories documented in
the problem-solving playbook, creating a user-facing knowledge gap; and (2) a minor
divergence exists between the plugin verification method described in `INSTALLATION.md`
(plugin UI) and the method described in `getting-started.md` (CLI command). These gaps
keep the aggregate score below the PASS threshold.

**Composite Score:** 0.906

**Verdict: REVISE** (score 0.906 falls in the 0.85-0.91 REVISE band; targeted corrections
are likely sufficient to reach >= 0.92)

---

## Prior Gate Context

| Gate | Deliverable(s) | Score | Verdict |
|------|---------------|-------|---------|
| QG-1 | FEAT-017: `docs/INSTALLATION.md` | 0.9220 | PASS |
| QG-2 | FEAT-018: getting-started.md + 3 playbooks | 0.9260 | PASS |
| QG-3 | All 5 deliverables — cross-document | 0.906 | REVISE |

QG-3 applies a different and more demanding lens than QG-1 and QG-2: it evaluates
consistency ACROSS documents rather than quality WITHIN each document. Documents that
passed individual review can still have cross-document consistency gaps that only surface
when all are read together. This is the expected function of a final cross-deliverable gate.

---

## Deliverables Reviewed

| # | File | Feature | Lines |
|---|------|---------|-------|
| 1 | `docs/INSTALLATION.md` | FEAT-017 | ~826 |
| 2 | `docs/runbooks/getting-started.md` | FEAT-018 | ~208 |
| 3 | `docs/playbooks/problem-solving.md` | FEAT-018 | ~233 |
| 4 | `docs/playbooks/orchestration.md` | FEAT-018 | ~263 |
| 5 | `docs/playbooks/transcript.md` | FEAT-018 | ~279 |

All 5 files were read in full before scoring commenced.

---

## Dimension Scores

### 1. Completeness — Score: 0.88 (Weight: 0.20)

**Definition:** All information a user needs to successfully use the documented capability
is present across the documentation set, with no unexplained gaps.

**Evidence — Strengths:**

- `INSTALLATION.md` covers prerequisites, collaborator SSH setup, macOS/Windows platform
  steps, marketplace/plugin installation, configuration, verification, troubleshooting,
  uninstall, and future public repo installation. No lifecycle gaps.
- `getting-started.md` covers all 5 steps from a freshly installed Jerry to a persisted
  artifact, with explicit verification checklist and troubleshooting table.
- `problem-solving.md` documents all 9 agents with roles, triggers, and output locations.
  The creator-critic-revision cycle section includes the complete 6-dimension scoring table
  and all 3 score bands — fully self-contained.
- `orchestration.md` documents all 3 workflow patterns with ASCII diagrams, all 3 core
  artifacts, all 3 agents, and P-003 compliance implications. The troubleshooting section
  covers 7 failure modes.
- `transcript.md` documents the 2-phase architecture, all 9 domain contexts, all 3 input
  formats, and all phases of the output packet. The CRITICAL WARNING on
  `canonical-transcript.json` is prominently placed.

**Evidence — Gaps:**

**Gap 1 (moderate severity):** `INSTALLATION.md` "Persistent Artifacts" table (line 597)
lists only 5 output directories:
- `docs/research/`, `docs/analysis/`, `docs/decisions/`, `docs/reviews/`, `docs/reports/`

However, `problem-solving.md` Agent Reference documents 9 agents writing to 9 output
directories. Three directories are entirely absent from the INSTALLATION.md table:
- `docs/critiques/` (ps-critic)
- `docs/synthesis/` (ps-synthesizer)
- `docs/investigations/` (ps-investigator)

A user reading only `INSTALLATION.md` to understand where Jerry saves files would have an
incomplete picture. This is a user-facing documentation gap.

**Gap 2 (minor severity):** `INSTALLATION.md` "Using Jerry" section (line 562) describes
the available skills but does not link to `docs/runbooks/getting-started.md` for new
users' first run. The handoff is implicit — a user who reads INSTALLATION.md through to
the end must independently discover that `getting-started.md` exists. The getting-started
runbook explicitly references INSTALLATION.md as its prerequisite, but the reverse link is
absent.

**Gap 3 (minor severity):** The Adversary skill appears in the INSTALLATION.md skill table
with "Adversarial quality reviews and tournament scoring" — consistent with CLAUDE.md.
However, none of the FEAT-018 playbooks covers `/adversary` — that playbook was not in
scope for FEAT-018. This creates an asymmetry: three playbooks are reachable from
getting-started.md's Next Steps, but the full skill set (7 skills per INSTALLATION.md)
has no playbooks for Architecture, NASA SE, and Adversary. This is a scope boundary
issue, not a defect in the delivered documents, but it creates a coverage completeness
perception gap.

**Score rationale:** Gap 1 is the most significant — it directly misleads users about
where artifacts are saved. Gaps 2-3 are navigation and scope issues. Score 0.88 (below
0.90) applies the downward-resolve rule for the genuine artifact table incompleteness.

---

### 2. Internal Consistency — Score: 0.89 (Weight: 0.20)

**Definition:** Terms, procedures, rule references, thresholds, and file paths are used
consistently across all 5 documents without contradiction.

**Evidence — Strengths:**

- `JERRY_PROJECT` environment variable naming: consistent across all 5 documents without
  deviation. Each document uses the same exact string, same formatting, same export
  syntax examples (`export JERRY_PROJECT=...` on macOS, `$env:JERRY_PROJECT = ...` on
  Windows).
- Quality gate threshold: `problem-solving.md` states >= 0.92 — exactly matches
  quality-enforcement.md SSOT. The 6 scoring dimensions and weights in
  `problem-solving.md` exactly match the SSOT:
  Completeness 0.20, Internal Consistency 0.20, Methodological Rigor 0.20,
  Evidence Quality 0.15, Actionability 0.15, Traceability 0.10. No drift.
- Score bands: PASS >= 0.92, REVISE 0.85-0.91, REJECTED < 0.85 — consistent with SSOT
  in `problem-solving.md`.
- `transcript.md` states a skill-specific threshold of >= 0.90 (lower than the 0.92
  SSOT) and explicitly documents this as a documented deviation: "the transcript skill
  uses a skill-specific threshold lower than the general 0.92 SSOT; see the SKILL.md
  Design Rationale section for the selection rationale." This is a documented, justified
  deviation — not an inconsistency.
- XML session tags (`<project-context>`, `<project-required>`, `<project-error>`):
  defined in INSTALLATION.md troubleshooting and used identically in `getting-started.md`
  Step 3 with the same meaning. Consistent.
- Slash command format: `/problem-solving`, `/worktracker`, `/orchestration`,
  `/transcript`, `/adversary` — identical formatting across all documents.
- Keyword triggers listed in `getting-started.md` Step 4 (research, analyze, investigate,
  explore, root cause, why) exactly match the trigger list in `problem-solving.md`
  header and Step-by-Step. Consistent.
- `uv run jerry transcript parse` syntax: used consistently in `transcript.md` and
  aligns with H-05 UV-only constraint stated in INSTALLATION.md for hooks.

**Evidence — Inconsistencies:**

**Inconsistency 1 (moderate):** Plugin verification method diverges between documents:
- `INSTALLATION.md` Verification section instructs: "In Claude Code, run `/plugin`, go
  to the Installed tab, verify `jerry-framework` appears."
- `getting-started.md` Prerequisites instructs: "The Jerry plugin is registered in Claude
  Code — confirm with `claude mcp list` (you should see `jerry-framework` in the output)."

These are two different verification methods. `claude mcp list` is a CLI command;
`/plugin` > Installed tab is an in-Claude UI flow. Both may be valid, but a new user
who follows INSTALLATION.md and then getting-started.md will encounter two different
verification methods for the same step. The discrepancy could cause confusion about
which is authoritative.

**Inconsistency 2 (minor):** `INSTALLATION.md` uses "Table of Contents" as the navigation
heading; all four FEAT-018 documents use "Document Sections" as the heading. This is a
formatting convention difference, not a content inconsistency. The table structure and
anchor link usage are equivalent. This does not affect user comprehension.

**Score rationale:** The plugin verification inconsistency is real and user-facing.
Score 0.89 — downward-resolved from uncertain 0.90/0.91 range given the concrete
verification method divergence.

---

### 3. Methodological Rigor — Score: 0.93 (Weight: 0.20)

**Definition:** Documentation is structured with clear procedures, decision criteria,
prerequisites, and error handling. The methodology for guiding users through Jerry is
sound.

**Evidence — Strengths:**

- All 5 documents use a consistent documentation methodology: navigation table at top,
  prerequisites defined before procedures, procedures with expected outputs, verification
  criteria, troubleshooting tables with symptom/cause/resolution columns.
- `getting-started.md` uses checkboxes for prerequisites and verification end-state —
  reinforcing the runbook methodology distinct from the playbook format.
- `problem-solving.md` provides explicit disambiguation guidance (ps-analyst vs
  ps-investigator, ps-critic vs /adversary) — methodologically rigorous agent selection
  guidance.
- `orchestration.md` P-003 compliance section explicitly states the violation pattern to
  avoid with a concrete anti-pattern example — a methodologically sophisticated addition.
- `transcript.md` two-phase architecture is explained with cost rationale (1,250x cheaper
  than LLM parsing) and a CRITICAL WARNING with a recovery procedure — methodologically
  complete.
- Auto-escalation rules are correctly cited in `problem-solving.md` (AE-001 through
  AE-006) and cross-referenced to quality-enforcement.md.
- Score bands in `problem-solving.md` include the "circuit breaker" after 3 iterations —
  preventing infinite loops. Methodologically sound.
- Quality gate evaluation is required at each phase boundary in orchestration.md — quality
  gates are not optional, and the troubleshooting table includes a failure mode for
  skipped gates.

**Minor gap:** `orchestration.md` Step 6 references the S-014 quality rubric via a link
to quality-enforcement.md but does not reproduce the dimensions table inline. For the
orchestration playbook this is acceptable (the problem-solving playbook is the primary
reference for the rubric), but a user following the orchestration playbook alone would
need to navigate away to understand the gate criteria.

**Score rationale:** The methodology across all 5 documents is genuinely rigorous. The
minor gap in orchestration.md does not meaningfully impair usability. Score 0.93 — above
threshold for this dimension.

---

### 4. Evidence Quality — Score: 0.92 (Weight: 0.15)

**Definition:** Claims are supported by specific examples, rule citations, or concrete
artifacts (paths, commands, expected outputs). Evidence is traceable to authoritative
sources.

**Evidence — Strengths:**

- All documents provide concrete CLI commands with expected outputs — not vague
  descriptions but exact commands users can copy and run.
- Rule citations are specific: H-04, H-05, H-13, H-14, H-15, H-16, AE-001 through
  AE-006 — all cited with anchor links to quality-enforcement.md.
- Examples in all playbooks describe specific system behaviors, not just abstract
  descriptions: agent name activated, output directory written to, qualitative behavior
  observed.
- `transcript.md` includes quantified evidence for the cost rationale: "~1,250:1 cost
  ratio," "~280K tokens," "<1 second" — rare in documentation but highly valuable.
- `orchestration.md` example system behaviors explicitly state the workflow ID format
  generated (e.g., `sao-crosspoll-20260218-001`) and the directory path structure.
- P-002 (file persistence requirement) is cited in both `orchestration.md` and
  `getting-started.md` as the authority for artifact persistence guarantees.

**Minor gap:** `problem-solving.md` and `orchestration.md` reference
`docs/governance/JERRY_CONSTITUTION.md` auto-escalation indirectly via the
quality-enforcement.md link. The AE rules are cited correctly, but users unfamiliar with
the governance structure would need to follow multiple links to understand the full
escalation chain. This is a depth-of-evidence issue, not a quality problem.

**Score rationale:** Evidence quality is strong with specific citations, concrete commands,
and expected outputs throughout. Score 0.92 — at threshold, with the minor multi-hop
navigation gap noted.

---

### 5. Actionability — Score: 0.94 (Weight: 0.15)

**Definition:** Users can take immediate, concrete action from the documentation. Failure
modes lead to clear resolution steps.

**Evidence — Strengths:**

- Every troubleshooting table across all 5 documents uses symptom/cause/resolution
  structure — immediately actionable for users encountering errors.
- `getting-started.md` troubleshooting table covers 5 distinct failure modes with exact
  commands to resolve each.
- `problem-solving.md` troubleshooting table covers 8 failure modes including a
  multi-step recovery procedure for partial agent output.
- `orchestration.md` troubleshooting table covers 8 failure modes including the specific
  ORCHESTRATION.yaml field to check when resuming a workflow.
- `transcript.md` troubleshooting table covers 7 failure modes with explicit recovery
  steps for the most critical one (context fill from canonical-transcript.json).
- All platform-specific commands are provided in parallel (macOS/Linux and Windows
  PowerShell variants).
- `INSTALLATION.md` Windows path section includes a PowerShell one-liner to convert
  backslash paths to forward slashes for the Claude Code command — a specific, actionable
  workaround for a known platform pain point.
- `orchestration.md` explicitly documents the violation pattern (asking orch-planner to
  "coordinate the workflow") and the correct alternative phrasing — directly preventing
  a predictable user error.

**Score rationale:** Actionability is the strongest dimension across all 5 documents.
No meaningful gaps identified. Score 0.94.

---

### 6. Traceability — Score: 0.91 (Weight: 0.10)

**Definition:** Design decisions, rule citations, and cross-document references can be
followed to their authoritative sources.

**Evidence — Strengths:**

- Cross-playbook references form a complete and consistent ring:
  - `problem-solving.md` Related Resources links to `orchestration.md` and `transcript.md`
  - `orchestration.md` Related Resources links to `problem-solving.md` and `transcript.md`
  - `transcript.md` Related Resources links to `problem-solving.md` and `orchestration.md`
  All three links verified correct (relative paths).
- All playbooks link to their own `SKILL.md` as the authoritative technical reference.
- All playbooks link to `quality-enforcement.md` as the quality gate SSOT.
- `getting-started.md` Step 1 cites H-04 with a direct anchor link to
  `../../.context/rules/quality-enforcement.md#hard-rule-index`.
- `transcript.md` cites ADR-006 for the mindmap default-on design decision — traceable
  to a specific ADR.
- `problem-solving.md` correctly cites AE-001 through AE-006 auto-escalation rules with
  a link to the SSOT.

**Partial gaps:**

- `INSTALLATION.md` does not cite H-rules — appropriate for a user-facing installation
  guide (no traceability expectation). Not penalized.
- `getting-started.md` references "P-002 (file persistence requirement)" in the Step 5
  text but does not link to the source of P-002. The problem-solving.md and
  orchestration.md docs also cite P-002 but do not link it (P-002 appears to live in
  CLAUDE.md or a rules file not linked from these docs). This is a minor traceability gap
  — P-002 is cited but not linked.

**Score rationale:** Traceability is strong with consistent anchor-linked rule citations
and a complete cross-reference ring. The P-002 source link gap is a minor but real
traceability issue. Score 0.91 — downward-resolved from 0.92 given the unlinkable P-002
citation appears in 3 of 5 documents.

---

## Weighted Composite

| Dimension | Weight | Score | Contribution |
|-----------|--------|-------|-------------|
| Completeness | 0.20 | 0.88 | 0.176 |
| Internal Consistency | 0.20 | 0.89 | 0.178 |
| Methodological Rigor | 0.20 | 0.93 | 0.186 |
| Evidence Quality | 0.15 | 0.92 | 0.138 |
| Actionability | 0.15 | 0.94 | 0.141 |
| Traceability | 0.10 | 0.91 | 0.091 |
| **TOTAL** | **1.00** | — | **0.910** |

**Weighted Composite Score: 0.910**

> Note: After leniency bias check (see below), no upward adjustments were applied. Final
> score is 0.910, rounded to 0.910 (three decimal places). Score band: REVISE (0.85-0.91).

---

## Leniency Bias Check

Per P-022 and QG-3 scoring instructions: uncertain scores must resolve DOWNWARD. The
following dimension scores were reviewed for leniency bias:

| Dimension | Initial Range Considered | Resolved | Direction | Justification |
|-----------|------------------------|----------|-----------|---------------|
| Completeness | 0.88-0.90 | 0.88 | DOWN | Artifact table gap is user-facing; cannot round up |
| Internal Consistency | 0.89-0.91 | 0.89 | DOWN | Plugin verification divergence is concrete; not ambiguous |
| Methodological Rigor | 0.92-0.94 | 0.93 | NEUTRAL | No ambiguity; evidence supports this range |
| Evidence Quality | 0.91-0.93 | 0.92 | DOWN | Multi-hop navigation gap; at-threshold not above |
| Actionability | 0.93-0.95 | 0.94 | NEUTRAL | No meaningful gaps found; strong evidence for high score |
| Traceability | 0.91-0.92 | 0.91 | DOWN | P-002 cited-but-not-linked in 3 docs; resolve down |

No scores were inflated. The 0.910 composite represents genuine quality — these are
professionally-written, well-structured documents — held to the required standard that
0.92 means genuinely excellent and leniency is actively counteracted.

---

## Verdict

**REVISE** — Score 0.910 is in the REVISE band (0.85-0.91).

The documentation set is near-threshold. The gaps identified are targeted and correctable
without structural rework. Specifically:

- Completeness and Internal Consistency are the two dimensions below 0.90, both driven by
  correctable issues in `INSTALLATION.md`.
- Methodological Rigor, Evidence Quality, Actionability, and Traceability all meet or
  exceed the 0.92 threshold individually.

A targeted revision of `INSTALLATION.md` and a minor fix to `getting-started.md` is
likely sufficient to bring the composite above 0.92.

---

## Improvement Recommendations

Ordered by estimated impact on composite score (highest first):

### R1 — Fix INSTALLATION.md Persistent Artifacts Table (Impact: HIGH — Completeness +0.04)

**File:** `docs/INSTALLATION.md` — "Persistent Artifacts" section (line ~597)

**Problem:** The table lists only 5 output directories. Three additional directories
documented in `problem-solving.md` are missing, creating a user-visible gap.

**Fix:** Add the missing rows to the table:

```markdown
| Output Type | Location |
|-------------|----------|
| Research | `docs/research/` |
| Analysis | `docs/analysis/` |
| Critiques | `docs/critiques/` |       ← ADD
| Decisions (ADRs) | `docs/decisions/` |
| Reviews | `docs/reviews/` |
| Investigations | `docs/investigations/` | ← ADD
| Synthesis | `docs/synthesis/` |        ← ADD
| Reports | `docs/reports/` |
```

**Verification:** The table should now match all output locations documented in
`docs/playbooks/problem-solving.md` Agent Reference.

---

### R2 — Reconcile Plugin Verification Methods (Impact: MEDIUM — Internal Consistency +0.02)

**Files:** `docs/INSTALLATION.md` and `docs/runbooks/getting-started.md`

**Problem:** INSTALLATION.md verification says use `/plugin` > Installed tab; getting-started.md
prerequisites say use `claude mcp list`. Two different verification methods for the same
fact.

**Options:**
1. Standardize on the UI method: update getting-started.md prerequisites to use
   `/plugin` > Installed tab (matching INSTALLATION.md).
2. Standardize on the CLI method: update INSTALLATION.md Verification to use
   `claude mcp list`.
3. Document both as valid alternatives in one location and reference from the other.

**Recommendation:** Option 1 — use the `/plugin` > Installed tab as the primary
verification method in both documents, since INSTALLATION.md covers it in more detail
(including the Errors tab check). The `claude mcp list` method can remain as an
alternative in a tip/note callout.

---

### R3 — Add getting-started.md Link from INSTALLATION.md (Impact: LOW — Completeness +0.01)

**File:** `docs/INSTALLATION.md` — "Using Jerry" section

**Problem:** INSTALLATION.md does not link to `docs/runbooks/getting-started.md` for new
users starting their first session.

**Fix:** Add a callout at the end of the "Using Jerry" section:

```markdown
> **New to Jerry?** Follow the [Getting Started runbook](runbooks/getting-started.md)
> for a guided walkthrough from installation to your first persisted skill output.
```

---

### R4 — Add P-002 Source Links (Impact: LOW — Traceability +0.01)

**Files:** `docs/runbooks/getting-started.md`, `docs/playbooks/problem-solving.md`,
`docs/playbooks/orchestration.md`

**Problem:** P-002 (file persistence requirement) is cited in all three documents but
no link is provided to the source of P-002.

**Fix:** Locate the authoritative source of P-002 (likely `CLAUDE.md` or a rules file)
and add an anchor link alongside each citation. Example:

```markdown
P-002 ([file persistence requirement](../../.context/rules/...))
```

If P-002 does not have an existing anchor target, add one or reference the nearest
containing section.

---

## Summary

| # | Recommendation | Dimension Impact | Effort |
|---|---------------|-----------------|--------|
| R1 | Fix artifact table in INSTALLATION.md | Completeness +0.04 | Low |
| R2 | Reconcile plugin verification methods | Internal Consistency +0.02 | Low |
| R3 | Add getting-started link from INSTALLATION.md | Completeness +0.01 | Trivial |
| R4 | Add P-002 source links | Traceability +0.01 | Low |

Applying R1 + R2 alone is estimated to bring Completeness from 0.88 to ~0.92 and
Internal Consistency from 0.89 to ~0.91, which would raise the composite from 0.910 to
approximately **0.923** — above the 0.92 PASS threshold.

---

*Report generated by adv-scorer-003 per S-014 LLM-as-Judge methodology.*
*H-15 self-review completed: scores reviewed for leniency bias; all uncertain ranges
resolved downward per QG-3 scoring instructions.*
