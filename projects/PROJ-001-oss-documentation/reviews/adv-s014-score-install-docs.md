# Quality Score Report: Installation Documentation Set

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Verdict, score, and top action item |
| [Scoring Context](#scoring-context) | Deliverable metadata and scoring parameters |
| [Score Summary](#score-summary) | Composite score, threshold, verdict |
| [Dimension Scores](#dimension-scores) | Weighted score table across 6 dimensions |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Per-dimension evidence, gaps, and improvement paths |
| [Improvement Recommendations](#improvement-recommendations) | Priority-ordered remediation table |
| [Leniency Bias Check](#leniency-bias-check) | Bias counteraction verification |

---

## L0 Executive Summary

**Score:** 0.74/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.67)

**One-line assessment:** The documentation set is structurally sound and internally cleaner after revision, but an unverifiable Quick Install claim (DA-001), unquantified value proposition (SM-001/SM-002), and missing actionability elements (SM-007, DA-006) prevent quality gate passage — targeted revision on three dimensions is required.

**Special Case Applied:** DA-001 (unverified Quick Install) remains an open Critical finding from the S-002 Devil's Advocate report. Per the scoring protocol, any unresolved Critical finding from adv-executor reports triggers automatic REVISE regardless of composite score.

---

## Scoring Context

- **Deliverable:** `docs/INSTALLATION.md`, `docs/index.md`, `docs/BOOTSTRAP.md`, `docs/runbooks/getting-started.md` (cohesive documentation set — "installation documentation rewrite")
- **Deliverable Type:** Documentation
- **Criticality Level:** C2 (Standard — public-facing OSS documentation, reversible in 1 day)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Strategy Findings Incorporated:** Yes — S-003 Steelman (13 findings), S-007 Constitutional (2 findings, both fixed in revision), S-002 Devil's Advocate (10 findings, 5 addressed in revision, 5 remain)
- **Revision State:** Post-revision (6 fixes applied: CC-001, CC-002, DA-002 partial, DA-003 partial, DA-004, DA-005 version fix)
- **Scored:** 2026-02-18

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.74 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Gap to Threshold** | -0.18 |
| **Strategy Findings Incorporated** | Yes — 25 total (2 Critical, 6 Major, 5 Minor from S-003; 2 Major from S-007; 3 Critical, 5 Major, 2 Minor from S-002) |
| **Open Critical Findings** | 1 (DA-001 — unverified Quick Install, acknowledged unresolvable in current session) |

**Score Band:** 0.70–0.84 — Significant gaps, focused revision needed.

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.72 | 0.144 | Primary install path unverifiable (DA-001 open); CLI availability for plugin users unaddressed (DA-005); no concrete output example in Step 4 (SM-007 open) |
| Internal Consistency | 0.20 | 0.76 | 0.152 | CC-001/CC-002 fixed; DA-004 hooks label now consistent; BUG-002 known-issue callout added but "activate automatically" claim still present alongside it |
| Methodological Rigor | 0.20 | 0.75 | 0.150 | DA-003 partially addressed with /plugin marketplace list guidance; two-step install pattern still unexplained (SM-004); bootstrap two-directory rationale absent (SM-006) |
| Evidence Quality | 0.15 | 0.67 | 0.1005 | Quick Install explicitly acknowledged as unverifiable (DA-001); context rot problem statement still lacks quantitative anchor (SM-001); capabilities still unquantified (SM-002) |
| Actionability | 0.15 | 0.74 | 0.111 | Hooks label fixed; DA-006 unaddressed (no explicit /problem-solving fallback); SM-007 unaddressed (no concrete output block in Step 4); hook failure-mode enumeration still general |
| Traceability | 0.10 | 0.83 | 0.083 | H-04, P-002, P-003 citations present and correct; cross-document links consistent; CONTRIBUTING.md external link not verified live (DA-007 minor residual) |
| **TOTAL** | **1.00** | | **0.74** | |

---

## Detailed Dimension Analysis

### Completeness (0.72/1.00)

**Evidence:**

The four-document set covers a comprehensive scope: two installation methods (Quick Install, Local Clone), hooks setup, capability matrix, configuration, verification, developer setup, troubleshooting, and a step-by-step onboarding runbook. Navigation tables are present and correct in all four files (CC-001 fixed). Cross-document linking is consistent. Post-revision, the set eliminates the Python prerequisite contradiction (CC-002) and aligns hooks labeling (DA-004).

**Gaps:**

1. **DA-001 (Critical — open):** The Quick Install section claims "Jerry is a public Claude Code plugin. Install it with two commands." This is acknowledged as unverifiable in the current session. The primary install path — the one described as appropriate for "Most Users" — cannot be confirmed to work. A disclosure note exists in the review context but may not be reflected in the documents themselves.

2. **DA-005 (Major — unaddressed):** `getting-started.md` Step 3 presents `jerry session start` as an explicit trigger command available to users, but the prerequisites do not establish whether the `jerry` CLI is available after a plugin-only install. A plugin-only user (the intended audience for getting-started.md) may not have the CLI on their PATH, making Step 3's explicit trigger path fail for the primary audience.

3. **DA-006 (Major — unaddressed):** Step 4 of the runbook describes skill activation via trigger keywords but provides no fallback explicit invocation path (e.g., `/problem-solving`). Users whose LLM-mediated keyword activation fails have no documented recovery path within the primary onboarding document.

4. **SM-007 (Major — unaddressed):** Step 4 describes expected behavior in prose ("you will see a message indicating which agent was selected") without a concrete output example block. New users cannot verify success against a specific pattern.

5. **DA-007 (Major — partially unaddressed):** Windows is described as "in progress — core functionality works, but some hooks may behave differently." No specific hooks are named, no Windows-specific tracking issue is linked. The complete Windows command coverage creates a completeness appearance that the platform caveat partially invalidates.

6. **DA-008 (Major — unaddressed):** The `/plugin` UI tabs ("Installed," "Errors," "Discover") are referenced throughout without a version assertion confirming they exist in Claude Code 1.0.33+.

**Improvement Path:**

Adding a concrete expected output block to Step 4 (SM-007) and clarifying CLI availability for plugin users (DA-005) are the two highest-leverage completeness improvements that do not require external verification. These can be addressed in the next revision without a live Claude Code test environment.

---

### Internal Consistency (0.76/1.00)

**Evidence:**

Post-revision, the two most clear-cut internal consistency violations are fixed:
- CC-001: BOOTSTRAP.md navigation table now includes Command Reference section.
- CC-002: Developer Setup prerequisites no longer list Python 3.11+ as a separate install requirement, consistent with the general docs' "uv manages Python automatically" claim.
- DA-004: "Recommended" label for hooks is now consistent between `INSTALLATION.md` and `index.md` (previously "Optional" in index.md, "Recommended" in INSTALLATION.md).

**Gaps:**

1. **DA-002 (Critical — partially addressed):** The "Known issues" callout has been added, acknowledging hook schema validation issues. However, the sentence "Hooks activate automatically the next time you start Claude Code — no additional configuration needed" still appears in the Enable Hooks section. The callout and the promotional claim exist in the same section, creating a soft contradiction: the headline claim is unconditional, while the caveat acknowledges activation may silently fail. A user reading quickly will absorb the headline and miss the caveat.

2. **DA-007 (Major — unaddressed):** `INSTALLATION.md` provides complete Windows PowerShell instructions throughout (full platform coverage), while simultaneously labeling Windows as "in progress — edge cases may exist." The depth of Windows documentation creates an implicit claim of support that the caveat language undercuts. This creates an inconsistency between documentation thoroughness and platform support status.

**Improvement Path:**

The DA-002 partial fix should be strengthened: move the known issues callout above the "activate automatically" headline, or revise the headline to be conditional ("Hooks activate automatically when working correctly — see Known Issues below for current defect status"). This removes the impression that the callout is a minor addendum to an unconditional claim.

---

### Methodological Rigor (0.75/1.00)

**Evidence:**

The documentation follows a disciplined structure throughout: navigation tables in all files, consistent section ordering (prerequisites → steps → verification → troubleshooting → reference), platform-specific commands presented in parallel tabs, troubleshooting organized by symptom/cause/solution. The scope guidance (Quick Install vs. Local Clone vs. Developer Setup) is logically structured with clear use-case framing.

Post-revision, DA-003 is partially addressed: Step 2 of the Quick Install now instructs users to run `/plugin marketplace list` to confirm the marketplace name before attempting install, and the troubleshooting section similarly advises this. This converts an asserted fact into a verified-empirical approach, which is a meaningful methodological improvement.

**Gaps:**

1. **SM-004 (Major — unaddressed):** The two-step install pattern (why two commands, what each does, why the `@suffix` is needed) is not explained in the install procedure. The mechanics of marketplace registration followed by plugin installation are non-obvious for users new to the Claude Code plugin system. The troubleshooting section addresses symptoms of misunderstanding this pattern, but the install section does not preempt the misunderstanding.

2. **SM-006 (Major — unaddressed):** `BOOTSTRAP.md` explains what the two-directory structure does (`.context/` is canonical, `.claude/` is where Claude Code looks) without explaining why this approach was chosen over a single directory. The three design rationale points (auditability, distribution, stability) are absent.

3. **DA-003 (Critical — partially addressed):** The marketplace name derivation is now more defensively documented (users are told to verify with `/plugin marketplace list`), but the underlying mechanism — how Claude Code derives the name from the URL or directory — is still not cited to any Claude Code documentation. The documentation continues to state `geekatron-jerry` and `jerry-framework` as the expected names without documented derivation logic.

**Improvement Path:**

Adding a brief two-paragraph explanation of the marketplace-then-install pattern model (SM-004) is a contained addition that addresses a root cause of multiple troubleshooting scenarios. It can be added without external verification.

---

### Evidence Quality (0.67/1.00)

**Evidence:**

The documentation makes several verifiable claims: the H-04 rule exists and is correctly cited, P-002 is cited with a link to its constitutional source, the 0.92 quality threshold is correctly stated, the six scoring dimensions are correctly listed in `index.md`'s What is Jerry section. Commands shown throughout use the correct `uv run` pattern (H-05 compliant). The CA matrix in INSTALLATION.md correctly maps features to uv/no-uv states.

**Gaps:**

1. **DA-001 (Critical — open, acknowledged):** The most prominent user-facing claim — "Jerry is a public Claude Code plugin. Install it with two commands" — is explicitly acknowledged as unverifiable in the current session. This is not a documentation failure that can be addressed by wording changes; it requires a live end-to-end test of the `/plugin marketplace add` path. Until this is verified, the documentation's central premise for the primary install path has no evidentiary foundation.

2. **SM-001 (Critical — unaddressed):** `docs/index.md` Why Jerry section states: "As sessions grow, LLMs lose track of earlier instructions, skip rules, and produce inconsistent output." This claim is asserted without a quantitative anchor (token range, empirical observation, or reference). The steelmanned version (50,000–100,000 tokens as the typical onset range) provides a concrete claim; the current text remains qualitative. Skeptical evaluators will note the vagueness.

3. **SM-002 (Critical — unaddressed):** The four core capabilities in `index.md` What is Jerry section are described with varying levels of specificity. Quality Enforcement mentions the 0.92 threshold. Behavioral Guardrails describes "a layered rule system (HARD / MEDIUM / SOFT)" but does not cite the enforcement token budget (~15,100 tokens), the 5-layer architecture (L1–L5), or any concrete differentiator from a manually maintained CLAUDE.md. Adversarial Review lists "ten adversarial strategies" but does not name them or their criticality-level mappings. The value proposition relies primarily on assertion rather than quantified evidence.

4. **DA-008 (Major — unaddressed):** The `/plugin` UI described (Installed tab, Errors tab, Discover tab) is asserted as the correct interface for Claude Code 1.0.33+ without any version-pinned evidence that these tabs exist or have stable names at the minimum supported version.

**Improvement Path:**

SM-001 and SM-002 are addressable without external verification — the quantitative specifics exist in the framework's internal documentation and can be surfaced into the public-facing value proposition. This would raise Evidence Quality from 0.67 to approximately 0.78 without requiring any new information to be generated.

---

### Actionability (0.74/1.00)

**Evidence:**

The documentation is procedurally strong: each step has a clear action, expected outcome, and verification check. Troubleshooting is organized by symptom, cause, and resolution. Platform-specific commands (macOS/Linux/Windows) are consistently provided in parallel throughout all four documents. The getting-started.md runbook uses a checklist verification format that allows users to confirm their state at each step.

Post-revision, DA-004 is fixed: hook installation is consistently labeled "Recommended" across both INSTALLATION.md and index.md. The version number in getting-started.md was corrected (DA-005 version fix). The BUG-002 known-issue callout provides users a place to look when hooks fail silently.

**Gaps:**

1. **DA-006 (Major — unaddressed):** Step 4 of getting-started.md instructs users to include a trigger keyword (research, analyze, investigate, etc.) to activate the problem-solving skill. No explicit invocation fallback is documented. The troubleshooting entry for "skill does not activate" correctly suggests using exact trigger keywords but does not mention `/problem-solving` as an always-available explicit invocation. A user whose LLM-mediated keyword activation fails has no documented escape hatch within the runbook.

2. **SM-007 (Major — unaddressed):** Step 4 describes expected behavior in prose: "Claude responds by activating the problem-solving skill — you will see a message indicating which agent was selected." No concrete output block is provided. A new user cannot compare their actual output against a specific expected pattern to confirm success or diagnose failure. The absence of a concrete output example is the highest-leverage single improvement to actionability.

3. **SM-005 (Major — unaddressed at the specific level):** The Capability Matrix correctly shows the hooks feature delta. The "Known issues" callout was added per DA-002. However, the Enable Hooks section's description of what is lost without uv ("you lose the automated guardrail enforcement") remains general. The three specific enforcement layers that are inactive without hooks (L2 per-prompt re-injection, L3 pre-tool-call AST validation, P-003 hook-layer enforcement) are described in the hooks table but not explicitly enumerated as a consequence of the skip decision.

**Improvement Path:**

Adding one line to Step 4 — "If keyword activation does not trigger the skill, invoke it explicitly with `/problem-solving`" — and adding a concrete 3-line expected output block directly addresses DA-006 and SM-007. Both are contained changes to a single document section.

---

### Traceability (0.83/1.00)

**Evidence:**

Traceability is the strongest dimension. Rule citations are accurate and properly linked:
- `getting-started.md` cites H-04 with a link to `.context/rules/quality-enforcement.md#hard-rule-index`
- `getting-started.md` cites P-002 with a link to `../governance/JERRY_CONSTITUTION.md#p-002-file-persistence`
- `getting-started.md` cites P-003 by name in the context of subagent enforcement
- `index.md` cites the 0.92 quality threshold, six scoring dimensions (by count), and 10 adversarial strategies (by count)
- Cross-document links are consistent: `index.md` Quick Start links to `INSTALLATION.md` sections and `runbooks/getting-started.md`; `INSTALLATION.md` links to `runbooks/getting-started.md`; `BOOTSTRAP.md` is correctly linked from `INSTALLATION.md` Developer Setup
- Internal section anchor links are correctly formatted throughout all four files (H-24 compliant)

**Gaps:**

1. **DA-007 (Minor residual):** `INSTALLATION.md` Developer Setup references `CONTRIBUTING.md` at `https://github.com/geekatron/jerry/blob/main/CONTRIBUTING.md` for "Windows-specific notes" and the "full Make target equivalents table." This is an external link to a repository that may not be public at the time of documentation release. If the link is dead at publication time, the traceability for Windows developer setup instructions is broken.

2. **DA-001 shadow:** The Quick Install instruction traces to a GitHub URL (`https://github.com/geekatron/jerry`) as the plugin source. Since this URL is unverified as a working plugin marketplace source, the traceability from the install instruction to a confirmed working endpoint is absent.

**Improvement Path:**

Verifying the CONTRIBUTING.md link is live (or providing inline fallback content for the Windows Make table) would close the primary traceability gap. This requires a one-time external verification.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.67 | 0.78 | Address SM-001: Add quantitative anchor to the context rot problem statement in `index.md` Why Jerry section (e.g., "typically beyond 50,000–100,000 tokens"). Address SM-002: Add measurable specifics to Behavioral Guardrails and Adversarial Review capability bullets (~15,100 enforcement tokens, 5-layer architecture, strategy names). These are the highest-leverage changes that do not require external verification. |
| 2 | Actionability | 0.74 | 0.84 | Address SM-007: Add a concrete 3-line expected output block to `getting-started.md` Step 4 showing the artifact invocation message and saved file path pattern. Address DA-006: Add one sentence to Step 4 and the troubleshooting entry noting that explicit invocation (`/problem-solving`) is always available as a fallback when keyword activation does not trigger. |
| 3 | Completeness | 0.72 | 0.80 | Address DA-005: Clarify in `getting-started.md` Step 3 whether `jerry session start` is available to plugin-only users. If not, replace with a plugin-user-appropriate verification (e.g., "Open Claude Code and watch for `<project-context>` in session output"). Address DA-006 (overlaps with Priority 2). |
| 4 | Internal Consistency | 0.76 | 0.84 | Address DA-002: Reorder the Enable Hooks section so the Known Issues callout appears before the "activate automatically" headline, or revise the headline to be conditional ("Hooks activate automatically when working correctly — see Known Issues for current defect status"). This prevents the callout from reading as a minor footnote to an unconditional claim. |
| 5 | Methodological Rigor | 0.75 | 0.82 | Address SM-004: Add a brief explanation of the two-command install pattern ("marketplace add registers the source; install installs from it — like adding a package repository, then installing a package"). Address SM-006: Add the three-purpose rationale for the two-directory bootstrap structure (auditability, distribution, stability). |
| 6 | Evidence Quality (DA-001) | — | — | Address DA-001: This requires a live end-to-end test of `/plugin marketplace add https://github.com/geekatron/jerry` on a fresh Claude Code 1.0.33+ installation. If the test succeeds, document the test result. If the test cannot be run before release, add a disclosure to the Quick Install section: "This path requires Jerry to be registered in the Claude Code plugin marketplace. If the install fails, use the Local Clone Install instead." |

---

## Leniency Bias Check

- [x] Each dimension scored independently — scores were assigned per-dimension before computing the composite; no dimension was adjusted based on another
- [x] Evidence documented for each score — specific findings from S-003, S-007, S-002 reports cited per dimension; specific document locations and finding IDs cited throughout
- [x] Uncertain scores resolved downward — Completeness (0.72 vs. 0.75 considered; lowered due to DA-001 and DA-005 being unaddressed), Evidence Quality (0.67 vs. 0.70 considered; lowered due to SM-001/SM-002 being entirely unaddressed)
- [x] First-draft calibration considered — this is a revised draft, not a first draft; post-revision calibration was applied; the revision fixes (6 items) did raise the effective score from what it would have been pre-revision (~0.68 estimated), but significant gaps remain
- [x] No dimension scored above 0.95 without exceptional evidence — highest score is Traceability at 0.83; no dimension exceeded 0.85

**Calibration note:** The S-007 Constitutional score of 0.90 (pre-revision) provides a reference point. Post-revision, the two Major Constitutional findings are fixed, which would have raised the Constitutional score to approximately 1.00 in isolation. However, the broader quality assessment across all six dimensions — incorporating S-003 and S-002 findings — reveals that the Constitutional pass does not translate to an overall quality gate pass. The S-007 score measured a narrower set of compliance principles; the full S-014 rubric applies a broader quality standard. This is the expected relationship between the two scoring instruments.

**Score confidence:** Medium-high. The Evidence Quality dimension score (0.67) carries the highest uncertainty — the actual severity of DA-001 depends on whether the Quick Install path is verified before release. If DA-001 is verified as working, Evidence Quality could rise to 0.72–0.75, lifting the composite to approximately 0.76–0.77. If DA-001 is verified as not working (plugin not yet published), the score would remain at or below 0.67 for that dimension. The current score reflects the acknowledged uncertainty by treating the unverifiable claim as an evidence gap.

---

*Strategy: S-014 LLM-as-Judge*
*Agent: adv-scorer v1.0.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Scored: 2026-02-18*
*Deliverable Revision State: Post-revision (6 fixes applied)*
*Iteration: 1 (first score)*
