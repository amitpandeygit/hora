"""§1.3.6 Nakshatras (constellations) — Table 2 and the section's statements.

Table 2 was already right: 27 rows of name, Vimsottari lord and ruling deity,
and boundaries that follow from the 13 deg 20 min span. What was missing was
the prose — the pada gloss, the counts, and the 28-nakshatra exception.

One assertion here **documents a disagreement rather than a pass**: see
`test_abhijit_end_does_not_match_the_book`.
"""
import pytest

from hora.core import const as c

ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]


def dms(longitude: float) -> str:
    """Render as the "00 Ar 00" form Table 2 prints."""
    lon = longitude % 360.0
    sign, within = int(lon // 30), lon - int(lon // 30) * 30
    return f"{int(within):02d} {ABBR[sign]} {round((within - int(within)) * 60):02d}"


# --------------------------------------------------------------------------
# Table 2
# --------------------------------------------------------------------------

#: Table 2 as printed: name, Vimsottari lord, ruling deity.
TABLE_2 = [
    ("Aswini", "Ketu", "Aswini Kumara"), ("Bharani", "Venus", "Yama"),
    ("Krittika", "Sun", "Agni"), ("Rohini", "Moon", "Bramha"),
    ("Mrigasira", "Mars", "Moon"), ("Aardra", "Rahu", "Shiva"),
    ("Punarvasu", "Jupiter", "Aditi"), ("Pushyami", "Saturn", "Jupiter"),
    ("Aasresha", "Mercury", "Rahu"), ("Makha", "Ketu", "Sun"),
    ("Poorva Phalguni", "Venus", "Aryaman"), ("Uttara Phalguni", "Sun", "Sun"),
    ("Hasta", "Moon", "Viswakarma"), ("Chitra", "Mars", "Vaayu"),
    ("Swaati", "Rahu", "Indra"), ("Visaakha", "Jupiter", "Mitra"),
    ("Anooraadha", "Saturn", "Indra"), ("Jyeshtha", "Mercury", "Nirriti"),
    ("Moola", "Ketu", "Varuna"), ("Poorvaashaadha", "Venus", "Viswadeva"),
    ("Uttaraashaadha", "Sun", "Brahma"), ("Sravanam", "Moon", "Vishnu"),
    ("Dhanishtha", "Mars", "Vasu"), ("Satabhishak", "Rahu", "Varuna"),
    ("Poorvaabhaadra", "Jupiter", "Ajacharana"),
    ("Uttaraabhaadra", "Saturn", "Ahirbudhanya"),
    ("Revati", "Mercury", "Pooshan"),
]


@pytest.mark.parametrize("index,row", list(enumerate(TABLE_2)))
def test_table_2_name_lord_and_deity(index, row):
    name, lord, deity = row
    assert c.NAKSHATRA_NAMES_BOOK[index] == name
    assert c.GRAHA_NAMES[c.NAKSHATRA_LORD[index]] == lord
    assert c.NAKSHATRA_DEITY[index] == deity


@pytest.mark.parametrize("index,starts", [
    (0, "00 Ar 00"), (1, "13 Ar 20"), (2, "26 Ar 40"), (3, "10 Ta 00"),
    (9, "00 Le 00"), (18, "00 Sg 00"), (20, "26 Sg 40"), (26, "16 Pi 40"),
])
def test_table_2_start_boundaries(index, starts):
    """The "Starts at" column, which follows from the span."""
    assert dms(index * c.NAKSHATRA_SPAN) == starts


def test_the_twenty_seventh_ends_at_the_end_of_the_zodiac():
    """Revati "Ends at" 30 Pi 00 — the zodiac closing on itself."""
    assert 27 * c.NAKSHATRA_SPAN == pytest.approx(360.0)


# --------------------------------------------------------------------------
# The counts and spans
# --------------------------------------------------------------------------

def test_twenty_seven_nakshatras_of_thirteen_twenty():
    """"the zodiac is divided into 27 nakshatras. Each nakshatra has a length
    of 360/27 = 13 deg 20 min"."""
    assert c.NAKSHATRA_COUNT == 27
    assert len(c.NAKSHATRA_NAMES) == 27
    assert c.NAKSHATRA_SPAN == pytest.approx(13 + 20 / 60)
    assert c.NAKSHATRA_SPAN == 360.0 / 27.0


def test_four_padas_of_three_twenty():
    """"Each nakshatra is again divided into 4 quarters. They are called padas
    (legs/feet). The length of a nakshatra pada is 3 deg 20 min."""
    assert c.PADAS_PER_NAKSHATRA == 4
    assert c.PADA_GLOSS == "legs/feet"
    assert c.PADA_SPAN == pytest.approx(3 + 20 / 60)
    assert c.PADA_SPAN * 4 == pytest.approx(c.NAKSHATRA_SPAN)


def test_the_first_three_nakshatras_stretch_where_the_section_says():
    """"The first nakshatra stretches from the beginning of Aries to 13 deg
    20 min in Aries. The second stretches from there to 26 deg 40 min in
    Aries. The third stretches from there to 10 deg in Taurus."""
    assert dms(1 * c.NAKSHATRA_SPAN) == "13 Ar 20"
    assert dms(2 * c.NAKSHATRA_SPAN) == "26 Ar 40"
    assert dms(3 * c.NAKSHATRA_SPAN) == "10 Ta 00"


# --------------------------------------------------------------------------
# The 28-nakshatra exception
# --------------------------------------------------------------------------

def test_the_abhijit_rule_is_stored_verbatim():
    rule = c.ABHIJIT_RULE
    assert "Kota Chakra and Sarvatobhadra Chakra" in rule
    assert "we consider 28 nakshatras" in rule
    assert "The last quarter of Uttarashadha is known as \"Abhijit\"" in rule
    assert "we consider 27 nakshatras for all other purposes" in rule


def test_the_special_charts_are_named():
    assert c.TWENTY_EIGHT_NAKSHATRA_CHARTS == (
        "Kota Chakra", "Sarvatobhadra Chakra"
    )
    assert c.NAKSHATRA_COUNT_SPECIAL == 28
    assert len(c.NAKSHATRA_NAMES_28) == 28


def test_abhijit_starts_at_the_last_quarter_of_uttarashadha():
    """6 Cp 40 — the start the section gives, and parity.md's claim."""
    last_pada = 20 * c.NAKSHATRA_SPAN + 3 * c.PADA_SPAN
    assert c.ABHIJIT_START == pytest.approx(last_pada)
    assert dms(c.ABHIJIT_START) == "06 Cp 40"


def test_abhijit_end_does_not_match_the_book():
    """**This test documents a disagreement, not a pass.** See OI-36.

    §1.3.6 says Abhijit *is* "the last quarter of Uttarashadha", which ends
    where Uttarashadha does, at 10 Cp 00. `ABHIJIT_END` runs to 10 Cp 53'20",
    adding the first 1/15 of Sravana — the classical Muhurta definition, which
    this section does not give.

    Pinned so the discrepancy cannot be closed by accident in either
    direction: changing the constant fails this test and forces the decision
    to be taken deliberately.
    """
    uttarashadha_ends = 21 * c.NAKSHATRA_SPAN
    assert dms(uttarashadha_ends) == "10 Cp 00", "what the book's wording gives"
    assert c.ABHIJIT_END != pytest.approx(uttarashadha_ends), (
        "if this now passes, the constant was changed — update OI-36"
    )
    surplus = c.ABHIJIT_END - uttarashadha_ends
    assert surplus == pytest.approx(c.NAKSHATRA_SPAN / 15)
    assert surplus == pytest.approx(53 / 60 + 20 / 3600)


def test_abhijit_occupies_the_twenty_eighth_slot():
    assert c.ABHIJIT_INDEX == 27       # 0-based, so the 28th


# --------------------------------------------------------------------------
# Published
# --------------------------------------------------------------------------

def test_the_section_is_published():
    from hora.services import reference_service

    payload = reference_service.terms()["nakshatra"]
    assert payload["count"] == 27
    assert payload["padas_each"] == 4
    assert payload["pada_gloss"] == "legs/feet"
    assert payload["count_for_special_charts"] == 28
    assert payload["special_charts"] == list(c.TWENTY_EIGHT_NAKSHATRA_CHARTS)
    assert payload["abhijit_rule"] == c.ABHIJIT_RULE


def test_the_abhijit_bounds_reach_a_live_api_field():
    """OI-36's blast radius, asserted rather than assumed.

    `abhijit_active` on /v1/panchanga is computed from these bounds, so
    changing ABHIJIT_END changes shipped output. An earlier draft of OI-36
    claimed the constants were unused; this test exists so that claim cannot
    be made again without failing.
    """
    import inspect

    from hora.panchanga import core

    source = inspect.getsource(core)
    assert "ABHIJIT_START" in source and "ABHIJIT_END" in source
    assert "abhijit_active" in source


def test_the_disputed_arc_is_fifty_three_arcminutes():
    """The size of the disagreement, so its cost is visible in OI-36."""
    disputed = c.ABHIJIT_END - 21 * c.NAKSHATRA_SPAN
    assert disputed == pytest.approx(53 / 60 + 20 / 3600)
    # Just under a quarter of one percent of the zodiac.
    assert disputed / 360 == pytest.approx(0.00247, abs=1e-5)
