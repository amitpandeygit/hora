"""Chapter 19 — Lagna Kendradi Rasi Dasa.

The book's second rasi dasa, and the simplest. Narayana walks the zodiac by a
movement chosen from the seed's modality; this one always walks the same way —
the four quadrants from the dasa seed, then the four panapharas, then the four
apoklimas — and only its direction varies.

Almost everything else it borrows. §19.2 rule 1 takes the same dasa seed as
§18.2.1, and rule 6 says outright that "dasa periods of various rasis in this
dasa system are found just like in Narayana dasa", so lengths, sub-periods and
the solar-arc measure all come from :mod:`hora.dasha.rasi.narayana` rather than
being restated here.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core import validate
from hora.core.const import GRAHA_NAMES, RASI_IS_ODD, RASI_NAMES, Graha
from hora.dasha.rasi.narayana import BOTH_EXCEPTIONS_UNDEFINED, NarayanaError


class KendradiError(NarayanaError):
    """A Lagna Kendradi Rasi Dasa input that cannot be resolved."""


#: §19.1's account of the dasa it declines to teach. Kept because the section
#: opens with it and a reader meeting "Moola dasa" elsewhere should find the
#: book's position on it here.
MOOLA_DASA_OUT_OF_SCOPE = (
    "There is a dasa called \"Kendradi Graha Dasa\" or \"Moola dasa\", which "
    "goes through the dasas of planets in quadrants, panapharas and apoklimas "
    "from the stronger of lagna and Moon (some authors include Sun). "
    "Vimsottari dasa years with moolatrikona correction are used... Moola "
    "dasa is beyond the scope of this book."
)

#: §19.1's one claim about when it beats Vimsottari.
MOOLA_DASA_WHEN_IT_IS_BETTER = (
    "In particular, if there are 4 planets in quadrants from the stronger of "
    "lagna and Moon, this dasa gives much better results than Vimsottari dasa."
)

#: What §19.1 says this dasa is for. Narayana is "a general purpose phalita
#: dasa" (§18.6); this one is narrower.
SHOWS_MATERIAL_SUCCESS = (
    "This is a phalita dasa that shows material success well."
)

#: §19.2's three groups, in the order the dasas take them. Unlike Narayana's
#: three movements this never varies — only the direction does.
GROUPS: tuple[dict, ...] = (
    {"name": "kendra", "english": "quadrants", "houses": (1, 4, 7, 10)},
    {"name": "panaphara", "english": "succedents", "houses": (2, 5, 8, 11)},
    {"name": "apoklima", "english": "cadents", "houses": (3, 6, 9, 12)},
)

#: The twelve house numbers in order, flattened from :data:`GROUPS`.
HOUSE_ORDER: tuple[int, ...] = tuple(
    house for group in GROUPS for house in group["houses"]
)

#: §19.2 rule 2, with its own note. This is the odd/even **sign** test, the
#: same one §18.3 uses for antardasas and warns about — not the odd-footed
#: test §18.2.1 and §18.2.2 use.
DIRECTION_RULE = (
    "The direction of reckoning dasas is forward or backward based on whether "
    "lagna is in an odd sign or an even sign. NOTE: We are talking about odd "
    "and even signs here and not about odd-footed and even-footed signs."
)

#: §19.2 rule 2's two exceptions. They read the **dasa seed** where the
#: direction rule reads lagna, and unlike §18.2.1's pair they act on the same
#: thing, so a seed holding both is a direct contradiction rather than a
#: composition. See OI-120, which is the same question one chapter earlier.
EXCEPTIONS: tuple[dict, ...] = (
    {"graha": "Saturn", "text": ("If Saturn is in the stronger of lagna and "
                                 "7th, dasa order is forward."),
     "gives": "forward"},
    {"graha": "Ketu", "text": ("If Ketu is in the stronger of lagna and 7th, "
                               "dasa order is reversed."),
     "gives": "reversed"},
)

#: §19.2 rule 6, which is why this module borrows rather than restates.
LENGTHS_ARE_NARAYANAS = (
    "Dasa periods of various rasis in this dasa system are found just like in "
    "Narayana dasa."
)


def direction_of(lagna: int) -> str:
    """§19.2 rule 2's direction, from whether **lagna** is an odd sign.

    The rule names lagna where rule 1 has just named the dasa seed, and the
    two can differ — but never here. Lagna and the 7th are six signs apart and
    six is even, so they always share their parity; testing either gives the
    same answer for every chart. :func:`lagna_and_seventh_always_agree` is the
    proof, and it is why this takes a lagna and not a seed.
    """
    index = validate.in_range("lagna", lagna, 0, 11)
    return "forward" if RASI_IS_ODD[index] else "backward"


def lagna_and_seventh_always_agree(lagna: int) -> bool:
    """Whether lagna and the 7th from it share their odd/even parity.

    Always True. Kept as a function rather than a comment because §19.2's
    direction rule reads lagna while its exceptions read the dasa seed, and
    the reason that mismatch is harmless is worth being able to point at.
    """
    index = validate.in_range("lagna", lagna, 0, 11)
    return bool(RASI_IS_ODD[index]) == bool(RASI_IS_ODD[(index + 6) % 12])


def house_signs(seed: int, direction: str) -> tuple[int, ...]:
    """The twelve rasis in dasa order, counted from the seed.

    :param direction: "forward" counts houses zodiacally from the seed;
        "backward" counts them the other way, so the 4th from Taurus is
        Aquarius rather than Leo.
    """
    index = validate.in_range("seed", seed, 0, 11)
    if direction not in ("forward", "backward"):
        raise KendradiError(
            f"direction must be 'forward' or 'backward', got {direction!r}")
    step = 1 if direction == "forward" else -1
    return tuple((index + step * (house - 1)) % 12 for house in HOUSE_ORDER)


@dataclass(frozen=True, slots=True)
class Progression:
    """The order in which rasis take their Lagna Kendradi dasa."""

    seed: int
    seed_name: str
    lagna: int
    lagna_name: str
    direction: str
    #: Sign index per period, in order. Twelve entries, each rasi once.
    signs: tuple[int, ...]
    sign_names: tuple[str, ...]
    #: The house numbers those signs answer to, before direction is applied.
    houses: tuple[int, ...]
    #: The group each period belongs to — kendra, panaphara or apoklima.
    group_names: tuple[str, ...]
    #: Which of §19.2's two exceptions applied, if any.
    exception: str | None
    why: str


def progression(
    seed: int,
    lagna: int,
    seed_occupants: set[int] | None = None,
) -> Progression:
    """§19.2's full order of rasis for one dasa seed.

    :param seed: the dasa seed — the stronger of lagna and the 7th, by
        §15.5.2, which is §18.2.1's rule unchanged. Use
        :func:`hora.dasha.rasi.narayana.dasa_seed`.
    :param lagna: the chart's lagna, which rule 2 reads for the direction.
    :param seed_occupants: grahas in the **seed**, for rule 2's exceptions.
    :raises KendradiError: when the seed holds both Saturn and Ketu, whose
        exceptions contradict each other outright here.
    """
    index = validate.in_range("seed", seed, 0, 11)
    lagna_index = validate.in_range("lagna", lagna, 0, 11)

    direction = direction_of(lagna_index)
    present = set() if seed_occupants is None else {int(g) for g in seed_occupants}
    saturn = int(Graha.SATURN) in present
    ketu = int(Graha.KETU) in present
    if saturn and ketu:
        raise KendradiError(
            f"the dasa seed {RASI_NAMES[index]} holds both Saturn and Ketu. "
            f"Saturn's exception makes the order forward and Ketu's reverses "
            f"it, and §19.2 states no precedence. {BOTH_EXCEPTIONS_UNDEFINED}")

    exception = None
    if saturn:
        exception, direction = "Saturn", "forward"
    elif ketu:
        exception = "Ketu"
        direction = "backward" if direction == "forward" else "forward"

    signs = house_signs(index, direction)
    groups = tuple(group["name"] for group in GROUPS for _ in group["houses"])
    why = (f"{RASI_NAMES[lagna_index]} is an "
           f"{'odd' if RASI_IS_ODD[lagna_index] else 'even'} sign, so the "
           f"order is {direction_of(lagna_index)}; the quadrants from "
           f"{RASI_NAMES[index]} come first, then its panapharas, then its "
           f"apoklimas")
    if exception:
        why += (f" — but {GRAHA_NAMES[int(Graha.SATURN) if saturn else int(Graha.KETU)]}"
                f" occupies the seed, making it {direction}")
    return Progression(
        seed=index, seed_name=str(RASI_NAMES[index]),
        lagna=lagna_index, lagna_name=str(RASI_NAMES[lagna_index]),
        direction=direction, signs=signs,
        sign_names=tuple(str(RASI_NAMES[s]) for s in signs),
        houses=HOUSE_ORDER, group_names=groups,
        exception=exception, why=why,
    )


# --------------------------------------------------------------------------
# §19.3 Interpretation
# --------------------------------------------------------------------------

#: §19.3's attribution, which is what gives this dasa its meaning.
PARASARA_MOVEMENT_RULERS: tuple[dict, ...] = (
    {"houses": "quadrants", "ruler": "Sri Maha Vishnu"},
    {"houses": "trines", "ruler": "Sri Maha Lakshmi"},
)

#: §19.3's naming, and it inverts what a reader expects. A sequence built of
#: **trines** (1st, 5th, 9th, then the next quadrant's) is called
#: *quadrant-based*, because the groups it steps between are quadrants. A
#: sequence built of **quadrants** (1st, 4th, 7th, 10th, then the next
#: trine's) is called *trine-based*, because the groups are trines. The label
#: names the outer grouping, never the inner step.
MOVEMENT_NAMING: tuple[dict, ...] = (
    {"sequence": "1st, 5th, 9th, 10th etc", "steps": "trines",
     "grouping": "quadrant-based", "ruler": "Narayana",
     "seen_in": "Narayana dasa's dual signs — §18.2.1's Vishnu movement"},
    {"sequence": "1st, 4th, 7th, 10th", "steps": "quadrants",
     "grouping": "trine-based", "ruler": "Lakshmi",
     "seen_in": "Kendradi rasi dasa — §19.2's order"},
)

#: §19.3's own words for the inversion, kept because paraphrasing it is how a
#: reader ends up with it backwards.
MOVEMENT_NAMING_TEXT = (
    "In other words, the sequence 1st, 5th, 9th, 10th etc is quadrant-based "
    "and it is ruled by Narayana. The sequence 1st, 4th, 7th, 10th is "
    "trine-based and it is ruled by Lakshmi."
)

#: Why this dasa is the one for material fortune — §19.1 said it shows
#: material success; §19.3 says why.
LAKSHMI_SHOWS_PROSPERITY = (
    "So Kendradi rasi dasa uses the movement ruled by Lakshmi. Lakshmi is the "
    "goddess of wealth and prosperity. So this dasa shows the periods of "
    "prosperity. It shows the progression of lagna using the movement ruled "
    "by Sri Lakshmi."
)

#: §19.3's forward reference. Sudasa is this same dasa from a different seed,
#: which is why :func:`progression` takes the seed and the lagna separately.
#: §5.7 had already recorded that Sree Lagna is used in Sudasa; this is the
#: other end of that link.
SUDASA_IS_KENDRADI_FROM_SREE_LAGNA = (
    "We will learn Sudasa in a later chapter. Sudasa is also a Kendradi Rasi "
    "Dasa, but started from Sree Lagna instead of lagna. Sree Lagna is the "
    "Lakshmi sthana in a horoscope. So its progression using the movement "
    "ruled by Sri Lakshmi is more important."
)


#: §19.2 and §19.3 name the same three groups from different members. Rule 4
#: lists the second as "2nd, 5th, 8th and 11th"; §19.3 calls it "the quadrants
#: of 5th/9th", which would start it at the 5th. The **sets** are identical —
#: {2,5,8,11} is the quadrant-set of 5 — and §19.2's printed orders settle the
#: order within each group, so nothing turns on it. Recorded because the two
#: descriptions look like they disagree and do not.
SECOND_GROUP_IS_LISTED_FROM_ITS_LOWEST = (
    "Next 4 dasas will belong to the panapharas (2nd, 5th, 8th and 11th) from "
    "dasa seed."
)


def _trine_set(house: int) -> frozenset[int]:
    return frozenset(((house - 1 + 4 * k) % 12) + 1 for k in range(3))


def _quadrant_set(house: int) -> frozenset[int]:
    return frozenset(((house - 1 + 3 * k) % 12) + 1 for k in range(4))


def movement_grouping(houses: tuple[int, ...]) -> dict:
    """Which of §19.3's two movements a twelve-house order is, and who rules.

    Makes the section's claim checkable rather than only quoted. A run of four
    trines whose leaders form a quadrant is **quadrant-based** and Narayana's;
    a run of three quadrants whose leaders form a trine is **trine-based** and
    Lakshmi's.

    :param houses: twelve house numbers, 1 to 12, each once.
    :returns: the grouping, its ruler, and the groups themselves.
    :raises KendradiError: on an order that is neither.
    """
    if sorted(houses) != list(range(1, 13)):
        raise KendradiError(
            "expected the twelve houses once each, got "
            f"{sorted(houses)}")

    by_three = [houses[i:i + 3] for i in range(0, 12, 3)]
    if (all(frozenset(g) == _trine_set(g[0]) for g in by_three)
            and frozenset(g[0] for g in by_three) == _quadrant_set(by_three[0][0])):
        return {"grouping": "quadrant-based", "ruler": "Narayana",
                "steps": "trines", "groups": tuple(by_three)}

    by_four = [houses[i:i + 4] for i in range(0, 12, 4)]
    if all(frozenset(g) == _quadrant_set(g[0]) for g in by_four):
        # The three groups are then necessarily the quadrant-sets of a trine.
        # §19.3 names them from their trine members — "the quadrants of lagna,
        # then of 5th/9th, then of the 3rd trine" — while §19.2 lists each
        # from its lowest member, 1st, 2nd and 3rd. The sets are the same, and
        # §19.2's printed orders give the order within them, so that is what
        # `house_signs` follows. See SECOND_GROUP_IS_LISTED_FROM_ITS_LOWEST.
        assert {frozenset(g) for g in by_four} == {
            _quadrant_set(h) for h in _trine_set(by_four[0][0])}
        return {"grouping": "trine-based", "ruler": "Lakshmi",
                "steps": "quadrants", "groups": tuple(by_four)}

    raise KendradiError(
        f"{houses} is neither of §19.3's two movements — it is not four "
        f"trines grouped by quadrant nor three quadrants grouped by trine")


# --------------------------------------------------------------------------
# Example 76 — how a Kendradi dasa is read.
# --------------------------------------------------------------------------

#: Chapter 19 has no principle list of its own — §19.3 is about whose movement
#: this is, not about reading a period. These four are the only interpretive
#: rules it gives, and they arrive in Example 76 rather than in a section.
#: Every one is computable from what the engine already has; what is missing
#: is the layer that would apply them. Unlike OI-122's eleven these are not
#: readings §18.4's sixteen fail to carry — chapter 19 simply has no sixteen.
SUCCESS_READINGS: tuple[dict, ...] = (
    {"looks_at": "AK", "needs": "the rasi contains the atmakaraka",
     "gives": "success",
     "text": "Usually rasis containing AK give success."},
    {"looks_at": "AmK", "needs": "an unobstructed argala from the amatyakaraka",
     "gives": "political power",
     "text": ("Signs having a strong argala of AmK show coming under the "
              "decisive influence of good advisors, ministers and "
              "bureaucrats. We find in the charts of politicians that rasis "
              "having strong argalas from AmK give political power.")},
    {"looks_at": "GL", "needs": "the rasi contains ghati lagna",
     "gives": "power",
     "text": "More than anything else, Sg has GL. GL is the seat of power in "
             "a chart."},
    {"looks_at": "lagna lord", "needs": "the lagna's lord occupies the rasi",
     "gives": "a link between lagna and what the rasi holds",
     "text": "Lagna lord Mars is in Sg and he connects lagna to GL."},
)

#: Example 76's reason for the AmK rule, which is the part that makes it more
#: than an association. Recorded separately because a reading layer that gives
#: the verdict without it says something the book does not.
WHY_AMK_ARGALA_GIVES_POWER = (
    "That is because political power usually brings a leader in the company "
    "of excellent advisors, ministers, secretaries or bureaucrats."
)

#: Example 76 does not take "the lord" to mean §15.5.1's stronger co-lord. Its
#: lagna is Scorpio and it says "lagna lord Mars", while the same chart's
#: Scorpio *dasa length* and *arudha* both go to Ketu by §15.5.1. So the
#: cascade answers only where a rule sends it, and `RASI_LORD` stays the lord
#: everywhere else — which is what D-4 decided when the nodes gained
#: co-lordship without gaining `RASI_LORD`.
STRONGER_CO_LORD_IS_NOT_THE_LORD = (
    "Lagna lord Mars is in Sg and he connects lagna to GL."
)
