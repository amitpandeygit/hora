"""Divisional chart endpoints that take a longitude rather than a birth.

A varga is a pure function of a longitude, so it is exposed as one: no birth
data, no ephemeris, no settings. `/v1/chart/vargas` remains the way to get the
divisional charts of an actual nativity.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from hora.api.models_varga import (
    AmsabalaIn,
    AmsabalaOut,
    MatterOut,
    VargaComputeIn,
    VargaComputeOut,
    VargaRulesOut,
)
from hora.services import varga_service

router = APIRouter(prefix="/v1/varga", tags=["vargas"])


@router.post("/compute", response_model=VargaComputeOut,
             summary="Where a longitude falls in one or more divisional charts")
def compute(req: VargaComputeIn) -> dict:
    try:
        longitude = varga_service.resolve_longitude(req.longitude)
        return varga_service.compute(longitude, req.charts, req.variants)
    except varga_service.UnknownVarga as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/for-matter", response_model=MatterOut,
            summary="Section 6.5: which chart to analyse for a matter")
def for_matter(matter: str = Query(..., min_length=1, examples=["career"])) -> dict:
    """Table 11 read matter-first, as §6.5 prescribes.

    A matter the book does not name returns an empty list rather than a guess.
    """
    try:
        return varga_service.for_matter(matter)
    except varga_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/rules", response_model=VargaRulesOut,
            summary="Every named divisional chart, its rule and its aliases")
def rules() -> dict:
    return varga_service.rules()


@router.post("/amsabala", response_model=AmsabalaOut,
             summary="Vaiseshikamsa — strength by count of good divisional placements")
def amsabala(req: AmsabalaIn) -> dict:
    """Section 6.6: count the charts of each group in which the graha holds its
    moolatrikona, own rasi or exaltation, and name the amsa that count earns."""
    try:
        longitude = varga_service.resolve_longitude(req.longitude)
        return varga_service.amsabala(longitude, req.graha)
    except varga_service.UnknownVarga as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
