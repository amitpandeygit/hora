"""Chapter 32, §32.1 — why an accurate birthtime is a precondition.

The chapter's argument is that the fast-moving points — divisional lagnas and
the special lagnas of chapter 5 — are what separate two nativities minutes
apart, so a birthtime in error by minutes is a different nativity, not an
approximation of the right one.
"""

from __future__ import annotations

from collections.abc import Callable

from hora.core import validate

CHAPTER_TITLE = "Impact of Birthtime Error"


# --------------------------------------------------------------------------
# §32.1 Introduction
# --------------------------------------------------------------------------

#: §32.1's first paragraph, verbatim. The emphasis on "proves" is the book's.
TWINS_PROVE_THE_VARGAS_MATTER = (
    "There are twins in this world who are born 1-2 minutes apart, but live "
    "significantly different lives. There may be some similarities between "
    "closely born twins, but there can be significant differences too. So "
    "this *proves* that divisional charts and special lagnas, which change "
    "very fast, have a great bearing on a native's fortune. If one's "
    "birthtime is wrong by 2 minutes, lagna and special lagnas in some "
    "divisional charts change and so the results change. This is how we can "
    "explain the differences between twins.")

#: §32.1's second paragraph, verbatim.
A_WRONG_BIRTHTIME_IS_A_HYPOTHETICAL_TWIN = (
    "Now the question is - if changes in lagna and special lagnas in "
    "divisional charts explain the different fortunes of twins, what about "
    "people who don't have a twin? Well, the same thing applies to them. If "
    "we analyze the chart cast with a birthtime that is wrong by 2 minutes, "
    "we are no longer examining the chart of the native - we are simply "
    "looking at the chart of his hypothetical twin! The results predicted "
    "need not be true.")

#: §32.1's third paragraph, verbatim. The emphasis is the book's.
WE_MUST_FIRST_HAVE_AN_ACCURATE_BIRTHTIME = (
    "Lagna in D-1 changes rasi once in 2 hours. Some people make predictions "
    "only using D-1, but that is unscientific and against the teachings of "
    "maharshis. Due to divine powers and God-given intuition, one can be "
    "successful in one's predictions only using D-1, but that is clearly "
    "unscientific. We should see different areas of life in different "
    "divisional charts, as taught by Maharshi Parasara. When we do that, we "
    "need an accurate birthtime. If one's birthtime is between 9:02 am and "
    "9:08 am, can we make accurate predictions using an average of 9:05 am? "
    "No! Many people are born within the small span of 6 minutes (between "
    "9:02 and 9:08) and they can be significantly different from each other "
    "(e.g. twins). Applying precise techniques is pointless when we only "
    "have an approximate time. So let us conclude that **we must first make "
    "sure that we are working with an accurate birthtime**. Readers should "
    "remember that our analysis could be only as accurate as our data!")

#: §32.1's fourth paragraph, verbatim.
BIRTHTIMES_ARE_SELDOM_ACCURATE = (
    "We are often told by clients that their birthtime is very accurate. "
    "However, it is this author's experience that birthtimes reported by "
    "people are seldom accurate. There can be various reasons behind a "
    "birthtime error: (1) using an unadjusted clock/wristwatch showing a "
    "slightly incorrect time, (2) forgetting to note the birthtime exactly "
    "after birth and noting down it a little later with some manual "
    "correction applied to compensate for the lapse, (3) wrong memory of "
    "mother or father when giving the correctly noted birthtime to an "
    "astrologer, (4) using the wrong definition of 'birth'.")

#: The four causes §32.1 lists, numbered as the book numbers them.
BIRTHTIME_ERROR_CAUSES: tuple[dict[str, object], ...] = (
    {"number": 1, "cause": "an unadjusted clock or wristwatch showing a "
                           "slightly incorrect time",
     "lies_with": "the instrument"},
    {"number": 2, "cause": "the time not noted at birth, written down later "
                           "with a manual correction for the lapse",
     "lies_with": "the recording"},
    {"number": 3, "cause": "wrong memory of mother or father when passing a "
                           "correctly noted birthtime to an astrologer",
     "lies_with": "the reporting"},
    {"number": 4, "cause": "using the wrong definition of 'birth'",
     "lies_with": "the definition"},
)

#: Footnote 89, verbatim.
FOOTNOTE_89 = (
    "In order to explain the differences between twins, some astrologers take "
    "the lagna of the second twin in the 3rd house (younger brother) from the "
    "first twin. If Aquarius is rising at the birth of both, they take Aries "
    "(3rd from Aquarius) as the lagna of the younger twin. This is, however, "
    "illogical, irrational and against the teachings of maharshis. One who "
    "understands what lagna means and what the rasi chart shows will reject "
    "such theories without any consideration at all.")

#: The technique footnote 89 names and rejects, held as data so it is on
#: record as **not implemented and not implementable here**: the second twin's
#: lagna is taken as the 3rd house from the first twin's.
THE_REJECTED_THIRD_HOUSE_TWIN_LAGNA: dict[str, object] = {
    "technique": "take the second twin's lagna as the 3rd house from the "
                 "first twin's, the 3rd being the younger brother",
    "worked_example": {"first_twin_lagna": "Aquarius",
                       "second_twin_lagna": "Aries"},
    "verdict": "illogical, irrational and against the teachings of maharshis",
    "source": FOOTNOTE_89,
    "implemented": False,
}


class BirthtimeError(validate.InputError):
    """A birthtime-sensitivity input that cannot be resolved."""


def varga_signs_that_change(
    before: dict[str, float],
    after: dict[str, float],
    vargas: dict[int, Callable[[float], object]],
) -> tuple[dict[str, object], ...]:
    """Which (point, varga) signs differ between two castings of one chart.

    §32.1's claim is that "if one's birthtime is wrong by 2 minutes, lagna and
    special lagnas in some divisional charts change". This answers *which*,
    for a given pair of castings.

    :param before: point name -> longitude in the chart as recorded.
    :param after: the same points in the chart cast from the shifted time.
    :param vargas: varga number -> a function returning an object with a
        ``sign`` attribute, the way `hora.charts.vargas` supplies them.
    :raises BirthtimeError: if the two castings do not carry the same points.
    """
    if set(before) != set(after):
        raise BirthtimeError(
            "before and after must hold the same points; got "
            f"{sorted(before)} and {sorted(after)}")
    if not vargas:
        raise BirthtimeError("at least one varga is needed")

    out: list[dict[str, object]] = []
    for point in sorted(before):
        for number in sorted(vargas):
            was = int(vargas[number](
                validate.longitude(point, float(before[point]))).sign)  # type: ignore[attr-defined]
            now = int(vargas[number](
                validate.longitude(point, float(after[point]))).sign)  # type: ignore[attr-defined]
            if was != now:
                out.append({"point": point, "varga": number,
                            "from_sign": was, "to_sign": now})
    return tuple(out)


# --------------------------------------------------------------------------
# What §32.1 says, and what it measures out to
# --------------------------------------------------------------------------

#: **Finding, measured.** "Lagna in D-1 changes rasi once in 2 hours" is a
#: **mean**, not a rate. Twelve rasis rise in one sidereal day, so the average
#: span is 1436 minutes over 12 = **119.7 minutes**, which is the two hours to
#: within twenty seconds. The individual spans are nothing like it, and the
#: spread widens with latitude: at the equator the shortest rasi takes 110
#: minutes and the longest 130; at 16 N 15 it is 96 and 133; at 42 N 30 —
#: Chart 1's latitude — it is 67 and 155; at 60 N it is 28 and 195.
#:
#: Nothing in the argument turns on it. The section needs an order of
#: magnitude, and two hours is the right order of magnitude everywhere.
THE_TWO_HOURS_IS_A_MEAN_NOT_A_RATE = (
    "Twelve rasis rise in a sidereal day, so the mean span is 119.7 minutes. "
    "The actual spans run 110 to 130 minutes at the equator, 67 to 155 at 42 "
    "N 30 and 28 to 195 at 60 N."
)

#: **Finding, measured on Chart 1.** The section's claim is understated. Move
#: the reference chart's birthtime by the two minutes §32.1 names and, across
#: the ascendant and the four special lagnas of chapter 5 in twenty-three
#: vargas — 115 signs in all — **54 change**. Not one of the five changes in
#: D-1, which is why the claim is worded about divisional charts; the
#: ascendant first changes at D-27, and **Ghati Lagna changes in eighteen of
#: the twenty-three**, because §5.5 advances it 1.25° a minute against the
#: ascendant's own 0.19° here.
FIFTY_FOUR_OF_A_HUNDRED_AND_FIFTEEN_SIGNS_MOVE = (
    "Two minutes on Chart 1 changes 54 of the 115 varga signs of the "
    "ascendant and the four special lagnas, and none of the five in D-1. "
    "Ghati Lagna changes in 18 of the 23 vargas."
)

#: **Finding.** §32.1 supplies the reason the ascendants of Charts 72, 73 and
#: 74 needed seconds their headers never printed. Each of those figures was
#: reproduced by solving for the printed ascendant — 48, 50 and 48 seconds
#: past the printed minute — and the arithmetic there is this section's:
#: the ascendant moves 13 to 20 arcminutes a clock minute, so a header that
#: rounds to the minute leaves a chart whose fast points are a different
#: native's. The book prints the rounded time and computes from the exact one.
THE_CHAPTER_EXPLAINS_THE_ROUNDED_HEADERS = (
    "Charts 72, 73 and 74 each needed seconds their headers did not print, "
    "and section 32.1 is the section that says why that matters."
)

#: **Finding.** The same charge is laid twice in one section, in the same
#: words: reading only D-1 is "unscientific and **against the teachings of
#: maharshis**", and footnote 89's third-house lagna for the second twin is
#: "illogical, irrational and **against the teachings of maharshis**". One is
#: a method the book says is too coarse, the other a method it says is
#: baseless; the objection offered against both is the same appeal.
THE_SAME_OBJECTION_IS_MADE_TO_BOTH_PRACTICES = (
    "Reading only D-1 and taking the second twin's lagna from the 3rd house "
    "are both dismissed as against the teachings of maharshis. It is the only "
    "reason given against either."
)

#: **Finding.** §32.1 concedes its opponent's results before rejecting the
#: method: "due to divine powers and God-given intuition, one can be
#: successful in one's predictions only using D-1, **but that is clearly
#: unscientific**." The objection is to the method's reproducibility and not
#: to its outcomes — the only place in the book that separates the two.
THE_SECTION_GRANTS_THE_RESULTS_AND_REJECTS_THE_METHOD = (
    "The section allows that a D-1-only astrologer can be successful and "
    "still calls the method unscientific. It objects to reproducibility, not "
    "to outcome."
)

#: **Finding, and it is the fourth cause that matters to us.** Three of
#: §32.1's four causes of birthtime error are about the clock or the person
#: reading it, and nothing downstream can detect them. The fourth — "using the
#: wrong definition of 'birth'" — is a **definitional** error, and it is the
#: only one an API can be built to be explicit about. §32.1 raises it and does
#: not say here what the right definition is.
ONLY_THE_FOURTH_CAUSE_IS_OURS_TO_ANSWER = (
    "Three of the four causes are instrument, recording and memory errors "
    "that no calculation can see. The fourth is the definition of birth, and "
    "section 32.1 names it without defining it."
)
