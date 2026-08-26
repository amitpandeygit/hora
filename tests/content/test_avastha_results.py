"""§15.4.4's per-graha results — structure, resolution and licence gating.

These are **not life stages.** A sayanaadi avastha is one natal state per
planet, fixed by section 15.4.4's formula. Each entry answers "what does this
planet give while it is in this state", keyed by (avastha, graha).

The transcription is checked against the screenshots the user supplied, so a
failure in the verbatim tests means the data drifted from the book.
"""
import pytest

from hora.content import get_store
from hora.content.resolve import Placement, resolve
from hora.services import strength_service

GRAHA_NAMES = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
               "Rahu", "Ketu"]

#: All twelve are transcribed: 12 x 9 = 108 entries.
TRANSCRIBED = tuple(range(1, 13))


@pytest.fixture(scope="module")
def store():
    return get_store()


# --------------------------------------------------------------------------
# Coverage and shape
# --------------------------------------------------------------------------

@pytest.mark.parametrize("avastha", TRANSCRIBED)
@pytest.mark.parametrize("graha", range(9))
def test_every_transcribed_pair_has_exactly_one_entry(avastha, graha, store):
    entries = store.get("avastha", avastha, qualifier=graha)
    assert len(entries) == 1, (avastha, graha)
    assert entries[0].qualifier_name == GRAHA_NAMES[graha]


def test_all_one_hundred_and_eight_pairs_are_present(store):
    """12 avasthas x 9 grahas, with no gap and no duplicate."""
    total = sum(
        len(store.get("avastha", a, qualifier=g))
        for a in range(1, 13) for g in range(9)
    )
    assert total == 108
    for avastha in range(1, 13):
        for graha in range(9):
            assert len(store.get("avastha", avastha, qualifier=graha)) == 1, (
                avastha, graha
            )


def test_an_untranscribed_pair_would_say_so_rather_than_return_nothing():
    """Guards the branch even though nothing hits it now.

    An empty result must never read as "this planet gives nothing" if the
    table is ever extended or split.
    """
    from hora.content.store import ContentStore

    empty = ContentStore(sources={}, entries={}, categorisation_notes={})
    from hora import content

    original = content.get_store
    content.get_store = lambda: empty
    try:
        missing = strength_service.activity_results(12, 0)
    finally:
        content.get_store = original
    assert missing["available"] is False
    assert "partial" in missing["note"]
    assert missing["results"] == []


@pytest.mark.parametrize("avastha", TRANSCRIBED)
@pytest.mark.parametrize("graha", range(9))
def test_every_entry_has_at_least_one_result_clause(avastha, graha, store):
    entry = store.get("avastha", avastha, qualifier=graha)[0]
    assert entry.results, (avastha, graha)
    assert entry.verbatim.strip()


@pytest.mark.parametrize("avastha", TRANSCRIBED)
@pytest.mark.parametrize("graha", range(9))
def test_every_clause_comes_from_its_own_verbatim(avastha, graha, store):
    """A clause we split out must be text the book actually printed there."""
    entry = store.get("avastha", avastha, qualifier=graha)[0]
    for result in entry.results:
        assert result.text in entry.verbatim, (avastha, graha, result.text)


# --------------------------------------------------------------------------
# The book's own wording, from the screenshots
# --------------------------------------------------------------------------

@pytest.mark.parametrize("avastha,graha,verbatim", [
    (1, 0, "Digestive troubles, diseases, stout legs, bile, piles, heart troubles."),
    (1, 3, ("Addicted to pleasures, licentious, wicked, always hungry; "
            "[in lagna] lame, eyes like a bee.")),
    (1, 7, "Many miseries; [in Ar, Ta, Ge, Vi] wealth."),
    (2, 3, ("[in lagna] good character; [conjoined/aspected by malefics] poor; "
            "[conjoined/aspected by benefics] wealthy and happy.")),
    (3, 2, "[in lagna] penury; [elsewhere] ruler of a town."),
    (3, 5, ("[in lagna, 7th or 10th] troubles to eyes and loss of wealth; "
            "[else] large house.")),
    (4, 2, ("Virtuous and honored by kings; [in 5th] loss of children; "
            "[in 5th with Rahu] faces a severe fall.")),
    (5, 1, "[if waning] sinful, cruel, eye troubles; [if waxing] troubled by fear."),
])
def test_verbatim_matches_the_screenshots(avastha, graha, verbatim, store):
    assert store.get("avastha", avastha, qualifier=graha)[0].verbatim == verbatim


@pytest.mark.parametrize("avastha,graha,typo", [
    (1, 6, "dieases"),      # Saturn in Sayana
    (4, 7, "welthy"),       # Rahu in Prakaasana
    (8, 3, "daugher"),      # Mercury in Aagama
    (9, 5, "dieases"),      # Venus in Bhojana
    (10, 0, "reverred"),    # Sun in Nrityalipsaa
    (10, 2, "though"),      # Mars in Nrityalipsaa — "through" intended
    (9, 2, "means acts"),   # Mars in Bhojana — "mean acts" intended
])
def test_the_authors_typos_are_kept(avastha, graha, typo, store):
    """Silently correcting these is what D-18's discipline exists to stop."""
    entry = store.get("avastha", avastha, qualifier=graha)[0]
    assert typo in entry.verbatim
    assert entry.transcription_notes and typo in entry.transcription_notes


def test_jupiter_in_upavesana_keeps_its_repeated_word(store):
    """The printed line says "ulcers on feet, hands, feet"."""
    entry = store.get("avastha", 2, qualifier=4)[0]
    assert "feet, hands, feet" in entry.verbatim
    assert entry.transcription_notes


# --------------------------------------------------------------------------
# Resolving conditions
# --------------------------------------------------------------------------

def test_an_unconditional_clause_always_applies(store):
    entry = store.get("avastha", 1, qualifier=0)[0]
    resolved = resolve(entry, Placement())
    assert len(resolved) == 1
    assert resolved[0].applies is True
    assert resolved[0].conditional is False


def test_a_house_condition_fires_only_in_that_house(store):
    entry = store.get("avastha", 1, qualifier=3)[0]      # Mercury, [in lagna]
    in_lagna = {r.text: r.applies for r in resolve(entry, Placement(house=1))}
    assert in_lagna["lame, eyes like a bee"] is True
    elsewhere = {r.text: r.applies for r in resolve(entry, Placement(house=4))}
    assert elsewhere["lame, eyes like a bee"] is False


def test_a_rasi_condition_fires_only_in_those_rasis(store):
    entry = store.get("avastha", 1, qualifier=7)[0]      # Rahu, [in Ar,Ta,Ge,Vi]
    for rasi, expected in ((0, True), (1, True), (2, True), (5, True), (3, False)):
        got = {r.text: r.applies for r in resolve(entry, Placement(rasi=rasi))}
        assert got["wealth"] is expected, rasi


def test_a_compound_condition_needs_both_parts(store):
    """"[in 5th with Rahu]" needs the house and the conjunction."""
    entry = store.get("avastha", 4, qualifier=2)[0]
    fall = "faces a severe fall"
    both = {r.text: r.applies for r in resolve(
        entry, Placement(house=5, joined_by=frozenset({7})))}
    assert both[fall] is True
    house_only = {r.text: r.applies for r in resolve(entry, Placement(house=5))}
    assert house_only[fall] is False


def test_moon_phase_conditions_are_exclusive(store):
    entry = store.get("avastha", 5, qualifier=1)[0]
    waning = {r.text: r.applies for r in resolve(
        entry, Placement(moon_phase="waning"))}
    assert waning["sinful, cruel, eye troubles"] is True
    assert waning["troubled by fear"] is False


def test_a_missing_input_is_undetermined_not_false(store):
    """The whole point: silence must not read as "this does not apply"."""
    entry = store.get("avastha", 1, qualifier=3)[0]
    got = {r.text: r.applies for r in resolve(entry, Placement())}
    assert got["lame, eyes like a bee"] is None


def test_an_aspect_condition_stays_undetermined_without_aspect_data(store):
    """We do not compute aspects — OI-18."""
    entry = store.get("avastha", 2, qualifier=3)[0]
    got = {r.text: (r.applies, r.reason) for r in resolve(entry, Placement(house=4))}
    applies, reason = got["poor"]
    assert applies is None
    assert "OI-18" in reason


def test_the_else_branch_fires_only_when_no_sibling_does(store):
    entry = store.get("avastha", 3, qualifier=2)[0]      # Mars: [in lagna] / [elsewhere]
    in_lagna = {r.text: r.applies for r in resolve(entry, Placement(house=1))}
    assert in_lagna["penury"] is True
    assert in_lagna["ruler of a town"] is False
    elsewhere = {r.text: r.applies for r in resolve(entry, Placement(house=9))}
    assert elsewhere["penury"] is False
    assert elsewhere["ruler of a town"] is True


def test_the_else_branch_is_undetermined_when_a_sibling_is(store):
    """We cannot know the fallback applies until we know the others do not."""
    entry = store.get("avastha", 3, qualifier=5)[0]      # Venus
    got = {r.text: r.applies for r in resolve(entry, Placement())}
    assert got["troubles to eyes and loss of wealth"] is None
    assert got["large house"] is None


# --------------------------------------------------------------------------
# Licence gating
# --------------------------------------------------------------------------

def test_the_text_is_withheld_but_the_structure_is_not():
    """Which clauses apply is calculation. The wording is the author's."""
    payload = strength_service.activity_results(4, 2, house=5, joined_by=[7])
    assert payload["text_withheld"] is True
    assert payload["verbatim"] is None
    assert all(r["text"] is None for r in payload["results"])
    # The structure still answers the question.
    assert payload["applies_count"] == 3
    assert payload["undetermined_count"] == 0
    assert all(r["reason"] for r in payload["results"])


def test_every_avastha_entry_is_licence_unconfirmed(store):
    for avastha in TRANSCRIBED:
        for graha in range(9):
            entry = store.get("avastha", avastha, qualifier=graha)[0]
            assert entry.licence_status == "unconfirmed"
            assert not entry.servable



# --------------------------------------------------------------------------
# Condition types that only the later avasthas use
# --------------------------------------------------------------------------

def test_trines_are_read_as_the_first_fifth_and_ninth(store):
    """Mars in Sabhaa: "[in trines] unlearned"."""
    entry = store.get("avastha", 7, qualifier=2)[0]
    clause = next(r for r in entry.results if r.text == "unlearned")
    assert clause.condition.houses == (1, 5, 9)


def test_a_negative_conjunction_condition_resolves(store):
    """Moon in Nidraa: "[if with Jupiter]" versus "[without Jupiter]"."""
    entry = store.get("avastha", 12, qualifier=1)[0]
    with_jupiter = {r.text: r.applies for r in resolve(
        entry, Placement(joined_by=frozenset({4})))}
    assert with_jupiter["eminent"] is True
    assert with_jupiter["loses wealth on females, troubles"] is False
    without = {r.text: r.applies for r in resolve(
        entry, Placement(joined_by=frozenset()))}
    assert without["eminent"] is False
    assert without["loses wealth on females, troubles"] is True


def test_a_malefic_rasi_condition_resolves(store):
    """Mercury in Nrityalipsaa: "[in a malefic rasi]"."""
    entry = store.get("avastha", 10, qualifier=3)[0]
    clause = "licentious, goes to prostitutes"
    malefic = {r.text: r.applies for r in resolve(
        entry, Placement(rasi_lord="malefic"))}
    assert malefic[clause] is True
    benefic = {r.text: r.applies for r in resolve(
        entry, Placement(rasi_lord="benefic"))}
    assert benefic[clause] is False
    unknown = {r.text: r.applies for r in resolve(entry, Placement())}
    assert unknown[clause] is None


def test_strong_and_weak_conditions_are_undetermined_by_design(store):
    """Mars in Bhojana: "[if strong] / [if weak]".

    No measure in this book settles strength — shadbala is out of scope and
    the simple rules are not transcribed. Both clauses must therefore come
    back undetermined, with the reason pointing at the measures endpoint.
    """
    entry = store.get("avastha", 9, qualifier=2)[0]
    resolved = {r.text: (r.applies, r.reason) for r in resolve(entry, Placement())}
    for text in ("sweet food", "means acts, dishonorable"):
        applies, reason = resolved[text]
        assert applies is None, text
        assert "/v1/strength/measures" in reason


def test_a_debilitation_condition_resolves(store):
    """Venus in Bhojana: "[debilitated] ... ; [else] ..."."""
    entry = store.get("avastha", 9, qualifier=5)[0]
    debilitated = {r.text: r.applies for r in resolve(
        entry, Placement(dignity="debilitated"))}
    assert debilitated["wealthy, respected by scholars"] is True
    assert debilitated[
        "Distressed due to hunger, dieases, fear from enemies"] is False


def test_mercury_reads_the_same_in_gamana_and_aagamana(store):
    """The book prints the identical line for both. Not a transcription slip."""
    gamana = store.get("avastha", 5, qualifier=3)[0]
    aagamana = store.get("avastha", 6, qualifier=3)[0]
    assert gamana.verbatim == aagamana.verbatim
    assert aagamana.transcription_notes and "Gamana" in aagamana.transcription_notes


def test_the_tenth_avastha_is_stored_under_both_spellings(store):
    """D-20. Table 36 prints "Nriyalipsaa"; the results heading prints
    "Nrityalipsaa". Both are the author's."""
    from hora.core.const import SAYANAADI_AVASTHAS

    assert SAYANAADI_AVASTHAS[10]["name"] == "Nriyalipsaa"
    assert "Nrityalipsaa" in SAYANAADI_AVASTHAS[10]["aliases"]
    assert store.get("avastha", 10, qualifier=0)[0].subject_name == "Nrityalipsaa"
