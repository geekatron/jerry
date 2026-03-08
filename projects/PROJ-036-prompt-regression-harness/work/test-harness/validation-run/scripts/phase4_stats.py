# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau
"""Phase 4: Layer 4 Statistical Comparison smoke test.

Demonstrates Layer4Pipeline with synthetic baseline arrays vs Phase 2
candidate scores. N=20 per array (minimum for Wilcoxon signed-rank).

This is a SMOKE/VALIDATION test — synthetic baselines, not real historical
baselines. Purpose: verify the Layer4Pipeline wiring works end-to-end.

Usage:
    uv run python projects/PROJ-036-prompt-regression-harness/work/test-harness/validation-run/scripts/phase4_stats.py
"""

from __future__ import annotations

import json
import random
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(PROJECT_ROOT))

from jerry.testing.baselines.store import BaselineStore  # noqa: E402
from jerry.testing.layer4_stats import Layer4Pipeline  # noqa: E402
from jerry.testing.types import EvaluationMode  # noqa: E402

VALIDATION_DIR = Path(__file__).resolve().parent.parent
N_SAMPLES = 20  # Minimum for Wilcoxon signed-rank test
SEED = 42

AGENT_FLOORS = {
    "ps-researcher": 0.82,
    "ps-analyst": 0.85,
    "ps-architect": 0.88,
    "ps-critic": 0.83,
    "adv-scorer": 0.90,
}


def generate_synthetic_baseline(floor: float, n: int, rng: random.Random) -> list[float]:
    """Generate synthetic baseline scores clustered around floor + 0.05."""
    center = min(floor + 0.05, 0.95)
    return [max(0.0, min(1.0, rng.gauss(center, 0.03))) for _ in range(n)]


def generate_candidate_from_composite(composite: float, n: int, rng: random.Random) -> list[float]:
    """Generate candidate score array centered on Phase 2 composite with noise."""
    return [max(0.0, min(1.0, rng.gauss(composite, 0.02))) for _ in range(n)]


def main() -> None:
    """Run Phase 4 Layer 4 statistical comparison."""
    # Load Phase 2 composites
    composites_path = VALIDATION_DIR / "layer2-geval" / "composites.json"
    if not composites_path.exists():
        print("ERROR: phase2-composites.json not found. Run Phase 2 first.")
        sys.exit(1)

    composites = json.loads(composites_path.read_text(encoding="utf-8"))

    rng = random.Random(SEED)

    # Use a temp directory for baseline store (validation only)
    with tempfile.TemporaryDirectory() as tmpdir:
        store = BaselineStore(Path(tmpdir))
        pipeline = Layer4Pipeline(baseline_store=store)

        print("=" * 60)
        print("Phase 4: Layer 4 Statistical Comparison (Synthetic Baselines)")
        print(f"N={N_SAMPLES} per array | Wilcoxon signed-rank | Wilson CIs")
        print("=" * 60)

        results: list[dict] = []

        for agent_id, floor in AGENT_FLOORS.items():
            agent_data = composites.get(agent_id, {})
            phase2_composite = agent_data.get("composite", 0.0)

            if phase2_composite == 0.0:
                print(f"\n  SKIP {agent_id}: Phase 2 composite is 0.0")
                results.append(
                    {
                        "agent_id": agent_id,
                        "status": "SKIP",
                        "reason": "Phase 2 composite is 0.0",
                    }
                )
                continue

            print(f"\n--- {agent_id} (floor={floor}, Phase 2 composite={phase2_composite:.4f}) ---")

            # Generate score arrays
            baseline_scores = generate_synthetic_baseline(floor, N_SAMPLES, rng)
            candidate_scores = generate_candidate_from_composite(phase2_composite, N_SAMPLES, rng)

            print(
                f"  Baseline:  mean={sum(baseline_scores) / len(baseline_scores):.4f} (synthetic, centered ~{floor + 0.05:.2f})"
            )
            print(
                f"  Candidate: mean={sum(candidate_scores) / len(candidate_scores):.4f} (from Phase 2 composite)"
            )

            version_key_a = f"baseline:{agent_id}"
            version_key_b = f"candidate:{agent_id}"

            metric_scores = {
                "composite_score": (baseline_scores, candidate_scores),
            }

            try:
                exit_code = pipeline.run(
                    agent_id=agent_id,
                    version_key_a=version_key_a,
                    version_key_b=version_key_b,
                    metric_scores=metric_scores,
                    evaluation_mode=EvaluationMode.FULL,
                    apply_bonferroni=False,  # Single metric, no Bonferroni needed
                    output_json_path=VALIDATION_DIR / "layer4-statistical" / f"{agent_id}.json",
                    output_markdown_path=VALIDATION_DIR / "layer4-statistical" / f"{agent_id}.md",
                )

                exit_label = {0: "PASS", 1: "BLOCK", 2: "WARNING"}.get(
                    exit_code, f"UNKNOWN({exit_code})"
                )
                print(f"  Exit code: {exit_code} ({exit_label})")

                results.append(
                    {
                        "agent_id": agent_id,
                        "status": exit_label,
                        "exit_code": exit_code,
                        "baseline_mean": round(sum(baseline_scores) / len(baseline_scores), 4),
                        "candidate_mean": round(sum(candidate_scores) / len(candidate_scores), 4),
                        "phase2_composite": phase2_composite,
                        "n_samples": N_SAMPLES,
                        "note": "Synthetic baseline -- validation only",
                    }
                )

            except Exception as exc:
                print(f"  ERROR: {exc}")
                results.append(
                    {
                        "agent_id": agent_id,
                        "status": "ERROR",
                        "error": str(exc),
                    }
                )

    # Write summary report
    write_report(results)


def write_report(results: list[dict]) -> None:
    """Write the Layer 4 validation results report."""
    lines = [
        "# Layer 4: Statistical Comparison Validation Results",
        "",
        "> VALIDATION TEST -- synthetic baselines, not real historical data.",
        f"> N={N_SAMPLES} per array (minimum for Wilcoxon signed-rank).",
        "> Purpose: verify Layer4Pipeline wiring works end-to-end.",
        "",
        "## Summary Table",
        "",
        "| Agent | Floor | Phase 2 | Baseline Mean | Candidate Mean | Verdict |",
        "|-------|-------|---------|---------------|----------------|---------|",
    ]

    for r in results:
        if r.get("status") == "SKIP":
            lines.append(f"| {r['agent_id']} | -- | -- | -- | -- | SKIP |")
            continue
        if r.get("status") == "ERROR":
            lines.append(f"| {r['agent_id']} | -- | -- | -- | -- | ERROR |")
            continue
        lines.append(
            f"| {r['agent_id']} | {AGENT_FLOORS[r['agent_id']]} | "
            f"{r['phase2_composite']:.4f} | {r['baseline_mean']:.4f} | "
            f"{r['candidate_mean']:.4f} | **{r['status']}** |"
        )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Baselines are synthetic (Gaussian centered at floor + 0.05, σ=0.03)",
            "- Candidates are derived from Phase 2 composite (Gaussian, σ=0.02)",
            "- No Bonferroni correction applied (single metric per agent)",
            f"- Seed: {SEED} for reproducibility",
        ]
    )

    report_path = VALIDATION_DIR / "layer4-statistical" / "results.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport written: {report_path.name}")

    # Write JSON for Phase 5
    json_path = VALIDATION_DIR / "layer4-statistical" / "results.json"
    json_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"JSON written: {json_path.name}")


if __name__ == "__main__":
    main()
