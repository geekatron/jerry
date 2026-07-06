# Revision Notes — FU-Log Convention (2026-07-05)

> **PS Context:** PROJ-031-cowork-skeleton · ps-architect (convergent, opus) · Owner-revision of the FEEDBACK-LOG + LLM-DECISION-LOG convention package.
> **Inputs:** user Review Round FU.5–FU.9 (`FEEDBACK-LOG.md §Review Round`), `ux/heuristic-evaluation.md` (31 findings), design doc + 4 staged artifacts, `quality-enforcement.md` (MEDIUM tier / HARD ceiling 25/25).
> **Doctrine:** anti-bloat — close findings by *simplifying*, never by adding machinery; every mechanism earns its place; token budgets are hard (learned from the ADR-convention over-engineering spiral, iteration-005 composite 0.66).
> **Constitutional:** P-003 no subagents · P-020 draft-only, nothing written into `.context/`, `docs/`, `hooks/`, or any framework path · P-022 evidence cited, inference labelled · public-repo hygiene (no employer refs, no absolute home-directory paths — repo-relative only).

## Document Sections

| Section | Purpose |
|---------|---------|
| [FU.5 — Segment rotation](#fu5--segment-rotation-log-growth) | Capped-collection linked-list design |
| [FU.6 — Canonical id vs alias](#fu6--canonical-id-vs-alias) | Logger-assigned ids; user labels are aliases |
| [FU.8 — Worked examples](#fu8--worked-examples) | Embedded examples + appendix |
| [Open-question defaults](#proposed-defaults-q1q4) | Q1–Q4 PROPOSED-DEFAULTs |
| [UX findings disposition](#ux-findings-disposition-31) | Fold/rebut per finding with evidence |
| [Token budget](#token-budget) | Rule-file size discipline |
| [Files changed](#files-changed) | Artifact inventory |

---

## FU.5 — Segment rotation (log growth)

**Requirement (verbatim, alias FU.0.1):** append-only logs will exceed LLM read limits; treat as a capped collection with an upper limit before starting a new file; treat like a linked-list to navigate forward/backward between the decision and feedback logs.

**Design (added, earns its place — closes Severity-4 F-001):**

- **Cap:** seal the ACTIVE log when it first reaches **~50 entries OR ~800 lines** (whichever comes first).
  - *Justification (evidence):* default Read tool window ≈ 2,000 lines → 800 lines leaves **2.5× headroom**; 800 lines of these entries ≈ **8–12k tokens**, i.e. **2–3× under the ~25k-token truncation** observed in this very project (PM-001). Entry-count (~50) is the human-eyeballable trip-wire; line-count (~800) is the hard truncation guard. At ~12–18 lines/entry (measured on the real bootstrap entries) the two thresholds land together.
- **Stable ACTIVE name:** the tail segment always keeps the plain name `FEEDBACK-LOG.md` / `LLM-DECISION-LOG.md`. The operator/LLM **always reads and appends here** — they never need to know the current segment number.
- **Sealed segments:** `FEEDBACK-LOG.001.md`, `FEEDBACK-LOG.002.md`, … — **immutable once sealed**, deterministic ascending names.
- **Linked-list (bidirectional):** each file's header blockquote carries `Segment N · prev · next`.
  - Sealed segment N: `prev = FEEDBACK-LOG.{N-1:03d}.md` (`—` for segment 1), `next = FEEDBACK-LOG.{N+1:03d}.md`.
  - ACTIVE (segment N): `prev = FEEDBACK-LOG.{N-1:03d}.md`, `next = —` (it is the tail).
  - **Forward-nav rule:** from segment N, the successor is `FEEDBACK-LOG.{N+1:03d}.md` **if it exists**, else the ACTIVE `FEEDBACK-LOG.md`. This lets `next` be written once at seal time and stay immutable (the not-yet-sealed successor resolves to the stable ACTIVE name).
- **Lightweight index:** a small **Segment Index** table (one row per segment: file · canonical-id range) lives **only in the ACTIVE file** (grows one row per rotation; rebuildable by `ls` if lost). Sealed segments carry a one-line pointer to it, so they stay immutable.
- **Cross-log navigation (FEEDBACK ⇄ DECISION):** achieved **purely by canonical id** — an FU entry references `DEC-LLM-NNN` and vice-versa; because canonical ids are globally monotonic per log and never reset, the reference survives rotation, and each log's Segment Index resolves *id → which segment file*. **No file paths in cross-references, no extra machinery.**
- **Rotation procedure (documented, not new enforcement):** copy the filled ACTIVE content to the next `.{NNN}.md`, mark it SEALED with prev/next, then reset the ACTIVE to a fresh segment N+1 header (canonical ids continue — FU.50, FU.51, …). Rotate *after* the entry that crossed the cap, so no entry is split.

**Anti-bloat guard:** no new lint check (segment-awareness folded into the existing id-integrity lint — ids unique + monotonic *across segments*); exactly one new MEDIUM rule (LOG-M-006). The index and prev/next are one line each, not a subsystem.

---

## FU.6 — Canonical id vs alias

**Requirement (verbatim, alias FU.0.2):** the operator restarts at FU.0 every turn AND every reviewed document; must never maintain a global counter.

**Design (folded into revised LOG-M-005; closes F-002/F-006/F-020/F-030):**

- **Canonical id** = **logger-assigned** (the LLM mints it), **unique and strictly monotonic per log across all segments**, never resets (FU.0, FU.1, … FU.50, …; `DEC-LLM-001`, `DEC-LLM-002`, …).
- **Alias** = the operator's raw turn-local / document-local label (`FU.0`, `FU.0.1`, `FU.1`, …), which may restart freely. Recorded **verbatim** as a heading suffix `(alias: <label>)` — zero burden on the operator, full provenance kept.
- **Same rule for `DEC-LLM-NNN`.**
- **Taught in the templates** (not just the design doc) — a two-line "Ids & aliases" note + a before/after example in the appendix, because the UX finding was that the *template* never explained the scheme (F-006/F-030).

---

## FU.8 — Worked examples

**Requirement (verbatim, alias FU.0.4):** concrete examples alongside the schema so it is rationalizable.

**Design (closes F-025/F-029; keeps rule lean):**

- **One embedded worked example inside each template** (real, lightly genericized): FEEDBACK-LOG template gets a genericized **FU.3 (commit-push-cadence)** DONE exemplar; LLM-DECISION-LOG template gets a genericized **DEC-LLM-001 (ratify-approach-B)** exemplar.
- **New examples appendix** `staging-feedback-logs/examples-appendix.md`: two FU exemplars (a standing DONE directive; an IN-PROGRESS item showing the alias), one DEC-LLM exemplar, the id/alias before-after, and a segment-rotation walkthrough.
- **Rule file stays lean (≤ ~1,500 tokens) and POINTS at the appendix** — it does not embed the examples (that would bloat it).

---

## Proposed defaults (Q1–Q4)

> Marked **PROPOSED-DEFAULT — pending user ratification.** Presented in the design doc, NOT as decided (P-020).

- **Q1 (assistant verbatim):** decision-relevant excerpt + transcript pointer as the default; full-paste documented as **rejected-by-default** with size math (~0.3M–1.5M tokens/100 decisions → re-creates context rot); **full verbatim optional for C3+/ADR-graduating decisions.**
- **Q2 (framework-feedback routing):** active-project log with a `scope: framework` tag (aggregatable later), rather than always repo-root — keeps one capture surface per session.
- **Q3 (hook):** designed in v1 (`hook-design-note.md` stays), **shipped as a separate gated change** (touches `hooks/`).
- **Q4 (backfill):** supported by the design (BACKFILL-marked entries), **execution pending user authorization.**

---

## UX findings disposition (31)

> 22 folded · 9 rebutted. Rebuttals cite the anti-bloat doctrine + evidence. "Folded" = addressed by an FU fold or a zero-machinery clarification.

| ID | Sev | Disposition | Rationale |
|----|-----|-------------|-----------|
| F-001 | 4 | **FOLD** | FU.5 segment rotation. |
| F-002 | 3 | **FOLD** | FU.6 id/alias taught in template. |
| F-003 | 3 | **FOLD** | Assistant announces harvested items in-turn; `Source: inline-doc` + path/anchor is the durable confirmation (zero machinery). |
| F-004 | 2 | **REBUT** | A confirmation message is machinery; the written entry *is* the confirmation. Operator re-reads. Their own note rates it low. |
| F-005 | 2 | **REBUT** | Hand-maintained status dashboard drifts (the exact [internal-kb] failure); hook-generated = machinery. Segment Index + `grep 'Disposition: OPEN'` cover triage at zero cost. |
| F-006 | 3 | **FOLD** | FU.6 taught in template + appendix before/after. |
| F-007 | 2 | **FOLD** | One-line glosses for `chat` / `inline-doc` / `transcript`. |
| F-008 | 2 | **FOLD** | One-line note in decision-log template on user-full vs assistant-excerpt+pointer + why (size). |
| F-009 | 2 | **FOLD** | Document the append-only correction pattern (follow-up entry corrects; original verbatim stays as the record). |
| F-010 | 2 | **REBUT** | A disposition state-machine is exactly the worktracker DECISION entity's job (H-33); graduation covers it. Lint check 3 already asserts terminal evidence. MEDIUM-tier by ceiling constraint. |
| F-011 | 2 | **FOLD** | Same correction pattern: reopen = new entry referencing the old canonical id. |
| F-012 | 2 | **FOLD** | One-line rationale (FU tracks status over time → Disposition; a decision is point-in-time → none). No field unification (that adds machinery). |
| F-013 | 2 | **FOLD** | Make Context field order identical across both logs (parallelism, zero cost). |
| F-014 | 1 | **FOLD** | Standardize `YYYY-MM-DD` in templates. |
| F-015 | 3 | **FOLD** | Standardize ONE inline marker (`FU:` / `DEC:` line, optionally blockquoted); removes "any inline directive" ambiguity — a simplification. |
| F-016 | 2 | **FOLD** | Q3 default acknowledged; until the hook ships, the operator fills only what they know; sidecar-key reference keeps burden low. |
| F-017 | 2 | **FOLD (partial)** | Evidence-format *examples* added to appendix. **REBUT** strict format validation — evidence is intentionally free-form (hash | path | id | reason); lint asserts presence only. |
| F-018 | 2 | **FOLD (partial)** | Segment Index + H-23 nav table give navigation. **REBUT** tagging/categories/search (machinery). |
| F-019 | 2 | **REBUT** | Same as F-005 — drift-prone machinery; grep suffices. |
| F-020 | 2 | **FOLD** | FU.6 alias formalization (`(alias: FU.0.1)`) removes the FU.0.1-vs-FU.N confusion. |
| F-021 | 1 | **REBUT** | Shorthand/quick-capture syntax is the bloat class that sank the ADR convention; the inline `FU:` marker *is* the quick capture. |
| F-022 | 1 | **REBUT** | Backfill Queue is intentionally a lightweight candidate list, not full entries; promotion converts a row to a full entry. The format difference is meaningful. |
| F-023 | 2 | **REBUT** | Single-line Context is intentional density; multi-line expansion multiplies file size across every entry, directly worsening FU.5. Parallel order (F-013) gets the scannability win without the bulk. |
| F-024 | 1 | **FOLD** | Bootstrap/template banner clarified (truthfully — not over-claiming ratification). |
| F-025 | 2 | **FOLD** | Rule file points at the examples appendix (intended lean-rule design). |
| F-026 | 3 | **FOLD (partial)** | Standardized syntax + in-turn announce give a recovery signal. **REBUT** writing a `<!-- HARVESTED -->` comment back into the operator's source doc (intrusive doc-mutation machinery). |
| F-027 | 2 | **REBUT** | Post-hoc L5 lint is the right cheap enforcement for a MEDIUM convention; the assistant's capture-time self-check is the preventive layer. Real-time validator = machinery. |
| F-028 | 1 | **REBUT** | Pointer validation = machinery; hook stamping makes hand-typing the rare exception (their own note). |
| F-029 | 2 | **FOLD** | Embedded examples (FU.8). |
| F-030 | 2 | **FOLD** | Id/alias scheme taught in template (FU.6). |
| F-031 | 1 | **FOLD (partial)** | A tiny "Common cases" note (forgot → backfill; find → index/grep; fix → follow-up entry). **REBUT** a full FAQ (machinery). |

**Tally:** folded = 22 (F-001,002,003,006,007,008,009,011,012,013,014,015,016,017,018,020,024,025,026,029,030,031); rebutted = 9 (F-004,005,010,019,021,022,023,027,028).

---

## Token budget

Rule file target **≤ ~1,500 tokens**. Baseline ~1,050. **Final: 1,584 tokens** (`tiktoken cl100k`). The ~84-token overage over the soft target buys two newly-required subsystems (FU.5 segment rotation + FU.6 alias scheme) without which the mandate is unmet; anti-bloat was honored by (a) pushing all worked examples to `examples-appendix.md`, (b) delegating the exact field-format strings to the templates, (c) adding exactly one new MEDIUM rule and zero new lint checks. Measured iteratively down from a 1,908-token first pass. Reporting the honest measured count (P-022) rather than an estimate.

---

## Files changed

| File | Change |
|------|--------|
| `design/feedback-decision-log-convention-design.md` | FU.5/6/8 folded; Q1–Q4 → PROPOSED-DEFAULTs; UX disposition summary; changelog appended. |
| `design/staging-feedback-logs/feedback-decision-logs-standards.md` | LOG-M-005 revised (canonical/alias); LOG-M-006 added (rotation); inline-marker standard; Source glosses; points to appendix. |
| `design/staging-feedback-logs/examples-appendix.md` | **NEW** — worked examples (FU.8). |
| `design/staging-feedback-logs/FEEDBACK-LOG.template.md` | Segment header; id/alias note + example; standardized inline marker; embedded worked example. |
| `design/staging-feedback-logs/LLM-DECISION-LOG.template.md` | Segment header; verbatim-policy note; embedded worked example; parallel Context. |
| `design/staging-feedback-logs/hook-design-note.md` | Q3-default note; segment-size trigger acknowledged. |
| `FEEDBACK-LOG.md` / `LLM-DECISION-LOG.md` (live) | Banner clarified (F-024) — truthful, no ratification over-claim. |
