"""Chapter 9 — Arudha Padas. §9.2's six steps.

Chapter 9 had no test module of its own until now: its behaviour was pinned
only by golden fixtures, which catch drift but do not say what the book
requires. These do.

The section's own worked example runs through the six steps: a house in Gemini
whose lord Mercury is in Aquarius gives a count of 9, lands in Libra, and the
exception does not fire.
"""
import pytest

from hora.charts.arudha import (
    ARUDHA_GENERIC_NAMES,
    ARUDHA_SPECIAL_NAMES,
    ARUDHA_SPECIAL_SYMBOLS,
    ARUDHA_SYMBOLS,
    DUAL_LORDED,
    ArudhaError,
    advance_from_lord,
    all_arudha_padas,
    apply_exception,
    arudha_pada,
    count_to_lord,
    house_sign,
    lord_of,
)
from hora.core.const import GRAHA_NAMES, GRAHA_OWNS, Graha, Rasi
from hora.services import arudha_service

ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]
R = {name: i for i, name in enumerate(ABBR)}


# --------------------------------------------------------------------------
# Step 1
# --------------------------------------------------------------------------

def test_step_1_takes_the_sign_containing_the_house():
    """Houses are counted from the lagna, so the nth is n-1 signs on."""
    assert house_sign(1, R["Ge"]) == R["Ge"]
    assert house_sign(2, R["Ge"]) == R["Cn"]
    assert house_sign(12, R["Ge"]) == R["Ta"]


@pytest.mark.parametrize("house", [0, 13, -1])
def test_step_1_rejects_a_house_out_of_range(house):
    """Range checks raise the shared InputError, which ArudhaError subclasses.

    The docstrings said ArudhaError, which would have let a caller catching
    only that miss a range error. Corrected to InputError, the accurate and
    wider type.
    """
    from hora.core.validate import InputError

    assert issubclass(ArudhaError, InputError)
    with pytest.raises(InputError):
        house_sign(house, 0)


# --------------------------------------------------------------------------
# Step 2 and its NOTE
# --------------------------------------------------------------------------

def test_step_2_finds_the_lord_of_the_sign():
    assert lord_of(R["Ge"]) == int(Graha.MERCURY)
    assert lord_of(R["Ar"]) == int(Graha.MARS)


def test_the_note_names_both_co_owned_signs_and_their_lords():
    """"Aquarius is owned by Saturn and Rahu. Scorpio is owned by Mars and
    Ketu." """
    assert set(DUAL_LORDED) == {int(Rasi.AQUARIUS), int(Rasi.SCORPIO)}
    assert DUAL_LORDED[Rasi.AQUARIUS] == (Graha.SATURN, Graha.RAHU)
    assert DUAL_LORDED[Rasi.SCORPIO] == (Graha.MARS, Graha.KETU)


def test_a_co_owned_sign_needs_a_choice_and_names_who_owns_it():
    with pytest.raises(ArudhaError, match="Saturn or Rahu"):
        lord_of(int(Rasi.AQUARIUS))
    assert lord_of(int(Rasi.AQUARIUS),
                   {int(Rasi.AQUARIUS): int(Graha.RAHU)}) == int(Graha.RAHU)


def test_a_graha_that_does_not_own_the_sign_is_refused():
    with pytest.raises(ArudhaError, match="does not own"):
        lord_of(int(Rasi.SCORPIO), {int(Rasi.SCORPIO): int(Graha.JUPITER)})


# --------------------------------------------------------------------------
# Steps 3 and 4
# --------------------------------------------------------------------------

def test_step_3_counts_gemini_to_aquarius_as_nine():
    """The section's own example."""
    assert count_to_lord(R["Ge"], R["Aq"]) == 9


def test_step_3_counts_zodiacally_always():
    """"Counting is in the zodiacal direction always" — never the short way."""
    assert count_to_lord(R["Aq"], R["Ge"]) == 5      # not 9 back the other way
    assert count_to_lord(R["Ar"], R["Ar"]) == 1      # inclusive of the start
    assert count_to_lord(R["Ar"], R["Pi"]) == 12


def test_step_4_counts_nine_from_aquarius_to_libra():
    """"we count 9 signs from Aquarius and we end up in Libra"."""
    assert advance_from_lord(R["Aq"], 9) == R["Li"]


def test_step_4_is_inclusive_so_a_count_of_one_stays_put():
    assert advance_from_lord(R["Ar"], 1) == R["Ar"]


# --------------------------------------------------------------------------
# Step 5, the exception
# --------------------------------------------------------------------------

@pytest.mark.parametrize("landed,original,expected,fired", [
    (R["Ar"], R["Ar"], R["Cp"], 1),      # 1st from the original -> the 10th
    (R["Li"], R["Ar"], R["Cn"], 7),      # 7th from the original -> the 10th
    (R["Li"], R["Ge"], R["Li"], None),   # 5th — no change
])
def test_step_5_fires_only_from_the_first_or_seventh(landed, original, expected, fired):
    sign, position = apply_exception(landed, original)
    assert sign == expected
    assert position == fired


def test_the_exception_can_only_ever_fire_from_the_first_or_seventh():
    """Step 4's sign is 2L - H, which is congruent to H exactly when the lord
    sits in the house itself or the 7th from it. No other position is
    reachable, so the rule names all the cases there are."""
    seen = set()
    for house in range(12):
        for lord in range(12):
            landed = advance_from_lord(lord, count_to_lord(house, lord))
            _sign, position = apply_exception(landed, house)
            seen.add(position)
    assert seen == {None, 1, 7}


# --------------------------------------------------------------------------
# Step 6 — the whole procedure
# --------------------------------------------------------------------------

def test_the_sections_worked_example_runs_end_to_end():
    """Gemini house, Mercury in Aquarius: count 9, land in Libra, no change."""
    signs = {g: 0 for g in range(9)}
    signs[int(Graha.MERCURY)] = R["Aq"]
    pada = arudha_pada(house=1, lagna_sign=R["Ge"], graha_signs=signs)

    assert pada.house_sign == R["Ge"]
    assert pada.lord == int(Graha.MERCURY)
    assert pada.lord_sign == R["Aq"]
    assert pada.count == 9
    assert pada.before_exception == R["Li"]
    assert pada.exception_applied is False
    assert pada.sign == R["Li"]
    assert [s.number for s in pada.steps] == [1, 2, 3, 4, 5, 6]


def test_the_closed_form_agrees_with_the_six_steps_everywhere():
    """Steps 3 and 4 reduce to 2L - H. Asserted for all 144 combinations so
    the step-by-step implementation cannot drift from the arithmetic."""
    for house in range(12):
        for lord in range(12):
            landed = advance_from_lord(lord, count_to_lord(house, lord))
            assert landed == (2 * lord - house) % 12


def test_all_twelve_padas_are_returned_in_order():
    # Mars in Ge (dual) beats Ketu in Aq (fixed) by 15.5.1 rule 4, so the
    # 8th house in Scorpio resolves without the caller naming a lord.
    signs = {g: g for g in range(9)}
    signs[int(Graha.KETU)] = R["Aq"]
    lords = arudha_service.resolve_dual_lords(
        {g: s * 30.0 for g, s in signs.items()}, advancement_known=False
    )
    padas = all_arudha_padas(lagna_sign=R["Ar"], graha_signs=signs,
                             stronger_lord=lords)
    assert [p.house for p in padas] == list(range(1, 13))
    assert [p.symbol for p in padas] == [f"A{n}" for n in range(1, 13)]


# --------------------------------------------------------------------------
# "in all the divisional charts"
# --------------------------------------------------------------------------

def test_arudhas_can_be_taken_in_a_divisional_chart():
    """§9.2's opening: "in all the divisional charts".

    The engine takes signs, so a caller passes the divisional chart's signs and
    gets that chart's arudhas. Demonstrated here with D-9 rather than left as
    a claim in a docstring.
    """
    from hora.charts.vargas import d9_navamsa

    longitudes = {g: g * 37.5 + 4.0 for g in range(9)}
    rasi_signs = {g: int(lon // 30) for g, lon in longitudes.items()}
    navamsa_signs = {g: d9_navamsa(lon).sign for g, lon in longitudes.items()}

    rasi = arudha_pada(1, rasi_signs[int(Graha.SUN)], rasi_signs)
    navamsa = arudha_pada(1, navamsa_signs[int(Graha.SUN)], navamsa_signs)
    # Both are well-formed; the point is that the divisional chart is accepted
    # and produces its own answer.
    assert 0 <= rasi.sign <= 11
    assert 0 <= navamsa.sign <= 11
    assert navamsa.house_sign == navamsa_signs[int(Graha.SUN)]


# --------------------------------------------------------------------------
# Naming
# --------------------------------------------------------------------------

def test_the_an_notation_covers_all_twelve():
    assert ARUDHA_SYMBOLS == {n: f"A{n}" for n in range(1, 13)}


def test_the_two_special_cases_are_named():
    """"Arudha pada of lagna is denoted as AL (arudha lagna) and arudha pada
    of 12th house is denoted as UL (upapada lagna)." """
    assert ARUDHA_SPECIAL_SYMBOLS == {1: "AL", 12: "UL"}
    assert ARUDHA_SPECIAL_NAMES == {1: "Arudha Lagna", 12: "Upapada Lagna"}


def test_the_generic_names_are_carried():
    """"Arudha pada of a house is simply called arudha or pada also." """
    assert ARUDHA_GENERIC_NAMES == ("arudha pada", "arudha", "pada")
    payload = arudha_service.one(1, R["Ar"], {g: g for g in range(9)})
    assert payload["generic_names"] == ["arudha pada", "arudha", "pada"]
    assert arudha_service.rules()["generic_names"] == list(ARUDHA_GENERIC_NAMES)


def test_the_rules_endpoint_states_all_six_steps():
    payload = arudha_service.rules()
    assert [s["number"] for s in payload["steps"]] == [1, 2, 3, 4, 5, 6]
    assert "zodiacal direction always" in payload["steps"][2]["text"]
    assert "1st or 7th" in payload["steps"][4]["text"]


# --------------------------------------------------------------------------
# Example 29 — Chart 1, all twelve arudhas
#
# The section's only fully worked chart. It exercises the whole chain: two of
# its houses fall in co-owned rasis (the 3rd in Sc, the 6th in Aq), so the
# lords come from §15.5.1's cascade rather than from the caller, and both are
# settled by that section's rule 1 — "he is stronger... being with 2 other
# planets", which is exactly what the book says.
#
# It also carries chara karaka labels on every graha, so it doubles as a second
# independent check of chapter 8 on a chart that chapter never used.
# --------------------------------------------------------------------------

#: Chart 1 — April 9 2000, 5:55 pm (4:00 West), 71 W 12, 42 N 30.
CHART_1_LONGITUDES = {
    int(Graha.SUN): R["Pi"] * 30 + 26 + 29 / 60,        # 26 Pi 29 (AK)
    int(Graha.MOON): R["Ge"] * 30 + 4 + 45 / 60,        # 4 Ge 45 (GK)
    int(Graha.MARS): R["Ar"] * 30 + 19 + 9 / 60,        # 19 Ar 09 (MK)
    int(Graha.MERCURY): R["Pi"] * 30 + 1 + 36 / 60,     # 1 Pi 36 (DK)
    int(Graha.JUPITER): R["Ar"] * 30 + 17 + 21 / 60,    # 17 Ar 21 (PiK)
    int(Graha.VENUS): R["Pi"] * 30 + 10 + 1 / 60,       # 10 Pi 01 (PK)
    int(Graha.SATURN): R["Ar"] * 30 + 22 + 41 / 60,     # 22 Ar 41 (BK)
    int(Graha.RAHU): R["Cn"] * 30 + 5 + 55 / 60,        # 5 Cn 55 (AmK)
    int(Graha.KETU): R["Cp"] * 30 + 5 + 55 / 60,        # 5 Cp 55
}
CHART_1_SIGNS = {g: int(lon // 30) for g, lon in CHART_1_LONGITUDES.items()}
CHART_1_LAGNA = R["Vi"]                                  # Asc 10 Vi 58

#: The twelve results as printed, with the house sign, lord, count and the
#: sign step 4 lands on — so a failure says which step diverged.
EXAMPLE_29 = [
    # house, house sign, lord,     lord sign, count, step 4, exception, arudha
    (1,  "Vi", Graha.MERCURY, "Pi",  7, "Vi", 1,    "Ge"),
    (2,  "Li", Graha.VENUS,   "Pi",  6, "Le", None, "Le"),
    (3,  "Sc", Graha.MARS,    "Ar",  6, "Vi", None, "Vi"),
    (4,  "Sg", Graha.JUPITER, "Ar",  5, "Le", None, "Le"),
    (5,  "Cp", Graha.SATURN,  "Ar",  4, "Cn", 7,    "Ar"),
    (6,  "Aq", Graha.SATURN,  "Ar",  3, "Ge", None, "Ge"),
    (7,  "Pi", Graha.JUPITER, "Ar",  2, "Ta", None, "Ta"),
    (8,  "Ar", Graha.MARS,    "Ar",  1, "Ar", 1,    "Cp"),
    (9,  "Ta", Graha.VENUS,   "Pi", 11, "Cp", None, "Cp"),
    (10, "Ge", Graha.MERCURY, "Pi", 10, "Sg", 7,    "Vi"),
    (11, "Cn", Graha.MOON,    "Ge", 12, "Ta", None, "Ta"),
    (12, "Le", Graha.SUN,     "Pi",  8, "Li", None, "Li"),
]


@pytest.mark.parametrize("row", EXAMPLE_29, ids=[f"A{r[0]}" for r in EXAMPLE_29])
def test_example_29_reproduces_step_by_step(row):
    house, house_sign_, lord, lord_sign_, count, landed, exception, arudha = row
    padas = arudha_service.table(
        CHART_1_LAGNA, CHART_1_SIGNS,
        graha_longitudes=CHART_1_LONGITUDES, include_steps=False,
    )["padas"]
    pada = padas[house - 1]

    assert pada["house_sign"] == R[house_sign_], "step 1"
    assert pada["lord"] == int(lord), "step 2"
    assert pada["lord_sign"] == R[lord_sign_], "step 2"
    assert pada["count"] == count, "step 3"
    assert pada["before_exception"] == R[landed], "step 4"
    assert pada["exception_position"] == exception, "step 5"
    assert pada["sign"] == R[arudha], "step 6"


def test_example_29_needs_no_stronger_lord_from_the_caller():
    """The 3rd and 6th houses fall in Scorpio and Aquarius.

    "Lord is Mars - he is stronger than Ketu, being with 2 other planets" and
    "Lord is Saturn - he is stronger than Rahu, being with 2 other planets".
    Both are §15.5.1 rule 1, and the cascade reaches them unaided.
    """
    from hora.charts.colord import stronger

    for rasi, winner in ((Rasi.SCORPIO, Graha.MARS), (Rasi.AQUARIUS, Graha.SATURN)):
        verdict = stronger(rasi, CHART_1_LONGITUDES, purpose="arudha")
        assert verdict.winner == int(winner)
        assert verdict.decided_by == "1", "the book decides both by planet count"
        assert "2 other planets" in verdict.reason


def test_example_29_names_al_and_ul():
    padas = arudha_service.table(
        CHART_1_LAGNA, CHART_1_SIGNS,
        graha_longitudes=CHART_1_LONGITUDES, include_steps=False,
    )["padas"]
    assert padas[0]["special_symbol"] == "AL"
    assert padas[0]["sign"] == R["Ge"], "AL is in Ge"
    assert padas[11]["special_symbol"] == "UL"
    assert padas[11]["sign"] == R["Li"], "UL is in Li"


def test_example_29_works_from_signs_alone():
    """Both co-owned houses are settled by rule 1, which needs only signs."""
    padas = arudha_service.table(
        CHART_1_LAGNA, CHART_1_SIGNS, include_steps=False
    )["padas"]
    assert [p["sign"] for p in padas] == [R[row[7]] for row in EXAMPLE_29]


def test_chart_1_also_confirms_the_chapter_8_chara_karakas():
    """Chart 1 labels every graha with its chara karaka.

    Chapter 8 was verified against Example 28 and Exercise 11; this is a third
    chart, from a different chapter, agreeing independently.
    """
    from hora.charts.karaka import chara_karakas

    printed = {
        "Sun": "AK", "Rahu": "AmK", "Saturn": "BK", "Mars": "MK",
        "Jupiter": "PiK", "Venus": "PK", "Moon": "GK", "Mercury": "DK",
    }
    # Chara karakas exclude Ketu, per section 8.1.
    longitudes = {g: lon for g, lon in CHART_1_LONGITUDES.items()
                  if g != int(Graha.KETU)}
    for karaka in chara_karakas(longitudes):
        assert karaka.symbol == printed[karaka.graha_name], karaka.graha_name


# --------------------------------------------------------------------------
# Table 18 — specific names of arudha padas
# --------------------------------------------------------------------------

#: Table 18 exactly as printed.
TABLE_18 = {
    1: ["Arudha lagna", "Pada lagna", "Arudha", "Pada"],
    2: ["Dhanarudha", "Vittarudha", "Dhana pada", "Vitta pada"],
    3: ["Bhatrarudha", "Bhratri pada", "Vikramarudha", "Vikrama pada"],
    4: ["Matri pada", "Vahana pada", "Sukha pada", "Matrarudha",
        "Vahanarudha", "Sukharudha"],
    5: ["Mantra pada", "Mantrarudha", "Putrarudha", "Putra pada",
        "Buddhi pada"],
    6: ["Roga pada", "Satru pada", "Rogarudha", "Satrarudha"],
    7: ["Dara pada", "Dararudha"],
    8: ["Mrityu pada", "Kashta pada", "Kashtarudha", "Randhrarudha"],
    9: ["Bhagya pada", "Bhagyarudha", "Pitri pada", "Pitrarudha",
        "Dharma pada", "Guru pada"],
    10: ["Karma pada", "Karmarudha", "Swarga pada", "Swargarudha",
         "Rajya pada"],
    11: ["Labha pada", "Labharudha"],
    12: ["Upapada lagna", "Upapada", "Gaunapada", "Vyayarudha", "Moksha pada"],
}


@pytest.mark.parametrize("house", range(1, 13))
def test_table_18_matches_the_book(house):
    from hora.charts.arudha import ARUDHA_SPECIFIC_NAMES

    assert list(ARUDHA_SPECIFIC_NAMES[house]) == TABLE_18[house]


def test_table_18_keeps_the_books_inconsistent_row():
    """A3 prints "Bhatrarudha" and "Bhratri pada" — the first missing the r.

    Regularising it would be an unmarked correction in transcribed data, which
    is what D-18's discipline exists to prevent. Recorded as D-21.
    """
    from hora.charts.arudha import ARUDHA_SPECIFIC_NAMES

    names = ARUDHA_SPECIFIC_NAMES[3]
    assert "Bhatrarudha" in names
    assert "Bhratri pada" in names
    assert "Bhratrarudha" not in names


def test_table_18_is_returned_per_pada_and_in_the_rules():
    pada = arudha_service.one(9, R["Ar"], {g: g for g in range(9)})
    assert pada["specific_names"] == TABLE_18[9]

    rows = arudha_service.rules()["specific_names"]
    assert [r["house"] for r in rows] == list(range(1, 13))
    assert {r["symbol"] for r in rows} == {f"A{n}" for n in range(1, 13)}
    assert sum(len(r["names"]) for r in rows) == 51


def test_the_special_symbols_agree_with_table_18():
    """A1's list opens with "Arudha lagna" and A12's with "Upapada lagna",
    which are exactly the two special cases §9.2 names."""
    assert TABLE_18[1][0] == "Arudha lagna"
    assert TABLE_18[12][0] == "Upapada lagna"
    assert ARUDHA_SPECIAL_NAMES[1] == "Arudha Lagna"
    assert ARUDHA_SPECIAL_NAMES[12] == "Upapada Lagna"


# --------------------------------------------------------------------------
# Exercise 12 — Chart 2, arudhas in a DIVISIONAL chart
#
# The exercise is set in D-16, not the rasi chart, so it exercises §9.2's
# opening claim — "in all the divisional charts" — end to end. Its two
# co-owned houses are settled by §15.5.1 rule 1, and the exercise's hint
# states that reasoning outright.
# --------------------------------------------------------------------------

#: Chart 2 — April 9 2000, 5:55 pm (5:00 West), 71 W 12, 42 N 30. Rasi
#: longitudes; the exercise works in the D-16 built from them.
CHART_2_RASI = {
    int(Graha.SUN): R["Pi"] * 30 + 26 + 32 / 60,        # 26 Pi 32 (AK)
    int(Graha.MOON): R["Ge"] * 30 + 5 + 21 / 60,        # 5 Ge 21 (GK)
    int(Graha.MARS): R["Ar"] * 30 + 19 + 11 / 60,       # 19 Ar 11 (MK)
    int(Graha.MERCURY): R["Pi"] * 30 + 1 + 39 / 60,     # 1 Pi 39 (DK)
    int(Graha.JUPITER): R["Ar"] * 30 + 17 + 22 / 60,    # 17 Ar 22 (PiK)
    int(Graha.VENUS): R["Pi"] * 30 + 10 + 4 / 60,       # 10 Pi 04 (PK)
    int(Graha.SATURN): R["Ar"] * 30 + 22 + 42 / 60,     # 22 Ar 42 (BK)
    int(Graha.RAHU): R["Cn"] * 30 + 5 + 55 / 60,        # 5 Cn 55 (AmK)
    int(Graha.KETU): R["Cp"] * 30 + 5 + 55 / 60,        # 5 Cp 55
}
CHART_2_ASC_RASI = R["Vi"] * 30 + 22 + 41 / 60          # Asc 22 Vi 41

#: The D-16 placements as the printed chart shows them.
CHART_2_D16 = {
    int(Graha.SUN): "Aq", int(Graha.MOON): "Aq", int(Graha.MARS): "Aq",
    int(Graha.MERCURY): "Sg", int(Graha.JUPITER): "Cp",
    int(Graha.VENUS): "Ta", int(Graha.SATURN): "Ar",
    int(Graha.RAHU): "Cn", int(Graha.KETU): "Cn",
}

#: "AL in Aq, A2 in Ar, A3 in Sg, A4 in Sc, A5 in Sg, A6 in Aq, A7 in Pi,
#:  A8 in Vi, A9 in Ta, A10 in Sg, A11 in Sg, UL in Aq."
EXERCISE_12 = ["Aq", "Ar", "Sg", "Sc", "Sg", "Aq", "Pi", "Vi", "Ta", "Sg",
               "Sg", "Aq"]


def _chart_2_d16_signs():
    from hora.charts.vargas import d16_shodasamsa

    return {g: d16_shodasamsa(lon).sign for g, lon in CHART_2_RASI.items()}


@pytest.mark.parametrize("graha,sign", sorted(CHART_2_D16.items()))
def test_chart_2_d16_placements_match_the_printed_chart(graha, sign):
    """Before the arudhas: the D-16 itself must be right.

    A third check of chapter 6's D-16, on a chart that chapter never used.
    """
    assert _chart_2_d16_signs()[graha] == R[sign]


def test_chart_2_d16_lagna_is_sagittarius():
    from hora.charts.vargas import d16_shodasamsa

    assert d16_shodasamsa(CHART_2_ASC_RASI).sign == R["Sg"]


def test_exercise_12_hint_reproduces_both_co_lord_decisions():
    """"Mars is with 2 other planets and Ketu is with only one planet...
    Saturn is alone and Rahu is with another planet."

    Both are §15.5.1 rule 1, decided on the D-16 placements.
    """
    from hora.charts.colord import stronger

    signs = _chart_2_d16_signs()
    as_longitudes = {g: s * 30.0 for g, s in signs.items()}
    for rasi, winner in ((Rasi.SCORPIO, Graha.MARS), (Rasi.AQUARIUS, Graha.RAHU)):
        verdict = stronger(rasi, as_longitudes, purpose="arudha",
                           advancement_known=False)
        assert verdict.winner == int(winner)
        assert verdict.decided_by == "1"


@pytest.mark.parametrize("house,expected", list(enumerate(EXERCISE_12, start=1)))
def test_exercise_12_answer(house, expected):
    from hora.charts.vargas import d16_shodasamsa

    signs = _chart_2_d16_signs()
    lagna = d16_shodasamsa(CHART_2_ASC_RASI).sign
    padas = arudha_service.table(lagna, signs, include_steps=False)["padas"]
    assert padas[house - 1]["sign"] == R[expected]


def test_exercise_12_is_a_divisional_chart_not_the_rasi_chart():
    """The answers differ between D-16 and the rasi chart, so this really does
    exercise "in all the divisional charts"."""
    from hora.charts.vargas import d16_shodasamsa

    d16 = arudha_service.table(
        d16_shodasamsa(CHART_2_ASC_RASI).sign, _chart_2_d16_signs(),
        include_steps=False,
    )["padas"]
    rasi_signs = {g: int(lon // 30) for g, lon in CHART_2_RASI.items()}
    rasi = arudha_service.table(
        int(CHART_2_ASC_RASI // 30), rasi_signs,
        graha_longitudes=CHART_2_RASI, include_steps=False,
    )["padas"]
    assert [p["sign"] for p in d16] != [p["sign"] for p in rasi]


# --------------------------------------------------------------------------
# §9.5 — Graha Arudhas
#
# The dual of §9.2: a bhava arudha starts from a house's sign and looks up its
# lord; a graha arudha starts from a planet's sign and looks up the sign that
# planet owns. Steps 3 to 6 are shared, and the module reuses them rather than
# restating them.
# --------------------------------------------------------------------------

def test_section_9_5_worked_example():
    """"if the planet we are interested in is Sun and he is Gemini, we count
    signs from Gemini to Leo and get 3... we count 3 signs from Leo and we end
    up in Libra"."""
    from hora.charts.graha_arudha import graha_arudha

    signs = {g: g for g in range(9)}
    signs[int(Graha.SUN)] = R["Ge"]
    arudha = graha_arudha(int(Graha.SUN), signs)

    assert arudha.graha_sign == R["Ge"], "step 1"
    assert arudha.owned_sign == R["Le"], "step 2 — the Sun owns Leo"
    assert arudha.count == 3, "step 3"
    assert arudha.before_exception == R["Li"], "step 4"
    assert arudha.exception_applied is False, "step 5"
    assert arudha.sign == R["Li"], "step 6"
    assert [s.number for s in arudha.steps] == [1, 2, 3, 4, 5, 6]


def test_the_note_names_the_five_two_sign_owners():
    """"Mars, Mercury, Jupiter, Venus and Saturn own 2 signs each"."""
    from hora.charts.graha_arudha import TWO_SIGN_OWNERS

    assert TWO_SIGN_OWNERS == {
        int(Graha.MARS), int(Graha.MERCURY), int(Graha.JUPITER),
        int(Graha.VENUS), int(Graha.SATURN),
    }


def test_the_one_sign_owners_need_no_comparison():
    """Sun and Moon own one each; Rahu and Ketu co-own one each per §9.2."""
    from hora.charts.graha_arudha import owned_sign

    signs = {g: g for g in range(9)}
    for graha, expected in ((Graha.SUN, "Le"), (Graha.MOON, "Cn"),
                            (Graha.RAHU, "Aq"), (Graha.KETU, "Sc")):
        sign, decided_by, why = owned_sign(int(graha), signs)
        assert sign == R[expected]
        assert decided_by is None, "no comparison was needed"
        assert "owns only" in why


@pytest.mark.parametrize("graha", [
    Graha.MARS, Graha.MERCURY, Graha.JUPITER, Graha.VENUS, Graha.SATURN,
])
def test_a_two_sign_owner_is_always_resolvable(graha):
    """§15.5.2's note: "this rule will surely resolve the tie, because the two
    rasis owned by each planet have a different oddity".

    Asserted over every arrangement of the planet itself, so the guarantee is
    demonstrated rather than trusted.
    """
    from hora.charts.graha_arudha import owned_sign

    for sign in range(12):
        signs = {g: g for g in range(9)}
        signs[int(graha)] = sign
        chosen, decided_by, _why = owned_sign(int(graha), signs)
        assert chosen in GRAHA_OWNS[graha]
        assert decided_by is not None


def test_the_two_owned_signs_always_differ_in_oddity():
    """The property §15.5.2's guarantee rests on."""
    from hora.charts.graha_arudha import TWO_SIGN_OWNERS
    from hora.core.const import RASI_IS_ODD

    for graha in TWO_SIGN_OWNERS:
        first, second = GRAHA_OWNS[graha]
        assert RASI_IS_ODD[first] != RASI_IS_ODD[second], GRAHA_NAMES[graha]


def test_graha_arudhas_never_need_a_dasa_input():
    """OI-29 recorded an expectation that this would need dasa analysis.

    It does not. §15.5.2's rule 6 and §15.5.1's rule 5a are the only branches
    that touch dasa lengths, and neither is reached: rule 4 settles every
    two-sign comparison first.
    """
    from hora.charts.graha_arudha import TWO_SIGN_OWNERS, owned_sign

    reached = set()
    for graha in TWO_SIGN_OWNERS:
        for sign in range(12):
            signs = {g: g for g in range(9)}
            signs[int(graha)] = sign
            _chosen, decided_by, _why = owned_sign(int(graha), signs)
            reached.add(decided_by)
    assert "6" not in reached, "rule 6 is the only dasa-adjacent branch"


def test_all_nine_planets_get_an_arudha():
    """"arudha padas of all the nine planets (grahas) are also defined"."""
    padas = arudha_service.graha_table({g: g for g in range(9)},
                                       include_steps=False)["arudhas"]
    assert len(padas) == 9
    assert [p["graha"] for p in padas] == list(range(9))
    assert all(0 <= p["sign"] <= 11 for p in padas)


def test_step_5_is_the_same_exception_as_section_9_2():
    """Both sections state it identically, and both use the same helper."""
    from hora.charts.graha_arudha import graha_arudha

    # Sun in Leo: he owns Leo, so the count is 1 and step 4 stays put —
    # the 1st from the original, so the exception fires.
    signs = {g: g for g in range(9)}
    signs[int(Graha.SUN)] = R["Le"]
    arudha = graha_arudha(int(Graha.SUN), signs)
    assert arudha.count == 1
    assert arudha.before_exception == R["Le"]
    assert arudha.exception_position == 1
    assert arudha.sign == R["Ta"], "the 10th from Leo"


def test_graha_arudhas_work_in_a_divisional_chart():
    """"in the divisional chart of interest" — same claim as §9.2."""
    from hora.charts.vargas import d16_shodasamsa

    d16 = {g: d16_shodasamsa(lon).sign for g, lon in CHART_2_RASI.items()}
    rasi = {g: int(lon // 30) for g, lon in CHART_2_RASI.items()}
    in_d16 = arudha_service.graha_table(d16, include_steps=False)["arudhas"]
    in_rasi = arudha_service.graha_table(rasi, include_steps=False)["arudhas"]
    assert [p["sign"] for p in in_d16] != [p["sign"] for p in in_rasi]


def test_the_graha_rules_endpoint_states_the_procedure_and_the_note():
    payload = arudha_service.graha_rules()
    assert [s["number"] for s in payload["steps"]] == [1, 2, 3, 4, 5, 6]
    assert "Mars, Mercury, Jupiter, Venus and Saturn own 2 signs each" in payload["note"]
    assert payload["stronger_sign_section"] == "15.5.2 Stronger Rasi"
    needs = {r["graha_name"] for r in payload["ownership"] if r["needs_comparison"]}
    assert needs == {"Mars", "Mercury", "Jupiter", "Venus", "Saturn"}


def test_a_missing_position_is_refused():
    from hora.charts.graha_arudha import GrahaArudhaError, graha_arudha

    with pytest.raises(GrahaArudhaError, match="Sun"):
        graha_arudha(int(Graha.SUN), {int(Graha.MOON): 0})


# --------------------------------------------------------------------------
# Example 30 — all nine graha arudhas in Chart 1
#
# The same chart as Example 29, so bhava and graha arudhas are checked against
# one another's source. Five planets own two signs, and the book says which is
# stronger and why for four of them; the fifth it declines to explain, leaving
# it to §15.5.2. That fifth is the real test.
# --------------------------------------------------------------------------

#: (owned sign selected, count, exception position, arudha sign).
EXAMPLE_30 = [
    (Graha.SUN,     "Le",  6, None, "Cp"),
    (Graha.MOON,    "Cn",  2, None, "Le"),
    (Graha.MARS,    "Ar",  1, 1,    "Cp"),
    (Graha.MERCURY, "Ge",  4, 7,    "Ge"),
    (Graha.JUPITER, "Pi", 12, None, "Aq"),
    (Graha.VENUS,   "Li",  8, None, "Ta"),
    (Graha.SATURN,  "Cp", 10, 7,    "Cn"),
    (Graha.RAHU,    "Aq",  8, None, "Vi"),
    (Graha.KETU,    "Sc", 11, None, "Vi"),
]


@pytest.mark.parametrize("row", EXAMPLE_30, ids=[r[0].name for r in EXAMPLE_30])
def test_example_30_reproduces_step_by_step(row):
    graha, owned, count, exception, arudha = row
    table = arudha_service.graha_table(
        CHART_1_SIGNS, CHART_1_LONGITUDES, include_steps=False
    )["arudhas"]
    entry = table[int(graha)]

    assert entry["graha_sign"] == CHART_1_SIGNS[int(graha)], "step 1"
    assert entry["owned_sign"] == R[owned], "step 2"
    assert entry["count"] == count, "step 3"
    assert entry["exception_position"] == exception, "step 5"
    assert entry["sign"] == R[arudha], "step 6"


def test_example_30_agrees_with_the_books_stated_reasons():
    """The book names *why* it picks each owned sign, for four of the five.

    "Ar is stronger as it contains more planets", "Ge is stronger as it has
    Moon and Vi is empty", "Pi is stronger as it has 3 planets and Sg is
    empty", "Cp is stronger as it has Ketu and Aq is empty" — all four are
    §15.5.2 rule 1, the planet count.
    """
    table = arudha_service.graha_table(
        CHART_1_SIGNS, CHART_1_LONGITUDES, include_steps=False
    )["arudhas"]
    for graha in (Graha.MARS, Graha.MERCURY, Graha.JUPITER, Graha.SATURN):
        assert table[int(graha)]["owned_decided_by"] == "1", GRAHA_NAMES[graha]


def test_example_30_settles_the_case_the_book_declines_to_explain():
    """Venus owns Ta and Li, and both are empty in Chart 1.

    "Li is stronger (it will become clear after reading the chapter on
    'Strength of Planets and Rasis')." The book gives the answer and no
    reasoning, so this is the one item that genuinely exercises §15.5.2 rather
    than restating a planet count.

    Rule 4 settles it: Venus lords both signs and sits in Pisces, an even rasi.
    Libra is odd, so its lord is in a rasi of *different* oddity; Taurus is
    even, so its lord is in a rasi of the *same* oddity. Libra wins.
    """
    from hora.charts.graha_arudha import owned_sign

    sign, decided_by, why = owned_sign(
        int(Graha.VENUS), CHART_1_SIGNS, CHART_1_LONGITUDES
    )
    assert sign == R["Li"]
    assert decided_by == "4", "not the planet count — both signs are empty"
    assert "rule 4" in why

    from hora.core.const import RASI_IS_ODD

    venus_sign = CHART_1_SIGNS[int(Graha.VENUS)]
    assert not RASI_IS_ODD[venus_sign], "Venus is in Pisces, an even rasi"
    assert RASI_IS_ODD[R["Li"]] and not RASI_IS_ODD[R["Ta"]]


def test_example_30_both_exception_positions_are_exercised():
    """Mars from the 1st, Mercury and Saturn from the 7th."""
    table = arudha_service.graha_table(
        CHART_1_SIGNS, CHART_1_LONGITUDES, include_steps=False
    )["arudhas"]
    fired = {
        e["graha_name"]: e["exception_position"]
        for e in table if e["exception_applied"]
    }
    assert fired == {"Mars": 1, "Mercury": 7, "Saturn": 7}


def test_example_30_needs_no_input_beyond_the_chart():
    """No stronger-sign choice is supplied; §15.5.2 resolves all five."""
    table = arudha_service.graha_table(CHART_1_SIGNS, include_steps=False)["arudhas"]
    assert [e["sign"] for e in table] == [R[row[4]] for row in EXAMPLE_30]


def test_chart_1_answers_both_of_its_examples():
    """Example 29 gives the twelve bhava arudhas of Chart 1 and Example 30 the
    nine graha arudhas. Both from the same fixture, so a wrong chart would
    break both rather than silently pass one."""
    bhava = arudha_service.table(
        CHART_1_LAGNA, CHART_1_SIGNS,
        graha_longitudes=CHART_1_LONGITUDES, include_steps=False,
    )["padas"]
    graha = arudha_service.graha_table(
        CHART_1_SIGNS, CHART_1_LONGITUDES, include_steps=False
    )["arudhas"]
    assert [p["sign"] for p in bhava] == [R[row[7]] for row in EXAMPLE_29]
    assert [e["sign"] for e in graha] == [R[row[4]] for row in EXAMPLE_30]


# --------------------------------------------------------------------------
# Exercise 13 — all nine graha arudhas in Chart 2, a D-16 chart
#
# The graha counterpart of Exercise 12, and the only worked graha arudha set
# in a divisional chart. Its hint states which of each two-sign planet's signs
# is stronger, so the intermediate is checked as well as the answer.
# --------------------------------------------------------------------------

#: The hint: "Out of the 2 signs owned by Mars, Mercury, Jupiter, Venus and
#: Saturn, Ar, Ta, Vi, Sg and Aq are stronger (respectively)."
#:
#: Read by ownership, not by the stated order — see the test below.
EXERCISE_13_STRONGER = {
    Graha.MARS: "Ar", Graha.VENUS: "Ta", Graha.MERCURY: "Vi",
    Graha.JUPITER: "Sg", Graha.SATURN: "Aq",
}

#: "Sun - Sc, Moon - Sg, Mars - Ge, Mercury - Pi, Jupiter - Sc, Venus - Aq,
#:  Saturn - Sg, Rahu - Vi, Ketu - Pi."
EXERCISE_13 = ["Sc", "Sg", "Ge", "Pi", "Sc", "Aq", "Sg", "Vi", "Pi"]


def test_exercise_13_hint_maps_by_ownership_not_by_its_stated_order():
    """The hint's "respectively" does not line up, and cannot.

    Taken literally it pairs Mercury with Ta and Jupiter with Vi, and neither
    planet owns either sign. The five signs are listed in zodiacal order and
    each belongs to exactly one of the five planets, so the intended mapping is
    unambiguous — but it is not the one the word "respectively" states.

    Recorded here rather than silently reinterpreted.
    """
    literal = dict(zip(
        [Graha.MARS, Graha.MERCURY, Graha.JUPITER, Graha.VENUS, Graha.SATURN],
        ["Ar", "Ta", "Vi", "Sg", "Aq"],
    ))
    for graha, sign in literal.items():
        if graha in (Graha.MERCURY, Graha.JUPITER, Graha.VENUS):
            assert R[sign] not in GRAHA_OWNS[graha], (
                f"{GRAHA_NAMES[graha]} does not own {sign}"
            )
    # By ownership every one of the five signs resolves to a single planet.
    for graha, sign in EXERCISE_13_STRONGER.items():
        assert R[sign] in GRAHA_OWNS[graha]


@pytest.mark.parametrize("graha,sign", sorted(
    EXERCISE_13_STRONGER.items(), key=lambda kv: int(kv[0])))
def test_exercise_13_stronger_owned_signs_match_the_hint(graha, sign):
    """The intermediate, not just the answer.

    Four are settled by §15.5.2 rule 1 (the planet count) and Mercury's by
    rule 4 (the oddity of its lord's sign), so the exercise exercises more of
    that cascade than Example 30 did.
    """
    from hora.charts.graha_arudha import owned_sign

    chosen, decided_by, _why = owned_sign(int(graha), _chart_2_d16_signs())
    assert chosen == R[sign]
    assert decided_by in {"1", "4"}


def test_exercise_13_mercury_needs_rule_4():
    """Ge and Vi are both empty in Chart 2's D-16, so the count ties.

    Mercury lords both and sits in Sagittarius, an odd rasi. Virgo is even, so
    its lord is in a rasi of different oddity; Gemini is odd, so its lord is in
    a rasi of the same oddity. Virgo wins.
    """
    from hora.charts.graha_arudha import owned_sign

    signs = _chart_2_d16_signs()
    occupied = set(signs.values())
    assert R["Ge"] not in occupied and R["Vi"] not in occupied

    chosen, decided_by, _why = owned_sign(int(Graha.MERCURY), signs)
    assert chosen == R["Vi"]
    assert decided_by == "4"


@pytest.mark.parametrize("graha,expected", list(enumerate(EXERCISE_13)))
def test_exercise_13_answer(graha, expected):
    table = arudha_service.graha_table(
        _chart_2_d16_signs(), include_steps=False
    )["arudhas"]
    assert table[graha]["sign"] == R[expected]


def test_exercise_13_exercises_both_exception_positions():
    table = arudha_service.graha_table(
        _chart_2_d16_signs(), include_steps=False
    )["arudhas"]
    fired = {
        e["graha_name"]: e["exception_position"]
        for e in table if e["exception_applied"]
    }
    assert fired == {"Sun": 1, "Mercury": 7, "Venus": 1}


def test_chart_2_answers_both_of_its_exercises():
    """Exercise 12 gives Chart 2's twelve bhava arudhas and Exercise 13 its
    nine graha arudhas, both in D-16 and both from the same fixture."""
    from hora.charts.vargas import d16_shodasamsa

    signs = _chart_2_d16_signs()
    bhava = arudha_service.table(
        d16_shodasamsa(CHART_2_ASC_RASI).sign, signs, include_steps=False
    )["padas"]
    graha = arudha_service.graha_table(signs, include_steps=False)["arudhas"]
    assert [p["sign"] for p in bhava] == [R[s] for s in EXERCISE_12]
    assert [e["sign"] for e in graha] == [R[s] for s in EXERCISE_13]
