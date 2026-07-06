# S-002 Devil's Advocate — Factual-Accuracy Refutation Pass (Iteration 9)

> Lens: FACTUAL-ACCURACY. Question per finding: does the cited defect actually exist in the CURRENT deliverables at the cited locations? Default to REFUTED if uncertain. Blind pass — no other refuters' or panels' outputs read.

## Scope

Critical findings under review (per `s-002-findings.md` Findings Table): **DA-001-20260706-i9**, **DA-002-20260706-i9**. (DA-003-20260706-i9 is Major, out of scope for this Critical-only refutation panel.)

---

## DA-001-20260706-i9: Flagship promoted-ADR precedent (`docs/design/ADR-output-path-resolution-001.md`) contains 13 currently-broken outbound citations

**Verdict: VERIFIED**

**Reasoning:**

1. Direct reads of `docs/design/ADR-output-path-resolution-001.md` at lines 380, 481, 529, 593, 602, 632, 633, 634, 635, 642 confirm the cited markdown hyperlinks exist verbatim, all of the form `../../PROJ-030-bugs/work/BUG-006-*.md` or `../../PROJ-030-bugs/work/TASK-008-*.md` (line 380 alone contains 4 such links: BUG-006 audit, eng-audit, red-audit, ux-audit). Counting all 10 cited lines yields exactly 13 links, matching the finding's tally precisely.
2. Relative to the file's actual location (`docs/design/`), `../../` resolves to the repository root. `Glob` verification confirms **zero** matches for a top-level `PROJ-030-bugs/*` or `docs/PROJ-030-bugs/*` directory — the links are missing the `projects/` path segment. The correct targets (`projects/PROJ-030-bugs/work/BUG-006-skill-output-path-hardcoded.md`, and — for the three audit files — `projects/PROJ-030-bugs/research/BUG-006-{eng,red,ux}-audit-detail.md`, which live under `research/`, not `work/` as cited) were Glob-confirmed to exist at their real paths. The links are broken today, confirmed by direct filesystem check, not by inference.
3. The finding's characterization of the surrounding claims is accurate: ADR-PROJ031-004's Related Decisions table (line 733) does state `ADR-output-path-resolution-001 (docs/design) | PRECEDENT | Migrated in the ~150-reference BUG-006 remediation... the paid promotion tax this decision removes`, and the Rationale (line 266) does state "Jerry's own thesis picks the regime, and the corpus has already voted," resting in part on this same document (confirmed as one of the 3 canonical framework ADRs via its own `Parent: EPIC-002` frontmatter at `docs/design/ADR-output-path-resolution-001.md:8`, matching the "EPIC-002 → 1" count at ADR-004 line 266).
4. This is not a restatement of a disclosed residual. R-B (citation staleness) is explicitly scoped to full-path citations **of an ADR's own identifier/path** going stale (the 72%/28% bare-ID-vs-full-path ratio measured at ADR-004 lines 566-568), and Migration Plan row M-10 (ADR-004 line 540) is explicitly scoped to citations **to renamed ADRs** (`ci.yml`'s `ADR-CI-001`, the stale `ADR-PROJ007-001/002` references). Neither residual nor M-10 addresses a promoted ADR's own outbound relative links to non-ADR sibling project artifacts (audit/task files). L-7 (rule-draft line 179, confirmed by direct read) checks only YAML `superseded_by`/`promoted_to`/`promoted_from` targets, existence-only — it structurally cannot catch markdown-body hyperlink breakage. The finding's evidence and framing hold up under direct verification.

---

## DA-002-20260706-i9: This ADR's own self-promotion (M-9) is under-scoped — five additional relative links not in the stated repair plan

**Verdict: VERIFIED**

**Reasoning:**

1. All five cited links were directly confirmed present at the stated lines: `ADR-PROJ031-004-adr-identifier-convention.md:85` and `:213` (`[FEEDBACK-LOG.md → FU.0](../FEEDBACK-LOG.md)`), `:780` (same target, Changelog v1.7 row), `:652` (`[subtraction-pass-notes](../orchestration/adr-convention-20260702-001/subtraction-pass-notes.md)`), and `adr-standards-rule-draft.md:165` (`[Claim-Status Convention](../decisions/ADR-PROJ031-003-credential-protection-supply-chain.md#claim-status-convention-p-022--foundational)`). All five currently resolve correctly (Glob-confirmed: `projects/PROJ-031-cowork-skeleton/FEEDBACK-LOG.md` and `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-003-credential-protection-supply-chain.md` both exist at their expected relative targets from the ADR's and rule-draft's current locations).
2. M-2's repair scope, quoted verbatim at ADR line 530, is confirmed textually limited to "(a) *this* rule file's inbound relative link to the parent ADR... and (b) the parent ADR's outbound relative links to `../design/adr-standards-rule-draft.md`" — i.e., only the reciprocal ADR↔rule-draft pair. M-9 (line 539) likewise names only this same reciprocal pair ("the same commit MUST re-point the companion rule file's inbound link to this ADR... paired with M-2's outbound-link fix"). No Migration Plan row, and no line in the Meta-Note (`#meta-note-this-adrs-own-identity-and-remap-path`, read in full at lines 711-722), enumerates the FEEDBACK-LOG.md, subtraction-pass-notes.md, or ADR-PROJ031-003 links. The Meta-Note's only relevant language is the generic "re-point any citations" (line 717) — an aspirational, unenumerated phrase, not a gated/owned action item comparable to M-2/M-9's specific, named repair scope.
3. The forward-looking arithmetic is correct and is explicitly labeled by the finder as inference (P-022), consistent with the destination paths stated elsewhere in the same document: M-9 moves the ADR to `docs/design/ADR-adr-convention-001-*.md` (line 539/717) and M-2 moves the rule draft to `.context/rules/adr-standards.md` (line 530/247). Applying standard relative-path resolution: `../FEEDBACK-LOG.md` from `docs/design/` resolves to `docs/FEEDBACK-LOG.md` (nonexistent); `../orchestration/.../subtraction-pass-notes.md` from `docs/design/` resolves to `docs/orchestration/.../subtraction-pass-notes.md` (nonexistent); `../decisions/ADR-PROJ031-003-...` from `.context/rules/` resolves to `.context/decisions/ADR-PROJ031-003-...` (nonexistent). This math is not disputable given the stated destinations.
4. Not a restatement of a disclosed residual: R-B concerns full-path citations of ADR identifiers going stale (a different citation object and direction than these five links, which cite FEEDBACK-LOG.md, a notes file, and a sibling ADR that itself never moves). The prior iteration's "DA-002" tag (Changelog v1.3, ADR line 776) refers to a distinct, earlier-closed finding — the reciprocal ADR↔rule-draft link repair itself — not to the five additional links this iteration's DA-002 newly identifies. No double-counting or stale-reference defect found.

---

## Summary

| ID | Severity | Verdict |
|----|----------|---------|
| DA-001-20260706-i9 | Critical | VERIFIED |
| DA-002-20260706-i9 | Critical | VERIFIED |

Both Critical findings survive factual-accuracy scrutiny: cited file+line locations were re-read directly, hyperlink targets were Glob-verified against the live filesystem, and the claimed absence of coverage in the residual register / Migration Plan / Meta-Note was independently confirmed by direct grep/read rather than taken on the finder's word.
