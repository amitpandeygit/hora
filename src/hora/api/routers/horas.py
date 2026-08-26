"""Hora endpoints — book §1.3.11."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Path

from hora.api.models_hora import HoraDayOut, HoraIn, HoraOut, HoraRulesOut
from hora.services import hora_service

router = APIRouter(prefix="/v1/hora", tags=["horas"])


@router.post("/compute", response_model=HoraOut,
             summary="The hora running so long after sunrise, with all five steps")
def compute(req: HoraIn) -> dict:
    try:
        return hora_service.hora(req.weekday, req.elapsed_hours, req.day_length_hours)
    except hora_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/day/{weekday}", response_model=HoraDayOut,
            summary="All 24 hora lords of a weekday, from sunrise")
def day(weekday: int = Path(..., ge=0, le=6)) -> dict:
    try:
        return hora_service.day(weekday)
    except hora_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/rules", response_model=HoraRulesOut,
            summary="Section 1.3.11's definitions, speed order and weekday lords")
def rules() -> dict:
    return hora_service.rules()
