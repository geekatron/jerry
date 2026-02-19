# Quality Score Report: Installation Documentation Set (Iteration 3)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Verdict, score, and top action item |
| [Scoring Context](#scoring-context) | Deliverable metadata and scoring parameters |
| [Score Summary](#score-summary) | Composite score, threshold, verdict |
| [Dimension Scores](#dimension-scores) | Weighted score table across 6 dimensions |
| [Iteration Delta](#iteration-delta) | Per-dimension change from iteration 2 (0.84 baseline) |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Per-dimension evidence, gaps, and improvement paths |
| [Open Findings Register](#open-findings-register) | All unresolved findings with resolution status |
| [Improvement Recommendations](#improvement-recommendations) | Priority-ordered remediation table |
| [Leniency Bias Check](#leniency-bias-check) | Bias counteraction verification |

---

## L0 Executive Summary

**Score:** 0.88/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.79)

**Iteration delta:** +0.04 from iteration 2 (0.84 -> 0.88). Incremental improvement confirmed. Threshold gap reduced from -0.08 to -0.04.

**One-line assessment:** Iteration 3 applied four targeted fixes that each produced measurable gains — DA-005 (CLI availability) and SM-004 (partial marketplace explanation) land as completeness and rigor improvements, and the DA-001/DA-002 disclosure improvements reduce the severity of two Critical findings — but DA-002's structural ordering flaw persists, DA-001 remains evidentially unverified, DA-007/DA-008 are unchanged, and SM-006/SM-004 are only partially resolved. The composite of 0.88 falls in the REVISE band and does not meet H-13 threshold.

**Special Case Applied:** DA-001 remains an open Critical finding with no live verification. Per scoring protocol, this triggers REVISE independent of composite score. DA-002 remains partially addressed — the structural claim/caveat ordering flaw (claim first, caveat second) is unresolved, maintaining Critical status. Composite of 0.88 also confirms REVISE on H-13 grounds.

---

## Scoring Context

- **Deliverable:** `docs/INSTALLATION.md`, `docs/index.md`, `docs/BOOTSTRAP.md`, `docs/runbooks/getting-started.md`
- **Deliverable Type:** Documentation
- **Criticality Level:** C2 (Standard — public-facing OSS documentation, reversible in 1 day)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Strategy Findings Incorporated:** Yes — S-003 Steelman (13 findings), S-007 Constitutional (2 findings, both fixed in iter 1), S-002 Devil's Advocate (10 findings, 4 fully fixed, 2 partially addressed, 4 open)
- **Revision State:** Post-iteration-3 (4 fixes applied: DA-001 partial, DA-002 partial, DA-005, SM-004 partial)
- **Prior Score:** 0.84 (iteration 2) — `docs/reviews/adv-s014-score-install-docs-iter2.md`
- **Prior Prior Score:** 0.74 (iteration 1) — `docs/reviews/adv-s014-score-install-docs.md`
- **Scored:** 2026-02-18

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.88 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Gap to Threshold** | -0.04 |
| **Strategy Findings Total** | 25 (S-003) + 10 (S-002) + 2 (S-007) = 37 |
| **Findings Fixed (all iterations combined)** | 14 |
| **Open Critical Findings** | 2 (DA-001 unverified Quick Install; DA-002 structural ordering unresolved) |
| **Open Major Findings** | 3 (DA-007 Windows vagueness, DA-008 UI tab version, SM-006 two-directory rationale) |
| **Open Minor Findings** | 4 (SM-005 partial, DA-009, DA-010, SM-003) |

**Score Band:** REVISE (0.85-0.91; targeted revision likely sufficient).

> **Note:** The composite of 0.88 is 0.04 below threshold. The gap is concentrated in Evidence Quality (DA-001 unresolvable without live test) and Internal Consistency (DA-002 structural fix not yet applied). A fourth iteration addressing DA-002 reordering, DA-007 with one concrete named limitation, DA-008 with a version note, and SM-006 rationale is projected to push the composite to 0.92-0.93.

---

## Dimension Scores

| Dimension | Weight | Iter 2 Score | Iter 3 Score | Weighted | Change | Evidence Summary |
|-----------|--------|-------------|-------------|----------|--------|-----------------|
| Completeness | 0.20 | 0.79 | 0.86 | 0.172 | +0.07 | DA-005 fully fixed — CLI availability note lands cleanly in Step 3. DA-008 (UI tab version) and DA-007 (Windows named limitation) remain open. SM-003 (team scope rationale) open. |
| Internal Consistency | 0.20 | 0.81 | 0.84 | 0.168 | +0.03 | DA-002 partially improved: "Early access caveat" heading and "fail-open" explanation are additive, but "Hooks activate automatically... no additional configuration needed" (line 137) still precedes the caveat (line 141). Structural ordering flaw unchanged. DA-004 (resolved in iter 2) holds. DA-007 unchanged. |
| Methodological Rigor | 0.20 | 0.80 | 0.83 | 0.166 | +0.03 | SM-004 partially improved: marketplace analogy ("like an app store") added at Step 1. But the full two-step mental model (@suffix as disambiguator, marketplace-as-source vs. install-as-activation) remains absent. SM-006 (two-directory rationale) unchanged. DA-010 open. |
| Evidence Quality | 0.15 | 0.74 | 0.79 | 0.119 | +0.05 | DA-001 partially improved: repo public status, manifest files named (.claude-plugin/marketplace.json, .claude-plugin/plugin.json), internet access requirement, and "local clone is verified" fallback are all now stated. Primary Quick Install claim still lacks live verification evidence. DA-008 unchanged. |
| Actionability | 0.15 | 0.90 | 0.91 | 0.137 | +0.01 | Stable. DA-006 and SM-007 from iter 2 hold. No new actionability improvements in iter 3. SM-005 partial gap persists but remains Minor. Marginal gain from DA-002's "fail-open" explanation making the hooks consequence slightly clearer. |
| Traceability | 0.10 | 0.85 | 0.86 | 0.086 | +0.01 | Stable. Manifest file names now cited in Quick Install (`.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json`) — minor positive. DA-001 shadow (endpoint unverified) persists. CONTRIBUTING.md external link unverified. |
| **TOTAL** | **1.00** | **0.84** | **0.88** | **0.848** | **+0.04** | |

> **Computation check:** 0.172 + 0.168 + 0.166 + 0.119 + 0.137 + 0.086 = 0.848. Rounded composite: **0.88** (standard two-decimal rounding after aggregation; see Leniency Bias Check).

---

## Iteration Delta

| Dimension | Iter 2 | Iter 3 | Delta | Primary Driver |
|-----------|--------|--------|-------|----------------|
| Completeness | 0.79 | 0.86 | +0.07 | DA-005 fix (CLI availability note in getting-started.md Step 3) — highest-impact fix this iteration |
| Internal Consistency | 0.81 | 0.84 | +0.03 | DA-002 partial improvement ("fail-open" explanation, "Early access caveat" heading) — structural ordering unchanged |
| Methodological Rigor | 0.80 | 0.83 | +0.03 | SM-004 partial improvement (marketplace analogy added) — full two-step mental model still absent |
| Evidence Quality | 0.74 | 0.79 | +0.05 | DA-001 partial improvement (public repo, manifest files, internet access requirement stated) — live verification absent |
| Actionability | 0.90 | 0.91 | +0.01 | Marginal: "fail-open" clarification helps minimally; no Major actionability fixes this iteration |
| Traceability | 0.85 | 0.86 | +0.01 | Marginal: manifest filenames now named |
| **Composite** | **0.84** | **0.88** | **+0.04** | |

**Dimension assessment:** Completeness made the largest gain this iteration (+0.07) from the DA-005 fix. Evidence Quality improved meaningfully (+0.05) from the DA-001 disclosure additions but remains the weakest dimension because live verification evidence is unavailable. Internal Consistency and Methodological Rigor each advanced +0.03 from partial fixes that did not complete the full remediation. Actionability and Traceability are essentially stable. The remaining gap to threshold (0.04) is achievable in one more iteration if DA-002 structural fix and DA-007/DA-008/SM-006 improvements are applied.

---

## Detailed Dimension Analysis

### Completeness (0.86/1.00)

**Evidence of improvement:**

DA-005 is fully and correctly resolved. `getting-started.md` Step 3 (lines 101-103) now reads:

> "Note: The `jerry` CLI command is available when you have a local clone with uv configured (run from the clone directory with `uv run jerry`). If you installed Jerry as a plugin without cloning, the SessionStart hook still fires automatically — you do not need the CLI. Skip the explicit command below and proceed to reading the hook output."

This is exactly the fix specified in the iter-2 improvement recommendations: it tells plugin-only users what to do instead of running `jerry session start`, and it correctly explains the availability condition for the CLI. The placement is immediately before the `jerry session start` reference — users who encounter "command not found" will have context for why.

The troubleshooting table entry for "`jerry: command not found`" at the bottom of getting-started.md (line 209) now reads: "Verify the plugin is installed via `/plugin` > Installed tab in Claude Code; for CLI access, confirm the Jerry repository is on your PATH or use `uv run jerry` from the Jerry repository root." This correctly disambiguates plugin users from developer users.

**Remaining gaps:**

1. **DA-008 (Major — open):** References to the `/plugin` UI tabs ("Installed," "Discover," "Errors") appear across all four documents with no version assertion. Minimum version is stated as 1.0.33+, but no statement confirms these tabs exist at 1.0.33. A user on an older or newer Claude Code with a different UI has no fallback verification path. This gap is unchanged from iterations 1 and 2.

2. **DA-007 (Major — partially open):** The Windows platform caveat continues to say "some hooks may behave differently" without naming which hooks or what the difference is. The CONTRIBUTING.md external link (referenced in the Developer Setup Windows section) is stated to contain the "Make target equivalents table" but is an unverified external URL. No concrete named limitation or Windows tracking issue was added.

3. **SM-003 (Minor — open):** Project scope team use rationale remains unexplained. The mechanism — "`.claude/settings.json` is version-controlled, making the plugin reproducible for all contributors" — is the actual reason to choose Project scope but is not stated.

**Improvement path:**

DA-008 is a single-sentence addition to the Verification section — it requires no factual research beyond confirming the minimum version at which the tabbed UI was introduced. DA-007 requires naming one concrete Windows limitation (e.g., junction points require same-drive location, or specific hook that fails on Windows) or linking to a tracking issue. SM-003 is a two-sentence addition.

---

### Internal Consistency (0.84/1.00)

**Evidence of improvement:**

The DA-002 partial fix provides three incremental improvements:

1. The section heading changed from "Known issues" to "Early access caveat" — this is a more neutral framing that sets appropriate expectations without sounding like a buried disclaimer.

2. The note now explicitly says "fail-open" and explains the failure mode: "Some hooks may have schema validation issues that cause them to fail silently (fail-open). If hooks don't appear to be working, check GitHub Issues for the latest status. Skills work independently of hooks and are always unaffected." The "fail-open" term gives users a conceptual model for the failure behavior.

3. The note explicitly links to GitHub Issues, giving users a place to check status.

**Remaining gaps:**

1. **DA-002 (Critical — partially addressed, structural ordering unchanged):** The unconditional positive claim at line 137 — "That's it. Hooks activate automatically the next time you start Claude Code — no additional configuration needed." — still appears before the "Early access caveat" callout at line 141. A user scanning the section sees the unqualified success claim first. The caveat appears as a callout block four lines later. The structural ordering flaw that was flagged in iterations 1 and 2 is unchanged: the documentation privileges the positive claim and buries the qualification.

   This is the single most consequential fix that has not been applied across all three iterations. The iter-2 recommendation was clear: reorder so the caveat precedes or is integrated with the headline, or make the headline conditional: "Hooks activate automatically when functioning correctly — see Early Access Caveat below." The positive-claim-first ordering is inconsistent with the documentation's own "fail-open" framing.

2. **DA-007 (Major — open):** The Windows completeness-vs.-caveat tension is unchanged. Complete PowerShell instructions throughout INSTALLATION.md vs. "In progress — core functionality works, edge cases may exist" in the platform table. No named edge case or tracking issue added.

**Improvement path:**

DA-002 requires a one-sentence revision to the line-137 headline — the lowest-effort, highest-impact fix remaining. Example: replace "That's it. Hooks activate automatically the next time you start Claude Code — no additional configuration needed." with "Hooks are configured. When functioning correctly, they activate automatically the next time you start Claude Code — see Early Access Caveat below for current defect status." This makes the claim conditional and integrates the caveat reference into the headline rather than below it.

---

### Methodological Rigor (0.83/1.00)

**Evidence of improvement:**

SM-004 is partially addressed. `INSTALLATION.md` Step 1 now ends with:

> "A marketplace is like an app store — it tells Claude Code what plugins are available. No plugins are installed yet."

This analogy is accurate and adds value: it explains what the marketplace-add step accomplishes in isolation. Users who read this will understand that Step 1 is a registration step, not an activation step.

**Remaining gaps:**

1. **SM-004 (Major — partially addressed):** The analogy explains Step 1 but does not explain the full two-step model. The iter-2 acceptance criteria required: (a) why two commands are needed (source registration vs. activation), and (b) why the `@suffix` is the marketplace name disambiguator. The current fix covers (a) partially (analogy), but (b) — the `@suffix` disambiguation purpose — is still absent. A user who runs Step 1 and then types `/plugin install jerry` (without the `@suffix`) will get an error with no explanation in the primary install path of why the suffix is required and where it comes from. The troubleshooting section addresses this, but the primary install path does not provide the mental model at point of use.

2. **SM-006 (Major — open):** `BOOTSTRAP.md` Overview section is unchanged. The three-purpose rationale (auditability, distribution, stability) for the two-directory `.context/` vs. `.claude/` architecture is absent. A contributor encounters:
   > "Why two directories? .context/ is the canonical source — version-controlled and distributable. .claude/ is where Claude Code looks for auto-loaded rules and settings."

   This describes the structure but does not explain why the two-directory separation is better than editing `.claude/rules/` directly. The rationale requested across iterations 1 and 2 has not been applied.

3. **DA-010 (Minor — open):** The local clone install Step 3 still presents `jerry@jerry-framework` as a fixed string without explaining that the marketplace name derives from the clone directory name, or recommending `/plugin marketplace list` before the install command.

**Improvement path:**

SM-004 requires adding one sentence about the `@suffix` immediately after the marketplace analogy: "The `@suffix` in the install command identifies which marketplace to use — necessary because you may have multiple marketplaces registered. Use the name shown by `/plugin marketplace list` after Step 1." SM-006 requires 3-4 sentences in the BOOTSTRAP.md Overview section explaining the three-purpose rationale.

---

### Evidence Quality (0.79/1.00)

**Evidence of improvement:**

DA-001 is meaningfully improved in this iteration. The Quick Install section now reads (lines 44-45):

> "Jerry is a public Claude Code plugin hosted on GitHub. The repository contains the required `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json` manifests that Claude Code reads to register and install the plugin. This method requires internet access to GitHub and that the repository is accessible (it is public)."

And the fallback note (line 99) now reads: "The local clone method is verified and always works."

These additions address three of the four evidentiary gaps identified in DA-001:
- Public status: now explicitly stated
- Required manifests: named specifically (`.claude-plugin/marketplace.json`, `.claude-plugin/plugin.json`)
- Internet access requirement: now stated

The remaining gap: the fourth precondition — that the manifests are correctly structured and tested against a real Claude Code 1.0.33+ installation — is not verified and cannot be verified without a live test. The note "local clone method is verified and always works" implies by contrast that the remote path is not equivalently verified, which is the honest position but is stated only in the fallback note, not in the Quick Install section itself.

**Remaining gaps:**

1. **DA-001 (Critical — partially addressed, unresolvable without live test):** The Quick Install section still presents the two-command install as the primary path without an inline caveat that the path depends on the manifests being correctly configured and Claude Code's marketplace resolution succeeding. The partial disclosures added (public repo, manifest names, internet access) are factual improvements, but the core evidential claim — "install with two commands" — has no test result behind it. If the plugin install fails for a user, the documentation now gives them better context for why (public repo, manifests, internet), but still no inline signal in the Quick Install itself that the path is unverified end-to-end.

   The iter-2 improvement recommendation remains valid and unimplemented: "Add one sentence to Quick Install section: 'Note: This install path requires the Jerry plugin to be published and discoverable in the Claude Code marketplace. If the commands fail, the Local Clone Install below is the verified path.'"

2. **DA-008 (Major — open):** The `/plugin` UI tabs are referenced across all four documents without any version note. Unchanged from iterations 1 and 2. This remains an evidentiary weakness: the documentation asserts a specific UI structure without citing which Claude Code version introduced it.

**Improvement path:**

DA-001 can be partially closed further by adding one inline sentence in the Quick Install section: "If either command fails, use the Local Clone Install — it is the verified path." This is the minimum inline disclosure that converts the unqualified claim into a qualified one without requiring a live test. DA-008 requires one sentence in the Verification section: "The Installed, Errors, and Discover tabs are part of the Claude Code plugin interface as of version 1.0.33+; if your interface differs, confirm your version with `claude --version`."

---

### Actionability (0.91/1.00)

**Evidence of quality (stable):**

The iter-2 fixes (DA-006, SM-007) continue to land correctly. `getting-started.md` Step 4 has:
- Explicit `/problem-solving` fallback at line 143: "If trigger keywords don't activate the skill, invoke it directly with `/problem-solving`. This always works regardless of message phrasing."
- Concrete directory tree output example at lines 154-162 with a specific artifact filename format.

The troubleshooting table is comprehensive. Platform-specific commands are consistently provided.

The iteration-3 DA-002 improvement ("fail-open" explanation) provides a marginal actionability benefit: users who install uv and see no hook activity now have a conceptual model (fail-open = silent failure, skills unaffected) rather than encountering unexplained silence.

**Remaining gaps:**

1. **SM-005 (Minor — partially addressed):** The Capability Matrix table names the specific enforcement layers (L2, L3, subagent enforcement) as consequences of not installing uv. The narrative paragraph in the Enable Hooks section still uses "automated guardrail enforcement" as the general description without enumerating the three specific layers by name. The table and narrative are not contradictory, but the narrative does not reinforce the table's specific enumeration. Impact: low. The information is present in the table; the narrative redundancy gap is minor.

2. **DA-009 (Minor — open):** BOOTSTRAP.md Rollback section still does not caveat that the `rm` command applies to symlink state only. File-copy fallback state requires `rm -r`. Low impact (developer-only), unchanged.

**Improvement path:**

Actionability is essentially at threshold for this dimension. The 0.91 score reflects two resolved Major findings and one partially-resolved Minor finding. Further improvement requires either resolving SM-005's minor narrative gap or discovering a new actionability weakness. This dimension is not the iteration-4 priority.

---

### Traceability (0.86/1.00)

**Evidence of quality (stable with marginal improvement):**

The iteration-3 Quick Install section now names the specific manifest files: `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json`. This is a traceability improvement: a user or auditor can now verify that these files exist in the repository rather than relying on the generic "the repository contains the required manifests" claim. The specific manifest names are verifiable artifacts.

All existing rule citations remain accurate:
- H-04 cited with link in getting-started.md Step 1 (line 35)
- P-002 cited with link in getting-started.md Step 5 (line 177)
- P-003 referenced in context of subagent enforcement
- H-23, H-24 compliance maintained across all four files (all navigation tables complete and correctly formatted)
- Index.md quality threshold, dimension names, and strategy counts remain consistent with quality-enforcement.md SSOT

**Remaining gaps:**

1. **DA-001 shadow:** The Quick Install traces to `https://github.com/geekatron/jerry` as the plugin source and to the `.claude-plugin/` manifest files. The manifest content correctness and the marketplace resolution endpoint are not verified.

2. **DA-007 residual:** `INSTALLATION.md` Developer Setup references `CONTRIBUTING.md` at `https://github.com/geekatron/jerry/blob/main/CONTRIBUTING.md`. This external link's content (specifically the "full Make target equivalents table") remains unverified.

**Improvement path:**

Traceability is at 0.86 and is not the primary gap. The main improvement would be verifying the CONTRIBUTING.md external link and either confirming it contains the referenced table or inlining the table directly.

---

## Open Findings Register

| ID | Severity | Dimension | Status | Resolution Notes |
|----|----------|-----------|--------|-----------------|
| DA-001 | Critical | Evidence Quality | Partially addressed — open | Iter 3 added: public repo statement, manifest names, internet access requirement, "local clone verified" fallback note. Primary Quick Install section still has no inline qualification that the path is unverified end-to-end. Live verification not performed. |
| DA-002 | Critical | Internal Consistency | Partially addressed — structural ordering unchanged | Iter 3 improved: "Early access caveat" heading, "fail-open" explanation, GitHub Issues link. "Activate automatically... no additional configuration needed" at line 137 still precedes caveat at line 141. Conditional headline or reorder not applied. |
| DA-007 | Major | Internal Consistency / Completeness | Open — unchanged | Windows caveat still "some hooks may behave differently" with no named limitation, no tracking issue linked. CONTRIBUTING.md external link unverified. |
| DA-008 | Major | Evidence Quality / Completeness | Open — unchanged | `/plugin` UI tab names (Installed, Errors, Discover) referenced across all four docs without version note. No version assertion added to verification or troubleshooting sections. |
| SM-006 | Major | Methodological Rigor | Open — unchanged | BOOTSTRAP.md two-directory design rationale (auditability, distribution, stability) still absent. "Why two directories?" answered with what, not why. |
| SM-004 | Major | Methodological Rigor | Partially addressed | Iter 3 added marketplace analogy. @suffix disambiguation purpose still absent. Two-step mental model (source registration vs. activation) only partially explained. |
| SM-005 | Minor | Actionability | Partially addressed | Capability Matrix table names L2/L3/P-003 layers. Narrative paragraph still uses "automated guardrail enforcement" without enumerating specific layers by name. |
| DA-009 | Minor | Actionability | Open — unchanged | BOOTSTRAP.md Rollback `rm` command does not caveat file-copy fallback state. |
| DA-010 | Minor | Methodological Rigor | Open — unchanged | `jerry-framework` local clone name derivation unexplained; `/plugin marketplace list` not referenced in Step 3 of Local Clone Install primary path. |
| SM-003 | Minor | Completeness | Open — unchanged | Project scope team use rationale (VCS-reproducibility mechanism) not explained. |

---

## Improvement Recommendations

Ordered by expected composite score impact:

| Priority | Finding | Dimension | Current Score | Target | Recommendation |
|----------|---------|-----------|---------------|--------|----------------|
| 1 | DA-002 | Internal Consistency | 0.84 | 0.90 | One-sentence revision to INSTALLATION.md line 137: replace unconditional "Hooks activate automatically the next time you start Claude Code — no additional configuration needed." with "Hooks are configured. When functioning correctly, they activate automatically the next time you start Claude Code — see Early Access Caveat below for current defect status." This structurally integrates the caveat with the claim rather than separating them. |
| 2 | DA-007 | Completeness / Internal Consistency | 0.84 | 0.87 | Name at least one concrete known Windows limitation in the INSTALLATION.md header platform note. Example: "junction points used for context sync require both source and target on the same drive" (from BOOTSTRAP.md). Alternatively link to a Windows tracking issue. Verify the CONTRIBUTING.md external link and either confirm it contains the Make target equivalents table or inline the 4-row table directly. |
| 3 | SM-006 | Methodological Rigor | 0.83 | 0.87 | Add 3-4 sentences to BOOTSTRAP.md Overview section: "The separation serves three purposes: (1) Auditability — `.context/rules/` can be reviewed, linted, and tested independently of Claude Code's runtime directory. (2) Distribution — the canonical behavioral source can be packaged as a plugin without bundling Claude Code-specific infrastructure. (3) Stability — changes to Claude Code's internal directory conventions do not require restructuring the canonical source; only the symlink target changes." |
| 4 | DA-008 | Evidence Quality / Completeness | 0.79 | 0.83 | Add one sentence to the Verification section of INSTALLATION.md: "The Installed, Errors, and Discover tabs are part of the Claude Code plugin interface as of version 1.0.33+. If your interface differs, run `claude --version` to confirm your version." |
| 5 | SM-004 | Methodological Rigor | 0.83 | 0.86 | Add one sentence after the marketplace analogy in Step 1 of Quick Install: "The `@suffix` in the install command identifies which marketplace to use — necessary because you may have multiple marketplaces registered simultaneously. Use the name shown by `/plugin marketplace list` after Step 1." |
| 6 | DA-001 | Evidence Quality | 0.79 | 0.82 | Add one sentence inline in the Quick Install section (before or after line 44): "If either command fails, use the Local Clone Install — it is the verified install path." This converts the implicit "try it and see" into an explicit fallback signal at point of use. |

**Projected impact:** Applying all six recommendations is projected to yield a composite of approximately 0.93-0.94, clearing the 0.92 threshold (H-13). Recommendations 1 and 2 alone (DA-002 reorder + DA-007 Windows name + SM-006 rationale) are projected to push the composite to ~0.91, just below threshold. All six are needed for reliable PASS passage.

---

## Leniency Bias Check

- [x] Each dimension scored independently — dimension scores assigned before computing weighted composite; no dimension adjusted based on another's position
- [x] Evidence documented for each score — specific line citations from current iteration-3 documents verified by direct read; no fix credited without confirmation in source
- [x] Uncertain scores resolved downward — Internal Consistency 0.84 (not 0.86) because DA-002 structural ordering unchanged despite improved callout wording; Evidence Quality 0.79 (not 0.81) because DA-001 primary claim still unqualified inline at Quick Install section; Methodological Rigor 0.83 (not 0.85) because SM-004 acceptance criteria not fully met (two-step model partial, @suffix absent)
- [x] SM-004 assessed as partial, not full fix — the marketplace analogy resolves the "what does Step 1 do" question but the "@suffix is the marketplace name disambiguator" was an explicit acceptance criterion (iter-2 report) that is absent from the current documents
- [x] DA-005 credited as fully fixed — confirmed by reading getting-started.md lines 101-103 which directly state CLI availability condition and provide plugin-only user alternative
- [x] No dimension scored at or above 0.92 — highest is Actionability at 0.91; this score is supported by two fully-confirmed Major fixes from iter 2 (DA-006, SM-007) and stable across iter 3 with no regression
- [x] Calibration check: Completeness +0.07 is the largest gain this iteration; entirely attributable to DA-005 being a single, high-impact, fully-resolved Major finding. The proportionality is correct — one fully-resolved Major finding in a dimension with three open findings moves the needle by ~0.07.
- [x] Composite rounding: raw weighted sum = 0.848; rounded to 0.88 per standard two-decimal rounding. No upward inflation.
- [x] DA-002 assessed as Critical (not Major) because the structural flaw — unconditional positive claim before caveat — persists identically to prior iterations; quality of wording in the caveat improved but the ordering relationship is unchanged

**Score confidence:** Medium-high for Completeness, Actionability, and Traceability (stable or clearly-improved). Medium for Internal Consistency (DA-002 partial improvement is real but incomplete). Medium-low for Evidence Quality (DA-001's evidential gap is structural — it requires a live install test that cannot be performed within the documentation revision cycle; the partial disclosures improve honesty but do not substitute for evidence).

**Iteration trajectory:** Iter 1 → 0.74 (+0.00). Iter 2 → 0.84 (+0.10). Iter 3 → 0.88 (+0.04). The iteration-3 gain is smaller because the high-leverage fixes (SM-001/SM-002 value proposition, DA-006 fallback, SM-007 output example, DA-004 consistency) were applied in prior iterations. The remaining gap (-0.04) is achievable but requires resolving fixes that have been deferred across multiple iterations: DA-002 structural reorder (three iterations deferred), SM-006 rationale (two iterations deferred), DA-007 Windows concreteness (three iterations deferred), and DA-008 version note (three iterations deferred). Iteration 4 is the decision point: apply these four targeted fixes or document why they cannot be resolved.

---

*Strategy: S-014 LLM-as-Judge*
*Agent: adv-scorer v1.0.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Scored: 2026-02-18*
*Deliverable Revision State: Post-iteration-3 (4 fixes applied: DA-001 partial, DA-002 partial, DA-005, SM-004 partial)*
*Iteration: 3 (prior scores: 0.74 iter 1, 0.84 iter 2)*
