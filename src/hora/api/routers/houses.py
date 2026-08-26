"""House endpoints — book chapter 7.

A house is a rasi counted from a reference, so these take rasi indices rather
than a birth: the arithmetic needs nothing else.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Path, Query

from hora.api.models_house import (
    CategoriesOut,
    DerivedHouseOut,
    HouseMeaningsOut,
    HouseRulesOut,
    HousesFromIn,
    HousesFromOut,
    ReferencesIn,
    ReferencesOut,
)
from hora.services import house_service

router = APIRouter(prefix="/v1/house", tags=["houses"])


@router.post("/from", response_model=HousesFromOut,
             summary="All twelve houses counted from a reference rasi")
def houses_from(req: HousesFromIn) -> dict:
    try:
        return house_service.houses_from_reference(req.reference_rasi, req.reference)
    except house_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/references", response_model=ReferencesOut,
             summary="Resolve section 7.3's reference points")
def references(req: ReferencesIn) -> dict:
    try:
        return house_service.references(
            lagna_rasi=req.lagna_rasi,
            graha_rasis=req.graha_rasis,
            ghati_lagna_rasi=req.ghati_lagna_rasi,
            hora_lagna_rasi=req.hora_lagna_rasi,
        )
    except house_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/categories/{base_house}", response_model=CategoriesOut,
            summary="Trines, quadrants and the rest, counted from any house")
def categories(
    base_house: int = Path(..., ge=1, le=12,
                           description="Count the categories from this house"),
) -> dict:
    return house_service.categories(base_house)


@router.get("/derived", response_model=DerivedHouseOut,
            summary="Section 7.2: a house counted from another house")
def derived(
    house: int = Query(..., ge=1, le=12, examples=[2]),
    from_house: int = Query(..., ge=1, le=12, examples=[3]),
) -> dict:
    """"The 2nd house from the 3rd house is the 4th house." Counting is
    inclusive: the 3rd counts as the 1st."""
    try:
        return house_service.derived(house, from_house)
    except house_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/meanings", response_model=HouseMeaningsOut,
            summary="Section 7.3: which of a house's meanings apply in a chart")
def meanings(
    house: int = Query(..., ge=1, le=12, examples=[4]),
    chart: str = Query(..., examples=["D16"]),
) -> dict:
    """The literal overlap of the two signification lists — a hint, not a
    derivation. See the `limitation` field."""
    try:
        return house_service.meanings_in_varga(house, chart)
    except house_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/rules", response_model=HouseRulesOut,
            summary="Significations, categories, purusharthas and Table 12")
def rules() -> dict:
    return house_service.rules()
