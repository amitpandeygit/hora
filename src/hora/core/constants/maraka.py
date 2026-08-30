"""Chapter 14 — topics related to longevity.

Section 14.2's marakas. The chapter's own framing on how the subject is used
is transcribed first and served with every answer, because it is the book's
and not ours to leave out.
"""
from __future__ import annotations

CHAPTER_14_INTRO = (
    "Many human beings are curious about how long they will live. An ethical "
    "astrologer will not scare a client by predicting death, but he may "
    "caution a client gently before critical periods and suggest some "
    "remedial measures to ward off an impending danger. An estimation of "
    "longevity is also helpful in matchmaking. After all, if one person will "
    "live for 81 years and the other only for 36 years, it is not advisable "
    "to approve a match between those two people. In matchmaking, it is "
    "desirable that the bridegroom and the bride have comparable longevity."
)

CHAPTER_14_SCOPE = (
    "In this chapter, we will study some basic tools that are used in "
    "longevity determination techniques. There are formulas for determining "
    "longevity, based on ashtakavarga. But they do not always work and they "
    "will not be covered in this book. We will cover the estimation of "
    "longevity based on natal chart and dasas. Though there are many dasas "
    "that help us in timing death, we will cover only Shoola dasa in this "
    "book."
)

#: What §14.1 rules out, so a caller is not left wondering where it went.
CHAPTER_14_NOT_COVERED: tuple[tuple[str, str], ...] = (
    (
        "ashtakavarga longevity formulas",
        ("there are formulas based on ashtakavarga, but section 14.1 says "
         "'they do not always work and they will not be covered in this "
         "book'"),
    ),
    (
        "dasas other than Shoola dasa",
        ("section 14.1 says many dasas help in timing death and that only "
         "Shoola dasa is covered"),
    ),
)

MARAKA_MEANS = "killer"
MARAKA_STHANA_MEANS = "killer station"
MARAKA_GRAHA_MEANS = "killer planet"

MARAKA_CHARTS = (
    "Each chart has some rasis and planets that are called marakas (killers). "
    "Since death is an event relating to the physical existence, rasi chart "
    "is of utmost importance in seeing death. Rudramsa (D-11) shows the "
    "forces of death and destruction and it can also give insight into death. "
    "D-30 shows one's evils and punishment for the evils. Death can be a "
    "punishment for one's evils and so we should look at D-30 also. However, "
    "the most important chart is the rasi chart."
)

#: The charts §14.2 names, in the order of weight it gives them.
MARAKA_CHART_ORDER: tuple[tuple[str, str], ...] = (
    ("D1", "the most important chart is the rasi chart"),
    ("D11", "Rudramsa shows the forces of death and destruction"),
    ("D30", "shows one's evils and punishment for the evils"),
)

HOUSES_OF_LIFE_RULE = (
    "The 3rd and 8th houses are the houses of life. The 3rd house shows the "
    "vitality of one's existence and the 8th house shows the longevity. The "
    "12th house from any house shows losses related to the matters signified "
    "by that house. So the 12th house from these two houses shows death. So "
    "the 2nd and 7th houses are the houses of death. For good longevity, the "
    "3rd and 8th houses and their lords should be strong and the 2nd and 7th "
    "houses and their lords should be weak."
)

#: The houses of life, and what each shows.
HOUSES_OF_LIFE: dict[int, str] = {
    3: "the vitality of one's existence",
    8: "the longevity",
}

#: §14.2 derives the maraka houses rather than asserting them: the 12th from
#: each house of life. Chapter 11's MARAKA_HOUSES was the same pair as a bare
#: label — see OI-23, closed — and this is the derivation behind it.
MARAKA_DERIVATION: tuple[tuple[int, int], ...] = ((3, 2), (8, 7))

GOOD_LONGEVITY_RULE = (
    "For good longevity, the 3rd and 8th houses and their lords should be "
    "strong and the 2nd and 7th houses and their lords should be weak."
)

MARAKA_STHANA_RULE = (
    "The rasis containing the 2nd and 7th houses are called maraka sthanas "
    "(killer stations). When we use rasi-ruled dasas that can show death, "
    "dasas of these rasis can bring death. Lords of the 2nd and 7th houses "
    "are called maraka grahas (killer planets). When we use planet-ruled "
    "dasas that can show death, dasas of these planets can bring death."
)

ADDITIONAL_MARAKA_RULE = (
    "There are other maraka grahas too. If a malefic planet powerfully "
    "conjoins or aspects, using graha drishti, the 2nd and 7th houses or "
    "their lords, then it qualifies as a maraka graha."
)

#: The four things an additional maraka can reach.
ADDITIONAL_MARAKA_TARGETS = (
    "the 2nd house", "the 7th house", "the 2nd lord", "the 7th lord")

#: **Gap.** "Powerfully" is not quantified anywhere in §14.2. We report the
#: contact and leave the strength judgement to the caller. See
#: docs/open-items.md OI-108.
ADDITIONAL_MARAKA_POWERFULLY_UNDEFINED = (
    "Section 14.2 says a malefic qualifies if it 'powerfully' conjoins or "
    "aspects the 2nd or 7th house or their lords. It does not say what makes "
    "the contact powerful, and neither worked example applies any threshold — "
    "both simply note the contacts and conclude. We report every contact with "
    "what made it, and do not filter on a strength the section never defines."
)

MARAKA_USE = (
    "When we time one's death using a dasa, we should look for the "
    "involvement of maraka sthanas and maraka grahas. We can also use marakas "
    "when timing death using the transits of planets."
)

#: §14.2's two worked examples. Each is
#: ``(lagna, positions, expected marakas with the reason)``.
MARAKA_EXAMPLES: tuple[
        tuple[str, dict[str, str], tuple[tuple[str, str], ...]], ...] = (
    (
        "Le",
        {"Sat": "Sg", "Mars": "Ge"},
        (
            ("Saturn", "on account of owning the 7th house (Aq)"),
            (
                "Mars",
                ("a malefic in Ge who aspects the 2nd house (Vi, with the "
                 "4th house aspect) and the 7th lord (Saturn in Sg — with "
                 "the 7th house aspect)"),
            ),
        ),
    ),
    (
        "Pi",
        {"Mars": "Ge", "Merc": "Cp", "Sat": "Ar"},
        (
            ("Mars", "on account of owning the 2nd house"),
            ("Mercury", "on account of owning the 7th house"),
            (
                "Saturn",
                ("in the 2nd house, aspecting the 2nd lord Mars (with the "
                 "3rd house aspect) and the 7th lord Mercury (with the 10th "
                 "house aspect)"),
            ),
        ),
    ),
)

#: §14.2's closing judgement on the second example. It is a comparison the
#: section makes without giving a rule for it.
MARAKA_STRONGER_REMARK = (
    "So Saturn is also a maraka and he may in fact be a stronger maraka than "
    "Mars and Mercury."
)

MARAKA_STRONGER_NOT_A_RULE = (
    "Section 14.2 remarks that the second example's Saturn 'may in fact be a "
    "stronger maraka' than the two house lords, but gives no rule for ranking "
    "marakas. We return every maraka with how it qualified and do not order "
    "them."
)
