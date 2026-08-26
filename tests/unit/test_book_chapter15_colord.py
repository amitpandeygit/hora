"""§15.5.1 Stronger Co-Lord — the rule §9.2 defers to.

Scorpio is co-owned by Mars and Ketu, Aquarius by Saturn and Rahu. The stronger
acts as lord and decides the arudha pada.

All five worked examples in the section are fixtures here and all five
reproduce. Two things the section says that are easy to lose:

* the cascade **stops** at the first rule that decides, and
* a rule that cannot be evaluated stops it too — skipping to a later rule
  would let a lower rule answer a question a higher one might have settled.
"""
import pytest

from hora.charts.colord import (
    CO_LORDS,
    CoLordError,
    default_rasi_aspects,
    rule_2_count,
    rule_5b_advancement,
    stronger,
)
from hora.core.const import Graha, Rasi
from hora.services import colord_service

ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]


def lon(degrees: float, rasi: str) -> float:
    return ABBR.index(rasi) * 30 + degrees


#: Rule 2 computes its own aspects now. This is the same table, kept explicit
#: so these tests state what they depend on; ``test_rasi_drishti.py`` pins the
#: table itself.
RASI_ASPECTS = default_rasi_aspects()


def test_the_default_table_satisfies_the_books_example():
    """"Rahu in Ar is aspected by Mars, his dispositor, from Le".

    Rule 2 no longer needs a table passed in — this is what it uses.
    """
    assert ABBR.index("Ar") in RASI_ASPECTS[ABBR.index("Le")]


# --------------------------------------------------------------------------
# The basic rule
# --------------------------------------------------------------------------

def test_a_co_lord_in_the_rasi_hands_lordship_to_the_other():
    """"If Saturn is in Aq and Rahu is in a rasi other than Aq, Rahu becomes
    the primary lord of Aq"."""
    verdict = stronger(
        Rasi.AQUARIUS,
        {int(Graha.SATURN): lon(10, "Aq"), int(Graha.RAHU): lon(10, "Ar")},
        rasi_aspects=RASI_ASPECTS,
    )
    assert verdict.winner == int(Graha.RAHU)
    assert verdict.decided_by == "basic"


def test_both_co_lords_in_the_rasi_falls_through_to_the_cascade():
    verdict = stronger(
        Rasi.SCORPIO,
        {int(Graha.MARS): lon(10, "Sc"), int(Graha.KETU): lon(20, "Sc"),
         int(Graha.SUN): lon(5, "Sc")},
        rasi_aspects=RASI_ASPECTS,
    )
    assert verdict.rules[0].rule == "basic"
    assert verdict.rules[0].decided is False
    assert "both co-lords" in verdict.rules[0].detail


# --------------------------------------------------------------------------
# The five worked examples
# --------------------------------------------------------------------------

def test_rule_1_more_planets_joined():
    """Saturn in Pi with Mars and Sun; Rahu in Ar with Jupiter."""
    verdict = stronger(Rasi.AQUARIUS, {
        int(Graha.SATURN): lon(10, "Pi"), int(Graha.MARS): lon(11, "Pi"),
        int(Graha.SUN): lon(12, "Pi"), int(Graha.RAHU): lon(10, "Ar"),
        int(Graha.JUPITER): lon(11, "Ar"),
    }, rasi_aspects=RASI_ASPECTS)
    assert verdict.winner == int(Graha.SATURN)
    assert verdict.decided_by == "1"


def test_rule_2_counts_jupiter_mercury_and_dispositor_by_role():
    """Saturn in Ge with Mercury, Rahu in Ar, Mars in Le, Jupiter in Ta.

    "Saturn is conjoined by Mercury and his dispositor (who is Mercury again).
    His count is 2." The three are counted as roles, not as distinct planets —
    Mercury contributes twice here.

    The section's own example never reaches rule 2 through the cascade,
    because Saturn has a co-tenant and Rahu does not, so rule 1 already
    decides. The counting is therefore checked directly.
    """
    longitudes = {
        int(Graha.SATURN): lon(10, "Ge"), int(Graha.MERCURY): lon(11, "Ge"),
        int(Graha.RAHU): lon(10, "Ar"), int(Graha.MARS): lon(10, "Le"),
        int(Graha.JUPITER): lon(10, "Ta"),
    }
    saturn, why = rule_2_count(int(Graha.SATURN), longitudes, RASI_ASPECTS)
    assert saturn == 2
    assert sum("Mercury" in w for w in why) == 2      # counted twice, by role

    rahu, why = rule_2_count(int(Graha.RAHU), longitudes, RASI_ASPECTS)
    assert rahu == 1
    assert "dispositor (Mars) aspects from Leo" in why


def test_rule_2_decides_when_rule_1_ties():
    """Same placements, but with Rahu given a co-tenant so rule 1 ties."""
    verdict = stronger(Rasi.AQUARIUS, {
        int(Graha.SATURN): lon(10, "Ge"), int(Graha.MERCURY): lon(11, "Ge"),
        int(Graha.RAHU): lon(10, "Ar"), int(Graha.VENUS): lon(11, "Ar"),
        int(Graha.MARS): lon(10, "Le"), int(Graha.JUPITER): lon(10, "Ta"),
    }, rasi_aspects=RASI_ASPECTS)
    assert verdict.rules[1].decided is False          # rule 1 tied
    assert verdict.decided_by == "2"
    assert verdict.winner == int(Graha.SATURN)


def test_rule_3_exaltation():
    """Saturn in Li (exalted), Rahu in Cn, tie after (2)."""
    verdict = stronger(Rasi.AQUARIUS, {
        int(Graha.SATURN): lon(10, "Li"), int(Graha.RAHU): lon(10, "Cn"),
    }, rasi_aspects=RASI_ASPECTS)
    assert verdict.winner == int(Graha.SATURN)
    assert verdict.decided_by == "3"


def test_rule_4_dual_beats_fixed_beats_movable():
    """Mars in Ge (dual), Ketu in Aq (fixed), tie after (3)."""
    verdict = stronger(Rasi.SCORPIO, {
        int(Graha.MARS): lon(10, "Ge"), int(Graha.KETU): lon(10, "Aq"),
    }, rasi_aspects=RASI_ASPECTS)
    assert verdict.winner == int(Graha.MARS)
    assert verdict.decided_by == "4"


def test_rule_5b_the_more_advanced_planet():
    """Mars at 23Li17, Ketu at 5Cn54.

    Mars is advanced 23 deg 17'. Ketu is measured from the END of Cancer:
    30 deg - 5 deg 54' = 24 deg 6'. Ketu is more advanced and wins.
    """
    verdict = stronger(Rasi.SCORPIO, {
        int(Graha.MARS): lon(23 + 17 / 60, "Li"),
        int(Graha.KETU): lon(5 + 54 / 60, "Cn"),
    }, rasi_aspects=RASI_ASPECTS)
    assert verdict.winner == int(Graha.KETU)
    assert verdict.decided_by == "5b"
    assert "from the end of the rasi" in verdict.reason


def test_rule_5a_the_longer_dasa():
    """Saturn in Ge gives 8 years, Rahu in Vi gives 5. Saturn is used."""
    verdict = stronger(Rasi.AQUARIUS, {
        int(Graha.SATURN): lon(10, "Ge"), int(Graha.RAHU): lon(10, "Vi"),
    }, purpose="dasa", rasi_aspects=RASI_ASPECTS,
        dasa_years={int(Graha.SATURN): 8, int(Graha.RAHU): 5})
    assert verdict.winner == int(Graha.SATURN)
    assert verdict.decided_by == "5a"


# --------------------------------------------------------------------------
# Rule 5b measures BOTH nodes from the end — unlike chapter 8
# --------------------------------------------------------------------------

def test_both_nodes_are_measured_from_the_end_of_the_rasi():
    """§15.5.1 says "Rahu and Ketu"; §8.2 says only "Rahu".

    Chapter 8 names only Rahu because chara karakas exclude Ketu entirely.
    Reusing chapter 8's helper here gave Ketu the wrong advancement and lost
    the worked example above, so the two rules are implemented separately.
    """
    from hora.charts.karaka import advancement as chapter_8

    ketu_at = lon(5 + 54 / 60, "Cn")
    assert rule_5b_advancement(ketu_at, Graha.KETU) == pytest.approx(24 + 6 / 60)
    assert rule_5b_advancement(ketu_at, Graha.RAHU) == pytest.approx(24 + 6 / 60)
    # Chapter 8 measures Ketu from the start, which is right for chapter 8.
    assert chapter_8(ketu_at, Graha.KETU) == pytest.approx(5 + 54 / 60)
    assert chapter_8(ketu_at, Graha.RAHU) == pytest.approx(24 + 6 / 60)


# --------------------------------------------------------------------------
# The cascade's stopping behaviour
# --------------------------------------------------------------------------

def test_the_cascade_stops_at_the_first_rule_that_decides():
    """"If we have a winner in one step, we do not go through the remaining
    steps." Later rules must not even be evaluated."""
    verdict = stronger(Rasi.AQUARIUS, {
        int(Graha.SATURN): lon(10, "Pi"), int(Graha.MARS): lon(11, "Pi"),
        int(Graha.SUN): lon(12, "Pi"), int(Graha.RAHU): lon(10, "Ar"),
        int(Graha.JUPITER): lon(11, "Ar"),
    }, rasi_aspects=RASI_ASPECTS)
    assert [r.rule for r in verdict.rules] == ["basic", "1"]


def test_an_unevaluable_rule_stops_the_cascade_rather_than_being_skipped():
    """Rule 2 has a default table, so this passes an empty one to model
    "no aspects known". The answer must be "undetermined", not "whatever rule
    3 says" — skipping could give a different lord."""
    longitudes = {
        int(Graha.SATURN): lon(10, "Li"), int(Graha.RAHU): lon(10, "Cn"),
    }
    with_aspects = stronger(Rasi.AQUARIUS, longitudes, rasi_aspects=RASI_ASPECTS)
    assert with_aspects.decided_by == "3"

    without = stronger(Rasi.AQUARIUS, longitudes, rasi_aspects={})
    assert without.winner is None
    assert without.determined is False
    assert [r.rule for r in without.rules] == ["basic", "1", "2"]
    assert without.rules[-1].decided is None
    assert "stops here" in without.rules[-1].detail


def test_rule_5a_is_undetermined_without_dasa_lengths():
    verdict = stronger(Rasi.AQUARIUS, {
        int(Graha.SATURN): lon(10, "Ge"), int(Graha.RAHU): lon(10, "Vi"),
    }, purpose="dasa")
    assert verdict.winner is None
    assert verdict.rules[-1].rule == "5a"
    assert verdict.rules[-1].decided is None


# --------------------------------------------------------------------------
# Inputs
# --------------------------------------------------------------------------

def test_only_scorpio_and_aquarius_are_co_owned():
    assert set(CO_LORDS) == {int(Rasi.SCORPIO), int(Rasi.AQUARIUS)}
    assert CO_LORDS[Rasi.SCORPIO] == (Graha.MARS, Graha.KETU)
    assert CO_LORDS[Rasi.AQUARIUS] == (Graha.SATURN, Graha.RAHU)


@pytest.mark.parametrize("rasi", [0, 3, 6, 11])
def test_a_single_lorded_rasi_is_refused(rasi):
    with pytest.raises(CoLordError, match="one lord"):
        stronger(rasi, {int(Graha.MARS): 10.0, int(Graha.KETU): 100.0})


def test_a_missing_co_lord_is_refused():
    with pytest.raises(CoLordError, match="Ketu"):
        stronger(Rasi.SCORPIO, {int(Graha.MARS): 10.0})


def test_an_unknown_purpose_is_refused():
    with pytest.raises(CoLordError, match="purpose"):
        stronger(Rasi.SCORPIO, {int(Graha.MARS): 10.0, int(Graha.KETU): 100.0},
                 purpose="yoga")


def test_the_service_returns_every_rule_reached_in_order():
    payload = colord_service.stronger(
        int(Rasi.SCORPIO),
        {int(Graha.MARS): lon(23 + 17 / 60, "Li"),
         int(Graha.KETU): lon(5 + 54 / 60, "Cn")},
        "arudha",
        {sign: list(targets) for sign, targets in RASI_ASPECTS.items()},
    )
    assert payload["winner_name"] == "Ketu"
    assert payload["decided_by"] == "5b"
    assert [r["rule"] for r in payload["rules"]] == ["basic", "1", "2", "3", "4", "5b"]
    assert all(r["description"] for r in payload["rules"])


# --------------------------------------------------------------------------
# The arudha blocker
#
# §9.2 defers "take the stronger lord" to a later chapter. These assert that
# the deferral is actually discharged at the endpoint, not merely that the
# cascade exists — it existed for a while as dead code the service never
# called.
# --------------------------------------------------------------------------

def test_a_scorpio_house_resolves_without_the_caller_naming_a_lord():
    """The blocker, gone. Nothing supplied but the chart."""
    from hora.services import arudha_service

    # Mars in Ge (dual) beats Ketu in Aq (fixed) by rule 4 — signs suffice.
    signs = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 8, 8: 10}
    result = arudha_service.one(house=1, lagna_sign=int(Rasi.SCORPIO),
                                graha_signs=signs)
    assert result["lord_name"] == "Ketu"
    assert "stronger than Mars" in result["steps"][1]["detail"]


def test_longitudes_let_the_cascade_reach_rule_5b():
    """Signs alone cannot decide rule 5b; longitudes can."""
    from hora.services import arudha_service

    # Both co-lords in Gemini: rules 1 to 4 all tie.
    signs = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 8, 8: 2}
    with pytest.raises(Exception, match="could not decide"):
        arudha_service.one(1, int(Rasi.SCORPIO), signs)

    longitudes = {g: s * 30 + 12.5 + g for g, s in signs.items()}
    result = arudha_service.one(1, int(Rasi.SCORPIO), signs,
                                graha_longitudes=longitudes)
    assert result["lord_name"] in {"Mars", "Ketu"}


def test_an_explicit_stronger_lord_is_never_overruled():
    """A caller who has decided keeps their decision."""
    from hora.services import arudha_service

    signs = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 8, 8: 10}
    auto = arudha_service.one(1, int(Rasi.SCORPIO), signs)
    assert auto["lord_name"] == "Ketu"

    forced = arudha_service.one(1, int(Rasi.SCORPIO), signs,
                                stronger_lord={int(Rasi.SCORPIO): int(Graha.MARS)})
    assert forced["lord_name"] == "Mars"


def test_the_whole_table_resolves_for_a_scorpio_lagna():
    """All twelve padas, four of which involve a co-owned rasi."""
    from hora.services import arudha_service

    signs = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 8, 8: 10}
    table = arudha_service.table(int(Rasi.SCORPIO), signs, include_steps=False)
    assert len(table["padas"]) == 12
    assert all(p["sign_name"] for p in table["padas"])


def test_rule_5b_reports_that_it_needs_longitudes():
    """Comparing two zeros and calling it a tie would be a wrong answer."""
    signs_as_longitudes = {int(Graha.MARS): 60.0, int(Graha.KETU): 60.0}
    verdict = stronger(Rasi.SCORPIO, signs_as_longitudes,
                       advancement_known=False)
    assert verdict.winner is None
    assert verdict.rules[-1].rule == "5b"
    assert verdict.rules[-1].decided is None
    assert "needs longitudes" in verdict.rules[-1].detail
