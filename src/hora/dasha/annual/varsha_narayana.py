"""§30.4 — Varsha Narayana dasa.

Narayana dasa compressed from 120 years to 360 solar days, with the **muntha**
standing in for the lagna. The book calls this the best dasa for Tajaka charts.
"""

from __future__ import annotations

from hora.core import validate
from hora.core.const import RASI_NAMES

#: §30.4's "Dasa durations", verbatim.
DURATION_RULE = (
    "This is essentially Narayana dasa compressed from 120 years to 360 solar "
    "days. If a rasi's dasa is of n years, it becomes 3 x n solar days after "
    "compression, i.e. a period in which Sun moves by (3 x n) degrees.")

#: §30.4's "Dasa order", verbatim.
ORDER_RULE = (
    "We find the dasa order in Narayana dasa of rasi chart and Narayana dasa "
    "of divisional charts just as in natal charts. The only difference is "
    "that we should progress natal lagna and use it, instead of lagna in the "
    "annual chart. Just as we progress Moon by one constellation per year "
    "when finding Varsha Vimsottari dasa, we progress lagna by one rasi per "
    "year when finding Varsha Narayana dasa. In other words, we take muntha "
    "as lagna when finding Varsha Narayana dasa. This is the link between the "
    "natal chart and the Tajaka chart.")

#: Footnote 88, verbatim. It answers OI-174.
FOOTNOTE_88 = (
    "Sum of the 2 cycles of Narayana dasa for natal charts is 12 x 12 = 144 "
    "years. However, only the first 120 years of this is valid, as the "
    "paramayush of human beings is 120 years.")

#: §30.4's closing ranking of the chapter's three dasas, verbatim.
THE_BOOKS_OWN_RANKING = (
    "Usually Patyayini dasa gives better results than Mudda dasa. Varsha "
    "Narayana dasa is, however, the best dasa for Tajaka annual charts. So we "
    "will see more examples of Varsha Narayana dasa.")

VARSHA_NARAYANA_MULTIPLIER = 3
VARSHA_NARAYANA_YEAR_DAYS = 360


def compressed_days(years: int) -> int:
    """A rasi's Narayana dasa of `years` years, in solar days."""
    return validate.non_negative("years", int(years)).__int__() * (
        VARSHA_NARAYANA_MULTIPLIER)


def progressed_lagna(natal_lagna_rasi: int, year: int) -> dict:
    """The natal lagna progressed one rasi a year — which is the muntha.

    §30.4 says so outright: "we take muntha as lagna when finding Varsha
    Narayana dasa". `hora.tajaka.muntha.muntha_rasi` computes the same rasi
    from §28.1, and `THE_PROGRESSED_LAGNA_IS_THE_MUNTHA` records that the two
    rules are one.
    """
    seat = validate.in_range("natal_lagna_rasi", int(natal_lagna_rasi), 0, 11)
    index = validate.in_range("year", int(year), 1, 200)
    rasi = (seat + index - 1) % 12
    return {
        "natal_lagna_rasi": seat,
        "year": index,
        "house_from_natal_lagna": (index - 1) % 12 + 1,
        "rasi": rasi,
        "rasi_name": str(RASI_NAMES[rasi]),
        "rule": ORDER_RULE,
    }


# --------------------------------------------------------------------------
# What the section settles, and what it leaves
# --------------------------------------------------------------------------

#: **Closes OI-174.** §30.1 said "In Vimsottari dasa and Narayana dasa,
#: paramayush of 120 years is compressed to one year", and Narayana dasa's two
#: cycles run to 144. Footnote 88 explains it in the book's own words: the sum
#: **is** 144 — "12 x 12" — but only the first 120 are used, because a human
#: paramayush is 120 years. So the divisor is 120 by intent, not by error, and
#: the arithmetic behind the 144 is the book's own.
FOOTNOTE_88_ANSWERS_THE_144 = (
    "Footnote 88 states that Narayana dasa's two cycles sum to 12 x 12 = 144 "
    "years and that only the first 120 are used, the paramayush of human "
    "beings being 120. Section 30.1's figure is deliberate."
)

#: **Finding.** §30.4 identifies two rules the book gave separately: §28.1's
#: **muntha**, the natal lagna advanced one rasi a year, and §30.4's
#: **progressed lagna**. They are the same rasi in every chart and every year,
#: and the section says so — "we take muntha as lagna" — calling it "the link
#: between the natal chart and the Tajaka chart". Two chapters apart, one
#: quantity.
THE_PROGRESSED_LAGNA_IS_THE_MUNTHA = (
    "Section 28.1's muntha and section 30.4's progressed lagna are the same "
    "rasi in every chart. The section names the identity and calls it the "
    "link between the natal chart and the Tajaka chart."
)

#: **Finding.** All three of chapter 30's dasas are seeded from the natal
#: chart and none from the annual one, and the two compressed dasas use the
#: same device: the Moon's constellation advanced one a year for mudda, the
#: lagna advanced one rasi a year here. §30.4 draws the parallel itself —
#: "just as we progress Moon by one constellation per year".
THE_TWO_COMPRESSED_DASAS_PROGRESS_THE_SAME_WAY = (
    "Mudda progresses the natal Moon's constellation and Varsha Narayana the "
    "natal lagna, both at one step a year. Neither reads the annual chart's "
    "own Moon or lagna."
)

#: **Finding.** §30.4 states the solar day again and more plainly than §30.3
#: — "a period in which Sun moves by (3 x n)°" — and its own date fits neither
#: reading. Sc, Sg, Cp and Aq are 48 solar days from 1 June 1993; in calendar
#: days that ends **19 July** and in the solar days just defined **21 July**,
#: and the section prints **20 July**, one day from each. §30.3's date matched
#: calendar days exactly. Nothing turns on it here: the marriage on 24 July
#: falls inside Pisces dasa under every reading. See OI-175.
THE_DATE_FITS_NEITHER_READING_OF_A_SOLAR_DAY = (
    "Forty-eight days from 1 June 1993 end on 19 July as calendar days and 21 "
    "July as solar days. Section 30.4 prints 20 July, one day from each, "
    "where section 30.3's date matched calendar days exactly."
)

#: **Finding.** The example needs **Scorpio's co-lord** decided and the book
#: does not say which it took. Scorpio's dasa is printed as **7 years**, and
#: that is Ketu's figure — Ketu is in Gemini in the navamsa, eight houses from
#: Scorpio. Mars, in Aquarius, gives four houses and a dasa of **3 years**. So
#: the printed number requires Ketu, and §15.5.1's own co-lord comparison,
#: computed independently, also makes Ketu the stronger. The example is the
#: first in the book where the Scorpio choice changes a Narayana dasa length.
SCORPIOS_CO_LORD_HAS_TO_BE_KETU_HERE = (
    "Scorpio's dasa is printed as 7 years, which is Ketu's length from "
    "Gemini. Mars in Aquarius would give 3. Section 15.5.1's co-lord "
    "comparison independently makes Ketu the stronger."
)

#: **Finding.** Both dasa orders the section prints reproduce, and the second
#: is the first place in the book where §18.2.1's **Saturn exception** changes
#: a printed answer. Scorpio is fixed, so its movement is "sixth" and the
#: order runs Sc, Ge, Cp, Le, Pi, Li — which the section gives as what it
#: "should have been". Saturn stands in Scorpio in the navamsa, so the
#: progression becomes regular and zodiacal: Sc, Sg, Cp, Aq, Pi, Ar.
BOTH_ORDERS_REPRODUCE_AND_SATURN_DECIDES = (
    "Scorpio's sixth movement gives Sc, Ge, Cp, Le, Pi, Li, which the section "
    "prints as the normal order, and Saturn in Scorpio makes it Sc, Sg, Cp, "
    "Aq, Pi, Ar. Both come back exactly."
)

#: **Finding.** The book ranks its own three dasas and puts this one first:
#: "Usually Patyayini dasa gives better results than Mudda dasa. Varsha
#: Narayana dasa is, however, the best dasa for Tajaka annual charts." §30.3
#: had already said patyayini showed Example 122's marriage better than mudda.
#: No reason is given for either ranking, and none of the three is scored.
THE_BOOK_RANKS_ITS_THREE_DASAS_AND_GIVES_NO_REASON = (
    "Varsha Narayana first, patyayini second, mudda third. The chapter states "
    "the order twice and argues for it nowhere."
)
