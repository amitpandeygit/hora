"""Aspect endpoints — book chapter 10.

Section 10.2 derives three things from one placement — aspected rasis, the
houses they are, and the grahas in them — so ``/chart`` answers all three at
once. The single-graha and pair endpoints exist for the chapter's own
one-line examples, which need no chart at all.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.models_aspect import (
    AspectRulesOut,
    BetweenIn,
    BetweenOut,
    ChartAspectIn,
    ChartAspectOut,
    GrahaAspectIn,
    GrahaAspectOut,
)
from hora.services import aspect_service

router = APIRouter(prefix="/v1/aspect", tags=["aspects"])


@router.post("/chart", response_model=ChartAspectOut,
             summary="Every graha drishti in one chart — rasis, houses and planets")
def chart(req: ChartAspectIn) -> dict:
    """The shape Exercise 14 asks for, in one call.

    ``lagna_rasi`` is optional: without it the aspected rasis are still
    returned and the house column is null, because section 10.2 needs no
    lagna to say which rasis a graha aspects.
    """
    try:
        return aspect_service.chart(
            req.rasis, req.lagna_rasi, rahu_ketu_aspects=req.rahu_ketu_aspects)
    except aspect_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/graha", response_model=GrahaAspectOut,
             summary="What one graha aspects from one rasi")
def graha(req: GrahaAspectIn) -> dict:
    try:
        return aspect_service.graha(
            req.graha, req.rasi, lagna_rasi=req.lagna_rasi, others=req.others,
            rahu_ketu_aspects=req.rahu_ketu_aspects)
    except aspect_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/between", response_model=BetweenOut,
             summary="Whether a graha aspects a rasi, and the house that decides it")
def between(req: BetweenIn) -> dict:
    try:
        return aspect_service.between(
            req.graha, req.graha_rasi, req.target_rasi,
            rahu_ketu_aspects=req.rahu_ketu_aspects)
    except aspect_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/rules", response_model=AspectRulesOut,
            summary="Chapter 10's aspect rules as the chapter states them")
def rules() -> dict:
    return aspect_service.rules()
