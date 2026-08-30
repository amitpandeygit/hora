"""Sodhya pinda endpoints — book section 12.7.

Kept apart from `ashtakavarga.py`, which is at the architecture line cap, and
because section 12.7 is a family in its own right: the reductions that turn a
BAV into a SoAV, and then the pindas computed from it.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.models_sodhana import (
    EkaadhipatyaIn,
    EkaadhipatyaOut,
    SodhanaRulesOut,
    TrikonaSodhanaIn,
    TrikonaSodhanaOut,
)
from hora.services import sodhana_service

router = APIRouter(prefix="/v1/sodhana", tags=["ashtakavarga"])


@router.get("/rules", response_model=SodhanaRulesOut,
            summary="Section 12.7's framing, its rules, and Example 40")
def rules() -> dict:
    return sodhana_service.rules()


@router.post("/trikona", response_model=TrikonaSodhanaOut,
             summary="Section 12.7.1 — trinal reduction of a planet's BAV")
def trikona(req: TrikonaSodhanaIn) -> dict:
    try:
        return sodhana_service.trikona(
            req.owner, req.rekhas, req.reference_signs)
    except (sodhana_service.AshtakavargaError,
            sodhana_service.InputError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/ekaadhipatya", response_model=EkaadhipatyaOut,
             summary="Section 12.7.2 — co-owned reduction of a reduced BAV")
def ekaadhipatya(req: EkaadhipatyaIn) -> dict:
    try:
        return sodhana_service.ekaadhipatya(
            req.owner, req.rekhas, req.reference_signs,
            req.occupied_signs, req.already_trikona_reduced)
    except (sodhana_service.AshtakavargaError,
            sodhana_service.InputError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
