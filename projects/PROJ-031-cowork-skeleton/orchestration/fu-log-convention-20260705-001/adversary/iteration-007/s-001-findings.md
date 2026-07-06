# Red Team Report: FEEDBACK-LOG + LLM-DECISION-LOG Jerry Convention (Iteration 7, VERIFIED-CRITICALS pass)

**Strategy:** S-001 Red Team Analysis
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-001, iteration-007, VERIFIED-CRITICALS protocol — blind to iteration-007/008 adversary outputs except `restore-notes.md`, which is readable per the owner's disclosure)
**H-16 Compliance:** `[INFERENCE]` — blind protocol prohibits reading `iteration-007/s-003-findings.md` content; its presence in the directory listing (structural fact, not content) plus the six-round Steelman-family history recorded in the design doc's own Revision Changelog (rows v3–v9, `SM-NNN` findings every round) supports the reasonable inference that S-003 has run this round in the standing tournament sequence. Flagged as inference, not verified evidence, per P-022.

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall Red Team assessment |
| [Threat Actor Profile](#threat-actor-profile) | Adversary goal/capability/motivation |
| [Verification of Iteration-006 Criticals](#verification-of-iteration-006-criticals) | Independent re-check of the 6 Criticals the Restore pass claims closed |
| [Findings Table](#findings-table) | RT-NNN inventory (new this iteration only) |
| [Finding Details](#finding-details) | Expanded Critical/Major findings |
| [Recommendations](#recommendations) | P0/P1/P2 countermeasures |
| [Scoring Impact](#scoring-impact) | Dimension impact mapping |

---

## Summary

This iteration-7 pass runs under the VERIFIED-CRITICALS protocol against a package that has already survived six adversarial rounds and a Restore pass. Per the engagement brief, disclosed residuals are a valid MEDIUM-tier posture and are **not** re-litigated here. This pass did two things: (1) independently re-verified, against the *current* deliverable text (not the Restore notes' self-report), that the six iteration-006 Criticals are actually closed — all six verified closed, no regression; and (2) hunted specifically for genuinely new instances of the package's own recurring failure class (a claim or disclosure that exists at one point but contradicts, or is absent from, an adjacent/cross-referenced location) that six prior rounds have not yet named. One **new, independently-verifiable Critical** and one **new Major** resulted, both wording-only fixes consistent with the deliverable's established anti-bloat remediation pattern; two Minor items are noted for completeness. **Recommendation: REVISE (targeted).**

## Threat Actor Profile

- **Goal:** Exploit a definitional gap in what counts as a "sanctioned" edit to an otherwise-immutable sealed entry — either to challenge the legitimacy of an inconvenient edit after the fact (a compliance-literalist dispute), or to argue that an edit type not clearly enumerated is permissible by omission. Secondary goal: rely on an operator using only the hands-on template (not the rule file or appendix) to miss a disclosure obligation that exists only in the sibling artifacts.
- **Capability:** Same privileged single-writer this design already trusts (full append access to the logs), plus ordinary reading comprehension of the shipped rule file and design doc — no special access required.
- **Motivation:** Avoid the "presence, not veracity" scrutiny discipline that RT-001 (iteration-6) attached to redactions, by disputing whether redaction is a "sanctioned" edit at all under the design's own more structural definition; or benefit from an operator-facing template that never teaches the forward-pointer correction convention its sibling artifact teaches explicitly.

---

## Verification of Iteration-006 Criticals

Re-checked independently against current text (not trusted from `restore-notes.md`'s self-report), per the VERIFIED-CRITICALS mandate:

| # | Iteration-006 Critical/Major | Verified closed at | Status |
|---|---|---|---|
| 1 | RT-001 (redaction carve-out, no size/category discipline) | `staging-feedback-logs/feedback-decision-logs-standards.md:24` ("category... approximate size... presence, not veracity — RT-001"); design doc L1.1 | **Confirmed closed** |
| 2 | RT-002 (LLM-DECISION-LOG missing supersession marker) | design doc line 118; `feedback-decision-logs-standards.md:59`; `LLM-DECISION-LOG.template.md:26` | **Confirmed closed for LLM-DECISION-LOG** — see new finding RT-002-20260706-iter7 below for an asymmetric gap this closure exposed on the FEEDBACK-LOG side |
| 3 | RT-003 (alias-count self-contradiction, "8" vs "5+3") | design doc Adoption plan step 4 (line 255): "5 receive `(alias: —)`... FU.0, FU.1, and FU.2 receive their embedded self-label re-derived" | **Confirmed closed** |
| 4 | RT-004 (absence-≠-nothing caveat) | `feedback-decision-logs-standards.md:3` (rule-file header): "A missing entry is therefore not evidence that nothing happened that turn — treat a gap as unknown, not as negative confirmation (RT-004)." | **Confirmed closed** |
| 5 | DA-001/FM-006 ("Four" safety functions undercount) | design doc "One shared dependency" section: "**Five** safety functions... and the Segment-Index-overflow re-assessment (L1.4)" | **Confirmed closed** (count verified: 5 named) |
| 6 | PM-001/IN-001 (AE-006e false cap-backstop claim) | design doc L1.4 cap row; rule file LOG-M-006: "AE-006e fires on *compaction*... not on cap-crossing" | **Confirmed closed by disclosure** (no automated backstop — matches the restore notes' own framing of this one as a disclosed residual, not a mechanism) |
| 7 | PM-002 (`~N sessions` unfilled placeholder) | design doc Install-stall paragraph: "~3 sessions or 30 days since this review round, or the next milestone checkpoint" | **Confirmed closed** |
| 8 | FM-001 (no inline-doc dedup) | rule file line 51; `FEEDBACK-LOG.template.md:25` | **Confirmed closed** |
| 9 | FM-003 ("verbatim and full" vs. live split-entry practice) | rule file LOG-M-002 (line 24): "a multi-item message MAY split into per-item entries... note the split in Summary" | **Confirmed closed** |

No regression found in any of the nine items above. This matches the Restore notes' own claim; independent verification against current text confirms it holds.

---

## Findings Table

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|-----------------|----------|----------|---------|---------------------|
| RT-001-20260706-iter7 | The identical bolded phrase "the one sanctioned edit to a sealed entry" is applied, verbatim, to **two different mechanisms** (the redaction carve-out, and the `Superseded by:` status pointer) within the same shipping rule file — a direct, unhedged self-contradiction, not an inference | Ambiguity | Medium | Critical | P0 | Missing | Internal Consistency |
| RT-002-20260706-iter7 | `FEEDBACK-LOG.template.md` — the stand-alone, "copy-to-start" operator artifact — never states the `Superseded by: FU.N` forward-pointer convention, unlike its sibling `LLM-DECISION-LOG.template.md` (explicit "Reversal/supersession" bullet) and unlike the design doc's own L1.2 treatment of the DEC-LLM side; an operator working from the template alone has no in-artifact instruction to route a stale FU.N reference forward | Boundary | Medium | Major | P1 | Missing (present only in the rule file and the appendix FAQ, not the template) | Completeness |
| RT-003-20260706-iter7 (Minor, condensed) | The rule-file `stateDiagram-v2` names the in-progress state `IN_PROGRESS` (underscore), while the disposition enum used everywhere else in the package (schema, both templates, appendix, lint check 3) is `IN-PROGRESS` (hyphen); the divergence is undisclosed as a Mermaid-identifier-syntax necessity | Ambiguity | Low | Minor | P2 | Missing | Methodological Rigor |
| RT-004-20260706-iter7 (Minor, condensed) | The two FU.10 Mermaid diagrams are presentation-only (no new content per the design's own framing), but neither diagram carries a text-only fallback for a reader/tool that does not render Mermaid (e.g., a plain-text `cat`/`grep` pass, which the design elsewhere endorses as the primary discovery method for this convention); the surrounding prose independently restates the same rules, so this is a presentation gap, not a content-loss one | Dependency | Low | Minor | P2 | Partial (prose duplicates the ruleset outside the diagram) | Traceability |

---

## Finding Details

### RT-001: "The one sanctioned edit to a sealed entry" is claimed twice, for two different mechanisms, in the same rule file [CRITICAL]

**Attack Vector:** `staging-feedback-logs/feedback-decision-logs-standards.md:24` (LOG-M-002, redaction clause) states: *"This is the **one sanctioned edit to a sealed entry** (design doc L1.1, modeled on the project's own `FU.4` sanitization)"* — describing the **redaction** carve-out. Twenty-nine lines later, the same file at `feedback-decision-logs-standards.md:53` (FEEDBACK-LOG Corrections bullet) states: *"mark the old entry `Superseded by: FU.N` (**the one sanctioned edit to a sealed entry** — a status pointer, not a verbatim change; see appendix)"* — describing a **different** mechanism, the disposition/reversal status pointer. Both sentences use the identical definite-article phrase ("**the** one sanctioned edit"), each without acknowledging the other exists. The same duplicate claim propagates into the design doc: L1.1 (`feedback-decision-log-convention-design.md:65`) says redaction is *"the one exception to sealed-segment immutability (**L1.4**)"* — explicitly directing the reader to L1.4 for corroboration — but L1.4 itself (`feedback-decision-log-convention-design.md:197`, the "Sealed segments" row) says *"The **one sanctioned edit** to a sealed entry is a *status pointer* (`Superseded by: FU.N` / disposition update)"*, with no mention of redaction at all. The L1.1→L1.4 cross-reference therefore points a verifying reader directly at a passage that contradicts the claim it was cited to support. A third instance appears at `feedback-decision-log-convention-design.md:118` (L1.2, DEC-LLM reversal), which repeats the status-pointer framing as "the one sanctioned edit to a sealed entry," and a fourth at `staging-feedback-logs/LLM-DECISION-LOG.template.md:26`. In total: **1 location names redaction as "the one," 4 locations name the status pointer as "the one,"** and none reconciles the count.

**Category:** Ambiguity exploitation (with a Rule Circumvention corollary — see Severity below).
**Exploitability:** Medium — no special access required; any reader comparing LOG-M-002 (line 24) against the FEEDBACK-LOG Corrections bullet (line 53) of the *same file*, or following the L1.1→L1.4 cross-reference in the design doc, encounters the contradiction directly. No inference chain is needed; both are verbatim, bolded claims.
**Severity:** Critical — this is not merely a wording nit. The design doc's own canonical statement of "the one sanctioned edit to a sealed entry" (L1.4, line 197 — the section that defines sealed-segment immutability itself) omits redaction entirely. A literalist reader treating L1.4 as authoritative (it is the section that actually defines what "sealed" and "immutable" mean) could conclude the redaction carve-out is **not** actually sanctioned by the design's own rules — directly undermining the legitimacy of the very redaction-scrutiny discipline that iteration-6's RT-001 fix (category + size disclosure) was built to protect. Conversely, a reader starting from LOG-M-002 could conclude the status-pointer mechanism is *not* "the" sanctioned edit, since LOG-M-002 already claimed that title for redaction. Either reading is defensible from the text as written, which is precisely the ambiguity a bad-faith reviewer or writer could exploit to dispute which edits are legitimate after the fact. This is the same class of gap (an enumeration that undercounts or miscounts a small, named set of exceptions) that iteration-6's DA-001/FM-006 finding ("Four" vs. "Five" safety functions) rated Critical for an analogous reason.
**Existing Defense:** Missing — none of the ≤3 L5 lint checks verify prose-level cross-artifact claim consistency (this is exactly the class of gap the ≤3-lint ceiling cannot catch by design), and no reconciling clause exists anywhere in the reviewed package.
**Evidence:** `staging-feedback-logs/feedback-decision-logs-standards.md:24` vs. `staging-feedback-logs/feedback-decision-logs-standards.md:53` (same file, verbatim phrase collision); `feedback-decision-log-convention-design.md:65` vs. `feedback-decision-log-convention-design.md:197` (explicit cross-reference that does not corroborate); `feedback-decision-log-convention-design.md:118`; `staging-feedback-logs/LLM-DECISION-LOG.template.md:26`.
**Dimension:** Internal Consistency (the count and identity of "the one sanctioned edit" differs by location, with no reconciliation anywhere in the six-file package).
**Countermeasure:** Replace every "the one sanctioned edit to a sealed entry" / "the one exception to sealed-segment immutability" instance with consistent language naming **two** sanctioned edit types to a sealed entry: (a) the redaction carve-out (hygiene, LOG-M-002), and (b) the `Superseded by:` status pointer (correction/reversal routing). A single one-sentence reconciling clause at the L1.4 "Sealed segments" row (the design's canonical definition point) — e.g., "Two edits are sanctioned: a hygiene redaction (L1.1) and a status-pointer update (`Superseded by:`/disposition) — both touch no other verbatim content" — closes all four/five locations' contradiction at its source; the LOG-M-002 and Superseded-by bullets in the rule file, design doc, and template can then each drop "the one" in favor of "one of the two sanctioned edits," or equivalent. Zero new lint, file, or subsystem — a pure wording reconciliation, consistent with the deliverable's own established anti-bloat remediation pattern.
**Acceptance Criteria:** No location in any of the six deliverable files claims to name "the one/only sanctioned edit (or exception)" to a sealed entry without enumerating both the redaction and status-pointer mechanisms; the L1.4 "Sealed segments" row explicitly names both.

### RT-002: FEEDBACK-LOG.template.md never states the `Superseded by: FU.N` convention (asymmetric with the sibling template) [MAJOR]

**Attack Vector:** `staging-feedback-logs/FEEDBACK-LOG.template.md:26` — the file's own "Corrections are append-only" guidance — reads in full: *"On any conflict, **verbatim wins** (secrets/PII excepted — redact before capture, LOG-M-002). Corrections are append-only (convention-only, git-backstopped — not a filesystem lock): to fix a verbatim or reopen a `DONE`, add a new entry referencing the old id."* It stops there. It never instructs the operator/assistant to mark the **old** entry `Superseded by: FU.N`, even though that exact convention is documented in three other places: the rule file (`staging-feedback-logs/feedback-decision-logs-standards.md:53`), the worked FAQ in the appendix (`staging-feedback-logs/examples-appendix.md:172`: *"Add a `Superseded by: FU.N` line to the old entry... so a later reader following a stale cross-reference is routed forward"*), and — for the sibling log — `staging-feedback-logs/LLM-DECISION-LOG.template.md:26`, which carries a full, explicit **"Reversal/supersession"** bullet with its own `RT-002` citation. The design doc's own canonical L1.1 entry-schema section for FEEDBACK-LOG (`feedback-decision-log-convention-design.md`, lines 50–79) likewise never states this convention for the FEEDBACK-LOG side either — it appears only in L1.4's generic "Sealed segments" row (framed around segment sealing, not corrections) and in L1.2's DEC-LLM-NNN-specific clause. `FEEDBACK-LOG.template.md` is billed in the Staged Artifacts table as the "**Copy-to-start template**" — the artifact an operator is expected to use directly, without necessarily also opening the rule file or the appendix.
**Category:** Boundary (a convention that exists at the rule-file/appendix layer does not reach the operator-facing template surface for the FEEDBACK-LOG side, though it does for the LLM-DECISION-LOG side).
**Exploitability:** Medium — arises passively whenever an operator corrects or reopens a FEEDBACK-LOG entry using only the template as a guide; no special action or bad faith required.
**Severity:** Major — this is the exact risk profile iteration-6's RT-002 finding named as Major for the LLM-DECISION-LOG side ("a reader consulting a sealed segment in isolation can act on a decision that was later reversed, with no structural signal that a reversal occurred"). The same risk now applies to FEEDBACK-LOG corrections/reopenings performed by an operator who follows only the template: the old (superseded) entry is left with no forward pointer, and a later reader of that sealed entry in isolation has no signal that a follow-up correction exists.
**Existing Defense:** Missing in the template; Partial at the package level (the rule file and appendix both state the convention correctly, so a reader who consults those artifacts is covered — but the template itself, meant to be self-sufficient for day-to-day use, is not).
**Evidence:** `staging-feedback-logs/FEEDBACK-LOG.template.md:26` (the incomplete Corrections bullet) vs. `staging-feedback-logs/LLM-DECISION-LOG.template.md:26` (the complete, explicit sibling bullet) and `staging-feedback-logs/examples-appendix.md:172` (the FAQ that does state it) and `staging-feedback-logs/feedback-decision-logs-standards.md:53` (the rule-file statement).
**Dimension:** Completeness (the template artifact is missing a documented convention its own sibling artifact carries) / Traceability (a reader of the template alone cannot discover the forward-pointer convention exists).
**Countermeasure:** Add one clause to `FEEDBACK-LOG.template.md`'s Corrections bullet, mirroring the sibling template's wording: *"...add a new entry referencing the old id; mark the old entry `Superseded by: FU.N` (a status pointer — not a verbatim change) so a later reader is routed forward."* Pure wording addition to one bullet; zero new lint, file, or subsystem.
**Acceptance Criteria:** `FEEDBACK-LOG.template.md`'s Corrections bullet states the `Superseded by: FU.N` marker requirement, symmetric with `LLM-DECISION-LOG.template.md`'s "Reversal/supersession" bullet.

### RT-003, RT-004 (Minor — condensed)

- **RT-003 (state-name naming drift in the new diagram):** The rule-file `stateDiagram-v2` (FU.10) uses `IN_PROGRESS` (underscore) as a state identifier, while every other occurrence of this disposition value in the package (schema tables, both templates, the appendix, lint check 3's scope) is written `IN-PROGRESS` (hyphen). This is very likely a Mermaid state-identifier syntax constraint (state names typically cannot contain a bare hyphen), not a deliberate second value — but nothing in the rule file discloses this as a rendering necessity, so a literal reader comparing the diagram against the schema table could wonder whether a second, undocumented disposition value now exists. **Recommendation:** disclosure-only — a parenthetical note near the diagram ("state names use `_` for Mermaid-syntax compatibility; the disposition value itself remains `IN-PROGRESS`") closes this at zero cost (P2).
- **RT-004 (diagram-only presentation dependency):** The two FU.10 diagrams are correctly framed as presentation of existing rules, not new content, and the surrounding prose in both files independently restates the same information in text form — so no information is actually lost if a reader's tool does not render Mermaid (a plain `cat`/`grep` pass, which the design elsewhere recommends as the primary discovery method: "a handful of files are cheap to grep"). This is noted for completeness of the Dependency-category sweep, not as a new content gap (P2, monitor only).

---

## Recommendations

**P0 (Critical — MUST mitigate before acceptance):**
- **RT-001** — Reconcile the "one sanctioned edit to a sealed entry" / "one exception to sealed-segment immutability" language across all four/five locations to name **both** sanctioned edit types (redaction, status pointer). Acceptance: no location claims singularity without enumerating both mechanisms; the L1.4 "Sealed segments" row explicitly names both.

**P1 (Major — SHOULD mitigate):**
- **RT-002** — Add the `Superseded by: FU.N` marker instruction to `FEEDBACK-LOG.template.md`'s Corrections bullet, symmetric with the sibling template. Acceptance: bullet present and worded consistently with `LLM-DECISION-LOG.template.md:26`.

**P2 (Monitor — MAY mitigate):**
- **RT-003** — Disclose the `IN_PROGRESS`/`IN-PROGRESS` Mermaid-syntax naming divergence with a one-line parenthetical near the diagram.
- **RT-004** — No action required; verified that surrounding prose duplicates all diagram content, so no fallback text is needed. Noted for category-sweep completeness only.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | RT-002 — the operator-facing FEEDBACK-LOG template is missing a convention its sibling template states explicitly. |
| Internal Consistency | 0.20 | Negative | RT-001 — a direct, verbatim self-contradiction ("the one sanctioned edit") applied to two different mechanisms within the same shipping rule file, with an explicit cross-reference (L1.1→L1.4) that fails to corroborate. |
| Methodological Rigor | 0.20 | Negative (mild) | RT-003 — an undisclosed naming divergence between the new diagram and the existing schema vocabulary; narrow, cosmetic. |
| Evidence Quality | 0.15 | Neutral | Both P0/P1 findings this round are independently verified by direct, non-inferential textual comparison (exact phrase collision, exact bullet omission); no unsupported claims introduced. |
| Actionability | 0.15 | Neutral | Both countermeasures are one-clause/one-bullet wording additions, matching the deliverable's own established remediation style; no change to the deliverable's actionability rating. |
| Traceability | 0.10 | Negative (mild) | RT-002 was found by tracing the design doc's own claimed symmetry ("same canonical-id/alias rule as FEEDBACK-LOG, FU.6") against the actual template content, where the symmetry did not hold for the correction/supersession convention specifically. |

**Overall assessment:** No finding in this pass invalidates the deliverable's core architecture, and both new findings are one-clause, wording-only fixes — fully consistent with the deliverable's own six-round anti-bloat remediation pattern. RT-001 is rated Critical because it is a direct, verifiable, unhedged self-contradiction (not an inference) inside the artifact that will actually ship and govern (`feedback-decision-logs-standards.md`), and because it functionally muddies the legitimacy boundary of the redaction mechanism iteration-6 just finished hardening. RT-002 is rated Major because it reproduces — on the FEEDBACK-LOG side, in the operator-facing template — the exact risk profile iteration-6's RT-002 finding closed on the LLM-DECISION-LOG side. All nine iteration-006 Criticals/Majors independently re-verified closed; zero regression found. **Recommendation: REVISE (targeted).**

---

## Execution Statistics

- **Total Findings (new this iteration):** 4
- **Critical:** 1 (RT-001)
- **Major:** 1 (RT-002)
- **Minor:** 2 (RT-003, RT-004)
- **Protocol Steps Completed:** 5 of 5 (Threat Actor, Enumerate Attack Vectors, Assess Defense Gaps, Develop Countermeasures, Synthesize/Score Impact)
- **Prior-iteration Criticals/Majors independently re-verified closed:** 9 of 9 (see [Verification of Iteration-006 Criticals](#verification-of-iteration-006-criticals))
