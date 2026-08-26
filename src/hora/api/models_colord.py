"""Models for the stronger-co-lord endpoint — book §15.5.1."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CoLordIn(BaseModel):
    rasi: int = Field(
        ..., ge=0, le=11,
        description="Scorpio (7) or Aquarius (10) — the two co-owned rasis",
    )
    graha_longitudes: dict[int, float] = Field(
        ..., description="Graha id -> sidereal longitude; both co-lords required"
    )
    purpose: str = Field(
        "arudha",
        description=(
            'Which step-5 tie-break applies. "arudha" uses rule 5b (more '
            'advanced in its rasi); "dasa" uses rule 5a (the longer dasa).'
        ),
        examples=["arudha", "dasa"],
    )
    rasi_aspects: dict[int, list[int]] | None = Field(
        None,
        description=(
            "Sign -> signs it aspects, for rule 2. Defaults to Jaimini rasi "
            "drishti; supply a table only to override it. An empty object "
            "models 'no aspects known', which stops the cascade at rule 2 "
            "rather than skipping to rule 3 — section 15.5.1 forbids skipping."
        ),
    )
    dasa_years: dict[int, float] | None = Field(
        None, description="Graha -> dasa length, for rule 5a only"
    )


class RuleVerdictOut(BaseModel):
    rule: str = Field(..., examples=["basic", "1", "5b"])
    description: str = Field(..., description="The rule as section 15.5.1 states it")
    winner: int | None = None
    winner_name: str | None = None
    evaluated: bool = Field(
        ..., description="False when the cascade stopped before this rule"
    )
    decided: bool | None = Field(
        None, description="Null when the rule could not be evaluated"
    )
    detail: str


class CoLordOut(BaseModel):
    rasi: int
    rasi_name: str
    co_lords: list[int]
    co_lord_names: list[str]
    winner: int | None = None
    winner_name: str | None = None
    decided_by: str | None = Field(
        None, description="Which rule settled it, or null if none did"
    )
    determined: bool
    reason: str
    rules: list[RuleVerdictOut] = Field(
        ..., description="Every rule reached, in order, and what it decided"
    )
