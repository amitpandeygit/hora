"""Section 2.3, Indications of Rasis — the transcription, character for character.

`test_rasi_indications.py` checks the *shape* of the store: that every rasi has
an entry, that categories are known, that the licence gate holds. It cannot
catch a wrong word, because it has nothing to compare against.

This file holds the twelve lists as the book prints them and asserts equality.
Two deviations were found the first time it was run — Libra's "Businessmen" had
been silently lowercased, and Aquarius's double space had been collapsed by
YAML folding. Neither would have been caught by any other test.

**Nothing here may be "tidied".** The book's own typos are part of the source:
"garrages", "uproght", "slender buils", a capital B mid-sentence, a double
space. Each is kept in `verbatim` and corrected only in the `terms` list.
"""

from __future__ import annotations

import pytest

from hora.content.store import get_store
from hora.core import const as c

#: Section 2.3 exactly as printed, rasi index to text.
SECTION_2_3 = {
    0: (
        "Dynamic, enterprising, valiant, ruddy, head, forests, large forehead, "
        "hasty, impulsive, restless, thick eyebrows, leadership, overbearing, "
        "dry, lean, tall."
    ),
    1: (
        "Beautiful, face, stable, sluggish, loyal, meadows, plains, luxury "
        "halls, dining halls, eating places, fine teeth, large eyes, luxurious, "
        "faithful, thick hair, stout."
    ),
    2: (
        "Chest, garden, communication, journalism, schools, colleges, study "
        "rooms, cables, telephone, newspapers, tall, well-built, prominent "
        "cheeks, thick hair, broad chest, curious, learned, jovial."
    ),
    3: (
        "Heart, breast, watery fields, rivers, canals, kitchen, food, "
        "attractive, small build, emotional, deeply attached, mother-like, "
        "sensitive."
    ),
    4: (
        "Stomach, digestion, navel, mountains, forests, caves, deserts, "
        "palaces, parks, forts, boilers, steel factories, thin, dry, hot, "
        "royal, self-pride, insolent, domineering."
    ),
    5: (
        "Hip, appendix, lush gardens, fields, orchards, libraries, bookstores, "
        "farms, intelligent, sharp, orator, nervous, physically weak, "
        "discretion, tactfulness."
    ),
    6: (
        "Groins, Businessmen, markets, trade centers, banks, hotels, amusement "
        "parks, entertainment, toilets, cosmetics, balanced, wise, good talker."
    ),
    7: (
        "Private parts, holes, deep caves, mines, garrages, small build, dusky "
        "complexion, bright eyes, secretive, scheming, occult, best friend or "
        "a worst enemy, peevish, sensitive."
    ),
    8: (
        "Thighs, royal, attorneys, government offices, aircraft, falling, "
        "sparse hair, muscular, deep eyes, uproght, honest, genial, gambler."
    ),
    9: (
        "Knees, marsh lands, watery places, alligators, beasts, bushes, "
        "slender buils, long neck, prominent teeth, witty, perfectionist, "
        "patient, organizer, cautious, secretive, pragmatic."
    ),
    10: (
        "Ankles, charity, philosophy, tall, bony, small eyes, mountain spring, "
        "places with water, ill-formed teeth,  coarse hair, hard-working, "
        "stoic, honest."
    ),
    11: (
        "Feet, oceans, seas, prisons, hospitals, hermitages, short, plump, "
        "large eyes, large eyebrows, lazy, emotional, timid, honest, "
        "irresolute, talkative, intuitive."
    ),
}


@pytest.fixture(scope="module")
def store():
    return get_store()


@pytest.mark.parametrize("rasi", sorted(SECTION_2_3))
def test_the_verbatim_text_matches_the_book(rasi, store):
    entries = store.get("rasi", rasi, source="pvr-vaia")
    assert entries, c.RASI_NAMES[rasi]
    assert entries[0].verbatim == SECTION_2_3[rasi], c.RASI_NAMES[rasi]


def test_all_twelve_rasis_have_an_entry():
    assert sorted(SECTION_2_3) == list(range(12))


@pytest.mark.parametrize("rasi,typo,corrected", [
    (7, "garrages", "garages"),
    (8, "uproght", "upright"),
    (9, "slender buils", "slender build"),
])
def test_the_books_typos_stay_in_verbatim_and_are_fixed_only_in_terms(
    rasi, typo, corrected, store
):
    """Three misspellings are the book's own. The transcription keeps them; the
    searchable term list carries the correction, and says so."""
    entry = store.get("rasi", rasi, source="pvr-vaia")[0]
    assert typo in entry.verbatim
    assert corrected not in entry.verbatim
    terms = [t.term for t in entry.terms]
    assert corrected in terms
    assert typo not in terms
    assert entry.transcription_notes and typo in entry.transcription_notes


def test_libras_capital_b_is_the_books_own(store):
    """"Groins, Businessmen, markets" — the book capitalises it mid-list. It
    had been silently lowercased; this is why that is now pinned."""
    entry = store.get("rasi", 6, source="pvr-vaia")[0]
    assert "Businessmen" in entry.verbatim
    assert "businessmen" not in entry.verbatim
    assert entry.transcription_notes and "capitalises" in entry.transcription_notes


def test_aquarius_keeps_the_books_double_space(store):
    """A plain YAML folded scalar collapses runs of whitespace, so this entry
    is stored as a quoted scalar. If someone re-dumps the file with default
    styles, this test fails rather than the space vanishing unnoticed."""
    entry = store.get("rasi", 10, source="pvr-vaia")[0]
    assert "teeth,  coarse hair" in entry.verbatim
    assert entry.transcription_notes and "double space" in entry.transcription_notes


@pytest.mark.parametrize("rasi", sorted(SECTION_2_3))
def test_the_2_2_1_limb_appears_in_the_2_3_list(rasi, store):
    """§2.2.1 assigns each rasi a limb; §2.3 repeats body parts inside the
    indication lists. They agree for ten of the twelve.

    The two that do not are **Gemini** (2.2.1 "arms", 2.3 "chest") and
    **Libra** (2.2.1 "space below navel", 2.3 "groins") — which is exactly
    D-3, found independently here. Asserting the ten and naming the two keeps
    D-3 from silently growing a third member.

    The limb is not always first: Aries opens with "Dynamic" and has "head"
    fifth, Taurus opens with "Beautiful" and has "face" second.
    """
    entry = store.get("rasi", rasi, source="pvr-vaia")[0]
    parts = [p.strip().rstrip(".").lower() for p in entry.verbatim.split(",")]
    limb = c.RASI_LIMB[rasi].lower()
    d3 = {2: "chest", 6: "groins"}
    if rasi in d3:
        assert limb not in parts, "D-3 says these two disagree"
        assert d3[rasi] in parts
    else:
        assert limb in parts, (c.RASI_NAMES[rasi], limb)


def test_d3_covers_exactly_gemini_and_libra(store):
    """The deviation is two signs wide. If a third ever drifts, this fails
    rather than D-3 quietly becoming incomplete."""
    disagree = []
    for rasi in range(12):
        entry = store.get("rasi", rasi, source="pvr-vaia")[0]
        parts = [p.strip().rstrip(".").lower() for p in entry.verbatim.split(",")]
        if c.RASI_LIMB[rasi].lower() not in parts:
            disagree.append(c.RASI_NAMES[rasi])
    assert disagree == ["Gemini", "Libra"]


def test_every_entry_is_licence_gated(store):
    """Section 2.3 is PVR's own prose. It is stored, not served, until the
    licence is settled — OI-12."""
    for rasi in range(12):
        assert store.get("rasi", rasi, source="pvr-vaia")[0].licence_status == (
            "unconfirmed"
        )


def test_every_indication_appears_in_the_term_list(store):
    """The term list is the searchable decomposition of the verbatim text.
    Every comma-separated indication must be represented, allowing for the
    three corrected typos."""
    corrections = {"garrages": "garages", "uproght": "upright",
                   "slender buils": "slender build"}
    for rasi in range(12):
        entry = store.get("rasi", rasi, source="pvr-vaia")[0]
        parts = [p.strip().rstrip(".") for p in entry.verbatim.split(",")]
        terms = {t.term.lower() for t in entry.terms}
        for part in parts:
            expected = corrections.get(part, part).lower()
            assert expected in terms, (c.RASI_NAMES[rasi], part)
        assert len(entry.terms) == len(parts), c.RASI_NAMES[rasi]
