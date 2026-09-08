"""Chapter 29 — Tajaka yogas.

§29.1's introduction and the definitions of §29.2, one section at a time.
The yogas apply to Tajaka annual and monthly charts and, the chapter says, to
prasna charts as well.
"""

from __future__ import annotations

import itertools

from hora.core import validate
from hora.core.const import GRAHA_NAMES, NAVAGRAHA, Graha
from hora.core.constants.house import APOKLIMA, KENDRA, PANAPHARA
from hora.tajaka.aspects import (
    TajakaAspectError,
    aspect_on_house,
    deeptamsa,
)

CHAPTER_TITLE = "Tajaka Yogas"


# --------------------------------------------------------------------------
# §29.1 Introduction
# --------------------------------------------------------------------------

#: §29.1, verbatim.
INTRODUCTION = (
    "Just as we have yogas in natal charts, we have special combinations with "
    "special results that are applicable to Tajaka annual/monthly charts. "
    "These are called Tajaka yogas. These yogas are applicable to Tajaka "
    "annual charts as well as prasna charts (horary charts). We will briefly "
    "go over their definitions in this chapter."
)

#: **Finding.** §29.1 extends the chapter to **prasna** charts, which the book
#: has not taught and does not teach. The only other mention is §3.2.13's note
#: that the graha periods "are very useful in prasna or horary astrology".
#: Nothing here depends on it — a prasna chart is a chart, and the yogas read
#: whatever chart they are given — but a reader looking for how to cast one
#: will not find it.
PRASNA_IS_NAMED_BUT_NEVER_TAUGHT = (
    "Section 29.1 says the Tajaka yogas apply to prasna charts. The book "
    "never explains how a prasna chart is cast. Nothing in the chapter needs "
    "it: the yogas read a chart's placements, whatever the chart is for."
)


# --------------------------------------------------------------------------
# §29.2.1 Ishkavala yoga · §29.2.2 Induvara yoga
# --------------------------------------------------------------------------

#: §29.2.1, verbatim.
ISHKAVALA_RULE = (
    "If planets occupy only kendras (1st, 4th, 7th and 10th houses) and "
    "panapharas (2nd, 5th, 8th and 11th houses) and if apoklimas (3rd, 6th, "
    "9th and 12th houses) are empty, then this yoga is present. This yoga "
    "gives wealth, happiness and good fortune."
)

#: §29.2.2, verbatim.
INDUVARA_RULE = (
    "If planets occupy only apoklimas (3rd, 6th, 9th and 12th houses) and if "
    "kendras (1st, 4th, 7th and 10th houses) and panapharas (2nd, 5th, 8th "
    "and 11th houses) are empty, then this yoga is present. This yoga gives "
    "disappointments, worries and illnesses."
)

ISHKAVALA_RESULTS = "wealth, happiness and good fortune"
INDUVARA_RESULTS = "disappointments, worries and illnesses"

#: **Finding.** Both rules are stated twice over — "occupy only X" and "Y is
#: empty" say the same thing when X and Y partition the twelve houses, and
#: they do. Nothing turns on it; it means a chart can be tested either way and
#: `ishkavala` checks both so a disagreement would be caught rather than
#: assumed away.
THE_TWO_HALVES_OF_EACH_RULE_ARE_THE_SAME_TEST = (
    "\"Planets occupy only kendras and panapharas\" and \"apoklimas are "
    "empty\" are one condition, because the three groups partition the "
    "twelve houses with nothing left over."
)

#: **Gap.** Neither section says which bodies count as "planets". The seven
#: classical grahas and the two nodes are both defensible: footnote 83, three
#: paragraphs later, puts Rahu and Ketu in the same chapter's speed order, and
#: the nodes always sit six houses apart, so including them makes both yogas
#: strictly rarer. `ishkavala` and `induvara` take the occupied houses as an
#: input and never decide which bodies produced them. See OI-159.
WHICH_BODIES_COUNT_IS_NOT_SAID = (
    "Sections 29.2.1 and 29.2.2 say \"planets\" without saying whether Rahu "
    "and Ketu are among them. The nodes are always six houses apart, so "
    "including them makes both yogas rarer."
)


class TajakaYogaError(validate.InputError):
    """A Tajaka yoga input that cannot be resolved."""


def _house_group(house: int) -> str:
    index = validate.in_range("house", int(house), 1, 12)
    if index in KENDRA:
        return "kendra"
    if index in PANAPHARA:
        return "panaphara"
    if index in APOKLIMA:
        return "apoklima"
    raise TajakaYogaError(              # pragma: no cover
        f"house {index} is in none of the three groups, which cannot "
        f"happen while they partition the twelve")


def house_groups(houses: tuple[int, ...] | list[int]) -> dict[str, tuple]:
    """The occupied houses split into §7.4's three groups."""
    seen = tuple(dict.fromkeys(int(h) for h in houses))
    out: dict[str, tuple] = {"kendra": (), "panaphara": (), "apoklima": ()}
    for house in seen:
        group = _house_group(house)
        out[group] = (*out[group], house)
    return out


def ishkavala(houses: tuple[int, ...] | list[int]) -> dict:
    """§29.2.1. `houses` are the houses the chart's planets occupy."""
    groups = house_groups(houses)
    occupies_only = bool(houses) and not groups["apoklima"]
    apoklimas_empty = not groups["apoklima"]
    return {
        "yoga": "Ishkavala",
        "present": occupies_only and apoklimas_empty,
        "occupies_only_kendras_and_panapharas": occupies_only,
        "apoklimas_empty": apoklimas_empty,
        "groups": groups,
        "gives": ISHKAVALA_RESULTS,
        "rule": ISHKAVALA_RULE,
    }


def induvara(houses: tuple[int, ...] | list[int]) -> dict:
    """§29.2.2."""
    groups = house_groups(houses)
    occupies_only = bool(houses) and not (groups["kendra"]
                                          or groups["panaphara"])
    others_empty = not (groups["kendra"] or groups["panaphara"])
    return {
        "yoga": "Induvara",
        "present": occupies_only and others_empty,
        "occupies_only_apoklimas": occupies_only,
        "kendras_and_panapharas_empty": others_empty,
        "groups": groups,
        "gives": INDUVARA_RESULTS,
        "rule": INDUVARA_RULE,
    }


#: **Finding, measured.** The chapter presents the two as a matched pair, one
#: good and one bad, but they are nothing like equally likely: ishkavala
#: allows eight houses and induvara four. Over four thousand random charts,
#: ishkavala came up in **6.2%** with the seven classical grahas and **4.1%**
#: with nine, and induvara in **0.03%** and **0%** — one chart in four
#: thousand, and none. Both figures track the naive model, (2/3)^n against
#: (1/3)^n, so nothing but the house count is driving it.
ISHKAVALA_IS_ORDERS_OF_MAGNITUDE_COMMONER = (
    "Ishkavala allows eight of the twelve houses and induvara four, so "
    "ishkavala appears in roughly one chart in sixteen and induvara in "
    "fewer than one in a thousand. The chapter presents them as a pair."
)

#: **Finding.** The two yogas cannot both be present, and in a chart with any
#: planet at all exactly one of three things is true: ishkavala, induvara, or
#: neither. They are opposite ends of one test and the chapter does not say so.
THE_TWO_YOGAS_ARE_OPPOSITE_ENDS_OF_ONE_TEST = (
    "Ishkavala needs every planet outside the apoklimas and induvara needs "
    "every planet inside them, so no chart has both and most charts have "
    "neither."
)


# --------------------------------------------------------------------------
# §29.2.3 Ithasala yoga
# --------------------------------------------------------------------------

#: §29.2.3, verbatim.
ITHASALA_RULE = (
    "If two planets have an aspect and if the faster moving planet is less "
    "advanced in its rasi than the slower moving planet, then we have an "
    "ithasala yoga between the two. In western astrology, this is called an "
    "\"applying aspect\"."
)

#: The Results paragraph, verbatim.
ITHASALA_RESULTS = (
    "This is a good yoga and this shows fulfillment of the matters "
    "represented by the two planets in ithasala. Suppose we want to analyze "
    "prospects for a particular matter. Then ithasala involving lagna lord, "
    "lord of the related house, lord of the related saham or the naisargika "
    "karaka (natural significator) will show good results related to the "
    "matter. For example, ithasala between lagna lord and 7th lord (or the "
    "lord of vivaha saham or Venus) shows that the native may get married in "
    "the year."
)

#: Footnote 83, verbatim.
SPEED_ORDER_FOOTNOTE = (
    "In the increasing order of speed, planets can be listed as: Saturn, "
    "Rahu/Ketu, Jupiter, Mars, Sun, Venus, Mercury and Moon."
)

#: Footnote 83 as data, slowest first. Rahu and Ketu share a place.
SPEED_ORDER: tuple[tuple[int, ...], ...] = (
    (int(Graha.SATURN),),
    (int(Graha.RAHU), int(Graha.KETU)),
    (int(Graha.JUPITER),),
    (int(Graha.MARS),),
    (int(Graha.SUN),),
    (int(Graha.VENUS),),
    (int(Graha.MERCURY),),
    (int(Graha.MOON),),
)

_SPEED_RANK: dict[int, int] = {
    graha: rank for rank, group in enumerate(SPEED_ORDER) for graha in group}


def speed_rank(graha: int) -> int:
    """Footnote 83's rank, 0 for the slowest. Rahu and Ketu share rank 1."""
    index = validate.in_range("graha", int(graha), 0, 8)
    return _SPEED_RANK[index]


def faster_of(a: int, b: int) -> int | None:
    """Which of two grahas footnote 83 calls faster, or ``None`` for a tie.

    The only tie the footnote can produce is Rahu against Ketu, which it
    lists together.
    """
    first, second = speed_rank(a), speed_rank(b)
    if first == second:
        return None
    return int(b) if second > first else int(a)


def advancement(longitude: float) -> float:
    """How far into its own rasi a longitude is — the ithasala comparison.

    §29.2.3 compares the two planets' positions **within their rasis**, not
    their longitudes, so two planets in different signs are compared on the
    same 0°-to-30° scale.
    """
    return validate.longitude("longitude", float(longitude)) % 30.0


#: **Finding.** "Less advanced **in its rasi**" is a comparison of the two
#: degrees-within-sign, not of the longitudes. A planet at 2° of a later sign
#: is *less* advanced than one at 25° of an earlier sign, though it is ahead
#: of it in the zodiac. Easy to implement as a longitude comparison and wrong
#: if you do.
ADVANCEMENT_IS_WITHIN_THE_RASI = (
    "The test compares each planet's degrees within its own rasi. It is not "
    "a comparison of longitudes, and the two disagree whenever the planets "
    "are in different signs."
)

#: **Finding.** §28.2 gives no deeptamsa for Rahu or Ketu, and footnote 83
#: puts them in ithasala's speed order. So an ithasala involving a node can be
#: tested by house distance and **cannot** be tested within an orb. The
#: chapter does not notice the gap.
A_NODES_ITHASALA_CANNOT_BE_ORBED = (
    "Footnote 83 gives Rahu and Ketu a place in the speed order, but section "
    "28.2 gives them no deeptamsa, so an ithasala involving a node has no "
    "orb to be tested against."
)

#: **Settled by §29.2.3's example.** §28.2 gives each graha its **own**
#: deeptamsa, and an aspect between two grahas has two of them — Venus's 7°
#: and Jupiter's 9°, say. The rule does not say whose governs; the example
#: does, in one clause: "**Both** the planets are within the deeptaamsa (orb)
#: **of the other**." Both orbs must hold, so the effective orb is the
#: **smaller** of the two, and it is neither summed nor averaged.
#: `ithasala` already required both, so the example confirms the reading
#: rather than changing it. OI-161 narrowed to the nodes.
WHOSE_DEEPTAMSA_GOVERNS_IS_NOT_SAID = (
    "An ithasala's two grahas have two different deeptamsas. The example "
    "requires each planet to be within the other's, so both must hold and "
    "the smaller of the two governs."
)

#: **Finding.** Requiring both orbs makes the test the smaller deeptamsa, and
#: §28.2's range is 7° to 15°, so which graha is in the pair decides the width
#: by better than a factor of two. A Sun–Moon ithasala has 12° to play with
#: and a Mercury–Venus one has 7°.
THE_SMALLER_DEEPTAMSA_GOVERNS = (
    "Because each planet must be inside the other's orb, an ithasala is "
    "tested against the smaller of the two deeptamsas."
)

#: **Finding.** The orb test and the advancement test read **the same
#: number**. §28.2's aspects are whole-sign, so the exact aspect point falls
#: at the faster planet's own degree in the slower's rasi, and the separation
#: from exact is just the difference of the two advancements. So an ithasala
#: is one interval test: the slower planet's degree minus the faster's, above
#: zero and inside the orb.
THE_ORB_AND_THE_ADVANCEMENT_ARE_ONE_NUMBER = (
    "Because section 28.2's aspects are whole-sign, the separation from the "
    "exact aspect equals the difference between the two planets' degrees "
    "within their rasis. Ithasala is that one difference being positive and "
    "inside the orb."
)

#: **Settled by §29.2.3's example.** "If two planets have an aspect" left it
#: open whether §28.2's deeptamsa had to be satisfied or whether the house
#: distance alone was enough. The example checks the orb as one of its three
#: conditions, before and separately from the advancement test, so the orb is
#: required. `present_by_house` is kept beside `present_within_orb` because
#: the two differ often and a caller reading the wrong one would not be told.
WHETHER_THE_ASPECT_NEEDS_THE_ORB_IS_NOT_SAID = (
    "Section 29.2.3's rule does not say whether section 28.2's deeptamsa "
    "must be satisfied. Its example checks the orb before declaring the "
    "yoga, so it is required."
)


def ithasala(*, faster: int, slower: int, faster_longitude: float,
             slower_longitude: float) -> dict:
    """§29.2.3, for one pair of grahas.

    `faster` and `slower` are not trusted: footnote 83 decides which is which
    and the answer says so, because a caller that has them the wrong way
    round would otherwise get a silently inverted yoga.
    """
    first = validate.in_range("faster", int(faster), 0, 8)
    second = validate.in_range("slower", int(slower), 0, 8)
    if first == second:
        raise TajakaYogaError("an ithasala needs two different grahas")
    quick = faster_of(first, second)
    if quick is None:
        raise TajakaYogaError(
            f"footnote 83 lists {GRAHA_NAMES[first]} and "
            f"{GRAHA_NAMES[second]} together, so neither is the faster")
    slow = second if quick == first else first
    lon = {first: float(faster_longitude), second: float(slower_longitude)}

    house = int((int(lon[slow] // 30) - int(lon[quick] // 30)) % 12) + 1
    aspect = aspect_on_house(house)
    exact = (lon[quick] + 30.0 * (house - 1)) % 360.0
    separation = abs(((lon[slow] - exact + 180.0) % 360.0) - 180.0)
    orbs: dict[str, float | None]
    within: dict[str, bool | None]
    try:
        # Each graha has its own deeptamsa and the section never says whose
        # governs, so both are answered and neither is summed or averaged.
        orbs = {"faster": deeptamsa(quick), "slower": deeptamsa(slow)}
        within = {
            side: aspect is not None and separation <= orb
            for side, orb in orbs.items() if orb is not None}
    except TajakaAspectError:
        orbs = {"faster": None, "slower": None}
        within = {"faster": None, "slower": None}
    within_orb = (None if within["faster"] is None
                  else (within["faster"] and within["slower"]))
    orbs_agree = (None if within["faster"] is None
                  else within["faster"] == within["slower"])

    applying = advancement(lon[quick]) < advancement(lon[slow])
    orb_values = [v for v in orbs.values() if v is not None]
    binding = min(orb_values) if orb_values else None

    vartamaana: bool | None
    poorna: bool | None
    bhavishya: bool | None
    to_go: float | None
    if aspect is None or not applying:
        vartamaana = poorna = bhavishya = False
        to_go = None
    elif binding is None:
        vartamaana = poorna = bhavishya = None
        to_go = None
    else:
        vartamaana = separation <= binding
        poorna = separation <= POORNA_DEGREES
        to_go = max(separation - binding, 0.0)
        bhavishya = (not vartamaana) and to_go <= BHAVISHYA_DEGREES

    kind = None
    if poorna:
        kind = "Poorna"
    elif vartamaana:
        kind = "Vartamaana"
    elif bhavishya:
        kind = "Bhavishya"

    return {
        "yoga": "Ithasala",
        "faster": quick, "faster_name": str(GRAHA_NAMES[quick]),
        "slower": slow, "slower_name": str(GRAHA_NAMES[slow]),
        "caller_had_them_the_right_way_round": quick == first,
        "house_from_faster": house,
        "aspect": None if aspect is None else aspect["name"],
        "aspects_by_house": aspect is not None,
        "aspects_within_faster_deeptamsa": within["faster"],
        "aspects_within_slower_deeptamsa": within["slower"],
        "deeptamsa_of_faster": orbs["faster"],
        "deeptamsa_of_slower": orbs["slower"],
        "deeptamsas_agree": orbs_agree,
        "separation_from_exact": separation,
        "faster_advancement": advancement(lon[quick]),
        "slower_advancement": advancement(lon[slow]),
        "faster_is_less_advanced": applying,
        "present_by_house": bool(aspect is not None and applying),
        # Present under both orbs. When the two disagree the caller is told
        # so rather than handed one of them.
        "present_within_orb": None if within_orb is None
                              else bool(within_orb and applying),
        "binding_deeptamsa": binding,
        "vartamaana": vartamaana,
        "poorna": poorna,
        "bhavishya": bhavishya,
        "degrees_to_vartamaana": to_go,
        "bhavishya_crosses_a_rasi": (
            None if to_go is None
            else advancement(lon[quick]) + to_go >= 30.0),
        # Poorna is a vartamaana, so the most specific name is reported and
        # the three flags stay beside it.
        "type": kind,
        # The example settles whose orb governs — both — so a disagreement
        # between the two is an answer, not an undecided. What is still
        # undecided is a node, which section 28.2 gives no orb at all.
        "undecided": (A_NODES_ITHASALA_CANNOT_BE_ORBED
                      if within_orb is None else None),
        "rule": ITHASALA_RULE,
    }


#: The Results paragraph's four ways in, as data. The paragraph offers them
#: for "a particular matter" and gives marriage as its worked case.
ITHASALA_REFERENCE_LORDS: tuple[str, ...] = (
    "lagna lord",
    "lord of the related house",
    "lord of the related saham",
    "the naisargika karaka",
)

#: The Results paragraph's own example, as data.
ITHASALA_MARRIAGE_EXAMPLE: dict[str, object] = {
    "matter": "marriage",
    "one_side": "lagna lord",
    "other_side": ("the 7th lord", "the lord of vivaha saham", "Venus"),
    "shows": "the native may get married in the year",
}

#: **Finding.** The marriage example is the **third** rule in the book for
#: reading a marriage against vivaha saham, and the first to use the saham's
#: **lord** rather than the saham itself. §25.3 transits the 7th lord or Venus
#: close to the point; §28.8.2 has Jupiter occupy or aspect it; §29.2.3 puts
#: the lagna lord in ithasala with its lord. Three sections, three tests, one
#: event, and none of them cites the others.
A_THIRD_RULE_FOR_THE_SAME_MARRIAGE = (
    "Section 25.3 reads a transit to vivaha saham, section 28.8.2 reads an "
    "aspect on it, and section 29.2.3 reads an ithasala with its lord. Three "
    "different tests for marriage against one saham."
)

#: **Finding, and a parity risk.** Footnote 83's order is a **fixed list**,
#: and real speeds cross it constantly. Over thirty years of daily samples,
#: **22 of the 36 pairs invert at some point**: Mercury is slower than the Sun
#: 34% of the time and slower than Venus 37%, Jupiter is slower than Saturn
#: 24%, Venus slower than the Sun 24%. The footnote is the book's own answer
#: and is what `faster_of` uses; whether JHora reads the list or the
#: instantaneous speed is unchecked. See OI-160.
THE_SPEED_ORDER_IS_A_LIST_NOT_A_MEASUREMENT = (
    "Footnote 83 fixes the order of speed once for all charts. Measured "
    "against the ephemeris, 22 of the 36 pairs invert at some point, so the "
    "list and the true speeds give different ithasalas."
)

#: **Book defect.** Footnote 83's order is right for all seven classical
#: grahas — mean daily motion runs Saturn 4.17', Jupiter 7.95', Mars 34.06',
#: Sun 59.14', Venus 62.54', Mercury 73.09', Moon 790.63' — and wrong for the
#: nodes. It puts Rahu and Ketu **faster** than Saturn; they move 3.18' a day,
#: which is slower. See D-81. The list is followed as printed.
THE_NODES_ARE_THE_ONE_PLACE_THE_ORDER_IS_WRONG = (
    "Footnote 83 lists Rahu and Ketu as faster than Saturn. The nodes move "
    "3.18 arcminutes a day and Saturn averages 4.17, so the nodes are the "
    "slowest bodies in the list, not the second slowest."
)


# --------------------------------------------------------------------------
# §29.2.3 — the three types of ithasala
# --------------------------------------------------------------------------

#: The three types, verbatim.
ITHASALA_TYPES: tuple[dict[str, str], ...] = (
    {"name": "Vartamaana", "means": "present (current)",
     "rule": ("Vartamaana ithasala yoga results when the planets aspect each "
              "other and both are within the deeptaamsa (orb) of the other "
              "planet."),
     "gives": ""},
    {"name": "Poorna", "means": "complete",
     "rule": ("Poorna ithasala yoga results when the planets aspect each "
              "other closely and their advancements in respective rasis are "
              "within 1 degree of each other."),
     "gives": ("Poorna ithasala is the most powerful ithasala. It shows "
               "speedy fulfillment of the matter.")},
    {"name": "Bhavishya", "means": "future",
     "rule": ("Bhavishya ithasala yoga is formed if vartamaana ithasala yoga "
              "is about to be formed when the faster moving planet moves by "
              "1 degree or less."),
     "gives": ("Bhavishya ithasala shows fulfillment after some obstructions "
               "or delay.")},
)

#: Poorna's threshold and bhavishya's are both one degree, and both are stated
#: as "within 1°" and "by 1° or less" — inclusive on either side.
POORNA_DEGREES = 1.0
BHAVISHYA_DEGREES = 1.0

#: **Finding.** The three "types" are not three cases. **Every poorna is a
#: vartamaana**: poorna needs the two advancements within 1° and the smallest
#: deeptamsa in §28.2 is 7°, so a poorna pair is always inside both orbs.
#: Bhavishya is the only one that excludes the others — it is defined by
#: vartamaana *not* holding yet. So the set is one nested pair and one
#: disjoint case, and the chapter numbers them (i), (ii), (iii) as if they
#: were alternatives.
POORNA_IS_A_KIND_OF_VARTAMAANA = (
    "Poorna needs the two advancements within one degree and the smallest "
    "deeptamsa in the book is seven, so every poorna ithasala is also a "
    "vartamaana ithasala. Bhavishya is the only type that excludes the "
    "other two."
)

#: **Finding.** All three types reduce to **one number**: the separation, which
#: is the difference of the two advancements. Inside the smaller deeptamsa it
#: is vartamaana; inside one degree it is also poorna; within one degree
#: *outside* the smaller deeptamsa it is bhavishya. The book works each type
#: from windows in the aspected rasi — Venus at 19° "extends from 12° to 26°"
#: — and every one of those windows is the same subtraction.
ALL_THREE_TYPES_READ_ONE_SEPARATION = (
    "The separation is the slower planet's degree in its rasi minus the "
    "faster planet's. Inside the smaller deeptamsa gives vartamaana, inside "
    "one degree gives poorna as well, and up to one degree outside the "
    "smaller deeptamsa gives bhavishya."
)

#: **Finding.** Bhavishya moves the faster planet forward by up to a degree,
#: which raises the question of what happens when it is near the end of its
#: rasi and would change sign instead, taking the whole-sign aspect with it.
#: **It cannot happen.** Bhavishya needs the separation above the binding
#: deeptamsa, the smallest in §28.2 is 7°, and the separation is the slower
#: planet's degree minus the faster's — so the faster planet is below 23° of
#: its rasi in every bhavishya, and a further degree leaves it below 24°. The
#: book does not raise the case and does not need to. `bhavishya_crosses_a_rasi`
#: is reported anyway, and is False in every chart.
BHAVISHYA_CANNOT_REACH_THE_END_OF_A_RASI = (
    "A bhavishya needs a separation above the smaller deeptamsa, which is at "
    "least seven degrees, so the faster planet is below 23 degrees of its "
    "rasi. Moving it forward by a degree cannot take it out of the sign."
)


#: §29.2.3's worked example, as the book states it.
ITHASALA_EXAMPLE: dict[str, object] = {
    "faster": "Moon", "faster_at": "14 Le", "faster_longitude": 134.0,
    "slower": "Venus", "slower_at": "19 Li", "slower_longitude": 199.0,
    "aspect": "Sextile aspect",
    "both_within_the_others_orb": True,
    "faster_advancement": 14.0,
    "slower_advancement": 19.0,
    "present": True,
}

#: **Finding.** The example states four things and every one of them is
#: checkable: the aspect is a sextile (Leo to Libra is the 3rd, which §28.2
#: calls a sextile), both planets are inside the other's deeptamsa (5° apart,
#: against Venus's 7° and the Moon's 12°), the advancements are 14° and 19°,
#: and the Moon is the faster by footnote 83. All four reproduce.
THE_EXAMPLE_CHECKS_OUT_ON_ALL_FOUR_CLAIMS = (
    "Leo to Libra is the 3rd house, which section 28.2 makes a sextile. The "
    "separation is 5 degrees against orbs of 7 and 12. The advancements are "
    "14 and 19. The Moon is the faster. The yoga is present."
)


#: The three worked cases for the types, as the book states them. The Moon
#: moves and Venus stays; one pair, three separations, three types.
ITHASALA_TYPE_EXAMPLES: tuple[dict[str, object], ...] = (
    {"type": "Vartamaana", "moon": "14 Le", "venus": "19 Li",
     "moon_longitude": 134.0, "venus_longitude": 199.0,
     "separation": 5.0, "book_says": "So we have vartamaana ithasala."},
    {"type": "Poorna", "moon": "18 Le 25", "venus": "19 Li",
     "moon_longitude": 120.0 + 18.0 + 25.0 / 60.0, "venus_longitude": 199.0,
     "separation": 35.0 / 60.0, "book_says": "So we have a poorna ithasala now."},
    {"type": "Bhavishya", "moon": "13 Le 35", "venus": "21 Li 20",
     "moon_longitude": 120.0 + 13.0 + 35.0 / 60.0,
     "venus_longitude": 180.0 + 21.0 + 20.0 / 60.0,
     "separation": 7.0 + 45.0 / 60.0,
     "degrees_to_vartamaana": 45.0 / 60.0,
     "book_says": "he needs to move by just 0 degrees 45 minutes"},
)

#: **Book defect, and it is two slips that mirror each other.** The bhavishya
#: example sets up "Moon is at 13°35' in Le and Venus is at 21°20' in **Le**".
#: Venus is in **Li**: the paragraph calls the aspect a sextile, which Leo to
#: Leo is not, it puts the Moon's sextile "on Li", and it computes Venus's
#: window from 21°20' and compares it against a Leo degree. Then, computing
#: that window, it writes "extends from 14°20' to 28°20' **in Li**". That one
#: is in **Le** — it is Venus's aspect *on Leo*, and the next sentence tests
#: the Moon's Leo degree against it. Le for Li, then Li for Le.
THE_BHAVISHYA_EXAMPLE_SWAPS_TWO_RASI_NAMES = (
    "The bhavishya example puts Venus in Le where it means Li, and then puts "
    "Venus's window in Li where it means Le. Every number in the example is "
    "right; the two rasi names are exchanged."
)

#: **Finding.** All three examples reproduce to the arcminute, including the
#: windows the book prints: Venus at 19° gives 12° to 26°, the Moon at 13°35'
#: gives 1°35' to 25°35', Venus at 21°20' gives 14°20' to 28°20'. And the
#: bhavishya distance the book computes by hand, 0°45', is exactly the
#: separation less the smaller deeptamsa.
THE_THREE_TYPE_EXAMPLES_REPRODUCE = (
    "One pair at three separations gives the three types: 5 degrees is "
    "vartamaana, 35 arcminutes is poorna, and 7 degrees 45 arcminutes is "
    "bhavishya with 45 arcminutes to go."
)


def pairs_in_speed_order() -> tuple[tuple[int, int], ...]:
    """Every graha pair footnote 83 can rank, slower first."""
    out = []
    for a, b in itertools.combinations(sorted(NAVAGRAHA), 2):
        quick = faster_of(a, b)
        if quick is None:
            continue
        out.append((b if quick == a else a, quick))
    return tuple(out)
