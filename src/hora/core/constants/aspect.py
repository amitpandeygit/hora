"""Aspects — book chapter 10.

§10.1: "Planets aspect other planets, rasis and houses in astrology." Two
kinds, and the chapter separates them at the outset:

* **graha drishti** (planetary aspect) — each graha aspects certain houses
  *counted from itself*, and the houses are fixed per graha;
* **rasi drishti** (sign aspect) — rasis aspect each other, and a graha
  inherits the aspects of the rasi it occupies.

Import from :mod:`hora.core.const`, which re-exports every constant.
"""
from __future__ import annotations

from hora.core.constants.graha import Graha

#: §10.2's heading is printed "Graha Drishri". Every other use in the chapter,
#: including §10.1's own sentence, spells it "drishti". Recorded so the typo is
#: not mistaken for a term.
GRAHA_DRISHTI_HEADING_AS_PRINTED = "Graha Drishri"
DRISHTI_MEANS = "aspect"

#: §10.1, in full.
ASPECT_DEFINITION = (
    "Planets aspect other planets, rasis and houses in astrology. A planet "
    "aspecting a house or a planet has some influence on the matters signified "
    "by that house or planet. The nature of the influence exerted and the "
    "degree to which that influence succeeds depends on the individual "
    "situation."
)

#: The two kinds, with what §10.1 says distinguishes them.
ASPECT_KINDS: dict[str, dict] = {
    "graha_drishti": {
        "name": "graha drishti",
        "gloss": "planetary aspect",
        "rule": (
            "Each planet aspects certain houses from it with graha drishti. "
            "The houses aspected are fixed based on the planet."
        ),
        "counted_from": "the graha",
        "varies_by": "graha",
    },
    "rasi_drishti": {
        "name": "rasi drishti",
        "gloss": "sign aspect",
        "rule": (
            "Rasis aspect each other and a planet aspects the rasis aspected "
            "by the rasi occupied by it."
        ),
        "counted_from": "the rasi occupied",
        "varies_by": "rasi",
    },
}

#: §10.2's universal rule, stated before any exception.
SEVENTH_HOUSE_RULE = (
    "All planets aspect the 7th house from them. Find the 7th house from the "
    "planet and the planet aspects that house."
)

#: §10.2's five worked one-liners for the 7th-house rule.
SEVENTH_HOUSE_EXAMPLES: tuple[tuple[int, int, int], ...] = (
    (Graha.SUN, 1, 7),        # Sun in Ta aspects Sc
    (Graha.MARS, 2, 8),       # Mars in Ge aspects Sg
    (Graha.MOON, 4, 10),      # Moon in Le aspects Aq
    (Graha.JUPITER, 11, 5),   # Jupiter in Pi aspects Vi
    (Graha.SATURN, 9, 3),     # Saturn in Cp aspects Cn
)

#: §10.2: "In addition, Mars, Jupiter and Saturn have special aspects."
#: Exactly three grahas, and the chapter names no others.
SPECIAL_ASPECT_GRAHAS: tuple[int, ...] = (Graha.MARS, Graha.JUPITER, Graha.SATURN)
SPECIAL_ASPECT_RULE = "In addition, Mars, Jupiter and Saturn have special aspects."

#: The three bullets, in the chapter's own order — Jupiter, Mars, Saturn.
SPECIAL_ASPECT_BULLETS: tuple[dict, ...] = (
    {"graha": Graha.JUPITER, "houses": (5, 9),
     "text": "Jupiter aspects the 5th and 9th houses from him, in addition to "
             "the 7th house."},
    {"graha": Graha.MARS, "houses": (4, 8),
     "text": "Mars aspects the 4th and 8th houses from him, in addition to the "
             "7th house."},
    {"graha": Graha.SATURN, "houses": (3, 10),
     "text": "Saturn aspects the 3rd and 10th houses from him, in addition to "
             "the 7th house."},
)

#: §10.2's rule for turning aspected houses into aspected planets. A graha is
#: aspected because of *where it sits*, never in its own right.
ASPECTED_PLANET_RULE = (
    "We can decide the signs and houses aspected by a planet as above. If any "
    "planet occupies the aspected houses, then the planet is also aspected."
)
ASPECTED_PLANET_EXAMPLE = (
    "Jupiter in Ta will aspect Saturn in Cp, because Cp is the 9th house from "
    "Ta and Jupiter aspects the 9th from him."
)

#: §10.2 closes by telling the reader to practise on charts rather than giving
#: another rule. Recorded because it is the chapter's own statement of what the
#: computation is for.
ASPECTS_ARE_A_SKILL_NOTE = (
    "Look at a few charts and figure out which planets are aspecting which "
    "houses and which planets are aspecting which planets. With experience, "
    "you can become good at it and this is an important skill required in "
    "interpreting charts."
)
