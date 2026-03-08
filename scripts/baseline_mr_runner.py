# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Phase 3 MR testing for PROJ-036 FEAT-036-004.

Executes metamorphic relation tests (MR-001 Paraphrase, MR-003 Irrelevant Context)
at N>=20 per agent, with I/O trace capture and BaselineStore population.

Usage:
    uv run python scripts/baseline_mr_runner.py \
        --prompts-dir tests/prompt-regression/baselines/prompts \
        --output-dir projects/PROJ-036-prompt-regression-harness/orchestration/baseline-execution-20260308-001 \
        --agents ps-researcher,ps-architect

Environment variables:
    ANTHROPIC_API_KEY    Required. API key for Anthropic.
    JERRY_AGENT_MODEL    Optional. Override agent model (default: claude-sonnet-4-20250514).
    JERRY_JUDGE_MODEL    Optional. Override judge model (default: claude-sonnet-4-20250514).
"""

from __future__ import annotations

import argparse
import json
import logging
import math
import os
import re
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    import anthropic

    from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter

logger = logging.getLogger(__name__)

# Default models
DEFAULT_AGENT_MODEL = "claude-sonnet-4-20250514"
DEFAULT_JUDGE_MODEL = "claude-sonnet-4-20250514"

# Quality floors per agent
QUALITY_FLOORS = {
    "ps-researcher": 0.82,
    "ps-architect": 0.88,
}

# Patterns to redact
_SECRET_PATTERNS = [
    re.compile(r"sk-ant-[a-zA-Z0-9_-]+"),
    re.compile(r"sk-[a-zA-Z0-9_-]{20,}"),
    re.compile(r"ANTHROPIC_API_KEY=[^\s]+"),
    re.compile(
        r"api[_-]?key[\"']?\s*[:=]\s*[\"']?[a-zA-Z0-9_-]{20,}[\"']?",
        re.IGNORECASE,
    ),
]

# Single composite criterion for efficient MR scoring (1 API call instead of 6)
MR_SCORING_DESCRIPTION = (
    "Evaluate the overall quality of this LLM response on a scale from 0.0 to 1.0. "
    "Consider: (1) Completeness - does it address all aspects of the request with "
    "appropriate depth? (2) Correctness - is information accurate and internally "
    "consistent? (3) Actionability - does it provide specific, implementable guidance? "
    "(4) Evidence - are claims supported with reasoning or citations? "
    "(5) Structure - is it well-organized with clear sections? "
    "Score 1.0 for excellent quality across all dimensions. Score 0.0 for poor quality."
)


def _redact_secrets(text: str) -> str:
    """Redact API keys and secrets from text."""
    result = text
    for pattern in _SECRET_PATTERNS:
        result = pattern.sub("[REDACTED]", result)
    return result


def load_prompt_yaml(yaml_path: Path) -> dict:
    """Load and parse a prompt YAML file."""
    with open(yaml_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_system_prompt(system_prompt_path: str, repo_root: Path) -> str:
    """Load agent system prompt from definition file."""
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
    """Execute a single prompt against the Anthropic API."""
    start_ms = time.monotonic_ns() // 1_000_000

    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    end_ms = time.monotonic_ns() // 1_000_000

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
        "latency_ms": end_ms - start_ms,
        "stop_reason": message.stop_reason,
    }


def score_output_composite(
    adapter: DeepEvalAdapter,
    user_prompt: str,
    output_text: str,
) -> float:
    """Score a single output with a composite criterion (1 API call).

    Uses a single comprehensive criterion instead of 6 separate dimensions
    for cost efficiency in MR testing. Both original and variant outputs
    are scored with the same method, ensuring valid paired comparison.
    """
    from deepeval.test_case import LLMTestCase

    from jerry.testing.evaluation.criterion import QualityCriterion

    criterion = QualityCriterion(
        name="composite_quality",
        description=MR_SCORING_DESCRIPTION,
        weight=1.0,
        dimension="composite",
    )

    metric = adapter.build_metric_for_agent(
        agent_name="mr-scorer",
        criteria=[criterion],
        quality_floor=0.0,  # No floor for MR scoring
    )

    truncated_output = output_text[:8000] if len(output_text) > 8000 else output_text
    truncated_prompt = user_prompt[:10000] if len(user_prompt) > 10000 else user_prompt

    test_case = LLMTestCase(
        input=truncated_prompt,
        actual_output=truncated_output,
    )

    debiased = metric._jerry_metric.get_criteria_for_debiasing()
    results = metric.evaluate_criteria(criteria=debiased, test_case=test_case)

    return results[0].score if results else 0.0


def persist_io_trace(
    output_dir: Path,
    agent_name: str,
    prompt_id: str,
    mr_id: str,
    run_number: int,
    model: str,
    system_prompt: str,
    user_prompt: str,
    result: dict,
    variant_id: str | None = None,
) -> Path:
    """Persist I/O trace for an MR variant execution."""
    trace = {
        "agent": agent_name,
        "prompt_id": prompt_id,
        "mr_id": mr_id,
        "run_number": run_number,
        "variant_id": variant_id or f"run-{run_number:03d}",
        "timestamp": datetime.now(UTC).isoformat(),
        "model": model,
        "system_prompt": _redact_secrets(system_prompt),
        "user_prompt": _redact_secrets(user_prompt),
        "raw_response": _redact_secrets(result["raw_response"]),
        "token_usage": result["token_usage"],
        "latency_ms": result["latency_ms"],
    }

    if mr_id == "original":
        trace_dir = output_dir / "mr-traces" / agent_name / "originals" / prompt_id
    else:
        trace_dir = output_dir / "mr-traces" / agent_name / mr_id / prompt_id

    trace_dir.mkdir(parents=True, exist_ok=True)
    trace_path = trace_dir / f"run-{run_number:03d}-io.json"
    trace_path.write_text(
        json.dumps(trace, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return trace_path


def _check_existing_trace(
    output_dir: Path, agent_name: str, prompt_id: str, mr_id: str, run_number: int
) -> dict | None:
    """Check if a trace already exists and load its output for scoring."""
    if mr_id == "original":
        trace_dir = output_dir / "mr-traces" / agent_name / "originals" / prompt_id
    else:
        trace_dir = output_dir / "mr-traces" / agent_name / mr_id / prompt_id

    trace_path = trace_dir / f"run-{run_number:03d}-io.json"
    if trace_path.exists():
        trace = json.loads(trace_path.read_text(encoding="utf-8"))
        return trace
    return None


def run_phase3(
    agents: list[str],
    prompt_data: dict[str, dict],
    output_dir: Path,
    repo_root: Path,
    agent_model: str,
    judge_model: str,
    runs_per_prompt: int,
) -> dict:
    """Execute Phase 3 MR testing for all agents.

    Supports resume: skips runs that already have persisted I/O traces,
    re-scoring their outputs instead of re-executing API calls.
    """
    import anthropic  # noqa: PLC0415

    from jerry.testing.evaluation.debiasing import DebiasingStrategy
    from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter
    from jerry.testing.metamorphic.mr_001_paraphrase import ParaphraseConsistency
    from jerry.testing.metamorphic.mr_003_context import IrrelevantContextAppendation
    from jerry.testing.stats import InsufficientSamplesError

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable is required.")

    client = anthropic.Anthropic(api_key=api_key)
    adapter = DeepEvalAdapter(
        model_name=judge_model,
        debiasing_strategy=DebiasingStrategy(),
    )

    mr001 = ParaphraseConsistency()

    all_results = {}
    total_execution_calls = 0
    total_scoring_calls = 0
    total_input_tokens = 0
    total_output_tokens = 0
    resumed_count = 0

    for agent_name in agents:
        agent_data = prompt_data[agent_name]
        system_prompt = load_system_prompt(agent_data["system_prompt_path"], repo_root)
        prompts = agent_data["prompts"]
        num_prompts = len(prompts)

        # Calculate K: runs per prompt to reach N>=20
        k = max(runs_per_prompt, math.ceil(20 / num_prompts))
        n_total = num_prompts * k

        logger.info(
            "Agent %s: %d prompts × %d runs = %d paired observations",
            agent_name,
            num_prompts,
            k,
            n_total,
        )

        # Accumulate paired scores
        original_scores: list[float] = []
        mr001_scores: list[float] = []
        mr003_scores: list[float] = []

        # Per-prompt detail for reporting
        prompt_details: dict[str, dict] = {}

        for prompt_entry in prompts:
            prompt_id = prompt_entry["id"]
            user_prompt = prompt_entry["user_prompt"]

            # Generate MR-001 transform (deterministic, done once)
            mr001_text = mr001.transform(user_prompt)

            prompt_orig_scores: list[float] = []
            prompt_mr001_scores: list[float] = []
            prompt_mr003_scores: list[float] = []

            for run_idx in range(k):
                run_num = run_idx + 1
                seed = 42 + run_idx  # Sequential seeds for MR-003

                # --- Run original (or resume from trace) ---
                existing = _check_existing_trace(
                    output_dir,
                    agent_name,
                    prompt_id,
                    "original",
                    run_num,
                )
                if existing:
                    logger.info(
                        "  %s / %s / original / run %d RESUMED from trace",
                        agent_name,
                        prompt_id,
                        run_num,
                    )
                    orig_response = existing["raw_response"]
                    resumed_count += 1
                else:
                    logger.info(
                        "  %s / %s / original / run %d of %d",
                        agent_name,
                        prompt_id,
                        run_num,
                        k,
                    )
                    orig_result = execute_prompt(
                        client,
                        agent_model,
                        system_prompt,
                        user_prompt,
                    )
                    total_execution_calls += 1
                    total_input_tokens += orig_result["token_usage"]["input_tokens"]
                    total_output_tokens += orig_result["token_usage"]["output_tokens"]
                    persist_io_trace(
                        output_dir,
                        agent_name,
                        prompt_id,
                        "original",
                        run_num,
                        agent_model,
                        system_prompt,
                        user_prompt,
                        orig_result,
                    )
                    orig_response = orig_result["raw_response"]

                orig_score = score_output_composite(
                    adapter,
                    user_prompt,
                    orig_response,
                )
                total_scoring_calls += 1
                prompt_orig_scores.append(orig_score)

                # --- Run MR-001 variant (or resume) ---
                existing = _check_existing_trace(
                    output_dir,
                    agent_name,
                    prompt_id,
                    "mr-001",
                    run_num,
                )
                if existing:
                    logger.info(
                        "  %s / %s / MR-001 / run %d RESUMED from trace",
                        agent_name,
                        prompt_id,
                        run_num,
                    )
                    mr001_response = existing["raw_response"]
                    resumed_count += 1
                else:
                    logger.info(
                        "  %s / %s / MR-001 / run %d of %d",
                        agent_name,
                        prompt_id,
                        run_num,
                        k,
                    )
                    mr001_result = execute_prompt(
                        client,
                        agent_model,
                        system_prompt,
                        mr001_text,
                    )
                    total_execution_calls += 1
                    total_input_tokens += mr001_result["token_usage"]["input_tokens"]
                    total_output_tokens += mr001_result["token_usage"]["output_tokens"]
                    persist_io_trace(
                        output_dir,
                        agent_name,
                        prompt_id,
                        "mr-001",
                        run_num,
                        agent_model,
                        system_prompt,
                        mr001_text,
                        mr001_result,
                        variant_id=f"paraphrase-run-{run_num:03d}",
                    )
                    mr001_response = mr001_result["raw_response"]

                mr001_score = score_output_composite(
                    adapter,
                    mr001_text,
                    mr001_response,
                )
                total_scoring_calls += 1
                prompt_mr001_scores.append(mr001_score)

                # --- Run MR-003 variant (or resume) ---
                mr003 = IrrelevantContextAppendation(seed=seed)
                mr003_text = mr003.transform(user_prompt)

                existing = _check_existing_trace(
                    output_dir,
                    agent_name,
                    prompt_id,
                    "mr-003",
                    run_num,
                )
                if existing:
                    logger.info(
                        "  %s / %s / MR-003 / run %d RESUMED from trace (seed=%d)",
                        agent_name,
                        prompt_id,
                        run_num,
                        seed,
                    )
                    mr003_response = existing["raw_response"]
                    resumed_count += 1
                else:
                    logger.info(
                        "  %s / %s / MR-003 / run %d of %d (seed=%d)",
                        agent_name,
                        prompt_id,
                        run_num,
                        k,
                        seed,
                    )
                    mr003_result = execute_prompt(
                        client,
                        agent_model,
                        system_prompt,
                        mr003_text,
                    )
                    total_execution_calls += 1
                    total_input_tokens += mr003_result["token_usage"]["input_tokens"]
                    total_output_tokens += mr003_result["token_usage"]["output_tokens"]
                    persist_io_trace(
                        output_dir,
                        agent_name,
                        prompt_id,
                        "mr-003",
                        run_num,
                        agent_model,
                        system_prompt,
                        mr003_text,
                        mr003_result,
                        variant_id=f"context-seed{seed}-run-{run_num:03d}",
                    )
                    mr003_response = mr003_result["raw_response"]

                mr003_score = score_output_composite(
                    adapter,
                    mr003_text,
                    mr003_response,
                )
                total_scoring_calls += 1
                prompt_mr003_scores.append(mr003_score)

                logger.info(
                    "    Scores: orig=%.2f  mr001=%.2f  mr003=%.2f",
                    orig_score,
                    mr001_score,
                    mr003_score,
                )

            original_scores.extend(prompt_orig_scores)
            mr001_scores.extend(prompt_mr001_scores)
            mr003_scores.extend(prompt_mr003_scores)

            prompt_details[prompt_id] = {
                "original_scores": prompt_orig_scores,
                "mr001_scores": prompt_mr001_scores,
                "mr003_scores": prompt_mr003_scores,
            }

        # --- Evaluate MR-001 ---
        mr001_eval = None
        mr001_error = None
        try:
            mr001_eval = mr001.evaluate(original_scores, mr001_scores)
            logger.info(
                "%s MR-001: passed=%s, delta=%.4f, p=%.4f, N=%d",
                agent_name,
                mr001_eval.passed,
                mr001_eval.mean_delta,
                mr001_eval.p_value,
                len(original_scores),
            )
        except InsufficientSamplesError as e:
            mr001_error = str(e)
            logger.warning("%s MR-001: InsufficientSamplesError: %s", agent_name, e)
        except Exception as e:
            mr001_error = str(e)
            logger.warning("%s MR-001: Error: %s", agent_name, e)

        # --- Evaluate MR-003 ---
        mr003_ref = IrrelevantContextAppendation(seed=42)
        mr003_eval = None
        mr003_error = None
        try:
            mr003_eval = mr003_ref.evaluate(original_scores, mr003_scores)
            logger.info(
                "%s MR-003: passed=%s, delta=%.4f, p=%.4f, N=%d",
                agent_name,
                mr003_eval.passed,
                mr003_eval.mean_delta,
                mr003_eval.p_value,
                len(original_scores),
            )
        except InsufficientSamplesError as e:
            mr003_error = str(e)
            logger.warning("%s MR-003: InsufficientSamplesError: %s", agent_name, e)
        except Exception as e:
            mr003_error = str(e)
            logger.warning("%s MR-003: Error: %s", agent_name, e)

        # --- Build agent result ---
        n_scores = len(original_scores)

        def _mr_result_to_dict(mr_result, error_msg=None, n=n_scores):
            if error_msg:
                return {"error": error_msg, "n": n}
            if mr_result is None:
                return {"error": "No result", "n": n}
            return {
                "mr_id": mr_result.mr_id,
                "passed": mr_result.passed,
                "mean_original": round(mr_result.mean_original, 4),
                "mean_transformed": round(mr_result.mean_transformed, 4),
                "mean_delta": round(mr_result.mean_delta, 4),
                "tolerance": mr_result.tolerance,
                "p_value": round(mr_result.p_value, 6),
                "effect_size": round(mr_result.effect_size, 4),
                "severity": mr_result.severity.value,
                "n": n,
                "evidence": mr_result.evidence,
            }

        all_results[agent_name] = {
            "n_paired_observations": n_total,
            "runs_per_prompt": k,
            "agent_model": agent_model,
            "mr_001": _mr_result_to_dict(mr001_eval, mr001_error),
            "mr_003": _mr_result_to_dict(mr003_eval, mr003_error),
            "original_scores": [round(s, 4) for s in original_scores],
            "mr001_scores": [round(s, 4) for s in mr001_scores],
            "mr003_scores": [round(s, 4) for s in mr003_scores],
            "prompt_details": {
                pid: {
                    "original": [round(s, 4) for s in d["original_scores"]],
                    "mr001": [round(s, 4) for s in d["mr001_scores"]],
                    "mr003": [round(s, 4) for s in d["mr003_scores"]],
                }
                for pid, d in prompt_details.items()
            },
        }

    if resumed_count > 0:
        logger.info("Resumed %d runs from existing traces.", resumed_count)

    # --- Persist calibration data ---
    calibration_data = {
        "timestamp": datetime.now(UTC).isoformat(),
        "agent_model": agent_model,
        "judge_model": judge_model,
        "agents": all_results,
        "note": "CalibrationRunner.calibrate_tolerances() is a stub. "
        "This data is persisted for future calibration use.",
    }
    cal_path = output_dir / "mr-calibration-data.json"
    cal_path.write_text(
        json.dumps(calibration_data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    logger.info("Calibration data: %s", cal_path)

    # --- Attempt BaselineStore population ---
    baseline_results = _attempt_baseline_store(
        agents,
        all_results,
        output_dir,
        agent_model,
        judge_model,
    )

    return {
        "agents": all_results,
        "baseline_store": baseline_results,
        "agent_model": agent_model,
        "judge_model": judge_model,
        "total_execution_calls": total_execution_calls,
        "total_scoring_calls": total_scoring_calls,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "timestamp": datetime.now(UTC).isoformat(),
    }


def _attempt_baseline_store(
    agents: list[str],
    all_results: dict,
    output_dir: Path,
    agent_model: str,
    judge_model: str,
) -> dict:
    """Attempt to populate BaselineStore. Handle quality gate failures gracefully."""
    from jerry.testing.baselines.store import BaselineStore
    from jerry.testing.types import EvaluationMode

    repo_root = Path(__file__).parents[1]
    store_root = repo_root / "tests" / "prompt-regression" / "baselines" / "data"
    store = BaselineStore(store_root)

    # Get git hash for version key
    import subprocess

    try:
        git_hash = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=repo_root,
            text=True,
        ).strip()
    except Exception:
        git_hash = "unknown"

    results = {}
    for agent_name in agents:
        agent_data = all_results[agent_name]
        scores = agent_data["original_scores"]
        mean_score = sum(scores) / len(scores) if scores else 0.0

        version_key = f"{git_hash}:skills/problem-solving/agents/{agent_name}.md"

        try:
            store.store(
                version_key=version_key,
                agent_id=agent_name,
                metric_id="composite_score",
                scores=scores,
                evaluation_mode=EvaluationMode.FULL,
                model_version=agent_model,
            )
            results[agent_name] = {
                "stored": True,
                "n_scores": len(scores),
                "mean_score": round(mean_score, 4),
                "version_key": version_key,
            }
            logger.info(
                "%s BaselineStore: STORED %d scores, mean=%.4f",
                agent_name,
                len(scores),
                mean_score,
            )
        except ValueError as e:
            results[agent_name] = {
                "stored": False,
                "reason": str(e),
                "n_scores": len(scores),
                "mean_score": round(mean_score, 4),
                "note": "Quality gate (mean >= 0.92) not met. Scores reflect "
                "MR-testing composite scoring, not full 6-dimension scoring. "
                "BaselineStore population deferred until scoring calibration.",
            }
            logger.warning(
                "%s BaselineStore: BLOCKED by quality gate (mean=%.4f): %s",
                agent_name,
                mean_score,
                e,
            )
        except Exception as e:
            results[agent_name] = {
                "stored": False,
                "reason": str(e),
                "n_scores": len(scores),
                "mean_score": round(mean_score, 4),
            }
            logger.error("%s BaselineStore: ERROR: %s", agent_name, e)

    return results


def verify_phase3(
    output_dir: Path,
    agents: list[str],
    prompt_data: dict[str, dict],
    runs_per_prompt: int,
) -> list[str]:
    """Verify Phase 3 outputs."""
    failures = []

    for agent_name in agents:
        prompts = prompt_data[agent_name]["prompts"]
        num_prompts = len(prompts)
        k = max(runs_per_prompt, math.ceil(20 / num_prompts))

        for prompt_entry in prompts:
            prompt_id = prompt_entry["id"]

            # Check original traces
            for run_num in range(1, k + 1):
                trace_path = (
                    output_dir
                    / "mr-traces"
                    / agent_name
                    / "originals"
                    / prompt_id
                    / f"run-{run_num:03d}-io.json"
                )
                if not trace_path.exists():
                    failures.append(f"MISSING original trace: {trace_path}")

            # Check MR-001 traces
            for run_num in range(1, k + 1):
                trace_path = (
                    output_dir
                    / "mr-traces"
                    / agent_name
                    / "mr-001"
                    / prompt_id
                    / f"run-{run_num:03d}-io.json"
                )
                if not trace_path.exists():
                    failures.append(f"MISSING MR-001 trace: {trace_path}")

            # Check MR-003 traces
            for run_num in range(1, k + 1):
                trace_path = (
                    output_dir
                    / "mr-traces"
                    / agent_name
                    / "mr-003"
                    / prompt_id
                    / f"run-{run_num:03d}-io.json"
                )
                if not trace_path.exists():
                    failures.append(f"MISSING MR-003 trace: {trace_path}")

    # Check calibration data
    cal_path = output_dir / "mr-calibration-data.json"
    if not cal_path.exists():
        failures.append(f"MISSING calibration data: {cal_path}")

    # Check phase3 results
    results_path = output_dir / "phase3-mr-results.json"
    if not results_path.exists():
        failures.append(f"MISSING phase3 results: {results_path}")

    return failures


def main() -> int:
    """CLI entry point for Phase 3 MR runner."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    parser = argparse.ArgumentParser(
        description="Phase 3 MR testing for PROJ-036 baseline execution.",
    )
    parser.add_argument("--prompts-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--agents", required=True)
    parser.add_argument(
        "--agent-model",
        default=None,
        help=f"Model for variant execution (default: {DEFAULT_AGENT_MODEL}).",
    )
    parser.add_argument(
        "--judge-model",
        default=None,
        help=f"Model for G-Eval scoring (default: {DEFAULT_JUDGE_MODEL}).",
    )
    parser.add_argument(
        "--runs-per-prompt",
        type=int,
        default=4,
        help="Minimum runs per prompt (adjusted up to reach N>=20). Default: 4.",
    )
    parser.add_argument("--verify-only", action="store_true")

    args = parser.parse_args()

    repo_root = Path(__file__).parents[1]
    prompts_dir = Path(args.prompts_dir)
    if not prompts_dir.is_absolute():
        prompts_dir = repo_root / prompts_dir
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = repo_root / output_dir

    agents = [a.strip() for a in args.agents.split(",")]
    agent_model = args.agent_model or os.environ.get("JERRY_AGENT_MODEL", DEFAULT_AGENT_MODEL)
    judge_model = args.judge_model or os.environ.get("JERRY_JUDGE_MODEL", DEFAULT_JUDGE_MODEL)

    # Load prompt YAMLs
    prompt_data: dict[str, dict] = {}
    for agent_name in agents:
        yaml_path = prompts_dir / f"{agent_name}-prompts.yaml"
        if not yaml_path.exists():
            logger.error("Prompt file not found: %s", yaml_path)
            return 1
        prompt_data[agent_name] = load_prompt_yaml(yaml_path)
        logger.info(
            "Loaded %d prompts for %s",
            len(prompt_data[agent_name]["prompts"]),
            agent_name,
        )

    if args.verify_only:
        failures = verify_phase3(output_dir, agents, prompt_data, args.runs_per_prompt)
        if failures:
            logger.error("Verification FAILED with %d issue(s):", len(failures))
            for f in failures:
                logger.error("  - %s", f)
            return 1
        logger.info("Phase 3 verification PASSED.")
        return 0

    # Cost estimation before execution
    estimated_runs = 0
    for agent_name in agents:
        num_p = len(prompt_data[agent_name]["prompts"])
        k = max(args.runs_per_prompt, math.ceil(20 / num_p))
        estimated_runs += num_p * k * 3  # original + MR-001 + MR-003

    # Sonnet pricing: $3/MTok input, $15/MTok output
    est_exec_cost = estimated_runs * (5000 * 3 / 1_000_000 + 3000 * 15 / 1_000_000)
    est_score_cost = estimated_runs * (2000 * 3 / 1_000_000 + 500 * 15 / 1_000_000)
    est_total = est_exec_cost + est_score_cost

    logger.info(
        "Estimated: %d execution calls + %d scoring calls = ~$%.2f",
        estimated_runs,
        estimated_runs,
        est_total,
    )

    # Execute Phase 3
    results = run_phase3(
        agents=agents,
        prompt_data=prompt_data,
        output_dir=output_dir,
        repo_root=repo_root,
        agent_model=agent_model,
        judge_model=judge_model,
        runs_per_prompt=args.runs_per_prompt,
    )

    # Persist results
    results_path = output_dir / "phase3-mr-results.json"
    results_text = json.dumps(results, indent=2, ensure_ascii=False)
    results_text = _redact_secrets(results_text)
    results_path.write_text(results_text, encoding="utf-8")
    logger.info("Phase 3 results: %s", results_path)

    # Run verification
    failures = verify_phase3(output_dir, agents, prompt_data, args.runs_per_prompt)

    # Summary
    for agent_name, agent_data in results["agents"].items():
        mr001 = agent_data["mr_001"]
        mr003 = agent_data["mr_003"]
        logger.info(
            "%s: N=%d | MR-001: %s | MR-003: %s",
            agent_name,
            agent_data["n_paired_observations"],
            mr001.get("passed", mr001.get("error", "?")),
            mr003.get("passed", mr003.get("error", "?")),
        )

    # Cost
    est_cost = (
        results["total_input_tokens"] * 3 / 1_000_000
        + results["total_output_tokens"] * 15 / 1_000_000
        + results["total_scoring_calls"] * (2000 * 3 / 1_000_000 + 500 * 15 / 1_000_000)
    )
    logger.info(
        "Execution calls: %d, scoring calls: %d, estimated cost: $%.2f",
        results["total_execution_calls"],
        results["total_scoring_calls"],
        est_cost,
    )

    if failures:
        logger.error("Verification FAILED with %d issue(s):", len(failures))
        for f in failures:
            logger.error("  - %s", f)
        return 1

    logger.info("Phase 3 COMPLETE.")
    return 0


if __name__ == "__main__":
    import sys  # noqa: PLC0415

    sys.exit(main())
