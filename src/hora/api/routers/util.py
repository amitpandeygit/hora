"""Utility endpoints: longitude notation and the chapter reference tables.

HTTP only — the tables are built in :mod:`hora.services.reference_service`.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from hora.api.models_reference import (
    GrahaTableOut,
    NakshatraTableOut,
    NameSchemesOut,
    NotationOut,
    RasiTableOut,
    RelationshipTermsOut,
    TermsOut,
    TithiTableOut,
    YogaTableOut,
)
from hora.core.notation import NotationError
from hora.services import reference_service

router = APIRouter(prefix="/v1/util", tags=["util"])


class NotationIn(BaseModel):
    value: str = Field(
        ...,
        examples=["5s 17 45", "25 Li 31", "167.75"],
        description="Decimal degrees, sign-degree-minute, or rasi-relative",
    )


@router.post("/notation", response_model=NotationOut,
             summary="Parse a classical longitude notation")
def notation(req: NotationIn) -> dict:
    try:
        return reference_service.resolve_notation(req.value)
    except NotationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/tables/nakshatras", response_model=NakshatraTableOut,
            summary="Table 2 — nakshatras, spans and Vimsottari lords")
def nakshatra_table() -> dict:
    return reference_service.nakshatra_table()


@router.get("/tables/tithis", response_model=TithiTableOut,
            summary="Table 3 — tithis, pakshas and lords")
def tithi_table() -> dict:
    return reference_service.tithi_table()


@router.get("/tables/yogas", response_model=YogaTableOut,
            summary="Table 5 — the 27 yogas and their meanings")
def yoga_table() -> dict:
    return reference_service.yoga_table()


@router.get("/tables/relationship-terms", response_model=RelationshipTermsOut,
            summary="Section 3.4's Sanskrit terms for planetary relationships")
def relationship_terms() -> dict:
    return reference_service.relationship_terms()


@router.get("/tables/rasis", response_model=RasiTableOut,
            summary="Chapter 2 — every rasi attribute")
def rasi_table() -> dict:
    return reference_service.rasi_table()


@router.get("/tables/grahas", response_model=GrahaTableOut,
            summary="Chapter 3 — every graha attribute")
def graha_table() -> dict:
    return reference_service.graha_table()


@router.get("/tables/name-schemes", response_model=NameSchemesOut,
            summary="Available transliteration schemes")
def name_schemes() -> dict:
    return reference_service.name_schemes()


@router.get("/tables/terms", response_model=TermsOut,
            summary="Vocabulary the book defines once and uses throughout")
def terms() -> dict:
    return reference_service.terms()
