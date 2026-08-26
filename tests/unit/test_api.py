"""API contract: status codes, shapes and input validation."""
BODY = {
    "year": 1972, "month": 10, "day": 1, "hour": 13, "minute": 30,
    "tz_name": "Asia/Kolkata",
    "place": {"latitude": 16.2, "longitude": 81.13, "name": "Machilipatnam"},
}


def test_health(client):
    assert client.get("/health").json()["status"] == "ok"


def test_rasi_chart_shape(client):
    r = client.post("/v1/chart/rasi", json=BODY)
    assert r.status_code == 200
    d = r.json()
    assert len(d["grahas"]) == 9
    assert len(d["bhavas"]) == 12
    assert d["lagna"]["rasi_name"] == "Sagittarius"


def test_outer_planets_are_opt_in(client):
    plain = client.post("/v1/chart/rasi", json=BODY).json()
    with_outer = client.post(
        "/v1/chart/rasi", json={**BODY, "settings": {"include_outer_planets": True}}
    ).json()
    assert len(plain["grahas"]) == 9
    assert len(with_outer["grahas"]) == 12


def test_varga_request(client):
    r = client.post("/v1/chart/vargas", json={**BODY, "charts": ["D1", "D9", "D144"]})
    assert r.status_code == 200
    assert set(r.json()["charts"]) == {"D1", "D9", "D144"}


def test_unknown_varga_is_a_400(client):
    r = client.post("/v1/chart/vargas", json={**BODY, "charts": ["Q9"]})
    assert r.status_code == 400


def test_shodasavarga_returns_sixteen(client):
    r = client.post("/v1/chart/shodasavarga", json=BODY)
    assert len(r.json()["charts"]) == 16


def test_dasha_endpoint(client):
    r = client.post("/v1/dasha", json={**BODY, "system": "vimshottari", "levels": 2})
    assert r.status_code == 200
    d = r.json()
    assert len(d["periods"]) == 9
    assert d["running"][0]["lord_name"] == "Saturn"


def test_unknown_dasha_system_is_a_400(client):
    r = client.post("/v1/dasha", json={**BODY, "system": "nonesuch"})
    assert r.status_code == 400


def test_missing_timezone_is_rejected(client):
    body = {k: v for k, v in BODY.items() if k != "tz_name"}
    assert client.post("/v1/chart/rasi", json=body).status_code == 422


def test_out_of_range_latitude_is_rejected(client):
    body = {**BODY, "place": {**BODY["place"], "latitude": 99.0}}
    assert client.post("/v1/chart/rasi", json=body).status_code == 422


def test_explicit_offset_matches_named_zone(client):
    a = client.post("/v1/chart/rasi", json=BODY).json()
    body = {k: v for k, v in BODY.items() if k != "tz_name"}
    b = client.post("/v1/chart/rasi", json={**body, "utc_offset_hours": 5.5}).json()
    assert a["lagna"]["longitude"] == b["lagna"]["longitude"]


def test_settings_schema_is_published(client):
    d = client.get("/v1/settings/schema").json()
    assert d["defaults"]["ayanamsa"] == "lahiri"
    assert "properties" in d["schema"]
