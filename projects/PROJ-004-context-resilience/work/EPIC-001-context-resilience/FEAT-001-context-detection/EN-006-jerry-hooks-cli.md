# EN-006: `jerry hooks` CLI Command Namespace

> **Type:** enabler
> **Status:** pending
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** infrastructure
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** --
> **Parent:** FEAT-001
> **Owner:** --
> **Effort:** 3-5h

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Technical scope |
| [CLI Commands](#cli-commands) | Command specification |
| [Acceptance Criteria](#acceptance-criteria) | BDD scenarios and checklist |
| [Dependencies](#dependencies) | Relationships |
| [History](#history) | Status changes |

---

## Summary

Register the `jerry hooks` subcommand group in the CLI adapter and parser. Create four command handlers that consolidate all hook event logic, dispatching to bounded context application services. This is the central integration item -- it makes the bounded context accessible to hook scripts via the CLI.

---

## CLI Commands

| Command | Handler | Services Used |
|---------|---------|---------------|
| `jerry hooks prompt-submit` | `HooksPromptSubmitHandler` | ContextFillEstimator, CheckpointService, PromptReinforcementEngine (existing) |
| `jerry hooks session-start` | `HooksSessionStartHandler` | RetrieveProjectContextQuery (existing), SessionQualityContextGenerator (existing), CheckpointService, ResumptionContextGenerator |
| `jerry hooks pre-compact` | `HooksPreCompactHandler` | CheckpointService, AbandonSessionCommand (existing) |
| `jerry hooks pre-tool-use` | `HooksPreToolUseHandler` | PreToolEnforcementEngine (existing), staleness detection (EN-005) |

**Stdin payload:** Each command reads Claude Code's hook payload JSON from stdin, extracts relevant fields (e.g., `env.TRANSCRIPT_PATH`, `tool_use.input`).

**Output:** All handlers return JSON to stdout matching Claude Code's hook response schema. `--json` flag follows existing CLI pattern.

**Error handling:** Each handler step wrapped in try/except. Step failures log to stderr and continue (fail-open). Handler always exits 0.

---

## Acceptance Criteria

### BDD Scenarios (pytest-bdd)

```gherkin
Feature: jerry hooks CLI command namespace

  Scenario: prompt-submit returns combined context
    Given a valid UserPromptSubmit JSON payload on stdin
    When I run "jerry --json hooks prompt-submit"
    Then the output should be valid JSON
    And it should contain "additionalContext" with context-monitor and quality reinforcement

  Scenario: session-start returns project + quality + resumption context
    Given a valid SessionStart JSON payload on stdin
    When I run "jerry --json hooks session-start"
    Then the output should contain project context
    And quality enforcement context
    And resumption context (if unacknowledged checkpoint exists)

  Scenario: pre-compact creates checkpoint and abandons session
    Given a valid PreCompact JSON payload on stdin
    And an active session exists
    When I run "jerry --json hooks pre-compact"
    Then a checkpoint file should be created in ".jerry/checkpoints/"
    And the active session should be abandoned with reason containing "compaction"

  Scenario: pre-tool-use returns enforcement decision
    Given a valid PreToolUse JSON payload on stdin
    When I run "jerry --json hooks pre-tool-use"
    Then the output should contain enforcement validation result

  Scenario: Handler step failure is fail-open
    Given ContextFillEstimator raises an exception
    When I run "jerry --json hooks prompt-submit"
    Then the command should exit 0
    And the output should contain valid JSON with quality reinforcement (other steps still run)
    And stderr should contain the error message

  Scenario: Commands registered in CLI parser
    When I run "jerry hooks --help"
    Then the output should list: prompt-submit, session-start, pre-compact, pre-tool-use

  Scenario: Handlers constructed via dependency injection
    Given bootstrap.py composition root
    When HooksPromptSubmitHandler is constructed
    Then it should receive ContextFillEstimator, CheckpointService, and PromptReinforcementEngine
    And no ad-hoc instantiation should occur
```

### Acceptance Checklist

- [ ] `jerry hooks prompt-submit` callable, accepts stdin JSON, returns stdout JSON
- [ ] `jerry hooks session-start` callable
- [ ] `jerry hooks pre-compact` callable
- [ ] `jerry hooks pre-tool-use` callable
- [ ] All 4 commands registered in CLI parser as subcommand group
- [ ] All 4 handlers constructed via DI in `bootstrap.py`
- [ ] Stdin payload read and parsed correctly
- [ ] `jerry --json hooks prompt-submit` returns valid Claude Code hook response JSON
- [ ] ContextFillEstimator, CheckpointService, ResumptionContextGenerator called correctly
- [ ] `jerry hooks pre-compact` triggers session abandon via command dispatcher
- [ ] Fail-open: step failures log stderr, continue, exit 0, return valid JSON
- [ ] H-08: CLI adapter does not import bounded context infrastructure directly
- [ ] Integration tests: end-to-end with sample stdin payloads
- [ ] One class per file for handlers (H-10)

---

## Dependencies

**Depends On:**
- EN-001 (session abandon command)
- EN-003 (CheckpointService, FilesystemCheckpointRepository)
- EN-004 (ContextFillEstimator, ResumptionContextGenerator)
- EN-005 (staleness detection logic)

**Enables:**
- EN-007 (wrapper scripts call these commands)
- ST-003 (system operational check)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Enabler created from CWI-10. Resolves QG-2 DEF-004. |
