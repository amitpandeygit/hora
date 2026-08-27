"""Planetary yoga endpoints — book chapter 11 onward.

Separate from ``/v1/yoga``, which is §1.3.9's nithya yoga and an unrelated
calculation that happens to share the word.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from hora.api.models_planetary_yoga import (
    GuidelineIn,
    GuidelinesOut,
    PlanetaryYogaRulesOut,
    RaajaMagnitudeIn,
    RaajaMagnitudeOut,
    YogaCatalogueOut,
    YogaChartIn,
    YogaChartOut,
    YogaOneIn,
    YogaVerdictOut,
)
from hora.services import planetary_yoga_service

router = APIRouter(prefix="/v1/planetary-yoga", tags=["planetary yogas"])


@router.post("/chart", response_model=YogaChartOut,
             summary="Every known yoga on one chart, present or absent")
def chart(req: YogaChartIn) -> dict:
    try:
        return planetary_yoga_service.chart(
            req.rasis, chart_code=req.chart,
            include_nodes=req.include_nodes, group=req.group,
            lagna_rasi=req.lagna_rasi, paksha=req.paksha)
    except (planetary_yoga_service.InputError,
            planetary_yoga_service.YogaError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/one", response_model=YogaVerdictOut,
             summary="One yoga by key, with its evidence either way")
def one(req: YogaOneIn) -> dict:
    try:
        return planetary_yoga_service.one(
            req.key, req.rasis, chart_code=req.chart,
            include_nodes=req.include_nodes)
    except (planetary_yoga_service.InputError,
            planetary_yoga_service.YogaError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/guidelines", response_model=GuidelinesOut,
             summary="Section 11.3's three General Guidelines — graded readings, not yogas")
def guidelines(req: GuidelineIn) -> dict:
    try:
        return planetary_yoga_service.guidelines(req.rasis, paksha=req.paksha)
    except (planetary_yoga_service.InputError,
            planetary_yoga_service.YogaError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/catalogue", response_model=YogaCatalogueOut,
            summary="Every yoga the engine knows, with no chart supplied")
def catalogue(
    group: str | None = Query(None, examples=["ravi"]),
) -> dict:
    try:
        return planetary_yoga_service.catalogue(group)
    except planetary_yoga_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/rules", response_model=PlanetaryYogaRulesOut,
            summary="Chapter 11's framing, and what the engine does not decide")
def rules() -> dict:
    return planetary_yoga_service.rules()


@router.post("/raaja-magnitude", response_model=RaajaMagnitudeOut,
             summary="Section 11.7.2 — how far each Raaja yoga fructifies")
def raaja_magnitude(req: RaajaMagnitudeIn) -> dict:
    try:
        return planetary_yoga_service.raaja_magnitude(
            req.longitudes, lagna_rasi=req.lagna_rasi)
    except (planetary_yoga_service.InputError,
            planetary_yoga_service.YogaError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
