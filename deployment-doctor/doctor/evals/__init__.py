"""The graded set that answers "is the judgement pass any good?"

`cases.py` is the artefact; `score.py` and `run.py` are bookkeeping around it.
"""

from .cases import CASES, Case, Expected
from .run import DEFAULT_MODELS, render, run_model
from .score import CaseResult, RunResult, score_case

__all__ = [
    "CASES",
    "Case",
    "CaseResult",
    "DEFAULT_MODELS",
    "Expected",
    "RunResult",
    "render",
    "run_model",
    "score_case",
]
