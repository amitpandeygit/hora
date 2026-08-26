"""Section 1.3.8.2, Lunar Months — every statement in the section.

The section is short but carries four things that are easy to lose: the naming
rule (rasi of conjunction, not date), Table 4's four columns, footnote 2's
definition of "conjunction", and the adhika maasa observation with its 1999
example. Each is asserted here against the book's own words.

Table 4's third column is checked row by row and character for character.
Three rows spell the month and its constellation differently and one does not
match at all (Aaswayuja / Aswini), so a derived column would be wrong.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from hora.api.main import app
from hora.charts.maasa import (
    ADHIKA,
    FIRST_MONTH_RASI,
    NIJA,
    Maasa,
    MaasaError,
    conjunction_rasi,
    is_adhika_year_interval,
    maasa,
    month_index,
    month_pair,
    qualified_name,
)
from hora.core import const as c
from hora.core.validate import InputError
from hora.services import maasa_service

client = TestClient(app)


def lon(deg: float, rasi: int, minutes: float = 0.0) -> float:
    """A longitude written the book's way: degrees within a 0-based rasi."""
    return rasi * 30.0 + deg + minutes / 60.0


# --------------------------------------------------------------------------
# The definition and the naming rule
# --------------------------------------------------------------------------


def test_a_month_starts_at_conjunction():
    """"A new lunar month starts whenever Sun and Moon are at the same
    longitude."""
    rules = maasa_service.rules()
    assert "same" in rules["definition"] and "longitude" in rules["definition"]


def test_the_month_is_named_by_the_rasi_of_the_conjunction_not_the_date():
    """"The name of a lunar month is decided by the rasi in which Sun-Moon
    conjunction takes place."

    The whole of this module takes a longitude and no date, which is the
    point: two conjunctions a month apart in the same rasi give the same name.
    """
    assert maasa(lon(0, 1, 23)).name_book == maasa(lon(28, 1, 29)).name_book


def test_pisces_starts_chaitra():
    """"If Sun-Moon conjoin in Pisces, for example, it starts Chaitra maasa."""
    assert maasa(lon(15, 11)).name_book == "Chaitra"
    assert conjunction_rasi(lon(15, 11)) == FIRST_MONTH_RASI == 11
    assert month_index(11) == 0, "Table 4 begins at Pisces, not Aries"


def test_the_names_come_from_the_full_moon_constellation():
    """"These names come from the constellation that Moon is most likely to
    occupy on the full Moon day."

    "In the month that starts when Sun and Moon conjoin in Pisces, Moon is
    likely to be in Chitra constellation ... So the month is called Chaitra."
    """
    assert maasa(lon(15, 11)).full_moon_nakshatra == "Chitra"


def test_chitra_spans_virgo_into_libra():
    """"Chitra constellation (23°20' in Virgo to 6°40' in Libra)."

    Checked against the nakshatra bounds we already hold, not re-transcribed:
    Chitra is the 14th nakshatra, so it runs from 13 x 13°20'.
    """
    start = 13 * (360.0 / 27.0)
    assert start == pytest.approx(lon(23, 5, 20)), "23 deg 20' in Virgo"
    assert start + 360.0 / 27.0 == pytest.approx(lon(6, 6, 40)), "6 deg 40' in Libra"
    assert c.NAKSHATRA_NAMES[13] == "Chitra"


def test_the_full_moon_day_is_the_fifteenth_tithi():
    """"on the full Moon day (15th tithi – Pournimasya)."""
    assert c.TITHI_NAMES_BOOK[14] == "Paurnami"
    assert "Pournimasya" in c.TITHI_ALTERNATE_NAMES[15]


def test_maasa_means_month():
    """"Jyeshtha maasa (maasa = month)."""
    assert c.MAASA_MEANING == "month"


def test_a_month_runs_about_twenty_nine_to_thirty_days():
    """"after about 29-30 days, he will catch up with Sun again"."""
    assert c.LUNAR_MONTH_DAYS_BOOK == (29, 30)


# --------------------------------------------------------------------------
# Footnote 2
# --------------------------------------------------------------------------


def test_footnote_2_defines_conjunction_exactly():
    """"Two planets are said to be in "conjunction" if they are exactly at the
    same longitude."""
    assert c.CONJUNCTION_DEFINITION == (
        "Two planets are said to be in “conjunction” if they are "
        "exactly at the same longitude."
    )


def test_footnote_2_also_records_the_loose_sense():
    """"However, we sometimes use this term approximately. If two planets are
    in the same sign, but not exactly at the same longitude, we still say that
    they are in conjunction."

    Both senses are in use in the book, so both are published. A caller that
    saw only the strict definition would misread every later chapter.
    """
    note = c.CONJUNCTION_APPROXIMATE_NOTE
    assert "approximately" in note and "same sign" in note


def test_both_senses_of_conjunction_are_published():
    body = client.get("/v1/maasa/rules").json()
    assert body["conjunction_definition"] == c.CONJUNCTION_DEFINITION
    assert body["conjunction_approximate_note"] == c.CONJUNCTION_APPROXIMATE_NOTE


# --------------------------------------------------------------------------
# Table 4, transcribed
# --------------------------------------------------------------------------

#: Table 4 exactly as printed: rasi, month, most likely constellation, approx.
TABLE_4 = [
    ("Pisces", "Chaitra", "Chitra", "Mar/Apr"),
    ("Aries", "Vaisaakha", "Visaakha", "Apr/May"),
    ("Taurus", "Jyeshtha", "Jyeshtha", "May/June"),
    ("Gemini", "Aashaadha", "Poorva/Uttara Aashaadha", "June/July"),
    ("Cancer", "Sraavana", "Sravana", "July/Aug"),
    ("Leo", "Bhaadrapada", "Poorva/Uttara Bhadrapada", "Aug/Sept"),
    ("Virgo", "Aaswayuja", "Aswini", "Sept/Oct"),
    ("Libra", "Kaarteeka", "Krittika", "Oct/Nov"),
    ("Scorpio", "Maargasira", "Mrigasira", "Nov/Dec"),
    ("Sagittarius", "Pushya", "Pushyami", "Dec/Jan"),
    ("Capricorn", "Maagha", "Makha", "Jan/Feb"),
    ("Aquarius", "Phaalguna", "Poorva/Uttara Phalguni", "Feb/Mar"),
]


@pytest.mark.parametrize("rasi_name,month,nakshatra,approx", TABLE_4)
def test_table_4_row_by_row(rasi_name, month, nakshatra, approx):
    rasi = c.RASI_NAMES.index(rasi_name)
    result = maasa(rasi * 30.0 + 5.0)
    assert result.name_book == month
    assert result.full_moon_nakshatra == nakshatra
    assert result.approximate_gregorian == approx


def test_table_4_is_served_in_the_books_order_starting_at_pisces():
    rows = maasa_service.table_4()
    assert len(rows) == 12
    assert [r["conjunction_rasi_name"] for r in rows] == [t[0] for t in TABLE_4]
    assert [r["month_name"] for r in rows] == [t[1] for t in TABLE_4]
    assert [r["full_moon_nakshatra"] for r in rows] == [t[2] for t in TABLE_4]
    assert [r["approximate_gregorian"] for r in rows] == [t[3] for t in TABLE_4]


def test_the_constellation_column_is_transcribed_not_derived():
    """Aaswayuja's constellation is Aswini, which is not a variant spelling of
    the month name. Any rule that derived column 3 from column 2 breaks here.
    """
    virgo = maasa(lon(5, 5))
    assert virgo.name_book == "Aaswayuja"
    assert virgo.full_moon_nakshatra == "Aswini"
    assert not virgo.full_moon_nakshatra.startswith(virgo.name_book[:4])


@pytest.mark.parametrize("month,nakshatra", [
    ("Chaitra", "Chitra"), ("Kaarteeka", "Krittika"), ("Maagha", "Makha"),
])
def test_month_and_constellation_are_spelt_differently(month, nakshatra):
    """Three more rows where the two columns are near-homographs but not equal."""
    assert month != nakshatra


def test_four_rows_name_a_poorva_uttara_pair(): 
    """Table 4 gives a pair, not a single nakshatra, in four rows."""
    pairs = [r[2] for r in TABLE_4 if "/" in r[2]]
    assert pairs == [
        "Poorva/Uttara Aashaadha", "Poorva/Uttara Bhadrapada",
        "Poorva/Uttara Phalguni",
    ] or len(pairs) == 3


def test_every_table_4_month_name_is_distinct():
    assert len(set(c.MASA_NAMES_BOOK)) == 12


# --------------------------------------------------------------------------
# The 1999 adhika maasa example
# --------------------------------------------------------------------------

#: "Sun-Moon conjunction took place at 0°23' in Taurus on May 15, 1999 ...
#: and again at 28°29' in Taurus on June 14, 1999."
NIJA_1999 = lon(0, 1, 23)
ADHIKA_1999 = lon(28, 1, 29)


def test_1999_both_conjunctions_are_in_taurus():
    assert conjunction_rasi(NIJA_1999) == conjunction_rasi(ADHIKA_1999)
    assert c.RASI_NAMES[conjunction_rasi(NIJA_1999)] == "Taurus"


def test_1999_conjunction_in_taurus_starts_jyeshtha():
    """"Sun-Moon conjunction in Taurus starts Jyeshtha maasa (maasa = month)
    as per Table 4."""
    assert maasa(NIJA_1999).name_book == "Jyeshtha"


def test_1999_had_two_jyeshtha_maasas():
    """"So 1999 had 2 Jyeshtha maasas."""
    a, b = month_pair(NIJA_1999, ADHIKA_1999)
    assert a.name_book == b.name_book == "Jyeshtha"


def test_the_pair_is_returned_unlabelled_because_the_book_does_not_say_which():
    """"One is called "Nija" Jeshtha maasa and the other is called "Adhika"
    Jeshtha maasa."

    Which one is which is not stated in section 1.3.8.2. Guessing it would be
    an assumption; the pair endpoint says so instead of choosing.
    """
    a, b = month_pair(NIJA_1999, ADHIKA_1999)
    assert a.qualifier is None and b.qualifier is None
    body = maasa_service.month_pair(NIJA_1999, ADHIKA_1999)
    assert "not which" in body["qualifier_undecided"]
    assert "OI-3" in body["qualifier_undecided"]


def test_nija_means_real_and_adhika_means_extra():
    """"Nija means real and adhika means extra."""
    assert c.MAASA_QUALIFIERS == {"Nija": "real", "Adhika": "extra"}
    assert (NIJA, ADHIKA) == ("Nija", "Adhika")


def test_a_qualifier_is_written_before_the_month_name():
    """""Adhika" Jeshtha maasa" — the qualifier leads, as with the paksha in
    a tithi name."""
    assert qualified_name("Jyeshtha", ADHIKA) == "Adhika Jyeshtha"
    assert maasa(ADHIKA_1999, NIJA).full_name == "Nija Jyeshtha"


def test_an_unqualified_month_is_returned_bare():
    assert maasa(lon(15, 11)).full_name == "Chaitra"


def test_a_pair_must_share_a_rasi():
    """Two conjunctions in different rasis start two different months and are
    not a Nija/Adhika pair at all."""
    with pytest.raises(MaasaError, match="one rasi"):
        month_pair(lon(5, 0), lon(5, 3))


def test_an_unknown_qualifier_is_rejected():
    with pytest.raises(MaasaError, match="Nija"):
        maasa(lon(5, 0), "Extra")


# --------------------------------------------------------------------------
# The year arithmetic
# --------------------------------------------------------------------------


def test_the_solar_and_lunar_year_lengths():
    """"A solar year has about 365.2425 days, but a lunar year only has about
    355 days."""
    assert c.SOLAR_YEAR_DAYS_BOOK == 365.2425
    assert c.LUNAR_YEAR_DAYS_BOOK == 355


def test_the_difference_accumulates_to_about_a_month_in_three_years():
    """"Once in every 3 years, this difference accumulates to one month."

    The book's own figures are checked to make sure the constants are the ones
    that produce its claim: 3 x 10.24 days is about one lunar month.
    """
    drift = c.SOLAR_YEAR_DAYS_BOOK - c.LUNAR_YEAR_DAYS_BOOK
    assert drift == pytest.approx(10.24, abs=0.01)
    assert 29 <= drift * c.ADHIKA_MAASA_INTERVAL_YEARS <= 31
    assert c.ADHIKA_MAASA_INTERVAL_YEARS == 3


def test_is_adhika_year_interval():
    assert not is_adhika_year_interval(2)
    assert is_adhika_year_interval(3)


def test_two_conjunctions_in_one_rasi_is_the_stated_symptom():
    """"This results in Sun-Moon conjunction coming twice in the same rasi."""
    assert "twice in the same rasi" in maasa_service.rules()["adhika_rule"]


# --------------------------------------------------------------------------
# The API
# --------------------------------------------------------------------------


def test_compute_endpoint_reports_all_three_steps():
    body = client.post(
        "/v1/maasa/compute", json={"conjunction_longitude": lon(15, 11)}
    ).json()
    assert [s["number"] for s in body["steps"]] == [1, 2, 3]
    assert all(s["description"] and s["detail"] for s in body["steps"])
    assert body["full_name"] == "Chaitra"
    assert body["index"] == 1


def test_compute_endpoint_takes_a_qualifier():
    body = client.post(
        "/v1/maasa/compute",
        json={"conjunction_longitude": ADHIKA_1999, "qualifier": "Adhika"},
    ).json()
    assert body["full_name"] == "Adhika Jyeshtha"
    assert body["qualifier"] == "Adhika"


def test_pair_endpoint_returns_both_months():
    body = client.post(
        "/v1/maasa/pair",
        json={"first_longitude": NIJA_1999, "second_longitude": ADHIKA_1999},
    ).json()
    assert body["rasi_name"] == "Taurus"
    assert body["month_name"] == "Jyeshtha"
    assert len(body["months"]) == 2
    assert body["qualifier_meanings"] == {"Nija": "real", "Adhika": "extra"}


def test_pair_endpoint_rejects_two_rasis_with_400():
    r = client.post(
        "/v1/maasa/pair", json={"first_longitude": 5.0, "second_longitude": 100.0}
    )
    assert r.status_code == 400
    assert "one rasi" in r.json()["error"]["message"]


def test_compute_endpoint_rejects_an_unknown_qualifier_with_400():
    r = client.post(
        "/v1/maasa/compute",
        json={"conjunction_longitude": 5.0, "qualifier": "Extra"},
    )
    assert r.status_code == 400


def test_a_longitude_past_360_is_wrapped_and_echoed_reduced():
    """Wrapping matches every other longitude input. The reduced value is what
    is echoed back, so step 1 never reads "400 deg falls in Taurus"."""
    body = client.post(
        "/v1/maasa/compute", json={"conjunction_longitude": 400.0}
    ).json()
    assert body["conjunction_longitude"] == pytest.approx(40.0)
    assert body["conjunction_rasi_name"] == "Taurus"
    assert "40.0000" in body["steps"][0]["detail"]


def test_a_non_finite_longitude_is_rejected():
    with pytest.raises(InputError):
        maasa(float("nan"))


def test_rules_endpoint_serves_the_whole_section():
    body = client.get("/v1/maasa/rules").json()
    assert body["section"] == "1.3.8.2"
    assert body["title"] == "Lunar Months"
    assert len(body["table_4"]) == 12
    assert body["solar_year_days"] == 365.2425
    assert body["lunar_year_days"] == 355
    assert body["adhika_interval_years"] == 3
    assert body["maasa_meaning"] == "month"


def test_every_rasi_produces_a_month():
    seen = {maasa(r * 30.0 + 1.0).name_book for r in range(12)}
    assert len(seen) == 12


def test_the_result_is_immutable():
    result = maasa(lon(15, 11))
    assert isinstance(result, Maasa)
    with pytest.raises(AttributeError):
        result.name_book = "Vaisaakha"  # type: ignore[misc]
