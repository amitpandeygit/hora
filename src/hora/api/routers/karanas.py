"""Karana endpoints — book §1.3.10."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.models_karana import (
    KaranaLongitudesIn,
    KaranaOut,
    KaranaRulesOut,
    KaranaSlotIn,
)
from hora.services import karana_service

router = APIRouter(prefix="/v1/karana", tags=["karanas"])


@router.post("/compute", response_model=KaranaOut,
             summary="The karana at a slot, or in a given half of a tithi")
def compute(req: KaranaSlotIn) -> dict:
    try:
        if req.slot is not None:
            return karana_service.for_slot(req.slot)
        if req.tithi is not None and req.half is not None:
            return karana_service.for_tithi_half(req.tithi, req.half)
    except karana_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    raise HTTPException(
        status_code=400, detail="give either slot, or both tithi and half"
    )


@router.post("/at", response_model=KaranaOut,
             summary="The karana running for a Sun and Moon longitude")
def at(req: KaranaLongitudesIn) -> dict:
    try:
        return karana_service.at_longitudes(req.sun_longitude, req.moon_longitude)
    except karana_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/rules", response_model=KaranaRulesOut,
            summary="Section 1.3.10's statements and the 11 karanas")
def rules() -> dict:
    return karana_service.rules()
