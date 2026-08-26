"""Lunar month endpoints — book §1.3.8.2.

Takes the conjunction longitude rather than a date: §1.3.8.2 names a month by
where the Sun-Moon conjunction fell. For the month running at an instant, use
/v1/panchanga.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.models_maasa import (
    MaasaIn,
    MaasaOut,
    MaasaPairIn,
    MaasaPairOut,
    MaasaRulesOut,
)
from hora.services import maasa_service

router = APIRouter(prefix="/v1/maasa", tags=["lunar months"])


@router.post("/compute", response_model=MaasaOut,
             summary="The lunar month a Sun-Moon conjunction starts")
def compute(req: MaasaIn) -> dict:
    try:
        return maasa_service.maasa(req.conjunction_longitude, req.qualifier)
    except maasa_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/pair", response_model=MaasaPairOut,
             summary="Two conjunctions in one rasi — the adhika maasa case")
def pair(req: MaasaPairIn) -> dict:
    try:
        return maasa_service.month_pair(req.first_longitude, req.second_longitude)
    except maasa_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/rules", response_model=MaasaRulesOut,
            summary="Section 1.3.8.2's definitions and Table 4")
def rules() -> dict:
    return maasa_service.rules()
