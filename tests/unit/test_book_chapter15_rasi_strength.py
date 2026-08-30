"""§15.5.2 Stronger Rasi — the cascade rasi dasas start from.

Every worked example in the section is a fixture here.

Three of them — rules 2, 4 and 6 — say "suppose we have a tie after rule (N-1)"
but give placements that do **not** produce that tie: rule 2's chart is settled
by rule 1, and rules 4 and 6 say outright that the tie is assumed. So those
rules are checked in isolation against the numbers the book states, and
separately through the cascade with charts constructed to reach them.
"""
import pytest

from hora.charts.rasi_strength import (
    PURPOSE_ADAPTATIONS,
    RasiStrengthError,
    advancement,
    co_lords_of,
    lord_of,
    occupants,
    rule_2_count,
    stronger,
)
from hora.core.const import RASI_LORD, Graha, Rasi

ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]
AR, LI = ABBR.index("Ar"), ABBR.index("Li")


def lon(degrees: float, rasi: str) -> float:
    return ABBR.index(rasi) * 30 + degrees


# --------------------------------------------------------------------------
# The worked examples
# --------------------------------------------------------------------------

def test_rule_1_more_planets():
    """"Ar contains Saturn and Jupiter and Li contains Venus. Then Ar is
    stronger, as it contains more planets"."""
    verdict = stronger(AR, LI, {
        int(Graha.SATURN): lon(10, "Ar"), int(Graha.JUPITER): lon(11, "Ar"),
        int(Graha.VENUS): lon(10, "Li"),
    })
    assert verdict.winner == AR
    assert verdict.decided_by == "1"


def test_rule_2_counts_match_the_book():
    """Jupiter in Ar; Mercury and Venus in Ta; Mars in Vi.

    "Ar is occupied by Jupiter and not by the other two... Its count is 1. Li
    is aspected by two (Mercury and lord Venus) and only Jupiter doesn't aspect
    it... So Li's count of 2 beats Ar's count of 1."

    Checked directly: the chart has a planet in Ar and none in Li, so rule 1
    settles it before rule 2 is reached.
    """
    longitudes = {
        int(Graha.JUPITER): lon(10, "Ar"), int(Graha.MERCURY): lon(10, "Ta"),
        int(Graha.VENUS): lon(11, "Ta"), int(Graha.MARS): lon(10, "Vi"),
    }
    aries, why = rule_2_count(AR, int(RASI_LORD[AR]), longitudes)
    assert aries == 1
    assert why == ["Jupiter (Jupiter) occupies it"]

    libra, why = rule_2_count(LI, int(RASI_LORD[LI]), longitudes)
    assert libra == 2
    assert "Mercury (Mercury) aspects from Taurus" in why
    assert "lord (Venus) aspects from Taurus" in why


def test_rule_2_counts_by_role_not_by_planet():
    """A lord that is also Jupiter or Mercury contributes twice.

    Same convention as §15.5.1's sibling rule, where Mercury-as-dispositor is
    counted a second time.
    """
    # Gemini's lord is Mercury, so Mercury fills two of the three roles.
    gemini = ABBR.index("Ge")
    count, why = rule_2_count(
        gemini, int(RASI_LORD[gemini]), {int(Graha.MERCURY): lon(10, "Ge")}
    )
    assert count == 2
    assert sum("Mercury" in w for w in why) == 2


def test_rule_3_exalted_planet():
    """Saturn and Mercury in Li, Jupiter and Venus in Ar. Saturn exalts in Li."""
    verdict = stronger(AR, LI, {
        int(Graha.SATURN): lon(10, "Li"), int(Graha.MERCURY): lon(11, "Li"),
        int(Graha.JUPITER): lon(10, "Ar"), int(Graha.VENUS): lon(11, "Ar"),
    })
    assert verdict.winner == LI
    assert verdict.decided_by == "3"
    assert "Saturn exalted" in verdict.reason


def test_rule_4_different_oddity_wins():
    """"Venus is in Cn, an even rasi and Mars is in Le, an odd rasi. Both Ar
    and Li are odd rasis... Li is stronger."

    The section says "suppose we have a tie after rule (3)"; these placements
    do not produce one, so the rule's own logic is checked here and the
    cascade route in the test below.
    """
    from hora.core.const import RASI_IS_ODD

    venus_in, mars_in = ABBR.index("Cn"), ABBR.index("Le")
    assert not RASI_IS_ODD[venus_in]           # Cancer is even
    assert RASI_IS_ODD[mars_in]                # Leo is odd
    assert RASI_IS_ODD[AR] and RASI_IS_ODD[LI]
    # Libra's lord sits in a rasi of different oddity; Aries' does not.
    assert RASI_IS_ODD[venus_in] != RASI_IS_ODD[LI]
    assert RASI_IS_ODD[mars_in] == RASI_IS_ODD[AR]


def test_rule_4_decides_through_the_cascade():
    """Mars in Ta (even) against Venus in Ge (odd), both rasis empty."""
    verdict = stronger(AR, LI, {
        int(Graha.MARS): lon(23, "Ta"), int(Graha.VENUS): lon(19, "Ge"),
    })
    assert verdict.decided_by == "4"
    assert verdict.winner == AR
    assert "different oddity" in verdict.reason


def test_rule_5_cannot_decide_a_rasi_against_the_seventh_from_it():
    """The section says so itself.

    "This rule is not useful in Narayana dasa, because we always compare a
    rasi and the 7th from it. If a rasi is dual/fixed/movable, the 7th from it
    is also of the same type."
    """
    from hora.core.const import RASI_MODALITY

    for rasi in range(12):
        assert RASI_MODALITY[rasi] == RASI_MODALITY[(rasi + 6) % 12]


def test_rule_5_decides_when_the_modalities_differ():
    """Aries (movable) against Gemini (dual) — a pair Narayana never compares."""
    gemini = ABBR.index("Ge")
    verdict = stronger(AR, gemini, {
        int(Graha.MARS): lon(23, "Ta"), int(Graha.MERCURY): lon(23, "Cp"),
    })
    assert verdict.decided_by == "5"
    assert verdict.winner == gemini


def test_rule_6_advancement_matches_the_book():
    """"Mars is at 23Ge17 and Venus is at 19Le51... Because Mars is more
    advanced, his Ar is stronger than Li"."""
    assert advancement(lon(23 + 17 / 60, "Ge"), Graha.MARS) == pytest.approx(
        23 + 17 / 60)
    assert advancement(lon(19 + 51 / 60, "Le"), Graha.VENUS) == pytest.approx(
        19 + 51 / 60)


def test_rule_6_decides_through_the_cascade():
    """The book's own longitudes, with the lords placed so rule 6 is reached."""
    verdict = stronger(AR, LI, {
        int(Graha.MARS): lon(23 + 17 / 60, "Ta"),
        int(Graha.VENUS): lon(19 + 51 / 60, "Cn"),
    })
    assert verdict.decided_by == "6"
    assert verdict.winner == AR


def test_the_nodes_are_measured_from_the_end_of_the_rasi():
    """"If Rahu is at 9Sc34, his advancement in Sc is 30° - 9°34' = 20°26'"."""
    assert advancement(lon(9 + 34 / 60, "Sc"), Graha.RAHU) == pytest.approx(
        20 + 26 / 60)
    assert advancement(lon(9 + 34 / 60, "Sc"), Graha.KETU) == pytest.approx(
        20 + 26 / 60)
    assert advancement(lon(9 + 34 / 60, "Sc"), Graha.MARS) == pytest.approx(
        9 + 34 / 60)


# --------------------------------------------------------------------------
# Scorpio and Aquarius go through section 15.5.1
# --------------------------------------------------------------------------

def test_a_co_owned_rasi_takes_its_lord_from_section_15_5_1():
    """"In the case of Aq and Sc, we use the stronger lord"."""
    longitudes = {
        int(Graha.MARS): lon(10, "Ge"), int(Graha.KETU): lon(10, "Aq"),
    }
    lord, why = lord_of(int(Rasi.SCORPIO), longitudes)
    assert lord == int(Graha.MARS)             # dual beats fixed, 15.5.1 rule 4
    assert "stronger co-lord" in why
    assert "rule 4" in why


def test_an_undecidable_co_lord_stops_this_cascade_too():
    """If §15.5.1 cannot name the lord, §15.5.2 cannot use it."""
    longitudes = {
        int(Graha.MARS): lon(10, "Cn"), int(Graha.KETU): lon(20, "Cp"),
    }
    lord, why = lord_of(int(Rasi.SCORPIO), longitudes)
    if lord is None:
        assert "could not decide" in why
    verdict = stronger(int(Rasi.SCORPIO), ABBR.index("Ta"), longitudes)
    # Either it resolved, or it stopped for the stated reason — never guessed.
    assert verdict.determined or "could not decide" in verdict.reason


def test_a_single_lorded_rasi_uses_its_plain_lord():
    lord, why = lord_of(AR, {int(Graha.MARS): lon(10, "Ge")})
    assert lord == int(Graha.MARS)
    assert "stronger co-lord" not in why


# --------------------------------------------------------------------------
# The section's warning
# --------------------------------------------------------------------------

def test_the_warning_is_recorded_as_data():
    """"The above rules are too general. One should understand the meaning of
    each rule and adapt based on the situation." """
    assert set(PURPOSE_ADAPTATIONS) == {"phalita", "ak_based", "ayur"}
    assert PURPOSE_ADAPTATIONS["phalita"]["implemented"] is True
    assert PURPOSE_ADAPTATIONS["ak_based"]["implemented"] is True
    assert PURPOSE_ADAPTATIONS["ayur"]["implemented"] is False


def test_ayur_dasas_are_refused_rather_than_approximated():
    """The text does not say how to weigh the luminaries against "all other
    planets", so rule 2 cannot be computed for that purpose."""
    with pytest.raises(RasiStrengthError, match="not implemented"):
        stronger(AR, LI, {int(Graha.MARS): lon(10, "Ge")}, purpose="ayur")


def test_ak_based_puts_the_ak_sign_above_every_other_rasi():
    """"the sign containing AK is stronger than any other rasi"."""
    verdict = stronger(AR, LI, {
        int(Graha.MARS): lon(10, "Ge"), int(Graha.VENUS): lon(10, "Cn"),
    }, purpose="ak_based", atma_karaka_rasi=LI)
    assert verdict.winner == LI
    assert verdict.decided_by == "ak"


def test_ak_based_prefers_a_lord_in_a_quadrant_from_ak():
    """"A rasi whose lord is in a quadrant from AK is stronger than a rasi
    whose lord is in a panaphara from AK"."""
    ak = ABBR.index("Ta")
    verdict = stronger(AR, LI, {
        int(Graha.MARS): lon(10, "Ta"),       # 1st from AK — a quadrant
        int(Graha.VENUS): lon(10, "Ge"),      # 2nd from AK — a panaphara
    }, purpose="ak_based", atma_karaka_rasi=ak)
    assert verdict.decided_by == "ak-placement"
    assert verdict.winner == AR
    # The rule sits after rule 2, as the section says: "After we check for the
    # aspects of Mercury, Jupiter and rasi lord, we should look at the
    # placement of rasi lord from AK."
    assert [r.rule for r in verdict.rules] == ["ak", "1", "2", "ak-placement"]


def test_ak_based_needs_the_ak_rasi():
    with pytest.raises(RasiStrengthError, match="atma_karaka_rasi"):
        stronger(AR, LI, {int(Graha.MARS): lon(10, "Ge")}, purpose="ak_based")


# --------------------------------------------------------------------------
# Cascade discipline and inputs
# --------------------------------------------------------------------------

def test_the_cascade_stops_at_the_first_rule_that_decides():
    verdict = stronger(AR, LI, {
        int(Graha.SATURN): lon(10, "Ar"), int(Graha.JUPITER): lon(11, "Ar"),
        int(Graha.VENUS): lon(10, "Li"),
    })
    assert [r.rule for r in verdict.rules] == ["1"]


def test_every_rule_reached_is_reported_with_its_wording():
    verdict = stronger(AR, LI, {
        int(Graha.MARS): lon(23 + 17 / 60, "Ta"),
        int(Graha.VENUS): lon(19 + 51 / 60, "Cn"),
    })
    assert [r.rule for r in verdict.rules] == ["1", "2", "3", "4", "5", "6"]
    assert all(r.description for r in verdict.rules)
    assert all(r.detail for r in verdict.rules)


def test_a_rasi_cannot_be_compared_with_itself():
    with pytest.raises(RasiStrengthError, match="itself"):
        stronger(AR, AR, {int(Graha.MARS): lon(10, "Ge")})


def test_an_unknown_purpose_is_refused():
    with pytest.raises(RasiStrengthError, match="unknown purpose"):
        stronger(AR, LI, {int(Graha.MARS): lon(10, "Ge")}, purpose="yoga")


# --------------------------------------------------------------------------
# Exercise 26 — rule 2 counts a co-lord that is not the stronger one
# --------------------------------------------------------------------------

def test_rule_2_counts_a_co_lord_that_is_not_the_stronger_lord():
    """Exercise 26 (5): "Aq is aspected by co-lord Rahu (though Saturn is the
    primary/stronger lord, Rahu's aspect also counts)."

    Resolving Aquarius to one lord before rule 2 runs loses that aspect, which
    is what this code used to do.
    """
    from hora.charts.rasi_strength import (
        co_lords_of,
        lord_of,
        rule_2_count,
    )
    from hora.core.const import Graha

    longitudes = {
        int(Graha.RAHU): ABBR.index("Ar") * 30 + 10, int(Graha.KETU): ABBR.index("Li") * 30 + 10,
        int(Graha.SATURN): ABBR.index("Ta") * 30 + 5,
        int(Graha.JUPITER): ABBR.index("Ge") * 30 + 5,
        int(Graha.MERCURY): ABBR.index("Cn") * 30 + 5,
        int(Graha.SUN): ABBR.index("Le") * 30 + 5, int(Graha.MOON): ABBR.index("Vi") * 30 + 5,
        int(Graha.MARS): ABBR.index("Sc") * 30 + 5, int(Graha.VENUS): ABBR.index("Sg") * 30 + 5,
    }
    stronger, _ = lord_of(ABBR.index("Aq"), longitudes)
    assert stronger == int(Graha.SATURN), "Saturn is the stronger co-lord"

    count, why = rule_2_count(ABBR.index("Aq"), co_lords_of(ABBR.index("Aq")), longitudes)
    assert any("Rahu" in reason for reason in why)
    assert count == 2

    only_stronger, _ = rule_2_count(ABBR.index("Aq"), stronger, longitudes)
    assert only_stronger == 1, "the old behaviour, kept as the contrast"


def test_co_lords_of_returns_two_only_for_scorpio_and_aquarius():
    from hora.charts.rasi_strength import co_lords_of

    doubles = {ABBR[s] for s in range(12) if len(co_lords_of(s)) == 2}
    assert doubles == {"Sc", "Aq"}
    for sign in range(12):
        assert 1 <= len(co_lords_of(sign)) <= 2


def test_rule_6_still_takes_the_stronger_co_lord():
    """Its own note says so — "In the case of Aq and Sc, we use the stronger
    lord" — so the two rules genuinely differ. See OI-111."""
    import inspect

    from hora.charts import rasi_strength

    source = inspect.getsource(rasi_strength.stronger)
    assert "co_lords_of(r)" in source, "rule 2 takes both"
    assert "lords[r]" in source, "the later rules take the resolved one"


def test_the_rule_2_example_contradicts_the_sections_own_cascade():
    """See D-49. Rule (1) gives Aries; the section concludes Libra.

    Unlike section 15.5.1's equivalent slip, where rule (1) and rule (2) named
    the same planet, here they disagree — so running the cascade as the
    section instructs produces the opposite of the section's answer. Pinned so
    the divergence is a recorded fact rather than a surprise.
    """
    longitudes = {
        int(Graha.JUPITER): lon(10, "Ar"), int(Graha.MERCURY): lon(10, "Ta"),
        int(Graha.VENUS): lon(11, "Ta"), int(Graha.MARS): lon(10, "Vi"),
    }
    verdict = stronger(AR, LI, longitudes)
    assert verdict.decided_by == "1"
    assert verdict.winner == AR                      # the book says Libra

    # Give Libra an occupant so rule (1) ties, and rule (2) does give Libra.
    tied = dict(longitudes) | {int(Graha.SATURN): lon(10, "Li")}
    verdict = stronger(AR, LI, tied)
    assert verdict.decided_by == "2"
    assert verdict.winner == LI


def test_rule_4s_note_holds_for_every_two_rasi_owner():
    """"the two rasis owned by each planet have a different oddity".

    The note is what makes rule (4) a guaranteed tie-break for graha arudhas,
    so the claim is worth checking rather than trusting. All five two-rasi
    owners satisfy it, which is why rule (4) can never leave a graha-arudha
    tie standing.
    """
    from collections import defaultdict

    from hora.core.const import RASI_IS_ODD, RASI_LORD

    owned = defaultdict(list)
    for rasi in range(12):
        owned[int(RASI_LORD[rasi])].append(rasi)

    pairs = [rs for rs in owned.values() if len(rs) == 2]
    assert len(pairs) == 5                       # every graha but the luminaries
    for first, second in pairs:
        assert RASI_IS_ODD[first] != RASI_IS_ODD[second]


# --------------------------------------------------------------------------
# Exercise 26 — six pairs. The exercise names Chart 12; see D-48.
# --------------------------------------------------------------------------

#: The chart Exercises 25 and 26 actually describe, determined entirely by
#: their own statements. It is not Chart 12 and matches nothing in the
#: register. Degrees are arbitrary within each rasi except where a rule needs
#: them; every claim either exercise makes is about rasis, not degrees.
EX26_CHART = {
    int(Graha.KETU): lon(10, "Ar"), int(Graha.VENUS): lon(10, "Ta"),
    int(Graha.RAHU): lon(10, "Li"), int(Graha.MARS): lon(10, "Sc"),
    int(Graha.JUPITER): lon(12, "Sc"), int(Graha.SUN): lon(10, "Sg"),
    int(Graha.MERCURY): lon(12, "Sg"), int(Graha.MOON): lon(10, "Cp"),
    int(Graha.SATURN): lon(10, "Pi"),
}

EX26_PAIRS = [
    ("Ar", "Li", "Ar", "2"), ("Ta", "Sc", "Sc", "1"), ("Ge", "Sg", "Sg", "1"),
    ("Cn", "Cp", "Cp", "1"), ("Le", "Aq", "Aq", "2"), ("Vi", "Pi", "Pi", "1"),
]


@pytest.mark.parametrize("first,second,winner,rule", EX26_PAIRS)
def test_exercise_26_on_the_chart_it_describes(first, second, winner, rule):
    """All six answers, each by the book's own deciding rule."""
    verdict = stronger(ABBR.index(first), ABBR.index(second), EX26_CHART)
    assert verdict.winner == ABBR.index(winner)
    assert verdict.decided_by == rule


def test_exercise_26s_own_occupancy_claims_hold_on_that_chart():
    """Twelve counts, stated across the six answers. None holds on Chart 12."""
    from hora.charts.book import graha_longitudes

    claimed = {"Ar": 1, "Ta": 1, "Ge": 0, "Cn": 0, "Le": 0, "Vi": 0,
               "Li": 1, "Sc": 2, "Sg": 2, "Cp": 1, "Aq": 0, "Pi": 1}
    for abbr, count in claimed.items():
        assert len(occupants(ABBR.index(abbr), EX26_CHART)) == count

    # On Chart 12 every claim of an occupied rasi fails. Three claims of an
    # empty rasi hold, but only because both charts leave Ge, Vi and Aq empty —
    # a coincidence of zeros, not agreement.
    chart_12 = {int(g): l for g, l in graha_longitudes(12).items()}
    agree = {a for a, c in claimed.items()
             if len(occupants(ABBR.index(a), chart_12)) == c}
    assert agree == {"Ge", "Vi", "Aq"}
    assert all(claimed[a] == 0 for a in agree)
    assert not any(claimed[a] for a in agree), (
        "if an occupied-rasi claim ever holds on Chart 12, D-48 needs revisiting")


def test_exercise_26s_rule_2_readings_hold_on_that_chart():
    """The four aspect readings the answers quote, by name."""
    def why(abbr):
        return rule_2_count(ABBR.index(abbr), co_lords_of(ABBR.index(abbr)),
                            EX26_CHART)[1]

    assert why("Ar") == ["Jupiter (Jupiter) aspects from Scorpio",
                         "lord (Mars) aspects from Scorpio"]
    assert why("Li") == ["lord (Venus) aspects from Taurus"]
    assert why("Le") == []
    assert why("Aq") == ["co-lord (Rahu) aspects from Libra"]
