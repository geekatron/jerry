---
document_id: PROJ-006-SYNTH-CP-001
workflow_id: consensus-panel-20260316-001
phase_id: phase-1-draft
authored_by: orch-synthesizer (claude-sonnet-4-6)
date: 2026-03-16
status: COMPLETE
---

# Consensus Panel Synthesis: Implement the Consensus Panel Runner

> **PARTIAL PANEL WARNING:** This synthesis is based on a 2-model panel (Codex / Gemini only).
> Claude was unavailable due to T-002 (nested `CLAUDECODE=1` session — IPC hang prevention).
> This is NOT a full 3-way consensus. All conclusions carry reduced confidence relative to a
> complete panel. Human review is strongly recommended before acting on recommendations.

---

## L0: Executive Summary

- **Both models agree on the fundamental implementation choice:** the Consensus Panel runner should be a pure Python CLI script executed via `uv run`, not a hybrid Bash/Python approach. This is the most actionable and high-confidence finding from the panel.
- **Gemini's draft is the stronger technical artifact.** Codex identified a valid conceptual component model, but Gemini provided runnable code, a complete architecture diagram, and superior risk mitigations. Codex's own critique of Gemini confirms this by praising the Python approach without challenging its core design.
- **A critical flaw exists in Codex's hybrid proposal:** there is no mechanism to pass Bash-generated PIDs to the Python wait function. This flaw was correctly identified by Gemini's critique and is the decisive technical reason to reject the hybrid approach.
- **Seven open questions require human decisions** before implementation begins, covering timeout configuration, credential management, synthesizer CLI contract, retry policy, output retention, and configuration strategy.
- **Implementation can begin now on the agreed architecture.** The areas of divergence (State Manager lifecycle depth, conformance check integration detail) are refinement concerns, not blockers.

---

## Panel Composition Note

| Model | Transport | Status | Reason |
|-------|-----------|--------|--------|
| Claude (claude-sonnet-4-6) | CLI | UNAVAILABLE | T-002: nested `CLAUDECODE=1` session — IPC hang prevention. Claude CLI cannot invoke itself as a subprocess without deadlock risk. |
| Codex (gpt-4o) | CLI (`codex exec --full-auto`) | PARTICIPATED | Draft + cross-critique completed. |
| Gemini (gemini-2.5-pro) | CLI (`gemini --yolo`) | PARTICIPATED | Draft + cross-critique completed. |

**Implication:** With Claude absent, the panel lacks a perspective that might have challenged both models' Python-centrism, offered alternative architectural patterns (e.g., async-first with `asyncio.subprocess`), or provided insight into how Claude CLI's own output format should be handled by the runner. All consensus conclusions should be treated as 2-of-2 agreement, not 3-of-3.

---

## Consensus Points

The following points represent agreement between both participating models. Confidence is HIGH where both models independently arrived at the same position, or where one model's critique explicitly endorsed the other's approach.

**CP-1: Pure Python CLI is the correct implementation form.**
Both models converge on a Python-centric runner. Gemini proposed it directly. Codex's critique of Gemini praised the "robust Python CLI recommendation" without dissent. Gemini's critique of Codex explicitly recommended abandoning the hybrid Bash/Python approach and adopting pure Python. The rationale is consistent across both: Python's `subprocess` module handles parallel process management robustly, `uv run` alignment is required by framework constraints, and Python's error handling and YAML state management are superior to shell scripting.
*Sources: `phase-1-draft-gemini-draft.md` §1; `phase-1-draft-codex-critique.md` §1; `phase-1-draft-gemini-critique.md` §4, Rec 1.*

**CP-2: The five core components are correct: Pre-flight, Worker Launcher, Wait/Timeout Handler, Output Verifier, Synthesis Handoff.**
Both models independently identified the same logical component decomposition. Gemini added a sixth component (State Manager) as an explicit module; Codex referenced state management implicitly. There is no disagreement on the necessity of the five core components.
*Sources: `phase-1-draft-codex-draft.md` §2; `phase-1-draft-gemini-draft.md` §2.*

**CP-3: `subprocess.Popen` is the correct process launch primitive.**
Both models agree the worker launcher should use `subprocess.Popen`, not shell background jobs (`&`). Gemini proposed it; Codex's critique endorsed the approach; Gemini's critique of Codex explicitly called for `subprocess.Popen` adoption.
*Sources: `phase-1-draft-gemini-draft.md` §3; `phase-1-draft-gemini-critique.md` §4, Rec 1.*

**CP-4: Output verification must check existence AND non-emptiness (at minimum).**
Both models flag file-existence-only checks as insufficient. Gemini's draft checks existence + `getsize > 0`. Gemini's critique of Codex specifically called out `os.path.exists` alone as insufficient and recommended adding size checks and considering completion marker files. Codex's critique of Gemini also noted the need for handling partial or corrupted outputs.
*Sources: `phase-1-draft-gemini-draft.md` §3; `phase-1-draft-gemini-critique.md` §4, Rec 4; `phase-1-draft-codex-critique.md` §3.*

**CP-5: `stdout`/`stderr` from worker subprocesses must be redirected to per-model log files.**
Neither model's draft treated silent failure as acceptable. Gemini's draft redirects stdout/stderr to log files in the `Popen` call. Gemini's critique of Codex called the absence of stdout/stderr capture a critical gap that makes debugging "practically impossible." Codex did not disagree.
*Sources: `phase-1-draft-gemini-draft.md` §3; `phase-1-draft-gemini-critique.md` §3.*

**CP-6: Graceful termination must follow SIGTERM → wait → SIGKILL escalation (never immediate SIGKILL).**
Gemini's draft implements `proc.terminate()` → `proc.wait(timeout=2)` → `proc.kill()`. Gemini's critique of Codex explicitly cited Codex's immediate-SIGKILL approach as unsafe. Codex did not defend immediate SIGKILL in its critique of Gemini. There is no dissent on the correct escalation sequence.
*Sources: `phase-1-draft-gemini-draft.md` §3; `phase-1-draft-gemini-critique.md` §2.*

**CP-7: The `CLAUDECODE=1` nested session guard must be implemented in the pre-flight module.**
Both models reference the nested session guard requirement (from the intent document) as belonging in pre-flight. Neither challenges this placement.
*Sources: `phase-1-draft-codex-draft.md` §4, Risk 3; `phase-1-draft-gemini-draft.md` §2, Pre-flight Module.*

**CP-8: State must be persisted to ORCHESTRATION.yaml using atomic write operations.**
Gemini's draft specifies atomic writes (write to `.tmp`, then `os.rename`). Codex's draft acknowledges YAML state management as a responsibility of the Python layer. Codex's critique of Gemini called for more clarity on state management lifecycle but did not challenge atomic writes.
*Sources: `phase-1-draft-gemini-draft.md` §2, State Manager; §4, Risk 3; `phase-1-draft-codex-critique.md` §2.*

---

## Divergence Points

The following points represent disagreement or asymmetric coverage between the two models. Each divergence includes a recommended resolution.

**DP-1: Depth of State Manager specification.**
Gemini treats the State Manager as an explicit, named component with defined responsibilities (atomic writes, state transitions, error state tracking). Codex treats state management as implicit background behavior without a dedicated component. Codex's critique of Gemini identified the State Manager lifecycle (error states, recovery) as underspecified even in Gemini's draft.
*Recommendation:* Accept Gemini's explicit State Manager component. Designate it a first-class module. Prior to implementation, define the state machine: valid states (INITIALIZED, PREFLIGHT_COMPLETE, DRAFTING, CRITIQUING, SYNTHESIZING, COMPLETE, FAILED), valid transitions, and recovery behavior on FAILED. This is a human decision (see OQ-3).
*Sources: `phase-1-draft-gemini-draft.md` §2; `phase-1-draft-codex-critique.md` §2.*

**DP-2: Pre-flight conformance check detail.**
Gemini specifies running `{cli} --version` as a conformance check during pre-flight, with CLI adapter functions to isolate command construction. Codex's critique of Gemini noted this conformance check is "sparse" — it does not address how to handle CLIs that do not support `--version`, how to parse the version output, or how versioning affects capability detection.
*Recommendation:* Gemini's conformance check pattern is correct directionally. Prior to implementation, define the conformance check protocol per CLI: which command validates availability (e.g., `--version`, `--help`, a dry-run probe), what exit codes are accepted, and what minimum version constraints apply. Log conformance check results to the State Manager.
*Sources: `phase-1-draft-gemini-draft.md` §4, Risk 2; `phase-1-draft-codex-critique.md` §2.*

**DP-3: Process group management for orphan/zombie prevention.**
Gemini explicitly recommends `os.setsid` / `os.killpg` to kill entire process groups when a CLI tool spawns child processes. Codex does not address orphan/zombie processes at all (Gemini's critique flagged this as a missed edge case). The question of how to handle the Git Bash / MSYS2 environment's interaction with `os.setsid` (a POSIX call) is unresolved.
*Recommendation:* Adopt Gemini's process group approach as the design intent. Before implementation, verify `os.setsid` behavior under Git Bash on Windows 11 / MSYS2. If `os.setsid` is unavailable or unreliable in the target environment, document the fallback (e.g., Windows Job Objects via `subprocess` `CREATE_NEW_PROCESS_GROUP` flag). This is a platform-specific concern that requires a targeted test.
*Sources: `phase-1-draft-gemini-draft.md` §4, Risk 1; `phase-1-draft-gemini-critique.md` §3.*

**DP-4: Configuration strategy for worker command construction.**
Gemini's critique of Codex identified the absence of a configuration strategy as a significant gap — specifically, how individual model commands are constructed, how dynamic arguments are passed, and where model-specific configuration lives. Gemini's own draft partially addresses this (the `PanelComposition` data structure from pre-flight), but does not specify the external configuration format. Codex is silent on this entirely.
*Recommendation:* Define a YAML/JSON worker configuration schema before implementation. At minimum: model name, executable path, argument template, output file path template, required environment variables, timeout override (if per-model timeouts are adopted — see OQ-1).
*Sources: `phase-1-draft-gemini-critique.md` §3, §4, Rec 5; `phase-1-draft-gemini-draft.md` §2.*

---

## Panel Gaps

These are perspectives and concerns that may be missing due to Claude's absence from the panel. They are inferences, not conclusions, and are flagged for human consideration.

**PG-1: Claude CLI output format and behavioral quirks.**
Claude CLI (`claude`) is one of the three managed worker processes. Gemini and Codex discussed the runner's architecture abstractly, but neither has direct knowledge of Claude CLI's actual argument syntax, output format, exit code conventions, or interactive prompt behavior. A Claude-perspective draft might have provided concrete detail on its own CLI interface, reducing integration risk. *Human action: consult Claude CLI documentation or conduct a manual conformance test before implementing the Claude adapter.*

**PG-2: `asyncio`-based alternative.**
Both participating models converged on synchronous polling with `time.sleep`. A third perspective might have proposed Python's `asyncio.subprocess` for event-driven process management — potentially cleaner than polling loops for I/O-bound concurrent subprocesses. This alternative was not evaluated. *Human action: consider whether an async approach warrants a follow-up spike before committing to the polling design.*

**PG-3: Jerry Framework integration depth.**
The panel was asked to evaluate the runner as either a standalone script or a Jerry skill. Both models leaned toward standalone script with weak justification for the skill option. A Claude perspective, being native to the Jerry Framework, might have provided stronger reasoning about the tradeoffs of tight vs. loose framework coupling, the impact on skill discoverability, and the invocation contract for `orch-synthesizer`. *Human action: confirm the integration model (standalone vs. skill) before implementation.*

**PG-4: Windows-specific subprocess behavior under Git Bash.**
Both models provided POSIX-oriented implementation details. The target platform is Windows 11 with Git Bash (MSYS2/MINGW64). Neither model addressed Windows-specific concerns such as: whether `signal.SIGTERM` behaves correctly under Git Bash for Python-launched subprocesses, how `subprocess.Popen` handles path quoting with MSYS2 path translation, or whether `os.setsid` is available. *Human action: run a targeted Windows/Git Bash compatibility test for the core subprocess primitives before full implementation.*

---

## Implementation Findings

These are actionable spec update candidates for `MULTI_CLI_INTEGRATION.md` v1.2.0. They are numbered to extend the existing T-NNN findings series from prior panel runs.

**T-004: Hybrid Bash/Python architecture is non-functional — adopt pure Python.**
The spec's description of the Consensus Panel runner should not describe or imply a Bash/Python hybrid. The Bash background job (`&`) model cannot pass PIDs to a Python wait function. The spec must specify `subprocess.Popen` as the sole process launch mechanism.
*Evidence: `phase-1-draft-gemini-critique.md` §2, critical implementation gaps.*

**T-005: Output verification must be multi-step: existence + size + optional completion marker.**
The spec should define the output verification contract explicitly. Step 1: file exists. Step 2: file size > 0. Step 3 (optional, recommended for large outputs): completion marker file written by worker upon successful exit. This prevents partial-write false positives.
*Evidence: `phase-1-draft-gemini-draft.md` §3; `phase-1-draft-gemini-critique.md` §4, Rec 4; `phase-1-draft-codex-critique.md` §3.*

**T-006: Worker stdout/stderr must be redirected to named log files — not suppressed.**
The spec must require per-model log files (e.g., `{output_dir}/{model_name}.stdout.log`). Silent subprocess failure is not acceptable. This is a named requirement, not an implementation suggestion.
*Evidence: `phase-1-draft-gemini-critique.md` §3, §4, Rec 3.*

**T-007: Timeout escalation sequence must be SIGTERM → grace period → SIGKILL.**
The spec must prohibit immediate SIGKILL. The required sequence is: send SIGTERM, wait up to N seconds (suggested: 10 seconds) for graceful exit, then send SIGKILL only if the process has not exited. This applies to all worker termination paths (timeout, error, shutdown).
*Evidence: `phase-1-draft-gemini-critique.md` §2, §4, Rec 2.*

**T-008: Pre-flight conformance check is required, not optional.**
The spec must designate the CLI conformance check (run a non-destructive command per CLI, validate exit code) as a mandatory pre-flight step, not an optional enhancement. Failure of a conformance check must update the State Manager and exclude that model from the panel composition.
*Evidence: `phase-1-draft-gemini-draft.md` §4, Risk 2; `phase-1-draft-codex-critique.md` §2.*

**T-009: State Manager must be an explicit, named component with atomic write semantics.**
The spec must define a State Manager component responsible for all ORCHESTRATION.yaml I/O. Writes must use the atomic rename pattern: write to `{file}.tmp`, then `os.rename()` to the final path. Direct in-place writes to ORCHESTRATION.yaml are prohibited.
*Evidence: `phase-1-draft-gemini-draft.md` §2, §4, Risk 3.*

**T-010: Worker configuration must be externalized to a structured config file.**
The spec must define a worker configuration schema (YAML or JSON) that decouples model-specific command construction from runner logic. The runner must read this config at startup. Hardcoded model commands in runner source are prohibited.
*Evidence: `phase-1-draft-gemini-critique.md` §3, §4, Rec 5.*

**T-011: Process group management strategy must be defined for the target platform.**
The spec must address zombie/orphan subprocess prevention. For POSIX-like environments (including Git Bash), the recommended approach is `os.setsid` + `os.killpg`. The spec must include a note on Windows compatibility and require a platform detection check in the pre-flight module to select the correct termination strategy.
*Evidence: `phase-1-draft-gemini-draft.md` §4, Risk 1; `phase-1-draft-gemini-critique.md` §3.*

---

## Open Questions

Aggregated and deduplicated from both drafts. These require human decisions before implementation begins.

**OQ-1: Timeout configuration — global vs. per-model vs. per-phase.**
Should the worker timeout be a single global value, or configurable per-model (e.g., Gemini may be slower than Codex) and per-phase (critique may require more time than draft)? The default value (Codex suggested 300s) also requires confirmation.
*Sources: `phase-1-draft-codex-draft.md` §5; `phase-1-draft-gemini-draft.md` §5, OQ-1.*

**OQ-2: Output retention after synthesis.**
Should worker output files (drafts, critiques, logs) be purged after synthesis completes, or retained as part of the workflow artifact record? Retention has audit trail value; purging reduces storage noise.
*Source: `phase-1-draft-codex-draft.md` §5.*

**OQ-3: State Manager state machine definition.**
What are the valid states and transitions for the ORCHESTRATION.yaml workflow state? What is the recovery behavior when the runner enters FAILED state? Who is responsible for resetting state for a retry?
*Source: `phase-1-draft-codex-critique.md` §2; implied by `phase-1-draft-gemini-draft.md` §2.*

**OQ-4: Retry policy for transient failures.**
If a worker fails due to a transient error (network, API rate limit, transient auth failure), should the runner retry automatically? If so: how many retries, what backoff strategy, and which failure types qualify as retryable vs. permanent?
*Sources: `phase-1-draft-codex-draft.md` §5; `phase-1-draft-gemini-draft.md` §5, OQ-4.*

**OQ-5: Credential management for API fallback.**
When a CLI is unavailable and the pre-flight check selects an API fallback path, how are API keys sourced? Environment variables (e.g., `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`), a central framework config file, or another mechanism?
*Source: `phase-1-draft-gemini-draft.md` §5, OQ-2.*

**OQ-6: orch-synthesizer CLI contract.**
What is the precise command-line interface for invoking `orch-synthesizer`? Specifically: how are draft file paths, critique file paths, panel composition metadata, and workflow ID passed to it? This contract must be defined before the Synthesis Handoff component can be implemented.
*Source: `phase-1-draft-gemini-draft.md` §5, OQ-3.*

**OQ-7: Worker configuration schema and location.**
Where does the worker configuration file live (relative to the runner script or to the project root)? What is the schema — at minimum: model name, executable, argument template, output path template, timeout override, required env vars?
*Source: `phase-1-draft-gemini-critique.md` §4, Rec 5; DP-4 above.*

---

## Quality Score (S-014 Self-Assessment)

This synthesis document is evaluated against the 6-dimension adversarial quality rubric.

| Dimension | Weight | Score | Notes |
|-----------|--------|-------|-------|
| Completeness | 0.20 | 0.90 | All 4 source artifacts read and cited. Panel gap (Claude absent) explicitly documented. One minor gap: `phase-1-draft-codex-prompt.md` and `phase-1-draft-gemini-prompt.md` were not read (prompts, not findings — low synthesis value). |
| Internal Consistency | 0.20 | 0.97 | No contradictions between sections. Consensus points and divergence points are mutually exclusive. Implementation findings trace to consensus/divergence claims. |
| Methodological Rigor | 0.15 | 0.93 | Adversarial critique findings integrated. Inversion applied (PG-1 through PG-4 capture what the panel did NOT cover). Steelman applied (weakest recommendations strengthened in DP-3 and DP-4). |
| Evidence Quality | 0.20 | 0.95 | Every claim cites a specific source artifact and section. No unsupported assertions. Inferences (Panel Gaps) are labeled as inferences. |
| Actionability | 0.15 | 0.94 | Eight T-NNN findings provide spec-update language. Seven OQs are decision-framed. Divergence points include resolution recommendations. |
| Traceability | 0.10 | 0.96 | Document ID, workflow ID, phase ID, and source artifacts are all registered. All T-NNN findings extend the established series. |

**Weighted Composite:**

```
(0.90 × 0.20) + (0.97 × 0.20) + (0.93 × 0.15) + (0.95 × 0.20) + (0.94 × 0.15) + (0.96 × 0.10)
= 0.180 + 0.194 + 0.1395 + 0.190 + 0.141 + 0.096
= 0.9405
```

**Composite Score: 0.94**
**Threshold: 0.92**
**Verdict: PASS**

S-013 (Inversion) gap check: The synthesis does not specify a concrete implementation timeline or effort estimate — this is intentional (out of scope for a synthesis document). The synthesis does not resolve OQs — also intentional (they require human decisions). No unintentional gaps identified.

S-003 (Steelman) check: The weakest recommendation is DP-3 (process group management on Windows). It was strengthened by adding the specific Windows alternative (`CREATE_NEW_PROCESS_GROUP`) and requiring a platform detection check. The weakest consensus point is CP-7 (`CLAUDECODE=1` guard in pre-flight) — it is correct but the least technically elaborated. It was not strengthened further because both models agree and no critique challenged it; elaboration would pad without adding value.

---

## Disclaimer

This synthesis was generated by `orch-synthesizer` (claude-sonnet-4-6) based on 4 artifacts from workflow `consensus-panel-20260316-001` (2 drafts, 2 cross-critiques). The panel was a 2-of-3 partial panel — Claude was unavailable due to T-002. Human review is recommended before acting on any recommendation, particularly those in the Divergence Points and Panel Gaps sections. This document does not constitute official Jerry Framework specification; findings become spec candidates only after human review and acceptance.

*Artifacts synthesized:*
- `consensus/phase-1-draft-codex-draft.md`
- `consensus/phase-1-draft-gemini-draft.md`
- `consensus/phase-1-draft-codex-critique.md` (Codex critiquing Gemini)
- `consensus/phase-1-draft-gemini-critique.md` (Gemini critiquing Codex)
- `consensus/phase-1-draft-intent.md` (context reference)
