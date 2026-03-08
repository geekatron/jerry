# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau
"""Phase 2: Layer 2 G-Eval scoring using DeepEvalAdapter.

Scores each agent's output against its criteria set using the PROJ-036
DeepEvalAdapter with mandatory C-007 debiasing (position randomization,
rubric shuffling).

Usage:
    uv run python projects/PROJ-036-prompt-regression-harness/work/test-harness/validation-run/phase2_score.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Project root for imports
PROJECT_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(PROJECT_ROOT))
load_dotenv(PROJECT_ROOT / ".env")

# Must set OPENAI_API_KEY for DeepEval's GEval (it uses OpenAI-compatible API)
# DeepEval uses litellm under the hood, which routes "claude-*" models via Anthropic
# but needs ANTHROPIC_API_KEY set
api_key = os.environ.get("ANTHROPIC_API_KEY", "")
if not api_key:
    print("ERROR: ANTHROPIC_API_KEY not found in .env")
    sys.exit(1)

from deepeval.test_case import LLMTestCase  # noqa: E402

from jerry.testing.evaluation.criteria.adv_scorer import ADV_SCORER_CRITERIA  # noqa: E402
from jerry.testing.evaluation.criteria.ps_analyst import PS_ANALYST_CRITERIA  # noqa: E402
from jerry.testing.evaluation.criteria.ps_architect import PS_ARCHITECT_CRITERIA  # noqa: E402
from jerry.testing.evaluation.criteria.ps_critic import PS_CRITIC_CRITERIA  # noqa: E402
from jerry.testing.evaluation.criteria.ps_researcher import PS_RESEARCHER_CRITERIA  # noqa: E402
from jerry.testing.evaluation.debiasing import DebiasingStrategy  # noqa: E402
from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter  # noqa: E402

MODEL = "claude-sonnet-4-20250514"
VALIDATION_DIR = Path(__file__).parent
PRICING_INPUT_PER_M = 3.0
PRICING_OUTPUT_PER_M = 15.0

AGENT_CONFIG = {
    "ps-researcher": {
        "criteria": PS_RESEARCHER_CRITERIA,
        "quality_floor": 0.82,
        "prompt": (
            "Research the trade-offs between property-based testing and "
            "metamorphic testing for LLM output evaluation. Output L0/L1/L2 sections."
        ),
    },
    "ps-analyst": {
        "criteria": PS_ANALYST_CRITERIA,
        "quality_floor": 0.85,
        "prompt": (
            "Analyze the failure modes of LLM-as-Judge scoring with "
            "leniency bias. Apply FMEA methodology."
        ),
    },
    "ps-architect": {
        "criteria": PS_ARCHITECT_CRITERIA,
        "quality_floor": 0.88,
        "prompt": (
            "Evaluate two options for test harness persistence: "
            "(A) JSON file store, (B) SQLite with WAL mode."
        ),
    },
    "ps-critic": {
        "criteria": PS_CRITIC_CRITERIA,
        "quality_floor": 0.83,
        "prompt": (
            "Critique the following deliverable for quality gaps. "
            "Apply S-014 LLM-as-Judge with 6-dimension rubric."
        ),
    },
    "adv-scorer": {
        "criteria": ADV_SCORER_CRITERIA,
        "quality_floor": 0.90,
        "prompt": (
            "Score the following deliverable against the S-014 quality gate. "
            "Return per-dimension scores, weighted composite, and verdict."
        ),
    },
}


def classify_composite(score: float) -> str:
    """Classify composite score per S-014 quality bands."""
    if score >= 0.92:
        return "PASS"
    if score >= 0.85:
        return "REVISE"
    return "REJECTED"


def write_layer2_report(
    agent_id: str,
    results: list,
    composite: float,
    quality_floor: float,
) -> None:
    """Write per-agent Layer 2 scoring report."""
    verdict = "PASS" if composite >= quality_floor else "FAIL"
    classification = classify_composite(composite)

    lines = [
        f"# Layer 2 G-Eval Scores: {agent_id}",
        "",
        f"> Model: {MODEL} | Quality Floor: {quality_floor} | "
        f"Debiasing: C-007 (criterion order shuffled) | "
        f"Engine: DeepEvalAdapter + JerryGEvalDeepEvalMetric",
        "",
        "## Document Sections",
        "",
        "| Section | Purpose |",
        "|---------|---------|",
        "| [Dimension Scores](#dimension-scores) | Per-criterion scores |",
        "| [Verdict](#verdict) | Pass/fail determination |",
        "| [Evidence](#evidence) | Per-dimension rationale |",
        "",
        "---",
        "",
        "## Dimension Scores",
        "",
        "| Dimension | Weight | Raw Score | Weighted | Floor |",
        "|-----------|--------|-----------|----------|-------|",
    ]

    for r in sorted(results, key=lambda x: x.criterion_name):
        weighted = r.score * r.weight
        lines.append(
            f"| {r.criterion_name} | {r.weight:.2f} | {r.score:.3f} | {weighted:.4f} | -- |"
        )

    lines.extend(
        [
            f"| **Composite** | | | **{composite:.4f}** | **{quality_floor}** |",
            f"| **Verdict** | | | **{verdict}** | |",
            f"| **Classification** | | | **{classification}** | |",
            "",
            "---",
            "",
            "## Verdict",
            "",
            f"- Composite Score: **{composite:.4f}**",
            f"- Quality Floor: **{quality_floor}**",
            f"- Verdict: **{verdict}**",
            f"- S-014 Classification: **{classification}**",
            "",
            "---",
            "",
            "## Evidence",
            "",
        ]
    )

    for r in sorted(results, key=lambda x: x.criterion_name):
        lines.append(f"### {r.criterion_name} ({r.score:.3f})")
        lines.append("")
        lines.append(r.evidence if hasattr(r, "evidence") else "No evidence captured.")
        lines.append("")

    report_path = VALIDATION_DIR / f"layer2-scores-{agent_id}.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Report written: {report_path.name}")


def main() -> None:
    """Run Phase 2 Layer 2 scoring for all 5 agents."""
    # Create adapter with C-007 mandatory debiasing
    debiasing = DebiasingStrategy()  # Non-deterministic for production
    adapter = DeepEvalAdapter(
        model_name=MODEL,
        debiasing_strategy=debiasing,
    )

    all_composites: dict[str, float] = {}
    all_results: dict[str, list] = {}

    print("=" * 60)
    print("Phase 2: Layer 2 G-Eval Scoring (DeepEvalAdapter)")
    print(f"Model: {MODEL}")
    print("=" * 60)

    for agent_id, config in AGENT_CONFIG.items():
        output_path = VALIDATION_DIR / f"{agent_id}-output.md"
        if not output_path.exists():
            print(f"\n  SKIP {agent_id}: {output_path.name} not found")
            all_composites[agent_id] = 0.0
            all_results[agent_id] = []
            continue

        print(f"\n--- Scoring {agent_id} (floor={config['quality_floor']}) ---")

        agent_output = output_path.read_text(encoding="utf-8")
        agent_prompt = config["prompt"]

        # Build the metric using DeepEvalAdapter
        metric = adapter.build_metric_for_agent(
            agent_name=agent_id,
            criteria=config["criteria"],
            quality_floor=config["quality_floor"],
        )

        # Create LLMTestCase
        test_case = LLMTestCase(
            input=agent_prompt,
            actual_output=agent_output,
        )

        # Run measurement (applies debiasing internally)
        print("  Measuring via DeepEvalAdapter...", flush=True)
        composite = metric.measure(test_case)

        # Get per-criterion results from the internal metric
        jerry_metric = metric._jerry_metric
        debiased_criteria = jerry_metric.get_criteria_for_debiasing()
        scoring_results = metric.evaluate_criteria(
            criteria=debiased_criteria,
            test_case=test_case,
        )

        all_composites[agent_id] = composite
        all_results[agent_id] = scoring_results

        # Write report
        write_layer2_report(agent_id, scoring_results, composite, config["quality_floor"])

        verdict = "PASS" if composite >= config["quality_floor"] else "FAIL"
        print(f"  Composite: {composite:.4f} | Floor: {config['quality_floor']} | {verdict}")

    # Summary
    print("\n" + "=" * 60)
    print("Phase 2 Summary")
    print("=" * 60)

    for agent_id in AGENT_CONFIG:
        floor = AGENT_CONFIG[agent_id]["quality_floor"]
        comp = all_composites.get(agent_id, 0.0)
        verdict = "PASS" if comp >= floor else "FAIL"
        n_results = len(all_results.get(agent_id, []))
        print(f"  {agent_id}: composite={comp:.4f} floor={floor} {verdict} dims={n_results}")

    # Write composites as JSON for Phase 4
    composites_path = VALIDATION_DIR / "phase2-composites.json"
    composites_path.write_text(
        json.dumps(
            {
                aid: {
                    "composite": round(c, 4),
                    "floor": AGENT_CONFIG[aid]["quality_floor"],
                    "verdict": "PASS" if c >= AGENT_CONFIG[aid]["quality_floor"] else "FAIL",
                    "per_dimension": {
                        r.criterion_name: round(r.score, 4) for r in all_results.get(aid, [])
                    },
                }
                for aid, c in all_composites.items()
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\n  Composites JSON written: {composites_path.name}")


if __name__ == "__main__":
    main()
