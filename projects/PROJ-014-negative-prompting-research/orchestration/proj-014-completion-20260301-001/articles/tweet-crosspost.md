---
title: Tweet + Cross-Post — PROJ-014 Negative Prompting Research
date: 2026-03-01
status: final
voice: saucer-boy
---

# Tweet + Cross-Post

## Document Sections

| Section | Purpose |
|---------|---------|
| [Tweet](#tweet) | 280-char announcement for Medium article |
| [Cross-Post Thread](#cross-post-thread) | 6-post X thread / 5-post LinkedIn thread |
| [Character Counts](#character-counts) | Verification |

---

## Tweet

270 tests across 3 Claude models. NPT-013 (structured negation): 100% compliance. Positive-only: 92.2%. The 7.8pp gap held across every constraint and model — McNemar p=0.016. The variable is structure, not polarity. [Medium article](../articles/medium-negative-prompting.md)

**Character count (without URL):** 216 chars + URL. Within budget.

---

## Cross-Post Thread

> 6 posts for X (Post 4 split into 4a/4b). 5 posts for LinkedIn (Post 4 unsplit). Each under 280 chars for X compatibility.

---

### Post 1 — Hook + Key Finding

270 LLM compliance tests. 3 Claude models. One format hit 100%.

Positive-only: 92.2%. McNemar exact p=0.016. NPT-013 — structured negation — never lost a single matchup across any constraint, model, or scenario.

The variable is structure, not polarity.

**Character count:** 254 chars.

---

### Post 2 — What We Tested

90 matched pairs. 75 academic and industry sources. 10 constraints from a production system. 3 pressure scenarios each. Blind-scored by a separate model instance.

No cherry-picking. NPT-013 won every matchup — every constraint, every model, every scenario.

**Character count:** 257 chars.

---

### Post 3 — The Format That Works

The winning format — NPT-013 — has three parts:

NEVER {action} — Consequence: {impact}. Instead: {alternative}.

The prohibition draws a hard line. Stakes come from the consequence. And the alternative gives the model somewhere to go. Drop any part and compliance falls.

**Character count:** 271 chars.

---

### Post 4a — The Insight (X only)

The field says: use positive framing. True, but incomplete.

Constraints that break in production aren't failing because of polarity. They're failing because they lack stakes and a path forward.

**Character count:** 194 chars.

---

### Post 4b — The Data (X only)

Behavioral timing constraints — *when* to act — showed a 56% violation rate under positive-only framing. Blunt negation hit 97.8%. Structured negation: 0%.

Haiku showed a 10pp improvement. The less capable the model, the more structure matters.

**Character count:** 245 chars.

---

### Post 4 — The Insight (LinkedIn — unsplit)

The field says: use positive framing. True, but incomplete.

Constraints that break in production aren't failing because of polarity. They're failing because they lack stakes and a path forward.

Behavioral timing constraints — *when* to act — showed a 56% violation rate under positive-only framing. Blunt negation hit 97.8%. Structured negation: 0%. Haiku showed a 10pp improvement. The less capable the model, the more structure matters.

---

### Post 5 — Link + Call to Action

Full writeup covers the methodology, why McNemar over chi-square for matched-pair designs, the failure modes, and 5 things you can apply today.

Read it: [Medium article](../articles/medium-negative-prompting.md)

14-pattern NPT taxonomy + Jerry Framework docs: [Jerry docs](../articles/jerry-docs-negative-prompting.md)

**Character count (without URLs):** 204 chars + URLs. Within budget.

---

## Character Counts

| Item | Count | Budget | Status |
|------|-------|--------|--------|
| Tweet | 216 + URL | 280 | Pass |
| Post 1 | 254 | 280 | Pass |
| Post 2 | 257 | 280 | Pass |
| Post 3 | 271 | 280 | Pass |
| Post 4a (X) | 194 | 280 | Pass |
| Post 4b (X) | 245 | 280 | Pass |
| Post 5 | 204 + URLs | 280 | Pass |

> Post 4 for X is split into 4a + 4b (6-post thread). For LinkedIn where limits are higher, use the unsplit Post 4 version (5-post thread).
