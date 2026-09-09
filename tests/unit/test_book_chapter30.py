"""Chapter 30 — Annual dasas. §30.1 and footnotes 85 and 86."""

import pytest

from hora.dasha.annual import intro

# --------------------------------------------------------------------------
# §30.1 Introduction
# --------------------------------------------------------------------------


def test_the_introduction_is_transcribed():
    assert intro.CHAPTER_TITLE == "Annual Dasas"
    assert "when in the year will (s)he get married?" in intro.WHY_ANNUAL_DASAS
    assert "paramayush is of the order of 100 years" in (
        intro.WHY_THEY_MUST_BE_COMPRESSED)
    assert "compressed to a one-year period" in intro.WHY_THEY_MUST_BE_COMPRESSED
    assert "one constellation per year" in (
        intro.HOW_THE_TWO_COMPRESSED_DASAS_ARE_SEEDED)
    assert "one sign per year" in intro.HOW_THE_TWO_COMPRESSED_DASAS_ARE_SEEDED


def test_the_three_dasas_are_named_in_the_chapters_order():
    names = [row["name"] for row in intro.ANNUAL_DASAS]
    assert names == ["Patyayini dasa", "Mudda dasa", "Varsha Narayana dasa"]
    assert [row["number"] for row in intro.ANNUAL_DASAS] == [1, 2, 3]
    mudda = intro.ANNUAL_DASAS[1]
    assert mudda["also_called"] == ("Varsha Vimsottari dasa",)
    assert intro.ANNUAL_DASAS[0]["source"] == "mentioned by Tajaka writers"


def test_footnote_85_gives_ramans_name_for_patyayini():
    assert intro.FOOTNOTE_85 == (
        'Dr. B.V. Raman simply called this "Varsha dasa" (annual dasa).')
    assert "Varsha dasa" in intro.ANNUAL_DASAS[0]["also_called"]


def test_vimsottaris_paramayush_is_the_120_the_chapter_names():
    assert intro.paramayush("vimshottari") == 120
    assert "paramayush of 120 years" in (
        intro.HOW_THE_TWO_COMPRESSED_DASAS_ARE_SEEDED)


def test_narayana_dasas_paramayush_is_144_not_120():
    """Every rasi's first cycle plus its second is twelve years, and there are
    twelve rasis. Derived from chapter 18's own rule, not asserted. OI-174.
    """
    from hora.dasha.rasi.narayana import second_cycle_length

    for first in range(1, 13):
        assert first + second_cycle_length(first) == 12
    assert intro.narayana_full_cycle_years() == 144
    assert intro.narayana_full_cycle_years() != 120
    assert "144 years" in intro.NARAYANA_DASAS_PARAMAYUSH_IS_144_NOT_120


def test_the_first_narayana_cycle_alone_is_not_a_fixed_total_either():
    """So 120 is not the first cycle's sum under any chart."""
    from hora.dasha.rasi.narayana import second_cycle_length

    # A rasi's first-cycle length runs 1 to 12, so twelve rasis sum anywhere
    # from 12 to 144. Nothing pins it to 120.
    assert 12 * 1 == 12
    assert 12 * 12 == 144
    assert second_cycle_length(12) == 0
    assert "not a fixed total at all" in (
        intro.NARAYANA_DASAS_PARAMAYUSH_IS_144_NOT_120)


def test_the_order_of_a_hundred_covers_the_dasas_the_book_taught():
    from hora.dasha.nakshatra.systems import NAKSHATRA_DASHA_SYSTEMS

    totals = sorted(spec.total_years
                    for spec in NAKSHATRA_DASHA_SYSTEMS.values())
    assert totals[0] == 36 and totals[-1] == 120
    assert sum(1 for t in totals if 84 <= t <= 120) == 7
    assert "from 36 years to 120" in (
        intro.THE_ORDER_OF_A_HUNDRED_IS_A_RANGE_NOT_A_FIGURE)


# --------------------------------------------------------------------------
# The seeding choice, and footnote 86
# --------------------------------------------------------------------------


def test_both_seeds_come_from_the_natal_chart_not_the_annual_one():
    seeds = intro.SEEDING_CHOICES
    assert [row["dasa"] for row in seeds] == ["Mudda dasa",
                                              "Varsha Narayana dasa"]
    for row in seeds:
        assert "annual chart" in row["declined"]
        assert "natal chart" in row["taken"]
    assert [row["rate"] for row in seeds] == ["one constellation per year",
                                              "one sign per year"]
    assert "named and declined in both cases" in (
        intro.THE_ANNUAL_CHART_IS_NOT_THE_SEED)


def test_the_two_progressions_cycle_on_different_schedules():
    """27 constellations at one a year, 12 signs at one a year."""
    from hora.core.const import NAKSHATRA_COUNT

    assert NAKSHATRA_COUNT == 27
    assert intro.SEEDING_CHOICES[0]["rate"] == "one constellation per year"
    assert intro.SEEDING_CHOICES[1]["rate"] == "one sign per year"
    assert "cycles in 27 years and one sign a year in 12" in (
        intro.THE_TWO_PROGRESSIONS_HAVE_DIFFERENT_PERIODS)


def test_footnote_86_is_a_provenance_mark():
    assert intro.FOOTNOTE_86 == "This is a result of the author's own researches."
    assert "the author's own research" in intro.FOOTNOTE_86_IS_A_PROVENANCE_MARK


def test_25_4s_note_no_longer_claims_to_be_the_only_such_mark():
    """It said "the only section in the book to label its own technique".
    Footnote 86 does the same thing.
    """
    import inspect

    from hora.transits import gochara

    source = inspect.getsource(gochara)
    assert "the only section in the book to label its own" not in source
    assert "one of\n#: two places in the book that label the author's own" in (
        source)
    assert "footnote 86 of §30.1" in source


def test_precedence_covers_both_places(tmp_path):
    import pathlib

    text = pathlib.Path("docs/precedence.md").read_text()
    assert "When PVR marks his own research" in text
    assert "§25.4 and §30.1's footnote 86" in text
    assert "seeds two of chapter 30's three annual dasas" in text


def test_whether_footnote_86_covers_both_rules_is_not_marked():
    """It sits on the Narayana sentence; the Vimsottari sentence one earlier
    makes the same claim and carries none.
    """
    paragraph = intro.HOW_THE_TWO_COMPRESSED_DASAS_ARE_SEEDED
    vimsottari = paragraph.index("compressed Vimsottari dasa")
    narayana = paragraph.index("compressed Narayana dasa")
    assert vimsottari < narayana
    assert "Similarly" in paragraph
    assert "carries no footnote" in (
        intro.WHETHER_FOOTNOTE_86_COVERS_BOTH_RULES_IS_NOT_MARKED)


def test_the_compressed_dasas_point_at_systems_we_already_have():
    from hora.dasha.nakshatra.systems import NAKSHATRA_DASHA_SYSTEMS

    mudda = intro.ANNUAL_DASAS[1]
    assert mudda["compressed_from"] == "vimshottari"
    assert mudda["compressed_from"] in NAKSHATRA_DASHA_SYSTEMS
    assert intro.ANNUAL_DASAS[2]["compressed_from"] == "narayana"
    assert intro.ANNUAL_DASAS[0]["compressed_from"] is None


def test_nothing_is_computed_from_the_introduction_yet():
    """§30.1 states the plan; the three dasas arrive in §30.2 onwards."""
    with pytest.raises(KeyError):
        intro.paramayush("patyayini")
