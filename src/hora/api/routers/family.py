"""Family-member endpoints — book section 13.4.2."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.models_family import (
    ChildrenIn,
    FamilyRulesOut,
    ParentIn,
    RelativeIn,
    SiblingsIn,
)
from hora.services import family_service

router = APIRouter(prefix="/v1/family", tags=["interpretation"])


def _guard(call, *args, **kwargs) -> dict:
    try:
        return call(*args, **kwargs)
    except (family_service.FamilyError, family_service.InputError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/rules", response_model=FamilyRulesOut,
            summary="Section 13.4.2's charts, method and worked examples")
def rules() -> dict:
    return family_service.rules()


@router.post("/parent", summary="Father or mother, from D-12")
def parent(req: ParentIn) -> dict:
    return _guard(family_service.parent, req.relation, req.lagna,
                  req.graha_signs, req.stronger_lord)


@router.post("/siblings", summary="Elder or younger siblings, from D-3")
def siblings(req: SiblingsIn) -> dict:
    return _guard(family_service.siblings, req.lagna, req.elder, req.depth,
                  req.graha_signs, req.stronger_lord)


@router.post("/children", summary="Children, from D-7")
def children(req: ChildrenIn) -> dict:
    return _guard(family_service.children, req.lagna, req.depth,
                  req.graha_signs, req.stronger_lord)


@router.post("/relative", summary="Any relation, once you choose the house")
def relative(req: RelativeIn) -> dict:
    return _guard(family_service.any_relative, req.relation, req.chart,
                  req.house, req.lagna, req.graha_signs, req.stronger_lord,
                  req.directional)
