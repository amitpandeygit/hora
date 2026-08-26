"""House service — chapter 7.

Houses are relative twice over: a rasi is a house only with respect to a
reference, and a category is a category only with respect to a house. Both
relativities are exposed, because collapsing either into "from the lagna" is
what makes house analysis wrong in subtle ways.

Callable without a nativity: give it a reference rasi and some target rasis.
"""
from __future__ import annotations

import re

from hora.charts.arudha import arudha_pada
from hora.charts.house import (
    categories_of,
    category_houses,
    graha_lagna_houses,
    half_of,
    house_of_rasi,
    karakamsa_rasi,
    paaka_lagna_rasi,
    purushartha_of,
    rasi_of_house,
    signification,
)
from hora.charts.vargas import VARGA_SIGNIFICATIONS
from hora.core import const as c
from hora.core import validate
from hora.core.const import (
    GRAHA_NAMES,
    HOUSE_CATEGORIES,
    HOUSE_REFERENCES,
    HOUSE_SIGNIFICATIONS,
    INVISIBLE_HALF,
    NAVAGRAHA,
    PURUSHARTHA_TRIKONAS,
    RASI_LORD,
    RASI_NAMES,
    VISIBLE_HALF,
)
from hora.services import reference_service

InputError = validate.InputError

__all__ = [
    "InputError", "categories", "houses_from_reference", "references", "rules",
]


def _house_out(house: int, rasi: int) -> dict:
    return {
        "house": house,
        "rasi": rasi,
        "rasi_name": RASI_NAMES[rasi],
        "lord": int(RASI_LORD[rasi]),
        "lord_name": GRAHA_NAMES[RASI_LORD[rasi]],
        "categories": categories_of(house),
        "purushartha": purushartha_of(house),
        "half": half_of(house),
        "signifies": signification(house),
    }


def houses_from_reference(reference_rasi: int, reference: str = "lagna") -> dict:
    """All twelve houses counted from a reference rasi."""
    validate.in_range("reference_rasi", reference_rasi, 0, 11)
    if reference not in HOUSE_REFERENCES:
        raise InputError(
            f"unknown reference {reference!r}; expected one of "
            f"{', '.join(sorted(HOUSE_REFERENCES))}"
        )
    return {
        "reference": reference,
        "reference_name": HOUSE_REFERENCES[reference]["name"],
        "reference_rasi": reference_rasi,
        "reference_rasi_name": RASI_NAMES[reference_rasi],
        "shows": HOUSE_REFERENCES[reference]["shows"],
        "houses": [
            _house_out(h, rasi_of_house(reference_rasi, h)) for h in range(1, 13)
        ],
    }


def references(
    *,
    lagna_rasi: int,
    graha_rasis: dict[int, int],
    ghati_lagna_rasi: int | None = None,
    hora_lagna_rasi: int | None = None,
    graha_longitudes: dict[int, float] | None = None,
) -> dict:
    """Every reference of §7.3 that can be computed from what was supplied.

    A reference whose inputs are missing, or that needs a later chapter, is
    reported as unavailable with the reason — never silently dropped.
    """
    from hora.core.const import Graha

    validate.in_range("lagna_rasi", lagna_rasi, 0, 11)
    for graha, graha_rasi in graha_rasis.items():
        validate.in_range(f"graha_rasis[{graha}]", graha_rasi, 0, 11)

    resolved: dict[str, int | None] = {"lagna": lagna_rasi}
    reasons: dict[str, str] = {}

    for key, graha in (("chandra_lagna", Graha.MOON), ("ravi_lagna", Graha.SUN)):
        if int(graha) in graha_rasis:
            resolved[key] = graha_rasis[int(graha)]
        else:
            reasons[key] = f"needs the rasi of {GRAHA_NAMES[graha]}"

    try:
        resolved["paaka_lagna"] = paaka_lagna_rasi(lagna_rasi, graha_rasis)
    except InputError as exc:
        reasons["paaka_lagna"] = str(exc)

    # §7.3.6 defines karakamsa, so it is computable once longitudes are
    # given: the atma karaka's navamsa rasi.
    if graha_longitudes:
        try:
            resolved["karakamsa_lagna"] = karakamsa_rasi(graha_longitudes)
        except (InputError, KeyError) as exc:
            reasons["karakamsa_lagna"] = str(exc)
    else:
        reasons["karakamsa_lagna"] = (
            "needs graha longitudes, not only rasis: the atma karaka is the "
            "graha of highest advancement within its rasi"
        )

    # §9.2's arudha pada of the 1st house. Scorpio and Aquarius have two lords
    # each, so a chart with the lagna there may need stronger_lord.
    try:
        resolved["arudha_lagna"] = arudha_pada(1, lagna_rasi, graha_rasis).sign
    except (InputError, KeyError) as exc:
        reasons["arudha_lagna"] = str(exc)

    for key, value in (("ghati_lagna", ghati_lagna_rasi), ("hora_lagna", hora_lagna_rasi)):
        if value is None:
            reasons[key] = "supply its rasi, or compute it from chapter 5"
        else:
            resolved[key] = validate.in_range(key, value, 0, 11)

    out = []
    for key, entry in HOUSE_REFERENCES.items():
        rasi: int | None = resolved.get(key)
        out.append({
            "reference": key,
            "name": entry["name"],
            "shows": entry["shows"],
            "available": rasi is not None,
            "rasi": rasi,
            "rasi_name": RASI_NAMES[rasi] if rasi is not None else None,
            "unavailable_because": (
                None if rasi is not None
                else reasons.get(key, entry["note"])
            ),
        })
    return {"lagna_rasi": lagna_rasi, "references": out}


def categories(base_house: int = 1) -> dict:
    """Every category, re-based onto a house.

    §7.4 does exactly this: "the 3rd, 7th and 11th houses are the trines from
    the 3rd house".
    """
    validate.in_range("base_house", base_house, 1, 12)
    return {
        "base_house": base_house,
        "categories": [
            {
                "category": name,
                "synonyms": entry["synonyms"],
                "houses": list(category_houses(name, base_house)),
                "shows": entry["shows"],
                "derivation": entry.get("derivation"),
                "presiding_deity": entry["presiding"],
            }
            for name, entry in HOUSE_CATEGORIES.items()
        ],
        # §7.4.5's split is relative too: "the houses in the visible half of
        # the zodiac with respect to a reference". Re-based here so a caller
        # asking for the categories from a house gets the halves from it too.
        "halves": {
            "visible": [h for h in range(1, 13) if half_of(h, base_house) == "visible"],
            "invisible": [
                h for h in range(1, 13) if half_of(h, base_house) == "invisible"
            ],
        },
    }


#: Ordinary English that would match any pair of signification lists.
_MEANING_STOPWORDS = frozenset({
    "and", "the", "for", "with", "from", "all", "any", "related", "everything",
    "some", "other", "also", "level", "matters", "matter", "etc", "various",
})


def _significant_words(text: str) -> set[str]:
    """Words of a signification list, singularised crudely.

    "house" must match "houses owned" — §7.3's own D-4 case turns on exactly
    that, so a plural-blind comparison would miss it.
    """
    out = set()
    for word in re.split(r"[^a-z]+", text.lower()):
        if len(word) <= 3 or word in _MEANING_STOPWORDS:
            continue
        out.add(word[:-1] if len(word) > 4 and word.endswith("s") else word)
    return out


def meanings_in_varga(house: int, chart: str) -> dict:
    """§7.3 — which of a house's meanings apply in a given divisional chart.

    "We have to note the area of life seen in the divisional chart under
    examination. We have to choose the meanings of houses that are relevant in
    that area of life. For example, the 4th house shows education, vehicle,
    house and mother (among other things)... the 4th houses in D-24, D-16, D-4
    and D-12 show education, vehicle, house and mother (respectively)."

    **This is a hint, not a derivation.** It intersects the house's
    signification with the chart's, so every word it returns is PVR's own. But
    the intersection cannot reach §7.3's fourth case: D-12 signifies "parents"
    and the 4th house signifies "Mother", and *mother is a parent* is world
    knowledge the two tables do not contain. `derivable` says so per call
    rather than presenting a partial answer as complete.
    """
    validate.in_range("house", house, 1, 12)
    if chart not in VARGA_SIGNIFICATIONS:
        raise validate.InputError(
            f"unknown chart {chart!r}; expected one of "
            f"{', '.join(VARGA_SIGNIFICATIONS)}"
        )
    house_words = _significant_words(HOUSE_SIGNIFICATIONS[house])
    chart_words = _significant_words(VARGA_SIGNIFICATIONS[chart])
    shared = sorted(house_words & chart_words)
    return {
        "house": house,
        "chart": chart,
        "house_signifies": HOUSE_SIGNIFICATIONS[house],
        "chart_signifies": VARGA_SIGNIFICATIONS[chart],
        "shared_meanings": shared,
        "derivable": bool(shared),
        "rule": c.CHOOSE_MEANING_BY_VARGA,
        "limitation": (
            "Shared meanings are the literal overlap of the two signification "
            "lists, so every word is the book's own. Where the link is "
            "semantic rather than literal the overlap is empty or partial - "
            "section 7.3's own D-12 case reads the 4th house as 'mother' "
            "because mother is a parent, which the tables do not say. "
            "See open item OI-55."
        ),
    }


def derived(house: int, from_house: int) -> dict:
    """§7.2 — a house counted from another house, with both meanings.

    "We can find houses from houses and concatenate the meanings in some
    places. For example, the 3rd house shows younger brother. The 2nd house
    from the 3rd house is the 4th house (count 1, 2 from 3rd and get 3rd,
    4th). So the 4th house shows the wealth, speech etc of younger brother."

    Note the counting is **inclusive** — the 2nd from the 3rd is the 4th, not
    the 5th, because the 3rd counts as the 1st.
    """
    validate.in_range("house", house, 1, 12)
    validate.in_range("from_house", from_house, 1, 12)
    result = (from_house + house - 2) % 12 + 1
    return {
        "house": house,
        "from_house": from_house,
        "result": result,
        "counting_note": (
            f"count {house} from the {_ordinal(from_house)} inclusive: the "
            f"{_ordinal(from_house)} is the 1st, so the {_ordinal(house)} "
            f"from it is the {_ordinal(result)}"
        ),
        "from_house_signifies": HOUSE_SIGNIFICATIONS[from_house],
        "house_signifies": HOUSE_SIGNIFICATIONS[house],
        "result_signifies": HOUSE_SIGNIFICATIONS[result],
        "concatenation": (
            f"the {_ordinal(result)} house shows the matters of the "
            f"{_ordinal(house)} house for the matters of the "
            f"{_ordinal(from_house)} house"
        ),
        "rule": c.HOUSES_FROM_HOUSES_RULE,
    }


def _ordinal(n: int) -> str:
    if 11 <= n % 100 <= 13:
        return f"{n}th"
    return f"{n}{ {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th') }".replace(" ", "")


def rules() -> dict:
    """The chapter as data: significations, categories, purusharthas, Table 12.

    Opens with section 1.3.3's definition, because that is where a house is
    said to be a rasi counted from a reference and where the default reference
    is fixed.
    """
    return {
        "definition": reference_service.house_definition(),
        "significations": [
            {"house": h, "signifies": HOUSE_SIGNIFICATIONS[h],
             "purushartha": purushartha_of(h), "half": half_of(h)}
            for h in range(1, 13)
        ],
        "categories": categories(1)["categories"],
        "purusharthas": [
            {"purushartha": name, "houses": list(entry["houses"]),
             "meaning": entry["meaning"]}
            for name, entry in PURUSHARTHA_TRIKONAS.items()
        ],
        "halves": {"visible": list(VISIBLE_HALF), "invisible": list(INVISIBLE_HALF)},
        "graha_lagnas": [
            {"graha": int(g), "graha_name": GRAHA_NAMES[g],
             "houses": list(graha_lagna_houses(g))}
            for g in NAVAGRAHA if graha_lagna_houses(g)
        ],
        "references": [
            {"reference": k, "name": v["name"], "shows": v["shows"],
             "available": v["available"], "note": v["note"]}
            for k, v in HOUSE_REFERENCES.items()
        ],
        "note": (
            "A house never spans two rasis. Section 7.5 rejects bhava chalit, "
            "equal-house and Sripathi division outright: 'Each rasi is a house.' "
            "That is why the engine's default house_system is whole_sign."
        ),
    }


def house_of(reference_rasi: int, target_rasi: int) -> int:
    """Which house a rasi is, from a reference. Exposed for direct use."""
    return house_of_rasi(reference_rasi, target_rasi)
