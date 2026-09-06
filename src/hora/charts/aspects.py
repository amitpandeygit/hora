"""Drishti — Parashari sign aspects and planetary aspects."""
from __future__ import annotations

from hora.core.const import RASI_MODALITY, SPECIAL_ASPECTS, Graha

#: Jaimini rasi drishti, as 0-based sign offsets.
#:
#: A movable rasi aspects the fixed rasis other than the one next to it; a
#: fixed rasi aspects the movable rasis other than the one before it; a dual
#: rasi aspects the other three dual rasis.
#:
#: **Corrected 2026-08-26.** These were previously ``{0: (4, 6, 8),
#: 1: (2, 4, 10), 2: (2, 6, 10)}``, which is wrong in all three rows: each sent
#: a rasi to targets of the wrong modality, and Leo did not aspect Aries, which
#: section 15.5.1's own worked example requires. See docs/open-items.md OI-27.
_RASI_DRISHTI_OFFSETS = {
    0: (4, 7, 10),   # movable -> the fixed rasis, except the next one
    1: (2, 5, 8),    # fixed -> the movable rasis, except the previous one
    2: (3, 6, 9),    # dual -> the other three dual rasis
}

#: Which modality a rasi of each modality aspects. Movable and fixed aspect
#: each other; dual aspects only dual.
_ASPECTED_MODALITY = {0: 1, 1: 0, 2: 2}


def rasi_drishti(sign: int) -> tuple[int, ...]:
    """Signs aspected by a sign under Jaimini's rasi drishti.

    Aspects are mutual: if A aspects B then B aspects A. No sign aspects
    itself. Both properties are asserted in
    ``tests/unit/test_rasi_drishti.py``.
    """
    return tuple((sign + o) % 12 for o in _RASI_DRISHTI_OFFSETS[RASI_MODALITY[sign]])


def graha_drishti_houses(graha: int, *, rahu_ketu_aspects: bool = False) -> tuple[int, ...]:
    """Houses (counted from the graha, 1-based) that a graha aspects fully."""
    if graha in (Graha.RAHU, Graha.KETU) and not rahu_ketu_aspects:
        return (7,)
    extra = SPECIAL_ASPECTS.get(graha, ())
    return tuple(sorted({7, *extra}))


def graha_aspects_sign(graha: int, graha_sign: int, target_sign: int, *, rahu_ketu_aspects: bool = False) -> bool:
    """Whether a graha in ``graha_sign`` casts a full aspect on ``target_sign``."""
    house = (target_sign - graha_sign) % 12 + 1
    return house in graha_drishti_houses(graha, rahu_ketu_aspects=rahu_ketu_aspects)


#: Parashari partial-aspect table (virupas out of 60) by house distance.
#: Index is the house counted from the graha, 1-based.
_PARTIAL: dict[int, dict[int, int]] = {
    Graha.MARS:    {4: 60, 7: 60, 8: 60, 5: 15, 9: 15, 3: 30, 10: 30},
    Graha.JUPITER: {5: 60, 7: 60, 9: 60, 4: 15, 8: 15, 3: 30, 10: 30},
    Graha.SATURN:  {3: 60, 7: 60, 10: 60, 4: 15, 8: 15, 5: 30, 9: 30},
}
_PARTIAL_DEFAULT = {7: 60, 4: 15, 8: 15, 5: 30, 9: 30, 3: 30, 10: 30}


def drishti_value(graha: int, from_sign: int, to_sign: int) -> int:
    """Aspect strength in virupas (0-60), used by drik bala and ashtakavarga."""
    house = (to_sign - from_sign) % 12 + 1
    table = _PARTIAL.get(graha, _PARTIAL_DEFAULT)
    return table.get(house, 0)


# --------------------------------------------------------------------------
# §26.5 — nakshatra-based aspects
# --------------------------------------------------------------------------
# A third drishti scheme, kept beside the other two because that is where a
# reader looks for aspects. Chapter 26 introduces it while discussing
# transits, but nothing in the rule is transit-specific.

#: Nakshatras aspected, counted inclusively from the graha's own — so 1 means
#: the nakshatra it occupies. §26.5 gives no rule for Rahu and Ketu.
NAKSHATRA_DRISHTI: dict[int, tuple[int, ...]] = {
    int(Graha.SUN): (14, 15),
    int(Graha.MOON): (14, 15),
    int(Graha.MARS): (1, 3, 7, 8, 15),
    int(Graha.MERCURY): (1, 15),
    int(Graha.JUPITER): (10, 15, 19),
    int(Graha.VENUS): (1, 15),
    int(Graha.SATURN): (3, 5, 15, 19),
}

NAKSHATRA_DRISHTI_RULE = (
    "Sun and Moon aspect the 14th and 15th constellations from them. Mars "
    "aspects the 1st, 3rd, 7th, 8th and 15th constellations from him. "
    "Mercury and Venus aspect the 1st and 15th constellations from them. "
    "Jupiter aspects the 10th, 15th and 19th constellations from him. Saturn "
    "aspects the 3rd, 5th, 15th and 19th constellations from him.")

NAKSHATRA_DRISHTI_RESULTS = (
    "A natural benefic gives good results related to the constellations "
    "aspected by it and a natural malefic gives bad results related to the "
    "constellations aspected by it.")

#: **Finding.** Every graha aspects the **15th**, which is this scheme's
#: version of every graha aspecting the 7th house. The reason is exact: 180°
#: from the *middle* of a nakshatra lands precisely on the boundary between
#: the 14th and the 15th from it, 13.5 nakshatras being half of 27. So the
#: 14th and 15th are the two that meet at the opposition, and the luminaries
#: alone take both while everyone else takes the later one.
EVERY_GRAHA_ASPECTS_THE_FIFTEENTH = (
    "All seven lists contain the 15th. Half of 27 is 13.5, so 180 degrees "
    "from the midpoint of a nakshatra falls exactly on the join between the "
    "14th and the 15th from it; the Sun and Moon aspect both sides of that "
    "join and the other five take the 15th only."
)

#: **Finding.** Mars, Mercury and Venus aspect the **1st** — their own
#: nakshatra — which has no counterpart in graha drishti, where a graha never
#: aspects the house it stands in. So the two schemes are not the same rule
#: rescaled.
THREE_GRAHAS_ASPECT_THEIR_OWN_NAKSHATRA = (
    "Mars, Mercury and Venus aspect the 1st constellation from themselves. "
    "No graha aspects its own house under graha drishti, so this has no "
    "counterpart there."
)

#: **Finding.** The ranking survives the change of scheme. The three grahas
#: §10.2 gives special rasi aspects — Mars, Jupiter and Saturn — are exactly
#: the three that aspect more than two nakshatras here, and Mars leads in
#: both. The lists themselves do not correspond, so it is the ordering that
#: carries over, not the offsets.
THE_SAME_THREE_GRAHAS_ASPECT_MOST_IN_BOTH_SCHEMES = (
    "Mars aspects five nakshatras, Saturn four and Jupiter three; the Sun, "
    "Moon, Mercury and Venus aspect two each. Those first three are the "
    "grahas with special aspects in section 10.2, and Mars leads there too."
)

#: **Finding.** Jupiter's 10th and 19th are the other two nakshatras of his
#: own Vimsottari triple — §25.6 proved a nakshatra shares its lord with the
#: 10th and 19th from it. So Jupiter aspects, wherever he stands, the rest of
#: the holding his nakshatra belongs to. Saturn takes the 19th but not the
#: 10th, which the book states without explanation and is left as printed.
JUPITER_ASPECTS_HIS_OWN_VIMSOTTARI_TRIPLE = (
    "The 10th and 19th from a nakshatra are the two that share its "
    "Vimsottari lord, so Jupiter's aspects fall on the rest of his own "
    "nakshatra's holding. Saturn aspects the 19th alone of that pair."
)

#: **Gap.** §26.5 lists seven grahas. Neither node is given a nakshatra
#: aspect, and the section does not say whether they have none or are simply
#: not covered — the same silence §10.2 leaves for rasi aspects, where
#: `rahu_ketu_aspects` is a setting. Nothing is assumed here: asking for a
#: node's nakshatra aspects raises.
THE_NODES_ARE_NOT_GIVEN_NAKSHATRA_ASPECTS = (
    "Section 26.5 names the Sun, Moon, Mars, Mercury, Jupiter, Venus and "
    "Saturn. Rahu and Ketu are absent, and it does not say whether they "
    "aspect nothing or were left out."
)


def nakshatra_drishti(graha: int) -> tuple[int, ...]:
    """§26.5's aspected nakshatras for a graha, counted inclusively.

    :raises ValueError: for Rahu, Ketu or anything else the section does not
        cover — see `THE_NODES_ARE_NOT_GIVEN_NAKSHATRA_ASPECTS`.
    """
    index = int(graha)
    if index not in NAKSHATRA_DRISHTI:
        raise ValueError(
            f"section 26.5 gives no nakshatra aspects for graha {index}; it "
            f"covers the seven planets only")
    return NAKSHATRA_DRISHTI[index]


def nakshatra_aspects(graha: int, from_nakshatra: int) -> tuple[int, ...]:
    """The nakshatra indexes `graha` aspects from where it stands.

    :param from_nakshatra: 0 = Aswini.
    """
    start = int(from_nakshatra)
    if not 0 <= start <= 26:
        raise ValueError("nakshatra index must be between 0 and 26")
    return tuple(sorted((start + offset - 1) % 27
                        for offset in nakshatra_drishti(graha)))


def graha_aspects_nakshatra(graha: int, from_nakshatra: int,
                            target: int) -> bool:
    """Does `graha`, standing in `from_nakshatra`, aspect `target`?"""
    if not 0 <= int(target) <= 26:
        raise ValueError("nakshatra index must be between 0 and 26")
    return int(target) in nakshatra_aspects(graha, from_nakshatra)
