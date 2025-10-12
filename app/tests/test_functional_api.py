import os

from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app
from app.models import WeatherReport
from app.storage import storage


def setup_module() -> None:
    os.environ.setdefault("OPENWEATHER_API_KEY", "test-key")
    get_settings.cache_clear()
    storage.clear()


client = TestClient(app)


def setup_function() -> None:
    storage.clear()


def test_get_weather_success(monkeypatch):
    async def fake_fetch_weather_report(**kwargs):
        return WeatherReport(
            city="Naters",
            country="CH",
            temp=21.5,
            feels_like=20.8,
            condition="klarer himmel",
        )

    monkeypatch.setattr("app.main.fetch_weather_report", fake_fetch_weather_report)

    response = client.get("/weather", params={"city": "Naters"})

    assert response.status_code == 200
    body = response.json()
    assert body["city"] == "Naters"
    assert body["country"] == "CH"
    assert "timestamp" in body


def test_get_weather_handles_http_error(monkeypatch):
    from app.weather_service import WeatherServiceHTTPError

    async def fake_fetch_weather_report(**kwargs):
        raise WeatherServiceHTTPError(404, "city not found")

    monkeypatch.setattr("app.main.fetch_weather_report", fake_fetch_weather_report)

    response = client.get("/weather", params={"city": "Foo"})

    assert response.status_code == 404
    assert "Wetter-API" in response.json()["detail"]


def test_history_roundtrip():
    history_entry = {
        "city": "Bern",
        "temp": 19.0,
        "country": "CH",
    }

    post_response = client.post("/history", json=history_entry)
    assert post_response.status_code == 200

    response = client.get("/history")
    assert response.status_code == 200
    history = response.json()
    assert len(history) == 1
    assert history[0]["city"] == "Bern"


def test_health_endpoint():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
