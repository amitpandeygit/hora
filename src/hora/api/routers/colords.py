"""Stronger co-lord — book §15.5.1.

The rule section 9.2 defers to when a house falls in Scorpio or Aquarius.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.models_colord import CoLordIn, CoLordOut
from hora.services import colord_service

router = APIRouter(prefix="/v1/colord", tags=["colords"])


@router.post("/stronger", response_model=CoLordOut,
             summary="The primary lord of Scorpio or Aquarius, rule by rule")
def stronger(req: CoLordIn) -> dict:
    try:
        return colord_service.stronger(
            req.rasi, req.graha_longitudes, req.purpose,
            req.rasi_aspects, req.dasa_years,
        )
    except colord_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
