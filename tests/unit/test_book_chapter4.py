"""Every claim in Chapter 4 of PVR Narasimha Rao's textbook.

Source: "Vedic Astrology: An Integrated Approach", Chapter 4 (Upagrahas),
book pages 41-44.

Chapter 4 is almost entirely calculation: Table 9's five chained formulas,
Table 10's two 7x8 grids of part lords, and the rule that a time-based upagraha
is the lagna rising inside its ruler's part. Everything here runs through
production code.

Deviation: PVR-5 in docs/precedence.md — the Exercise 7 answer for Upaketu
contradicts both of Table 9's formulas.
"""
import pytest

from hora.charts.upagraha import (
    part_bounds,
    part_index_of,
    part_lords,
    sun_based,
    time_based,
)
from hora.core.const import (
    DAY_NIGHT_DEFINITION,
    DHUMA_OFFSET,
    GRAHA_NAMES,
    LONGITUDE_REDUCTION_NOTE,
    MALEFIC_UPAGRAHAS,
    PART_LORD_CYCLE,
    PARTS_PER_PERIOD,
    RASI_ABBR,
    RISE_POINT_VARIANT_NOTE,
    SUN_BASED_UPAGRAHAS,
    TABLE_10_DAY,
    TABLE_10_NIGHT,
    TIME_BASED_HARDER_NOTE,
    TIME_BASED_UPAGRAHAS,
    UPAGRAHA_COUNT,
    UPAGRAHA_GLOSS,
    UPAGRAHA_GROUP_COUNT,
    UPAGRAHA_GROUPS,
    UPAGRAHA_NAME_VARIANTS,
    UPAGRAHA_NAMES,
    UPAGRAHA_NATURE,
    UPAGRAHA_NOT_PHYSICAL,
    UPAGRAHA_PART_LORD,
    UPAGRAHA_RISES_AT_BEGINNING,
    UPAGRAHA_SOURCE,
    UPAKETU_OFFSET,
    VAARA_LORD,
    VAARA_NAMES,
    Graha,
    Upagraha,
)
from hora.core.notation import parse, to_rasi_dm
from hora.core.settings import Settings, UpagrahaRisePoint

DAY_NAMES = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


def readable(longitude: float) -> str:
    return to_rasi_dm(longitude)


# --------------------------------------------------------------------------
# 4.1 The eleven upagrahas
# --------------------------------------------------------------------------

def test_there_are_eleven_upagrahas_in_two_groups():
    """4.1: eleven, defined in two groups."""
    assert len(UPAGRAHA_NAMES) == 11
    assert len(SUN_BASED_UPAGRAHAS) == 5
    assert len(TIME_BASED_UPAGRAHAS) == 6
    assert set(SUN_BASED_UPAGRAHAS) | set(TIME_BASED_UPAGRAHAS) == set(Upagraha)
    assert not set(SUN_BASED_UPAGRAHAS) & set(TIME_BASED_UPAGRAHAS)


def test_the_five_sun_based_are_the_ones_the_book_names():
    assert [UPAGRAHA_NAMES[u] for u in SUN_BASED_UPAGRAHAS] == [
        "Dhuma", "Vyatipaata", "Parivesha", "Indrachaapa", "Upaketu",
    ]


def test_the_six_time_based_are_the_ones_the_book_names():
    assert [UPAGRAHA_NAMES[u] for u in TIME_BASED_UPAGRAHAS] == [
        "Kaala", "Mrityu", "Artha Praharaka", "Yama Ghantaka", "Gulika", "Maandi",
    ]


# --------------------------------------------------------------------------
# 4.2 Table 9 — the Sun-based formulas
# --------------------------------------------------------------------------

def test_table_9_offsets():
    assert DHUMA_OFFSET == pytest.approx(133 + 20 / 60)
    assert UPAKETU_OFFSET == pytest.approx(16 + 40 / 60)


@pytest.mark.parametrize("sun", [0.0, 43.31666, 123.456, 249.6, 359.99])
def test_table_9_chain_relationships(sun):
    """The relationships the book states must hold for any Sun longitude."""
    u = sun_based(sun)
    d = u[int(Upagraha.DHUMA)]
    v = u[int(Upagraha.VYATIPAATA)]
    p = u[int(Upagraha.PARIVESHA)]
    i = u[int(Upagraha.INDRACHAAPA)]

    assert d == pytest.approx((sun + DHUMA_OFFSET) % 360, abs=1e-9)
    assert v == pytest.approx((360 - d) % 360, abs=1e-9)
    assert p == pytest.approx((v + 180) % 360, abs=1e-9)
    assert i == pytest.approx((360 - p) % 360, abs=1e-9)


@pytest.mark.parametrize("sun", [0.0, 43.31666, 123.456, 249.6, 359.99])
def test_dhuma_and_indrachaapa_are_180_apart(sun):
    """4.2 states this outright."""
    u = sun_based(sun)
    diff = (u[int(Upagraha.INDRACHAAPA)] - u[int(Upagraha.DHUMA)]) % 360
    assert diff == pytest.approx(180.0, abs=1e-9)


@pytest.mark.parametrize("sun", [0.0, 43.31666, 123.456, 249.6, 359.99])
def test_vyatipaata_and_parivesha_are_180_apart(sun):
    """4.2 states this outright."""
    u = sun_based(sun)
    diff = (u[int(Upagraha.PARIVESHA)] - u[int(Upagraha.VYATIPAATA)]) % 360
    assert diff == pytest.approx(180.0, abs=1e-9)


@pytest.mark.parametrize("sun", [0.0, 43.31666, 123.456, 249.6, 359.99, 270.0])
def test_table_9s_two_upaketu_formulas_agree(sun):
    """Table 9 gives Upaketu two ways; unrolled, the chain is Sun - 30."""
    got = sun_based(sun)[int(Upagraha.UPAKETU)]
    assert got == pytest.approx((sun - 30.0) % 360, abs=1e-9)


# --------------------------------------------------------------------------
# 4.2 Example 6 — Sun at 9 Sg 36
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "upagraha,expected",
    [
        (Upagraha.DHUMA, "22 Ar 56"),
        (Upagraha.INDRACHAAPA, "22 Li 56"),
        (Upagraha.VYATIPAATA, "7 Pi 04"),
        (Upagraha.PARIVESHA, "7 Vi 04"),
    ],
)
def test_example_6(upagraha, expected):
    sun = parse("9 Sg 36")
    assert readable(sun_based(sun)[int(upagraha)]) == expected


def test_example_6_sun_longitude_is_what_the_book_computes():
    """"Sg is the 9th rasi and so Sun's longitude can be expressed as 8s 9d36'
    ... The length of each of the 8 rasis before Sg is 30d. So we can find the
    longitude of Sun ... as 8x30d+9d36' = 249d36'."""
    assert parse("9 Sg 36") == pytest.approx(249 + 36 / 60)
    assert 8 * 30 + 9 + 36 / 60 == pytest.approx(249 + 36 / 60)


def test_example_6_dhuma_is_computed_before_it_is_reduced():
    """"Adding 133d20' to it, we get 382d56'. This can be rewritten as
    22d56'."

    The book shows the un-wrapped sum and then reduces it. Asserting only the
    reduced value would pass even if the offset were 133d20' - 360d.
    """
    sun = parse("9 Sg 36")
    raw = sun + DHUMA_OFFSET
    assert raw == pytest.approx(382 + 56 / 60), "the sum before reduction"
    assert raw > 360.0, "which is why the book reduces it"
    assert raw % 360.0 == pytest.approx(22 + 56 / 60)
    assert sun_based(sun)[int(Upagraha.DHUMA)] == pytest.approx(22 + 56 / 60)


def test_example_6_indrachaapa_needs_no_computation():
    """"Because Dhuma and Indrachaapa are 180d apart, you can say without
    further computation that Indrachapa is in the 7th sign from Ar, which is
    Li. His advancement from the start of Li is also 22d56'."

    Two claims: the sign is the 7th from Dhuma's, and the degrees within the
    sign are unchanged. Both are asserted, because 180 degrees preserves the
    advancement only because 180 is a whole number of rasis.
    """
    sun = parse("9 Sg 36")
    dhuma = sun_based(sun)[int(Upagraha.DHUMA)]
    indra = sun_based(sun)[int(Upagraha.INDRACHAAPA)]
    assert int(indra // 30) == (int(dhuma // 30) + 6) % 12, "the 7th sign"
    assert indra % 30 == pytest.approx(dhuma % 30), "same advancement"
    assert indra % 30 == pytest.approx(22 + 56 / 60)


def test_example_6_vyatipaata_is_computed_by_subtraction():
    """"Vyatipata is obtained by subtracting Dhuma from 360d. We see that
    360d - 22d56' = 337d4'. So Vyatipata is at 337d4', i.e. at 7d4' from the
    start of Pi."""
    sun = parse("9 Sg 36")
    dhuma = sun_based(sun)[int(Upagraha.DHUMA)]
    vyatipaata = sun_based(sun)[int(Upagraha.VYATIPAATA)]
    assert 360.0 - dhuma == pytest.approx(337 + 4 / 60)
    assert vyatipaata == pytest.approx(337 + 4 / 60)
    assert vyatipaata % 30 == pytest.approx(7 + 4 / 60)
    assert int(vyatipaata // 30) == 11, "Pisces"


def test_example_6_parivesha_is_180_from_vyatipaata():
    """"Since Parivesha is at 180d from Vyatipata, he is at 7d4' in Vi."""
    sun = parse("9 Sg 36")
    vyatipaata = sun_based(sun)[int(Upagraha.VYATIPAATA)]
    parivesha = sun_based(sun)[int(Upagraha.PARIVESHA)]
    assert parivesha == pytest.approx((vyatipaata + 180.0) % 360.0)
    assert readable(parivesha) == "7 Vi 04"


#: The NOTE's six pairs of signs that are 180 degrees apart.
OPPOSITE_SIGNS = [
    ("Ar", "Li"), ("Ta", "Sc"), ("Ge", "Sg"),
    ("Cn", "Cp"), ("Le", "Aq"), ("Vi", "Pi"),
]


@pytest.mark.parametrize("first,second", OPPOSITE_SIGNS)
def test_example_6_note_the_six_opposite_sign_pairs(first, second):
    """"You can verify that Aries and Libra, Taurus and Scorpio, Gemini and
    Sagittarius, Cancer and Capricorn, Leo and Aquarius, Virgo and Pisces are
    the signs that are 180d apart."""
    abbr = list(RASI_ABBR)
    a, b = abbr.index(first), abbr.index(second)
    assert (b - a) % 12 == 6
    assert abs(b * 30 - a * 30) == 180


def test_example_6_note_covers_every_sign_exactly_once():
    """Six pairs, twelve signs. If the list were mistyped the union would not
    be the whole zodiac."""
    abbr = list(RASI_ABBR)
    seen = [abbr.index(x) for pair in OPPOSITE_SIGNS for x in pair]
    assert sorted(seen) == list(range(12))


def test_example_6_note_worked_illustration():
    """"So, if Dhuma is at 11d36' from the start of Aquarius, Indrachapa will
    be at 11d36' from the start of Leo."

    Worked backwards: find the Sun that puts Dhuma there, then check
    Indrachaapa. This tests the claim rather than restating the arithmetic.
    """
    abbr = list(RASI_ABBR)
    target = abbr.index("Aq") * 30 + 11 + 36 / 60
    sun = (target - DHUMA_OFFSET) % 360.0
    assert sun_based(sun)[int(Upagraha.DHUMA)] == pytest.approx(target)
    indra = sun_based(sun)[int(Upagraha.INDRACHAAPA)]
    assert int(indra // 30) == abbr.index("Le")
    assert indra % 30 == pytest.approx(11 + 36 / 60)


def test_example_6_upaketu_is_in_scorpio():
    """Example 6's fifth upagraha, which the book does not print but which
    Exercise 7's answer appears to have borrowed. Table 9's second form —
    Sun's longitude minus 30 — gives 9 Sc 36 from 9 Sg 36."""
    assert readable(sun_based(parse("9 Sg 36"))[int(Upagraha.UPAKETU)]) == "9 Sc 36"


def test_example_6_all_five_at_once():
    """The whole of Example 6 in one place, so a regression in any one shows
    against the others."""
    got = {
        UPAGRAHA_NAMES[u]: readable(lon)
        for u, lon in sorted(sun_based(parse("9 Sg 36")).items())
    }
    assert got == {
        "Dhuma": "22 Ar 56",
        "Vyatipaata": "7 Pi 04",
        "Parivesha": "7 Vi 04",
        "Indrachaapa": "22 Li 56",
        "Upaketu": "9 Sc 36",
    }


# --------------------------------------------------------------------------
# 4.1 Introduction
# --------------------------------------------------------------------------


def test_4_1_eleven_upagrahas_from_sage_parasara():
    """"There are 11 upagrahas (sub-planets or satellites) defined by Sage
    Parasara."""
    assert UPAGRAHA_COUNT == 11 == len(UPAGRAHA_NAMES)
    assert UPAGRAHA_SOURCE == "Sage Parasara"
    assert UPAGRAHA_GLOSS == "sub-planets or satellites"


def test_4_1_they_are_not_physical_bodies():
    """"They do not appear to correspond to any physical bodies (planets,
    stars etc)... they appear to be some significant mathematical points."""
    assert "physical bodies" in UPAGRAHA_NOT_PHYSICAL
    assert "mathematical points" in UPAGRAHA_NOT_PHYSICAL


def test_4_1_two_groups_and_the_split_is_five_and_six():
    """"They will be defined in two groups." Five Sun-based in 4.2, six
    time-based in 4.3."""
    assert UPAGRAHA_GROUP_COUNT == 2
    assert set(UPAGRAHA_GROUPS) == {"sun_based", "time_based"}
    assert len(sun_based(0.0)) == 5
    assert UPAGRAHA_COUNT - len(sun_based(0.0)) == 6


def test_4_2_names_the_five_sun_based_in_order():
    """"Five upagrahas called Dhuma, Vyatipaata, Parivesha, Indrachaapa and
    Upaketu are defined based on Sun's longitude."""
    assert UPAGRAHA_NAMES[:5] == [
        "Dhuma", "Vyatipaata", "Parivesha", "Indrachaapa", "Upaketu",
    ]
    assert sorted(sun_based(0.0)) == list(range(5))


# --------------------------------------------------------------------------
# 4.2 Exercise 7 — Sun at 13d19' Ta
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "upagraha,expected",
    [
        (Upagraha.DHUMA, "26 Vi 39"),
        (Upagraha.VYATIPAATA, "3 Li 21"),
        (Upagraha.PARIVESHA, "3 Ar 21"),
        (Upagraha.INDRACHAAPA, "26 Pi 39"),
    ],
)
def test_exercise_7_four_answers_that_match(upagraha, expected):
    sun = parse("13 Ta 19")
    assert readable(sun_based(sun)[int(upagraha)]) == expected


def test_exercise_7_all_five_at_once():
    """Exercise 7 in one place. Four reproduce; Upaketu is D-9 / PVR-5.

    Written as a whole-answer comparison so that a regression in any one of
    the four shows up here even if its own test were deleted, and so the one
    disagreement is visible beside the four that agree rather than buried.
    """
    sun = parse("13 Ta 19")
    got = {
        UPAGRAHA_NAMES[u]: readable(lon)
        for u, lon in sorted(sun_based(sun).items())
    }
    printed = {
        "Dhuma": "26 Vi 39", "Vyatipaata": "3 Li 21", "Parivesha": "3 Ar 21",
        "Indrachaapa": "26 Pi 39", "Upaketu": "19 Sc 01",
    }
    assert {k: v for k, v in got.items() if k != "Upaketu"} == {
        k: v for k, v in printed.items() if k != "Upaketu"
    }
    assert got["Upaketu"] == "13 Ar 19"
    disagree = [k for k in printed if got[k] != printed[k]]
    assert disagree == ["Upaketu"], "the deviation is one answer wide"


def test_exercise_7_the_sun_longitude():
    """"If Sun is at 13d19' from the start of Ta" — Taurus is the 2nd rasi, so
    1 x 30 + 13d19'."""
    assert parse("13 Ta 19") == pytest.approx(30 + 13 + 19 / 60)


def test_exercise_7_both_upaketu_forms_agree_here():
    """Table 9 gives Upaketu twice. On this Sun the two forms must land on the
    same degree, which is what makes the printed answer unreachable from
    either."""
    sun = parse("13 Ta 19")
    indra = sun_based(sun)[int(Upagraha.INDRACHAAPA)]
    from_indra = (indra + UPAKETU_OFFSET) % 360.0
    from_sun = (sun - 30.0) % 360.0
    assert from_indra == pytest.approx(from_sun)
    assert readable(from_indra) == readable(from_sun) == "13 Ar 19"


def test_exercise_7_upaketu_follows_the_formula_not_the_printed_answer():
    """PVR-5: the printed answer contradicts both of Table 9's formulas.

    The book answers "19d1' from the start of Sc". Both Table 9 forms give
    13d19' Ar, and they agree with each other exactly.

    **Where the printed answer comes from is unknown.** It falls in Scorpio,
    which is also Upaketu's sign in Example 6 — but Example 6's Upaketu is
    9d36' Sc, so a carry-over would print 9d36', not 19d1'. The sign
    coincides and the degrees do not, so that explanation does not hold and no
    other has been found.

    Tie-break rule 1 (a derivation rule beats its transcribed output) and rule 3
    (a table beats prose) both select the formula. See docs/precedence.md.
    """
    sun = parse("13 Ta 19")
    assert readable(sun_based(sun)[int(Upagraha.UPAKETU)]) == "13 Ar 19"
    assert readable(sun_based(sun)[int(Upagraha.UPAKETU)]) != "19 Sc 01"
    # The sign coincides with Example 6's Upaketu; the degrees do not, which
    # is what defeats the carry-over explanation.
    example_6 = readable(sun_based(parse("9 Sg 36"))[int(Upagraha.UPAKETU)])
    assert example_6 == "9 Sc 36"
    assert example_6.split()[1] == "Sc", "same sign as the printed answer"
    assert example_6 != "19 Sc 01", "but not the same degree"


# --------------------------------------------------------------------------
# 4.3 Table 10 — lords of the eight parts
# --------------------------------------------------------------------------

@pytest.mark.parametrize("vaara", range(7))
def test_table_10_day_rows(vaara):
    assert part_lords(vaara, night=False) == TABLE_10_DAY[vaara], DAY_NAMES[vaara]


@pytest.mark.parametrize("vaara", range(7))
def test_table_10_night_rows(vaara):
    assert part_lords(vaara, night=True) == TABLE_10_NIGHT[vaara], DAY_NAMES[vaara]


@pytest.mark.parametrize("vaara", range(7))
def test_day_parts_start_with_the_weekday_lord(vaara):
    """4.3: "The first part is ruled by the lord of weekday"."""
    from hora.core.const import VAARA_LORD

    assert part_lords(vaara, night=False)[0] == VAARA_LORD[vaara]


@pytest.mark.parametrize(
    "vaara,first_lord",
    [(0, "Jupiter"), (1, "Venus"), (2, "Saturn"), (3, "Sun"),
     (4, "Moon"), (5, "Mars"), (6, "Mercury")],
)
def test_night_parts_start_with_the_fifth_graha_from_the_weekday_lord(vaara, first_lord):
    """4.3 works Thursday through: 5th from Jupiter is Moon."""
    assert GRAHA_NAMES[part_lords(vaara, night=True)[0]] == first_lord


@pytest.mark.parametrize("night", [False, True])
@pytest.mark.parametrize("vaara", range(7))
def test_exactly_one_part_is_lord_less(vaara, night):
    """Seven grahas fill eight slots, so one part has no lord."""
    lords = part_lords(vaara, night=night)
    assert len(lords) == 8
    assert lords.count(None) == 1
    assert len({g for g in lords if g is not None}) == 7


@pytest.mark.parametrize("night", [False, True])
@pytest.mark.parametrize("vaara", range(7))
def test_the_lord_less_part_follows_saturns(vaara, night):
    """4.3: "The part after the one ruled by Saturn is lord-less"."""
    lords = part_lords(vaara, night=night)
    saturn_at = lords.index(Graha.SATURN)
    assert lords[(saturn_at + 1) % 8] is None


# --------------------------------------------------------------------------
# 4.3 Rise points and the worked example
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "upagraha,lord",
    [(Upagraha.KAALA, "Sun"), (Upagraha.MRITYU, "Mars"),
     (Upagraha.ARTHA_PRAHARAKA, "Mercury"), (Upagraha.YAMA_GHANTAKA, "Jupiter"),
     (Upagraha.GULIKA, "Saturn"), (Upagraha.MAANDI, "Saturn")],
)
def test_each_time_based_upagraha_rises_in_its_lords_part(upagraha, lord):
    assert GRAHA_NAMES[UPAGRAHA_PART_LORD[upagraha]] == lord


def test_only_maandi_rises_at_the_beginning_of_its_part():
    """4.3: Gulika at the middle of Saturn's part, Maandi at its beginning."""
    assert UPAGRAHA_RISES_AT_BEGINNING == frozenset({Upagraha.MAANDI})


@pytest.mark.parametrize(
    "upagraha,like",
    [(Upagraha.KAALA, "Sun"), (Upagraha.MRITYU, "Mars"),
     (Upagraha.ARTHA_PRAHARAKA, "Mercury"), (Upagraha.YAMA_GHANTAKA, "Jupiter"),
     (Upagraha.GULIKA, "Saturn"), (Upagraha.MAANDI, "Saturn")],
)
def test_natures_of_the_time_based_upagrahas(upagraha, like):
    """4.3: "Kaala is a malefic upagraha similar to Sun", and so on."""
    assert GRAHA_NAMES[UPAGRAHA_NATURE[upagraha]] == like


def test_worked_example_thursday_night_yama_ghantaka():
    """4.3: Thursday night, sunset 6pm to sunrise 6am.

    The book: Jupiter rules the 4th part; each part is 12/8 = 1.5 hours; the 4th
    runs 10:30pm to midnight; its middle is 11:15pm.
    """
    thursday = 4
    index = part_index_of(Graha.JUPITER, thursday, night=True)
    assert index == 4

    # Express the night as a unit interval of 0.5 days starting at 18:00.
    begin, end = part_bounds(index, 0.0, 0.5)
    hours = lambda frac: 18.0 + frac * 24.0
    assert (end - begin) * 24.0 == pytest.approx(1.5)
    assert hours(begin) == pytest.approx(22.5)     # 10:30 pm
    assert hours(end) == pytest.approx(24.0)       # midnight
    assert hours((begin + end) / 2) == pytest.approx(23.25)   # 11:15 pm


def test_the_eight_parts_tile_the_period_exactly():
    for i in range(1, 9):
        begin, end = part_bounds(i, 100.0, 100.5)
        assert end - begin == pytest.approx(0.5 / 8)
        if i > 1:
            assert begin == pytest.approx(part_bounds(i - 1, 100.0, 100.5)[1])
    assert part_bounds(1, 100.0, 100.5)[0] == 100.0
    assert part_bounds(8, 100.0, 100.5)[1] == pytest.approx(100.5)


# --------------------------------------------------------------------------
# Footnote 9 — the "beginning of the part" variant
# --------------------------------------------------------------------------

def _six(settings, **kw):
    return time_based(
        4, night=True, period_start_jd=2441591.25, period_end_jd=2441591.75,
        latitude=16.2, longitude=81.13, settings=settings, **kw
    )


def test_footnote_9_variant_moves_every_upagraha_to_its_parts_beginning():
    middle = _six(Settings())
    beginning = _six(Settings(upagraha_rise_point=UpagrahaRisePoint.BEGINNING))

    for u in TIME_BASED_UPAGRAHAS:
        if u in UPAGRAHA_RISES_AT_BEGINNING:
            # Maandi already rises at the beginning, so it must not move.
            assert middle[int(u)].rise_jd == pytest.approx(beginning[int(u)].rise_jd)
        else:
            assert middle[int(u)].rise_jd != beginning[int(u)].rise_jd


def test_default_rise_point_is_the_books_main_text():
    assert Settings().upagraha_rise_point is UpagrahaRisePoint.MIDDLE


def test_gulika_and_maandi_share_a_part_but_not_a_rise_point():
    """Both rise in Saturn's part; Gulika at its middle, Maandi at its start."""
    six = _six(Settings())
    gulika = six[int(Upagraha.GULIKA)]
    maandi = six[int(Upagraha.MAANDI)]
    assert gulika.part_index == maandi.part_index
    assert maandi.rise_jd < gulika.rise_jd


# --------------------------------------------------------------------------
# 4.3 Which day or night a birth falls in
#
# "A day starts at the time of sunrise and ends at the time of sunset. A night
# starts at the time of sunset and ends at the time of next day's sunrise."
#
# The pre-dawn case is the one that bites: the night began at YESTERDAY's
# sunset, and since the vaara turns at sunrise the birth still belongs to
# yesterday's vaara.
# --------------------------------------------------------------------------

MACHILIPATNAM = (16.2, 81.13, 0.0)


def _period(hour, minute=0, y=1990, mo=6, d=15):
    from hora.charts.upagraha import birth_period
    from hora.core.timeutil import from_local

    jd = from_local(y, mo, d, hour, minute, 0, tz_name="Asia/Kolkata").jd_ut
    return birth_period(jd, *MACHILIPATNAM, Settings())


@pytest.mark.parametrize(
    "hour,is_night",
    [(2, True), (5, True), (7, False), (13, False), (18, False), (20, True), (23, True)],
)
def test_day_and_night_classification(hour, is_night):
    assert _period(hour).is_night is is_night


def test_a_day_birth_runs_sunrise_to_sunset():
    p = _period(13)
    assert not p.is_night
    assert p.start_jd == p.sunrise_jd
    assert p.start_jd < p.end_jd


def test_an_evening_birth_runs_this_sunset_to_tomorrows_sunrise():
    p = _period(20)
    assert p.is_night
    assert p.sunrise_jd < p.start_jd < p.end_jd


def test_a_pre_dawn_birth_belongs_to_the_previous_nights_period():
    """The night began at yesterday's sunset, not anywhere near today's.

    An earlier version estimated it as ``sunset - night_length``, which put it
    around 05:00 instead of 18:34 — out by roughly thirteen hours, displacing
    all eight parts and every time-based upagraha with them.
    """
    pre_dawn = _period(2)
    evening_before = _period(20, y=1990, mo=6, d=14)

    assert pre_dawn.is_night
    assert pre_dawn.start_jd == pytest.approx(evening_before.start_jd, abs=1e-6)
    assert pre_dawn.end_jd == pytest.approx(evening_before.end_jd, abs=1e-6)
    # The period must actually contain the birth.
    from hora.core.timeutil import from_local

    jd = from_local(1990, 6, 15, 2, 0, 0, tz_name="Asia/Kolkata").jd_ut
    assert pre_dawn.start_jd < jd < pre_dawn.end_jd


def test_a_pre_dawn_birth_keeps_the_previous_vaara():
    """The vaara turns at sunrise, not at midnight. 15 June 1990 was a Friday."""
    assert _period(2).vaara == 4        # Thursday
    assert _period(13).vaara == 5       # Friday
    assert _period(23).vaara == 5       # still Friday


@pytest.mark.parametrize("hour", [0, 2, 5, 7, 13, 18, 20, 23])
def test_the_period_always_contains_the_birth(hour):
    """Whatever the hour, the returned window must bracket the moment."""
    from hora.core.timeutil import from_local

    p = _period(hour)
    jd = from_local(1990, 6, 15, hour, 0, 0, tz_name="Asia/Kolkata").jd_ut
    assert p.start_jd <= jd < p.end_jd


@pytest.mark.parametrize("month", [1, 4, 6, 10, 12])
def test_pre_dawn_periods_are_sane_across_the_year(month):
    """Night length varies; the window must stay plausible in every season."""
    p = _period(2, mo=month)
    hours = (p.end_jd - p.start_jd) * 24.0
    assert 9.0 < hours < 15.0, hours


# --------------------------------------------------------------------------
# 4.2 Malefic natures
# --------------------------------------------------------------------------

def test_all_five_sun_based_upagrahas_are_very_malefic():
    """4.2: "All these upagrahas are very malefic in nature"."""
    from hora.core.const import VERY_MALEFIC_UPAGRAHAS

    assert VERY_MALEFIC_UPAGRAHAS == frozenset(SUN_BASED_UPAGRAHAS)


def test_only_kaala_and_mrityu_are_called_malefic_among_the_time_based():
    """4.3 says "malefic" for Kaala and Mrityu; for the other four it gives
    only the graha they resemble, and nothing is inferred beyond that."""
    from hora.core.const import MALEFIC_UPAGRAHAS

    assert MALEFIC_UPAGRAHAS == frozenset({Upagraha.KAALA, Upagraha.MRITYU})


# --------------------------------------------------------------------------
# Footnote 8 — longitude normalisation
# --------------------------------------------------------------------------

@pytest.mark.parametrize("sun", [0.0, 1.0, 200.0, 240.0, 300.0, 359.999])
def test_footnote_8_every_longitude_is_reduced_into_range(sun):
    """Footnote 8: "reduce all longitudes to a value between 0 and 360"."""
    for value in sun_based(sun).values():
        assert 0.0 <= value < 360.0


def test_footnote_8_wraparound_cases():
    """Dhuma from a late-zodiac Sun must wrap, not exceed 360."""
    # Example 6 itself wraps: 249d36' + 133d20' = 382d56' -> 22d56'.
    assert sun_based(parse("9 Sg 36"))[int(Upagraha.DHUMA)] == pytest.approx(
        22 + 56 / 60, abs=1e-6
    )
    # And Upaketu from an early-zodiac Sun must wrap the other way.
    assert sun_based(10.0)[int(Upagraha.UPAKETU)] == pytest.approx(340.0, abs=1e-9)


# --------------------------------------------------------------------------
# 4.3 Other Upagrahas — the six time-based ones
# --------------------------------------------------------------------------

#: "Kaala is a malefic upagraha similar to Sun. Mritya is a malefic upagraha
#: similar to Mars. Arthaprahaara is similar to Mercury. Yamaghantaka is
#: similar to Jupiter. Gulika and Maandi are similar to Saturn."
SIMILAR_TO = [
    (Upagraha.KAALA, "Sun"), (Upagraha.MRITYU, "Mars"),
    (Upagraha.ARTHA_PRAHARAKA, "Mercury"), (Upagraha.YAMA_GHANTAKA, "Jupiter"),
    (Upagraha.GULIKA, "Saturn"), (Upagraha.MAANDI, "Saturn"),
]


@pytest.mark.parametrize("upagraha,graha", SIMILAR_TO)
def test_4_3_each_upagraha_resembles_a_graha(upagraha, graha):
    assert GRAHA_NAMES[UPAGRAHA_NATURE[int(upagraha)]] == graha


def test_4_3_only_kaala_and_mrityu_are_called_malefic():
    """"Kaala is a malefic upagraha... Mritya is a malefic upagraha..." — the
    word is used for those two only. The other four get a resemblance and no
    verdict, so none is inferred for them."""
    assert MALEFIC_UPAGRAHAS == frozenset({Upagraha.KAALA, Upagraha.MRITYU})
    assert "more difficult to compute" in TIME_BASED_HARDER_NOTE


def test_4_3_gulika_and_maandi_share_a_graha():
    """The only pair that does, which is why UPAGRAHA_NATURE is not a
    bijection and a uniqueness check would be wrong."""
    assert UPAGRAHA_NATURE[int(Upagraha.GULIKA)] == UPAGRAHA_NATURE[
        int(Upagraha.MAANDI)
    ]
    assert len(set(UPAGRAHA_NATURE.values())) == 5


def test_4_3_the_book_spells_two_of_them_two_ways():
    """The opening list writes "Arthaprahaara" and "Yamaghantaka"; the
    numbered procedure writes "Artha Praharaka" and "Yama Ghantaka". Both are
    PVR's. The procedure's spelling is canonical because that is where the six
    are defined; the list's spelling is kept as a variant."""
    assert UPAGRAHA_NAMES[int(Upagraha.ARTHA_PRAHARAKA)] == "Artha Praharaka"
    assert UPAGRAHA_NAME_VARIANTS[int(Upagraha.ARTHA_PRAHARAKA)] == "Arthaprahaara"
    assert UPAGRAHA_NAMES[int(Upagraha.YAMA_GHANTAKA)] == "Yama Ghantaka"
    assert UPAGRAHA_NAME_VARIANTS[int(Upagraha.YAMA_GHANTAKA)] == "Yamaghantaka"
    assert len(UPAGRAHA_NAME_VARIANTS) == 2, "only these two are spelt twice"


def test_4_3_the_day_and_night_spans():
    """"A day starts at the time of sunrise and ends at the time of sunset. A
    night starts at the time of sunset and ends at the time of next day's
    sunrise."

    **Not the same day as 1.3.11's.** A hora divides sunrise-to-next-sunrise
    into 24; a part divides only the daylight, or only the night, into 8.
    """
    from hora.charts.hora import HORAS_PER_DAY

    assert "ends at the time of sunset" in DAY_NIGHT_DEFINITION
    assert "next day's sunrise" in DAY_NIGHT_DEFINITION
    assert PARTS_PER_PERIOD == 8
    assert HORAS_PER_DAY == 24, "1.3.11 divides a different span"


# --------------------------------------------------------------------------
# 4.3 Table 10 — every row of both halves
# --------------------------------------------------------------------------

#: Table 10 exactly as printed. "—" is the lord-less part.
PRINTED_TABLE_10_DAY = [
    ("Sun", ["Sun", "Moon", "Mars", "Merc", "Jup", "Ven", "Sat", "—"]),
    ("Mon", ["Moon", "Mars", "Merc", "Jup", "Ven", "Sat", "—", "Sun"]),
    ("Tue", ["Mars", "Merc", "Jup", "Ven", "Sat", "—", "Sun", "Moon"]),
    ("Wed", ["Merc", "Jup", "Ven", "Sat", "—", "Sun", "Moon", "Mars"]),
    ("Thu", ["Jup", "Ven", "Sat", "—", "Sun", "Moon", "Mars", "Merc"]),
    ("Fri", ["Ven", "Sat", "—", "Sun", "Moon", "Mars", "Merc", "Jup"]),
    ("Sat", ["Sat", "—", "Sun", "Moon", "Mars", "Merc", "Jup", "Ven"]),
]
PRINTED_TABLE_10_NIGHT = [
    ("Sun", ["Jup", "Ven", "Sat", "—", "Sun", "Moon", "Mars", "Merc"]),
    ("Mon", ["Ven", "Sat", "—", "Sun", "Moon", "Mars", "Merc", "Jup"]),
    ("Tue", ["Sat", "—", "Sun", "Moon", "Mars", "Merc", "Jup", "Ven"]),
    ("Wed", ["Sun", "Moon", "Mars", "Merc", "Jup", "Ven", "Sat", "—"]),
    ("Thu", ["Moon", "Mars", "Merc", "Jup", "Ven", "Sat", "—", "Sun"]),
    ("Fri", ["Mars", "Merc", "Jup", "Ven", "Sat", "—", "Sun", "Moon"]),
    ("Sat", ["Merc", "Jup", "Ven", "Sat", "—", "Sun", "Moon", "Mars"]),
]

_ABBR = {"Sun": 0, "Moon": 1, "Mars": 2, "Merc": 3, "Jup": 4, "Ven": 5, "Sat": 6}


def _row(vaara: int, *, night: bool) -> list[str]:
    out = []
    for lord in part_lords(vaara, night=night):
        if lord is None:
            out.append("—")
        else:
            out.append(next(k for k, v in _ABBR.items() if v == int(lord)))
    return out


@pytest.mark.parametrize("weekday,expected", PRINTED_TABLE_10_DAY)
def test_table_10_day_row_matches_the_printed_table(weekday, expected):
    vaara = [w[:3] for w in VAARA_NAMES].index(weekday)
    assert _row(vaara, night=False) == expected


@pytest.mark.parametrize("weekday,expected", PRINTED_TABLE_10_NIGHT)
def test_table_10_night_row_matches_the_printed_table(weekday, expected):
    vaara = [w[:3] for w in VAARA_NAMES].index(weekday)
    assert _row(vaara, night=True) == expected


def test_the_daytime_rule_as_stated():
    """"The first part is ruled by the lord of weekday and then we cover
    planets in the order of weekdays. The part after the one ruled by Saturn
    is lord-less. After that, Sun's part comes."""
    for vaara in range(7):
        lords = part_lords(vaara, night=False)
        assert int(lords[0]) == int(VAARA_LORD[vaara]), "first part is the weekday lord"
        saturn_at = lords.index(Graha.SATURN)
        assert lords[(saturn_at + 1) % 8] is None, "the part after Saturn"
        assert int(lords[(saturn_at + 2) % 8]) == int(Graha.SUN), "then Sun"


def test_the_daytime_worked_example_is_thursday():
    """"the first 1/8th of the daytime on a Thursday is ruled by Jupiter. Next
    part is ruled by Venus. The 3rd part is ruled by Saturn. The 4th part is
    lord-less. The 5th part is ruled by Sun. The 6th part is ruled by Moon.
    The 7th planet is ruled by Mars. The 8th part is ruled by Mercury."""
    thursday = [w[:3] for w in VAARA_NAMES].index("Thu")
    assert _row(thursday, night=False) == [
        "Jup", "Ven", "Sat", "—", "Sun", "Moon", "Mars", "Merc",
    ]


def test_the_nighttime_rule_as_stated():
    """"The first part is ruled by the 5th planet from the lord of weekday and
    then we cover planets in the order of weekdays."

    The count is through the seven grahas, skipping the lord-less slot — which
    is why it is not simply five positions along the eight-slot cycle.
    """
    order = [Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY,
             Graha.JUPITER, Graha.VENUS, Graha.SATURN]
    for vaara in range(7):
        start = order.index(VAARA_LORD[vaara])
        fifth = order[(start + 4) % 7]
        assert int(part_lords(vaara, night=True)[0]) == int(fifth)


def test_the_nighttime_worked_example_is_thursday():
    """"the first 1/8th of a Thursday night is ruled by the 5th planet from
    Jupiter, i.e. Moon (Jupiter, Venus, Saturn, Sun, Moon - that's the 5th
    one). Next part is ruled by Mars. The 3rd part is ruled by Mercury. The
    4th part is ruled by Jupiter. The 5th part is ruled by Venus. The 6th part
    is ruled by Saturn. The 7th planet is lord-less. The 8th part is ruled by
    Sun."""
    thursday = [w[:3] for w in VAARA_NAMES].index("Thu")
    assert _row(thursday, night=True) == [
        "Moon", "Mars", "Merc", "Jup", "Ven", "Sat", "—", "Sun",
    ]


def test_every_row_of_table_10_is_the_same_cycle_rotated():
    """All fourteen rows are PART_LORD_CYCLE at a different offset. Asserting
    it means a mistyped row cannot hide as a plausible-looking permutation."""
    for vaara in range(7):
        for night in (False, True):
            lords = part_lords(vaara, night=night)
            offset = PART_LORD_CYCLE.index(lords[0])
            assert lords == tuple(
                PART_LORD_CYCLE[(offset + i) % 8] for i in range(8)
            ), (vaara, night)


def test_exactly_one_part_is_lord_less_in_every_row():
    for vaara in range(7):
        for night in (False, True):
            lords = part_lords(vaara, night=night)
            assert sum(x is None for x in lords) == 1
            assert len({int(x) for x in lords if x is not None}) == 7


# --------------------------------------------------------------------------
# 4.3 Rise points, and footnote 9
# --------------------------------------------------------------------------

RISE_POINTS = [
    (Upagraha.KAALA, Graha.SUN, "middle"),
    (Upagraha.MRITYU, Graha.MARS, "middle"),
    (Upagraha.ARTHA_PRAHARAKA, Graha.MERCURY, "middle"),
    (Upagraha.YAMA_GHANTAKA, Graha.JUPITER, "middle"),
    (Upagraha.GULIKA, Graha.SATURN, "middle"),
    (Upagraha.MAANDI, Graha.SATURN, "beginning"),
]


@pytest.mark.parametrize("upagraha,graha,where", RISE_POINTS)
def test_4_3_each_rise_point(upagraha, graha, where):
    """"Kaala rises at the middle of Sun's part... Maandi rises at the
    beginning of Saturn's part."""
    assert int(UPAGRAHA_PART_LORD[int(upagraha)]) == int(graha)
    at_beginning = int(upagraha) in UPAGRAHA_RISES_AT_BEGINNING
    assert at_beginning == (where == "beginning")


def test_4_3_maandi_alone_rises_at_the_beginning():
    """Five of the six take the middle. Maandi is the exception in the book's
    own numbered list, not a variant reading."""
    assert UPAGRAHA_RISES_AT_BEGINNING == frozenset({Upagraha.MAANDI})


def test_4_3_gulika_and_maandi_share_saturns_part_but_not_the_point():
    """Both are Saturn's, and they are told apart only by where in the part
    they rise. A rise-point bug would silently merge them."""
    assert UPAGRAHA_PART_LORD[int(Upagraha.GULIKA)] == UPAGRAHA_PART_LORD[
        int(Upagraha.MAANDI)
    ]
    assert int(Upagraha.GULIKA) not in UPAGRAHA_RISES_AT_BEGINNING
    assert int(Upagraha.MAANDI) in UPAGRAHA_RISES_AT_BEGINNING


def test_footnote_9_offers_the_beginning_for_all_six():
    """"Some scholars suggest that Kaala rises at the beginning of Sun's part.
    The same thing applies to others."

    "The same thing applies to others" makes this a variant for all six, not
    only Kaala — which is why the setting is a global rise point rather than a
    per-upagraha override.
    """
    assert "beginning of Sun's part" in RISE_POINT_VARIANT_NOTE
    assert "applies to others" in RISE_POINT_VARIANT_NOTE
    assert {x.value for x in UpagrahaRisePoint} == {"middle", "beginning"}


def test_footnote_8_states_the_reduction_convention():
    """"When adding or subtracting longitudes, we should subtract 360d if we
    get more than 360d... We should finally reduce all longitudes to a value
    between 0d and 360d."

    Every Table 9 formula relies on this; Example 6's 382d56' is where it is
    first used.
    """
    assert "between 0" in LONGITUDE_REDUCTION_NOTE
    assert "going around the zodiac" in LONGITUDE_REDUCTION_NOTE
    # And the implementation follows it, for arbitrarily large inputs.
    assert 0.0 <= sun_based(0.0)[int(Upagraha.DHUMA)] < 360.0
    assert sun_based(359.9)[int(Upagraha.VYATIPAATA)] >= 0.0


# --------------------------------------------------------------------------
# 4.3 The Thursday-night Yamaghantaka worked example
# --------------------------------------------------------------------------


def test_the_worked_example_jupiter_rules_the_fourth_part_of_a_thursday_night():
    """"We see from the table that Jupiter rules the 4th part of a Thursday
    night."""
    thursday = [w[:3] for w in VAARA_NAMES].index("Thu")
    assert part_index_of(Graha.JUPITER, thursday, night=True) == 4


def test_the_worked_example_part_length_and_bounds():
    """"Suppose night starts at 6 pm and ends at 6 am on the next day... Each
    part is 12/8 = 1.5 hours. The 4th part starts 4.5 hours after sunset, i.e.
    at 10:30 pm, and ends 1.5 hours later. So Jupiter's part extends from
    10:30 pm to midnight. The middle point of this part is at 11:15 pm."

    Worked in hours from sunset so no ephemeris is needed — the timing is the
    part of the example that is arithmetic rather than a lagna lookup.
    """
    night_length = 12.0
    part = night_length / 8
    assert part == 1.5

    start = (4 - 1) * part
    assert start == 4.5, "4.5 hours after sunset"
    assert start + part == 6.0, "which is midnight, 6 hours after 6 pm"
    middle = start + part / 2
    assert middle == 5.25, "11:15 pm, 5.25 hours after 6 pm"

    # 6 pm plus 5.25 hours is 11:15 pm.
    hour = (18 + middle) % 24
    assert (int(hour), round((hour % 1) * 60)) == (23, 15)


def test_the_worked_example_uses_the_middle_because_of_the_rise_point():
    """Yama Ghantaka takes the middle of its part, which is why the example
    lands on 11:15 pm and not 10:30 pm. Under footnote 9's variant it would be
    10:30 pm."""
    assert int(Upagraha.YAMA_GHANTAKA) not in UPAGRAHA_RISES_AT_BEGINNING
    assert UPAGRAHA_PART_LORD[int(Upagraha.YAMA_GHANTAKA)] == Graha.JUPITER


def test_part_bounds_reproduces_the_worked_example():
    """The same numbers through `part_bounds`, so the example checks the code
    rather than a hand calculation beside it."""
    start, end = part_bounds(4, 0.0, 12.0)
    assert (start, end) == (4.5, 6.0)
    assert (start + end) / 2 == 5.25
