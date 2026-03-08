"""Quick import check for the validation pipeline dependencies."""

import anthropic

from jerry.testing.evaluation.criteria.adv_scorer import ADV_SCORER_CRITERIA
from jerry.testing.evaluation.criteria.ps_analyst import PS_ANALYST_CRITERIA
from jerry.testing.evaluation.criteria.ps_architect import PS_ARCHITECT_CRITERIA
from jerry.testing.evaluation.criteria.ps_critic import PS_CRITIC_CRITERIA
from jerry.testing.evaluation.criteria.ps_researcher import PS_RESEARCHER_CRITERIA
from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter
from jerry.testing.metamorphic.mr_001_paraphrase import ParaphraseConsistency
from jerry.testing.metamorphic.mr_003_context import IrrelevantContextAppendation

print("All imports OK")
print(f"  DeepEvalAdapter: {DeepEvalAdapter}")
print(f"  ps-researcher criteria: {len(PS_RESEARCHER_CRITERIA)} dimensions")
print(f"  ps-analyst criteria: {len(PS_ANALYST_CRITERIA)} dimensions")
print(f"  ps-architect criteria: {len(PS_ARCHITECT_CRITERIA)} dimensions")
print(f"  ps-critic criteria: {len(PS_CRITIC_CRITERIA)} dimensions")
print(f"  adv-scorer criteria: {len(ADV_SCORER_CRITERIA)} dimensions")
print(f"  ParaphraseConsistency: {ParaphraseConsistency}")
print(f"  IrrelevantContextAppendation: {IrrelevantContextAppendation}")
print(f"  anthropic SDK: {anthropic.__version__}")
