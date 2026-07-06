# Refutation Panel — S-004 Pre-Mortem Analysis (Iteration 8, VERIFIED-CRITICALS Protocol)

> **Lens:** remediation-value — would fixing the Critical materially change adoption outcomes, or is it churn? Fixes that would ADD machinery against the anti-bloat doctrine are REFUTED.
> **Target:** `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-008/s-004-findings.md`
> **Scope:** the 2 Criticals only (PM-001-iter8, PM-002-iter8). Default REFUTED if uncertain.
> **Constitutional:** P-003 no subagents. P-020 draft-only (no writes to `.context/`, `docs/`, `hooks/`). P-022: file+line citations below; inferential reasoning labelled `[INFERENCE]`.

## Navigation

| Section | Purpose |
|---------|---------|
| [PM-001-iter8](#pm-001-iter8-refuted) | CP-01 exception-propagation claim |
| [PM-002-iter8](#pm-002-iter8-verified) | Segment-cap number absent from templates/live logs |
| [Summary](#summary) | Verdict table |

---

## PM-001-iter8: REFUTED

**Claim:** CP-01 (`.context/rules/agent-development-standards.md:382`, "File paths only in handoffs, NEVER inline content") carries no textual exception, so a background/worker agent asked to surface a feedback candidate has no sanctioned path — either it inlines and silently violates the real SSOT, or it follows the real SSOT and the candidate is dropped. Rated Critical/P0, requiring an SSOT edit.

**Verification of the citation:** confirmed accurate — `agent-development-standards.md:382` reads exactly `| CP-01 | File paths only in handoffs, NEVER inline content | MEDIUM | Prevents context duplication; receiving agent loads content via Read |`, and the design doc (`design/feedback-decision-log-convention-design.md:78`) and rule file (`design/staging-feedback-logs/feedback-decision-logs-standards.md:27`) do frame the LOG-M-005 mechanism as "a stated exception to CP-01."

**Why this is refuted on remediation-value grounds:**

1. **CP-01 is MEDIUM-tier, and the framework's own Tier Vocabulary already defines the override mechanism as "documented justification"** (`.context/rules/quality-enforcement.md`, Tier Vocabulary table: `MEDIUM | SHOULD, RECOMMENDED, PREFERRED, EXPECTED | Documented justification | Unlimited`). LOG-M-005 *is* that documented justification, stated in the convention's own governing rule text. The finding treats CP-01 as though it required a literal SSOT-row edit to be overridden, but the framework's existing governance model does not impose that requirement — a project-local rule with a stated rationale already satisfies the override bar. `mcp-tool-standards.md`'s own "Not included" section (eng-\*/red-\* Memory-Keeper exclusion, documented outside the primary tool matrix) is precedent for exactly this pattern: local, disclosed exceptions to a general framework convention, without editing the general convention's own row.
2. **The described payload already fits an existing, universally-sanctioned handoff field.** The design's own framing calls the candidate "a short judgment-bearing text payload returned inline in the handoff's `key_findings`/summary" (design doc L1.1). CP-02 already permits, in *every* handoff, "3-5 key findings bullets" (`agent-development-standards.md:383`) — a 1-3-line candidate is well inside that existing allowance. The self-imposed "exception to CP-01" framing is the design authors' own rhetorical hedge, not a structural gap; recharacterizing the candidate as a normal `key_findings` bullet resolves the apparent tension with zero edits anywhere.
3. **The proposed fix itself cuts against the anti-bloat doctrine this package champions.** The mitigation asks for an edit to a global, cross-skill SSOT file (`agent-development-standards.md`) to accommodate one project's narrow convention — a bigger-footprint, higher-precedent-risk change than anything else in this design, which otherwise deliberately keeps all mechanism disclosure inside its own project-scoped documents. Propagating project-local conventions into global framework files on this basis would itself be scope creep.

Given (1) and (2), the claimed failure mode (silent candidate loss) does not follow from the current text with any real probability, and given (3), the suggested remediation is disproportionate machinery for a self-resolved non-issue. Net remediation value: churn, not a material adoption-outcome change.

---

## PM-002-iter8: VERIFIED

**Claim:** the segment-rotation cap ("~50 entries or ~800 lines") exists only in the rule file (`design/staging-feedback-logs/feedback-decision-logs-standards.md:28`, LOG-M-006) and the design doc (`design/feedback-decision-log-convention-design.md:195`) — never in `FEEDBACK-LOG.template.md`'s Segment Index section or in the live bootstrap `FEEDBACK-LOG.md`, so the artifacts actually read/appended turn after turn carry no numeric trigger for the core anti-truncation safety mechanism.

**Verification by direct read:**
- `design/staging-feedback-logs/FEEDBACK-LOG.template.md` "Log Conventions" (lines 16-26) and "Segment Index" (lines 28-36) confirmed — no cap number anywhere in either section.
- `projects/PROJ-031-cowork-skeleton/FEEDBACK-LOG.md` "Log Conventions (bootstrap)" (lines 18-22) confirmed — no cap number stated; the live file's own text only says "a robust scheme is part of the convention design" (line 20), pointing away from itself rather than stating the number.
- The cap number is confirmed present only at `feedback-decision-logs-standards.md:28` and `feedback-decision-log-convention-design.md:195` (`| **Cap** | Seal the ACTIVE file when it first reaches **~50 entries or ~800 lines**...`), both design-time artifacts, not the runtime templates/live logs.
- No disclosed-residual language matching this specific gap ("template/live log omits the cap") was found anywhere in the design doc (targeted search for "restat"/"cap number"/"not repeated" returned no hits) — this is not a duplicate of an already-accepted residual.

**Why this is verified as high remediation-value, not churn:**

1. **The fix is genuinely zero-machinery** — a one-line restatement of an existing number in two templates plus the two live bootstrap files. No new lint, field, file, or subsystem, fully consistent with the package's own anti-bloat doctrine (the same doctrine cited to refuted PM-001 above).
2. **The gap is not hypothetical** — confirmed as the artifacts' *current* state by direct read, not a 12-months-out projection.
3. **The design's own fallback mechanism already depends on this exact information being in-context.** LOG-M-006 / design doc L1.4's "Cap" row states the interim safety net is that "the assistant SHOULD self-count entries/lines... and proactively propose rotation on approaching the cap" — a mechanism that is only actionable if the assistant knows the number *at the moment it is appending*, i.e., while reading the live log/template rather than the (currently uninstalled) rule file. This is a load-bearing single point of knowledge failure for the mechanism the whole package exists to guarantee (preventing the exact truncation problem, per L1.4's opening problem statement), and the artifacts a session actually touches during normal operation do not carry it.
4. **Low cost, directly serves core purpose** — restating the number where it is actually consumed measurably reduces the risk of re-creating the specific failure (unbounded log growth / context-rot truncation) this design was commissioned to solve, independent of whether the rule file happens to be loaded, trimmed, or not yet installed.

This is a legitimate gap with real adoption-outcome consequences and a near-zero-cost fix; it is not churn.

---

## Summary

| ID | Verdict | One-line basis |
|----|---------|-----------------|
| PM-001-iter8 | REFUTED | CP-01 is MEDIUM-tier and already override-able via documented justification (which LOG-M-005 provides); the candidate already fits CP-02's existing key_findings allowance; the proposed SSOT edit is itself disproportionate, precedent-risky machinery for a self-resolved non-issue. |
| PM-002-iter8 | VERIFIED | Confirmed by direct read that neither template nor live bootstrap log states the cap number the design's own fallback (self-count) mechanism depends on; fix is a one-line, zero-machinery restatement with direct bearing on the package's core anti-truncation purpose. |
