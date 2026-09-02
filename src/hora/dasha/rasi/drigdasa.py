"""Chapter 21 — Drigdasa, the aspect dasa.

"Drik means vision and drigdasa is a dasa based on aspects." It is the first
rasi dasa whose groups come from **aspects** rather than from houses: each of
the 9th, 10th and 11th brings itself and the three signs it aspects.

Three things separate it from chapters 19 and 20, and all three are easy to
carry over wrongly:

* its direction is **odd-footed**, not odd/even sign — chapters 19 and 20 both
  used the sign test and printed a NOTE warning against this one;
* it has **three** directions in a single run, one per group, each from its own
  leader's footedness, where every earlier rasi dasa had one;
* its groups do **not** always cover the twelve rasis. See OI-127.

Rule 5 sends the lengths to §18.2.2, so those come from
:mod:`hora.dasha.rasi.narayana` as they do for chapters 19 and 20.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core import validate
from hora.core.const import RASI_IS_ODD_FOOTED, RASI_NAMES
from hora.dasha.rasi.narayana import NarayanaError


class DrigdasaError(NarayanaError):
    """A Drigdasa input that cannot be resolved."""


#: §21.1's derivation of the name, which is also the rule in miniature.
DRIK_MEANS_VISION = (
    "Drik means vision and drigdasa is a dasa based on aspects."
)

#: What §21.1 says it shows. Part 2's map calls it "phalita - spirituality",
#: and this is the sentence behind that.
SHOWS_SPIRITUAL_VISION = (
    "It shows how spiritual vision develops in a native and steers one's "
    "life. If a native's chart promises spiritual growth, this dasa shows "
    "religious and spiritual activities and the evolution of one's soul."
)

#: §21.2's three group leaders, in order. Consecutive houses, which is what
#: makes their modalities one of each — and what OI-127 turns on.
#:
#: Example 80 works all three on a Libra lagna: the 9th Gemini forward, the
#: 10th Cancer and the 11th Leo backward, which is also the chapter's proof
#: that one run carries more than one direction.
GROUP_HOUSES: tuple[int, ...] = (9, 10, 11)

#: §21.2's direction test. Back to odd-**footed**, which §18.2.1 and §18.2.2
#: use and which chapters 19 and 20 both took pains to say they were *not*
#: using. The two classifications disagree on Taurus, Leo, Scorpio and
#: Aquarius, so carrying either chapter's rule here is wrong a third of the
#: time.
FOOTEDNESS_DECIDES_THE_DIRECTION = (
    "Order of reckoning is forward or backward based on whether the 9th house "
    "is odd-footed or even-footed."
)

#: Rule 5, the same borrowing chapters 19 and 20 make.
LENGTHS_ARE_NARAYANAS = (
    "Dasa periods of various rasis in this dasa system are found just like in "
    "Narayana dasa."
)


def direction_of(leader_sign: int) -> str:
    """A group's direction, from its leader's **footedness**.

    Not the odd/even sign test chapters 19 and 20 use. They differ on Taurus,
    Leo, Scorpio and Aquarius.
    """
    index = validate.in_range("leader_sign", leader_sign, 0, 11)
    return "forward" if RASI_IS_ODD_FOOTED[index] else "backward"


def group_signs(leader_sign: int, direction: str) -> tuple[int, ...]:
    """A leader and the three signs it aspects, in dasa order.

    §21.2 says only "forward or backward"; Example 80 spells out the walk it
    means — "go forward as Ge, Cn, Le, Vi, Li etc and find the signs that
    aspect Ge. We get Ge, Vi, Sg and Pi." So: step round the zodiac from the
    leader, forward or backward, and take the signs that aspect it in the
    order met. The leader itself heads the group, which the example's own list
    shows by starting with Ge.
    """
    from hora.charts.aspects import rasi_drishti

    index = validate.in_range("leader_sign", leader_sign, 0, 11)
    if direction not in ("forward", "backward"):
        raise DrigdasaError(
            f"direction must be 'forward' or 'backward', got {direction!r}")
    aspected = set(rasi_drishti(index))
    step = 1 if direction == "forward" else -1
    ordered = [index]
    for offset in range(1, 12):
        candidate = (index + step * offset) % 12
        if candidate in aspected:
            ordered.append(candidate)
    return tuple(ordered)


@dataclass(frozen=True, slots=True)
class Group:
    """One of §21.2's three groups of four."""

    house: int
    leader: int
    leader_name: str
    direction: str
    signs: tuple[int, ...]
    sign_names: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Progression:
    """The order in which rasis take their Drigdasa."""

    lagna: int
    lagna_name: str
    groups: tuple[Group, ...]
    #: Twelve dasas in order. Not necessarily twelve *distinct* rasis — see
    #: `covers_every_rasi`.
    signs: tuple[int, ...]
    sign_names: tuple[str, ...]
    #: True when the three groups partition the zodiac. False for the four
    #: dual lagnas, whose 9th house is fixed. See OI-127.
    covers_every_rasi: bool
    #: Rasis taking two dasas, and rasis taking none. Empty when it covers.
    repeated: tuple[int, ...]
    omitted: tuple[int, ...]
    why: str


def progression(lagna: int) -> Progression:
    """§21.2's twelve dasas for one lagna.

    Built as the section reads. Where its groups overlap — the four dual
    lagnas — the overlap is reported rather than removed: deduplicating would
    invent an order the section does not give, and dropping a repeat would
    leave eleven dasas where it asks for twelve.
    """
    index = validate.in_range("lagna", lagna, 0, 11)

    groups: list[Group] = []
    for house in GROUP_HOUSES:
        leader = (index + house - 1) % 12
        direction = direction_of(leader)
        signs = group_signs(leader, direction)
        groups.append(Group(
            house=house, leader=leader, leader_name=str(RASI_NAMES[leader]),
            direction=direction, signs=signs,
            sign_names=tuple(str(RASI_NAMES[s]) for s in signs)))

    order = tuple(s for group in groups for s in group.signs)
    seen = {s: order.count(s) for s in set(order)}
    repeated = tuple(sorted(s for s, n in seen.items() if n > 1))
    omitted = tuple(sorted(s for s in range(12) if s not in seen))
    covers = not repeated and not omitted

    why = "; ".join(
        f"the {group.house}th is {group.leader_name}, "
        f"{'odd' if RASI_IS_ODD_FOOTED[group.leader] else 'even'}-footed, so "
        f"{group.direction}" for group in groups)
    if not covers:
        why += (f" — but {', '.join(RASI_NAMES[s] for s in repeated)} take two "
                f"dasas each and {', '.join(RASI_NAMES[s] for s in omitted)} "
                f"take none; see OI-127")
    return Progression(
        lagna=index, lagna_name=str(RASI_NAMES[index]), groups=tuple(groups),
        signs=order, sign_names=tuple(str(RASI_NAMES[s]) for s in order),
        covers_every_rasi=covers, repeated=repeated, omitted=omitted, why=why,
    )


# --------------------------------------------------------------------------
# §21.3 Interpretation
# --------------------------------------------------------------------------

#: §21.3's eight readings. Every reference computes — lagna, the arudha lagna,
#: two arudha padas, and where the nodes sit — but two of the eight are
#: conditional on something the section does not settle, and those conditions
#: are carried rather than assumed away.
SPIRITUAL_READINGS: tuple[dict, ...] = (
    {"rule": 1, "reads": "AL", "test": "the dasa sign is the arudha lagna",
     "gives": "renunciation", "needs": "parivraja yogas in the chart",
     "text": ("Dasa of arudha lagna can bring renunciation if there are "
              "parivraja yogas in the chart, indicating renunciation.")},
    {"rule": 2, "reads": "AL", "test": "the dasa sign aspects the arudha lagna",
     "gives": "external activities important for one's spiritual evolution",
     "needs": None,
     "text": ("Dasas of signs aspecting arudha lagna can bring external "
              "activities that are important for one's spiritual evolution.")},
    {"rule": 3, "reads": "lagna",
     "test": "the dasa sign is lagna or the 7th from it",
     "gives": "internal awakening and self-realization", "needs": None,
     "text": ("Dasa of lagna and the 7th house can bring internal awakening "
              "and self-realization.")},
    {"rule": 4, "reads": "lagna", "test": "the dasa sign is lagna",
     "gives": "fame and power related to spreading spiritual knowledge",
     "needs": None,
     "text": ("Dasa of lagna can also bring fame and power related to "
              "spreading spiritual knowledge. A monk may, for example, become "
              "the Chief Pontiff of a monastery.")},
    {"rule": 5, "reads": "A5",
     "test": "the dasa sign holds or aspects the mantrapada",
     "gives": "a religious initiation or sadhana of a mantra", "needs": None,
     "text": ("Dasas of signs containing or aspecting mantrapada (A5, arudha "
              "pada of the 5th house) can bring a religious initiation or "
              "sadhana (rigorous practice) of a mantra.")},
    {"rule": 6, "reads": "A8", "test": "the dasa sign holds the mrityupada",
     "gives": "yogic sadhana; it can activate Kundalini sakti", "needs": None,
     "text": ("Dasa of the sign containing mrityupada (A8, arudha pada of 8th "
              "house) can bring yogic sadhana. It can activate Kundalini "
              "sakti.")},
    {"rule": 7, "reads": "Ketu", "test": "the dasa sign holds Ketu",
     "gives": "spiritual activities that take one towards liberation",
     "needs": None,
     "text": ("Ketu is the significator of moksha (final liberation). Dasa of "
              "the sign containing Ketu can bring spiritual activities that "
              "take one towards liberation.")},
    {"rule": 8, "reads": "Rahu", "test": "the dasa sign holds Rahu",
     "gives": "progress after internal turmoil, or a turn to materialism",
     "needs": "whether Rahu is favorable",
     "text": ("Dasa of the sign containing Rahu can create progress after "
              "internal turmoil if Rahu is favorable. If Rahu is unfavorable, "
              "it can take the native in the direction of materialism.")},
)

#: §21.3 rule 7's claim, which is stronger than the rule it justifies and is
#: the sharpest thing the chapter says.
KETU_IS_THE_ONLY_LIBERATOR = (
    "Ketu is the only planet who can give real spiritual awakening and "
    "liberation."
)

#: Rule 1 cannot fire until parivraja yogas exist. Nothing in the engine
#: detects them and no chapter so far has taught them, so the condition is
#: reported unsettled rather than read as absent.
PARIVRAJA_YOGAS_NOT_BUILT = (
    "Dasa of arudha lagna can bring renunciation if there are parivraja yogas "
    "in the chart, indicating renunciation."
)

#: §21.3 names A5 "mantrapada"; Example 78 read the same pada as showing one's
#: following and the trappings of power. Not a conflict — Exercise 30 stated
#: the principle, that an arudha shows the appearance of its house's matter,
#: narrowed by what is being asked. Asked about mantras it is the mantrapada;
#: asked about power it shows a following.
A5_IS_ALSO_THE_MANTRAPADA = (
    "Dasas of signs containing or aspecting mantrapada (A5, arudha pada of "
    "the 5th house) can bring a religious initiation or sadhana (rigorous "
    "practice) of a mantra."
)


def spiritual_readings(
    dasa_sign: int,
    *,
    lagna: int,
    arudha_lagna: int,
    mantrapada: int,
    mrityupada: int,
    signs: dict[int, int],
    parivraja_yogas: bool | None = None,
    rahu_favourable: bool | None = None,
) -> tuple[dict, ...]:
    """Which of §21.3's eight readings a Drigdasa sign reaches.

    :param mantrapada: A5's rasi, from :func:`hora.charts.arudha.arudha_pada`.
    :param mrityupada: A8's rasi. Both may need §15.5.1 for a co-owned house,
        which is the caller's to settle.
    :param signs: rasi per graha, for rules 7 and 8 and for the aspects.
    :param parivraja_yogas: whether the chart carries them. None — the default,
        and the only honest one today, since nothing detects them — leaves
        rule 1 reported with its condition unmet rather than dropped.
    :param rahu_favourable: rule 8 branches on it and §21.3 does not say what
        settles it. None reports both branches.
    :returns: dicts carrying the rule number, what it gives, why it applies,
        and ``undecided`` when the section made it conditional and the caller
        did not settle the condition.
    """
    from hora.charts.aspects import rasi_drishti
    from hora.core.const import Graha

    sign = validate.in_range("dasa_sign", dasa_sign, 0, 11)
    lagna_index = validate.in_range("lagna", lagna, 0, 11)
    al = validate.in_range("arudha_lagna", arudha_lagna, 0, 11)
    a5 = validate.in_range("mantrapada", mantrapada, 0, 11)
    a8 = validate.in_range("mrityupada", mrityupada, 0, 11)

    by_rule = {r["rule"]: r for r in SPIRITUAL_READINGS}
    out: list[dict] = []

    def add(rule: int, why: str, *, undecided: str | None = None,
            gives: str | None = None) -> None:
        entry = {"rule": rule, "gives": gives or by_rule[rule]["gives"],
                 "why": why}
        if undecided:
            entry["undecided"] = undecided
        out.append(entry)

    if sign == al:
        why = f"{RASI_NAMES[sign]} is the arudha lagna"
        if parivraja_yogas is True:
            add(1, f"{why}, and the chart carries parivraja yogas")
        elif parivraja_yogas is None:
            add(1, why, undecided="whether the chart carries parivraja yogas; "
                                  "nothing here detects them")
    if al in rasi_drishti(sign):
        add(2, f"{RASI_NAMES[sign]} aspects the arudha lagna "
               f"{RASI_NAMES[al]}")
    if sign in (lagna_index, (lagna_index + 6) % 12):
        add(3, f"{RASI_NAMES[sign]} is "
               + ("lagna" if sign == lagna_index else "the 7th from lagna"))
    if sign == lagna_index:
        add(4, f"{RASI_NAMES[sign]} is lagna")
    if sign == a5 or a5 in rasi_drishti(sign):
        verb = "holds" if sign == a5 else "aspects"
        add(5, f"{RASI_NAMES[sign]} {verb} the mantrapada {RASI_NAMES[a5]}")
    if sign == a8:
        add(6, f"{RASI_NAMES[sign]} holds the mrityupada")
    if signs.get(int(Graha.KETU)) == sign:
        add(7, f"Ketu is in {RASI_NAMES[sign]}")
    if signs.get(int(Graha.RAHU)) == sign:
        why = f"Rahu is in {RASI_NAMES[sign]}"
        if rahu_favourable is True:
            add(8, f"{why}, and he is favorable",
                gives="progress after internal turmoil")
        elif rahu_favourable is False:
            add(8, f"{why}, and he is unfavorable",
                gives="a turn in the direction of materialism")
        else:
            add(8, why, undecided="whether Rahu is favorable, which §21.3 "
                                  "does not say how to settle")
    return tuple(out)
