# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Phase 2 scorer for PROJ-036 FEAT-036-004: G-Eval Scoring with Score Transparency.

Scores Phase 1 agent outputs using DeepEvalAdapter with full scoring trace
capture for transparency and reproducibility.

Usage:
    uv run python scripts/baseline_scorer.py \
        --prompts-dir tests/prompt-regression/baselines/prompts \
        --output-dir projects/PROJ-036-prompt-regression-harness/orchestration/baseline-execution-20260308-001 \
        --agents ps-researcher,ps-architect

Environment variables:
    ANTHROPIC_API_KEY    Required. API key for Anthropic.
    JERRY_JUDGE_MODEL    Optional. Override judge model (default: claude-sonnet-4-20250514).
"""

from __future__ import annotations

import argparse
import json
import logging
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter
import re
import time
from datetime import UTC, datetime
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

# S-014 dimension weights from quality-enforcement.md
DIMENSION_WEIGHTS = {
    "completeness": 0.20,
    "internal_consistency": 0.20,
    "methodological_rigor": 0.20,
    "evidence_quality": 0.15,
    "actionability": 0.15,
    "traceability": 0.10,
}

# Quality floors per agent
QUALITY_FLOORS = {
    "ps-researcher": 0.82,
    "ps-architect": 0.88,
}

# Patterns that look like API keys or secrets to redact
_SECRET_PATTERNS = [
    re.compile(r"sk-ant-[a-zA-Z0-9_-]+"),
    re.compile(r"sk-[a-zA-Z0-9_-]{20,}"),
    re.compile(r"ANTHROPIC_API_KEY=[^\s]+"),
    re.compile(
        r"api[_-]?key[\"']?\s*[:=]\s*[\"']?[a-zA-Z0-9_-]{20,}[\"']?",
        re.IGNORECASE,
    ),
]


def _redact_secrets(text: str) -> str:
    """Redact API keys and secrets from text before persisting."""
    result = text
    for pattern in _SECRET_PATTERNS:
        result = pattern.sub("[REDACTED]", result)
    return result


def load_prompt_yaml(yaml_path: Path) -> dict:
    """Load and parse a prompt YAML file."""
    with open(yaml_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_criteria_from_yaml(g_eval_criteria: dict) -> list:
    """Build QualityCriterion objects from YAML g_eval_criteria section."""
    from jerry.testing.evaluation.criterion import QualityCriterion

    criteria = []
    for name, description in g_eval_criteria.items():
        weight = DIMENSION_WEIGHTS.get(name, 0.10)
        criteria.append(
            QualityCriterion(
                name=name,
                description=description.strip(),
                weight=weight,
                dimension=name,
            )
        )
    return criteria


def score_single_output(
    adapter: DeepEvalAdapter,
    agent_name: str,
    prompt_id: str,
    user_prompt: str,
    output_text: str,
    criteria: list,
    quality_floor: float,
) -> dict:
    """Score a single output using DeepEvalAdapter and capture scoring trace.

    Returns a dictionary with dimension scores, composite, and judge metadata.
    """
    from deepeval.test_case import LLMTestCase

    start_ms = time.monotonic_ns() // 1_000_000

    # Build metric for this agent
    metric = adapter.build_metric_for_agent(
        agent_name=agent_name,
        criteria=criteria,
        quality_floor=quality_floor,
    )

    # Truncate for LLMTestCase (MC-02 pattern)
    truncated_output = output_text[:8000] if len(output_text) > 8000 else output_text
    truncated_prompt = user_prompt[:10000] if len(user_prompt) > 10000 else user_prompt

    test_case = LLMTestCase(
        input=truncated_prompt,
        actual_output=truncated_output,
    )

    # Get debiased criteria order for trace
    debiased_criteria = metric._jerry_metric.get_criteria_for_debiasing()
    criteria_order = [c.name for c in debiased_criteria]

    # Evaluate each criterion individually to capture per-dimension scores
    scoring_results = metric.evaluate_criteria(
        criteria=debiased_criteria,
        test_case=test_case,
    )

    # Build dimension scores dict
    dimension_scores = {}
    for result in scoring_results:
        dimension_scores[result.criterion_name] = result.score

    # Compute composite
    composite = metric._jerry_metric.score_composite(scoring_results)

    end_ms = time.monotonic_ns() // 1_000_000
    latency_ms = end_ms - start_ms

    return {
        "dimension_scores": dimension_scores,
        "composite_score": composite,
        "criteria_order": criteria_order,
        "debiasing_applied": True,
        "scoring_results": [
            {
                "criterion_name": r.criterion_name,
                "score": r.score,
                "weight": r.weight,
                "weighted_score": r.weighted_score,
                "evidence": r.evidence,
                "debiasing_applied": r.debiasing_applied,
            }
            for r in scoring_results
        ],
        "latency_ms": latency_ms,
    }


def run_phase2_scoring(
    agents: list[str],
    prompt_data: dict[str, dict],
    output_dir: Path,
    judge_model: str,
) -> dict:
    """Execute Phase 2 scoring for all agents and persist traces."""
    from jerry.testing.evaluation.debiasing import DebiasingStrategy
    from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter

    adapter = DeepEvalAdapter(
        model_name=judge_model,
        debiasing_strategy=DebiasingStrategy(),
    )

    all_agent_results = {}
    total_scoring_calls = 0

    for agent_name in agents:
        agent_data = prompt_data[agent_name]
        g_eval_criteria = agent_data.get("g_eval_criteria", {})
        criteria = build_criteria_from_yaml(g_eval_criteria)
        quality_floor = QUALITY_FLOORS.get(agent_name, 0.82)
        prompts = agent_data["prompts"]

        agent_composites = []
        agent_dimensions: dict[str, list[float]] = {}

        for prompt_entry in prompts:
            prompt_id = prompt_entry["id"]
            user_prompt = prompt_entry["user_prompt"]

            # Load Phase 1 output
            output_path = output_dir / "outputs" / agent_name / prompt_id / "output.md"
            if not output_path.exists():
                logger.error("Phase 1 output missing: %s", output_path)
                continue
            output_text = output_path.read_text(encoding="utf-8")

            logger.info("Scoring %s / %s ...", agent_name, prompt_id)

            # Score
            result = score_single_output(
                adapter=adapter,
                agent_name=agent_name,
                prompt_id=prompt_id,
                user_prompt=user_prompt,
                output_text=output_text,
                criteria=criteria,
                quality_floor=quality_floor,
            )
            total_scoring_calls += len(criteria)

            # Persist scoring trace
            trace = {
                "agent": agent_name,
                "prompt_id": prompt_id,
                "judge_model": judge_model,
                "timestamp": datetime.now(UTC).isoformat(),
                "dimension_scores": result["dimension_scores"],
                "composite_score": result["composite_score"],
                "debiasing_applied": result["debiasing_applied"],
                "criteria_order": result["criteria_order"],
                "scoring_results": result["scoring_results"],
                "latency_ms": result["latency_ms"],
            }

            # Redact any secrets from evidence text
            trace_text = json.dumps(trace, indent=2, ensure_ascii=False)
            trace_text = _redact_secrets(trace_text)

            trace_dir = output_dir / "scoring-traces" / agent_name / prompt_id
            trace_dir.mkdir(parents=True, exist_ok=True)
            trace_path = trace_dir / "scoring-trace.json"
            trace_path.write_text(trace_text, encoding="utf-8")

            logger.info(
                "  Composite: %.3f | Dims: %s | Trace: %s",
                result["composite_score"],
                {k: f"{v:.2f}" for k, v in result["dimension_scores"].items()},
                trace_path,
            )

            agent_composites.append(result["composite_score"])
            for dim_name, dim_score in result["dimension_scores"].items():
                agent_dimensions.setdefault(dim_name, []).append(dim_score)

        mean_composite = sum(agent_composites) / len(agent_composites) if agent_composites else 0.0

        all_agent_results[agent_name] = {
            "prompts": {
                prompt_entry["id"]: {
                    "composite": agent_composites[i] if i < len(agent_composites) else 0.0,
                }
                for i, prompt_entry in enumerate(prompts)
            },
            "mean_composite": round(mean_composite, 4),
            "quality_floor": quality_floor,
            "floor_met": mean_composite >= quality_floor,
            "prompt_count": len(prompts),
        }

        logger.info(
            "%s: mean_composite=%.4f, quality_floor=%.2f, floor_met=%s",
            agent_name,
            mean_composite,
            quality_floor,
            mean_composite >= quality_floor,
        )

    return {
        "agents": all_agent_results,
        "judge_model": judge_model,
        "total_scoring_calls": total_scoring_calls,
        "timestamp": datetime.now(UTC).isoformat(),
    }


def verify_phase2(output_dir: Path, agents: list[str], prompt_data: dict[str, dict]) -> list[str]:
    """Verify Phase 2 outputs meet acceptance criteria."""
    failures = []

    for agent_name in agents:
        prompts = prompt_data[agent_name]["prompts"]
        for prompt_entry in prompts:
            prompt_id = prompt_entry["id"]
            trace_path = (
                output_dir / "scoring-traces" / agent_name / prompt_id / "scoring-trace.json"
            )
            if not trace_path.exists():
                failures.append(f"MISSING scoring trace: {trace_path}")
            else:
                trace = json.loads(trace_path.read_text(encoding="utf-8"))
                required_fields = [
                    "agent",
                    "prompt_id",
                    "judge_model",
                    "timestamp",
                    "dimension_scores",
                    "composite_score",
                    "debiasing_applied",
                    "criteria_order",
                ]
                for f in required_fields:
                    if f not in trace:
                        failures.append(f"MISSING field '{f}' in {trace_path}")
                if trace.get("debiasing_applied") is not True:
                    failures.append(f"DEBIASING not applied in {trace_path}")

                # Check no credentials leaked
                trace_text = json.dumps(trace)
                for pattern in _SECRET_PATTERNS:
                    if pattern.search(trace_text):
                        failures.append(f"CREDENTIAL LEAK in {trace_path}")
                        break

    # Check composites file
    composites_path = output_dir / "phase2-composites.json"
    if not composites_path.exists():
        failures.append(f"MISSING composites file: {composites_path}")

    return failures


def main() -> int:
    """CLI entry point for the Phase 2 scorer."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    parser = argparse.ArgumentParser(
        description="Score Phase 1 outputs with G-Eval for PROJ-036 Phase 2.",
    )
    parser.add_argument(
        "--prompts-dir", required=True, help="Directory containing agent prompt YAML files."
    )
    parser.add_argument(
        "--output-dir", required=True, help="Root output directory (same as Phase 1)."
    )
    parser.add_argument("--agents", required=True, help="Comma-separated list of agent names.")
    parser.add_argument("--judge-model", default=None, help="LLM model for G-Eval judge.")
    parser.add_argument(
        "--verify-only", action="store_true", help="Only verify existing scoring outputs."
    )

    args = parser.parse_args()

    repo_root = Path(__file__).parents[1]
    prompts_dir = Path(args.prompts_dir)
    if not prompts_dir.is_absolute():
        prompts_dir = repo_root / prompts_dir
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = repo_root / output_dir

    agents = [a.strip() for a in args.agents.split(",")]
    judge_model = args.judge_model or os.environ.get(
        "JERRY_JUDGE_MODEL", "claude-sonnet-4-20250514"
    )

    # Load prompt YAML files
    prompt_data: dict[str, dict] = {}
    for agent_name in agents:
        yaml_path = prompts_dir / f"{agent_name}-prompts.yaml"
        if not yaml_path.exists():
            logger.error("Prompt file not found: %s", yaml_path)
            return 1
        prompt_data[agent_name] = load_prompt_yaml(yaml_path)
        logger.info("Loaded %d prompts for %s", len(prompt_data[agent_name]["prompts"]), agent_name)

    # Verify-only mode
    if args.verify_only:
        failures = verify_phase2(output_dir, agents, prompt_data)
        if failures:
            logger.error("Verification FAILED with %d issue(s):", len(failures))
            for f in failures:
                logger.error("  - %s", f)
            return 1
        logger.info("Phase 2 verification PASSED.")
        return 0

    # Check API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("ANTHROPIC_API_KEY environment variable is required.")
        return 1

    # Execute scoring
    results = run_phase2_scoring(
        agents=agents,
        prompt_data=prompt_data,
        output_dir=output_dir,
        judge_model=judge_model,
    )

    # Persist composites
    composites_path = output_dir / "phase2-composites.json"
    composites_path.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    logger.info("Composites: %s", composites_path)

    # Run verification
    failures = verify_phase2(output_dir, agents, prompt_data)

    # Log summary
    for agent_name, agent_result in results["agents"].items():
        logger.info(
            "%s: mean_composite=%.4f, floor=%.2f, met=%s",
            agent_name,
            agent_result["mean_composite"],
            agent_result["quality_floor"],
            agent_result["floor_met"],
        )

    # Estimate cost (Sonnet: $3/MTok input, $15/MTok output)
    # Each scoring call is ~2K input + ~500 output tokens on average
    est_calls = results["total_scoring_calls"]
    est_cost = est_calls * (2000 * 3 / 1_000_000 + 500 * 15 / 1_000_000)
    logger.info("Scoring calls: %d, estimated cost: $%.2f", est_calls, est_cost)

    if failures:
        logger.error("Verification FAILED with %d issue(s):", len(failures))
        for f in failures:
            logger.error("  - %s", f)
        return 1

    logger.info("Phase 2 COMPLETE. All scoring traces verified.")
    return 0


if __name__ == "__main__":
    import sys  # noqa: PLC0415

    sys.exit(main())
