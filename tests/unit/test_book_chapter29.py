"""Chapter 29 — Tajaka yogas. §29.1, §29.2.1, §29.2.2, §29.2.3."""

import itertools
import random

import pytest

from hora.core.const import Graha
from hora.tajaka import yogas

# --------------------------------------------------------------------------
# §29.1 Introduction
# --------------------------------------------------------------------------


def test_the_introduction_is_transcribed():
    assert yogas.CHAPTER_TITLE == "Tajaka Yogas"
    assert "Tajaka annual/monthly charts" in yogas.INTRODUCTION
    assert "prasna charts (horary charts)" in yogas.INTRODUCTION


def test_prasna_is_named_here_and_taught_nowhere():
    """The only other mention in the book is §3.2.13's note on graha periods.
    """
    from hora.core.constants.graha import TIME_PERIOD_USE

    assert "prasna or horary astrology" in TIME_PERIOD_USE
    assert "never explains how a prasna chart is cast" in (
        yogas.PRASNA_IS_NAMED_BUT_NEVER_TAUGHT)


# --------------------------------------------------------------------------
# §29.2.1 Ishkavala and §29.2.2 Induvara
# --------------------------------------------------------------------------


def test_both_rules_are_transcribed_with_their_results():
    assert "apoklimas (3rd, 6th, 9th and 12th houses) are empty" in (
        yogas.ISHKAVALA_RULE)
    assert "wealth, happiness and good fortune" in yogas.ISHKAVALA_RULE
    assert "occupy only apoklimas" in yogas.INDUVARA_RULE
    assert "disappointments, worries and illnesses" in yogas.INDUVARA_RULE
    assert yogas.ISHKAVALA_RESULTS in yogas.ISHKAVALA_RULE
    assert yogas.INDUVARA_RESULTS in yogas.INDUVARA_RULE


def test_the_three_house_groups_match_chapter_7s():
    """§29.2 restates §7.4's groups house for house. If they had drifted the
    yogas would be reading a different chart from the rest of the book.
    """
    from hora.core.constants.house import APOKLIMA, KENDRA, PANAPHARA

    assert KENDRA == (1, 4, 7, 10)
    assert PANAPHARA == (2, 5, 8, 11)
    assert APOKLIMA == (3, 6, 9, 12)
    assert sorted(KENDRA + PANAPHARA + APOKLIMA) == list(range(1, 13))


def test_ishkavala_is_present_when_no_apoklima_is_occupied():
    assert yogas.ishkavala([1, 4, 7, 10])["present"] is True
    assert yogas.ishkavala([2, 5, 8, 11])["present"] is True
    assert yogas.ishkavala([1, 2, 4, 5, 7, 8, 10, 11])["present"] is True
    for spoiler in (3, 6, 9, 12):
        assert yogas.ishkavala([1, 4, spoiler])["present"] is False


def test_induvara_is_present_when_only_apoklimas_are_occupied():
    assert yogas.induvara([3, 6, 9, 12])["present"] is True
    assert yogas.induvara([3])["present"] is True
    for spoiler in (1, 2, 4, 5, 7, 8, 10, 11):
        assert yogas.induvara([3, 6, spoiler])["present"] is False


def test_an_empty_chart_gives_neither_yoga():
    """"If planets occupy only X" needs a planet to occupy something."""
    assert yogas.ishkavala([])["present"] is False
    assert yogas.induvara([])["present"] is False


def test_the_two_halves_of_each_rule_are_one_condition():
    """Over every non-empty subset of the twelve houses, "occupies only" and
    "the rest are empty" never disagree.
    """
    for size in range(1, 5):
        for houses in itertools.combinations(range(1, 13), size):
            ish = yogas.ishkavala(houses)
            assert (ish["occupies_only_kendras_and_panapharas"]
                    == ish["apoklimas_empty"])
            ind = yogas.induvara(houses)
            assert (ind["occupies_only_apoklimas"]
                    == ind["kendras_and_panapharas_empty"])
    assert "one condition" in yogas.THE_TWO_HALVES_OF_EACH_RULE_ARE_THE_SAME_TEST


def test_no_chart_has_both_yogas():
    for size in range(1, 6):
        for houses in itertools.combinations(range(1, 13), size):
            both = (yogas.ishkavala(houses)["present"]
                    and yogas.induvara(houses)["present"])
            assert not both
    assert "no chart has both" in (
        yogas.THE_TWO_YOGAS_ARE_OPPOSITE_ENDS_OF_ONE_TEST)


def test_house_groups_partitions_what_it_is_given():
    got = yogas.house_groups([1, 2, 3, 4, 3])
    assert got == {"kendra": (1, 4), "panaphara": (2,), "apoklima": (3,)}


def test_ishkavala_is_far_commoner_than_induvara_in_real_charts():
    """Eight houses against four. Measured, because the chapter presents the
    two as a matched pair and they are not one.
    """
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    random.seed(291)
    place = Place(name="x", latitude=19.0, longitude=73.0)
    settings = Settings(node_type=NodeType.MEAN)
    hits = {"ishkavala": 0, "induvara": 0}
    trials = 400
    for _ in range(trials):
        chart = compute_chart(
            from_local(random.randint(1900, 2050), random.randint(1, 12),
                       random.randint(1, 28), random.randint(0, 23),
                       random.randint(0, 59), 0.0, utc_offset_hours=5.5),
            place, settings)
        houses = [(int(chart.positions[g].longitude // 30) - chart.lagna_rasi)
                  % 12 + 1 for g in range(7)]
        hits["ishkavala"] += yogas.ishkavala(houses)["present"]
        hits["induvara"] += yogas.induvara(houses)["present"]

    # (2/3)^7 = 5.9% and (1/3)^7 = 0.046%: the house count is the whole story.
    assert 0.02 < hits["ishkavala"] / trials < 0.12
    assert hits["induvara"] <= 1
    assert "one chart in sixteen" in (
        yogas.ISHKAVALA_IS_ORDERS_OF_MAGNITUDE_COMMONER)


def test_which_bodies_count_is_left_open():
    """OI-159. The functions take houses, never a body list."""
    assert "without saying whether Rahu" in yogas.WHICH_BODIES_COUNT_IS_NOT_SAID


# --------------------------------------------------------------------------
# §29.2.3 Ithasala — footnote 83
# --------------------------------------------------------------------------


def test_the_ithasala_rule_and_its_results_are_transcribed():
    assert "less advanced in its rasi" in yogas.ITHASALA_RULE
    assert "applying aspect" in yogas.ITHASALA_RULE
    assert "naisargika karaka" in yogas.ITHASALA_RESULTS
    assert "lord of vivaha saham or Venus" in yogas.ITHASALA_RESULTS
    assert yogas.ITHASALA_REFERENCE_LORDS == (
        "lagna lord", "lord of the related house",
        "lord of the related saham", "the naisargika karaka")


def test_footnote_83s_order_is_transcribed_and_ranked():
    assert "Saturn, Rahu/Ketu, Jupiter, Mars, Sun, Venus, Mercury and Moon" in (
        yogas.SPEED_ORDER_FOOTNOTE)
    names = [tuple(str(Graha(g).name).title() for g in group)
             for group in yogas.SPEED_ORDER]
    assert names == [("Saturn",), ("Rahu", "Ketu"), ("Jupiter",), ("Mars",),
                     ("Sun",), ("Venus",), ("Mercury",), ("Moon",)]
    assert yogas.speed_rank(int(Graha.SATURN)) == 0
    assert yogas.speed_rank(int(Graha.MOON)) == 7
    assert yogas.speed_rank(int(Graha.RAHU)) == yogas.speed_rank(int(Graha.KETU))


def test_rahu_and_ketu_are_the_only_pair_the_footnote_cannot_rank():
    assert yogas.faster_of(int(Graha.RAHU), int(Graha.KETU)) is None
    assert len(yogas.pairs_in_speed_order()) == 35      # 36 pairs less that one
    for slower, faster in yogas.pairs_in_speed_order():
        assert yogas.speed_rank(slower) < yogas.speed_rank(faster)


def test_the_footnote_is_right_about_the_seven_and_wrong_about_the_nodes():
    """Mean daily motion, measured over thirty years of samples. D-81."""
    import statistics

    from hora.core.ephemeris import get_ephemeris
    from hora.core.settings import NodeType, Settings

    eph = get_ephemeris(Settings(node_type=NodeType.MEAN))
    ids = list(range(9))
    speeds: dict[int, list[float]] = {g: [] for g in ids}
    for step in range(0, 11000, 60):
        for graha, position in eph.positions(2447893.0 + step, ids).items():
            speeds[graha].append(abs(position.speed_longitude))
    mean = {g: statistics.fmean(v) * 60 for g, v in speeds.items()}

    seven = [int(Graha.SATURN), int(Graha.JUPITER), int(Graha.MARS),
             int(Graha.SUN), int(Graha.VENUS), int(Graha.MERCURY),
             int(Graha.MOON)]
    # The footnote's order for the seven classical grahas is exactly right.
    assert seven == sorted(seven, key=lambda g: mean[g])
    assert [yogas.speed_rank(g) for g in seven] == sorted(
        yogas.speed_rank(g) for g in seven)

    # And exactly wrong for the nodes, which it puts above Saturn.
    assert mean[int(Graha.RAHU)] < mean[int(Graha.SATURN)]
    assert yogas.speed_rank(int(Graha.RAHU)) > yogas.speed_rank(
        int(Graha.SATURN))
    assert "not the second slowest" in (
        yogas.THE_NODES_ARE_THE_ONE_PLACE_THE_ORDER_IS_WRONG)


def test_the_fixed_order_and_the_true_speeds_disagree_often():
    """OI-160. 22 of the 36 pairs invert at some point."""
    from hora.core.ephemeris import get_ephemeris
    from hora.core.settings import NodeType, Settings

    eph = get_ephemeris(Settings(node_type=NodeType.MEAN))
    ids = list(range(9))
    speeds: dict[int, list[float]] = {g: [] for g in ids}
    for step in range(0, 11000, 30):
        for graha, position in eph.positions(2447893.0 + step, ids).items():
            speeds[graha].append(abs(position.speed_longitude))
    samples = len(speeds[0])

    inverting = 0
    for slower, faster in yogas.pairs_in_speed_order():
        if any(speeds[slower][i] > speeds[faster][i] for i in range(samples)):
            inverting += 1
    # 35 rankable pairs; the Rahu-Ketu pair the footnote ties is not among
    # them and never inverts anyway.
    assert inverting == 22
    assert "22 of the 36 pairs invert" in (
        yogas.THE_SPEED_ORDER_IS_A_LIST_NOT_A_MEASUREMENT)


# --------------------------------------------------------------------------
# §29.2.3 Ithasala — the yoga itself
# --------------------------------------------------------------------------


def test_advancement_is_the_degree_within_the_rasi():
    assert yogas.advancement(180 + 13) == pytest.approx(13.0)
    assert yogas.advancement(29.5) == pytest.approx(29.5)
    assert yogas.advancement(30.0) == pytest.approx(0.0)
    assert "not a comparison of longitudes" in (
        yogas.ADVANCEMENT_IS_WITHIN_THE_RASI)


def test_advancement_and_longitude_disagree_across_a_sign_boundary():
    """2° of Taurus is less advanced than 25° of Aries and ahead of it."""
    early, late = 30.0 + 2.0, 25.0
    assert early > late
    assert yogas.advancement(early) < yogas.advancement(late)


def test_a_worked_ithasala():
    """Venus at 13 Li and Jupiter at 20 Ge: a trinal aspect, and Venus, the
    faster, is less advanced in his rasi. Applying.
    """
    got = yogas.ithasala(faster=int(Graha.VENUS), slower=int(Graha.JUPITER),
                         faster_longitude=180 + 13, slower_longitude=60 + 20)
    assert got["faster_name"] == "Venus" and got["slower_name"] == "Jupiter"
    assert got["house_from_faster"] == 9
    assert got["aspect"] == "Trinal aspect"
    assert got["faster_is_less_advanced"] is True
    assert got["present_by_house"] is True
    assert got["present_within_orb"] is True


def test_the_same_pair_separating_is_not_an_ithasala():
    """Venus at 25 Li, Jupiter at 20 Ge: the aspect is the same and Venus is
    now past it.
    """
    got = yogas.ithasala(faster=int(Graha.VENUS), slower=int(Graha.JUPITER),
                         faster_longitude=180 + 25, slower_longitude=60 + 20)
    assert got["aspects_by_house"] is True
    assert got["faster_is_less_advanced"] is False
    assert got["present_by_house"] is False


def test_the_caller_cannot_invert_the_yoga_by_swapping_the_arguments():
    """Footnote 83 decides which planet is the faster, not the caller."""
    right = yogas.ithasala(faster=int(Graha.MOON), slower=int(Graha.SATURN),
                           faster_longitude=5.0, slower_longitude=100.0)
    wrong = yogas.ithasala(faster=int(Graha.SATURN), slower=int(Graha.MOON),
                           faster_longitude=100.0, slower_longitude=5.0)
    assert right["caller_had_them_the_right_way_round"] is True
    assert wrong["caller_had_them_the_right_way_round"] is False
    for key in ("faster", "slower", "faster_advancement", "slower_advancement",
                "faster_is_less_advanced", "present_by_house"):
        assert right[key] == wrong[key]


def test_the_sixth_and_eighth_houses_carry_no_aspect_so_no_ithasala():
    """§28.2 gives them none, and §29.2.3 needs an aspect."""
    for house in (6, 8):
        got = yogas.ithasala(
            faster=int(Graha.MOON), slower=int(Graha.SATURN),
            faster_longitude=5.0, slower_longitude=(house - 1) * 30.0 + 20.0)
        assert got["house_from_faster"] == house
        assert got["aspect"] is None
        assert got["aspects_by_house"] is False
        assert got["present_by_house"] is False


def test_the_orb_and_the_advancement_are_the_same_number():
    """Whole-sign aspects, so the separation from exact is the difference of
    the two advancements. Checked over three thousand random pairs.
    """
    random.seed(29)
    for _ in range(3000):
        a, b = random.sample(range(7), 2)
        got = yogas.ithasala(faster=a, slower=b,
                             faster_longitude=random.uniform(0, 360),
                             slower_longitude=random.uniform(0, 360))
        assert got["separation_from_exact"] == pytest.approx(
            abs(got["slower_advancement"] - got["faster_advancement"]),
            abs=1e-9)
    assert "equals the difference between the two planets' degrees" in (
        yogas.THE_ORB_AND_THE_ADVANCEMENT_ARE_ONE_NUMBER)


def test_the_two_deeptamsas_are_both_answered_and_neither_is_summed():
    """Venus's orb is 7° and Jupiter's 9°, so a separation of 8° is inside
    one and outside the other. The example requires both, so the yoga is
    absent — but the caller is still shown each answer.
    """
    got = yogas.ithasala(faster=int(Graha.VENUS), slower=int(Graha.JUPITER),
                         faster_longitude=180 + 13, slower_longitude=60 + 21)
    assert got["separation_from_exact"] == pytest.approx(8.0)
    assert got["deeptamsa_of_faster"] == 7.0
    assert got["deeptamsa_of_slower"] == 9.0
    assert got["aspects_within_faster_deeptamsa"] is False
    assert got["aspects_within_slower_deeptamsa"] is True
    assert got["deeptamsas_agree"] is False
    assert got["present_within_orb"] is False
    assert "both must hold" in yogas.WHOSE_DEEPTAMSA_GOVERNS_IS_NOT_SAID


def test_an_ithasala_with_a_node_has_no_orb_to_be_tested_against():
    """Footnote 83 ranks the nodes; §28.2 gives them no deeptamsa."""
    got = yogas.ithasala(faster=int(Graha.RAHU), slower=int(Graha.SATURN),
                         faster_longitude=5.0, slower_longitude=100.0)
    assert got["aspects_by_house"] is True
    assert got["present_by_house"] is True
    assert got["aspects_within_faster_deeptamsa"] is None
    assert got["present_within_orb"] is None
    assert "no deeptamsa" in yogas.A_NODES_ITHASALA_CANNOT_BE_ORBED


def test_ithasala_rejects_a_pair_it_cannot_rank_or_a_graha_with_itself():
    with pytest.raises(yogas.TajakaYogaError, match="two different grahas"):
        yogas.ithasala(faster=int(Graha.SUN), slower=int(Graha.SUN),
                       faster_longitude=1.0, slower_longitude=2.0)
    with pytest.raises(yogas.TajakaYogaError, match="neither is the faster"):
        yogas.ithasala(faster=int(Graha.RAHU), slower=int(Graha.KETU),
                       faster_longitude=1.0, slower_longitude=2.0)


def test_the_marriage_example_is_the_third_rule_for_one_event():
    """§25.3, §28.8.2 and now §29.2.3 all read a marriage against vivaha
    saham, and no two of them agree.
    """
    from hora.tajaka.saham_use import NATAL_SAHAM_TRANSITS
    from hora.transits.gochara import SAHAM_TRANSIT_EXAMPLES

    assert any(row["saham"] == "vivaha" for row in SAHAM_TRANSIT_EXAMPLES)
    assert any("Vivaha" in row["sahams"] for row in NATAL_SAHAM_TRANSITS)
    assert yogas.ITHASALA_MARRIAGE_EXAMPLE["matter"] == "marriage"
    assert "the lord of vivaha saham" in (
        yogas.ITHASALA_MARRIAGE_EXAMPLE["other_side"])
    # This one reads the saham's lord, where the other two read the point.
    assert "with its lord" in yogas.A_THIRD_RULE_FOR_THE_SAME_MARRIAGE


# --------------------------------------------------------------------------
# §29.2.3's worked example
# --------------------------------------------------------------------------


def test_the_ithasala_example_reproduces_on_all_four_claims():
    """Moon 14 Le, Venus 19 Li. Sextile; both inside the other's orb;
    advancements 14 and 19; the Moon the faster. Ithasala.
    """
    want = yogas.ITHASALA_EXAMPLE
    got = yogas.ithasala(
        faster=int(Graha.MOON), slower=int(Graha.VENUS),
        faster_longitude=float(want["faster_longitude"]),
        slower_longitude=float(want["slower_longitude"]))

    assert got["faster_name"] == want["faster"]
    assert got["slower_name"] == want["slower"]
    assert got["aspect"] == want["aspect"]
    assert got["faster_advancement"] == pytest.approx(
        want["faster_advancement"])
    assert got["slower_advancement"] == pytest.approx(
        want["slower_advancement"])
    assert got["aspects_within_faster_deeptamsa"] is True
    assert got["aspects_within_slower_deeptamsa"] is True
    assert got["faster_is_less_advanced"] is True
    assert got["present_within_orb"] is want["present"]
    assert "All four reproduce" not in yogas.ITHASALA_RULE
    assert "The yoga is present" in yogas.THE_EXAMPLE_CHECKS_OUT_ON_ALL_FOUR_CLAIMS


def test_the_examples_longitudes_are_where_the_book_puts_them():
    from hora.core.const import RASI_ABBR

    want = yogas.ITHASALA_EXAMPLE
    for key, printed in (("faster_longitude", "14 Le"),
                         ("slower_longitude", "19 Li")):
        value = float(want[key])
        degree, rasi = printed.split()
        assert int(value % 30) == int(degree)
        assert RASI_ABBR[int(value // 30)] == rasi


def test_the_example_settles_whose_deeptamsa_governs():
    """"Both the planets are within the deeptaamsa (orb) of the other."
    Both, so the smaller of the two governs. OI-161, narrowed.
    """
    assert yogas.ITHASALA_EXAMPLE["both_within_the_others_orb"] is True
    assert "both must hold and" in yogas.WHOSE_DEEPTAMSA_GOVERNS_IS_NOT_SAID
    assert "smaller of the two deeptamsas" in yogas.THE_SMALLER_DEEPTAMSA_GOVERNS

    # 8° apart: inside Jupiter's 9° and outside Venus's 7°, so not an
    # ithasala under the example's reading, whichever way it is put.
    from hora.tajaka.aspects import deeptamsa

    near = yogas.ithasala(faster=int(Graha.VENUS), slower=int(Graha.JUPITER),
                          faster_longitude=180 + 13, slower_longitude=60 + 21)
    assert near["separation_from_exact"] == pytest.approx(8.0)
    assert near["present_by_house"] is True
    assert near["present_within_orb"] is False
    assert min(deeptamsa(int(Graha.VENUS)),
               deeptamsa(int(Graha.JUPITER))) == 7.0


def test_the_example_settles_that_the_orb_is_required():
    """The rule says only "have an aspect". The example checks the orb before
    declaring the yoga.
    """
    assert "so it is required" in (
        yogas.WHETHER_THE_ASPECT_NEEDS_THE_ORB_IS_NOT_SAID)
    # And the two readings do come apart: a wide separation aspects by house
    # and fails the orb.
    wide = yogas.ithasala(faster=int(Graha.MERCURY), slower=int(Graha.SATURN),
                          faster_longitude=1.0, slower_longitude=60 + 25.0)
    assert wide["aspects_by_house"] is True
    assert wide["faster_is_less_advanced"] is True
    assert wide["present_by_house"] is True
    assert wide["present_within_orb"] is False


def test_only_the_node_hole_is_left_in_the_orb_rule():
    """Two of OI-161's three holes are closed by the example. §28.2 still
    gives Rahu and Ketu no deeptamsa.
    """
    got = yogas.ithasala(faster=int(Graha.RAHU), slower=int(Graha.SATURN),
                         faster_longitude=5.0, slower_longitude=100.0)
    assert got["present_by_house"] is True
    assert got["present_within_orb"] is None
    assert got["deeptamsa_of_faster"] is None
    assert got["undecided"] == yogas.A_NODES_ITHASALA_CANNOT_BE_ORBED


# --------------------------------------------------------------------------
# §29.2.3 — the three types of ithasala
# --------------------------------------------------------------------------


def test_the_three_types_are_transcribed_with_their_meanings():
    names = [row["name"] for row in yogas.ITHASALA_TYPES]
    assert names == ["Vartamaana", "Poorna", "Bhavishya"]
    means = [row["means"] for row in yogas.ITHASALA_TYPES]
    assert means == ["present (current)", "complete", "future"]
    assert "within the deeptaamsa (orb) of the other" in (
        yogas.ITHASALA_TYPES[0]["rule"])
    assert "within 1 degree of each other" in yogas.ITHASALA_TYPES[1]["rule"]
    assert "speedy fulfillment" in yogas.ITHASALA_TYPES[1]["gives"]
    assert "is about to be formed" in yogas.ITHASALA_TYPES[2]["rule"]
    assert "obstructions or delay" in yogas.ITHASALA_TYPES[2]["gives"]
    assert yogas.POORNA_DEGREES == yogas.BHAVISHYA_DEGREES == 1.0


def test_the_three_worked_cases_reproduce():
    """One pair, three separations, three types. Every number the book prints
    comes back, including the 0°45' it computes by hand for bhavishya.
    """
    for want in yogas.ITHASALA_TYPE_EXAMPLES:
        got = yogas.ithasala(
            faster=int(Graha.MOON), slower=int(Graha.VENUS),
            faster_longitude=float(want["moon_longitude"]),
            slower_longitude=float(want["venus_longitude"]))
        assert got["type"] == want["type"], want["type"]
        assert got["separation_from_exact"] == pytest.approx(
            float(want["separation"]), abs=1e-9), want["type"]
        if "degrees_to_vartamaana" in want:
            assert got["degrees_to_vartamaana"] == pytest.approx(
                float(want["degrees_to_vartamaana"]), abs=1e-9)
    assert "three types" in yogas.THE_THREE_TYPE_EXAMPLES_REPRODUCE


def test_the_deeptamsa_windows_the_book_prints_come_back():
    """Venus at 19° gives 12° to 26°; the Moon at 13°35' gives 1°35' to
    25°35'; Venus at 21°20' gives 14°20' to 28°20'.
    """
    from hora.tajaka.aspects import aspect_span

    venus_at_19 = aspect_span(int(Graha.VENUS), 180.0 + 19.0, 11)
    assert venus_at_19["from"] % 30 == pytest.approx(12.0)
    assert venus_at_19["to"] % 30 == pytest.approx(26.0)

    moon_at_13_35 = aspect_span(int(Graha.MOON), 120.0 + 13.0 + 35 / 60, 3)
    assert moon_at_13_35["from"] % 30 == pytest.approx(1 + 35 / 60)
    assert moon_at_13_35["to"] % 30 == pytest.approx(25 + 35 / 60)

    venus_at_21_20 = aspect_span(int(Graha.VENUS), 180.0 + 21.0 + 20 / 60, 11)
    assert venus_at_21_20["from"] % 30 == pytest.approx(14 + 20 / 60)
    assert venus_at_21_20["to"] % 30 == pytest.approx(28 + 20 / 60)


def test_vartamaana_is_the_orb_test_already_built():
    """(i) restates §29.2.3's own rule, so the two must agree in every chart.
    """
    random.seed(2923)
    for _ in range(2000):
        a, b = random.sample(range(7), 2)
        got = yogas.ithasala(faster=a, slower=b,
                             faster_longitude=random.uniform(0, 360),
                             slower_longitude=random.uniform(0, 360))
        assert got["vartamaana"] == got["present_within_orb"]


def test_every_poorna_is_also_a_vartamaana():
    """1° against a smallest deeptamsa of 7°, so poorna nests inside."""
    from hora.tajaka.aspects import DEEPTAMSA

    assert min(DEEPTAMSA.values()) > yogas.POORNA_DEGREES

    random.seed(2924)
    poornas = 0
    for _ in range(4000):
        a, b = random.sample(range(7), 2)
        got = yogas.ithasala(faster=a, slower=b,
                             faster_longitude=random.uniform(0, 360),
                             slower_longitude=random.uniform(0, 360))
        if got["poorna"]:
            poornas += 1
            assert got["vartamaana"] is True
            assert got["type"] == "Poorna"
    assert poornas > 20
    assert "every poorna ithasala is also a" in (
        yogas.POORNA_IS_A_KIND_OF_VARTAMAANA)


def test_bhavishya_excludes_the_other_two():
    random.seed(2925)
    for _ in range(4000):
        a, b = random.sample(range(7), 2)
        got = yogas.ithasala(faster=a, slower=b,
                             faster_longitude=random.uniform(0, 360),
                             slower_longitude=random.uniform(0, 360))
        if got["bhavishya"]:
            assert got["vartamaana"] is False and got["poorna"] is False
            assert got["type"] == "Bhavishya"
            assert 0 < got["degrees_to_vartamaana"] <= 1.0


def test_all_three_types_are_one_subtraction():
    """The separation against the smaller deeptamsa decides everything."""
    random.seed(2926)
    for _ in range(3000):
        a, b = random.sample(range(7), 2)
        got = yogas.ithasala(faster=a, slower=b,
                             faster_longitude=random.uniform(0, 360),
                             slower_longitude=random.uniform(0, 360))
        if not got["aspects_by_house"] or not got["faster_is_less_advanced"]:
            assert got["type"] is None
            continue
        gap, orb = got["separation_from_exact"], got["binding_deeptamsa"]
        assert got["vartamaana"] == (gap <= orb)
        assert got["poorna"] == (gap <= 1.0)
        assert got["bhavishya"] == (orb < gap <= orb + 1.0)
    assert "smaller deeptamsa" in yogas.ALL_THREE_TYPES_READ_ONE_SEPARATION


def test_the_binding_orb_is_the_smaller_of_the_two():
    got = yogas.ithasala(faster=int(Graha.MOON), slower=int(Graha.VENUS),
                         faster_longitude=134.0, slower_longitude=199.0)
    assert got["deeptamsa_of_faster"] == 12.0
    assert got["deeptamsa_of_slower"] == 7.0
    assert got["binding_deeptamsa"] == 7.0


def test_a_separating_pair_has_no_type_at_all():
    """None of the three survives the faster planet being ahead."""
    got = yogas.ithasala(faster=int(Graha.MOON), slower=int(Graha.VENUS),
                         faster_longitude=120.0 + 25.0, slower_longitude=199.0)
    assert got["faster_is_less_advanced"] is False
    assert got["type"] is None
    assert (got["vartamaana"], got["poorna"], got["bhavishya"]) == (
        False, False, False)


def test_a_bhavishya_can_never_reach_the_end_of_a_rasi():
    """The obvious worry — the faster planet changing sign as it advances,
    taking the whole-sign aspect with it — cannot arise. A bhavishya needs a
    separation above the binding orb, so the faster planet is below 23° of
    its rasi and a further degree leaves it below 24°.
    """
    from hora.tajaka.aspects import DEEPTAMSA

    smallest = min(DEEPTAMSA.values())
    assert smallest == 7.0

    random.seed(2927)
    seen = 0
    for _ in range(6000):
        a, b = random.sample(range(7), 2)
        got = yogas.ithasala(faster=a, slower=b,
                             faster_longitude=random.uniform(0, 360),
                             slower_longitude=random.uniform(0, 360))
        if got["degrees_to_vartamaana"] is not None:
            assert got["bhavishya_crosses_a_rasi"] is False
        if got["bhavishya"]:
            seen += 1
            assert got["faster_advancement"] < 30.0 - smallest
    assert seen > 20
    assert "cannot take it out of the sign" in (
        yogas.BHAVISHYA_CANNOT_REACH_THE_END_OF_A_RASI)


def test_the_bhavishya_example_swaps_two_rasi_names():
    """Venus is put in Le where the arithmetic needs Li, and his window in Li
    where it needs Le. Both are checkable from the numbers.
    """
    from hora.tajaka.aspects import aspect_on_house

    # If Venus were in Le with the Moon the aspect would be a conjunction,
    # not the sextile the paragraph names.
    assert aspect_on_house(1)["name"] == "Conjunction"
    assert aspect_on_house(3)["name"] == "Sextile aspect"

    bhavishya = yogas.ITHASALA_TYPE_EXAMPLES[2]
    assert bhavishya["venus"] == "21 Li 20"
    assert int(float(bhavishya["venus_longitude"]) // 30) == 6      # Libra
    assert int(float(bhavishya["moon_longitude"]) // 30) == 4       # Leo
    assert "Le for Li, then Li for Le" not in yogas.ITHASALA_RULE
    assert "the two rasi names are exchanged" in (
        yogas.THE_BHAVISHYA_EXAMPLE_SWAPS_TWO_RASI_NAMES)


# --------------------------------------------------------------------------
# §29.2.3's Special Notes — retrogression
# --------------------------------------------------------------------------

_RASI = {"Ar": 0, "Ta": 1, "Ge": 2, "Cn": 3, "Le": 4, "Vi": 5,
         "Li": 6, "Sc": 7, "Sg": 8, "Cp": 9, "Aq": 10, "Pi": 11}
_GRAHA = {"Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
          "Mercury": Graha.MERCURY, "Jupiter": Graha.JUPITER,
          "Venus": Graha.VENUS, "Saturn": Graha.SATURN}


def _longitude(printed: str) -> float:
    """"18 Li 10" -> 198.1666..."""
    parts = printed.split()
    minutes = float(parts[2]) / 60.0 if len(parts) > 2 else 0.0
    return _RASI[parts[1]] * 30.0 + float(parts[0]) + minutes


def test_the_special_notes_restate_the_criterion():
    assert "reach the same advancement in their rasis" in yogas.THE_REAL_CRITERION
    assert "sookshma drishti" in yogas.THE_REAL_CRITERION
    assert yogas.SOOKSHMA_DRISHTI == "sookshma drishti"
    assert "retrograde or about to become retrograde" in (
        yogas.ADAPT_THE_RULES_UNDER_RETROGRESSION)


def test_all_four_retrogression_cases_give_the_books_verdict():
    for case in yogas.RETROGRESSION_CASES:
        got = yogas.ithasala(
            faster=int(_GRAHA[str(case["faster"])]),
            slower=int(_GRAHA[str(case["slower"])]),
            faster_longitude=_longitude(str(case["faster_at"])),
            slower_longitude=_longitude(str(case["slower_at"])),
            faster_retrograde=bool(case["faster_retrograde"]),
            slower_retrograde=bool(case["slower_retrograde"]),
            faster_stations_at=case.get("stations_at"))
        assert got["approaching"] is case["has_ithasala"], case["case"]
        assert (got["type"] is not None) is case["has_ithasala"], case["case"]


def test_the_three_named_aspects_in_the_special_notes_are_right():
    """The section names a trinal aspect three times and it is one each
    time: Ge to Li, Vi to Cp, and Vi to Cp again.
    """
    for faster_at, slower_at in (("18 Ge", "18 Li 10"),
                                 ("23 Vi", "21 Cp"),
                                 ("18 Vi", "18 Cp 45")):
        got = yogas.ithasala(
            faster=int(Graha.MERCURY), slower=int(Graha.MARS),
            faster_longitude=_longitude(faster_at),
            slower_longitude=_longitude(slower_at))
        assert got["aspect"] == "Trinal aspect", (faster_at, slower_at)


def test_a_retrograde_faster_planet_behind_is_not_an_ithasala():
    """The section's sharpest case: 10 arcminutes apart in a trinal aspect,
    which reads as a textbook poorna and is failure.
    """
    direct = yogas.ithasala(faster=int(Graha.MERCURY), slower=int(Graha.MARS),
                            faster_longitude=_longitude("18 Ge"),
                            slower_longitude=_longitude("18 Li 10"))
    assert direct["type"] == "Poorna"
    assert direct["separation_from_exact"] == pytest.approx(10 / 60)

    retro = yogas.ithasala(faster=int(Graha.MERCURY), slower=int(Graha.MARS),
                           faster_longitude=_longitude("18 Ge"),
                           slower_longitude=_longitude("18 Li 10"),
                           faster_retrograde=True)
    assert retro["faster_is_less_advanced"] is True
    assert retro["converging"] is False
    assert retro["type"] is None
    assert (retro["vartamaana"], retro["poorna"], retro["bhavishya"]) == (
        False, False, False)
    assert "dogged with failure" in str(yogas.RETROGRESSION_CASES[0]["book_says"])
    assert "the more convincing the false reading" in (
        yogas.A_TIGHT_DIFFERENCE_CAN_BE_THE_WORST_CASE)


def test_a_retrograde_faster_planet_ahead_is_an_ithasala():
    """Mars 21 Cp, retrograde Mercury 23 Vi. The faster planet is more
    advanced and they still converge, near 22°.
    """
    got = yogas.ithasala(faster=int(Graha.MERCURY), slower=int(Graha.MARS),
                         faster_longitude=_longitude("23 Vi"),
                         slower_longitude=_longitude("21 Cp"),
                         faster_retrograde=True)
    assert got["faster_is_less_advanced"] is False
    assert got["converging"] is True
    assert got["type"] == "Vartamaana"
    assert got["separation_from_exact"] == pytest.approx(2.0)


def test_a_retrograde_slower_planet_changes_nothing_but_the_speed():
    """Moon 18 Ar, retrograde Mercury 24 Ge. The verdict is the same either
    way; the section's point is that it happens sooner.
    """
    kwargs = {"faster": int(Graha.MOON), "slower": int(Graha.MERCURY),
              "faster_longitude": _longitude("18 Ar"),
              "slower_longitude": _longitude("24 Ge")}
    retro = yogas.ithasala(**kwargs, slower_retrograde=True)
    direct = yogas.ithasala(**kwargs)
    assert retro["converging"] is direct["converging"] is True
    assert retro["type"] == direct["type"] == "Vartamaana"
    assert retro["slower_retrograde"] is True
    assert "faster realization" in str(yogas.RETROGRESSION_CASES[1]["book_says"])


def test_only_the_faster_planets_direction_decides_convergence():
    """The whole retrogression rule in one clause, over every combination."""
    for faster_behind in (True, False):
        for faster_retro in (True, False):
            for slower_retro in (True, False):
                # 10° apart either way, in a sextile.
                faster_at = 4.0 if faster_behind else 14.0
                slower_at = 74.0 if faster_behind else 64.0
                got = yogas.ithasala(
                    faster=int(Graha.MOON), slower=int(Graha.SATURN),
                    faster_longitude=faster_at, slower_longitude=slower_at,
                    faster_retrograde=faster_retro,
                    slower_retrograde=slower_retro)
                assert got["faster_is_less_advanced"] is faster_behind
                assert got["converging"] is (faster_behind != faster_retro)
    assert "The slower planet's direction changes only how soon" in (
        yogas.ONLY_THE_FASTER_PLANETS_DIRECTION_DECIDES)


def test_both_retrograde_is_answered_by_the_same_clause():
    """The section never works it. The argument extends unchanged."""
    behind = yogas.ithasala(faster=int(Graha.MERCURY), slower=int(Graha.SATURN),
                            faster_longitude=4.0, slower_longitude=74.0,
                            faster_retrograde=True, slower_retrograde=True)
    ahead = yogas.ithasala(faster=int(Graha.MERCURY), slower=int(Graha.SATURN),
                           faster_longitude=14.0, slower_longitude=64.0,
                           faster_retrograde=True, slower_retrograde=True)
    assert behind["converging"] is False
    assert ahead["converging"] is True
    assert "never both at once" in yogas.BOTH_RETROGRADE_IS_NOT_WORKED


def test_a_planet_that_stations_first_never_reaches_the_meeting():
    """Mercury 18 Vi, Mars 18°45' Cp, neither retrograde: a poorna on the
    numbers. Mercury turns back at 18°05'.
    """
    kwargs = {"faster": int(Graha.MERCURY), "slower": int(Graha.MARS),
              "faster_longitude": _longitude("18 Vi"),
              "slower_longitude": _longitude("18 Cp 45")}
    unaware = yogas.ithasala(**kwargs)
    assert unaware["type"] == "Poorna"
    assert unaware["separation_from_exact"] == pytest.approx(45 / 60)

    aware = yogas.ithasala(**kwargs, faster_stations_at=18.0 + 5.0 / 60.0)
    assert aware["converging"] is True
    assert aware["stationed_before_the_meeting"] is True
    assert aware["approaching"] is False
    assert aware["type"] is None

    # A station beyond the slower planet does not block anything.
    later = yogas.ithasala(**kwargs, faster_stations_at=25.0)
    assert later["stationed_before_the_meeting"] is False
    assert later["type"] == "Poorna"


def test_the_station_test_works_backwards_for_a_retrograde_faster_planet():
    kwargs = {"faster": int(Graha.MERCURY), "slower": int(Graha.MARS),
              "faster_longitude": _longitude("23 Vi"),
              "slower_longitude": _longitude("21 Cp"),
              "faster_retrograde": True}
    blocked = yogas.ithasala(**kwargs, faster_stations_at=22.0)
    assert blocked["stationed_before_the_meeting"] is True
    assert blocked["type"] is None
    clear = yogas.ithasala(**kwargs, faster_stations_at=15.0)
    assert clear["stationed_before_the_meeting"] is False
    assert clear["type"] == "Vartamaana"


def test_a_station_outside_a_rasi_is_rejected():
    for bad in (-1.0, 30.0, 45.0):
        with pytest.raises(yogas.TajakaYogaError, match="advancement in a rasi"):
            yogas.ithasala(faster=int(Graha.MOON), slower=int(Graha.SATURN),
                           faster_longitude=4.0, slower_longitude=64.0,
                           faster_stations_at=bad)


def test_the_defaults_leave_the_earlier_rule_untouched():
    """Both flags default to direct, so everything built before the Special
    Notes answers exactly as it did.
    """
    random.seed(2928)
    for _ in range(2000):
        a, b = random.sample(range(7), 2)
        got = yogas.ithasala(faster=a, slower=b,
                             faster_longitude=random.uniform(0, 360),
                             slower_longitude=random.uniform(0, 360))
        assert got["faster_retrograde"] is False
        assert got["slower_retrograde"] is False
        assert got["converging"] is got["faster_is_less_advanced"]
        assert got["approaching"] is got["faster_is_less_advanced"]


def test_the_narrower_window_under_retrogression_has_no_figure():
    """OI-162. The thresholds are left at one degree and the flag says so."""
    got = yogas.ithasala(faster=int(Graha.MERCURY), slower=int(Graha.MARS),
                         faster_longitude=_longitude("23 Vi"),
                         slower_longitude=_longitude("21 Cp"),
                         faster_retrograde=True)
    assert got["retrogression_narrows_the_window"] is not None
    assert "gives no figure" in yogas.RETROGRESSION_NARROWS_THE_WINDOW
    assert yogas.POORNA_DEGREES == 1.0

    direct = yogas.ithasala(faster=int(Graha.MERCURY), slower=int(Graha.MARS),
                            faster_longitude=_longitude("23 Vi"),
                            slower_longitude=_longitude("21 Cp"))
    assert direct["retrogression_narrows_the_window"] is None


# --------------------------------------------------------------------------
# §29.2.4 Eesarpha yoga
# --------------------------------------------------------------------------


def test_the_eesarpha_rule_and_results_are_transcribed():
    assert "opposite of ithasala" in yogas.EESARPHA_RULE
    assert "higher advancement in its rasi" in yogas.EESARPHA_RULE
    assert "failures and disappointments" in yogas.EESARPHA_RESULTS
    assert "president or prime minister or king" in yogas.EESARPHA_RESULTS
    assert "We have an ithasala yoga instead" in yogas.EESARPHA_SPECIAL_NOTES


def test_the_two_readings_are_data():
    matters = [row["matter"] for row in yogas.EESARPHA_READINGS]
    assert matters == ["children", "loss of power"]
    assert yogas.EESARPHA_READINGS[0]["other_side"] == (
        "the 5th lord", "the putra saham lord", "Jupiter")
    assert yogas.EESARPHA_READINGS[1]["only_for"] == (
        "a president or prime minister or king")
    for row in yogas.EESARPHA_READINGS:
        assert row["one_side"] == "lagna lord"
        assert str(row["shows"]) in yogas.EESARPHA_RESULTS


def test_both_sahams_the_results_name_are_in_table_74():
    """Putra saham and raajya saham — 13 and 11."""
    from hora.tajaka.sahams import TABLE_74_SAHAMS

    numbers = {str(row["name"]): row["number"] for row in TABLE_74_SAHAMS}
    assert numbers["Putra"] == 13
    assert numbers["Rajya"] == 11


def test_the_fifth_lord_appears_in_both_readings():
    first, second = yogas.EESARPHA_READINGS
    assert "the 5th lord" in first["other_side"]
    assert "the 5th lord" in second["other_side"]
    shared = set(first["other_side"]) & set(second["other_side"])
    assert shared == {"the 5th lord"}
    assert "the only reference in either list to appear twice" in (
        yogas.THE_FIFTH_LORD_IS_IN_BOTH_READINGS)


def test_the_eesarpha_example_reproduces():
    """Moon 23 Le, Venus 19 Li: a sextile, both inside the other's orb, and
    the Moon the more advanced.
    """
    want = yogas.EESARPHA_EXAMPLE
    got = yogas.eesarpha(
        faster=int(Graha.MOON), slower=int(Graha.VENUS),
        faster_longitude=float(want["faster_longitude"]),
        slower_longitude=float(want["slower_longitude"]))
    assert got["aspect"] == want["aspect"]
    assert got["faster_advancement"] == pytest.approx(
        float(want["faster_advancement"]))
    assert got["slower_advancement"] == pytest.approx(
        float(want["slower_advancement"]))
    assert got["faster_is_more_advanced"] is True
    assert got["separation_from_exact"] == pytest.approx(4.0)
    assert got["present_within_orb"] is want["present"]
    assert got["ithasala_instead"] is None


def test_the_example_is_29_2_3s_example_with_the_moon_moved_on():
    """Same pair, same aspect, same orbs — the Moon at 23° instead of 14°."""
    ith = yogas.ITHASALA_EXAMPLE
    ees = yogas.EESARPHA_EXAMPLE
    assert ees["slower_longitude"] == ith["slower_longitude"]
    assert ees["aspect"] == ith["aspect"]
    assert float(ees["faster_longitude"]) - float(ith["faster_longitude"]) == 9.0


def test_all_four_special_note_cases_come_out_right():
    """Retrograde and less advanced is eesarpha; retrograde and more advanced
    is ithasala instead. Both directions of both flags.
    """
    cases = ((True, True, "eesarpha"), (True, False, "ithasala"),
             (False, False, "eesarpha"), (False, True, "ithasala"))
    for retrograde, behind, want in cases:
        faster_at = 4.0 if behind else 9.0
        slower_at = 69.0 if behind else 64.0       # 5° apart, inside both orbs
        got = yogas.eesarpha(
            faster=int(Graha.MOON), slower=int(Graha.SATURN),
            faster_longitude=faster_at, slower_longitude=slower_at,
            faster_retrograde=retrograde)
        other = yogas.ithasala(
            faster=int(Graha.MOON), slower=int(Graha.SATURN),
            faster_longitude=faster_at, slower_longitude=slower_at,
            faster_retrograde=retrograde)
        if want == "eesarpha":
            assert got["present_within_orb"] is True, (retrograde, behind)
            assert other["type"] is None, (retrograde, behind)
        else:
            assert got["present_within_orb"] is False, (retrograde, behind)
            assert other["type"] is not None, (retrograde, behind)
            assert got["ithasala_instead"] == other["type"]


def test_eesarpha_is_the_negation_of_ithasalas_clause():
    """Over random pairs: given an aspect and unequal advancements, exactly
    one of the two yogas holds by house, whatever the flags.
    """
    random.seed(2941)
    both = neither = 0
    for _ in range(4000):
        a, b = random.sample(range(7), 2)
        kwargs = {"faster": a, "slower": b,
                  "faster_longitude": random.uniform(0, 360),
                  "slower_longitude": random.uniform(0, 360),
                  "faster_retrograde": random.random() < 0.3,
                  "slower_retrograde": random.random() < 0.3}
        ith = yogas.ithasala(**kwargs)
        ees = yogas.eesarpha(**kwargs)
        if not ith["aspects_by_house"]:
            assert not ith["present_by_house"] and not ees["present_by_house"]
            continue
        both += ith["present_by_house"] and ees["present_by_house"]
        neither += not (ith["present_by_house"] or ees["present_by_house"])
    assert both == 0
    assert neither == 0          # equal advancements never come up at random
    assert "negation of ithasala's condition" in (
        yogas.EESARPHA_IS_THE_NEGATION_OF_THE_SAME_CLAUSE)


def test_the_exact_aspect_is_neither_yoga():
    """Equal advancements: the faster planet is neither less nor more
    advanced, so no definition reaches it — and that is the sookshma drishti
    an ithasala is heading towards. OI-163.
    """
    ith = yogas.ithasala(faster=int(Graha.MOON), slower=int(Graha.SATURN),
                         faster_longitude=10.0, slower_longitude=70.0)
    ees = yogas.eesarpha(faster=int(Graha.MOON), slower=int(Graha.SATURN),
                         faster_longitude=10.0, slower_longitude=70.0)
    assert ith["aspects_by_house"] is True
    assert ith["separation_from_exact"] == pytest.approx(0.0)
    assert ith["type"] is None
    assert ees["advancements_are_equal"] is True
    assert ees["present_by_house"] is False
    assert ees["present_within_orb"] is False
    assert "neither ithasala nor eesarpha" in yogas.THE_EXACT_ASPECT_IS_NEITHER_YOGA
    assert yogas.SOOKSHMA_DRISHTI in yogas.THE_EXACT_ASPECT_IS_NEITHER_YOGA


def test_eesarpha_needs_the_orb_the_same_way_ithasala_does():
    """The example checks it in the same words, so the same reading holds:
    both planets inside the other's deeptamsa.
    """
    assert yogas.EESARPHA_EXAMPLE["both_within_the_others_orb"] is True
    wide = yogas.eesarpha(faster=int(Graha.MERCURY), slower=int(Graha.SATURN),
                          faster_longitude=25.0, slower_longitude=60.0 + 1.0)
    assert wide["faster_is_more_advanced"] is True
    assert wide["present_by_house"] is True
    assert wide["present_within_orb"] is False
    assert wide["separation_from_exact"] > wide["binding_deeptamsa"]


def test_an_eesarpha_with_a_node_leaves_the_orb_undecided():
    got = yogas.eesarpha(faster=int(Graha.RAHU), slower=int(Graha.SATURN),
                         faster_longitude=100.0, slower_longitude=5.0)
    assert got["present_by_house"] is True
    assert got["present_within_orb"] is None
    assert got["undecided"] == yogas.A_NODES_ITHASALA_CANNOT_BE_ORBED


def test_the_section_spells_its_own_yoga_three_ways():
    assert "Easarpha yoga is the opposite" in yogas.EESARPHA_RULE
    assert "eesarpha yoga" in yogas.EESARPHA_RULE
    assert "eesaarpha yoga" in yogas.EESARPHA_SPECIAL_NOTES
    assert "the Special Notes eesaarpha" in (
        yogas.THE_SECTION_SPELLS_ITS_OWN_YOGA_THREE_WAYS)


def test_the_station_case_is_named_here_and_not_worked():
    """The Special Notes point back at "about to become retrograde" and then
    work only the two retrograde cases.
    """
    assert "about to become retrograde" in yogas.EESARPHA_SPECIAL_NOTES
    assert "station" not in yogas.EESARPHA_SPECIAL_NOTES
    assert "no window is given" in (
        yogas.THE_STATION_CASE_IS_NAMED_BUT_NOT_WORKED_HERE)


# --------------------------------------------------------------------------
# §29.2.5 Nakta yoga
# --------------------------------------------------------------------------


def test_the_nakta_rule_is_transcribed_with_its_slip_intact():
    assert "no ithasala yoga or eesarpha yoga" in yogas.NAKTA_RULE
    assert "moves faster than both the planets" in yogas.NAKTA_RULE
    assert "forms ithasala yoga with both" in yogas.NAKTA_RULE
    # "shows by the 3rd planet" for "shown by", kept as printed.
    assert "someone shows by the 3rd planet" in yogas.NAKTA_RULE


def test_the_nakta_example_reproduces():
    """Venus 13 Ge, Mars 15 Sc, Moon 11 Cn. The Moon aspects both, is behind
    both, and is faster than both.
    """
    want = yogas.NAKTA_EXAMPLE
    got = yogas.nakta(
        first=int(Graha.VENUS), second=int(Graha.MARS),
        connector=int(Graha.MOON),
        first_longitude=float(want["first_longitude"]),
        second_longitude=float(want["second_longitude"]),
        connector_longitude=float(want["connector_longitude"]))
    assert got["first_pair_aspect"] is want["first_pair_aspect"]
    assert got["connector_aspects"] == (want["connector_to_first"],
                                        want["connector_to_second"])
    assert got["connector_is_faster_than_both"] is True
    assert got["connector_ithasala_types"] == ("Vartamaana", "Vartamaana")
    assert got["connector_carries"] is True
    assert got["present_as_worked"] is True


def test_the_examples_two_planets_have_no_aspect_at_all():
    """Ge to Sc is the 6th, which §28.2 leaves aspectless. The example says
    so and the rule says the opposite.
    """
    from hora.tajaka.aspects import aspect_on_house

    assert aspect_on_house(6) is None
    got = yogas.nakta(first=int(Graha.VENUS), second=int(Graha.MARS),
                      connector=int(Graha.MOON), first_longitude=73.0,
                      second_longitude=225.0, connector_longitude=101.0)
    assert got["first_pair_aspect"] is None
    assert got["first_pair_qualifies_as_worked"] is True
    assert got["first_pair_qualifies_as_worded"] is False
    assert got["readings_agree"] is False
    assert got["undecided"] is not None
    assert "have no aspect at all" in (
        yogas.THE_RULE_AND_ITS_EXAMPLE_DISAGREE_ON_THE_FIRST_PAIR)


def test_the_examples_lordships_and_placements_all_hold():
    """Venus lagna lord in the 2nd, Mars 7th lord in the 7th, Moon owning the
    3rd — from a Taurus lagna, every one of them.
    """
    from hora.core.const import RASI_LORD

    rasi = {"Ta": 1, "Ge": 2, "Cn": 3, "Sc": 7}
    lagna = rasi["Ta"]
    sits = {"Venus": rasi["Ge"], "Mars": rasi["Sc"], "Moon": rasi["Cn"]}
    for row in yogas.NAKTA_EXAMPLE["lordships"]:
        name = str(row["graha"])
        owned = (lagna + int(row["owns"]) - 1) % 12
        assert str(_GRAHA[name].name).title() == str(
            __import__("hora.core.const", fromlist=["GRAHA_NAMES"]
                       ).GRAHA_NAMES[int(RASI_LORD[owned])])
        assert (sits[name] - lagna) % 12 + 1 == int(row["sits_in"])


def test_as_worded_nakta_needs_an_aspect_wider_than_the_orb():
    """§29.2.4 showed an aspect inside the orb always gives one yoga or the
    other, so the rule's own condition needs a wide aspect.
    """
    # Mercury 1 Ar and Saturn 25 Ge: a sextile by house, 24° apart, far
    # outside the binding orb of 7° and outside bhavishya's further degree,
    # so no ithasala of any of the three kinds and no eesarpha.
    got = yogas.nakta(first=int(Graha.MERCURY), second=int(Graha.SATURN),
                      connector=int(Graha.MOON), first_longitude=1.0,
                      second_longitude=60.0 + 25.0, connector_longitude=0.5)
    assert got["first_pair_aspect"] == "Sextile aspect"
    assert got["first_pair_has_ithasala"] is None
    assert got["first_pair_has_eesarpha"] is False
    assert got["first_pair_qualifies_as_worded"] is True
    assert got["first_pair_qualifies_as_worked"] is False
    assert "an aspect wider than that" in (
        yogas.AS_WORDED_NAKTA_NEEDS_A_WIDE_ASPECT)


def test_a_close_aspect_can_never_satisfy_the_rule_as_worded():
    """The complement of §29.2.4's partition, over random pairs."""
    random.seed(2951)
    checked = 0
    for _ in range(3000):
        a, b = random.sample(range(7), 2)
        connector = next(g for g in (int(Graha.MOON), int(Graha.MERCURY),
                                     int(Graha.VENUS)) if g not in (a, b))
        got = yogas.nakta(first=a, second=b, connector=connector,
                          first_longitude=random.uniform(0, 360),
                          second_longitude=random.uniform(0, 360),
                          connector_longitude=random.uniform(0, 360))
        if not got["first_pair_qualifies_as_worded"]:
            continue
        checked += 1
        assert got["first_pair_aspect"] is not None
        assert got["first_pair_has_ithasala"] is None
        assert got["first_pair_has_eesarpha"] is False
    assert checked > 50


def test_the_connector_must_be_faster_than_both():
    """Swap the Moon for Saturn and nothing carries."""
    got = yogas.nakta(first=int(Graha.VENUS), second=int(Graha.MARS),
                      connector=int(Graha.SATURN), first_longitude=73.0,
                      second_longitude=225.0, connector_longitude=101.0)
    assert got["connector_is_faster_than_both"] is False
    assert got["connector_carries"] is False
    assert got["connector_ithasala_types"] == (None, None)
    assert got["present_as_worked"] is False


def test_the_speed_condition_and_the_two_ithasalas_are_one_condition():
    """A planet faster than both is the faster party in both legs, always."""
    random.seed(2952)
    for _ in range(1500):
        trio = random.sample(range(7), 3)
        trio.sort(key=yogas.speed_rank)
        first, second, connector = trio[0], trio[1], trio[2]
        got = yogas.nakta(first=first, second=second, connector=connector,
                          first_longitude=random.uniform(0, 360),
                          second_longitude=random.uniform(0, 360),
                          connector_longitude=random.uniform(0, 360))
        assert got["connector_is_faster_than_both"] is True
    assert "one condition stated twice" in (
        yogas.THE_SPEED_CONDITION_IS_THE_ITHASALA_CONDITION)


def test_a_bhavishya_leg_still_counts_as_an_ithasala():
    """"Forms ithasala with both" is not narrowed to vartamaana, and a
    bhavishya has not formed yet. Reported, not filtered.
    """
    assert "whether a bhavishya counts" in (
        yogas.WHICH_ITHASALA_THE_CONNECTOR_NEEDS_IS_NOT_SAID)
    # Moon 3° Ar; Venus at 11° Ge is 8° on, outside Venus's 7° orb by 1°.
    got = yogas.nakta(first=int(Graha.VENUS), second=int(Graha.MARS),
                      connector=int(Graha.MOON), first_longitude=60.0 + 11.0,
                      second_longitude=120.0 + 10.0, connector_longitude=3.0)
    assert got["connector_ithasala_types"] == ("Bhavishya", "Vartamaana")
    assert got["connector_carries"] is True


def test_nakta_needs_three_different_grahas():
    with pytest.raises(yogas.TajakaYogaError, match="three different grahas"):
        yogas.nakta(first=int(Graha.VENUS), second=int(Graha.VENUS),
                    connector=int(Graha.MOON), first_longitude=1.0,
                    second_longitude=2.0, connector_longitude=3.0)


def test_nakta_refuses_a_first_pair_footnote_83_cannot_rank():
    with pytest.raises(yogas.TajakaYogaError, match="cannot rank"):
        yogas.nakta(first=int(Graha.RAHU), second=int(Graha.KETU),
                    connector=int(Graha.MOON), first_longitude=1.0,
                    second_longitude=2.0, connector_longitude=3.0)


# --------------------------------------------------------------------------
# §29.2.6 Yamaya yoga
# --------------------------------------------------------------------------


def test_the_yamaya_rule_is_nakta_with_one_word_changed():
    assert "moves slower than both the planets" in yogas.YAMAYA_RULE
    assert "after obstacles and delays" in yogas.YAMAYA_RULE
    # The same slip, repeated verbatim.
    assert "someone shows by the 3rd planet" in yogas.YAMAYA_RULE

    # The two rules differ only in the speed word and the closing clause.
    swapped = yogas.YAMAYA_RULE.replace("Yamaya", "Nakta").replace(
        "moves slower than", "moves faster than").replace(
        " planet, after obstacles and delays.", " planet.")
    assert swapped == yogas.NAKTA_RULE
    assert "slower for faster" in yogas.YAMAYA_IS_NAKTA_WITH_THE_SPEED_REVERSED


def test_the_yamaya_example_reproduces():
    """Jupiter 16 Cn against Venus 13 Ge and Mars 15 Sc: a semi-sextile and a
    trinal, and Jupiter ahead of both because he is the slower party.
    """
    want = yogas.YAMAYA_EXAMPLE
    got = yogas.yamaya(
        first=int(Graha.VENUS), second=int(Graha.MARS),
        connector=int(Graha.JUPITER),
        first_longitude=float(want["first_longitude"]),
        second_longitude=float(want["second_longitude"]),
        connector_longitude=float(want["connector_longitude"]))
    assert got["first_pair_aspect"] is want["first_pair_aspect"]
    assert got["connector_aspects"] == (want["connector_to_first"],
                                        want["connector_to_second"])
    assert got["connector_is_slower_than_both"] is True
    assert got["connector_carries"] is True
    assert got["present_as_worked"] is True
    assert "after obstacles and delays" in str(got["shows"])


def test_the_jupiter_to_mars_leg_is_exactly_a_poorna():
    """16° against 15° is one degree, which is poorna's threshold on the nose.
    """
    got = yogas.yamaya(first=int(Graha.VENUS), second=int(Graha.MARS),
                       connector=int(Graha.JUPITER), first_longitude=73.0,
                       second_longitude=225.0, connector_longitude=106.0)
    assert got["connector_ithasala_types"] == ("Vartamaana", "Poorna")

    leg = yogas.ithasala(faster=int(Graha.MARS), slower=int(Graha.JUPITER),
                         faster_longitude=225.0, slower_longitude=106.0)
    assert leg["separation_from_exact"] == pytest.approx(1.0)
    assert leg["separation_from_exact"] == yogas.POORNA_DEGREES


def test_the_yamaya_example_is_the_nakta_example_with_jupiter_substituted():
    nakta_case, yamaya_case = yogas.NAKTA_EXAMPLE, yogas.YAMAYA_EXAMPLE
    for key in ("lagna_rasi", "first", "first_at", "first_longitude",
                "second", "second_at", "second_longitude",
                "first_pair_aspect", "connector_to_first",
                "connector_to_second"):
        assert nakta_case[key] == yamaya_case[key], key
    assert nakta_case["connector"] == "Moon"
    assert yamaya_case["connector"] == "Jupiter"


def test_jupiter_owns_the_eleventh_from_taurus():
    from hora.core.const import GRAHA_NAMES, RASI_LORD

    eleventh = (1 + 11 - 1) % 12
    assert str(GRAHA_NAMES[int(RASI_LORD[eleventh])]) == "Jupiter"
    row = next(r for r in yogas.YAMAYA_EXAMPLE["lordships"]
               if r["graha"] == "Jupiter")
    assert row["owns"] == 11
    assert row["matter"] == "elder siblings or friends"


def test_the_connector_looks_the_other_way_in_a_yamaya():
    """A nakta's connector is behind both; a yamaya's is ahead of both. The
    two examples differ in exactly that.
    """
    assert float(yogas.NAKTA_EXAMPLE["connector_longitude"]) % 30 == 11.0
    assert float(yogas.YAMAYA_EXAMPLE["connector_longitude"]) % 30 == 16.0
    for case in (yogas.NAKTA_EXAMPLE, yogas.YAMAYA_EXAMPLE):
        advancements = [float(case[k]) % 30 for k in
                        ("first_longitude", "second_longitude")]
        connector = float(case["connector_longitude"]) % 30
        if case["connector"] == "Moon":
            assert all(connector < x for x in advancements)
        else:
            assert all(connector > x for x in advancements)
    assert "must be more advanced than both" in (
        yogas.THE_CONNECTOR_LOOKS_THE_OTHER_WAY_IN_A_YAMAYA)


def test_a_yamaya_connector_that_is_behind_carries_nothing():
    """Put Jupiter at 11° instead of 16° and both legs fail, because as the
    slower party he now has an eesarpha with each.
    """
    got = yogas.yamaya(first=int(Graha.VENUS), second=int(Graha.MARS),
                       connector=int(Graha.JUPITER), first_longitude=73.0,
                       second_longitude=225.0, connector_longitude=101.0)
    assert got["connector_is_slower_than_both"] is True
    assert got["connector_ithasala_types"] == (None, None)
    assert got["connector_carries"] is False


def test_the_moon_cannot_make_a_yamaya_and_jupiter_cannot_make_a_nakta():
    """Each section's own connector is disqualified by the other's rule."""
    shared = {"first": int(Graha.VENUS), "second": int(Graha.MARS),
              "first_longitude": 73.0, "second_longitude": 225.0}
    assert yogas.yamaya(**shared, connector=int(Graha.MOON),
                        connector_longitude=101.0)["connector_speed_holds"] is (
        False)
    assert yogas.nakta(**shared, connector=int(Graha.JUPITER),
                       connector_longitude=106.0)["connector_speed_holds"] is (
        False)


def test_a_third_of_every_possible_connector_has_no_yoga():
    """Faster than both, slower than both, or between — and between is a case
    §29.2 never names.
    """
    tally = {"Nakta": 0, "Yamaya": 0, None: 0}
    for a, b in itertools.combinations(range(7), 2):
        for c in range(7):
            if c in (a, b):
                continue
            tally[yogas.connector_role(a, b, c)] += 1
    assert tally == {"Nakta": 35, "Yamaya": 35, None: 35}
    assert "35 have no yoga at all" in (
        yogas.A_CONNECTOR_BETWEEN_THE_TWO_HAS_NO_YOGA)


def test_connector_role_agrees_with_both_functions():
    random.seed(2961)
    for _ in range(1200):
        a, b, c = random.sample(range(7), 3)
        role = yogas.connector_role(a, b, c)
        shared = {"first": a, "second": b, "connector": c,
                  "first_longitude": random.uniform(0, 360),
                  "second_longitude": random.uniform(0, 360),
                  "connector_longitude": random.uniform(0, 360)}
        assert yogas.nakta(**shared)["connector_speed_holds"] is (
            role == "Nakta")
        assert yogas.yamaya(**shared)["connector_speed_holds"] is (
            role == "Yamaya")


def test_yamaya_carries_oi_164_the_same_way_nakta_does():
    got = yogas.yamaya(first=int(Graha.VENUS), second=int(Graha.MARS),
                       connector=int(Graha.JUPITER), first_longitude=73.0,
                       second_longitude=225.0, connector_longitude=106.0)
    assert got["first_pair_qualifies_as_worded"] is False
    assert got["first_pair_qualifies_as_worked"] is True
    assert got["readings_agree"] is False
    assert got["undecided"] == (
        yogas.THE_RULE_AND_ITS_EXAMPLE_DISAGREE_ON_THE_FIRST_PAIR)


def test_yamaya_rejects_the_same_bad_inputs_as_nakta():
    with pytest.raises(yogas.TajakaYogaError, match="three different grahas"):
        yogas.yamaya(first=int(Graha.VENUS), second=int(Graha.VENUS),
                     connector=int(Graha.JUPITER), first_longitude=1.0,
                     second_longitude=2.0, connector_longitude=3.0)
    with pytest.raises(yogas.TajakaYogaError, match="cannot rank"):
        yogas.yamaya(first=int(Graha.RAHU), second=int(Graha.KETU),
                     connector=int(Graha.JUPITER), first_longitude=1.0,
                     second_longitude=2.0, connector_longitude=3.0)
