"""Chapter 26 — transits: miscellaneous topics.

§26.1 sets out two threads, rasi principles chapter 25 left and nakshatra
interactions it never touched, and names not one of them. The last test here
is the coverage line, and it stays failing-by-omission until the chapter's own
sections arrive: nothing is built ahead of a page.
"""
from __future__ import annotations

from hora.core.const import RASI_ABBR

A = list(RASI_ABBR)
R = {abbr: index for index, abbr in enumerate(RASI_ABBR)}


def test_26_1_names_chapter_25_by_its_own_title():
    """"In the chapter "Transits and Natal References", we concentrated on
    correlating the natal chart and the transit chart using the rasis."
    """
    from hora.core.const import CHAPTER_26_LOOKS_BACK_AT_25

    assert "Transits and Natal References" in CHAPTER_26_LOOKS_BACK_AT_25
    assert "using the rasis" in CHAPTER_26_LOOKS_BACK_AT_25
    assert "haven't yet covered" in CHAPTER_26_LOOKS_BACK_AT_25


def test_26_1_sets_out_two_threads_and_names_no_principle():
    from hora.core.const import (
        CHAPTER_26_NAMES_NOTHING_IT_WILL_COVER,
        CHAPTER_26_THREADS,
        PART_3_IS_KNOWINGLY_PARTIAL,
    )

    assert len(CHAPTER_26_THREADS) == 2
    assert [t["thread"] for t in CHAPTER_26_THREADS] == [
        "rasi transits", "nakshatra transits"]
    assert CHAPTER_26_THREADS[0]["scope"] == "a couple of concepts"
    assert CHAPTER_26_THREADS[1]["scope"] == "a few principles"
    assert "names none of them" in CHAPTER_26_NAMES_NOTHING_IT_WILL_COVER
    assert "Some of those techniques" in PART_3_IS_KNOWINGLY_PARTIAL


def test_nakshatras_are_put_level_with_rasis():
    from hora.core.const import NAKSHATRAS_ARE_AS_IMPORTANT_AS_RASIS

    assert "as important as rasis" in NAKSHATRAS_ARE_AS_IMPORTANT_AS_RASIS
    assert "natal and transit charts" in NAKSHATRAS_ARE_AS_IMPORTANT_AS_RASIS


def test_chapter_25_correlated_by_rasi_throughout():
    """The claim §26.1 makes about chapter 25, checked against what chapter 25
    actually built rather than taken on trust.
    """
    from hora.core.const import CHAPTER_26_IS_THE_FIRST_TO_PAIR_NAKSHATRAS
    from hora.transits import gochara

    # every chapter 25 entry point takes or returns rasis, not nakshatras
    for name in ("janma_rasi", "house_from_janma", "houses_from_janma",
                 "transit_result", "read_transits", "influenced_rasis",
                 "influences", "transits_over", "divisional_interaction"):
        assert callable(getattr(gochara, name))
    # only §25.6 produces a nakshatra anywhere in chapter 25
    callables = {name for name in dir(gochara)
                 if "nakshatra" in name.lower()
                 and callable(getattr(gochara, name))}
    assert callables == {"timing_nakshatra", "companion_nakshatras"}

    # and it comes from a product, not from a graha's own nakshatra
    got = gochara.timing_nakshatra(430)
    assert got["nakshatra"] == "Purva Bhadrapada"
    assert got["product"] == 430
    assert "times a sodhya pinda" in (
        CHAPTER_26_IS_THE_FIRST_TO_PAIR_NAKSHATRAS)


def test_nothing_of_chapter_26_is_built_yet():
    """The coverage line. §26.1 is prose; the first section with a rule has
    not been supplied, and no module is created ahead of one.
    """
    import importlib

    for module in ("hora.transits.nakshatra", "hora.transits.misc"):
        try:
            importlib.import_module(module)
        except ModuleNotFoundError:
            continue
        raise AssertionError(f"{module} exists before its section arrived")
