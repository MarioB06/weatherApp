"""Einfache Settings-Verwaltung ohne zusätzliche Dependencies."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    openweather_api_key: str
    openweather_base_url: str = "https://api.openweathermap.org/data/2.5/weather"


@lru_cache
def get_settings() -> Settings:
    return Settings(
        openweather_api_key=os.getenv("OPENWEATHER_API_KEY", ""),
        openweather_base_url=os.getenv(
            "OPENWEATHER_BASE_URL", "https://api.openweathermap.org/data/2.5/weather"
        ),
    )
