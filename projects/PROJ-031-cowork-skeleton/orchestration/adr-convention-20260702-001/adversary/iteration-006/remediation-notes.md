# Iteration-6 Remediation Notes — Subtraction-Doctrine Pass 2

> Owner: ps-architect (creator/owner). Owner-first remediation after iteration-6 S-014 (score 0.59, gate 0.95).
> **Doctrine (FU.1, user-authorized, binding):** close findings by DELETING the exposing claim/mechanism or by honest EDIT/DISCLOSURE — never by bolting on compensating machinery. Adding a mechanism requires deleting something bigger and stating the trade. Rebut invalid findings with evidence. P-002 incremental; P-020 within-mandate; P-022 no fabrication (cite paths/lines; label inference).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Doctrine and Method](#doctrine-and-method) | How each finding was closed |
| [The Central Fix](#the-central-fix-l-3-regex-bug) | L-3 regex bug — the highest-value correction |
| [Disposition Table (every FIXABLE-NOW item)](#disposition-table-every-fixable-now-item) | Iter-6 remediation-table items 1–21 |
| [Rebuttals and Non-Edits](#rebuttals-and-non-edits) | Findings answered by evidence, not edit |
| [New Residuals Disclosed](#new-residuals-disclosed) | Honest residuals after this pass |
| [Budget Verification](#budget-verification) | Rule-draft token/line count re-measured |
| [Files Edited](#files-edited) | Change surface |
| [Tally](#tally) | changes / deletions / additions / rebuttals |

---

## Doctrine and Method

Iteration-6 found 9 raw / 7 distinct new Criticals. Every one is an **overclaim** (a prose claim about what a retained/deleted mechanism does, not verified against the mechanism) or a **disposition-completeness** gap — NOT a demand to restore deleted machinery. The subtraction-pure response to an overclaim is to **delete the overclaim or fix the one-line bug that makes it false**, not to add a compensating rule. That is exactly what this pass does. No new lint rule, ledger, gate, or matrix was added. One character-class in an existing regex was widened (a bug fix to the single retained one-liner, not a new mechanism — trade stated below).

---

## The Central Fix: L-3 regex bug

**Finding (RT-101 + DA-001, Critical, 2 reviewers):** the retained L-3 dedup one-liner uses `grep -E '^ADR-[a-z0-9-]+-[0-9]{3}'` — a **lowercase-only** character class. Every dialect ID (`ADR-PROJ031-005`, `ADR-EPIC002-001`) begins with an uppercase closed-set prefix, so the anchored pattern never matches and every dialect ADR is silently dropped before `sort | uniq -d`. The exact class of the ADR's own headline `ADR-EPIC002-001` collision is invisible to its own collision lint.

**Two doctrine-legal closes existed:** (a) narrow the claim to "canonical IDs only" + disclose a permanent dialect-dedup residual; (b) widen the existing character class `[a-z0-9-]` → `[A-Za-z0-9-]` in both the grep and the sed of the single one-liner.

**Chosen: (b), the regex fix.** Trade stated per doctrine: this is a **1-character-class widening of an existing rule, not a new mechanism** — it does not re-grow the lint, add a rule, or add attack surface. It is preferred over (a) because it makes the twice-stated "all non-frozen ADRs… Repo-wide" claim **actually true** (the honest outcome) rather than disclosing a permanent gap that swallows the founding-incident class. Verified by trace: `ADR-PROJ031-006-alpha.md` and `-beta.md` both reduce to `ADR-PROJ031-006` and are caught by `uniq -d`; bare `ADR-001-slug` (no second 3-digit group) still does not match (correctly left to L-2). This single fix cascades to close RT-101, DA-001, RT-104 (R-6's "detected via L-3" now accurate for dialect), and reconciles the ADR's own "canonical IDs" vs "all non-frozen" scope-description contradiction.

---

## Disposition Table (every FIXABLE-NOW item)

Legend: **FIX-BUG** (correct an existing mechanism) · **DELETE** (remove the exposing claim) · **EDIT** (honest reword/narrow) · **DISCLOSE** (add named residual) · **REBUT** (answer with evidence).

| # | ID(s) | Close | Action taken |
|---|-------|-------|--------------|
| 1 | RT-101 / DA-001 | FIX-BUG | Widened `[a-z0-9-]`→`[A-Za-z0-9-]` in the L-3 one-liner (grep+sed) in all 4 copies (rule draft L-3 row + one-liner; ADR pre-flight + Enforcement L-3 row). Reconciled ADR "canonical IDs" → "canonical and dialect IDs". |
| 2 | RT-102 | DELETE | Removed the false "case-folded entity-prefix look-alikes… are rejected" claim from L-1 rows in both files; kept the true numeric-leading rejection; disclosed the case-fold shadow as SHOULD-NOT guidance. |
| 3 | DA-002 | EDIT+DISCLOSE | "Frozen = closed to new entries" reworded to "closed by convention (SHOULD-NOT extend); not lint-enforced (L-9 removed; L-2 exempts frozen dirs)" — disclosed residual. |
| 4 | PM-001 / IN-001 | DISCLOSE | Added one honest current-state sentence to Status: guidance not yet relocated to `.context/rules/` (M-2), producer agent not yet fixed (M-12); no fabricated Tasks. |
| 5 | FM-001-iter6 | DELETE | Deleted the dangling "New-Project-Onboarding section" reference from M-14; changelog v1.8 records the section was removed in the subtraction pass. |
| 6 | FM-002-iter6 | EDIT+DISCLOSE | Narrowed "19 files pass L-1" → "18 reachable"; `ADR-STORY015-001` disclosed as out-of-`decisions/`-scan residual in both files. |
| 7 | FM-005-iter6 | ADD-ROW | Added RT-007 disposition row (CLOSED-BY-DELETION + residual) to subtraction-pass-notes. |
| 8 | DA-003-iter6 | EDIT | Reconciled "13 of 18": 12 named deleted rules + the L-1a/L-1b split collapsed into single retained L-1 = the 13th reduction. |
| 9 | CC-001-iter6 | EDIT | Reworded lowercase "never" at rule-draft :47/:133/:144 to SHOULD-NOT; added L5 preamble scoping the mechanism "must" as tool trigger-conditions. |
| 10 | RT-104-iter6 | (cascade) | Closed by item 1: R-6's L-3 detection is now accurate for dialect; RT-004 note updated. |
| 11 | FM-010-iter6 | EDIT | M-9 "review checklist item on the promoting PR" → "intended reviewer-checklist item (no PR template exists yet — not yet instrumented)". |
| 12 | FM-009-iter6 | ADD | Gave R-B/R-C an owner+cadence (governance; at each Path-1/Path-2 promotion), mirroring M-5b. |
| 13 | DA-004 / PM-006 | EDIT | "periodic audit" → "best-effort, at-authoring-time (M-5b); no fixed cadence". |
| 14 | PM-002-iter6 / FM-006 | DISCLOSE | Added a one-line definition of the post-ratification "Gating?" column (gates M-6 ship-readiness / M-9 self-promotion, not M-1). |
| 15 | FM-004-iter6 | EDIT | Separated grandfathered dialect families from PROJ-014's transient bare drafts (not a recognized dialect) in the rule draft. |
| 16 | IN-002-iter6 | EDIT | Null-alternative "strictly better than the null" qualified: designed/argued, not yet demonstrated until M-2/M-12 land. |
| 17 | IN-003-iter6 | DISCLOSE | Added a note that H-32 parity applies to all jerry-repo work-item rows; the 3 explicit "(H-32)" flags are illustrative, not an exemption of the other 11. |
| 18 | FM-003-iter6 / RT-103 | DISCLOSE | Disclosed L-7's 3-of-6 field asymmetry and existence-not-semantic-correctness scope in both files (no field-list extension — subtraction-consistent). |
| 20 | CC-002-iter6 | DISCLOSE | Added honest L1-aggregate note: `.context/rules/*.md` measures ~26.9k words (~36k tokens); the SSOT ~12,500 figure is not a raw corpus sum; this file's ~3.3k is a bounded ~9% add. |
| 21 | SM-001-iter6 | EDIT | M-8 (/adversary C4 review) marked IN-PROGRESS (iteration 6 is that review). |

Item 19 (FM-012, open worktracker Tasks/GH Issues) is **[INHERENT]** — an organizational action, already honestly disclosed at ADR :497; not fabricated (P-022).

---

## Rebuttals and Non-Edits

- **FM-007 (L-5/L-6 numbering gap, Minor):** added a one-line footnote (numbering preserved for changelog traceability) rather than renumber — renumbering would break every changelog cross-reference to L-8..L-14 (FM-014 historical-record principle).
- **CC-003 (232 vs 233 lines):** corrected to 233 in the notes/changelog. `wc -l` reports 232 newlines; the file has 233 content lines (final line unterminated). Stated precisely.
- **CC-004 (--no-verify 24 doc-convention failures):** independently re-verified both deliverables' H-23 nav tables and anchors resolve clean (matching S-007's own Verified-Compliant finding); added a one-line cross-reference rather than treat as implicating these files. Evidence: S-007 :39, :42.
- **FM-011 (supersession cycle, Minor):** disclosed as a one-line residual in Amend-vs-Supersede; no structural cycle-checker added (would be new machinery).

---

## New Residuals Disclosed

| ID | Residual | Where | Framing |
|----|----------|-------|---------|
| R-9 | Case-folded slug look-alike (`ADR-proj031-001` shadowing dialect `ADR-PROJ031-001`) is not structurally rejected | ADR/rule-draft L-1 rows | SHOULD-NOT guidance; not lint-enforced |
| R-10 | Entity-embedded dialect ADRs (`ADR-STORY015-001`) are outside the `projects/*/decisions/` scan path | ADR/rule-draft grandfather note + descoped note | Grandfathered in place; out-of-scan, not lint-covered |
| R-11 | L-7 checks the 3 forward/promotion links only (existence, not bidirectional/semantic correctness); `supersedes`/`amends`/`amended_by` unchecked | ADR/rule-draft L-7 rows | Disclosed asymmetry; the historically-demonstrated orphaning side is covered |
| RT-007 (re-dispositioned) | Repository-based-topology dialect misuse — its sole control L-4b was deleted | subtraction-pass-notes disposition table | CLOSED-BY-DELETION; canonical slug is topology-agnostic and RECOMMENDED; SHOULD-NOT guidance residual |

---

## Budget Verification

Re-measured post-edit (`wc`): rule draft = **2,870 words → ~3,875 tokens; 238 lines.** Against the mandate budget (≤ ~2,500 tokens / 250–350 lines): **lines (238) are within/under the 250–350 guidance**; **tokens (~3.9k) exceed the ~2,500 soft target** — the same irreducible-normative-content tension the v1.7 changelog already disclosed (the two budget expressions are mutually inconsistent at real rule-file density). The iter-6 growth (+~430 words vs the 233-line subtraction result) is **overclaim-correction** (regex-fix comment, R-9/R-10/R-11 disclosures, L-7 asymmetry, L5 mechanism-scoping) — cutting it to hit 2,500 tokens would *reintroduce* the overclaim this pass exists to remove. Trade stated per doctrine, disclosed in the rule-draft CC-002 note. `.context/rules/*.md` aggregate = 26,921 words (~36.3k tokens), so the SSOT's ~12,500-token L1 figure is a curated subset, not a raw corpus sum (CC-002 honest note).

---

## Files Edited

- `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md`
- `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/subtraction-pass-notes.md`
- `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-006/remediation-notes.md` (this file)

---

## Tally

Counted at the edit-operation level across the three edited files (36 Edit operations + 1 new file):

| Category | Count | Notes |
|----------|-------|-------|
| **Changes** (fix-bug / narrow / reword in place) | 22 | incl. the L-3 regex fix (4 copies), 3× CC-001 never→SHOULD-NOT, DA-002 frozen reword, FM-002 grandfather narrow (both files), DA-003 count, CC-003 232→233 (3×), IN-002 qualifier, DA-004/PM-006 periodic (2×), M-8 status, scope reconciliations |
| **Deletions** (exposing claim removed) | 3 | RT-102 case-fold-rejection claim; FM-001 dangling onboarding cross-ref; FM-010 M-9 as-built PR-template implication |
| **Additions** (honest disclosure/note/row — no mechanism) | 16 | R-9/R-10/R-11 Risks rows; RT-007 disposition row; Status/null/R-6/Gating/H-32/L-7/R-B/R-C/FM-011/FM-007/CC-002 notes; L5 mechanism-scoping note; iter-6 notes section + nav; 2 changelog rows; this file |
| **Rebuttals** (answered by evidence, no defect-edit) | 2 | CC-004 (nav/anchors re-verified clean — both files not among the FU.3 24 failures; S-007 :39/:42); FM-007 (numbering kept + footnoted, not renumbered — renumber would break changelog cross-refs, FM-014) |

**Doctrine adherence:** zero new lint rules / ledgers / gates / matrices. One existing regex character-class widened (`[a-z0-9-]`→`[A-Za-z0-9-]`) as a bug fix, trade stated. Additions are all honest residual disclosures (R-9/R-10/R-11, RT-007) or notes — the doctrine-sanctioned "disclose as an honest residual" move — not compensating machinery. The only [INHERENT] items left open (M-6 lint build, M-12 producer fix, FM-012 Tasks/Issues) are organizational/engineering actions honestly disclosed, not fabricated.

*No subagents spawned (P-003). No files edited outside mandate (P-020). All claims cite paths/lines; inference labeled (P-022).*
