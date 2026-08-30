"""Chapter 15 — avasthas and the comparison of two planets' strength.

Built from §15.4's tables and §15.1's prose. The four worked examples under
Table 35 are the fixtures.

This chapter exists in the codebase because §9.2 is blocked on it: "we have to
take the stronger of Mars and Ketu as the lord of Scorpio". What it does *not*
do is unblock that cleanly — see
:func:`test_comparison_always_carries_the_caveat`.
"""
from itertools import pairwise

import pytest

from hora.charts.avastha import (
    AvasthaError,
    all_avasthas,
    avastha_by_age,
    avastha_by_alertness,
    avasthas_by_mood,
)
from hora.charts.strength import AGE_RANK, StrengthError, compare, stronger
from hora.core.const import (
    ADDITIONAL_MOOD_AVASTHAS,
    AGE_AVASTHAS,
    ALERTNESS_AVASTHAS,
    MOOD_AVASTHAS,
    STRENGTH_MEASURES,
    Graha,
)
from hora.core.ephemeris.base import PlanetPosition
from hora.services import arudha_service, strength_service

ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]


def lon(degrees: float, rasi: str) -> float:
    return ABBR.index(rasi) * 30 + degrees


def positions(longitudes: dict[int, float]) -> dict[int, PlanetPosition]:
    """A chart from bare longitudes.

    Every graha whose rasi lord matters must be present, so callers that only
    care about one planet still supply the seven classical lords.
    """
    return {
        graha: PlanetPosition(graha, value, 0.0, 0.0, 0.0, 0.0, 0.0)
        for graha, value in longitudes.items()
    }


#: A background chart with every graha placed, so a rasi lord is always
#: available. Individual tests override the graha they are testing.
def chart(**overrides: float) -> dict[int, PlanetPosition]:
    base = {
        int(Graha.SUN): lon(1, "Ar"), int(Graha.MOON): lon(1, "Ta"),
        int(Graha.MARS): lon(1, "Ge"), int(Graha.MERCURY): lon(1, "Cn"),
        int(Graha.JUPITER): lon(1, "Le"), int(Graha.VENUS): lon(1, "Vi"),
        int(Graha.SATURN): lon(1, "Li"), int(Graha.RAHU): lon(1, "Sc"),
        int(Graha.KETU): lon(1, "Sg"),
    }
    base.update({int(getattr(Graha, k.upper())): v for k, v in overrides.items()})
    return positions(base)


# --------------------------------------------------------------------------
# 15.4.1 — Table 35, and the four examples printed under it
# --------------------------------------------------------------------------

@pytest.mark.parametrize("degrees,rasi,name,results", [
    (23, "Cn", "Kumaara", "Half"),      # "A planet at 23 deg in Cn ... half"
    (19, "Li", "Vriddha", "Some"),      # "... 19 deg in Li ... not very effective"
    (14, "Sg", "Yuva", "Full"),         # "... 14 deg in Sg ... all of its results"
    (27, "Pi", "Saisava", "Quarter"),   # "... 27 deg in Pi ... one quarter"
])
def test_the_four_worked_age_examples(degrees, rasi, name, results):
    state = avastha_by_age(lon(degrees, rasi))
    assert state.name == name
    assert state.results == results


def test_odd_and_even_rasis_run_the_bands_in_opposite_directions():
    """The whole point of Table 35's two columns."""
    assert avastha_by_age(lon(3, "Ar")).name == "Saisava"   # odd, first band
    assert avastha_by_age(lon(3, "Ta")).name == "Mrita"     # even, last band


@pytest.mark.parametrize("rasi", ["Ar", "Ta"])
def test_the_age_bands_tile_the_whole_rasi(rasi):
    """No degree may fall in a gap, and no two bands may overlap."""
    seen = [avastha_by_age(lon(d / 10, rasi)).name for d in range(300)]
    runs = [seen[0]] + [b for a, b in pairwise(seen) if a != b]
    assert len(runs) == 5, runs
    assert len(set(runs)) == 5, runs


def test_vriddha_has_no_fraction_because_the_book_gives_none():
    """Its result is "Some". Assigning 0.75 would be inventing a number."""
    by_name = {r["name"]: r for r in AGE_AVASTHAS}
    assert by_name["Vriddha"]["results"] == "Some"
    assert by_name["Vriddha"]["fraction"] is None
    assert by_name["Yuva"]["fraction"] == 1.0
    assert by_name["Mrita"]["fraction"] == 0.0
    assert avastha_by_age(lon(19, "Li")).fraction is None


def test_vriddha_is_not_ranked_for_comparison():
    """Unquantified means unrankable, not middling."""
    assert "Vriddha" not in AGE_RANK
    assert set(AGE_RANK) == {"Yuva", "Kumaara", "Saisava", "Mrita"}


def test_age_avastha_carries_the_chapters_caution():
    longitudes = {g: p.longitude for g, p in chart(sun=lon(14, "Sg")).items()}
    payload = strength_service.avasthas(Graha.SUN, longitudes)
    assert "child prodigies" in payload["age"]["caution"]
    assert "just one of the factors" in payload["age"]["caution"]


# --------------------------------------------------------------------------
# 15.4.2 — the three alertness states
# --------------------------------------------------------------------------

def test_alertness_has_exactly_three_states():
    assert [r["name"] for r in ALERTNESS_AVASTHAS] == [
        "Jaagrita", "Swapna", "Sushupta"
    ]
    assert [r["results"] for r in ALERTNESS_AVASTHAS] == [
        "full", "medium", "negligible"
    ]


def test_exalted_planet_is_awake():
    """Sun exalts in Aries."""
    pos = chart(sun=lon(10, "Ar"))
    assert avastha_by_alertness(Graha.SUN, pos).name == "Jaagrita"


def test_debilitated_planet_is_asleep():
    """Sun debilitates in Libra."""
    pos = chart(sun=lon(10, "Li"))
    assert avastha_by_alertness(Graha.SUN, pos).name == "Sushupta"


def test_moolatrikona_counts_as_an_own_rasi():
    """"in its exaltation rasi or an own rasi" — a moolatrikona rasi is owned."""
    pos = chart(sun=lon(5, "Le"))
    state = avastha_by_alertness(Graha.SUN, pos)
    assert state.name == "Jaagrita"
    assert state.basis in ("own", "moolatrikona")


# --------------------------------------------------------------------------
# 15.4.3 — mood states are a set, not a winner
# --------------------------------------------------------------------------

def test_mood_states_are_not_mutually_exclusive():
    """A planet can be exalted and joined by malefics at once."""
    pos = chart(sun=lon(10, "Ar"), saturn=lon(12, "Ar"))
    applying = {m.name for m in avasthas_by_mood(Graha.SUN, pos) if m.applies}
    assert "Deepta" in applying
    assert "Vikala" in applying


def test_there_are_nine_mood_states_and_six_additional():
    assert len(MOOD_AVASTHAS) == 9
    assert len(ADDITIONAL_MOOD_AVASTHAS) == 6


def test_states_needing_aspects_are_undetermined_not_false():
    """The engine has no aspects (OI-18). Silence must not read as "no"."""
    pos = chart(sun=lon(10, "Ar"), mars=lon(2, "Ta"))
    mood = {m.name: m for m in avasthas_by_mood(Graha.MARS, pos)}
    for name in ("Trishita", "Kshobhita"):
        assert mood[name].applies is None, name
        assert "aspect" in mood[name].reason


def test_lajjita_is_undetermined_without_the_house():
    pos = chart(sun=lon(10, "Ar"), mars=lon(12, "Ar"))
    mood = {m.name: m for m in avasthas_by_mood(Graha.MARS, pos)}
    assert mood["Lajjita"].applies is None
    assert "house" in mood["Lajjita"].reason


def test_lajjita_applies_in_the_fifth_with_one_of_the_five():
    pos = chart(sun=lon(10, "Ar"), jupiter=lon(12, "Ar"))
    mood = {m.name: m for m in avasthas_by_mood(Graha.JUPITER, pos, house=5)}
    assert mood["Lajjita"].applies is True
    mood = {m.name: m for m in avasthas_by_mood(Graha.JUPITER, pos, house=4)}
    assert mood["Lajjita"].applies is False


def test_kopita_says_that_closely_is_unquantified():
    """The book gives no orb for "joined closely by Sun"."""
    pos = chart(sun=lon(2, "Ar"), mars=lon(28, "Ar"))
    mood = {m.name: m for m in avasthas_by_mood(Graha.MARS, pos)}
    assert mood["Kopita"].applies is True
    assert "does not quantify" in mood["Kopita"].reason
    # With an orb supplied, 26 degrees apart is not close.
    mood = {m.name: m for m in avasthas_by_mood(Graha.MARS, pos, close_orb=10.0)}
    assert mood["Kopita"].applies is False


# --------------------------------------------------------------------------
# Comparing two planets — what section 9.2 needs
# --------------------------------------------------------------------------

def test_comparison_reports_each_axis_separately():
    pos = chart(mars=lon(23, "Cn"), ketu=lon(5, "Ar"))
    result = compare(Graha.MARS, Graha.KETU, pos)
    assert {ax.axis for ax in result.axes} == {"age", "alertness"}


def test_disagreeing_axes_produce_no_winner():
    """Two measures pointing opposite ways is not a tie to be broken by fiat."""
    pos = chart(mars=lon(23, "Cn"), ketu=lon(5, "Ar"))
    result = compare(Graha.MARS, Graha.KETU, pos)
    assert result.winner is None
    assert not result.determined
    assert "disagree" in result.reason
    assert stronger(Graha.MARS, Graha.KETU, pos) is None


def test_agreeing_axes_produce_a_winner():
    pos = chart(sun=lon(14, "Ar"), saturn=lon(27, "Ar"))
    result = compare(Graha.SUN, Graha.SATURN, pos)
    assert result.winner == int(Graha.SUN)
    assert result.determined


def test_comparison_always_carries_the_caveat():
    """The measure the book nominates for this is not available.

    A verdict without that attached would read as the book's answer. It is not.
    """
    pos = chart(sun=lon(14, "Ar"), saturn=lon(27, "Ar"))
    result = compare(Graha.SUN, Graha.SATURN, pos)
    assert "shadbala" in result.caveat
    assert "beyond the scope" in result.caveat
    assert "evidence, not" in result.caveat


def test_a_graha_cannot_be_compared_with_itself():
    pos = chart(sun=lon(14, "Ar"))
    with pytest.raises(StrengthError):
        compare(Graha.SUN, Graha.SUN, pos)


def test_missing_position_is_an_error_not_a_default():
    pos = chart(sun=lon(14, "Ar"))
    del pos[int(Graha.MARS)]
    with pytest.raises(StrengthError, match="Mars"):
        compare(Graha.SUN, Graha.MARS, pos)
    with pytest.raises(AvasthaError, match="Mars"):
        all_avasthas(Graha.MARS, pos)


def test_a_missing_rasi_lord_is_named_rather_than_crashing():
    """Alertness and mood both need the lord of the occupied rasi."""
    pos = chart(mars=lon(23, "Cn"))
    del pos[int(Graha.MOON)]                      # Cancer's lord
    with pytest.raises(AvasthaError, match="Moon"):
        all_avasthas(Graha.MARS, pos)


# --------------------------------------------------------------------------
# The five measures, and what feeding this into arudhas actually gives
# --------------------------------------------------------------------------

def test_three_of_the_five_measures_are_available():
    """§15.2 names five ways of measuring strength. Three are built.

    The flags were written when only avasthas existed and went stale as
    chapters 12 and 15.5 landed — a real chart run surfaced it. Each flag is
    checked against the code that would provide it, so the next drift shows.
    """
    by_key = {m["key"]: m for m in STRENGTH_MEASURES}
    assert set(by_key) == {
        "shadbala", "ashtakavarga", "avastha", "vimsopaka", "simple_rules"
    }
    for key in ("avastha", "ashtakavarga", "simple_rules"):
        assert by_key[key]["available"] is True, key
    for key in ("shadbala", "vimsopaka"):
        assert by_key[key]["available"] is False, key
    assert "beyond" in by_key["shadbala"]["why_not"]


def test_each_available_flag_matches_code_that_actually_exists():
    """The flags are a promise to a caller, so they are checked against the
    functions that keep it rather than trusted."""
    from hora.charts.ashtakavarga import bhinnashtakavarga
    from hora.charts.colord import stronger as stronger_co_lord
    from hora.charts.rasi_strength import stronger as stronger_rasi
    from hora.services import strength_service

    by_key = {m["key"]: m for m in STRENGTH_MEASURES}

    assert by_key["ashtakavarga"]["available"] is True
    assert callable(bhinnashtakavarga)

    assert by_key["simple_rules"]["available"] is True
    assert callable(stronger_co_lord) and callable(stronger_rasi)

    assert by_key["avastha"]["available"] is True
    for family in ("avasthas", "activity"):
        assert callable(getattr(strength_service, family)), family


def test_all_four_avastha_families_are_implemented_not_three():
    """The note used to say only age, alertness and mood were built. The
    activity family — sayanadi — is there too."""
    from hora.services import strength_service

    by_key = {m["key"]: m for m in STRENGTH_MEASURES}
    assert "All four families" in by_key["avastha"]["note"]
    result = strength_service.activity(
        graha=0, graha_longitude=22.83, moon_longitude=24.10,
        lagna_rasi=3, ghati=17)
    assert result["name"]


def test_simple_rules_is_the_measure_section_9_2_actually_wants():
    by_key = {m["key"]: m for m in STRENGTH_MEASURES}
    assert "Mars and Ketu" in by_key["simple_rules"]["note"]


def test_resolve_dual_lords_omits_what_it_cannot_decide():
    """An undecided sign must stay out of the map.

    Putting it in with an arbitrary winner would make the arudha endpoint
    answer confidently and wrongly. Leaving it out makes the endpoint raise,
    which is the truth.

    Rule 2 supplies its own aspects now, so an empty table is passed to model
    "no aspects known" and stop the cascade there.
    """
    from hora.core.const import Rasi

    # Every graha alone in its rasi, so rule 1 ties for both pairs.
    longitudes = {
        int(Graha.SUN): lon(1, "Ar"), int(Graha.MOON): lon(1, "Ta"),
        int(Graha.MARS): lon(23, "Cn"), int(Graha.MERCURY): lon(1, "Ge"),
        int(Graha.JUPITER): lon(1, "Le"), int(Graha.VENUS): lon(1, "Vi"),
        int(Graha.SATURN): lon(27, "Cp"), int(Graha.RAHU): lon(14, "Pi"),
        int(Graha.KETU): lon(5, "Sg"),
    }
    stopped = arudha_service.resolve_dual_lords(longitudes, rasi_aspects={})
    assert Rasi.SCORPIO not in stopped
    assert Rasi.AQUARIUS not in stopped

    # With the default aspect table the cascade runs to completion.
    resolved = arudha_service.resolve_dual_lords(longitudes)
    assert Rasi.SCORPIO in resolved and Rasi.AQUARIUS in resolved


def test_arudha_now_has_the_books_own_comparison():
    """§15.5.1 supplies the rule §9.2 defers to.

    Until it was transcribed, this asserted the opposite — avastha was the
    only measure available and was explicitly not the book's answer. The
    cascade replaced it; see test_book_chapter15_colord.py.
    """
    payload = arudha_service.rules()
    assert payload["strength_comparison_available"] is True
    assert payload["strength_comparison_section"] == "15.5.1 Stronger Co-Lord"
    assert "cascade" in payload["strength_comparison_note"]


# --------------------------------------------------------------------------
# 15.4.4 — states related to activity (sayanaadi avasthas)
#
# Tables 36 and 37, the formula, the six term definitions and the planetary
# adjustments were checked against the user's screenshots of section 15.4.4 and
# match. The tables below are those screenshots, so a failure here means the
# code drifted from the book, not that the test is out of date.
#
# Still unchecked: footnotes 51 and 52, which the screenshots cut off before.
# See docs/open-items.md OI-26.
# --------------------------------------------------------------------------

#: Table 36 exactly as printed.
TABLE_36 = {
    1: ("Sayana", "Lying down, resting"),
    2: ("Upavesana", "Sitting down"),
    3: ("Netrapaani", "Eyes and hands"),
    4: ("Prakaasana", "Shining"),
    5: ("Gamana", "Going (on the move)"),
    6: ("Aagamana", "Coming, returning"),
    7: ("Sabhaa", "Being at an assembly"),
    8: ("Aagama", "Coming/Acquiring"),
    9: ("Bhojana", "Eating"),
    10: ("Nriyalipsaa", "Longing to dance"),
    11: ("Kautuka", "Being eager"),
    12: ("Nidraa", "Sleeping"),
}

#: Table 37 exactly as printed — Devanagari and the book's own Roman column.
TABLE_37 = {
    1: ("अकछडधभव", "a, ka, chh, d (alveolar), dh (dental), bh, v"),
    2: ("इखजढनमश", "i, kh, j, dh (alveolar), n (dental), m, s/sh (palatal)"),
    3: ("उगझतपयष", "u, g, jh, t, p, y, sh (alveolar)"),
    4: ("एघटथफरस", "e, gh, t (alveolar), th (dental), ph, r, s (dental)"),
    5: ("ओचठदबलह", "o, ch, th (alveolar), d (dental), b, l, h"),
}


@pytest.mark.parametrize("index,expected", sorted(TABLE_36.items()))
def test_table_36_matches_the_book(index, expected):
    from hora.core.const import SAYANAADI_AVASTHAS

    name, meaning = expected
    row = SAYANAADI_AVASTHAS[index]
    assert row["name"] == name
    assert row["meaning"] == meaning


def test_only_the_two_rows_the_book_gives_two_names_have_aliases():
    """Row 7 is parenthesised in Table 36: "Sabhaa (Sabhaa vasati)".

    Row 10 is spelled "Nriyalipsaa" in Table 36 and "Nrityalipsaa" in the
    results heading later in the section, so both are the author's. See D-20 —
    an earlier pass dropped that alias on Table 36 alone, before the results
    heading had been seen.

    No other row may acquire an alias without the book printing one.
    """
    from hora.core.const import SAYANAADI_AVASTHAS

    with_aliases = {
        index: row["aliases"]
        for index, row in SAYANAADI_AVASTHAS.items() if row.get("aliases")
    }
    assert with_aliases == {7: ["Sabhaa vasati"], 10: ["Nrityalipsaa"]}


@pytest.mark.parametrize("number,expected", sorted(TABLE_37.items()))
def test_table_37_matches_the_book(number, expected):
    from hora.core.const import SOUND_NUMBERS

    devanagari, roman = expected
    row = SOUND_NUMBERS[number]
    assert "".join(row["devanagari"]) == devanagari
    assert row["roman"] == roman


def test_every_table_37_group_has_seven_sounds():
    from hora.core.const import SOUND_NUMBERS

    for number, row in SOUND_NUMBERS.items():
        assert len(row["devanagari"]) == 7, number


def test_the_six_term_definitions_match_the_book():
    from hora.core.const import SAYANAADI_TERMS

    printed = {
        "C": "the number of the constellation occupied by the planet "
             "(1 for Aswini, 2 for Bharani and so on)",
        "P": "the index of the planet whose avastha we are finding "
             "(1 for Sun, 2 for Moon)",
        "A": "the index of the amsa (navamsa) occupied by the planet in its rasi",
        "M": "the constellation occupied by Moon",
        "G": "the ghati running at birth",
        "L": "the rasi occupied by lagna (1 for Ar, 2 for Ta and so on)",
    }
    assert {t["symbol"]: t["text"] for t in SAYANAADI_TERMS} == printed


def test_the_planetary_adjustments_match_the_book():
    """"5 for Sun and Jupiter, 2 Moon and Mars, 3 for Mercury, Venus and
    Saturn and 4 for Rahu and Ketu"."""
    from hora.core.const import PLANETARY_ADJUSTMENT

    assert PLANETARY_ADJUSTMENT == {0: 5, 4: 5, 1: 2, 2: 2, 3: 3, 5: 3, 6: 3,
                                    7: 4, 8: 4}


def test_the_three_strength_values_match_the_book():
    """"1 means drishti and medium, 2 means cheshta and full, 3 (or 0) means
    vicheshta and very little"."""
    from hora.core.const import ACTIVITY_STRENGTH, VICHESHTA_REMAINDER_NOTE

    assert ACTIVITY_STRENGTH[1] == {"name": "drishti", "results": "medium"}
    assert ACTIVITY_STRENGTH[2] == {"name": "cheshta", "results": "full"}
    assert ACTIVITY_STRENGTH[0] == {"name": "vicheshta", "results": "very little"}
    # The book says "3 (or 0)"; a remainder mod 3 is never 3.
    assert 3 not in ACTIVITY_STRENGTH
    assert "cannot be 3" in VICHESHTA_REMAINDER_NOTE


def test_this_family_is_recorded_as_the_most_important():
    from hora.core.const import ACTIVITY_IS_MOST_IMPORTANT

    assert "most important of all states" in ACTIVITY_IS_MOST_IMPORTANT
    assert strength_service.rules()["activity"]["most_important"] == \
        ACTIVITY_IS_MOST_IMPORTANT


def test_the_verification_note_names_what_was_checked():
    payload = strength_service.rules()["activity"]
    for checked in ("Tables 36", "formula", "footnotes 51 and 52", "108"):
        assert checked in payload["verification_note"], checked

def test_there_are_twelve_sayanaadi_states():
    from hora.core.const import SAYANAADI_AVASTHAS

    assert sorted(SAYANAADI_AVASTHAS) == list(range(1, 13))


def test_navamsa_index_is_the_amsa_of_its_own_rasi_not_the_navamsa_rasi():
    """Footnote 51's example: Mercury at 22Ge14 gives A = 7."""
    from hora.charts.avastha import navamsa_index

    assert navamsa_index(lon(22 + 14 / 60, "Ge")) == 7
    # Each navamsa is 3 deg 20', so the boundaries must land exactly.
    assert navamsa_index(lon(0, "Ar")) == 1
    assert navamsa_index(lon(29.99, "Pi")) == 9


def test_ghati_at_birth_follows_footnote_52():
    """17 hours after sunrise is 42.5 ghatis elapsed, so the 43rd is running."""
    from hora.charts.avastha import ghati_at_birth

    assert ghati_at_birth(17.0) == 43
    assert ghati_at_birth(0.0) == 1


def test_a_remainder_of_zero_indexes_the_twelfth_state():
    """D-19. Table 36 has no row 0, so 0 can only mean the twelfth."""
    from hora.charts.avastha import SAYANAADI_AVASTHAS, avastha_by_activity

    # Search for an input whose total is divisible by 12.
    found = None
    for ghati in range(1, 61):
        result = avastha_by_activity(0, 0.0, 0.0, 0, ghati)
        if result.steps[1].value % 12 == 0:
            found = result
            break
    assert found is not None, "no input produced a remainder of zero"
    assert found.index == 12
    assert found.name == SAYANAADI_AVASTHAS[12]["name"]
    assert "12th row" in found.steps[2].detail


def test_the_formula_is_computed_step_by_step():
    result = strength_service.activity(
        3, lon(22 + 14 / 60, "Ge"), 100.0, 5, 43, name_sound=1
    )
    assert result["formula"] == "((C x P x A) + M + G + L) mod 12"
    assert [t["symbol"] for t in result["terms"]] == ["C", "P", "A", "M", "G", "L"]
    # Step 1 must be the product of exactly C, P and A.
    terms = {t["symbol"]: t["value"] for t in result["terms"]}
    assert result["steps"][0]["value"] == terms["C"] * terms["P"] * terms["A"]
    # Step 2 adds M, G and L to it.
    assert result["steps"][1]["value"] == (
        result["steps"][0]["value"] + terms["M"] + terms["G"] + terms["L"]
    )


def test_strength_is_null_without_a_name_sound_not_guessed():
    result = strength_service.activity(3, lon(22, "Ge"), 100.0, 5, 43)
    assert result["strength"] is None
    assert result["strength_results"] is None
    assert result["sound_number"] is None
    assert len(result["steps"]) == 4       # the four index steps only


def test_supplying_a_name_sound_adds_the_strength_steps():
    result = strength_service.activity(3, lon(22, "Ge"), 100.0, 5, 43, name_sound=1)
    assert result["strength"] in {"cheshta", "drishti", "vicheshta"}
    assert len(result["steps"]) == 9


def test_devanagari_sound_lookup_is_unambiguous():
    from hora.charts.avastha import sound_number

    assert sound_number("क") == 1
    assert sound_number("इ") == 2


def test_an_ambiguous_roman_syllable_is_refused():
    """The book's Roman column puts "d" in two groups. A guess would be wrong
    half the time, so it raises and names both options."""
    from hora.charts.avastha import sound_number

    with pytest.raises(AvasthaError, match="ambiguous"):
        sound_number("d")


def test_an_unknown_syllable_is_refused():
    from hora.charts.avastha import sound_number

    with pytest.raises(AvasthaError, match="no Table 37 sound"):
        sound_number("zzz")


@pytest.mark.parametrize("graha,expected", [
    (0, 5), (4, 5),          # Sun, Jupiter
    (1, 2), (2, 2),          # Moon, Mars
    (3, 3), (5, 3), (6, 3),  # Mercury, Venus, Saturn
    (7, 4), (8, 4),          # Rahu, Ketu
])
def test_planetary_adjustments_cover_all_nine_grahas(graha, expected):
    from hora.core.const import PLANETARY_ADJUSTMENT

    assert PLANETARY_ADJUSTMENT[graha] == expected


def test_activity_strength_has_three_cases_including_zero():
    """Remainders 1, 2 and 0 — there is no case 3."""
    from hora.core.const import ACTIVITY_STRENGTH

    assert sorted(ACTIVITY_STRENGTH) == [0, 1, 2]


def test_footnote_51_matches_the_book():
    """The navamsa-index example, which pins what A is *not*."""
    from hora.core.const import NAVAMSA_INDEX_NOTE

    assert NAVAMSA_INDEX_NOTE == (
        "For example, let us say Mercury is in 22Ge14. Each navamsa has a "
        "length of 3°20' (1/9th of 30°) and 22°14' in Ge is in the 7th "
        "navamsa of Ge (please note that we are not talking about the rasi "
        "occupied by the planet in navamsa). Then we use A = 7 for Mercury."
    )
    # The behaviour the footnote describes.
    from hora.charts.avastha import navamsa_index

    assert navamsa_index(lon(22 + 14 / 60, "Ge")) == 7


def test_footnote_52_matches_the_book():
    """The ghati example, and the arithmetic it states."""
    from hora.charts.avastha import ghati_at_birth
    from hora.core.const import GHATI_NOTE, GHATIS_PER_HOUR

    assert GHATI_NOTE == (
        "Suppose sunrise was at 6 am and someone was born at 11 pm. So 17 "
        "hours were over. Each hour has 2.5 ghatis and 17 hours = 17 x 2.5 "
        "= 42.5. So the 43rd ghati was running at birth."
    )
    assert GHATIS_PER_HOUR == 2.5
    assert 17 * GHATIS_PER_HOUR == 42.5
    assert ghati_at_birth(17.0) == 43


def test_section_15_4_4_is_now_fully_verified():
    """Nothing in the section is outstanding — OI-26 is closed."""
    payload = strength_service.rules()["activity"]
    assert payload["verified"] is True
    assert payload["footnotes_verified"] is True


def test_15_4_1s_four_worked_examples():
    """"A planet at 23 deg in Cn will be in Kumaara avastha" and the three
    others. Two odd rasis and two even, so the reversal is exercised."""
    from hora.charts.avastha import avastha_by_age

    abbr = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi",
            "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]
    for degrees, rasi, expected, results in (
        (23, "Cn", "Kumaara", "Half"),
        (19, "Li", "Vriddha", "Some"),
        (14, "Sg", "Yuva", "Full"),
        (27, "Pi", "Saisava", "Quarter"),
    ):
        got = avastha_by_age(abbr.index(rasi) * 30 + degrees)
        assert got.name == expected, rasi
        assert got.results == results


def test_the_age_table_reverses_for_even_rasis_except_at_yuva():
    """Table 35's two columns are mirror images, so only the middle band —
    12 to 18 degrees, Yuva — falls on the same degrees in both."""
    from hora.charts.avastha import avastha_by_age

    same = [d for d in range(30)
            if avastha_by_age(d + 0.5).name           # Aries, odd
            == avastha_by_age(30 + d + 0.5).name]     # Taurus, even
    assert same == list(range(12, 18))
    assert avastha_by_age(14.0).name == "Yuva"
    assert avastha_by_age(44.0).name == "Yuva"


def test_15_4_2s_alertness_uses_the_compound_relationship():
    """OI-114. §15.4.2 says "a rasi owned by a neutral or friendly planet"
    without saying which friendship, and chapter 3 defines two. We read the
    compound one, and it changes a real verdict: Jupiter in Gemini is
    naturally Mercury's enemy but compound-neutral, so Swapna rather than
    Sushupta."""
    import inspect

    from hora.charts.avastha import avastha_by_alertness
    from hora.core.const import NATURAL_RELATION, Graha

    assert NATURAL_RELATION[Graha.JUPITER][Graha.MERCURY] == 0, "natural enemy"
    doc = inspect.getdoc(avastha_by_alertness)
    assert "compound relationship" in doc
    assert "OI-114" in doc
