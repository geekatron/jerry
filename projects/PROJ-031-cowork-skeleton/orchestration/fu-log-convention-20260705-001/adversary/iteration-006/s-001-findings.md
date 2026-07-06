# Red Team Report: FEEDBACK-LOG + LLM-DECISION-LOG Jerry Convention (Iteration 6)

**Strategy:** S-001 Red Team Analysis
**Deliverable:** `design/feedback-decision-log-convention-design.md` + `design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-001, iteration-006, blind protocol — no prior-iteration adversary files read)
**H-16 Compliance:** `[INFERENCE]` — blind protocol prohibits reading prior `adversary/` iteration outputs, so no direct S-003 artifact was inspected this pass. The deliverable's own Revision Changelog (design doc, rows v3–v7) discloses that Steelman-family findings (`SM-NNN`) have run in every one of the five prior tournament rounds on this same package, and this is a continuing C4 tournament sequence (iterations 1–5 already completed with RT/DA/SM/CC/PM/CV/FM/IN findings addressed). Proceeding on the reasonable inference that S-003 has already been applied in this tournament's standing sequence; flagged as an inference, not verified evidence, per P-022.

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall Red Team assessment |
| [Threat Actor Profile](#threat-actor-profile) | Adversary goal/capability/motivation |
| [Findings Table](#findings-table) | RT-NNN inventory |
| [Finding Details](#finding-details) | Expanded Critical/Major findings |
| [Recommendations](#recommendations) | P0/P1/P2 countermeasures |
| [Scoring Impact](#scoring-impact) | Dimension impact mapping |

---

## Summary

This iteration-6 Red Team pass targets a heavily-hedged, extensively self-disclosing MEDIUM-tier convention (append-only feedback/decision ledgers) that has already survived 5 remediation rounds. Per the user's framing, a MINIMAL package with honestly-disclosed residuals is a valid posture — this pass therefore does **not** re-litigate the many already-disclosed residuals (concurrent-writer last-write-wins race, `--no-verify` lint bypass, transcript-retention dependency, Q5 silent-non-capture) which are, on inspection, thoroughly and consistently propagated across all five artifacts and honestly scoped. Instead, this pass hunted specifically for (a) genuinely new attack surfaces the prior five rounds have not yet named, and (b) fresh instances of the package's own recurring failure class — a disclosure existing somewhere but not where a claim is made, or an overclaim contradicting an adjacent hedge (the exact pattern named by the design doc's own changelog, rounds v3–v7). One Critical and three Major findings resulted, plus three lower-materiality Minor findings. **Recommendation: REVISE (targeted).** All four P0/P1 countermeasures are one-line-to-one-field wording/schema additions consistent with the deliverable's own established anti-bloat remediation pattern — no new lint, file, or subsystem is required for any finding in this report.

## Threat Actor Profile

- **Goal:** Quietly alter or suppress the historical record (feedback or decision) this convention exists to protect, while preserving a plausible appearance of compliance with "verbatim wins" / "append-only, git-backstopped" — or exploit a schema/instruction gap to cause a governance-relevant misread of the log's completeness.
- **Capability:** Full write access to the log files (the convention's own threat model already assumes a trusted single-writer session/operator with append privileges — this actor is *that* same privileged party, acting in bad faith or carelessly, not an external intruder).
- **Motivation:** Avoid the friction/accountability of the graduation, evidence-link, or disposition disciplines; or simply benefit from an install-time / cross-artifact inconsistency that a careless implementer follows literally.

---

## Findings Table

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|-----------------|----------|----------|---------|---------------------|
| RT-001-20260706-iter6 | Redaction carve-out (the *one* sanctioned edit to a sealed entry) has no size/category discipline, no lint coverage, and no "presence not veracity" disclosure — unlike every other trust-sensitive mechanism in this design — so it is a lower-scrutiny channel to launder substantive content tampering as "hygiene" | Rule Circumvention | Medium | Critical | P0 | Partial (git diff exists; reviewer suspicion is structurally lowered for a *sanctioned* edit class) | Internal Consistency |
| RT-002-20260706-iter6 | LLM-DECISION-LOG has no `Superseded by:` / reversal marker, unlike FEEDBACK-LOG — a later decision that reverses an earlier `DEC-LLM-NNN` leaves no forward pointer, so a reader consulting a sealed entry can act on a stale/reversed decision | Boundary | Medium | Major | P1 | Missing | Completeness |
| RT-003-20260706-iter6 | Design doc Adoption plan step 4 claims "8 of 13... receive a freshly-added `(alias: —)`" then immediately carves out re-derivation for embedded self-labels — verified against the live bootstrap files, 3 of those 8 (`FU.0`, `FU.1`, `FU.2`) *do* embed a self-label matching their own canonical id, so the "8" headline count contradicts its own parenthetical exception for the entries with the highest provenance value | Ambiguity | Low | Major | P1 | Missing (plain prose, no lint applies) | Evidence Quality |
| RT-004-20260706-iter6 | Nothing in the package states that a missing log entry is not evidence that no reportable feedback/decision occurred that turn; Q5 discloses the capture gap itself but not this governance-relevant *reader-side* misinterpretation risk | Ambiguity | Medium | Major | P1 | Partial (Q5 discloses the gap exists, not the misread risk) | Methodological Rigor |
| RT-005-20260706-iter6 | The H-31 back-reference enumeration is scoped per-log; an operator who reuses the same turn-local label (e.g. `FU.0`) across both logs in one session creates a cross-log alias ambiguity the enumeration procedure never names | Ambiguity | Low | Minor | P2 | Missing | Completeness |
| RT-006-20260706-iter6 | Capture-trigger recognition (5 categories, esp. interrogative/challenge cues) is a judgment call by the *currently active* model; model swaps are already tracked in Context (`claude-opus-4-8` → `claude-fable-5`, this project's own history) but reliability drift of trigger recognition across a swap is never named as a degradation risk | Degradation | Low | Minor | P2 | Missing | Methodological Rigor |
| RT-007-20260706-iter6 | Concurrent-writer last-write-wins race remains technically undefended (no lock, no lease) — already extensively and consistently disclosed across all five artifacts; included here for completeness of the 5-category sweep, not as a new gap | Dependency | High | Minor | P2 | Partial (procedural single-writer discipline only) | Completeness |

---

## Finding Details

### RT-001: Redaction carve-out enables unscrutinized tampering laundering [CRITICAL]

**Attack Vector:** LOG-M-002 (`feedback-decision-logs-standards.md:24`) and design doc L1.1 both name the secrets/PII redaction as "the **one sanctioned edit** to a sealed entry" in an otherwise append-only, verbatim-wins ledger. The mechanism requires only a `‹redacted: {what}›` marker and "a one-line note that a redaction occurred and why" — free-text, self-reported, unverified. Every *other* trust-sensitive presence-check in this design carries an explicit "presence, not veracity" disclosure (lint check 3 on terminal evidence: "veracity is out of scope by design"; the backfill `(backfilled)` datetime tag: "presence, not veracity — mirrors lint 3"). The redaction carve-out carries **no such disclosure**, and none of the ≤3 L5 lint checks touch it. A privileged writer (the same single-writer this design already trusts) can therefore replace *substantive* verbatim content with a `‹redacted: employer-name›`-style marker, and a git-history reviewer — primed by the design itself to treat redaction as a *sanctioned, expected* edit class — has a **lower** suspicion threshold for that diff than for an unlabeled edit. This is qualitatively different from the already-disclosed generic tampering risk ("none of the lint checks verify content immutability... the diff backstop has two preconditions"): ordinary tampering has no cover story, so a reviewer's guard is up; a labeled "redaction" is designed to look legitimate.

**Category:** Rule Circumvention
**Exploitability:** Medium — requires existing single-writer append privilege (the same privilege the whole scheme already trusts), no external access needed.
**Severity:** Critical — this is the one clean bypass of the deliverable's sole stated integrity backstop (git diff review) for the field the design calls "the fidelity anchor" of the entire convention ("the verbatim is the fidelity anchor: on any conflict, verbatim wins" — design doc L1.1).
**Existing Defense:** Partial — a git diff technically exists for any redaction edit, but the mechanism is explicitly sanctioned, so it does not carry the same reviewer scrutiny an unlabeled edit would.
**Evidence:** `feedback-decision-log-convention-design.md:63` ("This is the one exception to sealed-segment immutability... a redaction to a sealed segment is a sanctioned edit (like a status pointer)... No new lint is required"); `feedback-decision-logs-standards.md:24` (LOG-M-002 redaction clause, no size/category/veracity discipline); contrast with `feedback-decision-logs-standards.md:67` (lint 3: "presence only, not format; veracity is out of scope by design") and `feedback-decision-log-convention-design.md:285` (Q5 backfill note (e): "presence, not veracity — mirrors lint 3") — both of which explicitly disclose the same class of gap for *other* mechanisms, but the redaction carve-out has no equivalent disclosure anywhere in the package.
**Dimension:** Internal Consistency (the design applies a "presence not veracity" honesty discipline everywhere else but omits it at the one point that is literally a sanctioned exception to append-only/verbatim-wins).
**Countermeasure:** Add one clause to LOG-M-002 (and its propagated instances in the design doc L1.1 and, if referenced, the templates) requiring the redaction note to name the redaction **category** (credential / PII / employer-internal) and an approximate **size indicator** of the replaced span (e.g., "≤1 line" / "≤N words"), so a reviewer diffing the commit can sanity-check that the edit's shape matches a plausible secret-shaped token rather than substantive content. This is a pure-text convention addition — zero new lint, file, or subsystem — consistent with the anti-bloat doctrine already used throughout this package.
**Acceptance Criteria:** LOG-M-002 and design doc L1.1 both state the category+size-indicator requirement for a redaction note; a redaction whose replaced span is disproportionate to its stated category (e.g., an "employer name" redaction spanning several sentences) is named as a signal that SHOULD prompt scrutiny at the next commit-cadence checkpoint.

### RT-002: LLM-DECISION-LOG has no supersession/reversal marker (asymmetric with FEEDBACK-LOG) [MAJOR]

**Attack Vector:** FEEDBACK-LOG has an explicit, named correction mechanism: "mark the old entry `Superseded by: FU.N` (the one sanctioned edit to a sealed entry — a status pointer, not a verbatim change)" (`feedback-decision-logs-standards.md:38`). LLM-DECISION-LOG's entry schema (rule file `feedback-decision-logs-standards.md:42`, template `LLM-DECISION-LOG.template.md:17-27`) has **no equivalent field or convention** for the case where a later decision (`DEC-LLM-011`, say) reverses or supersedes an earlier one (`DEC-LLM-003`). The only forward-pointer defined for LLM-DECISION-LOG is `Reflected in`, which is scoped exclusively to *outward* graduation into a worktracker `DEC-NNN`/ADR — not to an *in-log* decision being overridden by a later one. Decisions are, by the design's own framing, higher-ceremony and higher-stakes than feedback items (they feed the H-33/worktracker DECISION lifecycle), yet they have a **weaker** self-correction mechanism than the lower-ceremony feedback log.
**Category:** Boundary
**Exploitability:** Medium — no special access needed; simply arises whenever a decision is later reversed and the operator/assistant does not think to retrofit a workaround.
**Severity:** Major — a reader (or a later session/auditor) consulting a sealed `DEC-LLM-NNN` segment in isolation can act on a decision that was later reversed, with no structural signal that a reversal occurred.
**Existing Defense:** Missing.
**Evidence:** `feedback-decision-logs-standards.md:26,38` (FEEDBACK-LOG `Superseded by:` convention, LOG-M-004 graduation-only forward-link for decisions) vs. `feedback-decision-logs-standards.md:42` and `LLM-DECISION-LOG.template.md:17-27` (LLM-DECISION-LOG entry schema: Decision, User verbatim, Assistant verbatim, Summary/consequences, Context with `Reflected in` — no reversal field anywhere).
**Dimension:** Completeness / Internal Consistency.
**Countermeasure:** Add a `Superseded by: DEC-LLM-NNN` convention to the LLM-DECISION-LOG entry schema and Context line, symmetric with FEEDBACK-LOG's existing mechanism — a pure schema-text addition, zero new lint/machinery.
**Acceptance Criteria:** `feedback-decision-logs-standards.md` LLM-DECISION-LOG section and `LLM-DECISION-LOG.template.md` Entry Schema both document the `Superseded by:` field/marker as the sanctioned edit for a reversed decision.

### RT-003: Install-plan alias-count contradicts its own re-derivation carve-out (verified against live bootstrap entries) [MAJOR]

**Attack Vector:** Design doc Adoption plan step 4 states: "the 8 of 13 live entries (FU.0–FU.4, DEC-LLM-001..003) that currently carry no suffix receive a freshly-added `(alias: —)` (... where a raw verbatim embeds a self-label, the installer re-derives the alias from it per the appendix worked-example convention rather than defaulting to `—`)." Reading the actual live bootstrap entries (`FEEDBACK-LOG.md`): `FU.0` verbatim begins `"FU.0. (1) ratify promotion-is-the-point..."`, `FU.1` verbatim begins `"FU.1. (2) authorize the subtraction pass..."`, `FU.2` verbatim begins `"FU.2. Feedback and Decision Log"` — all three embed a self-label matching their own canonical id. Per the parenthetical's own rule, these three should be **re-derived** to `(alias: FU.0)`, `(alias: FU.1)`, `(alias: FU.2)`, not defaulted to `—`. Only 5 of the claimed "8" (`FU.3`, `FU.4` — whose verbatims carry no self-label — plus `DEC-LLM-001..003`, whose **User verbatim** fields also carry no self-label) actually qualify for the blank-`—` default. The headline "8... receive `(alias: —)`" therefore contradicts the very next clause in the same sentence, verified directly against the live artifact this project already has.
**Category:** Ambiguity
**Exploitability:** Low — a one-time install-step misreading, not a live/repeatable exploit; but the entries at risk (`FU.0` ratify-Scheme-B, `FU.1` subtraction-authorization, `FU.2` the commissioning feedback for this very convention) are arguably the three highest-provenance-value entries in the bootstrap log.
**Severity:** Major — a literal reading of the headline clause, if followed by an installer, would blank out a derivable, meaningful alias on exactly the three entries whose provenance value is highest, contradicting the design's own stated intent ("entries and ids are preserved").
**Existing Defense:** Missing — this is plain prose in a design document; none of the ≤3 L5 lints apply to install-plan text, and no other artifact cross-checks the claim.
**Evidence:** `feedback-decision-log-convention-design.md:239` (Adoption plan step 4, the "8 of 13... (alias: —)... rather than defaulting to —" sentence) vs. `FEEDBACK-LOG.md:26-37,41-53,55-68` (live `FU.0`/`FU.1`/`FU.2` verbatim text, each opening with a self-referential `FU.N.` label).
**Dimension:** Evidence Quality / Internal Consistency / Traceability.
**Countermeasure:** Correct the sentence to state the actual breakdown: 5 of the 8 (`FU.3`, `FU.4`, `DEC-LLM-001..003`) get `(alias: —)`; the remaining 3 (`FU.0`, `FU.1`, `FU.2`) get their self-embedded label re-derived as `(alias: FU.0)`, `(alias: FU.1)`, `(alias: FU.2)` respectively. Wording-only fix, directly verifiable against the live files at install time.
**Acceptance Criteria:** Adoption plan step 4 no longer contains a self-contradicting count; the corrected sentence's claim is checked against `FEEDBACK-LOG.md`/`LLM-DECISION-LOG.md` live content before install proceeds.

### RT-004: "Missing entry" is not distinguished from "nothing happened" for a governance-relevant reader [MAJOR]

**Attack Vector:** Q5 (design doc, "Proposed Defaults" table) honestly discloses that there is "no detector for a turn that should have been logged but was not," and frames this around *forgetting* (accidental capture failure). Nowhere in the package — L0 scope note, Q5, the rule file header, or either template — does it state the reader-side consequence: **a missing entry for a given turn is not evidence that no reportable feedback or decision occurred in that turn.** Because the LLM-DECISION-LOG boundary to worktracker `DEC-NNN`/ADR and the H-32 GitHub-parity lifecycle both treat the log as the record of what was decided, a future auditor or session skimming the log for completeness could misread "no entry here" as "nothing happened here" — precisely the opposite of what Q5 already admits is possible. This is a distinct, previously-unstated risk: Q5 discloses the *capture* gap; this finding is about the *interpretation* gap that follows from it.
**Category:** Ambiguity
**Exploitability:** Medium — arises passively any time someone consults the log for completeness (e.g., during a graduation review or a compliance check), no special action required.
**Severity:** Major — for a governance-adjacent artifact whose stated purpose includes protecting decision provenance (L1.2 boundary to worktracker DECISION/ADR), a silent misread of "absence" as "confirmation of nothing" is a real interpretive risk, not merely a cosmetic gap.
**Existing Defense:** Partial — Q5 discloses that the gap can exist; it does not disclose the specific misinterpretation risk that follows from a reader not knowing the gap exists at read time.
**Evidence:** `feedback-decision-log-convention-design.md:283` (Q5: "Accept as a disclosed residual with no proactive detector... capture stays a MEDIUM discipline") — states the capture gap but not the reader-facing consequence anywhere in the package.
**Dimension:** Methodological Rigor / Completeness.
**Countermeasure:** Add one sentence to the rule-file header or Q5 stating the epistemic caveat explicitly (example wording): "Absence of a log entry for a given turn is not evidence that no reportable feedback/decision occurred — it may mean capture did not happen (Q5). Treat gaps as unknown, not as negative confirmation." Pure wording addition, propagated per the design's own established sweep pattern.
**Acceptance Criteria:** The caveat sentence appears at minimum in the rule file header (the shipping, no-L2-reinjection artifact) and in Q5.

---

### RT-005, RT-006, RT-007 (Minor — condensed)

- **RT-005 (cross-log alias ambiguity):** The H-31 enumeration procedure (design doc L1.1) is scoped to "entries whose alias matches" **within one log**. An operator who reuses the same turn-local label (e.g. `FU.0`) in the same session for both a feedback item and a decision-bearing exchange creates a cross-log ambiguity the enumeration never names as a candidate axis. **Recommendation:** disclosure-only — note that a bare back-reference may need a follow-up clarifying *which log* is meant if the operator has reused a label across both. No new mechanism (P2, anti-bloat-consistent).
- **RT-006 (model-swap degradation of capture-trigger judgment):** The 5 capture-trigger categories (LOG-M-001 / design doc "Capture triggers") are recognized by whichever model is currently active; this project's own bootstrap Context lines already record a mid-project model swap (`claude-opus-4-8` → `claude-fable-5`). Nothing states that trigger-recognition reliability (especially the interrogative/challenge category, item 5, which the package itself notes an earlier keyword-only list already missed once — `FU.9`) may vary across such a swap, and no detector exists for this drift beyond the already-disclosed best-effort Q3 hook. **Recommendation:** fold one clause into the existing Q3/hook-design-note disclosure rather than build new machinery (P2).
- **RT-007 (concurrent-writer race, disclosed residual — included for category coverage only):** The last-write-wins race for concurrent sessions/background writers remains technically undefended by any lock or lease. This is already extensively and consistently disclosed across all five artifacts (design doc L1.1, rule file LOG-M-005, both templates, appendix "Common cases"). No new finding; listed to complete the 5-attack-category sweep and to record that the disclosure is, on this pass, verified consistent everywhere it appears (P2, monitor only).

---

## Recommendations

**P0 (Critical — MUST mitigate before acceptance):**
- **RT-001** — Add redaction-category + size-indicator discipline to LOG-M-002 (rule file) and design doc L1.1. Acceptance: both artifacts state the requirement; disproportionate redactions are named as a review-scrutiny trigger.

**P1 (Major — SHOULD mitigate):**
- **RT-002** — Add `Superseded by: DEC-LLM-NNN` to the LLM-DECISION-LOG entry schema (rule file + template). Acceptance: field documented in both artifacts.
- **RT-003** — Correct the Adoption plan step 4 alias-count sentence to match the verified live-file breakdown (5 get `—`, 3 get re-derived aliases). Acceptance: sentence no longer self-contradicts; matches `FEEDBACK-LOG.md` content.
- **RT-004** — Add the "absence is not evidence of absence" caveat to the rule-file header and/or Q5. Acceptance: sentence present in the shipping rule file (no-L2-reinjection artifact) at minimum.

**P2 (Monitor — MAY mitigate):**
- **RT-005** — Disclose cross-log alias-reuse ambiguity in the H-31 enumeration note (design doc L1.1).
- **RT-006** — Fold a model-swap capture-trigger-drift disclosure into the existing Q3/hook-design-note residual language.
- **RT-007** — No action; existing disclosure verified consistent across all five artifacts on this pass.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | RT-002 (no decision-reversal marker), RT-004, RT-005 name schema/procedure gaps not covered elsewhere. |
| Internal Consistency | 0.20 | Negative | RT-001 (the package's own "presence not veracity" honesty pattern is applied everywhere except the one sanctioned-edit exception); RT-003 (a verified, self-contradicting install-plan claim). |
| Methodological Rigor | 0.20 | Negative (mild) | RT-004 (interpretation-risk not disclosed), RT-006 (model-swap judgment-reliability not named) — narrow gaps against an otherwise thorough 5-category, evidence-heavy methodology. |
| Evidence Quality | 0.15 | Negative | RT-003 is a verified mismatch between a design-doc claim and the live artifact it describes; several other spot-checked claims in this pass (entry counts, `Related:` label drift, Backfill `Added` column parity, `FU.9` interrogative-miss claim) were independently verified accurate, so this is a narrow, not systemic, defect. |
| Actionability | 0.15 | Neutral | All four P0/P1 countermeasures in this report are one-line/one-field wording additions, matching the deliverable's own established remediation style; they do not change the deliverable's own actionability rating. |
| Traceability | 0.10 | Negative (mild) | RT-003's contradiction was found by tracing the design-doc claim to the live bootstrap file it describes — a traceability check that failed once out of several attempted in this pass. |

**Overall assessment:** No finding in this Red Team pass invalidates the deliverable's core architecture. One Critical (RT-001) closes a genuine, previously-undisclosed integrity-laundering channel at the single sanctioned exception to "verbatim wins" / append-only. Three Major findings (RT-002, RT-003, RT-004) are narrow, evidence-verified gaps consistent in kind with (but distinct instances from) the package's own well-documented recurring failure class (a disclosure or symmetry missing at one specific point, not a systemic defect). All proposed countermeasures are wording/schema-field additions — zero new lint, file, or subsystem — consistent with the deliverable's own anti-bloat doctrine and the user's explicit steering against demanding heavyweight machinery for a deliberately minimal, MEDIUM-tier package. **Recommendation: REVISE (targeted).**
