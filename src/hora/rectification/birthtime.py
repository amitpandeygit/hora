"""Chapter 32, §32.1 — why an accurate birthtime is a precondition.

The chapter's argument is that the fast-moving points — divisional lagnas and
the special lagnas of chapter 5 — are what separate two nativities minutes
apart, so a birthtime in error by minutes is a different nativity, not an
approximation of the right one.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import cast

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
# §32.1 continued — what rectification is, and which methods survive
# --------------------------------------------------------------------------

#: §32.1's definition of rectification and its description of the quantum
#: family, verbatim. The emphasis on the term is the book's.
RECTIFICATION_DEFINED = (
    "**Birthtime rectification** is the process of correcting the reported "
    "birthtime before proceeding to make predictions based on the birthtime. "
    "There are some formulas in literature for birthtime rectification, but "
    "these assume that human births happen in certain quanta. For example, an "
    "approach may assume that nobody is born during a period of 3 minutes and "
    "people can be born in a period of half a minute then. Then again, nobody "
    "is born for 3 minutes and people can be born in a period of half a "
    "minute following it. Like this, time is divided into certain quanta in "
    "which people can be born. Then we find the nearest \"human birth can "
    "happen now\" quantum from the reported birthtime and use it as the "
    "rectified (corrected) birthtime.")

#: §32.1's verdict on the three methods it calls reasonable, verbatim.
THE_THREE_REASONABLE_METHODS = (
    "Out of these methods, some of the reasonable methods are the ones based "
    "on (a) Tattva siddhaanta, (b) Pranapada lagna in navamsa, and, (c) "
    "Kunda. The first method beyond the scope of this book and the other two "
    "fail the acid test of twins. If we were to apply those methods to the "
    "charts of twins born 2 minutes apart, the rectified birthtimes of the "
    "two twins would be either the same or too far apart.")

#: **Gap.** The acid test has two halves and only one of them is decidable.
#: "The same" is exact. "Too far apart" is not — §32.1 gives no threshold, and
#: nothing in the chapter so far supplies one. `acid_test_of_twins` therefore
#: returns `passes: None` with this as the reason unless a caller states a
#: tolerance of its own.
THE_ACID_TEST_GIVES_NO_THRESHOLD = (
    "Section 32.1 says a failing method returns the twins either at the same "
    "time or too far apart, and never says how far is too far. Only the "
    "collapse to one time can be judged from the section."
)

#: The three named methods, with what the section does with each.
NAMED_METHODS: tuple[dict[str, object], ...] = (
    {"label": "a", "method": "Tattva siddhaanta",
     "verdict": "beyond the scope of this book",
     "fails_the_acid_test": None, "taught_here": False},
    {"label": "b", "method": "Pranapada lagna in navamsa",
     "verdict": "fails the acid test of twins",
     "fails_the_acid_test": True, "taught_here": False},
    {"label": "c", "method": "Kunda",
     "verdict": "fails the acid test of twins",
     "fails_the_acid_test": True, "taught_here": False},
)

#: §32.1's conclusion on rectification, verbatim.
THE_ONLY_CORRECT_WAY = (
    "In essence, most of the birthtime rectification techniques described in "
    "literature do not work. The only correct way to rectify a birthtime is "
    "to find a time in the neighborhood of the reported birthtime so that we "
    "can explain the nature, credentials, attitude and aptitude of the native "
    "and the known events from the native's past. This is a laborious "
    "process, but there is no other way.")

#: The five things a rectified birthtime has to explain, in §32.1's order.
WHAT_A_RECTIFIED_TIME_MUST_EXPLAIN: tuple[str, ...] = (
    "the nature of the native",
    "the credentials of the native",
    "the attitude of the native",
    "the aptitude of the native",
    "the known events from the native's past",
)

#: §32.1's worked procedure, verbatim.
THE_SCAN_OVER_THE_REPORTED_RANGE = (
    "Suppose we are told that one was born between 9:02 and 9:08 am and "
    "suppose we are looking at his chart. Because we don't know the exact "
    "birthtime, we can look at a range. If we do that, we are potentially "
    "looking at thousands of people born during that time. Our native could "
    "be anyone among thousands of people born in that range.\n\n"
    "But all those thousands of people have significant differences. We want "
    "to identify our native among those thousands of people and the only way "
    "is to look at the known past. That's the only thing that distinguishes "
    "him from others born closely.\n\n"
    "So we should look at 9:02, 9:03, 9:04 etc and see which one explains the "
    "known past better. The rectified birthtime is the birthtime with which "
    "the known life events of the native make sense.")

#: The quantum example §32.1 describes: three minutes in which nobody is born,
#: then half a minute in which they can be.
QUANTUM_CLOSED_MINUTES = 3.0
QUANTUM_OPEN_MINUTES = 0.5
QUANTUM_CYCLE_MINUTES = QUANTUM_CLOSED_MINUTES + QUANTUM_OPEN_MINUTES


def nearest_quantum(reported_minutes: float, *,
                    closed_minutes: float = QUANTUM_CLOSED_MINUTES,
                    open_minutes: float = QUANTUM_OPEN_MINUTES,
                    epoch_minutes: float = 0.0) -> float:
    """§32.1's quantum family: snap a reported time to the nearest open window.

    The section describes the family and not one member of it, so the window
    lengths are parameters and the numbers it gives are the defaults. The
    **epoch** — where the first window sits — is not given by the section at
    all; see `THE_QUANTUM_FAMILY_HAS_NO_STATED_EPOCH`. Nothing about the acid
    test depends on it.

    :param reported_minutes: the reported birthtime, in minutes from any fixed
        origin.
    :param closed_minutes: the stretch in which nobody is born.
    :param open_minutes: the stretch in which they can be.
    :param epoch_minutes: where the first open window begins.
    :returns: the centre of the nearest open window.
    :raises BirthtimeError: if either stretch is not positive.
    """
    shut = validate.finite("closed_minutes", float(closed_minutes))
    ajar = validate.finite("open_minutes", float(open_minutes))
    if shut <= 0 or ajar <= 0:
        raise BirthtimeError(
            "closed_minutes and open_minutes must both be positive; got "
            f"{closed_minutes} and {open_minutes}")
    reported = validate.finite("reported_minutes", float(reported_minutes))
    epoch = validate.finite("epoch_minutes", float(epoch_minutes))

    cycle = shut + ajar
    centre = epoch + ajar / 2.0
    index = round((reported - centre) / cycle)
    return centre + index * cycle


def acid_test_of_twins(rectify: Callable[[float], float],
                       first_birth_minutes: float, *,
                       gap_minutes: float = 2.0,
                       tolerance_minutes: float | None = None) -> dict:
    """§32.1's acid test, applied to one rectification method at one instant.

    "If we were to apply those methods to the charts of twins born 2 minutes
    apart, the rectified birthtimes of the two twins would be either the same
    or too far apart."

    The first half of that is exact and needs nothing: either the two
    rectified times are one time or they are not. The second half is not —
    **§32.1 never says how far is too far** — so `passes` is left *undecided*,
    with a reason, unless the caller supplies `tolerance_minutes`. What is
    always decided is `preserves_the_gap`: whether the method returns the twins
    as far apart as they really were.

    :param rectify: a rectification, minutes in and minutes out.
    :param first_birth_minutes: when the first twin was born.
    :param gap_minutes: how far apart the twins really were born.
    :param tolerance_minutes: how far off the rectified gap may be and still
        pass. `None` leaves the verdict undecided.
    :raises BirthtimeError: if the gap or the tolerance is not positive.
    """
    gap = validate.finite("gap_minutes", float(gap_minutes))
    if gap <= 0:
        raise BirthtimeError(f"gap_minutes must be positive; got {gap_minutes}")
    first = validate.finite("first_birth_minutes", float(first_birth_minutes))
    slack = None
    if tolerance_minutes is not None:
        slack = validate.finite("tolerance_minutes", float(tolerance_minutes))
        if slack < 0:
            raise BirthtimeError(
                f"tolerance_minutes must not be negative; got {slack}")

    one, two = float(rectify(first)), float(rectify(first + gap))
    rectified_gap = two - one
    error = rectified_gap - gap
    collapsed = abs(rectified_gap) < 1e-9
    preserved = abs(error) < 1e-9

    passes: bool | None
    reason: str | None
    if collapsed:
        passes, reason = False, "the two twins rectify to one time"
    elif slack is None:
        passes, reason = None, THE_ACID_TEST_GIVES_NO_THRESHOLD
    else:
        passes = abs(error) <= slack
        reason = None if passes else (
            f"the rectified gap is off by {error:.4g} minutes, more than the "
            f"{slack:.4g} allowed")

    return {
        "true_gap_minutes": gap,
        "rectified_gap_minutes": rectified_gap,
        "collapsed_to_one_time": collapsed,
        "preserves_the_gap": preserved,
        "error_minutes": error,
        "tolerance_minutes": slack,
        "passes": passes,
        "reason": reason,
        "rule": THE_THREE_REASONABLE_METHODS,
    }


def scan_over_range(low_minutes: float, high_minutes: float, *,
                    step_minutes: float = 1.0) -> tuple[float, ...]:
    """§32.1's procedure: "look at 9:02, 9:03, 9:04 etc".

    The section says which times to try and leaves what to do with each of
    them to the astrologer — the candidates must explain the known past. This
    returns the candidates and judges none of them.

    :raises BirthtimeError: if the range is empty or the step is not positive.
    """
    low = validate.finite("low_minutes", float(low_minutes))
    high = validate.finite("high_minutes", float(high_minutes))
    step = validate.finite("step_minutes", float(step_minutes))
    if high < low:
        raise BirthtimeError(
            f"high_minutes must not precede low_minutes; got {low} and {high}")
    if step <= 0:
        raise BirthtimeError(f"step_minutes must be positive; got {step}")

    out: list[float] = []
    count = int((high - low) / step) + 1
    for index in range(count):
        candidate = low + index * step
        if candidate <= high + 1e-9:
            out.append(candidate)
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

#: **Finding, and the section's own example proves more than it claims.**
#: §32.1 levels the acid test at Pranapada lagna and Kunda. Run it on the
#: quantum family it had just described — three minutes shut, half a minute
#: open — and that fails too, structurally. Over a whole cycle, twins born
#: **2 minutes apart** come out with the **same** rectified time 42.9% of the
#: time and **3.5 minutes apart** the other 57.1%. Never 2 minutes. Never
#: anything in between.
#:
#: It is not a contingent failing. A quantum method returns window centres, so
#: the gap between any two rectified times is always a whole number of cycles;
#: the true gap survives only when it happens to be a multiple of the cycle.
#: "Either the same or too far apart" is the only thing such a method can
#: produce, whatever its numbers and wherever its windows sit.
THE_QUANTUM_FAMILY_FAILS_THE_ACID_TEST_BY_CONSTRUCTION = (
    "Twins two minutes apart come out of the section's own quantum example "
    "with the same time 42.9% of the time and 3.5 minutes apart the rest. A "
    "quantum method can only ever return a whole number of cycles, so it "
    "cannot return two minutes at all."
)

#: **Gap in the section, and it does not matter.** A quantum scheme needs
#: three numbers: how long the shut stretch is, how long the open one is, and
#: **where the first window sits**. §32.1 gives the first two and never the
#: third. Without an epoch the "nearest quantum" is not defined, so the family
#: as described cannot be implemented from the section alone.
#:
#: `nearest_quantum` therefore takes `epoch_minutes` and defaults it to zero,
#: with no claim that zero is the book's. Nothing turns on it: the acid test
#: fails for every epoch, because shifting the windows shifts both twins.
THE_QUANTUM_FAMILY_HAS_NO_STATED_EPOCH = (
    "Section 32.1 gives the quantum lengths and never says where the windows "
    "begin, so the method it describes cannot be run from the section alone. "
    "The acid test fails at every epoch, so nothing here depends on it."
)

#: **Finding.** The acid test is a **criterion**, not a technique — the first
#: thing in the book that judges methods rather than charts. §32.1 applies it
#: to two named methods and reports the outcome without working either, and
#: neither Pranapada lagna nor Kunda is taught anywhere in the book. So the
#: verdict cannot be reproduced from the book: `acid_test_of_twins` is built
#: and there is nothing here to run it on but the quantum example.
THE_ACID_TEST_IS_STATED_ON_METHODS_THE_BOOK_NEVER_TEACHES = (
    "Pranapada lagna in navamsa and Kunda are failed by the acid test and "
    "neither is taught in the book, so the verdict cannot be checked. The "
    "criterion itself is built and the quantum example is the only method "
    "available to run it on."
)

#: **Finding.** The section rejects every formula and puts a **person** in
#: their place. What the rectified time must explain is five things —
#: "the nature, credentials, attitude and aptitude of the native and the known
#: events from the native's past" — and four of the five are judgements about
#: a life, not events with dates. Only the fifth is data. "This is a laborious
#: process, but there is no other way" is the section conceding that it has
#: named no procedure that can be automated.
THE_ONLY_ACCEPTED_METHOD_IS_THE_ONE_THAT_CANNOT_BE_AUTOMATED = (
    "Four of the five things a rectified birthtime must explain are "
    "judgements about a native and the fifth is the dated past. The section "
    "calls the process laborious and offers no alternative."
)

#: **Finding.** §32.1's own scan is coarser than §32.1's own argument. It says
#: to try "9:02, 9:03, 9:04 etc" over a six-minute range, which is seven
#: candidates a minute apart — while the paragraphs above it argue that a
#: **two-minute** error already makes a different native. A one-minute grid
#: leaves each candidate standing for a spread the section has just called
#: significant. The section states the principle and demonstrates it at half
#: the resolution the principle asks for.
THE_SCAN_STEP_IS_COARSER_THAN_THE_ARGUMENT = (
    "The section argues that two minutes changes the native and then scans a "
    "six-minute range one minute at a time. Seven candidates cover a range "
    "the same section says holds thousands of different people."
)


# --------------------------------------------------------------------------
# §32.2 Robustness of Computations — §32.2.1 Divisional Charts
# --------------------------------------------------------------------------

SECTION_32_2_TITLE = "Robustness of Computations"
SECTION_32_2_1_TITLE = "Divisional Charts"

#: §32.2's opening, verbatim. The emphasis on "approximate" is the book's, and
#: it governs every figure in the section.
ROBUSTNESS_IS_APPROXIMATE = (
    "When we try different birthtimes, all the computations change. If we "
    "know how various computations are altered based on small changes in the "
    "birthtime, we can approach the problem of birthtime rectification "
    "intelligently. We will discuss the **approximate** impact of birthtime "
    "change on various computations.")

#: §32.2.1's paragraph on the grahas, verbatim.
PLANETS_CHANGE_VERY_SLOWLY = (
    "Positions of planets in rasi chart and divisional charts change very "
    "slowly. For example, Sun stays in one rasi for 30 days. He changes rasi "
    "in D-10 once in 30/10=3 days. He changes rasi in D-24 once in every "
    "30/24=1.25 days. The speed of Mercury, Venus and Mars is comparable to "
    "Sun's. Jupiter and Saturn are even slower. Moon is faster than all these "
    "planets. He stays in one rasi for 2.5 days or 60 hours. He changes rasi "
    "in D-10 once in 60/10=6 hours. He changes rasi in D-24 once in every "
    "60/24=2.5 hours.")

#: §32.2.1's worked border case, verbatim.
THE_MOON_AT_A_DASAMSA_BORDER = (
    "If the uncertainty in birthtime is of the order of 5 minutes or 10 "
    "minutes, one may think that there is no problem with these planets as "
    "they stay in the same rasi in all divisional charts for a lot longer "
    "time than 5-10 minutes. However, if a planet is at a border and changes "
    "rasi in a divisional chart during those 5 minutes, we have to take that "
    "into consideration. Suppose Moon is is at 23Sc59. Suppose That places "
    "him in the 8th dasamsa of Sc, i.e. Aq. Suppose lagna in D-10 is Cn. So "
    "D-10 has lagna lord in 8th. This makes the D-10 chart weak. On the other "
    "hand, it Moon is at 24Sc00 or above, he will be in the 9th dasamsa of "
    "Sc, i.e. Pi. This puts lagna lord in 9th in D-10 and the chart is "
    "strengthened. Because Moon moves by one quarter of a nakshatra (or 200 "
    "arc-min) in 6 hours (or 360 min), he takes 360/200=1.8 min to move by 1 "
    "arc-min. For Moon to go from 23Sc59 to 24Sc00, it only takes about 2 "
    "minutes. If we cannot rule out an error of 2 minutes, we should consider "
    "Moon in both Aq and Pi and see which one explains the native's career "
    "better.")

#: §32.2.1's rule for the grahas, verbatim.
CONSIDER_BOTH_SIDES_OF_A_BORDER = (
    "Thus, we should pay attention if any planet is at a rasi border in the "
    "divisional chart of interest. If so, we must consider both the positions "
    "and see which one makes better sense based on known past.")

#: Footnote 90, verbatim. It hangs off "it only takes about 2 minutes".
FOOTNOTE_90 = (
    "We are assuming here that our computation of Moon's longitude is very "
    "accurate. There are some unresolved controversies like (1) ayanamsa and "
    "(2) geocentric positions vs topocentric positions. Due to these "
    "controversies, we cannot be confident of our calculations. It is prudent "
    "to consider both the rasis in border-line situations.")

#: The two controversies footnote 90 names, and where each already lives in
#: our settings. **Neither default is proposed for change here.**
FOOTNOTE_90_CONTROVERSIES: tuple[dict[str, object], ...] = (
    {"number": 1, "controversy": "ayanamsa",
     "our_setting": "Settings.ayanamsa", "our_default": "lahiri"},
    {"number": 2,
     "controversy": "geocentric positions vs topocentric positions",
     "our_setting": "Settings.topocentric", "our_default": "geocentric"},
)

#: §32.2.1's paragraphs on the lagna, verbatim.
LAGNA_IS_THE_MOST_IMPORTANT_CONSIDERATION = (
    "Lagna changes rasi in divisional charts much faster than planets. So it "
    "is the most important consideration in birthtime rectification.")

LAGNA_MOVES_ONE_DEGREE_IN_FOUR_MINUTES = (
    "Lagna moves by one rasi (30 degrees) in 2 hours or 120 min. To move by "
    "1 degree, lagna takes about 4 min.")

#: The boxed Lesson, verbatim.
LESSON = (
    "Lagna moves by 1 degree in 4 min. Lagna moves by 10' in 2/3 min (or 40 "
    "seconds). Lagna moves by 1' in 4 sec. Lagna moves by 10\" in 2/3 sec.")

#: The Lesson as data: how much lagna moves, and how long it takes.
LESSON_ROWS: tuple[dict[str, object], ...] = (
    {"arc_arcseconds": 3600.0, "seconds": 240.0, "as_printed": "1 degree in 4 min"},
    {"arc_arcseconds": 600.0, "seconds": 40.0, "as_printed": "10' in 2/3 min"},
    {"arc_arcseconds": 60.0, "seconds": 4.0, "as_printed": "1' in 4 sec"},
    {"arc_arcseconds": 10.0, "seconds": 2.0 / 3.0, "as_printed": "10\" in 2/3 sec"},
)

#: §32.2.1's closing line on the lagna, verbatim.
LAGNA_CHANGES_RASI_IN_D10_IN_TWELVE_MINUTES = (
    "We can see that lagna changes rasi in D-10 in 12 min. It changes rasi in "
    "D-24 in 5 min.")

#: The section's own figures, as data, so each can be checked on its own.
ROBUSTNESS_FIGURES: tuple[dict[str, object], ...] = (
    {"body": "Sun", "rasi_interval_minutes": 30 * 24 * 60.0, "varga": 1},
    {"body": "Sun", "rasi_interval_minutes": 3 * 24 * 60.0, "varga": 10},
    {"body": "Sun", "rasi_interval_minutes": 1.25 * 24 * 60.0, "varga": 24},
    {"body": "Moon", "rasi_interval_minutes": 60 * 60.0, "varga": 1},
    {"body": "Moon", "rasi_interval_minutes": 6 * 60.0, "varga": 10},
    {"body": "Moon", "rasi_interval_minutes": 2.5 * 60.0, "varga": 24},
    {"body": "lagna", "rasi_interval_minutes": 120.0, "varga": 1},
    {"body": "lagna", "rasi_interval_minutes": 12.0, "varga": 10},
    {"body": "lagna", "rasi_interval_minutes": 5.0, "varga": 24},
)

#: The one varga whose amsas are not equal, and so the one the section's
#: divide-by-N rule does not describe. §9's trimsamsa runs 5, 5, 8, 7, 5
#: degrees in an odd rasi and 5, 7, 8, 5, 5 in an even one.
UNEQUAL_VARGAS: tuple[int, ...] = (30,)


def varga_rasi_change_interval(rasi_interval: float, varga: int) -> dict:
    """§32.2.1's rule: a body changes rasi in D-N once in (its rasi time)/N.

    "Sun stays in one rasi for 30 days. He changes rasi in D-10 once in
    30/10=3 days."

    The rule holds because a varga cuts the 30-degree rasi into N equal parts
    — for every varga the book teaches **except D-30**, whose five parts are
    unequal. For D-30 the interval is returned as a **range**, and
    `equal_parts` says which case you are in.

    :param rasi_interval: how long the body takes to cross one whole rasi, in
        any unit; the answer comes back in the same unit.
    :param varga: the divisional chart's number.
    :raises BirthtimeError: on a non-positive interval or varga.
    """
    span = validate.finite("rasi_interval", float(rasi_interval))
    if span <= 0:
        raise BirthtimeError(
            f"rasi_interval must be positive; got {rasi_interval}")
    number = validate.in_range("varga", int(varga), 1, 300)

    equal = number not in UNEQUAL_VARGAS
    if equal:
        interval = span / number
        return {"varga": number, "equal_parts": True,
                "interval": interval, "shortest": interval,
                "longest": interval, "rule": PLANETS_CHANGE_VERY_SLOWLY}
    # D-30: 5, 5, 8, 7, 5 degrees out of 30.
    parts = (5.0, 5.0, 8.0, 7.0, 5.0)
    return {"varga": number, "equal_parts": False, "interval": None,
            "shortest": span * min(parts) / 30.0,
            "longest": span * max(parts) / 30.0,
            "rule": PLANETS_CHANGE_VERY_SLOWLY}


def signs_across_the_uncertainty(longitude: float,
                                 varga: Callable[[float], object], *,
                                 arcminutes: float,
                                 samples: int = 2001) -> tuple[int, ...]:
    """Every varga sign a body could be in, given an uncertainty either side.

    §32.2.1: "we should pay attention if any planet is at a rasi border in the
    divisional chart of interest. If so, we must consider both the positions."
    This answers *which* positions. One sign back means the body is not at a
    border; two or more mean it is.

    The window is sampled rather than solved, at `samples` points, so a window
    far wider than the varga's own amsa needs more samples than the default.

    :param longitude: the body's computed longitude.
    :param varga: a varga function returning an object with a ``sign``.
    :param arcminutes: the uncertainty either side of that longitude.
    :raises BirthtimeError: if the uncertainty is negative or samples < 2.
    """
    centre = validate.longitude("longitude", float(longitude))
    slack = validate.finite("arcminutes", float(arcminutes))
    if slack < 0:
        raise BirthtimeError(f"arcminutes must not be negative; got {slack}")
    if int(samples) < 2:
        raise BirthtimeError(f"samples must be at least 2; got {samples}")

    width = slack / 60.0
    low = centre - width
    step = (2 * width) / (int(samples) - 1) if width else 0.0
    seen: list[int] = []
    for index in range(int(samples) if width else 1):
        point = (low + index * step) % 360.0
        sign = int(varga(point).sign)  # type: ignore[attr-defined]
        if sign not in seen:
            seen.append(sign)
    return tuple(seen)

#: **Finding.** The section's rule — a body changes rasi in D-N once in its
#: rasi time divided by N — is exact for **twenty-two of the twenty-three**
#: vargas the book teaches, because every one of them cuts the rasi into N
#: equal parts. **D-30 is the exception.** §9's trimsamsa runs 5, 5, 8, 7, 5
#: degrees in an odd rasi and 5, 7, 8, 5, 5 in an even one, so the lagna's
#: D-30 sign holds for **20 to 32 minutes**, not the 4 the rule gives — five
#: to eight times longer. The error is in the safe direction: D-30 is steadier
#: under a birthtime error than the rule claims, not shakier.
#:
#: `varga_rasi_change_interval` returns a range and `equal_parts: False` for
#: D-30 rather than a figure the rule cannot support.
THE_DIVIDE_BY_N_RULE_HAS_ONE_EXCEPTION = (
    "The rule is exact for every varga that cuts the rasi into equal parts, "
    "which is all of them but D-30. Trimsamsa's parts are 5, 5, 8, 7 and 5 "
    "degrees, so the lagna's D-30 sign lasts 20 to 32 minutes and not 4."
)

#: **Finding, measured.** Every figure the section prints is a **mean**, and
#: the section says so in its own first paragraph by bolding "approximate".
#: Measured against the ephemeris over one year from 2000:
#:
#: * The **Sun**'s rasi takes 29.4 to 31.4 days, mean **30.4**. The section's
#:   30 days is good to two per cent.
#: * The **Moon**'s rasi takes 47.5 to 61.2 hours, mean **54.7**. The
#:   section's "2.5 days or 60 hours" is not the mean but close to the
#:   **maximum**, and it is about ten per cent high.
#: * The **lagna**'s rasi is the two hours of §32.1, whose mean is 119.7
#:   minutes and whose spread runs 67 to 155 minutes at 42 N 30.
THE_SECTIONS_FIGURES_ARE_MEANS_AND_IT_SAYS_SO = (
    "The Sun's rasi runs 29.4 to 31.4 days against the section's 30, the "
    "Moon's runs 47.5 to 61.2 hours against its 60, and the lagna's is "
    "section 32.1's two hours. The section bolds \"approximate\" in its own "
    "first sentence."
)

#: **Finding, and the two numbers disagree by ten per cent.** The Moon
#: paragraph carries **two** speeds and derives its answer from the better
#: one. "He stays in one rasi for 2.5 days or 60 hours" makes the Moon cover
#: 1800 arcminutes in 3600 minutes — **2.0 minutes per arcminute**, and 200
#: arcminutes in 6 hours 40. Two sentences later: "Moon moves by one quarter
#: of a nakshatra (or 200 arc-min) in 6 hours (or 360 min), he takes
#: 360/200=1.8 min to move by 1 arc-min" — **1.8 minutes per arcminute**, and
#: 200 arcminutes in 6 hours flat.
#:
#: The measured mean is **1.82 minutes per arcminute**. So the figure the
#: section actually computes with is right to one per cent and the 60-hour
#: rasi it stated first is the loose one. Nothing downstream moves: the
#: conclusion is "about 2 minutes" and the truth is 1.82.
THE_MOON_PARAGRAPH_CARRIES_TWO_SPEEDS = (
    "Sixty hours a rasi gives 2.0 minutes per arcminute; the quarter-"
    "nakshatra sentence gives 1.8; the measured mean is 1.82. The section "
    "derives its answer from the accurate one."
)

#: **Finding.** The worked border reproduces exactly. 23 Sc 59 falls in the
#: **8th** dasamsa of Scorpio, which is Aquarius, and 24 Sc 00 falls in the
#: **9th**, which is Pisces — both as printed. Scorpio's dasamsas are three
#: degrees each and, Scorpio being an even rasi, they are counted from the 9th
#: from it; the 8th and 9th land on Aq and Pi. The lagna-lord argument follows:
#: with D-10 lagna in Cancer the lord is the Moon, so one arcminute of the
#: Moon moves the lagna lord from the 8th house to the 9th.
THE_DASAMSA_BORDER_REPRODUCES = (
    "23 Sc 59 gives the 8th dasamsa, Aquarius, and 24 Sc 00 gives the 9th, "
    "Pisces. With D-10 lagna in Cancer the lord is the Moon himself, so one "
    "arcminute moves him from the 8th house to the 9th."
)

#: **Finding, and it is the chapter's own thesis restated as a number.** The
#: section says the lagna is "the most important consideration in birthtime
#: rectification", and its own figures say why: in the two minutes §32.1 calls
#: a different native, the **lagna moves 30 arcminutes and the Moon moves
#: one**. Thirty to one is the whole reason a rectification watches the lagna
#: and not the grahas — and the Moon is the fastest graha there is.
THE_LAGNA_OUTRUNS_THE_FASTEST_GRAHA_THIRTY_TO_ONE = (
    "In two minutes the lagna moves 30 arcminutes and the Moon moves 1.1. "
    "The section calls the lagna the most important consideration and its own "
    "figures give the ratio."
)

#: **Finding.** The boxed Lesson is four statements of one rate and they agree
#: to the last digit: 3600 arcseconds in 240 seconds, 600 in 40, 60 in 4, 10
#: in 2/3 — **fifteen arcseconds of lagna per second of clock** every time. It
#: is the only boxed lesson in the book that is pure arithmetic, and the only
#: place the book gives a rate to the arcsecond.
THE_LESSON_IS_ONE_RATE_STATED_FOUR_WAYS = (
    "All four rows of the Lesson are 15 arcseconds of lagna per second of "
    "clock. It is the only boxed lesson in the book that is arithmetic alone."
)

#: **Finding, measured, and it dwarfs the section it annotates.** Footnote 90
#: says the two controversies leave us unable to be confident of a Moon
#: longitude. Measured on Chart 1, in the Moon:
#:
#: * **Lahiri, Lahiri ICRC, Krishnamurti and True Citra** — the family our own
#:   default sits in — span **5.8 arcminutes**.
#: * Add **Raman, Yukteshwar and Fagan-Bradley** and the span is **139.8
#:   arcminutes**, two and a third degrees.
#: * **Geocentric against topocentric** moves the Moon by up to **55
#:   arcminutes** over thirty days at 42 N 30, and by 0.1 arcminutes or less
#:   for every other graha — parallax is a Moon problem alone.
#:
#: The border §32.2.1 works turns on **one** arcminute. At the section's own
#: 1.82 minutes per arcminute those spreads are worth 11 minutes, 254 minutes
#: and 100 minutes of birthtime. The footnote is not a hedge: the ephemeris
#: question is one to two orders of magnitude larger than the birthtime
#: question the section is about.
THE_TWO_CONTROVERSIES_DWARF_THE_BORDER_THEY_ANNOTATE = (
    "The Lahiri family spans 5.8 arcminutes in the Moon, all six mainstream "
    "ayanamsas span 139.8, and geocentric against topocentric reaches 55. "
    "Section 32.2.1's worked border turns on one arcminute."
)

#: **Finding.** Footnote 90 widens the rule above it. §32.2.1 said to consider
#: both rasis when a **birthtime** error could carry a graha over a border;
#: the footnote says to do it when the **ephemeris** could. Same instruction,
#: a second and much larger reason. `signs_across_the_uncertainty` takes an
#: uncertainty in arcminutes and does not care where it came from, so it
#: answers both — but nothing in the API yet supplies the ephemeris figure.
#: See OI-182.
THE_FOOTNOTE_WIDENS_THE_RULE_FROM_TIME_TO_POSITION = (
    "Section 32.2.1 hedges against a birthtime error and footnote 90 hedges "
    "against the ephemeris. The rule is the same, consider both rasis, and "
    "the second reason is the larger one."
)

#: **Finding.** D-69 is footnote 90's own case, recorded eight chapters early
#: and before there was a rule to hang it on. Charts 37 and 49 are one
#: nativity printed twice, and the uniform 1.5 arcminutes of ayanamsa between
#: them moved **Venus and GL a whole sign in D-20**. That is exactly the
#: footnote's warning happening inside the book's own pages.
D69_IS_THE_FOOTNOTES_OWN_CASE = (
    "Charts 37 and 49 differ by about 1.5 arcminutes of ayanamsa and that "
    "moves Venus and GL a whole sign in D-20. Footnote 90 states the general "
    "case; D-69 is the instance."
)

#: **Finding.** Both controversies are already settings and neither default
#: moves: `Settings.ayanamsa` offers sixteen with **Lahiri** as ours, and
#: `Settings.topocentric` defaults to **geocentric**. The footnote gives no
#: preference between the options — it says only that the disagreement exists
#: and that a border should therefore be read both ways.
THE_FOOTNOTE_NAMES_NO_WINNER = (
    "Footnote 90 says the ayanamsa and the geocentric-topocentric questions "
    "are unresolved and does not choose. Our defaults are Lahiri and "
    "geocentric and nothing here proposes changing either."
)


# --------------------------------------------------------------------------
# §32.2.1 continued — Special Lagnas, and the second boxed Lesson
# --------------------------------------------------------------------------

#: §32.2.1's paragraph on the special lagnas, verbatim.
SPECIAL_LAGNAS_ARE_FASTER_STILL = (
    "Hora lagna moves twice as fast as lagna. Ghati lagna moves 5 times as "
    "fast as lagna.")

#: The second boxed Lesson, verbatim. It runs across a page break.
LESSON_SPECIAL_LAGNAS = (
    "HL moves by 1 degree in 2 min. HL moves by 10' in 1/3 min (or 20 "
    "seconds). HL moves by 1' in 2 sec. HL moves by 10\" in 1/3 sec.\n\n"
    "GL moves by 1 degree in 4/5 min (or 48 seconds). GL moves by 10' in 4.8 "
    "seconds. GL moves by 1' in 0.48 sec (less than half a second).")

#: The second Lesson as data, each row as printed against what the row's own
#: opening line implies. See D-85 for the two GL rows that disagree.
LESSON_SPECIAL_LAGNA_ROWS: tuple[dict[str, object], ...] = (
    {"lagna": "HL", "arc_arcseconds": 3600.0, "printed_seconds": 120.0,
     "as_printed": "1 degree in 2 min"},
    {"lagna": "HL", "arc_arcseconds": 600.0, "printed_seconds": 20.0,
     "as_printed": "10' in 1/3 min"},
    {"lagna": "HL", "arc_arcseconds": 60.0, "printed_seconds": 2.0,
     "as_printed": "1' in 2 sec"},
    {"lagna": "HL", "arc_arcseconds": 10.0, "printed_seconds": 1.0 / 3.0,
     "as_printed": "10\" in 1/3 sec"},
    {"lagna": "GL", "arc_arcseconds": 3600.0, "printed_seconds": 48.0,
     "as_printed": "1 degree in 4/5 min"},
    {"lagna": "GL", "arc_arcseconds": 600.0, "printed_seconds": 4.8,
     "as_printed": "10' in 4.8 seconds"},
    {"lagna": "GL", "arc_arcseconds": 60.0, "printed_seconds": 0.48,
     "as_printed": "1' in 0.48 sec"},
)

#: **Finding, and it inverts Example 129's caveat.** The lagna's four minutes
#: a degree is a mean, and Example 129 withdrew it. HL's two minutes and GL's
#: forty-eight seconds are **not means**: §5.5 defines both as a uniform
#: advance from the Sun's position at sunrise — 0.5 and 1.25 degrees a minute —
#: so `ADVANCE_PER_MINUTE` carries those exact figures and the Lesson's HL
#: rows are true to the arcsecond at every latitude and every hour. Where the
#: rectifier can least trust the ascendant, it can most trust these two.
THE_SPECIAL_LAGNA_RATES_ARE_EXACT_AND_THE_LAGNAS_IS_NOT = (
    "Hora lagna and Ghati lagna advance 0.5 and 1.25 degrees a minute by "
    "definition, so their rates are exact where the ascendant's four minutes "
    "a degree is only a mean."
)

#: **Finding, measured.** "Twice as fast" and "5 times as fast" are ratios to
#: the **nominal** lagna, and they are exact there — 0.5 and 1.25 against
#: 0.25 degrees a minute. Against the real ascendant they drift with latitude:
#:
#: | place | ascendant | HL / lagna | GL / lagna |
#: |---|---|---|---|
#: | the equator | 13.8'-16.4'/min | 1.83-2.17 | 4.57-5.43 |
#: | 16 N 15 | 13.5'-18.8' | 1.60-2.23 | 4.00-5.57 |
#: | 42 N 30 | 11.6'-27.2' | 1.10-2.59 | 2.76-6.48 |
#: | 60 N | 9.2'-65.7' | 0.46-3.27 | 1.14-8.17 |
#:
#: At 60 N there are hours when the ascendant outruns Hora Lagna outright, and
#: hours when it nearly matches Ghati Lagna. The ordering the sentence asserts
#: is a property of the mean, not of the sky.
THE_TWO_RATIOS_HOLD_ONLY_AGAINST_THE_MEAN_LAGNA = (
    "Twice and five times are exact against the nominal quarter-degree a "
    "minute. Against the real ascendant they run 1.10 to 2.59 and 2.76 to "
    "6.48 at 42 N 30, and at 60 N the ascendant sometimes outruns Hora Lagna."
)

#: **Finding, and it explains an omission.** The section gives rates for HL
#: and GL and none for **Bhava Lagna**, which §5.5 taught alongside them. The
#: reason is arithmetic: BL advances **0.25 degrees a minute**, which is the
#: ascendant's own nominal rate exactly, so a BL row would repeat §32.2.1's
#: first Lesson word for word. **Sree Lagna** is left out for the opposite
#: reason — it moves with the Moon as well as the clock and so has no fixed
#: rate to print.
BHAVA_LAGNA_IS_OMITTED_BECAUSE_ITS_ROW_WOULD_REPEAT_THE_LAGNAS = (
    "Bhava Lagna advances a quarter degree a minute, which is the nominal "
    "ascendant rate, so its Lesson row would be the first Lesson again. Sree "
    "Lagna has no fixed rate at all."
)


# --------------------------------------------------------------------------
# Example 129 — a rectification worked from the varga borders alone
# --------------------------------------------------------------------------

#: Example 129, verbatim.
EXAMPLE_129 = (
    "Suppose we are told that someone was born at 9:05 am. Suppose lagna is "
    "at 4Sg39. Suppose we have events related to D-10 (career), D-12 "
    "(parents) and D-24 (education). Lagna at 4Sg39 puts lagna in these 3 "
    "charts in Cp, Cp and Sc (respectively). Suppose the birthtime is "
    "reasonably accurate and the maximum error is 5 minutes (i.e. birthtime "
    "can be 9:00-9:10). Let us find the possible lagnas in the 3 charts.\n\n"
    "An error of 5 min changes lagna by about 5/4=1.25 degrees or 1 deg 15'. "
    "So, instead of being 4Sg39, it can be as low as 3Sg24 or as high as "
    "5Sg54. So we should consider all lagnas between 3Sg24 and 5Sg54. In "
    "D-10, lagna changes rasi at multiples of 3 degrees. So the whole range "
    "we have for lagna results in the same D-10 lagna (Cp). In D-12, lagna "
    "changes rasi at multiples of 2 deg 30'. So we have a transition at 5 "
    "degrees. So there are two possibilities for lagna - one in 3Sg24-5Sg00 "
    "and the other in 5Sg00-5Sg54. So lagna in D-12 can be Cp or Aq. Lagna "
    "in D-24 changes rasi at multiples of 1 deg 15'. It changes rasi at 3 "
    "deg 45' and 5 deg 00'. So we have 3 possibilities for lagna - (1) "
    "3Sg24-3Sg45: Li, (2) 3Sg45-5Sg00: Sc, (3) 5Sg00-5Sg54: Sg.\n\n"
    "Using these sets of lagnas, we should analyze the charts and see which "
    "one makes sense. Suppose Sg lagna in D-24 and Aq lagna in D-12 explain "
    "known events. But suppose we cannot explain his career. Suppose Aq "
    "lagna instead of Cp lagna explains his career well. Then what do we "
    "do?\n\n"
    "To get the next rasi as D-10 lagna (Aq instead of Cp), we should cross "
    "the next D-10 border, which is 6Sg00. So the lagna should become 6Sg00 "
    "(or higher) instead of 4Sg39. So we have to add 1 deg 21' or higher to "
    "lagna. Lagna moves by 1 deg 21' or 81' in 81x4 sec = 324 sec = 5 min 24 "
    "sec.\n\n"
    "This means that the birthtime should be 9:10:24 instead of 9:05. Though "
    "we are told that the error in birthtime cannot be more than 5 minutes, "
    "it has to be more than 5 minutes in this case to explain known "
    "facts.\n\n"
    "Please note that these calculations are made on the assumption that "
    "lagna moves uniformly. That is not the case in reality. So the actual "
    "rectified birthtime may be a little off. We can do approximate "
    "calculations first and then see if it has to be corrected further. For "
    "example, we may get lagna at 9:10:24 to be 5Sg59 instead of the "
    "expected value of 6Sg00. Then we have to add a few more seconds and see "
    "if we cross 6Sg00.\n\n"
    "One may see from this example that an astrologer should know the "
    "details of the computation of divisional charts and be familiar with "
    "the longitudes at which lagna changes rasi in various divisional "
    "charts. That familiarity is a necessity for quick birthtime "
    "rectification.")

#: Everything Example 129 states, as data. Degrees are within Sagittarius.
EXAMPLE_129_STATED: dict[str, object] = {
    "reported_birthtime": "9:05 am",
    "lagna": "4 Sg 39",
    "lagna_degree_in_rasi": 4 + 39 / 60,
    "maximum_error_minutes": 5.0,
    "range": ("3 Sg 24", "5 Sg 54"),
    "range_degrees_in_rasi": (3 + 24 / 60, 5 + 54 / 60),
    "vargas": {10: "career", 12: "parents", 24: "education"},
    "lagnas_as_reported": {10: "Cp", 12: "Cp", 24: "Sc"},
    "windows": {
        10: (((3 + 24 / 60, 5 + 54 / 60), "Cp"),),
        12: (((3 + 24 / 60, 5.0), "Cp"), ((5.0, 5 + 54 / 60), "Aq")),
        24: (((3 + 24 / 60, 3 + 45 / 60), "Li"),
             ((3 + 45 / 60, 5.0), "Sc"),
             ((5.0, 5 + 54 / 60), "Sg")),
    },
    "wanted_d10_lagna": "Aq",
    "next_d10_border": 6.0,
    "shortfall_arcminutes": 81.0,
    "shift_seconds": 324.0,
    "rectified_birthtime": "9:10:24",
}


def lagna_windows(low: float, high: float, varga: Callable[[float], object],
                  *, coarse_steps: int = 4000) -> tuple[dict[str, object], ...]:
    """Example 129's own move: split a lagna range into its varga signs.

    "So we have 3 possibilities for lagna - (1) 3Sg24-3Sg45: Li, (2)
    3Sg45-5Sg00: Sc, (3) 5Sg00-5Sg54: Sg."

    Borders are found by bisection, so the ends of each window come back
    exact rather than to the scan's resolution.

    :param low: the low end of the lagna range, an absolute longitude.
    :param high: the high end.
    :param varga: a varga function returning an object with a ``sign``.
    :returns: one entry per window, in order, with its ``from``, ``to`` and
        ``sign``.
    :raises BirthtimeError: if the range is inverted or wider than a rasi.
    """
    start = validate.longitude("low", float(low))
    # `high` may run past 360 so a window can straddle the zodiac's start.
    stop = validate.finite("high", float(high))
    if stop < start:
        raise BirthtimeError(f"high must not precede low; got {low} and {high}")
    if stop - start > 30.0:
        raise BirthtimeError(
            "the range must not exceed one rasi; got "
            f"{stop - start} degrees")

    def sign_at(point: float) -> int:
        return int(varga(point % 360.0).sign)  # type: ignore[attr-defined]

    steps = max(int(coarse_steps), 2)
    step = (stop - start) / steps if stop > start else 0.0
    windows: list[dict[str, object]] = []
    window_from, current = start, sign_at(start)
    previous_point = start
    for index in range(1, steps + 1):
        point = start + index * step
        here = sign_at(point)
        if here != current:
            low_edge, high_edge = previous_point, point
            for _ in range(60):
                middle = (low_edge + high_edge) / 2.0
                if sign_at(middle) == current:
                    low_edge = middle
                else:
                    high_edge = middle
            windows.append({"from": window_from, "to": high_edge,
                            "sign": current})
            window_from, current = high_edge, here
        previous_point = point
    windows.append({"from": window_from, "to": stop, "sign": current})
    # A border landing exactly on `stop` leaves an empty last window.
    return tuple(w for w in windows
                 if cast(float, w["to"]) - cast(float, w["from"]) > 1e-9)


def seconds_to_move(arcminutes: float) -> float:
    """The Lesson's rate applied: lagna moves one arcminute in four seconds.

    Example 129: "Lagna moves by 1 deg 21' or 81' in 81x4 sec = 324 sec = 5
    min 24 sec." It is the two-hour rasi of §32.1 and so a **mean**; see
    `THE_UNIFORM_LAGNA_IS_THE_SECTIONS_OWN_CAVEAT`.
    """
    arc = validate.finite("arcminutes", float(arcminutes))
    return arc * 4.0

#: **Finding.** Every figure Example 129 prints reproduces, and none of it
#: needs a chart. 4 Sg 39 gives Cp, Cp and Sc in D-10, D-12 and D-24; five
#: minutes of error is 1°15' either side, so 3 Sg 24 to 5 Sg 54; that range
#: holds **one** D-10 sign, **two** D-12 signs split at 5°00', and **three**
#: D-24 signs split at 3°45' and 5°00' — Li, Sc and Sg. The whole example is
#: worked from the varga borders and a rate, which is what its closing
#: sentence says an astrologer should be able to do.
EXAMPLE_129_REPRODUCES_FROM_BORDERS_ALONE = (
    "One D-10 sign, two D-12 signs and three D-24 signs across the range, "
    "split exactly where the example says. No ephemeris is needed for any of "
    "it."
)

#: **Finding.** The example's rectified time **breaks its own constraint and
#: says so**: "though we are told that the error in birthtime cannot be more
#: than 5 minutes, it has to be more than 5 minutes in this case to explain
#: known facts." 9:05 plus 5 min 24 sec is 9:10:24, which is outside the
#: 9:00-9:10 the native reported. The known past outranks the reported bound —
#: §32.1's four causes of birthtime error are the reason it can.
THE_ANSWER_LEAVES_THE_REPORTED_WINDOW_AND_THE_EXAMPLE_SAYS_SO = (
    "The rectified 9:10:24 falls outside the 9:00-9:10 the native gave, and "
    "the example keeps it. The known past outranks the reported bound."
)

#: **Finding, measured, and the caveat is right in the direction it warns of.**
#: The example ends by saying its arithmetic assumes the lagna moves uniformly,
#: "that is not the case in reality", and that the rectified time "may be a
#: little off" — it guesses 5 Sg 59 where 6 Sg 00 was wanted. Put a real chart
#: under it. Taking instants where the lagna truly is 4 Sg 39 at 9:05:
#:
#: | place | lagna after 5m24s | short of 6 Sg 00 by | extra time needed |
#: |---|---|---|---|
#: | 16 N 15 | 5 Sg 55 | 5.1' | 22 sec |
#: | 42 N 30 | 5 Sg 50 | 9.7' | 42 sec |
#: | the equator | 5 Sg 55 | 5.2' | 21 sec |
#: | 60 N | 5 Sg 52 | 8.3' | 35 sec |
#:
#: Early Sagittarius rises at about **13.7 arcminutes a minute** at these
#: latitudes against the nominal 15, so the uniform figure always overshoots
#: and the true time is always **later**. The book's illustrative 5 Sg 59 is
#: optimistic — the real shortfall is five to ten arcminutes, not one — but
#: its instruction, add a few more seconds and check, is exactly right.
THE_UNIFORM_LAGNA_IS_THE_SECTIONS_OWN_CAVEAT = (
    "Measured at four latitudes, the lagna after the example's 5 min 24 sec "
    "lands 5 to 10 arcminutes short of 6 Sg 00 and needs another 21 to 42 "
    "seconds. Early Sagittarius rises at about 13.7 arcminutes a minute "
    "against the nominal 15."
)

#: **Finding, and it settles a question §32.1 left hanging.** §32.1 said the
#: lagna "changes rasi once in 2 hours" flatly; §32.2 bolded "approximate";
#: Example 129 finally says outright that "these calculations are made on the
#: assumption that lagna moves uniformly. **That is not the case in
#: reality.**" So the mean-not-a-rate finding recorded against §32.1 is the
#: book's own position, stated two sections later, and the book's remedy is to
#: iterate rather than to compute the rate properly.
THE_BOOK_STATES_THE_MEAN_IS_NOT_A_RATE = (
    "Section 32.1 gave the two hours flatly, section 32.2 called its figures "
    "approximate, and Example 129 says the uniform lagna is not the case in "
    "reality. The remedy offered is to iterate."
)

#: **Finding.** Example 129's closing sentence is a **product requirement**
#: dressed as advice: "an astrologer should know the details of the
#: computation of divisional charts and be familiar with the longitudes at
#: which lagna changes rasi in various divisional charts. That familiarity is
#: a necessity for quick birthtime rectification." What a human is asked to
#: memorise, `lagna_windows` returns — including for D-30, whose borders are
#: not multiples of anything.
THE_CLOSING_SENTENCE_IS_A_REQUIREMENT_NOT_ADVICE = (
    "The example closes by asking the astrologer to know where lagna changes "
    "rasi in every varga. That is a table, and lagna_windows computes it, "
    "D-30's unequal borders included."
)


def window_for_varga_sign(current: float, wanted_sign: int,
                          varga: Callable[[float], object], *,
                          degrees_per_minute: float) -> dict:
    """Exercise 50's inequation: when is this point in that varga sign?

    "So the birthtime should be between 9:06:07 am and 9:08:31 am for GL in
    D-10 to be in Ar." Given where a point stands now and how fast it moves,
    this returns the seconds after the reported birthtime during which its
    varga sign is `wanted_sign` — the first such stretch at or after now.

    :param current: the point's longitude in the chart as reported.
    :param wanted_sign: the varga sign the known past calls for, 0 = Aries.
    :param varga: a varga function returning an object with a ``sign``.
    :param degrees_per_minute: the point's speed. Exact for HL and GL;
        a mean for the ascendant — see
        `THE_SPECIAL_LAGNA_RATES_ARE_EXACT_AND_THE_LAGNAS_IS_NOT`.
    :returns: ``from_seconds`` and ``to_seconds``, the arc each end needs, and
        ``found``. ``found`` is False when the sign is not reached within one
        rasi of travel.
    :raises BirthtimeError: on a non-positive speed.
    """
    here = validate.longitude("current", float(current))
    sign = validate.in_range("wanted_sign", int(wanted_sign), 0, 11)
    rate = validate.finite("degrees_per_minute", float(degrees_per_minute))
    if rate <= 0:
        raise BirthtimeError(
            f"degrees_per_minute must be positive; got {degrees_per_minute}")

    windows = lagna_windows(here, here + 30.0, varga)
    for window in windows:
        if int(cast(int, window["sign"])) != sign:
            continue
        low_arc = cast(float, window["from"]) - here
        high_arc = cast(float, window["to"]) - here
        return {
            "found": True, "wanted_sign": sign,
            "from_degrees": low_arc, "to_degrees": high_arc,
            "from_seconds": low_arc / rate * 60.0,
            "to_seconds": high_arc / rate * 60.0,
            "degrees_per_minute": rate,
        }
    return {"found": False, "wanted_sign": sign,
            "from_degrees": None, "to_degrees": None,
            "from_seconds": None, "to_seconds": None,
            "degrees_per_minute": rate,
            "reason": "the wanted sign is not reached within one rasi of "
                      "travel from the reported position"}


def narrow_down(windows: tuple[dict, ...] | list[dict]) -> dict:
    """The exercise's closing sentence: intersect several inequations.

    "If we create several inequations like the above using lagna and special
    lagnas in various divisional charts, we can narrow down to the correct
    birthtime."

    :param windows: results from `window_for_varga_sign`.
    :returns: the overlap in seconds after the reported birthtime, with
        ``possible`` False and a reason when the constraints cannot all hold.
    :raises BirthtimeError: if no windows are given, or one was not found.
    """
    rows = list(windows)
    if not rows:
        raise BirthtimeError("at least one window is needed")
    for index, row in enumerate(rows):
        if not row.get("found"):
            raise BirthtimeError(
                f"window {index} was not found and cannot be intersected")

    low = max(float(cast(float, row["from_seconds"])) for row in rows)
    high = min(float(cast(float, row["to_seconds"])) for row in rows)
    if high <= low:
        return {"possible": False, "from_seconds": None, "to_seconds": None,
                "windows": len(rows),
                "reason": "the windows do not overlap, so no single birthtime "
                          "satisfies every constraint"}
    return {"possible": True, "from_seconds": low, "to_seconds": high,
            "windows": len(rows), "reason": None}


# --------------------------------------------------------------------------
# Exercise 50 — the same move, on Ghati Lagna
# --------------------------------------------------------------------------

#: Exercise 50, verbatim.
EXERCISE_50 = (
    "Suppose someone is born at 9:05 am and has GL at 20Le37. This puts GL in "
    "D-10 in Aq. Suppose we expect the D-10 GL in Ar to explain the native's "
    "periods of power and authority. What should the correct birthtime be?")

#: Exercise 50's printed answer, verbatim.
EXERCISE_50_ANSWER = (
    "GL in D-10 goes to the next rasi at multiples of 3 degrees. Here it goes "
    "from Aq to Pi when GL crosses 21 degrees. It goes from Pi to Ar when GL "
    "crosses 24 degrees. So GL has to be at or above 24Le00. So the amount we "
    "have to add is 24 deg 0' - 20 deg 37' = 3 deg 21' = 201'.\n\n"
    "GL moves by 201' in 201 x 0.48 sec = 96.48 sec = 1 min 6.48 sec. So we "
    "should roughly add 1 min 7 sec and the birthtime should be 9:06:07 am or "
    "above.\n\n"
    "There is an upper limit also. If it becomes too high, GL in D-10 will "
    "move from Ar to Ta. But we decided that GL in D-10 in Ar makes the best "
    "sense. So we cannot add another 3 degrees to GL. GL moves by 3 degrees "
    "in 3 x 4/5 = 12/5 min = 2 min 24 sec. Adding this to 9:06:07, we get "
    "9:08:31. So the birthtime should be between 9:06:07 am and 9:08:31 am "
    "for GL in D-10 to be in Ar.\n\n"
    "If we create several inequations like the above using lagna and special "
    "lagnas in various divisional charts, we can narrow down to the correct "
    "birthtime.")

#: Exercise 50's figures, as printed against what they should be. See D-86.
EXERCISE_50_STATED: dict[str, object] = {
    "reported_birthtime": "9:05 am",
    "gl": "20 Le 37",
    "gl_degree_in_rasi": 20 + 37 / 60,
    "gl_in_d10_as_reported": "Aq",
    "wanted_d10_sign": "Ar",
    "borders": {"Aq_to_Pi": 21.0, "Pi_to_Ar": 24.0, "Ar_to_Ta": 27.0},
    "printed": {
        "arc_arcminutes": 201.0, "lower_seconds": 96.48,
        "lower_bound": "9:06:07", "upper_bound": "9:08:31",
        "width_seconds": 144.0,
    },
    "correct": {
        "arc_arcminutes": 203.0, "lower_seconds": 162.4,
        "lower_bound": "9:07:42.4", "upper_bound": "9:10:06.4",
        "width_seconds": 144.0,
    },
}

#: **Finding.** Every rasi the exercise names is right. Leo being odd, its
#: dasamsas run from Leo itself: 18°-21° is the 7th and gives **Aq**, 21°-24°
#: the 8th and gives **Pi**, 24°-27° the 9th and gives **Ar**, 27°-30° the
#: 10th and gives **Ta**. So GL must sit in **24 Le 00 to 27 Le 00**, exactly
#: the bracket the exercise reasons its way to.
EXERCISE_50S_RASIS_ARE_ALL_CORRECT = (
    "Leo's 7th, 8th, 9th and 10th dasamsas are Aq, Pi, Ar and Ta, so the "
    "wanted window is 24 Le 00 to 27 Le 00. The exercise's reasoning is "
    "right throughout."
)

#: **Finding, and it is the sharpest contrast in the chapter.** Example 129
#: had to end with a caveat — the ascendant does not move uniformly, so the
#: answer "may be a little off" and needs iterating. Exercise 50 needs no
#: caveat and does not give one, because **Ghati Lagna does move uniformly**.
#: Taking a real chart whose GL is 20 Le 37, the corrected 162.4 seconds lands
#: GL on 24 Le 00 to within the residual of the starting point. The arithmetic
#: is the answer, with no chart and no second pass.
THE_GHATI_LAGNA_METHOD_NEEDS_NO_SECOND_PASS = (
    "Example 129's ascendant answer needs iterating and Exercise 50's does "
    "not. Ghati Lagna advances 1.25 degrees a minute exactly, so the "
    "corrected 162.4 seconds lands on 24 Le 00 on a real chart."
)

#: **Finding, and it is the chapter's actual algorithm.** The last line —
#: "if we create several inequations like the above using lagna and special
#: lagnas in various divisional charts, we can narrow down to the correct
#: birthtime" — is the only place the book says how the pieces combine, and it
#: is a set intersection. `window_for_varga_sign` produces one inequation and
#: `narrow_down` intersects them, reporting `possible: False` with a reason
#: when the known past asks for something no single birthtime can give.
THE_LAST_LINE_IS_THE_ALGORITHM = (
    "Several inequations intersected is the whole method, and it is stated "
    "once, in the last line of an exercise answer. narrow_down is that "
    "intersection."
)


# --------------------------------------------------------------------------
# §32.2.2 Dasas
# --------------------------------------------------------------------------

SECTION_32_2_2_TITLE = "Dasas"

#: §32.2.2's first paragraph, verbatim.
RASI_DASAS_ARE_ROBUST = (
    "Rasi dasas based on rasi chart change only if lagna changes rasi or a "
    "planet changes rasi. Because lagna changes rasi once in 2 hours, we do "
    "not have to deal with inaccuracies in rasi dasas in most cases.")

#: §32.2.2's second paragraph, verbatim. See D-87.
NARAYANA_DASA_OF_VARGAS_IS_ROBUST = (
    "Narayana dasa of divisional charts does not change in a small period of "
    "time, unless a planet changes rasi in the divisional chart of interest.")

#: §32.2.2's derivation for the nakshatra dasas, verbatim.
NAKSHATRA_DASA_DATE_ERROR = (
    "However, the dasa start dates in nakshatra dasas change with small "
    "changes in birthtime. Let us say the complete duration (and not just the "
    "remainder at birth) of the dasa running at birth is n years. Let us say "
    "the birthtime is wrong by m minutes. Moon stays in the nakshatra for "
    "about 24x60 minutes (24 hours) and the error in the fraction of Moon's "
    "constellation that is yet to be traversed is m/(24x60). The error in the "
    "number of days of dasa left is nx360xm/(24x60) = (n x m)/4. If we add m "
    "minutes to the birthtime, we should subtract (n x m)/4 days from dasa "
    "dates and vice versa.")

#: §32.2.2's two worked nakshatra cases, verbatim.
NAKSHATRA_DASA_WORKED_CASES = (
    "If 7 years of Venus dasa remains at birth, then n = 20 and the "
    "approximate error in dasa dates is 20m/4 = 5m days, where m is the "
    "birthtime error in minutes. If the birthtime is wrong by 2 minutes, dasa "
    "dates are wrong by 10 days.\n\n"
    "If the birthtime is wrong by 2 minutes and 3 years of Moon dasa were "
    "remaining at birth, then n = 10 and m = 2 and the error in dasa dates is "
    "10x2/4 = 5 days.")

#: §32.2.2's Kalachakra paragraphs, verbatim.
KALACHAKRA_DATE_ERROR = (
    "In Kalachakra dasa, the error is more. If n years is the paramayush of "
    "the sequence corresponding to the navamsa of natal Moon and m minutes is "
    "the error in birthtime, the error in the dates of dasa is (n x m) days. "
    "If we add m minutes to the birthtime, we should subtract (n x m) days "
    "from dasa dates and vice versa.\n\n"
    "For example, if the paramayush is 100 years and the birthtime error is 2 "
    "minutes, then the error in dates is 200 days. It is almost 7 months!\n\n"
    "For this reason, it is futile to use pratyantardasas in Kalachakra dasa "
    "unless one is absolutely confident of the birthtime.")

#: The section's three worked figures, as data.
DASA_ERROR_CASES: tuple[dict[str, object], ...] = (
    {"system": "nakshatra", "lord": "Venus", "full_years": 20,
     "remaining_years": 7, "minutes": 2, "days": 10.0},
    {"system": "nakshatra", "lord": "Moon", "full_years": 10,
     "remaining_years": 3, "minutes": 2, "days": 5.0},
    {"system": "kalachakra", "lord": None, "full_years": 100,
     "remaining_years": None, "minutes": 2, "days": 200.0},
)


def nakshatra_dasa_date_error(full_dasa_years: float, minutes: float) -> dict:
    """§32.2.2's nakshatra formula: (n x m)/4 days.

    `full_dasa_years` is the **complete** length of the dasa running at birth
    and not the balance — the section says so where it defines n, and both of
    its worked cases print a balance that plays no part in the answer.

    The sign is the section's: "if we add m minutes to the birthtime, we
    should subtract (n x m)/4 days from dasa dates and vice versa", so a
    positive `minutes` returns days to be **subtracted**.

    :raises BirthtimeError: on a non-positive dasa length.
    """
    years = validate.finite("full_dasa_years", float(full_dasa_years))
    if years <= 0:
        raise BirthtimeError(
            f"full_dasa_years must be positive; got {full_dasa_years}")
    error = validate.finite("minutes", float(minutes))
    return {
        "days": years * error / 4.0,
        "subtract_from_dasa_dates": error > 0,
        "full_dasa_years": years, "minutes": error,
        "rule": NAKSHATRA_DASA_DATE_ERROR,
    }


def kalachakra_date_error(paramayush_years: float, minutes: float) -> dict:
    """§32.2.2's Kalachakra formula: (n x m) days.

    `paramayush_years` is the paramayush of the sequence for the natal Moon's
    navamsa — one of the four values §24.2's Table 48 gives.

    :raises BirthtimeError: on a non-positive paramayush.
    """
    years = validate.finite("paramayush_years", float(paramayush_years))
    if years <= 0:
        raise BirthtimeError(
            f"paramayush_years must be positive; got {paramayush_years}")
    error = validate.finite("minutes", float(minutes))
    return {
        "days": years * error,
        "subtract_from_dasa_dates": error > 0,
        "paramayush_years": years, "minutes": error,
        "rule": KALACHAKRA_DATE_ERROR,
    }


#: **Finding, measured, and it settles §32.2.1's loose Moon.** "Moon stays in
#: the nakshatra for about 24x60 minutes" is a good figure: measured over a
#: year, the Moon's nakshatra takes **21.00 to 27.25 hours, mean 24.34**. And
#: 24.34 hours a nakshatra implies **54.76 hours a rasi**, which is the
#: measured rasi mean to a rounding. So the chapter states the Moon's speed
#: three times — 60 hours a rasi in §32.2.1, 200 arcminutes in 6 hours two
#: sentences later, and 24 hours a nakshatra here — and the last two agree
#: with the sky and with each other. Only the 60 is loose.
THE_TWENTY_FOUR_HOUR_NAKSHATRA_IS_THE_ACCURATE_FIGURE = (
    "The Moon's nakshatra runs 21.00 to 27.25 hours with a mean of 24.34, "
    "which implies 54.76 hours a rasi and not section 32.2.1's 60. Of the "
    "chapter's three statements of the Moon's speed, only the 60 is loose."
)

#: **Finding, and it is OI-115's year.** The derivation turns years into days
#: by multiplying by **360** — "nx360xm/(24x60)" — so §32.2.2 computes in
#: **savana** years, the 360-day year §16.2's controversy box chose for every
#: nakshatra dasa in the book. It is used here without comment, and it is what
#: makes the quotient come out as a clean quarter. Evidence on OI-115;
#: **nothing changes** — precedence keeps JHora's sidereal default until you
#: rule.
THE_DERIVATION_USES_SAVANA_YEARS = (
    "The formula turns years into days by multiplying by 360, so section "
    "32.2.2 is working in savana years. It is stated nowhere here and it is "
    "what makes n x m / 4 come out whole. Evidence on OI-115, no change."
)

#: **Finding, and it is why the two formulas differ by exactly four.** The
#: nakshatra dasas divide by four and Kalachakra does not, and the reason is
#: geometry: Kalachakra is seeded from the Moon's **navamsa**, a quarter of a
#: nakshatra. A nakshatra takes 24x60 minutes and a pada 360, so the
#: Kalachakra error is n x 360 x m / 360 = n x m — the 360 days of a savana
#: year cancelling the 360 minutes of a pada, which is why that formula has no
#: divisor at all.
THE_KALACHAKRA_FACTOR_IS_FOUR_BECAUSE_A_PADA_IS_A_QUARTER = (
    "Kalachakra reads the Moon's navamsa, a quarter of a nakshatra, so its "
    "error is four times the nakshatra dasas'. A savana year's 360 days "
    "cancel a pada's 360 minutes, which is why the formula has no divisor."
)

#: **Finding.** Both worked nakshatra cases print a **balance** that plays no
#: part in the answer — "7 years of Venus dasa remains", "3 years of Moon dasa
#: were remaining". The formula takes the complete duration, and the section
#: warns of exactly this in the same breath it introduces n: "the complete
#: duration (and not just the remainder at birth)". The 20 and the 10 are
#: Venus's and the Moon's whole Vimsottari periods; the 7 and the 3 are
#: decoys the section plants and defuses in advance.
THE_PRINTED_BALANCES_PLAY_NO_PART = (
    "Seven years of Venus and three of the Moon are printed and unused. The "
    "formula takes 20 and 10, the complete Vimsottari periods, and the "
    "section warns of exactly this where it defines n."
)

#: **Finding, measured, and "futile" understates it.** At the section's own
#: m = 2 and paramayush 100 the error is 200 days. Run against a real savya
#: pada-1 sequence, using §24.2's own wheel rather than a proportional model:
#: **715 of the 729 pratyantardasas** are shorter than 200 days, so the
#: warning about pratyantardasas is right. But **17 of the 81 antardasas** are
#: shorter than 200 days too — the shortest is exactly **100 days** — and the
#: section says nothing about antardasas. Only the nine dasas survive, the
#: shortest being 1800 days.
EVEN_ANTARDASAS_ARE_SWAMPED_AT_TWO_MINUTES = (
    "Two minutes of error is 200 days at paramayush 100. In a savya pada-1 "
    "sequence that exceeds 715 of the 729 pratyantardasas and 17 of the 81 "
    "antardasas, the shortest of which is 100 days. All nine dasas survive it."
)

#: **Finding, and it is the reason the varga claim is as safe as it is.**
#: §32.2.1 spent its length establishing that the **varga lagna** is the
#: fastest thing in a chart — a D-24 lagna changes rasi every five minutes.
#: A varga Narayana dasa never touches it. §18.5 counts the seed house in the
#: **rasi** chart, takes that house's lord, and asks where **that graha** sits
#: in the varga; `varga_lagna` takes a rasi lagna and a table of graha varga
#: rasis, and no varga ascendant at all. So the volatile quantity plays no
#: part, which is why §32.2.2 can say what it says.
THE_VARGA_ASCENDANT_PLAYS_NO_PART_IN_A_VARGA_NARAYANA_DASA = (
    "Section 18.5 reads the seed house in the rasi chart and finds its lord "
    "in the varga, so a varga Narayana dasa never uses the varga ascendant — "
    "the one quantity section 32.2.1 showed to be volatile."
)

#: **Book defect, D-87.** §32.2.2's second paragraph gives a varga Narayana
#: dasa one trigger: "unless a planet changes rasi in the divisional chart of
#: interest". There is a second. §18.5 counts the seed house from the **rasi**
#: lagna, so when that lagna crosses a rasi boundary the seed rasi changes,
#: its **lord** changes, and the varga lagna jumps to wherever the new lord
#: stands — with no graha having moved anywhere.
#:
#: The first paragraph names it for rasi-chart dasas — "only if **lagna
#: changes rasi** or a planet changes rasi" — and the second drops the term
#: for varga charts, where §18.5 makes it just as load-bearing. The
#: conclusion survives: a rasi lagna crosses a boundary once in about two
#: hours, so a varga Narayana dasa still does not change in a small period of
#: time. It is a missing term, not a wrong conclusion.
THE_RASI_LAGNA_IS_LEFT_OUT_OF_THE_NARAYANA_CLAIM = (
    "A varga Narayana dasa also changes when the rasi lagna crosses a rasi "
    "boundary, because section 18.5 counts the seed house from it. Section "
    "32.2.2 names only the grahas. The conclusion survives; the term is "
    "missing. See D-87."
)


# --------------------------------------------------------------------------
# §32.2.3 Tajaka Charts
# --------------------------------------------------------------------------

SECTION_32_2_3_TITLE = "Tajaka Charts"

#: §32.2.3's first paragraph, verbatim.
THE_TAJAKA_LAGNA_MOVES_WITH_THE_NATAL_ONE = (
    "If the change in lagna in the natal chart due to a birthtime change is "
    "x, then the lagna in the Tajaka annual and monthly charts will also "
    "change by approximately x. However, we have to keep in mind that the "
    "list of divisional charts in which lagna is near rasi borders may "
    "change.")

#: §32.2.3's worked example, verbatim. See D-88 on "the middle".
THE_TAJAKA_BORDER_EXAMPLE = (
    "For example, let us say that natal lagna is at 23Sc30 and lagna in a "
    "Tajaka annual chart for 1980-81 is at 15Cn05. Let us say that the "
    "birthtime can have an error of upto 3 minutes (either way - plus or "
    "minus). Let us say that we are interested in the career of the native "
    "and especially in an event in career that took place in 1980-81. In "
    "natal D-10, lagna (23Sc30) is in the *middle* of the 8th dasamsa in Sc. "
    "Unless the birthtime changes by more than 6 minutes in either direction, "
    "lagna in D-10 will not change. However, lagna in 1980-81 Tajaka annual "
    "chart is close to a dasamsa border. If lagna is just below 15 degrees in "
    "Cn, lagna in D-10 will be in the 5th from Pi, i.e. Cn itself. If lagna "
    "is just above 15 degrees in Cn, lagna in D-10 will be in the 6th from "
    "Pi, i.e. Le. With the given birthtime, we get 15Cn05 and so lagna in "
    "D-10 in the Tajaka chart is in Le. But it could be Cn if the native's "
    "birth took place half a minute before the reported birthtime.")

#: §32.2.3's conclusion from the example, verbatim.
THE_TAJAKA_CHART_CAN_SHOW_WHAT_THE_NATAL_ONE_HIDES = (
    "Thus, sometimes we cannot detect a birthtime error just by looking at "
    "the natal chart and dasas. Looking at the divisional charts of Tajaka "
    "annual charts can help in some cases.")

#: §32.2.3's caveat on how the Tajaka chart itself is cast, verbatim. "boo"
#: is the book's; the word is not completed on the page.
THE_ACCURACY_ASSUMPTION = (
    "The assumption here is that one casts Tajaka charts very accurately. "
    "This is not true with those who use the approximate method taught in "
    "this boo or those who find the exact solar return but use an approximate "
    "formula for Sun's motion or use a linear formula for ayanamsa.")

#: §32.2.3's closing paragraph on the ayanamsa, verbatim.
AYANAMSA_MUST_BE_NONLINEAR = (
    "The actual ayanamsa used matters only to a small extent, in the sense "
    "that it has the same impact on the longitude of lagna and the rasis "
    "occupied by lagna in various divisional charts, as it has in the natal "
    "chart. On the other hand, using an approximate linear formula for "
    "ayanamsa brings minor discrepancy in Sun's longitude which is multiplied "
    "by 360 in the longitude of lagna. This results in a serious error. "
    "Though we do not know exactly when Nirayana zodiac coincided with the "
    "Sayana zodiac, we do know the exact nonlinear formula of the precession. "
    "So one hoping to use Tajaka charts in birthtime rectification **must** "
    "use the correct **nonlinear** formula of the ayanamsa of one's choice. "
    "Unfortunately, many people use linear approximations. They are not good "
    "enough for Tajaka charts.")

#: The example's figures, as printed against what they should be. See D-88.
TAJAKA_BORDER_EXAMPLE_STATED: dict[str, object] = {
    "natal_lagna": "23 Sc 30",
    "natal_lagna_degree_in_rasi": 23.5,
    "natal_dasamsa": 8,
    "natal_dasamsa_span": (21.0, 24.0),
    "printed_margin_minutes": 6.0,
    "correct_margin_minutes": (10.0, 2.0),      # down, up
    "the_middle_of_the_eighth": 22.5,
    "annual_lagna": "15 Cn 05",
    "annual_lagna_degree_in_rasi": 15 + 5 / 60,
    "annual_border": 15.0,
    "below_the_border": "Cn",
    "above_the_border": "Le",
    "printed_margin_seconds": 30.0,
    "correct_margin_seconds": 20.0,
    "error_bound_minutes": 3.0,
}

#: The Sun's mean daily motion in degrees — 360 over a sidereal year. The
#: denominator of §32.2.3's amplification.
SUN_DEGREES_PER_DAY = 360.0 / 365.2564


def solar_return_amplification(sun_error_arcminutes: float, *,
                               sun_degrees_per_day: float = SUN_DEGREES_PER_DAY,
                               lagna_degrees_per_day: float = 360.0) -> dict:
    """§32.2.3's x360: what an error in the Sun costs the annual lagna.

    "Using an approximate linear formula for ayanamsa brings minor
    discrepancy in Sun's longitude which is multiplied by 360 in the longitude
    of lagna."

    The mechanism is the solar return itself. An error of d degrees in the
    Sun's longitude moves the instant the Sun is judged to have returned by
    d / (the Sun's daily motion) **days**, and the ascendant covers 360
    degrees in a day — so the annual chart's lagna is out by 360 d / (daily
    motion), which is about 360 times d.

    :param sun_error_arcminutes: the error in the Sun's longitude.
    :raises BirthtimeError: on a non-positive daily motion.
    """
    error = validate.finite("sun_error_arcminutes",
                            float(sun_error_arcminutes))
    per_day = validate.finite("sun_degrees_per_day",
                              float(sun_degrees_per_day))
    lagna_per_day = validate.finite("lagna_degrees_per_day",
                                    float(lagna_degrees_per_day))
    if per_day <= 0 or lagna_per_day <= 0:
        raise BirthtimeError(
            "sun_degrees_per_day and lagna_degrees_per_day must both be "
            f"positive; got {sun_degrees_per_day} and {lagna_degrees_per_day}")

    days = (error / 60.0) / per_day
    return {
        "sun_error_arcminutes": error,
        "instant_error_minutes": days * 1440.0,
        "lagna_error_degrees": days * lagna_per_day,
        "amplification": lagna_per_day / per_day,
        "rule": AYANAMSA_MUST_BE_NONLINEAR,
    }


#: **Finding, measured, and the first claim is stronger than "approximately".**
#: A birthtime shifted by m minutes moves the natal Sun by m minutes' worth of
#: motion, so the solar return moves by **m minutes too** — measured on a real
#: nativity, +1, +3 and +5 minutes of birthtime moved the eleventh annual
#: chart's instant by 1.006, 3.007 and 5.003 minutes. The annual lagna then
#: moves by whatever its own ascendant does in that time: 17.3' against the
#: natal chart's 14.5' for one minute, the two differing only because the two
#: charts' ascendants rise at different rates. "Approximately x" is right, and
#: the *instant* tracks to better than a per cent.
THE_ANNUAL_INSTANT_TRACKS_THE_BIRTHTIME_ALMOST_EXACTLY = (
    "One, three and five minutes of birthtime moved a real annual chart's "
    "instant by 1.006, 3.007 and 5.003 minutes. The annual lagna moved 17.3' "
    "against the natal chart's 14.5', the difference being the two "
    "ascendants' own rates."
)

#: **Finding, measured.** "The actual ayanamsa used matters only to a small
#: extent... it has the same impact on the longitude of lagna... as it has in
#: the natal chart" is exactly right, and the reason is that the solar return
#: is defined against the **same** sidereal zodiac it is measured in: change
#: the ayanamsa and both the target and the Sun shift together, so the
#: **instant does not move**. Measured on one nativity, Lahiri and Raman give
#: the same return instant to **0.002 seconds**, and the annual lagna shifts
#: by 1.44631 degrees against the natal lagna's 1.44630 — the same shift to
#: five decimal places.
CHANGING_THE_AYANAMSA_DOES_NOT_MOVE_THE_RETURN_INSTANT = (
    "Lahiri and Raman put one nativity's solar return at the same instant to "
    "two thousandths of a second, and shift the annual and natal lagnas by "
    "the same 1.4463 degrees. The ayanamsa cancels out of the return."
)

#: **Finding, measured against the engine, and the x360 is exact.** Perturbing
#: the natal Sun by **one arcminute** and re-solving the return moved the
#: instant by **24.38 minutes** and the annual lagna by **6.88 degrees** —
#: more than two whole dasamsas. A tenth of an arcminute still costs 2.44
#: minutes and 0.70 degrees. The book's ×360 is not rhetoric: it is
#: 360 divided by the Sun's degree a day.
#:
#: How much that bites depends on the baseline. **Lahiri itself is very nearly
#: linear over the modern era**: against a least-squares line it departs by at
#: most **0.014 arcminutes** over 1900-2100, worth 0.08 degrees of annual
#: lagna. Over 1500-2100 it is 0.111 arcminutes and 0.67 degrees, and over
#: 1000-2100 0.371 arcminutes and 2.26 degrees. So the warning is right, and
#: it is a warning about crude linearisations and long baselines rather than
#: about a century-scale best fit.
THE_TIMES_360_IS_EXACT_AND_THE_BASELINE_DECIDES_THE_DAMAGE = (
    "One arcminute of Sun error moved a real annual chart's instant by 24.38 "
    "minutes and its lagna by 6.88 degrees. Lahiri departs from a best-fit "
    "line by 0.014 arcminutes over 1900-2100 and 0.371 over 1000-2100, worth "
    "0.08 and 2.26 degrees of annual lagna."
)

#: **Finding, and the book's warning about its own method is quantified by its
#: own exercise.** §32.2.3 says the accuracy assumption "is not true with
#: those who use the approximate method taught in this boo". §27.2's method
#: was measured against Exercise 47 at **72 seconds** out in one year and
#: **118 seconds** in another. At the ascendant's nominal quarter-degree a
#: minute that is **18 to 30 arcminutes** of annual lagna — three to six times
#: the 5 arcminutes this section's own example turns on.
THE_BOOKS_OWN_APPROXIMATE_METHOD_MISSES_BY_A_THIRD_OF_A_DEGREE = (
    "Section 27.2's approximate method was 72 and 118 seconds out on one "
    "nativity, which is 18 to 30 arcminutes of annual lagna — several times "
    "the 5 arcminutes section 32.2.3's own example hangs on."
)

#: **Finding.** The annual lagna's margin is **20 seconds**, not the half
#: minute printed: 15 Cn 05 stands 5 arcminutes above the 15-degree border and
#: the ascendant covers 15 arcminutes a minute. Half a minute earlier would
#: certainly put it below, so the sentence is true as a **sufficient**
#: condition and loose as an exact one, which is what §32.2's bolded
#: "approximate" licenses. Both figures reproduce: just below 15 gives Cancer
#: and 15 Cn 05 gives Leo, counted the 5th and 6th from Pisces as printed.
THE_ANNUAL_MARGIN_IS_TWENTY_SECONDS_NOT_THIRTY = (
    "15 Cn 05 is 5 arcminutes above the border and the ascendant does 15 a "
    "minute, so 20 seconds suffices. Half a minute is a true sufficient "
    "condition, not the exact margin."
)

#: **Book defect, D-88.** "In natal D-10, lagna (23Sc30) is in the *middle* of
#: the 8th dasamsa in Sc." The 8th dasamsa of Scorpio spans 21 to 24 degrees
#: and its middle is **22 Sc 30**, not 23 Sc 30. The consequence the section
#: draws — "unless the birthtime changes by more than 6 minutes in either
#: direction, lagna in D-10 will not change" — is right for 22 Sc 30, whose
#: margins are 1°30' each way at four minutes a degree. From 23 Sc 30 the
#: margins are **10 minutes down and 2 minutes up**.
#:
#: Two arcminutes up is **inside the example's own ±3 minute error bound**, so
#: as printed the natal D-10 lagna is not safe either — and the contrast the
#: whole example is built on collapses. Reading 22 for 23 restores it.
THE_MIDDLE_OF_THE_EIGHTH_DASAMSA_IS_22_SC_30 = (
    "The 8th dasamsa of Scorpio runs 21 to 24, so its middle is 22 Sc 30. "
    "From the printed 23 Sc 30 the margins are 10 minutes down and 2 up, and "
    "the 2 is inside the example's own 3-minute bound. See D-88."
)


# --------------------------------------------------------------------------
# §32.3 A Practical Approach
# --------------------------------------------------------------------------

SECTION_32_3_TITLE = "A Practical Approach"

#: §32.3's first paragraph, verbatim.
NARROW_DOWN_WITH_EACH_CRITERION = (
    "It is a good idea to first determine the correct D-9 lagna or D-10 lagna "
    "and then go to the other divisional charts. We should first determine "
    "that the birthtime is between 9:05 and 9:15. Then we can determine that "
    "it is between 9:07 and 9:11. Then we can use a more precise criterion "
    "and narrow down further. Thus we narrow down further and further with "
    "each criterion.")

#: §32.3's second paragraph, verbatim.
SOMETIMES_WE_MUST_COME_BACK_TO_D9 = (
    "If one's marriage has already taken place, we can use D-9 to see it and "
    "fix D-9 lagna. If not, we can see one's general sense of duty, one's "
    "basic skills and one's interaction with others and fix D-9 lagna based "
    "on them. Then we can go to a higher divisional chart. However, in "
    "reality, sometimes it may become necessary to come back to D-9. For "
    "example, suppose someone can have lagna in D-9 in Li or Sc. Suppose we "
    "think that Li is also a good candidate but Sc is better. Then the "
    "candidates for D-24 lagna that we get with this choice may not make "
    "sense. It may make sense to place lagna in D-24 in another rasi and that "
    "may require lagna in D-9 to be in Li. In that case, we can revisit D-9 "
    "and change the lagna.")

#: §32.3's closing paragraph, verbatim.
BROAD_THEN_FINE = (
    "Trying to first do a broad rectification with D-9 and D-10 and then "
    "doing a fine rectification with high divisional charts like D-20 and "
    "Kalachakra dasa will provide a systematic approach to the problem, but "
    "we should be willing to come back to the first step if we are stuck in "
    "the second step.")

#: §32.3's two narrowing steps, as data.
NARROWING_STEPS: tuple[dict[str, object], ...] = (
    {"step": 1, "from": "9:05", "to": "9:15", "width_minutes": 10.0},
    {"step": 2, "from": "9:07", "to": "9:11", "width_minutes": 4.0},
)

#: The instruments §32.3 names, in the order it names them, broad first.
THE_NAMED_INSTRUMENTS: tuple[dict[str, object], ...] = (
    {"stage": "broad", "instrument": "D-9", "varga": 9},
    {"stage": "broad", "instrument": "D-10", "varga": 10},
    {"stage": "fine", "instrument": "D-20", "varga": 20},
    {"stage": "fine", "instrument": "Kalachakra dasa", "varga": None},
)


def refine_windows(low: float, high: float,
                   coarse: Callable[[float], object],
                   fine: Callable[[float], object]) -> tuple[dict, ...]:
    """§32.3's move: which fine-varga lagnas each coarse-varga choice allows.

    "Suppose someone can have lagna in D-9 in Li or Sc... Then the candidates
    for D-24 lagna that we get with this choice may not make sense."

    :param low: the low end of the lagna range the birthtime allows.
    :param high: the high end.
    :param coarse: the varga whose lagna is being fixed first.
    :param fine: the varga whose candidates that choice constrains.
    :returns: one entry per coarse window, each carrying its own ``from``,
        ``to`` and ``sign`` and the ``fine`` windows inside it.
    """
    out: list[dict[str, object]] = []
    for window in lagna_windows(low, high, coarse):
        inner = lagna_windows(cast(float, window["from"]),
                              cast(float, window["to"]), fine)
        out.append({
            "from": window["from"], "to": window["to"],
            "sign": window["sign"],
            "fine": inner,
            "fine_signs": tuple(dict.fromkeys(
                int(cast(int, row["sign"])) for row in inner)),
        })
    return tuple(out)


#: **Finding, measured.** The order §32.3 names is strictly coarse to fine,
#: and by its own §32.2.1 rule the intervals fall monotonically: a **D-9**
#: lagna holds for **13.3 minutes**, a **D-10** lagna for **12**, a **D-20**
#: lagna for **6**, and **Kalachakra** resolves finer than any of them — at
#: paramayush 100 a whole day of dasa date costs only **0.6 seconds** of
#: birthtime. Four named instruments, four decreasing resolutions, in the
#: order printed.
THE_NAMED_ORDER_IS_STRICTLY_COARSE_TO_FINE = (
    "D-9's lagna holds 13.3 minutes, D-10's 12, D-20's 6, and Kalachakra "
    "moves a dasa date a whole day for 0.6 seconds of birthtime. The four "
    "instruments fall in resolution in the order the section names them."
)

#: **Finding.** The section's own two steps match the instruments it ends
#: with. The first window, 9:05 to 9:15, is **10 minutes** — about what fixing
#: a **D-10** lagna gives you, whose window is 12. The second, 9:07 to 9:11,
#: is **4 minutes** — about what a **D-20** or **D-24** lagna gives, whose
#: windows are 6 and 5. The illustration is not arbitrary; it is the broad
#: step and the fine step in minutes.
THE_TWO_STEPS_ARE_THE_TWO_STAGES_IN_MINUTES = (
    "Ten minutes is about a D-10 lagna's twelve and four is about a D-20's "
    "six or a D-24's five. The section's illustrative narrowing is its own "
    "broad and fine stages."
)

#: **Finding, demonstrated.** The backtracking §32.3 describes is real and
#: computable. Take a lagna near Aries 23°20', where the navamsa turns from
#: **Li** to **Sc**, with the three minutes either side §32.2.3 used:
#:
#: * D-9 in **Li** leaves exactly **one** D-24 candidate, Aquarius.
#: * D-9 in **Sc** leaves **two**, Aquarius or Pisces.
#:
#: So the D-9 choice really does decide what D-24 can be, and a D-24 answer of
#: Pisces forces D-9 to Sc while an answer outside those two forces the window
#: itself to widen. `refine_windows` returns exactly this.
THE_BACKTRACKING_IS_COMPUTABLE = (
    "Three minutes either side of Aries 23 degrees 20 gives D-9 in Li with "
    "one D-24 candidate, Aquarius, and D-9 in Sc with two, Aquarius or "
    "Pisces. The first choice constrains the second."
)

#: **Finding, and it says when backtracking is forced.** D-9's boundaries fall
#: at multiples of 3°20' and D-24's at multiples of 1°15', and inside one rasi
#: those coincide **only at 0°, 10°, 20° and 30°**. Everywhere else a D-24
#: amsa straddles a D-9 boundary, so two neighbouring D-9 choices **share** a
#: D-24 candidate — which is why the Aries case above overlaps in Aquarius.
#: Backtracking is forced only when the D-24 answer lies outside that shared
#: amsa; at the three coincident degrees the candidate sets are disjoint and
#: the D-9 choice decides D-24 outright.
D9_AND_D24_BORDERS_COINCIDE_ONLY_AT_TEN_DEGREE_MARKS = (
    "Inside a rasi the D-9 and D-24 boundaries coincide only at 0, 10, 20 and "
    "30 degrees, so neighbouring D-9 windows usually share one D-24 "
    "candidate. That shared amsa is what decides whether backtracking is "
    "forced."
)

#: **Finding.** The criteria §32.3 offers for fixing a D-9 lagna are §18.5's
#: own reasons for the varga. §18.5 explains D-9's seed as the 9th house
#: because "D-9 shows dharma (**duty**). To get married, to live with one's
#: spouse... are one's duties"; §32.3 says to use "one's marriage" or, failing
#: that, "one's general sense of **duty**". The rectification criterion is the
#: signification, taken straight across.
THE_D9_CRITERIA_ARE_SECTION_18_5S_OWN_SIGNIFICATIONS = (
    "Section 18.5 justifies D-9's seed by dharma and marriage, and section "
    "32.3 offers marriage and a general sense of duty as the things to fix a "
    "D-9 lagna by. The criterion is the signification."
)

