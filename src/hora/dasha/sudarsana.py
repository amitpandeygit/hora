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


# --------------------------------------------------------------------------
# §31.3 Dasa Computation
# --------------------------------------------------------------------------

#: §31.3's first paragraph, verbatim.
THE_CYCLE_OF_TWELVE = (
    "Dasas of the 12 houses run in cycles throughout a native's life. Each "
    "dasa is for one year. For example, dasa of the 1st house runs in the 1st "
    "year of one's life. Dasa of the 2nd house runs in the 2nd year of one's "
    "life. After 12 years, dasa of the 1st house will return in the 13th "
    "year. Dasa of the 2nd house will return in the 14th year. After every 12 "
    "years, the same dasas keep coming.")

#: §31.3's second paragraph, verbatim.
THE_YEAR_AND_THE_REMAINDER = (
    "One year stands for a solar year here. A new dasa starts after every one "
    "year. The exact date and time when a new SC dasa starts can be found by "
    "casting Tajaka annual chart. Look at the number of years completed. "
    "Adding one to it, you get the year that starts. Divide it by 12 and find "
    "the remainder (if the remainder is zero, make it 12). This remainder "
    "gives the house whose dasa runs in the year.")

#: §31.3's reading of the house, and its simplification, verbatim.
THE_HOUSE_IS_READ_FROM_ALL_THREE = (
    "When we say dasa of the 9th house here, we mean the 9th house from "
    "lagna, Moon and Sun. If lagna is in Pi, Moon is in Aq and Sun is in Cn, "
    "then the 9th house is in Sc, Li and Pi. However, analyzing with 3 signs "
    "becomes difficult. So one may conveniently choose the strongest "
    "reference out of lagna, Moon and Sun and take dasas from it. This is "
    "only an approximation, but it simplifies analysis.")

#: The Antardasas paragraphs, verbatim.
ANTARDASA_RULE = (
    "Each dasa is divided into 12 antardasas. Take the dasa sign as lagna and "
    "give the 1st, 2nd, 3rd etc houses from it to antardasas. If Pi is natal "
    "lagna, dasa in the 45th year belongs to the 9th house, i.e. Sc. "
    "Antardasas in this dasa go as Sc, Sg, Cp, Aq etc. We can use Tajaka "
    "monthly charts to find the date and time when an antardasa starts. "
    "Similarly, we can find pratyantardasas from antardasas and use Tajaka "
    "sixty-hour charts to find the date and time when a pratyantardasa "
    "starts.")

#: The paragraph that ties chapters 27 to 30 back to this one, verbatim.
THE_TAJAKA_CHARTS_ARE_ENTRY_CHARTS = (
    "In short, Tajaka annual, monthly and sixty-hour charts are nothing but "
    "the entry charts of dasas, antardasas and pratyantardasas as per "
    "Sudarsana Chakra dasa. Muntha in Tajaka annual charts is nothing but the "
    "dasa sign as per Sudarsana Chakra dasa, but always reckoned from lagna. "
    "If we redefine muntha to be the progressed from the strongest of lagna, "
    "Moon and Sun (instead of always from lagna), it exactly becomes the SC "
    "dasa sign.")

#: The closing paragraph, verbatim.
SC_DASA_IN_A_VARGA = (
    "We can find Sudarsana Chakra dasa for divisional charts also. We take "
    "the strongest of lagna, Moon and Sun and then start SC dasa from there. "
    "It moves at the rate of one house per year. Examples will make this "
    "clear.")

FIGURE_4_TITLE = "Sudarsana Chakra"


def dasa_house(year: int) -> int:
    """§31.3's house for a given year of life: the year modulo twelve.

    "Divide it by 12 and find the remainder (if the remainder is zero, make
    it 12)." The 45th year gives the 9th house.
    """
    index = validate.in_range("year", int(year), 1, 200)
    return index % 12 or 12


def dasa_signs(*, lagna_rasi: int, moon_rasi: int, sun_rasi: int,
               year: int) -> dict:
    """The dasa's three rasis — the same house from lagna, Moon and Sun."""
    house = dasa_house(year)
    seats = {
        "lagna": validate.in_range("lagna_rasi", int(lagna_rasi), 0, 11),
        "Moon": validate.in_range("moon_rasi", int(moon_rasi), 0, 11),
        "Sun": validate.in_range("sun_rasi", int(sun_rasi), 0, 11),
    }
    return {
        "year": int(year),
        "house": house,
        "signs": {name: house_from(seat, house) for name, seat in seats.items()},
        "sign_names": {name: str(RASI_NAMES[house_from(seat, house)])
                       for name, seat in seats.items()},
        "rule": THE_HOUSE_IS_READ_FROM_ALL_THREE,
    }


def antardasa_signs(dasa_sign: int) -> tuple[int, ...]:
    """§31.3's twelve antardasas: the dasa sign as lagna, then its houses."""
    seat = validate.in_range("dasa_sign", int(dasa_sign), 0, 11)
    return tuple((seat + step) % 12 for step in range(12))


def pratyantardasa_signs(antardasa_sign: int) -> tuple[int, ...]:
    """The twelve pratyantardasas of one antardasa, by the same rule."""
    return antardasa_signs(antardasa_sign)


# --------------------------------------------------------------------------
# What §31.3 settles about chapters 27 to 30
# --------------------------------------------------------------------------

#: **Finding, and it is a three-way identity the book states only half of.**
#: §31.3 says "Muntha in Tajaka annual charts is nothing but the dasa sign as
#: per Sudarsana Chakra dasa, but always reckoned from lagna." That is exact:
#: §28.1's muntha is the natal lagna advanced one rasi a year, and the SC dasa
#: sign from lagna is the lagna plus the year modulo twelve, which is the same
#: rasi in every chart and every year.
#:
#: §30.4 had already made the muntha the **progressed lagna** of a Varsha
#: Narayana dasa. So one quantity carries three names in three chapters —
#: muntha, progressed lagna, SC dasa sign — and §31.3 names two of the three.
THE_MUNTHA_IS_THE_SC_DASA_SIGN_FROM_LAGNA = (
    "Section 28.1's muntha, section 30.4's progressed lagna and section "
    "31.3's SC dasa sign from lagna are one rasi under three names. Section "
    "31.3 states the second identity and section 30.4 stated the first."
)

#: **Finding.** The three Tajaka chart types map onto the three dasa levels
#: **exactly by count**, and §27.3 and §27.4 had already supplied the numbers:
#: a year holds twelve Tajaka months and a month twelve shashti-horas, while a
#: dasa holds twelve antardasas and an antardasa twelve pratyantardasas. So a
#: year holds 144 shashti-horas and a dasa 144 pratyantardasas. §31.3 says the
#: charts "are nothing but the entry charts" of the three, and the arithmetic
#: was in place four chapters earlier.
THE_THREE_CHART_TYPES_MATCH_THE_THREE_DASA_LEVELS = (
    "A Tajaka year holds twelve months and a month twelve shashti-horas; a "
    "dasa holds twelve antardasas and an antardasa twelve pratyantardasas. "
    "The counts match at every level, so 144 shashti-horas answer 144 "
    "pratyantardasas."
)

#: **Finding.** §31.3 retro-explains why chapter 27 built three kinds of chart
#: and never said what the second and third were for. §27.3's monthly charts
#: and §27.4's sixty-hour charts were given a casting rule and no reading;
#: this section supplies it — they mark antardasa and pratyantardasa entries.
CHAPTER_27S_THREE_CHARTS_FIND_THEIR_PURPOSE_HERE = (
    "Sections 27.3 and 27.4 cast monthly and sixty-hour charts without saying "
    "what to read in them. Section 31.3 says: they are the entry charts of "
    "antardasas and pratyantardasas."
)

#: **Finding.** The section offers a simplification and marks it as one: "one
#: may conveniently choose the strongest reference out of lagna, Moon and Sun
#: and take dasas from it. This is **only an approximation**." It is the only
#: place in the chapter to label its own method that way, and the varga rule
#: that follows takes the simplification as its definition — "We take the
#: strongest of lagna, Moon and Sun and then start SC dasa from there" — with
#: no three-sign version offered for a divisional chart at all.
THE_SIMPLIFICATION_BECOMES_THE_RULE_FOR_VARGAS = (
    "Section 31.3 calls choosing the strongest reference an approximation for "
    "the rasi chart and then gives it as the rule for divisional charts, "
    "where no three-sign version is offered."
)

#: **Gap.** "The strongest reference out of lagna, Moon and Sun" — the section
#: names no test. §15.5 compares two **rasis** and chapter 15's other rules
#: compare grahas; neither ranks a lagna against two grahas, which is what
#: this asks for. `dasa_signs` returns all three references and picks none.
#: See OI-180.
WHICH_REFERENCE_IS_STRONGEST_IS_NOT_SAID = (
    "Section 31.3 asks for the strongest of lagna, Moon and Sun and gives no "
    "test. Section 15.5 compares rasis and the book's other strength rules "
    "compare grahas; neither ranks a lagna against two grahas."
)

#: §31.3's own worked case, as data: a native starting the 45th year.
THE_FORTY_FIFTH_YEAR: dict[str, object] = {
    "completed": 44, "year": 45, "house": 9,
    "lagna": "Pi", "moon": "Aq", "sun": "Cn",
    "signs": {"lagna": "Sc", "Moon": "Li", "Sun": "Pi"},
    "antardasas_from_lagna": ("Sc", "Sg", "Cp", "Aq"),
}


# --------------------------------------------------------------------------
# §31.4 Dasa Interpretation
# --------------------------------------------------------------------------

#: §31.4's first three paragraphs, verbatim.
INTERPRETATION_RULE = (
    "To interpret a dasa (or antardasa or pratyantardasa), we have to take "
    "the dasa sign (or antardasa sign or pratyantardasa sign) as lagna and "
    "analyze the planetary positions with respect to it. What planetary "
    "positions do we mean - natal or transit? Some people may prefer to "
    "analyze the natal positions, but that would suggest that one gets the "
    "same results after every 12 years. That is not logical. Parasara clearly "
    "advised that we have to analyze the planetary positions at the "
    "commencement of a dasa (or antardasa or pratyantardasa) with respect to "
    "the dasa sign (or antardasa sign or pratyantardasa sign). This is where "
    "Tajaka charts fit in.")

#: §31.4's placement rules, verbatim.
PLACEMENT_RULES = (
    "If benefics are in quadrants, trines and 8th from dasa sign, favorable "
    "results can be expected. Benefics in houses other than the 6th and 12th "
    "houses produce good results for the houses they occupy. Malefics in the "
    "3rd, 6th and 11th houses bring good results. Malefics in other houses "
    "spoil the results of the houses they occupy. In particular, Rahu "
    "destroys the house he occupies.")

#: The four rules as data, with the houses each names.
PLACEMENT_VERDICTS: tuple[dict[str, object], ...] = (
    {"nature": "benefic", "houses": (1, 4, 5, 7, 8, 9, 10),
     "verdict": "favourable results can be expected",
     "source": "quadrants, trines and the 8th"},
    {"nature": "benefic", "houses": (1, 2, 3, 4, 5, 7, 8, 9, 10, 11),
     "verdict": "good results for the house occupied",
     "source": "every house but the 6th and the 12th"},
    {"nature": "malefic", "houses": (3, 6, 11),
     "verdict": "good results", "source": "the 3rd, 6th and 11th"},
    {"nature": "malefic",
     "houses": (1, 2, 4, 5, 7, 8, 9, 10, 12),
     "verdict": "spoils the results of the house occupied",
     "source": "every other house"},
)

#: The houses §31.4's first benefic rule names, as a set.
BENEFIC_FAVOURABLE_HOUSES: tuple[int, ...] = (1, 4, 5, 7, 8, 9, 10)

#: The houses §31.4 exempts a malefic in.
MALEFIC_GOOD_HOUSES: tuple[int, ...] = (3, 6, 11)


def placement_verdict(*, house: int, nature: str, graha: int | None = None
                      ) -> dict:
    """§31.4's verdict on one graha in one house from the dasa sign.

    `nature` is "benefic" or "malefic"; §31.4 does not say which
    classification it means — see `THE_NATURE_IS_NOT_QUALIFIED`.
    """
    number = validate.in_range("house", int(house), 1, 12)
    if nature not in ("benefic", "malefic"):
        raise SudarsanaError(
            f"nature must be 'benefic' or 'malefic'; got {nature!r}")
    rahu = graha is not None and int(graha) == 7

    if nature == "benefic":
        return {
            "house": number, "nature": nature,
            "favourable": number in BENEFIC_FAVOURABLE_HOUSES,
            "good_for_the_house": number not in (6, 12),
            "spoils_the_house": False,
            "rahu_destroys": False,
            "rule": PLACEMENT_RULES,
        }
    good = number in MALEFIC_GOOD_HOUSES
    return {
        "house": number, "nature": nature,
        "favourable": False,
        # "In particular, Rahu destroys the house he occupies" is emphasis
        # inside the general rule and not a rule above it: Example 126 puts
        # Rahu in the 11th and calls the placement good. OI-181 closed. See
        # `RAHU_IN_THE_ELEVENTH_IS_CALLED_GOOD`.
        "good_for_the_house": good,
        "spoils_the_house": not good,
        "rahu_destroys": rahu and not good,
        "rule": PLACEMENT_RULES,
    }


#: **Finding.** §31.4's case against reading natal positions is an argument,
#: not an assertion, and it is checkable: the SC dasa house is the year modulo
#: twelve, so it repeats every twelve years, and a natal reading from it would
#: repeat with it. "That would suggest that one gets the same results after
#: every 12 years. That is not logical." The Tajaka charts exist because the
#: **entry** chart differs each cycle while the house does not.
THE_TWELVE_YEAR_REPEAT_IS_THE_ARGUMENT = (
    "The dasa house is the year modulo twelve, so a natal reading from it "
    "would give identical results in the 1st, 13th, 25th year and so on. "
    "That is the section's reason for reading the entry chart instead."
)

#: **Finding.** The favourable list is quadrants, trines and the **8th**, and
#: the 8th is a **dusthana** — §7.4's own "bad/evil houses" are the 6th, 8th
#: and 12th. So §31.4 puts a benefic in one dusthana among its good placements
#: and excludes the other two, and the second rule excludes the 6th and 12th
#: while leaving the 8th in. The 8th is treated as good for a benefic twice
#: over and the section does not remark on it.
THE_EIGHTH_IS_GOOD_FOR_A_BENEFIC_HERE = (
    "Section 7.4's dusthanas are the 6th, 8th and 12th. Section 31.4 puts a "
    "benefic in the 8th among its favourable placements and excludes only the "
    "6th and the 12th from its second rule."
)

#: **Finding.** The malefic exemption is the **upachayas less the 10th**:
#: §7.4's upachayas are the 3rd, 6th, 10th and 11th, and §31.4 names the 3rd,
#: 6th and 11th. The 10th is the one it drops, and it is also the one house in
#: that set that is a quadrant.
THE_MALEFIC_HOUSES_ARE_THE_UPACHAYAS_LESS_THE_TENTH = (
    "The upachayas are the 3rd, 6th, 10th and 11th and section 31.4 exempts "
    "a malefic in the 3rd, 6th and 11th. The 10th is dropped, and it is the "
    "only quadrant among them."
)

#: **Finding.** The two benefic rules are not the same rule. The first names
#: seven houses and gives a general verdict; the second names ten — every
#: house but the 6th and the 12th — and gives a verdict about the house
#: occupied. The second is a superset, and the three houses it adds are the
#: **2nd, 3rd and 11th**. A benefic there is good for that house without being
#: on the favourable list.
THE_TWO_BENEFIC_RULES_COVER_DIFFERENT_HOUSES = (
    "The first benefic rule names seven houses and the second ten. The three "
    "the second adds are the 2nd, the 3rd and the 11th, where a benefic is "
    "good for its house without being favourable outright."
)

#: **Settled by Example 126.** "In particular, Rahu destroys the house he
#: occupies" follows the rule exempting malefics in the 3rd, 6th and 11th, and
#: §31.4 does not say whether it overrides that exemption — Rahu being a
#: malefic, both sentences reach him in those three houses. Example 126 puts
#: him in the **11th** and calls the placement **good**, so the exemption
#: stands and the Rahu sentence is emphasis inside the general rule. OI-181
#: closed; see `RAHU_IN_THE_ELEVENTH_IS_CALLED_GOOD`.
WHETHER_RAHU_OVERRIDES_THE_EXEMPTION_IS_NOT_SAID = (
    "Malefics in the 3rd, 6th and 11th bring good results and Rahu destroys "
    "the house he occupies. Example 126 puts Rahu in the 11th and calls it a "
    "good placement, so the exemption wins."
)

#: **Gap.** §31.4 says "benefics" and "malefics" and names no classification.
#: Chapter 3 gives Jupiter and Venus as natural benefics outright, the Moon's
#: nature by her phase and Mercury's by his company, so two of the nine are
#: conditional. `placement_verdict` takes the nature as an input.
THE_NATURE_IS_NOT_QUALIFIED = (
    "Section 31.4 does not say which benefic-and-malefic classification it "
    "means, and chapter 3 makes the Moon's nature depend on her phase and "
    "Mercury's on his company."
)


# --------------------------------------------------------------------------
# Example 126 — §31.4's rules worked on Chart 69's D-24
# --------------------------------------------------------------------------

#: Example 126, verbatim.
EXAMPLE_126 = (
    "Let us revisit Example 124. In the natal chart, lagna and Moon are in Ge "
    "in D-24. In 1987-88, the native ran the 18th year of his life. So SC "
    "dasa of the 6th house was running. The 6th house from Ge is Sc. So "
    "Scorpio dasa was running as per Sudarsana Chakra dasa of D-24. We should "
    "look at planetary positions w.r.t. Sc at the time this dasa started, "
    "i.e. in Tajaka annual chart of the year (see Chart 69). Benefics "
    "Mercury, Jupiter and Venus are in 5th, 8th and 9th respectively and all "
    "of them are good placements. Malefics Saturn, Rahu and Ketu are in 6th, "
    "11th and 11th respectively and all of them are good placements. "
    "Moreover, dasa sign Sc houses a powerful raja yoga involving the 1st, "
    "9th and 10th lords from it. For all these reasons, this year was "
    "excellent for matters shown in D-24.")

#: The closing line, verbatim.
PAY_SPECIAL_ATTENTION_TO_THE_RASI_CHART = (
    "Though Sudarsana Chakra dasa can be found for all divisional charts, pay "
    "special attention to rasi chart.")

#: Example 126's six placements, as data. Every one reproduces.
EXAMPLE_126_PLACEMENTS: tuple[dict[str, object], ...] = (
    {"graha": "Mercury", "nature": "benefic", "house": 5, "good": True},
    {"graha": "Jupiter", "nature": "benefic", "house": 8, "good": True},
    {"graha": "Venus", "nature": "benefic", "house": 9, "good": True},
    {"graha": "Saturn", "nature": "malefic", "house": 6, "good": True},
    {"graha": "Rahu", "nature": "malefic", "house": 11, "good": True},
    {"graha": "Ketu", "nature": "malefic", "house": 11, "good": True},
)

#: **Closes OI-181.** "Malefics Saturn, Rahu and Ketu are in 6th, 11th and
#: 11th respectively and **all of them are good placements**." Rahu stands in
#: the 11th, one of the three houses §31.4's exemption covers, and the example
#: calls his placement good. So "in particular, Rahu destroys the house he
#: occupies" does **not** override the 3rd, 6th and 11th — it is emphasis
#: inside the general rule, not a rule above it.
RAHU_IN_THE_ELEVENTH_IS_CALLED_GOOD = (
    "Example 126 puts Rahu in the 11th from the dasa sign and calls the "
    "placement good, so section 31.4's Rahu sentence does not override its "
    "exemption for the 3rd, 6th and 11th."
)

#: **Finding, and the book uses its own oddity.** §31.4 puts a benefic in the
#: **8th** among the favourable placements even though the 8th is one of
#: §7.4's dusthanas, and Example 126 relies on it: "Benefics Mercury, Jupiter
#: and Venus are in 5th, **8th** and 9th respectively and all of them are good
#: placements." Jupiter's 8th is the placement that would be bad anywhere else
#: in the book.
THE_EIGHTH_HOUSE_RULE_IS_USED_NOT_JUST_STATED = (
    "Jupiter stands in the 8th from the dasa sign and Example 126 calls it a "
    "good placement, which is section 31.4's own inclusion of the 8th being "
    "put to work."
)

#: **Finding.** All six placements reproduce and so does the raja yoga.
#: Scorpio holds the **Sun, Moon and Mars** in Chart 69's D-24, which from
#: Scorpio are the **10th lord, the 9th lord and the 1st lord** — the three
#: the example names.
EXAMPLE_126_REPRODUCES_WHOLE = (
    "Mercury in the 5th, Jupiter the 8th, Venus the 9th, Saturn the 6th and "
    "both nodes the 11th, and Scorpio holding the Sun, Moon and Mars, who "
    "are the 10th, 9th and 1st lords from it."
)

#: **Finding, and it is evidence on OI-180 without settling it.** The example
#: reads the dasa from **Gemini** because the natal D-24 puts lagna **and**
#: Moon there. It never mentions the natal Sun, who is in **Scorpio** in that
#: D-24 — so the three references do not coincide, the full three-sign reading
#: is not done, and no strength test is applied either. Two of the three
#: agreeing made the choice without one.
THE_EXAMPLE_USES_THE_TWO_REFERENCES_THAT_AGREE = (
    "The natal D-24 has lagna and Moon in Gemini and the Sun in Scorpio. "
    "Example 126 reads from Gemini and never mentions the Sun, so it takes "
    "the simplification without needing a strength test."
)

#: **Finding.** §31.3 gave the varga rule and §31.4's example is the first to
#: use it, and the section that follows immediately qualifies it: "Though
#: Sudarsana Chakra dasa can be found for all divisional charts, **pay special
#: attention to rasi chart**." A preference stated straight after the only
#: varga worked so far.
THE_VARGA_RULE_IS_QUALIFIED_AS_SOON_AS_IT_IS_USED = (
    "Example 126 is the chapter's first worked SC dasa and it is in a varga. "
    "The next sentence asks for special attention to the rasi chart."
)


# --------------------------------------------------------------------------
# Example 128 — the rasi-chart preference set aside for a navamsa
# --------------------------------------------------------------------------

#: Example 128, verbatim.
EXAMPLE_128 = (
    "Let us consider the lady of Chart 74. She got married in January 1999. "
    "Let us analyze her Sudarsana Chakra dasa of navamsa for 1998-99. She was "
    "born in 1973 and she started her 26th year in July 1998. If we divide 26 "
    "by 12, we get a remainder of 2. So SC dasa in 1998-99 belongs to the 2nd "
    "house. In natal navamsa, lagna is in Cn and it is stronger than Moon and "
    "Sun. The 2nd house from Cn is Le. So Le dasa was running in 1998-99. Is "
    "it a good dasa? Three benefics are in quadrants and 3 malefics are in "
    "3rd/11th. Though Mars is in 9th, he is strong being in own house. Most "
    "planets are favorably placed and, more importantly, lagna and 7th are "
    "strong with Jupiter and Venus in them (respectively). So this was a "
    "favorable year for matters shown by D-9. No wonder she got married.")

#: The 1998-99 annual chart printed inside Chart 74, which the book numbers
#: separately from nothing. Its navamsa is the chart Example 128 reads.
EXAMPLE_128_ANNUAL: dict[str, object] = {
    "birth": "July 27, 1998, 7:15 am (IST), 80 E 28, 16 N 13",
    "birth_data": {"year": 1998, "month": 7, "day": 27, "hour": 7,
                   "minute": 15, "second": 0.0, "utc_offset_hours": 5.5},
    "longitudes": {
        "Asc": "29 Cn 23", "Sun": "10 Cn 01", "Moon": "21 Le 16",
        "Mars": "20 Ge 01", "Merc": "3 Le 45", "Jup": "4 Pi 05",
        "Ven": "15 Ge 08", "Sat": "9 Ar 27", "Rahu": "8 Le 55",
        "Ketu": "8 Aq 55", "HL": "24 Le 04", "GL": "0 Sc 14",
    },
    "d9": {"Asc": "Pi", "Mars": "Ar", "Merc": "Ta", "Rahu": "Ge",
           "Sat": "Ge", "Ven": "Aq", "GL": "Cn", "AL": "Cp", "Jup": "Le",
           "Ketu": "Sg", "HL": "Sc", "Moon": "Li", "Sun": "Li"},
    "year": 26,
}

#: Example 128's placements from the Leo dasa sign, as data.
EXAMPLE_128_PLACEMENTS: tuple[dict[str, object], ...] = (
    {"graha": "Jupiter", "nature": "benefic", "house": 1},
    {"graha": "Venus", "nature": "benefic", "house": 7},
    {"graha": "Mercury", "nature": "benefic", "house": 10},
    {"graha": "Sun", "nature": "malefic", "house": 3},
    {"graha": "Saturn", "nature": "malefic", "house": 11},
    {"graha": "Rahu", "nature": "malefic", "house": 11},
    {"graha": "Mars", "nature": "malefic", "house": 9},
    {"graha": "Moon", "nature": "benefic", "house": 3},
    {"graha": "Ketu", "nature": "malefic", "house": 5},
)

#: **Finding.** Chart 74 is **Chart 53** printed again. Every one of the twelve
#: longitudes matches, and the marriage is the same marriage: Example 104 read
#: 24 January 1999 by transit against her vivaha saham in chapter 25, and
#: Example 128 reads it by Sudarsana Chakra dasa here. Forty-six chapters and
#: two methods on one wedding.
CHART_74_IS_CHART_53_AGAIN = (
    "Chart 74 reprints Chart 53's twelve longitudes exactly and adds her "
    "navamsa. Example 104 timed her January 1999 marriage by transit and "
    "Example 128 times it by SC dasa."
)

#: **Finding.** Both blocks of Chart 74 reproduce. The natal longitudes come
#: back within an arcminute and every navamsa box; the 1998-99 annual chart
#: does too, except its **ascendant**, which needs seconds the header does not
#: print. The header says 7:15 am; the printed 29 Cn 23 is reached at
#: **07:15:48**, and our own solar return for her 26th year lands at
#: **07:16:01** — thirteen seconds later, which a birth time given to the
#: minute covers. This is Chart 72's problem again: the ascendant is the only
#: body fast enough to feel a rounded clock.
BOTH_BLOCKS_REPRODUCE_AND_THE_ASCENDANT_NEEDS_SECONDS = (
    "The natal chart and both navamsas come back exactly. The annual "
    "ascendant reaches its printed 29 Cn 23 at 07:15:48 and our solar return "
    "is 07:16:01, thirteen seconds apart, with the header printing only 7:15."
)

#: **Finding, and OI-180 is still open but now has a case.** §31.2 asks for
#: three references and §31.3 allows the strongest to stand for them. Example
#: 126 never had to choose — its lagna and Moon shared a rasi. Example 128
#: does choose, and says so: "In natal navamsa, lagna is in Cn and **it is
#: stronger than Moon and Sun**." The three are in Cancer, Leo and Libra, so
#: they differ; the book asserts the lagna is strongest and still gives no
#: test.
THE_STRENGTH_CLAIM_IS_MADE_AND_STILL_NOT_SHOWN = (
    "Example 128's natal navamsa has lagna in Cancer, the Moon in Leo and the "
    "Sun in Libra, and the example says the lagna is stronger without saying "
    "how. It is the first case where the three references differ and one is "
    "chosen."
)

#: **Finding.** All nine placements reproduce and the example's counts are
#: exact: **three benefics in quadrants** — Jupiter 1st, Venus 7th, Mercury
#: 10th — and **three malefics in the 3rd or 11th** — the Sun 3rd, Saturn 11th,
#: Rahu 11th. Mars is in the 9th in Aries, his own house, which is what
#: "strong being in own house" means.
EXAMPLE_128_COUNTS_ARE_EXACT = (
    "Jupiter, Venus and Mercury take the 1st, 7th and 10th; the Sun, Saturn "
    "and Rahu take the 3rd, 11th and 11th; Mars is in the 9th in his own "
    "Aries."
)

#: **Finding, and it settles the Moon's nature here.** The example counts
#: **three** malefics in the 3rd and 11th. The Moon is also in the 3rd, so if
#: she were counted a malefic there would be four. She is waxing — about 41°
#: ahead of the Sun in the annual chart — so §3's rule makes her a benefic, and
#: the count only works that way. It is the chapter's only evidence on
#: `THE_NATURE_IS_NOT_QUALIFIED`.
THE_MOON_IS_COUNTED_A_BENEFIC_HERE = (
    "The Moon stands in the 3rd with the Sun and the example still counts "
    "three malefics there and in the 11th, so she is being taken as a "
    "benefic. She is waxing in the annual chart."
)

#: **Finding.** Ketu is in the **5th** from the dasa sign — a malefic outside
#: the 3rd, 6th and 11th, which §31.4 says spoils the house it occupies. The
#: example does not mention him. It names eight of the nine grahas and passes
#: over the one placement that counts against its conclusion, saying only that
#: "most planets are favorably placed".
KETU_IN_THE_FIFTH_IS_PASSED_OVER = (
    "Ketu is in the 5th from the dasa sign, which section 31.4 makes a "
    "spoiled house, and Example 128 does not mention him. It says most "
    "planets are favourably placed."
)

#: **Finding.** §31.4 closed by asking for "special attention to rasi chart",
#: and the two examples that follow are both in vargas — Example 126 in a D-24
#: and Example 128 in a navamsa. The preference is stated once and not
#: exercised.
THE_RASI_PREFERENCE_IS_STATED_AND_NOT_EXERCISED = (
    "Both worked SC dasas after the preference for the rasi chart are in "
    "divisional charts, a D-24 and a navamsa."
)
