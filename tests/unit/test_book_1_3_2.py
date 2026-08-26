"""§1.3.2 Rasis (signs) — Table 1, the three notations, and Exercise 1.

Table 1 is already pinned by `test_book_source_fidelity.py` against the PDF.
What was not pinned is the section's *prose*: what a longitude is, what range
it runs over, and the three notations the Notation paragraph introduces.

Added when the user reviewed §1.3.2 and asked for the section to be well typed
end to end. It turned up a real gap: `notation.parse` documented plain degrees
as a supported form and did not accept it, which is the form Exercise 1 gives
Jupiter in.
"""
import pytest

from hora.core import const as c
from hora.core.notation import (
    MAX_LONGITUDE,
    MIN_LONGITUDE,
    NotationError,
    all_forms,
    parse,
    to_rasi_dm,
    to_sign_dm,
)
from hora.services import reference_service

# --------------------------------------------------------------------------
# Table 1
# --------------------------------------------------------------------------

#: Table 1 as printed: name, Sanskrit name, symbol, start degree.
TABLE_1 = [
    ("Aries", "Mesha", "Ar", 0),
    ("Taurus", "Vrishabha", "Ta", 30),
    ("Gemini", "Mithuna", "Ge", 60),
    ("Cancer", "Karkataka", "Cn", 90),
    ("Leo", "Simha", "Le", 120),
    ("Virgo", "Kanya", "Vi", 150),
    ("Libra", "Thula", "Li", 180),
    ("Scorpio", "Vrischika", "Sc", 210),
    ("Sagittarius", "Dhanus", "Sg", 240),
    ("Capricorn", "Makara", "Cp", 270),
    ("Aquarius", "Kumbha", "Aq", 300),
    ("Pisces", "Meena", "Pi", 330),
]


@pytest.mark.parametrize("index,row", list(enumerate(TABLE_1)))
def test_table_1_names_symbols_and_bounds(index, row):
    name, sanskrit, symbol, start = row
    assert c.RASI_NAMES[index] == name
    assert c.RASI_NAMES_SA_BOOK[index].startswith(sanskrit)
    assert c.RASI_ABBR[index] == symbol
    assert index * 30 == start


def test_the_zodiac_is_twelve_equal_parts_of_thirty_degrees():
    """"The zodiac (sky) lasts 360° ... divided into 12 equal parts"."""
    assert len(c.RASI_NAMES) == 12
    assert MAX_LONGITUDE == 360.0
    assert MAX_LONGITUDE / 12 == 30.0


def test_two_rasis_carry_a_second_sanskrit_name():
    """Table 1 prints "Vrishabha/Vrisha" and "Karkataka/Karka"."""
    taurus = c.RASI_NAMES_SA_BOOK[1]
    cancer = c.RASI_NAMES_SA_BOOK[3]
    assert "Vrishabha" in taurus and "Vrisha" in taurus
    assert "Karkataka" in cancer and "Karka" in cancer


# --------------------------------------------------------------------------
# The longitude range
# --------------------------------------------------------------------------

def test_the_range_is_the_one_the_section_states():
    """"the longitude of any planet ... can be from 0°0'0" to 359°59'59"."""
    assert MIN_LONGITUDE == 0.0
    assert parse("0°0'0\"") == 0.0
    assert parse("359°59'59\"") == pytest.approx(359 + 59 / 60 + 59 / 3600)


@pytest.mark.parametrize("text", ["360", "360°0'0\"", "400", "999"])
def test_a_longitude_outside_the_zodiac_is_refused(text):
    """Wrapping silently would turn a typo into a plausible position."""
    with pytest.raises(NotationError, match="outside the zodiac"):
        parse(text)


def test_more_than_eleven_completed_signs_is_refused():
    with pytest.raises(NotationError, match="out of range"):
        parse("12s 0 0")


def test_zero_is_the_beginning_of_the_zodiac():
    """"0°0'0" corresponds to the beginning of the zodiac"."""
    assert parse("0") == 0.0
    assert to_rasi_dm(0.0).startswith("0 Ar")


# --------------------------------------------------------------------------
# The three notations
# --------------------------------------------------------------------------

def test_the_notation_paragraphs_worked_example():
    """"If a planet is at 221°37' ... that planet is in Scorpio ... Its
    advancement from the start of the rasi occupied by is 11°37'."

    The same position is written three ways, and all three must agree.
    """
    plain = parse("221°37'")
    assert plain == pytest.approx(221 + 37 / 60)
    assert int(plain // 30) == c.Rasi.SCORPIO
    assert plain % 30 == pytest.approx(11 + 37 / 60)

    # "11°37' in Sc", "11 Sc 37" and "7s 11° 37'" are the same point.
    assert parse("11 Sc 37") == pytest.approx(plain)
    assert parse("7s 11 37") == pytest.approx(plain)


def test_the_s_notation_counts_completed_signs():
    """"after completing 7 signs, advanced by 11°37' in the 8th sign"."""
    assert to_sign_dm(parse("221°37'")) == "7s 11d 37'"


def test_the_rasi_notation_is_relative_to_the_sign():
    assert to_rasi_dm(parse("221°37'")) == "11 Sc 37"


@pytest.mark.parametrize("text", ["94°19'", "94d19", "94 19", "94.3166667"])
def test_plain_degrees_parse_in_every_spelling(text):
    """The form §1.3.2 states first, and the one Exercise 1 uses.

    `parse` documented this as supported and did not accept it until this
    section was reviewed.
    """
    assert parse(text) == pytest.approx(94 + 19 / 60, abs=1e-6)


def test_a_sign_bearing_form_is_not_swallowed_by_the_plain_one():
    """"5s 17 45" must not be read as 5 degrees 17 minutes 45 seconds."""
    assert parse("5s 17 45") == pytest.approx(167.75)
    assert parse("25 Li 31") == pytest.approx(205 + 31 / 60)


def test_a_non_string_is_refused_rather_than_coerced():
    with pytest.raises(NotationError, match="expected a string"):
        parse(94.3167)          # type: ignore[arg-type]


def test_an_unknown_rasi_name_is_refused():
    with pytest.raises(NotationError, match="unknown rasi"):
        parse("25 Xx 31")


# --------------------------------------------------------------------------
# Exercise 1
# --------------------------------------------------------------------------

#: "Jupiter is at 94°19'. Mercury is at 5s 17° 45'. Venus is at 25 Li 31."
#: Answers: Jupiter Cancer 4°19'; Mercury Virgo 17°45'; Venus Libra 25°31'.
EXERCISE_1 = [
    ("Jupiter", "94°19'", "Cancer", 4, 19),
    ("Mercury", "5s 17° 45'", "Virgo", 17, 45),
    ("Venus", "25 Li 31", "Libra", 25, 31),
]


@pytest.mark.parametrize("row", EXERCISE_1, ids=[r[0] for r in EXERCISE_1])
def test_exercise_1(row):
    _who, text, rasi_name, degrees, minutes = row
    longitude = parse(text)
    assert c.RASI_NAMES[int(longitude // 30)] == rasi_name, "(a) the rasi occupied"
    assert longitude % 30 == pytest.approx(degrees + minutes / 60, abs=1e-9), (
        "(b) the advancement from the start of the rasi"
    )


@pytest.mark.parametrize("row", EXERCISE_1, ids=[r[0] for r in EXERCISE_1])
def test_exercise_1_through_the_service(row):
    _who, text, rasi_name, degrees, minutes = row
    payload = reference_service.resolve_notation(text)
    assert payload["rasi_name"] == rasi_name
    assert payload["degrees_in_rasi"] == pytest.approx(
        degrees + minutes / 60, abs=1e-6
    )
    assert payload["rasi_dm"] == f"{degrees} {c.RASI_ABBR[payload['rasi']]} {minutes}"


def test_exercise_1_answers_round_trip_through_every_notation():
    """Each answer re-rendered in all three forms must parse back unchanged."""
    for _who, text, _rasi, _d, _m in EXERCISE_1:
        longitude = parse(text)
        forms = all_forms(longitude)
        for key in ("sign_dm", "rasi_dm"):
            assert parse(str(forms[key])) == pytest.approx(longitude, abs=1e-6), key


# --------------------------------------------------------------------------
# Vargas are named here and defined later
# --------------------------------------------------------------------------

def test_vargas_are_named_in_this_section_and_defined_in_chapter_6():
    """"Each rasi again has many kinds of divisions and they are called
    'vargas'. They will be defined in detail later." """
    from hora.charts.vargas import VARGA_REGISTRY

    assert len(VARGA_REGISTRY) >= 16
    assert "D9" in VARGA_REGISTRY


def test_the_service_refuses_what_parse_refuses():
    """The service used to bypass `parse` for anything float() accepted.

    "400" came back as 10 Taurus, because the bare float skipped the range
    check and was then silently wrapped. Every input goes through `parse` now.
    """
    for text in ("400", "360", "-5", "25 Xx 31"):
        with pytest.raises(NotationError):
            reference_service.resolve_notation(text)


def test_the_service_still_accepts_a_plain_decimal():
    """The float() shortcut is gone; `parse` covers the case it existed for."""
    payload = reference_service.resolve_notation("94.3166667")
    assert payload["rasi_name"] == "Cancer"
    assert payload["degrees_in_rasi"] == pytest.approx(4 + 19 / 60, abs=1e-6)
