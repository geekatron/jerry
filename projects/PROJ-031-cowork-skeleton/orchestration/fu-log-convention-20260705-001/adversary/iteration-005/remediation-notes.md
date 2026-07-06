# Iteration-005 Remediation Notes — Owner-First, Anti-Bloat

> **Agent:** ps-architect (convergent, opus) · **Date:** 2026-07-06
> **Input:** `adversary/iteration-005/s-014-quality-score.md` (composite 0.468, gate 0.95, ESCALATE-recommended) + 9 blind strategy reports (S-001/002/003/004/007/010/011/012/013).
> **Directive:** Owner directed a fifth remediation despite the ESCALATE recommendation. This pass is deliberately **propagation-focused** to break the recurring failure class rather than chase one more instance of it.
> **Doctrine:** Close findings by *propagating an existing disclosure to the point of the claim*, *clarifying*, or *deleting* — never by adding machinery. Any genuine addition is offset by deletion/reframe; the trade is stated.
> **Constitutional:** P-003 no subagents · P-020 draft-only (no framework paths touched; all edits under `projects/PROJ-031-cowork-skeleton/`) · P-022 evidence cited, inference labelled.
> **Public-repo hygiene:** repo-relative paths + placeholders only; no employer/internal references introduced.

## Systemic root cause this round attacks

The scorer's delta read (and SM-002/CV-003/FM-008) name the recurring failure class: **a disclosure/hedge/caveat exists somewhere in the 6-file package, but not at the specific location where the claim is made or in the artifact that actually ships.** Four of six Criticals (RT-001, DA-002, DA-003, DA-004) and CC-001's adjacent phrasing are instances. This pass therefore runs a **full propagation sweep**: for every disclosure the design doc carries, echo it (a) at the point the claim is made and (b) into the shipping rule file / templates. To avoid re-committing DA-004's own error (the iter-4 changelog claimed a blanket "swept across all sibling artifacts" that was falsified), each fix below names the *specific* artifact it landed in. The one genuinely new rule (secrets carve-out, DA-001/PM-001) is a real safety gap, not machinery (zero new lint/file/subsystem).

## Critical findings — disposition (all 6 resolved by edit)

| # | Finding(s) | Strat | Resolution (artifact + action) | Class |
|---|------------|-------|--------------------------------|-------|
| C1 | DA-001 / PM-001 secrets-PII vs "verbatim wins" | S-002+S-004 | **New LOG-M-002 carve-out** (rule file) + design-doc L1.1 "Secrets/PII carve-out" para + both template banners + both append-only lines: redact secret-shaped tokens/PII **before** append; redaction is the one sanctioned sealed-segment edit; modeled on the project's own `FU.4`. | Add (safety) |
| C2 | RT-001 Q5 "no proactive detector" absent from rule file | S-001 | **Rule-file header** now carries "there is no detector for a turn that should have been logged but was not (Q5)". | Propagate |
| C3 | CC-001 L0 "captures **every**…" self-contradiction | S-007 | **Design L0** both bullets reworded → "append target for every … *that gets logged / is captured*"; both **template banners** softened (CC-003). Deletes the "every" overclaim. | Delete/reframe |
| C4 | DA-002 L1.1 enumeration vs L1.4 degradation | S-002 | **Design L1.1** now cross-references L1.4's multi-segment degradation admission ("both say the same thing"); stray HARD "MUST check" → "SHOULD check" (CC-002). | Propagate + delete |
| C5 | DA-003 L0/Ledger "never outgrows" hedge | S-002 | **Design L0 headline** and **Improvement-Ledger row 9** now carry the scale hedge (seals at ~40 not ~50; sidecar fallback not built). Deletes "never outgrows". | Propagate + delete |
| C6 | DA-004 untested-generalization caveat absent from rule file | S-002 | **Rule-file Adoption-profile bullet** now carries the `[INFERENCE]` "untested for a different operator" caveat (the artifact iter-4 wrongly claimed carried it). | Propagate |

## Major findings — disposition (resolved by edit unless noted)

| Finding | Strat | Resolution |
|---------|-------|-----------|
| PM-004 / FM-002 background-agent goal disconnected | S-004/S-012 | Candidate-handoff bullet (design L1.1) now ties the 1–3-line candidate to FU.2's "don't burn main context" goal. |
| PM-006 single-writer caveat absent from templates | S-004 | Added to **both templates'** Ids-&-aliases sections. |
| IN-004 MEMORY.md dual-write precedence | S-013 | Design Scoping now states FEEDBACK-LOG is canonical on divergence (mirrors DEC-LLM→worktracker precedence). |
| RT-004 / FM-001 self-count re-violates governing principle | S-001/S-012 | Named as a deliberate temporary exception + AE-006e backstop (design L1.4 **and** rule LOG-M-006). |
| PM-002 oversized-file id-mint via LLM Read | S-004 | Deterministic `grep -c` count near cap (design L1.4, rule LOG-M-006, appendix hand-edit case). |
| IN-003 / IN-001 / FM-003 / FM-005 lint blind spots | S-013/S-012 | Single **L5-lint scope-limits block** in the rule file discloses all four at once. |
| RT-003 commit-granularity absent from rule file | S-001 | Added to the rule-file Segment-rotation section (was design-doc-only). |
| RT-002 no project attribution | S-001 | Optional `project: PROJ-NNN` trailing tag — reuses the existing `scope:`-tag pattern, no new field/line. |
| FM-007 datetime format | S-012 | `datetime` = `YYYY-MM-DD` note in rule file. |
| IN-002 density variance | S-013 | LOG-M-006: verbose entries trigger earlier rotation regardless of count. |
| FM-004 single-candidate crash recovery | S-012 | Design L1.1: a single append needs no parity procedure; re-derivable from the handoff/transcript; lint 2 catches a half-written dup. |
| RT-005 unbounded deferral renewal | S-001 | Design L1.2: a second consecutive deferral SHOULD be flagged, not renewed silently. |
| PM-005 Q3 hook no forcing function | S-004 | Adoption step 6: recorded as a dated worktracker item at install. |
| FM-008 / SM-002 / CV-003 no convergence fallback / trend not synthesized | S-012/S-003/S-011 | New "remediation-convergence / escalate-to-user trigger" in the Adoption section + 5-round trend synthesized in the v7 changelog. |
| CV-001 / CV-002 appendix id/alias labeling | S-011 | Appendix header (line 4) reconciled with its own illustrative-ids disclaimer (line 36): ids/aliases are explicitly illustrative, disclosed at the point of the claim. |
| DA-005 hand-edit concurrent-session precondition | S-002 | Appendix "Common cases": single-writer holds only if no other session/window is appending. |

## Rebuttals (closed by evidence, no edit / no new machinery)

1. **PM-003** ("no de-correlation proposed" for the correlated commit-cadence SPOF). *Rebuttal:* the design **already** proposes the ~3-month/next-milestone calendar caps as the de-correlation backstop and names the owner (L2 "One shared dependency, named as such"). The residual skipped-checkpoint case is an accepted, disclosed anti-bloat trade — not an unaddressed gap.
2. **PM-007 / SR-003** (rule file over its ~1,500-token soft target). *Rebuttal / trade:* the overage buys adversary-mandated **shipping-artifact** disclosures (the SM-003 class: "the rule file omitted disclosures the design doc carried"), not scope creep. It stays a P-020 **[USER-DECISION]** (ratify-at-current vs trim), consistent with every prior iteration — not a silent scorer resolution. Measured `wc -w` = ~1,791 words (was ~1,425); design doc figures updated for honesty (P-001).
3. **PM-008** (single-operator drift undetectable). *Rebuttal:* **[INHERENT]** accepted disclosed residual; a drift detector is machinery for an unstated requirement.
4. **Content-hash / real-time-validator lint** — re-declined (git provides tamper-evidence; MEDIUM tier does not warrant it), consistent with iterations 2–4.

## Anti-bloat accounting (P-022, honest)

- **Zero new machinery:** no new lint (still ≤3), no new file, no new subsystem. The one new *rule* (LOG-M-002 secrets carve-out) is a governance clarification and a genuine safety gap the project already exercised once (`FU.4`).
- **Design doc:** net-reframes overclaims — deletes "captures every", "never outgrows", stray "MUST" — while propagating disclosures. Roughly balanced.
- **Rule file (shipping):** grew ~1,425 → ~1,791 words because the six Critical fixes are the exact disclosures the adversary said belong in the shipping artifact. This is the **disclosed [USER-DECISION] overage**, not new machinery. Forcing deletions of load-bearing, adversary-mandated content to hit a token number would be counterproductive; the trade is stated openly and the ratify-vs-trim call remains the user's (P-020).

## Files edited

- `design/feedback-decision-log-convention-design.md` (L0, L1.1, L1.2, L1.4, Scoping, Ledger, Adoption, L2, Staged Artifacts, Design posture, v7 changelog)
- `design/staging-feedback-logs/feedback-decision-logs-standards.md` (header, LOG-M-002, LOG-M-006, Adoption profile, Segment rotation, L5 Lint, FEEDBACK-LOG entry)
- `design/staging-feedback-logs/FEEDBACK-LOG.template.md` (banner, Ids-&-aliases, append-only line)
- `design/staging-feedback-logs/LLM-DECISION-LOG.template.md` (banner, Entry-schema ids line)
- `design/staging-feedback-logs/examples-appendix.md` (header genericization scope, hand-edit common case)

## Note on the ESCALATE recommendation

The scorer's ESCALATE (composite < 0.50 after 4 cycles) is honored *within* this remediation, not ignored: the design now carries an explicit **escalate-to-user-at-the-ceiling** convergence trigger (FM-008), and the v7 changelog synthesizes the 5-round trend transparently (SM-002/CV-003). If a re-score after this propagation sweep does not converge, the standing fallback the document now names is to present the user with the trajectory + explicitly-accepted residuals + a ratify-the-substance-vs-continue choice — every strategy across all five rounds agrees the design's *substance* is sound.
