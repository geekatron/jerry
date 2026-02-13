#!/usr/bin/env python3
"""
Subagent Stop Hook - Handoff Orchestration

This hook runs when a subagent completes its task, enabling automatic
handoff logic between agents (e.g., Code -> Review -> QA).

Reference: https://docs.anthropic.com/en/docs/claude-code/hooks

Exit Codes:
    0 - Success (handoff processed)
    1 - No handoff needed
    2 - Error in hook execution
"""

import json
import os
import sys
from datetime import datetime
from typing import Any

# =============================================================================
# CONFIGURATION
# =============================================================================

# Handoff rules: {from_agent: [(condition, to_agent, context)]}
HANDOFF_RULES = {
    "orchestrator": [
        # After orchestrator delegates implementation, route to QA
        ("implementation_complete", "qa-engineer", "Review and test the implementation"),
    ],
    "qa-engineer": [
        # After QA finds security concerns, route to security
        ("security_concern", "security-auditor", "Review security findings"),
        # After QA passes, route back to orchestrator
        ("tests_passing", "orchestrator", "All tests passing, ready for synthesis"),
    ],
    "security-auditor": [
        # After security review, route back to orchestrator
        ("review_complete", "orchestrator", "Security review complete"),
    ],
}

# Work item status transitions on handoff
STATUS_TRANSITIONS = {
    "implementation_complete": "IN_REVIEW",
    "tests_passing": "TESTING_COMPLETE",
    "security_concern": "SECURITY_REVIEW",
    "review_complete": "READY_FOR_MERGE",
}


# =============================================================================
# HOOK LOGIC
# =============================================================================


def parse_agent_output(output: str) -> dict[str, Any]:
    """
    Parse the agent's output to determine handoff signals.

    Agents should include structured signals in their output:
    - ##HANDOFF:condition## - Triggers handoff rule
    - ##WORKITEM:WORK-xxx## - Links to work item
    - ##STATUS:status## - Updates work item status
    """
    signals: dict[str, Any] = {
        "handoff_condition": None,
        "work_items": [],
        "status_update": None,
        "summary": "",
    }

    lines = output.splitlines()
    summary_lines = []

    for line in lines:
        if "##HANDOFF:" in line:
            # Extract handoff condition
            start = line.index("##HANDOFF:") + 10
            end = line.index("##", start)
            signals["handoff_condition"] = line[start:end]

        elif "##WORKITEM:" in line:
            # Extract work item reference
            start = line.index("##WORKITEM:") + 11
            end = line.index("##", start)
            signals["work_items"].append(line[start:end])

        elif "##STATUS:" in line:
            # Extract status update
            start = line.index("##STATUS:") + 9
            end = line.index("##", start)
            signals["status_update"] = line[start:end]

        else:
            # Collect non-signal lines as summary
            summary_lines.append(line)

    signals["summary"] = "\n".join(summary_lines).strip()
    return signals


def determine_handoff(from_agent: str, signals: dict[str, Any]) -> tuple[str | None, str | None]:
    """Determine if a handoff should occur based on agent and signals."""
    condition = signals.get("handoff_condition")

    if not condition:
        return None, None

    rules = HANDOFF_RULES.get(from_agent, [])
    for rule_condition, to_agent, context in rules:
        if rule_condition == condition:
            return to_agent, context

    return None, None


def log_handoff(from_agent: str, to_agent: str, signals: dict[str, Any], context: str) -> None:
    """Log the handoff for audit trail."""
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "docs", "experience")
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"handoff_{timestamp}.md")

    log_content = f"""# Agent Handoff Log

**Timestamp**: {datetime.now().isoformat()}
**From**: {from_agent}
**To**: {to_agent}
**Condition**: {signals.get("handoff_condition", "N/A")}

## Context
{context}

## Work Items
{", ".join(signals.get("work_items", [])) or "None referenced"}

## Summary from {from_agent}
{signals.get("summary", "No summary provided")}
"""

    try:
        with open(log_file, "w") as f:
            f.write(log_content)
    except OSError:
        # Non-fatal: log to stderr instead
        print(f"Warning: Could not write handoff log to {log_file}", file=sys.stderr)


def main() -> int:
    """Main hook entry point."""
    try:
        # Read hook input from stdin
        input_data = json.loads(sys.stdin.read())

        agent_name = input_data.get("agent_name", "unknown")
        agent_output = input_data.get("output", "")
        # session_id available in input_data if needed for future logging

        # Parse the agent's output for signals
        signals = parse_agent_output(agent_output)

        # Determine if handoff is needed
        to_agent, context = determine_handoff(agent_name, signals)

        if to_agent:
            # Log the handoff
            log_handoff(agent_name, to_agent, signals, context)

            # Output handoff instruction
            print(
                json.dumps(
                    {
                        "action": "handoff",
                        "to_agent": to_agent,
                        "context": context,
                        "work_items": signals.get("work_items", []),
                        "summary": signals.get("summary", ""),
                        "status_transition": STATUS_TRANSITIONS.get(
                            signals.get("handoff_condition", ""), None
                        ),
                    }
                )
            )
            return 0

        # No handoff needed
        print(json.dumps({"action": "none", "reason": "No handoff condition matched"}))
        return 1

    except json.JSONDecodeError as e:
        print(json.dumps({"action": "error", "reason": f"Invalid JSON input - {e}"}))
        return 2
    except Exception as e:
        print(json.dumps({"action": "error", "reason": str(e)}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
