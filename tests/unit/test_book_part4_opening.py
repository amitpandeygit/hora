"""Part 4's opening page — the Tajaka system, and the case for including it.

Part 2 opened with a roadmap of nine named dasa systems. Part 3 named no
techniques. Part 4 names "a few special dasa systems" and no names either, so
these tests pin the definition, the provenance and the gate the natal chart
puts on an annual chart — and record that the casting method has not arrived,
so nothing here may be computed yet.
"""
from __future__ import annotations

import pytest


def test_the_system_is_defined_by_the_solar_return():
    from hora.core.const import (
        ANNUAL_CHART_NAMES,
        SOLAR_RETURN_RULE,
        TAJAKA_IS_USEFUL_FOR_PRECISE_PREDICTIONS,
    )

    assert "solar return charts" in SOLAR_RETURN_RULE
    assert "the position he occupied in the zodiac" in SOLAR_RETURN_RULE
    assert ANNUAL_CHART_NAMES == ("Tajaka annual chart",
                                  "Tajaka varsha chakra")
    for name in ANNUAL_CHART_NAMES:
        assert name in SOLAR_RETURN_RULE
    assert "closer to western astrology" in (
        TAJAKA_IS_USEFUL_FOR_PRECISE_PREDICTIONS)


def test_the_part_admits_it_has_no_maharshi_behind_it():
    """The only technique in the book argued for on precedent, not authority.
    """
    from hora.core.const import (
        TAJAKA_AUTHORITIES,
        TAJAKA_IS_ADMITTED_ON_PRECEDENT_NOT_AUTHORITY,
        TAJAKA_PROVENANCE,
    )

    assert "may validly question" in TAJAKA_PROVENANCE
    assert ("There are no references to it in the works of Parasara, Jaimini "
            "and other maharshis") in TAJAKA_PROVENANCE

    silent = [row["who"] for row in TAJAKA_AUTHORITIES
              if row["gives"].startswith("nothing")]
    assert silent == ["Parasara", "Jaimini", "other maharshis"]
    speaking = [row["who"] for row in TAJAKA_AUTHORITIES
                if not row["gives"].startswith("nothing")]
    assert speaking == ["Neelakantha", "Dr. B.V. Raman"]
    for who in speaking:
        assert who.replace("Dr. ", "Dr. ") in TAJAKA_PROVENANCE
    assert "set the precedent" in TAJAKA_PROVENANCE
    assert "No other part of the book argues for a technique this way" in (
        TAJAKA_IS_ADMITTED_ON_PRECEDENT_NOT_AUTHORITY)


def test_the_lost_parasara_is_offered_as_speculation_only():
    from hora.core.const import (
        TAJAKA_PROVENANCE,
        THE_MISSING_PARASARA_IS_MARKED_AS_SPECULATION,
    )

    assert "One can only speculate whether Parasara talked about this system" \
        in TAJAKA_PROVENANCE
    assert "possibly missing today" in TAJAKA_PROVENANCE
    assert "not as a provenance" in (
        THE_MISSING_PARASARA_IS_MARKED_AS_SPECULATION)


def test_the_natal_chart_gates_the_annual_chart_one_way():
    from hora.core.const import (
        ANNUAL_CHART_SCOPE,
        THE_NATAL_CHART_VETOES_AND_IS_NOT_VETOED,
    )

    assert "can take place only if they are 'possible' based on natal chart" \
        in ANNUAL_CHART_SCOPE
    assert "finer insight into the year" in ANNUAL_CHART_SCOPE
    # The gate is stated once, in one direction, and nowhere reversed.
    assert ANNUAL_CHART_SCOPE.count("only if") == 1
    assert "The part gives no reverse rule" in (
        THE_NATAL_CHART_VETOES_AND_IS_NOT_VETOED)


def test_the_annual_chart_is_what_26_9_asked_for_and_could_not_name():
    """§26.9 required chart-sensitive methods and named none. A solar return
    is cast for one person's own instant, which is the property every
    technique in chapters 25 and 26 lacks.
    """
    from hora.core.const import (
        CHAPTER_26_CONCLUSION,
        SOLAR_RETURN_RULE,
        THE_ANNUAL_CHART_IS_THE_CHART_SENSITIVE_METHOD_26_9_ASKED_FOR,
    )

    assert "chart-sensitive methods" in CHAPTER_26_CONCLUSION
    # §26.9 names no method; Part 4 supplies one.
    for named in ("Tajaka", "annual", "solar"):
        assert named not in CHAPTER_26_CONCLUSION
    assert "at the time of a person's birth" in SOLAR_RETURN_RULE
    assert "belong to that nativity" in (
        THE_ANNUAL_CHART_IS_THE_CHART_SENSITIVE_METHOD_26_9_ASKED_FOR)


def test_part_4_names_none_of_the_dasas_it_promises():
    from hora.core.const import (
        DASAS_WITHIN_THE_YEAR,
        PART_3_IS_KNOWINGLY_PARTIAL,
        PART_4_NAMES_NONE_OF_ITS_DASAS,
    )
    from hora.core.constants.transit import CHAPTER_26_NAMES_NOTHING_IT_WILL_COVER

    assert "A few special dasa systems" in DASAS_WITHIN_THE_YEAR
    assert "Vimsottari" not in DASAS_WITHIN_THE_YEAR
    assert "Mudda" not in DASAS_WITHIN_THE_YEAR
    # The same omission three parts running; Part 2's list is still the only
    # checkable one.
    assert "Some of those techniques" in PART_3_IS_KNOWINGLY_PARTIAL
    assert "names none of them" in CHAPTER_26_NAMES_NOTHING_IT_WILL_COVER
    assert "remains the only checkable list" in PART_4_NAMES_NONE_OF_ITS_DASAS

    from hora.core.const import PART_2_DASA_SYSTEMS
    assert len(PART_2_DASA_SYSTEMS) == 9


def test_the_two_chart_kinds_are_recorded_with_what_each_covers():
    from hora.core.const import (
        MASA_CHAKRA_RULE,
        TAJAKA_CHART_KINDS,
    )

    assert len(TAJAKA_CHART_KINDS) == 2
    annual, monthly = TAJAKA_CHART_KINDS
    assert annual["chart"] == "Tajaka annual chart"
    assert annual["cast_for"] == "the Sun's return to its natal longitude"
    assert monthly["chart"] == "Tajaka masa chakra"
    # The monthly chart is named and its casting is not given.
    assert monthly["cast_for"] == ""
    assert "monthly solar return charts" in MASA_CHAKRA_RULE
    assert "one-month period" in MASA_CHAKRA_RULE


def test_the_365_day_year_is_flagged_and_not_resolved():
    """The page says 365 days; a sidereal solar return is about 365.2564. The
    difference is recorded rather than decided, because the section that
    supplies the special dasas has not arrived.
    """
    from hora.core.const import (
        DASAS_WITHIN_THE_YEAR,
        THE_YEAR_IS_CALLED_365_DAYS_AND_A_SOLAR_RETURN_IS_LONGER,
    )
    from hora.core.constants.timespan import SIDEREAL_YEAR_DAYS
    from hora.core.settings import DashaYearLength

    assert "365-day period" in DASAS_WITHIN_THE_YEAR
    assert SIDEREAL_YEAR_DAYS > 365.0
    assert round(SIDEREAL_YEAR_DAYS - 365.0, 4) == pytest.approx(0.2564,
                                                                 abs=5e-4)
    # Both readings are already settings, so neither is baked in anywhere.
    assert {"sidereal", "civil"} <= {m.value for m in DashaYearLength}
    assert "is not stated here" in (
        THE_YEAR_IS_CALLED_365_DAYS_AND_A_SOLAR_RETURN_IS_LONGER)


def test_three_earlier_passages_were_waiting_on_this_part():
    from hora.core.const import TAJAKA_WAS_PROMISED_BY
    from hora.dasha.nakshatra.kalachakra import FOOTNOTE_68
    from hora.transits.tara import FOOTNOTE_74

    assert "Tajaka annual and monthly charts" in FOOTNOTE_68
    assert "Tajaka charts also show death" in FOOTNOTE_74 or (
        "Tajaka charts" in FOOTNOTE_74)
    wants = {row["where"] for row in TAJAKA_WAS_PROMISED_BY}
    assert {"footnote 68", "footnote 74"} <= wants
    assert any("OI-116" in row["where"] for row in TAJAKA_WAS_PROMISED_BY)


def test_the_opening_defers_the_casting_and_27_1_supplies_it():
    """The opening page gives no moment, place or ayanamsa rule. Section 27.1
    gives the first two. Neither says how to READ an annual chart, so footnote
    74's bar on death readings still stands.
    """
    from hora.core.const import (
        PART_4_SCOPE,
        THE_OPENING_PROMISES_THE_CASTING_AND_27_1_GIVES_IT,
    )
    from hora.tajaka.annual import BIRTHPLACE_RULE, VARSHA_PRAVESH_RULE
    from hora.transits.tara import (
        THE_TECHNIQUE_NEEDS_DASAS_AND_TAJAKA_TO_BE_USED_AT_ALL,
    )

    assert "explains the casting" in PART_4_SCOPE
    assert "exact moment" in VARSHA_PRAVESH_RULE
    assert "birthplace" in BIRTHPLACE_RULE
    assert "nothing yet lifts footnote 74's bar" in (
        THE_OPENING_PROMISES_THE_CASTING_AND_27_1_GIVES_IT)
    assert "never sufficient on its own" in (
        THE_TECHNIQUE_NEEDS_DASAS_AND_TAJAKA_TO_BE_USED_AT_ALL)
