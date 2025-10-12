"""Pydantic-Modelle für das Weather-Backend."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class WeatherReport(BaseModel):
    """Ein einzelner Wetterbericht, wie er von der API geliefert wird."""

    city: str = Field(..., description="Name der Stadt")
    country: Optional[str] = Field(
        default=None, description="ISO-Ländercode, falls von der API geliefert"
    )
    temp: Optional[float] = Field(
        default=None, description="Aktuelle Temperatur in °C"
    )
    feels_like: Optional[float] = Field(
        default=None, description="Gefühlte Temperatur in °C"
    )
    condition: Optional[str] = Field(
        default=None, description="Beschreibung der Wetterlage"
    )


class HistoryEntry(WeatherReport):
    """Persistierter Wetterbericht inklusive Zeitstempel."""

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Zeitpunkt, an dem die Abfrage gespeichert wurde (UTC)",
    )


class Alert(BaseModel):
    """Einfaches Alert-Objekt, das vom Frontend gesendet werden kann."""

    message: str = Field(..., min_length=1, description="Warntext")


class AlertResponse(BaseModel):
    """Antwortstruktur für gespeicherte Alerts."""

    msg: str
    data: Alert


class HealthResponse(BaseModel):
    """Antwort des Health-Checks."""

    status: str = Field(default="ok")
