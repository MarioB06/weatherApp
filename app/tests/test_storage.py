from datetime import UTC, datetime

from app.models import WeatherReport
from app.storage import WeatherStorage


def test_storage_adds_timestamp():
    storage = WeatherStorage()
    report = WeatherReport(city="Bern", temp=20.0)

    entry = storage.add_history(report)

    assert entry.city == "Bern"
    assert isinstance(entry.timestamp, datetime)
    assert entry.timestamp.tzinfo is UTC
    assert entry.timestamp <= datetime.now(UTC)


def test_storage_list_returns_copy():
    storage = WeatherStorage()
    storage.add_history(WeatherReport(city="Bern"))

    history = storage.list_history()
    history.append(WeatherReport(city="Fake"))  # sollte Original nicht beeinflussen

    assert len(storage.list_history()) == 1
