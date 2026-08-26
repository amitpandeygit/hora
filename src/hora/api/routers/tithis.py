"""Tithi endpoints — book §1.3.8.1.

Takes longitudes rather than a nativity: the procedure needs nothing else.
For the tithi running at an instant, use /v1/panchanga.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.models_tithi import TithiIn, TithiOut, TithiRulesOut
from hora.services import tithi_service

router = APIRouter(prefix="/v1/tithi", tags=["tithis"])


@router.post("/compute", response_model=TithiOut,
             summary="The tithi for a Sun and Moon longitude, with all four steps")
def compute(req: TithiIn) -> dict:
    try:
        return tithi_service.tithi(req.sun_longitude, req.moon_longitude)
    except tithi_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/rules", response_model=TithiRulesOut,
            summary="Section 1.3.8.1's definition, procedure and Table 3")
def rules() -> dict:
    return tithi_service.rules()
