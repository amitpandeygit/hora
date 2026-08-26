"""Argala endpoints — book chapter 10, §10.5 and §10.6.

Separate from ``/v1/aspect`` because argala is a different mechanism: it counts
houses from a target rather than casting from a graha, and section 10.6's
obstruction pairing has no counterpart in drishti.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.models_argala import (
    ArgalaChartIn,
    ArgalaChartOut,
    ArgalaOnKarakaIn,
    ArgalaOnKarakaOut,
    ArgalaOnSignIn,
    ArgalaOnSignOut,
    ArgalaRulesOut,
)
from hora.services import argala_service

router = APIRouter(prefix="/v1/argala", tags=["argalas"])


@router.post("/chart", response_model=ArgalaChartOut,
             summary="Argalas and virodhargalas on all twelve houses")
def chart(req: ArgalaChartIn) -> dict:
    """Exercise 16's shape, in one call."""
    try:
        return argala_service.chart(
            req.rasis, req.lagna_rasi, malefics=req.malefics,
            several=req.several_malefics)
    except argala_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/sign", response_model=ArgalaOnSignOut,
             summary="Argalas and virodhargalas on one sign")
def on_sign(req: ArgalaOnSignIn) -> dict:
    """One target, the form section 10.6's own worked example takes.

    No lagna is needed: argala counts from the target sign, not from the
    ascendant.
    """
    try:
        return argala_service.on_sign(
            req.sign, req.rasis, malefics=req.malefics,
            several=req.several_malefics)
    except argala_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/karaka", response_model=ArgalaOnKarakaOut,
             summary="Section 10.7: argalas on a karaka rather than a house")
def on_karaka(req: ArgalaOnKarakaIn) -> dict:
    """Argala on a graha is argala on the sign it occupies.

    Section 10.6 says so outright — planets in the argala houses "cause argala
    on Vi *and on the planets in Vi*" — and section 10.7 step 1 makes the
    karaka a first-class target alongside a house.
    """
    try:
        return argala_service.on_karaka(
            req.graha, req.rasis, malefics=req.malefics,
            several=req.several_malefics)
    except argala_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/rules", response_model=ArgalaRulesOut,
            summary="Section 10.6's obstruction pairing and its two special rules")
def rules() -> dict:
    return argala_service.rules()
