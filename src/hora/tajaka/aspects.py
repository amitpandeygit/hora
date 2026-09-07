"""§28.2 — the Tajaka aspects, and deeptamsa.

This is the third aspect system in the book and it is not built from the other
two. Chapter 10's **graha drishti** gives each planet its own houses; §26.5's
**nakshatra drishti** gives each planet its own constellations; §28.2 gives all
seven planets the same six aspects, distinguished by house distance alone. It
is the western scheme by another name, and footnote 79 says so and adds a
caution: "the exact meaning and use of these special aspects needs to be
further researched ... The current understanding of scholars may be
incomplete."

The system is also the first in the book to call a **conjunction malefic**, and
it leaves the 6th and 8th houses without any aspect at all. Both are recorded
rather than smoothed over.
"""
from __future__ import annotations

from hora.core import validate
from hora.core.const import GRAHA_NAMES, RASI_NAMES

TAJAKA_ASPECTS_INTRO = "In Tajaka analysis, we consider the following aspects:"

#: §28.2's six aspects, in its own order and words. ``houses`` are counted
#: from the aspecting planet inclusively, so 1 is its own house.
TAJAKA_ASPECTS: tuple[dict[str, object], ...] = (
    {"name": "Trinal aspect", "houses": (5, 9), "nature": "benefic",
     "strength": "strong", "degrees": 120,
     "text": ("A planet has a strong benefic aspect on the 5th and 9th "
              "houses from it and on the planets in those houses.")},
    {"name": "Sextile aspect", "houses": (3, 11), "nature": "benefic",
     "strength": "weak", "degrees": 60,
     "text": ("A planet has a weak benefic aspect on the 3rd and 11th "
              "houses from it and on the planets in those houses.")},
    {"name": "Square aspect", "houses": (4, 10), "nature": "malefic",
     "strength": "weak", "degrees": 90,
     "text": ("A planet has a weak malefic aspect on the 4th and 10th "
              "houses from it and on the planets in those houses.")},
    {"name": "Conjunction", "houses": (1,), "nature": "malefic",
     "strength": "strong", "degrees": 0,
     "text": ("A planet has a strong malefic aspect on the planets in the "
              "same house occupied by it.")},
    {"name": "Opposition", "houses": (7,), "nature": "malefic",
     "strength": "strong", "degrees": 180,
     "text": ("A planet has a strong malefic aspect on the 7th house from it "
              "and on the planets in that house.")},
    {"name": "Semi-sextile aspect", "houses": (2, 12), "nature": "neutral",
     "strength": "neutral", "degrees": 30,
     "text": ("A planet has a neutral aspect on the 2nd and 12th houses from "
              "it and on the planets in those houses.")},
)

DEEPTAMSA_MEANS = "the orb of an aspect"

DEEPTAMSA_RULE = (
    "Deeptamsa is \"the orb of an aspect\". Deeptamsas of planets: Sun – 15°, "
    "Moon – 12°, Mars – 8°, Mercury – 7°, Jupiter – 9°, Venus – 7°, Saturn – "
    "9°. If Venus is at 13° in Li, he will have a trinal aspect on Ge, but "
    "his aspect doesn't cover the entire rasi. Venusian aspect covers an "
    "angle of 7° from 13° in Gemini mainly, though Venus may have a moderate "
    "aspectual influence on the entire rasi. So Venus mainly influences 6°–"
    "20° in Ge by aspect. Deeptamsa is the same for all kinds of aspects.")

#: Deeptamsa in degrees, by graha id. The nodes are not given one.
DEEPTAMSA: dict[int, float] = {
    0: 15.0,   # Sun
    1: 12.0,   # Moon
    2: 8.0,    # Mars
    3: 7.0,    # Mercury
    4: 9.0,    # Jupiter
    5: 7.0,    # Venus
    6: 9.0,    # Saturn
}

FOOTNOTE_79 = (
    "These aspects are similar to the ones used in western astrology. "
    "Considering that graha and rasi aspects were mentioned by maharshis, the "
    "exact meaning and use of these special aspects needs to be further "
    "researched and correctly understood. The current understanding of "
    "scholars may be incomplete. Rishi prokta (words spoken by great sages) "
    "should form the basis of our knowledge.")

#: **Finding.** The six aspects reach ten houses and leave the **6th and 8th**
#: untouched. Those are the two at 150° — western astrology's quincunx — so
#: the omission is one named western aspect and not an oversight of shape:
#: every other multiple of 30° up to 180° is here. Nothing is invented for
#: them, and `aspect_on_house` returns None rather than a nature.
THE_SIXTH_AND_EIGHTH_RECEIVE_NO_ASPECT = (
    "Section 28.2's six aspects cover the 1st, 2nd, 3rd, 4th, 5th, 7th, 9th, "
    "10th, 11th and 12th houses. The 6th and 8th — the two at 150 degrees, "
    "which western astrology calls the quincunx — get none."
)

#: **Finding.** This is the first place in the book where a **conjunction is
#: malefic**, and strongly so. Chapter 10 treats conjunction as association
#: whose nature follows the planets; §11.7.1 counts it as one of the three
#: ways a Raaja Yoga forms. Here it is graded with opposition, and both are
#: "strong malefic". So a Tajaka reading of a conjunction cannot be carried
#: over from a natal one.
THE_CONJUNCTION_IS_MALEFIC_HERE_AND_NOWHERE_ELSE = (
    "Section 28.2 makes a conjunction a strong malefic aspect, alongside the "
    "opposition. Everywhere else in the book a conjunction is an association "
    "whose nature comes from the planets in it."
)

#: **Finding.** Deeptamsa is per **planet**, not per aspect — the section says
#: so in its last sentence — so one orb serves all six. It is also a
#: half-width: Venus's 7° around 13° gives 6° to 20°, which is the section's
#: own arithmetic and a fourteen-degree span.
THE_ORB_IS_PER_PLANET_AND_IS_A_HALF_WIDTH = (
    "Deeptamsa is the same for all kinds of aspects, and it is measured "
    "either side of the exact aspect point: Venus's seven degrees around "
    "13 Ge is 6 to 20 Ge."
)

#: **Finding.** No deeptamsa is given for **Rahu or Ketu**, so a Tajaka aspect
#: cannot be bounded for them. §26.5's nakshatra drishti left the nodes out in
#: the same way. `deeptamsa` refuses them rather than borrowing a value.
THE_NODES_HAVE_NO_DEEPTAMSA = (
    "Section 28.2 lists deeptamsas for the seven classical planets only. The "
    "nodes are not given one, exactly as section 26.5 gave them no nakshatra "
    "aspects."
)

#: **Finding.** Three aspect systems now, none derived from another. Chapter
#: 10's graha drishti is per planet and asymmetric; §26.5's nakshatra drishti
#: is per planet and counted in constellations; §28.2's is uniform across the
#: seven and counted in houses. A planet can therefore aspect a rasi in one
#: system and not in another, and the book never reconciles them.
THREE_ASPECT_SYSTEMS_AND_NO_RECONCILIATION = (
    "Graha drishti gives each planet its own houses, nakshatra drishti gives "
    "each its own constellations, and the Tajaka aspects give all seven the "
    "same six. The book states no rule for using them together."
)


class TajakaAspectError(validate.InputError):
    """A Tajaka aspect input that cannot be resolved."""


def aspect_on_house(house: int) -> dict | None:
    """Which of §28.2's aspects falls on the `house`-th house from a planet.

    :param house: 1 to 12, counted inclusively from the aspecting planet.
    :returns: the aspect, or ``None`` for the 6th and 8th, which the section
        gives no aspect at all.
    """
    index = validate.in_range("house", int(house), 1, 12)
    for aspect in TAJAKA_ASPECTS:
        houses = aspect["houses"]
        assert isinstance(houses, tuple)
        if index in houses:
            return dict(aspect)
    return None


def aspects_from(rasi: int) -> tuple[dict, ...]:
    """Every rasi a planet in `rasi` aspects, with the aspect on each."""
    index = validate.in_range("rasi", int(rasi), 0, 11)
    out = []
    for house in range(1, 13):
        aspect = aspect_on_house(house)
        if aspect is None:
            continue
        target = (index + house - 1) % 12
        out.append({
            "house": house,
            "rasi": target,
            "rasi_name": str(RASI_NAMES[target]),
            "aspect": aspect["name"],
            "nature": aspect["nature"],
            "strength": aspect["strength"],
            "degrees": aspect["degrees"],
        })
    return tuple(out)


def deeptamsa(graha: int) -> float:
    """A graha's orb in degrees, the same for all six aspects.

    :raises TajakaAspectError: for Rahu, Ketu or anything else §28.2 does not
        list, rather than borrowing a value from a neighbour.
    """
    index = validate.in_range("graha", int(graha), 0, 8)
    if index not in DEEPTAMSA:
        raise TajakaAspectError(
            f"section 28.2 gives no deeptamsa for {GRAHA_NAMES[index]}; "
            f"{THE_NODES_HAVE_NO_DEEPTAMSA}")
    return DEEPTAMSA[index]


def aspect_span(graha: int, longitude: float, house: int) -> dict:
    """Where a graha's aspect on the `house`-th house from it mainly falls.

    §28.2's own example: Venus at 13 Li has a trinal aspect on Gemini, and
    with a deeptamsa of 7° he "mainly influences 6°-20° in Ge".

    :returns: the exact aspect point, the orb, and the span it covers, or
        ``aspect`` ``None`` for the two houses the section leaves out.
    """
    aspect = aspect_on_house(house)
    orb = deeptamsa(graha)
    place = validate.longitude("longitude", float(longitude))
    if aspect is None:
        return {
            "graha": int(graha), "house": int(house), "aspect": None,
            "deeptamsa": orb, "exact": None, "from": None, "to": None,
            "reason": THE_SIXTH_AND_EIGHTH_RECEIVE_NO_ASPECT,
        }
    exact = (place + 30.0 * (int(house) - 1)) % 360.0
    return {
        "graha": int(graha),
        "graha_name": str(GRAHA_NAMES[int(graha)]),
        "house": int(house),
        "aspect": aspect["name"],
        "nature": aspect["nature"],
        "strength": aspect["strength"],
        "deeptamsa": orb,
        "exact": exact,
        "exact_rasi": str(RASI_NAMES[int(exact // 30)]),
        "from": (exact - orb) % 360.0,
        "to": (exact + orb) % 360.0,
        "whole_rasi_note": (
            "Section 28.2 allows that the planet \"may have a moderate "
            "aspectual influence on the entire rasi\" outside this span, and "
            "gives no strength for it."),
        "reason": None,
    }
