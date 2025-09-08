from fastapi.testclient import TestClient
import types
from app.main import app, history
import app.main as m

client = TestClient(app)

def setup_function():
    history.clear()

def test_weather_success(monkeypatch):
    class FakeResp:
        status_code = 200
        ok = True
        def json(self):
            return {
                "name": "Naters",
                "sys": {"country": "CH"},
                "main": {"temp": 21.5, "feels_like": 20.8},
                "weather": [{"description": "klarer himmel"}],
            }

    def fake_get(url, params=None, timeout=10):
        return FakeResp()

    # requests.get mocken
    import app.main as m
    monkeypatch.setattr(m.requests, "get", fake_get)

    r = client.get("/weather", params={"city": "Naters"})
    assert r.status_code == 200
    data = r.json()
    assert data["city"] == "Naters"
    assert data["country"] == "CH"
    assert isinstance(data["temp"], (int, float))
    assert history and history[-1]["city"] == "Naters"

def test_weather_bad_city(monkeypatch):
    class FakeBadResp:
        status_code = 404
        ok = False
        def json(self):
            return {"message": "city not found"}

    def fake_get(url, params=None, timeout=10):
        return FakeBadResp()

    import app.main as m
    monkeypatch.setattr(m.requests, "get", fake_get)

    r = client.get("/weather", params={"city": "NowhereLand"})
    assert r.status_code == 404
    assert "Wetter-API" in r.json()["detail"]

def test_history_add_and_get():
    entry = {"city": "Bern", "temp": 18.0}
    r1 = client.post("/history", json=entry)
    assert r1.status_code == 200

    r2 = client.get("/history")
    assert r2.status_code == 200
    data = r2.json()
    assert len(data) == 1
    assert data[0]["city"] == "Bern"

def test_alert_dummy():
    payload = {"type": "storm", "threshold": "high"}
    r = client.post("/alert", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["data"]["type"] == "storm"
