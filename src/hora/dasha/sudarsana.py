"""Chapter 31 — Sudarsana Chakra dasa.

A **natal** dasa, printed in Part 4 because its chakra is what the Tajaka
annual, monthly and sixty-hour charts are read against.
"""

from __future__ import annotations

from hora.core import validate
from hora.core.const import GRAHA_NAMES, NAVAGRAHA, RASI_NAMES

CHAPTER_TITLE = "Sudarsana Chakra Dasa"


# --------------------------------------------------------------------------
# §31.1 Introduction
# --------------------------------------------------------------------------

#: §31.1, verbatim.
INTRODUCTION = (
    "Parasara said that Sudarsana Chakra dasa was taught by Brahma - the "
    "Creator - Himself and that it is a great tool for predicting daily, "
    "monthly and annual fortune. Because the calculations necessary for "
    "Sudarsana Chakra dasa interpretation are an integral part of casting "
    "Tajaka annual, monthly and sixty-hour charts, this dasa is being covered "
    "in the part on \"Tajaka Analysis\" rather than the part on \"Dasa "
    "Analysis\". However, it should be borne in mind that this is a dasa "
    "applicable to natal charts. This is just a natal dasa like Vimsottari "
    "dasa, Narayana dasa and Kalachakra dasa.")

#: **Finding.** §31.1 is the second place in the book to explain **where** it
#: has put something rather than what it is. §25.4 explained a section's
#: provenance; this explains a chapter's position — a natal dasa printed among
#: the Tajaka material because its chakra is the thing chapters 27 to 30 read
#: against. The paragraph then says twice over that the dasa itself is natal,
#: which is the only reason it needs saying at all.
THE_CHAPTER_EXPLAINS_ITS_OWN_PLACEMENT = (
    "Section 31.1 says why a natal dasa is printed in the Tajaka part, and "
    "then says twice that it is a natal dasa. No other chapter explains "
    "where it sits."
)

#: The three dasas §31.1 compares this one to, in its own order.
NAMED_ALONGSIDE: tuple[str, ...] = (
    "Vimsottari dasa", "Narayana dasa", "Kalachakra dasa")

#: **Finding.** The three dasas §31.1 names as its peers are one from each
#: family the book taught: **Vimsottari** is a nakshatra dasa, **Narayana** a
#: rasi dasa and **Kalachakra** neither. Sudarsana chakra is a fourth kind
#: again — it advances one house a year from three references at once.
THE_THREE_PEERS_ARE_ONE_FROM_EACH_FAMILY = (
    "Vimsottari is a nakshatra dasa, Narayana a rasi dasa and Kalachakra "
    "neither, and sudarsana chakra is a fourth kind. The section picks one "
    "of each to place it among."
)


# --------------------------------------------------------------------------
# §31.2 Sudarsana Chakra
# --------------------------------------------------------------------------

#: §31.2's first paragraph, verbatim.
THE_THREE_REFERENCES = (
    "In each chart, there are 3 important reference points: (1) lagna, (2) "
    "Moon, and, (3) Sun. Lagna represents the physical body. Moon represents "
    "the mind. Sun represents the soul. The three together represent one's "
    "self. We should consider houses from all the three reference points when "
    "judging a chart. For example, we need to look at the 10th house from "
    "lagna, Moon and Sun to see career. Though we typically give importance "
    "to lagna, all the three references are important.")

#: §31.2's second paragraph, verbatim.
THE_THREE_CIRCLES = (
    "To symbolically represent this, we can draw Sudarsana Chakra (SC) as "
    "taught by Parasara. We should draw 3 concentric circles. We should write "
    "down the bhava chakra with respect to lagna, Moon and Sun in the inner, "
    "middle and outer charts.")

#: The three references, with what each stands for and which circle it takes.
SUDARSANA_REFERENCES: tuple[dict[str, object], ...] = (
    {"number": 1, "reference": "lagna", "stands_for": "the physical body",
     "circle": "inner"},
    {"number": 2, "reference": "Moon", "stands_for": "the mind",
     "circle": "middle"},
    {"number": 3, "reference": "Sun", "stands_for": "the soul",
     "circle": "outer"},
)

#: §31.2's worked reading of Chart 72, verbatim.
THE_TENTH_FROM_ALL_THREE = (
    "The 10th house from lagna is in Sg and it has Ketu. The 10th house from "
    "Moon is Sc and it is empty. The 10th house from Sun is Aries and it is "
    "empty. We should analyze all the 3 factors together to draw conclusions.")


class SudarsanaError(validate.InputError):
    """A sudarsana chakra input that cannot be resolved."""


def house_from(reference_rasi: int, house: int) -> int:
    """The rasi holding the `house`-th house from a reference rasi."""
    seat = validate.in_range("reference_rasi", int(reference_rasi), 0, 11)
    number = validate.in_range("house", int(house), 1, 12)
    return (seat + number - 1) % 12


def sudarsana_chakra(*, lagna_rasi: int, moon_rasi: int, sun_rasi: int,
                     graha_rasis: dict[int, int] | None = None) -> dict:
    """§31.2's three bhava chakras, and what each house of each one holds.

    :returns: one entry per reference, each with the twelve houses in order
        and the grahas standing in them.
    """
    seats = {
        "lagna": validate.in_range("lagna_rasi", int(lagna_rasi), 0, 11),
        "Moon": validate.in_range("moon_rasi", int(moon_rasi), 0, 11),
        "Sun": validate.in_range("sun_rasi", int(sun_rasi), 0, 11),
    }
    occupants: dict[int, list[int]] = {rasi: [] for rasi in range(12)}
    for graha, rasi in (graha_rasis or {}).items():
        if int(graha) not in set(NAVAGRAHA):
            raise SudarsanaError(f"unknown graha {graha!r}")
        occupants[validate.in_range("rasi", int(rasi), 0, 11)].append(
            int(graha))

    circles = {}
    for row in SUDARSANA_REFERENCES:
        name = str(row["reference"])
        seat = seats[name]
        circles[name] = {
            "reference": name,
            "stands_for": row["stands_for"],
            "circle": row["circle"],
            "rasi": seat,
            "rasi_name": str(RASI_NAMES[seat]),
            "houses": tuple(
                {"house": house,
                 "rasi": house_from(seat, house),
                 "rasi_name": str(RASI_NAMES[house_from(seat, house)]),
                 "grahas": tuple(sorted(occupants[house_from(seat, house)])),
                 "graha_names": tuple(
                     str(GRAHA_NAMES[g])
                     for g in sorted(occupants[house_from(seat, house)])),
                 "empty": not occupants[house_from(seat, house)]}
                for house in range(1, 13)),
        }
    return {
        "circles": circles,
        "order": tuple(str(row["reference"]) for row in SUDARSANA_REFERENCES),
        "rule": THE_THREE_CIRCLES,
    }


def the_same_house_everywhere(chakra: dict, house: int) -> tuple[dict, ...]:
    """One house read from all three references at once — §31.2's own method.
    """
    number = validate.in_range("house", int(house), 1, 12)
    return tuple(chakra["circles"][name]["houses"][number - 1]
                 for name in chakra["order"])


# --------------------------------------------------------------------------
# What §31.2's worked reading shows
# --------------------------------------------------------------------------

#: **Finding.** §31.2's three-house reading of Chart 72 reproduces: the 10th
#: from the Pisces lagna is **Sagittarius and holds Ketu**, the 10th from the
#: Aquarius Moon is **Scorpio and is empty**, and the 10th from the Cancer Sun
#: is **Aries and is empty**.
THE_TENTH_HOUSE_READING_REPRODUCES = (
    "Sagittarius with Ketu from the lagna, Scorpio empty from the Moon and "
    "Aries empty from the Sun, exactly as section 31.2 reads them."
)

#: **Finding.** Two things the reading settles about what "empty" counts.
#: Scorpio holds **GL and HL** in Chart 72 and §31.2 calls it empty, so the
#: special lagnas are not occupants. Sagittarius holds **Ketu and AL**, and the
#: section says it "has Ketu", so a node **is** an occupant. `sudarsana_chakra`
#: takes graha rasis alone and counts the nine.
EMPTY_MEANS_NO_GRAHA_AND_A_NODE_COUNTS = (
    "Scorpio holds GL and HL and section 31.2 calls it empty; Sagittarius "
    "holds Ketu and AL and the section says it has Ketu. Special lagnas are "
    "not occupants and the nodes are."
)

#: **Finding, and it is the sharpest ascendant test in the book.** Chart 72 is
#: the only chart whose printed **ascendant** does not reproduce from its
#: printed birth time: at 9:14:00 pm it comes out 15.8 arcminutes low, while
#: every graha is inside an arcminute. The reason is rate, not error — the
#: ascendant moves **19.7 arcminutes a clock minute** at 21 N 27 with Pisces
#: rising, so a birth time printed to the minute cannot pin it closer than
#: about ten. At 9:14:**48** the ascendant is 14 Pi 00.98 against the printed
#: 14 Pi 01, and every other body still reproduces.
THE_ASCENDANT_NEEDS_FORTY_EIGHT_SECONDS = (
    "Chart 72's ascendant is 15.8 arcminutes low at the printed 9:14:00 pm "
    "and exact at 9:14:48. It moves 19.7 arcminutes a clock minute there, so "
    "a birth time given to the minute leaves it that far out while every "
    "graha stays inside an arcminute."
)

#: **Finding.** §31.2 gives the three references an order and a meaning each,
#: and the order is not the one the book usually reads. Lagna, Moon and Sun
#: are body, mind and soul, and the section says "though we typically give
#: importance to lagna, all the three references are important" — which is the
#: first time the book asks for three charts to be weighed together rather
#: than one ranked above the others.
THE_SECTION_LEVELS_THE_THREE_REFERENCES = (
    "Lagna is the body, the Moon the mind and the Sun the soul, and section "
    "31.2 asks for all three to be judged together rather than the lagna "
    "first."
)
