"""Example 124 — academic success timed by Varsha Narayana dasa of D-24.

The same native again, four years earlier still, and the chapter's third and
last worked Varsha Narayana dasa. It is the one that settles §18.2.2's
exceptions for a varga dasa.
"""

from __future__ import annotations

CHART_NUMBER = 69

#: Example 124's opening, verbatim.
EXAMPLE_124 = (
    "The native of Exercise 48 stood State First in Intermediate (Secondary "
    "School) examinations in the AP state of India on 28th May 1987 and he "
    "was selected for Indian Institute of Technology (India's top engineering "
    "school) on 1st June 1987. Let us time this academic success using Varsha "
    "Narayana dasa of D-24.")

VARSHA_PRAVESH_DATA = "5th April 1987, 2:15:41 am (IST), 81 E 12, 16 N 15"

#: The vidya saham paragraph, verbatim.
WHY_EDUCATION = (
    "Vidya saham lord Mars is in the 5th house in rasi chart. He is in own "
    "sign in D-24, which shows education (see Chart 69). He is in the 3rd "
    "house from AL in D-24, showing material success (in education, as this "
    "is in D-24).")

#: The dasa paragraph, verbatim.
THE_DASA_PARAGRAPH = (
    "Muntha is in Aq in rasi chart. Taking Aq as lagna, 12th house is Cp. Its "
    "lord is Saturn. He is in Ar in D-24 and Ar is stronger than Li. So "
    "Varsha Narayana dasa of D-24 goes as Ar, Ta, Ge, Cn etc. Cn dasa runs "
    "during May 26-June 17, 1987. This dasa brought academic success.")

#: The four reasons, verbatim in substance and all four checkable.
WHY_CANCER: tuple[dict[str, object], ...] = (
    {"number": 1,
     "reason": "Cancer contains the lagna lord and shows prosperity to the "
               "matters signified by the chart, i.e. education"},
    {"number": 2,
     "reason": "it is the 11th from AL and shows gains in status"},
    {"number": 3, "reason": "its lord the Moon is in the 5th house from it"},
    {"number": 4,
     "reason": "the 5th house from it has a very strong Mars, in his own "
               "sign, who owns vidya saham and occupies the 5th in the rasi "
               "chart"},
)

BIRTH = {"year": 1970, "month": 4, "day": 4, "hour": 17, "minute": 50,
         "second": 0.0, "utc_offset_hours": 5.5}
PLACE = {"latitude": 16 + 15 / 60, "longitude": 81 + 12 / 60}
VARSHA_PRAVESH = {"year": 1987, "month": 4, "day": 5, "hour": 2, "minute": 15,
                  "second": 41.0, "utc_offset_hours": 5.5}
EVENTS = {"state first": (1987, 5, 28), "selected for the IIT": (1987, 6, 1)}
ANNUAL_YEAR = 18
VARGA = 24

#: **Finding.** The vidya saham reproduces and its lord is Mars, as the
#: paragraph says. The varsha pravesh is at 2:15 am, so the chart is a
#: **night** one and Table 74's vidya row reverses to Moon − Sun + Lagna; the
#: saham lands at **27 Ar 38**, whose lord is Mars. Vidya saham is the row
#: Table 74 prints without a number — see
#: `hora.tajaka.sahams.VIDYA_HAS_NO_ROW_NUMBER` — so this is its first use in
#: the book.
THE_VIDYA_SAHAM_REPRODUCES_AND_ITS_LORD_IS_MARS = (
    "The chart is cast at 2:15 am, so vidya saham takes its night form and "
    "lands at 27 Ar 38, ruled by Mars. It is the first use in the book of the "
    "row Table 74 printed without a number."
)

#: **Finding.** Every claim in the two paragraphs reproduces: Mars in the 5th
#: from the rasi lagna Capricorn, Mars in his own Scorpio in the D-24 and in
#: the 3rd from a Virgo AL there, the muntha in Aquarius, Capricorn as its
#: 12th with Saturn as lord, Saturn in Aries in the D-24, Aries stronger than
#: Libra, and the order Ar, Ta, Ge, Cn.
EVERY_CLAIM_IN_THE_PARAGRAPHS_REPRODUCES = (
    "Mars's two placements, the muntha, the twelfth from it, its lord's "
    "varga rasi, the seed comparison and the dasa order all come back as "
    "printed."
)

#: **Finding.** All four reasons for Cancer hold. The D-24 lagna is Taurus, so
#: its lord Venus is the lagna lord and he stands in **Cancer**; the arudha
#: lagna computes to **Virgo**, of which Cancer is the **11th**; Cancer's own
#: lord the Moon is in Scorpio, the **5th** from Cancer; and Scorpio holds
#: Mars in his own sign, who owns vidya saham and sits in the 5th of the rasi
#: chart.
ALL_FOUR_REASONS_FOR_CANCER_HOLD = (
    "Venus the lagna lord is in Cancer, Cancer is the 11th from the Virgo "
    "arudha lagna, the Moon is in Scorpio which is the 5th from Cancer, and "
    "Scorpio holds Mars in his own sign."
)

#: **Finding.** This is the example that fixes §18.2.2's exceptions for a
#: varga Varsha Narayana dasa. Without the lords' dignities Cancer's dasa opens
#: on 29 May 1987 and the 28 May result falls outside it; with Mercury's and
#: the Moon's debilitations in the D-24 it opens on **26 May**, the date the
#: example prints, and both events fall inside. See
#: `hora.dasha.annual.varsha_narayana.DIGNITY_APPLIES_TO_THE_SEVEN_AND_NOT_THE_NODES`.
THE_DIGNITIES_ARE_WHAT_MAKE_THE_DATE_COME_OUT = (
    "Mercury is debilitated in Pisces and the Moon in Scorpio in this D-24, "
    "shortening Gemini from 9 years to 8 and Cancer from 8 to 7. Cancer's "
    "dasa then opens on 26 May 1987, which is what the example prints, and "
    "both events fall inside it."
)

#: **Finding.** The closing date is still one day out. With the dignities
#: applied Cancer runs **26 May to 16 June** against the printed 26 May to 17
#: June — the opening exact and the close a day short. Every Varsha Narayana
#: date in the chapter has been out by a day or so at one end; this is the
#: only one whose opening lands exactly.
THE_OPENING_IS_EXACT_AND_THE_CLOSE_IS_A_DAY_SHORT = (
    "Cancer runs 26 May to 16 June against the printed 26 May to 17 June. It "
    "is the only Varsha Narayana date in the chapter whose opening is exact."
)

#: **Finding.** Chapter 30's three Varsha Narayana examples use three
#: different vargas — D-9 for a marriage, D-4 for a foreign trip, D-24 for
#: academic success — and each takes its seed lord from the house matching its
#: varga number: the 9th, the 4th and the 12th. Three cases fix the rule.
THREE_EXAMPLES_THREE_VARGAS_ONE_RULE = (
    "The chapter works D-9, D-4 and D-24 and takes the seed lord from the "
    "9th, the 4th and the 12th house of the muntha. The house is the varga "
    "number reduced by twelves."
)
