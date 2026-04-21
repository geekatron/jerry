# Quality Score Report: Diataxis Audit — Jerry Framework User-Facing Documentation (2026-04-20)

## L0 Executive Summary

**Score:** 0.844/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.82)

**One-line assessment:** The audit is substantively strong and independently verifiable for most findings, but falls short of the 0.95 C4 threshold due to: an unresolved agent-count arithmetic contradiction in the executive summary vs. body findings, abbreviated criterion evaluation for playbooks and AGENTS.md, weak EV-009 evidence entry, and broken evidence-log traceability for playbook findings.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-040-documentation/reports/diataxis-audit-20260420.md`
- **Deliverable Type:** Analysis (Audit Report)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **User-Specified Threshold:** 0.95 (overrides H-13 default of 0.92)
- **Scored:** 2026-04-17T00:00:00Z
- **Iteration:** 1 of creator-critic-revision cycle

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.844 |
| **Threshold** | 0.95 (user-specified) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |
| **Gap to threshold** | 0.106 |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.87 | 0.174 | All 30 skills, 15 docs covered; 3 playbooks have "~unknown" line counts — not verified |
| Internal Consistency | 0.20 | 0.82 | 0.164 | Executive summary asserts "89 agents" without caveat; body flags 87-vs-89 as Major finding — contradictory framing |
| Methodological Rigor | 0.20 | 0.84 | 0.168 | Full T/H/R/E criterion batteries applied to 11 documents; playbooks and AGENTS.md evaluated with abbreviated criterion sets |
| Evidence Quality | 0.15 | 0.82 | 0.123 | 17 of 18 EV entries cite specific file:line with direct quotes; EV-009 is empty and internally inconsistent |
| Actionability | 0.15 | 0.88 | 0.132 | 18 remediation items with effort, owner-skill, and P1/P2/P3 priority; extraction targets lack section-level specificity |
| Traceability | 0.10 | 0.83 | 0.083 | Documents 1-10 fully traced to EV-NNN; playbook findings (Documents 11-14) reference criterion IDs but no EV-NNN entries |
| **TOTAL** | **1.00** | | **0.844** | |

**Weighted composite math:**
```
(0.87 × 0.20) = 0.174
(0.82 × 0.20) = 0.164
(0.84 × 0.20) = 0.168
(0.82 × 0.15) = 0.123
(0.88 × 0.15) = 0.132
(0.83 × 0.10) = 0.083
─────────────────────
Total           0.844
```

---

## Detailed Dimension Analysis

### Completeness (0.87/1.00)

**Evidence:**
- All 30 skills confirmed present via `skills/*/SKILL.md` glob (independently verified: 30 files returned).
- 15 in-scope documents catalogued with classification, line count, confidence, and purity verdict.
- Coverage matrix provides complete skill × quadrant grid for all 30 skills.
- Gap analysis organized by P1/P2/P3 with all major gap types identified.
- Delta from PROJ-015 covers all 6 original documents plus 9 additions.
- Remediation table covers 18 items across three priority bands.
- Scope boundaries are explicit and justified (in-scope/out-of-scope lists).
- AGENTS.md included in inventory (not audited in PROJ-015 — new coverage).

**Gaps:**
- Documents 11-13 (orchestration.md, transcript.md playbooks) have line count listed as "~unknown" — the auditor did not read these files to verify line counts or confirm the mixed-quadrant pattern with direct quotes.
- Document 14 (`docs/playbooks/PLUGIN-DEVELOPMENT.md`) similarly has "~unknown" lines.
- EV-009 claims `ci-cd-supply-chain-security.md` lines 7-9 evidence is "Empty" — this is factually inconsistent with the document having passed 7/7 criteria, and the "lead evidence" mentioned (scope statement line 5, Alternative Perspectives section) is described but not cited as an EV entry.
- The coverage summary note "partial how-to coverage: 4/30 skills (13%)" does not explicitly account for the `bootstrap` skill's `BOOTSTRAP.md` as a fifth how-to (listed in coverage matrix row 4 but not counted in the summary).

**Improvement Path:**
- Read and record actual line counts for the four playbooks (replace "~unknown" with verified figures and add at least one direct quote per finding).
- Fix EV-009: either remove it or replace "Empty" with actual evidence from the file's scope statement.
- Reconcile the "partial" count in the coverage summary (4 vs 5 skills with how-to coverage).

---

### Internal Consistency (0.82/1.00)

**Evidence:**
- The document classification criteria (Diataxis two-axis test) are applied uniformly across all 15 documents.
- Severity labels (Major, Minor) are used consistently throughout all finding tables.
- Verdict labels (PASS, NEEDS REVISION) are used consistently.
- The criteria IDs (H-01 through H-07, T-01 through T-08, etc.) are cited consistently.
- PROJ-015 status column uses "UNCHANGED" consistently for all re-verified findings.

**Gaps:**
The most significant internal inconsistency is the agent-count framing. The executive summary states: "30 skills, 89 agents" as a plain assertion. The body (AGENTS.md finding, EV-012) flags the agent count as a Major accuracy concern. A reader who only reads the executive summary accepts 89 as authoritative; a reader who reads the body learns it is contested. This is not a contradiction between two factual claims — it is a framing inconsistency where the executive summary presents uncertain data as settled.

The arithmetic in EV-012 is also internally unstable:
- Audit claims: "87 files found via glob" (confirmed independently: 87 `.md` files returned by `skills/*/agents/*.md` glob).
- AGENTS.md line 71 claims: "82 total files found; 4 template/extension files excluded" — my independent verification found no template files in the glob results that would explain this discrepancy. AGENTS.md says "82 total, 4 excluded = net 83 vs. per-skill sum 89 = discrepancy of 6."
- The audit's EV-012 says "87 files - 4 templates = 83... vs claimed 89. Discrepancy of 6" — but then separately says "Discrepancy requires independent verification" without resolving which figure (82 or 87 file count) is correct.
- The executive summary then uses "89 agents" without noting this discrepancy at all.

A C4 deliverable cannot present contested figures as settled in the summary while flagging them as Major concerns in the body.

**Improvement Path:**
- Executive summary should add a parenthetical: "89 agents per AGENTS.md (count accuracy flagged as Major finding — see EV-012)."
- EV-012 should resolve the 82 vs 87 file count discrepancy by identifying which glob was run (were template files in subdirectories? were `.governance.yaml` companion files excluded?). The finding should state a single verified number and clearly explain the remaining gap.

---

### Methodological Rigor (0.84/1.00)

**Evidence:**
- Classification methodology explicitly cites diataxis-standards.md Section 4 with the two-axis table reproduced.
- Confidence scoring is derived deterministically from a four-band rubric (1.00, 0.85, 0.70, <0.70) with explicit conditions for each band.
- Evidence standards are explicitly defined: file path + line range or direct quote + criterion ID + severity.
- Scope boundaries include both in-scope and out-of-scope lists with rationale (e.g., "SKILL.md is an internal file per skill-standards.md").
- Documents 7-10 (the four new passing documents) receive full criterion-by-criterion evaluation against 7 criteria each, with a cell for result, evidence, and status.
- Documents 1-6 (legacy documents) are fully re-verified against PROJ-015 with status column.
- The methodology section explicitly states all PROJ-015 findings are "independently re-verified against current file content" — and this is confirmed: INSTALLATION.md line 3 quote in EV-003 matches the actual file content.

**Gaps:**
- Documents 11-14 (all four playbooks) receive abbreviated findings: only 3 criteria evaluated per document (H-01, H-04, and the reference-table mixing observation), compared to the full 7-criterion battery. No explicit statement that the remaining 4 criteria (H-02, H-03, H-05, H-06, H-07) were evaluated and passed. A second auditor cannot tell whether these were evaluated and found compliant or were simply not checked.
- AGENTS.md (Document 12) receives finding tables but no full criterion evaluation against R-01 through R-07. The classification is Reference/Explanation mixed with 0.85 confidence, but only 2 findings are documented without a complete criteria sweep.
- No explicit statement of false-positive handling for the T-04 tutorial branching flag (diataxis-standards.md T-04 has an OS-conditional exception; the getting-started.md T-04 flag is plugin vs CLI, not OS-conditional — the auditor applies it correctly but doesn't explicitly invoke the False-Positive Handling Protocol to justify the flag).

**Improvement Path:**
- For each playbook: either complete the full H-01 through H-07 evaluation with a pass/fail for all 7 criteria, or explicitly state "criteria H-02, H-03, H-05, H-06, H-07 evaluated — PASS, no issues found" with a one-line justification.
- For AGENTS.md: add R-01 through R-07 evaluation table following the same pattern as Documents 9-10.
- Add a sentence to the getting-started.md T-04 finding explicitly addressing why the OS-conditional exception does not apply.

---

### Evidence Quality (0.82/1.00)

**Evidence:**
- 18 evidence log entries organized by EV-NNN IDs.
- EV-001: README.md lines 103-115 — independently verified: README.md lines 107-114 contain the 6-skill table (`/problem-solving`, `/worktracker`, `/nasa-se`, `/orchestration`, `/architecture`, `/transcript`). Claim confirmed.
- EV-003: INSTALLATION.md lines 1-5 — independently verified: line 3 contains the exact blockquote "Your AI coding partner just got guardrails, knowledge accrual, and a whole crew of specialized agents. Let's get you set up and shredding" and line 5 contains "battle-tested on macOS." Claim confirmed.
- EV-008: getting-started.md line 27 — independently verified: line 27 reads "Tested with: uv 0.5.x, Jerry v0.2.2, Claude Code 1.0.33+." CLAUDE.md confirms v0.31.5. Claim confirmed.
- EV-010: permission-security-model.md lines 7-9 — cites inline Diataxis compliance comments. Credible.
- EV-013: AGENTS.md lines 36-44 — independently verified: AGENTS.md lines 40-43 contain the Agent Philosophy bullets. Claim confirmed.
- Key claims for the four passing documents are backed by criterion-by-criterion tables with direct quotes for each finding.

**Gaps:**
- EV-009 (`docs/explanation/ci-cd-supply-chain-security.md`) reads: "Empty — file passes all E-01 through E-07 criteria. Lead evidence: scope statement line 5 and Alternative Perspectives section." This is self-contradictory: it claims to be "Empty" while also describing evidence. The passing documents should have a brief affirmative evidence entry, not an empty placeholder. This is the weakest entry in the log.
- Playbook findings (Documents 11-14) cite criterion IDs (H-01, H-04) but do not provide direct quotes for the failing text. For example, the H-04 failure in problem-solving.md ("Creator-Critic-Revision Cycle" section) cites section name but not the actual pedagogical sentence. A direct quote like "The creator-critic-revision cycle works as follows..." would make the finding independently verifiable without reading the full document.
- EV-012 cites two different file counts (82 per AGENTS.md vs 87 per audit's glob) without resolving which is authoritative. One of these is wrong, and the evidence log does not adjudicate.

**Improvement Path:**
- Replace EV-009 with an actual affirmative evidence entry citing the scope statement line 5 text and a quote from the Alternative Perspectives section.
- Add direct quotes for all H-01 and H-04 failures in playbook findings.
- Resolve the 82 vs 87 file count by re-running the glob and documenting the exact command and output.

---

### Actionability (0.88/1.00)

**Evidence:**
- All 18 remediation items include: action description, effort estimate (15min to 20h), and owner skill (diataxis-tutorial, diataxis-explanation, diataxis-howto, diataxis-reference, or Manual edit).
- P1 items (P1-1 through P1-4) are unambiguously actionable without follow-up questions: exact line references, exact replacement guidance, exact version numbers (uv 0.10.9, Jerry v0.31.5).
- P1-6 "Verify AGENTS.md agent count accuracy (87 files found via glob vs 89 claimed)" is specific and actionable as an audit task.
- P2-3 "Remove explanation blocks from BOOTSTRAP.md 'How It Works' and 'Why two directories?' sections; replace with single-sentence cross-references" — the specific sections are named and the replacement action is specified.
- Effort estimates are granular: 15min, 30min, 1h, 2h, 3h, 4h, 6h, 8h, 12h, 16h, 20h — not just "Low/Medium/High" categories (those labels are also present as a secondary mapping).
- The priority rationale in the executive summary ("Zero skills have a dedicated user-facing tutorial") provides strategic context that validates the P1 urgency classification.

**Gaps:**
- P2-1 "Create `docs/explanation/context-architecture.md` (extraction from BOOTSTRAP.md and CLAUDE-MD-GUIDE.md)" — the extraction targets are named at the section level (How It Works, Why two directories?, Context Architecture), but the writer would benefit from the exact line ranges (available in the findings as EV-004, EV-005, EV-006) being cross-referenced in the remediation item. Currently the remediation item and the evidence log are not explicitly linked.
- P2-4 "Remove explanation blocks and marketing voice from INSTALLATION.md" — "explanation blocks" is plural but the audit only documented one explanation block (lines 4-5 rationale, EV-003). A writer implementing P2-4 does not know how many explanation blocks to remove or where they all are.
- P1-5 "Create `docs/tutorial/` directory and one tutorial for the highest-use skill (`/problem-solving`) covering a complete end-to-end research task" — "complete end-to-end research task" is underspecified. What scenario? What prerequisite state? The diataxis-tutorial agent can infer these, but explicit scenario naming would further reduce ambiguity.

**Improvement Path:**
- Add EV cross-references to P2-1, P2-2, P2-3, P2-4 remediation items (e.g., "See EV-004, EV-005 for exact line ranges").
- For P2-4, enumerate all explanation blocks found in INSTALLATION.md (currently only lines 4-5 rationale documented; auditor should scan the full document for additional H-04 violations).
- For P1-5, specify the tutorial scenario (e.g., "researcher creates a research spike on a .NET library from scratch using ps-researcher").

---

### Traceability (0.83/1.00)

**Evidence:**
- Every finding in Documents 1-10 maps to a named EV-NNN entry in the evidence log.
- The evidence log uses a consistent schema: Finding ID, File, Evidence.
- The Delta section traces back to PROJ-015 findings by name (exact PROJ-015 priority action text).
- The methodology section explicitly cites diataxis-standards.md Section 4 and Section 2 (severity table).
- The confidence scoring rubric is traced to "diataxis-standards.md Section 4" with the rubric reproduced inline.
- PROJ-015 status ("NOT DONE," "UNCHANGED") is provided for every one of the 9 carry-forward items.
- The coverage matrix traces every skill to its documentation state with notes for partial coverage.

**Gaps:**
- Documents 11-14 (playbook findings) use criterion IDs in finding tables but no EV-NNN cross-references. For example, the H-01 failure in problem-solving.md is documented in the finding table but EV-018 is the only playbook-related evidence log entry — and it covers only the H-01 title finding. The H-04 finding in the same document has no EV entry at all.
- The coverage summary note ("The four playbooks cover their respective skills with how-to content mixed with reference tables. None pass full H-01 through H-07 criteria.") references criteria but no EV entries.
- EV-014 through EV-016 (glob results) are appropriate evidence for the missing directories finding, but EV-014 claims "30 SKILL.md files found; none have corresponding docs/ peer documents" — this is a meta-finding that would benefit from tracing back to a specific source command rather than just noting the glob result.
- The remediation table does not reference gap analysis items by any ID (e.g., "P1-5 addresses Gap: Zero tutorial documents"). Cross-referencing remediation to gap analysis would close the traceability chain from finding to remediation.

**Improvement Path:**
- Add EV-019 through EV-022 entries for the playbook findings (H-04 violations in each playbook), with direct quotes.
- Add EV cross-references to playbook finding tables (same pattern as Documents 1-10).
- Add a "Addresses Gap" column or note to the remediation table linking each item to its source gap.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.82 | 0.90 | Fix executive summary to flag agent count as contested ("89 per AGENTS.md — see EV-012 for accuracy concern"); resolve the 82 vs 87 file count discrepancy in EV-012 by re-running the glob with documented command and adjudicating the correct figure |
| 2 | Traceability | 0.83 | 0.92 | Add EV-NNN evidence log entries for all four playbook findings (H-01 and H-04 violations with direct quotes); add "Addresses Gap" linkage in the remediation table |
| 3 | Evidence Quality | 0.82 | 0.90 | Replace EV-009 with a substantive affirmative evidence entry; add direct quotes for all playbook criterion failures; resolve the 82 vs 87 file count in EV-012 |
| 4 | Methodological Rigor | 0.84 | 0.92 | Complete H-01 through H-07 evaluation for all four playbooks and AGENTS.md R-01 through R-07; add T-04 False-Positive Protocol analysis for getting-started.md |
| 5 | Completeness | 0.87 | 0.93 | Replace "~unknown" line counts with verified counts for playbooks 11-14; reconcile the "4 skills with partial how-to" count vs the 5 in the coverage matrix |
| 6 | Actionability | 0.88 | 0.93 | Add EV cross-references to P2-1 through P2-4 remediation items; enumerate all explanation blocks in INSTALLATION.md; add scenario specificity to P1-5 |

---

## Calibration Notes (What Would Push Each Dimension Higher)

**Completeness to 0.93+:** Verified line counts for all 15 documents (not estimated), full criteria sweeps for all 15 documents (not abbreviated for 4 playbooks), and reconciliation of the partial how-to coverage count.

**Internal Consistency to 0.92+:** A single authoritative agent count with the discrepancy fully resolved and the executive summary reflecting the verified number. No contested figures presented as settled.

**Methodological Rigor to 0.92+:** Full H-01 through H-07 battery for every how-to guide in scope (including all four playbooks and INSTALLATION.md), and full R-01 through R-07 for AGENTS.md. The methodology is sound — it just needs complete application to all in-scope documents.

**Evidence Quality to 0.92+:** Direct quotes for every Major and Minor finding (not just criterion ID references), EV-009 replaced with substantive evidence, and the file count discrepancy in EV-012 resolved with a single authoritative number.

**Actionability to 0.93+:** Explicit EV cross-references in each remediation item, scenario specification for P1-5, and a complete enumeration of explanation blocks in INSTALLATION.md for P2-4.

**Traceability to 0.92+:** All 15 documents with full EV-NNN traceability (not just 10 of 15), and remediation-to-gap linkage. The framework is present — it just needs to extend to the playbook section.

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computed
- [x] Evidence documented for each score (file:line citations verified against actual files)
- [x] Uncertain scores resolved downward (Internal Consistency: chose 0.82 over 0.85 given unresolved agent count in executive summary; Traceability: chose 0.83 over 0.85 given 4 of 15 documents with broken EV chain)
- [x] First-draft calibration considered (this is iteration 1; 0.844 is within the expected 0.80-0.90 range for strong first drafts)
- [x] No dimension scored above 0.95 without exceptional evidence
- [x] Independent verification performed against actual files (README.md, INSTALLATION.md, getting-started.md, AGENTS.md, agents glob) to confirm or challenge audit claims

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.844
threshold: 0.95
weakest_dimension: Internal Consistency
weakest_score: 0.82
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Fix executive summary agent count: note 89 is contested per EV-012; resolve 82 vs 87 file count discrepancy"
  - "Add EV-NNN entries for all four playbook findings (H-01, H-04 failures with direct quotes)"
  - "Replace EV-009 empty entry with substantive affirmative evidence for ci-cd-supply-chain-security.md"
  - "Complete H-01 through H-07 for all playbooks; complete R-01 through R-07 for AGENTS.md"
  - "Replace ~unknown line counts with verified figures for playbooks 11-14"
  - "Add EV cross-references to P2-1 through P2-4 remediation items; specify P1-5 scenario"
```
