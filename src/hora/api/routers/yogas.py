"""Sun-Moon yoga endpoints — book §1.3.9.

Takes longitudes rather than a nativity: the procedure needs nothing else.
For the yoga running at an instant, use /v1/panchanga.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.models_yoga import YogaIn, YogaOut, YogaRulesOut
from hora.services import yoga_service

router = APIRouter(prefix="/v1/yoga", tags=["yogas"])


@router.post("/compute", response_model=YogaOut,
             summary="The Sun-Moon yoga for two longitudes, with all five steps")
def compute(req: YogaIn) -> dict:
    try:
        return yoga_service.yoga(req.sun_longitude, req.moon_longitude)
    except yoga_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/rules", response_model=YogaRulesOut,
            summary="Section 1.3.9's procedure and Table 5")
def rules() -> dict:
    return yoga_service.rules()
