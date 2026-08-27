"""Planetary yogas — book chapters 11 onward.

**Not `charts/yoga.py`.** That module computes §1.3.9's nithya yoga, the
panchanga's Sun-plus-Moon reckoning, and shares only the word. These are the
planetary combinations.

The design constraint is exhaustiveness. :func:`evaluate` runs **every**
registered yoga and returns a verdict for each — present or absent, with the
evidence either way. A caller never has to ask whether a yoga was considered,
and a yoga cannot be dropped by being forgotten in a loop, because the registry
is what is iterated.
"""
from __future__ import annotations

# Importing the group modules is what fills the registry. Every group must be
# imported here, or its yogas silently never run — which is the one failure
# this design has to prevent. `test_every_group_module_is_imported` guards it.
from hora.charts.planetary_yogas import aakriti as _aakriti  # noqa: F401
from hora.charts.planetary_yogas import chandra as _chandra  # noqa: F401
from hora.charts.planetary_yogas import mahapurusha as _mahapurusha  # noqa: F401
from hora.charts.planetary_yogas import naabhasa as _naabhasa  # noqa: F401
from hora.charts.planetary_yogas import popular as _popular  # noqa: F401
from hora.charts.planetary_yogas import ravi as _ravi  # noqa: F401
from hora.charts.planetary_yogas import sankhya as _sankhya  # noqa: F401
from hora.charts.planetary_yogas.registry import (
    YOGA_REGISTRY,
    YogaError,
    YogaInput,
    YogaVerdict,
    evaluate,
    evaluate_one,
    groups,
)

__all__ = [
    "YOGA_REGISTRY", "YogaError", "YogaInput", "YogaVerdict",
    "evaluate", "evaluate_one", "groups",
]
