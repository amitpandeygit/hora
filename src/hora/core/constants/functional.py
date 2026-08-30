"""Chapter 13 — interpreting charts.

Section 13.2's functional nature. Table 30 is transcribed as data and is the
authority: §13.2 says planets owning two rasis need their two indications
"judiciously combined" and then prints the result, so the table is PVR's
output and not something the stated rules determine. The rules are held
separately in `charts.functional` and checked against the table, which names
exactly where judgement was exercised.
"""
from __future__ import annotations

CHAPTER_13_INTRO = (
    "In the previous chapters, we have learnt various parameters and tools "
    "available in Vedic astrology. When it comes to putting them all together "
    "and interpreting charts, there is no substitute for experience. One "
    "should also refer to classics and “How to Judge a Horoscope” (Vols I & "
    "II) by Dr. B.V. Raman, to become familiar with the standard results "
    "attributed to different planets being in different houses and the lords "
    "of different houses being in various houses. In this chapter, we will "
    "cover some topics not covered yet and go through a couple of examples of "
    "interpreting charts. We will see many more examples in the rest of this "
    "book.")

#: The one outside reference chapter 13 names. Not a source we consume.
RAMAN_REFERENCE = (
    "“How to Judge a Horoscope” (Vols I & II) by Dr. B.V. Raman")

FUNCTIONAL_NATURE_INTRO = (
    "We learnt that Jupiter, Venus, waxing Moon and well-associated Mercury "
    "are natural benefics. We learnt that Sun, Mars, Saturn, Rahu, Ketu, "
    "waning Moon and ill-associated Mercury are natural malefics. In "
    "addition, we have the concept of functional benefics and functional "
    "malefics.")

#: §13.2's boxed rules, verbatim and in order.
FUNCTIONAL_NATURE_RULES: tuple[str, ...] = (
    "The lords of trines from lagna are functional benefics.",
    "The lords of 3rd, 6th and 11th are functional malefics.",
    (
        "The lord of a quadrant is a functional malefic if he is a natural "
        "benefic and functionally neutral if he is a natural malefic."
    ),
    (
        "The lords of 2nd, 8th and 12th are functionally neutral. Of these, "
        "the 8th house is more malefic than the other two."
    ),
    (
        "Planet owning a quadrant and a trine becomes a yogakaraka "
        "(excellent planet)."
    ),
)

TWO_RASI_OWNERS_NEED_JUDGEMENT = (
    "In the case of planets owning two rasis, we need to judiciously combine "
    "the two indications.")

MOON_NOT_LISTED_FOR_MOVABLE = (
    "Moon is not listed for movable rasis, because his functional nature "
    "depends on whether he is waxing or waning. Waxing Moon is a natural "
    "benefic and he becomes a functional malefic with quadrant ownership. "
    "Waning Moon, on the other hand, is a natural malefic and quadrant "
    "ownership makes him functionally neutral.")

#: Table 30. ``lagna -> (yogakaraka, benefics, neutrals, malefics)``. Moon is
#: absent from Aries, Libra and Capricorn — see `MOON_NOT_LISTED_FOR_MOVABLE`.
TABLE_30_FUNCTIONAL_NATURE: dict[
        str, tuple[str | None, tuple[str, ...], tuple[str, ...],
                   tuple[str, ...]]] = {
    "Ar": (None, ("Sun", "Mars", "Jupiter"), (),
           ("Mercury", "Venus", "Saturn")),
    "Ta": ("Saturn", ("Sun", "Mercury", "Saturn"), ("Mars",),
           ("Moon", "Jupiter", "Venus")),
    "Ge": (None, ("Venus",), ("Moon", "Mercury", "Saturn"),
           ("Sun", "Mars", "Jupiter")),
    "Cn": ("Mars", ("Moon", "Mars", "Jupiter"), ("Sun", "Saturn"),
           ("Mercury", "Venus")),
    "Le": ("Mars", ("Sun", "Mars", "Jupiter"), ("Moon",),
           ("Mercury", "Venus", "Saturn")),
    "Vi": (None, ("Mercury", "Venus"), ("Sun", "Saturn"),
           ("Moon", "Mars", "Jupiter")),
    "Li": ("Saturn", ("Mercury", "Venus", "Saturn"), (),
           ("Sun", "Mars", "Jupiter")),
    "Sc": (None, ("Moon", "Jupiter"), ("Sun", "Mars"),
           ("Mercury", "Venus", "Saturn")),
    "Sg": (None, ("Sun", "Mars"), ("Moon", "Mercury", "Jupiter"),
           ("Venus", "Saturn")),
    "Cp": ("Venus", ("Venus", "Mercury", "Saturn"), ("Sun",),
           ("Mars", "Jupiter")),
    "Aq": ("Venus", ("Venus", "Saturn"), ("Sun", "Mercury"),
           ("Moon", "Mars", "Jupiter")),
    "Pi": (None, ("Moon", "Mars"), ("Jupiter",),
           ("Sun", "Mercury", "Venus", "Saturn")),
}

#: The three lagnas Table 30 leaves the Moon out of. In each, Moon owns a
#: quadrant, so `MOON_NOT_LISTED_FOR_MOVABLE`'s two branches decide him.
MOON_OMITTED_FROM = ("Ar", "Li", "Cp")

#: Cancer is movable too and Moon *is* listed there, because Cancer's Moon
#: owns the 1st. §13.2's "movable rasis" is therefore a shade loose — the real
#: condition is owning a quadrant **other than the 1st**. That Cancer is the
#: exception is itself the proof that the 1st counts as a trine here and not
#: as a quadrant. See docs/book-deviations.md D-45.
MOON_MOVABLE_WORDING = (
    "Section 13.2 says Moon is not listed for movable rasis, but Cancer is "
    "movable and Table 30 does list him there, as a functional benefic. The "
    "condition that actually holds is owning a quadrant other than the 1st, "
    "which for Cancer's Moon is true of Aries, Libra and Capricorn only. "
    "Cancer being the exception is what proves the 1st is treated as a trine "
    "and not as a quadrant.")

PLACEMENT_RULE = (
    "A functional benefic is a favorable planet in a chart. Placement of a "
    "functional benefic in quadrants (sustenance) and trines (prosperity) "
    "brings good results. Placement of a functional malefic in these houses "
    "is not good, unless it is very strong. A functional malefic placed in "
    "the 3rd house and dusthanas (6th, 8th and 12th houses) brings good "
    "results, by spoiling the significations of the bad houses.")

YOGADA_RULE = (
    "If a planet aspects or conjoins or owns HL and lagna, it becomes a "
    "yogada (giver of yoga) in money matters. If a planet aspects or conjoins "
    "or owns GL and lagna, it becomes a yogada in the matters of power and "
    "authority. Irrespective of their functional nature, planets that become "
    "yogada bring goodluck. Similarly, planets involved in important yogas "
    "also bring good luck.")

#: The two yogadas and what each governs.
YOGADA_KINDS: dict[str, str] = {
    "HL": "money matters",
    "GL": "the matters of power and authority",
}

#: The three ways a planet can be tied to a special lagna for yogada.
YOGADA_LINKS = ("aspects", "conjoins", "owns")

NATURAL_VERSUS_FUNCTIONAL = (
    "We should consider the inherent nature and the functional nature of "
    "planets. Whether a planet is a natural benefic or a natural malefic is "
    "analogous to whether a person is inherently good or bad. Whether a "
    "planet is a functional benefic or a functional malefic is analogous to "
    "whether a person does good or bad to one. Just as a nice person may harm "
    "one and a bad person may do good, natural benefics can become functional "
    "malefics and natural malefics can become functional benefics.")
