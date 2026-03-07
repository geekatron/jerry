# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Per-agent G-Eval criteria definitions for the Five Target Agents.

Each submodule defines a ``list[QualityCriterion]`` constant (``*_CRITERIA``)
that encodes the G-Eval rubric for one Jerry agent. Criteria are authored using
the six S-014 quality dimensions (quality-enforcement.md) plus agent-specific
structural assertions derived from behavioral-contracts.md.

Available criteria sets:
    - ps_researcher.PS_RESEARCHER_CRITERIA  (floor 0.82)
    - ps_analyst.PS_ANALYST_CRITERIA        (floor 0.85)
    - ps_architect.PS_ARCHITECT_CRITERIA    (floor 0.88)
    - ps_critic.PS_CRITIC_CRITERIA          (floor 0.83)
    - adv_scorer.ADV_SCORER_CRITERIA        (floor 0.90)

Domain Isolation (H-07):
    All modules in this package are DOMAIN modules. They import only from:
    - jerry.testing.evaluation.criterion (QualityCriterion)
    - stdlib

References:
    - FR-007: G-Eval custom criteria evaluation
    - contracts/behavioral-contracts.md §B.3: Per-agent quality floors
    - contracts/behavioral-contracts.md §B.4: Per-agent per-dimension bounds
    - quality-enforcement.md: S-014 dimension weights (SSOT)
"""

from jerry.testing.evaluation.criteria.adv_scorer import ADV_SCORER_CRITERIA
from jerry.testing.evaluation.criteria.ps_analyst import PS_ANALYST_CRITERIA
from jerry.testing.evaluation.criteria.ps_architect import PS_ARCHITECT_CRITERIA
from jerry.testing.evaluation.criteria.ps_critic import PS_CRITIC_CRITERIA
from jerry.testing.evaluation.criteria.ps_researcher import PS_RESEARCHER_CRITERIA

__all__ = [
    "PS_RESEARCHER_CRITERIA",
    "PS_ANALYST_CRITERIA",
    "PS_ARCHITECT_CRITERIA",
    "PS_CRITIC_CRITERIA",
    "ADV_SCORER_CRITERIA",
]
