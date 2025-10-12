"""Kommunikation mit der externen Wetter-API."""

from __future__ import annotations

from typing import Any

import httpx

from .models import WeatherReport


class WeatherServiceError(RuntimeError):
    """Allgemeiner Fehler des externen Wetterdienstes."""


class WeatherServiceHTTPError(WeatherServiceError):
    """Fehler, ausgelöst durch eine HTTP-Antwort != 2xx."""

    def __init__(self, status_code: int, detail: str | None = None) -> None:
        super().__init__(detail or f"Fehlerhafte Antwort ({status_code})")
        self.status_code = status_code
        self.detail = detail or "Unbekannter Fehler"


async def fetch_weather_report(
    *, city: str, api_key: str, base_url: str
) -> WeatherReport:
    """Fragt das Wetter beim externen Dienst an und gibt ein ``WeatherReport`` zurück."""

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "de",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(base_url, params=params, timeout=10.0)
        except httpx.RequestError as exc:  # pragma: no cover - reine Fehlerbehandlung
            raise WeatherServiceError(f"Netzwerkfehler: {exc}") from exc

    if response.status_code >= 400:
        detail = _extract_error(response)
        raise WeatherServiceHTTPError(response.status_code, detail)

    payload = response.json()
    weather = WeatherReport(
        city=payload.get("name") or city,
        country=(payload.get("sys") or {}).get("country"),
        temp=(payload.get("main") or {}).get("temp"),
        feels_like=(payload.get("main") or {}).get("feels_like"),
        condition=((payload.get("weather") or [{}])[0] or {}).get("description"),
    )
    return weather


def _extract_error(response: httpx.Response) -> str:
    """Hilfsfunktion, um eine sinnvolle Fehlermeldung zu generieren."""

    try:
        payload: Any = response.json()
    except ValueError:
        return response.text or f"HTTP {response.status_code}"

    if isinstance(payload, dict) and payload.get("message"):
        return str(payload.get("message"))
    return str(payload)
