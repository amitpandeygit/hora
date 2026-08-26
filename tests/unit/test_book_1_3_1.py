"""§1.3.1 Grahas (planets) — the section that names what a chart is made of.

Nine planets, eleven upagrahas, the lagna and the special ascendants. Every
count and every definition here is stated outright in the section, so each is
pinned rather than left implicit in a table's length.

Added when the user reviewed §1.3.1 against the code and found the shadow-planet
vocabulary unreachable. Five of the section's statements were missing
altogether; see docs/open-items.md OI-31 and OI-32.
"""
import pytest

from hora.core import const as c
from hora.services import reference_service

# --------------------------------------------------------------------------
# What a graha is
# --------------------------------------------------------------------------

def test_the_definition_of_graha_is_stored():
    """"a graha or a planet is a body that has considerable influence on the
    living beings on earth"."""
    assert "considerable influence on the living beings on earth" in c.GRAHA_DEFINITION


def test_the_definition_says_why_it_is_not_the_astronomical_sense():
    """The Sun is a star and the Moon a satellite; both are grahas."""
    note = c.GRAHA_DEFINITION_NOTE
    assert "slightly different sense" in note
    assert "Distant stars have negligible influence" in note


# --------------------------------------------------------------------------
# Nine planets
# --------------------------------------------------------------------------

def test_seven_classical_planets_plus_two_nodes():
    """"Seven planets are considered in Indian astrology... In addition, two
    'chaayaa grahas' (shadow planets)... Rahu and Ketu"."""
    assert len(c.CLASSICAL_SEVEN) == 7
    assert len(c.NAVAGRAHA) == 9
    assert set(c.CHAAYAA_GRAHAS) == {int(c.Graha.RAHU), int(c.Graha.KETU)}
    assert set(c.NAVAGRAHA) == set(c.CLASSICAL_SEVEN) | set(c.CHAAYAA_GRAHAS)


@pytest.mark.parametrize("graha,aliases", [
    (c.Graha.RAHU, ["north node", "head of dragon"]),
    (c.Graha.KETU, ["south node", "tail of dragon"]),
])
def test_the_nodes_other_names(graha, aliases):
    """"These are also called 'the north node' and 'the south node'
    respectively (or the head and tail of dragon)"."""
    assert c.NODE_ALIASES[int(graha)] == aliases


def test_the_nodes_are_recorded_as_mathematical_points():
    """"Rahu and Ketu are not real planets; they are just some mathematical
    points."

    Worth storing rather than implying: it is the reason the nodes have no
    deep-exaltation degree in Table 6, no combustion, and no disc.
    """
    assert "not real planets" in c.NODES_ARE_MATHEMATICAL_POINTS
    assert "mathematical points" in c.NODES_ARE_MATHEMATICAL_POINTS
    # The absences that follow from it.
    assert int(c.Graha.RAHU) not in c.EXALTATION_DEG
    assert int(c.Graha.KETU) not in c.EXALTATION_DEG


# --------------------------------------------------------------------------
# Eleven upagrahas
# --------------------------------------------------------------------------

def test_there_are_exactly_eleven_upagrahas():
    """"there are 11 moving mathematical points known as Upagrahas"."""
    assert c.UPAGRAHA_COUNT == 11
    assert len(c.UPAGRAHA_NAMES) == c.UPAGRAHA_COUNT
    assert len(c.SUN_BASED_UPAGRAHAS) + len(c.TIME_BASED_UPAGRAHAS) == 11


def test_the_two_upagraha_families_do_not_overlap():
    assert not set(c.SUN_BASED_UPAGRAHAS) & set(c.TIME_BASED_UPAGRAHAS)


def test_the_upagraha_gloss_is_stored():
    """"(sub-planets or satellites)"."""
    assert c.UPAGRAHA_GLOSS == "sub-planets or satellites"
    assert c.UPAGRAHA_DEFINITION == "moving mathematical points"


# --------------------------------------------------------------------------
# Lagna and the special ascendants
# --------------------------------------------------------------------------

def test_the_definition_of_lagna_is_stored():
    """"the point that rises on the eastern horizon as the earth rotates
    around itself"."""
    assert "rises on the eastern horizon" in c.LAGNA_DEFINITION
    assert "as the earth rotates around itself" in c.LAGNA_DEFINITION


def test_special_ascendants_are_named_and_implemented():
    """§1.3.1 names the class; chapter 5 defines its members."""
    from hora.charts.special_lagna import SPECIAL_LAGNA_NAMES

    assert c.SPECIAL_ASCENDANT_TERM == "special ascendants"
    assert SPECIAL_LAGNA_NAMES == [
        "Bhaava Lagna", "Hora Lagna", "Ghati Lagna", "Sree Lagna"
    ]


# --------------------------------------------------------------------------
# All of it reaches the API
# --------------------------------------------------------------------------

def test_every_section_1_3_1_term_is_published():
    """The failure that started this: defined, registered, unreachable."""
    terms = reference_service.terms()
    assert terms["graha"]["definition"] == c.GRAHA_DEFINITION
    assert terms["graha"]["count"] == 9
    assert terms["graha"]["classical_count"] == 7
    assert terms["nodes"]["are_mathematical_points"] == c.NODES_ARE_MATHEMATICAL_POINTS
    assert terms["upagraha"]["count"] == 11
    assert terms["upagraha"]["gloss"] == c.UPAGRAHA_GLOSS
    assert terms["lagna"]["definition"] == c.LAGNA_DEFINITION
    assert terms["lagna"]["special_ascendants_term"] == c.SPECIAL_ASCENDANT_TERM


def test_the_shadow_planet_vocabulary_reaches_the_graha_table():
    rows = {r["name"]: r for r in reference_service.graha_table()["grahas"]}
    assert rows["Rahu"]["is_chaayaa_graha"] is True
    assert rows["Sun"]["is_chaayaa_graha"] is False
    assert rows["Ketu"]["aliases"] == ["south node", "tail of dragon"]
    assert rows["Sun"]["aliases"] == []
