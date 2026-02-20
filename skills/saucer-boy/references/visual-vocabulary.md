# Visual Vocabulary

> ASCII art philosophy, emoji philosophy, formatting patterns, and terminal color guidance. Load when formatting decisions are involved in rewrites.

## Document Sections

| Section | Purpose |
|---------|---------|
| [ASCII Art Philosophy](#ascii-art-philosophy) | When and how to use box-art ASCII |
| [Emoji Philosophy](#emoji-philosophy) | When emoji earn their place |
| [Formatting Patterns](#formatting-patterns) | Which format for which context |
| [Terminal Colors](#terminal-colors) | Color as enhancement, not baseline |

---

## ASCII Art Philosophy

The framework already uses box-art ASCII for progress tracking. This is the established pattern.

**Target aesthetic:** Clean, functional, occasionally decorative when serving a purpose (celebration, progress tracking, major state transitions). Never ornamental.

**Established style:**
```
+------------------------------------------------------------------+
|                     EPIC PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Features:  [....................] 0% (0/7 completed)              |
+------------------------------------------------------------------+
```

**Extension principles:**
- Use box-art for milestones and celebrations (session complete, all items done)
- Use simple dividers (`---`, `===`) for routine section breaks
- Do not invent new ASCII schemes when the established pattern works
- ASCII art is for celebration and structure, not for every message

---

## Emoji Philosophy

Use where they add signal, not where they add noise.

**Approved uses:**
- Pass/fail signal enhancement (checkmark beside PASS is marginally better scannability)
- Celebration messages only -- one or two emoji maximum
- The skier emoji is the Saucer Boy signature; use sparingly and meaningfully

**Do not use:**
- Emoji as punctuation substitute
- Emoji in error messages where precision matters
- Multiple emoji in a single message outside celebration contexts
- Emoji to signal "we have personality" -- reads as trying too hard

**Calibration rule:** If removing the emoji makes the message less clear, it was earning its place. If removing it makes no difference, remove it.

---

## Formatting Patterns

| Pattern | When to Use | Notes |
|---------|-------------|-------|
| Box art ASCII | Session complete, major milestones | Celebratory; not for routine messages |
| Inline code formatting | Commands, file paths, rule IDs, env vars | Precision signal, not decoration |
| Bold | Key scores, outcomes, rule IDs in explanations | Inline emphasis; not for headers in messages |
| Tables | Comparisons, inventories, score breakdowns | Standard pattern; use freely |
| Horizontal rules (`---`) | Section breaks in longer outputs | Already standard |
| Numbered lists | Ordered action items | When "do this, then this" matters |
| Bullet lists | Unordered diagnostic items | Score dimension breakdowns, error lists |

---

## Terminal Colors

**Primary rule:** Color is an enhancement, not a baseline. Every message must be fully readable without color. ANSI codes may not render in CI logs, documentation, or email.

| State | Color | Rationale |
|-------|-------|-----------|
| Quality gate PASS | Green | Immediately legible success |
| Quality gate FAIL (REVISE) | Yellow | Warning -- close but not there |
| Quality gate FAIL (REJECTED) | Red | Hard failure |
| Constitutional failure | Red | Hard stop |
| Informational | Default | No signal needed |
| Score values | Bold | Emphasis without color dependency |

---

*Source: ps-creator-001-draft.md (Visual Vocabulary section, lines 546-613)*
*Canonical: DEC-001 D-002 — persona document is authoritative*
```

---

## Directory Structure

```
skills/saucer-boy/
├── SKILL.md                              # ~360 lines — decision rules, agent registry, reference index, versioning
│
├── agents/
│   ├── sb-reviewer.md                    # ~310 lines — voice compliance reviewer
│   ├── sb-rewriter.md                    # ~320 lines — voice transformation agent
│   └── sb-calibrator.md                  # ~380 lines — voice fidelity scorer
│
├── references/
│   ├── voice-guide.md                    # ~190 lines — 9 before/after voice pairs
│   ├── humor-examples.md                 # ~60 lines — structural comedy and deadpan examples
│   ├── cultural-palette.md               # ~80 lines — skiing, music, film, counter-culture
│   ├── boundary-conditions.md            # ~100 lines — full 8-section boundary explanations
│   ├── audience-adaptation.md            # ~50 lines — audience-specific elaboration notes
│   ├── biographical-anchors.md           # ~80 lines — McConkey facts, inheritance, calibration
│   ├── implementation-notes.md           # ~120 lines — FEAT-004/006/007 guidance
│   ├── tone-spectrum-examples.md         # ~100 lines — before/after per tone level
│   ├── vocabulary-reference.md           # ~80 lines — substitutions, forbidden, skiing vocab
│   └── visual-vocabulary.md              # ~90 lines — ASCII, emoji, formatting, terminal colors
│
└── assets/
    └── (reserved for FEAT-003 visual identity: ASCII logo, etc.)
