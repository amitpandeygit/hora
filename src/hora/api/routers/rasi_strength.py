"""Stronger rasi — book §15.5.2.

The cascade rasi dasas start from, and the one used for the stronger of the two
rasis a planet owns when computing its graha arudha.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.models_rasi_strength import (
    PurposesOut,
    RasiStrengthIn,
    RasiStrengthOut,
)
from hora.services import rasi_strength_service

router = APIRouter(prefix="/v1/rasi-strength", tags=["rasi-strength"])


@router.post("/stronger", response_model=RasiStrengthOut,
             summary="Which of two rasis is stronger, rule by rule")
def stronger(req: RasiStrengthIn) -> dict:
    try:
        return rasi_strength_service.stronger(
            req.first, req.second, req.graha_longitudes, req.purpose,
            req.dasa_years, req.atma_karaka_rasi,
        )
    except rasi_strength_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/purposes", response_model=PurposesOut,
            summary="Section 15.5.2's warning: which adaptation fits which dasa")
def purposes() -> dict:
    return rasi_strength_service.purposes()
