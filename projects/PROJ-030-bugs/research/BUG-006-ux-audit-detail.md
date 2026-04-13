# BUG-006: UX Sub-Skill Output Path Audit Detail

> Persisted audit findings from exploration agents. Referenced by BUG-006 worktracker entity.
> Verification command: `grep -rl 'skills/ux-.*output\|skills/user-experience.*output' skills/ux-*/ skills/user-experience/`
> Result: 60 files (verified 2026-03-31)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Methodology](#methodology) | How the audit was conducted |
| [Per-Skill Line-Level Citations](#per-skill-line-level-citations) | Exact file paths and line numbers for all 11 sub-skills |
| [Verification](#verification) | Reproducibility commands |

---

## Methodology

Each of the 11 UX sub-skills was audited by an exploration agent that:
1. Read every `.md`, `.yaml`, and `.yml` file in the skill directory tree
2. Searched for `skills/ux-*/output/` or `skills/user-experience/output/` patterns
3. Recorded file path, line number, and the hardcoded path found

---

## Per-Skill Line-Level Citations

### 1. user-experience (parent orchestrator) — 7 files

| File | Lines | Content |
|------|-------|---------|
| `skills/user-experience/SKILL.md` | 141-151, 378 | Agent output table (11 entries), synthesis output path |
| `skills/user-experience/agents/ux-orchestrator.md` | 216, 219, 231, 293-295, 342 | Engagement ID generation, output locations, directory creation |
| `skills/user-experience/agents/ux-orchestrator.governance.yaml` | 73-76 | `output.location` field |
| `skills/user-experience/rules/ux-routing-rules.md` | 161, 180-185, 237, 254, 307 | Crisis output, signoff files, bypass docs, engagement path |
| `skills/user-experience/rules/wave-progression.md` | 83-88, 129 | Signoff file paths, bypass path |
| `skills/user-experience/rules/ci-checks.md` | 304, 330, 403, 415, 570-581, 606-627, 672-685, 723-724 | CI check rules, test scope definitions |
| `skills/user-experience/rules/synthesis-validation.md` | 181, 193 | Synthesis report paths |

### 2. ux-heuristic-eval — 5 files

| File | Lines | Content |
|------|-------|---------|
| `skills/ux-heuristic-eval/SKILL.md` | 112, 116, 195, 241, 328, 363, 487 | Agent table, examples, output spec |
| `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.md` | 210, 298 | Output location, artifact path |
| `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.governance.yaml` | 51 | `output.location` field |
| `skills/ux-heuristic-eval/rules/mcp-runbook.md` | 204 | Output persistence statement |
| `skills/ux-heuristic-eval/templates/heuristic-report-template.md` | 445 | Template output path |

### 3. ux-jtbd — 5 files

| File | Lines | Content |
|------|-------|---------|
| `skills/ux-jtbd/SKILL.md` | 134, 412, 629 | Agent table, output spec, P-002 |
| `skills/ux-jtbd/agents/ux-jtbd-analyst.md` | 89, 315, 349, 373 | Output location, artifact paths |
| `skills/ux-jtbd/agents/ux-jtbd-analyst.governance.yaml` | 50 | `output.location` field |
| `skills/ux-jtbd/templates/switch-interview-guide.md` | 75, 374 | Template output paths |
| `skills/ux-jtbd/templates/job-statement-template.md` | 348 | Template output path |

### 4. ux-lean-ux — 7 files

| File | Lines | Content |
|------|-------|---------|
| `skills/ux-lean-ux/SKILL.md` | 115, 199, 424 | Agent table, example, output spec |
| `skills/ux-lean-ux/agents/ux-lean-ux-facilitator.md` | 303, 419, 422 | Output location, artifact paths |
| `skills/ux-lean-ux/agents/ux-lean-ux-facilitator.governance.yaml` | 51 | `output.location` field |
| `skills/ux-lean-ux/templates/hypothesis-backlog-template.md` | 398, 421 | Template output paths |
| `skills/ux-lean-ux/templates/assumption-map-template.md` | 377 | Template output path |
| `skills/ux-lean-ux/rules/lean-ux-methodology-rules.md` | 447 | Agent definition reference |
| `skills/ux-lean-ux/rules/mcp-runbook.md` | 208 | Output persistence statement |

### 5. ux-heart-metrics — 3 files

| File | Lines | Content |
|------|-------|---------|
| `skills/ux-heart-metrics/SKILL.md` | 152, 488, 717 | Agent table, output spec, P-002 |
| `skills/ux-heart-metrics/agents/ux-heart-analyst.md` | 288, 405 | Output location, artifact path |
| `skills/ux-heart-metrics/agents/ux-heart-analyst.governance.yaml` | 50 | `output.location` field |

### 6. ux-kano-model — 6 files

| File | Lines | Content |
|------|-------|---------|
| `skills/ux-kano-model/SKILL.md` | 120, 193, 403, 412, 443, 675 | Agent table, examples, output spec |
| `skills/ux-kano-model/agents/ux-kano-analyst.md` | 135, 238, 272, 389 | Output location, artifact paths |
| `skills/ux-kano-model/agents/ux-kano-analyst.governance.yaml` | 53 | `output.location` field |
| `skills/ux-kano-model/templates/feature-priority-template.md` | 222, 245 | Template output paths |
| `skills/ux-kano-model/templates/kano-survey-template.md` | 144 | Template output path |
| `skills/ux-kano-model/rules/kano-methodology-rules.md` | 291 | Agent definition reference |

### 7. ux-atomic-design — 6 files

| File | Lines | Content |
|------|-------|---------|
| `skills/ux-atomic-design/SKILL.md` | 117, 204, 364, 487, 656 | Agent table, examples, output spec |
| `skills/ux-atomic-design/agents/ux-atomic-architect.md` | 126, 254, 361 | Output location, artifact paths |
| `skills/ux-atomic-design/agents/ux-atomic-architect.governance.yaml` | 51 | `output.location` field |
| `skills/ux-atomic-design/templates/component-inventory-template.md` | 462, 486 | Template output paths |
| `skills/ux-atomic-design/rules/atomic-design-rules.md` | 373 | Agent definition reference |
| `skills/ux-atomic-design/rules/mcp-runbook.md` | 261 | Output persistence statement |

### 8. ux-inclusive-design — 7 files

| File | Lines | Content |
|------|-------|---------|
| `skills/ux-inclusive-design/SKILL.md` | 126, 215, 446, 628 | Agent table, examples, output spec |
| `skills/ux-inclusive-design/agents/ux-inclusive-evaluator.md` | 358, 487 | Output location, artifact path |
| `skills/ux-inclusive-design/agents/ux-inclusive-evaluator.governance.yaml` | 54 | `output.location` field |
| `skills/ux-inclusive-design/templates/persona-spectrum-template.md` | 231, 252 | Template output paths |
| `skills/ux-inclusive-design/templates/accessibility-report-template.md` | 547, 574 | Template output paths |
| `skills/ux-inclusive-design/rules/inclusive-design-rules.md` | 451 | SKILL.md reference |
| `skills/ux-inclusive-design/rules/mcp-runbook.md` | 251 | Output persistence statement |

### 9. ux-behavior-design — 5 files

| File | Lines | Content |
|------|-------|---------|
| `skills/ux-behavior-design/SKILL.md` | 119, 203, 351, 426, 525, 698 | Agent table, examples, output spec |
| `skills/ux-behavior-design/agents/ux-behavior-diagnostician.md` | 122, 300, 416, 458 | Output location, artifact paths |
| `skills/ux-behavior-design/agents/ux-behavior-diagnostician.governance.yaml` | 53 | `output.location` field |
| `skills/ux-behavior-design/templates/bmap-diagnosis-template.md` | 267 | Template artifact path |
| `skills/ux-behavior-design/rules/fogg-behavior-rules.md` | 390 | Agent definition reference |

### 10. ux-design-sprint — 4 files

| File | Lines | Content |
|------|-------|---------|
| `skills/ux-design-sprint/SKILL.md` | 119, 202, 357, 422, 522, 729 | Agent table, examples, output spec |
| `skills/ux-design-sprint/agents/ux-sprint-facilitator.md` | 132, 266, 382, 408, 450 | Output location, artifact paths |
| `skills/ux-design-sprint/agents/ux-sprint-facilitator.governance.yaml` | 58 | `output.location` field |
| `skills/ux-design-sprint/rules/sprint-methodology-rules.md` | 37, 436 | Output path, agent reference |

### 11. ux-ai-first-design — 5 files

| File | Lines | Content |
|------|-------|---------|
| `skills/ux-ai-first-design/SKILL.md` | 127, 220, 422, 531, 737 | Agent table, examples, output spec |
| `skills/ux-ai-first-design/agents/ux-ai-design-guide.md` | 267, 312, 443, 476, 521 | Output location, artifact paths |
| `skills/ux-ai-first-design/agents/ux-ai-design-guide.governance.yaml` | 60 | `output.location` field |
| `skills/ux-ai-first-design/templates/ai-first-design-template.md` | 374 | Template artifact path |
| `skills/ux-ai-first-design/rules/ai-first-design-rules.md` | 398 | Agent definition reference |

---

## Composition YAML Note

UX sub-skills do **not** have composition YAML files (`*.agent.yaml`). Only eng-team (10 files) and red-team (11 files) use the composition YAML pattern. This is an intentional architectural difference, not a gap in the audit. The UX audit covers governance YAML (11 files), agent .md (11 files), SKILL.md (11 files), templates (12 files), and rules (15 files) — 60 files total.

---

## Verification

**File count verification:**
```bash
grep -rl 'skills/ux-.*output\|skills/user-experience.*output' skills/ux-*/ skills/user-experience/ | wc -l
# Result: 60
```

**Per-skill breakdown:**
| Sub-Skill | Files | Sum Check |
|-----------|-------|-----------|
| user-experience | 7 | 7 |
| ux-heuristic-eval | 5 | 12 |
| ux-jtbd | 5 | 17 |
| ux-lean-ux | 7 | 24 |
| ux-heart-metrics | 3 | 27 |
| ux-kano-model | 6 | 33 |
| ux-atomic-design | 6 | 39 |
| ux-inclusive-design | 7 | 46 |
| ux-behavior-design | 5 | 51 |
| ux-design-sprint | 4 | 55 |
| ux-ai-first-design | 5 | 60 |
| **Total** | **60** | **60** |
