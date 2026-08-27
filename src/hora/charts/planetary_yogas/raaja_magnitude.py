"""§11.7.2 — how far a Raaja yoga fructifies.

Not a yoga. A grading of one that is already present, and deliberately not
collapsed into a single number:

    "None of the above factors influences the end result completely. We
    should look at all the factors and make the final judgment."

So this returns the factors, each answered or explicitly unanswerable, and
never a verdict. §11.7.2 names three factors and then adds Parasara's
dasavarga amsa count on top of them.

What cannot be answered, and says so rather than guessing:

- **Functional malefics.** Factor (1) turns on them and nothing read so far
  defines what a functional malefic is. Reported as not assessed — OI-88.
- **Bad avasthas.** Factor (3) says "bad avasthas (states)" without naming
  which. Every avastha the chart yields is reported, and none is called bad —
  OI-89.
- **The orb of an aspect.** The 6° guideline is exemplified only for a
  conjunction. The deviation from the exact aspect angle is what is measured
  here, and the response says so — OI-90.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from hora.charts.planetary_yogas.popular import lord_of_house
from hora.charts.planetary_yogas.raaja import association, kendra_lords, trikona_lords
from hora.charts.planetary_yogas.registry import YogaInput
from hora.core.const import (
    GRAHA_NAMES,
    RAAJA_AMSA_RESULTS,
    RAAJA_CLOSE_ORB_DEGREES,
    RASI_NAMES,
    Graha,
)

_BY_COUNT = {entry["count"]: entry for entry in RAAJA_AMSA_RESULTS}


@dataclass(frozen=True, slots=True)
class Factor:
    """One of §11.7.2's factors, for one pair."""

    key: str
    #: True, False, or None when the book gives us no way to decide.
    satisfied: bool | None
    detail: str


@dataclass(frozen=True, slots=True)
class PairMagnitude:
    """The magnitude picture for one quadrant-lord/trine-lord pair."""

    quadrant_lord: int
    quadrant_lord_name: str
    quadrant_houses: tuple[int, ...]
    trine_lord: int
    trine_lord_name: str
    trine_houses: tuple[int, ...]
    association: str
    #: Degrees, or None when the association is a parivartana — §11.7.2's
    #: closeness rule speaks only of "the conjunction or aspect".
    orb_degrees: float | None
    factors: tuple[Factor, ...]
    amsa: dict = field(default_factory=dict)


def _orb(data: YogaInput, a: int, b: int, kind: str) -> tuple[float | None, str]:
    """How close the association is, in degrees.

    For a conjunction this is the plain separation, which is what §11.7.2's
    worked example measures. For an aspect it is the deviation from the exact
    aspect angle — a whole-sign graha drishti on the Nth house is exact at
    ``(N - 1) x 30`` degrees of separation. The book gives no aspect example,
    so that reading is named in the response. See OI-90.
    """
    if kind == "parivartana":
        return None, ("a parivartana has no orb; section 11.7.2's closeness "
                      "rule speaks only of “the conjunction or aspect”")
    if not data.positions or a not in data.positions or b not in data.positions:
        return None, ("closeness is a degree measurement and no longitudes "
                      "were supplied")
    lon_a = data.positions[a].longitude
    lon_b = data.positions[b].longitude
    separation = abs(lon_a - lon_b) % 360.0
    separation = min(separation, 360.0 - separation)
    if kind == "conjunction":
        return separation, (f"{GRAHA_NAMES[a]} and {GRAHA_NAMES[b]} are "
                            f"{separation:.2f}° apart")
    # Nearest exact whole-sign aspect angle.
    exact = min((abs(separation - step * 30.0), step)
                for step in range(7))
    deviation = exact[0]
    return deviation, (f"the aspect is {deviation:.2f}° from exact "
                       f"(nearest whole-sign angle {exact[1] * 30}°); "
                       f"section 11.7.2 exemplifies the 6° rule only for a "
                       f"conjunction — see docs/open-items.md OI-90")


def _blemishes(data: YogaInput, graha: int) -> tuple[bool | None, str]:
    """Factor (3): combust, debilitated, in an inimical house, bad avastha."""
    from hora.charts.dignity import sign_dignity
    from hora.charts.planetary_yogas.popular import in_enemy_sign, is_debilitated

    name = GRAHA_NAMES[graha]
    found = []
    if is_debilitated(data, graha):
        sign = data.sign_of(graha)
        found.append(f"debilitated in {RASI_NAMES[sign]}" if sign is not None
                     else "debilitated")
    if in_enemy_sign(data, graha):
        sign = data.sign_of(graha)
        found.append(f"in an inimical house, {RASI_NAMES[sign]}"
                     if sign is not None else "in an inimical house")

    combust: bool | None = None
    why_not_combust = ""
    sun = int(Graha.SUN)
    if not data.positions or graha not in data.positions:
        why_not_combust = "no longitude was supplied for him"
    elif sun not in data.positions:
        why_not_combust = "no longitude was supplied for the Sun"
    elif graha == sun:
        combust = False
        why_not_combust = ""
    else:
        from hora.charts.dignity import combustion

        combust = combustion(graha, data.positions).combust
        if combust:
            found.append("combust")

    notes = []
    if combust is None:
        notes.append(f"combustion could not be judged: {why_not_combust}")
    if data.positions and graha in data.positions:
        dignity = sign_dignity(graha, data.positions[graha].longitude)
        notes.append(f"sign dignity is {dignity}")
    notes.append("section 11.7.2 says “bad avasthas (states)” without "
                 "naming which, so no avastha is called a blemish here — "
                 "see docs/open-items.md OI-89")

    detail = (f"{name}: " + (", ".join(found) if found else "no blemish found")
              + "; " + "; ".join(notes))
    if found:
        return False, detail
    if combust is None:
        return None, detail
    return True, detail


def _amsa(data: YogaInput, a: int, b: int) -> dict:
    """Parasara's dasavarga count for each planet, and what §11.7.2 says.

    The book speaks of "the two planets" being in one amsa. Its own worked
    example does not: Mercury at 2° Taurus counts 2 and Venus at 26° Taurus
    counts 3. So both counts are reported, and a shared result is given only
    when they agree. See OI-91.
    """
    if not data.positions or a not in data.positions or b not in data.positions:
        return {"decidable": False,
                "reason": ("the dasavarga count needs longitudes, which were "
                           "not supplied")}
    from hora.services.varga_service import amsabala

    per: dict[int, dict] = {}
    for graha in (a, b):
        group = amsabala(data.positions[graha].longitude, graha)["groups"]["dasavarga"]
        per[graha] = {
            "graha": graha,
            "graha_name": GRAHA_NAMES[graha],
            "count": group["count"],
            "amsa": group["amsa"],
            "strong_in": [row["chart"] for row in group["strong_in"]],
        }
    counts = {per[a]["count"], per[b]["count"]}
    out: dict = {"decidable": True, "planets": [per[a], per[b]]}
    if len(counts) == 1:
        count = counts.pop()
        entry = _BY_COUNT.get(count)
        out["shared_count"] = count
        out["amsa"] = entry["amsa"] if entry else None
        out["result"] = entry["result"] if entry else None
        if entry is None:
            out["note"] = (f"section 11.7.2 does not discuss a count of "
                           f"{count}")
    else:
        out["shared_count"] = None
        out["note"] = (
            f"the two planets have different counts — "
            f"{per[a]['graha_name']} {per[a]['count']}, "
            f"{per[b]['graha_name']} {per[b]['count']}. Section 11.7.2 speaks "
            f"of “the two planets” being in one amsa and does not say what "
            f"to do when they differ, which its own worked example does. No "
            f"shared amsa is asserted — see docs/open-items.md OI-91")
    return out


def magnitude(data: YogaInput) -> list[PairMagnitude]:
    """§11.7.2 for every associated quadrant-lord/trine-lord pair in a chart.

    Returns an empty list when no Raaja yoga is present: magnitude is a
    grading of a yoga that already exists.
    """
    if data.lagna_rasi is None:
        return []
    kendras, trikonas = kendra_lords(data), trikona_lords(data)
    seen: set[tuple[int, int]] = set()
    out: list[PairMagnitude] = []
    for quadrant_lord in sorted(kendras):
        for trine_lord in sorted(trikonas):
            kind = association(data, quadrant_lord, trine_lord)
            if kind is None:
                continue
            pair = (min(quadrant_lord, trine_lord), max(quadrant_lord, trine_lord))
            if pair in seen:
                continue
            seen.add(pair)

            orb, orb_detail = _orb(data, quadrant_lord, trine_lord, kind)
            close: bool | None = None
            if orb is not None:
                close = orb <= RAAJA_CLOSE_ORB_DEGREES
                orb_detail += (f"; section 11.7.2 asks for “within 6° or "
                               f"so”, which this "
                               f"{'meets' if close else 'does not meet'}")

            blemish_verdicts = [_blemishes(data, g) for g in pair]
            blemish_ok: bool | None
            if any(v is False for v, _ in blemish_verdicts):
                blemish_ok = False
            elif any(v is None for v, _ in blemish_verdicts):
                blemish_ok = None
            else:
                blemish_ok = True

            factors = (
                Factor("unafflicted", None,
                       ("section 11.7.2 asks that the two planets be free "
                        "from afflictions from functional malefics. Nothing "
                        "read so far defines a functional malefic, so this "
                        "factor is not assessed — see docs/open-items.md "
                        "OI-88")),
                Factor("close", close, orb_detail),
                Factor("unblemished", blemish_ok,
                       " | ".join(detail for _, detail in blemish_verdicts)),
            )
            out.append(PairMagnitude(
                quadrant_lord=quadrant_lord,
                quadrant_lord_name=str(GRAHA_NAMES[quadrant_lord]),
                quadrant_houses=kendras[quadrant_lord],
                trine_lord=trine_lord,
                trine_lord_name=str(GRAHA_NAMES[trine_lord]),
                trine_houses=trikonas[trine_lord],
                association=kind,
                orb_degrees=orb,
                factors=factors,
                amsa=_amsa(data, quadrant_lord, trine_lord),
            ))
    return out


def dharma_karmadhipati_pair(data: YogaInput) -> tuple[int, int] | None:
    """The 9th and 10th lords, when they are two planets. §11.7.2's example
    grades this pair in particular."""
    if data.lagna_rasi is None:
        return None
    ninth, tenth = lord_of_house(data, 9), lord_of_house(data, 10)
    return None if ninth == tenth else (ninth, tenth)
