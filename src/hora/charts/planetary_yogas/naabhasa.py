"""§11.5 Naabhasa yogas — the classified celestial combinations.

§11.5 names **thirty-two** across four families and defines five of them:
three Aasraya and two Dala. The other twenty-seven are named only, and are
listed in `NAABHASA_NOT_YET_DEFINED` rather than registered — a yoga we cannot
detect must not appear among the verdicts, where its absence would read as a
finding.

The two families here work quite differently:

* **Aasraya** reads the modality of every planet's sign. "All the planets"
  means every one considered, so `include_nodes` changes the answer — and it
  bites harder here than in §11.2, because two more grahas must agree. Rahu
  and Ketu are always six signs apart and six signs apart is always the same
  modality, so admitting them never makes the yoga impossible, only rarer.
* **Dala** reads the natures of the grahas in the quadrants from lagna, so it
  needs a lagna and the benefic natures of §3.2.2. It ignores `include_nodes`
  entirely: that flag exists for the unresolved phrase "a planet", and
  "natural malefics" is not unresolved — §3.2.2 makes the nodes malefic, and
  §11.5.2's own Sarpa example is built from Mars, Rahu and Ketu.
"""
from __future__ import annotations

from hora.charts.planetary_yogas._shared import house_sign, ordinal
from hora.charts.planetary_yogas.registry import (
    YogaInput,
    YogaSpec,
    YogaVerdict,
    register,
)
from hora.core.const import (
    GRAHA_NAMES,
    KENDRA,
    MODALITY_NAMES_EN,
    NAABHASA_YOGAS,
    RASI_MODALITY,
    RASI_NAMES,
)

_SPEC = {entry["key"]: entry for entry in NAABHASA_YOGAS}

#: §11.5.2 asks for **three** quadrants, not four and not two.
_DALA_QUADRANTS = 3


def _make_aasraya_detector(key: str):
    spec = _SPEC[key]
    modality = spec["modality"]
    name = spec["name"]
    word = MODALITY_NAMES_EN[modality]

    def detect(data: YogaInput) -> YogaVerdict:
        # "**All** the planets" is literally universal, so a partial chart
        # cannot decide it: a graha not supplied might be the one in another
        # modality. Answering from what happens to be present would report a
        # yoga that a fuller chart destroys.
        expected = data.considered()
        missing = [g for g in expected if data.sign_of(g) is None]
        if missing:
            named = ", ".join(GRAHA_NAMES[g] for g in missing)
            return YogaVerdict(
                key=key, name=name, present=False,
                reason=(f"this yoga needs every planet placed and "
                        f"{named} {'is' if len(missing) == 1 else 'are'} "
                        f"missing; it cannot be decided"),
            )
        placed = list(expected)
        outside = [g for g in placed if RASI_MODALITY[data.rasis[g]] != modality]
        if outside:
            named = ", ".join(
                f"{GRAHA_NAMES[g]} in {RASI_NAMES[data.rasis[g]]}"
                for g in outside[:3]
            )
            more = "" if len(outside) <= 3 else f" and {len(outside) - 3} more"
            return YogaVerdict(
                key=key, name=name, present=False,
                reason=f"not every planet is in a {word} sign: {named}{more}",
            )
        return YogaVerdict(
            key=key, name=name, present=True,
            reason=(f"all {len(placed)} placed planets are in {word} signs"),
            participants=tuple(sorted(int(g) for g in placed)),
        )

    return detect


def _make_dala_detector(key: str):
    spec = _SPEC[key]
    name = spec["name"]
    wanted = spec["nature"]

    def detect(data: YogaInput) -> YogaVerdict:
        if data.lagna_rasi is None:
            return YogaVerdict(
                key=key, name=name, present=False,
                reason=("no lagna was supplied, and this yoga counts quadrants "
                        "from lagna; it cannot be decided"),
            )
        benefics, undecidable = data.benefics()
        benefic_set = {int(g) for g in benefics}

        occupied: dict[int, list[int]] = {}
        for house in KENDRA:
            sign = house_sign(data.lagna_rasi, house)
            # **Every** placed graha, not `considered()`. `include_nodes`
            # governs the phrase "a planet" (§11.2, §11.3, §11.5.1), which the
            # book never resolves. "Natural benefics"/"natural malefics" is a
            # different phrase and §3.2.2 settles it: the nodes are natural
            # malefics. §11.5.2's own Sarpa example proves the point — it is
            # built from Mars, **Rahu and Ketu**.
            grahas = [int(g) for g in sorted(data.rasis)
                      if data.rasis[g] == sign]
            if grahas:
                occupied[house] = grahas

        # Dala works from the grahas supplied. §11.5.2's own examples give
        # only three or four placements, so a partial chart is what the book
        # itself illustrates with — but a graha left out could be a contrary
        # one in a quadrant, so an incomplete chart is flagged.
        matching = {
            house: grahas for house, grahas in occupied.items()
            if all((g in benefic_set) is (wanted == "benefic") for g in grahas)
        }
        contrary = {
            house: grahas for house, grahas in occupied.items()
            if house not in matching
        }

        if len(matching) < _DALA_QUADRANTS:
            return YogaVerdict(
                key=key, name=name, present=False,
                reason=(f"{len(matching)} of the four quadrants from lagna are "
                        f"occupied wholly by natural {wanted}s; "
                        f"{_DALA_QUADRANTS} are needed"),
            )

        qualifiers: tuple[str, ...] = ()
        weakened = bool(contrary)
        absent = [g for g in data.considered() if data.sign_of(g) is None]
        if absent:
            named = ", ".join(GRAHA_NAMES[g] for g in absent)
            qualifiers = (
                (f"{named} had no placement, so a contrary graha in a quadrant "
                 f"may have been missed"),
            )
        if contrary:
            named = ", ".join(
                f"{GRAHA_NAMES[g]} in the {ordinal(house)}"
                for house, grahas in sorted(contrary.items()) for g in grahas
            )
            qualifiers = (f"{spec['weakened_text']} ({named})",)
        if undecidable:
            named = ", ".join(GRAHA_NAMES[g] for g in undecidable)
            qualifiers = (
                *qualifiers,
                f"the nature of {named} could not be judged from the input",
            )

        participants = tuple(sorted(
            g for grahas in matching.values() for g in grahas))
        houses = {g: house for house, grahas in matching.items() for g in grahas}
        where = ", ".join(f"the {ordinal(h)}" for h in sorted(matching))
        return YogaVerdict(
            key=key, name=name, present=True,
            reason=(f"natural {wanted}s occupy {len(matching)} quadrants from "
                    f"lagna — {where}"),
            participants=participants, houses=houses, qualifiers=qualifiers,
            weakened=weakened,
        )

    return detect


for _key, _entry in _SPEC.items():
    _detector = (_make_aasraya_detector if _entry["group"] == "aasraya"
                 else _make_dala_detector)
    register(YogaSpec(
        key=_key,
        name=_entry["name"],
        aliases=(),
        section=_entry["section"],
        group=f"naabhasa_{_entry['group']}",
        definition=_entry["definition"],
        detect=_detector(_key),
    ))
