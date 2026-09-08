"""§28.8.1 — sahams, the significant points of a Tajaka chart.

A saham is a longitude computed from three others. The formula is written
``A - B + C``, which the section glosses as "how far A is from B ... taken
from C" — the same arithmetic either way. On top of that there is one
correction, and it is the whole subtlety of the section:

    if C is not **between** B and A — walking zodiacally from B until A is
    met, without passing C — then thirty degrees are added.

The test is on **C**, not on the result, and the section adds thirty once and
not repeatedly. Both are taken as written.

Most formulas are for a **daytime** chart, and at night ``A - B + C`` becomes
``B - A + C``: the first two terms swap and the third stands. The between-test
then runs on the night formula's own first two terms, since §28.8.1 states the
rule for "a formula that looks like A - B + C" and at night that is the
formula. Table 74 marks the sahams where this does not apply.

Table 74 needs inputs the chapter does not define — a house's longitude, most
of all. Those are supplied by the caller and refused when missing; see OI-157.
"""
from __future__ import annotations

from hora.core import validate
from hora.core.const import GRAHA_NAMES, RASI_LORD, RASI_NAMES

SAHAM_DEFINITION = (
    "Sahams are the significant points in the zodiac related to specific "
    "matters. For example, \"raajya\" means kingdom and \"raajya saham\" is a "
    "significant point in the zodiac related to obtaining kingdom. "
    "\"Paradesa\" means a foreign country and \"paradesa saham\" is a "
    "significant point in the zodiac related to going abroad.")

SAHAM_FORMULA_RULE = (
    "Each saham has a formula that looks like A – B + C. What this means is "
    "that we take the longitudes of A, B and C and find (A – B + C). This is "
    "equivalent to finding how far A is from B and then taking the same "
    "distance from C. However, if C is not between B and A (i.e. we start "
    "from B and go zodiacally till we meet A and we do not find C on the "
    "way), then we add 30º to the value evaluated above.")

SAHAM_WORKED_GLOSS = (
    "For example, finding (Moon – Sun + Lagna) is equivalent to finding how "
    "far Moon is from Sun and taking the same distance from lagna. If we "
    "start from the longitude of Sun and go zodiacally till the longitude of "
    "Moon and do not find lagna on the way, then we have to add 30º.")

DAY_AND_NIGHT_RULE = (
    "For most sahams, the formula given as (A – B + C) is for daytime charts. "
    "For nighttime charts, it changes to (B – A + C). This will not be "
    "explicitly mentioned for each saham and a mention will be made only when "
    "there is a difference.")

#: The correction the section adds, in degrees, and it is added once.
SAHAM_CORRECTION_DEGREES = 30.0

TABLE_74_TITLE = "Sahams"


class SahamError(validate.InputError):
    """A saham input that cannot be resolved."""


# --------------------------------------------------------------------------
# Table 74's terms
# --------------------------------------------------------------------------
#
# A formula term is one of:
#
#   ("graha", name)      a graha's longitude
#   ("lagna",)           the lagna's longitude
#   ("saham", name)      another saham, computed first
#   ("house", n)         the nth house's longitude — see OI-157
#   ("house_lord", n)    the longitude of the nth house's lord
#   ("lagna_lord",)      the longitude of the lagna's lord
#   ("sign_lord", name)  the longitude of the lord of the sign a graha is in
#   ("fixed", degrees)   a fixed point in the zodiac
#
# The terms are data so the table can be read back and checked, and so that
# every input Table 74 needs is enumerable without running anything.

_GRAHA_IDS: dict[str, int] = {name: index for index, name in enumerate(
    ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"))}


def _g(name: str) -> tuple[str, str]:
    return ("graha", name)


_L: tuple[str] = ("lagna",)


def _s(name: str) -> tuple[str, str]:
    return ("saham", name)


#: Table 74 exactly as printed. ``day`` is (A, B, C); ``night`` is ``None``
#: when the general rule applies — the first two terms swap — ``"same"`` when
#: the row says the formula is the same for day and night, and a triple of its
#: own where the row prints a different night formula.
TABLE_74_SAHAMS: tuple[dict[str, object], ...] = (
    {"number": 1, "name": "Punya", "means": "Fortune/good deeds",
     "day": (_g("Moon"), _g("Sun"), _L), "night": None},
    {"number": None, "name": "Vidya", "means": "Education",
     "day": (_g("Sun"), _g("Moon"), _L), "night": None},
    {"number": 3, "name": "Yasas", "means": "Fame",
     "day": (_g("Jupiter"), _s("Punya"), _L), "night": None},
    {"number": 4, "name": "Mitra", "means": "Friend",
     "day": (_g("Jupiter"), _s("Punya"), _g("Venus")), "night": None},
    {"number": 5, "name": "Mahatmya", "means": "Greatness",
     "day": (_s("Punya"), _g("Mars"), _L), "night": None},
    {"number": 6, "name": "Asha", "means": "Desires",
     "day": (_g("Saturn"), _g("Mars"), _L), "night": None},
    {"number": 7, "name": "Samartha", "means": "Enterprise/ability",
     "day": (_g("Mars"), ("lagna_lord",), _L), "night": None,
     "if_mars_owns_lagna": (_g("Jupiter"), _g("Mars"), _L)},
    {"number": 8, "name": "Bhratri", "means": "Brothers",
     "day": (_g("Jupiter"), _g("Saturn"), _L), "night": "same"},
    {"number": 9, "name": "Gaurava", "means": "Respect/regard",
     "day": (_g("Jupiter"), _g("Moon"), _g("Sun")), "night": None},
    {"number": 10, "name": "Pitri", "means": "Father",
     "day": (_g("Saturn"), _g("Sun"), _L), "night": None},
    {"number": 11, "name": "Rajya", "means": "Kingdom",
     "day": (_g("Saturn"), _g("Sun"), _L), "night": None},
    {"number": 12, "name": "Matri", "means": "Mother",
     "day": (_g("Moon"), _g("Venus"), _L), "night": None},
    {"number": 13, "name": "Putra", "means": "Children",
     "day": (_g("Jupiter"), _g("Moon"), _L), "night": None},
    {"number": 14, "name": "Jeeva", "means": "Life",
     "day": (_g("Saturn"), _g("Jupiter"), _L), "night": None},
    {"number": 15, "name": "Karma", "means": "Action (work)",
     "day": (_g("Mars"), _g("Mercury"), _L), "night": None},
    {"number": 16, "name": "Roga", "means": "Disease",
     "day": (_L, _g("Moon"), _L), "night": None},
    {"number": 17, "name": "Kali", "means": "Great misfortune",
     "day": (_g("Jupiter"), _g("Mars"), _L), "night": None},
    {"number": 18, "name": "Sastra", "means": "Sciences",
     "day": (_g("Jupiter"), _g("Saturn"), _g("Mercury")), "night": None},
    {"number": 19, "name": "Bandhu", "means": "Relatives",
     "day": (_g("Mercury"), _g("Moon"), _L), "night": None},
    {"number": 20, "name": "Mrityu", "means": "Death",
     "day": (("house", 8), _g("Moon"), _L), "night": "same"},
    {"number": 21, "name": "Paradesa", "means": "Foreign countries",
     "day": (("house", 9), ("house_lord", 9), _L), "night": "same"},
    {"number": 22, "name": "Artha", "means": "Money",
     "day": (("house", 2), ("house_lord", 2), _L), "night": "same"},
    {"number": 23, "name": "Paradara", "means": "Adultery",
     "day": (_g("Venus"), _g("Sun"), _L), "night": None},
    {"number": 24, "name": "Vanik", "means": "Commerce",
     "day": (_g("Moon"), _g("Mercury"), _L), "night": None},
    {"number": 25, "name": "Karyasiddhi", "means": "Success in endeavours",
     "day": (_g("Saturn"), _g("Sun"), ("sign_lord", "Sun")),
     "night": (_g("Saturn"), _g("Moon"), ("sign_lord", "Moon"))},
    {"number": 26, "name": "Vivaha", "means": "Marriage",
     "day": (_g("Venus"), _g("Saturn"), _L), "night": None},
    {"number": 27, "name": "Santapa", "means": "Sadness",
     "day": (_g("Saturn"), _g("Moon"), ("house", 6)), "night": None},
    {"number": 28, "name": "Sraddha", "means": "Devotion/sincerity",
     "day": (_g("Venus"), _g("Mars"), _L), "night": None},
    {"number": 29, "name": "Preeti", "means": "Love/attachment",
     "day": (_s("Sastra"), _s("Punya"), _L), "night": None},
    {"number": 30, "name": "Jadya", "means": "Chronic disease",
     "day": (_g("Mars"), _g("Saturn"), _g("Mercury")), "night": None},
    {"number": 31, "name": "Vyapara", "means": "Business",
     "day": (_g("Mars"), _g("Saturn"), _L), "night": "same"},
    {"number": 32, "name": "Satru", "means": "Enemy",
     "day": (_g("Mars"), _g("Saturn"), _L), "night": None},
    {"number": 33, "name": "Jalapatana", "means": "Crossing an ocean",
     "day": (("fixed", 105.0), _g("Saturn"), _L), "night": None},
    {"number": 34, "name": "Bandhana", "means": "Imprisonment",
     "day": (_s("Punya"), _g("Saturn"), _L), "night": None},
    {"number": 35, "name": "Apamrityu", "means": "Bad death",
     "day": (("house", 8), _g("Mars"), _L), "night": None},
    {"number": 36, "name": "Labha", "means": "Material gains",
     "day": (("house", 11), ("house_lord", 11), _L), "night": "same"},
)


#: **Book defect.** Table 74's ``#`` column is blank for Vidya, between rows 1
#: and 3. Every other row is numbered, and the count is thirty-six either way,
#: so the number 2 is simply missing from the page.
VIDYA_HAS_NO_ROW_NUMBER = (
    "Table 74 numbers Punya 1 and Yasas 3 and leaves the cell between them "
    "blank. Vidya is the second saham and its number is not printed."
)

#: **Finding.** Sahams coincide, and not by accident. Checked over sixty
#: random charts, the same collisions appear in every one:
#:
#: * **Pitri = Rajya** always — both are Saturn − Sun + Lagna, so a nativity's
#:   father-point and kingdom-point are one longitude by day and by night.
#: * **Satru = Vyapara by day** — both Mars − Saturn + Lagna. At night they
#:   part, because Vyapara is marked "same for day & night" and Satru swaps.
#: * **Asha = Vyapara at night** — Asha swaps into Mars − Saturn + Lagna,
#:   which is what Vyapara stays.
#: * **Bhratri = Jeeva at night** — Jeeva swaps into Jupiter − Saturn +
#:   Lagna, which is what Bhratri stays.
#:
#: Three of the four are made by the "same for day & night" markers meeting
#: the general swap, so they are a consequence of how Table 74 is annotated
#: rather than of what it says. `saham_collisions` lists them.
SAHAMS_COINCIDE_STRUCTURALLY = (
    "Pitri and Rajya are the same point in every chart. Satru joins Vyapara "
    "by day; Asha joins Vyapara and Jeeva joins Bhratri at night. Only the "
    "first pair shares a printed formula — the others are the day-and-night "
    "markers meeting the general swap."
)

#: The collisions above, as data, with the condition each holds under.
SAHAM_COLLISIONS: tuple[dict[str, str | tuple[str, str]], ...] = (
    {"sahams": ("Pitri", "Rajya"), "when": "always",
     "because": "both are printed Saturn - Sun + Lagna"},
    {"sahams": ("Satru", "Vyapara"), "when": "day",
     "because": "both are printed Mars - Saturn + Lagna"},
    {"sahams": ("Asha", "Vyapara"), "when": "night",
     "because": "Asha swaps to Mars - Saturn + Lagna; Vyapara does not swap"},
    {"sahams": ("Bhratri", "Jeeva"), "when": "night",
     "because": "Jeeva swaps to Jupiter - Saturn + Lagna; Bhratri does not "
                "swap"},
)


def saham_collisions(*, daytime: bool) -> tuple[tuple[str, str], ...]:
    """Which sahams share a longitude in every chart, by day or by night."""
    wanted = "day" if daytime else "night"
    out: list[tuple[str, str]] = []
    for row in SAHAM_COLLISIONS:
        pair = row["sahams"]
        if row["when"] in ("always", wanted) and isinstance(pair, tuple):
            out.append(pair)
    return tuple(out)

#: **Finding.** Five sahams are computed from other sahams — Yasas, Mitra,
#: Mahatmya and Bandhana from Punya, and Preeti from **both** Sastra and
#: Punya. So Table 74 has an order, and Punya must be found before four of the
#: rows below it and Sastra before one. The dependency graph is acyclic and
#: two deep; `saham_order` returns a working order.
FIVE_SAHAMS_DEPEND_ON_OTHERS = (
    "Yasas, Mitra, Mahatmya and Bandhana take Punya as a term and Preeti "
    "takes Sastra and Punya. Nothing else in Table 74 refers to a saham, and "
    "no reference is circular."
)

#: **Finding.** Roga is **Lagna − Moon + Lagna**: the same point is both the
#: A term and the C term. It is the only row in Table 74 that repeats a term,
#: and it reduces to twice the lagna minus the Moon, so the between-test asks
#: whether the lagna lies on the arc from the Moon to the lagna — which is
#: the whole circle less that arc, and is therefore true only when the Moon
#: is at the lagna itself.
ROGA_USES_THE_LAGNA_TWICE = (
    "Roga is Lagna minus Moon plus Lagna. No other saham repeats a term, and "
    "the correction applies to it in every chart but one."
)

#: **Finding.** §28.8.1's correction is a **step**, not a smooth adjustment.
#: As C crosses either end of the arc from B to A the saham jumps by a whole
#: thirty degrees, so two charts a minute apart can put a saham a rasi apart.
#: That is what the rule says and it is not smoothed here.
THE_CORRECTION_IS_A_THIRTY_DEGREE_STEP = (
    "The thirty degrees are added when C leaves the arc from B to A, so the "
    "saham is discontinuous at both ends of that arc."
)

#: **Settled by Example 121.** Five rows need a **house's longitude** — the
#: 2nd, 6th, 8th, 9th and 11th — and §28.8 never says what that means. Example
#: 121 shows it: with lagna at 10 Cp 50 it puts the 2nd house at **10 Aq 50**,
#: which is the lagna carried forward exactly thirty degrees. Houses are equal
#: from the **lagna's own degree**, not from the start of its rasi and not
#: from a cusp system. `house_longitude` builds them; `sahams` still takes
#: them as an input so a caller may pass something else, but it no longer
#: needs to. OI-157 closed.
A_HOUSES_LONGITUDE_IS_NOT_DEFINED = (
    "Table 74 uses the 2nd, 6th, 8th, 9th and 11th houses as longitudes and "
    "section 28.8 does not say what that means. Example 121 fixes it: the "
    "2nd house is the lagna plus thirty degrees, to the arcminute."
)

#: **Finding.** The rule Example 121 fixes, as arithmetic. It is equal houses
#: from the lagna **point**, which is what §6 called the bhava madhya reading
#: — not the whole-sign rasi the chart is drawn in.
HOUSES_ARE_EQUAL_FROM_THE_LAGNA_DEGREE = (
    "The nth house's longitude is the lagna plus thirty degrees times n minus "
    "one. Example 121's lagna at 280 degrees 50 minutes gives a 2nd house at "
    "310 degrees 50 minutes, which is what the example prints."
)


def house_longitude(lagna: float, house: int) -> float:
    """The `house`th house's longitude under Example 121's rule."""
    seat = validate.longitude("lagna", float(lagna))
    number = validate.in_range("house", int(house), 1, 12)
    return (seat + 30.0 * (number - 1)) % 360.0


def house_longitudes(lagna: float) -> dict[int, float]:
    """Every house longitude Table 74 asks for, under Example 121's rule."""
    return {n: house_longitude(lagna, n) for n in houses_needed()}


def _needs(entry: dict, kind: str) -> tuple:
    """Every term of one row that is of `kind`, in both formulas."""
    out = []
    for formula in (entry["day"], entry.get("night")):
        if not isinstance(formula, tuple):
            continue
        for term in formula:
            if term[0] == kind:
                out.append(term)
    extra = entry.get("if_mars_owns_lagna")
    if isinstance(extra, tuple):
        for term in extra:
            if term[0] == kind:
                out.append(term)
    return tuple(dict.fromkeys(out))


def houses_needed() -> tuple[int, ...]:
    """Which house longitudes Table 74 asks for."""
    return tuple(sorted({term[1] for entry in TABLE_74_SAHAMS
                         for term in _needs(entry, "house")}))


def house_lords_needed() -> tuple[int, ...]:
    """Which house lords Table 74 asks for."""
    return tuple(sorted({term[1] for entry in TABLE_74_SAHAMS
                         for term in _needs(entry, "house_lord")}))


def saham_order() -> tuple[str, ...]:
    """Table 74's names in an order that satisfies every dependency."""
    by_name = {str(entry["name"]): entry for entry in TABLE_74_SAHAMS}
    done: list[str] = []
    pending = [str(entry["name"]) for entry in TABLE_74_SAHAMS]
    while pending:
        progressed = False
        for name in list(pending):
            wanted = {term[1] for term in _needs(by_name[name], "saham")}
            if wanted <= set(done):
                done.append(name)
                pending.remove(name)
                progressed = True
        if not progressed:                              # pragma: no cover
            raise SahamError(
                f"Table 74's saham references do not resolve: {pending}")
    return tuple(done)


def is_between(a: float, b: float, c: float) -> bool:
    """Is C on the arc walked zodiacally from B until A is met?

    §28.8.1's own words. The arc is measured forward from B, so it wraps
    through Aries without a special case, and both ends count as on the way:
    C at B is met at once and C at A is met last.
    """
    return ((c - b) % 360.0) <= ((a - b) % 360.0) + 1e-9


def saham_point(a: float, b: float, c: float) -> dict:
    """One saham from three longitudes, with §28.8.1's correction.

    :returns: the uncorrected value, whether C was on the arc, and the point.
    """
    first = validate.longitude("a", float(a))
    second = validate.longitude("b", float(b))
    third = validate.longitude("c", float(c))
    raw = (first - second + third) % 360.0
    inside = is_between(first, second, third)
    return {
        "a": first, "b": second, "c": third,
        "uncorrected": raw,
        "c_is_between": inside,
        "correction": 0.0 if inside else SAHAM_CORRECTION_DEGREES,
        "longitude": raw if inside else
                     (raw + SAHAM_CORRECTION_DEGREES) % 360.0,
        "rule": SAHAM_FORMULA_RULE,
    }


def formula_for(entry: dict, *, daytime: bool,
                mars_owns_lagna: bool = False) -> tuple:
    """Which of Table 74's formulas applies, given the time and the lagna.

    The general rule swaps the first two terms at night. A row marked "same
    for day & night" does not swap, and a row printing its own night formula
    uses that instead.
    """
    day = entry["day"]
    if entry["name"] == "Samartha" and mars_owns_lagna:
        day = entry["if_mars_owns_lagna"]
    if daytime:
        return day
    night = entry.get("night")
    if night == "same":
        return day
    if isinstance(night, tuple):
        return night
    return (day[1], day[0], day[2])          # the general swap


#: **Finding.** Punya and Vidya are each other's night formula. Punya is
#: Moon − Sun + Lagna and Vidya is Sun − Moon + Lagna, so the general swap
#: turns each into the other — the same three terms, the same between-test,
#: the same point. In a night chart the fortune-saham and the education-saham
#: simply exchange places.
PUNYA_AND_VIDYA_EXCHANGE_AT_NIGHT = (
    "Punya's night formula is Sun minus Moon plus Lagna, which is Vidya's day "
    "formula, and Vidya's night formula is Punya's day formula. The two "
    "sahams trade values between a day chart and a night chart."
)


def _resolve(term: tuple, *, longitudes: dict[str, float],
             lagna: float, lagna_rasi: int,
             houses: dict[int, float] | None,
             found: dict[str, float]) -> float:
    kind = term[0]
    if kind == "graha":
        return longitudes[term[1]]
    if kind == "lagna":
        return lagna
    if kind == "fixed":
        return float(term[1])
    if kind == "saham":
        return found[term[1]]
    if kind == "lagna_lord":
        return longitudes[str(GRAHA_NAMES[int(RASI_LORD[lagna_rasi])])]
    if kind == "house_lord":
        rasi = (lagna_rasi + int(term[1]) - 1) % 12
        return longitudes[str(GRAHA_NAMES[int(RASI_LORD[rasi])])]
    if kind == "sign_lord":
        rasi = int(longitudes[term[1]] // 30)
        return longitudes[str(GRAHA_NAMES[int(RASI_LORD[rasi])])]
    if kind == "house":
        if houses is None:
            return house_longitude(lagna, int(term[1]))
        if int(term[1]) not in houses:
            raise SahamError(
                f"the {term[1]}th house's longitude is needed and was not "
                f"supplied; {A_HOUSES_LONGITUDE_IS_NOT_DEFINED}")
        return float(houses[int(term[1])])
    raise SahamError(f"unknown term {term!r}")        # pragma: no cover


def sahams(*, longitudes: dict[str, float], lagna: float, daytime: bool,
           houses: dict[int, float] | None = None) -> dict[str, dict]:
    """Every saham of Table 74 that the supplied inputs allow.

    :param longitudes: the seven classical grahas by name, in the chart the
        sahams are being read for.
    :param houses: the 2nd, 6th, 8th, 9th and 11th houses as longitudes.
        §28.8 never says what a house's longitude is, but **Example 121
        does** — the lagna plus thirty degrees per house — so leaving this
        ``None`` uses that rule rather than returning those five undecided.
        Pass a mapping to override it; a mapping that omits a house Table 74
        needs still returns that saham undecided. See OI-157, closed.
    """
    for name in _GRAHA_IDS:
        if name not in longitudes:
            raise SahamError(f"{name}'s longitude is needed and was not "
                             f"supplied")
    seat = validate.longitude("lagna", float(lagna))
    rasi = int(seat // 30)
    mars_owns = rasi in (0, 7)
    by_name = {str(entry["name"]): entry for entry in TABLE_74_SAHAMS}

    found: dict[str, float] = {}
    out: dict[str, dict] = {}
    for name in saham_order():
        entry = by_name[name]
        formula = formula_for(entry, daytime=daytime,
                              mars_owns_lagna=mars_owns)
        try:
            a, b, c = (
                _resolve(term, longitudes=longitudes, lagna=seat,
                         lagna_rasi=rasi, houses=houses, found=found)
                for term in formula)
        except SahamError as why:
            out[name] = {
                "saham": name, "means": entry["means"],
                "number": entry["number"], "longitude": None,
                "undecided": str(why), "formula": formula,
            }
            continue
        point = saham_point(a, b, c)
        found[name] = point["longitude"]
        out[name] = {
            "saham": name,
            "means": entry["means"],
            "number": entry["number"],
            "formula": formula,
            "daytime": bool(daytime),
            "rasi": int(point["longitude"] // 30),
            "rasi_name": str(RASI_NAMES[int(point["longitude"] // 30)]),
            "undecided": None,
            **point,
        }
    return {name: out[name] for name in
            (str(entry["name"]) for entry in TABLE_74_SAHAMS)}


#: **Finding.** Two sahams the book prints elsewhere both reproduce, and both
#: need the **night** formula. Example 54 places Navin Patnaik's **Rajya
#: saham in Libra**; he was born at 12:58 am, and Sun − Saturn + Lagna on
#: Chart 19 gives **6 Li 20**, where the day formula gives Gemini. Example
#: 104 prints a lady's **vivaha saham at 1 Cp**; she was born at 9:41 pm, and
#: Saturn − Venus + Lagna on Chart 53 gives **0 Cp 41**, where the day formula
#: gives Gemini. Two nativities, two sahams, and the day-and-night swap
#: settled by both.
TWO_PRINTED_SAHAMS_REPRODUCE = (
    "Chart 19's Rajya saham comes out 6 Li 20 against Example 54's Libra, "
    "and Chart 53's vivaha saham 0 Cp 41 against Example 104's 1 Cp. Both "
    "are night births and both need the night formula."
)

#: **Was: not confirmed. Now confirmed by Example 121.** In both of those the
#: C term already lay on the arc, so neither added the thirty degrees. Example
#: 121's **samartha saham** does: lagna 280°50\' is not on the arc from Mars
#: 354°58\' to Saturn 19°10\', so 305°2\' becomes **335°2\' = 5 Pi 02**, which
#: is what the book prints. The correction now has a worked value.
THE_CORRECTION_HAS_NO_WORKED_VALUE = (
    "The two sahams printed outside chapter 28 both have C between B and A, "
    "so neither takes the correction. Example 121's samartha saham does: it "
    "prints 5 Pi 02, which is 305 degrees 2 minutes plus the thirty."
)

#: **Finding.** Example 121 works three sahams on Chart 66 and each exercises
#: something different: **artha** the "same for day & night" note and a house
#: as a longitude, **samartha** the thirty-degree correction, and **vanik**
#: the plain night swap. All three reproduce to the arcminute from the
#: example's own printed inputs.
EXAMPLE_121_COVERS_THREE_DIFFERENT_RULES = (
    "Artha exercises the day-and-night exemption and a house longitude, "
    "samartha the thirty-degree correction, and vanik the ordinary night "
    "swap. Three sahams, three rules, all reproducing."
)

#: **Book defect.** Chart 66's diagram and Example 121 disagree by an
#: arcminute on four of the five longitudes the example uses, and the reason
#: is mechanical: the **diagram truncates arcminutes and the example rounds
#: them**. Our own values sit between the two — Lagna 10 Cp 49.59\', Saturn
#: 19 Ar 9.59\', Moon 15 Pi 13.89\', Mercury 11 Aq 27.60\' — so each printing
#: is right about its own convention, and Mars at 24 Pi 58.22\' agrees with
#: both because its fraction is under a half. Five for five. Recorded rather
#: than corrected; the sahams are computed from the diagram, and the example's
#: numbers are reproduced separately from the example's own inputs.
CHART_66_TRUNCATES_WHERE_EXAMPLE_121_ROUNDS = (
    "Chart 66's diagram truncates arcminutes and Example 121 rounds them. "
    "The four values whose true fraction is over a half differ by one "
    "arcminute between the two printings, and Mars, whose fraction is under "
    "a half, agrees with both."
)

#: **Book defect.** The vanik paragraph of Example 121 opens its arithmetic
#: with "So samartha saham = 311°28\' - 345°14\' + 280°50\'". Those are vanik
#: saham's terms and the paragraph's own conclusion calls it vanik. A stray
#: word carried down from the paragraph above.
EXAMPLE_121_MISNAMES_VANIK_ONCE = (
    "The third paragraph writes \"samartha saham\" where it means vanik "
    "saham, in the line setting out the arithmetic. Its terms and its "
    "conclusion are both vanik's."
)

#: Example 121's three answers, as the book prints them.
EXAMPLE_121_SAHAMS: tuple[dict[str, object], ...] = (
    {"saham": "Artha", "means": "money", "printed": "2 Sc 30",
     "longitude": 212.5, "correction": 0.0,
     "exercises": "the same-for-day-and-night note, and a house longitude"},
    {"saham": "Samartha", "means": "enterprise/ability", "printed": "5 Pi 02",
     "longitude": 335.0 + 2.0 / 60.0, "correction": 30.0,
     "exercises": "the thirty-degree correction"},
    {"saham": "Vanik", "means": "commerce", "printed": "7 Sg 04",
     "longitude": 247.0 + 4.0 / 60.0, "correction": 0.0,
     "exercises": "the ordinary night swap"},
)

#: Example 121's own printed inputs, which differ from Chart 66's diagram by
#: an arcminute — see `CHART_66_TRUNCATES_WHERE_EXAMPLE_121_ROUNDS`.
EXAMPLE_121_INPUTS: dict[str, float] = {
    "lagna": 280.0 + 50.0 / 60.0,
    "second_house": 310.0 + 50.0 / 60.0,
    "Saturn": 19.0 + 10.0 / 60.0,
    "Mars": 354.0 + 58.0 / 60.0,
    "Moon": 345.0 + 14.0 / 60.0,
    "Mercury": 311.0 + 28.0 / 60.0,
}
