"""Avastha computation — book §15.4.

Three families are computed here: age, alertness, and attitude/mood. Together
they are the part of "strength of planets" this book actually defines well
enough to compute — shadbala, ashtakavarga and vimsopaka bala are named by the
chapter but not derived in it.

Mood states are returned as a **set**, not one winner. §15.4.3 lists nine
conditions and six more, and nothing says they are exclusive: a planet can be
exalted (Deepta) and joined by malefics (Vikala) at the same time.

Any state whose condition needs an input we do not have is reported as
**undetermined** with the reason, never as false.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from hora.charts.dignity import compound_relation, sign_dignity
from hora.core import validate
from hora.core.const import (
    ACTIVITY_STRENGTH,
    ADDITIONAL_MOOD_AVASTHAS,
    AGE_AVASTHAS,
    ALERTNESS_AVASTHAS,
    ELEMENT_NAMES,
    GHATIS_PER_HOUR,
    GRAHA_NAMES,
    MOOD_AVASTHAS,
    NATURAL_BENEFIC,
    NATURAL_MALEFIC,
    PLANETARY_ADJUSTMENT,
    RASI_ELEMENT,
    RASI_IS_ODD,
    RASI_LORD,
    RASI_NAMES,
    SAYANAADI_AVASTHAS,
    SAYANAADI_SPECIAL_RESULTS,
    SOUND_NUMBERS,
    Graha,
)
from hora.core.ephemeris.base import PlanetPosition


class AvasthaError(validate.InputError):
    """An avastha input that cannot be resolved."""


#: Rasis of watery element, for Trishita.
WATERY_RASIS = frozenset(
    i for i in range(12) if ELEMENT_NAMES[RASI_ELEMENT[i]] == "water"
)

#: §15.4.3's first additional state names these five explicitly.
LAJJITA_GRAHAS = frozenset(
    {Graha.SUN, Graha.MARS, Graha.SATURN, Graha.RAHU, Graha.KETU}
)


@dataclass(frozen=True)
class AgeAvastha:
    """§15.4.1 — the state a planet's degree in its rasi puts it in."""

    name: str
    meaning: str
    results: str
    #: ``results`` as a number, where the book gives one. Vriddha's result is
    #: "Some", which is not a quantity, so this is None there.
    fraction: float | None
    rasi: int
    rasi_name: str
    rasi_is_odd: bool
    degrees_in_rasi: float
    #: The band of the rasi this state occupies, for the rasi's parity.
    band: tuple[float, float]


@dataclass(frozen=True)
class AlertnessAvastha:
    """§15.4.2 — awake, dreaming or asleep."""

    name: str
    meaning: str
    results: str
    when: str
    #: What the planet's relationship to its rasi was judged to be.
    basis: str


@dataclass(frozen=True)
class MoodAvastha:
    """§15.4.3 — one attitude/mood state, and whether it applies."""

    name: str
    meaning: str
    when: str
    applies: bool | None
    #: Why it applies, or what is missing when ``applies`` is None.
    reason: str
    additional: bool = False


@dataclass(frozen=True)
class Avasthas:
    """Every state computed for one graha."""

    graha: int
    graha_name: str
    age: AgeAvastha
    alertness: AlertnessAvastha
    mood: list[MoodAvastha] = field(default_factory=list)

    @property
    def in_mood(self) -> list[str]:
        """Names of the mood states that apply."""
        return [m.name for m in self.mood if m.applies]

    @property
    def undetermined(self) -> list[str]:
        """Names of the mood states that could not be decided."""
        return [m.name for m in self.mood if m.applies is None]


# --------------------------------------------------------------------------
# §15.4.1 Age
# --------------------------------------------------------------------------

def avastha_by_age(longitude: float) -> AgeAvastha:
    """The age-related state, from the longitude alone — Table 35.

    Odd and even rasis run the bands in opposite directions: a planet at 3° is
    Saisava (child) in an odd rasi and Mrita (dead) in an even one.

    :param longitude: sidereal longitude in degrees; wrapped into 0-360.
    :raises AvasthaError: if the longitude is not finite.
    """
    lon = validate.longitude("longitude", longitude)
    rasi = int(lon // 30.0)
    degrees = lon % 30.0
    odd = bool(RASI_IS_ODD[rasi])
    key = "odd" if odd else "even"

    for row in AGE_AVASTHAS:
        start, end = row[key]
        if start <= degrees < end:
            return AgeAvastha(
                name=row["name"], meaning=row["meaning"], results=row["results"],
                fraction=row["fraction"], rasi=rasi, rasi_name=RASI_NAMES[rasi],
                rasi_is_odd=odd, degrees_in_rasi=degrees, band=(start, end),
            )
    raise AvasthaError(  # pragma: no cover - the bands tile 0 to 30
        f"no age avastha band contains {degrees}° of {RASI_NAMES[rasi]}"
    )


# --------------------------------------------------------------------------
# §15.4.2 Alertness
# --------------------------------------------------------------------------

def _relation_to_lord(graha: int, positions: dict[int, PlanetPosition]) -> str:
    """The graha's compound relationship to the lord of the rasi it sits in."""
    rasi = int(positions[graha].longitude // 30.0)
    lord = int(RASI_LORD[rasi])
    if lord == graha:
        return "own"
    if lord not in positions:
        raise AvasthaError(
            f"{GRAHA_NAMES[graha]} is in {RASI_NAMES[rasi]}, whose lord is "
            f"{GRAHA_NAMES[lord]}; the relationship to the lord needs its "
            f"position, which was not given"
        )
    return compound_relation(graha, lord, positions)


def avastha_by_alertness(
    graha: int, positions: dict[int, PlanetPosition]
) -> AlertnessAvastha:
    """Awake, dreaming or asleep — §15.4.2.

    Moolatrikona counts as an own rasi: the book's condition is "its exaltation
    rasi or an own rasi", and a moolatrikona rasi is one the planet owns.

    **"Neutral or friendly" and "enemy" are read as the compound relationship**,
    not the natural one. §15.4.2 does not say which, and chapter 3 defines both.
    The two part company wherever natural enmity is offset by temporary
    friendship, which changes the verdict between Swapna and Sushupta — see
    docs/open-items.md OI-114.

    :raises AvasthaError: if the graha has no position.
    """
    if graha not in positions:
        raise AvasthaError(f"no position given for {GRAHA_NAMES[graha]}")

    dignity = sign_dignity(graha, positions[graha].longitude)
    if dignity in ("exalted", "own", "moolatrikona"):
        row, basis = ALERTNESS_AVASTHAS[0], dignity
    elif dignity == "debilitated":
        row, basis = ALERTNESS_AVASTHAS[2], dignity
    else:
        relation = _relation_to_lord(graha, positions)
        if relation in ("enemy", "great_enemy"):
            row, basis = ALERTNESS_AVASTHAS[2], relation
        else:
            row, basis = ALERTNESS_AVASTHAS[1], relation

    return AlertnessAvastha(
        name=row["name"], meaning=row["meaning"], results=row["results"],
        when=row["when"], basis=basis,
    )


# --------------------------------------------------------------------------
# §15.4.3 Attitude and mood
# --------------------------------------------------------------------------

def _co_tenants(graha: int, positions: dict[int, PlanetPosition]) -> set[int]:
    """Other grahas in the same rasi. "Joined by" is read as same-rasi."""
    rasi = int(positions[graha].longitude // 30.0)
    return {
        other for other, pos in positions.items()
        if other != graha and int(pos.longitude // 30.0) == rasi
    }


def _joined_by_sun(
    graha: int, positions: dict[int, PlanetPosition], close_orb: float | None
) -> tuple[bool | None, str]:
    """Kopita's condition: "joined closely by Sun".

    The book does not quantify "closely". With no orb given, same-rasi is used
    and the response says so; pass ``close_orb`` to tighten it.
    """
    if graha == Graha.SUN or Graha.SUN not in positions:
        return False, "the Sun cannot be joined by itself" if graha == Graha.SUN \
            else "no position given for the Sun"
    same_rasi = Graha.SUN in _co_tenants(graha, positions)
    if close_orb is None:
        return same_rasi, (
            "Sun is in the same rasi; the book does not quantify \"closely\", "
            "so same-rasi is used"
            if same_rasi else "Sun is not in the same rasi"
        )
    separation = abs(positions[graha].longitude - positions[Graha.SUN].longitude)
    separation = min(separation, 360.0 - separation)
    within = separation <= close_orb
    return within, f"Sun is {separation:.2f}° away, orb {close_orb}°"


def avasthas_by_mood(
    graha: int,
    positions: dict[int, PlanetPosition],
    house: int | None = None,
    aspected_by: set[int] | None = None,
    close_orb: float | None = None,
) -> list[MoodAvastha]:
    """The nine mood states and the six additional ones — §15.4.3.

    Returns every state with ``applies`` True, False, or **None** where the
    condition needs an input that was not supplied. None is never collapsed to
    False: "we could not tell" and "it does not apply" are different answers.

    :param house: the house the planet occupies, needed by Lajjita only.
    :param aspected_by: grahas aspecting this one. This engine does not compute
        aspects (see docs/open-items.md OI-18), so the four states that need
        them stay undetermined unless the caller supplies this.
    :param close_orb: degrees for Kopita's "closely". Unquantified in the book.
    """
    if graha not in positions:
        raise AvasthaError(f"no position given for {GRAHA_NAMES[graha]}")

    longitude = positions[graha].longitude
    rasi = int(longitude // 30.0)
    dignity = sign_dignity(graha, longitude)
    relation = _relation_to_lord(graha, positions)
    joined = _co_tenants(graha, positions)
    lord = int(RASI_LORD[rasi])

    joined_malefics = joined & set(NATURAL_MALEFIC)
    enemies_joined = {
        g for g in joined
        if g != graha and compound_relation(graha, g, positions)
        in ("enemy", "great_enemy")
    }

    def rel(name: str) -> bool:
        return relation == name

    out: list[MoodAvastha] = []

    def add(row: dict, applies: bool | None, reason: str, additional: bool = False):
        out.append(MoodAvastha(
            name=row["name"], meaning=row["meaning"], when=row["when"],
            applies=applies, reason=reason, additional=additional,
        ))

    # --- the nine ---
    add(MOOD_AVASTHAS[0], dignity == "exalted", f"dignity is {dignity}")
    add(MOOD_AVASTHAS[1], dignity in ("own", "moolatrikona"), f"dignity is {dignity}")
    add(MOOD_AVASTHAS[2], rel("great_friend"), f"relation to lord is {relation}")
    add(MOOD_AVASTHAS[3], rel("friend"), f"relation to lord is {relation}")
    add(MOOD_AVASTHAS[4], rel("neutral"), f"relation to lord is {relation}")
    add(MOOD_AVASTHAS[5], rel("enemy") or rel("great_enemy"),
        f"relation to lord is {relation}")
    add(MOOD_AVASTHAS[6], bool(joined_malefics),
        "joined by " + (", ".join(sorted(GRAHA_NAMES[g] for g in joined_malefics))
                        or "no malefic"))
    add(MOOD_AVASTHAS[7], lord in NATURAL_MALEFIC,
        f"{RASI_NAMES[rasi]} is owned by {GRAHA_NAMES[lord]}")
    applies, reason = _joined_by_sun(graha, positions, close_orb)
    add(MOOD_AVASTHAS[8], applies, reason)

    # --- the six additional ---
    if house is None:
        add(ADDITIONAL_MOOD_AVASTHAS[0], None,
            "needs the house the planet occupies", additional=True)
    else:
        in_fifth = house == 5
        present = joined & LAJJITA_GRAHAS
        add(ADDITIONAL_MOOD_AVASTHAS[0], in_fifth and bool(present),
            f"house {house}; joined by "
            + (", ".join(sorted(GRAHA_NAMES[g] for g in present)) or "none of the five"),
            additional=True)

    add(ADDITIONAL_MOOD_AVASTHAS[1], dignity in ("exalted", "moolatrikona"),
        f"dignity is {dignity}", additional=True)

    saturn_joined = Graha.SATURN in joined and graha != Graha.SATURN
    hungry_now = rel("enemy") or rel("great_enemy") or bool(enemies_joined) or saturn_joined
    if aspected_by is None and not hungry_now:
        add(ADDITIONAL_MOOD_AVASTHAS[2], None,
            "no aspect data; the other three conditions do not hold", additional=True)
    else:
        why = []
        if rel("enemy") or rel("great_enemy"):
            why.append("in an enemy's rasi")
        if enemies_joined:
            why.append("conjoined by enemies")
        if saturn_joined:
            why.append("conjoined by Saturn")
        if aspected_by:
            aspecting_enemies = {
                g for g in aspected_by
                if compound_relation(graha, g, positions) in ("enemy", "great_enemy")
            }
            if aspecting_enemies:
                why.append("aspected by enemies")
        add(ADDITIONAL_MOOD_AVASTHAS[2], bool(why),
            "; ".join(why) or "none of the four conditions hold", additional=True)

    if aspected_by is None:
        add(ADDITIONAL_MOOD_AVASTHAS[3], None,
            "needs aspect data", additional=True)
    else:
        watery = rasi in WATERY_RASIS
        enemy_aspects = any(
            compound_relation(graha, g, positions) in ("enemy", "great_enemy")
            for g in aspected_by
        )
        benefic_aspects = bool(aspected_by & set(NATURAL_BENEFIC))
        add(ADDITIONAL_MOOD_AVASTHAS[3],
            watery and enemy_aspects and not benefic_aspects,
            f"{RASI_NAMES[rasi]} watery={watery}, enemy aspect={enemy_aspects}, "
            f"benefic aspect={benefic_aspects}", additional=True)

    if aspected_by is None:
        add(ADDITIONAL_MOOD_AVASTHAS[4], None, "needs aspect data", additional=True)
    else:
        friends_around = {
            g for g in (joined | aspected_by)
            if compound_relation(graha, g, positions) in ("friend", "great_friend")
        }
        jupiter_joined = Graha.JUPITER in joined and graha != Graha.JUPITER
        add(ADDITIONAL_MOOD_AVASTHAS[4],
            (rel("friend") or rel("great_friend")) and bool(friends_around)
            and jupiter_joined,
            f"relation to lord is {relation}; friends around={bool(friends_around)}; "
            f"Jupiter joined={jupiter_joined}", additional=True)

    if aspected_by is None:
        add(ADDITIONAL_MOOD_AVASTHAS[5], None, "needs aspect data", additional=True)
    else:
        sun_joined = Graha.SUN in joined and graha != Graha.SUN
        hostile_aspects = any(
            g in NATURAL_MALEFIC
            or compound_relation(graha, g, positions) in ("enemy", "great_enemy")
            for g in aspected_by
        )
        add(ADDITIONAL_MOOD_AVASTHAS[5], sun_joined and hostile_aspects,
            f"Sun joined={sun_joined}; malefic or enemy aspect={hostile_aspects}",
            additional=True)

    return out


def all_avasthas(
    graha: int,
    positions: dict[int, PlanetPosition],
    house: int | None = None,
    aspected_by: set[int] | None = None,
    close_orb: float | None = None,
) -> Avasthas:
    """Every computable state for one graha."""
    if graha not in positions:
        raise AvasthaError(f"no position given for {GRAHA_NAMES[graha]}")
    return Avasthas(
        graha=int(graha),
        graha_name=GRAHA_NAMES[graha],
        age=avastha_by_age(positions[graha].longitude),
        alertness=avastha_by_alertness(graha, positions),
        mood=avasthas_by_mood(graha, positions, house, aspected_by, close_orb),
    )


# --------------------------------------------------------------------------
# §15.4.4 States related to activity — the sayanaadi avasthas
#
# "This state is the most important of all states."
#
# Unlike the other three families this one is a formula, so it is computed
# step by step and every intermediate is returned. A caller checking a chart
# against JHora needs to see which term diverged, not just that the answer did.
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class ActivityStep:
    """One step of §15.4.4's computation."""

    number: int
    name: str
    description: str
    value: int | None = None
    detail: str | None = None


@dataclass(frozen=True)
class ActivityAvastha:
    """§15.4.4 — the state, and the strength of the activity."""

    graha: int
    graha_name: str
    #: The six inputs, keyed by the book's symbols.
    terms: dict[str, int]
    index: int
    name: str
    meaning: str
    aliases: tuple[str, ...]
    #: None when no name was supplied — the strength needs one.
    strength: str | None
    strength_results: str | None
    strength_remainder: int | None
    sound_number: int | None
    steps: tuple[ActivityStep, ...]


def navamsa_index(longitude: float) -> int:
    """``A`` — which of the nine navamsas of its *own rasi* a planet is in.

    Footnote 51 is explicit that this is **not** the rasi the planet occupies
    in the navamsa chart. Mercury at 22Ge14 gives 7, because each navamsa is
    3°20' and 22°14' falls in the seventh.

    :returns: 1 to 9.
    """
    lon = validate.longitude("longitude", longitude)
    return int((lon % 30.0) / (30.0 / 9.0)) + 1


def constellation_number(longitude: float) -> int:
    """``C`` and ``M`` — the nakshatra number, 1 for Aswini."""
    lon = validate.longitude("longitude", longitude)
    return int(lon / (360.0 / 27.0)) + 1


def ghati_at_birth(hours_after_sunrise: float) -> int:
    """``G`` — the ghati running at birth.

    Footnote 52: 17 hours after sunrise is 42.5 ghatis elapsed, so the 43rd
    ghati is running. The ghati *running* is one past the number elapsed.

    :raises AvasthaError: if the value is negative or not finite.
    """
    hours = validate.non_negative(
        "hours_after_sunrise", validate.finite("hours_after_sunrise", hours_after_sunrise)
    )
    return int(hours * GHATIS_PER_HOUR) + 1


def sound_number(syllable: str) -> int:
    """Table 37's number for the first sound of a name.

    Accepts a Devanagari character, which is unambiguous. A Roman syllable is
    matched against the book's own transliteration and **raises when it is
    ambiguous**: the book's Roman column distinguishes "d (alveolar)" in group
    1 from "d (dental)" in group 5, and a bare "d" cannot choose between them.

    :raises AvasthaError: on an unknown or ambiguous syllable.
    """
    text = syllable.strip()
    if not text:
        raise AvasthaError("empty syllable")

    for number, row in SOUND_NUMBERS.items():
        if text[0] in row["devanagari"]:
            return number

    lowered = text.lower()
    matches = []
    for number, row in SOUND_NUMBERS.items():
        for token in row["roman"].split(","):
            bare = token.split("(")[0].strip().lower()
            if bare and lowered.startswith(bare):
                matches.append((number, len(bare), token.strip()))
    if not matches:
        raise AvasthaError(
            f"no Table 37 sound matches {syllable!r}; pass the Devanagari "
            f"letter, or the sound number directly"
        )
    longest = max(length for _n, length, _t in matches)
    best = [(n, t) for n, length, t in matches if length == longest]
    if len({n for n, _t in best}) > 1:
        options = "; ".join(f"{n}: {t}" for n, t in sorted(best))
        raise AvasthaError(
            f"{syllable!r} is ambiguous in Table 37's Roman column ({options}). "
            f"The Devanagari is unambiguous — pass that, or the sound number."
        )
    return best[0][0]


def avastha_by_activity(
    graha: int,
    graha_longitude: float,
    moon_longitude: float,
    lagna_rasi: int,
    ghati: int,
    name_sound: int | str | None = None,
) -> ActivityAvastha:
    """§15.4.4 — the sayanaadi avastha and the strength of its activity.

    ``(C x P x A) + M + G + L``, divided by 12, remainder as the index.

    :param graha: 0 = Sun. The book's ``P`` is this plus one.
    :param graha_longitude: gives ``C`` and ``A``.
    :param moon_longitude: gives ``M``.
    :param lagna_rasi: 0 = Aries. The book's ``L`` is this plus one.
    :param ghati: the ghati running at birth, from :func:`ghati_at_birth`.
    :param name_sound: Table 37's number (1-5), or a syllable to look up. The
        strength cannot be computed without it and is returned as None.
    :raises AvasthaError: on an out-of-range input or an ambiguous syllable.

    **Remainder zero is read as 12.** The book says to "take the remainder"
    and index Table 36 with it, but the table runs 1 to 12 and has no row 0,
    so a remainder of 0 can only mean the twelfth. Recorded as D-19.
    """
    p = validate.in_range("graha", graha, 0, 8) + 1
    c = constellation_number(graha_longitude)
    a = navamsa_index(graha_longitude)
    m = constellation_number(moon_longitude)
    g = validate.in_range("ghati", ghati, 1, 60)
    ell = validate.in_range("lagna_rasi", lagna_rasi, 0, 11) + 1

    steps: list[ActivityStep] = []
    product = c * p * a
    steps.append(ActivityStep(
        1, "product", "C x P x A", product, f"{c} x {p} x {a} = {product}"))
    total = product + m + g + ell
    steps.append(ActivityStep(
        2, "sum", "(C x P x A) + M + G + L", total,
        f"{product} + {m} + {g} + {ell} = {total}"))
    remainder = total % 12
    index = remainder if remainder != 0 else 12
    steps.append(ActivityStep(
        3, "index", "divide by 12 and take the remainder", index,
        f"{total} mod 12 = {remainder}"
        + ("; a remainder of 0 indexes the 12th row" if remainder == 0 else ""),
    ))

    row = SAYANAADI_AVASTHAS[index]
    steps.append(ActivityStep(
        4, "avastha", "look up Table 36", index,
        f"{index} is {row['name']} ({row['meaning']})"))

    strength = results = None
    strength_remainder = sound = None
    if name_sound is not None:
        sound = (
            name_sound if isinstance(name_sound, int)
            else sound_number(name_sound)
        )
        validate.in_range("name_sound", sound, 1, 5)
        squared = index * index
        steps.append(ActivityStep(
            5, "squared", "multiply the index by itself", squared,
            f"{index} x {index} = {squared}"))
        with_sound = squared + sound
        steps.append(ActivityStep(
            6, "with_sound",
            "add Table 37's number for the first sound of the name",
            with_sound, f"{squared} + {sound} = {with_sound}"))
        reduced = with_sound % 12
        steps.append(ActivityStep(
            7, "reduced", "take the remainder on division by 12", reduced,
            f"{with_sound} mod 12 = {reduced}"))
        adjustment = PLANETARY_ADJUSTMENT[int(graha)]
        adjusted = reduced + adjustment
        steps.append(ActivityStep(
            8, "adjusted", "add the planetary adjustment", adjusted,
            f"{reduced} + {adjustment} for {GRAHA_NAMES[graha]} = {adjusted}"))
        strength_remainder = adjusted % 3
        entry = ACTIVITY_STRENGTH[strength_remainder]
        strength, results = entry["name"], entry["results"]
        steps.append(ActivityStep(
            9, "strength", "divide by 3 and take the remainder",
            strength_remainder,
            f"{adjusted} mod 3 = {strength_remainder}, which is {strength} "
            f"and {results} results",
        ))

    return ActivityAvastha(
        graha=int(graha), graha_name=GRAHA_NAMES[graha],
        terms={"C": c, "P": p, "A": a, "M": m, "G": g, "L": ell},
        index=index, name=row["name"], meaning=row["meaning"],
        aliases=tuple(row.get("aliases", ())),
        strength=strength, strength_results=results,
        strength_remainder=strength_remainder, sound_number=sound,
        steps=tuple(steps),
    )


@dataclass(frozen=True)
class SpecialResult:
    """One of Parasara's special results, decided or explicitly not."""

    rule: int
    verbatim: str
    effect: str
    auspicious: bool
    applies: bool | None
    reason: str


def special_results(
    avastha_index: int,
    nature: str | None = None,
    house: int | None = None,
    dignity: str | None = None,
    graha: int | None = None,
    associated_with_malefics: bool | None = None,
) -> list[SpecialResult]:
    """§15.4.4's eight special results for one graha, all eight every time.

    Every rule comes back with ``applies`` True, False, or **None** where an
    input it needs was not supplied. None is never collapsed to False, for the
    same reason section 15.4.4's own conditions are not: "we cannot tell" and
    "it does not apply" are different answers.

    :param avastha_index: Table 36's index, 1 to 12.
    :param nature: "benefic" or "malefic", from :mod:`hora.charts.benefic`.
        The Moon has none apart from its phase, so it must be resolved first.
    :param house: the house the graha occupies, 1 to 12.
    :param dignity: only rule 7 uses it, and only to admit a graha that is not
        a benefic but sits in its own or exaltation rasi.
    :param graha: only rule 8 uses it, to recognise the Moon.
    :param associated_with_malefics: only rule 2 uses it. This function is
        given a placement, not a chart, so the caller must supply it.
    :raises AvasthaError: on an out-of-range avastha index or house.
    """
    index = validate.in_range("avastha_index", avastha_index, 1, 12)
    if house is not None:
        validate.in_range("house", house, 1, 12)

    out: list[SpecialResult] = []
    for rule in SAYANAADI_SPECIAL_RESULTS:
        applies, reason = _special_rule(
            rule, index, nature, house, dignity, graha, associated_with_malefics)
        out.append(SpecialResult(
            rule=int(rule["rule"]), verbatim=str(rule["verbatim"]),
            effect=str(rule["effect"]), auspicious=bool(rule["auspicious"]),
            applies=applies, reason=reason))
    return out


def _special_rule(
    rule: dict,
    index: int,
    nature: str | None,
    house: int | None,
    dignity: str | None,
    graha: int | None,
    associated_with_malefics: bool | None,
) -> tuple[bool | None, str]:
    """One rule against one placement. The avastha is checked first: a rule
    that does not fire in this avastha is decided without any other input."""
    if index not in rule["avasthas"]:
        wanted = ", ".join(SAYANAADI_AVASTHAS[a]["name"] for a in rule["avasthas"])
        return False, f"{SAYANAADI_AVASTHAS[index]['name']}, not {wanted}"

    checks: list[tuple[bool | None, str]] = []

    actor = rule["actor"]
    if actor == "Moon":
        if graha is None:
            checks.append((None, "needs to know which graha this is"))
        else:
            checks.append((int(graha) == int(Graha.MOON),
                           f"graha is {GRAHA_NAMES[graha]}, wants Moon"))
    elif actor.startswith("benefic or"):
        # Rule 7 admits either route, so one satisfied route decides it.
        by_nature = None if nature is None else nature == "benefic"
        by_dignity = (
            None if dignity is None else dignity in ("own", "exalted"))
        if by_nature or by_dignity:
            checks.append((True, f"nature {nature}, dignity {dignity}"))
        elif by_nature is None or by_dignity is None:
            checks.append((None, (
                f"needs a benefic nature or an own/exaltation dignity "
                f"(nature {nature}, dignity {dignity})")))
        else:
            checks.append((False, f"nature {nature}, dignity {dignity}"))
    elif nature is None:
        checks.append((None, f"needs the graha's nature (wants {actor})"))
    else:
        checks.append((nature == actor, f"nature is {nature}, wants {actor}"))

    if rule["houses"]:
        wanted = ", ".join(str(h) for h in rule["houses"])
        if house is None:
            checks.append((None, f"needs the house (wants {wanted})"))
        else:
            checks.append((house in rule["houses"], f"house {house}, wants {wanted}"))

    if rule.get("unless_associated_with"):
        if associated_with_malefics is None:
            checks.append((None, (
                "needs to know about conjunction or aspect by another "
                "malefic; this function is given a placement, not a chart")))
        else:
            checks.append((not associated_with_malefics,
                           f"associated with malefics: {associated_with_malefics}"))

    detail = "; ".join(text for _v, text in checks)
    if any(value is False for value, _t in checks):
        return False, detail
    if any(value is None for value, _t in checks):
        return None, detail
    return True, detail
