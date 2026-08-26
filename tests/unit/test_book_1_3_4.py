"""§1.3.4 Chakras (charts) — occupancy and the rasi/bhava distinction.

The section is mostly about *drawing*, which this codebase does not do. Two
things in it are calculation and are implemented:

* **occupancy** — which bodies fall in which of the twelve rasis
* **rasi-based vs bhava-based** — whether a fixed position in a layout holds a
  rasi or a house. It is the only respect in which the three styles differ in
  substance, and it decides what a renderer needs from us.

Example 1 is Lord Sree Rama's rasi chart, drawn in all three styles in
Figure 1. The South and East Indian panels give the occupancy; the North
Indian panel gives the house numbers. Both are checked.
"""
import pytest

from hora.charts.chakra import (
    CHART_STYLES,
    LAGNA_MARK,
    STYLES_USED_IN_THE_BOOK,
    ChakraError,
    build,
)
from hora.core.const import Graha
from hora.services import chakra_service

ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]
R = {name: i for i, name in enumerate(ABBR)}


# --------------------------------------------------------------------------
# Example 1 — Lord Sree Rama's rasi chart
# --------------------------------------------------------------------------

#: "Ar - Sun; Ta - Mercury; Ge - Ketu; Cn - Ascendant (lagna), Moon & Jupiter;
#:  Li - Saturn; Sg - Rahu; Cp - Mars; Pi - Venus."
RAMA_GRAHAS = {
    int(Graha.SUN): "Ar", int(Graha.MERCURY): "Ta", int(Graha.KETU): "Ge",
    int(Graha.MOON): "Cn", int(Graha.JUPITER): "Cn", int(Graha.SATURN): "Li",
    int(Graha.RAHU): "Sg", int(Graha.MARS): "Cp", int(Graha.VENUS): "Pi",
}
RAMA_LAGNA = "Cn"

#: The occupancy as the South and East Indian panels of Figure 1 show it.
RAMA_OCCUPANCY = {
    "Ar": ["Sun"], "Ta": ["Mercury"], "Ge": ["Ketu"],
    "Cn": ["Jupiter", "Lagna", "Moon"], "Li": ["Saturn"], "Sg": ["Rahu"],
    "Cp": ["Mars"], "Pi": ["Venus"],
}

#: The house numbers the North Indian panel of Figure 1 writes beside each body.
RAMA_HOUSES = {
    "Sun": 10, "Mercury": 11, "Ketu": 12, "Moon": 1, "Jupiter": 1,
    "Lagna": 1, "Saturn": 4, "Rahu": 6, "Mars": 7, "Venus": 9,
}


@pytest.fixture(scope="module")
def rama():
    return build(
        graha_positions={g: R[s] for g, s in RAMA_GRAHAS.items()},
        lagna=R[RAMA_LAGNA],
        positions_are_longitudes=False,
    )


@pytest.mark.parametrize("abbr", ABBR)
def test_example_1_occupancy(abbr, rama):
    """Every cell, occupied or not — an empty cell is an assertion too."""
    cell = rama.cell_for_rasi(R[abbr])
    assert sorted(b.name for b in cell.bodies) == sorted(
        RAMA_OCCUPANCY.get(abbr, [])
    )


def test_example_1_leaves_four_rasis_empty(rama):
    assert [ABBR[r] for r in rama.empty_rasis] == ["Le", "Vi", "Sc", "Aq"]
    assert len(rama.occupied_rasis) == 8


@pytest.mark.parametrize("name,house", sorted(RAMA_HOUSES.items()))
def test_example_1_north_indian_house_numbers(name, house, rama):
    """Figure 1's North Indian panel labels each body with its house."""
    body = next(b for b in rama.bodies if b.name == name)
    assert rama.cell_for_rasi(body.rasi).house == house


def test_the_asc_box_shows_four_and_holds_cancer(rama):
    """"the box with 'Asc' has 4 in it and it shows Cn. So the 1st house is in
    Cn."

    The rasi number is what a North Indian chart writes in the box, and the
    section uses this chart to explain it.
    """
    first = rama.cell_for_house(1)
    assert first.rasi_number == 4
    assert first.abbreviation == "Cn"
    assert any(b.name == "Lagna" for b in first.bodies)


def test_example_1_lagna_shares_its_cell_with_two_grahas(rama):
    """"Cn - Ascendant (lagna), Moon & Jupiter" — one cell, three bodies."""
    cell = rama.cell_for_rasi(R["Cn"])
    assert len(cell.bodies) == 3
    assert {b.kind for b in cell.bodies} == {"lagna", "graha"}


# --------------------------------------------------------------------------
# What a chart is
# --------------------------------------------------------------------------

def test_a_chart_always_has_twelve_cells(rama):
    """"there are 12 boxes ... with each representing a rasi"."""
    assert len(rama.cells) == 12
    assert [c.rasi for c in rama.cells] == list(range(12))
    assert chakra_service.styles()["cells"] == 12


def test_rasi_numbers_run_one_to_twelve(rama):
    """"1 for Ar, 2 for Ta, 3 for Ge and so on"."""
    assert [c.rasi_number for c in rama.cells] == list(range(1, 13))


def test_the_twelve_houses_cover_every_cell_once(rama):
    seen = {rama.cell_for_house(h).rasi for h in range(1, 13)}
    assert seen == set(range(12))


def test_a_chart_can_be_built_from_any_subset_of_bodies():
    """Every group is optional; nothing is invented for one left out."""
    only_lagna = build(lagna=R["Ar"], positions_are_longitudes=False)
    assert only_lagna.body_count if False else len(only_lagna.bodies) == 1
    assert len(only_lagna.empty_rasis) == 11

    only_grahas = build(
        graha_positions={int(Graha.SUN): R["Le"]},
        positions_are_longitudes=False, reference=None,
    )
    assert len(only_grahas.bodies) == 1
    assert all(cell.house is None for cell in only_grahas.cells)


def test_upagrahas_and_special_lagnas_are_placed_too():
    """"all planets, upagrahas, lagna and special lagnas"."""
    chart = build(
        graha_positions={int(Graha.SUN): R["Ar"]},
        upagraha_positions={0: R["Ta"]},           # Dhuma
        special_lagna_positions={1: R["Ge"]},      # Hora Lagna
        lagna=R["Cn"], positions_are_longitudes=False,
    )
    kinds = {b.kind for b in chart.bodies}
    assert kinds == {"graha", "upagraha", "lagna", "special_lagna"}
    assert chart.cell_for_rasi(R["Ta"]).bodies[0].name == "Dhuma"
    assert chart.cell_for_rasi(R["Ge"]).bodies[0].name == "Hora Lagna"


# --------------------------------------------------------------------------
# Rasi-based against bhava-based
# --------------------------------------------------------------------------

def test_the_three_styles_and_their_ruling_planets():
    """"(1) South Indian style chart ruled by Jupiter, (2) North Indian style
    diamond chart ruled by Venus and (3) East Indian style Sun chart ruled by
    Sun"."""
    assert set(CHART_STYLES) == {"south_indian", "north_indian", "east_indian"}
    assert CHART_STYLES["south_indian"]["ruled_by"] == "Jupiter"
    assert CHART_STYLES["north_indian"]["ruled_by"] == "Venus"
    assert CHART_STYLES["east_indian"]["ruled_by"] == "Sun"


def test_only_the_north_indian_style_is_bhava_based():
    """"(1) and (3) are rasi-based and (2) is bhava-based"."""
    assert CHART_STYLES["south_indian"]["rasi_based"] is True
    assert CHART_STYLES["east_indian"]["rasi_based"] is True
    assert CHART_STYLES["north_indian"]["rasi_based"] is False


def test_the_book_uses_two_of_the_three():
    """"In this book, all the charts will be given in formats (1) and (2)"."""
    assert STYLES_USED_IN_THE_BOOK == ("south_indian", "north_indian")


def test_lagna_is_marked_asc():
    """"Lagna (denoted by 'Asc' for ascendant)"."""
    assert LAGNA_MARK == "Asc"
    assert chakra_service.styles()["lagna_mark"] == "Asc"


def test_a_rasi_based_and_a_bhava_based_view_of_the_same_chart_differ(rama):
    """The distinction is not cosmetic: position 1 holds a different cell.

    A rasi-based layout puts Aries first; a bhava-based one puts the 1st house
    first, which here is Cancer.
    """
    assert rama.cell_for_rasi(0).abbreviation == "Ar"
    assert rama.cell_for_house(1).abbreviation == "Cn"


# --------------------------------------------------------------------------
# Inputs
# --------------------------------------------------------------------------

def test_houses_are_refused_when_there_is_no_reference():
    """Undefined, not silently assumed to start at Aries."""
    chart = build(
        graha_positions={int(Graha.SUN): R["Le"]},
        positions_are_longitudes=False, reference=None,
    )
    with pytest.raises(ChakraError, match="no reference point"):
        chart.cell_for_house(1)


def test_a_named_reference_without_a_rasi_is_refused():
    with pytest.raises(ChakraError, match="no rasi for it was given"):
        build(graha_positions={int(Graha.SUN): 5.0}, reference="chandra_lagna")


def test_longitudes_carry_the_degrees_within_the_rasi():
    chart = build(graha_positions={int(Graha.SUN): 100.5})
    body = chart.bodies[0]
    assert body.rasi == R["Cn"]
    assert body.longitude == 100.5
    assert body.degrees_in_rasi == pytest.approx(10.5)


def test_bare_rasi_indices_carry_no_longitude():
    """A rasi is all §1.3.4 needs; claiming a longitude we were not given
    would be inventing precision."""
    chart = build(
        graha_positions={int(Graha.SUN): R["Cn"]}, positions_are_longitudes=False
    )
    body = chart.bodies[0]
    assert body.rasi == R["Cn"]
    assert body.longitude is None
    assert body.degrees_in_rasi is None


@pytest.mark.parametrize("position", [-1, 12, 99])
def test_an_out_of_range_rasi_is_refused(position):
    with pytest.raises(ValueError):
        build(graha_positions={int(Graha.SUN): position},
              positions_are_longitudes=False)


def test_the_service_returns_the_same_chart_as_the_engine(rama):
    payload = chakra_service.chakra(rama)
    assert payload["reference_rasi_name"] == "Cancer"
    assert payload["has_houses"] is True
    assert payload["body_count"] == 10
    assert len(payload["cells"]) == 12
    cancer = payload["cells"][R["Cn"]]
    assert cancer["rasi_number"] == 4
    assert cancer["house"] == 1
    assert len(cancer["bodies"]) == 3


def test_the_default_reference_applies_when_a_lagna_was_given():
    """§1.3.3's default, honoured without the caller naming it."""
    chart = build(
        graha_positions={int(Graha.SUN): R["Ar"]}, lagna=R["Cn"],
        positions_are_longitudes=False,
    )
    assert chart.reference == "lagna"
    assert chart.cell_for_rasi(R["Ar"]).house == 10


def test_the_default_reference_is_skipped_when_no_lagna_was_given():
    """Not asking for houses is not the same as asking for impossible ones.

    A caller who wants occupancy alone gets it. A caller who *names* a
    reference that cannot be resolved gets an error — see the test above.
    """
    chart = build(
        graha_positions={int(Graha.SUN): R["Ar"]}, positions_are_longitudes=False
    )
    assert chart.reference is None
    assert all(cell.house is None for cell in chart.cells)
    assert chart.cell_for_rasi(R["Ar"]).bodies[0].name == "Sun"


def test_a_fractional_value_is_refused_in_rasi_mode():
    """The likeliest misuse: a longitude passed with the flag off.

    5.5 is not a rasi index, so it is refused rather than read as Virgo.
    A whole number below 12 stays genuinely ambiguous and is accepted —
    see docs/api-contract.md D-1.
    """
    for value in (5.5, 11.99, 0.1):
        with pytest.raises(ChakraError, match="not a rasi index"):
            build(graha_positions={int(Graha.SUN): value},
                  positions_are_longitudes=False)


def test_a_whole_number_is_still_accepted_as_a_rasi():
    for value in (5, 5.0):
        chart = build(graha_positions={int(Graha.SUN): value},
                      positions_are_longitudes=False)
        assert chart.bodies[0].rasi == R["Vi"]


def test_a_longitude_out_of_rasi_range_is_caught_by_the_range_check():
    with pytest.raises(ValueError, match="between 0 and 11"):
        build(graha_positions={int(Graha.SUN): 150.0},
              positions_are_longitudes=False)
