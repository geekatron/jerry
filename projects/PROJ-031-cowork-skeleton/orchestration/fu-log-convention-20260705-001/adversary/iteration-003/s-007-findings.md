# Constitutional Compliance Report: Feedback & Decision Log Convention (iteration-3)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, deliverable, scope |
| [Summary](#summary) | Overall verdict |
| [Findings Table](#findings-table) | All findings, severity-classified |
| [Finding Details](#finding-details) | Full evidence + remediation per finding |
| [Compliant Areas (Evidence)](#compliant-areas-evidence) | Principle areas checked and found COMPLIANT |
| [Remediation Plan](#remediation-plan) | Prioritized P0/P1/P2 actions |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping + compliance score |

---

## Execution Context

- **Strategy:** S-007 Constitutional AI Critique
- **Template:** `.context/templates/adversarial/s-007-constitutional-ai.md`
- **Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, hook-design-note.md, examples-appendix.md}`
- **Criticality:** C4 (engagement gate 0.95, user-set)
- **Iteration:** 3 (blind protocol; no prior adversary iteration files read)
- **Date:** 2026-07-06
- **Reviewer:** adv-executor (S-007 Constitutional AI Critique)
- **Constitutional Context:** `docs/governance/JERRY_CONSTITUTION.md` v1.0 (P-001–P-022 read directly: P-002, P-003, P-011, P-020, P-022); `.context/rules/quality-enforcement.md` (HARD Rule Index, Tier Vocabulary, HARD ceiling 25/25); `.context/rules/markdown-navigation-standards.md` (H-23/H-24)

---

## Summary

**PARTIAL compliance.** 0 Critical, 2 Major, 2 Minor findings. The package is disciplined and well-remediated: MEDIUM-tier vocabulary is clean in the file destined for `.context/rules/` (no MUST/SHALL leakage), the HARD ceiling (25/25) is correctly cited and left untouched, all six files carry H-23-compliant navigation tables with verified-correct anchor links, the four open questions (Q1–Q4) are consistently labeled `PROPOSED-DEFAULT, pending ratification` everywhere they appear (P-020 respected — nothing is silently treated as decided), and public-repo hygiene is intact (no absolute `[home]/` paths, no un-bracketed employer/internal references found in the reviewed package). The two Major findings are a genuine but *disclosed-elsewhere* overclaim in `hook-design-note.md` ("provenance becomes harness-guaranteed") that reads as absolute against the same file's own fail-open contract, and an asymmetric gap where the interim (pre-hook) manual fallback is stated for FEEDBACK-LOG but omitted for LLM-DECISION-LOG. Recommendation: REVISE (targeted wording fixes only; no new machinery required).

---

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-20260706iter3 | P-022 No Deception (honesty about capability/coverage) | HARD | Major | `hook-design-note.md:30` "provenance becomes harness-guaranteed" vs. `hook-design-note.md:47` fail-open contract | Internal Consistency |
| CC-002-20260706iter3 | P-022 No Deception (completeness of interim-state disclosure) / Actionability | HARD (disclosure) / MEDIUM (fallback guidance) | Major | `feedback-decision-logs-standards.md:27` (LOG-M-005) and `LLM-DECISION-LOG.template.md:19-27` omit the "otherwise fill what you know" fallback present in `FEEDBACK-LOG.template.md:22` | Actionability |
| CC-003-20260706iter3 | Tier Vocabulary consistency (quality-enforcement.md) | MEDIUM | Minor | `feedback-decision-logs-standards.md:23-28` — LOG-M-001/002/003/006 omit inline "SHOULD"; LOG-M-004/005 retain it | Internal Consistency |
| CC-004-20260706iter3 | P-020 User Authority (process completeness for provisional-to-ratified transition) | MEDIUM | Minor | `feedback-decision-log-convention-design.md:225-236` (Adoption plan) has an explicit alias-rename install action (step 4) but no equivalent action to update/strip `PROPOSED-DEFAULT` wording after Q1–Q4 ratification | Completeness |

**Finding ID format:** `CC-{NNN}-20260706iter3` per S-007 template (execution_id = `20260706iter3`).

---

## Finding Details

### CC-001-20260706iter3: "Harness-guaranteed" overclaim vs. same-file fail-open contract [MAJOR]

**Principle:** P-022 No Deception — "Agents SHALL NOT deceive users about... Capabilities or limitations" (`JERRY_CONSTITUTION.md:178-185`).

**Location:** `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/hook-design-note.md:30` (Seam 1 bullet) vs. same file line 47 (Fail-open contract).

**Evidence:**
- Line 30: *"When an entry is minted, its Context line references the sidecar key instead of hand-typing metadata → provenance becomes **harness-guaranteed**."*
- Line 47: *"A capture hook MUST be **fail-open**: a logging failure never costs the user a turn."*
- Package-wide framing (design doc L0, line 30): capture "stays a **MEDIUM (SHOULD)** discipline until the fail-open hook of Q3 ships."

**Analysis:** Read literally and in isolation, "provenance becomes harness-guaranteed" is an absolute claim of coverage. The same document's own Fail-open Contract section establishes the opposite operating assumption: the hook can silently fail to stamp/write on any given turn and this is an accepted, by-design outcome ("a logging failure never costs the user a turn" — i.e., the turn proceeds regardless of whether the stamp landed). A charitable reading is that "guaranteed" modifies the *source* of the data (harness-sourced vs. hand-typed) conditional on successful stamping, not the *existence* of the stamp on every turn — but the sentence as written does not carry that qualifier, and the task's explicit review criterion is exactly this class of issue ("overclaimed coverage IS Critical" per the assigned brief). I am classifying this Major rather than Critical because: (a) the document's own banner and the design doc's L0 scope note both already disclose, in the same package, that capture is MEDIUM/best-effort until Q3 ships; (b) the contradiction is resolvable by reading 17 lines further in the same file, not hidden across artifacts; (c) it is a single wording choice, not a claim that the hook has shipped or that entries cannot be lost. This is nonetheless a real internal-consistency defect that a downstream reader (e.g., someone implementing Seam 1, or a stakeholder skimming only the Seam 1 section) could reasonably misread as an availability guarantee.

**Recommendation:** Reword line 30 to remove the absolute claim, e.g.: *"...its Context line references the sidecar key instead of hand-typing metadata → when the stamp is present, provenance is harness-sourced rather than hand-typed (subject to the fail-open contract below — a hook failure omits the stamp, never blocks the turn)."*

---

### CC-002-20260706iter3: Interim (pre-hook) fallback disclosed for FEEDBACK-LOG, omitted for LLM-DECISION-LOG [MAJOR]

**Principle:** P-022 No Deception (completeness of "what governs until the hook ships") / Actionability (S-014 dimension).

**Location:**
- Present (compliant): `FEEDBACK-LOG.template.md:22` — *"Context format:... When the provenance hook is installed, the assistant stamps this; **otherwise fill what you know**."*
- Absent: `LLM-DECISION-LOG.template.md:19-27` (Entry Schema section) — describes the Context field ("`datetime · session · model · agents/workflow · artifacts · Reflected in`") with no equivalent "otherwise fill what you know" clause.
- Absent: `feedback-decision-logs-standards.md:27` (LOG-M-005) — *"Provenance SHOULD reference the harness sidecar, not hand-typed values."* No inline caveat that the sidecar does not exist until Q3 ships (the caveat lives only in the document's opening banner, three sections earlier).

**Analysis:** The package is correct and consistent at the top-level banner ("a fail-open hook is designed to assist but is not yet shipped") and in the FEEDBACK-LOG template. But an operator or agent who opens `LLM-DECISION-LOG.template.md` directly to author a DEC-LLM entry today (pre-hook) has no in-context instruction for what to do about the Context line's provenance fields absent the sidecar — the same gap that the FEEDBACK-LOG template explicitly closes. Similarly, LOG-M-005's "SHOULD reference the harness sidecar" reads as current operative guidance without its own local caveat. This is a completeness/actionability asymmetry between the two logs' guidance, not a fabricated capability claim — but it leaves exactly the gap the assigned review brief asked about ("must-log is model-dependent until hook ships — is that disclosed?" — disclosed at the package level, not at the point of use for the decision log).

**Recommendation:** Add the same "otherwise fill what you know (until the Q3 hook ships)" clause to `LLM-DECISION-LOG.template.md`'s Context field description, and add a three-word parenthetical to LOG-M-005 (e.g., "...reference the harness sidecar **once available**, not hand-typed values").

---

### CC-003-20260706iter3: Inconsistent inline "SHOULD" across LOG-M-001..006 [MINOR]

**Principle:** Tier Vocabulary consistency (`quality-enforcement.md` — MEDIUM keywords: SHOULD, RECOMMENDED, PREFERRED, EXPECTED).

**Location:** `feedback-decision-logs-standards.md:23-28`.

**Evidence:**
- LOG-M-001: *"Append feedback to the scoped FEEDBACK-LOG the same turn it is given..."* — no inline "SHOULD".
- LOG-M-002: *"Capture user feedback verbatim and full..."* — no inline "SHOULD".
- LOG-M-003: *"Append decision-bearing exchanges to the scoped LLM-DECISION-LOG..."* — no inline "SHOULD".
- LOG-M-004: *"...Graduation **SHOULD** be proposed at the next commit-cadence checkpoint..."* — inline "SHOULD" present.
- LOG-M-005: *"Provenance **SHOULD** reference the harness sidecar..."* — inline "SHOULD" present.
- LOG-M-006: *"At the segment cap... seal the ACTIVE log and start a fresh ACTIVE..."* — no inline "SHOULD".

**Analysis:** The section banner ("All rows are SHOULD-tier. Override requires documented justification.") correctly declares the whole table MEDIUM-tier, so there is no HARD-vocabulary leak and no ceiling risk. This is a Minor readability nit: rows quoted in isolation (commit messages, PR comments, lint failure text) would read as bare imperatives rather than clearly MEDIUM-tier guidance, inconsistent with how the design doc's own L2 section phrases the same rules (`feedback-decision-log-convention-design.md:204` — *"Feedback **SHOULD** be appended..."*).

**Recommendation:** Add inline "SHOULD" to LOG-M-001, LOG-M-002, LOG-M-003, LOG-M-006 for uniformity with LOG-M-004/005 and with the design doc's phrasing. Token cost is negligible (~4-6 tokens per row).

---

### CC-004-20260706iter3: No explicit install-time action to resolve PROPOSED-DEFAULT wording [MINOR]

**Principle:** P-020 User Authority (process completeness for the provisional→ratified transition).

**Location:** `feedback-decision-log-convention-design.md:225-236` (Adoption / migration plan, L2).

**Evidence:** Step 4 explicitly calls out a wording-update action at install time: *"heading suffixes are renamed from the bootstrap `(user label: X)` form to the ratified `(alias: X)` form at install time."* No equivalent step exists for updating/removing the `(PROPOSED-DEFAULT, pending ratification)` annotations that are baked directly into rule text (`feedback-decision-logs-standards.md:25` LOG-M-003; `:44` assistant-verbatim policy; `:57` Q2 scope tag) once step 1 ("Approve this design... user sign-off on the 4 open questions") completes.

**Analysis:** This is not a governance violation — the design correctly treats Q1–Q4 as undecided today and labels them as such everywhere (P-020 respected). But if the rule file is copied to `.context/rules/` per step 3 without an explicit action to reconcile the now-ratified defaults, the installed HARD-adjacent MEDIUM rule text would retain stale "(PROPOSED-DEFAULT, pending ratification)" language indefinitely. This is a hygiene/completeness gap in the adoption plan, not a present-tense compliance failure.

**Recommendation:** Add one line to the Adoption plan (near step 3 or 4): *"Resolve PROPOSED-DEFAULT wording in LOG-M-003 and the Q2 scope-tag description to reflect the ratified choice (or the accepted alternative) before or during install."*

---

## Compliant Areas (Evidence)

Documented per Step 3 of the S-007 protocol (principle stated, evidence cited, COMPLIANT).

| Principle | Evidence of Compliance |
|-----------|-------------------------|
| Tier Vocabulary / HARD ceiling (quality-enforcement.md) | No MUST/SHALL found in `feedback-decision-logs-standards.md` (the file destined for `.context/rules/`) via direct grep. The only MUST/MUST NOT usage across the package is in `hook-design-note.md:38-43`, which carries an explicit, correctly-reasoned exemption note (line 4: "code-implementation contracts for the (separately gated) hook script — not Jerry HARD-rule-tier governance... do not count against the 25/25 HARD-rule ceiling"). No new `H-XX` ID is introduced anywhere; LOG-M-00x namespace is consistently used. |
| H-23 Navigation Tables | All 6 reviewed files (design doc + 5 staging files) carry a "Document Sections" nav table. Anchor links were manually re-derived from each heading using GitHub's slug algorithm and cross-checked against all ~35 nav-table entries across the 6 files — zero broken anchors found, including two non-trivial double-hyphen cases (`#l2-governance--migration`, `#seam-2-capture-reminder-stop--precompact`) that were correctly anticipated by the author. |
| P-020 User Authority (provisional-vs-decided labeling) | All four open questions (Q1 assistant-verbatim policy, Q2 framework-feedback scope tag, Q3 hook timing, Q4 backfill) are labeled `PROPOSED-DEFAULT` consistently at every location they appear: design doc (`:264-269`), standards file (`:25,44,57`), and `LLM-DECISION-LOG.template.md:27`. Backfill Queue sections in both templates explicitly say "pending user authorization." No artifact silently treats an open question as decided. |
| Public-repo hygiene | Grep for `[home]/`, `[employer]`, `[employer]` across `projects/PROJ-031-cowork-skeleton/design/` returned zero matches; all internal-KB references use bracketed placeholders (`[internal-kb]`, `[legacy-fu-id]`, `[legacy-oi-id]`) consistent with the FU.4 sanitization precedent recorded in `FEEDBACK-LOG.md:84-93`. No TODO/FIXME/XXX placeholder debris found in the staged files. |
| P-004 Explicit Provenance | Every design claim in the reviewed package traces to a cited source (`[R]`/`[B]`/`[U]`/`[G]` reference scheme, `feedback-decision-log-convention-design.md:314-323`); `[INFERENCE]` is used consistently to flag unverified claims (e.g., design doc `:85` inline-doc harvest caveat, `:119` transcript-retention assumption). |

---

## Remediation Plan

**P0 (Critical):** None.

**P1 (Major):**
- CC-001: Reword `hook-design-note.md:30` to remove the unqualified "harness-guaranteed" claim; make it explicitly conditional on the fail-open contract.
- CC-002: Add the "otherwise fill what you know (until Q3 ships)" fallback clause to `LLM-DECISION-LOG.template.md`'s Context field description and to LOG-M-005.

**P2 (Minor):**
- CC-003: Add inline "SHOULD" to LOG-M-001/002/003/006 for uniformity with LOG-M-004/005 and the design doc's own phrasing.
- CC-004: Add one Adoption-plan line covering PROPOSED-DEFAULT wording resolution at/before install.

All four recommendations are wording-only; none require new machinery, new lint checks, or new files — consistent with the package's stated anti-bloat doctrine.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative (minor) | CC-002: interim-state fallback guidance present for FEEDBACK-LOG but absent for LLM-DECISION-LOG |
| Internal Consistency | 0.20 | Negative | CC-001: "harness-guaranteed" claim vs. same-file fail-open contract; CC-003: inline-SHOULD inconsistency across LOG-M-00x rows |
| Methodological Rigor | 0.20 | Neutral | No violations found; MEDIUM-tier discipline, ceiling discipline, and H-23 discipline all hold |
| Evidence Quality | 0.15 | Neutral | No constitutional findings affect evidence quality; citations and `[INFERENCE]` labeling are thorough throughout |
| Actionability | 0.15 | Negative (minor) | CC-002: gap leaves the LLM-DECISION-LOG author without in-context guidance for the pre-hook interim state |
| Traceability | 0.10 | Neutral | No constitutional findings affect traceability; reference scheme (`[R]/[B]/[U]/[G]`) is intact |

**Constitutional Compliance Score:** `1.00 - (0.10 × 0 + 0.05 × 2 + 0.02 × 2) = 1.00 - 0.14 = 0.86` → **REVISE** (0.85–0.91 band; below the H-13 threshold of 0.92, but no Critical findings and all four recommended fixes are wording-only).

**Threshold Determination:** REVISE. No blocking (Critical/HARD) findings identified in this S-007 pass. The two Major findings are disclosure/consistency gaps that are already substantially mitigated by disclosure elsewhere in the same package, not undisclosed capability claims.
