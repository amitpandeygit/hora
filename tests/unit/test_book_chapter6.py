"""Every claim in Chapter 6 of PVR Narasimha Rao's textbook.

Source: "Vedic Astrology: An Integrated Approach", Chapter 6 (Divisional
Charts), book pages 51-66.

Twenty divisional charts, sixteen worked examples, Table 11's significations,
and the four varga groups with their amsa names.

This chapter was implemented long before it was read — the rules were written
from general classical knowledge — and the audit found **three of them wrong**:
D-5, D-8 and D-11. All three are covered here.

Deviation: PVR-7 in docs/precedence.md — Example 23 miscounts by one.
"""
from itertools import pairwise

import pytest

from hora.charts.vargas import (
    AMSA_NAMES,
    DASAVARGA,
    SAPTAVARGA,
    SHADVARGA,
    SHODASAVARGA,
    VARGA_GROUPS,
    VARGA_REGISTRY,
    VARGA_RULES,
    VARGA_SIGNIFICATIONS,
    charts_for_matter,
    d1_rasi,
    d2_hora,
    d3_drekkana,
    d4_chaturthamsa,
    d5_panchamsa,
    d6_shashtamsa,
    d7_saptamsa,
    d8_ashtamsa,
    d9_navamsa,
    d10_dasamsa,
    d11_rudramsa,
    d12_dwadasamsa,
    d16_shodasamsa,
    d20_vimsamsa,
    d24_chaturvimsamsa,
    d27_nakshatramsa,
    d30_trimsamsa,
    d40_khavedamsa,
    d45_akshavedamsa,
    d60_shashtyamsa,
    part_index,
    part_size_degrees,
    varga,
)
from hora.core import const as c
from hora.core.const import (
    AMSABALA_DIGNITIES,
    AMSABALA_IS_MONOTONIC,
    AMSABALA_RULE,
    CHOOSE_CHART_BY_MATTER,
    D1_ALIAS,
    D2_INCOMPLETE_NOTE,
    DASAVARGA_COMBINATIONS,
    DASAVARGA_NOTE,
    ELEMENT_NAMES,
    FIND_LINKS_METHOD,
    GRAHA_NAMES,
    HIGHER_CHARTS_CAUTION,
    HIGHER_CHARTS_CAUTIONED,
    KAARMIC_PLANE_IS_ABOVE,
    KEY_TO_CHART_ANALYSIS,
    MATTER_ANALYSIS_PATTERNS,
    MODALITY_NAMES,
    RASI_ABBR,
    RASI_ELEMENT,
    RASI_IS_ODD,
    RASI_IS_ODD_FOOTED,
    RASI_LORD,
    RASI_MODALITY,
    VARGA_BODY_DEFINITION,
    VARGA_GROUP_MEANINGS,
    VARGA_PLANES,
    Graha,
)
from hora.services import varga_service

RASI = {a: i for i, a in enumerate(RASI_ABBR)}


def at(abbr: str, degrees: float) -> float:
    return RASI[abbr] * 30.0 + degrees


def sign_of(longitude: float, code: str) -> str:
    return RASI_ABBR[varga(longitude, code).sign]


# --------------------------------------------------------------------------
def readable_sign(sign: int) -> str:
    """The book's two-letter abbreviation for a rasi index."""
    return RASI_ABBR[sign]


# 6.2 The twenty charts — every worked example
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "example,code,rasi,degrees,expected",
    [
        # Example 11 — D-3, three bodies together in Gemini
        (11, "D3", "Ge", 3, "Ge"), (11, "D3", "Ge", 19, "Li"), (11, "D3", "Ge", 21, "Aq"),
        # Example 12 — D-4, three bodies in Taurus
        (12, "D4", "Ta", 3, "Ta"), (12, "D4", "Ta", 14, "Le"), (12, "D4", "Ta", 23, "Aq"),
        # Example 13 — D-6
        (13, "D6", "Ge", 11, "Ge"), (13, "D6", "Sc", 19, "Cp"),
        # Example 14 — D-7
        (14, "D7", "Ge", 10, "Le"), (14, "D7", "Vi", 19, "Cn"),
        # Example 15 — D-8, which our implementation got wrong
        (15, "D8", "Ge", 10, "Li"), (15, "D8", "Sc", 19, "Ta"),
        # Example 16 — D-9
        (16, "D9", "Ge", 11, "Cp"), (16, "D9", "Sc", 19, "Sg"),
        # Example 17 — D-10
        (17, "D10", "Ge", 10, "Vi"), (17, "D10", "Sc", 19, "Cp"),
        # Example 18 — D-11, which our implementation got wrong
        (18, "D11", "Ge", 11, "Ge"), (18, "D11", "Sc", 19, "Pi"),
        # Example 19 — D-12
        (19, "D12", "Ge", 11, "Li"), (19, "D12", "Sc", 19, "Ge"),
        # Example 20 — D-16
        (20, "D16", "Ge", 11, "Ta"), (20, "D16", "Sc", 19, "Ge"),
        # Example 21 — D-20
        (21, "D20", "Ge", 11, "Pi"), (21, "D20", "Sc", 19, "Sg"),
        # Example 22 — D-24
        (22, "D24", "Ge", 11, "Ar"), (22, "D24", "Sc", 19, "Li"),
        # Example 23 — D-27; the Gemini half is PVR-7 and is tested separately
        (23, "D27", "Sc", 19, "Ge"),
        # Example 24 — D-40
        (24, "D40", "Ge", 11, "Ge"), (24, "D40", "Sc", 19, "Sc"),
        # Example 25 — D-45
        (25, "D45", "Ge", 11, "Ar"), (25, "D45", "Sc", 19, "Sg"),
    ],
)
def test_worked_examples(example, code, rasi, degrees, expected):
    assert sign_of(at(rasi, degrees), code) == expected


def test_example_26_shashtyamsa():
    """D-60: "multiply by 2, take degrees, ignore minutes, add 1"."""
    longitude = at("Sc", 12 + 58 / 60)
    assert part_index(longitude, 60) == 26
    assert sign_of(longitude, "D60") == "Sg"


# --------------------------------------------------------------------------
# The three rules the audit corrected
# --------------------------------------------------------------------------

def test_d5_odd_rasi_sequence():
    """6.2.5: odd rasis go into Ar, Aq, Sg, Ge and Li.

    Ours ended the odd sequence in Leo and had the even sequence out of order.
    D-5 has no worked example in the book, which is why nothing caught it.
    """
    assert [sign_of(at("Ar", d), "D5") for d in (1, 7, 13, 19, 25)] == [
        "Ar", "Aq", "Sg", "Ge", "Li"
    ]


def test_d5_even_rasi_sequence():
    """6.2.5: even rasis go into Ta, Vi, Pi, Cp and Sc."""
    assert [sign_of(at("Ta", d), "D5") for d in (1, 7, 13, 19, 25)] == [
        "Ta", "Vi", "Pi", "Cp", "Sc"
    ]


@pytest.mark.parametrize(
    "rasi,modality,start",
    [("Ar", "movable", "Ar"), ("Ta", "fixed", "Sg"), ("Ge", "dual", "Le")],
)
def test_d8_starts_from_ar_sg_or_le(rasi, modality, start):
    """6.2.8 counts from Ar, Sg or Le — NOT the Ar, Le, Sg of D-16 and D-45.

    Conflating the two orders is what made D-8 wrong.
    """
    assert sign_of(at(rasi, 0.1), "D8") == start


def test_d8_and_d16_use_different_orders():
    """The book gives both explicitly and they differ; a shared table is a bug."""
    dual = at("Ge", 0.1)
    assert sign_of(dual, "D8") == "Le"
    assert sign_of(dual, "D16") == "Sg"


@pytest.mark.parametrize(
    "rasi,start",
    [("Ar", "Ar"), ("Ta", "Pi"), ("Ge", "Aq"), ("Cn", "Cp"), ("Sc", "Vi")],
)
def test_d11_starts_from_the_rasi_reflected_about_aries(rasi, start):
    """6.2.11: count the rasi's position from Ar, then count that many back.

    Gemini is the 3rd from Aries; the 3rd from Aries counting backwards is
    Aquarius, which is where Example 18 starts.
    """
    assert sign_of(at(rasi, 0.1), "D11") == start


# --------------------------------------------------------------------------
# PVR-7 — Example 23 miscounts
# --------------------------------------------------------------------------

def test_example_23_gemini_half_follows_the_rule_not_the_printed_answer():
    """PVR-7: "The 10th from Li is Le" — it is Cancer.

    Counting Libra as the 1st: Li, Sc, Sg, Cp, Aq, Pi, Ar, Ta, Ge, Cn. Leo is
    the 11th. The stated rule (§6.2.16, count from Ar/Cn/Li/Cp by element) and
    the part index the example itself gives (the 10th) both yield Cancer.

    Tie-break rule 1 — a stated rule beats its transcribed output.
    """
    longitude = at("Ge", 11)
    assert part_index(longitude, 27) == 10          # the example agrees so far
    assert sign_of(longitude, "D27") == "Cn"
    assert sign_of(longitude, "D27") != "Le"        # what Example 23 prints


def test_the_other_half_of_example_23_reproduces():
    """Only the Gemini half is wrong; Sc 19 -> Ge is correct."""
    assert sign_of(at("Sc", 19), "D27") == "Ge"


# --------------------------------------------------------------------------
# 6.2 Part sizes, as the book states them
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "divisions,degrees,minutes,seconds",
    [
        (2, 15, 0, 0), (3, 10, 0, 0), (4, 7, 30, 0), (5, 6, 0, 0), (6, 5, 0, 0),
        (7, 4, 17, 8.57), (8, 3, 45, 0), (9, 3, 20, 0), (10, 3, 0, 0),
        (11, 2, 43, 38), (12, 2, 30, 0), (16, 1, 52, 30), (20, 1, 30, 0),
        (24, 1, 15, 0), (27, 1, 6, 40), (40, 0, 45, 0), (45, 0, 40, 0),
        (60, 0, 30, 0),
    ],
)
def test_part_sizes(divisions, degrees, minutes, seconds):
    """The book prints these to whole arcseconds, so allow half of one.

    D-11 is the tight case: 30/11 is 2 deg 43' 38.18", printed as 2 deg 43' 38".
    """
    expected = degrees + minutes / 60 + seconds / 3600
    assert part_size_degrees(divisions) == pytest.approx(expected, abs=0.5 / 3600)


# --------------------------------------------------------------------------
# 6.3 Table 11 — significations
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "code,fragment",
    [
        ("D1", "physical level"), ("D2", "Wealth and money"),
        ("D3", "brothers and sisters"), ("D4", "Residence"),
        ("D5", "Fame, authority and power"), ("D6", "Health troubles"),
        ("D7", "children"), ("D8", "Sudden and unexpected troubles"),
        ("D9", "Marriage"), ("D10", "Career"), ("D11", "Death and destruction"),
        ("D12", "parents"), ("D16", "Vehicles"), ("D20", "spiritual"),
        ("D24", "Learning"), ("D27", "Strengths and weaknesses"),
        ("D30", "Evils and punishment"), ("D40", "Auspicious"),
        ("D45", "All matters"), ("D60", "Karma of past life"),
    ],
)
def test_table_11_significations(code, fragment):
    assert fragment in VARGA_SIGNIFICATIONS[code]


def test_table_11_covers_twenty_charts():
    assert len(VARGA_SIGNIFICATIONS) == 20


# --------------------------------------------------------------------------
# 6.6 Varga groups and amsabala
# --------------------------------------------------------------------------

def test_shadvarga_membership():
    """6.6.1: rasi, D-2, D-3, D-9, D-12, D-30."""
    assert list(SHADVARGA) == ["D1", "D2", "D3", "D9", "D12", "D30"]


def test_saptavarga_membership():
    """6.6.2: shadvarga plus D-7."""
    assert list(SAPTAVARGA) == ["D1", "D2", "D3", "D7", "D9", "D12", "D30"]
    assert set(SHADVARGA) < set(SAPTAVARGA)


def test_dasavarga_membership():
    """6.6.3: rasi, D-2, D-3, D-7, D-9, D-10, D-12, D-16, D-30, D-60."""
    assert list(DASAVARGA) == [
        "D1", "D2", "D3", "D7", "D9", "D10", "D12", "D16", "D30", "D60"
    ]


def test_shodasavarga_membership():
    """6.6.4: the sixteen."""
    assert list(SHODASAVARGA) == [
        "D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16",
        "D20", "D24", "D27", "D30", "D40", "D45", "D60",
    ]
    assert set(DASAVARGA) < set(SHODASAVARGA)


@pytest.mark.parametrize(
    "group,size", [("shadvarga", 6), ("saptavarga", 7),
                   ("dasavarga", 10), ("shodasavarga", 16)],
)
def test_group_sizes_match_their_names(group, size):
    """"Shadvarga" is six divisions, "shodasa varga" sixteen, and so on."""
    assert len(VARGA_GROUPS[group]) == size


@pytest.mark.parametrize(
    "group,count,name",
    [
        ("shadvarga", 2, "Kimsukaamsa"), ("shadvarga", 6, "Kundalaamsa"),
        ("saptavarga", 7, "Mukutaamsa"),
        ("dasavarga", 2, "Paarijaataamsa"), ("dasavarga", 5, "Simhaasanaamsa"),
        ("dasavarga", 10, "Sreedhaamaamsa"),
        ("shodasavarga", 2, "Bhedakaamsa"), ("shodasavarga", 16, "Sree Vallabhaamsa"),
    ],
)
def test_amsa_names(group, count, name):
    assert AMSA_NAMES[group][count] == name


@pytest.mark.parametrize("group", list(AMSA_NAMES))
def test_amsa_names_start_at_two_and_run_to_the_group_size(group):
    """The book names nothing below a count of two, and nothing is invented."""
    counts = sorted(AMSA_NAMES[group])
    assert counts == list(range(2, len(VARGA_GROUPS[group]) + 1))


def test_amsabala_counts_only_moolatrikona_own_and_exaltation():
    """6.6: "moolatrikona or an own rasi or its rasi of exaltation"."""
    from hora.core.const import Graha
    from hora.services.varga_service import amsabala

    result = amsabala(at("Ar", 10), Graha.SUN)
    for group in result["groups"].values():
        for entry in group["strong_in"]:
            assert entry["dignity"] in {"moolatrikona", "own", "exalted"}
        assert group["count"] == len(group["strong_in"])


def test_amsabala_names_the_amsa_for_the_count():
    from hora.core.const import Graha
    from hora.services.varga_service import amsabala

    result = amsabala(at("Ar", 10), Graha.SUN)
    for name, group in result["groups"].items():
        expected = AMSA_NAMES[name].get(group["count"])
        assert group["amsa"] == expected


def test_amsabala_leaves_a_low_count_unnamed():
    """Below two, the book names no amsa, so neither do we."""
    from hora.core.const import Graha
    from hora.services.varga_service import amsabala

    # Sun in Aquarius is in neither its own rasi, moolatrikona nor exaltation.
    result = amsabala(at("Aq", 5), Graha.SUN)
    for group in result["groups"].values():
        if group["count"] < 2:
            assert group["amsa"] is None


# --------------------------------------------------------------------------
# Rule metadata and the aliases the chapter gives
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "code,alias",
    [
        ("D1", "Kshetra Chakra"), ("D4", "Turyamsa"), ("D9", "Dharmamsa"),
        ("D10", "Karmamsa"), ("D11", "Ekadasamsa"), ("D16", "Kalamsa"),
        ("D24", "Siddhamsa"), ("D27", "Bhamsa"), ("D40", "Chatvarimsamsa"),
        ("D45", "Pancha-chatvarimsamsa"),
    ],
)
def test_aliases_the_chapter_gives(code, alias):
    assert alias in VARGA_RULES[code]["aliases"]


def test_charts_without_a_worked_example_are_marked():
    """These are the rules a transcription error can hide in.

    D-5 was wrong for exactly this reason: no example to catch it.
    """
    unexampled = {c for c, r in VARGA_RULES.items() if not r["example"]}
    assert "D5" in unexampled
    assert "D2" in unexampled
    assert "D9" not in unexampled


# --------------------------------------------------------------------------
# The endpoint
# --------------------------------------------------------------------------

def test_compute_endpoint_accepts_all_three_notations(client):
    for value in ["11 Ge 00", "2s 11 00", 71.0]:
        body = client.post(
            "/v1/varga/compute", json={"longitude": value, "charts": ["D9"]}
        ).json()
        assert body["charts"][0]["rasi_name"] == "Capricorn", value


def test_compute_endpoint_explains_the_placement(client):
    body = client.post(
        "/v1/varga/compute", json={"longitude": "11 Ge 00", "charts": ["D8"]}
    ).json()
    chart = body["charts"][0]
    assert chart["part_index"] == 3
    assert chart["divisions"] == 8
    assert "movable, fixed or dual" in chart["counts_from"]


def test_rules_endpoint_publishes_groups_and_amsa_names(client):
    body = client.get("/v1/varga/rules").json()
    assert set(body["groups"]) == set(VARGA_GROUPS)
    assert body["amsa_names"]["dasavarga"]["5"] == "Simhaasanaamsa"


def test_compute_endpoint_rejects_an_unparseable_longitude(client):
    response = client.post(
        "/v1/varga/compute", json={"longitude": "not a longitude", "charts": ["D9"]}
    )
    assert response.status_code == 400
    assert response.json()["error"]["type"] == "bad_request"


# --------------------------------------------------------------------------
# Input guards
#
# A varga is arithmetic on a longitude, and arithmetic on nonsense produced
# nonsense: a NaN longitude surfaced as "cannot convert float NaN to integer"
# from inside a floor division, and a zero division count raised
# ZeroDivisionError. Neither named the input that was wrong.
# --------------------------------------------------------------------------

def test_non_finite_longitudes_are_rejected():
    from hora.core.validate import InputError

    for bad in (float("nan"), float("inf"), float("-inf")):
        with pytest.raises(InputError, match="finite"):
            varga(bad, "D9")


@pytest.mark.parametrize("divisions", [0, -1, 301, 10_000])
def test_division_counts_outside_1_to_300_are_rejected(divisions):
    from hora.core.validate import InputError

    with pytest.raises(InputError, match="between 1 and 300"):
        part_size_degrees(divisions)
    with pytest.raises(InputError, match="between 1 and 300"):
        part_index(10.0, divisions)


def test_the_generic_chart_rejects_an_out_of_range_code():
    from hora.core.validate import InputError

    with pytest.raises(InputError, match="between 1 and 300"):
        varga(10.0, "D0")
    with pytest.raises(InputError, match="between 1 and 300"):
        varga(10.0, "D999")


@pytest.mark.parametrize("longitude,equivalent", [(-45.0, 315.0), (405.0, 45.0),
                                                 (-0.5, 359.5), (720.0, 0.0)])
def test_longitudes_still_wrap_around_the_zodiac(longitude, equivalent):
    """Wrapping is deliberate — the book says to "expunge multiples of 360"."""
    assert varga(longitude, "D9").sign == varga(equivalent, "D9").sign
    assert varga(longitude, "D60").sign == varga(equivalent, "D60").sign


def test_compute_endpoint_rejects_an_empty_chart_list(client):
    """Asking for no charts is a mistake, not a request for nothing."""
    response = client.post("/v1/varga/compute", json={"longitude": 10.0, "charts": []})
    assert response.status_code == 422


def test_compute_endpoint_caps_the_request_size(client):
    """Unbounded fan-out is a denial-of-service shape, however cheap each is."""
    assert client.post(
        "/v1/varga/compute", json={"longitude": 10.0, "charts": ["D9"] * 64}
    ).status_code == 200
    assert client.post(
        "/v1/varga/compute", json={"longitude": 10.0, "charts": ["D9"] * 65}
    ).status_code == 422


@pytest.mark.parametrize("code", ["D0", "D999", "Q9"])
def test_compute_endpoint_rejects_bad_chart_codes(code, client):
    response = client.post("/v1/varga/compute", json={"longitude": 10.0, "charts": [code]})
    assert response.status_code == 400
    assert response.json()["error"]["type"] == "bad_request"


def test_compute_endpoint_rejects_an_unknown_variant(client):
    response = client.post(
        "/v1/varga/compute",
        json={"longitude": 10.0, "charts": ["D9"], "variants": {"D9": "nope"}},
    )
    assert response.status_code == 400
    assert "variant" in response.json()["error"]["message"]


# --------------------------------------------------------------------------
# 6.2.1 Rasi Chart (D-1)
# --------------------------------------------------------------------------


def test_6_2_1_the_rasi_chart_is_a_varga_too():
    """"A simple example of divisions is rasi chart itself. It is also called
    "kshetra chakra". It is denoted by D-1."

    D-1 divides each rasi into one part, so it is the identity — but it is a
    varga by the book's own framing, not an exception to the scheme.
    """
    assert D1_ALIAS == "kshetra chakra"
    for degrees in (0.0, 15.0, 29.999, 180.0, 359.999):
        assert d1_rasi(degrees).sign == int(degrees // 30)
        assert d1_rasi(degrees).amsa_index == 0, "one part per rasi"


def test_6_2_1_longitudes_map_to_rasis_thirty_degrees_at_a_time():
    """"Longitudes in the range 0d-30d are mapped to Aries, 30d-60d to Taurus
    and so on."""
    assert d1_rasi(0.0).sign == 0
    assert d1_rasi(29.999).sign == 0
    assert d1_rasi(30.0).sign == 1
    assert d1_rasi(59.999).sign == 1


def test_6_2_1_a_body_is_anything_with_a_longitude():
    """"By "body" here, we mean planets, upagrahas, lagna or special lagnas -
    basically a physical or a mathematical point in the zodiac that has a
    longitude associated with it."

    The only place the book says the **upagrahas and special lagnas** belong
    in a divisional chart, not just the nine grahas. It licenses putting an
    upagraha or a GL into D-9, which nothing else in the book states.
    """
    for term in ("planets", "upagrahas", "lagna", "special lagnas"):
        assert term in VARGA_BODY_DEFINITION
    assert "has a longitude associated with it" in VARGA_BODY_DEFINITION


# --------------------------------------------------------------------------
# 6.2.2 Hora Chart (D-2)
# --------------------------------------------------------------------------

#: §6.2.2's four cases. Gemini is odd, Taurus even.
D2_CASES = [
    ("Ge", 3, "Sun", "Le"),      # first 15 of an odd rasi
    ("Ge", 21, "Moon", "Cn"),    # second 15 of an odd rasi
    ("Ta", 3, "Moon", "Cn"),     # first 15 of an even rasi
    ("Ta", 21, "Sun", "Le"),     # second 15 of an even rasi
]


@pytest.mark.parametrize("rasi,degrees,lord,expected", D2_CASES)
def test_6_2_2_the_four_hora_cases(rasi, degrees, lord, expected):
    """"Bodies in the first 15d of odd rasis are in Sun's hora. Bodies in the
    second 15d of odd rasis are in Moon's hora. Bodies in the first 15d of
    even rasis are in Moon's hora. Bodies in the second 15d of even rasis are
    in Sun's hora."

    The hora is named by its lord; the chart places the body in the rasi that
    lord owns — Leo for the Sun, Cancer for the Moon.
    """
    abbr = list(RASI_ABBR)
    longitude = abbr.index(rasi) * 30 + degrees
    assert readable_sign(d2_hora(longitude).sign) == expected
    assert GRAHA_NAMES[RASI_LORD[abbr.index(expected)]] == lord


def test_6_2_2_each_rasi_splits_into_two_equal_halves():
    """"Each rasi is divided into 2 equal parts of 15d each."""
    for rasi in range(12):
        base = rasi * 30
        assert d2_hora(base).amsa_index == 0
        assert d2_hora(base + 14.999).amsa_index == 0
        assert d2_hora(base + 15.0).amsa_index == 1
        assert d2_hora(base + 29.999).amsa_index == 1


def test_6_2_2_only_cancer_and_leo_are_ever_occupied():
    """Every body lands in the Sun's or the Moon's own rasi, so a D-2 chart
    has bodies in at most two signs. A varga that used all twelve would be
    wrong."""
    landed = {d2_hora(x / 10).sign for x in range(3600)}
    assert landed == {list(RASI_ABBR).index("Cn"), list(RASI_ABBR).index("Le")}


def test_6_2_2_the_odd_and_even_split_is_2_2_2s():
    """"odd rasis" and "even rasis" here are §2.2.2's, counted from Aries —
    not §2.2.3's odd-footed split, which partitions the same twelve signs
    differently."""
    abbr = list(RASI_ABBR)
    assert RASI_IS_ODD[abbr.index("Ge")] is True
    assert RASI_IS_ODD[abbr.index("Ta")] is False
    # And the two splits genuinely differ, so picking the wrong one matters.
    assert RASI_IS_ODD[abbr.index("Ta")] != RASI_IS_ODD_FOOTED[abbr.index("Ta")]


def test_6_2_2_the_book_declines_to_complete_the_rule():
    """"Though absolutely correct, the above is not quite complete. Proper use
    of hora chart is beyond the scope of this book. So we will ignore and not
    use hora chart in this book."

    So D-2 is implemented from a rule PVR calls **correct but incomplete**,
    and the completion is nowhere in the book. See OI-52.
    """
    assert "absolutely correct" in D2_INCOMPLETE_NOTE
    assert "not quite complete" in D2_INCOMPLETE_NOTE
    assert "not use hora chart in this book" in D2_INCOMPLETE_NOTE


# --------------------------------------------------------------------------
# 6.2.3 Drekkana Chart (D-3) and Example 11
# --------------------------------------------------------------------------


def test_6_2_3_the_three_drekkana_cases():
    """"Bodies in the first 10d of a rasi are placed in drekkana chart in the
    same rasi. Bodies in the middle 10d of a rasi are placed in drekkana chart
    in the 5th from the rasi. Bodies in the last 10d of a rasi are placed in
    drekkana chart in the 9th from the rasi."

    Checked from every rasi, not only Gemini — the offsets are 0, 4 and 8, and
    the rule says nothing about odd or even, unlike D-2.
    """
    for rasi in range(12):
        base = rasi * 30
        assert d3_drekkana(base + 5).sign == rasi, "the same rasi"
        assert d3_drekkana(base + 15).sign == (rasi + 4) % 12, "the 5th"
        assert d3_drekkana(base + 25).sign == (rasi + 8) % 12, "the 9th"


def test_6_2_3_the_three_parts_are_ten_degrees_each():
    """"Each rasi is divided into 3 equal parts of 10d each."""
    for rasi in range(12):
        base = rasi * 30
        for degrees, index in ((0, 0), (9.999, 0), (10, 1), (19.999, 1), (20, 2)):
            assert d3_drekkana(base + degrees).amsa_index == index


def test_6_2_3_the_drekkanas_of_a_rasi_are_the_trines():
    """Same, 5th and 9th from a rasi are its three trines. Worth naming: it
    means a D-3 chart never moves a body out of its own element."""
    for rasi in range(12):
        signs = {d3_drekkana(rasi * 30 + d).sign for d in (5, 15, 25)}
        assert signs == {rasi, (rasi + 4) % 12, (rasi + 8) % 12}
        assert len({RASI_ELEMENT[s] for s in signs}) == 1, "one element"


#: Example 11: "Mercury, Jupiter and Venus are together in Gemini in rasi
#: chart. Mercury is at 3d. Jupiter is at 19d. Venus is at 21d."
EXAMPLE_11 = [
    ("Mercury", 3, "0-10", "Ge"),
    ("Jupiter", 19, "10-20", "Li"),
    ("Venus", 21, "20-30", "Aq"),
]


@pytest.mark.parametrize("who,degrees,band,expected", EXAMPLE_11)
def test_example_11_which_band_each_body_falls_in(who, degrees, band, expected):
    """"Mercury is in the first 10d (0d-10d), Jupiter is in the middle 10d
    (10d-20d) and Venus is in the last 10d (20d-30d)."""
    low, high = (int(x) for x in band.split("-"))
    assert low <= degrees < high
    assert d3_drekkana(list(RASI_ABBR).index("Ge") * 30 + degrees).amsa_index == (
        low // 10
    )


@pytest.mark.parametrize("who,degrees,band,expected", EXAMPLE_11)
def test_example_11_drekkana_placement(who, degrees, band, expected):
    """"Mercury is placed in Gemini itself; Jupiter is placed in Libra (5th
    from Gemini); and, Venus is placed in Aquarius (9th from Gemini)."""
    longitude = list(RASI_ABBR).index("Ge") * 30 + degrees
    assert readable_sign(d3_drekkana(longitude).sign) == expected


def test_example_11_three_bodies_together_in_d1_are_scattered_in_d3():
    """The point of the example: all three share Gemini in the rasi chart and
    land in three different signs in D-3. That is what a varga is for."""
    base = list(RASI_ABBR).index("Ge") * 30
    d1_signs = {d1_rasi(base + d).sign for _, d, _, _ in EXAMPLE_11}
    d3_signs = {d3_drekkana(base + d).sign for _, d, _, _ in EXAMPLE_11}
    assert len(d1_signs) == 1, "together in the rasi chart"
    assert len(d3_signs) == 3, "apart in the drekkana chart"


def test_example_11_in_the_hora_chart_too():
    """The book does not work D-2 for Example 11, but the same three bodies
    give a third pattern: Mercury alone in the Sun's hora, the other two
    together in the Moon's. Gemini is odd, so the first 15d is the Sun's.
    """
    base = list(RASI_ABBR).index("Ge") * 30
    got = {who: readable_sign(d2_hora(base + d).sign) for who, d, _, _ in EXAMPLE_11}
    assert got == {"Mercury": "Le", "Jupiter": "Cn", "Venus": "Cn"}


# --------------------------------------------------------------------------
# 6.2.4 Chaturthamsa (D-4) and Example 12
# --------------------------------------------------------------------------


def test_6_2_4_the_four_offsets():
    """"Bodies in the first, second, third and fourth 7.5d arc of a rasi are
    in the 1st, 4th, 7th and 10th from that rasi (respectively)."

    Checked from every rasi: the offsets are 0, 3, 6, 9 — the kendras.
    """
    for rasi in range(12):
        base = rasi * 30
        for part, house in enumerate((1, 4, 7, 10)):
            longitude = base + part * 7.5 + 1.0
            assert d4_chaturthamsa(longitude).sign == (rasi + house - 1) % 12


def test_6_2_4_the_four_parts_are_seven_and_a_half_degrees():
    """"Each rasi is divided into 4 equal parts of 7.5d each."""
    assert 30.0 / 4 == 7.5
    for part, (low, high) in enumerate(((0, 7.5), (7.5, 15), (15, 22.5), (22.5, 30))):
        assert d4_chaturthamsa(low).amsa_index == part
        assert d4_chaturthamsa(high - 0.001).amsa_index == part


def test_6_2_4_the_destinations_are_the_kendras():
    """1st, 4th, 7th, 10th from a rasi are its four kendras. So a D-4 chart
    never moves a body off the natal sign's angular axis."""
    for rasi in range(12):
        signs = {d4_chaturthamsa(rasi * 30 + p * 7.5 + 1).sign for p in range(4)}
        assert signs == {(rasi + k) % 12 for k in (0, 3, 6, 9)}


def test_6_2_4_the_two_other_names():
    """"This chart is also known as Chaturamsa or Turyamsa."""
    assert VARGA_RULES["D4"]["aliases"] == ["Chaturamsa", "Turyamsa"]


def test_6_2_1_alias_matches_the_varga_rules_entry():
    """D1_ALIAS and VARGA_RULES["D1"] both carry the kshetra chakra name.
    Asserted so the two cannot drift apart."""
    assert D1_ALIAS.lower() in [a.lower() for a in VARGA_RULES["D1"]["aliases"]]


#: Example 12: "Mercury, Jupiter and Venus are together in Taurus. Mercury is
#: at 3d, Jupiter is at 14d and Venus is at 23d."
EXAMPLE_12 = [
    ("Mercury", 3, 1, "Ta"),     # 0-7.5, the 1st from Ta
    ("Jupiter", 14, 4, "Le"),    # 7.5-15, the 4th
    ("Venus", 23, 10, "Aq"),     # 22.5-30, the 10th
]


@pytest.mark.parametrize("who,degrees,house,expected", EXAMPLE_12)
def test_example_12_chaturthamsa(who, degrees, house, expected):
    """"Mercury is in 0d-7.5d arc... So he is in Ta (1st from Ta) in D-4.
    Jupiter is in 7.5d-15d arc... Le (4th from Ta). Venus is in 22.5d-30d
    arc... Aq (10th from Ta)."""
    base = list(RASI_ABBR).index("Ta") * 30
    got = d4_chaturthamsa(base + degrees)
    assert readable_sign(got.sign) == expected
    assert got.sign == (list(RASI_ABBR).index("Ta") + house - 1) % 12


def test_example_12_skips_the_third_arc():
    """The book works the 1st, 2nd and 4th arcs and never places a body in the
    3rd. Nothing lands in the 7th from Taurus, which is Scorpio."""
    assert {h for _, _, h, _ in EXAMPLE_12} == {1, 4, 10}
    base = list(RASI_ABBR).index("Ta") * 30
    assert readable_sign(d4_chaturthamsa(base + 16).sign) == "Sc", "the 7th, untested"


# --------------------------------------------------------------------------
# 6.2.5 Panchamsa (D-5)
# --------------------------------------------------------------------------

#: §6.2.5's two explicit sequences. D-12 was a defect here — the odd sequence
#: had ended in Leo and the even one had been reordered.
D5_ODD = ["Ar", "Aq", "Sg", "Ge", "Li"]
D5_EVEN = ["Ta", "Vi", "Pi", "Cp", "Sc"]


def test_6_2_5_the_odd_sequence():
    """"Bodies in the 5 parts of an odd rasi go into Ar, Aq, Sg, Ge and Li
    (respectively)."""
    for rasi in range(12):
        if not RASI_IS_ODD[rasi]:
            continue
        got = [readable_sign(d5_panchamsa(rasi * 30 + p * 6 + 1).sign) for p in range(5)]
        assert got == D5_ODD, RASI_ABBR[rasi]


def test_6_2_5_the_even_sequence():
    """"Bodies in the 5 parts of an even rasi go into Ta, Vi, Pi, Cp and Sc
    (respectively)."""
    for rasi in range(12):
        if RASI_IS_ODD[rasi]:
            continue
        got = [readable_sign(d5_panchamsa(rasi * 30 + p * 6 + 1).sign) for p in range(5)]
        assert got == D5_EVEN, RASI_ABBR[rasi]


def test_6_2_5_the_sequences_are_absolute_not_relative():
    """Unlike D-3, D-4 and D-7, the D-5 destinations do **not** depend on the
    natal rasi — every odd rasi sends its five parts to the same five signs.
    That is why a "count from the rasi" implementation would be wrong here."""
    odd = [readable_sign(d5_panchamsa(0 * 30 + p * 6 + 1).sign) for p in range(5)]
    other_odd = [
        readable_sign(d5_panchamsa(8 * 30 + p * 6 + 1).sign) for p in range(5)
    ]
    assert odd == other_odd == D5_ODD


def test_6_2_5_the_five_parts_are_six_degrees():
    """"Each rasi is divided into 5 equal parts of 6d each."""
    assert 30.0 / 5 == 6.0
    for part in range(5):
        assert d5_panchamsa(part * 6.0).amsa_index == part
        assert d5_panchamsa(part * 6.0 + 5.999).amsa_index == part


def test_6_2_5_has_no_worked_example():
    """D-5 is one of the charts the book never works through, which is exactly
    why the D-12 defect survived until a full longitude sweep found it."""
    assert VARGA_RULES["D5"]["example"] is False


# --------------------------------------------------------------------------
# 6.2.6 Shashthamsa (D-6) and Example 13
# --------------------------------------------------------------------------


def test_6_2_6_counting_starts_from_aries_or_libra():
    """"Bodies in the 6 parts of a rasi go into the 6 rasis starting from Ar
    or Li, based on whether the rasi is odd or even."""
    for rasi in range(12):
        start = 0 if RASI_IS_ODD[rasi] else 6
        for part in range(6):
            got = d6_shashtamsa(rasi * 30 + part * 5 + 1).sign
            assert got == (start + part) % 12, (RASI_ABBR[rasi], part)


def test_6_2_6_the_six_parts_are_five_degrees():
    """"Each rasi is divided into 6 equal parts of 5d each."""
    assert 30.0 / 6 == 5.0
    for part in range(6):
        assert d6_shashtamsa(part * 5.0).amsa_index == part


def test_6_2_6_only_the_first_half_of_the_zodiac_is_used_by_odd_rasis():
    """Starting at Aries and taking six signs reaches Virgo; starting at Libra
    reaches Pisces. So D-6 splits the zodiac in half by the natal parity."""
    odd_signs = {d6_shashtamsa(0 * 30 + p * 5 + 1).sign for p in range(6)}
    even_signs = {d6_shashtamsa(1 * 30 + p * 5 + 1).sign for p in range(6)}
    assert odd_signs == set(range(6))
    assert even_signs == set(range(6, 12))
    assert odd_signs & even_signs == set()


#: Example 13: "Mercury is at 11d in Ge and Jupiter is at 19d in Sc."
EXAMPLE_13 = [
    ("Mercury", "Ge", 11, 3, "Ar", "Ge"),
    ("Jupiter", "Sc", 19, 4, "Li", "Cp"),
]


@pytest.mark.parametrize("who,rasi,degrees,part,start,expected", EXAMPLE_13)
def test_example_13_shashthamsa(who, rasi, degrees, part, start, expected):
    """"11d is in the 3rd part of the rasi and 19d is in the 4th part. Ge is
    an odd rasi and counting starts from Ar. The 3rd from Ar is Ge... Sc is an
    even rasi and counting starts from Li. The 4th from Li is Cp."""
    longitude = list(RASI_ABBR).index(rasi) * 30 + degrees
    got = d6_shashtamsa(longitude)
    assert got.amsa_index == part - 1, f"the {part}th part"
    assert readable_sign(got.sign) == expected
    # And the count really starts where the book says.
    start_index = list(RASI_ABBR).index(start)
    assert got.sign == (start_index + part - 1) % 12


# --------------------------------------------------------------------------
# 6.2.7 Saptamsa (D-7) and Example 14
# --------------------------------------------------------------------------


def test_6_2_7_the_part_size_is_four_degrees_seventeen_minutes():
    """"Each rasi is divided into 7 equal parts of 4d 17' 8.57"."""
    part = 30.0 / 7
    assert part == pytest.approx(4 + 17 / 60 + 8.57 / 3600, abs=1e-6)
    assert part_size_degrees(7) == pytest.approx(part)


def test_6_2_7_odd_rasis_count_from_themselves_and_even_from_the_seventh():
    """"Bodies in the 1st ... 7th parts of a rasi go into the 7 rasis starting
    from the rasi itself, if it is an odd rasi, or starting from the 7th sign
    from it, if it is an even rasi."""
    part = 30.0 / 7
    for rasi in range(12):
        start = rasi if RASI_IS_ODD[rasi] else (rasi + 6) % 12
        for index in range(7):
            got = d7_saptamsa(rasi * 30 + index * part + 0.5).sign
            assert got == (start + index) % 12, (RASI_ABBR[rasi], index)


def test_6_2_7_an_even_rasi_starts_opposite_itself():
    """"the 7th sign from it" is the opposite sign — 180 degrees away."""
    for rasi in range(12):
        if RASI_IS_ODD[rasi]:
            continue
        first = d7_saptamsa(rasi * 30 + 0.5).sign
        assert first == (rasi + 6) % 12
        assert abs(first * 30 - rasi * 30) in (180, 180)


#: Example 14: "Mercury is at 10d in Ge and Jupiter is at 19d in Vi."
EXAMPLE_14 = [
    ("Mercury", "Ge", 10, 3, "Ge", "Le"),
    ("Jupiter", "Vi", 19, 5, "Pi", "Cn"),
]


@pytest.mark.parametrize("who,rasi,degrees,part,start,expected", EXAMPLE_14)
def test_example_14_saptamsa(who, rasi, degrees, part, start, expected):
    """"10d is in the 3rd part of the rasi and 19d is in the 5th part. Because
    Ge is an odd rasi, the 3rd part in Ge goes into the 3rd from Ge, i.e. Le.
    ... Vi is an even sign and counting starts from the 7th from it, i.e. Pi.
    The 5th from Pi is Cn."""
    longitude = list(RASI_ABBR).index(rasi) * 30 + degrees
    got = d7_saptamsa(longitude)
    assert got.amsa_index == part - 1, f"the {part}th part"
    assert readable_sign(got.sign) == expected
    start_index = list(RASI_ABBR).index(start)
    assert got.sign == (start_index + part - 1) % 12


def test_example_14_the_part_boundaries_put_the_bodies_where_the_book_says():
    """10d and 19d are not obviously in the 3rd and 5th parts — the parts are
    4d17'8.57" wide, so the boundaries fall at 8.57, 12.86, 17.14, 21.43.
    Asserted because a wrong part size would still give a plausible sign."""
    part = 30.0 / 7
    assert 2 * part < 10 < 3 * part, "10d is in the 3rd part"
    assert 4 * part < 19 < 5 * part, "19d is in the 5th part"


# --------------------------------------------------------------------------
# The four charts together
# --------------------------------------------------------------------------


@pytest.mark.parametrize("code,divisions,fn", [
    ("D4", 4, d4_chaturthamsa), ("D5", 5, d5_panchamsa),
    ("D6", 6, d6_shashtamsa), ("D7", 7, d7_saptamsa),
])
def test_each_chart_uses_every_part_index_and_no_more(code, divisions, fn):
    """A varga with n divisions must produce amsa indices 0..n-1 and nothing
    else, for every longitude in the zodiac."""
    seen = {fn(x / 100).amsa_index for x in range(36000)}
    assert seen == set(range(divisions)), code
    assert part_size_degrees(divisions) == pytest.approx(30.0 / divisions)


# --------------------------------------------------------------------------
# 6.2.8 Ashtamsa (D-8) and Example 15
# --------------------------------------------------------------------------

#: §6.2.8: "starting from Ar, Sg or Le, based on whether the rasi is a
#: movable, fixed or dual sign." Not the Ar/Le/Sg order D-16 and D-45 use —
#: conflating them was D-13.
D8_START = {"chara": "Ar", "sthira": "Sg", "dwiswabhava": "Le"}


@pytest.mark.parametrize("modality,start", list(D8_START.items()))
def test_6_2_8_the_start_sign_by_modality(modality, start):
    index = MODALITY_NAMES.index(modality)
    expected = list(RASI_ABBR).index(start)
    for rasi in range(12):
        if RASI_MODALITY[rasi] != index:
            continue
        for part in range(8):
            got = d8_ashtamsa(rasi * 30 + part * 3.75 + 0.5).sign
            assert got == (expected + part) % 12, (RASI_ABBR[rasi], part)


def test_6_2_8_is_not_the_order_used_by_d16_and_d45():
    """D-13. The book prints Ar/Sg/Le here and Ar/Le/Sg for D-16 and D-45.
    Using one for the other misplaces 67% of longitudes, so the difference is
    asserted rather than left to a reader's memory."""
    assert list(D8_START.values()) == ["Ar", "Sg", "Le"]
    assert list(D8_START.values()) != ["Ar", "Le", "Sg"]


def test_6_2_8_the_eight_parts_are_three_degrees_forty_five():
    """"Each rasi is divided into 8 equal parts of 3d 45' each."""
    assert 30.0 / 8 == 3.75
    assert 3.75 == 3 + 45 / 60
    for part in range(8):
        assert d8_ashtamsa(part * 3.75).amsa_index == part


#: Example 15: "Mercury is at 10d in Ge and Jupiter is at 19d in Sc."
EXAMPLE_15 = [
    ("Mercury", "Ge", 10, 3, "dwiswabhava", "Le", "Li"),
    ("Jupiter", "Sc", 19, 6, "sthira", "Sg", "Ta"),
]


@pytest.mark.parametrize("who,rasi,degrees,part,modality,start,expected", EXAMPLE_15)
def test_example_15_ashtamsa(who, rasi, degrees, part, modality, start, expected):
    """"Because Ge is a dual rasi, counting starts from Le. The 3rd from Le is
    Li... Sc is a fixed sign and counting starts from Sg. The 6th from Sg is
    Ta."""
    index = list(RASI_ABBR).index(rasi)
    assert MODALITY_NAMES[RASI_MODALITY[index]] == modality
    got = d8_ashtamsa(index * 30 + degrees)
    assert got.amsa_index == part - 1
    assert readable_sign(got.sign) == expected
    start_index = list(RASI_ABBR).index(start)
    assert got.sign == (start_index + part - 1) % 12


def test_example_15_summary_contradicts_its_own_working():
    """The example's working gives Mercury **Li**; its closing sentence says
    "So Mercury is in **Le**".

    Le is the *starting* sign for dual rasis, not the destination — the
    summary repeats the start where it means the result. The rule and the
    working agree, so this is a summary slip, not a rule conflict, and needs
    no PVR entry. See D-13.
    """
    ge = list(RASI_ABBR).index("Ge")
    got = d8_ashtamsa(ge * 30 + 10)
    assert readable_sign(got.sign) == "Li", "the working"
    assert readable_sign(got.sign) != "Le", "the closing sentence"
    # Le really is where the count starts for a dual rasi.
    assert readable_sign(d8_ashtamsa(ge * 30 + 0.5).sign) == "Le"
    # Jupiter's half is consistent throughout.
    sc = list(RASI_ABBR).index("Sc")
    assert readable_sign(d8_ashtamsa(sc * 30 + 19).sign) == "Ta"


# --------------------------------------------------------------------------
# 6.2.9 Navamsa (D-9) and Example 16
# --------------------------------------------------------------------------

#: §6.2.9: "starting from Ar, Cp, Li or Cn, based on whether the rasi is a
#: fiery, earthy, airy or watery sign."
D9_START = {"fire": "Ar", "earth": "Cp", "air": "Li", "water": "Cn"}


@pytest.mark.parametrize("element,start", list(D9_START.items()))
def test_6_2_9_the_start_sign_by_element(element, start):
    index = ELEMENT_NAMES.index(element)
    expected = list(RASI_ABBR).index(start)
    for rasi in range(12):
        if RASI_ELEMENT[rasi] != index:
            continue
        for part in range(9):
            got = d9_navamsa(rasi * 30 + part * (30 / 9) + 0.5).sign
            assert got == (expected + part) % 12, (RASI_ABBR[rasi], part)


def test_6_2_9_the_nine_parts_are_three_degrees_twenty():
    """"Each rasi is divided into 9 equal parts of 3d 20' each."""
    assert 30.0 / 9 == pytest.approx(3 + 20 / 60)
    assert part_size_degrees(9) == pytest.approx(30.0 / 9)


def test_6_2_9_the_start_signs_are_the_movable_ones():
    """Ar, Cp, Li, Cn are the four chara rasis. So a navamsa count always
    begins at a movable sign — which is what makes the D-9 of a movable rasi
    begin at itself."""
    chara = MODALITY_NAMES.index("chara")
    for start in D9_START.values():
        assert RASI_MODALITY[list(RASI_ABBR).index(start)] == chara


def test_6_2_9_the_other_names():
    """"This chart is also known as Dharmamsa... some astrologers simply refer
    to it as "Amsa" (division)."""
    aliases = [a.lower() for a in VARGA_RULES["D9"]["aliases"]]
    assert "dharmamsa" in aliases


#: Example 16: "Mercury is at 11d in Ge and Jupiter is at 19d in Sc."
EXAMPLE_16 = [
    ("Mercury", "Ge", 11, 4, "air", "Li", "Cp"),
    ("Jupiter", "Sc", 19, 6, "water", "Cn", "Sg"),
]


@pytest.mark.parametrize("who,rasi,degrees,part,element,start,expected", EXAMPLE_16)
def test_example_16_navamsa(who, rasi, degrees, part, element, start, expected):
    """"Because Ge is an airy rasi, counting starts from Li. The 4th from Li
    is Cp... Sc is a watery sign and counting starts from Cn. The 6th from Cn
    is Sg."""
    index = list(RASI_ABBR).index(rasi)
    assert ELEMENT_NAMES[RASI_ELEMENT[index]] == element
    got = d9_navamsa(index * 30 + degrees)
    assert got.amsa_index == part - 1
    assert readable_sign(got.sign) == expected
    start_index = list(RASI_ABBR).index(start)
    assert got.sign == (start_index + part - 1) % 12


# --------------------------------------------------------------------------
# 6.2.10 Dasamsa (D-10) and Example 17
# --------------------------------------------------------------------------


def test_6_2_10_odd_rasis_start_at_themselves_and_even_at_the_ninth():
    """"Bodies in the 10 parts of a rasi go into the 10 rasis starting from
    the rasi itself or the 9th from it, based on whether the rasi is an odd or
    even sign."""
    for rasi in range(12):
        start = rasi if RASI_IS_ODD[rasi] else (rasi + 8) % 12
        for part in range(10):
            got = d10_dasamsa(rasi * 30 + part * 3.0 + 0.5).sign
            assert got == (start + part) % 12, (RASI_ABBR[rasi], part)


def test_6_2_10_the_ten_parts_are_three_degrees():
    """"Each rasi is divided into 10 equal parts of 3d each."""
    assert 30.0 / 10 == 3.0
    for part in range(10):
        assert d10_dasamsa(part * 3.0).amsa_index == part


def test_6_2_10_the_three_other_names():
    """"This chart is also known as Dasamaamsa or Karmamsa or Swargamsa."""
    aliases = [a.lower() for a in VARGA_RULES["D10"]["aliases"]]
    for name in ("dasamaamsa", "karmamsa", "swargamsa"):
        assert name in aliases


#: Example 17: "Mercury is at 10d in Ge and Jupiter is at 19d in Sc."
EXAMPLE_17 = [
    ("Mercury", "Ge", 10, 4, "Ge", "Vi"),
    ("Jupiter", "Sc", 19, 7, "Cn", "Cp"),
]


@pytest.mark.parametrize("who,rasi,degrees,part,start,expected", EXAMPLE_17)
def test_example_17_dasamsa(who, rasi, degrees, part, start, expected):
    """"Because Ge is an odd rasi, counting starts from Ge itself. The 4th
    from Ge is Vi... Sc is an even sign and counting starts from the 9th from
    it, i.e. Cn. The 7th from Cn is Cp."""
    index = list(RASI_ABBR).index(rasi)
    got = d10_dasamsa(index * 30 + degrees)
    assert got.amsa_index == part - 1
    assert readable_sign(got.sign) == expected
    start_index = list(RASI_ABBR).index(start)
    assert got.sign == (start_index + part - 1) % 12
    # The book names the start for Scorpio as the 9th from it.
    if not RASI_IS_ODD[index]:
        assert start_index == (index + 8) % 12


# --------------------------------------------------------------------------
# 6.2.11 Rudramsa (D-11) and Example 18
# --------------------------------------------------------------------------


def test_6_2_11_the_start_is_the_rasi_reflected_about_aries():
    """"Count rasis from Ar to the rasi being divided, in the zodiacal order.
    Count the same number of rasis anti-zodiacally from Ar."

    Gemini is the 3rd from Aries; the 3rd from Aries counted backwards is
    Aquarius. That is a reflection about Aries, i.e. -rasi mod 12. D-14 was
    getting this wrong.
    """
    for rasi in range(12):
        start = (-rasi) % 12
        for part in range(11):
            got = d11_rudramsa(rasi * 30 + part * (30 / 11) + 0.5).sign
            assert got == (start + part) % 12, (RASI_ABBR[rasi], part)


def test_6_2_11_the_two_reflections_the_book_works():
    """"In the case of Ge, it is the 3rd rasi from Ar. The 3rd rasi from Ar in
    the reverse order is Aq... In the case of Sc, it is the 8th rasi from Ar.
    Counting the 8th rasi from Ar in the reverse order, we get Vi."""
    abbr = list(RASI_ABBR)
    assert (-abbr.index("Ge")) % 12 == abbr.index("Aq")
    assert (-abbr.index("Sc")) % 12 == abbr.index("Vi")


def test_6_2_11_aries_reflects_to_itself():
    """The one fixed point of the reflection — worth pinning because an
    off-by-one would move it to Pisces or Taurus."""
    assert (-0) % 12 == 0
    assert d11_rudramsa(0.5).sign == 0


def test_6_2_11_the_eleven_parts_are_two_degrees_forty_three():
    """"Each rasi is divided into 11 equal parts of 2d 43' 38" each."""
    part = 30.0 / 11
    assert part == pytest.approx(2 + 43 / 60 + 38 / 3600, abs=1e-4)
    assert part_size_degrees(11) == pytest.approx(part)


def test_6_2_11_the_other_name():
    """"This chart is also known as Ekadasamsa."""
    assert "ekadasamsa" in [a.lower() for a in VARGA_RULES["D11"]["aliases"]]


#: Example 18: "Mercury is at 11d in Ge and Jupiter is at 19d in Sc."
EXAMPLE_18 = [
    ("Mercury", "Ge", 11, 5, "Aq", "Ge"),
    ("Jupiter", "Sc", 19, 7, "Vi", "Pi"),
]


@pytest.mark.parametrize("who,rasi,degrees,part,start,expected", EXAMPLE_18)
def test_example_18_rudramsa(who, rasi, degrees, part, start, expected):
    """"The 5th from Aq is Ge. So the 5th part in Ge goes into Ge in D-11...
    The 7th from Vi is Pi. So the 7th part of Sc goes into Pi in D-11."""
    index = list(RASI_ABBR).index(rasi)
    got = d11_rudramsa(index * 30 + degrees)
    assert got.amsa_index == part - 1
    assert readable_sign(got.sign) == expected
    start_index = list(RASI_ABBR).index(start)
    assert start_index == (-index) % 12, "the reflection"
    assert got.sign == (start_index + part - 1) % 12


def test_example_18_mercury_returns_to_its_own_rasi():
    """Mercury is in Gemini in D-1 and lands in Gemini again in D-11 — a
    coincidence of this longitude, not a property of D-11. Asserted so the
    example is not mistaken for an identity rule."""
    abbr = list(RASI_ABBR)
    ge = abbr.index("Ge")
    assert d11_rudramsa(ge * 30 + 11).sign == ge
    assert d11_rudramsa(ge * 30 + 1).sign != ge, "the first part does not"


# --------------------------------------------------------------------------
# The four together
# --------------------------------------------------------------------------


@pytest.mark.parametrize("code,divisions,fn", [
    ("D8", 8, d8_ashtamsa), ("D9", 9, d9_navamsa),
    ("D10", 10, d10_dasamsa), ("D11", 11, d11_rudramsa),
])
def test_each_of_these_charts_tiles_its_rasi(code, divisions, fn):
    seen = {fn(x / 100).amsa_index for x in range(36000)}
    assert seen == set(range(divisions)), code


# --------------------------------------------------------------------------
# 6.2.12 Dwadasamsa (D-12) and Example 19
# --------------------------------------------------------------------------


def test_6_2_12_counting_always_starts_from_the_rasi_itself():
    """"Bodies in the 12 parts of a rasi go into the 12 rasis starting from
    the rasi itself."

    The only chart in the chapter with no condition at all — no parity, no
    modality, no element.
    """
    for rasi in range(12):
        for part in range(12):
            got = d12_dwadasamsa(rasi * 30 + part * 2.5 + 0.1).sign
            assert got == (rasi + part) % 12, (RASI_ABBR[rasi], part)


def test_6_2_12_the_twelve_parts_are_two_and_a_half_degrees():
    """"Each rasi is divided into 12 equal parts of 2d 30' each."""
    assert 30.0 / 12 == 2.5 == 2 + 30 / 60


def test_6_2_12_every_rasi_is_reached_from_every_rasi():
    """Twelve parts into twelve signs starting from itself means a D-12 chart
    maps each rasi onto the whole zodiac exactly once."""
    for rasi in range(12):
        landed = [d12_dwadasamsa(rasi * 30 + p * 2.5 + 0.1).sign for p in range(12)]
        assert sorted(landed) == list(range(12))


#: Example 19: "Mercury is at 11d in Ge and Jupiter is at 19d in Sc."
EXAMPLE_19 = [
    ("Mercury", "Ge", 11, 5, "Ge", "Li"),
    ("Jupiter", "Sc", 19, 8, "Sc", "Ge"),
]


@pytest.mark.parametrize("who,rasi,degrees,part,start,expected", EXAMPLE_19)
def test_example_19_dwadasamsa(who, rasi, degrees, part, start, expected):
    """"The 5th from Ge is Li... The 8th from Sc is Ge."""
    index = list(RASI_ABBR).index(rasi)
    got = d12_dwadasamsa(index * 30 + degrees)
    assert got.amsa_index == part - 1
    assert readable_sign(got.sign) == expected
    assert list(RASI_ABBR).index(start) == index, "the start is the rasi itself"


# --------------------------------------------------------------------------
# 6.2.13 Shodasamsa (D-16) and Example 20
# --------------------------------------------------------------------------

#: §6.2.13: "starting from Ar, Le and Sg, based on whether the rasi is
#: movable, fixed or dual." **Not** D-8's and D-20's Ar/Sg/Le.
D16_START = {"chara": "Ar", "sthira": "Le", "dwiswabhava": "Sg"}


@pytest.mark.parametrize("modality,start", list(D16_START.items()))
def test_6_2_13_the_start_sign_by_modality(modality, start):
    index = MODALITY_NAMES.index(modality)
    expected = list(RASI_ABBR).index(start)
    for rasi in range(12):
        if RASI_MODALITY[rasi] != index:
            continue
        for part in range(16):
            got = d16_shodasamsa(rasi * 30 + part * 1.875 + 0.1).sign
            assert got == (expected + part) % 12, (RASI_ABBR[rasi], part)


def test_6_2_13_states_the_wrap_rule_explicitly():
    """"After going over the 12 rasis from a rasi, we get the same rasi as the
    13th rasi. So the 13th, 14th, 15th and 16th rasis from a rasi are simply
    the 1st, 2nd, 3rd and 4th rasis."

    D-16 is the first chart with more than twelve parts, so this is where the
    book pauses to say the count wraps. It applies to D-20, D-24 and up.
    """
    for rasi in range(12):
        for part, equivalent in ((12, 0), (13, 1), (14, 2), (15, 3)):
            a = d16_shodasamsa(rasi * 30 + part * 1.875 + 0.1).sign
            b = d16_shodasamsa(rasi * 30 + equivalent * 1.875 + 0.1).sign
            assert a == b, (RASI_ABBR[rasi], part)


def test_6_2_13_the_sixteen_parts_are_one_degree_fifty_two_thirty():
    """"Each rasi is divided into 16 equal parts of 1d 52' 30" each."""
    assert 30.0 / 16 == 1.875
    assert 1.875 == 1 + 52 / 60 + 30 / 3600


def test_6_2_13_the_other_name():
    """"This chart is also known as Kalamsa."""
    assert "kalamsa" in [a.lower() for a in VARGA_RULES["D16"]["aliases"]]


#: Example 20: "Mercury is at 11d in Ge and Jupiter is at 19d in Sc."
EXAMPLE_20 = [
    ("Mercury", "Ge", 11, 6, "dwiswabhava", "Sg", "Ta"),
    ("Jupiter", "Sc", 19, 11, "sthira", "Le", "Ge"),
]


@pytest.mark.parametrize("who,rasi,degrees,part,modality,start,expected", EXAMPLE_20)
def test_example_20_shodasamsa(who, rasi, degrees, part, modality, start, expected):
    """"Ge is a dual rasi and we start counting from Sg. The 6th from Sg is
    Ta... Sc is a fixed sign and we start counting from Le. The 11th from Le
    is Ge."""
    index = list(RASI_ABBR).index(rasi)
    assert MODALITY_NAMES[RASI_MODALITY[index]] == modality
    got = d16_shodasamsa(index * 30 + degrees)
    assert got.amsa_index == part - 1
    assert readable_sign(got.sign) == expected
    start_index = list(RASI_ABBR).index(start)
    assert got.sign == (start_index + part - 1) % 12


# --------------------------------------------------------------------------
# 6.2.14 Vimsamsa (D-20) and Example 21
# --------------------------------------------------------------------------

#: §6.2.14: "starting from Ar, Sg and Le" — the same order as D-8, and the
#: reverse of D-16's last two.
D20_START = {"chara": "Ar", "sthira": "Sg", "dwiswabhava": "Le"}


@pytest.mark.parametrize("modality,start", list(D20_START.items()))
def test_6_2_14_the_start_sign_by_modality(modality, start):
    index = MODALITY_NAMES.index(modality)
    expected = list(RASI_ABBR).index(start)
    for rasi in range(12):
        if RASI_MODALITY[rasi] != index:
            continue
        for part in range(20):
            got = d20_vimsamsa(rasi * 30 + part * 1.5 + 0.1).sign
            assert got == (expected + part) % 12, (RASI_ABBR[rasi], part)


def test_the_three_modality_charts_do_not_share_one_order():
    """**The trap that caused D-13.** Three charts key off modality and they
    do not agree:

        D-8   Ar, Sg, Le
        D-16  Ar, Le, Sg
        D-20  Ar, Sg, Le

    D-16 is the odd one. Using its order for D-8 misplaced 67% of longitudes.
    Asserted here so the difference is a test failure, not a memory test.
    """
    assert list(D8_START.values()) == ["Ar", "Sg", "Le"]
    assert list(D20_START.values()) == ["Ar", "Sg", "Le"]
    assert list(D16_START.values()) == ["Ar", "Le", "Sg"]
    assert D8_START == D20_START
    assert D16_START != D8_START
    # The movable start is the one thing all three share.
    assert D8_START["chara"] == D16_START["chara"] == D20_START["chara"] == "Ar"


def test_6_2_14_the_twenty_parts_are_one_and_a_half_degrees():
    """"Each rasi is divided into 20 equal parts of 1d 30' each."""
    assert 30.0 / 20 == 1.5 == 1 + 30 / 60


#: Example 21: "Mercury is at 11d in Ge and Jupiter is at 19d in Sc."
EXAMPLE_21 = [
    ("Mercury", "Ge", 11, 8, "dwiswabhava", "Le", "Pi"),
    ("Jupiter", "Sc", 19, 13, "sthira", "Sg", "Sg"),
]


@pytest.mark.parametrize("who,rasi,degrees,part,modality,start,expected", EXAMPLE_21)
def test_example_21_vimsamsa(who, rasi, degrees, part, modality, start, expected):
    """"Because Ge is a dual rasi, we start counting from Le. The 8th from Le
    is Pi... Sc is a fixed sign and the counting starts from Sg. The 13th from
    Sg is Sg itself (13th = 1st, after removing 12)."""
    index = list(RASI_ABBR).index(rasi)
    assert MODALITY_NAMES[RASI_MODALITY[index]] == modality
    got = d20_vimsamsa(index * 30 + degrees)
    assert got.amsa_index == part - 1
    assert readable_sign(got.sign) == expected
    start_index = list(RASI_ABBR).index(start)
    assert got.sign == (start_index + part - 1) % 12


def test_example_21_jupiter_lands_on_its_own_start_sign():
    """"The 13th from Sg is Sg itself (13th = 1st, after removing 12)." The
    book's own worked instance of §6.2.13's wrap rule."""
    sc = list(RASI_ABBR).index("Sc")
    got = d20_vimsamsa(sc * 30 + 19)
    assert readable_sign(got.sign) == "Sg" == D20_START["sthira"]
    assert got.amsa_index == 12, "the 13th part, 0-based"
    assert (13 - 1) % 12 == 0, "which is the 1st after removing 12"


# --------------------------------------------------------------------------
# 6.2.15 Chaturvimsamsa (D-24) and Example 22
# --------------------------------------------------------------------------


def test_6_2_15_odd_rasis_start_at_leo_and_even_at_cancer():
    """"Bodies in the 24 parts of a rasi go into the 24 rasis starting from Le
    or Cn, based on whether the rasi is odd or even."

    Absolute starts, like D-5 and D-6 — not counted from the natal rasi.
    """
    abbr = list(RASI_ABBR)
    for rasi in range(12):
        start = abbr.index("Le") if RASI_IS_ODD[rasi] else abbr.index("Cn")
        for part in range(24):
            got = d24_chaturvimsamsa(rasi * 30 + part * 1.25 + 0.1).sign
            assert got == (start + part) % 12, (RASI_ABBR[rasi], part)


def test_6_2_15_the_twenty_four_parts_are_one_degree_fifteen():
    """"Each rasi is divided into 24 equal parts of 1d 15' each."""
    assert 30.0 / 24 == 1.25 == 1 + 15 / 60


def test_6_2_15_the_other_name():
    """"This chart is also called Siddhamsa."""
    assert "siddhamsa" in [a.lower() for a in VARGA_RULES["D24"]["aliases"]]


def test_6_2_15_twenty_four_parts_cover_the_zodiac_twice():
    """Two full circuits, so every sign is reached exactly twice from any
    rasi — the strongest case of §6.2.13's wrap rule in the chapter so far."""
    for rasi in range(12):
        landed = [
            d24_chaturvimsamsa(rasi * 30 + p * 1.25 + 0.1).sign for p in range(24)
        ]
        assert sorted(landed) == sorted(list(range(12)) * 2)


#: Example 22: "Mercury is at 11d in Ge and Jupiter is at 19d in Sc."
EXAMPLE_22 = [
    ("Mercury", "Ge", 11, 9, "Le", "Ar"),
    ("Jupiter", "Sc", 19, 16, "Cn", "Li"),
]


@pytest.mark.parametrize("who,rasi,degrees,part,start,expected", EXAMPLE_22)
def test_example_22_chaturvimsamsa(who, rasi, degrees, part, start, expected):
    """"Ge is an odd rasi and counting starts from Le. The 9th from Le is
    Ar... Sc is an even rasi and counting starts from Cn. The 16th from Cn is
    Li (16th = 4th, after removing 12)."""
    index = list(RASI_ABBR).index(rasi)
    got = d24_chaturvimsamsa(index * 30 + degrees)
    assert got.amsa_index == part - 1
    assert readable_sign(got.sign) == expected
    start_index = list(RASI_ABBR).index(start)
    assert got.sign == (start_index + part - 1) % 12


def test_example_22_jupiter_needs_the_wrap_rule_too():
    """"The 16th from Cn is Li (16th = 4th, after removing 12)."""
    assert (16 - 1) % 12 == 3, "the 4th, 0-based"
    abbr = list(RASI_ABBR)
    assert (abbr.index("Cn") + 3) % 12 == abbr.index("Li")


# --------------------------------------------------------------------------
# Footnote 11 and the four together
# --------------------------------------------------------------------------


def test_footnote_11_the_two_counting_orders():
    """"The zodiacal order is: Ar, Ta, Ge, Cn, Le, ... The anti-zodiacal order
    is: Ar, Pi, Aq, Cp, Sg, ..."

    Attached to D-11, the only chart that counts backwards. Aries opens both.
    """
    abbr = list(RASI_ABBR)
    assert [abbr[i % 12] for i in range(5)] == ["Ar", "Ta", "Ge", "Cn", "Le"]
    assert [abbr[(-i) % 12] for i in range(5)] == ["Ar", "Pi", "Aq", "Cp", "Sg"]


@pytest.mark.parametrize("code,divisions,fn", [
    ("D12", 12, d12_dwadasamsa), ("D16", 16, d16_shodasamsa),
    ("D20", 20, d20_vimsamsa), ("D24", 24, d24_chaturvimsamsa),
])
def test_the_later_charts_tile_their_rasi(code, divisions, fn):
    seen = {fn(x / 100).amsa_index for x in range(36000)}
    assert seen == set(range(divisions)), code


@pytest.mark.parametrize("code,rasi,degrees,expected", [
    ("D12", "Ge", 11, "Li"), ("D16", "Ge", 11, "Ta"),
    ("D20", "Ge", 11, "Pi"), ("D24", "Ge", 11, "Ar"),
])
def test_examples_19_to_22_through_the_endpoint(client, code, rasi, degrees, expected):
    """One longitude, four charts, four different signs — and the response
    carries the rule it used, so a caller can see why."""
    body = client.post(
        "/v1/varga/compute",
        json={"longitude": f"{degrees} {rasi} 0", "charts": [code]},
    ).json()
    chart = body["charts"][0]
    assert chart["chart"] == code
    assert readable_sign(chart["rasi"]) == expected
    assert chart["counts_from"], "the response explains its own rule"
    assert chart["part_index"] >= 1, "1-based, as the book numbers parts"


# --------------------------------------------------------------------------
# 6.2.16 Nakshatramsa (D-27) and Example 23
# --------------------------------------------------------------------------

#: §6.2.16: "starting from Ar, Cn, Li and Cp based on whether the rasi is a
#: fiery, earthy, airy or watery rasi." **Earth and water are swapped**
#: relative to D-9's Ar/Cp/Li/Cn.
D27_START = {"fire": "Ar", "earth": "Cn", "air": "Li", "water": "Cp"}


@pytest.mark.parametrize("element,start", list(D27_START.items()))
def test_6_2_16_the_start_sign_by_element(element, start):
    index = ELEMENT_NAMES.index(element)
    expected = list(RASI_ABBR).index(start)
    part_size = 30.0 / 27
    for rasi in range(12):
        if RASI_ELEMENT[rasi] != index:
            continue
        for part in range(27):
            got = d27_nakshatramsa(rasi * 30 + part * part_size + 0.05).sign
            assert got == (expected + part) % 12, (RASI_ABBR[rasi], part)


def test_d9_and_d27_swap_earth_and_water():
    """**The second trap of D-13's kind.** Both charts key off element and
    they do not agree:

        D-9   fire Ar, earth **Cp**, air Li, water **Cn**
        D-27  fire Ar, earth **Cn**, air Li, water **Cp**

    Fire and air are shared; earth and water are exchanged. Sharing one table
    between them would be right for half the zodiac and wrong for the other
    half — the shape that hid D-13 for so long.
    """
    assert D9_START["fire"] == D27_START["fire"] == "Ar"
    assert D9_START["air"] == D27_START["air"] == "Li"
    assert D9_START["earth"] == "Cp" and D27_START["earth"] == "Cn"
    assert D9_START["water"] == "Cn" and D27_START["water"] == "Cp"
    assert D9_START["earth"] == D27_START["water"]
    assert D9_START["water"] == D27_START["earth"]


def test_6_2_16_the_twenty_seven_parts_are_one_degree_six_forty():
    """"Each rasi is divided into 27 equal parts of 1d 6' 40" each."""
    part = 30.0 / 27
    assert part == pytest.approx(1 + 6 / 60 + 40 / 3600, abs=1e-6)


def test_6_2_16_the_other_names():
    """"This chart is also called Saptavimsamsa or Bhamsa."""
    aliases = [a.lower() for a in VARGA_RULES["D27"]["aliases"]]
    for name in ("saptavimsamsa", "bhamsa"):
        assert name in aliases


def test_example_23_jupiter_reproduces():
    """"Sc is a watery sign and counting starts from Cp. The 18th from Cp is
    Ge (18th = 6th, after removing 12)." Jupiter's half is correct."""
    sc = list(RASI_ABBR).index("Sc")
    got = d27_nakshatramsa(sc * 30 + 19)
    assert got.amsa_index == 17, "the 18th part"
    assert readable_sign(got.sign) == "Ge"
    abbr = list(RASI_ABBR)
    assert (abbr.index("Cp") + 17) % 12 == abbr.index("Ge")


def test_example_23_mercury_is_pvr_7():
    """"Because Ge is an airy rasi, counting starts from Li. The 10th from Li
    is **Le**."

    Counting Libra as the first: Li, Sc, Sg, Cp, Aq, Pi, Ar, Ta, Ge, **Cn**.
    Leo is the *eleventh*. The rule and the start are both right in the
    example; only the count is off by one. We follow the rule — D-27 for 11
    degrees Gemini is **Cancer**. PVR-7 / D-15.
    """
    ge = list(RASI_ABBR).index("Ge")
    got = d27_nakshatramsa(ge * 30 + 11)
    assert got.amsa_index == 9, "the 10th part, as the book says"
    assert readable_sign(got.sign) == "Cn", "the rule"
    assert readable_sign(got.sign) != "Le", "what the example prints"

    abbr = list(RASI_ABBR)
    chain = [abbr[(abbr.index("Li") + i) % 12] for i in range(11)]
    assert chain[9] == "Cn", "the 10th from Libra"
    assert chain[10] == "Le", "Leo is the 11th"


# --------------------------------------------------------------------------
# 6.2.17 Trimsamsa (D-30) — the one chart with unequal parts
# --------------------------------------------------------------------------

#: §6.2.17's two tables. Note the boundaries differ by parity: 5/10/18/25 for
#: odd and 5/12/20/25 for even.
D30_ODD = [(0, 5, "Ar"), (5, 10, "Aq"), (10, 18, "Sg"), (18, 25, "Ge"), (25, 30, "Li")]
D30_EVEN = [(0, 5, "Ta"), (5, 12, "Vi"), (12, 20, "Pi"), (20, 25, "Cp"), (25, 30, "Sc")]


@pytest.mark.parametrize("low,high,expected", D30_ODD)
def test_6_2_17_odd_rasi_bands(low, high, expected):
    """"Bodies in 0d-5d in odd rasis are placed in Ar in D-30." and the four
    that follow. Checked from every odd rasi, at both ends of each band."""
    for rasi in range(12):
        if not RASI_IS_ODD[rasi]:
            continue
        for degrees in (low + 0.01, high - 0.01):
            got = d30_trimsamsa(rasi * 30 + degrees)
            assert readable_sign(got.sign) == expected, (RASI_ABBR[rasi], degrees)


@pytest.mark.parametrize("low,high,expected", D30_EVEN)
def test_6_2_17_even_rasi_bands(low, high, expected):
    """"Bodies in 0d-5d in even rasis are placed in Ta in D-30." and the four
    that follow."""
    for rasi in range(12):
        if RASI_IS_ODD[rasi]:
            continue
        for degrees in (low + 0.01, high - 0.01):
            got = d30_trimsamsa(rasi * 30 + degrees)
            assert readable_sign(got.sign) == expected, (RASI_ABBR[rasi], degrees)


def test_6_2_17_is_the_only_chart_with_unequal_parts():
    """Every other varga in the chapter divides a rasi into n equal parts.
    D-30 has five bands of 5, 5, 8, 7 and 5 degrees — so 30/30 is **not** its
    part size and a generic equal-division helper would be wrong.
    """
    odd_spans = [high - low for low, high, _ in D30_ODD]
    assert odd_spans == [5, 5, 8, 7, 5]
    assert sum(odd_spans) == 30
    assert len(set(odd_spans)) > 1, "not equal parts"
    assert 30.0 / 30 == 1.0, "which the name would suggest, and is not used"


def test_6_2_17_the_even_bands_are_the_odd_bands_reversed():
    """5, 5, 8, 7, 5 read backwards is 5, 7, 8, 5, 5 — the even spans exactly.
    Not stated in the book; it falls out of the two tables and is the cheapest
    check that neither was mistyped.
    """
    odd_spans = [high - low for low, high, _ in D30_ODD]
    even_spans = [high - low for low, high, _ in D30_EVEN]
    assert even_spans == list(reversed(odd_spans))


def test_6_2_17_only_ten_signs_are_ever_reached():
    """Five destinations per parity, ten in all — Cancer and Leo appear in
    neither table. D-30 is the only chart that leaves signs unreachable."""
    reached = {s for _, _, s in D30_ODD} | {s for _, _, s in D30_EVEN}
    assert len(reached) == 10
    assert reached & {"Cn", "Le"} == set()
    swept = {readable_sign(d30_trimsamsa(x / 10).sign) for x in range(3600)}
    assert swept == reached


def test_6_2_17_has_no_worked_example():
    """Like D-5, D-30 is given no example — and it is the most irregular rule
    in the chapter. The two facts together are why it is worth sweeping."""
    assert VARGA_RULES["D30"]["example"] is False


# --------------------------------------------------------------------------
# 6.2.18 Khavedamsa (D-40) and Example 24
# --------------------------------------------------------------------------


def test_6_2_18_odd_rasis_start_at_aries_and_even_at_libra():
    """"Bodies in the 40 parts of a rasi go into the 40 rasis starting from Ar
    or Li, based on whether the rasi is odd or even."

    The same pair D-6 uses, and absolute rather than counted from the rasi.
    """
    abbr = list(RASI_ABBR)
    for rasi in range(12):
        start = abbr.index("Ar") if RASI_IS_ODD[rasi] else abbr.index("Li")
        for part in range(40):
            got = d40_khavedamsa(rasi * 30 + part * 0.75 + 0.01).sign
            assert got == (start + part) % 12, (RASI_ABBR[rasi], part)


def test_6_2_18_the_forty_parts_are_forty_five_arcminutes():
    """"Each rasi is divided into 40 equal parts of 45' each."""
    assert 30.0 / 40 == 0.75 == 45 / 60


def test_6_2_18_the_other_name():
    """"This chart is also called Chatvarimsamsa."""
    assert "chatvarimsamsa" in [a.lower() for a in VARGA_RULES["D40"]["aliases"]]


#: Example 24: "Mercury is at 11d in Ge and Jupiter is at 19d in Sc."
EXAMPLE_24 = [
    ("Mercury", "Ge", 11, 15, "Ar", "Ge"),
    ("Jupiter", "Sc", 19, 26, "Li", "Sc"),
]


@pytest.mark.parametrize("who,rasi,degrees,part,start,expected", EXAMPLE_24)
def test_example_24_khavedamsa(who, rasi, degrees, part, start, expected):
    """"The 15th from Ar is Ge (15th = 3rd, after removing 12)... The 26th
    from Li is Sc (26th = 2nd, after removing multiples of 12)."""
    index = list(RASI_ABBR).index(rasi)
    got = d40_khavedamsa(index * 30 + degrees)
    assert got.amsa_index == part - 1
    assert readable_sign(got.sign) == expected
    start_index = list(RASI_ABBR).index(start)
    assert got.sign == (start_index + part - 1) % 12


def test_example_24_needs_twelve_removed_twice_for_jupiter():
    """"26th = 2nd, after removing **multiples** of 12" — the book's own note
    that one subtraction is not always enough."""
    assert (26 - 1) % 12 == 1, "the 2nd, 0-based"
    assert 26 - 12 == 14, "still over twelve"
    assert 26 - 24 == 2


def test_example_24_both_bodies_land_in_their_own_rasi():
    """A coincidence of these two longitudes, not a property of D-40 —
    asserted so the example is not mistaken for an identity rule."""
    abbr = list(RASI_ABBR)
    for _, rasi, degrees, _, _, expected in EXAMPLE_24:
        assert rasi == expected
        assert d40_khavedamsa(abbr.index(rasi) * 30 + degrees).sign == abbr.index(rasi)
    # And the neighbouring part does not.
    ge = abbr.index("Ge")
    assert d40_khavedamsa(ge * 30 + 11.8).sign != ge


# --------------------------------------------------------------------------
# 6.2.19 Akshavedamsa (D-45) and Example 25
# --------------------------------------------------------------------------

#: §6.2.19: "starting from Ar, Le or Sg" — D-16's order, not D-8's.
D45_START = {"chara": "Ar", "sthira": "Le", "dwiswabhava": "Sg"}


@pytest.mark.parametrize("modality,start", list(D45_START.items()))
def test_6_2_19_the_start_sign_by_modality(modality, start):
    index = MODALITY_NAMES.index(modality)
    expected = list(RASI_ABBR).index(start)
    part_size = 30.0 / 45
    for rasi in range(12):
        if RASI_MODALITY[rasi] != index:
            continue
        for part in range(45):
            got = d45_akshavedamsa(rasi * 30 + part * part_size + 0.01).sign
            assert got == (expected + part) % 12, (RASI_ABBR[rasi], part)


def test_the_four_modality_charts_split_two_and_two():
    """Completing the picture. Four charts key off modality:

        D-8   Ar, Sg, Le
        D-16  Ar, Le, Sg
        D-20  Ar, Sg, Le
        D-45  Ar, Le, Sg

    Two orders, two charts each — D-8 with D-20, D-16 with D-45. Every one of
    them starts movable at Aries, which is what makes the other two columns
    easy to transpose. That transposition was D-13.
    """
    assert D8_START == D20_START
    assert D16_START == D45_START
    assert D8_START != D16_START
    assert all(
        s["chara"] == "Ar" for s in (D8_START, D16_START, D20_START, D45_START)
    )


def test_6_2_19_the_forty_five_parts_are_forty_arcminutes():
    """"Each rasi is divided into 45 equal parts of 40' each."""
    assert 30.0 / 45 == pytest.approx(40 / 60)


def test_6_2_19_the_other_name():
    """"This chart is also called Pancha-chatvarimsamsa."""
    aliases = [a.lower().replace("-", "") for a in VARGA_RULES["D45"]["aliases"]]
    assert "panchachatvarimsamsa" in aliases


#: Example 25: "Mercury is at 11d in Ge and Jupiter is at 19d in Sc."
EXAMPLE_25 = [
    ("Mercury", "Ge", 11, 17, "dwiswabhava", "Sg", "Ar"),
    ("Jupiter", "Sc", 19, 29, "sthira", "Le", "Sg"),
]


@pytest.mark.parametrize("who,rasi,degrees,part,modality,start,expected", EXAMPLE_25)
def test_example_25_akshavedamsa(who, rasi, degrees, part, modality, start, expected):
    """"Because Ge is a dual rasi, we start counting from Sg. The 17th from Sg
    is Ar (17th = 5th, after removing 12)... Sc is a fixed rasi and counting
    starts from Le. The 29th from Le is Sg."""
    index = list(RASI_ABBR).index(rasi)
    assert MODALITY_NAMES[RASI_MODALITY[index]] == modality
    got = d45_akshavedamsa(index * 30 + degrees)
    assert got.amsa_index == part - 1
    assert readable_sign(got.sign) == expected
    start_index = list(RASI_ABBR).index(start)
    assert got.sign == (start_index + part - 1) % 12


def test_example_25_jupiter_needs_twelve_removed_twice():
    """The 29th is the 5th after two circuits — the book states the reduction
    for Mercury's 17th but not for Jupiter's 29th."""
    assert (29 - 1) % 12 == 4, "the 5th, 0-based"
    assert 29 - 24 == 5


# --------------------------------------------------------------------------
# The last four, and the chapter's charts as a whole
# --------------------------------------------------------------------------


@pytest.mark.parametrize("code,divisions,fn", [
    ("D27", 27, d27_nakshatramsa), ("D40", 40, d40_khavedamsa),
    ("D45", 45, d45_akshavedamsa),
])
def test_the_last_equal_charts_tile_their_rasi(code, divisions, fn):
    seen = {fn(x / 100).amsa_index for x in range(36000)}
    assert seen == set(range(divisions)), code


@pytest.mark.parametrize("code,rasi,degrees,expected", [
    ("D27", "Ge", 11, "Cn"), ("D30", "Ge", 11, "Sg"),
    ("D40", "Ge", 11, "Ge"), ("D45", "Ge", 11, "Ar"),
])
def test_examples_23_to_25_through_the_endpoint(client, code, rasi, degrees, expected):
    body = client.post(
        "/v1/varga/compute",
        json={"longitude": f"{degrees} {rasi} 0", "charts": [code]},
    ).json()
    chart = body["charts"][0]
    assert chart["chart"] == code
    assert readable_sign(chart["rasi"]) == expected
    assert chart["counts_from"]


# --------------------------------------------------------------------------
# 6.2.20 Shashtyamsa (D-60) and Example 26
# --------------------------------------------------------------------------


def test_6_2_20_counting_starts_from_the_rasi_itself():
    """"Bodies in the 60 parts of a rasi go into the 60 rasis starting the
    rasi itself."

    Like D-12, no condition at all — no parity, modality or element.
    """
    for rasi in range(12):
        for part in range(60):
            got = d60_shashtyamsa(rasi * 30 + part * 0.5 + 0.01).sign
            assert got == (rasi + part) % 12, (RASI_ABBR[rasi], part)


def test_6_2_20_the_sixty_parts_are_thirty_arcminutes():
    """"Each rasi is divided into 60 equal parts of 30' each."""
    assert 30.0 / 60 == 0.5 == 30 / 60


def test_6_2_20_sixty_parts_cover_the_zodiac_five_times():
    """The most circuits of any chart in the chapter — every sign is reached
    exactly five times from any rasi."""
    for rasi in range(12):
        landed = [d60_shashtyamsa(rasi * 30 + p * 0.5 + 0.01).sign for p in range(60)]
        assert sorted(landed) == sorted(list(range(12)) * 5)


def test_6_2_20_the_shortcut_for_the_part_index():
    """"To see the part occupied by a body, we can take its longitude from the
    beginning of the occupied rasi, multiply it by 2, take degrees and ignore
    minutes, add 1 to it."

    A shortcut, not a second rule: doubling and truncating is dividing by the
    0.5-degree part size. Asserted across a whole rasi so the two can never
    disagree — including at exact part boundaries, where truncation is the
    place an off-by-one would appear.
    """
    for tenth in range(300):
        within = tenth / 10
        shortcut = int(within * 2) + 1
        computed = d60_shashtyamsa(within).amsa_index + 1
        assert shortcut == computed, within
    for part in range(60):
        boundary = part * 0.5
        assert int(boundary * 2) + 1 == d60_shashtyamsa(boundary).amsa_index + 1


def test_6_2_20_the_shortcut_is_the_part_size_in_disguise():
    """Multiplying by 2 works only because a part is 30 arcminutes. Stated so
    that a reader does not carry "multiply by 2" to another chart."""
    assert 1 / (30.0 / 60) == 2.0
    assert 1 / (30.0 / 30) != 2.0, "D-30's parts are not 30 arcminutes"


#: Example 26: "Jupiter is at 222d 58', i.e. 12d 58' in Scorpio."
EXAMPLE_26_LONGITUDE = 222 + 58 / 60


def test_example_26_the_longitude_within_the_rasi():
    """"Jupiter is at 222d 58', i.e. 12d 58' in Scorpio." Scorpio is the 8th
    rasi, so seven whole rasis precede it."""
    assert EXAMPLE_26_LONGITUDE % 30 == pytest.approx(12 + 58 / 60)
    assert int(EXAMPLE_26_LONGITUDE // 30) == list(RASI_ABBR).index("Sc")
    assert 7 * 30 + 12 + 58 / 60 == pytest.approx(EXAMPLE_26_LONGITUDE)


def test_example_26_the_shortcut_step_by_step():
    """"Multiplying 12d 58' by 2, we get 25d 56'. Taking degrees and ignoring
    minutes, we get 25. Adding 1, we get 26."

    The truncation matters: 25d56' is nearly 26, and rounding rather than
    truncating would give the 27th part and the wrong sign.
    """
    within = EXAMPLE_26_LONGITUDE % 30
    doubled = within * 2
    assert doubled == pytest.approx(25 + 56 / 60)
    assert int(doubled) == 25, "ignore minutes"
    assert round(doubled) == 26, "rounding would give 26 here, then 27 after +1"
    assert int(doubled) + 1 == 26, "the 26th part"


def test_example_26_counts_the_twenty_sixth_rasi_from_scorpio():
    """"So we have to count the 26th rasi from Sc. Removing multiples of 12
    from 26, we get 2. The 2nd rasi from Sc is Sg."""
    got = d60_shashtyamsa(EXAMPLE_26_LONGITUDE)
    assert got.amsa_index == 25, "the 26th part, 0-based"
    assert readable_sign(got.sign) == "Sg"
    abbr = list(RASI_ABBR)
    assert (26 - 1) % 12 == 1, "the 2nd, 0-based"
    assert (abbr.index("Sc") + 1) % 12 == abbr.index("Sg")


def test_example_26_needs_twelve_removed_twice():
    """"Removing **multiples** of 12 from 26" — 26 - 12 is still over twelve."""
    assert 26 - 12 == 14
    assert 26 - 24 == 2


def test_example_26_through_the_endpoint(client):
    body = client.post(
        "/v1/varga/compute",
        json={"longitude": EXAMPLE_26_LONGITUDE, "charts": ["D60"]},
    ).json()
    chart = body["charts"][0]
    assert chart["chart"] == "D60"
    assert chart["part_index"] == 26
    assert chart["rasi_name"] == "Sagittarius"
    assert chart["part_size_degrees"] == 0.5
    assert body["input"]["rasi_dm"].endswith("Sc 58")


def test_d60_tiles_its_rasi():
    seen = {d60_shashtyamsa(x / 100).amsa_index for x in range(36000)}
    assert seen == set(range(60))


def test_d12_and_d60_are_the_two_unconditional_charts():
    """Of the twenty, only D-12 and D-60 count from the rasi itself with no
    condition. Every other chart keys off parity, modality or element — or, in
    D-30's case, has no counting at all."""
    unconditional = {"D12", "D60"}
    for code in unconditional:
        assert "the rasi itself" in VARGA_RULES[code]["counts_from"]
    for rasi in range(12):
        assert d12_dwadasamsa(rasi * 30 + 0.1).sign == rasi
        assert d60_shashtyamsa(rasi * 30 + 0.1).sign == rasi


# --------------------------------------------------------------------------
# 6.3 Table 11 — the significations
# --------------------------------------------------------------------------

#: Table 11 exactly as printed, all twenty rows.
TABLE_11 = [
    ("D1", "Rasi", "Existence at the physical level"),
    ("D2", "Hora", "Wealth and money"),
    ("D3", "Drekkana", "Everything related to brothers and sisters"),
    ("D4", "Chaturthamsa", "Residence, houses owned, properties and fortune"),
    ("D5", "Panchamsa", "Fame, authority and power"),
    ("D6", "Shashthamsa", "Health troubles"),
    ("D7", "Saptamsa", "Everything related to children (and grand-children)"),
    ("D8", "Ashtamsa", "Sudden and unexpected troubles, litigation etc"),
    ("D9", "Navamsa", (
        "Marriage and everything related to spouse(s), dharma (duty and "
        "righteousness), interaction with other people, basic skills, inner self"
    )),
    ("D10", "Dasamsa", "Career, activities and achievements in society"),
    ("D11", "Rudramsa", "Death and destruction"),
    ("D12", "Dwadasamsa", (
        "Everything related to parents (also uncles, aunts and grand-parents, "
        "i.e. blood-relatives of parents)"
    )),
    ("D16", "Shodasamsa", "Vehicles, pleasures, comforts and discomforts"),
    ("D20", "Vimsamsa", "Religious activities and spiritual matters"),
    ("D24", "Chaturvimsamsa", "Learning, knowledge and education"),
    ("D27", "Nakshatramsa", "Strengths and weaknesses, inherent nature"),
    ("D30", "Trimsamsa", "Evils and punishment, sub-conscious self, some diseases"),
    ("D40", "Khavedamsa", "Auspicious and inauspicious events"),
    ("D45", "Akshavedamsa", "All matters"),
    ("D60", "Shashtyamsa", "Karma of past life, all matters"),
]


@pytest.mark.parametrize("code,name,signifies", TABLE_11)
def test_table_11_row_by_row(code, name, signifies):
    """"Each divisional chart signifies a particular area of life and throws
    light on it." Transcribed, since none of it is derivable."""
    assert VARGA_SIGNIFICATIONS[code] == signifies


def test_table_11_covers_exactly_the_twenty_charts():
    assert [c for c, _, _ in TABLE_11] == list(VARGA_SIGNIFICATIONS)
    assert len(TABLE_11) == 20


@pytest.mark.parametrize("code,name,signifies", TABLE_11)
def test_table_11_names_match_the_section_headings(code, name, signifies):
    """The Divisional Chart column of Table 11 and the §6.2.x headings are the
    same names, so the two cannot drift."""
    assert VARGA_REGISTRY[code][1] == name


def test_two_charts_are_given_all_matters():
    """D-45 "All matters" and D-60 "Karma of past life, all matters" — the
    only two whose scope is not a single area. Worth naming: a caller cannot
    treat every varga as narrow."""
    broad = [c for c, _, s in TABLE_11 if "all matters" in s.lower()]
    assert broad == ["D45", "D60"]


def test_the_signification_of_d1_is_not_a_subject_but_a_level():
    """"Existence at the physical level" — D-1 is the whole of physical
    existence, not one area within it, which is why every other chart refines
    rather than competes with it."""
    assert VARGA_SIGNIFICATIONS["D1"] == "Existence at the physical level"


# --------------------------------------------------------------------------
# 6.4 The four planes
# --------------------------------------------------------------------------


def test_6_4_the_four_planes_and_their_division_ranges():
    """"Divisional charts based on divisions between 1 and 12 operate in the
    physical plane... between 13 and 24... the mental plane... between 25 and
    36... the plane of sub-consciousness... above 36... a kaarmic plane."
    """
    assert [p["plane"] for p in VARGA_PLANES] == [
        "physical", "mental", "sub-conscious", "kaarmic",
    ]
    assert [(p["low"], p["high"]) for p in VARGA_PLANES] == [
        (1, 12), (13, 24), (25, 36), (37, None),
    ]


def test_6_4_the_ranges_are_contiguous_and_do_not_overlap():
    """1-12, 13-24, 25-36, 37 up. Each band is twelve wide and the last is
    open — so every possible division belongs to exactly one plane."""
    bounded = [p for p in VARGA_PLANES if p["high"] is not None]
    for lower, upper in zip(bounded, VARGA_PLANES[1:]):
        assert lower["high"] + 1 == upper["low"]
    for p in bounded:
        assert p["high"] - p["low"] + 1 == 12


def test_6_4_the_plane_follows_from_the_number_of_divisions_alone():
    """§6.4 groups by **n**, not by subject. So D-11 (death) and D-12
    (parents) share a plane with D-1, while D-16 (vehicles) does not — the
    grouping cuts across the significations of Table 11."""

    def plane_of(divisions: int) -> str:
        for p in VARGA_PLANES:
            if p["low"] <= divisions and (p["high"] is None or divisions <= p["high"]):
                return str(p["plane"])
        raise AssertionError(divisions)

    assert plane_of(1) == plane_of(11) == plane_of(12) == "physical"
    assert plane_of(16) == plane_of(20) == plane_of(24) == "mental"
    assert plane_of(27) == plane_of(30) == "sub-conscious"
    assert plane_of(40) == plane_of(45) == plane_of(60) == "kaarmic"


def test_6_4_the_charts_the_book_names_in_each_plane():
    """The book names the members of the last three planes explicitly —
    "(i.e. D-16, D-20 and D-24)", "(i.e. D-27 and D-30)", "(i.e. D-40, D-45
    and D-60)". Checked against the twenty we implement."""

    def members(low, high):
        return [
            c for c in VARGA_SIGNIFICATIONS
            if low <= VARGA_REGISTRY[c][2] <= (high or 10**6)
        ]

    assert members(13, 24) == ["D16", "D20", "D24"]
    assert members(25, 36) == ["D27", "D30"]
    assert members(37, None) == ["D40", "D45", "D60"]
    assert len(members(1, 12)) == 12, "D-1 to D-12, all of them"


def test_6_4_the_physical_plane_holds_twelve_of_the_twenty():
    """Every division from 1 to 12 exists as a chart; the higher planes are
    sparse — three, two and three."""
    counts = []
    for p in VARGA_PLANES:
        counts.append(sum(
            1 for c in VARGA_SIGNIFICATIONS
            if p["low"] <= VARGA_REGISTRY[c][2]
            and (p["high"] is None or VARGA_REGISTRY[c][2] <= p["high"])
        ))
    assert counts == [12, 3, 2, 3]
    assert sum(counts) == 20


def test_6_4_the_kaarmic_plane_is_above_the_other_three():
    """"a kaarmic plane of existence that is **above** physical self, mind and
    sub-conscious self."

    A hierarchy, not a fourth peer — which is why D-45 and D-60 are the two
    charts Table 11 gives "all matters".
    """
    assert "above physical self" in KAARMIC_PLANE_IS_ABOVE
    kaarmic = [c for c in VARGA_SIGNIFICATIONS if VARGA_REGISTRY[c][2] >= 37]
    broad = [c for c, _, s in TABLE_11 if "all matters" in s.lower()]
    assert set(broad) <= set(kaarmic)


def test_6_4_the_planes_agree_with_table_11_where_the_book_says_so():
    """Two significations name their plane outright: D-30's "sub-conscious
    self" and D-60's "Karma of past life". Both land in the plane §6.4 puts
    them in, which is the cheapest check that the two sections agree.
    """
    assert "sub-conscious" in VARGA_SIGNIFICATIONS["D30"]
    assert 25 <= VARGA_REGISTRY["D30"][2] <= 36
    assert "Karma" in VARGA_SIGNIFICATIONS["D60"]
    assert VARGA_REGISTRY["D60"][2] >= 37


def test_the_rules_endpoint_publishes_the_significations_and_planes(client):
    body = client.get("/v1/varga/rules").json()
    charts = {c["chart"]: c for c in body["charts"]}
    for code, name, signifies in TABLE_11:
        assert charts[code]["name"] == name
        assert charts[code]["signifies"] == signifies


def test_three_served_charts_are_not_in_the_book(client):
    """`/v1/varga/rules` serves **23** charts. Chapter 6 defines twenty.

    D-81, D-108 and D-144 are composites — D-9 of D-9, D-12 of D-9, D-12 of
    D-12 — and PVR defines none of them. They have no Table 11 signification
    and no worked example. See OI-53.
    """
    body = client.get("/v1/varga/rules").json()
    served = {c["chart"] for c in body["charts"]}
    in_book = {c for c, _, _ in TABLE_11}
    assert len(in_book) == 20
    assert served - in_book == {"D81", "D108", "D144"}
    for code in ("D81", "D108", "D144"):
        assert code not in VARGA_SIGNIFICATIONS, "no Table 11 row"
        assert VARGA_RULES[code]["example"] is False


# --------------------------------------------------------------------------
# 6.5 Using Divisional Charts — the method, read matter-first
# --------------------------------------------------------------------------


def test_6_5_the_choice_is_driven_by_the_matter():
    """"We should choose the divisional chart to analyze, based on the matter
    we are interested in."

    Table 11 is published chart-first; §6.5 reads it matter-first. That
    direction is what `charts_for_matter` provides.
    """
    assert "based on the matter" in CHOOSE_CHART_BY_MATTER


@pytest.mark.parametrize("matter,expected", [
    ("career", "D10"),                 # "we should analyze one's dasamsa chart (D-10)"
    ("luxuries and pleasures", "D16"),  # "we should analyze one's shodasamsa (D-16)"
    ("residence and fortune", "D4"),    # "related to residence and fortune"
])
def test_6_5_the_books_own_three_examples(matter, expected):
    """The three matters §6.5 names, resolved through the index."""
    assert charts_for_matter(matter) == [expected]


def test_6_5_an_unnamed_matter_returns_nothing_rather_than_a_guess():
    """The index is built from Table 11's own wording, so it can only answer
    for matters the book names. Returning a plausible chart for anything else
    would be inventing significations."""
    assert charts_for_matter("cryptocurrency") == []
    assert charts_for_matter("xyzzy") == []


def test_6_5_the_index_invents_no_vocabulary():
    """Every chart the index can return is returned because a word of the
    query appears in **PVR's own signification text** for it.

    D-45 is excluded — see the next test.
    """
    from hora.charts.vargas import _MATTER_STOPWORDS

    for code in VARGA_SIGNIFICATIONS:
        if code == "D45":
            continue
        word = next(
            w for w in VARGA_SIGNIFICATIONS[code].lower().replace(",", " ").split()
            if len(w) > 4 and w not in _MATTER_STOPWORDS
        )
        assert code in charts_for_matter(word), (code, word)


def test_6_5_d45_can_never_be_reached_by_matter():
    """Table 11 gives D-45 the signification **"All matters"** — and nothing
    else. Both words are ordinary English, so no specific query can single it
    out, and it is the only chart of the twenty in that position.

    That is the right behaviour rather than a gap: a chart that signifies
    everything cannot be *chosen by matter*, which is all §6.5's method does.
    It stays reachable by name through `/v1/varga/compute` and `/v1/varga/rules`.
    D-60 escapes the same fate only because its row also says "Karma of past
    life".
    """
    from hora.charts.vargas import _MATTER_STOPWORDS

    assert VARGA_SIGNIFICATIONS["D45"] == "All matters"
    assert all(
        w in _MATTER_STOPWORDS
        for w in VARGA_SIGNIFICATIONS["D45"].lower().split()
    )
    unreachable = [
        code for code in VARGA_SIGNIFICATIONS
        if not any(
            code in charts_for_matter(w)
            for w in VARGA_SIGNIFICATIONS[code].lower().replace(",", " ").split()
            if len(w) > 2
        )
    ]
    assert unreachable == ["D45"]
    assert charts_for_matter("karma") == ["D60"], "D-60 has a specific word too"


def test_6_5_all_matters_charts_do_not_crowd_out_specific_ones():
    """D-45 and D-60 signify "all matters". A query for career must not come
    back with them beside D-10, or the index would be useless."""
    assert charts_for_matter("career") == ["D10"]
    assert "D45" not in charts_for_matter("marriage")
    # But they are reachable when nothing more specific matches.
    assert charts_for_matter("past life karma") == ["D60"]


def test_6_5_the_stopwords_are_grammar_not_astrology():
    """"and" alone appears in nine of the twenty significations. The excluded
    words are ordinary English; none is a term of art, so excluding them
    cannot drop a real match."""
    from hora.charts.vargas import _MATTER_STOPWORDS

    for word in _MATTER_STOPWORDS:
        assert not any(
            s.lower().strip(" ,.") == word for s in VARGA_SIGNIFICATIONS.values()
        ), word
    assert "and" in _MATTER_STOPWORDS
    assert sum("and" in s.lower() for s in VARGA_SIGNIFICATIONS.values()) >= 9


def test_6_5_the_general_method():
    """"We should remember which planets, rasis and houses show a particular
    matter and find links between them in the divisional chart of interest."

    Three things to link — planets, rasis, houses — and both worked patterns
    name all three.
    """
    for term in ("planets", "rasis", "houses", "find links"):
        assert term in FIND_LINKS_METHOD


@pytest.mark.parametrize("pattern", MATTER_ANALYSIS_PATTERNS)
def test_6_5_each_worked_pattern_names_a_chart_houses_and_a_significator(pattern):
    """§6.5's two patterns — going abroad via D-4, promotion via D-10. Each
    gives the chart, the houses and the significator, which is the shape
    FIND_LINKS_METHOD describes."""
    assert pattern["chart"] in VARGA_SIGNIFICATIONS
    assert pattern["houses"] and all(1 <= h <= 12 for h in pattern["houses"])
    assert pattern["significator"]
    assert pattern["link"]


def test_6_5_the_abroad_pattern_matches_table_11():
    """"It is related to residence and fortune and we should analyze one's
    chaturthamsa (D-4)." Table 11's D-4 row is "Residence, houses owned,
    properties and fortune" — the pattern's reasoning is Table 11's wording,
    which is the check that the two sections agree."""
    abroad = next(p for p in MATTER_ANALYSIS_PATTERNS if p["chart"] == "D4")
    assert "residence" in abroad["why"].lower()
    assert "fortune" in abroad["why"].lower()
    assert "Residence" in VARGA_SIGNIFICATIONS["D4"]
    assert "fortune" in VARGA_SIGNIFICATIONS["D4"]
    assert abroad["houses"] == [9, 12], "the 9th and 12th show foreign residence"


def test_6_5_the_promotion_pattern_uses_ghati_lagna():
    """"Because GL (ghati lagna) shows power and authority, planets or rasis
    giving a promotion are usually connected with GL."

    Chapter 5 gives GL "fame, power and authority" — the same words, so the
    two chapters are consistent.
    """
    from hora.charts.special_lagna import SPECIAL_LAGNA_SIGNIFIES, SpecialLagna

    promotion = next(p for p in MATTER_ANALYSIS_PATTERNS if p["chart"] == "D10")
    assert promotion["significator"] == "GL"
    assert "power and authority" in promotion["link"]
    assert "power and authority" in SPECIAL_LAGNA_SIGNIFIES[SpecialLagna.GHATI]


def test_6_5_the_closing_claim():
    """"This is the key to correct chart analysis."""
    assert "key to correct chart analysis" in KEY_TO_CHART_ANALYSIS


def test_footnote_12_cautions_the_three_highest_charts():
    """"Readers are advised to leave these higher charts until they find
    [a competent guru]."

    A caution about **interpretation**, not arithmetic — we compute D-40,
    D-45 and D-60 either way, and flag them in the response.
    """
    assert "competent guru" in HIGHER_CHARTS_CAUTION
    assert HIGHER_CHARTS_CAUTIONED == ("D40", "D45", "D60")
    # Exactly the kaarmic plane, which is what the footnote is attached to.
    kaarmic = [c for c in VARGA_SIGNIFICATIONS if VARGA_REGISTRY[c][2] >= 37]
    assert set(HIGHER_CHARTS_CAUTIONED) == set(kaarmic)
    # And they are still computed.
    for code in HIGHER_CHARTS_CAUTIONED:
        assert VARGA_REGISTRY[code][0](45.0) is not None


def test_the_for_matter_endpoint(client):
    """GET /v1/varga/for-matter is §6.5's direction of Table 11."""
    body = client.get("/v1/varga/for-matter", params={"matter": "career"}).json()
    assert [c["chart"] for c in body["charts"]] == ["D10"]
    assert body["charts"][0]["signifies"] == VARGA_SIGNIFICATIONS["D10"]
    assert body["charts"][0]["cautioned"] is False
    assert "find links" in body["method"]


def test_the_for_matter_endpoint_flags_the_cautioned_charts(client):
    body = client.get(
        "/v1/varga/for-matter", params={"matter": "past life karma"}
    ).json()
    assert body["charts"][0]["chart"] == "D60"
    assert body["charts"][0]["cautioned"] is True


def test_the_for_matter_endpoint_is_honest_about_a_miss(client):
    body = client.get("/v1/varga/for-matter", params={"matter": "xyzzy"}).json()
    assert body["charts"] == []
    assert "rather than a guess" in body["no_match_note"]


def test_the_rules_endpoint_now_carries_the_method_and_the_planes(client):
    body = client.get("/v1/varga/rules").json()
    assert "based on the matter" in body["choose_by_matter"]
    assert len(body["analysis_patterns"]) == 2
    assert len(body["planes"]) == 4
    assert body["higher_charts_caution"]["charts"] == ["D40", "D45", "D60"]


# --------------------------------------------------------------------------
# 6.6 Varga Grouping and Amsabala
# --------------------------------------------------------------------------


def test_6_6_what_makes_a_planet_strong_in_a_chart():
    """"If a planet is in its moolatrikona or an own rasi or its rasi of
    exaltation in a chart, it makes the planet very strong in that chart."

    Three dignities, and **debilitation does not subtract** — amsabala is a
    count that only goes up.
    """
    assert AMSABALA_DIGNITIES == ("moolatrikona", "own", "exalted")
    assert "debilitated" not in AMSABALA_DIGNITIES

    # The prose names the same three; it says "exaltation" where our label is
    # "exalted", so the concepts are checked rather than the exact strings.
    for phrase in ("moolatrikona", "own rasi", "exaltation"):
        assert phrase in AMSABALA_RULE

    # And the labels are the ones sign_dignity actually returns, so the count
    # cannot be looking for a word the calculation never produces.
    from hora.charts.dignity import sign_dignity
    from hora.core.const import Graha

    produced = {sign_dignity(g, x / 10) for g in range(7) for x in range(3600)}
    assert set(AMSABALA_DIGNITIES) <= produced
    # §3.3 rule 1 splits Leo: moolatrikona to 20 degrees, own beyond.
    assert sign_dignity(Graha.SUN, 125.0) == "moolatrikona", "5 deg Leo"
    assert sign_dignity(Graha.SUN, 145.0) == "own", "25 deg Leo"

    assert "higher this number" in AMSABALA_IS_MONOTONIC


#: §6.6.1 to §6.6.4 exactly as printed.
VARGA_GROUP_TABLE = [
    ("shadvarga", "six divisions",
     ["D1", "D2", "D3", "D9", "D12", "D30"]),
    ("saptavarga", "seven divisions",
     ["D1", "D2", "D3", "D7", "D9", "D12", "D30"]),
    ("dasavarga", "ten divisions",
     ["D1", "D2", "D3", "D7", "D9", "D10", "D12", "D16", "D30", "D60"]),
    ("shodasavarga", "sixteen divisions",
     ["D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20",
      "D24", "D27", "D30", "D40", "D45", "D60"]),
]


@pytest.mark.parametrize("group,meaning,charts", VARGA_GROUP_TABLE)
def test_6_6_each_group_is_the_charts_the_book_lists(group, meaning, charts):
    """"Shadvarga is a group of the following divisional charts: (1) Rasi
    chart, (2) D-2, (3) D-3, (4) D-9, (5) D-12, and, (6) D-30." and the three
    that follow."""
    assert list(VARGA_GROUPS[group]) == charts


@pytest.mark.parametrize("group,meaning,charts", VARGA_GROUP_TABLE)
def test_6_6_each_group_name_means_its_size(group, meaning, charts):
    """""Shadvarga" literally means "six divisions"." The name and the member
    count must agree — a chart added to a group would break the gloss."""
    assert VARGA_GROUP_MEANINGS[group] == meaning
    spelt = {"six": 6, "seven": 7, "ten": 10, "sixteen": 16}[meaning.split()[0]]
    assert len(charts) == spelt == len(VARGA_GROUPS[group])


def test_6_6_the_four_groups_are_strictly_nested():
    """shadvarga ⊂ saptavarga ⊂ dasavarga ⊂ shodasavarga.

    Not stated in the book; it falls out of the four lists. Each step only
    adds — saptavarga adds D-7, dasavarga adds D-10, D-16 and D-60,
    shodasavarga adds six more. A chart dropped from any group would break
    the chain, which is the cheapest check that none was mistyped.
    """
    order = ["shadvarga", "saptavarga", "dasavarga", "shodasavarga"]
    for smaller, larger in pairwise(order):
        assert set(VARGA_GROUPS[smaller]) < set(VARGA_GROUPS[larger]), (
            smaller, larger
        )
    assert set(VARGA_GROUPS["saptavarga"]) - set(VARGA_GROUPS["shadvarga"]) == {"D7"}
    assert set(VARGA_GROUPS["dasavarga"]) - set(VARGA_GROUPS["saptavarga"]) == {
        "D10", "D16", "D60",
    }


def test_6_6_every_group_starts_with_the_rasi_chart():
    """"(1) Rasi chart" opens all four lists. D-1 is the only chart in every
    group."""
    in_all = set.intersection(*(set(VARGA_GROUPS[g]) for g in VARGA_GROUPS))
    assert "D1" in in_all
    for charts in VARGA_GROUPS.values():
        assert charts[0] == "D1"


def test_6_6_five_charts_belong_to_no_group():
    """Of the twenty, D-5, D-6, D-8, D-11 and D-24 are absent from shadvarga,
    saptavarga and dasavarga; only D-24 makes shodasavarga. So four charts
    carry no amsabala weight at all."""
    grouped = set().union(*(set(v) for v in VARGA_GROUPS.values()))
    ungrouped = sorted(set(VARGA_SIGNIFICATIONS) - grouped)
    assert ungrouped == ["D11", "D5", "D6", "D8"]
    assert "D24" in VARGA_GROUPS["shodasavarga"]
    assert "D24" not in VARGA_GROUPS["dasavarga"]


#: The amsa names, exactly as §6.6.1 to §6.6.4 print them.
AMSA_TABLE = {
    "shadvarga": {
        2: "Kimsukaamsa", 3: "Vyanjanaamsa", 4: "Chaamaraamsa",
        5: "Chatraamsa", 6: "Kundalaamsa",
    },
    "saptavarga": {
        2: "Kimsukaamsa", 3: "Vyanjanaamsa", 4: "Chaamaraamsa",
        5: "Chatraamsa", 6: "Kundalaamsa", 7: "Mukutaamsa",
    },
    "dasavarga": {
        2: "Paarijaataamsa", 3: "Uttamaamsa", 4: "Gopuraamsa",
        5: "Simhaasanaamsa", 6: "Paaraavataamsa", 7: "Devalokaamsa",
        8: "Brahmalokamsa", 9: "Airaavataamsa", 10: "Sreedhaamaamsa",
    },
    "shodasavarga": {
        2: "Bhedakaamsa", 3: "Kusumaamsa", 4: "Nagapurushaamsa",
        5: "Kandukaamsa", 6: "Keralaamsa", 7: "Kalpavrikshaamsa",
        8: "Chandanavanaamsa", 9: "Poornachandraamsa", 10: "Uchchaisravaamsa",
        11: "Dhanvantaryamsa", 12: "Sooryakaantaamsa", 13: "Vidrumaamsa",
        14: "Indraasanaamsa", 15: "Golokaamsa", 16: "Sree Vallabhaamsa",
    },
}


@pytest.mark.parametrize("group", sorted(AMSA_TABLE))
def test_6_6_the_amsa_names_of_each_group(group):
    assert AMSA_NAMES[group] == AMSA_TABLE[group]


def test_6_6_the_amsa_counts_start_at_two():
    """Every list begins at 2. A planet strong in **one** chart, or none, has
    no amsa name — so an implementation keyed 0-based or starting at 1 would
    be off by one against every table."""
    for group, names in AMSA_TABLE.items():
        assert min(names) == 2, group
        assert 0 not in names and 1 not in names


def test_6_6_the_amsa_counts_run_up_to_the_group_size():
    """The top amsa of each group is the count of all its charts — 6, 7, 10
    and 16."""
    for group, names in AMSA_TABLE.items():
        assert max(names) == len(VARGA_GROUPS[group]), group
        assert sorted(names) == list(range(2, len(VARGA_GROUPS[group]) + 1))


def test_6_6_shadvarga_and_saptavarga_share_their_first_five_names():
    """Saptavarga is shadvarga plus D-7, and its amsa list is shadvarga's plus
    Mukutaamsa. The two are not independent vocabularies."""
    for count in range(2, 7):
        assert AMSA_TABLE["shadvarga"][count] == AMSA_TABLE["saptavarga"][count]
    assert set(AMSA_TABLE["saptavarga"]) - set(AMSA_TABLE["shadvarga"]) == {7}
    assert AMSA_TABLE["saptavarga"][7] == "Mukutaamsa"


def test_6_6_dasavarga_and_shodasavarga_share_no_names_with_the_others():
    """Unlike shadvarga and saptavarga, the larger two groups have their own
    vocabularies entirely — so an amsa name identifies its group."""
    small = set(AMSA_TABLE["saptavarga"].values())
    assert small & set(AMSA_TABLE["dasavarga"].values()) == set()
    assert small & set(AMSA_TABLE["shodasavarga"].values()) == set()
    assert (
        set(AMSA_TABLE["dasavarga"].values())
        & set(AMSA_TABLE["shodasavarga"].values())
    ) == set()


def test_6_6_every_amsa_name_is_distinct_across_all_four_groups():
    """35 names in all, allowing for the five shadvarga/saptavarga share."""
    everything = [n for g in AMSA_TABLE.values() for n in g.values()]
    assert len(everything) == 5 + 6 + 9 + 15
    assert len(set(everything)) == 6 + 9 + 15, "five names appear twice"


def test_6_6_3_note_says_what_the_amsas_are_for():
    """"This group is very important and some yogas – special combinations –
    make use of these amsas... Readers should memorize the above amsas."

    The only place the chapter says what an amsa is *used* for.
    """
    assert "yogas" in DASAVARGA_NOTE
    assert "memorize the above amsas" in DASAVARGA_NOTE


@pytest.mark.parametrize("combination", DASAVARGA_COMBINATIONS)
def test_6_6_3_the_two_named_combinations(combination):
    """"lagna lord or ghati lagna lord in Simhaasanaamsa would make one very
    famous. A quadrant lord with good amsabala in dasavarga makes one very
    successful."

    Both are dasavarga, and neither is implemented — they need yogas, which
    are a later chapter. See OI-54.
    """
    assert combination["group"] == "dasavarga"
    assert combination["result"] in ("very famous", "very successful")
    if combination["amsa"] is not None:
        assert combination["amsa"] in AMSA_TABLE["dasavarga"].values()


def test_6_6_3_simhaasanaamsa_is_five_of_ten():
    """The named amsa is the 5th of dasavarga's ten — half the charts, not a
    near-perfect score. Worth pinning: "very famous" is not the top amsa."""
    assert AMSA_TABLE["dasavarga"][5] == "Simhaasanaamsa"
    assert max(AMSA_TABLE["dasavarga"]) == 10
    assert AMSA_TABLE["dasavarga"][10] == "Sreedhaamaamsa"


def test_the_rules_endpoint_publishes_the_groups_and_amsa_names(client):
    body = client.get("/v1/varga/rules").json()
    for group, _, charts in VARGA_GROUP_TABLE:
        assert body["groups"][group] == charts
    for group, names in AMSA_TABLE.items():
        assert body["amsa_names"][group] == {str(k): v for k, v in names.items()}


# --------------------------------------------------------------------------
# 6.6 Example 27 — Bill Cosby's Jupiter, the chapter's only amsabala case
#
# This lived only in test_book_pages.py, which is gated on HORA_BOOK_PDF — so
# sixteen chart placements and four amsa verdicts were **skipped in CI**. Only
# one assertion there needs the PDF (that the book really prints "D-3: Li");
# it stays. Everything else is arithmetic and belongs here, where it always
# runs.
# --------------------------------------------------------------------------

#: "Jupiter is at 29 deg 49' in Sg."
COSBY_JUPITER = 240 + 29 + 49 / 60

#: "The signs occupied by him in various charts are shown below." All sixteen
#: as printed, D-3 included.
EXAMPLE_27_PRINTED = {
    "D1": "Sg", "D2": "Cn", "D3": "Li", "D4": "Vi", "D7": "Ge", "D9": "Sg",
    "D10": "Vi", "D12": "Sc", "D16": "Pi", "D20": "Pi", "D24": "Cn",
    "D27": "Ge", "D30": "Li", "D40": "Cn", "D45": "Le", "D60": "Sc",
}


def test_example_27_jupiters_longitude():
    """"Jupiter is at 29 deg 49' in Sg." Sagittarius is the 9th rasi."""
    assert COSBY_JUPITER == pytest.approx(269 + 49 / 60)
    assert readable_sign(int(COSBY_JUPITER // 30)) == "Sg"
    assert COSBY_JUPITER % 30 == pytest.approx(29 + 49 / 60)


@pytest.mark.parametrize(
    "code,expected",
    [(k, v) for k, v in EXAMPLE_27_PRINTED.items() if k != "D3"],
)
def test_example_27_fifteen_of_sixteen_charts_reproduce(code, expected):
    """Every chart in the printed list except D-3."""
    assert readable_sign(VARGA_REGISTRY[code][0](COSBY_JUPITER).sign) == expected


def test_example_27_d3_is_pvr_8():
    """The example prints **D-3: Li**. §6.2.3's rule sends the last 10 degrees
    of a rasi to the **9th** from it: Sg, Cp, Aq, Pi, Ar, Ta, Ge, Cn, **Le**.
    Libra is the 11th. We follow the rule. D-16 / PVR-8.
    """
    got = d3_drekkana(COSBY_JUPITER)
    assert got.amsa_index == 2, "the last 10 degrees"
    assert readable_sign(got.sign) == "Le"
    assert EXAMPLE_27_PRINTED["D3"] == "Li", "what the example prints"

    abbr = list(RASI_ABBR)
    chain = [abbr[(abbr.index("Sg") + i) % 12] for i in range(11)]
    assert chain[8] == "Le", "the 9th from Sagittarius"
    assert chain[10] == "Li", "Libra is the 11th"


def test_example_27_the_d3_deviation_cannot_change_any_amsa():
    """Why D-16's blast radius is nil: Jupiter's good signs are Cn, Sg and Pi.
    **Neither** Leo nor Libra is among them, so the D-3 cell is not counted in
    any group whichever reading is taken.

    Asserted rather than asserted-once-in-prose, because it is the whole
    reason the four amsa verdicts below still reproduce.
    """
    good = {"Cn", "Sg", "Pi"}
    assert "Le" not in good and "Li" not in good
    for group, charts in VARGA_GROUPS.items():
        if "D3" not in charts:
            continue
        strong = {
            code for code in charts
            if readable_sign(VARGA_REGISTRY[code][0](COSBY_JUPITER).sign) in good
        }
        assert "D3" not in strong, group


def test_example_27_jupiters_good_signs():
    """"Jupiter owns Sg and Pi. His moolatrikona is Sg. He is exalted in Cn.
    So we have to count the charts in which he is in Cn, Sg or Pi."""
    abbr = list(RASI_ABBR)
    assert {abbr[int(r)] for r in c.GRAHA_OWNS[Graha.JUPITER]} == {"Sg", "Pi"}
    assert abbr[int(c.MOOLATRIKONA[Graha.JUPITER][0])] == "Sg"
    assert abbr[int(c.EXALTATION_RASI[Graha.JUPITER])] == "Cn"


#: The four verdicts, and the charts the book says produce them.
EXAMPLE_27_AMSABALA = [
    ("shadvarga", 3, "Vyanjanaamsa", ["D1", "D2", "D9"]),
    ("saptavarga", 3, "Vyanjanaamsa", ["D1", "D2", "D9"]),
    ("dasavarga", 4, "Gopuraamsa", ["D1", "D2", "D9", "D16"]),
    ("shodasavarga", 7, "Kalpavrikshaamsa",
     ["D1", "D2", "D9", "D16", "D20", "D24", "D40"]),
]


@pytest.mark.parametrize("group,count,amsa,charts", EXAMPLE_27_AMSABALA)
def test_example_27_amsabala(group, count, amsa, charts):
    """"Out of the 6 divisional charts of shadvarga, Jupiter is in Cn, Sg or
    Pi in 3 charts – Rasi, D-2 and D-9. So Jupiter is in Vyanjanaamsa." and
    the three that follow.

    The **charts** are asserted, not only the count — a right total from the
    wrong charts would pass a count-only check.
    """
    result = varga_service.amsabala(COSBY_JUPITER, int(Graha.JUPITER))
    got = result["groups"][group]
    assert got["charts_in_group"] == len(VARGA_GROUPS[group])
    assert got["count"] == count
    assert got["amsa"] == amsa
    assert [entry["chart"] for entry in got["strong_in"]] == charts


def test_example_27_each_strong_chart_names_its_dignity():
    """D-1 and D-9 are own, D-2 is exalted — the three dignities §6.6 counts,
    with two of them actually appearing in one example."""
    result = varga_service.amsabala(COSBY_JUPITER, int(Graha.JUPITER))
    by_chart = {
        e["chart"]: e["dignity"]
        for e in result["groups"]["shodasavarga"]["strong_in"]
    }
    assert by_chart["D1"] == "own", "Sagittarius"
    assert by_chart["D9"] == "own", "Sagittarius"
    assert by_chart["D2"] == "exalted", "Cancer"
    assert set(by_chart.values()) <= set(AMSABALA_DIGNITIES)


def test_example_27_the_counts_rise_with_the_group_size():
    """3, 3, 4, 7 — the nested groups mean a count can never fall as the group
    grows, since every smaller group's charts are in the larger one."""
    result = varga_service.amsabala(COSBY_JUPITER, int(Graha.JUPITER))
    counts = [result["groups"][g]["count"] for g, _, _, _ in EXAMPLE_27_AMSABALA]
    assert counts == [3, 3, 4, 7]
    assert counts == sorted(counts), "nested groups cannot lose a strong chart"


def test_example_27_through_the_endpoint(client):
    body = client.post(
        "/v1/varga/amsabala", json={"longitude": "29 Sg 49", "graha": 4}
    ).json()
    assert body["graha_name"] == "Jupiter"
    for group, count, amsa, _ in EXAMPLE_27_AMSABALA:
        assert body["groups"][group]["count"] == count
        assert body["groups"][group]["amsa"] == amsa


def test_example_27_makes_jupiter_very_strong():
    """"Being in Gopuramsa and Kalpavrikshamsa makes Jupiter very strong."

    Both are above the midpoint of their group — 4 of 10 and 7 of 16 — which
    is what "very strong" rests on. Neither is near the top, so the claim is
    about the amsa reached, not a high fraction.
    """
    result = varga_service.amsabala(COSBY_JUPITER, int(Graha.JUPITER))
    assert result["groups"]["dasavarga"]["amsa"] == "Gopuraamsa"
    assert result["groups"]["shodasavarga"]["amsa"] == "Kalpavrikshaamsa"
    assert AMSA_TABLE["dasavarga"][4] == "Gopuraamsa"
    assert AMSA_TABLE["shodasavarga"][7] == "Kalpavrikshaamsa"
    assert max(AMSA_TABLE["dasavarga"]) == 10
    assert max(AMSA_TABLE["shodasavarga"]) == 16
    assert 4 < max(AMSA_TABLE["dasavarga"]), "not the top amsa"
    assert 7 < max(AMSA_TABLE["shodasavarga"]), "not the top amsa"
