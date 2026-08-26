"""Strength comparison endpoints — book chapter 15.

Which of two planets is stronger, and what measures of strength exist. The
states those verdicts rest on are in ``routers/avasthas.py``.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.models_strength import CompareIn, ComparisonOut, MeasuresOut
from hora.services import strength_service

router = APIRouter(prefix="/v1/strength", tags=["strength"])


@router.post("/compare", response_model=ComparisonOut,
             summary="Which of two grahas is stronger, axis by axis")
def compare(req: CompareIn) -> dict:
    try:
        return strength_service.comparison(req.left, req.right, req.graha_longitudes)
    except strength_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/measures", response_model=MeasuresOut,
            summary="The five measures of strength the chapter names")
def measures() -> dict:
    return strength_service.measures()
