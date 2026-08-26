"""Every claim in Chapter 5 of PVR Narasimha Rao's textbook.

Source: "Vedic Astrology: An Integrated Approach", Chapter 5 (Special Lagnas),
book pages 45-50.

Every worked example gives its own inputs — sunrise time, the Sun's longitude
at sunrise, the birth time — so each one can be run straight through the
production functions without an ephemeris in the way.

Deviation: PVR-6 in docs/precedence.md — §5.2's numbered method and Example 7
contradict the rate the same section states.
"""
import pytest
from fastapi.testclient import TestClient

from hora.api.main import app
from hora.charts.special_lagna import (
    ADVANCE_PER_MINUTE,
    BIRTHTIME_ERRORS_ARE_A_FACT_NOTE,
    BIRTHTIME_SENSITIVITY_NOTE,
    GHATIS_PER_DAY,
    ILLUSTRATION_NAMES_HORALAGNA,
    MINUTES_PER_DAY,
    MINUTES_PER_GHATI,
    MORE_PARASARA_LAGNAS_WARNING,
    NORMAL_LAGNA_SHOWS,
    SPECIAL_LAGNA_ABBR,
    SPECIAL_LAGNA_ALIASES,
    SPECIAL_LAGNA_NAMES,
    SPECIAL_LAGNA_SIGNIFIES,
    SPECIAL_LAGNA_USE_EXAMPLES,
    SPECIAL_LAGNA_VIEWPOINT,
    SREE_ALSO_MEANS,
    SREE_LAGNA_USED_IN,
    SREE_MEANING,
    SUNRISE_DEFINITIONS,
    SUNRISE_RECOMMENDED,
    SpecialLagna,
    advance_from_sunrise,
    birthtime_correction,
    ghati_lagna_birthtime_sensitivity,
    sree_lagna,
)
from hora.core.const import (
    NAKSHATRA_NAME_VARIANTS,
    NAKSHATRA_NAMES,
    NAKSHATRA_NAMES_BOOK,
    NAKSHATRA_SPAN,
)
from hora.core.notation import parse, to_rasi_dm

client = TestClient(app)

#: Examples 7, 8 and 9 share one native: born 19:23, sunrise 06:37, and the Sun
#: at 24d17' Capricorn at sunrise.
GENTLEMAN_SUN_AT_SUNRISE = parse("24 Cp 17")
GENTLEMAN_MINUTES = (19 * 60 + 23) - (6 * 60 + 37)          # 766


def readable(longitude: float) -> str:
    return to_rasi_dm(longitude)


# --------------------------------------------------------------------------
# Rates — the definitions in 5.2, 5.3 and 5.4
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "lagna,per_minute,rasi_per",
    [
        (SpecialLagna.BHAAVA, 0.25, 120.0),   # one rasi per 2 hours
        (SpecialLagna.HORA, 0.5, 60.0),       # one rasi per hour
        (SpecialLagna.GHATI, 1.25, 24.0),     # one rasi per ghati
    ],
)
def test_rates_match_their_stated_definitions(lagna, per_minute, rasi_per):
    """Each rate must equal 30 degrees over the stated period."""
    assert ADVANCE_PER_MINUTE[lagna] == pytest.approx(per_minute)
    assert ADVANCE_PER_MINUTE[lagna] * rasi_per == pytest.approx(30.0)


def test_the_three_rates_are_ordered_as_the_book_describes():
    """Bhaava is the slowest and Ghati the fastest; any other order is a bug."""
    assert (
        ADVANCE_PER_MINUTE[SpecialLagna.BHAAVA]
        < ADVANCE_PER_MINUTE[SpecialLagna.HORA]
        < ADVANCE_PER_MINUTE[SpecialLagna.GHATI]
    )


def test_bhaava_lagna_is_half_the_speed_of_hora_lagna():
    """One rasi per 2 hours against one rasi per hour."""
    assert ADVANCE_PER_MINUTE[SpecialLagna.BHAAVA] * 2 == pytest.approx(
        ADVANCE_PER_MINUTE[SpecialLagna.HORA]
    )


# --------------------------------------------------------------------------
# 5.2 Bhaava Lagna — PVR-6
# --------------------------------------------------------------------------

def test_bhaava_lagna_follows_the_stated_rate_not_the_printed_example():
    """PVR-6: §5.2 disagrees with itself three ways against two.

    Saying 0.25 deg/min: the rate ("one rasi per 2 hours"), the restatement
    ("1 degree per 4 minutes, i.e. 15 degrees per hour"), and the section's own
    illustration, where 06:00 to 07:00 advances 15 degrees.

    Saying 1 deg/min: the numbered method, which treats the elapsed minutes as
    degrees directly, and Example 7 which follows it.

    At 1 deg/min Bhaava Lagna would move 60 degrees an hour — twice Hora
    Lagna's speed — contradicting its own definition. The rate wins.
    """
    got = advance_from_sunrise(
        GENTLEMAN_SUN_AT_SUNRISE, GENTLEMAN_MINUTES,
        ADVANCE_PER_MINUTE[SpecialLagna.BHAAVA],
    )
    assert readable(got) == "5 Le 47"
    assert readable(got) != "10 Pi 17"          # what Example 7 prints


def test_the_illustration_in_5_2_confirms_the_rate():
    """"sunrise 06:00, Sun at 6s 4d47'; at 07:00 bhavalagna is at 6s 19d47'"."""
    sun = parse("6s 4 47")
    at_seven = advance_from_sunrise(sun, 60, ADVANCE_PER_MINUTE[SpecialLagna.BHAAVA])
    assert readable(at_seven) == readable(parse("6s 19 47"))
    at_eight = advance_from_sunrise(sun, 120, ADVANCE_PER_MINUTE[SpecialLagna.BHAAVA])
    assert readable(at_eight) == readable(parse("7s 4 47"))
    at_ten = advance_from_sunrise(sun, 240, ADVANCE_PER_MINUTE[SpecialLagna.BHAAVA])
    assert readable(at_ten) == readable(parse("8s 4 47"))


# --------------------------------------------------------------------------
# 5.3 Hora Lagna — Example 8
# --------------------------------------------------------------------------

def test_example_8_hora_lagna():
    """766 minutes / 2 = 383 degrees, added to 294d17' -> 17d17' Aquarius."""
    got = advance_from_sunrise(
        GENTLEMAN_SUN_AT_SUNRISE, GENTLEMAN_MINUTES,
        ADVANCE_PER_MINUTE[SpecialLagna.HORA],
    )
    assert readable(got) == "17 Aq 17"


def test_the_illustration_in_5_3_confirms_the_hora_rate():
    """"at 6s 19d47' at 6:30 am" — half a rasi in half an hour."""
    sun = parse("6s 4 47")
    assert readable(
        advance_from_sunrise(sun, 30, ADVANCE_PER_MINUTE[SpecialLagna.HORA])
    ) == readable(parse("6s 19 47"))


# --------------------------------------------------------------------------
# 5.4 Ghati Lagna — Example 9
# --------------------------------------------------------------------------

def test_example_9_ghati_lagna():
    """766 x 5/4 = 957.5 degrees, added to 294d17' -> 21d47' Virgo."""
    got = advance_from_sunrise(
        GENTLEMAN_SUN_AT_SUNRISE, GENTLEMAN_MINUTES,
        ADVANCE_PER_MINUTE[SpecialLagna.GHATI],
    )
    assert readable(got) == "21 Vi 47"


def test_the_illustration_in_5_4_confirms_the_ghati_rate():
    """"at 7s 4d47' at 6:24 am" — one rasi in one ghati."""
    sun = parse("6s 4 47")
    assert readable(
        advance_from_sunrise(sun, 24, ADVANCE_PER_MINUTE[SpecialLagna.GHATI])
    ) == readable(parse("7s 4 47"))


# --------------------------------------------------------------------------
# Exercise 8 — and the pre-dawn sunrise it implies
# --------------------------------------------------------------------------

#: Born 03:11:48 on 28 May 1961; sunrise was 06:19:18 on **27** May, with the
#: Sun at 12d11' Taurus. The exercise works from the previous day's sunrise,
#: which is what `birth_period` does for a pre-dawn birth.
LADY_SUN_AT_SUNRISE = parse("12 Ta 11")
LADY_MINUTES = ((24 - 6) * 60 - 19 - 18 / 60) + (3 * 60 + 11 + 48 / 60)


def test_exercise_8_elapsed_time_spans_the_previous_sunrise():
    assert LADY_MINUTES == pytest.approx(1252.5)
    assert LADY_MINUTES / 60 == pytest.approx(20.875)      # 20 hr 52.5 min


def test_exercise_8_hora_lagna():
    got = advance_from_sunrise(
        LADY_SUN_AT_SUNRISE, LADY_MINUTES, ADVANCE_PER_MINUTE[SpecialLagna.HORA]
    )
    assert readable(got) == "8 Aq 26"


def test_exercise_8_ghati_lagna():
    got = advance_from_sunrise(
        LADY_SUN_AT_SUNRISE, LADY_MINUTES, ADVANCE_PER_MINUTE[SpecialLagna.GHATI]
    )
    # The book prints 17d48.5' Virgo — half an arcminute, so check the value.
    assert got == pytest.approx(parse("17 Vi 48") + 0.5 / 60, abs=1e-6)


# --------------------------------------------------------------------------
# 5.5 Comments — birthtime sensitivity and Exercise 9
# --------------------------------------------------------------------------

def test_comment_1_ghati_lagna_moves_1_25_degrees_per_minute():
    """"If the birthtime changes by one minute, GL will change by 1.25 deg"."""
    assert ghati_lagna_birthtime_sensitivity(1.0) == pytest.approx(1.25)
    assert ghati_lagna_birthtime_sensitivity(1.0) == pytest.approx(1 + 15 / 60)


def test_exercise_9_birthtime_correction():
    """Inverting the sensitivity to correct a birthtime from a known GL range.

    GL at the given 03:11:48 is 17d48.5' Virgo. If it must lie between 16d15'
    and 17d30', the error is between 18.5' and 1d33.5'. The book answers
    03:10:33 to 03:11:33.
    """
    given = parse("17 Vi 48") + 0.5 / 60
    low, high = parse("16 Vi 15"), parse("17 Vi 30")
    rate = ADVANCE_PER_MINUTE[SpecialLagna.GHATI]

    smallest_error_deg = given - high        # 18.5 arcmin
    largest_error_deg = given - low          # 1 deg 33.5 arcmin
    assert smallest_error_deg == pytest.approx(18.5 / 60, abs=1e-9)
    assert largest_error_deg == pytest.approx(1 + 33.5 / 60, abs=1e-9)

    # The hint also prints both errors in decimal degrees.
    assert smallest_error_deg == pytest.approx(0.3083, abs=5e-5)
    assert largest_error_deg == pytest.approx(1.5583, abs=5e-5)

    # Convert each to seconds of birthtime and subtract from 03:11:48.
    earliest = 48 - largest_error_deg / rate * 60
    latest = 48 - smallest_error_deg / rate * 60
    assert round(latest) == 33          # 03:11:33
    assert round(earliest + 60) == 33   # 03:10:33, a minute earlier


# --------------------------------------------------------------------------
# 5.7 Sree Lagna
# --------------------------------------------------------------------------

def test_example_10_sree_lagna():
    """Moon 13 Li 06, lagna 25 Vi 05 -> 18d47' Pisces."""
    got = sree_lagna(parse("13 Li 06"), parse("25 Vi 05"))
    assert readable(got) == "18 Pi 47"


def test_example_10_intermediate_steps():
    """The book shows its working; each step is checkable."""
    from hora.core.const import NAKSHATRA_SPAN

    moon = parse("13 Li 06")
    # Swati runs 6d40' to 20d00' in Libra.
    assert int(moon // NAKSHATRA_SPAN) == 14
    advancement = moon - 14 * NAKSHATRA_SPAN
    assert advancement == pytest.approx(6 + 26 / 60, abs=1e-9)
    fraction = advancement / NAKSHATRA_SPAN
    assert fraction == pytest.approx(0.4825, abs=1e-4)
    assert fraction * 360 == pytest.approx(173.7, abs=1e-2)


def test_exercise_10_sree_lagna():
    """Moon 15 Le 29, lagna 14 Sc 19 -> 12d22' Capricorn."""
    got = sree_lagna(parse("15 Le 29"), parse("14 Sc 19"))
    assert readable(got) == "12 Cp 22"


@pytest.mark.parametrize("lagna_deg", [0.0, 45.0, 200.0, 359.9])
def test_sree_lagna_equals_the_lagna_at_a_nakshatra_boundary(lagna_deg):
    """Zero progress through the nakshatra means zero advancement."""
    from hora.core.const import NAKSHATRA_SPAN

    assert sree_lagna(5 * NAKSHATRA_SPAN, lagna_deg) == pytest.approx(lagna_deg)


def test_sree_lagna_wraps_past_360():
    """Step (4): "Subtract multiples of 360 if necessary"."""
    from hora.core.const import NAKSHATRA_SPAN

    almost_whole = 6 * NAKSHATRA_SPAN - 1e-9
    got = sree_lagna(almost_whole, 350.0)
    assert 0.0 <= got < 360.0


# --------------------------------------------------------------------------
# 5.6 What each one shows
# --------------------------------------------------------------------------

def test_significations():
    """"hora lagna shows money and ghati lagna shows power"."""
    assert "money" in SPECIAL_LAGNA_SIGNIFIES[SpecialLagna.HORA]
    assert "power" in SPECIAL_LAGNA_SIGNIFIES[SpecialLagna.GHATI]
    assert SPECIAL_LAGNA_SIGNIFIES[SpecialLagna.SREE] == "prosperity"


def test_bhaava_lagna_carries_no_signification():
    """5.2 footnote: "defined only for the sake of completeness"."""
    assert SPECIAL_LAGNA_SIGNIFIES[SpecialLagna.BHAAVA] is None


def test_names_and_abbreviations():
    assert SPECIAL_LAGNA_ABBR == ["BL", "HL", "GL", "SL"]
    assert SPECIAL_LAGNA_NAMES[SpecialLagna.GHATI] == "Ghati Lagna"


# --------------------------------------------------------------------------
# The endpoint
# --------------------------------------------------------------------------

BODY = {
    "year": 1972, "month": 10, "day": 1, "hour": 13, "minute": 30,
    "tz_name": "Asia/Kolkata",
    "place": {"latitude": 16.2, "longitude": 81.13},
}


def test_endpoint_returns_all_four(client):
    body = client.post("/v1/chart/special-lagnas", json=BODY).json()
    assert [x["abbreviation"] for x in body["special_lagnas"]] == ["BL", "HL", "GL", "SL"]


def test_endpoint_reports_the_sunrise_it_worked_from(client):
    body = client.post("/v1/chart/special-lagnas", json=BODY).json()
    assert body["sunrise"].startswith("1972-10-01")
    assert body["minutes_since_sunrise"] > 0


def test_endpoint_uses_the_previous_sunrise_for_a_pre_dawn_birth(client):
    """Exercise 8 works a 03:11 birth from the previous day's sunrise."""
    pre_dawn = {**BODY, "hour": 3, "minute": 11}
    body = client.post("/v1/chart/special-lagnas", json=pre_dawn).json()
    assert body["sunrise"].startswith("1972-09-30")
    assert body["minutes_since_sunrise"] > 1000


def test_endpoint_marks_sree_lagna_as_having_no_rate(client):
    body = client.post("/v1/chart/special-lagnas", json=BODY).json()
    by_abbr = {x["abbreviation"]: x for x in body["special_lagnas"]}
    assert by_abbr["SL"]["degrees_per_minute"] is None
    assert by_abbr["GL"]["degrees_per_minute"] == 1.25


# --------------------------------------------------------------------------
# The longitude-level endpoint — the book's own inputs, no ephemeris
# --------------------------------------------------------------------------

GENTLEMAN = {"sun_at_sunrise": "24 Cp 17", "minutes_since_sunrise": 766}


@pytest.mark.parametrize(
    "abbr,expected",
    [("BL", "5 Le 47"), ("HL", "17 Aq 17"), ("GL", "21 Vi 47")],
)
def test_pure_endpoint_reproduces_examples_7_to_9(abbr, expected, client):
    body = client.post(
        "/v1/lagna/special", json={**GENTLEMAN, "lagnas": [abbr]}
    ).json()
    assert body["special_lagnas"][0]["rasi_dm"] == expected


def test_pure_endpoint_reproduces_example_10(client):
    body = client.post(
        "/v1/lagna/special",
        json={"lagnas": ["SL"], "moon": "13 Li 06", "lagna": "25 Vi 05"},
    ).json()
    assert body["special_lagnas"][0]["rasi_dm"] == "18 Pi 47"


def test_pure_endpoint_reproduces_exercise_8(client):
    """Sun 12d11' Ta at sunrise, 1252.5 minutes later."""
    body = client.post(
        "/v1/lagna/special",
        json={"sun_at_sunrise": "12 Ta 11", "minutes_since_sunrise": 1252.5,
              "lagnas": ["HL", "GL"]},
    ).json()
    by_abbr = {x["abbreviation"]: x for x in body["special_lagnas"]}
    assert by_abbr["HL"]["rasi_dm"] == "8 Aq 26"
    assert by_abbr["GL"]["longitude"] == pytest.approx(parse("17 Vi 48") + 0.5 / 60, abs=1e-6)


def test_pure_endpoint_accepts_every_notation(client):
    for value in ["24 Cp 17", "9s 24 17", 294 + 17 / 60]:
        body = client.post(
            "/v1/lagna/special",
            json={"sun_at_sunrise": value, "minutes_since_sunrise": 766, "lagnas": ["HL"]},
        ).json()
        assert body["special_lagnas"][0]["rasi_dm"] == "17 Aq 17", value


def test_pure_endpoint_echoes_only_the_inputs_it_used(client):
    """Asking for HL alone must not echo a Moon that was never supplied."""
    body = client.post("/v1/lagna/special", json={**GENTLEMAN, "lagnas": ["HL"]}).json()
    assert body["input"]["sun_at_sunrise"] is not None
    assert body["input"]["moon"] is None


@pytest.mark.parametrize(
    "payload,fragment",
    [
        ({"lagnas": ["SL"]}, "moon and lagna"),
        ({"lagnas": ["GL"]}, "sun_at_sunrise and minutes_since_sunrise"),
    ],
)
def test_pure_endpoint_rejects_a_request_its_inputs_cannot_answer(
    payload, fragment, client
):
    """Asking for a lagna without its inputs is a 422 with a field location.

    Caught at the schema rather than deep in the service, so the error names
    where the request is wrong.
    """
    response = client.post("/v1/lagna/special", json=payload)
    assert response.status_code == 422
    details = response.json()["error"]["details"]
    assert any(fragment in d["message"] for d in details)


def test_pure_endpoint_rejects_an_unknown_lagna(client):
    response = client.post("/v1/lagna/special", json={**GENTLEMAN, "lagnas": ["XX"]})
    assert response.status_code == 400
    assert "unknown special lagna" in response.json()["error"]["message"]


def test_the_service_guards_the_same_thing_without_http():
    """Defence in depth: the service is callable directly, so it checks too."""
    from hora.services import lagna_service

    with pytest.raises(lagna_service.SpecialLagnaError, match="moon and lagna"):
        lagna_service.compute(
            sun_at_sunrise=None, minutes_since_sunrise=None,
            moon=None, lagna=None, lagnas=["SL"],
        )


@pytest.mark.parametrize("minutes", [-1, -5000, 99999])
def test_pure_endpoint_rejects_impossible_elapsed_time(minutes, client):
    """A special lagna is measured forward from sunrise.

    A negative elapsed time used to produce a plausible-looking answer.
    """
    response = client.post(
        "/v1/lagna/special",
        json={"sun_at_sunrise": 0, "minutes_since_sunrise": minutes, "lagnas": ["GL"]},
    )
    assert response.status_code == 422


def test_pure_functions_reject_nonsense():
    from hora.charts.special_lagna import (
        SpecialLagnaError,
        advance_from_sunrise,
        sree_lagna,
    )

    with pytest.raises(SpecialLagnaError):
        advance_from_sunrise(0.0, -1.0, 1.25)
    with pytest.raises(SpecialLagnaError):
        advance_from_sunrise(0.0, 10.0, 0.0)
    with pytest.raises(SpecialLagnaError):
        sree_lagna(float("nan"), 0.0)
    with pytest.raises(SpecialLagnaError):
        sree_lagna(0.0, float("inf"))


def test_rules_endpoint_publishes_rates_and_sensitivity(client):
    body = client.get("/v1/lagna/rules").json()
    by_abbr = {x["abbreviation"]: x for x in body["lagnas"]}
    assert by_abbr["GL"]["degrees_per_minute"] == 1.25
    assert by_abbr["GL"]["one_rasi_per_minutes"] == pytest.approx(24.0)
    assert by_abbr["HL"]["one_rasi_per_minutes"] == pytest.approx(60.0)
    assert by_abbr["BL"]["one_rasi_per_minutes"] == pytest.approx(120.0)
    assert by_abbr["SL"]["degrees_per_minute"] is None
    assert body["birthtime_sensitivity_per_minute"]["GL"] == 1.25


def test_the_5_2_illustration_says_horalagna_but_means_bhavalagna():
    """§5.2's illustration paragraph opens "then, **horalagna** is at 6s 4d47'
    at 6:00 am" and closes "**Bhavalagna** moves at the rate of 1d per 4
    minutes".

    The numbers decide it. 6s 4d47' at 06:00 to 6s 19d47' at 07:00 is 15
    degrees an hour — Bhaava Lagna's rate. Hora Lagna moves 30 degrees an
    hour, so the illustration cannot be its.

    That makes the paragraph a **fourth** statement of the 0.25 deg/min rate,
    not a statement about a different lagna, and strengthens PVR-6. See D-11.
    """
    illustrated = (parse("6s 19 47") - parse("6s 4 47")) * 60.0 / 60.0
    assert illustrated == pytest.approx(15.0), "15 degrees in the hour 06:00-07:00"

    assert ADVANCE_PER_MINUTE[SpecialLagna.BHAAVA] * 60 == pytest.approx(15.0)
    assert ADVANCE_PER_MINUTE[SpecialLagna.HORA] * 60 == pytest.approx(30.0)
    assert illustrated != ADVANCE_PER_MINUTE[SpecialLagna.HORA] * 60

    assert "horalagna" in ILLUSTRATION_NAMES_HORALAGNA
    assert "bhavalagna" in ILLUSTRATION_NAMES_HORALAGNA


def test_the_illustration_read_as_hora_lagna_would_be_wrong():
    """Taken at its word, the paragraph would put Hora Lagna at 6s 19d47' an
    hour after sunrise. At Hora Lagna's own stated rate it is at 7s 4d47'.
    Asserting the mismatch is what makes "slip" a finding rather than a guess.
    """
    sun = parse("6s 4 47")
    as_hora = advance_from_sunrise(sun, 60.0, ADVANCE_PER_MINUTE[SpecialLagna.HORA])
    assert readable(as_hora) == readable(parse("7s 4 47"))
    assert readable(as_hora) != readable(parse("6s 19 47"))


def test_example_7_step_1_the_elapsed_minutes():
    """"19:23-6:37=12 hr 46 min=12x60 + 46 min = 766 min"."""
    assert GENTLEMAN_MINUTES == 766
    assert GENTLEMAN_MINUTES == 12 * 60 + 46


def test_example_7_step_2_the_sun_longitude_at_sunrise():
    """"Sun's longitude at sunrise is 270d+24d17'=294d17'." Capricorn is the
    10th rasi, so nine whole rasis precede it."""
    assert parse("24 Cp 17") == pytest.approx(270 + 24 + 17 / 60)
    assert 9 * 30 == 270


def test_example_7_step_2_the_printed_sum_needs_360_twice():
    """"Add 766d to it. The result is 1060d17'. Subtracting 360d twice, we get
    340d17'. So BL is at 10d17' in Pisces."

    That is the 1 deg/min reading. Reproduced here **only** to show the
    printed answer is arithmetically consistent with the numbered method — the
    method is what PVR-6 rejects, not the arithmetic.
    """
    sun = parse("24 Cp 17")
    printed = sun + 766.0
    assert printed == pytest.approx(1060 + 17 / 60)
    assert printed - 720.0 == pytest.approx(340 + 17 / 60)
    assert readable((printed) % 360.0) == "10 Pi 17"


def test_example_7_at_the_stated_rate_gives_leo():
    """At 0.25 deg/min the advancement is 766/4 = 191d30', and
    294d17' + 191d30' = 485d47' - 360d = 125d47' = 5d47' Leo. PVR-6."""
    sun = parse("24 Cp 17")
    advancement = GENTLEMAN_MINUTES * ADVANCE_PER_MINUTE[SpecialLagna.BHAAVA]
    assert advancement == pytest.approx(191.5)
    assert sun + advancement == pytest.approx(485 + 47 / 60, abs=0.01)
    assert readable(
        advance_from_sunrise(sun, GENTLEMAN_MINUTES,
                             ADVANCE_PER_MINUTE[SpecialLagna.BHAAVA])
    ) == "5 Le 47"


def test_5_2_step_3_expunges_multiples_of_360():
    """"Expunge multiples of 360d and reduce the number to the range
    0d-360d." Example 7 needs it twice; a single subtraction would leave
    700d17'."""
    sun = parse("24 Cp 17")
    for minutes in (766.0, 5000.0, 100000.0):
        got = advance_from_sunrise(sun, minutes,
                                   ADVANCE_PER_MINUTE[SpecialLagna.BHAAVA])
        assert 0.0 <= got < 360.0


def test_5_1_the_special_lagnas_are_parasaras():
    """"There are some special lagnas defined by Parasara. In this book, we
    will widely use Hora lagna and Ghati lagna."

    Bhaava Lagna is named in the same breath but footnote 10 says it is
    "defined only for the sake of completeness. We will not use it in this
    book." — which is why SPECIAL_LAGNA_SIGNIFIES has None for it alone.
    """
    assert SPECIAL_LAGNA_SIGNIFIES[SpecialLagna.BHAAVA] is None
    assert SPECIAL_LAGNA_SIGNIFIES[SpecialLagna.HORA] is not None
    assert SPECIAL_LAGNA_SIGNIFIES[SpecialLagna.GHATI] is not None


def test_5_2_bhaava_lagna_starts_at_the_sun():
    """"Bhaava lagna is at the position of Sun at the time of sunrise." So at
    zero elapsed minutes it *is* the Sun's longitude, for any rate."""
    sun = parse("24 Cp 17")
    for lagna in (SpecialLagna.BHAAVA, SpecialLagna.HORA, SpecialLagna.GHATI):
        assert advance_from_sunrise(sun, 0.0, ADVANCE_PER_MINUTE[lagna]) == (
            pytest.approx(sun)
        )


def test_5_2_bl_is_the_abbreviation():
    """"In the rest of this book, bhava lagna will be denoted by BL."""
    assert SPECIAL_LAGNA_ABBR[int(SpecialLagna.BHAAVA)] == "BL"


# --------------------------------------------------------------------------
# 5.3 Hora Lagna — the section, and where §5.2's "horalagna" slip came from
# --------------------------------------------------------------------------

#: §5.3's illustration: sunrise 06:00 with the Sun at 6s 4d47'.
HORA_ILLUSTRATION = [
    (0, "6s 4 47"),      # 6:00 am
    (30, "6s 19 47"),    # 6:30 am
    (60, "7s 4 47"),     # 7:00 am
    (120, "8s 4 47"),    # 8:00 am
]

#: §5.2's illustration — the same longitudes at double the elapsed time.
BHAAVA_ILLUSTRATION = [
    (0, "6s 4 47"),      # 6:00 am
    (60, "6s 19 47"),    # 7:00 am
    (120, "7s 4 47"),    # 8:00 am
    (240, "8s 4 47"),    # 10:00 am
]


@pytest.mark.parametrize("minutes,expected", HORA_ILLUSTRATION)
def test_5_3_illustration_point_by_point(minutes, expected):
    """"horalagna is at 6s 4d47' at 6:00 am, at 6s 19d47' at 6:30 am, at
    7s 4d47' at 7:00 am, 8s 4d47' at 8:00 am"."""
    sun = parse("6s 4 47")
    got = advance_from_sunrise(sun, minutes, ADVANCE_PER_MINUTE[SpecialLagna.HORA])
    assert readable(got) == readable(parse(expected))


def test_5_2_and_5_3_illustrations_are_the_same_one_retimed():
    """This is where §5.2's "horalagna" slip came from.

    The two illustrations list **identical longitudes**; §5.2's elapsed times
    are exactly **double** §5.3's at every point — which is the 15 deg/h
    versus 30 deg/h difference. §5.2's paragraph is §5.3's re-timed for the
    slower lagna, and "horalagna" was left behind in its first sentence.

    Not an inference about intent: the two paragraphs are the same
    illustration. See D-11.
    """
    assert [p for _, p in BHAAVA_ILLUSTRATION] == [p for _, p in HORA_ILLUSTRATION]
    for (slow, _), (fast, _) in zip(BHAAVA_ILLUSTRATION, HORA_ILLUSTRATION):
        assert slow == fast * 2

    sun = parse("6s 4 47")
    for (slow, point), (fast, _) in zip(BHAAVA_ILLUSTRATION, HORA_ILLUSTRATION):
        bl = advance_from_sunrise(sun, slow, ADVANCE_PER_MINUTE[SpecialLagna.BHAAVA])
        hl = advance_from_sunrise(sun, fast, ADVANCE_PER_MINUTE[SpecialLagna.HORA])
        assert readable(bl) == readable(hl) == readable(parse(point))


def test_5_3_the_rate_is_stated_three_ways():
    """"one rasi per hora (hour)" ... "1/2 deg per minute (i.e., 30 deg per
    hour)". Three forms of one number, and unlike §5.2 the method agrees:
    step (3) says "Divide the number by 2", which is also 0.5 deg/min."""
    rate = ADVANCE_PER_MINUTE[SpecialLagna.HORA]
    assert rate == 0.5, "1/2 degree per minute"
    assert rate * 60 == 30.0, "30 degrees per hour"
    assert 30.0 / rate / 60 == 1.0, "one rasi per hour"
    assert 766 / 2 == 766 * rate, "step (3): divide by 2"


def test_5_3_has_no_internal_contradiction_unlike_5_2():
    """The reason §5.3 needs no PVR entry and §5.2 does. Hora Lagna's method
    step ("divide by 2") and its stated rate give the same number; Bhaava
    Lagna's method ("convert to minutes, that is the advancement in degrees")
    gives four times its stated rate."""
    minutes = 766.0
    assert minutes / 2 == minutes * ADVANCE_PER_MINUTE[SpecialLagna.HORA]
    assert minutes != minutes * ADVANCE_PER_MINUTE[SpecialLagna.BHAAVA]
    assert minutes / (minutes * ADVANCE_PER_MINUTE[SpecialLagna.BHAAVA]) == 4.0


def test_5_3_hl_is_the_abbreviation():
    """"In the rest of this book, horalagna will be denoted by HL."""
    assert SPECIAL_LAGNA_ABBR[int(SpecialLagna.HORA)] == "HL"


def test_5_3_hora_lagna_starts_at_the_sun():
    """"Hora lagna is at the position of Sun at the time of sunrise."""
    sun = parse("24 Cp 17")
    assert advance_from_sunrise(
        sun, 0.0, ADVANCE_PER_MINUTE[SpecialLagna.HORA]
    ) == pytest.approx(sun)


# --------------------------------------------------------------------------
# Example 8, step by step
# --------------------------------------------------------------------------


def test_example_8_step_1_elapsed_minutes():
    """"19:23-6:37=12 hr 46 min=12x60 + 46 min = 766 min" — the same
    gentleman as Example 7, so the three lagnas are read off one birth."""
    assert GENTLEMAN_MINUTES == 766


def test_example_8_step_2_divide_by_two():
    """"766/2=383"."""
    assert GENTLEMAN_MINUTES / 2 == 383.0
    assert GENTLEMAN_MINUTES * ADVANCE_PER_MINUTE[SpecialLagna.HORA] == 383.0


def test_example_8_step_3_the_sum_and_its_reduction():
    """"Sun's longitude at sunrise is 270d+24d17'=294d17'. Add 383d to it. The
    result is 677d17'. Subtracting 360d, we get 317d17'. So HL is at 17d17' in
    Aquarius."

    One subtraction here, where Example 7 needed two — worth asserting so the
    reduction is not assumed to be a single wrap.
    """
    sun = parse("24 Cp 17")
    assert sun == pytest.approx(294 + 17 / 60)
    raw = sun + 383.0
    assert raw == pytest.approx(677 + 17 / 60)
    assert raw - 360.0 == pytest.approx(317 + 17 / 60)
    assert raw < 720.0, "one subtraction suffices, unlike Example 7"
    assert readable(raw % 360.0) == "17 Aq 17"


def test_example_8_through_the_endpoint():
    """POST /v1/lagna/special is the endpoint. Asking for HL alone needs only
    the Sun at sunrise and the elapsed minutes."""
    body = client.post(
        "/v1/lagna/special",
        json={
            "lagnas": ["HL"],
            "sun_at_sunrise": "24 Cp 17",
            "minutes_since_sunrise": 766,
        },
    ).json()
    assert body["input"]["sun_at_sunrise"]["rasi_dm"] == "24 Cp 17"
    hl = body["special_lagnas"][0]
    assert hl["abbreviation"] == "HL"
    assert hl["rasi_dm"] == "17 Aq 17"
    assert hl["longitude"] == pytest.approx(317 + 17 / 60)
    assert hl["degrees_per_minute"] == 0.5
    assert hl["signifies"] == "money, wealth and prosperity"


def test_asking_for_sree_lagna_without_its_inputs_is_rejected():
    """SL needs the Moon and the lagna, which Example 8 does not give. The
    request is refused rather than quietly answered short."""
    r = client.post(
        "/v1/lagna/special",
        json={"sun_at_sunrise": "24 Cp 17", "minutes_since_sunrise": 766},
    )
    assert r.status_code == 422
    assert "SL needs both" in str(r.json()["error"]["details"])


# --------------------------------------------------------------------------
# 5.4 Ghati Lagna — the section and Example 9
# --------------------------------------------------------------------------

#: §5.4's illustration: sunrise 06:00 with the Sun at 6s 4d47'.
GHATI_ILLUSTRATION = [
    (0, "6s 4 47"),      # 6:00 am
    (12, "6s 19 47"),    # 6:12 am
    (24, "7s 4 47"),     # 6:24 am
    (48, "8s 4 47"),     # 6:48 am
]


@pytest.mark.parametrize("minutes,expected", GHATI_ILLUSTRATION)
def test_5_4_illustration_point_by_point(minutes, expected):
    """"ghatilagna is at 6s 4d47' at 6:00 am, at 6s 19d47' at 6:12 am, at
    7s 4d47' at 6:24 am, 8s 4d47' at 6:48 am"."""
    sun = parse("6s 4 47")
    got = advance_from_sunrise(sun, minutes, ADVANCE_PER_MINUTE[SpecialLagna.GHATI])
    assert readable(got) == readable(parse(expected))


def test_all_three_illustrations_are_the_same_one_retimed():
    """§5.2, §5.3 and §5.4 print the *same four longitudes*, each at its own
    lagna's pace: 0 / 60 / 120 / 240 minutes for BL, half that for HL, and a
    fifth of HL's for GL.

    Which is the whole story behind §5.2's "horalagna" slip — see D-11. It
    also means the three illustrations are one test, not three.
    """
    assert [p for _, p in GHATI_ILLUSTRATION] == [p for _, p in HORA_ILLUSTRATION]
    assert [p for _, p in GHATI_ILLUSTRATION] == [p for _, p in BHAAVA_ILLUSTRATION]
    for (bl, _), (hl, _), (gl, _) in zip(
        BHAAVA_ILLUSTRATION, HORA_ILLUSTRATION, GHATI_ILLUSTRATION
    ):
        assert bl == hl * 2
        assert hl * 2 == gl * 5, "GL covers in 12 minutes what BL takes 60 for"


def test_5_4_the_ghati_is_defined_and_the_rate_follows_from_it():
    """"one rasi per ghati (ghati=1/60th of a day, i.e., 24 minutes)" and
    "1d15' per minute (i.e., 30d per 24 minutes)".

    The rate is not an independent number — it is 30 degrees over one ghati.
    Asserted that way so a wrong ghati length cannot coexist with a right rate.
    """
    assert GHATIS_PER_DAY == 60
    assert MINUTES_PER_GHATI == 24.0
    assert MINUTES_PER_DAY / GHATIS_PER_DAY == MINUTES_PER_GHATI
    assert ADVANCE_PER_MINUTE[SpecialLagna.GHATI] == 30.0 / MINUTES_PER_GHATI
    assert ADVANCE_PER_MINUTE[SpecialLagna.GHATI] == pytest.approx(1 + 15 / 60)


def test_5_4_step_3_multiply_by_five_divide_by_four():
    """"Multiply the number by 5. Divide the result by 4." Which is 1.25, the
    stated rate — §5.4's method agrees with itself, as §5.3's does and §5.2's
    does not."""
    for minutes in (766.0, 1252.5, 1.0):
        assert minutes * 5 / 4 == minutes * ADVANCE_PER_MINUTE[SpecialLagna.GHATI]


def test_5_4_ghatika_lagna_is_the_alias():
    """"Ghati lagna is also called "ghatika lagna"." and "ghatilagna will be
    denoted by GL"."""
    assert SPECIAL_LAGNA_ALIASES[int(SpecialLagna.GHATI)] == ["Ghatika Lagna"]
    assert SPECIAL_LAGNA_ABBR[int(SpecialLagna.GHATI)] == "GL"


def test_example_9_step_2_the_advancement():
    """"766x5/4=957.5"."""
    assert GENTLEMAN_MINUTES * 5 / 4 == 957.5


def test_example_9_step_3_the_sum_needs_360_three_times():
    """"Sun's longitude at sunrise is 294d17'. Add 957d30' to it. The result
    is 1251d47'. Subtracting 360d three times, we get 171d47'. So GL is at
    21d47' in Virgo."

    Three subtractions, where Example 8 needed one and Example 7 two — the
    same native, so the count is a property of the rate.
    """
    sun = parse("24 Cp 17")
    raw = sun + 957.5
    assert 957.5 == pytest.approx(957 + 30 / 60), "957d30'"
    assert raw == pytest.approx(1251 + 47 / 60)
    assert raw - 3 * 360.0 == pytest.approx(171 + 47 / 60)
    assert readable(raw % 360.0) == "21 Vi 47"


def test_example_9_through_the_endpoint():
    body = client.post(
        "/v1/lagna/special",
        json={
            "lagnas": ["GL"],
            "sun_at_sunrise": "24 Cp 17",
            "minutes_since_sunrise": 766,
        },
    ).json()
    gl = body["special_lagnas"][0]
    assert gl["abbreviation"] == "GL"
    assert gl["rasi_dm"] == "21 Vi 47"
    assert gl["degrees_per_minute"] == 1.25
    assert gl["signifies"] == "fame, power and authority"


def test_examples_7_8_9_are_one_native_read_three_ways():
    """One birth, one sunrise, three rates. Asserting them together means a
    change to the shared inputs cannot pass by fixing only one example."""
    body = client.post(
        "/v1/lagna/special",
        json={
            "lagnas": ["BL", "HL", "GL"],
            "sun_at_sunrise": "24 Cp 17",
            "minutes_since_sunrise": 766,
        },
    ).json()
    got = {x["abbreviation"]: x["rasi_dm"] for x in body["special_lagnas"]}
    assert got == {"BL": "5 Le 47", "HL": "17 Aq 17", "GL": "21 Vi 47"}
    # BL is ours, not the book's — PVR-6. The other two are the book's own.
    assert got["BL"] != "10 Pi 17"


# --------------------------------------------------------------------------
# Exercise 8 — a pre-dawn birth, so sunrise is the previous day's
# --------------------------------------------------------------------------

_LADY_SUNRISE_SECONDS = 6 * 3600 + 19 * 60 + 18
_LADY_BIRTH_SECONDS = 24 * 3600 + 3 * 3600 + 11 * 60 + 48      # the next day


def test_exercise_8_the_elapsed_time_crosses_midnight():
    """Sunrise is on **May 27** and the birth on **May 28** — a pre-dawn birth
    is measured from the *previous* day's sunrise, not the same morning's.

    Taking the same day's sunrise would give a negative elapsed time; taking
    the following morning's would give about 3 hours instead of nearly 21.
    """
    assert LADY_MINUTES == 1252.5, "20 hours 52 minutes 30 seconds"
    hours, rest = divmod(_LADY_BIRTH_SECONDS - _LADY_SUNRISE_SECONDS, 3600)
    minutes, seconds = divmod(rest, 60)
    assert (hours, minutes, seconds) == (20, 52, 30)
    assert LADY_MINUTES > MINUTES_PER_DAY / 2, "most of a day, not a few hours"


def test_exercise_8_uses_the_sun_at_sunrise_not_at_birth():
    """The exercise gives two Sun positions: 13d1' Taurus **at birth** and
    12d11' Taurus **at sunrise**. Every method in chapter 5 starts from the
    sunrise value; the birth value is not used.

    Using it would shift both answers by 50 arcminutes.
    """
    at_birth = parse("13 Ta 1")
    assert LADY_SUN_AT_SUNRISE == pytest.approx(30 + 12 + 11 / 60)
    assert at_birth - LADY_SUN_AT_SUNRISE == pytest.approx(50 / 60)


def test_exercise_8_needs_360_removed_four_times_for_gl():
    """1607d48'30" is more than four full circles."""
    raw = LADY_SUN_AT_SUNRISE + LADY_MINUTES * 5 / 4
    assert raw == pytest.approx(1607 + 48.5 / 60)
    assert raw - 4 * 360.0 == pytest.approx(167 + 48.5 / 60)


def test_exercise_8_through_the_endpoint():
    """1252.5 minutes is inside the model's 1500-minute ceiling, which exists
    precisely so a pre-dawn birth is accepted."""
    body = client.post(
        "/v1/lagna/special",
        json={
            "lagnas": ["HL", "GL"],
            "sun_at_sunrise": "12 Ta 11",
            "minutes_since_sunrise": 1252.5,
        },
    ).json()
    got = {x["abbreviation"]: x["rasi_dm"] for x in body["special_lagnas"]}
    assert got == {"HL": "8 Aq 26", "GL": "17 Vi 49"}


def test_exercise_9_through_birthtime_correction():
    """The same answer from `birthtime_correction`, so the exercise checks the
    code rather than arithmetic written beside it.

    A negative shift means the birth was **earlier** than recorded.
    """
    correction = birthtime_correction(
        parse("17 Vi 48") + 0.5 / 60, parse("16 Vi 15"), parse("17 Vi 30")
    )
    assert correction.earliest_shift_minutes * 60 == pytest.approx(-74.8)
    assert correction.latest_shift_minutes * 60 == pytest.approx(-14.8)
    assert correction.earliest_shift_minutes < 0, "the birth was earlier"

    recorded = 3 * 3600 + 11 * 60 + 48
    earliest = recorded + correction.earliest_shift_minutes * 60
    latest = recorded + correction.latest_shift_minutes * 60
    assert (int(earliest // 3600), int(earliest % 3600 // 60)) == (3, 10)
    assert earliest % 60 == pytest.approx(33.2)
    assert (int(latest // 3600), int(latest % 3600 // 60)) == (3, 11)
    assert latest % 60 == pytest.approx(33.2)

    # The book prints whole seconds: "Birthtime has to be between
    # 3:10:33 - 3:11:33 am." Both ends round to those.
    assert round(earliest % 60) == 33
    assert round(latest % 60) == 33


def test_exercise_9_window_is_exactly_one_minute():
    """16d15' to 17d30' is 1d15' — which is exactly GL's travel in one minute.

    The range was chosen to make the answer a clean one-minute window, and the
    window width depends only on the range and the rate, never on where the
    observed value sits.
    """
    low, high = parse("16 Vi 15"), parse("17 Vi 30")
    assert high - low == pytest.approx(1.25)
    assert high - low == ADVANCE_PER_MINUTE[SpecialLagna.GHATI]

    correction = birthtime_correction(parse("17 Vi 48") + 0.5 / 60, low, high)
    assert correction.window_minutes == pytest.approx(1.0)

    # Independent of the observed value.
    for observed in (parse("1 Ar 0"), parse("29 Pi 59"), high):
        assert birthtime_correction(observed, low, high).window_minutes == (
            pytest.approx(1.0)
        )


def test_birthtime_correction_lands_the_lagna_on_the_range_ends():
    """Applying either shift must put GL exactly on the boundary it came
    from — the round trip, which is what makes the inversion trustworthy."""
    sun = parse("12 Ta 11")
    minutes = 1252.5
    rate = ADVANCE_PER_MINUTE[SpecialLagna.GHATI]
    observed = advance_from_sunrise(sun, minutes, rate)
    low, high = parse("16 Vi 15"), parse("17 Vi 30")
    correction = birthtime_correction(observed, low, high)

    at_earliest = advance_from_sunrise(
        sun, minutes + correction.earliest_shift_minutes, rate
    )
    at_latest = advance_from_sunrise(
        sun, minutes + correction.latest_shift_minutes, rate
    )
    assert at_earliest == pytest.approx(low)
    assert at_latest == pytest.approx(high)


def test_birthtime_correction_rejects_an_inverted_range():
    from hora.charts.special_lagna import SpecialLagnaError as Err

    with pytest.raises(Err, match="target_high"):
        birthtime_correction(parse("17 Vi 48"), parse("17 Vi 30"), parse("16 Vi 15"))
    with pytest.raises(Err):
        birthtime_correction(parse("17 Vi 48"), parse("16 Vi 15"), parse("16 Vi 15"))


def test_birthtime_correction_is_slower_for_hora_lagna():
    """The same GL range would need four times the birthtime shift if it were
    Bhaava Lagna, and half if Hora Lagna — the window scales with the rate."""
    low, high = parse("16 Vi 15"), parse("17 Vi 30")
    observed = parse("17 Vi 48") + 0.5 / 60
    windows = {
        lagna: birthtime_correction(observed, low, high, lagna=lagna).window_minutes
        for lagna in (SpecialLagna.BHAAVA, SpecialLagna.HORA, SpecialLagna.GHATI)
    }
    assert windows[SpecialLagna.GHATI] == pytest.approx(1.0)
    assert windows[SpecialLagna.HORA] == pytest.approx(2.5)
    assert windows[SpecialLagna.BHAAVA] == pytest.approx(5.0)


def test_comment_1_says_why_birthtime_correction_matters():
    """"ghati lagna is more sensitive to birthtime errors than normal lagna...
    try to correct the birthtime based on known events first. Wrong data
    produces wrong results. Our analysis can only be as good as our data!"

    Exercise 9 is that instruction carried out.
    """
    assert "correct the birthtime based on known events" in BIRTHTIME_SENSITIVITY_NOTE
    assert "as good as our data" in BIRTHTIME_SENSITIVITY_NOTE


def test_comment_2_birthtime_errors_are_a_fact_of_life():
    """"birthtime errors are a fact of life and we have to live with them...
    there are many people in this world who are born a few minutes apart in
    nearby places and yet lead significantly different lives."

    PVR's argument against choosing coarse methods that hide the problem.
    """
    assert "fact of life" in BIRTHTIME_ERRORS_ARE_A_FACT_NOTE
    assert "few minutes apart" in BIRTHTIME_ERRORS_ARE_A_FACT_NOTE


def test_comment_3_the_two_sunrise_definitions():
    """"Some people define sunrise as the time when the **center** of the
    visual disk... Some other people consider sunrise as the time when the
    **upper tip**... The latter approach is recommended."

    Both are stored and the recommendation is the default. See D-10, OI-19.
    """
    assert set(SUNRISE_DEFINITIONS) == {"disc_centre", "disc_upper_limb"}
    assert "center of the visual disk" in SUNRISE_DEFINITIONS["disc_centre"]
    assert "first ray of Sun is seen" in SUNRISE_DEFINITIONS["disc_upper_limb"]
    assert SUNRISE_RECOMMENDED == "disc_upper_limb"


def test_the_recommended_sunrise_is_the_default():
    """D-10: the book's recommendation outranks PyJHora's disc-centre. Still
    unverified against JHora — OI-19."""
    from hora.core.settings import Settings

    assert Settings().sunrise_mode.value == SUNRISE_RECOMMENDED


# --------------------------------------------------------------------------
# 5.6 Use of Special Lagnas
# --------------------------------------------------------------------------


def test_5_6_every_lagna_shows_self_through_a_different_lens():
    """"In any chart, normal lagna shows self. Hora lagna shows self, from the
    point of view of money, wealth and prosperity. Ghati lagna shows self, from
    the point of view of fame, power and authority."

    The framing matters: these are not separate significators, they are one
    subject seen three ways. Both viewpoints begin with "self".
    """
    assert NORMAL_LAGNA_SHOWS == "self"
    for lagna in (SpecialLagna.HORA, SpecialLagna.GHATI):
        assert SPECIAL_LAGNA_VIEWPOINT[lagna].startswith("self, from the point of view")


def test_5_6_the_short_form_matches_the_long_one():
    """"hora lagna shows money and ghati lagna shows power" — the one-line
    version. SPECIAL_LAGNA_SIGNIFIES carries it; the viewpoint carries the
    fuller wording. They must not drift apart."""
    assert "money" in SPECIAL_LAGNA_SIGNIFIES[SpecialLagna.HORA]
    assert "money" in SPECIAL_LAGNA_VIEWPOINT[SpecialLagna.HORA]
    assert "power" in SPECIAL_LAGNA_SIGNIFIES[SpecialLagna.GHATI]
    assert "power" in SPECIAL_LAGNA_VIEWPOINT[SpecialLagna.GHATI]


def test_5_6_the_two_worked_cases():
    """"when we time good and bad periods for a businessman, hora lagna may be
    very important. When we time good and bad periods for a politician, ghati
    lagna may be very important."""
    assert "businessman" in SPECIAL_LAGNA_USE_EXAMPLES[SpecialLagna.HORA]
    assert "politician" in SPECIAL_LAGNA_USE_EXAMPLES[SpecialLagna.GHATI]


def test_5_6_bhaava_lagna_is_given_no_use():
    """§5.6 names only HL and GL. Footnote 10 says BL is "defined only for the
    sake of completeness", so it has no viewpoint and no worked case."""
    assert SpecialLagna.BHAAVA not in SPECIAL_LAGNA_VIEWPOINT
    assert SpecialLagna.BHAAVA not in SPECIAL_LAGNA_USE_EXAMPLES
    assert SPECIAL_LAGNA_SIGNIFIES[SpecialLagna.BHAAVA] is None


# --------------------------------------------------------------------------
# 5.7 Sree Lagna — Example 10 and Exercise 10
# --------------------------------------------------------------------------


def test_5_7_what_sree_means():
    """"In Sanskrit, the word "Sree" means wealth. It also means Lakshmi, wife
    of Lord Narayana and goddess of wealth."
    """
    assert SREE_MEANING == "wealth"
    assert "Lakshmi" in SREE_ALSO_MEANS
    assert "goddess of wealth" in SREE_ALSO_MEANS
    assert SPECIAL_LAGNA_ABBR[int(SpecialLagna.SREE)] == "SL"


def test_5_7_its_use_is_deferred_to_the_sudasa_chapter():
    """"Its use will be shown in the chapter on Sudasa. Computation of Sree
    Lagna will be explained for now." — so chapter 5 gives the arithmetic
    only, which is all we implement."""
    assert SREE_LAGNA_USED_IN == "Sudasa"
    assert SPECIAL_LAGNA_SIGNIFIES[SpecialLagna.SREE] == "prosperity"


def test_5_7_sree_lagna_does_not_use_sunrise():
    """The only special lagna that does not advance from sunrise — it takes
    the Moon and the lagna and nothing else. So it is the one lagna in the
    chapter that OI-19's sunrise question cannot move."""
    assert SpecialLagna.SREE not in ADVANCE_PER_MINUTE


#: Example 10: "Moon at 13 Li 06 and lagna at 25 Vi 05."
EXAMPLE_10_MOON = parse("13 Li 06")
EXAMPLE_10_LAGNA = parse("25 Vi 05")


def test_example_10_the_two_longitudes():
    """"Moon's longitude is 180d + 13d6' = 193d6'. Lagna's longitude
    150d+25d5' is 175d5'."
    """
    assert EXAMPLE_10_MOON == pytest.approx(193 + 6 / 60)
    assert EXAMPLE_10_LAGNA == pytest.approx(175 + 5 / 60)


def test_example_10_step_1_the_constellation():
    """"Moon is in Swathi constellation, which runs from 6d40' to 20d0' in
    Libra."

    §5.7 spells it "Swathi"; Table 2 spells it "Swaati". Both are the book's.
    """
    nakshatra = int(EXAMPLE_10_MOON * 27 / 360)
    assert NAKSHATRA_NAMES_BOOK[nakshatra] == "Swaati"
    assert NAKSHATRA_NAME_VARIANTS["Swaati"] == "Swathi"
    start = nakshatra * NAKSHATRA_SPAN
    assert start == pytest.approx(parse("6 Li 40"))
    assert start + NAKSHATRA_SPAN == pytest.approx(parse("20 Li 0"))


def test_example_10_step_2_the_fraction_traversed():
    """"Moon's advancement in his constellation is 13d6' - 6d40' = 6d26'. As
    fraction of the whole constellation, this is (6d26')/(13d20') = 386'/800'
    = 0.4825."

    The book works it in arcminutes, so both forms are asserted.
    """
    start = int(EXAMPLE_10_MOON * 27 / 360) * NAKSHATRA_SPAN
    advancement = EXAMPLE_10_MOON - start
    assert advancement == pytest.approx(6 + 26 / 60)
    assert advancement * 60 == pytest.approx(386.0), "386 arcminutes"
    assert NAKSHATRA_SPAN * 60 == pytest.approx(800.0), "800 arcminutes"
    assert advancement / NAKSHATRA_SPAN == pytest.approx(0.4825)
    assert 386.0 / 800.0 == 0.4825


def test_example_10_step_3_the_same_fraction_of_the_zodiac():
    """"The same fraction of the zodiac is 0.4825 x 360d = 173.7d = 173d42'."
    """
    assert 0.4825 * 360 == pytest.approx(173.7)
    assert 173.7 == pytest.approx(173 + 42 / 60)


def test_example_10_step_4_added_to_the_lagna():
    """"Adding this amount to the longitude of lagna, we get 175d5' + 173d42'
    = 348d47'. This is the longitude of SL. So SL is in Pisces at 18d47'."
    """
    got = sree_lagna(EXAMPLE_10_MOON, EXAMPLE_10_LAGNA)
    assert got == pytest.approx(348 + 47 / 60, abs=1e-4)
    assert readable(got) == "18 Pi 47"


def test_example_10_through_the_endpoint():
    body = client.post(
        "/v1/lagna/special",
        json={
            "lagnas": ["SL"],
            "moon": "13 Li 06",
            "lagna": "25 Vi 05",
        },
    ).json()
    sl = body["special_lagnas"][0]
    assert sl["abbreviation"] == "SL"
    assert sl["rasi_dm"] == "18 Pi 47"


#: Exercise 10: "Moon at 15 Le 29 and lagna at 14 Sc 19."
EXERCISE_10_MOON = parse("15 Le 29")
EXERCISE_10_LAGNA = parse("14 Sc 19")
def test_exercise_10_every_intermediate():
    """Worked the same way as Example 10, since the exercise prints only the
    answer: Moon is in Purva Phalguni, 2d9' in, which is 0.16125 of it."""
    nakshatra = int(EXERCISE_10_MOON * 27 / 360)
    assert NAKSHATRA_NAMES[nakshatra] == "Purva Phalguni"
    start = nakshatra * NAKSHATRA_SPAN
    advancement = EXERCISE_10_MOON - start
    assert advancement == pytest.approx(2 + 9 / 60)
    fraction = advancement / NAKSHATRA_SPAN
    assert fraction == pytest.approx(0.16125)
    assert fraction * 360 == pytest.approx(58.05)
    assert EXERCISE_10_LAGNA + fraction * 360 == pytest.approx(282 + 22 / 60, abs=1e-3)


def test_exercise_10_through_the_endpoint():
    body = client.post(
        "/v1/lagna/special",
        json={
            "lagnas": ["SL"],
            "moon": "15 Le 29",
            "lagna": "14 Sc 19",
        },
    ).json()
    assert body["special_lagnas"][0]["rasi_dm"] == "12 Cp 22"
def test_5_7_warns_of_parasara_lagnas_outside_the_book():
    """"There are some more special lagnas defined by Parasara, but they are
    beyond the scope of this book."

    Those will arrive from BPHS with no PVR text to check them against — see
    OI-51 and the precedence rule that BPHS may fill a gap but never override
    PVR without an explicit decision.
    """
    assert "beyond the scope of this book" in MORE_PARASARA_LAGNAS_WARNING
    assert len(SPECIAL_LAGNA_NAMES) == 4, "the four this book defines"
