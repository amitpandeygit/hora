"""Reference tables and notation — the data-publishing services.

These build the chapter tables the API publishes. They compute nothing
astrological; they format constants. Kept out of the routers so the HTTP layer
stays uniform and so `test_routers_stay_thin` has nothing to except.
"""
from __future__ import annotations

from hora.charts import benefic
from hora.core import const as c
from hora.core.const import (
    GRAHA_NAMES,
    NAKSHATRA_LORD,
    NAKSHATRA_SPAN,
    RASI_NAMES,
    TITHI_LORD,
)
from hora.core.names import NameScheme, both
from hora.core.notation import all_forms, parse
from hora.core.timeutil import format_dms


def resolve_notation(value: str) -> dict:
    """Parse decimal degrees, sign-degree-minute or rasi-relative notation.

    Everything goes through :func:`hora.core.notation.parse`, including plain
    decimals. It used to try ``float(value)`` first, which skipped every check
    ``parse`` makes: "400" came back as 10 Taurus rather than being refused,
    because the bare float was silently wrapped by the modulo below.

    :raises NotationError: on unparseable text, an unknown rasi name, or a
        longitude outside 0 to 360 degrees.
    """
    lon = parse(value)
    rasi = int(lon // 30.0)
    return {
        "input": value,
        **all_forms(lon),
        "rasi": rasi,
        "rasi_name": RASI_NAMES[rasi],
        "degrees_in_rasi": round(lon % 30.0, 8),
        "dms": format_dms(lon % 30.0),
    }


def nakshatra_table() -> dict:
    return {
        "span_degrees": NAKSHATRA_SPAN,
        "nakshatras": [
            {
                "index": i,
                "number": i + 1,
                **both("nakshatra", i),
                "starts": round(i * NAKSHATRA_SPAN, 8),
                "ends": round((i + 1) * NAKSHATRA_SPAN, 8),
                "vimsottari_lord": int(NAKSHATRA_LORD[i]),
                "vimsottari_lord_name": GRAHA_NAMES[NAKSHATRA_LORD[i]],
                "deity": c.NAKSHATRA_DEITY[i],
            }
            for i in range(27)
        ],
    }


def tithi_table() -> dict:
    return {
        "tithis": [
            {
                "number": i + 1,
                **both("tithi", i),
                "paksha": 0 if i < 15 else 1,
                "paksha_name": "Sukla" if i < 15 else "Krishna",
                "lord": int(TITHI_LORD[i]),
                "lord_name": GRAHA_NAMES[TITHI_LORD[i]],
                "alternate_names": c.TITHI_ALTERNATE_NAMES[(i % 15) + 1],
                "paksha_synonyms": c.PAKSHA_SYNONYMS[0 if i < 15 else 1],
            }
            for i in range(30)
        ],
    }


def rasi_table() -> dict:
    """All rasi classifications from book chapter 2.

    Calculation-side reference data only. The descriptive indications from
    section 2.3 are editorial and live under /v1/reference/rasis.
    """
    return {
        "rasis": [
            {
                "rasi": i,
                "name": c.RASI_NAMES[i],
                "sanskrit": c.RASI_NAMES_SA_BOOK[i],
                "symbol": c.RASI_ABBR[i],
                "starts": i * 30.0,
                "ends": (i + 1) * 30.0,
                "limb": c.RASI_LIMB[i],
                "is_odd": c.RASI_IS_ODD[i],
                "odd_even_names": c.ODD_EVEN_NAMES[0 if c.RASI_IS_ODD[i] else 1],
                "is_odd_footed": c.RASI_IS_ODD_FOOTED[i],
                "footed_names": c.FOOTED_NAMES[0 if c.RASI_IS_ODD_FOOTED[i] else 1],
                "ayana": c.AYANA_NAMES[c.RASI_AYANA[i]],
                "guna_adjectives": c.GUNA_ADJECTIVES[c.RASI_GUNA[i]],
                "modality": c.MODALITY_NAMES[c.RASI_MODALITY[i]],
                "modality_english": c.MODALITY_NAMES_EN[c.RASI_MODALITY[i]],
                "modality_deity": c.MODALITY_DEITY[c.RASI_MODALITY[i]],
                "modality_deity_role": c.MODALITY_DEITY_ROLE[c.RASI_MODALITY[i]],
                "modality_nature": c.MODALITY_NATURE[c.RASI_MODALITY[i]],
                "element": c.ELEMENT_NAMES[c.RASI_ELEMENT[i]],
                "element_sanskrit": c.ELEMENT_NAMES_SA[c.RASI_ELEMENT[i]],
                "element_definition": c.ELEMENT_DEFINITIONS[
                    c.ELEMENT_NAMES[c.RASI_ELEMENT[i]]
                ],
                "dosha": c.DOSHA_NAMES[c.RASI_DOSHA[i]],
                "dosha_english": c.DOSHA_NAMES_EN[c.RASI_DOSHA[i]],
                "guna": c.GUNA_NAMES[c.RASI_GUNA[i]],
                "guna_meaning": c.GUNA_MEANINGS[c.RASI_GUNA[i]],
                "direction": c.DIRECTION_NAMES[c.RASI_DIRECTION[i]],
                "color": c.RASI_COLOR[i],
                "strong_at": "night" if c.RASI_IS_NIGHT[i] else "day",
                "day_night_names": c.DAY_NIGHT_NAMES[0 if c.RASI_IS_NIGHT[i] else 1],
                "day_night_governor": int(
                    c.DAY_NIGHT_GOVERNOR[0 if c.RASI_IS_NIGHT[i] else 1]
                ),
                "rising": c.RISING_NAMES[c.RASI_RISING[i]],
                "rising_description": c.RISING_DESCRIPTIONS[c.RASI_RISING[i]],
                "rising_dasa_half": c.RISING_DASA_HALF[c.RASI_RISING[i]],
                "varna": c.VARNA_NAMES[c.RASI_VARNA[i]],
                "varna_english": c.VARNA_NAMES_EN[c.RASI_VARNA[i]],
                "varna_description": c.VARNA_DESCRIPTIONS[c.RASI_VARNA[i]],
                "lord": int(c.RASI_LORD[i]),
                "lord_name": GRAHA_NAMES[c.RASI_LORD[i]],
            }
            for i in range(12)
        ],
        "section_2_2_1": {
            "zodiac_as_vishnu": c.ZODIAC_AS_VISHNU,
            "applies_to_native": c.LIMB_APPLIES_TO_NATIVE,
        },
        "section_2_2_2": {
            "names": c.ODD_EVEN_NAMES,
            "used_for": c.ODD_EVEN_USE,
        },
        "section_2_2_3": {
            "names": c.FOOTED_NAMES,
            "used_for": c.FOOTED_USE,
            "note": (
                "A different partition from 2.2.2's odd/even — Taurus is an "
                "even rasi but an odd-footed one."
            ),
        },
        "section_2_2_4": {
            "modalities": [
                {
                    "modality": c.MODALITY_NAMES[m],
                    "english": c.MODALITY_NAMES_EN[m],
                    "deity": c.MODALITY_DEITY[m],
                    "role": c.MODALITY_DEITY_ROLE[m],
                    "nature": c.MODALITY_NATURE[m],
                }
                for m in range(3)
            ],
            "trinity_note": c.TRINITY_NOTE,
        },
        "section_2_2_5": {
            "five_elements": c.FIVE_ELEMENTS_BOOK_ORDER,
            "definitions": c.ELEMENT_DEFINITIONS,
            "ether_name": c.ETHER_NAME,
            "ether_name_sanskrit": c.ETHER_NAME_SA,
            "ether_in_every_rasi": c.ETHER_IN_EVERY_RASI,
            "elements_underlie_everything": c.ELEMENTS_UNDERLIE_EVERYTHING,
        },
        "section_2_2_6": {
            "ayurveda_note": c.AYURVEDA_NOTE,
            "humours": [
                {
                    "dosha": c.DOSHA_NAMES[d],
                    "english": c.DOSHA_NAMES_EN[d],
                    "elements": c.DOSHA_ELEMENTS[d],
                    "shows": c.DOSHA_SHOWS[d],
                    "body_example": c.DOSHA_BODY_EXAMPLE[d],
                }
                for d in range(4)
            ],
            "note": (
                "The stated compositions do not give the sign assignment — "
                "see D-1 in docs/book-deviations.md. The pitta sentence prints "
                f"{c.DOSHA_SHOWS_TYPO!r}, which is the book's own typo."
            ),
        },
        "section_2_2_7": {
            "triguna_note": c.TRIGUNA_NOTE,
            "gunas": [
                {
                    "guna": c.GUNA_NAMES[g],
                    "alternate_name": c.GUNA_NAMES_ALT[g],
                    "meaning": c.GUNA_MEANINGS[g],
                    "effect": c.GUNA_EFFECTS[g],
                    "adjectives": c.GUNA_ADJECTIVES[g],
                }
                for g in range(3)
            ],
        },
        "section_2_2_10": {
            "names": c.DAY_NIGHT_NAMES,
            "pair_rule": c.DAY_NIGHT_PAIR_RULE,
            "governors": [
                {
                    "half": c.DAY_NIGHT_NAMES[h][0],
                    "graha": int(c.DAY_NIGHT_GOVERNOR[h]),
                    "graha_name": GRAHA_NAMES[c.DAY_NIGHT_GOVERNOR[h]],
                }
                for h in range(2)
            ],
        },
        "section_2_2_11": {
            "descriptions": c.RISING_DESCRIPTIONS,
            "dasa_rule": c.RISING_DASA_RULE,
            "prishthodaya_note": c.PRISHTHODAYA_NOTE,
        },
        "section_2_2_12": {
            "varnas": [
                {
                    "varna": c.VARNA_NAMES[v],
                    "english": c.VARNA_NAMES_EN[v],
                    "description": c.VARNA_DESCRIPTIONS[v],
                    "element": c.VARNA_ELEMENT[v],
                }
                for v in range(4)
            ],
        },
        "deviations": [
            (
                "dosha assignment follows the book, not conventional Ayurveda "
                "— see docs/book-deviations.md D-1"
            )
        ],
    }


def name_schemes() -> dict:
    return {
        "default": NameScheme.BOOK.value,
        "schemes": [s.value for s in NameScheme],
        "note": (
            "book = spellings as printed in 'Vedic Astrology: An Integrated Approach'. "
            "standard = common pan-Indian Sanskrit forms. Names are display only; "
            "integer indices are the stable contract."
        ),
    }


def graha_table() -> dict:
    """All graha classifications and dignities from book chapter 3.

    ``None`` means the book gives no value — Mars has no abode, and the nodes
    have no deep-exaltation degree. Nothing is filled in from elsewhere.
    """
    def opt(table, g, names=None):
        v = table.get(g)
        if v is None:
            return None
        return names[v] if names else v

    return {
        "grahas": [
            {
                "id": int(g),
                "name": GRAHA_NAMES[g],
                "sanskrit": c.GRAHA_NAMES_SA[g],
                "abbreviation": c.GRAHA_ABBR[g],
                "is_chaayaa_graha": g in c.CHAAYAA_GRAHAS,
                "aliases": c.NODE_ALIASES.get(g, []),
                "avatara": c.GRAHA_AVATARA.get(g),
                "avatara_aliases": c.AVATARA_ALIASES.get(
                    c.GRAHA_AVATARA.get(g) or "", []),
                "avatara_description": c.AVATARA_DESCRIPTIONS.get(
                    c.GRAHA_AVATARA.get(g) or ""),
                "governs": c.GRAHA_GOVERNS.get(g),
                "color": c.GRAHA_COLOR.get(g),
                "cabinet_role": c.GRAHA_CABINET.get(g),
                "deity": c.GRAHA_DEITY.get(g),
                "deity_role": c.GRAHA_DEITY_ROLE.get(g),
                "sex": opt(c.GRAHA_SEX, g, c.SEX_NAMES),
                "natural_nature": (
                    "benefic" if g in c.NATURAL_BENEFIC
                    else "malefic" if g in c.NATURAL_MALEFIC
                    else "conditional"
                ),
                "element": opt(c.GRAHA_ELEMENT, g, c.PLANET_ELEMENT_NAMES),
                "element_adjective": opt(c.GRAHA_ELEMENT, g,
                                         c.PLANET_ELEMENT_ADJECTIVES),
                "element_tattva": opt(c.GRAHA_ELEMENT, g, c.PLANET_ELEMENT_TATTVAS),
                "rules_element": int(g) in {int(x) for x in c.ELEMENT_RULER.values()},
                "shares_element_without_ruling": g in c.SHARES_ELEMENT_WITHOUT_RULING,
                "element_governance": c.ELEMENT_GOVERNANCE.get(g),
                "varna": opt(c.GRAHA_VARNA, g, c.VARNA_NAMES),
                "varna_english": opt(c.GRAHA_VARNA, g, c.VARNA_NAMES_EN_3_2_9),
                "varna_forte": opt(c.GRAHA_VARNA, g, c.VARNA_FORTE),
                "guna": opt(c.GRAHA_GUNA, g, c.GUNA_NAMES),
                "guna_definition": opt(c.GRAHA_GUNA, g, c.GUNA_DEFINITIONS),
                "abode": c.GRAHA_ABODE.get(g),
                "dhatu": c.GRAHA_DHATU.get(g),
                "dhatu_description": c.DHATU_DESCRIPTIONS.get(g),
                "time_period": c.GRAHA_TIME_PERIOD.get(g),
                "taste": c.GRAHA_TASTE.get(g),
                "taste_examples": c.TASTE_EXAMPLES.get(g, []),
                "dhatu_moola_jeeva": opt(c.GRAHA_DHATU_MOOLA_JEEVA, g,
                                         c.DHATU_MOOLA_JEEVA_NAMES),
                "dhatu_moola_jeeva_meaning": opt(
                    c.GRAHA_DHATU_MOOLA_JEEVA, g, c.DHATU_MOOLA_JEEVA_MEANINGS),
                "dig_bala_house": c.DIG_BALA_STRONG_HOUSE.get(g),
                "ritu": next(
                    (c.RITU_NAMES[i] for i, r in c.RITU_RULER.items() if r == g),
                    None,
                ),
                "strong_in_ayana": (
                    c.AYANA_NAMES[c.BENEFIC_STRONG_AYANA] if g in c.NATURAL_BENEFIC
                    else c.AYANA_NAMES[c.MALEFIC_STRONG_AYANA]
                    if g in c.NATURAL_MALEFIC else None
                ),
                "strong_at": ("night" if g in c.STRONG_AT_NIGHT else
                              "day" if g in c.STRONG_BY_DAY else
                              "always" if g in c.STRONG_ALWAYS else None),
                "natural_benefic": g in c.NATURAL_BENEFIC,
                "natural_malefic": g in c.NATURAL_MALEFIC,
                "digbala_house": c.DIG_BALA_STRONG_HOUSE.get(g),
                "owns": [c.RASI_NAMES[r] for r in c.GRAHA_OWNS.get(g, ())],
                "co_lord_only": g in c.CO_LORDS_ONLY,
                "exaltation_rasi": (c.RASI_NAMES[c.EXALTATION_RASI[g]]
                                    if g in c.EXALTATION_RASI else None),
                "deep_exaltation_degree": (round(c.EXALTATION_DEG[g] % 30.0, 6)
                                           if g in c.EXALTATION_DEG else None),
                "debilitation_rasi": (c.RASI_NAMES[c.DEBILITATION_RASI[g]]
                                      if g in c.DEBILITATION_RASI else None),
                "moolatrikona": (
                    {"rasi": c.RASI_NAMES[c.MOOLATRIKONA[g][0]],
                     "from_degree": c.MOOLATRIKONA[g][1],
                     "to_degree": c.MOOLATRIKONA[g][2]}
                    if g in c.MOOLATRIKONA else None
                ),
                "natural_relations": {
                    GRAHA_NAMES[o]: ["enemy", "neutral", "friend"][v]
                    for o, v in c.NATURAL_RELATION.get(g, {}).items() if o != g
                },
            }
            for g in c.NAVAGRAHA
        ],
        "ritus": [
            {"index": i, "name": c.RITU_NAMES[i], "meaning": c.RITU_MEANINGS[i],
             "ruler": GRAHA_NAMES[c.RITU_RULER[i]]}
            for i in range(6)
        ],
        "section_3_2_14": {
            "use": c.TASTE_USE,
            "mercury_has_no_examples": (
                "Mercury governs a mixed taste and the book gives it no "
                "examples, so none are invented."
            ),
        },
        "section_3_2_15": {
            "name": c.DIG_BALA_NAME,
            "note": c.DIG_BALA_NOTE,
            "always_strong_note": c.ALWAYS_STRONG_NOTE,
            "strong_at_night": sorted(int(x) for x in c.STRONG_AT_NIGHT),
            "strong_by_day": sorted(int(x) for x in c.STRONG_BY_DAY),
            "always_strong": sorted(int(x) for x in c.STRONG_ALWAYS),
            "benefic_strong_paksha": c.PAKSHA_NAMES[c.BENEFIC_STRONG_PAKSHA],
            "malefic_strong_paksha": c.PAKSHA_NAMES[c.MALEFIC_STRONG_PAKSHA],
            "benefic_strong_ayana": c.AYANA_NAMES[c.BENEFIC_STRONG_AYANA],
            "malefic_strong_ayana": c.AYANA_NAMES[c.MALEFIC_STRONG_AYANA],
        },
        "section_3_2_16": {
            "note": c.RITU_RULERSHIP_NOTE,
            "ritus": [
                {
                    "ritu": c.RITU_NAMES[i],
                    "meaning": c.RITU_MEANINGS[i],
                    "lord": int(c.RITU_RULER[i]),
                    "lord_name": GRAHA_NAMES[c.RITU_RULER[i]],
                }
                for i in range(6)
            ],
        },
        "section_3_2_17": {
            "classes": [
                {"name": c.DHATU_MOOLA_JEEVA_NAMES[i],
                 "meaning": c.DHATU_MOOLA_JEEVA_MEANINGS[i],
                 "grahas": sorted(
                     int(g) for g, v in c.GRAHA_DHATU_MOOLA_JEEVA.items() if v == i
                 )}
                for i in range(3)
            ],
        },
        "section_3_3": {
            "strong_note": c.DIGNITY_STRONG_NOTE,
            "strong_placements": list(c.DIGNITY_STRONG_PLACEMENTS),
            "sanskrit_names": dict(c.DIGNITY_NAMES_SA),
            "analogy": dict(c.DIGNITY_ANALOGY),
            "subtle_difference": c.DIGNITY_SUBTLE_DIFFERENCE,
        },
        "section_3_2_8": {
            "note": c.ELEMENT_GOVERNANCE_NOTE,
            "shares_without_ruling_phrase": c.SHARES_ELEMENT_PHRASE,
            "shares_without_ruling": sorted(
                int(x) for x in c.SHARES_ELEMENT_WITHOUT_RULING
            ),
        },
        "section_3_2_9": {
            "english_names": list(c.VARNA_NAMES_EN_3_2_9),
            "fortes": list(c.VARNA_FORTE),
            "nature_not_caste": c.VARNA_MEANS_NATURE_NOT_CASTE,
            "cabinet_note": c.VARNA_CABINET_NOTE,
            "gloss_differs_from_2_2_12": (
                "Section 2.2.12 glosses the four as scholars, warriors, "
                "traders, workers; 3.2.9 as learned, warriors, traders, "
                "worker. Both are the book's own and neither is normalised."
            ),
        },
        "section_3_2_10": {
            "definitions": list(c.GUNA_DEFINITIONS),
            "sattwa_meaning": c.SATTWA_MEANING,
            "misconception_note": c.SATTWA_MISCONCEPTION_NOTE,
        },
        "section_3_2_11": {"note": c.ABODE_NOTE},
        "section_3_2_12": {
            "name": c.SAPTA_DHATU_NAME,
            "note": c.SAPTA_DHATU_NOTE,
            "affliction_note": c.DHATU_AFFLICTION_NOTE,
        },
        "section_3_2_13": {"use": c.TIME_PERIOD_USE},
        "section_3_2_2": {
            "benefic_class_names": list(c.BENEFIC_CLASS_NAMES),
            "malefic_class_names": list(c.MALEFIC_CLASS_NAMES),
            "fixed_benefics": sorted(int(x) for x in c.NATURAL_BENEFIC),
            "fixed_malefics": sorted(int(x) for x in c.NATURAL_MALEFIC),
            "conditional": sorted(int(x) for x in benefic.CONDITIONAL),
            "mercury_rule": (
                "Mercury becomes a natural benefic when he is alone or with "
                "more natural benefics. Mercury becomes a natural malefic "
                "when he is joined by more natural malefics."
            ),
            "moon_rule": (
                "Waxing Moon of Sukla paksha is a natural benefic. Waning "
                "Moon of Krishna paksha is a natural malefic."
            ),
            "inherent_nature_note": benefic.INHERENT_NATURE_NOTE,
        },
        "section_3_2_4": {"color_use": c.GRAHA_COLOR_USE},
        "section_3_2_7": {"sex_prediction_note": c.SEX_PREDICTION_NOTE},
        "deviations": [
            (
                "Rahu exalts in Gemini and Ketu in Sagittarius per Table 6, not "
                "the commonly cited Taurus and Scorpio — see docs/book-deviations.md D-4"
            ),
            (
                "Mercury's moolatrikona starts at 15 degrees Virgo per section 3.3 "
                "rule 4, not the usual 16 — D-5"
            ),
            "Mercury and Saturn are recorded as neuter; the book prints female — D-6",
            (
                "The nodes co-own Aquarius and Scorpio for dignity only; rasi "
                "lordship is unchanged — D-4"
            ),
        ],
    }


def varga_catalog() -> dict:
    """The divisional charts this service knows by name."""
    from hora.charts.vargas import SHODASAVARGA, VARGA_REGISTRY

    return {
        "named": [
            {"code": code, "name": entry[1], "divisions": entry[2]}
            for code, entry in VARGA_REGISTRY.items()
        ],
        "generic": "Any D<N> for N in 1..300 falls back to the cyclic (parivritti) rule.",
        "groups": {"shodasavarga": list(SHODASAVARGA)},
    }


def dasha_catalog() -> dict:
    """The dasa systems currently implemented."""
    from hora.dasha.nakshatra.systems import NAKSHATRA_DASHA_SYSTEMS

    return {
        "nakshatra_dashas": [
            {"key": s.key, "name": s.display_name, "total_years": s.total_years}
            for s in NAKSHATRA_DASHA_SYSTEMS.values()
        ],
    }


def yoga_table() -> dict:
    """Table 5 — the twenty-seven Sun-Moon yogas and what their names mean."""
    return {
        "span_degrees": NAKSHATRA_SPAN,
        "yogas": [
            {
                "number": i + 1,
                "index": i,
                **both("yoga", i),
                "means": c.YOGA_MEANINGS[i],
                "starts": round(i * NAKSHATRA_SPAN, 8),
                "ends": round((i + 1) * NAKSHATRA_SPAN, 8),
            }
            for i in range(27)
        ],
    }


def relationship_terms() -> dict:
    """Section 3.4's own vocabulary for planetary relationships.

    The engine's labels are English (``great_friend`` and the rest); these are
    the book's terms, so a client can render either without guessing.
    """
    return {
        "kinds": c.RELATIONSHIP_KINDS,
        "natural": [
            {"value": v, "label": ["enemy", "neutral", "friend"][v],
             "sanskrit": c.NATURAL_RELATION_NAMES[v]}
            for v in (2, 1, 0)
        ],
        "compound": [
            {"label": k, "sanskrit": v, "gloss": c.COMPOUND_RELATION_GLOSSES[k]}
            for k, v in c.COMPOUND_RELATION_NAMES.items()
        ],
        "dignities": c.DIGNITY_NAMES_SA,
    }


def terms() -> dict:
    """Vocabulary the book defines but that belongs to no single table row.

    The zodiac's two names, what "panchaanga" means, the essences, the
    paksha descriptions, the purushartha gloss and the upagraha spelling
    variants. Each is a phrase the book states once and uses throughout.
    """
    return {
        "graha": {
            "definition": c.GRAHA_DEFINITION,
            "note": c.GRAHA_DEFINITION_NOTE,
            "count": len(c.NAVAGRAHA),
            "classical_count": len(c.CLASSICAL_SEVEN),
        },
        "nodes": {
            "are_mathematical_points": c.NODES_ARE_MATHEMATICAL_POINTS,
        },
        "upagraha": {
            "definition": c.UPAGRAHA_DEFINITION,
            "gloss": c.UPAGRAHA_GLOSS,
            "count": c.UPAGRAHA_COUNT,
        },
        "lagna": {
            "definition": c.LAGNA_DEFINITION,
            "special_ascendants_term": c.SPECIAL_ASCENDANT_TERM,
        },
        "solar_calendar": {
            "year_degrees": c.SOLAR_YEAR_DEGREES,
            "month_degrees": c.SOLAR_MONTH_DEGREES,
            "day_degrees": c.SOLAR_DAY_DEGREES,
            "days_per_month": c.DAYS_PER_SOLAR_MONTH,
            "definition": (
                "One year is the time in which Sun moves by 360 degrees and "
                "one month is the time in which Sun moves by 30 degrees. Each "
                "solar month has 30 days, where one day stands for exactly 1 "
                "degree motion of Sun."
            ),
            "used_in": list(c.SOLAR_CALENDAR_USED_IN),
            "note": (
                "Defined by the Sun's motion, not by elapsed days, so a solar "
                "month is not a fixed number of days"
            ),
        },
        "nakshatra": {
            "count": c.NAKSHATRA_COUNT,
            "span_degrees": c.NAKSHATRA_SPAN,
            "padas_each": c.PADAS_PER_NAKSHATRA,
            "pada_span_degrees": c.PADA_SPAN,
            "pada_gloss": c.PADA_GLOSS,
            "count_for_special_charts": c.NAKSHATRA_COUNT_SPECIAL,
            "special_charts": list(c.TWENTY_EIGHT_NAKSHATRA_CHARTS),
            "abhijit_rule": c.ABHIJIT_RULE,
        },
        "varga": {
            "sanskrit": c.VARGA_CHAKRA_NAME,
            "aliases": list(c.VARGA_ALIASES),
            "definition": c.VARGA_DEFINITION,
            "signifies": c.VARGA_SIGNIFIES_AN_AREA,
            "independent_chart_rule": c.VARGA_INDEPENDENT_CHART_RULE,
        },
        "four_pillars": {
            "statement": (
                "The science of Vedic astrology stands on the basis of 4 "
                "pillars"
            ),
            "pillars": [dict(p) for p in c.FOUR_PILLARS],
            "conclusion_order": list(c.FOUR_PILLARS_CONCLUSION_ORDER),
            "ordering_note": (
                "Section 6.7 lists the same four in a different order and "
                "calls divisional charts the third pillar. The numbering here "
                "follows section 1.3.5, which defines them. See "
                "docs/book-deviations.md D-23."
            ),
        },
        "zodiac": {
            "used": c.ZODIAC_USED,
            "names": [
                {"name": name, "means": means}
                for name, means in c.ZODIAC_NAMES.items()
            ],
        },
        "panchanga": {
            "book_spelling": c.PANCHANGA_NAME_BOOK,
            "means": c.PANCHANGA_MEANING,
            "almanacs_called": c.PANCHANGA_ALMANAC_NAME,
        },
        "chaayaa_grahas": {
            "term": c.CHAAYAA_GRAHA_NAME,
            "grahas": [
                {"id": int(g), "name": GRAHA_NAMES[g],
                 "aliases": c.NODE_ALIASES.get(int(g), [])}
                for g in sorted(c.CHAAYAA_GRAHAS)
            ],
        },
        "essences": [
            {"key": key, "name": name,
             "aliases": c.ESSENCE_ALIASES.get(key, [])}
            for key, name in c.ESSENCE_NAMES.items()
        ],
        "paksha": [
            {"index": i, "name": c.PAKSHA_NAMES[i],
             "synonyms": c.PAKSHA_SYNONYMS[i],
             "describes": c.PAKSHA_DESCRIPTIONS[i]}
            for i in range(len(c.PAKSHA_NAMES))
        ],
        "purushartha": {
            "book_spelling": c.PURUSHARTHA_NAME_BOOK,
            "means": c.PURUSHARTHA_MEANING,
        },
        "upagraha_aliases": [
            {"name": name, "aliases": aliases}
            for name, aliases in c.UPAGRAHA_ALIASES.items()
        ],
    }


def house_definition() -> dict:
    """§1.3.3 — what a house is and what it is counted from.

    Lives here rather than in `house_service` because it is vocabulary, not
    calculation: this module is one of the register's declared exposers, so
    naming a constant here publishes it without marking it consumed.
    """
    return {
        "sanskrit": c.BHAVA_NAME,
        "text": c.HOUSE_DEFINITION,
        "order_wraps": c.HOUSE_ORDER_WRAPS,
        "common_references": list(c.HOUSE_COMMON_REFERENCES),
        "default_reference": c.HOUSE_DEFAULT_REFERENCE,
        "default_reference_rule": c.HOUSE_DEFAULT_REFERENCE_RULE,
    }
