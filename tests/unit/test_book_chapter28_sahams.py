"""§28.8.1 and Table 74 — the sahams.

The section OI-116 has waited on since chapter 13. Its one subtlety is the
thirty-degree correction, so that is checked from three sides: against the
section's own gloss, against an independently written re-derivation of every
row, and against the properties the rule has to have.
"""
from __future__ import annotations

import pytest


def test_the_formula_rule_and_its_gloss_are_transcribed():
    from hora.tajaka.sahams import (
        DAY_AND_NIGHT_RULE,
        SAHAM_CORRECTION_DEGREES,
        SAHAM_DEFINITION,
        SAHAM_FORMULA_RULE,
        SAHAM_WORKED_GLOSS,
    )

    assert "raajya saham" in SAHAM_DEFINITION
    assert "paradesa saham" in SAHAM_DEFINITION
    assert "A – B + C" in SAHAM_FORMULA_RULE
    assert "if C is not between B and A" in SAHAM_FORMULA_RULE
    assert "we add 30º" in SAHAM_FORMULA_RULE
    assert SAHAM_CORRECTION_DEGREES == 30.0
    assert "(Moon – Sun + Lagna)" in SAHAM_WORKED_GLOSS
    assert "it changes to (B – A + C)" in DAY_AND_NIGHT_RULE


def test_the_between_test_is_the_arc_walked_forward_from_b():
    from hora.tajaka.sahams import is_between

    # Plain arc.
    assert is_between(100.0, 10.0, 50.0) is True
    assert is_between(100.0, 10.0, 200.0) is False
    # An arc that wraps through Aries needs no special case.
    assert is_between(10.0, 350.0, 0.0) is True
    assert is_between(10.0, 350.0, 180.0) is False
    # Both ends count as met.
    assert is_between(100.0, 10.0, 10.0) is True
    assert is_between(100.0, 10.0, 100.0) is True
    # A zero-length arc admits only its own point.
    assert is_between(40.0, 40.0, 40.0) is True
    assert is_between(40.0, 40.0, 41.0) is False


def test_the_correction_is_thirty_degrees_applied_once():
    from hora.tajaka.sahams import saham_point

    inside = saham_point(100.0, 10.0, 50.0)
    assert inside["c_is_between"] is True
    assert inside["correction"] == 0.0
    assert inside["longitude"] == inside["uncorrected"] == 140.0

    outside = saham_point(100.0, 10.0, 200.0)
    assert outside["c_is_between"] is False
    assert outside["correction"] == 30.0
    assert outside["uncorrected"] == 290.0
    assert outside["longitude"] == 320.0
    # Once, not until it lands somewhere.
    assert (outside["longitude"] - outside["uncorrected"]) % 360 == 30.0

    for step in range(0, 360, 11):
        got = saham_point(100.0, 10.0, float(step))
        assert 0.0 <= got["longitude"] < 360.0
        assert got["longitude"] == (got["uncorrected"]
                                    + got["correction"]) % 360.0


def test_the_sections_own_gloss_of_punya_reproduces():
    """"finding how far Moon is from Sun and taking the same distance from
    lagna" — the two readings must agree, and they do.
    """
    from hora.tajaka.sahams import saham_point

    moon, sun, lagna = 100.0, 10.0, 50.0
    got = saham_point(moon, sun, lagna)
    # "How far Moon is from Sun", taken from lagna.
    assert got["uncorrected"] == (lagna + (moon - sun) % 360) % 360
    # "If we ... do not find lagna on the way, then we have to add 30º."
    assert saham_point(moon, sun, 200.0)["correction"] == 30.0


def test_the_correction_is_a_thirty_degree_step():
    from hora.tajaka.sahams import (
        THE_CORRECTION_IS_A_THIRTY_DEGREE_STEP,
        saham_point,
    )

    # Walking C past the end of the arc jumps the saham by a whole rasi.
    just_in = saham_point(100.0, 10.0, 99.999)["longitude"]
    just_out = saham_point(100.0, 10.0, 100.001)["longitude"]
    assert abs((just_out - just_in) % 360 - 30.0) < 0.01
    assert "discontinuous at both ends" in (
        THE_CORRECTION_IS_A_THIRTY_DEGREE_STEP)


def test_table_74_has_thirty_six_rows_and_vidya_has_no_number():
    from hora.tajaka.sahams import (
        TABLE_74_SAHAMS,
        TABLE_74_TITLE,
        VIDYA_HAS_NO_ROW_NUMBER,
    )

    assert TABLE_74_TITLE == "Sahams"
    assert len(TABLE_74_SAHAMS) == 36
    names = [row["name"] for row in TABLE_74_SAHAMS]
    assert len(set(names)) == 36
    numbers = [row["number"] for row in TABLE_74_SAHAMS]
    assert numbers[0] == 1 and numbers[1] is None and numbers[2] == 3
    assert [n for n in numbers if n is not None] == [1, *range(3, 37)]
    assert names[1] == "Vidya"
    assert "its number is not printed" in VIDYA_HAS_NO_ROW_NUMBER


def test_every_row_has_three_terms_of_known_kinds():
    from hora.tajaka.sahams import TABLE_74_SAHAMS

    kinds = {"graha", "lagna", "saham", "house", "house_lord", "lagna_lord",
             "sign_lord", "fixed"}
    for row in TABLE_74_SAHAMS:
        for key in ("day", "night", "if_mars_owns_lagna"):
            formula = row.get(key)
            if not isinstance(formula, tuple):
                continue
            assert len(formula) == 3, (row["name"], key)
            for term in formula:
                assert term[0] in kinds, (row["name"], term)
        assert row["night"] in (None, "same") or isinstance(row["night"],
                                                            tuple)


def test_the_inputs_table_74_needs_are_enumerable_without_running_it():
    from hora.tajaka.sahams import house_lords_needed, houses_needed

    assert houses_needed() == (2, 6, 8, 9, 11)
    assert house_lords_needed() == (2, 9, 11)


def test_five_sahams_depend_on_others_and_the_order_resolves_them():
    from hora.tajaka.sahams import (
        FIVE_SAHAMS_DEPEND_ON_OTHERS,
        TABLE_74_SAHAMS,
        saham_order,
    )

    dependent = {}
    for row in TABLE_74_SAHAMS:
        wanted = {term[1] for term in row["day"] if term[0] == "saham"}
        if wanted:
            dependent[row["name"]] = wanted
    assert dependent == {
        "Yasas": {"Punya"}, "Mitra": {"Punya"}, "Mahatmya": {"Punya"},
        "Preeti": {"Sastra", "Punya"}, "Bandhana": {"Punya"}}

    order = saham_order()
    assert len(order) == 36
    place = {name: index for index, name in enumerate(order)}
    for name, wanted in dependent.items():
        for other in wanted:
            assert place[other] < place[name], (name, other)
    assert "no reference is circular" in FIVE_SAHAMS_DEPEND_ON_OTHERS


def test_the_night_formula_swaps_the_first_two_terms_except_where_marked():
    from hora.tajaka.sahams import TABLE_74_SAHAMS, formula_for

    by_name = {row["name"]: row for row in TABLE_74_SAHAMS}

    # The general rule.
    punya = by_name["Punya"]
    assert formula_for(punya, daytime=True) == (
        ("graha", "Moon"), ("graha", "Sun"), ("lagna",))
    assert formula_for(punya, daytime=False) == (
        ("graha", "Sun"), ("graha", "Moon"), ("lagna",))

    # "same for day & night" — six rows say so.
    unchanged = [row["name"] for row in TABLE_74_SAHAMS
                 if row["night"] == "same"]
    assert unchanged == ["Bhratri", "Mrityu", "Paradesa", "Artha", "Vyapara",
                         "Labha"]
    for name in unchanged:
        row = by_name[name]
        assert formula_for(row, daytime=True) == formula_for(row,
                                                             daytime=False)

    # Karyasiddhi prints its own night formula, and it is not a swap.
    karya = by_name["Karyasiddhi"]
    day, night = (formula_for(karya, daytime=d) for d in (True, False))
    assert day == (("graha", "Saturn"), ("graha", "Sun"),
                   ("sign_lord", "Sun"))
    assert night == (("graha", "Saturn"), ("graha", "Moon"),
                     ("sign_lord", "Moon"))
    assert night != (day[1], day[0], day[2])


def test_samartha_takes_its_other_formula_when_mars_owns_lagna():
    from hora.tajaka.sahams import TABLE_74_SAHAMS, formula_for

    samartha = next(row for row in TABLE_74_SAHAMS
                    if row["name"] == "Samartha")
    ordinary = formula_for(samartha, daytime=True, mars_owns_lagna=False)
    assert ordinary == (("graha", "Mars"), ("lagna_lord",), ("lagna",))
    special = formula_for(samartha, daytime=True, mars_owns_lagna=True)
    assert special == (("graha", "Jupiter"), ("graha", "Mars"), ("lagna",))


def test_punya_and_vidya_exchange_at_night():
    from hora.tajaka.sahams import (
        PUNYA_AND_VIDYA_EXCHANGE_AT_NIGHT,
        TABLE_74_SAHAMS,
        formula_for,
    )

    by_name = {row["name"]: row for row in TABLE_74_SAHAMS}
    punya, vidya = by_name["Punya"], by_name["Vidya"]
    assert formula_for(punya, daytime=False) == formula_for(vidya,
                                                            daytime=True)
    assert formula_for(vidya, daytime=False) == formula_for(punya,
                                                            daytime=True)
    assert "trade values" in PUNYA_AND_VIDYA_EXCHANGE_AT_NIGHT


def test_roga_is_the_only_row_that_repeats_a_term():
    from hora.tajaka.sahams import ROGA_USES_THE_LAGNA_TWICE, TABLE_74_SAHAMS

    repeats = [row["name"] for row in TABLE_74_SAHAMS
               if len(set(row["day"])) < 3]
    assert repeats == ["Roga"]
    roga = next(row for row in TABLE_74_SAHAMS if row["name"] == "Roga")
    assert roga["day"] == (("lagna",), ("graha", "Moon"), ("lagna",))
    assert "No other saham repeats a term" in ROGA_USES_THE_LAGNA_TWICE


# --------------------------------------------------------------------------
# The computation, checked against an independent re-derivation
# --------------------------------------------------------------------------

E118_LAT, E118_LON = 26 + 18 / 60, 73 + 4 / 60
CHART_66 = (2000, 3, 8, 4, 41, 21.0)


def _chart_66_inputs():
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import GRAHA_NAMES
    from hora.core.settings import Settings
    from hora.core.timeutil import from_local
    from hora.tajaka.sahams import houses_needed

    chart = compute_chart(
        from_local(*CHART_66, utc_offset_hours=5.5),
        Place(name="birthplace", latitude=E118_LAT, longitude=E118_LON),
        Settings())
    longitudes = {str(GRAHA_NAMES[graha]): chart.positions[graha].longitude
                  for graha in range(7)}
    # One possible reading of "the nth house", supplied rather than assumed.
    houses = {n: ((chart.lagna_rasi + n - 1) % 12) * 30.0
              for n in houses_needed()}
    return longitudes, chart.lagna_longitude, houses


def test_all_thirty_six_sahams_compute_for_chart_66():
    from hora.tajaka.sahams import TABLE_74_SAHAMS, sahams

    longitudes, lagna, houses = _chart_66_inputs()
    got = sahams(longitudes=longitudes, lagna=lagna, daytime=False,
                 houses=houses)
    assert len(got) == 36
    assert list(got) == [row["name"] for row in TABLE_74_SAHAMS]
    for name, row in got.items():
        assert row["undecided"] is None, name
        assert 0.0 <= row["longitude"] < 360.0, name
        assert row["rasi"] == int(row["longitude"] // 30)


def test_every_saham_is_re_derived_independently():
    """The arithmetic written a second time, from the returned terms.

    If the resolver picked the wrong longitude for a term this would not
    catch it, but any error in the formula, the correction or the wrap would.
    """
    from hora.tajaka.sahams import sahams

    longitudes, lagna, houses = _chart_66_inputs()
    for daytime in (True, False):
        got = sahams(longitudes=longitudes, lagna=lagna, daytime=daytime,
                     houses=houses)
        for name, row in got.items():
            a, b, c = row["a"], row["b"], row["c"]
            expected = (a - b + c) % 360.0
            on_the_way = ((c - b) % 360.0) <= ((a - b) % 360.0) + 1e-9
            if not on_the_way:
                expected = (expected + 30.0) % 360.0
            assert row["c_is_between"] == on_the_way, name
            assert abs(row["longitude"] - expected) < 1e-9, name


def test_punya_and_vidya_check_out_by_hand_for_chart_66():
    """Two rows worked through with nothing but arithmetic."""
    from hora.tajaka.sahams import sahams

    longitudes, lagna, houses = _chart_66_inputs()
    got = sahams(longitudes=longitudes, lagna=lagna, daytime=False,
                 houses=houses)
    sun, moon = longitudes["Sun"], longitudes["Moon"]

    # Night, so Punya is Sun - Moon + Lagna.
    punya = got["Punya"]
    assert (punya["a"], punya["b"], punya["c"]) == (sun, moon, lagna)
    assert ((lagna - moon) % 360) <= ((sun - moon) % 360)      # on the arc
    assert punya["correction"] == 0.0
    assert abs(punya["longitude"] - (sun - moon + lagna) % 360) < 1e-9

    # And Vidya is Moon - Sun + Lagna, with the lagna off the arc.
    vidya = got["Vidya"]
    assert (vidya["a"], vidya["b"], vidya["c"]) == (moon, sun, lagna)
    assert ((lagna - sun) % 360) > ((moon - sun) % 360)        # off the arc
    assert vidya["correction"] == 30.0
    assert abs(vidya["longitude"]
               - ((moon - sun + lagna) % 360 + 30) % 360) < 1e-9


def test_the_structural_collisions_hold_in_every_chart():
    """Checked over sixty random charts, not asserted from the table."""
    import random

    from hora.tajaka.sahams import houses_needed, saham_collisions, sahams

    random.seed(11)
    for daytime in (True, False):
        expected = set(saham_collisions(daytime=daytime))
        for _trial in range(60):
            longitudes = {name: random.uniform(0.0, 360.0) for name in
                          ("Sun", "Moon", "Mars", "Mercury", "Jupiter",
                           "Venus", "Saturn")}
            lagna = random.uniform(0.0, 360.0)
            houses = {n: ((int(lagna // 30) + n - 1) % 12) * 30.0
                      for n in houses_needed()}
            got = sahams(longitudes=longitudes, lagna=lagna,
                         daytime=daytime, houses=houses)
            for first, second in expected:
                assert abs(got[first]["longitude"]
                           - got[second]["longitude"]) < 1e-9, (
                    first, second, daytime)


def test_the_collisions_are_what_the_finding_says():
    from hora.tajaka.sahams import (
        SAHAM_COLLISIONS,
        SAHAMS_COINCIDE_STRUCTURALLY,
        saham_collisions,
    )

    assert saham_collisions(daytime=True) == (("Pitri", "Rajya"),
                                              ("Satru", "Vyapara"))
    assert saham_collisions(daytime=False) == (("Pitri", "Rajya"),
                                               ("Asha", "Vyapara"),
                                               ("Bhratri", "Jeeva"))
    # Only the first pair shares a printed formula; the rest are made by the
    # day-and-night markers.
    printed = [row for row in SAHAM_COLLISIONS
               if "printed" in str(row["because"])]
    assert {tuple(row["sahams"]) for row in printed} == {
        ("Pitri", "Rajya"), ("Satru", "Vyapara")}
    assert "meeting the general swap" in SAHAMS_COINCIDE_STRUCTURALLY


def test_a_missing_house_longitude_leaves_five_sahams_undecided():
    """OI-157. §28.8 never says what a house's longitude is, so it is an
    input and the rows that need one say so when it is absent.
    """
    from hora.tajaka.sahams import (
        A_HOUSES_LONGITUDE_IS_NOT_DEFINED,
        sahams,
    )

    longitudes, lagna, _houses = _chart_66_inputs()
    got = sahams(longitudes=longitudes, lagna=lagna, daytime=False)
    blank = [name for name, row in got.items() if row["longitude"] is None]
    assert sorted(blank) == ["Apamrityu", "Artha", "Labha", "Mrityu",
                             "Paradesa", "Santapa"]
    for name in blank:
        assert "was not supplied" in got[name]["undecided"]
    # The other thirty are unaffected.
    assert len(got) - len(blank) == 30
    assert "up to thirty degrees" in A_HOUSES_LONGITUDE_IS_NOT_DEFINED


def test_sahams_checks_its_inputs():
    from hora.tajaka.sahams import SahamError, sahams

    longitudes, lagna, houses = _chart_66_inputs()
    for missing in ("Sun", "Saturn"):
        short = {k: v for k, v in longitudes.items() if k != missing}
        with pytest.raises(SahamError):
            sahams(longitudes=short, lagna=lagna, daytime=True,
                   houses=houses)


# --------------------------------------------------------------------------
# Against the two sahams the book prints elsewhere
# --------------------------------------------------------------------------


def test_chart_19s_rajya_saham_comes_out_in_libra():
    """Example 54: "Rajya saham and GL are also in Libra."

    Navin Patnaik was born at 12:58 am, so the night formula applies —
    Sun − Saturn + Lagna. The day formula puts it in Gemini.
    """
    from hora.charts import book
    from hora.core.const import RASI_ABBR
    from hora.tajaka.sahams import TWO_PRINTED_SAHAMS_REPRODUCE, saham_point

    printed = book.longitudes(19)
    night = saham_point(printed["Sun"], printed["Sat"], printed["Asc"])
    assert RASI_ABBR[int(night["longitude"] // 30)] == "Li"
    assert night["longitude"] == pytest.approx(186 + 20 / 60, abs=0.02)

    day = saham_point(printed["Sat"], printed["Sun"], printed["Asc"])
    assert RASI_ABBR[int(day["longitude"] // 30)] != "Li"
    assert "against Example 54's Libra" in TWO_PRINTED_SAHAMS_REPRODUCE


def test_chart_53s_vivaha_saham_comes_out_at_one_capricorn():
    """Example 104 prints vivaha saham at 1 Cp. The lady was born at 9:41 pm,
    so the night formula applies — Saturn − Venus + Lagna.
    """
    from hora.charts import book
    from hora.core.const import RASI_ABBR
    from hora.core.constants.book_charts import BOOK_CHARTS
    from hora.tajaka.sahams import saham_point

    assert BOOK_CHARTS[53]["sahams"] == {"vivaha": "1 Cp"}
    printed = book.longitudes(53)
    night = saham_point(printed["Sat"], printed["Ven"], printed["Asc"])
    assert RASI_ABBR[int(night["longitude"] // 30)] == "Cp"
    # 0 Cp 41, which is what "1 Cp" prints to at whole-degree precision.
    assert night["longitude"] % 30 == pytest.approx(41 / 60, abs=0.02)
    assert round(night["longitude"] % 30) == 1

    day = saham_point(printed["Ven"], printed["Sat"], printed["Asc"])
    assert RASI_ABBR[int(day["longitude"] // 30)] != "Cp"


def test_example_104s_saham_claim_can_now_be_checked():
    """"about 1° away" — measured against a computed saham, not a printed one.
    """
    from hora.charts import book
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import Settings
    from hora.core.timeutil import from_local
    from hora.tajaka.sahams import saham_point

    printed = book.longitudes(53)
    saham = saham_point(printed["Sat"], printed["Ven"],
                        printed["Asc"])["longitude"]
    place = Place(name="x", latitude=16 + 13 / 60, longitude=80 + 28 / 60)
    # The wedding day; the book gives no time.
    mercury = compute_chart(
        from_local(1999, 1, 24, 0, 0, 0.0, utc_offset_hours=5.5), place,
        Settings()).positions[3].longitude
    gap = abs(((mercury - saham + 180) % 360) - 180)
    assert 1.0 < gap < 1.5


def test_the_correction_has_no_worked_value_in_the_book():
    """Both printed sahams have C on the arc, so neither exercises the +30."""
    from hora.charts import book
    from hora.tajaka.sahams import (
        THE_CORRECTION_HAS_NO_WORKED_VALUE,
        saham_point,
    )

    nineteen = book.longitudes(19)
    fifty_three = book.longitudes(53)
    rajya = saham_point(nineteen["Sun"], nineteen["Sat"], nineteen["Asc"])
    vivaha = saham_point(fifty_three["Sat"], fifty_three["Ven"],
                         fifty_three["Asc"])
    assert rajya["correction"] == 0.0
    assert vivaha["correction"] == 0.0
    assert "Nothing in the book shows the correction applied" in (
        THE_CORRECTION_HAS_NO_WORKED_VALUE)
