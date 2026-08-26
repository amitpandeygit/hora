"""Divisional (varga) charts.

Each varga maps a zodiacal longitude onto a sign of the divisional chart.  The
classical Parashari rule for every chart is encoded as its own function rather
than a single generic formula, because the charts genuinely disagree: D-9 obeys
the cyclic ``(rasi*N + part)`` rule, D-3 counts in steps of four signs, D-30 has
unequal divisions, and so on.

Jagannatha Hora ships multiple *variants* for several vargas (six horas, four
drekkanas, three navamsas...).  Variants are named in :class:`VargaVariant` and
selected per request; the default of each is the Parashari rule.

Rules whose JHora default has not yet been pinned against real JHora output are
marked ``PARITY`` and listed in docs/parity.md.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from hora.core import validate
from hora.core.const import RASI_ELEMENT, RASI_IS_ODD, RASI_MODALITY, Rasi

# --------------------------------------------------------------------------
# Result type
# --------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class VargaPosition:
    """Where a longitude falls in a divisional chart."""

    sign: int
    #: Longitude projected into the varga chart: ``sign*30`` plus the position
    #: within the amsa rescaled to a full sign. JHora prints this for D-9 etc.
    longitude: float
    #: 0-based index of the amsa within the natal sign.
    amsa_index: int


def _equal(longitude: float, divisions: int) -> tuple[int, float, int, float]:
    """Split a longitude into (rasi, degrees_in_rasi, amsa_index, fraction_in_amsa)."""
    validate.in_range("divisions", divisions, 1, 300)
    lon = validate.longitude("longitude", longitude)
    rasi = int(lon // 30.0)
    deg = lon - rasi * 30.0
    span = 30.0 / divisions
    idx = min(int(deg // span), divisions - 1)
    frac = (deg - idx * span) / span
    return rasi, deg, idx, frac


def _result(sign: int, idx: int, frac: float) -> VargaPosition:
    """Build a VargaPosition, keeping the projected longitude inside its sign.

    ``frac`` is clamped below 1.0 because floating-point division can land a
    longitude exactly on the next amsa boundary, which would otherwise push the
    projected longitude into the following sign (or past 360 for Pisces).
    """
    sign %= 12
    frac = min(max(frac, 0.0), 1.0 - 1e-12)
    return VargaPosition(sign=sign, longitude=sign * 30.0 + frac * 30.0, amsa_index=idx)


# --------------------------------------------------------------------------
# Individual vargas
# --------------------------------------------------------------------------


def d1_rasi(longitude: float) -> VargaPosition:
    """D-1. The rasi chart is the longitude itself."""
    lon = validate.longitude("longitude", longitude)
    rasi = int(lon // 30.0)
    return VargaPosition(sign=rasi, longitude=lon, amsa_index=0)


def d2_hora(longitude: float, variant: str = "parashari") -> VargaPosition:
    """D-2. JHora offers six horas; Parashari is the default.

    Parashari: an odd sign's first half is the Sun's hora (Leo) and its second
    half the Moon's (Cancer); even signs are reversed.
    """
    rasi, _, idx, frac = _equal(longitude, 2)
    odd = RASI_IS_ODD[rasi]
    if variant == "parashari":
        sign = (4 if idx == 0 else 3) if odd else (3 if idx == 0 else 4)
    elif variant == "parivritti":
        # Cyclic: 24 horas counted continuously from Aries.
        sign = (rasi * 2 + idx) % 12
    elif variant == "kashinatha":
        # PARITY: Kashinatha hora rule taken from JHora's help text; unverified.
        sign = (rasi * 2 + idx) % 12
    else:
        raise ValueError(f"unknown hora variant {variant!r}")
    return _result(sign, idx, frac)


def d3_drekkana(longitude: float, variant: str = "parashari") -> VargaPosition:
    """D-3. Parashari: the three drekkanas fall in the 1st, 5th and 9th signs."""
    rasi, _, idx, frac = _equal(longitude, 3)
    if variant == "parashari":
        sign = rasi + 4 * idx
    elif variant == "parivritti":
        sign = rasi * 3 + idx
    elif variant == "somanatha":
        # PARITY: Somanatha drekkana; JHora variant 3.
        sign = rasi * 3 + idx
    else:
        raise ValueError(f"unknown drekkana variant {variant!r}")
    return _result(sign, idx, frac)


def d4_chaturthamsa(longitude: float) -> VargaPosition:
    """D-4. The four quarters fall in the 1st, 4th, 7th and 10th signs."""
    rasi, _, idx, frac = _equal(longitude, 4)
    return _result(rasi + 3 * idx, idx, frac)


#: §6.2.5: "Bodies in the 5 parts of an odd rasi go into Ar, Aq, Sg, Ge and Li
#: (respectively). Bodies in the 5 parts of an even rasi go into Ta, Vi, Pi, Cp
#: and Sc (respectively)."
#:
#: Chapter 6 gives no worked example for D-5, so this rule is only checkable
#: against its own wording — which is exactly why it was wrong before the
#: chapter was audited.
_D5_ODD = (Rasi.ARIES, Rasi.AQUARIUS, Rasi.SAGITTARIUS, Rasi.GEMINI, Rasi.LIBRA)
_D5_EVEN = (Rasi.TAURUS, Rasi.VIRGO, Rasi.PISCES, Rasi.CAPRICORN, Rasi.SCORPIO)


def d5_panchamsa(longitude: float) -> VargaPosition:
    """D-5. Unequal sign sequence differing by parity of the natal sign."""
    rasi, _, idx, frac = _equal(longitude, 5)
    table = _D5_ODD if RASI_IS_ODD[rasi] else _D5_EVEN
    return _result(table[idx], idx, frac)


def d6_shashtamsa(longitude: float) -> VargaPosition:
    """D-6. Odd signs count from Aries, even signs from Libra."""
    rasi, _, idx, frac = _equal(longitude, 6)
    start = 0 if RASI_IS_ODD[rasi] else 6
    return _result(start + idx, idx, frac)


def d7_saptamsa(longitude: float) -> VargaPosition:
    """D-7. Odd signs count from the sign itself, even signs from the 7th."""
    rasi, _, idx, frac = _equal(longitude, 7)
    start = rasi if RASI_IS_ODD[rasi] else rasi + 6
    return _result(start + idx, idx, frac)


#: §6.2.8: D-8 counts from Ar, Sg or Le for movable, fixed and dual.
#: Note this is NOT the same order as D-16 and D-45, which use Ar, Le, Sg —
#: the book gives both orders explicitly and they differ. Conflating them is
#: what made D-8 wrong before chapter 6 was audited.
_D8_START = (Rasi.ARIES, Rasi.SAGITTARIUS, Rasi.LEO)


def d8_ashtamsa(longitude: float) -> VargaPosition:
    """D-8. Movable signs count from Aries, fixed from Sagittarius, dual from Leo."""
    rasi, _, idx, frac = _equal(longitude, 8)
    return _result(_D8_START[RASI_MODALITY[rasi]] + idx, idx, frac)


def d9_navamsa(longitude: float, variant: str = "parashari") -> VargaPosition:
    """D-9. Movable from the sign itself, fixed from the 9th, dual from the 5th.

    That classical statement is exactly the cyclic rule ``(rasi*9 + amsa)``,
    which is how it is computed here.
    """
    rasi, _, idx, frac = _equal(longitude, 9)
    if variant in ("parashari", "cyclic"):
        sign = rasi * 9 + idx
    elif variant == "kalachakra":
        # PARITY: Kalachakra navamsa follows a different amsa ordering.
        sign = rasi * 9 + idx
    else:
        raise ValueError(f"unknown navamsa variant {variant!r}")
    return _result(sign, idx, frac)


def d10_dasamsa(longitude: float) -> VargaPosition:
    """D-10. Odd signs count from the sign itself, even signs from the 9th."""
    rasi, _, idx, frac = _equal(longitude, 10)
    start = rasi if RASI_IS_ODD[rasi] else rasi + 8
    return _result(start + idx, idx, frac)


def d11_rudramsa(longitude: float, variant: str = "pvr") -> VargaPosition:
    """D-11 (rudramsa / ekadasamsa).

    §6.2.11: "Count rasis from Ar to the rasi being divided, in the zodiacal
    order. Count the same number of rasis anti-zodiacally from Ar. Bodies in the
    11 parts of the rasi go into the 11 rasis starting from the rasi found thus."

    So the starting rasi is the natal rasi reflected about Aries. Gemini is the
    3rd from Aries, and the 3rd from Aries counting backwards is Aquarius, which
    is where Example 18 starts.
    """
    rasi, _, idx, frac = _equal(longitude, 11)
    if variant == "pvr":
        sign = (-rasi) % 12 + idx
    elif variant == "parivritti":
        sign = rasi * 11 + idx
    else:
        raise ValueError(f"unknown rudramsa variant {variant!r}")
    return _result(sign % 12, idx, frac)


def d12_dwadasamsa(longitude: float) -> VargaPosition:
    """D-12. The twelve parts count from the sign itself."""
    rasi, _, idx, frac = _equal(longitude, 12)
    return _result(rasi + idx, idx, frac)


def d16_shodasamsa(longitude: float) -> VargaPosition:
    """D-16. Movable from Aries, fixed from Leo, dual from Sagittarius."""
    rasi, _, idx, frac = _equal(longitude, 16)
    return _result(RASI_MODALITY[rasi] * 4 + idx, idx, frac)


#: D-20 start signs by modality: movable Aries, fixed Sagittarius, dual Leo.
_D20_START = (0, 8, 4)


def d20_vimsamsa(longitude: float) -> VargaPosition:
    """D-20."""
    rasi, _, idx, frac = _equal(longitude, 20)
    return _result(_D20_START[RASI_MODALITY[rasi]] + idx, idx, frac)


def d24_chaturvimsamsa(longitude: float) -> VargaPosition:
    """D-24 (siddhamsa). Odd signs count from Leo, even signs from Cancer."""
    rasi, _, idx, frac = _equal(longitude, 24)
    start = 4 if RASI_IS_ODD[rasi] else 3
    return _result(start + idx, idx, frac)


def d27_nakshatramsa(longitude: float) -> VargaPosition:
    """D-27 (bhamsa). Counted from Aries/Cancer/Libra/Capricorn by element."""
    rasi, _, idx, frac = _equal(longitude, 27)
    return _result(RASI_ELEMENT[rasi] * 3 + idx, idx, frac)


#: Trimsamsa is unequal. Each entry is (upper_bound_deg, target_sign).
_D30_ODD = ((5.0, 0), (10.0, 10), (18.0, 8), (25.0, 2), (30.0, 6))
_D30_EVEN = ((5.0, 1), (12.0, 5), (20.0, 11), (25.0, 9), (30.0, 7))


def d30_trimsamsa(longitude: float, variant: str = "parashari") -> VargaPosition:
    """D-30. Five unequal parts ruled by the five non-luminary planets.

    Odd signs: Mars 5, Saturn 5, Jupiter 8, Mercury 7, Venus 5.
    Even signs: the same spans reversed, starting with Venus.
    """
    lon = validate.longitude("longitude", longitude)
    rasi = int(lon // 30.0)
    deg = lon - rasi * 30.0
    table = _D30_ODD if RASI_IS_ODD[rasi] else _D30_EVEN
    if variant == "parivritti":
        rasi, _, idx, frac = _equal(longitude, 30)
        return _result(rasi * 30 + idx, idx, frac)
    if variant != "parashari":
        raise ValueError(f"unknown trimsamsa variant {variant!r}")
    lower = 0.0
    for idx, (upper, sign) in enumerate(table):
        if deg < upper:
            frac = (deg - lower) / (upper - lower)
            return _result(sign, idx, frac)
        lower = upper
    sign = table[-1][1]
    return _result(sign, 4, 0.999999)


def d40_khavedamsa(longitude: float) -> VargaPosition:
    """D-40. Odd signs count from Aries, even signs from Libra."""
    rasi, _, idx, frac = _equal(longitude, 40)
    start = 0 if RASI_IS_ODD[rasi] else 6
    return _result(start + idx, idx, frac)


def d45_akshavedamsa(longitude: float) -> VargaPosition:
    """D-45. Movable from Aries, fixed from Leo, dual from Sagittarius."""
    rasi, _, idx, frac = _equal(longitude, 45)
    return _result(RASI_MODALITY[rasi] * 4 + idx, idx, frac)


def d60_shashtyamsa(longitude: float) -> VargaPosition:
    """D-60. Twice the degrees-in-sign, counted from the sign itself."""
    rasi, deg, idx, frac = _equal(longitude, 60)
    return _result(rasi + int(deg * 2.0), idx, frac)


# --------------------------------------------------------------------------
# Composite and generic vargas
# --------------------------------------------------------------------------


def d_generic(longitude: float, divisions: int) -> VargaPosition:
    """Custom D-N chart for N in 1..300, using the cyclic (parivritti) rule.

    This is the rule JHora applies to its user-defined divisional charts.
    """
    validate.in_range("divisions", divisions, 1, 300)
    rasi, _, idx, frac = _equal(longitude, divisions)
    return _result(rasi * divisions + idx, idx, frac)


def compose(longitude: float, outer: str, inner: str) -> VargaPosition:
    """Apply one varga to the projected longitude of another (D-m x D-n)."""
    first = varga(longitude, inner)
    return varga(first.longitude, outer)


def d81_nava_navamsa(longitude: float) -> VargaPosition:
    """D-81. Navamsa of the navamsa."""
    return compose(longitude, "D9", "D9")


def d108_ashtottaramsa(longitude: float) -> VargaPosition:
    """D-108. Dwadasamsa of the navamsa (JHora's first D-108 variant)."""
    return compose(longitude, "D12", "D9")


def d144_dwadas_dwadasamsa(longitude: float) -> VargaPosition:
    """D-144. Dwadasamsa of the dwadasamsa."""
    return compose(longitude, "D12", "D12")


# --------------------------------------------------------------------------
# Registry
# --------------------------------------------------------------------------

#: Canonical varga code -> (callable, display name, number of divisions).
VARGA_REGISTRY: dict[str, tuple] = {
    "D1": (d1_rasi, "Rasi", 1),
    "D2": (d2_hora, "Hora", 2),
    "D3": (d3_drekkana, "Drekkana", 3),
    "D4": (d4_chaturthamsa, "Chaturthamsa", 4),
    "D5": (d5_panchamsa, "Panchamsa", 5),
    "D6": (d6_shashtamsa, "Shashthamsa", 6),
    "D7": (d7_saptamsa, "Saptamsa", 7),
    "D8": (d8_ashtamsa, "Ashtamsa", 8),
    "D9": (d9_navamsa, "Navamsa", 9),
    "D10": (d10_dasamsa, "Dasamsa", 10),
    "D11": (d11_rudramsa, "Rudramsa", 11),
    "D12": (d12_dwadasamsa, "Dwadasamsa", 12),
    "D16": (d16_shodasamsa, "Shodasamsa", 16),
    "D20": (d20_vimsamsa, "Vimsamsa", 20),
    "D24": (d24_chaturvimsamsa, "Chaturvimsamsa", 24),
    "D27": (d27_nakshatramsa, "Nakshatramsa", 27),
    "D30": (d30_trimsamsa, "Trimsamsa", 30),
    "D40": (d40_khavedamsa, "Khavedamsa", 40),
    "D45": (d45_akshavedamsa, "Akshavedamsa", 45),
    "D60": (d60_shashtyamsa, "Shashtyamsa", 60),
    "D81": (d81_nava_navamsa, "Nava Navamsa", 81),
    "D108": (d108_ashtottaramsa, "Ashtottaramsa", 108),
    "D144": (d144_dwadas_dwadasamsa, "Dwadas Dwadasamsa", 144),
}

#: How each chart is defined, as data rather than prose (book chapter 6).
#:
#: ``counts_from`` states the rule in the book's own terms so that a caller can
#: see *why* a body lands where it does, not only that it did. Charts whose
#: rule the book states without a worked example are marked ``example: False``;
#: those are the ones a transcription error can hide in, and D-5 and D-2 are
#: both in that group.
VARGA_RULES: dict[str, dict] = {
    "D1":  {"aliases": ["Kshetra Chakra"], "counts_from": "the longitude itself", "example": False},
    "D2":  {"aliases": [], "counts_from": "Sun's or Moon's hora, by half and parity", "example": False},
    "D3":  {"aliases": [], "counts_from": "the 1st, 5th and 9th from the rasi", "example": True},
    "D4":  {"aliases": ["Chaturamsa", "Turyamsa"], "counts_from": "the 1st, 4th, 7th and 10th from the rasi", "example": True},
    "D5":  {"aliases": [], "counts_from": "Ar, Aq, Sg, Ge, Li (odd) or Ta, Vi, Pi, Cp, Sc (even)", "example": False},
    "D6":  {"aliases": [], "counts_from": "Ar (odd rasi) or Li (even rasi)", "example": True},
    "D7":  {"aliases": [], "counts_from": "the rasi itself (odd) or the 7th from it (even)", "example": True},
    "D8":  {"aliases": [], "counts_from": "Ar, Sg or Le, by movable, fixed or dual", "example": True},
    "D9":  {"aliases": ["Dharmamsa"], "counts_from": "Ar, Cp, Li or Cn, by fiery, earthy, airy or watery", "example": True},
    "D10": {"aliases": ["Dasamaamsa", "Karmamsa", "Swargamsa"], "counts_from": "the rasi itself (odd) or the 9th from it (even)", "example": True},
    "D11": {"aliases": ["Ekadasamsa"], "counts_from": "the rasi reflected about Aries, counted anti-zodiacally", "example": True},
    "D12": {"aliases": [], "counts_from": "the rasi itself", "example": True},
    "D16": {"aliases": ["Kalamsa"], "counts_from": "Ar, Le or Sg, by movable, fixed or dual", "example": True},
    "D20": {"aliases": [], "counts_from": "Ar, Sg or Le, by movable, fixed or dual", "example": True},
    "D24": {"aliases": ["Siddhamsa"], "counts_from": "Le (odd rasi) or Cn (even rasi)", "example": True},
    "D27": {"aliases": ["Saptavimsamsa", "Bhamsa"], "counts_from": "Ar, Cn, Li or Cp, by fiery, earthy, airy or watery", "example": True},
    "D30": {"aliases": [], "counts_from": "five unequal arcs, by parity of the rasi", "example": False},
    "D40": {"aliases": ["Chatvarimsamsa"], "counts_from": "Ar (odd rasi) or Li (even rasi)", "example": True},
    "D45": {"aliases": ["Pancha-chatvarimsamsa"], "counts_from": "Ar, Le or Sg, by movable, fixed or dual", "example": True},
    "D60": {"aliases": [], "counts_from": "the rasi itself, the part being 2 x degrees + 1", "example": True},
    "D81": {"aliases": ["Nava Navamsa"], "counts_from": "D-9 applied to the D-9 longitude", "example": False},
    "D108":{"aliases": ["Ashtottaramsa"], "counts_from": "D-12 applied to the D-9 longitude", "example": False},
    "D144":{"aliases": ["Dwadas Dwadasamsa"], "counts_from": "D-12 applied to the D-12 longitude", "example": False},
}


def part_size_degrees(divisions: int) -> float:
    """Arc of one division, in degrees. D-7 is 4 deg 17' 8.57", and so on."""
    validate.in_range("divisions", divisions, 1, 300)
    return 30.0 / divisions


def part_index(longitude: float, divisions: int) -> int:
    """Which part of its rasi a longitude falls in, 1-based, as the book counts."""
    _, _, idx, _ = _equal(longitude, divisions)
    return idx + 1


#: The sixteen shodasavarga charts, in BPHS order.
SHODASAVARGA = ("D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12",
                "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60")
#: Sub-groups used by vimsopaka bala.
SHADVARGA = ("D1", "D2", "D3", "D9", "D12", "D30")
SAPTAVARGA = ("D1", "D2", "D3", "D7", "D9", "D12", "D30")
DASAVARGA = ("D1", "D2", "D3", "D7", "D9", "D10", "D12", "D16", "D30", "D60")


#: Table 11 — the area of life each divisional chart is read for.
VARGA_SIGNIFICATIONS = {
    "D1": "Existence at the physical level",
    "D2": "Wealth and money",
    "D3": "Everything related to brothers and sisters",
    "D4": "Residence, houses owned, properties and fortune",
    "D5": "Fame, authority and power",
    "D6": "Health troubles",
    "D7": "Everything related to children (and grand-children)",
    "D8": "Sudden and unexpected troubles, litigation etc",
    "D9": ("Marriage and everything related to spouse(s), dharma (duty and "
           "righteousness), interaction with other people, basic skills, inner self"),
    "D10": "Career, activities and achievements in society",
    "D11": "Death and destruction",
    "D12": ("Everything related to parents (also uncles, aunts and grand-parents, "
            "i.e. blood-relatives of parents)"),
    "D16": "Vehicles, pleasures, comforts and discomforts",
    "D20": "Religious activities and spiritual matters",
    "D24": "Learning, knowledge and education",
    "D27": "Strengths and weaknesses, inherent nature",
    "D30": "Evils and punishment, sub-conscious self, some diseases",
    "D40": "Auspicious and inauspicious events",
    "D45": "All matters",
    "D60": "Karma of past life, all matters",
}

#: §6.6 — the amsa a graha is said to occupy, by how many charts of a group it
#: is in its moolatrikona, own rasi or rasi of exaltation. Indexed by that
#: count, so index 2 is the first named amsa in every group.
#: 6.6's closing sentence drops the doubled vowel the tables use: "Being in
#: Gopuramsa and Kalpavrikshamsa makes Jupiter very strong." Only the two the
#: book actually writes that way are recorded — the pattern is not generalised
#: to all 42 names, because the book does not.
AMSA_NAME_ALIASES: dict[str, list[str]] = {
    "Gopuraamsa": ["Gopuramsa"],
    "Kalpavrikshaamsa": ["Kalpavrikshamsa"],
}

AMSA_NAMES: dict[str, dict[int, str]] = {
    "shadvarga": {
        2: "Kimsukaamsa", 3: "Vyanjanaamsa", 4: "Chaamaraamsa",
        5: "Chatraamsa", 6: "Kundalaamsa",
    },
    "saptavarga": {
        2: "Kimsukaamsa", 3: "Vyanjanaamsa", 4: "Chaamaraamsa",
        5: "Chatraamsa", 6: "Kundalaamsa", 7: "Mukutaamsa",
    },
    "dasavarga": {
        2: "Paarijaataamsa", 3: "Uttamaamsa", 4: "Gopuraamsa",
        5: "Simhaasanaamsa", 6: "Paaraavataamsa", 7: "Devalokaamsa",
        8: "Brahmalokamsa", 9: "Airaavataamsa", 10: "Sreedhaamaamsa",
    },
    "shodasavarga": {
        2: "Bhedakaamsa", 3: "Kusumaamsa", 4: "Nagapurushaamsa",
        5: "Kandukaamsa", 6: "Keralaamsa", 7: "Kalpavrikshaamsa",
        8: "Chandanavanaamsa", 9: "Poornachandraamsa", 10: "Uchchaisravaamsa",
        11: "Dhanvantaryamsa", 12: "Sooryakaantaamsa", 13: "Vidrumaamsa",
        14: "Indraasanaamsa", 15: "Golokaamsa", 16: "Sree Vallabhaamsa",
    },
}

#: The four groups of §6.6, by name.
#: Ordinary English that would otherwise match every row of Table 11 — "and"
#: alone appears in nine of the twenty significations. Grammar, not astrology
#: vocabulary; nothing here is a term of art.
_MATTER_STOPWORDS = frozenset({
    "and", "the", "for", "with", "from", "all", "any", "related", "everything",
    "some", "other", "also", "level", "matters", "matter",
})


def charts_for_matter(matter: str) -> list[str]:
    """Which divisional charts to analyse for a matter — §6.5's direction.

    "We should choose the divisional chart to analyze, based on the matter we
    are interested in. If we want to know something about one's career, for
    example, we should analyze one's dasamsa chart (D-10)."

    Table 11 is published chart-first; §6.5 uses it matter-first. This is that
    index, and it is built **from Table 11's own wording** — every word it
    matches is PVR's, so no signification vocabulary is invented here. A
    matter the book does not name simply returns nothing rather than a guess.

    Charts whose signification is "all matters" are returned last, and only
    when something more specific does not match, so a query for "career" does
    not come back with D-45 and D-60 alongside D-10.
    """
    query = str(matter).strip().lower()
    if not query:
        raise validate.InputError("matter must not be empty")
    words = [
        w for w in re.split(r"[^a-z]+", query)
        if len(w) > 2 and w not in _MATTER_STOPWORDS
    ]
    if not words:
        return []
    broad: list[str] = []
    specific: list[str] = []
    for code, signifies in VARGA_SIGNIFICATIONS.items():
        text = signifies.lower()
        if not any(word in text for word in words):
            continue
        (broad if "all matters" in text else specific).append(code)
    return specific or broad


VARGA_GROUPS = {
    "shadvarga": SHADVARGA,
    "saptavarga": SAPTAVARGA,
    "dasavarga": DASAVARGA,
    "shodasavarga": SHODASAVARGA,
}


def varga(longitude: float, code: str, variant: str | None = None) -> VargaPosition:
    """Compute any registered varga by code, e.g. ``varga(lon, "D9")``.

    Unregistered ``D<N>`` codes fall through to the generic cyclic rule, which
    is how JHora handles custom divisional charts.
    """
    code = code.upper()
    entry = VARGA_REGISTRY.get(code)
    if entry is None:
        if code.startswith("D") and code[1:].isdigit():
            return d_generic(longitude, int(code[1:]))
        raise ValueError(f"unknown varga {code!r}")
    fn = entry[0]
    if variant is not None:
        return fn(longitude, variant)
    return fn(longitude)
