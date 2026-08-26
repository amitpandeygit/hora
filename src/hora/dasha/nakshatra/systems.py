"""Descriptors for the nakshatra-based dasha systems JHora supports."""
from __future__ import annotations

from hora.core.const import Graha
from hora.dasha.base import NakshatraDashaSpec

VIMSHOTTARI = NakshatraDashaSpec(
    key="vimshottari",
    display_name="Vimshottari",
    order=(Graha.KETU, Graha.VENUS, Graha.SUN, Graha.MOON, Graha.MARS,
           Graha.RAHU, Graha.JUPITER, Graha.SATURN, Graha.MERCURY),
    years=(7, 20, 6, 10, 7, 18, 16, 19, 17),
)

ASHTOTTARI = NakshatraDashaSpec(
    key="ashtottari",
    display_name="Ashtottari",
    order=(Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY,
           Graha.SATURN, Graha.JUPITER, Graha.RAHU, Graha.VENUS),
    years=(6, 15, 8, 17, 10, 19, 12, 21),
)

DWADASOTTARI = NakshatraDashaSpec(
    key="dwadasottari",
    display_name="Dwadasottari",
    order=(Graha.SUN, Graha.JUPITER, Graha.KETU, Graha.MERCURY,
           Graha.RAHU, Graha.MARS, Graha.SATURN, Graha.MOON),
    years=(7, 9, 11, 13, 15, 17, 19, 21),
)

SHATTRIMSA_SAMA = NakshatraDashaSpec(
    key="shattrimsa_sama",
    display_name="Shattrimsa Sama",
    order=(Graha.MOON, Graha.SUN, Graha.JUPITER, Graha.MARS,
           Graha.MERCURY, Graha.SATURN, Graha.VENUS, Graha.KETU),
    years=(1, 2, 3, 4, 5, 6, 7, 8),
)

DWISAPTATI_SAMA = NakshatraDashaSpec(
    key="dwisaptati_sama",
    display_name="Dwisaptati Sama",
    order=(Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY,
           Graha.JUPITER, Graha.VENUS, Graha.SATURN, Graha.RAHU),
    years=(9, 9, 9, 9, 9, 9, 9, 9),
)

CHATURASEETI_SAMA = NakshatraDashaSpec(
    key="chaturaseeti_sama",
    display_name="Chaturaseeti Sama",
    order=(Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY,
           Graha.JUPITER, Graha.VENUS, Graha.SATURN),
    years=(12, 12, 12, 12, 12, 12, 12),
)

SATAABDIKA = NakshatraDashaSpec(
    key="sataabdika",
    display_name="Sataabdika",
    order=(Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY,
           Graha.JUPITER, Graha.VENUS, Graha.SATURN),
    years=(5, 5, 10, 10, 20, 20, 30),
)

SHODASOTTARI = NakshatraDashaSpec(
    key="shodasottari",
    display_name="Shodasottari",
    order=(Graha.SUN, Graha.MARS, Graha.JUPITER, Graha.SATURN,
           Graha.KETU, Graha.MOON, Graha.MERCURY, Graha.VENUS),
    years=(11, 12, 13, 14, 15, 16, 17, 18),
)

PANCHOTTARI = NakshatraDashaSpec(
    key="panchottari",
    display_name="Panchottari",
    order=(Graha.SUN, Graha.MERCURY, Graha.SATURN, Graha.MARS,
           Graha.VENUS, Graha.MOON, Graha.JUPITER),
    years=(12, 13, 14, 15, 16, 17, 18),
)

SHASHTIHAYANI = NakshatraDashaSpec(
    key="shashtihayani",
    display_name="Shashtihayani",
    order=(Graha.JUPITER, Graha.SUN, Graha.MARS, Graha.VENUS,
           Graha.MERCURY, Graha.MOON, Graha.SATURN, Graha.RAHU),
    years=(10, 10, 10, 10, 10, 5, 4, 1),
)

#: PARITY: the starting-nakshatra rule differs per system in JHora (some count
#: from Ashwini, some from Krittika, Ashtottari from Ardra). Only Vimshottari's
#: rule is confirmed; the rest use the plain modulo rule until pinned.
NAKSHATRA_DASHA_SYSTEMS = {
    s.key: s
    for s in (
        VIMSHOTTARI, ASHTOTTARI, DWADASOTTARI, SHATTRIMSA_SAMA, DWISAPTATI_SAMA,
        CHATURASEETI_SAMA, SATAABDIKA, SHODASOTTARI, PANCHOTTARI, SHASHTIHAYANI,
    )
}
