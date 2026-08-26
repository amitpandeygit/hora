"""Special-lagna endpoints that take longitudes rather than a birth.

A special lagna is a pure function of the Sun at sunrise, the elapsed minutes
and a rate — which is exactly what the book's worked examples supply. Exposing
it that way makes chapter 5 callable and checkable without an ephemeris.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.models_lagna import (
    SpecialLagnaComputeOut,
    SpecialLagnaIn,
    SpecialLagnaRulesOut,
)
from hora.services import lagna_service

router = APIRouter(prefix="/v1/lagna", tags=["lagnas"])


@router.post("/special", response_model=SpecialLagnaComputeOut,
             summary="Special lagnas from the book's own inputs")
def special(req: SpecialLagnaIn) -> dict:
    try:
        return lagna_service.compute(
            sun_at_sunrise=req.sun_at_sunrise,
            minutes_since_sunrise=req.minutes_since_sunrise,
            moon=req.moon,
            lagna=req.lagna,
            lagnas=req.lagnas,
        )
    except lagna_service.SpecialLagnaError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/rules", response_model=SpecialLagnaRulesOut,
            summary="Each special lagna, its rate and what it shows")
def rules() -> dict:
    return lagna_service.rules()
