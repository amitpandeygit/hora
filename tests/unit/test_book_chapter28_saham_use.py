"""§28.8.2 — Use of sahams."""

import pytest

from hora.tajaka import saham_use

# --------------------------------------------------------------------------
# The annual-chart rule
# --------------------------------------------------------------------------


def test_the_annual_rule_is_transcribed():
    assert "lord of the rasi containing an important saham" in (
        saham_use.USE_IN_ANNUAL_CHART)
    assert "may materialize during the year" in saham_use.USE_IN_ANNUAL_CHART


def test_the_annual_rule_supplies_one_of_its_three_terms():
    """The two lords are computable; "important" and "good" are not."""
    got = saham_use.annual_rule_terms(saham_longitude=212.5,
                                      lagna=280.0 + 50.0 / 60.0)
    # Example 121's artha saham at 2 Sc 30 — Scorpio, so Mars.
    assert got["saham_dispositor"]["rasi_name"] == "Scorpio"
    assert got["saham_dispositor"]["lord_name"] == "Mars"
    # Lagna 10 Cp 50 — Capricorn, so Saturn.
    assert got["lagna_lord_name"] == "Saturn"
    assert got["grahas"] == (2, 6)
    assert got["is_one_graha"] is False
    assert "does not say which yogas count as good" in got["yoga_undecided"]


def test_the_two_lords_are_one_graha_whenever_the_saham_sits_in_his_rasi():
    """Aries lagna, saham in Scorpio: Mars is both. The rule asks for a yoga
    between a graha and itself, and says nothing about that case.
    """
    got = saham_use.annual_rule_terms(saham_longitude=215.0, lagna=5.0)
    assert got["lagna_lord_name"] == "Mars"
    assert got["saham_dispositor"]["lord_name"] == "Mars"
    assert got["is_one_graha"] is True
    assert got["grahas"] == (2,)
    assert "forms none with itself" in saham_use.THE_TWO_LORDS_CAN_BE_ONE_GRAHA


def test_how_often_the_two_lords_collide():
    """Two rasis in twelve for the five two-rasi lords, one in twelve for the
    Sun and the Moon. Counted rather than asserted from the rule.
    """
    collisions = sum(
        saham_use.annual_rule_terms(saham_longitude=saham * 30.0 + 15.0,
                                    lagna=lagna * 30.0 + 15.0)["is_one_graha"]
        for lagna in range(12) for saham in range(12))
    # 10 lagnas owned by a two-rasi lord × 2, plus Cancer and Leo × 1.
    assert collisions == 22
    assert collisions / 144 == pytest.approx(0.1528, abs=5e-4)


def test_the_saham_dispositor_is_the_lord_of_the_rasi_it_falls_in():
    for longitude, rasi_name, lord in ((0.0, "Aries", "Mars"),
                                       (95.0, "Cancer", "Moon"),
                                       (359.99, "Pisces", "Jupiter")):
        got = saham_use.saham_dispositor(longitude)
        assert got["rasi_name"] == rasi_name
        assert got["lord_name"] == lord


# --------------------------------------------------------------------------
# The natal-chart rule
# --------------------------------------------------------------------------


def test_the_natal_rule_is_transcribed_with_both_of_its_cases():
    assert "Saturn or Rahu transits close to" in saham_use.USE_IN_NATAL_CHART
    assert "Jupiter occupies or aspects" in saham_use.USE_IN_NATAL_CHART

    rows = saham_use.NATAL_SAHAM_TRANSITS
    assert [row["sahams"] for row in rows] == [
        ("Paradesa", "Jalapatana"), ("Vivaha",)]
    assert [row["gives"] for row in rows] == [
        "one may go abroad", "one may get married"]


def test_all_three_sahams_the_rule_names_are_in_table_74():
    """Paradesa, Jalapatana and Vivaha — 21, 33 and 26."""
    from hora.tajaka.sahams import TABLE_74_SAHAMS

    numbers = {str(row["name"]): row["number"] for row in TABLE_74_SAHAMS}
    named = [name for row in saham_use.NATAL_SAHAM_TRANSITS
             for name in row["sahams"]]
    assert named == ["Paradesa", "Jalapatana", "Vivaha"]
    assert [numbers[n] for n in named] == [21, 33, 26]


def test_one_of_the_two_rules_needs_an_orb_and_the_other_does_not():
    rows = saham_use.NATAL_SAHAM_TRANSITS
    assert [row["needs_an_orb"] for row in rows] == [True, False]
    assert [row["test"] for row in rows] == ["transits close to",
                                             "occupies or aspects"]
    assert "can be answered outright" in (
        saham_use.ONE_RULE_NEEDS_AN_ORB_AND_ONE_DOES_NOT)


def test_saturn_or_rahu_near_refuses_to_invent_an_orb():
    got = saham_use.saturn_or_rahu_near(graha_longitude=1.0,
                                        saham_longitude=359.0)
    assert got["separation"] == pytest.approx(2.0)
    assert got["close"] is None
    assert got["undecided"] is not None

    with_orb = saham_use.saturn_or_rahu_near(graha_longitude=1.0,
                                             saham_longitude=359.0, orb=3.0)
    assert with_orb["close"] is True and with_orb["undecided"] is None
    tight = saham_use.saturn_or_rahu_near(graha_longitude=1.0,
                                          saham_longitude=359.0, orb=1.0)
    assert tight["close"] is False


def test_the_separation_wraps_through_aries():
    assert saham_use.saturn_or_rahu_near(
        graha_longitude=359.0, saham_longitude=1.0)["separation"] == (
        pytest.approx(2.0))
    assert saham_use.saturn_or_rahu_near(
        graha_longitude=90.0, saham_longitude=270.0)["separation"] == (
        pytest.approx(180.0))


def test_jupiter_occupying_vivaha_saham_is_a_hit_under_either_scheme():
    got = saham_use.jupiter_on_vivaha(jupiter_rasi=4, vivaha_rasi=4)
    assert got["occupies"] is True
    assert got["hit_by_graha_drishti"] and got["hit_by_tajaka"]
    assert got["agree"] is True and got["undecided"] is None


def test_the_two_aspect_schemes_disagree_and_neither_is_chosen():
    """Graha drishti reaches four rasis of twelve; §28.2's aspects reach ten.
    OI-158.
    """
    hits = {"graha_drishti": 0, "tajaka": 0, "disagree": 0}
    for vivaha in range(12):
        got = saham_use.jupiter_on_vivaha(jupiter_rasi=0, vivaha_rasi=vivaha)
        hits["graha_drishti"] += got["hit_by_graha_drishti"]
        hits["tajaka"] += got["hit_by_tajaka"]
        hits["disagree"] += not got["agree"]
    assert hits == {"graha_drishti": 4, "tajaka": 10, "disagree": 6}
    assert "reaches ten of the twelve rasis" in (
        saham_use.THE_TAJAKA_READING_WOULD_FIRE_ALMOST_ALWAYS)
    assert "without saying under which scheme" in (
        saham_use.WHICH_ASPECT_SCHEME_IS_NOT_SAID)


def test_the_tajaka_reading_misses_only_the_sixth_and_the_eighth():
    """§28.2 gives no aspect on those two houses, and that is the whole of
    the difference on the Tajaka side.
    """
    missed = [v for v in range(12)
              if not saham_use.jupiter_on_vivaha(
                  jupiter_rasi=0, vivaha_rasi=v)["hit_by_tajaka"]]
    assert missed == [5, 7]          # the 6th and 8th rasis from Aries


def test_jupiters_graha_drishti_reaches_the_fifth_seventh_and_ninth():
    reached = [v for v in range(12)
               if saham_use.jupiter_on_vivaha(
                   jupiter_rasi=0, vivaha_rasi=v)["aspects_by_graha_drishti"]]
    assert reached == [4, 6, 8]


def test_the_jupiter_rule_is_rejected_bad_input():
    for bad in ({"jupiter_rasi": 12, "vivaha_rasi": 0},
                {"jupiter_rasi": 0, "vivaha_rasi": -1}):
        with pytest.raises(Exception, match="rasi"):
            saham_use.jupiter_on_vivaha(**bad)


# --------------------------------------------------------------------------
# Against §25.3, which read the same saham
# --------------------------------------------------------------------------


def test_two_sections_read_vivaha_saham_for_marriage_and_disagree():
    from hora.core.const import GRAHA_NAMES, Graha
    from hora.transits.gochara import SAHAM_TRANSIT_EXAMPLES

    earlier = next(row for row in SAHAM_TRANSIT_EXAMPLES
                   if row["saham"] == "vivaha")
    assert earlier["transiting"] == ("the 7th lord", "Venus")
    assert earlier["gives"] == "marriage"

    later = next(row for row in saham_use.NATAL_SAHAM_TRANSITS
                 if "Vivaha" in row["sahams"])
    assert later["transiting"] == (int(Graha.JUPITER),)
    assert later["gives"] == "one may get married"

    # Neither graha is in the other's list, and the tests differ too.
    assert "Jupiter" not in earlier["transiting"]
    assert "Venus" not in [GRAHA_NAMES[g] for g in later["transiting"]]
    assert "two different tests for one event" in (
        saham_use.TWO_SECTIONS_READ_VIVAHA_SAHAM_DIFFERENTLY)


# --------------------------------------------------------------------------
# The closing note
# --------------------------------------------------------------------------


def test_the_arabian_parts_note_and_the_origin_paragraph_are_transcribed():
    assert "Arabian parts" in saham_use.ARABIAN_PARTS_NOTE
    assert "part of fortune" in saham_use.ARABIAN_PARTS_NOTE
    assert "learnt Tajaka system from Arabs" in (
        saham_use.TAJAKA_ORIGIN_SPECULATION)
    # The book offers it as speculation twice and asserts neither way.
    assert "This is possible" in saham_use.TAJAKA_ORIGIN_SPECULATION
    assert "One may speculate" in saham_use.TAJAKA_ORIGIN_SPECULATION


def test_the_origin_note_drives_no_calculation():
    assert "nothing is computed from it" in (
        saham_use.THE_ORIGIN_NOTE_CHANGES_NOTHING_COMPUTED)


def test_25_4s_provenance_note_no_longer_claims_to_be_the_only_one():
    """§28.8.2 carries a provenance too, of a different kind. The earlier
    note said "the only section in the book to carry one".
    """
    import inspect

    from hora.transits import gochara

    source = inspect.getsource(gochara)
    assert "the only section in the book to label its own" in source
    assert "the only section in the book to carry one" not in source
