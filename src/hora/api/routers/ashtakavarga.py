"""Ashtakavarga endpoints — book chapter 12."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from hora.api.models_ashtakavarga import (
    AshtakavargaChartIn,
    AshtakavargaChartOut,
    AshtakavargaRulesOut,
    AshtakavargaTableOut,
    BeneficRasisIn,
    BeneficRasisOut,
    DivisionalIn,
    MuhurtaIn,
    MuhurtaOut,
)
from hora.services import ashtakavarga_service

router = APIRouter(prefix="/v1/ashtakavarga", tags=["ashtakavarga"])


@router.get("/rules", response_model=AshtakavargaRulesOut,
            summary="Chapter 12's framing, its notation, and which tables exist")
def rules() -> dict:
    return ashtakavarga_service.rules()


@router.get("/table", response_model=AshtakavargaTableOut,
            summary="One ashtakavarga table, as the book prints it")
def table(owner: str = Query(..., examples=["Sun"])) -> dict:
    try:
        return ashtakavarga_service.table(owner)
    except (ashtakavarga_service.AshtakavargaError,
            ashtakavarga_service.InputError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/chart", response_model=AshtakavargaChartOut,
             summary="A chart's ashtakavarga, from every table that exists")
def chart(req: AshtakavargaChartIn) -> dict:
    try:
        return ashtakavarga_service.chart(req.reference_signs, req.owner)
    except (ashtakavarga_service.AshtakavargaError,
            ashtakavarga_service.InputError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/benefic-rasis", response_model=BeneficRasisOut,
             summary="Where one planet is benefic, reference by reference")
def benefic_rasis(req: BeneficRasisIn) -> dict:
    try:
        return ashtakavarga_service.benefic_rasis(req.owner, req.reference_signs)
    except (ashtakavarga_service.AshtakavargaError,
            ashtakavarga_service.InputError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/muhurta", response_model=MuhurtaOut,
             summary="Section 12.4's muhurta rule, read against a natal SAV")
def muhurta(req: MuhurtaIn) -> dict:
    try:
        return ashtakavarga_service.muhurta(
            req.natal_reference_signs, req.muhurta_signs)
    except (ashtakavarga_service.AshtakavargaError,
            ashtakavarga_service.InputError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/divisional", response_model=AshtakavargaChartOut,
             summary="Section 12.5 — the same tables on any divisional chart")
def divisional(req: DivisionalIn) -> dict:
    try:
        return ashtakavarga_service.divisional(
            req.reference_longitudes, req.chart, req.owner)
    except (ashtakavarga_service.AshtakavargaError,
            ashtakavarga_service.InputError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
