# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Baseline runner for PROJ-036 FEAT-036-004: Agent Output Generation with I/O Capture.

Executes canonical test prompts against real agent system prompts via the
Anthropic API, capturing full I/O traces for transparency and reproducibility.

Phase 1 of the baseline-execution-20260308-001 orchestration pipeline.

Usage:
    uv run python scripts/baseline_runner.py \
        --prompts-dir tests/prompt-regression/baselines/prompts \
        --output-dir projects/PROJ-036-prompt-regression-harness/orchestration/baseline-execution-20260308-001 \
        --agents ps-researcher,ps-architect

Environment variables:
    ANTHROPIC_API_KEY    Required. API key for Anthropic.
    JERRY_AGENT_MODEL    Optional. Override agent model (default: claude-opus-4-20250514).
"""

from __future__ import annotations

import argparse
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import anthropic
import logging
import os
import re
import time
from datetime import UTC, datetime
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

# Default model for agent execution
DEFAULT_AGENT_MODEL = "claude-opus-4-20250514"

# Patterns that look like API keys or secrets to redact
_SECRET_PATTERNS = [
    re.compile(r"sk-ant-[a-zA-Z0-9_-]+"),
    re.compile(r"sk-[a-zA-Z0-9_-]{20,}"),
    re.compile(r"ANTHROPIC_API_KEY=[^\s]+"),
    re.compile(r"api[_-]?key[\"']?\s*[:=]\s*[\"']?[a-zA-Z0-9_-]{20,}[\"']?", re.IGNORECASE),
]


def _redact_secrets(text: str) -> str:
    """Redact API keys and secrets from text before persisting."""
    result = text
    for pattern in _SECRET_PATTERNS:
        result = pattern.sub("[REDACTED]", result)
    return result


def _sanitize_text(text: str, field_name: str, max_chars: int = 100_000) -> str:
    """Sanitize text input (MC-02 pattern from deepeval_adapter.py)."""
    if not isinstance(text, str):
        raise TypeError(f"Expected str for {field_name}, got {type(text).__name__}")
    sanitized = text.replace("\x00", "").replace("\r\n", "\n").replace("\r", "\n")
    if len(sanitized) > max_chars:
        logger.warning("%s truncated from %d to %d chars.", field_name, len(sanitized), max_chars)
        sanitized = sanitized[:max_chars]
    return sanitized


def load_prompt_yaml(yaml_path: Path) -> dict:
    """Load and parse a prompt YAML file."""
    with open(yaml_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_system_prompt(system_prompt_path: str, repo_root: Path) -> str:
    """Load the agent system prompt from its definition file."""
    full_path = repo_root / system_prompt_path
    if not full_path.exists():
        raise FileNotFoundError(f"Agent definition not found: {full_path}")
    return full_path.read_text(encoding="utf-8")


def execute_prompt(
    client: anthropic.Anthropic,
    model: str,
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 8192,
) -> dict:
    """Execute a single prompt against the Anthropic API with I/O capture.

    Returns a dictionary with response text, token usage, and latency.
    """
    start_ms = time.monotonic_ns() // 1_000_000

    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    end_ms = time.monotonic_ns() // 1_000_000
    latency_ms = end_ms - start_ms

    # Extract response text from content blocks
    response_text = ""
    for block in message.content:
        if block.type == "text":
            response_text += block.text

    return {
        "raw_response": response_text,
        "token_usage": {
            "input_tokens": message.usage.input_tokens,
            "output_tokens": message.usage.output_tokens,
        },
        "latency_ms": latency_ms,
        "stop_reason": message.stop_reason,
    }


def run_agent_prompts(
    agent_name: str,
    prompt_data: dict,
    repo_root: Path,
    output_dir: Path,
    model: str,
    client: anthropic.Anthropic,
) -> dict:
    """Execute all prompts for a single agent and persist I/O traces.

    Returns a summary dict with per-prompt results.
    """
    system_prompt_path = prompt_data["system_prompt_path"]
    system_prompt = load_system_prompt(system_prompt_path, repo_root)
    prompts = prompt_data["prompts"]

    results = {}
    total_input_tokens = 0
    total_output_tokens = 0

    for prompt_entry in prompts:
        prompt_id = prompt_entry["id"]
        user_prompt = prompt_entry["user_prompt"]

        logger.info("Executing %s / %s ...", agent_name, prompt_id)

        # Sanitize inputs
        sanitized_user_prompt = _sanitize_text(user_prompt, f"{prompt_id}.user_prompt")

        # Execute
        result = execute_prompt(
            client=client,
            model=model,
            system_prompt=system_prompt,
            user_prompt=sanitized_user_prompt,
        )

        total_input_tokens += result["token_usage"]["input_tokens"]
        total_output_tokens += result["token_usage"]["output_tokens"]

        # Build I/O trace
        io_trace = {
            "agent": agent_name,
            "prompt_id": prompt_id,
            "run_number": 1,
            "timestamp": datetime.now(UTC).isoformat(),
            "model": model,
            "system_prompt": _redact_secrets(system_prompt),
            "user_prompt": _redact_secrets(sanitized_user_prompt),
            "raw_response": _redact_secrets(result["raw_response"]),
            "token_usage": result["token_usage"],
            "latency_ms": result["latency_ms"],
        }

        # Persist I/O trace
        trace_dir = output_dir / "io-traces" / agent_name / prompt_id
        trace_dir.mkdir(parents=True, exist_ok=True)
        trace_path = trace_dir / "run-001-io.json"
        trace_path.write_text(
            json.dumps(io_trace, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        logger.info("  I/O trace: %s", trace_path)

        # Persist agent output as markdown
        output_md_dir = output_dir / "outputs" / agent_name / prompt_id
        output_md_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_md_dir / "output.md"
        output_path.write_text(result["raw_response"], encoding="utf-8")
        logger.info("  Output:    %s (%d chars)", output_path, len(result["raw_response"]))

        results[prompt_id] = {
            "output_chars": len(result["raw_response"]),
            "input_tokens": result["token_usage"]["input_tokens"],
            "output_tokens": result["token_usage"]["output_tokens"],
            "latency_ms": result["latency_ms"],
            "stop_reason": result["stop_reason"],
        }

    return {
        "agent": agent_name,
        "model": model,
        "prompt_count": len(prompts),
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "per_prompt": results,
    }


def verify_outputs(output_dir: Path, agents: list[str], prompt_data: dict[str, dict]) -> list[str]:
    """Verify Phase 1 outputs meet acceptance criteria.

    Returns a list of verification failures (empty = all pass).
    """
    failures = []

    for agent_name in agents:
        prompts = prompt_data[agent_name]["prompts"]
        for prompt_entry in prompts:
            prompt_id = prompt_entry["id"]

            # Check output file exists and has >500 chars
            output_path = output_dir / "outputs" / agent_name / prompt_id / "output.md"
            if not output_path.exists():
                failures.append(f"MISSING output: {output_path}")
            else:
                content = output_path.read_text(encoding="utf-8")
                if len(content) < 500:
                    failures.append(f"SHORT output ({len(content)} chars < 500): {output_path}")

            # Check I/O trace exists and has required fields
            trace_path = output_dir / "io-traces" / agent_name / prompt_id / "run-001-io.json"
            if not trace_path.exists():
                failures.append(f"MISSING trace: {trace_path}")
            else:
                trace = json.loads(trace_path.read_text(encoding="utf-8"))
                required_fields = [
                    "agent",
                    "prompt_id",
                    "run_number",
                    "timestamp",
                    "model",
                    "system_prompt",
                    "user_prompt",
                    "raw_response",
                    "token_usage",
                    "latency_ms",
                ]
                for field in required_fields:
                    if field not in trace:
                        failures.append(f"MISSING field '{field}' in {trace_path}")

                # Check no credentials leaked
                trace_text = json.dumps(trace)
                for pattern in _SECRET_PATTERNS:
                    if pattern.search(trace_text):
                        failures.append(f"CREDENTIAL LEAK in {trace_path}")
                        break

    return failures


def main() -> int:
    """CLI entry point for the baseline runner."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    parser = argparse.ArgumentParser(
        description="Execute baseline prompts with I/O capture for PROJ-036.",
    )
    parser.add_argument(
        "--prompts-dir",
        required=True,
        help="Directory containing agent prompt YAML files.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Root output directory for traces and outputs.",
    )
    parser.add_argument(
        "--agents",
        required=True,
        help="Comma-separated list of agent names to execute (e.g., ps-researcher,ps-architect).",
    )
    parser.add_argument(
        "--model",
        default=None,
        help=f"LLM model for agent execution (default: {DEFAULT_AGENT_MODEL}, env: JERRY_AGENT_MODEL).",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=8192,
        help="Maximum output tokens per API call (default: 8192).",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Only run verification on existing outputs (no API calls).",
    )

    args = parser.parse_args()

    # Resolve paths
    repo_root = Path(__file__).parents[1]
    prompts_dir = Path(args.prompts_dir)
    if not prompts_dir.is_absolute():
        prompts_dir = repo_root / prompts_dir
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = repo_root / output_dir

    agents = [a.strip() for a in args.agents.split(",")]
    model = args.model or os.environ.get("JERRY_AGENT_MODEL", DEFAULT_AGENT_MODEL)

    # Load all prompt YAML files
    prompt_data: dict[str, dict] = {}
    for agent_name in agents:
        yaml_path = prompts_dir / f"{agent_name}-prompts.yaml"
        if not yaml_path.exists():
            logger.error("Prompt file not found: %s", yaml_path)
            return 1
        prompt_data[agent_name] = load_prompt_yaml(yaml_path)
        logger.info(
            "Loaded %d prompts for %s from %s",
            len(prompt_data[agent_name]["prompts"]),
            agent_name,
            yaml_path,
        )

    # Verify-only mode
    if args.verify_only:
        failures = verify_outputs(output_dir, agents, prompt_data)
        if failures:
            logger.error("Verification FAILED with %d issue(s):", len(failures))
            for f in failures:
                logger.error("  - %s", f)
            return 1
        logger.info("Verification PASSED: all outputs and traces valid.")
        return 0

    # Check API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("ANTHROPIC_API_KEY environment variable is required.")
        return 1

    # Import anthropic here to defer the import
    import anthropic  # noqa: PLC0415

    client = anthropic.Anthropic(api_key=api_key)

    # Execute prompts for each agent
    all_results = {}
    for agent_name in agents:
        logger.info("=" * 60)
        logger.info("Agent: %s (model: %s)", agent_name, model)
        logger.info("=" * 60)

        result = run_agent_prompts(
            agent_name=agent_name,
            prompt_data=prompt_data[agent_name],
            repo_root=repo_root,
            output_dir=output_dir,
            model=model,
            client=client,
        )
        all_results[agent_name] = result

        logger.info(
            "%s complete: %d prompts, %d input tokens, %d output tokens",
            agent_name,
            result["prompt_count"],
            result["total_input_tokens"],
            result["total_output_tokens"],
        )

    # Run verification
    failures = verify_outputs(output_dir, agents, prompt_data)

    # Persist execution summary
    summary = {
        "timestamp": datetime.now(UTC).isoformat(),
        "model": model,
        "agents": all_results,
        "verification": {
            "passed": len(failures) == 0,
            "failure_count": len(failures),
            "failures": failures,
        },
    }
    summary_path = output_dir / "phase1-execution-summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    logger.info("Execution summary: %s", summary_path)

    # Cost estimation
    total_input = sum(r["total_input_tokens"] for r in all_results.values())
    total_output = sum(r["total_output_tokens"] for r in all_results.values())
    # Opus pricing: $15/MTok input, $75/MTok output
    est_cost = (total_input * 15 / 1_000_000) + (total_output * 75 / 1_000_000)
    logger.info("Total tokens: %d input, %d output", total_input, total_output)
    logger.info("Estimated cost: $%.2f", est_cost)

    if failures:
        logger.error("Verification FAILED with %d issue(s):", len(failures))
        for f in failures:
            logger.error("  - %s", f)
        return 1

    logger.info(
        "Phase 1 COMPLETE. All %d outputs verified.",
        sum(r["prompt_count"] for r in all_results.values()),
    )
    return 0


if __name__ == "__main__":
    import sys  # noqa: PLC0415

    sys.exit(main())
