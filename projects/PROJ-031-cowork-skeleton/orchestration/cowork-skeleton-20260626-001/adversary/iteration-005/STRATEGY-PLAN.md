# Iteration-005 — Blind C4 Tournament Strategy Plan

> Re-adversary of the CONSOLIDATED design after ps-architect ADR remediation (D7/RTB-1..5/tests-strip) + nse-requirements ADR-003 mirror. Target: S-014 composite **≥ 0.92** (H-13). Prior: iteration-004 = 0.74 REVISE (Internal Consistency 0.62 was the drag; remediation specifically targeted it).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Protocol](#protocol) | The blind-agent + dependency-order rules |
| [Input set](#input-set-what-every-adversary-reviews) | The 5 consolidated artifacts under review |
| [Launch matrix](#launch-matrix-6-group-order) | Which agent runs in which group |
| [Blind prompt template](#blind-prompt-template) | The contract every adversary agent gets |
| [Remediation routing](#remediation-routing) | Owner-first feedback rules |

## Protocol

Per memory `feedback-adversary-blind-agents` (re-read before launch):
- **One strategy = one blind background agent.** An adversary NEVER reads another adversary's findings, NEVER reads prior iterations, NEVER reads the scorer. It reviews ONLY the design artifacts in the input set.
- **6-group order — sequential BETWEEN groups, parallel WITHIN:** A self-refine → B steelman → C challenge → D verify → E decompose → F score. Launch a group, wait for it to finish, then launch the next. Within a group, all agents run concurrently (single message, multiple Agent calls).
- **H-16:** Steelman (B / S-003) MUST precede Devil's Advocate (C / S-002).
- **Findings route to the original CREATOR** (ADR→ps-architect, requirements→nse-requirements). Adversaries NEVER edit design artifacts. Group A self-refine is the ONLY group whose creator may edit (its own artifacts), owner-first.
- **F (S-014) runs last and is the ONLY agent permitted to read all findings.**

## Input set (what every adversary reviews)

All relative to `projects/PROJ-031-cowork-skeleton/`:
1. `decisions/ADR-001-skeleton-derived-branch-strategy.md` (dedicated-repo + tests/ strip ~1,417 files)
2. `decisions/ADR-003-credential-protection-supply-chain.md` (D1–D7, RTB-1..5, SC-06)
3. `requirements/phase1-requirements.md` (REQ-001..051 after ADR-003 mirror)
4. `security/phase2-stride-threat-model.md`
5. `security/phase2-attack-surface.md`

(ADR-002 is SUPERSEDED by ADR-003 — out of scope. Context for the domain: `research/cowork-plugin-install-mechanism.md`, `research/R-001-cowork-test-validation.md`.)

## Launch matrix (6-group order)

| Group | Strategy | Agent | Blind? | Edits? | Output file |
|-------|----------|-------|--------|--------|-------------|
| **A** self-refine | S-010 Self-Refine | ps-architect (CREATOR voice) | No (is creator) | Yes — ADR-side only; flags req-side to nse-requirements | `s-010-self-refine-findings.md` |
| **B** steelman | S-003 Steelman | adv-executor | Yes | No | `s-003-steelman-findings.md` |
| **C** challenge | S-002 Devil's Advocate | adv-executor | Yes | No | `s-002-devils-advocate-findings.md` |
| **C** challenge | S-004 Pre-Mortem | adv-executor | Yes | No | `s-004-pre-mortem-findings.md` |
| **C** challenge | S-001 Red Team | adv-executor | Yes | No | `s-001-red-team-findings.md` |
| **D** verify | S-007 Constitutional AI | adv-executor | Yes | No | `s-007-constitutional-ai-findings.md` |
| **D** verify | S-011 Chain-of-Verification | adv-executor | Yes | No | `s-011-cove-findings.md` |
| **E** decompose | S-012 FMEA | adv-executor | Yes | No | `s-012-fmea-findings.md` |
| **E** decompose | S-013 Inversion | adv-executor | Yes | No | `s-013-inversion-findings.md` |
| **F** score | S-014 LLM-as-Judge | adv-scorer | reads ALL | No | `s-014-quality-score.md` |

Wall-clock = 6 sequential phases (A→B→C→D→E→F); phases C/D/E fan out 3/2/2 concurrent blind agents.

## Blind prompt template

Every Group B–E agent receives this contract (instantiated per strategy):

```
You are adv-executor running strategy {S-NNN} ({name}) for PROJ-031, criticality C4, quality gate ≥0.92.
BLINDNESS (HARD): Review ONLY the 5 design artifacts listed below. You MUST NOT read ANY file under
  .../adversary/ (no other strategy's findings, no prior iterations iteration-001..004, no scores).
  Reading another adversary's output contaminates the tournament — do not do it.
INPUT (read all 5): [the input set paths above]
TASK: Apply {strategy} rigorously. Produce findings with severity Critical/Major/Minor. For each finding give:
  location (file + REQ/section), the problem, why it matters at C4, and a recommended remediation tagged
  with its OWNER (ADR→ps-architect | requirements→nse-requirements). You do NOT edit any design artifact.
GUARDRAILS: P-003 no sub-agents; P-022 no overstated confidence; persist (P-002) to the output file below.
OUTPUT: write to .../adversary/iteration-005/{output file}. Final message ≤120 words: counts by severity + top finding.
```

## Remediation routing

After F scores:
- **≥ 0.92** → tournament PASS. Proceed to Phase 3.
- **< 0.92** → consolidate findings by OWNER, sequence owner-first (ps-architect resolves ADR decisions first; nse-requirements mirrors), remediate, then re-run from Group B (or targeted groups if the scorer localizes the drag). Respect H-14 min-3-iteration / RT-M-010 C4 ceiling=10.
