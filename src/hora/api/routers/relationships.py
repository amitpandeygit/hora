"""Planetary relationship endpoints — book §3.4."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.models_relationship import (
    ChartIn,
    ChartOut,
    CompoundIn,
    CompoundOut,
    NaturalIn,
    NaturalOut,
    RelationshipRulesOut,
    TemporaryIn,
    TemporaryOut,
)
from hora.services import relationship_service

router = APIRouter(prefix="/v1/relationship", tags=["relationships"])


@router.post("/chart", response_model=ChartOut,
             summary="Every relationship in one chart — natural, temporary, "
                     "compound, and the friendly/inimical house standing")
def chart(req: ChartIn) -> dict:
    """The whole of section 3.4 for one chart, in one call.

    The three endpoints below answer a single pair or serve a rule in
    isolation. This one is what a caller building a reading wants: nothing
    has to be joined by hand.
    """
    try:
        return relationship_service.chart(req.rasis, req.include_nodes)
    except relationship_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/natural", response_model=NaturalOut,
             summary="Section 3.4.1's natural relation, with its derivation")
def natural(req: NaturalIn) -> dict:
    try:
        return relationship_service.natural_relation(req.graha, req.other)
    except relationship_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/temporary", response_model=TemporaryOut,
             summary="Section 3.4.2's temporary relations, for one chart")
def temporary(req: TemporaryIn) -> dict:
    try:
        return relationship_service.temporary_relation(
            req.graha, req.rasis, req.include_nodes
        )
    except relationship_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/compound", response_model=CompoundOut,
             summary="Section 3.4.3's compound relation, with both inputs shown")
def compound(req: CompoundIn) -> dict:
    try:
        return relationship_service.compound_relation(
            req.graha, req.rasis, req.other
        )
    except relationship_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/rules", response_model=RelationshipRulesOut,
            summary="Section 3.4's two schemes and Table 7")
def rules() -> dict:
    return relationship_service.rules()
