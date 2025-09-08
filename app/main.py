from fastapi import FastAPI, HTTPException, Query
import os, requests

app = FastAPI(title="Weather Service")

history = []

# Nutze eine feste ENV-Variable, z. B. OPENWEATHER_API_KEY
API_KEY = "1ae22c96f65feed51923e80599a286f5"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.get("/weather")
def get_weather(city: str = Query(..., min_length=1)):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "de",
    }
    try:
        r = requests.get(BASE_URL, params=params, timeout=10)
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Netzwerkfehler: {e}")

    if not r.ok:
        try:
            payload = r.json()
            # Falls payload kein Dict ist, nimm String-Repräsentation
            msg = payload.get("message") if isinstance(payload, dict) else str(payload)
        except Exception:
            msg = getattr(r, "text", "") or f"HTTP {r.status_code}"
        raise HTTPException(status_code=r.status_code, detail=f"Wetter-API: {msg}")


    data = r.json()
    entry = {
        "city": data.get("name", city),
        "country": data.get("sys", {}).get("country"),
        "temp": data.get("main", {}).get("temp"),
        "feels_like": data.get("main", {}).get("feels_like"),
        "condition": (data.get("weather") or [{}])[0].get("description"),
    }
    history.append(entry)
    return entry

@app.get("/history")
def get_history():
    return history

@app.post("/history")
def add_history(entry: dict):
    history.append(entry)
    return {"msg": "Eintrag hinzugefügt", "data": entry}

@app.post("/alert")
def add_alert(alert: dict):
    return {"msg": "Alert gespeichert", "data": alert}
