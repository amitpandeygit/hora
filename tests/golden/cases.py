"""The request set that defines the API's observable behaviour.

Every endpoint appears at least once, with inputs chosen to exercise the paths
that have actually gone wrong before — a pre-dawn birth, a night birth, a
non-default settings object, a rejected input.

`scripts/capture_golden.py` records the responses; `test_golden_api.py` replays
them and fails on any difference. Adding a case here and re-capturing is how a
deliberate change to the contract gets recorded.
"""

#: P.V.R. Narasimha Rao's own chart — a daytime birth.
PVR = {
    "year": 1972, "month": 10, "day": 1, "hour": 13, "minute": 30,
    "tz_name": "Asia/Kolkata",
    "place": {"latitude": 16.2, "longitude": 81.13, "name": "Machilipatnam"},
}

#: A pre-dawn birth. The night began at the previous sunset and the vaara has
#: not yet turned — the case that carried a 13-hour error until it was fixed.
PRE_DAWN = {
    "year": 1990, "month": 6, "day": 15, "hour": 2, "minute": 0,
    "tz_name": "Asia/Kolkata",
    "place": {"latitude": 16.2, "longitude": 81.13, "name": "Machilipatnam"},
}

#: An evening birth, so the night runs from this sunset to tomorrow's sunrise.
EVENING = {
    "year": 1990, "month": 6, "day": 15, "hour": 21, "minute": 45,
    "tz_name": "Asia/Kolkata",
    "place": {"latitude": 28.61, "longitude": 77.21, "name": "Delhi"},
}

#: Southern hemisphere, and a fixed UTC offset rather than a zone name.
SOUTHERN = {
    "year": 2001, "month": 12, "day": 21, "hour": 6, "minute": 5,
    "utc_offset_hours": -3.0,
    "place": {"latitude": -23.55, "longitude": -46.63, "name": "Sao Paulo"},
}

#: Non-default settings across every knob that changes output.
ALT_SETTINGS = {
    "ayanamsa": "raman",
    "node_type": "mean",
    "house_system": "placidus",
    "sunrise_mode": "disc_center",
    "apparent_positions": True,
    "dasha_year_length": "civil",
    "name_scheme": "standard",
    "upagraha_rise_point": "beginning",
    "include_outer_planets": True,
}


#: (case id, method, path, json body or None). Ids become file names.
CASES = [
    ("health", "GET", "/health", None),

    ("chart_rasi_pvr", "POST", "/v1/chart/rasi", PVR),
    ("chart_rasi_southern", "POST", "/v1/chart/rasi", SOUTHERN),
    ("chart_rasi_alt_settings", "POST", "/v1/chart/rasi", {**PVR, "settings": ALT_SETTINGS}),

    ("chart_vargas", "POST", "/v1/chart/vargas",
     {**PVR, "charts": ["D1", "D9", "D10", "D30", "D60", "D144", "D150"]}),
    ("chart_vargas_variant", "POST", "/v1/chart/vargas",
     {**PVR, "charts": ["D2", "D3"], "variants": {"D2": "parivritti", "D3": "parivritti"}}),
    ("chart_shodasavarga", "POST", "/v1/chart/shodasavarga", PVR),

    ("chart_upagrahas_day", "POST", "/v1/chart/upagrahas", PVR),
    ("chart_upagrahas_pre_dawn", "POST", "/v1/chart/upagrahas", PRE_DAWN),
    ("chart_upagrahas_evening", "POST", "/v1/chart/upagrahas", EVENING),
    ("chart_upagrahas_beginning", "POST", "/v1/chart/upagrahas",
     {**PVR, "settings": {"upagraha_rise_point": "beginning"}}),

    ("chart_special_lagnas", "POST", "/v1/chart/special-lagnas", PVR),
    ("chart_special_lagnas_pre_dawn", "POST", "/v1/chart/special-lagnas", PRE_DAWN),

    ("panchanga_pvr", "POST", "/v1/panchanga", PVR),
    ("panchanga_evening", "POST", "/v1/panchanga", EVENING),

    ("dasha_vimshottari", "POST", "/v1/dasha",
     {**PVR, "system": "vimshottari", "levels": 3}),
    ("dasha_ashtottari", "POST", "/v1/dasha", {**PVR, "system": "ashtottari", "levels": 1}),
    ("dasha_as_of", "POST", "/v1/dasha",
     {**PVR, "system": "vimshottari", "levels": 2, "as_of": "2026-08-25T10:00:00"}),

    ("ephemeris_positions", "POST", "/v1/ephemeris/positions", PVR),

    ("util_notation_sign_dm", "POST", "/v1/util/notation", {"value": "5s 17 45"}),
    ("util_notation_rasi_dm", "POST", "/v1/util/notation", {"value": "25 Li 31"}),
    ("util_notation_decimal", "POST", "/v1/util/notation", {"value": "167.75"}),

    ("varga_compute", "POST", "/v1/varga/compute",
     {"longitude": "11 Ge 00",
      "charts": ["D3", "D5", "D8", "D9", "D11", "D24", "D27", "D30", "D60"]}),
    ("varga_compute_decimal", "POST", "/v1/varga/compute",
     {"longitude": 222.9666666, "charts": ["D60", "D150"]}),
    ("varga_rules", "GET", "/v1/varga/rules", None),

    ("lagna_special_time_based", "POST", "/v1/lagna/special",
     {"sun_at_sunrise": "24 Cp 17", "minutes_since_sunrise": 766,
      "lagnas": ["BL", "HL", "GL"]}),
    ("lagna_special_sree", "POST", "/v1/lagna/special",
     {"lagnas": ["SL"], "moon": "13 Li 06", "lagna": "25 Vi 05"}),
    ("lagna_rules", "GET", "/v1/lagna/rules", None),

    ("house_from_lagna", "POST", "/v1/house/from",
     {"reference_rasi": 8, "reference": "lagna"}),
    ("house_from_chandra", "POST", "/v1/house/from",
     {"reference_rasi": 10, "reference": "chandra_lagna"}),
    ("house_references", "POST", "/v1/house/references",
     {"lagna_rasi": 11, "graha_rasis": {"0": 5, "1": 3, "4": 3},
      "ghati_lagna_rasi": 5, "hora_lagna_rasi": 8}),
    ("house_categories_1", "GET", "/v1/house/categories/1", None),
    ("house_categories_3", "GET", "/v1/house/categories/3", None),
    ("house_rules", "GET", "/v1/house/rules", None),
    ("err_house_bad_reference", "POST", "/v1/house/from",
     {"reference_rasi": 0, "reference": "nonesuch"}),
    ("err_house_bad_base", "GET", "/v1/house/categories/13", None),
    ("err_lagna_missing_inputs", "POST", "/v1/lagna/special", {"lagnas": ["SL"]}),
    ("varga_amsabala", "POST", "/v1/varga/amsabala", {"longitude": "10 Ar 00", "graha": 0}),
    ("err_varga_compute_bad", "POST", "/v1/varga/compute",
     {"longitude": "not a longitude", "charts": ["D9"]}),
    ("err_varga_empty_charts", "POST", "/v1/varga/compute",
     {"longitude": 10.0, "charts": []}),
    ("err_varga_bad_code", "POST", "/v1/varga/compute",
     {"longitude": 10.0, "charts": ["D0"]}),

    ("strength_activity_mercury", "POST", "/v1/avastha/activity", {
        # Footnote 51's own example longitude: Mercury at 22Ge14.
        "graha": 3, "graha_longitude": 82.23333333333333,
        "moon_longitude": 100.0, "lagna_rasi": 5, "ghati": 43,
        "name_sound": 1,
    }),
    ("strength_activity_no_name_sound", "POST", "/v1/avastha/activity", {
        "graha": 3, "graha_longitude": 82.23333333333333,
        "moon_longitude": 100.0, "lagna_rasi": 5, "ghati": 43,
    }),
    ("strength_ghati", "POST", "/v1/avastha/ghati", {"hours_after_sunrise": 17.0}),
    ("strength_sound_devanagari", "POST", "/v1/avastha/sound", {"syllable": "\u0915"}),
    ("err_strength_sound_ambiguous", "POST", "/v1/avastha/sound", {"syllable": "d"}),
    ("avastha_results_mars_prakaasana", "POST", "/v1/avastha/activity/results", {
        "avastha": 4, "graha": 2, "house": 5, "joined_by": [7],
    }),
    ("avastha_results_venus_undetermined", "POST", "/v1/avastha/activity/results", {
        "avastha": 3, "graha": 5,
    }),
    ("avastha_results_not_transcribed", "POST", "/v1/avastha/activity/results", {
        "avastha": 12, "graha": 0,
    }),
    ("strength_measures", "GET", "/v1/strength/measures", None),
    ("strength_rules", "GET", "/v1/avastha/rules", None),
    ("strength_avastha_mars", "POST", "/v1/avastha/state", {
        "graha": 2, "graha_longitudes": {0: 1.0, 1: 31.0, 2: 113.0, 3: 91.0, 4: 121.0, 5: 151.0, 6: 207.0, 7: 211.0, 8: 241.0},
    }),
    ("strength_compare_mars_ketu", "POST", "/v1/strength/compare", {
        "left": 2, "right": 8, "graha_longitudes": {0: 1.0, 1: 31.0, 2: 113.0, 3: 91.0, 4: 121.0, 5: 151.0, 6: 207.0, 7: 211.0, 8: 241.0},
    }),
    ("rasi_strength_purposes", "GET", "/v1/rasi-strength/purposes", None),
    ("rasi_strength_rule_1", "POST", "/v1/rasi-strength/stronger", {
        # 15.5.2 rule 1: Ar holds Saturn and Jupiter, Li holds Venus.
        "first": 0, "second": 6,
        "graha_longitudes": {6: 10.0, 4: 11.0, 5: 190.0},
    }),
    ("rasi_strength_full_cascade", "POST", "/v1/rasi-strength/stronger", {
        # Reaches rule 6 with the section's own longitudes.
        "first": 0, "second": 6,
        "graha_longitudes": {2: 53.28333333333333, 5: 109.85},
    }),
    ("err_rasi_strength_ayur", "POST", "/v1/rasi-strength/stronger", {
        "first": 0, "second": 6, "graha_longitudes": {2: 70.0, 5: 100.0},
        "purpose": "ayur",
    }),
    ("colord_rule_5b", "POST", "/v1/colord/stronger", {
        # Section 15.5.1 rule 5b: Mars 23Li17 vs Ketu 5Cn54 -> Ketu.
        "rasi": 7,
        "graha_longitudes": {2: 203.28333333333333, 8: 95.9},
        "purpose": "arudha",
        "rasi_aspects": {0: [4, 7, 10], 1: [3, 6, 9], 2: [5, 8, 11], 3: [7, 10, 1], 4: [6, 9, 0], 5: [8, 11, 2], 6: [10, 1, 4], 7: [9, 0, 3], 8: [11, 2, 5], 9: [1, 4, 7], 10: [0, 3, 6], 11: [2, 5, 8]},
    }),
    ("colord_stops_without_rasi_aspects", "POST", "/v1/colord/stronger", {
        # An empty table models "no aspects known": the cascade must stop at
        # rule 2 rather than skipping to rule 3.
        "rasi": 10, "graha_longitudes": {6: 190.0, 7: 100.0},
        "rasi_aspects": {},
    }),
    ("colord_default_aspects", "POST", "/v1/colord/stronger", {
        "rasi": 10, "graha_longitudes": {6: 190.0, 7: 100.0},
    }),
    ("err_colord_single_lorded_rasi", "POST", "/v1/colord/stronger", {
        "rasi": 0, "graha_longitudes": {2: 10.0, 8: 100.0},
    }),
    ("arudha_example_29", "POST", "/v1/arudha/table", {
        # Example 29, Chart 1. Two houses fall in co-owned rasis and are
        # resolved by section 15.5.1 without the caller naming a lord.
        "lagna_sign": 5,
        "graha_signs": {0: 11, 1: 2, 2: 0, 3: 11, 4: 0, 5: 11, 6: 0, 7: 3, 8: 9},
        "graha_longitudes": {0: 356.48333333333335, 1: 64.75, 2: 19.15, 3: 331.6, 4: 17.35, 5: 340.01666666666665, 6: 22.683333333333334, 7: 95.91666666666667, 8: 275.9166666666667},
        "include_steps": False,
    }),
    ("graha_arudha_example_30", "POST", "/v1/graha-arudha/table", {
        # Example 30, Chart 1 — the same chart as Example 29.
        "graha_signs": {0: 11, 1: 2, 2: 0, 3: 11, 4: 0, 5: 11, 6: 0, 7: 3, 8: 9},
        "graha_longitudes": {0: 356.48333333333335, 1: 64.75, 2: 19.15, 3: 331.6, 4: 17.35, 5: 340.01666666666665, 6: 22.683333333333334, 7: 95.91666666666667, 8: 275.9166666666667},
        "include_steps": False,
    }),
    ("graha_arudha_exercise_13", "POST", "/v1/graha-arudha/table", {
        # Exercise 13, Chart 2's D-16 — the divisional graha arudha set.
        "graha_signs": {0: 10, 1: 10, 2: 10, 3: 8, 4: 9, 5: 1, 6: 0, 7: 3, 8: 3},
        "include_steps": False,
    }),
    ("graha_arudha_rules", "GET", "/v1/graha-arudha/rules", None),
    ("graha_arudha_section_example", "POST", "/v1/graha-arudha/pada", {
        # 9.5's own example: Sun in Gemini owns Leo, count 3, ends in Libra.
        "graha": 0,
        "graha_signs": {0: 2, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8},
    }),
    ("graha_arudha_table", "POST", "/v1/graha-arudha/table", {
        "graha_signs": {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8},
        "include_steps": False,
    }),
    ("arudha_rules", "GET", "/v1/arudha/rules", None),
    ("arudha_pada_excerpt_example", "POST", "/v1/arudha/pada", {
        # Section 9.2's own example: house in Gemini, lord Mercury in Aquarius.
        "house": 1, "lagna_sign": 2,
        "graha_signs": {0: 0, 1: 0, 2: 0, 3: 10, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
    }),
    ("arudha_table", "POST", "/v1/arudha/table", {
        "lagna_sign": 5,
        "graha_signs": {0: 11, 1: 2, 2: 0, 3: 11, 4: 0, 5: 11, 6: 0, 7: 0, 8: 0},
        "stronger_lord": {7: 2, 10: 6},
    }),
    ("err_arudha_dual_lord_unresolved", "POST", "/v1/arudha/pada", {
        "house": 1, "lagna_sign": 10,
        "graha_signs": {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
    }),
    # Chapter 10 — aspects. The chart case is Exercise 14: Chart 5's navamsa,
    # Scorpio lagna. Its whole answer table is a golden.
    ("aspect_rules", "GET", "/v1/aspect/rules", None),
    ("aspect_chart_exercise_14", "POST", "/v1/aspect/chart", {
        "rasis": {0: 1, 1: 0, 2: 7, 3: 8, 4: 5, 5: 9, 6: 7, 7: 4, 8: 10},
        "lagna_rasi": 7,
    }),
    ("aspect_graha_jupiter_gemini", "POST", "/v1/aspect/graha", {
        # Example 34's first line: Jupiter in Ge aspects Li, Sg and Aq.
        "graha": 4, "rasi": 2,
    }),
    ("aspect_between_jupiter_saturn", "POST", "/v1/aspect/between", {
        # 10.2's own example: Jupiter in Ta aspects Saturn in Cp.
        "graha": 4, "graha_rasi": 1, "target_rasi": 9,
    }),
    # Chapter 10 §10.6 — argala. The chart case is Exercise 16: Chart 5's
    # navamsa, Scorpio lagna, all twelve houses and all ninety-six cells.
    ("argala_rules", "GET", "/v1/argala/rules", None),
    ("argala_chart_exercise_16", "POST", "/v1/argala/chart", {
        "rasis": {0: 1, 1: 0, 2: 7, 3: 8, 4: 5, 5: 9, 6: 7, 7: 4, 8: 10},
        "lagna_rasi": 7,
    }),
    ("argala_sign_worked_example", "POST", "/v1/argala/sign", {
        # 10.6's own example: Mercury, Jupiter, Venus, Saturn in Ge, Pi, Ar, Vi.
        "sign": 2, "rasis": {3: 2, 4: 11, 5: 0, 6: 5},
    }),
    ("err_argala_empty_chart", "POST", "/v1/argala/chart",
     {"rasis": {}, "lagna_rasi": 0}),

    ("aspect_rasi_aries", "GET", "/v1/aspect/rasi/0", None),
    ("aspect_rasi_taurus", "GET", "/v1/aspect/rasi/1", None),
    ("aspect_rasi_gemini", "GET", "/v1/aspect/rasi/2", None),
    ("err_aspect_empty_chart", "POST", "/v1/aspect/chart", {"rasis": {}}),

    ("karaka_kinds", "GET", "/v1/karaka/kinds", None),
    ("karaka_sthira", "GET", "/v1/karaka/sthira", None),
    ("karaka_naisargika", "GET", "/v1/karaka/naisargika", None),
    ("karaka_chara_example28", "POST", "/v1/karaka/chara", {
        "longitudes": {
            0: 72.78333333333333,   # Sun     12Ge47
            1: 20.466666666666665,  # Moon    20Ar28
            2: 73.85,               # Mars    13Ge51
            3: 85.3,                # Mercury 25Ge18
            4: 35.666666666666664,  # Jupiter  5Ta40
            5: 77.35,               # Venus   17Ge21
            6: 32.46666666666667,   # Saturn   2Ta28
            7: 91.71666666666667,   # Rahu     1Cn43
        },
    }),
    ("err_karaka_chara_with_ketu", "POST", "/v1/karaka/chara", {
        "longitudes": {0: 10.0, 1: 20.0, 2: 30.0, 3: 40.0, 4: 50.0,
                       5: 60.0, 6: 70.0, 7: 80.0, 8: 90.0},
    }),
    ("catalog_vargas", "GET", "/v1/chart/varga-catalog", None),
    ("catalog_dashas", "GET", "/v1/dasha/systems", None),
    ("settings_schema", "GET", "/v1/settings/schema", None),
    ("tables_rasis", "GET", "/v1/util/tables/rasis", None),
    ("tables_grahas", "GET", "/v1/util/tables/grahas", None),
    ("tables_nakshatras", "GET", "/v1/util/tables/nakshatras", None),
    ("tables_tithis", "GET", "/v1/util/tables/tithis", None),
    ("tables_yogas", "GET", "/v1/util/tables/yogas", None),
    ("tables_relationship_terms", "GET", "/v1/util/tables/relationship-terms", None),
    ("yoga_exercise_4", "POST", "/v1/yoga/compute", {
        # Exercise 4: Moon 14 Le 43, Sun 28 Cp 13 -> Atiganda, the 6th.
        "sun_longitude": 298.21666666666664, "moon_longitude": 134.71666666666667,
    }),
    ("relationship_compound_example_5", "POST", "/v1/relationship/compound", {
        # Example 5: the Sun's compound relations in Lord Sree Rama's chart.
        "graha": 0,
        "rasis": {0: 0, 1: 3, 2: 9, 3: 1, 4: 3, 5: 11, 6: 6, 7: 8, 8: 2},
    }),
    ("relationship_chart_rama", "POST", "/v1/relationship/chart", {
        # The whole of section 3.4 for Lord Sree Rama's chart, in one call.
        "rasis": {0: 0, 1: 3, 2: 9, 3: 1, 4: 3, 5: 11, 6: 6, 7: 8, 8: 2},
    }),
    ("house_meanings_4_in_d16", "GET", "/v1/house/meanings?house=4&chart=D16", None),
    ("house_derived_2_from_3", "GET", "/v1/house/derived?house=2&from_house=3", None),
    ("varga_for_matter_career", "GET", "/v1/varga/for-matter?matter=career", None),
    ("relationship_rules", "GET", "/v1/relationship/rules", None),
    ("relationship_natural_moon_venus", "POST", "/v1/relationship/natural",
     {"graha": 1, "other": 5}),
    ("relationship_temporary_example_4", "POST", "/v1/relationship/temporary", {
        # Example 4: Sun in Lord Sree Rama's chart. Saturn is the only enemy.
        "graha": 0,
        "rasis": {0: 0, 1: 3, 2: 9, 3: 1, 4: 3, 5: 11, 6: 6, 7: 8, 8: 2},
    }),
    ("benefic_rules", "GET", "/v1/benefic/rules", None),
    ("benefic_mercury_alone", "POST", "/v1/benefic/nature", {"graha": 3}),
    ("benefic_mercury_with_malefics", "POST", "/v1/benefic/nature",
     {"graha": 3, "companions": [0, 2]}),
    ("benefic_waxing_moon", "POST", "/v1/benefic/nature", {"graha": 1, "paksha": 0}),
    ("karana_rules", "GET", "/v1/karana/rules", None),
    ("karana_slot_58", "POST", "/v1/karana/compute", {"slot": 58}),
    ("karana_first_half_of_first_tithi", "POST", "/v1/karana/compute",
     {"tithi": 1, "half": 1}),
    ("karana_at_example_2", "POST", "/v1/karana/at", {
        # Example 2's pair from 1.3.8.1: the 19th tithi.
        "sun_longitude": 227.76666666666668, "moon_longitude": 84.2,
    }),
    ("hora_rules", "GET", "/v1/hora/rules", None),
    ("hora_wednesday", "GET", "/v1/hora/day/3", None),
    ("hora_example_1_3_11", "POST", "/v1/hora/compute", {
        # 9:40 pm Wednesday, sunrise 6:10 am -> 16th hora -> Moon.
        "weekday": 3, "elapsed_hours": 15.5,
    }),
    ("yoga_rules", "GET", "/v1/yoga/rules", None),
    ("yoga_example_3", "POST", "/v1/yoga/compute", {
        # Example 3: Sun 23 Cp 50, Moon 17 Li 20 -> Ganda, the 10th.
        "sun_longitude": 293.8333333333333, "moon_longitude": 197.33333333333334,
    }),
    ("maasa_rules", "GET", "/v1/maasa/rules", None),
    ("maasa_chaitra", "POST", "/v1/maasa/compute", {
        # 1.3.8.2: conjunction in Pisces starts Chaitra maasa.
        "conjunction_longitude": 345.0,
    }),
    ("maasa_adhika_jyeshtha_1999", "POST", "/v1/maasa/compute", {
        # The second Taurus conjunction of 1999, 28 Ta 29.
        "conjunction_longitude": 58.483333333333334, "qualifier": "Adhika",
    }),
    ("maasa_pair_1999", "POST", "/v1/maasa/pair", {
        "first_longitude": 30.383333333333333, "second_longitude": 58.483333333333334,
    }),
    ("tithi_rules", "GET", "/v1/tithi/rules", None),
    ("tithi_example_2", "POST", "/v1/tithi/compute", {
        # Example 2: Moon 24 Ge 12, Sun 17 Sc 46 -> Krishna Chaturthi, 19th.
        "sun_longitude": 227.76666666666668, "moon_longitude": 84.2,
    }),
    ("tithi_exercise_3", "POST", "/v1/tithi/compute", {
        # Exercise 3: Moon 14 Le 43, Sun 28 Cp 13 -> Krishna Dwitiya, 17th.
        "sun_longitude": 298.21666666666664, "moon_longitude": 134.71666666666667,
    }),
    ("tithi_new_moon", "POST", "/v1/tithi/compute", {
        "sun_longitude": 0.0, "moon_longitude": 349.0,
    }),
    ("chakra_styles", "GET", "/v1/chakra/styles", None),
    ("chakra_example_1_rama", "POST", "/v1/chakra/build", {
        # Example 1: Lord Sree Rama's rasi chart, as rasi indices.
        "graha_positions": {0: 0, 3: 1, 8: 2, 1: 3, 4: 3, 6: 6, 7: 8, 2: 9, 5: 11},
        "lagna": 3,
        "positions_are_longitudes": False,
    }),
    ("err_chakra_no_reference_for_houses", "POST", "/v1/chakra/build", {
        "graha_positions": {0: 5.0}, "reference": "chandra_lagna",
    }),
    ("house_exercise_2_from_lagna", "POST", "/v1/house/from", {
        # Exercise 2 (1): no reference given, so lagna in Cancer.
        "reference_rasi": 3, "reference": "lagna",
    }),
    ("house_exercise_2_from_moon", "POST", "/v1/house/from", {
        # Exercise 2 (2): Moon in Taurus as the reference.
        "reference_rasi": 1, "reference": "chandra_lagna",
    }),
    ("notation_exercise_1_jupiter", "POST", "/v1/util/notation", {"value": "94\u00b019'"}),
    ("notation_exercise_1_mercury", "POST", "/v1/util/notation", {"value": "5s 17\u00b0 45'"}),
    ("notation_exercise_1_venus", "POST", "/v1/util/notation", {"value": "25 Li 31"}),
    ("err_notation_out_of_zodiac", "POST", "/v1/util/notation", {"value": "400"}),
    ("tables_terms", "GET", "/v1/util/tables/terms", None),
    ("tables_name_schemes", "GET", "/v1/util/tables/name-schemes", None),

    ("reference_sources", "GET", "/v1/reference/sources", None),
    ("reference_rasis_all", "GET", "/v1/reference/rasis", None),
    ("reference_rasis_one", "GET", "/v1/reference/rasis/0", None),

    # Error paths are part of the contract too.
    ("err_missing_zone", "POST", "/v1/chart/rasi",
     {k: v for k, v in PVR.items() if k != "tz_name"}),
    ("err_bad_latitude", "POST", "/v1/chart/rasi",
     {**PVR, "place": {**PVR["place"], "latitude": 99.0}}),
    ("err_unknown_varga", "POST", "/v1/chart/vargas", {**PVR, "charts": ["Q9"]}),
    ("err_unknown_dasha", "POST", "/v1/dasha", {**PVR, "system": "nonesuch"}),
    ("err_bad_notation", "POST", "/v1/util/notation", {"value": "not a longitude"}),
    ("err_reference_range", "GET", "/v1/reference/rasis/12", None),
]
