# WeatherApp (Modul 324)

Dieses Projekt beinhaltet ein vollständiges Beispiel für das Modul 324 mit Backend (FastAPI), Frontend (React/Vite), Tests, Lasttests, Container-Builds sowie einer Jenkins Pipeline.

## Schnellstart

1. `.env.example` kopieren und `OPENWEATHER_API_KEY` setzen.
2. Docker Compose verwenden:

   ```bash
   docker compose up --build
   ```

   Das Backend läuft anschließend auf `http://localhost:8000`, das Frontend auf `http://localhost:5173`.
   Für das Frontend kann optional `VITE_API_URL` in einer `.env` im `frontend/`-Ordner gesetzt werden.

## Tests

- **Unit-Tests & Functional Tests**: `pytest`
- **Frontend Build**: `cd frontend && npm run build`
- **Load-Test**: `k6 run loadtests/weather.js` (`API_BASE_URL` ggf. setzen)

## Jenkins Pipeline

Die Pipeline (`Jenkinsfile`) führt Checkout, Backend-Tests, Frontend-Build und optionales Deployment per Docker Compose aus. Über den Parameter `DEPLOY` kann das Starten des API-Containers gesteuert werden.

## Monitoring / Health

Der Endpoint `/healthz` liefert einen einfachen Health-Check, der z. B. von Prometheus oder einem Load Balancer abgefragt werden kann.
