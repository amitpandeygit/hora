"""§30.2 — Patyayini dasa.

The first of chapter 30's three annual dasas, and the only one that is not a
compressed natal system: it is built from the annual chart's own longitudes.
"""

from __future__ import annotations

from hora.core import validate
from hora.core.const import GRAHA_NAMES, RASI_NAMES, Graha

#: §30.2's opening, verbatim.
PATYAYINI_SCOPE = (
    "This dasa is based on the longitudes of lagna and all planets and it is "
    "specifically meant for Tajaka charts."
)

#: The four steps, verbatim.
PATYAYINI_PROCEDURE: tuple[dict[str, object], ...] = (
    {"step": 1, "text": (
        "Consider lagna and the seven planets. Find their advancement from "
        "the beginning of the respective signs occupied by them. Arrange them "
        "in the ascending order. These are called \"Krisamsas\" of planets.")},
    {"step": 2, "text": (
        "Leave the krisamsa of the first planet (the one with the lowest "
        "value). From krisamsas of all other planets, subtract the krisamsas "
        "of the previous planets. In other words, subtract the krisamsa that "
        "is just below the current planet's krisamsa. These values are called "
        "\"Patyamsas\".")},
    {"step": 3, "text": (
        "Dasas of lagna and the seven planet are in the order found in (1). "
        "Their dasas are in the ratio of their patyamsas. Dasa of a planet "
        "(in days) is given by the formula: 365.2425 x (its patyamsa / sum of "
        "all patyamsas)")},
    {"step": 4, "text": (
        "To find antardasas, we use the same ratios and order used in dasas, "
        "just as in Vimsottari dasa. First antardasa is the same as dasa. "
        "Then we go in the order.")},
)

#: Footnote 87, verbatim.
FOOTNOTE_87 = (
    "It may be noted that the sum of all patyamsas is nothing but the largest "
    "krisamsa.")

#: The divisor §30.2 names. It is the **Gregorian mean calendar year**, not
#: the sidereal year — see `THE_DIVISOR_IS_THE_CALENDAR_YEAR_NOT_THE_REAL_ONE`.
PATYAYINI_YEAR_DAYS = 365.2425

#: The eight bodies the dasa uses. The nodes are not among them: §30.2 says
#: "lagna and the seven planets" and Table 75 lists eight rows.
PATYAYINI_BODIES: tuple[int, ...] = (
    int(Graha.SUN), int(Graha.MOON), int(Graha.MARS), int(Graha.MERCURY),
    int(Graha.JUPITER), int(Graha.VENUS), int(Graha.SATURN))


class PatyayiniError(validate.InputError):
    """A patyayini input that cannot be resolved."""


#: **Finding.** Footnote 87 states an identity rather than an observation: the
#: patyamsas are successive differences of a sorted list whose first term is
#: kept whole, so they **telescope** and their sum is the largest krisamsa
#: exactly, in every chart. Table 75's own column adds to 23°53', which is
#: Mars's krisamsa. `patyayini_dasa` computes the sum and asserts nothing —
#: the identity is checked, not assumed.
THE_SUM_TELESCOPES_TO_THE_LARGEST_KRISAMSA = (
    "The patyamsas are successive differences of the sorted krisamsas with "
    "the first kept whole, so they sum to the largest krisamsa in every "
    "chart. Footnote 87 states an identity, not a coincidence."
)

#: **Finding.** 365.2425 days is the **Gregorian mean calendar year**. The year
#: a Tajaka chart actually covers is the interval between two varsha praveshes,
#: which is a **sidereal** year — 365.2564 days, and §27.2's own Table 71 uses
#: that figure. So a full set of patyayini dasas runs out about **20 minutes
#: before** the next annual chart begins. The section does not mention the gap.
THE_DIVISOR_IS_THE_CALENDAR_YEAR_NOT_THE_REAL_ONE = (
    "Section 30.2 divides by 365.2425, the Gregorian calendar year. The "
    "interval between two varsha praveshes is a sidereal year of about "
    "365.2564 days, so the dasas end roughly twenty minutes early."
)

#: **Gap.** Two bodies at the same degree of their respective signs give a
#: patyamsa of **zero** and a dasa of zero days. The book does not reach the
#: case, and it is not far-fetched: Table 75's own Moon and Mercury are two
#: arcminutes apart, which is a dasa of half a day. `patyayini_dasa` returns
#: the zero rather than dropping the body.
A_TIE_GIVES_A_DASA_OF_ZERO_DAYS = (
    "Two bodies at the same advancement give a patyamsa of zero and a dasa "
    "of no length. Table 75's Moon and Mercury are two arcminutes apart, "
    "which is already only half a day."
)

#: **Finding.** The first body's patyamsa is its whole krisamsa, which step
#: (2) says by omission — "leave the krisamsa of the first planet" — and
#: Table 75 confirms: Venus's krisamsa and patyamsa are both 1°38'. So the
#: first dasa is proportional to how far the lowest body stands from the start
#: of its sign, and a body at 0°00' would give the first dasa no length at all.
THE_FIRST_PATYAMSA_IS_THE_WHOLE_KRISAMSA = (
    "Step 2 leaves the lowest krisamsa alone, so the first body's patyamsa is "
    "its own krisamsa. Table 75 shows Venus with 1 degree 38 minutes in both "
    "columns."
)


def krisamsa(longitude: float) -> float:
    """Step (1): a body's advancement from the start of the sign it occupies.
    """
    return validate.longitude("longitude", float(longitude)) % 30.0


def patyayini_dasa(*, lagna: float, longitudes: dict[int, float],
                   start_jd: float | None = None) -> dict:
    """§30.2's whole procedure, steps (1) to (3).

    :param longitudes: the seven classical grahas by id. The nodes take no
        part; §30.2 says "lagna and the seven planets".
    """
    missing = [g for g in PATYAYINI_BODIES if g not in longitudes]
    if missing:
        raise PatyayiniError(
            "patyayini needs all seven grahas; missing "
            + ", ".join(str(GRAHA_NAMES[g]) for g in missing))

    seat = validate.longitude("lagna", float(lagna))
    places: list[tuple[str, int | None, float]] = [("Lagna", None, seat)]
    for graha in PATYAYINI_BODIES:
        places.append((str(GRAHA_NAMES[graha]), graha, validate.longitude(
            str(GRAHA_NAMES[graha]), float(longitudes[graha]))))

    order: list[dict] = sorted(
        ({"body": name, "graha": graha, "longitude": place,
          "krisamsa": krisamsa(place),
          "rasi": str(RASI_NAMES[int(place // 30)])}
         for name, graha, place in places),
        key=lambda row: float(row["krisamsa"]))

    previous = 0.0
    for row in order:
        row["patyamsa"] = float(row["krisamsa"]) - previous
        previous = float(row["krisamsa"])

    total = sum(float(row["patyamsa"]) for row in order)
    largest = float(order[-1]["krisamsa"])
    for row in order:
        row["fraction"] = float(row["patyamsa"]) / total if total else 0.0
        row["days"] = PATYAYINI_YEAR_DAYS * float(row["fraction"])

    running = 0.0
    for row in order:
        row["from_day"] = running
        running += float(row["days"])
        row["to_day"] = running
        if start_jd is not None:
            row["from_jd"] = float(start_jd) + float(row["from_day"])
            row["to_jd"] = float(start_jd) + float(row["to_day"])

    return {
        "order": tuple(str(row["body"]) for row in order),
        "rows": tuple(order),
        "sum_of_patyamsas": total,
        "largest_krisamsa": largest,
        "footnote_87_holds": abs(total - largest) < 1e-9,
        "total_days": running,
        "year_days": PATYAYINI_YEAR_DAYS,
        "ties": tuple(str(row["body"]) for row in order[1:]
                      if float(row["patyamsa"]) == 0.0),
        "procedure": PATYAYINI_PROCEDURE,
    }


def antardasas(dasa: dict, body: str) -> tuple[dict, ...]:
    """Step (4): the antardasas of one dasa, in the dasa order from its lord.

    "First antardasa is the same as dasa. Then we go in the order." The
    fractions are the dasa fractions, so the antardasas of a dasa sum to its
    length exactly.
    """
    order = list(dasa["order"])
    if body not in order:
        raise PatyayiniError(f"{body!r} has no dasa in this chart")
    start = order.index(body)
    rotated = order[start:] + order[:start]
    by_body = {str(row["body"]): row for row in dasa["rows"]}
    length = float(by_body[body]["days"])

    out = []
    running = float(by_body[body]["from_day"])
    for name in rotated:
        span = length * float(by_body[name]["fraction"])
        out.append({
            "dasa": body, "antardasa": name,
            "fraction": float(by_body[name]["fraction"]),
            "days": span, "from_day": running, "to_day": running + span,
        })
        running += span
    return tuple(out)


# --------------------------------------------------------------------------
# Table 75 and Example 122's timing
# --------------------------------------------------------------------------

TABLE_75_TITLE = "Patyayini Dasa Calculation"

#: Table 75 exactly as printed, in its own order. The krisamsas are the eight
#: bodies of Chart 67 **rounded** to the arcminute where the diagram truncated
#: them — see `TABLE_75_ROUNDS_WHERE_CHART_67_TRUNCATES`.
TABLE_75: tuple[dict[str, object], ...] = (
    {"body": "Venus", "krisamsa": "1 38", "patyamsa": "1 38",
     "fraction": 0.0684, "days": 24.98},
    {"body": "Mercury", "krisamsa": "4 47", "patyamsa": "3 9",
     "fraction": 0.1319, "days": 48.17},
    {"body": "Moon", "krisamsa": "4 49", "patyamsa": "0 2",
     "fraction": 0.0014, "days": 0.51},
    {"body": "Saturn", "krisamsa": "6 30", "patyamsa": "1 41",
     "fraction": 0.0705, "days": 25.74},
    {"body": "Lagna", "krisamsa": "7 14", "patyamsa": "0 44",
     "fraction": 0.0307, "days": 11.21},
    {"body": "Jupiter", "krisamsa": "10 59", "patyamsa": "3 45",
     "fraction": 0.1570, "days": 57.35},
    {"body": "Sun", "krisamsa": "17 5", "patyamsa": "6 6",
     "fraction": 0.2554, "days": 93.29},
    {"body": "Mars", "krisamsa": "23 53", "patyamsa": "6 48",
     "fraction": 0.2847, "days": 103.99},
)

#: The denominator Table 75 prints in every row: the largest krisamsa.
TABLE_75_DENOMINATOR = "23 53"

#: The two dasa spans §30.2 states, and the marriage they bracket.
PATYAYINI_SPANS: tuple[dict[str, str], ...] = (
    {"body": "Venus", "days": "25", "from": "June 1, 1993",
     "to": "June 26, 1993"},
    {"body": "Mercury", "days": "48", "from": "June 26, 1993",
     "to": "Aug 13, 1993"},
)

#: The four antardasas §30.2 works inside Venus dasa, verbatim in substance.
VENUS_ANTARDASAS: tuple[dict[str, object], ...] = (
    {"antardasa": "Venus", "fraction": 0.0684, "days": 1.7},
    {"antardasa": "Mercury", "fraction": 0.1319, "days": 3.3},
    {"antardasa": "Moon", "fraction": 0.0014, "days": 0.03},
    {"antardasa": "Saturn", "fraction": 0.0705, "days": 1.8},
)

#: **Finding, and it settles D-80 from inside one example.** Table 75's eight
#: krisamsas are Chart 67's eight longitudes to the arcminute, and the two
#: printings disagree on **five** of the eight: Venus 1°37' against 1°38',
#: the Moon 4°48' against 4°49', Saturn 6°29' against 6°30', the lagna 7°13'
#: against 7°14', the Sun 17°04' against 17°05'. Our value sits between every
#: pair — it **truncates** to the diagram and **rounds** to the table, eight
#: times out of eight. D-80 inferred that convention from Chart 66 and
#: Example 121; here the book prints the same eight numbers both ways four
#: pages apart.
TABLE_75_ROUNDS_WHERE_CHART_67_TRUNCATES = (
    "Table 75 gives the same eight bodies as Chart 67's diagram and differs "
    "on five of them by an arcminute. Our value truncates to the diagram and "
    "rounds to the table in all eight cases."
)

#: **Finding.** Table 75 reproduces **cell for cell** from its own printed
#: krisamsas: every fraction to the fourth decimal and every day count to
#: within 0.005 days, which is the printing to two decimals. So the section's
#: arithmetic is exactly this module's, and the differences from our own
#: ephemeris values come only from the book rounding krisamsas to whole
#: arcminutes.
TABLE_75_REPRODUCES_FROM_ITS_OWN_KRISAMSAS = (
    "Fed Table 75's own krisamsas, every fraction and every day count comes "
    "back to the precision printed. The arithmetic is confirmed separately "
    "from the ephemeris."
)

#: **Finding.** The Moon's dasa is where the book's rounding bites hardest.
#: Her patyamsa is 1.6 arcminutes and Table 75 prints 2', so the printed 0.51
#: days is a quarter longer than the 0.40 our own longitudes give. Every other
#: dasa agrees within 0.2 days. The smallest patyamsa is the one the rounding
#: cannot afford.
THE_SHORTEST_DASA_IS_THE_LEAST_ROBUST = (
    "The Moon's patyamsa is 1.6 arcminutes, printed as 2, so her dasa comes "
    "out 0.51 days in the book against 0.40 from unrounded longitudes. No "
    "other dasa moves by more than a fifth of a day."
)

#: **Finding.** The antardasas of a dasa use the **dasa** fractions, so they
#: sum to the dasa's own length exactly and the whole year is partitioned
#: twice over. §30.2's four worked antardasas in Venus dasa reproduce: 1.71,
#: 3.29, 0.03 and 1.76 days against the printed 1.7, 3.3, 0.03 and 1.8.
THE_ANTARDASAS_PARTITION_THE_DASA_EXACTLY = (
    "Antardasa fractions are the dasa fractions, so the antardasas of any "
    "dasa sum to its length. The four the section works reproduce to the "
    "precision it prints them."
)
