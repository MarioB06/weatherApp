# Projektbewertung (WetterApp)

Bewertung anhand des bereitgestellten Rasters.

| Kategorie | Punkte | Begründung |
| --- | --- | --- |
| Backend Implementation | 5 | FastAPI-Backend mit klarer Fehlerbehandlung, Persistenz und Validierung der Eingaben. Endpunkte für Wetter, Verlauf, Alerts und Healthcheck vorhanden und nutzen strukturierte Modelle. 【F:app/main.py†L1-L75】【F:app/models.py†L1-L46】【F:app/storage.py†L1-L39】 |
| Minimal Frontend UI | 4 | React-Frontend mit Komponenten für Suche, Verlauf und Alerts. Nutzt asynchrone Datenabrufe, Zustand und Tailwind-Styles; kleinere Komfortfunktionen (z. B. Routing) fehlen. 【F:frontend/src/App.jsx†L1-L45】【F:frontend/src/components/WeatherSearch.jsx†L1-L48】【F:frontend/src/components/HistoryList.jsx†L1-L27】 |
| Unit Testing | 4 | Pytest-Suite deckt Speicherschicht und zentrale API-Flows inkl. Fehlerpfaden ab; keine Metriken oder negative Tests für alle Module. 【F:app/tests/test_storage.py†L1-L26】【F:app/tests/test_functional_api.py†L1-L79】 |
| CI with Jenkins | 4 | Jenkinsfile orchestriert Checkout, Backend-Tests, Frontend-Build, Image-Build und optionales Deployment per Docker Compose; keine Qualitäts-Gates wie Linting oder Berichte. 【F:Jenkinsfile†L1-L39】 |
| k6 Load Testing | 3 | K6-Skript mit Ramp-Up-Plan und Basis-Check gegen Wetter-Endpunkt vorhanden, aber ohne Thresholds oder mehrere Szenarien. 【F:loadtests/weather.js†L1-L20】 |
| Playwright | 4 | Playwright-Setup mit Vite-Webserver-Integration und zwei End-to-End-Szenarien, die Fehlermeldungen, Suchfluss und History-Darstellung abdecken. 【F:frontend/playwright.config.js†L1-L29】【F:frontend/tests/weather.spec.js†L1-L47】【F:frontend/package.json†L1-L18】 |
| Grafana | 4 | Docker-Compose-Stack für Loki, Promtail und Grafana inkl. vorkonfigurierter Datasource und Dashboard für Container-Logs. 【F:docker-compose.yml†L24-L64】【F:monitoring/promtail/promtail-config.yml†L1-L22】【F:monitoring/grafana/provisioning/datasources/datasource.yml†L1-L9】【F:monitoring/grafana/dashboards/weather-logs.json†L1-L36】 |

**Gesamtpunkte (gewichtete Summe laut Raster):** 5·20% + 4·20% + 4·15% + 4·15% + 3·15% + 4·10% + 4·5% = **4.05 / 5** (≈81 %).
