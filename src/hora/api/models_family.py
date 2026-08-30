"""Request and response models for section 13.4.2."""
from __future__ import annotations

from pydantic import BaseModel, Field


class _Base(BaseModel):
    lagna: int = Field(..., ge=0, le=11, examples=[2])
    graha_signs: dict[int, int] | None = Field(None, examples=[None])
    stronger_lord: dict[int, int] | None = Field(None, examples=[None])


class ParentIn(_Base):
    relation: str = Field(..., examples=["father"])


class SiblingsIn(_Base):
    elder: bool = Field(..., examples=[False])
    depth: int = Field(6, ge=1, le=6, examples=[6])


class ChildrenIn(_Base):
    depth: int = Field(6, ge=1, le=6, examples=[6])


class RelativeIn(_Base):
    relation: str = Field(..., examples=["paternal uncle"])
    chart: str = Field(..., examples=["D12"])
    house: int = Field(..., ge=1, le=12, examples=[11])
    directional: bool = Field(False, examples=[False])


class FamilyRulesOut(BaseModel):
    intro: str
    charts: list[dict]
    chart_for: dict
    method: str
    named_relatives: list[dict]
    siblings_rule: str
    children_rule: str
    nested_house_claims: list[dict]
    direction_rule: str
    direction_scope: str
    direction_examples: list[dict]
    note: str
    note_is_underspecified: str
    chain_depth: int
