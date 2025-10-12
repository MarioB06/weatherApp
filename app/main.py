"""FastAPI-Anwendung für das Weather-Modul 324."""

from __future__ import annotations

from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query

from .config import Settings, get_settings
from .models import Alert, AlertResponse, HealthResponse, HistoryEntry, WeatherReport
from .storage import storage
from .weather_service import (
    WeatherServiceError,
    WeatherServiceHTTPError,
    fetch_weather_report,
)


app = FastAPI(title="Weather Service", version="1.0.0")


@app.get("/healthz", response_model=HealthResponse, tags=["System"])
async def healthcheck() -> HealthResponse:
    """Einfache Monitoring-Route für Load-Balancer/Prometheus."""

    return HealthResponse()


@app.get("/weather", response_model=HistoryEntry, tags=["Weather"])
async def get_weather(
    city: str = Query(..., min_length=1, description="Stadtname"),
    settings: Settings = Depends(get_settings),
) -> HistoryEntry:
    """Ruft das Wetter für eine Stadt ab und speichert es in der Historie."""

    if not settings.openweather_api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENWEATHER_API_KEY ist nicht gesetzt. Bitte ENV konfigurieren.",
        )

    try:
        report: WeatherReport = await fetch_weather_report(
            city=city,
            api_key=settings.openweather_api_key,
            base_url=settings.openweather_base_url,
        )
    except WeatherServiceHTTPError as exc:
        raise HTTPException(status_code=exc.status_code, detail=f"Wetter-API: {exc.detail}")
    except WeatherServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    entry = storage.add_history(report)
    return entry


@app.get("/history", response_model=List[HistoryEntry], tags=["Weather"])
async def get_history() -> List[HistoryEntry]:
    """Gibt die gespeicherten Wetterabfragen zurück."""

    return storage.list_history()


@app.post("/history", response_model=HistoryEntry, tags=["Weather"])
async def add_history(entry: WeatherReport) -> HistoryEntry:
    """Erlaubt es, eigene Einträge zur Historie hinzuzufügen (z. B. für Tests)."""

    return storage.add_history(entry)


@app.post("/alert", response_model=AlertResponse, tags=["Alerts"])
async def add_alert(alert: Alert) -> AlertResponse:
    """Dummy-Endpunkt, der Alerts entgegennimmt."""

    return AlertResponse(msg="Alert gespeichert", data=alert)
