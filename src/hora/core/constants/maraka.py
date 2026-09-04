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

#: **Gap.** §14.3 says "find the 8th house using Table 32 and not in the normal
#: way", with no exception. Example 86, eight chapters later, takes one:
RUDRA_TABLE_32_SATURN_EXCEPTION = (
    "Because Saturn is in Cn, we take the 8th houses from Cn and Cp in the "
    "normal way, instead of using Table 32."
)

#: **Finding.** What that exception undoes is a *direction*. Footnote 50 counts
#: the 8th zodiacally from an odd rasi and anti-zodiacally from an even one,
#: and Cancer and Capricorn are both even: Table 32 sends them to Sagittarius
#: and Gemini, which are their anti-zodiacal 8ths, while "the normal way"
#: gives Aquarius and Leo. So the exception reverses footnote 50's count back
#: to zodiacal — the same thing §18.2.1's Saturn exception does to a Narayana
#: dasa's direction. What it does not say is what triggers it: Saturn occupies
#: one of the two reference rasis here and owns the other. See OI-134.
TABLE_32_EXCEPTION_REVERSES_THE_COUNT = (
    "Table 32's entries for Cancer and Capricorn are their anti-zodiacal 8th "
    "houses, which is footnote 50's rule for an even rasi. Example 86's \"the "
    "normal way\" is the zodiacal count, giving Aquarius and Leo. The two "
    "routes give different Rudra candidates on every chart with those "
    "references, so the exception is not a refinement."
)

#: **Gap.** Neither §14.3 nor §14.4 says which co-lord owns a co-owned 8th
#: house. Examples 85 and 87 both call Ketu the 8th lord of Scorpio, and in
#: Example 87 §15.5.1's cascade says Mars — and the choice decides the whole
#: longevity category there, so it is not cosmetic. See OI-135.
CO_OWNED_EIGHTH_LORD_IS_UNSETTLED = (
    "The 8th house for Rudra and for section 14.4's first pair can be Scorpio "
    "or Aquarius, which have two lords. Neither section says which to take. "
    "Examples 85 and 87 both name Ketu for Scorpio; section 15.5.1's cascade "
    "gives Mars on Example 87's chart, and taking Mars there turns its short "
    "life into a long one."
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


EXAMPLE_47 = (
    "Let us say that lagna is in Ta, HL is in Ar, Moon is in Ta, Mercury is "
    "in Cn, Venus is in Cp, and Saturn is in Ge."
)

#: Example 47's chart. A hypothetical, so it names only the six points §14.4
#: needs and gives no birth data.
EXAMPLE_47_CHART: dict[str, str] = {
    "Lagna": "Ta", "HL": "Ar", "Moon": "Ta", "Merc": "Cn",
    "Ven": "Cp", "Sat": "Ge",
}

#: Each pair as the example works it: ``(pair, the two placements, the
#: combination it looks up, the result)``.
EXAMPLE_47_PAIRS: tuple[tuple[int, str, str, str], ...] = (
    (
        1,
        (
            "Lagna lord Venus is in Cp, a movable rasi. The 8th house is in "
            "Ge (see Table 32) and Mercury owns it. He is in Cn, another "
            "movable rasi."
        ),
        "Movable + Movable",
        "long",
    ),
    (
        2,
        "Moon is in Ta, a fixed rasi. Saturn is in Ge, a dual rasi.",
        "Fixed + Dual",
        "long",
    ),
    (
        3,
        "Lagna in Ta, a fixed rasi. Horalagna is in Ar, a movable rasi.",
        "Movable + Fixed",
        "middle",
    ),
)

EXAMPLE_47_RESULT = (
    "We see that two pairs indicate long life and one pair indicates middle "
    "life. So “long life” dominates and the native has long life. Using "
    "Table 34, we see that the paramaayush for this case is 108 years."
)

EXAMPLE_47_CATEGORY = "long"
EXAMPLE_47_PARAMAAYUSH = 108

#: Example 47 exercises the two-against-one branch, which is the only one
#: Table 34 covers. The unanimous and three-way-split branches still have no
#: worked example — see docs/open-items.md OI-110.
EXAMPLE_47_COVERS = (
    "Example 47 works the two-against-one case: two pairs long, one middle, "
    "so long dominates and Table 34's middle-over-long cell gives 108 years. "
    "It is the only branch of section 14.4's combination rule the book works "
    "through."
)


# --------------------------------------------------------------------------
# §14.5 — The Eighth Lord Method
# --------------------------------------------------------------------------

EIGHTH_LORD_METHOD_RULE = (
    "Parasara and Jaimini prescribed another method for estimating the "
    "longevity category. Find the stronger of lagna and 7th house and take it "
    "as the reference. Find the 8th lord from it and see where he is placed "
    "from it. If he is in a quadrant, long life is indicated. If he is in a "
    "panaphara, middle life is indicated. If he is in an apoklima, short life "
    "is indicated."
)

#: The three house groups and the category each gives.
EIGHTH_LORD_GROUPS: tuple[tuple[str, tuple[int, ...], str], ...] = (
    ("quadrant", (1, 4, 7, 10), "long"),
    ("panaphara", (2, 5, 8, 11), "middle"),
    ("apoklima", (3, 6, 9, 12), "short"),
)

#: **Finding.** §14.5 uses the *ordinary* 8th, not Table 32. Exercise 23
#: settles it: with Scorpio as reference it calls the 8th lord Mercury, and
#: Mercury owns Gemini, the ordinary 8th from Scorpio. Table 32 sends Scorpio
#: to Sagittarius, whose lord is Jupiter.
EIGHTH_LORD_USES_THE_ORDINARY_EIGHTH = (
    "The eighth lord method counts the 8th the ordinary way. Exercise 23 "
    "settles it: from a Scorpio reference it names Mercury, who owns Gemini "
    "— the ordinary 8th from Scorpio. Table 32 sends Scorpio to Sagittarius "
    "and Jupiter. Example 48 cannot decide it, since both give Venus for a "
    "Libra reference."
)

#: Which 8th each part of chapter 14 uses. Getting one wrong is silent.
WHICH_EIGHTH_HOUSE: tuple[tuple[str, str, str], ...] = (
    ("14.3 Rudra", "Table 32", "the section says so outright"),
    ("14.3 Maheswara", "ordinary",
     "exception 2 calls Sagittarius the 8th from a Taurus AK"),
    ("14.4 first pair", "Table 32", "the section says so in its parenthesis"),
    ("14.5 eighth lord method", "ordinary",
     "Exercise 23 names Mercury from a Scorpio reference"),
)

#: §14.5 says to take "the stronger of lagna and 7th house" without saying
#: how to compare them, and both worked examples state the winner as given.
EIGHTH_LORD_STRENGTH_IS_GIVEN = (
    "Section 14.5 says to take the stronger of lagna and the 7th house and "
    "does not say how to decide it. Example 48 opens 'Li is stronger than Ar' "
    "and Exercise 23 opens 'Lagna is stronger than the 7th house', both as "
    "premises. So the reference is the caller's to state."
)

EXAMPLE_48 = (
    "Let us say that lagna is in Ar and Li is stronger than Ar. Then we take "
    "Li as the reference. The 8th lord is Venus. If Venus is in Li, Cp, Ar or "
    "Cn (i.e. a quadrant from Li), it shows long life. If Venus is in Sc, Aq, "
    "Ta or Le (i.e. a panaphara from Li), it shows middle life. If Venus is "
    "in Sg, Pi, Ge or Vi (i.e. an apoklima from Li), it shows short life."
)

#: Example 48's three branches, as ``(the rasis it lists, the group, the
#: category)``. Every rasi appears exactly once across the three, so the
#: example is exhaustive.
EXAMPLE_48_BRANCHES: tuple[tuple[tuple[str, ...], str, str], ...] = (
    (("Li", "Cp", "Ar", "Cn"), "quadrant", "long"),
    (("Sc", "Aq", "Ta", "Le"), "panaphara", "middle"),
    (("Sg", "Pi", "Ge", "Vi"), "apoklima", "short"),
)

EXAMPLE_48_REFERENCE = "Li"
EXAMPLE_48_EIGHTH_LORD = "Venus"


# --------------------------------------------------------------------------
# Exercise 23 — the whole chapter over Chart 8
# --------------------------------------------------------------------------

EXERCISE_23 = (
    "Consider the rasi chart shown in Chart 8. Identify the maraka planets in "
    "this chart. Find Rudra, Trishoolas and Maheswara. Finally estimate the "
    "longevity category of the native using the method of three pairs and the "
    "eighth lord method."
)

EXERCISE_23_MARAKAS = (
    "Jupiter and Venus own the 2nd and 7th houses. Rahu is in the 7th house. "
    "These three planets are the main marakas. Mercury owns 8th and joins "
    "Jupiter and Venus. So he may also be considered a maraka."
)

#: The three the exercise calls the main marakas, and how each qualifies.
EXERCISE_23_MAIN_MARAKAS: tuple[tuple[str, str], ...] = (
    ("Jupiter", "owns the 2nd house"),
    ("Venus", "owns the 7th house"),
    ("Rahu", "is in the 7th house"),
)

#: **Finding.** Mercury's route is not §14.2's stated rule. That rule admits a
#: *malefic* conjoining or aspecting the 2nd or 7th house or their lords;
#: Exercise 23 admits Mercury for owning the **8th** — a house of life — and
#: joining the two lords. And Mercury here joins Jupiter and Venus, which by
#: §13.2's reading makes him well-associated and so a natural benefic.
EXERCISE_23_MERCURY_IS_A_FURTHER_CONSIDERATION = (
    "Exercise 23 adds Mercury as a maraka for owning the 8th and joining "
    "Jupiter and Venus. Section 14.2's stated rule for extra marakas needs a "
    "malefic reaching the 2nd or 7th house or their lords, and owning the 8th "
    "is not part of it — the 8th is a house of life, not death. The exercise "
    "hedges it as 'may also be considered', and nothing here computes it."
)

EXERCISE_23_RUDRA = (
    "The 8th house from lagna is Sg (see Table 32) and its lord is Jupiter. "
    "The 8th house from Ta (the 7th house) is Ge and its lord is Mercury. "
    "Mercury is stronger, as he is more advanced in his rasi. He is Rudra. "
    "Rudra is in Libra. So Trishoola (Destroyer Shiva's trident) has spikes "
    "in Ge, Li and Aq."
)

EXERCISE_23_RUDRA_PLANET = "Mercury"
EXERCISE_23_RUDRA_RASI = "Li"
EXERCISE_23_TRISHOOLA: tuple[str, ...] = ("Ge", "Li", "Aq")
#: Which of §14.3's five strength tests decided it.
EXERCISE_23_CASCADE_STEP = 5

EXERCISE_23_MAHESWARA = (
    "Mercury is AK. The 8th from him is Ta. The 8th from him has Rahu. So we "
    "take the 6th from Li and get Pi. Its lord Jupiter is Maheswara."
)
EXERCISE_23_MAHESWARA_PLANET = "Jupiter"

EXERCISE_23_THREE_PAIRS = (
    "Lagna lord and 8th lord show middle life (fixed+movable). Moon and "
    "Saturn show middle life (fixed+movable). Lagna and horalagna show short "
    "life (fixed+fixed). So the longevity category is “middle life” (36-72 "
    "years). The native died at the age of 50 years."
)
EXERCISE_23_CATEGORY = "middle"
EXERCISE_23_PAIR_CATEGORIES: tuple[str, ...] = ("middle", "middle", "short")
EXERCISE_23_AGE_AT_DEATH = 50

EXERCISE_23_EIGHTH_LORD = (
    "Lagna is stronger than the 7th house. So let us take Sc as the "
    "reference. The 8th lord from it is Mercury. He is in an apoklima from Sc "
    "(12th). So the result is “short life”. This method did not work here."
)
EXERCISE_23_EIGHTH_LORD_CATEGORY = "short"

#: **The book records its own method failing.** The native died at 50, inside
#: the middle-life range the three-pairs method gives; the eighth lord method
#: says short life. §14.5's own exercise says so outright.
EIGHTH_LORD_METHOD_FAILED_HERE = (
    "Exercise 23 ends 'This method did not work here'. The native died at 50, "
    "which is inside the 36-72 range the method of three pairs gives, while "
    "the eighth lord method gives short life. Both results are reported as "
    "the book reports them; neither is suppressed to make the chapter look "
    "consistent."
)


# --------------------------------------------------------------------------
# Chapter 14's closing caution
# --------------------------------------------------------------------------

CHAPTER_14_CLOSING = (
    "The definitions and methods given in this chapter will be useful in "
    "timing death using dasas. The two methods of outlined here for "
    "determining the longevity category are not infallible. There are some "
    "exceptions not covered in this book. So we should not be biased by these "
    "calculations."
)

#: The book prints "The two methods of outlined here", which is a slip for
#: "The two methods outlined here". Transcribed as printed.
CHAPTER_14_CLOSING_TYPO = (
    "The closing paragraph reads 'The two methods of outlined here'. The "
    "stray 'of' is a slip for 'The two methods outlined here'. Kept as "
    "printed."
)

#: **This is PVR saying the gaps are real.** Chapter 14 leaves several rules
#: unstated — OI-108's "powerfully", OI-109's affliction override, OI-110's
#: missing paramaayush cases, and §14.5's uncompared lagna and 7th. The
#: closing paragraph says outright that the methods are not infallible and
#: that exceptions are not covered. So those items are acknowledged
#: incompleteness in the source, not a failure to find a rule that is there.
CHAPTER_14_ADMITS_ITS_GAPS = (
    "Chapter 14 closes by saying its two longevity methods 'are not "
    "infallible' and that 'there are some exceptions not covered in this "
    "book'. That is the author's own account of the gaps this project "
    "recorded while working through it, and it is why none of them was filled "
    "by guessing: the missing rules are missing from the source, not from our "
    "reading of it. Exercise 23 shows one method failing outright on the "
    "book's own chart."
)

#: What the chapter says its results are *for*, and the caution it ends on.
CHAPTER_14_USE_AND_CAUTION: tuple[str, str] = (
    "will be useful in timing death using dasas",
    "we should not be biased by these calculations",
)


# --------------------------------------------------------------------------
# Chart 61 completes Example 86's Rudra chain
# --------------------------------------------------------------------------
# Example 86 read Indira Gandhi's chart in chapter 22 and the book printed it
# eight chapters later, with Example 110. These record what the arrival
# settled. Nothing here changes `rudra`; see OI-109, OI-134 and OI-135.

#: **Finding.** With Chart 61 in hand, Example 86's Rudra can be followed
#: step by step for the first time, and every step lands:
#:
#: 1. Saturn is in Cancer, so the exception applies and the 8th houses are
#:    taken the normal way — **Aquarius** and **Leo**, not Table 32's
#:    Sagittarius and Gemini.
#: 2. Aquarius is co-owned and the example takes **Rahu**; Leo's lord is the
#:    **Sun**.
#: 3. Both conjoin exactly one planet — Rahu with Venus, the Sun with
#:    Mercury — which is the example's own "both candidates join another
#:    planet", and the cascade's first step ties.
#: 4. The cascade resolves at **step 4**: the Sun is rasi-aspected by two
#:    planets and Rahu by one, so the Sun is stronger and **Rahu is the
#:    weaker**.
#: 5. Rahu is **debilitated** in Sagittarius and rasi-aspected by Ketu, a
#:    malefic on §14.3's own list, so the affliction override fires and
#:    **Rahu becomes Rudra** — the example's answer.
EXAMPLE_86_RUDRA_CHAIN_REPRODUCES = (
    "Chart 61 makes Example 86's Rudra checkable end to end. The exception "
    "gives Aquarius and Leo, their lords Rahu and the Sun tie at cascade step "
    "1 as the example says, step 4 makes the Sun stronger on rasi aspects "
    "two to one, and the weaker Rahu is debilitated in Sagittarius and "
    "aspected by Ketu, so the affliction override makes him Rudra."
)

#: **Finding.** The same chart shows our default disagreeing with the book,
#: and names all three reasons. `rudra` returns **Mercury** on Chart 61 where
#: Example 86 gives **Rahu**, because it takes Table 32's Sagittarius and
#: Gemini rather than applying the Saturn exception (OI-134), would take
#: Saturn as Aquarius's first co-lord rather than Rahu (OI-135), and does not
#: apply the affliction override (OI-109). Each is an open item on its own and
#: none is changed here; this is the first chart on which all three bite at
#: once, and the first on which the book's answer can be reconstructed.
CHART_61_SEPARATES_ALL_THREE_RUDRA_OPEN_ITEMS = (
    "On Chart 61 our default Rudra is Mercury and the book's is Rahu. Table "
    "32 versus the Saturn exception changes the two houses, the co-lord "
    "choice for Aquarius changes one candidate, and the affliction override "
    "changes the winner. It is the only chart so far where all three matter."
)

#: The Rudra Example 86 names, and the two houses it reaches him through.
EXAMPLE_86_RUDRA = "Rahu"
EXAMPLE_86_RUDRA_HOUSES = ("Aquarius", "Leo")


#: **Finding.** Every co-owned 8th house the book has actually read, it reads
#: as the **node**. Scorpio is called Ketu's in Examples 85 and 87, and
#: Aquarius is called Rahu's in Example 86 — three for three, and the opposite
#: of our first-co-lord default in both signs. It is a pattern in the worked
#: examples, not a rule PVR states, so nothing acts on it. See OI-135.
THE_BOOK_ALWAYS_TAKES_THE_NODE_AS_THE_CO_LORD = (
    "Scorpio's 8th lord is Ketu in Examples 85 and 87 and Aquarius's is Rahu "
    "in Example 86. In all three co-owned 8th houses the book has read, it "
    "names the node rather than Mars or Saturn."
)

#: The three instances behind that pattern: (example, rasi, the co-lord the
#: book names, the co-lord our default would take).
CO_OWNED_EIGHTH_INSTANCES: tuple[tuple[int, str, str, str], ...] = (
    (85, "Scorpio", "Ketu", "Mars"),
    (86, "Aquarius", "Rahu", "Saturn"),
    (87, "Scorpio", "Ketu", "Mars"),
)
