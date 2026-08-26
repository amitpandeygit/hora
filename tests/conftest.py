import pytest

from hora.charts.chart import Place, compute_chart
from hora.core.settings import Settings
from hora.core.timeutil import from_local

#: P.V.R. Narasimha Rao's own chart — the worked example running through
#: "Vedic Astrology: An Integrated Approach", which makes it the natural
#: reference case for benchmarking against his software.
PVR_BIRTH = {
    "year": 1972, "month": 10, "day": 1, "hour": 13, "minute": 30, "second": 0.0,
    "tz_name": "Asia/Kolkata",
}
PVR_PLACE = Place(latitude=16.2, longitude=81.13, name="Machilipatnam, India")


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings()


@pytest.fixture(scope="session")
def pvr_chart(settings):
    return compute_chart(from_local(**PVR_BIRTH), PVR_PLACE, settings)


@pytest.fixture(scope="session")
def client():
    from fastapi.testclient import TestClient

    from hora.api.main import app

    return TestClient(app)
