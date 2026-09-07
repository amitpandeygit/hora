"""§28.5 — dwaadasa vargeeya bala, the strength from twelve divisional charts.

A count rather than a score. Look at the same planet in D-1 through D-12, mark
each chart strong, weak or neither, and take the difference.

The section's own three-way classification is what makes this work where §28.4
does not. There a neutral's rasi had no price and left the total undecided
(OI-153); here a neutral's rasi is simply neither strong nor weak and
contributes nothing, which the arithmetic of a difference handles without a
fourth grade. The one case §28.5 does not cover is a **tie** — see OI-155.
"""
from __future__ import annotations

from hora.charts.relationship import natural
from hora.charts.vargas import varga
from hora.core import validate
from hora.core.const import (
    DEBILITATION_RASI,
    EXALTATION_RASI,
    GRAHA_NAMES,
    RASI_LORD,
    RASI_NAMES,
)

DWADASA_VARGEEYA_CHARTS = (
    "Consider the twelve divisional charts: D-1, D-2, D-3, D-4, D-5, D-6, "
    "D-7, D-8, D-9, D-10, D-11, and, D-12.")

DWADASA_VARGEEYA_RULE = (
    "A planet is strong in a chart if it is in its exaltation rasi or its own "
    "rasi or a rasi owned by a friend. A planet is weak in a chart if it is "
    "in its debilitation rasi or a rasi owned by an enemy. Out of the 12 "
    "charts above, count the charts in which a planet is strong and count the "
    "charts in which a planet is weak. The difference gives Dwadasavargeeya "
    "bala. If a planet is strong in more charts, it is strong overall. If a "
    "planet is weak in more charts, it is weak overall.")

FOOTNOTE_82 = (
    "Dwaadasa means \"twelve\". Dwaadasavargeeya means \"from the 12 "
    "groups\".")

DWAADASA_MEANS = "twelve"
DWAADASAVARGEEYA_MEANS = "from the 12 groups"

#: The twelve charts, in the section's order. D-1 to D-12 with nothing
#: skipped and nothing added.
DWADASA_VARGAS: tuple[str, ...] = tuple(f"D{n}" for n in range(1, 13))

#: What makes a planet strong in one chart, in the section's order.
STRONG_IN_A_CHART: tuple[str, ...] = (
    "its exaltation rasi", "its own rasi", "a rasi owned by a friend")

#: And weak. Note there are two here and three above.
WEAK_IN_A_CHART: tuple[str, ...] = (
    "its debilitation rasi", "a rasi owned by an enemy")

#: **Finding.** These twelve are not any group the book has named before.
#: `VARGA_GROUPS` holds shadvarga, saptavarga, dasavarga and shodasavarga, and
#: **D-5, D-6, D-8 and D-11 appear in none of them**. So a third of §28.5's
#: charts are ones no earlier grouping uses, and the set is simply the first
#: twelve rather than a selection.
THE_TWELVE_ARE_NOT_ANY_EARLIER_GROUP = (
    "D-5, D-6, D-8 and D-11 belong to none of shadvarga, saptavarga, "
    "dasavarga or shodasavarga. Section 28.5's twelve is D-1 to D-12 taken "
    "consecutively, not a selection from the vargas the book already groups."
)

#: **Finding.** §28.5 reads exaltation at **rasi** level — "its exaltation
#: rasi" — where §28.4.2's uchcha bala reads it by **degree**, from the deep
#: exaltation point. Both are in the same chapter and neither mentions the
#: other. D-52 records the same sign-or-degree question for Narayana dasa.
EXALTATION_IS_BY_RASI_HERE_AND_BY_DEGREE_IN_28_4_2 = (
    "Section 28.5 asks only whether a planet is in its exaltation rasi. "
    "Section 28.4.2 measures the arc to its deep exaltation point. The "
    "chapter uses exaltation both ways without reconciling them."
)

#: **Finding.** The neutral case that OI-153 leaves open in §28.4 does not
#: arise here. §28.5 names three strong conditions and two weak ones, and a
#: rasi owned by a neutral matches none of them — so it contributes nothing to
#: a difference, which is exactly right and needs no fourth grade. The same
#: author, two sections apart, handles the same gap two ways.
THE_NEUTRAL_CASE_IS_COHERENT_HERE = (
    "A rasi owned by a neutral is neither strong nor weak in section 28.5, "
    "and a difference of counts absorbs that without a value. Section 28.4 "
    "needed one and did not give it."
)

#: **Finding.** The section says which way to read a majority and never says
#: what a **tie** means, and ties are not rare: with twelve charts and a third
#: verdict available, equal counts are an ordinary outcome. See OI-155;
#: `dwadasavargeeya_bala` returns the difference always and leaves the overall
#: verdict ``None`` when the counts are level.
A_TIE_HAS_NO_VERDICT = (
    "Strong in more charts is strong overall and weak in more is weak "
    "overall. Section 28.5 gives no reading for equal counts, which a "
    "twelve-chart count with a neutral option produces routinely."
)

#: **Finding.** The relationship scheme is unnamed, as it was throughout
#: §28.4. Here one argument settles it that did not apply there: a
#: **compound** relationship depends on where the planets sit, so it would
#: differ from varga to varga and the twelve charts would be judged by twelve
#: different friendships. The **natural** relationship is the only one stable
#: across the set, so it is what is used, and the reason is recorded.
THE_NATURAL_RELATIONSHIP_IS_THE_ONLY_STABLE_ONE_HERE = (
    "Section 28.5 says \"a rasi owned by a friend\" without naming a scheme. "
    "A compound relationship is computed from positions and would change "
    "between the twelve charts; the natural one does not."
)

#: **Finding.** The nodes cannot be scored. Chapter 3's natural relationship
#: is defined for the seven classical grahas only, and Rahu and Ketu own no
#: rasi, so neither the friend nor the own test can be applied to them. That
#: is the fourth strength in Part 4 to cover seven planets — harsha bala,
#: pancha vargeeya bala and the deeptamsas being the others.
THE_NODES_CANNOT_BE_SCORED = (
    "Dwadasavargeeya bala needs a rasi's owner and a friendship, and the "
    "nodes own nothing and have no natural relationships in chapter 3's "
    "table. Section 28.5 is a seven-planet measure like the rest of Part 4."
)


class DwadasaVargeeyaError(validate.InputError):
    """A dwadasavargeeya bala input that cannot be resolved."""


def strength_in_rasi(graha: int, rasi: int) -> dict:
    """Whether `graha` is strong, weak or neither in `rasi`.

    §28.5's own five conditions, tested in its own order. A rasi owned by a
    neutral is neither, which is the section's silence and not an omission —
    see `THE_NEUTRAL_CASE_IS_COHERENT_HERE`.
    """
    index = validate.in_range("graha", int(graha), 0, 6)
    sign = validate.in_range("rasi", int(rasi), 0, 11)
    owner = int(RASI_LORD[sign])
    if sign == int(EXALTATION_RASI[index]):
        return {"verdict": "strong", "because": "its exaltation rasi",
                "owner": owner}
    if owner == index:
        return {"verdict": "strong", "because": "its own rasi",
                "owner": owner}
    if sign == int(DEBILITATION_RASI[index]):
        return {"verdict": "weak", "because": "its debilitation rasi",
                "owner": owner}
    relation = natural(index, owner)
    if relation == "friend":
        return {"verdict": "strong", "because": "a rasi owned by a friend",
                "owner": owner}
    if relation == "enemy":
        return {"verdict": "weak", "because": "a rasi owned by an enemy",
                "owner": owner}
    return {"verdict": "neither",
            "because": "a rasi owned by a neutral, which section 28.5 counts "
                       "neither way",
            "owner": owner}


def dwadasavargeeya_bala(graha: int, longitude: float) -> dict:
    """§28.5's count across D-1 to D-12, and the difference it gives.

    :returns: every chart's verdict, the two counts, their difference, and
        the overall reading — ``None`` when the counts are level, which the
        section does not cover. See OI-155.
    """
    index = validate.in_range("graha", int(graha), 0, 6)
    place = validate.longitude("longitude", float(longitude))
    charts = []
    for code in DWADASA_VARGAS:
        sign = varga(place, code).sign
        found = strength_in_rasi(index, sign)
        charts.append({
            "chart": code,
            "rasi": sign,
            "rasi_name": str(RASI_NAMES[sign]),
            "owner": found["owner"],
            "owner_name": str(GRAHA_NAMES[found["owner"]]),
            "verdict": found["verdict"],
            "because": found["because"],
        })
    strong = sum(1 for row in charts if row["verdict"] == "strong")
    weak = sum(1 for row in charts if row["verdict"] == "weak")
    return {
        "graha": index,
        "graha_name": str(GRAHA_NAMES[index]),
        "longitude": place,
        "charts": tuple(charts),
        "strong": strong,
        "weak": weak,
        "neither": len(charts) - strong - weak,
        "units": strong - weak,
        "overall": ("strong" if strong > weak else
                    "weak" if weak > strong else None),
        "tie": strong == weak,
        "tie_note": None if strong != weak else A_TIE_HAS_NO_VERDICT,
        "rule": DWADASA_VARGEEYA_RULE,
    }
