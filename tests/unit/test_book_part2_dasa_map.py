"""Part 2's opening — the map of dasa systems it will teach.

No calculation here. The part classifies dasa systems two ways and names the
nine it covers, and this holds that list against what is built so "Part 2 is
started" is never mistaken for "Part 2 is done".
"""
from __future__ import annotations

from hora.core.const import (
    DASA_USES_ARE_NOT_IN_THE_CLASSICS,
    DEFERRED_TO_TAJAKA,
    PART_2_DASA_SYSTEMS,
)
from hora.dasha.nakshatra.systems import NAKSHATRA_DASHA_SYSTEMS


def test_part_2_lists_nine_systems_in_the_books_order():
    names = [s["name"] for s in PART_2_DASA_SYSTEMS]
    assert names == [
        "Vimsottari dasa", "Ashtottari dasa", "Narayana dasa",
        "Lagna Kendradi Rasi dasa", "Sudasa", "Drigdasa",
        "Niryaana Shoola dasa", "Shoola dasa", "Kalachakra dasa",
    ]


def test_every_system_is_classified_both_ways():
    """The opening gives two independent classifications, so each system must
    carry a kind and a purpose."""
    for system in PART_2_DASA_SYSTEMS:
        assert system["kind"] in {"nakshatra", "rasi"}
        assert "phalita" in system["purpose"] or "ayur" in system["purpose"]


def test_six_of_the_nine_are_rasi_dasas():
    """Which is why `dasha/rasi/` not existing is the whole gap in Part 2."""
    rasi = [s["name"] for s in PART_2_DASA_SYSTEMS if s["kind"] == "rasi"]
    assert len(rasi) == 6
    nakshatra = [s["name"] for s in PART_2_DASA_SYSTEMS if s["kind"] == "nakshatra"]
    assert nakshatra == ["Vimsottari dasa", "Ashtottari dasa", "Kalachakra dasa"]


def test_vimsottari_and_ashtottari_are_ordered_oppositely():
    """The part writes Vimsottari "phalita/ayur" and Ashtottari "ayur/phalita".

    Both serve both ends, so the order of the pair is the only thing the book
    gives to separate their emphasis. Flattening either to "both" would throw
    away the distinction, so the printed order is preserved.
    """
    by_name = {s["name"]: s for s in PART_2_DASA_SYSTEMS}
    assert by_name["Vimsottari dasa"]["purpose"] == "phalita/ayur"
    assert by_name["Ashtottari dasa"]["purpose"] == "ayur/phalita"


def test_four_of_the_nine_are_built():
    """This is the coverage line for Part 2 and should fail — loudly — as each
    one lands. A nakshatra system is built when its `key` is in the service's
    registry; a rasi dasa when it names a `module` that imports.
    """
    import importlib

    built = set()
    for system in PART_2_DASA_SYSTEMS:
        if system["key"] in NAKSHATRA_DASHA_SYSTEMS:
            built.add(system["name"])
        elif system.get("module"):
            importlib.import_module(system["module"])
            built.add(system["name"])
    assert built == {"Vimsottari dasa", "Ashtottari dasa", "Narayana dasa",
                     "Lagna Kendradi Rasi dasa"}

    missing = [s["name"] for s in PART_2_DASA_SYSTEMS
               if s["key"] is None and not s.get("module")]
    assert len(missing) == 5
    assert "Kalachakra dasa" in missing      # a nakshatra dasa we do not have
    assert missing[0] == "Sudasa"            # the next one the book teaches


def test_the_engine_carries_nakshatra_systems_part_2_never_names():
    """Ten nakshatra systems are built, from JHora rather than from this part.

    Part 2 names only three of them. The other eight are not book-derived and
    the difference should stay visible rather than being read as coverage.
    """
    named = {s["key"] for s in PART_2_DASA_SYSTEMS if s["key"]}
    extra = set(NAKSHATRA_DASHA_SYSTEMS) - named
    assert len(extra) == 8
    assert "dwadasottari" in extra


def test_sudarsana_chakra_is_named_but_deferred():
    assert "Sudarsana Chakra dasa" in DEFERRED_TO_TAJAKA
    assert "Tajaka Analysis" in DEFERRED_TO_TAJAKA
    assert all(s["name"] != "Sudarsana Chakra dasa" for s in PART_2_DASA_SYSTEMS)


def test_the_classics_note_is_kept_with_the_books_typo():
    assert "astrologey" in DASA_USES_ARE_NOT_IN_THE_CLASSICS
