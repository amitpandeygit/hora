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


# --------------------------------------------------------------------------
# §14.3 — Rudra, Trishoola and Maheswara
# --------------------------------------------------------------------------

RUDRA_MYTHOLOGY = (
    "In Indian mythology, there are eleven Rudras. They are all different "
    "forms of Lord Shiva. They bring suffering and death to a native. "
    "Trishoola or trident is the weapon of Lord Shiva. Maheswara is the "
    "Supreme form of Lord Shiva and he gives emancipation to the soul."
)

RUDRA_INTRO = (
    "For every person, there are eleven rasis that represent the eleven "
    "Rudras. These rasis bring suffering related to various areas of life. "
    "Out of all the eleven Rudras, the one who brings suffering to the "
    "physical self is the most important one. In each chart, there is one "
    "planet that plays this role. That planet is simply called “Rudra”. "
    "That planet stands for the suffering and destruction of the native. "
    "There are three rasis designated as Trishoola rasis and they bring "
    "death."
)

#: Table 32, rasi -> the rasi its 8th house falls in for Rudra. Not the
#: ordinary 8th: see `TABLE_32_CONSTRUCTION`.
TABLE_32_EIGHTH: dict[str, str] = {
    "Ar": "Sc", "Ta": "Ge", "Ge": "Cp", "Cn": "Sg",
    "Le": "Cn", "Vi": "Aq", "Li": "Ta", "Sc": "Sg",
    "Sg": "Cn", "Cp": "Ge", "Aq": "Cp", "Pi": "Le",
}

FOOTNOTE_50 = (
    "For odd rasis, we count houses zodiacally. For even rasis, we count "
    "houses anti-zodiacally. For Brahma and Vishnu rasis, we use the regular "
    "motion. For Shiva rasis, we use Shiva's motion. That is how Table 32 is "
    "constructed. Shiva's rasi and Shiva's motion will be discussed in "
    "“Narayana Dasa”."
)

#: **Finding.** Footnote 50's first sentence accounts for eight of the twelve
#: entries: the 8th counted forward from an odd rasi and backward from an
#: even one. The four it does not account for are exactly the four **fixed**
#: rasis — Ta, Le, Sc and Aq — so those are footnote 50's "Shiva rasis", and
#: the movable and dual ones are its Brahma and Vishnu rasis. Shiva's motion
#: itself is deferred to the Narayana Dasa chapter, so Table 32 is kept as
#: data rather than derived.
TABLE_32_CONSTRUCTION = (
    "Eight of Table 32's twelve entries follow footnote 50's stated rule — "
    "the 8th counted zodiacally from an odd rasi and anti-zodiacally from an "
    "even one. The four that do not are exactly Taurus, Leo, Scorpio and "
    "Aquarius, the fixed rasis, which identifies them as footnote 50's Shiva "
    "rasis. Shiva's motion is deferred to the Narayana Dasa chapter, so the "
    "table is held as data and checked against the part of the rule the "
    "footnote does state."
)

RUDRA_RULE = (
    "Consider the lord of the 8th house from (i) lagna and (ii) the 7th "
    "house. Find the 8th house using Table 32 and not in the normal way. The "
    "stronger of the two planets becomes Rudra. If the weaker planet is "
    "afflicted, it can also become Rudra."
)

#: §14.3's strength cascade for Rudra, in the order it gives them.
RUDRA_STRENGTH_CASCADE: tuple[str, ...] = (
    "We say that a planet is stronger if it conjoins more planets.",
    (
        "If both planets conjoin the same number of planets, a planet in "
        "exaltation or own rasi is stronger."
    ),
    "A planet joining exalted planets is stronger.",
    "A planet aspected by many planets (rasi aspect) is stronger.",
    "Finally, a planet which is more advanced in its rasi is stronger.",
)

RUDRA_AFFLICTION_RULE = (
    "However, if the weaker planet is debilitated or in an inimical sign and "
    "conjoined/aspected by malefics like Mars, Saturn, Rahu and Ketu, then it "
    "becomes Rudra."
)

#: The malefics §14.3 names for the affliction test, which is a shorter list
#: than §14.2's — the Sun is absent, and "like" leaves it open-ended.
RUDRA_AFFLICTION_MALEFICS = ("Mars", "Saturn", "Rahu", "Ketu")

TRISHOOLA_RULE = (
    "The three trines from the rasi occupied by Rudra in rasi chart represent "
    "the three spikes of Shiva's Trishoola/trident. They are called Trishoola "
    "rasis. Depending on whether a native has short life or middle life or "
    "long life, one of the three Trishoola rasis kills the native during its "
    "Shoola dasa."
)

MAHESWARA_RULE = (
    "The lord of the 8th house from AK (chara atma karaka) is called "
    "Maheswara. AK stands for the soul and the 8th lord from him stands for "
    "the liberation of soul. He represents the channels through which one's "
    "soul strives for liberation."
)

#: **Finding.** Maheswara uses the *ordinary* 8th, not Table 32. Exception 2
#: settles it: "AK is Mars and he is in Taurus. Then Sg is the 8th house from
#: Mars" — the ordinary 8th from Taurus is Sagittarius, while Table 32 gives
#: Gemini. Table 32's own title says "for Rudra Calculation".
MAHESWARA_USES_THE_ORDINARY_EIGHTH = (
    "Table 32 is for Rudra only, as its title says. Maheswara counts the 8th "
    "in the ordinary way, which section 14.3's second exception settles: it "
    "calls Sagittarius the 8th from a Taurus AK, and Table 32 gives Gemini "
    "for Taurus. The first exception cannot decide it — its Gemini and Libra "
    "both give the same answer either way."
)

MAHESWARA_EXCEPTIONS: tuple[str, ...] = (
    (
        "If the 8th lord from AK is in own rasi or exaltation rasi, then take "
        "the stronger of the 8th and 12th lords from him."
    ),
    (
        "If Rahu or Ketu joins AK or the 8th from him, then we find the 6th "
        "lord from AK instead of the 8th lord. Please note that this is "
        "equivalent to taking the 8th lord in the anti-zodiacal order."
    ),
    (
        "If Rahu becomes Maheswara, we take Mercury instead. If Ketu becomes "
        "Maheswara, we take Jupiter instead."
    ),
)

#: Exception 3's substitutions.
MAHESWARA_NODE_SUBSTITUTES: dict[str, str] = {
    "Rahu": "Mercury", "Ketu": "Jupiter"}

#: §14.3's worked examples for the exceptions, each as
#: ``(which exception, the setup, what it yields)``.
MAHESWARA_EXAMPLES: tuple[tuple[int, str, str], ...] = (
    (
        1,
        "AK is Mars and he is in Ge",
        "the 8th house from AK is Cp and Saturn is Maheswara",
    ),
    (
        1,
        "Saturn is exalted in Li",
        (
            "from Saturn (Li), Venus owns the 8th house (Ta) and Mercury owns "
            "the 12th house (Vi); the stronger of Mercury and Venus becomes "
            "Maheswara"
        ),
    ),
    (
        2,
        "AK is Mars and he is in Taurus",
        "Sg is the 8th house from Mars and Jupiter, lord of Sg, is Maheswara",
    ),
    (
        2,
        "Ketu is in Ta or Sg",
        (
            "we find the 6th house from Mars instead of the 8th; it is Li, "
            "and Venus owns it, so Venus becomes Maheswara"
        ),
    ),
)

#: Exception 2's own equivalence, which is checkable: the 6th zodiacally is
#: the 8th anti-zodiacally.
SIXTH_IS_THE_ANTIZODIACAL_EIGHTH = (
    "Section 14.3 notes that taking the 6th lord from AK 'is equivalent to "
    "taking the 8th lord in the anti-zodiacal order'. Counting six forward "
    "and eight backward land on the same rasi from any starting point."
)


# --------------------------------------------------------------------------
# §14.4 — The Method of Three Pairs
# --------------------------------------------------------------------------

THREE_PAIRS_INTRO = (
    "This method allows us to determine the approximate range of one's "
    "longevity. In this method, we look at 3 pairs of planets/mathematical "
    "points. In each pair, we look at the two planets and see if they occupy "
    "a movable or fixed or dual rasi. Using Table 33, we look at the "
    "longevity category corresponding to the combination."
)

#: The three pairs, in §14.4's order. The first uses Table 32's 8th house,
#: not the ordinary one — the section says so in its own parenthesis.
THREE_PAIRS: tuple[tuple[str, str], ...] = (
    (
        "lagna lord and 8th lord",
        "find the 8th house and its lord using Table 32",
    ),
    ("Moon and Saturn", "the rasis the two planets occupy"),
    ("lagna and Horalagna (HL)", "the rasis the two points fall in"),
)

#: Table 33. Each key is the unordered pair of modalities; the value is the
#: longevity category. All six possible pairs appear, so the table is
#: exhaustive and no combination can fall through.
TABLE_33_LONGEVITY: dict[frozenset[str], str] = {
    frozenset({"fixed", "dual"}): "long",
    frozenset({"movable"}): "long",
    frozenset({"movable", "fixed"}): "middle",
    frozenset({"dual"}): "middle",
    frozenset({"movable", "dual"}): "short",
    frozenset({"fixed"}): "short",
}

#: Table 33 as the book prints it — two combination columns per result.
TABLE_33_PRINTED: tuple[tuple[str, str, str], ...] = (
    ("Fixed + Dual", "Movable + Movable", "Long life"),
    ("Movable + Fixed", "Dual + Dual", "Middle life"),
    ("Movable + Dual", "Fixed + Fixed", "Short life"),
)

#: The years each category spans.
LONGEVITY_RANGES: dict[str, tuple[int, int]] = {
    "short": (0, 36),
    "middle": (36, 72),
    "long": (72, 108),
}

LONGEVITY_RANGE_TEXT = (
    "Long life means 72-108 years. Middle life means 36-72 years. Short life "
    "means 0-36 years."
)

THREE_PAIRS_COMBINATION_RULE = (
    "If all the three pairs result in the same longevity category, that will "
    "be the combined classification. If two pairs give one result and the "
    "third pair gives a different result, then the result given by two pairs "
    "dominates. Parasara gave further hints regarding this case and suggested "
    "finding the maximum longevity (paramaayush) of a person using Table 34."
)

THREE_PAIRS_TIEBREAK_RULE = (
    "If all the three pairs give three different results (i.e. one giving "
    "short life, one giving middle life and one giving long life), then we "
    "should give preference to the third pair of lagna and horalagna. "
    "However, if Moon is in lagna or the 7th house, then the second pair of "
    "Moon and Saturn should be given preference."
)

#: Table 34, the paramaayush reckoner. Outer key is the odd pair's category,
#: inner key is the category the other two agree on.
TABLE_34_PARAMAAYUSH: dict[str, dict[str, int]] = {
    "short": {"short": 32, "middle": 64, "long": 96},
    "middle": {"short": 36, "middle": 72, "long": 108},
    "long": {"short": 40, "middle": 80, "long": 120},
}

#: **Finding.** Table 34 is not nine independent numbers. Every cell is the
#: majority category's own upper bound scaled by a factor that depends only
#: on the odd pair: 8/9 for short, 1 for middle, 10/9 for long. All nine come
#: out as exact integers, which is checked by test rather than asserted.
TABLE_34_STRUCTURE = (
    "Every cell of Table 34 is the majority category's upper bound — 36, 72 "
    "or 108 — multiplied by a factor fixed by the odd pair alone: 8/9 for a "
    "short third pair, 1 for middle, 10/9 for long. All nine products are "
    "exact integers. So the table encodes one factor triple against the three "
    "range tops, not nine separate figures."
)

TABLE_34_FACTORS: dict[str, tuple[int, int]] = {
    "short": (8, 9), "middle": (1, 1), "long": (10, 9),
}

#: **Gap.** Table 34 is introduced for the two-against-one case only, and its
#: shape needs a majority and an odd one out. §14.4 gives no paramaayush for
#: three matching pairs or for three different ones. See docs/open-items.md
#: OI-110.
PARAMAAYUSH_ONLY_FOR_THE_SPLIT_CASE = (
    "Section 14.4 introduces Table 34 for the case where two pairs agree and "
    "the third differs, and the table's own shape needs both a majority and "
    "an odd one out. It gives no paramaayush when all three pairs agree, nor "
    "when all three differ — in the latter it names a preferred pair and "
    "stops at a category."
)

#: Long life tops out at 108 years, yet Table 34's long-over-long cell is 120.
PARAMAAYUSH_CAN_EXCEED_THE_RANGE = (
    "Long life is defined as 72-108 years, but Table 34's long-over-long cell "
    "gives 120. The paramaayush is a maximum longevity and not a reading of "
    "the same range, so the two are reported side by side rather than "
    "reconciled."
)
