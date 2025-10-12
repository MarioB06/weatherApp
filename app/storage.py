"""In-Memory-Speicher für Wetterabfragen."""

from __future__ import annotations

from threading import Lock
from typing import Iterable, List

from .models import HistoryEntry, WeatherReport


class WeatherStorage:
    """Faden-sicherer In-Memory-Speicher für Wetterhistorie."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._history: List[HistoryEntry] = []

    def add_history(self, entry: WeatherReport | HistoryEntry) -> HistoryEntry:
        """Speichert einen Eintrag und gibt ihn inklusive Zeitstempel zurück."""

        history_entry = (
            entry if isinstance(entry, HistoryEntry) else HistoryEntry(**entry.model_dump())
        )
        with self._lock:
            self._history.append(history_entry)
        return history_entry

    def list_history(self) -> list[HistoryEntry]:
        """Gibt eine Kopie der gespeicherten Historie zurück."""

        with self._lock:
            return list(self._history)

    def extend(self, entries: Iterable[WeatherReport | HistoryEntry]) -> None:
        """Hilfsfunktion für Tests, um mehrere Werte vorzubelegen."""

        for entry in entries:
            self.add_history(entry)

    def clear(self) -> None:
        """Löscht alle gespeicherten Einträge."""

        with self._lock:
            self._history.clear()


# Globale Instanz, die vom FastAPI-Container verwendet wird
storage = WeatherStorage()
