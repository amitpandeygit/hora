"""Arudha pada endpoints — book chapter 9.

Takes a chart as signs, because section 9.2's procedure never needs a finer
position than the sign. Every response carries the six steps that produced it.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.models_arudha import (
    ArudhaOneIn,
    ArudhaPadaOut,
    ArudhaRulesOut,
    ArudhaTableIn,
    ArudhaTableOut,
)
from hora.services import arudha_service

router = APIRouter(prefix="/v1/arudha", tags=["arudhas"])


@router.post("/pada", response_model=ArudhaPadaOut,
             summary="One house's arudha pada, with all six steps of section 9.2")
def pada(req: ArudhaOneIn) -> dict:
    try:
        return arudha_service.one(
            req.house, req.lagna_sign, req.graha_signs, req.stronger_lord,
            req.graha_longitudes,
        )
    except arudha_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/table", response_model=ArudhaTableOut,
             summary="All twelve arudha padas, A1 to A12")
def table(req: ArudhaTableIn) -> dict:
    try:
        return arudha_service.table(
            req.lagna_sign, req.graha_signs, req.stronger_lord,
            req.include_steps, req.graha_longitudes,
        )
    except arudha_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/rules", response_model=ArudhaRulesOut,
            summary="Section 9.2's six steps and the dual-lordship note")
def rules() -> dict:
    return arudha_service.rules()
