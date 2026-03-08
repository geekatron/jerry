# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau
"""Phase 3: Layer 3 Metamorphic Relation smoke tests using existing MR classes.

Uses ParaphraseConsistency (MR-001) and IrrelevantContextAppendation (MR-003)
from jerry.testing.metamorphic, with DeepEvalAdapter for scoring.

N=5 pairs per MR (SMOKE TEST -- not statistically powered per ADR-001 N>=20).

Usage:
    uv run python projects/PROJ-036-prompt-regression-harness/work/test-harness/validation-run/scripts/phase3_mr_smoke.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(PROJECT_ROOT))
load_dotenv(PROJECT_ROOT / ".env")

api_key = os.environ.get("ANTHROPIC_API_KEY", "")
if not api_key:
    print("ERROR: ANTHROPIC_API_KEY not found in .env")
    sys.exit(1)

import anthropic  # noqa: E402
from deepeval.test_case import LLMTestCase  # noqa: E402

from jerry.testing.evaluation.criteria.ps_architect import PS_ARCHITECT_CRITERIA  # noqa: E402
from jerry.testing.evaluation.criteria.ps_researcher import PS_RESEARCHER_CRITERIA  # noqa: E402
from jerry.testing.evaluation.debiasing import DebiasingStrategy  # noqa: E402
from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter  # noqa: E402
from jerry.testing.metamorphic.mr_001_paraphrase import ParaphraseConsistency  # noqa: E402
from jerry.testing.metamorphic.mr_003_context import IrrelevantContextAppendation  # noqa: E402

MODEL = "claude-sonnet-4-20250514"
VALIDATION_DIR = Path(__file__).resolve().parent.parent
N_VARIANTS = 5

AGENT_CONFIGS = {
    "ps-researcher": {
        "criteria": PS_RESEARCHER_CRITERIA,
        "quality_floor": 0.82,
        "prompt": (
            "Research the trade-offs between property-based testing and "
            "metamorphic testing for LLM output evaluation. Output L0/L1/L2 sections."
        ),
        "system": (
            "You are ps-researcher, a divergent-mode research agent. "
            "Produce research output with ## L0 (executive summary), "
            "## L1 (technical detail), and ## L2 (strategic implications) sections. "
            "Cite at least 3 sources."
        ),
    },
    "ps-architect": {
        "criteria": PS_ARCHITECT_CRITERIA,
        "quality_floor": 0.88,
        "prompt": (
            "Evaluate two options for test harness persistence: "
            "(A) JSON file store, (B) SQLite with WAL mode. Dimensions: write latency, "
            "corruption recovery, concurrent access, operational simplicity. "
            "Output in Nygard ADR format."
        ),
        "system": (
            "You are ps-architect, a convergent-mode architecture decision agent. "
            "Produce an ADR in Nygard format with Status, Context, Decision, "
            "Consequences sections. Include ## L0 and ## L2 sections. "
            "Include a navigation table."
        ),
    },
}


def score_output(
    adapter: DeepEvalAdapter,
    agent_id: str,
    criteria: list,
    quality_floor: float,
    prompt: str,
    output_text: str,
) -> float:
    """Score an output using DeepEvalAdapter and return composite."""
    metric = adapter.build_metric_for_agent(
        agent_name=agent_id,
        criteria=criteria,
        quality_floor=quality_floor,
    )
    test_case = LLMTestCase(input=prompt, actual_output=output_text)
    return metric.measure(test_case)


def generate_variant(
    client: anthropic.Anthropic,
    system_prompt: str,
    user_prompt: str,
) -> str:
    """Generate an agent output for a variant prompt via Anthropic SDK."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return response.content[0].text


def run_mr_for_agent(
    client: anthropic.Anthropic,
    adapter: DeepEvalAdapter,
    agent_id: str,
    config: dict,
    mr_id: str,
    mr_name: str,
    transformer,
) -> dict:
    """Run a single MR test for an agent."""
    original_path = VALIDATION_DIR / "agent-outputs" / f"{agent_id}.md"
    if not original_path.exists():
        return {"status": "SKIP", "agent_id": agent_id, "mr_id": mr_id}

    original_output = original_path.read_text(encoding="utf-8")
    original_prompt = config["prompt"]

    print(f"\n  {mr_id} ({mr_name}) for {agent_id}:")

    # Score original
    print("    Scoring original...", end=" ", flush=True)
    original_score = score_output(
        adapter,
        agent_id,
        config["criteria"],
        config["quality_floor"],
        original_prompt,
        original_output,
    )
    print(f"{original_score:.4f}")

    # Generate and score N variants
    variant_scores: list[float] = []
    for i in range(N_VARIANTS):
        variant_prompt = transformer.transform(original_prompt)
        print(f"    Variant {i + 1}/{N_VARIANTS}: generating...", end=" ", flush=True)
        variant_output = generate_variant(client, config["system"], variant_prompt)
        print("scoring...", end=" ", flush=True)
        v_score = score_output(
            adapter,
            agent_id,
            config["criteria"],
            config["quality_floor"],
            variant_prompt,
            variant_output,
        )
        variant_scores.append(v_score)
        print(f"{v_score:.4f}")

    mean_variant = sum(variant_scores) / len(variant_scores) if variant_scores else 0.0
    mean_delta = abs(original_score - mean_variant)
    tolerance = getattr(transformer, "TOLERANCE", 0.05)
    passed = mean_delta <= tolerance

    result = {
        "mr_id": mr_id,
        "mr_name": mr_name,
        "agent_id": agent_id,
        "original_score": round(original_score, 4),
        "variant_scores": [round(s, 4) for s in variant_scores],
        "mean_variant": round(mean_variant, 4),
        "mean_delta": round(mean_delta, 4),
        "tolerance": tolerance,
        "passed": passed,
        "n_variants": N_VARIANTS,
        "note": "SMOKE TEST - not statistically powered (N=5, ADR-001 requires N>=20)",
    }

    status = "PASS" if passed else "FAIL"
    print(f"    Result: {status} | delta={mean_delta:.4f} tolerance={tolerance}")
    return result


def write_report(results: list[dict]) -> None:
    """Write the Layer 3 MR results report."""
    lines = [
        "# Layer 3: Metamorphic Relation Smoke Test Results",
        "",
        "> SMOKE TEST -- N=5 pairs per MR. NOT statistically powered.",
        "> ADR-001 requires N>=20 for valid Wilcoxon signed-rank tests.",
        "> These results demonstrate pipeline functionality only.",
        f"> Scoring engine: DeepEvalAdapter + JerryGEvalDeepEvalMetric ({MODEL})",
        "",
        "## Document Sections",
        "",
        "| Section | Purpose |",
        "|---------|---------|",
        "| [Summary Table](#summary-table) | Pass/fail per MR per agent |",
        "| [Detailed Results](#detailed-results) | Per-variant scores |",
        "",
        "---",
        "",
        "## Summary Table",
        "",
        "| Agent | MR | Tolerance | Original | Mean Variant | Delta | Status |",
        "|-------|-----|-----------|----------|-------------|-------|--------|",
    ]

    for r in results:
        if r.get("status") == "SKIP":
            lines.append(f"| {r['agent_id']} | {r['mr_id']} | -- | -- | -- | -- | SKIP |")
            continue
        status = "PASS" if r["passed"] else "FAIL"
        lines.append(
            f"| {r['agent_id']} | {r['mr_id']} | {r['tolerance']} | "
            f"{r['original_score']:.4f} | {r['mean_variant']:.4f} | "
            f"{r['mean_delta']:.4f} | **{status}** |"
        )

    lines.extend(["", "---", "", "## Detailed Results", ""])

    for r in results:
        if r.get("status") == "SKIP":
            continue
        lines.extend(
            [
                f"### {r['agent_id']} / {r['mr_id']} ({r['mr_name']})",
                "",
                f"- **Original Score:** {r['original_score']:.4f}",
                f"- **Variant Scores:** {r['variant_scores']}",
                f"- **Mean Variant:** {r['mean_variant']:.4f}",
                f"- **Mean Delta:** {r['mean_delta']:.4f}",
                f"- **Tolerance:** {r['tolerance']}",
                f"- **Status:** {'PASS' if r['passed'] else 'FAIL'}",
                f"- **Note:** {r['note']}",
                "",
            ]
        )

    report_path = VALIDATION_DIR / "layer3-metamorphic" / "mr-results.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport written: {report_path.name}")


def main() -> None:
    """Run Phase 3 MR smoke tests."""
    client = anthropic.Anthropic(api_key=api_key)
    adapter = DeepEvalAdapter(
        model_name=MODEL,
        debiasing_strategy=DebiasingStrategy(),
    )

    mr001 = ParaphraseConsistency()
    mr003 = IrrelevantContextAppendation(seed=42)

    print("=" * 60)
    print("Phase 3: Layer 3 MR Smoke Tests (DeepEvalAdapter)")
    print(f"Model: {MODEL} | N={N_VARIANTS} (smoke test)")
    print("=" * 60)

    results: list[dict] = []
    for agent_id in ["ps-researcher", "ps-architect"]:
        config = AGENT_CONFIGS[agent_id]
        results.append(
            run_mr_for_agent(
                client, adapter, agent_id, config, "MR-001", "Paraphrase Consistency", mr001
            )
        )
        results.append(
            run_mr_for_agent(
                client, adapter, agent_id, config, "MR-003", "Irrelevant Context Appendation", mr003
            )
        )

    write_report(results)

    # Write cost summary
    cost_path = VALIDATION_DIR / "layer3-metamorphic" / "costs.json"
    cost_path.write_text(
        json.dumps(
            {
                "phase": "phase3",
                "note": "Token tracking for Phase 3 is approximate - DeepEval GEval calls tracked internally",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
