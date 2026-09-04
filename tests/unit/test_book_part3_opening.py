"""Part 3's opening page — what a transit is and what the part is for.

Part 2 opened with a roadmap of nine named dasa systems, which
`test_book_part2_dasa_map.py` checks off as they are built. Part 3 names no
techniques at all, so these tests pin the definition and the scope instead, and
record that there is nothing to check off.
"""
from __future__ import annotations


def test_a_transit_is_a_relation_between_two_charts():
    """"The relationship between (1) the positions of planets at a given time
    and (2) the positions of planets at a person's birthtime."  Not a property
    of the sky on its own.
    """
    from hora.core.const import (
        TRANSIT_INPUTS,
        TRANSITS_MEANS,
        TRANSITS_RELATE_TWO_CHARTS,
    )

    assert "constant movement of planets" in TRANSITS_MEANS
    assert "Planets keep moving" in TRANSITS_MEANS

    assert len(TRANSIT_INPUTS) == 2
    assert [row["input"] for row in TRANSIT_INPUTS] == ["1", "2"]
    assert TRANSIT_INPUTS[0]["is"] == "the positions of planets at a given time"
    assert TRANSIT_INPUTS[1]["is"] == (
        "the positions of planets at a person's birthtime")
    for row in TRANSIT_INPUTS:
        assert row["is"] in TRANSITS_RELATE_TWO_CHARTS


def test_part_3_assumes_positions_and_judges_them():
    """"Judging the results for a person based on those, given the natal
    (birth) chart, is the subject of this part."  The part computes no
    positions; it reads them.
    """
    from hora.core.const import (
        PART_3_NEEDS_NO_NEW_EPHEMERIS,
        POSITIONS_ARE_ASSUMED,
        TRANSIT_INPUTS,
    )

    assert "is the subject of this part" in POSITIONS_ARE_ASSUMED
    assert "ephemeris or almanacs" in TRANSIT_INPUTS[0]["source"]
    assert TRANSIT_INPUTS[1]["source"] == "the natal (birth) chart"
    assert "reading between them" in PART_3_NEEDS_NO_NEW_EPHEMERIS


def test_both_of_part_3s_inputs_are_already_computable():
    """A chart for an arbitrary instant and a chart for a birth are the same
    call, so nothing in Part 3 waits on the ephemeris.
    """
    from hora.charts.book import chart
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import Settings
    from hora.core.timeutil import from_local

    record = chart(3)
    place = Place(name="Chart 3", **record["place"])
    natal = compute_chart(from_local(**record["birth_data"]), place, Settings())
    later = compute_chart(
        from_local(year=1998, month=3, day=19, hour=12, minute=0,
                   second=0.0, utc_offset_hours=5.5),
        place, Settings())

    assert natal.positions.keys() == later.positions.keys()
    assert natal.lagna_rasi is not None and later.lagna_rasi is not None
    assert natal.instant.jd_ut < later.instant.jd_ut


def test_part_3_names_no_techniques_where_part_2_named_nine():
    """"Some of those techniques are explained in this part."  There is no
    roadmap to check off, unlike Part 2's nine systems.
    """
    from hora.core.const import PART_2_DASA_SYSTEMS, PART_3_IS_KNOWINGLY_PARTIAL

    assert len(PART_2_DASA_SYSTEMS) == 9
    assert "Some of those techniques" in PART_3_IS_KNOWINGLY_PARTIAL
    assert "many special techniques" in PART_3_IS_KNOWINGLY_PARTIAL
    # nothing named, so nothing to count
    assert not [word for word in PART_3_IS_KNOWINGLY_PARTIAL.split()
                if word.endswith(("dasa", "gochara"))]


def test_the_verbatim_list_covers_every_transcribed_passage():
    from hora.core import const
    from hora.core.const import TRANSIT_VERBATIM_CONSTANTS

    for name in TRANSIT_VERBATIM_CONSTANTS:
        value = getattr(const, name)
        assert isinstance(value, str) and value
    assert set(TRANSIT_VERBATIM_CONSTANTS) == {
        "TRANSITS_MEANS", "TRANSITS_RELATE_TWO_CHARTS",
        "POSITIONS_ARE_ASSUMED", "PART_3_IS_KNOWINGLY_PARTIAL"}
