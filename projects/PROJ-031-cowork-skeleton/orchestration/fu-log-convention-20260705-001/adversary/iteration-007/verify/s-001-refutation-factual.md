# Refutation Panel — Factual Lens (Iteration 7, S-001 Red Team Findings)

> **Panel:** Adversarial Refutation, factual-accuracy lens.
> **Target:** `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-007/s-001-findings.md`
> **Protocol:** Default-refuted-if-uncertain. Only Critical findings are in scope (per instructions).
> **Scope note:** The target report names exactly **one** Critical this iteration: `RT-001-20260706-iter7`. `RT-002-20260706-iter7` is Major and `RT-003`/`RT-004` are Minor — out of scope for this Critical-only refutation pass, but spot-checked for context below.

## Navigation

| Section | Purpose |
|---------|---------|
| [Verdict Summary](#verdict-summary) | Verified/Refuted table |
| [RT-001-20260706-iter7 Analysis](#rt-001-20260706-iter7-analysis) | Full factual-accuracy trace |
| [Context Spot-Check: RT-002 (Major, not scored)](#context-spot-check-rt-002-major-not-scored) | Non-binding sanity check |

## Verdict Summary

| Finder ID | Severity | Verdict | Basis |
|---|---|---|---|
| RT-001-20260706-iter7 | Critical | **VERIFIED** | Direct textual contradiction confirmed at all cited lines; no reconciling clause found anywhere in the 6-file package. |

## RT-001-20260706-iter7 Analysis

**Claim:** The bolded phrase "the one sanctioned edit to a sealed entry" (or its L1.1 variant "the one exception to sealed-segment immutability") is applied to two different, non-overlapping mechanisms — the redaction carve-out and the `Superseded by:` status pointer — with no location reconciling the two, and the L1.1→L1.4 cross-reference in the design doc does not corroborate the claim it is cited to support.

**Verification performed:** Read all 4 cited files in full/relevant sections and grepped for `sanctioned edit`, `exception to sealed`, `sealed-segment immutability`, and `sealed entry` across the whole `design/` tree.

Confirmed exact text at every cited location:

1. `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md:24` — LOG-M-002 redaction clause: *"Because the redaction is the *one sanctioned*, lower-scrutiny edit to a sealed entry..."* / *"This is the **one sanctioned edit to a sealed entry** (design doc L1.1...)"* — names **redaction**.
2. `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md:53` — Corrections bullet: *"mark the old entry `Superseded by: FU.N` (**the one sanctioned edit to a sealed entry** — a status pointer, not a verbatim change; see appendix)"* — names the **status pointer**, same file, 29 lines later, no cross-reference to line 24.
3. `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:65` (L1.1) — *"**This is the one exception to sealed-segment immutability (L1.4):** the unredacted original is never the log's job to keep..."* — explicitly directs the reader to L1.4 to corroborate the **redaction** claim.
4. `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:197` (L1.4, "Sealed segments" row) — *"The **one sanctioned edit** to a sealed entry is a *status pointer* (`Superseded by: FU.N` / disposition update) — it touches no verbatim text and only routes a stale cross-reference forward; **verbatim content stays immutable**."* — this is the canonical definition point for sealed-segment immutability, and it names only the **status pointer**, explicitly stating verbatim content (which redaction modifies) "stays immutable." Zero mention of redaction anywhere in this row or the surrounding L1.4 table. The L1.1→L1.4 cross-reference therefore lands on a passage that contradicts, rather than corroborates, the claim it was cited to support.
5. `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:118` (L1.2) — *"...a status pointer, **the one sanctioned edit to a sealed entry**, symmetric with FEEDBACK-LOG's `Superseded by: FU.N`."* — a third instance naming the status pointer.
6. `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/LLM-DECISION-LOG.template.md:26` — *"...mark the old entry `Superseded by: DEC-LLM-NNN` (a status pointer — **the one sanctioned edit to a sealed entry**, symmetric with FEEDBACK-LOG's `Superseded by: FU.N`...)"* — a fourth instance naming the status pointer.

**Reconciliation search:** Grepped the full `design/` tree (design doc + all 5 staging artifacts) for `sanctioned edit`, `exception to sealed`, and `sealed-segment immutability`. No location anywhere states that there are **two** sanctioned edit types, and no location qualifies "the one" in either direction (e.g., "the one *hygiene* edit" vs. "the one *status* edit"). The count as found: 1 location names redaction as "the one" (rule file L24, corroborated by design L65's cross-reference to L1.4), 4 locations name the status pointer as "the one" (rule file L53/L59, design L118/L197, template L26) — with L197 being the section that actually defines what "sealed" and "immutable" mean for this convention, and it omits redaction entirely.

**Regression check against restore-notes.md and the iteration-006 closure list:** `restore-notes.md` Step 1 lists only 6 closed Criticals — RT-001 (redaction category/size discipline), DA-001/FM-006 (safety-function count), PM-001/IN-001 (AE-006e backstop overclaim), PM-002 (placeholder), FM-001 (inline-doc dedup), FM-003 (split-entry). None of these correspond to the "one sanctioned edit" phrase-duplication issue; the residual is not named or disclosed anywhere in `restore-notes.md`, nor in the v3–v9 Revision Changelog rows read in full (`feedback-decision-log-convention-design.md:343-351`). The changelog shows the redaction "one sanctioned edit" framing was added in v7/iteration-5 (DA-001/PM-001) and the status-pointer "one sanctioned edit" framing was separately introduced across iterations 3–6 (IN-003, RT-002) — each addition independent, neither iteration reconciling with the other. This finding is therefore not a restatement of an already-disclosed residual or of a restore-notes disposition; it is a genuine, previously-unflagged instance of the package's own recurring "claim contradicts an adjacent/cross-referenced disclosure" class, accurately cited.

**Conclusion:** All five/six citations are accurate at the current line numbers; the contradiction is direct (verbatim phrase collision within the same file, plus a cross-reference that fails to corroborate), not an inferential stretch. **VERIFIED.**

## Context Spot-Check: RT-002 (Major, not scored)

Not required for this Critical-only pass, but checked for internal consistency of the panel's own evidence chain: `FEEDBACK-LOG.template.md:26` reads *"On any conflict, **verbatim wins** (secrets/PII excepted — redact before capture, LOG-M-002). Corrections are append-only (convention-only, git-backstopped — not a filesystem lock): to fix a verbatim or reopen a `DONE`, add a new entry referencing the old id."* — confirmed no `Superseded by:` instruction anywhere in this file, versus `LLM-DECISION-LOG.template.md:26` which does carry the explicit "Reversal/supersession" bullet. The asymmetry claim is accurate at the cited lines. (Not adjudicated as part of the Critical verdict above; included only as corroborating context.)
