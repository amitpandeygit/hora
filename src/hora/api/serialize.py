"""Domain objects -> JSON-ready dictionaries.

Angles are emitted both as raw floats (for callers doing further maths) and as
JHora-style ``d-m-s`` strings (for eyeballing against the benchmark).
"""
from __future__ import annotations

from hora.charts.bhava import Bhava
from hora.charts.chart import Chart
from hora.charts.vargas import VargaPosition
from hora.core.const import GRAHA_NAMES, RASI_NAMES
from hora.core.notation import to_rasi_dm, to_sign_dm
from hora.core.timeutil import format_dms, jd_to_local_str
from hora.dasha.base import DashaPeriod
from hora.panchanga.core import Element, Panchanga


def angle(value: float) -> dict:
    return {"deg": round(value, 8), "dms": format_dms(value)}


def sign_and_degree(longitude: float) -> dict:
    rasi = int(longitude % 360.0 // 30.0)
    return {
        "longitude": round(longitude % 360.0, 8),
        "rasi": rasi,
        "rasi_name": RASI_NAMES[rasi],
        "degrees_in_rasi": round(longitude % 30.0, 8),
        "dms": format_dms(longitude % 30.0),
        # Classical notations from book section 1.3.2.
        "sign_dm": to_sign_dm(longitude),
        "rasi_dm": to_rasi_dm(longitude),
    }


def bhava_out(b: Bhava) -> dict:
    return {
        "house": b.index,
        "start": round(b.start, 8),
        "middle": round(b.middle, 8),
        "end": round(b.end, 8),
        "rasi": b.sign,
        "rasi_name": RASI_NAMES[b.sign],
    }


def envelope(instant, place, settings) -> dict:
    """The header every calculation response carries.

    ``input`` is the request as the engine resolved it and ``settings`` is the
    configuration actually used, so a result is reproducible from its own body
    without the caller having to remember what they sent.
    """
    return {
        "input": input_echo(instant, place),
        "settings": settings.model_dump(mode="json"),
    }


def input_echo(instant, place) -> dict:
    return {
        "local_time": instant.local.isoformat(),
        "utc": instant.utc.isoformat(),
        "utc_offset_hours": instant.utc_offset_hours,
        "timezone": instant.tz_name,
        "julian_day_ut": round(instant.jd_ut, 9),
        "place": {
            "name": place.name,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "altitude": place.altitude,
        },
    }


def chart_out(c: Chart) -> dict:
    off = c.instant.utc_offset_hours
    return {
        "input": {
            "local_time": c.instant.local.isoformat(),
            "utc": c.instant.utc.isoformat(),
            "utc_offset_hours": off,
            "timezone": c.instant.tz_name,
            "julian_day_ut": round(c.instant.jd_ut, 9),
            "place": {
                "name": c.place.name,
                "latitude": c.place.latitude,
                "longitude": c.place.longitude,
                "altitude": c.place.altitude,
            },
        },
        "settings": c.settings.model_dump(mode="json"),
        "ayanamsa": angle(c.ayanamsa),
        "lagna": {
            **sign_and_degree(c.lagna_longitude),
            "midheaven": round(c.houses.midheaven, 8),
        },
        "grahas": [
            {
                "id": st.graha,
                "name": st.name,
                "longitude": round(st.longitude, 8),
                "latitude": round(st.latitude, 8),
                "speed": round(st.speed, 8),
                "retrograde": st.retrograde,
                "rasi": st.rasi,
                "rasi_name": st.rasi_name,
                "degrees_in_rasi": round(st.degrees_in_rasi, 8),
                "dms": format_dms(st.degrees_in_rasi),
                "sign_dm": to_sign_dm(st.longitude),
                "rasi_dm": to_rasi_dm(st.longitude),
                "nakshatra": st.nakshatra,
                "nakshatra_name": st.nakshatra_name,
                "pada": st.pada,
                "house": st.house,
                "house_labels": st.house_labels,
                "dignity": st.dignity,
                "combust": st.combust,
                "sun_separation": round(st.combustion_orb, 6),
                "lord_of_houses": st.lord_of_houses,
            }
            for st in c.grahas.values()
        ],
        "bhavas": [bhava_out(b) for b in c.bhavas],
        "planetary_war": [
            {"a": a, "b": b, "winner": w} for a, b, w in c.planetary_war
        ],
    }


def varga_out(positions: dict[int, VargaPosition], chart: Chart, code: str) -> dict:
    lagna = positions[-1]
    return {
        "chart": code,
        "lagna": {"rasi": lagna.sign, "rasi_name": RASI_NAMES[lagna.sign],
                  "longitude": round(lagna.longitude, 8)},
        "grahas": [
            {
                "id": g,
                "name": chart.grahas[g].name,
                "rasi": v.sign,
                "rasi_name": RASI_NAMES[v.sign],
                "longitude": round(v.longitude, 8),
                "house": (v.sign - lagna.sign) % 12 + 1,
                "retrograde": chart.grahas[g].retrograde,
            }
            for g, v in sorted(positions.items())
            if g >= 0
        ],
    }


def element_out(e: Element, off: float) -> dict:
    """One panchanga limb.

    ``number`` is the 1-based value almanacs print; ``index`` is 0-based.
    """
    out = {
        "number": e.number,
        "index": e.index,
        "name": e.name,
        "name_standard": e.name_standard,
        "ends_local": jd_to_local_str(e.end_jd, off) if e.end_jd else None,
        "ends_jd": round(e.end_jd, 9) if e.end_jd else None,
    }
    if e.lord is not None:
        out["lord"] = e.lord
        out["lord_name"] = GRAHA_NAMES[e.lord]
    return out


def hora_out(h, off: float) -> dict:
    return {
        "index": h.index,
        "lord": h.lord,
        "lord_name": h.lord_name,
        "start_local": jd_to_local_str(h.start_jd, off),
        "end_local": jd_to_local_str(h.end_jd, off),
    }


def lunar_month_out(m, off: float) -> dict:
    return {
        "reckoning": m.reckoning,
        "index": m.index,
        "name": m.name,
        "paksha": m.paksha,
        "paksha_name": m.paksha_name,
        "is_adhika": m.is_adhika,
        "starts_local": jd_to_local_str(m.start_jd, off),
        "ends_local": jd_to_local_str(m.end_jd, off),
        "conjunction_rasi": m.conjunction_rasi,
        "conjunction_rasi_name": m.conjunction_rasi_name,
    }


def panchanga_out(p: Panchanga) -> dict:
    off = p.instant.utc_offset_hours
    d = p.day
    return {
        "date_local": p.instant.local.date().isoformat(),
        "vaara": {"index": p.vaara, "name": p.vaara_name, "lord": p.vaara_lord},
        "sunrise": jd_to_local_str(d.sunrise, off),
        "sunset": jd_to_local_str(d.sunset, off),
        "next_sunrise": jd_to_local_str(d.next_sunrise, off),
        "moonrise": jd_to_local_str(d.moonrise, off) if d.moonrise else None,
        "moonset": jd_to_local_str(d.moonset, off) if d.moonset else None,
        "day_length_hours": round(d.day_length * 24.0, 6),
        "night_length_hours": round(d.night_length * 24.0, 6),
        "tithi": [element_out(e, off) for e in p.tithis],
        "nakshatra": [element_out(e, off) for e in p.nakshatras],
        "yoga": [element_out(e, off) for e in p.yogas],
        "karana": [element_out(e, off) for e in p.karanas],
        "paksha": {"index": p.paksha, "name": p.paksha_name},
        "hora": hora_out(p.hora, off),
        "lunar_month": {k: lunar_month_out(v, off) for k, v in p.lunar_months.items()},
        "solar_date": {
            "month": p.solar_date.month,
            "month_name": p.solar_date.month_name,
            "day": p.solar_date.day,
        },
        "abhijit_active": p.abhijit_active,
        "sun_longitude": round(p.sun_longitude, 8),
        "moon_longitude": round(p.moon_longitude, 8),
    }


def dasha_out(p: DashaPeriod, off: float) -> dict:
    return {
        "lord": p.lord,
        "lord_name": p.lord_name,
        "level": p.level,
        "start": jd_to_local_str(p.start_jd, off),
        "end": jd_to_local_str(p.end_jd, off),
        "start_jd": round(p.start_jd, 9),
        "end_jd": round(p.end_jd, 9),
        "duration_days": round(p.duration_days, 6),
        "children": [dasha_out(c, off) for c in p.children],
    }
