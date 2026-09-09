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

