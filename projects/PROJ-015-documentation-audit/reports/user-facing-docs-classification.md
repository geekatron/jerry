# Diataxis Classification Report: User-Facing Documentation

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary Table](#summary-table) | Quick-view classification of all 6 docs |
| [Per-Document Classification](#per-document-classification) | Detailed axis analysis per document |
| [Key Findings](#key-findings) | Documents requiring decomposition |

---

## Summary Table

| File | Quadrant | Confidence | Mixing | Decomposition |
|------|----------|------------|--------|---------------|
| **BOOTSTRAP.md** | How-To | 0.95 (High) | No | No |
| **INSTALLATION.md** | How-To | 0.92 (High) | Minimal (explanation for context only) | No |
| **CLAUDE-MD-GUIDE.md** | Explanation | 0.80 (Medium) | **Yes** (explanation + how-to mixed) | **Yes** -- split into explanation + how-to |
| **getting-started.md** | Tutorial | 0.93 (High) | No | No |
| **prompt-templates.md** | How-To | 0.94 (High) | No | No |
| **prompt-quality.md** | Reference | 0.85 (Medium-High) | **Yes** (reference + explanation + how-to) | **Yes** -- split into reference + explanation + how-to |

- **Classification date:** 2026-03-02
- **Classifier:** diataxis-classifier (diataxis skill)

---

## Per-Document Classification

### 1. `docs/BOOTSTRAP.md`

**Primary Quadrant:** How-To Guide | **Confidence:** 0.95

- **Practical/Theoretical:** Practical -- teaches HOW to set up symlinks, run bootstrap commands, troubleshoot linking issues
- **Acquisition/Application:** Application -- reader is already working with Jerry and needs to execute specific operational tasks
- **Mixing:** No -- pure how-to guide with step-by-step procedures, platform notes, command reference, troubleshooting
- **Decomposition:** Not needed

### 2. `docs/INSTALLATION.md`

**Primary Quadrant:** How-To Guide | **Confidence:** 0.92

- **Practical/Theoretical:** Practical -- extensive step-by-step installation procedures (GitHub install, local clone, session install), configuration steps, verification checks
- **Acquisition/Application:** Application -- readers are working developers installing Jerry
- **Mixing:** Minimal -- small explanation segments ("What does 'marketplace' mean?", "Why does SSH come up?") are peripheral context-setting (3-5% of content)
- **Decomposition:** Not needed -- explanatory segments are tightly integrated as disambiguation

### 3. `docs/CLAUDE-MD-GUIDE.md`

**Primary Quadrant:** Explanation | **Confidence:** 0.80

- **Practical/Theoretical:** Theoretical -- primary focus is understanding WHY Jerry's context architecture is structured (tiered loading, separation of `.context/` and `.claude/`)
- **Acquisition/Application:** Acquisition -- targeted at new contributors learning how Jerry works
- **Mixing:** **Yes, moderate** -- "Modifying Rules," "Modifying Patterns," "Adding Skills" sections contain procedural how-to content embedded in explanation framework
- **Decomposition:** **Yes** -- split into:
  1. Explanation: "Context Architecture" (understanding tiered loading, why separation exists)
  2. How-To: "Modifying Rules," "Modifying Patterns," "Adding Skills," "Bootstrap for New Contributors"

### 4. `docs/runbooks/getting-started.md`

**Primary Quadrant:** Tutorial | **Confidence:** 0.93

- **Practical/Theoretical:** Practical -- step-by-step hands-on procedures
- **Acquisition/Application:** Acquisition -- designed for users with freshly installed Jerry learning the framework
- **Mixing:** No -- pure tutorial with scaffolded learning steps
- **Decomposition:** Not needed -- excellent sequencing (Prerequisites -> Procedure -> Verification -> Troubleshooting -> Next Steps)

### 5. `.context/rules/prompt-templates.md`

**Primary Quadrant:** How-To Guide | **Confidence:** 0.94

- **Practical/Theoretical:** Practical -- copy-paste templates, placeholder substitution rules, worked examples
- **Acquisition/Application:** Application -- readers actively using Jerry need templates for specific workflows
- **Mixing:** No -- templates are the core artifact; Quick-Select is navigation
- **Decomposition:** Not needed -- six templates are tightly related and Quick-Select ties them together

### 6. `.context/rules/prompt-quality.md`

**Primary Quadrant:** Reference (with secondary Explanation) | **Confidence:** 0.85

- **Practical/Theoretical:** Mixed -- primarily theoretical (understanding quality dimensions, anti-patterns) with practical elements (checklist, scoring formula)
- **Acquisition/Application:** Application -- readers actively writing and evaluating prompts
- **Mixing:** **Yes, significant** -- serves three purposes:
  1. Reference: quality rubric (7 criteria, weights, scoring formula) -- lookup material
  2. Explanation: "5 Elements," "Adversarial Critique Loop," "Anti-Patterns" -- conceptual understanding
  3. How-To: "Pre-Submission Checklist" -- procedural validation
- **Decomposition:** **Yes** -- split into:
  1. Reference: quality rubric + agent selection table
  2. Explanation: 5 elements, adversarial critique loop, anti-patterns
  3. How-To: pre-submission checklist

---

## Key Findings

**Strong Single-Quadrant (no decomposition needed):**
- BOOTSTRAP.md (how-to)
- getting-started.md (tutorial)
- prompt-templates.md (how-to)

**Minor Mixing (keep intact):**
- INSTALLATION.md (how-to with embedded explanation fragments; integrated well enough to keep)

**Significant Mixing (decomposition recommended):**
- **CLAUDE-MD-GUIDE.md:** Explanation core with embedded how-to sections
- **prompt-quality.md:** Three-way split needed (reference, explanation, how-to)
