"""Nakshatras and the Vimsottari lord cycle (book chapter 1).

Split out of the former single ``const.py``. Import from
:mod:`hora.core.const`, which re-exports every constant — that facade is the
stable internal surface and keeps call sites independent of how the tables are
filed.
"""
from __future__ import annotations

from hora.core.constants.graha import Graha

# --------------------------------------------------------------------------
# Nakshatras
# --------------------------------------------------------------------------

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]

#: Transliterations exactly as printed in Table 2 of "Vedic Astrology: An
#: Integrated Approach". These are the default output names; the list above is
#: available as the ``standard`` name scheme.
NAKSHATRA_NAMES_BOOK = [
    "Aswini", "Bharani", "Krittika", "Rohini", "Mrigasira", "Aardra",
    "Punarvasu", "Pushyami", "Aasresha", "Makha", "Poorva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swaati", "Visaakha", "Anooraadha", "Jyeshtha",
    "Moola", "Poorvaashaadha", "Uttaraashaadha", "Sravanam", "Dhanishtha", "Satabhishak",
    "Poorvaabhaadra", "Uttaraabhaadra", "Revati",
]

#: Table 2's fourth column — the deity ruling each nakshatra.
#: "Ahirbudhanya" is printed as "Ahirbudhany a" in the PDF, a line-break
#: artefact rather than the book's own spelling.
NAKSHATRA_DEITY = [
    "Aswini Kumara", "Yama", "Agni", "Bramha", "Moon", "Shiva",
    "Aditi", "Jupiter", "Rahu", "Sun", "Aryaman", "Sun",
    "Viswakarma", "Vaayu", "Indra", "Mitra", "Indra", "Nirriti",
    "Varuna", "Viswadeva", "Brahma", "Vishnu", "Vasu", "Varuna",
    "Ajacharana", "Ahirbudhanya", "Pooshan",
]

#: §1.3.6: "the zodiac is divided into 27 nakshatras".
NAKSHATRA_COUNT = 27
#: The book spells one nakshatra two ways: Table 2 (§1.3.6) prints "Swaati",
#: §5.7's Example 10 prints "Swathi". Both are PVR's; NAKSHATRA_NAMES_BOOK
#: carries Table 2's, because that is where the twenty-seven are defined.
NAKSHATRA_NAME_VARIANTS: dict[str, str] = {"Swaati": "Swathi"}

NAKSHATRA_SPAN = 360.0 / 27.0        # 13 deg 20 min
PADA_SPAN = NAKSHATRA_SPAN / 4.0     # 3 deg 20 min

#: §1.3.6: "Each nakshatra is again divided into 4 quarters. They are called
#: padas (legs/feet)."
PADAS_PER_NAKSHATRA = 4
PADA_GLOSS = "legs/feet"

#: §1.3.6's exception, in its own words.
ABHIJIT_RULE = (
    "For the purpose of some special charts like Kota Chakra and "
    "Sarvatobhadra Chakra, we consider 28 nakshatras. The last quarter of "
    "Uttarashadha is known as \"Abhijit\". However, we consider 27 nakshatras "
    "for all other purposes."
)
NAKSHATRA_COUNT_SPECIAL = 28
TWENTY_EIGHT_NAKSHATRA_CHARTS: tuple[str, ...] = (
    "Kota Chakra", "Sarvatobhadra Chakra",
)

#: Abhijit's extent. Used only for Kota Chakra, Sarvatobhadra Chakra and
#: similar; every other calculation uses 27 nakshatras.
#:
#: **These bounds do not match §1.3.6.** The book says Abhijit *is* "the last
#: quarter of Uttarashadha", which ends at 10 Cp 00. ABHIJIT_END below runs to
#: 10 Cp 53'20", adding the first 1/15 of Sravana — the classical Muhurta
#: definition, which §1.3.6 does not give. Unresolved; see
#: docs/open-items.md OI-36. Not changed pending a decision, because altering
#: a boundary silently is worse than a documented disagreement.
ABHIJIT_INDEX = 27
ABHIJIT_START = 20 * NAKSHATRA_SPAN + 3 * PADA_SPAN     # 26 Cp 40 -> 276.6667
ABHIJIT_END = 21 * NAKSHATRA_SPAN + NAKSHATRA_SPAN / 15.0
NAKSHATRA_NAMES_28 = [*NAKSHATRA_NAMES, "Abhijit"]
NAKSHATRA_NAMES_28_BOOK = [*NAKSHATRA_NAMES_BOOK, "Abhijit"]

#: Vimshottari lord of each nakshatra, repeating in the Ketu..Mercury order.
VIMSHOTTARI_ORDER = [
    Graha.KETU, Graha.VENUS, Graha.SUN, Graha.MOON, Graha.MARS,
    Graha.RAHU, Graha.JUPITER, Graha.SATURN, Graha.MERCURY,
]
VIMSHOTTARI_YEARS = {
    Graha.KETU: 7, Graha.VENUS: 20, Graha.SUN: 6, Graha.MOON: 10, Graha.MARS: 7,
    Graha.RAHU: 18, Graha.JUPITER: 16, Graha.SATURN: 19, Graha.MERCURY: 17,
}
NAKSHATRA_LORD = [VIMSHOTTARI_ORDER[i % 9] for i in range(27)]
