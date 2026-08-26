"""Every checkable claim in Chapter 1 of PVR Narasimha Rao's textbook.

Source: "Vedic Astrology: An Integrated Approach", Chapter 1 (Basic Concepts),
book pages 3-20. Section numbers below refer to the book.

These are the strongest evidence available short of running JHora itself: the
worked examples and the two conjunction timestamps in section 1.3.8.2 were
produced by the author's own software.
"""
import pytest

from hora.charts.bhava import house_from_sign
from hora.charts.chart import nakshatra_of
from hora.core.const import (
    GRAHA_NAMES,
    NAKSHATRA_LORD,
    NAKSHATRA_SPAN,
    RASI_NAMES,
    TITHI_LORD,
    YOGA_NAMES_BOOK,
)
from hora.core.names import NameScheme, name
from hora.core.notation import parse, to_rasi_dm, to_sign_dm
from hora.core.settings import Settings
from hora.core.timeutil import from_local, jd_to_local_str
from hora.panchanga.core import karana_at, paksha_at, tithi_at, yoga_at

IST = "Asia/Kolkata"


# --------------------------------------------------------------------------
# 1.3.2 Rasis and longitude notation  (Exercise 1)
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "notation,rasi,degrees",
    [
        ("5s 17 45", "Virgo", 17 + 45 / 60),
        ("25 Li 31", "Libra", 25 + 31 / 60),
    ],
)
def test_exercise_1_notation(notation, rasi, degrees):
    lon = parse(notation)
    assert RASI_NAMES[int(lon // 30)] == rasi
    assert lon % 30 == pytest.approx(degrees)


def test_exercise_1_jupiter_decimal():
    """Jupiter at 94 deg 19' is Cancer 4 deg 19'."""
    lon = 94 + 19 / 60
    assert RASI_NAMES[int(lon // 30)] == "Cancer"
    assert lon % 30 == pytest.approx(4 + 19 / 60)


def test_sign_notation_round_trips():
    """Book 1.3.2: '7s 11 37' means 11 deg 37' into the 8th sign, Scorpio."""
    lon = parse("7s 11 37")
    assert to_rasi_dm(lon) == "11 Sc 37"
    assert to_sign_dm(lon) == "7s 11d 37'"
    assert to_rasi_dm(94 + 19 / 60) == "4 Cn 19"


def test_table_1_rasi_definitions():
    """Book Table 1: names, Sanskrit names, symbols and 30-degree boundaries."""
    from hora.core.const import RASI_ABBR, RASI_NAMES_SA_BOOK

    book = [
        ("Aries", "Mesha", "Ar"), ("Taurus", "Vrishabha", "Ta"),
        ("Gemini", "Mithuna", "Ge"), ("Cancer", "Karkataka", "Cn"),
        ("Leo", "Simha", "Le"), ("Virgo", "Kanya", "Vi"),
        ("Libra", "Thula", "Li"), ("Scorpio", "Vrischika", "Sc"),
        ("Sagittarius", "Dhanus", "Sg"), ("Capricorn", "Makara", "Cp"),
        ("Aquarius", "Kumbha", "Aq"), ("Pisces", "Meena", "Pi"),
    ]
    for i, (english, sanskrit, symbol) in enumerate(book):
        assert RASI_NAMES[i] == english
        assert RASI_NAMES_SA_BOOK[i] == sanskrit
        assert RASI_ABBR[i] == symbol
        assert int((i * 30.0) // 30) == i                       # start of rasi
        assert int((i * 30.0 + 29 + 59 / 60 + 59 / 3600) // 30) == i   # end of rasi


def test_table_1_notation_example():
    """Book: 221 deg 37' is Scorpio, advanced 11 deg 37', written '11 Sc 37'."""
    lon = 221 + 37 / 60
    assert RASI_NAMES[int(lon // 30)] == "Scorpio"
    assert lon % 30 == pytest.approx(11 + 37 / 60)
    assert to_rasi_dm(lon) == "11 Sc 37"
    assert parse("11 Sc 37") == pytest.approx(lon)


def test_karana_is_half_a_tithi():
    """Book 1.3.10: each tithi is divided into 2 karanas."""
    for sun, moon in [(0.0, 5.0), (0.0, 13.0), (100.0, 250.0), (359.0, 12.0)]:
        assert karana_at(sun, moon) in (2 * tithi_at(sun, moon) - 1, 2 * tithi_at(sun, moon))


# --------------------------------------------------------------------------
# 1.3.3 Bhavas  (Exercise 2)
# --------------------------------------------------------------------------

def test_exercise_2_houses_from_lagna_and_from_moon():
    CN, AR, TA, CP = 3, 0, 1, 9
    assert [house_from_sign(AR, CN), house_from_sign(TA, CN), house_from_sign(CP, CN)] == [10, 11, 7]
    assert [house_from_sign(AR, TA), house_from_sign(TA, TA), house_from_sign(CP, TA)] == [12, 1, 9]


# --------------------------------------------------------------------------
# 1.3.6 Nakshatras  (Table 2)
# --------------------------------------------------------------------------

BOOK_NAKSHATRA_LORDS = ["Ketu", "Venus", "Sun", "Moon", "Mars",
                        "Rahu", "Jupiter", "Saturn", "Mercury"] * 3


def test_table_2_boundaries_are_exactly_13_20_each():
    for i in range(27):
        assert nakshatra_of(i * NAKSHATRA_SPAN + 1e-6)[0] == i
        assert nakshatra_of((i + 1) * NAKSHATRA_SPAN - 1e-6)[0] == i
    assert NAKSHATRA_SPAN == pytest.approx(13 + 20 / 60)


@pytest.mark.parametrize("i", range(27))
def test_table_2_vimsottari_lords(i):
    assert GRAHA_NAMES[NAKSHATRA_LORD[i]] == BOOK_NAKSHATRA_LORDS[i]


def test_table_2_first_three_nakshatra_ranges():
    """Book: 1st is 0-13d20' Ar, 2nd to 26d40' Ar, 3rd to 10d00' Ta."""
    assert nakshatra_of(0.0)[0] == 0
    assert nakshatra_of(parse("26 Ar 39"))[0] == 1
    assert nakshatra_of(parse("9 Ta 59"))[0] == 2
    assert nakshatra_of(parse("10 Ta 01"))[0] == 3


def test_abhijit_is_the_last_quarter_of_uttarashadha():
    """Book 1.3.6: 28-nakshatra scheme is used only for special chakras."""
    from hora.core.const import ABHIJIT_END, ABHIJIT_START

    # Uttarashadha runs 26 Sg 40 to 10 Cp 00; its last pada starts at 6 Cp 40.
    assert ABHIJIT_START == pytest.approx(parse("6 Cp 40"))
    assert ABHIJIT_END == pytest.approx(280 + NAKSHATRA_SPAN / 15.0)
    assert nakshatra_of(ABHIJIT_START + 1e-6)[0] == 20      # still Uttarashadha
    assert name("nakshatra28", 27) == "Abhijit"


# --------------------------------------------------------------------------
# 1.3.7 Solar calendar
# --------------------------------------------------------------------------

def test_solar_month_is_the_rasi_of_the_sun_and_day_is_degrees():
    from hora.panchanga.calendar import solar_date

    jd = from_local(1999, 5, 25, 12, 0, 0, tz_name=IST).jd_ut
    sd = solar_date(jd, Settings())
    assert sd.month_name == RASI_NAMES[sd.month]
    assert sd.day == int(sd.sun_longitude % 30) + 1
    assert 1 <= sd.day <= 31


# --------------------------------------------------------------------------
# 1.3.8 Tithis  (Table 3, Example 2, Exercise 3)
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "moon,sun,number,paksha,name_",
    [
        # Example 2: Moon 24d12' Ge, Sun 17d46' Sc -> 19th, Krishna Chaturthi
        (parse("24 Ge 12"), parse("17 Sc 46"), 19, "Krishna", "Chaturthi"),
        # Exercise 3: Moon 14d43' Le, Sun 28d13' Cp -> 17th, Krishna Dwitiya
        (parse("14 Le 43"), parse("28 Cp 13"), 17, "Krishna", "Dwitiya"),
    ],
)
def test_tithi_examples(moon, sun, number, paksha, name_):
    n = tithi_at(sun, moon)
    assert n == number
    assert name("tithi", n - 1) == name_
    assert name("paksha", paksha_at(sun, moon)) == paksha


@pytest.mark.parametrize(
    "number,lord",
    [(1, "Sun"), (2, "Moon"), (3, "Mars"), (4, "Mercury"), (5, "Jupiter"),
     (6, "Venus"), (7, "Saturn"), (8, "Rahu"), (9, "Sun"), (14, "Venus"),
     (15, "Saturn"), (16, "Sun"), (29, "Venus"), (30, "Rahu")],
)
def test_table_3_tithi_lords(number, lord):
    assert GRAHA_NAMES[TITHI_LORD[number - 1]] == lord


# --------------------------------------------------------------------------
# 1.3.8.2 Lunar months  (Table 4 and the 1999 adhika maasa)
# --------------------------------------------------------------------------

def test_table_4_month_name_from_conjunction_rasi():
    """Pisces conjunction starts Chaitra, Aries starts Vaisakha, and so on."""
    from hora.core.const import MASA_FROM_CONJUNCTION_RASI

    expected = {11: "Chaitra", 0: "Vaisaakha", 1: "Jyeshtha", 2: "Aashaadha",
                3: "Sraavana", 4: "Bhaadrapada", 5: "Aaswayuja", 6: "Kaarteeka",
                7: "Maargasira", 8: "Pushya", 9: "Maagha", 10: "Phaalguna"}
    for rasi, month in expected.items():
        assert name("masa", MASA_FROM_CONJUNCTION_RASI[rasi]) == month


@pytest.mark.parametrize(
    "when,expected_time,expected_position",
    [
        ((1999, 5, 13), "1999-05-15 17:35:32", (1, 0 + 23 / 60)),
        ((1999, 6, 12), "1999-06-14 00:33:27", (1, 28 + 29 / 60)),
    ],
)
def test_1999_conjunctions_match_the_authors_own_figures(when, expected_time, expected_position):
    """Book 1.3.8.2 prints both conjunctions to the second.

    These came out of the author's own software, so they are the closest thing
    to a JHora reading available without running JHora. Tolerance is 5 seconds
    of time and 1 arcminute of longitude, the precision the book prints.
    """
    from datetime import datetime

    from hora.core.const import Graha
    from hora.core.ephemeris import get_ephemeris
    from hora.panchanga.calendar import new_moon_after

    settings = Settings()
    eph = get_ephemeris(settings)
    jd = new_moon_after(from_local(*when, 0, 0, 0, tz_name=IST).jd_ut, settings)

    got = datetime.fromisoformat(jd_to_local_str(jd, 5.5))
    want = datetime.fromisoformat(expected_time)
    assert abs((got - want).total_seconds()) <= 5

    sun = eph.positions(jd, (Graha.SUN,))[Graha.SUN]
    want_rasi, want_deg = expected_position
    assert sun.rasi == want_rasi
    assert sun.degrees_in_rasi == pytest.approx(want_deg, abs=1 / 60)


def test_1999_had_two_jyeshtha_maasas_one_adhika():
    """Book 1.3.8.2: two Taurus conjunctions in 1999 gave nija and adhika Jyeshtha."""
    from hora.panchanga.calendar import lunar_months

    settings = Settings()
    first = lunar_months(from_local(1999, 5, 25, 12, 0, 0, tz_name=IST).jd_ut, settings)["amanta"]
    second = lunar_months(from_local(1999, 6, 25, 12, 0, 0, tz_name=IST).jd_ut, settings)["amanta"]

    assert first.name == second.name == "Jyeshtha"
    assert first.conjunction_rasi_name == second.conjunction_rasi_name == "Taurus"
    # Exactly one of the pair is the intercalary month.
    assert first.is_adhika != second.is_adhika


# --------------------------------------------------------------------------
# 1.3.9 Yogas  (Table 5, Example 3, Exercise 4)
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "sun,moon,number,name_",
    [
        (parse("23 Cp 50"), parse("17 Li 20"), 10, "Ganda"),      # Example 3
        (parse("28 Cp 13"), parse("14 Le 43"), 6, "Atiganda"),    # Exercise 4
    ],
)
def test_yoga_examples(sun, moon, number, name_):
    n = yoga_at(sun, moon)
    assert n == number
    assert name("yoga", n - 1) == name_


def test_table_5_all_27_yogas_in_order():
    assert len(YOGA_NAMES_BOOK) == 27
    assert YOGA_NAMES_BOOK[0] == "Vishkambha"
    assert YOGA_NAMES_BOOK[16] == "Vyatipaata"
    assert YOGA_NAMES_BOOK[26] == "Vaidhriti"


# --------------------------------------------------------------------------
# 1.3.11 Hora
# --------------------------------------------------------------------------

def test_hora_worked_example_wednesday_16th_hora_is_moon():
    """Book 1.3.11: Wednesday, sunrise 6:10, time 21:40 -> 16th hora -> Moon."""
    from hora.panchanga.hora import hora_lord

    assert GRAHA_NAMES[hora_lord(3, 16)] == "Moon"


@pytest.mark.parametrize(
    "vaara,lord",
    list(enumerate(["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"])),
)
def test_first_hora_of_a_day_belongs_to_the_weekday_lord(vaara, lord):
    from hora.panchanga.hora import hora_lord

    assert GRAHA_NAMES[hora_lord(vaara, 1)] == lord


def test_hora_lords_follow_decreasing_speed_order():
    """Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon, then repeat."""
    from hora.panchanga.hora import hora_lord

    order = [GRAHA_NAMES[hora_lord(6, i)] for i in range(1, 9)]   # Saturday
    assert order == ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon", "Saturn"]


def test_hora_index_is_bounded():
    from hora.panchanga.hora import hora_lord

    with pytest.raises(ValueError):
        hora_lord(0, 25)


# --------------------------------------------------------------------------
# 1.3.13 Ayanamsa
# --------------------------------------------------------------------------

def test_book_uses_lahiri_ayanamsa_and_so_do_we():
    """Book 1.3.13: 'We will use Chitrapaksha/Lahiri ayanamsa in this book.'"""
    assert Settings().ayanamsa.value == "lahiri"


# --------------------------------------------------------------------------
# Name schemes
# --------------------------------------------------------------------------

def test_book_spellings_are_the_default_and_standard_is_available():
    assert Settings().name_scheme is NameScheme.BOOK
    assert name("nakshatra", 7) == "Pushyami"
    assert name("nakshatra", 7, NameScheme.STANDARD) == "Pushya"
    assert name("tithi", 10) == "Ekadasi"
    assert name("tithi", 10, NameScheme.STANDARD) == "Ekadashi"
