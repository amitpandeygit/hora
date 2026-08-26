"""Graha arudha endpoints — book §9.5.

The arudha pada of a *planet*, as opposed to §9.2's arudha pada of a house.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.models_graha_arudha import (
    GrahaArudhaOneIn,
    GrahaArudhaOut,
    GrahaArudhaRulesOut,
    GrahaArudhaTableIn,
    GrahaArudhaTableOut,
)
from hora.services import arudha_service

router = APIRouter(prefix="/v1/graha-arudha", tags=["graha-arudhas"])


@router.post("/pada", response_model=GrahaArudhaOut,
             summary="One planet's arudha pada, with all six steps of section 9.5")
def pada(req: GrahaArudhaOneIn) -> dict:
    try:
        return arudha_service.graha(
            req.graha, req.graha_signs, req.graha_longitudes
        )
    except arudha_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/table", response_model=GrahaArudhaTableOut,
             summary="All nine graha arudhas")
def table(req: GrahaArudhaTableIn) -> dict:
    try:
        return arudha_service.graha_table(
            req.graha_signs, req.graha_longitudes, req.include_steps
        )
    except arudha_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/rules", response_model=GrahaArudhaRulesOut,
            summary="Section 9.5's six steps and the two-sign note")
def rules() -> dict:
    return arudha_service.graha_rules()
